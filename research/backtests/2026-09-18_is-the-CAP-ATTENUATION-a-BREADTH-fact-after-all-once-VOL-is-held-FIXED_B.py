#!/usr/bin/env python3
"""Idea 1080 (lane B, 2026-09-18) — is the CAP ATTENUATION a BREADTH fact after all, once VOL is
held FIXED?

QUESTION (QUEUE idea 1080, verbatim)
    idea 1073's crossing arm shows breadth falling monotonically with the same ordering rho does
    (0.7376 / 0.6796 / 0.5943 / 0.4179 over BSTK-LO / BSTK-HI / SMALL-LO / SMALL-HI), so the
    surviving cap effect may be idea 706's breadth axis re-entering through the 200d gate rather
    than cap itself.  Re-run the vol-matched ladder with panels additionally matched on realised
    breadth, and report how much of the 0.4063 cap shift survives.  Max 2 params (q, breadth-match
    tolerance).

THE OBJECT.  "The 0.4063 cap shift" is idea 1073's CROSSING arm line 103:
    |rho(BSTK-HI, panel vol 0.325) - rho(SMALL-LO, panel vol 0.297)| = 0.4063 (vol gap 0.0277)
i.e. move CAP while VOL is already matched and the partial rho(n/k, OOS Sharpe | k) moves 0.4063.
1073 read that as the cap axis surviving a vol control.  1080 asks whether BREADTH — the mean
fraction of the panel that passes the 200d/vol20 gate on a rebalance day — is what actually moved.

THE TWO DIALS (rule 4 — no more than two tuned parameters)
    1. q                     the cap mix, {0.00 (pure BSTK), 0.50, 1.00 (pure SMALL)} on the
                             MATCH ladder; on the CROSSING arms the cap axis is the cell itself.
    2. beta                  BREADTH-MATCH TOLERANCE.  A panel may only draw names whose IS
                             breadth lies inside B* x (1 +/- beta).  UNMATCHED is the zero rung.
    Every cell is reported.  Nothing is selected on.

FROZEN, INHERITED FROM 1073 — NOT TUNED HERE.  The vol control is the one 1073 published and is
    not re-opened: V* = 0.25, vol window tau = 0.20 (its tightest), the CROSSING cells (each pool
    cut at its OWN median IS vol), RULES v1 eligibility (above 200d, vol20 < 0.60), the v1
    composite with the vol scaler OFF, GROSS 0.75, weekly cadence, 10 bps, next-day execution, the
    260-day warm-up skip, IS ..2016-12-31, OOS 2017-01-01.., the n/k rungs {0.10,0.20,0.35,0.50}.

B* IS NOT A THIRD DIAL.  Like 1073's V* it is fixed by a declared FEASIBILITY rule computed on
    IS-only breadths before any book is run, at the WIDEST beta of its arm, and then held for every
    tighter beta.  CROSS arm: over a 0.01 grid on [0.30, 0.90], B* maximises min(n(BSTK-HI),
    n(SMALL-LO)) — the two cells the 0.4063 shift is taken between — inside beta = 0.25.  MATCH
    arm: the same grid, maximising min(n_small, n_large) inside the tau=0.20 vol window at
    beta = 0.20.  Neither rule mentions a return, a Sharpe or a verdict.  Both grids are published.

WHICH BREADTH.  1073's committed 0.7376/0.6796/0.5943/0.4179 are FULL-SAMPLE panel breadths
    (Ebar/k from the warm-up date to the end of the tape) — they see the OOS window.  They cannot
    be used to BUILD a panel.  Matching here therefore uses a per-name IS-ONLY breadth: the
    fraction of weekly rebalance days in [index[260], 2016-12-31] on which that name passes the
    v1 gate.  The gate is per-name (own 200d MA, own 20d vol), so a panel's mean IS breadth is
    exactly the mean of its names' IS breadths — the match is exact, not approximate.  BOTH
    measures are carried on every panel row and the FULL-SAMPLE one is gated against 1073's
    committed four (G6), so the two readings can be compared rather than conflated.

WHAT WAS SEEN BEFORE THE HYPOTHESES WERE WRITTEN (declared, because it matters).  Fixing B* and
    checking feasibility required a pre-run pass over the IS breadths.  That pass printed the pool
    and cell means, so H_BGAP and the near-equality noted in H_ALREADY are REPORTED, not blind.
    Nothing about any rho, Sharpe or book return was computed in it, so H_SURVIVE, H_MONO,
    H_BCROSS, H_LADDER and H_SIGN are blind.

THE ARMS
    REPRO   1073's crossing arm replayed bit-for-bit (its pools, its seed 1074, k in {20,30,40},
            8 draws, no breadth window) to reproduce the committed 0.4063 and the four breadths.
    CROSS   the same four cells with a breadth window at beta in {UNMATCHED, 0.25, 0.20, 0.15},
            k in {20, 30}, 12 draws.  The HEADLINE comparison is the COMMON k=20 block, declared
            in advance, because k=30 is infeasible in some cells at the tighter betas and a block
            that changes with the dial would confound the answer.
    CROSSB  the MIRROR, and the decisive one: each pool cut at its OWN median IS BREADTH into
            BLO/BHI, k in {20,30,40}, 8 draws.  This holds CAP fixed and moves BREADTH.  If
            breadth is what 1073 was measuring, moving it at fixed cap must shift rho at least as
            hard as moving cap at fixed vol did.
    MATCH   the vol-matched LADDER itself: panels drawn from 1073's tau=0.20 vol window,
            additionally inside the breadth window, q x beta x k in {20,30} x 16 draws.

RULE 8 (required).  n/k is chosen on 2009-2016 IS Sharpe ONLY inside each (arm, cell, k, draw)
    choice set and the pick is read ONCE on 2017- against that choice set's mean OOS (the
    do-nothing anchor), against RULES v2 on the same panel and against SPY.  OOS CAGR / Sharpe /
    MaxDD are reported for every selector including RANDOM.

BOTH KEEP PATHS are evaluated on EVERY book row by idea 286's committed `keep_paths`.

SURVIVORSHIP (rule 9).  SMALL and BSTK are CURRENT constituents of their screens
    (data/SMALL_PANEL_README.md).  Every CAGR level is optimistic and every 4a/4b count an UPPER
    bound.  Worse for THIS question: breadth is measured as a realised gate-pass rate on names
    that survived to be screened today, so a high-breadth window is doubly a survivor window — a
    name that spent 2011-2015 under its 200d MA and then delisted is in neither arm.  Nothing here
    is a capital candidate: these are the record's committed CAND-n books on random sub-panels, so
    a 4b pass is a statement about the draw, not about a rule.
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
COV_MIN = 0.90

VSTAR, TAU = 0.25, 0.20                      # FROZEN from idea 1073 — not re-opened here
QS = [0.00, 0.50, 1.00]                      # DIAL 1
BETAS_CROSS = [np.nan, 0.25, 0.20, 0.15]     # DIAL 2, CROSS arm (nan = UNMATCHED)
BETAS_MATCH = [np.nan, 0.20, 0.12]           # DIAL 2, MATCH ladder
KS_CROSS = [20, 30]
KS_MATCH = [20, 30]
KS_REPRO = [20, 30, 40]                      # 1073's own crossing-arm k set
K_HEAD = 20                                  # the declared COMMON block for every headline
RATIOS = [0.10, 0.20, 0.35, 0.50]            # 1073's rungs, unchanged
D_CROSS, D_MATCH, D_REPRO = 12, 16, 8
SEED = 1073                                  # 1073's own seed, so REPRO replays its stream
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 600)

# committed anchors — idea 1073 lane C, crossing.csv
RHO1073 = {"BSTK-LO": 0.8759082918622507, "BSTK-HI": 0.7649147351270061,
           "SMALL-LO": 0.3586072408278919, "SMALL-HI": 0.17691475003962565}
BR1073 = {"BSTK-LO": 0.7376167311871775, "BSTK-HI": 0.679627224259712,
          "SMALL-LO": 0.5943421454767727, "SMALL-HI": 0.41789510323281726}
SHIFT1073 = 0.4063                           # |rho(BSTK-HI) - rho(SMALL-LO)|, 1073 console l.103


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "i276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "i286")
M694 = _load(BT / "2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_cloud.py",
             "i694")

full_row, keep_paths = M286.full_row, M286.keep_paths
spearman, partial_spearman = M286.spearman, M286.partial_spearman
fast_bt, panel_cache, cand_w_fast, gross_stats = (M694.fast_bt, M694.panel_cache,
                                                  M694.cand_w_fast, M694.gross_stats)


def name_vol(px, cols, end=IS_END):
    """1073's IS-only realised annualised name vol, byte-identical rule."""
    sub = px[cols].loc[VOL_START:end]
    v = sub.pct_change().std() * np.sqrt(252)
    return v.where(sub.notna().mean() >= COV_MIN).dropna()


