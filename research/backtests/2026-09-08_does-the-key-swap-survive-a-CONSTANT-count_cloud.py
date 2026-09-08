#!/usr/bin/env python3
"""Idea 447 — does-the-key-swap-survive-a-CONSTANT-count   (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 227 (both lanes, 2026-09-08) killed the composite's q = 0.90-0.95 trim under CANDq —
    a TIME-VARYING count, n_t = round(q * E_t), at a constantly rebuilt 75% gross.  Its two
    findings were (i) VETO: KEEPTOP beats KEEPBOT in 77 of 90 cells, mean gap +0.0746, so the
    ranking carries real sign information, and (ii) NO SELECTOR: KEEPTOP does NOT beat a
    persistent-random key of the same trim depth (U56 q=0.90 sits at the 86.7th percentile of
    60 random keys, p = 0.148).  Idea 155 had separately shown that under a CONSTANT count at
    equal cash the selectivity argmax moves (0.55 on U56, 1.00 on B136).  So: is the
    VETO/SELECTOR split a property of the RANKING, or of the COUNT RULE?

WHAT THIS RUN DOES
    The same 5 keys x 2 directions x 60-seed persistent-random null as idea 227 lane B, run on
    THREE constructions at MATCHED mean book size, so the count rule is the treatment and
    everything else (gate, gross level, cadence, execution, cost identity) is held fixed:

        CANDq      n_t = clip(round(S * E_t), 1, E_t), w = 0.75 / count_held
                   idea 227's construction.  Count tracks the eligible set; gross always 75%.
        CONSTn-dg  n = round(S * mean_IS E_t) fixed for all time; hold the top min(n, E_t);
                   w = 0.75 / n PER NAME (equal cash).  Idea 155's "constant count at equal
                   cash": the book DE-GROSSES to cash whenever E_t < n.  THE QUEUE'S TARGET.
        CONSTn-rw  the same fixed n, but w = 0.75 / count_held (gross rebuilt).
                   Not asked for; carried because CANDq and CONSTn-dg differ in TWO ways at
                   once (the count rule AND the cash convention).  CONSTn-rw isolates the
                   count rule alone, so a difference can be attributed rather than just seen.

    n is pinned on the IN-SAMPLE window only (mean E_t over 2009-2016 rebalance weeks), so the
    constant-count arms never read the evaluation period to set their own size.  This is idea
    160's matching convention, imported, not invented here.

    ARMS (all pre-registered treatment axes, none tuned)
        KEYS        COMP (idea 155's composite: mean pct-rank of 12-1 momentum, 6m, 3m; no vol
                    tilt) · MOM · R6 · R3 · LOWVOL (-vol20)
        DIRECTIONS  KEEPTOP (drop the worst — idea 155's reading) · KEEPBOT (drop the best)
        NULL        SHUFF, one uniform draw per NAME held forever, 60 seeds.  This is the
                    turnover-matched null; idea 227 lane B established that the weekly-redraw
                    null SHUFW answers a different question (persistence, not information),
                    so it is NOT re-run here.
        CONTROL     S0 = CANDq at S = 1.00 = hold EVERY eligible name at full gross (EWall).
                    Key-independent by construction and identical across all 70 arms, so it is
                    the shared do-nothing endpoint every premium is measured from.

    The cost identity net(c) = gross - turnover * c / 1e4 (idea 155, re-verified here to
    < 1e-12) means every rung is read off ONE 0-bps backtest per book.

TUNED PARAMETERS (exactly two; every grid point reported)
    P1  the depth S in {0.40, 0.55, 0.70, 0.85, 0.95, 1.00}, which sets the count: n_t under
        CANDq and n under both CONSTn arms.  0.55 and 1.00 are idea 155's published constant-
        count argmaxes, carried in rather than fitted; 0.85/0.95 are idea 227's trim region.
    P2  cost rung in {0, 5, 10, 15, 20, 25, 30} bps.  10 bps is the protocol rung and the only
        rung a KEEP verdict is read at; 0 is a composition diagnostic; 25/30 are robustness.
    Panel, construction, key, direction and seed are reported at every point, never chosen.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    R1  The VETO (KEEPTOP > KEEPBOT) survives the count rule: the direction gap stays positive
        in a large majority of cells under CONSTn-dg too.  A ranking's sign content should not
        depend on whether the count floats.
    R2  The NO-SELECTOR result also survives: COMP/KEEPTOP will not clear the 60-seed
        persistent-random null at the 5% level on more than 1 of 6 headline cells under
        CONSTn-dg, i.e. the same base rate idea 227 found under CANDq.
    R3  CONSTn-dg will show a LOWER Sharpe than CANDq at the same S on the panels where E_t is
        most variable (B136), because the fixed count de-grosses into cash exactly when breadth
        is narrow, which is when the gate is already defensive.  If instead it shows a HIGHER
        Sharpe, the "argmax moves" result of idea 155 is a CASH effect, not a count effect —
        and CONSTn-rw is the arm that tells the two apart.
    R4  No 4b KEEP survives rule 8 on any panel under any construction.
    R5  SMALL439 produces 0 4b passes (idea 136's 17th reproduction).

CONFOUNDS / CAVEATS declared up front
    * CONSTn-dg changes the count rule AND the cash convention relative to CANDq.  CONSTn-rw is
      the decomposition control and is read beside it at every point.
    * A constant count is a different EXPOSURE, not just a different selection: gross is 75%
      only when E_t >= n.  Realised mean gross is reported for every CONSTn-dg cell.
    * Premiums are differences of Sharpe ratios on overlapping samples; no significance is
      claimed from a curve's shape, only from the 60-seed null.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md) with every ticker
      whose max_1d_move >= 1.0 in data/small_meta.csv dropped first.  SURVIVORSHIP BIAS — it
      is a shape check, never a tradable return.
    * The fast backtester used here is validated against products/backtester/engine.backtest
      on 6 books (2 per panel) to < 1e-12 on both returns and turnover BEFORE any grid number
      is read; if that gate fails the run aborts.

Deterministic (seed 447000), standalone, no network.
Writes .console.txt .grid.csv.gz .curve.csv .null.csv .walkforward.csv .keep.csv .result.md
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
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics, rebalance_mask                           # noqa: E402

STEM = "2026-09-08_does-the-key-swap-survive-a-CONSTANT-count_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 447000
IS_END, OOS_START = "2016-12-31", "2017-01-01"

FREQ, MAX_VOL, GROSS = "W", 0.60, 0.75
S_GRID = [0.40, 0.55, 0.70, 0.85, 0.95, 1.00]              # P1
COSTS = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]           # P2
PROTO = 10.0
N_NULL = 60
KEYS = ["COMP", "MOM", "R6", "R3", "LOWVOL"]
DIRS = ["KEEPTOP", "KEEPBOT"]
CONSTRUCTIONS = ["CANDq", "CONSTn-dg", "CONSTn-rw"]
PANEL_SEED = {"U56": 1, "B136": 2, "SMALL439": 3}          # fixed, never hash() (randomised)

pd.set_option("display.width", 250)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# --------------------------------------------------------------------------- fast backtester
def fast_backtest(px, w, freq=FREQ):
    """Exact vectorised replica of engine.backtest(cost_bps=0).  Validated < 1e-12 below."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    starts = np.flatnonzero(mask)
    ends = np.append(starts[1:], len(idx))
    port = np.zeros(len(idx))
    tno = np.zeros(len(idx))
    carry = np.zeros(px.shape[1])
    for s, e in zip(starts, ends):
        w0 = wt[s]
        tno[s] = np.abs(w0 - carry).sum()
        c0 = 1.0 - w0.sum()
        g = np.cumprod(1.0 + rets[s:e], axis=0)
        gs = np.vstack([np.ones((1, px.shape[1])), g])          # value factor at each day start
        v = w0[None, :] * gs                                    # e-s+1 rows
        tot = v.sum(axis=1) + c0
        tot = np.where(tot > 0, tot, np.nan)
        held = v / tot[:, None]
        port[s:e] = np.nansum(held[:-1] * rets[s:e], axis=1)
        carry = held[-1]
        if not np.isfinite(carry).all():
            carry = np.where(np.isfinite(carry), carry, np.nan)
    return (pd.Series(port, index=idx), pd.Series(tno, index=idx))


