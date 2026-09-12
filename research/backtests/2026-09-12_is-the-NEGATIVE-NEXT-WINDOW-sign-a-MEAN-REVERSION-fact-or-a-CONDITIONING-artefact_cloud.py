#!/usr/bin/env python3
"""Idea 839 (cloud lane, 2026-09-12) — is the NEGATIVE NEXT-WINDOW sign a MEAN-REVERSION fact or
a CONDITIONING artefact?

(Numbering note: a concurrent lane filed a different idea also numbered 839 on the same day.
This is the 2026-09-12 MEAN-REVERSION entry, disambiguated by title.)

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 832's H_INFO leg found P(next window passes 4b |
this window's halves leg PASSES) = 0.3182 against 0.3810 when it FAILS at H=756 (delta -0.0628),
and 0.7072 against 0.7838 at H=1260 (-0.0765) — the WRONG sign for a robustness clause.  But
those pairs were (i) conditioned on the other three 4b legs already passing and (ii) pooled over
entries spaced 21 trading days apart, so consecutive pairs share almost all of their data and
every book contributes a different number of them.  Either defect alone can manufacture the
sign.  This run re-runs the measurement with NON-OVERLAPPING entries, WITH and WITHOUT the
conditioning, and against permutation nulls, and reports whether the sign survives.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  CONDITIONING — which legs of the PREDICTOR window a pair must clear to enter the sample:
                     NONE (no conditioning), OTHER3 (idea 832's: full-window Sharpe + DD + CAGR),
                     DDCAGR (the two ratio legs only), SHARPE (the full-window Sharpe leg only).
  P2  PERMUTATION COUNT — 1,000 and 10,000, both reported.
Horizon H {756, 1260}, entry scheme {OVERLAP21, CHAIN, DISJOINT}, tiling offset (12 per H),
cost rung {0, 10, 25} bps and memo set {MEMO8, MEMO12} are REPORTED AT EVERY POINT, not selected.
No book dial is tuned: every book runs at the gross, band, n and cadence its own committed memo
published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C6 copied verbatim from ideas 831/832 so the three
censuses are directly comparable; C7-C10 are this run's own):
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest, weights
      decided at close t applied at t+1, the book's own cadence); windows are SLICES of it.
  C2  A window's 4b legs are read WINDOW-LOCALLY against SPY over the SAME window: full-window
      Sharpe > SPY, the HALVES leg (both len//2 blocks beat SPY's Sharpe), MaxDD >= 0.6 x SPY's,
      CAGR >= 0.7 x SPY's.  PASS requires all four.
  C3  The CAGR floor is applied LITERALLY, including where SPY's window CAGR is negative.
  C4  Warm-up: entry dates start at each panel's px.index[260], as baseline.compare does.
  C5  A window must lie wholly inside the sample.
  C6  A book is scored against its own panel's SPY column.
  C7  ENTRY SCHEMES.  OVERLAP21 = idea 832's own pooling: entries every 21 trading days, the
      pair partner is the window starting H days later.  CHAIN = a disjoint TILING at offset o
      (windows at i0+o, i0+o+H, i0+o+2H, ...) with pairs (tile j, tile j+1): no window overlaps
      another, but each window appears in two pairs.  DISJOINT = the same tiling with pairs
      (t0,t1), (t2,t3), ...: every window is used exactly ONCE, in one pair, as either predictor
      or target.  DISJOINT is the queue's "non-overlapping entries only" and is the headline.
  C8  A tiling offset o runs over 12 values evenly spaced on [0, H).  Offsets are NOT independent
      samples of anything — they are reported as a SPREAD, and the pooled statistic pools the
      pairs, it does not average the offsets' deltas.
  C9  DELTA = P(target window PASSes 4b | predictor window's halves leg PASSES)
            - P(target window PASSes 4b | predictor window's halves leg FAILS), over the pairs a
      given conditioning admits.  NaN where either arm is empty.
  C10 NULLS.  WITHIN = permute the predictor's halves verdict WITHIN each book (preserves book
      sizes and each book's halves marginal; destroys any within-book relation).  BOOKLAB =
      permute the BOOK LABEL across pairs, keeping book sizes (the queue's ask).  Both two-sided,
      fixed seed.  Gate G6 records that BOOKLAB leaves the POOLED delta exactly invariant, which
      is itself the reason the pooled number cannot be defended with that null.

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_REPRO    idea 832's committed H_INFO cell reproduces: 627 pairs at H=756 with 0.3182 /
             0.3810 / -0.0628, and 419 pairs at H=1260 with 0.7072 / 0.7838 / -0.0765.
  H_SURVIVE  the sign SURVIVES the strictest reading: pooled delta < 0 under DISJOINT entries at
             H=756 with NO conditioning.
  H_COND     the conditioning is doing the work: |delta(NONE)| < 0.5 x |delta(OTHER3)| at the
             OVERLAP21 / H=756 cell.
  H_WITHIN   the pooled delta is outside its own two-sided 95% WITHIN-book permutation band at
             the DISJOINT / H=756 / NONE cell.
  H_SIMPSON  the pooled delta is NOT a composition effect: the pair-weighted mean of the
             per-book deltas has the same sign and is within 0.05 of the pooled delta at the
             OVERLAP21 / H=756 / OTHER3 cell.
  H_BOOKS    at least 9 of the books with a defined delta carry the negative sign at the
             DISJOINT / H=756 / NONE cell (idea 832 reported 9 of 11 at its own cell).
  H_BOOKLAB  the mean per-book delta is outside its two-sided 95% BOOKLAB band at the same cell.
  H_WF       (rule 8) the (conditioning, H) cell with the most negative delta on IS pairs is
             also the most negative on OOS pairs, and |OOS delta - IS delta| <= 0.10 there.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp.
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05%.
  G3  the vectorised window metrics reproduce engine.metrics exactly (bar 1e-10) on 200
      fixed-seed random windows.
  G4  this run's OVERLAP21 census reproduces idea 832's committed H_INFO numbers (H_REPRO above,
      bars |dP| <= 0.0005 and exact pair counts).
  G5  every DISJOINT tiling is disjoint and in-sample: no two windows in a tiling share a day,
      and each window is used in exactly one pair.
  G6  BOOKLAB leaves the POOLED delta invariant to 1e-15 over 100 draws (by construction — the
      pooled statistic does not read labels).  Recorded, not a pass/fail of the finding.

Outputs (all under research/backtests/, all committed):
  .txt            full console log
  .books.csv      one row per book: fixed-window + OOS metrics, both KEEP paths
  .pairs.csv.gz   one row per (book, H, scheme, offset, cost, pair): every leg on both windows
  .grid.csv       one row per (memo set, H, scheme, cost, conditioning): pooled delta, n, arms
  .perbook.csv    per-book deltas at every headline cell
  .null.csv       the WITHIN and BOOKLAB permutation bands at both permutation counts
  .wf.csv         rule-8 IS/OOS table on the tuned axes plus both KEEP paths per book
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_is-the-NEGATIVE-NEXT-WINDOW-sign-a-MEAN-REVERSION-fact-or-a-CONDITIONING-artefact_cloud.py
"""
from __future__ import annotations
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state, compare)                                        # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

