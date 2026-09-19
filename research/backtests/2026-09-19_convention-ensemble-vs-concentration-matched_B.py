#!/usr/bin/env python3
"""
Idea 1423 (lane B, 2026-09-19) — does a CONVENTION-ENSEMBLE beat the SINGLE COMMITTED CELL on the
BINDING 4b DD LEG, once it is scored against its OWN CONCENTRATION-MATCHED CONTROL?

THE PREMISE (2026-09-19 CHANGELOG, idea 1409).  The standing 2026-09-04 KEEP-4b incumbent (U56,
N = 20, H = 126, gross 0.75, weekly Fri-decide / Mon-trade, 10 bps, t+1) passes 4b on ONE leg by
ONE margin: MaxDD -19.13% against a -20.23% cap, +1.1028 pp.  Idea 1409 walked the 12-1 leg's
(skip, long) convention and found that margin spans 5.3173 pp across the grid, that (21, 252) is
the ONLY one of ten cells that passes, and that two neighbouring skips BEAT the anchor out of
sample while failing on drawdown.  The committed pass is therefore ONE DRAW from a band.

THE OBVIOUS ANTIDOTE, AND THE OBVIOUS TRAP.  The textbook answer to a convention artefact is to
stop choosing: average the member books over the whole convention grid.  That removes the lookback
choice entirely (ZERO tuned lookback parameters) and it is the band's centre rather than its lucky
tail.  The trap is that a blended book HOLDS MORE NAMES, and a book that shallows drawdown by
holding more names has bought a plain CONCENTRATION dial, not a convention insight -- which is
exactly how idea 1405 (trailing equity stop vs exposure-matched flat cut) and idea 1413 (breadth
throttle vs exposure-matched flat cut) both died.  So the ensemble is scored here against its OWN
CONCENTRATION-MATCHED CONTROL: the frozen anchor convention (skip 21, long 252) re-run at the
ensemble's own realised average name count.  The control is DERIVED from the ensemble, not chosen.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  BLEND {WAVG, VOTE}            DIAL 1.  WAVG = mean of the member weight frames (de-concentrates).
                                         VOTE = hold the top N = 20 names of that blended frame
                                         (concentration-preserving) under the same H = 126 rule.
  SPAN  {SKIP5, LONG2, BOTH10}  DIAL 2.  Which convention axis is averaged over:
                                         SKIP5  = skip {0,5,10,21,42} at long 252   (5 members)
                                         LONG2  = long {189,252} at skip 21         (2 members)
                                         BOTH10 = the full 5 x 2 grid              (10 members)

  6 cells per panel, 18 in all, EVERY ONE published in .grid.csv, each beside its own
  concentration-matched control and the frozen anchor.

WHAT IS AND IS NOT TOUCHED.  Members are the idea-1409 books exactly: the composite's first leg at
(skip, long), the other two legs frozen at (0, 126) and (0, 63), N = 20, H = 126, gross 0.75,
MAXVOL 0.60, the 200d MA gate, the weekly cadence, 10 bps and t+1.  Only the COMBINATION of member
books is new.  Every frame is decided at t-1 and applied at t (the member frames already carry the
lag), so no cell can see its own day.

THE PRE-REGISTERED BAR, STATED HERE BEFORE THE NUMBERS AND NOT MOVED AFTERWARDS.
  The ensemble is worth capital only if BOTH hold on U56:
    (i)  its 4b DD MARGIN exceeds the anchor's own +1.1028 pp, AND
    (ii) its Sharpe edge over its OWN concentration-matched control RESOLVES POSITIVE (t > +2
         under the paired circular-block bootstrap).
  (i) alone is what a plain concentration dial already buys, so (i) alone is a KILL.  If (ii) fails
  at every cell, the answer is NO and this is a KILL (capital), reported as such.

REPORTED DIAGNOSTIC (added after the first pass, bar unchanged): because MaxDD is the
BINDING leg, the ensemble-minus-control DRAWDOWN gap is bootstrapped on the same paired blocks
and published beside the Sharpe gap.  It cannot move the pre-registered verdict, only explain it.

RESOLVABILITY, not just sign.  Every gap -- ensemble vs its control, and ensemble vs the frozen
anchor -- is scored by a PAIRED circular-block bootstrap (400 reps x 63-row blocks, seed 20260919,
identical block starts for both books), full sample and OOS.  |t| > 2 is the record's bar; a gap
inside its own SE is published as UNRESOLVED, not as a finding.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised name count;
name overlap with the anchor book.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, the frozen
(21, 252) incumbent, and each cell's own concentration-matched control.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: (BLEND, SPAN) chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen anchor);
rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY: the (21, 252) anchor must reproduce the
committed U56 numbers (15.80% / 1.1537 / -19.13% full; 17.32% / 1.1857 / -19.13% OOS) to < 5e-3 of
Sharpe.  G2 all 18 cells published.  G3 exactly two tuned parameters.  G4 no leverage: realised
weight sum never exceeds gross.  G5 the chooser reads no row on or after 2017-01-01.  G6 the
ensembles genuinely differ from the anchor book: max |W_ens - W_anchor| published, never asserted,
so a "no effect" reading cannot be a silent no-op.  G7 the concentration match is real: the
control's realised mean name count is published beside the ensemble's and the worst |gap| is
gated.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_convention-ensemble-vs-concentration-matched_B.py
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
SLUG = "convention-ensemble-vs-concentration-matched"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, MAXVOL = 260, 0.60
TAIL_LEGS = [(0, 126), (0, 63)]                 # frozen
I_N, I_H, I_G = 20, 126, 0.75                   # the frozen 2026-09-04 incumbent
A_SKIP, A_LONG = 21, 252                        # ... and its 12-1 leg
SKIPS = [0, 5, 10, 21, 42]
LONGS = [189, 252]
SPANS = {
    "SKIP5":  [(s, 252) for s in SKIPS],
    "LONG2":  [(21, L) for L in LONGS],
    "BOTH10": [(s, L) for L in LONGS for s in SKIPS],
}
BLENDS = ["WAVG", "VOTE"]
COST, CADENCE = 10.0, "W"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
PREREG_DD_BAR = 1.1028                          # the incumbent's own committed DD margin, pp
PREREG_T_BAR = 2.0                              # vs its OWN concentration-matched control
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857)

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


def mech(q, skip, long):
    """The live composite with its FIRST leg at (skip, long); the other two legs are frozen."""
    legs = [(skip, long)] + TAIL_LEGS
    parts = []
    for sk, lk in legs:
        x = (q.shift(sk) / q.shift(lk) - 1.0) if sk else (q / q.shift(lk) - 1.0)
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
        self.idx = px.index
        m = rebalance_mask(px.index, CADENCE).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def build1(pan, rank_key, elig, N, H, lag=1):
    """The incumbent's selector: top-N by rank_key among eligible, minimum holding period H."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
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
            k = rank_key[ts].copy()
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
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def build_vote(pan, Wens, N, H):
    """Hold the top-N names of an already-lagged blended frame, same minimum holding period H.
    Reads Wens only at rebalance rows, where it is already decided from t-1 information."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    V = Wens[:, pan.iinv]
    for i, t in enumerate(reb):
        row = V[t]
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young] & (row[young] > 0)]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = np.where(pr[t] & (row > 0), -row, np.inf)
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


def run(pan, frame, gross):
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    curw = np.zeros(M)
    wmax = 0.0
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * frame[i0]
        wmax = max(wmax, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = pan.Cp[i0]
        A = w0[None, :] * (pan.Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (pan.C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return out, turn, wmax


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


def paired_block_dsharpe(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def sh(X):
        v = X.std(axis=1, ddof=0) * np.sqrt(252)
        return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)

    d = sh(A) - sh(B)
    obs = float(sharpe(a) - sharpe(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def paired_block_dmaxdd(a, b, reps=BOOT_REPS, L=BOOT_BLOCK, seed=BOOT_SEED):
    """Same paired circular-block resample, scored on MAXDD instead of Sharpe.  Added as a
    REPORTED DIAGNOSTIC after the first pass because MaxDD is the incumbent's BINDING leg; the
    pre-registered bar (i)/(ii) above is stated on the DD MARGIN and on the SHARPE t and is NOT
    moved by it.  Positive = the ensemble's drawdown is SHALLOWER than its control's."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n
    A, B = a[idx], b[idx]

    def dd(X):
        E = np.cumprod(1 + X, axis=1)
        return (E / np.maximum.accumulate(E, axis=1) - 1).min(axis=1)

    d = dd(A) - dd(B)
    obs = float(mdd(a) - mdd(b))
    se = float(np.nanstd(d, ddof=1))
    return obs, se, (obs / se if se > 0 else np.nan)


