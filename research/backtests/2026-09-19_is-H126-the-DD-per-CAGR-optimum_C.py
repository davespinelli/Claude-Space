#!/usr/bin/env python3
"""
Idea 1461 (lane C, 2026-09-19) — is H = 126 the DD-per-CAGR OPTIMUM, or a GRID ARTEFACT?

THE PREMISE.  Idea 1444 swept the beta band's half-width c against the min-hold H on a SIX-RUNG
ladder {21, 63, 126, 189, 252, 378} and reported an EXCHANGE RATE at each rung — pp of drawdown
bought per pp of CAGR given up, measured against that rung's OWN c = 0 anchor.  Its finding #2
was that the rate PEAKS at H = 126 on U56 (-0.901) AND on B136 (-1.047), and H = 126 is the
frozen 2026-09-04 incumbent's own min-hold.  The rung sits INTERIOR to the ladder, its two
neighbours are 63 and 189 — a factor of 2 and 1.5 away — and the peak was read off a single
point estimate with NO standard error at all.

So the claim "the incumbent already stands on the best rung" rests on a coarse grid and an
unmeasured statistic.  This run refines the ladder AROUND 126 and puts an SE on the peak:

  IF the argmax stays at 126 AND the gap to its nearest rival resolves, the incumbent's H was a
  lucky pick worth documenting, and the exchange rate is a real function of H.
  IF the argmax MOVES to a neighbour, the coarse ladder mislocated it.
  IF the gap DISSOLVES into noise, every 'best rung' claim read off a coarse ladder in this
  record is suspect — including 1444's own.

THE RULE (identical to 1429/1444, re-used verbatim so the three runs are comparable):
    rank the n held names by trailing beta to SPY (ascending);  z_i = 1 - 2*(rank_i - 0.5)/n
    in [-1, +1] with sum z = 0 EXACTLY;  w_i = (G/n) * (1 + c * z_i),  G = 0.75.
    LOWEST beta takes the CAP side, HIGHEST beta takes the FLOOR side.  c = 0 is inert.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):

  H  {100, 112, 126, 142, 160}   DIAL 1 — min-hold, trading days.  The REFINED ladder, with the
                                 incumbent's 126 INTERIOR (two rungs each side, ~+/-12% and
                                 ~+/-27%).  Every capital claim and both rule-8 choosers read
                                 THIS ladder only.
  L  {21, 63, 126}               DIAL 2 — circular-block length for the bootstrap that measures
                                 the peak.  ALL THREE reported; 63 is the record's default and
                                 the primary; the verdict must hold at all three.

FROZEN, NOT TUNED:
  c = 0.50 — the idea's own instruction.  Every CAPITAL claim in this run is read off the
             c = 0.50 book.  The other c values {0.00, 0.25, 0.75, 1.00} are computed ONLY to
             re-form 1444's OLS-over-c slope so its published numbers can be REPLAYED (gate G2)
             and so the same peak question can be asked in 1444's own currency as well as in
             the frozen-c one.  No cell is ever SELECTED on c.
  B = 126 — the beta lookback, 1429's headline and the incumbent's own H.  The B = 252 arm below
            is a PUBLISHED CONTROL, never a selection axis.

THE CONTROL THAT MATTERS HERE.  H = 126 is also the beta lookback B = 126 AND the middle
momentum leg (0, 126) of the live selection composite.  A peak sitting exactly on a number the
book already uses three times over is a coincidence worth testing, so the whole refined ladder
is re-run with the beta lookback decoupled at B = 252.  If the peak tracks H it is a fact about
the MIN-HOLD; if it tracks B, or vanishes, it was a lookback coincidence.  Published at both
values; the verdict is read from the B = 126 arm alone.

THE STATISTIC, DEFINED TWICE, BOTH PRE-REGISTERED:
  SLOPE_OLS (1444's own):  OLS slope of dMaxDD_pp on dCAGR_pp across the four BITING c
                           {0.25, 0.50, 0.75, 1.00}, both differences taken against that H's OWN
                           c = 0 anchor.  This is the statistic whose peak is under test.
  SLOPE_C50 (the idea's):  the single ratio dMaxDD_pp / dCAGR_pp at c = 0.50, same anchor.
  On U56 / B136 both differences have a fixed sign (the band buys drawdown and costs CAGR), so
  the slope is NEGATIVE and MORE NEGATIVE IS BETTER: more drawdown bought per pp of CAGR paid.
  "Peak" therefore means ARGMIN of the slope.

HOW THE PEAK IS MEASURED (the thing 1444 did not do).  A circular-block bootstrap on the
REALISED DAILY NET RETURNS, with ONE block-start matrix per (panel, L) shared by EVERY book in
that panel — so cell, anchor and every rung are resampled on IDENTICAL days and the slope
difference between two rungs is a PAIRED statistic.  Three readings, all published:
  (a) SE and t of each rung's own slope;
  (b) the PAIRED difference slope(126) - slope(rung), its SE, t and sign-fraction;
  (c) P(argmin) — the fraction of replicates in which each rung is the STEEPEST of the five.
      This is the ratio-blowup-immune reading: it needs no denominator to be well behaved, only
      an ordering, and it answers "is 126 the optimum" directly.
A ratio of two small differences is exactly where a point estimate lies, so the count of
replicates with a degenerate denominator is reported rather than silently dropped.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The H = 126 peak is REAL — i.e. the
incumbent's min-hold is a documented optimum rather than a grid artefact — only if, on U56 AND
B136 and at ALL THREE block lengths:
  (i)   argmin SLOPE_OLS over the refined 5-rung ladder is H = 126 (the point estimate);
  (ii)  the PAIRED gap to the best rival rung resolves at |t| > 2;
  (iii) P(argmin = 126) >= 0.50 in the bootstrap.
Failing (i) is "the peak MOVED"; passing (i) and failing (ii)/(iii) is "the peak DISSOLVED".
Either failure is a finding about the record's coarse ladders, reported as one.  This run
proposes NO rules change either way: its capital arm exists to price the refined rungs as real
books, not to replace the incumbent.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell FULL and OOS; the halves; turnover and its 10 bps drag; realised mean gross, effective N,
max/min weight, book beta; the per-H anchor so the H effect is separable from the c effect.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (c = 0, H = 126, B = 126) 2026-09-04 incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: H chosen on
warm-up..2016-12-31 at c = 0.50, 2017-2026 read ONCE) under TWO pre-registered choosers — the
record's argmax-IS-Sharpe and this idea's own STEEPEST-IS-SLOPE; rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed U56 anchor (15.80% / 1.1537 /
-19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 CROSS-SCRIPT REPLAY OF THE STATISTIC UNDER
TEST: re-running 1444's COARSE ladder reproduces its six published U56 slopes and B136's H = 126
slope.  G3 the c = 0 cell at each H is BIT-IDENTICAL to that H's own anchor.  G4 all cells
published.  G5 exactly two tuned dials (H, L); c frozen at 0.50 for every capital claim.  G6 the
choosers read no row on or after 2017-01-01.  G7 exposure channel SHUT (equal mean gross across
c at fixed H).  G7b every rebalance's weight sum == G.  G7c no leverage.  G8 selection depends
on H ONLY: identical name sets across every c and both B at a given (panel, H).  G9 the B = 252
arm's c = 0 book is BIT-IDENTICAL to the B = 126 arm's (beta enters only through the ordering).
G10 bit-identical recompute of the U56 headline cell.  G11 the band is respected exactly and
widens with c.  G12 beta uses trailing rows only.  G14 the H dial BITES: turnover strictly
decreasing in H at c = 0 across the refined ladder.  G15 the refined ladder brackets 126 as an
INTERIOR point.  G16 one block-start matrix per (panel, L), shared by every book (pairing).

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_is-H126-the-DD-per-CAGR-optimum_C.py
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

DATE = "2026-09-19"
SLUG = "is-H126-the-DD-per-CAGR-optimum"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
C_HEAD = 0.50                              # FROZEN by the idea — every capital claim reads this
CS = [0.00, 0.25, 0.50, 0.75, 1.00]        # published; only 0.50 is ever a capital claim
HS_FINE = [100, 112, 126, 142, 160]        # DIAL 1 — the refined ladder
HS_COARSE = [21, 63, 126, 189, 252, 378]   # 1444's ladder, re-run ONLY to replay its slopes (G2)
BS = [126, 252]                            # beta lookback: 126 frozen, 252 a PUBLISHED control
LS = [21, 63, 126]                         # DIAL 2 — bootstrap block length; 63 primary
L_PRIMARY = 63
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, SEED = 400, 20260919
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
# 1444's published COARSE-ladder OLS slopes, for the cross-script replay gate G2
S1444_U56 = {21: -0.462, 63: -0.391, 126: -0.901, 189: -0.755, 252: -0.608, 378: -0.810}
S1444_B136_126 = -1.047
BAR_T = 2.0
BAR_P = 0.50

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


def mech(q):
    """The live selection mechanics (baseline.score with the incumbent's 3-leg composite)."""
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def rolling_beta(R, y, B):
    """Trailing beta of every column of R to the benchmark over B TRAILING rows (gate G12)."""
    ey = y.rolling(B).mean()
    vy = (y * y).rolling(B).mean() - ey * ey
    ex = R.rolling(B).mean()
    exy = R.mul(y, axis=0).rolling(B).mean()
    cov = exy.sub(ex.mul(ey, axis=0))
    return cov.div(vy.replace(0.0, np.nan), axis=0).values


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.beta = {B: rolling_beta(px[invest].pct_change(), px["SPY"].pct_change(), B)
                     for B in BS}
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N, H, lag=1):
    """The min-hold selection frame.  Depends on H ONLY (not on c, not on B), so it is built
    ONCE per (panel, H) and every (c, B) at that H holds the IDENTICAL names on the IDENTICAL
    rows (gate G8)."""
    T = pan.rets.shape[0]
    K = len(pan.iinv)
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    segs = []
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        segs.append((int(t), int(stop), int(ts), sel.copy()))
    return segs


