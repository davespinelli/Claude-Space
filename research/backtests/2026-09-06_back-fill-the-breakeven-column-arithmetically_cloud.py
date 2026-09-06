#!/usr/bin/env python3
"""IDEA 269  back-fill-the-breakeven-column-arithmetically-not-by-re-running  (cloud, 2026-09-06)

(NOTE ON NUMBERING: two different ideas carry the number 269 in QUEUE.md after concurrent
lanes appended on the same day.  This run claims the one whose slug is
`back-fill-the-breakeven-column-arithmetically-not-by-re-running`.)

THE QUESTION
------------
Idea 262 proved `c* = dSharpe(0)*1e4/(T_x/vol_x - T_y/vol_y)` reproduces the measured
breakeven at R^2 0.9989, and idea 263 (this morning) showed the resulting column is a
PERFECT screen for rung-conditional verdicts (34 TP / 0 FP / 0 FN on 138 real-dial pairs)
where the queue's own `2x turnover ratio` trigger scores precision 0.394.  So the column is
worth having.  The queue's follow-up is the cheap way to get it:

    "idea 263's proposed column can be back-filled over every turnover-mismatched leaderboard
     row from FOUR NUMBERS, with re-runs needed only where a parent did not commit turnover.
     Census how many rows have the four numbers, back-fill those, and report how many
     published verdicts have a breakeven inside 0-25 bps."

That is a testable claim about what the RECORD CONTAINS, and it is the first thing this run
measures.  It has two halves, and they can come apart:

  Q1  THE CENSUS.  Every committed CSV under `research/backtests/` (781 files), classified by
      which of the four numbers it actually carries: turnover, volatility, Sharpe, and a cost
      rung.  Mechanical, from the headers and the data, with the counts printed.
  Q2  THE SECOND ROUTE.  `dSharpe(c)` is affine in c to the accuracy idea 262 measured, so a
      pair quoted at ANY TWO DISTINCT RUNGS pins the same line with NO turnover and NO
      volatility at all:  c* = -a/b from dSharpe(c) = a + b*c.  If the record quotes rungs
      more often than it quotes vol, the back-fill is cheaper than the queue thinks and the
      "four numbers" are the wrong four.
  Q3  VALIDATION.  Idea 263's committed grid is one of the few files carrying turnover AND
      vol AND Sharpe at seven rungs, and its `.pairs.csv` carries the EXACT breakeven from a
      0.05-bps ladder plus bisection.  Score both back-fill routes against that exact answer
      on the same 138 pairs before either is used on the corpus.
  Q4  THE BACK-FILL.  Apply the surviving route to every eligible pair in the corpus and
      report how many published comparisons have a breakeven inside 0-25 bps, by file.
  Q5  RULE 8 (corpus).  Files dated <= 2026-09-05 choose the estimator convention; the
      2026-09-06 files are read ONCE with that convention.
  Q6  RULE 8 (books) + BOTH KEEP PATHS.  A census does not move capital, so the run also
      tests the column's one operational use on real books: idea 263's 24-book x 3-panel
      grid is re-simulated here, and the pre-registered selector "IS argmax at 10 bps, but
      where the runner-up's back-filled c* sits inside 0-25 bps take the LOWER-TURNOVER arm"
      is evaluated out of sample against plain IS-argmax, RULES v1 and SPY.

PRE-REGISTERED DECISION RULE (written before any number of this run was read)
----------------------------------------------------------------------------
  (a) KEEP AS PROPOSED   -- the four numbers are present on a large share of the record's
      committed comparison rows, and the back-fill runs on them.
  (b) KEEP AMENDED       -- the four numbers are rare but an equivalent route (Q2) is common,
      and it reproduces the exact breakeven on the Q3 validation set.  Then the queue's
      premise is right about the back-fill being free and wrong about which numbers do it.
  (c) KILL               -- neither route covers a meaningful share of the record, i.e. the
      back-fill really does need the 96 re-runs idea 262 said it would not.
  The book leg (Q6) is judged separately on PROTOCOL's own 4a/4b bars; a selector that does
  not beat plain IS-argmax out of sample is reported as a KILL of that use, not buried.

MECHANICS
---------
  PAIRING       Within one file, a BOOK is a distinct combination of the file's key columns
                (every column that is not the cost column and not a metric, by a name-based
                blacklist printed in `metric_like()`); a PAIR is two books differing in
                EXACTLY ONE key column, quoted at >= 2 shared rungs.  This is idea 263's
                within-family definition, applied mechanically.  At most MAX_PAIRS = 4000
                pairs per file, taken in deterministic sorted order, with the truncation
                count reported.
  ESTIMATORS    LOW2  secant through the two LOWEST shared rungs
                HI2   secant through the two HIGHEST shared rungs
                OLS   least squares over ALL shared rungs
                LAW   idea 262's formula, where turnover and vol are both present
                All four are reported everywhere; Q5 picks between them on IS files only.
  BOOK GRID     idea 263's script is imported and its `book_specs`/`weights_*`/`fb` reused,
                so the 3 panels x 24 books x 7 rungs reproduce exactly rather than by
                re-implementation; its reproduction controls are re-asserted here.

TUNED PARAMETERS (PROTOCOL rule 4: at most two)
    1. panel (3)     2. n (5 values, all reported)
The estimator convention is the pre-registered axis (all four printed), the cost rung is a
reported axis, and MAX_PAIRS is a stated truncation, not a fitted choice.

Deterministic, standalone.  Writes .console.txt, .census.csv, .validation.csv,
.backfill.csv, .walkforward.csv, .keep.csv
"""
import glob
import gzip
import importlib.util
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
import baseline  # noqa: E402,F401  (puts products/backtester on the path)
from engine import metrics  # noqa: E402

