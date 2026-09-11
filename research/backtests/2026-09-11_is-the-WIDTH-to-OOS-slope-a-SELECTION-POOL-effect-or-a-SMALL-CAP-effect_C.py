#!/usr/bin/env python3
"""Idea 694 - "is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect"
(lane C, 2026-09-11).

The question
------------
Two committed lane-C runs disagree about what a WIDER panel does to a book's OUT-OF-SAMPLE
Sharpe:

  * idea 688 (q = 1.00, pure SMALL439 draws, k = 40..400, CAND-n at FIXED n): the wide end
    WINS.  Spearman(k, OOS Sharpe) over its 288 committed book rows is **+0.5269** and the
    mean OOS Sharpe is monotone **0.2516 -> 0.2729 -> 0.3232 -> 0.3725 -> 0.4257 -> 0.4849**.
    Its stated mechanism: "a CAND-n book at fixed n selects from a bigger pool".
  * idea 685 (mixed q, k = 40..400): the wide end LOSES (-0.1685 of OOS Sharpe for the
    EBAR-MAX pick).  Its wide panels are FORCED small-cap-heavy - only q >= 0.75 can reach
    k = 400 at all, because BSTK100 carries exactly 100 large-cap names.

The two ladders differ in TWO things at once, so neither can settle the mechanism:
  (i)  POOL DEPTH / SELECTIVITY.  At FIXED n, widening k from 40 to 400 takes the book from
       "top 20 of 40" to "top 20 of 400" - a 10x change in the SELECTION RATIO r = n/k.  Any
       "width" slope measured that way is also a selectivity slope, and the record already
       holds (idea 78/666) that the ranking payoff is governed by selectivity, not by count.
  (ii) CAP MIX.  In idea 685's ladder q rises with k; in idea 688's it cannot move at all.

This run separates them, exactly as the queue asks: **hold n/k fixed while varying k**, and
price the cap-mix channel separately at MATCHED width and MATCHED ratio.

Design - one panel set, two arms through the (k, n) plane, plus a cap-mix leg
----------------------------------------------------------------------------
LADDER W (width, q = 1.00): idea 688's own panels, rebuilt by importing its `build_ladder`
    (k in {40,60,80,100,200,400} x 8 draws = 48 panels, the first three draws at each k
    replaying lane B's / idea 685's generators).  Every panel is a uniform draw of columns
    from ONE pool (SMALL439), so panels are exchangeable up to their size and NO cap-mix
    variation exists inside this ladder by construction.
LADDER Q (cap mix, k = 100 fixed): lane B's own (q, k=100) cells replayed from seed 2026,
    q in {0.00, 0.25, 0.50, 0.75, 1.00} x 3 draws.  Width is held at 100 and the selection
    ratio is held at r, so the ONLY thing moving is the small-cap share q.

Every panel is priced on the SAME book ladder, so the two arms are not two experiments but
two paths through one grid:
    ARM A (the record's construction)  n in {5, 10, 15, 20, 30}, fixed as k varies.
    ARM B (this run's construction)    r = n/k in {0.05, 0.10, 0.25, 0.50}, n = round(r*k),
                                       so r is fixed as k varies (n = 2..200).
A book that appears in both arms (e.g. k = 100, n = 5) is ONE backtest, counted in both.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. SELECTION RATIO r = n/k in {0.05, 0.10, 0.25, 0.50}  (the queue's first named dial).
    2. WIDTH k in {40, 60, 80, 100, 200, 400}               (the queue's second named dial).
    Everything else is inherited from the committed record and is not chosen here: the
    RULES v1 gate (idea 276), CAND-n / EWall / ADAPT books (idea 286), GROSS = 0.75, weekly
    cadence, 10 bps, next-day execution, the 260-day warm-up skip, the fixed-n ladder
    {5,10,15,20,30} (idea 525's NS_LAD), the q levels (idea 525's QS), the draws and seeds
    (2026 / 685 / 688).  No level of r or k is dropped after the fact.

PRE-REGISTERED BARS (fixed here before any number in this run was read)
----------------------------------------------------------------------
    A = mean over the 5 FIXED-n levels of within-n Spearman(k, OOS Sharpe)   [the record's]
    B = mean over the 4 FIXED-r levels of within-r Spearman(k, OOS Sharpe)   [this run's]
    SURVIVAL = B / A.
        SURVIVAL >= 0.60 AND B >= +0.30   -> POOL-DEPTH: width itself buys OOS Sharpe.
        SURVIVAL <= 0.25  OR  |B| <= 0.15 -> SELECTIVITY ARTEFACT: the published width slope
                                             is the selection ratio n/k wearing k's clothes.
        otherwise                         -> MIXED.
    CAP = mean over the 4 FIXED-r levels of within-r Spearman(q, OOS Sharpe) at k = 100.
        |CAP| >= 0.30 -> a REAL cap-mix channel at matched width and matched ratio.
        |CAP| <= 0.15 -> NO cap-mix channel; idea 685's wide-end loss is not a cap story.
    The verdict names which of the queue's two candidate mechanisms survives; a run in which
    BOTH fail their bars is reported as NEITHER, not rescued by a third statistic.

Gates, asserted before any new number is read
    G0  REPRODUCTION-688: the q = 1.00 panels are idea 688's `build_ladder` output, and the
        CAND-n rows at n in {5,10,15,20,30} are asserted against its committed .books.csv at
        1e-9 on CAGR/Sharpe/MaxDD/H1/H2/OOS_CAGR/OOS_Sharpe/OOS_MaxDD/IS_Sharpe.
    G0b REPRODUCTION-525: the q < 1.00, k = 100 panels replay lane B's generator and are
        asserted against idea 525's committed .books.csv on the same nine quantities.
    G0c HEADLINE: Spearman(k, OOS Sharpe) over the 288 fixed-n rows re-measured from this
        run's own books, asserted equal to the published +0.5269 at 1e-3, and the six
        published means 0.2516..0.4849 at 1e-3.  The disagreement this run adjudicates has
        to reproduce before it can be decomposed.
    G1  ENVELOPE: exact width, exact cap mix, no duplicate columns, inside the pool bounds.
    G2  RATIO IDENTITY: every ARM B book has n == round(r*k) exactly; the realised n/k is
        reported for every cell so the reader can see the rounding (worst |n/k - r| printed).

Rule 8 walk-forward (PROTOCOL rule 8, required)
    The dials are chosen on the IS window (..2016-12-31) ONLY and read once on 2017-01-01..
    untouched, per draw:
      PICK-r      : argmax over r of IS Sharpe, at each k  -> OOS CAGR/Sharpe/MaxDD.
      PICK-n      : argmax over the fixed-n ladder of IS Sharpe, at each k (the record's
                    selector, for contrast).
      PICK-(k,r)  : argmax over the WHOLE (k, r) grid of IS Sharpe -> which k does an
                    IS-honest selector take when the ratio is a free dial, and what does it
                    pay?  This is idea 688's width-pin question asked with r free.
    Every pick is reported against the do-nothing anchor (the choice-set mean), against
    RULES v2 on the SAME panel, and against SPY on the same calendar.  Both KEEP paths are
    evaluated on every book row (.books.csv carries pass4a / pass4b from idea 286's
    `keep_paths`, i.e. PROTOCOL 4a vs RULES v2 and 4b vs SPY at 10 bps).

CAPACITY CAVEAT (reported, not tuned): CAND-n holds the top n of the eligible set, so a book
with n above the panel's mean eligible count Ebar is an EWall book in disguise.  n/Ebar is
published for every cell and every arm-level statistic is re-read on the subset with
n <= Ebar_IS, so the reader can see whether the answer rests on capacity-bound cells.

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): SMALL439 and BSTK100 are CURRENT
constituents of their screens, so every level here is optimistic, most of all at the small
end; LADDER W is entirely small-cap.  The object under test is which COORDINATE of the (k,
n, q) grid carries a slope, and survivorship moves the level of every panel in a ladder
together - it can bias a LEVEL, not the sign of a within-ladder slope.  No arm here is a new
BOOK: CAND-n / EWall are the record's existing books re-run on re-drawn panels, so a 4a/4b
pass is a statement about the panel, not a capital candidate.

Outputs: .panels.csv .books.csv .grid.csv .slopes.csv .walkforward.csv .keeppaths.csv
         .console.txt .result.md
"""
import importlib.util, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- this run's grid (2 tuned params) -------------------------------------------------
RATIOS   = [0.05, 0.10, 0.25, 0.50]             # param 1: selection ratio r = n/k
KS       = [40, 60, 80, 100, 200, 400]          # param 2: width k
NS_FIXED = [5, 10, 15, 20, 30]                  # inherited (idea 525's NS_LAD) - ARM A
Q_LEVELS = [0.00, 0.25, 0.50, 0.75, 1.00]       # inherited (idea 525's QS) - cap-mix leg
K_CAP    = 100                                  # inherited: the only width lane B ran all q at
BAR_SURV_HI, BAR_SURV_LO, BAR_B, BAR_CAP = 0.60, 0.25, 0.30, 0.30
BAR_FLAT = 0.15

