#!/usr/bin/env python3
"""Idea 1023 (cloud lane, 2026-09-16) — should a RULE-8 CHOOSER be scored on PICK STABILITY
rather than IS FIT?

QUESTION (QUEUE idea 1023, verbatim)
    idea 1013 found IS_SHARPE and IS_LEGS pick identically in all 6 cells while IS_CAGR takes 4
    distinct books over 16 ends, and that the two stable choosers land on lower-OOS-Sharpe
    books (1.162 vs 1.293 at E=REC on U56).  Price the trade directly: rank the three choosers
    by pick stability across the split-point band and by OOS Sharpe, and report whether
    stability costs return.  Max 2 params (chooser set, stability statistic).

WHAT IS NEW AGAINST 1013.  1013 measured pick stability as a DEFECT of the split-point fiat and
    stopped there.  It never asked whether the instability is what EARNS IS_CAGR its higher OOS
    Sharpe, or whether the two are merely co-located in one chooser.  Those have opposite
    implications: if instability pays, PROTOCOL should stop rewarding pick stability; if it does
    not, 1013's 1.162-vs-1.293 gap is about WHAT IS_CAGR picks and stabilising a chooser is free.
    1023 separates them with two controls 1013 did not carry:

      RANDOM   a chooser that picks uniformly at random from the same pool at every end.  It is
               MAXIMALLY unstable and reads no IS data at all.  If instability per se bought
               return, RANDOM would beat the record's three.  This is the decisive control.
      BANDMODE a STABILISED version of each raw chooser: at end E, run the raw chooser at E and
               the THREE PRECEDING quarter-ends and take the modal pick (ties -> the pick at E).
               It reads only data at or before E, so it is rule-8 legal, and it is the concrete
               thing PROTOCOL would adopt if it scored choosers on stability.  The trade is then
               priced directly: BANDMODE's OOS Sharpe minus its raw chooser's.

    The honest summary statistic for a chooser is its MEAN OOS result OVER the band, not its
    result at any one end -- reporting the best end is selection on the OOS window.  Every
    headline number below is a band mean with its declared-split value printed beside it.

WHAT IS MEASURED
    (A) THE STABILITY-RETURN TABLE.  Every chooser x panel x cost: three stability statistics
        and the mean / median / declared-split OOS Sharpe, CAGR and MaxDD of its picks.
    (B) THE TRADE.  Spearman rank correlation between stability and mean OOS Sharpe across the
        chooser set, in every panel x cost cell.
    (C) THE RANDOM CONTROL, MEASURED not asserted.  R = 400 independent chooser SEQUENCES per
        (panel, cost) -- each a uniform pool draw at every one of the 16 ends -- so RANDOM's
        NUNIQ, MODE_SHARE and OOS_BAND are sample means of the same statistics the deterministic
        choosers are scored on, and its return is the mean over sequences.
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's own split, with OOS CAGR/Sharpe/MaxDD against the
        live RULES v2 baseline and against SPY, and BOTH KEEP paths for every pick.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported, none selected.
    (1) CHOOSER SET in {REC3, STAB3, NULL1}
          REC3    the record's three: IS_SHARPE, IS_LEGS, IS_CAGR                  <- HEADLINE
          STAB3   their BANDMODE-stabilised twins (see above)
          NULL1   RANDOM, the uniform pool draw
          All three sets are scored at every point; the union is 7 choosers.
    (2) STABILITY STATISTIC in {NUNIQ, MODE_SHARE, OOS_BAND}
          NUNIQ       number of DISTINCT picks over the 16 ends (1013's own statistic)
          MODE_SHARE  share of the 16 ends taking the modal pick
          OOS_BAND    max - min of the pick's published OOS Sharpe over the 16 ends
          NUNIQ is the headline because it is the statistic 1013 published.

    NOT TUNED, reported as CONTROLS at every point:
      END GRID  1013's own END_Q: the 16 quarter-ends 2015-03-31 .. 2018-12-31.  PROTOCOL's own
                2016-12-31 ("REC") is a member and is the declared split everywhere.
      COST      0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL     U56 (binding) and B136 (labelled replication); each keeps its OWN calendar.
      POOL      the 36 never-memo-selected GRID ladder books.  The committed SHELF is NOT a
                legal rule-8 pool: it was selected on the full tape.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_REPRO   reproduce 1013 at E = REC on U56 at 10 bps: IS_SHARPE and IS_LEGS agree, IS_CAGR
              differs, and the two picks read 1.162 and 1.293 OOS Sharpe (tol 0.005).
    H_COST    HEADLINE.  Spearman(stability rank, mean OOS Sharpe) over REC3 in the headline
              cell is NEGATIVE, i.e. stability costs return.
              PASS => PROTOCOL cannot score choosers on stability for free.
              FAIL => stability is free (or pays) and the clause is cheap.
    H_RANDOM  RANDOM's mean OOS Sharpe does NOT exceed the best of REC3 in ANY of the 6
              panel x cost cells.  PASS => instability per se buys nothing.
    H_RAND2   the per-chooser version: RANDOM beats NONE of the 18 (cell, chooser) pairs.
              H_RANDOM asks about the BEST chooser; H_RAND2 asks about each, which is where a
              stable-vs-unstable split would show up.
    H_STAB    BANDMODE costs <= 0.05 of mean OOS Sharpe against its raw chooser in every cell.
    H_SIGN    sign(mean OOS Sharpe of IS_CAGR - IS_SHARPE) is the SAME in all 6 cells.
              PASS => 1013's ordering is a fact about the choosers, not about one cell.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                  0.0
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples
        (U56 11.99/1.162/-19.05 and 15.60/1.293/-15.59; B136 11.05/1.097/-19.50 and
        14.30/1.157/-17.31).
    G5  determinism: the whole end x book ladder rebuilt reproduces bit-for-bit.          0.0
    G6  IS PURITY: every chooser's pick is invariant under a permutation of the OOS returns.
    G7  BANDMODE LEGALITY: BANDMODE's pick at E depends only on rows with IS end <= E.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b count an UPPER bound.  The measured object is
    a DIFFERENCE between choosers reading the SAME pool over the SAME tape, and the bias is a
    common factor to every chooser.  Where it does not cancel it works against the RANDOM
    control: a uniform draw from a survivor panel is a BETTER book than a real-time one, so
    RANDOM's numbers are an UPPER bound and H_RANDOM is the HARDER call.  SPY is a real index
    series and is not inflated.

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
SLUG = "should-a-RULE-8-CHOOSER-be-scored-on-PICK-STABILITY-rather-than-IS-FIT"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
REC_END = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
RAW = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
STAB = [f"BM_{c}" for c in RAW]
RANDOM = "RANDOM"
SETS = {"REC3": RAW, "STAB3": STAB, "NULL1": [RANDOM]}
SET_HEAD = "REC3"
STATS = ["NUNIQ", "MODE_SHARE", "OOS_BAND"]
STAT_HEAD = "NUNIQ"
NBAND = 4          # BANDMODE looks at E and the 3 preceding quarter-ends
NRAND = 400
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
# 1013's four published declared-split picks (OOS CAGR, Sharpe, MaxDD)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
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


def spearman(x, y):
    """Rank correlation without scipy: Pearson of the average ranks."""
    x = pd.Series(np.asarray(x, float)).rank()
    y = pd.Series(np.asarray(y, float)).rank()
    if x.nunique() < 2 or y.nunique() < 2:
        return np.nan
    return float(np.corrcoef(x.values, y.values)[0, 1])


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_Q = quarter_ends("2015-01-01", "2018-12-31")            # 1013's own 16
END_PRE = quarter_ends("2014-03-01", "2014-12-31")          # BANDMODE's look-back only
ALLE = END_PRE + END_Q


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
    """IS-ONLY choosers.  sub is one (panel, cost, E) slice indexed by book."""
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


def main():
    t0 = time.time()
    P(f"# Idea 1023 (cloud lane, {DATE}) — should a RULE-8 CHOOSER be scored on PICK STABILITY "
      f"rather than IS FIT?")
    P(f"# 2 tuned dials: CHOOSER SET {list(SETS)} x STABILITY STATISTIC {STATS}.  All points "
      f"reported, none selected.")
    P(f"# CONTROLS at every point: END GRID = 1013's 16 quarter-ends {END_Q[0]}..{END_Q[-1]}, "
      f"COST {RUNGS} bps (head {RUNG_HEAD:.0f}), PANEL [U56, B136], POOL = GRID.")
    P(f"# Declared split = PROTOCOL's own {REC_END}.  Headline chooser statistic is the BAND "
      f"MEAN, not the value at any one end.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic.  The")
    P("#   measured object is a DIFFERENCE between choosers on the SAME pool; where the bias does")
    P("#   not cancel it flatters RANDOM, so H_RANDOM is the HARDER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    pool = C.grid_books(U, B)
    P(f"POOL = {len(pool)} never-memo-selected GRID books "
      f"({sum(b['panel']=='U56' for b in pool.values())} U56 / "
      f"{sum(b['panel']=='B136' for b in pool.values())} B136).")

    NET = {}
    for nm, b in pool.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    V2 = {}
    for p, px in PX.items():
        r, t = fast_run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for c in RUNGS:
            V2[(p, c)] = metblock((r - t * c / 1e4).loc[REC[p]:].values)

    # ================================================================ GATES
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    g1 = d_r < 1e-12 and d_t < 1e-10
    P(f"G1 fast_run == engine.backtest (returns / turnover): {d_r:.3e} / {d_t:.3e}  "
      f"{'PASS' if g1 else 'FAIL'}")
    gates.append(dict(gate="G1", what="fast runner == engine.backtest",
                      value=f"{d_r:.3e}/{d_t:.3e}", verdict="PASS" if g1 else "FAIL"))

    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    g2 = d2 == 0.0
    P(f"G2 rules_v2_weights(U,0.03,0.75) == baseline.rules_v2_weights(U): {d2:.3e}  "
      f"{'PASS' if g2 else 'FAIL'}")
    gates.append(dict(gate="G2", what="band book == live baseline", value=f"{d2:.3e}",
                      verdict="PASS" if g2 else "FAIL"))

    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    sb = SPYB[("U56", REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    g3 = d3 <= 5e-4
    P(f"G3 CROSS-RUN SPY OOS at {REC_END}: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.4%}  "
      f"max|d| {d3:.3e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple vs record", value=f"{d3:.3e}",
                      verdict="PASS" if g3 else "FAIL"))

    # ---------------------------------------------------------------- the ladder
    def build_ladder():
        rows = []
        for nm, b in pool.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    s = SPYB[(p, e)]
                    lg = legs_at(bk, s)
                    v2 = V2[(p, c)]
                    rows.append(dict(
                        book=nm, panel=p, cost=c, E=e,
                        **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                              "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                              "OOS_MaxDD")},
                        spy_OOS_Sharpe=s["OOS_Sharpe"], spy_OOS_CAGR=s["OOS_CAGR"],
                        **lg, pass4b=all(lg.values()),
                        pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                    and bk["MaxDD"] >= v2["MaxDD"])))
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    g5 = d5 == 0.0
    P(f"G5 determinism over the {len(L):,}-row ladder: {d5:.3e}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="ladder determinism", value=f"{d5:.3e}",
                      verdict="PASS" if g5 else "FAIL"))

    # G4 cross-run against 1013's four published picks
    bad4, rows4 = 0, []
    for (p, nm), trip13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - trip13[0]), abs(r.OOS_Sharpe - trip13[1]),
                abs(r.OOS_MaxDD - trip13[2]))
        ok = d <= 5e-4
        bad4 += 0 if ok else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=trip13[0], pub_Sharpe=trip13[1],
                          pub_MaxDD=trip13[2], maxd=d, verdict="PASS" if ok else "FAIL"))
    g4 = bad4 == 0
    P(f"G4 CROSS-RUN 1013's four published declared-split picks: {len(PUB_1013)-bad4}/"
      f"{len(PUB_1013)}  max|d| {max(r['maxd'] for r in rows4):.3e}  {'PASS' if g4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="1013 published picks", value=f"{len(PUB_1013)-bad4}/"
                      f"{len(PUB_1013)}", verdict="PASS" if g4 else "FAIL"))
    dump(pd.DataFrame(rows4), "crossrun")

    # ---------------------------------------------------------------- choosers
    SPYIS = {(p, e): fmet(SPYR[p].loc[:pd.Timestamp(e)].values) for p in PX for e in ALLE}
    IDX = {}
    for p in PX:
        for c in RUNGS:
            for e in ALLE:
                IDX[(p, c, e)] = L[(L.panel == p) & (L.cost == c) & (L.E == e)].set_index("book")

    def picks_raw(p, c):
        return {e: {ch: raw_pick(IDX[(p, c, e)], ch, SPYIS[(p, e)]) for ch in RAW} for e in ALLE}

    def picks_all(p, c, rng):
        pr = picks_raw(p, c)
        out = {}
        for e in END_Q:
            j = ALLE.index(e)
            look = ALLE[max(0, j - NBAND + 1): j + 1]
            d = dict(pr[e])
            for ch in RAW:
                seq = [pr[x][ch] for x in look]
                vc = pd.Series(seq).value_counts()
                top = vc.max()
                cand = [b for b in vc.index if vc[b] == top]
                d[f"BM_{ch}"] = pr[e][ch] if pr[e][ch] in cand else cand[0]
            d[RANDOM] = None
            out[e] = d
        return out, pr

    # G6 IS purity: permuting OOS returns cannot move any raw pick
    rng6 = np.random.default_rng(SEED0)
    base_pick = picks_raw("U56", RUNG_HEAD)
    NET_SAVE = {k: v for k, v in NET.items()}
    for nm, b in pool.items():
        if b["panel"] != "U56":
            continue
        s = NET[(nm, RUNG_HEAD)]
        o = s.loc[pd.Timestamp(END_Q[-1]) + pd.Timedelta(days=1):]
        perm = pd.Series(rng6.permutation(o.values), index=o.index)
        NET[(nm, RUNG_HEAD)] = pd.concat([s.loc[:pd.Timestamp(END_Q[-1])], perm])
    Lp = build_ladder()
    IDXp = {e: Lp[(Lp.panel == "U56") & (Lp.cost == RUNG_HEAD) & (Lp.E == e)].set_index("book")
            for e in ALLE}
    bad6 = 0
    for e in ALLE:
        for ch in RAW:
            if raw_pick(IDXp[e], ch, SPYIS[("U56", e)]) != base_pick[e][ch]:
                bad6 += 1
    NET.clear()
    NET.update(NET_SAVE)
    g6 = bad6 == 0
    P(f"G6 IS PURITY (picks invariant to an OOS permutation): {bad6} moved picks of "
      f"{len(ALLE)*len(RAW)}  {'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="IS purity", value=f"{bad6}/{len(ALLE)*len(RAW)}",
                      verdict="PASS" if g6 else "FAIL"))

    # ---------------------------------------------------------------- the chooser ladder
    rng = np.random.default_rng(SEED0 + 7)
    prows, rrows, bandmode_src = [], [], []
    for p in PX:
        books_p = sorted(b for b in pool if pool[b]["panel"] == p)
        for c in RUNGS:
            allp, pr = picks_all(p, c, rng)
            for e in END_Q:
                sub = IDX[(p, c, e)]
                for ch in SETS["REC3"] + SETS["STAB3"]:
                    bk = allp[e][ch]
                    r = sub.loc[bk]
                    prows.append(dict(
                        panel=p, cost=c, E=e, chooser=ch, pick=bk,
                        IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        spy_OOS_Sharpe=r.spy_OOS_Sharpe, spy_OOS_CAGR=r.spy_OOS_CAGR,
                        pass4b=bool(r.pass4b), pass4a=bool(r.pass4a)))
            # RANDOM, MEASURED not asserted: NRAND independent chooser SEQUENCES, each a
            # uniform pool draw at every one of the 16 ends.  Its stability statistics are the
            # mean over sequences; its return is the mean over sequences of the sequence mean.
            M = np.array([[IDX[(p, c, e)].loc[b, "OOS_Sharpe"] for b in books_p] for e in END_Q])
            MC = np.array([[IDX[(p, c, e)].loc[b, "OOS_CAGR"] for b in books_p] for e in END_Q])
            MD = np.array([[IDX[(p, c, e)].loc[b, "OOS_MaxDD"] for b in books_p] for e in END_Q])
            MB = np.array([[IDX[(p, c, e)].loc[b, "pass4b"] for b in books_p] for e in END_Q])
            MA = np.array([[IDX[(p, c, e)].loc[b, "pass4a"] for b in books_p] for e in END_Q])
            seq = rng.integers(0, len(books_p), (NRAND, len(END_Q)))
            er = np.arange(len(END_Q))
            sh = M[er[None, :], seq]
            nuq = np.array([len(np.unique(s)) for s in seq])
            msh = np.array([np.bincount(s, minlength=len(books_p)).max() for s in seq]) / len(END_Q)
            rrows.append(dict(
                panel=p, cost=c, n_seq=NRAND, pool=len(books_p),
                NUNIQ=nuq.mean(), NUNIQ_sd=nuq.std(ddof=1),
                MODE_SHARE=msh.mean(), OOS_BAND=(sh.max(axis=1) - sh.min(axis=1)).mean(),
                mean_OOS_Sharpe=sh.mean(), sd_over_seq=sh.mean(axis=1).std(ddof=1),
                mean_OOS_CAGR=MC[er[None, :], seq].mean(),
                mean_OOS_MaxDD=MD[er[None, :], seq].mean(),
                rate4b=MB[er[None, :], seq].mean(), rate4a=MA[er[None, :], seq].mean(),
                dec_OOS_Sharpe=M[END_Q.index(REC_END)].mean(),
                dec_OOS_CAGR=MC[END_Q.index(REC_END)].mean(),
                dec_OOS_MaxDD=MD[END_Q.index(REC_END)].mean()))
            for e in ALLE:
                for ch in RAW:
                    bandmode_src.append(dict(panel=p, cost=c, E=e, chooser=ch, pick=pr[e][ch]))
    PKS = pd.DataFrame(prows)
    RND = pd.DataFrame(rrows)
    dump(PKS, "picks")
    dump(RND, "random")
    dump(pd.DataFrame(bandmode_src), "rawpicks")

    # G7 BANDMODE legality — its pick at E is a function of raw picks at ends <= E only
    bad7 = 0
    for p in PX:
        for c in RUNGS:
            src = {(r.E, r.chooser): r.pick for r in
                   pd.DataFrame(bandmode_src).query("panel==@p and cost==@c").itertuples()}
            for e in END_Q:
                j = ALLE.index(e)
                look = ALLE[max(0, j - NBAND + 1): j + 1]
                for ch in RAW:
                    seq = [src[(x, ch)] for x in look]
                    vc = pd.Series(seq).value_counts()
                    cand = [b for b in vc.index if vc[b] == vc.max()]
                    want = src[(e, ch)] if src[(e, ch)] in cand else cand[0]
                    got = PKS[(PKS.panel == p) & (PKS.cost == c) & (PKS.E == e)
                              & (PKS.chooser == f"BM_{ch}")].iloc[0]["pick"]
                    if want != got:
                        bad7 += 1
    g7 = bad7 == 0
    P(f"G7 BANDMODE legality (pick at E uses only ends <= E): {bad7} disagreeing cells  "
      f"{'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="BANDMODE legality", value=f"{bad7} cells",
                      verdict="PASS" if g7 else "FAIL"))
    dump(pd.DataFrame(gates), "gates")

    # ================================================================ (A) the table
    P("")
    P("## (A) THE STABILITY-RETURN TABLE — 3 stability statistics x mean/median/declared OOS")
    P(f"   band = the {len(END_Q)} quarter-ends {END_Q[0]}..{END_Q[-1]};  declared = {REC_END}")
    P("")
    rows = []
    for p in PX:
        for c in RUNGS:
            for ch in SETS["REC3"] + SETS["STAB3"]:
                g = PKS[(PKS.panel == p) & (PKS.cost == c) & (PKS.chooser == ch)]
                picks = g.set_index("E")["pick"]
                dec = g[g.E == REC_END].iloc[0]
                rows.append(dict(
                    panel=p, cost=c, chooser=ch,
                    set=("STAB3" if ch.startswith("BM_") else "REC3"),
                    NUNIQ=float(picks.nunique()),
                    MODE_SHARE=float(picks.value_counts().max() / len(picks)),
                    OOS_BAND=float(g.OOS_Sharpe.max() - g.OOS_Sharpe.min()),
                    mean_OOS_Sharpe=g.OOS_Sharpe.mean(), med_OOS_Sharpe=g.OOS_Sharpe.median(),
                    mean_OOS_CAGR=g.OOS_CAGR.mean(), mean_OOS_MaxDD=g.OOS_MaxDD.mean(),
                    dec_pick=dec["pick"], dec_OOS_Sharpe=dec.OOS_Sharpe,
                    dec_OOS_CAGR=dec.OOS_CAGR, dec_OOS_MaxDD=dec.OOS_MaxDD,
                    rate4b=g.pass4b.mean(), rate4a=g.pass4a.mean()))
            rr = RND[(RND.panel == p) & (RND.cost == c)].iloc[0]
            rows.append(dict(
                panel=p, cost=c, chooser=RANDOM, set="NULL1",
                NUNIQ=rr.NUNIQ, MODE_SHARE=rr.MODE_SHARE, OOS_BAND=rr.OOS_BAND,
                mean_OOS_Sharpe=rr.mean_OOS_Sharpe, med_OOS_Sharpe=rr.mean_OOS_Sharpe,
                mean_OOS_CAGR=rr.mean_OOS_CAGR, mean_OOS_MaxDD=rr.mean_OOS_MaxDD,
                dec_pick=f"(uniform draw, {rr.pool} books)", dec_OOS_Sharpe=rr.dec_OOS_Sharpe,
                dec_OOS_CAGR=rr.dec_OOS_CAGR, dec_OOS_MaxDD=rr.dec_OOS_MaxDD,
                rate4b=rr.rate4b, rate4a=rr.rate4a))
    T = pd.DataFrame(rows)
    dump(T, "stability")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':12s} | {'NUNIQ':>5s} {'MODEsh':>6s} {'OOSband':>7s} "
      f"| {'meanSh':>7s} {'medSh':>7s} {'decSh':>7s} {'meanCAGR':>8s} {'meanDD':>8s} "
      f"| {'4b':>5s} {'4a':>5s}  declared pick")
    for _, r in T.iterrows():
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:12s} | {r.NUNIQ:5.0f} {r.MODE_SHARE:6.3f} "
          f"{r.OOS_BAND:7.4f} | {r.mean_OOS_Sharpe:7.4f} {r.med_OOS_Sharpe:7.4f} "
          f"{r.dec_OOS_Sharpe:7.4f} {r.mean_OOS_CAGR:8.2%} {r.mean_OOS_MaxDD:8.2%} | "
          f"{r.rate4b:5.3f} {r.rate4a:5.3f}  {r.dec_pick}")

    for p in PX:
        s = SPYB[(p, REC_END)]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p} at the declared split: SPY OOS {s['OOS_CAGR']:.2%} / "
          f"{s['OOS_Sharpe']:.3f} / {s['OOS_MaxDD']:.2%};  RULES v2 (live, {RUNG_HEAD:.0f} bps) "
          f"full {v2['CAGR']:.2%} / {v2['Sharpe']:.3f} / {v2['MaxDD']:.2%} "
          f"(H1 {v2['H1']:.3f} / H2 {v2['H2']:.3f})")
        sh = [SPYB[(p, e)]["OOS_Sharpe"] for e in END_Q]
        P(f"   SPY's own OOS Sharpe over the band: {min(sh):.4f}..{max(sh):.4f} "
          f"(mean {np.mean(sh):.4f})")

    # ================================================================ (B) the trade
    P("")
    P("## (B) THE TRADE — Spearman(stability rank, mean OOS Sharpe), by chooser set and statistic")
    P("   stability rank: MORE stable = lower NUNIQ / higher MODE_SHARE / lower OOS_BAND.")
    tr = []
    for sname, chs in SETS.items():
        if len(chs) < 3:
            continue
        for stat in STATS:
            for p in PX:
                for c in RUNGS:
                    g = T[(T.panel == p) & (T.cost == c) & (T.chooser.isin(chs))]
                    x = g[stat].values.astype(float)
                    if stat == "MODE_SHARE":
                        x = -x            # so that higher x = LESS stable, uniformly
                    y = g.mean_OOS_Sharpe.values.astype(float)
                    rho = spearman(x, y)
                    tr.append(dict(chooser_set=sname, stat=stat, panel=p, cost=c,
                                   spearman_instability_vs_OOS=rho, n=len(g)))
    TR = pd.DataFrame(tr)
    dump(TR, "trade")
    P(f"{'set':6s} {'stat':11s} {'panel':6s} {'cost':>4s}  rho(INSTABILITY, mean OOS Sharpe)")
    for _, r in TR.iterrows():
        P(f"{r.chooser_set:6s} {r.stat:11s} {r.panel:6s} {r.cost:4.0f}  "
          f"{r.spearman_instability_vs_OOS:+.4f}" if not np.isnan(
              r.spearman_instability_vs_OOS) else
          f"{r.chooser_set:6s} {r.stat:11s} {r.panel:6s} {r.cost:4.0f}  n/a (no variance)")

    # is the TRADE even sign-stable across the three definitions of stability?
    P("")
    P("   SIGN AGREEMENT of the trade across the three stability statistics, per cell:")
    agree = []
    for sname in ("REC3", "STAB3"):
        for p in PX:
            for c in RUNGS:
                v = TR[(TR.chooser_set == sname) & (TR.panel == p) & (TR.cost == c)]
                sg = [int(np.sign(x)) for x in v.spearman_instability_vs_OOS if not np.isnan(x)]
                agree.append(dict(chooser_set=sname, panel=p, cost=c, n_defined=len(sg),
                                  signs="/".join(f"{s:+d}" for s in sg),
                                  unanimous=(len(set(s for s in sg if s != 0)) <= 1)))
    AG = pd.DataFrame(agree)
    dump(AG, "signagreement")
    for _, r in AG.iterrows():
        P(f"     {r.chooser_set:6s} {r.panel:6s} {r.cost:4.0f}bps  signs [{r.signs}]  "
          f"unanimous {r.unanimous}")
    P(f"   the three stability statistics agree on the SIGN of the trade in "
      f"{int(AG.unanimous.sum())} of {len(AG)} cells.")

    # ================================================================ HYPOTHESES
    P("")
    hyp = []
    HD = T[(T.panel == "U56") & (T.cost == RUNG_HEAD)].set_index("chooser")

    # H_REPRO
    same = HD.loc["IS_SHARPE", "dec_pick"] == HD.loc["IS_LEGS", "dec_pick"]
    diff = HD.loc["IS_CAGR", "dec_pick"] != HD.loc["IS_SHARPE", "dec_pick"]
    d_a = abs(HD.loc["IS_SHARPE", "dec_OOS_Sharpe"] - 1.162)
    d_b = abs(HD.loc["IS_CAGR", "dec_OOS_Sharpe"] - 1.293)
    h = same and diff and d_a <= 5e-3 and d_b <= 5e-3
    P(f"H_REPRO  bar: 1013's U56/10bps declared-split reading reproduces.  IS_SHARPE==IS_LEGS "
      f"{same}, IS_CAGR differs {diff}, OOS Sharpe {HD.loc['IS_SHARPE','dec_OOS_Sharpe']:.4f} "
      f"(|d| {d_a:.1e}) and {HD.loc['IS_CAGR','dec_OOS_Sharpe']:.4f} (|d| {d_b:.1e})  "
      f"-> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_REPRO", bar="1013 declared-split reading",
                    value=f"{d_a:.1e}/{d_b:.1e}", verdict="PASS" if h else "FAIL"))

    # H_COST (headline)
    rho_h = TR[(TR.chooser_set == SET_HEAD) & (TR.stat == STAT_HEAD) & (TR.panel == "U56")
               & (TR.cost == RUNG_HEAD)].iloc[0].spearman_instability_vs_OOS
    h = (not np.isnan(rho_h)) and rho_h > 0
    P(f"H_COST   HEADLINE bar: rho(INSTABILITY, mean OOS Sharpe) over {SET_HEAD} with "
      f"{STAT_HEAD} at U56/{RUNG_HEAD:.0f}bps is POSITIVE (i.e. stability COSTS return).  "
      f"rho = {rho_h:+.4f}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_COST", bar="rho > 0 (stability costs return)",
                    value=f"{rho_h:+.4f}", verdict="PASS" if h else "FAIL"))

    # H_RANDOM
    bad, worst = 0, None
    for p in PX:
        for c in RUNGS:
            g = T[(T.panel == p) & (T.cost == c)].set_index("chooser")
            best = g.loc[RAW, "mean_OOS_Sharpe"].max()
            rd = g.loc[RANDOM, "mean_OOS_Sharpe"]
            if rd > best:
                bad += 1
            if worst is None or (rd - best) > worst[0]:
                worst = (rd - best, p, c, rd, best)
    h = bad == 0
    P(f"H_RANDOM bar: RANDOM's mean OOS Sharpe never exceeds the best of REC3 in any of 6 "
      f"cells.  violations {bad}/6; worst margin {worst[0]:+.4f} at {worst[1]}/{worst[2]:.0f}bps "
      f"(RANDOM {worst[3]:.4f} vs best REC3 {worst[4]:.4f})  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_RANDOM", bar="RANDOM never beats best REC3", value=f"{bad}/6",
                    verdict="PASS" if h else "FAIL"))

    # H_RAND2 — the per-chooser version.  H_RANDOM asks whether a coin flip beats the BEST of
    # the record's three; H_RAND2 asks how many of the 18 (cell, chooser) pairs it beats, which
    # is where the stable-vs-unstable split shows up.
    r2, beat = [], 0
    for p in PX:
        for c in RUNGS:
            g = T[(T.panel == p) & (T.cost == c)].set_index("chooser")
            rd = g.loc[RANDOM, "mean_OOS_Sharpe"]
            for ch in RAW:
                d = rd - g.loc[ch, "mean_OOS_Sharpe"]
                beat += int(d > 0)
                r2.append(dict(panel=p, cost=c, chooser=ch,
                               chooser_Sharpe=g.loc[ch, "mean_OOS_Sharpe"], RANDOM_Sharpe=rd,
                               RANDOM_minus_chooser=d,
                               chooser_4b=g.loc[ch, "rate4b"], RANDOM_4b=g.loc[RANDOM, "rate4b"],
                               d_4b=g.loc[ch, "rate4b"] - g.loc[RANDOM, "rate4b"]))
    R2 = pd.DataFrame(r2)
    dump(R2, "randomduel")
    h = beat == 0
    P(f"H_RAND2  bar: RANDOM beats NO individual chooser in any of the 18 (cell, chooser) pairs."
      f"  RANDOM wins {beat}/18  -> {'PASS' if h else 'FAIL'}")
    for ch in RAW:
        s = R2[R2.chooser == ch]
        P(f"     {ch:10s} RANDOM wins {int((s.RANDOM_minus_chooser > 0).sum())}/6, mean margin "
          f"{s.RANDOM_minus_chooser.mean():+.4f};  4b rate {s.chooser_4b.mean():.3f} vs RANDOM "
          f"{s.RANDOM_4b.mean():.3f} (gap {s.d_4b.mean():+.3f})")
    hyp.append(dict(hyp="H_RAND2", bar="RANDOM beats 0 of 18 (cell, chooser) pairs",
                    value=f"{beat}/18", verdict="PASS" if h else "FAIL"))

    # H_STAB
    deltas = []
    for p in PX:
        for c in RUNGS:
            g = T[(T.panel == p) & (T.cost == c)].set_index("chooser")
            for ch in RAW:
                deltas.append(dict(panel=p, cost=c, chooser=ch,
                                   raw=g.loc[ch, "mean_OOS_Sharpe"],
                                   bandmode=g.loc[f"BM_{ch}", "mean_OOS_Sharpe"],
                                   delta=g.loc[f"BM_{ch}", "mean_OOS_Sharpe"]
                                   - g.loc[ch, "mean_OOS_Sharpe"],
                                   d_NUNIQ=g.loc[f"BM_{ch}", "NUNIQ"] - g.loc[ch, "NUNIQ"]))
    D = pd.DataFrame(deltas)
    dump(D, "bandmode")
    worst_d = float(D.delta.min())
    h = worst_d >= -0.05
    P(f"H_STAB   bar: BANDMODE costs <= 0.05 mean OOS Sharpe against its raw chooser in every "
      f"cell.  worst delta {worst_d:+.4f} "
      f"({D.loc[D.delta.idxmin(),'panel']}/{D.loc[D.delta.idxmin(),'cost']:.0f}bps/"
      f"{D.loc[D.delta.idxmin(),'chooser']})  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_STAB", bar="BANDMODE delta >= -0.05", value=f"{worst_d:+.4f}",
                    verdict="PASS" if h else "FAIL"))
    P(f"   BANDMODE stabilisation, all 6 cells x 3 choosers: mean delta {D.delta.mean():+.4f}, "
      f"mean d_NUNIQ {D.d_NUNIQ.mean():+.2f}, cells where BANDMODE is strictly more stable "
      f"{int((D.d_NUNIQ < 0).sum())}/{len(D)}")

    # H_SIGN
    signs = []
    for p in PX:
        for c in RUNGS:
            g = T[(T.panel == p) & (T.cost == c)].set_index("chooser")
            signs.append(int(np.sign(g.loc["IS_CAGR", "mean_OOS_Sharpe"]
                                     - g.loc["IS_SHARPE", "mean_OOS_Sharpe"])))
    h = len(set(signs)) == 1
    P(f"H_SIGN   bar: sign(IS_CAGR - IS_SHARPE mean OOS Sharpe) identical in all 6 cells.  "
      f"signs {signs}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_SIGN", bar="same sign in 6/6 cells", value=str(signs),
                    verdict="PASS" if h else "FAIL"))

    dump(pd.DataFrame(hyp), "hypotheses")

    # ================================================================ (D) rule 8 / KEEP paths
    P("")
    P(f"## (D) RULE 8 at the declared split {REC_END} — picks made on "
      f"[{REC['U56'].date()}, {REC_END}] alone, 2017-2026 read once")
    wf = PKS[PKS.E == REC_END].copy()
    for p in PX:
        v2 = V2[(p, RUNG_HEAD)]
        wf.loc[wf.panel == p, "base_Sharpe"] = v2["Sharpe"]
        wf.loc[wf.panel == p, "base_MaxDD"] = v2["MaxDD"]
    dump(wf, "walkforward")
    P(f"{'panel':6s} {'cost':>4s} {'chooser':12s} {'pick':30s} {'OOS CAGR':>9s} {'Sh':>7s} "
      f"{'MaxDD':>8s} | {'4b':>5s} {'4a':>5s}")
    for _, r in wf.iterrows():
        P(f"{r.panel:6s} {r.cost:4.0f} {r.chooser:12s} {str(r['pick']):30s} {r.OOS_CAGR:9.2%} "
          f"{r.OOS_Sharpe:7.3f} {r.OOS_MaxDD:8.2%} | {str(r.pass4b):>5s} {str(r.pass4a):>5s}")
    n4b = int(wf.pass4b.sum())
    n4a = int(wf.pass4a.sum())
    P(f"   OOS 4b {n4b} of {len(wf)};  OOS 4a {n4a} of {len(wf)} (deterministic choosers).")
    for p in PX:
        for c in RUNGS:
            rr = RND[(RND.panel == p) & (RND.cost == c)].iloc[0]
            P(f"   RANDOM {p}/{c:.0f}bps at the declared split: OOS {rr.dec_OOS_CAGR:.2%} / "
              f"{rr.dec_OOS_Sharpe:.3f} / {rr.dec_OOS_MaxDD:.2%};  band 4b rate {rr.rate4b:.3f}, "
              f"4a rate {rr.rate4a:.3f}")
    P(f"   Over the whole {len(PKS)}-row band x chooser grid: 4b {PKS.pass4b.mean():.4f}, "
      f"4a {PKS.pass4a.mean():.4f}.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
