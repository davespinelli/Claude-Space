#!/usr/bin/env python3
"""Idea 685 - "extend-the-q-x-k-ladder-past-k-EQUALS-100" (lane C, 2026-09-11).

The question
------------
Idea 525 (lane B) broke idea 286's breadth/n_elig confound with a two-factor panel ladder
(q = share of the panel drawn from SMALL439, k = panel width) and classified the record's
five published "panel property explains the result" statistics by a rank regression on
(log breadth, log k) - the coordinates that span (log Ebar, log k), since

        log Ebar == log breadth + log k        EXACTLY.

Its verdict: 3 of 5 are eligible-SHARE claims, 1 (S2, idea 153's overlap) is a RAW PANEL
WIDTH claim (beta_logk -0.919 vs beta_logbreadth -0.421), 1 is NULL, 0 are n_elig.

The defect idea 685 names: that ladder's k arm spans 40..100, i.e. **2.5x**, capped because
BSTK100 (the broad panel minus every ETF) has exactly 100 names and q=0 cannot be built
wider.  The record itself publishes panel claims across ETF36 (k=35) .. SMALL439 (k=439),
i.e. **12.5x**.  A width classification fitted on 2.5x of width and read onto 12.5x of
width is an extrapolation, and the single statistic lane B called "raw width" is exactly
the one that would be most sensitive to it.

The queue's ask (idea 685): "Build a wider large-cap pool (or run the k arm on q>=0.5 only,
where SMALL439 supplies 439 names) and re-read the classification at k up to 400."

This sandbox has no internet, so the large-cap pool cannot be widened (BSTK100 is the whole
committed cache).  This run therefore takes the queue's OWN second option: restrict to
q >= 0.5 and extend k to 400.

Design - the feasible envelope
------------------------------
A (q, k) cell needs q*k names from SMALL439 (439 available) and (1-q)*k from BSTK100
(100 available), so it exists iff  q*k <= 439  AND  (1-q)*k <= 100:

    q=0.50 -> k <= 200        q=0.75 -> k <= 400        q=1.00 -> k <= 439

    k    |  40   60   80  100  200  400
    -----+------------------------------
    0.50 |   x    x    x    x    x    .
    0.75 |   x    x    x    x    x    x
    1.00 |   x    x    x    x    x    x

17 cells x 3 draws = 51 panels.  k spans 40..400 = **10.0x**, against lane B's 2.5x and the
record's own 12.5x.  This is the widest k arm the committed caches can support at all.

THREE READINGS, so the k extension is isolated from the q restriction
--------------------------------------------------------------------
Restricting to q >= 0.5 changes the support on its own, so "wide vs lane B" would confound
two changes.  Every statistic is therefore classified three times:

    (N) NARROW  q >= 0.5, k <= 100   (36 panels)  - lane B's panels, REPRODUCED (gate 0)
    (W) WIDE    q >= 0.5, k <= 400   (51 panels)  - N plus the 15 new wide panels
    (B) lane B  q in [0,1], k <= 100 (58 panels)  - read from its committed .decomp.csv

        W - N  =  the k EXTENSION, on matched q support   <- what idea 685 asks for
        N - B  =  the q RESTRICTION, at matched k         <- the cost of the envelope

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.50, 0.75, 1.00}      2. k in {40, 60, 80, 100, 200, 400}
    Everything else is inherited, not chosen: the RULES v1 gate, GROSS=0.75, weekly cadence,
    10 bps, next-day execution, the 260-day warm-up skip, the SPY benchmark column, the
    3 seeded draws per cell and NS_LAD = {5,10,15,20,30} are lane B's / idea 286's published
    conventions.  NS_LAD is still truncated at 30 so max(n) < min(k) = 40, for lane B's
    reason: CAND-40 on a k=40 panel IS the equal-weight book.  ALL 17 cells, ALL 51 panels,
    ALL 5 statistics and ALL 306 book rows are reported, not a selected subset.

PRE-REGISTERED CLASSIFICATION BAR (fixed here before any number in this run was read)
-------------------------------------------------------------------------------------
Lane B's bar, transported unchanged in magnitude and in sign-consistency SHARE:

    A statistic S is an **n_elig statistic** iff
        |mean over the q-levels of within-q Spearman(S, Ebar)| >= 0.30, and that sign holds
        in >= ceil(0.727 * L_q) of the L_q q-levels.
    A statistic S is a **breadth statistic** iff
        |mean over the Ebar-quintile bins of within-bin Spearman(S, breadth)| >= 0.30, and
        that sign holds in >= ceil(0.727 * 5) of the 5 bins.
    Both -> JOINT.  Neither -> NULL.

0.727 is idea 286's own 8-of-11; lane B rounded it to 4-of-5 on a 5-level grid.  On this
grid L_q = 3, so ceil(0.727*3) = 3 -> the q-side needs 3 of 3 and the bin-side 4 of 5.
REPORTED HONESTLY, NOT HIDDEN: 3-of-3 is a STRICTER gate than lane B's 4-of-5 (100% vs 80%
of levels), purely because 3 levels cannot express 80%.  That asymmetry biases this run
AGAINST an n_elig classification, so an n_elig verdict here is conservative and a
non-n_elig verdict is partly a discreteness artefact.  The 2-of-3 variant is therefore
computed and printed beside every headline as a labelled SENSITIVITY - it is not the
headline, and no verdict in the result memo is taken from it.

Gates, asserted before any new number is read
    G0  THE REPRODUCTION GATE.  Lane B's rng draw sequence (seed 2026, its full QS x KS x
        N_DRAWS loop in its own order, including the q=0.00/0.25 cells whose draws advance
        the generator) is replayed here, and the q >= 0.5 subset re-measured from scratch.
        Asserted against lane B's COMMITTED .panels.csv and .stats.csv at 1e-9 on Ebar,
        breadth, Emed, Ebar_IS, breadth_IS and on S1..S5, EW_Sharpe, ADAPT_Sharpe,
        best_prem.  These panels are drawn from prices_broad.csv / prices_small.csv, which
        the daily close job does not restate (idea 513), and SPY never enters a gate matrix
        or a CAND/EWall book - so machine precision is the right bar and any failure is a
        code-path difference, not drift.  The SPY-dependent columns (spy_*, v2_*) are
        reported separately, at the looser bar drift allows.
    G1  THE k-IDENTITY: max |k * breadth - Ebar| over all 51 panels, asserted < 1e-9.
    G2  ENVELOPE: every built cell satisfies q*k <= 439 and (1-q)*k <= 100, and the drawn
        column sets are duplicate-free within a cell.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Panel properties measured on 2010..2016 only (Ebar_IS, breadth_IS).  Five selectors -
    EBAR-MAX, EBAR-MIN, BREADTH-MAX, BREADTH-MIN, IS-SHARPE-MAX - each pick one panel per
    book size n on the IS window; the pick is read once on 2017-01-01..end, untouched.  Run
    TWICE, once with the NARROW choice set (k <= 100) and once with the WIDE one (k <= 400),
    so the rule-8 arm answers idea 685 directly: does giving the selector 10x of width
    instead of 2.5x change what it picks and what that pick earns?  Reported per n and
    pooled against the do-nothing anchor (mean OOS over the choice set), RULES v2 on the
    same panel, and SPY.

KEEP paths (PROTOCOL rule 4, both evaluated on every arm row, 10 bps, in .books.csv)
    4a vs RULES v2 on the same panel; 4b vs SPY.  Broken out by k so the wide panels are
    visible separately.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens (see
data/SMALL_PANEL_README.md); every level here is optimistic, and the q >= 0.5 envelope this
idea forces makes the whole ladder MORE small-cap than lane B's, hence more exposed.  The
object under test is which COORDINATE of the panel carries a statistic; survivorship reaches
that only through the level of the eligible share, not through the k slice.  No arm here is
a new BOOK - CAND-n and EWall are the record's existing books re-run on re-drawn panels, so
a 4a/4b pass is a statement about the panel, not a capital candidate.

Outputs: .panels.csv .stats.csv .books.csv .decomp.csv .walkforward.csv .console.txt
         .result.md
"""
import importlib.util, math, sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v2_weights          # noqa
from engine import rebalance_mask              # noqa

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- this run's grid (2 tuned params) -------------------------------------------------
QS   = [0.50, 0.75, 1.00]
KS   = [40, 60, 80, 100, 200, 400]
NS_LAD = [5, 10, 15, 20, 30]
N_DRAWS = 3
SEED_B, SEED_NEW = 2026, 685            # SEED_B replays lane B; SEED_NEW draws only k>100
NARROW_K = 100                          # the lane-B ceiling, the matched-control boundary
BAR_RHO, N_BINS = 0.30, 5
SHARE = 8 / 11                          # idea 286's own 8-of-11 sign-consistency share

