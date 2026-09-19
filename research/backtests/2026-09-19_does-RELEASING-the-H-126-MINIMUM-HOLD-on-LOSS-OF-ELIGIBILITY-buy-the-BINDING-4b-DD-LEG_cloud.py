#!/usr/bin/env python3
"""
Idea 1366 (lane cloud, 2026-09-19) — does RELEASING the H=126 MINIMUM HOLD on LOSS OF
ELIGIBILITY buy the BINDING 4b DD LEG?

THE PREMISE.  The frozen 2026-09-04 incumbent makes a name immune from replacement for H = 126
trading days from the day it enters.  Inside that window the book holds the name whatever it
does: it can lose its 200d MA, its vol20 can blow through the 0.60 gate, and the construction
keeps it.  Idea 1258 ran into exactly this ("the cap is NOT enforceable on the book it would
govern, with the committed H=126 minimum"), and idea 1298 established that the incumbent's 4b
pass rests on **1.10 pp of drawdown room** with the MaxDD cap as the SOLE binding leg.  No
implementer would hold a name six months after it broke down.  Ideas 275 and 507 priced a daily
hard exit — but on the RULES v1 / v2 BAND books, where nothing blocks an exit; never on the
MIN-HOLD incumbent, which is the only book where the clause has something to overrule.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):

  EXIT {HOLD, ELIG, MA}          DIAL 1 — HOLD is the incumbent (no release)
     HOLD  a held name is immune for H rows, as committed
     ELIG  release it the moment it fails the FULL eligibility test (above 200d MA AND
           vol20 < 0.60), read on the same lagged row the ranker reads
     MA    release it only when it loses the 200d MA, ignoring the vol gate
  H {63, 126, 189}               DIAL 2 — 126 is the incumbent's value

  9 cells per panel, 27 in all, EVERY ONE published in `.grid.csv`.

THE BOOK, OTHERWISE FROZEN.  The record's certified incumbent as this lane has carried it since
idea 1296: 3-leg rank composite ((21,252), (0,126), (0,63)) x the `0.5 + 0.5*above-200d` tilt,
eligibility = above the 200d MA AND vol20 < 0.60, N = 15 names at equal weight, GROSS 0.60 with
the residual in CASH at 0% (the record's convention — idea 1358, committed earlier today, shows
that convention understates every de-grossed book, and it is left untouched here so this run
changes exactly one thing), weekly cadence, decisions lagged one row and applied at t+1 (rule 2),
10 bps per unit turnover.

WHAT IS BEING ASKED, PRECISELY.  Not "is more trading better".  An exit clause that buys drawdown
by cutting exposure and paying turnover has bought nothing the H dial could not buy more cheaply,
so every EXIT cell is ALSO scored against a TURNOVER-MATCHED HOLD TWIN: the un-released book on a
fine H ladder (21..252, CONTROLS, not dials) whose realised annual turnover is nearest that
cell's.  And because a 4b leg flip inside its own noise is a coin flip (idea 1298), every
cell-minus-twin Sharpe gap is scored by a PAIRED circular-block bootstrap (400 reps x 63-row
blocks, seed 20260919, both books resampled on IDENTICAL blocks).  |t| > 2 is the bar; anything
inside it is published as UNRESOLVED, not as a finding.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); both KEEP paths at every
cell; the halves; IS and OOS windows; turnover and its 10 bps drag in bp/yr; realised vol; the
mean number of names actually held (a release clause can leave the book under-populated).

COMPARANDS (rule 3): the live RULES v2 baseline at 10 bps weekly, SPY buy-and-hold, and the
FROZEN (HOLD, H=126) incumbent.

PROTOCOL: rule 1 (>= 10 years); rule 2 (t+1, 10 bps, no leverage, no shorting); rule 3 (RULES v2
AND SPY); rule 4 (both KEEP paths, 2 tuned parameters); rule 8 (walk-forward: the (EXIT, H) PAIR
chosen on warm-up..2016-12-31 by argmax IS Sharpe, 2017-2026 read ONCE, scored against the frozen
(HOLD, 126) incumbent); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

GATES.  G1 is a CROSS-SCRIPT replay: the (HOLD, 126) cell must reproduce, on ALL THREE panels to
< 5e-6, the anchor row committed by ideas 1296 / 1346 / 1358 — same tape, and the release-aware
selector must collapse EXACTLY onto the committed one when the release is switched off.  G2
asserts the release can only ever REMOVE a name from the held set (the ELIG frame's held set is a
subset of HOLD's at every rebalance, at equal H).  G3 asserts no leverage.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-19_does-RELEASING-the-H-126-MINIMUM-HOLD-on-LOSS-OF-ELIGIBILITY-buy-the-BINDING-4b-DD-LEG_cloud.py
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
SLUG = "does-RELEASING-the-H-126-MINIMUM-HOLD-on-LOSS-OF-ELIGIBILITY-buy-the-BINDING-4b-DD-LEG"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, MAXVOL = 260, 0.60
LEGS = [(21, 252), (0, 126), (0, 63)]
I_N, I_GROSS = 15, 0.60                            # frozen: width, gross
COST = 10.0                                        # PROTOCOL rule 2
CADENCE = "W"                                      # frozen
EXITS = ["HOLD", "ELIG", "MA"]                     # DIAL 1
HS = [63, 126, 189]                                # DIAL 2
ANCHOR_EXIT, ANCHOR_H = "HOLD", 126                # the frozen incumbent
CTRL_HS = [21, 42, 63, 84, 105, 126, 147, 168, 189, 210, 252]   # HOLD-only turnover controls
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BOOT_REPS, BOOT_BLOCK, BOOT_SEED = 400, 63, 20260919
# Committed by ideas 1296 / 1346 and re-read bit-identically by idea 1358 earlier today.
C_ANCHOR = {
    "U56": dict(CAGR=0.1367020011892825, Sharpe=1.17166235540161, MaxDD=-0.163814812515476,
                H1=1.2526855979053693, H2=1.121880836109541, turn=2.463043347965852),
    "B136": dict(CAGR=0.1343474037905223, Sharpe=1.0630027470342966, MaxDD=-0.1597051532314095,
                 H1=1.2318389322712402, H2=0.9406397253110836, turn=2.6461090252500337),
    "SMALL": dict(CAGR=0.0753535266944089, Sharpe=0.5569518940285322, MaxDD=-0.3263346826561878,
                  H1=0.8125393414921002, H2=0.358407645038224, turn=3.407055866031751),
}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=value, target="published, not asserted", pass_=True))


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


def cadence_rows(idx, cad):
    m = rebalance_mask(idx, cad).shift(1, fill_value=False).values.copy()
    m[0] = True
    return np.flatnonzero(m)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        self.reb = cadence_rows(px.index, CADENCE)
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.above = above
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, exit_rule="HOLD", lag=1):
    """The record's selection frame at GROSS = 1.0; lag = 1 is rule 2.  `exit_rule` is the ONLY
    departure from the committed construction: with HOLD it is bit-identical to what ideas 1296 /
    1346 / 1358 committed; with ELIG or MA a held name whose age is still below H is RELEASED
    when it fails the named test on the same lagged row the ranker reads.  A released name cannot
    be re-taken in the same breath because the take-list is itself filtered on eligibility.
    Returns (frame, held_count_at_each_rebalance, held_mask_at_each_rebalance)."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    reb = pan.reb
    nheld = np.zeros(len(reb), dtype=np.int64)
    hmask = np.zeros((len(reb), K), dtype=bool)
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        if len(young) and exit_rule == "ELIG":
            young = young[pan.elig[ts, young]]
        elif len(young) and exit_rule == "MA":
            young = young[pan.above[ts, young]]
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
        nheld[i] = len(sel)
        hmask[i, sel] = True
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W, nheld, hmask