DATE = "2026-09-12"
SLUG = "is-the-NEGATIVE-NEXT-WINDOW-sign-a-MEAN-REVERSION-fact-or-a-CONDITIONING-artefact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
COSTS = [0, 10, 25]
COST = 10
HORIZONS = [756, 1260]
SCHEMES = ["OVERLAP21", "CHAIN", "DISJOINT"]
N_OFFSETS = 12
CONDS = ["NONE", "OTHER3", "DDCAGR", "SHARPE"]          # P1
NPERMS = [1000, 10000]                                  # P2
HEAD_H, HEAD_SCHEME, HEAD_COND = 756, "DISJOINT", "NONE"
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
MAX_VOL, WARMUP = 0.60, 260
SEED = 8390
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 112 + f"\n{s}\n" + "=" * 112)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from idea 832's committed script (which copied them from
# 831/641/574/804), so the corpus is not silently redefined here.
# =====================================================================================
def comp_rank(px):
    s, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < MAX_VOL)
    return s.where(elig), elig


def topn_weights(px, n=20, gross=0.75, m=0, fixed=False):
    sc, elig = comp_rank(px)
    rank = sc.rank(axis=1, ascending=False)
    if m == 0:
        sel = (rank <= n).fillna(False)
    else:
        R, E = rank.values, elig.values
        held = np.zeros(px.shape[1], bool)
        out = np.zeros(px.shape, bool)
        for i in range(len(px)):
            r_i, e_i = R[i], E[i]
            ok = ~np.isnan(r_i)
            keep = held & e_i & ok & (r_i <= n + m)
            need = n - int(keep.sum())
            if need > 0:
                cand = np.where(e_i & ok & ~keep)[0]
                if len(cand):
                    cand = cand[np.argsort(r_i[cand])][:need]
                    keep[cand] = True
            held = keep
            out[i] = keep
        sel = pd.DataFrame(out, index=px.index, columns=px.columns)
    if fixed:
        return sel.astype(float).mul(gross / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(k, axis=0).mul(gross).fillna(0.0)


def band_ew_respread(px, band, gross):
    e = band_state(px, band).astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def ewall_weights(px, gross=1.00):
    _, elig = comp_rank(px)
    e = elig.astype(float).where(px.notna(), 0.0)
    k = e.sum(axis=1).replace(0, np.nan)
    return e.div(k, axis=0).mul(gross).fillna(0.0)


def shy_residual_weights(px, gross=0.375, sleeve="SHY"):
    W = ewall_weights(px.drop(columns=[sleeve]), gross).reindex(columns=px.columns).fillna(0.0)
    W[sleeve] = (1.0 - W.sum(axis=1)).clip(lower=0.0)
    return W


def breadth_gate_weights(px, gross=1.00, q=0.17, wroll=1008, depth=1.0, freq="W"):
    from engine import rebalance_mask
    core = px.drop(columns=["SPY"], errors="ignore")
    above = core > core.rolling(200).mean()
    breadth = above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)
    thr = breadth.rolling(wroll, min_periods=wroll).quantile(q)
    bad = (breadth < thr) & breadth.notna() & thr.notna()
    m = pd.Series(1.0, index=px.index).where(~bad, 1.0 - depth)
    mask = rebalance_mask(px.index, freq)
    m = m.where(mask).ffill().fillna(1.0)
    return ewall_weights(px, gross).mul(m, axis=0)


def ma_respread(px, gross=0.75):
    pm = px.notna()
    ma = (px > px.rolling(200).mean()) & pm
    k = ma.sum(axis=1).replace(0, np.nan)
    return gross * ma.astype(float).div(k, axis=0).fillna(0.0)


def ma_dist_tophalf(px, gross=0.75, q=0.50):
    pm = px.notna()
    dist = (px / px.rolling(200).mean() - 1.0).where(pm)
    rk = dist.rank(axis=1, ascending=False)
    n_priced = dist.notna().sum(axis=1)
    k = np.ceil(q * n_priced).replace(0, np.nan)
    sel = rk.le(k, axis=0).fillna(False) & dist.notna()
    kk = sel.sum(axis=1).replace(0, np.nan)
    return gross * sel.astype(float).div(kk, axis=0).fillna(0.0)


