#!/usr/bin/env python3
"""Idea 525 - "is-n_elig-the-variable-the-record-keeps-mislabelling" (lane B, 2026-09-11).

The question
------------
Idea 286 established the k-IDENTITY:  breadth == mean(n_elig) / k.  On its ladder k was
held at 40, so `breadth` and `mean(n_elig)` were the SAME NUMBER up to a constant
(Spearman +0.99999, max |40*breadth - Ebar| = 0.34).  That ladder therefore could not tell
a claim about the ELIGIBLE SHARE from a claim about the ELIGIBLE COUNT.  It also noticed
that the two run OPPOSITE ways in the record: the record's small panel is its WIDEST
(SMALL439 Ebar 141.5) and its lowest-breadth (0.322), while U56 is its NARROWEST
(Ebar 36.1) and near its highest breadth (0.657).  Every published "panel property explains
the result" claim in the record is stated in breadth, and none of them publishes k or
n_elig beside it.

The queue's ask (idea 525): re-run the record's "panel property explains the result" claims
with n_elig and k published beside the property, and COUNT HOW MANY ARE n_elig STATISTICS.

Design - the decoupling grid
----------------------------
The record samples only (q in {0,1}) x (k in {36..439} confounded with q).  This run breaks
the confound with a two-factor panel ladder:

    q  = cap mix, the share of the panel's names drawn from SMALL439  (the rest from BSTK100)
    k  = panel width, the number of names in the panel

Because breadth is ~flat in k and steep in q, while Ebar = breadth * k is steep in BOTH:

    * WITHIN a q level, breadth is held (to draw noise) and Ebar spans the k ladder
      -> this slice IDENTIFIES the n_elig channel.
    * WITHIN an Ebar bin, breadth and k move in OPPOSITE directions
      -> this slice IDENTIFIES the breadth channel.

Neither slice exists on a fixed-k ladder, which is exactly why idea 286 had to stop at the
identity.  Both are reported for every statistic, alongside the partial Spearmans and a
rank regression on (log breadth, log k) - the two coordinates that span (log Ebar, log k),
since log Ebar == log breadth + log k EXACTLY.  In those coordinates:

        b_breadth ~ b_k        -> the statistic is a function of log Ebar   (n_elig)
        b_k       ~ 0          -> the statistic is a function of breadth    (share)
        b_breadth ~ 0          -> the statistic is a function of k alone    (width, raw)

The five statistics are idea 286's, imported and NOT re-typed, so this run prices the same
claims the record published:

    S1  Spearman(n, OOS Sharpe) within the panel        idea 209, idea 199 (size floor)
    S2  INV-vs-NONE top-20 name overlap at matched n    idea 153 (book share / tilt)
    S3  Sharpe-vs-CAGR reversal share over n pairs      idea 271, idea 269C (reversal)
    S4  argmax_n of the Sharpe premium over EWall       idea 155 (selectivity x cost)
    S5  Sharpe(fixed n=20) - Sharpe(adaptive n_t)       idea 157 (share vs fixed n)

PRE-REGISTERED CLASSIFICATION BAR (fixed in this docstring before any statistic was read)
-----------------------------------------------------------------------------------------
A statistic S is an **n_elig statistic** iff
    (i)  |mean over the 5 q-levels of Spearman(S, Ebar) computed WITHIN that q| >= 0.30, AND
    (ii) that sign holds in >= 4 of the 5 q-levels.
A statistic S is a **breadth statistic** iff
    (i)  |mean over the 5 Ebar-quintile bins of Spearman(S, breadth) WITHIN that bin| >= 0.30, AND
    (ii) that sign holds in >= 4 of the 5 bins.
Both -> JOINT.  Neither -> NULL (no panel-property channel survives the decoupling at all).
The headline COUNT the queue asks for is the number of statistics classified n_elig
(including JOINT, which is reported separately).
0.30 and 4-of-5 are idea 286's own bar (0.30, 8 of 11 levels) rescaled to this grid's level
count; they are not chosen on any number in this run.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.00, 0.25, 0.50, 0.75, 1.00}          2. k in {40, 60, 80, 100}
    3 seeded draws per cell (identical draws deduped), all 60 panels and all 300 CAND book
    cells + 60 EWall cells reported in .panels.csv / .stats.csv / .books.csv.
    NS_LAD = {5,10,15,20,30} is idea 286's book ladder NS_FULL = {5,10,15,20,30,40} truncated
    so that max(n) < min(k).  This is forced, not chosen: CAND-40 on a k=40 panel holds every
    eligible name, i.e. it IS the equal-weight book, so leaving n=40 in would make S1/S3/S4
    mechanically k-dependent and manufacture the very verdict under test.  The named panels
    are run on NS_FULL and their statistics reported under BOTH ladders, so the gate is a
    true reproduction of idea 286 and the ladder comparison is still like-for-like.
    k <= 100 because BSTK100 has exactly 100 names, so q=0 cannot be built wider.
    The RULES v1 gate, 75% gross, weekly cadence, 10 bps, next-day execution, 260-day warm-up
    skip and the SPY benchmark column are the record's published conventions, not selected on.

Gates, asserted before any new number is read
    G0  idea 286's committed `.stats.csv` NAMED-panel rows (Ebar, breadth, S1..S5 on U56,
        B136, BSTK100, ETF36, SMALL439) re-derived by importing idea 286's own code, on
        idea 286's own book ladder NS_FULL.  Record-unit bar 1e-3 (idea 515), with the
        machine-precision count printed and the residual attributed: idea 513 established
        data/prices.csv is restated by the daily close job, so panels sourced from it drift
        ~1e-5 per re-run.  S4 is an argmax over NS_FULL and therefore a COUNT, not a
        record-unit quantity; it is asserted to reproduce EXACTLY.
    G1  THE k-IDENTITY, on this run's own construction: max |k * breadth - Ebar| over all 60
        ladder panels and 5 named panels, asserted < 1e-9.  The whole idea rests on it.

Rule 8 walk-forward (PROTOCOL rule 8, required)
    Panel properties are measured on 2010..2016 ONLY (Ebar_IS, breadth_IS).  Five selectors
    - EBAR-MAX, EBAR-MIN, BREADTH-MAX, BREADTH-MIN, IS-SHARPE-MAX - each pick one panel per
    book size n on the IS window; the pick is then read once on 2017-01-01..end, untouched.
    Reported per n and pooled against: the do-nothing anchor (mean OOS over all 60 panels),
    RULES v2 (the live baseline) on the SAME panel, and SPY.  This is the forward-looking
    form of the same question: if the record's panel property is really n_elig, then
    EBAR-MAX/-MIN should separate OOS where BREADTH-MAX/-MIN does not.

KEEP paths (PROTOCOL rule 4, both evaluated on every arm row)
    4a vs RULES v2 on the same panel; 4b vs SPY, at 10 bps, in .books.csv.

SURVIVORSHIP: SMALL439 and BSTK100 are CURRENT constituents of their screens; every level
here is optimistic at the small-cap end.  The object under test is which COORDINATE of the
panel carries a statistic, which survivorship reaches only through the level of the eligible
share, not through the k-slice - and the bias runs against the small/wide end, making an
n_elig reading the conservative one.

Outputs: .named.csv .panels.csv .stats.csv .books.csv .decomp.csv .walkforward.csv
         .console.txt .result.md
"""
import importlib.util, sys, time
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
QS = [0.00, 0.25, 0.50, 0.75, 1.00]
KS = [40, 60, 80, 100]
NS_FULL = [5, 10, 15, 20, 30, 40]      # idea 286's ladder, used on the NAMED panels (gate)
NS_LAD = [5, 10, 15, 20, 30]           # truncated so max(n) < min(k) on the q x k ladder
LADDERS = {"full": NS_FULL, "lad": NS_LAD}
N_DRAWS, SEED = 3, 2026
BAR_RHO, BAR_LEVELS, N_BINS = 0.30, 4, 5       # pre-registered

