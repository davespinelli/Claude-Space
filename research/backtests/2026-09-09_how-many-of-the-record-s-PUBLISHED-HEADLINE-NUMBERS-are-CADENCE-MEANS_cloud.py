#!/usr/bin/env python3
"""Idea 577 — HOW MANY OF THE RECORD'S PUBLISHED HEADLINE NUMBERS ARE CADENCE MEANS  (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number below was read)
    Idea 314 found idea 51R's headline "-3.93 vs -1.44 pp/yr, 2.7x" is a mean over three
    cadences pairing a 0-bps CAGR column with a 10-bps Sharpe column, and that the ratio
    reads 1.54x at the weekly cell and 4.69x at monthly; sign and ordering held everywhere
    but the magnitude is an average nobody can trade.  Census the committed CSVs for
    headline claims whose quoted number is a MEAN OVER A REPORTING AXIS (cadence, cost
    rung, seed, panel) rather than a cell, and report how many change by more than 2x at
    their own cells.  Max 2 params.

WHAT IS UNDER TEST.  Not a book.  The object is the RECORD ITSELF: every committed
research/backtests/*.csv[.gz].  A "collapsed cell" is one (file, metric column, reporting
axis) triple where the axis carries >= 2 levels inside that file, so that the file's pooled
mean of the metric — the number a memo quotes when it writes one figure — is an average
over levels that a trader must pick between.  For each such triple we compute the pooled
mean (the HEADLINE) and the per-level means (the CELLS), and ask by how much the cells
disagree.

THE FOUR REPORTING AXES are exactly the four the queue names, fixed before any read:
    cadence  {cadence, cad, freq}          cost  {cost, bps, cost_bps, rung, cost_rung}
    seed     {seed, draw, rep, replicate}  panel {panel, universe, uni}
Nothing else is treated as an axis.  Gross, n, band, book and family are NOT axes here:
they are the objects of most of the record's sweeps, and collapsing over them is a
different (and already-cited) sin.  A column with > 20 distinct levels is treated as an
identifier, not an axis, and dropped.

METRICS are columns whose name contains cagr / sharpe / maxdd / turn / _pp / pp_, or is
exactly h1, h2, dd.  They must be numeric with >= 2 non-null values.

THE TWO TUNED PARAMETERS (there are exactly two; every other axis is reported at every
value and never selected on)
    P1  RSTAR, the disagreement threshold.  Point value 2.0 (the queue's own bar).
        Reported at every point of {1.25, 1.5, 2.0, 3.0, 5.0, 10.0}.
    P2  MATCHPREC, which numeric renderings count as "this headline was published".
        Point value the 3-significant-figure set.  Reported at every point of
        {2dp, 3dp, pct1dp, pct2dp, ALL}.

PRE-REGISTERED BARS
    B1  COLLAPSE RATE.  If > 20% of collapsed cells move more than RSTAR=2.0x across their
        own levels, quoting a single pooled number is a record-wide practice that loses
        the magnitude, not a one-file slip in idea 51R.
    B2  SIGN FLIP.  The severe case: the cells disagree in SIGN, so the headline's
        direction is an artefact of the mix.  Any non-trivial rate here is worse than B1.
    B3  PUBLISHED SUBSET.  Restricted to headlines that literally appear in the published
        surface (research/LEADERBOARD.md + research/CHANGELOG.md), is the collapse rate
        HIGHER or LOWER than the corpus rate?  Higher means the record publishes its
        worst averages; lower means the memos already quote cells.
        This leg is reported as an UPPER BOUND and its collision rate is printed: a
        rendering like "0.50" occurs in the published text for reasons unrelated to the
        file that produced it, and this run does not pretend otherwise.

RULE 8 (PROTOCOL 8) — two walk-forwards, because this idea produces no book.
    WF-CENSUS  The corpus is split by each file's own date stamp at the median commit
        date.  RSTAR is chosen on the IS half ALONE as the smallest grid value whose IS
        flag rate falls to <= 20%, and the OOS half is then read ONCE at that value.  A
        census whose threshold does not transport is a description of the past, not of
        the record's practice.
    WF-BOOK    The census nominates no weights, so the price-panel leg is the reference
        the census is placed against, not a candidate: the LIVE RULES v2 baseline and SPY
        on U56 and B136, full sample / H1 / H2 and on the untouched 2017-01-01.. OOS
        window, with BOTH KEEP paths evaluated.  There is no arm to KEEP: the honest
        report is that 4a and 4b are vacuous for a record audit, and the numbers are
        printed so the verdict can be read in the record's own units.

COSTS AND EXECUTION for the WF-BOOK leg are PROTOCOL's: 10 bps per unit turnover,
weights at close t applied at t+1 (engine).  Weekly cadence, the live book's.

OUTPUTS
    .cells.csv.gz     every (file, metric, axis) census row, all of them
    .grid.csv         the full RSTAR x MATCHPREC grid, all points
    .published.csv.gz every published-matched headline with its cells
    .walkforward.csv  WF-CENSUS and WF-BOOK
    .console.txt      this run's stdout
"""
import sys, re, glob, gzip, math, io, os
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, backtest, metrics  # noqa

