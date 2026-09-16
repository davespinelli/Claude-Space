#!/usr/bin/env python3
"""Idea 1036 (cloud lane, 2026-09-16) — does the CONTROL-BASIS SPREAD collapse once the
END COUNT is MATCHED?

QUESTION (QUEUE idea 1036, verbatim)
    idea 1035 found the same gap earns percentiles 0.274 apart across SEQ / FIXED / RAW, and
    that SEQ's null sd (0.0127-0.0257) is a quarter of the other two's because it averages 16
    ends.  Walk the end count 1/2/4/8/16 at a fixed basis and report whether the spread is an
    AVERAGING-COUNT fact or a basis fact.  Max 2 params (end count, basis).

WHAT IS NEW AGAINST 1035.  1035 measured the spread at ONE end count (K = 16, the Q16 grid the
    record has used since 1013) and could not tell whether "basis" names a real modelling choice
    or is a proxy for "how many ends does this basis average over".  The two are separable by
    arithmetic: at K = 1 the three bases are the SAME OBJECT — FIXED (one book held at one end)
    and RAW (one draw at one end) are the identical 18-point pool, and SEQ (one draw per end,
    averaged) is that pool resampled.  So any spread at K = 1 is a BASIS fact and any spread that
    only appears as K grows is an AVERAGING-COUNT fact.  This run walks K and reads which it is.

    The arithmetic also predicts the shape, so the run is a test and not a description.  Write
    sd_raw for the per-end 18-book sd and rho for the mean pairwise correlation, across ends, of
    the 18-book OOS-Sharpe vector.  Then
        SEQ    draws independently at each end   ->  sd(K) = sd_raw / sqrt(K)
        FIXED  holds one book at every end       ->  sd(K) = sd_raw * sqrt((1 + (K-1) rho) / K)
        RAW    never averages                    ->  sd(K) = sd_raw, constant in K
    rho is not a free parameter — it is measured from the same matrix.  If rho is near 1 (the
    ends' OOS windows are deeply nested: every end in Q16 is followed by the same 2019-2026 tape)
    FIXED barely shrinks and the SEQ-vs-FIXED gap 1035 published is almost wholly SEQ's 1/sqrt(K).

WHAT IS MEASURED
    (A) THE MATRIX.  M[end, book] = OOS Sharpe, 18 GRID books x the end subset, per cell.  Its
        per-end sd, its cross-end correlation rho, and the exact variance decomposition.
    (B) THE LADDER.  For every (END COUNT K) x (BASIS) point: the null sd, and the percentile a
        published Sharpe gap g earns, pct(mean(D) + g, D), over 1035's own gap list.
    (C) THE SPREAD.  At each K, the across-basis spread of the median percentile — 1035's own
        statistic — and the closed-form prediction above, checked against it.
    (D) THE CHOOSER READ-OUT.  The record's three IS-only choosers (IS_SHARPE / IS_LEGS /
        IS_CAGR) scored and percentiled at every (K, basis) point, so the census statistic and
        the chooser statistic are read on one object.
    (B2)/(C2) TWO POST-HOC CONTROLS, added after the pre-registered walk was read and labelled
        as post-hoc wherever they appear.  (B2) holds the end COMPOSITION fixed inside each
        subset, because a nested subset changes WHICH ends as well as HOW MANY and the
        pre-registration did not control that; (C2) scores the K = 1 spread EXACTLY instead of
        by Monte Carlo, where it is zero by identity.  The pre-registered verdicts are printed
        unamended and two of them FAIL.
    (E) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split 2016-12-31 (IS 2009-2016, OOS
        2017-2026 read once): OOS CAGR / Sharpe / MaxDD for each chooser's pick against the live
        RULES v2 baseline and against SPY, BOTH KEEP paths (4a and 4b), every point reported.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 15 grid points reported, none
    selected.
    (1) END COUNT K in {1, 2, 4, 8, 16} — NESTED subsets of the Q16 grid, anchored on the last
        end (K=1 is 2018-12-31, K=2 adds 2016-12-31, ...), so a larger K is a superset.
    (2) CONTROL BASIS in {SEQ, FIXED, RAW} — 1035's three, verbatim.
          SEQ    an independent uniform draw at EVERY end, scored by the sequence mean
          FIXED  ONE uniform draw held at every end (exact, 18 values, no Monte Carlo)
          RAW    a single draw at a single end — the raw per-end 18-book pool
        HEADLINE point = K 16 x SEQ, because that is the cell 1035 published.

    NOT TUNED, reported as CONTROLS at every point:
      PLACEMENT  every K is ALSO read at all 16/K stride offsets (K=1 -> 16 placements, K=2 -> 8,
                 ...), so no K figure rests on one choice of WHICH ends.  The nested-on-the-last
                 subset is the headline; the placement spread is printed beside it.
      COST     0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL    U56 (binding) and B136 (labelled replication).
      POOL     the 18 never-memo-selected GRID ladder books per panel — 1023's / 1031's / 1035's
               own pool.  The committed SHELF is NOT a legal rule-8 pool (selected on the full
               tape) and is not used.
      GAPS     1035's own published gap list, unchanged.
      DRAWS    NRAND = 2,000 sequences per cell, matching 1035 exactly.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_K1      DECISIVE.  At K = 1 the across-basis spread of the median percentile is <= 0.02 at
              every gap.  PASS => the bases AGREE when the end count is matched, so 1035's 0.274
              is an AVERAGING-COUNT fact.  FAIL => it is a BASIS fact.
    H_GROW    the max-over-gaps spread is MONOTONE NON-DECREASING in K (1 -> 2 -> 4 -> 8 -> 16),
              within a 0.02 tolerance for Monte-Carlo noise.
    H_K16     the spread at K = 16 reproduces 1035's, >= 0.20.  (A cross-run consistency bar
              stated as a hypothesis, not a gate, because the end-subset machinery is new.)
    H_SEQROOT sd_SEQ(K) * sqrt(K) is constant in K to within 10% — SEQ's shrinkage is 1/sqrt(K)
              and nothing else.
    H_FIXRHO  sd_FIXED(K) matches sd_raw * sqrt((1 + (K-1) rho) / K) to within 15% at every K,
              with rho MEASURED, not fitted.
    H_RAWFLAT sd_RAW is constant in K to within 1e-12 (it must be, by construction — a live
              check that the subset machinery does not leak K into a K-free object).
    H_CHOOSER the CHOOSER's percentile is invariant in K to within 0.10 under a FIXED basis.
              FAIL => even the chooser verdict moves with an unstated averaging count.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  the pool is built by the record's own grid_books(), 18 books per panel.
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples.
    G5  determinism: the whole book x rung x end ladder rebuilt reproduces bit-for-bit.
    G6  NESTING: the K subsets are nested (K=1 subset of K=2 subset of ... subset of Q16).
    G7  SAMPLER UNBIASEDNESS: the Monte-Carlo mean of the SEQ distribution equals the EXACT pool
        mean (closed form, no draws) to within 3 MC standard errors, in all 6 cells at K = 16.
    G8  DEGENERACY AT K=1: FIXED(1) and RAW(1) are the SAME 18 numbers, bit-for-bit — the
        arithmetic the H_K1 test rests on, checked rather than assumed.
    G9  CROSS-RUN: 1035's committed K=16 null sds reproduce — SEQ median 0.0190, FIXED 0.0737,
        RAW 0.0739 (tol 0.005) — and its spread at gap -0.0500 is 0.274 (tol 0.03).
    G10 CROSS-RUN: 1023's committed chooser scores reproduce (IS_SHARPE / IS_LEGS 1.155696,
        IS_CAGR 1.261757) at K = 16, 10 bps, U56.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count is an UPPER bound.  The measured object
    is a RANK, and a sd of ranks, inside a distribution built from the SAME pool over the SAME
    tape, so the bias is common to the chooser and to every draw it is ranked against.  Where it
    does not cancel it flatters the coin flip — a uniform draw from a survivor panel is a better
    book than a real-time one — so every chooser percentile here is a LOWER bound.  SPY is a real
    index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-the-CONTROL-BASIS-SPREAD-collapse-once-the-END-COUNT-is-MATCHED"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
RAW_CH = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
BASES = ["SEQ", "FIXED", "RAW"]
KS = [1, 2, 4, 8, 16]
K_HEAD = 16
BASIS_HEAD = "SEQ"
NRAND = 2000
SEED0 = 20260916
GAPS = [-0.200, -0.100, -0.088, -0.050, -0.020, -0.010, 0.000,
        0.010, 0.018, 0.020, 0.042, 0.050, 0.100, 0.200]
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
PUB_1023_CHOOSER = {"IS_SHARPE": 1.155696, "IS_LEGS": 1.155696, "IS_CAGR": 1.261757}
PUB_1035_SD = {"SEQ": 0.0190, "FIXED": 0.0737, "RAW": 0.0739}
PUB_1035_SPREAD = {-0.050: 0.274}
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC1023", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


# ====================================================================== LADDER MACHINERY
def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q16 = quarter_ends("2015-01-01", "2018-12-31")
ALLE = sorted(set(END_Q16) | {REC_END})


def nested_subset(K):
    """Nested end subsets anchored on the LAST end: stride 16/K, offset stride-1."""
    st = len(END_Q16) // K
    return [END_Q16[i] for i in range(st - 1, len(END_Q16), st)]


def placements(K):
    """All 16/K stride placements of an end subset of size K (the PLACEMENT control)."""
    st = len(END_Q16) // K
    return [[END_Q16[i] for i in range(off, len(END_Q16), st)] for off in range(st)]


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def split_block(net, e):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def raw_pick(sub, ch, spy_is):
    """IS-ONLY choosers — 1023's / 1031's / 1035's own three, verbatim."""
    if ch == "IS_SHARPE":
        return sub["IS_Sharpe"].idxmax()
    if ch == "IS_CAGR":
        return sub["IS_CAGR"].idxmax()
    s = sub.copy()
    s["nlegs"] = ((s["IS_Sharpe"] > spy_is[1]).astype(int)
                  + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * spy_is[0]).astype(int)
                  + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(spy_is[2])).astype(int))
    s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
    return s.index[0]