def r6_topn(px, n=20, gross=0.65):
    pm = px.notna()
    r6 = (px / px.shift(126) - 1.0).where(pm)
    rk = r6.rank(axis=1, ascending=False)
    return (rk <= n).astype(float) * (gross / n)


# (key, label, panel, weights_fn, cadence, published (CAGR, Sharpe, MaxDD), memo file)
CORPUS = [
    ("K1", "u56 top20 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 0), "W", (0.1279, 1.064, -0.1831),
     "2026-09-07_u56-top20-g075-4b_C_MEMO.md"),
    ("K2", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W", (None, None, None),
     "2026-09-07_u56-top20-band-m20_4b_B_MEMO.md"),
    ("K3", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D", (0.1171, 1.1454, -0.1237),
     "2026-09-06_daily-plus-buffer30_PARK_MEMO.md"),
    ("K4", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.0, 1.00), "M", (0.1196, 1.2126, -0.1549),
     "2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO.md"),
    ("K5", "u56 RULES v2 band 0.03, W, g1.00  [the standing candidate]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W", (0.1159, 1.2055, -0.1591),
     "2026-09-08_u56-band3-fullgross_KEEP_MEMO.md"),
    ("K6", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W", (0.1402, 1.2264, -0.1942),
     "2026-09-06_band12-ewall-rw_PARK_MEMO.md"),
    ("K7", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W", (0.0627, 1.1777, -0.1110),
     "2026-09-07_b136-ewall-shy-residual"),
    ("K8", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W", (0.1413, 1.2204, -0.1479),
     "2026-09-10_does-the-BREADTH-gate-4b-pass-live-only-at-gross-1.00_cloud.memo.md"),
    ("R1", "u56 band 0.08, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W", (0.1137, 1.1439, -0.1905),
     "2026-09-11_u56-band008-gross100_4b_cloud_MEMO.md"),
    ("R2", "u56 MA-RESPREAD, W, g0.75", "U56",
     lambda px: ma_respread(px, 0.75), "W", (0.1155, 1.0914, -0.1862),
     "2026-09-11_u56-marsrespread-gross075_4b_C_MEMO.md"),
    ("R3", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M", (0.1547, 1.2359, -0.1980),
     "2026-09-11_4b-candidate-U56-MA-DISTANCE-TOP-HALF-monthly_memo.md"),
    ("R4", "b136 R6-top20 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 20, 0.65), "W", (0.1499, 1.1264, -0.1943),
     "2026-09-12_b136-r620-gross065-W_4b_C_MEMO.md"),
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W", (0.0863, 1.202, -0.1205), "RULES.md v2"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56",
     rules_v1_weights, "W", (None, None, None), "RULES.md v1"),
]
KEYS = [c[0] for c in CORPUS]
MEMO8 = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
MEMO12 = MEMO8 + ["R1", "R2", "R3", "R4"]
MEMO_SETS = {"MEMO8": MEMO8, "MEMO12": MEMO12}
COMPARANDS = ["LIVE", "V1"]
HEAD_SET = "MEMO12"


