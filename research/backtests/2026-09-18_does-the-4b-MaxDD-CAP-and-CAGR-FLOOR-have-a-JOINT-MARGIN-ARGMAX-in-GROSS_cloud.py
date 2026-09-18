#!/usr/bin/env python3
"""
Idea 1290 (lane cloud, 2026-09-18) — does the 4b MaxDD CAP and CAGR FLOOR have a JOINT MARGIN
ARGMAX in GROSS, and is that argmax the SAME IN-SAMPLE AS OUT?

THE PREMISE.  Idea 1292 found the two non-Sharpe legs of PROTOCOL rule 4b move in OPPOSITE
directions in gross: on U56 / N=20 the worst-over-ensemble DD margin runs +6.23 pp at g=0.45
against -2.22 pp at g=0.75, while the CAGR margin runs -1.71 pp against +4.25 pp.  The robust
band is their thin overlap.  That makes gross a SIZING dial with an interior optimum — the gross
maximising the MINIMUM of the two margins — and raises the only question that decides whether
any committed gross in the record means anything: is that argmax a property of the book, or of
the window it was read on?

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.

  (1) THE ANCHOR.  (U56, N=20, gross 0.75, Fri decision, t+1) must reproduce the committed
      incumbent (15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837; idea 1287/1292).  Reported as
      a check, not a result; a failure to reproduce invalidates everything below and says so.
  (2) THE LADDER.  Every gross rung on every panel, with BOTH KEEP paths (rule 4) and both
      4b margins evaluated on FOUR windows (FULL, H1, H2, IS, OOS).  All rows published.
  (3) THE JOINT MARGIN.  J(w, g) := min( dd_margin(w, g), cagr_margin(w, g) ) in pp, where
          dd_margin   = 100 * ( MaxDD(book) - 0.60 * MaxDD(SPY) )     [rule 4b's cap]
          cagr_margin = 100 * ( CAGR(book)  - 0.70 * CAGR(SPY)  )     [rule 4b's floor]
      both measured on window w over the SAME dates.  J > 0 iff both non-Sharpe legs of 4b
      clear on that window.  g*(w) := argmax_g J(w, g).
  (4) THE QUESTION.  g*(IS) vs g*(OOS) vs g*(FULL) on each panel, plus the OOS REGRET of the
      IS choice: J(OOS, g*(IS)) - J(OOS, g*(OOS)), in pp.  A stable argmax is a sizing rule;
      a moving one makes every committed gross a window fact.
  (5) RULE 8.  Gross chosen on warm-up..2016-12-31 ONLY by the chooser declared below,
      2017-2026 read ONCE, OOS CAGR / Sharpe / MaxDD reported against RULES v2 and SPY.

  PRE-DECLARED OUTCOMES, fixed before the run.
    (A) STABLE — g*(IS) and g*(OOS) agree within ONE rung on every panel where J is defined.
        Gross is a sizing rule; the argmax may be published as one.
    (B) MOVES — they differ by more than one rung on at least one such panel.  Every committed
        gross is a window fact and no argmax may be published without its window.
    (C) DEGENERATE — no rung has J > 0 on a panel, i.e. the two legs never clear together
        there; the joint argmax exists arithmetically but certifies nothing.
  A KEEP-4b candidate is claimed only if the rule-8 pick clears 4b on the full sample AND its
  OOS Sharpe beats SPY's; otherwise KILL or PARK, said plainly.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  GROSS  {0.20, 0.25, ..., 1.00}   17 rungs (0.75 = the incumbent, 0.65 = 1292's robust cell)
  PANEL  {U56, B136, SMALL}        3 values (rule 9 caveat below)

  51 (panel, gross) cells, EVERY ONE PUBLISHED on every window in `.grid.csv`.

FROZEN at the incumbent's construction, NOT dials: N = 20 names, H = 126-row min hold, weekly
cadence deciding on the last trading row of the week (Fri phase) and applying at t+1 (rule 2),
3-leg composite (21/252, 0/126, 0/63) equal-ranked, above-200d and vol20 < 0.60 eligibility,
10 bps per unit turnover, 260-row warm-up, first-wins stable tie-break, equal weights inside
the book, un-invested weight in cash at 0%.

RULE 8 CHOOSER, DECLARED HERE AND NOT CHANGED AFTER READING ANYTHING.  On the IS window
(warm-up .. 2016-12-31) only, per panel, pick the gross maximising J(IS, g); ties to the LOWER
gross (declared, not chosen on a result).  Two declared comparands, both also IS-only: the
gross maximising IS Sharpe, and the frozen incumbent g = 0.75.  Then 2017-2026 is read ONCE.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT constituents of hand-kept lists; SMALL is the
current constituent list of a sub-$2B screen.  Delisted, acquired and bankrupt names are absent
from all three, which flatters every momentum book here and, because drawdown is the leg that
binds, flatters the DD margin specifically.  Tickers with max_1d_move >= 1.0 in
data/small_meta.csv are dropped from SMALL before anything is built.  Nothing here estimates
live expectancy; every reading is a within-grid difference on fixed panels and identical dates.

PROTOCOL: rule 2 execution and costs; rule 4 both KEEP paths at every rung; rule 8 walk-forward
with 2017-2026 read once; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-18_does-the-4b-MaxDD-CAP-and-CAGR-FLOOR-have-a-JOINT-MARGIN-ARGMAX-in-GROSS_cloud.py
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
A_N, A_H, A_PHASE, A_DELAY = 20, 126, 4, 1        # frozen: top-20, 126-row hold, Fri, t+1
GROSSES = [round(0.20 + 0.05 * i, 2) for i in range(17)]   # the one real dial
INCUMBENT_G = 0.75
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
    w = 4 (Fri) is exactly the incumbent's 'last trading day of the week' convention."""
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
    """The incumbent's min-hold top-N frame at UNIT gross.  Kept names hold at least A_H rows
    from their own application row; free slots go to the best-ranked eligible names read at the
    DECISION row.  Independent of gross, so it is built once per panel and scaled."""
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
    return dict(FULL=np.ones(n, bool), H1=h1, H2=h2, IS=~oos, OOS=oos)


