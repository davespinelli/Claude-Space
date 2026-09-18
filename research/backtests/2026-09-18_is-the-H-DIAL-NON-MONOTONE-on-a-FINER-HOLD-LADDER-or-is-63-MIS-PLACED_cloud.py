#!/usr/bin/env python3
"""Idea 1095 (lane cloud, 2026-09-18): is the H DIAL NON-MONOTONE on a FINER HOLD LADDER, or
is 63 simply MIS-PLACED?

QUESTION.  Idea 1086 read the min-hold dial on THREE rungs {21, 63, 126} and found H=63 is
not between H=21 and H=126 on either panel (U56 Sharpe argmax at N=12/8/12; B136's EDGE(5)
peaking at the MIDDLE hold).  The queue asks whether that non-monotonicity survives
resolution or is a three-point artefact: walk H on the finer ladder at the incumbent n and
say which.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names the ladder itself):
    H  {5, 10, 21, 42, 63, 90, 126, 189} MIN-HOLD days — the queue's own 8-rung ladder,
       which strictly CONTAINS 1086's three rungs, so the 3-rung read is a sub-ladder of
       this one and the two are directly comparable (gate G5).
    N  {5, 20} — 20 is the incumbent slot count (the standing 2026-09-04 KEEP 4b book and
       the cell 936/1071/1082/1174 quote); 5 is 1086's own second family (its B136 EDGE(5)
       reading), carried so the answer is not a one-family artefact.
  8 x 2 = 16 cells per panel, 48 in all, EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); the three IS-only
choosers {C_ISSHARPE, C_ISCAGR, C_ISDD}; both KEEP paths leg by leg at every cell; full /
halves / IS / OOS everywhere.

FROZEN, NOT DIALS: CAND20 composite of the 12-1 / 6m / 3m percentile ranks; eligibility =
above own 200d MA AND 20d vol < 0.60; cap INF; equal weight gross/len(selected) with gated
weight to CASH; gross 0.75; WEEKLY cadence; 10 bps per unit turnover; next-day execution
(LAG 1); 260-row warm-up; IS = warm-up..2016-12-31, OOS = 2017-01-01 onward read ONCE;
moving-block bootstrap L = 63, 1000 draws, block index SHARED across the rungs of a ladder
so the cross-rung correlation that makes this dial hard to resolve is preserved, not
destroyed by independent resampling.

WHAT IS MEASURED, STATED BEFORE ANY NUMBER
  SHAPE   the sign of each of the 7 adjacent-rung Sharpe steps; MONOTONE iff all 7 agree;
          the argmax rung and whether it is INTERIOR; and 1086's own statistic BETWEEN(63)
          = is S(63) inside [min, max] of S(21), S(126), read on this run's tape.
  RESOLUTION  each step's paired bootstrap SE (same draws for both rungs), DECISIVE iff
          |step| >= 2 SE; P(rung is the full-sample Sharpe argmax) over 1000 draws.
  CAPITAL 4a against live RULES v2 and 4b against SPY at every cell, leg by leg.
  RULE 8  each chooser picks H from the IS window ALONE over all 8 rungs; the OOS window is
          read ONCE; the pick is scored against (i) the ANCHOR H=126 over the same rows (the
          do-nothing bar, the book the record already holds), (ii) the 8-rung mean, (iii) the
          best and the worst rung, (iv) SPY; plus the IS/OOS Sharpe rank correlation over the
          8 rungs, which is the direct answer to "does this dial carry selection information".

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) THREE-POINT ARTEFACT — the 8-rung curve is MONOTONE (all 7 steps one sign) at >= 2 of
      3 panels at both N.  Then 1086's "63 is not between 21 and 126" was a gap artefact of
      a ladder that skipped 42..90, and the record should stop citing it.
  (B) SURVIVES AND IS RESOLVED — non-monotone with an INTERIOR argmax whose top-minus-second
      gap clears 2 paired SE on >= 2 panels.  Then H has a real interior optimum and is a
      dial worth turning.
  (C) NON-MONOTONE BUT UNRESOLVED — the point curve wiggles while ~none of the 7 steps clears
      2 SE.  Then the shape is noise at this sample length (1181 found the H argmax is not
      resolvable at ANY attainable rung count, so this is the outcome to beat), and the
      capital reading is: leave H at the incumbent, because nothing on the ladder is
      choosable.
  (D) MIS-PLACED, NOT NON-MONOTONE — 63 IS bracketed by its own fine-ladder neighbours 42 and
      90 while failing 1086's coarse BETWEEN test, i.e. the coarse ladder's own spacing made
      the reading.
  Whichever fires, the rule-8 pick-minus-anchor OOS delta is reported FIRST, because that is
  the only number that touches capital.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 anchor book (N=20, H=126,
W, gross 0.75).  G2 CROSS-RUN: that book's (CAGR, Sharpe, MaxDD) reproduces 936/1082/1174's
committed triple (0.155787, 1.139701, -0.191276).  G3 CROSS-RUN SPY OOS triple (0.1521,
0.8713, -0.3372).  G2/G3 are read on the tape TRUNCATED to 2026-09-15, where the tape ended
when those numbers were committed; the live-tape readings are printed beside them, ungated.
G4 the live RULES v2 MaxDD == the committed -12.05%.  G5 the 8-rung ladder CONTAINS 1086's
{21, 63, 126}.  G6 the bootstrap's per-rung argmax probabilities sum to 1 and are
deterministic under a fixed seed.  G7 MECHANICAL: annual turnover is non-increasing in H at
every (panel, N) — a longer minimum hold cannot trade more.  G8 determinism: the whole U56
grid recomputes bit for bit.  Every gate is published, pass or fail.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point, 2 dials;
rule 5 one idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an UPPER bound: a momentum book on a current-constituent panel never holds the names that
delisted.  The headline is a CONTRAST between rungs of one ladder on one tape, which is
first-order immune to a level bias that moves all rungs together; the 4a/4b legs are not.

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
SLUG = "is-the-H-DIAL-NON-MONOTONE-on-a-FINER-HOLD-LADDER-or-is-63-MIS-PLACED"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
COST = 10.0
GROSS = 0.75
CADENCE = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BLOCK, NDRAW, SEED0 = 63, 1000, 1095
SE_MULT = 2.0
COMMIT_TAPE_END = "2026-09-15"

# ---- the two dials ---------------------------------------------------------------------------
LAD_H = [5, 10, 21, 42, 63, 90, 126, 189]
LAD_N = [5, 20]
COARSE_H = [21, 63, 126]          # 1086's three rungs, a strict sub-ladder (gate G5)
ANCHOR_H = 126                    # the incumbent hold; the do-nothing bar for rule 8
CHOOSERS = ["C_ISSHARPE", "C_ISCAGR", "C_ISDD"]
PANELS = ["U56", "B136", "SMALL"]

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


def dump(df, suffix):
    p = Path(f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    say(f"   wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


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


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(A_H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                A_H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                A_DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(L_H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                L_H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                L_OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                L_DD=abs(bk["full"]["MaxDD"]) <= DD_CAP * abs(spy["full"]["MaxDD"]),
                L_CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


def stat_of(chooser, w):
    return {"C_ISSHARPE": w["is_"]["Sharpe"], "C_ISCAGR": w["is_"]["CAGR"],
            "C_ISDD": w["is_"]["MaxDD"]}[chooser]


# ------------------------------------------------------------------ bootstrap
def boot_draws(R, seed):
    """Moving-block bootstrap with a SHARED block index across the rows of R (the rungs).
    Returns per-draw Sharpe of shape (NDRAW, n_rung)."""
    n, T = R.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / BLOCK))
    starts = rng.integers(0, T - BLOCK + 1, size=(NDRAW, nb))
    off = np.arange(BLOCK)
    out = np.empty((NDRAW, n))
    for d in range(NDRAW):
        idx = (starts[d][:, None] + off[None, :]).ravel()[:T]
        X = R[:, idx]
        mu = X.mean(axis=1)
        sd = X.std(axis=1, ddof=0)
        out[d] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1095 lane cloud — {SLUG}")
    say(f"# DIAL 1 H (MIN-HOLD days) = {LAD_H}   DIAL 2 N = {LAD_N}  (incumbent 20; 1086's second family 5)")
    say(f"# 1086's coarse ladder {COARSE_H} is a strict sub-ladder of dial 1 (gate G5)")
    say(f"# frozen: CAND20 legs {LEGS}, elig above-200d & vol20<{MAXVOL}, cap INF, gross {GROSS}, "
        f"cadence {CADENCE}, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}, IS end {IS_END.date()}")
    say(f"# bootstrap L={BLOCK}, {NDRAW} draws, shared block index across rungs; DECISIVE at {SE_MULT:.0f} SE")
    say("# PRE-DECLARED: (A) three-point artefact / (B) survives and resolved / "
        "(C) non-monotone but unresolved / (D) mis-placed, not non-monotone")
    gate("G5 the 8-rung ladder CONTAINS 1086's {21,63,126}", COARSE_H,
         "all in " + str(LAD_H), all(h in LAD_H for h in COARSE_H))

    gridrows, shaperows, r8rows, steprows = [], [], [], []

    for pi, panel in enumerate(PANELS):
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
        yrs = (len(idx) - WARMUP) / 252.0
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

        m = rebalance_mask(idx, CADENCE).values
        reb = np.flatnonzero(m)

        cache: dict[tuple, tuple] = {}

        def book(N, H):
            key = (N, H)
            if key not in cache:
                Wm = build(rank_key, elig, priced, reb, N, H, T, K, GROSS)
                gr, tn = nrun(rets, lagmat(Wm), np.roll(m, LAG))
                cache[key] = (gr - tn * COST / 1e4, tn)
            return cache[key]

        for N in LAD_N:
            for H in LAD_H:
                r, tn = book(N, H)
                w = windows_of(r[WARMUP:], i_oos - WARMUP)
                a4, b4 = legs_4a(w, lw), legs_4b(w, sw)
                gridrows.append(dict(panel=pname, N=N, H=H, turn_yr=float(tn[WARMUP:].sum() / yrs),
                                     **flat(w), keep4a=all(a4.values()), keep4b=all(b4.values()),
                                     fail4a=failed(a4), fail4b=failed(b4), **a4, **b4))

        if pi == 0:
            Wm = build(rank_key, elig, priced, reb, 20, ANCHOR_H, T, K, GROSS)
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=COST, freq=CADENCE)["returns"].values
            r, _ = book(20, ANCHOR_H)
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - r[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 N=20 H=126)", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wl = windows_of(r[WARMUP:], i_oos - WARMUP)
            wt = windows_of(r[WARMUP:itr], i_oos - WARMUP)
            say(f"   U56 anchor on the LIVE tape (ungated): {wl['full']['CAGR']:.6f}/"
                f"{wl['full']['Sharpe']:.6f}/{wl['full']['MaxDD']:.6f}")
            d2 = max(abs((wt["full"]["CAGR"], wt["full"]["Sharpe"], wt["full"]["MaxDD"])[i] - A936_WH126[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN U56 N=20 H=126 triple == 936/1082/1174's committed (tape to {COMMIT_TAPE_END})",
                 f"{wt['full']['CAGR']:.6f}/{wt['full']['Sharpe']:.6f}/{wt['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{A936_WH126} < 5e-4", d2 < 5e-4)
            swt = windows_of(spy_r[WARMUP:itr], i_oos - WARMUP)
            d3 = max(abs((swt["oos"]["CAGR"], swt["oos"]["Sharpe"], swt["oos"]["MaxDD"])[i] - SPY_OOS_COMMITTED[i])
                     for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END}; live tape "
                 f"{sw['oos']['CAGR']:.4f}/{sw['oos']['Sharpe']:.4f}/{sw['oos']['MaxDD']:.4f})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            gate("G4 live RULES v2 MaxDD == committed -12.05%", f"{lw['full']['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4", abs(lw["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)

        # ---------------- shape + resolution + rule 8, per N family
        for N in LAD_N:
            R = np.array([book(N, H)[0][WARMUP:] for H in LAD_H])
            W = [windows_of(R[j], i_oos - WARMUP) for j in range(len(LAD_H))]
            S = np.array([w["full"]["Sharpe"] for w in W])
            tn_yr = np.array([float(book(N, H)[1][WARMUP:].sum() / yrs) for H in LAD_H])
            seed = zlib.crc32(f"{pname}|{N}".encode()) ^ SEED0
            B = boot_draws(R, seed)                       # (NDRAW, 8) Sharpe per draw
            if pi == 0 and N == LAD_N[0]:
                am = np.zeros(len(LAD_H))
                for d in range(NDRAW):
                    am[int(np.nanargmax(B[d]))] += 1
                gate("G6 bootstrap argmax probabilities sum to 1", f"{am.sum()/NDRAW:.6f}", "== 1.0",
                     abs(am.sum() / NDRAW - 1.0) < 1e-12)
                B2 = boot_draws(R, seed)
                gate("G6b bootstrap determinism (same seed, same draws)",
                     f"{float(np.abs(B - B2).max()):.3e}", "== 0.0", float(np.abs(B - B2).max()) == 0.0)
            pboot = np.array([float((np.nanargmax(B, axis=1) == j).mean()) for j in range(len(LAD_H))])

            # adjacent steps with PAIRED bootstrap SE
            ndec = 0
            signs = []
            for j in range(len(LAD_H) - 1):
                step = S[j + 1] - S[j]
                se = float(np.nanstd(B[:, j + 1] - B[:, j], ddof=1))
                dec = bool(abs(step) >= SE_MULT * se) if se > 0 else False
                ndec += int(dec)
                signs.append(np.sign(step))
                steprows.append(dict(panel=pname, N=N, H_lo=LAD_H[j], H_hi=LAD_H[j + 1],
                                     S_lo=S[j], S_hi=S[j + 1], step=step, paired_SE=se,
                                     step_over_SE=(step / se if se > 0 else np.nan), decisive=dec))
            mono = bool(len(set(np.sign(np.array(signs)[np.array(signs) != 0]))) <= 1)
            jmax = int(np.nanargmax(S))
            interior = bool(0 < jmax < len(LAD_H) - 1)
            top2 = np.sort(S)[::-1]
            j2 = int(np.argsort(S)[::-1][1])
            gap_se = float(np.nanstd(B[:, jmax] - B[:, j2], ddof=1))
            # 1086's own statistic on the coarse sub-ladder
            ci = [LAD_H.index(h) for h in COARSE_H]
            lo, hi = min(S[ci[0]], S[ci[2]]), max(S[ci[0]], S[ci[2]])
            between_coarse = bool(lo <= S[ci[1]] <= hi)
            se_c = float(np.nanstd(B[:, ci[1]] - B[:, ci[0]], ddof=1))
            se_c2 = float(np.nanstd(B[:, ci[1]] - B[:, ci[2]], ddof=1))
            excess = 0.0 if between_coarse else min(abs(S[ci[1]] - lo), abs(S[ci[1]] - hi))
            # fine-ladder neighbours of 63
            k63 = LAD_H.index(63)
            lo_f, hi_f = min(S[k63 - 1], S[k63 + 1]), max(S[k63 - 1], S[k63 + 1])
            between_fine = bool(lo_f <= S[k63] <= hi_f)
            shaperows.append(dict(panel=pname, N=N, monotone=mono, n_decisive_steps=ndec,
                                  argmax_H=LAD_H[jmax], argmax_interior=interior,
                                  S_top=top2[0], S_second=top2[1], top_gap=top2[0] - top2[1],
                                  top_gap_SE=gap_se,
                                  top_gap_over_SE=((top2[0] - top2[1]) / gap_se if gap_se > 0 else np.nan),
                                  top_decisive=bool((top2[0] - top2[1]) >= SE_MULT * gap_se),
                                  P_argmax_top=float(pboot[jmax]), P_argmax_126=float(pboot[LAD_H.index(126)]),
                                  between_coarse_1086=between_coarse, coarse_excess=excess,
                                  coarse_excess_over_SE=(excess / max(se_c, se_c2) if max(se_c, se_c2) > 0 else np.nan),
                                  between_fine_neighbours=between_fine,
                                  S_by_H={h: round(float(S[j]), 4) for j, h in enumerate(LAD_H)}))
            say(f"\n   {pname} N={N}: Sharpe by H  " +
                "  ".join(f"{h}:{S[j]:.4f}" for j, h in enumerate(LAD_H)))
            say(f"      turnover/yr  " + "  ".join(f"{h}:{tn_yr[j]:.2f}" for j, h in enumerate(LAD_H)))
            say(f"      P(argmax)    " + "  ".join(f"{h}:{pboot[j]:.3f}" for j, h in enumerate(LAD_H)))
            say(f"      monotone={mono}  decisive steps {ndec}/7  argmax H={LAD_H[jmax]} "
                f"(interior={interior}, top gap {top2[0]-top2[1]:+.4f} on paired SE {gap_se:.4f} = "
                f"{(top2[0]-top2[1])/gap_se if gap_se>0 else float('nan'):.2f} SE)")
            say(f"      1086's BETWEEN(63 | 21,126) = {between_coarse}  (excess {excess:+.4f} = "
                f"{excess/max(se_c,se_c2) if max(se_c,se_c2)>0 else float('nan'):.2f} SE); "
                f"between FINE neighbours 42,90 = {between_fine}")

            # ---- rule 8: IS-only pick over the 8 rungs, OOS read once
            oos_S = np.array([w["oos"]["Sharpe"] for w in W])
            is_S = np.array([w["is_"]["Sharpe"] for w in W])
            rc = rankcorr(is_S, oos_S)
            ai = LAD_H.index(ANCHOR_H)
            for ch in CHOOSERS:
                vals = np.array([stat_of(ch, w) for w in W])
                j = int(np.nanargmax(vals))
                pw = W[j]
                b4 = legs_4b(pw, sw)
                a4 = legs_4a(pw, lw)
                r8rows.append(dict(panel=pname, N=N, chooser=ch, pick_H=LAD_H[j],
                                   reach_anchor=int(j == ai),
                                   pick_OOS_S=oos_S[j], anchor_OOS_S=oos_S[ai],
                                   delta_vs_anchor=oos_S[j] - oos_S[ai],
                                   ladder_mean_OOS_S=float(np.nanmean(oos_S)),
                                   best_OOS_S=float(np.nanmax(oos_S)), worst_OOS_S=float(np.nanmin(oos_S)),
                                   spy_OOS_S=sw["oos"]["Sharpe"],
                                   pick_OOS_CAGR=pw["oos"]["CAGR"], pick_OOS_DD=pw["oos"]["MaxDD"],
                                   anchor_OOS_CAGR=W[ai]["oos"]["CAGR"], anchor_OOS_DD=W[ai]["oos"]["MaxDD"],
                                   spy_OOS_CAGR=sw["oos"]["CAGR"], spy_OOS_DD=sw["oos"]["MaxDD"],
                                   rank_IS_OOS=rc, keep4b=all(b4.values()), fail4b=failed(b4),
                                   keep4a=all(a4.values()), fail4a=failed(a4)))
                say(f"      rule8 {ch:11s} picks H={LAD_H[j]:3d} (anchor {ANCHOR_H})  OOS S "
                    f"{oos_S[j]:.4f} vs anchor {oos_S[ai]:.4f}  delta {oos_S[j]-oos_S[ai]:+.4f}  "
                    f"SPY {sw['oos']['Sharpe']:.4f}  4b {'PASS' if all(b4.values()) else 'FAIL ' + failed(b4)}")
            say(f"      IS/OOS Sharpe rank correlation over the 8 rungs: {rc:+.4f}")

        # G7 turnover monotone in H
        for N in LAD_N:
            tn_yr = np.array([float(book(N, H)[1][WARMUP:].sum() / yrs) for H in LAD_H])
            d = np.diff(tn_yr)
            gate(f"G7 turnover non-increasing in H ({pname} N={N})",
                 f"max positive step {float(d.max()):+.4f}/yr", "<= 1e-9", bool(d.max() <= 1e-9))

        if pi == 0:
            r_a, _ = book(20, ANCHOR_H)
            cache.clear()
            r_b, _ = book(20, ANCHOR_H)
            gate("G8 determinism (anchor book recomputes bit for bit)",
                 f"{float(np.abs(r_a - r_b).max()):.3e}", "== 0.0", float(np.abs(r_a - r_b).max()) == 0.0)

    g = pd.DataFrame(gridrows)
    sh = pd.DataFrame(shaperows)
    st = pd.DataFrame(steprows)
    r8 = pd.DataFrame(r8rows)
    dump(g, "grid")
    dump(sh, "shape")
    dump(st, "steps")
    dump(r8, "walkforward")
    dump(pd.DataFrame(GATES), "gates")

    say("\n" + "=" * 100)
    say("## ANSWER")
    say(f"   shape families: {len(sh)}  monotone {int(sh.monotone.sum())}/{len(sh)}  "
        f"interior argmax {int(sh.argmax_interior.sum())}/{len(sh)}  "
        f"top gap decisive at {SE_MULT:.0f} SE {int(sh.top_decisive.sum())}/{len(sh)}")
    say(f"   adjacent steps: {len(st)}  decisive at {SE_MULT:.0f} SE {int(st.decisive.sum())}/{len(st)} "
        f"({st.decisive.mean():.4f}); median |step|/SE {float(st.step_over_SE.abs().median()):.4f}")
    say(f"   1086's BETWEEN(63 | 21,126) holds at {int(sh.between_coarse_1086.sum())}/{len(sh)} families; "
        f"63 inside its FINE neighbours (42,90) at {int(sh.between_fine_neighbours.sum())}/{len(sh)}")
    say(f"   P(argmax = the incumbent H=126): {sh.P_argmax_126.tolist()}")
    say(f"   rule 8 pick-minus-anchor OOS Sharpe: mean {float(r8.delta_vs_anchor.mean()):+.4f}, "
        f"positive at {int((r8.delta_vs_anchor > 0).sum())}/{len(r8)}, "
        f"reach (pick == incumbent H) {int(r8.reach_anchor.sum())}/{len(r8)}")
    say(f"   IS/OOS Sharpe rank correlation over the 8 rungs, per family: "
        f"{[round(x,4) for x in sh.index.map(lambda i: r8.iloc[i*len(CHOOSERS)].rank_IS_OOS).tolist()]}")
    say(f"   4b PASS at {int(g.keep4b.sum())}/{len(g)} cells; 4a PASS at {int(g.keep4a.sum())}/{len(g)}")
    say(f"   gates: {sum(x['pass_'] for x in GATES)}/{len(GATES)} PASS")
    say(f"   [t={time.time()-t0:.0f}s]")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
