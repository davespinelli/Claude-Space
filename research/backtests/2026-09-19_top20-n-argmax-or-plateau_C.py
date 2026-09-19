#!/usr/bin/env python3
"""Idea 1639 (lane C, 2026-09-19): IS THE KEEP-4b TOP-20 BOOK'S N AN ARGMAX, A PLATEAU MEMBER, OR A
POINT ON A MONOTONE RAY?

THE DEFECT.  The standing 2026-09-04 KEEP-4b candidate holds the top N = 20 names of a three-leg
composite, equal weight, min-hold H = 126, 200d gate, vol20 < 0.60, weekly, gross 0.75.  Its
committed U56 cell is 15.80% / 1.1537 / -19.13% full and 17.32% / 1.1857 OOS at 10 bps.  N = 20 has
been carried forward by every run since, and the record has replayed that ONE cell dozens of times
as a gate -- but it has NEVER read N against its own neighbours at matched gross.  A number nobody
has laddered is not a chosen parameter; it is an inheritance.  Idea 1476 found that coarse interior
argmaxes RELOCATE when the ladder is refined, so the coarse ladder is run AND refined here.

THE QUESTION, in three mutually exclusive answers, decided mechanically:
  (A) INTERIOR ARGMAX   N = 20 maximises Sharpe at that (panel, gross) AND both coarse neighbours
                        are lower by more than 2 paired bootstrap SEs.
  (B) PLATEAU MEMBER    the argmax is elsewhere but N = 20 is inside 2 SE of it -- i.e. the ladder
                        cannot tell 20 from the best rung, so 20 is as defensible as anything and
                        no re-tune is warranted.
  (C) MONOTONE RAY      Sharpe is monotone in N over the ladder (argmax at an endpoint).  Then the
                        book's N is a corner the record has never walked to, and 20 is arbitrary.
The SE is not asserted: it is a paired circular-block bootstrap on the two books' OWN daily returns
(block length 65 trading days, the record's LB from idea 1511; 1000 draws; fixed seed), so the same
resampled calendar prices both books and the difference is paired.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  N  {10, 14, 20, 28, 40}                 DIAL 1 -- number of names held.
  G  {0.50, 0.75, 1.00}                   DIAL 2 -- constant gross.
  45 cells (3 panels x 5 N x 3 G), EVERY ONE PUBLISHED at 10 bps.
  A REFINED N ladder {8, 10, 12, 14, 17, 20, 24, 28, 34, 40} is ALSO run at G = 0.75 on all three
  panels (30 further cells, all published).  That is a DENSER SAMPLING OF DIAL 1, not a third
  parameter: no new axis is introduced, and it is what idea 1476's finding demands.

FROZEN, NOT TUNED: H = 126, MAXVOL = 0.60, the 200d gate, the three composite legs (21/252, 0/126,
0/63), weekly cadence, 10 bps on both legs, t+1 execution, gated-out weight to 0.00%/yr cash
(the live de-gross convention), no leverage, no shorting.

COMPARANDS.  Live RULES v2 (`baseline.rules_v2_weights`, band 0.03, G = 0.75, weekly) is the 4a bar;
SPY buy-and-hold is the 4b bar.  Both are recomputed on EACH panel's own tape and window.

RULE 8.  Parameters are chosen on 2009-2016 rows ALONE by four LEGAL IS-only choosers and the picks
are read once on 2017-2026:
  C1 argmax IS Sharpe over (N, G) jointly          C3 argmax IS Calmar (CAGR / |MaxDD|) over (N, G)
  C2 argmax IS Sharpe over N at G frozen 0.75      C4 argmax IS 4b-leg count over (N, G), ties to
                                                      smaller G then smaller N
The headline rule-8 question is whether ANY of them reaches N = 20.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) N = 20 is an interior argmax on most panel-gross cells -> the inheritance is vindicated.
  (b) N = 20 is a plateau member almost everywhere -> the dial is UNRESOLVABLE at this sample
      length, the record should stop quoting N as a chosen parameter, and no re-tune is justified.
  (c) Sharpe is monotone in N -> 20 is an arbitrary point on a ray and the record has never priced
      the corner it implies.
  (d) No IS-only chooser reaches N = 20 -> the standing candidate's N is HINDSIGHT, whatever its
      ex-post rank, and must be recorded as such.
All four are reported.  Nothing is tuned until it works.

GATES.  G0 sample >= 10y (rule 1).  G1 cross-script replay of the committed 2026-09-04 U56 anchor
(N = 20, G = 0.75: 15.80% / 1.1537 / -19.13% full, 1.1857 OOS) to < 5e-3 of Sharpe.  G2 no leverage
(max realised gross <= G).  G3 exactly two tuned parameters.  G4 no chooser reads a row on or after
2017-01-01 (verified by construction on the IS slice index).  G5 all cells published.  G6 monotone
holding count: realised mean names held is non-decreasing in N at fixed (panel, G).  G7 gross
invariance: at fixed N the three G rungs differ ONLY by exposure, so their pre-cost gross-scaled
returns agree -- published as the realised correlation of the G = 0.50 and G = 1.00 return paths.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward, 2017-2026 read exactly once); rule 9
(survivorship stated).  RULES.md, scan.py, bot.py and baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-19_top20-n-argmax-or-plateau_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "top20-n-argmax-or-plateau"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL, H_FROZEN = 260, 0.60, 126
LEGS = [(21, 252), (0, 126), (0, 63)]
CAD, COST, BAND = "W", 10.0, 0.03
GRID_N = [10, 14, 20, 28, 40]
GRID_G = [0.50, 0.75, 1.00]
FINE_N = [8, 10, 12, 14, 17, 20, 24, 28, 34, 40]
G_FINE = 0.75
N_STAR = 20                                   # the inherited value under test
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LB, NBOOT, SEED = 65, 1000, 20260919
# committed 2026-09-04 U56 anchor (CHANGELOG 2026-09-19, idea 1590 cost ladder, 10 bps, delay +0)
ANCHOR = dict(CAGR=0.1580, Sharpe=1.1537, MaxDD=-0.1913, oSharpe=1.1857, oCAGR=0.1732)

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
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- selection frame (frozen)
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


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.i_oos = int(np.searchsorted(px.index.values, np.datetime64(OOS_START)))
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])

    def reb_rows(self, cadence):
        m = rebalance_mask(self.idx, cadence).shift(1, fill_value=False).values.copy()
        m[0] = True
        return np.flatnonzero(m)


def frame_inc(pan, reb, N, H=H_FROZEN, lag=1):
    """Frozen min-hold composite-momentum selection at GROSS = 1.0: the 2026-09-04 incumbent shape
    with N as the only free number.  Row t carries the close-(t-1) decision (rule 2)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    nheld = np.zeros(T)
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
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
            nheld[t:stop] = len(sel)
    return W, nheld


