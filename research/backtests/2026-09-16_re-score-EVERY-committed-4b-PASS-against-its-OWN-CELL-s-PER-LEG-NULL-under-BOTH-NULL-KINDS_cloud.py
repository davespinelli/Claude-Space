#!/usr/bin/env python3
"""Idea 969 (cloud lane, 2026-09-16) — re-score EVERY committed 4b PASS in the record against its
OWN CELL's PER-LEG NULL, under BOTH NULL KINDS.

QUESTION (QUEUE idea 969, the SECOND entry carrying that number — defect 932 again)
    idea 942 found no leg of 4b has a coin-flip base rate <= 0.25 in all six cells tested, that
    L_OOS reads 1.000 on U56 monthly, and that the standing 2026-09-04 candidate's monthly pass
    sits in a cell whose null passes 76.0% of the time.  Harvest every committed 4b PASS row in
    LEADERBOARD.md, rebuild its cell's gross-matched null under BOTH kinds, and publish how many
    passes survive the memo's 0.90 non-certifying bar.  Max 2 params (claim set, null kind).

WHAT "BOTH KINDS" AND "THE 0.90 BAR" MEAN, quoted rather than invented.  The memo the queue
    points at is `2026-09-15_4b-leg-certification-clause_cloud.memo.md`, clause (ii), verbatim:
        "Any published 4b PASS carries, beside it, the per-leg base rate of its own cell's
         gross-matched null under BOTH null kinds (rotating and fixed).  Any leg whose base rate
         exceeds 0.90 is reported as NOT CERTIFYING rather than as a pass, and a 4b PASS in which
         every leg is non-certifying is reported as UNADJUDICATED, not as a KEEP."
    So the two kinds are ROTATING and FIXED, the bar is on a PER-LEG BASE RATE, and a pass
    SURVIVES iff at least one of its five legs has a null base rate <= 0.90.

WHAT IS NEW AGAINST COMMITTED IDEA 998.  Idea 998
    (`2026-09-16_re-score-the-record-s-COMMITTED-4b-PASSES-against-their-own-PER-LEG-NULL-
    PERCENTILES_cloud.py`) already ran this idea's CLAIM-SET half — the harvest, the STRICT /
    WIDE / STRUCT resolution, and the per-leg base rates — but on the ROTATING null ALONE.  The
    memo asks for BOTH kinds and the record has never built the FIXED one.  This run therefore
    takes the dial 998 left untouched and does NOT re-publish 998's claim-set/statistic grid:
    998's machinery is IMPORTED verbatim (panels, ladder, harvest, resolve, `draw_null`,
    `walkforward`) so that the null kind is the ONLY thing that changes, and 998's committed
    `cells.csv` is reproduced cell-for-cell as a hard gate.

WHAT HAD TO BE SAID BEFORE ANY NUMBER (declared here, ahead of the gates).
    A ROTATING draw redraws its whole basket at every rebalance.  That is not a cost-neutral
    choice: it churns far harder than any book the record holds, so at PROTOCOL's 10 bps the
    rotating null is HANDICAPPED by a cost the book does not pay, and every base rate read off
    it is therefore an UNDERSTATEMENT of what a coin flip can do.  A FIXED draw — names chosen
    once and held — pays almost nothing and is the harder comparand by arithmetic alone.  The
    prediction, written before any number below the gates was read, is that the FIXED null's
    per-leg base rates are HIGHER, that more legs cross the 0.90 non-certifying bar under it,
    and that the direction of the effect is a COST fact and not a skill fact.  A second
    prediction: 998's DEGENERACY defect (on `EWELIG` the book already holds the whole eligible
    pool, so a count-matched ROTATING draw has nothing to choose and all 200 draws are
    identical) should be CURED by the fixed kind, because a fixed basket stops tracking the
    pool the moment eligibility moves.

WHAT IS MEASURED
    (A) THE LADDER AND THE HARVEST, rebuilt with 998's own code, and the harvest DRIFT against
        998's committed counts reported rather than gated (the corpus grows between runs — that
        is ideas 1019/1026's finding, and this run is itself one of the commits that moves it).
    (B) PER-CELL, PER-KIND: the five per-leg null base rates, the null's own 4b base rate, the
        count of DISTINCT draws, and the book's mid-rank percentile inside its own null.
    (C) THE BAR: per cell and per kind, how many of the five legs CERTIFY (base rate <= 0.90),
        and whether the pass SURVIVES (>= 1 certifying leg) or is UNADJUDICATED.  Published by
        claim set, and the per-claim-unit share is published beside the per-cell share.
    (D) THE RULE-8 WALK-FORWARD at PROTOCOL's declared split (IS 2009-2016 chooses, 2017-2026
        read ONCE), run SEPARATELY UNDER EACH NULL KIND, because one of the record's three
        choosers (`C_ISPCT`) reads a null percentile and therefore inherits the dial: OOS CAGR /
        Sharpe / MaxDD against the live RULES v2 baseline and against SPY, BOTH KEEP paths.

TUNED PARAMETERS: exactly TWO, the two the queue names.  Every level published, none selected.
    (1) CLAIM SET   STRICT / WIDE / STRUCT — 998's three, verbatim, so the kinds are compared on
                    the same cells the record was already scored on.
    (2) NULL KIND   ROT   the ROTATING draw, `draw_null` imported from 998 UNCHANGED (ideas
                          680/926/931/942/970/971's construction);
                    FIX   the FIXED draw the memo names and the record has never built: the
                          basket is carried from rebalance to rebalance and only resized;
                    MID   phi = 0.50, a reported RUNG between them — the two named kinds are the
                          endpoints of one continuous rotation dial, and the rung says whether
                          the effect is a cliff or a slope.  Never used to choose anything.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_KIND   DECISIVE.  The null kind does not move the per-leg base rate: the MEDIAN
             |base_ROT - base_FIX| over all (cell, leg) points is <= 0.05.  PASS => the record's
             single-kind base rates are safe to quote.  FAIL => every per-leg base rate in the
             record is quoting an unnamed dial, and the memo's "BOTH kinds" is load-bearing.
    H_HARDER DIRECTION.  The FIXED null is the HARDER comparand: its own 4b base rate is >= the
             rotating null's in at least 0.50 of non-degenerate cells.
    H_SURV   THE BAR ITSELF.  At least 0.50 of STRICT-resolvable committed 4b passes SURVIVE the
             0.90 bar (>= 1 certifying leg) under BOTH kinds.
    H_LEG    WHICH leg certifies is kind-invariant: the two kinds agree on the certify/not
             classification of >= 0.80 of (cell, leg) points.
    H_DEGEN  The FIXED kind CURES 998's degeneracy: on the cells 998 recorded as degenerate, the
             fixed null has more than 0.50 * DRAWS distinct draws in >= 0.80 of them.
    H_RULE8  The null kind does not move a rule-8 pick: `C_ISPCT` picks the same (book, gross) in
             >= 0.80 of the 9 (panel, cadence) cells under ROT and under FIX.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  998's committed `cells.csv` reproduces EXACTLY on the ROT kind — every per-leg base rate,
        every 4b base rate and every distinct-draw count, on every shared cell.
    G2  998's committed `ladder.csv` reproduces on the shared rows (the price leg is stable even
        though the text corpus is not).
    G3  the fast `Ctx` == engine.backtest on a live book, returns AND turnover.
    G4  GROSS AND COUNT MATCH: on every kind and every cell, the draw's gross on decision rows
        equals the book's and the holding count equals the book's exactly.
    G5  THE ROTATION DIAL IS WHAT IT SAYS: realised name turnover falls monotonically from ROT
        to MID to FIX on every cell, and at phi = 1.00 the new sampler reproduces ROT's per-leg
        base rates within Monte-Carlo error on a 12-cell subset.
    G6  determinism: every null rebuilds bit-for-bit (md5 seeds, never Python's `hash()`).
    G7  CROSS-RUN: SPY's OOS triple == the committed 15.21% / 0.8711 / -33.72%.
    G8  the harvest is the record's own: 998's regexes and resolution rule, unmodified.

SURVIVORSHIP (PROTOCOL rule 9).  U56 / B136 / SMALL663 are CURRENT-CONSTITUENT lists (SMALL663
    additionally drops the tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every
    CAGR and drawdown LEVEL here is optimistic and every 4b count an UPPER bound, most severely
    on SMALL663.  The measured object is a DIFFERENCE between two nulls drawn from the SAME
    survivorship-inflated pool over the SAME tape, so the inflation is common to both kinds and
    very largely cancels; where it does not it raises BOTH base rates together, which makes the
    0.90 bar EASIER to cross on both kinds and so works AGAINST H_SURV on both.  SPY is a real
    index series and is not inflated.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py — and idea
    998's committed script, which is imported read-only.
"""
from __future__ import annotations