def validate_fast(PANELS):
    P("\n  pre-check [a]: fast backtester vs products/backtester/engine.backtest (6 books)")
    worst_r = worst_t = 0.0
    for pk, (px, tradable, _) in PANELS.items():
        start = px.index[260]
        gate = gate_mask(px, tradable)
        E = gate.sum(axis=1)
        elig, rank = key_rank(px, gate, "COMP", "KEEPTOP")
        for w in (rules_v1_weights(px), weights_candq(elig, rank, E, 0.85)):
            ref = backtest(px, w, cost_bps=0.0, freq=FREQ)
            r, t = fast_backtest(px, w)
            dr = float((ref["returns"].loc[start:] - r.loc[start:]).abs().max())
            dt = float((ref["turnover"].loc[start:] - t.loc[start:]).abs().max())
            worst_r, worst_t = max(worst_r, dr), max(worst_t, dt)
    P(f"      max |d returns| = {worst_r:.3e}   max |d turnover| = {worst_t:.3e}"
      f"   (both must be < 1e-12)")
    assert worst_r < 1e-12 and worst_t < 1e-12, "fast backtester does not replicate the engine"
    return worst_r, worst_t


# --------------------------------------------------------------------------- panels & books
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[keep + ["SPY"]]
    return {
        "U56": (px56, set(px56.columns), "universe.json(56)"),
        "B136": (px136, set(px136.columns), "universe_broad.json(136)"),
        "SMALL439": (pxs, set(keep), f"prices_small({len(keep)}, SPY held out)"),
    }


