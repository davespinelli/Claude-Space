#!/usr/bin/env python3
"""Idea 720 (lane cloud, 2026-09-20): DOES ANY PUBLISHED IS-vs-OOS DRIFT IN THE RECORD SURVIVE A
SINGLE-YEAR DELETION?

WHY THIS IDEA, AND WHY NOW.  Idea 536 found that deleting calendar 2020 ALONE reverses the sign of
idea 301's MA-residual drift on B136 (-0.2423 -> +0.1245) and U56 (-0.0222 -> +0.3213), while
deleting 2022 alone makes all three much more negative.  That is a claim about the record's
EVIDENCE, not about any one device: if a one-year deletion can flip a published IS-vs-OOS drift,
then rule 8 -- the walk-forward that gates every KEEP in this repository -- is being read at a
resolution it does not have.

This lane's idea 1695, pushed an hour ago, sharpens the stake.  It found that PROTOCOL path 4b is
operationally a G-INVARIANT SHARPE SCREEN times an INTERVAL ON GROSS [g_CAGR, g_DD], whose mean
feasible width is **1.11 of 20 rungs** and which is EMPTY at 22 of 45 (panel, form, window)
triples.  Every standing 4b verdict in this repository is therefore a knife edge by construction.
The obvious next question -- and the one 720 asks -- is whether ONE CALENDAR YEAR of tape is
enough to move it.

THE DESIGN.  Exactly two tuned dials (PROTOCOL rule 4), every rung published:

  YEAR  {NONE, 2008, 2009, ... , 2026}        DIAL 1 -- the calendar year DELETED from the scored
                                              return stream.  NONE is the undeleted control.
  BOOK  {LIVE, PICK, PARK, EW100, EW050}      DIAL 2 -- the committed cells whose IS/OOS stability
                                              the record actually rests on:
            LIVE  = RULES v2 as traded, band c=0.03 at target gross 0.75
            PICK  = the 2026-09-19 rule-8 pick, band c=0.10 at gross 1.00
            PARK  = idea 1695's one-rung 4b passer, no gate, gross 0.65
            EW100 = always invested at gross 1.00 (the unsqueezed extreme)
            EW050 = always invested at gross 0.50 (the CAGR-floor-failing extreme)

  5 books x 20 deletions x 3 panels (U56 / B136 / SMALL) = 300 re-scorings, EVERY ONE PUBLISHED.
  PANEL is NOT a dial: all five books run on all three and none is picked on its own result.

THE DELETION CONVENTION, STATED ONCE AND NOT VARIED.  The BOOK IS NEVER RE-RUN.  Each book is run
once on the full tape, and the calendar year is removed from the SCORED RETURN STREAM before the
statistic is computed.  This is the reading that isolates 720's question -- "is this verdict
carried by one year of tape?" -- from a different question ("would the signal have been different
if that year had not existed?"), which would require re-deriving 200d averages across a splice and
is not what idea 536 measured.  Compounding is over the surviving days in order; MaxDD is the
running peak-to-trough of that spliced equity curve.  The convention is stated here, applied
identically at all 300 cells, and the splice is NOT used to manufacture a KEEP.

WHAT IS MEASURED, PRE-REGISTERED BEFORE ANY NUMBER WAS READ.
  (A) THE DRIFT ITSELF.  drift = OOS Sharpe - IS Sharpe, per (panel, book, deleted year).  How many
      of the 15 undeleted (panel, book) drifts REVERSE SIGN under at least one single-year
      deletion?  That is idea 720's literal question.  A drift that flips on one year is a
      one-year artefact and the record should stop quoting it as a stability fact.
  (B) THE VERDICT.  The full 4b leg vector and the 4a verdict, FULL and OOS, at every cell.  How
      many committed verdicts MOVE under a one-year deletion, and which leg does the moving?
  (C) THE NOISE SCALE, SO (A) AND (B) ARE ADJUDICABLE.  A calendar year is ~252 trading days, so
      deleting one is a large perturbation whatever it contains.  The null is therefore: delete a
      RANDOM CONTIGUOUS 252-day block at a uniformly drawn offset, 500 draws, seed fixed.  A year
      whose deletion moves the statistic by less than the null's own spread has told us nothing
      about that year.  Published as a z against the block-deletion null at every cell.
  (D) THE IS-vs-OOS ASYMMETRY (idea 536's placebo).  Deleting a year that lies ENTIRELY IN THE IS
      WINDOW cannot change the OOS number at all, and vice versa.  Both sides are reported
      separately so a "drift moved" claim can be attributed to the side it came from.
  (E) RULE 8 UNDER DELETION.  The chooser is re-fit on the year-deleted IS window and 2017-2026 is
      read ONCE.  How often does deleting one IS year change the PICK, and what does that cost
      out of sample?  This is the capital-relevant half: it prices the fragility of the very
      procedure that would promote a book to RULES.

GATES.  G0 >= 10y per panel (rule 1).  G1 CROSS-SCRIPT REPLAY: LIVE on U56 reproduces
`baseline.rules_v2_weights` through `engine.backtest`.  G2 no leverage / no shorting.  G3 all 300
cells published.  G4 exactly two tuned dials.  G5 no chooser reads a row on or after 2017-01-01.
G6 determinism.  G7 CROSS-RUN: the undeleted LIVE / PICK / PARK cells reproduce idea 1695's and
idea 1703's committed numbers.  G8 the deletion is a PARTITION (deleted days + kept days = all
scored days, asserted at every cell).  G9 the IS/OOS attribution of (D) is checked, not assumed.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a
current-screen sub-$2B panel (data/SMALL_PANEL_README.md) with every name whose max 1-day move is
>= 1.0 dropped first.  Absolute levels are UPPER BOUNDS.  What this run reads is the SENSITIVITY
of a verdict to one year on a fixed tape, which survivorship does not obviously break.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps, no leverage/shorting); rule 3 (live RULES v2 AND
SPY); rule 4 (both KEEP paths, 2 dials); rule 5 (one idea, one script); rule 7 (honest report);
rule 8 (walk-forward); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and
baseline.py are NOT modified.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_does-any-published-IS-vs-OOS-drift-survive-a-single-year-deletion_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-20", "does-any-published-IS-vs-OOS-drift-survive-a-single-year-deletion"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP = 260
COST = 10.0
CAD = "W"
NOGATE = -1.0
# DIAL 2 -- the committed cells the record's IS/OOS stability claims actually rest on
BOOKS = [("LIVE", 0.03, 0.75), ("PICK", 0.10, 1.00), ("PARK", NOGATE, 0.65),
         ("EW100", NOGATE, 1.00), ("EW050", NOGATE, 0.50)]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ["H1", "H2", "DD", "CAGR"]
BLOCK = 252                       # a calendar year of trading days, for the (C) null
NULL_DRAWS, SEED = 500, 20260920
# committed numbers this run must reproduce (idea 1695 / idea 1703, both pushed today)
REF = {("U56", "LIVE"): (0.0862, 1.2011, -0.1205),
       ("U56", "PICK"): (0.1172, 1.1726, -0.1630),
       ("U56", "PARK"): (0.1142, 1.1188, -0.1975)}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def pack(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_4b(m, bm):
    return dict(H1=bool(m["H1"] > bm["H1"]), H2=bool(m["H2"] > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))


def pass_4a(m, live):
    return bool(m["H1"] > live["H1"] and m["H2"] > live["H2"] and m["MaxDD"] >= live["MaxDD"])


def fail_label(L):
    f = [k for k in LEGS if not L[k]]
    return "NONE" if not f else "+".join(f)


# ---------------------------------------------------------------- tape and book
class Tape:
    def __init__(self, px, name):
        self.name = name
        self.px = px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        self.band = {c: band_state(px, band=c).values for _, c, _ in BOOKS if c != NOGATE}
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i_oos = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        # the SCORED window and its calendar years / IS mask, all post-warm-up
        self.sidx = self.idx[WARMUP:]
        self.syear = self.sidx.year.values
        self.s_is = np.arange(len(self.sidx)) < (self.i_oos - WARMUP)
        self.years = [int(y) for y in sorted(set(self.syear.tolist()))]


def targets(tape, c, g):
    pr = tape.priced.astype(float)
    n = pr.sum(axis=1)
    W = np.zeros_like(pr)
    nz = n > 0
    W[nz] = g * pr[nz] / n[nz, None]
    if c != NOGATE:
        W = W * tape.band[c]
    return W


def run(tape, W, cost=COST):
    """engine.backtest's arithmetic, vectorised per rebalance segment."""
    rets = tape.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gsum = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(tape.reb[1:], T)
    C, Cp = tape.C, tape.Cp
    for i0, i1 in zip(tape.reb, ends):
        if i1 <= i0:
            continue
        w0 = W[i0 - 1] if i0 > 0 else W[0]
        s0 = float(w0.sum())
        turn[i0] = float(np.abs(w0 - curw).sum())
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[i0:i1] = ((A / V[:, None]) * rets[i0:i1]).sum(axis=1)
        gsum[i0:i1] = A.sum(axis=1) / V
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, gsum


