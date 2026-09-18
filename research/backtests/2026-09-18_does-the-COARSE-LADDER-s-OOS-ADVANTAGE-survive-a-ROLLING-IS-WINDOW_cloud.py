#!/usr/bin/env python3
"""Idea 1183 (lane cloud, 2026-09-18): does the COARSE LADDER's OOS ADVANTAGE survive a
ROLLING IS WINDOW?

QUESTION.  Idea 1174 found that an IS-only chooser restricted to the three-rung hold ladder
{21, 63, 126} beat one allowed all 16 rungs by +0.0559 of mean OOS Sharpe.  Every one of
those picks came from ONE 2009-2016 / 2017-2016 split: one decision per (panel, N) family,
i.e. two picks per ladder on the tape.  Two picks cannot separate two ladders.  This run
gives each ladder DOZENS of picks by rolling the IS window forward and re-deciding, and asks
whether the coarse ladder's advantage is a measurement or a two-draw accident.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    WINDOW {252, 504, 756, 1008, 1260} trading days — the trailing IS window each decision
           is made on.
    STEP   {21, 63, 126} trading days — how often the chooser may re-decide, and therefore
           how long each pick is held before it can be revised.
  5 x 3 = 15 cells per (panel, arm).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); ARM {L3, L7, L16,
DO_NOTHING}; both KEEP paths leg by leg; full / halves / IS / OOS; switch counts; the
switching cost charged and uncharged; the realised pick distribution over the rungs.

THE BOOK FAMILY IS 1082/1174'S, FROZEN, NOT RE-CHOSEN HERE.  CAND20 composite of the
12-1 / 6m / 3m percentile ranks; eligibility = above own 200d MA AND 20d vol < 0.60;
MIN-HOLD H (a name is replaced only once it is H days old); N = 20 slots; equal weight
GROSS/len(selected) at GROSS = 0.75 of NAV; gated-out weight to CASH; weekly rebalance;
10 bps per unit turnover; next-day execution (LAG 1); 260-row warm-up.  N is FROZEN at the
incumbent 20 and is not a dial — 1174's headline is about the H axis.

THE LADDERS (strictly nested, identical range 21..126, 1174's own rung sets):
    L3  = [21, 63, 126]                                   the record's three-point ladder
    L7  = [21, 42, 52, 63, 76, 90, 126]                    reported, not a dial
    L16 = L7 + [26, 32, 37, 47, 57, 69, 83, 105, 115]      the finest ladder 1174 walked
    DO_NOTHING = always H = 63, the incumbent hold, no choosing at all.  This is the bar
    that matters for capital: a chooser that loses to holding one book is not a chooser.

THE CHOOSER IS IS-SHARPE, THE SAME ONE 1174 USED.  At each decision date d the trailing
WINDOW of the realised returns of every rung IN THAT ARM'S LADDER is read and the rung with
the highest window Sharpe is taken.  Ties break FIRST-WINS in ascending rung order (idea
1202's open question); the tie rate is published per cell.  The pick earns that rung's
returns over the NEXT STEP days and nothing else is carried forward — the realised book is
the concatenation of those segments, which is what a real account would have held.

SWITCHING IS CHARGED, NOT ASSUMED FREE.  When the pick changes at a decision date the
realised book pays 2 * GROSS * 10 bps (a full liquidation and a full rebuild) that day.
That is an UPPER bound — two min-hold books at neighbouring H share most of their names, and
the finer ladder switches more often, so the charge is the conservative direction for the
question asked.  Both the charged and the uncharged series are published at every cell and
the verdict is read off the CHARGED one.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) THE ADVANTAGE SURVIVES — L3 beats L16 on mean OOS Sharpe across the 15 cells with the
      same sign and a comparable size to 1174's +0.0559.  Then coarsening the ladder is a
      real defence against selection noise and the PROTOCOL should say so.
  (B) THE ADVANTAGE VANISHES — the two ladders are inside noise of each other once each
      makes dozens of picks.  Then 1174's +0.0559 was two draws.
  (C) THE ADVANTAGE REVERSES — the fine ladder wins.
  (D) NEITHER LADDER BEATS DO-NOTHING — both lose to always holding H = 63.  That is the
      capital finding whichever of (A)-(C) fires, and it is reported first.

RULE 8 (walk-forward, required).  The picks are walk-forward by construction.  On top of
that the DIALS are chosen honestly: (WINDOW, STEP) is picked on warm-up..2016-12-31 by IS
Sharpe ALONE, per (panel, arm), and 2017-2026 is read ONCE.  Reported against (i) DO_NOTHING
over the same rows, (ii) the mean over all 15 cells, (iii) the worst cell, with the IS/OOS
rank correlation over the 15.  The capital verdict is the sign of arm-minus-do-nothing,
never the best cell.

BENCHMARKS ARE RECOMPUTED ON EACH CELL'S OWN ROWS.  A long WINDOW starts the realised book
later, so SPY, the LIVE RULES v2 baseline and DO_NOTHING are re-measured over exactly the
rows that cell covers.  Without that, 4a and 4b would compare books drawn on different
tapes.  The OOS segment (2017-01-01 onward) is common to every cell.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 N=20 H=126 book post
warm-up.  G2 CROSS-RUN: that book's (CAGR, Sharpe, MaxDD) reproduces 936/1071/1082/1086/
1093/1174's committed triple (0.155787, 1.139701, -0.191276).  G3 CROSS-RUN SPY OOS triple
(0.1521, 0.8713, -0.3372).  BOTH cross-run gates are read on the tape TRUNCATED to
2026-09-15, which is where the tape ended when those numbers were committed; this run's cache
carries two further rows and two days are worth 0.0034 of SPY's OOS Sharpe.  The live-tape
readings are printed beside them, ungated, so the reader sees both.  G4 the live RULES v2 MaxDD == the committed -12.05%.  G5 the
cumsum window Sharpe equals the direct computation to 1e-10.  G6 DO_NOTHING's realised
series equals the plain H=63 book on the same rows (the harness adds nothing when the pick
never moves).  G7 the ladders are strictly nested L3 c L7 c L16.  G8 determinism: the whole
U56 grid recomputes bit for bit.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an UPPER bound.  The headline is a CONTRAST between two ladders choosing from the SAME books
on the SAME tape, which is first-order immune to a level bias that moves all of them
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
SLUG = "does-the-COARSE-LADDER-s-OOS-ADVANTAGE-survive-a-ROLLING-IS-WINDOW"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (NOT dials), identical to 1082/1174 --------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
COST = 10.0
GROSS = 0.75
FREQ = "W"
NSLOT = 20
LEGS = [(21, 252), (0, 126), (0, 63)]
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SWITCH_COST = 2.0 * GROSS * COST / 1e4

# ---- the ladders ---------------------------------------------------------------------------
L3 = [21, 63, 126]
L7 = [21, 42, 52, 63, 76, 90, 126]
L16 = sorted(set(L7) | {26, 32, 37, 47, 57, 69, 83, 105, 115})
LADDERS = {"L3": L3, "L7": L7, "L16": L16}
HS = L16
HIDX = {h: i for i, h in enumerate(HS)}
DO_NOTHING_H = 63
ARMS = ["L3", "L7", "L16", "DO_NOTHING"]

# ---- the two dials -------------------------------------------------------------------------
WINDOWS = [252, 504, 756, 1008, 1260]
STEPS = [21, 63, 126]

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
# The committed triples above were measured on the tape as it stood on 2026-09-17, which ends
# 2026-09-15; this run's cache carries two more rows.  Two days move SPY's OOS Sharpe by
# 0.0034, so the cross-run gates are checked on the TRUNCATED tape (an exact equality on the
# same rows) and the live-tape readings are printed beside them, ungated.
COMMIT_TAPE_END = "2026-09-15"

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


def windows_of(r, i_oos):
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:i_oos]), oos=stats(r[i_oos:]))


def flat(w):
    return {f"{k}_{m}": v for k, d in w.items() for m, v in d.items()}


# ------------------------------------------------------------------ the frozen book machinery
def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1082's build(), unmodified: MIN HOLD H, N slots, cap INF, equal weight gross/len(sel)."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def nrun(rets, wt, mk):
    """1082/1174's fast runner: gross return and turnover of a weight path."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


