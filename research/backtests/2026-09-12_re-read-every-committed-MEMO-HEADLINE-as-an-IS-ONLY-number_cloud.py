#!/usr/bin/env python3
"""Idea 836 (cloud lane, 2026-09-12) — re-read every committed MEMO HEADLINE as an IS-ONLY number.

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 833 found that 11 of 12 committed books' FULL-sample
MaxDD *is* their 2017+ MaxDD to 1e-9, and that the record's two strongest "the headline predicts
out of window" cells (MAXDD -> OOS_MaxDD +1.0000, H2 -> OOS_Sharpe +0.9510) are IDENTITIES, not
predictions.  Every memo in research/backtests/ leads with a FULL-sample triple (CAGR, Sharpe,
MaxDD) whose window CONTAINS the 2017+ window the memo then claims to be validated on.  This run
asks the only question that separates the two: recompute every headline on the IS window ALONE
and report which memo's lead number changes rank.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  MEMO SET   — MEMO8 (the 8 books with committed KEEP/PARK memos), MEMO12 (those plus the 4
                   reconstructed 4b candidates), MEMO14 (plus the two comparands LIVE and V1).
  P2  SPLIT DATE — 2013-12-31 .. 2018-12-31 (6 rungs).  2016-12-31 is PROTOCOL rule 8's own
                   split and the headline cell.
Cost rung {0, 10, 25} bps and the LEAD READING (which of CAGR / Sharpe / MaxDD counts as "the
lead number") are REPORTED AT EVERY POINT, not selected.  No book dial is tuned: every book runs
at the gross, band, n and cadence its own committed memo published.

CONVENTIONS, DECLARED BEFORE ANY NUMBER (C1-C4 copied from ideas 831/832/833 so the censuses are
directly comparable; C5-C7 are this run's own):
  C1  Each book's daily return series is run ONCE over the full sample (engine.backtest, weights
      decided at close t applied at t+1, the book's own cadence).  Windows are SLICES of it.
  C2  Warm-up: scoring starts at each panel's px.index[260], as baseline.compare does.
  C3  A book is scored against its own panel's SPY column.
  C4  4b legs are read against SPY over the SAME window; the CAGR floor is applied literally.
  C5  FULL = [start_260 .. end].  IS = [start_260 .. split].  POST = (split .. end], i.e. the
      first trading day strictly after the split date.  IS and POST are disjoint and their union
      is FULL exactly (gate G4 asserts this, row for row).
  C6  "Lead number" = the first number a memo's section-3 headline quotes, which is CAGR in every
      committed memo.  Sharpe and MaxDD are reported beside it at every cell because the record
      elsewhere treats Sharpe as the headline (idea 833).
  C7  Rank 1 = best: highest CAGR, highest Sharpe, SHALLOWEST MaxDD (MaxDD is negative, so rank
      descending on the raw value).  Ties share the average rank (pandas default).

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_RANK     at the headline cell (MEMO12, split 2016-12-31, 10 bps, lead = CAGR) at least one
             book's lead-number rank moves by >= 3 places when the headline is recomputed IS-only.
  H_TOP1     the top-1 book by lead number CHANGES IDENTITY at the headline cell.
  H_RHO      Spearman(FULL lead, IS lead) < 0.90 at the headline cell — i.e. the published
             headline is not simply a restatement of its own in-sample half.
  H_CONTAM   the FULL headline orders the POST window BETTER than the IS-only headline does
             (rho_FULL_POST > rho_IS_POST) at >= 4 of the 6 split dates, on the lead number —
             the signature of in-window contamination rather than prediction.
  H_MAXDD_ID >= 8 of the 12 books have full-sample MaxDD equal to POST MaxDD to 1e-9 at the
             2016-12-31 split (idea 833 committed 11 of 12; this re-derives it).
  H_STABLE   no headline number's IS-only rank order is stable across all six splits
             (min pairwise Spearman over the 15 split pairs < 1.0).
  H_WF       (rule 8) the book chosen on IS-only Sharpe (<= 2016-12-31) is also the OOS-best book
             by Sharpe over 2017+.
  H_CENSUS   at least half of the committed memo files state NO IS-only headline anywhere.

GATES (printed before any new number):
  G1  every book reproduces its own memo's published (CAGR, Sharpe, MaxDD) within
      |dCAGR| <= 1.00pp, |dSharpe| <= 0.060, |dMaxDD| <= 2.00pp (data/prices.csv is re-cached
      daily; ideas 406/574 measured u56 vintage drift at ~3e-3).
  G2  the LIVE book reproduces RULES.md v2's committed 8.63% / 1.202 / -12.05%.
  G3  the vectorised window metrics reproduce engine.metrics exactly (bar 1e-10) on 200
      fixed-seed random windows.
  G4  C5's split is EXHAUSTIVE and DISJOINT: len(IS) + len(POST) == len(FULL) and the
      concatenated index is FULL's index, at every split, for every panel.
  G5  the MaxDD-identity count at the 2016-12-31 split reproduces idea 833's committed 11 of 12.

Outputs (all under research/backtests/, all committed):
  .txt             full console log
  .books.csv       one row per (book, split, cost): FULL / IS / POST triples
  .grid.csv        one row per (memo set, split, cost, lead reading): every rank statistic
  .ranks.csv       the per-book rank table at the headline cell
  .census.csv      the textual memo census (does the file state an IS-only headline at all?)
  .wf.csv          rule-8 IS/OOS table plus both KEEP paths per book
  .result.md       the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_re-read-every-committed-MEMO-HEADLINE-as-an-IS-ONLY-number_cloud.py
"""
from __future__ import annotations
import re
import sys
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import (load_universe, rules_v1_weights, rules_v2_weights, score,  # noqa: E402
                      band_state, compare)                                        # noqa: E402