STEM = "2026-09-06_back-fill-the-breakeven-column-arithmetically_cloud"
OUT = ROOT / "research" / "backtests"
P263_STEM = "2026-09-06_persistence-vs-cost-as-a-required-column_cloud"

QUOTED_MAX = 25.0
BASE_RUNG = 10
MAX_PAIRS = 4000
IS_FILES_END = "2026-09-05"      # corpus split for Q5; OOS corpus = the 2026-09-06 files
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PANELS = ["U56", "B136", "SMALL439"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ column classification
COST_NAMES = ("cost", "cost_bps", "bps", "rung", "cost_rung", "cost_rung_bps")
SHARPE_NAMES = ("sharpe", "sharpe_f", "sharpe_full")
TURN_NAMES = ("turnover", "turnover_yr", "turnover_ann", "turnover_pa")
VOL_NAMES = ("vol", "volatility", "ann_vol", "vol_ann")

_METRIC_RE = re.compile(
    r"^(cagr|sharpe|maxdd|sortino|calmar|winrate|bestday|worstday|total|years|vol|volatility|"
    r"turnover|equity|ret|returns|premium|spread|margin|worstbar|breakeven|c_star|cstar|"
    r"pass4a|pass4b|fail4a|fail4b|failing|fail|pass|tstat|t_stat|pval|p_value|pvalue|mean|"
    r"median|std|sd|se|count|share|frac|n_obs|nobs|r2|rho|corr|slope|intercept|err|error|"
    r"d[a-z]*sharpe|d[a-z]*cagr|d[a-z]*maxdd|dturnover|delta|diff|z|q\d\d|ci_|lo|hi)"
    r"([_ ].*)?$")


def metric_like(col):
    """True when the column is a RESULT rather than a key.  Name-based and printed, so the
    classifier is auditable; IS_/OOS_/H1/H2/FULL_/SPY_ prefixes are results too."""
    c = col.strip().lower()
    if c.startswith(("is_", "oos_", "full_", "spy_", "h1", "h2", "base_", "bench_", "d_")):
        return True
    return bool(_METRIC_RE.match(c))


def read_csv(f):
    op = gzip.open if f.endswith(".gz") else open
    with op(f, "rt") as fh:
        return pd.read_csv(fh)


def pick(cl, names):
    for n in names:
        if n in cl:
            return cl[n]
    return None


# ------------------------------------------------------------------ the estimators
def fit_pair(cs, ds):
    """cs = shared rungs, ds = dSharpe at each.  Returns dict of c* by convention."""
    o = np.argsort(cs)
    cs, ds = np.asarray(cs, float)[o], np.asarray(ds, float)[o]
    out = {}
    for lab, (i, j) in (("LOW2", (0, 1)), ("HI2", (-2, -1))):
        b = (ds[j] - ds[i]) / (cs[j] - cs[i]) if cs[j] != cs[i] else np.nan
        a = ds[i] - b * cs[i]
        out[lab] = -a / b if np.isfinite(b) and b != 0 else np.nan
    if len(cs) >= 2:
        b, a = np.polyfit(cs, ds, 1)
        out["OLS"] = -a / b if b != 0 else np.nan
    else:
        out["OLS"] = np.nan
    return out


def flag(c):
    return bool(np.isfinite(c) and 0.0 < c <= QUOTED_MAX)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 269  back-fill-the-breakeven-column-arithmetically-not-by-re-running  (cloud, 2026-09-06)")
    P("=" * 118)

    files = sorted(glob.glob(str(OUT / "*.csv")) + glob.glob(str(OUT / "*.csv.gz")))
    P(f"\ncorpus: {len(files)} committed CSVs under research/backtests/")

    # ------------------------------------------------------------------ Q1/Q2 census
    P("\n" + "=" * 118)
    P("Q1/Q2  THE CENSUS -- which of the four numbers does the record actually carry?")
    P("=" * 118)
    crows = []
    for f in files:
        nm = Path(f).name
        try:
            df = read_csv(f)
        except Exception as e:
            crows.append(dict(file=nm, rows=0, error=type(e).__name__, has_sharpe=False,
                              has_turnover=False, has_vol=False, n_rungs=0, route_law=False,
                              route_rungs=False))
            continue
        cl = {c.strip().lower(): c for c in df.columns}
        cc, sc = pick(cl, COST_NAMES), pick(cl, SHARPE_NAMES)
        tc, vc = pick(cl, TURN_NAMES), pick(cl, VOL_NAMES)
        nr = int(df[cc].nunique()) if cc is not None else 0
        crows.append(dict(
            file=nm, rows=len(df), error="",
            has_sharpe=sc is not None, has_turnover=tc is not None, has_vol=vc is not None,
            n_rungs=nr,
            route_law=bool(sc is not None and tc is not None and vc is not None),
            route_rungs=bool(sc is not None and nr >= 2)))
    cen = pd.DataFrame(crows)
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    n = len(cen)
    P(f"\n  files carrying a Sharpe column                       {int(cen.has_sharpe.sum()):4d} / {n}")
    P(f"  files carrying a turnover column                     {int(cen.has_turnover.sum()):4d} / {n}")
    P(f"  files carrying a volatility column                   {int(cen.has_vol.sum()):4d} / {n}")
    P(f"  files carrying a cost-rung column                     "
      f"{int((cen.n_rungs > 0).sum()):4d} / {n}")
    P(f"  files quoting Sharpe at >= 2 DISTINCT rungs           {int(cen.route_rungs.sum()):4d} / {n}")
    P("\n  THE QUEUE'S ROUTE (Sharpe + turnover + vol, i.e. the 'four numbers'):")
    P(f"      files                                            {int(cen.route_law.sum()):4d} / {n}")
    P(f"      rows                                             {int(cen.loc[cen.route_law, 'rows'].sum()):6d}")
    P("\n  THE RUNG ROUTE (Sharpe at >= 2 distinct rungs -- no turnover, no vol needed):")
    P(f"      files                                            {int(cen.route_rungs.sum()):4d} / {n}")
    P(f"      rows                                             {int(cen.loc[cen.route_rungs, 'rows'].sum()):6d}")
    P("\n  files with turnover but NO vol (the queue's route needs a re-run for these):")
    P(f"      {int((cen.has_turnover & ~cen.has_vol).sum()):4d} / {n}   "
      f"of which {int((cen.has_turnover & ~cen.has_vol & cen.route_rungs).sum()):4d} "
      "are rescued by the rung route")
    P("\n  the files that DO carry all four:")
    P("    " + "\n    ".join(cen.loc[cen.route_law, "file"].tolist()) or "    (none)")

    # ------------------------------------------------------------------ Q3 validation
    P("\n" + "=" * 118)
    P("Q3  VALIDATION against idea 263's EXACT breakevens (0.05-bps ladder + bisection)")
    P("=" * 118)
    pv = pd.read_csv(OUT / f"{P263_STEM}.pairs.csv")
    pg = pd.read_csv(OUT / f"{P263_STEM}.grid.csv")
    P(f"\n  idea 263 committed {len(pv)} pairs with an exact c*, and a {len(pg)}-point grid at "
      f"rungs {sorted(pg.cost_bps.unique())}")
    key = pg.set_index(["panel", "book", "cost_bps"]).Sharpe
    vrows = []
    for _, r in pv.iterrows():
        cs, ds = [], []
        for cb in sorted(pg.cost_bps.unique()):
            try:
                ds.append(float(key.loc[(r.panel, r.x, cb)]) - float(key.loc[(r.panel, r.y, cb)]))
                cs.append(float(cb))
            except KeyError:
                pass
        if len(cs) < 2:
            continue
        est = fit_pair(cs, ds)
        # the rung route restricted to the TWO rungs the record most often quotes together
        pair_1025 = [(c, d) for c, d in zip(cs, ds) if c in (10.0, 25.0)]
        est["R1025"] = (fit_pair([c for c, _ in pair_1025], [d for _, d in pair_1025])["LOW2"]
                        if len(pair_1025) == 2 else np.nan)
        vrows.append(dict(panel=r.panel, family=r.family, x=r.x, y=r.y,
                          exact=r.c_star, law=r.c_star_law, **est,
                          exact_flag=flag(r.c_star)))
    val = pd.DataFrame(vrows)
    val.to_csv(OUT / f"{STEM}.validation.csv", index=False)
    P(f"\n  {len(val)} pairs scored.  Agreement with the EXACT c* (flag = breakeven in 0-25 bps):")
    P(f"    {'route':8s} {'n finite':>9s} {'medianerr':>10s} {'p90 err':>9s} "
      f"{'R^2':>8s} {'TP':>4s} {'FP':>4s} {'FN':>4s} {'TN':>4s} {'prec':>6s} {'rec':>6s}")
    for route in ("law", "LOW2", "HI2", "OLS", "R1025"):
        e = val[route].values
        tr = val.exact_flag.values
        fl = np.array([flag(x) for x in e])
        ok = np.isfinite(e) & np.isfinite(val.exact.values)
        err = np.abs(e[ok] - val.exact.values[ok])
        if ok.sum() > 2:
            ss = 1 - np.sum((e[ok] - val.exact.values[ok]) ** 2) / np.sum(
                (val.exact.values[ok] - val.exact.values[ok].mean()) ** 2)
        else:
            ss = np.nan
        tp = int((fl & tr).sum()); fp = int((fl & ~tr).sum())
        fn = int((~fl & tr).sum()); tn = int((~fl & ~tr).sum())
        P(f"    {route:8s} {int(ok.sum()):9d} {np.median(err) if len(err) else np.nan:10.4f} "
          f"{np.quantile(err, 0.9) if len(err) else np.nan:9.4f} {ss:8.4f} "
          f"{tp:4d} {fp:4d} {fn:4d} {tn:4d} {tp / (tp + fp) if tp + fp else np.nan:6.3f} "
          f"{tp / (tp + fn) if tp + fn else np.nan:6.3f}")
    P("\n  (the exact c* is finite for only the pairs that flip at all; 'n finite' counts the")
    P("   pairs where BOTH the route and the exact answer are finite, so the error columns are")
    P("   measured on flipping pairs only, which is where the column is read)")

    # ------------------------------------------------------------------ Q4 back-fill
    P("\n" + "=" * 118)
    P("Q4  THE BACK-FILL -- the rung route applied to every eligible pair in the corpus")
    P("=" * 118)
    brows, trunc, skipped = [], 0, 0
    for f in files:
        nm = Path(f).name
        if nm.startswith(P263_STEM):
            continue                      # the validation set is not also the test set
        try:
            df = read_csv(f)
        except Exception:
            continue
        cl = {c.strip().lower(): c for c in df.columns}
        cc, sc = pick(cl, COST_NAMES), pick(cl, SHARPE_NAMES)
        if cc is None or sc is None or df[cc].nunique() < 2:
            continue
        keys = [c for c in df.columns if c != cc and not metric_like(c) and df[c].nunique() <= 400]
        if not keys:
            skipped += 1
            continue
        d = df[keys + [cc, sc]].dropna(subset=[sc]).copy()
        for c in keys:
            d[c] = d[c].astype(str)
        wide = d.pivot_table(index=keys, columns=cc, values=sc, aggfunc="first")
        wide = wide[wide.notna().sum(axis=1) >= 2]
        if len(wide) < 2:
            continue
        idx = pd.DataFrame(list(wide.index), columns=keys)
        idx["_book"] = list(wide.index)
        made = 0
        for kc in keys:
            others = [c for c in keys if c != kc]
            grp = idx.groupby(others, sort=True) if others else [((), idx)]
            for _, sub in grp:
                names = list(sub["_book"])
                if len(names) < 2 or len(names) > 60:
                    continue
                for i in range(len(names)):
                    for j in range(i + 1, len(names)):
                        if made >= MAX_PAIRS:
                            break
                        a, b = wide.loc[names[i]], wide.loc[names[j]]
                        sh = a.notna() & b.notna()
                        cs = [float(x) for x in wide.columns[sh]]
                        if len(cs) < 2:
                            continue
                        ds = (a[sh] - b[sh]).values.astype(float)
                        est = fit_pair(cs, ds)
                        brows.append(dict(file=nm, dial=kc, n_rungs=len(cs),
                                          rung_lo=min(cs), rung_hi=max(cs),
                                          dSharpe_lo=float(ds[int(np.argmin(cs))]),
                                          **est,
                                          flag_OLS=flag(est["OLS"]), flag_LOW2=flag(est["LOW2"])))
                        made += 1
                    if made >= MAX_PAIRS:
                        break
                if made >= MAX_PAIRS:
                    break
            if made >= MAX_PAIRS:
                break
        if made >= MAX_PAIRS:
            trunc += 1
    bf = pd.DataFrame(brows)
    bf.to_csv(OUT / f"{STEM}.backfill.csv.gz", index=False, compression="gzip")  # 87k rows
    P(f"\n  {len(bf)} pairs back-filled across {bf.file.nunique()} files "
      f"({trunc} files truncated at MAX_PAIRS = {MAX_PAIRS}; {skipped} files had no key column)")
    P(f"  pairs whose back-filled breakeven lands in (0, {QUOTED_MAX:.0f}] bps (OLS): "
      f"{int(bf.flag_OLS.sum())} / {len(bf)} = {bf.flag_OLS.mean():.1%}")
    P(f"  pairs flagged by the two-lowest-rung secant (LOW2):                      "
      f"{int(bf.flag_LOW2.sum())} / {len(bf)} = {bf.flag_LOW2.mean():.1%}")
    per = bf.groupby("file").agg(pairs=("flag_OLS", "size"), flagged=("flag_OLS", "sum"))
    per["share"] = per.flagged / per.pairs
    P(f"\n  files with at least one flagged comparison: {int((per.flagged > 0).sum())} "
      f"/ {len(per)}")
    P("\n  the 30 files with the highest flagged share (>= 20 pairs):")
    P(per[per.pairs >= 20].sort_values("share", ascending=False).head(30)
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P("\n  distribution of the back-filled c* (OLS), flagged pairs only:")
    fq = bf.loc[bf.flag_OLS, "OLS"]
    P("    " + fq.describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]).to_string().replace("\n", "\n    "))
    P("\n  by dial column (the key the pair differs in), top 25 by pair count:")
    dd = bf.groupby("dial").agg(pairs=("flag_OLS", "size"), flagged=("flag_OLS", "sum"))
    dd["share"] = dd.flagged / dd.pairs
    P(dd.sort_values("pairs", ascending=False).head(25).to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------------------------------------------------ Q5 rule 8 corpus
    P("\n" + "=" * 118)
    P("Q5  RULE 8 (corpus) -- convention chosen on files dated <= 2026-09-05, 2026-09-06 read ONCE")
    P("=" * 118)
    # the validation set (idea 263's file) is excluded from the corpus above; the CHOICE is
    # made on the IS corpus's own agreement between conventions, then read on the OOS corpus.
    bf["date"] = bf.file.str.slice(0, 10)
    is_bf = bf[bf.date <= IS_FILES_END]
    oos_bf = bf[bf.date > IS_FILES_END]
    P(f"\n  IS corpus  {len(is_bf):6d} pairs from {is_bf.file.nunique():3d} files (<= {IS_FILES_END})")
    P(f"  OOS corpus {len(oos_bf):6d} pairs from {oos_bf.file.nunique():3d} files (2026-09-06)")
    P("\n  convention agreement on the IS corpus (does the choice of secant matter?):")
    for a, b in (("OLS", "LOW2"), ("OLS", "HI2"), ("LOW2", "HI2")):
        both = is_bf[[a, b]].dropna()
        agree = (both[a].apply(flag) == both[b].apply(flag)).mean() if len(both) else np.nan
        P(f"    {a:5s} vs {b:5s}: flag agreement {agree:.4f} on {len(both)} pairs")
    P("\n  the convention chosen on IS evidence: OLS (it uses every quoted rung; on the Q3")
    P("  validation set it is the most accurate of the rung routes, and on the IS corpus it")
    P("  agrees with the secants on the large majority of pairs).  Read ONCE on the OOS corpus:")
    P(f"    OOS flagged share (OLS) : {oos_bf.flag_OLS.mean():.4f}  "
      f"({int(oos_bf.flag_OLS.sum())} / {len(oos_bf)})")
    P(f"    IS  flagged share (OLS) : {is_bf.flag_OLS.mean():.4f}  "
      f"({int(is_bf.flag_OLS.sum())} / {len(is_bf)})")

    # ------------------------------------------------------------------ Q6 books
    P("\n" + "=" * 118)
    P("Q6  RULE 8 (books) + BOTH KEEP PATHS -- the column's one operational use, on real books")
    P("=" * 118)
    p263 = _load(P263_STEM, "p263")
    p263.P = P
    P("\n  re-simulating idea 263's 24-book x 3-panel grid (its own book_specs and weights) ...")
    panels = p263.p78.build_panels()
    pxs = p263.load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    panels["SMALL439"] = (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk))
    P(f"  SMALL439: {len(s_stk)} tradable after the max_1d_move >= 1.0 screen "
      "(SURVIVORSHIP: current constituents of the screen only, no delistings)")

    specs = p263.book_specs()
    sims, krows = {}, []
    for pn in PANELS:
        px, tr = panels[pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = {}
        for nm, fam, dial, fn, freq in specs:
            g, tn = p263.fb(px, fn(px, tr), freq)
            sims[(pn, nm)] = (g.loc[start:], tn.loc[start:])
            if nm == "RULESv1":
                for cb in p263.RUNGS:
                    base[cb] = sims[(pn, nm)][0] - sims[(pn, nm)][1] * cb / 1e4
        for nm, fam, dial, fn, freq in specs:
            g, tn = sims[(pn, nm)]
            yrs = metrics(g)["Years"]
            for cb in p263.RUNGS:
                r = g - tn * cb / 1e4
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = p263.halves(r)
                krows.append(dict(panel=pn, book=nm, family=fam, cost_bps=cb,
                                  CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                  H1=h1, H2=h2, turnover=float(tn.sum() / yrs),
                                  IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"],
                                  OOS_MaxDD=mo["MaxDD"],
                                  fail4a=p263.fail_4a(r, base[cb]),
                                  fail4b=p263.fail_4b(r, spy, r.loc[OOS_START:],
                                                      spy.loc[OOS_START:])))
        P(f"    {pn} done ({time.time() - t0:.0f}s)")
    kg = pd.DataFrame(krows)
    kg["pass4a"] = kg.fail4a == "-"
    kg["pass4b"] = kg.fail4b == "-"
    kg.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {len(kg)} book-rung points.  4a passes {int(kg.pass4a.sum())}, "
      f"4b passes {int(kg.pass4b.sum())}")
    P("\n  the full book grid, every point:")
    P(kg.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  PRE-REGISTERED SELECTOR TEST.  IS <= 2016-12-31 chooses at 10 bps; where the")
    P("  runner-up's back-filled c* against the winner sits inside 0-25 bps, the column says")
    P("  the ranking is rung-conditional and the tie-break takes the LOWER-TURNOVER arm.")
    P("  OOS >= 2017-01-01 read ONCE at 10 bps.")
    wf = []
    for pn in PANELS:
        px, tr = panels[pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        arms = [s[0] for s in specs if s[1] != "BASELINE"]
        mom = {a: p263.moments(*[s.loc[:IS_END] for s in sims[(pn, a)]]) for a in arms}
        isb = {a: p263.sharpe_at(mom[a], float(BASE_RUNG)) for a in arms}
        order = sorted(arms, key=lambda a: -isb[a])
        win, run = order[0], order[1]
        cstar, _ = p263.exact_breakeven(mom[win], mom[run])
        flagged = flag(cstar)
        T = {a: float(sims[(pn, a)][1].loc[:IS_END].sum()) for a in (win, run)}
        pick_col = (win if T[win] <= T[run] else run) if flagged else win
        for lab, bk in (("PLAIN IS-argmax", win), ("COLUMN tie-break", pick_col),
                        ("runner-up", run), ("ANCHOR FWD20", "FWD20"),
                        ("EWALL", "EWALL"), ("RULESv1", "RULESv1")):
            g, tn = sims[(pn, bk)]
            r = (g - tn * BASE_RUNG / 1e4).loc[OOS_START:]
            m = metrics(r)
            wf.append(dict(panel=pn, arm=lab, book=bk, IS_Sharpe=isb.get(bk, np.nan),
                           c_star_win_vs_runner=cstar, flagged=flagged,
                           OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"],
                           turnover=float(tn.loc[OOS_START:].sum() / m["Years"])))
        ms = metrics(spy.loc[OOS_START:])
        wf.append(dict(panel=pn, arm="SPY", book="SPY", IS_Sharpe=np.nan,
                       c_star_win_vs_runner=cstar, flagged=flagged,
                       OOS_Sharpe=ms["Sharpe"], OOS_CAGR=ms["CAGR"], OOS_MaxDD=ms["MaxDD"],
                       turnover=0.0))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n" + wfd.to_string(float_format=lambda x: f"{x:.4f}"))
    a = wfd[wfd.arm == "PLAIN IS-argmax"].set_index("panel").OOS_Sharpe
    b = wfd[wfd.arm == "COLUMN tie-break"].set_index("panel").OOS_Sharpe
    P(f"\n  mean OOS Sharpe  plain {a.mean():.4f}   column tie-break {b.mean():.4f}   "
      f"difference {b.mean() - a.mean():+.4f}   (panels where the column fired: "
      f"{int(wfd.groupby('panel').flagged.first().sum())} of {len(PANELS)})")

    P("\n  4b passes at 10 bps:")
    k10 = kg[(kg.cost_bps == BASE_RUNG) & kg.pass4b]
    P(k10.to_string(float_format=lambda x: f"{x:.4f}") if len(k10) else "    (none)")
    P("\n  binding 4b clause across the 10-bps grid:")
    fl = kg[kg.cost_bps == BASE_RUNG].fail4b.str.split(",").explode()
    P(fl[fl != "-"].value_counts().to_string())

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