def margins(r, spy, m):
    """4b's two non-Sharpe margins in pp on mask m, and their minimum."""
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



def _spearman(a, b):
    """Rank correlation without scipy (average ranks, Pearson on the ranks)."""
    ra = pd.Series(np.asarray(a, dtype=float)).rank().values
    rb = pd.Series(np.asarray(b, dtype=float)).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


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
    say("IDEA 1290 (lane cloud, 2026-09-18) — does the 4b MaxDD CAP and CAGR FLOOR have a JOINT")
    say("MARGIN ARGMAX in GROSS, and is that argmax the SAME IN-SAMPLE AS OUT?")
    say("=" * 100)
    say("")
    say(f"  DIALS (2, rule 4): GROSS {GROSSES[0]}..{GROSSES[-1]} step 0.05 ({len(GROSSES)} rungs)")
    say("                     x PANEL {U56, B136, SMALL}.  All 51 cells published.")
    say(f"  FROZEN: N={A_N}, H={A_H}, weekly (Fri decision), t+1 application, {REF_COST:.0f} bps,")
    say("          above-200d & vol20<0.60, equal weights, 260-row warm-up, cash at 0%.")
    say("  J(w,g) := min(dd_margin, cagr_margin) in pp on window w; g*(w) := argmax_g J(w,g).")
    say("  OUTCOMES: (A) STABLE within one rung  (B) MOVES  (C) DEGENERATE (no rung has J>0).")
    say("")

    panels, n_drop = make_panels()
    say(f"  PANELS: U56 {len(panels[0].invest)} investable; B136 {len(panels[1].invest)}; "
        f"SMALL {len(panels[2].invest)} ({n_drop} dropped for max_1d_move >= 1.0). SPY = benchmark only.")
    say("")

    # ---------------------------------------------------------- benchmarks
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
        W = windows(idx)
        B[pan.name] = dict(spy=spy, live=live, idx=idx, W=W)
        for tag, ser in (("SPY (buy & hold)", spy), ("RULES v2 (live book)", live)):
            m, mo = mt(ser), mt(ser[W["OOS"]])
            say(f"  {pan.name:6} {tag:22} {m['CAGR']:8.2%} {m['Sharpe']:8.4f} {m['MaxDD']:8.2%} "
                f"{mt(ser[W['H1']])['Sharpe']:7.4f} {mt(ser[W['H2']])['Sharpe']:7.4f} "
                f"{mo['CAGR']:9.2%} {mo['Sharpe']:8.4f} {mo['MaxDD']:8.2%}")
    say("")
    say("  Note: the 4b bar moves with the panel because SPY's window is the panel's own dates.")
    say("")

    # ---------------------------------------------------------- the ladder
    rows = []
    for pan in panels:
        spy, live, idx, W = (B[pan.name][k] for k in ("spy", "live", "idx", "W"))
        W1, app = build(pan)
        nh = (W1[WARMUP:][:, pan.iinv] > 0).sum(axis=1)
        for g in GROSSES:
            gr, tu = nrun(pan, W1 * g, app)
            r = at_cost(gr, tu, REF_COST)[WARMUP:]
            rec = legs(r, spy, live, W)
            for wn, m in W.items():
                dd, cg, j, R, S = margins(r, spy, m)
                rec[f"dd_{wn}"], rec[f"cg_{wn}"], rec[f"J_{wn}"] = dd, cg, j
                rec[f"Sharpe_{wn}"], rec[f"CAGR_{wn}"], rec[f"MaxDD_{wn}"] = (
                    R["Sharpe"], R["CAGR"], R["MaxDD"])
            rec.update(panel=pan.name, gross=g, avg_names=float(nh.mean()),
                       turnover_yr=float(tu[WARMUP:].sum() / (len(r) / 252.0)))
            rows.append(rec)
    G = pd.DataFrame(rows)

    # ---------------------------------------------------------- anchor
    say("=" * 100)
    say("ARM B — THE ANCHOR CHECK: (U56, N=20, gross 0.75, Fri, t+1) against the committed")
    say("incumbent 15.79% / 1.1529 / -19.13%, OOS 17.30% / 1.1837 (ideas 1287 / 1292)")
    say("=" * 100)
    say("")
    a = G[(G.panel == "U56") & (G.gross == INCUMBENT_G)].iloc[0]
    tgt = dict(CAGR=0.1579, Sharpe=1.1529, MaxDD=-0.1913, OOS_CAGR=0.1730, OOS_Sharpe=1.1837)
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

    # ---------------------------------------------------------- ladder table
    say("=" * 100)
    say("ARM C — THE GROSS LADDER, every rung, every panel (all 51 cells; .grid.csv has all")
    say("windows).  dd/cg/J in pp on the FULL sample; J>0 iff both non-Sharpe 4b legs clear.")
    say("=" * 100)
    say("")
    for pan in panels:
        sub = G[G.panel == pan.name]
        say(f"  --- {pan.name} " + "-" * 84)
        say(f"  {'gross':>6} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'turn/yr':>8} "
            f"{'ddFULL':>8} {'cgFULL':>8} {'J_FULL':>8} {'J_IS':>8} {'J_OOS':>8} "
            f"{'4a':>3} {'4b':>3}")
        for _, x in sub.iterrows():
            mark = " <-inc" if x.gross == INCUMBENT_G else ""
            say(f"  {x.gross:6.2f} {x.CAGR:8.2%} {x.Sharpe:8.4f} {x.MaxDD:8.2%} "
                f"{x.turnover_yr:8.2f} {x.dd_FULL:8.2f} {x.cg_FULL:8.2f} {x.J_FULL:8.2f} "
                f"{x.J_IS:8.2f} {x.J_OOS:8.2f} {'Y' if x.pass4a else '.':>3} "
                f"{'Y' if x.pass4b else '.':>3}{mark}")
        say("")
    say(f"  LADDER-WIDE: 4b passes {int(G.pass4b.sum())} of {len(G)} cells; "
        f"4a passes {int(G.pass4a.sum())} of {len(G)}.")
    say("  4b by panel: " + ", ".join(
        f"{p}: {int(G[G.panel == p].pass4b.sum())}/{len(G[G.panel == p])}"
        for p in ["U56", "B136", "SMALL"]) + ".")
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

    # ---------------------------------------------------------- the argmax
    say("=" * 100)
    say("ARM D — THE JOINT ARGMAX, window by window.  g*(w) = argmax_g J(w,g), ties to the")
    say("LOWER gross.  'defined' means max_g J(w,g) > 0, i.e. some rung clears both legs.")
    say("=" * 100)
    say("")
    WNAMES = ["FULL", "H1", "H2", "IS", "OOS"]
    ARG = []
    for pan in panels:
        sub = G[G.panel == pan.name].sort_values("gross").reset_index(drop=True)
        rec = dict(panel=pan.name)
        for wn in WNAMES:
            col = sub[f"J_{wn}"].values
            i = int(np.nanargmax(col))
            rec[f"gstar_{wn}"] = float(sub.gross.values[i])
            rec[f"Jmax_{wn}"] = float(col[i])
            rec[f"defined_{wn}"] = bool(col[i] > 0)
            rec[f"interior_{wn}"] = bool(0 < i < len(col) - 1)
        ARG.append(rec)
    A2 = pd.DataFrame(ARG)
    say(f"  {'panel':6} " + " ".join(f"{'g*/J ' + w:>16}" for w in WNAMES))
    for _, x in A2.iterrows():
        say(f"  {x.panel:6} " + " ".join(
            f"{x['gstar_' + w]:6.2f} /{x['Jmax_' + w]:8.2f}" for w in WNAMES))
    say("")
    say(f"  {'panel':6} " + " ".join(f"{'defined ' + w:>12}" for w in WNAMES)
        + "   interior maxima")
    for _, x in A2.iterrows():
        say(f"  {x.panel:6} " + " ".join(
            f"{('YES' if x['defined_' + w] else 'no'):>12}" for w in WNAMES)
            + "   " + ",".join(w for w in WNAMES if x[f"interior_{w}"]))
    say("")

    # ---------------------------------------------------------- stability
    say("=" * 100)
    say("ARM E — IS THE ARGMAX THE SAME IN-SAMPLE AS OUT?  Rung distance and OOS REGRET.")
    say("=" * 100)
    say("")
    step = 0.05
    STAB = []
    for pan in panels:
        sub = G[G.panel == pan.name].set_index("gross")
        x = A2[A2.panel == pan.name].iloc[0]
        gi, go = x.gstar_IS, x.gstar_OOS
        rungs = abs(round((gi - go) / step))
        regret = float(sub.loc[gi, "J_OOS"] - sub.loc[go, "J_OOS"])
        # what the incumbent's frozen 0.75 would have cost on the same OOS window
        reg_inc = float(sub.loc[INCUMBENT_G, "J_OOS"] - sub.loc[go, "J_OOS"])
        rho = _spearman(sub["J_IS"].values, sub["J_OOS"].values)
        STAB.append(dict(panel=pan.name, gstar_IS=gi, gstar_OOS=go, rungs_apart=int(rungs),
                         J_OOS_at_ISpick=float(sub.loc[gi, "J_OOS"]),
                         J_OOS_at_OOSpick=float(sub.loc[go, "J_OOS"]),
                         oos_regret_pp=regret, incumbent_regret_pp=reg_inc,
                         spearman_J_IS_vs_J_OOS=rho,
                         defined_IS=bool(x.defined_IS), defined_OOS=bool(x.defined_OOS)))
    ST = pd.DataFrame(STAB)
    say(f"  {'panel':6} {'g*(IS)':>7} {'g*(OOS)':>8} {'rungs':>6} {'J_OOS@IS':>9} "
        f"{'J_OOS@OOS':>10} {'regret pp':>10} {'g=0.75 regret':>14} {'rho(J_IS,J_OOS)':>16}")
    for _, x in ST.iterrows():
        say(f"  {x.panel:6} {x.gstar_IS:7.2f} {x.gstar_OOS:8.2f} {x.rungs_apart:6d} "
            f"{x.J_OOS_at_ISpick:9.2f} {x.J_OOS_at_OOSpick:10.2f} {x.oos_regret_pp:10.2f} "
            f"{x.incumbent_regret_pp:14.2f} {x.spearman_J_IS_vs_J_OOS:16.4f}")
    say("")
    say("  Read: regret is NEGATIVE by construction (the OOS argmax maximises J_OOS); its SIZE")
    say("  in pp is what choosing gross in-sample costs on the untouched window.  A rung")
    say("  distance of 0-1 with small regret is outcome (A); anything larger is (B).")
    say("")

    # ---------------------------------------------------------- rule 8
    say("=" * 100)
    say("ARM F — RULE 8 WALK-FORWARD: gross chosen on warm-up..2016 ONLY, 2017-2026 read ONCE")
    say("=" * 100)
    say("")
    say("  CHOOSER (declared in the header): argmax_g J(IS, g), ties to the LOWER gross.")
    say("  COMPARANDS, also IS-only: argmax_g IS Sharpe; and the frozen incumbent g=0.75.")
    say("")
    WF = []
    for pan in panels:
        sub = G[G.panel == pan.name].sort_values("gross").reset_index(drop=True)
        gJ = float(sub.gross.values[int(np.nanargmax(sub["J_IS"].values))])
        gS = float(sub.gross.values[int(np.nanargmax(sub["Sharpe_IS"].values))])
        bs = mt(B[pan.name]["spy"][B[pan.name]["W"]["OOS"]])
        bl = mt(B[pan.name]["live"][B[pan.name]["W"]["OOS"]])
        for tag, g in (("JOINT-MARGIN (this run)", gJ), ("IS-SHARPE-MAX", gS),
                       ("INCUMBENT g=0.75", INCUMBENT_G)):
            x = sub[sub.gross == g].iloc[0]
            WF.append(dict(panel=pan.name, chooser=tag, gross=g, OOS_CAGR=x.OOS_CAGR,
                           OOS_Sharpe=x.OOS_Sharpe, OOS_MaxDD=x.OOS_MaxDD, J_OOS=x.J_OOS,
                           J_IS=x.J_IS, pass4b_full=bool(x.pass4b), pass4a_full=bool(x.pass4a),
                           beats_SPY_OOS=bool(x.OOS_Sharpe > bs["Sharpe"]),
                           spy_OOS_Sharpe=bs["Sharpe"], spy_OOS_CAGR=bs["CAGR"],
                           spy_OOS_MaxDD=bs["MaxDD"], live_OOS_Sharpe=bl["Sharpe"],
                           live_OOS_CAGR=bl["CAGR"], live_OOS_MaxDD=bl["MaxDD"]))
    W8 = pd.DataFrame(WF)
    say(f"  {'panel':6} {'chooser':24} {'g':>5} {'OOS CAGR':>9} {'OOS Sh':>8} {'OOS DD':>8} "
        f"{'J_OOS':>8} {'>SPY?':>6} {'4b full':>8}")
    for _, x in W8.iterrows():
        say(f"  {x.panel:6} {x.chooser:24} {x.gross:5.2f} {x.OOS_CAGR:9.2%} {x.OOS_Sharpe:8.4f} "
            f"{x.OOS_MaxDD:8.2%} {x.J_OOS:8.2f} {'YES' if x.beats_SPY_OOS else 'no':>6} "
            f"{'PASS' if x.pass4b_full else 'FAIL':>8}")
    say("")
    say("  Same OOS window, the two things a real account is measured against:")
    say(f"  {'panel':6} {'series':22} {'CAGR':>9} {'Sharpe':>9} {'MaxDD':>9}")
    for pan in panels:
        x = W8[W8.panel == pan.name].iloc[0]
        say(f"  {pan.name:6} {'RULES v2 (live)':22} {x.live_OOS_CAGR:9.2%} "
            f"{x.live_OOS_Sharpe:9.4f} {x.live_OOS_MaxDD:9.2%}")
        say(f"  {pan.name:6} {'SPY':22} {x.spy_OOS_CAGR:9.2%} {x.spy_OOS_Sharpe:9.4f} "
            f"{x.spy_OOS_MaxDD:9.2%}")
    say("")

    # ---------------------------------------------------------- verdict
    say("=" * 100)
    say("ARM G — THE ANSWER")
    say("=" * 100)
    say("")
    live_panels = ST[ST.defined_IS & ST.defined_OOS]
    if len(live_panels) == 0:
        outcome = ("(C) DEGENERATE everywhere — no panel has a gross rung where BOTH non-Sharpe "
                   "4b legs clear on both windows, so the joint argmax certifies nothing")
    elif (live_panels.rungs_apart <= 1).all():
        outcome = ("(A) STABLE — g*(IS) and g*(OOS) agree within one rung on every panel where "
                   "J is defined on both windows")
    else:
        outcome = ("(B) MOVES — g*(IS) and g*(OOS) differ by more than one rung on at least one "
                   "panel where J is defined on both windows")
    say(f"  OUTCOME: {outcome}.")
    say("")
    for _, x in ST.iterrows():
        say(f"    {x.panel:6} g*(IS)={x.gstar_IS:.2f} g*(OOS)={x.gstar_OOS:.2f} "
            f"({x.rungs_apart} rungs, regret {x.oos_regret_pp:+.2f} pp, "
            f"J defined IS={'Y' if x.defined_IS else 'N'} OOS={'Y' if x.defined_OOS else 'N'})")
    say("")
    cand = W8[(W8.chooser == "JOINT-MARGIN (this run)") & W8.pass4b_full & W8.beats_SPY_OOS]
    if len(cand):
        say("  KEEP-4b CANDIDATE(S) from the declared chooser: " + ", ".join(
            f"{r.panel} g={r.gross:.2f} (OOS {r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / "
            f"{r.OOS_MaxDD:.2%})" for _, r in cand.iterrows()))
        say("  A memo is written for these; RULES.md is NOT touched (rule 6: Sunday review).")
    else:
        say("  NO KEEP-4b CANDIDATE: the declared chooser's pick clears 4b on the full sample")
        say("  and beats SPY out-of-sample on ZERO panels.")
    say("")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents; delisted and")
    say("  bankrupt names are absent, which flatters the drawdown leg specifically. Every")
    say("  number here is a within-grid difference on fixed panels and identical dates.")
    say("")
    say(f"  ({time.time() - t0:.1f}s)")

    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    A2.to_csv(OUT.with_suffix(".argmax.csv"), index=False)
    ST.to_csv(OUT.with_suffix(".stability.csv"), index=False)
    W8.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    OUT.with_suffix(".log.txt").write_text("\n".join(_LOG) + "\n")
    print(f"\nwrote {OUT.name}.grid.csv / .argmax.csv / .stability.csv / .walkforward.csv / .log.txt")


if __name__ == "__main__":
    main()
