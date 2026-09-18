#!/usr/bin/env python3
"""Idea 1271 (lane cloud, 2026-09-18): does a PER-NAME TRAILING STOP buy the DD LEG more cheaply
than PORTFOLIO-LEVEL DE-GROSSING?

THE PREMISE, AND WHY THIS AXIS IS DIFFERENT FROM EVERY ONE ALREADY PRICED.  Nine dials on the
standing 2026-09-04 KEEP 4b book — rebalance phase (1253), calendar years (1254), ex-post winner
names (1255), the signal (1257), sector caps (1258), an explicit drawdown brake (1262),
portfolio vol targeting (1263), inverse-vol slot sizing (1264), the idle sleeve (1268), a
defensive rotation (1267) and this morning's correlation brake (1266) — land on one sentence:
every other 4b leg passes at essentially every grid point, the DRAWDOWN CAP is the only leg that
ever fails, and EVERY mechanism tried so far pays for drawdown WITH EXPOSURE, which is why a flat
gross cut at the same mean exposure reproduces all of them (1266: the correlation brake's OOS
Sharpe beats its own flat control at 3 of 96 cells).

A PER-NAME TRAILING STOP IS THE ONE UNTESTED MECHANISM THAT IS NOT AN EXPOSURE CUT.  It removes
the LOSING NAME and REFILLS its slot from the same eligible pool by the same ranking rule, so
realised gross is unchanged by construction (gate G4 proves it rather than assuming it).  If the
drawdown is carried by specific names rather than by the book's aggregate exposure, this is the
only cut that can show it; if it is not, the stop must fail against controls that churn the book
at the same rate for no reason at all.

PRIOR ART, CITED AND NOT RE-RUN.  Idea 9 (2026-09-04) KILLED the trailing stop as a source of
Sharpe on RULES v1, top20 and ew-band3: it fires 0.4x/yr on v1 (whose vol scaler selects low-vol
names), and where it bites it lost in 22 of 22 arms on universe.json.  It also called the stop
"the cheapest drawdown instrument the project has measured".  What idea 9 never did: run it on
the STANDING 4b BOOK (N=20, H=126 minimum hold, RAW 3-leg composite, gross 0.75), dose-match it
against a RANDOM-EXPULSION placebo, or read rule 8 on this anchor.  The binding leg today is the
DD cap, so the cheapest DD instrument on record has to be priced on the book that needs it.  This
run does not re-open idea 9's verdict on v1; it asks the 2026 question on the 2026 book.

THE MECHANISM, EXACTLY.  For every CORE name the book holds, track its running maximum close
since the date it ENTERED the book.  At each weekly decision close t-1:

    stopped(c)  <=>  STOP > 0  and  px[t-1, c] <= (1 - STOP) * max(px[entry(c) .. t-1, c])

A stopped name is expelled at the next rebalance and its slot is refilled from the eligible pool
by the book's own ranking.  THE STOP OVERRIDES THE H=126 MINIMUM HOLD — stated plainly because it
is the only reading under which the mechanism has a dose at all: 1066/1267 established that the
min hold freezes the book through exactly the weeks a drawdown is made, so a stop that yields to
it would be measuring the min hold, not the stop.  A stopped name then sits out a COOLDOWN before
it may be re-selected.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    STOP   {0.00, 0.05, 0.10, 0.15, 0.20, 0.30} — trailing stop depth from the name's own running
           max since entry.  STOP = 0.00 IS EXACTLY THE COMMITTED ANCHOR and is in the grid so
           the do-nothing control is MEASURED, not assumed.
    COOL   {0, 21, 63, 126} trading days — the re-entry cooldown before a stopped name may be
           picked again.  COOL = 0 means it may return at the same rebalance if it still ranks.
  6 x 4 = 24 cells per (panel, arm).  EVERY ONE PUBLISHED in the .grid.csv.

THE COMPARAND THE TITLE NAMES: THE DE-GROSSING FRONTIER.  The same anchor book, no stop, held at
GROSS {0.75, 0.65, 0.55, 0.45, 0.35, 0.25} — six points, no dial, chosen on nothing.  Each point
gives a (MaxDD, CAGR) pair, and together they are the EXCHANGE RATE at which this book's own
drawdown is for sale by the cheapest known means.  A stop cell is CHEAPER THAN DE-GROSSING only if
it sits ABOVE that frontier: more CAGR than the flat gross cut that reaches the SAME MaxDD, read
by linear interpolation along the frontier.  That comparison, not the anchor, answers the title.

THE TWO DOSE-MATCHED CONTROL ARMS, neither of them a dial, both reported at every cell.  The
record has established (931) that churn alone is worth a turnover rebate, so "the stop helped"
means nothing until the same amount of churn with no drawdown input is differenced out:
    RANDOM     expel the SAME NUMBER of held names at the SAME rebalances, chosen uniformly at
               random from the book (3 fixed seeds).  This is the pure-churn control and
               STOP minus RANDOM is the number this run is actually about.
    WORSTRANK  expel the same number at the same rebalances, choosing the held names with the
               WORST CURRENT COMPOSITE RANK.  The sign test: is it the name's DRAWDOWN that
               matters, or merely dropping whatever currently scores worst?
Dose is matched by COUNT and by WEEK, not by identity — the three arms' books diverge after the
first expulsion, as they must.  The per-rebalance expulsion counts are taken from the STOP arm.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA AND
vol20 < 0.60; RAW three-leg composite (21/252, 0/126, 0/63 percentile ranks); N = 20 slots;
H = 126 minimum hold on names the stop does not take; GROSS = 0.75; WEEKLY decide-Friday /
trade-Monday; 10 bps per unit turnover; t+1 execution; 260-row warm-up; equal 1/len(held) slots
(the committed RESPREAD fill).  ONE SIGNAL ONLY (the committed COMPOSITE3): 1257 already priced
the signal axis and it is not this run's dial.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — the stop barely fires on this book (idea 9's v1 result transferring), MaxDD moves
      less than 0.20pp at every cell.  Then the DD leg is not a per-name object at all.
  (B) THE DD LEG IS BOUGHT AT CONSTANT EXPOSURE — some cell materially improves MaxDD, holds
      4b's CAGR floor and both half-Sharpe legs, BEATS ITS OWN RANDOM ARM at the same dose, and
      rule 8 reaches it.  KEEP-candidate memo with exact RULES wording.
  (C) BOUGHT BY CHURN, NOT BY THE STOP — MaxDD improves but RANDOM at the same dose does as well
      or better, i.e. the drawdown input is decorative.
  (D) WORSE — whipsaw: the stop sells the bottom and the book buys back higher, so both drawdown
      and Sharpe degrade against doing nothing (idea 9's finding, transferred to this book).
  Not mutually exclusive across panels; whichever fire are reported as they fall, and the capital
  verdict follows rule 8, never the best cell.

RULE 8 (walk-forward, required).  (STOP, COOL) is CHOSEN on warm-up..2016-12-31 by IS Sharpe
ALONE and 2017-2026 is read ONCE, per (panel, arm).  Reported against the do-nothing STOP = 0.00
cell, the cell mean, the worst cell, and the IS/OOS rank correlation over the 24 cells.  The
capital verdict is the sign of chooser-minus-do-nothing.

GATES.  G1 vintage-pinned replay truncated at 2026-09-16: U56 STOP 0.00 must replay the committed
15.7147% / 1.1480 / -19.1276% to 1e-4.  G2 STOP 0.00 is bit-identical at every COOL and in all
three arms (nothing is expelled, so nothing may differ).  G3 the mechanism has a DOSE: stop-out
counts and the share of rebalances with an expulsion are published per panel and must be > 0
somewhere, or outcome (A) is declared on the spot.  G4 THE STOP IS NOT AN EXPOSURE CUT: realised mean gross at every
cell equals the anchor's, and no cell's drifted gross exceeds the anchor's own.  [THIS GATE WAS
FIRST WRITTEN AS "drifted gross <= 0.75" AND FAILED ON ALL THREE PANELS; the diagnosis is that the
COMMITTED ANCHOR ITSELF drifts to 0.7674 on U56 because held weights drift between weekly
rebalances, so the bar was wrong, not the book.  The original wording, its failure and the fix are
published rather than quietly re-specified; the braked cells in fact drift LESS than the anchor.]  G5 CAUSALITY: the stop flag at decision i recomputed from prices TRUNCATED at i is
bit-identical to the full-sample flag.  G6 MONOTONE DOSE: the stop-out count is non-increasing in
STOP depth at fixed COOL.  G7 the RANDOM and WORSTRANK arms expel exactly min(the STOP arm's
count, what they hold) at each rebalance — the dose match is verified, not asserted.  [ALSO
CORRECTED MID-RUN: first written as "exactly the STOP arm's count", which failed at |d| = 2 on U56
because a control arm's book had drifted to fewer names than the dose asked for — the legal case
the gate's own prose already named and its code did not.]  G8
determinism: the U56 grid recomputed bit for bit.  G9 the one-extra-day cache drift against the
pinned vintage, published not toleranced.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is
computed).  Every absolute level is optimistic and every 4b pass an UPPER bound.  The headline is
a DIFFERENCE between expulsion rules applied to the SAME book on the SAME panel at the SAME dose,
which is first-order immune to a level bias moving all cells together.  One direction is NOT
neutral and is stated: a current-constituent panel has had its permanent losers removed in
advance, so a trailing stop — whose whole job is to cut names that keep falling — is measured
here on a tape where the worst thing a name can do is fall and then recover.  That flatters the
DO-NOTHING arm and understates the stop; any KILL reported here is therefore conservative, and
any WIN would need re-testing on a delisting-complete panel before capital.

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
SLUG = "does-a-PER-NAME-TRAILING-STOP-buy-the-DD-LEG-more-cheaply-than-PORTFOLIO-DE-GROSSING"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
STOPS = [0.00, 0.05, 0.10, 0.15, 0.20, 0.30]       # DIAL 1
COOLS = [0, 21, 63, 126]                           # DIAL 2
ARMS = ["STOP", "RANDOM", "WORSTRANK"]             # reported control set, not a dial
GROSS_LADDER = [0.75, 0.65, 0.55, 0.45, 0.35, 0.25]   # the DE-GROSSING FRONTIER, the title's comparand
RAND_SEEDS = [11, 23, 37]
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)
VINTAGE = pd.Timestamp("2026-09-16")
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


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0) if len(r) >= 20 else np.nan


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def vol(r):
    return float(np.asarray(r, float).std(ddof=0) * np.sqrt(252))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), Vol=vol(r))


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


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), is_=stats(r[:o]), oos=stats(r[o:]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


class Panel:
    """The committed book's inputs, computed once per panel and shared by every cell."""

    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        self.q = q.values                      # prices of the investable names, for the stop
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)   # smaller = better
        self.above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, arm, stop, cool, seed=0, counts=None, N=A_N, H=A_H, lag=1):
    """Selection is the committed book; an EXPULSION RULE may remove held names before the
    minimum hold expires and the freed slots are refilled from the same eligible pool by the same
    ranking.  arm STOP expels on the name's own trailing drawdown; RANDOM and WORSTRANK expel the
    SAME COUNT at the SAME rebalance (passed in `counts`) with no drawdown input.
    Returns the slot frame, the filled-slot count per row, the per-rebalance expulsion counts and
    diagnostics."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    S = np.zeros((T, M))
    NSL = np.zeros(T)
    entry = np.full(K, -1, dtype=np.int64)     # the committed MIN-HOLD clock, -1 = not held
    since = np.full(K, -1, dtype=np.int64)     # CONTINUOUS entry index, for the trailing max only
    rmax = np.zeros(K)                         # running max close since CONTINUOUS entry
    cooldown = np.full(K, -10 ** 9, dtype=np.int64)   # index until which a name is barred
    pr = pan.priced[:, pan.iinv]
    q = pan.q
    rng = np.random.default_rng(7_919 * seed + 13)
    nreb = len(pan.reb)
    out_counts = np.zeros(nreb, dtype=np.int64)
    held_counts = np.zeros(nreb, dtype=np.int64)
    weeks = expel_weeks = expel_tot = 0.0
    holdlen: list[float] = []
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        # --- running max since entry, read at the DECISION close ts (rule 2) ---
        for c in held:
            e = int(since[c])
            w = q[e:ts + 1, c]
            w = w[np.isfinite(w)]
            if len(w):
                rmax[c] = max(rmax[c], float(w.max()))
        held_counts[i] = len(held)
        # --- the expulsion rule ---
        expel: list[int] = []
        if arm == "STOP":
            if stop > 0 and len(held):
                for c in held:
                    p = q[ts, c]
                    if np.isfinite(p) and rmax[c] > 0 and p <= (1.0 - stop) * rmax[c]:
                        expel.append(int(c))
        else:
            want = int(counts[i]) if counts is not None else 0
            want = min(want, len(held))
            if want > 0:
                if arm == "RANDOM":
                    expel = [int(c) for c in rng.choice(held, size=want, replace=False)]
                else:                                   # WORSTRANK
                    kk = pan.key[ts][held]
                    kk = np.where(np.isfinite(kk), kk, -np.inf)   # unrankable = treated as worst
                    order = np.argsort(-kk, kind="stable")        # largest key = worst composite
                    expel = [int(held[j]) for j in order[:want]]
        out_counts[i] = len(expel)
        for c in expel:
            holdlen.append(float(t - since[c]))
            entry[c] = -1
            since[c] = -1
            rmax[c] = 0.0
            cooldown[c] = t + cool
        # --- the committed selection, on what is left ---
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        keep = [int(c) for c in held[(t - entry[held]) < H]] if len(held) else []
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        k[cooldown > t] = np.inf                        # barred while cooling down
        for c in keep:
            k[c] = np.inf
        take, need = [], N - len(keep)
        for c in np.argsort(k, kind="stable"):
            if need == 0 or not np.isfinite(k[int(c)]):
                break
            take.append(int(c))
            need -= 1
        was = entry.copy()
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = entry[c]
        for c in take:
            new[c] = t                       # the min-hold clock restarts (committed behaviour)
            if was[c] < 0:                   # ... but the TRAILING MAX only restarts on a REAL entry
                since[c] = t
                rmax[c] = 0.0
        entry = new
        since = np.where(new >= 0, since, -1)
        sel = keep + take
        if t >= WARMUP:
            weeks += 1.0
            if len(expel):
                expel_weeks += 1.0
                expel_tot += len(expel)
        if not sel:
            continue
        stop_i = pan.reb[i + 1] if i + 1 < nreb else T
        S[t:stop_i, pan.iinv[np.array(sel)]] = 1.0
        NSL[t:stop_i] = len(sel)
    d = max(weeks, 1.0)
    diag = dict(expel_week_share=expel_weeks / d, expel_per_year=expel_tot / (d / 52.0),
                expel_total=expel_tot, mean_stopped_hold=float(np.mean(holdlen)) if holdlen else 0.0,
                held_counts=held_counts)
    return S, NSL, out_counts, diag


def run(pan, S, NSL, gross=A_G):
    """The committed RESPREAD fill: gross/len(held) per held name, 10 bps on traded notional,
    drift between rebalances."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        n = NSL[i0]
        if n <= 0:
            curw = np.zeros(M)
            continue
        per = gross / n
        w0 = per * S[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    expo = held[WARMUP:].sum(axis=1)
    return r, float(turn.sum() / (T / 252.0)), float(expo.mean()), float(expo.max())


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


def main():
    t0 = time.time()
    say(f"# {DATE} idea 1271 lane cloud — {SLUG}")
    say(f"# frozen book: RAW 3-leg composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, "
        f"H={A_H} (the STOP overrides it), GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 STOP = {STOPS} (0.00 = the COMMITTED ANCHOR)   DIAL 2 COOL = {COOLS} days")
    say(f"# dose-matched control arms (not dials): {ARMS}, RANDOM over seeds {RAND_SEEDS}")
    say("# THE STOP REFILLS THE FREED SLOT, SO IT IS NOT AN EXPOSURE CUT — G4 proves it rather than assuming it")
    say("# PRIOR ART: idea 9 (2026-09-04) killed the trailing stop on v1/top20/ew-band3; it never ran on "
        "THIS book, never dose-matched a churn control, never read rule 8 on this anchor")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows: list[dict] = []
    r8rows: list[dict] = []
    frontier: list[dict] = []
    dose_rows: list[dict] = []

    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}  n_rebalances={len(pan.reb)}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe bars H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        # ---- the STOP arm first: it defines the dose every control arm must match ----
        cells: dict = {}
        counts_by_cell: dict = {}
        dose_err = 0
        for stop in STOPS:
            for cool in COOLS:
                S, NSL, cnt, diag = build(pan, "STOP", stop, cool)
                r, turn, gmean, gmax = run(pan, S, NSL)
                cells[("STOP", stop, cool, 0)] = (windows(idx, r[WARMUP:]), turn, gmean, gmax, diag)
                counts_by_cell[(stop, cool)] = cnt
                dose_rows.append(dict(panel=pname, stop=stop, cool=cool, **diag,
                                      expel_weeks_pct=100 * diag["expel_week_share"]))
        # ---- the dose-matched control arms ----
        for stop in STOPS:
            for cool in COOLS:
                cnt = counts_by_cell[(stop, cool)]
                S, NSL, c2, diag = build(pan, "WORSTRANK", stop, cool, counts=cnt)
                dose_err = max(dose_err, int(np.abs(c2 - np.minimum(cnt, diag["held_counts"])).max()))
                r, turn, gmean, gmax = run(pan, S, NSL)
                cells[("WORSTRANK", stop, cool, 0)] = (windows(idx, r[WARMUP:]), turn, gmean, gmax, diag)
                for sd in RAND_SEEDS:
                    S, NSL, c3, diag = build(pan, "RANDOM", stop, cool, seed=sd, counts=cnt)
                    dose_err = max(dose_err, int(np.abs(c3 - np.minimum(cnt, diag["held_counts"])).max()))
                    r, turn, gmean, gmax = run(pan, S, NSL)
                    cells[("RANDOM", stop, cool, sd)] = (windows(idx, r[WARMUP:]), turn, gmean, gmax, diag)

        # ---- the de-grossing frontier: the anchor book at lower constant gross ----
        Sa, Na, _, _ = build(pan, "STOP", 0.0, 0)
        front = []
        for g in GROSS_LADDER:
            rg, tg, gmg, _ = run(pan, Sa, Na, gross=g)
            wg = windows(idx, rg[WARMUP:])
            front.append(dict(panel=pname, gross=g, CAGR=wg["full"]["CAGR"], Sharpe=wg["full"]["Sharpe"],
                              MaxDD=wg["full"]["MaxDD"], oos=wg["oos"]["Sharpe"], turnover=tg,
                              gross_mean=gmg, pass_4b=all(legs_4b(wg, spy).values()),
                              fail_4b=failed(legs_4b(wg, spy))))
            say(f"   FRONTIER gross {g:.2f}: {wg['full']['CAGR']:7.2%} / {wg['full']['Sharpe']:.4f} / "
                f"{wg['full']['MaxDD']:7.2%}  OOS {wg['oos']['Sharpe']:.4f}  4b "
                f"{'PASS' if all(legs_4b(wg, spy).values()) else 'FAIL(' + failed(legs_4b(wg, spy)) + ')'}")
        frontier.extend(front)

        anchor = cells[("STOP", 0.0, COOLS[0], 0)][0]
        say(f"   anchor (STOP 0.00) {anchor['full']['CAGR']:7.2%} / {anchor['full']['Sharpe']:.4f} / "
            f"{anchor['full']['MaxDD']:7.2%}   OOS {anchor['oos']['Sharpe']:.4f}")

        # ---- gates that need this panel ----
        if pname == "U56":
            pv = Panel("U56v", p_px.loc[p_px.index <= VINTAGE], inv)
            S, NSL, _, _ = build(pv, "STOP", 0.0, 0)
            rv, _, _, _ = run(pv, S, NSL)
            sv = stats(rv[WARMUP:])
            err = max(abs(sv["CAGR"] - COMMITTED_U56[0]), abs(sv["Sharpe"] - COMMITTED_U56[1]),
                      abs(sv["MaxDD"] - COMMITTED_U56[2]))
            gate("G1 vintage-pinned replay (U56 STOP 0.00 @ 2026-09-16)",
                 f"{sv['CAGR']:.4%}/{sv['Sharpe']:.4f}/{sv['MaxDD']:.4%} err {err:.2e}",
                 "committed 15.7147%/1.1480/-19.1276%, err < 1e-4", err < 1e-4)
            gate("G9 one-extra-day cache drift",
                 f"CAGR {anchor['full']['CAGR']-sv['CAGR']:+.4%}  Sharpe "
                 f"{anchor['full']['Sharpe']-sv['Sharpe']:+.4f}", "published, not toleranced", True)

        base = cells[("STOP", 0.0, COOLS[0], 0)][0]["full"]
        worst = 0.0
        for arm in ARMS:
            for cool in COOLS:
                for sd in (RAND_SEEDS if arm == "RANDOM" else [0]):
                    c = cells[(arm, 0.0, cool, sd)][0]["full"]
                    worst = max(worst, abs(c["CAGR"] - base["CAGR"]), abs(c["Sharpe"] - base["Sharpe"]),
                                abs(c["MaxDD"] - base["MaxDD"]))
        gate(f"G2 STOP 0.00 identical at every COOL and arm [{pname}]", f"{worst:.3e}", "== 0.0", worst == 0.0)

        tot = sum(d["expel_total"] for d in dose_rows if d["panel"] == pname)
        gate(f"G3 the mechanism has a DOSE [{pname}]",
             f"{tot:.0f} expulsions over the grid; "
             f"max per-cell {max((d['expel_per_year'] for d in dose_rows if d['panel']==pname)):.2f}/yr",
             "> 0", tot > 0)

        agm, agx = cells[("STOP", 0.0, COOLS[0], 0)][2], cells[("STOP", 0.0, COOLS[0], 0)][3]
        dmean = max(abs(v[2] - agm) for v in cells.values())
        dmax = max(v[3] for v in cells.values()) - agx
        gate(f"G4 NOT an exposure cut [{pname}]",
             f"mean gross range [{min(v[2] for v in cells.values()):.4f}, "
             f"{max(v[2] for v in cells.values()):.4f}] vs the anchor's {agm:.4f} (max |d| {dmean:.4f}); "
             f"max drifted gross {max(v[3] for v in cells.values()):.4f} vs the anchor's own {agx:.4f}",
             "mean within 0.005 of the anchor's and no cell drifts higher than the anchor does "
             "[SPEC CORRECTED MID-RUN: the first wording demanded drifted gross <= 0.75, which the "
             "COMMITTED ANCHOR ITSELF fails at 0.7674 because held weights drift between rebalances; "
             "the original wording and its failure are published in the memo]",
             dmean <= 5e-3 and dmax <= 1e-9)

        mono = True
        for cool in COOLS:
            cs = [sum(counts_by_cell[(s, cool)]) for s in STOPS[1:]]
            mono &= all(cs[i] >= cs[i + 1] for i in range(len(cs) - 1))
        gate(f"G6 stop-out count non-increasing in STOP depth [{pname}]", f"monotone={mono}", "True", mono)

        gate(f"G7 control arms expel the STOP arm's count at every rebalance [{pname}]",
             f"max |expelled - min(wanted, held)| over all {24*4} control builds = {dose_err}",
             "== 0 (an arm may fall short ONLY when it holds fewer names than the dose)", dose_err == 0)

        # ---- causality spot-check: the stop flag from truncated prices ----
        if pname == "U56":
            cut = pan.idx[len(pan.idx) // 2]
            ptr = Panel("trunc", p_px.loc[p_px.index <= cut], inv)
            _, _, ctr, _ = build(ptr, "STOP", 0.15, 63)
            _, _, cfu, _ = build(pan, "STOP", 0.15, 63)
            m = len(ctr) - 1                       # the truncated panel's last rebalance is partial
            dcz = int(np.abs(ctr[:m] - cfu[:m]).max()) if m > 0 else -1
            gate("G5 CAUSALITY (stop-out counts rebuilt from prices TRUNCATED at the midpoint)",
                 f"{m} rebalances to {cut.date()}, max |d count| {dcz}", "== 0", dcz == 0)
            S1, N1, _, _ = build(pan, "STOP", 0.15, 63)
            S2, N2, _, _ = build(pan, "STOP", 0.15, 63)
            r1 = run(pan, S1, N1)[0]
            r2 = run(pan, S2, N2)[0]
            d = float(np.abs(r1 - r2).max())
            gate("G8 determinism (U56 STOP 0.15/COOL 63 rebuilt and re-run)", f"{d:.3e}", "== 0.0", d == 0.0)

        # ---- publish every cell ----
        say("   arm       stop cool seed |    CAGR   Sharpe    MaxDD    vol |  H1/H2 Sharpe |  OOS Sh"
            " | turn  gmean | exp/yr wk% | 4a 4b | fail4b")
        for arm in ARMS:
            for stop in STOPS:
                for cool in COOLS:
                    for sd in (RAND_SEEDS if arm == "RANDOM" else [0]):
                        w, turn, gmean, gmax, diag = cells[(arm, stop, cool, sd)]
                        a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                        rows.append(dict(panel=pname, arm=arm, stop=stop, cool=cool, seed=sd,
                                         turnover=turn, gross_mean=gmean, gross_max=gmax,
                                         expel_per_year=diag["expel_per_year"],
                                         expel_week_share=diag["expel_week_share"],
                                         mean_stopped_hold=diag["mean_stopped_hold"],
                                         pass_4a=all(a4.values()), pass_4b=all(b4.values()),
                                         fail_4a=failed(a4), fail_4b=failed(b4), **flat(w)))
                        if arm != "RANDOM" or sd == RAND_SEEDS[0]:
                            say(f"   {arm:9s} {stop:4.2f} {cool:4d} {sd:4d} | {w['full']['CAGR']:7.2%} "
                                f"{w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} {w['full']['Vol']:6.2%} | "
                                f"{w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | {w['oos']['Sharpe']:7.4f} | "
                                f"{turn:5.2f} {gmean:.3f} | {diag['expel_per_year']:6.2f} "
                                f"{100*diag['expel_week_share']:4.1f} | "
                                f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | "
                                f"{failed(b4)}")

        # ---- rule 8, per arm ----
        for arm in ARMS:
            for sd in (RAND_SEEDS if arm == "RANDOM" else [0]):
                grid = [(s, c) for s in STOPS for c in COOLS]
                iss = [cells[(arm, s, c, sd)][0]["is_"]["Sharpe"] for s, c in grid]
                oos = [cells[(arm, s, c, sd)][0]["oos"]["Sharpe"] for s, c in grid]
                j = int(np.nanargmax(iss))
                dn = cells[(arm, 0.0, COOLS[0], sd)][0]["oos"]["Sharpe"]
                w = cells[(arm, grid[j][0], grid[j][1], sd)][0]
                r8rows.append(dict(panel=pname, arm=arm, seed=sd, pick_stop=grid[j][0], pick_cool=grid[j][1],
                                   is_sharpe=iss[j], oos_sharpe=oos[j], donothing_oos=dn,
                                   delta=oos[j] - dn, cellmean_oos=float(np.nanmean(oos)),
                                   worst_oos=float(np.nanmin(oos)), rank_is_oos=rankcorr(iss, oos),
                                   spy_oos=spy["oos"]["Sharpe"], live_oos=live["oos"]["Sharpe"],
                                   pick_4b=all(legs_4b(w, spy).values()),
                                   donothing_4b=all(legs_4b(cells[(arm, 0.0, COOLS[0], sd)][0], spy).values())))
                if arm != "RANDOM" or sd == RAND_SEEDS[0]:
                    say(f"   RULE 8 [{arm}] IS-argmax = STOP {grid[j][0]:.2f} / COOL {grid[j][1]} "
                        f"(IS Sh {iss[j]:.4f}) -> OOS {oos[j]:.4f}  vs do-nothing {dn:.4f}  "
                        f"delta {oos[j]-dn:+.4f}   cellmean {np.nanmean(oos):.4f}  "
                        f"worst {np.nanmin(oos):.4f}  rank corr IS/OOS {rankcorr(iss, oos):+.2f}")

    F = pd.DataFrame(frontier)
    F.to_csv(f"{STEM}.frontier.csv", index=False)
    G = pd.DataFrame(rows)
    W = pd.DataFrame(r8rows)
    D = pd.DataFrame(dose_rows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    W.to_csv(f"{STEM}.walkforward.csv", index=False)
    D.to_csv(f"{STEM}.dose.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say("\n## SUMMARY")
    say(f"   cells {len(G)}   4a passes {int(G.pass_4a.sum())}   4b passes {int(G.pass_4b.sum())}")

    # (1) dose
    say("\n   (1) DOSE — does the stop fire on THIS book at all?")
    for pname in G.panel.unique():
        d = D[D.panel == pname]
        for stop in STOPS[1:]:
            dd = d[d.stop == stop]
            say(f"      {pname:9s} STOP {stop:4.2f}: {dd.expel_per_year.mean():6.2f} expulsions/yr, "
                f"{dd.expel_weeks_pct.mean():5.1f}% of rebalances, mean stopped holding "
                f"{dd.mean_stopped_hold.mean():5.1f} days")

    # (2) the headline: STOP minus its dose-matched controls
    say("\n   (2) THE STOP AGAINST ITS DOSE-MATCHED CONTROLS (same count, same weeks):")
    key = ["panel", "stop", "cool"]
    st = G[(G.arm == "STOP") & (G.stop > 0)].set_index(key)
    for ctrl in ("RANDOM", "WORSTRANK"):
        cg = G[(G.arm == ctrl) & (G.stop > 0)].groupby(key)[
            ["full_CAGR", "full_Sharpe", "full_MaxDD", "oos_Sharpe"]].mean()
        j = st.join(cg, rsuffix="_c", how="inner")
        n = len(j)
        say(f"      vs {ctrl:9s} n={n}  d_CAGR {100*(j.full_CAGR-j.full_CAGR_c).mean():+.2f}pp  "
            f"d_Sharpe {(j.full_Sharpe-j.full_Sharpe_c).mean():+.4f} "
            f"(>0 at {int((j.full_Sharpe>j.full_Sharpe_c).sum())}/{n})  "
            f"d_MaxDD {100*(j.full_MaxDD-j.full_MaxDD_c).mean():+.2f}pp "
            f"(>0 at {int((j.full_MaxDD>j.full_MaxDD_c).sum())}/{n})  "
            f"d_OOS {(j.oos_Sharpe-j.oos_Sharpe_c).mean():+.4f} "
            f"(>0 at {int((j.oos_Sharpe>j.oos_Sharpe_c).sum())}/{n})")

    # (3) the stop against DOING NOTHING
    say("\n   (3) THE STOP AGAINST DOING NOTHING (its own panel's STOP 0.00):")
    for pname in G.panel.unique():
        a = G[(G.panel == pname) & (G.arm == "STOP") & (G.stop == 0.0)].iloc[0]
        b = G[(G.panel == pname) & (G.arm == "STOP") & (G.stop > 0)]
        say(f"      {pname:9s} anchor {a.full_CAGR:7.2%}/{a.full_Sharpe:.4f}/{a.full_MaxDD:7.2%} "
            f"OOS {a.oos_Sharpe:.4f} | braked cells: MaxDD "
            f"{b.full_MaxDD.max():7.2%}..{b.full_MaxDD.min():7.2%}  CAGR {b.full_CAGR.min():6.2%}.."
            f"{b.full_CAGR.max():6.2%}  Sharpe {b.full_Sharpe.min():.4f}..{b.full_Sharpe.max():.4f}  "
            f"d_MaxDD best {100*(b.full_MaxDD.max()-a.full_MaxDD):+.2f}pp at a CAGR cost of "
            f"{100*(b.loc[b.full_MaxDD.idxmax()].full_CAGR-a.full_CAGR):+.2f}pp")

    # (4) structure in the dials
    say("\n   (4) STRUCTURE IN THE DIALS (STOP arm, pooled over panels):")
    for stop in STOPS[1:]:
        b = G[(G.arm == "STOP") & (G.stop == stop)]
        a = G[(G.arm == "STOP") & (G.stop == 0.0)].groupby("panel").first()
        dd = np.mean([r.full_MaxDD - a.loc[r.panel].full_MaxDD for r in b.itertuples()])
        dc = np.mean([r.full_CAGR - a.loc[r.panel].full_CAGR for r in b.itertuples()])
        ds = np.mean([r.full_Sharpe - a.loc[r.panel].full_Sharpe for r in b.itertuples()])
        do = np.mean([r.oos_Sharpe - a.loc[r.panel].oos_Sharpe for r in b.itertuples()])
        say(f"      STOP {stop:4.2f}: d_MaxDD {100*dd:+.2f}pp  d_CAGR {100*dc:+.2f}pp  "
            f"d_Sharpe {ds:+.4f}  d_OOS {do:+.4f}")
    for cool in COOLS:
        b = G[(G.arm == "STOP") & (G.stop > 0) & (G.cool == cool)]
        a = G[(G.arm == "STOP") & (G.stop == 0.0)].groupby("panel").first()
        dd = np.mean([r.full_MaxDD - a.loc[r.panel].full_MaxDD for r in b.itertuples()])
        ds = np.mean([r.full_Sharpe - a.loc[r.panel].full_Sharpe for r in b.itertuples()])
        say(f"      COOL {cool:4d}: d_MaxDD {100*dd:+.2f}pp  d_Sharpe {ds:+.4f}")

    # (4b) THE TITLE'S QUESTION: the stop against the DE-GROSSING FRONTIER at matched MaxDD
    say("\n   (4b) IS THE STOP CHEAPER THAN DE-GROSSING?  Every STOP cell against the flat-gross cut "
        "that reaches the SAME MaxDD (positive = the stop is cheaper):")
    above = tot_in = 0
    for pname in G.panel.unique():
        f = F[F.panel == pname].sort_values("MaxDD")
        b = G[(G.panel == pname) & (G.arm == "STOP") & (G.stop > 0)]
        a = G[(G.panel == pname) & (G.arm == "STOP") & (G.stop == 0.0)].iloc[0]
        dd = []
        for r in b.itertuples():
            if r.full_MaxDD < f.MaxDD.min() or r.full_MaxDD > f.MaxDD.max():
                continue
            cg = float(np.interp(r.full_MaxDD, f.MaxDD.values, f.CAGR.values))
            sg = float(np.interp(r.full_MaxDD, f.MaxDD.values, f.Sharpe.values))
            og = float(np.interp(r.full_MaxDD, f.MaxDD.values, f.oos.values))
            dd.append((r.stop, r.cool, r.full_MaxDD, r.full_CAGR - cg, r.full_Sharpe - sg,
                       r.oos_Sharpe - og))
        if not dd:
            say(f"      {pname:9s} no STOP cell lands inside the frontier's MaxDD range")
            continue
        arr = np.array([[x[3], x[4], x[5]] for x in dd])
        above += int((arr[:, 0] > 0).sum())
        tot_in += len(dd)
        best = max(dd, key=lambda x: x[3])
        say(f"      {pname:9s} n={len(dd)}  d_CAGR vs frontier {100*arr[:,0].mean():+.2f}pp "
            f"(>0 at {int((arr[:,0]>0).sum())}/{len(dd)})  d_Sharpe {arr[:,1].mean():+.4f} "
            f"(>0 at {int((arr[:,1]>0).sum())}/{len(dd)})  d_OOS {arr[:,2].mean():+.4f} "
            f"(>0 at {int((arr[:,2]>0).sum())}/{len(dd)})  | best STOP {best[0]:.2f}/COOL {best[1]} "
            f"at MaxDD {best[2]:7.2%}: {100*best[3]:+.2f}pp")
        b2 = b[b.full_MaxDD > a.full_MaxDD]
        fl = f[f.MaxDD > a.full_MaxDD]
        if len(b2) and len(fl):
            xr = float(((a.full_CAGR - b2.full_CAGR) / (b2.full_MaxDD - a.full_MaxDD)).mean())
            xf = float(((a.full_CAGR - fl.CAGR) / (fl.MaxDD - a.full_MaxDD)).mean())
            say(f"                exchange rate, pp CAGR paid per pp of MaxDD bought:  STOP {xr:.2f}"
                f"   DE-GROSSING {xf:.2f}   (lower is cheaper)")
    say(f"      POOLED: the stop beats the de-grossing frontier at {above} of {tot_in} cells "
        f"inside its MaxDD range")

    # (5) 4b conversions
    conv = []
    for r in G[(G.arm == "STOP") & (G.stop > 0)].itertuples():
        dn = G[(G.panel == r.panel) & (G.arm == "STOP") & (G.stop == 0.0)].iloc[0]
        if r.pass_4b and not dn.pass_4b:
            conv.append(r)
    say(f"\n   (5) 4b CONVERSIONS (the panel's own do-nothing fails 4b, the cell passes): "
        f"{len(conv)} of {len(G[(G.arm=='STOP')&(G.stop>0)])} braked STOP cells")
    for r in conv:
        cg = G[(G.panel == r.panel) & (G.arm == "RANDOM") & (G.stop == r.stop) & (G.cool == r.cool)]
        say(f"      {r.panel:9s} STOP {r.stop:.2f}/COOL {r.cool}: {r.full_CAGR:7.2%} / "
            f"{r.full_Sharpe:.4f} / {r.full_MaxDD:7.2%}  OOS {r.oos_Sharpe:.4f} | RANDOM at the same "
            f"dose passes 4b at {int(cg.pass_4b.sum())}/{len(cg)}")

    # (6) rule 8
    say("\n   (6) RULE 8 chooser-minus-do-nothing:")
    for arm in ARMS:
        w = W[W.arm == arm]
        say(f"      {arm:9s} mean {w.delta.mean():+.4f}  positive at {int((w.delta>0).sum())}/{len(w)}  "
            f"mean rank corr IS/OOS {w.rank_is_oos.mean():+.3f}")
    ws = W[W.arm == "STOP"]
    say(f"      STOP arm cell by cell:")
    for r in ws.itertuples():
        say(f"      {r.panel:9s} pick STOP {r.pick_stop:.2f}/COOL {r.pick_cool}  OOS {r.oos_sharpe:.4f} "
            f"vs do-nothing {r.donothing_oos:.4f} ({r.delta:+.4f})  SPY OOS {r.spy_oos:.4f}  "
            f"live v2 OOS {r.live_oos:.4f}  4b pick {'PASS' if r.pick_4b else 'FAIL'} / "
            f"do-nothing {'PASS' if r.donothing_4b else 'FAIL'}")
    say(f"      ALL ARMS: mean {W.delta.mean():+.4f}, beats do-nothing at "
        f"{int((W.delta>0).sum())} of {len(W)}")

    # (7) which leg fails
    fl: dict = {}
    for f in G.fail_4b:
        for x in str(f).split(","):
            if x and x != "-":
                fl[x] = fl.get(x, 0) + 1
    say(f"\n   (7) WHICH 4b LEG FAILS, over the {int((~G.pass_4b).sum())} failures: "
        + "  ".join(f"{k} {v}" for k, v in sorted(fl.items(), key=lambda kv: -kv[1])))

    npass = sum(1 for g in GATES if g["pass_"])
    say(f"\n   GATES {npass} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
