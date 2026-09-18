#!/usr/bin/env python3
"""Idea 1267 (lane cloud, 2026-09-18): does a DEFENSIVE ROTATION buy the DD LEG more cheaply
than DE-GROSSING?

THE PREMISE.  Eight dials on the standing 2026-09-04 KEEP 4b book — rebalance phase (1253),
calendar years (1254), ex-post winner names (1255), the signal (1257), sector caps (1258), an
explicit drawdown brake (1262), portfolio vol targeting (1263), inverse-vol slot sizing (1264),
the idle sleeve (1268) and this run's own idea 1066 — all land on one sentence: every other 4b
leg passes at essentially every grid point and the DRAWDOWN CAP is the only leg that ever
fails.  Every mechanism priced so far moves HOW MUCH is held (exposure) or HOW IT IS SIZED.
None of them changes WHAT is held when the trend is off.  1267 asks the remaining question: when
the gate takes names out of the book, is the drawdown cheaper to buy INSIDE equities — park the
freed slots in the lowest-beta names available — than by de-grossing to cash?

WHERE THE FREED SLOTS ARE, AND A CORRECTION TO THE QUEUE'S WORDING.  The committed book keeps
N=20 slots and equal-weights whatever it holds at GROSS=0.75, so when the 200d gate empties the
eligible pool the book does NOT go to cash: it RE-SPREADS onto the survivors (U56, H=126: fewer
than 20 names held at 3.7% of rebalances, minimum 8; at H=0 that is 10.8% and minimum 3, and
those weeks are where the drawdown is made).  Both readings are therefore run as a reported
axis, not assumed:
    FILL = RESPREAD — the COMMITTED book.  ROT=0 replays the 2026-09-04 anchor exactly (G1).
    FILL = CASH     — the fixed-slot variant: each held name gets GROSS/N and every unfilled
                      slot is cash.  This is the de-grossing book the queue's premise assumes
                      and the thing the rotation is supposed to beat.
Second correction, stated rather than buried: the queue says "the lowest-beta ELIGIBLE names",
but a slot is freed only when the eligible pool is EXHAUSTED — by construction there is never an
eligible name left to rotate into.  The rotation pool is therefore the priced, not-currently-held
names that pass the book's own vol20 < 0.60 risk filter, ranked by trailing beta to SPY.  That
is the only reading under which the mechanism exists at all.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    BETA_LOOK {63, 126, 252} trading days — the trailing window of beta to SPY, read at the
              DECISION date t-1 and applied at t (rule 2).
    ROT       {0.00, 0.25, 0.50, 0.75, 1.00} — the share of FREED slots that are rotated.
              ROT=0.00 is the do-nothing control and is in the grid so it is measured.
EVERY grid point is published in the .grid.csv.

NOT DIALS, reported at every value.  PANEL {U56, B135, SMALL} (rule 9).  FILL {RESPREAD, CASH}.
MINHOLD {126, 0} — ADDED AFTER THE FIRST PASS AND SAID SO PLAINLY, because the first pass showed
the mechanism has almost no DOSE on the committed book: with H=126 the minimum hold retains stale
names through the trough, so slots are freed at only 3.7% of rebalances and 0.205 of a slot per
week at ROT=1.00.  That is itself this run's first finding and it is exactly idea 1066's result
seen from the other side (the min hold IS frozen weight, so there is nothing left to free).  The
question "is the drawdown cheaper to buy inside equities" can only be asked of a book that
actually frees slots, so the H=0 book — the record's own BOOK_H0, where the gate empties the book
at 10.8% of rebalances, minimum 3 names held — is run beside it at every cell.  MINHOLD is a
REPORTED AXIS, not a third dial: no cell is chosen on it, both values are published everywhere,
and rule 8 is run separately inside each.
ROT_KIND — the control set without which the headline is unreadable, because rotating ADDS
EXPOSURE and this record has already established that exposure alone is a pure CAGR-for-drawdown
slide:
    LOWBETA  the mechanism (lowest trailing beta first);
    HIGHBETA the sign test (highest beta first) — if the axis is real the two must differ;
    RANDOM   3 seeds, the PURE EXPOSURE control: the same slots filled with no beta input at
             all.  LOWBETA minus RANDOM at the same ROT is the beta channel with exposure
             differenced out, and is the number this run is actually about.
Also reported at every cell: both KEEP paths leg by leg; full / halves / IS / OOS; annual
turnover; mean realised gross; the share of rebalances at which anything is rotated; the mean
rotated slot count; and the realised book beta to SPY.

THE TACTICAL SLEEVE IS TACTICAL, and this is a frozen construction choice, not a dial.  Rotated
names are re-decided EVERY rebalance: they are released before the next week's selection and
never acquire the H=126 minimum hold.  Parking cash in a defensive name for one week at a time
is the mechanism; locking a defensive name in for half a year is a different idea and is not
this one.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA
AND vol20 < 0.60; RAW three-leg composite (21/252, 0/126, 0/63 percentile ranks); N=20 slots;
H=126 minimum hold on CORE names; GROSS=0.75; WEEKLY decide-Friday / trade-Monday; 10 bps per
unit turnover; t+1 execution; 260-row warm-up; equal slots.  CORE SELECTION IS IDENTICAL AT
EVERY CELL BY CONSTRUCTION — the dials touch only what happens to slots the gate has emptied.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — freed slots are too rare to move anything; MaxDD moves less than 0.20pp at every
      cell.  Then the mechanism has no dose on this book and the queue's premise is wrong about
      where the drawdown comes from.
  (B) THE DD LEG IS BOUGHT INSIDE EQUITIES — some cell materially improves MaxDD, holds 4b's
      CAGR floor and both half-Sharpe legs, BEATS ITS OWN RANDOM-ROTATION CONTROL at the same
      ROT (so it is beta and not exposure), and rule 8 reaches it.  KEEP-candidate memo with
      exact RULES wording.
  (C) BOUGHT AND OVERPAID FOR, or BOUGHT BY EXPOSURE — MaxDD improves but a 4b leg fails, or
      the improvement equals the RANDOM control's, in which case the beta axis is decorative.
  (D) WORSE — low-beta names in a crash are still equities: rotation deepens the drawdown
      against holding cash, and de-grossing was the cheaper purchase after all.
  Not mutually exclusive across panels; whichever fire are reported as they fall, and the
  capital verdict follows rule 8, never the best cell.

RULE 8 (walk-forward, required).  (BETA_LOOK, ROT) is CHOSEN on warm-up..2016-12-31 by IS
Sharpe ALONE and 2017-2026 is read ONCE, per (panel, FILL, ROT_KIND).  Reported against the
do-nothing ROT=0.00 cell, the cell mean, the worst cell, and the IS/OOS rank correlation over
the 15 cells.  The capital verdict is the sign of chooser-minus-do-nothing.

GATES.  G1 vintage-pinned replay: truncated at 2026-09-16, U56 RESPREAD ROT=0 must replay the
committed 15.7147% / 1.14804 / -19.1276% to 1e-4.  G2 ROT=0.00 is bit-identical across all
BETA_LOOK and all ROT_KIND (nothing is rotated, so nothing may differ).  G3 the mechanism has a
dose: the share of rebalances with a rotation and the mean rotated slots are published per
panel, and must be > 0 somewhere or outcome (A) is declared on the spot.  G4 the beta axis does
what it says: the realised book beta of LOWBETA is BELOW HIGHBETA's at every (panel, FILL) at
ROT=1.00.  G5 determinism: the U56 RESPREAD grid recomputed bit for bit.  G6 the one-extra-day
cache drift, published not toleranced.  G7 no leverage: realised gross <= 0.75 everywhere, and
RESPREAD's gross is exactly 0.75 whenever anything is held.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level is optimistic and every 4b pass is an UPPER bound.
The headline is a DIFFERENCE between what is done with the SAME freed slots on the SAME panel
with the SAME core selection, which is first-order immune to a level bias moving all cells
together.  One direction is NOT neutral and is stated: the rotation pool is drawn from names
that FAILED the trend gate — exactly the population a current-constituent panel has cleaned of
its casualties — so the defensive sleeve's return here is flattered and any LOWBETA gain is an
UPPER bound, while the de-grossing control (cash) carries no such flattery at all.

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
SLUG = "does-a-DEFENSIVE-SECTOR-ROTATION-buy-the-DD-LEG-more-cheaply-than-DE-GROSSING"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                     # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
BETA_LOOKS = [63, 126, 252]                       # DIAL 1
ROTS = [0.00, 0.25, 0.50, 0.75, 1.00]             # DIAL 2
KINDS = ["LOWBETA", "HIGHBETA", "RANDOM"]         # reported control set, not a dial
RAND_SEEDS = 3
FILLS = ["RESPREAD", "CASH"]                      # reported, not a dial
MINHOLDS = [A_H, 0]                               # reported axis, not a dial (see docstring)
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
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
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
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        qr = q.pct_change()
        vol20 = (qr.rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        spy_s = px["SPY"].pct_change()
        self.spy = spy_s.fillna(0.0).values
        # trailing beta to SPY at every date, for each lookback (no look-ahead: read at t-1)
        self.beta = {}
        for L in BETA_LOOKS:
            vs = spy_s.rolling(L).var()
            cv = qr.rolling(L).cov(spy_s)
            b = cv.div(vs, axis=0).values
            self.beta[L] = np.where(np.isfinite(b), b, np.inf)   # unknown beta = never "lowest"
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, kind, look, rot, seed=0, N=A_N, H=A_H, lag=1):
    """Core selection is the frozen book; slots the gate cannot fill are optionally parked in a
    TACTICAL sleeve chosen from the priced, not-held, vol-OK names by trailing beta (LOWBETA /
    HIGHBETA) or at random (RANDOM).  Tactical names are released every rebalance and never
    acquire the minimum hold.  Returns the slot frame (1 = one of N slots) and diagnostics."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    S = np.zeros((T, M))               # slot indicator, scaled by the caller
    NSL = np.zeros(T)                  # filled slots at each row
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.key
    bet = pan.beta[look]
    nreb = len(pan.reb)
    rng = np.random.default_rng(7_919 * seed + 13)
    rot_weeks = rot_slots = weeks = freed_tot = 0.0
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        if len(held):
            held = held[pr[t, held]]
        keep = [int(c) for c in held[(t - cur[held]) < H]] if len(held) else []
        k = key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
        for c in keep:
            k[c] = np.inf
        take, need = [], N - len(keep)
        for c in np.argsort(k, kind="stable"):
            if need == 0 or not np.isfinite(k[int(c)]):
                break
            take.append(int(c))
            need -= 1
        core = keep + take
        freed = N - len(core)
        tact = []
        if freed > 0 and rot > 0:
            pool = np.flatnonzero(pr[ts] & pan.volok[ts])
            pool = np.array([c for c in pool if c not in set(core)], dtype=np.int64)
            nrot = int(round(rot * freed))
            if nrot > 0 and len(pool):
                nrot = min(nrot, len(pool))
                if kind == "RANDOM":
                    tact = [int(c) for c in rng.choice(pool, size=nrot, replace=False)]
                else:
                    b = bet[ts][pool]
                    ordr = np.argsort(b, kind="stable")
                    if kind == "HIGHBETA":
                        ordr = ordr[np.isfinite(b[ordr])][::-1]
                    tact = [int(pool[j]) for j in ordr[:nrot]]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new                      # tactical names are NOT carried: released next week
        sel = core + tact
        if t >= WARMUP:
            weeks += 1.0
            freed_tot += freed
            if tact:
                rot_weeks += 1.0
                rot_slots += len(tact)
        if not sel:
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        S[t:stop, pan.iinv[np.array(sel)]] = 1.0
        NSL[t:stop] = len(sel)
    d = max(weeks, 1.0)
    return S, NSL, dict(rot_week_share=rot_weeks / d, rot_slots_mean=rot_slots / d,
                        freed_mean=freed_tot / d)


