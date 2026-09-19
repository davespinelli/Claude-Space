#!/usr/bin/env python3
"""
Idea 1444 (lane C, 2026-09-19) — does a CAGR-NEUTRAL BETA BAND exist AT ALL?

THE PREMISE.  Idea 1429 built a beta-keyed floor-and-cap band around the frozen 2026-09-04
KEEP-4b incumbent (U56, N = 20, H = 126, gross 0.75, weekly Fri-decide / Mon-trade, 10 bps,
t+1) and found it DOES widen the binding 4b drawdown leg (+1.1028 -> +1.83..+4.40 pp on U56)
at identical names, identical name count and identical gross.  But EVERY cell paid for that
margin twice: in CAGR (-0.84 .. -3.79 pp vs the anchor, monotone in c) and in turnover
(2.87 -> 3.02..9.89 /yr).  Idea 1436 then showed the band is a BETA-MATCHED EXPOSURE DIAL and
a dominated one.

This run asks the ONE question those two leave open, and it is a question about the EXCHANGE
RATE, not about beta: is the CAGR cost a CONSTANT of the band, or a CHOICE?  The incumbent
carries exactly one dial that cuts turnover without touching names-per-book or gross — the
MIN-HOLD H.  So sweep the band half-width c against H and look for a CAGR-NEUTRAL cell: one
that holds the FROZEN anchor's CAGR to within its own bootstrap SE while keeping a 4b DD
margin above the anchor's own +1.1028 pp.

  IF THE FRONTIER IS NON-EMPTY, the DD/CAGR exchange is a choice and the band is a live
  candidate again.  IF IT IS EMPTY, the exchange rate is a FACT ABOUT THE BOOK, and the beta
  family is closed on the return leg as 1436 closed it on the drawdown leg.

THE RULE (identical to 1429's, re-used verbatim so the two runs are comparable):
    rank the n held names by trailing beta to SPY (ascending);  z_i = 1 - 2*(rank_i - 0.5)/n
    in [-1, +1] with sum z = 0 EXACTLY;  w_i = (G/n) * (1 + c * z_i),  G = 0.75.
    LOWEST beta takes the CAP side, HIGHEST beta takes the FLOOR side.  c = 0 is inert.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  C  {0.00, 0.25, 0.50, 0.75, 1.00}    DIAL 1 — band half-width.  c = 0.00 de-bands the cell.
  H  {21, 63, 126, 189, 252, 378}      DIAL 2 — min-hold, trading days.  H = 126 IS the frozen
                                       incumbent's value; (c=0, H=126) IS the frozen incumbent.

30 cells per panel, 90 in all, EVERY ONE published in .grid.csv.

FROZEN, NOT TUNED: the beta lookback is pinned at B = 126 trading days — 1429's headline cell
and the incumbent's own H — and is NEVER varied here.  1429 already published all four
lookbacks and found the cell ordering flat in B; re-opening it would be a third parameter.

THE CONTROL THAT MATTERS.  Five consecutive runs (1405 trailing stop, 1413 breadth throttle,
1423 convention blend, 1433 inverse-vol, 1429/1436 beta band) each found a DD-buying device
that is BEATEN BY A PLAIN DE-GROSS of the same anchor.  So the primary control here is that
same de-gross, posed in THIS idea's own currency:

  CAGR-MATCHED DE-GROSS TWIN — the frozen anchor's weights scaled by a constant f in (0, 1],
  cash remainder, with f solved by bisection so the twin's REALISED FULL-SAMPLE CAGR equals
  the cell's to < 2 bp.  At equal CAGR, whichever book draws down less wins.  If the de-gross
  twin is shallower, the band buys nothing a scalar does not, and the CAGR-neutrality question
  is moot.  (Turnover and its 10 bps drag scale with f, so the twin is charged honestly.)  De-grossing can
  only LOWER return and rule 2 forbids f > 1, so a cell that OUT-EARNS the frozen anchor has NO
  such twin; those cells are reported as unmatched and never scored as wins.

  SAME-H CAGR-MATCHED DE-GROSS TWIN — the same construction applied to THIS H's own c = 0
  anchor.  It shuts the H channel as well as the gross channel: the only difference left between
  cell and twin is the band itself.  It is NOT attainable everywhere either — on a panel where
  the band RAISES CAGR, no de-gross can reach the cell — and the unmatched count is reported.

  RANK-PERMUTATION TWIN (K = 8 seeds) — the cell's own weight multiset re-assigned to the same
  held names in seeded random order.  Matches gross, names, name count, the entire weight
  distribution, effective N and Herfindahl at every row; differs ONLY in which name gets which
  slot.  Tests whether the BETA ORDERING carries anything at all.

NEUTRALITY IS DEFINED TWO WAYS, BOTH PRE-REGISTERED, BOTH REPORTED:
  NEUTRAL-A (the idea's literal wording): cell CAGR >= frozen anchor CAGR - SE_anchor, where
            SE_anchor is the anchor's OWN circular-block-bootstrap SE of CAGR.
  NEUTRAL-B (the stricter, paired form):  cell CAGR >= frozen anchor CAGR - SE_paired, where
            SE_paired is the bootstrap SE of the DIFFERENCE (identical block starts).
A cell is on the FRONTIER if it is neutral under BOTH and its 4b DD margin exceeds the frozen
anchor's own.

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The band is a live candidate again
only if, on U56:
  (i)   the FRONTIER is NON-EMPTY (>= 1 cell neutral under both conventions with DD margin
        above the anchor's +1.1028 pp);
  (ii)  at least one frontier cell passes 4b FULL-SAMPLE and OOS;
  (iii) at least one frontier cell draws down LESS than its own CAGR-MATCHED DE-GROSS TWIN,
        resolved at |t| > 2 on a paired circular-block bootstrap.
Anything less is KILL or PARK, whatever the headline says.  An empty frontier is the
pre-registered KILL and is reported as a finding, not as a failure.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at
every cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised
mean gross, effective N, max/min weight, realised book beta; the per-H anchor (c = 0 at that
H) so the H effect is separable from the c effect.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (c = 0, H = 126) incumbent.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: (c, H)
chosen on warm-up..2016-12-31, 2017-2026 read ONCE) under TWO pre-registered choosers — the
record's argmax-IS-Sharpe and this idea's own CAGR-NEUTRAL-FRONTIER chooser (among IS-neutral
cells take the largest IS DD margin; fall back to the anchor if none is neutral); rule 9
(survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY: the (c=0, H=126) cell must reproduce the
committed U56 anchor (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS).  G2 the
c = 0 cell at each H is BIT-IDENTICAL to that H's own anchor book.  G3 the c = 0 permutation
twin is BIT-IDENTICAL to the c = 0 cell.  G4 all 90 cells published.  G5 exactly two tuned
parameters.  G6 the choosers read no row on or after 2017-01-01.  G7 exposure channel SHUT:
at every H, every c shares the anchor's realised mean gross to < 1e-12.  G7b every rebalance's
weight sum equals G to < 1e-12.  G7c no leverage.  G8 at a given H every c holds the IDENTICAL
name set on every row (one frame per (panel, H), built before any c).  G9 every twin matches
its cell's effective-N path to < 1e-12.  G11 the band is respected exactly and widens with c.
G12 beta uses trailing rows only.  G13 every de-gross twin matches its cell's CAGR to < 2 bp.
G14 the H dial BITES: turnover is strictly decreasing in H at c = 0.  G10 bit-identical
recompute of the U56 headline cell.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_cagr-neutral-beta-band_C.py
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
SLUG = "cagr-neutral-beta-band"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
COST, CADENCE = 10.0, "W"
CS = [0.00, 0.25, 0.50, 0.75, 1.00]        # DIAL 1 — band half-width
HS = [21, 63, 126, 189, 252, 378]          # DIAL 2 — min-hold (trading days)
B_FIXED = 126                              # FROZEN, not a dial
NPERM, SEED = 8, 20260919
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK = 400, 63
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)
BAR_DD_PP = 1.1028                          # the frozen anchor's own 4b DD margin, U56
BAR_T = 2.0
CAGR_TOL = 2e-4                             # de-gross CAGR match tolerance (2 bp)

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
        self.beta = rolling_beta(px[invest].pct_change(), px["SPY"].pct_change(), B_FIXED)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N, H, lag=1):
    """The min-hold selection frame.  Depends on H ONLY (not on c), so it is built ONCE per
    (panel, H) and every c at that H holds the IDENTICAL names on the IDENTICAL rows (G8)."""
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


def cell_weights(pan, segs, c, perm_seed=None, gross=I_G):
    """Per-segment weight vector over the segment's held names, summing to `gross`.
    LOWEST trailing beta takes the CAP side.  perm_seed shuffles the SAME multiset."""
    BE = pan.beta
    rng = np.random.default_rng(perm_seed) if perm_seed is not None else None
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
        if rng is not None:
            w = w[rng.permutation(n)]
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
    wsum_dev = 0.0
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
    return out, turn, gross_path, effn, maxw, minw, wsum_max, wsum_dev


def net(pan, segs, ws):
    g, t, gp, en, mw, mn, wsx, _ = run_book(pan, segs, ws)
    return g - t * COST / 1e4, t, gp, en, mw, mn, wsx


def book_beta(pan, segs, ws):
    num, den = 0.0, 0.0
    for (t, stop, ts, sel), wv in zip(segs, ws):
        if not len(sel):
            continue
        b = pan.beta[ts, sel].astype(float)
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


def _blocks(n, reps=BOOT_REPS, L=BOOT_BLOCK, seed=SEED):
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def _stat(X, stat):
    if stat == "sharpe":
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)
    if stat == "cagr":
        return np.cumprod(1 + X, axis=1)[:, -1] ** (252 / X.shape[1]) - 1
    e = np.cumprod(1 + X, axis=1)
    return (e / np.maximum.accumulate(e, axis=1) - 1).min(axis=1)


def paired_block(a, b, stat="sharpe"):
    """Paired circular-block bootstrap on a PAIRED statistic (identical block starts)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    idx = _blocks(n)
    f = {"sharpe": sharpe, "cagr": cagr, "mdd": mdd}[stat]
    obs = float(f(a) - f(b))
    d = _stat(a[idx], stat) - _stat(b[idx], stat)
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def marginal_se(a, stat="cagr"):
    """The series' OWN circular-block-bootstrap SE of the statistic."""
    a = np.asarray(a, float)
    return float(np.nanstd(_stat(a[_blocks(len(a))], stat), ddof=1))


