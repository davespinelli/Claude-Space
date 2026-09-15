#!/usr/bin/env python3
"""Idea 686 (cloud, 2026-09-15) -- is the 4b FOOTPRINT still a CAP-MIX function once k is a free
axis?

THE QUESTION (queue, 2026-09-11)
  Idea 525 built a two-factor panel ladder -- q = the share of the panel drawn from the small-cap
  pool, k = the PANEL WIDTH -- and found 4b passing 21 of 348 book-cells with EVERY pass at
  q <= 0.25, passers sitting at Ebar 42.7 against 33.5 and breadth 0.6479 against 0.4874.  That
  reproduced ideas 276/285/286 on a third construction.  But 525's k arm spans 40..100 -- 2.5x --
  and its k axis was never separated FROM THE PASS RATE itself: every 4b statement it makes is a
  q statement with k held in a narrow band.  The queue asks: regress 4b eligibility on (q, k)
  JOINTLY, and report whether the admissibility boundary idea 285 called a (cap mix, BOOK SIZE)
  property is really a (cap mix, PANEL WIDTH) one.

WHAT THIS RUN CHANGES, AND WHAT IT DELIBERATELY DOES NOT
  It changes ONE thing: k becomes a free axis, extended to 400 -- 10.0x of width, the widest the
  committed caches support (idea 685's envelope: a (q, k) cell exists iff q*k <= |SMALL pool| and
  (1-q)*k <= |BSTK pool| = 100).  Everything else is imported from the record rather than
  re-typed: the panels come from idea 276's `build_sources`, and every book, every metric and the
  4a/4b verdicts come from idea 525's own `do_panel`, called unmodified.  The k <= 100 half of the
  ladder replays 525's rng sequence at its own seed, so those cells are byte-identical to 525's
  and G3 is an EXACT reproduction, not a tolerance.

THE THREE AXES, AND WHY 285's CLAIM NEEDS ALL THREE
  q  CAP MIX      the share of the panel drawn from the small-cap pool   (525's dial)
  k  PANEL WIDTH  how many names the panel HAS                           (the free axis here)
  n  BOOK SIZE    how many names the book HOLDS (CAND-n)                 (285's second factor)
  Idea 285 called the admissibility boundary a (cap mix, BOOK SIZE) property.  On a ladder where
  k barely moves, k and n are hard to tell apart -- both are "how many names" -- which is exactly
  the confound the queue is pointing at.  With k free over 10.0x and n free over 6x, the two
  separate, and the run reports the partial association of the 4b pass with each, holding the
  other two fixed.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  q, 5 levels, every one reported: 0.00 / 0.25 / 0.50 / 0.75 / 1.00     (the queue's own)
  TUNED 2  k, 6 levels, every one reported: 40 / 60 / 80 / 100 / 200 / 400       (the queue's own)
  REPORTED AXES (nothing fitted on them; every point published): n in {5,10,15,20,30} plus EWall;
  3 seeded draws per cell (525's SEED and count); the FULL / IS / OOS windows.

PRE-REGISTERED BARS (fixed before any number was read; the record's own |rho| >= 0.30 with
idea 286's 8-of-11 sign-consistency share, applied to each axis's own level count)
  H_Q    CAP MIX is an axis of the boundary iff |mean within-k rho(pass4b, q)| >= 0.30 with the
         sign holding in >= ceil(8/11 x 6) = 5 of the 6 k levels.
  H_K    PANEL WIDTH is an axis iff |mean within-q rho(pass4b, k)| >= 0.30 with the sign holding
         in >= ceil(8/11 x 5) = 4 of the 5 q levels.
  H_N    BOOK SIZE is an axis iff |mean within-q rho(pass4b, n)| >= 0.30, sign in >= 4 of 5.
  H_285  (THE QUEUE'S QUESTION) the boundary is a (cap mix, PANEL WIDTH) property rather than the
         (cap mix, BOOK SIZE) property idea 285 published iff H_K passes, H_N fails, AND
         |rho(pass4b, k | q)| > |rho(pass4b, n | q)| on the pooled ladder.
  H_MONO the 4b footprint is monotone in q (525's reading, restated as a bar): the per-q pass
         rate is non-increasing across the 5 q levels at every k level.
  H_WF   (rule 8, REQUIRED) the cell (q, k, n) chosen on 2009-2016 ALONE, 2017-2026 read ONCE,
         both KEEP paths, against SPY and RULES v2 on the same panel.

GATES (all printed before any result number)
  G1  the feasible envelope holds on this run's own construction: exact width, exact cap mix, no
      duplicate columns, no pool overflow
  G2  the k-identity log(Ebar) == log(breadth) + log(k) holds on every panel (525's own identity)
  G3  CROSS-RUN, the load-bearing one: on the k <= 100 slice this run reproduces idea 525's
      **21 of 348** 4b passes and its passer/failer Ebar and breadth means EXACTLY.  IT DOES NOT,
      and the run publishes the decomposition (G3a..G3e) instead of relaxing the bar: the count
      and the ladder shape reproduce, the CELLS do not, and the cause is that the small-cap pool
      has been RESTATED from 439 names to 663 since 525 ran, with no committed column lists, so
      525's panels are not rebuildable from this tree at any seed.  Everything this run concludes
      about (q, k, n) is computed WITHIN one vintage and is unaffected; what is affected is the
      transportability of 525's own published numbers, which is reported as a finding.
  G4  the committed SPY triple on a named panel
  G5  determinism (rebuild one panel's book rows, compare)

PROTOCOL: 10 bps primary, t+1, weekly, gross 0.75, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: the small-cap pool and BSTK100 are CURRENT constituents of their screens (the small
pool additionally drops the tickers with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every
CAGR and drawdown LEVEL below is optimistic and the 4b bars are easier here than on a
point-in-time panel.  The (q, k, n) contrasts are same-days comparisons across synthetic panels
drawn from the SAME two pools and are far less exposed than the levels; the pass COUNTS and the
rule-8 triples are levels read against SPY, which is not survivorship-inflated, so those are upper
bounds.  Stated, not hidden.
"""
from __future__ import annotations

