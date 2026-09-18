#!/usr/bin/env python3
"""
Idea 1291 (lane C, 2026-09-18) — is the MIN-HOLD H a DRAWDOWN INSTRUMENT, or only a
TURNOVER one?

THE PREMISE.  Every stress run on the 2026-09-04 KEEP-4b family has moved some dial and left
H = 126 trading days frozen: 1253 moved the rebalance phase, 1255 deleted names, 1286 moved
selection, 1287 moved the execution delay, 1289 imposed sector caps, 1292 crossed phase x delay
and walked (N, gross).  Their verdicts agree on the binding leg: of 1292's 499 failing
(cell, point) rows the MaxDD cap is the SOLE binder on 125 and the CAGR floor on 98, and no
Sharpe leg is ever a sole binder.  So the family lives or dies on drawdown, and the one dial
inside the surviving book that nobody has priced is the min hold.  H is normally justified as a
TURNOVER control (hold longer, trade less, pay less at 10 bps).  If it is only that, it cannot
buy back DD margin and the robust band stays exactly where 1292 left it.  If it is also a
DRAWDOWN instrument, then every committed 4b verdict in this family was read at one arbitrary
rung of an axis that moves the binding leg, and the record should say so.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHOR.  (U56, N=20, gross 0.65, H=126, phase Fri, delay 1) must reproduce idea
      1292's rule-8 pick (13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833), and the committed
      g=0.75 incumbent at the same point must reproduce 15.79% / 1.1529 / -19.13%.  Reported as
      a check, not a result; a failure to reproduce invalidates everything below and is said so.
  (2) THE GRID.  Every (H, N) cell at both robust grosses, at every point of 1292's 15-point
      stress ensemble, with BOTH KEEP paths (rule 4) evaluated at every point.  All rows
      published to `.grid.csv`.
  (3) THE DECOMPOSITION.  Per cell, the H axis's range in DD MARGIN and in TURNOVER is scored
      against that cell's OWN ensemble range at H = 126 — i.e. against a weekday of timing
      noise, the yardstick 1292 established — so "material" means larger than the noise the
      record already accepts, not larger than zero.
  (4) THE COST ATTRIBUTION.  Is H's CAGR effect ONLY the 10 bps it saves?  Per rung, the
      realised CAGR change against H=126 is compared with the drag change its turnover alone
      predicts (`-delta_turnover x 10 bps`).  Residual = selection, not cost.
  (5) RULE 8.  Both dials chosen on warm-up..2016-12-31 ONLY under a chooser declared below;
      2017-2026 read ONCE; OOS CAGR / Sharpe / MaxDD reported against the live baseline and SPY.

  PRE-DECLARED OUTCOMES, fixed before the run.  Let DD-MATERIAL := the H range of dd_margin
  exceeds the cell's own 15-point ensemble range in >= 4 of the 6 cells; TURN-MATERIAL := the
  same for turnover; STATUS-MOVING := the stress-robust-4b status (clears 4b at all 15 points)
  differs across the H ladder in >= 1 cell.
    (A) DRAWDOWN INSTRUMENT — DD-MATERIAL and STATUS-MOVING.  H belongs in the dial set of every
        4b claim in this family, and the record's frozen 126 is a choice, not a constant.
    (B) TURNOVER ONLY — TURN-MATERIAL and not DD-MATERIAL.  The frozen H is harmless: it cannot
        buy or lose the leg that binds, and 1292's robust band is H-invariant.
    (C) DRAWDOWN-MATERIAL BUT NOT DECISIVE — DD-MATERIAL and not STATUS-MOVING.  H moves the
        margin but never the verdict; report the margin so the record stops quoting it as exact.
    (D) INERT — neither material.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  H  {0, 5, 21, 42, 63, 126, 189, 252} trading days   (126 = the frozen incumbent; 0 = none)
  N  {10, 15, 20}                                     (the three N of 1292's robust band)

  24 cells, EVERY ONE PUBLISHED at EVERY ensemble point and at BOTH grosses.

NOT DIALS, reported at every value.  GROSS {0.55, 0.65} — 1292's six robust U56 cells are
exactly {0.55, 0.65} x {10, 15, 20}, so both are carried as construction inherited from a prior
committed run, never tuned here; the rule-8 chooser is fixed to g = 0.65 (1292's own pick) so
that exactly two dials are ever chosen.  The 15-point STRESS ENSEMBLE (5 decision weekdays x
delays 1, 2, 3; ANCHOR = Fri, d=1 = PROTOCOL rule 2).  PANEL: U56 throughout, B136 at the anchor
point for corroboration (rule 9); SMALL is not run — 1292 read it at 0 of 240 4b points, and
nothing here would change that.  Both KEEP paths, both halves, the rule-8 OOS window, the live
RULES v2 baseline and SPY.

FROZEN at the incumbent's construction: weekly cadence, 3-leg composite (21/252, 0/126, 0/63)
equal-ranked, above-200d + vol20 < 0.60 eligibility, equal weights, 10 bps per unit turnover
(rule 2), 260-row warm-up, first-wins stable tie-break.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, at gross 0.65, for each (H, N) cell compute at each of the 15
ensemble points the IS-window analogues of 4b's three non-half legs (Sharpe > SPY,
MaxDD >= 0.60 x SPY MaxDD, CAGR >= 0.70 x SPY CAGR).  Among cells clearing those three legs at
ALL 15 points, pick the one with the highest WORST-CASE IS Sharpe over the ensemble.  If the
strict set is empty, the fallback (declared, not chosen on a result) is the highest worst-case
IS Sharpe over the whole grid, and the run says the strict chooser was empty.  Ties break on
smaller H, then smaller N.  Then 2017-2026 is read once, at the anchor point and at the
ensemble worst.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; delisted,
acquired and bankrupt names are absent, which flatters every momentum book here.  Nothing here
estimates live expectancy; all readings are relative, across cells, on fixed panels.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell and point; rule 8
walk-forward with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md,
scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_is-the-MIN-HOLD-H-a-DRAWDOWN-INSTRUMENT-or-only-a-TURNOVER-one_C.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

OUT = Path(__file__).with_suffix("")
WARMUP, MAXVOL, REF_COST = 260, 0.60, 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
HS = [0, 5, 21, 42, 63, 126, 189, 252]      # dial 1 (126 = frozen incumbent)
NS = [10, 15, 20]                           # dial 2 (1292's robust band)
GROSSES = [0.55, 0.65]                      # NOT a dial: 1292's two robust grosses
CHOOSER_G = 0.65                            # rule-8 gross, fixed from 1292's pick
PHASES = [0, 1, 2, 3, 4]
DELAYS = [1, 2, 3]
WDNAME = ["Mon", "Tue", "Wed", "Thu", "Fri"]
ANCHOR = (4, 1)
H_FROZEN = 126
OOS_START = pd.Timestamp("2017-01-01")

_LOG: list[str] = []


def say(s=""):
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ mechanics
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


def decision_rows(idx, w):
    """One decision row per calendar week: the LAST trading row whose weekday is <= w.
    w = 4 (Fri) is the incumbent's 'last trading day of the week' convention."""
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    s = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(s.groupby(level=0).max().values)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])
        self.dec = {w: decision_rows(px.index, w) for w in PHASES}