from engine import backtest, metrics                                              # noqa: E402

DATE = "2026-09-12"
SLUG = "re-read-every-committed-MEMO-HEADLINE-as-an-IS-ONLY-number"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
COSTS = [0, 10, 25]
COST = 10                                     # PROTOCOL's rung and the headline
SPLITS = [pd.Timestamp(f"{y}-12-31") for y in (2013, 2014, 2015, 2016, 2017, 2018)]   # P2
HEAD_SPLIT = pd.Timestamp("2016-12-31")       # PROTOCOL rule 8's own split
LEADS = ["CAGR", "Sharpe", "MaxDD"]           # C6: CAGR is the lead; all three reported
HEAD_LEAD = "CAGR"
MAX_VOL, WARMUP = 0.60, 260
NPERM = 20000
SEED = 8360
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
MEMO14 = MEMO12 + ["LIVE", "V1"]
MEMO_SETS = {"MEMO8": MEMO8, "MEMO12": MEMO12, "MEMO14": MEMO14}      # P1
COMPARANDS = ["LIVE", "V1"]
HEAD_SET = "MEMO12"


# =====================================================================================
# metrics (gate G3 checks them against engine.metrics exactly)
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


def spearman(a: pd.Series, b: pd.Series):
    v = pd.concat([a, b], axis=1).dropna()
    if len(v) < 3:
        return np.nan
    return float(v.iloc[:, 0].rank().corr(v.iloc[:, 1].rank()))


def perm_band(n, nperm=NPERM, seed=SEED):
    """Two-sided 95% |rho| band of Spearman under the label-permutation null at this n."""
    rng = np.random.default_rng(seed)
    x = np.arange(n, dtype=float)
    xr = x - x.mean()
    den = (xr ** 2).sum()
    rr = np.empty(nperm)
    for i in range(nperm):
        y = rng.permutation(x)
        rr[i] = float(((xr * (y - y.mean())).sum()) / den)
    return float(np.quantile(np.abs(rr), 0.95))


def ranks_of(df: pd.DataFrame, col: str):
    """C7: rank 1 = best.  CAGR/Sharpe high-is-best; MaxDD is negative so high-is-best too."""
    return df[col].rank(ascending=False)


# =====================================================================================
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


def gate_g3(books, panels):
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
    P(f"GATE G3 — vectorised window metrics vs engine.metrics on 200 fixed-seed random windows: "
      f"max |diff| = {worst:.3e} vs bar 1e-10 -> {'PASS' if worst <= 1e-10 else 'FAIL'}")
    return worst


