#!/usr/bin/env python3
"""Idea 703 - "is-the-RATIO-to-OOS-slope-steeper-at-the-WIDE-end-for-a-reason"
(lane C, 2026-09-11).

The question
------------
Idea 694 (lane C, committed today) held the SELECTION RATIO r = n/k fixed while sweeping the
panel width k, and found that the OTHER axis - the ratio itself - carries the OOS slope, and
that it carries MORE of it the wider the panel:

    within-k Spearman(r, OOS Sharpe), q = 1.00, ARM B cells (4 r-levels x 8 draws = 32 rows
    at each k):
        k =  40   60   80  100  200  400
        rho  -0.3693  -0.1393  -0.3724  -0.4632  -0.8325  -0.9415

The queue reads this as "the selectivity payoff is not a fixed dial but sharpens with pool
depth", and asks for it to be decomposed into (i) the dispersion of the score's top tail and
(ii) the cost of holding more names, with an explicit verdict on whether the sharpening is a
RANK-STATISTIC ARTEFACT "of having more cells to order".

Two things about the premise have to be said before it is decomposed, and this run says both
with numbers rather than adjusting the quote:

  * THE SEQUENCE IS NOT MONOTONE.  k = 40 -> 60 goes -0.3693 -> -0.1393, i.e. the slope gets
    FLATTER, by more than a third of the total span, before it turns.  The queue's word
    "monotonically" is wrong on the record's own six numbers; 5 of the 6 steps are monotone.
    This run reports the monotone-step count for every statistic it publishes.
  * "MORE CELLS TO ORDER" IS FALSE BY CONSTRUCTION on this ladder.  Every k carries exactly
    4 r-levels x 8 draws = 32 rows, and n = max(2, round(r*k)) is 4 DISTINCT values at every
    k (checked in GATE 2), so the pooled Spearman at k=400 orders neither more cells nor more
    distinct levels than at k=40.  The literal reading of the queue's artefact is refuted by
    counting; this run therefore tests the artefact that IS available to a rank statistic -
    ATTENUATION.  Spearman is a signal-to-NOISE statistic, not an effect size: pooling 4
    r-levels across 8 exchangeable draws attenuates rho by exactly the between-draw spread of
    OOS Sharpe.  On a 439-name pool, k=40 draws overlap ~9% and k=400 draws overlap ~91%, so
    the between-draw spread MUST collapse as k grows whether or not the r-effect changes at
    all.  That is the artefact with teeth, and it is what the bars below are set on.

Design - no new panels, no new dials, one exact counterfactual
-------------------------------------------------------------
PANELS: idea 688's own q = 1.00 ladder, rebuilt by importing its `build_ladder`
    (k in {40,60,80,100,200,400} x 8 draws = 48 panels, draws 0..2 replaying lane B's and
    idea 685's generators).  Pure SMALL439 draws, so NO cap-mix variation exists inside the
    ladder by construction and idea 694's cap channel cannot leak into this measurement.
BOOKS: idea 276/286's CAND-n at n = max(2, round(r*k)) for r in {0.05, 0.10, 0.25, 0.50} -
    idea 694's ARM B, re-run verbatim - plus EWall as the r = breadth limit point.

Tuned parameters (PROTOCOL rule 4: at most two) - ALL grid points reported
    1. SELECTION RATIO r = n/k in {0.05, 0.10, 0.25, 0.50}   (the queue's first named dial)
    2. WIDTH k in {40, 60, 80, 100, 200, 400}                (the queue's second named dial)
    Everything else is inherited from the committed record and is NOT chosen here: the RULES
    v1 gate (idea 276), CAND-n / EWall (idea 286), GROSS = 0.75, weekly cadence, 10 bps,
    next-day execution, the 260-day warm-up skip, the draws and seeds (2026 / 685 / 688).
    No level of r or k is dropped after the fact.

THE DECOMPOSITION (exact, non-parametric, and it costs no extra backtests)
-------------------------------------------------------------------------
Write the ARM B grid at width k as S_k(r, d), r a ratio level, d a draw.  Split it into the
r-PROFILE (what the ratio does, in Sharpe units) and the DRAW RESIDUAL (what the panel draw
does, i.e. the noise the pooled rank statistic has to see through):

    A_k(r)    = mean_d S_k(r, d)                         [the r-profile at width k]
    R_k(r, d) = S_k(r, d) - A_k(r)                       [draw effect + interaction]

and then TRANSPLANT one width's profile onto another's noise:

    Stilde(r, d | e, m) = A_e(r) + R_m(r, d)   ->   RHO(e, m) = Spearman(r, Stilde)

RHO(k, k) is the observed within-k rho EXACTLY (Spearman is invariant to the common location
shift), which is GATE 3.  The full 6 x 6 matrix is published.  The headline move
RHO(400,400) - RHO(40,40) then splits into

    EFFECT channel = RHO(400, 40) - RHO(40, 40)   [k=400's r-profile read at k=40's noise]
    NOISE  channel = RHO(40, 400) - RHO(40, 40)   [k=40's r-profile read at k=400's noise]
    INTERACTION    = total - EFFECT - NOISE

PRE-REGISTERED BARS (fixed here before any number in this run was read)
    share_NOISE  = NOISE / total,  share_EFFECT = EFFECT / total  (total = -0.5722 published)
      share_NOISE  >= 0.60  ->  RANK-STATISTIC ARTEFACT: the sharpening is the between-draw
                                spread collapsing as panels overlap, not the ratio biting
                                harder.
      share_EFFECT >= 0.60  ->  REAL SHARPENING: the r-profile itself steepens with k.
      otherwise            ->  SPLIT, with both shares quoted.
    Second, independent bar on the SHARPE-UNIT span (rank-free, so it cannot be attenuated):
      SPANRATIO = [A_400(0.05) - A_400(0.50)] / [A_40(0.05) - A_40(0.50)]
      SPANRATIO >= 1.50 -> the profile really does steepen;  <= 1.15 -> it does not.
    A run whose two bars disagree is reported as SPLIT with both, never rescued by a third.

CHANNEL SPLIT of whatever EFFECT survives - the queue's two named mechanisms
    (ii) COST OF HOLDING MORE NAMES is measured EXACTLY and for free: `engine.backtest`
         subtracts `turnover * cost_bps/1e4` from an otherwise cost-free return path, so the
         0 bps return series is the 10 bps series plus turnover*10/1e4, to machine precision
         (GATE 4 asserts this against a fresh cost_bps=0 backtest on 3 cells).  The whole
         profile is therefore re-read at 0 bps and
             COSTSHARE = 1 - span(A^0bps_400 - A^0bps_40) / span(A_400 - A_40).
    (i)  DISPERSION OF THE SCORE'S TOP TAIL is measured cost-free and book-free, on the same
         gate and the same weekly cadence, as a RANK-BUCKET ladder: B1 = ranks 1..n(0.05),
         B2 = (n05, n10], B3 = (n10, n25], B4 = (n25, n50], each held equal-weighted from one
         rebalance day to the next.  TAIL(k) = mean over draws of OOS Sharpe(B1) - Sharpe(B4).
         If the top tail's edge over the deep tail widens with k, TAIL(k) rises with k.
    A third channel the record already named (FILL / capacity, n vs Ebar) is reported and
    predicted INERT here: at fixed r everything scale-free is fixed, n/Ebar = r/breadth, and
    idea 694 measured rho(k, breadth) = -0.1356 over these same 48 panels.  Published, not
    tuned; if it moves, it is reported as moving.

Gates, asserted before any new number is read
    G0  REPRODUCTION-694: every ARM B book row (r x k x draw) is asserted against idea 694's
        committed `..._C.books.csv` at 1e-9 on CAGR/Sharpe/MaxDD/H1/H2/OOS_CAGR/OOS_Sharpe/
        OOS_MaxDD/IS_Sharpe, and the six published within-k rho values at 1e-4.  The number
        this run decomposes has to reproduce before it may be decomposed.
    G1  ENVELOPE: exact width, no duplicate columns, all columns inside SMALL439.
    G2  CELL COUNT: at every k the pooled Spearman orders exactly 4 distinct n values and 32
        rows - the literal "more cells to order" reading, tested and refuted by counting.
    G3  TRANSPLANT IDENTITY: RHO(k, k) == observed within-k rho at 1e-12 for all six k.
    G4  COST IDENTITY: the reconstructed 0 bps return series equals a fresh cost_bps=0
        `engine.backtest` on 3 sampled cells at 1e-15.
    G5  FAST-PATH IDENTITY: this run prices every book from ONE score/rank frame per panel
        instead of recomputing it per n; the resulting weights are asserted equal to
        idea 286's `cand_weights(n)` output at 0.0 on 3 sampled cells.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Dials chosen on the IS window (..2016-12-31) ONLY, OOS 2017-01-01.. read once, per draw:
      PICK-r @ k   : argmax over r of IS Sharpe at each width  (the dial this idea is about)
      PICK-(k,r)   : argmax over the WHOLE (k, r) grid of IS Sharpe
      R-MIN / R-MAX: the two fixed-ratio anchors, no choosing
    Every pick is reported against the choice-set mean (do-nothing anchor), against RULES v2
    on the SAME panel, and against SPY on the same calendar, with OOS CAGR / Sharpe / MaxDD.
    Both KEEP paths are evaluated on every book row (idea 286's `keep_paths`: 4a vs RULES v2,
    4b vs SPY, 10 bps).

SURVIVORSHIP (idea 54, data/SMALL_PANEL_README.md): SMALL439 is the CURRENT constituents of
its screen, so every LEVEL here is optimistic and this ladder is entirely small-cap.  The
object under test is a WITHIN-ladder rank statistic and a WITHIN-ladder Sharpe span; a
survivor list moves every panel in a ladder in the same direction, so it can bias the level
and not the sign of the decomposition.  No arm here is a new BOOK - CAND-n / EWall are the
record's existing books on re-drawn panels - so a 4a/4b pass is a statement about the panel,
not a capital candidate.

Outputs: .books.csv .profile.csv .transplant.csv .buckets.csv .walkforward.csv .keeppaths.csv
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

RATIOS = [0.05, 0.10, 0.25, 0.50]           # param 1
KS     = [40, 60, 80, 100, 200, 400]        # param 2

# pre-registered bars
BAR_SHARE, BAR_SPAN_HI, BAR_SPAN_LO = 0.60, 1.50, 1.15

# published quantities this run must reproduce before it may decompose them (GATE 0)
PUB_RHO_R = [-0.3693, -0.1393, -0.3724, -0.4632, -0.8325, -0.9415]
PUB_TOTAL = PUB_RHO_R[-1] - PUB_RHO_R[0]

GATECOLS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "IS_Sharpe"]


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P688 = BT / "2026-09-11_is-WIDTH-MAXIMISATION-a-general-rule-8-selector-pathology_C"
M688 = _load(f"{P688}.py", "idea688")
P694 = BT / "2026-09-11_is-the-WIDTH-to-OOS-slope-a-SELECTION-POOL-effect-or-a-SMALL-CAP-effect_C"

spearman, full_row, keep_paths = M286.spearman, M286.full_row, M286.keep_paths
from baseline import score, rules_v2_weights                         # noqa
from engine import backtest, rebalance_mask, metrics                 # noqa


def ratio_n(k, r):
    """Idea 694's ARM B book size: n = round(r*k), floored at 2 names."""
    return max(2, int(round(r * k)))