import importlib.util
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

I998 = HERE / ("2026-09-16_re-score-the-record-s-COMMITTED-4b-PASSES-against-their-own-"
               "PER-LEG-NULL-PERCENTILES_cloud.py")
_spec = importlib.util.spec_from_file_location("i998", I998)
C9 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C9)

from baseline import load_universe  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "re-score-EVERY-committed-4b-PASS-against-its-OWN-CELL-s-PER-LEG-NULL-under-BOTH-NULL-KINDS"
OUT = HERE / f"{DATE}_{SLUG}_cloud"

PANELS, BOOKS, GROSS_GRID, CADENCES = C9.PANELS, C9.BOOKS, C9.GROSS_GRID, C9.CADENCES
LEGS, CLAIMSETS, PROTO_COST = C9.LEGS, C9.CLAIMSETS, C9.PROTO_COST
DRAWS = C9.DRAWS
SEED0 = C9.SEED0

KINDS = ["ROT", "MID", "FIX"]            # the tuned dial; MID is a reported rung
PHI = {"ROT": 1.00, "MID": 0.50, "FIX": 0.00, "PHI1": 1.00}  # PHI1: gate G5 only
CERT_BAR = 0.90                          # the memo's non-certifying bar, quoted not invented
GATE_SUBSET = 12                         # cells used for the phi=1.00 construction gate
SMOKE = int(os.environ.get("IDEA969_SMOKE", "0"))   # >0 = that many cells, for timing only
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================== the rotation dial (new code)
def draw_phi(buf, pn, W, dec, rng, phi, state):
    """Gross- and holding-count-matched draw with a ROTATION FRACTION.

    phi = 1.00 redraws the whole basket at every decision row — that IS 998's `draw_null`
    construction.  phi = 0.00 carries the basket forward and only RESIZES it, which is the FIXED
    kind the memo names.  In between, round(phi * k) of the k holdings are replaced.

    The pool a fresh name is drawn from is 998's: the eligible names on that row, widened with the
    remaining PRICED names when the book holds more names than the pool has (`EWELIG`, wide
    `BAND03`), so the holding count matches the book exactly on every row.  A carried name is kept
    only while it is still PRICED — a fixed basket ignores eligibility, but it cannot hold a name
    that does not trade.
    """
    buf[:] = 0.0
    held = W > 0
    kcount = held.sum(axis=1)
    gross = W.sum(axis=1)
    cur = state
    for i in np.flatnonzero(dec):
        k = int(kcount[i])
        if k == 0:
            cur = np.empty(0, dtype=int)
            continue
        pool = np.flatnonzero(pn.elig[i])
        if len(pool) < k:
            extra = np.setdiff1d(np.flatnonzero(pn.priced[i]), pool, assume_unique=False)
            pool = np.concatenate([pool, extra]) if len(extra) else pool
        if len(pool) == 0:
            continue
        k = min(k, len(pool))
        keep_n = int(round((1.0 - phi) * k))
        alive = cur[pn.priced[i][cur]] if len(cur) else np.empty(0, dtype=int)
        if keep_n > 0 and len(alive):
            keep = alive if len(alive) <= keep_n else rng.choice(alive, size=keep_n, replace=False)
        else:
            keep = np.empty(0, dtype=int)
        nfresh = k - len(keep)
        if nfresh > 0:
            cand = np.setdiff1d(pool, keep, assume_unique=False)
            if len(cand) < nfresh:                      # widen once more with the priced remainder
                cand = np.setdiff1d(np.flatnonzero(pn.priced[i]), keep, assume_unique=False)
            nfresh = min(nfresh, len(cand))
            fresh = rng.choice(cand, size=nfresh, replace=False) if nfresh else np.empty(0, int)
        else:
            fresh = np.empty(0, dtype=int)
        pick = np.concatenate([keep, fresh]).astype(int)
        if len(pick) == 0:
            continue
        buf[i, pick] = gross[i] / len(pick)
        cur = pick
    return buf, cur