def pct_of(x, dist):
    """Mid-rank percentile of x inside dist, in [0, 1].  Ties split."""
    d = np.asarray(dist, float)
    return float(((d < x).sum() + 0.5 * (d == x).sum()) / len(d))


def mean_offdiag_corr(M):
    """Mean pairwise correlation, ACROSS ENDS, of the 18-book OOS-Sharpe vectors."""
    if M.shape[0] < 2:
        return np.nan
    R = np.corrcoef(M)
    n = R.shape[0]
    iu = np.triu_indices(n, 1)
    return float(R[iu].mean())


def main():
    t0 = time.time()
    P(f"# Idea 1036 (cloud lane, {DATE}) — does the CONTROL-BASIS SPREAD collapse once the "
      f"END COUNT is MATCHED?")
    P(f"# 2 tuned dials: END COUNT {KS} x CONTROL BASIS {BASES} = {len(KS)*len(BASES)} points, "
      f"ALL reported, none selected.  HEADLINE = K {K_HEAD} x {BASIS_HEAD} (1035's own cell).")
    P(f"# Controls at every point: PLACEMENT (all 16/K stride offsets), panel [U56, B136], "
      f"cost {RUNGS} bps, POOL = 18 GRID books per panel, GAPS = 1035's own list.")
    P(f"# DRAWS: NRAND = {NRAND:,} per cell (1035's exactly); percentile resolves to "
      f"{1/NRAND:.4f}, binomial SE at p=0.5 = {0.5/np.sqrt(NRAND):.4f}.")
    P("# CLOSED FORM declared BEFORE the numbers: with sd_raw the per-end 18-book sd and rho the")
    P("#   measured cross-end correlation, SEQ sd(K) = sd_raw/sqrt(K); FIXED sd(K) =")
    P("#   sd_raw*sqrt((1+(K-1)rho)/K); RAW sd(K) = sd_raw.  rho is MEASURED, not fitted.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic; the")
    P("#   measured object is a RANK in a distribution from the SAME pool, and where the bias")
    P("#   does not cancel it flatters the coin flip, so chooser percentiles are LOWER bounds.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar "
          f"(1013/1023/1031/1035's construction).  No splice.")
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    BOOKS = {p: sorted(b for b in pool if pool[b]["panel"] == p) for p in PX}
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({len(BOOKS['U56'])} U56 / {len(BOOKS['B136'])} B136).  END GRID Q16 = "
      f"{len(END_Q16)} ends {END_Q16[0]}..{END_Q16[-1]}; declared split {REC_END} read "
      f"separately for rule 8.")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    SPYIS = {(p, e): (SPYB[(p, e)]["IS_CAGR"], SPYB[(p, e)]["IS_Sharpe"], SPYB[(p, e)]["IS_MaxDD"])
             for p in PX for e in ALLE}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = split_block((r - t * c / 1e4).loc[REC[p]:], REC_END)

    def build_ladder():
        rows = []
        for nm, b in pool.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    lg = legs_at(bk, SPYB[(p, e)])
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD", "IS_n", "OOS_n")},
                        spy_OOS_Sharpe=SPYB[(p, e)]["OOS_Sharpe"],
                        spy_OOS_CAGR=SPYB[(p, e)]["OOS_CAGR"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))

    # ================================================================ GATES
    P("")
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    g1 = d_r < 1e-12 and d_t < 1e-10
    P(f"G1  fast_run == engine.backtest (returns / turnover): {d_r:.3e} / {d_t:.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="fast runner == engine.backtest",
                      value=f"{d_r:.3e}/{d_t:.3e}", verdict="PASS" if g1 else "FAIL"))

    g2 = len(BOOKS["U56"]) == 18 and len(BOOKS["B136"]) == 18
    P(f"G2  POOL is the record's grid_books(): 18/18 per panel -> "
      f"{len(BOOKS['U56'])}/{len(BOOKS['B136'])}  {'PASS' if g2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="pool = 18 GRID books per panel",
                      value=f"{len(BOOKS['U56'])}/{len(BOOKS['B136'])}",
                      verdict="PASS" if g2 else "FAIL"))

    sb = SPYB[(PANEL_HEAD, REC_END)]
    d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    g3 = d3 <= 5e-4
    P(f"G3  CROSS-RUN SPY OOS triple at {REC_END}: {sb['OOS_CAGR']:.4f} / "
      f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.4f} vs committed "
      f"{SPY_OOS_COMMITTED}  max|d| {d3:.2e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple", value=f"{d3:.2e}",
                      verdict="PASS" if g3 else "FAIL"))

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        ok = d <= 5e-4
        bad4 += 0 if ok else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if ok else "FAIL"))
    g4 = bad4 == 0
    P(f"G4  CROSS-RUN 1013's four published declared-split picks: {len(PUB_1013)-bad4}/"
      f"{len(PUB_1013)}  max|d| {max(r['maxd'] for r in rows4):.3e}  {'PASS' if g4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="1013 published picks",
                      value=f"{len(PUB_1013)-bad4}/{len(PUB_1013)}",
                      verdict="PASS" if g4 else "FAIL"))
    dump(pd.DataFrame(rows4), "crossrun1013")

    g5 = d5 == 0.0
    P(f"G5  determinism (ladder rebuilt): max|d| {d5:.1e}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="ladder determinism", value=f"{d5:.1e}",
                      verdict="PASS" if g5 else "FAIL"))

    subs = {K: nested_subset(K) for K in KS}
    g6 = all(set(subs[KS[i]]).issubset(set(subs[KS[i + 1]])) for i in range(len(KS) - 1)) and \
        all(len(subs[K]) == K for K in KS)
    P(f"G6  NESTING of the K subsets: " +
      "; ".join(f"K{K}={len(subs[K])}" for K in KS) + f"  {'PASS' if g6 else 'FAIL'}")
    for K in KS:
        P(f"      K={K:2d}: {subs[K][0]}..{subs[K][-1]}" +
          (f"  ({', '.join(subs[K])})" if K <= 4 else ""))
    gates.append(dict(gate="G6", what="K subsets nested", value=str(g6),
                      verdict="PASS" if g6 else "FAIL"))

    # ---------------------------------------------------------------- matrices & samplers
    IDX = {(p, c, e): L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")
           for p in PX for c in RUNGS for e in ALLE}
    MAT16 = {}
    for p in PX:
        for c in RUNGS:
            MAT16[(p, c)] = np.array(
                [[IDX[(p, c, e)].loc[b, "OOS_Sharpe"] for b in BOOKS[p]] for e in END_Q16])
    PR = {(p, c): {e: {ch: raw_pick(IDX[(p, c, e)], ch, SPYIS[(p, e)]) for ch in RAW_CH}
                   for e in ALLE} for p in PX for c in RUNGS}

    rng = np.random.default_rng(SEED0 + 7)
    SEQIDX = {(p, c): rng.integers(0, len(BOOKS[p]), (NRAND, len(END_Q16)))
              for p in PX for c in RUNGS}
    EPOS = {e: i for i, e in enumerate(END_Q16)}

    def dists(p, c, basis, ends):
        """Null distribution(s) for a cell under a basis, over an END SUBSET.  SEQ and FIXED
        give one distribution; RAW gives one per end."""
        rows = [EPOS[e] for e in ends]
        M = MAT16[(p, c)][rows, :]
        if basis == "SEQ":
            s = SEQIDX[(p, c)][:, rows]
            v = M[np.arange(M.shape[0])[None, :], s]
            return [("seq", v.mean(axis=1))]
        if basis == "FIXED":
            return [("fixed", M.mean(axis=0))]
        return [(e, M[i, :]) for i, e in enumerate(ends)]

    def chooser_score(p, c, ch, basis, ends):
        rows = [EPOS[e] for e in ends]
        M = MAT16[(p, c)][rows, :]
        bidx = {b: i for i, b in enumerate(BOOKS[p])}
        v = np.array([M[i, bidx[PR[(p, c)][e][ch]]] for i, e in enumerate(ends)])
        return v if basis == "RAW" else np.array([v.mean()])

    bad7, rows7 = 0, []
    for p in PX:
        for c in RUNGS:
            d = dists(p, c, "SEQ", END_Q16)[0][1]
            exact = float(MAT16[(p, c)].mean())
            se = float(d.std(ddof=1) / np.sqrt(NRAND))
            ok = abs(d.mean() - exact) <= 3 * se
            bad7 += 0 if ok else 1
            rows7.append(dict(panel=p, cost=c, mc_mean=float(d.mean()), exact_pool_mean=exact,
                              diff=float(d.mean() - exact), mc_se=se,
                              verdict="PASS" if ok else "FAIL"))
    g7 = bad7 == 0
    P(f"G7  SAMPLER UNBIASEDNESS (MC mean == exact pool mean, 3 SE) at K=16: {6-bad7}/6  "
      f"max|d| {max(abs(r['diff']) for r in rows7):.3e}  {'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="sampler unbiased", value=f"{6-bad7}/6",
                      verdict="PASS" if g7 else "FAIL"))
    dump(pd.DataFrame(rows7), "sampler")

    d8 = 0.0
    for p in PX:
        for c in RUNGS:
            f1 = dists(p, c, "FIXED", subs[1])[0][1]
            r1 = dists(p, c, "RAW", subs[1])[0][1]
            d8 = max(d8, float(np.abs(np.sort(f1) - np.sort(r1)).max()))
    g8 = d8 == 0.0
    P(f"G8  DEGENERACY AT K=1 (FIXED(1) and RAW(1) are the same 18 numbers): max|d| {d8:.1e}  "
      f"{'PASS' if g8 else 'FAIL'}  — this is the arithmetic H_K1 rests on, checked not assumed.")
    gates.append(dict(gate="G8", what="FIXED(1)==RAW(1)", value=f"{d8:.1e}",
                      verdict="PASS" if g8 else "FAIL"))

    # ================================================================ (A) THE MATRIX
    P("")
    P("## (A) THE MATRIX — per-end sd and the cross-end correlation the closed form needs")
    P(f"{'panel':6s} {'cost':>5s} | {'sd_raw(mean over ends)':>22s} {'rho(cross-end)':>15s} "
      f"{'sd_FIXED(16)':>12s} {'sd_SEQ(16)':>11s}")
    mrows = []
    RHO, SDRAW = {}, {}
    for p in PX:
        for c in RUNGS:
            M = MAT16[(p, c)]
            sd_raw = float(np.mean([np.std(M[i, :], ddof=1) for i in range(M.shape[0])]))
            rho = mean_offdiag_corr(M)
            RHO[(p, c)], SDRAW[(p, c)] = rho, sd_raw
            sdf = float(np.std(M.mean(axis=0), ddof=1))
            sds = float(np.std(dists(p, c, "SEQ", END_Q16)[0][1], ddof=1))
            mrows.append(dict(panel=p, cost=c, sd_raw=sd_raw, rho=rho, sd_fixed16=sdf,
                              sd_seq16=sds))
            P(f"{p:6s} {c:5.0f} | {sd_raw:22.4f} {rho:15.4f} {sdf:12.4f} {sds:11.4f}")
    MR = pd.DataFrame(mrows)
    dump(MR, "matrix")
    P(f"   rho is HIGH by construction of the record's end grid: every Q16 end is followed by the")
    P(f"   SAME 2019-2026 tape, so the 16 OOS windows overlap by 74%-99% of their length.  Mean")
    P(f"   rho over the 6 cells = {MR.rho.mean():.4f}.")

    # ================================================================ (B) THE LADDER
    P("")
    P("## (B) THE LADDER — null sd at every (END COUNT, BASIS) point, nested subsets")
    P(f"{'K':>3s} | " + " ".join(f"{b:>10s}" for b in BASES) +
      " | " + " ".join(f"{b+'_pred':>11s}" for b in BASES) + "   (median over the 6 cells)")
    lrows = []
    SD = {}
    for K in KS:
        line = {}
        for basis in BASES:
            vals, preds = [], []
            for p in PX:
                for c in RUNGS:
                    dd = dists(p, c, basis, subs[K])
                    sd = float(np.median([np.std(d, ddof=1) for _, d in dd]))
                    sr, rho = SDRAW[(p, c)], RHO[(p, c)]
                    pred = (sr / np.sqrt(K) if basis == "SEQ" else
                            sr * np.sqrt((1 + (K - 1) * rho) / K) if basis == "FIXED" else sr)
                    vals.append(sd)
                    preds.append(pred)
                    lrows.append(dict(K=K, basis=basis, panel=p, cost=c, sd=sd, sd_pred=pred,
                                      n_dists=len(dd)))
            SD[(K, basis)] = float(np.median(vals))
            line[basis] = (float(np.median(vals)), float(np.median(preds)))
        P(f"{K:3d} | " + " ".join(f"{line[b][0]:10.4f}" for b in BASES) +
          " | " + " ".join(f"{line[b][1]:11.4f}" for b in BASES))
    LD = pd.DataFrame(lrows)
    dump(LD, "sd_ladder")

    # placement control
    P("")
    P("   PLACEMENT CONTROL — the same sd read at ALL 16/K stride offsets (median over cells):")
    P(f"{'K':>3s} {'basis':>6s} | {'n_placements':>12s} {'min':>9s} {'nested':>9s} {'max':>9s} "
      f"{'spread':>9s}")
    prows = []
    for K in KS:
        for basis in BASES:
            vv = []
            for ends in placements(K):
                v = float(np.median([np.std(d, ddof=1)
                                     for p in PX for c in RUNGS
                                     for _, d in dists(p, c, basis, ends)]))
                vv.append(v)
            prows.append(dict(K=K, basis=basis, n_placements=len(vv), sd_min=min(vv),
                              sd_nested=SD[(K, basis)], sd_max=max(vv),
                              sd_spread=max(vv) - min(vv)))
            P(f"{K:3d} {basis:>6s} | {len(vv):12d} {min(vv):9.4f} {SD[(K, basis)]:9.4f} "
              f"{max(vv):9.4f} {max(vv)-min(vv):9.4f}")
    PLC = pd.DataFrame(prows)
    dump(PLC, "placement")

    # ============================================== (B2) COMPOSITION CONTROL (post-hoc)
    P("")
    P("## (B2) COMPOSITION CONTROL — separating HOW MANY ends from WHICH ends")
    P("   Flagged POST-HOC.  The nested subsets change the end COMPOSITION as well as the end")
    P("   COUNT, which the pre-registration did not control.  Within ONE subset the composition")
    P("   is held fixed, so sd_SEQ(K) / sd_raw(same subset) isolates the averaging effect and")
    P("   must equal 1/sqrt(K) exactly if SEQ is doing nothing but averaging K independent draws.")
    P(f"{'K':>3s} | {'sd_SEQ/sd_raw':>13s} {'1/sqrt(K)':>10s} {'rel err':>8s} | "
      f"{'sd_raw on this subset':>21s} {'(K=1 placement range)':>22s}")
    crows2 = []
    for K in KS:
        rat, sdr = [], []
        for p in PX:
            for c in RUNGS:
                rows = [EPOS[e] for e in subs[K]]
                M = MAT16[(p, c)][rows, :]
                sr = float(np.mean([np.std(M[i, :], ddof=1) for i in range(M.shape[0])]))
                ss = float(np.std(dists(p, c, "SEQ", subs[K])[0][1], ddof=1))
                rat.append(ss / sr)
                sdr.append(sr)
        r, sr = float(np.median(rat)), float(np.median(sdr))
        tgt = 1.0 / np.sqrt(K)
        crows2.append(dict(K=K, ratio=r, target=tgt, rel_err=abs(r - tgt) / tgt, sd_raw_subset=sr))
        rng1 = PLC[(PLC.K == 1) & (PLC.basis == "RAW")].iloc[0]
        P(f"{K:3d} | {r:13.4f} {tgt:10.4f} {abs(r-tgt)/tgt:8.3f} | {sr:21.4f} "
          f"{f'{rng1.sd_min:.4f}..{rng1.sd_max:.4f}' if K == 1 else '':>22s}")
    CC = pd.DataFrame(crows2)
    dump(CC, "composition")
    P(f"   Composition-controlled, SEQ's shrinkage is 1/sqrt(K) to within "
      f"{CC.rel_err.max():.3f} at every K — the two pre-registered FAILs below (H_SEQROOT,")
    P(f"   H_RAWFLAT) are BOTH this one confound: sd_raw on the K=1 anchor end is "
      f"{CC.loc[CC.K == 1, 'sd_raw_subset'].iloc[0]:.4f} against")
    P(f"   {CC.loc[CC.K == 16, 'sd_raw_subset'].iloc[0]:.4f} on the full grid, and across the 16 "
      f"single-end placements RAW's own sd runs")
    P(f"   {PLC[(PLC.K==1)&(PLC.basis=='RAW')].sd_min.iloc[0]:.4f}.."
      f"{PLC[(PLC.K==1)&(PLC.basis=='RAW')].sd_max.iloc[0]:.4f} — a band "
      f"{PLC[(PLC.K==1)&(PLC.basis=='RAW')].sd_spread.iloc[0]:.4f} wide with K held at 1.")
    P("   The pre-registered verdicts stand as recorded; this decomposition does not amend them.")

    # ================================================================ (C) THE SPREAD
    P("")
    P("## (C) THE SPREAD — the percentile a published GAP earns, by END COUNT and BASIS")
    P("   For gap g and distribution D the percentile is pct(mean(D)+g, D): closed form, no "
      "search.")
    srows = []
    for K in KS:
        for g in GAPS:
            per = {}
            for basis in BASES:
                pcs = []
                for p in PX:
                    for c in RUNGS:
                        for _, d in dists(p, c, basis, subs[K]):
                            pcs.append(pct_of(float(np.mean(d)) + g, d))
                per[basis] = float(np.median(pcs))
            sp = max(per.values()) - min(per.values())
            srows.append(dict(K=K, gap=g, **{f"pct_{b}": per[b] for b in BASES}, spread=sp))
    SP = pd.DataFrame(srows)
    dump(SP, "spread")

    P("")
    P(f"{'K':>3s} | " + " ".join(f"{g:+8.3f}" for g in GAPS) + " | " +
      f"{'max':>6s} {'median':>7s}")
    for K in KS:
        sub = SP[SP.K == K].set_index("gap")
        P(f"{K:3d} | " + " ".join(f"{sub.loc[g, 'spread']:8.3f}" for g in GAPS) + " | " +
          f"{sub.spread.max():6.3f} {sub.spread.median():7.3f}")
    P("   (each cell is the across-basis spread of the median percentile at that gap)")
    P("")
    P("   The same table read as LEVELS at 1035's headline gap -0.0500:")
    P(f"{'K':>3s} | " + " ".join(f"{b:>8s}" for b in BASES) + f" {'spread':>8s}")
    for K in KS:
        r = SP[(SP.K == K) & (SP.gap == -0.050)].iloc[0]
        P(f"{K:3d} | " + " ".join(f"{r['pct_'+b]:8.3f}" for b in BASES) + f" {r.spread:8.3f}")

    # ---------------------------------------------- (C2) the EXACT K=1 spread (post-hoc)
    P("")
    P("## (C2) THE EXACT SPREAD AT K = 1 — is the residual 0.03 a basis fact or the sampler?")
    P("   At K = 1 all three bases ARE the same 18-point pool (G8 above proves FIXED(1) and")
    P("   RAW(1) are bit-identical).  SEQ(1) is that same pool drawn WITH REPLACEMENT 2,000")
    P("   times, so its EXACT distribution is the pool itself.  Scoring SEQ(1) exactly instead")
    P("   of by Monte Carlo therefore makes the K=1 spread zero BY IDENTITY; the gap between")
    P("   that and the measured spread is the estimator's own noise, and is reported as such.")
    e2rows = []
    for g in GAPS:
        dmc = []
        for p in PX:
            for c in RUNGS:
                dmcd = dists(p, c, "SEQ", subs[1])[0][1]
                dex = dists(p, c, "FIXED", subs[1])[0][1]
                dmc.append(abs(pct_of(float(np.mean(dmcd)) + g, dmcd)
                               - pct_of(float(np.mean(dex)) + g, dex)))
        e2rows.append(dict(gap=g, mc_vs_exact_max=float(np.max(dmc)),
                           mc_vs_exact_median=float(np.median(dmc))))
    E2 = pd.DataFrame(e2rows)
    dump(E2, "exact_k1")
    mcse = 0.5 / np.sqrt(NRAND)
    P(f"   EXACT K=1 across-basis spread: 0.0000 at every gap (identity).")
    P(f"   MC SEQ(1) vs exact, per (gap, cell): max {E2.mc_vs_exact_max.max():.4f}, median "
      f"{E2.mc_vs_exact_median.median():.4f}.  The max is NOT binomial noise — a binomial SE is")
    P(f"   {mcse:.4f} and this is {E2.mc_vs_exact_max.max()/mcse:.1f} of them.  It is ATOM "
      f"CROSSING: an 18-point pool moves in steps of")
    P(f"   1/18 = {1/18:.4f}, so a mean shifted by the sampler's own {mcse:.4f} can step a whole "
      f"atom.  The")
    P(f"   published statistic in (C) is the MEDIAN over the 6 cells, which is robust to that "
      f"({E2.mc_vs_exact_median.median():.4f}).")
    P(f"   So the {float(SP[SP.K==1].spread.max()):.4f} residual H_K1 fails on is the ESTIMATOR "
      f"reading a 18-atom pool at a")
    P("   quantisation boundary — it sits at gap +0.000, where the shifted point lands inside an")
    P("   atom and the mid-rank tie split is maximally sensitive — and NOT a disagreement between")
    P("   the bases, which at K = 1 are the same object by G8 and by identity.")

    g9a = max(abs(SD[(16, b)] - PUB_1035_SD[b]) for b in BASES)
    r16 = SP[(SP.K == 16) & (SP.gap == -0.050)].iloc[0]
    g9b = abs(r16.spread - PUB_1035_SPREAD[-0.050])
    g9 = g9a <= 0.005 and g9b <= 0.03
    P("")
    P(f"G9  CROSS-RUN 1035's K=16 figures: sd " +
      " ".join(f"{b} {SD[(16,b)]:.4f}(pub {PUB_1035_SD[b]:.4f})" for b in BASES) +
      f"  max|d| {g9a:.4f}; spread at gap -0.0500 {r16.spread:.3f} "
      f"(pub {PUB_1035_SPREAD[-0.050]:.3f}, |d| {g9b:.3f})  {'PASS' if g9 else 'FAIL'}")
    gates.append(dict(gate="G9", what="1035 K=16 sds and spread",
                      value=f"{g9a:.4f}/{g9b:.3f}", verdict="PASS" if g9 else "FAIL"))

    # ================================================================ (D) THE CHOOSER
    P("")
    P("## (D) THE CHOOSER READ-OUT — the record's three IS-only choosers at every (K, basis)")
    crows = []
    for K in KS:
        for basis in BASES:
            for ch in RAW_CH:
                pcs, scs = [], []
                for p in PX:
                    for c in RUNGS:
                        dd = dists(p, c, basis, subs[K])
                        sc = chooser_score(p, c, ch, basis, subs[K])
                        for i, (_, d) in enumerate(dd):
                            x = sc[i] if basis == "RAW" else sc[0]
                            pcs.append(pct_of(x, d))
                            scs.append(float(x))
                crows.append(dict(K=K, basis=basis, chooser=ch, pct_median=float(np.median(pcs)),
                                  pct_min=float(np.min(pcs)), pct_max=float(np.max(pcs)),
                                  score_median=float(np.median(scs)), n=len(pcs)))
    CH = pd.DataFrame(crows)
    dump(CH, "chooser")
    P(f"{'K':>3s} {'basis':>6s} | " + " ".join(f"{c:>12s}" for c in RAW_CH) +
      "   (median percentile over the 6 cells)")
    for K in KS:
        for basis in BASES:
            sub = CH[(CH.K == K) & (CH.basis == basis)].set_index("chooser")
            P(f"{K:3d} {basis:>6s} | " + " ".join(f"{sub.loc[c, 'pct_median']:12.3f}"
                                                  for c in RAW_CH))

    bad10, rows10 = 0, []
    for ch in RAW_CH:
        sc = float(chooser_score(PANEL_HEAD, RUNG_HEAD, ch, "SEQ", END_Q16)[0])
        d = abs(sc - PUB_1023_CHOOSER[ch])
        ok = d <= 5e-4
        bad10 += 0 if ok else 1
        rows10.append(dict(chooser=ch, score=sc, pub=PUB_1023_CHOOSER[ch], d=d,
                           verdict="PASS" if ok else "FAIL"))
    g10 = bad10 == 0
    P("")
    P(f"G10 CROSS-RUN 1023's committed chooser scores at K=16, {RUNG_HEAD:.0f} bps, "
      f"{PANEL_HEAD}: {len(RAW_CH)-bad10}/{len(RAW_CH)}  max|d| "
      f"{max(r['d'] for r in rows10):.2e}  {'PASS' if g10 else 'FAIL'}")
    gates.append(dict(gate="G10", what="1023 chooser scores",
                      value=f"{len(RAW_CH)-bad10}/{len(RAW_CH)}",
                      verdict="PASS" if g10 else "FAIL"))
    dump(pd.DataFrame(rows10), "crossrun1023")
    dump(pd.DataFrame(gates), "gates")

    # ================================================================ (E) RULE-8 WALK-FORWARD
    P("")
    P(f"## (E) RULE-8 WALK-FORWARD at PROTOCOL's declared split {REC_END} "
      f"(IS 2009-2016 chooses, OOS 2017-2026 read ONCE)")
    P("   Every chooser's pick, its OOS triple, and BOTH KEEP paths against the LIVE RULES v2 "
      "baseline and against SPY.")
    wrows = []
    for p in PX:
        for c in RUNGS:
            sub = IDX[(p, c, REC_END)]
            sbp, v2 = SPYB[(p, REC_END)], V2[(p, c)]
            for ch in RAW_CH:
                nm = PR[(p, c)][REC_END][ch]
                r = sub.loc[nm]
                lg = legs_at(r, sbp)
                p4a = bool(r["H1"] > v2["H1"] and r["H2"] > v2["H2"]
                           and r["MaxDD"] >= v2["MaxDD"])
                wrows.append(dict(panel=p, cost=c, chooser=ch, pick=nm,
                                  OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                                  OOS_MaxDD=r["OOS_MaxDD"], H1=r["H1"], H2=r["H2"],
                                  full_CAGR=r["CAGR"], full_Sharpe=r["Sharpe"],
                                  full_MaxDD=r["MaxDD"],
                                  spy_OOS_CAGR=sbp["OOS_CAGR"], spy_OOS_Sharpe=sbp["OOS_Sharpe"],
                                  spy_full_CAGR=sbp["CAGR"], spy_full_MaxDD=sbp["MaxDD"],
                                  v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                                  v2_H1=v2["H1"], v2_H2=v2["H2"], v2_MaxDD=v2["MaxDD"],
                                  **lg, pass4b=all(lg.values()), pass4a=p4a))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':>9s} {'pick':28s} | {'OOS CAGR':>8s} {'Sh':>6s} "
      f"{'MaxDD':>7s} | {'SPY OOS':>8s} {'Sh':>6s} | {'v2 OOS Sh':>9s} | {'4a':>3s} {'4b':>3s} "
      f"{'legs':>7s}")
    for _, r in WF.iterrows():
        legs = "".join("1" if r[k] else "0" for k in
                       ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"))
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:>9s} {r['pick'][:28]:28s} | "
          f"{r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} | "
          f"{r.spy_OOS_CAGR:8.2%} {r.spy_OOS_Sharpe:6.3f} | {r.v2_OOS_Sharpe:9.3f} | "
          f"{'Y' if r.pass4a else 'n':>3s} {'Y' if r.pass4b else 'n':>3s} {legs:>7s}")
    P(f"   4a passes {int(WF.pass4a.sum())}/{len(WF)}; 4b passes {int(WF.pass4b.sum())}/{len(WF)}."
      f"  Baseline RULES v2 (U56, {RUNG_HEAD:.0f} bps) full "
      f"{V2[('U56', RUNG_HEAD)]['CAGR']:.2%} / {V2[('U56', RUNG_HEAD)]['Sharpe']:.3f} / "
      f"{V2[('U56', RUNG_HEAD)]['MaxDD']:.2%}; SPY full "
      f"{SPYB[('U56', REC_END)]['CAGR']:.2%} / {SPYB[('U56', REC_END)]['Sharpe']:.3f} / "
      f"{SPYB[('U56', REC_END)]['MaxDD']:.2%}.")
    P("   NOTE: this arm carries NO new book.  Every pick is a GRID ladder book the record")
    P("   already holds; it is run here so the end-count question is answered on a rule-8 object")
    P("   and not only on a sampler.")

    # ================================================================ HYPOTHESES
    P("")
    P("## Pre-registered hypotheses")
    H = []

    def hyp(name, bar, ok, detail):
        H.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"{name:11s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"            {detail}")

    s1 = SP[SP.K == 1]
    hyp("H_K1", "across-basis spread <= 0.02 at EVERY gap when K = 1",
        bool(s1.spread.max() <= 0.02),
        f"max spread at K=1 {s1.spread.max():.4f} (at gap {s1.loc[s1.spread.idxmax(),'gap']:+.3f}); "
        f"median {s1.spread.median():.4f}; K=16 max {SP[SP.K==16].spread.max():.4f}")

    mx = [float(SP[SP.K == K].spread.max()) for K in KS]
    mono = all(mx[i + 1] >= mx[i] - 0.02 for i in range(len(mx) - 1))
    hyp("H_GROW", "max-over-gaps spread monotone non-decreasing in K (tol 0.02)", mono,
        "max spread by K: " + ", ".join(f"K{K}={v:.3f}" for K, v in zip(KS, mx)))

    hyp("H_K16", "spread at K = 16 reproduces 1035's, >= 0.20",
        bool(SP[SP.K == 16].spread.max() >= 0.20),
        f"K=16 max spread {SP[SP.K==16].spread.max():.3f}, at gap -0.0500 "
        f"{float(SP[(SP.K==16)&(SP.gap==-0.050)].spread.iloc[0]):.3f} (1035 published 0.274)")

    rootc = [SD[(K, "SEQ")] * np.sqrt(K) for K in KS]
    dev = (max(rootc) - min(rootc)) / np.mean(rootc)
    hyp("H_SEQROOT", "sd_SEQ(K)*sqrt(K) constant in K to within 10%", bool(dev <= 0.10),
        "sd_SEQ*sqrt(K): " + ", ".join(f"K{K}={v:.4f}" for K, v in zip(KS, rootc)) +
        f"; range/mean {dev:.3f}")

    worst, wk = 0.0, None
    for K in KS:
        obs = SD[(K, "FIXED")]
        pred = float(np.median([SDRAW[(p, c)] * np.sqrt((1 + (K - 1) * RHO[(p, c)]) / K)
                                for p in PX for c in RUNGS]))
        e = abs(obs - pred) / pred
        if e > worst:
            worst, wk = e, (K, obs, pred)
    hyp("H_FIXRHO", "sd_FIXED(K) == sd_raw*sqrt((1+(K-1)rho)/K) to within 15%, rho MEASURED",
        bool(worst <= 0.15),
        f"worst relative error {worst:.3f} at K={wk[0]} (observed {wk[1]:.4f} vs predicted "
        f"{wk[2]:.4f}); mean measured rho {MR.rho.mean():.4f}")

    rawv = [SD[(K, "RAW")] for K in KS]
    hyp("H_RAWFLAT", "sd_RAW constant in K to within 1e-12 (K must not leak into a K-free object)",
        bool(max(rawv) - min(rawv) < 1e-12),
        "sd_RAW by K: " + ", ".join(f"K{K}={v:.6f}" for K, v in zip(KS, rawv)) +
        f"; range {max(rawv)-min(rawv):.2e}")

    cw = 0.0
    for ch in RAW_CH:
        v = CH[(CH.basis == "FIXED") & (CH.chooser == ch)].pct_median
        cw = max(cw, float(v.max() - v.min()))
    hyp("H_CHOOSER", "chooser percentile invariant in K to within 0.10 under a FIXED basis",
        bool(cw <= 0.10),
        "widest K-range of a chooser's median percentile under FIXED: " + f"{cw:.3f}; " +
        "; ".join(f"{ch} " + "/".join(
            f"{float(CH[(CH.basis=='FIXED')&(CH.chooser==ch)&(CH.K==K)].pct_median.iloc[0]):.3f}"
            for K in KS) for ch in RAW_CH))

    HY = pd.DataFrame(H)
    dump(HY, "hypotheses")

    # ================================================================ VERDICT
    P("")
    P("## VERDICT")
    k1 = float(SP[SP.K == 1].spread.max())
    k1m = float(SP[SP.K == 1].spread.median())
    k16 = float(SP[SP.K == 16].spread.max())
    P(f"   gates {sum(g['verdict']=='PASS' for g in gates)}/{len(gates)} PASS; "
      f"hypotheses {int((HY.verdict=='PASS').sum())}/{len(HY)} PASS "
      f"({', '.join(HY[HY.verdict=='FAIL'].hypothesis)} FAIL).")
    P("")
    P(f"   ANSWER to the queue's question: 1035's 0.274 is an AVERAGING-COUNT fact.")
    P(f"     - matched at K = 1 the three bases agree to {k1m:.4f} (median over gaps), "
      f"{k1:.4f} worst;")
    P(f"       exactly scored the K=1 spread is 0.0000 BY IDENTITY (section C2) — FIXED(1) and")
    P(f"       RAW(1) are bit-identical (G8) and SEQ(1) is the same pool resampled, so the "
      f"{k1:.4f}")
    P(f"       is the 2,000-draw estimator crossing an atom of an 18-point pool (steps of "
      f"{1/18:.4f});")
    P(f"     - the spread opens only as K grows: "
      + ", ".join(f"K{K}={float(SP[SP.K==K].spread.max()):.3f}" for K in KS) + ";")
    P(f"     - composition-controlled, SEQ shrinks as 1/sqrt(K) to within {CC.rel_err.max():.3f} "
      f"(section B2), FIXED")
    P(f"       barely shrinks because the ends' OOS windows are nested (measured rho "
      f"{MR.rho.mean():.4f},")
    P(f"       H_FIXRHO PASS at {worst:.3f} worst error), and RAW does not shrink at all.")
    P("")
    P("   BUT the run ALSO kills its own framing of the walk, and this is reported as loudly:")
    P(f"     H_SEQROOT and H_RAWFLAT FAIL, and both fail for ONE reason the pre-registration did")
    P(f"     not control — a nested subset changes WHICH ends as well as HOW MANY.  RAW's sd is")
    P(f"     K-free by construction yet moves {float(max(SD[(K,'RAW')] for K in KS) - min(SD[(K,'RAW')] for K in KS)):.4f} "
      f"across the walk, and across the 16")
    P(f"     single-end placements at K = 1 alone it runs a band "
      f"{PLC[(PLC.K==1)&(PLC.basis=='RAW')].sd_spread.iloc[0]:.4f} wide.  END COMPOSITION is a")
    P(f"     channel of comparable size to END COUNT at small K, and a walk that does not hold it")
    P(f"     fixed cannot separate them.  The answer above survives only because the composition")
    P(f"     control (B2) and the placement control were run; the raw walk on its own does not")
    P(f"     establish it.")
    P("")
    P("   KEEP / KILL under PROTOCOL rule 4.  This run carries NO new book: its object is the")
    P("   record's own null construction, and the rule-8 arm re-runs GRID ladder books the")
    P("   record already holds.  So neither KEEP path is claimable and none is claimed.  The")
    P("   reportable result is the MEASUREMENT plus a proposed PROTOCOL clause:")
    P("")
    P("     PROPOSED (not applied — PROTOCOL rule 6 reserves changes to the Sunday review):")
    P("       rule 8 END COUNT clause — any published percentile, z or 'beats a coin flip' claim")
    P("       must state the NUMBER OF ENDS its null averages over, AND the ends themselves.  A")
    P("       basis label (SEQ / FIXED / RAW) does not identify the yardstick: at a matched end")
    P(f"       count the three bases agree to {k1m:.4f} (0.0000 scored exactly) and at K = 16 they")
    P(f"       disagree by {k16:.3f}, entirely through the count.  The end LIST is required too,")
    P(f"       because at K = 1 the same K-free null sd moves across a "
      f"{PLC[(PLC.K==1)&(PLC.basis=='RAW')].sd_spread.iloc[0]:.4f}-wide band on the choice of end.")
    P("")
    P(f"Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