def gate_mask(px, tradable):
    """Idea 155's eligibility gate, key-independent: above the 200d MA and vol20 < 0.60."""
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def raw_key(px, name, rng=None):
    if name == "COMP":
        mom = px.shift(21) / px.shift(252) - 1
        r6 = px / px.shift(126) - 1
        r3 = px / px.shift(63) - 1
        return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                + r3.rank(axis=1, pct=True)) / 3
    if name == "MOM":
        return px.shift(21) / px.shift(252) - 1
    if name == "R6":
        return px / px.shift(126) - 1
    if name == "R3":
        return px / px.shift(63) - 1
    if name == "LOWVOL":
        return -(px.pct_change().rolling(20).std() * np.sqrt(252))
    if name == "SHUFF":
        draw = rng.random(px.shape[1])
        return pd.DataFrame(np.tile(draw, (len(px), 1)), index=px.index, columns=px.columns)
    raise KeyError(name)


def key_rank(px, gate, kname, direction, rng=None):
    """(elig, rank) with rank 1 = held first.  A name with an undefined key is not eligible."""
    k = raw_key(px, kname, rng).where(gate)
    elig = gate & k.notna()
    rank = k.rank(axis=1, ascending=(direction == "KEEPBOT"))
    return elig, rank.where(elig)


def weights_candq(elig, rank, E, s):
    """n_t = clip(round(s*E_t), 1, E_t); gross rebuilt over the held names."""
    n_t = np.clip(np.round(s * E.values), 1, np.maximum(E.values, 1))
    sel = rank.le(pd.Series(n_t, index=elig.index), axis=0) & elig
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def weights_constn(elig, rank, n, mode):
    """Fixed count n.  mode 'dg': w = GROSS/n per name (equal cash, de-grosses when E_t < n).
       mode 'rw': w = GROSS/count_held (gross rebuilt)."""
    sel = rank.le(float(n)) & elig
    if mode == "dg":
        return sel.astype(float).mul(GROSS / n)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def net(r0, tno, c):
    return r0 - tno * c / 1e4


