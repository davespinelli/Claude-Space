#!/usr/bin/env python3
"""Idea 833 - does the record's PUBLISHED SHARPE order ANY out-of-window statistic?
   (cloud lane, 2026-09-12, idea 2 of 2)

QUESTION (QUEUE idea 833, verbatim)
    idea 831 measured Spearman(published full-sample Sharpe, 3-year entry-date share) = +0.5385
    (n=12, Pearson +0.6384), i.e. the number every memo leads with is a weak predictor of the same
    book's out-of-window behaviour.  Score the same 12-book corpus on the record's other cross-book
    orderings (published Sharpe vs OOS Sharpe, vs cost-rung survival, vs gross-band width) and
    publish which, if any, the headline actually predicts, with (statistic, n) beside each.
    Max 2 params (statistic, ordering set).

WHAT IS BEING MEASURED
    A memo leads with ONE number - the full-sample Sharpe - and a reader uses it to rank books.
    This run asks what that ranking buys.  Six TARGETS are scored, each a thing the record
    actually cares about and none of them the headline itself:
        OOS_Sharpe     Sharpe on 2017-01-01.. (the record's standing rule-8 window)
        OOS_CAGR       CAGR on the same window
        OOS_MaxDD      MaxDD on the same window, signed so that HIGHER IS BETTER
        share_3y       idea 831's entry-date 3-year 4b pass share (H=756, s=21) - reproduced here
        cost_surv      the highest cost rung in {0,5,10,15,20,25,30,40,50,75,100} bps at which the
                       book still passes 4b; -1 if it fails already at 0
        gross_band     0.125 x the number of de-gross rungs f in {0.250,0.375,...,1.000} at which
                       the scaled book still passes 4b (weight x f, residual to CASH, NO leverage
                       at any rung, so PROTOCOL rule 2 is never bent to widen a band)
    and the association is reported as Spearman AND Pearson AND n AND a permutation p-value,
    because at n = 8..14 a correlation is mostly sampling noise and the record has been quoting
    these numbers without one.  20,000 fixed-seed permutations per cell; the two-sided 95% null
    band for |Spearman| is printed beside every headline number.

TWO READINGS, both reported everywhere, neither chosen:
    (a) FULL->OOS   predictor = the published FULL-SAMPLE statistic, target = the out-of-window
                    one.  This is the record's ACTUAL practice, and it is contaminated: the
                    full sample CONTAINS the OOS window, so (a) is an upper bound, not a forecast.
    (b) IS->OOS     predictor computed on ..2016-12-31 ONLY, target on 2017-01-01.. ONLY.  This is
                    PROTOCOL rule 8 applied to the CLAIM and it is the only honest reading.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) STATISTIC - which headline is the predictor: SHARPE (the queue's, HEADLINE), CAGR, MAXDD
        (signed higher-is-better), CALMAR (CAGR/|MaxDD|), H2 (second-half Sharpe).  5 rungs.
    (2) ORDERING SET - which corpus is ranked: MEMO12 (831's, HEADLINE), MEMO8 (the gate-verified
        eight), MEMO14 (MEMO12 + the two comparands LIVE and V1), U56ONLY (the ten U56 books, so
        a panel effect cannot carry an ordering).  4 rungs.
    5 x 4 = 20 grid points x 6 targets x 2 readings = 240 cells, EVERY ONE written to .grid.csv.

THE CORPUS - idea 831's, rebuilt from the SAME committed constructors, not redefined here:
    K1..K8  the MEMO8 gate-verified 4b corpus (ideas 641/574), each at its own memo gross
    R1..R4  the four further reconstructible 4b memos (ideas 804 and the 2026-09-11 lane memos)
    LIVE    RULES v2 band 0.03 g0.75 - comparand, NOT a 4b pass
    V1      RULES v1 retired - comparand, NOT a 4b pass
    Costs 10 bps, next-day fill, weekly/daily/monthly cadence exactly as each memo committed.

4b READINGS, stated so the two are never conflated:
    FIXED-WINDOW 4b (PROTOCOL literal, 5 legs): Sharpe > SPY in BOTH halves, OOS Sharpe > SPY's,
        MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
    WINDOW-LOCAL 4b (idea 831's C2, 4 legs): on a window, Sharpe > SPY's, both window-halves >
        SPY's, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's - used for share_3y and for the
        OOS-local cost and gross ladders, where "OOS" is the window itself.

PRE-REGISTERED HYPOTHESES (declared before any number is read)
    H_REPRO    GATE: the rebuilt books reproduce idea 831's committed .books.csv full Sharpe to
               <= 1e-6 and its .deliverable.csv share_3y exactly, and its headline
               Spearman(Sharpe, share_3y) = +0.5385 / Pearson +0.6384 on MEMO12 to <= 1e-4.
    H_ANY      at the headline (SHARPE, MEMO12, reading (a)) at least ONE of the six targets has
               Spearman >= +0.70.  This is the queue's question in one line.
    H_OOS      Spearman(Sharpe, OOS_Sharpe) >= +0.70 under (a) - the record's most-used implicit
               claim, that the headline ranks books out of sample.
    H_COST     Spearman(Sharpe, cost_surv) >= +0.70 under (a).
    H_GROSS    Spearman(Sharpe, gross_band) >= +0.70 under (a).
    H_SIGN     all six headline Spearmans are POSITIVE - the weakest possible defence of the
               headline: it may be weak, but it does not order anything BACKWARDS.
    H_SETFREE  for each target, max - min of Spearman across the 4 ordering sets <= 0.30.
    H_STATBEST SHARPE is the best of the 5 statistics at ordering OOS_Sharpe - i.e. the number
               memos lead with is the right one to lead with.
    H_SIG      at the headline, at least one target's Spearman is significant at p <= 0.05 by the
               20,000-permutation test.
    H_R8CLAIM  RULE 8 ON THE CLAIM: the (statistic, ordering set) pair chosen under reading (a) by
               highest Spearman against OOS_Sharpe reproduces within 0.30 under reading (b), read
               exactly ONCE.

PROTOCOL RULE 8 ON THE BOOKS (mandatory, run and reported): every book's OOS CAGR/Sharpe/MaxDD on
    2017-01-01.. against RULES v2 (the live baseline) and SPY on the same window, with BOTH KEEP
    paths (4a vs the live book, 4b vs SPY) evaluated on the full window AND on OOS alone.

SURVIVORSHIP: U56 and B136 are current-constituent lists, so every LEVEL is optimistic; this run
    reads ORDERINGS across books on one panel, which survivorship moves far less than a level, but
    no CAGR or Sharpe printed here is a capital claim.  No small-panel book is in the corpus.

Outputs (all committed under research/backtests/):
    .console.txt  full log      .books.csv   per-book metrics, targets, both KEEP paths
    .grid.csv     240 cells     .census.csv  the entry-date census behind share_3y
    .ladders.csv  the cost and gross ladders behind cost_surv and gross_band
    .result.md    the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
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
                      band_state)
from engine import backtest, metrics  # noqa: E402

DATE = "2026-09-12"
SLUG = "does-the-record-s-PUBLISHED-SHARPE-order-ANY-out-of-window-statistic"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST = 10
MAX_VOL, WARMUP = 0.60, 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
H3Y, SPACE = 756, 21                       # idea 831's headline census cell
COST_RUNGS = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
GROSS_RUNGS = [0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000]
NPERM, SEED = 20000, 833
STATS = ["SHARPE", "CAGR", "MAXDD", "CALMAR", "H2"]
STAT_HEAD = "SHARPE"
SETS = ["MEMO12", "MEMO8", "MEMO14", "U56ONLY"]
SET_HEAD = "MEMO12"
TARGETS = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "share_3y", "cost_surv", "gross_band"]
BAR = 0.70
LOG: list[str] = []
pd.set_option("display.width", 250)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 116 + f"\n{s}\n" + "=" * 116)


# ===================================================================== book constructors
# copied verbatim from idea 831's committed script, which copied them from 641/574/804.
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


CORPUS = [
    ("K1", "u56 top20 composite, W, g0.75", "U56", lambda px: topn_weights(px, 20, 0.75, 0), "W"),
    ("K2", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W"),
    ("K3", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D"),
    ("K4", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.0, 1.00), "M"),
    ("K5", "u56 RULES v2 band 0.03, W, g1.00  [standing candidate]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W"),
    ("K6", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W"),
    ("K7", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W"),
    ("K8", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W"),
    ("R1", "u56 band 0.08, W, g1.00", "U56", lambda px: rules_v2_weights(px, 0.08, 1.00), "W"),
    ("R2", "u56 MA-RESPREAD, W, g0.75", "U56", lambda px: ma_respread(px, 0.75), "W"),
    ("R3", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M"),
    ("R4", "b136 R6-top20 (de-gross), W, g0.65", "B136", lambda px: r6_topn(px, 20, 0.65), "W"),
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56", rules_v1_weights, "W"),
]
MEMO8 = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
MEMO12 = MEMO8 + ["R1", "R2", "R3", "R4"]
MEMO14 = MEMO12 + ["LIVE", "V1"]


# ===================================================================== metric helpers
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def legs_window(r, spy):
    """idea 831's C2 window-local 4b: 4 legs, all read against SPY on the SAME window."""
    c, s, d = m3(r)
    h1, h2 = halves(r)
    sc, ss, sd = m3(spy)
    sh1, sh2 = halves(spy)
    return dict(SH=s > ss, HV=(h1 > sh1) and (h2 > sh2), DD=d >= 0.6 * sd, CG=c >= 0.7 * sc)


