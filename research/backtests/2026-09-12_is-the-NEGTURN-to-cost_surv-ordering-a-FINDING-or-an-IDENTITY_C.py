#!/usr/bin/env python3
"""Idea 839 - is the NEGTURN -> cost_surv ordering a FINDING or an IDENTITY?  (lane C, 2026-09-12)

QUESTION (QUEUE idea 839, verbatim)
    idea 837's only iid-significant OOS-Sharpe predictor was NEGTURN (+0.4587, p 0.0040, cluster
    CI [-0.0109, +0.7735]) and its one cluster-surviving cost cell was NEGTURN->cost_surv +0.4637,
    but cost survival is turnover times the rung by construction.  Decompose how much of that
    association is arithmetic and report whether any residual ordering of OOS Sharpe survives once
    the mechanical part is removed.  Max 2 params (decomposition, rung set).

THE ARITHMETIC BEING TESTED
    The engine charges  cost_t = turnover_t * c / 1e4,  so a book's TOTAL annual cost at rung c is
    turn_yr * c / 1e4 in return units.  Write D for a book's DRAG BUDGET: the largest flat annual
    return drag (bps/yr) it can absorb and still pass 4b.  Then, to the extent the lumpiness of
    turnover does not matter,

            c_star  =  D_star / turn_yr                                          (the IDENTITY)

    and since 1/turn is a strictly DECREASING function of turn, -turn and 1/turn have IDENTICAL
    ranks.  So if D_star were the SAME for every book, Spearman(NEGTURN, cost_surv) would be
    EXACTLY +1.0000 with no information of any kind in the corpus.  The question is therefore not
    "is +0.4637 big" but "is +0.4637 what is LEFT of +1.0000 after D_star disperses, or is there a
    turnover-free ordering underneath it".  Both readings are computed here:

        MECHANICAL part   rho(NEGTURN, c_hat)  with c_hat = D_star / turn_yr - the identity's own
                          prediction of the target, built from a TURNOVER-FREE headroom.
        RESIDUAL part     rho(NEGTURN, D_star) - does low turnover buy a bigger ABSOLUTE headroom?
                          This is the only part of the association that is not arithmetic.

    The same split is applied to the OOS-Sharpe leg by switching the cost channel OFF: the engine's
    only turnover -> Sharpe channel is the 10 bps charge, so rho(NEGTURN, OOS_Sharpe) read at
    cost = 0 bps is the ordering that survives removal of the mechanical part.

NO NEW CONSTRUCTORS.  The 39-arm corpus, the two comparands, the panels, the cadences and the 4b
    leg definitions are copied VERBATIM from idea 837's committed script (which copied them from
    833 / 831 / 641 / 574 / 804).  Gate G1 reproduces 837's committed .books.csv book by book and
    its two committed headline cells to 1e-4 before any new number is interpreted.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) DECOMPOSITION - what is removed before NEGTURN is read.  5 rungs:
        RAW       nothing removed; the target is cost_surv itself          <== 837's reading
        MECHPRED  target replaced by c_hat = D_star / turn_yr (pure arithmetic, turnover-free
                  headroom divided by turnover) - the CEILING the identity can explain
        DRAGFREE  target replaced by D_star itself (turnover divided OUT)  <== HEADLINE: the
                  residual.  A null here means the ordering is an identity.
        DIVTURN   target replaced by cost_surv * turn_yr (the observed rung re-expressed as a
                  drag budget) - the same removal applied to the OBSERVED target, not the model
        PARTIAL   Spearman partial correlation of NEGTURN with cost_surv CONTROLLING for D_star
    (2) RUNG SET - which cost rungs cost_surv is read on.  4 rungs:
        R11     0,5,10,15,20,25,30,40,50,75,100 bps - idea 837's exact ladder   <== HEADLINE
        FINE    0..100 bps in steps of 2 (51 rungs) - granularity control
        COARSE  0,25,50,100 - the opposite granularity control
        CONT    continuous c_star by bisection to 0.01 bps - no rung grid at all
    5 x 4 = 20 cost cells, and the OOS-Sharpe leg is read at every rung of every ladder.
    EVERY grid point is printed and written to .grid.csv.  The tuned pair only names the HEADLINE.

REPORTED AXES (not tuned, all printed)
    POPULATION  ALL39 (837's convention: a book failing 4b at every rung scores cost_surv = -1)
                and PASS0 (only the books that pass 4b at ZERO cost, where the identity applies
                at all).  13 of 39 arms fail 4b at every rung for reasons that are not about cost.
    WINDOW      FULL (fixed-window 4b, 837's) and IS(..2016) / OOS(2017..) window-local 4b.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    G1  GATE  the 39 arms reproduce idea 837's committed .books.csv turn_yr / full+IS+OOS
              CAGR,Sharpe,MaxDD / cost_surv to <= 1e-9, and its two committed cells
              rho(NEGTURN, cost_surv) = +0.4637 and rho(NEGTURN, OOS_Sharpe) = +0.4587 to <= 1e-3.
    G2  GATE  the analytic cost ladder r_c = r0 - turnover*c/1e4 equals the engine's own cost_bps=c
              backtest at c = 10 to <= 1e-12 for every book (the identity's premise).
    G3  GATE  the 4b pass indicator is MONOTONE non-increasing in c on the FINE ladder for every
              book, so c_star is well defined.  Violations counted and printed, not hidden.
    G4  GATE  max realised gross <= 1.0000 at every book - PROTOCOL rule 2's no-leverage clause.
    K0  SANITY  rho(NEGTURN, 1/turn_yr) = +1.0000 exactly - the arithmetic ceiling, by construction.
    H_MECH      the mechanical model reproduces the whole association:
                rho(NEGTURN, c_hat) >= rho(NEGTURN, cost_surv) at the headline rung set.
    H_SHARE     arithmetic share = rho(NEGTURN, c_hat) / rho(NEGTURN, cost_surv) >= 0.80.
    H_RECON     the identity reconstructs the target rank by rank: rho(c_star, c_hat) >= 0.90.
    H_RESID     RESIDUAL IS A NULL (the "it is an identity" hypothesis): rho(NEGTURN, D_star) has
                iid p > 0.05 AND a cluster-bootstrap 95% CI covering 0.
    H_RESID_SIG the OPPOSITE hypothesis, stated so it can win: rho(NEGTURN, D_star) >= +0.30 with
                a cluster CI excluding 0 - low turnover buys real headroom.
    H_OOSSH_0   a residual ordering of OOS Sharpe SURVIVES: rho(NEGTURN, OOS_Sharpe) read at
                cost = 0 bps has iid p <= 0.05 AND a cluster CI excluding 0.
    H_OOSSH_DROP  the cost channel carries the OOS-Sharpe cell: rho at 10 bps minus rho at 0 bps
                >= 0.20.
    H_POP       the association is not an artefact of the 13 structural non-passers: the sign and
                significance of rho(NEGTURN, cost_surv) agree on ALL39 and PASS0.
    H_SETFREE   max - min of rho(NEGTURN, cost_surv) across the 4 rung sets <= 0.15.
    H_R8CLAIM   RULE 8 ON THE CLAIM, read exactly ONCE: the (decomposition, rung set) cell with the
                highest rho on IS-window-local data (..2016 only, predictor AND target) reproduces
                within 0.30 when read on the OOS window alone.

PROTOCOL RULE 8 ON THE BOOKS (mandatory, run and reported): every arm's CAGR/Sharpe/MaxDD on the
    full window, on IS (..2016-12-31) and on OOS (2017-01-01..), against RULES v2 (the live book),
    RULES v1 and SPY on the same windows, with BOTH KEEP paths evaluated - 4a against the live
    book, 4b against SPY - on the fixed window AND on the OOS window alone.

SURVIVORSHIP: U56 and B136 are current-constituent lists, so every LEVEL printed here is
    optimistic.  This run reads ORDERINGS ACROSS books on one panel, which survivorship moves far
    less than a level, but no CAGR or Sharpe below is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt  full log        .books.csv   per-book metrics, turnover, all headroom measures
    .grid.csv     every cell      .ladders.csv cost / drag ladders, every rung, every book
    .cluster.csv  cluster CIs     .walkforward.csv  PROTOCOL rule 8 on the books
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
SLUG = "is-the-NEGTURN-to-cost_surv-ordering-a-FINDING-or-an-IDENTITY"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
PRIOR = (Path(__file__).resolve().parent /
         ("2026-09-12_does-ANY-cheap-to-compute-BOOK-STATISTIC-order-OOS-SHARPE-out-of-window-"
          "at-n-GE-30_C.books.csv"))

COST = 10
MAX_VOL, WARMUP = 0.60, 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
NPERM, NBOOT, SEED = 20000, 10000, 839

R11 = [0, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100]          # idea 837's exact ladder
FINE = list(range(0, 101, 2))
COARSE = [0, 25, 50, 100]
RUNGSETS = {"R11": R11, "FINE": FINE, "COARSE": COARSE, "CONT": None}
RUNG_HEAD = "R11"
DECOMPS = ["RAW", "MECHPRED", "DRAGFREE", "DIVTURN", "PARTIAL"]
DEC_HEAD = "DRAGFREE"
POPS = ["ALL39", "PASS0"]
POP_HEAD = "ALL39"
# REPORTED AXIS (not tuned): which 4b reading defines "survival".  Gate G1 established that idea
# 837's committed +0.4637 cell is its cost_surv_OOS column - the OOS-WINDOW-LOCAL 4b (legs_window
# on 2017..), NOT the fixed-window one, whose value on the same committed file is +0.5018.  Both
# are carried at every cell so the queue's number is reproduced and the other is not hidden.
WINDOWS = ["OOSLOC", "FIXED"]
WIN_HEAD = "OOSLOC"
WINLEG = {"OOSLOC": "OOS", "FIXED": "FULL"}
CS_OOS_837, SH_OOS_837, CS_FIX_837 = 0.4637, 0.4587, 0.5018

CMAX = 400.0                 # bisection bracket for c_star, bps
DMAX = 4000.0                # bisection bracket for D_star, bps/yr
BIS = 26
SHARE_BAR, RECON_BAR, RESID_BAR, DROP_BAR, SETFREE_BAR, R8_BAR = 0.80, 0.90, 0.30, 0.20, 0.15, 0.30
LOG: list[str] = []
pd.set_option("display.width", 260)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def hdr(s):
    P("\n" + "=" * 118 + f"\n{s}\n" + "=" * 118)


# ===================================================================== book constructors
# VERBATIM from idea 837's committed script.  Nothing here is new.
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


# ===================================================================== the 39-arm corpus (837's)
CORPUS = [
    ("TOPN", "TOPN-n10", "u56 top10 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 10, 0.75, 0), "W"),
    ("TOPN", "TOPN-n20", "u56 top20 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 0), "W"),
    ("TOPN", "TOPN-n30", "u56 top30 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 30, 0.75, 0), "W"),
    ("TOPN", "TOPN-n40", "u56 top40 composite, W, g0.75", "U56",
     lambda px: topn_weights(px, 40, 0.75, 0), "W"),
    ("BUF", "BUF-m10", "u56 top20 + rank buffer m=10, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 10), "W"),
    ("BUF", "BUF-m20", "u56 top20 + rank buffer m=20, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20), "W"),
    ("BUF", "BUF-m50", "u56 top20 + rank buffer m=50, W, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50), "W"),
    ("TOPND", "TOPND-m20", "u56 top20 DAILY + buffer m=20 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 20, fixed=True), "D"),
    ("TOPND", "TOPND-m50", "u56 top20 DAILY + buffer m=50 (fixed g/n), D, g0.75", "U56",
     lambda px: topn_weights(px, 20, 0.75, 50, fixed=True), "D"),
    ("BANDW", "BANDW-b0.00", "u56 EW-all 200d-MA gate (band 0), W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "W"),
    ("BANDW", "BANDW-b0.03", "u56 RULES v2 band 0.03, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W"),
    ("BANDW", "BANDW-b0.06", "u56 band 0.06, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.06, 1.00), "W"),
    ("BANDW", "BANDW-b0.08", "u56 band 0.08, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W"),
    ("BANDW", "BANDW-b0.12", "u56 band 0.12, W, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.12, 1.00), "W"),
    ("BANDM", "BANDM-b0.00", "u56 EW-all 200d-MA gate (band 0), M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "M"),
    ("BANDM", "BANDM-b0.03", "u56 band 0.03, M, g1.00", "U56",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "M"),
    ("BANDRS", "BANDRS-b0.03", "u56 band 0.03 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.03, 0.75), "W"),
    ("BANDRS", "BANDRS-b0.12", "u56 wide band b=0.12 EW respread, W, g0.75", "U56",
     lambda px: band_ew_respread(px, 0.12, 0.75), "W"),
    ("MARS", "MARS-g0.50", "u56 MA-RESPREAD, W, g0.50", "U56",
     lambda px: ma_respread(px, 0.50), "W"),
    ("MARS", "MARS-g0.75", "u56 MA-RESPREAD, W, g0.75", "U56",
     lambda px: ma_respread(px, 0.75), "W"),
    ("MARS", "MARS-g1.00", "u56 MA-RESPREAD, W, g1.00", "U56",
     lambda px: ma_respread(px, 1.00), "W"),
    ("MADIST", "MADIST-q0.25", "u56 MA-DISTANCE top-quarter, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.25), "M"),
    ("MADIST", "MADIST-q0.50", "u56 MA-DISTANCE top-half, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.50), "M"),
    ("MADIST", "MADIST-q0.75", "u56 MA-DISTANCE top-three-quarters, M, g0.75", "U56",
     lambda px: ma_dist_tophalf(px, 0.75, 0.75), "M"),
    ("BRD", "BRD-q0.10", "u56 EW-all, de-gross to ZERO on breadth<q0.10(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.10), "W"),
    ("BRD", "BRD-q0.17", "u56 EW-all, de-gross to ZERO on breadth<q0.17(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.17), "W"),
    ("BRD", "BRD-q0.25", "u56 EW-all, de-gross to ZERO on breadth<q0.25(1008d), W, g1.00", "U56",
     lambda px: breadth_gate_weights(px, 1.00, 0.25), "W"),
    ("EWALL", "EWALL-g0.75", "u56 scored-eligible EW-all, W, g0.75", "U56",
     lambda px: ewall_weights(px, 0.75), "W"),
    ("EWALL", "EWALL-g1.00", "u56 scored-eligible EW-all, W, g1.00", "U56",
     lambda px: ewall_weights(px, 1.00), "W"),
    ("SHY", "SHY-g0.375", "b136 scored-eligible EW, residual in SHY, W, g0.375", "B136",
     lambda px: shy_residual_weights(px, 0.375), "W"),
    ("SHY", "SHY-g0.625", "b136 scored-eligible EW, residual in SHY, W, g0.625", "B136",
     lambda px: shy_residual_weights(px, 0.625), "W"),
    ("R6", "R6-n10", "b136 R6-top10 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 10, 0.65), "W"),
    ("R6", "R6-n20", "b136 R6-top20 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 20, 0.65), "W"),
    ("R6", "R6-n30", "b136 R6-top30 (de-gross), W, g0.65", "B136",
     lambda px: r6_topn(px, 30, 0.65), "W"),
    ("BANDWB", "BANDWB-b0.00", "b136 EW-all 200d-MA gate (band 0), W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.00, 1.00), "W"),
    ("BANDWB", "BANDWB-b0.03", "b136 band 0.03, W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.03, 1.00), "W"),
    ("BANDWB", "BANDWB-b0.08", "b136 band 0.08, W, g1.00", "B136",
     lambda px: rules_v2_weights(px, 0.08, 1.00), "W"),
    ("MARSB", "MARSB-g0.50", "b136 MA-RESPREAD, W, g0.50", "B136",
     lambda px: ma_respread(px, 0.50), "W"),
    ("MARSB", "MARSB-g0.75", "b136 MA-RESPREAD, W, g0.75", "B136",
     lambda px: ma_respread(px, 0.75), "W"),
]
COMPARANDS = [
    ("LIVE", "RULES v2 LIVE band 0.03, W, g0.75  [comparand, NOT a 4b pass]", "U56",
     lambda px: rules_v2_weights(px, 0.03, 0.75), "W"),
    ("V1", "RULES v1 retired, W  [comparand, NOT a 4b pass]", "U56", rules_v1_weights, "W"),
]
ARMS = [c[1] for c in CORPUS]
FAMOF = {c[1]: c[0] for c in CORPUS}
FAMS = sorted(set(FAMOF.values()))


# ===================================================================== metric / stat helpers
def m3(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


_SPY_CACHE: dict[int, tuple] = {}


def _spy_ref(spy):
    """SPY's own (CAGR, Sharpe, MaxDD, h1, h2, OOS Sharpe) on a window - cached by identity."""
    k = id(spy)
    if k not in _SPY_CACHE:
        sc, ss, sd = m3(spy)
        sh1, sh2 = halves(spy)
        o_ss = metrics(spy.loc[OOS_START:])["Sharpe"] if len(spy.loc[OOS_START:]) else np.nan
        _SPY_CACHE[k] = (sc, ss, sd, sh1, sh2, o_ss)
    return _SPY_CACHE[k]