BT = ROOT / "research" / "backtests"
STEM = BT / "2026-09-09_how-many-of-the-record-s-PUBLISHED-HEADLINE-NUMBERS-are-CADENCE-MEANS_cloud"
SELF = Path(__file__).name

AXES = {
    "cadence": {"cadence", "cad", "freq"},
    "cost":    {"cost", "bps", "cost_bps", "rung", "cost_rung"},
    "seed":    {"seed", "draw", "rep", "replicate"},
    "panel":   {"panel", "universe", "uni"},
}
AXIS_OF = {c: a for a, cs in AXES.items() for c in cs}
METRIC_SUB = ("cagr", "sharpe", "maxdd", "turn", "_pp", "pp_")
METRIC_EXACT = {"h1", "h2", "dd"}
MAX_LEVELS = 20
EPS = 1e-9
RSTAR_GRID = [1.25, 1.5, 2.0, 3.0, 5.0, 10.0]
RSTAR_POINT = 2.0
PREC_GRID = ["2dp", "3dp", "pct1dp", "pct2dp", "ALL"]
PREC_POINT = "3dp"
IS_END = pd.Timestamp("2016-12-31")

tee = io.StringIO()
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); tee.write(s + "\n")

def is_metric(c):
    c = c.strip().lower()
    return c in METRIC_EXACT or any(s in c for s in METRIC_SUB)

# ---------------------------------------------------------------- 1. CENSUS
def census():
    files = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    files = [f for f in files if SELF.replace(".py", "") not in Path(f).name]
    rows, skipped, read_fail = [], 0, 0
    for f in files:
        name = Path(f).name
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            read_fail += 1; continue
        cols = list(head.columns)
        low = {c: c.strip().lower() for c in cols}
        acols = [c for c in cols if low[c] in AXIS_OF]
        mcols = [c for c in cols if is_metric(low[c]) and c not in acols]
        if not acols or not mcols:
            skipped += 1; continue
        try:
            df = pd.read_csv(f, usecols=acols + mcols)
        except Exception:
            read_fail += 1; continue
        if len(df) < 2:
            skipped += 1; continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})_", name)
        fdate = pd.Timestamp(m.group(1)) if m else pd.NaT
        for ac in acols:
            lv = df[ac].dropna()
            k = lv.nunique()
            if k < 2 or k > MAX_LEVELS:
                continue
            for mc in mcols:
                s = pd.to_numeric(df[mc], errors="coerce")
                if s.notna().sum() < 2:
                    continue
                sub = pd.DataFrame({"a": df[ac], "v": s}).dropna()
                g = sub.groupby("a")["v"].mean()
                if g.size < 2:
                    continue
                head_mean = float(sub["v"].mean())
                if abs(head_mean) < 1e-6:
                    continue
                a = g.abs()
                amin, amax = float(a.min()), float(a.max())
                ratio = amax / amin if amin > EPS else float("inf")
                rows.append(dict(
                    file=name, date=fdate, axis=AXIS_OF[low[ac]], axis_col=ac, metric=mc,
                    levels=int(g.size), n_rows=int(len(sub)), headline=head_mean,
                    cell_min=float(g.min()), cell_max=float(g.max()),
                    absmin=amin, absmax=amax, ratio=ratio,
                    signflip=bool(g.max() > 0 and g.min() < 0),
                    cells="|".join(f"{str(i)}={v:.6g}" for i, v in g.items())))
        del df
    return pd.DataFrame(rows), len(files), skipped, read_fail