# published quantities this run must reproduce before it may decompose them (GATE 0c)
PUB_RHO  = 0.5269
PUB_MEAN = [0.2516, 0.2729, 0.3232, 0.3725, 0.4257, 0.4849]


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P525 = BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B"
M525 = _load(f"{P525}.py", "idea525")
P688 = BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C"
M688 = _load(f"{P688}.py", "idea688")

spearman = M286.spearman
do_panel = M525.do_panel
QS_B, KS_B, NDRAWS_B, SEED_B = M525.QS, M525.KS, M525.N_DRAWS, M525.SEED

GATECOLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "IS_Sharpe"]


def ratio_n(k, r):
    """ARM B's book size at width k and ratio r: n = round(r*k), floored at 2 names."""
    return max(2, int(round(r * k)))


def ns_for(k):
    """Every book size run on a width-k panel: ARM A's fixed ladder + ARM B's ratio ladder."""
    ns = set(n for n in NS_FIXED if n < k) | {ratio_n(k, r) for r in RATIOS}
    return sorted(n for n in ns if 2 <= n < k)


def replay_laneB_q(s_stk, b_stk):
    """Lane B's (q x k x draw) generator, replayed in its own order so the rng state matches
    at every cell; returns the k = K_CAP cells at q < 1.00 (the q = 1.00 cell is already in
    idea 688's ladder and is not run twice)."""
    rng = np.random.default_rng(SEED_B)
    out, seen = {}, set()
    for q in QS_B:
        for k in KS_B:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(NDRAWS_B):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen: continue
                seen.add(key)
                if k == K_CAP and q < 1.0:
                    out[(q, d)] = (list(sc), list(lc))
    return out