def legs_window(r, spy):
    """idea 831's window-local 4b: 4 legs, all read against SPY on the SAME window."""
    c, s, d = m3(r)
    h1, h2 = halves(r)
    sc, ss, sd, sh1, sh2, _ = _spy_ref(spy)
    return dict(SH=s > ss, HV=(h1 > sh1) and (h2 > sh2), DD=d >= 0.6 * sd, CG=c >= 0.7 * sc)


def legs_fixed(r, spy):
    """PROTOCOL literal fixed-window 4b: 5 legs (both halves, OOS Sharpe, DD cap, CAGR floor)."""
    c, s, d = m3(r)
    h1, h2 = halves(r)
    sc, ss, sd, sh1, sh2, o_ss = _spy_ref(spy)
    o_s = metrics(r.loc[OOS_START:])["Sharpe"]
    return dict(H1=h1 > sh1, H2=h2 > sh2, OOS=o_s > o_ss, DD=d >= 0.6 * sd, CG=c >= 0.7 * sc)


def _rank(v):
    o = np.argsort(v, kind="mergesort")
    r = np.empty(len(v), float)
    r[o] = np.arange(1, len(v) + 1, dtype=float)
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


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3 or len(np.unique(a)) < 2 or len(np.unique(b)) < 2:
        return np.nan
    return _rho(a, b)