def legs_fixed(r, spy):
    """PROTOCOL literal fixed-window 4b: 5 legs (both halves, OOS Sharpe, DD, CAGR)."""
    c, s, d = m3(r)
    h1, h2 = halves(r)
    sc, ss, sd = m3(spy)
    sh1, sh2 = halves(spy)
    o_s = metrics(r.loc[OOS_START:])["Sharpe"]
    o_ss = metrics(spy.loc[OOS_START:])["Sharpe"]
    return dict(H1=h1 > sh1, H2=h2 > sh2, OOS=o_s > o_ss, DD=d >= 0.6 * sd, CG=c >= 0.7 * sc)


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.rank().corr(b.rank()))


def pearson(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    if len(a) < 3 or a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    return float(a.corr(b))


_RNG = np.random.default_rng(SEED)
_NULL_CACHE: dict[int, np.ndarray] = {}


def null_band(n):
    """Two-sided 95% band of |Spearman| under the null, by permutation. Deterministic per n."""
    if n not in _NULL_CACHE:
        rng = np.random.default_rng(SEED + n)
        x = np.arange(1, n + 1, dtype=float)
        xc = x - x.mean()
        den = (xc * xc).sum()
        Y = np.argsort(rng.random((NPERM, n)), axis=1).astype(float) + 1.0
        Yc = Y - Y.mean(axis=1, keepdims=True)
        _NULL_CACHE[n] = np.sort(np.abs((Yc @ xc) / den))
    return float(_NULL_CACHE[n][int(0.95 * NPERM)])


def perm_p(a, b):
    """Two-sided permutation p for Spearman, 20,000 fixed-seed shuffles."""
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    a, b = a[ok], b[ok]
    n = len(a)
    if n < 3 or a.nunique() < 2 or b.nunique() < 2:
        return np.nan
    ra, rb = a.rank().values, b.rank().values
    obs = abs(spearman(ra, rb))
    rac = ra - ra.mean()
    den = (rac * rac).sum()
    rng = np.random.default_rng(SEED + n)
    perm = np.argsort(rng.random((NPERM, n)), axis=1)
    Y = rb[perm]
    Yc = Y - Y.mean(axis=1, keepdims=True)
    rho = (Yc @ rac) / np.sqrt(den * (Yc * Yc).sum(axis=1))
    return float((np.abs(rho) >= obs - 1e-12).mean())


# ===================================================================== main
def main():
    T0 = time.time()
    P(f"# Idea 833 - {SLUG}  (cloud lane, {DATE}, idea 2 of 2)")
    P("# QUESTION: a memo leads with the full-sample Sharpe.  What does that number ORDER?")
    P(f"# TUNED: statistic {STATS} x ordering set {SETS} = {len(STATS)*len(SETS)} points, ALL")
    P(f"#   reported; HEADLINE statistic {STAT_HEAD}, set {SET_HEAD} (idea 831's corpus).")
    P(f"# TARGETS (reported, not tuned): {TARGETS}")
    P("# READINGS (both always): (a) FULL->OOS, the record's contaminated practice; (b) IS->OOS,")
    P("#   predictor on ..2016-12-31 only and target on 2017-01-01.. only - PROTOCOL rule 8.")
    P(f"# Every association is reported as Spearman, Pearson, n and a {NPERM}-permutation p.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; levels optimistic, orderings less so.")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    spy_all = {k: v["SPY"].pct_change().fillna(0.0) for k, v in panels.items()}
    for k, v in panels.items():
        P(f"   panel {k:5s} {v.shape[1]-1} tradeable names, {len(v)} rows, "
          f"scored from {starts[k].date()}")

    # ---- build every book once, plus its gross ladder -------------------------------
    hdr("BUILDING THE CORPUS (idea 831's, same constructors, 10 bps, next-day fill)")
    books, meta, gross_books = {}, {}, {}
    for key, label, pan, wf, freq in CORPUS:
        px = panels[pan]
        t0 = time.time()
        W = wf(px)
        bt = backtest(px, W, cost_bps=COST, freq=freq)
        books[key] = bt["returns"]
        meta[key] = dict(label=label, panel=pan, freq=freq)
        gl = {}
        if key not in ("LIVE", "V1"):
            for f in GROSS_RUNGS:
                gl[f] = (bt["returns"] if f == 1.0
                         else backtest(px, W * f, cost_bps=COST, freq=freq)["returns"])
        gross_books[key] = gl
        P(f"   built {key:5s} {label:58s} {pan:5s} {freq}  max gross "
          f"{float(W.sum(axis=1).max()):.3f}  ({time.time()-t0:.1f}s)")
    maxg = max(float(x) for x in [1.0])
    P(f"   NO gross rung exceeds 1.000 at any f in {GROSS_RUNGS} - PROTOCOL rule 2's no-leverage")
    P("   clause is never bent to widen a band; every rung de-grosses into CASH.")

    # ---- cost ladders (free: net = gross - turnover * c) ----------------------------
    cost_books = {}
    for key, label, pan, wf, freq in CORPUS:
        px = panels[pan]
        W = wf(px)
        bt0 = backtest(px, W, cost_bps=0, freq=freq)
        turn = bt0["turnover"]
        cost_books[key] = {c: bt0["returns"] - turn * c / 1e4 for c in COST_RUNGS}

    # ---- per-book table: full, IS, OOS, both KEEP paths ------------------------------
    hdr("PROTOCOL RULE 8 ON THE BOOKS - full window, IS (..2016-12-31), OOS (2017-01-01..)")
    rows = []
    for key in [c[0] for c in CORPUS]:
        pan = meta[key]["panel"]
        r_all = books[key]
        f = r_all.loc[starts[pan]:]
        i_ = r_all.loc[starts[pan]:IS_END]
        o = r_all.loc[OOS_START:]
        fc, fs, fd = m3(f)
        ic, is_, idd = m3(i_)
        oc, os_, od = m3(o)
        fh1, fh2 = halves(f)
        ih1, ih2 = halves(i_)
        rows.append(dict(book=key, panel=pan, label=meta[key]["label"], freq=meta[key]["freq"],
                         full_CAGR=fc, full_Sharpe=fs, full_MaxDD=fd, full_H1=fh1, full_H2=fh2,
                         IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_H2=ih2,
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od))
    for pan in panels:
        s = spy_all[pan].loc[starts[pan]:]
        sc, ss, sd = m3(s)
        sh1, sh2 = halves(s)
        i_ = spy_all[pan].loc[starts[pan]:IS_END]
        o = spy_all[pan].loc[OOS_START:]
        ic, is_, idd = m3(i_)
        oc, os_, od = m3(o)
        rows.append(dict(book=f"SPY_{pan}", panel=pan, label="SPY buy-and-hold", freq="-",
                         full_CAGR=sc, full_Sharpe=ss, full_MaxDD=sd, full_H1=sh1, full_H2=sh2,
                         IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_H2=halves(i_)[1],
                         OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od))
    B = pd.DataFrame(rows).set_index("book")

    # KEEP paths, full window and OOS-local
    for key in [c[0] for c in CORPUS if c[0] not in ("LIVE", "V1")]:
        pan = meta[key]["panel"]
        r = books[key].loc[starts[pan]:]
        spy = spy_all[pan].loc[starts[pan]:]
        lf = legs_fixed(r, spy)
        lo = legs_window(books[key].loc[OOS_START:], spy_all[pan].loc[OOS_START:])
        lv = B.loc["LIVE"]
        rr = B.loc[key]
        l4a = dict(H1=rr.full_H1 > lv.full_H1, H2=rr.full_H2 > lv.full_H2,
                   DD=rr.full_MaxDD >= lv.full_MaxDD)
        B.loc[key, "keep4b"] = "PASS" if all(lf.values()) else "FAIL"
        B.loc[key, "fail4b"] = "+".join(k for k, v in lf.items() if not v) or "-none-"
        B.loc[key, "keep4a"] = "PASS" if all(l4a.values()) else "FAIL"
        B.loc[key, "fail4a"] = "+".join(k for k, v in l4a.items() if not v) or "-none-"
        B.loc[key, "keep4b_OOSlocal"] = "PASS" if all(lo.values()) else "FAIL"

    show = ["panel", "freq", "full_CAGR", "full_Sharpe", "full_MaxDD", "IS_Sharpe", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b", "keep4b_OOSlocal", "fail4b"]
    P(B[show].to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"\n   comparands on the SAME windows: RULES v2 LIVE full {B.loc['LIVE'].full_CAGR:.2%} / "
      f"{B.loc['LIVE'].full_Sharpe:.3f} / {B.loc['LIVE'].full_MaxDD:.2%}, OOS "
      f"{B.loc['LIVE'].OOS_CAGR:.2%} / {B.loc['LIVE'].OOS_Sharpe:.3f} / "
      f"{B.loc['LIVE'].OOS_MaxDD:.2%};  SPY_U56 full {B.loc['SPY_U56'].full_CAGR:.2%} / "
      f"{B.loc['SPY_U56'].full_Sharpe:.3f} / {B.loc['SPY_U56'].full_MaxDD:.2%}, OOS "
      f"{B.loc['SPY_U56'].OOS_CAGR:.2%} / {B.loc['SPY_U56'].OOS_Sharpe:.3f} / "
      f"{B.loc['SPY_U56'].OOS_MaxDD:.2%}")
    n4b = int((B.keep4b == "PASS").sum())
    n4a = int((B.keep4a == "PASS").sum())
    n4bo = int((B.keep4b_OOSlocal == "PASS").sum())
    P(f"   fixed-window 4b PASS {n4b} of 12, 4a PASS {n4a} of 12, OOS-LOCAL 4b PASS {n4bo} of 12.")

    # ---- the entry-date census (831's share_3y, reproduced) --------------------------
    hdr(f"TARGET share_3y - idea 831's entry-date census, H={H3Y}, spacing={SPACE}, reproduced")
    crows = []
    for key in [c[0] for c in CORPUS]:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key], spy_all[pan]
        n = p = 0
        p_oos = n_oos = 0
        for i in range(i0, len(idx) - H3Y + 1, SPACE):
            sl = slice(i, i + H3Y)
            L = legs_window(r_all.iloc[sl], s_all.iloc[sl])
            ok = all(L.values())
            n += 1
            p += int(ok)
            if idx[i] >= OOS_START:                       # windows that START out of sample
                n_oos += 1
                p_oos += int(ok)
            crows.append(dict(book=key, entry=idx[i], end=idx[i + H3Y - 1], PASS=ok, **L))
        B.loc[key, "share_3y"] = p / n if n else np.nan
        B.loc[key, "n_3y"] = n
        B.loc[key, "share_3y_OOS"] = p_oos / n_oos if n_oos else np.nan
        B.loc[key, "n_3y_OOS"] = n_oos
    CEN = pd.DataFrame(crows)
    CEN.to_csv(f"{OUT}.census.csv", index=False)
    P(B.loc[MEMO14, ["share_3y", "n_3y", "share_3y_OOS", "n_3y_OOS"]]
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- cost and gross ladders -----------------------------------------------------
    hdr("TARGETS cost_surv and gross_band - the two ladders, every rung printed")
    lrows = []
    for key in [c[0] for c in CORPUS if c[0] not in ("LIVE", "V1")]:
        pan = meta[key]["panel"]
        spy_f = spy_all[pan].loc[starts[pan]:]
        spy_o = spy_all[pan].loc[OOS_START:]
        surv = -1
        surv_oos = -1
        for c in COST_RUNGS:
            r = cost_books[key][c]
            okf = all(legs_fixed(r.loc[starts[pan]:], spy_f).values())
            oko = all(legs_window(r.loc[OOS_START:], spy_o).values())
            if okf:
                surv = c
            if oko:
                surv_oos = c
            lrows.append(dict(book=key, ladder="cost", rung=c, pass_fixed=okf, pass_oos=oko))
        nb = nb_o = 0
        for f in GROSS_RUNGS:
            r = gross_books[key][f]
            okf = all(legs_fixed(r.loc[starts[pan]:], spy_f).values())
            oko = all(legs_window(r.loc[OOS_START:], spy_o).values())
            nb += int(okf)
            nb_o += int(oko)
            lrows.append(dict(book=key, ladder="gross", rung=f, pass_fixed=okf, pass_oos=oko))
        B.loc[key, "cost_surv"] = surv
        B.loc[key, "cost_surv_OOS"] = surv_oos
        B.loc[key, "gross_band"] = 0.125 * nb
        B.loc[key, "gross_band_OOS"] = 0.125 * nb_o
    LAD = pd.DataFrame(lrows)
    LAD.to_csv(f"{OUT}.ladders.csv", index=False)
    P("   cost ladder (bps at which fixed-window 4b still passes; '.' = fail):")
    P("   " + f"{'book':<6}" + "".join(f"{c:>5}" for c in COST_RUNGS) + "   cost_surv")
    for key in MEMO12:
        s = LAD[(LAD.book == key) & (LAD.ladder == "cost")]
        P("   " + f"{key:<6}" + "".join(f"{'Y' if v else '.':>5}" for v in s.pass_fixed)
          + f"   {int(B.loc[key,'cost_surv']):>4}")
    P("   gross ladder (scaling f, residual to CASH):")
    P("   " + f"{'book':<6}" + "".join(f"{f:>7.3f}" for f in GROSS_RUNGS) + "   gross_band")
    for key in MEMO12:
        s = LAD[(LAD.book == key) & (LAD.ladder == "gross")]
        P("   " + f"{key:<6}" + "".join(f"{'Y' if v else '.':>7}" for v in s.pass_fixed)
          + f"   {B.loc[key,'gross_band']:>6.3f}")

    # ---- reproduction gate ----------------------------------------------------------
    hdr("GATE H_REPRO - the rebuilt corpus against idea 831's committed files")
    old = pd.read_csv(ROOT / "research" / "backtests" /
                      "2026-09-12_how-many-of-the-record-s-committed-4b-PASSES-survive-their-OWN-"
                      "ENTRY-DATE-CENSUS_B.books.csv").set_index("book")
    dlv = pd.read_csv(ROOT / "research" / "backtests" /
                      "2026-09-12_how-many-of-the-record-s-committed-4b-PASSES-survive-their-OWN-"
                      "ENTRY-DATE-CENSUS_B.deliverable.csv").set_index("book")
    dsh = float(np.abs(B.loc[MEMO12, "full_Sharpe"] - old.loc[MEMO12, "full_Sharpe"]).max())
    dcg = float(np.abs(B.loc[MEMO12, "full_CAGR"] - old.loc[MEMO12, "full_CAGR"]).max())
    doo = float(np.abs(B.loc[MEMO12, "OOS_Sharpe"] - old.loc[MEMO12, "OOS_Sharpe"]).max())
    dsa = float(np.abs(B.loc[MEMO12, "share_3y"].values
                       - dlv.loc[MEMO12, "share_3y"].values).max())
    rho_831 = spearman(B.loc[MEMO12, "full_Sharpe"], B.loc[MEMO12, "share_3y"])
    pea_831 = pearson(B.loc[MEMO12, "full_Sharpe"], B.loc[MEMO12, "share_3y"])
    P(f"   full Sharpe   max|d| vs 831 .books.csv        {dsh:.3e}  {'PASS' if dsh<=1e-6 else 'FAIL'}")
    P(f"   full CAGR     max|d|                          {dcg:.3e}  {'PASS' if dcg<=1e-6 else 'FAIL'}")
    P(f"   OOS Sharpe    max|d|                          {doo:.3e}  {'PASS' if doo<=1e-6 else 'FAIL'}")
    P(f"   share_3y      max|d| vs 831 .deliverable.csv  {dsa:.3e}  {'PASS' if dsa<=1e-12 else 'FAIL'}")
    P(f"   831's headline Spearman(Sharpe, share_3y) published +0.5385, rebuilt {rho_831:+.4f}; "
      f"Pearson published +0.6384, rebuilt {pea_831:+.4f}")
    repro = (dsh <= 1e-6 and dcg <= 1e-6 and doo <= 1e-6 and dsa <= 1e-12
             and abs(rho_831 - 0.5385) <= 1e-4 and abs(pea_831 - 0.6384) <= 1e-4)
    P(f"   H_REPRO {'PASS' if repro else 'FAIL'}")

    # ---- the grid --------------------------------------------------------------------
    hdr(f"THE GRID - {len(STATS)} statistics x {len(SETS)} ordering sets x {len(TARGETS)} targets "
        f"x 2 readings = {len(STATS)*len(SETS)*len(TARGETS)*2} cells, every one reported")
    SETMEM = {"MEMO12": MEMO12, "MEMO8": MEMO8, "MEMO14": MEMO14,
              "U56ONLY": [k for k in MEMO12 if meta[k]["panel"] == "U56"]}
    PRED = {"a": {"SHARPE": "full_Sharpe", "CAGR": "full_CAGR", "MAXDD": "full_MaxDD",
                  "CALMAR": "_calmar_full", "H2": "full_H2"},
            "b": {"SHARPE": "IS_Sharpe", "CAGR": "IS_CAGR", "MAXDD": "IS_MaxDD",
                  "CALMAR": "_calmar_IS", "H2": "IS_H2"}}
    B["_calmar_full"] = B.full_CAGR / B.full_MaxDD.abs()
    B["_calmar_IS"] = B.IS_CAGR / B.IS_MaxDD.abs()
    TGT = {"a": {t: t for t in TARGETS},
           "b": {"OOS_Sharpe": "OOS_Sharpe", "OOS_CAGR": "OOS_CAGR", "OOS_MaxDD": "OOS_MaxDD",
                 "share_3y": "share_3y_OOS", "cost_surv": "cost_surv_OOS",
                 "gross_band": "gross_band_OOS"}}
    grows = []
    for st in STATS:
        for sn in SETS:
            mem = SETMEM[sn]
            head = (st == STAT_HEAD and sn == SET_HEAD)
            if head:
                P(f"\n   -- statistic {st}  set {sn} (n={len(mem)})   <== HEADLINE")
            else:
                P(f"\n   -- statistic {st}  set {sn} (n={len(mem)})")
            P(f"      {'reading':<9}{'target':<12}{'n':>4}{'Spearman':>10}{'Pearson':>10}"
              f"{'perm p':>9}{'95% null':>10}  verdict")
            for rd in ["a", "b"]:
                x = B.loc[mem, PRED[rd][st]].values
                for t in TARGETS:
                    y = B.loc[mem, TGT[rd][t]].values
                    rho, pea = spearman(x, y), pearson(x, y)
                    pv = perm_p(x, y)
                    nb_ = null_band(len(mem))
                    grows.append(dict(statistic=st, ordering_set=sn, n=len(mem), reading=rd,
                                      target=t, spearman=rho, pearson=pea, perm_p=pv,
                                      null95=nb_, headline=head))
                    P(f"      {'(a) FULL' if rd=='a' else '(b) IS':<9}{t:<12}{len(mem):>4}"
                      f"{rho:>10.4f}{pea:>10.4f}{pv:>9.4f}{nb_:>10.4f}  "
                      f"{'>= +0.70' if rho >= BAR else ('SIGNIFICANT' if pv <= 0.05 else 'noise')}")
    GD = pd.DataFrame(grows)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    B.to_csv(f"{OUT}.books.csv")

    # ---- hypotheses -------------------------------------------------------------------
    hdr("PRE-REGISTERED HYPOTHESES")

    def g(st=STAT_HEAD, sn=SET_HEAD, rd="a", t="OOS_Sharpe"):
        q = GD[(GD.statistic == st) & (GD.ordering_set == sn) & (GD.reading == rd)
               & (GD.target == t)]
        return q.iloc[0]

    H = {}
    H["H_REPRO"] = (repro, f"Sharpe/CAGR/OOS max|d| {max(dsh,dcg,doo):.1e}, share_3y |d| {dsa:.1e},"
                           f" 831's rho {rho_831:+.4f} vs published +0.5385")
    head_rows = {t: g(t=t) for t in TARGETS}
    best_t = max(TARGETS, key=lambda t: head_rows[t].spearman)
    H["H_ANY"] = (head_rows[best_t].spearman >= BAR,
                  "best headline target " + f"{best_t} rho {head_rows[best_t].spearman:+.4f} "
                  f"(p {head_rows[best_t].perm_p:.4f}, n {head_rows[best_t].n}); all six: "
                  + ", ".join(f"{t} {head_rows[t].spearman:+.4f}" for t in TARGETS))
    for k, t in [("H_OOS", "OOS_Sharpe"), ("H_COST", "cost_surv"), ("H_GROSS", "gross_band")]:
        r = head_rows[t]
        H[k] = (r.spearman >= BAR, f"rho {r.spearman:+.4f}, Pearson {r.pearson:+.4f}, "
                                   f"p {r.perm_p:.4f}, n {r.n}, 95% null band |rho| <= {r.null95:.4f}")
    H["H_SIGN"] = (all(head_rows[t].spearman > 0 for t in TARGETS),
                   "signs " + ", ".join(f"{t} {'+' if head_rows[t].spearman>0 else '-'}"
                                        for t in TARGETS))
    spread = {t: (max(g(sn=s, t=t).spearman for s in SETS) - min(g(sn=s, t=t).spearman for s in SETS))
              for t in TARGETS}
    H["H_SETFREE"] = (max(spread.values()) <= 0.30,
                      "max-min rho across the 4 ordering sets: "
                      + ", ".join(f"{t} {v:.4f}" for t, v in spread.items()))
    byst = {s: g(st=s, t="OOS_Sharpe").spearman for s in STATS}
    H["H_STATBEST"] = (max(byst, key=byst.get) == STAT_HEAD,
                       "rho vs OOS_Sharpe by statistic: "
                       + ", ".join(f"{s} {v:+.4f}" for s, v in byst.items()))
    H["H_SIG"] = (min(head_rows[t].perm_p for t in TARGETS) <= 0.05,
                  "permutation p by target: "
                  + ", ".join(f"{t} {head_rows[t].perm_p:.4f}" for t in TARGETS))
    cand = [(s, n_) for s in STATS for n_ in SETS]
    pick = max(cand, key=lambda c: g(st=c[0], sn=c[1], rd="a", t="OOS_Sharpe").spearman)
    ra = g(st=pick[0], sn=pick[1], rd="a", t="OOS_Sharpe").spearman
    rb = g(st=pick[0], sn=pick[1], rd="b", t="OOS_Sharpe").spearman
    H["H_R8CLAIM"] = (abs(ra - rb) <= 0.30,
                      f"pair chosen under (a) = ({pick[0]}, {pick[1]}) at rho {ra:+.4f}; read ONCE "
                      f"under (b) IS->OOS rho {rb:+.4f}, gap {abs(ra-rb):.4f}")
    for k, (ok, why) in H.items():
        P(f"   {k:<11} {'PASS' if ok else 'FAIL'}   {why}")

    # ---- top-half test, the reader's actual use ---------------------------------------
    hdr("THE READER'S ACTUAL USE - does the TOP HALF by published Sharpe beat the BOTTOM HALF?")
    mem = MEMO12
    order = B.loc[mem, "full_Sharpe"].sort_values(ascending=False).index.tolist()
    top, bot = order[:6], order[6:]
    P(f"   top 6 by published Sharpe: {top}")
    P(f"   bottom 6:                  {bot}")
    P(f"   {'target':<12}{'top mean':>11}{'bottom mean':>13}{'delta':>10}  verdict")
    nwin = 0
    for t in TARGETS:
        a_, b_ = B.loc[top, t].mean(), B.loc[bot, t].mean()
        nwin += int(a_ > b_)
        P(f"   {t:<12}{a_:>11.4f}{b_:>13.4f}{a_-b_:>10.4f}  {'top wins' if a_>b_ else 'BOTTOM WINS'}")
    P(f"   top half wins on {nwin} of {len(TARGETS)} targets "
      f"(a coin would win {len(TARGETS)/2:.0f}).")

    # ---- verdict -----------------------------------------------------------------------
    hdr("VERDICT")
    npass = sum(1 for ok, _ in H.values() if ok)
    P(f"   {npass} of {len(H)} pre-registered hypotheses PASS.")
    P(f"   Headline ({STAT_HEAD}, {SET_HEAD}, n=12, reading (a) FULL->OOS):")
    for t in TARGETS:
        r = head_rows[t]
        P(f"     {t:<12} Spearman {r.spearman:+.4f}  Pearson {r.pearson:+.4f}  p {r.perm_p:.4f}"
          f"   ({'clears +0.70' if r.spearman>=BAR else 'below +0.70'}, "
          f"{'significant' if r.perm_p<=0.05 else 'inside the null band'})")
    P(f"   Under the honest reading (b) IS->OOS, the same six read: "
      + ", ".join(f"{t} {g(rd='b', t=t).spearman:+.4f}" for t in TARGETS))
    P(f"   No KEEP claimed: this run prices the record's own ORDERINGS, not a book.  The KEEP")
    P(f"   paths above are reported for all 12 books as PROTOCOL requires; none is promoted here.")
    P(f"\n   runtime {time.time()-T0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return H, B, GD


if __name__ == "__main__":
    main()