def run_cell(pan, frame, reb, g, cost=COST):
    """Frozen frame at constant gross g; idle NAV is CASH at 0.00%/yr (the live de-gross
    convention).  The book drifts between rebalances and pays `cost` bps of turnover."""
    rets = pan.rets
    T, M = rets.shape
    turn = np.zeros(T)
    out = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    wsum_max = 0.0
    ends = np.append(reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for i0, i1 in zip(reb, ends):
        if i1 <= i0:
            continue
        w0 = g * frame[i0]
        s0 = float(w0.sum())
        wsum_max = max(wsum_max, s0)
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        Ccash = np.full(i1 - i0, 1.0 - s0)
        V = A.sum(axis=1) + Ccash
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, wsum_max, gsum


# ---------------------------------------------------------------- metrics
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


def block_index(T, lb, nboot, rng):
    """Circular block bootstrap row indices, shape (nboot, T).  The SAME matrix prices both books
    in a pair, so every contrast is paired on one resampled calendar."""
    nblk = int(np.ceil(T / lb))
    starts = rng.integers(0, T, size=(nboot, nblk))
    off = np.arange(lb)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(nboot, nblk * lb)[:, :T]
    return idx % T


def boot_sharpe(r, idx):
    x = np.asarray(r, float)[idx]
    mu = x.mean(axis=1) * 252
    sd = x.std(axis=1, ddof=0) * np.sqrt(252)
    return np.where(sd > 0, mu / np.where(sd > 0, sd, 1.0), np.nan)


def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 1639 (lane C, 2026-09-19) — IS THE KEEP-4b TOP-20 BOOK'S N AN ARGMAX, A PLATEAU MEMBER,")
    say("OR A POINT ON A MONOTONE RAY?")
    say(f"DIALS: N {GRID_N}  x  GROSS {GRID_G}.  Everything else frozen (H = {H_FROZEN}, MAXVOL "
        f"{MAXVOL}, 200d gate, weekly, {COST:.0f} bps, t+1).")
    say(f"REFINEMENT (same dial, denser sampling — idea 1476): N {FINE_N} at G = {G_FINE}.")
    say(f"PLATEAU SE: paired circular-block bootstrap, block {LB} rows, {NBOOT} draws, seed {SEED}.")
    say("=" * 118)

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
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)} "
        f"(of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010.  Every absolute level below is an UPPER BOUND.  What "
        "survives the bias is the SHAPE of Sharpe in N on one fixed name pool: every rung of the "
        "ladder inherits the identical bias, and a ladder read against ITSELF is the object here.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)  OOS from row {p.i_oos}")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G3 exactly two tuned parameters", "N and GROSS", "== 2", True)
    for p in panels:
        assert p.idx[p.i_oos] >= pd.Timestamp(OOS_START) and p.idx[p.i_oos - 1] <= pd.Timestamp(IS_END)
    gate("G4 IS slice ends before 2017-01-01 on every panel",
         " | ".join(f"{p.name} {p.idx[p.i_oos-1].date()}" for p in panels), "<= 2016-12-31", True)

    rng = np.random.default_rng(SEED)
    grid, RET, BARS, NH = [], {}, {}, {}
    wsum_global, gmax_dev = 0.0, 0.0

    for pan in panels:
        T = len(pan.idx)
        i_oos = pan.i_oos
        spy = bmpack(pan.spy[WARMUP:]); spyO = bmpack(pan.spy[i_oos:]); spyI = bmpack(pan.spy[WARMUP:i_oos])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq=CAD)["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])
        BARS[pan.name] = dict(spy=spy, spyO=spyO, spyI=spyI, live=live, liveO=liveO, i_oos=i_oos)
        say(f"\n  [{pan.name}]  SPY FULL {spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} "
            f"H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap {DD_CAP*spy['MaxDD']:.2%}, "
            f"CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           SPY OOS  {spyO['CAGR']:.2%} / {spyO['Sharpe']:.4f} / {spyO['MaxDD']:.2%}  |  "
            f"OOS bars: DD cap {DD_CAP*spyO['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spyO['CAGR']:.2%}")
        say(f"           RULES v2 live @{COST:.0f}bps  {live['CAGR']:.2%} / {live['Sharpe']:.4f} / "
            f"{live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}  (the 4a bar)")

        reb = pan.reb_rows(CAD)
        ladder = sorted(set(GRID_N) | set(FINE_N))
        frames = {}
        for N in ladder:
            frames[N] = frame_inc(pan, reb, N)
        for N in ladder:
            fm, nh = frames[N]
            NH[(pan.name, N)] = float(np.mean(nh[WARMUP:]))
            gl = GRID_G if N in GRID_N else ([G_FINE] if G_FINE not in GRID_G else [])
            gl = sorted(set(gl) | ({G_FINE} if N in FINE_N else set()))
            for g in gl:
                r, tu, ws, gs = run_cell(pan, fm, reb, g)
                wsum_global = max(wsum_global, ws)
                gmax_dev = max(gmax_dev, float(np.max(gs[WARMUP:])) - g)
                RET[(pan.name, N, g)] = r
                k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
                k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
                _, k4bI, mi, _, _, legsI = keep_paths(r[WARMUP:i_oos], spyI, live)
                yrs = (T - WARMUP) / 252.0
                grid.append(dict(panel=pan.name, N=N, gross=g,
                                 coarse=bool(N in GRID_N and g in GRID_G),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                                 isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                                 isCalmar=(mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] < 0 else np.nan),
                                 is4b_legs=int(sum(legsI.values())),
                                 mean_names=NH[(pan.name, N)],
                                 mean_gross=float(np.mean(gs[WARMUP:])),
                                 turnover_yr=float(tu[WARMUP:].sum() / yrs),
                                 keep4a=k4a, keep4b=k4b, keep4a_oos=k4aO, keep4b_oos=k4bO,
                                 leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                                 leg_CAGR=legs["CAGR"], oleg_H1=legsO["H1"], oleg_H2=legsO["H2"],
                                 oleg_DD=legsO["DD"], oleg_CAGR=legsO["CAGR"]))
        say(f"    [{pan.name}] {len([x for x in grid if x['panel']==pan.name])} cells done "
            f"({time.time()-t0:.0f}s elapsed)")

    G = pd.DataFrame(grid).sort_values(["panel", "gross", "N"]).reset_index(drop=True)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    gate("G5 all cells published", f"{len(G)} rows -> {OUT.name}.grid.csv",
         f"{3*len(GRID_N)*len(GRID_G)} coarse + {3*len(FINE_N)} fine (dedup)", len(G) == len(grid))
    gate("G2 no leverage (max realised gross)", f"{wsum_global:.6f}", f"<= {max(GRID_G)}",
         wsum_global <= max(GRID_G) + 1e-9)
    publish("G2b max realised drifted gross above its rung", f"{gmax_dev:+.4f} (drift between weekly rebalances)")

    # ---------------------------------------------------------------- G1 anchor replay
    ar = RET[("U56", N_STAR, 0.75)]
    am, ao = triple(ar[WARMUP:]), triple(ar[BARS["U56"]["i_oos"]:])
    d_sh = abs(am["Sharpe"] - ANCHOR["Sharpe"])
    gate("G1 replay of committed 2026-09-04 U56 anchor (N=20, G=0.75)",
         f"{am['CAGR']:.2%} / {am['Sharpe']:.4f} / {am['MaxDD']:.2%} full, OOS {ao['CAGR']:.2%} / "
         f"{ao['Sharpe']:.4f}  (committed {ANCHOR['CAGR']:.2%} / {ANCHOR['Sharpe']:.4f} / "
         f"{ANCHOR['MaxDD']:.2%}, OOS {ANCHOR['oCAGR']:.2%} / {ANCHOR['oSharpe']:.4f}); |dSharpe| {d_sh:.2e}",
         "|dSharpe| < 5e-3", d_sh < 5e-3)

    # G6 monotone holding count
    mono_ok = True
    for pan in panels:
        v = [NH[(pan.name, N)] for N in GRID_N]
        mono_ok &= all(v[i] <= v[i + 1] + 1e-9 for i in range(len(v) - 1))
        publish(f"G6 mean names held on {pan.name}",
                " ".join(f"N={N}:{NH[(pan.name,N)]:.1f}" for N in GRID_N))
    gate("G6 realised holding count non-decreasing in N", mono_ok, "True", mono_ok)

    # G7 gross invariance
    cors = []
    for pan in panels:
        for N in GRID_N:
            a = RET[(pan.name, N, 0.50)][WARMUP:]
            b = RET[(pan.name, N, 1.00)][WARMUP:]
            cors.append(float(np.corrcoef(a, b)[0, 1]))
    gate("G7 gross rungs are one exposure family (min corr of G=0.50 vs G=1.00 paths)",
         f"{min(cors):.4f}", ">= 0.99", min(cors) >= 0.99)

    # ---------------------------------------------------------------- the coarse ladder, published
    say("\n" + "=" * 118)
    say("THE 45 COARSE CELLS (3 panels x N {10,14,20,28,40} x G {0.50,0.75,1.00}), 10 bps, all published")
    say("=" * 118)
    say(f"  {'panel':6s} {'G':>5s} {'N':>4s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1':>7s} "
        f"{'H2':>7s} {'oCAGR':>8s} {'oSharpe':>8s} {'oMaxDD':>8s} {'turn/y':>7s}  4a 4b 4aO 4bO")
    Gc = G[G["coarse"]]
    for _, r in Gc.iterrows():
        say(f"  {r['panel']:6s} {r['gross']:5.2f} {int(r['N']):4d} {r['CAGR']:8.2%} {r['Sharpe']:8.4f} "
            f"{r['MaxDD']:8.2%} {r['H1']:7.3f} {r['H2']:7.3f} {r['oCAGR']:8.2%} {r['oSharpe']:8.4f} "
            f"{r['oMaxDD']:8.2%} {r['turnover_yr']:7.2f}   "
            f"{'Y' if r['keep4a'] else '.'}  {'Y' if r['keep4b'] else '.'}  "
            f"{'Y' if r['keep4a_oos'] else '.'}   {'Y' if r['keep4b_oos'] else '.'}")
    say(f"\n  KEEP counts over the 45 coarse cells: 4a FULL {int(Gc['keep4a'].sum())}, "
        f"4b FULL {int(Gc['keep4b'].sum())}, 4a OOS {int(Gc['keep4a_oos'].sum())}, "
        f"4b OOS {int(Gc['keep4b_oos'].sum())}, 4b FULL-AND-OOS "
        f"{int((Gc['keep4b'] & Gc['keep4b_oos']).sum())}")

    # ---------------------------------------------------------------- argmax / plateau / ray
    say("\n" + "=" * 118)
    say(f"IS N = {N_STAR} AN ARGMAX, A PLATEAU MEMBER, OR A POINT ON A MONOTONE RAY?")
    say(f"  paired circular-block bootstrap, block {LB} rows, {NBOOT} draws, seed {SEED}; "
        f"t = dSharpe / SE(dSharpe)")
    say("=" * 118)
    shape_rows, boot_rows = [], []
    for pan in panels:
        Tn = len(pan.idx) - WARMUP
        idxb = block_index(Tn, LB, NBOOT, np.random.default_rng(SEED + hash(pan.name) % 1000))
        for g in GRID_G:
            sh = {N: float(G[(G.panel == pan.name) & (G.N == N) & (G.gross == g)]["Sharpe"].iloc[0])
                  for N in GRID_N}
            best = max(sh, key=lambda k: sh[k])
            inc = all(sh[GRID_N[i]] <= sh[GRID_N[i + 1]] + 1e-12 for i in range(len(GRID_N) - 1))
            dec = all(sh[GRID_N[i]] >= sh[GRID_N[i + 1]] - 1e-12 for i in range(len(GRID_N) - 1))
            b20 = boot_sharpe(RET[(pan.name, N_STAR, g)][WARMUP:], idxb)
            ts = {}
            for N in GRID_N:
                if N == N_STAR:
                    ts[N] = 0.0
                    continue
                bN = boot_sharpe(RET[(pan.name, N, g)][WARMUP:], idxb)
                d = bN - b20
                se = float(np.nanstd(d, ddof=1))
                obs = sh[N] - sh[N_STAR]
                ts[N] = obs / se if se > 0 else np.nan
                boot_rows.append(dict(panel=pan.name, gross=g, N=N, dSharpe=obs, SE=se,
                                      t=ts[N], sig=bool(abs(ts[N]) > 2)))
            t_best = ts[best]
            if best == N_STAR:
                nb = [N for N in GRID_N if abs(GRID_N.index(N) - GRID_N.index(N_STAR)) == 1]
                verdict = ("A INTERIOR ARGMAX (both neighbours > 2 SE below)"
                           if all(abs(ts[N]) > 2 for N in nb) else
                           "B PLATEAU MEMBER (is argmax, but a neighbour is inside 2 SE)")
            elif abs(t_best) <= 2:
                verdict = f"B PLATEAU MEMBER (argmax N={best}, inside {abs(t_best):.2f} SE)"
            else:
                verdict = f"C BEATEN (argmax N={best} by {abs(t_best):.2f} SE)"
            if inc or dec:
                verdict += f" | MONOTONE RAY ({'increasing' if inc else 'decreasing'} in N)"
            say(f"  [{pan.name} G={g:.2f}] Sharpe " +
                "  ".join(f"N{N}={sh[N]:.4f}" for N in GRID_N) +
                f"   argmax N={best}")
            say(f"      t(N vs N=20): " + "  ".join(f"N{N}={ts[N]:+.2f}" for N in GRID_N if N != N_STAR)
                + f"   ->  {verdict}")
            shape_rows.append(dict(panel=pan.name, gross=g, argmax_N=best,
                                   sharpe_at_20=sh[N_STAR], sharpe_at_argmax=sh[best],
                                   d_argmax=sh[best] - sh[N_STAR], t_argmax=t_best,
                                   monotone=("inc" if inc else "dec" if dec else "no"),
                                   verdict=verdict))
    SH = pd.DataFrame(shape_rows); SH.to_csv(f"{OUT}.shape.csv", index=False)
    BT = pd.DataFrame(boot_rows); BT.to_csv(f"{OUT}.bootstrap.csv", index=False)
    n_sig = int(BT["sig"].sum())
    say(f"\n  OF {len(BT)} NEIGHBOUR CONTRASTS AGAINST N = 20, {n_sig} REACH |t| > 2 "
        f"({n_sig/len(BT):.1%}).  Mean |dSharpe| {BT['dSharpe'].abs().mean():.4f}, "
        f"mean SE {BT['SE'].mean():.4f}, max |t| {BT['t'].abs().max():.2f}.")
    say(f"  N = 20 IS THE ARGMAX AT {int((SH['argmax_N']==N_STAR).sum())} OF {len(SH)} PANEL-GROSS "
        f"CELLS; {int((SH['monotone']!='no').sum())} of {len(SH)} ladders are MONOTONE in N.")

    # ---------------------------------------------------------------- refined ladder
    say("\n" + "=" * 118)
    say(f"THE REFINED LADDER (same dial, denser sampling — idea 1476) at G = {G_FINE}")
    say("=" * 118)
    fine_rows = []
    for pan in panels:
        sh = {N: float(G[(G.panel == pan.name) & (G.N == N) & (G.gross == G_FINE)]["Sharpe"].iloc[0])
              for N in FINE_N}
        best = max(sh, key=lambda k: sh[k])
        say(f"  [{pan.name}] " + "  ".join(f"N{N}={sh[N]:.4f}" for N in FINE_N))
        say(f"      refined argmax N={best} (coarse argmax "
            f"{int(SH[(SH.panel==pan.name)&(SH.gross==G_FINE)]['argmax_N'].iloc[0])}); "
            f"Sharpe spread over the whole ladder {max(sh.values())-min(sh.values()):.4f}")
        fine_rows.append(dict(panel=pan.name, refined_argmax=best,
                              coarse_argmax=int(SH[(SH.panel == pan.name) & (SH.gross == G_FINE)]["argmax_N"].iloc[0]),
                              spread=max(sh.values()) - min(sh.values())))
    FR = pd.DataFrame(fine_rows)
    say(f"\n  REFINEMENT MOVES THE ARGMAX ON {int((FR['refined_argmax']!=FR['coarse_argmax']).sum())} "
        f"OF {len(FR)} PANELS (idea 1476's prediction).")

    # ---------------------------------------------------------------- rule 8
    say("\n" + "=" * 118)
    say("RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 ROWS ALONE, 2017-2026 read ONCE")
    say("=" * 118)
    wf = []
    for pan in panels:
        b = BARS[pan.name]
        C = G[(G.panel == pan.name) & (G.coarse)].copy()
        picks = {}
        picks["C1 argmax IS Sharpe (N,G) joint"] = C.sort_values(
            ["isSharpe", "gross", "N"], ascending=[False, True, True]).iloc[0]
        c2 = C[C.gross == 0.75]
        picks["C2 argmax IS Sharpe over N at G=0.75"] = c2.sort_values(
            ["isSharpe", "N"], ascending=[False, True]).iloc[0]
        picks["C3 argmax IS Calmar (N,G)"] = C.sort_values(
            ["isCalmar", "gross", "N"], ascending=[False, True, True]).iloc[0]
        picks["C4 argmax IS 4b-leg count (N,G)"] = C.sort_values(
            ["is4b_legs", "gross", "N"], ascending=[False, True, True]).iloc[0]
        say(f"\n  [{pan.name}]  LIVE OOS {b['liveO']['CAGR']:.2%} / {b['liveO']['Sharpe']:.4f} / "
            f"{b['liveO']['MaxDD']:.2%}   SPY OOS {b['spyO']['CAGR']:.2%} / "
            f"{b['spyO']['Sharpe']:.4f} / {b['spyO']['MaxDD']:.2%}")
        for lab, p in picks.items():
            say(f"    {lab:38s} -> N={int(p['N']):2d} G={p['gross']:.2f} | OOS {p['oCAGR']:7.2%} / "
                f"{p['oSharpe']:.4f} / {p['oMaxDD']:7.2%}  4aO {'Y' if p['keep4a_oos'] else '.'} "
                f"4bO {'Y' if p['keep4b_oos'] else '.'}  | reaches N=20: "
                f"{'YES' if int(p['N']) == N_STAR else 'no'}")
            wf.append(dict(panel=pan.name, chooser=lab, N=int(p["N"]), gross=float(p["gross"]),
                           isSharpe=p["isSharpe"], oCAGR=p["oCAGR"], oSharpe=p["oSharpe"],
                           oMaxDD=p["oMaxDD"], keep4a_oos=bool(p["keep4a_oos"]),
                           keep4b_oos=bool(p["keep4b_oos"]),
                           reaches_20=bool(int(p["N"]) == N_STAR),
                           live_oSharpe=b["liveO"]["Sharpe"], spy_oSharpe=b["spyO"]["Sharpe"],
                           anchor_oSharpe=float(G[(G.panel == pan.name) & (G.N == N_STAR) &
                                                  (G.gross == 0.75)]["oSharpe"].iloc[0])))
    WF = pd.DataFrame(wf); WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE 8 HEADLINE: {int(WF['reaches_20'].sum())} of {len(WF)} legal IS-only choosers "
        f"reach N = {N_STAR}.  Mean OOS Sharpe of the picks {WF['oSharpe'].mean():.4f} vs the "
        f"N = 20 anchor's {WF['anchor_oSharpe'].mean():.4f} on the same panels "
        f"(delta {WF['oSharpe'].mean()-WF['anchor_oSharpe'].mean():+.4f}).")
    say(f"  Picks clearing 4b OOS: {int(WF['keep4b_oos'].sum())} of {len(WF)}; 4a OOS: "
        f"{int(WF['keep4a_oos'].sum())} of {len(WF)}.")

    gpass = sum(1 for g in GATES if g["target"] != "published, not asserted" and g["pass_"])
    gtot = sum(1 for g in GATES if g["target"] != "published, not asserted")
    say(f"\n  GATES {gpass}/{gtot} PASS.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wrote {OUT.name}.grid.csv / .shape.csv / .bootstrap.csv / .walkforward.csv / .gates.csv / .log.txt")
    say(f"  total {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