def gate_g4(books, meta, starts):
    """C5's split is exhaustive and disjoint at every split, for every book."""
    worst_ok = True
    for key in KEYS:
        full = books[key].loc[starts[meta[key]["panel"]]:]
        for sp in SPLITS:
            is_ = full.loc[:sp]
            post = full.loc[full.index > sp]
            ok = (len(is_) + len(post) == len(full)
                  and is_.index.append(post.index).equals(full.index))
            worst_ok &= ok
    P(f"GATE G4 — C5 split exhaustive + disjoint over {len(KEYS)} books x {len(SPLITS)} splits: "
      f"{'PASS' if worst_ok else 'FAIL'}")
    return worst_ok


# ----------------------------------------------------------------- the headline recomputation
def headlines(books, meta, panels, starts, cost_tag=COST):
    """One row per (book, split): the FULL, IS and POST triples of that book's headline."""
    rows = []
    spy = {pan: px["SPY"].pct_change().fillna(0.0) for pan, px in panels.items()}
    for key in KEYS + ["SPY_U56", "SPY_B136"]:
        if key.startswith("SPY_"):
            pan = key.split("_")[1]
            r_all = spy[pan]
        else:
            pan = meta[key]["panel"]
            r_all = books[key]
        full = r_all.loc[starts[pan]:]
        fc, fs, fd = w_metrics(full.values)
        for sp in SPLITS:
            is_ = full.loc[:sp]
            post = full.loc[full.index > sp]
            ic, isr, idd = w_metrics(is_.values)
            pc, ps, pdd = w_metrics(post.values)
            rows.append(dict(book=key, panel=pan, cost=cost_tag, split=sp.date(),
                             n_full=len(full), n_IS=len(is_), n_POST=len(post),
                             post_share=len(post) / len(full),
                             full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd,
                             IS_CAGR=ic, IS_Sharpe=isr, IS_MaxDD=idd,
                             POST_CAGR=pc, POST_Sharpe=ps, POST_MaxDD=pdd,
                             dd_identity=bool(abs(fd - pdd) < 1e-9)))
    return pd.DataFrame(rows)


def rank_grid(H):
    """One row per (memo set, split, cost, lead reading): every rank statistic."""
    out, ranks_rows = [], []
    bands = {}
    for cost in COSTS:
        for set_name, keys in MEMO_SETS.items():
            for sp in SPLITS:
                sub = H[(H.cost == cost) & (H.split == sp.date()) & (H.book.isin(keys))]
                sub = sub.set_index("book").reindex(keys)
                n = len(sub)
                if n not in bands:
                    bands[n] = perm_band(n)
                for lead in LEADS:
                    rf = ranks_of(sub, f"full_{lead}")
                    ri = ranks_of(sub, f"IS_{lead}")
                    rp = ranks_of(sub, f"POST_{lead}")
                    disp = (rf - ri).abs()
                    row = dict(cost=cost, memo_set=set_name, split=sp.date(), lead=lead, n=n,
                               rho_FULL_IS=spearman(sub[f"full_{lead}"], sub[f"IS_{lead}"]),
                               rho_FULL_POST=spearman(sub[f"full_{lead}"], sub[f"POST_{lead}"]),
                               rho_IS_POST=spearman(sub[f"IS_{lead}"], sub[f"POST_{lead}"]),
                               perm95=bands[n],
                               n_moved=int((disp > 0).sum()), max_disp=float(disp.max()),
                               mean_disp=float(disp.mean()),
                               n_moved_ge3=int((disp >= 3).sum()),
                               top1_FULL=rf.idxmin(), top1_IS=ri.idxmin(),
                               top1_POST=rp.idxmin(),
                               top1_changed=bool(rf.idxmin() != ri.idxmin()),
                               argmax_disp=disp.idxmax(),
                               post_share=float(sub.post_share.iloc[0]))
                    row["contam"] = row["rho_FULL_POST"] - row["rho_IS_POST"]
                    out.append(row)
                    if cost == COST and set_name == HEAD_SET and sp == HEAD_SPLIT:
                        for k in keys:
                            ranks_rows.append(dict(
                                book=k, lead=lead, full=sub.loc[k, f"full_{lead}"],
                                IS=sub.loc[k, f"IS_{lead}"], POST=sub.loc[k, f"POST_{lead}"],
                                rank_FULL=rf[k], rank_IS=ri[k], rank_POST=rp[k],
                                disp=disp[k]))
    return pd.DataFrame(out), pd.DataFrame(ranks_rows)


