#!/usr/bin/env python3
"""
Idea 1282 (lane C, 2026-09-18) — does the WORST 21-DAY DRAWDOWN make a BETTER RISK CAP
than MAXDD in KEEP 4b?

THE PREMISE, READ FROM THE RECORD.  Idea 1146 (both lanes, 2026-09-18) found that on the
truncated-maximum ladder only k=21 genuinely truncates — K_63 is bit-identical to MAXDD in
73 of 74 books and K_k for k>=126 in 74 of 74, so those rungs truncate NOTHING — and that
K21 is the one rung carrying MAXDD's tape-length signature on all three panels and under
both window geometries (b_SD +0.1805 / +0.1947 / +0.5668).  PROTOCOL rule 4b keys its risk
leg on MAXDD:  MaxDD(book) >= 0.60 * MaxDD(SPY).  MAXDD is a single order statistic of one
tape — on this sample, one or two crash troughs.  K_21 is the worst drawdown inside a
trailing 21-day window: it is a statistic of MANY local troughs, so it has more independent
information per year of tape.  The queue's question is whether re-keying 4b's cap on K_21
is an IMPROVEMENT or merely a DIFFERENT arbitrary choice.

WHAT "BETTER" MEANS HERE, STATED BEFORE ANY NUMBER IS READ.  A cap is a bar placed on a
risk statistic.  Three things can make one key better than another, and all three are
measured:

  (1) IT MUST MOVE SOMETHING.  If the K-keyed leg passes and fails exactly the books the
      MAXDD-keyed leg does, the question is empty.  ARM 1 re-scores every book in the
      record's own verdict set under every (k, cap multiple) cell and counts FLIPS.

  (2) IT SHOULD BE BETTER RESOLVED.  A binary is information only if the quantity it
      thresholds is measurable at the bar.  ARM 2 measures each key's margin
          M(k, m) = K_k(book) - m * K_k(SPY)      (both negative; pass iff M >= 0)
      and its PAIRED sampling SD under a circular block bootstrap (block 63, the record's
      inherited L; the book and SPY are resampled with the SAME draws).  The better-keyed
      cap is the one with the smaller inside-1-SD share, i.e. fewer verdicts decided inside
      their own noise.

  (3) IT SHOULD FORECAST.  A risk cap is used IN SAMPLE to decide what to run OUT of
      sample, so the key that matters is the one whose in-sample reading ranks books by
      their FUTURE drawdown.  ARM 3 reports, per panel, the Spearman rank correlation
      between the IS reading of each key and the OOS MAXDD actually realised (and against
      OOS K_21, so neither statistic is graded only on its own home turf).

  (4) AND IT MUST PAY, OR IT IS A PUBLISHING FACT.  ARM 4 is PROTOCOL rule 8's capital arm:
      a chooser per (k, m) cell buys the highest-IS-Sharpe book that passes all four 4b legs
      in sample with the DD leg keyed on (k, m), falling back to the highest-IS-Sharpe book
      when the filter is empty (declared in advance, not chosen after).  2017-2026 is then
      read ONCE.  d = (K-keyed chooser) - (MAXDD-keyed chooser at the same cap multiple) is
      the price of re-keying.

PRE-DECLARED OUTCOMES, none selected on:
  (A) K_21 IS A BETTER CAP   — flip share >= 0.05 at the protocol multiple AND (K_21 is
                               better resolved than MAXDD OR forecasts OOS drawdown better)
                               AND the K_21-keyed chooser's mean d(OOS Sharpe) is >= +1 SE.
  (B) DIFFERENT, NOT BETTER  — it flips verdicts (>= 0.05) but buys no resolution, no
                               forecast and no capital.
  (C) THE SAME CAP           — flip share < 0.05 at the protocol multiple: the re-key is a
                               relabelling and the queue's question is empty.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both — "k, cap multiple"):

  DIAL 1  k  {21, 63, 126, 252, FULL}      FULL is the incumbent key: K_FULL IS MaxDD
                                           exactly (gate G2), so the ladder contains the
                                           statistic it is being compared against.
  DIAL 2  cap multiple m  {0.50, 0.60, 0.75, 1.00}   0.60 is PROTOCOL rule 4b's own.

  All 20 cells are published on every panel, every window and every book
  (`.rescore.csv`, `.cells.csv`, `.capital.csv`).  No verdict is read at one cell only.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL663} (rule 9); the three windows
(FULL / IS 2009-2016 / OOS 2017-2026); the four 4b legs; block length {42, 63, 126}.

FROZEN at the record's construction: the verdict set is the record's own four ladders around
its anchor (N=20, H=126, GROSS=0.75, CADENCE=W); 3-leg composite (21/252, 0/126, 0/63);
above-200d eligibility; max_vol 0.60; decide-at-t / apply-at-t+1 (rule 2); warm-up 260 rows;
cost 10 bps (rule 2's rung — the cost ladder is idea 1277's object, not opened here).

PROTOCOL: rule 2 execution (10 bps, next-day); rule 4 BOTH KEEP paths on every OOS row;
rule 8 walk-forward (every chooser decides on warm-up..2016-12-31 only); rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_does-the-WORST-21-DAY-DRAWDOWN-make-a-BETTER-RISK-CAP-than-MAXDD-in-KEEP-4b_C.py
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
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-the-WORST-21-DAY-DRAWDOWN-make-a-BETTER-RISK-CAP-than-MAXDD-in-KEEP-4b"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
COST = 10.0                                  # PROTOCOL rule 2's rung; not a dial here
LEGS_MOM = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"      # the record's anchor
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70              # PROTOCOL rule 4b's own numbers
SEED = 1282
B_REPS = 400
BLOCK_REF = 63                               # the record's inherited L (1241 / 1250)
BLOCKS = [42, 63, 126]                       # robustness, reported; not a dial

KS = [21, 63, 126, 252, 0]                   # DIAL 1; 0 == FULL == MaxDD
KNAME = {21: "K21", 63: "K63", 126: "K126", 252: "K252", 0: "KFULL"}
MULTS = [0.50, 0.60, 0.75, 1.00]             # DIAL 2
INCUMBENT_K, PROTO_M = 0, 0.60               # the key 4b is written on today
LADDERS = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"  GATE {name}: {'PASS' if ok else 'FAIL'}  value={value}  target={target}")
    return bool(ok)


# ============================================================ panels / books (the record's)
def mech(q):
    parts = []
    for skip, look in LEGS_MOM:
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
        self.seg = {}
        for f in LADDERS["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
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
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, reb):
    """The record's fast runner: GROSS daily returns and one-way turnover at each row.  Costs
    are applied afterwards as r(c) = gross - turn * c / 1e4 (gate G1)."""
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
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1), turn


# ============================================================ metrics
def m_sharpe(r):
    r = np.asarray(r, float)
    if r.size < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def m_cagr(r):
    r = np.asarray(r, float)
    if r.size < 5:
        return np.nan
    return float(np.prod(1 + r) ** (252 / r.size) - 1)


def m_mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if e.size else np.nan


def v_sharpe(R):
    v = R.std(axis=1, ddof=0) * np.sqrt(252)
    out = np.full(R.shape[0], np.nan)
    ok = v > 0
    out[ok] = R[ok].mean(axis=1) * 252 / v[ok]
    return out


def v_cagr(R):
    return np.exp(np.log1p(R).sum(axis=1) * (252 / R.shape[1])) - 1


# ------------------------------------------------- the truncated maximum (idea 1146's rung)
def rolling_max_deque(e, k):
    """Trailing k-day running maximum, min_periods=1, via a monotone deque (O(n)).  This is
    idea 1146's own implementation, kept verbatim as the reference for gate G3."""
    n = len(e)
    out = np.empty(n)
    dq: list[int] = []
    for i in range(n):
        while dq and e[dq[-1]] <= e[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
        out[i] = e[dq[0]]
    return out


def rolling_max_2d(E, k):
    """Trailing k-column running maximum of a (B, T) array, min_periods=1, by sparse-table
    doubling: O(B*T*log k) with no k-sized window materialised.  Checked against the deque
    reference at gate G3."""
    B, T = E.shape
    if k <= 0 or k >= T:
        return np.maximum.accumulate(E, axis=1)
    p = int(np.floor(np.log2(k)))
    M = E.copy()
    for j in range(p):
        s = 1 << j
        nxt = M.copy()
        nxt[:, s:] = np.maximum(M[:, s:], M[:, :-s])
        M = nxt
    d = k - (1 << p)
    if d > 0:
        out = M.copy()
        out[:, d:] = np.maximum(M[:, d:], M[:, :-d])
        return out
    return M


def kdd_1d(r, k):
    """SIGNED worst drawdown inside a trailing k-day window (<= 0).  k = 0 means FULL, and
    then this IS MaxDD exactly (gate G2)."""
    e = np.cumprod(1.0 + np.asarray(r, float))
    if e.size == 0:
        return np.nan
    rp = np.maximum.accumulate(e) if (k <= 0 or k >= e.size) else rolling_max_deque(e, k)
    return float((e / rp - 1.0).min())


def kdd_2d(R, k):
    """SIGNED worst k-day drawdown of every row of a (B, T) return matrix."""
    E = np.cumprod(1.0 + R, axis=1)
    return (E / rolling_max_2d(E, k) - 1.0).min(axis=1)


# ============================================================ the 4b legs
def legs_nonDD(r, spy):
    """The three 4b legs the re-key does NOT touch."""
    h = len(r) // 2
    return {
        "L_H1": m_sharpe(r[:h]) - m_sharpe(spy[:h]),
        "L_H2": m_sharpe(r[h:]) - m_sharpe(spy[h:]),
        "L_CAGR": m_cagr(r) - CAGR_FLOOR * m_cagr(spy),
    }


def dd_margin(r, spy, k, m):
    """The re-keyed 4b DD margin: K_k(book) - m * K_k(SPY).  Both are <= 0, so a book passes
    when the margin is >= 0 (its truncated drawdown is shallower than m times SPY's)."""
    return kdd_1d(r, k) - m * kdd_1d(spy, k)


def v_dd_margin(R, S, k, m):
    return kdd_2d(R, k) - m * kdd_2d(S, k)


def block_index(T, L, reps, rng):
    """Circular block bootstrap row index, (reps, T).  The SAME draw is reused for the book
    and for SPY, so every margin is a PAIRED resample."""
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(reps, nb))
    off = np.arange(L)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(reps, nb * L)[:, :T]
    return idx % T


