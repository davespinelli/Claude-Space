#!/usr/bin/env python3
"""
Idea 1288 (lane cloud, 2026-09-18) — does the 2026-09-04 KEEP-4b BOOK EXIST AT ALL on the
SMALL-CAP PANEL?

THE PREMISE.  The standing KEEP-4b candidate (first KEEP 4b, 2026-09-04: top-N equal weight,
NO vol scaler, 126-row min hold, weekly, later certified at U56 / N=20 / gross 0.65) was found
on U56 — 56 mega-cap and ETF names.  A rule that only clears 4b on the tape it was found on is
a PANEL FACT and should be written down as one.  A rule that clears 4b on 483 sub-$2B names too
is a MECHANISM.  Nobody has walked the recipe's own two dials on the small panel; the record's
SMALL readings are all at N=20 (idea 1295: SMALL 0 of 45 at every sector cap and gross).  This
run walks N as well, so the question is asked of the RECIPE and not of one cell of it.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHOR, reported as a CHECK and not as a result.  (U56, N=20, gross 0.65, 10 bps,
      Fri decision, t+1, H=126) must reproduce the certified uncapped candidate published by
      idea 1293: full 13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833.  A failure to reproduce
      invalidates every panel comparison below.
  (2) THE GRID.  N {5,10,15,20,25,30} x GROSS {0.55..0.85 step 0.05} on three panels
      = 6 x 7 x 3 = 126 cells, EVERY ONE PUBLISHED (.grid.csv), with BOTH KEEP paths (rule 4)
      and both non-Sharpe 4b margins on FIVE windows (FULL, H1, H2, IS, OOS).
  (3) THE JOINT MARGIN, idea 1290's definition, unchanged:
          dd_margin   = 100 * ( MaxDD(book) - 0.60 * MaxDD(SPY) )     [4b's cap]
          cagr_margin = 100 * ( CAGR(book)  - 0.70 * CAGR(SPY)  )     [4b's floor]
          J(w, N, g)  = min(dd_margin, cagr_margin) in pp on window w.
      J > 0 iff both non-Sharpe legs of 4b clear.  The Sharpe legs are reported separately.
  (4) THE BINDING LEG.  For every 4b failure, which of the five legs binds, and on how many
      cells each leg is the SOLE binder.  This is what distinguishes "the small panel cannot
      carry the recipe" from "the small panel cannot carry THIS SIZE of the recipe".
  (5) RULE 8.  Per panel, BOTH dials chosen on warm-up..2016-12-31 ONLY by the chooser declared
      below; 2017-2026 read ONCE, after the in-sample pick is fixed.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) MECHANISM — SMALL clears 4b somewhere on the grid AND at its own rule-8 pick.  The
        2026-09-04 recipe then survives a panel it was not found on.
    (B) PANEL FACT — SMALL clears 4b at 0 of 42 cells while U56 clears at >= 1.  The memo must
        then say the incumbent is a U56 fact, and the binding leg in (4) says which one.
    (C) RESIZABLE — SMALL clears 4b only at (N, g) far from the certified U56 cell, i.e. the
        mechanism survives but the SIZE does not transfer.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  N      {5, 10, 15, 20, 25, 30}        6 rungs (20 = the certified cell; the record's ladder)
  GROSS  {0.55 .. 0.85} step 0.05       7 rungs (0.65 = certified, 0.75 = the old incumbent)
  PANEL  {U56, B136, SMALL}             3 values — a REPLICATION axis, reported separately per
                                        panel, never pooled and never tuned over.

FROZEN at the 2026-09-04 book's construction, NOT dials: H = 126-row min hold, weekly cadence
deciding on the last trading row of the week (Fri phase) applying at t+1 (rule 2), 10 bps per
unit turnover (rule 2), 3-leg composite (21/252, 0/126, 0/63) equal-ranked and halved below the
200d average, above-200d AND vol20 < 0.60 eligibility, 260-row warm-up, first-wins stable
tie-break, equal weights, cash at 0%.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  Within each panel, on
the IS window (warm-up .. 2016-12-31) ONLY, pick the (N, gross) maximising J(IS); ties to the
LOWER gross, then the LOWER N.  This is idea 1290's chooser (IS Sharpe cannot size a book),
extended to the second dial by the same tie rule.  Declared comparands, also IS-only: the
certified cell (N=20, g=0.65) and the old incumbent (N=20, g=0.75).  Then 2017-2026 is read ONCE.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
CURRENT constituent list of a sub-$2B screen, so its delisted, acquired and bankrupt names are
absent.  That bias is WORST on the small panel — small caps die far more often than mega caps —
so SMALL's numbers here are an UPPER bound on what the recipe would have earned there, and a
KILL on SMALL is therefore the stronger reading, not the weaker one.  Tickers with
max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is built.  Nothing here
estimates live expectancy; every reading is a within-grid difference on fixed panels and dates.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-the-2026-09-04-KEEP-4b-BOOK-EXIST-AT-ALL-on-the-SMALL-CAP-PANEL_cloud.py
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

OUT = Path(str(Path(__file__))[:-3])
WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
A_H, A_PHASE, A_DELAY, COST = 126, 4, 1, 10.0     # frozen
NS = [5, 10, 15, 20, 25, 30]                      # dial 1
GROSSES = [round(0.55 + 0.05 * i, 2) for i in range(7)]   # dial 2
CERT_N, CERT_G, OLD_G = 20, 0.65, 0.75
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
REF = dict(CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673, OOS_CAGR=0.1495, OOS_Sharpe=1.1833)

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
        self.dec = decision_rows(px.index, A_PHASE)


def build(pan, N, d=A_DELAY):
    """The 2026-09-04 book's min-hold top-N frame at UNIT gross (gross-independent)."""
    dec = pan.dec
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keep = app < T
    dec, app = dec[keep], app[keep]
    W = np.zeros((T, M))
    nsel = np.zeros(T)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(app):
        ts = dec[i]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < A_H] if len(held) else held
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
        stop = app[i + 1] if i + 1 < len(app) else T
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
            nsel[t:stop] = len(sel)
    return W, app, nsel


