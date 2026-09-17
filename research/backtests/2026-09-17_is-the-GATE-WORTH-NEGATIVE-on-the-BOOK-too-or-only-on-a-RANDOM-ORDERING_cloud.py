#!/usr/bin/env python3
"""
Idea 1096 (lane cloud, 2026-09-17) — is the GATE WORTH NEGATIVE on the BOOK too, or only on a
RANDOM ORDERING?

THE PREMISE.  Idea 1085 priced the 200d/vol gate on a RANDOMLY-ORDERED book and found it costs
0.54-1.89 pp/yr of unmatched CAGR while buying 0.9-3.3 pp of drawdown — a risk filter, not an
alpha filter.  A random ordering has no reason to interact with the gate.  THE REAL BOOK DOES:
its ranking signal is momentum, and momentum names are ALREADY mostly above their own 200d MA,
so the gate may bind on almost nothing (and be free), or bind exactly when momentum is about to
break (and be the whole risk story).  Nobody has priced it on the incumbent.  This run does,
and asks the follow-on the idea states: IS THE LIVE BOOK PAYING 1-2 pp/yr FOR DRAWDOWN IT COULD
BUY MORE CHEAPLY BY SIMPLY HOLDING LESS?

WHAT IS MEASURED, STATED BEFORE ANY NUMBER IS READ.  The frozen 2026-09-04 candidate with its
ELIGIBILITY SCREEN swapped between four values and its width walked.  At every grid point:
full-sample CAGR/Sharpe/MaxDD, both halves, OOS (2017-01-01 onward), annual turnover, MEAN NET
EXPOSURE, the 4a verdict (vs live RULES v2), the 4b verdict (vs SPY, full AND OOS) and which
4b legs fail.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    n     {5, 10, 12, 15, 20, 25, 30, 40} — book width.  20 is the committed rung.
    GATE  {BOTH, MA, VOL, NONE} — eligibility = (above own 200d MA) AND (vol20 < 0.60) / the MA
          leg alone / the vol leg alone / no screen at all.  BOTH is the committed rung.
NOT DIALS, reported at every value: PANEL {U56, B136, SMALL663} (rule 9); the EXPOSURE-MATCHED
CONTROL (see below); the 4a/4b legs; the rule-8 halves.  Frozen at the record's construction:
composite legs (21/252, 0/126, 0/63) with NO vol scaler, H = 126 minimum hold, GROSS = 0.75 of
NAV with gated-out weight to CASH, WEEKLY rebalance, 10 bps (rule 2), t+1 execution, 260-row
warm-up.

ONE DELIBERATE SIMPLIFICATION, DECLARED.  scan.py multiplies the composite by (0.5 + 0.5*above)
before ranking.  Under the committed gate that multiplier is identically 1.0 on every ELIGIBLE
name, so it is a NO-OP for the incumbent; under GATE = NONE it would smuggle the MA back in as
a soft screen and the question would no longer be asked.  This run therefore ranks on the RAW
composite at every grid point.  Gate G1 checks that (n=20, GATE=BOTH) still replays the
committed U56 triple exactly.

THE CONTROL ARMS, AND A DEFECT IN THE RECORD FOUND WHILE BUILDING THEM (rule 7).  Every memo in
this record describes the book as "gated-out weight to CASH, de-gross, never re-spread".  IT DOES
NOT.  Every committed script, this one included, sets the weight of each selected name to
1/len(selected), so the book is ALWAYS fully invested at GROSS = 0.75 whenever it holds anything:
a screen that admits only 9 names holds those 9 at 8.33% each, not at 3.75% with the rest in cash.
Mean net exposure is 0.750 at EVERY cell of the main grid and this run publishes that number at
every grid point.  THE COMMITTED GATE IS THEREFORE A PURE SELECTION FILTER AND CANNOT TIME
EXPOSURE AT ALL.  The main grid is left exactly as the record built it (the anchor still replays
the committed triple), and the missing behaviour is measured as two CONTROL arms at every n,
reported and never chosen:
    CASH*  gate = BOTH with 1/N weights and unfilled slots left in cash — the book the memos
           describe, which really does de-gross.  Its mean net exposure is published.
    MTCH*  gate = NONE at a CONSTANT gross equal to CASH*'s own mean exposure — the same average
           money at risk, bought by permanently holding less instead of by timing.  If CASH* does
           not beat MTCH*, the gate is buying drawdown at a price a constant cash allocation
           undercuts, which is the question idea 1096 asks.

PRE-DECLARED OUTCOMES, written before the tape is read:
  (A) THE GATE IS FREE ON THE BOOK — the momentum ranking already selects above-MA names, so
      GATE = NONE and GATE = BOTH differ by under 0.25 pp/yr of CAGR and under 1 pp of MaxDD at
      the committed n, and the 4b verdict is the same at both.
  (B) THE GATE IS A REAL RISK FILTER AND IT PAYS — GATE = BOTH has materially better MaxDD than
      GATE = NONE at the committed n, and CASH* also beats MTCH* on MaxDD, i.e. timing beats
      simply holding less.
  (C) THE GATE IS WORTH NEGATIVE ON THE BOOK TOO — GATE = NONE (or MTCH*) has both higher CAGR
      and no worse MaxDD at the committed n, and the live rules are paying for protection they
      are not getting.

RULE 8 (walk-forward).  (n, GATE) is CHOSEN on warm-up..2016-12-31 by IS Sharpe alone and
2017-2026 is read ONCE, per panel.  Reported against (i) the do-nothing committed (20, BOTH)
anchor, (ii) the mean over all 32 cells and (iii) the WORST cell, with the IS/OOS rank
correlation over the 32 cells.

PROTOCOL: rule 2 costs and execution; rule 8 as above; BOTH KEEP paths at every grid point;
rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL663 is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
upper bound.  The headline is a DIFFERENCE between two screens on the same book on the same
panel, first-order immune to a common level bias; the levels are not.  A current-constituent
panel is if anything KIND to GATE = NONE, since a name that fell below its 200d MA and never
came back is disproportionately a name the screen dropped from the panel — so the ungated arm's
numbers are the more optimistic of the two and any win it posts is an upper bound on its win.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-17_is-the-GATE-WORTH-NEGATIVE-on-the-BOOK-too-or-only-on-a-RANDOM-ORDERING_cloud.py
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

DATE = "2026-09-17"
SLUG = "is-the-GATE-WORTH-NEGATIVE-on-the-BOOK-too-or-only-on-a-RANDOM-ORDERING"
OUT = ROOT / "research" / "backtests"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G = 20, 126, 0.75              # the frozen 2026-09-04 book
NS = [5, 10, 12, 15, 20, 25, 30, 40]       # DIAL 1
GATESET = ["BOTH", "MA", "VOL", "NONE"]    # DIAL 2
ANCHOR = (A_N, "BOTH")
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
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
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values          # RAW composite (see docstring)
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)

    def elig(self, g):
        if g == "BOTH":
            return self.above & self.volok
        if g == "MA":
            return self.above
        if g == "VOL":
            return self.volok
        return np.ones_like(self.above, dtype=bool)


def build(pan, elig, N, H=A_H, lag=1, spread=True):
    """The frozen book's selection frame at GROSS = 1.0 under eligibility mask `elig`.
    Row t is the APPLICATION-time weight (rule 2: decided at t-lag, applied at t).

    spread=True  — SPREAD convention: 1/len(selected), so the book is ALWAYS fully invested at
                   GROSS whenever it holds anything.  THIS IS WHAT EVERY COMMITTED SCRIPT IN THE
                   RECORD ACTUALLY DOES, and what the committed triple was measured with.
    spread=False — CASH convention: 1/N per slot, unfilled slots left in CASH, so a screen that
                   admits fewer than N names DE-GROSSES the book.  This is what the record's
                   memos SAY the book does ("gated-out weight to CASH, never re-spread").  It is
                   reported here as a CONTROL, never as a chooser."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = pan.reb[i + 1] if i + 1 < len(pan.reb) else T
            W[t:stop, pan.iinv[sel]] = (1.0 / len(sel)) if spread else (1.0 / N)
    return W


