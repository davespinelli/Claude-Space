#!/usr/bin/env python3
"""
Idea 1293 (lane cloud, 2026-09-18) — does the CERTIFIED U56 g=0.65 BOOK survive 25 and 50 bps
COSTS, and at what cost rung does its joint 4b margin go negative?

THE PREMISE.  PROTOCOL rule 2 fixes costs at 10 bps per unit turnover and EVERY margin in the
standing KEEP-4b candidate (U56 / N=20 / H=126 / gross 0.65 / weekly, ideas 1290 / 1292 / 1295)
is quoted there.  But 4b's CAGR floor is ONE-SIDED: the book pays turnover and SPY, the bar,
pays none.  The book turns ~2.4x/yr at unit gross, so a 25 or 50 bps account gives up roughly
0.6 / 1.2 pp/yr of CAGR that the bar never gives up.  If the 4b pass dies between 10 and 25 bps
it is a PROTOCOL ARTEFACT, not a book, and nobody should fund it at a retail commission.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHOR.  (U56, N=20, gross 0.65, 10 bps, Fri decision, t+1) must reproduce the
      certified candidate: full 13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833 (idea 1290).
      Reported as a CHECK, not a result; a failure to reproduce invalidates everything below.
  (2) THE GRID.  COST {0, 10, 25, 50} bps x GROSS {0.55..0.85, step 0.05} on three panels
      = 4 x 7 x 3 = 84 cells, EVERY ONE PUBLISHED, with BOTH KEEP paths (rule 4) and both
      4b margins on FIVE windows (FULL, H1, H2, IS, OOS).
  (3) THE JOINT MARGIN, as idea 1290 defined it:
          dd_margin   = 100 * ( MaxDD(book) - 0.60 * MaxDD(SPY) )       [4b's cap]
          cagr_margin = 100 * ( CAGR(book)  - 0.70 * CAGR(SPY)  )       [4b's floor]
          J(w, c, g)  = min(dd_margin, cagr_margin) in pp on window w.
      J > 0 iff both non-Sharpe legs of 4b clear.  SPY pays NO cost at any rung — that
      asymmetry IS the object under test and is not repaired here.
  (4) THE BREAKEVEN.  A cost rung is an EXACT affine shift of the return series
      (r(c) = r_0 - u*c/1e4 row-wise, idea 611), so J(c) is read on a FINE 0..100 bps sweep
      in 1 bp steps at no extra simulation.  This is a DERIVED READING of the same two dials,
      not a third dial.  Published: c*_cell (the cost at which a cell's J goes negative) and
      c*_panel = max over the gross rungs of c*_cell (the best any sizing can do).
  (5) 4a IS COST-MATCHED.  The live RULES v2 baseline is re-run at EVERY cost rung, so the
      4a verdict compares two books paying the same commission.  4b's SPY bar is not.
  (6) RULE 8.  Per (panel, cost rung), gross chosen on warm-up..2016-12-31 ONLY by the chooser
      declared below; 2017-2026 read ONCE.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) SURVIVES — the certified g=0.65 cell clears 4b at 25 AND 50 bps on U56.  The 10 bps
        quote is not doing the work; the book is a book.
    (B) PROTOCOL ARTEFACT — it clears at 10 bps and fails at 25 bps.  The committed pass is a
        property of PROTOCOL rule 2's rung.
    (C) RESIZABLE — the g=0.65 cell fails at some rung but ANOTHER gross in {0.55..0.85}
        clears 4b there.  Cost is then a sizing problem, not a kill.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  COST   {0, 10, 25, 50} bps     4 rungs (10 = PROTOCOL's; the record's committed ladder)
  GROSS  {0.55 .. 0.85} step .05 7 rungs (0.65 = the certified cell, 0.75 = the old incumbent)
  PANEL  {U56, B136, SMALL}      3 values (rule 9 caveat below) — a REPLICATION axis, reported
                                 separately per panel, not a tuned parameter.

FROZEN at the certified book's construction, NOT dials: N = 20 names, H = 126-row min hold,
weekly cadence deciding on the last trading row of the week (Fri phase) applying at t+1
(rule 2), 3-leg composite (21/252, 0/126, 0/63) equal-ranked, above-200d and vol20 < 0.60
eligibility, 260-row warm-up, first-wins stable tie-break, equal weights, cash at 0%.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  Within each (panel,
cost rung), on the IS window (warm-up .. 2016-12-31) ONLY, pick the gross maximising J(IS, c, g);
ties to the LOWER gross.  This is idea 1290's chooser, unchanged, applied at each rung.  Two
declared comparands, both also IS-only: the frozen certified g = 0.65, and the old incumbent
g = 0.75.  Then 2017-2026 is read ONCE.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen.  Delisted, acquired and bankrupt names are absent
from all three, which flatters every momentum book here and the drawdown leg specifically.
Tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped from SMALL before anything
is built.  Nothing here estimates live expectancy; every reading is a within-grid difference on
fixed panels and identical dates.

PROTOCOL: rule 2 execution (rule 2's 10 bps is the ANCHOR rung and the other rungs are the
object under test, declared as such); rule 4 both KEEP paths at every cell; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-the-CERTIFIED-U56-g0.65-BOOK-survive-25-and-50-bps-COSTS_cloud.py
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

OUT = Path(str(Path(__file__))[:-3])   # strip ".py" by length; with_suffix() would
                                      # eat the "0.65" in the filename
WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_PHASE, A_DELAY = 20, 126, 4, 1        # frozen: top-20, 126-row hold, Fri, t+1
COSTS = [0.0, 10.0, 25.0, 50.0]                   # dial 1
GROSSES = [round(0.55 + 0.05 * i, 2) for i in range(7)]   # dial 2
CERT_G, OLD_G, REF_COST = 0.65, 0.75, 10.0
FINE = np.arange(0.0, 100.5, 1.0)                 # derived breakeven sweep (affine, no new dial)
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


def build(pan, N=A_N, d=A_DELAY):
    """The certified book's min-hold top-N frame at UNIT gross (gross-independent)."""
    dec = pan.dec
    T, M = pan.rets.shape
    K = len(pan.iinv)
    app = dec + d
    keep = app < T
    dec, app = dec[keep], app[keep]
    W = np.zeros((T, M))
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
        if len(sel):
            stop = app[i + 1] if i + 1 < len(app) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, app


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
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=~oos, OOS=oos)


