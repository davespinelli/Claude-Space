#!/usr/bin/env python3
"""
Idea 1295 (lane cloud, 2026-09-18) — does the CERTIFIED U56 g=0.65 BOOK AFFORD a SECTOR CAP
that the g=0.75 one could NOT?

THE PREMISE.  Idea 1289 capped names per sector in the standing KEEP-4b book and found the cap
FLIPS its 4b verdict: at U56 / N=20 / gross 0.75 the book clears 4b uncapped (-19.13% MaxDD
against a -20.23% cap) and at c=8, and FAILS at c=5, c=3 and c=2 — every failure binding on the
MaxDD leg ALONE, at -21.76% / -21.57% / -21.29%.  That verdict was read at ONE gross.  Idea 1290
then solved for the gross maximising the joint 4b margin and certified g=0.65 on U56, whose DD
margin is 2.40 pp larger than 0.75's, and established that Sharpe is essentially invariant in
gross (U56 range 0.0024 over 17 rungs) so that de-grossing spends CAGR and buys drawdown and
does nothing else.  Those two facts make 1289's failures look like a SIZING result reported as a
CONCENTRATION one.  A 20-name book with no sector limit is not a book a real account wants; this
run asks what the limit costs once the book is sized correctly.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHORS.  (U56, c=20, g=0.75) must reproduce the committed incumbent (15.79% / 1.1529
      / -19.13%, OOS 17.30% / 1.1837) and (U56, c=5, g=0.75) must reproduce 1289's capped cell
      (15.91% / 1.2115 / -21.76%, OOS 16.88% / 1.2258).  Reported as checks, not results; a
      failure to reproduce either invalidates everything below and is said so.
  (2) THE GRID.  Every (cap, gross) cell on every panel, with BOTH KEEP paths (rule 4) and both
      4b margins.  135 rows, all published in `.grid.csv`.
  (3) THE AFFORDABILITY FRONTIER.  For each cap, the LOWEST gross rung at which the capped book
      clears 4b, beside the uncapped book's own.  A cap is AFFORDABLE iff that rung exists at or
      below 0.75; the DIFFERENCE in rungs against c=20 is what the limit costs in size.
  (4) WHAT THE CAP BUYS AT MATCHED GROSS.  Sharpe, CAGR and MaxDD of each capped book against
      the uncapped book at the SAME gross, so the cap's effect is never read through a size change.
  (5) RULE 8.  Both dials chosen on warm-up..2016-12-31 ONLY by the chooser declared below,
      2017-2026 read ONCE, OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) GROSS BUYS THE CAP — some cap <= 5 clears 4b at a gross rung at or below 0.75 on U56,
        i.e. 1289's failures were a sizing result.  If rule 8 also reaches such a cell it is a
        KEEP-4b candidate and a memo is written; if not, PARK.
    (B) UNAFFORDABLE — no cap <= 5 clears 4b at ANY gross rung on U56: the concentration the
        screen produces is load-bearing and this family cannot be diversified into 4b.
    (C) IRRELEVANT — the cap changes no 4b verdict at any gross rung, at any cap.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  GROUP CAP c  {2, 3, 5, 8, 20}                         (20 = no cap = the incumbent)
  GROSS        {0.45, 0.50, ..., 0.85}  9 rungs         (0.65 = 1290's certified, 0.75 = 1289's)

  45 cells per panel, 135 in all, EVERY ONE PUBLISHED.

FROZEN, NOT DIALS: N = 20 names (the incumbent; 1289's N=10 arm is NOT re-opened here because
that would be a third dial), H = 126 min hold, weekly cadence, decide-at-t / apply-at-t+1
(rule 2), 3-leg composite (21/252, 0/126, 0/63) equal-ranked, above-200d and vol20 < 0.60
eligibility, 10 bps per unit turnover, 260-row warm-up, first-wins stable tie-break, equal
weights inside the book, un-invested weight in cash at 0%.

THE GROUPING IS CONSTRUCTION, NOT A DIAL, AND IT IS POINT-IN-TIME — idea 1289's convention,
reused unchanged so the two runs are comparable.  Each investable name is assigned to whichever
of NINE sector ETFs (XLK, XLF, XLV, XLE, XLI, XLY, XLP, XLU, XLB) its daily returns correlate
with most over THE FIRST 252 TRADING DAYS OF ITS OWN HISTORY.  XLRE (2015) and XLC (2018) are
excluded for having no history at the start of the tape.  A name is UNCLASSIFIED and cap-exempt
until its own first 252 days have elapsed, so no assignment uses data from after the day it is
first applied.  Kept names count against their group's budget; a full group is skipped and the
next-ranked name takes the slot.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, per panel: among cells clearing the IS analogues of 4b's three
non-half legs (Sharpe > SPY, MaxDD >= 0.60 x SPY MaxDD, CAGR >= 0.70 x SPY CAGR), take the
highest IS joint margin J = min(IS DD margin, IS CAGR margin); ties to the LOWER gross, then to
the TIGHTER cap.  J rather than IS Sharpe because idea 1290 showed IS Sharpe cannot size a book
(it picks gross 1.00 on every panel and fails 4b).  If that set is empty the declared fallback
is the highest IS J over the whole grid, and the run says the strict set was empty.  Then
2017-2026 is read ONCE.

ONE ARM WAS ADDED AFTER THE MAIN GRID WAS READ, AND IT IS LABELLED AS SUCH.  Arm H runs the
rule-8 pick and three declared comparands through idea 1292's 15-point phase x delay stress
ensemble.  It was NOT pre-registered here; it is added because the pick's DD margin (the leg
every capped book in this grid binds on) is thinner than the 2.2 pp that ideas 1253 / 1287 /
1292 measured that ensemble to move the same leg, which makes a single-point pass unsafe to
publish as a capital verdict.  Its decision rule — ROBUST := clears 4b at all 15 points — is
idea 1292's, fixed before this run existed and not chosen here.  Every point is published.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists and SMALL is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped first).
Delisted, acquired and bankrupt names are absent from all three.  This flatters every momentum
book here and it flatters the UNCAPPED book most, because the corner the screen concentrates
into is exactly the corner whose survivors are known — so the cap's measured cost is, if
anything, an OVER-statement of its cost on a real tape.  Nothing here estimates live expectancy.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-the-CERTIFIED-U56-g0.65-BOOK-AFFORD-a-SECTOR-CAP-the-g0.75-one-could-NOT_cloud.py
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
from engine import rebalance_mask, backtest  # noqa: E402

OUT = Path(str(Path(__file__))[:-3])   # stem carries dots ("g0.65"); with_suffix would truncate
WARMUP, MAXVOL, REF_COST, LAG = 260, 0.60, 10.0, 1
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_CAD = 20, 126, "W"                       # frozen
CAPS = [2, 3, 5, 8, 20]                              # dial 1 (20 = no cap)
GROSSES = [round(0.45 + 0.05 * i, 2) for i in range(9)]   # dial 2
G_1290, G_1289 = 0.65, 0.75                          # the two committed grosses
SECTORS = ["XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB"]
CLASSIFY_DAYS = 252
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


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        m = rebalance_mask(px.index, A_CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, C.shape[1])), C[:-1]])


def sector_returns(idx):
    px = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    return px[SECTORS].reindex(idx, method="ffill").pct_change()


def classify(pan):
    """Point-in-time group per investable name (idea 1289's convention, unchanged)."""
    S = sector_returns(pan.idx).values
    T, K = len(pan.idx), len(pan.iinv)
    grp = np.full(K, -1, dtype=np.int64)
    ready = np.full(K, T, dtype=np.int64)
    for k, ci in enumerate(pan.iinv):
        r = pan.px.iloc[:, ci].pct_change().values
        ok = np.flatnonzero(np.isfinite(r) & (pan.priced[:, ci]))
        ok = ok[ok > 0]
        if len(ok) < CLASSIFY_DAYS:
            continue
        w = ok[:CLASSIFY_DAYS]
        ready[k] = int(w[-1]) + 1
        x = r[w]
        best, bg = -np.inf, -1
        for g in range(len(SECTORS)):
            y = S[w, g]
            m = np.isfinite(x) & np.isfinite(y)
            if m.sum() < 60:
                continue
            xs, ys = x[m] - x[m].mean(), y[m] - y[m].mean()
            den = np.sqrt((xs * xs).sum() * (ys * ys).sum())
            if den <= 0:
                continue
            c = float((xs * ys).sum() / den)
            if c > best:
                best, bg = c, g
        grp[k] = bg
        if bg < 0:
            ready[k] = T
    return grp, ready


def decision_rows(idx, w):
    """One decision row per calendar week: the LAST trading row whose weekday is <= w.
    w = 4 (Fri) is the incumbent's 'last trading day of the week' convention (idea 1292)."""
    pos = np.arange(len(idx))
    ok = idx.weekday <= w
    ser = pd.Series(pos[ok], index=idx.to_period("W")[ok])
    return np.sort(ser.groupby(level=0).max().values)


def build_capped_pd(pan, N, cap, grp, ready, w, d):
    """build_capped, but deciding on weekday phase `w` and applying `d` rows later.
    Returns the unit-gross frame and the application rows."""
    dec = decision_rows(pan.idx, w)
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keepm = app < T
    dec, app = dec[keepm], app[keepm]
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    ng = int(grp.max()) + 1 if (grp >= 0).any() else 1
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        cnt = np.zeros(ng, dtype=np.int64)
        for c in keep:
            if grp[c] >= 0 and t >= ready[c]:
                cnt[grp[c]] += 1
        ks = set(keep)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                c = int(c)
                gg = grp[c] if t >= ready[c] else -1
                if gg >= 0 and cnt[gg] >= cap:
                    continue
                take.append(c)
                if gg >= 0:
                    cnt[gg] += 1
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


def nrun_at(pan, Wt, app):
    """nrun for an arbitrary set of application rows."""
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


def build_capped(pan, N, cap, grp, ready):
    """Min-hold top-N frame at UNIT gross, at most `cap` names per group; group -1 exempt.
    cap >= N is no cap and reproduces the incumbent's frame. Independent of gross."""
    reb = pan.reb
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    ng = int(grp.max()) + 1 if (grp >= 0).any() else 1
    for i, t in enumerate(reb):
        ts = max(t - LAG, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        cnt = np.zeros(ng, dtype=np.int64)
        for c in keep:
            if grp[c] >= 0 and t >= ready[c]:
                cnt[grp[c]] += 1
        ks = set(keep)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in ks:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if len(take) >= need or not np.isfinite(k[c]):
                    break
                c = int(c)
                g = grp[c] if t >= ready[c] else -1
                if g >= 0 and cnt[g] >= cap:
                    continue
                take.append(c)
                if g >= 0:
                    cnt[g] += 1
        new = np.full(K, -1, dtype=np.int64)
        for c in ks:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt):
    rets, Cp, reb = pan.rets, pan.Cp, pan.reb
    T, M = rets.shape
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
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
    Ro, So = mt(r[oos]), mt(spy[oos])
    Ri, Si = mt(r[ins]), mt(spy[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    dd_m = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"])
    cg_m = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    is_dd = 100.0 * (Ri["MaxDD"] - 0.60 * Si["MaxDD"])
    is_cg = 100.0 * (Ri["CAGR"] - 0.70 * Si["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_Sharpe=Ri["Sharpe"], IS_CAGR=Ri["CAGR"],
                IS_MaxDD=Ri["MaxDD"], OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"],
                OOS_MaxDD=Ro["MaxDD"], dd_margin_pp=dd_m, cagr_margin_pp=cg_m,
                J=min(dd_m, cg_m), IS_J=min(is_dd, is_cg),
                is_b_sh=Ri["Sharpe"] > Si["Sharpe"], is_b_dd=is_dd >= 0.0,
                is_b_cagr=is_cg >= 0.0,
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], n_drop)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1295 (lane cloud, 2026-09-18) — does the CERTIFIED U56 g=0.65 BOOK AFFORD a SECTOR")
    say("CAP that the g=0.75 one could NOT?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): GROUP CAP {CAPS} x GROSS {GROSSES} = 45 cells/panel, 135 published.")
    say(f"  FROZEN: N={A_N}, H={A_H}, weekly, t+1, {REF_COST:.0f} bps, above-200d & vol20<0.60,")
    say("          equal weights, 260-row warm-up, cash at 0%. N is NOT re-opened (third dial).")
    say("  GROUPING (construction, point-in-time): argmax correlation with one of the nine sector")
    say(f"  ETFs {SECTORS} over a name's FIRST {CLASSIFY_DAYS} own trading days; unclassified and")
    say("  cap-exempt until then. Idea 1289's convention, reused unchanged.")
    say("  OUTCOMES: (A) GROSS BUYS THE CAP  (B) UNAFFORDABLE  (C) CAP IRRELEVANT.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY = benchmark only.")
    say("")

    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for pan in panels:
        spy = pan.spy[WARMUP:]
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST,
                        freq="W")["returns"].values[WARMUP:]
        idx = pan.idx[WARMUP:]
        h1, h2, _, oos = windows(idx)
        B[pan.name] = dict(spy=spy, live=live, idx=idx)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[oos])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[h1])['Sharpe']:7.4f} {mt(ser[h2])['Sharpe']:7.4f} {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
    say("")

    # ---------------------------------------------------------- the grid
    rows = []
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        grp, ready = classify(pan)
        B[pan.name]["grp"], B[pan.name]["ready"] = grp, ready
        nunc = int((grp < 0).sum())
        say(f"  {pan.name}: {len(grp) - nunc} of {len(grp)} names classified; {nunc} never.")
        for cap in CAPS:
            W1 = build_capped(pan, A_N, cap, grp, ready)
            nh = (W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1)
            for g in GROSSES:
                gr, tu = nrun(pan, W1 * g)
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, cap=cap, gross=g, avg_names=float(nh.mean()),
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)
    say("")

    # ---------------------------------------------------------- anchors
    say("=" * 100)
    say("ARM B — THE TWO ANCHOR CHECKS")
    say("=" * 100)
    say("")
    ok_all = True
    for tag, cap, g, tgt in (
            ("incumbent (1287/1292)", 20, G_1289,
             dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)),
            ("1289 capped c=5", 5, G_1289,
             dict(CAGR=0.1591, Sharpe=1.2115, MaxDD=-0.2176, OOS_CAGR=0.1688, OOS_Sharpe=1.2258))):
        a = G[(G.panel == "U56") & (G.cap == cap) & (G.gross == g)].iloc[0]
        say(f"  --- U56 c={cap} g={g}: {tag}")
        ok = True
        for k, v in tgt.items():
            say(f"      {k:10} {a[k]:12.4f} vs {v:12.4f}  diff {a[k] - v:10.2e}")
            ok &= abs(a[k] - v) < 5e-4
        say(f"      REPRODUCES: {'YES' if ok else 'NO'}  (4b {'PASS' if a.pass4b else 'FAIL'})")
        ok_all &= ok
    say("")
    say(f"  BOTH ANCHORS REPRODUCE: {'YES' if ok_all else 'NO'}.")
    if not ok_all:
        say("  *** An anchor does NOT reproduce; no verdict below may be taken on these numbers.")
    say("")

    # ---------------------------------------------------------- grid table
    say("=" * 100)
    say("ARM C — THE 135-CELL GRID (every cell published; dd/cg/J in pp on the full sample)")
    say("=" * 100)
    say("")
    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 84)
        say(f"  {'cap':>4} {'gross':>6} {'held':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
            f"{'H1':>7} {'H2':>7} {'OOScagr':>8} {'OOSsh':>7} {'ddmar':>7} {'cgmar':>7} "
            f"{'J':>7} {'turn':>5} {'4a':>3} {'4b':>3}")
        for cap in CAPS:
            for _, x in G[(G.panel == pan.name) & (G.cap == cap)].iterrows():
                mark = ""
                if cap == 20 and x.gross == G_1289:
                    mark = " <-1289 anchor"
                elif cap == 20 and x.gross == G_1290:
                    mark = " <-1290 certified"
                say(f"  {x.cap:4d} {x.gross:6.2f} {x.avg_names:6.2f} {x.CAGR:8.2%} "
                    f"{x.Sharpe:8.4f} {x.MaxDD:8.2%} {x.H1:7.4f} {x.H2:7.4f} {x.OOS_CAGR:8.2%} "
                    f"{x.OOS_Sharpe:7.4f} {x.dd_margin_pp:7.2f} {x.cagr_margin_pp:7.2f} "
                    f"{x.J:7.2f} {x.turnover_yr:5.2f} {'Y' if x.pass4a else '.':>3} "
                    f"{'Y' if x.pass4b else '.':>3}{mark}")
            say("")
    say(f"  GRID-WIDE: 4b passes {int(G.pass4b.sum())} of {len(G)}; 4a passes {int(G.pass4a.sum())}.")
    say("  4b by panel: " + ", ".join(
        f"{p}: {int(G[G.panel == p].pass4b.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + ".")
    say("  4b by cap: " + ", ".join(
        f"c={c}: {int(G[G.cap == c].pass4b.sum())}/{len(G[G.cap == c])}" for c in CAPS) + ".")
    say("")

    nm = dict(b_h1="H1 Sharpe", b_h2="H2 Sharpe", b_oos="OOS Sharpe", b_dd="MaxDD cap",
              b_cagr="CAGR floor")
    F = G[~G.pass4b]
    say(f"  WHICH LEG BINDS over the {len(F)} failing cells of {len(G)}:")
    say(f"  {'leg':12} {'fails':>7} {'share':>8} {'SOLE binder':>12}")
    for k, v in nm.items():
        f = ~F[k]
        sole = f & (F[[c for c in nm if c != k]].all(axis=1))
        say(f"  {v:12} {int(f.sum()):7d} {f.mean():8.4f} {int(sole.sum()):12d}")
    say("")

    # ---------------------------------------------------------- frontier
    say("=" * 100)
    say("ARM D — THE AFFORDABILITY FRONTIER: the LOWEST gross rung at which each cap clears 4b")
    say("=" * 100)
    say("")
    FR = []
    for pan in panels:
        base = G[(G.panel == pan.name) & (G.cap == 20)]
        g20 = base[base.pass4b].gross.min() if base.pass4b.any() else np.nan
        for cap in CAPS:
            s = G[(G.panel == pan.name) & (G.cap == cap)].sort_values("gross")
            p = s[s.pass4b]
            lo = float(p.gross.min()) if len(p) else np.nan
            hi = float(p.gross.max()) if len(p) else np.nan
            FR.append(dict(panel=pan.name, cap=cap, n_pass=int(len(p)), lowest_pass_gross=lo,
                           highest_pass_gross=hi,
                           rungs_vs_uncapped=(np.nan if (np.isnan(lo) or pd.isna(g20))
                                              else int(round((lo - g20) / 0.05))),
                           affordable_at_or_below_075=bool(len(p) and lo <= G_1289),
                           pass_at_065=bool(s[s.gross == G_1290].pass4b.iloc[0]),
                           pass_at_075=bool(s[s.gross == G_1289].pass4b.iloc[0]),
                           bestJ=float(s.J.max()), bestJ_gross=float(s.loc[s.J.idxmax(), "gross"])))
    FRD = pd.DataFrame(FR)
    say(f"  {'panel':6} {'cap':>4} {'#4b':>4} {'lowest g':>9} {'highest g':>10} "
        f"{'rungs vs c=20':>14} {'4b@0.65':>8} {'4b@0.75':>8} {'best J':>7} {'at g':>5}")
    for _, x in FRD.iterrows():
        say(f"  {x.panel:6} {x.cap:4d} {x.n_pass:4d} "
            f"{('n/a' if pd.isna(x.lowest_pass_gross) else f'{x.lowest_pass_gross:.2f}'):>9} "
            f"{('n/a' if pd.isna(x.highest_pass_gross) else f'{x.highest_pass_gross:.2f}'):>10} "
            f"{('n/a' if pd.isna(x.rungs_vs_uncapped) else f'{int(x.rungs_vs_uncapped):+d}'):>14} "
            f"{'Y' if x.pass_at_065 else '.':>8} {'Y' if x.pass_at_075 else '.':>8} "
            f"{x.bestJ:7.2f} {x.bestJ_gross:5.2f}")
    say("")
    say("  Read: 'rungs vs c=20' is what the concentration limit costs in SIZE — how much lower")
    say("  the book must be run for the same 4b pass. 0 means the cap is free at this gross.")
    say("")

    # ---------------------------------------------------------- matched gross
    say("=" * 100)
    say("ARM E — WHAT THE CAP BUYS AT MATCHED GROSS (each cap minus c=20 at the SAME gross,")
    say("so no effect below is read through a size change)")
    say("=" * 100)
    say("")
    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 60)
        say(f"  {'gross':>6} {'cap':>4} {'dSharpe':>9} {'dCAGR pp':>9} {'dMaxDD pp':>10} "
            f"{'dOOS Sh':>9} {'dJ pp':>7}")
        for g in (G_1290, G_1289):
            b = G[(G.panel == pan.name) & (G.cap == 20) & (G.gross == g)].iloc[0]
            for cap in CAPS:
                if cap == 20:
                    continue
                x = G[(G.panel == pan.name) & (G.cap == cap) & (G.gross == g)].iloc[0]
                say(f"  {g:6.2f} {cap:4d} {x.Sharpe - b.Sharpe:9.4f} "
                    f"{100 * (x.CAGR - b.CAGR):9.2f} {100 * (x.MaxDD - b.MaxDD):10.2f} "
                    f"{x.OOS_Sharpe - b.OOS_Sharpe:9.4f} {x.J - b.J:7.2f}")
        say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM F — RULE 8 WALK-FORWARD: BOTH dials chosen on warm-up..2016 ONLY, 2017-2026 ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER (declared in the header): among cells clearing the IS analogues of 4b's three")
    say("  non-half legs, the highest IS J; ties to LOWER gross then TIGHTER cap. Fallback if")
    say("  empty: highest IS J over the grid.")
    say("")
    WF = []
    for pan in panels:
        s = G[G.panel == pan.name].copy()
        strict = s[s.is_b_sh & s.is_b_dd & s.is_b_cagr]
        empty = len(strict) == 0
        pool = s if empty else strict
        pool = pool.sort_values(["IS_J", "gross", "cap"], ascending=[False, True, True])
        pick = pool.iloc[0]
        oos_spy = mt(B[pan.name]["spy"][windows(B[pan.name]["idx"])[3]])
        oos_liv = mt(B[pan.name]["live"][windows(B[pan.name]["idx"])[3]])
        inc = s[(s.cap == 20) & (s.gross == G_1289)].iloc[0]
        cert = s[(s.cap == 20) & (s.gross == G_1290)].iloc[0]
        WF.append(dict(panel=pan.name, strict_empty=empty, pool=len(pool),
                       pick_cap=int(pick.cap), pick_gross=float(pick.gross),
                       IS_J=float(pick.IS_J), OOS_CAGR=float(pick.OOS_CAGR),
                       OOS_Sharpe=float(pick.OOS_Sharpe), OOS_MaxDD=float(pick.OOS_MaxDD),
                       pass4b=bool(pick.pass4b), pass4a=bool(pick.pass4a),
                       full_CAGR=float(pick.CAGR), full_Sharpe=float(pick.Sharpe),
                       full_MaxDD=float(pick.MaxDD), H1=float(pick.H1), H2=float(pick.H2),
                       cert_OOS_Sharpe=float(cert.OOS_Sharpe), cert_OOS_CAGR=float(cert.OOS_CAGR),
                       cert_pass4b=bool(cert.pass4b), inc_OOS_Sharpe=float(inc.OOS_Sharpe),
                       inc_OOS_CAGR=float(inc.OOS_CAGR), inc_pass4b=bool(inc.pass4b),
                       spy_OOS_Sharpe=oos_spy["Sharpe"], spy_OOS_CAGR=oos_spy["CAGR"],
                       spy_OOS_MaxDD=oos_spy["MaxDD"], live_OOS_Sharpe=oos_liv["Sharpe"],
                       live_OOS_CAGR=oos_liv["CAGR"], live_OOS_MaxDD=oos_liv["MaxDD"]))
    W8 = pd.DataFrame(WF)
    say(f"  {'panel':6} {'pick':>14} {'strict?':>8} {'IS J':>7} {'full CAGR':>10} {'Sharpe':>8} "
        f"{'MaxDD':>8} {'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8} {'4b':>4}")
    for _, x in W8.iterrows():
        say(f"  {x.panel:6} {f'c={x.pick_cap},g={x.pick_gross}':>14} "
            f"{'EMPTY' if x.strict_empty else 'ok':>8} {x.IS_J:7.2f} {x.full_CAGR:10.2%} "
            f"{x.full_Sharpe:8.4f} {x.full_MaxDD:8.2%} {x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} "
            f"{x.OOS_MaxDD:8.2%} {'PASS' if x.pass4b else 'FAIL':>4}")
    say("")
    say("  Same OOS window (2017-01-01 ..), pick vs the two committed books vs live vs SPY:")
    say(f"  {'panel':6} {'series':26} {'CAGR':>9} {'Sharpe':>9} {'MaxDD':>9} {'4b':>5}")
    for _, x in W8.iterrows():
        say(f"  {x.panel:6} {f'PICK c={x.pick_cap} g={x.pick_gross}':26} {x.OOS_CAGR:9.2%} "
            f"{x.OOS_Sharpe:9.4f} {x.OOS_MaxDD:9.2%} {'PASS' if x.pass4b else 'FAIL':>5}")
        say(f"  {x.panel:6} {'  1290 certified c=20 g=.65':26} {x.cert_OOS_CAGR:9.2%} "
            f"{x.cert_OOS_Sharpe:9.4f} {'':>9} {'PASS' if x.cert_pass4b else 'FAIL':>5}")
        say(f"  {x.panel:6} {'  incumbent c=20 g=.75':26} {x.inc_OOS_CAGR:9.2%} "
            f"{x.inc_OOS_Sharpe:9.4f} {'':>9} {'PASS' if x.inc_pass4b else 'FAIL':>5}")
        say(f"  {x.panel:6} {'  RULES v2 (live)':26} {x.live_OOS_CAGR:9.2%} "
            f"{x.live_OOS_Sharpe:9.4f} {x.live_OOS_MaxDD:9.2%}")
        say(f"  {x.panel:6} {'  SPY':26} {x.spy_OOS_CAGR:9.2%} {x.spy_OOS_Sharpe:9.4f} "
            f"{x.spy_OOS_MaxDD:9.2%}")
    say("")

    # ---------------------------------------------------------- stress
    say("=" * 100)
    say("ARM H — STRESS ENSEMBLE (ADDED AFTER THE MAIN GRID WAS READ; see the header). Idea")
    say("1292's 15 points: 5 decision weekdays x 3 execution lags. ROBUST := 4b at ALL 15.")
    say("=" * 100)
    say("")
    pk = W8[W8.panel == "U56"].iloc[0]
    CELLS = [(int(pk.pick_cap), float(pk.pick_gross)), (5, 0.60), (5, 0.55), (20, G_1290),
             (20, G_1289)]
    pan = panels[0]
    spy, live, idx = B["U56"]["spy"], B["U56"]["live"], B["U56"]["idx"]
    grp, ready = B["U56"]["grp"], B["U56"]["ready"]
    WDN = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    srows = []
    for cap, g in CELLS:
        for w in range(5):
            for d in (1, 2, 3):
                Wf, app = build_capped_pd(pan, A_N, cap, grp, ready, w, d)
                gr, tu = nrun_at(pan, Wf * g, app)
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                rec = legs(r, spy, live, idx)
                rec.update(cap=cap, gross=g, phase=WDN[w], delay=d,
                           anchor=(w == 4 and d == 1))
                srows.append(rec)
    S = pd.DataFrame(srows)
    say(f"  {'cap':>4} {'gross':>6} {'4b pts':>7} {'ROBUST':>7} {'anchor DD':>10} "
        f"{'worst DD':>9} {'worst ddmar':>12} {'worst cgmar':>12} {'worst OOSsh':>12} "
        f"{'DD spread pp':>13}")
    for cap, g in CELLS:
        sub = S[(S.cap == cap) & (S.gross == g)]
        anc = sub[sub.anchor].iloc[0]
        say(f"  {cap:4d} {g:6.2f} {int(sub.pass4b.sum()):4d}/15 "
            f"{('YES' if sub.pass4b.all() else '.'):>7} {anc.MaxDD:10.2%} "
            f"{sub.MaxDD.min():9.2%} {sub.dd_margin_pp.min():12.2f} "
            f"{sub.cagr_margin_pp.min():12.2f} {sub.OOS_Sharpe.min():12.4f} "
            f"{100 * (sub.MaxDD.max() - sub.MaxDD.min()):13.2f}")
    say("")
    say("  Every point of the pick, published:")
    sub = S[(S.cap == int(pk.pick_cap)) & (S.gross == float(pk.pick_gross))]
    say(f"  {'phase':>6} {'lag':>4} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'OOS Sh':>8} "
        f"{'ddmar':>7} {'cgmar':>7} {'4b':>4}")
    for _, x in sub.iterrows():
        say(f"  {x.phase:>6} {int(x.delay):4d} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
            f"{x.OOS_Sharpe:8.4f} {x.dd_margin_pp:7.2f} {x.cagr_margin_pp:7.2f} "
            f"{'Y' if x.pass4b else '.':>4}")
    say("")
    S.to_csv(Path(str(OUT) + ".stress.csv"), index=False)
    ROBUST_PICK = bool(sub.pass4b.all())

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM G — THE ANSWER")
    say("=" * 100)
    say("")
    u = FRD[FRD.panel == "U56"]
    tight = u[u.cap <= 5]
    bought = tight[tight.affordable_at_or_below_075 & ~tight.pass_at_075]
    if len(bought):
        outcome = ("(A) GROSS BUYS THE CAP — a sector cap of " +
                   "/".join(str(int(c)) for c in bought.cap) +
                   " clears 4b on U56 at a gross at or below 0.75 where it FAILS at 0.75")
    elif not tight.affordable_at_or_below_075.any():
        outcome = ("(B) UNAFFORDABLE — no cap <= 5 clears 4b at any gross rung at or below 0.75 "
                   "on U56")
    else:
        outcome = ("(C) CAP IRRELEVANT / ALREADY AFFORDABLE — every tight cap that passes at some "
                   "gross also passes at 0.75, so gross buys nothing the cap did not already have")
    say(f"  OUTCOME: {outcome}.")
    say("")
    pick = W8[W8.panel == "U56"].iloc[0]
    if pick.pass4b and pick.OOS_Sharpe > pick.spy_OOS_Sharpe:
        say(f"  RULE 8 REACHES a 4b-passing capped cell on U56: c={pick.pick_cap}, "
            f"g={pick.pick_gross} — full {pick.full_CAGR:.2%} / {pick.full_Sharpe:.4f} / "
            f"{pick.full_MaxDD:.2%}, halves {pick.H1:.4f} / {pick.H2:.4f}, OOS "
            f"{pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:.2%}.")
        if pick.pick_cap < 20 and ROBUST_PICK:
            say("  ...and it is STRESS-ROBUST (4b at all 15 phase x delay points, arm H).")
            say("  KEEP-4b CANDIDATE (capped). Memo written; RULES.md NOT touched (rule 6).")
        elif pick.pick_cap < 20:
            say("  ...but it is NOT STRESS-ROBUST (arm H): it fails 4b at some phase x delay")
            say("  point, the same way ideas 1253 and 1287 killed the uncapped incumbent.")
            say("  PARK, not KEEP — it satisfies rule 4's 4b text and rule 8 at the anchor and")
            say("  no more. Nothing is promoted and RULES.md is NOT touched.")
        else:
            say("  The chooser lands on the UNCAPPED cell: the cap is not selected in-sample, so")
            say("  nothing new is promoted and the capped cells are PARK at most.")
    else:
        say("  RULE 8's pick does NOT clear 4b and/or does not beat SPY OOS on U56 — PARK/KILL.")
    say("")
    say("  CAVEAT: the 135-cell GRID is read at ONE rebalance phase and ONE execution lag; only")
    say("  the five cells of arm H carry the 15-point ensemble. Every capped book in the grid")
    say("  binds on the MaxDD leg, which that ensemble moves by up to 2.2 pp.")
    say("")
    say("  SURVIVORSHIP (rule 9): current constituents only, which flatters the UNCAPPED book")
    say("  most — the corner the screen concentrates into is the corner whose survivors are")
    say("  known — so the cap's measured cost is if anything an OVER-statement.")
    say("")
    say(f"  ({time.time() - t0:.1f}s)")

    G.to_csv(Path(str(OUT) + ".grid.csv"), index=False)
    FRD.to_csv(Path(str(OUT) + ".frontier.csv"), index=False)
    W8.to_csv(Path(str(OUT) + ".walkforward.csv"), index=False)
    Path(str(OUT) + ".log.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nwrote {OUT.name}.grid.csv / .frontier.csv / .walkforward.csv / .log.txt")


if __name__ == "__main__":
    main()