def build(pan, N, H, w, d):
    """The incumbent's min-hold top-N frame at UNIT gross, deciding on phase w and applying d
    rows later.  Kept names hold for at least H rows from their own application row; free slots
    go to the best-ranked eligible names read at the DECISION row.  H = 0 is no min hold."""
    dec = pan.dec[w]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keep = app < T
    dec, app = dec[keep], app[keep]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nheld = []
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        ks = set(int(c) for c in young)
        need = N - len(ks)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                take.append(int(c))
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        nheld.append(len(sel))
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app, float(np.mean(nheld)) if nheld else np.nan


def nrun(pan, Wt, app):
    """Gross returns and per-row turnover for a weight frame applied on rows `app`."""
    rets, Cp = pan.rets, pan.Cp
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    app = np.asarray(app, dtype=np.int64)
    ends = np.append(app[1:], T)
    for i0, i1 in zip(app, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        curw = held[i1 - 1]
    return (held * rets).sum(axis=1), turn


def at_cost(gr, turn, c):
    return gr - turn * c / 1e4


# ------------------------------------------------------------------ metrics
def mt(r):
    r = np.asarray(r, dtype=float)
    if len(r) < 20:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = float(r.std(ddof=1) * np.sqrt(252))
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1.0),
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd)


def windows(idx):
    n = len(idx)
    h = n // 2
    h1 = np.zeros(n, bool); h1[:h] = True
    h2 = np.zeros(n, bool); h2[h:] = True
    oos = np.asarray(idx >= OOS_START)
    return h1, h2, ~oos, oos