say("=" * 100)
say("IDEA 577 — census of axis-collapsed headline numbers in the committed record")
say("=" * 100)
cells, n_files, n_skip, n_fail = census()
say(f"corpus: {n_files} committed CSVs scanned; {n_skip} carry no (axis, metric) pair; "
    f"{n_fail} unreadable; {len(cells)} census cells from {cells.file.nunique()} files")
if cells.empty:
    say("EMPTY CENSUS — nothing to report."); sys.exit(1)

fin = cells[np.isfinite(cells.ratio)]
say(f"finite-ratio cells {len(fin)} ({len(cells)-len(fin)} have a zero-valued level, ratio=inf)")
say("\nB1  COLLAPSE RATE at every RSTAR (all grid points, no selection):")
for r in RSTAR_GRID:
    hit = (cells.ratio > r).sum()
    say(f"   RSTAR={r:5.2f}   {hit:6d}/{len(cells)} cells = {hit/len(cells):6.1%}   "
        f"files {cells[cells.ratio>r].file.nunique():4d}/{cells.file.nunique()}")
say(f"\nB2  SIGN FLIP: {cells.signflip.sum()}/{len(cells)} = {cells.signflip.mean():.1%} of cells "
    f"have levels of OPPOSITE SIGN ({cells[cells.signflip].file.nunique()} files)")
say("\nBY AXIS at the point RSTAR=2.0 (reporting axis, never selected on):")
for ax in ["cadence", "cost", "seed", "panel"]:
    d = cells[cells.axis == ax]
    if d.empty:
        say(f"   {ax:8s}  no cells"); continue
    say(f"   {ax:8s}  cells {len(d):6d}  >2x {(d.ratio>2).mean():6.1%}  signflip {d.signflip.mean():6.1%}  "
        f"median ratio {d.ratio.replace(np.inf,np.nan).median():.3f}")
say("\nBY METRIC FAMILY at RSTAR=2.0:")
def fam(m):
    m = m.lower()
    for k in ("sharpe", "cagr", "maxdd", "turn"):
        if k in m: return k
    return "other"
cells["fam"] = cells.metric.map(fam)
for k, d in cells.groupby("fam"):
    say(f"   {k:8s}  cells {len(d):6d}  >2x {(d.ratio>2).mean():6.1%}  signflip {d.signflip.mean():6.1%}")

# ------------------------------------------------- 2. PUBLISHED-SURFACE LEG
PUB = (ROOT / "research" / "LEADERBOARD.md").read_text() + "\n" + (ROOT / "research" / "CHANGELOG.md").read_text()
def renders(h, prec):
    out = []
    if prec in ("2dp", "ALL"):    out.append(f"{abs(h):.2f}")
    if prec in ("3dp", "ALL"):    out.append(f"{abs(h):.3f}")
    if prec in ("pct1dp", "ALL"): out.append(f"{abs(h)*100:.1f}")
    if prec in ("pct2dp", "ALL"): out.append(f"{abs(h)*100:.2f}")
    return out