# =====================================================================================
def w_metrics(r: np.ndarray):
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    sd = r.std(ddof=1)
    sharpe = (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan
    mdd = float(np.min(eq / np.maximum.accumulate(eq) - 1.0))
    return cagr, sharpe, mdd


def sharpe_of(r: np.ndarray):
    sd = r.std(ddof=1)
    return (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan


def legs_of(r: np.ndarray, sp: np.ndarray):
    """C2: the four window-local 4b legs, halves read at len//2 exactly as PROTOCOL does."""
    c, sh, dd = w_metrics(r)
    s_c, s_s, s_d = w_metrics(sp)
    h = len(r) // 2
    sub = bool(sharpe_of(r[:h]) > sharpe_of(sp[:h]) and sharpe_of(r[h:]) > sharpe_of(sp[h:]))
    return dict(CAGR=c, Sharpe=sh, MaxDD=dd, spy_CAGR=s_c, spy_Sharpe=s_s, spy_MaxDD=s_d,
                L_sharpe=bool(sh > s_s), L_sub=sub, L_dd=bool(dd >= 0.6 * s_d),
                L_cagr=bool(c >= 0.7 * s_c))


def build(panels, cost, verbose=False):
    books, meta = {}, {}
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        t0 = time.time()
        r = backtest(px, wf(px), cost_bps=cost, freq=freq)["returns"]
        books[key] = r
        meta[key] = dict(label=label, panel=pan, freq=freq, pub=pub, memo=memo)
        if verbose:
            P(f"  built {key:5s} {label:62s} panel {pan:5s} freq {freq}  ({time.time()-t0:.1f}s)")
    return books, meta


def gates_g1g2(books, meta, starts):
    hdr("GATES G1 / G2 — printed BEFORE any new number")
    rows = []
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        if pub[0] is None:
            rows.append(dict(gate=f"G1/{key}", pub_CAGR=np.nan, got_CAGR=np.nan,
                             pub_Sharpe=np.nan, got_Sharpe=np.nan, pub_MaxDD=np.nan,
                             got_MaxDD=np.nan, verdict="NO PUBLISHED TRIPLE"))
            continue
        gc, gs, gd = w_metrics(books[key].loc[starts[pan]:].values)
        ok = abs(gc - pub[0]) <= 0.010 and abs(gs - pub[1]) <= 0.060 and abs(gd - pub[2]) <= 0.020
        rows.append(dict(gate=f"G2/{key}" if key in COMPARANDS else f"G1/{key}",
                         pub_CAGR=pub[0], got_CAGR=gc, pub_Sharpe=pub[1], got_Sharpe=gs,
                         pub_MaxDD=pub[2], got_MaxDD=gd, verdict="PASS" if ok else "FAIL"))
    g = pd.DataFrame(rows)
    P(g.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    sc = g[g.verdict.isin(["PASS", "FAIL"])]
    P("Tolerance declared: |dCAGR|<=1.00pp, |dSharpe|<=0.060, |dMaxDD|<=2.00pp.")
    P(f"G1+G2: {(sc.verdict=='PASS').sum()} of {len(sc)} PASS "
      f"({len(g)-len(sc)} books publish no triple and are marked so).")
    return g


def gate_g3(books):
    rng = np.random.default_rng(SEED)
    worst = 0.0
    for _ in range(200):
        key = KEYS[rng.integers(len(KEYS))]
        r = books[key]
        T = int(rng.integers(252, 1261))
        i = int(rng.integers(0, len(r) - T))
        sl = r.iloc[i:i + T]
        a = w_metrics(sl.values)
        m = metrics(sl)
        worst = max(worst, max(abs(x - y) for x, y in
                               zip(a, (m["CAGR"], m["Sharpe"], m["MaxDD"]))))
    P(f"GATE G3 — vectorised window metrics vs engine.metrics on 200 fixed-seed random windows: "
      f"max |diff| = {worst:.3e} vs bar 1e-10 -> {'PASS' if worst <= 1e-10 else 'FAIL'}")
    return worst


# ----------------------------------------------------------------- the pair census
def pair_starts(i0, n, H, scheme, offset):
    """C7: return the (predictor_i, target_i) pairs of one (scheme, offset)."""
    if scheme == "OVERLAP21":
        idx = list(range(i0, n - 2 * H + 1, 21))
        return [(i, i + H) for i in idx]
    tiles = list(range(i0 + offset, n - H + 1, H))
    if scheme == "CHAIN":
        return [(tiles[j], tiles[j + 1]) for j in range(len(tiles) - 1)]
    return [(tiles[j], tiles[j + 1]) for j in range(0, len(tiles) - 1, 2)]   # DISJOINT


def census(books, meta, panels, starts, cost_tag=COST):
    rows = []
    spy = {pan: px["SPY"].pct_change().fillna(0.0).values for pan, px in panels.items()}
    for key in MEMO12:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key].values, spy[pan]
        cache: dict[int, dict] = {}

        def legs_at(i, H):
            k = (i, H)
            if k not in cache:
                cache[k] = legs_of(r_all[i:i + H], s_all[i:i + H])
            return cache[k]

        for H in HORIZONS:
            offs = [int(round(o)) for o in np.linspace(0, H, N_OFFSETS, endpoint=False)]
            for scheme in SCHEMES:
                for off in ([0] if scheme == "OVERLAP21" else offs):
                    for (a, b) in pair_starts(i0, len(r_all), H, scheme, off):
                        la, lb = legs_at(a, H), legs_at(b, H)
                        rows.append(dict(
                            book=key, panel=pan, H=H, scheme=scheme, offset=off, cost=cost_tag,
                            a_i=a, b_i=b, a_entry=idx[a], a_end=idx[a + H - 1],
                            b_entry=idx[b], b_end=idx[b + H - 1],
                            a_sharpe=la["L_sharpe"], a_sub=la["L_sub"], a_dd=la["L_dd"],
                            a_cagr=la["L_cagr"],
                            a_dSharpe=la["Sharpe"] - la["spy_Sharpe"],
                            b_pass=bool(lb["L_sharpe"] and lb["L_sub"] and lb["L_dd"]
                                        and lb["L_cagr"]),
                            b_dSharpe=lb["Sharpe"] - lb["spy_Sharpe"]))
    C = pd.DataFrame(rows)
    C["a_other3"] = C.a_sharpe & C.a_dd & C.a_cagr
    C["a_ddcagr"] = C.a_dd & C.a_cagr
    return C


COND_MASK = {
    "NONE": lambda c: pd.Series(True, index=c.index),
    "OTHER3": lambda c: c.a_other3,
    "DDCAGR": lambda c: c.a_ddcagr,
    "SHARPE": lambda c: c.a_sharpe,
}


def delta_of(sub: pd.DataFrame):
    """C9.  Returns (delta, n, n_pass_arm, p_pass, p_fail)."""
    if not len(sub):
        return np.nan, 0, 0, np.nan, np.nan
    hp, hf = sub[sub.a_sub], sub[~sub.a_sub]
    p_a = hp.b_pass.mean() if len(hp) else np.nan
    p_b = hf.b_pass.mean() if len(hf) else np.nan
    d = p_a - p_b if np.isfinite(p_a) and np.isfinite(p_b) else np.nan
    return d, len(sub), len(hp), p_a, p_b


def grid_of(C):
    out = []
    for cost in sorted(C.cost.unique()):
        for set_name, keys in MEMO_SETS.items():
            for H in HORIZONS:
                for scheme in SCHEMES:
                    base = C[(C.cost == cost) & (C.book.isin(keys)) & (C.H == H) &
                             (C.scheme == scheme)]
                    for cond in CONDS:
                        sub = base[COND_MASK[cond](base)]
                        d, n, nhp, pa, pb = delta_of(sub)
                        ds, ns = [], []
                        for _, sk in sub.groupby("book"):
                            dk, nk = delta_of(sk)[:2]
                            if np.isfinite(dk):
                                ds.append(dk)
                                ns.append(nk)
                        if ds:
                            ds_, ns_ = np.array(ds), np.array(ns, dtype=float)
                            wmean = float((ds_ * ns_).sum() / ns_.sum())
                            emean = float(ds_.mean())
                            nneg = int((ds_ < 0).sum())
                            ndef = len(ds_)
                        else:
                            wmean = emean = np.nan
                            nneg = ndef = 0
                        out.append(dict(cost=cost, memo_set=set_name, H=H, scheme=scheme,
                                        cond=cond, n_pairs=n, n_halvesPASS=nhp,
                                        p_next_given_PASS=pa, p_next_given_FAIL=pb, delta=d,
                                        within_wmean=wmean, within_emean=emean,
                                        simpson=d - wmean if np.isfinite(wmean) else np.nan,
                                        n_books_def=ndef, n_books_neg=nneg,
                                        base_rate=float(sub.b_pass.mean()) if len(sub) else
                                        np.nan))
    return pd.DataFrame(out)


# ----------------------------------------------------------------- the nulls (C10)
def nulls(C, cells, nperm_list=NPERMS):
    hdr("THE NULLS (C10) — WITHIN-book verdict permutation and BOOK-LABEL permutation")
    rows = []
    for (H, scheme, cond, set_name) in cells:
        sub = C[(C.cost == COST) & (C.book.isin(MEMO_SETS[set_name])) & (C.H == H) &
                (C.scheme == scheme)]
        sub = sub[COND_MASK[cond](sub)]
        if not len(sub):
            continue
        d_obs, n, _, _, _ = delta_of(sub)
        bk = sub.book.values
        sub_ = sub.reset_index(drop=True)
        # observed per-book mean delta (equal weight over books with a defined delta)
        pbd = [delta_of(sk)[0] for _, sk in sub_.groupby("book")]
        pbd = [x for x in pbd if np.isfinite(x)]
        em_obs = float(np.mean(pbd)) if pbd else np.nan
        for nperm in nperm_list:
            rng = np.random.default_rng(SEED + nperm)
            hs, bp = sub_.a_sub.values.copy(), sub_.b_pass.values
            dd = np.empty(nperm)
            ee = np.empty(nperm)
            order = {b: np.where(bk == b)[0] for b in np.unique(bk)}
            for t in range(nperm):
                # WITHIN: permute the halves verdict inside each book
                h2 = hs.copy()
                for b, ix in order.items():
                    h2[ix] = rng.permutation(hs[ix])
                a, f = bp[h2], bp[~h2]
                dd[t] = (a.mean() if len(a) else np.nan) - (f.mean() if len(f) else np.nan)
                # BOOKLAB: permute book labels across pairs, keeping book sizes
                lab = rng.permutation(bk)
                ds = []
                for b in np.unique(lab):
                    m = lab == b
                    aa, ff = bp[m & hs], bp[m & ~hs]
                    if len(aa) and len(ff):
                        ds.append(aa.mean() - ff.mean())
                ee[t] = float(np.mean(ds)) if ds else np.nan
            lo, hi = np.nanquantile(dd, [0.025, 0.975])
            elo, ehi = np.nanquantile(ee, [0.025, 0.975])
            p_within = float(np.nanmean(np.abs(dd) >= abs(d_obs)))
            p_book = float(np.nanmean(np.abs(ee) >= abs(em_obs))) if np.isfinite(em_obs) else \
                np.nan
            rows.append(dict(H=H, scheme=scheme, cond=cond, memo_set=set_name, n_pairs=n,
                             nperm=nperm, delta_obs=d_obs, within_lo=lo, within_hi=hi,
                             p_within=p_within, outside_within=bool(d_obs < lo or d_obs > hi),
                             emean_obs=em_obs, book_lo=elo, book_hi=ehi, p_booklab=p_book,
                             outside_booklab=bool(np.isfinite(em_obs) and
                                                  (em_obs < elo or em_obs > ehi))))
    N = pd.DataFrame(rows)
    P(N.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\nwithin_lo/hi = two-sided 95% band of the POOLED delta when the predictor's halves "
      "verdict is permuted INSIDE each book (book sizes and marginals preserved).")
    P("book_lo/hi   = two-sided 95% band of the EQUAL-WEIGHT MEAN of per-book deltas when the "
      "BOOK LABEL is permuted across pairs (the queue's null).")
    N.to_csv(f"{OUT}.null.csv", index=False)
    return N


def gate_g6(C):
    """BOOKLAB leaves the POOLED delta exactly invariant — by construction."""
    sub = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.H == HEAD_H) &
            (C.scheme == HEAD_SCHEME)]
    d0 = delta_of(sub)[0]
    rng = np.random.default_rng(SEED)
    worst = 0.0
    for _ in range(100):
        s2 = sub.copy()
        s2["book"] = rng.permutation(s2.book.values)
        worst = max(worst, abs(delta_of(s2)[0] - d0))
    P(f"GATE G6 — BOOKLAB leaves the POOLED delta invariant over 100 draws: max |d| = "
      f"{worst:.3e} (pooled delta {d0:+.4f}).  This is BY CONSTRUCTION: the pooled statistic "
      f"never reads a label, so a book-label null can only be run on a LABEL-USING statistic "
      f"(here the equal-weight mean of per-book deltas).")
    return worst


