#!/usr/bin/env python3
"""QUEUE idea 256 - every-published-reach-is-a-ladder-edge-until-proven-otherwise  (lane C, 2026-09-06).

QUESTION (pre-registered, verbatim from QUEUE.md idea 256)
    "idea 251 found idea 74's stop reach (2.73pp) sat at the SHALLOWEST level swept and moved to
     6.91pp when the ladder was extended, while the gates and the band did not move at all.
     Census the record for every published ceiling/floor/'unreachable' whose argmax or argmin sits
     at a grid END, and report what fraction of them have ever been re-run with the grid widened.
     Max 2 params."

WHAT IS BEING DECIDED
    A "reach", a "ceiling", a "floor" and an "unreachable" are all the same object: the best value
    a dial attains over the levels somebody chose to sweep.  If the best value sits at the FIRST or
    LAST level of that sweep, the number published is a property of the GRID, not of the
    instrument - the true optimum is somewhere outside and unmeasured.  Idea 251 hit one such case.
    This run answers two separable questions:
      A (CENSUS, mechanical)  over the 717 committed CSV artefacts: what fraction of the record's
        argmaxes sit at a grid END, measured against the null rate a random argmax would produce
        (2/L on a grid of L levels), and what fraction of those grids has anyone ever re-run wider?
      B (EXPERIMENT, engine runs)  does widening actually change the ANSWER, and does it change the
        OUTCOME?  Three dial families are swept at their RECORD grid and at an EXTENDED grid; the
        IS argmax is taken on each grid separately and the OOS window is read ONCE (PROTOCOL 8).
    A alone cannot decide anything: an edge argmax is a warning, not a defect.  B prices the
    warning - it separates edge argmaxes that MOVE and PAY from edge argmaxes that move and cost
    nothing, which is the only distinction a research protocol can act on.

PART A - THE CENSUS, computed in this script, not asserted
    POPULATION.  Every committed research/backtests/*.csv[.gz] (717 files).  A file enters if it
      has >= 6 rows and at least one outcome column named exactly (case-insensitive) Sharpe,
      OOS_Sharpe, Sharpe_OOS, IS_Sharpe, CAGR, OOS_CAGR, CAGR_OOS, IS_CAGR, MaxDD, OOS_MaxDD,
      MaxDD_OOS or IS_MaxDD.  Higher is better for all three families (MaxDD is stored negative),
      so "argmax" covers the idea's "argmax or argmin" - a floor on a loss IS an argmax of MaxDD.
    DIAL DETECTOR (pre-registered, name-blind except for a diagnostic blacklist).  A column is a
      candidate dial if it is >98% numeric, has 3..30 distinct values, has fewer distinct values
      than half the rows, and its name does not match the diagnostic blacklist (Sharpe/CAGR/MaxDD/
      Vol/turnover/gross/pass-fail/margin/t-stat/rho/counts/dates/seeds/means).  The blacklist is
      a name filter and is printed in full; everything downstream is arithmetic.
    CELL.  For dial d in a file, the grouping keys are every other column with 2..30 distinct
      values.  A group is a CELL only if it holds exactly one row per grid level and all L levels -
      i.e. only fully-crossed designs are read.  Ragged designs contribute nothing (conservative).
    EDGE.  best = argmax of the outcome over the cell's L levels; edge = best is the grid min or
      the grid max.  NULL: a uniformly random argmax is at an edge with probability 2/L, so the
      census reports observed edge rate MINUS mean(2/L).  Without that subtraction an edge rate is
      unreadable (on a 3-level grid two thirds of all argmaxes are edges by construction).
    MONOTONE.  A cell is monotone if the outcome is strictly increasing or strictly decreasing in
      the dial (Spearman |rho| == 1).  Monotone AND edge is the class the idea is about: the
      response never turned over, so the published number is the ladder end and nothing else.
    WEIGHTING.  Cell-weighted rates let one 1485-row artefact outvote thirty small ones, so every
      rate is ALSO reported unit-weighted, one unit = (script stem, dial, outcome family), and
      byte-identical files are de-duplicated by content hash first.
    WIDENED.  For each (file, dial) grid, "re-run wider" = another script's artefact sweeps a dial
      of the SAME NAME with a strictly lower min or strictly higher max.  Three variants:
      ANY (any date), LATER (strictly later file date - the only variant that can be called a
      re-run), and SUPERSET (contains the original range on both sides and extends at least one).

PART B - THE EXPERIMENT (does widening move the answer, and is the move worth anything?)
    BOOK, built from baseline.score's committed composite, constant-gross convention (idea 244's
      channel: weights are gross/count, NOT a fixed per-name weight, so an n sweep is not a
      disguised gross ladder):
        elig  = composite where (px > 200d MA) & (vol20 < max_vol)
        w     = gross / count  on the top-n of elig, weekly, t+1, engine-executed
    THREE DIAL FAMILIES, each with the grid the record actually uses (Part A prints the record's
      grids for these dial names) and an EXTENDED grid:
        n        record {5, 10, 20}        extended {2,3,5,8,10,14,20,28,40,56} (+80,136 on broad)
        max_vol  record {0.40,0.60,0.80}   extended {0.20,0.30,0.40,0.60,0.80,1.00,1.50, off}
        gross    record {0.50,0.75,1.00}   extended {0.20,0.35,0.50,0.75,1.00}
      The gross grid's top end is 1.00 because PROTOCOL rule 2 forbids leverage: that end is
      UNWIDENABLE BY PROTOCOL, which is a third census category the idea's dichotomy misses and
      this run reports separately.
    TUNED PARAMETERS: exactly ONE - the swept dial's level, chosen by IS Sharpe on <= 2016-12-31.
      CARRIED AXES, never selected on, every level reported: panel {u56, broad136, small484},
      cost rung {10, 25} bps, and the two dials not swept (n in {5,20} when n is not the dial).
      On small484 the n ladder runs to 484 and SPY is dropped from the selectable set (it is a
      joined benchmark there, not a constituent - data/SMALL_PANEL_README.md).
    COSTS.  Every book is run ONCE at 0 bps and each rung derived from the engine's own turnover
      series (r_net = r_gross - turnover*bps/1e4).  Asserted exact against a genuine engine run.
    WALK-FORWARD (PROTOCOL rule 8).  IS <= 2016-12-31 chooses; 2017-01-01..2026-09 read once.
        PICK-NARROW  IS argmax over the RECORD grid
        PICK-WIDE    IS argmax over the EXTENDED grid
        INCUMBENT    baseline.rules_v1_weights (the live book)
        SPY          buy and hold
      Both KEEP paths (4a vs the live rules, 4b vs SPY) are evaluated for every grid point and
      every pick, full sample and OOS window.  ALL grid points are written to .grid.csv.

PRE-REGISTERED PREDICTIONS (Part B; written before any Part B number was read)
    Part A's pooled edge rates were seen in a prototype before these were written, so they are
    NOT predictions and are not claimed as such; P1-P6 are about Part B, which had not been run.
    P1  The reproduction checks [a]-[b] hold.
    P2  On the `n` family the RECORD grid's IS argmax is the TOP level (20) in a majority of cells,
        and the EXTENDED grid's argmax is above 20 in a majority - the record's n grid end binds.
    P3  The `gross` ladder is monotone in CAGR by construction but nearly flat in Sharpe: the
        spread of OOS Sharpe across the whole extended gross grid is < 0.15 in every cell, so its
        edge argmax is real and decision-IRRELEVANT.
    P4  `max_vol`'s IS argmax sits at the loose end (0.80 / off) in a majority of large-cap cells
        (ideas 38/49/232), and moving from 0.80 to off changes OOS Sharpe by < 0.05: the gate
        rarely binds on large caps, so this is a second decision-irrelevant edge.
    P5  THE DECISIVE ONE.  Widening moves the ANSWER far more often than it moves the OUTCOME:
        the argmax leaves the record grid in a majority of cells, while mean OOS Sharpe
        (wide pick - narrow pick) is <= +0.05 and its paired t-stat is not significant.
    P6  No new 4b KEEP is produced by any widened pick on either panel.

CAVEATS carried, not buried
    * SURVIVORSHIP.  u56 and broad136 are current-constituent lists (idea 54); every LEVEL inherits
      the bias, the narrow-vs-wide COMPARISON is matched and does not.
    * The census matches dials BY NAME across scripts.  `n` means book size everywhere in this
      record, but `k`, `m` and `g` do not have to; a name-matched "wider re-run" can therefore be a
      different dial with the same letter.  The per-dial file counts are printed so the reader can
      discount, and the three Part B families were chosen from the unambiguous names.
    * The census can only see dials that reached a committed CSV.  A ladder discussed in a memo or
      printed only to console is invisible; every count is a floor, not a ceiling.
    * Duplicate artefacts (a script writing the same rows to .grid.csv and .keep.csv, or two
      commits of one run) are de-duplicated by content hash, not by intent; near-duplicates that
      differ by one column survive as two units.  Unit-weighted rates are the guarded ones.
    * Two-sided edges: a 2-level "grid" is all edge, so L >= 3 is required throughout.
    * SPY sits in both cached panels and is eligible for selection, exactly as the incumbent book
      has it (baseline.rules_v1_weights does not drop it).  Matched across all arms.
    * Idea 38 (calendar-day index after 2014-09-17) and idea 126 (t+1 execution only) carry over.

Deterministic, standalone, no seed anywhere (nothing is sampled).
Writes .console.txt, .census.csv, .cells.csv.gz, .widen.csv, .grid.csv, .walkforward.csv,
.keep.csv next to itself.
"""
import hashlib
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

