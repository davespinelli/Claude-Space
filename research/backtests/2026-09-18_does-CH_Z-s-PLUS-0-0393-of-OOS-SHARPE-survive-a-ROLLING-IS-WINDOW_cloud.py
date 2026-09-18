#!/usr/bin/env python3
"""Idea 1201 (lane cloud, 2026-09-18): does CH_Z's +0.0393 of OOS SHARPE survive a
ROLLING IS WINDOW?

QUESTION.  Idea 1197 found that the null-standardised z (CH_Z) beats the saturated null
percentile (CH_PCT) by 0.0393 of mean OOS Sharpe over 18 (panel, K) picks.  But every one
of those picks came from ONE 2009-2016 / 2017-2026 split: three panels x one decision each,
re-seeded.  Three picks cannot separate two choosers.  This run gives each chooser DOZENS
of picks by rolling the IS window forward across the whole tape and re-deciding, and asks
whether the gap survives, reverses, or was a two-draw accident.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    WINDOW {252, 504, 756, 1008, 1260} trading days — the length of the trailing IS window
           each decision is made on.
    STEP   {21, 63, 126} trading days — how often the chooser is allowed to re-decide, and
           therefore how long each pick is held before it can be revised.
  5 x 3 = 15 cells per (panel, chooser).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); CHOOSER {CH_PCT,
CH_Z, CH_ISSHARPE, DO_NOTHING}; both KEEP paths leg by leg; full / halves / IS / OOS;
turnover; switch counts; the switching cost charged and uncharged.

THE CANDIDATE SET IS 1197'S, FROZEN, NOT RE-CHOSEN HERE.  Four anchor books per panel,
(N, cadence) in {(20,W), (12,W), (20,M), (10,M)}: composite of 12-1 / 6m / 3m percentile
ranks, eligibility = above own 200d MA, top-N equal weight at GROSS/N = 0.75/N of NAV,
gated-out weight to CASH, 10 bps per unit turnover, next-day execution, 260-row warm-up.
Identical construction to 1197's book_weights / run_from_starts, so this run's anchors are
the same objects its numbers were computed on (gate G4 replays 1197's own IS reading).

THE CHOOSERS.  At each decision date d the trailing WINDOW of returns is read for the
anchor and for a pool of NDRAW = 200 GROSS-MATCHED null books built for that anchor's own
(N, cadence) — at each rebalance row N names drawn uniformly from those priced, weight
0.75/N, no score.  Then
    CH_PCT      = share of the pool whose window Sharpe the anchor beats   (1197's statistic)
    CH_Z        = (anchor window Sharpe - pool mean) / pool sd             (1197's challenger)
    CH_ISSHARPE = the anchor's own window Sharpe, no null at all           (free control)
    DO_NOTHING  = always anchor (20, W), the record's incumbent shape       (the bar that matters)
Ties are broken FIRST-WINS in the frozen anchor order, which is 1197's own habit and idea
1202's open question; the tie rate is published per cell so the reader can see how often it
binds.  The pick earns that anchor's returns over the NEXT STEP days and nothing else is
carried forward — the realised chooser book is the concatenation of those segments, which is
what a real account would have held.

K IS NOT A DIAL HERE and is frozen at the full pool (NDRAW = 200 draws at every decision),
i.e. each chooser is given the MOST resolved version of its own statistic.  1197's K ladder
established that CH_PCT saturates at every K on the large-cap panels; giving it the largest
pool this run can afford is the setting most favourable to it, so a CH_PCT loss here is not
a draw-count artefact.

SWITCHING IS CHARGED, NOT ASSUMED FREE.  When the pick changes at a decision date the
realised book pays 2 * GROSS * 10 bps (a full liquidation and a full rebuild) on that day.
That is an UPPER bound — two momentum books usually overlap in names — so the charged series
is pessimistic and the uncharged one optimistic; both are published at every cell, and the
verdict is read off the charged one.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) THE GAP SURVIVES — CH_Z beats CH_PCT on mean OOS Sharpe across the 15 cells with the
      same sign and a comparable size to 1197's +0.0393.  Then the null-standardised form is
      a real improvement and the PROTOCOL should say so.
  (B) THE GAP VANISHES — the two choosers are inside noise of each other once each makes
      dozens of picks.  Then 1197's +0.0393 was three draws and the record should stop
      quoting it as a measurement.
  (C) THE GAP REVERSES.
  (D) NEITHER CHOOSER BEATS DO-NOTHING — both lose to always holding the incumbent anchor.
      That is the capital finding regardless of which of (A)-(C) fires, and it is the one
      this run reports first.

RULE 8 (walk-forward, required).  The picks are already walk-forward by construction.  On
top of that, the DIALS themselves are chosen honestly: (WINDOW, STEP) is picked on
warm-up..2016-12-31 by IS Sharpe ALONE, per (panel, chooser), and 2017-2026 is read ONCE.
Reported against (i) DO_NOTHING over the same rows, (ii) the mean over all 15 cells, (iii)
the worst cell, with the IS/OOS rank correlation over the 15.  The capital verdict is the
sign of chooser-minus-do-nothing, never the best cell.

BENCHMARKS ARE RECOMPUTED ON EACH CELL'S OWN ROWS.  A long WINDOW starts the realised book
later, so SPY, the LIVE RULES v2 baseline and DO_NOTHING are re-measured over exactly the
rows that cell's realised book covers.  Without that, 4a and 4b would compare books drawn on
different tapes.  The OOS segment (2017-01-01 onward) is common to every cell.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 (20,W) anchor post-warm-up.
G2 determinism: the null pool and the whole U56 grid recompute bit for bit.  G3 the null is
gross-matched — target gross 0.75 on every rebalance row.  G4 replays 1197's IS reading:
CH_PCT saturation share and the anchors tied at its maximum on the 2009-2016 window.  G5 the
cumsum window-Sharpe used for the rolling decisions equals the direct computation to 1e-10.
G6 the DO_NOTHING realised series equals the plain (20,W) anchor on the same rows (the
chooser harness adds nothing when the pick never moves).

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an UPPER bound.  The headline is a CONTRAST between two choosers picking from the SAME four
books on the SAME tape, which is first-order immune to a level bias that moves all of them
together; the 4a/4b legs are not.

Runs standalone and offline (committed price caches only).
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

DATE = "2026-09-18"
SLUG = "does-CH_Z-s-PLUS-0-0393-of-OOS-SHARPE-survive-a-ROLLING-IS-WINDOW"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, GROSS, WARMUP = 10.0, 0.75, 260
ANCHORS = [(20, "W"), (12, "W"), (20, "M"), (10, "M")]   # 1197's frozen candidate set
DO_NOTHING_ANCHOR = 0                                    # (20, W), the incumbent shape
NDRAW = 200                                              # frozen, NOT a dial (see docstring)
SEED0 = 1201
WINDOWS = [252, 504, 756, 1008, 1260]                    # DIAL 1
STEPS = [21, 63, 126]                                    # DIAL 2
CHOOSERS = ["CH_PCT", "CH_Z", "CH_ISSHARPE", "DO_NOTHING"]
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SWITCH_COST = 2.0 * GROSS * COST / 1e4                   # upper-bound round trip

_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
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
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def windows_of(idx, r, i_oos):
    """full / halves / IS / OOS over a return vector aligned to idx."""
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:i_oos]), oos=stats(r[i_oos:]))


def flat(w):
    return {f"{k}_{m}": v for k, d in w.items() for m, v in d.items()}


# ------------------------------------------------------------------ panel / runner
class Panel:
    """1197's Panel, unchanged arithmetic."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.P = np.cumprod(1.0 + self.rets, axis=0)
        self.Pprev = np.vstack([np.ones((1, self.P.shape[1])), self.P[:-1]])
        self.priced = px.notna().values
        self.seg = {}
        for f in {a[1] for a in ANCHORS}:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            s = np.flatnonzero(m)
            self.seg[f] = (s, np.append(s[1:], len(px)))
        self.idx = px.index
        self.i0 = WARMUP
        self.ioos = int(px.index.searchsorted(OOS_START))
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def run_from_starts(pan, freq, Wstart):
    starts, ends = pan.seg[freq]
    T, M = pan.rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    cur = np.zeros(M)
    for k, (i0, i1) in enumerate(zip(starts, ends)):
        w0 = Wstart[k]
        turn[i0] = np.abs(w0 - cur).sum()
        base = pan.Pprev[i0]
        A = w0[None, :] * (pan.Pprev[i0:i1] / base[None, :])
        cash0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + cash0
        held[i0:i1] = A / V[:, None]
        Aend = w0 * (pan.P[i1 - 1] / base)
        cur = Aend / (Aend.sum() + cash0)
    return (held * pan.rets).sum(axis=1) - turn * COST / 1e4, turn