# ----------------------------------------------------------------- textual memo census
MEMO_PAT = re.compile(r"memo", re.I)
IS_PAT = re.compile(r"(rule\s*8|IS\s*<=|in-?sample|<=\s*2016|2009[-–]2016|dials on IS)", re.I)
HEAD_PAT = re.compile(r"full sample|full-sample", re.I)


def memo_census():
    hdr("THE TEXTUAL CENSUS — do the committed memos state an IS-ONLY headline at all?")
    files = sorted(p for p in (ROOT / "research" / "backtests").glob("*.md")
                   if MEMO_PAT.search(p.name))
    rows = []
    for p in files:
        t = p.read_text(errors="ignore")
        rows.append(dict(file=p.name, bytes=len(t),
                         states_full_sample=bool(HEAD_PAT.search(t)),
                         states_IS_only=bool(IS_PAT.search(t))))
    C = pd.DataFrame(rows)
    n = len(C)
    P(f"{n} committed memo files under research/backtests/.")
    P(f"  quote a FULL-SAMPLE headline:            {int(C.states_full_sample.sum())} of {n} "
      f"({C.states_full_sample.mean():.4f})")
    P(f"  mention an IS-only reading anywhere:     {int(C.states_IS_only.sum())} of {n} "
      f"({C.states_IS_only.mean():.4f})")
    P(f"  FULL headline and NO IS-only reading:    "
      f"{int((C.states_full_sample & ~C.states_IS_only).sum())} of {n}")
    P("  (the IS-only detector is a regex over 'rule 8' / 'in-sample' / '<= 2016' / "
      "'2009-2016' / 'dials on IS'; it is DELIBERATELY loose, so this count is an UPPER "
      "bound on how many memos say anything IS-only at all.)")
    C.to_csv(f"{OUT}.census.csv", index=False)
    return C