HERE = Path(__file__).resolve()
STEM = HERE.with_suffix("")
BT = ROOT / "research" / "backtests"
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")

_console = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


# --------------------------------------------------------------------------------------
# PART A - the census
# --------------------------------------------------------------------------------------
OUTNAMES = {"sharpe", "oos_sharpe", "sharpe_oos", "is_sharpe",
            "cagr", "oos_cagr", "cagr_oos", "is_cagr",
            "maxdd", "oos_maxdd", "maxdd_oos", "is_maxdd"}
FAMILY = {k: ("sharpe" if "sharpe" in k else "cagr" if "cagr" in k else "maxdd") for k in OUTNAMES}
DIAG = re.compile(
    r"(sharpe|cagr|maxdd|sortino|calmar|vol|turn|^to$|gross|pass|fail|p4a|p4b|f4a|f4b|"
    r"margin|pval|^p$|^t$|tstat|rho|^r2$|days|episodes|flips|delta|^d[A-Z]|rank|_n$|"
    r"^n_|nyears|ncol|n_books|switches|stops|point|seed|mean|median|^sd$|std)", re.I)


def classify(df):
    outs = [c for c in df.columns if str(c).strip().lower() in OUTNAMES]
    dials, keys = [], []
    n = len(df)
    for c in df.columns:
        if c in outs:
            continue
        nu = df[c].nunique(dropna=True)
        if nu < 2 or nu > 30 or nu > n / 2:
            continue
        keys.append(c)
        num = pd.to_numeric(df[c], errors="coerce")
        if num.notna().mean() > 0.98 and nu >= 3 and not DIAG.search(str(c)):
            dials.append(c)
    return outs, dials, keys


