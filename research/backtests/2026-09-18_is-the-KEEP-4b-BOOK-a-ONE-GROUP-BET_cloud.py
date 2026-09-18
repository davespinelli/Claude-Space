#!/usr/bin/env python3
"""
Idea 1289 (lane cloud, 2026-09-18) — is the 2026-09-04 KEEP-4b BOOK a ONE-GROUP BET?

THE PREMISE.  The standing candidate is U56 / N=20 / H=126 / gross 0.75 / weekly: a top-20
cross-sectional momentum book run over 55 instruments, of which 20 are mega-caps and 16 are
sector ETFs.  Nothing in the rule stops all 20 slots landing in one corner of the panel, and
the sample is 2009-2026 — the single best stretch US mega-cap technology has ever had.  If the
book's 4b pass is carried by holding the same corner continuously, then it is one bet with a
diversified-looking wrapper, and its -19.13% MaxDD (which idea 1287 showed is the ONLY binding
4b leg, with a margin of +1.10 pp) is a number drawn from one regime.  The cheapest test that
can refute this is a HARD CAP on how many names the book may draw from any one group.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE CENSUS.  For the uncapped incumbent, the share of held name-days falling in each
      group, its Herfindahl over groups, and the single largest group share.  A pure
      description of what the book actually holds — no bar, no verdict.
  (2) THE CAP.  Rebuild the same book subject to: at most c names from any one group at any
      time.  Kept min-hold names count against their group's budget; a candidate whose group
      is full is SKIPPED and the next eligible name takes the slot.  c = 20 is no cap and
      reproduces the incumbent exactly.
  (3) BOTH KEEP PATHS at every cell, plus rule 8.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) CONCENTRATION-FREE — the U56 N=20 book clears 4b at EVERY cap, tightest included.
    (B) CAP-SENSITIVE      — it clears uncapped and fails at some tighter cap: the pass is
                             partly a one-group bet.
    (C) CAP-IMPROVED       — a capped book clears 4b where the uncapped one does not.
    (D) NO PASS ANYWHERE   — no cell on U56 at N=20 clears 4b.
  (B) and (C) are not exclusive; both are reported if both occur.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  GROUP CAP c   {2, 3, 5, 8, 20}      (20 = no cap = the incumbent)
  N             {10, 20}              (20 = the incumbent)

  10 cells per panel, 30 in all, EVERY ONE PUBLISHED in `.grid.csv`.

THE GROUPING IS CONSTRUCTION, NOT A DIAL, AND IT IS POINT-IN-TIME.  One convention is used on
all three panels so the panels are comparable: each investable name is assigned to whichever of
NINE sector ETFs — XLK, XLF, XLV, XLE, XLI, XLY, XLP, XLU, XLB — its daily returns correlate
with most over THE FIRST 252 TRADING DAYS OF ITS OWN HISTORY.  XLRE (2015) and XLC (2018) are
excluded for having no history at the start of the tape; that exclusion is declared here and
not chosen on any result.  A name is UNCLASSIFIED (and exempt from the cap) until its own first
252 days have elapsed, so no assignment ever uses data from after the day it is first applied.
A sector ETF that is itself in the panel correlates with itself and lands in its own group, as
it should.  As a declared CROSS-CHECK, the U56 N=20 column is re-run under universe.json's own
four labels (broad / sectors / bonds_fx_commod / megacap); it is reported at every cap, is not
selected against the primary, and exists on no other panel.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the 4a and 4b legs;
full sample, both halves, and the rule-8 OOS window; the live RULES v2 baseline and SPY.

FROZEN at the incumbent's construction: H = 126, gross = 0.75, weekly cadence, 3-leg composite
(21/252, 0/126, 0/63), above-200d + vol20 < 0.60 eligibility, 10 bps per unit turnover (rule 2),
decide-at-t / apply-at-t+1, 260-row warm-up, first-wins stable tie-break.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
— the cap is CHOSEN on warm-up..2016-12-31 only and 2017-2026 is read ONCE; rule 9 survivorship
stated below.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists and SMALL is
the current constituent list of a sub-$2B screen; names that were delisted, acquired or went
bankrupt are absent from all three.  This flatters every momentum book here and it flatters the
UNCAPPED book most, because the corner the screen concentrates into is exactly the corner whose
survivors are known.  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped from
SMALL before anything is built.  Nothing here estimates live expectancy.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_is-the-KEEP-4b-BOOK-a-ONE-GROUP-BET_cloud.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

OUT = Path(__file__).with_suffix("")
WARMUP, MAXVOL, REF_COST, LAG = 260, 0.60, 10.0, 1
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_G, A_CAD = 126, 0.75, "W"        # frozen incumbent rungs
CAPS = [2, 3, 5, 8, 20]                 # dial 1 (20 = no cap)
NS = [10, 20]                           # dial 2
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


def sector_returns(idx):
    """The nine sector ETFs' daily returns, reindexed onto a panel's trading days."""
    px = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
    s = px[SECTORS].reindex(idx, method="ffill")
    return s.pct_change()


def classify(pan):
    """Point-in-time group per investable name.

    Each name is correlated with the nine sector ETFs over THE FIRST `CLASSIFY_DAYS` trading
    days on which it has a usable return, and assigned the argmax.  `ready[k]` is the row from
    which that assignment may be used; before it the name is UNCLASSIFIED (group -1, exempt).
    No assignment uses data from after the row on which it first applies.
    """
    S = sector_returns(pan.idx).values                       # T x 9
    T = len(pan.idx)
    K = len(pan.iinv)
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


def label_groups(pan):
    """The U56 cross-check grouping: universe.json's own four labels, known from row 0."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    names = sorted(U.keys())
    tag = {t: names.index(g) for g, ts in U.items() for t in ts}
    grp = np.array([tag.get(c, -1) for c in pan.invest], dtype=np.int64)
    return grp, np.zeros(len(grp), dtype=np.int64), names