def need(levels):                       # pre-registered, applied to both slices
    return int(math.ceil(SHARE * levels))

# ---------------------------------------------------------------- import the record
def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P525 = BT / "2026-09-11_is-n_elig-the-variable-the-record-keeps-mislabelling_B"

# every statistic definition is idea 286's / lane B's, imported, never re-typed
cand_weights, ewall_weights = M286.cand_weights, M286.ewall_weights
adaptive_weights, overlap_inv_none = M286.adaptive_weights, M286.overlap_inv_none
run, full_row, keep_paths, spearman = M286.run, M286.full_row, M286.keep_paths, M286.spearman
partial_spearman = M286.partial_spearman

M525 = _load(f"{P525}.py", "idea525")
within_slice_rho, rank_ols2, beta_reading = M525.within_slice_rho, M525.rank_ols2, M525.beta_reading
panel_measures, do_panel = M525.panel_measures, M525.do_panel
SLABEL, SCOLS = M525.SLABEL, M525.SCOLS

# lane B's ladder constants, needed to REPLAY its rng sequence exactly
QS_B, KS_B, NDRAWS_B = M525.QS, M525.KS, M525.N_DRAWS


# ---------------------------------------------------------------- panel construction
def build_ladder(s_stk, b_stk):
    """Return (built, from_B) where built is [(q,k,draw,small_cols,large_cols)].

    The k <= 100 half is lane B's EXACT panel set: its full nested loop is replayed on a
    generator seeded identically, so the generator state at every cell matches, and the
    q >= 0.5 cells therefore receive byte-identical column sets.  The k > 100 half is drawn
    from a SEPARATE generator so it cannot perturb that replay.
    """
    built, from_B, seen = [], set(), set()
    rng = np.random.default_rng(SEED_B)
    for q in QS_B:
        for k in KS_B:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(NDRAWS_B):
                sc = sorted(rng.choice(s_stk, size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(b_stk, size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    continue                      # lane B's dedupe, same position in the loop
                seen.add(key)
                if q in QS and k in KS:           # keep only this run's envelope
                    built.append((q, k, d, sc, lc))
                    from_B.add((q, k, d))
    rng2 = np.random.default_rng(SEED_NEW)
    for q in QS:
        for k in KS:
            if k <= NARROW_K: continue
            ns_ = int(round(q * k)); nl_ = k - ns_
            if ns_ > len(s_stk) or nl_ > len(b_stk): continue      # outside the envelope
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
    return built, from_B


def classify(df, qcol="q", tag=""):
    """The pre-registered classification, on whatever support `df` is."""
    d = df.copy()
    d["ebin"] = pd.qcut(d.Ebar, N_BINS, labels=False, duplicates="drop")
    nb = int(d.ebin.nunique())
    rows = []
    for c in SCOLS:
        perq, mq, sq, nq = within_slice_rho(d, c, "Ebar", qcol)
        perb, mb, sb, nbn = within_slice_rho(d, c, "breadth", "ebin")
        need_q, need_b = need(nq), need(nbn)
        is_ne = (abs(mq) >= BAR_RHO) and (sq >= need_q)
        is_br = (abs(mb) >= BAR_RHO) and (sb >= need_b)
        # labelled sensitivity only - never the headline
        is_ne2 = (abs(mq) >= BAR_RHO) and (sq >= max(2, need_q - 1))
        is_br2 = (abs(mb) >= BAR_RHO) and (sb >= max(2, need_b - 1))
        cls = "JOINT" if (is_ne and is_br) else "n_elig" if is_ne else "breadth" if is_br else "NULL"
        cls2 = "JOINT" if (is_ne2 and is_br2) else "n_elig" if is_ne2 else "breadth" if is_br2 else "NULL"
        b_br, b_k, r2 = rank_ols2(d[c], np.log(d.breadth), np.log(d.k))
        rows.append(dict(support=tag, stat=c, label=SLABEL[c], n_panels=len(d),
                         k_min=d.k.min(), k_max=d.k.max(), k_span=d.k.max() / d.k.min(),
                         uncond_rho_breadth=spearman(d[c], d.breadth),
                         uncond_rho_Ebar=spearman(d[c], d.Ebar),
                         uncond_rho_k=spearman(d[c], d.k),
                         withinq_rho_Ebar=mq, withinq_signlevels=f"{sq}/{nq}", need_q=need_q,
                         withinE_rho_breadth=mb, withinE_signlevels=f"{sb}/{nbn}", need_b=need_b,
                         partial_Ebar_given_breadth=partial_spearman(d[c], d.Ebar, d.breadth),
                         partial_breadth_given_Ebar=partial_spearman(d[c], d.breadth, d.Ebar),
                         beta_logbreadth=b_br, beta_logk=b_k, R2=r2,
                         beta_reading=beta_reading(b_br, b_k),
                         is_nelig=is_ne, is_breadth=is_br, verdict=cls, verdict_sens2=cls2,
                         **{f"q{q:.2f}": perq.get(q, np.nan) for q in QS},
                         **{f"ebin{i}": perb.get(i, np.nan) for i in range(nb)}))
    return pd.DataFrame(rows)


def walkforward(bmix, label):
    SELECTORS = {"EBAR-MAX": ("Ebar_IS", True), "EBAR-MIN": ("Ebar_IS", False),
                 "BREADTH-MAX": ("breadth_IS", True), "BREADTH-MIN": ("breadth_IS", False),
                 "IS-SHARPE-MAX": ("IS_Sharpe", True)}
    b = bmix
    wrows = []
    for n, sub in b.groupby("n"):
        anchor = sub.OOS_Sharpe.mean()
        for sel, (col, hi) in SELECTORS.items():
            pick = sub.loc[sub[col].idxmax() if hi else sub[col].idxmin()]
            wrows.append(dict(support=label, n=int(n), selector=sel, panel=pick.panel,
                              q=pick.q, k=pick.k, Ebar_IS=pick.Ebar_IS,
                              breadth_IS=pick.breadth_IS, IS_Sharpe=pick.IS_Sharpe,
                              OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                              OOS_MaxDD=pick.OOS_MaxDD, v2_OOS_S=pick.v2_OOS_S,
                              v2_OOS_CAGR=pick.v2_OOS_CAGR, v2_OOS_DD=pick.v2_OOS_DD,
                              spy_OOS_S=pick.spy_OOS_S, spy_OOS_CAGR=pick.spy_OOS_CAGR,
                              spy_OOS_DD=pick.spy_OOS_DD, anchor_OOS_S=anchor,
                              beats_anchor=bool(pick.OOS_Sharpe > anchor),
                              beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                              beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    return pd.DataFrame(wrows)


def main():
    t0all = time.time()
    P("=" * 100)
    P("IDEA 685 - extend-the-q-x-k-ladder-past-k-EQUALS-100 (lane C, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED BAR (docstring, fixed before any number below was read):")
    P(f"  |mean within-q Spearman(S, Ebar)| >= {BAR_RHO:.2f} and sign in >= ceil({SHARE:.3f}*L) "
      f"of L q-levels  -> n_elig   (L=3 here, so 3 of 3)")
    P(f"  |mean within-Ebar-bin Spearman(S, breadth)| >= {BAR_RHO:.2f} and sign in >= "
      f"ceil({SHARE:.3f}*5)=4 of 5 bins -> breadth")
    P("  both -> JOINT; neither -> NULL.  2-of-3 printed as a LABELLED SENSITIVITY only.")
    P("  THREE supports: NARROW (q>=0.5, k<=100) / WIDE (q>=0.5, k<=400) / lane B (committed).")
    P("  WIDE - NARROW isolates the k EXTENSION; NARROW - laneB isolates the q RESTRICTION.")

    src = M276.build_sources()
    pxs, pxb = src["pxs"], src["pxb"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    s_stk, b_stk = src["s_stk"], src["b_stk"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days); "
      f"pools: SMALL {len(s_stk)}, BSTK {len(b_stk)}")

    built, from_B = build_ladder(s_stk, b_stk)
    P(f"\n{len(built)} panels built ({len(from_B)} replayed from lane B at k<={NARROW_K}, "
      f"{len(built) - len(from_B)} new at k>{NARROW_K})")
    cells = sorted({(q, k) for q, k, *_ in built})
    P(f"  {len(cells)} feasible (q,k) cells: " + ", ".join(f"({q:.2f},{k})" for q, k in cells))

    P("\n--- GATE 2: the feasible envelope, on this run's own construction ---")
    bad = []
    for q, k, d, sc, lc in built:
        if len(sc) > len(s_stk) or len(lc) > len(b_stk): bad.append((q, k, d, "pool overflow"))
        if len(set(sc)) != len(sc) or len(set(lc)) != len(lc): bad.append((q, k, d, "dup column"))
        if len(sc) + len(lc) != k: bad.append((q, k, d, "width mismatch"))
        if abs(len(sc) - round(q * k)) > 0: bad.append((q, k, d, "cap mix mismatch"))
    assert not bad, f"GATE 2 FAILED: {bad[:5]}"
    P(f"  GATE 2 PASS - all {len(built)} panels: q*k <= {len(s_stk)}, (1-q)*k <= {len(b_stk)}, "
      "exact width, exact cap mix, no duplicate columns.")
    P(f"  k span on this ladder: {min(KS)}..{max(k for _, k in cells)} = "
      f"{max(k for _, k in cells) / min(KS):.1f}x   (lane B 2.5x; the record's own 35..439 = 12.5x)")

    # ------------------------------------------------------------ run every panel
    P("\n" + "=" * 100)
    P("RUNNING THE LADDER")
    P("=" * 100)
    brows, srows = [], []
    for i, (q, k, d, sc, lc) in enumerate(built):
        cols = sc + lc
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[cols + ["SPY"]]
        t0 = time.time()
        do_panel(f"MIX q={q:.2f} k={k} d{d}", "mix", q, d, px, cols, brows, srows,
                 NS_LAD, {"lad": NS_LAD})
        P(f"  [{i + 1:3d}/{len(built)}] q={q:.2f} k={k:3d} d{d}  {time.time() - t0:5.1f}s "
          f"(elapsed {time.time() - t0all:6.1f}s)"
          + ("  [lane B replay]" if (q, k, d) in from_B else "  [NEW]"))

    stats = pd.DataFrame(srows); books = pd.DataFrame(brows)
    stats.to_csv(f"{OUT}.stats.csv", index=False)
    books.to_csv(f"{OUT}.books.csv", index=False)
    mix = stats[stats.ladder == "lad"].copy()
    mix[["panel", "q", "k", "draw", "Ebar", "Emed", "breadth", "Ebar_IS", "breadth_IS",
         "selectivity20"]].to_csv(f"{OUT}.panels.csv", index=False)

    # ------------------------------------------------------------ GATE 0
    P("\n" + "=" * 100)
    P("GATE 0 - REPRODUCTION: lane B's committed rows, re-measured from its replayed draws")
    P("=" * 100)
    refp = pd.read_csv(f"{P525}.panels.csv")
    refp = refp[refp.kind == "mix"].set_index("panel")
    refs = pd.read_csv(f"{P525}.stats.csv")
    refs = refs[(refs.kind == "mix") & (refs.ladder == "lad")].set_index("panel")
    mine = mix.set_index("panel")
    over = [p for p in mine.index if p in refp.index]
    P(f"  overlap with lane B's committed ladder: {len(over)} panels "
      f"(expected {len(from_B)})")
    assert len(over) == len(from_B), f"GATE 0 FAILED: overlap {len(over)} != {len(from_B)}"
    EXACT = ["Ebar", "breadth", "Emed", "Ebar_IS", "breadth_IS"]
    worst = {}
    for c in EXACT:
        dd = (refp.loc[over, c] - mine.loc[over, c]).abs(); worst[c] = float(dd.max())
        P(f"  panel measure {c:12s} max |delta| {dd.max():.3e}  moving > 1e-9: "
          f"{int((dd > 1e-9).sum())}/{len(dd)}")
    SGATE = SCOLS + ["EW_Sharpe", "EW_OOS_Sharpe", "ADAPT_Sharpe", "best_prem"]
    for c in SGATE:
        dd = (refs.loc[over, c] - mine.loc[over, c]).abs(); worst[c] = float(dd.max())
        P(f"  statistic     {c:12s} max |delta| {dd.max():.3e}  moving > 1e-9: "
          f"{int((dd > 1e-9).sum())}/{len(dd)}")
    for c in EXACT + SGATE:
        assert worst[c] < 1e-9, f"GATE 0 FAILED on {c}: {worst[c]:.3e}"
    P(f"  GATE 0 PASS - {len(over)} panels x {len(EXACT + SGATE)} quantities reproduce at "
      f"MACHINE PRECISION (worst {max(worst.values()):.3e}).")
    P("  Both pools (prices_broad.csv, prices_small.csv) are cached weekly and were not")
    P("  restated between the two runs, and SPY never enters a gate matrix or a CAND/EWall")
    P("  book - so the SPY-dependent columns are reported separately, not asserted:")
    for c in ["spy_OOS_S", "v2_OOS_S", "v2_OOS_CAGR"]:
        dd = (refs.loc[over, c] - mine.loc[over, c]).abs()
        P(f"    {c:12s} max |delta| {dd.max():.3e}  (data/prices.csv drift, idea 513)")

    P("\n--- GATE 1: the k-IDENTITY on this run's own construction ---")
    dident = (mix.k * mix.breadth - mix.Ebar).abs()
    P(f"  max |k * breadth - Ebar| over all {len(mix)} panels: {dident.max():.3e}")
    assert float(dident.max()) < 1e-9, f"GATE 1 FAILED: {dident.max():.3e}"
    P("  GATE 1 PASS.")

    # ------------------------------------------------------------ the ladder itself
    P("\n" + "=" * 100)
    P("THE EXTENDED LADDER")
    P("=" * 100)
    piv = mix.pivot_table(index="q", columns="k", values=["breadth", "Ebar"], aggfunc="mean")
    P(piv.to_string(float_format=lambda x: f"{x:8.3f}"))
    P(f"\n  breadth range {mix.breadth.min():.4f} .. {mix.breadth.max():.4f} "
      f"({mix.breadth.max() / mix.breadth.min():.2f}x);  "
      f"Ebar range {mix.Ebar.min():.2f} .. {mix.Ebar.max():.2f} "
      f"({mix.Ebar.max() / mix.Ebar.min():.2f}x)")
    nar = mix[mix.k <= NARROW_K]
    P(f"  NARROW (k<={NARROW_K}) Ebar range {nar.Ebar.min():.2f} .. {nar.Ebar.max():.2f} "
      f"({nar.Ebar.max() / nar.Ebar.min():.2f}x)  -> the k extension buys "
      f"{(mix.Ebar.max() / mix.Ebar.min()) / (nar.Ebar.max() / nar.Ebar.min()):.2f}x more n_elig span")
    P(f"  Spearman(breadth, Ebar) WIDE {spearman(mix.breadth, mix.Ebar):+.4f}   "
      f"NARROW {spearman(nar.breadth, nar.Ebar):+.4f}   "
      f"(idea 286's fixed-k ladder: +0.99999)")
    P(f"  Spearman(q, breadth) {spearman(mix.q, mix.breadth):+.4f}   "
      f"Spearman(k, Ebar) {spearman(mix.k, mix.Ebar):+.4f}   "
      f"Spearman(k, breadth) {spearman(mix.k, mix.breadth):+.4f}")
    P("\n  breadth by k, within each q (is breadth still ~flat in k once k reaches 400?):")
    P(mix.pivot_table(index="k", columns="q", values="breadth", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    wq = mix.groupby("q").breadth.std()
    P(f"  within-q sd of breadth: " + ", ".join(f"q={q:.2f} {v:.4f}" for q, v in wq.items())
      + f"   across-q sd of the q-means: {mix.groupby('q').breadth.mean().std():.4f}")

    P("\n  the five statistics by k, pooled over q (the raw k arm, 10x of width):")
    P(mix.groupby("k")[SCOLS].mean().to_string(float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------------------------------------ classification x3
    P("\n" + "=" * 100)
    P("THE CLASSIFICATION ON THREE SUPPORTS")
    P("=" * 100)
    decW = classify(mix, tag="WIDE q>=0.5 k<=400")
    decN = classify(nar, tag="NARROW q>=0.5 k<=100")
    decB = pd.read_csv(f"{P525}.decomp.csv").set_index("stat")
    dec = pd.concat([decN, decW], ignore_index=True)
    dec.to_csv(f"{OUT}.decomp.csv", index=False)

    for lbl, dcf in [("NARROW  (q>=0.5, k<=100)  - lane B's panels, matched control", decN),
                     ("WIDE    (q>=0.5, k<=400)  - THE IDEA 685 READING", decW)]:
        P(f"\n--- {lbl} ---")
        P(dcf[["stat", "withinq_rho_Ebar", "withinq_signlevels", "withinE_rho_breadth",
               "withinE_signlevels", "verdict", "beta_logbreadth", "beta_logk", "R2",
               "beta_reading", "verdict_sens2"]]
          .to_string(index=False, float_format=lambda x: f"{x:+.3f}"))

    P("\n" + "-" * 100)
    P("HEAD TO HEAD - the three supports side by side (verdict / beta_logbreadth / beta_logk)")
    P("-" * 100)
    hrows = []
    for c in SCOLS:
        b = decB.loc[c]; n_ = decN[decN.stat == c].iloc[0]; w = decW[decW.stat == c].iloc[0]
        hrows.append(dict(stat=SLABEL[c],
                          B_verdict=b.verdict, B_bbr=b.beta_logbreadth, B_bk=b.beta_logk,
                          N_verdict=n_.verdict, N_bbr=n_.beta_logbreadth, N_bk=n_.beta_logk,
                          W_verdict=w.verdict, W_bbr=w.beta_logbreadth, W_bk=w.beta_logk,
                          B_read=b.beta_reading, N_read=n_.beta_reading, W_read=w.beta_reading,
                          flip_qrestrict=b.verdict != n_.verdict,
                          flip_kextend=n_.verdict != w.verdict,
                          read_flip_kextend=n_.beta_reading != w.beta_reading,
                          d_bk_kextend=w.beta_logk - n_.beta_logk,
                          d_bbr_kextend=w.beta_logbreadth - n_.beta_logbreadth))
    hh = pd.DataFrame(hrows)
    P(hh[["stat", "B_verdict", "N_verdict", "W_verdict", "flip_qrestrict", "flip_kextend"]]
      .to_string(index=False))
    P("")
    P(hh[["stat", "B_bbr", "B_bk", "N_bbr", "N_bk", "W_bbr", "W_bk", "d_bbr_kextend",
          "d_bk_kextend"]].to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("")
    P(hh[["stat", "B_read", "N_read", "W_read", "read_flip_kextend"]].to_string(index=False))

    nk = int(hh.flip_kextend.sum()); nq = int(hh.flip_qrestrict.sum())
    nrk = int(hh.read_flip_kextend.sum())
    P(f"\nTHE ANSWER IDEA 685 ASKED FOR:")
    P(f"  extending k 2.5x -> 10.0x on MATCHED q support flips {nk} of {len(SCOLS)} "
      f"pre-registered verdicts and {nrk} of {len(SCOLS)} beta readings.")
    P(f"  restricting q to >= 0.5 at matched k flips {nq} of {len(SCOLS)} verdicts against "
      "lane B's published reading (this is the ENVELOPE's cost, not the k arm's).")
    P(f"  max |change in beta_logk| from the k extension: "
      f"{hh.d_bk_kextend.abs().max():.3f}  (on {hh.loc[hh.d_bk_kextend.abs().idxmax(), 'stat']})")
    P(f"  max |change in beta_logbreadth|:                "
      f"{hh.d_bbr_kextend.abs().max():.3f}  (on {hh.loc[hh.d_bbr_kextend.abs().idxmax(), 'stat']})")
    s2W = decW[decW.stat == "S2_overlap"].iloc[0]; s2N = decN[decN.stat == "S2_overlap"].iloc[0]
    P(f"\n  THE CLAIM UNDER TEST - S2 (idea 153's overlap), lane B's one RAW-WIDTH claim:")
    P(f"    lane B  (k<=100, all q): beta_logbreadth {decB.loc['S2_overlap'].beta_logbreadth:+.3f} "
      f" beta_logk {decB.loc['S2_overlap'].beta_logk:+.3f}  -> {decB.loc['S2_overlap'].beta_reading}")
    P(f"    NARROW  (k<=100, q>=.5): beta_logbreadth {s2N.beta_logbreadth:+.3f}  "
      f"beta_logk {s2N.beta_logk:+.3f}  -> {s2N.beta_reading}")
    P(f"    WIDE    (k<=400, q>=.5): beta_logbreadth {s2W.beta_logbreadth:+.3f}  "
      f"beta_logk {s2W.beta_logk:+.3f}  -> {s2W.beta_reading}")
    P("    raw S2 level by k (pooled over q), the extrapolation lane B could not see:")
    P("      " + ", ".join(f"k={int(k)} {v:.4f}" for k, v in
                           mix.groupby('k').S2_overlap.mean().items()))

    P("\n  per-q within-slice Spearman(S, Ebar), NARROW vs WIDE (the q-side of the bar):")
    for c in SCOLS:
        n_ = decN[decN.stat == c].iloc[0]; w = decW[decW.stat == c].iloc[0]
        P(f"    {c:20s} NARROW " + " ".join(f"q{q:.2f} {n_[f'q{q:.2f}']:+.3f}" for q in QS)
          + f" | mean {n_.withinq_rho_Ebar:+.3f} {n_.withinq_signlevels}")
        P(f"    {'':20s} WIDE   " + " ".join(f"q{q:.2f} {w[f'q{q:.2f}']:+.3f}" for q in QS)
          + f" | mean {w.withinq_rho_Ebar:+.3f} {w.withinq_signlevels}")

    nW = int(decW.is_nelig.sum()); brW = int(decW.is_breadth.sum())
    P(f"\n  THE COUNT, re-read at k<=400: {nW} of {len(SCOLS)} statistics are n_elig "
      f"statistics ({int((decW.is_nelig & decW.is_breadth).sum())} JOINT), "
      f"{brW - int((decW.is_nelig & decW.is_breadth).sum())} breadth-only, "
      f"{int((~decW.is_nelig & ~decW.is_breadth).sum())} NULL.")
    P(f"  lane B's published count at k<=100 was "
      f"{int(decB.is_nelig.sum())} of {len(SCOLS)}.")
    P(f"  SENSITIVITY (2-of-3, NOT the headline): WIDE verdicts "
      f"{decW.verdict_sens2.value_counts().to_dict()} vs headline "
      f"{decW.verdict.value_counts().to_dict()}")

    # ------------------------------------------------------------ KEEP paths
    P("\n" + "=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4, both, 10 bps, every arm row)")
    P("=" * 100)
    bm = books.copy()
    P(f"  arm rows: {len(bm)} ({len(NS_LAD)} CAND + EWall on {len(built)} panels)")
    P(f"  4a (beat RULES v2 on the same panel): {int(bm.pass4a.sum())}/{len(bm)} "
      f"({bm.pass4a.mean():.3%})")
    P(f"  4b (capital-worthy vs SPY):           {int(bm.pass4b.sum())}/{len(bm)} "
      f"({bm.pass4b.mean():.3%})")
    P("\n  4a / 4b pass rate by k (the new wide panels are the last two rows):")
    byk = bm.groupby("k").agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                              p4b=("pass4b", "sum"), Ebar=("Ebar", "mean"),
                              breadth=("breadth", "mean"))
    byk["r4a"] = byk.p4a / byk.rows; byk["r4b"] = byk.p4b / byk.rows
    P(byk.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  4a / 4b pass rate by q:")
    byq = bm.groupby("q").agg(rows=("pass4a", "size"), p4a=("pass4a", "sum"),
                              p4b=("pass4b", "sum"))
    P(byq.to_string())
    if bm.pass4b.any():
        P(f"  4b passers by arm: {bm[bm.pass4b].arm.value_counts().to_dict()}")
        P(f"  4b passers: Ebar {bm[bm.pass4b].Ebar.mean():.1f} vs {bm[~bm.pass4b].Ebar.mean():.1f}; "
          f"breadth {bm[bm.pass4b].breadth.mean():.4f} vs {bm[~bm.pass4b].breadth.mean():.4f}; "
          f"k {bm[bm.pass4b].k.mean():.1f} vs {bm[~bm.pass4b].k.mean():.1f}")
    P("  NOTE: no arm here is a new BOOK - CAND-n and EWall are the record's existing books")
    P("  re-run on re-drawn panels.  A pass is a statement about the panel, not a candidate.")

    # ------------------------------------------------------------ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - properties on 2010..2016, read once on 2017..2026")
    P("=" * 100)
    bmix = books[books.n.notna()].copy()
    # books already carries panel, q, k, Ebar, breadth and the FULL-sample benchmark columns;
    # the IS properties and the OOS benchmark legs live on the per-panel stats rows, so attach
    # exactly those here (panel is the join key, one stats row per panel)
    props = mix.set_index("panel")[["Ebar_IS", "breadth_IS", "spy_OOS_CAGR", "spy_OOS_DD",
                                    "v2_OOS_CAGR", "v2_OOS_DD"]]
    assert not (set(props.columns) & set(bmix.columns)), "join would collide"
    bmix = bmix.join(props, on="panel")
    wfN = walkforward(bmix[bmix.k <= NARROW_K], "NARROW k<=100")
    wfW = walkforward(bmix, "WIDE k<=400")
    wf = pd.concat([wfN, wfW], ignore_index=True)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    for lbl, w in [("NARROW k<=100 (lane B's choice set)", wfN), ("WIDE k<=400 (idea 685's)", wfW)]:
        P(f"\n--- {lbl} ---")
        P(w[["n", "selector", "panel", "q", "k", "Ebar_IS", "breadth_IS", "IS_Sharpe",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "anchor_OOS_S", "v2_OOS_S", "spy_OOS_S",
             "beats_anchor", "beats_v2", "beats_spy"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        agg = w.groupby("selector").agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                        OOS_CAGR=("OOS_CAGR", "mean"),
                                        OOS_MaxDD=("OOS_MaxDD", "mean"),
                                        beats_anchor=("beats_anchor", "sum"),
                                        beats_v2=("beats_v2", "sum"),
                                        beats_spy=("beats_spy", "sum"))
        agg["of"] = len(NS_LAD)
        P("  pooled over the 5 book sizes:")
        P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\n  benchmarks on the WIDE ladder: SPY OOS Sharpe {bmix.spy_OOS_S.mean():.4f} "
      f"(CAGR {bmix.spy_OOS_CAGR.mean():.4f}, MaxDD {bmix.spy_OOS_DD.mean():.4f});  "
      f"RULES v2 OOS Sharpe {bmix.v2_OOS_S.mean():.4f} "
      f"(CAGR {bmix.v2_OOS_CAGR.mean():.4f}, MaxDD {bmix.v2_OOS_DD.mean():.4f})")
    P(f"  do-nothing anchor (mean OOS Sharpe over the choice set, per n): NARROW "
      + ", ".join(f"n={int(n)} {v:.4f}" for n, v in
                  bmix[bmix.k <= NARROW_K].groupby('n').OOS_Sharpe.mean().items()))
    P(f"  {'':63s} WIDE   "
      + ", ".join(f"n={int(n)} {v:.4f}" for n, v in bmix.groupby('n').OOS_Sharpe.mean().items()))

    P("\n  DOES A 10x CHOICE SET CHANGE THE PICK?  (per selector, over the 5 book sizes)")
    crows = []
    for sel in wfN.selector.unique():
        a = wfN[wfN.selector == sel].set_index("n"); b = wfW[wfW.selector == sel].set_index("n")
        same = int((a.panel == b.panel.reindex(a.index)).sum())
        crows.append(dict(selector=sel, same_panel=f"{same}/{len(a)}",
                          narrow_k=sorted(a.k.unique().tolist()),
                          wide_k=sorted(b.k.unique().tolist()),
                          narrow_OOS_S=a.OOS_Sharpe.mean(), wide_OOS_S=b.OOS_Sharpe.mean(),
                          d_OOS_S=b.OOS_Sharpe.mean() - a.OOS_Sharpe.mean(),
                          narrow_OOS_DD=a.OOS_MaxDD.mean(), wide_OOS_DD=b.OOS_MaxDD.mean(),
                          wide_beats_spy=f"{int(b.beats_spy.sum())}/{len(b)}",
                          narrow_beats_spy=f"{int(a.beats_spy.sum())}/{len(a)}",
                          wide_beats_v2=f"{int(b.beats_v2.sum())}/{len(b)}",
                          narrow_beats_v2=f"{int(a.beats_v2.sum())}/{len(a)}"))
    cmp_ = pd.DataFrame(crows)
    P(cmp_.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  does the IS property PREDICT OOS at all, within book size?")
    for lbl, col in [("Ebar_IS", "Ebar_IS"), ("breadth_IS", "breadth_IS")]:
        bb = bmix
        per, m_, s_, n_ = within_slice_rho(bb, "OOS_Sharpe", col, "n")
        P(f"    WIDE   Spearman(IS {lbl:11s}, OOS Sharpe): "
          + ", ".join(f"n={int(k)} {v:+.3f}" for k, v in sorted(per.items())) + f"   mean {m_:+.3f}")
        bn_ = bb[bb.k <= NARROW_K]
        per, m_, s_, n_ = within_slice_rho(bn_, "OOS_Sharpe", col, "n")
        P(f"    NARROW Spearman(IS {lbl:11s}, OOS Sharpe): "
          + ", ".join(f"n={int(k)} {v:+.3f}" for k, v in sorted(per.items())) + f"   mean {m_:+.3f}")

    P("\n" + "=" * 100)
    P(f"done in {time.time() - t0all:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dec, hh, stats, books, wf


if __name__ == "__main__":
    main()
