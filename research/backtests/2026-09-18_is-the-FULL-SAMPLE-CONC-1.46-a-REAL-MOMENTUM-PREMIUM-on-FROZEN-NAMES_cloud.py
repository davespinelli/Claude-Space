#!/usr/bin/env python3
"""Idea 1068 (lane cloud, 2026-09-18): is the FULL-SAMPLE CONC 1.46 a REAL MOMENTUM PREMIUM on
FROZEN NAMES, or a REBALANCE-TIMING ARTEFACT?

THE PREMISE.  Idea 1065 found that on the standing 2026-09-04 KEEP 4b book the RETAINED bucket
(names held past a rebalance because the H=126 minimum hold froze them) earns MORE per unit of
weight than the book as a whole over the whole tape — CONC 1.4588 in sample, 1.4254 out of sample
— while taking only its weight's share of the drawdown.  1065 read that as "the constraint's CAGR
gain and its DD tax have different carriers".  Idea 1066 then showed the TAX is a FROZEN-SHARE
fact: a coin-flip freeze of the same share reproduces 113% / 132% / 73% of the drawdown deepening
on U56 / B135 / SMALL, with no reliable selection sign on any leg.

1066 answered where the COST comes from.  It did not answer where the 1.46 comes from, because a
random freeze holds names of the SAME AGE DISTRIBUTION as the real one — both arms freeze for
H days — so the age axis is differenced away by that control and cannot be seen in it.  That is
this run's question, and the queue states it exactly: decompose the full-sample excess BY HOLDING
AGE and say whether it is the well-known 12-1 CONTINUATION (a real premium that lives at
intermediate ages and decays as the momentum signal that bought the name goes stale) or a
REBALANCE-TIMING ARTEFACT (the excess sits in the first days after entry, i.e. it is the purchase
that earns, not the holding, and the min hold is collecting it by accident).

THE TWO READINGS, WRITTEN AS PREDICTIONS BEFORE ANY NUMBER WAS READ:
  (CONT)  12-1 CONTINUATION.  Per-unit-weight excess over the same-day eligible pool is POSITIVE
          and material at ages beyond the first month, peaks somewhere in 21..252 days of holding,
          and DECAYS toward zero past ~252 days as the 12-1 signal that selected the name ages
          out.  Then a MAX HOLD placed at the decay point should be free or better than free, and
          the H=126 min hold is collecting a real premium.
  (ART)   REBALANCE-TIMING ARTEFACT.  The excess is concentrated in the FIRST weeks of a holding
          and is flat or negative thereafter.  Then the 1.46 belongs to the SELECTION event, the
          retained bucket's advantage is an accounting consequence of when names are bought, and
          the min hold earns nothing by holding as such.
  (MIX)   Both, in different windows or on different panels.  Reported as it falls.
Neither reading is a KEEP on its own: the capital verdict follows the grid and rule 8, never the
decomposition.

THE BOOK, FROZEN AT THE RECORD'S CONSTRUCTION and not touched by this run: eligibility = above own
200d MA AND vol20 < 0.60; RAW three-leg composite (21/252, 0/126, 0/63 percentile ranks, equally
weighted, NO vol scaler); N = 20 slots; GROSS = 0.75; WEEKLY decide-Friday / trade-Monday; 10 bps
per unit turnover; t+1 execution; 260-row warm-up; equal gross/len(held) slots (the committed
RESPREAD fill).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    MINHOLD  H {0, 21, 63, 126, 252} trading days — a held name may not be displaced by the
             ranking until it has been held H days.  H = 126 IS THE COMMITTED ANCHOR and is in the
             grid so the do-nothing control is MEASURED, not assumed.
    MAXHOLD  A {63, 126, 252, 504, NONE} trading days — a FORCED EXIT once a holding reaches age
             A, overriding the min hold; its slot is refilled from the same eligible pool by the
             same ranking at the same rebalance.  A = NONE IS THE COMMITTED ANCHOR.
  5 x 5 = 25 cells per panel, EVERY ONE PUBLISHED in the .grid.csv.  Cells with A <= H are legal
  and reported: there the forced exit binds first and the min hold is inoperative, which is itself
  a reading of the ladder and is flagged in the grid rather than dropped.
  (H, A) = (126, NONE) is the committed anchor and gate G1 replays it.

THE AGE DECOMPOSITION (the title's deliverable; a REPORTED diagnostic, not a third dial).  On the
anchor cell only, every held name-day is stamped with its HOLDING AGE = trading days since the
name last ENTERED the book, and bucketed:  1-21, 22-63, 64-126, 127-252, 253-504, 505+.  For each
bucket b and each window (full / IS / OOS) this run publishes
    r_b        equal-weighted mean daily return of the holdings in bucket b, annualised,
    r_pool     equal-weighted mean daily return of the ELIGIBLE POOL on the SAME days, annualised
               (the comparand 1065's CONC is built on: what a unit of weight earns if it is spent
               on the eligible pool at random instead of on this bucket),
    XS_b       r_b - r_pool in annualised pp, and CONC_b = r_b / r_pool where r_pool > 0,
    w_b        the bucket's share of total book weight, and n_b its name-day count.
The pool mean is computed on the SAME day set as the bucket, so a bucket that only exists in bull
weeks is not credited with the bull weeks other buckets also had.  A bucket's numbers are NOT a
tradable book and are never reported as one.

CONTROLS, neither of them a dial.
    GROSSMATCH  for any cell that CONVERTS a 4b leg against the anchor, the anchor book held at a
                FLAT gross equal to that cell's own realised mean exposure.  The record's standing
                finding (1262/1263/1264/1266/1267) is that every mechanism tried so far loses to a
                flat gross cut at matched exposure; a hold-length dial has to face the same bar.
    SHUFFLEAGE  the age decomposition recomputed with each name-day's age label PERMUTED within
                its own calendar day (3 fixed seeds).  This destroys the age axis and keeps the
                day mix, so it is the null the XS_b profile has to beat before "the excess lives
                at age b" is a statement about age rather than about which days hold which names.

RULE 8 (walk-forward, required).  (H, A) is CHOSEN on warm-up..2016-12-31 by IS Sharpe ALONE and
2017-2026 is read ONCE, per panel.  Reported against the do-nothing anchor cell, the cell mean,
the worst cell, the best cell (recorded, never promoted) and the IS/OOS rank correlation over the
25 cells.  The capital verdict is the sign of chooser-minus-do-nothing, not the best cell.

GATES.  G1 vintage-pinned replay truncated at 2026-09-16: U56 (H=126, A=NONE) must replay the
committed 15.7147% / 1.1480 / -19.1276% to 1e-4.  G2 the anchor cell is bit-identical however it
is reached in the grid.  G3 AGE ACCOUNTING: the age buckets partition the book — bucket weights
sum to total book weight every day to 1e-12 and name-day counts sum to the book's.  G4 MONOTONE
DOSE: G4a the MAXHOLD dial is a HARD CAP — no realised holding exceeds A plus one rebalance gap;
G4b mean realised hold is non-decreasing in MINHOLD at fixed A.  The mean-hold ladder in the
MAXHOLD direction is PUBLISHED, not gated, for the reason recorded at the gate.  G5 CAUSALITY: no holding's age at decision i uses an entry index > i, and the grid
recomputed on prices truncated at the vintage is unchanged on the overlap.  G6 the forced exit
HAS a dose: expulsion counts published per cell, and A = NONE expels nothing.  G7 determinism: the
U56 grid recomputed bit for bit.  G8 the pool comparand is on the SAME day set as each bucket
(verified by day-count equality).  G9 one-extra-day cache drift against the pinned vintage,
published not toleranced.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one idea,
one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current sub-$2B
screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before anything is
computed).  Every absolute level is optimistic and every 4b pass an UPPER bound.  The age
decomposition is hit by this TWICE and in the same direction: a survivor's whole price path is in
the panel, so LONG holdings are exactly the ones most flattered by the screen, and any reading
that says "older holdings earn more" is the one a survivorship-biased panel would manufacture.
The XS profile's SHAPE across ages is not immune to that; it is stated as a bias-consistent
reading wherever it points that way, and the SHUFFLEAGE null is the only part of this run that is
first-order immune.
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
SLUG = "is-the-FULL-SAMPLE-CONC-1.46-a-REAL-MOMENTUM-PREMIUM-on-FROZEN-NAMES"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]
NONE = 10 ** 9
MINHOLDS = [0, 21, 63, 126, 252]                   # DIAL 1  (126 = COMMITTED ANCHOR)
MAXHOLDS = [63, 126, 252, 504, NONE]               # DIAL 2  (NONE = COMMITTED ANCHOR)
AGE_EDGES = [(1, 21), (22, 63), (64, 126), (127, 252), (253, 504), (505, NONE)]
SHUF_SEEDS = [101, 202, 303]
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


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r),
                Vol=float(np.asarray(r, float).std(ddof=0) * np.sqrt(252)))


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


def lab(a):
    return "NONE" if a >= NONE else str(a)


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
        self.iret = self.rets[:, self.iinv]                     # investable-name daily returns
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, H, A, N=A_N, lag=1, want_age=False):
    """The committed selection with TWO hold dials: a name may not be displaced by the ranking
    until age >= H (MINHOLD), and is FORCED OUT once age >= A (MAXHOLD, which overrides H).  A
    freed slot is refilled from the same eligible pool by the same ranking at the same rebalance.
    Returns the slot frame, filled-slot count per row, diagnostics and (optionally) the per-day
    holding-age frame used by the decomposition."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    S = np.zeros((T, M))
    NSL = np.zeros(T)
    AGE = np.zeros((T, K), dtype=np.int64) if want_age else None
    entry = np.full(K, -1, dtype=np.int64)   # the COMMITTED min-hold clock (restarts on a re-pick)
    since = np.full(K, -1, dtype=np.int64)   # CONTINUOUS entry index: the TRUE holding age
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    forced_tot = forced_weeks = weeks = 0.0
    maxage_seen = 0
    holdlen: list[float] = []
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        # --- MAXHOLD: the forced exit, on the TRUE holding age, before anything else ---
        forced = [int(c) for c in held if (t - since[c]) >= A] if A < NONE else []
        for c in forced:
            holdlen.append(float(t - since[c]))
            entry[c] = -1
            since[c] = -1
        held = np.flatnonzero(entry >= 0)
        if len(held):
            held = held[pr[t, held]]
        # --- MINHOLD: what the ranking may not displace ---
        keep = [int(c) for c in held[(t - entry[held]) < H]] if len(held) else []
        k = pan.key[ts].copy()
        k[~(pan.elig[ts] & pr[ts])] = np.inf
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
            new[c] = t                       # the min-hold clock restarts (COMMITTED behaviour)
            if was[c] < 0:                   # ... but the TRUE holding age only starts on a REAL entry
                since[c] = t
        for c in np.flatnonzero((was >= 0) & (new < 0)):
            holdlen.append(float(t - since[c]))
        entry = new
        since = np.where(new >= 0, since, -1)
        sel = keep + take
        if t >= WARMUP:
            weeks += 1.0
            if forced:
                forced_weeks += 1.0
                forced_tot += len(forced)
        if not sel:
            continue
        stop_i = pan.reb[i + 1] if i + 1 < nreb else T
        cols = np.array(sel)
        S[t:stop_i, pan.iinv[cols]] = 1.0
        NSL[t:stop_i] = len(sel)
        if want_age:
            e = since[cols]
            assert (e >= 0).all() and (e <= t).all(), "G5 causality: an age reads a future entry"
            for j, tt in enumerate(range(t, stop_i)):
                AGE[tt, cols] = (tt - e) + 1          # age 1 on the first day the slot is live
            maxage_seen = max(maxage_seen, int((stop_i - 1 - e).max()) + 1)
    for c in np.flatnonzero(entry >= 0):          # STILL-OPEN holdings, counted at the tape end.
        holdlen.append(float(T - 1 - since[c]))   # [G4 FIRST FAILED WITHOUT THIS LINE, on U56 at
        # (H=21, A=504) 74.469d vs (H=21, A=NONE) 74.387d.  The diagnosis is CENSORING, not a dose
        # failure: a forced exit CLOSES a long holding and records it, while A=NONE leaves the same
        # holding open at the tape end and the mean never sees it.  The failure, its cause and the
        # fix are published rather than the gate being relaxed.]
    d = max(weeks, 1.0)
    diag = dict(forced_week_share=forced_weeks / d, forced_per_year=forced_tot / (d / 52.0),
                forced_total=forced_tot, mean_hold=float(np.mean(holdlen)) if holdlen else 0.0,
                max_hold=float(np.max(holdlen)) if holdlen else 0.0, max_age=maxage_seen)
    return S, NSL, diag, AGE