def margins(r, spy, m):
    R, S = mt(r[m]), mt(spy[m])
    dd = 100.0 * (R["MaxDD"] - 0.60 * S["MaxDD"])
    cg = 100.0 * (R["CAGR"] - 0.70 * S["CAGR"])
    return dd, cg, min(dd, cg), R, S


def legs(r, spy, live, W):
    R, S, L = mt(r), mt(spy), mt(live)
    r1, r2 = mt(r[W["H1"]]), mt(r[W["H2"]])
    s1, s2 = mt(spy[W["H1"]]), mt(spy[W["H2"]])
    l1, l2 = mt(live[W["H1"]]), mt(live[W["H2"]])
    Ro, So = mt(r[W["OOS"]]), mt(spy[W["OOS"]])
    a = dict(a_h1=r1["Sharpe"] > l1["Sharpe"], a_h2=r2["Sharpe"] > l2["Sharpe"],
             a_dd=R["MaxDD"] >= L["MaxDD"])
    b = dict(b_h1=r1["Sharpe"] > s1["Sharpe"], b_h2=r2["Sharpe"] > s2["Sharpe"],
             b_oos=Ro["Sharpe"] > So["Sharpe"], b_dd=R["MaxDD"] >= 0.60 * S["MaxDD"],
             b_cagr=R["CAGR"] >= 0.70 * S["CAGR"])
    return dict(CAGR=R["CAGR"], Sharpe=R["Sharpe"], MaxDD=R["MaxDD"], H1=r1["Sharpe"],
                H2=r2["Sharpe"], OOS_CAGR=Ro["CAGR"], OOS_Sharpe=Ro["Sharpe"],
                OOS_MaxDD=Ro["MaxDD"], pass4a=all(a.values()), pass4b=all(b.values()), **a, **b)


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
    say("IDEA 1293 (lane cloud, 2026-09-18) — does the CERTIFIED U56 g=0.65 BOOK survive 25 and")
    say("50 bps COSTS, and at what cost rung does its joint 4b margin go negative?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): COST {COSTS} bps x GROSS {GROSSES[0]}..{GROSSES[-1]} step 0.05")
    say(f"                     ({len(COSTS)} x {len(GROSSES)} rungs) on 3 panels = "
        f"{len(COSTS) * len(GROSSES) * 3} cells, all published.")
    say(f"  FROZEN: N={A_N}, H={A_H}, weekly (Fri decision), t+1 application, above-200d &")
    say("          vol20<0.60, equal weights, 260-row warm-up, cash at 0%.")
    say("  J(w,c,g) := min(dd_margin, cagr_margin) in pp.  SPY, the 4b bar, pays NO cost at any")
    say("  rung — that one-sidedness IS the object under test.  RULES v2 (the 4a bar) IS")
    say("  cost-matched at every rung.")
    say("  OUTCOMES: (A) SURVIVES 25 and 50  (B) PROTOCOL ARTEFACT (dies 10 -> 25)  (C) RESIZABLE.")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY = benchmark only.")
    say("")

    # ---------------------------------------------------------- benchmarks
    say("=" * 100)
    say("ARM A — BENCHMARKS (post-warm-up).  SPY buy & hold is cost-free by construction;")
    say("RULES v2, the 4a bar, is re-run at EVERY cost rung.")
    say("=" * 100)
    say("")
    B = {}
    say(f"  {'panel':6} {'series':26} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
        f"{'OOS CAGR':>9} {'OOS Sh':>8}")
    for pan in panels:
        spy = pan.spy[WARMUP:]
        idx = pan.idx[WARMUP:]
        W = windows(idx)
        lv = {}
        for c in COSTS:
            lv[c] = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=c,
                             freq="W")["returns"].values[WARMUP:]
        B[pan.name] = dict(spy=spy, live=lv, idx=idx, W=W)
        m, mo = mt(spy), mt(spy[W["OOS"]])
        say(f"  {pan.name:6} {'SPY (buy & hold, 0 bps)':26} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} "
            f"{m['MaxDD']:8.2%} {mt(spy[W['H1']])['Sharpe']:7.4f} {mt(spy[W['H2']])['Sharpe']:7.4f} "
            f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f}")
        for c in COSTS:
            s = lv[c]
            m, mo = mt(s), mt(s[W["OOS"]])
            say(f"  {pan.name:6} {f'RULES v2 @ {c:.0f} bps':26} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} "
                f"{m['MaxDD']:8.2%} {mt(s[W['H1']])['Sharpe']:7.4f} {mt(s[W['H2']])['Sharpe']:7.4f} "
                f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f}")
    say("")

    # ---------------------------------------------------------- the grid
    rows = []
    RAW = {}
    for pan in panels:
        spy, idx, W = B[pan.name]["spy"], B[pan.name]["idx"], B[pan.name]["W"]
        W1, app = build(pan)
        for g in GROSSES:
            gr, tu = nrun(pan, W1 * g, app)
            RAW[(pan.name, g)] = (gr[WARMUP:], tu[WARMUP:])
            for c in COSTS:
                r = at_cost(gr, tu, c)[WARMUP:]
                rec = legs(r, spy, B[pan.name]["live"][c], W)
                for wn, m in W.items():
                    dd, cg, j, R, S = margins(r, spy, m)
                    rec[f"dd_{wn}"], rec[f"cg_{wn}"], rec[f"J_{wn}"] = dd, cg, j
                    rec[f"Sharpe_{wn}"], rec[f"CAGR_{wn}"], rec[f"MaxDD_{wn}"] = (
                        R["Sharpe"], R["CAGR"], R["MaxDD"])
                rec.update(panel=pan.name, gross=g, cost_bps=c,
                           turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)),
                           cost_drag_pp=float(100.0 * tu[WARMUP:].sum() * c / 1e4
                                              / (len(r) / 252.0)))
                rows.append(rec)
    G = pd.DataFrame(rows)

    # ---------------------------------------------------------- anchor
    say("=" * 100)
    say("ARM B — THE ANCHOR CHECK: (U56, N=20, gross 0.65, 10 bps, Fri, t+1) against the")
    say("certified candidate 13.66% / 1.1526 / -16.73%, OOS 14.95% / 1.1833 (idea 1290)")
    say("=" * 100)
    say("")
    a = G[(G.panel == "U56") & (G.gross == CERT_G) & (G.cost_bps == REF_COST)].iloc[0]
    tgt = dict(CAGR=0.1366, Sharpe=1.1526, MaxDD=-0.1673, OOS_CAGR=0.1495, OOS_Sharpe=1.1833)
    say(f"  {'stat':10} {'this run':>12} {'committed':>12} {'diff':>12}")
    ok = True
    for k, v in tgt.items():
        say(f"  {k:10} {a[k]:12.4f} {v:12.4f} {a[k] - v:12.2e}")
        ok &= abs(a[k] - v) < 5e-4
    say("")
    say(f"  ANCHOR REPRODUCES: {'YES' if ok else 'NO'} (all five within 5e-4). "
        f"4b at the anchor: {'PASS' if a.pass4b else 'FAIL'}; 4a: {'PASS' if a.pass4a else 'FAIL'}.")
    if not ok:
        say("  *** The anchor does NOT reproduce; no verdict below may be taken on these numbers.")
    say("")

    # ---------------------------------------------------------- grid table
    say("=" * 100)
    say("ARM C — THE COST x GROSS GRID, every cell, every panel (84 cells; .grid.csv carries")
    say("all five windows).  dd/cg/J in pp on the FULL sample.")
    say("=" * 100)
    say("")
    for pan in panels:
        say(f"  --- {pan.name} " + "-" * 82)
        say(f"  {'cost':>5} {'gross':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'turn/yr':>8} "
            f"{'drag pp':>8} {'ddFULL':>8} {'cgFULL':>8} {'J_FULL':>8} {'J_IS':>8} {'J_OOS':>8} "
            f"{'4a':>3} {'4b':>3}")
        sub = G[G.panel == pan.name].sort_values(["cost_bps", "gross"])
        for _, x in sub.iterrows():
            mark = ""
            if x.gross == CERT_G:
                mark = " <-certified" if x.cost_bps == REF_COST else " <-cert g"
            say(f"  {x.cost_bps:5.0f} {x.gross:6.2f} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
                f"{x.turnover_yr:8.2f} {x.cost_drag_pp:8.2f} {x.dd_FULL:8.2f} {x.cg_FULL:8.2f} "
                f"{x.J_FULL:8.2f} {x.J_IS:8.2f} {x.J_OOS:8.2f} "
                f"{'Y' if x.pass4a else '.':>3} {'Y' if x.pass4b else '.':>3}{mark}")
        say("")
    say(f"  GRID-WIDE: 4b passes {int(G.pass4b.sum())} of {len(G)} cells; "
        f"4a passes {int(G.pass4a.sum())} of {len(G)}.")
    for p in ["U56", "B136", "SMALL"]:
        s = G[G.panel == p]
        say(f"    {p:6} 4b {int(s.pass4b.sum()):2d}/{len(s)}  by cost rung: " + ", ".join(
            f"{c:.0f}bps {int(s[s.cost_bps == c].pass4b.sum())}/{len(GROSSES)}" for c in COSTS))
    say("")

    # ---------------------------------------------------------- which leg binds
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
    say("  Same census restricted to the cost rungs ABOVE PROTOCOL's 10 bps (25 and 50):")
    F2 = G[(~G.pass4b) & (G.cost_bps > REF_COST)]
    for k, v in nm.items():
        f = ~F2[k]
        sole = f & (F2[[c for c in nm if c != k]].all(axis=1))
        say(f"  {v:12} {int(f.sum()):7d} {f.mean():8.4f} {int(sole.sum()):12d}")
    say("")

    # ---------------------------------------------------------- the certified cell
    say("=" * 100)
    say("ARM D — THE CERTIFIED CELL ITSELF (U56 / g=0.65) ACROSS THE COST LADDER")
    say("=" * 100)
    say("")
    say(f"  {'cost':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'drag pp':>8} {'dd marg':>8} "
        f"{'cg marg':>8} {'J_FULL':>8} {'OOS CAGR':>9} {'OOS Sh':>8} {'4b':>5} {'4a':>4}")
    for _, x in G[(G.panel == "U56") & (G.gross == CERT_G)].sort_values("cost_bps").iterrows():
        say(f"  {x.cost_bps:5.0f} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
            f"{x.cost_drag_pp:8.2f} {x.dd_FULL:8.2f} {x.cg_FULL:8.2f} {x.J_FULL:8.2f} "
            f"{x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} {'PASS' if x.pass4b else 'FAIL':>5} "
            f"{'PASS' if x.pass4a else 'FAIL':>4}")
    say("")

    # ---------------------------------------------------------- breakeven
    say("=" * 100)
    say("ARM E — THE BREAKEVEN COST.  A cost rung is an EXACT affine shift of the return series,")
    say("so J(c) is read on a 1-bp sweep 0..100 with no extra simulation.  c* = the largest cost")
    say("at which a cell still clears BOTH non-Sharpe 4b legs on the FULL sample (J >= 0);")
    say("'>100' means it never fails inside the sweep, '-' means it fails at 0 bps already.")
    say("=" * 100)
    say("")
    BE = []
    for pan in panels:
        spy, W = B[pan.name]["spy"], B[pan.name]["W"]
        for g in GROSSES:
            gr, tu = RAW[(pan.name, g)]
            cs = {}
            for wn in ("FULL", "IS", "OOS"):
                m = W[wn]
                good = [c for c in FINE if margins(at_cost(gr, tu, c), spy, m)[2] >= 0]
                cs[wn] = (max(good) if good else np.nan)
            BE.append(dict(panel=pan.name, gross=g, cstar_FULL=cs["FULL"], cstar_IS=cs["IS"],
                           cstar_OOS=cs["OOS"]))
    BEdf = pd.DataFrame(BE)

    def fmt(v):
        if not np.isfinite(v):
            return "     -"
        return "  >100" if v >= 100 else f"{v:6.0f}"

    for pan in panels:
        sub = BEdf[BEdf.panel == pan.name]
        say(f"  --- {pan.name} " + "-" * 60)
        say(f"  {'gross':>6} {'c* FULL':>8} {'c* IS':>8} {'c* OOS':>8}")
        for _, x in sub.iterrows():
            mk = " <-certified g" if x.gross == CERT_G else (" <-old incumbent" if x.gross == OLD_G else "")
            say(f"  {x.gross:6.2f} {fmt(x.cstar_FULL):>8} {fmt(x.cstar_IS):>8} "
                f"{fmt(x.cstar_OOS):>8}{mk}")
        best = sub.cstar_FULL.max()
        say(f"  PANEL BEST (max over gross) c*_FULL = {fmt(best)} bps"
            + (f" at gross {sub.loc[sub.cstar_FULL.idxmax(), 'gross']:.2f}"
               if np.isfinite(best) else " — no gross rung clears both legs at any cost"))
        say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM F — RULE 8 WALK-FORWARD: within each (panel, cost rung), gross chosen on")
    say("warm-up..2016 ONLY by argmax_g J(IS,c,g) (ties to the LOWER gross); 2017-2026 read ONCE.")
    say("=" * 100)
    say("")
    WF = []
    for pan in panels:
        W = B[pan.name]["W"]
        bs = mt(B[pan.name]["spy"][W["OOS"]])
        for c in COSTS:
            sub = G[(G.panel == pan.name) & (G.cost_bps == c)].sort_values("gross").reset_index(drop=True)
            gJ = float(sub.gross.values[int(np.nanargmax(sub["J_IS"].values))])
            bl = mt(B[pan.name]["live"][c][W["OOS"]])
            for tag, g in (("JOINT-MARGIN (declared)", gJ), ("FROZEN certified g=0.65", CERT_G),
                           ("FROZEN old incumbent g=0.75", OLD_G)):
                x = sub[sub.gross == g].iloc[0]
                WF.append(dict(panel=pan.name, cost_bps=c, chooser=tag, gross=g,
                               OOS_CAGR=x.OOS_CAGR, OOS_Sharpe=x.OOS_Sharpe,
                               OOS_MaxDD=x.OOS_MaxDD, J_IS=x.J_IS, J_OOS=x.J_OOS,
                               pass4b_full=bool(x.pass4b), pass4a_full=bool(x.pass4a),
                               beats_SPY_OOS=bool(x.OOS_Sharpe > bs["Sharpe"]),
                               spy_OOS_Sharpe=bs["Sharpe"], spy_OOS_CAGR=bs["CAGR"],
                               spy_OOS_MaxDD=bs["MaxDD"], live_OOS_Sharpe=bl["Sharpe"],
                               live_OOS_CAGR=bl["CAGR"], live_OOS_MaxDD=bl["MaxDD"]))
    W8 = pd.DataFrame(WF)
    say(f"  {'panel':6} {'cost':>5} {'chooser':28} {'g':>5} {'OOS CAGR':>9} {'OOS Sh':>8} "
        f"{'OOS DD':>8} {'J_OOS':>8} {'>SPY?':>6} {'4b full':>8}")
    for _, x in W8.iterrows():
        say(f"  {x.panel:6} {x.cost_bps:5.0f} {x.chooser:28} {x.gross:5.2f} {x.OOS_CAGR:9.2%} "
            f"{x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:8.2%} {x.J_OOS:8.2f} "
            f"{'YES' if x.beats_SPY_OOS else 'no':>6} {'PASS' if x.pass4b_full else 'FAIL':>8}")
    say("")
    say("  The two things a real account is measured against, same OOS window:")
    for pan in panels:
        for c in COSTS:
            x = W8[(W8.panel == pan.name) & (W8.cost_bps == c)].iloc[0]
            say(f"  {pan.name:6} RULES v2 @ {c:4.0f} bps: {x.live_OOS_CAGR:7.2%} / "
                f"{x.live_OOS_Sharpe:7.4f} / {x.live_OOS_MaxDD:7.2%}"
                + (f"   |  SPY (0 bps): {x.spy_OOS_CAGR:7.2%} / {x.spy_OOS_Sharpe:7.4f} / "
                   f"{x.spy_OOS_MaxDD:7.2%}" if c == COSTS[0] else ""))
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM G — THE ANSWER")
    say("=" * 100)
    say("")
    u = G[(G.panel == "U56") & (G.gross == CERT_G)].set_index("cost_bps")
    p10, p25, p50 = (bool(u.loc[c, "pass4b"]) for c in (10.0, 25.0, 50.0))
    resize25 = G[(G.panel == "U56") & (G.cost_bps == 25.0) & G.pass4b]
    resize50 = G[(G.panel == "U56") & (G.cost_bps == 50.0) & G.pass4b]
    if p25 and p50:
        outcome = ("(A) SURVIVES — the certified U56 g=0.65 cell clears 4b at 25 AND 50 bps; the "
                   "10 bps quote is not doing the work")
    elif not p25 and len(resize25) == 0:
        outcome = ("(B) PROTOCOL ARTEFACT — the certified cell fails 4b at 25 bps and NO gross in "
                   "{0.55..0.85} clears there; the committed pass is a property of rule 2's rung")
    else:
        outcome = ("(C) RESIZABLE — the certified cell fails 4b at some rung above 10 bps but "
                   "another gross clears 4b there; cost is a sizing problem, not a kill")
    say(f"  OUTCOME: {outcome}.")
    say("")
    say(f"    U56 g=0.65:  10 bps 4b {'PASS' if p10 else 'FAIL'}   "
        f"25 bps 4b {'PASS' if p25 else 'FAIL'}   50 bps 4b {'PASS' if p50 else 'FAIL'}")
    say(f"    U56 cells clearing 4b at 25 bps: {len(resize25)} of {len(GROSSES)}"
        + (" (" + ", ".join(f"g={r.gross:.2f}" for _, r in resize25.iterrows()) + ")" if len(resize25) else ""))
    say(f"    U56 cells clearing 4b at 50 bps: {len(resize50)} of {len(GROSSES)}"
        + (" (" + ", ".join(f"g={r.gross:.2f}" for _, r in resize50.iterrows()) + ")" if len(resize50) else ""))
    bu = BEdf[BEdf.panel == "U56"]
    say(f"    U56 breakeven c* at the certified gross: "
        f"{fmt(float(bu[bu.gross == CERT_G].cstar_FULL.iloc[0])).strip()} bps (FULL sample); "
        f"panel best {fmt(bu.cstar_FULL.max()).strip()} bps.")
    say("")
    cand = W8[W8.pass4b_full & W8.beats_SPY_OOS & (W8.chooser == "JOINT-MARGIN (declared)")
              & (W8.cost_bps > REF_COST)]
    if len(cand):
        say("  KEEP-4b CANDIDATE(S) ABOVE PROTOCOL's rung, from the declared chooser: " + ", ".join(
            f"{r.panel} @{r.cost_bps:.0f}bps g={r.gross:.2f} (OOS {r.OOS_CAGR:.2%} / "
            f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%})" for _, r in cand.iterrows()))
    else:
        say("  NO KEEP-4b CANDIDATE above 10 bps: the declared chooser's pick clears full-sample")
        say("  4b and beats SPY out-of-sample on ZERO (panel, cost rung) cells with cost > 10 bps.")
    say("")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents; delisted and")
    say("  bankrupt names are absent, which flatters the drawdown leg specifically. Every number")
    say("  here is a within-grid difference on fixed panels and identical dates.")
    say("")
    say(f"  ({time.time() - t0:.1f}s)")

    G.to_csv(Path(str(OUT) + ".grid.csv"), index=False)
    BEdf.to_csv(Path(str(OUT) + ".breakeven.csv"), index=False)
    W8.to_csv(Path(str(OUT) + ".walkforward.csv"), index=False)
    Path(str(OUT) + ".log.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nwrote {OUT.name}.grid.csv / .breakeven.csv / .walkforward.csv / .log.txt")


if __name__ == "__main__":
    main()