def run(pan, Wt, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional.
    Returns (net daily returns, annual turnover, mean net exposure post-warm-up)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), float(held[WARMUP:].sum(axis=1).mean())


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1096 lane cloud — {SLUG}")
    say("# frozen book: composite(21/252,0/126,0/63) RAW, no vol scaler, H=126, GROSS=0.75,")
    say(f"# cash for gated-out weight, weekly, {COST:.0f} bps, t+1 execution, warm-up {WARMUP}")
    say(f"# DIAL 1 n = {NS}   DIAL 2 gate = {GATESET}   anchor = {ANCHOR}")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append(("B136", pb, [c for c in pb.columns if c != "SPY"]))
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in ps.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {ps.shape[1]-1} names, {len(bad & set(ps.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", ps, inv_s))

    rows, ctrl_rows, r8rows = [], [], []
    for name, p_px, inv in panels:
        pan = Panel(name, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {name}  n_days={len(pan.idx)}  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}, CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}, "
            f"Sharpe H1 {spy['h1']['Sharpe']:.4f} / H2 {spy['h2']['Sharpe']:.4f} / OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   mean gate-on share of panel-days: MA {pan.above[WARMUP:].mean():.4f}  "
            f"VOL {pan.volok[WARMUP:].mean():.4f}  BOTH {(pan.above & pan.volok)[WARMUP:].mean():.4f}")

        cells, expo = {}, {}
        say(f"   {'n':>3} {'gate':>5} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} | {'H1':>6} {'H2':>6} | "
            f"{'oCAGR':>7} {'oSh':>7} {'oDD':>8} | {'turn':>5} {'expo':>5} | 4a 4b  failing 4b legs")
        for n in NS:
            for g in GATESET:
                r, turn, ex = run(pan, build(pan, pan.elig(g), n))
                w = windows(idx, r[WARMUP:])
                cells[(n, g)] = w
                expo[(n, g)] = ex
                a, b = legs_4a(w, live), legs_4b(w, spy)
                fails = [k for k, v in b.items() if not v]
                rows.append(dict(panel=name, n=n, gate=g, turnover=turn, exposure=ex, gross=A_G,
                                 **flat(w), **{f"a_{k}": v for k, v in a.items()},
                                 **{f"b_{k}": v for k, v in b.items()},
                                 pass4a=all(a.values()), pass4b=all(b.values()),
                                 fail4b=",".join(fails) or "NONE"))
                mark = " <= ANCHOR" if (n, g) == ANCHOR else ""
                say(f"   {n:>3} {g:>5} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:7.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:6.4f} {w['h2']['Sharpe']:6.4f} | "
                    f"{w['oos']['CAGR']:7.2%} {w['oos']['Sharpe']:7.4f} {w['oos']['MaxDD']:8.2%} | "
                    f"{turn:5.2f} {ex:5.3f} | {int(all(a.values()))}  {int(all(b.values()))}   "
                    f"{','.join(fails) or 'NONE':<18}{mark}")

            # ---- CONTROL ARMS (reported, never chosen).  The SPREAD convention above cannot
            # de-gross, so the "more cheaply" question needs the CASH convention to exist at all.
            rC, turnC, exC = run(pan, build(pan, pan.elig("BOTH"), n, spread=False))
            wC = windows(idx, rC[WARMUP:])
            aC, bC = legs_4a(wC, live), legs_4b(wC, spy)
            # ungated, SPREAD convention, at a CONSTANT gross matched to the cash arm's mean exposure
            gm = A_G * exC / max(expo[(n, "NONE")], 1e-9)
            rM, turnM, exM = run(pan, build(pan, pan.elig("NONE"), n), gross=gm)
            wM = windows(idx, rM[WARMUP:])
            aM, bM = legs_4a(wM, live), legs_4b(wM, spy)
            both = cells[(n, "BOTH")]
            ctrl_rows.append(dict(panel=name, n=n, cash_exposure=exC, matched_gross=gm, matched_exposure=exM,
                                  cash_CAGR=wC["full"]["CAGR"], cash_Sharpe=wC["full"]["Sharpe"],
                                  cash_MaxDD=wC["full"]["MaxDD"], cash_oos_Sharpe=wC["oos"]["Sharpe"],
                                  cash_oos_CAGR=wC["oos"]["CAGR"], cash_turnover=turnC,
                                  cash_pass4a=all(aC.values()), cash_pass4b=all(bC.values()),
                                  cash_fail4b=",".join(k for k, v in bC.items() if not v) or "NONE",
                                  m_CAGR=wM["full"]["CAGR"], m_Sharpe=wM["full"]["Sharpe"],
                                  m_MaxDD=wM["full"]["MaxDD"], m_oos_Sharpe=wM["oos"]["Sharpe"],
                                  m_pass4b=all(bM.values()),
                                  d_cagr_cash_minus_matched=wC["full"]["CAGR"] - wM["full"]["CAGR"],
                                  d_mdd_cash_minus_matched=wC["full"]["MaxDD"] - wM["full"]["MaxDD"],
                                  d_sharpe_cash_minus_matched=wC["full"]["Sharpe"] - wM["full"]["Sharpe"],
                                  d_oos_sharpe_cash_minus_matched=wC["oos"]["Sharpe"] - wM["oos"]["Sharpe"],
                                  d_cagr_spread_minus_cash=both["full"]["CAGR"] - wC["full"]["CAGR"],
                                  d_mdd_spread_minus_cash=both["full"]["MaxDD"] - wC["full"]["MaxDD"]))
            say(f"   {n:>3} CASH* | {wC['full']['CAGR']:7.2%} {wC['full']['Sharpe']:7.4f} "
                f"{wC['full']['MaxDD']:8.2%} | {wC['h1']['Sharpe']:6.4f} {wC['h2']['Sharpe']:6.4f} | "
                f"{wC['oos']['CAGR']:7.2%} {wC['oos']['Sharpe']:7.4f} {wC['oos']['MaxDD']:8.2%} | "
                f"{turnC:5.2f} {exC:5.3f} | {int(all(aC.values()))}  {int(all(bC.values()))}   "
                f"CONTROL: gate BOTH, CASH convention (de-grosses)")
            say(f"   {n:>3} MTCH* | {wM['full']['CAGR']:7.2%} {wM['full']['Sharpe']:7.4f} "
                f"{wM['full']['MaxDD']:8.2%} | {wM['h1']['Sharpe']:6.4f} {wM['h2']['Sharpe']:6.4f} | "
                f"{wM['oos']['CAGR']:7.2%} {wM['oos']['Sharpe']:7.4f} {wM['oos']['MaxDD']:8.2%} | "
                f"{turnM:5.2f} {exM:5.3f} | {int(all(aM.values()))}  {int(all(bM.values()))}   "
                f"CONTROL: UNGATED at constant gross {gm:.3f} (same average money at risk as CASH*)")

        # ---- the gate's own price, at every n: BOTH minus NONE, both at GROSS = 0.75
        say(f"\n   THE GATE'S PRICE ON THE REAL BOOK (BOTH minus NONE, both at gross {A_G}):")
        say(f"   {'n':>3} | {'dCAGR':>8} {'dMaxDD':>8} {'dSharpe':>8} {'dOOSSh':>8} | "
            f"pp of CAGR paid per pp of MaxDD bought (negative = the gate is worth negative)")
        for n in NS:
            B, N0 = cells[(n, "BOTH")], cells[(n, "NONE")]
            dc = B["full"]["CAGR"] - N0["full"]["CAGR"]
            dd = B["full"]["MaxDD"] - N0["full"]["MaxDD"]           # >0 means the gate IMPROVED DD
            price = (-dc * 100.0) / (dd * 100.0) if abs(dd) > 1e-9 else float("nan")
            say(f"   {n:>3} | {dc:+8.2%} {dd:+8.2%} {B['full']['Sharpe']-N0['full']['Sharpe']:+8.4f} "
                f"{B['oos']['Sharpe']-N0['oos']['Sharpe']:+8.4f} | {price:+.3f}")

        sub = pd.DataFrame([dict(n=n, g=g, full=cells[(n, g)]["full"]["Sharpe"], is_=cells[(n, g)]["is_"]["Sharpe"],
                                 oos=cells[(n, g)]["oos"]["Sharpe"], ocg=cells[(n, g)]["oos"]["CAGR"],
                                 odd=cells[(n, g)]["oos"]["MaxDD"],
                                 p4b=all(legs_4b(cells[(n, g)], spy).values()),
                                 p4a=all(legs_4a(cells[(n, g)], live).values()))
                            for n in NS for g in GATESET])
        an = cells[ANCHOR]
        say(f"\n   GRID {name}: 4b passes {int(sub.p4b.sum())} of {len(sub)}, 4a passes {int(sub.p4a.sum())} of {len(sub)}")
        say(f"        full Sharpe {sub.full.min():.4f}..{sub.full.max():.4f}   OOS Sharpe "
            f"{sub.oos.min():.4f}..{sub.oos.max():.4f}   anchor(20/BOTH) full {an['full']['Sharpe']:.4f}, "
            f"OOS {an['oos']['Sharpe']:.4f}, MaxDD {an['full']['MaxDD']:7.2%}")
        for g in GATESET:
            s = sub[sub.g == g]
            say(f"        gate {g:>4}: 4b {int(s.p4b.sum())} of {len(s)}, full Sharpe "
                f"{s.full.min():.4f}..{s.full.max():.4f}, OOS {s.oos.min():.4f}..{s.oos.max():.4f}")

        pick = sub.loc[sub.is_.idxmax()]
        r8 = dict(panel=name, pick_n=int(pick.n), pick_gate=pick.g, is_sharpe=float(pick.is_),
                  oos_pick=float(pick.oos), oos_pick_cagr=float(pick.ocg), oos_pick_mdd=float(pick.odd),
                  oos_mean=float(sub.oos.mean()), oos_worst=float(sub.oos.min()), oos_best=float(sub.oos.max()),
                  oos_anchor=float(an["oos"]["Sharpe"]), oos_spy=float(spy["oos"]["Sharpe"]),
                  pick_pass4b=bool(pick.p4b),
                  anchor_pass4b=bool(sub[(sub.n == A_N) & (sub.g == "BOTH")].p4b.iloc[0]),
                  is_oos_rank_corr=rankcorr(sub.is_.values, sub.oos.values),
                  n_pass4b=int(sub.p4b.sum()), n_cells=len(sub))
        r8rows.append(r8)
        say(f"   RULE 8 {name}: IS argmax (n={int(pick.n)}, {pick.g}) IS Sharpe {pick.is_:.4f} -> OOS Sharpe "
            f"{pick.oos:.4f} / CAGR {pick.ocg:7.2%} / MaxDD {pick.odd:7.2%}")
        say(f"           vs grid-mean OOS {sub.oos.mean():.4f}  worst {sub.oos.min():.4f}  best {sub.oos.max():.4f}  "
            f"anchor {an['oos']['Sharpe']:.4f}  SPY {spy['oos']['Sharpe']:.4f}   "
            f"IS/OOS rank corr {r8['is_oos_rank_corr']:+.4f}")
        say(f"           IS-chosen 4b = {bool(pick.p4b)}; anchor 4b = {r8['anchor_pass4b']}; gain vs grid mean "
            f"{pick.oos - sub.oos.mean():+.4f}, vs anchor {pick.oos - an['oos']['Sharpe']:+.4f}")

    df = pd.DataFrame(rows)
    dc = pd.DataFrame(ctrl_rows)
    d8 = pd.DataFrame(r8rows)
    df.to_csv(OUT / f"{DATE}_{SLUG}_cloud.grid.csv", index=False)
    dc.to_csv(OUT / f"{DATE}_{SLUG}_cloud.control.csv", index=False)
    d8.to_csv(OUT / f"{DATE}_{SLUG}_cloud.walkforward.csv", index=False)

    # ---------------------------------------------------------------- headline
    say("\n## HEADLINE — the gate's price at the committed n = 20, per panel")
    say(f"  {'panel':9s} {'CAGR B/N':>16} {'MaxDD B/N':>16} {'Sharpe B/N':>16}  {'4b B/N':>8}  "
        f"{'vs EXPOSURE-MATCHED CTRL':>26}")
    for name in df.panel.unique():
        b = df[(df.panel == name) & (df.n == A_N) & (df.gate == "BOTH")].iloc[0]
        n0 = df[(df.panel == name) & (df.n == A_N) & (df.gate == "NONE")].iloc[0]
        c = dc[(dc.panel == name) & (dc.n == A_N)].iloc[0]
        say(f"  {name:9s} {b.full_CAGR:7.2%}/{n0.full_CAGR:7.2%} {b.full_MaxDD:7.2%}/{n0.full_MaxDD:7.2%} "
            f"{b.full_Sharpe:7.4f}/{n0.full_Sharpe:7.4f}  {int(b.pass4b)}/{int(n0.pass4b)}       "
            f"CASH arm {c.cash_CAGR:7.2%} / {c.cash_Sharpe:.4f} / {c.cash_MaxDD:7.2%} at mean exposure "
            f"{c.cash_exposure:.3f}; vs its matched ungated control dCAGR {c.d_cagr_cash_minus_matched:+.2%}, "
            f"dMaxDD {c.d_mdd_cash_minus_matched:+.2%}, dSharpe {c.d_sharpe_cash_minus_matched:+.4f}")
    say("\n## DOES THE GATE IMPROVE DRAWDOWN AT ALL (BOTH vs NONE, same gross), count over n")
    for name in df.panel.unique():
        s = df[df.panel == name]
        wins_dd = wins_cagr = wins_sh = 0
        for n in NS:
            b = s[(s.n == n) & (s.gate == "BOTH")].iloc[0]
            n0 = s[(s.n == n) & (s.gate == "NONE")].iloc[0]
            wins_dd += b.full_MaxDD > n0.full_MaxDD
            wins_cagr += b.full_CAGR > n0.full_CAGR
            wins_sh += b.full_Sharpe > n0.full_Sharpe
        say(f"  {name:9s}: gate improves MaxDD at {wins_dd} of {len(NS)} rungs, CAGR at {wins_cagr}, "
            f"Sharpe at {wins_sh}")
    say("\n## CAN THE GATE DE-GROSS AT ALL, AND IS TIMING CHEAPER THAN SIMPLY HOLDING LESS?")
    say("   (CASH* = gate BOTH, 1/N weights, unfilled slots to cash.  MTCH* = UNGATED at a CONSTANT")
    say("    gross equal to CASH*'s own mean exposure — the same average money at risk, bought by")
    say("    permanently holding less instead of by timing.)")
    for name in dc.panel.unique():
        s = dc[dc.panel == name]
        say(f"  {name:9s}: CASH* mean exposure {s.cash_exposure.min():.3f}..{s.cash_exposure.max():.3f} "
            f"(SPREAD convention is 0.750 at every rung, i.e. THE COMMITTED BOOK NEVER DE-GROSSES). "
            f"CASH* beats MTCH* on MaxDD at {int((s.d_mdd_cash_minus_matched > 0).sum())} of {len(s)} rungs, "
            f"on Sharpe at {int((s.d_sharpe_cash_minus_matched > 0).sum())}, on OOS Sharpe at "
            f"{int((s.d_oos_sharpe_cash_minus_matched > 0).sum())}; mean dCAGR "
            f"{s.d_cagr_cash_minus_matched.mean():+.2%}, mean dMaxDD {s.d_mdd_cash_minus_matched.mean():+.2%}, "
            f"mean dSharpe {s.d_sharpe_cash_minus_matched.mean():+.4f}; CASH* 4b passes "
            f"{int(s.cash_pass4b.sum())} of {len(s)}, MTCH* {int(s.m_pass4b.sum())} of {len(s)}")
    say("\n## 4b PASS MAP (rows = n, cols = gate; 1 = pass)")
    for name in df.panel.unique():
        s = df[df.panel == name]
        say(f"  {name}")
        say("      " + "".join(f"{g:>7}" for g in GATESET))
        for n in NS:
            say(f"  {n:>3} " + "".join(f"{int(s[(s.n==n)&(s.gate==g)].pass4b.iloc[0]):>7d}" for g in GATESET))
    say(f"\n  RULE 8 pooled (3 panels): IS-chosen OOS Sharpe mean {d8.oos_pick.mean():.4f} vs grid-mean "
        f"{d8.oos_mean.mean():.4f} (delta {d8.oos_pick.mean()-d8.oos_mean.mean():+.4f}) vs anchor "
        f"{d8.oos_anchor.mean():.4f} (delta {d8.oos_pick.mean()-d8.oos_anchor.mean():+.4f})")
    say(f"  RULE 8 gate chosen in sample: " + ", ".join(f"{r.panel}={r.pick_gate}@n{r.pick_n}" for r in d8.itertuples()))

    # ---------------------------------------------------------------- gates
    u = df[df.panel == "U56"]
    an = u[(u.n == A_N) & (u.gate == "BOTH")].iloc[0]
    dev = max(abs(an.full_Sharpe - 1.1480), abs(an.full_MaxDD - (-0.1913)), abs(an.oos_Sharpe - 1.1759))
    gate("G1 anchor replays committed U56 triple", f"{dev:.2e}", "< 5e-3", dev < 5e-3)
    gate("G2 grid complete", len(df), 3 * len(NS) * len(GATESET), len(df) == 3 * 32)
    gate("G3 control rows (CASH* and MTCH* per rung)", len(dc), 3 * len(NS), len(dc) == 24)
    gate("G4 rule-8 rows", len(d8), 3, len(d8) == 3)
    gate("G5 no NaN in headline stats", int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()), 0,
         int(df[["full_Sharpe", "oos_Sharpe"]].isna().sum().sum()) == 0)
    gate("G6 SPREAD convention is fully invested at every U56 cell (min mean exposure)",
         f"{float(u.exposure.min()):.4f}", "~0.75", abs(float(u.exposure.min()) - 0.75) < 0.02)
    cu = dc[(dc.panel == "U56") & (dc.n == A_N)].iloc[0]
    gate("G7 CASH control really de-grosses (U56 n=20 mean exposure)",
         f"{float(cu.cash_exposure):.4f}", "< 0.75", float(cu.cash_exposure) < 0.75)
    gate("G8 matched control holds the same average money at risk (|exposure gap|)",
         f"{abs(float(cu.matched_exposure)-float(cu.cash_exposure)):.4f}", "< 0.02",
         abs(float(cu.matched_exposure) - float(cu.cash_exposure)) < 0.02)
    gate("G9 costs = 10 bps", COST, 10.0, COST == 10.0)
    gate("G10 OOS split date", str(OOS_START.date()), "2017-01-01", True)
    gate("G11 SMALL drops max_1d_move >= 1.0 before anything", len(bad), ">0", len(bad) > 0)
    pan0 = Panel("U56rep", panels[0][1], panels[0][2])
    rep, _, _ = run(pan0, build(pan0, pan0.elig("BOTH"), A_N))
    d2 = abs(sharpe(rep[WARMUP:]) - float(an.full_Sharpe))
    gate("G12 deterministic re-run (U56 anchor Sharpe dev)", f"{d2:.3e}", "0.0", d2 == 0.0)
    g = pd.DataFrame(GATES)
    say("\n## GATES")
    say(g.to_string(index=False))
    say(f"\n{int(g.pass_.sum())} of {len(g)} gates pass; {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