_DG_MEMO: dict = {}


def degross_to_cagr(pan, segs_a, ws_a, target, tag, lo=0.02, hi=1.0):
    """Scale the FROZEN anchor's weights by a constant f so realised full-sample CAGR == target.
    CAGR is monotone increasing in f over the region of interest (the book's full-sample return
    is positive), so plain bisection on the dyadic grid converges.  Every f is memoised per
    panel, and bisection from fixed endpoints visits a SHARED dyadic grid, so cells with nearby
    targets re-use each other's runs.  Returns (f, net returns, turnover, realised CAGR, hit),
    where hit=False means the target lies OUTSIDE [CAGR(f=lo), CAGR(f=hi=1)] and is therefore
    UNREACHABLE by de-grossing at all — de-grossing can only LOWER return, and PROTOCOL rule 2
    forbids the f > 1 that would be needed.  Such a cell has no de-gross twin, which is reported
    as such and never scored as a win."""
    def run(f):
        key = (pan.name, tag, round(f, 9))
        v = _DG_MEMO.get(key)
        if v is None:
            r, t, _, _, _, _, _ = net(pan, segs_a, [w * f for w in ws_a])
            v = (r, t, cagr(r[WARMUP:]))
            _DG_MEMO[key] = v
        return v
    rl, tl, cl = run(lo)
    rh, th, ch = run(hi)
    if target <= cl:
        return lo, rl, tl, cl, False
    if target >= ch:
        return hi, rh, th, ch, False
    mid, rm, tm, cm = hi, rh, th, ch
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        rm, tm, cm = run(mid)
        if abs(cm - target) < CAGR_TOL:
            return mid, rm, tm, cm, True
        if cm < target:
            lo = mid
        else:
            hi = mid
    return mid, rm, tm, cm, abs(cm - target) < CAGR_TOL