def present(tok):
    return re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", PUB) is not None

say("\n" + "-" * 100)
say("B3  PUBLISHED SUBSET — headline renderings that literally occur in LEADERBOARD.md + CHANGELOG.md")
say("    UPPER BOUND: a rendering can occur for reasons unrelated to the file that produced it.")
tok_cache = {}
grid_rows, pub_rows = [], []
for prec in PREC_GRID:
    toks = cells.headline.map(lambda h: renders(h, prec))
    matched = toks.map(lambda ts: any(tok_cache.setdefault(t, present(t)) for t in ts))
    d = cells[matched]
    # collision: how many distinct census cells share a rendering
    flat = [t for ts in toks[matched] for t in ts if tok_cache[t]]
    coll = len(flat) / max(1, len(set(flat)))
    for r in RSTAR_GRID:
        grid_rows.append(dict(prec=prec, rstar=r,
                              corpus_cells=len(cells), corpus_gt=int((cells.ratio > r).sum()),
                              corpus_rate=float((cells.ratio > r).mean()),
                              pub_cells=len(d), pub_gt=int((d.ratio > r).sum()),
                              pub_rate=float((d.ratio > r).mean()) if len(d) else np.nan,
                              pub_signflip=float(d.signflip.mean()) if len(d) else np.nan,
                              collision=coll))
    say(f"   prec={prec:7s} matched {len(d):6d}/{len(cells)} cells ({len(d)/len(cells):5.1%}) "
        f"from {d.file.nunique():4d} files | >2x {(d.ratio>2).mean() if len(d) else float('nan'):6.1%} "
        f"(corpus {(cells.ratio>2).mean():6.1%}) | signflip {d.signflip.mean() if len(d) else float('nan'):6.1%} "
        f"| renderings/distinct {coll:.2f}")
    if prec == PREC_POINT:
        pub_rows = d.copy()
grid = pd.DataFrame(grid_rows)

# ------------------------------------------------------- 3. WF-CENSUS (rule 8)
say("\n" + "-" * 100)
say("WF-CENSUS (PROTOCOL 8) — RSTAR chosen on IS-dated files alone, OOS half read ONCE")
dated = cells[cells.date.notna()].copy()
cut = dated.date.median()
IS, OOS = dated[dated.date <= cut], dated[dated.date > cut]
say(f"   split at the median commit date {cut.date()}: IS {len(IS)} cells / {IS.file.nunique()} files, "
    f"OOS {len(OOS)} cells / {OOS.file.nunique()} files")
pick, wf_rows = None, []
for r in RSTAR_GRID:
    isr, oosr = float((IS.ratio > r).mean()), float((OOS.ratio > r).mean())
    wf_rows.append(dict(leg="WF-CENSUS", rstar=r, is_rate=isr, oos_rate=oosr,
                        is_cells=len(IS), oos_cells=len(OOS)))
    say(f"   RSTAR={r:5.2f}  IS rate {isr:6.1%}   OOS rate {oosr:6.1%}   delta {oosr-isr:+6.1%}")
    if pick is None and isr <= 0.20:
        pick = r
say(f"   IS-CHOSEN RSTAR* = {pick} (smallest grid value with IS rate <= 20%)")
if pick is not None:
    isr, oosr = float((IS.ratio > pick).mean()), float((OOS.ratio > pick).mean())
    say(f"   READ ONCE: OOS flag rate at RSTAR*={pick} is {oosr:.1%} vs IS {isr:.1%} "
        f"({'TRANSPORTS' if abs(oosr-isr) <= 0.10 else 'DOES NOT TRANSPORT'}, bar |delta| <= 10 pp)")

# --------------------------------------------------------- 4. WF-BOOK anchor
say("\n" + "-" * 100)
say("WF-BOOK — the census nominates NO weights.  Reference book (live RULES v2) and SPY,")
say("          10 bps, weekly, next-day execution; full / H1 / H2 and the untouched OOS window.")
def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = r.loc["2017-01-01":]
    mo = metrics(o)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