def name_turnover(Wn, dec):
    """Mean share of the basket replaced at a decision row — the dial's own realised value."""
    rows = np.flatnonzero(dec)
    prev, acc = None, []
    for i in rows:
        s = set(np.flatnonzero(Wn[i] > 0).tolist())
        if prev is not None and (prev or s):
            acc.append(len(s - prev) / max(len(s), 1))
        prev = s
    return float(np.mean(acc)) if acc else np.nan


def build_null(pn, pk, bk, g, cad, kind, draws=DRAWS, collect_gross=False):
    """One cell, one kind: `draws` gross- and count-matched coin flips, scored like the book."""
    Wbook = pn.books[g][bk]
    dec = pn.dec[cad]
    buf = np.zeros_like(Wbook)
    recs, gchk, ntn = [], None, []
    for d in range(draws):
        # ROT reuses 998's OWN seed stream, so gate G1 can demand an EXACT reproduction
        # of its committed cells.csv rather than a Monte-Carlo agreement.
        rng = (np.random.default_rng(C9.seed_of(SEED0, pk, bk, g, cad, d)) if kind == "ROT"
               else np.random.default_rng(C9.seed_of(SEED0, pk, bk, g, cad, kind, d)))
        if kind == "ROT":
            Wn = C9.draw_null(buf, pn, Wbook, dec, rng).copy()
        else:
            Wn, _ = draw_phi(buf, pn, Wbook, dec, rng, PHI[kind], np.empty(0, dtype=int))
            Wn = Wn.copy()
        if d == 0:
            dm = np.flatnonzero(dec)
            gchk = dict(dgross=float(np.abs(Wn[dm].sum(1) - Wbook[dm].sum(1)).max()),
                        dk=int(np.abs((Wn[dm] > 0).sum(1) - (Wbook[dm] > 0).sum(1)).max()))
        if d < 5:
            ntn.append(name_turnover(Wn, dec))
        r_, t_ = pn.ctx[cad].run(C9.lag_weights(Wn), 0.0)
        r = r_ - t_ * PROTO_COST / 1e4
        st = C9.stats_of(pn, r)
        lg = C9.legs_4b(pn, st)
        recs.append(dict(draw=d, turnover=t_[pn.warm].sum() / pn.years, **st, **lg,
                         pass4b=all(lg.values())))
    nd = pd.DataFrame(recs)
    return nd, gchk, float(np.nanmean(ntn))


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 969 (cloud lane, {DATE}) — re-score EVERY committed 4b PASS against its OWN CELL's")
    P("                                PER-LEG NULL, under BOTH NULL KINDS")
    P("=" * 100)
    P(f"# 2 tuned dials: CLAIM SET {CLAIMSETS} x NULL KIND {KINDS} "
      f"(phi {[PHI[k] for k in KINDS]}), ALL levels published, none selected.")
    P(f"# THE BAR is the memo's, quoted: a leg whose null base rate exceeds {CERT_BAR:.2f} is NOT")
    P("#   CERTIFYING; a 4b PASS with no certifying leg is UNADJUDICATED.  Source:")
    P("#   2026-09-15_4b-leg-certification-clause_cloud.memo.md, clause (ii).")
    P("# NEW AGAINST COMMITTED IDEA 998: 998 ran the CLAIM-SET half on the ROTATING null ALONE.")
    P("#   998's machinery is imported VERBATIM here so the null kind is the only thing that")
    P("#   changes, and 998's committed cells.csv is reproduced cell-for-cell as gate G1.")
    P("# DECLARED BEFORE ANY NUMBER: a ROTATING draw churns its whole basket every rebalance, so")
    P(f"#   at PROTOCOL's {PROTO_COST:.0f} bps it pays a cost no book pays and every base rate read")
    P("#   off it UNDERSTATES the coin flip.  The FIXED kind should be HARDER, should push more")
    P("#   legs past 0.90, and should CURE 998's EWELIG degeneracy.  Direction, then magnitude.")
    P("# SURVIVORSHIP: current-constituent panels; the measured object is a DIFFERENCE between")
    P("#   two nulls off the SAME pool, so the inflation very largely cancels, and where it does")
    P("#   not it raises BOTH base rates and works AGAINST H_SURV on both kinds.")
    P("")

    # ---------------------------------------------------------------- panels (998's, verbatim)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    px["SMALL663"] = sm[[c for c in sm.columns if c == "SPY" or c not in bad]]
    P(f"PANELS (SMALL663 screen: {len(sm.columns) - px['SMALL663'].shape[1]} tickers with "
      f"max_1d_move >= 1.0 dropped, PROTOCOL rule 9)")
    pnl = {}
    for k in PANELS:
        pnl[k] = C9.Panel(k, px[k])
        p = pnl[k]
        P(f"  {k:9s} {p.px.shape[1]-1:4d} names + SPY   {p.idx[0].date()} -> {p.idx[-1].date()}   "
          f"SPY full {p.spy_full[0]:7.2%} / {p.spy_full[1]:.4f} / {p.spy_full[2]:7.2%}   "
          f"SPY OOS {p.spy_oos[0]:7.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:7.2%}")

    # ---------------------------------------------------------------- ladder (998's, verbatim)
    lad = []
    for pk in PANELS:
        pn = pnl[pk]
        for bk in BOOKS:
            for g in GROSS_GRID:
                W = C9.lag_weights(pn.books[g][bk])
                for cad in CADENCES:
                    r_, t_ = pn.ctx[cad].run(W, 0.0)
                    for cst in C9.COSTS:
                        r = r_ - t_ * cst / 1e4
                        st = C9.stats_of(pn, r)
                        lg = C9.legs_4b(pn, st)
                        row = dict(panel=pk, book=bk, gross=g, cadence=cad, cost=cst,
                                   turnover=t_[pn.warm].sum() / pn.years, **st, **lg)
                        row["pass4b"] = all(lg.values())
                        row["pass4a"] = C9.pass_4a(pn, r, pn.base_r[cst])
                        row["IS_pass4b"] = all(C9.legs_4b_is(pn, st).values())
                        lad.append(row)
    LAD = pd.DataFrame(lad)
    P(f"\nLADDER {len(LAD):,} rows.  4b PASS at {PROTO_COST:.0f} bps: "
      f"{int(LAD.loc[LAD.cost == PROTO_COST, 'pass4b'].sum())} of "
      f"{int((LAD.cost == PROTO_COST).sum())}")

    # ---------------------------------------------------------------- harvest (998's, verbatim)
    CEN, n_units = C9.harvest()
    claim_cells = {}
    for cs in ("STRICT", "WIDE"):
        claim_cells[cs] = C9.resolve(CEN, cs)
    struct = sorted({(r.panel, r.book, r.gross, r.cadence)
                     for _, r in LAD[(LAD.cost == PROTO_COST) & LAD.pass4b].iterrows()})
    claim_cells["STRUCT"] = [(a, b, c, d, "STRUCT", -1) for (a, b, c, d) in struct]
    need = sorted({c[:4] for cs in CLAIMSETS for c in claim_cells[cs]})
    if SMOKE:
        need = need[:: max(1, len(need) // SMOKE)][:SMOKE]
    P(f"HARVEST {n_units:,} claim units scanned; {len(CEN):,} assert a 4b PASS.")
    for cs in CLAIMSETS:
        P(f"  {cs:7s}: {len(claim_cells[cs]):,} claim->cell resolutions over "
          f"{len({c[:4] for c in claim_cells[cs]})} DISTINCT cells")
    P(f"  NULLS TO BUILD: {len(need)} cells x {len(KINDS)} kinds x {DRAWS} draws = "
      f"{len(need)*len(KINDS)*DRAWS:,} backtests")
    P("  HARVEST DRIFT vs committed 998 (reported, NOT gated): 998 published 6,880 units / 1,977")
    P("  asserting a 4b PASS / 17 STRICT cells / 157 WIDE cells.  The corpus GROWS between runs —")
    P("  ideas 1019 and 1026's finding — and this very run is one of the commits that moves it.")
    dump(CEN, "census.csv")

    # ---------------------------------------------------------------- the nulls, by kind
    P("")
    P("-" * 100)
    P(f"THE NULLS — {len(need)} cells x {len(KINDS)} kinds x {DRAWS} draws, md5 seeds")
    P("-" * 100)
    NULL, G4ROWS, NTURN = {}, [], {}
    for n_i, (pk, bk, g, cad) in enumerate(need):
        pn = pnl[pk]
        for kind in KINDS:
            nd, gchk, nt = build_null(pn, pk, bk, g, cad, kind)
            NULL[(pk, bk, g, cad, kind)] = nd
            NTURN[(pk, bk, g, cad, kind)] = nt
            G4ROWS.append(dict(cell=f"{pk}/{bk}/{g:.2f}/{cad}", kind=kind, **gchk, name_turn=nt))
        if (n_i + 1) % 20 == 0 or n_i == len(need) - 1:
            P(f"  {n_i+1:3d}/{len(need)} cells built  ({time.time()-t0:.0f}s)")
    G4 = pd.DataFrame(G4ROWS)

    # ---------------------------------------------------------------- per-cell, per-kind scoring
    lad10 = LAD[LAD.cost == PROTO_COST].set_index(["panel", "book", "gross", "cadence"])
    rows = []
    for key in need:
        pk, bk, g, cad = key
        b = lad10.loc[key]
        for kind in KINDS:
            nd = NULL[key + (kind,)]
            row = dict(panel=pk, book=bk, gross=g, cadence=cad, kind=kind,
                       book_pass4b=bool(b.pass4b), book_Sharpe=b.Sharpe,
                       book_OOS_Sharpe=b.OOS_Sharpe, book_MaxDD=b.MaxDD,
                       book_turnover=b.turnover, null_turnover=float(nd.turnover.median()),
                       name_turnover=NTURN[key + (kind,)],
                       null_base4b=float(nd.pass4b.mean()),
                       n_unique=int(nd.OOS_Sharpe.nunique()))
            row["degenerate"] = bool(row["n_unique"] < C9.DEGEN_BAR * DRAWS)
            ncert = 0
            for lg in LEGS:
                br = float(nd[lg].mean())
                row[f"base_{lg}"] = br
                row[f"cert_{lg}"] = bool(br <= CERT_BAR)
                ncert += int(br <= CERT_BAR)
            row["n_cert"] = ncert
            row["survives"] = bool(ncert >= 1)
            for s in C9.STATS:
                row[f"pct_{s}"] = C9.pct_in(float(b[s]), nd[s].values, s)
            rows.append(row)
    CELL = pd.DataFrame(rows)
    dump(CELL, "cells.csv")

    # ============================================================ GATES
    P("")
    P("=" * 100)
    P("GATES (printed before any hypothesis number)")
    P("=" * 100)
    gates, gd = {}, []

    def G(n, ok, detail):
        gates[n] = (ok, detail)
        gd.append(dict(gate=n, verdict="PASS" if ok else "FAIL", detail=detail))
        P(f"  {n:4s} {'PASS' if ok else 'FAIL'}  {detail}")

    # G1 998's committed cells.csv on the ROT kind
    p998 = Path(str(I998).replace(".py", ".cells.csv"))
    prev = pd.read_csv(p998)
    kcols = ["panel", "book", "gross", "cadence"]
    mine = CELL[CELL.kind == "ROT"].copy()
    m = prev.merge(mine, on=kcols, suffixes=("_p", "_m"))
    cmpcols = [f"base_{lg}" for lg in LEGS] + ["null_base4b"]
    d1 = float(np.nanmax([np.abs(m[f"{c}_p"] - m[f"{c}_m"]).max() for c in cmpcols]))
    dq = int(np.abs(m["n_unique_null"] - m["n_unique"]).max())
    G("G1", d1 < 1e-12 and dq == 0 and len(m) >= 100,
      f"998's committed cells.csv reproduced on ROT: {len(m)} shared cells, max|d| per-leg base "
      f"rate {d1:.2e}, max distinct-draw delta {dq}")

    # G2 998's committed ladder
    pl = pd.read_csv(Path(str(I998).replace(".py", ".ladder.csv")))
    lm = pl.merge(LAD, on=["panel", "book", "gross", "cadence", "cost"], suffixes=("_p", "_m"))
    d2 = float(np.nanmax([np.abs(lm[f"{c}_p"] - lm[f"{c}_m"]).max()
                          for c in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe", "turnover")]))
    G("G2", d2 < 1e-09 and len(lm) == len(pl),
      f"998's committed 900-row ladder reproduced: {len(lm)} of {len(pl)} rows, max|d| {d2:.2e}")

    # G3 Ctx == engine.backtest
    pn = pnl["U56"]
    wr = wt_ = 0.0
    for cad in ("W", "M"):
        Wdf = pd.DataFrame(pn.books[0.75]["TOP20"], index=pn.idx, columns=pn.px.columns)
        eng = backtest(pn.px, Wdf, cost_bps=PROTO_COST, freq=cad)
        r, t = pn.ctx[cad].run(C9.lag_weights(pn.books[0.75]["TOP20"]), PROTO_COST)
        wr = max(wr, float(np.abs(r[pn.warm] - eng["returns"].values[pn.warm]).max()))
        wt_ = max(wt_, float(np.abs(t[pn.warm] - eng["turnover"].values[pn.warm]).max()))
    G("G3", wr < 1e-12 and wt_ < 1e-12,
      f"fast Ctx == engine.backtest on returns AND turnover: {wr:.2e} / {wt_:.2e}")

    # G4 gross and count match on every kind
    G("G4", float(G4.dgross.max()) < 1e-10 and int(G4.dk.max()) == 0,
      f"gross/count match on all {len(G4)} (cell, kind) points: max|dgross| "
      f"{float(G4.dgross.max()):.2e}, max holding-count delta {int(G4.dk.max())}")

    # G5 the rotation dial is monotone, and phi=1 reproduces ROT
    nt = CELL.pivot_table(index=kcols, columns="kind", values="name_turnover")
    mono = int(((nt["ROT"] >= nt["MID"] - 1e-12) & (nt["MID"] >= nt["FIX"] - 1e-12)).sum())
    sub = need[:: max(1, len(need) // GATE_SUBSET)][:GATE_SUBSET]
    dmax = 0.0
    for (pk, bk, g, cad) in sub:
        nd_rot = NULL[(pk, bk, g, cad, "ROT")]
        nd_phi, _, _ = build_null(pnl[pk], pk, bk, g, cad, "PHI1", draws=DRAWS)
        for lg in LEGS:
            dmax = max(dmax, abs(float(nd_rot[lg].mean()) - float(nd_phi[lg].mean())))
    mcse = 3.0 * np.sqrt(0.25 / DRAWS)
    G("G5", mono == len(nt) and dmax <= mcse,
      f"name turnover ROT >= MID >= FIX on {mono} of {len(nt)} cells; the new sampler at "
      f"phi=1.00 reproduces ROT's per-leg base rates on {len(sub)} cells to {dmax:.4f} "
      f"(3 MC SE = {mcse:.4f})")

    # G6 determinism
    k0 = need[0]
    a, _, _ = build_null(pnl[k0[0]], *k0, "FIX", draws=25)
    b2, _, _ = build_null(pnl[k0[0]], *k0, "FIX", draws=25)
    d6 = float(np.nanmax(np.abs(a.select_dtypes(float).values - b2.select_dtypes(float).values)))
    sref = C9.seed_of(SEED0, "U56", "TOP20", 0.75, "W", "FIX", 0)
    G("G6", d6 == 0.0, f"determinism: FIX null rebuilt bit-for-bit, max|d| {d6:.1e} "
                       f"(md5 seeds; reference seed {sref})")

    # G7 SPY OOS triple
    s = pnl["U56"].spy_oos
    d7 = max(abs(s[0] - 0.1521), abs(s[1] - 0.8713), abs(s[2] + 0.3372))
    G("G7", d7 < 5e-3, f"SPY OOS {s[0]:.4f} / {s[1]:.4f} / {s[2]:.4f} vs committed "
                       f"0.1521 / 0.8713 / -0.3372, max|d| {d7:.2e}")

    # G8 the harvest is 998's
    G("G8", C9.harvest.__module__ == "i998" and C9.resolve.__module__ == "i998"
            and C9.draw_null.__module__ == "i998",
      "harvest(), resolve() and draw_null() are imported from idea 998's committed script, "
      "unmodified")

    npass = sum(1 for k in gates if gates[k][0])
    P(f"  GATES: {npass} of {len(gates)} PASS")
    dump(pd.DataFrame(gd), "gates.csv")

    # ============================================================ (B)/(C) THE ANSWER
    P("")
    P("=" * 100)
    P("THE BASE RATES AND THE 0.90 BAR, by NULL KIND")
    P("=" * 100)
    piv = CELL.groupby("kind").agg(
        cells=("panel", "size"),
        med_name_turnover=("name_turnover", "median"),
        med_null_turnover=("null_turnover", "median"),
        med_base4b=("null_base4b", "median"),
        degenerate=("degenerate", "sum"),
        med_n_cert=("n_cert", "median"),
        survive=("survives", "mean")).reindex(KINDS)
    for lg in LEGS:
        piv[f"base_{lg}"] = CELL.groupby("kind")[f"base_{lg}"].median().reindex(KINDS)
        piv[f"noncert_{lg}"] = (CELL.assign(x=~CELL[f"cert_{lg}"])
                                .groupby("kind")["x"].mean().reindex(KINDS))
    P("")
    for line in piv.to_string(float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    P("")
    P("  SURVIVAL OF THE 0.90 BAR, by CLAIM SET x NULL KIND (a pass SURVIVES iff >= 1 of its five")
    P("  legs has a null base rate <= 0.90; a pass with none is UNADJUDICATED):")
    ck = CELL.set_index(kcols + ["kind"])
    srows = []
    for cs in CLAIMSETS:
        cells = claim_cells[cs]
        uniq = sorted({c[:4] for c in cells})
        for kind in KINDS:
            per_cell = [bool(ck.loc[c + (kind,), "survives"]) for c in uniq if c + (kind,) in ck.index]
            per_claim = [bool(ck.loc[c[:4] + (kind,), "survives"]) for c in cells
                         if c[:4] + (kind,) in ck.index]
            ncert = [int(ck.loc[c + (kind,), "n_cert"]) for c in uniq if c + (kind,) in ck.index]
            srows.append(dict(claimset=cs, kind=kind, cells=len(per_cell),
                              survive_cellwt=float(np.mean(per_cell)) if per_cell else np.nan,
                              claims=len(per_claim),
                              survive_claimwt=float(np.mean(per_claim)) if per_claim else np.nan,
                              med_n_cert=float(np.median(ncert)) if ncert else np.nan,
                              unadjudicated=int(sum(1 for x in per_cell if not x))))
    SUR = pd.DataFrame(srows)
    dump(SUR, "survival.csv")
    P("")
    for line in SUR.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)

    # ============================================================ RULE 8, per kind
    P("")
    P("=" * 100)
    P("RULE 8 WALK-FORWARD — PROTOCOL's declared split; IS 2009-2016 ALONE chooses, 2017-2026")
    P("read ONCE.  Run SEPARATELY UNDER EACH NULL KIND, because `C_ISPCT` reads a percentile.")
    P("=" * 100)
    WFS = []
    for kind in KINDS:
        nk = {k[:4]: v for k, v in NULL.items() if k[4] == kind}
        w = C9.walkforward(pnl, LAD, nk, need)
        w["kind"] = kind
        WFS.append(w)
    WF = pd.concat(WFS, ignore_index=True)
    dump(WF, "walkforward.csv")
    P("")
    show = ["kind", "panel", "cadence", "chooser", "book", "gross", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "OOS_pass4b", "OOS_pass4a"]
    for line in WF[show].to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("  " + line)
    P("")
    for kind in KINDS:
        w = WF[WF.kind == kind]
        P(f"  {kind}: OOS 4b {int(w.OOS_pass4b.sum())} of {len(w)};  OOS 4a "
          f"{int(w.OOS_pass4a.sum())} of {len(w)};  best OOS Sharpe "
          f"{w.OOS_Sharpe.max():.4f} (CAGR {w.loc[w.OOS_Sharpe.idxmax(), 'OOS_CAGR']:.2%}, MaxDD "
          f"{w.loc[w.OOS_Sharpe.idxmax(), 'OOS_MaxDD']:.2%})")
    for pk in PANELS:
        p = pnl[pk]
        bo = C9.fmet(p.base_r[PROTO_COST][p.oos])
        P(f"  {pk}: SPY OOS {p.spy_oos[0]:.2%} / {p.spy_oos[1]:.4f} / {p.spy_oos[2]:.2%};  "
          f"RULES v2 live @{PROTO_COST:.0f} bps OOS {bo[0]:.2%} / {bo[1]:.4f} / {bo[2]:.2%}")
    P("  NO BOOK PROMOTED and NO BOOK KEEP CLAIMED: every pick is a ladder book the record")
    P("  already holds.")

    # ============================================================ HYPOTHESES
    P("")
    P("=" * 100)
    P("PRE-REGISTERED HYPOTHESES (bars fixed before any number above the gates was read)")
    P("=" * 100)
    H, hrows = {}, []
    w = CELL.pivot_table(index=kcols, columns="kind",
                         values=[f"base_{lg}" for lg in LEGS] + ["null_base4b", "n_unique"])
    dif = np.concatenate([np.abs(w[(f"base_{lg}", "ROT")] - w[(f"base_{lg}", "FIX")]).values
                          for lg in LEGS])
    H["H_KIND"] = (float(np.median(dif)) <= 0.05,
                   f"median |base_ROT - base_FIX| over {len(dif)} (cell, leg) points = "
                   f"{np.median(dif):.4f} (bar <= 0.05); mean {dif.mean():.4f}, "
                   f"p90 {np.percentile(dif, 90):.4f}, max {dif.max():.4f}.  "
                   f"REPORTED BESIDE THE BAR, because a median over points where BOTH kinds read "
                   f"exactly 0.000 is uninformative: share of points moving > 0.05 = "
                   f"{float((dif > 0.05).mean()):.4f}, > 0.10 = {float((dif > 0.10).mean()):.4f}, "
                   f"> 0.25 = {float((dif > 0.25).mean()):.4f}; share where BOTH kinds read 0.000 = "
                   f"{float(np.mean([(w[(f'base_{lg}','ROT')] == 0) & (w[(f'base_{lg}','FIX')] == 0) for lg in LEGS])):.4f}")

    nondeg = CELL[(CELL.kind == "ROT") & (~CELL.degenerate)].set_index(kcols).index
    hh = [(float(w.loc[i, ("null_base4b", "FIX")]) >= float(w.loc[i, ("null_base4b", "ROT")]))
          for i in nondeg]
    H["H_HARDER"] = (float(np.mean(hh)) >= 0.50,
                     f"FIX 4b base rate >= ROT's in {np.mean(hh):.4f} of {len(hh)} non-degenerate "
                     f"cells (bar >= 0.50); median FIX {w[('null_base4b','FIX')].median():.4f} vs "
                     f"ROT {w[('null_base4b','ROT')].median():.4f}")

    st = SUR[SUR.claimset == "STRICT"].set_index("kind")
    H["H_SURV"] = (bool(st.loc["ROT", "survive_cellwt"] >= 0.50
                        and st.loc["FIX", "survive_cellwt"] >= 0.50),
                   f"STRICT survive share ROT {st.loc['ROT','survive_cellwt']:.4f} / FIX "
                   f"{st.loc['FIX','survive_cellwt']:.4f} (bar >= 0.50 on BOTH); MID "
                   f"{st.loc['MID','survive_cellwt']:.4f}")

    agree = np.concatenate([(CELL[CELL.kind == "ROT"].set_index(kcols)[f"cert_{lg}"]
                             == CELL[CELL.kind == "FIX"].set_index(kcols)[f"cert_{lg}"]).values
                            for lg in LEGS])
    H["H_LEG"] = (float(agree.mean()) >= 0.80,
                  f"the two kinds agree on certify/not for {agree.mean():.4f} of {len(agree)} "
                  f"(cell, leg) points (bar >= 0.80)")

    degcells = CELL[(CELL.kind == "ROT") & CELL.degenerate].set_index(kcols).index
    cured = [int(w.loc[i, ("n_unique", "FIX")]) > C9.DEGEN_BAR * DRAWS for i in degcells]
    H["H_DEGEN"] = (bool(len(cured) and np.mean(cured) >= 0.80),
                    f"FIX gives > {C9.DEGEN_BAR:.0%} distinct draws in "
                    f"{np.mean(cured) if cured else float('nan'):.4f} of the {len(cured)} cells "
                    f"ROT makes degenerate (bar >= 0.80)")

    pk_ = WF[WF.chooser == "C_ISPCT"].pivot_table(index=["panel", "cadence"], columns="kind",
                                                  values=["book", "gross"], aggfunc="first")
    same = [(pk_.loc[i, ("book", "ROT")] == pk_.loc[i, ("book", "FIX")])
            and (pk_.loc[i, ("gross", "ROT")] == pk_.loc[i, ("gross", "FIX")]) for i in pk_.index]
    H["H_RULE8"] = (float(np.mean(same)) >= 0.80,
                    f"C_ISPCT picks the same (book, gross) under ROT and FIX in "
                    f"{np.mean(same):.4f} of {len(same)} (panel, cadence) cells (bar >= 0.80)")

    hp = 0
    for k in ["H_KIND", "H_HARDER", "H_SURV", "H_LEG", "H_DEGEN", "H_RULE8"]:
        ok, msg = H[k]
        hp += int(ok)
        hrows.append(dict(hypothesis=k, verdict="PASS" if ok else "FAIL", detail=msg))
        P(f"  {k:<9} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"  HYPOTHESES: {hp} of {len(H)} PASS")
    dump(pd.DataFrame(hrows), "hypotheses.csv")

    P("")
    P(f"# done in {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.log.txt")


if __name__ == "__main__":
    main()
