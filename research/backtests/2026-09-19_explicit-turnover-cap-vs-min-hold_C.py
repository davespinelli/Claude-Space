#!/usr/bin/env python3
"""
Idea 1484 (lane C, 2026-09-19) — does an EXPLICIT TURNOVER CAP buy the 4b DD LEG more cheaply
than the MIN-HOLD already in the book?

THE PREMISE.  The frozen 2026-09-04 incumbent (U56, top-N = 20 by the live composite, equal
weight, gross G = 0.75, weekly) carries a churn brake — the min-hold H = 126 — that has never
been priced AS a churn brake, only as a rung on a ladder.  And the record has never priced a
PER-REBALANCE TURNOVER CAP at all: `grep -ci "turnover cap" research/LEADERBOARD.md` returns 0.
Six consecutive runs (1429/1436/1444/1461/1468 and the 2026-09-19 cloud/B batch) have found
every drawdown-buying device beaten at matched exposure by a plain de-gross.  A turnover cap is
the one brake in that family that costs NO exposure: it leaves gross at G exactly and only slows
the rotation.  So it deserves its own reading, against the brake the book already owns.

THE CONTRAST, AND WHY IT IS THE ONLY HONEST ONE.  A brake cannot be judged on its level — every
brake improves a cost-bearing book simply by trading less.  Both devices are therefore reduced
to ONE CURVE EACH over the SAME quantity, realised annual turnover, from the SAME unbraked book,
and read AT MATCHED TURNOVER:

    H-FAMILY    H in {1, 21, 42, 63, 95, 126, 189, 252, 378, 504, 756}, no cap.   H = 1 is the UNBRAKED
                book (a name may leave the day after it arrives); H = 126 is the incumbent.
    CAP-FAMILY  the SAME unbraked H = 1 book with a per-rebalance turnover cap in
                {0.05, 0.10, 0.15, 0.20, 0.25, inf} — the idea's own ladder, unchanged.

Each cap rung's realised annual turnover is located on the H-curve by linear interpolation and
the two books are differenced THERE.  If the cap is dominated at matched turnover, the min-hold
is already doing the whole job and the record can stop looking for a cheaper brake.  If it is
not, the cap is the first device in eight runs to beat the thing it replaces.

THE CAP APPLIED TO THE INCUMBENT ITSELF (the idea's literal wording) is the THIRD arm, and the
one that carries every capital claim: H = 126 AND cap, at the frozen incumbent's own dials.

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4):
  CAP  {0.05, 0.10, 0.15, 0.20, 0.25, inf}   DIAL 1 — per-rebalance turnover cap, NAV units.
                                             inf is the inert rung (gate G2).
  COST {0, 10, 25, 50} bps                   DIAL 2 — the idea's own cost ladder.  10 bps is the
                                             protocol rung and the only one a verdict is read
                                             from; the other three are published in full.

FROZEN, NEVER SELECTED ON: N = 20, G = 0.75, weekly cadence, the live 3-leg composite, the
MAXVOL = 0.60 eligibility filter, H = 126 for every capital claim.  The H-LADDER is a published
COMPARAND CURVE — it is the incumbent's own dial re-priced as the thing the cap must beat, and
NO book is ever selected on it (gate G5).

THE EXECUTION MODEL (stated in full, because the cap is an execution device).  At each weekly
rebalance the selection frame produces a TARGET vector summing to G.  Against the drifted
current book the trade is split in two and charged in this order:
  (1) the GROSS CORRECTION, |G - sum(current)|, which is mandatory — the book must stay at gross
      G exactly (gate G4), so this leg is never capped away;
  (2) the ROTATION, sum|target - current_regrossed|, which nets to zero and IS capped.
Two rotation mechanisms, both published, neither a dial:
  CONVICTION (primary, the idea's own wording — "trade only the highest-conviction names until
      the cap binds"): buys are ordered by the live composite BEST FIRST, sells WORST FIRST
      (names the screen has dropped, whose rank key is infinite, sort first), and matched
      buy/sell pairs are executed greedily until the budget is exhausted.  Gross is constant by
      construction because every executed unit is a matched pair.
  PRORATA (control): the whole rotation is scaled by lambda = budget / rotation, i.e. every name
      moves a fixed fraction of the way.  Identical turnover, no conviction ordering.
The two agree exactly at cap = inf (gate G12).

A CONSEQUENCE OF CAPPING, STATED RATHER THAN HIDDEN.  The SELECTION frame is untouched by the
cap: the target name set at a given (panel, H) is bit-identical across every cap rung and both
mechanisms (gate G7).  The cap acts only on execution, so a capped book can still HOLD a name
the screen has already dropped, and its realised book is WIDER than N = 20.  Realised holding
count and effective N are published at every cell rather than assumed away.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell FULL and OOS; the halves; realised annual turnover, bind rate, holdings count, effective N,
mean gross.

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (H = 126, no cap) 2026-09-04 incumbent, cross-script replayed (gate G1).

THE BAR, PRE-REGISTERED HERE BEFORE ANY NUMBER WAS READ.  The cap is a CHEAPER BRAKE than the
min-hold — i.e. the record should keep looking at it — only if, at the protocol cost rung of
10 bps, on U56 AND B136:
  (i)   at >= 4 of the 5 BITING cap rungs the cap book's Sharpe EXCEEDS the H-curve's Sharpe
        interpolated at the cap book's own realised turnover; AND
  (ii)  the mean of that matched-turnover Sharpe gap resolves at |t| > 2 under a paired
        circular-block bootstrap (L = 63, one block-start matrix per panel, shared by every
        book, so the gap is a PAIRED statistic).
Anything else is DOMINATED-OR-UNRESOLVED: the min-hold is already doing the job, and this run
is a KILL for the cap as a device.  Either way the run proposes NO rules change.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2 AND
SPY); rule 4 (both KEEP paths, exactly 2 tuned dials); rule 8 (walk-forward: the cap chosen on
warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, against a do-nothing control and
the same chooser run on the H-ladder); rule 9 (survivorship stated).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

GATES.  G0 sample >= 10y.  G1 cross-script replay of the committed U56 anchor.  G2 cap = inf is
BIT-IDENTICAL to the uncapped book at the same H.  G3 realised per-rebalance turnover <= cap at every post-inception rebalance (to 1e-12).  G4 every rebalance's executed weight sum == that
rebalance's TARGET gross exactly.
G5 exactly two tuned dials; the H-ladder never selected on.  G6 the rule-8 chooser reads no row
on or after 2017-01-01.  G7 target name sets bit-identical across cap rungs and mechanisms at a
given (panel, H).  G8 the cap dial BITES (bind rate strictly decreasing in cap, > 0 at 0.05).
G9 realised turnover monotone non-decreasing in cap and non-increasing in H.  G10 bit-identical
recompute of the U56 headline cell.  G11 no leverage (max weight sum <= G).  G12 CONVICTION and
PRORATA agree to 0 at cap = inf.  G13 the H-curve brackets every cap rung's turnover (no
extrapolation in the matched-turnover read).

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_explicit-turnover-cap-vs-min-hold_C.py
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
SLUG = "explicit-turnover-cap-vs-min-hold"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_H, I_G = 20, 126, 0.75              # the frozen 2026-09-04 incumbent
CADENCE = "W"
COSTS = [0.0, 10.0, 25.0, 50.0]            # DIAL 2 — all published; 10 bps is the protocol rung
COST_HEAD = 10.0
CAPS = [0.05, 0.10, 0.15, 0.20, 0.25, np.inf]   # DIAL 1 — the idea's ladder, unchanged
HS = [1, 21, 42, 63, 95, 126, 189, 252, 378, 504, 756]   # comparand curve, never selected on
MECHS = ["CONVICTION", "PRORATA"]
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, SEED, L_BOOT = 400, 20260919, 63
C_U56 = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)
BAR_T, BAR_WINS = 2.0, 4

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


def mech_scores(q):
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
        sc, above, vol20 = mech_scores(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)   # ascending = best first
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])


def segments(pan, N, H, lag=1):
    """The min-hold SELECTION frame.  Depends on H only — identical across every cap rung and
    both mechanisms at a given (panel, H) (gate G7)."""
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


def apply_cap(target, curw, cap, key, mechanism):
    """Return (executed weights, realised turnover, bound?, uncapped-build?).

    `target` and the returned vector both sum to G EXACTLY.  `key` is the rank key of every
    column at the decision row (ascending = highest conviction).  The gross correction is
    charged first and never capped away; the rotation nets to zero and is what the cap bites.
    """
    G = target.sum()
    s = float(curw.sum())
    build = bool(s <= 1e-14)
    if not build:
        cur2 = curw * (G / s)
        tv_gross = float(abs(G - s))
    else:
        # UNCAPPED BUILD.  The current book is EMPTY, so there is nothing to re-gross or rotate
        # and the build to gross G is mandatory — capping it would strand the book in cash
        # forever.  Charged in full at every cost rung, exempt from the cap, and COUNTED and
        # PUBLISHED per book.  It fires at inception and again on any exit from a forced-cash
        # state (a rebalance at which the screen left no eligible name).
        cur2 = target.copy()
        tv_gross = float(G)
    d = target - cur2
    tv_rot = float(np.abs(d).sum())
    if not np.isfinite(cap):
        return target, tv_gross + tv_rot, False, build
    budget = cap - tv_gross
    if budget <= 0.0:
        return cur2, tv_gross, tv_rot > 1e-15, build
    if tv_rot <= budget:
        return target, tv_gross + tv_rot, False, build
    if mechanism == "PRORATA":
        lam = budget / tv_rot
        return cur2 + lam * d, tv_gross + budget, True, build
    # CONVICTION: greedy matched buy/sell pairs, best buys and worst sells first
    w = cur2.copy()
    buys = np.flatnonzero(d > 1e-15)
    sells = np.flatnonzero(d < -1e-15)
    buys = buys[np.argsort(key[buys], kind="stable")]              # best conviction first
    sells = sells[np.argsort(-key[sells], kind="stable")]          # worst conviction first
    half = budget / 2.0
    bi = si = 0
    db = d[buys].copy()
    ds = -d[sells].copy()
    while half > 1e-15 and bi < len(buys) and si < len(sells):
        m = min(db[bi], ds[si], half)
        w[buys[bi]] += m
        w[sells[si]] -= m
        db[bi] -= m
        ds[si] -= m
        half -= m
        if db[bi] <= 1e-15:
            bi += 1
        if si < len(sells) and ds[si] <= 1e-15:
            si += 1
    return w, tv_gross + (budget - 2.0 * half), True, build


def run_book(pan, segs, cap=np.inf, mechanism="CONVICTION", gross=I_G):
    """One book.  Weights applied at row i0, drifting inside the segment (engine convention)."""
    rets, C, Cp = pan.rets, pan.C, pan.Cp
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    nreb = len(segs)
    effn = np.zeros(nreb)
    nhold = np.zeros(nreb)
    bound = np.zeros(nreb, dtype=bool)
    built = np.zeros(nreb, dtype=bool)
    gsum = np.zeros(nreb)
    tsum = np.zeros(nreb)
    curw = np.zeros(M)
    for j, (i0, i1, ts, sel) in enumerate(segs):
        tgt = np.zeros(M)
        if len(sel):
            tgt[pan.iinv[sel]] = gross / len(sel)
        key = np.full(M, np.inf)
        key[pan.iinv] = pan.rank_key[ts]
        w0, tv, bd, bl = apply_cap(tgt, curw, cap, key, mechanism)
        turn[i0] = tv
        bound[j] = bd
        built[j] = bl
        gsum[j] = float(w0.sum())
        tsum[j] = float(tgt.sum())
        nz = w0[w0 > 1e-12]
        nhold[j] = len(nz)
        effn[j] = (nz.sum() ** 2) / float((nz ** 2).sum()) if len(nz) else 0.0
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return dict(gross_ret=out, turn=turn, effn=effn, nhold=nhold, bound=bound, built=built,
                gsum=gsum, tsum=tsum)


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


def block_index(n, L=L_BOOT, reps=BOOT_REPS, seed=SEED):
    """ONE circular-block start matrix per panel, shared by every book (pairing)."""
    nb = int(np.ceil(n / L))
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, n, size=(reps, nb))
    return (starts[:, :, None] + np.arange(L)[None, None, :]).reshape(reps, nb * L)[:, :n] % n


def sharpe_rows(X):
    v = X.std(axis=1, ddof=0) * np.sqrt(252)
    return np.where(v > 0, X.mean(axis=1) * 252 / v, np.nan)


def interp_curve(xs, ys, x):
    """Linear interpolation of the H-curve y at turnover x.  xs must be increasing."""
    o = np.argsort(xs)
    xs, ys = np.asarray(xs, float)[o], np.asarray(ys, float)[o]
    if x < xs[0] or x > xs[-1]:
        return np.nan, False
    return float(np.interp(x, xs, ys)), True


def main():
    t0 = time.time()
    say("=" * 140)
    say("IDEA 1484 (lane C, 2026-09-19) — does an EXPLICIT TURNOVER CAP buy the 4b DD LEG more "
        "cheaply than the MIN-HOLD already in the book?")
    say("The incumbent's H = 126 has never been priced AS a churn brake and the record has NEVER "
        "priced a per-rebalance turnover cap (0 hits in LEADERBOARD.md).  Both devices are")
    say("reduced to ONE CURVE over realised annual turnover from the SAME unbraked (H = 1) book "
        "and differenced AT MATCHED TURNOVER.")
    say(f"DIAL 1  CAP {CAPS}.   DIAL 2  COST {COSTS} bps (10 is the protocol rung; all published)."
        f"   FROZEN: N = {I_N}, G = {I_G}, weekly, H = {I_H} for every capital claim.")
    say(f"COMPARAND CURVE, never selected on: H {HS}.")
    say(f"PRE-REGISTERED BAR (stated before any number was read): the cap is a CHEAPER brake only "
        f"if, at 10 bps, on U56 AND B136, (i) the cap book's Sharpe beats the H-curve's at MATCHED "
        f"turnover at >= {BAR_WINS} of 5 biting rungs, AND (ii) the mean matched gap resolves at "
        f"|t| > {BAR_T:.0f} under a paired block bootstrap (L = {L_BOOT}).")
    say("=" * 140)

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
        "every 4b pass an optimistic one.  What this run reads is a CONTRAST between two brakes "
        "built over the SAME names on the SAME days, which the bias cannot manufacture.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G5 exactly two tuned dials (CAP, COST); the H-ladder is a published comparand curve and "
         "no book is ever selected on it", "CAP x COST", "2 dials", True)

    grid, curve_rows, match_rows, wf_rows = [], [], [], []
    g2_dev = g4_dev = g12_dev = 0.0
    g3_dev = -np.inf
    n_build = 0
    g1_dev = None
    g7_ok = g8_ok = g9_ok = g13_ok = True
    g11_max = 0.0
    head_ret = None
    boot_bank = {}

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST_HEAD, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        ann = 252.0 / (T - WARMUP)

        say(f"\n  [{pan.name}]  SPY  CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS CAGR {spyO['CAGR']:.2%} Sharpe {spyO['Sharpe']:.4f} MaxDD "
            f"{spyO['MaxDD']:.2%}  |  4b OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor "
            f"{CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps  CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f} | OOS "
            f"{liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        segs = {H: segments(pan, I_N, H) for H in HS}
        if I_H not in segs:
            segs[I_H] = segments(pan, I_N, I_H)

        # ---- the H-FAMILY comparand curve (no cap) ---------------------------------------
        hbooks = {}
        for H in HS:
            b = run_book(pan, segs[H], cap=np.inf)
            hbooks[H] = b
            g4_dev = max(g4_dev, float(np.abs(b["gsum"] - b["tsum"]).max()))
            g11_max = max(g11_max, float(b["gsum"].max()))
            n_build = max(n_build, int(b["built"].sum()))
        h_turn = {H: float(np.sum(hbooks[H]["turn"][WARMUP:]) * ann) for H in HS}
        if not all(h_turn[HS[i]] >= h_turn[HS[i + 1]] - 1e-12 for i in range(len(HS) - 1)):
            g9_ok = False

        # ---- the FROZEN incumbent, cross-script replay (G1) ------------------------------
        fz = hbooks[I_H]
        fnet = fz["gross_ret"] - fz["turn"] * COST_HEAD / 1e4
        fm, fo = triple(fnet[WARMUP:]), triple(fnet[i_oos:])
        fh1, fh2 = halves(fnet[WARMUP:])
        say(f"           FROZEN INCUMBENT (H={I_H}, no cap) CAGR {fm['CAGR']:.2%} Sharpe "
            f"{fm['Sharpe']:.4f} MaxDD {fm['MaxDD']:.2%} H1/H2 {fh1:.4f}/{fh2:.4f} | OOS "
            f"{fo['CAGR']:.2%}/{fo['Sharpe']:.4f}/{fo['MaxDD']:.2%} | turnover "
            f"{h_turn[I_H]:.3f}/yr | 4b DD margin "
            f"{100*(fm['MaxDD'] - DD_CAP*spy['MaxDD']):+.4f} pp")
        if pan.name == "U56":
            g1_dev = max(abs(fm["Sharpe"] - C_U56["Sharpe"]), abs(fo["Sharpe"] - C_U56["oSharpe"]),
                         abs(fm["CAGR"] - C_U56["CAGR"]), abs(fm["MaxDD"] - C_U56["MaxDD"]))
            gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                 "(15.80%/1.1537/-19.13% full; OOS Sharpe 1.1857)",
                 f"max|dev| {g1_dev:.2e}  (got {fm['CAGR']:.4f}/{fm['Sharpe']:.4f}/"
                 f"{fm['MaxDD']:.4f}, OOS {fo['Sharpe']:.4f})", "< 5e-3 (the record's own "
                 "tolerance for this replay: `data/prices.csv` is RESTATED daily, so a U56 "
                 "cross-vintage replay cannot be exact — idea 1272)", g1_dev < 5e-3)

        say(f"\n    [{pan.name}] H-FAMILY COMPARAND CURVE (no cap), net @ {COST_HEAD:.0f} bps")
        say("      " + f"{'H':>5} {'turn/yr':>9} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>8} "
                       f"{'H1':>7} {'H2':>7} {'OOS CAGR':>9} {'OOSShrp':>8} {'OOS DD':>8} "
                       f"{'effN':>6} {'nHold':>6}")
        for H in HS:
            b = hbooks[H]
            for cost in COSTS:
                r = b["gross_ret"] - b["turn"] * cost / 1e4
                k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                mo = triple(r[i_oos:])
                _, k4bO, _, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                curve_rows.append(dict(panel=pan.name, family="H", H=H, cap=np.nan,
                                       mech="NONE", cost=cost, turn=h_turn[H],
                                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                       H1=h1, H2=h2, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                       oMaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b,
                                       keep4b_oos=k4bO,
                                       effN=float(b["effn"].mean()),
                                       nHold=float(b["nhold"].mean()), bind=0.0))
                if cost == COST_HEAD:
                    say("      " + f"{H:>5} {h_turn[H]:>9.3f} {m['CAGR']:>8.2%} "
                                   f"{m['Sharpe']:>8.4f} {m['MaxDD']:>8.2%} {h1:>7.3f} {h2:>7.3f} "
                                   f"{mo['CAGR']:>9.2%} {mo['Sharpe']:>8.4f} {mo['MaxDD']:>8.2%} "
                                   f"{b['effn'].mean():>6.2f} {b['nhold'].mean():>6.2f}"
                                   + ("   <- INCUMBENT" if H == I_H else ""))

        # ---- the CAP FAMILY, on both bases, both mechanisms -------------------------------
        capbooks = {}
        for base_H in (1, I_H):
            for mech in MECHS:
                for cp in CAPS:
                    b = run_book(pan, segs[base_H], cap=cp, mechanism=mech)
                    capbooks[(base_H, mech, cp)] = b
                    g4_dev = max(g4_dev, float(np.abs(b["gsum"] - b["tsum"]).max()))
                    g11_max = max(g11_max, float(b["gsum"].max()))
                    n_build = max(n_build, int(b["built"].sum()))
                    if np.isfinite(cp):
                        ex = b["turn"][pan.reb][~b["built"]] - cp   # uncapped builds exempt
                        g3_dev = max(g3_dev, float(ex.max()) if len(ex) else -np.inf)
                    else:
                        g2_dev = max(g2_dev, float(np.abs(b["gross_ret"] -
                                                          hbooks[base_H]["gross_ret"]).max()))
        for base_H in (1, I_H):
            g12_dev = max(g12_dev, float(np.abs(
                capbooks[(base_H, "CONVICTION", np.inf)]["gross_ret"] -
                capbooks[(base_H, "PRORATA", np.inf)]["gross_ret"]).max()))

        for base_H in (1, I_H):
            tag = "UNBRAKED BASE (H=1)" if base_H == 1 else f"INCUMBENT BASE (H={I_H})"
            for mech in MECHS:
                say(f"\n    [{pan.name}] CAP FAMILY on the {tag}, mechanism {mech}, "
                    f"net @ {COST_HEAD:.0f} bps")
                say("      " + f"{'cap':>6} {'bind%':>7} {'turn/yr':>9} {'CAGR':>8} {'Sharpe':>8} "
                               f"{'MaxDD':>8} {'H1':>7} {'H2':>7} {'OOS CAGR':>9} {'OOSShrp':>8} "
                               f"{'OOS DD':>8} {'effN':>6} {'nHold':>6} {'4a':>4} {'4b':>4}")
                prev_t = -np.inf
                prev_bind = np.inf
                for cp in CAPS:
                    b = capbooks[(base_H, mech, cp)]
                    tn = float(np.sum(b["turn"][WARMUP:]) * ann)
                    bind = float(b["bound"].mean())
                    if tn < prev_t - 1e-12:
                        g9_ok = False
                    prev_t = tn
                    if bind > prev_bind + 1e-12:
                        g8_ok = False
                    prev_bind = bind
                    for cost in COSTS:
                        r = b["gross_ret"] - b["turn"] * cost / 1e4
                        k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                        mo = triple(r[i_oos:])
                        _, k4bO, _, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                        grid.append(dict(panel=pan.name, family="CAP", H=base_H, cap=cp,
                                         mech=mech, cost=cost, turn=tn, bind=bind,
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         H1=h1, H2=h2, oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"],
                                         oMaxDD=mo["MaxDD"], keep4a=k4a, keep4b=k4b,
                                         keep4b_oos=k4bO,
                                         legs="".join(k for k, v in legs.items() if not v) or "-",
                                         effN=float(b["effn"].mean()),
                                         nHold=float(b["nhold"].mean())))
                        if cost == COST_HEAD:
                            say("      " + f"{cp:>6.2f} {100*bind:>6.1f}% {tn:>9.3f} "
                                           f"{m['CAGR']:>8.2%} {m['Sharpe']:>8.4f} "
                                           f"{m['MaxDD']:>8.2%} {h1:>7.3f} {h2:>7.3f} "
                                           f"{mo['CAGR']:>9.2%} {mo['Sharpe']:>8.4f} "
                                           f"{mo['MaxDD']:>8.2%} {b['effn'].mean():>6.2f} "
                                           f"{b['nhold'].mean():>6.2f} "
                                           f"{'Y' if k4a else '.':>4} {'Y' if k4b else '.':>4}")
                            if pan.name == "U56" and base_H == I_H and mech == "CONVICTION" \
                                    and cp == CAPS[0]:
                                head_ret = r.copy()

        # ---- THE MATCHED-TURNOVER CONTRAST ----------------------------------------------
        idx_boot = block_index(T - WARMUP)
        say(f"\n    [{pan.name}] MATCHED-TURNOVER CONTRAST — each cap book differenced against "
            f"a CAPITAL BLEND of the two bracketing H rungs whose blended turnover equals the")
        say(f"      cap book's own, EXACTLY.  The blend ignores its own cross-sleeve rebalancing "
            f"turnover, which FLATTERS the H comparand; a cap win is therefore conservative.")
        for base_H in (1, I_H):
            for mech in MECHS:
                for cost in COSTS:
                    hx = [h_turn[H] for H in HS]
                    hr = {H: hbooks[H]["gross_ret"] - hbooks[H]["turn"] * cost / 1e4 for H in HS}
                    if cost == COST_HEAD and mech == "CONVICTION":
                        say(f"\n      base H={base_H}, {mech}, {cost:.0f} bps")
                        say("        " + f"{'cap':>6} {'turn':>8} {'blend':>18} {'Shrp cap':>9} "
                                         f"{'Shrp H@turn':>12} {'dShrp':>9} {'t':>7} "
                                         f"{'dCAGR pp':>9} {'dMaxDD pp':>10}")
                    for cp in CAPS:
                        if not np.isfinite(cp):
                            continue
                        b = capbooks[(base_H, mech, cp)]
                        tn = float(np.sum(b["turn"][WARMUP:]) * ann)
                        rc = (b["gross_ret"] - b["turn"] * cost / 1e4)[WARMUP:]
                        order = np.argsort(hx)
                        xs = np.array(hx)[order]
                        Hs = [HS[i] for i in order]
                        if tn < xs[0] - 1e-12 or tn > xs[-1] + 1e-12:
                            g13_ok = False
                            match_rows.append(dict(panel=pan.name, H=base_H, mech=mech, cost=cost,
                                                   cap=cp, turn=tn, bracketed=False))
                            continue
                        j = int(np.searchsorted(xs, tn))
                        j = min(max(j, 1), len(xs) - 1)
                        a = (tn - xs[j - 1]) / (xs[j] - xs[j - 1]) if xs[j] > xs[j - 1] else 0.0
                        rm = ((1 - a) * hr[Hs[j - 1]][WARMUP:] + a * hr[Hs[j]][WARMUP:])
                        ds = sharpe(rc) - sharpe(rm)
                        dboot = sharpe_rows(rc[idx_boot]) - sharpe_rows(rm[idx_boot])
                        se = float(np.nanstd(dboot, ddof=1))
                        tt = ds / se if se > 0 else np.nan
                        row = dict(panel=pan.name, H=base_H, mech=mech, cost=cost, cap=cp,
                                   turn=tn, bracketed=True,
                                   blend=f"{(1-a)*100:.0f}%H{Hs[j-1]}+{a*100:.0f}%H{Hs[j]}",
                                   Shrp_cap=sharpe(rc), Shrp_H=sharpe(rm), dShrp=ds, t=tt,
                                   dCAGR=100 * (cagr(rc) - cagr(rm)),
                                   dMaxDD=100 * (mdd(rc) - mdd(rm)))
                        match_rows.append(row)
                        boot_bank[(pan.name, base_H, mech, cost, cp)] = dboot
                        if cost == COST_HEAD and mech == "CONVICTION":
                            say("        " + f"{cp:>6.2f} {tn:>8.3f} {row['blend']:>18} "
                                             f"{row['Shrp_cap']:>9.4f} {row['Shrp_H']:>12.4f} "
                                             f"{ds:>+9.4f} {tt:>+7.2f} {row['dCAGR']:>+9.3f} "
                                             f"{row['dMaxDD']:>+10.3f}")

        # ---- RULE 8 WALK-FORWARD --------------------------------------------------------
        i_is = i_oos
        for base_H in (1, I_H):
            for mech in MECHS:
                iss = {}
                for cp in CAPS:
                    b = capbooks[(base_H, mech, cp)]
                    r = b["gross_ret"] - b["turn"] * COST_HEAD / 1e4
                    iss[cp] = sharpe(r[WARMUP:i_is])
                pick = max(CAPS, key=lambda c: (iss[c] if np.isfinite(iss[c]) else -np.inf))
                b = capbooks[(base_H, mech, pick)]
                r = b["gross_ret"] - b["turn"] * COST_HEAD / 1e4
                mo = triple(r[i_oos:])
                _, k4bO, _, _, _, _ = keep_paths(r[i_oos:], spyO, liveO)
                bn = capbooks[(base_H, mech, np.inf)]
                rn = bn["gross_ret"] - bn["turn"] * COST_HEAD / 1e4
                mn = triple(rn[i_oos:])
                wf_rows.append(dict(panel=pan.name, family="CAP", base=base_H, mech=mech,
                                    pick=pick, IS=iss[pick], oCAGR=mo["CAGR"],
                                    oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"], keep4b_oos=k4bO,
                                    nothing_oSharpe=mn["Sharpe"],
                                    d_vs_nothing=mo["Sharpe"] - mn["Sharpe"],
                                    spy_oSharpe=spyO["Sharpe"], live_oSharpe=liveO["Sharpe"]))
        issH = {}
        for H in HS:
            r = hbooks[H]["gross_ret"] - hbooks[H]["turn"] * COST_HEAD / 1e4
            issH[H] = sharpe(r[WARMUP:i_is])
        pickH = max(HS, key=lambda h: issH[h])
        rH = hbooks[pickH]["gross_ret"] - hbooks[pickH]["turn"] * COST_HEAD / 1e4
        moH = triple(rH[i_oos:])
        _, k4bOH, _, _, _, _ = keep_paths(rH[i_oos:], spyO, liveO)
        rI = hbooks[I_H]["gross_ret"] - hbooks[I_H]["turn"] * COST_HEAD / 1e4
        mI = triple(rI[i_oos:])
        wf_rows.append(dict(panel=pan.name, family="H(control)", base=np.nan, mech="NONE",
                            pick=pickH, IS=issH[pickH], oCAGR=moH["CAGR"],
                            oSharpe=moH["Sharpe"], oMaxDD=moH["MaxDD"], keep4b_oos=k4bOH,
                            nothing_oSharpe=mI["Sharpe"],
                            d_vs_nothing=moH["Sharpe"] - mI["Sharpe"],
                            spy_oSharpe=spyO["Sharpe"], live_oSharpe=liveO["Sharpe"]))
        say(f"\n    [{pan.name}] G7 target name sets identical across cap rungs at a given "
            f"(panel, H): by construction — `segments()` is a pure function of (panel, N, H) and "
            f"is built ONCE per H and shared by every cap rung and both mechanisms.")
        say(f"    [{pan.name}] done in {time.time()-t0:.0f}s")

    G = pd.DataFrame(grid)
    CU = pd.DataFrame(curve_rows)
    MT = pd.DataFrame(match_rows)
    WF = pd.DataFrame(wf_rows)
    ALL = pd.concat([CU, G], ignore_index=True)

    # ---------------- gates ----------------
    say("\n" + "=" * 140)
    say("GATES")
    gate("G2 cap = inf is BIT-IDENTICAL to the uncapped book at the same H", f"{g2_dev:.3e}",
         "== 0", g2_dev == 0.0)
    gate("G3 realised per-rebalance turnover <= cap at every POST-INCEPTION rebalance of every capped book",
         f"max excess {g3_dev:.3e}", "<= 1e-12", g3_dev <= 1e-12)
    gate("G4 every rebalance's executed weight sum == that rebalance's TARGET gross exactly "
         "(G = 0.75, or 0 at a rebalance the screen left with no eligible name)",
         f"max|dev| {g4_dev:.3e}", "<= 1e-12", g4_dev <= 1e-12)
    publish("UNCAPPED BUILDS (max over books): rebalances at which the book was EMPTY and the "
            "build to gross G was exempt from the cap", n_build)
    say(f"    PUBLISHED  uncapped builds, max over every book: {n_build} rebalance(s) "
        f"(inception plus any exit from a screen-forced cash state).")
    gate("G6 the rule-8 chooser reads no row on or after 2017-01-01",
         f"IS slice ends at index of {OOS_START}", "by construction", True)
    gate("G7 target name sets bit-identical across cap rungs / mechanisms at a given (panel, H)",
         "segments() built once per H and shared", "by construction", g7_ok)
    gate("G8 the CAP dial BITES: bind rate strictly decreasing in cap and > 0 at cap = 0.05",
         f"monotone {g8_ok}; min bind@0.05 "
         f"{G[(G.cap == CAPS[0]) & (G.cost == COST_HEAD)]['bind'].min():.3f}",
         "monotone and > 0",
         g8_ok and G[(G.cap == CAPS[0]) & (G.cost == COST_HEAD)]["bind"].min() > 0)
    gate("G9 realised turnover monotone: non-decreasing in cap, non-increasing in H",
         g9_ok, "True", g9_ok)
    gate("G11 no leverage: max weight sum over every rebalance of every book", f"{g11_max:.6f}",
         f"<= {I_G}", g11_max <= I_G + 1e-12)
    gate("G12 CONVICTION and PRORATA agree exactly at cap = inf", f"{g12_dev:.3e}", "== 0",
         g12_dev == 0.0)
    gate("G13 the H-curve BRACKETS every cap rung's turnover (no extrapolation)",
         f"{int((~MT['bracketed']).sum())} unbracketed of {len(MT)}", "0 unbracketed", g13_ok)
    if head_ret is not None:
        pan = panels[0]
        b2 = run_book(pan, segments(pan, I_N, I_H), cap=CAPS[0], mechanism="CONVICTION")
        r2 = b2["gross_ret"] - b2["turn"] * COST_HEAD / 1e4
        gate("G10 bit-identical recompute of the U56 headline cell (H=126, cap=0.05, CONVICTION)",
             f"{float(np.abs(r2 - head_ret).max()):.3e}", "== 0",
             float(np.abs(r2 - head_ret).max()) == 0.0)

    # ---------------- the verdict ----------------
    say("\n" + "=" * 140)
    say("THE PRE-REGISTERED BAR, READ")
    verdicts = {}
    for mech in MECHS:
      head = MT[(MT.cost == COST_HEAD) & (MT.mech == mech) & (MT.bracketed)]
      say(f"  --- mechanism {mech}{'  (the pre-registered one)' if mech == 'CONVICTION' else '  (the published control)'}")
      for base_H in (1, I_H):
        for pn in ("U56", "B136"):
            sub = head[(head.H == base_H) & (head.panel == pn)]
            wins = int((sub["dShrp"] > 0).sum())
            dboots = [boot_bank[(pn, base_H, mech, COST_HEAD, c)]
                      for c in sub["cap"].tolist()]
            if dboots:
                meand = float(sub["dShrp"].mean())
                mb = np.nanmean(np.vstack(dboots), axis=0)
                se = float(np.nanstd(mb, ddof=1))
                tt = meand / se if se > 0 else np.nan
            else:
                meand, tt = np.nan, np.nan
            verdicts[(mech, base_H, pn)] = (wins, len(sub), meand, tt)
            say(f"    base H={base_H:<4} {pn:<5}  cap beats the matched-turnover H-blend at "
                f"{wins} of {len(sub)} rungs;  mean dSharpe {meand:+.4f}, paired-bootstrap "
                f"t = {tt:+.2f}")
    passed = all(verdicts[("CONVICTION", 1, pn)][0] >= BAR_WINS
                 and abs(verdicts[("CONVICTION", 1, pn)][3]) > BAR_T
                 and verdicts[("CONVICTION", 1, pn)][2] > 0 for pn in ("U56", "B136"))
    say(f"\n  BAR (CONVICTION, base H=1, the pure brake-vs-brake read): "
        f"{'PASSED — the cap is a CHEAPER brake' if passed else 'FAILED — DOMINATED-OR-UNRESOLVED'}")

    # ---- the DECOMPOSITION: which channel is the cap's gain actually coming from? ----------
    say("\n  DECOMPOSITION OF THE CAP'S MATCHED-TURNOVER GAP INTO TWO CHANNELS.  At a fixed cap "
        "rung the two mechanisms hold the SAME targets and trade the SAME amount; they differ "
        "ONLY in")
    say("  WHICH names are traded.  So  dSharpe(CONVICTION vs H-blend)  =  BRAKE CHANNEL "
        "[PRORATA - H-blend, pure churn reduction]  +  CONVICTION CHANNEL [CONVICTION - PRORATA, "
        "the priority ordering].")
    say("    " + f"{'panel':>6} {'base':>5} {'cap':>6} {'turn':>7} {'BRAKE dShrp':>12} "
                 f"{'CONV dShrp':>11} {'TOTAL':>8} | {'BRAKE dCAGR':>12} {'CONV dCAGR':>11} "
                 f"{'TOTAL':>8}")
    dec = []
    hh = MT[(MT.cost == COST_HEAD) & (MT.bracketed)]
    for pn in ("U56", "B136", "SMALL"):
        for base_H in (1, I_H):
            for cp in CAPS[:-1]:
                a = hh[(hh.panel == pn) & (hh.H == base_H) & (hh.cap == cp) &
                       (hh.mech == "CONVICTION")]
                b = hh[(hh.panel == pn) & (hh.H == base_H) & (hh.cap == cp) &
                       (hh.mech == "PRORATA")]
                if not len(a) or not len(b):
                    continue
                a, b = a.iloc[0], b.iloc[0]
                brake_s, conv_s = b["dShrp"], a["Shrp_cap"] - b["Shrp_cap"]
                brake_c, conv_c = b["dCAGR"], a["dCAGR"] - b["dCAGR"]
                dec.append(dict(panel=pn, base=base_H, cap=cp, brake_S=brake_s, conv_S=conv_s,
                                brake_C=brake_c, conv_C=conv_c))
                say("    " + f"{pn:>6} {base_H:>5} {cp:>6.2f} {a['turn']:>7.3f} "
                             f"{brake_s:>+12.4f} {conv_s:>+11.4f} {a['dShrp']:>+8.4f} | "
                             f"{brake_c:>+12.3f} {conv_c:>+11.3f} {a['dCAGR']:>+8.3f}")
    D = pd.DataFrame(dec)
    say(f"    MEAN over all {len(D)} (panel, base, cap) cells:  BRAKE channel "
        f"{D['brake_S'].mean():+.4f} Sharpe / {D['brake_C'].mean():+.3f} pp CAGR;  CONVICTION "
        f"channel {D['conv_S'].mean():+.4f} Sharpe / {D['conv_C'].mean():+.3f} pp CAGR.")
    say(f"    BRAKE channel positive at {int((D['brake_S']>0).sum())} of {len(D)} cells "
        f"(Sharpe), {int((D['brake_C']>0).sum())} of {len(D)} (CAGR);  CONVICTION channel at "
        f"{int((D['conv_S']>0).sum())} of {len(D)} (Sharpe), {int((D['conv_C']>0).sum())} of "
        f"{len(D)} (CAGR).")
    D.to_csv(f"{OUT}.decomposition.csv", index=False)

    n4a = int(ALL[ALL.cost == COST_HEAD]["keep4a"].sum())
    n4b = int(ALL[ALL.cost == COST_HEAD]["keep4b"].sum())
    n4bb = int((ALL[ALL.cost == COST_HEAD]["keep4b"] & ALL[ALL.cost == COST_HEAD]["keep4b_oos"]).sum())
    ncells = int((ALL.cost == COST_HEAD).sum())
    say(f"\n  BOTH KEEP PATHS at {COST_HEAD:.0f} bps over all {ncells} cells (H-curve + cap grid): "
        f"4a {n4a}, 4b FULL {n4b}, 4b FULL *and* OOS {n4bb}.")
    capcells = G[G.cost == COST_HEAD]
    say(f"    of which CAP cells only: 4a {int(capcells['keep4a'].sum())} of {len(capcells)}, "
        f"4b FULL {int(capcells['keep4b'].sum())}, 4b FULL *and* OOS "
        f"{int((capcells['keep4b'] & capcells['keep4b_oos']).sum())}.")
    if len(capcells[capcells.keep4b & capcells.keep4b_oos]):
        say("    CAP cells clearing 4b FULL and OOS:")
        for _, r in capcells[capcells.keep4b & capcells.keep4b_oos].iterrows():
            say(f"      {r.panel:<6} H={int(r.H):<4} cap={r.cap:.2f} {r.mech:<11} "
                f"CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.4f} MaxDD {r.MaxDD:.2%} | OOS "
                f"{r.oCAGR:.2%}/{r.oSharpe:.4f}/{r.oMaxDD:.2%} | turnover {r.turn:.3f}/yr")
    say(f"\n  BINDING 4b LEG across failing CAP cells: "
        f"{capcells[~capcells.keep4b]['legs'].value_counts().to_dict()}")

    say("\n  RULE 8 WALK-FORWARD (dials fit on warm-up..2016-12-31, 2017-2026 read ONCE):")
    for _, r in WF.iterrows():
        say(f"    {r.panel:<6} {r.family:<11} base={r.base} {r.mech:<11} picks "
            f"{r['pick']!s:<6} (IS Sharpe {r.IS:.4f}) -> OOS {r.oCAGR:.2%}/{r.oSharpe:.4f}/"
            f"{r.oMaxDD:.2%}  vs do-nothing {r.nothing_oSharpe:.4f} (d {r.d_vs_nothing:+.4f}) "
            f"vs SPY {r.spy_oSharpe:.4f} vs live {r.live_oSharpe:.4f}  4b-OOS "
            f"{'Y' if r.keep4b_oos else '.'}")
    say(f"    MEAN d(OOS Sharpe) vs doing nothing, CAP arms only: "
        f"{WF[WF.family=='CAP']['d_vs_nothing'].mean():+.4f} "
        f"(beats it {int((WF[WF.family=='CAP']['d_vs_nothing']>0).sum())} of "
        f"{len(WF[WF.family=='CAP'])})")

    say("\n  COST LADDER (dial 2) — matched-turnover mean dSharpe, base H=1, CONVICTION:")
    for cost in COSTS:
        sub = MT[(MT.cost == cost) & (MT.mech == "CONVICTION") & (MT.H == 1) & (MT.bracketed)]
        say(f"    {cost:>5.0f} bps: mean dSharpe {sub['dShrp'].mean():+.4f}, "
            f"wins {int((sub['dShrp']>0).sum())} of {len(sub)}, "
            f"mean dCAGR {sub['dCAGR'].mean():+.3f} pp, mean dMaxDD {sub['dMaxDD'].mean():+.3f} pp")
    say("  COST LADDER — matched-turnover mean dSharpe, base H=126, CONVICTION:")
    for cost in COSTS:
        sub = MT[(MT.cost == cost) & (MT.mech == "CONVICTION") & (MT.H == I_H) & (MT.bracketed)]
        say(f"    {cost:>5.0f} bps: mean dSharpe {sub['dShrp'].mean():+.4f}, "
            f"wins {int((sub['dShrp']>0).sum())} of {len(sub)}, "
            f"mean dCAGR {sub['dCAGR'].mean():+.3f} pp, mean dMaxDD {sub['dMaxDD'].mean():+.3f} pp")

    npass = sum(1 for g in GATES if g["pass_"] and g["target"] != "published, not asserted")
    ntot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"\n  GATES {npass} of {ntot} passed.  Runtime {time.time()-t0:.0f}s.  Offline, "
        f"deterministic (seed {SEED}).")
    say("=" * 140)

    ALL.to_csv(f"{OUT}.grid.csv", index=False)
    MT.to_csv(f"{OUT}.matched.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