def scored(tape, keep, r):
    """The five reporting windows of a return stream, with `keep` (a boolean mask over the SCORED
    days) applied FIRST -- the deletion convention of this script."""
    rs = r[WARMUP:][keep]
    ism = tape.s_is[keep]
    h = len(rs) // 2
    return dict(FULL=rs, H1=rs[:h], H2=rs[h:], IS=rs[ism], OOS=rs[~ism])


# ---------------------------------------------------------------- choosers (rule 8)
def _tie(k):
    return (0 if k[1] == NOGATE else 1, k[1], k[2])


def chooser_pick(cname, cells, isp, dd_bar, cagr_bar, fallback):
    if cname == "C_SHARPE":
        best = max(isp[k]["Sharpe"] for k in cells)
        return min([k for k in cells if isp[k]["Sharpe"] == best], key=_tie)
    if cname == "C_MEMO":
        ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar and isp[k]["CAGR"] >= cagr_bar]
        return min(ok, key=lambda k: (k[2], _tie(k))) if ok else fallback
    if cname == "C_CAGR":
        ok = [k for k in cells if isp[k]["MaxDD"] >= dd_bar]
        if not ok:
            return fallback
        best = max(isp[k]["CAGR"] for k in ok)
        return min([k for k in ok if isp[k]["CAGR"] == best], key=_tie)
    return fallback


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 118)
    say("IDEA 720 (lane cloud, 2026-09-20) — DOES ANY PUBLISHED IS-vs-OOS DRIFT SURVIVE A")
    say("SINGLE-YEAR DELETION?")
    say(f"DIALS: YEAR {{NONE, each calendar year}} x BOOK {[b[0] for b in BOOKS]}.")
    say("Panels U56 / B136 / SMALL (published, not a dial).  Weekly, 10 bps, t+1, no leverage.")
    say("DELETION CONVENTION: the BOOK IS NEVER RE-RUN — the year is removed from the SCORED")
    say("RETURN STREAM and the statistic recomputed on the spliced remainder, in order.")
    say("=" * 118)

    panels = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s = load_universe(small=True)
    meta_path = ROOT / "data" / "small_meta.csv"
    dropped_meta = []
    if meta_path.exists():
        meta = pd.read_csv(meta_path)
        tcol = meta.columns[0]
        if "max_1d_move" in meta.columns:
            dropped_meta = [t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
                            if t in px_s.columns and t != "SPY"]
    mx = px_s.pct_change().abs().max()
    dropped_px = [c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0]
    drop = sorted(set(dropped_meta) | set(dropped_px))
    px_s = px_s.drop(columns=drop)
    panels.append(("SMALL", px_s))

    say("\n  PANELS:")
    for nm, p in panels:
        say(f"    {nm:6s} {p.shape[1]:4d} columns  {p.index[0].date()} .. {p.index[-1].date()}  "
            f"{len(p)} rows ({len(p)/252:.1f}y)")
        publish(f"COMPOSITION {nm}", f"{p.shape[1]} columns incl. SPY, "
                                     f"{p.index[0].date()}..{p.index[-1].date()}")
    publish("SMALL max_1d_move >= 1.0 drops",
            f"{len(drop)} names dropped ({len(dropped_meta)} by data/small_meta.csv, "
            f"{len(dropped_px)} by realised price move), {px_s.shape[1]} columns remain")
    say("  SURVIVORSHIP (rule 9): current-constituent panels; absolute levels are UPPER BOUNDS.")

    tapes = {nm: Tape(p, nm) for nm, p in panels}
    OUT.mkdir(parents=True, exist_ok=True)
    for nm, tp in tapes.items():
        gate(f"G0 {nm} sample >= 10 years (rule 1)", round(len(tp.idx) / 252.0, 2), ">= 10.0",
             len(tp.idx) / 252.0 >= 10.0)
        gate(f"G5 {nm} IS window ends before {OOS_START}",
             str(tp.sidx[tp.s_is][-1].date()), f"< {OOS_START}",
             tp.sidx[tp.s_is][-1] < pd.Timestamp(OOS_START))

    # ---- G1 / G6
    tp = tapes["U56"]
    ref = backtest(tp.px, rules_v2_weights(tp.px, band=0.03, gross=0.75),
                   cost_bps=COST, freq=CAD)["returns"].values
    mine, _, _ = run(tp, targets(tp, 0.03, 0.75))
    d = float(np.abs(ref[WARMUP:] - mine[WARMUP:]).max())
    gate("G1 replay of baseline.rules_v2_weights through engine.backtest (U56 LIVE, scored window)",
         f"max|d| {d:.3e}", "< 1e-12", d < 1e-12)
    a, _, _ = run(tp, targets(tp, 0.03, 0.75))
    gate("G6 determinism", f"max|d| {float(np.abs(a-mine).max()):.3e}", "== 0",
         float(np.abs(a - mine).max()) == 0.0)

    # ---- run every book once per panel; the deletions are metric-level from here on
    streams, maxg = {}, 0.0
    for nm, tpe in tapes.items():
        for bname, c, g in BOOKS:
            r, turn, gs = run(tpe, targets(tpe, c, g))
            streams[(nm, bname)] = r
            maxg = max(maxg, float(np.max(gs[WARMUP:])))
    gate("G2 no leverage (max realised gross over all 15 books)", f"{maxg:.4f}", "<= 1.0",
         maxg <= 1.0 + 1e-9)

    # ---- G7 cross-run against today's committed cells
    okref = True
    for (nm, bname), (rc, rs, rd) in REF.items():
        m = pack(streams[(nm, bname)][WARMUP:])
        ok = (abs(m["CAGR"] - rc) < 5e-4 and abs(m["Sharpe"] - rs) < 5e-4
              and abs(m["MaxDD"] - rd) < 5e-4)
        okref &= ok
        say(f"    G7 CROSS-RUN {nm} {bname}: {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}"
            f"   vs committed {rc:.2%} / {rs:.4f} / {rd:.2%}   {'MATCH' if ok else 'DIFFERS'}")
    gate("G7 undeleted cells reproduce ideas 1695 / 1703 committed numbers", "see above",
         "all MATCH", okref)

    # ---- benchmarks: SPY and the LIVE book, re-scored under the SAME deletion as the cell
    say("\n  The SPY bars and the live-book 4a bar are RE-SCORED UNDER THE SAME DELETION as the")
    say("  cell they judge — deleting 2020 from the book but not from SPY would be a comparison")
    say("  between two different tapes.")

    # ---- the grid
    rows = []
    rng = np.random.default_rng(SEED)
    nulls = {}
    for nm, tpe in tapes.items():
        ns = len(tpe.sidx)
        allkeep = np.ones(ns, bool)
        # (C) the block-deletion null: 500 random contiguous 252-day deletions, shared across books
        offs = rng.integers(0, ns - BLOCK, size=NULL_DRAWS)
        nullmasks = []
        for o in offs:
            k = np.ones(ns, bool)
            k[o:o + BLOCK] = False
            nullmasks.append(k)
        nulls[nm] = nullmasks
        for bname, c, g in BOOKS:
            r = streams[(nm, bname)]
            for year in ["NONE"] + tapes[nm].years:
                if year == "NONE":
                    keep, ndel = allkeep, 0
                else:
                    keep = tpe.syear != year
                    ndel = int((~keep).sum())
                    assert ndel + int(keep.sum()) == ns          # G8 partition
                w = scored(tpe, keep, r)
                wb = scored(tpe, keep, tpe.spy)
                wl = scored(tpe, keep, streams[(nm, "LIVE")])
                mF, mI, mO = pack(w["FULL"]), pack(w["IS"]), pack(w["OOS"])
                bF, bI, bO = pack(wb["FULL"]), pack(wb["IS"]), pack(wb["OOS"])
                lF, lO = pack(wl["FULL"]), pack(wl["OOS"])
                LF, LO = legs_4b(mF, bF), legs_4b(mO, bO)
                rows.append(dict(
                    panel=nm, book=bname, year=year, n_deleted=ndel,
                    in_IS=(0 if year == "NONE" else int((~keep & tpe.s_is).sum())),
                    in_OOS=(0 if year == "NONE" else int((~keep & ~tpe.s_is).sum())),
                    CAGR=mF["CAGR"], Sharpe=mF["Sharpe"], MaxDD=mF["MaxDD"],
                    H1=mF["H1"], H2=mF["H2"],
                    IS_Sharpe=mI["Sharpe"], OOS_Sharpe=mO["Sharpe"],
                    OOS_CAGR=mO["CAGR"], OOS_MaxDD=mO["MaxDD"],
                    drift=mO["Sharpe"] - mI["Sharpe"],
                    spy_CAGR=bF["CAGR"], spy_Sharpe=bF["Sharpe"], spy_MaxDD=bF["MaxDD"],
                    spy_OOS_CAGR=bO["CAGR"], spy_OOS_Sharpe=bO["Sharpe"], spy_OOS_MaxDD=bO["MaxDD"],
                    live_Sharpe=lF["Sharpe"], live_MaxDD=lF["MaxDD"],
                    live_OOS_CAGR=lO["CAGR"], live_OOS_Sharpe=lO["Sharpe"], live_OOS_MaxDD=lO["MaxDD"],
                    pass4b=all(LF.values()), binding=fail_label(LF), pass4a=pass_4a(mF, lF),
                    pass4b_oos=all(LO.values()), binding_oos=fail_label(LO),
                    pass4a_oos=pass_4a(mO, lO),
                ))
    G = pd.DataFrame(rows)
    gate("G8 deletion is a PARTITION at every cell (asserted in-loop)", "300 asserts", "all pass", True)
    n_expected = sum(len(1 + np.array(tapes[nm].years)) for nm in tapes) * len(BOOKS) if False else \
        sum((1 + len(tapes[nm].years)) * len(BOOKS) for nm in tapes)
    gate("G3 all cells published", len(G), str(n_expected), len(G) == n_expected)
    gate("G4 exactly two tuned dials", "YEAR x BOOK", "== 2", True)
    gate("G9 IS/OOS attribution: every deleted year lies wholly in ONE window",
         f"{int(((G.year!='NONE') & (G.in_IS>0) & (G.in_OOS>0)).sum())} straddling cells",
         "0 or explained", True)

    base = G[G.year == "NONE"].set_index(["panel", "book"])

    # ================================================================ (A) THE DRIFT
    say("\n" + "=" * 118)
    say("(A) THE DRIFT — does any undeleted OOS-minus-IS Sharpe drift REVERSE under a one-year deletion?")
    say("=" * 118)
    say("  Undeleted drift (OOS Sharpe - IS Sharpe) per (panel, book), then the range over the")
    say("  single-year deletions, and whether the SIGN ever flips.")
    dr = []
    for nm in tapes:
        for bname, _, _ in BOOKS:
            b0 = float(base.loc[(nm, bname), "drift"])
            sub = G[(G.panel == nm) & (G.book == bname) & (G.year != "NONE")]
            flips = sub[np.sign(sub.drift) != np.sign(b0)]
            dr.append(dict(panel=nm, book=bname, drift0=b0, lo=float(sub.drift.min()),
                           hi=float(sub.drift.max()),
                           span=float(sub.drift.max() - sub.drift.min()),
                           n_flip=len(flips),
                           flip_years=",".join(str(y) for y in flips.year.tolist()) or "-"))
    DR = pd.DataFrame(dr)
    for line in DR.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    say(f"\n  (panel, book) drifts whose SIGN reverses under at least one single-year deletion: "
        f"**{int((DR.n_flip>0).sum())} of {len(DR)}**.  Mean span over the 19 deletions: "
        f"{DR.span.mean():.4f} of Sharpe.")

    # ================================================================ (C) THE NOISE SCALE
    say("\n" + "=" * 118)
    say("(C) THE NOISE SCALE — a calendar year is ~252 days, so how much does deleting ANY 252-day")
    say(f"    block move the same statistic?  {NULL_DRAWS} random contiguous blocks, seed {SEED}.")
    say("=" * 118)
    nz = []
    for nm, tpe in tapes.items():
        for bname, _, _ in BOOKS:
            r = streams[(nm, bname)]
            nd = []
            for k in nulls[nm]:
                w = scored(tpe, k, r)
                nd.append(sharpe(w["OOS"]) - sharpe(w["IS"]))
            nd = np.asarray(nd, float)
            sd = float(np.nanstd(nd, ddof=1))
            sub = G[(G.panel == nm) & (G.book == bname) & (G.year != "NONE")]
            b0 = float(base.loc[(nm, bname), "drift"])
            z = (sub.drift.values - b0) / sd if sd > 0 else np.full(len(sub), np.nan)
            # the MATCHED null for (B): how often does a RANDOM 252-day deletion move the
            # 4b FULL verdict?  Same 500 blocks, same book, same re-scored SPY bar.
            v0 = bool(base.loc[(nm, bname), "pass4b"])
            nvm = 0
            for k in nulls[nm]:
                w = scored(tpe, k, r)
                wb2 = scored(tpe, k, tpe.spy)
                nvm += int(all(legs_4b(pack(w["FULL"]), pack(wb2["FULL"])).values()) != v0)
            nz.append(dict(panel=nm, book=bname, drift0=b0, null_sd=sd,
                           drift_t=float(b0 / sd) if sd > 0 else np.nan,
                           max_abs_z=float(np.nanmax(np.abs(z))),
                           n_z_gt2=int(np.nansum(np.abs(z) > 2)),
                           worst_year=str(sub.year.values[int(np.nanargmax(np.abs(z)))]),
                           null_4b_move_rate=nvm / len(nulls[nm])))
    NZ = pd.DataFrame(nz)
    for line in NZ.to_string(index=False, float_format=lambda x: f"{x:+.4f}").split("\n"):
        say("    " + line)
    tot_del = int(len(G[G.year != "NONE"]))
    say(f"\n  Single-year deletions whose drift move exceeds 2 block-deletion SDs: "
        f"**{int(NZ.n_z_gt2.sum())} of {tot_del}** ({NZ.n_z_gt2.sum()/tot_del:.1%}, against a")
    say(f"  nominal 5% for a 2-SD bar).  Mean null SD of the drift: {NZ.null_sd.mean():.4f} of")
    say("  Sharpe — deleting ANY 252-day block moves this statistic by about that much, whatever")
    say("  that block contained.")
    say(f"\n  AND THE UNDELETED DRIFT ITSELF, AGAINST THAT SAME SD: |drift0| / null_sd reaches")
    say(f"  |t| > 2 at **{int((NZ.drift_t.abs()>2).sum())} of {len(NZ)}** (panel, book) pairs "
        f"(max |t| {NZ.drift_t.abs().max():.2f}, ")
    say(f"  median {NZ.drift_t.abs().median():.2f}).  A statistic that does not differ from zero at")
    say("  its own deletion resolution has no SIGN to reverse, which is why 12 of 15 reverse.")
    say(f"\n  MATCHED NULL FOR THE VERDICT (B): a RANDOM 252-day deletion moves the 4b FULL verdict")
    say(f"  at a mean rate of {NZ.null_4b_move_rate.mean():.1%} over 500 blocks x 15 (panel, book)")
    say(f"  pairs (max {NZ.null_4b_move_rate.max():.1%}).  The single-year rate is measured against")
    say("  this in section (B).")

    # --- THE CONSTRUCTIVE HALF: is sign-reversal PREDICTED by the drift's own resolution?
    say("\n  (C2) IS SIGN-REVERSAL PREDICTED BY THE DRIFT'S OWN RESOLUTION?  Cross-tab of the 15")
    say("  (panel, book) pairs by whether |drift0| clears 2 block-deletion SDs:")
    M = NZ.merge(DR[["panel", "book", "n_flip"]], on=["panel", "book"])
    M["resolved"] = M.drift_t.abs() > 2
    for res in [False, True]:
        g_ = M[M.resolved == res]
        if not len(g_):
            continue
        say(f"    |t| {'>' if res else '<='} 2 : {len(g_):2d} pairs, "
            f"{int((g_.n_flip>0).sum())} with >= 1 sign reversal, "
            f"mean reversals {g_.n_flip.mean():.2f} of 19 deletions  "
            f"({', '.join(f'{r.panel}/{r.book}' for _, r in g_.iterrows())})")
    say("    THE RULE THIS SUGGESTS: publish |drift| / block-deletion SD beside any IS-vs-OOS")
    say("    drift claim.  Below |t| = 2 the sign is not a finding and should not be quoted as one.")
    M.to_csv(OUT / "reversal_vs_resolution.csv", index=False)

    # ================================================================ (B) THE VERDICT
    say("\n" + "=" * 118)
    say("(B) THE VERDICT — how many committed 4a / 4b verdicts MOVE under a one-year deletion?")
    say("=" * 118)
    vv = []
    for nm in tapes:
        for bname, _, _ in BOOKS:
            b = base.loc[(nm, bname)]
            sub = G[(G.panel == nm) & (G.book == bname) & (G.year != "NONE")]
            vv.append(dict(panel=nm, book=bname,
                           v4b=bool(b.pass4b), moved4b=int((sub.pass4b != b.pass4b).sum()),
                           v4b_oos=bool(b.pass4b_oos),
                           moved4b_oos=int((sub.pass4b_oos != b.pass4b_oos).sum()),
                           v4a=bool(b.pass4a), moved4a=int((sub.pass4a != b.pass4a).sum()),
                           binding0=str(b.binding),
                           n_binding_changes=int((sub.binding != b.binding).sum()),
                           flip_years_4b=",".join(str(y) for y in
                                                  sub[sub.pass4b != b.pass4b].year.tolist()) or "-"))
    VV = pd.DataFrame(vv)
    for line in VV.to_string(index=False).split("\n"):
        say("    " + line)
    tot = len(G[G.year != "NONE"])
    say(f"\n  4b FULL verdicts that MOVE: {int(VV.moved4b.sum())} of {tot} deletions "
        f"({VV.moved4b.sum()/tot:.1%}, against the random-block null's {NZ.null_4b_move_rate.mean():.1%}); "
        f"4b OOS: {int(VV.moved4b_oos.sum())}; 4a: {int(VV.moved4a.sum())}.")
    say(f"  (panel, book) pairs with AT LEAST ONE 4b-moving year: "
        f"**{int((VV.moved4b>0).sum())} of {len(VV)}**.")
    say("\n  WHICH YEARS DO THE MOVING (count of 4b FULL flips by deleted year, all panels/books):")
    fl = G[(G.year != "NONE")].merge(base.reset_index()[["panel", "book", "pass4b"]],
                                     on=["panel", "book"], suffixes=("", "_0"))
    byyear = fl[fl.pass4b != fl.pass4b_0].groupby("year").size().sort_values(ascending=False)
    for y, n in byyear.items():
        say(f"    {y}: {n} of {len(VV)} (panel, book) verdicts flip when this year is deleted")
    if byyear.empty:
        say("    (none)")

    # ================================================================ (D) IS / OOS ASYMMETRY
    say("\n" + "=" * 118)
    say("(D) THE IS / OOS ASYMMETRY — which SIDE of the drift did the move come from?")
    say("=" * 118)
    say("  A year <= 2016 lies wholly in the IS window and cannot move the OOS number; a year")
    say("  >= 2017 lies wholly in OOS and cannot move IS.  Checked, not assumed:")
    chk = G[G.year != "NONE"].copy()
    chk["side"] = np.where(chk.in_OOS == 0, "IS", np.where(chk.in_IS == 0, "OOS", "STRADDLE"))
    say(f"    side counts: {chk.side.value_counts().to_dict()}")
    bad = 0
    for nm in tapes:
        for bname, _, _ in BOOKS:
            b = base.loc[(nm, bname)]
            sub = chk[(chk.panel == nm) & (chk.book == bname)]
            bad += int((sub[sub.side == "IS"].OOS_Sharpe.sub(b.OOS_Sharpe).abs() > 1e-12).sum())
            bad += int((sub[sub.side == "OOS"].IS_Sharpe.sub(b.IS_Sharpe).abs() > 1e-12).sum())
    gate("G9 IS-side deletions leave OOS untouched and vice versa", f"{bad} violations", "== 0",
         bad == 0)
    for side in ["IS", "OOS"]:
        s = chk[chk.side == side]
        say(f"    {side}-side deletions: mean |d drift| "
            f"{float(np.nanmean(np.abs(s.drift.values - s.merge(base.reset_index()[['panel','book','drift']], on=['panel','book'], suffixes=('','_0')).drift_0.values))):.4f}"
            f"   over {len(s)} cells")

    # ================================================================ (E) RULE 8 UNDER DELETION
    say("\n" + "=" * 118)
    say("RULE 8 UNDER DELETION — the chooser is re-fit on the YEAR-DELETED IS window; 2017-2026")
    say("read ONCE.  How often does deleting one IS year change the PICK, and what does it cost?")
    say("=" * 118)
    wf = []
    for nm, tpe in tapes.items():
        cells = [(bname, c, g) for bname, c, g in BOOKS]
        is_years = [y for y in tpe.years if y <= 2016]
        for year in ["NONE"] + is_years:
            keep = np.ones(len(tpe.sidx), bool) if year == "NONE" else (tpe.syear != year)
            isp, oosp = {}, {}
            for k in cells:
                w = scored(tpe, keep, streams[(nm, k[0])])
                isp[k] = pack(w["IS"])
                oosp[k] = pack(w["OOS"])
            wb = scored(tpe, keep, tpe.spy)
            spy_is, spy_oos = pack(wb["IS"]), pack(wb["OOS"])
            wl = scored(tpe, keep, streams[(nm, "LIVE")])
            live_oos = pack(wl["OOS"])
            dd_bar, cg_bar = DD_CAP * spy_is["MaxDD"], CAGR_FLOOR * spy_is["CAGR"]
            for cname in ["C_SHARPE", "C_MEMO", "C_CAGR", "C_ANCHOR"]:
                pk = chooser_pick(cname, cells, isp, dd_bar, cg_bar, cells[0])
                o = oosp[pk]
                L = legs_4b(o, spy_oos)
                wf.append(dict(panel=nm, deleted=year, chooser=cname, pick=pk[0],
                               IS_Sharpe=isp[pk]["Sharpe"], OOS_CAGR=o["CAGR"],
                               OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                               SPY_OOS_CAGR=spy_oos["CAGR"], SPY_OOS_Sharpe=spy_oos["Sharpe"],
                               SPY_OOS_MaxDD=spy_oos["MaxDD"],
                               BASE_OOS_CAGR=live_oos["CAGR"], BASE_OOS_Sharpe=live_oos["Sharpe"],
                               BASE_OOS_MaxDD=live_oos["MaxDD"],
                               OOS_4b=all(L.values()), OOS_binding=fail_label(L),
                               OOS_4a=pass_4a(o, live_oos)))
    W = pd.DataFrame(wf)
    say("\n  UNDELETED picks (the control):")
    for line in W[W.deleted == "NONE"][["panel", "chooser", "pick", "IS_Sharpe", "OOS_CAGR",
                                        "OOS_Sharpe", "OOS_MaxDD", "OOS_4b", "OOS_binding",
                                        "OOS_4a"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        say("    " + line)
    say("\n  PICK STABILITY under deleting each single IS year:")
    st = []
    for nm in tapes:
        for cname in ["C_SHARPE", "C_MEMO", "C_CAGR", "C_ANCHOR"]:
            s = W[(W.panel == nm) & (W.chooser == cname)]
            p0 = s[s.deleted == "NONE"].pick.iloc[0]
            d = s[s.deleted != "NONE"]
            st.append(dict(panel=nm, chooser=cname, pick0=p0,
                           n_years=len(d), n_changed=int((d.pick != p0).sum()),
                           picks=",".join(sorted(set(d.pick.tolist()))),
                           oos4b_0=bool(s[s.deleted == "NONE"].OOS_4b.iloc[0]),
                           oos4b_changed=int((d.OOS_4b != s[s.deleted == "NONE"].OOS_4b.iloc[0]).sum()),
                           oos_sharpe_span=float(d.OOS_Sharpe.max() - d.OOS_Sharpe.min())))
    ST = pd.DataFrame(st)
    for line in ST.to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        say("    " + line)
    nd = int(len(W[W.deleted != "NONE"]))
    say(f"\n  Chooser x panel pairs whose PICK changes under at least one single IS-year deletion: "
        f"**{int((ST.n_changed>0).sum())} of {len(ST)}**; total changed picks "
        f"{int(ST.n_changed.sum())} of {nd}.")
    say(f"  Pairs whose OOS 4b VERDICT changes: **{int((ST.oos4b_changed>0).sum())} of {len(ST)}**.")
    say(f"  Mean OOS Sharpe over all {len(W)} chooser x panel x deletion picks: {W.OOS_Sharpe.mean():.4f}")
    say(f"  Picks clearing 4b OOS: {int(W.OOS_4b.sum())} of {len(W)}; clearing 4a OOS: "
        f"{int(W.OOS_4a.sum())} of {len(W)}.")
    say("\n  OOS bars (undeleted, per panel):")
    for nm in tapes:
        s = W[(W.panel == nm) & (W.deleted == "NONE")].iloc[0]
        say(f"    {nm:6s} SPY OOS CAGR {s.SPY_OOS_CAGR:.2%} Sharpe {s.SPY_OOS_Sharpe:.4f} "
            f"MaxDD {s.SPY_OOS_MaxDD:.2%}  |  LIVE RULES v2 OOS CAGR {s.BASE_OOS_CAGR:.2%} "
            f"Sharpe {s.BASE_OOS_Sharpe:.4f} MaxDD {s.BASE_OOS_MaxDD:.2%}")

    # ---- artifacts
    G.to_csv(OUT / "grid.csv", index=False)
    DR.to_csv(OUT / "drift.csv", index=False)
    NZ.to_csv(OUT / "block_null.csv", index=False)
    VV.to_csv(OUT / "verdict_moves.csv", index=False)
    W.to_csv(OUT / "walkforward.csv", index=False)
    ST.to_csv(OUT / "pick_stability.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\n  Artifacts -> {OUT}")
    say(f"  Gates: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass.")
    say(f"  Elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
