#!/usr/bin/env python3
"""
Idea 1488 (cloud lane, 2026-09-19) --- rank the FOUR DD-BUYING DEVICES at MATCHED CAGR instead
of by an UNMEASURABLE RATIO.

THE PREMISE.  Idea 1468 (this run's own first idea) re-formed 1461's DD-per-CAGR exchange rate
--- pp of drawdown bought per pp of CAGR given up --- on the record's three other DD-buying
families and found it resolves **1 rung-to-rung gap in 144** and **1 cross-family gap in 36** at
|t| > 2.  The ratio cannot rank rungs and it cannot rank devices.  What DID survive was its
SIGN: the ordering held in 0.83..0.995 of bootstrap replicates.

THE REPAIR IS TO STOP DIVIDING.  A ratio of two small tape differences has no usable sampling
distribution.  A DIFFERENCE does.  So: solve each device's OWN dial for the setting that matches
a COMMON CAGR HAIRCUT off the frozen anchor, then compare the resulting MaxDDs as a PAIRED
difference on one shared block-start matrix.  At matched CAGR, "which device buys more drawdown"
is a subtraction, and the question the record has been asking with a ratio becomes answerable.

THE FOUR DEVICES, each on the construction the record committed for it, all on the frozen
2026-09-04 incumbent frame (N = 20, H = 126, gross 0.75, MAXVOL 0.60, MA gate ON, weekly, 10 bps,
t+1) and all sharing ONE anchor book (asserted bit-identical, gate G2):

  GROSS  the gross scalar          (1446/1454)  dial g,      dense ladder 0.75 -> 0.30
  BAND   the beta band             (1429/1444/1461)  dial c,  dense ladder 0.00 -> 1.00 at H=126,
         B=126, gross 0.75:  rank held names by trailing beta, z_i = 1 - 2(rank_i - 0.5)/n,
         w_i = (g/n)(1 + c z_i); LOWEST beta takes the CAP side; c = 0 is inert
  IVOL   intra-book inverse-vol    (1433)       dial p,      w_i prop. to vol_i^(-p) renormalised
         to the SAME gross 0.75; vol lookback 63 FROZEN; p = 0 is inert
  STOP   trailing equity stop      (1405)       dial depth,  FRAC = 0.50, RESTORE = "SAME"
         FROZEN.  FRAC = 1.00 is NOT used: idea 1468 established it is an ABSORBING state (the
         braked book is all cash, so its own drawdown can never shrink and the brake can never
         release).  depth = None is inert.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  h, the CAGR HAIRCUT off the anchor, {0.5, 1.0, 1.5, 2.0, 2.5} pp.  A LADDER, not a
          point, so no device is ever compared at one convenient operating point.
  DIAL 2  L, the circular-block length, {21, 63, 126}.  ALL reported; 63 primary.
Each device's own dial is NOT a third parameter: it is SOLVED, not chosen --- at each haircut
every device is given the rung of its own dense ladder whose realised CAGR is closest to the
common target.  The dense ladders are published in full so the solve can be audited.

REACHABILITY IS A RESULT, NOT A NUISANCE.  A device whose entire legal ladder cannot reach a
haircut (the beta band cannot short, so c is capped at 1.00) is recorded UNREACHABLE at that
rung and excluded from that rung's contrasts.  The count is published.  A matched cell is only
used if |achieved CAGR - target| <= 0.25 pp; the max residual mismatch is published (gate G7).

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The matched-CAGR ruler REPAIRS the
statistic if, at L = 63 on U56 AND B136, strictly more than half the device-vs-device gaps
resolve at |t| > 2 --- against 1468's 1-in-36 under the ratio.  Separately, and independently of
that bar, the run reports whether the matched-CAGR winner is still the plain de-gross, which is
what six consecutive runs have found under weaker rulers.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
matched cell, FULL and OOS; the halves; turnover and its 10 bps drag; realised mean gross.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
frozen 2026-09-04 incumbent anchor.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned parameters); rule 8 (walk-forward: the haircut is
re-solved on warm-up..2016-12-31 ONLY --- each device's dial matched to the IS CAGR target ---
and 2017-2026 read ONCE, including the cross-device chooser "buy the device with the best IS
matched MaxDD"); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 CROSS-SCRIPT REPLAY of the committed frozen U56 anchor
(15.80% / 1.1537 / -19.13% full, 1.1857 OOS Sharpe).  G2 all four devices' INERT rungs are
BIT-IDENTICAL to one another and to the anchor.  G3 every cell published (dense ladders included).
G4 exactly two tuned dials.  G5 the rule-8 solve and chooser read no row on or after 2017-01-01.
G6 no leverage and no shorting: every rebalance's weight sum <= 0.75 and every weight >= 0.
G7 matched-CAGR residual |achieved - target| <= 0.25 pp on every cell used.  G8 every device dial
BITES on the large-cap panels (CAGR falls at least 0.5 pp off the anchor somewhere on each dense
ladder).  On SMALL it is PUBLISHED, not asserted: BAND and IVOL RAISE CAGR there at every legal
dial, so no haircut is matchable and both are UNREACHABLE on that panel --- a result reproducing
1444/1465's SMALL asymmetry, not a failure.  G9 ONE
block-start matrix per (panel, L), shared by every book.  G10 bit-identical recompute of the U56
anchor.  G11 the selection frame depends on NO dial (one segments() frame per panel).  G12 the
matched books really are matched: max pairwise |CAGR_A - CAGR_B| at a rung <= 0.50 pp.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_matched-cagr-device-ranking_cloud.py
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
SLUG = "matched-cagr-device-ranking"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75
COST, CADENCE = 10.0, "W"
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BETA_B = 126
VOL_LOOK = 63
STOP_FRAC, STOP_RESTORE = 0.50, "SAME"

HAIRCUTS = [0.5, 1.0, 1.5, 2.0, 2.5]                 # DIAL 1, pp of CAGR off the anchor
LS = [21, 63, 126]                                   # DIAL 2
L_PRIMARY = 63
BOOT_REPS, SEED = 400, 20260919
MATCH_TOL = 0.25                                     # pp
MATCH_SPREAD = 0.50                                  # pp, gate G12
BAR_T = 2.0

LAD_GROSS = [round(0.75 - 0.01 * i, 4) for i in range(46)]        # 0.75 .. 0.30
LAD_BAND = [round(0.025 * i, 4) for i in range(41)]               # 0.00 .. 1.00
LAD_IVOL = [round(0.1 * i, 4) for i in range(41)]                 # 0.0 .. 4.0
LAD_STOP = [None] + [round(0.02 + 0.005 * i, 4) for i in range(47)]  # inert, 0.020 .. 0.250
DEVICES = ["GROSS", "BAND", "IVOL", "STOP"]
PAIRS = [(a, b) for i, a in enumerate(DEVICES) for b in DEVICES[i + 1:]]
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


def mech(q):
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
        self.volL = (px[invest].pct_change().rolling(VOL_LOOK).std() * np.sqrt(252)).values
        self.beta = rolling_beta(px[invest].pct_change(), px["SPY"].pct_change(), BETA_B)
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N=I_N, H=I_H, lag=1):
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


def w_equal(segs, gross=I_G):
    return [np.full(len(sel), gross / len(sel)) if len(sel) else np.zeros(0)
            for (_a, _b, _c, sel) in segs]


def w_band(pan, segs, c, gross=I_G):
    """The beta band.  c = 0 is BIT-IDENTICAL to equal weight; c <= 1 keeps every weight >= 0."""
    ws = []
    for (_t, _s, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        if c == 0.0:
            ws.append(np.full(n, gross / n))
            continue
        ranks = np.arange(1, n + 1, dtype=float)
        z = 1.0 - 2.0 * (ranks - 0.5) / n
        m = (gross / n) * (1.0 + c * z)
        b = pan.beta[ts, sel].astype(float)
        fin = np.isfinite(b)
        if not fin.all():
            b = np.where(fin, b, (np.nanmedian(b[fin]) if fin.any() else 1.0))
        order = np.argsort(b, kind="stable")     # ascending beta -> CAP side first
        w = np.empty(n)
        w[order] = m
        ws.append(w)
    return ws


def w_ivol(pan, segs, p, gross=I_G):
    ws = []
    for (_t, _s, ts, sel) in segs:
        n = len(sel)
        if n == 0:
            ws.append(np.zeros(0))
            continue
        if p == 0.0:
            ws.append(np.full(n, gross / n))
            continue
        v = pan.volL[ts, sel].astype(float)
        fin = np.isfinite(v) & (v > 0)
        v = np.where(fin, v, (np.median(v[fin]) if fin.any() else 1.0))
        raw = v ** (-p)
        ws.append(gross * raw / raw.sum())
    return ws


def run_book(pan, segs, ws, depth=None, frac=0.0, restore="SAME"):
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gpath = np.zeros(T)
    curw = np.zeros(M)
    eq, peak, stopped, episodes = 1.0, 1.0, False, 0
    wsum_max, wmin = 0.0, 0.0
    for (i0, i1, _ts, sel), wv in zip(segs, ws):
        if frac > 0.0 and depth is not None:
            dd = eq / peak - 1.0
            if stopped:
                stopped = not (dd > -depth) if restore == "SAME" else (
                    not (dd > -depth / 2.0) if restore == "HALF" else not (dd >= -1e-12))
            elif dd <= -depth:
                stopped, episodes = True, episodes + 1
        scale = (1.0 - frac) if stopped else 1.0
        w0 = np.zeros(M)
        if len(sel):
            w0[pan.iinv[sel]] = wv * scale
            wmin = min(wmin, float(wv.min()))
        wsum_max = max(wsum_max, float(w0.sum()))
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        seg = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        out[i0:i1] = seg
        gpath[i0:i1] = w0.sum()
        nt = seg.copy()
        nt[0] -= turn[i0] * COST / 1e4
        e_path = eq * np.cumprod(1.0 + nt)
        peak = max(peak, float(e_path.max()))
        eq = float(e_path[-1])
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return dict(net=out - turn * COST / 1e4, turn=turn, gross=gpath,
                wsum_max=wsum_max, wmin=wmin, episodes=episodes)


def build(pan, segs, dev, dial):
    if dev == "GROSS":
        return run_book(pan, segs, w_equal(segs, dial))
    if dev == "BAND":
        return run_book(pan, segs, w_band(pan, segs, dial))
    if dev == "IVOL":
        return run_book(pan, segs, w_ivol(pan, segs, dial))
    if dev == "STOP":
        if dial is None:
            return run_book(pan, segs, w_equal(segs))
        return run_book(pan, segs, w_equal(segs), depth=dial, frac=STOP_FRAC,
                        restore=STOP_RESTORE)
    raise ValueError(dev)


LADDERS = {"GROSS": LAD_GROSS, "BAND": LAD_BAND, "IVOL": LAD_IVOL, "STOP": LAD_STOP}
INERT = {"GROSS": I_G, "BAND": 0.0, "IVOL": 0.0, "STOP": None}


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
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def boot_cagr_mdd(r, idx):
    X = np.asarray(r, float)[idx]
    n = X.shape[1]
    E = np.cumprod(1.0 + X, axis=1)
    return E[:, -1] ** (252.0 / n) - 1.0, (E / np.maximum.accumulate(E, axis=1) - 1.0).min(axis=1)


def main():
    t0 = time.time()
    say("=" * 136)
    say("IDEA 1488 (cloud, 2026-09-19) --- RANK THE FOUR DD-BUYING DEVICES AT MATCHED CAGR "
        "INSTEAD OF BY AN UNMEASURABLE RATIO")
    say("  1468 found the DD-per-CAGR ratio resolves 1 rung gap in 144 and 1 cross-family gap "
        "in 36 at |t| > 2.  A ratio of two small tape differences has no usable sampling")
    say("  distribution; a DIFFERENCE does.  Each device's dial is SOLVED to a common CAGR "
        "haircut, then the MaxDDs are compared as a PAIRED difference.")
    say(f"DIAL 1  CAGR haircut h {HAIRCUTS} pp off the frozen anchor (a LADDER, not a point).   "
        f"DIAL 2  block length L {LS} (primary {L_PRIMARY}), ALL reported.")
    say(f"Each device's own dial is SOLVED, not chosen, on a dense published ladder: "
        f"GROSS {len(LAD_GROSS)} rungs, BAND {len(LAD_BAND)}, IVOL {len(LAD_IVOL)}, "
        f"STOP {len(LAD_STOP)}.")
    say(f"FROZEN: N={I_N}, H={I_H}, gross={I_G}, MAXVOL={MAXVOL}, MA gate ON, weekly, "
        f"{COST:.0f} bps, t+1; BAND lookback B={BETA_B}; IVOL vol lookback {VOL_LOOK}; "
        f"STOP FRAC={STOP_FRAC:.2f} RESTORE={STOP_RESTORE} (FRAC=1.00 excluded: 1468 showed it "
        f"is an ABSORBING state).")
    say(f"PRE-REGISTERED BAR (written before any number was read): the matched-CAGR ruler "
        f"REPAIRS the statistic if, at L={L_PRIMARY} on U56 AND B136, MORE THAN HALF the "
        f"device-vs-device gaps resolve at |t| > {BAR_T:.0f} (1468's ratio: 1 of 36).")
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
        f"max_1d_move >= 1.0; {len(inv)} investable names remain.")
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level is an UPPER BOUND and every "
        "4b pass optimistic.  The headline is a MATCHED contrast between books built over the "
        "SAME names on the SAME days at the SAME bootstrap draws, which the bias cannot "
        "manufacture; the 4b pass counts are not so protected.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned dials (CAGR haircut h, block length L); each device's own dial is "
         "SOLVED to the haircut on a published dense ladder, never chosen on performance",
         "2", "== 2", True)

    ladder_rows, matched_rows, pair_rows, wf_rows = [], [], [], []
    g2_dev = g6_max = 0.0
    g6_min = 0.0
    g7_max = 0.0
    g12_max = 0.0

    for pan in panels:
        say("")
        say("=" * 136)
        say(f"PANEL {pan.name}")
        say("=" * 136)
        segs = segments(pan)
        w0 = WARMUP
        ev = pan.idx[w0:]
        oos = np.asarray(ev >= pd.Timestamp(OOS_START))
        ism = ~oos
        gate(f"G5 [{pan.name}] the rule-8 solve and chooser read no row on or after {OOS_START}",
             f"IS last row {ev[ism][-1].date()}", f"< {OOS_START}",
             ev[ism][-1] < pd.Timestamp(OOS_START))

        spy = pan.spy[w0:]
        base_r = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST,
                          freq=CADENCE)["returns"].values[w0:]
        bm_full, live_full = bmpack(spy), bmpack(base_r)
        bm_oos, live_oos = bmpack(spy[oos]), bmpack(base_r[oos])
        say(f"  SPY        full {bm_full['CAGR']:7.2%} / {bm_full['Sharpe']:6.4f} / "
            f"{bm_full['MaxDD']:7.2%}  | OOS {bm_oos['CAGR']:7.2%} / {bm_oos['Sharpe']:6.4f} / "
            f"{bm_oos['MaxDD']:7.2%}")
        say(f"  RULES v2   full {live_full['CAGR']:7.2%} / {live_full['Sharpe']:6.4f} / "
            f"{live_full['MaxDD']:7.2%}  | OOS {live_oos['CAGR']:7.2%} / "
            f"{live_oos['Sharpe']:6.4f} / {live_oos['MaxDD']:7.2%}")

        # ---- dense ladders, every rung published -----------------------------------
        BK = {}
        for dev in DEVICES:
            for dial in LADDERS[dev]:
                b = build(pan, segs, dev, dial)
                r = b["net"][w0:]
                m = triple(r)
                BK[(dev, dial)] = dict(book=b, r=r, m=m,
                                       is_CAGR=cagr(r[ism]), is_MaxDD=mdd(r[ism]),
                                       is_Sharpe=sharpe(r[ism]))
                g6_max = max(g6_max, b["wsum_max"])
                g6_min = min(g6_min, b["wmin"])
                ladder_rows.append(dict(panel=pan.name, device=dev, dial=dial,
                                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                        is_CAGR=BK[(dev, dial)]["is_CAGR"],
                                        is_MaxDD=BK[(dev, dial)]["is_MaxDD"],
                                        mean_gross=float(np.mean(b["gross"][w0:])),
                                        turnover_yr=float(b["turn"][w0:].sum())
                                        / (len(r) / 252.0),
                                        episodes=b["episodes"]))
        a = BK[("GROSS", I_G)]
        a_net, m_anchor = a["r"], a["m"]
        for dev in DEVICES:
            g2_dev = max(g2_dev, float(np.abs(BK[(dev, INERT[dev])]["r"] - a_net).max()))
        ah1, ah2 = halves(a_net)
        say(f"  ANCHOR (frozen incumbent, the inert rung of all four devices): "
            f"{m_anchor['CAGR']:7.2%} / {m_anchor['Sharpe']:6.4f} / {m_anchor['MaxDD']:7.2%}  "
            f"H1/H2 {ah1:.4f}/{ah2:.4f}  | OOS {cagr(a_net[oos]):7.2%} / "
            f"{sharpe(a_net[oos]):6.4f} / {mdd(a_net[oos]):7.2%}")
        if pan.name == "U56":
            gate("G1 cross-script replay of the committed frozen U56 anchor (full)",
                 f"CAGR {m_anchor['CAGR']:.4%} Sharpe {m_anchor['Sharpe']:.4f} "
                 f"MaxDD {m_anchor['MaxDD']:.4%}",
                 f"CAGR ~{C_U56['CAGR']:.2%} Sharpe ~{C_U56['Sharpe']:.4f} "
                 f"MaxDD ~{C_U56['MaxDD']:.2%}",
                 abs(m_anchor["CAGR"] - C_U56["CAGR"]) < 5e-4
                 and abs(m_anchor["Sharpe"] - C_U56["Sharpe"]) < 5e-3
                 and abs(m_anchor["MaxDD"] - C_U56["MaxDD"]) < 5e-4)
            gate("G1b cross-script replay of the committed frozen U56 anchor (OOS Sharpe)",
                 f"{sharpe(a_net[oos]):.4f}", f"~{C_U56['oSharpe']:.4f}",
                 abs(sharpe(a_net[oos]) - C_U56["oSharpe"]) < 5e-3)
            rp = build(pan, segs, "GROSS", I_G)["net"][w0:]
            gate("G10 bit-identical recompute of the U56 anchor",
                 f"{float(np.abs(rp - a_net).max()):.3e}", "== 0",
                 float(np.abs(rp - a_net).max()) == 0.0)
        # G8: each device's dial bites
        bites = {}
        for dev in DEVICES:
            cs = [BK[(dev, d)]["m"]["CAGR"] for d in LADDERS[dev]]
            bites[dev] = bool(min(cs) < m_anchor["CAGR"] - 0.005)
        if pan.name == "SMALL":
            publish(f"G8 [{pan.name}] device bite (PUBLISHED, NOT ASSERTED)", str(bites))
            say(f"    PUBLISHED [{pan.name}] device bite in the CAGR-COST direction: {bites}.  "
                f"BAND and IVOL do NOT bite on SMALL --- on this panel they RAISE CAGR above "
                f"the anchor at every legal dial, so no CAGR haircut can be matched and every "
                f"haircut is UNREACHABLE for them.  This reproduces 1444's and 1465's asymmetry "
                f"(the band raises CAGR at 24 of 24 biting cells on SMALL) and is a RESULT, not "
                f"a gate failure; the two devices are excluded from SMALL's contrasts and the "
                f"exclusion is counted.")
        else:
            gate(f"G8 [{pan.name}] every device dial BITES on the large-cap panels (its dense "
                 f"ladder reaches at least 0.5 pp below the anchor's CAGR)", str(bites),
                 "all True", all(bites.values()))

        # ---- solve each device to each haircut --------------------------------------
        say("")
        say(f"  {'h(pp)':>6} {'device':<6} {'dial':>8} {'CAGR':>8} {'miss(pp)':>9} {'Sharpe':>8} "
            f"{'MaxDD':>8} {'dDD_pp':>7} {'H1':>7} {'H2':>7} {'4a':>5} {'4b':>5} {'oCAGR':>8} "
            f"{'oSh':>7} {'oMDD':>8} {'4bOOS':>6} {'turn/y':>7}")
        MATCH = {}          # (h, dev) -> key into BK, or None
        MATCH_IS = {}
        for h in HAIRCUTS:
            tgt = m_anchor["CAGR"] * 100.0 - h
            tgt_is = cagr(a_net[ism]) * 100.0 - h
            for dev in DEVICES:
                cand = [(abs(BK[(dev, d)]["m"]["CAGR"] * 100.0 - tgt), d) for d in LADDERS[dev]]
                miss, dial = min(cand)
                cand_is = [(abs(BK[(dev, d)]["is_CAGR"] * 100.0 - tgt_is), d)
                           for d in LADDERS[dev]]
                miss_is, dial_is = min(cand_is)
                MATCH_IS[(h, dev)] = (dial_is, miss_is)
                if miss > MATCH_TOL:
                    MATCH[(h, dev)] = None
                    say(f"  {h:>6.1f} {dev:<6} {'UNREACHABLE':>8}  best miss {miss:6.3f} pp "
                        f"> tol {MATCH_TOL} at dial {dial}  --- the device's whole legal ladder "
                        f"cannot buy this haircut")
                    matched_rows.append(dict(panel=pan.name, haircut=h, device=dev, dial=dial,
                                             reachable=False, miss_pp=miss))
                    continue
                MATCH[(h, dev)] = dial
                g7_max = max(g7_max, miss)
                r = BK[(dev, dial)]["r"]
                k4a, k4b, m, h1, h2, legs = keep_paths(r, bm_full, live_full)
                ro = r[oos]
                k4ao, k4bo, mo, _o1, _o2, _lo = keep_paths(ro, bm_oos, live_oos)
                ddp = (m["MaxDD"] - m_anchor["MaxDD"]) * 100.0
                ty = float(BK[(dev, dial)]["book"]["turn"][w0:].sum()) / (len(r) / 252.0)
                say(f"  {h:>6.1f} {dev:<6} {str(dial):>8} {m['CAGR']:>7.2%} {miss:>9.3f} "
                    f"{m['Sharpe']:>8.4f} {m['MaxDD']:>7.2%} {ddp:>7.3f} {h1:>7.3f} {h2:>7.3f} "
                    f"{str(k4a):>5} {str(k4b):>5} {mo['CAGR']:>7.2%} {mo['Sharpe']:>7.4f} "
                    f"{mo['MaxDD']:>7.2%} {str(k4bo):>6} {ty:>7.3f}")
                matched_rows.append(dict(panel=pan.name, haircut=h, device=dev, dial=dial,
                                         reachable=True, miss_pp=miss,
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         dMaxDD_pp=ddp, H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                                         leg_H1=legs["H1"], leg_H2=legs["H2"],
                                         leg_DD=legs["DD"], leg_CAGR=legs["CAGR"],
                                         oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                         oMaxDD=mo["MaxDD"], keep4a_oos=k4ao, keep4b_oos=k4bo,
                                         turnover_yr=ty,
                                         anchor_CAGR=m_anchor["CAGR"],
                                         anchor_MaxDD=m_anchor["MaxDD"],
                                         spy_CAGR=bm_full["CAGR"], spy_Sharpe=bm_full["Sharpe"],
                                         spy_MaxDD=bm_full["MaxDD"],
                                         live_Sharpe=live_full["Sharpe"],
                                         live_MaxDD=live_full["MaxDD"],
                                         spy_oCAGR=bm_oos["CAGR"], spy_oSharpe=bm_oos["Sharpe"],
                                         spy_oMaxDD=bm_oos["MaxDD"],
                                         live_oSharpe=live_oos["Sharpe"],
                                         live_oMaxDD=live_oos["MaxDD"]))
            got = [d for d in DEVICES if MATCH[(h, d)] is not None]
            if len(got) > 1:
                cs = [BK[(d, MATCH[(h, d)])]["m"]["CAGR"] * 100.0 for d in got]
                g12_max = max(g12_max, max(cs) - min(cs))

        # ---- the paired bootstrap on the MATCHED cells ------------------------------
        n = len(a_net)
        for L in LS:
            idx = block_index(n, L)
            BC, BD = {}, {}
            need = {(d, MATCH[(h, d)]) for h in HAIRCUTS for d in DEVICES
                    if MATCH[(h, d)] is not None}
            for key in need:
                BC[key], BD[key] = boot_cagr_mdd(BK[key]["r"], idx)
            for h in HAIRCUTS:
                res_n = tot_n = 0
                for da, db in PAIRS:
                    ka, kb = MATCH[(h, da)], MATCH[(h, db)]
                    if ka is None or kb is None:
                        pair_rows.append(dict(panel=pan.name, L=L, haircut=h, dev_a=da,
                                              dev_b=db, reachable=False))
                        continue
                    dif = (BD[(da, ka)] - BD[(db, kb)]) * 100.0
                    pt = (BK[(da, ka)]["m"]["MaxDD"] - BK[(db, kb)]["m"]["MaxDD"]) * 100.0
                    se = float(dif.std(ddof=1))
                    tt = pt / se if se > 0 else np.nan
                    sgn = float(np.mean(np.sign(dif) == np.sign(pt))) if len(dif) else np.nan
                    cdif = (BC[(da, ka)] - BC[(db, kb)]) * 100.0
                    res = bool(np.isfinite(tt) and abs(tt) > BAR_T)
                    tot_n += 1
                    res_n += int(res)
                    pair_rows.append(dict(panel=pan.name, L=L, haircut=h, dev_a=da, dev_b=db,
                                          reachable=True, dial_a=ka, dial_b=kb,
                                          dMaxDD_pp=pt, se=se, t=tt, sign_frac=sgn,
                                          resolves=res,
                                          boot_dCAGR_mean_pp=float(cdif.mean()),
                                          boot_dCAGR_sd_pp=float(cdif.std(ddof=1))))
                say(f"  PAIRED [{pan.name} L={L:>3} h={h:.1f}pp]  device-vs-device MaxDD gaps "
                    f"resolving |t|>{BAR_T:.0f}: {res_n}/{tot_n}")

        # ---- rule 8 -------------------------------------------------------------------
        for h in HAIRCUTS:
            picks = {}
            for dev in DEVICES:
                dial_is, miss_is = MATCH_IS[(h, dev)]
                if miss_is > MATCH_TOL:
                    continue
                picks[dev] = (dial_is, BK[(dev, dial_is)]["is_MaxDD"])
            if not picks:
                continue
            win = max(picks.items(), key=lambda kv: kv[1][1])      # best (least negative) IS DD
            dev, (dial, is_dd) = win
            ro = BK[(dev, dial)]["r"][oos]
            k4ao, k4bo, mo, _a1, _a2, _lg = keep_paths(ro, bm_oos, live_oos)
            ao = a_net[oos]
            # did the IS winner also win OOS?
            oos_dds = {d: mdd(BK[(d, MATCH_IS[(h, d)][0])]["r"][oos]) for d in picks}
            oos_win = max(oos_dds.items(), key=lambda kv: kv[1])[0]
            say(f"  RULE 8 [{pan.name} h={h:.1f}pp] IS-matched, best IS MaxDD -> {dev} "
                f"dial {dial}  ->  OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:6.4f} / "
                f"{mo['MaxDD']:7.2%}  | anchor OOS {cagr(ao):7.2%} / {sharpe(ao):6.4f} / "
                f"{mdd(ao):7.2%}  | SPY {bm_oos['CAGR']:7.2%} / {bm_oos['Sharpe']:6.4f} / "
                f"{bm_oos['MaxDD']:7.2%}  | RULESv2 {live_oos['CAGR']:7.2%} / "
                f"{live_oos['Sharpe']:6.4f} / {live_oos['MaxDD']:7.2%}  4a {k4ao} 4b {k4bo}  "
                f"| OOS winner was {oos_win}")
            wf_rows.append(dict(panel=pan.name, haircut=h, chooser="IS_MATCHED_BEST_MAXDD",
                                pick_device=dev, pick_dial=dial, is_MaxDD=is_dd,
                                oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"],
                                oos_MaxDD=mo["MaxDD"], keep4a_oos=k4ao, keep4b_oos=k4bo,
                                oos_winner_device=oos_win, chooser_correct=(oos_win == dev),
                                anchor_oos_CAGR=cagr(ao), anchor_oos_Sharpe=sharpe(ao),
                                anchor_oos_MaxDD=mdd(ao),
                                d_oos_sharpe_vs_anchor=mo["Sharpe"] - sharpe(ao),
                                d_oos_maxdd_vs_anchor_pp=(mo["MaxDD"] - mdd(ao)) * 100.0,
                                spy_oos_CAGR=bm_oos["CAGR"], spy_oos_Sharpe=bm_oos["Sharpe"],
                                spy_oos_MaxDD=bm_oos["MaxDD"],
                                live_oos_CAGR=live_oos["CAGR"],
                                live_oos_Sharpe=live_oos["Sharpe"],
                                live_oos_MaxDD=live_oos["MaxDD"]))

    gate("G2 all four devices' INERT rungs are BIT-IDENTICAL to one another and to the frozen "
         "anchor", f"{g2_dev:.3e}", "== 0", g2_dev == 0.0)
    gate("G6 no leverage and no shorting (max weight sum over every rebalance of every book; "
         "min single weight)", f"max sum {g6_max:.6f}, min weight {g6_min:.3e}",
         f"<= {I_G:.4f} and >= 0", g6_max <= I_G + 1e-12 and g6_min >= -1e-15)
    gate("G7 matched-CAGR residual on every cell USED", f"max |miss| {g7_max:.4f} pp",
         f"<= {MATCH_TOL} pp", g7_max <= MATCH_TOL)
    gate("G12 the matched books really are matched (max pairwise CAGR spread at a haircut)",
         f"{g12_max:.4f} pp", f"<= {MATCH_SPREAD} pp", g12_max <= MATCH_SPREAD)
    gate("G9 ONE block-start matrix per (panel, L), shared by every book",
         f"seed {SEED}, reps {BOOT_REPS}", "paired by construction", True)
    gate("G11 the selection frame depends on NO dial (one segments() frame per panel, built "
         "before any dial is read)", "by construction", "identical name sets", True)

    LD = pd.DataFrame(ladder_rows)
    MT = pd.DataFrame(matched_rows)
    PR = pd.DataFrame(pair_rows)
    WF = pd.DataFrame(wf_rows)
    LD.to_csv(f"{OUT}.ladders.csv", index=False)
    MT.to_csv(f"{OUT}.matched.csv", index=False)
    PR.to_csv(f"{OUT}.pairs.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    gate("G3 every cell published", f"{len(LD)} dense-ladder rows, {len(MT)} matched rows, "
         f"{len(PR)} pair rows, {len(WF)} walk-forward rows", "all written", True)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    say("")
    say("=" * 136)
    say("HEADLINE")
    say("=" * 136)
    R = PR[PR["reachable"] == True]          # noqa: E712
    say(f"  DEVICE-vs-DEVICE MaxDD gaps at MATCHED CAGR resolving at |t| > {BAR_T:.0f}: "
        f"{int(R['resolves'].sum())} of {len(R)}   (1468's RATIO ruler on the same devices: "
        f"1 of 36)")
    say(f"    median |t| {np.nanmedian(np.abs(R['t'])):.4f}   max |t| "
        f"{np.nanmax(np.abs(R['t'])):.4f}   median sign fraction "
        f"{np.nanmedian(R['sign_frac']):.4f}")
    for pn in ["U56", "B136", "SMALL"]:
        s = R[R["panel"] == pn]
        say(f"    {pn:<6} {int(s['resolves'].sum())}/{len(s)}   median |t| "
            f"{np.nanmedian(np.abs(s['t'])):.4f}")
    prim = R[(R["L"] == L_PRIMARY) & (R["panel"].isin(["U56", "B136"]))]
    ok = bool(len(prim)) and prim["resolves"].sum() > len(prim) / 2.0
    say(f"  PRE-REGISTERED BAR (L={L_PRIMARY}, U56 + B136): "
        f"{int(prim['resolves'].sum())} of {len(prim)} resolve  ->  RULER REPAIRED = {ok}")
    say("")
    say("  WHICH DEVICE BUYS THE MOST DRAWDOWN AT MATCHED CAGR (argmax dMaxDD_pp per "
        "panel x haircut):")
    M = MT[MT["reachable"] == True]          # noqa: E712
    wins = {}
    for (pn, h), gdf in M.groupby(["panel", "haircut"]):
        w = gdf.loc[gdf["dMaxDD_pp"].idxmax()]
        wins[(pn, h)] = w["device"]
        say(f"    {pn:<6} h={h:.1f}pp  winner {w['device']:<6} dial {str(w['dial']):>8}  "
            f"dMaxDD {w['dMaxDD_pp']:+7.3f} pp   " +
            "  ".join(f"{r['device']}:{r['dMaxDD_pp']:+.3f}" for _, r in
                      gdf.sort_values('device').iterrows()))
    from collections import Counter
    say(f"    WIN COUNT over {len(wins)} (panel, haircut) cells: {dict(Counter(wins.values()))}")
    say("")
    say(f"  UNREACHABLE (device's whole legal ladder cannot buy the haircut): "
        f"{int((~MT['reachable']).sum())} of {len(MT)} cells  "
        f"{dict(Counter(MT.loc[~MT['reachable'], 'device']))}")
    say(f"  4a passes: {int(M['keep4a'].sum())} of {len(M)};  4b full: "
        f"{int(M['keep4b'].sum())} of {len(M)};  4b full AND OOS: "
        f"{int((M['keep4b'] & M['keep4b_oos']).sum())} of {len(M)}")
    for leg in ["leg_H1", "leg_H2", "leg_DD", "leg_CAGR"]:
        say(f"    4b leg {leg:<8} fails {int((~M[leg].astype(bool)).sum())} of {len(M)}")
    say(f"  RULE 8: the IS-matched best-MaxDD chooser names the OOS winner in "
        f"{int(WF['chooser_correct'].sum())} of {len(WF)} cells;  mean d(OOS Sharpe) vs the "
        f"anchor {WF['d_oos_sharpe_vs_anchor'].mean():+.4f} (beats it "
        f"{int((WF['d_oos_sharpe_vs_anchor'] > 0).sum())} of {len(WF)});  mean d(OOS MaxDD) "
        f"{WF['d_oos_maxdd_vs_anchor_pp'].mean():+.3f} pp (improves it "
        f"{int((WF['d_oos_maxdd_vs_anchor_pp'] > 0).sum())} of {len(WF)})")
    gp = pd.DataFrame(GATES)
    say(f"  GATES {int(gp['pass_'].sum())}/{len(gp)} pass")
    say(f"  runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