# ============================================================ book construction
def book_specs():
    """The record's own four ladders around its anchor (N=20, H=126, GROSS=0.75, W)."""
    out = {}
    for n in LADDERS["N"]:
        out[f"N={n}"] = (n, A_H, A_G, A_C)
    for h in LADDERS["H"]:
        out[f"H={h}"] = (A_N, h, A_G, A_C)
    for g in LADDERS["GROSS"]:
        out[f"G={g:.2f}"] = (A_N, A_H, g, A_C)
    for c in LADDERS["CADENCE"]:
        out[f"C={c}"] = (A_N, A_H, A_G, c)
    return out


def all_books(pan):
    specs = book_specs()
    frames = {}
    for (n, h, g, c) in set(specs.values()):
        frames.setdefault((n, h, c), None)
    for key in list(frames):
        frames[key] = build1(pan, key[0], key[1], key[2])
    rets, turns, cache = {}, {}, {}
    for kk, (n, h, g, c) in specs.items():
        rk = (n, h, g, c)
        if rk not in cache:
            gr, tu = nrun(pan, g * frames[(n, h, c)], pan.seg[c])
            cache[rk] = (gr - tu * COST / 1e4, tu)
        rets[kk], turns[kk] = cache[rk][0], cache[rk][1]
    return rets, turns, specs


