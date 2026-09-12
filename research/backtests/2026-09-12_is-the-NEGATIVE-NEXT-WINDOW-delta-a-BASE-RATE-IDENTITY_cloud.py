#!/usr/bin/env python3
"""Idea 842 (cloud lane, 2026-09-12) — is the NEGATIVE NEXT-WINDOW delta a BASE-RATE IDENTITY?

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 839 measured
    delta = P(next window passes 4b | this window's halves leg PASSES)
          - P(next window passes 4b | this window's halves leg FAILS)
and found it NEGATIVE at 48 of 48 cells at the PROTOCOL 10 bps rung (head cells -0.1620
DISJOINT/756/NONE, -0.1067 OVERLAP21/756/NONE, median of the 48 = -0.1273 -- the queue's
"-0.15"), while its BOOK-LABEL-permuted null was MORE negative than the real labels.  That is
the signature of a pure SELECTION / base-rate structure rather than any statement about a book:
windows whose halves leg passes are drawn disproportionately from books with LOW 4b pass rates.

THIS RUN DERIVES THE NO-INFORMATION DELTA IN CLOSED FORM AND MEASURES ITS SHARE.  For a cell
with books k, pair counts n_k, halves-PASS shares s_k and per-book 4b base rates b_k, write
    w_k^P = n_k s_k / SUM_j n_j s_j        w_k^F = n_k (1-s_k) / SUM_j n_j (1-s_j)
A generator in which the next window's verdict is INDEPENDENT of the halves verdict WITHIN every
book, but keeps every n_k, s_k and b_k, produces
    delta_NOINFO = SUM_k w_k^P b_k - SUM_k w_k^F b_k                                        (1)
and, because b_k = s_k p_k^P + (1-s_k) p_k^F identically,
    delta_REAL - delta_NOINFO = SUM_k [ w_k^P (1-s_k) + w_k^F s_k ] d_k ,  d_k = p_k^P - p_k^F (2)
(2) is an EXACT algebraic decomposition, not an approximation: the pooled delta is the sum of a
BASE-RATE term that carries no within-book information and a strictly positively weighted sum of
the per-book deltas.  Books with s_k in {0,1} get weight 0 and drop out, which is the right
behaviour -- their d_k is undefined.  G5 checks (2) to 1e-12 at every cell.
SHARE = delta_NOINFO / delta_REAL is the deliverable the queue asks for.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  GENERATOR    -- ANALYTIC  : the closed form (1), deterministic.
                      BERNOULLI : per pair, y ~ Bern(b_hat_k) i.i.d., observed s_i kept.
                      HYPERGEOM : permute the observed y within each book (exact conditional;
                                  preserves n_k, s_k and b_k exactly).
  P2  BASE-RATE ESTIMATOR -- RAW (cell mean per book) / LOO (leave-the-pair-out) /
                      SHRUNK (empirical-Bayes beta-binomial shrink to the cell's grand mean).
All 9 (P1 x P2) cells are reported.  DECLARED DEGENERACY: HYPERGEOM resamples the observed
labels, so it cannot read an estimator -- its three estimator cells are IDENTICAL by
construction and are printed as such rather than silently deduplicated.
Horizon H {756, 1260}, entry scheme {OVERLAP21, CHAIN, DISJOINT}, 12 tiling offsets,
conditioning {NONE, OTHER3, DDCAGR, SHARPE}, cost {0, 10, 25} bps and memo set
{MEMO8, MEMO12} are REPORTED AT ALL 144 CELLS, not selected.  No book dial is tuned: every book
runs at the gross, band, n and cadence its own committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C8 copied verbatim from ideas 831/832/839 so the
four censuses are directly comparable; C9-C12 are this run's own):
  C1  one full-sample simulation per book per cost rung; every window is a slice of it.
  C2  the four 4b legs are read WINDOW-LOCAL against the same window's SPY: Sharpe > SPY,
      both halves (at len//2) > SPY's halves, MaxDD >= 0.6 * SPY MaxDD, CAGR >= 0.7 * SPY CAGR.
  C3  "passes 4b" = all four legs.
  C4  scoring starts at trading day 260 of each panel (200d MA + 252d momentum warm-up).
  C5  next-day execution, 10 bps per unit turnover at the PROTOCOL rung; 0 and 25 reported.
  C6  no shorting, no leverage; each book keeps its published gross.
  C7  pair schemes: OVERLAP21 = predictor entries every 21 trading days, target = entry + H;
      CHAIN = contiguous H-tiles, consecutive tiles paired (each window in <=2 pairs);
      DISJOINT = contiguous H-tiles, paired 2-by-2 (each window used exactly once).
  C8  delta is pooled over books and offsets unless the table says per-book.
  C9  b_hat_k is estimated INSIDE the cell being decomposed -- never from the pooled corpus --
      so the no-information prediction uses no information the cell does not contain.
  C10 a book contributes to a cell only if it has >=1 pair there; a book with s_k in {0,1}
      contributes to delta_NOINFO but carries zero weight in the within term.
  C11 Monte-Carlo generators use 2,000 draws at a fixed seed; bands are [p2.5, p97.5] and the
      p-value is the two-sided share of draws at least as extreme as delta_REAL.
  C12 rule 8 splits PAIRS, not books: IS = predictor window ENDS <= 2016-12-31,
      OOS = predictor window ENTRY >= 2017-01-01.  Nothing between the two is scored twice.

PRE-REGISTERED HYPOTHESES (written before the run; a FAIL is the result, not a reason to retune):
  H_ID     the delta is a base-rate identity if SHARE >= 0.80 at the head cell.
  H_CONTENT the delta is content if SHARE <= 0.20 at the head cell.
  H_UNIV   whatever the head cell says holds if the SAME verdict holds at >= 80% of the 48
           negative 10-bps cells.
  H_EST    the answer is estimator-free if max-min SHARE over the 3 estimators <= 0.10.
  H_WF     the (generator, estimator) chosen on IS pairs reproduces its IS share on OOS pairs
           to within 0.20.
  H_POWER  the decomposition is not vacuous: an INJECTED within-book delta of +0.20 is
           recovered by (2) to within 0.01.

SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so every
LEVEL below is optimistic.  The object here is a within-corpus conditional contrast and its
algebraic decomposition, which survivorship does not cancel out of.
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
SLUG = "is-the-NEGATIVE-NEXT-WINDOW-delta-a-BASE-RATE-IDENTITY"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
COSTS = [0, 10, 25]
COST = 10
HORIZONS = [756, 1260]
SCHEMES = ["OVERLAP21", "CHAIN", "DISJOINT"]
N_OFFSETS = 12
CONDS = ["NONE", "OTHER3", "DDCAGR", "SHARPE"]
GENS = ["ANALYTIC", "BERNOULLI", "HYPERGEOM"]          # P1
ESTS = ["RAW", "LOO", "SHRUNK"]                        # P2
NDRAW = 2000                                           # C11
HEAD_H, HEAD_SCHEME, HEAD_COND, HEAD_SET = 756, "DISJOINT", "NONE", "MEMO12"
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
MAX_VOL, WARMUP = 0.60, 260
SEED = 8420
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 112 + f"\n{s}\n" + "=" * 112)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from idea 839's committed script (which copied them from
# 832/831/641/574/804), so the corpus is not silently redefined here.
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
    hdr("GATES G1 / G2 — the corpus reproduces its own committed triples (before any new number)")
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


# ----------------------------------------------------------------- the pair census (C7)
def pair_starts(i0, n, H, scheme, offset):
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
        cache: dict[tuple, dict] = {}

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
                            b_pass=bool(lb["L_sharpe"] and lb["L_sub"] and lb["L_dd"]
                                        and lb["L_cagr"])))
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
    if not len(sub):
        return np.nan, 0, 0, np.nan, np.nan
    hp, hf = sub[sub.a_sub], sub[~sub.a_sub]
    p_a = hp.b_pass.mean() if len(hp) else np.nan
    p_b = hf.b_pass.mean() if len(hf) else np.nan
    d = p_a - p_b if np.isfinite(p_a) and np.isfinite(p_b) else np.nan
    return d, len(sub), len(hp), p_a, p_b


# ============================== THE NO-INFORMATION GENERATOR ==========================
def per_book(sub: pd.DataFrame):
    """n_k, s_k, b_k, p_k^P, p_k^F, d_k for every book present in the cell (C10)."""
    g = sub.groupby("book")
    t = pd.DataFrame(dict(n=g.size(), s=g.a_sub.mean(), b=g.b_pass.mean()))
    t["nP"] = g.apply(lambda x: int(x.a_sub.sum()), include_groups=False)
    t["nF"] = t.n - t.nP
    t["pP"] = g.apply(lambda x: x.b_pass[x.a_sub].mean() if x.a_sub.any() else np.nan,
                      include_groups=False)
    t["pF"] = g.apply(lambda x: x.b_pass[~x.a_sub].mean() if (~x.a_sub).any() else np.nan,
                      include_groups=False)
    t["d"] = t.pP - t.pF
    return t


def shrink_m0(t: pd.DataFrame):
    """Beta-binomial method-of-moments prior weight m0 from the cell's own between-book spread
    (C9).  Returns 0.0 when the books' base rates are not over-dispersed (nothing to shrink to)
    and +inf-equivalent (a large finite cap) when they are indistinguishable."""
    w = t.n.values.astype(float)
    b = t.b.values.astype(float)
    ok = np.isfinite(b) & (w > 0)
    if ok.sum() < 2:
        return 0.0
    w, b = w[ok], b[ok]
    gm = float((w * b).sum() / w.sum())
    if gm <= 0.0 or gm >= 1.0:
        return 0.0
    # observed weighted variance of the per-book rates vs the binomial-sampling part
    vobs = float((w * (b - gm) ** 2).sum() / w.sum())
    vsamp = float(gm * (1.0 - gm) * (w.size / w.sum()))        # mean 1/n_k, weighted
    vsig = vobs - vsamp
    if vsig <= 1e-12:
        return 1e6                                            # no real spread -> shrink hard
    m0 = gm * (1.0 - gm) / vsig - 1.0
    return float(np.clip(m0, 0.0, 1e6))


def bhat_per_pair(sub: pd.DataFrame, t: pd.DataFrame, est: str):
    """b_hat for every PAIR under estimator `est` (P2)."""
    n = sub.book.map(t.n).values.astype(float)
    b = sub.book.map(t.b).values.astype(float)
    y = sub.b_pass.values.astype(float)
    if est == "RAW":
        return b
    if est == "LOO":
        out = np.where(n > 1, (n * b - y) / np.maximum(n - 1.0, 1.0), b)
        return out
    if est == "SHRUNK":
        m0 = shrink_m0(t)
        w = t.n.values.astype(float)
        bb = t.b.values.astype(float)
        ok = np.isfinite(bb)
        gm = float((w[ok] * bb[ok]).sum() / w[ok].sum()) if ok.any() else np.nan
        return (n * b + m0 * gm) / (n + m0)
    raise ValueError(est)


def noinfo_delta(sub: pd.DataFrame, t: pd.DataFrame, est: str):
    """Closed form (1), written per pair so LOO drops in unchanged."""
    s = sub.a_sub.values
    bh = bhat_per_pair(sub, t, est)
    if s.sum() == 0 or (~s).sum() == 0:
        return np.nan
    return float(bh[s].mean() - bh[~s].mean())


def within_term(sub: pd.DataFrame, t: pd.DataFrame):
    """The exact within-book term of (2), plus its weight sum for the normalised reading."""
    NP, NF = float(t.nP.sum()), float(t.nF.sum())
    if NP == 0 or NF == 0:
        return np.nan, np.nan
    wP = t.nP.values / NP
    wF = t.nF.values / NF
    s = t.s.values
    wt = wP * (1.0 - s) + wF * s
    d = t.d.values
    ok = np.isfinite(d)
    return float((wt[ok] * d[ok]).sum()), float(wt[ok].sum())


def mc_noinfo(sub: pd.DataFrame, t: pd.DataFrame, gen: str, est: str, ndraw=NDRAW, seed=SEED):
    """BERNOULLI / HYPERGEOM draws of the pooled delta under independence (C11)."""
    s = sub.a_sub.values
    if s.sum() == 0 or (~s).sum() == 0:
        return np.nan, np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    books = sub.book.values
    order = np.argsort(books, kind="stable")
    bsorted = books[order]
    bounds = np.unique(bsorted, return_index=True)[1].tolist() + [len(bsorted)]
    blocks = [order[bounds[j]:bounds[j + 1]] for j in range(len(bounds) - 1)]
    y = sub.b_pass.values.astype(float)
    bh = bhat_per_pair(sub, t, est)
    out = np.empty(ndraw)
    for it in range(ndraw):
        yy = np.empty(len(y))
        for blk in blocks:
            if gen == "BERNOULLI":
                yy[blk] = (rng.random(len(blk)) < bh[blk]).astype(float)
            else:                                              # HYPERGEOM: within-book permute
                yy[blk] = y[blk][rng.permutation(len(blk))]
        out[it] = yy[s].mean() - yy[~s].mean()
    d0 = delta_of(sub)[0]
    lo, hi = np.percentile(out, [2.5, 97.5])
    pv = float(np.mean(np.abs(out - out.mean()) >= abs(d0 - out.mean())))
    return float(out.mean()), float(lo), float(hi), pv


def cells_of(C):
    """The 144 reported cells (cost x memo set x H x scheme x conditioning)."""
    for cost in sorted(C.cost.unique()):
        for set_name, keys in MEMO_SETS.items():
            for H in HORIZONS:
                for scheme in SCHEMES:
                    base = C[(C.cost == cost) & (C.book.isin(keys)) & (C.H == H) &
                             (C.scheme == scheme)]
                    for cond in CONDS:
                        yield (cost, set_name, H, scheme, cond), base[COND_MASK[cond](base)]


def decompose(C):
    """The exact decomposition (2) and the ANALYTIC share at every cell, every estimator."""
    rows = []
    for (cost, set_name, H, scheme, cond), sub in cells_of(C):
        if not len(sub):
            continue
        t = per_book(sub)
        dR, n, nhp, pa, pb = delta_of(sub)
        wt, wsum = within_term(sub, t)
        r = dict(cost=cost, memo_set=set_name, H=H, scheme=scheme, cond=cond, n_pairs=n,
                 n_halvesPASS=nhp, n_books=len(t), p_PASS=pa, p_FAIL=pb, delta_REAL=dR,
                 base_rate=float(sub.b_pass.mean()), within_term=wt, within_wsum=wsum,
                 within_avg=wt / wsum if wsum and np.isfinite(wsum) and wsum > 0 else np.nan,
                 n_books_ddef=int(np.isfinite(t.d).sum()),
                 n_books_dneg=int((t.d < 0).sum()))
        for est in ESTS:
            dN = noinfo_delta(sub, t, est)
            r[f"noinfo_{est}"] = dN
            r[f"share_{est}"] = dN / dR if np.isfinite(dN) and np.isfinite(dR) and dR != 0 \
                else np.nan
            r[f"resid_{est}"] = dR - dN if np.isfinite(dN) and np.isfinite(dR) else np.nan
        rows.append(r)
    D = pd.DataFrame(rows)
    D["ident_err"] = (D.delta_REAL - D.noinfo_RAW - D.within_term).abs()
    return D


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


def rule8(C):
    """RULE 8 on THIS run's own tuned axis (P1 generator x P2 estimator), C12."""
    hdr("RULE 8 — the (GENERATOR, ESTIMATOR) pair chosen on IS pairs only, read once on OOS")
    base = C[(C.cost == COST) & (C.book.isin(MEMO_SETS[HEAD_SET])) & (C.H == HEAD_H) &
             (C.scheme == HEAD_SCHEME)]
    base = base[COND_MASK[HEAD_COND](base)]
    legs = {"IS": base[base.b_end <= IS_END], "OOS": base[base.a_entry >= OOS_START]}
    rows = []
    for tag, sub in legs.items():
        if not len(sub):
            rows.append(dict(leg=tag, n_pairs=0))
            continue
        t = per_book(sub)
        dR = delta_of(sub)[0]
        wt, ws = within_term(sub, t)
        for gen in GENS:
            for est in ESTS:
                if gen == "ANALYTIC":
                    dN = noinfo_delta(sub, t, est)
                    lo = hi = pv = np.nan
                else:
                    dN, lo, hi, pv = mc_noinfo(sub, t, gen, est)
                rows.append(dict(leg=tag, gen=gen, est=est, n_pairs=len(sub),
                                 n_books=len(t), delta_REAL=dR, noinfo=dN,
                                 share=dN / dR if np.isfinite(dN) and dR else np.nan,
                                 lo=lo, hi=hi, p=pv, within_term=wt, within_avg=wt / ws
                                 if ws and ws > 0 else np.nan))
    W = pd.DataFrame(rows)
    P(W.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    return W


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P(f"# {DATE} cloud lane — IDEA 842: is the NEGATIVE NEXT-WINDOW delta a BASE-RATE IDENTITY?")
    P("=" * 112)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C4)")
    P(f"next-day execution, no shorting, no leverage.  P1 generator {GENS} | "
      f"P2 base-rate estimator {ESTS} | H {HORIZONS}, scheme {SCHEMES}, {N_OFFSETS} tiling "
      f"offsets, conditioning {CONDS}, cost {COSTS} bps, memo set {list(MEMO_SETS)} reported.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-corpus conditional contrast "
      "and its algebraic decomposition, which survivorship does not cancel out of.")

    P("\nbuilding books at the PROTOCOL rung (one full-sample simulation each, C1):")
    books, meta = build(panels, COST, verbose=True)
    gates_g1g2(books, meta, starts)
    gate_g3(books)
    bt, K = fixed_window(books, meta, panels, starts)
    bt.to_csv(f"{OUT}.books.csv")

    hdr("THE PAIR CENSUS (C7) — rebuilt independently of idea 839's committed CSV")
    Cs = [census(books, meta, panels, starts, COST)]
    for c in COSTS:
        if c == COST:
            continue
        P(f"  re-building every book at {c} bps for the reported cost rung ...")
        bk, _ = build(panels, c)
        Cs.append(census(bk, meta, panels, starts, c))
    C = pd.concat(Cs, ignore_index=True)
    P(f"{len(C):,} (book, H, scheme, offset, cost, pair) rows over {len(MEMO12)} books.")

    # ---------------------------------------------------------------- GATE G4
    hdr("GATE G4 — reproduce idea 839's and idea 832's committed deltas from this census")
    want = [("OVERLAP21", 756, "OTHER3", 627, 0.3182, 0.3810, -0.0628, "832 H_INFO"),
            ("OVERLAP21", 1260, "OTHER3", 419, 0.7072, 0.7838, -0.0765, "832 H_INFO"),
            ("OVERLAP21", 756, "NONE", 1680, 0.2549, 0.3616, -0.1067, "839 P1"),
            ("OVERLAP21", 756, "SHARPE", 1472, 0.2549, 0.3818, -0.1269, "839 P1"),
            ("CHAIN", 756, "NONE", 564, None, None, -0.1149, "839 scheme"),
            ("DISJOINT", 756, "NONE", 288, None, None, -0.1620, "839 HEAD")]
    g4, okg4 = [], True
    for (sch, H, cond, wn, wa, wb, wd, src) in want:
        s = C[(C.cost == COST) & (C.book.isin(MEMO12)) & (C.H == H) & (C.scheme == sch)]
        s = s[COND_MASK[cond](s)]
        d, n, nhp, pa, pb = delta_of(s)
        ok = (n == wn and abs(d - wd) <= 5e-4
              and (wa is None or abs(pa - wa) <= 5e-4)
              and (wb is None or abs(pb - wb) <= 5e-4))
        okg4 &= ok
        g4.append(dict(src=src, scheme=sch, H=H, cond=cond, got_n=n, want_n=wn,
                       got_pPASS=pa, want_pPASS=wa, got_pFAIL=pb, want_pFAIL=wb,
                       got_delta=d, want_delta=wd, verdict="PASS" if ok else "FAIL"))
    G4 = pd.DataFrame(g4)
    P(G4.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"GATE G4 -> {'PASS' if okg4 else 'FAIL'} (tolerance 5e-4 on every rate, exact on n).")

    # ---------------------------------------------------------------- the decomposition
    hdr("THE EXACT DECOMPOSITION (2) AND THE NO-INFORMATION SHARE — all reported cells")
    D = decompose(C)
    D.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"{len(D)} cells decomposed.")
    P(f"GATE G5 — identity |delta_REAL - noinfo_RAW - within_term| over every cell: "
      f"max {D.ident_err.max():.3e} vs bar 1e-12 -> "
      f"{'PASS' if D.ident_err.max() <= 1e-12 else 'FAIL'}")

    head = D[(D.cost == COST) & (D.memo_set == HEAD_SET) & (D.H == HEAD_H) &
             (D.scheme == HEAD_SCHEME) & (D.cond == HEAD_COND)].iloc[0]
    cols = ["cost", "memo_set", "H", "scheme", "cond", "n_pairs", "n_books", "delta_REAL",
            "noinfo_RAW", "share_RAW", "noinfo_LOO", "share_LOO", "noinfo_SHRUNK",
            "share_SHRUNK", "within_term", "within_avg", "n_books_dneg", "n_books_ddef"]
    P("\n-- the PROTOCOL rung (10 bps), MEMO12, every (H, scheme, conditioning) cell --")
    P(D[(D.cost == COST) & (D.memo_set == HEAD_SET)][cols].to_string(
        index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n-- the head cell, spelled out --")
    P(f"HEAD = {HEAD_SET}/{HEAD_SCHEME}/H={HEAD_H}/{HEAD_COND} at {COST} bps: "
      f"n {int(head.n_pairs)} pairs, {int(head.n_books)} books, delta_REAL {head.delta_REAL:+.4f}"
      f" = base-rate term {head.noinfo_RAW:+.4f} + within term {head.within_term:+.4f}.")
    for est in ESTS:
        P(f"    SHARE ({est:6s}) = {head[f'noinfo_{est}']:+.4f} / {head.delta_REAL:+.4f} = "
          f"{head[f'share_{est}']:+.4f}")
    sp = [head[f"share_{e}"] for e in ESTS]
    P(f"H_EST: max-min SHARE over the three estimators = {max(sp)-min(sp):.4f} vs bar 0.10 -> "
      f"{'PASS' if max(sp)-min(sp) <= 0.10 else 'FAIL'}")
    P(f"H_ID (SHARE >= 0.80): {'PASS' if head.share_RAW >= 0.80 else 'FAIL'}   "
      f"H_CONTENT (SHARE <= 0.20): {'PASS' if head.share_RAW <= 0.20 else 'FAIL'}")

    # per-book table at the head cell
    hsub = C[(C.cost == COST) & (C.book.isin(MEMO_SETS[HEAD_SET])) & (C.H == HEAD_H) &
             (C.scheme == HEAD_SCHEME)]
    hsub = hsub[COND_MASK[HEAD_COND](hsub)]
    T = per_book(hsub)
    NP, NF = float(T.nP.sum()), float(T.nF.sum())
    T["wP"] = T.nP / NP
    T["wF"] = T.nF / NF
    T["contrib_baserate"] = (T.wP - T.wF) * T.b
    T["wt_within"] = T.wP * (1 - T.s) + T.wF * T.s
    T["contrib_within"] = T.wt_within * T.d
    T.to_csv(f"{OUT}.perbook.csv")
    P("\n-- per-book anatomy at the head cell (this is what the base-rate term is made of) --")
    P(T.to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"Spearman(per-book halves-PASS share s_k, per-book 4b base rate b_k) = "
      f"{T[['s','b']].corr(method='spearman').iloc[0,1]:+.4f}  "
      f"(a NEGATIVE value is the whole mechanism: the halves clause selects low-base-rate books)")

    # ---------------------------------------------------------------- universality
    hdr("H_UNIV — the verdict across the 48 negative 10-bps cells")
    neg = D[(D.cost == COST) & (D.delta_REAL < 0)]
    P(f"{len(neg)} of {len(D[D.cost==COST])} cells at {COST} bps have delta_REAL < 0 "
      f"(idea 839 reported 48 of 48).")
    for est in ESTS:
        sh = neg[f"share_{est}"].dropna()
        P(f"  SHARE {est:6s}: median {sh.median():+.4f}  min {sh.min():+.4f}  "
          f"max {sh.max():+.4f}  >=0.80 in {int((sh>=0.80).sum())} of {len(sh)}  "
          f"<=0.20 in {int((sh<=0.20).sum())} of {len(sh)}")
    shr = neg["share_RAW"].dropna()
    frac = float((shr >= 0.80).mean()) if len(shr) else np.nan
    P(f"H_UNIV (same verdict at >=80% of the cells): share>=0.80 at {frac:.1%} -> "
      f"{'PASS' if frac >= 0.80 else 'FAIL'}")
    P("\n-- all cost rungs, MEMO12, HEAD scheme/H/cond --")
    P(D[(D.memo_set == HEAD_SET) & (D.H == HEAD_H) & (D.scheme == HEAD_SCHEME) &
        (D.cond == HEAD_COND)][cols].to_string(index=False,
                                               float_format=lambda x: f"{x:+.4f}"))

    # ---------------------------------------------------------------- P1 x P2 full grid + MC
    hdr("P1 x P2 — all nine (GENERATOR, ESTIMATOR) cells at the head cell and at 839's OVERLAP21")
    mrows = []
    for (sch, H, cond) in [(HEAD_SCHEME, HEAD_H, HEAD_COND), ("OVERLAP21", 756, "NONE"),
                           ("OVERLAP21", 756, "OTHER3"), ("CHAIN", 756, "NONE"),
                           ("DISJOINT", 1260, "NONE")]:
        s = C[(C.cost == COST) & (C.book.isin(MEMO_SETS[HEAD_SET])) & (C.H == H) &
              (C.scheme == sch)]
        s = s[COND_MASK[cond](s)]
        if not len(s):
            continue
        t = per_book(s)
        dR = delta_of(s)[0]
        for gen in GENS:
            for est in ESTS:
                if gen == "ANALYTIC":
                    dN = noinfo_delta(s, t, est)
                    lo = hi = pv = np.nan
                else:
                    dN, lo, hi, pv = mc_noinfo(s, t, gen, est)
                mrows.append(dict(scheme=sch, H=H, cond=cond, gen=gen, est=est, n_pairs=len(s),
                                  delta_REAL=dR, noinfo=dN,
                                  share=dN / dR if np.isfinite(dN) and dR else np.nan,
                                  band_lo=lo, band_hi=hi, p_real_vs_null=pv,
                                  m0_shrink=shrink_m0(t) if est == "SHRUNK" else np.nan))
    M = pd.DataFrame(mrows)
    M.to_csv(f"{OUT}.generators.csv", index=False)
    P(M.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\nDECLARED: HYPERGEOM resamples the OBSERVED labels, so its three estimator rows are "
      "identical BY CONSTRUCTION (it preserves b_k exactly and cannot read an estimate). "
      "It is printed three times rather than deduplicated so the 9-cell grid is legible.")
    mc = M[(M.scheme == HEAD_SCHEME) & (M.H == HEAD_H) & (M.cond == HEAD_COND)]
    an = mc[mc.gen == "ANALYTIC"].set_index("est").noinfo
    be = mc[mc.gen == "BERNOULLI"].set_index("est").noinfo
    hy = mc[mc.gen == "HYPERGEOM"].set_index("est").noinfo
    P(f"GATE G6 — Monte-Carlo convergence to the closed form at the head cell: "
      f"max |BERNOULLI mean - ANALYTIC| = {float((be-an).abs().max()):.4f}, "
      f"max |HYPERGEOM mean - ANALYTIC(RAW)| = {float((hy-an['RAW']).abs().max()):.4f} "
      f"vs bar 0.02 over {NDRAW} draws -> "
      f"{'PASS' if max(float((be-an).abs().max()), float((hy-an['RAW']).abs().max())) <= 0.02 else 'FAIL'}")

    # ---------------------------------------------------------------- H_POWER
    hdr("H_POWER — inject a KNOWN within-book delta and check the decomposition recovers it")
    rng = np.random.default_rng(SEED + 1)
    prows = []
    for inj in [0.00, 0.20, -0.20]:
        s = hsub.copy()
        t0_ = per_book(s)
        y = np.empty(len(s), float)
        bk = s.book.values
        sb = s.a_sub.values
        for k in t0_.index:
            m = bk == k
            base = float(t0_.loc[k, "b"])
            pP = np.clip(base + (1 - float(t0_.loc[k, "s"])) * inj, 0, 1)
            pF = np.clip(base - float(t0_.loc[k, "s"]) * inj, 0, 1)
            y[m & sb] = (rng.random(int((m & sb).sum())) < pP).astype(float)
            y[m & ~sb] = (rng.random(int((m & ~sb).sum())) < pF).astype(float)
        s["b_pass"] = y.astype(bool)
        t = per_book(s)
        dR = delta_of(s)[0]
        dN = noinfo_delta(s, t, "RAW")
        wt, ws = within_term(s, t)
        prows.append(dict(injected_d=inj, n_pairs=len(s), delta_REAL=dR, noinfo_RAW=dN,
                          within_term=wt, within_avg=wt / ws if ws > 0 else np.nan,
                          ident_err=abs(dR - dN - wt),
                          recovery_err=abs((wt / ws if ws > 0 else np.nan) - inj)))
    PW = pd.DataFrame(prows)
    P(PW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    pw = float(PW[PW.injected_d.abs() > 0].recovery_err.max())
    P(f"H_POWER (normalised within term recovers an injected +/-0.20 to within 0.01): "
      f"max error {pw:.4f} -> {'PASS' if pw <= 0.01 else 'FAIL'}   "
      f"(sampling noise at n={int(PW.n_pairs.iloc[0])} pairs is the whole error term; the "
      f"identity itself holds to {PW.ident_err.max():.3e})")

    # ---------------------------------------------------------------- rule 8
    W = rule8(C)
    W.to_csv(f"{OUT}.wf.csv", index=False)
    isl = W[(W.leg == "IS") & W.share.notna()]
    oos = W[(W.leg == "OOS") & W.share.notna()]
    if len(isl) and len(oos):
        pick = isl.loc[(isl.share - 1.0).abs().idxmin()]
        mt = oos[(oos.gen == pick.gen) & (oos.est == pick.est)]
        og = float(mt.share.iloc[0]) if len(mt) else np.nan
        gap = abs(og - float(pick.share)) if np.isfinite(og) else np.nan
        P(f"\nIS pick (SHARE closest to 1.00): ({pick.gen}, {pick.est}) at SHARE "
          f"{pick.share:+.4f} on {int(pick.n_pairs)} IS pairs -> OOS SHARE {og:+.4f} on "
          f"{int(oos.n_pairs.iloc[0])} pairs, gap {gap:.4f} vs bar 0.20 -> "
          f"{'PASS' if np.isfinite(gap) and gap <= 0.20 else 'FAIL'} (H_WF)")

    # ---------------------------------------------------------------- baseline compare
    hdr("PROTOCOL 3 — baseline.compare() for the two books this run's head cell leans on")
    for key in ["K5", "K8"]:
        pan = meta[key]["panel"]
        P(f"\n--- {key}: {meta[key]['label']} ---")
        entry = [c for c in CORPUS if c[0] == key][0]
        compare(f"842 cloud {key} {meta[key]['label']}", entry[3], panels[pan],
                freq=meta[key]["freq"])

    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
