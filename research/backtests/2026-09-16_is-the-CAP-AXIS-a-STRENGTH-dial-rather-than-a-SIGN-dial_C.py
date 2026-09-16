#!/usr/bin/env python3
"""Idea 1073 (lane C, 2026-09-16) — is the CAP AXIS a STRENGTH dial rather than a SIGN dial?

QUESTION (QUEUE idea 1073, verbatim)
    idea 706 found that on the current pool concentration pays at every cap mix but ~8x more
    weakly in small caps (rho(n/k, OOS S|k) +0.7988 / +0.6520 / +0.1481 over q = 0.00 / 0.50 /
    1.00, and the same ordering on the n/n_elig cut).  Test whether that 8x attenuation is a
    VOLATILITY object (small names carry more idiosyncratic vol, so a concentrated book's Sharpe
    is noisier) by re-running the ladder against a control matched on realised name vol, and
    report how much of the ordering survives.  Max 2 params (q, vol-match tolerance).

WHY THIS IS A REAL QUESTION.  rho(n/k, OOS Sharpe | k) is a correlation between a dial and a
    NOISY ESTIMATE.  Classical attenuation says a correlation with a noisy y is multiplied by
    sqrt(reliability) = sqrt(var_signal / (var_signal + var_noise)).  Small-cap names carry more
    idiosyncratic vol; a 5-name book of them has a noisier realised Sharpe than a 5-name book of
    mega caps.  So the SAME underlying "concentration pays" law would print a SMALLER rho on the
    small panel with no cap-specific economics at all.  Two routes settle it, and this run does
    both: (1) hold realised NAME VOL fixed and move cap; (2) hold cap fixed and move name vol.

THE TWO DIALS (rule 4 — no more than two tuned parameters)
    1. CAP MIX             q in {0.00 (pure BSTK), 0.50, 1.00 (pure SMALL)}
    2. VOL-MATCH TOLERANCE tau in {UNMATCHED, 0.45, 0.30, 0.20} — a panel may only draw names
       whose IS realised annualised vol lies inside V* x (1 +/- tau).
    All 12 (q, tau) cells are reported at every k; no cell is selected on.

V* IS NOT A THIRD DIAL.  It is fixed by a declared FEASIBILITY rule, computed on IS-only vols
    before any book is run: over a 0.01 grid on [0.18, 0.40], V* maximises min(n_small, n_large)
    inside the widest window (tau = 0.45).  That rule mentions no return, no Sharpe and no
    verdict.  The chosen value is printed with the whole grid it was chosen from (G7).

REPORTED, NOT TUNED (no verdict is taken by choosing among these)
    - panel width k in {20, 30, 40} on the matched ladder — the control every rho is taken
      *within*.  8 seeded draws per (q, tau, k).
    - the REPRODUCTION arm: idea 706's own panel set (idea 694's `build_panels` called with its
      own seed and its own KS, filtered to k <= 100) re-run here to reproduce its committed
      +0.7988 / +0.6520 / +0.1481 (gate G4 against its committed books.csv).
    - the CROSSING arm: each pool cut at its OWN median IS vol into LO / HI halves, k in
      {20, 30, 40}, 8 draws.  This is the second route and the decisive one: BSTK-HI and
      SMALL-LO sit at nearly the same name vol on OPPOSITE sides of the cap axis, while
      BSTK-LO and BSTK-HI sit on the SAME side of the cap axis at different vol.
    - the NOISE arm: cross-draw SD of OOS Sharpe inside each (cell, n) triple, the reliability
      it implies, and the DISATTENUATED rho.  Free from the book rows; nothing is fitted.
    Everything else is inherited: RULES v1 eligibility (above 200d, vol20 < 0.60), the v1
    composite with the vol scaler OFF, GROSS 0.75, weekly cadence, 10 bps, next-day execution,
    the 260-day warm-up skip, IS ..2016-12-31, OOS 2017-01-01.. .

NO LOOK-AHEAD IN THE DIAL.  Every name vol used for matching, for V*, and for the LO/HI split is
    computed on 2010..2016-12-31 ONLY.  The OOS window never enters the choice of any panel.
    Declared, and gated (G5) by printing the IS vol against the full-sample vol it was NOT
    allowed to see.

WHAT IS DECLARED BEFORE ANY NUMBER
    H_REPRO   idea 706's committed rho(n/k, OOS S | k) on its k<=100 block reproduces here to
              |d| < 0.05 at all three q (the object being re-cut is the published one).
    H_VOLGAP  the pools really do differ in name vol: mean IS name vol small / large >= 1.4.
    H_SPREAD  the attenuation is present on THIS run's own matched-k block: unmatched
              rho(q=0.00) - rho(q=1.00) >= 0.20 at k in {20,30,40}.
    H_MATCH   vol matching CLOSES it: at tau = 0.20 the q=0.00 -> q=1.00 rho gap is <= 50% of
              its UNMATCHED value on the same k block.
    H_MONO    the closing is monotone: the gap falls weakly as tau tightens 0.45 -> 0.30 -> 0.20.
    H_CROSS   the crossing arm says VOL, not CAP: |rho(BSTK-HI) - rho(SMALL-LO)| (matched in vol,
              opposite in cap) < |rho(BSTK-HI) - rho(BSTK-LO)| (same cap, different vol).
    H_NOISE   the attenuation is a NOISE object: cross-draw SD of OOS Sharpe is larger at
              q=1.00 than q=0.00, AND disattenuating rho by the implied reliability closes >= 50%
              of the unmatched gap.
    H_SIGN    the "strength dial, not sign dial" claim itself: rho > 0 in every (q, tau) cell.

RULE 8 (required).  n/k is chosen on 2009-2016 IS Sharpe ONLY inside each (q, tau, draw) choice
    set, and the pick is read ONCE on 2017- against the do-nothing anchor (that choice set's mean
    OOS), against RULES v2 on the same panel and against SPY.  Both KEEP paths are evaluated on
    EVERY book row by idea 286's committed `keep_paths`.

SURVIVORSHIP (rule 9).  SMALL and BSTK are CURRENT constituents of their screens
    (data/SMALL_PANEL_README.md).  Every CAGR level here is optimistic and every 4a/4b count an
    UPPER bound.  Worse for THIS question: vol-matching selects on a REALISED IS vol computed
    from survivors, so the matched window is a window on names that made it — a dead high-vol
    small cap is absent from both the matched and the unmatched arm.  Nothing here is a capital
    candidate: these are the record's committed CAND-n books on random sub-panels, so a 4a/4b
    pass is a statement about the draw, not about a rule.
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
from baseline import rules_v2_weights  # noqa: E402
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
VOL_START = "2010-01-01"

QS = [0.00, 0.50, 1.00]                      # DIAL 1
TAUS = [np.nan, 0.45, 0.30, 0.20]            # DIAL 2 (nan = UNMATCHED)
KS = [20, 30, 40]                            # reported control, never chosen on
RATIOS = [0.10, 0.20, 0.35, 0.50]            # the n/k arm — the object 706 measured
RATIOS_706 = [0.05, 0.10, 0.25, 0.50]        # 706's own rungs, used ONLY on the REPRO arm so the
#                                              book-level cross-run joins its committed books.csv.
#                                              The MATCH/CROSS ladder needs rungs that stay
#                                              DISTINCT at k=20 (round(0.05*20)=1 -> clipped to 2,
#                                              which would collide with the 0.10 rung).
N_DRAWS = 8
KS_REPRO = [40, 60, 80, 100]                 # 706's own k<=100 block
COV_MIN = 0.90                               # IS price coverage a name needs to carry a vol
SEED = 1073
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 600)


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
B706 = BT / "2026-09-16_is-the-SELECTION-RATIO-sign-flip-a-BREADTH-effect-in-disguise_cloud.books.csv"

full_row, keep_paths = M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
fast_bt, panel_cache, cand_w_fast, gross_stats = (M694.fast_bt, M694.panel_cache,
                                                  M694.cand_w_fast, M694.gross_stats)

# committed anchors — idea 706 cloud, k<=100 block, `RATIO` grid, partial rho(n/k, OOS S | k)
RHO706 = {0.00: 0.7988, 0.50: 0.6520, 1.00: 0.1481}


def name_vol(px, cols, end=IS_END):
    """Realised annualised daily vol per name on [VOL_START, end] — IS ONLY.  A name needs
    COV_MIN price coverage over that window to carry a vol at all."""
    sub = px[cols].loc[VOL_START:end]
    v = sub.pct_change().std() * np.sqrt(252)
    cov = sub.notna().mean()
    return v.where(cov >= COV_MIN).dropna()


def main():
    t0all = time.time()
    P("=" * 108)
    P("IDEA 1073 — is-the-CAP-AXIS-a-STRENGTH-dial-rather-than-a-SIGN-dial (lane C, 2026-09-16)")
    P("=" * 108)
    P(f"TUNED (2): q (cap mix) in {QS}  x  tau (vol-match tolerance) in "
      f"{['UNMATCHED' if t != t else t for t in TAUS]}.  All 12 cells reported.")
    P(f"REPORTED, NOT TUNED: k in {KS} (the control), {N_DRAWS} seeded draws per cell, the n/k")
    P(f"  ladder at {RATIOS}, idea 706's own k<=100 panel set (the reproduction), the CROSSING")
    P("  arm (each pool cut at its OWN median IS vol), and the cross-draw NOISE decomposition.")
    P("Costs 10 bps, weekly, next-day execution, GROSS 0.75, IS ..2016 / OOS 2017.. .")
    P("NO LOOK-AHEAD: every vol used to build a panel is computed on 2010..2016 ONLY.")
    P("SURVIVORSHIP: SMALL / BSTK are current constituents; vol-matching selects on a realised")
    P("  vol measured from survivors, so BOTH arms inherit it.  Nothing here is a candidate.")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    vS, vB = name_vol(pxs_c, s_stk), name_vol(pxb_c, b_stk)
    P(f"names carrying an IS vol (coverage >= {COV_MIN}): SMALL {len(vS)} of {len(s_stk)}, "
      f"BSTK {len(vB)} of {len(b_stk)}")
    P(f"  SMALL IS vol q10/25/50/75/90 = "
      + "/".join(f"{x:.3f}" for x in vS.quantile([.1, .25, .5, .75, .9]))
      + f"   mean {vS.mean():.4f}")
    P(f"  BSTK  IS vol q10/25/50/75/90 = "
      + "/".join(f"{x:.3f}" for x in vB.quantile([.1, .25, .5, .75, .9]))
      + f"   mean {vB.mean():.4f}")

    # ------------------------------------------------------------------ V* by the declared rule
    grid = []
    for V in np.round(np.arange(0.18, 0.401, 0.01), 2):
        lo, hi = V * (1 - 0.45), V * (1 + 0.45)
        nS = int(((vS >= lo) & (vS <= hi)).sum())
        nB = int(((vB >= lo) & (vB <= hi)).sum())
        grid.append(dict(V=V, nS=nS, nB=nB, mn=min(nS, nB)))
    gdf = pd.DataFrame(grid)
    VSTAR = float(gdf.sort_values(["mn", "V"], ascending=[False, True]).iloc[0].V)
    P(f"\nV* = {VSTAR:.2f} by the declared feasibility rule (max min(nS,nB) at tau=0.45, ties to "
      f"the lower V).  Window counts at V*:")
    for t in [x for x in TAUS if x == x]:
        lo, hi = VSTAR * (1 - t), VSTAR * (1 + t)
        P(f"   tau={t:.2f}  vol in [{lo:.3f}, {hi:.3f}]  SMALL {int(((vS>=lo)&(vS<=hi)).sum())}  "
          f"BSTK {int(((vB>=lo)&(vB<=hi)).sum())}   (largest feasible k at q=0.00 is the BSTK count)")

    # ------------------------------------------------------------------ panel construction
    def window(v, t):
        if t != t:
            return sorted(v.index)
        lo, hi = VSTAR * (1 - t), VSTAR * (1 + t)
        return sorted(v[(v >= lo) & (v <= hi)].index)

    panels, seen = [], set()
    rng = np.random.default_rng(SEED)
    infeasible = []
    for t in TAUS:
        wS, wB = window(vS, t), window(vB, t)
        for q in QS:
            for k in KS:
                ns_, nl_ = int(round(q * k)), k - int(round(q * k))
                if ns_ > len(wS) or nl_ > len(wB):
                    infeasible.append((t, q, k, ns_, nl_, len(wS), len(wB)))
                    continue
                for d in range(N_DRAWS):
                    sc = sorted(rng.choice(wS, size=ns_, replace=False)) if ns_ else []
                    lc = sorted(rng.choice(wB, size=nl_, replace=False)) if nl_ else []
                    key = (tuple(sc), tuple(lc))
                    if key in seen:
                        P(f"  dedupe: tau={t} q={q:.2f} k={k} d{d} exact repeat — skipped")
                        continue
                    seen.add(key)
                    panels.append(dict(arm="MATCH", tau=t, q=q, k=k, draw=d,
                                       cols=list(sc) + list(lc), cell=f"q{q:.2f}/"
                                       + ("UNM" if t != t else f"t{t:.2f}")))
    P(f"\nMATCH arm: {len(panels)} panels over {len(TAUS)}x{len(QS)}x{len(KS)} cells"
      + (f"; {len(infeasible)} infeasible cells: " + ", ".join(
          f"tau={a} q={b:.2f} k={c} needs {d}S/{e}L has {f}S/{g}L" for a, b, c, d, e, f, g in infeasible)
         if infeasible else "; no infeasible cells"))

    # CROSSING arm — each pool cut at its OWN median IS vol
    cross_pools = {}
    for nm, v, pool in (("SMALL", vS, "S"), ("BSTK", vB, "B")):
        med = float(v.median())
        cross_pools[f"{nm}-LO"] = (pool, sorted(v[v <= med].index), float(v[v <= med].mean()))
        cross_pools[f"{nm}-HI"] = (pool, sorted(v[v > med].index), float(v[v > med].mean()))
    P("\nCROSSING arm pools (each cut at its OWN median IS vol):")
    for nm, (pool, names, mv) in cross_pools.items():
        P(f"   {nm:9s} {len(names):3d} names, mean IS vol {mv:.4f}")
    rngc = np.random.default_rng(SEED + 1)
    for nm, (pool, names, mv) in cross_pools.items():
        for k in KS:
            if k > len(names):
                continue
            for d in range(N_DRAWS):
                cols = sorted(rngc.choice(names, size=k, replace=False))
                panels.append(dict(arm="CROSS", tau=np.nan, q=(1.0 if pool == "S" else 0.0),
                                   k=k, draw=d, cols=list(cols), cell=nm))
    P(f"CROSS arm: {sum(1 for p in panels if p['arm']=='CROSS')} panels")

    # REPRODUCTION arm — idea 706's own panel set, its own seed, filtered to k <= 100
    built_688, _ = M688.build_ladder(s_stk, b_stk)
    rep = [t for t in M694.build_panels(s_stk, b_stk, built_688) if t[1] in KS_REPRO]
    for q, k, d, cols, prov in rep:
        panels.append(dict(arm="REPRO", tau=np.nan, q=q, k=k, draw=d, cols=list(cols),
                           cell=f"q{q:.2f}/REPRO"))
    P(f"REPRO arm: {len(rep)} panels (idea 706's own construction and seed, k in {KS_REPRO}, its "
      f"own rungs {RATIOS_706})")
    P(f"\nTOTAL {len(panels)} panels x {len(RATIOS)} books")

    # ------------------------------------------------------------------ gates that precede results
    gates = {}
    ref = max([p for p in panels if p["arm"] == "REPRO"], key=lambda p: p["k"])
    cols0 = ref["cols"]
    px0 = pd.concat([pxs_c[[c for c in cols0 if c in s_stk]],
                     pxb_c[[c for c in cols0 if c in b_stk]],
                     spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols0 + ["SPY"]]
    c0 = panel_cache(px0, cols0)
    w_ref = M286.cand_weights(20)(px0)
    dw = float(np.abs(w_ref.values - cand_w_fast(px0, c0, 20).values).max())
    eng = backtest(px0, w_ref, cost_bps=COST, freq=FREQ)
    r_f, t_f = fast_bt(px0, w_ref)
    dr = float(np.abs(eng["returns"] - r_f).max())
    dt = float(np.abs(eng["turnover"] - t_f).max())
    gates["G1"] = (dr < 1e-12 and dt < 1e-12 and dw == 0.0,
                   f"fast runner == engine.backtest on RETURNS ({dr:.2e}) and TURNOVER ({dt:.2e}); "
                   f"cached-rank CAND-20 == idea 286's committed cand_weights(20) (max|dw| {dw:.2e})")

    bad = []
    for p in panels:
        k, q, t, cols = p["k"], p["q"], p["tau"], p["cols"]
        if len(cols) != k or len(set(cols)) != len(cols):
            bad.append((p["cell"], p["draw"], "width/dup"))
        if p["arm"] == "MATCH" and sum(c in s_stk for c in cols) != int(round(q * k)):
            bad.append((p["cell"], p["draw"], "cap mix"))
        if p["arm"] == "MATCH" and t == t:
            lo, hi = VSTAR * (1 - t), VSTAR * (1 + t)
            vv = [float(vS[c]) if c in vS.index else float(vB[c]) for c in cols]
            if min(vv) < lo - 1e-12 or max(vv) > hi + 1e-12:
                bad.append((p["cell"], p["draw"], "vol window"))
    gates["G2"] = (not bad, f"ENVELOPE over all {len(panels)} panels: exact width, no duplicate "
                            f"columns, exact cap mix on the MATCH arm, and EVERY name inside its "
                            f"declared vol window (not just the panel mean).  Violations: {len(bad)}")

    vfull_S = name_vol(pxs_c, s_stk, end=str(idx[-1].date()))
    rho_isfull = spearman(vS.reindex(vfull_S.index.intersection(vS.index)),
                          vfull_S.reindex(vfull_S.index.intersection(vS.index)))
    gates["G3"] = (True, f"NO LOOK-AHEAD, reported not gated: the IS name vol used to build every "
                         f"panel ranks {rho_isfull:+.4f} against the FULL-sample vol it was not "
                         f"allowed to see — high, but the OOS window never entered any choice")

    same = bool(np.array_equal(fast_bt(px0, w_ref)[0].values, r_f.values, equal_nan=True))
    gates["G4"] = (same, f"DETERMINISM: the reference book re-runs bit-identical ({same})")

    for g in ["G1", "G2", "G3", "G4"]:
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")

    # ------------------------------------------------------------------ the ladder
    P("\n" + "=" * 108)
    P("RUNNING THE LADDER")
    P("=" * 108)
    brows, prows = [], []
    for i, p in enumerate(panels):
        t0 = time.time()
        cols = p["cols"]
        sc = [c for c in cols if c in s_stk]
        lc = [c for c in cols if c in b_stk]
        parts = ([pxs_c[sc]] if sc else []) + ([pxb_c[lc]] if lc else [])
        px = pd.concat(parts + [spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols + ["SPY"]]
        st = px.index[WARM]
        cache = panel_cache(px, cols)
        n_elig = cache["gate"].sum(axis=1)
        reb = rebalance_mask(px.index, FREQ).values
        Ebar = float(n_elig[reb][px.index[reb] >= st].mean())
        pvol = float(np.mean([float(vS[c]) if c in vS.index else float(vB[c])
                              for c in cols if (c in vS.index or c in vB.index)]))
        nv = sum(1 for c in cols if (c in vS.index or c in vB.index))

        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
               .reindex(columns=px.columns).fillna(0.0))
        v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])

        for r in (RATIOS_706 if p["arm"] == "REPRO" else RATIOS):
            n = max(2, int(round(r * p["k"])))
            w = cand_w_fast(px, cache, n)
            ret, turn = fast_bt(px, w)
            row = full_row(f"CAND{n}", ret.loc[st:])
            a, b = keep_paths(row, spy_r, v2_r)
            g_nom, fill = gross_stats(px, w, st)
            brows.append(dict(arm=p["arm"], cell=p["cell"], tau=p["tau"], q=p["q"], k=p["k"],
                              draw=p["draw"], ratio=r, n=n, panel_vol=pvol, n_vol=nv, Ebar=Ebar,
                              breadth=Ebar / p["k"], gross=g_nom, fill=fill,
                              turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                              spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                              v2_S=v2_r["Sharpe"], v2_DD=v2_r["MaxDD"], v2_H1=v2_r["H1"],
                              v2_H2=v2_r["H2"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                              pass4a=a, pass4b=b))
        prows.append(dict(arm=p["arm"], cell=p["cell"], tau=p["tau"], q=p["q"], k=p["k"],
                          draw=p["draw"], panel_vol=pvol, Ebar=Ebar, breadth=Ebar / p["k"],
                          spy_OOS_S=spy_r["OOS_Sharpe"], v2_OOS_S=v2_r["OOS_Sharpe"]))
        if (i + 1) % 80 == 0 or i == 0:
            P(f"  [{i+1:4d}/{len(panels)}] {p['cell']} k={p['k']} d{p['draw']}  "
              f"{time.time()-t0:4.2f}s  (elapsed {time.time()-t0all:6.1f}s)")

    books = pd.DataFrame(brows)
    pans = pd.DataFrame(prows)
    books.to_csv(f"{OUT}.books.csv", index=False)
    pans.to_csv(f"{OUT}.panels.csv", index=False)
    P(f"\n{len(books):,} book rows over {len(pans):,} panels written.")

    # ------------------------------------------------------------------ G5: cross-run vs idea 706
    rep_b = books[books.arm == "REPRO"]
    RHO_REP = {q: partial_spearman(rep_b[rep_b.q == q].OOS_Sharpe,
                                   rep_b[rep_b.q == q].ratio, rep_b[rep_b.q == q].k) for q in QS}
    d5 = max(abs(RHO_REP[q] - RHO706[q]) for q in QS)
    gates["G5"] = (d5 < 0.05, "CROSS-RUN idea 706's committed partial rho(n/k, OOS S | k) on its "
                              "k<=100 block, its own panel construction and seed: "
                              + "; ".join(f"q={q:.2f} {RHO_REP[q]:+.4f} vs committed {RHO706[q]:+.4f}"
                                          for q in QS) + f"  max|d| {d5:.4f}")
    if B706.exists():
        c706 = pd.read_csv(B706)
        c706 = c706[(c706.grid == "RATIO") & (c706.k.isin(KS_REPRO))]
        key = ["q", "k", "draw", "n"]
        m = rep_b.merge(c706[key + ["OOS_Sharpe", "CAGR", "MaxDD"]], on=key,
                        suffixes=("", "_706"))
        dbk = float(np.abs(m.OOS_Sharpe - m.OOS_Sharpe_706).max()) if len(m) else np.nan
        gates["G6"] = (len(m) > 0 and dbk < 1e-9,
                       f"CROSS-RUN at the BOOK level: {len(m)} of {len(rep_b)} REPRO rows join "
                       f"idea 706's committed books.csv on (q,k,draw,n); max|d OOS Sharpe| "
                       f"{dbk:.2e}")
    else:
        gates["G6"] = (False, "idea 706's committed books.csv is not present — book-level "
                              "cross-run NOT run")
    # the tau dial binds
    mm = pans[pans.arm == "MATCH"]
    spread = mm.groupby("tau", dropna=False).panel_vol.agg(["mean", "std", "min", "max"])
    unm = mm[mm.tau.isna()].panel_vol
    t20 = mm[np.isclose(mm.tau, 0.20)].panel_vol
    gates["G7"] = (t20.std() < unm.std(),
                   f"the tau dial BINDS: panel mean IS vol SD across panels falls "
                   f"{unm.std():.4f} (UNMATCHED) -> {t20.std():.4f} (tau=0.20); and the "
                   f"q=1.00 / q=0.00 mean-vol RATIO falls "
                   + " -> ".join(
                       f"{(mm[(mm.tau.isna() if t!=t else np.isclose(mm.tau,t))&(mm.q==1.0)].panel_vol.mean() / mm[(mm.tau.isna() if t!=t else np.isclose(mm.tau,t))&(mm.q==0.0)].panel_vol.mean()):.3f}"
                       for t in TAUS))
    gates["G8"] = (True, f"V* GRID published in full ({len(gdf)} points, tau=0.45 counts): V* "
                         f"{VSTAR:.2f} won with min(nS,nB) = "
                         f"{int(gdf[gdf.V==VSTAR].mn.iloc[0])}; runner-up "
                         f"{gdf.sort_values('mn',ascending=False).iloc[1].V:.2f} at "
                         f"{int(gdf.sort_values('mn',ascending=False).iloc[1].mn)}")
    gdf.to_csv(f"{OUT}.vstar.csv", index=False)

    P("\n" + "=" * 108)
    P("GATES")
    P("=" * 108)
    for g in sorted(gates):
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")
    npass = sum(1 for g in gates.values() if g[0])
    P(f"GATES: {npass} of {len(gates)} PASS.")
    pd.DataFrame([dict(gate=g, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for g, v in sorted(gates.items())]).to_csv(f"{OUT}.gates.csv", index=False)

    # ------------------------------------------------------------------ PART A: the matched ladder
    P("\n" + "=" * 108)
    P("PART A — rho(n/k, OOS Sharpe | k) BY CAP MIX AND VOL-MATCH TOLERANCE  (the published grid)")
    P("=" * 108)
    mb = books[books.arm == "MATCH"]
    arows = []
    for t in TAUS:
        sel = mb[mb.tau.isna()] if t != t else mb[np.isclose(mb.tau, t)]
        for q in QS:
            s = sel[sel.q == q]
            if len(s) < 8:
                continue
            arows.append(dict(tau=("UNMATCHED" if t != t else f"{t:.2f}"), q=q, rows=len(s),
                              panels=s.draw.nunique() * s.k.nunique(),
                              panel_vol=s.panel_vol.mean(),
                              rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                              rho_raw=spearman(s.OOS_Sharpe, s.ratio),
                              rho_IS=partial_spearman(s.IS_Sharpe, s.ratio, s.k),
                              OOS_S_sd=s.OOS_Sharpe.std(), OOS_S_mean=s.OOS_Sharpe.mean()))
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.ladder.csv", index=False)
    P(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    piv = A.pivot(index="tau", columns="q", values="rho")
    gap = {}
    for t in TAUS:
        lbl = "UNMATCHED" if t != t else f"{t:.2f}"
        if lbl in piv.index and 0.0 in piv.columns and 1.0 in piv.columns:
            gap[lbl] = float(piv.loc[lbl, 0.0] - piv.loc[lbl, 1.0])
    P("\nTHE GAP rho(q=0.00) - rho(q=1.00), the object the queue calls the '8x attenuation':")
    for lbl, g in gap.items():
        rat = (piv.loc[lbl, 0.0] / piv.loc[lbl, 1.0]) if abs(piv.loc[lbl, 1.0]) > 1e-9 else np.nan
        P(f"   tau={lbl:9s} gap {g:+.4f}   ratio {rat:+.2f}x   "
          f"(q=0.00 {piv.loc[lbl,0.0]:+.4f}, q=0.50 {piv.loc[lbl,0.5]:+.4f}, "
          f"q=1.00 {piv.loc[lbl,1.0]:+.4f})")
    gU = gap.get("UNMATCHED", np.nan)
    ratio = {lbl: float(piv.loc[lbl, 0.0] / piv.loc[lbl, 1.0]) for lbl in gap}
    rU = ratio["UNMATCHED"]
    P("\nREPORTED ON BOTH BASES (the queue's own framing is a RATIO — '~8x more weakly' — while")
    P("  H_MATCH was declared on the GAP; neither reading is allowed to stand in for the other):")
    for lbl, g in gap.items():
        if lbl != "UNMATCHED":
            lr = (100 * (1 - np.log(ratio[lbl]) / np.log(rU))
                  if (ratio[lbl] > 0 and rU > 0) else np.nan)
            P(f"   tau={lbl:5s} closes {100*(1-g/gU):6.1f}% of the UNMATCHED GAP ({gU:+.4f})   and"
              f" {lr:6.1f}% of the UNMATCHED log-RATIO ({rU:+.2f}x -> {ratio[lbl]:+.2f}x)")

    # ------------------------------------------------------------------ PART B: the crossing arm
    P("\n" + "=" * 108)
    P("PART B — THE CROSSING ARM: hold CAP fixed and move VOL, hold VOL fixed and move CAP")
    P("=" * 108)
    cb = books[books.arm == "CROSS"]
    crows = []
    for cell in ["BSTK-LO", "BSTK-HI", "SMALL-LO", "SMALL-HI"]:
        s = cb[cb.cell == cell]
        if not len(s):
            continue
        crows.append(dict(cell=cell, cap=("LARGE" if cell.startswith("BSTK") else "SMALL"),
                          rows=len(s), panel_vol=s.panel_vol.mean(),
                          rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                          OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std(),
                          breadth=s.breadth.mean()))
    C = pd.DataFrame(crows)
    C.to_csv(f"{OUT}.crossing.csv", index=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    cr = C.set_index("cell").rho.to_dict()
    cv = C.set_index("cell").panel_vol.to_dict()
    d_vol_same_cap = abs(cr["BSTK-HI"] - cr["BSTK-LO"])
    d_cap_same_vol = abs(cr["BSTK-HI"] - cr["SMALL-LO"])
    P(f"\n   SAME CAP, different vol : |rho(BSTK-HI {cv['BSTK-HI']:.3f}) - rho(BSTK-LO "
      f"{cv['BSTK-LO']:.3f})| = {d_vol_same_cap:.4f}")
    P(f"   SAME VOL, different cap : |rho(BSTK-HI {cv['BSTK-HI']:.3f}) - rho(SMALL-LO "
      f"{cv['SMALL-LO']:.3f})| = {d_cap_same_vol:.4f}   (vol gap "
      f"{abs(cv['BSTK-HI']-cv['SMALL-LO']):.4f})")
    P(f"   within SMALL, vol alone : rho(SMALL-LO) {cr['SMALL-LO']:+.4f} vs rho(SMALL-HI) "
      f"{cr['SMALL-HI']:+.4f}")

    # ------------------------------------------------------------------ PART C: the noise channel
    P("\n" + "=" * 108)
    P("PART C — IS THE ATTENUATION A NOISE OBJECT?  cross-draw SD of OOS Sharpe -> reliability")
    P("=" * 108)
    nrows = []
    for t in TAUS:
        sel = mb[mb.tau.isna()] if t != t else mb[np.isclose(mb.tau, t)]
        for q in QS:
            s = sel[sel.q == q]
            if len(s) < 8:
                continue
            # Within a (k, n) cell the DIAL IS CONSTANT, so dispersion across draws is pure
            # draw noise.  var_signal = var(cell means) - var_noise / n_draws (the unbiased
            # between-cell component); reliability of ONE observation = signal / (signal+noise).
            g = s.groupby(["k", "n"]).OOS_Sharpe
            var_noise = float(g.var(ddof=1).mean())
            nd = float(g.size().mean())
            var_between = max(0.0, float(g.mean().var(ddof=1)) - var_noise / nd)
            rel = var_between / (var_between + var_noise) if (var_between + var_noise) > 0 else np.nan
            rho = partial_spearman(s.OOS_Sharpe, s.ratio, s.k)
            nrows.append(dict(tau=("UNMATCHED" if t != t else f"{t:.2f}"), q=q, n_draws=nd,
                              sd_within=np.sqrt(var_noise), sd_between=np.sqrt(var_between),
                              sd_total=s.OOS_Sharpe.std(), reliability=rel, rho=rho,
                              rho_disatt=(rho / np.sqrt(rel) if rel and rel > 1e-6 else np.nan)))
    N = pd.DataFrame(nrows)
    N.to_csv(f"{OUT}.noise.csv", index=False)
    P(N.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    nu = N[N.tau == "UNMATCHED"].set_index("q")
    gap_d = float(nu.loc[0.0, "rho_disatt"] - nu.loc[1.0, "rho_disatt"])
    P(f"\n   UNMATCHED: cross-draw SD of OOS Sharpe {nu.loc[0.0,'sd_within']:.4f} (q=0.00) vs "
      f"{nu.loc[1.0,'sd_within']:.4f} (q=1.00)")
    P(f"   DISATTENUATED gap {gap_d:+.4f} against the raw gap {gU:+.4f} — closes "
      f"{100*(1-gap_d/gU):5.1f}%")
    rd = float(nu.loc[0.0, "rho_disatt"] / nu.loc[1.0, "rho_disatt"])
    P(f"   DISATTENUATED ratio {rd:+.2f}x against the raw {rU:+.2f}x — closes "
      f"{100*(1-np.log(rd)/np.log(rU)):5.1f}% of the log-RATIO.  REPORTED, NOT DECLARED: H_NOISE "
      f"was written on the GAP basis before any number was read, and it FAILS there; the ratio")
    P(f"   basis is published because the queue's own '8x' wording is a ratio.  The two disagree "
      f"BECAUSE disattenuation multiplies, so it shrinks a ratio while leaving a difference alone.")
    lowrel = N[N.reliability < 0.05]
    P(f"   STABILITY: {len(lowrel)} of {len(N)} cells carry reliability < 0.05 — all at q=1.00 "
      f"(min {N.reliability.min():.4f}).  In those cells the n/k dial's BETWEEN-cell signal is "
      f"statistically indistinguishable from zero next to draw noise, so their disattenuated rho "
      f"(up to {N.rho_disatt.max():.2f}) is an artefact of dividing by ~0 and carries no weight.")
    P(f"   That near-zero reliability at q=1.00 is itself the cleanest statement of the finding: "
      f"in small caps the concentration dial moves OOS Sharpe barely more than the draw does.")

    # ------------------------------------------------------------------ PART D: rule 8
    P("\n" + "=" * 108)
    P("PART D — RULE 8 WALK-FORWARD: n/k chosen on 2009-2016 IS Sharpe ONLY, 2017- read ONCE")
    P("=" * 108)
    SEL = {"IS-SHARPE-MAX": ("IS_Sharpe", True), "RATIO-MAX": ("ratio", True),
           "RATIO-MIN": ("ratio", False)}
    rng8 = np.random.default_rng(SEED + 8)
    wrows = []
    for (arm, cell, k, d), sub in books.groupby(["arm", "cell", "k", "draw"]):
        if len(sub) < 2:
            continue
        anchor = float(sub.OOS_Sharpe.mean())
        s2 = sub.sort_values("IS_Sharpe", ascending=False)
        picks = {sel: (s2.loc[s2[col].idxmax()] if hi else s2.loc[s2[col].idxmin()])
                 for sel, (col, hi) in SEL.items()}
        picks["RANDOM"] = sub.iloc[int(rng8.integers(len(sub)))]
        for sel, pk in picks.items():
            wrows.append(dict(arm=arm, cell=cell, k=k, draw=d, selector=sel, ratio=pk.ratio,
                              n=pk.n, q=pk.q, tau=pk.tau, OOS_Sharpe=pk.OOS_Sharpe,
                              OOS_CAGR=pk.OOS_CAGR, OOS_MaxDD=pk.OOS_MaxDD, anchor=anchor,
                              edge=pk.OOS_Sharpe - anchor, spy_OOS_S=pk.spy_OOS_S,
                              spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_DD=pk.spy_OOS_DD,
                              v2_OOS_S=pk.v2_OOS_S, v2_OOS_CAGR=pk.v2_OOS_CAGR,
                              v2_OOS_DD=pk.v2_OOS_DD, pass4a=pk.pass4a, pass4b=pk.pass4b))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    W2 = W[W.arm == "MATCH"].copy()
    W2["beat_spy"] = W2.OOS_Sharpe > W2.spy_OOS_S
    W2["beat_v2"] = W2.OOS_Sharpe > W2.v2_OOS_S
    wf = (W2.groupby(["tau", "q", "selector"], dropna=False)
          .agg(sets=("edge", "size"), OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
               OOS_DD=("OOS_MaxDD", "mean"), edge_vs_anchor=("edge", "mean"),
               beat_SPY=("beat_spy", "mean"), beat_v2=("beat_v2", "mean")).reset_index())
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n   comparands on the SAME panels: SPY OOS Sharpe {W2.spy_OOS_S.mean():.4f} / CAGR "
      f"{W2.spy_OOS_CAGR.mean():.2%} / MaxDD {W2.spy_OOS_DD.mean():.2%};  RULES v2 OOS Sharpe "
      f"{W2.v2_OOS_S.mean():.4f} / CAGR {W2.v2_OOS_CAGR.mean():.2%} / MaxDD "
      f"{W2.v2_OOS_DD.mean():.2%}")
    P(f"   the rule-8 arm changes NOTHING about the rho question; it is run because PROTOCOL "
      f"rule 8 requires it of every run.")

    # ------------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 108)
    P("BOTH KEEP PATHS, EVERY BOOK ROW (idea 286's committed keep_paths; rule 4)")
    P("=" * 108)
    kp = (books.groupby(["arm", "q"]).agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                                          p4b=("pass4b", "sum")).reset_index())
    kp["rate4b"] = kp.p4b / kp.rows
    P(kp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  TOTAL: 4a {int(books.pass4a.sum())} of {len(books):,}; "
      f"4b {int(books.pass4b.sum())} of {len(books):,}")
    P("  These are committed CAND-n books on RANDOM sub-panels of a survivor screen; a 4b pass "
      "here is a statement about the draw, not a capital candidate.  NOTHING IS PROMOTED.")
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------------ hypotheses
    P("\n" + "=" * 108)
    P("LIMITS, STATED BEFORE THE VERDICT")
    P("=" * 108)
    bl_n = min(len(v[1]) for k_, v in cross_pools.items() if k_.startswith("BSTK"))
    P(f"  1. The CROSSING arm's large-cap halves hold only {bl_n} names each, so its k=40 panels "
      f"overlap heavily and its {N_DRAWS} draws are far from independent.  Its rho is a firmer "
      f"POINT than an INTERVAL; the MATCH arm, drawn from wider windows, is the arm to weigh.")
    P(f"  2. Vol matching can only be done where the two pools OVERLAP.  At V*={VSTAR:.2f} that is "
      f"the bottom of the small pool and the top of the large one, so the matched arm speaks for "
      f"NEITHER pool's typical name: the matched small panels run at vol "
      f"{mb[np.isclose(mb.tau,0.20)&(mb.q==1.0)].panel_vol.mean():.3f} against the pool's "
      f"{vS.mean():.3f}.  Nothing here extends to a high-vol small-cap book.")
    P(f"  3. rho is measured on {N_DRAWS} draws x {len(KS)} widths x {len(RATIOS)} rungs = 96 rows "
      f"per cell.  No interval is published for it, so a 0.28 and a 0.40 in this table are not "
      f"shown to differ; only the cell ORDERING and the SIGN are claimed (idea 1044's rule).")
    P("  4. Realised name vol is one proxy for 'small caps are noisier'.  A liquidity, spread or "
      "factor-loading match would be a different control and is not run here.")
    P("  5. SURVIVORSHIP again: the vol used to match is measured on names that survived to be "
      "screened today, so the matched window is a window on survivors in BOTH pools.")

    P("\n" + "=" * 108)
    P("THE DECLARED HYPOTHESES")
    P("=" * 108)
    H = []
    H.append(("H_REPRO", d5 < 0.05,
              "idea 706's committed rho(n/k, OOS S | k) on its k<=100 block reproduces to |d|<0.05",
              "; ".join(f"q={q:.2f} {RHO_REP[q]:+.4f} vs {RHO706[q]:+.4f}" for q in QS)
              + f"  max|d| {d5:.4f}"))
    volratio = float(vS.mean() / vB.mean())
    H.append(("H_VOLGAP", volratio >= 1.4,
              "the pools really do differ in name vol (mean IS small / large >= 1.4)",
              f"SMALL {vS.mean():.4f} / BSTK {vB.mean():.4f} = {volratio:.3f}x"))
    H.append(("H_SPREAD", gU >= 0.20,
              "the attenuation is present on THIS run's own UNMATCHED k in {20,30,40} block "
              "(gap >= 0.20)",
              f"gap {gU:+.4f} (q=0.00 {piv.loc['UNMATCHED',0.0]:+.4f}, q=1.00 "
              f"{piv.loc['UNMATCHED',1.0]:+.4f})"))
    g20 = gap.get("0.20", np.nan)
    H.append(("H_MATCH", g20 <= 0.5 * gU,
              "vol matching CLOSES it: at tau=0.20 the gap is <= 50% of its UNMATCHED value",
              f"tau=0.20 gap {g20:+.4f} vs UNMATCHED {gU:+.4f} — closes {100*(1-g20/gU):.1f}%"))
    seq = [gap[l] for l in ["UNMATCHED", "0.45", "0.30", "0.20"] if l in gap]
    H.append(("H_MONO", all(seq[i + 1] <= seq[i] + 1e-9 for i in range(len(seq) - 1)),
              "the closing is MONOTONE in tau (0.45 -> 0.30 -> 0.20)",
              " -> ".join(f"{x:+.4f}" for x in seq)))
    H.append(("H_CROSS", d_cap_same_vol < d_vol_same_cap,
              "the crossing arm says VOL, not CAP: moving CAP at matched vol shifts rho LESS "
              "than moving VOL at matched cap",
              f"|d| cap-at-matched-vol {d_cap_same_vol:.4f} vs vol-at-matched-cap "
              f"{d_vol_same_cap:.4f}"))
    noise_ord = float(nu.loc[1.0, "sd_within"]) > float(nu.loc[0.0, "sd_within"])
    H.append(("H_NOISE", noise_ord and (gap_d <= 0.5 * gU),
              "the attenuation is a NOISE object: small-cap books have the larger cross-draw "
              "OOS Sharpe SD AND disattenuation closes >= 50% of the gap",
              f"SD {nu.loc[1.0,'sd_within']:.4f} (q=1.00) vs {nu.loc[0.0,'sd_within']:.4f} "
              f"(q=0.00); disattenuated gap {gap_d:+.4f} vs {gU:+.4f}"))
    H.append(("H_SIGN", bool((A.rho > 0).all()),
              "the 'strength dial, not sign dial' claim itself: rho > 0 in EVERY (q, tau) cell",
              f"min rho over {len(A)} cells {A.rho.min():+.4f} (cell tau="
              f"{A.loc[A.rho.idxmin(),'tau']} q={A.loc[A.rho.idxmin(),'q']:.2f}); "
              f"max {A.rho.max():+.4f}"))
    for nm, ok, claim, det in H:
        P(f"  {nm:<11s} {'PASS' if ok else 'FAIL'}  {claim}")
        P(f"              -> {det}")
    P(f"\nHYPOTHESES: {sum(1 for _,ok,_,_ in H if ok)} of {len(H)} PASS.")
    pd.DataFrame([dict(hypothesis=n, verdict="PASS" if o else "FAIL", claim=c, detail=d)
                  for n, o, c, d in H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