# ----------------------------------------------------------------- rule 8 + both KEEP paths
def rule8(H, books, meta, panels, starts):
    hdr("RULE 8 — choose on the FIRST half (IS <= 2016-12-31), evaluate 2017+ untouched")
    sub = H[(H.cost == COST) & (H.split == HEAD_SPLIT.date())].set_index("book")
    live = sub.loc["LIVE"]
    rows = []
    for key in MEMO12:
        r = sub.loc[key]
        spy = sub.loc[f"SPY_{meta[key]['panel']}"]
        # 4a vs the LIVE book, on the POST (OOS) window's own halves
        rp = books[key].loc[books[key].index > HEAD_SPLIT]
        lp = books["LIVE"].loc[books["LIVE"].index > HEAD_SPLIT]
        sp_ = panels[meta[key]["panel"]]["SPY"].pct_change().fillna(0.0)
        sp_ = sp_.loc[sp_.index > HEAD_SPLIT]
        h = len(rp) // 2
        a1, a2 = sharpe_of(rp.values[:h]), sharpe_of(rp.values[h:])
        l1, l2 = sharpe_of(lp.values[:h]), sharpe_of(lp.values[h:])
        s1, s2 = sharpe_of(sp_.values[:h]), sharpe_of(sp_.values[h:])
        keep4a = bool(a1 > l1 and a2 > l2 and r.POST_MaxDD >= live.POST_MaxDD)
        legs4b = {"H1>SPY": a1 > s1, "H2>SPY": a2 > s2,
                  "full>SPY": r.POST_Sharpe > spy.POST_Sharpe,
                  "DD<=60%SPY": r.POST_MaxDD >= 0.6 * spy.POST_MaxDD,
                  "CAGR>=70%SPY": r.POST_CAGR >= 0.7 * spy.POST_CAGR}
        rows.append(dict(book=key, panel=r.panel,
                         IS_CAGR=r.IS_CAGR, IS_Sharpe=r.IS_Sharpe, IS_MaxDD=r.IS_MaxDD,
                         OOS_CAGR=r.POST_CAGR, OOS_Sharpe=r.POST_Sharpe,
                         OOS_MaxDD=r.POST_MaxDD, OOS_H1=a1, OOS_H2=a2,
                         keep4a="PASS" if keep4a else "FAIL",
                         keep4b="PASS" if all(legs4b.values()) else "FAIL",
                         fail4b="+".join(k for k, v in legs4b.items() if not v)))
    W = pd.DataFrame(rows).set_index("book")
    for tag, key in (("LIVE (baseline)", "LIVE"), ("SPY u56", "SPY_U56"),
                     ("SPY b136", "SPY_B136")):
        r = sub.loc[key]
        W.loc[tag] = dict(panel=r.panel, IS_CAGR=r.IS_CAGR, IS_Sharpe=r.IS_Sharpe,
                          IS_MaxDD=r.IS_MaxDD, OOS_CAGR=r.POST_CAGR, OOS_Sharpe=r.POST_Sharpe,
                          OOS_MaxDD=r.POST_MaxDD, OOS_H1=np.nan, OOS_H2=np.nan,
                          keep4a="-", keep4b="-", fail4b="-")
    P(W.to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"\nfixed-window-on-OOS: 4a {int((W.keep4a == 'PASS').sum())} of {len(MEMO12)} PASS, "
      f"4b {int((W.keep4b == 'PASS').sum())} of {len(MEMO12)} PASS.")

    body = W.loc[MEMO12]
    pick_is = body.IS_Sharpe.idxmax()
    pick_full = sub.loc[MEMO12].full_Sharpe.idxmax()
    best_oos = body.OOS_Sharpe.idxmax()
    P(f"\nThe rule-8 chooser: best book on the IS half ALONE (Sharpe <= 2016-12-31) is "
      f"{pick_is} ({body.loc[pick_is, 'IS_Sharpe']:.4f} IS) -> OOS "
      f"{body.loc[pick_is,'OOS_CAGR']:.2%} / {body.loc[pick_is,'OOS_Sharpe']:.4f} / "
      f"{body.loc[pick_is,'OOS_MaxDD']:.2%}.")
    P(f"The book the PUBLISHED (full-sample) headline would pick is {pick_full} -> OOS "
      f"{body.loc[pick_full,'OOS_CAGR']:.2%} / {body.loc[pick_full,'OOS_Sharpe']:.4f} / "
      f"{body.loc[pick_full,'OOS_MaxDD']:.2%}.")
    P(f"The OOS-best book is {best_oos} ({body.loc[best_oos,'OOS_Sharpe']:.4f}).  "
      f"Baseline LIVE OOS {W.loc['LIVE (baseline)','OOS_CAGR']:.2%} / "
      f"{W.loc['LIVE (baseline)','OOS_Sharpe']:.4f} / "
      f"{W.loc['LIVE (baseline)','OOS_MaxDD']:.2%}; SPY u56 OOS "
      f"{W.loc['SPY u56','OOS_CAGR']:.2%} / {W.loc['SPY u56','OOS_Sharpe']:.4f} / "
      f"{W.loc['SPY u56','OOS_MaxDD']:.2%}.")
    W.to_csv(f"{OUT}.wf.csv")
    return W, pick_is, pick_full, best_oos


