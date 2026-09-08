#!/usr/bin/env python3
"""Idea 227 — is-the-top-decile-trim-a-drop-the-worst-rule   (cloud lane, 2026-09-08)

QUESTION (queue, verbatim intent)
    Idea 155's only surviving edge is q = 0.90-0.95, i.e. deleting the bottom 5-10% of the
    eligible set, worth +0.0316 / +0.0171 Sharpe.  Test whether that is the composite RANKING
    at all: replace the composite with each of its three legs and with a pure vol20 screen at
    the same trim depth, and report whether the trim survives when the ranking key is DESTROYED
    (shuffled within week).

WHAT THIS RUN DOES
    Idea 155's book, imported in construction (not re-invented):  eligible = above the 200d MA
    AND vol20 < 0.60, masked to the tradable set; rank the eligible names by a KEY; hold the top
    round(q * n_elig) equally weighted at 75% gross; weekly, t+1 execution, 260-bar warm-up
    skip.  q = 1.00 is the ladder's own exact EWall endpoint and is the DO-NOTHING arm: at
    q = 1.00 every key holds the identical book, so the premium curve of every key starts from
    the same point by construction.

    EIGHT keys, all pre-registered, none tuned:
        COMP      the composite of idea 155 / scan.py, no vol tilt: mean of the pct-ranks of
                  12-1 momentum, 6m return and 3m return.  THE INCUMBENT.
        MOM       the 12-1 momentum leg alone
        R6        the 6-month return leg alone
        R3        the 3-month return leg alone
        VOL20     a pure low-volatility screen: keep the LOWEST-vol20 names (no return content)
        COMP-REV  the composite REVERSED — keep the names COMP would delete.  The sign test.
        SHUF-W    the key DESTROYED: a fresh uniform draw at every rebalance (8 seeds).  This
                  null pays the turnover of a random book.
        SHUF-S    the key destroyed but STICKY: one uniform draw per NAME, constant over time
                  (8 seeds), so the null's turnover is the eligibility churn alone.  This is
                  the TURNOVER-MATCHED null and is the one the verdict turns on.

    The cost identity net(c) = gross - turnover * c / 1e4 (idea 155, verified here to < 1e-12)
    is used so every rung is read off ONE 0-bps backtest per book.  0 bps is carried as a
    DIAGNOSTIC (pure composition, no turnover handicap); 10 bps is the protocol rung and the
    only one KEEP verdicts are read at; 25 bps is the robustness axis.

    Rule 8 (PROTOCOL 8) is run on every panel: the (key, q) pair is chosen on IS <= 2016-12-31
    by IS Sharpe and 2017-2026 is read once, against the do-nothing arm (q = 1.00), RULES v2,
    RULES v1 and SPY.  Following idea 445 (committed earlier today) the selection result is
    published as ROOM and REGRET beside the margin, not as the margin alone.

TUNED PARAMETERS (exactly two; every grid point reported)
    P1  trim depth q in {0.75, 0.80, 0.85, 0.90, 0.95, 1.00}  — idea 155's top-decile region
        plus one rung below it, with 1.00 as the do-nothing endpoint.
    P2  cost rung in {0, 10, 25} bps.
    The keys are pre-registered treatment arms, not tuned; the 8 shuffle seeds are a null
    DISTRIBUTION, reported as mean +/- sd and as a share of draws beating the incumbent, never
    as a best draw.  Panels, gate, 75% gross, weekly cadence, t+1 execution and the composite
    are idea 155's committed conventions.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    R1  The STICKY null (turnover-matched random key) will show a POSITIVE trim premium too:
        dropping ~10% of an equally weighted eligible set is partly a concentration/exposure
        effect that has nothing to do with the key.
    R2  COMP's premium will not be the largest: at least one leg (R3 or R6) matches or beats it,
        so the edge is not the composite.
    R3  VOL20 will beat every return key on Sharpe — the record keeps finding (idea 330) that
        its Sharpe edges are volatility terms over negative return terms.
    R4  COMP-REV will be negative, but by LESS than COMP is positive; the asymmetry is the share
        of the effect that is exposure rather than ranking.
    R5  No 4b KEEP survives rule 8 on any panel.

CONFOUNDS / CAVEATS declared up front
    * q < 1 changes the NUMBER of names held as well as which ones, so every trim is partly a
      concentration effect.  The STICKY null is the control for exactly that and is reported
      beside every key; the WEEKLY null additionally shows what the same trim costs in turnover
      when the key carries no information.
    * VOL20 is a screen on a quantity that is already in the eligibility gate (vol20 < 0.60), so
      it trims within an already vol-capped set; it is not an independent volatility book.
    * Premiums are differences of Sharpe ratios on overlapping samples and are not independent
      across q; no significance is claimed from the ladder's shape, only from the null.
    * SMALL439 is a CURRENT-CONSTITUENTS panel (data/SMALL_PANEL_README.md) with tickers whose
      max_1d_move >= 1.0 in data/small_meta.csv dropped first.  SURVIVORSHIP BIAS — used as a
      shape check, never as a tradable return.
    * 10 bps is the protocol rung and the only rung KEEP is read at.

Deterministic (seed 227000), standalone, no network.
Writes .console.txt .grid.csv .curve.csv .null.csv .walkforward.csv .keep.csv .result.md
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
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, metrics                                            # noqa: E402

STEM = "2026-09-08_is-the-top-decile-trim-a-drop-the-worst-rule_cloud"
OUT = ROOT / "research" / "backtests"
SEED = 227000
IS_END, OOS_START = "2016-12-31", "2017-01-01"

FREQ, MAX_VOL, GROSS = "W", 0.60, 0.75
Q_GRID = [0.75, 0.80, 0.85, 0.90, 0.95, 1.00]          # P1
COSTS = [0.0, 10.0, 25.0]                              # P2 (10 = protocol rung)
N_SEEDS = 8
DET_KEYS = ["COMP", "MOM", "R6", "R3", "VOL20", "COMP-REV"]
NULL_KEYS = ["SHUF-W", "SHUF-S"]

pd.set_option("display.width", 250)
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# --------------------------------------------------------------------------- panels
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


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def key_frames(px, tradable):
    """Every ranking key, masked to the eligible set.  Higher value = KEPT first."""
    elig = eligible_mask(px, tradable)
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
            + r3.rank(axis=1, pct=True)) / 3
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    K = {"COMP": comp, "MOM": mom, "R6": r6, "R3": r3,
         "VOL20": -vol20,                      # keep the LOWEST vol
         "COMP-REV": -comp}
    rng = np.random.default_rng(SEED)
    for s in range(N_SEEDS):
        K[f"SHUF-W::{s}"] = pd.DataFrame(
            rng.random(px.shape), index=px.index, columns=px.columns)
        draw = rng.random(px.shape[1])
        K[f"SHUF-S::{s}"] = pd.DataFrame(
            np.tile(draw, (len(px), 1)), index=px.index, columns=px.columns)
    out = {}
    for name, k in K.items():
        kk = k.where(elig)
        # a name that passes the gate but has no defined key cannot be ranked at ANY q, so it
        # leaves the eligible set here too — idea 155's convention, which is what makes
        # q = 1.00 the ladder's exact EWall endpoint.
        out[name] = (elig & kk.notna(), kk.rank(axis=1, ascending=False))
    return out


def weights_q(px, elig, rank, q):
    n_elig = elig.sum(axis=1)
    n_t = np.clip(np.round(q * n_elig.values), 1, np.maximum(n_elig.values, 1))
    sel = rank.le(pd.Series(n_t, index=px.index), axis=0) & elig
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def run_book(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(r0, tno, c):
    return r0 - tno * c / 1e4


def csdm(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# --------------------------------------------------------------------------- main grid
def run_grid(PANELS):
    rows, REF = [], {}
    t0 = time.time()
    for pk, (px, tradable, desc) in PANELS.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        v1 = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        REF[pk] = dict(px=px, start=start, spy=spy,
                       v2=(v2["returns"].loc[start:], v2["turnover"].loc[start:]),
                       v1=(v1["returns"].loc[start:], v1["turnover"].loc[start:]), desc=desc)
        cg, sh, dd = csdm(spy)
        oc, osh, odd = csdm(spy.loc[OOS_START:])
        P(f"\n  [panel] {pk} = {desc}: {px.shape[1]} cols, eval {start.date()} -> "
          f"{px.index[-1].date()}")
        P(f"      SPY {cg:.2%}/{sh:.3f}/{dd:.2%} | OOS {oc:.2%}/{osh:.3f}/{odd:.2%}")
        for c in (10.0, 25.0):
            a, b, d_ = csdm(net(*REF[pk]["v2"], c))
            e, f_, g_ = csdm(net(*REF[pk]["v1"], c))
            P(f"      RULES v2 @{c:.0f}bps {a:.2%}/{b:.3f}/{d_:.2%}   "
              f"RULES v1 @{c:.0f}bps {e:.2%}/{f_:.3f}/{g_:.2%}")
        KF = key_frames(px, tradable)
        n_books = 0
        for kname, (elig, rank) in KF.items():
            for q in Q_GRID:
                w = weights_q(px, elig, rank, q)
                r0, tno = run_book(px, w, start)
                n_books += 1
                base_key = kname.split("::")[0]
                seed = int(kname.split("::")[1]) if "::" in kname else -1
                for c in COSTS:
                    r = net(r0, tno, c)
                    cg2, sh2, dd2 = csdm(r)
                    h1, h2 = halves(r)
                    oc2, osh2, odd2 = csdm(r.loc[OOS_START:])
                    rows.append(dict(
                        panel=pk, key=base_key, seed=seed, q=q, cost=c,
                        n_names=float((w > 0).sum(axis=1).replace(0, np.nan).mean()),
                        turnover=float(tno.mean() * 52),
                        CAGR=cg2, Sharpe=sh2, MaxDD=dd2, H1=h1, H2=h2,
                        IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                        OOS_CAGR=oc2, OOS_Sharpe=osh2, OOS_MaxDD=odd2))
        P(f"      {n_books} books done ({time.time()-t0:.0f}s cum.)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    return G, REF


def check_identity(REF, PANELS):
    P("\n  pre-check: cost identity net(c) = gross - turnover * c / 1e4")
    worst = 0.0
    for pk, (px, tradable, _) in PANELS.items():
        start = REF[pk]["start"]
        elig, rank = key_frames(px, tradable)["COMP"]
        w = weights_q(px, elig, rank, 0.90)
        r0, tno = run_book(px, w, start)
        direct = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        worst = max(worst, float((direct - net(r0, tno, 10.0)).abs().max()))
    P(f"      max |direct 10-bps backtest - net(gross, turnover, 10)| over 3 panels = "
      f"{worst:.3e}   (must be < 1e-12)")
    return worst


# --------------------------------------------------------------------------- the curves
def curves(G):
    P("\n" + "=" * 118)
    P("PART 1 — THE PREMIUM CURVE PER KEY.  Premium = Sharpe(q) - Sharpe(q=1.00), where q=1.00")
    P("         is the same book for every key (the ladder's own EWall endpoint).")
    P("=" * 118)
    out = []
    for (pk, cost), g in G.groupby(["panel", "cost"]):
        base = g[(g.q == 1.00) & (g.key == "COMP")].Sharpe.iloc[0]
        for (k, q), gg in g.groupby(["key", "q"]):
            out.append(dict(panel=pk, cost=cost, key=k, q=q,
                            Sharpe=gg.Sharpe.mean(), Sharpe_sd=gg.Sharpe.std(ddof=1),
                            premium=gg.Sharpe.mean() - base,
                            premium_sd=gg.Sharpe.std(ddof=1),
                            n_draws=len(gg), base=base,
                            CAGR=gg.CAGR.mean(), MaxDD=gg.MaxDD.mean(),
                            turnover=gg.turnover.mean(), n_names=gg.n_names.mean(),
                            OOS_Sharpe=gg.OOS_Sharpe.mean()))
    CV = pd.DataFrame(out)
    CV.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    for pk in G.panel.unique():
        for cost in COSTS:
            sub = CV[(CV.panel == pk) & (CV.cost == cost)]
            b = sub.base.iloc[0]
            P(f"\n  {pk} @ {cost:.0f} bps   (q=1.00 EWall Sharpe {b:.4f})")
            P(f"      {'key':9s} " + " ".join(f"{q:>8.2f}" for q in Q_GRID) + "   turnover@0.90")
            for k in DET_KEYS + NULL_KEYS:
                r = sub[sub.key == k].set_index("q").reindex(Q_GRID)
                tno = float(r.loc[0.90, "turnover"])
                line = f"      {k:9s} " + " ".join(f"{v:+8.4f}" for v in r.premium.values)
                if k in NULL_KEYS:
                    line += f"   {tno:6.2f}x  (null: mean of {int(r.n_draws.iloc[0])} seeds)"
                else:
                    line += f"   {tno:6.2f}x"
                P(line)
    return CV


def null_test(G, CV):
    P("\n" + "=" * 118)
    P("PART 2 — DOES THE TRIM SURVIVE THE KEY BEING DESTROYED?  Each deterministic key's")
    P("         premium against the 8-seed null DISTRIBUTION at the same q, same panel, same")
    P("         rung.  SHUF-S is the turnover-matched null and is the one that decides.")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        for cost in COSTS:
            for q in Q_GRID:
                if q == 1.00:
                    continue
                base = G[(G.panel == pk) & (G.cost == cost) & (G.q == 1.00)
                         & (G.key == "COMP")].Sharpe.iloc[0]
                for nk in NULL_KEYS:
                    nd = G[(G.panel == pk) & (G.cost == cost) & (G.q == q)
                           & (G.key == nk)].Sharpe.values - base
                    for k in DET_KEYS:
                        v = G[(G.panel == pk) & (G.cost == cost) & (G.q == q)
                              & (G.key == k)].Sharpe.iloc[0] - base
                        rows.append(dict(panel=pk, cost=cost, q=q, key=k, null=nk,
                                         premium=v, null_mean=nd.mean(),
                                         null_sd=nd.std(ddof=1),
                                         excess=v - nd.mean(),
                                         z=(v - nd.mean()) / nd.std(ddof=1)
                                         if nd.std(ddof=1) > 0 else np.nan,
                                         null_beats=float((nd >= v).mean())))
    NT = pd.DataFrame(rows)
    NT.to_csv(OUT / f"{STEM}.null.csv", index=False)
    P(f"\n  (a) The two nulls' OWN premium — what a MEANINGLESS key earns at the same trim:")
    P(f"      {'panel':9s} {'cost':>5s} {'null':7s} " +
      " ".join(f"{q:>9.2f}" for q in Q_GRID[:-1]))
    for pk in G.panel.unique():
        for cost in COSTS:
            for nk in NULL_KEYS:
                r = CV[(CV.panel == pk) & (CV.cost == cost)
                       & (CV.key == nk)].set_index("q").reindex(Q_GRID[:-1])
                P(f"      {pk:9s} {cost:5.0f} {nk:7s} " +
                  " ".join(f"{v:+9.4f}" for v in r.premium.values))
    P(f"\n  (b) EXCESS over the turnover-matched null (SHUF-S), protocol rung 10 bps.")
    P(f"      Positive = the KEY adds something the same trim with a random key does not.")
    sub = NT[(NT.null == "SHUF-S") & (NT.cost == 10.0)]
    P(f"      {'panel':9s} {'key':9s} " + " ".join(f"{q:>9.2f}" for q in Q_GRID[:-1])
      + "   mean z")
    for pk in G.panel.unique():
        for k in DET_KEYS:
            r = sub[(sub.panel == pk) & (sub.key == k)].set_index("q").reindex(Q_GRID[:-1])
            P(f"      {pk:9s} {k:9s} " + " ".join(f"{v:+9.4f}" for v in r.excess.values)
              + f"   {r.z.mean():+6.2f}")
    P(f"\n  (c) The idea-155 cells re-read: U56 q=0.90 and B136 q=0.95 at 10 bps.")
    for pk, q, pub in (("U56", 0.90, 0.0316), ("B136", 0.95, 0.0171)):
        c = NT[(NT.panel == pk) & (NT.q == q) & (NT.cost == 10.0) & (NT.key == "COMP")]
        if not len(c):
            continue
        s = c[c.null == "SHUF-S"].iloc[0]
        w = c[c.null == "SHUF-W"].iloc[0]
        P(f"      {pk} q={q:.2f}: idea 155 published COMP premium {pub:+.4f}; this run "
          f"{s.premium:+.4f}")
        P(f"          turnover-matched null SHUF-S {s.null_mean:+.4f} +/- {s.null_sd:.4f} "
          f"-> EXCESS {s.excess:+.4f} (z {s.z:+.2f}, {s.null_beats:.0%} of 8 random keys "
          f"beat COMP)")
        P(f"          weekly-redraw null SHUF-W  {w.null_mean:+.4f} +/- {w.null_sd:.4f} "
          f"-> excess {w.excess:+.4f}")
    return NT


# --------------------------------------------------------------------------- rule 8
def walkforward(G, REF):
    P("\n" + "=" * 118)
    P("PART 3 — RULE 8 WALK-FORWARD.  (key, q) chosen on IS <= 2016-12-31 by IS Sharpe;")
    P("         2017-2026 read once.  Published as ROOM and REGRET beside the margin, per the")
    P("         clause idea 445 drafted earlier today.")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        for cost in (10.0, 25.0):
            lad = G[(G.panel == pk) & (G.cost == cost) & (G.seed == -1)].copy()
            lad["arm"] = lad.key + "@" + lad.q.map(lambda x: f"{x:.2f}")
            s0 = lad[(lad.key == "COMP") & (lad.q == 1.00)].iloc[0]        # do nothing = EWall
            pick = lad.loc[lad.IS_Sharpe.idxmax()]
            best = lad.loc[lad.OOS_Sharpe.idxmax()]
            spy_o = metrics(REF[pk]["spy"].loc[OOS_START:])
            rows.append(dict(
                panel=pk, cost=cost, ladder_len=len(lad), pick=pick.arm, s0=s0.arm,
                oos_argmax=best.arm,
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
    P(f"\n  {'panel':9s} {'cost':>5s} {'IS pick':>14s} {'OOS pick':>9s} {'OOS S0':>8s} "
      f"{'MARGIN':>8s} {'OOS best':>9s} {'REGRET':>8s} {'ROOM':>8s} {'OOS argmax':>14s}")
    for r in WF.itertuples():
        P(f"  {r.panel:9s} {r.cost:5.0f} {r.pick:>14s} {r.OOS_Sharpe_pick:9.3f} "
          f"{r.OOS_Sharpe_s0:8.3f} {r.margin:+8.4f} {r.OOS_best:9.3f} {r.regret:8.4f} "
          f"{r.room:+8.4f} {r.oos_argmax:>14s}")
    P(f"\n      pooled over {len(WF)} cells: MARGIN {WF.margin.mean():+.5f}, "
      f"REGRET {WF.regret.mean():.5f}, ROOM {WF.room.mean():+.5f}; the chooser beats "
      f"do-nothing in {int((WF.margin>0).sum())} of {len(WF)}")
    P(f"\n      OOS CAGR / Sharpe / MaxDD, chooser vs do-nothing vs SPY:")
    for r in WF.itertuples():
        P(f"      {r.panel:9s} @{r.cost:.0f}bps  pick {r.OOS_CAGR_pick:7.2%}/"
          f"{r.OOS_Sharpe_pick:6.3f}/{r.OOS_MaxDD_pick:7.2%}   "
          f"S0 {r.OOS_CAGR_s0:7.2%}/{r.OOS_Sharpe_s0:6.3f}/{r.OOS_MaxDD_s0:7.2%}   "
          f"SPY {r.OOS_CAGR_spy:7.2%}/{r.OOS_Sharpe_spy:6.3f}/{r.OOS_MaxDD_spy:7.2%}")
    return WF


def keep_paths(G, REF):
    P("\n" + "=" * 118)
    P("PART 4 — BOTH KEEP PATHS on every deterministic cell (4a vs live RULES v2; 4b vs SPY).")
    P("=" * 118)
    rows = []
    for pk in G.panel.unique():
        spy = REF[pk]["spy"]
        sm, so = metrics(spy), metrics(spy.loc[OOS_START:])
        sh1, sh2 = halves(spy)
        for cost in (10.0, 25.0):
            v2 = net(*REF[pk]["v2"], cost)
            vm, vh1, vh2 = metrics(v2), *halves(v2)
            sub = G[(G.panel == pk) & (G.cost == cost) & (G.seed == -1)]
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
                rows.append(dict(panel=pk, cost=cost, key=r.key, q=r.q, CAGR=r.CAGR,
                                 Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                                 OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                 OOS_MaxDD=r.OOS_MaxDD, keep4a=f4a, keep4b=not fails,
                                 failing="|".join(fails) or "none"))
    KP = pd.DataFrame(rows)
    KP.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {len(KP)} deterministic cells (3 panels x 6 keys x 6 q x 2 rungs).")
    P(f"      4a (vs live RULES v2): {int(KP.keep4a.sum())} of {len(KP)}")
    P(f"      4b (vs SPY):           {int(KP.keep4b.sum())} of {len(KP)}")
    P(f"      both:                  {int((KP.keep4a & KP.keep4b).sum())}")
    P(f"\n      by panel:")
    for pk, g in KP.groupby("panel"):
        P(f"          {pk:9s} 4a {int(g.keep4a.sum()):3d}/{len(g)}   "
          f"4b {int(g.keep4b.sum()):3d}/{len(g)}")
    P(f"\n      the binding 4b bar, counted over all failing cells:")
    fc = {}
    for f in KP[~KP.keep4b].failing:
        for t in f.split("|"):
            fc[t] = fc.get(t, 0) + 1
    for t, n in sorted(fc.items(), key=lambda x: -x[1]):
        P(f"          {t:7s} binds on {n:4d} cells")
    if KP.keep4b.any():
        P(f"\n      4b-passing cells at the protocol rung:")
        for r in KP[KP.keep4b & (KP.cost == 10.0)].itertuples():
            P(f"          {r.panel:9s} {r.key:9s} q={r.q:.2f}  {r.CAGR:7.2%}/{r.Sharpe:6.3f}/"
              f"{r.MaxDD:7.2%}  halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_CAGR:7.2%}/"
              f"{r.OOS_Sharpe:6.3f}/{r.OOS_MaxDD:7.2%}")
    return KP


def main():
    t0 = time.time()
    P("# Idea 227 — is-the-top-decile-trim-a-drop-the-worst-rule")
    P(f"# cloud lane, {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())}, seed {SEED}")
    P(f"# idea 155's book: eligible = above 200d MA & vol20 < {MAX_VOL}, top round(q*n_elig)")
    P(f"# equal weight at {GROSS:.0%} gross, weekly, t+1.  P1 q in {Q_GRID}; "
      f"P2 cost in {COSTS} bps.")
    P(f"# 8 keys ({', '.join(DET_KEYS)}, {', '.join(NULL_KEYS)} x {N_SEEDS} seeds).")
    PANELS = build_panels()
    G, REF = run_grid(PANELS)
    check_identity(REF, PANELS)
    CV = curves(G)
    NT = null_test(G, CV)
    WF = walkforward(G, REF)
    KP = keep_paths(G, REF)
    P(f"\n\n[done in {time.time()-t0:.0f}s]")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