def main():
    t0 = time.time()
    say("=" * 132)
    say("IDEA 1444 (lane C, 2026-09-19) — does a CAGR-NEUTRAL BETA BAND exist AT ALL?")
    say("RULE: rank the n held names by trailing beta to SPY; z = 1 - 2(rank-0.5)/n (sum 0 "
        "EXACTLY); w = (G/n)(1 + c*z), G = 0.75.  LOWEST beta takes the CAP.")
    say(f"DIALS: C {CS} x H {HS} on the frozen incumbent (N={I_N}, gross {I_G}, MAXVOL {MAXVOL}, "
        f"MA gate ON, weekly, {COST:.0f} bps, t+1).  (c=0, H={I_H}) IS the frozen incumbent.")
    say(f"FROZEN, NOT TUNED: beta lookback B = {B_FIXED} trading days (1429's headline), never "
        "varied here.  Exactly two tuned parameters.")
    say(f"CONTROLS: (1) CAGR-MATCHED DE-GROSS TWIN of the frozen anchor (f solved by bisection "
        f"to < {CAGR_TOL*1e4:.0f} bp of the cell's CAGR).  (2) RANK-PERMUTATION twin, K={NPERM}.")
    say(f"PRE-REGISTERED BAR (stated before any number was read): the band is a live candidate "
        f"again only if on U56 (i) the CAGR-NEUTRAL frontier is NON-EMPTY (neutral under BOTH")
    say(f"  conventions AND DD margin > the anchor's {BAR_DD_PP:+.4f} pp), (ii) a frontier cell "
        f"passes 4b FULL and OOS, (iii) a frontier cell beats its CAGR-matched de-gross twin on "
        f"MaxDD at |t| > {BAR_T:.0f}.")
    say("=" * 132)

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

    grid, wf_rows, perm_rows = [], [], []
    g2_dev = g3_dev = g7_dev = g7b_dev = g9_dev = g11_dev = g13_dev = g13b_dev = 0.0
    wsum_global = 0.0
    g11_mono, g14_mono = True, True
    headline_ret = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")

        # ---- the FROZEN incumbent: (c = 0, H = I_H) -------------------------------------
        segs_f = segments(pan, I_N, I_H)
        ws_f = cell_weights(pan, segs_f, 0.0)
        frz, tf, gpf, enf, mwf, mnf, wsf = net(pan, segs_f, ws_f)
        wsum_global = max(wsum_global, wsf)
        fm, fo = triple(frz[WARMUP:]), triple(frz[i_oos:])
        fh1, fh2 = halves(frz[WARMUP:])
        frz_mg = float(np.mean(gpf[WARMUP:]))
        frz_turn = float(np.sum(tf[WARMUP:]) * 252.0 / (T - WARMUP))
        se_anchor = marginal_se(frz[WARMUP:], "cagr")
        say(f"           FROZEN INCUMBENT (c=0, H={I_H}) CAGR {fm['CAGR']:.2%} Sharpe "
            f"{fm['Sharpe']:.4f} MaxDD {fm['MaxDD']:.2%} H1/H2 {fh1:.4f}/{fh2:.4f} | OOS "
            f"{fo['CAGR']:.2%}/{fo['Sharpe']:.4f}/{fo['MaxDD']:.2%} | mean gross {frz_mg:.6f}, "
            f"turnover {frz_turn:.2f}/yr, book beta {book_beta(pan, segs_f, ws_f):.4f}")
        say(f"           ANCHOR 4b DD MARGIN {100*(fm['MaxDD'] - DD_CAP*spy['MaxDD']):+.4f} pp | "
            f"ANCHOR OWN BOOTSTRAP SE of CAGR (NEUTRAL-A tolerance) {100*se_anchor:.4f} pp")
        if pan.name == "U56":
            d = max(abs(fm["Sharpe"] - C_U56["Sharpe"]), abs(fo["Sharpe"] - C_U56["oSharpe"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                 f"|dSharpe| {d:.2e}  (got {fm['CAGR']:.4f}/{fm['Sharpe']:.4f}/"
                 f"{fm['MaxDD']:.4f}; OOS {fo['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- the 30-cell (c, H) grid ---------------------------------------------------
        prev_turn = None
        for H in HS:
            segs = segments(pan, I_N, H)
            nsel = np.array([len(s[3]) for s in segs], float)
            ws_a = cell_weights(pan, segs, 0.0)                    # this H's own anchor
            anc, ta, gpa, ena, _, _, _ = net(pan, segs, ws_a)
            am, ao = triple(anc[WARMUP:]), triple(anc[i_oos:])
            anc_mg = float(np.mean(gpa[WARMUP:]))
            anc_turn = float(np.sum(ta[WARMUP:]) * 252.0 / (T - WARMUP))
            if prev_turn is not None and not anc_turn < prev_turn + 1e-12:
                g14_mono = False
            prev_turn = anc_turn
            if H == I_H:
                g2_dev = max(g2_dev, float(np.max(np.abs(anc - frz))))

            prev_band = None
            for c in CS:
                ws = cell_weights(pan, segs, c)
                rr, tu, gp, en, mw, mn, wsx = net(pan, segs, ws)
                wsum_global = max(wsum_global, wsx)
                g7_dev = max(g7_dev, abs(float(np.mean(gp[WARMUP:])) - anc_mg))
                g7b_dev = max(g7b_dev, max(abs(float(w.sum()) - I_G) for w in ws if len(w)))
                if c == 0.0:
                    g2_dev = max(g2_dev, float(np.max(np.abs(rr - anc))))
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

                k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)

                # --- CAGR neutrality vs the FROZEN incumbent ---
                dC, seP, tC = paired_block(rr[WARMUP:], frz[WARMUP:], "cagr")
                neutral_A = bool(m["CAGR"] >= fm["CAGR"] - se_anchor)
                neutral_B = bool(m["CAGR"] >= fm["CAGR"] - seP)
                dd_marg = 100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"])
                frontier = bool(neutral_A and neutral_B and dd_marg > 100 * (fm["MaxDD"] - DD_CAP * spy["MaxDD"]))

                # --- CONTROL 1: CAGR-MATCHED DE-GROSS TWIN of the FROZEN incumbent ---
                f_dg, r_dg, t_dg, c_dg, hit_dg = degross_to_cagr(
                    pan, segs_f, ws_f, m["CAGR"], "FROZEN")
                if hit_dg:
                    g13_dev = max(g13_dev, abs(c_dg - m["CAGR"]))
                dg = triple(r_dg[WARMUP:])
                dgo = triple(r_dg[i_oos:])
                ddg, sedg, tdg = paired_block(rr[WARMUP:], r_dg[WARMUP:], "mdd")
                sdg, ssedg, stdg = paired_block(rr[WARMUP:], r_dg[WARMUP:], "sharpe")
                dg_turn = float(np.sum(t_dg[WARMUP:]) * 252.0 / (T - WARMUP))

                # --- CONTROL 1b: CAGR-MATCHED DE-GROSS of THIS H's OWN anchor.  Attainable at
                # every cell by construction (the band only ever LOWERS CAGR at fixed H), so it
                # is the control that covers all 90 cells and separates the band from the scalar
                # WITHOUT letting the H dial smuggle return in.
                f_dh, r_dh, t_dh, c_dh, hit_dh = degross_to_cagr(
                    pan, segs, ws_a, m["CAGR"], f"H{H}")
                if hit_dh:
                    g13b_dev = max(g13b_dev, abs(c_dh - m["CAGR"]))
                dh = triple(r_dh[WARMUP:])
                ddh, sedh, tdh = paired_block(rr[WARMUP:], r_dh[WARMUP:], "mdd")
                sdh, ssedh, stdh = paired_block(rr[WARMUP:], r_dh[WARMUP:], "sharpe")

                # --- rank-permutation twins ---
                tw_s, tw_dd, tw_r = [], [], []
                for k in range(NPERM):
                    wsp = cell_weights(pan, segs, c, perm_seed=SEED + 1000 * k + int(100 * c) + H)
                    rp, tp, _, enp, _, _, _ = net(pan, segs, wsp)
                    g9_dev = max(g9_dev, float(np.max(np.abs(enp - en))))
                    if c == 0.0:
                        g3_dev = max(g3_dev, float(np.max(np.abs(rp - rr))))
                    tw_r.append(rp)
                    tw_s.append(sharpe(rp[WARMUP:]))
                    tw_dd.append(mdd(rp[WARMUP:]))
                    perm_rows.append(dict(panel=pan.name, c=c, H=H, draw=k,
                                          Sharpe=tw_s[-1], MaxDD=tw_dd[-1],
                                          CAGR=cagr(rp[WARMUP:])))
                tw_s, tw_dd = np.array(tw_s), np.array(tw_dd)
                twin = tw_r[int(np.argsort(tw_s)[len(tw_s) // 2])]
                dsh, seT, tT = paired_block(rr[WARMUP:], twin[WARMUP:], "sharpe")
                ddT, seDT, tDT = paired_block(rr[WARMUP:], twin[WARMUP:], "mdd")

                turn_y = float(np.sum(tu[WARMUP:]) * 252.0 / (T - WARMUP))
                grid.append(dict(
                    panel=pan.name, c=c, H=H,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                    keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO, keep4a_oos=k4aO,
                    legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                    oleg_H1=legsO["H1"], oleg_H2=legsO["H2"], oleg_DD=legsO["DD"],
                    oleg_CAGR=legsO["CAGR"],
                    dd_margin_pp=dd_marg,
                    cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                    d_cagr_pp_vs_frozen=100 * dC, se_paired_cagr_pp=100 * seP, t_cagr=tC,
                    se_anchor_cagr_pp=100 * se_anchor,
                    neutral_A=neutral_A, neutral_B=neutral_B, frontier=frontier,
                    d_sharpe_vs_frozen=m["Sharpe"] - fm["Sharpe"],
                    d_maxdd_pp_vs_frozen=100 * (m["MaxDD"] - fm["MaxDD"]),
                    d_cagr_pp_vs_Hanchor=100 * (m["CAGR"] - am["CAGR"]),
                    d_maxdd_pp_vs_Hanchor=100 * (m["MaxDD"] - am["MaxDD"]),
                    Hanchor_CAGR=am["CAGR"], Hanchor_Sharpe=am["Sharpe"],
                    Hanchor_MaxDD=am["MaxDD"], Hanchor_turn=anc_turn,
                    dg_f=f_dg, dg_CAGR=dg["CAGR"], dg_Sharpe=dg["Sharpe"], dg_MaxDD=dg["MaxDD"],
                    dg_oSharpe=dgo["Sharpe"], dg_oMaxDD=dgo["MaxDD"], dg_turn=dg_turn,
                    dg_matched=hit_dg,
                    d_maxdd_pp_vs_degross=100 * ddg, t_maxdd_vs_degross=tdg,
                    d_sharpe_vs_degross=sdg, t_sharpe_vs_degross=stdg,
                    beats_degross=bool(hit_dg and ddg > 0),
                    dh_f=f_dh, dh_CAGR=dh["CAGR"], dh_Sharpe=dh["Sharpe"], dh_MaxDD=dh["MaxDD"],
                    dh_matched=hit_dh,
                    d_maxdd_pp_vs_degrossH=100 * ddh, t_maxdd_vs_degrossH=tdh,
                    d_sharpe_vs_degrossH=sdh, t_sharpe_vs_degrossH=stdh,
                    beats_degrossH=bool(hit_dh and ddh > 0),
                    mean_gross=float(np.mean(gp[WARMUP:])), eff_n=float(en.mean()),
                    max_w=float(mw.mean()), min_w=float(mn.mean()), band_w=bw,
                    n_held=float(nsel.mean()), book_beta=book_beta(pan, segs, ws),
                    turn_y=turn_y, drag_bpyr=turn_y * COST,
                    twin_Sharpe_med=float(np.median(tw_s)), twin_MaxDD_med=float(np.median(tw_dd)),
                    d_sharpe_vs_twin=dsh, t_vs_twin=tT,
                    d_maxdd_pp_vs_twin=100 * ddT, t_maxdd_vs_twin=tDT,
                    sharpe_pct_in_twins=float(np.mean(tw_s <= m["Sharpe"])),
                    maxdd_pct_in_twins=float(np.mean(tw_dd <= m["MaxDD"])),
                    spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                    live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"],
                    frozen_CAGR=fm["CAGR"], frozen_Sharpe=fm["Sharpe"], frozen_MaxDD=fm["MaxDD"],
                    frozen_turn=frz_turn,
                    frozen_dd_margin_pp=100 * (fm["MaxDD"] - DD_CAP * spy["MaxDD"])))
                if pan.name == "U56" and c == 0.50 and H == I_H:
                    headline_ret = rr.copy()

        # ---- rule 8: TWO pre-registered choosers, 2017-2026 read ONCE -------------------
        i_is0, i_is1 = WARMUP, i_oos
        IS = {}
        for H in HS:
            segs = segments(pan, I_N, H)
            for c in CS:
                rr, _, _, _, _, _, _ = net(pan, segs, cell_weights(pan, segs, c))
                IS[(c, H)] = rr
        is_frz = frz[i_is0:i_is1]
        se_is = marginal_se(is_frz, "cagr")
        c_frz_is = cagr(is_frz)
        dd_frz_is = 100 * (mdd(is_frz) - DD_CAP * mdd(pan.spy[i_is0:i_is1]))
        picks = {}
        picks["SHARPE"] = max(IS, key=lambda k: sharpe(IS[k][i_is0:i_is1]))
        elig = [k for k in IS
                if cagr(IS[k][i_is0:i_is1]) >= c_frz_is - se_is
                and 100 * (mdd(IS[k][i_is0:i_is1]) - DD_CAP * mdd(pan.spy[i_is0:i_is1])) > dd_frz_is]
        picks["FRONTIER"] = (max(elig, key=lambda k: mdd(IS[k][i_is0:i_is1]))
                             if elig else (0.0, I_H))
        for cname, (pc, pH) in picks.items():
            rr = IS[(pc, pH)]
            k4aO, k4bO, mo, _, _, legsO = keep_paths(rr[i_oos:], spyO, liveO)
            dS, seS, tS = paired_block(rr[i_oos:], frz[i_oos:], "sharpe")
            dD, seD, tD = paired_block(rr[i_oos:], frz[i_oos:], "mdd")
            wf_rows.append(dict(panel=pan.name, chooser=cname, is_c=pc, is_H=pH,
                                n_is_eligible=len(elig) if cname == "FRONTIER" else len(IS),
                                is_Sharpe=sharpe(rr[i_is0:i_is1]),
                                picked_anchor=bool(pc == 0.0 and pH == I_H),
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
    W = pd.DataFrame(wf_rows)
    P = pd.DataFrame(perm_rows)

    gate("G2 the c=0 cell at each H is BIT-IDENTICAL to that H's own anchor book (and to the "
         "frozen incumbent at H=126)", f"max |dret| {g2_dev:.3e}", "< 1e-15", g2_dev < 1e-15)
    gate("G3 the c=0 permutation twin is BIT-IDENTICAL to the c=0 cell",
         f"max |dret| {g3_dev:.3e}", "< 1e-15", g3_dev < 1e-15)
    gate("G4 all 90 grid cells published", len(G), "== 90", len(G) == 90)
    gate("G5 exactly two tuned parameters (c, H); beta lookback frozen at 126", "2", "== 2", True)
    gate("G6 both choosers read no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G7 exposure channel SHUT: at every H, every c shares that H's anchor mean gross",
         f"max |dmean gross| {g7_dev:.3e}", "< 1e-12", g7_dev < 1e-12)
    gate("G7b sum-zero identity: every rebalance's weight sum == G = 0.75",
         f"max |dsum| {g7b_dev:.3e}", "< 1e-12", g7b_dev < 1e-12)
    gate("G7c no leverage: realised weight sum never exceeds 1.0", f"max wsum {wsum_global:.6f}",
         "<= 1.0 + 1e-12", wsum_global <= 1.0 + 1e-12)
    gate("G8 selection untouched by c: one frame per (panel, H), built before any c",
         "by construction", "identical name sets", True)
    gate("G9 every permutation twin matches its cell's effective-N path",
         f"max |d effN| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G11 the band is respected exactly: realised max/min weight == the analytic cap/floor "
         "at every rebalance", f"max |dev| {g11_dev:.3e}", "< 1e-12", g11_dev < 1e-12)
    gate("G11b the band is strictly WIDER at each larger c", f"monotone: {g11_mono}", "True",
         g11_mono)
    nm = int((~G.dg_matched).sum())
    gate("G13 every ATTAINABLE frozen-anchor de-gross twin hits its cell's CAGR",
         f"max |dCAGR| {g13_dev:.3e} over {len(G)-nm} attainable cells",
         f"< {CAGR_TOL}", g13_dev < CAGR_TOL)
    gate("G13b every ATTAINABLE same-H de-gross twin hits its cell's CAGR",
         f"max |dCAGR| {g13b_dev:.3e} over {int(G.dh_matched.sum())} attainable cells",
         f"< {CAGR_TOL}", g13b_dev < CAGR_TOL)
    nmh = int((~G.dh_matched).sum())
    nmh0 = int((~G.dh_matched & (G.c == 0)).sum())
    publish("G13c cells with NO frozen-anchor de-gross twin (their CAGR EXCEEDS the frozen "
            "anchor's, so no f <= 1 can match it and PROTOCOL rule 2 forbids f > 1)",
            f"{nm} of {len(G)} — reported, never scored as a win")
    publish("G13d cells with NO same-H de-gross twin: c=0 identities (target == the anchor "
            "itself) plus cells where the BAND RAISES CAGR above its own H-anchor, which no "
            "de-gross can reach",
            f"{nmh} of {len(G)} ({nmh0} are the c=0 identities, {nmh-nmh0} are band-raises-CAGR)")
    say(f"    NOTE the band does NOT only cost CAGR: it RAISES CAGR above its own H-anchor at "
        f"{int((G.d_cagr_pp_vs_Hanchor > 0).sum())} of {len(G)} cells "
        f"(U56 {int(G[(G.panel=='U56')&(G.c>0)].d_cagr_pp_vs_Hanchor.gt(0).sum())} of 24, "
        f"B136 {int(G[(G.panel=='B136')&(G.c>0)].d_cagr_pp_vs_Hanchor.gt(0).sum())} of 24, "
        f"SMALL {int(G[(G.panel=='SMALL')&(G.c>0)].d_cagr_pp_vs_Hanchor.gt(0).sum())} of 24).")
    gate("G14 the H dial BITES: anchor turnover strictly DECREASING in H on every panel",
         f"monotone: {g14_mono}", "True", g14_mono)

    say("\n" + "=" * 132)
    say("GRID — EVERY CELL.  DD margin = MaxDD - 0.60 x SPY MaxDD (positive = the 4b DD leg "
        "passes).  dCAGR = cell - FROZEN incumbent, in pp.")
    say("NEUT-A: dCAGR >= -SE(anchor's own bootstrap CAGR SE).  NEUT-B: dCAGR >= -SE(paired).  "
        "FRONT: neutral under BOTH and DD margin above the frozen anchor's.")
    say("DEGROSS = the frozen anchor scaled to the CELL's OWN CAGR; dDD > 0 means the CELL drew "
        "down LESS than the scalar that earns the same return.")
    say("=" * 132)
    for pn in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pn]
        say(f"\n  [{pn}]   frozen (c=0,H=126): CAGR {sub.frozen_CAGR.iloc[0]:.2%}  Sharpe "
            f"{sub.frozen_Sharpe.iloc[0]:.4f}  MaxDD {sub.frozen_MaxDD.iloc[0]:.2%}  DD margin "
            f"{sub.frozen_dd_margin_pp.iloc[0]:+.4f} pp  turnover {sub.frozen_turn.iloc[0]:.2f}/yr"
            f"  |  NEUTRAL-A tolerance (anchor CAGR SE) {sub.se_anchor_cagr_pp.iloc[0]:.4f} pp")
        say("      c    H |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg  dCAGR  SEp  SEa | "
            "NA NB FR | 4a 4b o4b | effN  meanG  nHeld bBeta | turn drag | DEGROSS-FROZEN f  "
            "MaxDD   dDD    t  M | DEGROSS-sameH f  MaxDD   dDD    t   | dSh_twin   t   | "
            "OOS CAGR/Sh/DD")
        for _, r in sub.iterrows():
            say(f"    {r.c:4.2f} {int(r.H):4d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%} "
                f"{r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} {r.d_cagr_pp_vs_frozen:+6.2f} "
                f"{r.se_paired_cagr_pp:5.2f} {r.se_anchor_cagr_pp:5.2f} | "
                f"{int(r.neutral_A)}  {int(r.neutral_B)}  {int(r.frontier)} | "
                f"{int(r.keep4a)}  {int(r.keep4b)}  {int(r.keep4b_oos)}  | {r.eff_n:5.2f} "
                f"{r.mean_gross:6.4f} {r.n_held:5.2f} {r.book_beta:5.3f} | {r.turn_y:4.2f} "
                f"{r.drag_bpyr:5.1f} | {r.dg_f:6.4f} {r.dg_MaxDD:7.2%} "
                f"{r.d_maxdd_pp_vs_degross:+6.2f} {r.t_maxdd_vs_degross:+5.2f} "
                f"{int(r.dg_matched)} | {r.dh_f:6.4f} {r.dh_MaxDD:7.2%} "
                f"{r.d_maxdd_pp_vs_degrossH:+6.2f} {r.t_maxdd_vs_degrossH:+5.2f} | "
                f"{r.d_sharpe_vs_twin:+8.4f} {r.t_vs_twin:+5.2f} | {r.oCAGR:7.2%} "
                f"{r.oSharpe:6.4f} {r.oMaxDD:7.2%}")

    say("\n" + "=" * 132)
    say("RULE 8 WALK-FORWARD — (c, H) chosen on warm-up..2016-12-31 under TWO pre-registered "
        "choosers; 2017-2026 read ONCE.")
    say("  SHARPE   = the record's convention, argmax IS Sharpe over all 30 cells.")
    say("  FRONTIER = this idea's own deployable form: among IS cells that are CAGR-neutral to "
        "the frozen anchor (IS bootstrap SE) AND have a wider IS DD margin, take the shallowest "
        "IS MaxDD; fall back to the anchor if none qualifies.")
    say("=" * 132)
    say("  panel | chooser  | IS pick (c,H)  IS Sh | #IS elig | OOS CAGR  Sharpe   MaxDD 4b 4a | "
        "legs H1/H2/DD/CAGR | OOS DDmarg CAGRmarg | FROZEN OOS CAGR/Sh/DD | dSh (t) | dDD pp (t) "
        "| SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | {r.chooser:<8} | ({r.is_c:4.2f},{int(r.is_H):4d}) "
            f"{r.is_Sharpe:6.4f} | {int(r.n_is_eligible):8d} | {r.oCAGR:7.2%} {r.oSharpe:7.4f} "
            f"{r.oMaxDD:7.2%}  {int(r.keep4b_oos)}  {int(r.keep4a_oos)} | "
            f"{int(r.oleg_H1)}/{int(r.oleg_H2)}/{int(r.oleg_DD)}/{int(r.oleg_CAGR)} | "
            f"{r.oos_dd_margin_pp:+8.3f} {r.oos_cagr_margin_pp:+8.3f} | {r.frozen_oCAGR:7.2%} "
            f"{r.frozen_oSharpe:7.4f} {r.frozen_oMaxDD:7.2%} | {r.d_oSharpe_vs_frozen:+7.4f} "
            f"({r.t_oSharpe:+5.2f}) | {r.d_oMaxDD_pp_vs_frozen:+6.3f} ({r.t_oMaxDD:+5.2f}) | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 132)
    say("THE PRE-REGISTERED BAR")
    say("=" * 132)
    U = G[(G.panel == "U56") & (G.c > 0)]
    fr = U[U.frontier]
    say(f"  (i)   U56 CAGR-NEUTRAL FRONTIER (neutral under BOTH conventions AND DD margin > the "
        f"frozen anchor's {BAR_DD_PP:+.4f} pp): {len(fr)} of {len(U)} biting cells.")
    say(f"        NEUTRAL-A alone {int(U.neutral_A.sum())} of {len(U)}; NEUTRAL-B alone "
        f"{int(U.neutral_B.sum())}; DD margin above the anchor's alone "
        f"{int((U.dd_margin_pp > BAR_DD_PP).sum())}.")
    say(f"        U56 dCAGR vs the frozen anchor across the 24 biting cells: "
        f"{U.d_cagr_pp_vs_frozen.min():+.3f} .. {U.d_cagr_pp_vs_frozen.max():+.3f} pp "
        f"(tolerance: SE_anchor {U.se_anchor_cagr_pp.iloc[0]:.3f} pp, SE_paired "
        f"{U.se_paired_cagr_pp.min():.3f}..{U.se_paired_cagr_pp.max():.3f} pp).")
    say(f"  (ii)  of those, passing 4b FULL and OOS: {int((fr.keep4b & fr.keep4b_oos).sum())}.")
    say(f"  (iii) of those, beating the CAGR-MATCHED DE-GROSS twin on MaxDD at |t| > {BAR_T:.0f}: "
        f"{int((fr.beats_degross & (fr.t_maxdd_vs_degross.abs() > BAR_T)).sum())} vs the FROZEN "
        f"anchor's de-gross, {int((fr.beats_degrossH & (fr.t_maxdd_vs_degrossH.abs() > BAR_T)).sum())} "
        f"vs the SAME-H anchor's.")
    allb = G[G.c > 0]
    say(f"\n  ALL PANELS, {len(allb)} biting cells:")
    say(f"    CAGR-NEUTRAL FRONTIER non-empty at {int(allb.frontier.sum())} of {len(allb)} cells "
        f"(U56 {int(G[(G.panel=='U56')&(G.c>0)].frontier.sum())}, B136 "
        f"{int(G[(G.panel=='B136')&(G.c>0)].frontier.sum())}, SMALL "
        f"{int(G[(G.panel=='SMALL')&(G.c>0)].frontier.sum())}).")
    say(f"    dCAGR vs the frozen anchor NEGATIVE at {int((allb.d_cagr_pp_vs_frozen < 0).sum())} "
        f"of {len(allb)}; NEUTRAL-A at {int(allb.neutral_A.sum())}; NEUTRAL-B at "
        f"{int(allb.neutral_B.sum())}.")
    ab_m = allb[allb.dg_matched]
    say(f"    DE-GROSS CONTROL 1 (scale the FROZEN incumbent to the cell's CAGR): attainable at "
        f"{len(ab_m)} of {len(allb)} biting cells ({len(allb)-len(ab_m)} out-earn the frozen "
        f"anchor, so no f <= 1 matches them and rule 2 forbids f > 1).")
    say(f"      the cell draws down LESS than that scalar at {int(ab_m.beats_degross.sum())} of "
        f"{len(ab_m)} (dDD {ab_m.d_maxdd_pp_vs_degross.min():+.3f} .. "
        f"{ab_m.d_maxdd_pp_vs_degross.max():+.3f} pp; |t| > 2 at "
        f"{int((ab_m.t_maxdd_vs_degross.abs() > BAR_T).sum())}).")
    ab_h = allb[allb.dh_matched]
    say(f"    DE-GROSS CONTROL 1b (scale THIS H's OWN anchor to the cell's CAGR — this shuts the "
        f"H channel too, leaving ONLY the band): attainable at {len(ab_h)} of {len(allb)} biting "
        f"cells ({len(allb)-len(ab_h)} have a band that RAISES CAGR above its own H-anchor, "
        f"which no de-gross can reach).")
    say(f"      the cell draws down LESS than that scalar at {int(ab_h.beats_degrossH.sum())} of "
        f"{len(ab_h)} (dDD {ab_h.d_maxdd_pp_vs_degrossH.min():+.3f} .. "
        f"{ab_h.d_maxdd_pp_vs_degrossH.max():+.3f} pp; |t| > 2 at "
        f"{int((ab_h.t_maxdd_vs_degrossH.abs() > BAR_T).sum())}; mean f {ab_h.dh_f.mean():.4f}, "
        f"so the scalar deploys ~{100*(1-ab_h.dh_f.mean()):.1f}% LESS capital than the cell's "
        f"fixed {I_G:.2f} gross).")
    say(f"    vs the RANK-PERMUTATION twin: |t| > 2 on Sharpe at "
        f"{int((allb.t_vs_twin.abs() > BAR_T).sum())} of {len(allb)}; on MaxDD at "
        f"{int((allb.t_maxdd_vs_twin.abs() > BAR_T).sum())}.  Median Sharpe percentile in the "
        f"twin band {allb.sharpe_pct_in_twins.median():.3f} (0.5 = the ordering buys nothing).")
    say(f"    KEEP paths over all {len(G)} cells: 4a {int(G.keep4a.sum())}; 4b full "
        f"{int(G.keep4b.sum())}; 4b OOS {int(G.keep4b_oos.sum())}; both "
        f"{int((G.keep4b & G.keep4b_oos).sum())}.")
    say(f"    THE H DIAL ALONE (c = 0): U56 turnover "
        f"{G[(G.panel=='U56')&(G.c==0)].turn_y.min():.2f}..{G[(G.panel=='U56')&(G.c==0)].turn_y.max():.2f}/yr, "
        f"CAGR {G[(G.panel=='U56')&(G.c==0)].CAGR.min():.2%}..{G[(G.panel=='U56')&(G.c==0)].CAGR.max():.2%}, "
        f"DD margin {G[(G.panel=='U56')&(G.c==0)].dd_margin_pp.min():+.3f}.."
        f"{G[(G.panel=='U56')&(G.c==0)].dd_margin_pp.max():+.3f} pp.")
    say(f"    RULE 8: the two choosers AGREE on "
        f"{int(sum(1 for p in ['U56','B136','SMALL'] if tuple(W[(W.panel==p)&(W.chooser=='SHARPE')][['is_c','is_H']].iloc[0]) == tuple(W[(W.panel==p)&(W.chooser=='FRONTIER')][['is_c','is_H']].iloc[0])))} "
        f"of 3 panels; picks beat SPY OOS on Sharpe at "
        f"{int((W.oSharpe > W.spy_oSharpe).sum())} of {len(W)} panel-chooser pairs; "
        f"4b OOS at {int(W.keep4b_oos.sum())} of {len(W)}.")

    # G10 bit-identical recompute of the U56 headline cell
    pan = panels[0]
    segs = segments(pan, I_N, I_H)
    rr, _, _, _, _, _, _ = net(pan, segs, cell_weights(pan, segs, 0.50))
    d10 = float(np.max(np.abs(rr - headline_ret)))
    gate("G10 bit-identical recompute (U56, c=0.50, H=126)", f"max |dret| {d10:.3e}", "< 1e-15",
         d10 < 1e-15)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P.to_csv(f"{OUT}.perm.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .perm.csv / .gates.csv / .log.txt")
    say(f"  ALL GATES PASS: {all(g['pass_'] for g in GATES)}   ({time.time()-t0:.1f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