# =====================================================================================
def main():
    t0 = time.time()
    P("=" * 112)
    P(f"# {DATE} cloud lane — IDEA 836: re-read every committed MEMO HEADLINE as an")
    P("#                  IS-ONLY number")
    P("=" * 112)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    for k, v in panels.items():
        P(f"panel {k:5s} {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"scored from {starts[k].date()} (C2)")
    P(f"next-day execution, no shorting, no leverage.  P1 memo set {list(MEMO_SETS)} | "
      f"P2 split {[s.date().isoformat() for s in SPLITS]} | cost {COSTS} bps and lead reading "
      f"{LEADS} reported at every point.")
    P("SURVIVORSHIP: universe.json and universe_broad.json are CURRENT-CONSTITUENT lists, so "
      "every LEVEL below is optimistic; the object here is a within-corpus ORDERING contrast, "
      "which survivorship inflates uniformly only if it hits every book equally — it does not, "
      "so the ordering statistics carry it too.")

    P("\nbuilding books at the PROTOCOL rung (one full-sample simulation each, C1):")
    books, meta = build(panels, COST, verbose=True)
    gates_g1g2(books, starts)
    gate_g3(books, panels)
    gate_g4(books, meta, starts)

    # ------------------------------------------------------------------ headlines
    Hs = [headlines(books, meta, panels, starts, COST)]
    for c in COSTS:
        if c == COST:
            continue
        P(f"  re-building every book at {c} bps for the reported cost rung ...")
        bk, _ = build(panels, c)
        Hs.append(headlines(bk, meta, panels, starts, c))
    H = pd.concat(Hs, ignore_index=True)
    H.to_csv(f"{OUT}.books.csv", index=False)

    hdr("EVERY COMMITTED HEADLINE, RE-READ AS AN IS-ONLY NUMBER "
        f"(split {HEAD_SPLIT.date()}, {COST} bps)")
    sub = H[(H.cost == COST) & (H.split == HEAD_SPLIT.date())].set_index("book")
    show = sub.loc[MEMO14 + ["SPY_U56", "SPY_B136"],
                   ["panel", "n_IS", "n_POST", "full_CAGR", "IS_CAGR", "POST_CAGR",
                    "full_Sharpe", "IS_Sharpe", "POST_Sharpe", "full_MaxDD", "IS_MaxDD",
                    "POST_MaxDD", "dd_identity"]]
    P(show.to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"\npost_share = {sub.post_share.iloc[0]:.4f} of every FULL window is the POST window "
      "itself — that is how much of each published headline is a restatement of the window the "
      "memo claims to be validated on.")

    g5_n = int(sub.loc[MEMO12].dd_identity.sum())
    P(f"GATE G5 — MaxDD identity count at the {HEAD_SPLIT.date()} split: {g5_n} of "
      f"{len(MEMO12)} books have full MaxDD == POST MaxDD to 1e-9, vs idea 833's committed "
      f"11 of 12 -> {'PASS' if g5_n == 11 else 'FAIL'}")

    # ------------------------------------------------------------------ the rank grid
    G, R = rank_grid(H)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.ranks.csv", index=False)

    hdr("THE DELIVERABLE — which memo's LEAD NUMBER changes rank when it is re-read IS-only")
    for lead in LEADS:
        P(f"\n--- lead reading = {lead}  ({HEAD_SET}, split {HEAD_SPLIT.date()}, {COST} bps) ---")
        r = R[R.lead == lead].set_index("book").reindex(MEMO12)
        P(r.to_string(float_format=lambda x: f"{x:+.4f}"))
        mv = r[r.disp > 0]
        P(f"  {len(mv)} of {len(r)} books change rank; max displacement "
          f"{r.disp.max():.0f} places ({r.disp.idxmax()}); "
          f"{int((r.disp >= 3).sum())} move >= 3 places.  "
          f"top-1 FULL = {r.rank_FULL.idxmin()}, top-1 IS-only = {r.rank_IS.idxmin()}, "
          f"top-1 POST = {r.rank_POST.idxmin()}.")

    hdr("THE FULL GRID — every (memo set x split x cost x lead reading) point")
    for lead in LEADS:
        P(f"\n--- lead = {lead}, cost {COST} bps ---")
        t = G[(G.lead == lead) & (G.cost == COST)][
            ["memo_set", "split", "n", "post_share", "rho_FULL_IS", "rho_FULL_POST",
             "rho_IS_POST", "contam", "perm95", "n_moved", "max_disp", "n_moved_ge3",
             "top1_FULL", "top1_IS", "top1_POST", "argmax_disp"]]
        P(t.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\n--- the same table at 0 and 25 bps, {HEAD_SET} only (reported, not selected) ---")
    P(G[(G.cost != COST) & (G.memo_set == HEAD_SET)][
        ["cost", "lead", "split", "rho_FULL_IS", "rho_FULL_POST", "rho_IS_POST", "contam",
         "n_moved", "max_disp", "top1_FULL", "top1_IS"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\nperm95 = two-sided 95% |rho| band of Spearman under {NPERM:,} fixed-seed label "
      "permutations at that n.  A |rho| below it is NOT distinguishable from noise.")

    # ------------------------------------------------------------------ stability across splits
    hdr("H_STABLE — is any headline's IS-ONLY rank order stable across the six splits?")
    st_rows = []
    for lead in LEADS:
        piv = {}
        for sp in SPLITS:
            s = H[(H.cost == COST) & (H.split == sp.date()) & (H.book.isin(MEMO12))]
            s = s.set_index("book").reindex(MEMO12)
            piv[sp.date()] = ranks_of(s, f"IS_{lead}")
        Pv = pd.DataFrame(piv)
        # Pv already holds RANKS, so plain Pearson on them IS Spearman (no scipy in the sandbox).
        rhos = [float(Pv[a].corr(Pv[b])) for a, b in combinations(Pv.columns, 2)]
        st_rows.append(dict(lead=lead, n_pairs=len(rhos), min_rho=min(rhos),
                            median_rho=float(np.median(rhos)), max_rho=max(rhos),
                            n_identical=int(sum(1 for r_ in rhos if abs(r_ - 1.0) < 1e-12))))
        P(f"\n--- IS-only rank of each book by {lead}, by split ---")
        P(Pv.to_string(float_format=lambda x: f"{x:.1f}"))
    S = pd.DataFrame(st_rows)
    P("\n" + S.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    C = memo_census()
    W, pick_is, pick_full, best_oos = rule8(H, books, meta, panels, starts)

    # ------------------------------------------------------------------ hypotheses
    hdr("PRE-REGISTERED HYPOTHESES")
    head = G[(G.cost == COST) & (G.memo_set == HEAD_SET) &
             (G.split == HEAD_SPLIT.date()) & (G.lead == HEAD_LEAD)].iloc[0]
    verd = {}
    verd["H_RANK"] = (head.n_moved_ge3 >= 1,
                      f"{head.n_moved_ge3} of {int(head.n)} books move >= 3 places on the lead "
                      f"number ({head.n_moved} move at all, max {head.max_disp:.0f} at "
                      f"{head.argmax_disp})")
    verd["H_TOP1"] = (bool(head.top1_changed),
                      f"top-1 FULL = {head.top1_FULL}, top-1 IS-only = {head.top1_IS}, "
                      f"top-1 POST = {head.top1_POST}")
    verd["H_RHO"] = (head.rho_FULL_IS < 0.90,
                     f"Spearman(FULL {HEAD_LEAD}, IS-only {HEAD_LEAD}) = "
                     f"{head.rho_FULL_IS:+.4f} vs bar 0.90 "
                     f"(n={int(head.n)}, perm95 {head.perm95:.4f})")
    cs = G[(G.cost == COST) & (G.memo_set == HEAD_SET) & (G.lead == HEAD_LEAD)]
    nc = int((cs.contam > 0).sum())
    verd["H_CONTAM"] = (nc >= 4,
                        f"rho(FULL,POST) > rho(IS,POST) at {nc} of {len(cs)} splits; "
                        f"median contamination {cs.contam.median():+.4f} "
                        f"(median rho_FULL_POST {cs.rho_FULL_POST.median():+.4f} vs "
                        f"rho_IS_POST {cs.rho_IS_POST.median():+.4f})")
    verd["H_MAXDD_ID"] = (g5_n >= 8,
                          f"{g5_n} of {len(MEMO12)} books have full MaxDD == POST MaxDD to 1e-9")
    verd["H_STABLE"] = (bool((S.min_rho < 1.0).all()),
                        "min pairwise Spearman across the 15 split pairs: " +
                        ", ".join(f"{r.lead} {r.min_rho:+.4f}" for r in S.itertuples()))
    verd["H_WF"] = (pick_is == best_oos,
                    f"IS-only pick {pick_is} vs OOS-best {best_oos} "
                    f"(the published-headline pick is {pick_full})")
    verd["H_CENSUS"] = (bool((~C.states_IS_only).mean() >= 0.50),
                        f"{int((~C.states_IS_only).sum())} of {len(C)} memo files state no "
                        f"IS-only reading ({(~C.states_IS_only).mean():.4f}) vs bar 0.50")
    for k, (ok, why) in verd.items():
        P(f"  {k:11s} {'PASS' if ok else 'FAIL'}  — {why}")
    P(f"\n{sum(1 for v in verd.values() if v[0])} of {len(verd)} pre-registered hypotheses PASS.")

    # ------------------------------------------------------------------ PROTOCOL rule 3
    hdr("PROTOCOL rule 3 — baseline.compare on the two books this reading promotes/demotes")
    for key in sorted({pick_is, best_oos, pick_full}):
        wfun = dict((c[0], c[3]) for c in CORPUS)[key]
        fr = dict((c[0], c[4]) for c in CORPUS)[key]
        P(f"\n--- {key}: {meta[key]['label']} ---")
        res = compare(f"836 cloud {key} {meta[key]['label']}", wfun,
                      panels[meta[key]["panel"]], freq=fr, cost_bps=COST)
        LOG.append(str(res["table"]))

    P(f"\nTotal runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.txt").write_text("\n".join(LOG) + "\n")
    return H, G, R, S, C, W, verd


if __name__ == "__main__":
    main()
