#!/usr/bin/env python3
"""Idea 1018 (cloud lane, 2026-09-16) — is `L3_OOS` the leg 4b could ACTUALLY DROP?

QUESTION (QUEUE idea 1018, verbatim)
    idea 1014 found `L3_OOS` is the record's least pivotal leg in EVERY claim-set x
    binding-definition cell (sole binder 0.00013 record-wide, 0.00000 on fresh prices), well
    below `L2_H2`'s 0.00292.  Price the 4b-minus-OOS conjunction against its own null: how much
    does the PASS population widen, and does any committed FAIL become a rule-8 pass.
    Max 2 params (claim set, binding definition).

WHAT IS NEW AGAINST 1014.  1014 counted how often `L3_OOS` DECIDES a FAIL inside the record's
    own committed rows.  That is a census of a population that has ALREADY been filtered by the
    other four legs, and a leg can be rarely-sole-binding there while still being the only
    thing holding a COIN FLIP out.  1018 asks the question the census cannot: drop the leg and
    price the resulting 4-leg conjunction (`4b'`) against each book's OWN gross-matched null.
    The deliverable is not a pivotality rate — it is the DISCRIMINATION the record would lose:

        DISC(criterion) = (real pass rate) - (gross-matched null pass rate)

    If DISC(4b') ~ DISC(4b), the leg is free and the record should drop it.  If DISC(4b')
    collapses, `L3_OOS` is exactly the leg that separates a book from a coin flip, and its low
    sole-binding rate is a SELECTION ARTEFACT of the population 1014 censused.

WHAT IS MEASURED
    (A) THE WIDENING.  Every book in every claim set, at every cost rung, under 4b and 4b':
        the five legs, both verdicts, the binding-leg set, and which FAIL rows flip.
    (B) THE NULL PRICE (headline).  For every book, D = 100 gross-matched ROT draws (926's
        convention: at each rebalance date hold a RANDOM subset of the same SIZE at the same
        GROSS from the names priced that day).  Null 4b and 4b' pass rates, and DISC for both.
    (C) THE RULE-8 WALK-FORWARD.  IS-only choosers pick from the never-memo-selected GRID pool
        on 2009..2016-12-31 ALONE; 2017-2026 read once, under 4b and under 4b'.  Reports
        whether any committed 4b FAIL becomes a rule-8 pass once the leg is dropped, with OOS
        CAGR/Sharpe/MaxDD against the live RULES v2 baseline and against SPY.
    (D) BOTH KEEP PATHS (4a and 4b) evaluated at every grid point.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported, none
selected.
    (1) CLAIM SET in {REC, GRID, SHELF}
          REC    SHELF + GRID, 45 books                                  <- HEADLINE
          GRID   the 36 never-memo-selected mechanical ladder books      (clean pool, rule 8)
          SHELF  the 9 committed memo-backed 4b passes                   (1014's own subject)
    (2) BINDING DEFINITION in {SOLE, ANY}
          SOLE   `L3_OOS` is the ONLY failing leg  -> the row FLIPS when the leg is dropped
          ANY    `L3_OOS` is among the failing legs -> the row is TOUCHED but need not flip
          Both are 1014's own two definitions and both are reported everywhere.

    NOT TUNED, reported as CONTROLS at every point:
      COST    0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL   U56 (binding) and B136 (labelled replication).  Each keeps its OWN calendar.
      SPLIT   PROTOCOL rule 8's own 2016-12-31, unmoved (idea 1013 priced moving it).
      BAR     the record's own REC_FULL convention: `L4_DD`/`L5_CAGR` read against SPY's
              FULL-sample MaxDD/CAGR, as every committed row in this record used.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_BIND    reproduce 1014: `L3_OOS` is SOLE binder on < 0.01 of FAIL rows in every cell.
    H_WIDEN   dropping `L3_OOS` widens the REAL pass population by <= 0.10 of the claim set.
              PASS => the leg is nearly inert on real books, as 1014 found.
    H_NULL    HEADLINE.  dropping the leg widens the NULL population by no more than it widens
              the REAL one: d_null <= d_real in the headline cell.
              PASS => the leg is free and 4b could actually drop it.
              FAIL => the leg is what holds the coin flip out; 1014's rate is an artefact.
    H_DISC    the real-minus-null GAP shrinks by <= 0.05 when the leg is dropped.
    H_DEPTH   on NO population -- real books or null draws -- does `L3_OOS` ever fail at CO-FAIL
              DEPTH 1 (i.e. alone).  "Never sole" is a weak statement if the leg is one
              co-binder from deciding; the DEPTH distribution says how far from sole it is.
    H_RULE8   no rule-8 PICK changes when the criterion drops `L3_OOS`, and no committed 4b
              FAIL becomes a rule-8 pass under 4b'.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                  0.0
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72% (idea 1009 G4 / idea 1013 G3).
    G4  every SHELF book reproduces its committed memo triple (CAGR, Sharpe, MaxDD).
    G5  GROSS MATCH: every null draw's realised gross == its book's, and holding COUNT matches.
    G6  determinism: the real ladder rebuilt reproduces bit-for-bit.                     0.0
    G7  LEG IDENTITY: the five legs recomputed independently from metric dicts.     0 rows

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic and every 4b/4b' pass count an UPPER bound.  The measured
    object is a DIFFERENCE between a book and a coin flip drawn from the SAME panel on the SAME
    tape at the SAME gross.  A coin flip drawn from a survivor panel is a BETTER book than one
    drawn in real time, so every NULL pass rate here is an UPPER bound and every DISC a LOWER
    bound -- which cuts AGAINST this run's own H_NULL, i.e. the hypothesis that the leg is free
    is the EASIER one to pass.  SPY is a real index series and is not inflated.

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
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import rebalance_mask, backtest  # noqa: E402

DATE = "2026-09-16"
SLUG = "is-L3_OOS-the-leg-4b-could-ACTUALLY-DROP"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP, MAX_VOL = 260, 0.60
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
SPLIT = "2016-12-31"
DDCAP_FRAC, CAGRFLOOR_FRAC = 0.60, 0.70
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]
DROP = "L3_OOS"
LEGS4 = [k for k in LEGS if k != DROP]
CLAIM_SETS = ["REC", "GRID", "SHELF"]
CLAIM_HEAD = "REC"
BINDDEFS = ["SOLE", "ANY"]
CHOOSERS = ["IS_SHARPE", "IS_LEGS", "IS_CAGR"]
NDRAW = 100
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def load_lane_c():
    spec = importlib.util.spec_from_file_location("laneC1018", LANEC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = load_lane_c()
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def metblock(r):
    c, s, d = fmet(r)
    k = len(r) // 2
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:k]), H2=fsharpe(r[k:]))


def path_block(net, e=SPLIT):
    b = metblock(net.values)
    o = net.loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
    i = net.loc[:pd.Timestamp(e)].values
    oc, os_, od = fmet(o)
    ic, is_, idd = fmet(i)
    b.update(OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od, OOS_n=len(o),
             IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd, IS_n=len(i))
    return b


def legs_at(bk, sb):
    """PROTOCOL 4b's five legs in the record's own REC_FULL bar convention."""
    return {
        "L1_H1": bool(bk["H1"] > sb["H1"]),
        "L2_H2": bool(bk["H2"] > sb["H2"]),
        "L3_OOS": bool(bk["OOS_Sharpe"] > sb["OOS_Sharpe"]),
        "L4_DD": bool(abs(bk["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"])),
        "L5_CAGR": bool(bk["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]),
    }


def failstr(lg, keys=LEGS):
    f = [k for k in keys if not lg[k]]
    return "+".join(f) if f else "-"


# ---------------------------------------------------------------- the gross-matched null
def rot_null_weights(px, W, mask, rng):
    """926's ROT: at every rebalance date hold a RANDOM subset of the SAME SIZE at the SAME
    GROSS, drawn from the names PRICED that day.  Gross and holding count match by
    construction; nothing else about the book is preserved."""
    idx = px.index
    Wv = W.reindex(idx).fillna(0.0).values
    avail = px.notna().values
    reb = np.flatnonzero(mask.values)
    sub = Wv[reb]
    k = (sub != 0).sum(axis=1)
    g = sub.sum(axis=1)
    av = avail[reb]
    navail = av.sum(axis=1)
    k = np.minimum(k, navail)
    R = rng.random(sub.shape)
    R = np.where(av, R, np.inf)
    rank = np.argsort(np.argsort(R, axis=1), axis=1)
    sel = rank < k[:, None]
    out = np.zeros_like(Wv)
    per = np.where(k > 0, g / np.maximum(k, 1), 0.0)
    out[reb] = sel * per[:, None]
    # REALISED gross and holding count of the drawn book, measured off the built matrix
    return (pd.DataFrame(out, index=idx, columns=px.columns),
            (out[reb] != 0).sum(axis=1), out[reb].sum(axis=1))


def main():
    t0 = time.time()
    P(f"# Idea 1018 (cloud lane, {DATE}) — is `L3_OOS` the leg 4b could ACTUALLY DROP?")
    P(f"# 2 tuned dials: CLAIM SET {CLAIM_SETS} x BINDING DEFINITION {BINDDEFS}.  All points "
      f"reported, none selected.")
    P(f"# CONTROLS at every point: COST {RUNGS} bps (head {RUNG_HEAD:.0f}), PANEL [U56, B136], "
      f"SPLIT {SPLIT} (PROTOCOL rule 8's own), BAR REC_FULL (the record's own).")
    P(f"# NULL: {NDRAW} gross-matched ROT draws per book, seed {SEED0}.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels — every LEVEL is optimistic; the")
    P("#   null is drawn from the SAME survivor panel, so every null pass rate is an UPPER bound")
    P("#   and every DISC a LOWER bound, i.e. H_NULL is the EASIER call.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")
    P(f"Post-warm-up start: U56 {REC['U56'].date()}, B136 {REC['B136'].date()}.")

    shelf = C.shelf_books(U, B)
    s0, ab0, v0 = score(U, vol_scale=False)
    rk = s0.where(ab0 & (v0 < MAX_VOL)).rank(axis=1, ascending=False)
    shelf["u56-top20-g065-M"] = dict(
        panel="U56", freq="M", W=(rk <= 20).astype(float) * 0.65 / 20,
        memo=(0.1269, 1.201, -0.1711), src="2026-09-15_u56-top20-g065_4b_B_MEMO.md")
    grid = C.grid_books(U, B)
    BOOKS = {}
    for nm, b in shelf.items():
        BOOKS[nm] = dict(b, set="SHELF")
    for nm, b in grid.items():
        BOOKS[nm] = dict(b, set="GRID")
    MEMBER = {"REC": list(BOOKS), "GRID": [n for n in BOOKS if BOOKS[n]["set"] == "GRID"],
              "SHELF": [n for n in BOOKS if BOOKS[n]["set"] == "SHELF"]}
    P(f"SHELF = {len(shelf)} committed memo-backed 4b passes; GRID = {len(grid)} "
      f"never-memo-selected ladder books; REC = {len(BOOKS)}.")
    P("")

    # ---------------------------------------------------------------- real paths
    NET, TURN = {}, {}
    for nm, b in BOOKS.items():
        px = PX[b["panel"]]
        r, t = fast_run(px, b["W"], rebalance_mask(px.index, b["freq"]))
        st = REC[b["panel"]]
        for c in RUNGS:
            NET[(nm, c)] = (r - t * c / 1e4).loc[st:]
        TURN[nm] = float(t.loc[st:].sum() / (len(t.loc[st:]) / 252.0))
    SPYR = {p: PX[p]["SPY"].pct_change().fillna(0.0).loc[REC[p]:] for p in PX}
    SPYB = {p: path_block(SPYR[p]) for p in PX}
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

    trip = (SPYB["U56"]["OOS_CAGR"], SPYB["U56"]["OOS_Sharpe"], SPYB["U56"]["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    g3 = d3 <= 5e-4
    P(f"G3 CROSS-RUN SPY OOS at {SPLIT}: {trip[0]:.4%} / {trip[1]:.4f} / {trip[2]:.4%} vs "
      f"committed {SPY_OOS_COMMITTED[0]:.2%} / {SPY_OOS_COMMITTED[1]:.4f} / "
      f"{SPY_OOS_COMMITTED[2]:.2%}  max|d| {d3:.3e}  {'PASS' if g3 else 'FAIL'}")
    gates.append(dict(gate="G3", what="SPY OOS triple vs record", value=f"{d3:.3e}",
                      verdict="PASS" if g3 else "FAIL"))

    grows, ok4 = [], True
    for nm in MEMBER["SHELF"]:
        b = BOOKS[nm]
        c, s, d = fmet(NET[(nm, RUNG_HEAD)].values)
        m = b["memo"]
        dc = abs(c - m[0]) if m[0] is not None else 0.0
        ds = abs(s - m[1]) if m[1] is not None else 0.0
        dv = abs(d - m[2]) if m[2] is not None else 0.0
        good = dc <= 0.015 and ds <= 0.030 and dv <= 0.015
        ok4 &= good
        grows.append(dict(book=nm, panel=b["panel"], CAGR=c, Sharpe=s, MaxDD=d,
                          memo_CAGR=m[0], memo_Sharpe=m[1], memo_MaxDD=m[2],
                          d_CAGR=dc, d_Sharpe=ds, d_MaxDD=dv,
                          verdict="PASS" if good else "FAIL", src=b["src"]))
    P(f"G4 SHELF memo triples: {sum(r['verdict'] == 'PASS' for r in grows)}/{len(grows)}  "
      f"{'PASS' if ok4 else 'FAIL'}")
    gates.append(dict(gate="G4", what="SHELF memo triples",
                      value=f"{sum(r['verdict']=='PASS' for r in grows)}/{len(grows)}",
                      verdict="PASS" if ok4 else "FAIL"))
    dump(pd.DataFrame(grows), "shelf")

    # ---------------------------------------------------------------- the REAL ladder
    def build_real():
        rows = []
        for nm, b in BOOKS.items():
            p = b["panel"]
            sb = SPYB[p]
            for c in RUNGS:
                bk = path_block(NET[(nm, c)])
                lg = legs_at(bk, sb)
                v2 = V2[(p, c)]
                rows.append(dict(
                    book=nm, set=b["set"], panel=p, freq=b["freq"], cost=c,
                    **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
                                          "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe",
                                          "OOS_MaxDD")},
                    **lg,
                    pass4b=all(lg.values()),
                    pass4bp=all(lg[k] for k in LEGS4),
                    fail4b=failstr(lg), fail4bp=failstr(lg, LEGS4),
                    L3_sole=(failstr(lg) == DROP),
                    L3_any=(not lg[DROP]),
                    pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                and bk["MaxDD"] >= v2["MaxDD"]),
                    turnover=TURN[nm]))
        return pd.DataFrame(rows)

    R = build_real()
    R2 = build_real()
    num = R.select_dtypes(include=[float, int]).columns
    d6 = float(np.nanmax(np.abs(R[num].values - R2[num].values)))
    g6 = d6 == 0.0
    P(f"G6 determinism over the {len(R):,}-row real ladder: {d6:.3e}  {'PASS' if g6 else 'FAIL'}")
    gates.append(dict(gate="G6", what="real ladder determinism", value=f"{d6:.3e}",
                      verdict="PASS" if g6 else "FAIL"))

    bad7 = 0
    for _, r in R.iterrows():
        sb = SPYB[r["panel"]]
        lg = {"L1_H1": r["H1"] > sb["H1"], "L2_H2": r["H2"] > sb["H2"],
              "L3_OOS": r["OOS_Sharpe"] > sb["OOS_Sharpe"],
              "L4_DD": abs(r["OOS_MaxDD"]) <= DDCAP_FRAC * abs(sb["MaxDD"]),
              "L5_CAGR": r["OOS_CAGR"] >= CAGRFLOOR_FRAC * sb["CAGR"]}
        if any(bool(lg[k]) != bool(r[k]) for k in LEGS):
            bad7 += 1
    g7 = bad7 == 0
    P(f"G7 leg identity (independent recomputation): {bad7} disagreeing rows  "
      f"{'PASS' if g7 else 'FAIL'}")
    gates.append(dict(gate="G7", what="leg identity", value=f"{bad7} rows",
                      verdict="PASS" if g7 else "FAIL"))
    dump(R, "real")

    # ---------------------------------------------------------------- the NULL
    P("")
    P(f"## Building the gross-matched null: {len(BOOKS)} books x {NDRAW} draws "
      f"(926's ROT convention)")
    nrows, gross_err, count_err = [], 0.0, 0
    for bi, (nm, b) in enumerate(sorted(BOOKS.items())):
        p = b["panel"]
        px = PX[p]
        mask = rebalance_mask(px.index, b["freq"])
        sb = SPYB[p]
        rng = np.random.default_rng(SEED0 + 1000 * bi)
        Wv = b["W"].reindex(px.index).fillna(0.0).values
        reb = np.flatnonzero(mask.values)
        k_book = (Wv[reb] != 0).sum(axis=1)
        g_book = Wv[reb].sum(axis=1)
        st = REC[p]
        for d in range(NDRAW):
            Wn, kn, gn = rot_null_weights(px, b["W"], mask, rng)
            gross_err = max(gross_err, float(np.abs(gn - g_book).max()))
            count_err = max(count_err, int(np.abs(kn - k_book).max()))
            rr, tt = fast_run(px, Wn, mask)
            for c in RUNGS:
                bk = path_block((rr - tt * c / 1e4).loc[st:])
                lg = legs_at(bk, sb)
                nrows.append(dict(book=nm, set=b["set"], panel=p, draw=d, cost=c,
                                  OOS_Sharpe=bk["OOS_Sharpe"], OOS_CAGR=bk["OOS_CAGR"],
                                  OOS_MaxDD=bk["OOS_MaxDD"], Sharpe=bk["Sharpe"],
                                  **lg, pass4b=all(lg.values()),
                                  pass4bp=all(lg[k] for k in LEGS4)))
        if (bi + 1) % 10 == 0:
            P(f"   ... {bi+1}/{len(BOOKS)} books  ({time.time()-t0:.0f}s)")
    N = pd.DataFrame(nrows)
    g5 = gross_err < 1e-12 and count_err == 0
    P(f"G5 GROSS MATCH null vs book (max |d gross| / max |d count|): {gross_err:.3e} / "
      f"{count_err}  {'PASS' if g5 else 'FAIL'}")
    gates.append(dict(gate="G5", what="null gross/count match",
                      value=f"{gross_err:.3e}/{count_err}", verdict="PASS" if g5 else "FAIL"))
    dump(pd.DataFrame(gates), "gates")
    dump(N, "null", gz=True)

    # ================================================================ HYPOTHESES
    P("")
    P("## (A) THE WIDENING and (B) THE NULL PRICE — 2 tuned dials, all points reported")
    P("")
    hyp, cells = [], []
    for cs in CLAIM_SETS:
        mem = MEMBER[cs]
        for c in RUNGS:
            rr = R[(R.book.isin(mem)) & (R.cost == c)]
            nn = N[(N.book.isin(mem)) & (N.cost == c)]
            n_books = len(rr)
            p4b = rr.pass4b.mean()
            p4bp = rr.pass4bp.mean()
            q4b = nn.pass4b.mean()
            q4bp = nn.pass4bp.mean()
            fails = rr[~rr.pass4b]
            sole = fails.L3_sole.mean() if len(fails) else np.nan
            anyb = fails.L3_any.mean() if len(fails) else np.nan
            cells.append(dict(claim_set=cs, cost=c, n_books=n_books, n_null=len(nn),
                              real_4b=p4b, real_4bp=p4bp, d_real=p4bp - p4b,
                              null_4b=q4b, null_4bp=q4bp, d_null=q4bp - q4b,
                              DISC_4b=p4b - q4b, DISC_4bp=p4bp - q4bp,
                              d_DISC=(p4bp - q4bp) - (p4b - q4b),
                              n_fail=len(fails), L3_sole_rate=sole, L3_any_rate=anyb,
                              n_flip=int(fails.L3_sole.sum()) if len(fails) else 0))
    CELL = pd.DataFrame(cells)
    dump(CELL, "cells")
    P(f"{'claim':6s} {'cost':>5s} {'nbk':>4s} | {'real4b':>7s} {'real4b1':>7s} {'dreal':>7s} | "
      f"{'null4b':>7s} {'null4b1':>7s} {'dnull':>7s} | {'DISC4b':>7s} {'DISC4b1':>7s} "
      f"{'dDISC':>7s} | {'sole':>6s} {'any':>6s} {'flip':>4s}")
    for _, r in CELL.iterrows():
        P(f"{r.claim_set:6s} {r.cost:5.0f} {r.n_books:4.0f} | {r.real_4b:7.4f} {r.real_4bp:7.4f} "
          f"{r.d_real:+7.4f} | {r.null_4b:7.4f} {r.null_4bp:7.4f} {r.d_null:+7.4f} | "
          f"{r.DISC_4b:+7.4f} {r.DISC_4bp:+7.4f} {r.d_DISC:+7.4f} | {r.L3_sole_rate:6.4f} "
          f"{r.L3_any_rate:6.4f} {r.n_flip:4.0f}")

    HEAD = CELL[(CELL.claim_set == CLAIM_HEAD) & (CELL.cost == RUNG_HEAD)].iloc[0]

    # H_BIND
    sole_max = float(CELL.L3_sole_rate.max())
    h = sole_max < 0.01
    P("")
    P(f"H_BIND  bar: `L3_OOS` SOLE-binder rate < 0.01 in EVERY cell.  max over "
      f"{len(CELL)} cells = {sole_max:.4f}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_BIND", bar="max sole rate < 0.01", value=f"{sole_max:.4f}",
                    verdict="PASS" if h else "FAIL"))

    # H_WIDEN
    dr_max = float(CELL.d_real.max())
    h = dr_max <= 0.10
    P(f"H_WIDEN bar: real pass population widens <= 0.10 in every cell.  max d_real = "
      f"{dr_max:+.4f}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_WIDEN", bar="max d_real <= 0.10", value=f"{dr_max:+.4f}",
                    verdict="PASS" if h else "FAIL"))

    # H_NULL (headline)
    h = HEAD.d_null <= HEAD.d_real
    P(f"H_NULL  HEADLINE bar: d_null <= d_real at {CLAIM_HEAD}/{RUNG_HEAD:.0f}bps.  "
      f"d_null {HEAD.d_null:+.4f} vs d_real {HEAD.d_real:+.4f}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_NULL", bar="d_null <= d_real (head cell)",
                    value=f"{HEAD.d_null:+.4f} vs {HEAD.d_real:+.4f}",
                    verdict="PASS" if h else "FAIL"))

    # H_DISC
    dd_min = float(CELL.d_DISC.min())
    h = dd_min >= -0.05
    P(f"H_DISC  bar: real-minus-null GAP shrinks <= 0.05 in every cell.  min d_DISC = "
      f"{dd_min:+.4f}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_DISC", bar="min d_DISC >= -0.05", value=f"{dd_min:+.4f}",
                    verdict="PASS" if h else "FAIL"))

    # per-leg null pass rates in the headline cell — what actually holds the coin flip out
    P("")
    P(f"PER-LEG NULL PASS RATES ({CLAIM_HEAD}, {RUNG_HEAD:.0f} bps, {len(N[(N.cost==RUNG_HEAD)]):,} "
      f"draws) — which leg the coin flip cannot clear:")
    nh = N[(N.book.isin(MEMBER[CLAIM_HEAD])) & (N.cost == RUNG_HEAD)]
    rh = R[(R.book.isin(MEMBER[CLAIM_HEAD])) & (R.cost == RUNG_HEAD)]
    legrows = []
    for k in LEGS:
        legrows.append(dict(leg=k, null_rate=nh[k].mean(), real_rate=rh[k].mean(),
                            lift=rh[k].mean() - nh[k].mean()))
        P(f"   {k:8s} null {nh[k].mean():.4f}   real {rh[k].mean():.4f}   "
          f"lift {rh[k].mean()-nh[k].mean():+.4f}")
    dump(pd.DataFrame(legrows), "perleg")

    # BINDING DEFINITION x CLAIM SET table on the NULL's own FAIL rows
    P("")
    P("BINDING DEFINITION on the NULL's FAIL rows (the population 1014 could not see):")
    bd = []
    for cs in CLAIM_SETS:
        for c in RUNGS:
            nn = N[(N.book.isin(MEMBER[cs])) & (N.cost == c)]
            f = nn[~nn.pass4b]
            if not len(f):
                continue
            solerate = float(((~f[DROP]) & f[LEGS4].all(axis=1)).mean())
            anyrate = float((~f[DROP]).mean())
            bd.append(dict(claim_set=cs, cost=c, n_fail=len(f), SOLE=solerate, ANY=anyrate))
    BD = pd.DataFrame(bd)
    dump(BD, "bindingdef")
    for _, r in BD.iterrows():
        P(f"   {r.claim_set:6s} {r.cost:5.0f}bps  n_fail {r.n_fail:6.0f}  SOLE {r.SOLE:.4f}  "
          f"ANY {r.ANY:.4f}")

    # ---------------------------------------------------------------- CO-FAIL DEPTH
    # "never SOLE" is a weak statement if the leg is one co-binder away from deciding.  The
    # DEPTH distribution says how far from sole it actually is: among rows where `L3_OOS`
    # fails, how many legs fail in total.  depth 1 == sole; depth 2 == one co-binder away.
    P("")
    P(f"CO-FAIL DEPTH — among FAIL rows where `{DROP}` fails, the TOTAL number of failing legs.")
    P("   depth 1 = SOLE (the leg decides).  depth 2 = one co-binder away from deciding.")
    depth = []
    for src, D in (("REAL", R), ("NULL", N)):
        for c in RUNGS:
            d = D[D.cost == c]
            f = d[~d.pass4b]
            g = f[~f[DROP]]
            nf = (~g[LEGS]).sum(axis=1) if len(g) else pd.Series(dtype=int)
            row = dict(source=src, cost=c, n_fail=len(f), n_L3_fails=len(g),
                       min_depth=(int(nf.min()) if len(g) else np.nan))
            for k in range(1, 6):
                row[f"depth{k}"] = int((nf == k).sum()) if len(g) else 0
            depth.append(row)
            P(f"   {src:4s} {c:5.0f}bps  FAIL rows {len(f):6d}  of which `{DROP}` fails "
              f"{len(g):6d}  depths " + " ".join(f"{k}:{row[f'depth{k}']}" for k in range(1, 6))
              + (f"  min {int(nf.min())}" if len(g) else "  (none)"))
    DEP = pd.DataFrame(depth)
    dump(DEP, "cofaildepth")
    mind = DEP.min_depth.dropna()
    h = (len(mind) == 0) or (mind.min() >= 2)
    P(f"H_DEPTH bar: `{DROP}` never fails at depth 1 (never SOLE) on ANY population.  "
      f"min depth observed = {mind.min() if len(mind) else 'n/a'}  -> {'PASS' if h else 'FAIL'}")
    hyp.append(dict(hyp="H_DEPTH", bar="min co-fail depth >= 2",
                    value=f"{mind.min() if len(mind) else 'n/a'}",
                    verdict="PASS" if h else "FAIL"))

    # ================================================================ RULE 8
    P("")
    P(f"## (C) RULE 8 walk-forward — IS-only choosers on [start, {SPLIT}], 2017-2026 read once")
    P(f"   Pool = GRID ({len(MEMBER['GRID'])} never-memo-selected books).  SHELF is excluded "
      f"from the pool: it was selected on the FULL tape.")

    def choose(sub, ch, sb_is):
        if ch == "IS_SHARPE":
            return sub.loc[sub["IS_Sharpe"].idxmax()]
        if ch == "IS_CAGR":
            return sub.loc[sub["IS_CAGR"].idxmax()]
        s = sub.copy()
        s["nlegs"] = ((s["IS_Sharpe"] > sb_is[1]).astype(int)
                      + (s["IS_CAGR"] >= CAGRFLOOR_FRAC * sb_is[0]).astype(int)
                      + (s["IS_MaxDD"].abs() <= DDCAP_FRAC * abs(sb_is[2])).astype(int))
        s = s.sort_values(["nlegs", "IS_Sharpe"], ascending=False)
        return s.loc[s.index[0]]

    SPYIS = {}
    for p in PX:
        SPYIS[p] = fmet(SPYR[p].loc[:pd.Timestamp(SPLIT)].values)
    picks = []
    for p in PX:
        pool = [n for n in MEMBER["GRID"] if BOOKS[n]["panel"] == p]
        sb = SPYB[p]
        for c in RUNGS:
            sub = R[(R.book.isin(pool)) & (R.cost == c)].set_index("book")
            for ch in CHOOSERS:
                pk = choose(sub, ch, SPYIS[p])
                v2 = V2[(p, c)]
                picks.append(dict(
                    panel=p, cost=c, chooser=ch, pick=pk.name,
                    IS_Sharpe=pk.IS_Sharpe, IS_CAGR=pk.IS_CAGR,
                    OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                    spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                    spy_OOS_MaxDD=sb["OOS_MaxDD"],
                    base_Sharpe=v2["Sharpe"], base_H1=v2["H1"], base_H2=v2["H2"],
                    base_MaxDD=v2["MaxDD"],
                    **{k: bool(pk[k]) for k in LEGS},
                    pass4b=bool(pk.pass4b), pass4bp=bool(pk.pass4bp), pass4a=bool(pk.pass4a),
                    fail4b=pk.fail4b, fail4bp=pk.fail4bp))
    PK = pd.DataFrame(picks)
    dump(PK, "walkforward")
    P("")
    P(f"{'panel':6s} {'cost':>5s} {'chooser':10s} {'pick':34s} {'OOS CAGR':>9s} {'Sh':>6s} "
      f"{'MaxDD':>8s} | {'4b':>3s} {'4b-':>4s} {'4a':>3s}  binding")
    for _, r in PK.iterrows():
        P(f"{r.panel:6s} {r.cost:5.0f} {r.chooser:10s} {r['pick']:34s} {r.OOS_CAGR:9.2%} "
          f"{r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:8.2%} | {str(r.pass4b):>3s} {str(r.pass4bp):>4s} "
          f"{str(r.pass4a):>3s}  {r.fail4b}")
    for p in PX:
        sb = SPYB[p]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p}: SPY OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.3f} / "
          f"{sb['OOS_MaxDD']:.2%};  RULES v2 (live, {RUNG_HEAD:.0f} bps) full "
          f"{v2['CAGR']:.2%} / {v2['Sharpe']:.3f} / {v2['MaxDD']:.2%} "
          f"(H1 {v2['H1']:.3f} / H2 {v2['H2']:.3f})")

    n_change = int((PK.pass4b != PK.pass4bp).sum())
    h = n_change == 0
    P("")
    P(f"H_RULE8 bar: no rule-8 PICK changes verdict when `{DROP}` is dropped, and no committed "
      f"4b FAIL becomes a 4b' pass among the picks.  changed picks = {n_change} of {len(PK)}  "
      f"-> {'PASS' if h else 'FAIL'}")
    if n_change:
        for _, r in PK[PK.pass4b != PK.pass4bp].iterrows():
            P(f"     {r.panel}/{r.cost:.0f}bps/{r.chooser}: {r['pick']}  4b {r.pass4b} -> 4b' "
              f"{r.pass4bp}  (binding was {r.fail4b})")
    hyp.append(dict(hyp="H_RULE8", bar="0 pick verdicts change",
                    value=f"{n_change}/{len(PK)}", verdict="PASS" if h else "FAIL"))

    # how many GRID books flip from FAIL to PASS at the headline rung
    flips = R[(R.cost == RUNG_HEAD) & (~R.pass4b) & (R.pass4bp)]
    P(f"   FAIL->PASS flips at {RUNG_HEAD:.0f} bps over all {len(BOOKS)} books: {len(flips)}"
      + (f"  ({', '.join(flips.book.tolist())})" if len(flips) else ""))

    # 4a
    P(f"   4a (beat the live book) over the whole {len(R)}-row real ladder: "
      f"{int(R.pass4a.sum())} of {len(R)}.")

    dump(pd.DataFrame(hyp), "hypotheses")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P("")
    P(f"done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