book_rows = []
for pname, kw in [("U56", {}), ("B136", dict(broad=True))]:
    px = load_universe(**kw)
    start = px.index[260]
    v2 = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    for nm, r in [("RULES v2 (live)", v2), ("RULES v1", v1), ("SPY", spy)]:
        book_rows.append(dict(panel=pname, book=nm, **legs(r)))
book = pd.DataFrame(book_rows)
say(book.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
for pname in ["U56", "B136"]:
    b = book[(book.panel == pname) & (book.book == "RULES v2 (live)")].iloc[0]
    s = book[(book.panel == pname) & (book.book == "SPY")].iloc[0]
    p4b = (b.H1 > s.H1) and (b.H2 > s.H2) and (b.OOS_Sharpe > s.OOS_Sharpe) \
          and (b.MaxDD >= 0.60 * s.MaxDD) and (b.CAGR >= 0.70 * s.CAGR)
    say(f"   {pname}: reference book 4b legs — H1 {b.H1:.3f}>{s.H1:.3f} {b.H1>s.H1}, "
        f"H2 {b.H2:.3f}>{s.H2:.3f} {b.H2>s.H2}, OOS {b.OOS_Sharpe:.3f}>{s.OOS_Sharpe:.3f} {b.OOS_Sharpe>s.OOS_Sharpe}, "
        f"DD {b.MaxDD:.3f} vs 0.6*SPY {0.6*s.MaxDD:.3f} {b.MaxDD>=0.6*s.MaxDD}, "
        f"CAGR {b.CAGR:.3f} vs 0.7*SPY {0.7*s.CAGR:.3f} {b.CAGR>=0.7*s.CAGR} -> 4b {p4b}")
say("   4a and 4b are VACUOUS for this idea: a record audit nominates no arm, so no KEEP is "
    "available on either path and none is claimed.")

# --------------------------------------------------------------- 5. EXEMPLAR
say("\n" + "-" * 100)
say("EXEMPLAR — the ten worst collapsed headlines in the record (by ratio, finite):")
worst = fin.sort_values("ratio", ascending=False).head(10)
for _, w in worst.iterrows():
    say(f"   {w.ratio:9.2f}x  {w.axis:7s} {w.metric:14s} headline {w.headline:+.5g}  cells [{w.cells[:110]}]")
    say(f"              {w.file}")
say("\nIDEA 314's OWN EXEMPLAR — rows whose file is idea 51R / 314's vol-cap work:")
ex = cells[cells.file.str.contains("vol-cap|51R|universe-clause", case=False, regex=True)]
if len(ex):
    e = ex.sort_values("ratio", ascending=False).head(6)
    for _, w in e.iterrows():
        say(f"   {w.ratio:9.2f}x  {w.axis:7s} {w.metric:14s} headline {w.headline:+.5g}  cells [{w.cells[:110]}]")
        say(f"              {w.file}")
else:
    say("   (no matching file in the corpus)")

# ----------------------------------------------------------------- 6. WRITE
cells.drop(columns=["fam"]).to_csv(str(STEM) + ".cells.csv.gz", index=False)
grid.to_csv(STEM.with_suffix(".grid.csv"), index=False)
(pub_rows if isinstance(pub_rows, pd.DataFrame) else pd.DataFrame()).to_csv(str(STEM) + ".published.csv.gz", index=False)
wf = pd.concat([pd.DataFrame(wf_rows), book.assign(leg="WF-BOOK")], ignore_index=True)
wf.to_csv(STEM.with_suffix(".walkforward.csv"), index=False)
STEM.with_suffix(".console.txt").write_text(tee.getvalue())
print("wrote", STEM.name + ".{cells.csv.gz,grid.csv,published.csv.gz,walkforward.csv}/.console.txt")