def run_census():
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    say(f"[A] committed CSV artefacts: {len(files)}")
    seen, kept = {}, []
    for f in files:
        h = hashlib.sha1(f.read_bytes()).hexdigest()
        if h in seen:
            continue
        seen[h] = f.name
        kept.append(f)
    say(f"[A] after de-duplication by content hash: {len(kept)} ({len(files) - len(kept)} byte-identical dropped)")

    cells, grids = [], []
    for f in kept:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) < 6:
            continue
        outs, dials, keys = classify(df)
        if not outs or not dials:
            continue
        date = f.name[:10]
        stem = re.sub(r"\.[a-z_]+\.csv(\.gz)?$", "", f.name)
        for d in dials:
            x_all = pd.to_numeric(df[d], errors="coerce")
            lv = np.sort(x_all.dropna().unique())
            L = len(lv)
            gk = [k for k in keys if k != d]
            sub = df.dropna(subset=[d])
            groups = sub.groupby(gk, dropna=False, sort=False) if gk else [((), sub)]
            ncell = 0
            for _, g in groups:
                if len(g) != L:
                    continue
                x = pd.to_numeric(g[d], errors="coerce").values
                if len(np.unique(x)) != L:
                    continue
                order = np.argsort(x)
                ncell += 1
                for oc in outs:
                    y = pd.to_numeric(g[oc], errors="coerce").values
                    if np.isnan(y).any():
                        continue
                    ys = y[order]
                    best = float(np.sort(x)[int(np.argmax(ys))])
                    dy = np.diff(ys)
                    mono = bool(np.all(dy > 0) or np.all(dy < 0))
                    cells.append(dict(
                        stem=stem, file=f.name, date=date, dial=d, L=L,
                        gmin=float(lv[0]), gmax=float(lv[-1]), outcome=oc,
                        fam=FAMILY[str(oc).strip().lower()], best=best,
                        edge_lo=best == float(lv[0]), edge_hi=best == float(lv[-1]),
                        monotone=mono, null=2.0 / L))
            if ncell:
                grids.append(dict(stem=stem, file=f.name, date=date, dial=d, L=L,
                                  gmin=float(lv[0]), gmax=float(lv[-1]), cells=ncell))
    C = pd.DataFrame(cells)
    G = pd.DataFrame(grids)
    C["edge"] = C.edge_lo | C.edge_hi
    say(f"[A] readable cells: {len(C)}  over {C.file.nunique()} artefacts, "
        f"{C.stem.nunique()} scripts, {C.dial.nunique()} distinct dial names, {len(G)} (file,dial) grids")

    say("\n[A1] EDGE RATE vs the 2/L null - cell-weighted")
    C["edge_mono"] = C.edge & C.monotone
    C["edge_turn"] = C.edge & ~C.monotone
    t = C.groupby("fam").agg(cells=("edge", "size"), edge=("edge", "mean"),
                             null=("null", "mean"), monotone=("monotone", "mean"),
                             edge_mono=("edge_mono", "mean"), edge_turn=("edge_turn", "mean"))
    t["excess"] = t.edge - t.null
    say(t.to_string(float_format=lambda v: f"{v:.3f}"))
    say(f"ALL: cells {len(C)}  edge {C.edge.mean():.3f}  null {C.null.mean():.3f}  "
        f"excess {C.edge.mean() - C.null.mean():+.3f}")
    say(f"     decomposition: edge & MONOTONE (the ladder never turned over) {C.edge_mono.mean():.3f}; "
        f"edge & non-monotone (it turned, best still at an end) {C.edge_turn.mean():.3f}; "
        f"interior argmax {1 - C.edge.mean():.3f}")
    say("     (a strictly monotone response has its argmax at an end by construction, so "
        "edge&monotone == monotone; the reportable split is monotone vs edge-but-turning.)")
    cost_dials = C.dial.str.lower().isin(["cost", "cost_bps", "bps"])
    say(f"     cost-rung dials (cost/cost_bps/bps), where an edge is EXPECTED (more cost is always "
        f"worse): {int(cost_dials.sum())} cells, edge {C[cost_dials].edge.mean():.3f}; "
        f"all other dials: {int((~cost_dials).sum())} cells, edge {C[~cost_dials].edge.mean():.3f} "
        f"vs null {C[~cost_dials].null.mean():.3f}")

    say("\n[A2] EDGE RATE - unit-weighted (one unit = script stem x dial x outcome family)")
    U = C.groupby(["stem", "dial", "fam"]).agg(cells=("edge", "size"), edge=("edge", "mean"),
                                               null=("null", "mean"), mono=("monotone", "mean"),
                                               L=("L", "mean")).reset_index()
    say(f"units {len(U)}   mean edge {U.edge.mean():.3f}   mean null {U.null.mean():.3f}   "
        f"excess {U.edge.mean() - U.null.mean():+.3f}   mean monotone {U.mono.mean():.3f}")
    say(f"units whose argmax is at an edge in EVERY cell: {int((U.edge == 1).sum())} / {len(U)} "
        f"({(U.edge == 1).mean():.1%});  never at an edge: {int((U.edge == 0).sum())} "
        f"({(U.edge == 0).mean():.1%})")
    say(U.groupby("fam").agg(units=("edge", "size"), edge=("edge", "mean"), null=("null", "mean"),
                             mono=("mono", "mean")).to_string(float_format=lambda v: f"{v:.3f}"))

    say("\n[A3] BY DIAL NAME (unit-weighted; files = how many artefacts use the name)")
    D = U.groupby("dial").agg(units=("edge", "size"), edge=("edge", "mean"), null=("null", "mean"),
                              mono=("mono", "mean"), L=("L", "mean")).reset_index()
    D["files"] = D.dial.map(G.groupby("dial").file.nunique())
    D["stems"] = D.dial.map(G.groupby("dial").stem.nunique())
    D = D.sort_values("units", ascending=False)
    say(D.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    say("\n[A4] HAS THE GRID EVER BEEN RE-RUN WIDER?  (per (file,dial) grid, matched on dial name)")
    def widen_flags(r):
        o = G[(G.dial == r.dial) & (G.stem != r.stem)]
        lo = o.gmin < r.gmin - 1e-12
        hi = o.gmax > r.gmax + 1e-12
        any_w = bool((lo | hi).any())
        later = bool((o.date > r.date)[lo | hi].any()) if len(o) else False
        sup = bool(((o.gmin <= r.gmin + 1e-12) & (o.gmax >= r.gmax - 1e-12) & (lo | hi)).any())
        return any_w, later, sup
    flags = [widen_flags(r) for r in G.itertuples()]
    G["wider_any"], G["wider_later"], G["wider_superset"] = zip(*flags)
    G["edge"] = G.set_index(["file", "dial"]).index.map(
        C.groupby(["file", "dial"]).edge.mean())
    E = G[G.edge > 0.5]                       # grids whose typical argmax is an edge
    say(f"grids: {len(G)};  grids whose argmax is an edge in >50% of their cells: {len(E)} "
        f"({len(E) / len(G):.1%})")
    for label, sub in (("ALL grids", G), ("EDGE grids", E)):
        say(f"  {label:11s} ever wider (any date) {sub.wider_any.mean():.1%};  "
            f"wider LATER {sub.wider_later.mean():.1%};  strict SUPERSET {sub.wider_superset.mean():.1%}")
    say("  by dial name, EDGE grids only:")
    say(E.groupby("dial").agg(grids=("file", "size"), wider_any=("wider_any", "mean"),
                              wider_later=("wider_later", "mean"),
                              superset=("wider_superset", "mean")
                              ).sort_values("grids", ascending=False).to_string(
        float_format=lambda v: f"{v:.2f}"))

    say("\n[A5] the record's own grids for the three Part B dial names")
    for name in ("n", "max_vol", "gross", "g", "cost", "cost_bps"):
        s = G[G.dial == name]
        if len(s):
            lo, hi = s.groupby(["gmin", "gmax"]).size().idxmax()
            say(f"  {name:9s} {len(s)} grids over {s.stem.nunique()} scripts; "
                f"min of mins {s.gmin.min():g}, max of maxes {s.gmax.max():g}; "
                f"modal grid [{lo:g},{hi:g}]")
        else:
            say(f"  {name:9s} never appears as a swept numeric dial in a committed CSV")
    C.to_csv(f"{STEM}.cells.csv.gz", index=False)
    G.to_csv(f"{STEM}.widen.csv", index=False)
    D.to_csv(f"{STEM}.census.csv", index=False)
    return C, G, U


# --------------------------------------------------------------------------------------
# PART B - the experiment
# --------------------------------------------------------------------------------------
def book_weights(px, n, max_vol, gross, drop_spy=False):
    """Constant-gross top-n on the committed composite (idea 244's NORM channel).

    drop_spy: on SMALL484 the SPY column is a joined BENCHMARK, not a panel constituent
    (data/SMALL_PANEL_README.md), so it is removed from the selectable set there.
    """
    s, above, vol20 = score(px, vol_scale=True)
    elig = s.where(above & (vol20 < max_vol))
    if drop_spy and "SPY" in elig.columns:
        elig = elig.drop(columns=["SPY"])
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    cnt = sel.sum(axis=1).replace(0.0, np.nan)
    w = (sel.div(cnt, axis=0) * gross).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


def win_metrics(r, prefix=""):
    m = metrics(r)
    return {prefix + "CAGR": m["CAGR"], prefix + "Sharpe": m["Sharpe"], prefix + "MaxDD": m["MaxDD"]}


def all_metrics(r):
    h = len(r) // 2
    d = win_metrics(r)
    d["H1"] = metrics(r.iloc[:h])["Sharpe"]
    d["H2"] = metrics(r.iloc[h:])["Sharpe"]
    d.update(win_metrics(r.loc[:IS_END], "IS_"))
    d.update(win_metrics(r.loc[OOS_START:], "OOS_"))
    return d


def keep_flags(d, base, spy):
    """4a vs the live rules, 4b vs SPY - PROTOCOL rule 4, evaluated on the same window set."""
    p4a = (d["H1"] > base["H1"]) and (d["H2"] > base["H2"]) and (d["MaxDD"] >= base["MaxDD"])
    fails = []
    if not d["H1"] > spy["H1"]:
        fails.append("H1")
    if not d["H2"] > spy["H2"]:
        fails.append("H2")
    if not d["OOS_Sharpe"] > spy["OOS_Sharpe"]:
        fails.append("OOS")
    if not d["MaxDD"] >= 0.60 * spy["MaxDD"]:
        fails.append("DD")
    if not d["CAGR"] >= 0.70 * spy["CAGR"]:
        fails.append("CAGR")
    return p4a, (len(fails) == 0), "|".join(fails) if fails else "-"


EXT_N = {"u56": [2, 3, 5, 8, 10, 14, 20, 28, 40, 56],
         "broad136": [2, 3, 5, 8, 10, 14, 20, 28, 40, 56, 80, 136],
         "small484": [2, 3, 5, 8, 10, 14, 20, 28, 40, 56, 80, 140, 240, 484]}
EXT_MV = [0.20, 0.30, 0.40, 0.60, 0.80, 1.00, 1.50, 99.0]
EXT_G = [0.20, 0.35, 0.50, 0.75, 1.00]
FAMILIES = {
    "n":       dict(record=[5, 10, 20], ext=lambda p: EXT_N[p]),
    "max_vol": dict(record=[0.40, 0.60, 0.80], ext=lambda p: EXT_MV),
    "gross":   dict(record=[0.50, 0.75, 1.00], ext=lambda p: EXT_G),
}
CARRIED_N = [5, 20]
RUNGS = [10, 25]


def run_experiment():
    panels = {"u56": load_universe(), "broad136": load_universe(broad=True),
              "small484": load_universe(small=True)}
    rows, refs, cache = [], {}, {}

    for pname, px in panels.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_m = all_metrics(spy_r)
        base_raw = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        for bps in RUNGS:
            b = (base_raw["returns"] - base_raw["turnover"] * bps / 1e4).loc[start:]
            refs[(pname, bps, "RULESv1")] = all_metrics(b)
            refs[(pname, bps, "SPY")] = spy_m
        say(f"\n[B] {pname}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}  SPY full Sharpe {spy_m['Sharpe']:.3f} "
            f"CAGR {spy_m['CAGR']:.1%} MaxDD {spy_m['MaxDD']:.1%} OOS Sharpe {spy_m['OOS_Sharpe']:.3f}")

        drop_spy = pname == "small484"

        def run(n, mv, g):
            key = (pname, n, mv, g)
            if key not in cache:
                res = backtest(px, book_weights(px, n, mv, g, drop_spy), cost_bps=0.0, freq="W")
                cache[key] = (res["returns"], res["turnover"])
            return cache[key]

        for fam, spec in FAMILIES.items():
            ext = spec["ext"](pname)
            levels = sorted(set(spec["record"]) | set(ext))
            carried = [None] if fam == "n" else CARRIED_N
            for cn in carried:
                for lev in levels:
                    n = lev if fam == "n" else cn
                    mv = lev if fam == "max_vol" else 0.60
                    g = lev if fam == "gross" else 0.75
                    if n > px.shape[1]:
                        continue
                    r0, to = run(n, mv, g)
                    for bps in RUNGS:
                        r = (r0 - to * bps / 1e4).loc[start:]
                        d = all_metrics(r)
                        p4a, p4b, f4b = keep_flags(d, refs[(pname, bps, "RULESv1")], spy_m)
                        rows.append(dict(panel=pname, family=fam, carried_n=cn, level=lev,
                                         n=n, max_vol=mv, gross=g, cost=bps,
                                         in_record=lev in spec["record"], in_ext=lev in ext,
                                         turn=float(to.loc[start:].sum() / (len(r) / 252)),
                                         pass4a=p4a, pass4b=p4b, fail4b=f4b, **d))
            say(f"    {fam:8s} done ({len(levels)} levels x {len(carried)} carried n)")
    return pd.DataFrame(rows), refs


def walk_forward(GR, refs):
    """PICK-NARROW (IS argmax on the record grid) vs PICK-WIDE (IS argmax on the extended grid)."""
    out = []
    for (panel, fam, cn, bps), g in GR.groupby(["panel", "family", "carried_n", "cost"], dropna=False):
        rec = g[g.in_record]
        ext = g[g.in_ext]
        if len(rec) < 3 or len(ext) < 3:
            continue
        pn = rec.loc[rec.IS_Sharpe.idxmax()]
        pw = ext.loc[ext.IS_Sharpe.idxmax()]
        base = refs[(panel, bps, "RULESv1")]
        spy = refs[(panel, bps, "SPY")]
        rec_lo, rec_hi = rec.level.min(), rec.level.max()
        row = dict(panel=panel, family=fam, carried_n=cn, cost=bps,
                   rec_grid=f"[{rec_lo:g},{rec_hi:g}]", ext_grid=f"[{ext.level.min():g},{ext.level.max():g}]",
                   narrow_pick=pn.level, wide_pick=pw.level,
                   narrow_at_edge=bool(pn.level in (rec_lo, rec_hi)),
                   wide_outside_record=bool(pw.level < rec_lo or pw.level > rec_hi),
                   wide_at_ext_edge=bool(pw.level in (ext.level.min(), ext.level.max())),
                   n_OOS_Sharpe=pn.OOS_Sharpe, w_OOS_Sharpe=pw.OOS_Sharpe,
                   d_OOS_Sharpe=pw.OOS_Sharpe - pn.OOS_Sharpe,
                   n_OOS_CAGR=pn.OOS_CAGR, w_OOS_CAGR=pw.OOS_CAGR,
                   n_OOS_MaxDD=pn.OOS_MaxDD, w_OOS_MaxDD=pw.OOS_MaxDD,
                   ext_OOS_spread=ext.OOS_Sharpe.max() - ext.OOS_Sharpe.min(),
                   best_possible_OOS=ext.OOS_Sharpe.max(),
                   v1_OOS_Sharpe=base["OOS_Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                   v1_OOS_CAGR=base["OOS_CAGR"], spy_OOS_CAGR=spy["OOS_CAGR"],
                   spy_OOS_MaxDD=spy["OOS_MaxDD"],
                   n_pass4a=bool(pn.pass4a), w_pass4a=bool(pw.pass4a),
                   n_pass4b=bool(pn.pass4b), w_pass4b=bool(pw.pass4b),
                   n_fail4b=pn.fail4b, w_fail4b=pw.fail4b)
        out.append(row)
    return pd.DataFrame(out)


def main():
    t0 = time.time()
    say("=" * 100)
    say("idea 256  every-published-reach-is-a-ladder-edge-until-proven-otherwise   lane C  2026-09-06")
    say("=" * 100)
    say("dial-detector diagnostic blacklist: " + DIAG.pattern)

    C, G, U = run_census()

    # -------- reproduction checks -------------------------------------------------------
    say("\n[B0] reproduction checks")
    px = load_universe()
    w = book_weights(px, 5, 0.60, 0.75)
    a = backtest(px, w, cost_bps=0.0, freq="W")
    b = backtest(px, w, cost_bps=10.0, freq="W")
    derived = a["returns"] - a["turnover"] * 10 / 1e4
    err = float((derived - b["returns"]).abs().max())
    say(f"  [a] cost identity: max|derived(10bps from 0bps) - engine(10bps)| = {err:.3e}")
    assert err < 1e-15, err
    wv1 = rules_v1_weights(px)
    bv1 = backtest(px, wv1, cost_bps=10.0, freq="W")
    start = px.index[260]
    say(f"  [b] incumbent RULES v1 @10bps on u56: Sharpe "
        f"{metrics(bv1['returns'].loc[start:])['Sharpe']:.4f} "
        f"(baseline.compare self-check reference 0.6170 over its own window)")
    say(f"  [c] constant-gross convention: mean realised gross at n=5,g=0.75 = "
        f"{float(w.sum(axis=1).replace(0, np.nan).mean()):.4f} (target 0.75)")

    GR, refs = run_experiment()
    GR.to_csv(f"{STEM}.grid.csv", index=False)
    say(f"\n[B] grid points written: {len(GR)}")

    say("\n[B1] the extended ladders, OOS Sharpe @10bps (record levels marked *)")
    for (panel, fam, cn), g in GR[GR.cost == 10].groupby(["panel", "family", "carried_n"], dropna=False):
        g = g.sort_values("level")
        s = "  ".join(f"{r.level:g}{'*' if r.in_record else ''}:{r.OOS_Sharpe:.3f}" for r in g.itertuples())
        say(f"  {panel:9s} {fam:8s} carried_n={cn}  {s}")

    WF = walk_forward(GR, refs)
    WF.to_csv(f"{STEM}.walkforward.csv", index=False)
    say("\n[B2] WALK-FORWARD (PROTOCOL rule 8): IS<=2016 chooses, 2017+ read once")
    cols = ["panel", "family", "carried_n", "cost", "rec_grid", "narrow_pick", "narrow_at_edge",
            "wide_pick", "wide_outside_record", "wide_at_ext_edge", "n_OOS_Sharpe", "w_OOS_Sharpe",
            "d_OOS_Sharpe", "v1_OOS_Sharpe", "spy_OOS_Sharpe", "n_pass4b", "w_pass4b"]
    say(WF[cols].to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    say("\n[B3] the two rates the idea is actually about")
    say(f"  cells: {len(WF)}")
    say(f"  record-grid IS argmax sits at a grid END:            "
        f"{WF.narrow_at_edge.mean():.1%} ({int(WF.narrow_at_edge.sum())}/{len(WF)})")
    say(f"  widening MOVES the argmax outside the record grid:   "
        f"{WF.wide_outside_record.mean():.1%} ({int(WF.wide_outside_record.sum())}/{len(WF)})")
    say(f"  widened argmax is ITSELF at the extended grid's end: "
        f"{WF.wide_at_ext_edge.mean():.1%} ({int(WF.wide_at_ext_edge.sum())}/{len(WF)})")
    d = WF.d_OOS_Sharpe.values
    tstat = float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))) if d.std(ddof=1) > 0 else float("nan")
    say(f"  OOS Sharpe (wide pick - narrow pick): mean {d.mean():+.4f}  median {np.median(d):+.4f}  "
        f"sd {d.std(ddof=1):.4f}  t {tstat:+.2f}  wins {int((d > 0).sum())}/{len(d)}")
    mv = WF[WF.wide_outside_record]
    if len(mv):
        dm = mv.d_OOS_Sharpe.values
        say(f"  restricted to cells where the pick actually MOVED ({len(mv)}): mean {dm.mean():+.4f}  "
            f"median {np.median(dm):+.4f}  wins {int((dm > 0).sum())}/{len(dm)}")
    say("  per family:")
    say(WF.groupby("family").agg(cells=("d_OOS_Sharpe", "size"),
                                 narrow_edge=("narrow_at_edge", "mean"),
                                 moved=("wide_outside_record", "mean"),
                                 d_OOS=("d_OOS_Sharpe", "mean"),
                                 ext_spread=("ext_OOS_spread", "mean"),
                                 wide_4b=("w_pass4b", "mean")).to_string(float_format=lambda v: f"{v:.3f}"))

    say("\n[B4] KEEP paths on the picks (4a vs live rules, 4b vs SPY, full sample + OOS bar)")
    K = WF[["panel", "family", "carried_n", "cost", "narrow_pick", "n_pass4a", "n_pass4b", "n_fail4b",
            "wide_pick", "w_pass4a", "w_pass4b", "w_fail4b", "w_OOS_Sharpe", "w_OOS_CAGR",
            "w_OOS_MaxDD", "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
    say(K.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    K.to_csv(f"{STEM}.keep.csv", index=False)
    say(f"  4b passes: narrow picks {int(WF.n_pass4b.sum())}/{len(WF)}, "
        f"wide picks {int(WF.w_pass4b.sum())}/{len(WF)}")
    say(f"  4a passes: narrow picks {int(WF.n_pass4a.sum())}/{len(WF)}, "
        f"wide picks {int(WF.w_pass4a.sum())}/{len(WF)}")
    best = GR[GR.pass4b]
    if len(best):
        say("  every 4b-passing grid point:")
        say(best[["panel", "family", "carried_n", "level", "cost", "CAGR", "Sharpe", "MaxDD",
                  "H1", "H2", "OOS_Sharpe", "in_record"]].to_string(
            index=False, float_format=lambda v: f"{v:.3f}"))
    else:
        say("  no grid point passes 4b anywhere on the three panels.")

    say("\n[B5] the decisive census cross-link: are the capital-worthy points inside the grids the "
        "record sweeps?")
    inside = GR[GR.in_record]
    outside = GR[~GR.in_record]
    say(f"  grid points inside a record grid  : {len(inside):3d}, 4b passes {int(inside.pass4b.sum())} "
        f"({inside.pass4b.mean():.1%}), 4a passes {int(inside.pass4a.sum())}")
    say(f"  grid points outside a record grid : {len(outside):3d}, 4b passes {int(outside.pass4b.sum())} "
        f"({outside.pass4b.mean():.1%}), 4a passes {int(outside.pass4a.sum())}")
    say(f"  best OOS Sharpe inside  record grids: {inside.OOS_Sharpe.max():.3f}")
    say(f"  best OOS Sharpe outside record grids: {outside.OOS_Sharpe.max():.3f}")

    say(f"\n[done] {time.time() - t0:.1f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