# ---------------------------------------------------------------- one panel, one score frame
def panel_frames(px):
    """The gate / score / rank frames idea 286's `cand_weights` rebuilds for every n, built
    ONCE per panel.  GATE 5 asserts the weights that come out are bit-identical."""
    tradables = [c for c in px.columns if c != "SPY"]
    sub = px[tradables]
    s, above, vol20 = score(sub, vol_scale=False)
    gate = above & (vol20 < 0.60)
    rank = s.where(gate).rank(axis=1, ascending=False)
    return tradables, gate, rank


def cand_w(px, tradables, rank, n):
    w = (rank <= n).astype(float) * (GROSS / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def ew_all_w(px, tradables, gate):
    e = gate.astype(float)
    w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def run_both(px, w):
    """One backtest -> the 10 bps series AND the exact 0 bps series (GATE 4)."""
    res = backtest(px, w, cost_bps=COST, freq=FREQ)
    r10 = res["returns"]
    r00 = r10 + res["turnover"] * COST / 1e4
    return r10, r00


def bucket_sharpe(px, tradables, rank, lo, hi):
    """Cost-free EW block book: hold ranks (lo, hi] from one weekly rebalance day to the next.
    Measures the score's top-tail dispersion without a book convention or a cost rung."""
    mem = ((rank > lo) & (rank <= hi)).astype(float)
    mask = np.asarray(rebalance_mask(px.index, FREQ).values, dtype=bool)
    keep = np.repeat(mask[:, None], mem.shape[1], axis=1)
    mem = mem.where(keep).ffill().fillna(0.0)
    w = mem.div(mem.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0).shift(1).fillna(0.0)
    rets = px[tradables].pct_change().fillna(0.0)
    return (w * rets).sum(axis=1)


# ---------------------------------------------------------------- main
def main():
    t0all = time.time()
    P("=" * 100)
    P("IDEA 703 - is-the-RATIO-to-OOS-slope-steeper-at-the-WIDE-end-for-a-reason  (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  decomposition: Stilde(r,d | e,m) = A_e(r) + R_m(r,d);  RHO(e,m) = Spearman(r, Stilde)")
    P(f"  total = RHO(400,400) - RHO(40,40)  [published {PUB_TOTAL:+.4f}]")
    P(f"  EFFECT = RHO(400,40) - RHO(40,40);  NOISE = RHO(40,400) - RHO(40,40)")
    P(f"  share_NOISE  >= {BAR_SHARE:.2f} -> RANK-STATISTIC ARTEFACT")
    P(f"  share_EFFECT >= {BAR_SHARE:.2f} -> REAL SHARPENING;  otherwise SPLIT")
    P(f"  second bar (rank-free): SPANRATIO >= {BAR_SPAN_HI:.2f} -> profile steepens; "
      f"<= {BAR_SPAN_LO:.2f} -> it does not")
    P(f"  grid: r in {RATIOS} x k in {KS}, q = 1.00, 8 draws.  Every cell reported.")

    # ------------------------------------------------------------ sources + panels
    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()} ({len(idx)} days); "
      f"SMALL pool {len(s_stk)} names")

    built, prov = M688.build_ladder(s_stk, b_stk)
    built = [(k, d, cols) for k, d, cols in built]
    P(f"LADDER: {len(built)} panels at q=1.00 "
      f"({sum(1 for v in prov.values() if v != 'new')} replayed from the record)")

    P("\n--- GATE 1: envelope ---")
    bad = []
    for k, d, cols in built:
        if len(cols) != k: bad.append((k, d, "width"))
        if len(set(cols)) != len(cols): bad.append((k, d, "dup"))
        if any(c not in s_stk for c in cols): bad.append((k, d, "pool"))
    assert not bad, f"GATE 1 FAILED: {bad[:5]}"
    P(f"  GATE 1 PASS - {len(built)} panels, exact width, no duplicate columns, all in SMALL{len(s_stk)}.")

    P("\n--- GATE 2: 'more cells to order' tested by counting ---")
    for k in KS:
        ns = [ratio_n(k, r) for r in RATIOS]
        nd = len(set(ns))
        P(f"  k={k:3d}: n = {ns}  distinct={nd}  rows at this k = {len(RATIOS)} r x 8 draws = 32")
        assert nd == len(RATIOS), f"GATE 2: tied n at k={k}: {ns}"
    P("  GATE 2 PASS - every k orders exactly 4 distinct n and 32 rows.  The literal "
      "'more cells to order' artefact is REFUTED BY CONSTRUCTION; the tested artefact is "
      "rank ATTENUATION by between-draw spread.")

    P("\n--- panel overlap (the mechanism the NOISE channel would run on) ---")
    ov = {}
    for k in KS:
        cs = [set(c) for kk, d, c in built if kk == k]
        pairs = [len(a & b) / k for i, a in enumerate(cs) for b in cs[i + 1:]]
        ov[k] = float(np.mean(pairs))
        P(f"  k={k:3d}: mean pairwise column overlap {ov[k]:.4f}  (k/pool = {k / len(s_stk):.4f})")

    # ------------------------------------------------------------ run the grid
    P("\n" + "=" * 100)
    P("RUNNING THE GRID  (one panel = one score frame, every ratio book priced off it)")
    P("=" * 100)
    brows, bkrows = [], []
    gate5_done, gate4_done = 0, 0
    for i, (k, d, cols) in enumerate(built):
        t0 = time.time()
        px = pd.concat([pxs_c[cols], spy.rename("SPY")], axis=1)[cols + ["SPY"]]
        px = px.dropna(how="all").ffill()
        st = px.index[260]
        tradables, gate, rank = panel_frames(px)
        Ebar = float(gate.loc[rebalance_mask(px.index, FREQ).values].iloc[40:].sum(axis=1).mean())

        spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
        v2w = rules_v2_weights(px).drop(columns=["SPY"], errors="ignore").reindex(columns=px.columns).fillna(0.0)
        v2_r = full_row("v2", backtest(px, v2w, cost_bps=COST, freq=FREQ)["returns"].loc[st:])

        for r in RATIOS:
            n = ratio_n(k, r)
            w = cand_w(px, tradables, rank, n)
            if gate5_done < 3:                                  # GATE 5
                wref = M286.cand_weights(n)(px)
                assert float((w - wref).abs().max().max()) == 0.0, "GATE 5 FAILED"
                gate5_done += 1
            r10, r00 = run_both(px, w)
            if gate4_done < 3:                                  # GATE 4
                ref0 = backtest(px, w, cost_bps=0, freq=FREQ)["returns"]
                assert float((r00 - ref0).abs().max()) < 1e-15, "GATE 4 FAILED"
                gate4_done += 1
            row10 = full_row(f"CAND{n}", r10.loc[st:])
            row00 = full_row(f"CAND{n}_0bps", r00.loc[st:])
            a, b = keep_paths(row10, spy_r, v2_r)
            brows.append(dict(panel=f"MIX q=1.00 k={k} d{d}", k=k, draw=d, r=r, n=n, arm="CAND",
                              Ebar=Ebar, n_over_Ebar=n / Ebar, breadth=Ebar / k,
                              **{kk: vv for kk, vv in row10.items() if kk != "tag"},
                              **{f"{kk}_0bps": vv for kk, vv in row00.items() if kk != "tag"},
                              spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                              spy_H1=spy_r["H1"], spy_H2=spy_r["H2"],
                              spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                              spy_OOS_DD=spy_r["OOS_MaxDD"],
                              v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                              v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                              v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                              pass4a=a, pass4b=b))

        ew10, ew00 = run_both(px, ew_all_w(px, tradables, gate))
        rowE = full_row("EWall", ew10.loc[st:]); rowE0 = full_row("EWall0", ew00.loc[st:])
        a, b = keep_paths(rowE, spy_r, v2_r)
        brows.append(dict(panel=f"MIX q=1.00 k={k} d{d}", k=k, draw=d, r=np.nan, n=np.nan, arm="EWall",
                          Ebar=Ebar, n_over_Ebar=np.nan, breadth=Ebar / k,
                          **{kk: vv for kk, vv in rowE.items() if kk != "tag"},
                          **{f"{kk}_0bps": vv for kk, vv in rowE0.items() if kk != "tag"},
                          spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                          spy_H1=spy_r["H1"], spy_H2=spy_r["H2"],
                          spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                          spy_OOS_DD=spy_r["OOS_MaxDD"],
                          v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                          v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"],
                          v2_OOS_CAGR=v2_r["OOS_CAGR"], v2_OOS_DD=v2_r["OOS_MaxDD"],
                          pass4a=a, pass4b=b))

        # ---- top-tail dispersion ladder (cost-free, book-free)
        edges = [0] + [ratio_n(k, r) for r in RATIOS]
        for bi in range(4):
            lo, hi = edges[bi], edges[bi + 1]
            rb = bucket_sharpe(px, tradables, rank, lo, hi).loc[st:]
            m_oos, m_full = metrics(rb.loc[OOS_START:]), metrics(rb)
            bkrows.append(dict(panel=f"MIX q=1.00 k={k} d{d}", k=k, draw=d, block=f"B{bi + 1}",
                               lo=lo, hi=hi, width=hi - lo,
                               Sharpe=m_full["Sharpe"], CAGR=m_full["CAGR"], MaxDD=m_full["MaxDD"],
                               OOS_Sharpe=m_oos["Sharpe"], OOS_CAGR=m_oos["CAGR"],
                               OOS_MaxDD=m_oos["MaxDD"]))
        P(f"  [{i + 1:2d}/{len(built)}] k={k:3d} d{d}  n={[ratio_n(k, r) for r in RATIOS]}  "
          f"Ebar={Ebar:6.1f}  {time.time() - t0:5.1f}s (elapsed {time.time() - t0all:6.1f}s)")

    books = pd.DataFrame(brows); bks = pd.DataFrame(bkrows)
    books.to_csv(f"{OUT}.books.csv", index=False)
    bks.to_csv(f"{OUT}.buckets.csv", index=False)
    P(f"\n  GATE 4 PASS ({gate4_done} cells, 0 bps identity < 1e-15);  "
      f"GATE 5 PASS ({gate5_done} cells, weights identical at 0.0)")

    # ------------------------------------------------------------ GATE 0
    P("\n" + "=" * 100)
    P("GATE 0 - REPRODUCTION of idea 694's committed ARM B rows")
    P("=" * 100)
    ref = pd.read_csv(f"{P694}.books.csv")
    ref = ref[(ref.kind == "mix") & (ref.q == 1.00) & (ref.arm != "EWall")].copy()
    ref["n"] = ref.n.astype(float)
    mine = books[books.arm == "CAND"].copy()
    mine["n"] = mine.n.astype(float)
    m = mine.merge(ref, on=["panel", "n"], suffixes=("", "_ref"))
    P(f"  {len(m)} overlapping book rows (of {len(mine)} ARM B rows this run priced)")
    worst = {}
    for c in GATECOLS:
        dd = (m[c] - m[f"{c}_ref"]).abs(); worst[c] = float(dd.max())
        P(f"    {c:12s} max |delta| {dd.max():.3e}   >1e-9: {int((dd > 1e-9).sum())}/{len(dd)}")
    assert max(worst.values()) < 1e-9, f"GATE 0 FAILED: {worst}"
    P(f"  GATE 0 PASS - worst |delta| {max(worst.values()):.3e}")

    cand = books[books.arm == "CAND"].copy()
    rho_obs = {k: spearman(cand[cand.k == k].r, cand[cand.k == k].OOS_Sharpe) for k in KS}
    P("\n  the six published within-k rho(r, OOS Sharpe), re-measured from this run's books:")
    worstr = 0.0
    for k, pub in zip(KS, PUB_RHO_R):
        worstr = max(worstr, abs(rho_obs[k] - pub))
        P(f"    k={k:3d}  this run {rho_obs[k]:+.4f}   published {pub:+.4f}   "
          f"|delta| {abs(rho_obs[k] - pub):.2e}")
    assert worstr < 1e-4, f"GATE 0b FAILED: worst {worstr:.2e}"
    steps = [rho_obs[KS[i + 1]] - rho_obs[KS[i]] for i in range(len(KS) - 1)]
    nmono = sum(1 for s in steps if s <= 0)
    P(f"  GATE 0b PASS - worst |delta| {worstr:.2e}")
    P(f"  MONOTONICITY of the published sequence: {nmono}/{len(steps)} steps are downward; "
      f"the k=40->60 step is {steps[0]:+.4f} (UP).  The queue's 'monotonically' is WRONG on "
      f"the record's own numbers - the first step retraces "
      f"{abs(steps[0]) / abs(PUB_TOTAL) * 100:.1f}% of the total span.")

    # ------------------------------------------------------------ profile / residual
    P("\n" + "=" * 100)
    P("THE PROFILE A_k(r) AND THE DRAW RESIDUAL R_k(r,d)")
    P("=" * 100)
    piv = cand.pivot_table(index=["k", "r"], columns="draw", values="OOS_Sharpe")
    piv0 = cand.pivot_table(index=["k", "r"], columns="draw", values="OOS_Sharpe_0bps")
    A = {k: np.array([piv.loc[(k, r)].mean() for r in RATIOS]) for k in KS}
    A0 = {k: np.array([piv0.loc[(k, r)].mean() for r in RATIOS]) for k in KS}
    R = {k: np.array([[piv.loc[(k, r)][d] - A[k][j] for d in piv.columns]
                      for j, r in enumerate(RATIOS)]) for k in KS}
    prof = []
    P(f"  {'k':>4} " + " ".join(f"A(r={r:.2f})" for r in RATIOS) +
      "   span   span0bps   sd_draw   SNR   rho_blk  mono")
    for k in KS:
        span = A[k][0] - A[k][-1]; span0 = A0[k][0] - A0[k][-1]
        sd = float(np.mean([piv.loc[(k, r)].std(ddof=1) for r in RATIOS]))
        blk = float(np.mean([spearman(RATIOS, [piv.loc[(k, r)][d] for r in RATIOS])
                             for d in piv.columns]))
        mono = sum(1 for j in range(len(RATIOS) - 1) if A[k][j + 1] <= A[k][j])
        P(f"  {k:>4} " + " ".join(f"{A[k][j]:+9.4f}" for j in range(len(RATIOS))) +
          f"  {span:+.4f}  {span0:+.4f}   {sd:.4f}  {span / sd:5.2f}  {blk:+.4f}  {mono}/3")
        prof.append(dict(k=k, **{f"A_r{r:.2f}": A[k][j] for j, r in enumerate(RATIOS)},
                         **{f"A0_r{r:.2f}": A0[k][j] for j, r in enumerate(RATIOS)},
                         span=span, span_0bps=span0, sd_draw=sd, SNR=span / sd,
                         rho_pooled=rho_obs[k], rho_blocked=blk, overlap=ov[k],
                         mono_steps=mono,
                         Ebar=float(cand[cand.k == k].Ebar.mean()),
                         breadth=float(cand[cand.k == k].breadth.mean())))
    pd.DataFrame(prof).to_csv(f"{OUT}.profile.csv", index=False)

    # ------------------------------------------------------------ the transplant matrix
    P("\n" + "=" * 100)
    P("THE TRANSPLANT MATRIX  RHO(effect from e, noise from m)")
    P("=" * 100)
    rvec = np.repeat(RATIOS, len(piv.columns))
    RHO = pd.DataFrame(index=KS, columns=KS, dtype=float)
    for e in KS:
        for mm in KS:
            S = (A[e][:, None] + R[mm]).ravel()
            RHO.loc[e, mm] = spearman(rvec, S)
    P("  rows = r-profile source (e), cols = draw-noise source (m)")
    P("        " + " ".join(f"m={k:>4}" for k in KS))
    for e in KS:
        P(f"  e={e:>4} " + " ".join(f"{RHO.loc[e, k]:+.4f}" for k in KS))
    diag = max(abs(RHO.loc[k, k] - rho_obs[k]) for k in KS)
    assert diag < 1e-12, f"GATE 3 FAILED: {diag:.3e}"
    P(f"  GATE 3 PASS - diagonal equals the observed within-k rho at {diag:.3e}")
    RHO.to_csv(f"{OUT}.transplant.csv")

    lo, hi = KS[0], KS[-1]
    total = RHO.loc[hi, hi] - RHO.loc[lo, lo]
    eff = RHO.loc[hi, lo] - RHO.loc[lo, lo]
    noi = RHO.loc[lo, hi] - RHO.loc[lo, lo]
    inter = total - eff - noi
    sh_e, sh_n, sh_i = eff / total, noi / total, inter / total
    P(f"\n  total  RHO(400,400) - RHO(40,40) = {total:+.4f}  (published {PUB_TOTAL:+.4f})")
    P(f"  EFFECT RHO(400, 40) - RHO(40,40) = {eff:+.4f}   share {sh_e:+.1%}")
    P(f"  NOISE  RHO( 40,400) - RHO(40,40) = {noi:+.4f}   share {sh_n:+.1%}")
    P(f"  INTERACTION                      = {inter:+.4f}   share {sh_i:+.1%}")

    spanratio = (A[hi][0] - A[hi][-1]) / (A[lo][0] - A[lo][-1])
    P(f"\n  SPANRATIO (rank-free) = {A[hi][0] - A[hi][-1]:+.4f} / {A[lo][0] - A[lo][-1]:+.4f} "
      f"= {spanratio:.3f}")

    if sh_n >= BAR_SHARE: v1 = "RANK-STATISTIC ARTEFACT"
    elif sh_e >= BAR_SHARE: v1 = "REAL SHARPENING"
    else: v1 = "SPLIT"
    v2 = ("profile steepens" if spanratio >= BAR_SPAN_HI else
          "profile does NOT steepen" if spanratio <= BAR_SPAN_LO else "profile steepens WEAKLY")
    P(f"\n  BAR 1 (shares)    -> {v1}")
    P(f"  BAR 2 (span ratio) -> {v2}")

    # ------------------------------------------------------------ channel split of EFFECT
    P("\n" + "=" * 100)
    P("CHANNEL SPLIT of the EFFECT half - the queue's two named mechanisms")
    P("=" * 100)
    d_span = (A[hi][0] - A[hi][-1]) - (A[lo][0] - A[lo][-1])
    d_span0 = (A0[hi][0] - A0[hi][-1]) - (A0[lo][0] - A0[lo][-1])
    costshare = 1 - d_span0 / d_span if d_span else np.nan
    P(f"  (ii) COST OF HOLDING MORE NAMES (exact, turnover identity):")
    P(f"       span growth k=40->400 at 10 bps {d_span:+.4f}, at 0 bps {d_span0:+.4f}  "
      f"-> COSTSHARE {costshare:+.1%}")
    for k in KS:
        c = [A[k][j] - A0[k][j] for j in range(len(RATIOS))]
        P(f"       k={k:3d}  cost drag by r: " + " ".join(f"{x:+.4f}" for x in c))

    P(f"\n  (i) DISPERSION OF THE SCORE'S TOP TAIL (cost-free rank-bucket ladder):")
    P(f"      {'k':>4}  " + "  ".join(f"{b:>8}" for b in ["B1", "B2", "B3", "B4"]) + "     TAIL=B1-B4")
    tails = {}
    for k in KS:
        sub = bks[bks.k == k]
        mu = [float(sub[sub.block == f"B{i + 1}"].OOS_Sharpe.mean()) for i in range(4)]
        tails[k] = mu[0] - mu[3]
        P(f"      {k:>4}  " + "  ".join(f"{x:+8.4f}" for x in mu) + f"     {tails[k]:+.4f}")
    tail_ratio = tails[hi] / tails[lo] if tails[lo] else np.nan
    P(f"      TAIL(400)/TAIL(40) = {tail_ratio:.3f}   "
      f"rho(k, TAIL) = {spearman(KS, [tails[k] for k in KS]):+.4f}")

    P(f"\n  (iii) FILL / CAPACITY (predicted INERT at fixed r, published either way):")
    P(f"      {'k':>4}  breadth   Ebar   " + "  ".join(f"n/Ebar@r={r:.2f}" for r in RATIOS))
    for k in KS:
        sub = cand[cand.k == k]
        row = [float(sub[sub.r == r].n_over_Ebar.mean()) for r in RATIOS]
        P(f"      {k:>4}  {sub.breadth.mean():.4f}  {sub.Ebar.mean():6.1f}   " +
          "  ".join(f"{x:12.3f}" for x in row))
    P(f"      rho(k, breadth) over the {len(built)} panels = "
      f"{spearman(cand.groupby('panel').k.first(), cand.groupby('panel').breadth.first()):+.4f}")

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - r chosen on 2009..2016 IS Sharpe, 2017..2026 read ONCE")
    P("=" * 100)
    wf = []
    for k in KS:
        for d in sorted(cand.draw.unique()):
            sub = cand[(cand.k == k) & (cand.draw == d)]
            if not len(sub): continue
            for lab, pick in (("PICK-r", sub.loc[sub.IS_Sharpe.idxmax()]),
                              ("R-MIN", sub[sub.r == min(RATIOS)].iloc[0]),
                              ("R-MAX", sub[sub.r == max(RATIOS)].iloc[0])):
                wf.append(dict(scope=f"k={k}", k=k, draw=d, selector=lab, r=float(pick.r),
                               n=int(pick.n), IS_Sharpe=float(pick.IS_Sharpe),
                               OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                               OOS_MaxDD=float(pick.OOS_MaxDD),
                               anchor_OOS_S=float(sub.OOS_Sharpe.mean()),
                               anchor_OOS_CAGR=float(sub.OOS_CAGR.mean()),
                               best_OOS_S=float(sub.OOS_Sharpe.max()),
                               v2_OOS_S=float(pick.v2_OOS_S), v2_OOS_CAGR=float(pick.v2_OOS_CAGR),
                               v2_OOS_DD=float(pick.v2_OOS_DD),
                               spy_OOS_S=float(pick.spy_OOS_S), spy_OOS_CAGR=float(pick.spy_OOS_CAGR),
                               spy_OOS_DD=float(pick.spy_OOS_DD),
                               beats_anchor=bool(pick.OOS_Sharpe > sub.OOS_Sharpe.mean()),
                               beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                               beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    for d in sorted(cand.draw.unique()):
        sub = cand[cand.draw == d]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        wf.append(dict(scope="whole (k,r) grid", k=int(pick.k), draw=d, selector="PICK-(k,r)",
                       r=float(pick.r), n=int(pick.n), IS_Sharpe=float(pick.IS_Sharpe),
                       OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                       OOS_MaxDD=float(pick.OOS_MaxDD),
                       anchor_OOS_S=float(sub.OOS_Sharpe.mean()),
                       anchor_OOS_CAGR=float(sub.OOS_CAGR.mean()),
                       best_OOS_S=float(sub.OOS_Sharpe.max()),
                       v2_OOS_S=float(pick.v2_OOS_S), v2_OOS_CAGR=float(pick.v2_OOS_CAGR),
                       v2_OOS_DD=float(pick.v2_OOS_DD),
                       spy_OOS_S=float(pick.spy_OOS_S), spy_OOS_CAGR=float(pick.spy_OOS_CAGR),
                       spy_OOS_DD=float(pick.spy_OOS_DD),
                       beats_anchor=bool(pick.OOS_Sharpe > sub.OOS_Sharpe.mean()),
                       beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                       beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {'selector':>14} {'scope':>16}  cells  meanOOS_S  meanOOS_CAGR  meanOOS_DD  "
      f"beats_anchor  beats_v2  beats_SPY")
    for (lab, sc), g in wfd.groupby(["selector", "scope"], sort=False):
        P(f"  {lab:>14} {sc:>16}  {len(g):5d}  {g.OOS_Sharpe.mean():+9.4f}  "
          f"{g.OOS_CAGR.mean():+12.2%}  {g.OOS_MaxDD.mean():+10.2%}  "
          f"{g.beats_anchor.sum():12d}  {g.beats_v2.sum():8d}  {g.beats_spy.sum():9d}")
    P(f"\n  benchmarks on the same OOS window: SPY  Sharpe {cand.spy_OOS_S.mean():+.4f}  "
      f"CAGR {cand.spy_OOS_CAGR.mean():+.2%}  MaxDD {cand.spy_OOS_DD.mean():+.2%}")
    P(f"                                      RULES v2 (per panel, mean) Sharpe "
      f"{cand.v2_OOS_S.mean():+.4f}  CAGR {cand.v2_OOS_CAGR.mean():+.2%}  "
      f"MaxDD {cand.v2_OOS_DD.mean():+.2%}")
    P(f"  IS-picked r by width (mode over draws): " +
      "  ".join(f"k={k}:r={wfd[(wfd.selector == 'PICK-r') & (wfd.k == k)].r.mode().iloc[0]:.2f}"
                for k in KS))
    ppr = wfd[wfd.selector == "PICK-r"]
    rmin = wfd[wfd.selector == "R-MIN"]
    P(f"  cost of CHOOSING r on IS vs just taking r = 0.05: "
      f"{ppr.OOS_Sharpe.mean() - rmin.OOS_Sharpe.mean():+.4f} of OOS Sharpe "
      f"({int((ppr.OOS_Sharpe.values > rmin.OOS_Sharpe.values).sum())}/{len(ppr)} cells better)")

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4) on every book row, 10 bps")
    P("=" * 100)
    books.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(f"  4a (beat RULES v2 both halves, MaxDD no worse): {int(books.pass4a.sum())}/{len(books)}")
    P(f"  4b (beat SPY both halves + OOS, DD <= 60% SPY, CAGR >= 70% SPY): "
      f"{int(books.pass4b.sum())}/{len(books)}")
    if books.pass4b.any():
        b4 = books[books.pass4b].sort_values("OOS_Sharpe", ascending=False)
        P("  4b passers (panel / arm / n / CAGR / Sharpe / MaxDD / OOS Sharpe):")
        for _, x in b4.head(20).iterrows():
            P(f"    {x.panel:22s} {x.arm}{'' if np.isnan(x.n) else int(x.n)}  "
              f"{x.CAGR:7.2%}  {x.Sharpe:6.4f}  {x.MaxDD:7.2%}  OOS {x.OOS_Sharpe:6.4f}")
    P(f"  by width, 4b passes: " +
      "  ".join(f"k={k}:{int(books[books.k == k].pass4b.sum())}/{len(books[books.k == k])}"
                for k in KS))

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 100)
    P("VERDICT")
    P("=" * 100)
    P(f"  BAR 1 shares: EFFECT {sh_e:+.1%} / NOISE {sh_n:+.1%} / INTERACTION {sh_i:+.1%} -> {v1}")
    P(f"  BAR 2 span ratio {spanratio:.3f} -> {v2}")
    P(f"  COSTSHARE of the surviving span growth {costshare:+.1%}; "
      f"TAIL(400)/TAIL(40) {tail_ratio:.3f}")
    P(f"  monotonicity of the published sequence: {nmono}/5 steps (the queue says 6/5)")
    P(f"  total runtime {time.time() - t0all:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(rho_obs=rho_obs, RHO=RHO, total=total, eff=eff, noi=noi, inter=inter,
                spanratio=spanratio, costshare=costshare, tails=tails, v1=v1, v2=v2)


if __name__ == "__main__":
    main()