def mean_names(frame, lo):
    f = frame[lo:] > 0
    n = f.sum(axis=1)
    n = n[n > 0]
    return float(n.mean()) if len(n) else 0.0


def main():
    t0 = time.time()
    say("=" * 128)
    say("IDEA 1423 (lane B, 2026-09-19) — does a CONVENTION-ENSEMBLE beat the SINGLE COMMITTED CELL "
        "on the BINDING 4b DD LEG, against its OWN CONCENTRATION-MATCHED CONTROL?")
    say("DIALS: BLEND {WAVG, VOTE} x SPAN {SKIP5, LONG2, BOTH10} at the frozen incumbent "
        "(N=20, H=126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).  18 cells, all "
        "published.")
    say(f"PRE-REGISTERED BAR, stated before the numbers: the ensemble is worth capital only if on "
        f"U56 (i) its 4b DD MARGIN exceeds the anchor's own {PREREG_DD_BAR:.4f} pp AND (ii) its "
        f"Sharpe edge over its OWN concentration-matched control resolves POSITIVE at "
        f"t > +{PREREG_T_BAR:.1f}.  (i) alone is what a plain concentration dial already buys and "
        f"is a KILL.")
    say("=" * 128)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level is an UPPER BOUND and every 4b "
        "pass an optimistic one; what this run reads is the GAP between a blended book and its own "
        "concentration-matched twin, on identical names and identical days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, wf_rows = [], []
    wmax_global, g1_ok, maxframe_dev, worst_match = 0.0, None, 0.0, 0.0

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

        # ---- member books (the idea-1409 cells), built once ------------------------------------
        mem = {}
        for L in LONGS:
            for s in SKIPS:
                sc, above, vol20 = mech(pan.px[pan.invest], s, L)
                rank_key = np.where(np.isfinite(sc), -sc, np.inf)
                elig = above & (vol20 < MAXVOL)
                mem[(s, L)] = build1(pan, rank_key, elig, I_N, I_H)

        af = mem[(A_SKIP, A_LONG)]
        ar, atu, awm = run(pan, af, I_G)
        anchor = ar - atu * COST / 1e4
        wmax_global = max(wmax_global, awm)
        am, ao = triple(anchor[WARMUP:]), triple(anchor[i_oos:])
        ah1, ah2 = halves(anchor[WARMUP:])
        a_names = mean_names(af, WARMUP)
        say(f"           FROZEN INCUMBENT (skip 21, long 252)  CAGR {am['CAGR']:.2%} Sharpe "
            f"{am['Sharpe']:.4f} MaxDD {am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS "
            f"{ao['CAGR']:.2%}/{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%} | mean names {a_names:.2f}")
        if pan.name == "U56":
            d = max(abs(am["Sharpe"] - C_U56["Sharpe"]), abs(ao["Sharpe"] - C_U56["oSharpe"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 17.32%/1.1857/-19.13% OOS)",
                         f"|dSharpe| {d:.2e}  (got {am['CAGR']:.4f}/{am['Sharpe']:.4f}/"
                         f"{am['MaxDD']:.4f}; OOS {ao['Sharpe']:.4f})", "< 5e-3", d < 5e-3)

        # ---- concentration-matched control ladder: the ANCHOR convention at N = 1..80 ----------
        # Controls, not dials: the N used by a cell is DERIVED from that cell's realised name count.
        sc, above, vol20 = mech(pan.px[pan.invest], A_SKIP, A_LONG)
        a_key = np.where(np.isfinite(sc), -sc, np.inf)
        a_elig = above & (vol20 < MAXVOL)
        ctrl_cache: dict[int, tuple] = {}

        def control(n):
            n = int(max(1, min(n, len(pan.iinv))))
            if n not in ctrl_cache:
                f = build1(pan, a_key, a_elig, n, I_H)
                g, tu, wm = run(pan, f, I_G)
                ctrl_cache[n] = (g - tu * COST / 1e4, mean_names(f, WARMUP), wm)
            return ctrl_cache[n]

        cells = {}
        for span, members in SPANS.items():
            Wens = np.mean([mem[k] for k in members], axis=0)
            maxframe_dev = max(maxframe_dev, float(np.nanmax(np.abs(Wens[WARMUP:] - af[WARMUP:]))))
            for blend in BLENDS:
                frame = Wens if blend == "WAVG" else build_vote(pan, Wens, I_N, I_H)
                gg, tu, wm = run(pan, frame, I_G)
                wmax_global = max(wmax_global, wm)
                cells[(blend, span)] = dict(r=gg - tu * COST / 1e4, tu=tu, frame=frame,
                                            names=mean_names(frame, WARMUP), nmem=len(members))

        for (blend, span), c in cells.items():
            rr = c["r"]
            # its OWN concentration-matched control: anchor convention at the nearest N
            cand = sorted({int(np.floor(c["names"])), int(np.ceil(c["names"]))})
            pick = min(cand, key=lambda n: abs(control(n)[1] - c["names"]))
            cr, cn, cwm = control(pick)
            wmax_global = max(wmax_global, cwm)
            worst_match = max(worst_match, abs(cn - c["names"]))

            k4a, k4b, m, h1, h2, legs = keep_paths(rr[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, _ = keep_paths(rr[i_oos:], spyO, liveO)
            cm, cmo = triple(cr[WARMUP:]), triple(cr[i_oos:])
            _, ck4b, _, _, _, _ = keep_paths(cr[WARMUP:], spy, live)

            dctl, sectl, tctl = paired_block_dsharpe(rr[WARMUP:], cr[WARMUP:])
            ddd, sedd, tdd = paired_block_dmaxdd(rr[WARMUP:], cr[WARMUP:])
            dddO, seddO, tddO = paired_block_dmaxdd(rr[i_oos:], cr[i_oos:])
            dctlO, sectlO, tctlO = paired_block_dsharpe(rr[i_oos:], cr[i_oos:])
            danc, seanc, tanc = paired_block_dsharpe(rr[WARMUP:], anchor[WARMUP:])
            dancO, seancO, tancO = paired_block_dsharpe(rr[i_oos:], anchor[i_oos:])

            n = T - WARMUP
            turn_y = float(np.sum(c["tu"][WARMUP:]) * 252.0 / n)
            f, g = c["frame"][WARMUP:], af[WARMUP:]
            both = ((f > 0) & (g > 0)).sum(axis=1)
            held = np.maximum((g > 0).sum(axis=1), 1)
            grid.append(dict(
                panel=pan.name, blend=blend, span=span, n_members=c["nmem"],
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                keep4a=k4a, keep4b=k4b, keep4b_oos=k4bO,
                legH1=legs["H1"], legH2=legs["H2"], legDD=legs["DD"], legCAGR=legs["CAGR"],
                dd_margin_pp=100 * (m["MaxDD"] - DD_CAP * spy["MaxDD"]),
                cagr_margin_pp=100 * (m["CAGR"] - CAGR_FLOOR * spy["CAGR"]),
                odd_margin_pp=100 * (mo["MaxDD"] - DD_CAP * spyO["MaxDD"]),
                anchor_dd_margin_pp=100 * (am["MaxDD"] - DD_CAP * spy["MaxDD"]),
                turn_y=turn_y, drag_bpyr=turn_y * COST,
                mean_names=c["names"], name_overlap=float(np.mean(both / held)),
                ctrl_N=pick, ctrl_names=cn, ctrl_CAGR=cm["CAGR"], ctrl_Sharpe=cm["Sharpe"],
                ctrl_MaxDD=cm["MaxDD"], ctrl_keep4b=ck4b,
                ctrl_dd_margin_pp=100 * (cm["MaxDD"] - DD_CAP * spy["MaxDD"]),
                ctrl_oSharpe=cmo["Sharpe"], ctrl_oMaxDD=cmo["MaxDD"],
                d_sharpe_vs_ctrl=dctl, se_vs_ctrl=sectl, t_vs_ctrl=tctl,
                d_maxdd_vs_ctrl_pp=100 * (m["MaxDD"] - cm["MaxDD"]),
                se_maxdd_vs_ctrl_pp=100 * sedd, t_maxdd_vs_ctrl=tdd,
                ose_maxdd_vs_ctrl_pp=100 * seddO, ot_maxdd_vs_ctrl=tddO,
                od_sharpe_vs_ctrl=dctlO, ot_vs_ctrl=tctlO,
                od_maxdd_vs_ctrl_pp=100 * (mo["MaxDD"] - cmo["MaxDD"]),
                d_sharpe_vs_anchor=danc, se_vs_anchor=seanc, t_vs_anchor=tanc,
                d_maxdd_vs_anchor_pp=100 * (m["MaxDD"] - am["MaxDD"]),
                od_sharpe_vs_anchor=dancO, ot_vs_anchor=tancO,
                anchor_Sharpe=am["Sharpe"], anchor_MaxDD=am["MaxDD"], anchor_names=a_names,
                spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"], spy_MaxDD=spy["MaxDD"],
                live_Sharpe=live["Sharpe"], live_MaxDD=live["MaxDD"]))

        # ---- rule 8 -----------------------------------------------------------------------------
        best, bs = None, -np.inf
        for k, c in cells.items():
            s = sharpe(c["r"][WARMUP:i_oos])
            if s > bs:
                bs, best = s, k
        rr = cells[best]["r"]
        k4aO, k4bO, mo, _, _, _ = keep_paths(rr[i_oos:], spyO, liveO)
        cand = sorted({int(np.floor(cells[best]["names"])), int(np.ceil(cells[best]["names"]))})
        pick = min(cand, key=lambda n: abs(control(n)[1] - cells[best]["names"]))
        cro = triple(control(pick)[0][i_oos:])
        wf_rows.append(dict(panel=pan.name, is_blend=best[0], is_span=best[1], is_Sharpe=bs,
                            oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                            keep4b_oos=k4bO, keep4a_oos=k4aO,
                            anchor_oCAGR=ao["CAGR"], anchor_oSharpe=ao["Sharpe"],
                            anchor_oMaxDD=ao["MaxDD"],
                            d_oSharpe_vs_anchor=mo["Sharpe"] - ao["Sharpe"],
                            d_oMaxDD_vs_anchor_pp=100 * (mo["MaxDD"] - ao["MaxDD"]),
                            ctrl_N=pick, ctrl_oSharpe=cro["Sharpe"], ctrl_oMaxDD=cro["MaxDD"],
                            d_oSharpe_vs_ctrl=mo["Sharpe"] - cro["Sharpe"],
                            d_oMaxDD_vs_ctrl_pp=100 * (mo["MaxDD"] - cro["MaxDD"]),
                            spy_oSharpe=spyO["Sharpe"], spy_oCAGR=spyO["CAGR"],
                            spy_oMaxDD=spyO["MaxDD"], live_oSharpe=liveO["Sharpe"]))

    G = pd.DataFrame(grid)
    W = pd.DataFrame(wf_rows)
    gate("G2 all 18 grid cells published", len(G), "== 18", len(G) == 18)
    gate("G3 exactly two tuned parameters (blend, span)", "2", "== 2", True)
    gate("G4 no leverage: realised weight sum never exceeds gross",
         f"max wsum {wmax_global:.6f}", f"<= {I_G} + 1e-12", wmax_global <= I_G + 1e-12)
    gate("G5 chooser reads no row on or after 2017-01-01", "IS = warm-up..2016-12-31",
         "no OOS leakage", True)
    gate("G6 the ensembles genuinely differ from the anchor book (max |W_ens - W_anchor|, "
         "published not asserted)", f"{maxframe_dev:.4e}", "> 1e-6 (a no-op would read 0)",
         maxframe_dev > 1e-6)
    gate("G7 the concentration match is real (worst |control mean names - ensemble mean names|)",
         f"{worst_match:.3f} names", "<= 1.0", worst_match <= 1.0)

    say("\n" + "=" * 128)
    say("GRID — every cell, beside its OWN concentration-matched control.  DD margin = MaxDD - 0.60 "
        "x SPY MaxDD (positive = the 4b DD leg passes).")
    say("=" * 128)
    for pan in ["U56", "B136", "SMALL"]:
        sub = G[G.panel == pan]
        a = sub.iloc[0]
        say(f"\n  [{pan}]  frozen anchor: Sharpe {a.anchor_Sharpe:.4f}  MaxDD "
            f"{a.anchor_MaxDD:.2%}  DDmarg {a.anchor_dd_margin_pp:+.4f} pp  names "
            f"{a.anchor_names:.1f}")
        say("    blend span   m |    CAGR  Sharpe   MaxDD     H1     H2 | DDmarg CAGRmarg | 4a 4b |"
            " names turn drag ovlp | CONTROL N Sharpe  MaxDD DDmarg 4b | dSh vs ctrl   SE     t   |"
            " dDD pp  SE     t | OOS dSh/t vs ctrl")
        for _, r in sub.iterrows():
            say(f"    {r.blend:>4} {r.span:<6}{int(r.n_members):2d} | {r.CAGR:7.2%} {r.Sharpe:7.4f} "
                f"{r.MaxDD:7.2%} {r.H1:6.3f} {r.H2:6.3f} | {r.dd_margin_pp:+6.2f} "
                f"{r.cagr_margin_pp:+8.2f} | {int(r.keep4a)}  {int(r.keep4b)}  | "
                f"{r.mean_names:5.1f} {r.turn_y:4.2f} {r.drag_bpyr:5.1f} {r.name_overlap:4.2f} | "
                f"{int(r.ctrl_N):9d} {r.ctrl_Sharpe:6.4f} {r.ctrl_MaxDD:6.2%} "
                f"{r.ctrl_dd_margin_pp:+6.2f} {int(r.ctrl_keep4b)}  | {r.d_sharpe_vs_ctrl:+8.4f} "
                f"{r.se_vs_ctrl:7.4f} {r.t_vs_ctrl:+6.2f} | {r.d_maxdd_vs_ctrl_pp:+6.2f} "
                f"{r.se_maxdd_vs_ctrl_pp:5.2f} {r.t_maxdd_vs_ctrl:+5.2f} | "
                f"{r.od_sharpe_vs_ctrl:+7.4f}/{r.ot_vs_ctrl:+5.2f}")

    say("\n" + "=" * 128)
    say("EVERY CELL vs THE FROZEN ANCHOR (the other comparand).")
    say("=" * 128)
    say("    panel blend span   |    Sharpe   MaxDD | dSh vs anchor   SE     t   | dDD pp | "
        "OOS CAGR  Sharpe   MaxDD | oDDmarg | OOS dSh/t vs anchor")
    for _, r in G.iterrows():
        say(f"    {r.panel:>5} {r.blend:>4} {r.span:<6} | {r.Sharpe:8.4f} {r.MaxDD:7.2%} | "
            f"{r.d_sharpe_vs_anchor:+8.4f} {r.se_vs_anchor:7.4f} {r.t_vs_anchor:+6.2f} | "
            f"{r.d_maxdd_vs_anchor_pp:+6.2f} | {r.oCAGR:7.2%} {r.oSharpe:7.4f} {r.oMaxDD:7.2%} | "
            f"{r.odd_margin_pp:+7.2f} | {r.od_sharpe_vs_anchor:+7.4f}/{r.ot_vs_anchor:+5.2f}")

    say("\n" + "=" * 128)
    say("RULE 8 WALK-FORWARD — (BLEND, SPAN) chosen by argmax IS Sharpe on warm-up..2016-12-31; "
        "2017-2026 read ONCE.")
    say("=" * 128)
    say("  panel | IS pick        IS Sh | OOS CAGR  Sharpe   MaxDD 4b | ANCHOR OOS Sharpe MaxDD | "
        "dSh | dDD pp | CTRL N oSharpe | dSh vs ctrl | SPY OOS")
    for _, r in W.iterrows():
        say(f"  {r.panel:>5} | {r.is_blend:>4} {r.is_span:<6} {r.is_Sharpe:6.4f} | {r.oCAGR:7.2%} "
            f"{r.oSharpe:7.4f} {r.oMaxDD:7.2%}  {int(r.keep4b_oos)} | {r.anchor_oSharpe:7.4f} "
            f"{r.anchor_oMaxDD:7.2%} | {r.d_oSharpe_vs_anchor:+7.4f} | "
            f"{r.d_oMaxDD_vs_anchor_pp:+6.2f} | {int(r.ctrl_N):6d} {r.ctrl_oSharpe:7.4f} | "
            f"{r.d_oSharpe_vs_ctrl:+11.4f} | "
            f"{r.spy_oCAGR:6.2%}/{r.spy_oSharpe:.4f}/{r.spy_oMaxDD:7.2%}")

    say("\n" + "=" * 128)
    say("HEADLINE — THE PRE-REGISTERED BAR")
    say("=" * 128)
    u = G[G.panel == "U56"]
    leg_i = u[u.dd_margin_pp > PREREG_DD_BAR]
    leg_ii = u[u.t_vs_ctrl > PREREG_T_BAR]
    both_ok = u[(u.dd_margin_pp > PREREG_DD_BAR) & (u.t_vs_ctrl > PREREG_T_BAR)]
    say(f"  (i)  U56 DD MARGIN > anchor's {PREREG_DD_BAR:.4f} pp: {len(leg_i)} of {len(u)} cells "
        f"(range {u.dd_margin_pp.min():+.4f} .. {u.dd_margin_pp.max():+.4f} pp).")
    say(f"  (ii) U56 Sharpe edge over its OWN concentration-matched control resolves "
        f"t > +{PREREG_T_BAR:.1f}: {len(leg_ii)} of {len(u)} cells (t range "
        f"{u.t_vs_ctrl.min():+.2f} .. {u.t_vs_ctrl.max():+.2f}; median dSharpe "
        f"{u.d_sharpe_vs_ctrl.median():+.4f}, median dMaxDD "
        f"{u.d_maxdd_vs_ctrl_pp.median():+.2f} pp).")
    say(f"  BOTH legs: {len(both_ok)} of {len(u)} U56 cells  ->  "
        f"{'BAR MET — the ensemble is a real convention gain' if len(both_ok) else 'BAR NOT MET — ANSWERED NO'}.")
    say(f"  4a: {int(G.keep4a.sum())} of {len(G)}.")
    for pan in ["U56", "B136", "SMALL"]:
        sp = G[G.panel == pan]
        say(f"  4b {pan}: {int(sp.keep4b.sum())} of {len(sp)} cells (controls "
            f"{int(sp.ctrl_keep4b.sum())} of {len(sp)}); DD-leg passes {int(sp.legDD.sum())}, "
            f"CAGR-leg {int(sp.legCAGR.sum())}, H1 {int(sp.legH1.sum())}, H2 "
            f"{int(sp.legH2.sum())}; DD margin range {sp.dd_margin_pp.min():+.2f} .. "
            f"{sp.dd_margin_pp.max():+.2f} pp.")
    res = G[np.abs(G.t_vs_ctrl) > 2]
    say(f"  RESOLVABILITY vs the CONCENTRATION-MATCHED CONTROL (all {len(G)} cells, full sample): "
        f"{len(res)} resolve |t| > 2, {int((res.d_sharpe_vs_ctrl > 0).sum())} of them FAVOUR the "
        f"ensemble.  Median |t| {np.abs(G.t_vs_ctrl).median():.2f}, median dSharpe "
        f"{G.d_sharpe_vs_ctrl.median():+.4f}, median dMaxDD {G.d_maxdd_vs_ctrl_pp.median():+.2f} "
        f"pp.")
    ddres = G[np.abs(G.t_maxdd_vs_ctrl) > 2]
    say(f"  THE BINDING LEG, PRICED (reported diagnostic, added after the first pass; the "
        f"pre-registered bar is unchanged): the ensemble's MAXDD gap over its own "
        f"concentration-matched control resolves |t| > 2 at {len(ddres)} of {len(G)} cells, "
        f"{int((ddres.d_maxdd_vs_ctrl_pp > 0).sum())} of them SHALLOWER.  Median gap "
        f"{G.d_maxdd_vs_ctrl_pp.median():+.2f} pp, median |t| "
        f"{np.abs(G.t_maxdd_vs_ctrl).median():.2f}; U56 median {u.d_maxdd_vs_ctrl_pp.median():+.2f} "
        f"pp at |t| {np.abs(u.t_maxdd_vs_ctrl).median():.2f}.")
    resO = G[np.abs(G.ot_vs_ctrl) > 2]
    say(f"  ... OOS: {len(resO)} resolve, {int((resO.od_sharpe_vs_ctrl > 0).sum())} favour the "
        f"ensemble; median OOS dSharpe {G.od_sharpe_vs_ctrl.median():+.4f}, median OOS dMaxDD "
        f"{G.od_maxdd_vs_ctrl_pp.median():+.2f} pp.")
    resA = G[np.abs(G.t_vs_anchor) > 2]
    say(f"  RESOLVABILITY vs the FROZEN ANCHOR: {len(resA)} of {len(G)} resolve |t| > 2, "
        f"{int((resA.d_sharpe_vs_anchor > 0).sum())} of them BEAT it; median dSharpe "
        f"{G.d_sharpe_vs_anchor.median():+.4f}, median dMaxDD "
        f"{G.d_maxdd_vs_anchor_pp.median():+.2f} pp.")
    say(f"  RULE 8: mean OOS Sharpe of the IS-chosen (blend, span) minus the frozen anchor "
        f"{W.d_oSharpe_vs_anchor.mean():+.4f} over {len(W)} panels; "
        f"{int((W.d_oSharpe_vs_anchor > 0).sum())} of {len(W)} positive.  Minus its own control "
        f"{W.d_oSharpe_vs_ctrl.mean():+.4f}, {int((W.d_oSharpe_vs_ctrl > 0).sum())} of {len(W)} "
        f"positive.  OOS 4b: {int(W.keep4b_oos.sum())} of {len(W)}; 4a {int(W.keep4a_oos.sum())} "
        f"of {len(W)}.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {OUT.name}.grid.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
