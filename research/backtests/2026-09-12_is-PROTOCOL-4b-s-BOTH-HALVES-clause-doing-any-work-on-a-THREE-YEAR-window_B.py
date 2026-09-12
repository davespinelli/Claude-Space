#!/usr/bin/env python3
"""Idea 832 (lane B, 2026-09-12) — is PROTOCOL 4b's BOTH-HALVES clause doing any work on a
THREE-YEAR window?

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 831 censused the record's 12 committed,
reconstructible 4b passes on every entry date and found the binding leg of a 756d window is the
window-local HALVES clause: 975 of the 1,574 failing windows fail it, against 898 (DD cap), 550
(CAGR floor) and 211 (full-window Sharpe).  On the record's FIXED window the ranking is the
other way round.  A half of a 756d window is ~18 months, which may simply be too short to rank
two books at all — in which case the clause is not a robustness test, it is a coin flipped twice
and demanded to land heads twice.  This run asks whether that is what it is.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  CLAUSE READING k — the sub-window leg requires the book to beat SPY's Sharpe in EVERY one
                         of k contiguous equal blocks of the window.  k=1 IS the clause dropped
                         (the block is the window, so the leg collapses into the standing
                         full-window Sharpe leg); k=2 is the record's own reading; k=3 is the
                         queue's THIRDS; k=4 is reported as the other side of k=3.
  P2  WINDOW SPLIT H   — 756d (3y, the queue's ask) or 1260d (5y).  Both reported in full.
Entry spacing s in {21, 63}, claim set (MEMO8/MEMO12) and cost rung {0, 10, 25} bps are
REPORTED-NOT-SELECTED at every cell.  No book dial is tuned: every book runs at the gross, band,
n and cadence its own committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C6 copied verbatim from idea 831/829 so the three
censuses are directly comparable; C7-C8 are this run's own):
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest, weights
      decided at close t applied at t+1, the book's own cadence) and windows are SLICES of it.
  C2  A window's 4b legs are read WINDOW-LOCALLY against SPY over the SAME window: Sharpe (full
      window) > SPY, the sub-window leg under reading k, MaxDD >= 0.6 x SPY's MaxDD, CAGR >=
      0.7 x SPY's CAGR.  PASS_k requires all four.
  C3  The CAGR floor is applied LITERALLY, including where SPY's window CAGR is negative.
  C4  Warm-up: entry dates start at each panel's px.index[260], as baseline.compare does.
  C5  A window must lie wholly inside the sample; the last entry is len(px) - H.
  C6  A book is scored against its own panel's SPY column.
  C7  Block boundaries are j*T//k for j=0..k, so k=2 is bit-for-bit the `len(r)//2` split that
      PROTOCOL 4b, baseline.compare and idea 831 all use.  No block is dropped or overlapped.
  C8  A sub-block comparison's NOISE BAND is the Memmel (2003) correction to Jobson-Korkie for
      the difference of two correlated Sharpe ratios, computed on daily returns (annualisation
      cancels in z): V = (1/T)(2 - 2rho + 0.5(SRa^2 + SRb^2) - SRa SRb rho^2).  Gate G6 checks it
      against a paired stationary block bootstrap.

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_WORK     the clause CHANGES the verdict: at the headline cell (H=756, s=21, MEMO12, 10 bps)
             the MARGINAL BIND RATE — windows that pass the other three legs and fail only the
             halves leg, over all windows — is >= 0.10.
  H_MONO     the entry-date pass share is monotone non-increasing in k at every book (k is not
             nested, so this is a real test, not arithmetic).
  H_SURVIVE  dropping the clause (k=1) takes at least one committed 4b pass to the queue's
             standing 0.80 bar at the headline cell.
  H_NOISE    the clause is NOT a coin: FEWER than half of the k=2 sub-block comparisons are
             inside their own two-sided 95% noise band (|z| < 1.96).
  H_INFO     the clause is INFORMATIVE: among windows passing the other three legs, those that
             also pass the halves leg pass the NEXT, non-overlapping window's full 4b test at a
             rate at least 0.05 higher than those that fail it.
  H_WF       (rule 8, on this run's own tuned axes) the (k, H) cell chosen on IS entries only is
             also the OOS-best cell, and |OOS share - IS share| <= 0.10 there.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp (data/prices.csv is re-cached
      daily; ideas 406/574 measured u56 vintage drift at ~3e-3).
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05%.
  G3  this run's census machinery reproduces idea 828/829/831's committed entry-date share for
      the standing candidate (K5 g=1.00, H=756, s=21, k=2): 0.3977, bar |d| <= 0.02.
  G4  the vectorised window metrics reproduce engine.metrics exactly (bar 1e-10) on 200
      fixed-seed random windows.
  G5  the k=2 leg-failure counts at the headline cell reproduce idea 831's committed totals over
      its 12 books: 1,574 failing windows, halves 975, dd 898, cagr 550, sharpe 211.
  G6  the analytic noise band (C8) reproduces a paired stationary block bootstrap (block 21d,
      1,000 reps, fixed seed) on 60 sampled blocks: median ratio inside [0.75, 1.25].

Outputs (all under research/backtests/, all committed):
  .txt            full console log
  .books.csv      one row per book: fixed-window + OOS metrics, both KEEP paths under every k
  .census.csv.gz  one row per (book, H, s, entry): every leg under every k
  .grid.csv       one row per (book, H, s, k): pass share, leg shares, marginal bind rate
  .cells.csv      one row per (claim set, H, s, k, cost): how many committed passes clear each bar
  .noise.csv      the sub-block noise-band census + the bootstrap gate
  .info.csv       the next-window informativeness table
  .wf.csv         rule-8 IS/OOS table on the tuned (k, H) axes
  .result.md      the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_is-PROTOCOL-4b-s-BOTH-HALVES-clause-doing-any-work-on-a-THREE-YEAR-window_B.py
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state, compare)                                        # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

DATE, SLUG = "2026-09-12", "is-PROTOCOL-4b-s-BOTH-HALVES-clause-doing-any-work-on-a-THREE-YEAR-window"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
COSTS = [0, 10, 25]             # 10 is PROTOCOL's rung and the headline; 0/25 reported
COST = 10
KS = [1, 2, 3, 4]               # P1: 1 = clause DROPPED, 2 = the record's reading, 3/4 reported
HORIZONS = [756, 1260]          # P2: 3y (the queue's ask) and 5y
SPACINGS = [21, 63]             # reported, not selected
HEAD_H, HEAD_S, HEAD_K = 756, 21, 2
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
MAX_VOL, WARMUP = 0.60, 260
BAR_HI, BAR_MID = 0.80, 0.50
ZCRIT = 1.96
SEED = 8320
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 112 + f"\n{s}\n" + "=" * 112)


# =====================================================================================
# BOOK CONSTRUCTORS — copied verbatim from idea 831's committed script (which copied them
# from ideas 641/574/804), so the corpus is not silently redefined here.
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
    """R2 — hold every name above its own 200d MA, gross RE-SPREAD over exactly those names."""
    pm = px.notna()
    ma = (px > px.rolling(200).mean()) & pm
    k = ma.sum(axis=1).replace(0, np.nan)
    return gross * ma.astype(float).div(k, axis=0).fillna(0.0)


def ma_dist_tophalf(px, gross=0.75, q=0.50):
    """R3 — rank priced names by px/MA200-1, hold the top ceil(q*N) at gross/K each, rest CASH."""
    pm = px.notna()
    dist = (px / px.rolling(200).mean() - 1.0).where(pm)
    rk = dist.rank(axis=1, ascending=False)
    n_priced = dist.notna().sum(axis=1)
    k = np.ceil(q * n_priced).replace(0, np.nan)
    sel = rk.le(k, axis=0).fillna(False) & dist.notna()
    kk = sel.sum(axis=1).replace(0, np.nan)
    return gross * sel.astype(float).div(kk, axis=0).fillna(0.0)


def r6_topn(px, n=20, gross=0.65):
    """R4 — idea 804's committed constructor: rank priced names by 6m return, top n at g/n."""
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
CLAIM_SETS = {"MEMO8": MEMO8, "MEMO12": MEMO12}
COMPARANDS = ["LIVE", "V1"]