def starts_from_weights(pan, freq, W):
    starts, _ = pan.seg[freq]
    Wv = W.reindex(pan.px.index).fillna(0.0).shift(1).fillna(0.0).values
    return Wv[starts]


def book_weights(pan, n):
    q = pan.px[pan.invest]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3
    elig = comp.where(q > q.rolling(200).mean())
    rk = elig.rank(axis=1, ascending=False)
    W = pd.DataFrame(0.0, index=pan.px.index, columns=pan.px.columns)
    W[pan.invest] = (rk <= n).astype(float) * (GROSS / n)
    return W


def null_starts(pan, freq, n, rng):
    starts, _ = pan.seg[freq]
    out = np.zeros((len(starts), pan.rets.shape[1]))
    for k, i in enumerate(starts):
        avail = pan.iinv[pan.priced[max(i - 1, 0)][pan.iinv]]
        if len(avail) < n:
            continue
        out[k, rng.choice(avail, size=n, replace=False)] = GROSS / n
    return out


# ------------------------------------------------------------------ rolling window Sharpe
class RollSharpe:
    """O(1) trailing-window Sharpe for a stack of return series via prefix sums."""

    def __init__(self, R):                      # R: (D, T) or (T,)
        R = np.atleast_2d(np.asarray(R, float))
        z = np.zeros((R.shape[0], 1))
        self.c1 = np.concatenate([z, np.cumsum(R, axis=1)], axis=1)
        self.c2 = np.concatenate([z, np.cumsum(R * R, axis=1)], axis=1)

    def at(self, d, W):
        """Sharpe over rows [d-W, d)."""
        s1 = self.c1[:, d] - self.c1[:, d - W]
        s2 = self.c2[:, d] - self.c2[:, d - W]
        m = s1 / W
        v = np.maximum(s2 / W - m * m, 0.0)
        sd = np.sqrt(v)
        out = np.where(sd > 0, m * 252.0 / (sd * np.sqrt(252.0)), np.nan)
        return out


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ the chooser harness
def realise(pan, anchor_R, rs_anchor, rs_null, chooser, W, S):
    """Roll the IS window, decide, hold STEP days.  Returns (start_row, charged, uncharged,
    picks, n_switch, tie_rate)."""
    T = anchor_R.shape[1]
    d0 = pan.i0 + W
    if d0 >= T - 20:
        return None
    dates = list(range(d0, T, S))
    charged = np.zeros(T)
    unch = np.zeros(T)
    picks, ties, last = [], 0, None
    for d in dates:
        if chooser == "DO_NOTHING":
            j = DO_NOTHING_ANCHOR
        else:
            sc = np.empty(len(ANCHORS))
            for a in range(len(ANCHORS)):
                sa = rs_anchor[a].at(d, W)[0]
                if chooser == "CH_ISSHARPE":
                    sc[a] = sa
                else:
                    pool = rs_null[a].at(d, W)
                    pool = pool[np.isfinite(pool)]
                    if len(pool) < 10 or not np.isfinite(sa):
                        sc[a] = -np.inf
                    elif chooser == "CH_PCT":
                        sc[a] = float((pool < sa).mean())
                    else:
                        sd = pool.std(ddof=1)
                        sc[a] = float((sa - pool.mean()) / sd) if sd > 0 else -np.inf
            m = np.nanmax(sc)
            if np.sum(sc == m) > 1:
                ties += 1
            j = int(np.flatnonzero(sc == m)[0])          # FIRST-WINS, 1197's habit
        e = min(d + S, T)
        charged[d:e] = anchor_R[j, d:e]
        unch[d:e] = anchor_R[j, d:e]
        if last is not None and j != last:
            charged[d] -= SWITCH_COST
        picks.append(j)
        last = j
    nsw = sum(1 for i in range(1, len(picks)) if picks[i] != picks[i - 1])
    return d0, charged[d0:], unch[d0:], picks, nsw, ties / max(len(picks), 1)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1201 lane cloud — {SLUG}")
    say(f"# candidate set (frozen, 1197's): anchors {ANCHORS}, composite 12-1/6m/3m ranks, "
        f"above-200d-MA, top-N equal weight at GROSS/N = {GROSS}/N, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 WINDOW = {WINDOWS} days      DIAL 2 STEP = {STEPS} days")
    say(f"# choosers {CHOOSERS} (DO_NOTHING = always anchor {ANCHORS[DO_NOTHING_ANCHOR]})")
    say(f"# frozen constants (NOT dials): NDRAW = {NDRAW} null draws per decision, "
        f"switch charge = {SWITCH_COST*1e4:.1f} bps of NAV per changed pick, FIRST-WINS ties")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows, bookrows = [], [], []
    u56_check = None

    for pi, (pname, p_px, inv) in enumerate(panels):
        pan = Panel(pname, p_px, inv)
        T = pan.rets.shape[0]
        say(f"\n## {pname}  n_days={T}  n_names={len(inv)}  "
            f"{pan.idx[0].date()}..{pan.idx[-1].date()}  OOS row {pan.ioos}")

        # ---- the four anchor books
        anchor_R = np.zeros((len(ANCHORS), T))
        for a, (n, freq) in enumerate(ANCHORS):
            W = book_weights(pan, n)
            r, _ = run_from_starts(pan, freq, starts_from_weights(pan, freq, W))
            anchor_R[a] = r
            if pi == 0 and a == 0:
                eng = backtest(p_px, W, cost_bps=COST, freq=freq)["returns"].values
                d = float(np.nanmax(np.abs(np.asarray(eng[pan.i0:], float) - r[pan.i0:])))
                gate("G1 fast runner == engine.backtest (U56 20/W, post-warm-up)",
                     f"{d:.3e}", "< 1e-12", d < 1e-12)
            w = windows_of(pan.idx[pan.i0:], r[pan.i0:], pan.ioos - pan.i0)
            bookrows.append(dict(panel=pname, N=n, cadence=freq, **flat(w)))
            say(f"   anchor N={n:2d}/{freq}  full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / "
                f"{w['full']['MaxDD']:7.2%}   IS Sh {w['is_']['Sharpe']:.4f}   OOS {w['oos']['Sharpe']:.4f}")

        # ---- the null pools, one per anchor
        null_R = []
        for a, (n, freq) in enumerate(ANCHORS):
            cell = 1000 * (pi + 1) + a
            NR = np.zeros((NDRAW, T))
            for d_ in range(NDRAW):
                rng = np.random.default_rng(SEED0 + 100003 * cell + d_)
                st = null_starts(pan, freq, n, rng)
                if pi == 0 and a == 0 and d_ == 0:
                    gm = float(np.abs(st.sum(axis=1) - GROSS).max())
                    gate("G3 null gross-matched at every rebalance row", f"{gm:.3e}", "< 1e-12",
                         gm < 1e-12)
                NR[d_], _ = run_from_starts(pan, freq, st)
            null_R.append(NR)
            say(f"   null pool N={n:2d}/{freq}: {NDRAW} draws, IS Sharpe mean "
                f"{np.nanmean([sharpe(x[pan.i0:pan.ioos]) for x in NR]):.4f}  t={time.time()-t0:.0f}s")

        rs_anchor = [RollSharpe(anchor_R[a]) for a in range(len(ANCHORS))]
        rs_null = [RollSharpe(null_R[a]) for a in range(len(ANCHORS))]

        # ---- G5 / G4 on the first panel
        if pi == 0:
            d = pan.i0 + 1008
            direct = np.array([sharpe(anchor_R[a][d - 1008:d]) for a in range(len(ANCHORS))])
            viacs = np.array([rs_anchor[a].at(d, 1008)[0] for a in range(len(ANCHORS))])
            e = float(np.max(np.abs(direct - viacs)))
            gate("G5 cumsum window Sharpe == direct", f"{e:.3e}", "< 1e-10", e < 1e-10)
        # G4: 1197's own IS reading, full 2009-2016 window at the full pool
        d_is = pan.ioos
        Wis = d_is - pan.i0
        pcts, zs = [], []
        for a in range(len(ANCHORS)):
            sa = rs_anchor[a].at(d_is, Wis)[0]
            pool = rs_null[a].at(d_is, Wis)
            pool = pool[np.isfinite(pool)]
            pcts.append(float((pool < sa).mean()))
            zs.append(float((sa - pool.mean()) / pool.std(ddof=1)))
        sat = float(np.mean(np.array(pcts) >= 1.0 - 1e-12))
        tied = int(np.sum(np.array(pcts) == max(pcts)))
        say(f"   1197 IS replay: CH_PCT {['%.3f' % x for x in pcts]} (saturated share {sat:.3f}, "
            f"{tied} of 4 tied at max)   CH_Z {['%.2f' % x for x in zs]}")
        if pi < 2:
            gate(f"G4 CH_PCT saturated / tied at max on the 2009-2016 window ({pname})",
                 f"sat {sat:.3f}, tied {tied}/4", "1197: saturated on both large-cap panels",
                 sat >= 0.5)

        # ---- benchmarks (recomputed per cell's rows below)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values

        say("\n   chooser     WIN STEP |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe |  OOS Sh | sw ties | 4a 4b | fail4b")
        cells = {}
        for chooser in CHOOSERS:
            for W in WINDOWS:
                for S in STEPS:
                    out = realise(pan, anchor_R, rs_anchor, rs_null, chooser, W, S)
                    if out is None:
                        continue
                    d0, rc, ru, picks, nsw, tie = out
                    idx = pan.idx[d0:]
                    i_oos = max(int(np.searchsorted(idx.values, OOS_START.to_datetime64())), 1)
                    wc = windows_of(idx, rc, i_oos)
                    wu = windows_of(idx, ru, i_oos)
                    spy = windows_of(idx, pan.spy[d0:], i_oos)
                    live = windows_of(idx, live_r[d0:], i_oos)
                    a4, b4 = legs_4a(wc, live), legs_4b(wc, spy)
                    rec = dict(panel=pname, chooser=chooser, window=W, step=S,
                               start=str(idx[0].date()), n_dec=len(picks), n_switch=nsw,
                               tie_rate=tie, **flat(wc),
                               unch_full_Sharpe=wu["full"]["Sharpe"], unch_oos_Sharpe=wu["oos"]["Sharpe"],
                               spy_full_Sharpe=spy["full"]["Sharpe"], spy_oos_Sharpe=spy["oos"]["Sharpe"],
                               spy_full_MaxDD=spy["full"]["MaxDD"], spy_full_CAGR=spy["full"]["CAGR"],
                               live_full_Sharpe=live["full"]["Sharpe"], live_oos_Sharpe=live["oos"]["Sharpe"],
                               pick_share_A0=float(np.mean(np.array(picks) == 0)),
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(chooser, W, S)] = rec
                    say(f"   {chooser:11s} {W:4d} {S:4d} | {wc['full']['CAGR']:7.2%} "
                        f"{wc['full']['Sharpe']:8.4f} {wc['full']['MaxDD']:8.2%} | "
                        f"{wc['h1']['Sharpe']:.4f}/{wc['h2']['Sharpe']:.4f} | {wc['oos']['Sharpe']:7.4f} | "
                        f"{nsw:2d} {tie:4.2f} | {'Y' if all(a4.values()) else 'n'}  "
                        f"{'Y' if all(b4.values()) else 'n'} | {failed(b4)}")

        # ---- G6 DO_NOTHING == the plain anchor on the same rows
        k = ("DO_NOTHING", WINDOWS[0], STEPS[0])
        if k in cells:
            d0 = pan.i0 + WINDOWS[0]
            e = abs(cells[k]["unch_full_Sharpe"] - sharpe(anchor_R[DO_NOTHING_ANCHOR][d0:]))
            if pi == 0:
                gate("G6 DO_NOTHING realised == plain (20,W) anchor on the same rows",
                     f"{e:.3e}", "< 1e-12", e < 1e-12)

        # ---- the head-to-head 1201 asks about
        for scope in ["full_Sharpe", "oos_Sharpe"]:
            dz = [cells[("CH_Z", W, S)][scope] - cells[("CH_PCT", W, S)][scope]
                  for W in WINDOWS for S in STEPS if ("CH_Z", W, S) in cells]
            say(f"   HEAD-TO-HEAD {scope:12s} CH_Z - CH_PCT over {len(dz)} cells: "
                f"mean {np.mean(dz):+.4f}  median {np.median(dz):+.4f}  "
                f"min {np.min(dz):+.4f}  max {np.max(dz):+.4f}  "
                f"CH_Z ahead at {int(np.sum(np.array(dz) > 0))} of {len(dz)}")

        # ---- rule 8: choose (WINDOW, STEP) on IS only, read OOS once
        for chooser in CHOOSERS:
            ks = [(W, S) for W in WINDOWS for S in STEPS if (chooser, W, S) in cells]
            is_s = np.array([cells[(chooser, W, S)]["is__Sharpe"] for W, S in ks])
            oos_s = np.array([cells[(chooser, W, S)]["oos_Sharpe"] for W, S in ks])
            pick = ks[int(np.nanargmax(is_s))]
            dn = cells[("DO_NOTHING", pick[0], pick[1])]
            r8 = dict(panel=pname, chooser=chooser, pick_window=pick[0], pick_step=pick[1],
                      pick_IS=cells[(chooser, *pick)]["is__Sharpe"],
                      pick_OOS=cells[(chooser, *pick)]["oos_Sharpe"],
                      donothing_OOS=dn["oos_Sharpe"],
                      delta=cells[(chooser, *pick)]["oos_Sharpe"] - dn["oos_Sharpe"],
                      pick_OOS_CAGR=cells[(chooser, *pick)]["oos_CAGR"],
                      pick_OOS_MaxDD=cells[(chooser, *pick)]["oos_MaxDD"],
                      donothing_OOS_CAGR=dn["oos_CAGR"], donothing_OOS_MaxDD=dn["oos_MaxDD"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      spy_OOS=cells[(chooser, *pick)]["spy_oos_Sharpe"],
                      live_OOS=cells[(chooser, *pick)]["live_oos_Sharpe"],
                      pick_keep4a=cells[(chooser, *pick)]["keep4a"],
                      pick_keep4b=cells[(chooser, *pick)]["keep4b"])
            r8rows.append(r8)
            say(f"   RULE 8  {chooser:11s} IS-argmax = WINDOW {pick[0]} / STEP {pick[1]} "
                f"(IS Sh {r8['pick_IS']:.4f}) -> OOS {r8['pick_OOS']:.4f}  vs do-nothing "
                f"{r8['donothing_OOS']:.4f}  delta {r8['delta']:+.4f}   cellmean {r8['cellmean_OOS']:.4f} "
                f" worst {r8['worst_OOS']:.4f}  rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

        if pi == 0:
            u56_check = (pan, anchor_R, rs_anchor, rs_null,
                         {k: v["full_Sharpe"] for k, v in cells.items()})

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(bookrows).to_csv(f"{STEM}.books.csv", index=False)

    # ---- G2 determinism: re-run the whole U56 grid
    pan, anchor_R, rs_anchor, rs_null, ref = u56_check
    worst = 0.0
    for (chooser, W, S), v in ref.items():
        out = realise(pan, anchor_R, rs_anchor, rs_null, chooser, W, S)
        worst = max(worst, abs(sharpe(out[1]) - v))
    gate("G2 determinism (U56 grid re-run)", f"{worst:.3e}", "== 0.0", worst == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- summary
    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for chooser in CHOOSERS:
            g = grid[(grid.panel == pname) & (grid.chooser == chooser)]
            if not len(g):
                continue
            say(f"   {pname:9s} {chooser:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}  "
                f"full Sharpe {g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f}  "
                f"OOS Sharpe {g.oos_Sharpe.min():.4f}..{g.oos_Sharpe.max():.4f}  "
                f"switches {int(g.n_switch.min())}..{int(g.n_switch.max())}")
    wf = pd.DataFrame(r8rows)
    for chooser in ["CH_PCT", "CH_Z", "CH_ISSHARPE"]:
        s = wf[wf.chooser == chooser]
        say(f"   RULE 8 {chooser:11s} chooser-minus-do-nothing: {s.delta.round(4).tolist()}  "
            f"mean {s.delta.mean():+.4f}  beats do-nothing at {int((s.delta > 0).sum())} of {len(s)}")
    dz_full, dz_oos = [], []
    for pname in grid.panel.unique():
        for W in WINDOWS:
            for S in STEPS:
                z = grid[(grid.panel == pname) & (grid.chooser == "CH_Z") & (grid.window == W) & (grid.step == S)]
                p = grid[(grid.panel == pname) & (grid.chooser == "CH_PCT") & (grid.window == W) & (grid.step == S)]
                if len(z) and len(p):
                    dz_full.append(float(z.full_Sharpe.iloc[0] - p.full_Sharpe.iloc[0]))
                    dz_oos.append(float(z.oos_Sharpe.iloc[0] - p.oos_Sharpe.iloc[0]))
    say(f"   1201 ANSWER — CH_Z minus CH_PCT over all {len(dz_oos)} (panel, WINDOW, STEP) cells: "
        f"OOS Sharpe mean {np.mean(dz_oos):+.4f} (1197 reported +0.0393), "
        f"full Sharpe mean {np.mean(dz_full):+.4f}, CH_Z ahead OOS at "
        f"{int(np.sum(np.array(dz_oos) > 0))} of {len(dz_oos)}, "
        f"paired t {np.mean(dz_oos)/ (np.std(dz_oos, ddof=1)/np.sqrt(len(dz_oos))):+.2f}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
