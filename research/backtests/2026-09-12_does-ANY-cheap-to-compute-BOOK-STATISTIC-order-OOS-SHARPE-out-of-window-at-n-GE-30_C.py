#!/usr/bin/env python3
"""Idea 837 - does ANY cheap-to-compute BOOK STATISTIC order OOS SHARPE out of window at n >= 30?
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 837, verbatim)
    idea 833 found the published Sharpe orders nothing out of window at n=12, but n=12 cannot
    separate rho 0.5 from noise in either direction.  Build a 30+ book corpus from the record's
    already-committed arm tables (no new constructors) and re-run the same six-target census so
    the null band is narrow enough for a NULL to mean something.
    Max 2 params (corpus source, statistic set).

WHAT THIS RUN IS FOR
    833's answer was "no ordering survives", but its own honest caveat was that at n = 12 the
    two-sided 95% null band for |Spearman| is 0.5804 - i.e. the study could not have detected a
    real rho of 0.5 and could not have refuted one either.  The queue's remedy is more books.
    This run supplies them, and then asks the harder question the remedy raises: does widening
    n from 12 to 39 actually narrow the band, when the 39 books are 14 families of near-duplicate
    arms rather than 39 independent draws?  Both nulls are reported side by side at every cell:
        iid permutation null      833's, 20,000 fixed-seed shuffles of the target vector
        CLUSTER BOOTSTRAP 95% CI  10,000 fixed-seed resamples of the 14 FAMILIES with replacement
    A rho whose cluster CI covers 0 is not resolved by this corpus however many arms it contains.

NO NEW CONSTRUCTORS.  Every book below is an arm of a weights function already committed in
    research/backtests/2026-09-12_does-the-record-s-PUBLISHED-SHARPE-order-ANY-out-of-window-
    statistic_cloud.py (idea 833), which copied them verbatim from ideas 831 / 641 / 574 / 804.
    The only thing added here is more RUNGS of the dial each family was already swept on, so
    idea 833's MEMO12 corpus is a strict SUBSET of this one (gate G1 checks that book by book).

TARGETS - the same six as 833, none of them the predictor itself:
    OOS_Sharpe   Sharpe on 2017-01-01.. (the record's standing rule-8 window)   [the queue's]
    OOS_CAGR     CAGR on the same window
    OOS_MaxDD    MaxDD on the same window (signed as-is, so HIGHER IS BETTER)
    share_3y     idea 831's entry-date 3-year window-local 4b pass share (H=756, s=21)
    cost_surv    highest rung in {0,5,10,15,20,25,30,40,50,75,100} bps still passing 4b; -1 if none
    gross_band   0.125 x the number of de-gross rungs f in {0.250..1.000} still passing 4b
    All six are oriented HIGHER IS BETTER, so a positive Spearman means the statistic orders the
    corpus the way a reader would want it to.

PREDICTORS - ten cheap-to-compute book statistics, each oriented HIGHER IS BETTER:
    SHARPE  CAGR  MAXDD  CALMAR  SORTINO  WINRATE  H1  H2  NEGVOL (= -annualised vol)
    NEGTURN (= -turnover per year).  Every one is read straight off the book's own return series;
    none needs an extra backtest.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) CORPUS SOURCE - which set of books is ranked.  4 rungs:
        ARMS39    all 39 arms                                        <== HEADLINE (n = 39 >= 30)
        MEMO12    idea 833's twelve, rebuilt here - the replication comparand and the n=12 control
        U56ARMS   the 29 U56 arms, so a cross-panel effect cannot carry an ordering
        FAMMEAN14 the 14 family means (mean rank of predictor, mean rank of target per family) -
                  the cluster control: this is what n=39 is really worth if arms inside a family
                  are one observation.
    (2) STATISTIC SET - which predictors are read.  2 rungs:
        CORE5   SHARPE, CAGR, MAXDD, CALMAR, H2   (idea 833's five)  <== HEADLINE
        WIDE10  CORE5 + SORTINO, WINRATE, H1, NEGVOL, NEGTURN
    Every statistic in WIDE10 is reported at every corpus rung anyway, so the grid is
    4 corpora x 10 statistics x 6 targets x 2 readings = 480 cells, ALL written to .grid.csv.
    The tuned pair only decides which cell is called the HEADLINE.

TWO READINGS, both reported everywhere, neither chosen (833's, kept so the two runs are comparable)
    (a) FULL->OOS   predictor = the FULL-SAMPLE statistic, target = the out-of-window one.  This
                    is the record's ACTUAL practice and it is CONTAMINATED: the full sample
                    contains the OOS window.  An upper bound, not a forecast.
    (b) IS->OOS     predictor on ..2016-12-31 ONLY, target on 2017-01-01.. ONLY.  PROTOCOL rule 8
                    applied to the CLAIM, and the only honest reading.

PRE-REGISTERED HYPOTHESES (declared here before any number was read)
    H_REPRO    GATE: the 12 MEMO books rebuilt as arms reproduce idea 833's committed .books.csv
               full Sharpe / full CAGR / OOS Sharpe / share_3y to <= 1e-9, and 833's headline cell
               Spearman(SHARPE, MEMO12, (a), OOS_Sharpe) = +0.6084 to <= 1e-4.
    H_N30      GATE: the headline corpus has n >= 30 - the queue's whole premise.
    H_NARROW   the iid 95% null band at the headline corpus is <= 0.35, i.e. n >= 30 buys the
               resolution the queue asked for.
    H_ANY      at least ONE of the ten statistics orders OOS_Sharpe at Spearman >= +0.70 on
               ARMS39 under the honest reading (b).  This is the queue's question in one line.
    H_ANY_A    the same under the contaminated reading (a).
    H_SHARPE   SHARPE itself - the number every memo leads with - reaches +0.70 under (b).
    H_SIG      at least one of the ten is significant at iid p <= 0.05 under (b).
    H_CLUSTER  at least one of the ten has a cluster-bootstrap 95% CI that EXCLUDES 0 under (b).
    H_SIGN     all ten Spearmans vs OOS_Sharpe under (b) are POSITIVE - the weakest possible
               defence: the statistics may be weak but they do not order backwards.
    H_REPLIC   widening n CONFIRMS 833: the sign of Spearman(SHARPE, target) under (b) agrees
               with 833's MEMO12 reading on all six targets.
    H_SETFREE  max - min of Spearman(SHARPE, OOS_Sharpe) across the 4 corpus rungs <= 0.30.
    H_STATBEST SHARPE is the best of the ten at ordering OOS_Sharpe under (b) - i.e. the number
               memos lead with is the right one to lead with.
    H_IDENT    833's identity finding generalises: >= 0.75 of the 39 books have full-sample MaxDD
               EQUAL to their OOS MaxDD to 1e-9, so the published drawdown is largely a
               restatement of the window it is validated on.
    H_R8CLAIM  RULE 8 ON THE CLAIM: the (statistic, corpus) pair chosen under (a) by highest
               Spearman vs OOS_Sharpe reproduces within 0.30 under (b).  Read exactly ONCE.

GATES (printed before any new number is interpreted)
    G1  MEMO12 arms reproduce idea 833's committed books.csv (H_REPRO above).
    G2  the free cost ladder at rung 10 bps equals the 10-bps backtest to <= 1e-12, every book.
    G3  the gross ladder at f = 1.000 is the base book exactly, every book.
    G4  no book's realised gross exceeds 1.000 at any rung - PROTOCOL rule 2's no-leverage clause
        is never bent to widen a band; every rung de-grosses into CASH.

PROTOCOL RULE 8 ON THE BOOKS (mandatory, run and reported): every book's CAGR/Sharpe/MaxDD on the
    full window, on IS (..2016-12-31) and on OOS (2017-01-01..) against RULES v2 (the live
    baseline), RULES v1 and SPY on the same windows, with BOTH KEEP paths evaluated - 4a against
    the live book, 4b against SPY - on the fixed window AND on OOS alone.

SURVIVORSHIP: U56 and B136 are current-constituent lists, so every LEVEL printed here is
    optimistic.  This run reads ORDERINGS ACROSS books on one panel, which survivorship moves far
    less than a level, but no CAGR or Sharpe below is a capital claim.  No small-panel book is in
    the corpus.

Outputs (all committed under research/backtests/):
    .console.txt  full log       .books.csv   per-book metrics, predictors, targets, KEEP paths
    .grid.csv     480 cells      .census.csv  the entry-date census behind share_3y
    .ladders.csv  cost and gross ladders      .cluster.csv  cluster-bootstrap CIs
    .walkforward.csv  rule 8 on the books     .result.md   the answer
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
SLUG = "does-ANY-cheap-to-compute-BOOK-STATISTIC-order-OOS-SHARPE-out-of-window-at-n-GE-30"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST = 10
MAX_VOL, WARMUP = 0.60, 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
H3Y, SPACE = 756, 21                       # idea 831's headline census cell, unchanged
COST_RUNGS = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
GROSS_RUNGS = [0.250, 0.375, 0.500, 0.625, 0.750, 0.875, 1.000]
NPERM, NBOOT, SEED = 20000, 10000, 837
CORE5 = ["SHARPE", "CAGR", "MAXDD", "CALMAR", "H2"]
WIDE10 = CORE5 + ["SORTINO", "WINRATE", "H1", "NEGVOL", "NEGTURN"]
STATSETS = {"CORE5": CORE5, "WIDE10": WIDE10}
SET_HEAD = "CORE5"
CORPORA = ["ARMS39", "MEMO12", "U56ARMS", "FAMMEAN14"]
CORP_HEAD = "ARMS39"
TARGETS = ["OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "share_3y", "cost_surv", "gross_band"]
TGT_HEAD = "OOS_Sharpe"
BAR = 0.70
NARROW_BAR = 0.35
IDENT_BAR = 0.75
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 118 + f"\n{s}\n" + "=" * 118)


# ===================================================================== book constructors
# VERBATIM from idea 833's committed script (which copied them from 831 / 641 / 574 / 804).
# Nothing here is new; only the arms below are new rungs of dials already swept in the record.
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


# ===================================================================== the 39-arm corpus
# (family, key, label, panel, weights fn, cadence, memo-key-if-any)
# Every family is a dial the record has already swept; the memo arm of each is marked.
CORPUS = [
    # -- TOPN: idea 641/574's composite top-n, W, g0.75, respread ------------------------
    ("TOPN", "TOPN-n10", "u56 top10 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 10, 0.75, 0), "W", None),
    ("TOPN", "TOPN-n20", "u56 top20 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 0), "W", "K1"),
    ("TOPN", "TOPN-n30", "u56 top30 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 30, 0.75, 0), "W", None),
    ("TOPN", "TOPN-n40", "u56 top40 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 40, 0.75, 0), "W", None),
    # -- BUF: the same with a rank buffer m ---------------------------------------------
    ("BUF", "BUF-m10", "u56 top20 + rank buffer m=10, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 10), "W", None),
    ("BUF", "BUF-m20", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W", "K2"),
    ("BUF", "BUF-m50", "u56 top20 + rank buffer m=50, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50), "W", None),
    # -- TOPND: daily cadence, fixed g/n ------------------------------------------------
    ("TOPND", "TOPND-m20", "u56 top20 DAILY + buffer m=20 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20, fixed=True), "D", None),
    ("TOPND", "TOPND-m50", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D", "K3"),
    # -- BANDW: RULES v2 band, weekly, g1.00 --------------------------------------------
    ("BANDW", "BANDW-b0.00", "u56 EW-all 200d-MA gate (band 0), W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "W", None),
    ("BANDW", "BANDW-b0.03", "u56 RULES v2 band 0.03, W, g1.00  [standing candidate]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W", "K5"),
    ("BANDW", "BANDW-b0.06", "u56 band 0.06, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.06, 1.00), "W", None),
    ("BANDW", "BANDW-b0.08", "u56 band 0.08, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W", "R1"),
    ("BANDW", "BANDW-b0.12", "u56 band 0.12, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.12, 1.00), "W", None),
    # -- BANDM: the same band, monthly --------------------------------------------------
    ("BANDM", "BANDM-b0.00", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "M", "K4"),
    ("BANDM", "BANDM-b0.03", "u56 band 0.03, M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "M", None),
    # -- BANDRS: band with EW respread at g0.75 -----------------------------------------
    ("BANDRS", "BANDRS-b0.03", "u56 band 0.03 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.03, 0.75), "W", None),
    ("BANDRS", "BANDRS-b0.12", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W", "K6"),
    # -- MARS: plain 200d-MA respread ---------------------------------------------------
    ("MARS", "MARS-g0.50", "u56 MA-RESPREAD, W, g0.50", "U56",
     lambda px: ma_respread(px, 0.50), "W", None),
    ("MARS", "MARS-g0.75", "u56 MA-RESPREAD, W, g0.75", "U56",
     lambda px: ma_respread(px, 0.75), "W", "R2"),
    ("MARS", "MARS-g1.00", "u56 MA-RESPREAD, W, g1.00", "U56",
     lambda px: ma_respread(px, 1.00), "W", None),
    # -- MADIST: distance-above-MA quantile, monthly ------------------------------------
    ("MADIST", "MADIST-q0.25", "u56 MA-DISTANCE top-quarter, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.25), "M", None),
    ("MADIST", "MADIST-q0.50", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M", "R3"),
    ("MADIST", "MADIST-q0.75", "u56 MA-DISTANCE top-three-quarters, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.75), "M", None),
    # -- BRD: breadth de-gross gate -----------------------------------------------------
    ("BRD", "BRD-q0.10", "u56 EW-all, de-gross to ZERO on breadth<q0.10(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.10), "W", None),
    ("BRD", "BRD-q0.17", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W", "K8"),
    ("BRD", "BRD-q0.25", "u56 EW-all, de-gross to ZERO on breadth<q0.25(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.25), "W", None),
    # -- EWALL: scored-eligible equal weight, no gate -----------------------------------
    ("EWALL", "EWALL-g0.75", "u56 scored-eligible EW-all, W, g0.75", "U56",
     lambda px: ewall_weights(px, 0.75), "W", None),
    ("EWALL", "EWALL-g1.00", "u56 scored-eligible EW-all, W, g1.00", "U56",
     lambda px: ewall_weights(px, 1.00), "W", None),
    # -- SHY: B136 EW with residual parked in SHY ---------------------------------------
    ("SHY", "SHY-g0.375", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W", "K7"),
    ("SHY", "SHY-g0.625", "b136 scored-eligible EW, residual in SHY, W, g0.625", "B136",
     lambda px: shy_residual_weights(px, 0.625), "W", None),
    # -- R6: B136 six-month momentum top-n, de-grossed ----------------------------------
    ("R6", "R6-n10", "b136 R6-top10 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 10, 0.65), "W", None),
    ("R6", "R6-n20", "b136 R6-top20 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 20, 0.65), "W", "R4"),
    ("R6", "R6-n30", "b136 R6-top30 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 30, 0.65), "W", None),
    # -- BANDWB: the band family on the broad panel -------------------------------------
    ("BANDWB", "BANDWB-b0.00", "b136 EW-all 200d-MA gate (band 0), W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "W", None),
    ("BANDWB", "BANDWB-b0.03", "b136 band 0.03, W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W", None),
    ("BANDWB", "BANDWB-b0.08", "b136 band 0.08, W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W", None),
    # -- MARSB: MA respread on the broad panel ------------------------------------------
    ("MARSB", "MARSB-g0.50", "b136 MA-RESPREAD, W, g0.50", "B136",
     lambda px: ma_respread(px, 0.50), "W", None),
    ("MARSB", "MARSB-g0.75", "b136 MA-RESPREAD, W, g0.75", "B136",
     lambda px: ma_respread(px, 0.75), "W", None),
]
COMPARANDS = [
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56", rules_v1_weights, "W"),
]
ARMS = [c[1] for c in CORPUS]
MEMOMAP = {c[6]: c[1] for c in CORPUS if c[6]}
MEMO833 = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "R1", "R2", "R3", "R4"]
MEMO12 = [MEMOMAP[k] for k in MEMO833]
U56ARMS = [c[1] for c in CORPUS if c[3] == "U56"]
FAMOF = {c[1]: c[0] for c in CORPUS}
FAMS = sorted(set(FAMOF.values()))


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
    """PROTOCOL literal fixed-window 4b: 5 legs (both halves, OOS Sharpe, DD cap, CAGR floor)."""
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


_NULL_CACHE: dict[int, float] = {}


def null_band(n):
    """Two-sided 95% band of |Spearman| under the IID null, by permutation. Deterministic per n."""
    if n not in _NULL_CACHE:
        rng = np.random.default_rng(SEED + n)
        x = np.arange(1, n + 1, dtype=float)
        xc = x - x.mean()
        den = (xc * xc).sum()
        Y = np.argsort(rng.random((NPERM, n)), axis=1).astype(float) + 1.0
        Yc = Y - Y.mean(axis=1, keepdims=True)
        _NULL_CACHE[n] = float(np.sort(np.abs((Yc @ xc) / den))[int(0.95 * NPERM)])
    return _NULL_CACHE[n]


def perm_p(a, b):
    """Two-sided IID permutation p for Spearman, 20,000 fixed-seed shuffles."""
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


def _rank(v):
    """Average-rank of a 1-d array (ties averaged), numpy-only."""
    o = np.argsort(v, kind="mergesort")
    r = np.empty(len(v), float)
    r[o] = np.arange(1, len(v) + 1, dtype=float)
    # average ties
    s = v[o]
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[o[i:j + 1]] = r[o[i:j + 1]].mean()
        i = j + 1
    return r


def _rho(x, y):
    rx, ry = _rank(x), _rank(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    d = np.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / d) if d > 0 else np.nan


def cluster_ci(x, y, fams):
    """Cluster bootstrap: resample the FAMILIES with replacement NBOOT times, recompute Spearman,
    return the 2.5 / 97.5 percentiles.  This is the honest interval when arms inside a family are
    near-duplicates: an interval covering 0 means the corpus does not resolve the sign."""
    x, y, fams = np.asarray(x, float), np.asarray(y, float), np.asarray(fams)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y, fams = x[ok], y[ok], fams[ok]
    uf = np.unique(fams)
    idx = {f: np.where(fams == f)[0] for f in uf}
    rng = np.random.default_rng(SEED + 7)
    out = np.full(NBOOT, np.nan)
    for b in range(NBOOT):
        pick = rng.integers(0, len(uf), len(uf))
        sel = np.concatenate([idx[uf[p]] for p in pick])
        xx, yy = x[sel], y[sel]
        if len(np.unique(xx)) < 2 or len(np.unique(yy)) < 2:
            continue
        out[b] = _rho(xx, yy)
    out = out[np.isfinite(out)]
    if len(out) < 100:
        return np.nan, np.nan, len(uf)
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), len(uf)


# ===================================================================== main
def main():
    T0 = time.time()
    P(f"# Idea 837 - {SLUG}  (lane C, {DATE})")
    P("# QUESTION: at n=12 idea 833 could not separate rho 0.5 from noise.  Widen the corpus to")
    P("#   30+ books built from the record's OWN committed constructors and re-run its six-target")
    P("#   census, so that a NULL means something.  Then ask what n=39 is actually worth.")
    P(f"# TUNED: corpus source {CORPORA} x statistic set {list(STATSETS)}; HEADLINE corpus "
      f"{CORP_HEAD}, set {SET_HEAD}.")
    P(f"# REPORTED AXES (not tuned): {len(WIDE10)} statistics x {len(TARGETS)} targets x 2 readings")
    P(f"# GRID: {len(CORPORA)} x {len(WIDE10)} x {len(TARGETS)} x 2 = "
      f"{len(CORPORA)*len(WIDE10)*len(TARGETS)*2} cells, EVERY one written to .grid.csv")
    P(f"# NULLS: iid permutation ({NPERM} shuffles) AND cluster bootstrap over the "
      f"{len(FAMS)} FAMILIES ({NBOOT} resamples).")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; levels optimistic, orderings less so.")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    spy_all = {k: v["SPY"].pct_change().fillna(0.0) for k, v in panels.items()}
    for k, v in panels.items():
        P(f"   panel {k:5s} {v.shape[1]-1} tradeable names, {len(v)} rows, "
          f"scored from {starts[k].date()}")
    P(f"   corpus: {len(ARMS)} arms in {len(FAMS)} families {FAMS}")
    P(f"   MEMO12 (idea 833's) maps into it as: "
      + ", ".join(f"{k}={MEMOMAP[k]}" for k in MEMO833))

    # ---- build every book once, plus its gross ladder and its zero-cost twin ----------
    hdr("BUILDING THE CORPUS (no new constructors; 10 bps, next-day fill, each family's cadence)")
    books, meta, gross_books, cost_books, turn_yr, maxgross = {}, {}, {}, {}, {}, {}
    allspecs = [(c[0], c[1], c[2], c[3], c[4], c[5]) for c in CORPUS] + \
               [("-", c[0], c[1], c[2], c[3], c[4]) for c in COMPARANDS]
    for fam, key, label, pan, wf, freq in allspecs:
        px = panels[pan]
        t0 = time.time()
        W = wf(px)
        bt = backtest(px, W, cost_bps=COST, freq=freq)
        bt0 = backtest(px, W, cost_bps=0, freq=freq)
        books[key] = bt["returns"]
        meta[key] = dict(label=label, panel=pan, freq=freq, family=fam)
        maxgross[key] = float(W.sum(axis=1).max())
        cost_books[key] = {c: bt0["returns"] - bt0["turnover"] * c / 1e4 for c in COST_RUNGS}
        turn_yr[key] = float(bt["turnover"].sum() / (len(bt["turnover"]) / 252))
        gl = {}
        if key in ARMS:
            for f in GROSS_RUNGS:
                gl[f] = backtest(px, W * f, cost_bps=COST, freq=freq)["returns"]
        gross_books[key] = gl
        P(f"   built {key:14s} fam {fam:7s} {pan:5s} {freq}  max gross {maxgross[key]:.3f}  "
          f"turn {turn_yr[key]:5.2f}x/yr  ({time.time()-t0:.1f}s)")

    # ---- GATES -----------------------------------------------------------------------
    hdr("GATES G2-G4 (G1, the reproduction gate, is printed after the book table)")
    d2 = max(float(np.abs(cost_books[k][COST] - books[k]).max()) for k in books)
    P(f"   G2  free cost ladder at 10 bps == the 10-bps backtest, max|d| over all books "
      f"{d2:.3e}  {'PASS' if d2 <= 1e-12 else 'FAIL'}")
    d3 = max(float(np.abs(gross_books[k][1.0] - books[k]).max()) for k in ARMS)
    P(f"   G3  gross ladder at f=1.000 (re-run, not aliased) == the base book, max|d| {d3:.3e}  "
      f"{'PASS' if d3 <= 1e-15 else 'FAIL'}")
    d4 = max(maxgross.values())
    P(f"   G4  max realised gross over every book and every rung {d4:.4f} (rungs scale DOWN only, "
      f"residual to CASH)  {'PASS' if d4 <= 1.0 + 1e-9 else 'FAIL'}")
    G234 = (d2 <= 1e-12) and (d3 <= 1e-15) and (d4 <= 1.0 + 1e-9)

    # ---- per-book table: full, IS, OOS, the ten predictors, both KEEP paths -----------
    hdr("PROTOCOL RULE 8 ON THE BOOKS - full window, IS (..2016-12-31), OOS (2017-01-01..)")
    rows = []
    for key in list(books):
        pan = meta[key]["panel"]
        r_all = books[key]
        f = r_all.loc[starts[pan]:]
        i_ = r_all.loc[starts[pan]:IS_END]
        o = r_all.loc[OOS_START:]
        mf, mi, mo = metrics(f), metrics(i_), metrics(o)
        fh1, fh2 = halves(f)
        ih1, ih2 = halves(i_)
        rows.append(dict(
            book=key, family=meta[key]["family"], panel=pan, freq=meta[key]["freq"],
            label=meta[key]["label"],
            full_CAGR=mf["CAGR"], full_Sharpe=mf["Sharpe"], full_MaxDD=mf["MaxDD"],
            full_Vol=mf["Vol"], full_Sortino=mf["Sortino"], full_WinRate=mf["WinRate"],
            full_H1=fh1, full_H2=fh2, turn_yr=turn_yr[key],
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            IS_Vol=mi["Vol"], IS_Sortino=mi["Sortino"], IS_WinRate=mi["WinRate"],
            IS_H1=ih1, IS_H2=ih2,
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    for pan in panels:
        s = spy_all[pan].loc[starts[pan]:]
        ms = metrics(s)
        sh1, sh2 = halves(s)
        mi = metrics(spy_all[pan].loc[starts[pan]:IS_END])
        mo = metrics(spy_all[pan].loc[OOS_START:])
        rows.append(dict(book=f"SPY_{pan}", family="-", panel=pan, freq="-",
                         label="SPY buy-and-hold",
                         full_CAGR=ms["CAGR"], full_Sharpe=ms["Sharpe"], full_MaxDD=ms["MaxDD"],
                         full_Vol=ms["Vol"], full_Sortino=ms["Sortino"],
                         full_WinRate=ms["WinRate"], full_H1=sh1, full_H2=sh2, turn_yr=0.0,
                         IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                         IS_Vol=mi["Vol"], IS_Sortino=mi["Sortino"], IS_WinRate=mi["WinRate"],
                         IS_H1=np.nan, IS_H2=np.nan,
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    B = pd.DataFrame(rows).set_index("book")

    for key in ARMS:
        pan = meta[key]["panel"]
        r = books[key].loc[starts[pan]:]
        spy = spy_all[pan].loc[starts[pan]:]
        lf = legs_fixed(r, spy)
        lo = legs_window(books[key].loc[OOS_START:], spy_all[pan].loc[OOS_START:])
        lv, rr = B.loc["LIVE"], B.loc[key]
        l4a = dict(H1=rr.full_H1 > lv.full_H1, H2=rr.full_H2 > lv.full_H2,
                   DD=rr.full_MaxDD >= lv.full_MaxDD)
        B.loc[key, "keep4b"] = "PASS" if all(lf.values()) else "FAIL"
        B.loc[key, "fail4b"] = "+".join(k for k, v in lf.items() if not v) or "-none-"
        B.loc[key, "keep4a"] = "PASS" if all(l4a.values()) else "FAIL"
        B.loc[key, "fail4a"] = "+".join(k for k, v in l4a.items() if not v) or "-none-"
        B.loc[key, "keep4b_OOSlocal"] = "PASS" if all(lo.values()) else "FAIL"
        B.loc[key, "memo833"] = next((k for k, v in MEMOMAP.items() if v == key), "-")

    show = ["family", "panel", "freq", "full_CAGR", "full_Sharpe", "full_MaxDD", "IS_Sharpe",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b", "keep4b_OOSlocal",
            "fail4b", "memo833"]
    P(B.loc[ARMS + ["LIVE", "V1", "SPY_U56", "SPY_B136"], show]
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    n4b = int((B.loc[ARMS, "keep4b"] == "PASS").sum())
    n4a = int((B.loc[ARMS, "keep4a"] == "PASS").sum())
    n4bo = int((B.loc[ARMS, "keep4b_OOSlocal"] == "PASS").sum())
    nboth = int(((B.loc[ARMS, "keep4b"] == "PASS") & (B.loc[ARMS, "keep4a"] == "PASS")).sum())
    P(f"\n   fixed-window 4b PASS {n4b} of {len(ARMS)};  4a PASS {n4a} of {len(ARMS)};  "
      f"OOS-LOCAL 4b PASS {n4bo} of {len(ARMS)};  BOTH paths {nboth} of {len(ARMS)}.")
    newpass = [k for k in ARMS if B.loc[k, "keep4b"] == "PASS" and B.loc[k, "memo833"] == "-"]
    P(f"   4b passers that are NOT one of idea 833's twelve: {len(newpass)} -> {newpass}")
    P("   NOTE: these arms were enumerated to answer a CENSUS question, not searched for as")
    P("   candidates, so per the record's own standard (idea 814) none is promoted here; the")
    P("   list is filed as a follow-up, not as a KEEP.")
    B.loc[ARMS + ["LIVE", "V1", "SPY_U56", "SPY_B136"],
          ["family", "panel", "freq", "full_CAGR", "full_Sharpe", "full_MaxDD", "IS_CAGR",
           "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b",
           "keep4b_OOSlocal"]].to_csv(f"{OUT}.walkforward.csv")

    # ---- the entry-date census (share_3y) ---------------------------------------------
    hdr(f"TARGET share_3y - idea 831's entry-date census, H={H3Y}, spacing={SPACE}")
    crows = []
    for key in ARMS + ["LIVE", "V1"]:
        pan = meta[key]["panel"]
        idx = panels[pan].index
        i0 = idx.get_loc(starts[pan])
        r_all, s_all = books[key], spy_all[pan]
        n = p = n_oos = p_oos = 0
        for i in range(i0, len(idx) - H3Y + 1, SPACE):
            sl = slice(i, i + H3Y)
            L = legs_window(r_all.iloc[sl], s_all.iloc[sl])
            ok = all(L.values())
            n += 1
            p += int(ok)
            if idx[i] >= OOS_START:
                n_oos += 1
                p_oos += int(ok)
            crows.append(dict(book=key, entry=idx[i], end=idx[i + H3Y - 1], PASS=ok, **L))
        B.loc[key, "share_3y"] = p / n if n else np.nan
        B.loc[key, "n_3y"] = n
        B.loc[key, "share_3y_OOS"] = p_oos / n_oos if n_oos else np.nan
        B.loc[key, "n_3y_OOS"] = n_oos
    pd.DataFrame(crows).to_csv(f"{OUT}.census.csv", index=False)
    P(B.loc[ARMS, ["share_3y", "n_3y", "share_3y_OOS", "n_3y_OOS"]]
      .to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- cost and gross ladders --------------------------------------------------------
    hdr("TARGETS cost_surv and gross_band - every rung of both ladders, all 39 arms")
    lrows = []
    for key in ARMS:
        pan = meta[key]["panel"]
        spy_f = spy_all[pan].loc[starts[pan]:]
        spy_o = spy_all[pan].loc[OOS_START:]
        surv = surv_oos = -1
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
    P("   cost ladder (fixed-window 4b at each bps rung; '.' = fail):")
    P("   " + f"{'book':<14}" + "".join(f"{c:>5}" for c in COST_RUNGS) + "   cost_surv")
    for key in ARMS:
        s = LAD[(LAD.book == key) & (LAD.ladder == "cost")]
        P("   " + f"{key:<14}" + "".join(f"{'Y' if v else '.':>5}" for v in s.pass_fixed)
          + f"   {int(B.loc[key,'cost_surv']):>4}")
    P("   gross ladder (scaling f, residual to CASH):")
    P("   " + f"{'book':<14}" + "".join(f"{f:>7.3f}" for f in GROSS_RUNGS) + "   gross_band")
    for key in ARMS:
        s = LAD[(LAD.book == key) & (LAD.ladder == "gross")]
        P("   " + f"{key:<14}" + "".join(f"{'Y' if v else '.':>7}" for v in s.pass_fixed)
          + f"   {B.loc[key,'gross_band']:>6.3f}")

    # ---- GATE G1: reproduction of idea 833 --------------------------------------------
    hdr("GATE G1 / H_REPRO - the MEMO12 arms against idea 833's committed .books.csv")
    REFSTEM = (Path(__file__).resolve().parent /
               "2026-09-12_does-the-record-s-PUBLISHED-SHARPE-order-ANY-out-of-window-statistic"
               "_cloud")
    ref = pd.read_csv(f"{REFSTEM}.books.csv").set_index("book")
    REFG = pd.read_csv(f"{REFSTEM}.grid.csv")
    dev = {}
    for col in ["full_Sharpe", "full_CAGR", "full_MaxDD", "OOS_Sharpe", "OOS_CAGR", "share_3y"]:
        dev[col] = float(np.abs(B.loc[MEMO12, col].values - ref.loc[MEMO833, col].values).max())
        P(f"   {col:<12} max|d| over the twelve  {dev[col]:.3e}  "
          f"{'PASS' if dev[col] <= 1e-9 else 'FAIL'}")
    rho833 = spearman(B.loc[MEMO12, "full_Sharpe"], B.loc[MEMO12, "OOS_Sharpe"])
    rho833_pub = float(REFG[(REFG.statistic == "SHARPE") & (REFG.ordering_set == "MEMO12")
                            & (REFG.reading == "a")
                            & (REFG.target == "OOS_Sharpe")].spearman.iloc[0])
    P(f"   833's headline cell Spearman(SHARPE, MEMO12, (a), OOS_Sharpe) committed "
      f"{rho833_pub:+.6f}, rebuilt {rho833:+.6f}")
    repro = max(dev.values()) <= 1e-9 and abs(rho833 - rho833_pub) <= 1e-4
    P(f"   G1 / H_REPRO {'PASS' if repro else 'FAIL'}")

    # ---- predictor columns --------------------------------------------------------------
    B["_CALMAR_full"] = B.full_CAGR / B.full_MaxDD.abs()
    B["_CALMAR_IS"] = B.IS_CAGR / B.IS_MaxDD.abs()
    B["_NEGVOL_full"] = -B.full_Vol
    B["_NEGVOL_IS"] = -B.IS_Vol
    B["_NEGTURN"] = -B.turn_yr
    PRED = {
        "a": {"SHARPE": "full_Sharpe", "CAGR": "full_CAGR", "MAXDD": "full_MaxDD",
              "CALMAR": "_CALMAR_full", "H2": "full_H2", "SORTINO": "full_Sortino",
              "WINRATE": "full_WinRate", "H1": "full_H1", "NEGVOL": "_NEGVOL_full",
              "NEGTURN": "_NEGTURN"},
        "b": {"SHARPE": "IS_Sharpe", "CAGR": "IS_CAGR", "MAXDD": "IS_MaxDD",
              "CALMAR": "_CALMAR_IS", "H2": "IS_H2", "SORTINO": "IS_Sortino",
              "WINRATE": "IS_WinRate", "H1": "IS_H1", "NEGVOL": "_NEGVOL_IS",
              "NEGTURN": "_NEGTURN"}}
    TGT = {"a": {t: t for t in TARGETS},
           "b": {"OOS_Sharpe": "OOS_Sharpe", "OOS_CAGR": "OOS_CAGR", "OOS_MaxDD": "OOS_MaxDD",
                 "share_3y": "share_3y_OOS", "cost_surv": "cost_surv_OOS",
                 "gross_band": "gross_band_OOS"}}

    def vecs(corpus, st, rd, t):
        """(x, y, families) for one cell. FAMMEAN14 collapses each family to its mean RANK."""
        if corpus == "FAMMEAN14":
            x = B.loc[ARMS, PRED[rd][st]].astype(float)
            y = B.loc[ARMS, TGT[rd][t]].astype(float)
            fam = pd.Series([FAMOF[k] for k in ARMS], index=ARMS)
            rx, ry = x.rank(), y.rank()
            gx = rx.groupby(fam).mean().sort_index()
            gy = ry.groupby(fam).mean().sort_index()
            return gx.values, gy.values, gx.index.values
        mem = {"ARMS39": ARMS, "MEMO12": MEMO12, "U56ARMS": U56ARMS}[corpus]
        return (B.loc[mem, PRED[rd][st]].astype(float).values,
                B.loc[mem, TGT[rd][t]].astype(float).values,
                np.array([FAMOF[k] for k in mem]))

    # ---- the grid ------------------------------------------------------------------------
    hdr(f"THE GRID - {len(CORPORA)} corpora x {len(WIDE10)} statistics x {len(TARGETS)} targets "
        f"x 2 readings = {len(CORPORA)*len(WIDE10)*len(TARGETS)*2} cells, every one reported")
    grows = []
    for corpus in CORPORA:
        for st in WIDE10:
            inset = "CORE5" if st in CORE5 else "WIDE10"
            head_stat = (corpus == CORP_HEAD and st in STATSETS[SET_HEAD])
            P(f"\n   -- corpus {corpus}  statistic {st} ({inset})"
              + ("   <== HEADLINE corpus/set" if head_stat else ""))
            P(f"      {'reading':<9}{'target':<12}{'n':>4}{'Spearman':>10}{'Pearson':>10}"
              f"{'iid p':>8}{'iid95':>8}{'clusCI_lo':>11}{'clusCI_hi':>11}  verdict")
            for rd in ["a", "b"]:
                for t in TARGETS:
                    x, y, fam = vecs(corpus, st, rd, t)
                    rho, pea, pv = spearman(x, y), pearson(x, y), perm_p(x, y)
                    n_ = len(x)
                    nb_ = null_band(n_)
                    if corpus == CORP_HEAD:
                        lo, hi, nfam = cluster_ci(x, y, fam)
                    else:
                        lo = hi = np.nan
                        nfam = len(np.unique(fam))
                    ver = ("rho >= +0.70" if rho >= BAR
                           else ("SIGNIFICANT (iid)" if pv <= 0.05 else "inside the iid null"))
                    if corpus == CORP_HEAD and np.isfinite(lo):
                        ver += "; cluster CI " + ("EXCLUDES 0" if lo > 0 or hi < 0 else "covers 0")
                    grows.append(dict(corpus=corpus, statistic=st, stat_set=inset, n=n_,
                                      n_families=nfam, reading=rd, target=t, spearman=rho,
                                      pearson=pea, iid_p=pv, iid_null95=nb_,
                                      cluster_lo=lo, cluster_hi=hi,
                                      headline=(head_stat and t == TGT_HEAD)))
                    P(f"      {'(a) FULL' if rd=='a' else '(b) IS':<9}{t:<12}{n_:>4}"
                      f"{rho:>10.4f}{pea:>10.4f}{pv:>8.4f}{nb_:>8.4f}"
                      + (f"{lo:>11.4f}{hi:>11.4f}" if np.isfinite(lo) else f"{'-':>11}{'-':>11}")
                      + f"  {ver}")
    GD = pd.DataFrame(grows)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    GD[GD.corpus == CORP_HEAD][["statistic", "reading", "target", "spearman", "iid_p",
                                "iid_null95", "cluster_lo", "cluster_hi"]] \
        .to_csv(f"{OUT}.cluster.csv", index=False)
    B.to_csv(f"{OUT}.books.csv")

    def g(corpus=CORP_HEAD, st="SHARPE", rd="b", t=TGT_HEAD):
        q = GD[(GD.corpus == corpus) & (GD.statistic == st) & (GD.reading == rd)
               & (GD.target == t)]
        return q.iloc[0]

    # ---- what the widening actually bought ------------------------------------------------
    hdr("WHAT n = 39 ACTUALLY BUYS - the two nulls side by side")
    P(f"   iid 95% null band for |Spearman|:  n=12 {null_band(12):.4f}   n=29 {null_band(29):.4f}"
      f"   n=39 {null_band(39):.4f}   n=14 (family means) {null_band(14):.4f}")
    P(f"   The queue's premise is that going 12 -> 39 narrows the band from {null_band(12):.4f} to")
    P(f"   {null_band(39):.4f}.  It does, IF the 39 arms are 39 independent draws.  They are not:")
    P(f"   they are {len(FAMS)} families of {len(ARMS)/len(FAMS):.1f} near-duplicate arms each.  The")
    P("   cluster bootstrap below prices that; the FAMMEAN14 corpus is the same correction taken")
    P(f"   to its limit, and its own iid band is {null_band(14):.4f} - barely better than n=12.")
    P("")
    P(f"   {'statistic':<10}{'rho (b)':>9}{'iid p':>8}{'iid95':>8}{'clusCI':>20}"
      f"{'clus width':>12}   resolved?")
    for st in WIDE10:
        r = g(st=st)
        w = r.cluster_hi - r.cluster_lo
        res = "YES" if (r.cluster_lo > 0 or r.cluster_hi < 0) else "no - CI covers 0"
        P(f"   {st:<10}{r.spearman:>9.4f}{r.iid_p:>8.4f}{r.iid_null95:>8.4f}"
          f"   [{r.cluster_lo:+.4f}, {r.cluster_hi:+.4f}]{w:>12.4f}   {res}")

    # ---- pre-registered hypotheses ---------------------------------------------------------
    hdr("PRE-REGISTERED HYPOTHESES")
    H = {}
    H["H_REPRO"] = (repro, f"max|d| over 6 columns x 12 books {max(dev.values()):.3e}; "
                           f"833's headline rho rebuilt {rho833:+.4f} vs published +0.6084")
    H["H_N30"] = (len(ARMS) >= 30, f"headline corpus n = {len(ARMS)} ({len(FAMS)} families)")
    H["H_NARROW"] = (null_band(len(ARMS)) <= NARROW_BAR,
                     f"iid 95% band at n={len(ARMS)} is {null_band(len(ARMS)):.4f} vs bar "
                     f"{NARROW_BAR}; at n=12 it was {null_band(12):.4f}")
    rb = {st: g(st=st).spearman for st in WIDE10}
    ra_ = {st: g(st=st, rd="a").spearman for st in WIDE10}
    best_b = max(rb, key=rb.get)
    best_a = max(ra_, key=ra_.get)
    H["H_ANY"] = (rb[best_b] >= BAR,
                  f"best statistic under (b) is {best_b} at rho {rb[best_b]:+.4f} (bar +{BAR}); "
                  "all ten: " + ", ".join(f"{s} {v:+.4f}" for s, v in rb.items()))
    H["H_ANY_A"] = (ra_[best_a] >= BAR,
                    f"best under (a) is {best_a} at rho {ra_[best_a]:+.4f}; all ten: "
                    + ", ".join(f"{s} {v:+.4f}" for s, v in ra_.items()))
    rsh = g(st="SHARPE")
    H["H_SHARPE"] = (rsh.spearman >= BAR,
                     f"SHARPE -> OOS_Sharpe under (b) rho {rsh.spearman:+.4f}, Pearson "
                     f"{rsh.pearson:+.4f}, iid p {rsh.iid_p:.4f}, cluster CI "
                     f"[{rsh.cluster_lo:+.4f}, {rsh.cluster_hi:+.4f}]")
    pmin = min(g(st=s).iid_p for s in WIDE10)
    H["H_SIG"] = (pmin <= 0.05, "iid p by statistic under (b): "
                  + ", ".join(f"{s} {g(st=s).iid_p:.4f}" for s in WIDE10))
    excl = [s for s in WIDE10 if g(st=s).cluster_lo > 0 or g(st=s).cluster_hi < 0]
    H["H_CLUSTER"] = (len(excl) > 0,
                      f"{len(excl)} of {len(WIDE10)} cluster CIs exclude 0 under (b)"
                      + (f": {excl}" if excl else "; every interval covers zero"))
    H["H_SIGN"] = (all(v > 0 for v in rb.values()),
                   "signs under (b): " + ", ".join(f"{s}{'+' if v > 0 else '-'}"
                                                   for s, v in rb.items()))
    r833 = {t: float(REFG[(REFG.statistic == "SHARPE") & (REFG.ordering_set == "MEMO12")
                          & (REFG.reading == "b") & (REFG.target == t)].spearman.iloc[0])
            for t in TARGETS}
    agree = [t for t in TARGETS if np.sign(g(t=t).spearman) == np.sign(r833[t])]
    H["H_REPLIC"] = (len(agree) == len(TARGETS),
                     f"{len(agree)} of {len(TARGETS)} target signs agree with 833's committed "
                     "MEMO12 (b) reading; ARMS39: "
                     + ", ".join(f"{t} {g(t=t).spearman:+.4f}" for t in TARGETS)
                     + "; 833 MEMO12: " + ", ".join(f"{t} {v:+.4f}" for t, v in r833.items()))
    across = {c: g(corpus=c).spearman for c in CORPORA}
    H["H_SETFREE"] = (max(across.values()) - min(across.values()) <= 0.30,
                      "Spearman(SHARPE, OOS_Sharpe) under (b) by corpus: "
                      + ", ".join(f"{c} {v:+.4f}" for c, v in across.items())
                      + f"; spread {max(across.values())-min(across.values()):.4f}")
    H["H_STATBEST"] = (best_b == "SHARPE",
                       f"best statistic at ordering OOS_Sharpe under (b) is {best_b} "
                       f"({rb[best_b]:+.4f}); SHARPE reads {rb['SHARPE']:+.4f}")
    ident = float((np.abs(B.loc[ARMS, "full_MaxDD"] - B.loc[ARMS, "OOS_MaxDD"]) <= 1e-9).mean())
    H["H_IDENT"] = (ident >= IDENT_BAR,
                    f"{ident:.4f} of the {len(ARMS)} arms have full MaxDD == OOS MaxDD to 1e-9 "
                    f"(bar {IDENT_BAR}); 833 read 11 of 12 = 0.9167 on its corpus")
    cand = [(c, s) for c in CORPORA for s in WIDE10]
    pick = max(cand, key=lambda k: g(corpus=k[0], st=k[1], rd="a").spearman)
    r_a = g(corpus=pick[0], st=pick[1], rd="a").spearman
    r_b = g(corpus=pick[0], st=pick[1], rd="b").spearman
    H["H_R8CLAIM"] = (abs(r_a - r_b) <= 0.30,
                      f"pair chosen under (a) = ({pick[1]}, {pick[0]}) at rho {r_a:+.4f}; read "
                      f"ONCE under (b) IS->OOS rho {r_b:+.4f}, gap {abs(r_a-r_b):.4f} vs bar 0.30")
    for k, (ok, why) in H.items():
        P(f"   {k:<11} {'PASS' if ok else 'FAIL'}   {why}")

    # ---- the reader's actual use -----------------------------------------------------------
    hdr("THE READER'S ACTUAL USE - does the TOP HALF by IS Sharpe beat the BOTTOM HALF out of sample?")
    order = B.loc[ARMS, "IS_Sharpe"].sort_values(ascending=False).index.tolist()
    h = len(order) // 2
    top, bot = order[:h], order[-h:]
    P(f"   top {h} by IS (..2016) Sharpe:    {top}")
    P(f"   bottom {h}:                      {bot}")
    P(f"   {'target':<12}{'top mean':>11}{'bottom mean':>13}{'delta':>10}  verdict")
    nwin = 0
    for t in TARGETS:
        col = TGT["b"][t]
        a_, b_ = B.loc[top, col].mean(), B.loc[bot, col].mean()
        nwin += int(a_ > b_)
        P(f"   {t:<12}{a_:>11.4f}{b_:>13.4f}{a_-b_:>10.4f}  "
          f"{'top wins' if a_ > b_ else 'BOTTOM WINS'}")
    P(f"   top half wins on {nwin} of {len(TARGETS)} targets (a coin would win {len(TARGETS)//2}).")

    # ---- verdict -------------------------------------------------------------------------
    hdr("VERDICT")
    npass = sum(1 for ok, _ in H.values() if ok)
    P(f"   {npass} of {len(H)} pre-registered hypotheses PASS.  Gates G2-G4 "
      f"{'PASS' if G234 else 'FAIL'}, G1 {'PASS' if repro else 'FAIL'}.")
    P(f"   HEADLINE ({CORP_HEAD}, set {SET_HEAD}, n={len(ARMS)}, reading (b) IS->OOS, target "
      f"{TGT_HEAD}):")
    for st in CORE5:
        r = g(st=st)
        P(f"     {st:<8} Spearman {r.spearman:+.4f}  Pearson {r.pearson:+.4f}  iid p {r.iid_p:.4f}"
          f"  iid95 {r.iid_null95:.4f}  cluster CI [{r.cluster_lo:+.4f}, {r.cluster_hi:+.4f}]")
    P(f"   The other five (WIDE10): "
      + ", ".join(f"{s} {g(st=s).spearman:+.4f}" for s in WIDE10 if s not in CORE5))
    P(f"   Under the contaminated reading (a) the same five read: "
      + ", ".join(f"{s} {g(st=s, rd='a').spearman:+.4f}" for s in CORE5))
    P("   No KEEP claimed: this run prices the record's own ORDERINGS, not a book.  Both KEEP")
    P(f"   paths are reported for all {len(ARMS)} arms as PROTOCOL requires; none is promoted.")
    P(f"\n   runtime {time.time()-T0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return H, B, GD


if __name__ == "__main__":
    main()