# ----------------------------------------------------------------- fixed window + KEEP paths
def fixed_window(books, meta, panels, starts):
    hdr("RULE 8 MANDATED BOOK LEG + BOTH KEEP PATHS (fixed window and OOS 2017-01-01..)")
    rows = []
    for key in KEYS + ["SPY_U56", "SPY_B136"]:
        if key.startswith("SPY_"):
            pan = key.split("_")[1]
            r_all = panels[pan]["SPY"].pct_change().fillna(0.0)
        else:
            pan = meta[key]["panel"]
            r_all = books[key]
        f, o = r_all.loc[starts[pan]:], r_all.loc[OOS_START:]
        fc, fs, fd = w_metrics(f.values)
        oc, os_, od = w_metrics(o.values)
        hf, ho = len(f) // 2, len(o) // 2
        rows.append(dict(book=key, panel=pan, full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                         full_H1=sharpe_of(f.values[:hf]), full_H2=sharpe_of(f.values[hf:]),
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                         OOS_H1=sharpe_of(o.values[:ho]), OOS_H2=sharpe_of(o.values[ho:])))
    t = pd.DataFrame(rows).set_index("book")
    P(t.to_string(float_format=lambda x: f"{x:+.4f}"))
    lv = t.loc["LIVE"]
    out = []
    for key in MEMO12:
        r = t.loc[key]
        spy = t.loc[f"SPY_{meta[key]['panel']}"]
        legs4b = {"H1>SPY": r.full_H1 > spy.full_H1, "H2>SPY": r.full_H2 > spy.full_H2,
                  "OOS_Sharpe>SPY": r.OOS_Sharpe > spy.OOS_Sharpe,
                  "DD<=60%SPY": r.full_MaxDD >= 0.6 * spy.full_MaxDD,
                  "CAGR>=70%SPY": r.full_CAGR >= 0.7 * spy.full_CAGR}
        legs4a = {"H1>LIVE": r.full_H1 > lv.full_H1, "H2>LIVE": r.full_H2 > lv.full_H2,
                  "DD<=LIVE": r.full_MaxDD >= lv.full_MaxDD}
        legs4bo = {"OOS_H1>SPY": r.OOS_H1 > spy.OOS_H1, "OOS_H2>SPY": r.OOS_H2 > spy.OOS_H2,
                   "OOS_Sharpe>SPY": r.OOS_Sharpe > spy.OOS_Sharpe,
                   "OOS_DD<=60%SPY": r.OOS_MaxDD >= 0.6 * spy.OOS_MaxDD,
                   "OOS_CAGR>=70%SPY": r.OOS_CAGR >= 0.7 * spy.OOS_CAGR}
        out.append(dict(book=key, keep4a="PASS" if all(legs4a.values()) else "FAIL",
                        fail4a="+".join(k for k, v in legs4a.items() if not v),
                        keep4b="PASS" if all(legs4b.values()) else "FAIL",
                        fail4b="+".join(k for k, v in legs4b.items() if not v),
                        keep4b_OOS="PASS" if all(legs4bo.values()) else "FAIL",
                        fail4b_OOS="+".join(k for k, v in legs4bo.items() if not v)))
    K = pd.DataFrame(out).set_index("book")
    P("\n" + K.to_string())
    P(f"\nfixed window: 4a {int((K.keep4a=='PASS').sum())} of {len(MEMO12)} PASS, "
      f"4b {int((K.keep4b=='PASS').sum())} of {len(MEMO12)} PASS; "
      f"OOS-only 4b {int((K.keep4b_OOS=='PASS').sum())} of {len(MEMO12)} PASS.")
    return t, K