def run(pan, S, NSL, fill, N=A_N, gross=A_G):
    """RESPREAD: gross/len(held) per held name (the committed book).  CASH: gross/N per slot,
    unfilled slots stay in cash.  10 bps on traded notional, drift between rebalances."""
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
        per = gross / (n if fill == "RESPREAD" else N)
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
    set_max = 0.0
    for i0 in pan.reb:
        n = NSL[i0]
        if n > 0:
            set_max = max(set_max, (gross / (n if fill == "RESPREAD" else N)) * S[i0].sum())
    return (r, float(turn.sum() / (T / 252.0)), float(expo.mean()), float(expo.max()),
            float(set_max))


def book_beta(r, spy):
    v = np.var(spy, ddof=0)
    return float(np.cov(r, spy, ddof=0)[0, 1] / v) if v > 0 else np.nan


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
    say(f"# {DATE} idea 1267 lane cloud — {SLUG}")
    say(f"# frozen book: RAW 3-leg composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, "
        f"H={A_H}, GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 BETA_LOOK = {BETA_LOOKS}   DIAL 2 ROT = {ROTS} (0.00 = do-nothing control)")
    say(f"# reported-not-dials: panel {{U56,B135,SMALL}} x FILL {FILLS} x ROT_KIND {KINDS} "
        f"(RANDOM over {RAND_SEEDS} seeds = the PURE EXPOSURE control)")
    say("# CORE SELECTION IDENTICAL AT EVERY CELL; tactical names are released every rebalance "
        "and never acquire the min hold")

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

    rows, r8rows = [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spyv = pan.spy[WARMUP:]
        spy = windows(idx, spyv)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)
        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe bars H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        BUILDS = {}
        for mh in MINHOLDS:
            for kind in KINDS:
                for look in BETA_LOOKS:
                    if kind == "RANDOM" and look != BETA_LOOKS[1]:
                        continue
                    for rot in ROTS:
                        for sd in (range(RAND_SEEDS) if (kind == "RANDOM" and rot > 0) else [0]):
                            BUILDS[(mh, kind, look, rot, sd)] = build(pan, kind, look, rot,
                                                                      seed=sd, H=mh)
        cells = {}
        for mh in MINHOLDS:
            for fill in FILLS:
                say(f"\n   --- MINHOLD {mh} / FILL {fill} ---")
                say("   kind     look   ROT |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe |  OOS Sh | "
                    "turn  gross beta | rotwk rotsl | 4a 4b | fail4b")
                for kind in KINDS:
                    for look in BETA_LOOKS:
                        if kind == "RANDOM" and look != BETA_LOOKS[1]:
                            continue                  # RANDOM ignores the beta window
                        for rot in ROTS:
                            seeds = range(RAND_SEEDS) if (kind == "RANDOM" and rot > 0) else [0]
                            acc = []
                            for sd in seeds:
                                S, NSL, dg = BUILDS[(mh, kind, look, rot, sd)]
                                r, turn, ex, exmax, exset = run(pan, S, NSL, fill)
                                rr = r[WARMUP:]
                                w = windows(idx, rr)
                                a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                                rec = dict(panel=pname, minhold=mh, fill=fill, kind=kind,
                                           look=look, rot=rot, seed=sd, **flat(w), turnover=turn,
                                           gross_mean=ex, gross_max=exmax,
                                           gross_set_max=exset,
                                           book_beta=book_beta(rr, spyv), **dg,
                                           keep4a=all(a4.values()), keep4b=all(b4.values()),
                                           fail4a=failed(a4), fail4b=failed(b4))
                                rows.append(rec)
                                acc.append(rec)
                            a = acc[0] if len(acc) == 1 else {
                                k: (float(np.mean([c[k] for c in acc]))
                                    if isinstance(acc[0][k], float) else acc[0][k]) for k in acc[0]}
                            cells[(mh, fill, kind, look, rot)] = a
                            say(f"   {kind:8s} {look:4d} {rot:5.2f} | {a['full_CAGR']:7.2%} "
                                f"{a['full_Sharpe']:8.4f} {a['full_MaxDD']:8.2%} | "
                                f"{a['h1_Sharpe']:.4f}/{a['h2_Sharpe']:.4f} | "
                                f"{a['oos_Sharpe']:7.4f} | "
                                f"{a['turnover']:5.2f} {a['gross_mean']:5.3f} {a['book_beta']:5.2f} | "
                                f"{a['rot_week_share']:5.3f} {a['rot_slots_mean']:5.3f} | "
                                f"{'Y' if acc[0]['keep4a'] else 'n'}  "
                                f"{'Y' if acc[0]['keep4b'] else 'n'} | {acc[0]['fail4b']}")

                # ---- rule 8, per (panel, minhold, fill, kind)
                for kind in KINDS:
                    ks = [k for k in cells if k[0] == mh and k[1] == fill and k[2] == kind]
                    iss = np.array([cells[k]["is__Sharpe"] for k in ks])
                    oos = np.array([cells[k]["oos_Sharpe"] for k in ks])
                    j = int(np.nanargmax(iss))
                    pk = cells[ks[j]]
                    nothing = cells[[k for k in ks if k[4] == 0.0][0]]
                    r8 = dict(panel=pname, minhold=mh, fill=fill, kind=kind,
                              pick_look=ks[j][3], pick_rot=ks[j][4],
                              pick_IS=pk["is__Sharpe"], pick_OOS=pk["oos_Sharpe"],
                              donothing_OOS=nothing["oos_Sharpe"],
                              delta=pk["oos_Sharpe"] - nothing["oos_Sharpe"],
                              pick_OOS_CAGR=pk["oos_CAGR"], pick_OOS_MaxDD=pk["oos_MaxDD"],
                              nothing_OOS_CAGR=nothing["oos_CAGR"],
                              nothing_OOS_MaxDD=nothing["oos_MaxDD"],
                              cellmean_OOS=float(np.nanmean(oos)),
                              worst_OOS=float(np.nanmin(oos)), best_OOS=float(np.nanmax(oos)),
                              rank_IS_OOS=rankcorr(iss, oos), spy_OOS=spy["oos"]["Sharpe"],
                              live_OOS=live["oos"]["Sharpe"], pick_keep4a=pk["keep4a"],
                              pick_keep4b=pk["keep4b"], nothing_keep4b=nothing["keep4b"])
                    r8rows.append(r8)
                    say(f"   RULE 8 H={mh:3d} {fill:8s} {kind:8s} IS-argmax = look {ks[j][3]} / "
                        f"ROT {ks[j][4]:.2f} (IS Sh {r8['pick_IS']:.4f}) -> OOS "
                        f"{r8['pick_OOS']:.4f} vs do-nothing {r8['donothing_OOS']:.4f} "
                        f"({r8['delta']:+.4f})  cellmean {r8['cellmean_OOS']:.4f} worst "
                        f"{r8['worst_OOS']:.4f}  rank corr {r8['rank_IS_OOS']:+.2f}")

        # ---- gates
        z = [cells[k] for k in cells if k[4] == 0.0 and k[1] == "RESPREAD" and k[0] == A_H]
        d0 = max(abs(c["full_Sharpe"] - z[0]["full_Sharpe"]) for c in z)
        gate(f"G2 ROT=0.00 identical across BETA_LOOK and ROT_KIND ({pname})", f"{d0:.3e}",
             "== 0.0", d0 == 0.0)
        dose = cells[(A_H, "RESPREAD", "LOWBETA", 126, 1.00)]
        gate(f"G3 the mechanism has a dose ({pname})",
             f"rotates at {dose['rot_week_share']:.1%} of rebalances, {dose['rot_slots_mean']:.2f} "
             f"slots/week, freed {dose['freed_mean']:.2f}/week", "> 0", dose["rot_week_share"] > 0)
        for fill in FILLS:
            lo = cells[(0, fill, "LOWBETA", 126, 1.00)]["book_beta"]
            hi = cells[(0, fill, "HIGHBETA", 126, 1.00)]["book_beta"]
            gate(f"G4 beta axis does what it says ({pname}/{fill}, H=0, ROT=1.00)",
                 f"LOWBETA {lo:.4f} < HIGHBETA {hi:.4f}", "LOWBETA below", lo < hi)
        gset = max(cells[k]["gross_set_max"] for k in cells)
        gmax = max(cells[k]["gross_max"] for k in cells)
        gdrift = max(cells[k]["gross_max"] for k in cells if k[4] == 0.0)
        gate(f"G7 no leverage ({pname}) — gross SET at each rebalance; the drifted intra-week "
             f"figure is published, not gated, because the DO-NOTHING book drifts identically",
             f"max gross set {gset:.6f}; max drifted {gmax:.4f} (ROT=0 book {gdrift:.4f})",
             "set <= 0.750001", gset <= 0.750001)
        if pname == "U56":
            q = p_px.loc[:VINTAGE]
            vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
            S, NSL, _ = build(vpan, "LOWBETA", 126, 0.0, H=A_H)
            rv = run(vpan, S, NSL, "RESPREAD")[0]
            tv = stats(rv[WARMUP:])
            err = max(abs(tv["CAGR"] - COMMITTED_U56[0]), abs(tv["Sharpe"] - COMMITTED_U56[1]),
                      abs(tv["MaxDD"] - COMMITTED_U56[2]))
            gate(f"G1 vintage-pinned replay (U56 RESPREAD ROT=0 @ {VINTAGE.date()})",
                 f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                 f"committed {COMMITTED_U56[0]:.4%}/{COMMITTED_U56[1]:.4f}/{COMMITTED_U56[2]:.4%}, "
                 "err < 1e-4", err < 1e-4)
            a0 = cells[(A_H, "RESPREAD", "LOWBETA", 126, 0.0)]
            gate("G6 one-extra-day cache drift (U56 RESPREAD ROT=0)",
                 f"CAGR {a0['full_CAGR']-tv['CAGR']:+.4%} Sharpe {a0['full_Sharpe']-tv['Sharpe']:+.4f} "
                 f"MaxDD {(a0['full_MaxDD']-tv['MaxDD'])*100:+.4f}pp",
                 "published, not toleranced", True)

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G5 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    chk = []
    for kind in ("LOWBETA", "HIGHBETA"):
        for rot in ROTS:
            S, NSL, _ = build(pan, kind, 126, rot, H=A_H)
            r = run(pan, S, NSL, "RESPREAD")[0]
            chk.append(sharpe(r[WARMUP:]))
    ref = [grid[(grid.panel == "U56") & (grid.minhold == A_H) & (grid.fill == "RESPREAD")
                & (grid.kind == kind) & (grid.look == 126) & (grid.rot == rot)].full_Sharpe.iloc[0]
           for kind in ("LOWBETA", "HIGHBETA") for rot in ROTS]
    dd = float(np.max(np.abs(np.array(chk) - np.array(ref))))
    gate("G5 determinism (U56 RESPREAD look=126 grid re-run)", f"{dd:.3e}", "== 0.0", dd == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- summary
    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for mh in MINHOLDS:
            for fill in FILLS:
                g = grid[(grid.panel == pname) & (grid.minhold == mh) & (grid.fill == fill)]
                z = g[g.rot == 0.0].iloc[0]
                say(f"   {pname:9s} H={mh:3d} {fill:8s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                    f"ROT=0 {z.full_CAGR:6.2%}/{z.full_Sharpe:.4f}/{z.full_MaxDD:7.2%} (4b "
                    f"{'PASS' if z.keep4b else 'FAIL(' + z.fail4b + ')'})   MaxDD "
                    f"{g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   CAGR "
                    f"{g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   rot slots/wk "
                    f"{g.rot_slots_mean.max():.2f}")
    say("\n   THE DIRECT COMPARISON — ROTATION vs DE-GROSSING (the same freed slots, "
        "the same week):")
    for pname in grid.panel.unique():
        for mh in MINHOLDS:
            q = grid[(grid.panel == pname) & (grid.minhold == mh)]
            cz = q[(q.fill == "CASH") & (q.rot == 0.0)].iloc[0]
            rz = q[(q.fill == "RESPREAD") & (q.rot == 0.0)].iloc[0]
            say(f"   {pname:9s} H={mh:3d} de-gross-to-CASH {cz.full_CAGR:6.2%}/"
                f"{cz.full_Sharpe:.4f}/{cz.full_MaxDD:7.2%} (4b "
                f"{'PASS' if cz.keep4b else 'FAIL(' + cz.fail4b + ')'})  vs RE-SPREAD "
                f"{rz.full_CAGR:6.2%}/{rz.full_Sharpe:.4f}/{rz.full_MaxDD:7.2%} (4b "
                f"{'PASS' if rz.keep4b else 'FAIL(' + rz.fail4b + ')'})")
            for kind in KINDS:
                b = q[(q.fill == "CASH") & (q.kind == kind) & (q.rot == 1.0)]
                b = b.groupby("look").mean(numeric_only=True)
                for look, r in b.iterrows():
                    say(f"      CASH + {kind:8s} look {look:3d} ROT 1.00: {r.full_CAGR:6.2%}/"
                        f"{r.full_Sharpe:.4f}/{r.full_MaxDD:7.2%}  vs cash "
                        f"CAGR {(r.full_CAGR-cz.full_CAGR)*100:+5.2f}pp Sharpe "
                        f"{r.full_Sharpe-cz.full_Sharpe:+.4f} MaxDD "
                        f"{(r.full_MaxDD-cz.full_MaxDD)*100:+5.2f}pp OOS "
                        f"{r.oos_Sharpe-cz.oos_Sharpe:+.4f}")
    say("\n   THE BETA CHANNEL (LOWBETA minus its RANDOM control at the same ROT — exposure "
        "differenced out):")
    for pname in grid.panel.unique():
      for mh in MINHOLDS:
        for fill in FILLS:
            ds = []
            for rot in ROTS[1:]:
                q = grid[(grid.panel == pname) & (grid.minhold == mh) & (grid.fill == fill)]
                lo = q[(q.kind == "LOWBETA") & (q.rot == rot)]
                rd = q[(q.kind == "RANDOM") & (q.rot == rot)]
                ds.append((lo.full_CAGR.mean() - rd.full_CAGR.mean(),
                           lo.full_Sharpe.mean() - rd.full_Sharpe.mean(),
                           lo.full_MaxDD.mean() - rd.full_MaxDD.mean(),
                           lo.oos_Sharpe.mean() - rd.oos_Sharpe.mean(),
                           lo.book_beta.mean() - rd.book_beta.mean()))
            a = np.array(ds)
            say(f"   {pname:9s} H={mh:3d} {fill:8s} n={len(ds)} rungs  d_CAGR "
                f"{a[:,0].mean()*100:+5.2f}pp  "
                f"d_Sharpe {a[:,1].mean():+.4f} (>0 at {int((a[:,1]>0).sum())}/{len(ds)})  "
                f"d_MaxDD {a[:,2].mean()*100:+5.2f}pp (>0 at {int((a[:,2]>0).sum())}/{len(ds)})  "
                f"d_OOS {a[:,3].mean():+.4f}  d_beta {a[:,4].mean():+.3f}")
    say(f"\n   RULE 8 chooser-minus-do-nothing: mean {wf.delta.mean():+.4f}  positive at "
        f"{int((wf.delta > 0).sum())} of {len(wf)}   IS/OOS rank corr mean "
        f"{wf.rank_IS_OOS.mean():+.3f}")
    for mh in MINHOLDS:
        for fill in FILLS:
            w = wf[(wf.fill == fill) & (wf.minhold == mh)]
            say(f"      H={mh:3d} {fill:8s} mean {w.delta.mean():+.4f} positive at "
                f"{int((w.delta>0).sum())} of {len(w)}; picks 4b PASS at "
                f"{int(w.pick_keep4b.sum())} of {len(w)}")
    zero = grid[grid.rot == 0.0]
    conv = grid[[(not zero[(zero.panel == r.panel) & (zero.fill == r.fill)
                           & (zero.minhold == r.minhold)].keep4b.iloc[0]) and r.keep4b
                 for _, r in grid.iterrows()]]
    say(f"   4b CONVERSIONS (the do-nothing cell fails 4b, the rotated cell passes): {len(conv)} "
        f"of {len(grid)} cells")
    for _, r in conv.head(20).iterrows():
        say(f"      {r.panel:9s} H={r.minhold:3d} {r.fill:8s} {r.kind:8s} look {r.look} "
            f"ROT {r.rot:.2f}: "
            f"{r.full_CAGR:6.2%}/{r.full_Sharpe:.4f}/{r.full_MaxDD:7.2%} OOS {r.oos_Sharpe:.4f}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