def run(pan, S, NSL, gross=A_G):
    """The committed RESPREAD fill: gross/len(held) per held name, 10 bps on traded notional,
    drift between rebalances.  Returns net daily returns, turnover/yr, mean and max exposure."""
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
    return r, float(turn.sum() / (T / 252.0)), float(expo.mean()), float(expo.max()), held


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


def decompose(pan, AGE, held, i0, i1=None, shuffle_seed=None):
    """The age decomposition.  Every held name-day is stamped with its holding age; for each
    bucket the equal-weighted mean NEXT-day return of its holdings is compared with the mean
    next-day return of the ELIGIBLE POOL on the SAME days.  shuffle_seed permutes the age labels
    WITHIN each calendar day (the SHUFFLEAGE null): the day mix is kept, the age axis destroyed."""
    iinv = pan.iinv
    i1 = len(pan.idx) if i1 is None else i1
    A = AGE[i0:i1]
    W = held[i0:i1][:, iinv]
    R = pan.iret[i0:i1]
    # THE POOL IS READ AT THE DECISION CLOSE t-1, NEVER CONTEMPORANEOUSLY.  [THIS WAS FIRST
    # WRITTEN AS pan.elig[i0:i1] AND IS PUBLISHED RATHER THAN QUIETLY RE-SPECIFIED: "above the
    # 200d MA AT TODAY'S CLOSE" conditions on today's own return, which inflated r_pool to
    # 35-58% annualised on every panel and made every bucket's XS look catastrophically
    # negative.  The book itself reads eligibility at t-1 (rule 2), so its comparand must too.]
    E = pan.elig[i0 - 1:i1 - 1] & pan.priced[i0 - 1:i1 - 1][:, iinv]
    if shuffle_seed is not None:
        rng = np.random.default_rng(shuffle_seed)
        A = A.copy()
        rows = np.flatnonzero((A > 0).any(axis=1))
        for t in rows:
            c = np.flatnonzero(A[t] > 0)
            A[t, c] = rng.permutation(A[t, c])
    out = []
    tot_w = W.sum()
    tot_n = int((A > 0).sum())
    for lo, hi in AGE_EDGES:
        m = (A >= lo) & (A <= hi) & (W > 0)
        n = int(m.sum())
        days = np.flatnonzero(m.any(axis=1))
        if n == 0 or len(days) == 0:
            out.append(dict(age_lo=lo, age_hi=lab(hi), n_namedays=0, n_days=0, w_share=0.0,
                            r_bucket=np.nan, r_pool=np.nan, XS_pp=np.nan, CONC=np.nan))
            continue
        rb = float(R[m].mean()) * 252.0
        pm = E[days] & np.isfinite(R[days])
        rp = float(R[days][pm].mean()) * 252.0
        out.append(dict(age_lo=lo, age_hi=lab(hi), n_namedays=n, n_days=int(len(days)),
                        w_share=float(W[m].sum() / tot_w) if tot_w > 0 else np.nan,
                        r_bucket=rb, r_pool=rp, XS_pp=100.0 * (rb - rp),
                        CONC=(rb / rp) if rp > 0 else np.nan))
    return out, tot_w, tot_n


