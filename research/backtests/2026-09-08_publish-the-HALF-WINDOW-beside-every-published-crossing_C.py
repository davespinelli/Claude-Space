#!/usr/bin/env python3
"""Idea 441 — publish-the-HALF-WINDOW-beside-every-published-crossing (lane C, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 439 shows the record's crossings are quoted as bare numbers though the window that
  produced them moves them by up to 4 grid steps.  Propose (half-window, grid step,
  interior?) as required LEADERBOARD columns for any published location and back-fill them
  over the 2 interior crossings and 6 edge/argmax readings the census found.

WHAT THIS RUN DOES (declared before any number is read)
  A. PROVENANCE AUDIT — mechanical, over idea 439's own admitted items.  For each item:
       (a) did the ORIGINAL run smooth its x-axis at all?  Decided by grepping the run's
           committed .py for the record's own smoothing constructs (`local_curve`,
           `HALF_W`, `half_w`, `half-window`, `half window`) — the first matching line is
           printed as evidence, so the call is checkable.
       (b) is the half-window STATED in the run's result.md (what a LEADERBOARD reader can
           reach), in its .py, or in its .console.txt?  Three independent greps.
       (c) the GRID STEP of the committed x-axis, and the x range.
       (d) INTERIOR? — is the published location strictly inside the grid, at an edge, or
           is there no numeric location at all?
     Nothing is inferred: an item with no smoothing construct in its script is reported as
     UNSMOOTHED, and its half-window column as n/a rather than as a missing number.

  B. BACK-FILL / AMBIGUITY — the re-read every reader must do to reproduce a location.
     For every item, the location is re-read across the full (half-window x grid step)
     plane and the resulting SPAN in grid steps is the cost of not publishing the two
     columns.  A split-half diagnostic (10 seeds, cells split at random) gives the sampling
     noise floor the span has to be compared against.

  TWO TUNED PARAMETERS, ALL GRID POINTS REPORTED
    P1  HMULT — half-window as a multiple of the grid step, in {0.5, 1, 2, 3, 4, 5}.
        0.5 = non-overlapping bins (the closest thing to "no smoothing" a local reader has).
        HMULT 3 is the HEADLINE because on item 219 it is that run's own 0.075 to the digit.
    P2  SMULT — grid COARSENING, in {1, 2, 4}: keep every point / every 2nd / every 4th of
        the item's own committed x-grid.  Coarsening only, so it is defined for every item
        (a finer grid than the committed ladder does not exist for the unsmoothed items).
  Nothing else is tuned.  `local_curve`, `crossing_of`, `argmax_of`, `make_grid`, the item
  registry, min-cells-in-window (5) and the interiority convention are IMPORTED from idea
  439's committed script rather than re-chosen, so the frame is the record's own.

RULE 8
  (i)  CENSUS-LEVEL split-half: the location read on two disjoint halves of the same cells,
       10 seeds per item; mean |difference| in grid steps is the noise floor.
  (ii) BOOK-LEVEL (PROTOCOL rule 8, live prices): 252 fresh books, 3 panels x gross
       {0.75, 1.00} x cadence {W, M} x 21 band widths (0.00-0.20 step 0.01).  x = band
       width, y = IS (<= 2016-12-31) Sharpe minus the same cell's bare-200d IS Sharpe.  The
       threshold is read off the IS curve at EVERY (hmult, smult) point, and each adopted
       band is evaluated untouched on 2017-2026 against RULES v2 (live), RULES v1 and SPY.
       The SPREAD of OOS Sharpe across those reads is what a missing (half-window, grid
       step) pair costs a reader who tries to reproduce the adoption.
  BOTH KEEP PATHS are evaluated on all 252 books.

Costs 10 bps, weights at t applied at t+1 (PROTOCOL 2).  Deterministic (seeds fixed).
Artefacts: .console.txt, .provenance.csv, .backfill.csv, .splithalf.csv, .bookgrid.csv,
           .walkforward.csv, .keeppaths.csv, .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations
import sys, re, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest  # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_publish-the-HALF-WINDOW-beside-every-published-crossing_C"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- import idea 439's frame
_SRC = BT / "2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.py"
_spec = importlib.util.spec_from_file_location("idea439", _SRC)
C439 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C439)          # module-level only; its main() is behind __main__

ITEMS = C439.ITEMS
load_item, local_curve, crossing_of = C439.load_item, C439.local_curve, C439.crossing_of
argmax_of, steps_apart, make_grid = C439.argmax_of, C439.steps_apart, C439.make_grid
fast_backtest, band_book, csd = C439.fast_backtest, C439.band_book, C439.csd
COST_BPS, IS_END, OOS_START = C439.COST_BPS, C439.IS_END, C439.OOS_START

HMULTS = [0.5, 1.0, 2.0, 3.0, 4.0, 5.0]      # TUNED PARAMETER 1
SMULTS = [1, 2, 4]                           # TUNED PARAMETER 2
HM_HEADLINE, SM_HEADLINE = 3.0, 1
N_SEEDS = 10

# Each item's SOURCE RUN and the numeric location its own result.md publishes, declared here
# before anything is read.  `pub` is np.nan where the run published a KIND of location
# ("positive throughout", "argmax at the edge", "no crossing exists") and not a number.
PROV = {
    "219":      dict(stem="2026-09-06_what-modal-share-makes-a-mode-writable_cloud",
                     pub=0.425, kindpub="crossing (a number)"),
    "167":      dict(stem="2026-09-05_is-the-value-cost-parallelism-general_cloud",
                     pub=np.nan, kindpub="no crossing exists (12/12 cells)"),
    "159B":     dict(stem="2026-09-05_the-share-at-which-ranking-stops-paying_B",
                     pub=np.nan, kindpub="no crossing inside [0.05, 0.70]"),
    "159c":     dict(stem="2026-09-05_the-share-at-which-ranking-stops-paying_cloud",
                     pub=0.85, kindpub="FITTED log-linear crossing (not a pooled-curve location)"),
    "168B":     dict(stem="2026-09-05_the-sign-is-the-parameter-not-the-share_B",
                     pub=np.nan, kindpub="argmax at the grid EDGE (k >= +0.50, 10/12)"),
    "168c":     dict(stem="2026-09-05_the-sign-is-the-parameter-not-the-share_cloud",
                     pub=np.nan, kindpub="sign statement: live k = -0.5 loses to k = 0, 32/32"),
    "103":      dict(stem="2026-09-07_correlation-as-the-sleeve-design-variable_B",
                     pub=np.nan, kindpub="curve real, correlation killed (positive throughout)"),
    "61":       dict(stem="2026-09-06_gate-instrument-speed-curve_cloud",
                     pub=0.5, kindpub="a FLOOR ~0.5 flips/tkr/yr (per-pool sign statement)"),
    "277":      dict(stem="2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C",
                     pub=np.nan, kindpub="non-monotone; the run declined to locate a turn"),
    "bandgate": dict(stem="2026-09-06_band-gate-on-small-panel_B",
                     pub=np.nan, kindpub="gap rises in band (positive throughout)"),
}

# idea 439's classification, quoted so this run's back-fill scope is the queue's scope
INTERIOR_CROSSING = {"219", "168c"}                       # the 2 interior crossings
EDGE_OR_ARGMAX = {"167", "159B", "103", "bandgate", "168B", "277"}   # the 6 other readings
NOT_A_LOCATION = {"159c", "61"}                           # not pooled-curve locations

# A run SMOOTHED its x-axis iff its committed script contains one of the record's own
# smoothing constructs.  A run STATES its half-window iff its result.md / console.txt
# contains one of the prose forms the record uses for it.  Both patterns are declared here
# and every hit is printed with its line, so each call is checkable by hand.
SMOOTH_PAT = re.compile(r"local_curve|HALF_W\b|half_w\b|local[- ]window", re.I)
PROSE_PAT = re.compile(r"local[-_ ]?window|local_curve|half[-_ ]?window|HALF_W\b|half_w\b"
                       r"|local\s*\(\s*(?:±|\+-|\+/-)", re.I)
NUMWIN_PAT = re.compile(r"(?:HALF_W|half_w)\s*[,=]?\s*[A-Z_, ]*=\s*([0-9.]+)")
NUMWIN_PROSE = re.compile(r"(?:local[-_ ]?window|local)\s*\(?\s*(?:±|\+-|\+/-)\s*([0-9.]+)", re.I)
# a LEADERBOARD row "publishes a location" iff it uses one of the record's location words
LOCWORD_PAT = re.compile(r"\bcrossing\b|\bcrosses\b|\bargmax\b|\bthreshold\b|\bfloor at\b"
                         r"|\bturns? over\b|\bq\*", re.I)
GRIDWORD_PAT = re.compile(r"grid step|step [0-9.]+|grid of|grid point", re.I)
INTWORD_PAT = re.compile(r"\binterior\b|\bgrid edge\b|\bedge of the grid\b", re.I)


# ===================================================================== PART A: provenance
def grep_first(path: Path, pat: re.Pattern):
    if not path.exists():
        return None
    for i, line in enumerate(path.read_text(errors="ignore").split("\n"), 1):
        if pat.search(line):
            return i, line.strip()[:100]
    return None


LB = ROOT / "research" / "LEADERBOARD.md"


def lb_rows_for(stem: str):
    """Every committed LEADERBOARD row whose Script cell names this run."""
    out = []
    for i, line in enumerate(LB.read_text(errors="ignore").split("\n"), 1):
        if line.startswith("|") and stem in line:
            out.append((i, line))
    return out


def run_provenance():
    P("=" * 118)
    P("PART A — PROVENANCE AUDIT: what does the record actually publish beside a location?")
    P("=" * 118)
    rows = []
    for it in ITEMS:
        pid = it["id"]; pr = PROV[pid]
        stem = pr["stem"]
        py, md, con = (BT / f"{stem}.py"), (BT / f"{stem}.result.md"), (BT / f"{stem}.console.txt")
        g_py = grep_first(py, SMOOTH_PAT)
        g_md, g_con = (grep_first(p, PROSE_PAT) for p in (md, con))
        d, keys = load_item(it)
        grid = it.get("grid")
        grid = make_grid(d["__x__"].values) if grid is None else np.asarray(grid, float)
        step = float(np.median(np.diff(np.sort(grid))))
        # the run's own half-window, if a number is in its script or its prose
        hw = np.nan
        if py.exists():
            m = NUMWIN_PAT.search(py.read_text(errors="ignore"))
            if m:
                hw = float(m.group(1))
        hw_prose = np.nan
        if md.exists():
            m = NUMWIN_PROSE.search(md.read_text(errors="ignore"))
            if m:
                hw_prose = float(m.group(1))
        # what the LEADERBOARD rows for this run carry
        lbr = lb_rows_for(stem)
        loc_rows = [(i, l) for i, l in lbr if LOCWORD_PAT.search(l)]
        lb_hw = [(i, l) for i, l in loc_rows if PROSE_PAT.search(l)]
        lb_gs = [(i, l) for i, l in loc_rows if GRIDWORD_PAT.search(l)]
        lb_in = [(i, l) for i, l in loc_rows if INTWORD_PAT.search(l)]
        pub = pr["pub"]
        if not np.isfinite(pub):
            interior = "n/a (no numeric location published)"
        else:
            interior = ("INTERIOR" if float(np.min(grid)) < pub < float(np.max(grid))
                        else "EDGE") if pid not in NOT_A_LOCATION else "n/a (not on this curve)"
        cls = ("interior crossing" if pid in INTERIOR_CROSSING else
               "edge/argmax/no-crossing" if pid in EDGE_OR_ARGMAX else "not a pooled-curve location")
        rows.append(dict(item=pid, census_class=cls, source_run=stem,
                         published=pr["kindpub"], published_value=pub,
                         smoothed_in_script=bool(g_py), half_window_in_script=hw,
                         half_window_in_result_md=hw_prose,
                         stated_in_result_md=bool(g_md), stated_in_console=bool(g_con),
                         lb_rows=len(lbr), lb_location_rows=len(loc_rows),
                         lb_rows_with_half_window=len(lb_hw),
                         lb_rows_with_grid_step=len(lb_gs),
                         lb_rows_with_interior=len(lb_in),
                         cells=len(d), x=it["x"], x_min=float(np.min(grid)),
                         x_max=float(np.max(grid)), grid_points=len(grid), grid_step=step,
                         interior=interior, cell_keys="x".join(keys),
                         evidence_py=(g_py[1] if g_py else ""),
                         evidence_md=(g_md[1] if g_md else "")))
        P(f"\n  [{pid}] {cls}   source {stem}")
        P(f"       published: {pr['kindpub']}"
          + (f"   value {pub:g}" if np.isfinite(pub) else "   value: NONE (a kind, not a number)"))
        P(f"       committed x-axis: {it['x']}  [{np.min(grid):g}, {np.max(grid):g}], "
          f"{len(grid)} grid points, GRID STEP {step:.4g}, {len(d)} cells")
        P(f"       INTERIOR? {interior}")
        P(f"       original run SMOOTHED the x-axis: {'YES' if g_py else 'NO'}"
          + (f"   HALF-WINDOW {hw:g} (= {hw/step:.3g} grid steps)" if np.isfinite(hw) else ""))
        if g_py:
            P(f"         evidence  {stem}.py:{g_py[0]}  {g_py[1]}")
        P(f"       half-window stated in the run's result.md: {'YES' if g_md else 'NO'}"
          + (f"  (= {hw_prose:g})" if np.isfinite(hw_prose) else "")
          + f";  in console.txt: {'YES' if g_con else 'NO'}")
        if g_md:
            P(f"         evidence  {stem}.result.md:{g_md[0]}  {g_md[1]}")
        P(f"       LEADERBOARD rows for this run: {len(lbr)}, of which {len(loc_rows)} publish a "
          f"LOCATION;  of those, carrying the half-window {len(lb_hw)}, a grid step "
          f"{len(lb_gs)}, an interiority word {len(lb_in)}")
        for i, l in loc_rows[:3]:
            P(f"         LEADERBOARD:{i}  {l[:150]}")
    R = pd.DataFrame(rows)
    P("\n  " + "-" * 114)
    P(f"  SUMMARY over {len(R)} admitted items "
      f"({len(INTERIOR_CROSSING)} interior crossings + {len(EDGE_OR_ARGMAX)} edge/argmax "
      f"readings = the queue's 8, + {len(NOT_A_LOCATION)} non-locations):")
    P(f"    published a NUMERIC location                : {int(np.isfinite(R.published_value).sum())} of {len(R)}")
    P(f"    original run SMOOTHED its x-axis            : {int(R.smoothed_in_script.sum())} of {len(R)}")
    P(f"    half-window recoverable from the script     : {int(np.isfinite(R.half_window_in_script).sum())} of {len(R)}")
    P(f"    half-window stated in the run's result.md   : {int(R.stated_in_result_md.sum())} of {len(R)}")
    P(f"    grid step recoverable from committed cells  : {int(R.grid_step.notna().sum())} of {len(R)}")
    P(f"    LEADERBOARD rows for these runs             : {int(R.lb_rows.sum())}, "
      f"{int(R.lb_location_rows.sum())} of them publish a location")
    P(f"      of those location rows, carrying the half-window "
      f"{int(R.lb_rows_with_half_window.sum())}, a grid step {int(R.lb_rows_with_grid_step.sum())}, "
      f"an interiority word {int(R.lb_rows_with_interior.sum())}")

    # ---------------------------------------------------------------- THE BACK-FILL TABLE
    P("\n  " + "-" * 114)
    P("  THE BACK-FILL the queue asks for — the three proposed columns, filled in for the")
    P("  2 interior crossings and the 6 edge/argmax readings (+ the 2 non-locations, for")
    P("  completeness).  'half-window = none (unsmoothed)' is a VALUE, not a gap.")
    P(f"  {'item':9s} {'class':22s} {'location':34s} {'half-window':>13s} {'grid step':>10s} "
      f"{'interior?':>12s}")
    for _, r in R.iterrows():
        hwtxt = (f"{r.half_window_in_script:g} ({r.half_window_in_script/r.grid_step:.3g} st)"
                 if np.isfinite(r.half_window_in_script) else "none (unsmoothed)")
        loc = (f"{r.published_value:g}" if np.isfinite(r.published_value) else "kind only") \
            + f" [{r.published[:24]}]"
        P(f"  {r['item']:9s} {r.census_class:22s} {loc:34s} {hwtxt:>13s} {r.grid_step:10.4g} "
          f"{r.interior[:12]:>12s}")
    return R


# ================================================================== PART B: the back-fill
def coarsen(grid, s):
    g = np.asarray(grid, float)
    return g[::int(s)] if int(s) > 1 else g


def read_at(d, grid, half_w):
    loc = local_curve(d["__x__"].values, d["__y__"].values, grid, half_w)
    ch, below = crossing_of(loc)
    return ch, below, argmax_of(loc), int(sum(np.isfinite(r[2]) for r in loc))


def interior_of(ch, grid):
    return bool(np.isfinite(ch) and ch > float(np.min(grid)))


def run_backfill():
    P("\n" + "=" * 118)
    P("PART B — BACK-FILL: the same committed cells re-read across the (half-window x grid step)")
    P(f"plane.  P1 hmult {HMULTS}  x  P2 smult {SMULTS} = {len(HMULTS)*len(SMULTS)} reads per item,")
    P("every one reported.  SPAN = distance between the extreme readings, in FINEST-grid steps.")
    P("=" * 118)
    rows = []
    for it in ITEMS:
        pid = it["id"]
        d, keys = load_item(it)
        g0 = it.get("grid")
        g0 = make_grid(d["__x__"].values) if g0 is None else np.asarray(g0, float)
        step0 = float(np.median(np.diff(np.sort(g0))))
        P(f"\n  [{pid}] {it['label'][:78]}")
        P(f"       {'smult':>5s} {'step':>8s} {'pts':>4s} {'hmult':>6s} {'half-w':>8s} "
          f"{'crossing':>10s} {'argmax':>9s} {'interior':>9s} {'defined':>8s}")
        for s in SMULTS:
            grid = coarsen(g0, s)
            step = float(np.median(np.diff(np.sort(grid))))
            for hm in HMULTS:
                hw = hm * step
                ch, below, am, nd = read_at(d, grid, hw)
                rows.append(dict(item=pid, census_class=("interior crossing" if pid in INTERIOR_CROSSING
                                                        else "edge/argmax/no-crossing" if pid in EDGE_OR_ARGMAX
                                                        else "not a pooled-curve location"),
                                 smult=s, grid_step=step, grid_points=len(grid),
                                 hmult=hm, half_w=hw, crossing=ch, last_nonpos=below,
                                 argmax=am, interior=interior_of(ch, grid), n_defined=nd))
                P(f"       {s:5d} {step:8.4g} {len(grid):4d} {hm:6.1f} {hw:8.4g} "
                  f"{ch:10.4g} {am:9.4g} {'YES' if interior_of(ch, grid) else 'no':>9s} "
                  f"{nd:8d}")
    B = pd.DataFrame(rows)

    P("\n  " + "-" * 114)
    P("  AMBIGUITY PER ITEM (in units of the item's FINEST grid step):")
    P(f"  {'item':10s} {'class':24s} {'distinct':>8s} {'span all':>9s} {'span hmult':>11s} "
      f"{'span smult':>11s} {'interior':>9s}")
    amb = []
    for it in ITEMS:
        pid = it["id"]
        s = B[B.item == pid]
        g0 = it.get("grid")
        d, _ = load_item(it)
        g0 = make_grid(d["__x__"].values) if g0 is None else np.asarray(g0, float)
        v = s.crossing.dropna().values
        span_all = steps_apart(v.min(), v.max(), g0) if len(v) else np.nan
        vh = s[s.smult == SM_HEADLINE].crossing.dropna().values
        span_h = steps_apart(vh.min(), vh.max(), g0) if len(vh) else np.nan
        vs = s[s.hmult == HM_HEADLINE].crossing.dropna().values
        span_s = steps_apart(vs.min(), vs.max(), g0) if len(vs) else np.nan
        nint = int(s.interior.sum())
        amb.append(dict(item=pid, distinct_readings=int(len(set(np.round(v, 10)))),
                        span_all_steps=span_all, span_hmult_steps=span_h,
                        span_smult_steps=span_s, interior_reads=nint, reads=len(s)))
        P(f"  {pid:10s} {s.census_class.iloc[0]:24s} {len(set(np.round(v,10))):8d} "
          f"{span_all:9.1f} {span_h:11.1f} {span_s:11.1f} {nint:4d}/{len(s):<4d}")
    A = pd.DataFrame(amb)
    B = B.merge(A, on="item", how="left")
    ok = A[np.isfinite(A.span_all_steps)]
    P(f"\n  over the {len(ok)} items with a defined reading: mean span {ok.span_all_steps.mean():.2f} "
      f"grid steps, max {ok.span_all_steps.max():.0f};  "
      f"{int((ok.span_all_steps > 0).sum())} of {len(ok)} move at all")
    P(f"  half-window alone (smult {SM_HEADLINE}) moves it in "
      f"{int((A.span_hmult_steps.fillna(0) > 0).sum())} items; grid step alone "
      f"(hmult {HM_HEADLINE:.0f}) in {int((A.span_smult_steps.fillna(0) > 0).sum())}")
    return B, A


# ============================================================ PART C: rule 8 (i) split-half
def run_splithalf():
    P("\n" + "=" * 118)
    P("PART C — RULE 8 (i): SPLIT-HALF NOISE FLOOR.  The same reading on two disjoint random")
    P(f"halves of each item's cells, {N_SEEDS} seeds, at the headline (hmult {HM_HEADLINE:.0f}, "
      f"smult {SM_HEADLINE}).")
    P("If the (half-window x grid step) span is no larger than this, the columns buy nothing.")
    P("=" * 118)
    rows = []
    P(f"  {'item':10s} {'seeds used':>10s} {'mean |A-B|':>11s} {'max':>5s} {'span all':>9s}")
    for it in ITEMS:
        pid = it["id"]
        d, _ = load_item(it)
        g0 = it.get("grid")
        g0 = make_grid(d["__x__"].values) if g0 is None else np.asarray(g0, float)
        step = float(np.median(np.diff(np.sort(g0))))
        hw = HM_HEADLINE * step
        ds = []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(seed)
            perm = rng.permutation(len(d))
            a, b = d.iloc[perm[: len(d) // 2]], d.iloc[perm[len(d) // 2:]]
            ca, _, _, _ = read_at(a, g0, hw)
            cb, _, _, _ = read_at(b, g0, hw)
            e = steps_apart(ca, cb, g0)
            rows.append(dict(item=pid, seed=seed, crossing_A=ca, crossing_B=cb, steps=e))
            if np.isfinite(e):
                ds.append(e)
        P(f"  {pid:10s} {len(ds):10d} {np.mean(ds) if ds else np.nan:11.2f} "
          f"{max(ds) if ds else np.nan:5.0f}")
    return pd.DataFrame(rows)


# =========================================================== PART D: rule 8 (ii) live prices
BANDS = [round(0.01 * i, 2) for i in range(0, 21)]        # 0.00 .. 0.20, step 0.01
GROSSES = [0.75, 1.00]
CADENCES = ["W", "M"]


def run_books():
    P("\n" + "=" * 118)
    P("PART D — RULE 8 (ii), LIVE PRICES.  Does the (half-window, grid step) pair change the")
    P("threshold a reader would ADOPT, and what does that cost out of sample?  252 books:")
    P("3 panels x gross {0.75, 1.00} x cadence {W, M} x 21 band widths (0.00-0.20 step 0.01),")
    P("10 bps, t+1.  x = band, y = IS Sharpe minus the same cell's bare-200d IS Sharpe.")
    P("Threshold read IS-only at every (hmult, smult); 2017-2026 read once.")
    P("=" * 118)
    panels = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL439", dict(small=True))]:
        px = load_universe(**kw)
        panels[lab] = px
        P(f"  {lab:10s} {px.shape[1]:4d} cols  {px.index[0].date()} -> {px.index[-1].date()}")

    px0 = panels["U56"]
    W0 = rules_v2_weights(px0)
    a = engine_backtest(px0, W0, cost_bps=COST_BPS, freq="W")["returns"]
    b = fast_backtest(px0, W0, COST_BPS, "W")
    P(f"\n  GATE  fast_backtest vs engine.backtest on RULES v2 / U56: "
      f"max |diff| {float(np.abs(a - b).max()):.3e}")
    assert float(np.abs(a - b).max()) < 1e-12

    rows = []
    for lab, px in panels.items():
        st = px.index[260]
        for bnd in BANDS:
            for g in GROSSES:
                W = band_book(px, bnd, g)
                for cd in CADENCES:
                    r = fast_backtest(px, W, COST_BPS, cd).loc[st:]
                    fc, fs, fd = csd(r.values)
                    h = len(r) // 2
                    _, h1, _ = csd(r.iloc[:h].values); _, h2, _ = csd(r.iloc[h:].values)
                    _, isS, _ = csd(r.loc[:IS_END].values)
                    oc, os_, odd = csd(r.loc[OOS_START:].values)
                    rows.append(dict(panel=lab, gross=g, cadence=cd, band=bnd,
                                     CAGR=fc, Sharpe=fs, MaxDD=fd, H1=h1, H2=h2,
                                     IS_Sharpe=isS, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd))
    G = pd.DataFrame(rows)
    G["cell"] = G.panel + "|" + G.gross.astype(str) + "|" + G.cadence
    G["y_IS"] = G.IS_Sharpe - G.cell.map(G[G.band == 0].set_index("cell").IS_Sharpe)
    G["y_OOS"] = G.OOS_Sharpe - G.cell.map(G[G.band == 0].set_index("cell").OOS_Sharpe)
    P(f"\n  {len(G)} books over {G.cell.nunique()} cells.  IS gain over the bare 200d gate:")
    P(f"  {'band':>6s} {'n':>4s} {'mean IS gain':>13s} {'frac>0':>7s} {'mean OOS gain':>14s} "
      f"{'frac>0':>7s}")
    for bnd in BANDS:
        s = G[G.band == bnd]
        P(f"  {bnd:6.2f} {len(s):4d} {s.y_IS.mean():+13.4f} {(s.y_IS > 0).mean():7.2f} "
          f"{s.y_OOS.mean():+14.4f} {(s.y_OOS > 0).mean():7.2f}")

    d = G[G.band > 0].rename(columns={"band": "__x__", "y_IS": "__y__"}).copy()
    g0 = np.array([b for b in BANDS if b > 0], float)
    picks, picks_am = {}, {}
    P(f"\n  IS-only threshold, read at every (hmult, smult) point (crossing; argmax as the")
    P(f"  fallback when the curve carries none):")
    P(f"  {'smult':>5s} {'step':>6s} {'hmult':>6s} {'half-w':>7s} {'crossing':>9s} "
      f"{'argmax':>8s} {'ADOPTED':>8s}")
    for s in SMULTS:
        grid = coarsen(g0, s)
        step = float(np.median(np.diff(grid)))
        for hm in HMULTS:
            ch, _, am, _ = read_at(d, grid, hm * step)
            adopt = ch if np.isfinite(ch) else am
            adopt = float(min(BANDS, key=lambda b: abs(b - adopt))) if np.isfinite(adopt) else np.nan
            picks[(hm, s)] = adopt
            picks_am[(hm, s)] = (float(min(BANDS, key=lambda b: abs(b - am)))
                                 if np.isfinite(am) else np.nan)
            P(f"  {s:5d} {step:6.2f} {hm:6.1f} {hm*step:7.3f} {ch:9.3g} {am:8.3g} "
              f"{adopt:8.2f}")
    vals = sorted({v for v in picks.values() if np.isfinite(v)})
    vals_am = sorted({v for v in picks_am.values() if np.isfinite(v)})
    P(f"\n  the SAME committed IS curve yields {len(vals)} distinct CROSSING-adopted bands across")
    P(f"  the {len(picks)} (half-window, grid step) points: {vals}")
    P(f"  ... and {len(vals_am)} distinct ARGMAX-adopted bands: {vals_am}  <- the reading kind")
    P(f"  6 of the record's 8 published locations actually are (edge/argmax), and it MOVES.")

    P("\n  OOS 2017-2026, read once, pooled over the 12 (panel, gross, cadence) cells:")
    P(f"  {'arm':30s} {'band':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    wf = []

    def add(arm, bnd):
        if bnd is None:
            s = G.loc[G.groupby("cell").OOS_Sharpe.idxmax()]; lab = "orcl"
        else:
            s = G[G.band == bnd]; lab = f"{bnd:.2f}"
        wf.append(dict(arm=arm, band=lab, OOS_CAGR=s.OOS_CAGR.mean(),
                       OOS_Sharpe=s.OOS_Sharpe.mean(), OOS_MaxDD=s.OOS_MaxDD.mean(),
                       IS_Sharpe=s.IS_Sharpe.mean()))
        P(f"  {arm:30s} {lab:>5s} {s.OOS_CAGR.mean():9.2%} {s.OOS_Sharpe.mean():11.4f} "
          f"{s.OOS_MaxDD.mean():10.2%}")
        return wf[-1]

    reads, reads_am = {}, {}
    for (hm, s), bnd in picks.items():
        if np.isfinite(bnd):
            reads[(hm, s)] = add(f"CROSSING read, hmult {hm:g} smult {s}", bnd)
    for (hm, s), bnd in picks_am.items():
        if np.isfinite(bnd):
            reads_am[(hm, s)] = add(f"ARGMAX read, hmult {hm:g} smult {s}", bnd)
    add("bare 200d (band 0)", 0.00)
    add("live RULES v2 band", 0.03)
    add("ORACLE (best OOS band per cell)", None)
    for tag, rd in (("CROSSING", reads), ("ARGMAX", reads_am)):
        oo = [r["OOS_Sharpe"] for r in rd.values()]
        dd = [r["OOS_MaxDD"] for r in rd.values()]
        cc = [r["OOS_CAGR"] for r in rd.values()]
        P(f"\n  SPREAD of the {tag} reading across the {len(rd)} (half-window, grid step) points:")
        P(f"    OOS Sharpe {min(oo):.4f} to {max(oo):.4f} (range {max(oo)-min(oo):.4f});  "
          f"OOS CAGR {min(cc):.2%} to {max(cc):.2%};  "
          f"OOS MaxDD {min(dd):.2%} to {max(dd):.2%} (range {abs(max(dd)-min(dd)):.2%})")

    P("\n  Benchmarks, same OOS window (PROTOCOL 3):")
    P(f"  {'panel':10s} {'series':24s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} {'OOS MaxDD':>10s}")
    bench = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        for nm, r in [("SPY buy-and-hold", spy),
                      ("RULES v2 (live) @10bps", fast_backtest(px, rules_v2_weights(px), COST_BPS, "W").loc[st:]),
                      ("RULES v1 @10bps", fast_backtest(px, rules_v1_weights(px), COST_BPS, "W").loc[st:])]:
            c, sh, mdd = csd(r.loc[OOS_START:].values)
            fc, fs, fdd = csd(r.values)
            h = len(r) // 2
            _, h1, _ = csd(r.iloc[:h].values); _, h2, _ = csd(r.iloc[h:].values)
            bench.append(dict(panel=lab, series=nm, OOS_CAGR=c, OOS_Sharpe=sh, OOS_MaxDD=mdd,
                              CAGR=fc, Sharpe=fs, MaxDD=fdd, H1=h1, H2=h2))
            P(f"  {lab:10s} {nm:24s} {c:9.2%} {sh:11.4f} {mdd:10.2%}")
    B = pd.DataFrame(bench)

    P("\n" + "=" * 118)
    P("BOTH KEEP PATHS on all 252 books (4a vs the LIVE RULES v2 on the book's own panel;")
    P("4b vs SPY on that panel: Sharpe > SPY in H1, H2 and OOS, |MaxDD| <= 60% of SPY's,")
    P("CAGR >= 70% of SPY's).")
    P("=" * 118)
    krows = []
    for lab, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        sc, ss, sdd = csd(spy.values)
        h = len(spy) // 2
        _, sh1, _ = csd(spy.iloc[:h].values); _, sh2, _ = csd(spy.iloc[h:].values)
        _, soos, _ = csd(spy.loc[OOS_START:].values)
        v2 = B[(B.panel == lab) & (B.series.str.startswith("RULES v2"))].iloc[0]
        for _, r in G[G.panel == lab].iterrows():
            p4a = bool(r.H1 > v2.H1 and r.H2 > v2.H2 and r.MaxDD >= v2.MaxDD)
            p4b = bool(r.H1 > sh1 and r.H2 > sh2 and r.OOS_Sharpe > soos
                       and abs(r.MaxDD) <= 0.60 * abs(sdd) and r.CAGR >= 0.70 * sc)
            krows.append(dict(panel=lab, gross=r.gross, cadence=r.cadence, band=r.band,
                              CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                              OOS_Sharpe=r.OOS_Sharpe, spy_H1=sh1, spy_H2=sh2, spy_OOS=soos,
                              spy_CAGR=sc, spy_MaxDD=sdd, pass4a=p4a, pass4b=p4b))
    K = pd.DataFrame(krows)
    P(f"  {'panel':10s} {'books':>6s} {'4a pass':>8s} {'4b pass':>8s}")
    for lab in panels:
        s = K[K.panel == lab]
        P(f"  {lab:10s} {len(s):6d} {int(s.pass4a.sum()):8d} {int(s.pass4b.sum()):8d}")
    P(f"  {'TOTAL':10s} {len(K):6d} {int(K.pass4a.sum()):8d} {int(K.pass4b.sum()):8d}")
    for tag, col in (("4b", "pass4b"), ("4a", "pass4a")):
        s = K[K[col]]
        if len(s):
            P(f"\n  {tag} passes ({len(s)}):  gross values {sorted(s.gross.unique())}, "
              f"bands {sorted(s.band.unique())}, panels {sorted(s.panel.unique())}")
            for _, r in s.head(25).iterrows():
                P(f"    {r.panel:10s} gross {r.gross:.2f} {r.cadence} band {r.band:.2f}  "
                  f"CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} "
                  f"H1/H2 {r.H1:.3f}/{r.H2:.3f} OOS {r.OOS_Sharpe:.3f}")
    return G, pd.DataFrame(wf), B, K, picks, picks_am


# ==================================================================================== main
def main():
    P("=" * 118)
    P("IDEA 441 — PUBLISH THE HALF-WINDOW BESIDE EVERY PUBLISHED CROSSING (lane C, 2026-09-08)")
    P("=" * 118)

    it = ITEMS[0]
    d, keys = load_item(it)
    loc = local_curve(d["__x__"].values, d["__y__"].values, np.asarray(it["grid"], float), 0.075)
    ch, below = crossing_of(loc)
    P("\nREPRODUCTION GATE (idea 219's published crossing, from its own committed cells;")
    P("idea 439's frame imported, not re-implemented)")
    P(f"  cells {len(d)} (published 560);  half-window 0.075, grid 0.20-1.00 step 0.025")
    P(f"  crossing {ch:.3f} (published 0.425)   last non-positive {below:.3f} (published 0.400)"
      f"   -> {'MATCH' if (ch == 0.425 and below == 0.400 and len(d) == 560) else 'MISMATCH'}")
    assert len(d) == 560 and ch == 0.425 and below == 0.400

    R = run_provenance()
    BF, A = run_backfill()
    SH = run_splithalf()
    G, WF, B, K, picks, picks_am = run_books()

    R.to_csv(BT / f"{STEM}.provenance.csv", index=False)
    BF.to_csv(BT / f"{STEM}.backfill.csv", index=False)
    SH.to_csv(BT / f"{STEM}.splithalf.csv", index=False)
    G.to_csv(BT / f"{STEM}.bookgrid.csv", index=False)
    pd.concat([WF.assign(kind="arm"), B.assign(kind="benchmark")], ignore_index=True) \
        .to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    K.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)

    P("\n" + "=" * 118)
    P("HEADLINE")
    P("=" * 118)
    n_num = int(np.isfinite(R.published_value).sum())
    P(f"  1. Of the {len(R)} pooled-curve readings idea 439 admitted, {n_num} publish a NUMBER "
      f"at all; only {int((np.isfinite(R.published_value) & (R.census_class != 'not a pooled-curve location')).sum())} "
      f"of those is a location on its own committed curve.")
    P(f"  2. {int(R.smoothed_in_script.sum())} of {len(R)} runs smoothed their x-axis at all, and "
      f"that run DOES state its half-window in its own result.md "
      f"({int(R.stated_in_result_md.sum())} of {len(R)}); but of the "
      f"{int(R.lb_location_rows.sum())} LEADERBOARD rows that publish a location, "
      f"{int(R.lb_rows_with_half_window.sum())} carry the half-window, "
      f"{int(R.lb_rows_with_grid_step.sum())} a grid step and "
      f"{int(R.lb_rows_with_interior.sum())} an interiority word.")
    P(f"  3. Re-read across {len(HMULTS)}x{len(SMULTS)} (half-window, grid step) points, the "
      f"same committed cells give a span of up to {A.span_all_steps.max():.0f} grid steps.")
    sh = SH.dropna(subset=["steps"]).groupby("item").steps.mean()
    P(f"  4. Split-half noise floor (mean |A-B|, per item): "
      + ", ".join(f"{k} {v:.2f}" for k, v in sh.items()))
    P(f"  5. On live prices, the same IS curve yields "
      f"{len({v for v in picks.values() if np.isfinite(v)})} distinct CROSSING-adopted band(s) "
      f"and {len({v for v in picks_am.values() if np.isfinite(v)})} distinct ARGMAX-adopted "
      f"bands across the {len(picks)} (half-window, grid step) reads.")

    Path(BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {STEM}.console.txt and 6 CSVs")


if __name__ == "__main__":
    main()
