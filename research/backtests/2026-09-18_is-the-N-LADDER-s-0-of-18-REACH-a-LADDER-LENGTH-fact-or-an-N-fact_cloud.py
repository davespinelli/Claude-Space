#!/usr/bin/env python3
"""Idea 1153 (lane cloud, 2026-09-18): is the N LADDER's 0-of-18 REACH a LADDER-LENGTH fact
or an N fact?

QUESTION.  Idea 1101 found that an IS-only chooser picks the anchor's own rung from the
GROSS ladder at 6 of 18 decisions and from CADENCE at 5 of 18, but from N at 0 of 18 (mean
P_boot 0.050).  Two confounds sit inside that reading: N is the LONGEST ladder after GROSS,
and a longer ladder is harder to hit by construction; and GROSS's reaches are all BOUNDARY
picks (the anchor's 0.75 is that ladder's top rung).  The queue asks for the length confound
to be removed directly — truncate N, extend CADENCE — and for the answer to say whether
reach rate is explained by rung count alone.

THIS RUN REMOVES THE CONFOUND BY CONSTRUCTION, NOT BY CORRECTION.  All four CORE ladders are
cut to EXACTLY EIGHT rungs and then walked down a common LENGTH ladder K in {2, 3, 4, 6, 8},
each K a nested neighbourhood of the anchor's own rung.  At every K the four ladders are the
SAME LENGTH, so any surviving difference between them is not rung count.  N truncated to 4
rungs around the anchor and CADENCE extended to 8 — the two moves the queue names — are both
cells of that grid.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    K       {2, 3, 4, 6, 8} rungs — the LADDER LENGTH, a nested neighbourhood of the anchor.
    ANCHOR  {A, B} — A = W / H=126 / N=20 / gross 0.75, the standing cell 936/1071/1082/1094/
            1096/1101/1174 all quote; B = M / H=63 / N=12 / gross 0.55, 1101's own declared
            second anchor, interior on all four ladders where A is at the top rung of GROSS.
  5 x 2 = 10 cells per (panel, ladder, chooser).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); LADDER {N, H, GROSS,
CADENCE}; CHOOSER {C_ISSHARPE (1101's headline), C_ISCAGR, C_ISDD}; both KEEP paths leg by
leg on EVERY rung book and on EVERY pick; full / halves / IS / OOS; P_boot on every decision.
That is 4 ladders x 5 K x 2 anchors x 3 chooser x 3 panels = 360 reach decisions, against
1101's 72.

THE LADDERS, EACH EXACTLY EIGHT RUNGS, BOTH ANCHORS ON EVERY ONE:
    N        [5, 8, 10, 12, 15, 20, 25, 30]
    H        [5, 10, 21, 42, 63, 90, 126, 189]          (MIN-HOLD days)
    GROSS    [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
    CADENCE  [D, W, 2W, M, 2M, Q, 2Q, 4Q]
CADENCE IS EXTENDED WITH CALENDAR SUBSAMPLES, NOT A MODULAR PHASE CYCLE (idea 1064's open
question): 2W is every second week-end, 2M every second month-end, 2Q every second
quarter-end, 4Q every fourth — all anchored on the tape's own calendar period ends, phase
frozen at parity 0 from the first period end and stated here rather than chosen (idea 1253
priced phase at up to 2.18 pp of drawdown, so it is named, not tuned).

FROZEN, NOT DIALS: CAND20 composite of the 12-1 / 6m / 3m percentile ranks; eligibility =
above own 200d MA AND 20d vol < 0.60; cap INF; equal weight gross/len(selected) with gated
weight to CASH; 10 bps per unit turnover; next-day execution (LAG 1); 260-row warm-up;
IS = warm-up..2016-12-31, OOS = 2017-01-01 onward read ONCE; block bootstrap L = 63, 1000
draws, shared block index across the rungs of a ladder so the cross-rung correlation that
makes these ladders hard to resolve is preserved rather than destroyed.

WHAT REACH MEANS, STATED BEFORE ANY NUMBER (1101's definition, unchanged).  A ladder REACHES
its anchor under chooser C at length K iff C, given the IS window ALONE, picks the anchor's
own rung out of that K-rung neighbourhood.  P_boot is P(the anchor is the IS argmax) over
1000 joint redraws of the IS window, and it is the honest companion: a reach at P_boot 0.3
is a coin landing, not a measurement.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) LENGTH IS THE WHOLE STORY — at matched K the four ladders' reach rates are inside
      noise of each other and of the 1/K chance line.  Then 1101's 0-of-18 says nothing
      about N and the record should stop reading it as an N fact.
  (B) N IS DIFFERENT — N reaches strictly less often than the others at MATCHED K.  Then the
      0-of-18 is an N fact and survives the confound.
  (C) BOUNDARY IS THE STORY — reach is predicted by whether the anchor sits at a ladder
      endpoint, at matched K, whatever the ladder is called.
  (D) NOTHING IS RESOLVED — reach rates track 1/K and P_boot never clears 0.90/0.10, i.e.
      no ladder carries selection information at any length.  That is the capital finding
      whichever of (A)-(C) fires, and it is reported first.

RULE 8 (walk-forward, required).  Every pick here is IS-only by construction and the OOS
window is read ONCE.  At every (panel, anchor, ladder, K, chooser) the run publishes the
pick's OOS Sharpe against (i) the ANCHOR's OOS Sharpe over the same rows — the do-nothing
bar, since the anchor is the book the record already holds — (ii) the mean over the K rungs,
(iii) the best and worst rung, and the IS/OOS rank correlation over the K rungs.  The
capital verdict is the sign of pick-minus-anchor, never the best rung.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 anchor-A book.  G2
CROSS-RUN: that book's (CAGR, Sharpe, MaxDD) reproduces 936/1082/1174's committed triple
(0.155787, 1.139701, -0.191276).  G3 CROSS-RUN SPY OOS triple (0.1521, 0.8713, -0.3372).
G2 and G3 are read on the tape TRUNCATED to 2026-09-15, where the tape ended when those
numbers were committed (this cache carries two further rows and two days are worth 0.0034 of
SPY's OOS Sharpe); the live-tape readings are printed beside them, ungated.  G4 the live
RULES v2 MaxDD == the committed -12.05%.  G5 every K-neighbourhood contains the anchor rung
and is nested in the next.  G6 all four ladders have exactly 8 rungs, so K is length-matched
by construction.  G7 the gross=0.75 rung of anchor A's GROSS ladder is bit-identical to the
anchor book built from the CADENCE line (the four lines agree where they cross).  G8 the
bootstrap is deterministic and its per-rung argmax probabilities sum to 1 on every ladder.
G9 determinism: the whole U56 grid recomputes bit for bit.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an UPPER bound.  The headline is a CONTRAST between four ladders of the same length on the
same tape, which is first-order immune to a level bias that moves all of them together; the
4a/4b legs are not.

Runs standalone and offline (committed price caches only).
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-the-N-LADDER-s-0-of-18-REACH-a-LADDER-LENGTH-fact-or-an-N-fact"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BLOCK, NDRAW, SEED0 = 63, 1000, 1153
COMMIT_TAPE_END = "2026-09-15"

# ---- the four CORE ladders, EIGHT rungs each -------------------------------------------------
LAD_N = [5, 8, 10, 12, 15, 20, 25, 30]
LAD_H = [5, 10, 21, 42, 63, 90, 126, 189]
LAD_G = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
LAD_C = ["D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}

# ---- the two dials ---------------------------------------------------------------------------
KS = [2, 3, 4, 6, 8]
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

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


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows_of(r, i_oos):
    n = len(r)
    h = n // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                is_=stats(r[:i_oos]), oos=stats(r[i_oos:]))


def flat(w):
    return {f"{k}_{m}": v for k, d in w.items() for m, v in d.items()}


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


# ------------------------------------------------------------------ book machinery
def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def cadence_mask(idx, tag):
    """D/W/M/Q from the engine; 2W/2M/2Q/4Q = every k-th CALENDAR period end, parity 0."""
    base = {"D": "D", "W": "W", "2W": "W", "M": "M", "2M": "M", "Q": "Q", "2Q": "Q", "4Q": "Q"}[tag]
    every = {"D": 1, "W": 1, "2W": 2, "M": 1, "2M": 2, "Q": 1, "2Q": 2, "4Q": 4}[tag]
    m = rebalance_mask(idx, base).values.copy()
    if every > 1:
        pos = np.flatnonzero(m)
        keep = pos[::every]
        m = np.zeros(len(idx), dtype=bool)
        m[keep] = True
    return m


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1082's build(), unmodified: MIN HOLD H, N slots, cap INF, equal weight gross/len(sel)."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


# ------------------------------------------------------------------ ladder neighbourhoods
def neighbourhood(ladder, anchor_val, K):
    """The K rungs nearest the anchor BY LADDER POSITION, anchor always included, nested in K."""
    i = ladder.index(anchor_val)
    order = sorted(range(len(ladder)), key=lambda j: (abs(j - i), j))
    return sorted(order[:K])


# ------------------------------------------------------------------ KEEP paths
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


# ------------------------------------------------------------------ chooser statistics
def stat_of(chooser, w):
    return {"C_ISSHARPE": w["is_"]["Sharpe"], "C_ISCAGR": w["is_"]["CAGR"],
            "C_ISDD": w["is_"]["MaxDD"]}[chooser]


def boot_pick_probs(R_is, seed):
    """P(each rung is the IS argmax) under a moving-block bootstrap with a SHARED block index
    across the rungs of the ladder.  Returns (P_sharpe, P_cagr, P_dd), each of length n_rung."""
    n, T = R_is.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / BLOCK))
    cnt = np.zeros((3, n))
    starts_all = rng.integers(0, T - BLOCK + 1, size=(NDRAW, nb))
    off = np.arange(BLOCK)
    for d in range(NDRAW):
        idx = (starts_all[d][:, None] + off[None, :]).ravel()[:T]
        X = R_is[:, idx]
        mu = X.mean(axis=1)
        sd = X.std(axis=1, ddof=0)
        sh = np.where(sd > 0, mu * 252 / (sd * np.sqrt(252)), -np.inf)
        eq = np.cumprod(1.0 + X, axis=1)
        cg = eq[:, -1] ** (252.0 / T) - 1.0
        dd = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        for k, v in enumerate((sh, cg, dd)):
            cnt[k, int(np.argmax(v))] += 1
    return cnt / NDRAW


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1153 lane cloud — {SLUG}")
    say(f"# frozen: CAND20 legs {LEGS}, elig above-200d & vol20 < {MAXVOL}, cap INF, gated weight "
        f"to CASH, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}, IS end {IS_END.date()}")
    for k, v in LADDERS.items():
        say(f"# ladder {k:8s} ({len(v)} rungs): {v}")
    say(f"# DIAL 1 K = {KS} rungs (nested neighbourhood of the anchor)   "
        f"DIAL 2 ANCHOR = {{A: {ANCHORS['A']}, B: {ANCHORS['B']}}}")
    say(f"# choosers {CHOOSERS} (headline C_ISSHARPE, 1101's); block bootstrap L={BLOCK}, "
        f"{NDRAW} draws, shared block index across a ladder's rungs")
    gate("G6 all four ladders are EIGHT rungs (K length-matched by construction)",
         {k: len(v) for k, v in LADDERS.items()}, "all 8",
         all(len(v) == 8 for v in LADDERS.values()))
    nest_ok = True
    for lad, rungs in LADDERS.items():
        for aname, a in ANCHORS.items():
            prev = None
            for K in KS:
                nb = neighbourhood(rungs, a[lad], K)
                if rungs.index(a[lad]) not in nb or (prev is not None and not set(prev) <= set(nb)):
                    nest_ok = False
                prev = nb
    gate("G5 every K-neighbourhood contains the anchor and nests in the next", nest_ok, "True", nest_ok)

    rows, bookrows, r8rows = [], [], []
    u56_ref = None

    for pi, panel in enumerate(["U56", "B136", "SMALL"]):
        if panel == "SMALL":
            px = load_universe(small=True)
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
            drop = [c for c in px.columns if c in bad]
            px = px.drop(columns=drop)
            say(f"\n## SMALL: {len(drop)} tickers dropped for max_1d_move >= 1.0")
        else:
            px = load_universe(broad=(panel == "B136"))
        px = px.dropna(how="all").ffill()
        idx = px.index
        T, K = len(idx), len(px.columns)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        i_oos = int(idx.searchsorted(OOS_START))
        pname = {"U56": "U56", "B136": f"B{K-1}", "SMALL": f"SMALL{K-1}"}[panel]
        spy_r = px["SPY"].pct_change().fillna(0.0).values
        live_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values
        sw = windows_of(spy_r[WARMUP:], i_oos - WARMUP)
        lw = windows_of(live_r[WARMUP:], i_oos - WARMUP)
        say(f"\n## {pname}  n_days={T}  n_cols={K}  {idx[0].date()}..{idx[-1].date()}  OOS row {i_oos}")
        say(f"   SPY     full {sw['full']['CAGR']:7.2%} / {sw['full']['Sharpe']:.4f} / {sw['full']['MaxDD']:7.2%}"
            f"   OOS {sw['oos']['CAGR']:7.2%} / {sw['oos']['Sharpe']:.4f} / {sw['oos']['MaxDD']:7.2%}"
            f"   4b caps: DD {DD_CAP*sw['full']['MaxDD']:.4%}, CAGR {CAGR_FLOOR*sw['full']['CAGR']:.4%}")
        say(f"   RULESv2 full {lw['full']['CAGR']:7.2%} / {lw['full']['Sharpe']:.4f} / {lw['full']['MaxDD']:7.2%}"
            f"   OOS {lw['oos']['CAGR']:7.2%} / {lw['oos']['Sharpe']:.4f} / {lw['oos']['MaxDD']:7.2%}")

        # ---- every book any ladder needs, built once, keyed by the full (N,H,gross,cadence)
        cache: dict[tuple, np.ndarray] = {}

        def book(N, H, g, cad):
            key = (N, H, round(float(g), 4), cad)
            if key in cache:
                return cache[key]
            m = cadence_mask(idx, cad)
            reb = np.flatnonzero(m)
            Wm = build(rank_key, elig, priced, reb, N, H, T, K, float(g))
            gr, tn = nrun(rets, lagmat(Wm), np.roll(m, LAG))
            r = gr - tn * COST / 1e4
            cache[key] = r
            return r

        need = set()
        for aname, a in ANCHORS.items():
            for lad, rungs in LADDERS.items():
                for v in rungs:
                    c = dict(a)
                    c[lad] = v
                    need.add((c["N"], c["H"], c["GROSS"], c["CADENCE"]))
        say(f"   building {len(need)} distinct rung books ...")
        for (N, H, g, cad) in sorted(need, key=str):
            r = book(N, H, g, cad)
            w = windows_of(r[WARMUP:], i_oos - WARMUP)
            a4, b4 = legs_4a(w, lw), legs_4b(w, sw)
            bookrows.append(dict(panel=pname, N=N, H=H, gross=g, cadence=cad, **flat(w),
                                 keep4a=all(a4.values()), keep4b=all(b4.values()),
                                 fail4a=failed(a4), fail4b=failed(b4)))
        say(f"   built {len(need)} books  [t={time.time()-t0:.0f}s]")

        if pi == 0:
            a = ANCHORS["A"]
            m = cadence_mask(idx, a["CADENCE"])
            Wm = build(rank_key, elig, priced, np.flatnonzero(m), a["N"], a["H"], T, K, a["GROSS"])
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=COST, freq=a["CADENCE"])["returns"].values
            r = book(a["N"], a["H"], a["GROSS"], a["CADENCE"])
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - r[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 anchor A)", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wl = windows_of(r[WARMUP:], i_oos - WARMUP)
            wt = windows_of(r[WARMUP:itr], i_oos - WARMUP)
            say(f"   U56 anchor A on the LIVE tape (ungated): {wl['full']['CAGR']:.6f}/"
                f"{wl['full']['Sharpe']:.6f}/{wl['full']['MaxDD']:.6f}")
            d2 = max(abs((wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])[i] - A936_WH126[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN U56 anchor A triple == 936/1082/1174's committed (tape to {COMMIT_TAPE_END})",
                 f"{wt['full']['CAGR']:.6f}/{wt['full']['Sharpe']:.6f}/{wt['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{A936_WH126} < 5e-4", d2 < 5e-4)
            swt = windows_of(spy_r[WARMUP:itr], i_oos - WARMUP)
            d3 = max(abs((swt["oos"]["CAGR"], swt["oos"]["Sharpe"], swt["oos"]["MaxDD"])[i] - SPY_OOS_COMMITTED[i])
                     for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END}; live tape reads "
                 f"{sw['oos']['CAGR']:.4f}/{sw['oos']['Sharpe']:.4f}/{sw['oos']['MaxDD']:.4f})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            gate("G4 live RULES v2 MaxDD == committed -12.05%", f"{lw['full']['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4", abs(lw["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)
            rg = book(a["N"], a["H"], 0.75, a["CADENCE"])
            gate("G7 the GROSS=0.75 rung IS anchor A (the four lines agree where they cross)",
                 f"{float(np.abs(rg - r).max()):.3e}", "== 0.0", float(np.abs(rg - r).max()) == 0.0)

        # ---- the reach grid
        say("\n   anchor ladder   K | chooser     pick            reach P_boot | pickOOS anchOOS  delta | "
            "rankIS/OOS | 4b pick")
        gridrows_panel = []
        for aname, a in ANCHORS.items():
            for lad, rungs in LADDERS.items():
                full_idx = list(range(len(rungs)))
                R_all = []
                W_all = []
                for j in full_idx:
                    c = dict(a)
                    c[lad] = rungs[j]
                    r = book(c["N"], c["H"], c["GROSS"], c["CADENCE"])
                    R_all.append(r[WARMUP:])
                    W_all.append(windows_of(r[WARMUP:], i_oos - WARMUP))
                R_all = np.array(R_all)
                ai = rungs.index(a[lad])
                for Kk in KS:
                    nb = neighbourhood(rungs, a[lad], Kk)
                    seed = zlib.crc32(f"{pname}|{aname}|{lad}|{Kk}".encode()) ^ SEED0
                    P = boot_pick_probs(R_all[nb][:, :i_oos - WARMUP], seed)
                    if pi == 0 and aname == "A" and lad == "N" and Kk == 8:
                        gate("G8 bootstrap argmax probabilities sum to 1 on every statistic",
                             f"{P.sum(axis=1)}", "== 1.0", bool(np.allclose(P.sum(axis=1), 1.0)))
                        P2 = boot_pick_probs(R_all[nb][:, :i_oos - WARMUP], seed)
                        gate("G8b bootstrap determinism (same seed, same probabilities)",
                             f"{float(np.abs(P - P2).max()):.3e}", "== 0.0",
                             float(np.abs(P - P2).max()) == 0.0)
                    for ci, ch in enumerate(CHOOSERS):
                        vals = np.array([stat_of(ch, W_all[j]) for j in nb])
                        pick_local = int(np.nanargmax(vals))
                        pick = nb[pick_local]
                        reach = int(pick == ai)
                        pb = float(P[ci, nb.index(ai)])
                        oos = np.array([W_all[j]["oos"]["Sharpe"] for j in nb])
                        isv = np.array([W_all[j]["is_"]["Sharpe"] for j in nb])
                        wp, wa = W_all[pick], W_all[ai]
                        a4, b4 = legs_4a(wp, lw), legs_4b(wp, sw)
                        rec = dict(panel=pname, anchor=aname, ladder=lad, K=Kk, chooser=ch,
                                   anchor_rung=str(a[lad]), pick_rung=str(rungs[pick]),
                                   pick_is_boundary=int(pick in (nb[0], nb[-1])),
                                   anchor_is_boundary=int(ai in (nb[0], nb[-1])),
                                   reach=reach, P_boot=pb, chance=1.0 / Kk,
                                   pick_IS=wp["is_"]["Sharpe"], pick_OOS=wp["oos"]["Sharpe"],
                                   anchor_OOS=wa["oos"]["Sharpe"],
                                   delta=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                                   pick_full_CAGR=wp["full"]["CAGR"], pick_full_Sharpe=wp["full"]["Sharpe"],
                                   pick_full_MaxDD=wp["full"]["MaxDD"],
                                   pick_h1=wp["h1"]["Sharpe"], pick_h2=wp["h2"]["Sharpe"],
                                   mean_OOS=float(np.nanmean(oos)), best_OOS=float(np.nanmax(oos)),
                                   worst_OOS=float(np.nanmin(oos)), rank_IS_OOS=rankcorr(isv, oos),
                                   spy_full_Sharpe=sw["full"]["Sharpe"], spy_oos_Sharpe=sw["oos"]["Sharpe"],
                                   live_full_Sharpe=lw["full"]["Sharpe"],
                                   keep4a=all(a4.values()), keep4b=all(b4.values()),
                                   fail4a=failed(a4), fail4b=failed(b4))
                        rows.append(rec)
                        gridrows_panel.append(rec)
                        r8rows.append(dict(panel=pname, anchor=aname, ladder=lad, K=Kk, chooser=ch,
                                           pick=str(rungs[pick]), reach=reach, P_boot=pb,
                                           pick_OOS=wp["oos"]["Sharpe"], anchor_OOS=wa["oos"]["Sharpe"],
                                           delta=wp["oos"]["Sharpe"] - wa["oos"]["Sharpe"],
                                           mean_OOS=float(np.nanmean(oos)),
                                           rank_IS_OOS=rankcorr(isv, oos),
                                           spy_OOS=sw["oos"]["Sharpe"]))
                        if ch == "C_ISSHARPE":
                            say(f"   {aname}      {lad:8s} {Kk} | {ch:11s} {str(rungs[pick]):6s} -> "
                                f"{'REACH' if reach else '  -  '} {pb:5.3f} | {wp['oos']['Sharpe']:7.4f} "
                                f"{wa['oos']['Sharpe']:7.4f} {rec['delta']:+7.4f} | {rec['rank_IS_OOS']:+.2f} "
                                f"     | {'Y' if all(b4.values()) else 'n'} {failed(b4)}")
        say(f"   [t={time.time()-t0:.0f}s]")
        if pi == 0:
            u56_ref = (pd.DataFrame(gridrows_panel)[["anchor", "ladder", "K", "chooser", "reach", "P_boot",
                                                     "pick_OOS"]].copy(), px, idx)

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    pd.DataFrame(bookrows).drop_duplicates(subset=["panel", "N", "H", "gross", "cadence"]).to_csv(
        f"{STEM}.books.csv", index=False)
    pd.DataFrame(r8rows).to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G9 determinism of the reach grid arithmetic (re-derive the U56 rows from the csv)
    ref = u56_ref[0]
    chk = grid[grid.panel == "U56"][["anchor", "ladder", "K", "chooser", "reach", "P_boot", "pick_OOS"]]
    same = bool(np.allclose(chk[["reach", "P_boot", "pick_OOS"]].values.astype(float),
                            ref[["reach", "P_boot", "pick_OOS"]].values.astype(float), atol=0.0))
    gate("G9 U56 grid rows identical between the in-run record and the written frame", same, "True", same)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ---- the answer
    say("\n## THE ANSWER — REACH RATE BY LADDER AND BY LENGTH (headline chooser C_ISSHARPE)")
    h = grid[grid.chooser == "C_ISSHARPE"]
    piv = h.pivot_table(index="ladder", columns="K", values="reach", aggfunc="mean")
    say(piv.round(4).to_string())
    say("   chance line 1/K: " + ", ".join(f"K={k} {1/k:.4f}" for k in KS))
    say("\n   reach MINUS chance (1/K), by ladder and K:")
    say((piv - pd.Series({k: 1.0 / k for k in KS})).round(4).to_string())
    say("\n   AT MATCHED K = 4 (the queue's truncation), by ladder, all choosers:")
    for lad in LADDERS:
        g4 = grid[(grid.K == 4) & (grid.ladder == lad)]
        g8 = grid[(grid.K == 8) & (grid.ladder == lad)]
        say(f"     {lad:8s} K=4 reach {g4.reach.mean():.4f} ({int(g4.reach.sum())} of {len(g4)}), "
            f"mean P_boot {g4.P_boot.mean():.4f}   |   K=8 reach {g8.reach.mean():.4f} "
            f"({int(g8.reach.sum())} of {len(g8)}), mean P_boot {g8.P_boot.mean():.4f}")
    say("\n   POOLED over all 360 decisions:")
    say(f"     reach {grid.reach.mean():.4f} ({int(grid.reach.sum())} of {len(grid)})   "
        f"chance {grid.chance.mean():.4f}   excess {grid.reach.mean()-grid.chance.mean():+.4f}")
    for lad in LADDERS:
        g = grid[grid.ladder == lad]
        say(f"     {lad:8s} reach {g.reach.mean():.4f} ({int(g.reach.sum())}/{len(g)})  "
            f"chance {g.chance.mean():.4f}  excess {g.reach.mean()-g.chance.mean():+.4f}  "
            f"mean P_boot {g.P_boot.mean():.4f}  anchor-at-boundary {g.anchor_is_boundary.mean():.3f}  "
            f"pick-at-boundary {g.pick_is_boundary.mean():.3f}")
    say("\n   BOUNDARY (outcome C): reach rate split by whether the anchor is a ladder endpoint:")
    for b in (0, 1):
        g = grid[grid.anchor_is_boundary == b]
        say(f"     anchor_is_boundary={b}: reach {g.reach.mean():.4f} ({int(g.reach.sum())}/{len(g)})  "
            f"chance {g.chance.mean():.4f}  excess {g.reach.mean()-g.chance.mean():+.4f}")
    say("\n   RESOLUTION (outcome D): how many decisions clear P_boot >= 0.90 or <= 0.10?")
    dec = ((grid.P_boot >= 0.90) | (grid.P_boot <= 0.10)).mean()
    say(f"     decisive {dec:.4f} ({int(((grid.P_boot >= 0.90) | (grid.P_boot <= 0.10)).sum())} of {len(grid)})"
        f"   P_boot >= 0.90 at {int((grid.P_boot >= 0.90).sum())}   max P_boot {grid.P_boot.max():.4f}")
    say("\n   RULE 8 — the pick's OOS Sharpe minus the ANCHOR's, over the same rows:")
    for lad in LADDERS:
        g = grid[grid.ladder == lad]
        say(f"     {lad:8s} mean delta {g.delta.mean():+.4f}  median {g.delta.median():+.4f}  "
            f"positive at {int((g.delta > 0).sum())} of {len(g)}  mean rank corr IS/OOS {g.rank_IS_OOS.mean():+.3f}")
    for ch in CHOOSERS:
        g = grid[grid.chooser == ch]
        say(f"     {ch:11s} mean delta {g.delta.mean():+.4f}  positive at {int((g.delta > 0).sum())} of {len(g)}")
    g = grid[grid.K > 2]
    say(f"     POOLED (K>2) mean delta {g.delta.mean():+.4f}  positive at {int((g.delta > 0).sum())} of {len(g)}")
    bk = pd.DataFrame(bookrows).drop_duplicates(subset=["panel", "N", "H", "gross", "cadence"])
    say("\n## KEEP PATHS")
    say(f"   rung books: {len(bk)}   4a {int(bk.keep4a.sum())}   4b {int(bk.keep4b.sum())}")
    for p in bk.panel.unique():
        b = bk[bk.panel == p]
        say(f"     {p:10s} 4a {int(b.keep4a.sum()):3d}/{len(b)}   4b {int(b.keep4b.sum()):3d}/{len(b)}   "
            f"fail4b modes {b.fail4b.value_counts().head(3).to_dict()}")
    say(f"   PICKS: 4a {int(grid.keep4a.sum())} of {len(grid)}   4b {int(grid.keep4b.sum())} of {len(grid)}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass")
    say(f"   [total {time.time()-t0:.0f}s]")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