# =====================================================================================
# fast window metrics (gate G4 checks them against engine.metrics exactly)
# =====================================================================================
def w_metrics(r: np.ndarray):
    """(CAGR, Sharpe, MaxDD) of a daily return array, engine.metrics conventions."""
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    sd = r.std(ddof=1)
    sharpe = (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan
    mdd = float(np.min(eq / np.maximum.accumulate(eq) - 1.0))
    return cagr, sharpe, mdd


def sharpe_of(r: np.ndarray):
    sd = r.std(ddof=1)
    return (r.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else np.nan


def bounds(T, k):
    """C7 block boundaries: j*T//k.  k=2 is bit-for-bit engine's len(r)//2 split."""
    return [(j * T) // k for j in range(k + 1)]


def memmel_z(a: np.ndarray, b: np.ndarray):
    """z on (SR_a - SR_b) for two correlated daily return series (C8).  Annualisation cancels."""
    T = len(a)
    sa, sb = a.std(ddof=1), b.std(ddof=1)
    if sa <= 0 or sb <= 0:
        return np.nan, np.nan
    SRa, SRb = a.mean() / sa, b.mean() / sb
    rho = np.corrcoef(a, b)[0, 1]
    V = (2.0 - 2.0 * rho + 0.5 * (SRa ** 2 + SRb ** 2) - SRa * SRb * rho ** 2) / T
    if not np.isfinite(V) or V <= 0:
        return SRa - SRb, np.nan
    return SRa - SRb, (SRa - SRb) / np.sqrt(V)


# =====================================================================================
def build(panels, cost):
    books, meta = {}, {}
    for key, label, pan, wf, freq, pub, memo in CORPUS:
        px = panels[pan]
        t0 = time.time()
        r = backtest(px, wf(px), cost_bps=cost, freq=freq)["returns"]
        books[key] = r
        meta[key] = dict(label=label, panel=pan, freq=freq, pub=pub, memo=memo)
        if cost == COST:
            P(f"  built {key:5s} {label:62s} panel {pan:5s} freq {freq}  ({time.time()-t0:.1f}s)")
    return books, meta


def gates_g1g2(books, starts):
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


def gate_g4(books, panels, starts):
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
        b = (m["CAGR"], m["Sharpe"], m["MaxDD"])
        worst = max(worst, max(abs(x - y) for x, y in zip(a, b)))
    P(f"GATE G4 — vectorised window metrics vs engine.metrics on 200 fixed-seed random windows: "
      f"max |diff| = {worst:.3e} vs bar 1e-10 -> {'PASS' if worst <= 1e-10 else 'FAIL'}")
    return worst


# ----------------------------------------------------------------- the entry-date census
def census(books, meta, panels, starts, cost_tag=COST):
    rows = []
    spy = {pan: px["SPY"].pct_change().fillna(0.0).values for pan, px in panels.items()}
    for key in KEYS:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key].values, spy[pan]
        for H in HORIZONS:
            blk = {k: bounds(H, k) for k in KS}
            for s in SPACINGS:
                for i in range(i0, len(idx) - H + 1, s):
                    r, sp = r_all[i:i + H], s_all[i:i + H]
                    c, sh, dd = w_metrics(r)
                    s_c, s_s, s_d = w_metrics(sp)
                    row = dict(book=key, panel=pan, H=H, s=s, ipos=i, entry=idx[i],
                               end=idx[i + H - 1], cost=cost_tag,
                               CAGR=c, Sharpe=sh, MaxDD=dd,
                               spy_CAGR=s_c, spy_Sharpe=s_s, spy_MaxDD=s_d,
                               L_sharpe=bool(sh > s_s), L_dd=bool(dd >= 0.6 * s_d),
                               L_cagr=bool(c >= 0.7 * s_c), spy_neg=bool(s_c <= 0),
                               dSharpe=sh - s_s)
                    for k in KS:
                        bb = blk[k]
                        ok, ins, mind = True, 0, np.inf
                        for j in range(k):
                            a_, b_ = r[bb[j]:bb[j + 1]], sp[bb[j]:bb[j + 1]]
                            ok &= bool(sharpe_of(a_) > sharpe_of(b_))
                            d, z = memmel_z(a_, b_)
                            mind = min(mind, d)          # the worst block's daily-SR margin
                            if np.isfinite(z):
                                ins += int(abs(z) < ZCRIT)
                        row[f"L_sub{k}"] = ok
                        row[f"inside{k}"] = ins
                        row[f"margin{k}"] = mind
                        row[f"PASS{k}"] = bool(row["L_sharpe"] and ok and row["L_dd"]
                                               and row["L_cagr"])
                    rows.append(row)
    return pd.DataFrame(rows)


def grid_of(cen):
    out = []
    for (key, H, s), sub in cen.groupby(["book", "H", "s"]):
        base = dict(book=key, H=H, s=s, n=len(sub), leg_sharpe=sub.L_sharpe.mean(),
                    leg_dd=sub.L_dd.mean(), leg_cagr=sub.L_cagr.mean())
        oth = sub.L_sharpe & sub.L_dd & sub.L_cagr          # the other three legs
        for k in KS:
            r = dict(base)
            r.update(k=k, share=sub[f"PASS{k}"].mean(), leg_sub=sub[f"L_sub{k}"].mean(),
                     marginal_bind=float((oth & ~sub[f"L_sub{k}"]).mean()),
                     inside_share=sub[f"inside{k}"].sum() / (k * len(sub)),
                     med_margin=sub[f"margin{k}"].median(),
                     med_CAGR=sub.CAGR.median(), med_Sharpe=sub.Sharpe.median(),
                     worst_MaxDD=sub.MaxDD.min(), spy_neg=int(sub.spy_neg.sum()))
            out.append(r)
    return pd.DataFrame(out)


# ----------------------------------------------------------------- fixed-window KEEP paths
def fixed_window(books, meta, panels, starts):
    hdr("RULE 8 (b) MANDATED BOOK LEG + BOTH KEEP PATHS on the fixed window, under every k")
    rows = []
    for key in KEYS + ["SPY_U56", "SPY_B136"]:
        if key.startswith("SPY_"):
            pan = key.split("_")[1]
            r_all, pan_k = panels[pan]["SPY"].pct_change().fillna(0.0), pan
        else:
            r_all, pan_k = books[key], meta[key]["panel"]
        f, o = r_all.loc[starts[pan_k]:], r_all.loc[OOS_START:]
        fc, fs, fd = w_metrics(f.values)
        oc, os_, od = w_metrics(o.values)
        d = dict(book=key, panel=pan_k, full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                 OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)
        for k in KS:
            for tag, arr in (("full", f.values), ("OOS", o.values)):
                bb = bounds(len(arr), k)
                for j in range(k):
                    d[f"{tag}_k{k}b{j+1}"] = sharpe_of(arr[bb[j]:bb[j + 1]])
        rows.append(d)
    t = pd.DataFrame(rows).set_index("book")
    P(t[["panel", "full_CAGR", "full_Sharpe", "full_MaxDD", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD"]].to_string(float_format=lambda x: f"{x:+.4f}"))
    P("\n(OOS = entries 2017-01-01.. , the rule-8 evaluation window; the baseline is LIVE "
      "(RULES v2) and the benchmark is each panel's SPY.)")

    P("\nBoth KEEP paths per book, under every clause reading k "
      "(4a vs the LIVE book, 4b vs SPY; 4b judged on the full window AND OOS):")
    lv = t.loc["LIVE"]
    out = []
    for key in [c[0] for c in CORPUS if c[0] not in COMPARANDS]:
        r = t.loc[key]
        spy = t.loc[f"SPY_{meta[key]['panel']}"]
        for k in KS:
            sub_f = all(r[f"full_k{k}b{j+1}"] > spy[f"full_k{k}b{j+1}"] for j in range(k))
            sub_o = all(r[f"OOS_k{k}b{j+1}"] > spy[f"OOS_k{k}b{j+1}"] for j in range(k))
            sub_l = all(r[f"full_k{k}b{j+1}"] > lv[f"full_k{k}b{j+1}"] for j in range(k))
            legs4b = {"sub_full": sub_f, "OOSsh>SPY": r.OOS_Sharpe > spy.OOS_Sharpe,
                      "sub_OOS": sub_o,
                      "DD<=60%SPY": r.full_MaxDD >= 0.6 * spy.full_MaxDD,
                      "CAGR>=70%SPY": r.full_CAGR >= 0.7 * spy.full_CAGR,
                      "OOS_DD": r.OOS_MaxDD >= 0.6 * spy.OOS_MaxDD,
                      "OOS_CAGR": r.OOS_CAGR >= 0.7 * spy.OOS_CAGR}
            legs4a = {"sub>LIVE": sub_l, "DD<=LIVE": r.full_MaxDD >= lv.full_MaxDD}
            out.append(dict(book=key, k=k, keep4b="PASS" if all(legs4b.values()) else "FAIL",
                            fail4b="+".join(n for n, v in legs4b.items() if not v),
                            keep4a="PASS" if all(legs4a.values()) else "FAIL",
                            fail4a="+".join(n for n, v in legs4a.items() if not v)))
    kp = pd.DataFrame(out)
    piv = kp.pivot(index="book", columns="k", values="keep4b")
    piv.columns = [f"4b_k{c}" for c in piv.columns]
    pv2 = kp.pivot(index="book", columns="k", values="keep4a")
    pv2.columns = [f"4a_k{c}" for c in pv2.columns]
    both = piv.join(pv2).reindex(MEMO12)
    P(both.to_string())
    for k in KS:
        P(f"  k={k}: fixed-window 4b {int((piv[f'4b_k{k}']=='PASS').sum())} of {len(MEMO12)} PASS,"
          f"  4a {int((pv2[f'4a_k{k}']=='PASS').sum())} of {len(MEMO12)} PASS")
    return t, kp, both


# ----------------------------------------------------------------- bootstrap gate for C8
def gate_g6(books, meta, panels, starts):
    hdr("GATE G6 — the analytic noise band (C8) against a paired stationary block bootstrap")
    rng = np.random.default_rng(SEED)
    spy = {pan: panels[pan]["SPY"].pct_change().fillna(0.0).values for pan in panels}
    rows = []
    H, k, L, REPS = HEAD_H, HEAD_K, 21, 1000
    for _ in range(60):
        key = MEMO12[rng.integers(len(MEMO12))]
        pan = meta[key]["panel"]
        r_all, s_all = books[key].values, spy[pan]
        i0 = panels[pan].index.get_loc(starts[pan])
        i = int(rng.integers(i0, len(r_all) - H))
        bb = bounds(H, k)
        j = int(rng.integers(k))
        a = r_all[i + bb[j]: i + bb[j + 1]]
        b = s_all[i + bb[j]: i + bb[j + 1]]
        d, z = memmel_z(a, b)
        T = len(a)
        nb = int(np.ceil(T / L))
        st = rng.integers(0, T - L, size=(REPS, nb))
        idxm = (st[:, :, None] + np.arange(L)[None, None, :]).reshape(REPS, -1)[:, :T]
        A, B = a[idxm], b[idxm]
        sa = A.mean(axis=1) / A.std(axis=1, ddof=1)
        sb = B.mean(axis=1) / B.std(axis=1, ddof=1)
        boot_sd = (sa - sb).std(ddof=1)
        ana_sd = abs(d / z) if np.isfinite(z) and z != 0 else np.nan
        rows.append(dict(book=key, i=i, block=j, T=T, d=d, z=z, analytic_sd=ana_sd,
                         boot_sd=boot_sd, ratio=ana_sd / boot_sd if boot_sd else np.nan))
    B = pd.DataFrame(rows)
    med = B.ratio.median()
    ok = 0.75 <= med <= 1.25
    P(f"60 sampled (book, window, block) triples; stationary block bootstrap L=21, {REPS} reps, "
      f"seed {SEED}.")
    P(f"  median analytic_sd / bootstrap_sd = {med:.4f}  (IQR "
      f"{B.ratio.quantile(0.25):.4f} .. {B.ratio.quantile(0.75):.4f})  vs bar [0.75, 1.25] -> "
      f"{'PASS' if ok else 'FAIL'}")
    P(f"  median |z| over the 60 = {B.z.abs().median():.3f}; share |z| < {ZCRIT} = "
      f"{(B.z.abs() < ZCRIT).mean():.4f}")
    B.to_csv(f"{OUT}.noise.csv", index=False)
    return B, ok


# ----------------------------------------------------------------- informativeness
def informativeness(cen):
    hdr("H_INFO — does the halves verdict on THIS window say anything about the NEXT one?")
    c = cen[(cen.s == HEAD_S) & (cen.cost == COST) & (~cen.book.isin(COMPARANDS))].copy()
    rows = []
    for (key, H), sub in c.groupby(["book", "H"]):
        nxt = sub.set_index("ipos")
        for _, r in sub.iterrows():
            j = r.ipos + H                      # the next NON-OVERLAPPING window
            if j not in nxt.index:
                continue
            n = nxt.loc[j]
            if not (r.L_sharpe and r.L_dd and r.L_cagr):   # condition on the other three legs
                continue
            rows.append(dict(book=key, H=H, entry=r.entry, halves=bool(r.L_sub2),
                             margin2=r.margin2, nxt_pass=bool(n[f"PASS{HEAD_K}"]),
                             nxt_dSharpe=n.dSharpe))
    I = pd.DataFrame(rows)
    if not len(I):
        P("no (window, next window) pairs available")
        return I, {}
    res = {}
    for H in HORIZONS:
        s = I[I.H == H]
        if not len(s):
            continue
        a = s[s.halves].nxt_pass.mean() if s.halves.any() else np.nan
        b = s[~s.halves].nxt_pass.mean() if (~s.halves).any() else np.nan
        rho = s.margin2.rank().corr(s.nxt_dSharpe.rank())
        res[H] = (a, b, a - b if np.isfinite(a) and np.isfinite(b) else np.nan, rho, len(s),
                  int(s.halves.sum()))
        P(f"  H={H}: {len(s)} conditioned pairs ({int(s.halves.sum())} halves-PASS / "
          f"{int((~s.halves).sum())} halves-FAIL).  P(next window PASSes 4b | halves PASS) = "
          f"{a:.4f}, | halves FAIL = {b:.4f}, difference {a-b:+.4f} vs bar +0.05.  "
          f"Spearman(halves margin, next window dSharpe) = {rho:+.4f} (n={len(s)}).")
    pr = []
    for key, s in I[I.H == HEAD_H].groupby("book"):
        pr.append(dict(book=key, n=len(s), n_hp=int(s.halves.sum()),
                       p_next_given_pass=s[s.halves].nxt_pass.mean() if s.halves.any() else np.nan,
                       p_next_given_fail=s[~s.halves].nxt_pass.mean() if (~s.halves).any()
                       else np.nan))
    per = pd.DataFrame(pr).set_index("book")
    per["delta"] = per.p_next_given_pass - per.p_next_given_fail
    P("\nPer book at H=756 (positive delta = the clause carries information about the next window):")
    P(per.to_string(float_format=lambda x: f"{x:.4f}"))
    I.to_csv(f"{OUT}.info.csv", index=False)
    return I, res


# ----------------------------------------------------------------- rule 8 on the tuned axes
def rule8(cen):
    hdr("RULE 8 (a) — ON THIS RUN'S OWN TUNED AXES (k, H): chosen on IS entries only")
    c = cen[(cen.s == HEAD_S) & (cen.cost == COST) & (cen.book.isin(MEMO12))]
    rows = []
    for k in KS:
        for H in HORIZONS:
            sub = c[c.H == H]
            is_ = sub[sub.end <= IS_END]
            oos = sub[sub.entry >= OOS_START]
            rows.append(dict(k=k, H=H, n_IS=len(is_), IS_share=is_[f"PASS{k}"].mean()
                             if len(is_) else np.nan, n_OOS=len(oos),
                             OOS_share=oos[f"PASS{k}"].mean() if len(oos) else np.nan))
    t = pd.DataFrame(rows)
    P(t.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    v = t.dropna(subset=["IS_share"])
    pick = None
    if len(v) and v.n_IS.max() > 0:
        best = v.sort_values(["IS_share", "n_IS"], ascending=[False, False]).iloc[0]
        pick = (int(best.k), int(best.H))
        gap = abs(best.OOS_share - best.IS_share)
        ob = v.sort_values("OOS_share", ascending=False).iloc[0]
        P(f"\nIS-chosen (k, H) = {pick} on {int(best.n_IS)} IS windows (IS share "
          f"{best.IS_share:.4f}) -> OOS share {best.OOS_share:.4f} on {int(best.n_OOS)} windows, "
          f"read ONCE.  |OOS-IS| = {gap:.4f} vs bar 0.10.")
        P(f"OOS-best cell is (k={int(ob.k)}, H={int(ob.H)}) at {ob.OOS_share:.4f}; the IS pick "
          f"{'IS' if (int(ob.k), int(ob.H)) == pick else 'is NOT'} the OOS best.")
    else:
        P("\nNo IS window closes by 2016-12-31 -> nothing is selectable IS.")
    t.to_csv(f"{OUT}.wf.csv", index=False)
    return t, pick


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P(f"# {DATE} lane B — IDEA 832: is PROTOCOL 4b's BOTH-HALVES clause doing any work on a")
    P("#                 THREE-YEAR window?")
    P("=" * 112)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C4)")
    P(f"next-day execution, no shorting, no leverage.  P1 clause reading k {KS} "
      f"(1 = clause DROPPED, 2 = the record's reading) | P2 horizon H {HORIZONS} | "
      f"spacing {SPACINGS}, claim set {list(CLAIM_SETS)} and cost {COSTS} bps reported.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-window contrast.")

    P("\nbuilding books at the PROTOCOL rung (one full-sample simulation each, C1):")
    books, meta = build(panels, COST)
    gates_g1g2(books, starts)
    gate_g4(books, panels, starts)

    bt, kp, both = fixed_window(books, meta, panels, starts)
    bt.to_csv(f"{OUT}.books.csv")

    hdr("THE ENTRY-DATE CENSUS — every (book x H x s x k) cell reported")
    cens = [census(books, meta, panels, starts, COST)]
    for c in COSTS:
        if c == COST:
            continue
        P(f"  re-building every book at {c} bps for the reported cost rung ...")
        bk, _ = build(panels, c)
        cens.append(census(bk, meta, panels, starts, c))
    cen = pd.concat(cens, ignore_index=True)
    cen.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    head_cen = cen[cen.cost == COST]
    g = grid_of(head_cen)
    g.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"{len(cen):,} (book, H, s, entry, cost) rows; {len(head_cen):,} at the PROTOCOL rung, "
      f"over {len(CORPUS)} books and {len(KS)} clause readings.")

    g3 = g[(g.book == "K5") & (g.H == HEAD_H) & (g.s == HEAD_S) & (g.k == 2)].iloc[0]
    d3 = abs(g3.share - 0.3977)
    P(f"\nGATE G3 — this run's census reproduces idea 828/829/831's committed entry-date share "
      f"for the standing candidate (K5, H=756, s=21, k=2): got {g3.share:.4f} on {int(g3.n)} "
      f"windows vs committed 0.3977, |d| = {d3:.4f} vs bar 0.0200 -> "
      f"{'PASS' if d3 <= 0.02 else 'FAIL'}")

    f2 = head_cen[(head_cen.H == HEAD_H) & (head_cen.s == HEAD_S) & (head_cen.book.isin(MEMO12))]
    fail = f2[~f2.PASS2]
    g5 = dict(n_fail=len(fail), halves=int((~fail.L_sub2).sum()), dd=int((~fail.L_dd).sum()),
              cagr=int((~fail.L_cagr).sum()), sharpe=int((~fail.L_sharpe).sum()))
    want = dict(n_fail=1574, halves=975, dd=898, cagr=550, sharpe=211)
    okg5 = g5 == want
    P(f"GATE G5 — k=2 leg-failure counts at the headline cell vs idea 831's committed totals: "
      f"got {g5} vs committed {want} -> {'PASS' if okg5 else 'FAIL'}")

    B, okg6 = gate_g6(books, meta, panels, starts)

    # ---------------------------------------------------------------- the grid
    hdr("THE GRID — entry-date pass share by clause reading (PROTOCOL rung, 10 bps)")
    for H in HORIZONS:
        for s in SPACINGS:
            P(f"--- H={H}d  s={s}d ---")
            sub = (g[(g.H == H) & (g.s == s)]
                   .pivot(index="book", columns="k", values="share").reindex(KEYS))
            sub.columns = [f"share_k{c}" for c in sub.columns]
            leg = (g[(g.H == H) & (g.s == s)]
                   .pivot(index="book", columns="k", values="leg_sub").reindex(KEYS))
            leg.columns = [f"leg_sub_k{c}" for c in leg.columns]
            mb = (g[(g.H == H) & (g.s == s)]
                  .pivot(index="book", columns="k", values="marginal_bind").reindex(KEYS))
            mb.columns = [f"bind_k{c}" for c in mb.columns]
            n = g[(g.H == H) & (g.s == s)].groupby("book").n.first().reindex(KEYS)
            P(pd.concat([n.rename("n"), sub, leg, mb], axis=1)
              .to_string(float_format=lambda x: f"{x:.4f}"))
            P("")

    hdr("P1 x P2 x cost — how many committed 4b passes clear each entry-date bar, at every cell")
    cells = []
    for cost in COSTS:
        gg = grid_of(cen[cen.cost == cost])
        for cs, keys in CLAIM_SETS.items():
            for H in HORIZONS:
                for s in SPACINGS:
                    for k in KS:
                        sub = (gg[(gg.H == H) & (gg.s == s) & (gg.k == k) & (gg.book.isin(keys))]
                               .set_index("book").reindex(keys))
                        lv = gg[(gg.H == H) & (gg.s == s) & (gg.k == k) & (gg.book == "LIVE")]
                        cells.append(dict(cost=cost, claim_set=cs, H=H, s=s, k=k,
                                          n_books=len(keys),
                                          n_ge_080=int((sub.share >= BAR_HI).sum()),
                                          n_ge_050=int((sub.share >= BAR_MID).sum()),
                                          median_share=sub.share.median(),
                                          max_share=sub.share.max(), argmax=sub.share.idxmax(),
                                          min_share=sub.share.min(),
                                          median_bind=sub.marginal_bind.median(),
                                          live_share=lv.share.iloc[0]))
    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    P(C[C.cost == COST].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n--- the same table at 0 and 25 bps (reported, not selected) ---")
    P(C[(C.cost != COST) & (C.claim_set == "MEMO12") & (C.s == HEAD_S)]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- noise resolution
    hdr("IS AN 18-MONTH BLOCK LONG ENOUGH TO RANK TWO BOOKS?  (C8 noise band per sub-block)")
    nz = []
    for H in HORIZONS:
        for k in KS:
            if k == 1:
                continue
            sub = head_cen[(head_cen.H == H) & (head_cen.s == HEAD_S) &
                           (head_cen.book.isin(MEMO12))]
            nz.append(dict(H=H, k=k, block_days=H // k, block_months=round(H / k / 21.0, 1),
                           n_blocks=k * len(sub),
                           inside_share=sub[f"inside{k}"].sum() / (k * len(sub)),
                           med_margin=sub[f"margin{k}"].median(),
                           leg_share=sub[f"L_sub{k}"].mean()))
    NZ = pd.DataFrame(nz)
    P(NZ.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("inside_share = fraction of sub-block (book vs SPY) Sharpe comparisons that fall inside "
      f"their own two-sided 95% band (|z| < {ZCRIT}), i.e. comparisons the data cannot call.")

    I, info = informativeness(head_cen)
    wf, pick = rule8(head_cen)

    # ---------------------------------------------------------------- hypotheses
    hdr("PRE-REGISTERED HYPOTHESES")
    head = g[(g.H == HEAD_H) & (g.s == HEAD_S)]
    h2 = head[(head.k == HEAD_K) & (head.book.isin(MEMO12))]
    h1 = head[(head.k == 1) & (head.book.isin(MEMO12))]
    verd = {}
    mb_med = h2.marginal_bind.median()
    verd["H_WORK"] = (mb_med >= 0.10,
                      f"median marginal bind rate over MEMO12 = {mb_med:.4f} "
                      f"(min {h2.marginal_bind.min():.4f}, max {h2.marginal_bind.max():.4f}) "
                      f"vs bar 0.10; pooled {float((h2.marginal_bind*h2.n).sum()/h2.n.sum()):.4f}")
    piv = head[head.book.isin(MEMO12)].pivot(index="book", columns="k", values="share")
    mono = int(((piv[1] >= piv[2]) & (piv[2] >= piv[3]) & (piv[3] >= piv[4])).sum())
    verd["H_MONO"] = (mono == len(piv), f"share monotone non-increasing in k at {mono} of "
                                        f"{len(piv)} books")
    verd["H_SURVIVE"] = ((h1.share >= BAR_HI).any(),
                         f"k=1 (clause dropped): {(h1.share>=BAR_HI).sum()} of 12 reach "
                         f"{BAR_HI} (max {h1.share.max():.4f} at {h1.set_index('book').share.idxmax()}); "
                         f"k=2: {(h2.share>=BAR_HI).sum()} of 12")
    ins = NZ[(NZ.H == HEAD_H) & (NZ.k == HEAD_K)].inside_share.iloc[0]
    verd["H_NOISE"] = (ins < 0.50, f"{ins:.4f} of the 18-month sub-block comparisons are inside "
                                   f"their own 95% noise band vs bar 0.50")
    if HEAD_H in info:
        a, b, dlt, rho, n, nhp = info[HEAD_H]
        verd["H_INFO"] = (np.isfinite(dlt) and dlt >= 0.05,
                          f"P(next 4b PASS | halves PASS) - P(. | halves FAIL) = {dlt:+.4f} "
                          f"({a:.4f} vs {b:.4f}, n={n}) vs bar +0.05; Spearman(margin, next "
                          f"dSharpe) {rho:+.4f}")
    else:
        verd["H_INFO"] = (False, "no conditioned (window, next window) pairs")
    if pick is not None:
        row = wf[(wf.k == pick[0]) & (wf.H == pick[1])].iloc[0]
        gap = abs(row.OOS_share - row.IS_share)
        ob = wf.dropna(subset=["IS_share"]).sort_values("OOS_share", ascending=False).iloc[0]
        verd["H_WF"] = (gap <= 0.10 and (int(ob.k), int(ob.H)) == pick,
                        f"IS pick (k,H)={pick} -> gap {gap:.4f} vs bar 0.10; OOS best "
                        f"(k={int(ob.k)}, H={int(ob.H)})")
    else:
        verd["H_WF"] = (False, "no IS-selectable cell")
    for k, (ok, why) in verd.items():
        P(f"  {k:10s} {'PASS' if ok else 'FAIL'}  — {why}")
    P(f"\n{sum(1 for v in verd.values() if v[0])} of {len(verd)} pre-registered hypotheses PASS.")

    # ---------------------------------------------------------------- the deliverable
    hdr("THE DELIVERABLE — how many committed 4b passes survive each reading of the clause")
    rowsD = []
    for key in MEMO12:
        r = bt.loc[key]
        d = dict(book=key, panel=r.panel, full_Sharpe=r.full_Sharpe, full_CAGR=r.full_CAGR,
                 full_MaxDD=r.full_MaxDD)
        for k in KS:
            d[f"fixed_4b_k{k}"] = both.loc[key, f"4b_k{k}"]
            d[f"share_k{k}"] = head[(head.book == key) & (head.k == k)].share.iloc[0]
        d["bind_k2"] = head[(head.book == key) & (head.k == 2)].marginal_bind.iloc[0]
        rowsD.append(d)
    D = pd.DataFrame(rowsD).sort_values("share_k2", ascending=False)
    P(D.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    D.to_csv(f"{OUT}.deliverable.csv", index=False)

    hdr("PROTOCOL rule 3 — baseline.compare on the two books this run would have to defend")
    for key in ["K4", "K5"]:
        wfun = dict((c[0], c[3]) for c in CORPUS)[key]
        fr = dict((c[0], c[4]) for c in CORPUS)[key]
        P(f"\n--- {key}: {meta[key]['label']} ---")
        res = compare(f"832 B {key} {meta[key]['label']}", wfun, panels[meta[key]["panel"]],
                      freq=fr, cost_bps=COST)
        LOG.append(str(res["table"]))

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return D, C, g, bt, wf, verd, NZ


if __name__ == "__main__":
    main()