def rule8(C, t):
    hdr("RULE 8 (a) — ON THIS RUN'S OWN TUNED AXIS (conditioning x H): chosen on IS pairs only")
    base = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.scheme == HEAD_SCHEME)]
    rows = []
    for cond in CONDS:
        for H in HORIZONS:
            s = base[(base.H == H)]
            s = s[COND_MASK[cond](s)]
            is_ = s[s.b_end <= IS_END]
            oos = s[s.a_entry >= OOS_START]
            di, ni = delta_of(is_)[:2]
            do, no = delta_of(oos)[:2]
            rows.append(dict(cond=cond, H=H, n_IS=ni, IS_delta=di, n_OOS=no, OOS_delta=do))
    W = pd.DataFrame(rows)
    P(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    v = W.dropna(subset=["IS_delta"])
    pick = gap = obest = None
    if len(v):
        best = v.sort_values("IS_delta").iloc[0]            # most NEGATIVE on IS
        pick = (best["cond"], int(best.H))
        vo = W.dropna(subset=["OOS_delta"])
        if len(vo):
            ob = vo.sort_values("OOS_delta").iloc[0]
            obest = (ob["cond"], int(ob.H))
            gap = abs(best.OOS_delta - best.IS_delta) if np.isfinite(best.OOS_delta) else np.nan
        P(f"\nIS pick (most negative delta on IS pairs): {pick} at {best.IS_delta:+.4f} "
          f"(n={int(best.n_IS)}) -> OOS {best.OOS_delta:+.4f} (n={int(best.n_OOS)}), "
          f"gap {gap if gap is None else f'{gap:.4f}'} vs bar 0.10.  OOS-most-negative cell: "
          f"{obest}.")
    W.to_csv(f"{OUT}.wf.csv", index=False)
    return W, pick, gap, obest


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P(f"# {DATE} cloud lane — IDEA 839: is the NEGATIVE NEXT-WINDOW sign a MEAN-REVERSION fact")
    P("#                  or a CONDITIONING artefact?")
    P("=" * 112)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C4)")
    P(f"next-day execution, no shorting, no leverage.  P1 conditioning {CONDS} | "
      f"P2 permutation count {NPERMS} | H {HORIZONS}, scheme {SCHEMES}, {N_OFFSETS} tiling "
      f"offsets, cost {COSTS} bps and memo set {list(MEMO_SETS)} reported.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-corpus conditional "
      "contrast, which survivorship does not cancel out of.")

    P("\nbuilding books at the PROTOCOL rung (one full-sample simulation each, C1):")
    books, meta = build(panels, COST, verbose=True)
    gates_g1g2(books, meta, starts)
    gate_g3(books)

    bt, K = fixed_window(books, meta, panels, starts)
    bt.to_csv(f"{OUT}.books.csv")

    hdr("THE PAIR CENSUS")
    Cs = [census(books, meta, panels, starts, COST)]
    for c in COSTS:
        if c == COST:
            continue
        P(f"  re-building every book at {c} bps for the reported cost rung ...")
        bk, _ = build(panels, c)
        Cs.append(census(bk, meta, panels, starts, c))
    C = pd.concat(Cs, ignore_index=True)
    C.to_csv(f"{OUT}.pairs.csv.gz", index=False, compression="gzip")
    P(f"{len(C):,} (book, H, scheme, offset, cost, pair) rows over {len(MEMO12)} books.")

    # GATE G5 — DISJOINT tilings really are disjoint, each window used once
    bad = 0
    for (key, H, off), s in C[(C.cost == COST) & (C.scheme == "DISJOINT")].groupby(
            ["book", "H", "offset"]):
        ivs = sorted(list(s.a_i) + list(s.b_i))
        bad += sum(1 for a, b in zip(ivs, ivs[1:]) if b < a + H)
        bad += len(ivs) - len(set(ivs))
    P(f"GATE G5 — DISJOINT tilings: {bad} overlapping-or-reused windows over all "
      f"(book, H, offset) tilings -> {'PASS' if bad == 0 else 'FAIL'}")

    # GATE G4 — reproduce idea 832's committed H_INFO cell
    hdr("GATE G4 — reproduce idea 832's committed H_INFO numbers (OVERLAP21, OTHER3)")
    g4rows = []
    want = {756: (627, 0.3182, 0.3810, -0.0628), 1260: (419, 0.7072, 0.7838, -0.0765)}
    okg4 = True
    for H, (wn, wa, wb, wd) in want.items():
        s = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.H == H) &
              (C.scheme == "OVERLAP21")]
        s = s[s.a_other3]
        d, n, nhp, pa, pb = delta_of(s)
        ok = (n == wn and abs(pa - wa) <= 5e-4 and abs(pb - wb) <= 5e-4
              and abs(d - wd) <= 5e-4)
        okg4 &= ok
        g4rows.append(dict(H=H, got_n=n, want_n=wn, got_pPASS=pa, want_pPASS=wa,
                           got_pFAIL=pb, want_pFAIL=wb, got_delta=d, want_delta=wd,
                           verdict="PASS" if ok else "FAIL"))
    P(pd.DataFrame(g4rows).to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"GATE G4 -> {'PASS' if okg4 else 'FAIL'} (bars: exact n, |dP| <= 5e-4)")
    gate_g6(C)

    # ---------------------------------------------------------------- the grid
    G = grid_of(C)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    hdr("THE GRID — pooled delta at every (memo set x H x scheme x conditioning), 10 bps")
    P(G[(G.cost == COST)][["memo_set", "H", "scheme", "cond", "n_pairs", "n_halvesPASS",
                           "base_rate", "p_next_given_PASS", "p_next_given_FAIL", "delta",
                           "within_wmean", "simpson", "n_books_neg", "n_books_def"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\ndelta        = P(next window PASSes 4b | halves PASS) - P(. | halves FAIL)")
    P("within_wmean = the same delta computed INSIDE each book and pair-weighted across books")
    P("simpson      = delta - within_wmean, i.e. the part of the pooled number that is "
      "BETWEEN-book composition rather than a within-book relation")
    P(f"\n--- the same table at 0 and 25 bps ({HEAD_SET}, reported not selected) ---")
    P(G[(G.cost != COST) & (G.memo_set == HEAD_SET)][
        ["cost", "H", "scheme", "cond", "n_pairs", "delta", "within_wmean", "simpson",
         "n_books_neg", "n_books_def"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ---------------------------------------------------------------- offset spread
    hdr("OFFSET SPREAD — the DISJOINT delta re-computed at each of the 12 tilings")
    osp = []
    for H in HORIZONS:
        for cond in CONDS:
            s = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.H == H) &
                  (C.scheme == "DISJOINT")]
            s = s[COND_MASK[cond](s)]
            ds = []
            for off, so in s.groupby("offset"):
                ds.append(delta_of(so)[0])
            ds = np.array(ds, dtype=float)
            osp.append(dict(H=H, cond=cond, n_offsets=len(ds),
                            n_defined=int(np.isfinite(ds).sum()),
                            pooled=delta_of(s)[0], min=np.nanmin(ds), median=np.nanmedian(ds),
                            max=np.nanmax(ds), n_neg=int((ds[np.isfinite(ds)] < 0).sum())))
    OS = pd.DataFrame(osp)
    P(OS.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("Offsets are NOT independent draws — they are the same data re-tiled — so this is a "
      "sensitivity SPREAD, not a confidence interval.")

    # ---------------------------------------------------------------- per book
    hdr("PER-BOOK DELTAS at the headline cell and at idea 832's own cell")
    pbrows = []
    for (H, scheme, cond) in [(HEAD_H, HEAD_SCHEME, HEAD_COND), (HEAD_H, HEAD_SCHEME, "OTHER3"),
                              (HEAD_H, "OVERLAP21", "OTHER3"), (1260, HEAD_SCHEME, HEAD_COND)]:
        s = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.H == H) & (C.scheme == scheme)]
        s = s[COND_MASK[cond](s)]
        for key, sk in s.groupby("book"):
            d, n, nhp, pa, pb = delta_of(sk)
            pbrows.append(dict(cell=f"{scheme}/H{H}/{cond}", book=key, n=n, n_hp=nhp,
                               p_pass=pa, p_fail=pb, delta=d))
    PB = pd.DataFrame(pbrows)
    PB.to_csv(f"{OUT}.perbook.csv", index=False)
    for cell, s in PB.groupby("cell", sort=False):
        d = s.dropna(subset=["delta"])
        P(f"\n--- {cell} ---")
        P(s.set_index("book")[["n", "n_hp", "p_pass", "p_fail", "delta"]]
          .to_string(float_format=lambda x: f"{x:+.4f}"))
        P(f"  {len(d)} of {len(s)} books have a defined delta; {int((d.delta<0).sum())} "
          f"negative, {int((d.delta>0).sum())} positive, {int((d.delta==0).sum())} exactly zero. "
          f"equal-weight mean {d.delta.mean():+.4f}, median {d.delta.median():+.4f}.")

    # ---------------------------------------------------------------- nulls
    cells = [(HEAD_H, HEAD_SCHEME, HEAD_COND, HEAD_SET), (HEAD_H, HEAD_SCHEME, "OTHER3", HEAD_SET),
             (HEAD_H, "OVERLAP21", "OTHER3", HEAD_SET), (HEAD_H, "OVERLAP21", "NONE", HEAD_SET),
             (HEAD_H, "CHAIN", "NONE", HEAD_SET), (1260, HEAD_SCHEME, HEAD_COND, HEAD_SET)]
    N = nulls(C, cells)

    W, pick, gap, obest = rule8(C, bt)

    # ---------------------------------------------------------------- hypotheses
    hdr("PRE-REGISTERED HYPOTHESES")
    gh = G[(G.cost == COST) & (G.memo_set == HEAD_SET)]

    def cell(H, scheme, cond):
        r = gh[(gh.H == H) & (gh.scheme == scheme) & (gh.cond == cond)]
        return r.iloc[0] if len(r) else None

    verd = {}
    g4pass = all(r["verdict"] == "PASS" for r in g4rows)
    verd["H_REPRO"] = (g4pass, "; ".join(
        f"H={r['H']}: n {r['got_n']} vs {r['want_n']}, delta {r['got_delta']:+.4f} vs "
        f"{r['want_delta']:+.4f}" for r in g4rows))
    hd = cell(HEAD_H, HEAD_SCHEME, HEAD_COND)
    verd["H_SURVIVE"] = (bool(np.isfinite(hd.delta) and hd.delta < 0),
                         f"DISJOINT / H=756 / NONE pooled delta = {hd.delta:+.4f} on "
                         f"{int(hd.n_pairs)} pairs (base rate {hd.base_rate:.4f})")
    cn, co = cell(HEAD_H, "OVERLAP21", "NONE"), cell(HEAD_H, "OVERLAP21", "OTHER3")
    verd["H_COND"] = (abs(cn.delta) < 0.5 * abs(co.delta),
                      f"OVERLAP21 H=756: delta(NONE) {cn.delta:+.4f} on {int(cn.n_pairs)} pairs "
                      f"vs delta(OTHER3) {co.delta:+.4f} on {int(co.n_pairs)} — ratio "
                      f"{abs(cn.delta)/abs(co.delta):.3f} vs bar 0.5")
    nh = N[(N.H == HEAD_H) & (N.scheme == HEAD_SCHEME) & (N.cond == HEAD_COND) &
           (N.nperm == max(NPERMS))]
    if len(nh):
        r = nh.iloc[0]
        verd["H_WITHIN"] = (bool(r.outside_within),
                            f"pooled {r.delta_obs:+.4f} vs WITHIN band "
                            f"[{r.within_lo:+.4f}, {r.within_hi:+.4f}], p = {r.p_within:.4f} "
                            f"({max(NPERMS):,} perms)")
        verd["H_BOOKLAB"] = (bool(r.outside_booklab),
                             f"mean per-book delta {r.emean_obs:+.4f} vs BOOKLAB band "
                             f"[{r.book_lo:+.4f}, {r.book_hi:+.4f}], p = {r.p_booklab:.4f}")
    else:
        verd["H_WITHIN"] = (False, "cell empty")
        verd["H_BOOKLAB"] = (False, "cell empty")
    cs = cell(HEAD_H, "OVERLAP21", "OTHER3")
    verd["H_SIMPSON"] = (bool(np.isfinite(cs.simpson) and abs(cs.simpson) <= 0.05
                              and np.sign(cs.within_wmean) == np.sign(cs.delta)),
                         f"pooled {cs.delta:+.4f} vs pair-weighted within-book mean "
                         f"{cs.within_wmean:+.4f}; composition part {cs.simpson:+.4f} vs bar "
                         f"0.05")
    verd["H_BOOKS"] = (int(hd.n_books_neg) >= 9,
                       f"{int(hd.n_books_neg)} of {int(hd.n_books_def)} books with a defined "
                       f"delta are negative at DISJOINT / H=756 / NONE vs bar 9")
    verd["H_WF"] = (pick is not None and obest is not None and pick == obest
                    and gap is not None and np.isfinite(gap) and gap <= 0.10,
                    f"IS pick {pick}, OOS-most-negative {obest}, gap "
                    f"{'n/a' if gap is None or not np.isfinite(gap) else f'{gap:.4f}'} "
                    f"vs bar 0.10")
    for k, (ok, why) in verd.items():
        P(f"  {k:10s} {'PASS' if ok else 'FAIL'}  — {why}")
    P(f"\n{sum(1 for v in verd.values() if v[0])} of {len(verd)} pre-registered hypotheses PASS.")

    # ---------------------------------------------------------------- PROTOCOL rule 3
    hdr("PROTOCOL rule 3 — baseline.compare on the standing candidate and the OOS-best book")
    for key in ["K5", "K8"]:
        wfun = dict((c[0], c[3]) for c in CORPUS)[key]
        fr = dict((c[0], c[4]) for c in CORPUS)[key]
        P(f"\n--- {key}: {meta[key]['label']} ---")
        res = compare(f"839 cloud {key} {meta[key]['label']}", wfun,
                      panels[meta[key]["panel"]], freq=fr, cost_bps=COST)
        LOG.append(str(res["table"]))

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return C, G, N, PB, W, verd


if __name__ == "__main__":
    main()