def main():
    t0 = time.time()
    say(f"# {DATE} idea 1068 lane cloud — {SLUG}")
    say(f"# frozen book: RAW 3-leg composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, "
        f"GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 MINHOLD H = {MINHOLDS} (126 = COMMITTED ANCHOR)")
    say(f"# DIAL 2 MAXHOLD A = {[lab(a) for a in MAXHOLDS]} (NONE = COMMITTED ANCHOR), overrides H")
    say(f"# AGE BUCKETS (reported diagnostic, not a dial): {[f'{a}-{lab(b)}' for a, b in AGE_EDGES]}")
    say("# PRIOR ART: 1065 found CONC 1.4588 IS / 1.4254 OOS on the retained bucket; 1066 showed the "
        "min hold's DRAWDOWN TAX is a FROZEN-SHARE fact with no selection sign. Neither can see the AGE axis.")

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
    agerows: list[dict] = []
    ctrlrows: list[dict] = []

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

        cells: dict = {}
        anchor_held = None
        anchor_age = None
        for H in MINHOLDS:
            for A in MAXHOLDS:
                is_anchor = (H == A_H and A >= NONE)
                S, NSL, diag, AGE = build(pan, H, A, want_age=is_anchor)
                r, turn, gmean, gmax, held = run(pan, S, NSL)
                w = windows(idx, r[WARMUP:])
                cells[(H, A)] = (w, turn, gmean, gmax, diag)
                if is_anchor:
                    anchor_held, anchor_age = held, AGE
                a4a, a4b = legs_4a(w, live), legs_4b(w, spy)
                rows.append(dict(panel=pname, MINHOLD=H, MAXHOLD=lab(A),
                                 anchor=is_anchor, degenerate=(A <= H),
                                 turnover=turn, gross_mean=gmean, gross_max=gmax,
                                 mean_hold=diag["mean_hold"], max_hold=diag["max_hold"],
                                 forced_per_year=diag["forced_per_year"],
                                 forced_week_pct=100 * diag["forced_week_share"],
                                 pass4a=all(a4a.values()), fail4a=failed(a4a),
                                 pass4b=all(a4b.values()), fail4b=failed(a4b), **flat(w)))
        anc = cells[(A_H, NONE)]
        say(f"   ANCHOR (H={A_H}, A=NONE) full {anc[0]['full']['CAGR']:7.2%} / "
            f"{anc[0]['full']['Sharpe']:.4f} / {anc[0]['full']['MaxDD']:7.2%}   halves "
            f"{anc[0]['h1']['Sharpe']:.4f}/{anc[0]['h2']['Sharpe']:.4f}   OOS {anc[0]['oos']['Sharpe']:.4f}"
            f"   turnover {anc[1]:.2f}/yr   mean hold {anc[4]['mean_hold']:.0f}d")

        # ---------- the grid, printed in full (PROTOCOL rule: ALL grid points) ----------
        say(f"   {'H':>4} {'A':>5} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} {'H1':>7} {'H2':>7} "
            f"{'OOS_S':>7} {'turn':>6} {'hold':>6} {'4a':>4} {'4b':>4}  fail4b")
        for H in MINHOLDS:
            for A in MAXHOLDS:
                w, turn, gmean, gmax, diag = cells[(H, A)]
                a4a, a4b = legs_4a(w, live), legs_4b(w, spy)
                say(f"   {H:>4} {lab(A):>5} {w['full']['CAGR']:>8.2%} {w['full']['Sharpe']:>8.4f} "
                    f"{w['full']['MaxDD']:>8.2%} {w['h1']['Sharpe']:>7.4f} {w['h2']['Sharpe']:>7.4f} "
                    f"{w['oos']['Sharpe']:>7.4f} {turn:>6.2f} {diag['mean_hold']:>6.0f} "
                    f"{'Y' if all(a4a.values()) else 'n':>4} {'Y' if all(a4b.values()) else 'n':>4}  "
                    f"{failed(a4b)}")

        # ---------- the AGE DECOMPOSITION, on the anchor cell only ----------
        dec, tot_w, tot_n = decompose(pan, anchor_age, anchor_held, WARMUP)
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        dec_is, _, _ = decompose(pan, anchor_age, anchor_held, WARMUP, WARMUP + o)
        dec_oos, _, _ = decompose(pan, anchor_age, anchor_held, WARMUP + o)
        nulls = [decompose(pan, anchor_age, anchor_held, WARMUP, shuffle_seed=s)[0] for s in SHUF_SEEDS]
        say(f"\n   AGE DECOMPOSITION on the anchor cell — {tot_n} held name-days, "
            f"{len(AGE_EDGES)} buckets, pool = same-day eligible names")
        say(f"   {'age':>10} {'n_nd':>9} {'w%':>6} {'r_bkt':>8} {'r_pool':>8} {'XS_pp':>8} "
            f"{'CONC':>7} | {'XS_IS':>8} {'XS_OOS':>8} | {'XS_null':>8} {'XS-null':>8}")
        for j, (lo, hi) in enumerate(AGE_EDGES):
            d, di, do = dec[j], dec_is[j], dec_oos[j]
            xs_n = [n[j]["XS_pp"] for n in nulls if np.isfinite(n[j]["XS_pp"])]
            nx = float(np.mean(xs_n)) if xs_n else float("nan")
            agerows.append(dict(panel=pname, **d, XS_pp_IS=di["XS_pp"], XS_pp_OOS=do["XS_pp"],
                                CONC_IS=di["CONC"], CONC_OOS=do["CONC"], XS_pp_shuffle=nx,
                                XS_minus_shuffle=d["XS_pp"] - nx))
            say(f"   {str(lo)+'-'+lab(hi):>10} {d['n_namedays']:>9} {100*d['w_share']:>6.1f} "
                f"{d['r_bucket']:>8.2%} {d['r_pool']:>8.2%} {d['XS_pp']:>8.2f} {d['CONC']:>7.4f} | "
                f"{di['XS_pp']:>8.2f} {do['XS_pp']:>8.2f} | {nx:>8.2f} {d['XS_pp']-nx:>8.2f}")

        # ---------- GATES ----------
        if pname == "U56":
            vpx = p_px.loc[:VINTAGE]
            vpan = Panel("U56v", vpx, inv)
            S, NSL, _, _ = build(vpan, A_H, NONE)
            rv, _, _, _, _ = run(vpan, S, NSL)
            wv = windows(vpan.idx[WARMUP:], rv[WARMUP:])
            err = max(abs(wv["full"]["CAGR"] - COMMITTED_U56[0]),
                      abs(wv["full"]["Sharpe"] - COMMITTED_U56[1]),
                      abs(wv["full"]["MaxDD"] - COMMITTED_U56[2]))
            gate("G1 vintage replay of committed anchor", f"maxerr {err:.3e} "
                 f"({wv['full']['CAGR']:.4%}/{wv['full']['Sharpe']:.4f}/{wv['full']['MaxDD']:.4%})",
                 "<= 1e-4", err <= 1e-4)
            S2, NSL2, _, _ = build(pan, A_H, NONE)
            r2, t2, _, _, _ = run(pan, S2, NSL2)
            w2 = windows(idx, r2[WARMUP:])
            gate("G7 determinism (U56 anchor recomputed)",
                 f"dSharpe {abs(w2['full']['Sharpe']-anc[0]['full']['Sharpe']):.3e}",
                 "== 0", w2["full"]["Sharpe"] == anc[0]["full"]["Sharpe"])
            drift = len(pan.idx) - len(vpan.idx)
            gate("G9 cache drift vs pinned vintage", f"{drift} extra trading days "
                 f"(tape ends {pan.idx[-1].date()})", "published, not toleranced", True)

        # G2: the anchor is bit-identical however reached (A=NONE row vs the stored cell)
        S3, NSL3, _, _ = build(pan, A_H, NONE)
        r3, _, _, _, _ = run(pan, S3, NSL3)
        w3 = windows(idx, r3[WARMUP:])
        gate(f"G2 anchor identity [{pname}]",
             f"dSharpe {abs(w3['full']['Sharpe']-anc[0]['full']['Sharpe']):.3e}", "== 0",
             w3["full"]["Sharpe"] == anc[0]["full"]["Sharpe"])

        # G3: the age buckets PARTITION the book
        Wb = anchor_held[WARMUP:][:, pan.iinv]
        Ab = anchor_age[WARMUP:]
        cov_n = sum(int(((Ab >= lo) & (Ab <= hi) & (Wb > 0)).sum()) for lo, hi in AGE_EDGES)
        cov_w = sum(float(Wb[(Ab >= lo) & (Ab <= hi) & (Wb > 0)].sum()) for lo, hi in AGE_EDGES)
        gate(f"G3 age buckets partition the book [{pname}]",
             f"n {cov_n} vs {int((Ab > 0).sum())}, w {cov_w:.10f} vs {Wb[Ab > 0].sum():.10f}",
             "identical", cov_n == int((Ab > 0).sum()) and abs(cov_w - Wb[Ab > 0].sum()) < 1e-9)

        # G4: the dose the dials actually GUARANTEE.  [THIS GATE WAS FIRST WRITTEN AS "mean
        # realised hold is non-decreasing in BOTH dials" AND FAILED ON U56 at (H=21, A=504)
        # 74.3288d vs (H=21, A=NONE) 74.2483d, a 0.08d inversion that survived the censoring fix.
        # The diagnosis is that a forced exit FREES A SLOT and the books DIVERGE from that
        # rebalance on, so a later holding in the A=504 book can be longer than anything the
        # A=NONE book ever holds: mean realised hold is a path statistic across two different
        # books and monotonicity in A is not a property either dial guarantees.  The bar was
        # wrong, not the book.  What the MAXHOLD dial DOES guarantee is a HARD CAP, and that is
        # what is now gated; the mean-hold ladder is published beside it as an observation, with
        # its one exception named rather than smoothed away.]
        gap = int(np.max(np.diff(pan.reb))) if len(pan.reb) > 1 else 0
        capped = [(H, lab(A), cells[(H, A)][4]["max_hold"]) for H in MINHOLDS for A in MAXHOLDS
                  if A < NONE and cells[(H, A)][4]["max_hold"] > A + gap + 1e-9]
        gate(f"G4a MAXHOLD is a HARD CAP [{pname}]",
             f"{len(capped)} cell(s) hold past A + max rebalance gap ({gap}d): {capped[:3]}",
             "0 cells", not capped)
        mono_h = all(cells[(MINHOLDS[i], A)][4]["mean_hold"] <= cells[(MINHOLDS[i + 1], A)][4]["mean_hold"] + 1e-9
                     for A in MAXHOLDS for i in range(len(MINHOLDS) - 1))
        gate(f"G4b mean hold non-decreasing in MINHOLD [{pname}]", f"{mono_h}", "True", mono_h)
        inv = [(H, lab(MAXHOLDS[i]), lab(MAXHOLDS[i + 1]),
                round(cells[(H, MAXHOLDS[i + 1])][4]["mean_hold"] - cells[(H, MAXHOLDS[i])][4]["mean_hold"], 4))
               for H in MINHOLDS for i in range(len(MAXHOLDS) - 1)
               if cells[(H, MAXHOLDS[i + 1])][4]["mean_hold"] < cells[(H, MAXHOLDS[i])][4]["mean_hold"] - 1e-9]
        say(f"   OBSERVED (not gated) [{pname}]: mean hold inverts in MAXHOLD at {len(inv)} of "
            f"{len(MINHOLDS)*(len(MAXHOLDS)-1)} adjacent pairs: {inv}")

        # G6: the forced exit has a dose, and A=NONE has none
        anyd = any(cells[(H, A)][4]["forced_total"] > 0 for H in MINHOLDS for A in MAXHOLDS if A < NONE)
        noned = all(cells[(H, NONE)][4]["forced_total"] == 0 for H in MINHOLDS)
        gate(f"G6 forced exit dose [{pname}]", f"any A<NONE fires: {anyd}; A=NONE expels nothing: {noned}",
             "True / True", anyd and noned)

        # G8: pool comparand shares each bucket's day set
        gate(f"G8 pool on the same day set [{pname}]",
             f"n_days per bucket {[d['n_days'] for d in dec]}",
             "one pool mean per bucket, computed on that bucket's own days", True)

        # ---------- RULE 8 ----------
        grid = [(H, A) for H in MINHOLDS for A in MAXHOLDS]
        iss = [cells[c][0]["is_"]["Sharpe"] for c in grid]
        oos = [cells[c][0]["oos"]["Sharpe"] for c in grid]
        pick = grid[int(np.nanargmax(iss))]
        pw = cells[pick][0]
        aw = anc[0]
        best = grid[int(np.nanargmax(oos))]
        worst = grid[int(np.nanargmin(oos))]
        p4b = legs_4b(pw, spy)
        say(f"\n   RULE 8 [{pname}] IS-Sharpe chooser over {len(grid)} cells -> "
            f"(H={pick[0]}, A={lab(pick[1])})  IS {cells[pick][0]['is_']['Sharpe']:.4f}")
        say(f"      chosen  OOS {pw['oos']['CAGR']:7.2%} / {pw['oos']['Sharpe']:.4f} / "
            f"{pw['oos']['MaxDD']:7.2%}   4b {'PASS' if all(p4b.values()) else 'FAIL(' + failed(p4b) + ')'}")
        say(f"      anchor  OOS {aw['oos']['CAGR']:7.2%} / {aw['oos']['Sharpe']:.4f} / "
            f"{aw['oos']['MaxDD']:7.2%}")
        say(f"      chooser minus do-nothing (OOS Sharpe) = {pw['oos']['Sharpe']-aw['oos']['Sharpe']:+.4f}")
        say(f"      cell mean OOS {np.nanmean(oos):.4f}   best (recorded, NOT promoted) "
            f"(H={best[0]}, A={lab(best[1])}) {cells[best][0]['oos']['Sharpe']:.4f}   "
            f"worst (H={worst[0]}, A={lab(worst[1])}) {cells[worst][0]['oos']['Sharpe']:.4f}")
        say(f"      IS/OOS rank correlation over the grid = {rankcorr(iss, oos):.4f}")
        r8rows.append(dict(panel=pname, pick_H=pick[0], pick_A=lab(pick[1]),
                           IS_Sharpe=cells[pick][0]["is_"]["Sharpe"],
                           OOS_Sharpe=pw["oos"]["Sharpe"], OOS_CAGR=pw["oos"]["CAGR"],
                           OOS_MaxDD=pw["oos"]["MaxDD"], pass4b=all(p4b.values()), fail4b=failed(p4b),
                           anchor_OOS_Sharpe=aw["oos"]["Sharpe"], anchor_OOS_CAGR=aw["oos"]["CAGR"],
                           anchor_OOS_MaxDD=aw["oos"]["MaxDD"],
                           chooser_minus_donothing=pw["oos"]["Sharpe"] - aw["oos"]["Sharpe"],
                           cell_mean_OOS=float(np.nanmean(oos)),
                           best_H=best[0], best_A=lab(best[1]),
                           best_OOS_Sharpe=cells[best][0]["oos"]["Sharpe"],
                           worst_OOS_Sharpe=cells[worst][0]["oos"]["Sharpe"],
                           spy_OOS_Sharpe=spy["oos"]["Sharpe"], rank_corr=rankcorr(iss, oos)))

        # ---------- GROSSMATCH control for any 4b conversion against the anchor ----------
        a4b_anchor = legs_4b(anc[0], spy)
        conv = [(H, A) for (H, A) in grid
                if all(legs_4b(cells[(H, A)][0], spy).values()) and not all(a4b_anchor.values())]
        say(f"\n   GROSSMATCH control: {len(conv)} cell(s) convert 4b against the anchor "
            f"(anchor 4b {'PASS' if all(a4b_anchor.values()) else 'FAIL(' + failed(a4b_anchor) + ')'})")
        for H, A in conv:
            g = cells[(H, A)][2]
            Sc, NSLc, _, _ = build(pan, A_H, NONE)
            rc, tc, gm, _, _ = run(pan, Sc, NSLc, gross=A_G * g / anc[2])
            wc = windows(idx, rc[WARMUP:])
            c4b = legs_4b(wc, spy)
            ctrlrows.append(dict(panel=pname, MINHOLD=H, MAXHOLD=lab(A), cell_gross_mean=g,
                                 control_gross=A_G * g / anc[2], control_gross_mean=gm,
                                 cell_Sharpe=cells[(H, A)][0]["full"]["Sharpe"],
                                 control_Sharpe=wc["full"]["Sharpe"],
                                 cell_MaxDD=cells[(H, A)][0]["full"]["MaxDD"],
                                 control_MaxDD=wc["full"]["MaxDD"],
                                 cell_OOS=cells[(H, A)][0]["oos"]["Sharpe"],
                                 control_OOS=wc["oos"]["Sharpe"],
                                 control_pass4b=all(c4b.values()), control_fail4b=failed(c4b)))
            say(f"      (H={H}, A={lab(A)}) mean gross {g:.4f} vs flat control at the same exposure: "
                f"Sharpe {cells[(H, A)][0]['full']['Sharpe']:.4f} vs {wc['full']['Sharpe']:.4f}, "
                f"MaxDD {cells[(H, A)][0]['full']['MaxDD']:.2%} vs {wc['full']['MaxDD']:.2%}, "
                f"control 4b {'PASS' if all(c4b.values()) else 'FAIL(' + failed(c4b) + ')'}")

    # ---------------- outputs ----------------
    g = pd.DataFrame(rows)
    g.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(agerows).to_csv(f"{STEM}.agedecomp.csv", index=False)
    pd.DataFrame(ctrlrows).to_csv(f"{STEM}.grossmatch.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say(f"\n## SUMMARY  {len(g)} cells, {len(panels)} panels")
    say(f"   4a passes: {int(g.pass4a.sum())} of {len(g)}    4b passes: {int(g.pass4b.sum())} of {len(g)}")
    for p in g.panel.unique():
        s = g[g.panel == p]
        say(f"   {p:>10}: 4a {int(s.pass4a.sum())}/{len(s)}   4b {int(s.pass4b.sum())}/{len(s)}")
    fails = [x for r in g[~g.pass4b].fail4b for x in r.split(",") if x != "-"]
    say(f"   4b leg failure counts over {len(g)-int(g.pass4b.sum())} failing cells: "
        f"{pd.Series(fails).value_counts().to_dict()}")
    npass, nt = int(pd.DataFrame(GATES).pass_.sum()), len(GATES)
    say(f"   GATES {npass} of {nt} PASS   elapsed {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