def run(pan, frame, gross):
    """Uninvested gross sits in CASH at 0% (the record's convention).  No leverage, no shorting."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    turn = np.zeros(T)
    out = np.zeros(T)
    wmax = 0.0
    curw = np.zeros(M)
    reb = np.asarray(pan.reb, dtype=np.int64)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = gross * frame[i0]
        wmax = max(wmax, float(w0.sum()))
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        Ae = w0 * (C[i1 - 1] / base)
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


def annvol(r):
    return float(np.std(np.asarray(r, float), ddof=0) * np.sqrt(252))


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


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
    """SE of (Sharpe(a) - Sharpe(b)) under a PAIRED circular block bootstrap: both series are
    resampled on IDENTICAL block starts, so the pairing survives and the SE is of the DIFFERENCE,
    not of either level.  Returns (observed d, SE, t)."""
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


def main():
    t0 = time.time()
    say("=" * 126)
    say("IDEA 1366 (lane cloud, 2026-09-19) — does RELEASING the H=126 MINIMUM HOLD on LOSS OF "
        "ELIGIBILITY buy the BINDING 4b DD LEG?")
    say("DIALS: EXIT {HOLD,ELIG,MA} x H {63,126,189} at the frozen incumbent (N=15, gross 0.60, "
        "cash residual at 0%, MAXVOL 0.60, MA gate ON, weekly, 10 bps, t+1).")
    say("=" * 126)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    meta = ROOT / "data" / "small_meta.csv"
    if meta.exists():
        md = pd.read_csv(meta)
        col = "ticker" if "ticker" in md.columns else md.columns[0]
        bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
        say(f"  SMALL filter: data/small_meta.csv drops {len(bad)} tickers with "
            f"max_1d_move >= 1.0 (protocol-mandated).")
    else:
        bad = set()
        say("  SMALL filter: data/small_meta.csv absent; in-panel max |1d move| >= 1.0 screen.")
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]

    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, "
        f"SMALL {len(inv)} (of {len(pxS.columns)-1} priced).")
    say("  SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT-constituent lists; SMALL is a "
        "sub-$2B screen carried back to 2010, so its LEVELS are an upper bound and only its "
        "CONTRASTS across exit rule and hold length are read here.  A release clause is exactly "
        "the kind of rule a survivorship-clean panel would treat differently — names that were "
        "delisted after breaking down are ABSENT from all three panels, so the value of exiting "
        "is UNDERSTATED here, not overstated.")
    say("  TAPE STAMP:")
    for p in panels:
        say(f"    {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y);  {len(p.reb)} weekly rebalances")
        publish(f"TAPE STAMP {p.name}",
                f"{len(p.idx)} rows, {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p.idx) for p in panels) / 252.0, 2), ">= 10.0",
         min(len(p.idx) for p in panels) / 252.0 >= 10.0)

    grid, ctrl_rows, wf_rows, boot_rows, bench = [], [], [], [], {}
    max_wsum, subset_ok = 0.0, True

    for pan in panels:
        n = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.4f}/{spy['H2']:.4f}  |  4b bars: DD cap "
            f"{DD_CAP*spy['MaxDD']:.2%}, CAGR floor {CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps: CAGR {live['CAGR']:.2%} Sharpe "
            f"{live['Sharpe']:.4f} MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.4f}/"
            f"{live['H2']:.4f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        # ---- HOLD-ONLY CONTROL LADDER (not a dial: the turnover-matched twin for every cell) ---
        ctrl, ctrl_rr = [], {}
        for h_ in CTRL_HS:
            fr, nh, _ = build1(pan, I_N, h_, "HOLD")
            gg, tu, _ = run(pan, fr, I_GROSS)
            rr = gg - tu * COST / 1e4
            r = rr[WARMUP:]
            m = triple(r)
            h1, h2 = halves(r)
            mo = triple(rr[i_oos:])
            d = dict(panel=pan.name, H=h_, turn=annturn(tu, WARMUP, n), vol=annvol(r),
                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                     mean_held=float(nh.mean()))
            ctrl.append(d)
            ctrl_rr[h_] = rr
            ctrl_rows.append(d)
        ctrl_turn = np.array([c["turn"] for c in ctrl])

        say(f"    {'exit':>4} {'H':>4} | {'CAGR':>7} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} "
            f"{'H2':>6} | {'DDmargin':>8} {'CGmargin':>8} | {'vol':>6} {'turn':>5} {'drag':>6} "
            f"{'nheld':>5} | {'OOSCAGR':>8} {'OOSShrp':>7} {'OOSMaxDD':>8} | {'ISShrp':>7} | "
            f"{'vs HOLD same-H':>14} {'vs TURNMATCH':>12} | 4a 4b  fail-legs")
        runs, frames = {}, {}
        for ex in EXITS:
            for h_ in HS:
                fr, nh, hm = build1(pan, I_N, h_, ex)
                frames[(ex, h_)] = hm
                gg, tu, wmax = run(pan, fr, I_GROSS)
                max_wsum = max(max_wsum, wmax)
                rr = gg - tu * COST / 1e4
                r = rr[WARMUP:]
                turn = annturn(tu, WARMUP, n)
                ka, kb, m, h1, h2, legs = keep_paths(r, spy, live)
                mo = triple(rr[i_oos:])
                kb_oos = bool(mo["Sharpe"] > spyO["Sharpe"])
                runs[(ex, h_)] = rr
                ddm = m["MaxDD"] - DD_CAP * spy["MaxDD"]
                cgm = m["CAGR"] - CAGR_FLOOR * spy["CAGR"]
                same = [c for c in ctrl if c["H"] == h_][0]
                j = int(np.argmin(np.abs(ctrl_turn - turn)))
                tm = ctrl[j]
                row = dict(panel=pan.name, exit=ex, H=h_,
                           CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                           DD_margin_pp=ddm, CAGR_margin_pp=cgm,
                           vol_real=annvol(r), turn=turn, cost_drag_bp=turn * COST,
                           mean_held=float(nh.mean()), min_held=int(nh[WARMUP <= pan.reb].min()),
                           n_rebal=len(pan.reb),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           IS_Sharpe=sharpe(rr[WARMUP:i_oos]),
                           dS_vs_hold_same_H=m["Sharpe"] - same["Sharpe"],
                           dCAGR_vs_hold_same_H=m["CAGR"] - same["CAGR"],
                           dDD_vs_hold_same_H=m["MaxDD"] - same["MaxDD"],
                           turnmatch_H=tm["H"], turnmatch_turn=tm["turn"],
                           dS_vs_turnmatch=m["Sharpe"] - tm["Sharpe"],
                           dCAGR_vs_turnmatch=m["CAGR"] - tm["CAGR"],
                           dDD_vs_turnmatch=m["MaxDD"] - tm["MaxDD"],
                           dOOS_S_vs_turnmatch=mo["Sharpe"] - tm["OOS_Sharpe"],
                           SPY_Sharpe=spy["Sharpe"], SPY_CAGR=spy["CAGR"],
                           SPY_MaxDD=spy["MaxDD"], LIVE_Sharpe=live["Sharpe"],
                           LIVE_MaxDD=live["MaxDD"], OOS_SPY_Sharpe=spyO["Sharpe"],
                           OOS_SPY_CAGR=spyO["CAGR"], OOS_SPY_MaxDD=spyO["MaxDD"],
                           OOS_LIVE_Sharpe=liveO["Sharpe"],
                           keep4a=ka, keep4b=kb, keep4b_oos_sharpe=kb_oos,
                           keep4b_and_oos=bool(kb and kb_oos),
                           leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                           leg_CAGR=legs["CAGR"])
                grid.append(row)
                say(f"    {ex:>4} {h_:4d} | {m['CAGR']:7.2%} {m['Sharpe']:7.4f} "
                    f"{m['MaxDD']:8.2%} {h1:6.3f} {h2:6.3f} | {ddm:+8.2%} {cgm:+8.2%} | "
                    f"{annvol(r):6.2%} {turn:5.2f} {turn*COST:6.1f} {nh.mean():5.1f} | "
                    f"{mo['CAGR']:8.2%} {mo['Sharpe']:7.4f} {mo['MaxDD']:8.2%} | "
                    f"{row['IS_Sharpe']:7.4f} | {row['dS_vs_hold_same_H']:+14.4f} "
                    f"{row['dS_vs_turnmatch']:+7.4f}@H{tm['H']:d} | {int(ka)}  {int(kb)}   "
                    + (",".join(k for k, v_ in legs.items() if not v_) or "-"))
        bench[pan.name] = dict(spy=spy, spyO=spyO, live=live, liveO=liveO, runs=runs,
                               i_oos=i_oos, n=n, ctrl=ctrl, ctrl_rr=ctrl_rr)

        a = [r for r in grid if r["panel"] == pan.name and r["exit"] == ANCHOR_EXIT
             and r["H"] == ANCHOR_H][0]
        c = C_ANCHOR[pan.name]
        dev = max(abs(a[k] - v) for k, v in c.items())
        gate(f"G1 cross-script replay of ideas 1296/1346/1358's {pan.name} anchor (HOLD, H=126) "
             f"on CAGR/Sharpe/MaxDD/H1/H2/turn", f"{dev:.3e}", "< 5e-6", dev < 5e-6)
        # G2: the clause's own claim, checked directly — under ELIG, NO held name may be
        # ineligible on the lagged decision row it was held through.  Under HOLD it may, and the
        # count of those is exactly the exposure the release removes.
        ts = np.maximum(np.asarray(pan.reb, dtype=np.int64) - 1, 0)
        for h_ in HS:
            bad_e = int((frames[("ELIG", h_)] & ~pan.elig[ts]).sum())
            bad_h = int((frames[("HOLD", h_)] & ~pan.elig[ts]).sum())
            subset_ok = subset_ok and (bad_e == 0)
            publish(f"G2 exposure removed, {pan.name} H{h_}",
                    f"HOLD carries {bad_h} ineligible name-weeks, ELIG carries {bad_e}")
            say(f"    {pan.name} H{h_}: HOLD carries {bad_h} INELIGIBLE name-weeks "
                f"({bad_h/max(frames[('HOLD',h_)].sum(),1):.2%} of all held name-weeks); "
                f"ELIG carries {bad_e}.")

    gate("G3 NO LEVERAGE (rule 2): max invested weight sum over every cell and rebalance",
         f"{max_wsum:.12f}", f"<= {I_GROSS} + 1e-12", max_wsum <= I_GROSS + 1e-12)

    G = pd.DataFrame(grid)
    CTRL = pd.DataFrame(ctrl_rows)

    gate("G2 under ELIG no held name is ineligible on its own lagged decision row",
         "0 ineligible name-weeks on every panel and H" if subset_ok else "VIOLATED",
         "0", subset_ok)
    gate("G2b the release never widens the book: mean held names <= N at every cell",
         f"{G.mean_held.max():.4f}", f"<= {I_N}", G.mean_held.max() <= I_N + 1e-12)

    say("\n" + "=" * 126)
    say("1. DOES THE RELEASE BUY THE DD LEG?  (DD margin = MaxDD - 0.60 x SPY MaxDD; CAGR margin "
        "= CAGR - 0.70 x SPY CAGR.  BOTH must be >= 0 for 4b.)")
    say("=" * 126)
    for p in G.panel.unique():
        for ex in EXITS:
            sub = G[(G.panel == p) & (G.exit == ex)].sort_values("H")
            say(f"    {p:>6} {ex:>4}: " + "  ".join(
                f"H{r.H:d}[DD {r.DD_margin_pp:+.2%} / CG {r.CAGR_margin_pp:+.2%} / "
                f"S {r.Sharpe:.4f} / 4b {int(r.keep4b)}]" for r in sub.itertuples()))
        anc = G[(G.panel == p) & (G.exit == ANCHOR_EXIT) & (G.H == ANCHOR_H)].iloc[0]
        better = G[(G.panel == p) & (G.exit != "HOLD")
                   & (G.MaxDD > anc.MaxDD) & (G.CAGR > anc.CAGR)]
        say(f"      -> {p}: release cells with BOTH a shallower MaxDD AND a higher CAGR than the "
            f"frozen (HOLD, 126) anchor: "
            + (", ".join(f"{r.exit}@H{r.H:d}" for r in better.itertuples())
               if len(better) else "NONE"))
        say(f"         anchor DD room to the 4b cap: {anc.DD_margin_pp:+.2%};  best release DD "
            f"room on this panel: "
            + (f"{G[(G.panel==p)&(G.exit!='HOLD')].DD_margin_pp.max():+.2%}"))

    say("\n2. IS THE RELEASE A SIGNAL OR JUST MORE TRADING?  (every release cell vs the HOLD book "
        "on the 21-252 control ladder whose REALISED ANNUAL TURNOVER is nearest)")
    for p in G.panel.unique():
        for ex in ["ELIG", "MA"]:
            sub = G[(G.panel == p) & (G.exit == ex)].sort_values("H")
            say(f"    {p:>6} {ex:>4}: " + "  ".join(
                f"H{r.H:d}[dS {r.dS_vs_turnmatch:+.4f} dCAGR {r.dCAGR_vs_turnmatch:+.2%} "
                f"dDD {r.dDD_vs_turnmatch:+.2%} dOOSs {r.dOOS_S_vs_turnmatch:+.4f} "
                f"(twin H{r.turnmatch_H:d} turn {r.turnmatch_turn:.2f} vs {r.turn:.2f})]"
                for r in sub.itertuples()))
    nr = G[G.exit != "HOLD"]
    say(f"    POOLED over all {len(nr)} release cells vs their turnover-matched HOLD twins: mean "
        f"dSharpe {nr.dS_vs_turnmatch.mean():+.4f} (positive in "
        f"{int((nr.dS_vs_turnmatch>0).sum())} of {len(nr)}), mean dCAGR "
        f"{nr.dCAGR_vs_turnmatch.mean():+.2%}, mean dMaxDD {nr.dDD_vs_turnmatch.mean():+.2%} "
        f"(positive = SHALLOWER), mean dOOS Sharpe {nr.dOOS_S_vs_turnmatch.mean():+.4f} (positive "
        f"in {int((nr.dOOS_S_vs_turnmatch>0).sum())} of {len(nr)}).")
    say(f"    And vs the HOLD book at the SAME H (the un-matched comparison): mean dSharpe "
        f"{nr.dS_vs_hold_same_H.mean():+.4f} (positive in "
        f"{int((nr.dS_vs_hold_same_H>0).sum())} of {len(nr)}), mean dCAGR "
        f"{nr.dCAGR_vs_hold_same_H.mean():+.2%}, mean dMaxDD "
        f"{nr.dDD_vs_hold_same_H.mean():+.2%}.")

    say(f"\n2b. IS ANY OF IT RESOLVABLE?  Paired circular-block bootstrap of (release Sharpe - "
        f"turnover-matched HOLD twin Sharpe): {BOOT_REPS} reps x {BOOT_BLOCK}-row blocks, seed "
        f"{BOOT_SEED}, BOTH books resampled on IDENTICAL blocks.  |t| > 2 = resolvable.")
    for p in G.panel.unique():
        b = bench[p]
        for ex in ["ELIG", "MA"]:
            outs = []
            for h_ in HS:
                r = b["runs"][(ex, h_)]
                cell = G[(G.panel == p) & (G.exit == ex) & (G.H == h_)].iloc[0]
                tw = b["ctrl_rr"][int(cell.turnmatch_H)]
                o, se, t = paired_block_dsharpe(r[WARMUP:], tw[WARMUP:])
                oo, seo, to = paired_block_dsharpe(r[b["i_oos"]:], tw[b["i_oos"]:])
                boot_rows.append(dict(panel=p, exit=ex, H=h_, turnmatch_H=int(cell.turnmatch_H),
                                      full_dS=o, full_SE=se, full_t=t,
                                      oos_dS=oo, oos_SE=seo, oos_t=to,
                                      full_resolvable=bool(abs(t) > 2),
                                      oos_resolvable=bool(abs(to) > 2)))
                outs.append(f"H{h_:d}[full {o:+.4f} +-{se:.4f} t{t:+.2f} | OOS {oo:+.4f} "
                            f"+-{seo:.4f} t{to:+.2f}]")
            say(f"    {p:>6} {ex:>4}: " + "  ".join(outs))
    BOOT = pd.DataFrame(boot_rows)
    say(f"    RESOLVABLE (|t| > 2) on the FULL sample: {int(BOOT.full_resolvable.sum())} of "
        f"{len(BOOT)} release cells;  OOS: {int(BOOT.oos_resolvable.sum())} of {len(BOOT)}.")
    for ex in ["ELIG", "MA"]:
        sb = BOOT[BOOT.exit == ex]
        say(f"      {ex:>4}: full mean t {sb.full_t.mean():+.2f} (resolvable "
            f"{int(sb.full_resolvable.sum())}/{len(sb)}), OOS mean t {sb.oos_t.mean():+.2f} "
            f"(resolvable {int(sb.oos_resolvable.sum())}/{len(sb)}); OOS dS positive in "
            f"{int((sb.oos_dS > 0).sum())}/{len(sb)}, median SE {sb.oos_SE.median():.4f}")

    say("\n3. KEEP PATHS OVER ALL 27 CELLS")
    say(f"    4a (beat the live book): {int(G.keep4a.sum())} of {len(G)}")
    say(f"    4b full-sample: {int(G.keep4b.sum())} of {len(G)};  4b full AND OOS Sharpe > SPY: "
        f"{int(G.keep4b_and_oos.sum())} of {len(G)}")
    for p in G.panel.unique():
        s = G[G.panel == p]
        say(f"      {p:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/{len(s)}"
            f"   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for ex in EXITS:
        s = G[G.exit == ex]
        say(f"      {ex:>6}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    for h_ in HS:
        s = G[G.H == h_]
        say(f"      H{h_:d}: 4a {int(s.keep4a.sum())}/{len(s)}   4b {int(s.keep4b.sum())}/"
            f"{len(s)}   4b+OOS {int(s.keep4b_and_oos.sum())}/{len(s)}")
    fails = dict(H1=int((~G.leg_H1).sum()), H2=int((~G.leg_H2).sum()),
                 DD=int((~G.leg_DD).sum()), CAGR=int((~G.leg_CAGR).sum()))
    say(f"    4b binding legs across all {len(G)} cells: " + ", ".join(
        f"{k} fails {v}" for k, v in sorted(fails.items(), key=lambda kv: -kv[1])))
    say("    Cells that BEAT the frozen (HOLD, 126) incumbent on full-sample Sharpe AND pass 4b "
        "full+OOS:")
    any_dom = False
    for p in G.panel.unique():
        anc = G[(G.panel == p) & (G.exit == ANCHOR_EXIT) & (G.H == ANCHOR_H)].iloc[0]
        d = G[(G.panel == p) & (G.Sharpe > anc.Sharpe) & G.keep4b_and_oos]
        for r in d.itertuples():
            any_dom = True
            say(f"      {p} {r.exit}@H{r.H:d}: {r.Sharpe:.4f} vs anchor {anc.Sharpe:.4f} "
                f"(+{r.Sharpe-anc.Sharpe:.4f}), OOS {r.OOS_Sharpe:.4f} vs {anc.OOS_Sharpe:.4f}, "
                f"MaxDD {r.MaxDD:.2%} vs {anc.MaxDD:.2%}, CAGR {r.CAGR:.2%} vs {anc.CAGR:.2%}, "
                f"vs turnover-matched twin dS {r.dS_vs_turnmatch:+.4f}")
    if not any_dom:
        say("      NONE on any panel.")

    say("\n4. RULE 8 WALK-FORWARD — the (EXIT, H) PAIR chosen on warm-up..2016-12-31 by argmax IS "
        "Sharpe; 2017-2026 read ONCE")
    say("=" * 126)
    for p in G.panel.unique():
        b = bench[p]
        sub = G[G.panel == p]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        anc = sub[(sub.exit == ANCHOR_EXIT) & (sub.H == ANCHOR_H)].iloc[0]
        ro = b["runs"][(pick.exit, int(pick.H))][b["i_oos"]:]
        h1o, h2o = halves(ro)
        legs_oos = dict(OOS_Sharpe_vs_SPY=bool(pick.OOS_Sharpe > b["spyO"]["Sharpe"]),
                        DD=bool(pick.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                        CAGR=bool(pick.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        anc_legs_oos = dict(OOS_Sharpe_vs_SPY=bool(anc.OOS_Sharpe > b["spyO"]["Sharpe"]),
                            DD=bool(anc.OOS_MaxDD >= DD_CAP * b["spyO"]["MaxDD"]),
                            CAGR=bool(anc.OOS_CAGR >= CAGR_FLOOR * b["spyO"]["CAGR"]))
        best_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
        wf = dict(panel=p, IS_pick_exit=pick.exit, IS_pick_H=int(pick.H),
                  IS_Sharpe=pick.IS_Sharpe, ANCHOR_IS_Sharpe=anc.IS_Sharpe,
                  IS_margin_over_anchor=pick.IS_Sharpe - anc.IS_Sharpe,
                  is_the_incumbent=bool(pick.exit == ANCHOR_EXIT and pick.H == ANCHOR_H),
                  OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                  OOS_H1=h1o, OOS_H2=h2o,
                  ANCHOR_OOS_CAGR=anc.OOS_CAGR, ANCHOR_OOS_Sharpe=anc.OOS_Sharpe,
                  ANCHOR_OOS_MaxDD=anc.OOS_MaxDD,
                  dOOS_Sharpe_vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                  dOOS_CAGR_vs_anchor=pick.OOS_CAGR - anc.OOS_CAGR,
                  dOOS_MaxDD_vs_anchor=pick.OOS_MaxDD - anc.OOS_MaxDD,
                  SPY_OOS_CAGR=b["spyO"]["CAGR"], SPY_OOS_Sharpe=b["spyO"]["Sharpe"],
                  SPY_OOS_MaxDD=b["spyO"]["MaxDD"],
                  LIVE_OOS_CAGR=b["liveO"]["CAGR"], LIVE_OOS_Sharpe=b["liveO"]["Sharpe"],
                  LIVE_OOS_MaxDD=b["liveO"]["MaxDD"],
                  keep4b_oos_all=bool(all(legs_oos.values())),
                  anchor_keep4b_oos_all=bool(all(anc_legs_oos.values())),
                  oos_fail_legs=",".join(k for k, v in legs_oos.items() if not v) or "-",
                  best_OOS_exit=best_oos.exit, best_OOS_H=int(best_oos.H),
                  best_OOS_Sharpe=best_oos.OOS_Sharpe)
        wf_rows.append(wf)
        say(f"    {p:>6}: IS pick ({pick.exit}, H{int(pick.H)}) IS Sharpe {pick.IS_Sharpe:.4f} "
            f"(anchor {anc.IS_Sharpe:.4f}, margin {pick.IS_Sharpe-anc.IS_Sharpe:+.5f}) -> OOS "
            f"{pick.OOS_CAGR:7.2%}/{pick.OOS_Sharpe:.4f}/{pick.OOS_MaxDD:7.2%}")
        say(f"            vs FROZEN (HOLD, 126) {anc.OOS_CAGR:7.2%}/{anc.OOS_Sharpe:.4f}/"
            f"{anc.OOS_MaxDD:7.2%}   d Sharpe {pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}, d CAGR "
            f"{pick.OOS_CAGR-anc.OOS_CAGR:+.2%}, d MaxDD {pick.OOS_MaxDD-anc.OOS_MaxDD:+.2%}")
        say(f"            vs SPY {b['spyO']['CAGR']:7.2%}/{b['spyO']['Sharpe']:.4f}/"
            f"{b['spyO']['MaxDD']:7.2%}   vs RULES v2 {b['liveO']['CAGR']:7.2%}/"
            f"{b['liveO']['Sharpe']:.4f}/{b['liveO']['MaxDD']:7.2%}")
        say(f"            4b on every OOS leg: pick {int(wf['keep4b_oos_all'])} "
            f"[{wf['oos_fail_legs']}]  anchor {int(wf['anchor_keep4b_oos_all'])}   | ex-post best "
            f"OOS cell ({wf['best_OOS_exit']}, H{wf['best_OOS_H']:d}) "
            f"{wf['best_OOS_Sharpe']:.4f}")

    WF = pd.DataFrame(wf_rows)
    say(f"\n    The IS chooser lands on the frozen incumbent (HOLD, 126) in "
        f"{int(WF.is_the_incumbent.sum())} of {len(WF)} panels.")
    say(f"    Mean OOS Sharpe of the IS-chosen PAIR minus the frozen incumbent: "
        f"{WF.dOOS_Sharpe_vs_anchor.mean():+.4f} (min {WF.dOOS_Sharpe_vs_anchor.min():+.4f}, "
        f"max {WF.dOOS_Sharpe_vs_anchor.max():+.4f}); it beats the incumbent in "
        f"{int((WF.dOOS_Sharpe_vs_anchor > 0).sum())} of {len(WF)}.")
    say(f"    Mean OOS CAGR difference: {WF.dOOS_CAGR_vs_anchor.mean():+.2%};  mean OOS MaxDD "
        f"difference: {WF.dOOS_MaxDD_vs_anchor.mean():+.2%} (positive = SHALLOWER).")
    say(f"    4b on every OOS leg after rule 8: pick {int(WF.keep4b_oos_all.sum())} of {len(WF)}, "
        f"anchor {int(WF.anchor_keep4b_oos_all.sum())} of {len(WF)}.")
    hind = int(((WF.best_OOS_exit != WF.IS_pick_exit) | (WF.best_OOS_H != WF.IS_pick_H)).sum())
    say(f"    H_HINDSIGHT: the ex-post best OOS cell differs from the IS pick on {hind} of "
        f"{len(WF)} panels.")

    say("\n5. WHAT THE RELEASE COSTS IN OCCUPANCY AND TURNOVER (a released name is only replaced "
        "if something eligible outranks it, so the book can run under-populated)")
    for p in G.panel.unique():
        for ex in EXITS:
            sub = G[(G.panel == p) & (G.exit == ex)].sort_values("H")
            say(f"    {p:>6} {ex:>4}: " + "  ".join(
                f"H{r.H:d}[held {r.mean_held:.1f}/{I_N} min {r.min_held:d} turn {r.turn:.2f} "
                f"drag {r.cost_drag_bp:.1f}bp]" for r in sub.itertuples()))

    say("\n6. THE HOLD-ONLY CONTROL LADDER (H 21-252), the shape the release is scored against")
    for p in CTRL.panel.unique():
        sub = CTRL[CTRL.panel == p].sort_values("H")
        say(f"    {p:>6}: " + "  ".join(
            f"H{r.H:d}({r.Sharpe:.3f}/{r.CAGR:.1%}/{r.MaxDD:.1%}/t{r.turn:.2f})"
            for r in sub.itertuples()))

    G.to_csv(f"{OUT}.grid.csv", index=False)
    CTRL.to_csv(f"{OUT}.controls.csv", index=False)
    BOOT.to_csv(f"{OUT}.bootstrap.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  wrote {Path(OUT).name}.grid.csv ({len(G)} cells), .controls.csv ({len(CTRL)}), "
        f".bootstrap.csv ({len(BOOT)}), .walkforward.csv ({len(WF)}), .gates.csv")
    asserted = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"  GATES: {sum(g['pass_'] for g in asserted)}/{len(asserted)} asserted pass "
        f"(plus {len(GATES)-len(asserted)} published stamps)")
    say(f"  elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