def csdm(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# --------------------------------------------------------------------------- the grid
def run_grid(PANELS):
    rows, REF = [], {}
    t0 = time.time()
    for pk, (px, tradable, desc) in PANELS.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2r, v2t = fast_backtest(px, rules_v2_weights(px))
        v1r, v1t = fast_backtest(px, rules_v1_weights(px))
        gate = gate_mask(px, tradable)
        E = gate.sum(axis=1)
        rb = rebalance_mask(px.index, FREQ)
        E_is = float(E.loc[start:IS_END][rb.loc[start:IS_END]].mean())
        E_full = float(E.loc[start:][rb.loc[start:]].mean())
        NMAP = {s: max(1, int(round(s * E_is))) for s in S_GRID}
        REF[pk] = dict(px=px, start=start, spy=spy, gate=gate, E=E, E_is=E_is, E_full=E_full,
                       NMAP=NMAP, desc=desc,
                       v2=(v2r.loc[start:], v2t.loc[start:]),
                       v1=(v1r.loc[start:], v1t.loc[start:]))
        cg, sh, dd = csdm(spy)
        oc, osh, odd = csdm(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}")
        P(f"      SPY {cg:.2%}/{sh:.3f}/{dd:.2%} | OOS {oc:.2%}/{osh:.3f}/{odd:.2%}")
        for c in (PROTO, 25.0):
            a, b, d_ = csdm(net(*REF[pk]["v2"], c))
            e, f_, g_ = csdm(net(*REF[pk]["v1"], c))
            P(f"      RULES v2 @{c:.0f}bps {a:.2%}/{b:.3f}/{d_:.2%}   "
              f"RULES v1 @{c:.0f}bps {e:.2%}/{f_:.3f}/{g_:.2%}")
        P(f"      eligible count E_t: mean IS {E_is:.2f}, mean full {E_full:.2f}, "
          f"range {int(E.loc[start:].min())}-{int(E.loc[start:].max())}")
        P(f"      constant counts n(S) = round(S * mean_IS E_t): " +
          ", ".join(f"S={s:.2f}->n={NMAP[s]}" for s in S_GRID))

        arms = [(k, d, -1) for k in KEYS for d in DIRS] + [("SHUFF", "KEEPTOP", s)
                                                           for s in range(N_NULL)]
        rng = np.random.default_rng(SEED + PANEL_SEED[pk])
        n_books = 0
        for kname, direction, seed in arms:
            elig, rank = key_rank(px, gate, kname, direction, rng)
            for s in S_GRID:
                books = {
                    "CANDq": weights_candq(elig, rank, E, s),
                    "CONSTn-dg": weights_constn(elig, rank, NMAP[s], "dg"),
                    "CONSTn-rw": weights_constn(elig, rank, NMAP[s], "rw"),
                }
                for cons, w in books.items():
                    r0, tn = fast_backtest(px, w)
                    r0, tn = r0.loc[start:], tn.loc[start:]
                    n_books += 1
                    held = (w > 0).loc[start:]
                    gross_mean = float(w.loc[start:].sum(axis=1).mean())
                    n_names = float(held.sum(axis=1).replace(0, np.nan).mean())
                    for c in COSTS:
                        r = net(r0, tn, c)
                        cg2, sh2, dd2 = csdm(r)
                        h1, h2 = halves(r)
                        oc2, osh2, odd2 = csdm(r.loc[OOS_START:])
                        rows.append(dict(
                            panel=pk, cons=cons, key=kname, dir=direction, seed=seed, S=s,
                            n_target=NMAP[s], cost=c, n_names=n_names, gross=gross_mean,
                            turnover=float(tn.mean() * 52),
                            CAGR=cg2, Sharpe=sh2, MaxDD=dd2, H1=h1, H2=h2,
                            IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                            OOS_CAGR=oc2, OOS_Sharpe=osh2, OOS_MaxDD=odd2))
        P(f"      {n_books} books done ({time.time()-t0:.0f}s cum.)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False, compression="gzip")
    P(f"\n  grid: {len(G)} rows -> {STEM}.grid.csv.gz")
    return G, REF


def check_identity(REF, PANELS):
    P("\n  pre-check [b]: cost identity net(c) = gross - turnover * c / 1e4")
    worst = 0.0
    for pk, (px, tradable, _) in PANELS.items():
        start, gate, E = REF[pk]["start"], REF[pk]["gate"], REF[pk]["E"]
        elig, rank = key_rank(px, gate, "COMP", "KEEPTOP")
        for w in (weights_candq(elig, rank, E, 0.85),
                  weights_constn(elig, rank, REF[pk]["NMAP"][0.85], "dg")):
            r0, tn = fast_backtest(px, w)
            direct = backtest(px, w, cost_bps=PROTO, freq=FREQ)["returns"].loc[start:]
            worst = max(worst, float((direct - net(r0.loc[start:], tn.loc[start:],
                                                   PROTO)).abs().max()))
    P(f"      max |direct 10-bps backtest - net(gross, turnover, 10)| = {worst:.3e}"
      f"   (must be < 1e-12)")
    return worst


def check_premise(G, REF):
    """[c] the CANDq control must be key-independent, and idea 227's headline cells reproduce."""
    P("\n  pre-check [c]: CANDq @ S=1.00 must be the IDENTICAL book for all 70 arms")
    worst = 0.0
    for pk in G.panel.unique():
        v = G[(G.panel == pk) & (G.cons == "CANDq") & (G.S == 1.00)
              & (G.cost == PROTO)].Sharpe
        worst = max(worst, float(v.max() - v.min()))
    P(f"      max spread of the S=1.00 CANDq Sharpe across arms = {worst:.3e}"
      f"   (must be < 1e-12)")
    P("\n  pre-check [d]: idea 227's published CANDq COMP/KEEPTOP cells (10 bps).  This run's")
    P("      S grid does not contain 0.90/0.95, so these are re-derived here at those q.")
    got = {}
    for pk, q, pub in (("U56", 0.90, 1.0808), ("B136", 0.95, 1.0424)):
        px, gate, E, start = (REF[pk]["px"], REF[pk]["gate"], REF[pk]["E"], REF[pk]["start"])
        elig, rank = key_rank(px, gate, "COMP", "KEEPTOP")
        r0, tn = fast_backtest(px, weights_candq(elig, rank, E, q))
        sh = metrics(net(r0.loc[start:], tn.loc[start:], PROTO))["Sharpe"]
        got[(pk, q)] = sh
        P(f"      {pk} CANDq COMP/KEEPTOP q={q:.2f} @10bps: idea 227 published {pub:.4f}, "
          f"this run {sh:.4f}  (|d| = {abs(sh-pub):.4f})")
    return worst, got


# --------------------------------------------------------------------------- part 1
def curves(G):
    P("\n" + "=" * 118)
    P("PART 1 — SHARPE BY DEPTH, PER CONSTRUCTION.  Premium = Sharpe(arm) - Sharpe(S0), where")
    P("         S0 = CANDq @ S=1.00 (hold every eligible name at full gross), the one book all")
    P("         70 arms share.  Protocol rung 10 bps.")
    P("=" * 118)
    out = []
    for (pk, cost), g in G.groupby(["panel", "cost"]):
        base = g[(g.cons == "CANDq") & (g.S == 1.00) & (g.key == "COMP")
                 & (g["dir"] == "KEEPTOP")].Sharpe.iloc[0]
        for (cons, k, d, s), gg in g.groupby(["cons", "key", "dir", "S"]):
            out.append(dict(panel=pk, cost=cost, cons=cons, key=k, dir=d, S=s, base=base,
                            Sharpe=gg.Sharpe.mean(), Sharpe_sd=gg.Sharpe.std(ddof=1),
                            premium=gg.Sharpe.mean() - base, n_draws=len(gg),
                            CAGR=gg.CAGR.mean(), MaxDD=gg.MaxDD.mean(),
                            turnover=gg.turnover.mean(), gross=gg.gross.mean(),
                            n_names=gg.n_names.mean(), OOS_Sharpe=gg.OOS_Sharpe.mean()))
    CV = pd.DataFrame(out)
    CV.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    for pk in G.panel.unique():
        sub = CV[(CV.panel == pk) & (CV.cost == PROTO)]
        P(f"\n  {pk} @ 10 bps   (S0 = CANDq S=1.00, Sharpe {sub.base.iloc[0]:.4f})")
        for cons in CONSTRUCTIONS:
            P(f"    [{cons}]  {'arm':16s} " + " ".join(f"{s:>8.2f}" for s in S_GRID)
              + "   gross@0.70  tno@0.70")
            for k in KEYS + ["SHUFF"]:
                for d in (DIRS if k != "SHUFF" else ["KEEPTOP"]):
                    r = sub[(sub.cons == cons) & (sub.key == k)
                            & (sub["dir"] == d)].set_index("S").reindex(S_GRID)
                    tag = f"{k}/{d[4:]}" + (f" (null x{int(r.n_draws.iloc[0])})"
                                            if k == "SHUFF" else "")
                    P(f"             {tag:16s} " +
                      " ".join(f"{v:+8.4f}" for v in r.premium.values) +
                      f"   {float(r.loc[0.70,'gross']):6.3f}   {float(r.loc[0.70,'turnover']):6.1f}")
    return CV


# --------------------------------------------------------------------------- part 2
def veto_and_null(G, REF):
    P("\n" + "=" * 118)
    P("PART 2 — IS THE VETO/SELECTOR SPLIT A PROPERTY OF THE RANKING OR OF THE COUNT RULE?")
    P("=" * 118)
    P("\n  (a) THE VETO.  Direction gap = Sharpe(KEEPTOP) - Sharpe(KEEPBOT) at the same panel,")
    P("      key, depth and rung.  Idea 227 (CANDq only): positive in 77 of 90 cells, mean")
    P("      +0.0746.  Per construction, all rungs, all depths, all keys, all panels:")
    det = G[G.seed == -1]
    top = det[det["dir"] == "KEEPTOP"].set_index(["panel", "cons", "key", "S", "cost"]).Sharpe
    bot = det[det["dir"] == "KEEPBOT"].set_index(["panel", "cons", "key", "S", "cost"]).Sharpe
    gap = (top - bot).rename("gap").reset_index()
    P(f"\n      {'construction':12s} {'cells':>7s} {'gap>0':>10s} {'mean gap':>10s} "
      f"{'median':>9s} {'min':>9s} {'max':>9s}")
    for cons in CONSTRUCTIONS:
        s = gap[gap.cons == cons].gap
        P(f"      {cons:12s} {len(s):7d} {f'{(s>0).sum()}/{len(s)}':>10s} {s.mean():+10.4f} "
          f"{s.median():+9.4f} {s.min():+9.4f} {s.max():+9.4f}")
    P(f"\n      restricted to the protocol rung and S < 1.00 (a real trim), by panel:")
    P(f"      {'construction':12s} {'panel':9s} {'gap>0':>10s} {'mean gap':>10s}")
    for cons in CONSTRUCTIONS:
        for pk in G.panel.unique():
            s = gap[(gap.cons == cons) & (gap.panel == pk) & (gap.cost == PROTO)
                    & (gap.S < 1.0)].gap
            P(f"      {cons:12s} {pk:9s} {f'{(s>0).sum()}/{len(s)}':>10s} {s.mean():+10.4f}")
    P(f"\n      by key, protocol rung, pooled over panels and depths:")
    P(f"      {'construction':12s} " + " ".join(f"{k:>10s}" for k in KEYS))
    for cons in CONSTRUCTIONS:
        vals = []
        for k in KEYS:
            s = gap[(gap.cons == cons) & (gap.key == k) & (gap.cost == PROTO)].gap
            vals.append(f"{s.mean():+10.4f}")
        P(f"      {cons:12s} " + " ".join(vals))
    gap.to_csv(OUT / f"{STEM}.veto.csv", index=False)

    P("\n  (b) THE SELECTOR TEST.  COMP/KEEPTOP against the 60-seed persistent-random null at")
    P("      the same panel, construction, depth and rung.  Exact one-sided p = share of null")
    P("      draws >= COMP.  Idea 227 under CANDq: U56 q=0.90 p=0.148, B136 q=0.95 p=0.033,")
    P("      1 of 6 cells below 5%.")
    rows = []
    for pk in G.panel.unique():
        for cons in CONSTRUCTIONS:
            for s in S_GRID:
                for cost in COSTS:
                    nd = G[(G.panel == pk) & (G.cons == cons) & (G.S == s) & (G.cost == cost)
                           & (G.key == "SHUFF")].Sharpe.values
                    for k in KEYS:
                        for d in DIRS:
                            v = G[(G.panel == pk) & (G.cons == cons) & (G.S == s)
                                  & (G.cost == cost) & (G.key == k)
                                  & (G["dir"] == d)].Sharpe.iloc[0]
                            rows.append(dict(
                                panel=pk, cons=cons, key=k, dir=d, S=s, cost=cost,
                                Sharpe=v, null_mean=nd.mean(), null_sd=nd.std(ddof=1),
                                null_max=nd.max(), excess=v - nd.mean(),
                                pct=float((nd < v).mean()) * 100,
                                p=float((nd >= v).mean()),
                                z=(v - nd.mean()) / nd.std(ddof=1) if nd.std(ddof=1) > 0
                                else np.nan))
    NT = pd.DataFrame(rows)
    NT.to_csv(OUT / f"{STEM}.null.csv", index=False)
    for cons in CONSTRUCTIONS:
        P(f"\n      [{cons}] COMP/KEEPTOP vs the 60-seed null, 10 bps")
        P(f"      {'panel':9s} {'S':>5s} {'n':>5s} {'COMP':>8s} {'null mean':>10s} "
          f"{'null sd':>8s} {'pctile':>7s} {'exact p':>8s}")
        for pk in G.panel.unique():
            for s in S_GRID:
                r = NT[(NT.panel == pk) & (NT.cons == cons) & (NT.S == s)
                       & (NT.cost == PROTO) & (NT.key == "COMP")
                       & (NT["dir"] == "KEEPTOP")].iloc[0]
                nn = REF[pk]["NMAP"][s]
                P(f"      {pk:9s} {s:5.2f} {nn:5d} {r.Sharpe:8.4f} {r.null_mean:10.4f} "
                  f"{r.null_sd:8.4f} {r.pct:6.1f}% {r.p:8.3f}")
    sig = NT[(NT.key == "COMP") & (NT["dir"] == "KEEPTOP") & (NT.cost == PROTO)
             & (NT.S < 1.0)]
    P(f"\n      cells below p = 0.05 (COMP/KEEPTOP, 10 bps, S < 1.00), per construction:")
    for cons in CONSTRUCTIONS:
        s_ = sig[sig.cons == cons]
        P(f"          {cons:12s} {int((s_.p < 0.05).sum())} of {len(s_)}   "
          f"(mean percentile {s_.pct.mean():.1f})")
    P(f"\n      the same count over ALL 5 keys x KEEPTOP, 10 bps, S < 1.00:")
    allk = NT[(NT["dir"] == "KEEPTOP") & (NT.cost == PROTO) & (NT.S < 1.0)]
    for cons in CONSTRUCTIONS:
        s_ = allk[allk.cons == cons]
        P(f"          {cons:12s} {int((s_.p < 0.05).sum())} of {len(s_)} below 0.05; "
          f"{int((s_.p < 0.05).sum())/len(s_):.1%} vs the 5% a null surface would give")
    return gap, NT


# --------------------------------------------------------------------------- part 3
def walkforward(G, REF):
    P("\n" + "=" * 118)
    P("PART 3 — RULE 8 WALK-FORWARD.  Arm chosen on IS <= 2016-12-31 by IS Sharpe, 2017-2026")
    P("         read once.  S0 = CANDq @ S=1.00 (do nothing).  Published as MARGIN, REGRET and")
    P("         ROOM per idea 229/445.")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        spy_o = metrics(REF[pk]["spy"].loc[OOS_START:])
        for cons in CONSTRUCTIONS:
            for cost in (PROTO, 25.0):
                lad = G[(G.panel == pk) & (G.cost == cost)
                        & ((G.cons == cons) | ((G.cons == "CANDq") & (G.S == 1.00)))].copy()
                lad["arm"] = (lad.key + "/" + lad["dir"].str[4:] + "@S" +
                              lad.S.map(lambda x: f"{x:.2f}") +
                              lad.seed.map(lambda x: "" if x < 0 else f"#{x}"))
                s0 = lad[(lad.cons == "CANDq") & (lad.S == 1.00) & (lad.key == "COMP")
                         & (lad["dir"] == "KEEPTOP")].iloc[0]
                det = lad[lad.seed == -1]
                for sel, pool in (("all-arms", lad), ("det-only", det),
                                  ("COMP-only", lad[(lad.key == "COMP")
                                                    & (lad["dir"] == "KEEPTOP")])):
                    pick = pool.loc[pool.IS_Sharpe.idxmax()]
                    best = pool.loc[pool.OOS_Sharpe.idxmax()]
                    rows.append(dict(
                        panel=pk, cons=cons, cost=cost, selector=sel, ladder=len(pool),
                        pick=pick.arm, pick_shuffled=bool(pick.key == "SHUFF"),
                        oos_argmax=best.arm, oos_argmax_shuffled=bool(best.key == "SHUFF"),
                        OOS_Sharpe_pick=pick.OOS_Sharpe, OOS_Sharpe_s0=s0.OOS_Sharpe,
                        OOS_best=best.OOS_Sharpe,
                        margin=pick.OOS_Sharpe - s0.OOS_Sharpe,
                        regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                        room=best.OOS_Sharpe - s0.OOS_Sharpe,
                        OOS_CAGR_pick=pick.OOS_CAGR, OOS_MaxDD_pick=pick.OOS_MaxDD,
                        OOS_CAGR_s0=s0.OOS_CAGR, OOS_MaxDD_s0=s0.OOS_MaxDD,
                        OOS_CAGR_spy=spy_o["CAGR"], OOS_Sharpe_spy=spy_o["Sharpe"],
                        OOS_MaxDD_spy=spy_o["MaxDD"]))
    WF = pd.DataFrame(rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  {'panel':9s} {'cons':11s} {'cost':>5s} {'selector':10s} {'IS pick':>20s} "
      f"{'OOSpick':>8s} {'OOS S0':>8s} {'MARGIN':>8s} {'REGRET':>7s} {'ROOM':>8s}")
    for r in WF.itertuples():
        P(f"  {r.panel:9s} {r.cons:11s} {r.cost:5.0f} {r.selector:10s} {r.pick:>20s} "
          f"{r.OOS_Sharpe_pick:8.3f} {r.OOS_Sharpe_s0:8.3f} {r.margin:+8.4f} "
          f"{r.regret:7.4f} {r.room:+8.4f}")
    P(f"\n      pooled by construction (all selectors, both rungs, 3 panels):")
    P(f"      {'cons':12s} {'cells':>6s} {'margin>0':>10s} {'mean MARGIN':>12s} "
      f"{'mean REGRET':>12s} {'picks a shuffled key':>22s}")
    for cons in CONSTRUCTIONS:
        w = WF[WF.cons == cons]
        P(f"      {cons:12s} {len(w):6d} {f'{int((w.margin>0).sum())}/{len(w)}':>10s} "
          f"{w.margin.mean():+12.5f} {w.regret.mean():12.5f} "
          f"{f'{int(w.pick_shuffled.sum())}/{len(w)}':>22s}")
    P(f"\n      OOS CAGR / Sharpe / MaxDD at 10 bps, honest (all-arms) chooser vs do-nothing"
      f" vs SPY:")
    for r in WF[(WF.cost == PROTO) & (WF.selector == "all-arms")].itertuples():
        P(f"      {r.panel:9s} {r.cons:11s} pick {r.OOS_CAGR_pick:7.2%}/"
          f"{r.OOS_Sharpe_pick:6.3f}/{r.OOS_MaxDD_pick:7.2%}   "
          f"S0 {r.OOS_CAGR_s0:7.2%}/{r.OOS_Sharpe_s0:6.3f}/{r.OOS_MaxDD_s0:7.2%}   "
          f"SPY {r.OOS_CAGR_spy:7.2%}/{r.OOS_Sharpe_spy:6.3f}/{r.OOS_MaxDD_spy:7.2%}")
    return WF


# --------------------------------------------------------------------------- part 4
def keep_paths(G, REF):
    P("\n" + "=" * 118)
    P("PART 4 — BOTH KEEP PATHS on every grid point (4a vs the live RULES v2; 4b vs SPY).")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        spy = REF[pk]["spy"]
        sm, so = metrics(spy), metrics(spy.loc[OOS_START:])
        sh1, sh2 = halves(spy)
        for cost in COSTS:
            v2 = net(*REF[pk]["v2"], cost)
            vm = metrics(v2)
            vh1, vh2 = halves(v2)
            sub = G[(G.panel == pk) & (G.cost == cost)]
            for r in sub.itertuples():
                f4a = (r.H1 > vh1 and r.H2 > vh2 and abs(r.MaxDD) <= abs(vm["MaxDD"]))
                fails = []
                if r.H1 <= sh1:
                    fails.append("H1")
                if r.H2 <= sh2:
                    fails.append("H2")
                if r.OOS_Sharpe <= so["Sharpe"]:
                    fails.append("OOS")
                if abs(r.MaxDD) > abs(sm["MaxDD"]) * 0.6:
                    fails.append("MaxDD")
                if r.CAGR < sm["CAGR"] * 0.7:
                    fails.append("CAGR")
                rows.append(dict(panel=pk, cons=r.cons, cost=cost, key=r.key,
                                 dir=getattr(r, "dir"),
                                 seed=r.seed, S=r.S, CAGR=r.CAGR, Sharpe=r.Sharpe,
                                 MaxDD=r.MaxDD, H1=r.H1, H2=r.H2, OOS_CAGR=r.OOS_CAGR,
                                 OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                                 keep4a=f4a, keep4b=not fails,
                                 failing="|".join(fails) or "none"))
    KP = pd.DataFrame(rows)
    KP.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {len(KP)} grid points.  4a {int(KP.keep4a.sum())}   4b {int(KP.keep4b.sum())}   "
      f"both {int((KP.keep4a & KP.keep4b).sum())}")
    P(f"\n      {'construction':12s} {'panel':9s} {'points':>7s} {'4a':>9s} {'4b':>9s}")
    for cons in CONSTRUCTIONS:
        for pk in G.panel.unique():
            g = KP[(KP.cons == cons) & (KP.panel == pk)]
            P(f"      {cons:12s} {pk:9s} {len(g):7d} "
              f"{f'{int(g.keep4a.sum())}/{len(g)}':>9s} {f'{int(g.keep4b.sum())}/{len(g)}':>9s}")
    P(f"\n      the binding 4b bar over all failing points:")
    fc = {}
    for f in KP[~KP.keep4b].failing:
        for t in f.split("|"):
            fc[t] = fc.get(t, 0) + 1
    for t, n in sorted(fc.items(), key=lambda x: -x[1]):
        P(f"          {t:7s} binds on {n:5d} points")
    P(f"\n      4b PASS RATE BY KEY FAMILY at the protocol rung — if a random key passes as")
    P(f"      often as the composite, a 4b pass is a property of the BOOK, not of the key:")
    P(f"      {'construction':12s} " + " ".join(f"{k:>9s}" for k in KEYS + ["SHUFF"]))
    for cons in CONSTRUCTIONS:
        vals = []
        for k in KEYS + ["SHUFF"]:
            g = KP[(KP.cons == cons) & (KP.cost == PROTO) & (KP.key == k)
                   & (KP["dir"] == "KEEPTOP")]
            vals.append(f"{g.keep4b.mean():9.1%}")
        P(f"      {cons:12s} " + " ".join(vals))
    dets = KP[(KP.seed == -1) & (KP.cost == PROTO) & KP.keep4b]
    P(f"\n      deterministic 4b passes at 10 bps: {len(dets)}")
    for r in dets.sort_values("Sharpe", ascending=False).head(12).itertuples():
        P(f"          {r.panel:9s} {r.cons:11s} {r.key:7s}/{getattr(r,'dir')[4:]:3s} "
          f"S={r.S:.2f}  {r.CAGR:7.2%}/{r.Sharpe:6.3f}/{r.MaxDD:7.2%}  "
          f"halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:7.2%}/{r.OOS_Sharpe:6.3f}/"
          f"{r.OOS_MaxDD:7.2%}")
    return KP


def main():
    t0 = time.time()
    P("# Idea 447 — does-the-key-swap-survive-a-CONSTANT-count")
    P(f"# cloud lane, {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}, seed {SEED}")
    P(f"# 3 constructions x 5 keys x 2 directions (+ {N_NULL}-seed persistent-random null)")
    P(f"# P1 depth S in {S_GRID}; P2 cost rung in {COSTS} bps (10 = protocol).")
    P(f"# gate: above 200d MA & vol20 < {MAX_VOL}; gross {GROSS:.0%}; weekly; t+1.")
    PANELS = build_panels()
    validate_fast(PANELS)
    G, REF = run_grid(PANELS)
    check_identity(REF, PANELS)
    check_premise(G, REF)
    curves(G)
    veto_and_null(G, REF)
    walkforward(G, REF)
    keep_paths(G, REF)
    P(f"\n\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
