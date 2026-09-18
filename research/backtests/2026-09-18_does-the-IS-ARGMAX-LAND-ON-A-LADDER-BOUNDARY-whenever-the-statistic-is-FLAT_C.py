#!/usr/bin/env python3
"""Idea 1195 (lane C, 2026-09-18): does the IS ARGMAX LAND ON A LADDER BOUNDARY whenever the
STATISTIC is FLAT?

QUESTION.  Idea 1189 found that because IS Sharpe is flat in gross, the IS argmax lands on the
TOP rung g=1.00 at 2 of 3 panels on noise of order 1e-3, and carries OOS MaxDD -32.11% with it.
The queue asks for the general form: across the record's N, H, GROSS and CADENCE ladders,
measure each cell's IS FLATNESS and report whether BOUNDARY picks are predicted by it.

WHAT IS MEASURED.  For every (panel, ladder, statistic) cell the run builds all EIGHT rung
books, reads the statistic on the IS window ALONE, and records
    SPREAD    = max_j v_j - min_j v_j                 (the ladder's IS range)
    SE_PAIR   = block-bootstrap sd of (v_argmax - v_argmin), SHARED block index across rungs,
                so the cross-rung correlation that makes these ladders hard to resolve is
                preserved rather than destroyed
    FLAT_RATIO= SPREAD / SE_PAIR                      (bar-free; the bar is a dial below)
    BOUNDARY  = 1 iff the IS argmax sits at rung 0 or rung 7
    P_BOUND   = P(the IS argmax is at a boundary rung) over the same 1000 joint redraws
The chance line for BOUNDARY under a uniform pick over 8 rungs is exactly 2/8 = 0.250.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    AXIS SET  {ALL4, NONGROSS3}  -- ALL4 = {N, H, GROSS, CADENCE}; NONGROSS3 drops GROSS, the
              ladder 1214/1223 showed supplies its own significance (IS Sharpe spread
              0.0011-0.0034 against N's 0.0465-0.2552).  1189's headline lives on GROSS, so
              whether the general form survives without it is the question's own robustness.
    F_BAR     {0.5, 1.0, 2.0, 3.0} SE -- a cell is FLAT iff FLAT_RATIO < F_BAR.
  2 x 4 = 8 headline grid points, EVERY ONE PUBLISHED in the .grid.csv and the console.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); LADDER {N, H, GROSS,
CADENCE}; STATISTIC {Sharpe, CAGR, MaxDD}; both KEEP paths leg by leg on EVERY rung book and
on EVERY pick; full / halves / IS / OOS.  That is 3 x 4 x 3 = 36 flatness-and-boundary cells,
against 1189's 3.

THE FOUR LADDERS, EIGHT RUNGS EACH, THE RECORD'S OWN RUNGS (1153's, unchanged):
    N        [5, 8, 10, 12, 15, 20, 25, 30]
    H        [5, 10, 21, 42, 63, 90, 126, 189]        (MIN-HOLD days)
    GROSS    [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
    CADENCE  [D, W, 2W, M, 2M, Q, 2Q, 4Q]
ANCHOR (frozen, NAMED not tuned): N=20, H=126, gross=0.75, W -- the standing cell
936/1071/1082/1094/1096/1101/1174 quote.  Each ladder walks one coordinate off that anchor.
CADENCE's 2W/2M/2Q/4Q are every k-th CALENDAR period end, parity 0 from the first period end
(idea 1064: not a modular phase cycle), stated here rather than chosen.

FROZEN, NOT DIALS: CAND composite of the 12-1 / 6m / 3m percentile ranks; eligibility = above
own 200d MA AND 20d vol < 0.60; cap INF; equal weight gross/len(selected) with gated weight to
CASH; 10 bps per unit turnover; next-day execution (LAG 1); 260-row warm-up; IS = warm-up..
2016-12-31, OOS = 2017-01-01 onward read ONCE; block bootstrap L = 63, 1000 draws.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) FLATNESS PREDICTS BOUNDARY -- boundary rate among FLAT cells is materially above the
      NON-FLAT rate and above the 0.250 chance line.  Then 1189's reading generalises and the
      record should refuse any argmax whose ladder is flat at its own SE.
  (B) BOUNDARY IS UNCONDITIONAL -- the two rates are inside noise of each other.  Then
      boundary landing is not a flatness fact and 1189's mechanism is not the general one.
  (C) THE BAR IS UNSETTABLE -- FLAT_RATIO does not separate on this tape (all cells on one
      side at every F_BAR), so no clause can be written from 36 cells.
  (D) CAPITAL, reported FIRST whichever of (A)-(C) fires: the sign and size of
      pick-minus-anchor OOS Sharpe and OOS MaxDD, split by FLAT / NON-FLAT.

RULE 8 (walk-forward, required).  Every pick here is IS-only by construction (IS window ends
2016-12-31) and the OOS window 2017-01-01.. is read ONCE, after the picks are fixed.  At every
(panel, ladder, statistic) the run publishes the pick's OOS CAGR/Sharpe/MaxDD against (i) the
ANCHOR over the same rows -- the do-nothing bar, since the anchor is the book the record
already holds -- (ii) the LIVE RULES v2 baseline, (iii) SPY, and (iv) the ladder's own best and
worst rung OOS, plus the IS/OOS rank correlation over the 8 rungs.

GATES.  G1 the fast runner reproduces engine.backtest on the U56 anchor book.  G2 CROSS-RUN:
that book's (CAGR, Sharpe, MaxDD) reproduces 936/1082/1174's committed triple.  G3 CROSS-RUN
SPY OOS triple.  G2/G3 are read on the tape TRUNCATED to 2026-09-15, where the tape ended when
those numbers were committed; live-tape readings printed beside them, ungated.  G4 live RULES
v2 MaxDD == committed -12.05%.  G5 all four ladders are 8 rungs and contain the anchor.  G6 the
gross=0.75 rung is bit-identical to the W rung (the four lines agree where they cross).  G7 the
bootstrap is deterministic and its boundary probabilities are in [0,1].  G8 CROSS-RUN 1189: the
GROSS ladder's IS-Sharpe argmax is the TOP rung at 2 of 3 panels.  G9 determinism: the U56
GROSS ladder recomputes bit for bit.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a CONTRAST between cells of the same panel and dates (flat vs
non-flat ladders), which is first-order immune to a level bias that moves all of them together;
the 4a/4b legs and the pick-minus-anchor drawdowns are not.

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
SLUG = "does-the-IS-ARGMAX-LAND-ON-A-LADDER-BOUNDARY-whenever-the-statistic-is-FLAT"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"

# ---- frozen construction (NOT dials) --------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BLOCK, NDRAW, SEED0 = 63, 1000, 1195
COMMIT_TAPE_END = "2026-09-15"

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30]
LAD_H = [5, 10, 21, 42, 63, 90, 126, 189]
LAD_G = [0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 1.00]
LAD_C = ["D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
ANCHOR = dict(N=20, H=126, GROSS=0.75, CADENCE="W")
STATS = ["Sharpe", "CAGR", "MaxDD"]

# ---- the two dials ---------------------------------------------------------------------------
AXIS_SETS = {"ALL4": ["N", "H", "GROSS", "CADENCE"], "NONGROSS3": ["N", "H", "CADENCE"]}
F_BARS = [0.5, 1.0, 2.0, 3.0]

# ---- committed cross-run constants ----------------------------------------------------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
N1189_TOP_PANELS = 2          # 1189: IS-Sharpe argmax is the TOP gross rung at 2 of 3 panels

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


def stats_of(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows_of(r, i_oos):
    n = len(r)
    h = n // 2
    return dict(full=stats_of(r), h1=stats_of(r[:h]), h2=stats_of(r[h:]),
                is_=stats_of(r[:i_oos]), oos=stats_of(r[i_oos:]))


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


# ------------------------------------------------------------------ book machinery (1082/1153)
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
    """MIN HOLD H, N slots, cap INF, equal weight gross/len(sel), gated weight to CASH."""
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


# ------------------------------------------------------------------ flatness bootstrap
def boot_ladder(R_is, seed):
    """Joint moving-block redraws of the IS window, SHARED block index across the 8 rungs.

    Returns per statistic: sd of (v_argmax_obs - v_argmin_obs) over draws (the PAIRED SE of the
    observed ladder's own range), and P(argmax at a boundary rung).  The pair whose SE is taken
    is fixed by the OBSERVED ladder before any redraw, so the SE is not itself selected."""
    n, T = R_is.shape
    rng = np.random.default_rng(seed)
    nb = int(np.ceil(T / BLOCK))
    starts_all = rng.integers(0, T - BLOCK + 1, size=(NDRAW, nb))
    off = np.arange(BLOCK)
    draws = {s: np.empty((NDRAW, n)) for s in STATS}
    for d in range(NDRAW):
        idx = (starts_all[d][:, None] + off[None, :]).ravel()[:T]
        X = R_is[:, idx]
        mu = X.mean(axis=1)
        sd = X.std(axis=1, ddof=0)
        draws["Sharpe"][d] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
        eq = np.cumprod(1.0 + X, axis=1)
        draws["CAGR"][d] = eq[:, -1] ** (252.0 / T) - 1.0
        draws["MaxDD"][d] = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
    return draws


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1195 lane C — {SLUG}")
    say(f"# frozen: CAND legs {LEGS}, elig above-200d & vol20 < {MAXVOL}, cap INF, gated weight to "
        f"CASH, {COST:.0f} bps, t+{LAG}, warm-up {WARMUP}, IS end {IS_END.date()}")
    say(f"# ANCHOR {ANCHOR}")
    for k, v in LADDERS.items():
        say(f"# ladder {k:8s} ({len(v)} rungs): {v}")
    say(f"# DIAL 1 AXIS SET = {AXIS_SETS}")
    say(f"# DIAL 2 F_BAR = {F_BARS} SE (a cell is FLAT iff FLAT_RATIO = SPREAD/SE_PAIR < F_BAR)")
    say(f"# statistics {STATS} (reported at every value, not a dial); block bootstrap L={BLOCK}, "
        f"{NDRAW} draws, shared block index across a ladder's rungs")
    say(f"# chance line for a boundary landing under a uniform pick over 8 rungs = 0.250")

    ok5 = all(len(v) == 8 for v in LADDERS.values()) and all(
        ANCHOR[k] in v for k, v in LADDERS.items())
    gate("G5 four ladders, 8 rungs each, anchor on every one",
         {k: (len(v), ANCHOR[k] in v) for k, v in LADDERS.items()}, "all (8, True)", ok5)

    cellrows, bookrows, wfrows = [], [], []

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
        for lad, rungs in LADDERS.items():
            for v in rungs:
                c = dict(ANCHOR)
                c[lad] = v
                need.add((c["N"], c["H"], c["GROSS"], c["CADENCE"]))
        say(f"   building {len(need)} distinct rung books ...")
        W_by_key: dict[tuple, dict] = {}
        for (N, H, g, cad) in sorted(need, key=str):
            r = book(N, H, g, cad)
            w = windows_of(r[WARMUP:], i_oos - WARMUP)
            W_by_key[(N, H, round(float(g), 4), cad)] = w
            a4, b4 = legs_4a(w, lw), legs_4b(w, sw)
            bookrows.append(dict(panel=pname, N=N, H=H, gross=g, cadence=cad, **flat(w),
                                 keep4a=all(a4.values()), keep4b=all(b4.values()),
                                 fail4a=failed(a4), fail4b=failed(b4)))
        say(f"   built {len(need)} books  [t={time.time()-t0:.0f}s]")

        anch_r = book(ANCHOR["N"], ANCHOR["H"], ANCHOR["GROSS"], ANCHOR["CADENCE"])
        anch_w = W_by_key[(ANCHOR["N"], ANCHOR["H"], round(ANCHOR["GROSS"], 4), ANCHOR["CADENCE"])]

        if pi == 0:
            m = cadence_mask(idx, ANCHOR["CADENCE"])
            Wm = build(rank_key, elig, priced, np.flatnonzero(m), ANCHOR["N"], ANCHOR["H"], T, K,
                       ANCHOR["GROSS"])
            eng = backtest(px, pd.DataFrame(Wm, index=idx, columns=px.columns),
                           cost_bps=COST, freq=ANCHOR["CADENCE"])["returns"].values
            d1 = float(np.nanmax(np.abs(np.asarray(eng[WARMUP:], float) - anch_r[WARMUP:])))
            gate("G1 fast runner == engine.backtest (U56 anchor)", f"{d1:.3e}", "< 1e-12", d1 < 1e-12)
            itr = int(idx.searchsorted(pd.Timestamp(COMMIT_TAPE_END), side="right"))
            wt_ = windows_of(anch_r[WARMUP:itr], i_oos - WARMUP)
            say(f"   U56 anchor on the LIVE tape (ungated): {anch_w['full']['CAGR']:.6f}/"
                f"{anch_w['full']['Sharpe']:.6f}/{anch_w['full']['MaxDD']:.6f}")
            d2 = max(abs((wt_["full"]["CAGR"], wt_["full"]["Sharpe"], wt_["full"]["MaxDD"])[i] - A936_WH126[i])
                     for i in range(3))
            gate(f"G2 CROSS-RUN U56 anchor triple == 936/1082/1174's (tape to {COMMIT_TAPE_END})",
                 f"{wt_['full']['CAGR']:.6f}/{wt_['full']['Sharpe']:.6f}/{wt_['full']['MaxDD']:.6f} "
                 f"maxdiff {d2:.2e}", f"{A936_WH126} < 5e-4", d2 < 5e-4)
            swt = windows_of(spy_r[WARMUP:itr], i_oos - WARMUP)
            d3 = max(abs((swt["oos"]["CAGR"], swt["oos"]["Sharpe"], swt["oos"]["MaxDD"])[i] - SPY_OOS_COMMITTED[i])
                     for i in range(3))
            gate(f"G3 CROSS-RUN SPY OOS triple (tape to {COMMIT_TAPE_END}; live tape reads "
                 f"{sw['oos']['CAGR']:.4f}/{sw['oos']['Sharpe']:.4f}/{sw['oos']['MaxDD']:.4f})",
                 f"{swt['oos']['CAGR']:.4f}/{swt['oos']['Sharpe']:.4f}/{swt['oos']['MaxDD']:.4f} "
                 f"maxdiff {d3:.2e}", f"{SPY_OOS_COMMITTED} < 5e-4", d3 < 5e-4)
            gate("G4 live RULES v2 MaxDD == committed -12.05%", f"{lw['full']['MaxDD']:.4f}",
                 f"{LIVE_MAXDD_COMMITTED} < 5e-4",
                 abs(lw["full"]["MaxDD"] - LIVE_MAXDD_COMMITTED) < 5e-4)
            rg = book(ANCHOR["N"], ANCHOR["H"], 0.75, "W")
            gate("G6 the GROSS=0.75 rung IS the W rung (the four lines agree where they cross)",
                 f"{float(np.abs(rg - anch_r).max()):.3e}", "== 0.0",
                 float(np.abs(rg - anch_r).max()) == 0.0)

        # ---- the flatness / boundary grid
        say("\n   ladder   stat   | IS argmax rung      SPREAD   SE_PAIR  FLAT_RATIO  BOUND P_BOUND MONO |"
            "  pickOOS  anchOOS   delta | rankIS/OOS | 4b pick")
        for lad in LADDERS:
            rungs = LADDERS[lad]
            R_all, W_all = [], []
            for v in rungs:
                c = dict(ANCHOR)
                c[lad] = v
                r = book(c["N"], c["H"], c["GROSS"], c["CADENCE"])
                R_all.append(r[WARMUP:])
                W_all.append(W_by_key[(c["N"], c["H"], round(float(c["GROSS"]), 4), c["CADENCE"])])
            R_all = np.array(R_all)
            n_is = i_oos - WARMUP
            seed = zlib.crc32(f"{pname}|{lad}".encode()) ^ SEED0
            draws = boot_ladder(R_all[:, :n_is], seed)
            if pi == 0 and lad == "N":
                d2b = boot_ladder(R_all[:, :n_is], seed)
                same = max(float(np.abs(draws[s] - d2b[s]).max()) for s in STATS)
                gate("G7 bootstrap determinism (same seed, same draws)", f"{same:.3e}", "== 0.0",
                     same == 0.0)
            if pi == 0 and lad == "GROSS":
                r_re = []
                for v in rungs:
                    c = dict(ANCHOR)
                    c[lad] = v
                    m2 = cadence_mask(idx, c["CADENCE"])
                    Wm2 = build(rank_key, elig, priced, np.flatnonzero(m2), c["N"], c["H"], T, K,
                                float(c["GROSS"]))
                    g2, t2 = nrun(rets, lagmat(Wm2), np.roll(m2, LAG))
                    r_re.append((g2 - t2 * COST / 1e4)[WARMUP:])
                dz = float(np.abs(np.array(r_re) - R_all).max())
                gate("G9 determinism: U56 GROSS ladder recomputes bit for bit", f"{dz:.3e}", "== 0.0",
                     dz == 0.0)

            for st in STATS:
                v = np.array([W_all[j]["is_"][st] for j in range(len(rungs))], float)
                jmax, jmin = int(np.nanargmax(v)), int(np.nanargmin(v))
                spread = float(v[jmax] - v[jmin])
                dmat = draws[st]
                se_pair = float(np.nanstd(dmat[:, jmax] - dmat[:, jmin], ddof=1))
                fr = float(spread / se_pair) if se_pair > 0 else float("inf")
                bnd = int(jmax in (0, len(rungs) - 1))
                p_bound = float(np.mean([int(np.nanargmax(dmat[d]) in (0, len(rungs) - 1))
                                         for d in range(NDRAW)]))
                pw = W_all[jmax]
                # MONO: |rank correlation of the IS statistic with RUNG POSITION|.  A ladder whose
                # statistic is monotone in its dial puts its argmax at an end BY CONSTRUCTION,
                # flat or not; this is the competing explanation for a boundary landing and it is
                # measured here rather than assumed.  Reported, not a dial.
                mono = abs(rankcorr(np.arange(len(rungs), dtype=float), v))
                oos_l = np.array([W_all[j]["oos"]["Sharpe"] for j in range(len(rungs))])
                is_l = np.array([W_all[j]["is_"]["Sharpe"] for j in range(len(rungs))])
                rc = rankcorr(is_l, oos_l)
                a4p, b4p = legs_4a(pw, lw), legs_4b(pw, sw)
                c = dict(ANCHOR)
                c[lad] = rungs[jmax]
                cellrows.append(dict(
                    panel=pname, ladder=lad, stat=st, argmax_rung=str(rungs[jmax]),
                    argmax_index=jmax, argmin_rung=str(rungs[jmin]), is_max=v[jmax], is_min=v[jmin],
                    spread=spread, se_pair=se_pair, flat_ratio=fr, boundary=bnd, p_bound=p_bound,
                    mono=mono,
                    pick_N=c["N"], pick_H=c["H"], pick_gross=c["GROSS"], pick_cadence=c["CADENCE"],
                    pick_oos_CAGR=pw["oos"]["CAGR"], pick_oos_Sharpe=pw["oos"]["Sharpe"],
                    pick_oos_MaxDD=pw["oos"]["MaxDD"],
                    anchor_oos_CAGR=anch_w["oos"]["CAGR"], anchor_oos_Sharpe=anch_w["oos"]["Sharpe"],
                    anchor_oos_MaxDD=anch_w["oos"]["MaxDD"],
                    live_oos_Sharpe=lw["oos"]["Sharpe"], spy_oos_Sharpe=sw["oos"]["Sharpe"],
                    spy_oos_CAGR=sw["oos"]["CAGR"], spy_oos_MaxDD=sw["oos"]["MaxDD"],
                    d_oos_Sharpe=pw["oos"]["Sharpe"] - anch_w["oos"]["Sharpe"],
                    d_oos_MaxDD=pw["oos"]["MaxDD"] - anch_w["oos"]["MaxDD"],
                    d_oos_CAGR=pw["oos"]["CAGR"] - anch_w["oos"]["CAGR"],
                    best_rung_oos=float(np.nanmax(oos_l)), worst_rung_oos=float(np.nanmin(oos_l)),
                    mean_rung_oos=float(np.nanmean(oos_l)), rank_is_oos=rc,
                    pick_keep4a=all(a4p.values()), pick_keep4b=all(b4p.values()),
                    pick_fail4b=failed(b4p), **{f"pw_{k}": vv for k, vv in flat(pw).items()}))
                wfrows.append(dict(panel=pname, ladder=lad, stat=st, pick=str(rungs[jmax]),
                                   pick_oos_CAGR=pw["oos"]["CAGR"], pick_oos_Sharpe=pw["oos"]["Sharpe"],
                                   pick_oos_MaxDD=pw["oos"]["MaxDD"],
                                   anchor_oos_CAGR=anch_w["oos"]["CAGR"],
                                   anchor_oos_Sharpe=anch_w["oos"]["Sharpe"],
                                   anchor_oos_MaxDD=anch_w["oos"]["MaxDD"],
                                   live_oos_CAGR=lw["oos"]["CAGR"], live_oos_Sharpe=lw["oos"]["Sharpe"],
                                   live_oos_MaxDD=lw["oos"]["MaxDD"],
                                   spy_oos_CAGR=sw["oos"]["CAGR"], spy_oos_Sharpe=sw["oos"]["Sharpe"],
                                   spy_oos_MaxDD=sw["oos"]["MaxDD"],
                                   keep4a=all(a4p.values()), keep4b=all(b4p.values()),
                                   fail4b=failed(b4p)))
                say(f"   {lad:8s} {st:6s} | {str(rungs[jmax]):>6s} (idx {jmax}) {spread:9.4f} "
                    f"{se_pair:9.4f} {fr:9.3f}  {bnd:d}  {p_bound:6.3f} {mono:5.2f} | "
                    f"{pw['oos']['Sharpe']:7.4f} {anch_w['oos']['Sharpe']:7.4f} "
                    f"{pw['oos']['Sharpe']-anch_w['oos']['Sharpe']:+7.4f} | {rc:+.3f} | "
                    f"{'PASS' if all(b4p.values()) else failed(b4p)}")

    cells = pd.DataFrame(cellrows)
    books = pd.DataFrame(bookrows)
    wf = pd.DataFrame(wfrows)

    # ---- G8 cross-run of 1189 -------------------------------------------------------------
    gsh = cells[(cells.ladder == "GROSS") & (cells.stat == "Sharpe")]
    top = int((gsh.argmax_index == 7).sum())
    say(f"\n## CROSS-RUN 1189: GROSS ladder, IS Sharpe, argmax rung by panel: "
        f"{dict(zip(gsh.panel, gsh.argmax_rung))}; OOS MaxDD of those picks: "
        f"{dict(zip(gsh.panel, gsh.pick_oos_MaxDD.round(4)))}")
    gate("G8 CROSS-RUN 1189: IS-Sharpe argmax is the TOP gross rung at 2 of 3 panels",
         f"{top} of 3", f"== {N1189_TOP_PANELS}", top == N1189_TOP_PANELS)

    # ---- headline grid: the two dials -----------------------------------------------------
    say("\n## HEADLINE GRID — every one of the 2 x 4 dial points published")
    say("   axis_set   F_BAR | nFLAT  bound|FLAT   nNONFLAT  bound|NONFLAT   diff | "
        "dOOS_Sharpe FLAT / NONFLAT | dOOS_MaxDD FLAT / NONFLAT")
    grid = []
    for aname, axes in AXIS_SETS.items():
        sub = cells[cells.ladder.isin(axes)]
        for fb in F_BARS:
            fl = sub[sub.flat_ratio < fb]
            nf = sub[sub.flat_ratio >= fb]
            bf = float(fl.boundary.mean()) if len(fl) else float("nan")
            bn = float(nf.boundary.mean()) if len(nf) else float("nan")
            row = dict(axis_set=aname, f_bar=fb, n_flat=len(fl), n_nonflat=len(nf),
                       bound_flat=bf, bound_nonflat=bn, diff=bf - bn,
                       chance=2.0 / 8.0,
                       dS_flat=float(fl.d_oos_Sharpe.mean()) if len(fl) else float("nan"),
                       dS_nonflat=float(nf.d_oos_Sharpe.mean()) if len(nf) else float("nan"),
                       dDD_flat=float(fl.d_oos_MaxDD.mean()) if len(fl) else float("nan"),
                       dDD_nonflat=float(nf.d_oos_MaxDD.mean()) if len(nf) else float("nan"),
                       pbound_flat=float(fl.p_bound.mean()) if len(fl) else float("nan"),
                       pbound_nonflat=float(nf.p_bound.mean()) if len(nf) else float("nan"),
                       mono_flat=float(fl.mono.mean()) if len(fl) else float("nan"),
                       mono_nonflat=float(nf.mono.mean()) if len(nf) else float("nan"))
            grid.append(row)
            say(f"   {aname:10s} {fb:5.1f} | {len(fl):4d}  {bf:8.3f}   {len(nf):7d}  {bn:9.3f}  "
                f"{bf-bn:+6.3f} | {row['dS_flat']:+9.4f} / {row['dS_nonflat']:+9.4f} | "
                f"{row['dDD_flat']:+9.4f} / {row['dDD_nonflat']:+9.4f}")
    grid = pd.DataFrame(grid)

    # ---- bar-free readings -----------------------------------------------------------------
    rho_all = rankcorr(cells.flat_ratio.values, cells.boundary.values)
    rho_ng = rankcorr(cells[cells.ladder != "GROSS"].flat_ratio.values,
                      cells[cells.ladder != "GROSS"].boundary.values)
    say(f"\n## BAR-FREE: rho(FLAT_RATIO, BOUNDARY) = {rho_all:+.4f} over {len(cells)} cells "
        f"(ALL4), {rho_ng:+.4f} over {len(cells[cells.ladder!='GROSS'])} (NONGROSS3). "
        f"Negative = flatter ladders land on boundaries more often.")
    rho_m = rankcorr(cells.mono.values, cells.boundary.values)
    rho_mng = rankcorr(cells[cells.ladder != "GROSS"].mono.values,
                       cells[cells.ladder != "GROSS"].boundary.values)
    say(f"   COMPETING READING rho(MONO, BOUNDARY) = {rho_m:+.4f} (ALL4), {rho_mng:+.4f} "
        f"(NONGROSS3); MONO by ladder (median) "
        f"{cells.groupby('ladder').mono.median().round(3).to_dict()}")
    hi, lo = cells[cells.mono >= 0.9], cells[cells.mono < 0.9]
    say(f"   BOUNDARY rate at MONO >= 0.90: {hi.boundary.mean():.3f} over {len(hi)} cells; "
        f"at MONO < 0.90: {lo.boundary.mean():.3f} over {len(lo)} cells (chance 0.250)")
    say(f"   FLAT_RATIO by ladder (median): "
        f"{cells.groupby('ladder').flat_ratio.median().round(3).to_dict()}")
    say(f"   BOUNDARY rate by ladder: {cells.groupby('ladder').boundary.mean().round(3).to_dict()}")
    say(f"   BOUNDARY rate by statistic: {cells.groupby('stat').boundary.mean().round(3).to_dict()}")
    say(f"   overall BOUNDARY rate {cells.boundary.mean():.3f} over {len(cells)} cells "
        f"(chance 0.250); mean P_BOUND {cells.p_bound.mean():.3f}")

    # ---- capital, reported first in the memo ------------------------------------------------
    say("\n## CAPITAL (rule 8, OOS read once): pick minus anchor, by ladder")
    for lad in LADDERS:
        s = cells[cells.ladder == lad]
        say(f"   {lad:8s} dOOS Sharpe mean {s.d_oos_Sharpe.mean():+.4f} "
            f"(positive at {int((s.d_oos_Sharpe>0).sum())} of {len(s)}), "
            f"dOOS MaxDD mean {s.d_oos_MaxDD.mean():+.4f} "
            f"(worse at {int((s.d_oos_MaxDD<0).sum())} of {len(s)}), "
            f"dOOS CAGR mean {s.d_oos_CAGR.mean():+.4f}")
    say(f"   ALL  dOOS Sharpe mean {cells.d_oos_Sharpe.mean():+.4f} "
        f"(positive at {int((cells.d_oos_Sharpe>0).sum())} of {len(cells)}); "
        f"dOOS MaxDD mean {cells.d_oos_MaxDD.mean():+.4f}; "
        f"picks passing 4b {int(cells.pick_keep4b.sum())} of {len(cells)}; "
        f"passing 4a {int(cells.pick_keep4a.sum())} of {len(cells)}")
    say(f"   rung books: 4b PASS {int(books.keep4b.sum())} of {len(books)}; "
        f"4a PASS {int(books.keep4a.sum())} of {len(books)}")
    say(f"   IS/OOS Sharpe rank correlation over rungs: mean {cells.rank_is_oos.mean():+.4f}, "
        f"positive at {int((cells.rank_is_oos>0).sum())} of {len(cells)}")

    pb = books[books.keep4b]
    say(f"\n## 4b PASSES among the {len(books)} rung books ({len(pb)}): " +
        "; ".join(f"{r.panel} N{r.N}/H{r.H}/g{r.gross}/{r.cadence} "
                  f"CAGR {r.full_CAGR:.2%} S {r.full_Sharpe:.3f} DD {r.full_MaxDD:.2%} "
                  f"OOS S {r.oos_Sharpe:.3f}" for r in pb.itertuples()))
    pk = cells[cells.pick_keep4b]
    say(f"## 4b PASSES among the {len(cells)} IS-only PICKS ({len(pk)}): " +
        "; ".join(f"{r.panel}/{r.ladder}/{r.stat} -> {r.argmax_rung}" for r in pk.itertuples()))

    fails = [g for g in GATES if not g["pass_"]]
    say(f"\n## GATES {len(GATES)-len(fails)} of {len(GATES)} pass"
        + ("" if not fails else "; FAILED: " + ", ".join(g['gate'].split(' ')[0] for g in fails)))

    cells.to_csv(f"{STEM}.cells.csv", index=False)
    books.to_csv(f"{STEM}.books.csv", index=False)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")
    say(f"\n[done in {time.time()-t0:.0f}s] wrote {Path(STEM).name}.{{cells,books,grid,walkforward,gates}}.csv")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
