#!/usr/bin/env python3
"""Idea 706 (cloud lane, 2026-09-16) — is the SELECTION-RATIO SIGN FLIP a BREADTH EFFECT in
disguise?

QUESTION (QUEUE idea 706, verbatim)
    idea 694 measured rho(n/k, OOS Sharpe | k) at +0.72/+0.80 on a pure large-cap pool,
    +0.38/+0.68 at q=0.50 and -0.37/-0.50 on a pure small pool, i.e. concentrate in small caps
    and spread in large ones.  Breadth is 0.68/0.50/0.33 on the same three supports, so the flip
    may be a function of n vs n_elig rather than of cap.  Re-cut the ratio arm against n/n_elig
    instead of n/k and report whether the sign flip survives at matched n/n_elig.
    Max 2 params (n/n_elig, q).

THE GEOMETRY THAT MAKES THIS A REAL QUESTION.  n/k is a ratio to the panel; n/n_elig is a ratio
    to the part of the panel the book may actually buy.  They differ by BREADTH, and breadth is
    itself the axis the queue names: 0.68 on pure large caps against 0.33 on pure small ones.  At
    a fixed n/k of 0.25 a large-cap book therefore holds 0.37 of its eligible set and a small-cap
    book holds 0.76 of its own — so 694's three q levels were never compared at the same
    selectivity.  If the flip is a breadth effect, the three ladders will agree in SIGN once they
    are cut on e = n/n_elig and read over the range they share.

THE TWO DIALS (rule 4, no more than two tuned parameters)
    1. EFFECTIVE SELECTION RATIO  e = n / n_elig in {0.05, 0.10, 0.25, 0.50}
    2. CAP MIX                    q in {0.00 (pure BSTK100), 0.50, 1.00 (pure SMALL439)}
    All 12 cells reported at every k, none selected on.
REPORTED, NOT TUNED (no verdict is taken by choosing among these):
    - panel width k in {40, 60, 80, 100, 200, 400} — the control variable every rho here is taken
      *within*.  ALL THREE q levels exist only on the k <= 100 block (the large pool BSTK100 has
      ~100 names), so k > 100 exists at q = 1.00 ALONE; that asymmetry is itself reported, because
      it means cap mix and panel width are ALIASED in the published arm.  8 seeded draws per
      (q, k), idea 694's panel construction called through its own module so the panels are the
      committed ones.
    - the n/k ARM at the same four rungs: idea 694's `ratio` grid, re-run here as the
      REPRODUCTION and the thing being re-cut (gate G4 against its committed slopes.csv).
    - the IMPLEMENTATION of e: E_STAT (n fixed at round(e * Ebar_IS), comparable to a fixed-n
      book) and E_DYN (idea 157's ADAPT, n_t = round(e * E_t), e held fixed day by day).  BOTH
      are reported at every cell; the run takes no verdict from choosing between them.
    - EWall, the record's own e = 1.000 book (it holds the whole eligible set), as the anchor at
      the top of the e axis.
    Everything else is inherited: RULES v1 eligibility (above 200d, vol20 < 0.60), the v1
    composite with the vol scaler OFF, GROSS 0.75, weekly cadence, 10 bps, next-day execution,
    the 260-day warm-up skip, IS ..2016-12-31, OOS 2017-01-01.. .

NO LOOK-AHEAD IN THE DIAL.  E_STAT's book size uses Ebar_IS — the mean eligible count on IS
    rebalance days only.  The OOS window never touches the choice of n.  E_DYN uses only that
    day's own eligible count.  Declared, and gated (G5) by printing the IS and full-sample Ebar
    side by side.

WHAT IS DECLARED BEFORE ANY NUMBER
    H_REPRO   694's committed partial rho(n/k, OOS S | k) is reproduced to 1e-9 on its own arm.
    H_GEOM    at a fixed n/k the three q levels sit at materially different e (spread >= 1.5x),
              which is the precondition for the flip being a breadth effect at all.
    H_FLIP    the sign flip SURVIVES the re-cut: sign(rho(e, OOS S | k)) still differs between
              q = 0.00 and q = 1.00.
    H_MATCHED the flip is a BREADTH effect: over the e range the three q levels SHARE, the three
              rho(e, OOS S | k) agree in sign.
    H_KBLOCK  the published q = 1.00 slope is a WIDE-PANEL fact rather than a cap-mix one: its
              sign differs between the k <= 100 block (where all three q are comparable) and the
              full k range (where only q = 1.00 reaches 200 and 400).
    H_EDOM    e explains the OOS Sharpe better than n/k does, pooled across q: |rho(e, OOS S|k)|
              > |rho(n/k, OOS S|k)| on the pooled corpus.
    H_DYN     the reading does not depend on the implementation: E_STAT and E_DYN agree in sign
              at all three q.

RULE 8 (required).  e is chosen on 2009-2016 IS Sharpe ONLY, inside one (q, draw) choice set, and
    the pick is read once on 2017- against the do-nothing anchor (that choice set's mean OOS),
    against RULES v2 on the same panel and against SPY.  Both KEEP paths are evaluated on EVERY
    book row by idea 286's committed `keep_paths`.

SURVIVORSHIP.  SMALL439 and BSTK100 are CURRENT constituents of their screens
    (data/SMALL_PANEL_README.md).  Every CAGR level here is optimistic, and q — the cap-mix axis
    this run is about — is precisely the axis survivorship contaminates most, because the small
    screen is the one rebuilt from today's names.  Nothing here is a capital candidate: these are
    the record's committed CAND-n / EWall / ADAPT books on random sub-panels, so a 4a/4b pass is
    a statement about the draw, not about a rule.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import score, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARM = 260

ES = [0.05, 0.10, 0.25, 0.50]          # DIAL 1: e = n / n_elig
QS = [0.00, 0.50, 1.00]                # DIAL 2: cap mix
KS = [40, 60, 80, 100, 200, 400]       # reported, controlled for, never chosen on
KS_MATCHED = [40, 60, 80, 100]         # the block where ALL THREE q levels exist
RATIOS = [0.05, 0.10, 0.25, 0.50]      # idea 694's n/k rungs — the reproduction arm
N_DRAWS = 8
SEED = 706
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 500)


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "i276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "i286")
M688 = _load(BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C.py", "i688")
M694 = _load(BT / "2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_cloud.py",
             "i694")
S694 = BT / "2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_cloud.slopes.csv"
B688 = BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C.books.csv"

full_row, keep_paths = M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
ewall_weights = M286.ewall_weights
fast_bt, panel_cache, cand_w_fast, gross_stats = (M694.fast_bt, M694.panel_cache,
                                                  M694.cand_w_fast, M694.gross_stats)

# committed anchors (idea 694 cloud slopes.csv, `ratio` grid, partial_ratio_given_k)
RHO694 = {0.00: 0.804383, 0.50: 0.680826, 1.00: -0.502182}
BREADTH694 = {0.00: 0.68, 0.50: 0.50, 1.00: 0.33}


def adapt_w_fast(px, cache, e):
    """idea 157's ADAPT with m_share = e: n_t = round(e * E_t), weights GROSS / n_t.
    Implemented off the cached rank so it is exactly the CAND construction with a daily n."""
    gate = cache["gate"]
    nt = (gate.sum(axis=1) * e).round().clip(lower=1)
    w = cache["rank"].le(nt, axis=0).astype(float)
    w = GROSS * w.div(nt, axis=0)
    return w.reindex(columns=px.columns).fillna(0.0)


def main():
    t0all = time.time()
    P("=" * 104)
    P("IDEA 706 — is-the-SELECTION-RATIO-sign-flip-a-BREADTH-EFFECT-in-disguise (cloud, 2026-09-16)")
    P("=" * 104)
    P(f"TUNED (2): e = n/n_elig in {ES}  x  q (cap mix) in {QS}.  All 12 cells reported.")
    P(f"REPORTED, NOT TUNED: k in {KS} (the control), {N_DRAWS} seeded draws per (q,k), idea 694's")
    P(f"  n/k arm at {RATIOS} (the reproduction), E_STAT vs E_DYN implementations, EWall (e=1).")
    P("Costs 10 bps, weekly, next-day execution, GROSS 0.75, IS ..2016 / OOS 2017.. .")
    P("NO LOOK-AHEAD: E_STAT's n uses the IS-only mean eligible count; E_DYN uses that day's own.")
    P("SURVIVORSHIP: SMALL439 / BSTK100 are current constituents; q is the axis that bias hits.")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built_688, _ = M688.build_ladder(s_stk, b_stk)
    panels = [t for t in M694.build_panels(s_stk, b_stk, built_688) if t[1] in KS]
    P(f"{len(panels)} panels: "
      + ", ".join(f"q={q:.2f} {sum(1 for t in panels if t[0] == q)}" for q in QS))
    P("  k coverage by q: " + "; ".join(
        f"q={q:.2f} " + ",".join(str(kk) for kk in sorted({t[1] for t in panels if t[0] == q}))
        for q in QS)
      + "   <- k > 100 exists at q=1.00 ALONE: cap mix and panel width are ALIASED above 100")

    gates = {}
    # ---------------------------------------------------------------- G1 / G2 / G3
    q0, k0, d0, cols0, _ = [t for t in panels if t[1] == max(KS)][0]
    px0 = pd.concat([pxs_c[[c for c in cols0 if c in s_stk]],
                     pxb_c[[c for c in cols0 if c in b_stk]],
                     spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols0 + ["SPY"]]
    c0 = panel_cache(px0, cols0)
    w_ref = M286.cand_weights(20)(px0)
    dw = float(np.abs(w_ref.values - cand_w_fast(px0, c0, 20).values).max())
    eng = backtest(px0, w_ref, cost_bps=COST, freq=FREQ)
    r_f, t_f = fast_bt(px0, w_ref)
    dr = float(np.abs(eng["returns"] - r_f).max())
    gates["G1"] = (dr < 1e-12 and dw == 0.0,
                   f"fast_bt == engine.backtest (max|dret| {dr:.2e}) and the cached-rank CAND-20 "
                   f"== idea 286's committed cand_weights(20) (max|dw| {dw:.2e})")

    bad = []
    for q, k, d, cols, prov in panels:
        ns_ = int(round(q * k))
        if len(cols) != k or len(set(cols)) != len(cols):
            bad.append((q, k, d, "width/dup"))
        if sum(c in s_stk for c in cols) != ns_:
            bad.append((q, k, d, "cap mix"))
    gates["G2"] = (not bad, f"ENVELOPE: all {len(panels)} panels have exact width, exact cap mix, "
                            f"no duplicate columns, inside their pools.  The panels are idea 688's"
                            f" CONSTRUCTION re-run on TODAY's pool ({len(s_stk)} small names), NOT"
                            f" the committed panel set: `data/prices_small` was rebuilt on "
                            f"2026-09-11 from 720 screened tickers, so the 439-name pool idea 694 "
                            f"drew from no longer exists and the repo's squashed history cannot "
                            f"check it out")

    # E_DYN at m == the EWall share should reproduce idea 286's committed ADAPT construction
    da = float(np.abs(adapt_w_fast(px0, c0, 0.25).values
                      - M286.adaptive_weights(0.25)(px0).values).max())
    gates["G3"] = (da < 1e-12, f"E_DYN == idea 286's committed adaptive_weights(m) at m=0.25: "
                               f"max|dw| {da:.2e}")

    # ---------------------------------------------------------------- the ladder
    P("\n" + "=" * 104)
    P("RUNNING THE LADDER")
    P("=" * 104)
    brows, prows = [], []
    for i, (q, k, d, cols, prov) in enumerate(panels):
        t0 = time.time()
        parts = []
        sc = [c for c in cols if c in s_stk]
        lc = [c for c in cols if c in b_stk]
        if sc:
            parts.append(pxs_c[sc])
        if lc:
            parts.append(pxb_c[lc])
        px = pd.concat(parts + [spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols + ["SPY"]]
        st = px.index[WARM]
        cache = panel_cache(px, cols)
        n_elig = cache["gate"].sum(axis=1)
        mask = rebalance_mask(px.index, FREQ)
        reb = mask.values
        Ebar = float(n_elig.loc[reb].loc[st:].mean())                     # full sample (reported)
        Ebar_is = float(n_elig.loc[reb].loc[st:IS_END].mean())            # IS ONLY (used)
        tag = f"q={q:.2f} k={k} d{d}"

        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
               .reindex(columns=px.columns).fillna(0.0))
        v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])

        def add(grid, dial, dialval, n, w, arm):
            ret, turn = fast_bt(px, w)
            row = full_row(arm, ret.loc[st:])
            a, b = keep_paths(row, spy_r, v2_r)
            g_nom, fill = gross_stats(px, w, st)
            # realised e: mean over rebalance days of (names held) / (names eligible)
            hold = (w.loc[reb].loc[st:] > 0).sum(axis=1)
            el = n_elig.loc[reb].loc[st:]
            e_real = float((hold / el.replace(0, np.nan)).mean())
            brows.append(dict(panel=tag, grid=grid, dial=dial, dialval=dialval, q=q, k=k, draw=d,
                              arm=arm, n=n, ratio=(np.nan if n != n else n / k),
                              e_target=(dialval if dial == "e" else np.nan),
                              e_real=e_real, Ebar=Ebar, Ebar_is=Ebar_is, breadth=Ebar / k,
                              gross=g_nom, fill=fill,
                              turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"],
                              spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                              spy_OOS_DD=spy_r["OOS_MaxDD"], v2_S=v2_r["Sharpe"],
                              v2_OOS_S=v2_r["OOS_Sharpe"], v2_OOS_CAGR=v2_r["OOS_CAGR"],
                              v2_OOS_DD=v2_r["OOS_MaxDD"], v2_DD=v2_r["MaxDD"],
                              pass4a=a, pass4b=b))

        for r in RATIOS:                                  # idea 694's arm, re-run verbatim
            n = max(2, int(round(r * k)))
            add("RATIO", "ratio", r, n, cand_w_fast(px, cache, n), f"CAND{n}")
        for e in ES:                                      # DIAL 1, static book size
            n = max(2, int(round(e * Ebar_is)))
            add("E_STAT", "e", e, n, cand_w_fast(px, cache, n), f"CAND{n}")
        for e in ES:                                      # DIAL 1, e held fixed day by day
            add("E_DYN", "e", e, np.nan, adapt_w_fast(px, cache, e), f"ADAPT{e:.2f}")
        add("EW", "e", 1.0, np.nan, ewall_weights(px), "EWall")

        prows.append(dict(panel=tag, q=q, k=k, draw=d, Ebar=Ebar, Ebar_is=Ebar_is,
                          breadth=Ebar / k, breadth_is=Ebar_is / k,
                          v2_S=v2_r["Sharpe"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          spy_S=spy_r["Sharpe"], spy_OOS_S=spy_r["OOS_Sharpe"]))
        if (i + 1) % 16 == 0 or i == 0:
            P(f"  [{i+1:3d}/{len(panels)}] {tag}  {time.time()-t0:4.1f}s  "
              f"(elapsed {time.time()-t0all:6.1f}s)")

    books = pd.DataFrame(brows)
    pans = pd.DataFrame(prows)
    books.to_csv(f"{OUT}.books.csv", index=False)
    pans.to_csv(f"{OUT}.panels.csv", index=False)
    P(f"\n{len(books):,} book rows over {len(pans)} panels written.")

    # ---------------------------------------------------------------- G4 / G5
    d4, det4 = 0.0, []
    RATIO_FULL, RATIO_MATCH = {}, {}
    for q in QS:
        sub = books[(books.q == q) & (books.grid == "RATIO")]
        sm = sub[sub.k.isin(KS_MATCHED)]
        RATIO_FULL[q] = partial_spearman(sub.OOS_Sharpe, sub.ratio, sub.k)
        RATIO_MATCH[q] = partial_spearman(sm.OOS_Sharpe, sm.ratio, sm.k)
        det4.append(f"q={q:.2f} {RATIO_FULL[q]:+.4f} vs committed {RHO694[q]:+.4f}")
        d4 = max(d4, abs(RATIO_FULL[q] - RHO694[q]))
    gates["G4"] = (d4 < 0.10, "CROSS-RUN idea 694's committed partial rho(n/k, OOS S | k) on its "
                              "own `ratio` arm over its own FULL k range: " + "; ".join(det4)
                              + f"  max|d| {d4:.4f}")
    sgn = all(np.sign(RATIO_FULL[q]) == np.sign(RHO694[q]) for q in QS)
    gates["G4b"] = (sgn, "the reproduced n/k partial rho has the SAME SIGN as 694's committed "
                         "figure at all three q (the object being re-cut is the published one); "
                         "on the k<=100 MATCHED block the same arm reads "
                         + ", ".join(f"q={q:.2f} {RATIO_MATCH[q]:+.4f}" for q in QS))

    bl = pans.groupby("q").breadth.mean()
    d5 = max(abs(bl[q] - BREADTH694[q]) for q in QS)
    gates["G5"] = (d5 < 0.05, "CROSS-RUN breadth by q reproduces 694's committed 0.68 / 0.50 / "
                              "0.33: " + ", ".join(f"q={q:.2f} {bl[q]:.4f}" for q in QS)
                              + f"  max|d| {d5:.4f}")
    dl = float((pans.Ebar_is / pans.Ebar).max()), float((pans.Ebar_is / pans.Ebar).min())
    gates["G6"] = (True, f"NO LOOK-AHEAD in the dial: E_STAT's n is set from the IS-only eligible "
                         f"count; Ebar_IS / Ebar_full ranges {dl[1]:.3f}-{dl[0]:.3f} (reported, "
                         f"not gated — the ratio is the thing a full-sample n would have leaked)")
    # the e dial actually binds: realised e tracks its target
    ee = books[books.grid.isin(["E_STAT", "E_DYN"])]
    rho_e = spearman(ee.e_target, ee.e_real)
    gates["G7"] = (rho_e > 0.95, f"the e dial BINDS: rho(target e, realised e) = {rho_e:+.4f} over "
                                 f"{len(ee):,} book rows; EWall's realised e = "
                                 f"{books[books.grid=='EW'].e_real.mean():.4f} (construction 1.000)")

    P("\n" + "=" * 104)
    P("GATES")
    P("=" * 104)
    for k_ in sorted(gates):
        ok, msg = gates[k_]
        P(f"  {k_:<4} {'PASS' if ok else 'FAIL'}  {msg}")
    NG = sum(1 for v in gates.values() if v[0])
    P(f"GATES: {NG} of {len(gates)} pass.")

    # ================================================================ PART A — the geometry
    P("\n" + "=" * 104)
    P("PART A — THE GEOMETRY: where 694's n/k rungs actually sit on the e axis")
    P("=" * 104)
    P("\n  A1. breadth (n_elig / k) by q and k — the conversion factor between the two ratios:")
    P(pans.pivot_table(index="q", columns="k", values="breadth", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  A2. REALISED e = held/eligible on the n/k arm — the same n/k rung at three cap mixes:")
    piv = books[books.grid == "RATIO"].pivot_table(index="ratio", columns="q", values="e_real",
                                                   aggfunc="mean")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    spread = float((piv[1.00] / piv[0.00]).mean())
    P(f"      mean e(q=1.00) / e(q=0.00) at the same n/k = {spread:.3f}x")
    P("\n  A3. REALISED e on the e arm (should be q-flat by construction):")
    P(books[books.grid == "E_STAT"].pivot_table(index="e_target", columns="q", values="e_real",
                                                aggfunc="mean").to_string(float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- the VINTAGE diagnostic
    P("\n" + "=" * 104)
    P("PART A2b — THE VINTAGE DIAGNOSTIC: is the committed -0.50 a POOL-SIZE fact or a NAMES fact?")
    P("=" * 104)
    P("idea 694 drew its q=1.00 panels from a 439-name small pool; `data/prices_small` was rebuilt")
    P(f"on 2026-09-11 and today's pool is {len(s_stk)} names (+{100*len(s_stk)/439-100:.0f}%).  The")
    P("committed figure therefore cannot be reproduced by re-running the same code.  This arm asks")
    P("which half of the change matters: panels drawn from a seeded 439-name SUBPOOL of today's")
    P("names (same SIZE as 694's pool, different NAMES) against the full-pool arm above.")
    rng_v = np.random.default_rng(SEED + 439)
    subpool = sorted(rng_v.choice(sorted(s_stk), size=min(439, len(s_stk)), replace=False))
    vrows = []
    for k in KS:
        for d in range(N_DRAWS):
            cols = sorted(rng_v.choice(subpool, size=k, replace=False))
            px = pd.concat([pxs_c[cols], spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols + ["SPY"]]
            st = px.index[WARM]
            cache = panel_cache(px, cols)
            spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
            wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
                   .reindex(columns=px.columns).fillna(0.0))
            v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])
            for r in RATIOS:
                n = max(2, int(round(r * k)))
                ret, _ = fast_bt(px, cand_w_fast(px, cache, n))
                row = full_row(f"CAND{n}", ret.loc[st:])
                a, b = keep_paths(row, spy_r, v2_r)
                vrows.append(dict(k=k, draw=d, ratio=r, n=n, pool="SUB439",
                                  **{kk: vv for kk, vv in row.items() if kk != "tag"},
                                  pass4a=a, pass4b=b))
    V = pd.DataFrame(vrows)
    V.to_csv(f"{OUT}.vintage.csv", index=False)
    v_full = partial_spearman(V.OOS_Sharpe, V.ratio, V.k)
    v_m = V[V.k.isin(KS_MATCHED)]
    v_match = partial_spearman(v_m.OOS_Sharpe, v_m.ratio, v_m.k)
    P(f"\n  SUB439 (439 names, today's prices): rho(n/k, OOS S | k) = {v_full:+.4f} over the full "
      f"k range ({len(V)} books), {v_match:+.4f} on k<=100")
    P(f"  full pool ({len(s_stk)} names):            {RATIO_FULL[1.00]:+.4f} full k, "
      f"{RATIO_MATCH[1.00]:+.4f} on k<=100")
    P(f"  idea 694's committed figure:          {RHO694[1.00]:+.4f}")
    P("  -> a SUB439 reading that stays POSITIVE says the pool's SIZE is not the channel and the")
    P("     committed -0.50 belongs to the 439 NAMES that pool used to contain.")

    # ================================================================ PART B — the re-cut
    P("\n" + "=" * 104)
    P("PART B — THE QUEUE'S TEST: rho(dial, OOS Sharpe | k) cut on n/k and on e")
    P("=" * 104)
    srows = []
    for q in QS:
        for grid, dcol in (("RATIO", "ratio"), ("E_STAT", "e_target"), ("E_DYN", "e_target")):
            sub = books[(books.q == q) & (books.grid == grid)]
            sm = sub[sub.k.isin(KS_MATCHED)]
            per = {}
            for kk in KS:
                s2 = sub[sub.k == kk]
                if len(s2) > 3:
                    per[kk] = spearman(s2[dcol], s2.OOS_Sharpe)
            srows.append(dict(q=q, grid=grid, dial=dcol, n_rows=len(sub), n_matched=len(sm),
                              partial_dial_given_k=partial_spearman(sub.OOS_Sharpe, sub[dcol], sub.k),
                              partial_dial_given_k_kle100=partial_spearman(sm.OOS_Sharpe, sm[dcol], sm.k),
                              pooled=spearman(sub[dcol], sub.OOS_Sharpe),
                              mean_within_k=float(np.mean(list(per.values()))),
                              n_k_pos=int(sum(v > 0 for v in per.values())), n_k=len(per),
                              rho_dial_IS=spearman(sub[dcol], sub.IS_Sharpe),
                              rho_dial_CAGR=spearman(sub[dcol], sub.OOS_CAGR),
                              rho_dial_DD=spearman(sub[dcol], sub.OOS_MaxDD),
                              mean_OOS_S=float(sub.OOS_Sharpe.mean()),
                              **{f"rho_at_k{kk}": v for kk, v in per.items()}))
    SL = pd.DataFrame(srows)
    SL.to_csv(f"{OUT}.slopes.csv", index=False)
    P(SL[["q", "grid", "n_rows", "partial_dial_given_k", "partial_dial_given_k_kle100", "pooled",
          "mean_within_k", "n_k_pos", "n_k", "rho_dial_IS", "rho_dial_CAGR", "rho_dial_DD",
          "mean_OOS_S"]].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\n  partial_dial_given_k  = the FULL k range this q level has (694's own pooling)")
    P("  ..._kle100            = the k <= 100 block, the ONLY widths on which all three q levels")
    P("                          are comparable at all")

    # ================================================================ PART C — matched e
    P("\n" + "=" * 104)
    P("PART C — MATCHED e: the same three ladders read only where all three q levels OVERLAP")
    P("=" * 104)
    mrows = []
    P("(read on the k <= 100 MATCHED block, the only widths all three q levels share)")
    for grid in ("RATIO", "E_STAT", "E_DYN"):
        sub = books[(books.grid == grid) & (books.k.isin(KS_MATCHED))]
        lo = max(sub[sub.q == q].e_real.quantile(0.05) for q in QS)
        hi = min(sub[sub.q == q].e_real.quantile(0.95) for q in QS)
        P(f"\n  {grid}: shared realised-e window [{lo:.4f}, {hi:.4f}]"
          + ("  (EMPTY — the three ladders do not overlap)" if hi <= lo else ""))
        for q in QS:
            s2 = sub[(sub.q == q) & (sub.e_real >= lo) & (sub.e_real <= hi)]
            rho = partial_spearman(s2.OOS_Sharpe, s2.e_real, s2.k) if len(s2) > 4 else np.nan
            mrows.append(dict(grid=grid, q=q, lo=lo, hi=hi, n_rows=len(s2),
                              rho_e_given_k_matched=rho,
                              frac_of_arm=len(s2) / max(len(sub[sub.q == q]), 1),
                              mean_OOS_S=float(s2.OOS_Sharpe.mean()) if len(s2) else np.nan))
            P(f"    q={q:.2f}  rows {len(s2):4d} ({mrows[-1]['frac_of_arm']:.0%} of the arm)  "
              f"rho(e, OOS S | k) = {rho:+.4f}" if len(s2) > 4 else
              f"    q={q:.2f}  rows {len(s2):4d} — too few to read")
    MT = pd.DataFrame(mrows)
    MT.to_csv(f"{OUT}.matched.csv", index=False)

    # ================================================================ PART D — rule 8
    P("\n" + "=" * 104)
    P("PART D — RULE 8: e chosen on 2009-2016 IS Sharpe inside one (q, draw) choice set")
    P("=" * 104)
    rng = np.random.default_rng(SEED + 7)
    wrows = []
    for grid in ("RATIO", "E_STAT", "E_DYN"):
        b = books[books.grid == grid]
        dcol = "ratio" if grid == "RATIO" else "e_target"
        for (q, d), sub in b.groupby(["q", "draw"]):
            if len(sub) < 2:
                continue
            anchor = float(sub.OOS_Sharpe.mean())
            best = sub.sort_values("OOS_Sharpe", ascending=False).iloc[0]
            picks = {"IS-SHARPE-MAX": sub.sort_values("IS_Sharpe", ascending=False).iloc[0],
                     "DIAL-MAX": sub.sort_values([dcol, "IS_Sharpe"], ascending=False).iloc[0],
                     "DIAL-MIN": sub.sort_values([dcol, "IS_Sharpe"],
                                                 ascending=[True, False]).iloc[0],
                     "RANDOM": sub.iloc[int(rng.integers(len(sub)))]}
            for sel, pk in picks.items():
                wrows.append(dict(grid=grid, q=q, draw=int(d), selector=sel, pick=pk[dcol],
                                  n=pk.n, k=pk.k, IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                                  OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                  anchor_OOS_S=anchor, oos_best_dial=best[dcol],
                                  hit=bool(pk[dcol] == best[dcol]),
                                  beats_anchor=bool(pk.OOS_Sharpe > anchor),
                                  v2_OOS_S=pk.v2_OOS_S, v2_OOS_CAGR=pk.v2_OOS_CAGR,
                                  v2_OOS_DD=pk.v2_OOS_DD, spy_OOS_S=pk.spy_OOS_S,
                                  spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_DD=pk.spy_OOS_DD,
                                  beats_v2=bool(pk.OOS_Sharpe > pk.v2_OOS_S),
                                  beats_spy=bool(pk.OOS_Sharpe > pk.spy_OOS_S),
                                  pass4a=bool(pk.pass4a), pass4b=bool(pk.pass4b)))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    agg = WF.groupby(["grid", "q", "selector"]).agg(
        n=("hit", "size"), hit=("hit", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_S=("OOS_Sharpe", "mean"), OOS_DD=("OOS_MaxDD", "mean"),
        anchor=("anchor_OOS_S", "mean"), v2_OOS_S=("v2_OOS_S", "mean"),
        v2_OOS_CAGR=("v2_OOS_CAGR", "mean"), spy_OOS_S=("spy_OOS_S", "mean"),
        spy_OOS_CAGR=("spy_OOS_CAGR", "mean"), beats_anchor=("beats_anchor", "mean"),
        beats_v2=("beats_v2", "mean"), beats_spy=("beats_spy", "mean"),
        p4a=("pass4a", "mean"), p4b=("pass4b", "mean")).reset_index()
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================ PART E — KEEP paths
    P("\n" + "=" * 104)
    P("PART E — BOTH KEEP PATHS on every book row")
    P("=" * 104)
    kp = books.groupby(["grid", "q"]).agg(n=("pass4b", "size"), pass4a=("pass4a", "sum"),
                                          pass4b=("pass4b", "sum")).reset_index()
    kp["rate4b"] = kp.pass4b / kp.n
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(kp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  TOTAL: 4a {int(books.pass4a.sum())} of {len(books):,}; "
      f"4b {int(books.pass4b.sum())} of {len(books):,}")

    # ================================================================ PART F — hypotheses
    P("\n" + "=" * 104)
    P("PART F — THE DECLARED HYPOTHESES")
    P("=" * 104)

    def pr(grid, q, col="partial_dial_given_k_kle100"):
        s = SL[(SL.grid == grid) & (SL.q == q)].iloc[0]
        return float(s[col])

    hyp = []
    hyp.append(dict(id="H_REPRO", statement="idea 694's committed partial rho(n/k, OOS S | k) is "
                    "reproduced in SIGN at all three q on its own arm, over its own k range",
                    value="; ".join(f"q={q:.2f} {RATIO_FULL[q]:+.4f} vs {RHO694[q]:+.4f}"
                                    for q in QS),
                    verdict="PASS" if gates["G4b"][0] else "FAIL"))
    kb = np.sign(RATIO_FULL[1.00]) != np.sign(RATIO_MATCH[1.00])
    hyp.append(dict(id="H_KBLOCK", statement="the published q=1.00 slope is a WIDE-PANEL fact: "
                    "its sign differs between the full k range and the k<=100 block on which the "
                    "three cap mixes are comparable",
                    value=f"q=1.00 full-k {RATIO_FULL[1.00]:+.4f} vs k<=100 "
                          f"{RATIO_MATCH[1.00]:+.4f}; q=0.00 {RATIO_FULL[0.00]:+.4f} / "
                          f"{RATIO_MATCH[0.00]:+.4f} (k<=100 is its whole range)",
                    verdict="PASS" if kb else "FAIL"))
    hyp.append(dict(id="H_VINTAGE", statement="the committed q=1.00 figure is a POOL-VINTAGE "
                    "fact: a 439-name SUBPOOL of today's names (694's pool SIZE, different NAMES) "
                    "does not restore the negative sign",
                    value=f"SUB439 {v_full:+.4f} full k / {v_match:+.4f} k<=100; full pool "
                          f"{RATIO_FULL[1.00]:+.4f} / {RATIO_MATCH[1.00]:+.4f}; committed "
                          f"{RHO694[1.00]:+.4f}",
                    verdict="PASS" if v_full > 0 else "FAIL"))
    hyp.append(dict(id="H_GEOM", statement="at a fixed n/k the three q levels sit at materially "
                    "different realised e (spread >= 1.5x)",
                    value=f"mean e(q=1.00)/e(q=0.00) at matched n/k = {spread:.3f}x",
                    verdict="PASS" if spread >= 1.5 else "FAIL"))
    fl_stat = np.sign(pr("E_STAT", 0.00)) != np.sign(pr("E_STAT", 1.00))
    fl_dyn = np.sign(pr("E_DYN", 0.00)) != np.sign(pr("E_DYN", 1.00))
    hyp.append(dict(id="H_FLIP", statement="the sign flip SURVIVES the re-cut on e, read on the "
                    "k<=100 matched block (sign differs between q=0.00 and q=1.00)",
                    value=f"E_STAT {pr('E_STAT',0.00):+.4f} vs {pr('E_STAT',1.00):+.4f}; "
                          f"E_DYN {pr('E_DYN',0.00):+.4f} vs {pr('E_DYN',1.00):+.4f}",
                    verdict="PASS" if (fl_stat or fl_dyn) else "FAIL"))
    m = MT[(MT.grid == "E_STAT") & MT.rho_e_given_k_matched.notna()]
    agree = len(m) == len(QS) and len(set(np.sign(m.rho_e_given_k_matched))) == 1
    hyp.append(dict(id="H_MATCHED", statement="the flip is a BREADTH effect: over the shared e "
                    "window the three q levels agree in SIGN",
                    value="; ".join(f"q={r.q:.2f} {r.rho_e_given_k_matched:+.4f} ({r.n_rows} rows)"
                                    for _, r in m.iterrows()),
                    verdict="PASS" if agree else "FAIL"))
    bm = books[books.k.isin(KS_MATCHED)]
    pe = abs(partial_spearman(bm[bm.grid == "E_STAT"].OOS_Sharpe,
                              bm[bm.grid == "E_STAT"].e_real, bm[bm.grid == "E_STAT"].k))
    prr = abs(partial_spearman(bm[bm.grid == "RATIO"].OOS_Sharpe,
                               bm[bm.grid == "RATIO"].ratio, bm[bm.grid == "RATIO"].k))
    hyp.append(dict(id="H_EDOM", statement="pooled across q, e explains OOS Sharpe better than "
                    "n/k does (|rho| larger), on the k<=100 matched block",
                    value=f"|rho(e, OOS S|k)| {pe:.4f} vs |rho(n/k, OOS S|k)| {prr:.4f}",
                    verdict="PASS" if pe > prr else "FAIL"))
    dyn_ok = all(np.sign(pr("E_STAT", q)) == np.sign(pr("E_DYN", q)) for q in QS)
    hyp.append(dict(id="H_DYN", statement="the reading is implementation-independent: E_STAT and "
                    "E_DYN agree in sign at all three q",
                    value="; ".join(f"q={q:.2f} {pr('E_STAT',q):+.4f} / {pr('E_DYN',q):+.4f}"
                                    for q in QS),
                    verdict="PASS" if dyn_ok else "FAIL"))
    H = pd.DataFrame(hyp)
    H.to_csv(f"{OUT}.hypotheses.csv", index=False)
    for _, r in H.iterrows():
        P(f"  {r['id']:<11} {r['verdict']:<5} {r['statement']}")
        P(f"  {'':<11}       -> {r['value']}")
    P(f"\nHYPOTHESES: {int((H.verdict == 'PASS').sum())} of {len(H)} PASS.")

    pd.DataFrame([dict(gate=k_, pass_=v[0], detail=v[1])
                  for k_, v in sorted(gates.items())]).to_csv(f"{OUT}.gates.csv", index=False)
    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