def partial_spearman(a, b, z):
    """Spearman partial correlation of a and b controlling for z (rank residuals)."""
    a, b, z = np.asarray(a, float), np.asarray(b, float), np.asarray(z, float)
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(z)
    a, b, z = a[ok], b[ok], z[ok]
    if len(a) < 4:
        return np.nan
    rab, rbb, rzz = _rank(a), _rank(b), _rank(z)
    def res(u):
        uc, zc = u - u.mean(), rzz - rzz.mean()
        den = (zc * zc).sum()
        beta = (uc * zc).sum() / den if den > 0 else 0.0
        return uc - beta * zc
    ra, rb = res(rab), res(rbb)
    d = np.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / d) if d > 0 else np.nan


def perm_p(a, b):
    """Two-sided IID permutation p for Spearman, NPERM fixed-seed shuffles."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    n = len(a)
    if n < 3 or len(np.unique(a)) < 2 or len(np.unique(b)) < 2:
        return np.nan
    ra, rb = _rank(a), _rank(b)
    obs = abs(_rho(a, b))
    rac = ra - ra.mean()
    den = (rac * rac).sum()
    rng = np.random.default_rng(SEED + n)
    perm = np.argsort(rng.random((NPERM, n)), axis=1)
    Y = rb[perm]
    Yc = Y - Y.mean(axis=1, keepdims=True)
    rho = (Yc @ rac) / np.sqrt(den * (Yc * Yc).sum(axis=1))
    return float((np.abs(rho) >= obs - 1e-12).mean())


def null_band(n):
    rng = np.random.default_rng(SEED + 1000 + n)
    x = np.arange(1, n + 1, dtype=float)
    xc = x - x.mean()
    den = (xc * xc).sum()
    Y = np.argsort(rng.random((NPERM, n)), axis=1).astype(float) + 1.0
    Yc = Y - Y.mean(axis=1, keepdims=True)
    return float(np.sort(np.abs((Yc @ xc) / den))[int(0.95 * NPERM)])


def cluster_ci(x, y, fams, z=None):
    """Cluster bootstrap over FAMILIES.  If z is given the statistic is the partial Spearman."""
    x, y, fams = np.asarray(x, float), np.asarray(y, float), np.asarray(fams)
    zz = np.asarray(z, float) if z is not None else None
    ok = np.isfinite(x) & np.isfinite(y) & (np.isfinite(zz) if zz is not None else True)
    x, y, fams = x[ok], y[ok], fams[ok]
    if zz is not None:
        zz = zz[ok]
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
        out[b] = partial_spearman(xx, yy, zz[sel]) if zz is not None else _rho(xx, yy)
    out = out[np.isfinite(out)]
    if len(out) < 100:
        return np.nan, np.nan, len(uf)
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), len(uf)


# ===================================================================== main
def main():
    T0 = time.time()
    P(f"# Idea 839 - {SLUG}  (lane C, {DATE})")
    P("# QUESTION: cost survival is turnover x rung BY CONSTRUCTION.  Decompose 837's")
    P("#   NEGTURN->cost_surv +0.4637 into its arithmetic part and its residual, and ask whether")
    P("#   any ordering of OOS Sharpe survives when the cost channel is switched off.")
    P(f"# TUNED: decomposition {DECOMPS} x rung set {list(RUNGSETS)}; HEADLINE {DEC_HEAD} / "
      f"{RUNG_HEAD} / {POP_HEAD}.")
    P(f"# GRID: {len(DECOMPS)} x {len(RUNGSETS)} x {len(POPS)} cells for the cost leg, plus the")
    P("#   OOS-Sharpe leg at every rung of every ladder.  ALL written to .grid.csv.")
    P(f"# NULLS: iid permutation ({NPERM} shuffles) AND cluster bootstrap over the "
      f"{len(FAMS)} FAMILIES ({NBOOT} resamples).")
    P("# SURVIVORSHIP: U56/B136 are current-constituent lists; levels optimistic, orderings less.")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    starts = {k: v.index[WARMUP] for k, v in panels.items()}
    spy_all = {k: v["SPY"].pct_change().fillna(0.0) for k, v in panels.items()}
    # SPY comparand windows built ONCE so the leg-reference cache is stable
    SPYW = {}
    for k in panels:
        SPYW[(k, "FULL")] = spy_all[k].loc[starts[k]:]
        SPYW[(k, "IS")] = spy_all[k].loc[starts[k]:IS_END]
        SPYW[(k, "OOS")] = spy_all[k].loc[OOS_START:]
    for k, v in panels.items():
        P(f"   panel {k:5s} {v.shape[1]-1} tradeable names, {len(v)} rows, "
          f"scored from {starts[k].date()}")
    P(f"   corpus: {len(ARMS)} arms in {len(FAMS)} families {FAMS}")

    # ---- build every book ONCE at zero cost, keep its turnover series -------------------
    hdr("BUILDING THE CORPUS (no new constructors; next-day fill, each family's cadence)")
    r0, turn, meta, turn_yr, maxgross, r10_engine = {}, {}, {}, {}, {}, {}
    allspecs = [(c[0], c[1], c[2], c[3], c[4], c[5]) for c in CORPUS] + \
               [("-", c[0], c[1], c[2], c[3], c[4]) for c in COMPARANDS]
    for fam, key, label, pan, wf, freq in allspecs:
        px = panels[pan]
        t0 = time.time()
        W = wf(px)
        bt0 = backtest(px, W, cost_bps=0, freq=freq)
        bt10 = backtest(px, W, cost_bps=COST, freq=freq)
        r0[key] = bt0["returns"]
        turn[key] = bt0["turnover"]
        r10_engine[key] = bt10["returns"]
        meta[key] = dict(label=label, panel=pan, freq=freq, family=fam)
        maxgross[key] = float(W.sum(axis=1).max())
        turn_yr[key] = float(bt0["turnover"].sum() / (len(bt0["turnover"]) / 252))
        P(f"   built {key:14s} fam {fam:7s} {pan:5s} {freq}  max gross {maxgross[key]:.3f}  "
          f"turn {turn_yr[key]:5.2f}x/yr  ({time.time()-t0:.1f}s)")

    def r_cost(key, c):
        """The analytic cost ladder.  G2 proves this equals the engine at c = 10."""
        return r0[key] - turn[key] * c / 1e4

    def r_drag(key, D):
        """Flat annual return drag of D bps/yr - the TURNOVER-FREE headroom ladder."""
        return r0[key] - (D / 1e4) / 252.0

    # ---- GATES G2 / G4 -----------------------------------------------------------------
    hdr("GATES G2 and G4")
    d2 = max(float(np.abs(r_cost(k, COST) - r10_engine[k]).max()) for k in r0)
    P(f"   G2  analytic ladder r0 - turnover*c/1e4 at c=10 == engine cost_bps=10, max|d| over all "
      f"{len(r0)} books {d2:.3e}  {'PASS' if d2 <= 1e-12 else 'FAIL'}")
    d4 = max(maxgross.values())
    P(f"   G4  max realised gross over every book {d4:.4f} (no leverage)  "
      f"{'PASS' if d4 <= 1.0 + 1e-9 else 'FAIL'}")
    G2ok, G4ok = d2 <= 1e-12, d4 <= 1.0 + 1e-9

    # ---- per-book table: full, IS, OOS ---------------------------------------------------
    hdr("PROTOCOL RULE 8 ON THE BOOKS - full window, IS (..2016-12-31), OOS (2017-01-01..)")
    rows = []
    for key in list(r0):
        pan = meta[key]["panel"]
        r_all = r_cost(key, COST)
        f = r_all.loc[starts[pan]:]
        i_ = r_all.loc[starts[pan]:IS_END]
        o = r_all.loc[OOS_START:]
        mf, mi, mo = metrics(f), metrics(i_), metrics(o)
        rows.append(dict(
            book=key, family=meta[key]["family"], panel=pan, freq=meta[key]["freq"],
            label=meta[key]["label"], turn_yr=turn_yr[key],
            full_CAGR=mf["CAGR"], full_Sharpe=mf["Sharpe"], full_MaxDD=mf["MaxDD"],
            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    for pan in panels:
        s = spy_all[pan].loc[starts[pan]:]
        ms = metrics(s)
        mi = metrics(spy_all[pan].loc[starts[pan]:IS_END])
        mo = metrics(spy_all[pan].loc[OOS_START:])
        rows.append(dict(book=f"SPY_{pan}", family="-", panel=pan, freq="-",
                         label="SPY buy-and-hold", turn_yr=0.0,
                         full_CAGR=ms["CAGR"], full_Sharpe=ms["Sharpe"], full_MaxDD=ms["MaxDD"],
                         IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    B = pd.DataFrame(rows).set_index("book")

    for key in ARMS:
        pan = meta[key]["panel"]
        r = r_cost(key, COST)
        lf = legs_fixed(r.loc[starts[pan]:], SPYW[(pan, "FULL")])
        lo = legs_window(r.loc[OOS_START:], SPYW[(pan, "OOS")])
        lv, rr = B.loc["LIVE"], B.loc[key]
        fh1, fh2 = halves(r.loc[starts[pan]:])
        lh1, lh2 = halves(r_cost("LIVE", COST).loc[starts["U56"]:])
        l4a = dict(H1=fh1 > lh1, H2=fh2 > lh2, DD=rr.full_MaxDD >= lv.full_MaxDD)
        B.loc[key, "keep4b"] = "PASS" if all(lf.values()) else "FAIL"
        B.loc[key, "fail4b"] = "+".join(k for k, v in lf.items() if not v) or "-none-"
        B.loc[key, "keep4a"] = "PASS" if all(l4a.values()) else "FAIL"
        B.loc[key, "keep4b_OOSlocal"] = "PASS" if all(lo.values()) else "FAIL"

    show = ["family", "panel", "freq", "turn_yr", "full_CAGR", "full_Sharpe", "full_MaxDD",
            "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b",
            "keep4b_OOSlocal", "fail4b"]
    P(B.loc[ARMS + ["LIVE", "V1", "SPY_U56", "SPY_B136"], show]
      .to_string(float_format=lambda x: f"{x:+.4f}"))
    n4b = int((B.loc[ARMS, "keep4b"] == "PASS").sum())
    n4a = int((B.loc[ARMS, "keep4a"] == "PASS").sum())
    n4bo = int((B.loc[ARMS, "keep4b_OOSlocal"] == "PASS").sum())
    nboth = int(((B.loc[ARMS, "keep4b"] == "PASS") & (B.loc[ARMS, "keep4a"] == "PASS")).sum())
    P(f"\n   fixed-window 4b PASS {n4b} of {len(ARMS)};  4a PASS {n4a};  OOS-local 4b PASS {n4bo};"
      f"  BOTH {nboth}.")
    P("   NOTE: these arms are a CENSUS corpus, not searched-for candidates; none is promoted.")
    B.loc[ARMS + ["LIVE", "V1", "SPY_U56", "SPY_B136"],
          ["family", "panel", "freq", "turn_yr", "full_CAGR", "full_Sharpe", "full_MaxDD",
           "IS_CAGR", "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
           "keep4a", "keep4b", "keep4b_OOSlocal"]].to_csv(f"{OUT}.walkforward.csv")

    # ---- the ladders: cost (turnover-proportional) and drag (flat, turnover-free) --------
    hdr("LADDERS - cost rung c (bps on turnover) and flat drag D (bps/yr), fixed-window 4b")
    lrows = []

    _PC: dict = {}

    def _judge(key, r, win):
        pan = meta[key]["panel"]
        if win == "FULL":
            return all(legs_fixed(r.loc[starts[pan]:], SPYW[(pan, "FULL")]).values())
        if win == "IS":
            return all(legs_window(r.loc[starts[pan]:IS_END], SPYW[(pan, "IS")]).values())
        return all(legs_window(r.loc[OOS_START:], SPYW[(pan, "OOS")]).values())

    def pass_cost(key, c, win="FULL"):
        k = ("c", key, round(float(c), 6), win)
        if k not in _PC:
            _PC[k] = _judge(key, r_cost(key, c), win)
        return _PC[k]

    def pass_drag(key, D, win="FULL"):
        k = ("d", key, round(float(D), 6), win)
        if k not in _PC:
            _PC[k] = _judge(key, r_drag(key, D), win)
        return _PC[k]

    def bisect(fn, lo, hi):
        """Largest x in [lo,hi] still passing, assuming monotone.  -1 if lo already fails."""
        if not fn(lo):
            return -1.0
        if fn(hi):
            return hi
        a, b = lo, hi
        for _ in range(BIS):
            m = 0.5 * (a + b)
            if fn(m):
                a = m
            else:
                b = m
        return a

    ALLC = sorted(set(FINE + R11 + COARSE))
    costflag = {}
    for win in ("FULL", "OOS", "IS"):
        for key in ARMS:
            for c in ALLC:
                ok = pass_cost(key, c, win)
                costflag[(key, float(c), win)] = ok
                lrows.append(dict(book=key, ladder="cost", rung=float(c), window=win, passes=ok))

    # G3 monotonicity on the FINE ladder, both reported windows
    G3ok, g3msg = True, []
    for win in ("FULL", "OOS"):
        viol, violbooks = 0, []
        for key in ARMS:
            seq = [costflag[(key, float(c), win)] for c in FINE]
            v = sum(1 for i in range(1, len(seq)) if seq[i] and not seq[i - 1])
            viol += v
            if v:
                violbooks.append(f"{key}({v})")
        P(f"   G3  monotonicity of the 4b pass indicator in c, window {win:4s}, FINE ladder "
          f"({len(FINE)} rungs x {len(ARMS)} books): {viol} up-steps  "
          f"{'PASS' if viol == 0 else 'FAIL'}  {violbooks}")
        G3ok = G3ok and viol == 0
        g3msg.append(f"{win} {viol}")

    # drag ladder + continuous survivals
    DRUNGS = [0, 25, 50, 100, 150, 200, 300, 400, 600, 800, 1200, 1600, 2400]
    for win in ("FULL", "OOS", "IS"):
        for key in ARMS:
            for D in DRUNGS:
                lrows.append(dict(book=key, ladder="drag", rung=float(D), window=win,
                                  passes=pass_drag(key, D, win)))
    for key in ARMS:
        B.loc[key, "c_star"] = bisect(lambda c: pass_cost(key, c), 0.0, CMAX)
        B.loc[key, "D_star"] = bisect(lambda D: pass_drag(key, D), 0.0, DMAX)
        B.loc[key, "c_star_IS"] = bisect(lambda c: pass_cost(key, c, "IS"), 0.0, CMAX)
        B.loc[key, "D_star_IS"] = bisect(lambda D: pass_drag(key, D, "IS"), 0.0, DMAX)
        B.loc[key, "c_star_OOS"] = bisect(lambda c: pass_cost(key, c, "OOS"), 0.0, CMAX)
        B.loc[key, "D_star_OOS"] = bisect(lambda D: pass_drag(key, D, "OOS"), 0.0, DMAX)
    pd.DataFrame(lrows).to_csv(f"{OUT}.ladders.csv", index=False)

    # cost_surv per (window, rung set); D_star / c_hat per window
    SUF = {"FIXED": "", "OOSLOC": "_OOS"}
    for win in WINDOWS:
        leg, sfx = WINLEG[win], SUF[win]
        for name, rungs in RUNGSETS.items():
            for key in ARMS:
                if rungs is None:
                    B.loc[key, f"cs_{win}_{name}"] = B.loc[key, f"c_star{sfx}"]
                else:
                    s = -1.0
                    for c in rungs:
                        if costflag[(key, float(c), leg)]:
                            s = float(c)
                    B.loc[key, f"cs_{win}_{name}"] = s
        d = B.loc[ARMS, f"D_star{sfx}"]
        B.loc[ARMS, f"chat_{win}"] = (d / B.loc[ARMS, "turn_yr"]).where(d >= 0, -1.0)
    # 837's own column names, kept so the gate can be read against the committed file
    B.loc[ARMS, "cost_surv_R11"] = B.loc[ARMS, "cs_FIXED_R11"]
    B.loc[ARMS, "cost_surv_OOS_R11"] = B.loc[ARMS, "cs_OOSLOC_R11"]
    B.loc[ARMS, "c_hat_IS"] = (B.loc[ARMS, "D_star_IS"] / B.loc[ARMS, "turn_yr"]).where(
        B.loc[ARMS, "D_star_IS"] >= 0, -1.0)
    B.loc[ARMS, "NEGTURN"] = -B.loc[ARMS, "turn_yr"]
    B.loc[ARMS, "INVTURN"] = 1.0 / B.loc[ARMS, "turn_yr"]

    P("\n   FIXED = fixed-window 4b (5 legs).  OOSLOC = OOS-window-local 4b (4 legs) = the reading")
    P("   idea 837's committed +0.4637 cell is on.")
    P("   " + f"{'book':<14}{'turn/yr':>8}" + f"{'cFIX_R11':>9}{'cFIX*':>8}{'DFIX*':>8}"
      f"{'chatFIX':>8}" + f"{'cOOS_R11':>10}{'cOOS*':>8}{'DOOS*':>8}{'chatOOS':>8}")
    for key in ARMS:
        b = B.loc[key]
        P(f"   {key:<14}{b.turn_yr:8.2f}{b.cs_FIXED_R11:9.0f}{b.c_star:8.2f}{b.D_star:8.1f}"
          f"{b.chat_FIXED:8.2f}{b.cs_OOSLOC_R11:10.0f}{b.c_star_OOS:8.2f}{b.D_star_OOS:8.1f}"
          f"{b.chat_OOSLOC:8.2f}")

    # ---- G1 reproduction of idea 837 -----------------------------------------------------
    hdr("GATE G1 - reproduction of idea 837's committed .books.csv")
    G1ok = False
    if PRIOR.exists():
        prev = pd.read_csv(PRIOR).set_index("book")
        cols = {"turn_yr": "turn_yr", "full_CAGR": "full_CAGR", "full_Sharpe": "full_Sharpe",
                "full_MaxDD": "full_MaxDD", "IS_CAGR": "IS_CAGR", "IS_Sharpe": "IS_Sharpe",
                "IS_MaxDD": "IS_MaxDD", "OOS_CAGR": "OOS_CAGR", "OOS_Sharpe": "OOS_Sharpe",
                "OOS_MaxDD": "OOS_MaxDD", "cost_surv": "cost_surv_R11",
                "cost_surv_OOS": "cost_surv_OOS_R11"}
        dmax = 0.0
        for c, mycol in cols.items():
            d = float(np.abs(B.loc[ARMS, mycol].values - prev.loc[ARMS, c].values).max())
            dmax = max(dmax, d)
            P(f"   {c:<14} max|d| over 39 arms {d:.3e}")
        neg = B.loc[ARMS, "NEGTURN"]
        rho_cs = spearman(neg, B.loc[ARMS, "cost_surv_OOS_R11"])
        rho_fx = spearman(neg, B.loc[ARMS, "cost_surv_R11"])
        rho_sh = spearman(neg, B.loc[ARMS, "OOS_Sharpe"])
        P(f"   committed cell rho(NEGTURN, cost_surv_OOS) {CS_OOS_837:+.4f} -> rebuilt "
          f"{rho_cs:+.4f}  |d| {abs(rho_cs-CS_OOS_837):.4f}   <== the queue's +0.4637 cell")
        P(f"   the FIXED-window column on the SAME committed file reads {CS_FIX_837:+.4f} -> "
          f"rebuilt {rho_fx:+.4f}  |d| {abs(rho_fx-CS_FIX_837):.4f}")
        P(f"   committed cell rho(NEGTURN, OOS_Sharpe) {SH_OOS_837:+.4f} -> rebuilt {rho_sh:+.4f}"
          f"  |d| {abs(rho_sh-SH_OOS_837):.4f}")
        G1ok = (dmax <= 1e-9 and abs(rho_cs - CS_OOS_837) <= 1e-3
                and abs(rho_fx - CS_FIX_837) <= 1e-3 and abs(rho_sh - SH_OOS_837) <= 1e-3)
        P(f"   G1  {'PASS' if G1ok else 'FAIL'}  (max|d| {dmax:.3e})")
        P("   NOTE: the queue calls the cell 'NEGTURN->cost_surv'.  It is the OOS-WINDOW-LOCAL")
        P("   survival column; the fixed-window one is a different, higher number.  Both carried.")
    else:
        P("   G1  SKIP - idea 837's books.csv not found")
    P(f"\n   GATES: G1 {'PASS' if G1ok else 'FAIL'}  G2 {'PASS' if G2ok else 'FAIL'}  "
      f"G3 {'PASS' if G3ok else 'FAIL'}  G4 {'PASS' if G4ok else 'FAIL'}")

    # ---- K0: the arithmetic ceiling ------------------------------------------------------
    hdr("K0 - the arithmetic ceiling of the association")
    k0 = spearman(B.loc[ARMS, "NEGTURN"], B.loc[ARMS, "INVTURN"])
    P(f"   rho(NEGTURN, 1/turn_yr) = {k0:+.6f}   (-turn and 1/turn are the SAME ranking)")
    P("   => if D_star were CONSTANT across books, rho(NEGTURN, cost_surv) would be EXACTLY")
    P(f"      {k0:+.4f} with zero information in the corpus.  837's +0.4637 is what is LEFT of")
    P("      that ceiling once D_star disperses - not a signal added on top of it.")
    K0ok = abs(k0 - 1.0) <= 1e-9

    # ---- the grid ------------------------------------------------------------------------
    hdr("THE GRID - 2 windows x 5 decompositions x 4 rung sets x 2 populations (cost leg)")
    pass0 = {w: [k for k in ARMS if costflag[(k, 0.0, WINLEG[w])]] for w in WINDOWS}
    for w in WINDOWS:
        P(f"   window {w:7s} ALL39 n={len(ARMS)} (iid 95% band {null_band(len(ARMS)):.4f});  "
          f"PASS0 n={len(pass0[w])} (band {null_band(len(pass0[w])):.4f}) = arms passing 4b at "
          f"ZERO cost")
        P(f"      the {len(ARMS)-len(pass0[w])} arms outside PASS0 fail 4b at EVERY rung for "
          "reasons that are NOT about cost:")
        P("      " + ", ".join(k for k in ARMS if k not in pass0[w]))

    grows = []
    for win in WINDOWS:
        sfx = SUF[win]
        for pop in POPS:
            keys = ARMS if pop == "ALL39" else pass0[win]
            fams = [FAMOF[k] for k in keys]
            neg = B.loc[keys, "NEGTURN"].values
            dstar = B.loc[keys, f"D_star{sfx}"].values
            chat = B.loc[keys, f"chat_{win}"].values
            for rs in RUNGSETS:
                cs = B.loc[keys, f"cs_{win}_{rs}"].values
                for dec in DECOMPS:
                    if dec == "RAW":
                        tgt, ctrl, desc = cs, None, f"cost_surv({rs})"
                    elif dec == "MECHPRED":
                        tgt, ctrl, desc = chat, None, "D_star/turn_yr"
                    elif dec == "DRAGFREE":
                        tgt, ctrl, desc = dstar, None, "D_star (bps/yr)"
                    elif dec == "DIVTURN":
                        # a non-passer scores cost_surv = -1, and -1 x turn_yr IS NEGTURN, which
                        # would manufacture a perfect correlation out of a coding convention.
                        # Those arms are dropped here (n falls; it is reported).
                        tv = B.loc[keys, "turn_yr"].values
                        tgt = np.where(cs >= 0, cs * tv, np.nan)
                        ctrl, desc = None, f"cost_surv({rs}) x turn_yr"
                    else:
                        tgt, ctrl, desc = cs, dstar, f"cost_surv({rs}) | D_star"
                    rho = (partial_spearman(neg, tgt, ctrl) if ctrl is not None
                           else spearman(neg, tgt))
                    p = np.nan if ctrl is not None else perm_p(neg, tgt)
                    lo, hi, nf = cluster_ci(neg, tgt, fams, ctrl)
                    grows.append(dict(leg="cost", window=win, population=pop, rung_set=rs,
                                      decomposition=dec, target=desc,
                                      n=int(np.isfinite(tgt).sum()), n_fam=nf, spearman=rho,
                                      iid_p=p, cl_lo=lo, cl_hi=hi,
                                      cl_excl0=bool(np.isfinite(lo) and (lo > 0 or hi < 0))))
    G = pd.DataFrame(grows)
    P("\n   " + f"{'window':<8}{'pop':<7}{'rungs':<8}{'decomp':<10}{'target':<26}{'n':>4}"
      f"{'rho':>9}{'iid p':>9}{'cluster 95% CI':>24}{'excl0':>7}")
    for r in G.itertuples():
        ci = (f"[{r.cl_lo:+.4f}, {r.cl_hi:+.4f}]" if np.isfinite(r.cl_lo) else "n/a")
        pp = f"{r.iid_p:.4f}" if np.isfinite(r.iid_p) else "   -  "
        star = "  <== HEADLINE" if (r.window == WIN_HEAD and r.population == POP_HEAD
                                    and r.rung_set == RUNG_HEAD
                                    and r.decomposition == DEC_HEAD) else ""
        P(f"   {r.window:<8}{r.population:<7}{r.rung_set:<8}{r.decomposition:<10}{r.target:<26}"
          f"{r.n:>4}{r.spearman:>+9.4f}{pp:>9}{ci:>24}{'Y' if r.cl_excl0 else 'n':>7}{star}")

    # ---- the OOS-Sharpe leg: switch the cost channel off ---------------------------------
    hdr("THE OOS-SHARPE LEG - rho(NEGTURN, OOS_Sharpe) as the cost channel is switched off")
    CI_RUNGS = sorted(set(R11 + COARSE))          # full inference here
    ALL_RUNGS = sorted(set(FINE + R11 + COARSE))  # rho-only sweep everywhere
    srows = []
    shcache: dict = {}
    for pop in POPS:
        keys = ARMS if pop == "ALL39" else pass0[WIN_HEAD]
        fams = [FAMOF[k] for k in keys]
        neg = B.loc[keys, "NEGTURN"].values
        for c in ALL_RUNGS:
            sh, shf, cg = [], [], []
            for k in keys:
                if (k, c) not in shcache:
                    pan = meta[k]["panel"]
                    rr = r_cost(k, c)
                    mo = metrics(rr.loc[OOS_START:])
                    shcache[(k, c)] = (mo["Sharpe"], metrics(rr.loc[starts[pan]:])["Sharpe"],
                                       mo["CAGR"])
                a, b, d = shcache[(k, c)]
                sh.append(a)
                shf.append(b)
                cg.append(d)
            for tname, vec in (("OOS_Sharpe", sh), ("full_Sharpe", shf), ("OOS_CAGR", cg)):
                rho = spearman(neg, vec)
                if c in CI_RUNGS:
                    p = perm_p(neg, vec)
                    lo, hi, nf = cluster_ci(neg, vec, fams)
                else:
                    p, lo, hi, nf = np.nan, np.nan, np.nan, len(set(fams))
                srows.append(dict(leg="sharpe", population=pop, cost_bps=c, target=tname,
                                  n=len(keys), n_fam=nf, spearman=rho, iid_p=p, cl_lo=lo,
                                  cl_hi=hi,
                                  cl_excl0=bool(np.isfinite(lo) and (lo > 0 or hi < 0))))
    S = pd.DataFrame(srows)
    for pop in POPS:
        P(f"\n   population {pop}  (iid p and cluster CI computed at the R11+COARSE rungs; every")
        P("   other rung of the FINE ladder is a rho-only sweep, all of it in .grid.csv)")
        P("   " + f"{'cost':>5}{'OOS_Sharpe rho':>16}{'iid p':>9}{'cluster CI':>24}"
          f"{'full_Sharpe rho':>17}{'OOS_CAGR rho':>14}")
        for c in ALL_RUNGS:
            a = S[(S.population == pop) & (S.cost_bps == c) & (S.target == "OOS_Sharpe")].iloc[0]
            b = S[(S.population == pop) & (S.cost_bps == c) & (S.target == "full_Sharpe")].iloc[0]
            d = S[(S.population == pop) & (S.cost_bps == c) & (S.target == "OOS_CAGR")].iloc[0]
            ci = (f"[{a.cl_lo:+.4f}, {a.cl_hi:+.4f}]" if np.isfinite(a.cl_lo) else "-")
            pp = f"{a.iid_p:.4f}" if np.isfinite(a.iid_p) else "  -   "
            P(f"   {c:>5}{a.spearman:>+16.4f}{pp:>9}{ci:>24}{b.spearman:>+17.4f}"
              f"{d.spearman:>+14.4f}")

    pd.concat([G, S], ignore_index=True).to_csv(f"{OUT}.grid.csv", index=False)
    G.to_csv(f"{OUT}.cluster.csv", index=False)

    # ---- reconstruction ------------------------------------------------------------------
    hdr("RECONSTRUCTION - does D_star/turn_yr rebuild the observed cost survival rank by rank?")
    rec = {}
    for win in WINDOWS:
        sfx = SUF[win]
        for pop in POPS:
            keys = ARMS if pop == "ALL39" else pass0[win]
            ch = B.loc[keys, f"chat_{win}"]
            for rs in RUNGSETS:
                rec[(win, pop, rs)] = spearman(B.loc[keys, f"cs_{win}_{rs}"], ch)
            rec[(win, pop, "cstar")] = spearman(B.loc[keys, f"c_star{sfx}"], ch)
            P(f"   {win:<7} {pop:<7} rho(cost_surv, c_hat): " +
              "  ".join(f"{rs} {rec[(win, pop, rs)]:+.4f}" for rs in RUNGSETS) +
              f"   |  rho(c_star, c_hat) {rec[(win, pop, 'cstar')]:+.4f}")
    recon = rec[(WIN_HEAD, POP_HEAD, "cstar")]

    # ---- HYPOTHESES ----------------------------------------------------------------------
    hdr("PRE-REGISTERED HYPOTHESES")
    def cell(pop, rs, dec, win=WIN_HEAD):
        return G[(G.window == win) & (G.population == pop) & (G.rung_set == rs)
                 & (G.decomposition == dec)].iloc[0]

    raw = cell(POP_HEAD, RUNG_HEAD, "RAW")
    mech = cell(POP_HEAD, RUNG_HEAD, "MECHPRED")
    drag = cell(POP_HEAD, RUNG_HEAD, "DRAGFREE")
    part = cell(POP_HEAD, RUNG_HEAD, "PARTIAL")
    share = mech.spearman / raw.spearman if raw.spearman else np.nan
    _rawset = G[(G.window == WIN_HEAD) & (G.population == POP_HEAD)
                & (G.decomposition == "RAW")].spearman
    setspread = _rawset.max() - _rawset.min()
    raw0 = cell("PASS0", RUNG_HEAD, "RAW")
    s10 = S[(S.population == POP_HEAD) & (S.cost_bps == 10) & (S.target == "OOS_Sharpe")].iloc[0]
    s0 = S[(S.population == POP_HEAD) & (S.cost_bps == 0) & (S.target == "OOS_Sharpe")].iloc[0]

    H = {}
    H["G1 repro"] = (G1ok, "837's books.csv + all three committed cells rebuilt")
    H["G2 cost identity"] = (G2ok, f"max|d| {d2:.3e}")
    H["G3 monotone"] = (G3ok, f"up-steps: {', '.join(g3msg)} on {len(FINE)}x{len(ARMS)}")
    H["G4 no leverage"] = (G4ok, f"max gross {d4:.4f}")
    H["K0 ceiling"] = (K0ok, f"rho(NEGTURN, 1/turn) {k0:+.6f}")
    H["H_MECH"] = (mech.spearman >= raw.spearman,
                   f"mech {mech.spearman:+.4f} vs raw {raw.spearman:+.4f}")
    H["H_SHARE"] = (np.isfinite(share) and share >= SHARE_BAR,
                    f"arithmetic share {share:.4f} vs bar {SHARE_BAR}")
    H["H_RECON"] = (np.isfinite(recon) and recon >= RECON_BAR,
                    f"rho(c_star, c_hat) {recon:+.4f} vs bar {RECON_BAR}")
    H["H_RESID"] = ((drag.iid_p > 0.05) and not drag.cl_excl0,
                    f"DRAGFREE rho {drag.spearman:+.4f}, p {drag.iid_p:.4f}, "
                    f"CI [{drag.cl_lo:+.4f}, {drag.cl_hi:+.4f}]")
    H["H_RESID_SIG"] = ((drag.spearman >= RESID_BAR) and drag.cl_excl0,
                        f"DRAGFREE rho {drag.spearman:+.4f} vs bar {RESID_BAR}, "
                        f"excl0 {drag.cl_excl0}")
    H["H_OOSSH_0"] = ((s0.iid_p <= 0.05) and s0.cl_excl0,
                      f"0 bps rho {s0.spearman:+.4f}, p {s0.iid_p:.4f}, "
                      f"CI [{s0.cl_lo:+.4f}, {s0.cl_hi:+.4f}]")
    H["H_OOSSH_DROP"] = ((s10.spearman - s0.spearman) >= DROP_BAR,
                         f"10bps {s10.spearman:+.4f} - 0bps {s0.spearman:+.4f} = "
                         f"{s10.spearman - s0.spearman:+.4f} vs bar {DROP_BAR}")
    H["H_POP"] = ((np.sign(raw.spearman) == np.sign(raw0.spearman))
                  and ((raw.iid_p <= 0.05) == (raw0.iid_p <= 0.05)),
                  f"ALL39 {raw.spearman:+.4f} p {raw.iid_p:.4f} | "
                  f"PASS0 {raw0.spearman:+.4f} p {raw0.iid_p:.4f}")
    H["H_SETFREE"] = (setspread <= SETFREE_BAR,
                      f"rung-set spread of RAW {setspread:.4f} vs bar {SETFREE_BAR}")

    # ---- RULE 8 ON THE CLAIM, read exactly once ------------------------------------------
    hdr("RULE 8 ON THE CLAIM - choose the cell on IS (..2016) ONLY, read it ONCE on OOS")
    ISrows = []
    keys = ARMS
    fams = [FAMOF[k] for k in keys]
    neg = B.loc[keys, "NEGTURN"].values
    for rs in RUNGSETS:
        for key in keys:
            if rs == "CONT":
                B.loc[key, f"csIS_{rs}"] = B.loc[key, "c_star_IS"]
                B.loc[key, f"csOOS_{rs}"] = B.loc[key, "c_star_OOS"]
            else:
                for tag, wn in (("csIS", "IS"), ("csOOS", "OOS")):
                    s = -1.0
                    for c in RUNGSETS[rs]:
                        if pass_cost(key, c, wn):
                            s = float(c)
                    B.loc[key, f"{tag}_{rs}"] = s
    for rs in RUNGSETS:
        for dec in DECOMPS:
            def tgt_for(tag, dstar, chat):
                cs = B.loc[keys, f"{tag}_{rs}"].values
                if dec == "RAW":
                    return cs, None
                if dec == "MECHPRED":
                    return B.loc[keys, chat].values, None
                if dec == "DRAGFREE":
                    return B.loc[keys, dstar].values, None
                if dec == "DIVTURN":
                    return cs * B.loc[keys, "turn_yr"].values, None
                return cs, B.loc[keys, dstar].values
            ti, ci_ = tgt_for("csIS", "D_star_IS", "c_hat_IS")
            to, co_ = tgt_for("csOOS", "D_star_OOS", "chat_OOSLOC")
            rIS = partial_spearman(neg, ti, ci_) if ci_ is not None else spearman(neg, ti)
            rOOS = partial_spearman(neg, to, co_) if co_ is not None else spearman(neg, to)
            ISrows.append(dict(rung_set=rs, decomposition=dec, rho_IS=rIS, rho_OOS=rOOS,
                               gap=abs(rIS - rOOS)))
    W = pd.DataFrame(ISrows)
    P("   " + f"{'rungs':<8}{'decomp':<10}{'rho IS(..2016)':>16}{'rho OOS(2017..)':>17}{'gap':>9}")
    for r in W.itertuples():
        P(f"   {r.rung_set:<8}{r.decomposition:<10}{r.rho_IS:>+16.4f}{r.rho_OOS:>+17.4f}"
          f"{r.gap:>9.4f}")
    pick = W.loc[W.rho_IS.idxmax()]
    P(f"\n   IS-chosen cell (highest rho on ..2016 alone): ({pick.decomposition}, {pick.rung_set})"
      f" rho_IS {pick.rho_IS:+.4f}")
    P(f"   read ONCE on 2017.. : rho_OOS {pick.rho_OOS:+.4f}   gap {pick.gap:.4f}  "
      f"vs bar {R8_BAR}  {'PASS' if pick.gap <= R8_BAR else 'FAIL'}")
    H["H_R8CLAIM"] = (pick.gap <= R8_BAR,
                      f"({pick.decomposition},{pick.rung_set}) IS {pick.rho_IS:+.4f} -> OOS "
                      f"{pick.rho_OOS:+.4f}, gap {pick.gap:.4f}")
    W.to_csv(f"{OUT}.walkforward_claim.csv", index=False)

    hdr("HYPOTHESIS SCORECARD")
    npass = 0
    for k, (ok, why) in H.items():
        npass += int(bool(ok))
        P(f"   {'PASS' if ok else 'FAIL'}  {k:<18} {why}")
    P(f"\n   {npass} of {len(H)} PASS")

    B.to_csv(f"{OUT}.books.csv")
    P(f"\n# runtime {time.time()-T0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