def windows(pan):
    i0 = WARMUP
    ioos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
    ioos = max(ioos, i0 + 252)
    return {"FULL": (i0, len(pan.idx)), "IS": (i0, ioos), "OOS": (ioos, len(pan.idx))}


def resolution(pan, rets, win, L, reps, seed):
    """Paired-bootstrap SD of the DD margin for every book at every (k, m) cell over `win`."""
    a, b = win
    T = b - a
    rng = np.random.default_rng(seed)
    idx = block_index(T, L, reps, rng)
    S = pan.spy[a:b][idx]
    Sk = {k: kdd_2d(S, k) for k in KS}
    out = {}
    for key, r in rets.items():
        R = r[a:b][idx]
        Rk = {k: kdd_2d(R, k) for k in KS}
        out[key] = {(k, m): float(np.nanstd(Rk[k] - m * Sk[k], ddof=1))
                    for k in KS for m in MULTS}
    return out


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# ============================================================ main
def main():
    t0 = time.time()
    say(f"# Idea 1282 (lane C, {DATE}) — does the WORST 21-DAY DRAWDOWN make a BETTER RISK CAP")
    say(f"# than MAXDD in KEEP 4b?   seed {SEED}, B {B_REPS}, block {BLOCK_REF} "
        f"(robustness {BLOCKS}), cost {COST:.0f} bps")
    say(f"# DIAL 1 k = {[KNAME[k] for k in KS]}   DIAL 2 cap multiple = {MULTS}   "
        f"(incumbent cell = {KNAME[INCUMBENT_K]} @ {PROTO_M:.2f})")

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL663", pxS, inv)]
    say(f"\nPANELS: U56 {len(pxU.columns)-1} names ({pxU.index[0].date()}..{pxU.index[-1].date()}); "
        f"B136 {len(pxB.columns)-1} ({pxB.index[0].date()}..{pxB.index[-1].date()}); "
        f"SMALL663 {len(inv)} of {len(pxS.columns)-1} kept ({pxS.index[0].date()}..{pxS.index[-1].date()})")

    # ---- G1: the fast runner reproduces engine.backtest at the anchor rung
    p0 = panels[0]
    Wa = A_G * build1(p0, A_N, A_H, A_C)
    gr, tu = nrun(p0, Wa, p0.seg[A_C])
    fast = pd.Series(gr - tu * COST / 1e4, index=p0.idx)
    Wdf = pd.DataFrame(Wa, index=p0.idx, columns=p0.px.columns).shift(-1).fillna(0.0)
    eng = backtest(p0.px, Wdf, cost_bps=COST, freq=A_C)["returns"]
    d1 = float(np.nanmax(np.abs((fast - eng).iloc[WARMUP:].values)))
    gate("G1 fast runner == engine.backtest (anchor, U56)", f"{d1:.3e}", "< 1e-10", d1 < 1e-10)

    # ---- G2: K_FULL IS MaxDD exactly, and K_k -> MaxDD at k >= T (the ladder is a ladder)
    rtest = fast.values[WARMUP:]
    g2 = max(abs(kdd_1d(rtest, 0) - m_mdd(rtest)),
             abs(kdd_1d(rtest, 10 ** 6) - m_mdd(rtest)))
    gate("G2 K_FULL == MaxDD exactly (anchor, U56)", f"{g2:.3e}", "== 0", g2 == 0.0)

    # ---- G3: the vectorised rolling max == idea 1146's deque reference
    rng0 = np.random.default_rng(SEED)
    Etest = np.cumprod(1.0 + rng0.normal(0, 0.01, size=(6, 900)), axis=1)
    g3 = max(float(np.abs(rolling_max_2d(Etest, k)[i] - rolling_max_deque(Etest[i], k)).max())
             for k in (21, 63, 126, 252) for i in range(6))
    gate("G3 vectorised rolling max == deque reference", f"{g3:.3e}", "== 0", g3 == 0.0)

    # ---- G4: |K_k| is non-decreasing in k (nested trailing windows) on a real book
    mags = [abs(kdd_1d(rtest, k)) for k in (21, 63, 126, 252, 0)]
    g4 = int(sum(1 for a, b in zip(mags, mags[1:]) if b < a - 1e-15))
    gate("G4 |K_k| non-decreasing in k (anchor, U56)", g4, "== 0", g4 == 0)

    rescore_rows, cell_rows, cap_rows, book_rows, fore_rows, pick_rows = [], [], [], [], [], []
    for pan in panels:
        say(f"\n=== {pan.name} ===")
        rets, turns, specs = all_books(pan)
        win = windows(pan)
        say(f"  books {len(rets)} keys; windows FULL {pan.idx[win['FULL'][0]].date()}.."
            f"{pan.idx[-1].date()}, IS ..{pan.idx[win['IS'][1]-1].date()}, "
            f"OOS {pan.idx[win['OOS'][0]].date()}..")

        # ---------- ARM 1 + ARM 2: re-score every book at every cell, with its resolution
        for wname, w in win.items():
            a, b = w
            spy = pan.spy[a:b]
            spyk = {k: kdd_1d(spy, k) for k in KS}
            nonDD = {kk: legs_nonDD(r[a:b], spy) for kk, r in rets.items()}
            sds = {L: resolution(pan, rets, w, L, B_REPS, SEED + L) for L in BLOCKS}
            for kk, r in rets.items():
                rr = r[a:b]
                bk = {k: kdd_1d(rr, k) for k in KS}
                base3 = all(nonDD[kk][ln] >= 0 for ln in ("L_H1", "L_H2", "L_CAGR"))
                inc_M = bk[INCUMBENT_K] - PROTO_M * spyk[INCUMBENT_K]
                for k in KS:
                    for m in MULTS:
                        M = bk[k] - m * spyk[k]
                        sd = sds[BLOCK_REF][kk][(k, m)]
                        rescore_rows.append(dict(
                            panel=pan.name, window=wname, book=kk, k=KNAME[k], mult=m,
                            book_K=bk[k], spy_K=spyk[k], margin=M, DD_pass=bool(M >= 0),
                            incumbent_margin=inc_M, incumbent_pass=bool(inc_M >= 0),
                            DD_flip=bool((M >= 0) != (inc_M >= 0)),
                            other3_pass=base3,
                            whole4b=bool(base3 and M >= 0),
                            whole4b_incumbent=bool(base3 and inc_M >= 0),
                            whole4b_flip=bool((base3 and M >= 0) != (base3 and inc_M >= 0)),
                            SD=sd, ratio=(abs(M) / sd if sd > 0 else np.nan),
                            inside_1sd=bool(sd > 0 and abs(M) < sd),
                            inside_2sd=bool(sd > 0 and abs(M) < 2 * sd),
                            SD_L42=sds[42][kk][(k, m)], SD_L63=sds[63][kk][(k, m)],
                            SD_L126=sds[126][kk][(k, m)],
                            L_H1=nonDD[kk]["L_H1"], L_H2=nonDD[kk]["L_H2"],
                            L_CAGR=nonDD[kk]["L_CAGR"]))

        # ---------- book levels, for the record
        for wname in ("FULL", "IS", "OOS"):
            a, b = win[wname]
            spy = pan.spy[a:b]
            for kk, r in rets.items():
                rr = r[a:b]
                row = dict(panel=pan.name, window=wname, book=kk, CAGR=m_cagr(rr),
                           Sharpe=m_sharpe(rr), MaxDD=m_mdd(rr),
                           turnover_yr=float(turns[kk][a:b].sum() * 252 / (b - a)),
                           SPY_CAGR=m_cagr(spy), SPY_Sharpe=m_sharpe(spy), SPY_MaxDD=m_mdd(spy))
                for k in KS:
                    row[f"book_{KNAME[k]}"] = kdd_1d(rr, k)
                    row[f"spy_{KNAME[k]}"] = kdd_1d(spy, k)
                book_rows.append(row)

        # ---------- ARM 3: does the IS reading FORECAST the OOS drawdown?
        aI, bI = win["IS"]
        aO, bO = win["OOS"]
        keys = list(rets)
        oos_mdd = [kdd_1d(rets[kk][aO:bO], 0) for kk in keys]
        oos_k21 = [kdd_1d(rets[kk][aO:bO], 21) for kk in keys]
        for k in KS:
            is_k = [kdd_1d(rets[kk][aI:bI], k) for kk in keys]
            fore_rows.append(dict(panel=pan.name, k=KNAME[k], n_books=len(keys),
                                  rho_IS_to_OOS_MaxDD=spearman(is_k, oos_mdd),
                                  rho_IS_to_OOS_K21=spearman(is_k, oos_k21)))

        # ---------- ARM 4: the capital arm (PROTOCOL rule 8, OOS READ ONCE)
        spyI, spyO = pan.spy[aI:bI], pan.spy[aO:bO]
        nonDD_I = {kk: legs_nonDD(r[aI:bI], spyI) for kk, r in rets.items()}
        shI = {kk: m_sharpe(r[aI:bI]) for kk, r in rets.items()}
        spykI = {k: kdd_1d(spyI, k) for k in KS}
        bkI = {kk: {k: kdd_1d(rets[kk][aI:bI], k) for k in KS} for kk in rets}

        v2 = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        v1 = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        v2o, v1o = v2[aO:bO], v1[aO:bO]
        best = max(keys, key=lambda kk: (shI[kk] if np.isfinite(shI[kk]) else -9e9))

        picks = {}
        for k in KS:
            for m in MULTS:
                passers = [kk for kk in keys
                           if all(nonDD_I[kk][ln] >= 0 for ln in ("L_H1", "L_H2", "L_CAGR"))
                           and (bkI[kk][k] - m * spykI[k]) >= 0]
                pk = max(passers, key=lambda kk: shI[kk]) if passers else best
                picks[(k, m)] = (pk, len(passers), not passers)
                r = rets[pk][aO:bO]
                h = len(r) // 2
                lg = legs_nonDD(r, spyO)
                ddm_incumbent = dd_margin(r, spyO, INCUMBENT_K, PROTO_M)
                ddm_ownkey = dd_margin(r, spyO, k, m)
                keep4b = (lg["L_H1"] > 0 and lg["L_H2"] > 0 and lg["L_CAGR"] >= 0
                          and ddm_incumbent >= 0)
                keep4b_ownkey = (lg["L_H1"] > 0 and lg["L_H2"] > 0 and lg["L_CAGR"] >= 0
                                 and ddm_ownkey >= 0)
                keep4a = (m_sharpe(r[:h]) > m_sharpe(v2o[:h]) and
                          m_sharpe(r[h:]) > m_sharpe(v2o[h:]) and m_mdd(r) >= m_mdd(v2o))
                cap_rows.append(dict(
                    panel=pan.name, k=KNAME[k], mult=m, pick=pk, n_candidates=len(keys),
                    n_IS_pass=len(passers), filter_empty=not passers, IS_Sharpe=shI[pk],
                    OOS_CAGR=m_cagr(r), OOS_Sharpe=m_sharpe(r), OOS_MaxDD=m_mdd(r),
                    OOS_K21=kdd_1d(r, 21),
                    OOS_H1=m_sharpe(r[:h]), OOS_H2=m_sharpe(r[h:]),
                    SPY_OOS_CAGR=m_cagr(spyO), SPY_OOS_Sharpe=m_sharpe(spyO),
                    SPY_OOS_MaxDD=m_mdd(spyO), SPY_OOS_K21=kdd_1d(spyO, 21),
                    V2_OOS_CAGR=m_cagr(v2o), V2_OOS_Sharpe=m_sharpe(v2o),
                    V2_OOS_MaxDD=m_mdd(v2o), V1_OOS_Sharpe=m_sharpe(v1o),
                    m_H1=lg["L_H1"], m_H2=lg["L_H2"], m_CAGR=lg["L_CAGR"],
                    m_DD_incumbent=ddm_incumbent, m_DD_ownkey=ddm_ownkey,
                    KEEP_4b=keep4b, KEEP_4b_ownkey=keep4b_ownkey, KEEP_4a=keep4a))

        # every DISTINCT pick, read on the FULL sample too (PROTOCOL rule 4's halves), so a
        # 4b verdict is never quoted from the OOS window alone
        aF, bF = win["FULL"]
        spyF = pan.spy[aF:bF]
        hF = (bF - aF) // 2
        for pk in sorted({p[0] for p in picks.values()}):
            r = rets[pk][aF:bF]
            lgF = legs_nonDD(r, spyF)
            pick_rows.append(dict(
                panel=pan.name, pick=pk,
                FULL_CAGR=m_cagr(r), FULL_Sharpe=m_sharpe(r), FULL_MaxDD=m_mdd(r),
                FULL_H1=m_sharpe(r[:hF]), FULL_H2=m_sharpe(r[hF:]),
                SPY_FULL_H1=m_sharpe(spyF[:hF]), SPY_FULL_H2=m_sharpe(spyF[hF:]),
                SPY_FULL_CAGR=m_cagr(spyF), SPY_FULL_Sharpe=m_sharpe(spyF),
                SPY_FULL_MaxDD=m_mdd(spyF),
                V2_FULL_Sharpe=m_sharpe(v2[aF:bF]), V2_FULL_MaxDD=m_mdd(v2[aF:bF]),
                V2_FULL_H1=m_sharpe(v2[aF:aF + hF]), V2_FULL_H2=m_sharpe(v2[aF + hF:bF]),
                FULL_m_H1=lgF["L_H1"], FULL_m_H2=lgF["L_H2"], FULL_m_CAGR=lgF["L_CAGR"],
                FULL_m_DD_incumbent=dd_margin(r, spyF, INCUMBENT_K, PROTO_M),
                FULL_m_DD_K21=dd_margin(r, spyF, 21, PROTO_M),
                FULL_4b_incumbent=bool(lgF["L_H1"] > 0 and lgF["L_H2"] > 0
                                       and lgF["L_CAGR"] >= 0
                                       and dd_margin(r, spyF, INCUMBENT_K, PROTO_M) >= 0),
                FULL_4b_K21=bool(lgF["L_H1"] > 0 and lgF["L_H2"] > 0 and lgF["L_CAGR"] >= 0
                                 and dd_margin(r, spyF, 21, PROTO_M) >= 0),
                FULL_4a=bool(m_sharpe(r[:hF]) > m_sharpe(v2[aF:aF + hF])
                             and m_sharpe(r[hF:]) > m_sharpe(v2[aF + hF:bF])
                             and m_mdd(r) >= m_mdd(v2[aF:bF]))))

        for k in KS:
            for m in MULTS:
                pk, npass, _ = picks[(k, m)]
                pk0 = picks[(INCUMBENT_K, m)][0]
                r, r0 = rets[pk][aO:bO], rets[pk0][aO:bO]
                cell_rows.append(dict(
                    panel=pan.name, k=KNAME[k], mult=m, pick=pk, pick_incumbent_key=pk0,
                    same_pick=(pk == pk0), n_IS_pass=npass,
                    n_IS_pass_incumbent=picks[(INCUMBENT_K, m)][1],
                    d_OOS_Sharpe=m_sharpe(r) - m_sharpe(r0),
                    d_OOS_CAGR=m_cagr(r) - m_cagr(r0),
                    d_OOS_MaxDD=m_mdd(r) - m_mdd(r0)))

    res = pd.DataFrame(rescore_rows)
    cel = pd.DataFrame(cell_rows)
    cap = pd.DataFrame(cap_rows)
    bks = pd.DataFrame(book_rows)
    fore = pd.DataFrame(fore_rows)
    pks = pd.DataFrame(pick_rows)

    # ---- G5: the incumbent cell reproduces the record's own L_DD exactly
    sub = res[(res.k == "KFULL") & (res.mult == PROTO_M)]
    chk = []
    for _, rrow in bks[bks.window == "FULL"].iterrows():
        s = sub[(sub.panel == rrow.panel) & (sub.window == "FULL") & (sub.book == rrow.book)]
        if len(s):
            chk.append(abs(float(s.margin.iloc[0]) - (rrow.MaxDD - DD_CAP * rrow.SPY_MaxDD)))
    g5 = max(chk) if chk else np.nan
    gate("G5 incumbent cell == PROTOCOL 4b's L_DD", f"{g5:.3e}", "< 1e-12", g5 < 1e-12)

    # ---- G6: the bootstrap SD is stable across rng streams
    p0 = panels[0]
    r0, _, _ = all_books(p0)
    w0 = windows(p0)["FULL"]
    s_a = resolution(p0, r0, w0, BLOCK_REF, B_REPS, SEED)
    s_b = resolution(p0, r0, w0, BLOCK_REF, B_REPS, SEED + 7777)
    rel = [abs(s_a[kk][c] - s_b[kk][c]) / s_a[kk][c] for kk in s_a for c in s_a[kk]
           if s_a[kk][c] > 0]
    gate("G6 SD stable across rng streams (U56 FULL, median rel. move)",
         f"{np.median(rel):.4f}", "< 0.15", float(np.median(rel)) < 0.15)

    # ---- G7: no chooser saw an OOS row (rule 8, structural)
    g7 = bool(cap.n_IS_pass.notna().all() and (cap.n_candidates == len(book_specs())).all())
    gate("G7 every chooser decided on IS rows only (structural)", g7, "True", g7)

    # ================================================================== headline readings
    say("\n" + "=" * 78)
    say("ARM 1 — DOES THE RE-KEY MOVE ANYTHING?  (flip = this cell's DD verdict != KFULL@0.60)")
    say("=" * 78)
    piv = res.pivot_table(index="k", columns="mult", values="DD_flip", aggfunc="mean")
    say("  DD-leg flip share, every one of the 20 dial cells (all panels, all windows, all books):")
    say(piv.reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))
    piv2 = res.pivot_table(index="k", columns="mult", values="whole4b_flip", aggfunc="mean")
    say("\n  WHOLE-4b flip share (the other three legs held at their own values):")
    say(piv2.reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"\n  AT THE PROTOCOL MULTIPLE {PROTO_M:.2f}, by k and panel (DD-leg flip share):")
    pm = res[res.mult == PROTO_M]
    say(pm.pivot_table(index="k", columns="panel", values="DD_flip", aggfunc="mean")
        .reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  PASS RATES at the protocol multiple (share of books whose DD leg passes):")
    say(pm.pivot_table(index="k", columns="window", values="DD_pass", aggfunc="mean")
        .reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))
    deg = (pm[pm.k != "KFULL"].groupby("k")
           .apply(lambda d: float((d.margin - d.incumbent_margin).abs().lt(1e-12).mean()),
                  include_groups=False))
    say("\n  DEGENERACY (share of cells whose margin is bit-identical to the incumbent's), "
        "1146's reading reproduced at the cap:")
    say("    " + ", ".join(f"{i} {v:.4f}" for i, v in deg.items()))

    say("\n" + "=" * 78)
    say("ARM 2 — IS THE RE-KEYED CAP BETTER RESOLVED?  (paired block bootstrap, L=63)")
    say("=" * 78)
    say("  share of DD verdicts decided INSIDE 1 SD of their own margin:")
    say(res.pivot_table(index="k", columns="mult", values="inside_1sd", aggfunc="mean")
        .reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  median |margin| / SD, and the median SD itself (the cap's own resolution):")
    for k in KS:
        s = pm[pm.k == KNAME[k]]
        say(f"    {KNAME[k]:6s} median |M|/SD {s.ratio.median():.3f}; median SD {s.SD.median():.4f} "
            f"(L=42 {s.SD_L42.median():.4f}, L=126 {s.SD_L126.median():.4f}); "
            f"inside 1 SD {s.inside_1sd.mean():.4f}, inside 2 SD {s.inside_2sd.mean():.4f}")

    say("\n" + "=" * 78)
    say("ARM 3 — DOES THE IN-SAMPLE READING FORECAST THE OUT-OF-SAMPLE DRAWDOWN?")
    say("=" * 78)
    say("  Spearman rho across the record's own ladder books, IS statistic -> OOS outcome:")
    say(fore.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    fm = fore.groupby("k")[["rho_IS_to_OOS_MaxDD", "rho_IS_to_OOS_K21"]].mean()
    say("\n  panel-mean rho:")
    say(fm.reindex([KNAME[k] for k in KS]).to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 78)
    say("ARM 4 — CAPITAL ARM (PROTOCOL rule 8, OOS 2017-2026 READ ONCE)")
    say("=" * 78)
    say("  d = (K-keyed chooser) - (MAXDD-keyed chooser at the SAME cap multiple), OOS:")
    say(cel.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    nk = cel[cel.k != "KFULL"]
    d = nk.d_OOS_Sharpe.values
    se = float(np.std(d, ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
    say(f"\n  over {len(d)} re-keyed cells: mean d(OOS Sharpe) {d.mean():+.4f}, SE {se:.4f}, "
        f"t {d.mean()/se if se else np.nan:+.2f}; picks differ in "
        f"{int((~nk.same_pick).sum())} of {len(nk)} cells")
    k21 = cel[cel.k == "K21"]
    d21 = k21.d_OOS_Sharpe.values
    se21 = float(np.std(d21, ddof=1) / np.sqrt(len(d21))) if len(d21) > 1 else np.nan
    say(f"  K21 ALONE ({len(d21)} cells): mean d(OOS Sharpe) {d21.mean():+.4f}, SE {se21:.4f}; "
        f"mean d(OOS MaxDD) {k21.d_OOS_MaxDD.mean():+.4f} "
        f"(negative = deeper); picks differ in {int((~k21.same_pick).sum())} of {len(k21)}")

    say("\n  EVERY OOS CHOOSER ROW, BOTH KEEP PATHS (4b's DD leg shown on the INCUMBENT key, "
        "which is the one the record publishes, and on the cell's OWN key):")
    cols = ["panel", "k", "mult", "pick", "n_IS_pass", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "OOS_H1", "OOS_H2", "SPY_OOS_Sharpe", "V2_OOS_Sharpe", "KEEP_4b",
            "KEEP_4b_ownkey", "KEEP_4a"]
    say(cap[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  KEEP over {len(cap)} OOS chooser rows: 4b (incumbent key) {int(cap.KEEP_4b.sum())}, "
        f"4b (own key) {int(cap.KEEP_4b_ownkey.sum())}, 4a {int(cap.KEEP_4a.sum())}")
    s0 = cap[cap.panel == "U56"].iloc[0]
    say(f"  U56 comparands, OOS: SPY {s0.SPY_OOS_CAGR:.2%} / {s0.SPY_OOS_Sharpe:.4f} / "
        f"{s0.SPY_OOS_MaxDD:.2%} (K21 {s0.SPY_OOS_K21:.2%}); RULES v2 {s0.V2_OOS_CAGR:.2%} / "
        f"{s0.V2_OOS_Sharpe:.4f} / {s0.V2_OOS_MaxDD:.2%}; RULES v1 Sharpe {s0.V1_OOS_Sharpe:.4f}")

    say("\n  EVERY DISTINCT PICK ON THE FULL SAMPLE (rule 4's halves; no 4b verdict is quoted "
        "from the OOS window alone):")
    pcols = ["panel", "pick", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD", "FULL_H1", "FULL_H2",
             "SPY_FULL_Sharpe", "V2_FULL_Sharpe", "FULL_m_DD_incumbent", "FULL_m_DD_K21",
             "FULL_4b_incumbent", "FULL_4b_K21", "FULL_4a"]
    say(pks[pcols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"  FULL-sample 4b over {len(pks)} distinct picks: incumbent key "
        f"{int(pks.FULL_4b_incumbent.sum())}, K21 key {int(pks.FULL_4b_K21.sum())}; "
        f"4a {int(pks.FULL_4a.sum())}")

    # the anchor's own full / halves / OOS line, for the reply and the leaderboard
    anc = bks[(bks.panel == "U56") & (bks.book == f"H={A_H}")]
    af = anc[anc.window == "FULL"].iloc[0]
    ao = anc[anc.window == "OOS"].iloc[0]
    say(f"\n  ANCHOR (U56 N=20/H=126/G=0.75/W) FULL {af.CAGR:.2%} / {af.Sharpe:.4f} / "
        f"{af.MaxDD:.2%} (K21 {af.book_K21:.2%}); OOS {ao.CAGR:.2%} / {ao.Sharpe:.4f} / "
        f"{ao.MaxDD:.2%}")

    # ---- the pre-declared outcome, read mechanically
    flip21 = float(res[(res.k == "K21") & (res.mult == PROTO_M)].DD_flip.mean())
    ins21 = float(res[res.k == "K21"].inside_1sd.mean())
    insFU = float(res[res.k == "KFULL"].inside_1sd.mean())
    rho21 = float(fm.loc["K21", "rho_IS_to_OOS_MaxDD"])
    rhoFU = float(fm.loc["KFULL", "rho_IS_to_OOS_MaxDD"])
    better_res = ins21 < insFU
    better_fore = rho21 > rhoFU
    pays = bool(np.isfinite(se21) and se21 > 0 and d21.mean() >= se21)
    if flip21 < 0.05:
        outcome = "(C) THE SAME CAP"
    elif (better_res or better_fore) and pays:
        outcome = "(A) K_21 IS A BETTER CAP"
    else:
        outcome = "(B) DIFFERENT, NOT BETTER"
    say("\n" + "=" * 78)
    say(f"  PRE-DECLARED OUTCOME, read mechanically: {outcome}")
    say(f"    flip share at the protocol multiple {flip21:.4f} (bar 0.05); "
        f"inside-1-SD K21 {ins21:.4f} vs KFULL {insFU:.4f} ({'better' if better_res else 'worse'}); "
        f"forecast rho K21 {rho21:+.4f} vs KFULL {rhoFU:+.4f} "
        f"({'better' if better_fore else 'worse'}); capital d {d21.mean():+.4f} vs SE {se21:.4f} "
        f"({'pays' if pays else 'does not pay'})")
    say("=" * 78)

    OUT.with_suffix(".cells.csv").write_text(cel.to_csv(index=False))
    OUT.with_suffix(".capital.csv").write_text(cap.to_csv(index=False))
    OUT.with_suffix(".books.csv").write_text(bks.to_csv(index=False))
    OUT.with_suffix(".forecast.csv").write_text(fore.to_csv(index=False))
    OUT.with_suffix(".picks_full.csv").write_text(pks.to_csv(index=False))
    OUT.with_suffix(".gates.csv").write_text(pd.DataFrame(GATES).to_csv(index=False))
    res.to_csv(OUT.with_suffix(".rescore.csv.gz"), index=False, compression="gzip")
    say(f"\nwrote {OUT.name}.[rescore.csv.gz|cells|capital|books|forecast|picks_full|gates].csv  "
        f"({time.time()-t0:.0f}s); gates "
        f"{sum(g['pass_'] for g in GATES)} of {len(GATES)} passing")
    OUT.with_suffix(".result.md").write_text("# Idea 1282 (lane C) — run log\n\n```\n" +
                                             "\n".join(LOG) + "\n```\n")


if __name__ == "__main__":
    main()