def ols_rank2(y, x1, x2):
    """Standardised RANK regression y ~ x1 + x2 (idea 525's `rank_ols2`, imported)."""
    return M525.rank_ols2(y, x1, x2)


def wf_row(label, sub, pick):
    """One walk-forward line: the IS-chosen cell read once on the OOS window."""
    return dict(selector=label, k=int(pick.k), n=int(pick.n), r=float(pick.n) / float(pick.k),
                IS_Sharpe=float(pick.IS_Sharpe),
                OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                OOS_MaxDD=float(pick.OOS_MaxDD),
                anchor_OOS_S=float(sub.OOS_Sharpe.mean()),
                anchor_OOS_CAGR=float(sub.OOS_CAGR.mean()),
                anchor_OOS_DD=float(sub.OOS_MaxDD.mean()),
                best_OOS_S=float(sub.OOS_Sharpe.max()),
                v2_OOS_S=float(pick.v2_OOS_S), spy_OOS_S=float(pick.spy_OOS_S),
                beats_anchor=bool(pick.OOS_Sharpe > sub.OOS_Sharpe.mean()),
                beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S))


def main():
    t0all = time.time()
    P("=" * 100)
    P("IDEA 694 - is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect")
    P("           (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED BARS (docstring, fixed before any number below was read):")
    P(f"  A = mean over n in {NS_FIXED} of within-n Spearman(k, OOS Sharpe)   [record's arm]")
    P(f"  B = mean over r in {RATIOS} of within-r Spearman(k, OOS Sharpe)  [this run's arm]")
    P(f"  SURVIVAL = B / A.  >= {BAR_SURV_HI:.2f} and B >= +{BAR_B:.2f} -> POOL-DEPTH;  "
      f"<= {BAR_SURV_LO:.2f} or |B| <= {BAR_FLAT:.2f} -> SELECTIVITY ARTEFACT;  else MIXED.")
    P(f"  CAP = mean over r of within-r Spearman(q, OOS Sharpe) at k = {K_CAP}; "
      f"|CAP| >= {BAR_CAP:.2f} -> real cap channel, |CAP| <= {BAR_FLAT:.2f} -> none.")
    P(f"  Grid: k in {KS} x r in {RATIOS} (+ fixed n in {NS_FIXED}), q = 1.00 for the width "
      f"ladder; q in {Q_LEVELS} at k = {K_CAP} for the cap leg.  Every cell reported.")

    # ------------------------------------------------------------ sources
    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    # ------------------------------------------------------------ ladders
    built, prov = M688.build_ladder(s_stk, b_stk)          # LADDER W, q = 1.00
    capcells = replay_laneB_q(s_stk, b_stk)                # LADDER Q, k = K_CAP, q < 1.00
    P(f"\nLADDER W: {len(built)} panels at q=1.00 "
      f"({sum(1 for v in prov.values() if v != 'new')} replayed from the record)")
    P(f"LADDER Q: {len(capcells)} extra panels at k={K_CAP}, q in "
      f"{sorted({q for q, _ in capcells})} (lane B's own cells, replayed)")

    P("\n--- GATE 1: envelope ---")
    bad = []
    for k, d, cols in built:
        if len(cols) != k: bad.append((k, d, "width"))
        if len(set(cols)) != len(cols): bad.append((k, d, "dup"))
        if any(c not in s_stk for c in cols): bad.append((k, d, "cap mix"))
    for (q, d), (sc, lc) in capcells.items():
        if len(sc) + len(lc) != K_CAP: bad.append((q, d, "width"))
        if len(set(sc + lc)) != K_CAP: bad.append((q, d, "dup"))
        if int(round(q * K_CAP)) != len(sc): bad.append((q, d, "cap mix"))
        if any(c not in s_stk for c in sc) or any(c not in b_stk for c in lc):
            bad.append((q, d, "pool"))
    assert not bad, f"GATE 1 FAILED: {bad[:5]}"
    P(f"  GATE 1 PASS - all {len(built) + len(capcells)} panels: exact width, exact cap mix, "
      "no duplicate columns, inside the pool bounds.")

    P("\n--- GATE 2: ratio identity (ARM B book sizes) ---")
    worst = 0.0
    for k in KS:
        row = []
        for r in RATIOS:
            n = ratio_n(k, r); worst = max(worst, abs(n / k - r))
            row.append(f"r={r:.2f} -> n={n:3d} (n/k={n / k:.4f})")
        P(f"  k={k:3d}: " + " | ".join(row))
    P(f"  worst |n/k - r| over the grid: {worst:.4f}  (pure rounding; every cell published)")

    # ------------------------------------------------------------ run every panel
    P("\n" + "=" * 100)
    P("RUNNING THE GRID  (one panel = one price matrix, every book size on it)")
    P("=" * 100)
    brows, srows = [], []
    jobs = [(f"MIX q=1.00 k={k} d{d}", 1.00, k, d,
             pd.concat([pxs_c[cols], spy.rename("SPY")], axis=1)[cols + ["SPY"]], cols)
            for k, d, cols in built]
    jobs += [(f"MIX q={q:.2f} k={K_CAP} d{d}", q, K_CAP, d,
              pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                         spy.rename("SPY")], axis=1)[sc + lc + ["SPY"]], sc + lc)
             for (q, d), (sc, lc) in sorted(capcells.items())]
    for i, (tag, q, k, d, px, cols) in enumerate(jobs):
        px = px.dropna(how="all").ffill()
        nsr = ns_for(k)
        t0 = time.time()
        do_panel(tag, "mix", q, d, px, cols, brows, srows, nsr, {"lad": NS_FIXED})
        P(f"  [{i + 1:3d}/{len(jobs)}] q={q:.2f} k={k:3d} d{d}  n={nsr}  "
          f"{time.time() - t0:5.1f}s (elapsed {time.time() - t0all:6.1f}s)")

    books = pd.DataFrame(brows); stats = pd.DataFrame(srows)
    mix = stats[stats.ladder == "lad"].copy()
    books.to_csv(f"{OUT}.books.csv", index=False)
    mix.to_csv(f"{OUT}.panels.csv", index=False)

    # ------------------------------------------------------------ GATE 0
    P("\n" + "=" * 100)
    P("GATE 0 - REPRODUCTION of the committed record")
    P("=" * 100)
    cand = books[books.arm != "EWall"].copy()
    cand["r"] = cand.n / cand.k
    worst_all = {}
    for label, base, sel in (("idea 688 (q=1.00 width ladder)", P688, lambda b: b.q == 1.00),
                             ("idea 525 (lane B, k=100 cap cells)", P525, lambda b: b.q < 1.00)):
        ref = pd.read_csv(f"{base}.books.csv")
        ref = ref[(ref.kind == "mix") & (ref.arm != "EWall")]
        mine = cand[sel(cand)]
        key = ["panel", "arm"]
        m = mine.merge(ref, on=key, suffixes=("", "_ref"))
        P(f"  {label}: {len(m)} overlapping book rows")
        if not len(m): continue
        for c in GATECOLS:
            dd = (m[c] - m[f"{c}_ref"]).abs()
            worst_all[f"{label}:{c}"] = float(dd.max())
            P(f"    {c:12s} max |delta| {dd.max():.3e}   >1e-9: {int((dd > 1e-9).sum())}/{len(dd)}")
    for kk, vv in worst_all.items():
        assert vv < 1e-9, f"GATE 0 FAILED on {kk}: {vv:.3e}"
    P(f"  GATE 0 PASS - worst |delta| over all reproduced book rows: "
      f"{max(worst_all.values()):.3e}")

    P("\n--- GATE 0c: the published headline this run decomposes ---")
    w = books[books.q == 1.00]                          # 6 arms x 6 k x 8 draws = 288 rows
    wfix = w[(w.arm == "EWall") | (w.n.isin(NS_FIXED))]
    rho_pub = spearman(wfix.k, wfix.OOS_Sharpe)
    means = [float(wfix[wfix.k == k].OOS_Sharpe.mean()) for k in KS]
    P(f"  rows {len(wfix)} (published 288);  Spearman(k, OOS Sharpe) = {rho_pub:+.4f} "
      f"(published {PUB_RHO:+.4f})")
    P("  mean OOS Sharpe by k: " + " -> ".join(f"{m:.4f}" for m in means))
    P("  published           : " + " -> ".join(f"{m:.4f}" for m in PUB_MEAN))
    assert len(wfix) == 288, f"GATE 0c FAILED: {len(wfix)} rows, expected 288"
    assert abs(rho_pub - PUB_RHO) < 1e-3, f"GATE 0c FAILED on rho: {rho_pub:.4f}"
    assert max(abs(a - b) for a, b in zip(means, PUB_MEAN)) < 1e-3, "GATE 0c FAILED on means"
    P("  GATE 0c PASS - idea 688's headline reproduces exactly; it may now be decomposed.")

    # ------------------------------------------------------------ the grid
    P("\n" + "=" * 100)
    P("THE (k, r) GRID - every cell, mean over the 8 draws")
    P("=" * 100)
    wc = cand[cand.q == 1.00].copy()
    wc["Ebar_IS"] = wc.panel.map(mix.set_index("panel").Ebar_IS)
    wc["n_over_Ebar"] = wc.n / wc.Ebar_IS
    RCELL = {(k, ratio_n(k, r)): r for k in KS for r in RATIOS}
    wc["r_level"] = [RCELL.get((int(k), int(n)), np.nan) for k, n in zip(wc.k, wc.n)]
    wc["in_A"] = wc.n.isin(NS_FIXED)
    wc["in_B"] = wc.r_level.notna()
    wc.to_csv(f"{OUT}.grid.csv", index=False)

    grid = (wc[wc.in_B].groupby(["r_level", "k"])
            .agg(n=("n", "first"), OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                 OOS_DD=("OOS_MaxDD", "mean"), IS_S=("IS_Sharpe", "mean"),
                 Sharpe=("Sharpe", "mean"), CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                 n_over_Ebar=("n_over_Ebar", "mean"), rows=("OOS_Sharpe", "size")).reset_index())
    P("\nARM B - FIXED SELECTION RATIO (n = round(r*k)):")
    P("  " + grid.to_string(index=False, float_format=lambda x: f"{x:8.4f}").replace("\n", "\n  "))
    gridA = (wc[wc.in_A].groupby(["n", "k"])
             .agg(OOS_S=("OOS_Sharpe", "mean"), IS_S=("IS_Sharpe", "mean"),
                  r=("r", "mean"), n_over_Ebar=("n_over_Ebar", "mean")).reset_index())
    P("\nARM A - FIXED n (the record's construction), same panels:")
    P("  " + gridA.to_string(index=False, float_format=lambda x: f"{x:8.4f}").replace("\n", "\n  "))

    # ------------------------------------------------------------ the slopes
    P("\n" + "=" * 100)
    P("THE DECOMPOSITION - does the width slope survive at a FIXED selection ratio?")
    P("=" * 100)
    srow = []
    for n in NS_FIXED:
        sub = wc[wc.n == n]
        srow.append(dict(arm="A fixed-n", level=float(n), rho_k=spearman(sub.k, sub.OOS_Sharpe),
                         rho_k_IS=spearman(sub.k, sub.IS_Sharpe), rows=len(sub),
                         lo_k_OOS=float(sub[sub.k == min(KS)].OOS_Sharpe.mean()),
                         hi_k_OOS=float(sub[sub.k == max(KS)].OOS_Sharpe.mean())))
    for r in RATIOS:
        sub = wc[wc.r_level == r]
        srow.append(dict(arm="B fixed-r", level=r, rho_k=spearman(sub.k, sub.OOS_Sharpe),
                         rho_k_IS=spearman(sub.k, sub.IS_Sharpe), rows=len(sub),
                         lo_k_OOS=float(sub[sub.k == min(KS)].OOS_Sharpe.mean()),
                         hi_k_OOS=float(sub[sub.k == max(KS)].OOS_Sharpe.mean())))
    ew = books[(books.q == 1.00) & (books.arm == "EWall")]
    srow.append(dict(arm="EWall (r = breadth)", level=np.nan,
                     rho_k=spearman(ew.k, ew.OOS_Sharpe), rho_k_IS=spearman(ew.k, ew.IS_Sharpe),
                     rows=len(ew), lo_k_OOS=float(ew[ew.k == min(KS)].OOS_Sharpe.mean()),
                     hi_k_OOS=float(ew[ew.k == max(KS)].OOS_Sharpe.mean())))
    sl = pd.DataFrame(srow)
    sl["d_OOS_hi_lo"] = sl.hi_k_OOS - sl.lo_k_OOS
    P(sl.to_string(index=False, float_format=lambda x: f"{x:8.4f}"))
    A = float(sl[sl.arm == "A fixed-n"].rho_k.mean())
    B = float(sl[sl.arm == "B fixed-r"].rho_k.mean())
    SURV = B / A if A else np.nan
    signA = int((sl[sl.arm == "A fixed-n"].rho_k > 0).sum())
    signB = int((sl[sl.arm == "B fixed-r"].rho_k > 0).sum())
    P(f"\n  A (fixed n)  = {A:+.4f}  [positive on {signA}/{len(NS_FIXED)} levels]")
    P(f"  B (fixed r)  = {B:+.4f}  [positive on {signB}/{len(RATIOS)} levels]")
    P(f"  SURVIVAL     = B / A = {SURV:+.4f}")
    verdict_w = ("POOL-DEPTH" if (SURV >= BAR_SURV_HI and B >= BAR_B) else
                 "SELECTIVITY ARTEFACT" if (SURV <= BAR_SURV_LO or abs(B) <= BAR_FLAT) else
                 "MIXED")
    P(f"  -> WIDTH VERDICT: {verdict_w}")

    # capacity-bound subset
    ok = wc[wc.n_over_Ebar <= 1.0]
    Bok = float(np.mean([spearman(ok[ok.r_level == r].k, ok[ok.r_level == r].OOS_Sharpe)
                         for r in RATIOS]))
    Aok = float(np.mean([spearman(ok[ok.n == n].k, ok[ok.n == n].OOS_Sharpe) for n in NS_FIXED]))
    P(f"  capacity check (n <= Ebar_IS only, {len(ok)}/{len(wc)} rows): "
      f"A {Aok:+.4f}, B {Bok:+.4f}, survival {Bok / Aok if Aok else np.nan:+.4f}")

    # the ratio slope at fixed k, and the joint rank regression
    P("\n  the OTHER axis - within-k Spearman(r, OOS Sharpe) (ARM B cells only):")
    rk = [dict(k=k, rho_r=spearman(wc[(wc.k == k) & wc.in_B].r_level,
                                   wc[(wc.k == k) & wc.in_B].OOS_Sharpe),
               rho_n_fixedn=spearman(wc[(wc.k == k) & wc.in_A].n,
                                     wc[(wc.k == k) & wc.in_A].OOS_Sharpe)) for k in KS]
    P("    " + pd.DataFrame(rk).to_string(index=False, float_format=lambda x: f"{x:8.4f}")
      .replace("\n", "\n    "))
    b1, b2, r2 = ols_rank2(wc.OOS_Sharpe, np.log(wc.k), np.log(wc.r))
    P(f"\n  rank regression over ALL {len(wc)} q=1.00 CAND rows (k and n both free):")
    P(f"    OOS Sharpe ~ log k + log r :  beta_logk {b1:+.4f}   beta_logr {b2:+.4f}   R2 {r2:.4f}")
    b1b, b2b, r2b = ols_rank2(wc.OOS_Sharpe, np.log(wc.k), np.log(wc.n))
    P(f"    OOS Sharpe ~ log k + log n :  beta_logk {b1b:+.4f}   beta_logn {b2b:+.4f}   R2 {r2b:.4f}")
    b1c, b2c, r2c = ols_rank2(wc.Sharpe, np.log(wc.k), np.log(wc.r))
    P(f"    FULL Sharpe ~ log k + log r:  beta_logk {b1c:+.4f}   beta_logr {b2c:+.4f}   R2 {r2c:.4f}")

    # breadth is not moving with k (so n/k and n/n_elig are the same dial here)
    P(f"\n  Spearman(k, breadth) over the {len(mix[mix.q == 1.00])} q=1.00 panels: "
      f"{spearman(mix[mix.q == 1.00].k, mix[mix.q == 1.00].breadth):+.4f}  "
      f"(breadth {mix[mix.q == 1.00].breadth.min():.4f}..{mix[mix.q == 1.00].breadth.max():.4f}) "
      "- n/k and n/n_elig are the same dial on this ladder up to that spread.")

    # ------------------------------------------------------------ the cap-mix leg
    P("\n" + "=" * 100)
    P(f"THE CAP-MIX LEG - k = {K_CAP} held fixed, q swept, r held fixed")
    P("=" * 100)
    cc = cand[cand.k == K_CAP].copy()
    cc["r_level"] = [RCELL.get((K_CAP, int(n)), np.nan) for n in cc.n]
    capg = (cc[cc.r_level.notna()].groupby(["r_level", "q"])
            .agg(n=("n", "first"), OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                 OOS_DD=("OOS_MaxDD", "mean"), Sharpe=("Sharpe", "mean"),
                 rows=("OOS_Sharpe", "size")).reset_index())
    P(capg.to_string(index=False, float_format=lambda x: f"{x:8.4f}"))
    caprows = [dict(level=r, rho_q=spearman(cc[cc.r_level == r].q, cc[cc.r_level == r].OOS_Sharpe),
                    rows=int((cc.r_level == r).sum())) for r in RATIOS]
    capn = [dict(level=float(n), rho_q=spearman(cc[cc.n == n].q, cc[cc.n == n].OOS_Sharpe),
                 rows=int((cc.n == n).sum())) for n in NS_FIXED]
    CAP = float(np.nanmean([c["rho_q"] for c in caprows]))
    CAPn = float(np.nanmean([c["rho_q"] for c in capn]))
    P("\n  within-r Spearman(q, OOS Sharpe): " +
      ", ".join(f"r={c['level']:.2f} {c['rho_q']:+.4f}" for c in caprows))
    P("  within-n Spearman(q, OOS Sharpe): " +
      ", ".join(f"n={c['level']:.0f} {c['rho_q']:+.4f}" for c in capn))
    P(f"  CAP (mean over r) = {CAP:+.4f}   [fixed-n version {CAPn:+.4f}]")
    verdict_c = ("REAL CAP CHANNEL" if abs(CAP) >= BAR_CAP else
                 "NO CAP CHANNEL" if abs(CAP) <= BAR_FLAT else "WEAK")
    P(f"  -> CAP VERDICT: {verdict_c}")
    pd.concat([sl.assign(leg="width"),
               pd.DataFrame(caprows).assign(arm="CAP fixed-r", leg="cap"),
               pd.DataFrame(capn).assign(arm="CAP fixed-n", leg="cap")],
              ignore_index=True).to_csv(f"{OUT}.slopes.csv", index=False)

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - dials fitted on ..2016-12-31 ONLY, read once on 2017-01-01..")
    P("=" * 100)
    wrows = []
    for d, sd in wc.groupby("draw"):
        for k, sk in sd.groupby("k"):
            sb = sk[sk.in_B]
            if len(sb) == len(RATIOS):
                wrows.append(dict(draw=int(d), **wf_row(f"PICK-r @k={k}", sb,
                                                        sb.loc[sb.IS_Sharpe.idxmax()])))
            sa = sk[sk.in_A]
            if len(sa) == len(NS_FIXED):
                wrows.append(dict(draw=int(d), **wf_row(f"PICK-n @k={k}", sa,
                                                        sa.loc[sa.IS_Sharpe.idxmax()])))
        sb = sd[sd.in_B]
        if len(sb):
            wrows.append(dict(draw=int(d), **wf_row("PICK-(k,r) joint", sb,
                                                    sb.loc[sb.IS_Sharpe.idxmax()])))
        sa = sd[sd.in_A]
        if len(sa):
            wrows.append(dict(draw=int(d), **wf_row("PICK-(k,n) joint", sa,
                                                    sa.loc[sa.IS_Sharpe.idxmax()])))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    agg = (wf.groupby("selector")
             .agg(k=("k", "mean"), n=("n", "mean"), r=("r", "mean"),
                  OOS_S=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                  OOS_DD=("OOS_MaxDD", "mean"), anchor_S=("anchor_OOS_S", "mean"),
                  anchor_CAGR=("anchor_OOS_CAGR", "mean"), anchor_DD=("anchor_OOS_DD", "mean"),
                  best_S=("best_OOS_S", "mean"), v2_S=("v2_OOS_S", "mean"),
                  spy_S=("spy_OOS_S", "mean"), beats_anchor=("beats_anchor", "mean"),
                  beats_v2=("beats_v2", "mean"), beats_spy=("beats_spy", "mean"),
                  draws=("draw", "size")).reset_index())
    agg["edge_vs_anchor"] = agg.OOS_S - agg.anchor_S
    P(agg.to_string(index=False, float_format=lambda x: f"{x:8.4f}"))
    spyo = mix[mix.q == 1.00]
    P(f"  SPY OOS  : CAGR {spyo.spy_OOS_CAGR.mean():7.2%}  Sharpe {spyo.spy_OOS_S.mean():6.3f}  "
      f"MaxDD {spyo.spy_OOS_DD.mean():7.2%}")
    P(f"  RULES v2 : CAGR {spyo.v2_OOS_CAGR.mean():7.2%}  Sharpe {spyo.v2_OOS_S.mean():6.3f}  "
      f"MaxDD {spyo.v2_OOS_DD.mean():7.2%}  (on the same panels, OOS window)")

    P("\n  the joint selector's width choice (idea 688's question, with r free):")
    for lab in ("PICK-(k,r) joint", "PICK-(k,n) joint"):
        s = wf[wf.selector == lab]
        if not len(s): continue
        P(f"    {lab:18s} k picked: " +
          ", ".join(f"k={int(kk)} x{int(vv)}" for kk, vv in s.k.value_counts().sort_index().items()) +
          f"   mean OOS Sharpe {s.OOS_Sharpe.mean():+.4f} vs anchor {s.anchor_OOS_S.mean():+.4f}")

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 100)
    P("KEEP PATHS (PROTOCOL 4a vs RULES v2, 4b vs SPY; 10 bps, next-day, every book row)")
    P("=" * 100)
    kp = books.copy(); kp["r"] = kp.n / kp.k
    kp["cell"] = np.where(kp.arm == "EWall", "EWall",
                          np.where([RCELL.get((int(k), int(n) if pd.notna(n) else -1)) is not None
                                    for k, n in zip(kp.k, kp.n)], "ARM B (fixed r)", "ARM A (fixed n)"))
    tot = kp.groupby("cell").agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                                 p4b=("pass4b", "sum")).reset_index()
    P(tot.to_string(index=False))
    byk = kp[kp.q == 1.00].groupby("k").agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                                            p4b=("pass4b", "sum")).reset_index()
    P("\n  by width (q = 1.00 ladder):")
    P("    " + byk.to_string(index=False).replace("\n", "\n    "))
    if int(kp.pass4b.sum()):
        best = kp[kp.pass4b].sort_values("OOS_Sharpe", ascending=False).head(10)
        P("\n  4b passers (top 10 by OOS Sharpe):")
        P("    " + best[["panel", "arm", "k", "n", "r", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:8.4f}").replace("\n", "\n    "))
    else:
        P("\n  NO 4b pass anywhere on the grid.")
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    P("VERDICT")
    P("=" * 100)
    P(f"  A (fixed n, the record's arm)  {A:+.4f}")
    P(f"  B (fixed n/k, this run's arm)  {B:+.4f}   SURVIVAL {SURV:+.4f}  -> {verdict_w}")
    P(f"  CAP (q at matched k and r)     {CAP:+.4f}  -> {verdict_c}")
    P(f"  4a passes {int(kp.pass4a.sum())}/{len(kp)};  4b passes {int(kp.pass4b.sum())}/{len(kp)}")
    P(f"\ndone in {time.time() - t0all:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