def band_multiset(n, c, gross=I_G):
    """The weight multiset for n names at band half-width c, in CAP-FIRST order."""
    if n == 0:
        return np.zeros(0)
    ranks = np.arange(1, n + 1, dtype=float)
    z = 1.0 - 2.0 * (ranks - 0.5) / n            # sums to EXACTLY 0
    return (gross / n) * (1.0 + c * z)


def cell_weights(pan, segs, c, B=126, gross=I_G):
    """Per-segment weight vector over the segment's held names, summing to `gross`.
    LOWEST trailing beta takes the CAP side."""
    BE = pan.beta[B]
    ws = []
    for (t, stop, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        m = band_multiset(n, c, gross)
        if c == 0.0:
            order = np.arange(n)
        else:
            b = BE[ts, sel].astype(float)
            fin = np.isfinite(b)
            if not fin.all():
                med = np.nanmedian(b[fin]) if fin.any() else 1.0
                b = np.where(fin, b, med)
            order = np.argsort(b, kind="stable")   # ascending beta -> cap first
        w = np.empty(n)
        w[order] = m
        ws.append(w)
    return ws


def run_book(pan, segs, ws):
    """One book.  Weights applied at row i0, drifting inside the segment (engine convention)."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gross_path = np.zeros(T)
    effn = np.zeros(len(segs))
    maxw = np.zeros(len(segs))
    minw = np.zeros(len(segs))
    curw = np.zeros(M)
    wsum_max = 0.0
    for j, ((i0, i1, ts, sel), wv) in enumerate(zip(segs, ws)):
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv
            q = wv / wv.sum()
            effn[j] = 1.0 / float((q ** 2).sum())
            maxw[j] = float(wv.max())
            minw[j] = float(wv.min())
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gross_path[i0:i1] = w0.sum()
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, gross_path, effn, maxw, minw, wsum_max


def net(pan, segs, ws):
    g, t, gp, en, mw, mn, wsx = run_book(pan, segs, ws)
    return g - t * COST / 1e4, t, gp, en, mw, mn, wsx


def book_beta(pan, segs, ws, B=126):
    num, den = 0.0, 0.0
    for (t, stop, ts, sel), wv in zip(segs, ws):
        if not len(sel):
            continue
        b = pan.beta[B][ts, sel].astype(float)
        fin = np.isfinite(b)
        if not fin.any():
            continue
        num += float(np.sum(wv[fin] * b[fin]))
        den += float(np.sum(wv[fin]))
    return num / den if den > 0 else np.nan


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


def block_index(n, L, reps=BOOT_REPS, seed=SEED):
    """ONE circular-block start matrix, shared by every book in a (panel, L) — gate G16."""
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def boot_stats(r, idx):
    """CAGR (fraction) and MaxDD (fraction) of one book over every bootstrap replicate."""
    X = np.asarray(r, float)[idx]
    n = X.shape[1]
    E = np.cumprod(1 + X, axis=1)
    cg = E[:, -1] ** (252.0 / n) - 1.0
    dd = (E / np.maximum.accumulate(E, axis=1) - 1.0).min(axis=1)
    return cg, dd


def paired_block(a, b, idx, stat="sharpe"):
    """Paired circular-block bootstrap on a PAIRED statistic (identical block starts)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    ix = idx[:, :n] % n
    f = {"sharpe": sharpe, "cagr": cagr, "mdd": mdd}[stat]
    obs = float(f(a) - f(b))

    def st(X):
        if stat == "sharpe":
            v = X.std(axis=1, ddof=0) * np.sqrt(252)
            return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)
        if stat == "cagr":
            return np.cumprod(1 + X, axis=1)[:, -1] ** (252 / X.shape[1]) - 1
        E = np.cumprod(1 + X, axis=1)
        return (E / np.maximum.accumulate(E, axis=1) - 1).min(axis=1)
    d = st(a[ix]) - st(b[ix])
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def ols_slope(x, y):
    """OLS slope of y on x (1444's own definition of the exchange rate)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    vx = x.var()
    if not np.isfinite(vx) or vx <= 1e-18:
        return np.nan
    return float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())


def ols_slope_rows(X, Y):
    """Row-wise OLS slopes for a (reps, k) pair of matrices."""
    xm = X.mean(axis=1, keepdims=True)
    ym = Y.mean(axis=1, keepdims=True)
    num = ((X - xm) * (Y - ym)).sum(axis=1)
    den = ((X - xm) ** 2).sum(axis=1)
    return np.where(den > 1e-18, num / np.where(den > 1e-18, den, np.nan), np.nan)


def main():
    t0 = time.time()
    say("=" * 136)
    say("IDEA 1461 (lane C, 2026-09-19) — is H = 126 the DD-per-CAGR OPTIMUM, or a GRID ARTEFACT?")
    say("1444 read a SIX-RUNG ladder {21,63,126,189,252,378} and found the exchange rate peaks at "
        "H = 126 on U56 (-0.901) and B136 (-1.047) — the incumbent's OWN min-hold, INTERIOR to the")
    say("ladder, from a point estimate with NO standard error.  This run refines the ladder AROUND "
        "126 and puts a PAIRED BLOCK BOOTSTRAP on the peak itself.")
    say(f"DIAL 1  H {HS_FINE} (126 interior).   DIAL 2  block length L {LS} (primary {L_PRIMARY}), "
        f"ALL reported.   FROZEN: c = {C_HEAD:.2f} for every capital claim; beta lookback B = 126.")
    say(f"PUBLISHED CONTROL, never selected on: the same refined ladder at B = 252, because H = 126 "
        f"coincides with the beta lookback AND the composite's middle momentum leg.")
    say(f"PRE-REGISTERED BAR (stated before any number was read): the peak is REAL only if on U56 "
        f"AND B136 at ALL THREE L — (i) argmin SLOPE_OLS over the 5 refined rungs is H = 126, "
        f"(ii) the paired gap to the best rival resolves at |t| > {BAR_T:.0f}, "
        f"(iii) P(argmin = 126) >= {BAR_P:.2f}.")
    say("=" * 136)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND and "
        "every 4b pass an optimistic one; what this run reads is a CONTRAST between books built "
        "over the SAME names on the SAME days, which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G12 beta uses trailing rows only (pandas rolling is backward-looking; stamped at the "
         "t-1 decision row)", "by construction", "no look-ahead", True)
    gate("G15 the refined ladder brackets the incumbent's H = 126 as an INTERIOR point",
         f"{HS_FINE}", "two rungs each side of 126",
         HS_FINE.index(I_H) == 2 and len(HS_FINE) == 5)

    grid, slope_rows, boot_rows, wf_rows, pair_rows = [], [], [], [], []
    g3_dev = g7_dev = g7b_dev = g9_dev = g11_dev = 0.0
    wsum_global = 0.0
    g8_ok, g11_mono, g14_mono = True, True, True
    headline_ret = None
    g2_dev = 0.0
    g1_dev = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS CAGR {spyO['CAGR']:.2%} Sharpe {spyO['Sharpe']:.4f} MaxDD "
            f"{spyO['MaxDD']:.2%}  |  4b OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f} | OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        # ---- the FROZEN incumbent: (c = 0, H = 126, B = 126) ----------------------------
        segs_f = segments(pan, I_N, I_H)
        ws_f = cell_weights(pan, segs_f, 0.0, 126)
        frz, tf, gpf, enf, mwf, mnf, wsf = net(pan, segs_f, ws_f)
        wsum_global = max(wsum_global, wsf)
        fm, fo = triple(frz[WARMUP:]), triple(frz[i_oos:])
        fh1, fh2 = halves(frz[WARMUP:])
        frz_turn = float(np.sum(tf[WARMUP:]) * 252.0 / (T - WARMUP))
        say(f"           FROZEN INCUMBENT (c=0, H={I_H}) CAGR {fm['CAGR']:.2%} Sharpe "
            f"{fm['Sharpe']:.4f} MaxDD {fm['MaxDD']:.2%} H1/H2 {fh1:.4f}/{fh2:.4f} | OOS "
            f"{fo['CAGR']:.2%}/{fo['Sharpe']:.4f}/{fo['MaxDD']:.2%} | turnover {frz_turn:.2f}/yr "
            f"| 4b DD margin {100*(fm['MaxDD'] - DD_CAP*spy['MaxDD']):+.4f} pp")
        if pan.name == "U56":
            g1_dev = max(abs(fm["Sharpe"] - C_U56["Sharpe"]), abs(fo["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {g1_dev:.2e}  (got {fm['CAGR']:.4f}/{fm['Sharpe']:.4f}/"
                 f"{fm['MaxDD']:.4f}; OOS {fo['Sharpe']:.4f})", "< 5e-3", g1_dev < 5e-3)

        # ---- every book: H in (refined U coarse) x c x B ---------------------------------
        HS_ALL = sorted(set(HS_FINE) | set(HS_COARSE))
        R = {}          # (B, H, c) -> full net return series
        meta = {}
        names_by_H = {}
        for H in HS_ALL:
            segs = segments(pan, I_N, H)
            names_by_H[H] = [tuple(s[3]) for s in segs]
            nsel = np.array([len(s[3]) for s in segs], float)
            for B in BS:
                if B != 126 and H not in HS_FINE:
                    continue                       # the control arm runs the refined ladder only
                prev_band, anc_mg = None, None
                for c in CS:
                    ws = cell_weights(pan, segs, c, B)
                    rr, tu, gp, en, mw, mn, wsx = net(pan, segs, ws)
                    wsum_global = max(wsum_global, wsx)
                    R[(B, H, c)] = rr
                    if c == 0.0:
                        anc_mg = float(np.mean(gp[WARMUP:]))
                        anc_turn = float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP))
                        anc_full, anc_oos = triple(rr[WARMUP:]), triple(rr[i_oos:])
                    g7_dev = max(g7_dev, abs(float(np.mean(gp[WARMUP:])) - anc_mg))
                    g7b_dev = max(g7b_dev, max((abs(float(w.sum()) - I_G)
                                                for w in ws if len(w)), default=0.0))
                    with np.errstate(divide="ignore", invalid="ignore"):
                        nn = np.maximum(nsel, 1)
                        cap_t = np.where(nsel > 0, (I_G / nn) * (1 + c * (1 - 1 / nn)), 0.0)
                        flo_t = np.where(nsel > 0, (I_G / nn) * (1 - c * (1 - 1 / nn)), 0.0)
                    g11_dev = max(g11_dev, float(np.max(np.abs(mw - cap_t))),
                                  float(np.max(np.abs(mn - flo_t))))
                    bw = float(np.mean(mw - mn))
                    if prev_band is not None and not bw > prev_band - 1e-15:
                        g11_mono = False
                    prev_band = bw
                    if c == 0.0 and B == 126 and H == I_H:
                        g3_dev = max(g3_dev, float(np.max(np.abs(rr - frz))))
                    if c == 0.0 and B != 126:
                        g9_dev = max(g9_dev, float(np.max(np.abs(rr - R[(126, H, 0.0)]))))

                    k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                    k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
                    turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP))
                    grid.append(dict(
                        panel=pan.name, B=B, H=H, c=c,
                        ladder=("fine" if H in HS_FINE else "") + ("+" if H in HS_FINE and H in HS_COARSE else "") + ("coarse" if H in HS_COARSE else ""),
                        headline_c=bool(c == C_HEAD),
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                        oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                        keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                        legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                        oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                        oleg_CAGR=legsO["CAGR"],
                        dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                        cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                        oos_dd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                        oos_cagr_margin_pp=100 * (mo["CAGR"] - CAGR_FLOOR * spyO["CAGR"]),
                        d_cagr_pp_vs_Hanchor=100 * (m["CAGR"] - anc_full["CAGR"]),
                        d_maxdd_pp_vs_Hanchor=100 * (m["MaxDD"] - anc_full["MaxDD"]),
                        d_cagr_pp_vs_frozen=100 * (m["CAGR"] - fm["CAGR"]),
                        d_maxdd_pp_vs_frozen=100 * (m["MaxDD"] - fm["MaxDD"]),
                        d_sharpe_vs_frozen=m["Sharpe"] - fm["Sharpe"],
                        Hanchor_CAGR=anc_full["CAGR"], Hanchor_Sharpe=anc_full["Sharpe"],
                        Hanchor_MaxDD=anc_full["MaxDD"], Hanchor_turn=anc_turn,
                        Hanchor_oCAGR=anc_oos["CAGR"], Hanchor_oSharpe=anc_oos["Sharpe"],
                        Hanchor_oMaxDD=anc_oos["MaxDD"],
                        mean_gross=float(np.mean(gp[WARMUP:])), eff_n=float(en.mean()),
                        max_w=float(mw.mean()), min_w=float(mn.mean()), band_w=bw,
                        n_held=float(nsel.mean()), book_beta=book_beta(pan, segs, ws, B),
                        turn_y=turn_y, drag_bpyr=turn_y * COST,
                        spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                        spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                        spy_oMaxDD=spyO["MaxDD"],
                        live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                        live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"],
                        frozen_CAGR=fm["CAGR"], frozen_Sharpe=fm["Sharpe"],
                        frozen_MaxDD=fm["MaxDD"], frozen_oCAGR=fo["CAGR"],
                        frozen_oSharpe=fo["Sharpe"], frozen_oMaxDD=fo["MaxDD"]))
                    if pan.name == "U56" and B == 126 and H == I_H and c == C_HEAD:
                        headline_ret = rr.copy()

        # G8: at a given H the name sets are one frame, shared by every (c, B) — by construction
        for H in HS_ALL:
            if len(set(len(x) for x in [names_by_H[H]])) != 1:
                g8_ok = False

        # G14: turnover strictly decreasing in H at c = 0 on the refined ladder (B = 126)
        tt = [float(next(g["Hanchor_turn"] for g in grid
                         if g["panel"] == pan.name and g["B"] == 126 and g["H"] == H
                         and g["c"] == 0.0)) for H in HS_FINE]
        if not all(tt[i] > tt[i + 1] for i in range(len(tt) - 1)):
            g14_mono = False

        # ---- POINT SLOPES, both definitions, every ladder and both B arms --------------
        def point_slopes(B, HS):
            out = {}
            for H in HS:
                a = R[(B, H, 0.0)][WARMUP:]
                ca, da = cagr(a), mdd(a)
                x, y = [], []
                for c in CS[1:]:
                    r = R[(B, H, c)][WARMUP:]
                    x.append(100 * (cagr(r) - ca))
                    y.append(100 * (mdd(r) - da))
                r50 = R[(B, H, C_HEAD)][WARMUP:]
                dx50 = 100 * (cagr(r50) - ca)
                dy50 = 100 * (mdd(r50) - da)
                out[H] = dict(slope_ols=ols_slope(x, y),
                              slope_c50=(dy50 / dx50 if abs(dx50) > 1e-12 else np.nan),
                              dcagr_c50_pp=dx50, ddd_c50_pp=dy50,
                              dcagr_pp=list(x), ddd_pp=list(y))
            return out

        coarse = point_slopes(126, HS_COARSE)
        if pan.name == "U56":
            g2_dev = max(g2_dev, max(abs(coarse[H]["slope_ols"] - S1444_U56[H])
                                     for H in HS_COARSE))
        if pan.name == "B136":
            g2_dev = max(g2_dev, abs(coarse[126]["slope_ols"] - S1444_B136_126))

        say(f"\n    [{pan.name}] 1444's COARSE ladder re-formed (B=126): " +
            "  ".join(f"H={H}:{coarse[H]['slope_ols']:+.3f}" for H in HS_COARSE))

        for B in BS:
            fine = point_slopes(B, HS_FINE)
            for H in HS_FINE:
                s = fine[H]
                slope_rows.append(dict(panel=pan.name, B=B, ladder="fine", H=H,
                                       slope_ols=s["slope_ols"], slope_c50=s["slope_c50"],
                                       dcagr_c50_pp=s["dcagr_c50_pp"],
                                       ddd_c50_pp=s["ddd_c50_pp"],
                                       dcagr_pp=";".join(f"{v:.4f}" for v in s["dcagr_pp"]),
                                       ddd_pp=";".join(f"{v:.4f}" for v in s["ddd_pp"])))
            if B == 126:
                for H in HS_COARSE:
                    s = coarse[H]
                    slope_rows.append(dict(panel=pan.name, B=126, ladder="coarse", H=H,
                                           slope_ols=s["slope_ols"], slope_c50=s["slope_c50"],
                                           dcagr_c50_pp=s["dcagr_c50_pp"],
                                           ddd_c50_pp=s["ddd_c50_pp"],
                                           dcagr_pp=";".join(f"{v:.4f}" for v in s["dcagr_pp"]),
                                           ddd_pp=";".join(f"{v:.4f}" for v in s["ddd_pp"])))

        # ---- THE BOOTSTRAP ON THE PEAK ITSELF ------------------------------------------
        n = T - WARMUP
        for L in LS:
            idx = block_index(n, L)
            for B in BS:
                S_ols = np.zeros((BOOT_REPS, len(HS_FINE)))
                S_c50 = np.zeros((BOOT_REPS, len(HS_FINE)))
                degen = np.zeros(len(HS_FINE), dtype=int)
                for j, H in enumerate(HS_FINE):
                    ca, da = boot_stats(R[(B, H, 0.0)][WARMUP:], idx)
                    X = np.zeros((BOOT_REPS, len(CS) - 1))
                    Y = np.zeros((BOOT_REPS, len(CS) - 1))
                    for k, c in enumerate(CS[1:]):
                        cc, dc = boot_stats(R[(B, H, c)][WARMUP:], idx)
                        X[:, k] = 100 * (cc - ca)
                        Y[:, k] = 100 * (dc - da)
                    S_ols[:, j] = ols_slope_rows(X, Y)
                    x50 = X[:, CS[1:].index(C_HEAD)]
                    y50 = Y[:, CS[1:].index(C_HEAD)]
                    bad50 = np.abs(x50) < 1e-6
                    degen[j] = int(bad50.sum())
                    S_c50[:, j] = np.where(bad50, np.nan, y50 / np.where(bad50, np.nan, x50))
                ok = np.isfinite(S_ols).all(axis=1)
                arg = np.full(BOOT_REPS, -1)
                arg[ok] = np.argmin(S_ols[ok], axis=1)
                i126 = HS_FINE.index(I_H)
                for j, H in enumerate(HS_FINE):
                    d = S_ols[:, i126] - S_ols[:, j]
                    dm = np.nanmean(d)
                    ds = np.nanstd(d, ddof=1)
                    boot_rows.append(dict(
                        panel=pan.name, B=B, L=L, H=H,
                        slope_ols=float(np.nanmean(S_ols[:, j])),
                        slope_ols_se=float(np.nanstd(S_ols[:, j], ddof=1)),
                        slope_ols_med=float(np.nanmedian(S_ols[:, j])),
                        slope_c50=float(np.nanmean(S_c50[:, j])),
                        slope_c50_se=float(np.nanstd(S_c50[:, j], ddof=1)),
                        slope_c50_med=float(np.nanmedian(S_c50[:, j])),
                        degenerate_c50=int(degen[j]),
                        p_argmin=float(np.mean(arg == j)),
                        d_vs_126=float(dm), d_vs_126_se=float(ds),
                        t_vs_126=float(dm / ds) if ds > 0 else np.nan,
                        frac_126_steeper=float(np.nanmean(d < 0)),
                        n_ok=int(ok.sum())))
                # pairwise: 126 against its best rival on the POINT estimate
                fine_pt = point_slopes(B, HS_FINE)
                rivals = [H for H in HS_FINE if H != I_H]
                best_rival = min(rivals, key=lambda H: fine_pt[H]["slope_ols"])
                jr = HS_FINE.index(best_rival)
                d = S_ols[:, i126] - S_ols[:, jr]
                dm, ds = np.nanmean(d), np.nanstd(d, ddof=1)
                pair_rows.append(dict(panel=pan.name, B=B, L=L,
                                      point_argmin=int(min(HS_FINE,
                                                           key=lambda H: fine_pt[H]["slope_ols"])),
                                      point_slope_126=fine_pt[I_H]["slope_ols"],
                                      best_rival=int(best_rival),
                                      point_slope_rival=fine_pt[best_rival]["slope_ols"],
                                      point_gap=fine_pt[I_H]["slope_ols"] - fine_pt[best_rival]["slope_ols"],
                                      boot_gap=float(dm), boot_gap_se=float(ds),
                                      t_gap=float(dm / ds) if ds > 0 else np.nan,
                                      p_argmin_126=float(np.mean(arg == i126)),
                                      frac_126_steeper=float(np.nanmean(d < 0))))

        # ---- rule 8: H chosen on warm-up..2016-12-31 at c = 0.50, 2017-2026 read ONCE ----
        i_is0, i_is1 = WARMUP, i_oos
        IS = {H: R[(126, H, C_HEAD)] for H in HS_FINE}

        def is_slope(H):
            a = R[(126, H, 0.0)][i_is0:i_is1]
            r = R[(126, H, C_HEAD)][i_is0:i_is1]
            dx = 100 * (cagr(r) - cagr(a))
            dy = 100 * (mdd(r) - mdd(a))
            return dy / dx if abs(dx) > 1e-12 else np.nan

        picks = {"SHARPE": max(HS_FINE, key=lambda H: sharpe(IS[H][i_is0:i_is1])),
                 "SLOPE": min(HS_FINE, key=lambda H: (is_slope(H) if np.isfinite(is_slope(H))
                                                      else np.inf))}
        bidx = block_index(len(pan.idx) - i_oos, L_PRIMARY)
        for cname, pH in picks.items():
            rr = IS[pH]
            k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
            dS, seS, tS = paired_block(rr[i_oos:], frz[i_oos:], bidx, "sharpe")
            dD, seD, tD = paired_block(rr[i_oos:], frz[i_oos:], bidx, "mdd")
            wf_rows.append(dict(panel=pan.name, chooser=cname, is_H=pH, is_c=C_HEAD,
                                is_Sharpe=sharpe(rr[i_is0:i_is1]), is_slope=is_slope(pH),
                                picked_incumbent_H=bool(pH == I_H),
                                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                keep4b_oos=k4bO, keep4a_oos=k4aO,
                                oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                                oleg_CAGR=legsO["CAGR"],
                                oos_dd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                                oos_cagr_margin_pp=100 * (mo["CAGR"] - CAGR_FLOOR * spyO["CAGR"]),
                                frozen_oCAGR=fo["CAGR"], frozen_oSharpe=fo["Sharpe"],
                                frozen_oMaxDD=fo["MaxDD"],
                                d_oSharpe_vs_frozen=mo["Sharpe"] - fo["Sharpe"], t_oSharpe=tS,
                                d_oMaxDD_pp_vs_frozen=100 * dD, t_oMaxDD=tD,
                                spy_oCAGR=spyO["CAGR"], spy_oSharpe=spyO["Sharpe"],
                                spy_oMaxDD=spyO["MaxDD"],
                                live_oSharpe=liveO["Sharpe"], live_oMaxDD=liveO["MaxDD"]))

    G = pd.DataFrame(grid)
    S = pd.DataFrame(slope_rows)
    Bt = pd.DataFrame(boot_rows)
    Pr = pd.DataFrame(pair_rows)
    W = pd.DataFrame(wf_rows)

    n_exp = 3 * (len(set(HS_FINE) | set(HS_COARSE)) + len(HS_FINE)) * len(CS)
    gate("G2 CROSS-SCRIPT REPLAY OF THE STATISTIC UNDER TEST: 1444's six published U56 "
         "coarse-ladder slopes and B136's H=126 slope", f"max |dslope| {g2_dev:.3e}",
         "< 5e-3", g2_dev < 5e-3)
    gate("G3 the frozen (c=0, H=126, B=126) cell is BIT-IDENTICAL to the anchor book",
         f"max |dret| {g3_dev:.3e}", "< 1e-15", g3_dev < 1e-15)
    gate("G4 all cells published", f"{len(G)} rows", f"== {n_exp}", len(G) == n_exp)
    gate("G5 exactly two tuned dials (H, L); c frozen at 0.50 for every capital claim, B=252 a "
         "published control", "2", "== 2", True)
    gate("G6 both choosers read no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G7 exposure channel SHUT: at every (H, B), every c shares that H's anchor mean gross",
         f"max |dmean gross| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b sum-zero identity: every rebalance's weight sum == G = 0.75",
         f"max |dsum| {g7b_dev:.3e}", "< 1e-12", g7b_dev < 1e-12)
    gate("G7c no leverage: realised weight sum never exceeds 1.0", f"max wsum {wsum_global:.6f}",
         "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G8 selection depends on H ONLY: one name frame per (panel, H), built before any c or B",
         "by construction", "identical name sets", g8_ok)
    gate("G9 the B=252 arm's c=0 book is BIT-IDENTICAL to the B=126 arm's (beta enters ONLY "
         "through the within-book ordering)", f"max |dret| {g9_dev:.3e}", "< 1e-15",
         g9_dev < 1e-15)
    gate("G11 the band is respected exactly: realised max/min weight == the analytic cap/floor "
         "at every rebalance", f"max |dev| {g11_dev:.3e}", "< 1e-12", g11_dev < 1e-12)
    gate("G11b the band is strictly WIDER at each larger c", f"monotone: {g11_mono}", "True",
         g11_mono)
    gate("G14 the H dial BITES: anchor turnover strictly DECREASING across the refined ladder "
         "on every panel", f"monotone: {g14_mono}", "True", g14_mono)
    gate("G16 one block-start matrix per (panel, L), shared by every book (the rung-to-rung "
         "slope gap is PAIRED)", "by construction", "shared index", True)

    say("\n" + "=" * 136)
    say("THE REFINED LADDER — POINT SLOPES.  slope = pp of MaxDD bought per pp of CAGR given up "
        "vs that H's OWN c=0 anchor.  MORE NEGATIVE IS BETTER.")
    say("SLOPE_OLS is 1444's statistic (OLS over the four biting c); SLOPE_C50 is this idea's "
        "frozen-c ratio.  The coarse rungs are 1444's own ladder, replayed.")
    say("=" * 136)
    for pn in ["U56", "B136", "SMALL"]:
        for B in BS:
            sub = S[(S.panel == pn) & (S.B == B) & (S.ladder == "fine")].sort_values("H")
            star = min(sub.H, key=lambda H: float(sub[sub.H == H].slope_ols.iloc[0]))
            say(f"\n  [{pn}] B={B} REFINED   " + "   ".join(
                f"{'*' if int(r.H) == star else ' '}H={int(r.H):3d} OLS {r.slope_ols:+7.3f} "
                f"c50 {r.slope_c50:+7.3f} (dCAGR {r.dcagr_c50_pp:+6.3f} dDD {r.ddd_c50_pp:+6.3f})"
                for _, r in sub.iterrows()))
            if B == 126:
                co = S[(S.panel == pn) & (S.ladder == "coarse")].sort_values("H")
                say(f"  [{pn}] B=126 COARSE (1444's own, replayed)   " + "  ".join(
                    f"H={int(r.H):3d} OLS {r.slope_ols:+7.3f}" for _, r in co.iterrows()))

    say("\n" + "=" * 136)
    say("THE BOOTSTRAP ON THE PEAK.  One block-start matrix per (panel, L), shared by every rung "
        "and every c, so every gap below is PAIRED.")
    say("p_argmin = the fraction of replicates in which THIS rung is the steepest of the five.  "
        "t_vs_126 tests slope(126) - slope(rung) < 0.")
    say("=" * 136)
    for pn in ["U56", "B136", "SMALL"]:
        for B in BS:
            for L in LS:
                sub = Bt[(Bt.panel == pn) & (Bt.B == B) & (Bt.L == L)].sort_values("H")
                say(f"\n  [{pn}] B={B} L={L:3d}  " + "  ".join(
                    f"H={int(r.H):3d}: {r.slope_ols:+6.3f}+/-{r.slope_ols_se:5.3f} "
                    f"P(argmin) {r.p_argmin:.3f} t126 {r.t_vs_126:+6.2f}"
                    for _, r in sub.iterrows()))

    say("\n" + "=" * 136)
    say("126 AGAINST ITS BEST RIVAL RUNG (point estimate picks the rival; the gap is then read "
        "PAIRED in the bootstrap).")
    say("=" * 136)
    say("  panel | B   | L   | point argmin | slope(126) | best rival | slope(rival) | point gap "
        "| boot gap +/- SE | t | P(argmin=126) | frac replicates 126 steeper")
    for _, r in Pr.iterrows():
        say(f"  {r.panel:>5} | {int(r.B):3d} | {int(r.L):3d} | {int(r.point_argmin):12d} | "
            f"{r.point_slope_126:+10.3f} | {int(r.best_rival):10d} | {r.point_slope_rival:+12.3f} "
            f"| {r.point_gap:+9.3f} | {r.boot_gap:+8.3f} +/- {r.boot_gap_se:5.3f} | "
            f"{r.t_gap:+5.2f} | {r.p_argmin_126:13.3f} | {r.frac_126_steeper:.3f}")

    say("\n" + "=" * 136)
    say("CAPITAL — the refined ladder as REAL BOOKS at the frozen c = 0.50, B = 126 "
        "(both KEEP paths, FULL and OOS).")
    say("=" * 136)
    for pn in ["U56", "B136", "SMALL"]:
        sub = G[(G.panel == pn) & (G.B == 126) & (G.c == C_HEAD) & (G.H.isin(HS_FINE))].sort_values("H")
        say(f"\n  [{pn}]  SPY {sub.spy_CAGR.iloc[0]:.2%}/{sub.spy_Sharpe.iloc[0]:.4f}/"
            f"{sub.spy_MaxDD.iloc[0]:.2%}  |  RULES v2 live {sub.live_Sharpe.iloc[0]:.4f}/"
            f"{sub.live_MaxDD.iloc[0]:.2%}  |  FROZEN incumbent {sub.frozen_CAGR.iloc[0]:.2%}/"
            f"{sub.frozen_Sharpe.iloc[0]:.4f}/{sub.frozen_MaxDD.iloc[0]:.2%}")
        say("      H |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b | OOS CAGR "
            "Sharpe   MaxDD | o4a o4b | turn drag | dCAGR dDD vs its own H-anchor")
        for _, r in sub.iterrows():
            say(f"    {int(r.H):3d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} {r.H1:6.3f} "
                f"{r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.cagr_margin_pp:+8.2f} | "
                f"{int(r.keep4a)}  {int(r.keep4b)} | {r.oCAGR:8.2%} {r.oSharpe:6.4f} "
                f"{r.oMaxDD:7.2%} | {int(r.keep4a_oos):3d} {int(r.keep4b_oos):3d} | "
                f"{r.turn_y:4.2f} {r.drag_bpyr:5.1f} | {r.d_cagr_pp_vs_Hanchor:+6.3f} "
                f"{r.d_maxdd_pp_vs_Hanchor:+6.3f}")

    say("\n" + "=" * 136)
    say("RULE 8 WALK-FORWARD — H chosen on warm-up..2016-12-31 at the frozen c = 0.50; "
        "2017-2026 read ONCE.  SHARPE = the record's convention; SLOPE = this idea's own.")
    say("=" * 136)
    say("  panel | chooser | IS H  IS Sh  IS slope | OOS CAGR Sharpe  MaxDD | 4b 4a | legs "
        "H1/H2/DD/CAGR | OOS DDmarg CAGRmarg | FROZEN OOS | dSh (t) | dDD pp (t) | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | {r.chooser:<7} | {int(r.is_H):3d} {r.is_Sharpe:6.4f} "
            f"{r.is_slope:+8.3f} | {r.oCAGR:8.2%} {r.oSharpe:6.4f} {r.oMaxDD:7.2%} | "
            f"{int(r.keep4b_oos)}  {int(r.keep4a_oos)} | {int(r.oleg_H1)}/{int(r.oleg_H2)}/"
            f"{int(r.oleg_DD)}/{int(r.oleg_CAGR)} | {r.oos_dd_margin_pp:+8.3f} "
            f"{r.oos_cagr_margin_pp:+8.3f} | {r.frozen_oCAGR:.2%}/{r.frozen_oSharpe:.4f}/"
            f"{r.frozen_oMaxDD:.2%} | {r.d_oSharpe_vs_frozen:+7.4f} ({r.t_oSharpe:+5.2f}) | "
            f"{r.d_oMaxDD_pp_vs_frozen:+6.3f} ({r.t_oMaxDD:+5.2f}) | {r.spy_oCAGR:.2%}/"
            f"{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:.2%}")

    say("\n" + "=" * 136)
    say("THE PRE-REGISTERED BAR")
    say("=" * 136)
    verdicts = {}
    for pn in ["U56", "B136"]:
        sub = Pr[(Pr.panel == pn) & (Pr.B == 126)]
        i_ok = all(int(r.point_argmin) == I_H for _, r in sub.iterrows())
        ii_ok = all(abs(r.t_gap) > BAR_T for _, r in sub.iterrows())
        iii_ok = all(r.p_argmin_126 >= BAR_P for _, r in sub.iterrows())
        verdicts[pn] = (i_ok, ii_ok, iii_ok)
        say(f"  [{pn}]  (i) argmin == 126 at all three L: {i_ok}  "
            f"(point argmins {sorted(set(int(x) for x in sub.point_argmin))})")
        say(f"        (ii) |t| > {BAR_T:.0f} on the paired gap to the best rival at all three L: "
            f"{ii_ok}  (|t| {sub.t_gap.abs().min():.2f}..{sub.t_gap.abs().max():.2f})")
        say(f"        (iii) P(argmin = 126) >= {BAR_P:.2f} at all three L: {iii_ok}  "
            f"(P {sub.p_argmin_126.min():.3f}..{sub.p_argmin_126.max():.3f})")
    real = all(all(v) for v in verdicts.values())
    say(f"\n  THE PEAK IS REAL (all three legs, both large-cap panels): {real}")
    for pn in ["U56", "B136"]:
        i_ok, ii_ok, iii_ok = verdicts[pn]
        say(f"    {pn}: " + ("the peak MOVED — the coarse ladder MISLOCATED it" if not i_ok
                             else ("the peak DISSOLVED — 126 is the point argmin but the gap does "
                                   "not resolve" if not (ii_ok and iii_ok)
                                   else "the peak SURVIVES refinement and resolves")))
    say(f"\n  CONTROL (never selected on): with the beta lookback decoupled to B = 252, the point "
        f"argmin over the refined ladder is " + ", ".join(
            f"{pn} {int(Pr[(Pr.panel==pn)&(Pr.B==252)].point_argmin.iloc[0])}"
            for pn in ["U56", "B136", "SMALL"]) +
        f" (B = 126 gives " + ", ".join(
            f"{pn} {int(Pr[(Pr.panel==pn)&(Pr.B==126)].point_argmin.iloc[0])}"
            for pn in ["U56", "B136", "SMALL"]) + ").")
    say(f"\n  CAPITAL over all {len(G)} published cells: 4a {int(G.keep4a.sum())}; 4b FULL "
        f"{int(G.keep4b.sum())}; 4b OOS {int(G.keep4b_oos.sum())}; BOTH "
        f"{int((G.keep4b & G.keep4b_oos).sum())}.")
    hh = G[(G.B == 126) & (G.c == C_HEAD) & (G.H.isin(HS_FINE))]
    say(f"  At the frozen c = 0.50 on the refined ladder ({len(hh)} books): 4a "
        f"{int(hh.keep4a.sum())}; 4b FULL {int(hh.keep4b.sum())}; BOTH "
        f"{int((hh.keep4b & hh.keep4b_oos).sum())} (U56 "
        f"{int((hh[hh.panel=='U56'].keep4b & hh[hh.panel=='U56'].keep4b_oos).sum())}, B136 "
        f"{int((hh[hh.panel=='B136'].keep4b & hh[hh.panel=='B136'].keep4b_oos).sum())}, SMALL "
        f"{int((hh[hh.panel=='SMALL'].keep4b & hh[hh.panel=='SMALL'].keep4b_oos).sum())}).")
    say(f"  RULE 8: the two choosers AGREE on "
        f"{int(sum(1 for p in ['U56','B136','SMALL'] if W[(W.panel==p)&(W.chooser=='SHARPE')].is_H.iloc[0] == W[(W.panel==p)&(W.chooser=='SLOPE')].is_H.iloc[0]))}"
        f" of 3 panels; pick == the incumbent's H=126 at {int(W.picked_incumbent_H.sum())} of "
        f"{len(W)}; beats the FROZEN incumbent on OOS Sharpe at "
        f"{int((W.d_oSharpe_vs_frozen > 0).sum())} of {len(W)}; 4b OOS at "
        f"{int(W.keep4b_oos.sum())} of {len(W)}.")

    # G10 bit-identical recompute of the U56 headline cell
    pan = panels[0]
    segs = segments(pan, I_N, I_H)
    rr, _, _, _, _, _, _ = net(pan, segs, cell_weights(pan, segs, C_HEAD, 126))
    d10 = float(np.max(np.abs(rr - headline_ret)))
    gate("G10 bit-identical recompute (U56, c=0.50, H=126, B=126)", f"max |dret| {d10:.3e}",
         "< 1e-15", d10 < 1e-15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    S.to_csv(f"{OUT}.slopes.csv", index=False)
    Bt.to_csv(f"{OUT}.bootstrap.csv", index=False)
    Pr.to_csv(f"{OUT}.peak.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .slopes.csv / .bootstrap.csv / .peak.csv / "
        f".walkforward.csv / .gates.csv / .log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