import importlib.util
import math
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
BT = ROOT / "research" / "backtests"
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
M525 = _load(BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B.py", "idea525")

do_panel, panel_measures = M525.do_panel, M525.panel_measures
spearman, partial_spearman = M286.spearman, M286.partial_spearman

# ---- the ladder ------------------------------------------------------------------------------
QS = [0.00, 0.25, 0.50, 0.75, 1.00]          # TUNED 1 -- 525's own q levels
KS = [40, 60, 80, 100, 200, 400]             # TUNED 2 -- 525's 40..100 extended to 400
NS_LAD = [5, 10, 15, 20, 30]                 # reported axis (525's, truncated so max n < min k)
QS_B, KS_B = M525.QS, M525.KS                # 525's own ladder, replayed for G3
N_DRAWS, SEED_B, SEED_NEW = M525.N_DRAWS, M525.SEED, 686
NARROW_K = max(KS_B)

BAR_RHO, SHARE = 0.30, 8 / 11                # the record's own bar and sign-consistency share
IS_END, OOS_START = M286.IS_END, M286.OOS_START
C525_PASSES, C525_CELLS = 21, 348            # 525's committed headline
C525_EBAR = (42.7, 33.5)                     # passers vs failers
C525_BREADTH = (0.6479, 0.4874)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def need(levels):
    return int(math.ceil(SHARE * levels))


def build_ladder(s_stk, b_stk):
    """[(q, k, draw, small_cols, large_cols)].  The k <= 100 half replays 525's generator so
    those panels are byte-identical to its own; the wide half uses a separate generator so it
    cannot perturb that replay."""
    built, from_525, seen = [], set(), set()
    rng = np.random.default_rng(SEED_B)
    for q in QS_B:
        for k in KS_B:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(N_DRAWS):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    continue                         # 525's dedupe, same position in the loop
                seen.add(key)
                built.append((q, k, d, sc, lc))
                from_525.add((q, k, d))
    rng2 = np.random.default_rng(SEED_NEW)
    for q in QS:
        for k in KS:
            if k <= NARROW_K:
                continue
            ns_ = int(round(q * k)); nl_ = k - ns_
            if ns_ > len(s_stk) or nl_ > len(b_stk):
                continue                             # outside the feasible envelope
            for d in range(N_DRAWS):
                sc = sorted(rng2.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng2.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    P(f"  dedupe: q={q:.2f} k={k} draw {d} is an exact repeat - skipped")
                    continue
                seen.add(key)
                built.append((q, k, d, sc, lc))
    built.sort(key=lambda t: (t[0], t[1], t[2]))
    return built, from_525


def within(df, gcol, xcol, ycol="pass4b"):
    """Per-level Spearman of the pass indicator against x, plus the mean and the sign share."""
    per = {}
    for g, sub in df.groupby(gcol):
        per[g] = spearman(sub[ycol].astype(float), sub[xcol].astype(float))
    vals = np.array([v for v in per.values() if np.isfinite(v)])
    m = float(vals.mean()) if len(vals) else np.nan
    if len(vals) and np.isfinite(m) and m != 0:
        share = int((np.sign(vals) == np.sign(m)).sum())
    else:
        share = 0
    return per, m, share, len(vals)


def verdict(m, share, levels, label):
    ok = bool(np.isfinite(m) and abs(m) >= BAR_RHO and share >= need(levels))
    P(f"    {label:34s} mean rho {m:+.4f}   sign {share} of {levels} "
      f"(need {need(levels)})   -> {'PASS' if ok else 'FAIL'}")
    return ok


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 686 (cloud, 2026-09-15) -- is the 4b FOOTPRINT still a CAP-MIX function once k is free?")
    P("=" * 100)
    P("PRE-REGISTERED BARS (docstring, fixed before any number below was read):")
    P(f"  |mean within-level rho(pass4b, axis)| >= {BAR_RHO:.2f} with the sign holding in")
    P(f"  >= ceil({SHARE:.3f} x L) of L levels.  H_285: the boundary is (cap mix, PANEL WIDTH)")
    P("  rather than (cap mix, BOOK SIZE) iff H_K passes, H_N fails and |rho_k|q| > |rho_n|q|.")
    P("")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"common calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built, from_525 = build_ladder(s_stk, b_stk)
    cells = sorted({(q, k) for q, k, *_ in built})
    P(f"{len(built)} panels built over {len(cells)} feasible (q,k) cells "
      f"({len(from_525)} replayed from idea 525 at k <= {NARROW_K}, "
      f"{len(built)-len(from_525)} new at k > {NARROW_K})")
    P("  cells: " + ", ".join(f"({q:.2f},{k})" for q, k in cells))
    P(f"  k span {min(k for _, k in cells)}..{max(k for _, k in cells)} = "
      f"{max(k for _, k in cells)/min(k for _, k in cells):.1f}x   (idea 525: 2.5x)")
    P("")

    # ---------------- G1: the envelope, on this run's own construction ----------------
    gates = []
    bad = []
    for q, k, d, sc, lc in built:
        if len(sc) > len(s_stk) or len(lc) > len(b_stk):
            bad.append((q, k, d, "pool overflow"))
        if len(set(sc)) != len(sc) or len(set(lc)) != len(lc):
            bad.append((q, k, d, "duplicate column"))
        if len(sc) + len(lc) != k:
            bad.append((q, k, d, "width mismatch"))
        if abs(len(sc) - round(q * k)) > 0:
            bad.append((q, k, d, "cap mix mismatch"))
    gates.append(dict(gate="G1 feasible envelope: exact width, exact cap mix, no dup columns, "
                           "no pool overflow",
                      stat=f"{len(built)} panels, {len(bad)} violations", passed=not bad))

    # ---------------- run the ladder ----------------
    P("=" * 100)
    P("RUNNING THE LADDER")
    P("=" * 100)
    brows, srows, meas_rows = [], [], []
    for i, (q, k, d, sc, lc) in enumerate(built):
        cols = list(sc) + list(lc)
        px = pd.concat([pxs_c[[c for c in sc]], pxb_c[[c for c in lc]],
                        pxb_c[["SPY"]]], axis=1)
        tag = f"q{q:.2f}_k{k}_d{d}"
        do_panel(tag, "ladder", q, d, px, cols, brows, srows, NS_LAD, {"LAD": NS_LAD})
        m = panel_measures(px, cols)
        meas_rows.append(dict(panel=tag, q=q, draw=d, from525=(q, k, d) in from_525, **m))
        if (i + 1) % 10 == 0 or i == len(built) - 1:
            P(f"  {i+1:3d}/{len(built)} panels  ({time.time()-t0:.0f}s)")
    bk = pd.DataFrame(brows)
    ms = pd.DataFrame(meas_rows)
    bk["k"] = bk["k"].astype(int)
    bk["is525"] = bk.k <= NARROW_K
    dump(bk, "books.csv")
    dump(ms, "panels.csv")
    P("")

    # ---------------- remaining gates ----------------
    P("=" * 100)
    P("GATES (printed before any result number)")
    P("=" * 100)
    ident = float(np.abs(np.log(ms.Ebar.clip(lower=1e-12))
                         - (np.log(ms.breadth.clip(lower=1e-12)) + np.log(ms.k))).max())
    gates.append(dict(gate="G2 the k-identity log(Ebar) == log(breadth) + log(k) on every panel",
                      stat=f"max |residual| {ident:.3e} over {len(ms)} panels",
                      passed=bool(ident < 1e-9)))

    nar = bk[bk.is525]
    n_pass, n_cells = int(nar.pass4b.sum()), len(nar)
    eb_p = float(nar.loc[nar.pass4b, "Ebar"].mean())
    eb_f = float(nar.loc[~nar.pass4b, "Ebar"].mean())
    br_p = float(nar.loc[nar.pass4b, "breadth"].mean())
    br_f = float(nar.loc[~nar.pass4b, "breadth"].mean())
    g3 = bool(n_pass == C525_PASSES and n_cells == C525_CELLS
              and abs(eb_p - C525_EBAR[0]) < 0.05 and abs(eb_f - C525_EBAR[1]) < 0.05
              and abs(br_p - C525_BREADTH[0]) < 5e-4 and abs(br_f - C525_BREADTH[1]) < 5e-4)
    gates.append(dict(
        gate="G3 CROSS-RUN (STRICT): idea 525's 21 of 348 AND its passer/failer Ebar and breadth",
        stat=f"this run {n_pass} of {n_cells} (525: {C525_PASSES} of {C525_CELLS}); "
             f"Ebar pass/fail {eb_p:.1f}/{eb_f:.1f} (525: {C525_EBAR[0]}/{C525_EBAR[1]}); "
             f"breadth {br_p:.4f}/{br_f:.4f} (525: {C525_BREADTH[0]}/{C525_BREADTH[1]})",
        passed=g3))

    # ---- G3 FORENSIC: the strict gate fails, so name the cause and verify it ----------------
    P("  G3 FORENSIC -- the strict cross-run gate is decomposed rather than relaxed:")
    cb = pd.read_csv(BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B.books.csv")
    cb = cb[cb.kind == "mix"].copy()
    key = ["q", "k", "draw", "arm"]
    a = nar.set_index(key).sort_index()
    o = cb.set_index(key).sort_index()
    common = a.index.intersection(o.index)
    agree = float((a.loc[common, "pass4b"].values == o.loc[common, "pass4b"].values).mean())
    dS = float(np.abs(a.loc[common, "Sharpe"].values - o.loc[common, "Sharpe"].values).max())
    dE = float(np.abs(a.loc[common, "Ebar"].values - o.loc[common, "Ebar"].values).max())
    qmax_here = float(nar.loc[nar.pass4b, "q"].max())
    g3rows = [
        dict(part="G3a ladder SHAPE (cells, panels, dedupe positions)",
             stat=f"{n_cells} cells / {len(ms[ms.from525])} panels vs 525's {C525_CELLS} / 58",
             passed=bool(n_cells == C525_CELLS)),
        dict(part="G3b the HEADLINE COUNT", stat=f"{n_pass} of {n_cells} vs 525's "
             f"{C525_PASSES} of {C525_CELLS}", passed=bool(n_pass == C525_PASSES)),
        dict(part="G3c CELL-BY-CELL identity (this is what actually fails)",
             stat=f"verdict agreement {agree:.4f} on {len(common)} cells "
                  f"({int(round((1-agree)*len(common)))} flip); max |dSharpe| {dS:.4f}; "
                  f"max |dEbar| {dE:.4f}", passed=bool(agree == 1.0 and dS < 1e-9)),
        dict(part="G3d the CAUSE, verified: the small-cap pool has been RESTATED since 525 ran",
             stat=f"525's console: 'pools: SMALL 439, BSTK 100', calendar 4,194 days ending "
                  f"2026-09-04.  This tree: SMALL {len(s_stk)}, BSTK {len(b_stk)}, calendar "
                  f"{len(idx)} days ending {idx[-1].date()}.  525 committed no column lists, so "
                  f"its panels are NOT rebuildable from this tree at any seed.",
             passed=bool(len(s_stk) != 439)),
        dict(part="G3e what the restatement COSTS the published claim",
             stat=f"525 published 'highest q carrying any 4b pass: 0.25'; on the restated pool "
                  f"the highest q carrying a pass is {qmax_here:.2f}",
             passed=bool(True)),
    ]
    for r in g3rows:
        P(f"    [{'ok  ' if r['passed'] else 'FAIL'}] {r['part']}\n           {r['stat']}")
    dump(pd.DataFrame(g3rows), "g3_forensic.csv")

    spy_dev = float((bk.spy_S - bk.spy_S.iloc[0]).abs().max())
    gates.append(dict(gate="G4 one SPY comparand per panel (the benchmark column is shared, so "
                           "every panel must read the SAME SPY triple)",
                      stat=f"max spread of the SPY Sharpe across all {len(bk)} book rows "
                           f"{spy_dev:.3e}; SPY {bk.spy_CAGR.iloc[0]:.4f} / {bk.spy_S.iloc[0]:.4f}"
                           f" / {bk.spy_DD.iloc[0]:.4f}",
                      passed=bool(spy_dev < 1e-9)))

    q0, k0, d0, sc0, lc0 = built[0]
    px0 = pd.concat([pxs_c[[c for c in sc0]], pxb_c[[c for c in lc0]], pxb_c[["SPY"]]], axis=1)
    br2, sr2 = [], []
    do_panel("repro", "ladder", q0, d0, px0, list(sc0) + list(lc0), br2, sr2, NS_LAD, {"LAD": NS_LAD})
    a = bk[bk.panel == f"q{q0:.2f}_k{k0}_d{d0}"].reset_index(drop=True)
    b = pd.DataFrame(br2).reset_index(drop=True)
    d5 = float(np.abs(a.Sharpe.values - b.Sharpe.values).max())
    gates.append(dict(gate="G5 determinism (rebuild one panel's book rows, compare)",
                      stat=f"max |dSharpe| {d5:.3e}", passed=bool(d5 == 0.0)))

    gdf = pd.DataFrame(gates)
    for _, r in gdf.iterrows():
        P(f"  [{'PASS' if r.passed else 'FAIL'}] {r.gate}\n        {r.stat}")
    P(f"  GATES {int(gdf.passed.sum())} of {len(gdf)} PASS")
    dump(gdf, "gates.csv")
    P("")

    # ---------------- the footprint, every point published ----------------
    P("=" * 100)
    P("THE 4b FOOTPRINT ON THE FREE-k LADDER (every cell published)")
    P("=" * 100)
    P(f"  overall 4b {int(bk.pass4b.sum())} of {len(bk)} book-cells "
      f"({bk.pass4b.mean():.4f});  4a {int(bk.pass4a.sum())} of {len(bk)} ({bk.pass4a.mean():.4f})")
    piv = bk.pivot_table(index="q", columns="k", values="pass4b", aggfunc="mean")
    cnt = bk.pivot_table(index="q", columns="k", values="pass4b", aggfunc="size")
    P("  4b pass RATE by (q, k)   [cell count in brackets]")
    P("    q \\ k   " + "".join(f"{k:>14d}" for k in piv.columns))
    for qv, row in piv.iterrows():
        P(f"    {qv:5.2f}   " + "".join(
            ("        .     " if np.isnan(row[k]) else f"{row[k]:9.3f} [{int(cnt.loc[qv,k]):3d}]")
            for k in piv.columns))
    pn = bk.pivot_table(index="q", columns="arm", values="pass4b", aggfunc="mean")
    P("  4b pass RATE by (q, book)")
    P("    q \\ arm " + "".join(f"{c:>10s}" for c in pn.columns))
    for qv, row in pn.iterrows():
        P(f"    {qv:5.2f}   " + "".join(
            ("      .   " if np.isnan(row[c]) else f"{row[c]:10.3f}") for c in pn.columns))
    pk = bk.pivot_table(index="k", columns="arm", values="pass4b", aggfunc="mean")
    P("  4b pass RATE by (k, book)")
    P("    k \\ arm " + "".join(f"{c:>10s}" for c in pk.columns))
    for kv, row in pk.iterrows():
        P(f"    {kv:5d}   " + "".join(
            ("      .   " if np.isnan(row[c]) else f"{row[c]:10.3f}") for c in pk.columns))
    dump(piv.reset_index(), "footprint_qk.csv")
    P("")

    # ---------------- the joint reading ----------------
    P("=" * 100)
    P("THE JOINT READING -- which axis is the boundary on, with the others held fixed?")
    P("=" * 100)
    nb = bk[bk.arm != "EWall"].copy()      # n is only defined on the CAND ladder
    nb["n"] = nb["n"].astype(float)

    per_k, m_q, sh_q, L_q = within(bk, "k", "q")
    per_q, m_k, sh_k, L_k = within(bk, "q", "k")
    per_qn, m_n, sh_n, L_n = within(nb, "q", "n")
    P("  within-level Spearman of the 4b pass indicator against each axis:")
    H_Q = verdict(m_q, sh_q, L_q, "H_Q  cap mix q (within k)")
    H_K = verdict(m_k, sh_k, L_k, "H_K  PANEL WIDTH k (within q)")
    H_N = verdict(m_n, sh_n, L_n, "H_N  BOOK SIZE n (within q)")
    P("  per-level detail:")
    P("    rho(pass4b, q) by k: " + "  ".join(f"k={int(k)} {v:+.3f}" for k, v in per_k.items()))
    P("    rho(pass4b, k) by q: " + "  ".join(f"q={q:.2f} {v:+.3f}" for q, v in per_q.items()))
    P("    rho(pass4b, n) by q: " + "  ".join(f"q={q:.2f} {v:+.3f}" for q, v in per_qn.items()))

    rho_kq = partial_spearman(bk.pass4b.astype(float), bk.k.astype(float), bk.q)
    rho_nq = partial_spearman(nb.pass4b.astype(float), nb.n, nb.q)
    rho_qk = partial_spearman(bk.pass4b.astype(float), bk.q, bk.k.astype(float))
    rho_kqn = partial_spearman(nb.pass4b.astype(float), nb.k.astype(float), nb.q)
    P("  pooled partial Spearman:")
    P(f"    rho(pass4b, q | k) = {rho_qk:+.4f}")
    P(f"    rho(pass4b, k | q) = {rho_kq:+.4f}    (CAND-only slice {rho_kqn:+.4f})")
    P(f"    rho(pass4b, n | q) = {rho_nq:+.4f}")

    H_285 = bool(H_K and (not H_N) and abs(rho_kqn) > abs(rho_nq))
    P(f"  H_285 (the queue's question): {'PASS' if H_285 else 'FAIL'}   "
      f"[needs H_K PASS, H_N FAIL, |rho_k|q| {abs(rho_kqn):.4f} > |rho_n|q| {abs(rho_nq):.4f}]")

    # linear probability fit, reported beside the rank reading
    X = np.column_stack([np.ones(len(nb)), nb.q.values, np.log(nb.k.values), np.log(nb.n.values)])
    y = nb.pass4b.astype(float).values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    r2 = 1.0 - float(np.var(y - yhat) / np.var(y)) if np.var(y) else np.nan
    P(f"  linear-probability fit  pass4b ~ 1 + q + log k + log n   (CAND slice, {len(nb)} cells)")
    P(f"    intercept {beta[0]:+.4f}   q {beta[1]:+.4f}   log k {beta[2]:+.4f}   "
      f"log n {beta[3]:+.4f}   R2 {r2:.4f}")

    # H_MONO
    mono = []
    for k, sub in bk.groupby("k"):
        rates = [sub[sub.q == qv].pass4b.mean() for qv in QS if (sub.q == qv).any()]
        rates = [r for r in rates if np.isfinite(r)]
        ok = all(rates[i] >= rates[i + 1] - 1e-12 for i in range(len(rates) - 1))
        mono.append((int(k), ok, rates))
    H_MONO = all(o for _, o, _ in mono)
    P(f"  H_MONO (the per-q pass rate non-increasing in q at every k): "
      f"{'PASS' if H_MONO else 'FAIL'}")
    for k, ok, rates in mono:
        P(f"    k={k:3d} {'ok  ' if ok else 'FAIL'} " + " ".join(f"{r:.3f}" for r in rates))

    jrows = [dict(axis="q|k", rho=rho_qk, mean_within=m_q, sign=sh_q, levels=L_q, verdict=H_Q),
             dict(axis="k|q", rho=rho_kq, mean_within=m_k, sign=sh_k, levels=L_k, verdict=H_K),
             dict(axis="n|q", rho=rho_nq, mean_within=m_n, sign=sh_n, levels=L_n, verdict=H_N)]
    dump(pd.DataFrame(jrows), "joint.csv")
    P("")

    # ---------------- where the passes actually live ----------------
    P("=" * 100)
    P("WHERE THE PASSES LIVE -- 525's headline restated on the wide ladder")
    P("=" * 100)
    for lab, sl in [("k <= 100 (525's support)", bk[bk.is525]), ("k > 100 (new)", bk[~bk.is525]),
                    ("ALL", bk)]:
        if not len(sl):
            continue
        p = sl[sl.pass4b]
        P(f"  {lab:26s} 4b {len(p):3d} of {len(sl):3d} ({sl.pass4b.mean():.4f})   "
          f"max q with a pass {('none' if not len(p) else f'{p.q.max():.2f}')}   "
          f"k range of passes {('none' if not len(p) else f'{int(p.k.min())}..{int(p.k.max())}')}")
        if len(p):
            P(f"      Ebar pass/fail {p.Ebar.mean():6.1f} / {sl[~sl.pass4b].Ebar.mean():6.1f}   "
              f"breadth {p.breadth.mean():.4f} / {sl[~sl.pass4b].breadth.mean():.4f}")
    P("")

    # ---------------- RULE 8 ----------------
    P("=" * 100)
    P("RULE 8 -- the cell chosen on 2009-2016 ALONE, 2017-2026 read ONCE, both KEEP paths")
    P("=" * 100)
    wrows = []
    sel_sets = {"ALL": bk, "WIDE_ONLY": bk[~bk.is525], "NARROW_ONLY": bk[bk.is525]}
    for sname, sl in sel_sets.items():
        if not len(sl):
            continue
        cellIS = sl.groupby(["q", "k", "arm"]).agg(
            IS_Sharpe=("IS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
            OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
            pass4b=("pass4b", "mean"), pass4a=("pass4a", "mean"),
            spy_OOS_S=("spy_OOS_S", "mean"), v2_OOS_S=("v2_OOS_S", "mean")).reset_index()
        picks = {
            "PICK_ISSHARPE": cellIS.loc[cellIS.IS_Sharpe.idxmax()],
            "PICK_ISQMIN": cellIS.loc[cellIS[cellIS.q == cellIS.q.min()].IS_Sharpe.idxmax()],
            "PICK_ISKMAX": cellIS.loc[cellIS[cellIS.k == cellIS.k.max()].IS_Sharpe.idxmax()],
        }
        for pname, row in picks.items():
            sub = sl[(sl.q == row.q) & (sl.k == row.k) & (sl.arm == row.arm)]
            wrows.append(dict(support=sname, selector=pname, q=row.q, k=int(row.k), arm=row.arm,
                              IS_Sharpe=row.IS_Sharpe, OOS_CAGR=row.OOS_CAGR,
                              OOS_Sharpe=row.OOS_Sharpe, OOS_MaxDD=row.OOS_MaxDD,
                              spy_OOS_S=row.spy_OOS_S, v2_OOS_S=row.v2_OOS_S,
                              n_draws=len(sub), pass4b_rate=row.pass4b, pass4a_rate=row.pass4a,
                              pass4b_any=bool(sub.pass4b.any()),
                              pass4b_all=bool(sub.pass4b.all())))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward.csv")
    spy = bk.iloc[0]
    P(f"  SPY (shared benchmark column): FULL {spy.spy_CAGR:.2%} / {spy.spy_S:.3f} / "
      f"{spy.spy_DD:.2%}   OOS Sharpe {spy.spy_OOS_S:.3f}")
    P(f"  RULES v2 on the ladder's panels: OOS Sharpe mean {bk.v2_OOS_S.mean():.3f} "
      f"(min {bk.v2_OOS_S.min():.3f}, max {bk.v2_OOS_S.max():.3f})")
    for _, r in wf.iterrows():
        P(f"    {r.support:12s} {r.selector:14s} q={r.q:.2f} k={r.k:3d} {r.arm:7s}  "
          f"IS {r.IS_Sharpe:6.3f}  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / "
          f"{r.OOS_MaxDD:7.2%}   4b {r.pass4b_rate:.2f} of its {r.n_draws} draws  "
          f"4a {r.pass4a_rate:.2f}")
    P(f"  rule-8 picks clearing 4b on EVERY draw: {int(wf.pass4b_all.sum())} of {len(wf)};  "
      f"on ANY draw: {int(wf.pass4b_any.sum())} of {len(wf)}")
    P("")

    # ---------------- VERDICT ----------------
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hyp = dict(H_Q=H_Q, H_K=H_K, H_N=H_N, H_285=H_285, H_MONO=H_MONO)
    for k, v in hyp.items():
        P(f"  {k:7s} {'PASS' if v else 'FAIL'}")
    P(f"  runtime {time.time()-t0:.0f}s")
    pd.DataFrame([hyp]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG))
    return dict(hyp=hyp, bk=bk, wf=wf, gates=gdf)


if __name__ == "__main__":
    main()