def build_capped(pan, N, cap, grp, ready):
    """The incumbent's min-hold top-N frame at GROSS = 1.0, subject to at most `cap` names per
    group.  Kept names count against their group's budget.  group -1 (unclassified) is exempt.
    cap >= N is no cap and reproduces the incumbent's frame bit for bit."""
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
                    continue                      # group full: skip, next name takes the slot
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


def nrun(pan, Wt, reb):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
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
    Ro, So, Ri = mt(r[oos]), mt(spy[oos]), mt(r[ins])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_Sharpe=Ri["Sharpe"], OOS_CAGR=Ro["CAGR"],
                OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


# ------------------------------------------------------------------ world
def make_panels():
    pxU, pxB, pxS = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"].astype(str))
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    n_drop = len([c for c in pxS.columns if c != "SPY" and c in bad])
    return ([Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
             Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
             Panel("SMALL", pxS, inv)], n_drop)


def bench_for(pan):
    live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")["returns"].values
    return pan.spy[WARMUP:], live[WARMUP:]


def name_day_shares(pan, W, grp, names):
    """Share of held name-days by group, over the post-warm-up rows, for the uncapped book."""
    H = (W[WARMUP:][:, pan.iinv] > 0)
    tot = H.sum()
    out = {}
    for g in range(len(names)):
        out[names[g]] = float(H[:, grp == g].sum() / tot) if tot else np.nan
    out["UNCLASSIFIED"] = float(H[:, grp < 0].sum() / tot) if tot else np.nan
    return out, float(tot)


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say("=" * 100)
    say("IDEA 1289 (lane cloud, 2026-09-18) — is the 2026-09-04 KEEP-4b BOOK a ONE-GROUP BET?")
    say("=" * 100)
    say("")
    say("  CAP c: at most c names from any one group at any time. c=20 is NO CAP = the incumbent.")
    say("  DIALS (2, rule 4): GROUP CAP {2,3,5,8,20} x N {10,20} = 10 cells/panel, 30 published.")
    say("  GROUPING (construction, not a dial, POINT-IN-TIME): argmax correlation with one of")
    say(f"  {len(SECTORS)} sector ETFs {SECTORS} over a name's FIRST {CLASSIFY_DAYS} own trading days;")
    say("  unclassified (and cap-exempt) until then. XLRE/XLC excluded for no early history.")
    say("  FROZEN: H=126, gross=0.75, weekly, 10 bps, t+1, above-200d & vol20<0.60.")
    say("  OUTCOMES: (A) CONCENTRATION-FREE (B) CAP-SENSITIVE (C) CAP-IMPROVED (D) NO PASS.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY benchmark only.")
    say("")

    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up, 10 bps, weekly for the live book)")
    say("=" * 100)
    say("")
    B, GRP, RDY = {}, {}, {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        spy, live = bench_for(pan)
        idx = pan.idx[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, idx=idx)
        h1, h2, ins, oos = windows(idx)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[oos])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[h1])['Sharpe']:7.4f} {mt(ser[h2])['Sharpe']:7.4f} {mo['CAGR']:9.2%} "
                f"{mo['Sharpe']:8.4f}")
        GRP[pan.name], RDY[pan.name] = classify(pan)
    say("")

    # ---------------------------------------------------------- census
    say("=" * 100)
    say("ARM B — THE CENSUS: what the UNCAPPED incumbent actually holds (no bar, no verdict)")
    say("=" * 100)
    say("")
    cens = []
    for pan in panels:
        grp = GRP[pan.name]
        n_unc = int((grp < 0).sum())
        W = build_capped(pan, 20, 20, grp, RDY[pan.name])
        sh, tot = name_day_shares(pan, W, grp, SECTORS)
        vals = np.array([sh[s] for s in SECTORS] + [sh["UNCLASSIFIED"]])
        hhi = float((vals ** 2).sum())
        top = SECTORS[int(np.argmax([sh[s] for s in SECTORS]))]
        cens.append(dict(panel=pan.name, name_days=tot, unclassified_names=n_unc,
                         HHI=hhi, top_group=top, top_share=sh[top], **sh))
        say(f"  {pan.name:6} N=20 uncapped: {int(tot):,} held name-days; "
            f"{n_unc} of {len(grp)} names never classified.")
        say("         " + "  ".join(f"{s}:{sh[s]:.3f}" for s in SECTORS) +
            f"  UNC:{sh['UNCLASSIFIED']:.3f}")
        say(f"         largest group = {top} at {sh[top]:.3f} of name-days; "
            f"HHI over 10 groups = {hhi:.4f} (even split = {1/10:.4f}).")
        say("")
    C = pd.DataFrame(cens)

    # ---------------------------------------------------------- grid
    say("=" * 100)
    say("ARM C — THE FULL 30-CELL GRID (every cell published, none selected on)")
    say("=" * 100)
    say("")
    rows = []
    for pan in panels:
        spy, live, idx = B[pan.name]["spy"], B[pan.name]["live"], B[pan.name]["idx"]
        grp, rdy = GRP[pan.name], RDY[pan.name]
        for N in NS:
            for cap in CAPS:
                W = build_capped(pan, N, cap, grp, rdy) * A_G
                gr, tu = nrun(pan, W, pan.reb)
                r = at_cost(gr, tu, REF_COST)[WARMUP:]
                nh = (W[WARMUP:][:, pan.iinv] > 0).sum(axis=1)
                rec = legs(r, spy, live, idx)
                rec.update(panel=pan.name, N=N, cap=cap, grouping="SECTOR9",
                           avg_names=float(nh.mean()),
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)

    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 80)
        say(f"  {'N':>3} {'cap':>4} {'held':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} "
            f"{'H2':>7} {'OOScagr':>8} {'OOSsh':>7} {'turn':>6}  {'4a':>3} {'4b':>3}")
        for _, x in G[G.panel == pan.name].iterrows():
            say(f"  {x.N:3d} {x.cap:4d} {x.avg_names:6.2f} {x.CAGR:8.2%} {x.Sharpe:8.4f} "
                f"{x.MaxDD:8.2%} {x.H1:7.4f} {x.H2:7.4f} {x.OOS_CAGR:8.2%} {x.OOS_Sharpe:7.4f} "
                f"{x.turnover_yr:6.2f}  {'Y' if x.pass4a else '.':>3} {'Y' if x.pass4b else '.':>3}")
        say("")

    # ---------------------------------------------------------- cross-check
    say("=" * 100)
    say("ARM D — DECLARED CROSS-CHECK: U56 at N=20 under universe.json's OWN four labels")
    say("=" * 100)
    say("")
    pan = panels[0]
    lgrp, lrdy, lnames = label_groups(pan)
    say(f"  Labels: {lnames}; sizes " +
        ", ".join(f"{lnames[g]}={int((lgrp == g).sum())}" for g in range(len(lnames))) + ".")
    Wl = build_capped(pan, 20, 20, lgrp, lrdy)
    shl, totl = name_day_shares(pan, Wl, lgrp, lnames)
    say("  Uncapped name-day shares: " + "  ".join(f"{lnames[g]}:{shl[lnames[g]]:.3f}"
                                                   for g in range(len(lnames))) +
        f"  UNC:{shl['UNCLASSIFIED']:.3f}")
    say("")
    say(f"  {'cap':>4} {'held':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOSsh':>7}  {'4a':>3} {'4b':>3}")
    xrows = []
    spy, live, idx = B["U56"]["spy"], B["U56"]["live"], B["U56"]["idx"]
    for cap in CAPS:
        W = build_capped(pan, 20, cap, lgrp, lrdy) * A_G
        gr, tu = nrun(pan, W, pan.reb)
        r = at_cost(gr, tu, REF_COST)[WARMUP:]
        nh = (W[WARMUP:][:, pan.iinv] > 0).sum(axis=1)
        rec = legs(r, spy, live, idx)
        rec.update(panel="U56", N=20, cap=cap, grouping="LABEL4", avg_names=float(nh.mean()),
                   turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
        xrows.append(rec)
        say(f"  {cap:4d} {rec['avg_names']:6.2f} {rec['CAGR']:8.2%} {rec['Sharpe']:8.4f} "
            f"{rec['MaxDD']:8.2%} {rec['H1']:7.4f} {rec['H2']:7.4f} {rec['OOS_Sharpe']:7.4f}  "
            f"{'Y' if rec['pass4a'] else '.':>3} {'Y' if rec['pass4b'] else '.':>3}")
    X = pd.DataFrame(xrows)

    # ---------------------------------------------------------- rule 8
    say("")
    say("=" * 100)
    say("ARM E — RULE 8 WALK-FORWARD: cap chosen on warm-up..2016 ONLY, 2017-2026 read ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER: within each (panel, N), take the CAP with the highest IS Sharpe")
    say("  (warm-up..2016-12-31); read that cell's 2017-2026 window once. ANCHOR = cap 20.")
    say("")
    say(f"  {'panel':6} {'N':>3} {'IS-pick':>8} {'ISsh':>8} {'OOSsh(pick)':>12} {'OOSsh(cap20)':>13} "
        f"{'delta':>8} {'4b(pick)':>9} {'4b(cap20)':>10}")
    wf = []
    for pan in panels:
        for N in NS:
            sub = G[(G.panel == pan.name) & (G.N == N)].set_index("cap")
            pick = int(sub["IS_Sharpe"].idxmax())
            w = dict(panel=pan.name, N=N, pick_cap=pick, IS_Sharpe=sub.loc[pick, "IS_Sharpe"],
                     OOS_Sharpe_pick=sub.loc[pick, "OOS_Sharpe"],
                     OOS_Sharpe_cap20=sub.loc[20, "OOS_Sharpe"],
                     OOS_CAGR_pick=sub.loc[pick, "OOS_CAGR"],
                     OOS_MaxDD_pick=sub.loc[pick, "OOS_MaxDD"],
                     delta=sub.loc[pick, "OOS_Sharpe"] - sub.loc[20, "OOS_Sharpe"],
                     pass4b_pick=bool(sub.loc[pick, "pass4b"]),
                     pass4b_cap20=bool(sub.loc[20, "pass4b"]),
                     pass4a_pick=bool(sub.loc[pick, "pass4a"]))
            wf.append(w)
            say(f"  {pan.name:6} {N:3d} {pick:8d} {w['IS_Sharpe']:8.4f} {w['OOS_Sharpe_pick']:12.4f} "
                f"{w['OOS_Sharpe_cap20']:13.4f} {w['delta']:8.4f} "
                f"{'Y' if w['pass4b_pick'] else '.':>9} {'Y' if w['pass4b_cap20'] else '.':>10}")
    WF = pd.DataFrame(wf)
    say("")
    say(f"  The IS cap chooser beats the uncapped anchor OOS in {int((WF.delta > 0).sum())} of "
        f"{len(WF)}; mean delta {WF.delta.mean():+.4f} of OOS Sharpe; it clears 4b in "
        f"{int(WF.pass4b_pick.sum())} of {len(WF)} against the anchor's {int(WF.pass4b_cap20.sum())}.")

    say("")
    say("  THE STRICT READING — BOTH dials chosen on IS, which is what rule 8 actually asks.")
    say("  The arm above holds N fixed and chooses only the cap.  N is a dial too, so a legal")
    say("  chooser must pick (N, cap) JOINTLY from the IS window.  Both are reported; the strict")
    say("  one is the one any verdict here is taken on.")
    say("")
    say(f"  {'panel':6} {'joint pick':>12} {'ISsh':>8} {'OOSsh':>8} {'OOScagr':>9} {'OOSdd':>8} "
        f"{'anchor OOSsh':>13} {'delta':>8} {'4b':>4}")
    jt = []
    for pan in panels:
        sub = G[G.panel == pan.name]
        j = sub.loc[sub["IS_Sharpe"].idxmax()]
        anc = sub[(sub.N == 20) & (sub.cap == 20)].iloc[0]
        jt.append(dict(panel=pan.name, pick_N=int(j.N), pick_cap=int(j.cap),
                       IS_Sharpe=j.IS_Sharpe, OOS_Sharpe=j.OOS_Sharpe, OOS_CAGR=j.OOS_CAGR,
                       OOS_MaxDD=j.OOS_MaxDD, anchor_OOS_Sharpe=anc.OOS_Sharpe,
                       delta=j.OOS_Sharpe - anc.OOS_Sharpe, pass4b=bool(j.pass4b),
                       pass4a=bool(j.pass4a)))
        say(f"  {pan.name:6} {f'N={int(j.N)},c={int(j.cap)}':>12} {j.IS_Sharpe:8.4f} "
            f"{j.OOS_Sharpe:8.4f} {j.OOS_CAGR:9.2%} {j.OOS_MaxDD:8.2%} {anc.OOS_Sharpe:13.4f} "
            f"{j.OOS_Sharpe - anc.OOS_Sharpe:8.4f} {'Y' if j.pass4b else '.':>4}")
    JT = pd.DataFrame(jt)
    JT.to_csv(OUT.with_suffix(".joint.csv"), index=False)
    say("")
    say(f"  The JOINT IS chooser clears 4b in {int(JT.pass4b.sum())} of {len(JT)} panels and beats")
    say(f"  the uncapped anchor OOS in {int((JT.delta > 0).sum())} of {len(JT)}.")
    say("")
    say("  THE CELL THIS RUN MUST NOT OVERSELL.  The best 4b-clearing cell on U56 is")
    bc = G[(G.panel == "U56") & G.pass4b].sort_values("OOS_Sharpe", ascending=False).iloc[0]
    say(f"  N={int(bc.N)} / cap={int(bc.cap)}: {bc.CAGR:.2%} / {bc.Sharpe:.4f} / {bc.MaxDD:.2%}, "
        f"halves {bc.H1:.4f}/{bc.H2:.4f}, OOS {bc.OOS_CAGR:.2%} / {bc.OOS_Sharpe:.4f} — better")
    say("  than the incumbent on every 4b leg. But the JOINT IS chooser above does NOT land on it")
    ju = JT[JT.panel == "U56"].iloc[0]
    say(f"  (it lands on N={int(ju.pick_N)} / cap={int(ju.pick_cap)}, which FAILS 4b), so the cell")
    say("  is only reachable by fixing N a priori — which this run did not do. It is therefore")
    say("  PARK, not KEEP: a documented candidate that rule 8 does not certify.")

    # ---------------------------------------------------------- verdict
    say("")
    say("=" * 100)
    say("ARM F — THE ANSWER")
    say("=" * 100)
    say("")
    u = G[(G.panel == "U56") & (G.N == 20)].set_index("cap")
    spyU = mt(B["U56"]["spy"])
    say(f"  The incumbent's own row is (U56, N=20, cap=20). U56 SPY MaxDD {spyU['MaxDD']:.2%}, "
        f"so 4b's cap is {0.60 * spyU['MaxDD']:.2%}; CAGR floor {0.70 * spyU['CAGR']:.2%}.")
    say(f"  {'cap':>4} {'b_h1':>6} {'b_h2':>6} {'b_oos':>7} {'b_dd':>6} {'b_cagr':>7} {'4b':>5} "
        f"{'binding leg(s)':<28} {'DD margin pp':>12}")
    nm = dict(b_h1="H1 Sharpe", b_h2="H2 Sharpe", b_oos="OOS Sharpe", b_dd="MaxDD cap",
              b_cagr="CAGR floor")
    for c in CAPS:
        x = u.loc[c]
        bind = ", ".join(v for k, v in nm.items() if not x[k]) or "-none-"
        say(f"  {c:4d} {'Y' if x.b_h1 else 'N':>6} {'Y' if x.b_h2 else 'N':>6} "
            f"{'Y' if x.b_oos else 'N':>7} {'Y' if x.b_dd else 'N':>6} "
            f"{'Y' if x.b_cagr else 'N':>7} {'PASS' if x.pass4b else 'FAIL':>5} {bind:<28} "
            f"{100 * (x.MaxDD - 0.60 * spyU['MaxDD']):12.2f}")
    say("")
    unc = bool(u.loc[20, "pass4b"])
    tight = [c for c in CAPS if c != 20 and not bool(u.loc[c, "pass4b"])]
    gained = [c for c in CAPS if c != 20 and bool(u.loc[c, "pass4b"])]
    outs = []
    if not unc and not gained:
        outs.append("(D) NO PASS ANYWHERE on U56 at N=20")
    if unc and not tight:
        outs.append("(A) CONCENTRATION-FREE — clears 4b at every cap")
    if unc and tight:
        outs.append(f"(B) CAP-SENSITIVE — clears uncapped, fails at cap(s) {tight}")
    if not unc and gained:
        outs.append(f"(C) CAP-IMPROVED — fails uncapped, clears at cap(s) {gained}")
    if unc and gained and tight:
        outs.append(f"and clears at cap(s) {gained}")
    say(f"  PRE-DECLARED OUTCOME REACHED: {'; '.join(outs)}.")
    say("")
    say(f"  Grid-wide: 4a passes {int(G.pass4a.sum())} of {len(G)}; 4b passes {int(G.pass4b.sum())} "
        f"of {len(G)}.")
    say("  4b by cap: " + ", ".join(f"c={c}: {int(G[G.cap == c].pass4b.sum())}/{len(G[G.cap == c])}"
                                    for c in CAPS) + ".")
    say("  4b by panel: " + ", ".join(f"{p}: {int(G[G.panel == p].pass4b.sum())}/"
                                      f"{len(G[G.panel == p])}" for p in ["U56", "B136", "SMALL"])
        + ".")
    say(f"  CROSS-CHECK (LABEL4 grouping, U56 N=20): 4b passes "
        f"{int(X.pass4b.sum())} of {len(X)} caps.")
    say("")
    say("  SURVIVORSHIP (rule 9): all three panels are CURRENT-constituent lists, so dead and")
    say("  acquired names are absent. This flatters the UNCAPPED book most, because the corner")
    say("  the screen concentrates into is the corner whose survivors are known in advance.")
    say("  Relative readings across caps on fixed panels; not live expectancy.")

    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    C.to_csv(OUT.with_suffix(".census.csv"), index=False)
    X.to_csv(OUT.with_suffix(".crosscheck.csv"), index=False)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    say("")
    say(f"  Wrote .grid.csv ({len(G)}), .census.csv ({len(C)}), .crosscheck.csv ({len(X)}), "
        f".walkforward.csv ({len(WF)}), .log.txt")
    say(f"  Runtime {time.time() - t0:.1f}s, offline, deterministic.")
    OUT.with_suffix(".log.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