def nrun(pan, Wt, app):
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
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=~oos, OOS=oos)


def J(r, spy, m):
    R, S = mt(r[m]), mt(spy[m])
    dd = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"])
    cg = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    return dd, cg, min(dd, cg), R, S


def cell(r, spy, live, W):
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]])
    s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ro, So = mt(r[W["OOS"]]), mt(spy[W["OOS"]])
    Ri = mt(r[W["IS"]])
    a = dict(a_h1=bool(r1["Sharpe"] > l1["Sharpe"]), a_h2=bool(r2["Sharpe"] > l2["Sharpe"]),
             a_dd=bool(R["MaxDD"] >= L["MaxDD"]))
    b = dict(b_h1=bool(r1["Sharpe"] > s1["Sharpe"]), b_h2=bool(r2["Sharpe"] > s2["Sharpe"]),
             b_oos=bool(Ro["Sharpe"] > So["Sharpe"]),
             b_dd=bool(R["MaxDD"] >= 0.60 * S["MaxDD"]),
             b_cagr=bool(R["CAGR"] >= 0.70 * S["CAGR"]))
    dd_f, cg_f, j_f, _, _ = J(r, spy, W["FULL"])
    dd_i, cg_i, j_i, _, _ = J(r, spy, W["IS"])
    dd_o, cg_o, j_o, _, _ = J(r, spy, W["OOS"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], IS_CAGR=Ri["CAGR"], IS_Sharpe=Ri["Sharpe"],
                OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"], OOS_MaxDD=Ro["MaxDD"],
                dd_margin=dd_f, cagr_margin=cg_f, J_FULL=j_f, J_IS=j_i, J_OOS=j_o,
                dd_margin_OOS=dd_o, cagr_margin_OOS=cg_o,
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
    say("=" * 104)
    say("IDEA 1288 (lane cloud, 2026-09-18) — does the 2026-09-04 KEEP-4b BOOK EXIST AT ALL on")
    say("the SMALL-CAP PANEL?")
    say("=" * 104)
    say("")
    say(f"  DIALS (2, rule 4): N {NS} x GROSS {GROSSES[0]}..{GROSSES[-1]} step 0.05")
    say(f"                     ({len(NS)} x {len(GROSSES)} rungs) on 3 panels = "
        f"{len(NS) * len(GROSSES) * 3} cells, ALL published.")
    say(f"  FROZEN: H={A_H}-row min hold, weekly (Fri decision), t+1 application, {COST:.0f} bps,")
    say("          above-200d & vol20<0.60, equal weights, 260-row warm-up, cash at 0%.")
    say("  J(w,N,g) := min(dd_margin, cagr_margin) in pp; > 0 iff both non-Sharpe 4b legs clear.")
    say("  OUTCOMES: (A) MECHANISM  (B) PANEL FACT  (C) RESIZABLE.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0).")
    say("          SPY is the 4b bar on every panel and is never a constituent.")
    say("")

    # ---------------------------------------------------------- benchmarks
    say("=" * 104)
    say("ARM A — BENCHMARKS (post-warm-up, each on its own panel's trading days).")
    say("=" * 104)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':22} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8}")
    for pan in panels:
        spy = pan.spy[WARMUP:]
        idx = pan.idx[WARMUP:]
        W = windows(idx)
        live = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                        freq="W")["returns"].values[WARMUP:]
        B[pan.name] = dict(spy=spy, live=live, idx=idx, W=W)
        for lab, s in (("SPY (buy & hold)", spy), ("RULES v2 (live)", live)):
            m, mo = mt(s), mt(s[W["OOS"]])
            say(f"  {pan.name:6} {lab:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(s[W['H1']])['Sharpe']:7.4f} {mt(s[W['H2']])['Sharpe']:7.4f} "
                f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
        say(f"  {pan.name:6} {'4b bars (full)':22} MaxDD cap {0.60 * mt(spy)['MaxDD']:7.2%}   "
            f"CAGR floor {0.70 * mt(spy)['CAGR']:6.2%}   "
            f"[OOS cap {0.60 * mt(spy[W['OOS']])['MaxDD']:7.2%}, "
            f"floor {0.70 * mt(spy[W['OOS']])['CAGR']:6.2%}]")
    say("")

    # ---------------------------------------------------------- the grid
    rows = []
    for pan in panels:
        spy, idx, W, live = (B[pan.name][k] for k in ("spy", "idx", "W", "live"))
        for N in NS:
            W1, app, nsel = build(pan, N)
            names = float(np.mean(nsel[WARMUP:][nsel[WARMUP:] > 0])) if (nsel[WARMUP:] > 0).any() else 0.0
            for g in GROSSES:
                gr, turn = nrun(pan, W1 * g, app)
                r = (gr - turn * COST / 1e4)[WARMUP:]
                d = cell(r, spy, live, W)
                d.update(panel=pan.name, N=N, gross=g, names=names,
                         turns_yr=float(turn[WARMUP:].sum() / (len(r) / 252.0)))
                rows.append(d)
    G = pd.DataFrame(rows)
    cols = (["panel", "N", "gross", "names", "turns_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "IS_CAGR", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "dd_margin",
             "cagr_margin", "J_FULL", "J_IS", "J_OOS", "dd_margin_OOS", "cagr_margin_OOS",
             "pass4a", "a_h1", "a_h2", "a_dd", "pass4b", "b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"])
    G = G[cols]
    G.to_csv(str(OUT) + ".grid.csv", index=False)

    # ---------------------------------------------------------- anchor check
    say("=" * 104)
    say("ARM B — ANCHOR CHECK (not a result).  U56 / N=20 / g=0.65 against idea 1293's committed")
    say("certified uncapped cell.")
    say("=" * 104)
    say("")
    a = G[(G.panel == "U56") & (G.N == CERT_N) & (G.gross == CERT_G)].iloc[0]
    worst = 0.0
    for k, v in REF.items():
        got = float(a[k])
        worst = max(worst, abs(got - v))
        say(f"    {k:11} committed {v:>9.4f}   this run {got:>9.4f}   |d| {abs(got - v):.2e}")
    say(f"    max |d| over the five committed figures: {worst:.2e}  "
        f"({'REPRODUCED' if worst < 5e-3 else 'DOES NOT REPRODUCE — see caveat'})")
    say("")

    # ---------------------------------------------------------- grid, per panel
    say("=" * 104)
    say("ARM C — THE FULL GRID, ALL 126 CELLS.  (4b legs: h1 h2 oos dd cagr; '.' = fail)")
    say("=" * 104)
    for pan in panels:
        sub = G[G.panel == pan.name]
        say("")
        say(f"  --- {pan.name} " + "-" * 92)
        say(f"  {'N':>3} {'g':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOSCAGR':>8} {'OOS Sh':>8} {'J_FULL':>8} {'J_OOS':>8} {'4b legs':>10} {'4b':>4} {'4a':>4}")
        for _, r in sub.iterrows():
            legs = "".join(c if r[f"b_{k}"] else "."
                           for c, k in zip("HhOdc", ["h1", "h2", "oos", "dd", "cagr"]))
            say(f"  {int(r.N):3d} {r.gross:5.2f} {r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} "
                f"{r.H1:7.4f} {r.H2:7.4f} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:8.4f} "
                f"{r.J_FULL:8.2f} {r.J_OOS:8.2f} {legs:>10} "
                f"{'PASS' if r.pass4b else 'FAIL':>4} {'PASS' if r.pass4a else 'FAIL':>4}")
        say(f"  {pan.name}: 4b PASS {int(sub.pass4b.sum())} of {len(sub)};  "
            f"4a PASS {int(sub.pass4a.sum())} of {len(sub)}.")
    say("")

    # ---------------------------------------------------------- binding legs
    say("=" * 104)
    say("ARM D — WHICH LEG BINDS.  Counted over 4b FAILURES only, per panel.")
    say("=" * 104)
    say("")
    LEGN = ["b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"]
    brows = []
    say(f"  {'panel':6} {'fails':>6} " + " ".join(f"{k[2:]:>9}" for k in LEGN) +
        "   " + " ".join(f"{'sole-' + k[2:]:>10}" for k in LEGN))
    for pan in panels:
        f = G[(G.panel == pan.name) & (~G.pass4b)]
        binds = [int((~f[k]).sum()) for k in LEGN]
        sole = [int(((~f[k]) & (f[[x for x in LEGN if x != k]].all(axis=1))).sum()) for k in LEGN]
        brows.append(dict(panel=pan.name, fails=len(f),
                          **{f"binds_{k[2:]}": b for k, b in zip(LEGN, binds)},
                          **{f"sole_{k[2:]}": s for k, s in zip(LEGN, sole)}))
        say(f"  {pan.name:6} {len(f):6d} " + " ".join(f"{b:9d}" for b in binds) +
            "   " + " ".join(f"{s:10d}" for s in sole))
    pd.DataFrame(brows).to_csv(str(OUT) + ".binding.csv", index=False)
    say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 104)
    say("ARM E — RULE 8 WALK-FORWARD.  Both dials chosen on warm-up..2016-12-31 by IS joint")
    say("margin J(IS); ties to the LOWER gross, then the LOWER N.  2017-2026 READ ONCE.")
    say("=" * 104)
    say("")
    wrows = []
    for pan in panels:
        sub = G[G.panel == pan.name].copy()
        sub = sub.sort_values(["J_IS", "gross", "N"], ascending=[False, True, True])
        pick = sub.iloc[0]
        spy, W = B[pan.name]["spy"], B[pan.name]["W"]
        so, s1, s2 = mt(spy[W["OOS"]]), mt(spy[W["H1"]]), mt(spy[W["H2"]])
        lv = B[pan.name]["live"]
        lo = mt(lv[W["OOS"]])
        for lab, r in (("RULE-8 PICK", pick),
                       ("certified N=20 g=0.65", sub[(sub.N == CERT_N) & (sub.gross == CERT_G)].iloc[0]),
                       ("old incumbent N=20 g=0.75", sub[(sub.N == CERT_N) & (sub.gross == OLD_G)].iloc[0])):
            say(f"  {pan.name:6} {lab:26} N={int(r.N):2d} g={r.gross:.2f}  J_IS {r.J_IS:6.2f}  "
                f"FULL {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves "
                f"{r.H1:.4f} / {r.H2:.4f}  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / "
                f"{r.OOS_MaxDD:7.2%}  4b {'PASS' if r.pass4b else 'FAIL'}  "
                f"4a {'PASS' if r.pass4a else 'FAIL'}")
            wrows.append(dict(panel=pan.name, arm=lab, N=int(r.N), gross=r.gross, J_IS=r.J_IS,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                              OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                              OOS_MaxDD=r.OOS_MaxDD, J_OOS=r.J_OOS,
                              pass4a=bool(r.pass4a), pass4b=bool(r.pass4b),
                              SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"],
                              SPY_OOS_MaxDD=so["MaxDD"], SPY_H1=s1["Sharpe"], SPY_H2=s2["Sharpe"],
                              LIVE_OOS_CAGR=lo["CAGR"], LIVE_OOS_Sharpe=lo["Sharpe"],
                              LIVE_OOS_MaxDD=lo["MaxDD"], names=r.names, turns_yr=r.turns_yr))
        say(f"  {pan.name:6} {'SPY (the 4b bar)':26} {'':16}  "
            f"FULL {mt(spy)['CAGR']:7.2%} / {mt(spy)['Sharpe']:.4f} / {mt(spy)['MaxDD']:7.2%}  "
            f"halves {s1['Sharpe']:.4f} / {s2['Sharpe']:.4f}  "
            f"OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        say(f"  {pan.name:6} {'RULES v2 (the 4a bar)':26} {'':16}  "
            f"FULL {mt(lv)['CAGR']:7.2%} / {mt(lv)['Sharpe']:.4f} / {mt(lv)['MaxDD']:7.2%}  "
            f"halves {mt(lv[W['H1']])['Sharpe']:.4f} / {mt(lv[W['H2']])['Sharpe']:.4f}  "
            f"OOS {lo['CAGR']:7.2%} / {lo['Sharpe']:.4f} / {lo['MaxDD']:7.2%}")
        say("")
    pd.DataFrame(wrows).to_csv(str(OUT) + ".walkforward.csv", index=False)

    # ---------------------------------------------------------- verdict
    say("=" * 104)
    say("ARM F — VERDICT against the outcomes declared in the header.")
    say("=" * 104)
    say("")
    sm = G[G.panel == "SMALL"]
    u = G[G.panel == "U56"]
    bb = G[G.panel == "B136"]
    sm_pass, u_pass, b_pass = int(sm.pass4b.sum()), int(u.pass4b.sum()), int(bb.pass4b.sum())
    sm_pick = pd.DataFrame(wrows).query("panel=='SMALL' and arm=='RULE-8 PICK'").iloc[0]
    if sm_pass == 0 and u_pass >= 1:
        v = "(B) PANEL FACT"
    elif sm_pass >= 1 and bool(sm_pick.pass4b):
        v = "(A) MECHANISM"
    elif sm_pass >= 1:
        v = "(C) RESIZABLE"
    else:
        v = "(B) PANEL FACT (and U56 clears nowhere either — see grid)"
    say(f"  4b PASS counts: U56 {u_pass}/42, B136 {b_pass}/42, SMALL {sm_pass}/42.")
    say(f"  4a PASS counts: U56 {int(u.pass4a.sum())}/42, B136 {int(bb.pass4a.sum())}/42, "
        f"SMALL {int(sm.pass4a.sum())}/42.")
    say(f"  SMALL best J_FULL over the whole grid: {sm.J_FULL.max():.2f} pp "
        f"(at N={int(sm.loc[sm.J_FULL.idxmax(), 'N'])}, g={sm.loc[sm.J_FULL.idxmax(), 'gross']:.2f}); "
        f"best full Sharpe {sm.Sharpe.max():.4f} against SMALL-panel SPY "
        f"{mt(B['SMALL']['spy'])['Sharpe']:.4f}.")
    say(f"  SMALL rule-8 pick OOS {sm_pick.OOS_CAGR:.2%} / {sm_pick.OOS_Sharpe:.4f} / "
        f"{sm_pick.OOS_MaxDD:.2%} vs SPY {sm_pick.SPY_OOS_CAGR:.2%} / "
        f"{sm_pick.SPY_OOS_Sharpe:.4f} / {sm_pick.SPY_OOS_MaxDD:.2%}.")
    say("")
    say(f"  VERDICT: {v}")
    say("")
    say("  NOT CLAIMED: that any cell here is a new candidate book (the recipe is the committed")
    say("  2026-09-04 one, re-priced, not re-tuned); that the SMALL panel is untradeable for any")
    say("  other rule; that anything in RULES.md changes (rule 6).")
    say(f"  SURVIVORSHIP (rule 9): current constituents only on all three panels; the bias is")
    say("  worst on SMALL, so SMALL's readings are an UPPER bound and a KILL there is the")
    say("  stronger reading.")
    say("")
    say(f"  elapsed {time.time() - t0:.1f}s")
    Path(str(OUT) + ".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