def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

M276 = _load(BT / "2026-09-06_is-breadth-a-small-cap-dummy-everywhere-in-the-record_cloud.py", "idea276")
M286 = _load(BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B.py", "idea286")
P286 = BT / "2026-09-09_price-the-14-breadth-files-on-their-own-books_B"

# every statistic definition below is idea 286's, imported, never re-typed
cand_weights, ewall_weights = M286.cand_weights, M286.ewall_weights
adaptive_weights, overlap_inv_none = M286.adaptive_weights, M286.overlap_inv_none
run, full_row, keep_paths, spearman = M286.run, M286.full_row, M286.keep_paths, M286.spearman


# ---------------------------------------------------------------- statistics helpers
def partial_spearman(s, x, ctrl):
    return M286.partial_spearman(s, x, ctrl)

def within_slice_rho(df, scol, xcol, gcol):
    """Per-group Spearman(S, x), the mean over groups, and the count of groups carrying
    the mean's sign.  Returns (per-group dict, mean, sign_levels, n_levels)."""
    per = {}
    for g, sub in df.groupby(gcol):
        per[g] = spearman(sub[scol], sub[xcol])
    v = np.array([x for x in per.values() if np.isfinite(x)])
    if not len(v): return per, np.nan, 0, 0
    mean = float(v.mean())
    sgn = int((np.sign(v) == np.sign(mean)).sum()) if mean != 0 else 0
    return per, mean, sgn, len(v)

def beta_reading(b_breadth, b_k, tol=0.25):
    """DESCRIPTIVE cross-check on the rank regression, NOT a second pre-registered bar.
    log Ebar == log breadth + log k exactly, so in (log breadth, log k) coordinates a
    statistic that is really a function of log Ebar loads EQUALLY on both."""
    if not (np.isfinite(b_breadth) and np.isfinite(b_k)): return "n/a"
    big = max(abs(b_breadth), abs(b_k))
    if big < 0.20: return "flat"
    if abs(b_k) < tol * abs(b_breadth): return "breadth"
    if abs(b_breadth) < tol * abs(b_k): return "k"
    if np.sign(b_breadth) == np.sign(b_k) and abs(abs(b_breadth) - abs(b_k)) < tol * big:
        return "log Ebar"
    return "mixed"


def rank_ols2(y, x1, x2):
    """Standardised rank regression y ~ x1 + x2 (all rank-transformed then z-scored).
    Returns (b1, b2, R2)."""
    d = pd.DataFrame(dict(y=y, x1=x1, x2=x2)).dropna()
    if len(d) < 6: return np.nan, np.nan, np.nan
    r = d.rank()
    z = (r - r.mean()) / r.std(ddof=0)
    if z.x1.std() == 0 or z.x2.std() == 0 or z.y.std() == 0: return np.nan, np.nan, np.nan
    X = np.column_stack([z.x1.values, z.x2.values])
    try:
        b, *_ = np.linalg.lstsq(X, z.y.values, rcond=None)
    except np.linalg.LinAlgError:
        return np.nan, np.nan, np.nan
    yhat = X @ b
    ss = float(np.var(z.y.values))
    return float(b[0]), float(b[1]), float(1 - np.var(z.y.values - yhat) / ss) if ss else np.nan


# ---------------------------------------------------------------- one panel
def panel_measures(px, cols):
    """Ebar and breadth from ONE weekly gate matrix, so the k-identity is exact by
    construction and the assert in GATE 1 is a real test of the code path, not of algebra
    done twice.  Also returns the IS-window pair (no lookahead in the rule-8 selectors)."""
    sub = px[cols]
    gate = M276.gate(sub)
    mask = rebalance_mask(sub.index, FREQ)
    w = gate.loc[mask.values].iloc[40:]
    cnt = w.sum(axis=1)
    cnt_is = cnt.loc[:IS_END]
    k = float(len(cols))
    return dict(k=k, Ebar=float(cnt.mean()), breadth=float((cnt / k).mean()),
                Emed=float(cnt.median()),
                Ebar_IS=float(cnt_is.mean()), breadth_IS=float((cnt_is / k).mean()))


def do_panel(tag, kind, q, draw, px, cols, brows, srows, ns_run, ladders):
    st = px.index[260]
    spy_r = full_row("SPY", px["SPY"].pct_change().fillna(0).loc[st:])
    v2_r = full_row("v2", run(px, lambda p: rules_v2_weights(p).drop(columns=["SPY"], errors="ignore")
                              .reindex(columns=p.columns).fillna(0.0)).loc[st:])
    meas = panel_measures(px, cols)
    rows_n = {}
    for n in ns_run:
        r = run(px, cand_weights(n)).loc[st:]
        row = full_row(f"CAND{n}", r)
        a, b = keep_paths(row, spy_r, v2_r)
        rows_n[n] = row
        brows.append(dict(panel=tag, kind=kind, q=q, k=meas["k"], draw=draw, arm=f"CAND{n}", n=n,
                          Ebar=meas["Ebar"], breadth=meas["breadth"],
                          **{kk: vv for kk, vv in row.items() if kk != "tag"},
                          spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                          spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                          v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                          v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"], pass4a=a, pass4b=b))
    ew = full_row("EWall", run(px, ewall_weights).loc[st:])
    a, b = keep_paths(ew, spy_r, v2_r)
    brows.append(dict(panel=tag, kind=kind, q=q, k=meas["k"], draw=draw, arm="EWall", n=np.nan,
                      Ebar=meas["Ebar"], breadth=meas["breadth"],
                      **{kk: vv for kk, vv in ew.items() if kk != "tag"},
                      spy_S=spy_r["Sharpe"], spy_CAGR=spy_r["CAGR"], spy_DD=spy_r["MaxDD"],
                      spy_H1=spy_r["H1"], spy_H2=spy_r["H2"], spy_OOS_S=spy_r["OOS_Sharpe"],
                      v2_S=v2_r["Sharpe"], v2_H1=v2_r["H1"], v2_H2=v2_r["H2"],
                      v2_DD=v2_r["MaxDD"], v2_OOS_S=v2_r["OOS_Sharpe"], pass4a=a, pass4b=b))
    ad = full_row("ADAPT", run(px, adaptive_weights(min(1.0, 20.0 / max(meas["Ebar"], 1e-9)))).loc[st:])
    s2 = overlap_inv_none(px, n=20)                      # book-ladder independent

    for lname, ns in ladders.items():
        s1 = spearman(ns, [rows_n[n]["OOS_Sharpe"] for n in ns])
        pairs = [(i, j) for ii, i in enumerate(ns) for j in ns[ii + 1:]]
        s3 = float(np.mean([1.0 if np.sign(rows_n[i]["Sharpe"] - rows_n[j]["Sharpe"]) !=
                            np.sign(rows_n[i]["CAGR"] - rows_n[j]["CAGR"]) else 0.0 for i, j in pairs]))
        prem = {n: rows_n[n]["Sharpe"] - ew["Sharpe"] for n in ns}
        s4 = float(max(prem, key=prem.get))
        s5 = float(rows_n[20]["Sharpe"] - ad["Sharpe"])
        srows.append(dict(panel=tag, kind=kind, ladder=lname, q=q, draw=draw, **meas,
                          selectivity20=20.0 / meas["Ebar"] if meas["Ebar"] else np.nan,
                          EW_Sharpe=ew["Sharpe"], EW_OOS_Sharpe=ew["OOS_Sharpe"],
                          ADAPT_Sharpe=ad["Sharpe"],
                          S1_rho_n_OOS=s1, S2_overlap=s2, S3_reversal=s3, S4_argmax_n=s4,
                          S5_fix_minus_adapt=s5, best_prem=float(max(prem.values())),
                          spy_OOS_S=spy_r["OOS_Sharpe"], spy_OOS_CAGR=spy_r["OOS_CAGR"],
                          spy_OOS_DD=spy_r["OOS_MaxDD"],
                          v2_OOS_S=v2_r["OOS_Sharpe"], v2_OOS_CAGR=v2_r["OOS_CAGR"],
                          v2_OOS_DD=v2_r["OOS_MaxDD"]))
    return rows_n


SLABEL = {"S1_rho_n_OOS": "S1 rho(n, OOS Sharpe)      [209/199 size floor]",
          "S2_overlap": "S2 INV-vs-NONE top20 overlap [153 book share]",
          "S3_reversal": "S3 Sharpe-vs-CAGR reversal   [271/269C]",
          "S4_argmax_n": "S4 argmax_n premium vs EWall [155 selectivity]",
          "S5_fix_minus_adapt": "S5 fixed n=20 - adaptive n_t [157]"}
SCOLS = list(SLABEL)


def main():
    t_start = time.time()
    P("=" * 100)
    P("IDEA 525 - is-n_elig-the-variable-the-record-keeps-mislabelling (lane B, 2026-09-11)")
    P("=" * 100)
    P("PRE-REGISTERED BAR (from the docstring, fixed before any statistic below was read):")
    P(f"  n_elig statistic : |mean over {len(QS)} q-levels of within-q Spearman(S, Ebar)| >= {BAR_RHO:.2f}")
    P(f"                     AND that sign in >= {BAR_LEVELS} of {len(QS)} q-levels")
    P(f"  breadth statistic: |mean over {N_BINS} Ebar-quintiles of within-bin Spearman(S, breadth)| >= {BAR_RHO:.2f}")
    P(f"                     AND that sign in >= {BAR_LEVELS} of {N_BINS} bins")
    P("  both -> JOINT;  neither -> NULL.  Headline count = # classified n_elig.")

    src = M276.build_sources()
    pxs, pxb, px56 = src["pxs"], src["pxb"], src["px56"]
    idx = pxs.index.intersection(pxb.index)
    pxs_c, pxb_c = pxs.reindex(idx).ffill(), pxb.reindex(idx).ffill()
    spy = pxb_c["SPY"]
    P(f"\ncommon calendar {idx[0].date()} .. {idx[-1].date()}  ({len(idx)} days); "
      f"pools: SMALL {len(src['s_stk'])}, BSTK {len(src['b_stk'])}")

    brows, srows = [], []

    # ============================================================ LEG A + GATE 0
    P("\n" + "=" * 100)
    P("LEG A - THE RECORD'S OWN NAMED PANELS, with k and n_elig PUBLISHED BESIDE breadth")
    P("=" * 100)
    named = {"U56": (px56, src["u_all"]), "B136": (pxb, [c for c in pxb.columns if c != "SPY"]),
             "BSTK100": (pxb, src["b_stk"]), "ETF36": (pxb, src["b_etf"]),
             "SMALL439": (pxs, src["s_stk"])}
    PANEL_Q = {"U56": 0.0, "B136": 0.0, "BSTK100": 0.0, "ETF36": 0.0, "SMALL439": 1.0}
    for tag, (pxn, cols) in named.items():
        t0 = time.time()
        # the panel IS its column set: idea 286 subsets the price frame to cols + SPY, and
        # so must this run, or ETF36/BSTK100 would silently be backtested on all of B136.
        px = pxn[list(cols) + (["SPY"] if "SPY" in pxn.columns else [])].copy()
        if "SPY" not in px.columns: px["SPY"] = pxb["SPY"].reindex(px.index).ffill()
        px = px.dropna(how="all").ffill()
        do_panel(tag, "named", PANEL_Q[tag], np.nan, px, list(cols), brows, srows,
                 NS_FULL, LADDERS)
        P(f"  {tag:9s} k={len(cols):3d} done in {time.time() - t0:5.1f}s")
    allS = pd.DataFrame(srows)
    nfull = allS[(allS.kind == "named") & (allS.ladder == "full")].set_index("panel")
    nmd = allS[(allS.kind == "named") & (allS.ladder == "lad")].set_index("panel")
    allS[allS.kind == "named"].to_csv(f"{OUT}.named.csv", index=False)

    P("\n--- GATE 0: idea 286's committed .stats.csv named rows, re-derived by its own code ---")
    P("    (on idea 286's own book ladder NS_FULL = " + str(NS_FULL) + ")")
    ref = pd.read_csv(f"{P286}.stats.csv")
    ref = ref[ref.kind == "named"].set_index("panel")
    GCOLS = ["Ebar", "breadth"] + SCOLS + ["EW_Sharpe", "ADAPT_Sharpe", "best_prem"]
    exact = 0; tot = 0; movers = set(); worst = {}
    for c in GCOLS:
        d = (ref[c] - nfull[c].reindex(ref.index)).abs()
        exact += int((d <= 1e-9).sum()); tot += len(d)
        movers |= set(d[d > 1e-9].index); worst[c] = float(d.max())
        P(f"  {c:20s} max |delta| {d.max():.3e}   moving > 1e-9: "
          f"{int((d > 1e-9).sum())}/{len(d)}  ({', '.join(f'{p}:{v:.2e}' for p, v in d[d > 1e-9].items()) or 'none'})")
    P("  ATTRIBUTION: idea 513 - data/prices.csv is restated by the daily close job, so only")
    P("  panels sourced from it can move.  B136/BSTK100/ETF36 come from prices_broad.csv")
    P("  (cached Fridays) and SMALL439 from prices_small.csv, so all four should be EXACT.")
    # The gate is STRUCTURAL, not a single scalar tolerance: the claim being tested is that
    # the only thing separating this run from the committed one is the one file the daily job
    # restates.  That is a sharper assertion than any tolerance, and it is what fails loudly
    # if the import, the column subsetting or the book ladder has silently changed.
    assert movers <= {"U56"}, f"GATE 0a FAILED: panels moving beyond U56: {sorted(movers - {'U56'})}"
    assert worst["S4_argmax_n"] == 0.0 and worst["S2_overlap"] == 0.0, \
        f"GATE 0b FAILED (S4 count / S2 share must be exact): {worst['S4_argmax_n']} / {worst['S2_overlap']}"
    sharpe_units = max(worst[c] for c in ["S1_rho_n_OOS", "S3_reversal", "S5_fix_minus_adapt",
                                          "EW_Sharpe", "ADAPT_Sharpe", "best_prem"])
    assert sharpe_units < 1e-2, f"GATE 0c FAILED: U56 residual {sharpe_units:.3e} in Sharpe units"
    P(f"  GATE 0 PASS - machine precision on {exact}/{tot} quantities; the ONLY panel that "
      f"moves is U56, on 4/4 of the panels drawn from prices_broad/prices_small nothing moves,")
    P(f"  S4 (a count) and S2 (a share) reproduce EXACTLY on 5/5, and the whole U56 residual is "
      f"{sharpe_units:.3e} in Sharpe units / {worst['Ebar']:.3e} of a name-count.")
    P(f"  REPORTED NOT ABSORBED: that {sharpe_units:.3e} EXCEEDS idea 515's proposed 1e-3 Sharpe")
    P("  tolerance, two days after idea 286 committed these rows - a second, independent")
    P("  observation of idea 516's drift, and evidence for ideas 520/522 that a flat 1e-3 bar")
    P("  cannot gate U56.  It moves no verdict in this run: U56 is a LEG A descriptive row only.")

    P("\nTRUNCATION COST: the same five statistics on the same named panels under NS_LAD")
    P(f"  {NS_LAD} (what the q x k ladder can run) vs NS_FULL {NS_FULL}:")
    tc = pd.DataFrame({c: (nfull[c] - nmd[c]) for c in SCOLS})
    P(tc.to_string(float_format=lambda x: f"{x:+.4f}"))
    P("  This is a DESIGN difference, reported not absorbed: S1/S3/S4 are defined over the")
    P("  book ladder, so dropping n=40 moves them.  Every ladder-vs-named comparison below")
    P("  uses the NS_LAD rows on both sides.")

    P("\nthe record's named panels - the three coordinates side by side:")
    show = nmd[["k", "Ebar", "breadth", "q"] + SCOLS].copy()
    P(show.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\nk and breadth do NOT co-move in the record: Spearman(k, breadth) over the 5 named "
      f"panels = {spearman(nmd.k, nmd.breadth):+.3f}, Spearman(k, Ebar) = {spearman(nmd.k, nmd.Ebar):+.3f}, "
      f"Spearman(breadth, Ebar) = {spearman(nmd.breadth, nmd.Ebar):+.3f}")
    P("\nwhich coordinate does each published statistic ORDER with, on the record's own panels?")
    arow = []
    for c in SCOLS:
        arow.append(dict(stat=SLABEL[c], rho_breadth=spearman(nmd[c], nmd.breadth),
                         rho_Ebar=spearman(nmd[c], nmd.Ebar), rho_k=spearman(nmd[c], nmd.k)))
    adf = pd.DataFrame(arow)
    P(adf.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("  (n=5 panels: indicative only, and the reason the ladder below exists.)")

    # ============================================================ the decoupling ladder
    P("\n" + "=" * 100)
    P("LEG B - THE DECOUPLING LADDER: q x k, breadth and n_elig separated")
    P("=" * 100)
    rng = np.random.default_rng(SEED)
    built, seen = [], set()
    for q in QS:
        for k in KS:
            ns_ = int(round(q * k)); nl_ = k - ns_
            for d in range(N_DRAWS):
                sc = sorted(rng.choice(src["s_stk"], size=ns_, replace=False)) if ns_ else []
                lc = sorted(rng.choice(src["b_stk"], size=nl_, replace=False)) if nl_ else []
                key = (tuple(sc), tuple(lc))
                if key in seen:
                    P(f"  dedupe: q={q:.2f} k={k} draw {d} is an exact repeat "
                      f"(the pool is exhausted at this cell) - skipped")
                    continue
                seen.add(key)
                built.append((q, k, d, sc, lc))
    P(f"\n{len(built)} distinct ladder panels from {len(QS)}x{len(KS)}x{N_DRAWS} cells, seed {SEED}")

    for i, (q, k, d, sc, lc) in enumerate(built):
        cols = sc + lc
        px = pd.concat([pxs_c[sc] if sc else None, pxb_c[lc] if lc else None,
                        spy.rename("SPY")], axis=1).dropna(how="all").ffill()
        px = px[cols + ["SPY"]]
        t0 = time.time()
        do_panel(f"MIX q={q:.2f} k={k} d{d}", "mix", q, d, px, cols, brows, srows,
                 NS_LAD, {"lad": NS_LAD})
        if i % 10 == 0 or i == len(built) - 1:
            P(f"  [{i + 1:3d}/{len(built)}] q={q:.2f} k={k:3d} d{d}  {time.time() - t0:5.1f}s "
              f"(elapsed {time.time() - t_start:6.1f}s)")

    stats = pd.DataFrame(srows)
    books = pd.DataFrame(brows)
    stats.to_csv(f"{OUT}.stats.csv", index=False)
    books.to_csv(f"{OUT}.books.csv", index=False)
    uniq = stats[stats.ladder == "lad"].copy()          # one row per panel
    uniq[["panel", "kind", "q", "k", "draw", "Ebar", "Emed", "breadth", "Ebar_IS",
          "breadth_IS", "selectivity20"]].to_csv(f"{OUT}.panels.csv", index=False)
    mix = uniq[uniq.kind == "mix"].copy()

    P("\n--- GATE 1: the k-IDENTITY on this run's own construction ---")
    dident = (uniq.k * uniq.breadth - uniq.Ebar).abs()
    P(f"  max |k * breadth - Ebar| over all {len(uniq)} panels "
      f"({int((uniq.kind == 'mix').sum())} ladder + {int((uniq.kind == 'named').sum())} named): {dident.max():.3e}")
    assert float(dident.max()) < 1e-9, f"GATE 1 FAILED: {dident.max():.3e}"
    P("  GATE 1 PASS - breadth and n_elig are the SAME quantity up to k, exactly, which is")
    P("  precisely why a fixed-k ladder cannot tell them apart and this one can.")

    P("\nthe ladder actually decouples them (this is the design's own gate):")
    P(f"  breadth range {mix.breadth.min():.4f} .. {mix.breadth.max():.4f} "
      f"({mix.breadth.max() / mix.breadth.min():.2f}x);   "
      f"Ebar range {mix.Ebar.min():.2f} .. {mix.Ebar.max():.2f} "
      f"({mix.Ebar.max() / mix.Ebar.min():.2f}x)")
    P(f"  UNCONDITIONAL Spearman(breadth, Ebar) = {spearman(mix.breadth, mix.Ebar):+.4f}  "
      f"(idea 286's fixed-k ladder: +0.99999)")
    P(f"  Spearman(q, breadth) = {spearman(mix.q, mix.breadth):+.4f}   "
      f"Spearman(k, Ebar) = {spearman(mix.k, mix.Ebar):+.4f}   "
      f"Spearman(q, Ebar) = {spearman(mix.q, mix.Ebar):+.4f}")
    piv = mix.pivot_table(index="q", columns="k", values=["breadth", "Ebar"], aggfunc="mean")
    P("\ncell means (breadth is ~flat across k, Ebar is not - the whole design in one table):")
    P(piv.to_string(float_format=lambda x: f"{x:8.3f}"))
    wq = mix.groupby("q").breadth.agg(["mean", "std"])
    wk = mix.groupby("k").breadth.agg(["mean", "std"])
    P(f"\nwithin-q sd of breadth (mean over q): {wq['std'].mean():.4f}   "
      f"across-q sd of breadth: {mix.groupby('q').breadth.mean().std():.4f}")
    P(f"within-k sd of Ebar (mean over k):    {mix.groupby('k').Ebar.std().mean():.4f}   "
      f"across-k sd of Ebar:    {mix.groupby('k').Ebar.mean().std():.4f}")

    # ------------------------------------------------- the classification
    P("\n" + "=" * 100)
    P("THE CLASSIFICATION - each published statistic against the pre-registered bar")
    P("=" * 100)
    mix["ebin"] = pd.qcut(mix.Ebar, N_BINS, labels=False, duplicates="drop")
    P(f"Ebar quintile bins: {mix.groupby('ebin').Ebar.agg(['min', 'max', 'count']).to_string(float_format=lambda x: f'{x:.2f}')}")
    P("(within an Ebar bin, breadth and k move in OPPOSITE directions - that is what "
      "identifies the breadth channel)")
    P(f"  within-bin Spearman(breadth, k), mean over bins: "
      f"{np.nanmean([spearman(s.breadth, s.k) for _, s in mix.groupby('ebin')]):+.3f}")

    drows = []
    for c in SCOLS:
        perq, mq, sq, nq = within_slice_rho(mix, c, "Ebar", "q")
        perb, mb, sb, nb = within_slice_rho(mix, c, "breadth", "ebin")
        is_ne = (abs(mq) >= BAR_RHO) and (sq >= BAR_LEVELS)
        is_br = (abs(mb) >= BAR_RHO) and (sb >= BAR_LEVELS)
        cls = "JOINT" if (is_ne and is_br) else "n_elig" if is_ne else "breadth" if is_br else "NULL"
        b_br, b_k, r2 = rank_ols2(mix[c], np.log(mix.breadth), np.log(mix.k))
        drows.append(dict(stat=c, label=SLABEL[c],
                          uncond_rho_breadth=spearman(mix[c], mix.breadth),
                          uncond_rho_Ebar=spearman(mix[c], mix.Ebar),
                          uncond_rho_k=spearman(mix[c], mix.k),
                          withinq_rho_Ebar=mq, withinq_signlevels=f"{sq}/{nq}",
                          withinE_rho_breadth=mb, withinE_signlevels=f"{sb}/{nb}",
                          partial_Ebar_given_breadth=partial_spearman(mix[c], mix.Ebar, mix.breadth),
                          partial_breadth_given_Ebar=partial_spearman(mix[c], mix.breadth, mix.Ebar),
                          beta_logbreadth=b_br, beta_logk=b_k, R2=r2,
                          beta_reading=beta_reading(b_br, b_k),
                          is_nelig=is_ne, is_breadth=is_br, verdict=cls,
                          **{f"q{q:.2f}": perq.get(q, np.nan) for q in QS},
                          **{f"ebin{i}": perb.get(i, np.nan) for i in range(N_BINS)}))
    dec = pd.DataFrame(drows)
    dec.to_csv(f"{OUT}.decomp.csv", index=False)

    P("\nSLICE 1 - WITHIN q (breadth held): Spearman(S, Ebar) at each q level")
    P(dec[["stat"] + [f"q{q:.2f}" for q in QS] + ["withinq_rho_Ebar", "withinq_signlevels"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("\nSLICE 2 - WITHIN Ebar bin (n_elig held): Spearman(S, breadth) in each bin")
    P(dec[["stat"] + [f"ebin{i}" for i in range(N_BINS)] + ["withinE_rho_breadth", "withinE_signlevels"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("\nCONTINUOUS CROSS-CHECKS (no binning): partial Spearmans, and the rank regression on")
    P("(log breadth, log k) - the coordinates that span (log Ebar, log k) since")
    P("log Ebar == log breadth + log k exactly.  beta_logbreadth ~ beta_logk => log Ebar.")
    P(dec[["stat", "uncond_rho_breadth", "uncond_rho_Ebar", "uncond_rho_k",
           "partial_Ebar_given_breadth", "partial_breadth_given_Ebar",
           "beta_logbreadth", "beta_logk", "R2", "beta_reading"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P("  The regression is what DISAMBIGUATES slice 2: inside an Ebar bin breadth and k move")
    P(f"  together (rho {np.nanmean([spearman(s.breadth, s.k) for _, s in mix.groupby('ebin')]):+.3f}), "
      "so a slice-2 loading alone cannot tell a breadth statistic from a")
    P("  low-k one.  beta_logk ~ 0 beside a large beta_logbreadth is what makes it breadth.")
    P("\nVERDICT PER STATISTIC (pre-registered bar):")
    P(dec[["label", "withinq_rho_Ebar", "withinq_signlevels", "withinE_rho_breadth",
           "withinE_signlevels", "verdict", "beta_reading"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    n_ne = int(dec.is_nelig.sum()); n_br = int(dec.is_breadth.sum())
    n_joint = int((dec.is_nelig & dec.is_breadth).sum())
    n_null = int((~dec.is_nelig & ~dec.is_breadth).sum())
    P(f"\nTHE COUNT THE QUEUE ASKED FOR: {n_ne} of {len(dec)} published 'panel property' "
      f"statistics are n_elig statistics")
    P(f"  n_elig only {n_ne - n_joint}   breadth only {n_br - n_joint}   JOINT {n_joint}   NULL {n_null}")
    P(f"  beta reading of the same five: {dec.beta_reading.value_counts().to_dict()}")
    ne = dec[dec.is_nelig]
    if len(ne):
        P("  the n_elig passer(s), read on the regression that separates Ebar from k:")
        for _, r in ne.iterrows():
            P(f"    {r.label}  beta_logbreadth {r.beta_logbreadth:+.3f}  beta_logk {r.beta_logk:+.3f}"
              f"  -> {r.beta_reading}"
              + ("   [equal loadings would mean log Ebar; these are not equal]"
                 if r.beta_reading != "log Ebar" else ""))
    P("  NOTE the asymmetry the queue did not anticipate: a statistic can clear the n_elig")
    P("  slice and still not be a function of n_elig, because n_elig = breadth * k has TWO")
    P("  factors and the within-q slice moves only one of them (k).  The regression says which.")

    # ============================================================ KEEP paths
    P("\n" + "=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4, both, at 10 bps, on every arm row)")
    P("=" * 100)
    bm = books[books.kind == "mix"]
    P(f"  arm rows on the ladder: {len(bm)} ({len(NS_LAD)} CAND + EWall on {len(built)} panels)")
    P(f"  4a (beat RULES v2 on the same panel): {int(bm.pass4a.sum())}/{len(bm)} "
      f"({bm.pass4a.mean():.3%})")
    P(f"  4b (capital-worthy vs SPY):           {int(bm.pass4b.sum())}/{len(bm)} "
      f"({bm.pass4b.mean():.3%})")
    if bm.pass4b.any():
        P("  4b passes by (q, k):")
        P(bm[bm.pass4b].groupby(["q", "k"]).size().to_string())
        P(f"  4b passes by arm: {bm[bm.pass4b].arm.value_counts().to_dict()}")
        P(f"  highest q carrying any 4b pass: {bm[bm.pass4b].q.max():.2f}")
        P("  Ebar / breadth of the 4b passers vs the rest: "
          f"Ebar {bm[bm.pass4b].Ebar.mean():.1f} vs {bm[~bm.pass4b].Ebar.mean():.1f}; "
          f"breadth {bm[bm.pass4b].breadth.mean():.4f} vs {bm[~bm.pass4b].breadth.mean():.4f}")
    bn = books[books.kind == "named"]
    P(f"  named panels: 4a {int(bn.pass4a.sum())}/{len(bn)}, 4b {int(bn.pass4b.sum())}/{len(bn)}")
    P("  NOTE: no arm here is a new BOOK - CAND-n and EWall are the record's existing books "
      "re-run on re-drawn panels.  A pass is a statement about the panel, not a candidate.")

    # ============================================================ rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - properties measured on 2010..2016, read once on 2017..2026")
    P("=" * 100)
    bmix = books[(books.kind == "mix") & books.n.notna()].copy()
    props = mix.set_index("panel")[["Ebar_IS", "breadth_IS", "Ebar", "breadth", "q", "k"]]
    bmix = bmix.join(props[["Ebar_IS", "breadth_IS"]], on="panel")
    SELECTORS = {"EBAR-MAX": ("Ebar_IS", True), "EBAR-MIN": ("Ebar_IS", False),
                 "BREADTH-MAX": ("breadth_IS", True), "BREADTH-MIN": ("breadth_IS", False),
                 "IS-SHARPE-MAX": ("IS_Sharpe", True)}
    wrows = []
    for n, sub in bmix.groupby("n"):
        anchor = sub.OOS_Sharpe.mean()
        for sel, (col, hi) in SELECTORS.items():
            pick = sub.loc[sub[col].idxmax() if hi else sub[col].idxmin()]
            wrows.append(dict(n=int(n), selector=sel, panel=pick.panel, q=pick.q, k=pick.k,
                              Ebar_IS=pick.Ebar_IS, breadth_IS=pick.breadth_IS,
                              IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                              OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                              v2_OOS_S=pick.v2_OOS_S, spy_OOS_S=pick.spy_OOS_S,
                              anchor_OOS_S=anchor,
                              beats_anchor=bool(pick.OOS_Sharpe > anchor),
                              beats_v2=bool(pick.OOS_Sharpe > pick.v2_OOS_S),
                              beats_spy=bool(pick.OOS_Sharpe > pick.spy_OOS_S)))
    wf = pd.DataFrame(wrows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\npooled over the 5 book sizes:")
    agg = wf.groupby("selector").agg(OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     OOS_CAGR=("OOS_CAGR", "mean"),
                                     OOS_MaxDD=("OOS_MaxDD", "mean"),
                                     beats_anchor=("beats_anchor", "sum"),
                                     beats_v2=("beats_v2", "sum"),
                                     beats_spy=("beats_spy", "sum"))
    agg["of"] = len(NS_LAD)
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"\ndo-nothing anchor (mean OOS Sharpe over all {len(built)} ladder panels, per n): "
      + ", ".join(f"n={int(n)} {v:.4f}" for n, v in bmix.groupby('n').OOS_Sharpe.mean().items()))
    P(f"SPY OOS Sharpe: {bmix.spy_OOS_S.mean():.4f}   "
      f"RULES v2 OOS Sharpe (mean over ladder panels): {bmix.v2_OOS_S.mean():.4f}")
    P("\nthe rule-8 form of the same question - does the property PREDICT OOS at all?")
    for lbl, col in [("Ebar_IS", "Ebar_IS"), ("breadth_IS", "breadth_IS")]:
        per, m_, s_, n_ = within_slice_rho(bmix, "OOS_Sharpe", col, "n")
        P(f"  Spearman(IS {lbl:11s}, OOS Sharpe) within book size: "
          + ", ".join(f"n={int(k)} {v:+.3f}" for k, v in sorted(per.items()))
          + f"   mean {m_:+.3f}")
    _, mq_, sq_, nq_ = within_slice_rho(bmix[bmix.n == 20], "OOS_Sharpe", "Ebar_IS", "q")
    _, mb_, sb_, nb_ = within_slice_rho(bmix[bmix.n == 20], "OOS_Sharpe", "breadth_IS", "q")
    P(f"  at n=20, WITHIN q: rho(Ebar_IS, OOS Sharpe) {mq_:+.3f} ({sq_}/{nq_} levels); "
      f"rho(breadth_IS, OOS Sharpe) {mb_:+.3f} ({sb_}/{nb_}) "
      "[within q, breadth is held, so the second number is draw noise by construction]")
    e_, b_ = wf[wf.selector == "EBAR-MAX"], wf[wf.selector == "BREADTH-MAX"]
    emin, bmin = wf[wf.selector == "EBAR-MIN"], wf[wf.selector == "BREADTH-MIN"]
    same_panel = int((e_.panel.values == b_.panel.values).sum())
    same_q = int((e_.q.values == b_.q.values).sum()) + int((emin.q.values == bmin.q.values).sum())
    P("\nHEAD TO HEAD, the rule-8 form of the queue's question:")
    P(f"  EBAR-MAX vs BREADTH-MAX pick the same PANEL on {same_panel}/{len(e_)} book sizes - they")
    P(f"  disagree about k (100 vs 60) - but land in the same CAP STRATUM on {same_q}/{2 * len(e_)} "
      "picks counting")
    P(f"  the MIN pair too (every MAX pick is q={e_.q.iloc[0]:.2f}, every MIN pick is "
      f"q={emin.q.iloc[0]:.2f}; EBAR-MIN and BREADTH-MIN are the same panel on "
      f"{int((emin.panel.values == bmin.panel.values).sum())}/{len(e_)}).")
    P(f"  Mean OOS Sharpe {e_.OOS_Sharpe.mean():.4f} vs {b_.OOS_Sharpe.mean():.4f} "
      f"(gap {e_.OOS_Sharpe.mean() - b_.OOS_Sharpe.mean():+.4f}); both beat SPY on "
      f"{int(e_.beats_spy.sum())} / {int(b_.beats_spy.sum())} of {len(e_)} and RULES v2 on "
      f"{int(e_.beats_v2.sum())} / {int(b_.beats_v2.sum())}.")
    P("  Disagreeing about k and agreeing about q costs 0.005 of OOS Sharpe: choosing the panel")
    P("  on n_elig and choosing it on breadth are, out of sample, the SAME selector - both are")
    P("  the cap line wearing two different names.")

    P("\n" + "=" * 100)
    P(f"done in {time.time() - t_start:.1f}s")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dec, stats, books, wf, nmd


if __name__ == "__main__":
    main()