# ------------------------------------------------------------------ rolling window Sharpe
class RollSharpe:
    """O(1) trailing-window Sharpe for a stack of return series via prefix sums."""

    def __init__(self, R):
        R = np.atleast_2d(np.asarray(R, float))
        z = np.zeros((R.shape[0], 1))
        self.c1 = np.concatenate([z, np.cumsum(R, axis=1)], axis=1)
        self.c2 = np.concatenate([z, np.cumsum(R * R, axis=1)], axis=1)

    def at(self, d, W):
        s1 = self.c1[:, d] - self.c1[:, d - W]
        s2 = self.c2[:, d] - self.c2[:, d - W]
        m = s1 / W
        sd = np.sqrt(np.maximum(s2 / W - m * m, 0.0))
        return np.where(sd > 0, m * np.sqrt(252.0) / sd, np.nan)


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
def realise(R, rs, arm, W, S, i0):
    """Roll the IS window, decide, hold STEP days.  R: (16, T) rung returns."""
    T = R.shape[1]
    d0 = i0 + W
    if d0 >= T - 60:
        return None
    rungs = [HIDX[h] for h in LADDERS[arm]] if arm != "DO_NOTHING" else [HIDX[DO_NOTHING_H]]
    charged = np.zeros(T)
    unch = np.zeros(T)
    picks, ties, last = [], 0, None
    for d in range(d0, T, S):
        if arm == "DO_NOTHING":
            j = HIDX[DO_NOTHING_H]
        else:
            sc = rs.at(d, W)[rungs]
            sc = np.where(np.isfinite(sc), sc, -np.inf)
            m = sc.max()
            if np.sum(sc == m) > 1:
                ties += 1
            j = rungs[int(np.flatnonzero(sc == m)[0])]     # FIRST-WINS, ascending rung order
        e = min(d + S, T)
        charged[d:e] = R[j, d:e]
        unch[d:e] = R[j, d:e]
        if last is not None and j != last:
            charged[d] -= SWITCH_COST
        picks.append(j)
        last = j
    nsw = sum(1 for i in range(1, len(picks)) if picks[i] != picks[i - 1])
    return d0, charged[d0:], unch[d0:], picks, nsw, ties / max(len(picks), 1)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1183 lane cloud — {SLUG}")
    say(f"# frozen book family: CAND20 legs {LEGS}, elig above-200d & vol20 < {MAXVOL}, "
        f"MIN-HOLD H, N = {NSLOT} slots, gross {GROSS}, {FREQ} cadence, {COST:.0f} bps, "
        f"t+{LAG}, warm-up {WARMUP}")
    say(f"# ladders  L3  = {L3}")
    say(f"#          L7  = {L7}")
    say(f"#          L16 = {L16}")
    say(f"#          DO_NOTHING = always H = {DO_NOTHING_H}")
    say(f"# DIAL 1 WINDOW = {WINDOWS} days      DIAL 2 STEP = {STEPS} days   ({len(WINDOWS)*len(STEPS)} cells per panel-arm)")
    say(f"# switch charge = {SWITCH_COST*1e4:.1f} bps of NAV per changed pick (UPPER bound); "
        f"ties FIRST-WINS in ascending rung order")
    gate("G7 ladders strictly nested L3 c L7 c L16",
         f"{set(L3) <= set(L7)} / {set(L7) <= set(L16)}", "True / True",
         set(L3) <= set(L7) and set(L7) <= set(L16))

    rows, r8rows, bookrows, pickrows = [], [], [], []
    u56_check = None

    for pi, panel in enumerate(["U56", "B136", "SMALL"]):
        if panel == "SMALL":
            px = load_universe(small=True)
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
            drop = [c for c in px.columns if c in bad]
            px = px.drop(columns=drop)
            say(f"\n## SMALL panel: {len(drop)} tickers dropped for max_1d_move >= 1.0")
        else:
            px = load_universe(broad=(panel == "B136"))
        px = px.dropna(how="all").ffill()
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        i_oos_abs = int(idx.searchsorted(OOS_START))
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].fillna(0.0).values
        pname = panel if panel != "B136" else f"B{K-1}"
        if panel == "SMALL":
            pname = f"SMALL{K-1}"
        say(f"\n## {pname}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}  "
            f"{len(reb)} rebalance dates  OOS row {i_oos_abs}")

        # ---- the 16 rung books
        R = np.zeros((len(HS), T))
        for j, H in enumerate(HS):
            Wm = build(rank_key, elig, priced, reb, NSLOT, H, T, K, GROSS)
            g, tn = nrun(rets, lagmat(Wm), mkl)
            R[j] = g - tn * COST / 1e4
            w = windows_of(R[j][WARMUP:], i_oos_abs - WARMUP)
            ann_turn = float(tn[WARMUP:].sum() * 252.0 / (T - WARMUP))
            bookrows.append(dict(panel=pname, N=NSLOT, H=H, ann_turnover=ann_turn, **flat(w)))
            if pi == 0 and H == 126:
                eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                               cost_bps=COST, freq=FREQ)["returns"].values
                d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - R[j][WARMUP:])))
                gate("G1 fast runner == engine.backtest (U56, N=20, H=126)", f"{d1:.3e}",
                     "< 1e-12", d1 < 1e-12)
                trip = (w["full"]["CAGR"], w["full"]["Sharpe"], w["full"]["MaxDD"])
                say(f"   U56 N=20 H=126 on the LIVE tape (ungated): {trip[0]:.6f}/{trip[1]:.6f}/{trip[2]:.6f}")
                itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
                wt = windows_of(R[j][WARMUP:itr], i_oos_abs - WARMUP)
                tript = (wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])
                d2 = max(abs(tript[i] - A936_WH126[i]) for i in range(3))
                gate(f"G2 CROSS-RUN U56 N=20 H=126 triple == 936/1082/1174's committed "
                     f"(tape truncated to {COMMIT_TAPE_END})",
                     f"{tript[0]:.6f}/{tript[1]:.6f}/{tript[2]:.6f}  maxdiff {d2:.2e}",
                     f"{A936_WH126} < 5e-4", d2 < 5e-4)
        say("   rung books (post-warm-up):")
        for j, H in enumerate(HS):
            w = windows_of(R[j][WARMUP:], i_oos_abs - WARMUP)
            say(f"     H={H:4d}  full {w['full']['CAGR']:7.2%} / {w['full']['Sharpe']:.4f} / "
                f"{w['full']['MaxDD']:7.2%}   IS Sh {w['is_']['Sharpe']:.4f}   OOS Sh {w['oos']['Sharpe']:.4f}")

        sw = windows_of(spy_r[WARMUP:], i_oos_abs - WARMUP)
        lw = windows_of(live_r[WARMUP:], i_oos_abs - WARMUP)
        say(f"   SPY      full {sw['full']['CAGR']:7.2%} / {sw['full']['Sharpe']:.4f} / "
            f"{sw['full']['MaxDD']:7.2%}   OOS {sw['oos']['CAGR']:7.2%} / {sw['oos']['Sharpe']:.4f} / {sw['oos']['MaxDD']:7.2%}")
        say(f"   RULESv2  full {lw['full']['CAGR']:7.2%} / {lw['full']['Sharpe']:.4f} / "
            f"{lw['full']['MaxDD']:7.2%}   OOS {lw['oos']['CAGR']:7.2%} / {lw['oos']['Sharpe']:.4f} / {lw['oos']['MaxDD']:7.2%}")
        if pi == 0:
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            swt = windows_of(spy_r[WARMUP:itr], i_oos_abs - WARMUP)
            d3 = max(abs(swt["oos"]["CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(swt["oos"]["Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(swt["oos"]["MaxDD"] - SPY_OOS_COMMITTED[2]))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape truncated to {COMMIT_TAPE_END}; live tape "
                 f"reads {sw['oos']['CAGR']:.4f}/{sw['oos']['Sharpe']:.4f}/{sw['oos']['MaxDD']:.4f})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            d4 = abs(lw["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gate("G4 live RULES v2 MaxDD == committed -12.05%", f"{lw['full']['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4", d4 < 5e-4)

        rs = RollSharpe(R)
        if pi == 0:
            d = WARMUP + 1008
            direct = np.array([sharpe(R[j][d - 1008:d]) for j in range(len(HS))])
            viacs = rs.at(d, 1008)
            e = float(np.nanmax(np.abs(direct - viacs)))
            gate("G5 cumsum window Sharpe == direct", f"{e:.3e}", "< 1e-10", e < 1e-10)

        say("\n   arm         WIN STEP |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe | IS Sh   | OOS Sh  | sw ties | 4a 4b | fail4b")
        cells = {}
        for arm in ARMS:
            for W in WINDOWS:
                for S in STEPS:
                    out = realise(R, rs, arm, W, S, WARMUP)
                    if out is None:
                        continue
                    d0, rc, ru, picks, nsw, tie = out
                    i_oos = max(int(np.searchsorted(idx.values[d0:], OOS_START.to_datetime64())), 1)
                    wc, wu = windows_of(rc, i_oos), windows_of(ru, i_oos)
                    spy = windows_of(spy_r[d0:], i_oos)
                    live = windows_of(live_r[d0:], i_oos)
                    a4, b4 = legs_4a(wc, live), legs_4b(wc, spy)
                    rec = dict(panel=pname, arm=arm, window=W, step=S, start=str(idx[d0].date()),
                               n_dec=len(picks), n_switch=nsw, tie_rate=tie, **flat(wc),
                               unch_full_Sharpe=wu["full"]["Sharpe"], unch_oos_Sharpe=wu["oos"]["Sharpe"],
                               spy_full_Sharpe=spy["full"]["Sharpe"], spy_oos_Sharpe=spy["oos"]["Sharpe"],
                               spy_full_MaxDD=spy["full"]["MaxDD"], spy_full_CAGR=spy["full"]["CAGR"],
                               live_full_Sharpe=live["full"]["Sharpe"], live_oos_Sharpe=live["oos"]["Sharpe"],
                               live_full_MaxDD=live["full"]["MaxDD"],
                               mean_pick_H=float(np.mean([HS[j] for j in picks])),
                               share_outside_L3=float(np.mean([HS[j] not in L3 for j in picks])),
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(arm, W, S)] = rec
                    for j in picks:
                        pickrows.append(dict(panel=pname, arm=arm, window=W, step=S, H=HS[j]))
                    say(f"   {arm:11s} {W:4d} {S:4d} | {wc['full']['CAGR']:7.2%} "
                        f"{wc['full']['Sharpe']:8.4f} {wc['full']['MaxDD']:8.2%} | "
                        f"{wc['h1']['Sharpe']:.4f}/{wc['h2']['Sharpe']:.4f} | {wc['is_']['Sharpe']:7.4f} | "
                        f"{wc['oos']['Sharpe']:7.4f} | {nsw:2d} {tie:4.2f} | "
                        f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | {failed(b4)}")

        # ---- G6: DO_NOTHING == the plain H=63 book on the same rows
        k = ("DO_NOTHING", WINDOWS[0], STEPS[0])
        if pi == 0 and k in cells:
            d0 = WARMUP + WINDOWS[0]
            e = abs(cells[k]["unch_full_Sharpe"] - sharpe(R[HIDX[DO_NOTHING_H]][d0:]))
            gate("G6 DO_NOTHING realised == plain H=63 book on the same rows", f"{e:.3e}",
                 "< 1e-12", e < 1e-12)

        # ---- the head-to-head 1183 asks about
        for scope in ["full_Sharpe", "oos_Sharpe", "is__Sharpe"]:
            for a, b in [("L3", "L16"), ("L3", "L7"), ("L7", "L16")]:
                dz = [cells[(a, W, S)][scope] - cells[(b, W, S)][scope]
                      for W in WINDOWS for S in STEPS if (a, W, S) in cells]
                say(f"   HEAD-TO-HEAD {scope:12s} {a} - {b} over {len(dz)} cells: "
                    f"mean {np.mean(dz):+.4f}  median {np.median(dz):+.4f}  "
                    f"min {np.min(dz):+.4f}  max {np.max(dz):+.4f}  "
                    f"{a} ahead at {int(np.sum(np.array(dz) > 0))} of {len(dz)}")
        for arm in ["L3", "L7", "L16"]:
            dz = [cells[(arm, W, S)]["oos_Sharpe"] - cells[("DO_NOTHING", W, S)]["oos_Sharpe"]
                  for W in WINDOWS for S in STEPS if (arm, W, S) in cells]
            say(f"   vs DO_NOTHING  oos_Sharpe  {arm:4s}: mean {np.mean(dz):+.4f}  "
                f"ahead at {int(np.sum(np.array(dz) > 0))} of {len(dz)}")

        # ---- rule 8
        for arm in ARMS:
            ks = [(W, S) for W in WINDOWS for S in STEPS if (arm, W, S) in cells]
            is_s = np.array([cells[(arm, W, S)]["is__Sharpe"] for W, S in ks])
            oos_s = np.array([cells[(arm, W, S)]["oos_Sharpe"] for W, S in ks])
            pick = ks[int(np.nanargmax(is_s))]
            dn = cells[("DO_NOTHING", pick[0], pick[1])]
            c = cells[(arm, *pick)]
            r8 = dict(panel=pname, arm=arm, pick_window=pick[0], pick_step=pick[1],
                      pick_IS=c["is__Sharpe"], pick_OOS=c["oos_Sharpe"],
                      donothing_OOS=dn["oos_Sharpe"], delta=c["oos_Sharpe"] - dn["oos_Sharpe"],
                      pick_OOS_CAGR=c["oos_CAGR"], pick_OOS_MaxDD=c["oos_MaxDD"],
                      donothing_OOS_CAGR=dn["oos_CAGR"], donothing_OOS_MaxDD=dn["oos_MaxDD"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      spy_OOS=c["spy_oos_Sharpe"], live_OOS=c["live_oos_Sharpe"],
                      pick_keep4a=c["keep4a"], pick_keep4b=c["keep4b"], pick_fail4b=c["fail4b"])
            r8rows.append(r8)
            say(f"   RULE 8  {arm:11s} IS-argmax = WINDOW {pick[0]} / STEP {pick[1]} "
                f"(IS Sh {r8['pick_IS']:.4f}) -> OOS {r8['pick_OOS']:.4f}  vs do-nothing "
                f"{r8['donothing_OOS']:.4f}  delta {r8['delta']:+.4f}   cellmean {r8['cellmean_OOS']:.4f}"
                f"  worst {r8['worst_OOS']:.4f}  rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

        if pi == 0:
            u56_check = (R, rs, {k: v["full_Sharpe"] for k, v in cells.items()})
        say(f"   [t={time.time()-t0:.0f}s]")

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(bookrows).to_csv(f"{STEM}.books.csv", index=False)
    pd.DataFrame(pickrows).to_csv(f"{STEM}.picks.csv", index=False)

    # ---- G8 determinism
    R, rs, ref = u56_check
    worst = 0.0
    for (arm, W, S), v in ref.items():
        out = realise(R, rs, arm, W, S, WARMUP)
        worst = max(worst, abs(sharpe(out[1]) - v))
    gate("G8 determinism (U56 grid re-run)", f"{worst:.3e}", "== 0.0", worst == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- summary
    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for arm in ARMS:
            g = grid[(grid.panel == pname) & (grid.arm == arm)]
            if not len(g):
                continue
            say(f"   {pname:10s} {arm:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}  "
                f"mean full Sh {g.full_Sharpe.mean():.4f}  mean OOS Sh {g.oos_Sharpe.mean():.4f}  "
                f"mean CAGR {g.full_CAGR.mean():7.2%}  mean MaxDD {g.full_MaxDD.mean():7.2%}  "
                f"mean switches {g.n_switch.mean():5.1f}  outside-L3 {g.share_outside_L3.mean():.3f}")
    for scope in ["full_Sharpe", "oos_Sharpe"]:
        d = []
        for pname in grid.panel.unique():
            g = grid[grid.panel == pname]
            for W in WINDOWS:
                for S in STEPS:
                    a = g[(g.arm == "L3") & (g.window == W) & (g.step == S)]
                    b = g[(g.arm == "L16") & (g.window == W) & (g.step == S)]
                    if len(a) and len(b):
                        d.append(float(a.iloc[0][scope] - b.iloc[0][scope]))
        say(f"   POOLED L3 - L16 {scope:12s}: mean {np.mean(d):+.4f}  median {np.median(d):+.4f}  "
            f"sd {np.std(d, ddof=1):.4f}  t {np.mean(d)/(np.std(d, ddof=1)/np.sqrt(len(d))):+.2f}  "
            f"L3 ahead at {int(np.sum(np.array(d) > 0))} of {len(d)}   (1174 committed +0.0559 OOS)")
    wf = pd.DataFrame(r8rows)
    for arm in ["L3", "L7", "L16"]:
        g = wf[wf.arm == arm]
        say(f"   RULE 8 POOLED {arm:4s}: mean delta vs do-nothing {g.delta.mean():+.4f}  "
            f"positive at {int((g.delta > 0).sum())} of {len(g)}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"   [total {time.time()-t0:.0f}s]")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