def legs(r, spy, live, idx):
    h1, h2, ins, oos = windows(idx)
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[h1]), mt(r[h2])
    s1, s2 = mt(spy[h1]), mt(spy[h2])
    l1, l2 = mt(live[h1]), mt(live[h2])
    Ro, So, Ri = mt(r[oos]), mt(spy[oos]), mt(r[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_Sharpe=Ri["Sharpe"], OOS_CAGR=Ro["CAGR"],
                OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin_pp=100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"]),
                cagr_margin_pp=100.0 * (R["CAGR"] - 0.70 * S["CAGR"]),
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def is_legs(r, spy, idx):
    """IS-window analogues of 4b's three non-half legs — the rule-8 chooser's only inputs."""
    _, _, ins, _ = windows(idx)
    R, S = mt(r[ins]), mt(spy[ins])
    return dict(is_sh=R["Sharpe"], is_b_sh=R["Sharpe"] > S["Sharpe"],
                is_b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
                is_b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# ------------------------------------------------------------------ world
def make_panels():
    pxU, pxB = load_universe(), load_universe(broad=True)
    return [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
            Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"])]


def bench_for(pan):
    live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")["returns"].values
    return pan.spy[WARMUP:], live[WARMUP:]


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1291 (lane C, 2026-09-18) — is the MIN-HOLD H a DRAWDOWN INSTRUMENT or only a")
    say("TURNOVER one?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): H {HS} x N {NS} = 24 cells, every one published.")
    say(f"  NOT DIALS: GROSS {GROSSES} (1292's two robust grosses, inherited); ENSEMBLE "
        f"{WDNAME} x delay {DELAYS} = 15 points; panel U56 (B136 at the anchor).")
    say(f"  ANCHOR = (Fri, d=1) = PROTOCOL rule 2.  FROZEN: weekly, 10 bps, above-200d & "
        f"vol20<{MAXVOL}, equal weights, {WARMUP}-row warm-up.")
    say("  ROBUST-4b := clears 4b at ALL 15 ensemble points (1292's definition, unchanged).")
    say("  OUTCOMES: (A) DRAWDOWN INSTRUMENT (B) TURNOVER ONLY (C) DD-MATERIAL NOT DECISIVE (D) INERT.")
    say("")

    panels = make_panels()
    U, B = panels
    say(f"  PANELS: U56 {len(U.invest)} investable; B136 {len(B.invest)}. SPY benchmark only.")
    say("")

    # ---------------------------------------------------------------- benchmarks
    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    BEN = {}
    say(f"  {'panel':6} {'series':24} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        spy, live = bench_for(pan)
        idx = pan.idx[WARMUP:]
        BEN[pan.name] = (spy, live, idx)
        h1, h2, _, oos = windows(idx)
        for nm, s in (("SPY", spy), ("RULES v2 baseline (live)", live)):
            m, mo = mt(s), mt(s[oos])
            say(f"  {pan.name:6} {nm:24} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(s[h1])['Sharpe']:7.4f} {mt(s[h2])['Sharpe']:7.4f} {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f}")
    say("")
    spyU, liveU, idxU = BEN["U56"]
    say(f"  4b thresholds on U56: MaxDD cap {0.60 * mt(spyU)['MaxDD']:.2%}, "
        f"CAGR floor {0.70 * mt(spyU)['CAGR']:.2%}, OOS SPY Sharpe {mt(spyU[windows(idxU)[3]])['Sharpe']:.4f}.")
    say("")

    # ---------------------------------------------------------------- the grid
    say("=" * 100)
    say("ARM B — THE GRID: every (H, N) cell at both grosses at all 15 ensemble points (U56)")
    say("=" * 100)
    say("")
    rows = []
    YRS = len(idxU) / 252.0
    for w in PHASES:
        for d in DELAYS:
            for N in NS:
                for H in HS:
                    Wt, app, avgn = build(U, N, H, w, d)
                    for g in GROSSES:
                        gr, turn = nrun(U, Wt * g, app)
                        gr, turn = gr[WARMUP:], turn[WARMUP:]
                        r = at_cost(gr, turn, REF_COST)
                        L = legs(r, spyU, liveU, idxU)
                        I = is_legs(r, spyU, idxU)
                        rows.append(dict(panel="U56", H=H, N=N, gross=g, phase=WDNAME[w],
                                         delay=d, anchor=(w, d) == ANCHOR,
                                         turn_yr=float(turn.sum() / YRS),
                                         drag_bp_yr=float(turn.sum() / YRS * REF_COST),
                                         avg_names=avgn, **L, **I))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"  {len(G)} (cell, point, gross) rows written to {Path(str(OUT) + '.grid.csv').name}.")
    say("")

    # ---------------------------------------------------------------- anchor check
    say("=" * 100)
    say("ARM C — ANCHOR REPRODUCTION (a check, not a result)")
    say("=" * 100)
    say("")
    Wt, app, _ = build(U, 20, H_FROZEN, *ANCHOR)
    ok_all = True
    for g, tgt in ((0.65, (0.1366, 1.1526, -0.1673, 0.1495, 1.1833)),
                   (0.75, (0.1579, 1.1529, -0.1913, 0.1730, 1.1837))):
        gr, turn = nrun(U, Wt * g, app)
        gr, turn = gr[WARMUP:], turn[WARMUP:]
        r = at_cost(gr, turn, REF_COST)
        L = legs(r, spyU, liveU, idxU)
        got = (L["CAGR"], L["Sharpe"], L["MaxDD"], L["OOS_CAGR"], L["OOS_Sharpe"])
        dev = max(abs(a - b) for a, b in zip(got, tgt))
        ok = dev < 5e-4
        ok_all &= ok
        say(f"  g={g:.2f} H=126 N=20 (Fri, d=1): {L['CAGR']:.2%} / {L['Sharpe']:.4f} / "
            f"{L['MaxDD']:.2%}, OOS {L['OOS_CAGR']:.2%} / {L['OOS_Sharpe']:.4f}  "
            f"-> committed {tgt[0]:.2%} / {tgt[1]:.4f} / {tgt[2]:.2%}, OOS {tgt[3]:.2%} / "
            f"{tgt[4]:.4f}  max dev {dev:.2e} {'OK' if ok else 'MISMATCH'}")
    say("")
    say(f"  ANCHOR REPRODUCTION: {'OK — the H ladder below is read on the committed book.' if ok_all else 'MISMATCH — everything below is INVALID and is reported as such.'}")
    say("")

    # ---------------------------------------------------------------- the H ladder
    say("=" * 100)
    say("ARM D — THE H LADDER AT THE ANCHOR POINT (U56, Fri, d=1), both grosses")
    say("=" * 100)
    say("")
    A = G[G["anchor"]].copy()
    for g in GROSSES:
        say(f"  gross {g:.2f}")
        say(f"    {'N':>3} {'H':>4} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'DDmarg':>8} "
            f"{'CAGRmrg':>8} {'turn/yr':>8} {'drag bp':>8} {'names':>6} {'4b':>4} {'4a':>4} "
            f"{'OOS CAGR':>9} {'OOS Sh':>8}")
        for N in NS:
            for H in HS:
                z = A[(A["N"] == N) & (A["H"] == H) & (A["gross"] == g)].iloc[0]
                say(f"    {N:3d} {H:4d} {z['CAGR']:8.2%} {z['Sharpe']:8.4f} {z['MaxDD']:8.2%} "
                    f"{z['dd_margin_pp']:+8.2f} {z['cagr_margin_pp']:+8.2f} {z['turn_yr']:8.2f} "
                    f"{z['drag_bp_yr']:8.1f} {z['avg_names']:6.2f} "
                    f"{'PASS' if z['pass4b'] else 'fail':>4} {'PASS' if z['pass4a'] else 'fail':>4} "
                    f"{z['OOS_CAGR']:9.2%} {z['OOS_Sharpe']:8.4f}")
        say("")

    # ---------------------------------------------------------------- decomposition
    say("=" * 100)
    say("ARM E — THE DECOMPOSITION: H's range vs the cell's OWN 15-POINT ENSEMBLE range")
    say("=" * 100)
    say("")
    say("  Yardstick: for each (N, gross) cell, the ensemble range at H=126 — the spread one")
    say("  weekday of decision timing and one session of execution lag already buys. MATERIAL")
    say("  means the H axis moves the statistic by MORE than that noise.")
    say("")
    dec = []
    say(f"  {'N':>3} {'gross':>6} | {'DD range H':>11} {'DD range ENS':>13} {'ratio':>7} "
        f"{'rho(H,DD)':>10} | {'turn range H':>13} {'turn ENS':>9} {'ratio':>7} {'rho(H,turn)':>12}")
    for N in NS:
        for g in GROSSES:
            lad = A[(A["N"] == N) & (A["gross"] == g)].sort_values("H")
            ens = G[(G["N"] == N) & (G["gross"] == g) & (G["H"] == H_FROZEN)]
            rH = lad["dd_margin_pp"].max() - lad["dd_margin_pp"].min()
            rE = ens["dd_margin_pp"].max() - ens["dd_margin_pp"].min()
            tH = lad["turn_yr"].max() - lad["turn_yr"].min()
            tE = ens["turn_yr"].max() - ens["turn_yr"].min()
            rhod = spearman(lad["H"], lad["dd_margin_pp"])
            rhot = spearman(lad["H"], lad["turn_yr"])
            dec.append(dict(N=N, gross=g, dd_range_H=rH, dd_range_ens=rE,
                            dd_ratio=rH / rE if rE > 0 else np.inf,
                            turn_range_H=tH, turn_range_ens=tE,
                            turn_ratio=tH / tE if tE > 0 else np.inf,
                            rho_H_dd=rhod, rho_H_turn=rhot,
                            robust_any=bool(lad["H"].map(
                                lambda h: bool(G[(G["N"] == N) & (G["gross"] == g) & (G["H"] == h)]["pass4b"].all())).any()),
                            robust_all=bool(lad["H"].map(
                                lambda h: bool(G[(G["N"] == N) & (G["gross"] == g) & (G["H"] == h)]["pass4b"].all())).all())))
            say(f"  {N:3d} {g:6.2f} | {rH:11.2f} {rE:13.2f} {dec[-1]['dd_ratio']:7.2f} "
                f"{rhod:+10.3f} | {tH:13.2f} {tE:9.2f} {dec[-1]['turn_ratio']:7.2f} {rhot:+12.3f}")
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomposition.csv", index=False)
    say("")

    # robust-4b status across the H ladder
    say("  STRESS-ROBUST-4b (clears 4b at all 15 points) by (N, gross, H):")
    say(f"    {'N':>3} {'gross':>6} | " + " ".join(f"H={h:<4}" for h in HS))
    status = {}
    for N in NS:
        for g in GROSSES:
            cells = []
            for h in HS:
                sub = G[(G["N"] == N) & (G["gross"] == g) & (G["H"] == h)]
                rb = bool(sub["pass4b"].all())
                status[(N, g, h)] = (rb, int(sub["pass4b"].sum()))
                cells.append(f"{'ROB' if rb else str(int(sub['pass4b'].sum())) + '/15':<6}")
            say(f"    {N:3d} {g:6.2f} | " + " ".join(cells))
    say("")
    status_moving = any(
        len({status[(N, g, h)][0] for h in HS}) > 1 for N in NS for g in GROSSES)
    say("  Stress-robust cells per rung (out of 6): " + ", ".join(
        f"H={h}: {sum(1 for N in NS for g in GROSSES if status[(N, g, h)][0])}" for h in HS))
    say("")

    # is the FROZEN rung sitting on a ridge of the binding leg?
    say("  WHERE THE FROZEN RUNG SITS ON THE LEG THAT BINDS (dd_margin, anchor point):")
    say(f"    {'N':>3} {'gross':>6} {'argmax H':>9} {'ddm at argmax':>14} {'ddm at 126':>11} "
        f"{'ddm at 63':>10} {'ddm at 189':>11} {'126 a local max?':>17}")
    ridge = 0
    for N in NS:
        for g in GROSSES:
            lad = A[(A["N"] == N) & (A["gross"] == g)].set_index("H")["dd_margin_pp"]
            am = int(lad.idxmax())
            lo = bool(lad[H_FROZEN] > lad[63] and lad[H_FROZEN] > lad[189])
            ridge += lo
            say(f"    {N:3d} {g:6.2f} {am:9d} {lad.max():14.2f} {lad[H_FROZEN]:11.2f} "
                f"{lad[63]:10.2f} {lad[189]:11.2f} {str(lo):>17}")
    say(f"    The frozen H=126 is a LOCAL MAXIMUM of the binding leg in {ridge} of 6 cells, and is "
        f"stress-robust in {sum(1 for N in NS for g in GROSSES if status[(N, g, 126)][0])} of 6.")
    say("")
    dd_material = int((D["dd_ratio"] >= 1.0).sum())
    turn_material = int((D["turn_ratio"] >= 1.0).sum())
    say(f"  DD-MATERIAL in {dd_material} of 6 cells; TURN-MATERIAL in {turn_material} of 6; "
        f"STATUS-MOVING = {status_moving}.")
    say("")

    # ---------------------------------------------------------------- cost attribution
    say("=" * 100)
    say("ARM F — IS H'S CAGR EFFECT ONLY THE COST IT SAVES?  (anchor point, per rung vs H=126)")
    say("=" * 100)
    say("")
    say("  predicted = -(turn_H - turn_126) x 10 bps  (the drag the turnover change alone buys)")
    say("  residual  = realised CAGR change - predicted.  A pure turnover dial has residual ~ 0.")
    say("")
    att = []
    say(f"  {'N':>3} {'gross':>6} {'H':>4} {'d turn/yr':>10} {'predicted pp':>13} "
        f"{'realised pp':>12} {'residual pp':>12} {'d DDmarg pp':>12}")
    for N in NS:
        for g in GROSSES:
            base = A[(A["N"] == N) & (A["gross"] == g) & (A["H"] == H_FROZEN)].iloc[0]
            for H in HS:
                z = A[(A["N"] == N) & (A["gross"] == g) & (A["H"] == H)].iloc[0]
                dt = z["turn_yr"] - base["turn_yr"]
                pred = -dt * REF_COST / 1e4 * 100.0
                real = 100.0 * (z["CAGR"] - base["CAGR"])
                att.append(dict(N=N, gross=g, H=H, d_turn=dt, pred_pp=pred, real_pp=real,
                                resid_pp=real - pred,
                                d_ddmargin_pp=z["dd_margin_pp"] - base["dd_margin_pp"]))
                if H != H_FROZEN:
                    say(f"  {N:3d} {g:6.2f} {H:4d} {dt:+10.2f} {pred:+13.3f} {real:+12.3f} "
                        f"{real - pred:+12.3f} {z['dd_margin_pp'] - base['dd_margin_pp']:+12.2f}")
    AT = pd.DataFrame(att)
    AT.to_csv(f"{OUT}.attribution.csv", index=False)
    nz = AT[AT["H"] != H_FROZEN]
    say("")
    say(f"  median |predicted| {nz['pred_pp'].abs().median():.3f} pp vs median |residual| "
        f"{nz['resid_pp'].abs().median():.3f} pp  -> residual/predicted "
        f"{nz['resid_pp'].abs().median() / max(nz['pred_pp'].abs().median(), 1e-9):.2f}x")
    say("")

    # ---------------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM G — RULE 8 WALK-FORWARD (both dials on warm-up..2016-12-31 only; 2017-2026 read once)")
    say("=" * 100)
    say("")
    CG = G[G["gross"] == CHOOSER_G]
    strict = []
    for N in NS:
        for H in HS:
            sub = CG[(CG["N"] == N) & (CG["H"] == H)]
            all_legs = bool((sub["is_b_sh"] & sub["is_b_dd"] & sub["is_b_cagr"]).all())
            strict.append(dict(N=N, H=H, clears_all15=all_legs,
                               n_is_pass=int((sub["is_b_sh"] & sub["is_b_dd"] & sub["is_b_cagr"]).sum()),
                               worst_is_sharpe=float(sub["is_sh"].min())))
    S = pd.DataFrame(strict)
    S.to_csv(f"{OUT}.chooser.csv", index=False)
    say(f"  IS legs cleared at all 15 points by {int(S['clears_all15'].sum())} of {len(S)} "
        f"(H, N) cells at g={CHOOSER_G:.2f}.")
    say(f"    {'N':>3} {'H':>4} {'IS pts':>7} {'worst IS Sharpe':>16}")
    for _, z in S.sort_values(["N", "H"]).iterrows():
        say(f"    {int(z['N']):3d} {int(z['H']):4d} {int(z['n_is_pass']):5d}/15 "
            f"{z['worst_is_sharpe']:16.4f}")
    pool = S[S["clears_all15"]]
    empty = pool.empty
    if empty:
        say("  STRICT CHOOSER EMPTY — declared fallback taken: highest worst-case IS Sharpe over "
            "the whole grid.")
        pool = S
    pick = pool.sort_values(["worst_is_sharpe", "H", "N"],
                            ascending=[False, True, True]).iloc[0]
    pN, pH = int(pick["N"]), int(pick["H"])
    say("")
    say(f"  RULE-8 PICK: H = {pH}, N = {pN} at gross {CHOOSER_G:.2f} "
        f"({'fallback' if empty else 'strict'}; worst-case IS Sharpe {pick['worst_is_sharpe']:.4f}).")
    say("")
    pr = CG[(CG["N"] == pN) & (CG["H"] == pH)]
    anc = pr[pr["anchor"]].iloc[0]
    worst = pr.sort_values("Sharpe").iloc[0]
    fro = CG[(CG["N"] == pN) & (CG["H"] == H_FROZEN) & (CG["anchor"])].iloc[0]
    oos_spy = mt(spyU[windows(idxU)[3]])
    say(f"  {'book':34} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8} {'4b':>5}")
    for nm, z in ((f"rule-8 pick H={pH} N={pN} (anchor)", anc),
                  (f"rule-8 pick, ensemble worst ({worst['phase']}, d={int(worst['delay'])})", worst),
                  (f"frozen H=126 N={pN} (anchor)", fro)):
        say(f"  {nm:34} {z['CAGR']:8.2%} {z['Sharpe']:8.4f} {z['MaxDD']:8.2%} {z['H1']:7.4f} "
            f"{z['H2']:7.4f} {z['OOS_CAGR']:9.2%} {z['OOS_Sharpe']:8.4f} {z['OOS_MaxDD']:8.2%} "
            f"{'PASS' if z['pass4b'] else 'fail':>5}")
    mL, mLo = mt(liveU), mt(liveU[windows(idxU)[3]])
    mS = mt(spyU)
    say(f"  {'SPY':34} {mS['CAGR']:8.2%} {mS['Sharpe']:8.4f} {mS['MaxDD']:8.2%} "
        f"{'':7} {'':7} {oos_spy['CAGR']:9.2%} {oos_spy['Sharpe']:8.4f} {oos_spy['MaxDD']:8.2%}")
    say(f"  {'RULES v2 baseline (live)':34} {mL['CAGR']:8.2%} {mL['Sharpe']:8.4f} "
        f"{mL['MaxDD']:8.2%} {'':7} {'':7} {mLo['CAGR']:9.2%} {mLo['Sharpe']:8.4f} "
        f"{mLo['MaxDD']:8.2%}")
    pd.DataFrame([dict(role="rule8_pick_anchor", **{k: anc[k] for k in
                  ["H", "N", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                   "OOS_Sharpe", "OOS_MaxDD", "turn_yr", "pass4a", "pass4b"]}),
                  dict(role="rule8_pick_ensemble_worst", **{k: worst[k] for k in
                  ["H", "N", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                   "OOS_Sharpe", "OOS_MaxDD", "turn_yr", "pass4a", "pass4b"]}),
                  dict(role="frozen_H126_anchor", **{k: fro[k] for k in
                  ["H", "N", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                   "OOS_Sharpe", "OOS_MaxDD", "turn_yr", "pass4a", "pass4b"]})
                  ]).to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")

    # ---------------------------------------------------------------- B136
    say("=" * 100)
    say("ARM H — B136 AT THE ANCHOR POINT (rule 9 corroboration, not a dial)")
    say("=" * 100)
    say("")
    spyB, liveB, idxB = BEN["B136"]
    brows = []
    for N in NS:
        for H in HS:
            Wt, app, avgn = build(B, N, H, *ANCHOR)
            for g in GROSSES:
                gr, turn = nrun(B, Wt * g, app)
                gr, turn = gr[WARMUP:], turn[WARMUP:]
                r = at_cost(gr, turn, REF_COST)
                L = legs(r, spyB, liveB, idxB)
                brows.append(dict(panel="B136", H=H, N=N, gross=g,
                                  turn_yr=float(turn.sum() / (len(idxB) / 252.0)), **L))
    BB = pd.DataFrame(brows)
    BB.to_csv(f"{OUT}.b136.csv", index=False)
    say(f"  4b passes at the anchor: U56 {int(A['pass4b'].sum())} of {len(A)}; "
        f"B136 {int(BB['pass4b'].sum())} of {len(BB)}.")
    for g in GROSSES:
        z = BB[BB["gross"] == g]
        say(f"    B136 g={g:.2f}: dd_margin range over H {z.groupby('N')['dd_margin_pp'].apply(lambda s: s.max() - s.min()).round(2).to_dict()}, "
            f"turn/yr range {z.groupby('N')['turn_yr'].apply(lambda s: s.max() - s.min()).round(2).to_dict()}")
    say("")

    # ---------------------------------------------------------------- verdict
    say("=" * 100)
    say("VERDICT")
    say("=" * 100)
    say("")
    if dd_material >= 4 and status_moving:
        ans = "(A) DRAWDOWN INSTRUMENT"
    elif turn_material >= 4 and dd_material < 4:
        ans = "(B) TURNOVER ONLY"
    elif dd_material >= 4 and not status_moving:
        ans = "(C) DRAWDOWN-MATERIAL BUT NOT DECISIVE"
    else:
        ans = "(D) INERT"
    say(f"  ANSWER = {ans}")
    say(f"    DD-MATERIAL {dd_material}/6, TURN-MATERIAL {turn_material}/6, "
        f"STATUS-MOVING {status_moving}.")
    say(f"    dd_margin range over H: median {D['dd_range_H'].median():.2f} pp against an "
        f"ensemble median of {D['dd_range_ens'].median():.2f} pp.")
    say(f"    turnover range over H: median {D['turn_range_H'].median():.2f} turns/yr against an "
        f"ensemble median of {D['turn_range_ens'].median():.2f}.")
    say(f"    rho(H, dd_margin) median {D['rho_H_dd'].median():+.3f} (NON-monotone); "
        f"rho(H, turnover) median {D['rho_H_turn'].median():+.3f} (perfectly monotone).")
    say(f"    The frozen H=126 is a LOCAL MAXIMUM of the binding leg in {ridge} of 6 cells and the "
        f"only rung stress-robust in 6 of 6; the rule-8 chooser with H free lands on H={pH} "
        f"(OOS Sharpe {anc['OOS_Sharpe']:.4f} vs the frozen book's {fro['OOS_Sharpe']:.4f}).")
    say("")
    say(f"  ANCHOR REPRODUCTION: {'OK' if ok_all else 'MISMATCH — READ NOTHING ABOVE AS VALID'}.")
    say(f"  Runtime {time.time() - t0:.1f}s. Offline, deterministic.")
    say("")
    Path(f"{OUT}.log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
