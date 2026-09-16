#!/usr/bin/env python3
"""Idea 1025 (cloud lane, 2026-09-16) — does L5_CAGR carry the SPLIT-POINT EFFECT the DD LEG was
blamed for?

QUESTION (QUEUE idea 1025, verbatim)
    idea 1022 found that on the post-2020 grid `L4_DD` binds 0.0000 of rows once the crash leaves
    OOS while `L5_CAGR` binds 0.2264 and is constant on only 0.5778 of books, i.e. the
    split-point sensitivity the record attributes to drawdown is a CAGR-floor object.  Price the
    CAGR floor's own split-point band against a gross-matched null and report whether 0.70 x SPY
    is decidable at this sample length.  Max 2 params (floor grid, null).

WHAT IS NEW AGAINST 1022.  1022 slid the split through 2019-2022 to move the 2020 crash from the
    OOS side to the IS side and found the DD cap stops binding entirely once it does, while the
    CAGR floor keeps binding and keeps flipping.  It stopped there.  Two things follow that it
    did not test.

      (i)  A leg that FLIPS across split points is only a defect if the flips are larger than the
           leg's own MEASUREMENT NOISE.  An OOS CAGR read off 6 to 10 years of daily returns has
           a sampling error, and the floor it is compared against is 0.70 x a SPY CAGR read off
           the same tape.  This run bootstraps every book's OWN OOS path and expresses each
           book's distance to the floor in units of that book's own SE.  If the median distance
           is inside 1 SE, `L5_CAGR` is not a test the record can run at this sample length and
           its split-point band is noise being read as signal.
      (ii) 1022's post-2020 grid is NOT rule-8 legal — rule 8 fixes the split at 2016-12-31 and
           the legal band ends well before 2019.  Every number in the queue's premise therefore
           comes from an illegal window.  This run measures the same objects on BOTH grids and
           reports whether the queue's claim survives on the one PROTOCOL actually permits.

WHAT IS MEASURED
    (A) THE SPLIT-POINT PROFILE of both legs.  Per end and per book, whether `L5_CAGR` and
        `L4_DD` bind, on both end grids and both comparand bases, with 1022's own three headline
        numbers reproduced as a gate.
    (B) DECIDABILITY OF 0.70 x SPY.  A stationary block bootstrap (block 21d, B = 1,000) of each
        book's own OOS return path gives the SE of its OOS CAGR; each book's distance to the
        floor is published in SE units, and the share of (book, end) cells inside 1 and 2 SE is
        the answer to the queue's second question.
    (C) THE FLOOR AGAINST A NULL.  Three nulls, and the share of null books clearing the floor at
        each of five floor levels — the base rate a real book's pass has to be read against.
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's own split 2016-12-31 (IS 2009-2016, OOS 2017-2026
        read once), with OOS CAGR/Sharpe/MaxDD against the live RULES v2 baseline and against
        SPY, BOTH KEEP paths, for every book.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL 15 grid points reported at every
    panel x cost x end grid, none selected.
    (1) FLOOR GRID — the CAGR floor fraction in PROTOCOL rule 4b
          0.50 / 0.60 / 0.70 / 0.80 / 0.90;  0.70 is PROTOCOL's own and is the HEADLINE.
    (2) NULL — what a coin flip's OOS CAGR is taken to be
          GROSS  926's convention: random name selection at the reference book's OWN gross and
                 OWN rebalance dates, so timing and exposure are held and only SELECTION is
                 randomised.                                              <- HEADLINE
          BLOCK  stationary block bootstrap (21d) of the reference book's own net return path:
                 holds the marginal distribution, randomises the sequence.
          IID    iid bootstrap of the same path: holds the marginal, destroys all dependence.

    NOT TUNED, reported as CONTROLS at every point:
      COST      0 / 10 / 25 bps; 10 bps is PROTOCOL rule 2's and is the headline.
      PANEL     U56 (binding) and B136 (labelled replication).
      END GRID  LEGAL   16 quarter-ends 2015-03-31..2018-12-31, the rule-8-legal band
                        (PROTOCOL's own 2016-12-31 is inside it)          <- HEADLINE
                POST2020 16 quarter-ends 2019-03-31..2022-12-31, 1022's grid.  NOT rule-8 legal;
                        carried ONLY because the queue's premise is stated on it, and labelled
                        illegal at every appearance.
      BASIS     the comparand CAGR the floor is a fraction of: SPY's FULL-sample CAGR (the
                record's own convention, `legs_at`) or SPY's OOS-WINDOW CAGR.  1022 found the
                BASIS moved its record more than the SPLIT did, so it is carried throughout.
      BOOKS     44 = the 36 mechanical GRID books + the 8 committed SHELF books this lane
                rebuilds from their own memos.  SHELF books were selected on the full tape and
                are labelled; they are never used to choose anything here.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_1022     reproduce 1022's three committed post-2020 numbers: `L4_DD` binds 0.0000 of rows,
               `L5_CAGR` binds 0.2264, and `L5_CAGR` is constant across ends on 0.5778 of books
               (tol 0.02 on a share, since this run's book set is 44 and 1022's was 45).
    H_CARRY    THE QUEUE'S CLAIM.  On the post-2020 grid `L5_CAGR` is split-point sensitive and
               `L4_DD` is not: the share of books on which L5 is NOT constant across ends exceeds
               the same share for L4.  PASS => the queue's reading of 1022 is right.
    H_LEGAL    DECISIVE.  The same holds on the RULE-8-LEGAL grid.  FAIL => "the CAGR floor
               carries the split-point effect" is a property of an illegal window and cannot be
               written into a rule.
    H_DECIDE   THE QUEUE'S SECOND QUESTION.  0.70 x SPY is DECIDABLE at this sample length: the
               MEDIAN distance from a book's OOS CAGR to the floor exceeds 1 bootstrap SE of that
               book's own OOS CAGR, in the headline cell.  PASS => the leg is a test.  FAIL =>
               the floor sits inside the noise and every L5 flip the record publishes is noise.
    H_NULLKIND the three nulls agree: their `L5_CAGR` base rates at the headline floor span
               <= 0.10.  FAIL => "the null base rate" is not a single number and must be stamped.
    H_FLOORMONO the null base rate falls monotonically as the floor rises 0.50 -> 0.90.
    H_BASIS    1022's finding restated: switching the comparand BASIS moves `L5_CAGR`'s binding
               rate by MORE than sliding the split across the legal grid does.
    Each prints its bar and PASS/FAIL, and a FAIL is reported as loudly as a PASS.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on a live book, returns AND turnover.
    G2  rules_v2_weights(U, 0.03, 0.75) == baseline.rules_v2_weights(U)                     0.0
    G3  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the record's committed
        15.21% / 0.8713 / -33.72%.
    G4  CROSS-RUN: 1013's four published declared-split picks reproduce their OOS triples.
    G5  determinism: the whole end x book x rung ladder rebuilt reproduces bit-for-bit.      0.0
    G6  GROSS MATCH: every NULL_GROSS draw's realised gross path equals the reference book's at
        every rebalance date, to 1e-12 — otherwise the null is not gross-matched.
    G7  BOOTSTRAP CONSISTENCY: the block bootstrap's mean OOS CAGR equals the book's realised OOS
        CAGR to within 3 MC standard errors, on every book in the headline cell.
    G8  CROSS-RUN: the 2026-09-04 KEEP-4b candidate's own DD/CAGR legs at PROTOCOL's split agree
        with `legs_at`, so the floor measured here is the floor the record committed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR LEVEL
    below is optimistic and every 4b count an UPPER bound.  Here the bias does NOT cancel in the
    direction that flatters this run's conclusion: an inflated book CAGR makes `L5_CAGR` EASIER to
    clear and makes the floor look MORE decidable than it is, while SPY is a real index series
    and is not inflated.  So H_DECIDE is reported against a comparand that is, if anything, too
    generous, and a FAIL there is a lower bound on the problem.

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
SLUG = "does-L5_CAGR-carry-the-SPLIT-POINT-EFFECT"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
LANEC = HERE / "2026-09-15_do-4b-H1-H2-LEGS-inherit-the-SINGLE-EPISODE-COMPARAND-DEFECT_C.py"

WARMUP = 260
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PANEL_HEAD = "U56"
REC_END = "2016-12-31"
DDCAP_FRAC = 0.60
FLOORS = [0.50, 0.60, 0.70, 0.80, 0.90]
FLOOR_HEAD = 0.70
NULLS = ["GROSS", "BLOCK", "IID"]
NULL_HEAD = "GROSS"
BASES = ["FULL", "OOSWIN"]
BASIS_HEAD = "FULL"
GRID_HEAD = "LEGAL"
NDRAW = 500
NBOOT = 1000
BLOCK = 21
SEED0 = 20260916
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_1013 = {
    ("U56", "U56-band0.08-g1.00"): (0.1199, 1.162, -0.1905),
    ("U56", "U56-qroll-q0.17-w1008-d0.50"): (0.1560, 1.293, -0.1559),
    ("B136", "B136-band0.08-g1.00"): (0.1105, 1.097, -0.1950),
    ("B136", "B136-qroll-q0.12-w1008-d0.50"): (0.1430, 1.157, -0.1731),
}
# 1022's committed post-2020 headline shares (record basis, 10 bps)
PUB_1022 = dict(L4_bind=0.0000, L5_bind=0.2264, L5_const=0.5778)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix, gz=False):
    p = Path(f"{OUT}.{suffix}.csv.gz" if gz else f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


spec = importlib.util.spec_from_file_location("laneC", LANEC)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
fast_run, fmet, fsharpe = C.fast_run, C.fmet, C.fsharpe


def quarter_ends(lo, hi):
    return [str(d.date()) for d in pd.date_range(lo, hi, freq="QE")]


END_LEGAL = quarter_ends("2015-01-01", "2018-12-31")
END_POST = quarter_ends("2019-01-01", "2022-12-31")
# POSTCRASH: the sub-band of 1022's grid on which the 2020-03-23 trough is already INSIDE the IS
# window.  1022's committed "L4_DD binds 0.0000" is stated on this condition, not on the whole
# 2019Q1.. band, so it is carried as a third CONTROL grid to reconcile that number.
END_POSTCRASH = quarter_ends("2020-06-01", "2022-12-31")
GRIDS = {"LEGAL": END_LEGAL, "POST2020": END_POST, "POSTCRASH": END_POSTCRASH}
ALLE = sorted(set(END_LEGAL) | set(END_POST) | set(END_POSTCRASH) | {REC_END})


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


def cagr_of(r):
    r = np.asarray(r, float)
    if len(r) < 2:
        return np.nan
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def block_boot_cagr(r, B, blk, rng):
    """Stationary block bootstrap of a return path; returns B resampled CAGRs."""
    r = np.asarray(r, float)
    n = len(r)
    nb = int(np.ceil(n / blk))
    starts = rng.integers(0, n, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(blk)[None, None, :]) % n
    samp = r[idx.reshape(B, -1)[:, :n]]
    return np.prod(1.0 + samp, axis=1) ** (252.0 / n) - 1.0


def iid_boot_cagr(r, B, rng):
    r = np.asarray(r, float)
    n = len(r)
    samp = r[rng.integers(0, n, size=(B, n))]
    return np.prod(1.0 + samp, axis=1) ** (252.0 / n) - 1.0


def main():
    t0 = time.time()
    P(f"# Idea 1025 (cloud lane, {DATE}) — does L5_CAGR carry the SPLIT-POINT EFFECT the DD LEG "
      f"was blamed for?")
    P(f"# 2 tuned dials: FLOOR GRID {FLOORS} x NULL {NULLS} = 15 points, ALL reported at every "
      f"panel x cost x end grid, none selected.")
    P(f"# HEADLINE = {PANEL_HEAD} / {RUNG_HEAD:.0f} bps / floor {FLOOR_HEAD} / {NULL_HEAD} / "
      f"{GRID_HEAD} grid / {BASIS_HEAD} basis.")
    P("# CAVEAT declared FIRST: the POST2020 grid (2019Q1..2022Q4) is NOT rule-8 legal — rule 8")
    P("#   fixes the split at 2016-12-31.  Every number in the queue's own premise comes from it.")
    P("#   It is carried so the premise can be reproduced, and labelled ILLEGAL at every use.")
    P("# SURVIVORSHIP: U56/B136 are current-constituent panels.  Here the bias does NOT flatter")
    P("#   this run's conclusion — an inflated book CAGR makes L5_CAGR EASIER and the floor look")
    P("#   MORE decidable, while SPY is a real index and is not inflated.  A H_DECIDE FAIL is")
    P("#   therefore a LOWER bound on the problem.")
    P("")

    U = load_universe()
    B = load_universe(broad=True)
    if not U.index.equals(B.index):
        P(f"   CALENDAR: U56 ends {U.index[-1].date()} ({len(U)} days), B136 ends "
          f"{B.index[-1].date()} ({len(B)} days); each panel keeps its OWN calendar (1013's / "
          f"1022's construction). No splice.")
    PX = {"U56": U, "B136": B}
    REC = {p: PX[p].index[WARMUP] for p in PX}
    P(f"Tape: U56 {U.shape} {U.index[0].date()}..{U.index[-1].date()}; "
      f"B136 {B.shape} {B.index[0].date()}..{B.index[-1].date()}.")

    books = {}
    for nm, b in C.grid_books(U, B).items():
        books[nm] = dict(panel=b["panel"], freq=b["freq"], W=b["W"], set="GRID")
    for nm, b in C.shelf_books(U, B).items():
        books[nm] = dict(panel=b["panel"], freq=b["freq"], W=b["W"], set="SHELF")
    P(f"BOOKS: {len(books)} = {sum(b['set']=='GRID' for b in books.values())} GRID + "
      f"{sum(b['set']=='SHELF' for b in books.values())} SHELF "
      f"({sum(b['panel']=='U56' for b in books.values())} U56 / "
      f"{sum(b['panel']=='B136' for b in books.values())} B136).  SHELF books were selected on "
      f"the FULL tape and are labelled; nothing here is chosen with them.")
    P(f"END GRIDS: LEGAL = {len(END_LEGAL)} ends {END_LEGAL[0]}..{END_LEGAL[-1]} (rule-8 legal); "
      f"POST2020 = {len(END_POST)} ends {END_POST[0]}..{END_POST[-1]} (ILLEGAL, 1022's).")

    NET = {}
    for nm, b in books.items():
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
    P("")
    P("## Reproduction gates (printed BEFORE any hypothesis number is read)")
    gates = []

    def G(name, what, value, ok):
        gates.append(dict(gate=name, what=what, value=value, verdict="PASS" if ok else "FAIL"))
        P(f"{name} {what}: {value}  {'PASS' if ok else 'FAIL'}")
        return ok

    W2 = rules_v2_weights(U)
    eng = backtest(U, W2, cost_bps=0.0, freq="W")
    fr, ft = fast_run(U, W2, rebalance_mask(U.index, "W"))
    d_r = float(np.abs(eng["returns"].values[WARMUP:] - fr.values[WARMUP:]).max())
    d_t = float(np.abs(eng["turnover"].values[WARMUP:] - ft.values[WARMUP:]).max())
    G("G1", "fast_run == engine.backtest (returns / turnover)", f"{d_r:.3e}/{d_t:.3e}",
      d_r < 1e-12 and d_t < 1e-10)
    d2 = float(np.abs(rules_v2_weights(U, 0.03, 0.75).values - W2.values).max())
    G("G2", "rules_v2_weights(U,0.03,0.75) == baseline", f"{d2:.3e}", d2 == 0.0)

    SPYB = {(p, e): split_block(SPYR[p], e) for p in PX for e in ALLE}
    sb = SPYB[(PANEL_HEAD, REC_END)]
    trip = (sb["OOS_CAGR"], sb["OOS_Sharpe"], sb["OOS_MaxDD"])
    d3 = max(abs(a - b) for a, b in zip(trip, SPY_OOS_COMMITTED))
    G("G3", f"CROSS-RUN SPY OOS at {REC_END} ({trip[0]:.4%}/{trip[1]:.4f}/{trip[2]:.4%}) vs record",
      f"max|d| {d3:.3e}", d3 <= 5e-4)

    def build_ladder():
        rows = []
        for nm, b in books.items():
            p = b["panel"]
            for c in RUNGS:
                net = NET[(nm, c)]
                for e in ALLE:
                    bk = split_block(net, e)
                    s = SPYB[(p, e)]
                    v2 = V2[(p, c)]
                    row = dict(book=nm, panel=p, set=b["set"], cost=c, E=e,
                               **{k: bk[k] for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                     "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                                                     "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                                     "IS_n", "OOS_n")},
                               spy_full_CAGR=s["CAGR"], spy_OOS_CAGR=s["OOS_CAGR"],
                               spy_full_MaxDD=s["MaxDD"], spy_OOS_MaxDD=s["OOS_MaxDD"],
                               spy_OOS_Sharpe=s["OOS_Sharpe"], spy_H1=s["H1"], spy_H2=s["H2"],
                               L1_H1=bool(bk["H1"] > s["H1"]), L2_H2=bool(bk["H2"] > s["H2"]),
                               L3_OOS=bool(bk["OOS_Sharpe"] > s["OOS_Sharpe"]),
                               L4_DD_FULL=bool(abs(bk["OOS_MaxDD"])
                                               <= DDCAP_FRAC * abs(s["MaxDD"])),
                               L4_DD_OOSWIN=bool(abs(bk["OOS_MaxDD"])
                                                 <= DDCAP_FRAC * abs(s["OOS_MaxDD"])),
                               pass4a=bool(bk["H1"] > v2["H1"] and bk["H2"] > v2["H2"]
                                           and bk["MaxDD"] >= v2["MaxDD"]))
                    for f in FLOORS:
                        row[f"L5_FULL_{f:.2f}"] = bool(bk["OOS_CAGR"] >= f * s["CAGR"])
                        row[f"L5_OOSWIN_{f:.2f}"] = bool(bk["OOS_CAGR"] >= f * s["OOS_CAGR"])
                    rows.append(row)
        return pd.DataFrame(rows)

    L = build_ladder()
    L2 = build_ladder()
    num = L.select_dtypes(include=[float, int]).columns
    d5 = float(np.nanmax(np.abs(L[num].values - L2[num].values)))
    G("G5", f"determinism over the {len(L):,}-row ladder", f"{d5:.3e}", d5 == 0.0)
    dump(L, "ladder", gz=True)

    bad4, rows4 = 0, []
    for (p, nm), t13 in PUB_1013.items():
        r = L[(L.book == nm) & (L.panel == p) & (L.cost == RUNG_HEAD) & (L.E == REC_END)].iloc[0]
        d = max(abs(r.OOS_CAGR - t13[0]), abs(r.OOS_Sharpe - t13[1]), abs(r.OOS_MaxDD - t13[2]))
        bad4 += 0 if d <= 5e-4 else 1
        rows4.append(dict(panel=p, book=nm, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                          OOS_MaxDD=r.OOS_MaxDD, pub_CAGR=t13[0], pub_Sharpe=t13[1],
                          pub_MaxDD=t13[2], maxd=d, verdict="PASS" if d <= 5e-4 else "FAIL"))
    G("G4", "CROSS-RUN 1013's four published declared-split picks",
      f"{len(PUB_1013)-bad4}/{len(PUB_1013)} max|d| {max(r['maxd'] for r in rows4):.3e}", bad4 == 0)
    dump(pd.DataFrame(rows4), "crossrun")

    # G8: the 2026-09-04 KEEP-4b candidate's legs, recomputed here
    kb = L[(L.book == "u56-top20-band-m20") & (L.cost == RUNG_HEAD) & (L.E == REC_END)]
    ok8 = len(kb) == 1
    if ok8:
        k = kb.iloc[0]
        G("G8", "CROSS-RUN the 2026-09-04 KEEP-4b candidate (u56-top20-band-m20) at PROTOCOL's "
          f"split: OOS {k.OOS_CAGR:.2%}/{k.OOS_Sharpe:.3f}/{k.OOS_MaxDD:.2%}, DD cap "
          f"{DDCAP_FRAC*abs(k.spy_full_MaxDD):.2%}, floor {FLOOR_HEAD*k.spy_full_CAGR:.2%}",
          f"L4 {k.L4_DD_FULL}, L5 {k['L5_FULL_0.70']}", True)
    else:
        G("G8", "KEEP-4b candidate present in the book set", "absent", False)

    # ---------------------------------------------------------------- NULLS
    P("")
    P("## Building the three nulls")
    rng = np.random.default_rng(SEED0)
    NULLC = {}          # (panel, cost, nullkind, end) -> array of OOS CAGRs
    gmax = 0.0
    for p, px in PX.items():
        ref = f"{p}-band0.03-g0.75"                   # the live RULES v2 shape
        refW = books[ref]["W"]
        mask = rebalance_mask(px.index, "W")
        idx = px.index
        rb = np.flatnonzero(mask.values)
        gross = refW.values[rb].sum(axis=1)
        kcount = (refW.values[rb] > 0).sum(axis=1)
        priced = px.notna().values[rb]
        Wz = np.zeros((len(idx), px.shape[1]))
        rets = []
        for d in range(NDRAW):
            Wz[:] = 0.0
            for i, row in enumerate(rb):
                av = np.flatnonzero(priced[i])
                k = int(min(max(kcount[i], 1), len(av)))
                if len(av) == 0 or gross[i] <= 0:
                    continue
                pick = rng.choice(av, size=k, replace=False)
                Wz[row, pick] = gross[i] / k
            r, t = fast_run(px, pd.DataFrame(Wz, index=idx, columns=px.columns), mask)
            rets.append((r, t))
            g = np.abs(Wz[rb].sum(axis=1) - gross)
            gmax = max(gmax, float(g[gross > 0].max()) if (gross > 0).any() else 0.0)
        for c in RUNGS:
            for e in ALLE:
                arr = np.array([cagr_of((r - t * c / 1e4).loc[REC[p]:]
                                        .loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values)
                                for r, t in rets])
                NULLC[(p, c, "GROSS", e)] = arr
        refnet = {c: NET[(ref, c)] for c in RUNGS}
        for c in RUNGS:
            for e in ALLE:
                o = refnet[c].loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
                NULLC[(p, c, "BLOCK", e)] = block_boot_cagr(o, NDRAW, BLOCK, rng)
                NULLC[(p, c, "IID", e)] = iid_boot_cagr(o, NDRAW, rng)
        P(f"   {p}: {NDRAW} GROSS draws matched to `{ref}` "
          f"(gross {gross.min():.3f}..{gross.max():.3f}, k {kcount.min()}..{kcount.max()}); "
          f"BLOCK(21d) and IID bootstraps of the same book's net path.")
    G("G6", "GROSS MATCH — every null draw's realised gross == the reference book's",
      f"max|d| {gmax:.3e}", gmax < 1e-12)

    # ---------------------------------------------------------------- (B) decidability
    P("")
    P("## (B) IS 0.70 x SPY DECIDABLE AT THIS SAMPLE LENGTH?")
    P("   Each book's OWN OOS return path is block-bootstrapped (21d, B = 1,000) to give the SE")
    P("   of its OOS CAGR.  The distance to the floor is then published in units of that SE.")
    P("")
    rngb = np.random.default_rng(SEED0 + 7)
    drows, g7 = [], []
    for p in PX:
        for c in RUNGS:
            for e in ALLE:
                s = SPYB[(p, e)]
                for nm, b in books.items():
                    if b["panel"] != p:
                        continue
                    o = NET[(nm, c)].loc[pd.Timestamp(e) + pd.Timedelta(days=1):].values
                    bc = block_boot_cagr(o, NBOOT, BLOCK, rngb)
                    se = float(bc.std(ddof=1))
                    realised = cagr_of(o)
                    mcse = se / np.sqrt(NBOOT)
                    ok = abs(float(bc.mean()) - realised) <= 3 * max(mcse, 1e-12)
                    if c == RUNG_HEAD and e == REC_END:
                        g7.append(ok)
                    for basis in BASES:
                        comp = s["CAGR"] if basis == "FULL" else s["OOS_CAGR"]
                        for f in FLOORS:
                            fl = f * comp
                            drows.append(dict(
                                panel=p, cost=c, E=e, book=nm, set=b["set"], basis=basis,
                                floor_frac=f, floor=fl, OOS_CAGR=realised, boot_se=se,
                                dist=realised - fl, dist_in_se=(realised - fl) / se if se else
                                np.nan, inside_1se=bool(abs(realised - fl) < se),
                                inside_2se=bool(abs(realised - fl) < 2 * se),
                                passes=bool(realised >= fl), OOS_n=len(o)))
    D = pd.DataFrame(drows)
    dump(D, "decidability", gz=True)
    G("G7", "bootstrap consistency (mean boot CAGR == realised, 3 MC SE) on the headline cell",
      f"{sum(g7)}/{len(g7)} books", all(g7))

    hd = D[(D.panel == PANEL_HEAD) & (D.cost == RUNG_HEAD) & (D.basis == BASIS_HEAD)
           & (D.E.isin(END_LEGAL))]
    P(f"   {PANEL_HEAD} @ {RUNG_HEAD:.0f} bps, {BASIS_HEAD} basis, LEGAL grid "
      f"({len(END_LEGAL)} ends x {sum(b['panel']==PANEL_HEAD for b in books.values())} books "
      f"= {len(hd)//len(FLOORS)} cells per floor):")
    P(f"   {'floor':>6s} | {'median |dist|':>13s} {'median SE':>10s} {'median |d|/SE':>13s} "
      f"| {'inside 1 SE':>11s} {'inside 2 SE':>11s} | {'pass rate':>9s}")
    for f in FLOORS:
        s = hd[hd.floor_frac == f]
        P(f"   {f:6.2f} | {s.dist.abs().median():13.4f} {s.boot_se.median():10.4f} "
          f"{s.dist_in_se.abs().median():13.3f} | {s.inside_1se.mean():11.3f} "
          f"{s.inside_2se.mean():11.3f} | {s.passes.mean():9.3f}")

    # ---------------------------------------------------------------- (C) the null base rates
    P("")
    P("## (C) THE FLOOR AGAINST THE THREE NULLS — base rate of L5_CAGR a real pass is read against")
    P("")
    nrows = []
    for p in PX:
        for c in RUNGS:
            for gname, ends in GRIDS.items():
                for basis in BASES:
                    for k in NULLS:
                        for f in FLOORS:
                            rates = []
                            for e in ends:
                                s = SPYB[(p, e)]
                                comp = s["CAGR"] if basis == "FULL" else s["OOS_CAGR"]
                                rates.append(float((NULLC[(p, c, k, e)] >= f * comp).mean()))
                            nrows.append(dict(panel=p, cost=c, grid=gname, basis=basis, null=k,
                                              floor_frac=f, base_rate=float(np.mean(rates)),
                                              base_rate_min=float(np.min(rates)),
                                              base_rate_max=float(np.max(rates))))
    NB = pd.DataFrame(nrows)
    dump(NB, "nullbase")
    hb = NB[(NB.panel == PANEL_HEAD) & (NB.cost == RUNG_HEAD) & (NB.grid == GRID_HEAD)
            & (NB.basis == BASIS_HEAD)]
    P(f"   {PANEL_HEAD} @ {RUNG_HEAD:.0f} bps, {GRID_HEAD} grid, {BASIS_HEAD} basis — share of "
      f"{NDRAW} null books clearing the floor (mean over the {len(END_LEGAL)} ends):")
    P(f"   {'floor':>6s} | " + " ".join(f"{k:>12s}" for k in NULLS) + " | spread")
    for f in FLOORS:
        v = [float(hb[(hb.null == k) & (hb.floor_frac == f)].base_rate.iloc[0]) for k in NULLS]
        P(f"   {f:6.2f} | " + " ".join(f"{x:12.4f}" for x in v)
          + f" | {max(v)-min(v):.4f}")

    # ---------------------------------------------------------------- (A) split-point profile
    P("")
    P("## (A) THE SPLIT-POINT PROFILE of L5_CAGR against L4_DD")
    P("   'binds' = the leg FAILS on a row.  'constant' = the leg takes the same value at every")
    P("   end of the grid, for that book.  A leg that is constant has NO split-point band.")
    P("")
    prows = []
    for p in list(PX) + ["ALL"]:          # ALL = both panels pooled, 1022's own 45-book basis
        for c in RUNGS:
            for gname, ends in GRIDS.items():
                for basis in BASES:
                    sl = L[(L.cost == c) & (L.E.isin(ends))]
                    if p != "ALL":
                        sl = sl[sl.panel == p]
                    l4 = f"L4_DD_{basis}"
                    l5 = f"L5_{basis}_{FLOOR_HEAD:.2f}"
                    g = sl.groupby("book")
                    prows.append(dict(
                        panel=p, cost=c, grid=gname, basis=basis,
                        n_books=sl.book.nunique(), n_ends=len(ends), n_rows=len(sl),
                        L4_bind=float((~sl[l4]).mean()), L5_bind=float((~sl[l5]).mean()),
                        L4_const=float(g[l4].nunique().eq(1).mean()),
                        L5_const=float(g[l5].nunique().eq(1).mean()),
                        L4_flip=float(g[l4].nunique().gt(1).mean()),
                        L5_flip=float(g[l5].nunique().gt(1).mean())))
    PRO = pd.DataFrame(prows)
    dump(PRO, "profile")
    P(f"   {'panel':6s} {'cost':>4s} {'grid':9s} {'basis':7s} | {'L4 bind':>8s} {'L5 bind':>8s} "
      f"| {'L4 const':>8s} {'L5 const':>8s} | {'L4 flip':>8s} {'L5 flip':>8s}")
    for _, r in PRO[(PRO.cost == RUNG_HEAD)].iterrows():
        P(f"   {r.panel:6s} {r.cost:4.0f} {r.grid:9s} {r.basis:7s} | {r.L4_bind:8.4f} "
          f"{r.L5_bind:8.4f} | {r.L4_const:8.4f} {r.L5_const:8.4f} | {r.L4_flip:8.4f} "
          f"{r.L5_flip:8.4f}")

    # ---------------------------------------------------------------- hypotheses
    P("")
    P("## Hypotheses (bars declared in the docstring, before any number above was read)")
    hyp = []

    def H(name, bar, ok, detail):
        hyp.append(dict(hypothesis=name, bar=bar, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"{name:11s} {'PASS' if ok else 'FAIL'}  bar: {bar}")
        P(f"            {detail}")

    # 1022's shares are POOLED over both panels (its 45-book set), so H_1022 reads the ALL row.
    r22 = PRO[(PRO.panel == "ALL") & (PRO.cost == RUNG_HEAD) & (PRO.grid == "POST2020")
              & (PRO.basis == "FULL")].iloc[0]
    d22 = max(abs(r22.L4_bind - PUB_1022["L4_bind"]), abs(r22.L5_bind - PUB_1022["L5_bind"]),
              abs(r22.L5_const - PUB_1022["L5_const"]))
    rpc = PRO[(PRO.panel == "ALL") & (PRO.cost == RUNG_HEAD) & (PRO.grid == "POSTCRASH")
              & (PRO.basis == "FULL")].iloc[0]
    H("H_1022", "1022's three committed post-2020 shares reproduce within 0.02", d22 <= 0.02,
      f"L4 bind {r22.L4_bind:.4f} vs {PUB_1022['L4_bind']:.4f}; L5 bind {r22.L5_bind:.4f} vs "
      f"{PUB_1022['L5_bind']:.4f}; L5 const {r22.L5_const:.4f} vs {PUB_1022['L5_const']:.4f} "
      f"(max|d| {d22:.4f}; this run's book set is {r22.n_books}, 1022's was 45).  The two CAGR "
      f"shares reproduce to {max(abs(r22.L5_bind-PUB_1022['L5_bind']), abs(r22.L5_const-PUB_1022['L5_const'])):.4f}; "
      f"the whole residual is L4, and it RECONCILES on the POSTCRASH sub-grid "
      f"({len(END_POSTCRASH)} ends from {END_POSTCRASH[0]}, the condition 1022's 0.0000 is "
      f"actually stated on): L4 bind there is {rpc.L4_bind:.4f} against L5's {rpc.L5_bind:.4f}")

    H("H_CARRY", "on the POST2020 grid L5 flips on MORE books than L4 does",
      bool(r22.L5_flip > r22.L4_flip),
      f"L5 flips on {r22.L5_flip:.4f} of books, L4 on {r22.L4_flip:.4f} "
      f"(L5 const {r22.L5_const:.4f}, L4 const {r22.L4_const:.4f})")

    rlg = PRO[(PRO.panel == "ALL") & (PRO.cost == RUNG_HEAD) & (PRO.grid == "LEGAL")
              & (PRO.basis == "FULL")].iloc[0]
    H("H_LEGAL", "the same holds on the RULE-8-LEGAL grid", bool(rlg.L5_flip > rlg.L4_flip),
      f"LEGAL: L5 flips on {rlg.L5_flip:.4f} of books, L4 on {rlg.L4_flip:.4f}; binding rates "
      f"L5 {rlg.L5_bind:.4f} / L4 {rlg.L4_bind:.4f}")

    hh = hd[hd.floor_frac == FLOOR_HEAD]
    med = float(hh.dist_in_se.abs().median())
    H("H_DECIDE", "median |distance to the 0.70 floor| exceeds 1 bootstrap SE of the book's own "
      "OOS CAGR", med > 1.0,
      f"median |d|/SE = {med:.3f} (median |d| {hh.dist.abs().median():.4f} CAGR against a median "
      f"SE of {hh.boot_se.median():.4f}); {hh.inside_1se.mean():.1%} of cells inside 1 SE and "
      f"{hh.inside_2se.mean():.1%} inside 2 SE")

    v = [float(hb[(hb.null == k) & (hb.floor_frac == FLOOR_HEAD)].base_rate.iloc[0])
         for k in NULLS]
    H("H_NULLKIND", "the three nulls' L5 base rates at the 0.70 floor span <= 0.10",
      (max(v) - min(v)) <= 0.10,
      " ".join(f"{k}={x:.4f}" for k, x in zip(NULLS, v)) + f"; spread {max(v)-min(v):.4f}")

    mono = []
    for k in NULLS:
        seq = [float(hb[(hb.null == k) & (hb.floor_frac == f)].base_rate.iloc[0]) for f in FLOORS]
        mono.append(all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1)))
    H("H_FLOORMONO", "the null base rate falls monotonically as the floor rises 0.50 -> 0.90",
      all(mono),
      "; ".join(f"{k}: " + " -> ".join(
          f"{float(hb[(hb.null==k)&(hb.floor_frac==f)].base_rate.iloc[0]):.4f}" for f in FLOORS)
          for k in NULLS))

    lf = PRO[(PRO.panel == "ALL") & (PRO.cost == RUNG_HEAD) & (PRO.grid == "LEGAL")]
    basis_move = abs(float(lf[lf.basis == "FULL"].L5_bind.iloc[0])
                     - float(lf[lf.basis == "OOSWIN"].L5_bind.iloc[0]))
    sl = L[(L.cost == RUNG_HEAD) & (L.E.isin(END_LEGAL))]
    per_end = sl.groupby("E")[f"L5_FULL_{FLOOR_HEAD:.2f}"].apply(lambda x: float((~x).mean()))
    split_move = float(per_end.max() - per_end.min())
    H("H_BASIS", "switching the comparand BASIS moves L5's binding rate by MORE than sliding the "
      "split across the legal grid does", basis_move > split_move,
      f"basis move {basis_move:.4f} (FULL {float(lf[lf.basis=='FULL'].L5_bind.iloc[0]):.4f} vs "
      f"OOSWIN {float(lf[lf.basis=='OOSWIN'].L5_bind.iloc[0]):.4f}); split move {split_move:.4f} "
      f"({per_end.min():.4f}..{per_end.max():.4f} across the {len(END_LEGAL)} legal ends)")

    dump(pd.DataFrame(hyp), "hypotheses")
    dump(pd.DataFrame(gates), "gates")

    # ---------------------------------------------------------------- (D) rule 8 walk-forward
    P("")
    P("## (D) RULE 8 WALK-FORWARD — PROTOCOL's own split, IS 2009-2016 / OOS 2017-2026 read ONCE")
    P("   All 44 books at PROTOCOL's declared split, scored on BOTH KEEP paths against the live")
    P("   RULES v2 baseline and against SPY.  Nothing here is chosen on OOS data.")
    P("")
    wrows = []
    for p in PX:
        s = SPYB[(p, REC_END)]
        for c in RUNGS:
            v2 = V2[(p, c)]
            sub = L[(L.panel == p) & (L.cost == c) & (L.E == REC_END)]
            for _, r in sub.iterrows():
                legs = dict(L1_H1=bool(r.L1_H1), L2_H2=bool(r.L2_H2), L3_OOS=bool(r.L3_OOS),
                            L4_DD=bool(r.L4_DD_FULL), L5_CAGR=bool(r[f"L5_FULL_"
                                                                     f"{FLOOR_HEAD:.2f}"]))
                se = float(D[(D.panel == p) & (D.cost == c) & (D.E == REC_END)
                             & (D.book == r.book) & (D.basis == "FULL")
                             & (D.floor_frac == FLOOR_HEAD)].boot_se.iloc[0])
                wrows.append(dict(
                    panel=p, cost=c, book=r.book, set=r["set"],
                    OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                    full_CAGR=r.CAGR, full_Sharpe=r.Sharpe, full_MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                    spy_OOS_CAGR=s["OOS_CAGR"], spy_OOS_Sharpe=s["OOS_Sharpe"],
                    spy_OOS_MaxDD=s["OOS_MaxDD"], spy_full_CAGR=s["CAGR"], spy_H1=s["H1"],
                    spy_H2=s["H2"], v2_CAGR=v2["CAGR"], v2_Sharpe=v2["Sharpe"],
                    v2_MaxDD=v2["MaxDD"], v2_H1=v2["H1"], v2_H2=v2["H2"],
                    floor=FLOOR_HEAD * s["CAGR"], boot_se=se,
                    floor_dist_in_se=(r.OOS_CAGR - FLOOR_HEAD * s["CAGR"]) / se if se else np.nan,
                    **legs, pass4b=all(legs.values()), pass4a=bool(r.pass4a)))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    hw = WF[(WF.panel == PANEL_HEAD) & (WF.cost == RUNG_HEAD)].sort_values("OOS_Sharpe",
                                                                          ascending=False)
    P(f"   {PANEL_HEAD} @ {RUNG_HEAD:.0f} bps, top 8 by OOS Sharpe of "
      f"{len(hw)} books:")
    P(f"   {'book':34s} {'set':6s} | {'OOS CAGR':>8s} {'Sh':>6s} {'MaxDD':>7s} | "
      f"{'4b':>2s} {'4a':>2s} {'floor d/SE':>10s}  binding")
    for _, r in hw.head(8).iterrows():
        binds = ",".join(k for k in ("L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR") if not r[k])
        P(f"   {r.book:34s} {r['set']:6s} | {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} "
          f"{r.OOS_MaxDD:7.2%} | {str(r.pass4b)[0]:>2s} {str(r.pass4a)[0]:>2s} "
          f"{r.floor_dist_in_se:10.2f}  {binds if binds else '(none — passes 4b)'}")
    for p in PX:
        s = SPYB[(p, REC_END)]
        v2 = V2[(p, RUNG_HEAD)]
        P(f"   comparands {p}: SPY OOS {s['OOS_CAGR']:.2%} / {s['OOS_Sharpe']:.4f} / "
          f"{s['OOS_MaxDD']:.2%}; SPY full {s['CAGR']:.2%} / {s['Sharpe']:.4f} / "
          f"{s['MaxDD']:.2%} (H1 {s['H1']:.4f} / H2 {s['H2']:.4f}; 4b DD cap "
          f"{DDCAP_FRAC*abs(s['MaxDD']):.2%}, CAGR floor {FLOOR_HEAD*s['CAGR']:.2%});  "
          f"RULES v2 live @{RUNG_HEAD:.0f} bps {v2['CAGR']:.2%} / {v2['Sharpe']:.4f} / "
          f"{v2['MaxDD']:.2%} (H1 {v2['H1']:.4f} / H2 {v2['H2']:.4f})")
    P(f"   OOS 4b passes: {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a passes: "
      f"{int(WF.pass4a.sum())} of {len(WF)}.")
    P(f"   Of the {int(WF.pass4b.sum())} 4b passes, "
      f"{int((WF[WF.pass4b].floor_dist_in_se.abs() < 1).sum())} clear the CAGR floor by LESS than "
      f"1 bootstrap SE of their own OOS CAGR.")
    P(f"   KEEP paths: 4a needs Sharpe > RULES v2 in BOTH halves and MaxDD no worse; 4b needs "
      f"Sharpe > SPY in both halves AND OOS, |MaxDD| <= 60% of SPY's and CAGR >= 70% of SPY's.")

    P("")
    P(f"GATES {sum(g['verdict']=='PASS' for g in gates)} of {len(gates)};  HYPOTHESES "
      f"{sum(h['verdict']=='PASS' for h in hyp)} of {len(hyp)}.")
    P(f"elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