def name_breadth(px, cols, end=IS_END):
    """Per-name IS gate-pass rate: fraction of weekly rebalance days in [index[WARM], end] on
    which the name is above its own 200d MA with its own vol20 < 0.60.  IS ONLY."""
    sub = px[cols]
    above = sub > sub.rolling(200).mean()
    vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
    g = above & (vol20 < 0.60)
    reb = rebalance_mask(sub.index, FREQ).values
    return g.loc[reb].loc[sub.index[WARM]:end].mean()


def bstar(series_by_cell, keys, beta, lo=0.30, hi=0.90):
    """The declared feasibility rule: maximise min(count) over `keys` inside B*(1+-beta).
    Ties to the lower B.  Returns (B*, grid DataFrame)."""
    rows = []
    for B in np.round(np.arange(lo, hi + 1e-9, 0.01), 2):
        l, h = B * (1 - beta), B * (1 + beta)
        c = {k: int(((series_by_cell[k] >= l) & (series_by_cell[k] <= h)).sum()) for k in series_by_cell}
        rows.append(dict(Bstar=B, mn=min(c[k] for k in keys), **c))
    g = pd.DataFrame(rows)
    return float(g.sort_values(["mn", "Bstar"], ascending=[False, True]).iloc[0].Bstar), g


def main():
    t0all = time.time()
    P("=" * 108)
    P("IDEA 1080 — is-the-CAP-ATTENUATION-a-BREADTH-fact-after-all-once-VOL-is-held-FIXED (lane B)")
    P("=" * 108)
    P(f"TUNED (2): q (cap mix) in {QS}  x  beta (BREADTH-match tolerance): CROSS "
      f"{['UNMATCHED' if b != b else b for b in BETAS_CROSS]}, MATCH "
      f"{['UNMATCHED' if b != b else b for b in BETAS_MATCH]}.  Every cell reported.")
    P(f"FROZEN from idea 1073, NOT re-opened: V*={VSTAR}, vol tau={TAU}, the crossing cells, the")
    P(f"  n/k rungs {RATIOS}, GROSS {GROSS}, {FREQ} cadence, {COST} bps, next-day, warm-up {WARM}.")
    P(f"REPORTED, NOT TUNED: k (CROSS {KS_CROSS}, MATCH {KS_MATCH}, REPRO {KS_REPRO}); draws "
      f"({D_CROSS}/{D_MATCH}/{D_REPRO}); the CROSSB mirror arm; the rule-8 selectors.")
    P(f"HEADLINE BLOCK declared in advance: k = {K_HEAD} only, because k=30 goes infeasible in "
      f"some cells at tight beta and a block that moves with the dial would confound the answer.")
    P("NO LOOK-AHEAD: every vol and every breadth used to BUILD a panel is IS-only (2010..2016).")
    P("SURVIVORSHIP: SMALL / BSTK are current constituents; a high-breadth window is doubly a")
    P("  survivor window.  Nothing here is a capital candidate.")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"pools SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    vS, vB = name_vol(pxs_c, s_stk), name_vol(pxb_c, b_stk)
    bS, bB = name_breadth(pxs_c, list(vS.index)), name_breadth(pxb_c, list(vB.index))
    P(f"names carrying an IS vol (coverage >= {COV_MIN}): SMALL {len(vS)}, BSTK {len(vB)}")
    P(f"  SMALL IS breadth q10/25/50/75/90 = "
      + "/".join(f"{x:.3f}" for x in bS.quantile([.1, .25, .5, .75, .9])) + f"   mean {bS.mean():.4f}")
    P(f"  BSTK  IS breadth q10/25/50/75/90 = "
      + "/".join(f"{x:.3f}" for x in bB.quantile([.1, .25, .5, .75, .9])) + f"   mean {bB.mean():.4f}")

    # ---------------------------------------------------------------- 1073's crossing cells
    cross_pools, cell_b, cell_v = {}, {}, {}
    for nm, v, b, pool in (("SMALL", vS, bS, "S"), ("BSTK", vB, bB, "B")):
        med = float(v.median())
        for half, sel in (("LO", v <= med), ("HI", v > med)):
            names = sorted(v[sel].index)
            cross_pools[f"{nm}-{half}"] = (pool, names)
            cell_b[f"{nm}-{half}"] = b.reindex(names)
            cell_v[f"{nm}-{half}"] = v.reindex(names)
    P("\n1073's CROSSING cells (each pool cut at its OWN median IS vol), with IS breadth added:")
    for nm in cross_pools:
        P(f"   {nm:9s} {len(cross_pools[nm][1]):3d} names, mean IS vol {cell_v[nm].mean():.4f}, "
          f"mean IS breadth {cell_b[nm].mean():.4f}  (1073's FULL-SAMPLE breadth {BR1073[nm]:.4f})")

    BC, gC = bstar(cell_b, ["BSTK-HI", "SMALL-LO"], 0.25)
    gC.to_csv(f"{OUT}.bstar_cross.csv", index=False)
    P(f"\nB*(CROSS) = {BC:.2f} by the declared rule (max min(n BSTK-HI, n SMALL-LO) at beta=0.25, "
      f"ties to the lower B); {len(gC)}-point grid published.  Counts at fixed B*:")
    for beta in [b for b in BETAS_CROSS if b == b]:
        l, h = BC * (1 - beta), BC * (1 + beta)
        P(f"   beta={beta:.2f} breadth in [{l:.3f}, {h:.3f}]  "
          + "  ".join(f"{c} {int(((cell_b[c] >= l) & (cell_b[c] <= h)).sum())}" for c in cross_pools))

    # ---------------------------------------------------------------- the tau=0.20 vol window
    lo_v, hi_v = VSTAR * (1 - TAU), VSTAR * (1 + TAU)
    wS = sorted(vS[(vS >= lo_v) & (vS <= hi_v)].index)
    wB = sorted(vB[(vB >= lo_v) & (vB <= hi_v)].index)
    BM, gM = bstar({"S": bS.reindex(wS), "B": bB.reindex(wB)}, ["S", "B"], 0.20)
    gM.to_csv(f"{OUT}.bstar_match.csv", index=False)
    P(f"\nMATCH ladder: 1073's tau={TAU} vol window [{lo_v:.3f}, {hi_v:.3f}] holds SMALL {len(wS)} "
      f"/ BSTK {len(wB)}.  B*(MATCH) = {BM:.2f} (max min(nS,nB) at beta=0.20).  Counts:")
    for beta in [b for b in BETAS_MATCH if b == b]:
        l, h = BM * (1 - beta), BM * (1 + beta)
        P(f"   beta={beta:.2f} breadth in [{l:.3f}, {h:.3f}]  SMALL "
          f"{int(((bS.reindex(wS) >= l) & (bS.reindex(wS) <= h)).sum())}  BSTK "
          f"{int(((bB.reindex(wB) >= l) & (bB.reindex(wB) <= h)).sum())}")

    # ---------------------------------------------------------------- panel construction
    panels, infeasible = [], []

    # REPRO — replays idea 1073's crossing-arm RNG stream exactly (its cross_pools insertion
    # order SMALL-LO, SMALL-HI, BSTK-LO, BSTK-HI; its KS; its N_DRAWS; its seed SEED+1)
    rngr = np.random.default_rng(SEED + 1)
    for nm in ["SMALL-LO", "SMALL-HI", "BSTK-LO", "BSTK-HI"]:
        names = cross_pools[nm][1]
        for k in KS_REPRO:
            if k > len(names):
                continue
            for d in range(D_REPRO):
                panels.append(dict(arm="REPRO", cell=nm, beta=np.nan, q=np.nan, k=k, draw=d,
                                   cols=sorted(rngr.choice(names, size=k, replace=False))))

    # CROSS — the same cells inside a breadth window
    rngc = np.random.default_rng(SEED + 80)
    for beta in BETAS_CROSS:
        for nm in ["SMALL-LO", "SMALL-HI", "BSTK-LO", "BSTK-HI"]:
            b = cell_b[nm]
            if beta != beta:
                names = sorted(b.index)
            else:
                l, h = BC * (1 - beta), BC * (1 + beta)
                names = sorted(b[(b >= l) & (b <= h)].index)
            for k in KS_CROSS:
                if k > len(names):
                    infeasible.append(("CROSS", nm, beta, k, len(names)))
                    continue
                for d in range(D_CROSS):
                    panels.append(dict(arm="CROSS", cell=nm, beta=beta, q=np.nan, k=k, draw=d,
                                       cols=sorted(rngc.choice(names, size=k, replace=False))))

    # CROSSB — the mirror: cap fixed, breadth moved (each pool cut at its OWN median IS breadth)
    crossb_pools = {}
    for nm, b, v in (("SMALL", bS, vS), ("BSTK", bB, vB)):
        med = float(b.median())
        crossb_pools[f"{nm}-BLO"] = sorted(b[b <= med].index)
        crossb_pools[f"{nm}-BHI"] = sorted(b[b > med].index)
    P("\nCROSSB mirror pools (each pool cut at its OWN median IS BREADTH):")
    for nm, names in crossb_pools.items():
        bb = (bS if nm.startswith("SMALL") else bB).reindex(names)
        vv = (vS if nm.startswith("SMALL") else vB).reindex(names)
        P(f"   {nm:10s} {len(names):3d} names, mean IS breadth {bb.mean():.4f}, "
          f"mean IS vol {vv.mean():.4f}")
    rngb = np.random.default_rng(SEED + 81)
    for nm, names in crossb_pools.items():
        for k in [20, 30, 40]:
            if k > len(names):
                infeasible.append(("CROSSB", nm, np.nan, k, len(names)))
                continue
            for d in range(D_REPRO):
                panels.append(dict(arm="CROSSB", cell=nm, beta=np.nan, q=np.nan, k=k, draw=d,
                                   cols=sorted(rngb.choice(names, size=k, replace=False))))

    # MATCH — the vol-matched ladder, additionally breadth-matched
    rngm = np.random.default_rng(SEED + 82)
    for beta in BETAS_MATCH:
        if beta != beta:
            mS, mB = list(wS), list(wB)
        else:
            l, h = BM * (1 - beta), BM * (1 + beta)
            bs, bb = bS.reindex(wS), bB.reindex(wB)
            mS = sorted(bs[(bs >= l) & (bs <= h)].index)
            mB = sorted(bb[(bb >= l) & (bb <= h)].index)
        for q in QS:
            for k in KS_MATCH:
                ns_, nl_ = int(round(q * k)), k - int(round(q * k))
                if ns_ > len(mS) or nl_ > len(mB):
                    infeasible.append(("MATCH", f"q{q:.2f}", beta, k, f"{len(mS)}S/{len(mB)}L"))
                    continue
                for d in range(D_MATCH):
                    sc = sorted(rngm.choice(mS, size=ns_, replace=False)) if ns_ else []
                    lc = sorted(rngm.choice(mB, size=nl_, replace=False)) if nl_ else []
                    panels.append(dict(arm="MATCH",
                                       cell=f"q{q:.2f}/" + ("UNM" if beta != beta else f"b{beta:.2f}"),
                                       beta=beta, q=q, k=k, draw=d, cols=list(sc) + list(lc)))

    P(f"\nPANELS: " + ", ".join(f"{a} {sum(1 for p in panels if p['arm']==a)}"
                                for a in ["REPRO", "CROSS", "CROSSB", "MATCH"])
      + f"  TOTAL {len(panels)} x {len(RATIOS)} books")
    if infeasible:
        P(f"  {len(infeasible)} INFEASIBLE cells skipped and reported: "
          + "; ".join(f"{a}/{c} beta={b} k={k} pool {n}" for a, c, b, k, n in infeasible))
    else:
        P("  no infeasible cells")

    # ---------------------------------------------------------------- gates before results
    gates = {}
    bad = []
    for p in panels:
        if len(p["cols"]) != p["k"] or len(set(p["cols"])) != p["k"]:
            bad.append((p["arm"], p["cell"], p["draw"], "width/dup"))
        if p["arm"] == "MATCH" and sum(c in s_stk for c in p["cols"]) != int(round(p["q"] * p["k"])):
            bad.append((p["arm"], p["cell"], p["draw"], "cap mix"))
        if p["beta"] == p["beta"]:
            B0 = BC if p["arm"] == "CROSS" else BM
            l, h = B0 * (1 - p["beta"]), B0 * (1 + p["beta"])
            bv = [float(bS[c]) if c in bS.index else float(bB[c]) for c in p["cols"]]
            if min(bv) < l - 1e-12 or max(bv) > h + 1e-12:
                bad.append((p["arm"], p["cell"], p["draw"], "breadth window"))
        if p["arm"] in ("REPRO", "CROSS", "MATCH"):
            pool = p["cell"].split("/")[0]
            if p["arm"] != "MATCH":
                vv = [float(vS[c]) if c in vS.index else float(vB[c]) for c in p["cols"]]
                src_ok = all((c in vS.index) == pool.startswith("SMALL") for c in p["cols"])
                if not src_ok:
                    bad.append((p["arm"], p["cell"], p["draw"], "wrong pool"))
            else:
                vv = [float(vS[c]) if c in vS.index else float(vB[c]) for c in p["cols"]]
                if min(vv) < lo_v - 1e-12 or max(vv) > hi_v + 1e-12:
                    bad.append((p["arm"], p["cell"], p["draw"], "vol window"))
    gates["G1"] = (not bad, f"ENVELOPE over all {len(panels)} panels: exact width, no duplicate "
                            f"columns, exact cap mix on MATCH, EVERY name inside its declared "
                            f"BREADTH window and (MATCH) inside 1073's frozen vol window. "
                            f"Violations: {len(bad)}")

    ref = [p for p in panels if p["arm"] == "REPRO" and p["k"] == 40][0]
    cols0 = ref["cols"]
    px0 = pd.concat([pxb_c[[c for c in cols0 if c in b_stk]],
                     pxs_c[[c for c in cols0 if c in s_stk]],
                     spy.rename("SPY")], axis=1).dropna(how="all").ffill()[cols0 + ["SPY"]]
    c0 = panel_cache(px0, cols0)
    w_ref = M286.cand_weights(20)(px0)
    dw = float(np.abs(w_ref.values - cand_w_fast(px0, c0, 20).values).max())
    eng = backtest(px0, w_ref, cost_bps=COST, freq=FREQ)
    r_f, t_f = fast_bt(px0, w_ref)
    dr = float(np.abs(eng["returns"] - r_f).max())
    dt = float(np.abs(eng["turnover"] - t_f).max())
    gates["G2"] = (dr < 1e-12 and dt < 1e-12 and dw == 0.0,
                   f"fast runner == engine.backtest on RETURNS ({dr:.2e}) and TURNOVER ({dt:.2e}); "
                   f"cached-rank CAND-20 == idea 286's committed cand_weights(20) (max|dw| {dw:.2e})")
    gates["G3"] = (bool(np.array_equal(fast_bt(px0, w_ref)[0].values, r_f.values, equal_nan=True)),
                   "DETERMINISM: the reference book re-runs bit-identical")

    # the IS breadth is an IS object: report its rank correlation with the full-sample breadth it
    # was not allowed to see (the same disclosure 1073 made for vol)
    bS_full = name_breadth(pxs_c, list(vS.index), end=str(idx[-1].date()))
    rho_bfull = spearman(bS.values, bS_full.reindex(bS.index).values)
    gates["G4"] = (True, f"NO LOOK-AHEAD, reported not gated: the IS name breadth used to build "
                         f"every panel ranks {rho_bfull:+.4f} against the FULL-sample breadth it "
                         f"was not allowed to see (SMALL pool) — high, but the OOS window never "
                         f"entered any choice")
    for g in sorted(gates):
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")

    # ---------------------------------------------------------------- run
    P("\n" + "=" * 108)
    P("RUNNING")
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
        reb = rebalance_mask(px.index, FREQ).values
        n_elig = cache["gate"].sum(axis=1)
        Ebar = float(n_elig[reb][px.index[reb] >= st].mean())          # 1073's FULL-SAMPLE object
        b_is = float(np.mean([float(bS[c]) if c in bS.index else float(bB[c]) for c in cols]))
        pvol = float(np.mean([float(vS[c]) if c in vS.index else float(vB[c]) for c in cols]))

        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        wv2 = (rules_v2_weights(px).drop(columns=["SPY"], errors="ignore")
               .reindex(columns=px.columns).fillna(0.0))
        v2_r = full_row("v2", fast_bt(px, wv2)[0].loc[st:])

        for r in RATIOS:
            n = max(2, int(round(r * p["k"])))
            w = cand_w_fast(px, cache, n)
            ret, turn = fast_bt(px, w)
            row = full_row(f"CAND{n}", ret.loc[st:])
            a, b = keep_paths(row, spy_r, v2_r)
            g_nom, fill = gross_stats(px, w, st)
            brows.append(dict(arm=p["arm"], cell=p["cell"], beta=p["beta"], q=p["q"], k=p["k"],
                              draw=p["draw"], ratio=r, n=n, panel_vol=pvol, breadth_IS=b_is,
                              breadth_full=Ebar / p["k"], gross=g_nom, fill=fill,
                              turnover=float(turn.loc[st:].sum() / (len(ret.loc[st:]) / 252)),
                              **{kk: vv for kk, vv in row.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                              spy_OOS_CAGR=spy_r["OOS_CAGR"], spy_OOS_DD=spy_r["OOS_MaxDD"],
                              v2_S=v2_r["Sharpe"], v2_DD=v2_r["MaxDD"], v2_H1=v2_r["H1"],
                              v2_H2=v2_r["H2"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                              pass4a=a, pass4b=b))
        prows.append(dict(arm=p["arm"], cell=p["cell"], beta=p["beta"], q=p["q"], k=p["k"],
                          draw=p["draw"], panel_vol=pvol, breadth_IS=b_is, breadth_full=Ebar / p["k"]))
        if (i + 1) % 150 == 0 or i == 0:
            P(f"  [{i+1:4d}/{len(panels)}] {p['arm']}/{p['cell']} k={p['k']} d{p['draw']}  "
              f"{time.time()-t0:4.2f}s  (elapsed {time.time()-t0all:6.1f}s)")

    books = pd.DataFrame(brows)
    pans = pd.DataFrame(prows)
    books.to_csv(f"{OUT}.books.csv.gz", index=False, compression="gzip")
    pans.to_csv(f"{OUT}.panels.csv", index=False)
    P(f"\n{len(books):,} book rows over {len(pans):,} panels written.")

    # ---------------------------------------------------------------- G5/G6: reproduce 1073
    rp = books[books.arm == "REPRO"]
    rho_rep = {c: partial_spearman(rp[rp.cell == c].OOS_Sharpe, rp[rp.cell == c].ratio,
                                   rp[rp.cell == c].k) for c in RHO1073}
    d5 = max(abs(rho_rep[c] - RHO1073[c]) for c in RHO1073)
    shift_rep = abs(rho_rep["BSTK-HI"] - rho_rep["SMALL-LO"])
    gates["G5"] = (d5 < 5e-4, "CROSS-RUN idea 1073's committed crossing-arm rho(n/k, OOS S | k), "
                              "its pools, its seed, its k set: "
                   + "; ".join(f"{c} {rho_rep[c]:+.4f} vs {RHO1073[c]:+.4f}" for c in RHO1073)
                   + f"  max|d| {d5:.2e};  the SHIFT reproduces {shift_rep:.4f} vs committed "
                     f"{SHIFT1073:.4f}")
    brf = {c: float(rp[rp.cell == c].breadth_full.mean()) for c in BR1073}
    d6 = max(abs(brf[c] - BR1073[c]) for c in BR1073)
    gates["G6"] = (d6 < 5e-4, "CROSS-RUN 1073's four committed FULL-SAMPLE breadths: "
                   + "; ".join(f"{c} {brf[c]:.4f} vs {BR1073[c]:.4f}" for c in BR1073)
                   + f"  max|d| {d6:.2e}")

    # the beta dial binds
    cb = books[books.arm == "CROSS"]
    cbh = cb[cb.k == K_HEAD]
    sd_u = float(cbh[cbh.beta.isna()].groupby(["cell", "draw"]).breadth_IS.first().std())
    sd_t = float(cbh[np.isclose(cbh.beta, min(b for b in BETAS_CROSS if b == b))]
                 .groupby(["cell", "draw"]).breadth_IS.first().std())
    gates["G7"] = (sd_t < sd_u, f"the beta dial BINDS on the headline k={K_HEAD} block: SD of "
                                f"panel IS breadth across panels falls {sd_u:.4f} (UNMATCHED) -> "
                                f"{sd_t:.4f} (beta={min(b for b in BETAS_CROSS if b==b):.2f})")
    gates["G8"] = (True, f"B* GRIDS published in full: CROSS {len(gC)} points, B*={BC:.2f}; MATCH "
                         f"{len(gM)} points, B*={BM:.2f}")

    P("\n" + "=" * 108)
    P("GATES")
    P("=" * 108)
    for g in sorted(gates):
        P(f"  {g} {'PASS' if gates[g][0] else 'FAIL'}  {gates[g][1]}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} PASS.")
    pd.DataFrame([dict(gate=g, verdict="PASS" if v[0] else "FAIL", detail=v[1])
                  for g, v in sorted(gates.items())]).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------- PART A: the cap shift
    P("\n" + "=" * 108)
    P(f"PART A — THE 0.4063 CAP SHIFT UNDER A BREADTH MATCH  (headline block k={K_HEAD})")
    P("=" * 108)
    arows = []
    for beta in BETAS_CROSS:
        sel = cbh[cbh.beta.isna()] if beta != beta else cbh[np.isclose(cbh.beta, beta)]
        for c in ["BSTK-LO", "BSTK-HI", "SMALL-LO", "SMALL-HI"]:
            s = sel[sel.cell == c]
            if len(s) < 8:
                continue
            arows.append(dict(beta=("UNMATCHED" if beta != beta else f"{beta:.2f}"), cell=c,
                              rows=len(s), panel_vol=s.panel_vol.mean(),
                              breadth_IS=s.breadth_IS.mean(), breadth_full=s.breadth_full.mean(),
                              rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                              OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std()))
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.crossing.csv", index=False)
    P(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    shift, bgap, vgap = {}, {}, {}
    for beta in BETAS_CROSS:
        lbl = "UNMATCHED" if beta != beta else f"{beta:.2f}"
        s = A[A.beta == lbl].set_index("cell")
        if not {"BSTK-HI", "SMALL-LO"} <= set(s.index):
            continue
        shift[lbl] = abs(s.loc["BSTK-HI", "rho"] - s.loc["SMALL-LO", "rho"])
        bgap[lbl] = abs(s.loc["BSTK-HI", "breadth_IS"] - s.loc["SMALL-LO", "breadth_IS"])
        vgap[lbl] = abs(s.loc["BSTK-HI", "panel_vol"] - s.loc["SMALL-LO", "panel_vol"])
    sU = shift["UNMATCHED"]
    P(f"\nTHE CAP SHIFT |rho(BSTK-HI) - rho(SMALL-LO)| at k={K_HEAD}, and what is left of it:")
    for lbl in shift:
        P(f"   beta={lbl:9s} shift {shift[lbl]:.4f}   = {100*shift[lbl]/sU:6.1f}% of this block's "
          f"UNMATCHED ({sU:.4f})   = {100*shift[lbl]/SHIFT1073:6.1f}% of 1073's committed "
          f"{SHIFT1073:.4f}   |d breadth_IS| {bgap[lbl]:.4f}  |d vol| {vgap[lbl]:.4f}")
    P(f"   (the REPRO arm, 1073's own k {KS_REPRO} block, reproduces the committed shift at "
      f"{shift_rep:.4f})")

    # ---------------------------------------------------------------- PART B: the mirror
    P("\n" + "=" * 108)
    P("PART B — THE MIRROR: hold CAP fixed and move BREADTH  (the decisive arm)")
    P("=" * 108)
    xb = books[books.arm == "CROSSB"]
    brows2 = []
    for c in ["BSTK-BLO", "BSTK-BHI", "SMALL-BLO", "SMALL-BHI"]:
        s = xb[xb.cell == c]
        if not len(s):
            continue
        brows2.append(dict(cell=c, cap=("LARGE" if c.startswith("BSTK") else "SMALL"), rows=len(s),
                           breadth_IS=s.breadth_IS.mean(), panel_vol=s.panel_vol.mean(),
                           rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                           OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std()))
    Bm = pd.DataFrame(brows2)
    Bm.to_csv(f"{OUT}.mirror.csv", index=False)
    P(Bm.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mr = Bm.set_index("cell").rho.to_dict()
    d_breadth_large = abs(mr["BSTK-BHI"] - mr["BSTK-BLO"])
    d_breadth_small = abs(mr["SMALL-BHI"] - mr["SMALL-BLO"])
    P(f"\n   LARGE cap, breadth moved : |rho(BSTK-BHI) - rho(BSTK-BLO)|   = {d_breadth_large:.4f}")
    P(f"   SMALL cap, breadth moved : |rho(SMALL-BHI) - rho(SMALL-BLO)| = {d_breadth_small:.4f}")
    P(f"   against CAP moved at matched vol (1073's object)             = {SHIFT1073:.4f}")

    # ---------------------------------------------------------------- PART C: the ladder
    P("\n" + "=" * 108)
    P("PART C — THE VOL-MATCHED LADDER, ADDITIONALLY BREADTH-MATCHED  (every (beta, q) cell)")
    P("=" * 108)
    mb = books[books.arm == "MATCH"]
    mbh = mb[mb.k == K_HEAD]
    crows = []
    for beta in BETAS_MATCH:
        sel = mbh[mbh.beta.isna()] if beta != beta else mbh[np.isclose(mbh.beta, beta)]
        for q in QS:
            s = sel[sel.q == q]
            if len(s) < 8:
                continue
            crows.append(dict(beta=("UNMATCHED" if beta != beta else f"{beta:.2f}"), q=q,
                              rows=len(s), panel_vol=s.panel_vol.mean(),
                              breadth_IS=s.breadth_IS.mean(),
                              rho=partial_spearman(s.OOS_Sharpe, s.ratio, s.k),
                              rho_raw=spearman(s.OOS_Sharpe, s.ratio),
                              OOS_S_mean=s.OOS_Sharpe.mean(), OOS_S_sd=s.OOS_Sharpe.std()))
    C = pd.DataFrame(crows)
    C.to_csv(f"{OUT}.ladder.csv", index=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    lgap = {}
    for lbl in C.beta.unique():
        s = C[C.beta == lbl].set_index("q")
        if 0.0 in s.index and 1.0 in s.index:
            lgap[lbl] = float(s.loc[0.0, "rho"] - s.loc[1.0, "rho"])
    lU = lgap.get("UNMATCHED", np.nan)
    P(f"\nTHE LADDER GAP rho(q=0.00) - rho(q=1.00) at k={K_HEAD} inside 1073's tau={TAU} vol window:")
    for lbl, g in lgap.items():
        P(f"   beta={lbl:9s} gap {g:+.4f}   = {100*g/lU:6.1f}% of this block's UNMATCHED ({lU:+.4f})")
    # the same block at k=30 where feasible, reported not headlined
    m30 = mb[mb.k == 30]
    P("   k=30 sub-block (reported, NOT the headline; infeasible cells absent): "
      + "; ".join(f"beta={('UNM' if b!=b else f'{b:.2f}')} gap "
                  + (f"{(partial_spearman(m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==0.0)].OOS_Sharpe, m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==0.0)].ratio, m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==0.0)].k) - partial_spearman(m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==1.0)].OOS_Sharpe, m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==1.0)].ratio, m30[(m30.beta.isna() if b!=b else np.isclose(m30.beta,b))&(m30.q==1.0)].k)):+.4f}"
                     if len(m30[(m30.beta.isna() if b != b else np.isclose(m30.beta, b)) & (m30.q == 0.0)]) >= 8
                     and len(m30[(m30.beta.isna() if b != b else np.isclose(m30.beta, b)) & (m30.q == 1.0)]) >= 8
                     else "INFEASIBLE")
                  for b in BETAS_MATCH))

    # ---------------------------------------------------------------- PART D: rule 8
    P("\n" + "=" * 108)
    P("PART D — RULE 8 WALK-FORWARD: n/k chosen on 2009-2016 IS Sharpe ONLY, 2017- read ONCE")
    P("=" * 108)
    SEL = {"IS-SHARPE-MAX": ("IS_Sharpe", True), "RATIO-MAX": ("ratio", True),
           "RATIO-MIN": ("ratio", False)}
    rng8 = np.random.default_rng(SEED + 8)
    wrows = []
    for (arm, cell, beta, k, d), sub in books.groupby(["arm", "cell", "beta", "k", "draw"],
                                                      dropna=False):
        if len(sub) < 2:
            continue
        anchor = float(sub.OOS_Sharpe.mean())
        picks = {sel: (sub.loc[sub[col].idxmax()] if hi else sub.loc[sub[col].idxmin()])
                 for sel, (col, hi) in SEL.items()}
        picks["RANDOM"] = sub.iloc[int(rng8.integers(len(sub)))]
        for sel, pk in picks.items():
            wrows.append(dict(arm=arm, cell=cell, beta=beta, k=k, draw=d, selector=sel,
                              ratio=pk.ratio, n=pk.n, OOS_Sharpe=pk.OOS_Sharpe,
                              OOS_CAGR=pk.OOS_CAGR, OOS_MaxDD=pk.OOS_MaxDD, anchor=anchor,
                              edge=pk.OOS_Sharpe - anchor, spy_OOS_S=pk.spy_OOS_S,
                              spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_DD=pk.spy_OOS_DD,
                              v2_OOS_S=pk.v2_OOS_S, v2_OOS_CAGR=pk.v2_OOS_CAGR,
                              v2_OOS_DD=pk.v2_OOS_DD, pass4a=pk.pass4a, pass4b=pk.pass4b))
    W = pd.DataFrame(wrows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    W["beat_spy"] = W.OOS_Sharpe > W.spy_OOS_S
    W["beat_v2"] = W.OOS_Sharpe > W.v2_OOS_S
    wf = (W.groupby(["arm", "selector"]).agg(sets=("edge", "size"), OOS_S=("OOS_Sharpe", "mean"),
                                             OOS_CAGR=("OOS_CAGR", "mean"),
                                             OOS_DD=("OOS_MaxDD", "mean"),
                                             edge_vs_anchor=("edge", "mean"),
                                             beat_SPY=("beat_spy", "mean"),
                                             beat_v2=("beat_v2", "mean")).reset_index())
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    wfb = (W[W.arm == "CROSS"].groupby(["beta", "selector"], dropna=False)
           .agg(sets=("edge", "size"), OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                OOS_DD=("OOS_MaxDD", "mean"), edge_vs_anchor=("edge", "mean"),
                beat_SPY=("beat_spy", "mean")).reset_index())
    P("\nby beta on the CROSS arm (does letting the chooser see a breadth-matched panel help?):")
    P(wfb.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n   comparands on the SAME panels: SPY OOS Sharpe {W.spy_OOS_S.mean():.4f} / CAGR "
      f"{W.spy_OOS_CAGR.mean():.2%} / MaxDD {W.spy_OOS_DD.mean():.2%};  RULES v2 OOS Sharpe "
      f"{W.v2_OOS_S.mean():.4f} / CAGR {W.v2_OOS_CAGR.mean():.2%} / MaxDD {W.v2_OOS_DD.mean():.2%}")

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 108)
    P("BOTH KEEP PATHS, EVERY BOOK ROW (idea 286's committed keep_paths; rule 4)")
    P("=" * 108)
    kp = (books.groupby(["arm", "beta"], dropna=False)
          .agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"), p4b=("pass4b", "sum")).reset_index())
    kp["rate4b"] = kp.p4b / kp.rows
    P(kp.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  TOTAL: 4a {int(books.pass4a.sum())} of {len(books):,}; "
      f"4b {int(books.pass4b.sum())} of {len(books):,}")
    P("  These are committed CAND-n books on RANDOM sub-panels of a survivor screen; a 4b pass "
      "here is a statement about the draw, not a capital candidate.  NOTHING IS PROMOTED.")
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ---------------------------------------------------------------- limits
    P("\n" + "=" * 108)
    P("LIMITS, STATED BEFORE THE VERDICT")
    P("=" * 108)
    nmin = min(len(cell_b[c][(cell_b[c] >= BC * (1 - 0.15)) & (cell_b[c] <= BC * (1 + 0.15))])
               for c in ["BSTK-HI", "SMALL-LO"])
    P(f"  1. At the tightest CROSS beta the decisive cells hold only {nmin} names, so {D_CROSS} "
      f"k={K_HEAD} draws overlap heavily and are far from independent.  Every rho here is a "
      f"firmer POINT than an INTERVAL; no interval is published (idea 1044's rule), so only the "
      f"cell ORDERING and the SIGN are claimed.")
    P(f"  2. BREADTH and VOL are not orthogonal on this tape: within SMALL the LO-vol half carries "
      f"IS breadth {cell_b['SMALL-LO'].mean():.4f} against the HI-vol half's "
      f"{cell_b['SMALL-HI'].mean():.4f}.  A breadth window therefore moves the vol mix too, which "
      f"is why |d vol| is printed beside every shift above.")
    P("  3. The matched window is where the two pools OVERLAP in breadth, so it speaks for "
      "NEITHER pool's typical name.  Nothing here extends to a low-breadth small-cap book.")
    P("  4. IS breadth is measured over 2010-2016 only, a period with one real drawdown (2011) "
      "and no 2020/2022.  A breadth measured on a different window could rank names differently.")
    P("  5. SURVIVORSHIP again: a realised gate-pass rate is measured on names that survived to "
      "be screened today, so a high-breadth window is doubly a survivor window.")

    # ---------------------------------------------------------------- hypotheses
    P("\n" + "=" * 108)
    P("THE DECLARED HYPOTHESES")
    P("=" * 108)
    H = []
    H.append(("H_REPRO", d5 < 5e-4 and abs(shift_rep - SHIFT1073) < 5e-4,
               "1073's crossing arm replays exactly, shift included",
               f"max|d rho| {d5:.2e}; shift {shift_rep:.4f} vs {SHIFT1073:.4f}"))
    ratio_b = float(bB.mean() / bS.mean())
    H.append(("H_BGAP", ratio_b >= 1.15,
               "the pools really do differ in IS breadth (mean BSTK / SMALL >= 1.15) "
               "[REPORTED, not blind: seen in the pre-run feasibility pass]",
               f"BSTK {bB.mean():.4f} / SMALL {bS.mean():.4f} = {ratio_b:.3f}x"))
    H.append(("H_ALREADY", bgap["UNMATCHED"] >= 0.05,
               "the two cells the 0.4063 shift is taken between are NOT already breadth-matched "
               "on the IS measure (|d| >= 0.05) [REPORTED, not blind: same pass]",
               f"|d breadth_IS| BSTK-HI vs SMALL-LO {bgap['UNMATCHED']:.4f}; on 1073's FULL-SAMPLE "
               f"measure the same gap is {abs(BR1073['BSTK-HI']-BR1073['SMALL-LO']):.4f}"))
    tightest = f"{min(b for b in BETAS_CROSS if b == b):.2f}"
    H.append(("H_SURVIVE", shift.get(tightest, np.nan) <= 0.5 * sU,
               "BREADTH MATCHING CLOSES THE CAP SHIFT: at the tightest beta the shift is <= 50% "
               "of its own UNMATCHED value on the same k block  [THE IDEA'S QUESTION]",
               f"beta={tightest} shift {shift.get(tightest, np.nan):.4f} vs UNMATCHED {sU:.4f} — "
               f"{100*shift.get(tightest, np.nan)/sU:.1f}% survives"))
    seq = [shift[l] for l in ["UNMATCHED", "0.25", "0.20", "0.15"] if l in shift]
    H.append(("H_MONO", all(seq[i + 1] <= seq[i] + 1e-9 for i in range(len(seq) - 1)),
               "the closing is MONOTONE as beta tightens",
               " -> ".join(f"{x:.4f}" for x in seq)))
    H.append(("H_BCROSS", max(d_breadth_large, d_breadth_small) >= SHIFT1073,
               "the MIRROR says BREADTH: moving breadth at FIXED cap shifts rho at least as hard "
               "as moving cap at fixed vol did (0.4063)",
               f"LARGE {d_breadth_large:.4f}, SMALL {d_breadth_small:.4f} vs {SHIFT1073:.4f}"))
    lt = f"{min(b for b in BETAS_MATCH if b == b):.2f}"
    H.append(("H_LADDER", lgap.get(lt, np.nan) <= 0.5 * lU,
               "the same closing on the vol-matched LADDER: the q=0.00 -> q=1.00 rho gap at the "
               "tightest beta is <= 50% of the same block's UNMATCHED gap",
               f"beta={lt} gap {lgap.get(lt, np.nan):+.4f} vs UNMATCHED {lU:+.4f}"))
    allrho = list(A.rho) + list(C.rho) + list(Bm.rho)
    H.append(("H_SIGN", bool(min(allrho) > 0),
               "rho > 0 in EVERY published cell (the 'strength dial, not sign dial' claim)",
               f"min {min(allrho):+.4f} over {len(allrho)} cells; max {max(allrho):+.4f}"))
    for nm, ok, claim, det in H:
        P(f"  {nm:<11s} {'PASS' if ok else 'FAIL'}  {claim}")
        P(f"              -> {det}")
    P(f"\nHYPOTHESES: {sum(1 for _, ok, _, _ in H if ok)} of {len(H)} PASS.")
    pd.DataFrame([dict(hypothesis=n, verdict="PASS" if o else "FAIL", claim=c, detail=d)
                  for n, o, c, d in H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    P(f"\ntotal elapsed {time.time()-t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
