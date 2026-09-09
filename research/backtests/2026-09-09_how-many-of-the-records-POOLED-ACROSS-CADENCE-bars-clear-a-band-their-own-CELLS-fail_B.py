#!/usr/bin/env python3
"""Idea 553 - "how-many-of-the-record-s-POOLED-ACROSS-CADENCE-bars-clear-a-band-their-own-CELLS-fail"
(lane B, 2026-09-09).

The question
------------
Idea 551 pooled the MA gate's timing residual over the WHOLE cadence dial (D, W, M, Q, A) and
read -0.2852 pp/yr, which sits inside idea 300's pre-registered band [-0.70, -0.20] and so
PASSES it - while, the queue says, "its own D and A cells fail it".  A bar cleared by a pooled
mean and failed by its own levels is a Simpson's-paradox bar: the verdict it publishes is a
property of the POOLING, not of the quantity.

(G3 below tests that premise as literally stated and it FAILS: pooled over the three panels the
DAILY level is -0.2438, INSIDE the band; only ANNUAL is outside.  The queue's "D and A" is idea
551's SMALL439 ROW - a panel x cadence statement quoted as a cadence statement.  The gate is
reported as it falls and the granularity ladder below is the answer that replaces it.)

The queue asks the census question:

    (a) how many of the record's pre-registered bars are applied to a mean POOLED OVER A DIAL?
    (b) re-applied at each LEVEL of that dial, how many of those pooled PASSes are level FAILs?

and, because (a) is answerable only for bars whose cells survive in a committed artefact, the
run also prices the general version on the record's own grids:

    (c) BASE RATE.  Over every committed artefact CSV that tabulates a statistic against a dial,
        take a bar written the way this record writes them - centred on the pooled mean, half-width
        k standard deviations of the pooled cells - and ask how often at least one LEVEL mean
        falls outside it.  The pooled PASS is true BY CONSTRUCTION here (the bar is centred on the
        pooled mean); the number being measured is therefore the conditional rate
        P(some level fails | pooled passes), which is exactly what (b) asks and what the anchor
        exhibits.  This is stated up front so the "pooled PASS" is not read as a finding.

The dials (exactly 2, both fully reported)
------------------------------------------
    BAR  (dial 1)  k in {0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0} half-widths in pooled SD units (0.25
                   is on the grid because the anchor band's own nearer edge sits at k = 0.28).  Every k
                   is reported for every triple; nothing is selected on k except inside the rule-8
                   leg, where k is chosen on IS cells and read once on untouched OOS cells.
    DIAL (dial 2)  which dial the mean is pooled over (cadence, panel, theta, family, construction,
                   gross, cost, window, arm, universe, n, ...).  Every dial found in a grid is
                   reported; none is dropped.

    PANEL, CADENCE, THETA and CONSTRUCTION in the book leg are REPORTED CONTRASTS: all 270 books
    are printed and none is selected on except by the pre-stated walk-forward rule.

Pre-registered hypotheses (stated before the run)
-------------------------------------------------
H_COMMON   At the anchor's own width, a MAJORITY (> 50%) of the record's (grid, statistic, dial)
           triples have at least one level mean outside the bar.  The anchor is then typical and
           "pooled PASS / level FAIL" is a record-wide reading hazard.
H_OUTLIER  (the rival) The rate is < 10% and the anchor's cadence dial is an outlier.
H_CENSUS   Of the record's 80 pre-registered bars, the ones applied to a pooled mean can be
           re-priced at level from their own committed artefacts in a MAJORITY of cases.
H_BOOK     Selecting a book on a statistic POOLED over the cadence dial gives the same
           out-of-sample book as requiring the statistic at EVERY level of that dial.

Census rule (mechanical, pre-registered)
----------------------------------------
Step 1  The band population is idea 554's extractor, re-run verbatim over research/backtests/*.py
        (this file and idea 554's own file excluded, as 554 excluded itself), and gated against
        554's committed `.census.csv` (G2: every one of its rows re-found with the same arity;
        extra rows allowed only from later commits).  554 already established the arity split:
        224 raw intervals -> 80 eligible bars -> 64 REPRO constant gates + 16 GRID bands.
Step 2  A bar is POOLED when its bounded expression, or the variable assigned to it within 12
        lines above, is an aggregate (`.mean(`, `np.mean`, `mean_`, `_mean`, `.agg(`, `pooled`)
        AND its 12-line context names a dial from the dial vocabulary or calls `.groupby(`.
        Reported as POOLED / AGG_NO_DIAL / NOT_AGG.
Step 3  A POOLED bar is RE-PRICEABLE at level when a committed artefact CSV of its OWN script
        carries both (i) a numeric column named in the bounded expression (STRICT link, 554's
        rule) or matching it case-insensitively as a substring (RELAXED link, reported separately)
        and (ii) a dial column with >= 2 levels.  Both counts are reported; the relaxation is a
        reported contrast, not a repair.
Step 4  BASE RATE grids: every committed *.csv/*.csv.gz in research/backtests (this run's own
        outputs excluded) is scanned.  A DIAL column is one whose name is in the dial vocabulary
        with 2..12 distinct levels and >= 2 rows per level; a STATISTIC column is any numeric
        column not in the dial vocabulary, not matching the identifier regex, with >= 5 distinct
        finite values and non-zero SD.  Every (file, statistic, dial) triple is priced at every k.

Rule 8 (walk-forward), required
-------------------------------
WF-CENSUS  Grids carrying a `window` column (IS/OOS, the record's own split at 2016-12-31): the
           SMALLEST k at which every level passes is chosen on the IS rows only, and whether that
           k still holds at level is read once on the untouched OOS rows.
WF-BOOK    A real 270-book grid (3 panels x 9 thetas x 5 cadences x 2 constructions, MA-THRESH,
           gross 0.75, 10 bps, next-day execution) is run.  Parameters are chosen on 2009-2016
           only, under two competing selection rules - POOLED (best mean Sharpe over the cadence
           dial) and CELL (best mean Sharpe among (panel, theta) pairs that beat SPY at EVERY
           cadence in-sample) - and 2017-2026 is read once.  OOS CAGR/Sharpe/MaxDD are reported
           against live RULES v2 and against SPY.

KEEP paths (PROTOCOL 4)
-----------------------
Both are evaluated on all 270 books this script actually runs (full sample and both halves, 4a
against live RULES v2, 4b against SPY with the OOS clause).  A census cannot itself produce a
KEEP candidate; if a book passes both paths it is reported as such and named.

Pre-registered gates (a FAIL is reported, not repaired)
-------------------------------------------------------
    G1  fast_backtest == engine.backtest at D/W/M/Q on every panel (< 1e-12 on returns)
    G2  the band extractor re-finds every one of idea 554's 80 committed census rows with the same
        arity; extra rows are allowed ONLY from *.py committed after 554's run and are printed
    G3  the anchor reproduces from idea 551's committed decomp.csv: MA-THRESH resid0_pp pooled
        over D..A = -0.2852 +/- 5e-4, INSIDE [-0.70,-0.20]; D and A level means OUTSIDE it
        (this is the queue's premise, taken at the CADENCE cut, and it is where the run's first
        finding lands - the gate is reported as it falls, not adjusted)
    G4  pooled mean == mean of level means on every balanced triple (< 1e-10, ABSOLUTE)
    G5  the base-rate scan reads >= 300 committed grids and >= 1000 (file, stat, dial) triples
    G6  live RULES v2 on U56 reproduces the record's committed anchor (8.66% / 1.2056 / -12.05%)

SURVIVORSHIP: the book leg's panels are current constituents (B136 and SMALL439 are screens run
today), so every CAGR/Sharpe/MaxDD level and the 4a/4b counts below are optimistic.  The census
legs read numbers other scripts computed on the same biased panels and inherit the same optimism.
"""
import gzip
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

BTDIR = REPO / "research" / "backtests"
OUT = Path(__file__).with_suffix("")
SELF = Path(__file__).name
PRIOR554 = "2026-09-09_is-every-published-BAND-a-band-on-a-MEAN-quoted-as-a-CELL-expectation_cloud"
PRIOR551 = BTDIR / "2026-09-09_restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain_C.decomp.csv"

# ---- dial 1 (the bar) and the published anchor band
KS = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
BAND_PUB = (-0.70, -0.20)

# ---- book-leg constants (idea 551's design, verbatim)
COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
LIVE_PUB = (0.0866, 1.2056, -0.1205)

# ---- gate tolerances
BAR_ENGINE = 1e-12
BAR_ANCHOR = 5e-4
BAR_IDENT = 1e-10
BAR_LIVE = 5e-4
G5_MIN_GRIDS, G5_MIN_TRIPLES = 300, 1000

MAX_CSV_BYTES = 30_000_000
MAX_ROWS = 200_000

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# =====================================================================  idea 554's extractor
NUM = r"-?\d+\.?\d*(?:[eE][-+]?\d+)?"
PATTERNS = {
    "TUPLE2": re.compile(rf"^\s*([A-Z][A-Z0-9_]{{2,40}})\s*=\s*\(\s*({NUM})\s*,\s*({NUM})\s*\)\s*(?:#.*)?$"),
    "IN_BAND": re.compile(rf"in_band\s*\(\s*([^,]{{1,60}}?)\s*,\s*({NUM})\s*,\s*({NUM})\s*\)"),
    "CHAIN": re.compile(rf"({NUM})\s*<=?\s*([A-Za-z_][\w.\[\]\"'()]{{0,50}})\s*<=?\s*({NUM})"),
    "BETWEEN": re.compile(rf"([A-Za-z_][\w.\[\]\"']{{0,40}})\.between\s*\(\s*({NUM})\s*,\s*({NUM})\s*\)"),
    "ABSTOL": re.compile(rf"abs\s*\(\s*([^()]{{1,80}}?)\s*-\s*({NUM})\s*\)\s*<=?\s*({NUM})"),
}
VERDICT_RE = re.compile(r"\bPASS\b|\bFAIL\b|\bHIT\b|\bMISS\b|\bOK\b|CONFIRMED|REFUTED|\bok\b|"
                        r"in_band|inside|clears|\bgate\b|VERDICT|holds|violat", re.I)
NAME_RE = re.compile(r"^(BAR|BAND)_|_(BAR|BAND)S?$")
MEAN_RE = re.compile(r"\.mean\s*\(|np\.mean|\bmean_|_mean\b")
ITER_RE = re.compile(r"\bfor\b.*\bin\b|\ball\s*\(|\bany\s*\(")
SAYS_RE = re.compile(r"\bmean\b|\bmedian\b|\bpooled\b|\baverage\b|per-cell|each cell|every cell|"
                     r"per cell|cellwise|cell-level", re.I)
IDENT_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
PARAM_PAIRS = {"COSTS", "ANCHOR", "BULK_LAST_Q", "RUNGS", "COST_RUNGS", "GROSSES",
               "GROSS_AXIS", "DIP_CENTRES", "DIP_CELLS", "MOM_RUN", "QUEUE_WINDOW"}
REPRO_REL = 0.05

# step-2 additions (idea 553's own)
AGG_RE = re.compile(r"\.mean\s*\(|np\.mean|\bmean_|_mean\b|\.agg\s*\(|pooled|\.groupby\s*\(")
GROUPBY_RE = re.compile(r"\.groupby\s*\(")

DIAL_VOCAB = {
    "panel", "cad", "cadence", "freq", "family", "conv", "construction", "gross", "n", "theta",
    "cost", "bps", "cost_bps", "window", "arm", "universe", "uni", "band", "sleeve", "kind",
    "dial", "selector", "mode", "variant", "phase", "stratum", "strata", "q", "k", "m", "x",
    "rung", "half", "leg", "form", "cut", "side", "regime", "quantile", "scheme", "weighting",
    "lookback", "horizon", "gate", "filter", "split", "target", "metric", "stat", "statistic",
    "pick", "selection", "cap", "sector", "vintage", "year", "era",
}
ID_RE = re.compile(r"^(book|file|line|idx|index|seed|draw|id|row|count|n_obs|nobs|ticker|name|"
                   r"date|start|end|.*_id|.*_idx|.*count.*)$", re.I)


def read_text(p):
    return p.read_text(errors="replace").split("\n")


def extract_bands():
    """Idea 554 Steps 1-4, verbatim, over research/backtests/*.py."""
    rows = []
    files = sorted(p for p in BTDIR.glob("*.py") if p.name != SELF and p.stem != PRIOR554)
    for p in files:
        lines = read_text(p)
        for i, ln in enumerate(lines):
            for pat, rx in PATTERNS.items():
                for mt in rx.finditer(ln):
                    if pat == "TUPLE2":
                        nm, a, b = mt.group(1), float(mt.group(2)), float(mt.group(3))
                        expr, lo, hi = nm, min(a, b), max(a, b)
                    elif pat == "ABSTOL":
                        expr, c, h = mt.group(1).strip(), float(mt.group(2)), float(mt.group(3))
                        lo, hi, nm = c - h, c + h, None
                    elif pat == "CHAIN":
                        a, expr, b = float(mt.group(1)), mt.group(2).strip(), float(mt.group(3))
                        lo, hi, nm = min(a, b), max(a, b), None
                    else:
                        expr, a, b = mt.group(1).strip(), float(mt.group(2)), float(mt.group(3))
                        lo, hi, nm = min(a, b), max(a, b), None
                    if not (lo < hi):
                        continue
                    if nm in PARAM_PAIRS:
                        continue
                    elig = bool(VERDICT_RE.search(ln)) or bool(nm and NAME_RE.search(nm))
                    ctx = "\n".join(lines[max(0, i - 12):i + 1])
                    rows.append(dict(file=p.name, line=i + 1, pattern=pat, name=nm, expr=expr,
                                     lo=lo, hi=hi, text=ln.strip()[:160], elig=elig,
                                     half=0.5 * (hi - lo), centre=0.5 * (hi + lo), ctx=ctx))
    df = pd.DataFrame(rows).drop_duplicates(subset=["file", "line", "pattern", "lo", "hi"])
    df["rel_half"] = df.half / df.centre.abs().replace(0, np.nan)
    df["arity"] = np.where((df.pattern == "ABSTOL") & (df.rel_half <= REPRO_REL), "REPRO", "GRID")
    kinds, says, pooled = [], [], []
    for _, r in df.iterrows():
        ctx = r.ctx
        if MEAN_RE.search(r.expr) or MEAN_RE.search(ctx):
            k = "MEAN"
        elif ITER_RE.search(ctx):
            k = "CELL"
        elif IDENT_RE.fullmatch(str(r.expr).strip()):
            k = "SCALAR"
        else:
            k = "UNSTATED"
        kinds.append(k)
        says.append(bool(SAYS_RE.search("\n".join(ctx.split("\n")[-3:]))))
        is_agg = bool(AGG_RE.search(r.expr) or AGG_RE.search(ctx))
        has_dial = bool(GROUPBY_RE.search(ctx)) or any(
            re.search(rf"[\"'\.\[]{re.escape(d)}[\"'\]\s,\)]", ctx) for d in sorted(DIAL_VOCAB))
        pooled.append("POOLED" if (is_agg and has_dial) else ("AGG_NO_DIAL" if is_agg else "NOT_AGG"))
    df["kind"], df["says"], df["pool"] = kinds, says, pooled
    return df.reset_index(drop=True)


# =====================================================================  grid scan
def csv_files():
    out = []
    for p in sorted(BTDIR.iterdir()):
        if p.name.startswith(OUT.name):
            continue
        if p.suffix == ".csv" or p.name.endswith(".csv.gz"):
            if p.stat().st_size <= MAX_CSV_BYTES:
                out.append(p)
    return out


def header_of(p):
    op = gzip.open if p.name.endswith(".gz") else open
    try:
        with op(p, "rt", errors="replace") as f:
            return f.readline().strip().split(",")
    except Exception:
        return []


def scan_grids(files):
    """Every (file, statistic, dial) triple in the committed record, priced at every k, plus the
    CUT-DEPTH LADDER: the same bar re-applied at one dial, at a dial PAIR, and at the raw cells."""
    triples, ladder, skipped, n_grids = [], [], 0, 0
    for p in files:
        head = header_of(p)
        if not head or len(head) < 2:
            continue
        dial_cands = [c for c in head if c.strip().lower() in DIAL_VOCAB]
        if not dial_cands:
            continue
        try:
            df = pd.read_csv(p, nrows=MAX_ROWS, low_memory=False)
        except Exception:
            skipped += 1
            continue
        if len(df) < 4:
            continue
        dials = []
        for c in dial_cands:
            if c not in df.columns:
                continue
            lv = df[c].dropna()
            k = lv.nunique()
            if 2 <= k <= 12 and lv.groupby(lv).size().min() >= 2:
                dials.append(c)
        if not dials:
            continue
        stats = []
        for c in df.columns:
            if c.strip().lower() in DIAL_VOCAB or ID_RE.match(str(c)):
                continue
            s = pd.to_numeric(df[c], errors="coerce")
            s = s.replace([np.inf, -np.inf], np.nan).dropna()
            if len(s) >= 4 and s.nunique() >= 5 and s.std(ddof=0) > 0:
                stats.append(c)
        if not stats:
            continue
        n_grids += 1
        for sc in stats:
            v = pd.to_numeric(df[sc], errors="coerce").replace([np.inf, -np.inf], np.nan)
            for dc in dials:
                sub = pd.DataFrame({"v": v, "d": df[dc]}).dropna()
                if len(sub) < 4:
                    continue
                g = sub.groupby("d")["v"]
                sizes = g.size()
                if sizes.min() < 2 or len(sizes) < 2:
                    continue
                m = sub.v.mean()
                sd = sub.v.std(ddof=0)
                if not np.isfinite(sd) or sd <= 0:
                    continue
                lm = g.mean()
                row = dict(file=p.name, stat=sc, dial=dc, n_cells=len(sub), n_levels=len(lm),
                           balanced=bool(sizes.nunique() == 1), pooled_mean=m, pooled_sd=sd,
                           mean_of_level_means=lm.mean(), level_min=lm.min(), level_max=lm.max(),
                           spread_sd=(lm.max() - lm.min()) / sd)
                for k in KS:
                    lo, hi = m - k * sd, m + k * sd
                    out_lv = int(((lm < lo) | (lm > hi)).sum())
                    row[f"nfail_k{k}"] = out_lv
                    row[f"fail_k{k}"] = bool(out_lv > 0)
                    row[f"cellcov_k{k}"] = float(((sub.v >= lo) & (sub.v <= hi)).mean())
                triples.append(row)
            # ---- cut-depth ladder for this (file, statistic): 1 dial, 2 dials, raw cells
            vv = v.dropna()
            if len(vv) >= 4:
                m, sd = vv.mean(), vv.std(ddof=0)
                if np.isfinite(sd) and sd > 0:
                    dl = sorted(dials)[:6]
                    cuts = [("d1", [d]) for d in dl]
                    cuts += [("d2", [a, b]) for i, a in enumerate(dl) for b in dl[i + 1:]]
                    cuts += [("cell", None)]
                    for depth, ks_ in cuts:
                        if ks_ is None:
                            lm = vv
                        else:
                            s2 = df.loc[v.notna(), ks_ + []].copy()
                            s2["v"] = vv
                            s2 = s2.dropna()
                            if len(s2) < 4:
                                continue
                            gg = s2.groupby(ks_)["v"]
                            if gg.size().min() < 2 or gg.ngroups < 2:
                                continue
                            lm = gg.mean()
                        r2 = dict(file=p.name, stat=sc, depth=depth,
                                  cut="+".join(ks_) if ks_ else "cell", n_levels=len(lm))
                        for k in KS:
                            lo, hi = m - k * sd, m + k * sd
                            r2[f"fail_k{k}"] = bool(((lm < lo) | (lm > hi)).any())
                            r2[f"outrate_k{k}"] = float(((lm < lo) | (lm > hi)).mean())
                        ladder.append(r2)
    return pd.DataFrame(triples), pd.DataFrame(ladder), n_grids, skipped


# =====================================================================  book leg
def cad_mask(idx, cad):
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def fast_backtest(px, weights, cad):
    """Vectorised twin of engine.backtest with a cadence mask that also knows "A"; G1."""
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = cad_mask(px.index, cad).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


def net(px, w, cad, cost=COST_BPS):
    r, t = fast_backtest(px, w, cad)
    return r - t * cost / 1e4


def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def stats_of(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


# =====================================================================  main
def main():
    P("=" * 110)
    P("IDEA 553 - POOLED-OVER-A-DIAL BARS: how many pooled PASSes are level FAILs?")
    P("=" * 110)

    # ---------------- G2 + the census (legs a/b)
    P("\n" + "-" * 110)
    P("LEG (a) THE CENSUS - which of the record's pre-registered bars are POOLED over a dial")
    P("-" * 110)
    B = extract_bands()
    elig = B[B.elig].copy()
    P(f"raw two-sided intervals: {len(B)}   eligible bars (used as a PASS/FAIL bar): {len(elig)}")
    P(f"arity: {elig.arity.value_counts().to_dict()}")
    prior = pd.read_csv(BTDIR / f"{PRIOR554}.census.csv")
    key = ["file", "line", "pattern", "lo", "hi"]
    mine = elig[key + ["arity", "kind"]].copy()
    theirs = prior[key + ["arity", "kind"]].copy()
    for f in (mine, theirs):
        f["lo"] = f.lo.round(10)
        f["hi"] = f.hi.round(10)
    mg = mine.merge(theirs, on=key, how="outer", indicator=True, suffixes=("", "_554"))
    missing = mg[mg._merge == "right_only"]
    extra = mg[mg._merge == "left_only"]
    same_kind = bool((mg.loc[mg._merge == "both", "arity"]
                      == mg.loc[mg._merge == "both", "arity_554"]).all())
    g2 = len(missing) == 0 and same_kind
    P(f"G2 {'PASS' if g2 else 'FAIL'}  every one of idea 554's {len(theirs)} committed census "
      f"rows is re-found with the same arity ({int((mg._merge == 'both').sum())} matched, "
      f"{len(missing)} missing); this run finds {len(mine)} because the record grew")
    P(f"  EXTRA rows vs 554 ({len(extra)}) - each must come from a *.py committed AFTER 554's run:")
    if len(extra):
        P(fmt(extra[key + ["arity"]].reset_index(drop=True)))
    if len(missing):
        P("  MISSING (in 554, not re-found):\n" + fmt(missing[key].reset_index(drop=True)))

    tab = pd.crosstab(elig.arity, elig.pool)
    P("\nPOOLED classification (Step 2), by arity:\n" + tab.to_string())
    grid = elig[elig.arity == "GRID"].copy()
    P(f"\nGRID bands: {len(grid)}; POOLED among them: {int((grid.pool == 'POOLED').sum())}")
    P(fmt(grid[["file", "line", "expr", "lo", "hi", "kind", "says", "pool"]].reset_index(drop=True)))

    # Step 3: re-priceability of the POOLED bars from their own artefacts
    pooled_bars = elig[elig.pool == "POOLED"].copy()
    rows = []
    for _, r in pooled_bars.iterrows():
        stem = r.file[:-3]
        arts = [p for p in BTDIR.iterdir()
                if p.name.startswith(stem) and (p.suffix == ".csv" or p.name.endswith(".csv.gz"))]
        toks = set(IDENT_RE.findall(str(r.expr)))
        strict = relaxed = None
        for p in arts:
            head = [h.strip() for h in header_of(p)]
            if not head:
                continue
            dials = [c for c in head if c.lower() in DIAL_VOCAB]
            if not dials:
                continue
            for c in head:
                if c in toks and strict is None:
                    strict = (p.name, c)
                cl, el = c.lower(), str(r.expr).lower()
                if (cl and (cl in el or any(cl in t.lower() or t.lower() in cl for t in toks))
                        and relaxed is None):
                    relaxed = (p.name, c)
        rows.append(dict(file=r.file, line=r.line, expr=str(r.expr)[:40], arity=r.arity,
                         n_artefacts=len(arts), strict=bool(strict), relaxed=bool(relaxed),
                         link=str(strict or relaxed or "")))
    PB = pd.DataFrame(rows)
    if len(PB):
        P(f"\nStep 3 re-priceability of the {len(PB)} POOLED bars from their OWN artefacts: "
          f"STRICT {int(PB.strict.sum())}/{len(PB)}, RELAXED {int(PB.relaxed.sum())}/{len(PB)}")
        P(fmt(PB.head(40)))
    else:
        P("\nStep 3: no POOLED bar found by the mechanical rule.")
    h_census = bool(len(PB) and PB.relaxed.mean() > 0.5)
    P(f"H_CENSUS ({'HOLDS' if h_census else 'FAILS'}): a majority of pooled bars re-priceable "
      f"at level from their own artefacts")

    # ---------------- G3 + the anchor, re-applied per level
    P("\n" + "-" * 110)
    P("LEG (b) THE ANCHOR - idea 551's pooled resid0 vs its own cadence levels")
    P("-" * 110)
    D = pd.read_csv(PRIOR551)
    MA = D[(D.family == "MA-THRESH") & (D.window == "FULL")]
    pooled = MA.resid0_pp.mean()
    lvl = MA.groupby("cad").resid0_pp.mean().reindex(CADENCES)
    inside = lambda x: BAND_PUB[0] <= x <= BAND_PUB[1]
    P(f"pooled over D..A = {pooled:.4f} pp/yr -> {'PASS' if inside(pooled) else 'FAIL'} {BAND_PUB}")
    for c in CADENCES:
        P(f"   level {c}: {lvl[c]:+.4f} -> {'PASS' if inside(lvl[c]) else 'FAIL'}")
    g3 = (abs(pooled - (-0.2852)) < BAR_ANCHOR and inside(pooled)
          and not inside(lvl["D"]) and not inside(lvl["A"]))
    P(f"G3 {'PASS' if g3 else 'FAIL'}  anchor reproduces: pooled -0.2852 inside, D and A outside")
    sd_a = MA.resid0_pp.std(ddof=0)
    k_pub = min(pooled - BAND_PUB[0], BAND_PUB[1] - pooled) / sd_a
    P(f"anchor cell SD {sd_a:.4f}; the published band's nearer edge is k = {k_pub:.3f} pooled SDs "
      f"from the pooled mean -> the record's own width sits at k ~ {k_pub:.2f}")
    n_fail = sum(1 for c in CADENCES if not inside(lvl[c]))
    P(f"ANSWER (b) for the anchor: 1 pooled PASS, {n_fail} of {len(CADENCES)} cadence levels FAIL it.")

    # the granularity ladder - the same band, the same cells, cut at increasing depth
    P("\nTHE GRANULARITY LADDER (same band, same 135 cells, cut deeper each rung):")
    lad = []
    for label, keys in (("POOLED (no cut)", []), ("panel (3)", ["panel"]), ("cadence (5)", ["cad"]),
                        ("panel x cadence (15)", ["panel", "cad"]),
                        ("panel x cadence x theta = cells (135)", ["panel", "cad", "theta"])):
        gm = MA.resid0_pp.mean() if not keys else MA.groupby(keys).resid0_pp.mean()
        vals = np.atleast_1d(np.asarray(gm))
        nf = int(sum(not inside(v) for v in vals))
        lad.append(dict(cut=label, n_levels=len(vals), n_FAIL=nf, fail_rate=nf / len(vals),
                        min=vals.min(), max=vals.max()))
    LAD = pd.DataFrame(lad)
    P(fmt(LAD))
    P("panel x cadence table (pp/yr; the queue's 'D and A cells fail' is the SMALL439 ROW):")
    P(fmt(MA.groupby(["panel", "cad"]).resid0_pp.mean().unstack()[CADENCES]))
    LAD.to_csv(f"{OUT}.ladder.csv", index=False)

    # ---------------- leg (c) base rate
    P("\n" + "-" * 110)
    P("LEG (c) THE BASE RATE - a bar centred on the pooled mean, re-applied at every level")
    P("-" * 110)
    files = csv_files()
    T, LADR, n_grids, skipped = scan_grids(files)
    P(f"scanned {len(files)} committed artefact CSVs (<= {MAX_CSV_BYTES/1e6:.0f} MB); "
      f"{n_grids} carry a dial and a statistic; {skipped} unparseable; "
      f"{len(T)} (file, statistic, dial) triples")
    g5 = n_grids >= G5_MIN_GRIDS and len(T) >= G5_MIN_TRIPLES
    P(f"G5 {'PASS' if g5 else 'FAIL'}  >= {G5_MIN_GRIDS} grids and >= {G5_MIN_TRIPLES} triples")
    bal = T[T.balanced]
    err = (bal.pooled_mean - bal.mean_of_level_means).abs().max() if len(bal) else np.nan
    rel = ((bal.pooled_mean - bal.mean_of_level_means).abs()
           / bal.pooled_mean.abs().clip(lower=1e-12)).max() if len(bal) else np.nan
    g4 = bool(np.isfinite(err) and err < BAR_IDENT)
    P(f"G4 {'PASS' if g4 else 'FAIL'}  pooled mean == mean of level means on {len(bal)} balanced "
      f"triples (max abs diff {err:.2e}; max RELATIVE diff {rel:.2e} - the pre-registered "
      f"tolerance is absolute and the record carries columns of order 1e10, reported not repaired)")
    if not g4:
        w = (bal.pooled_mean - bal.mean_of_level_means).abs().idxmax()
        P(f"  worst triple: {bal.loc[w, 'file']} / {bal.loc[w, 'stat']} / {bal.loc[w, 'dial']} "
          f"(pooled mean {bal.loc[w, 'pooled_mean']:.6g})")

    P("\nFAIL RATE (>= 1 level mean outside the bar), by k - ALL {} triples:".format(len(T)))
    summ = pd.DataFrame({f"k={k}": [T[f"fail_k{k}"].mean(), T[f"nfail_k{k}"].sum(),
                                    T[f"cellcov_k{k}"].mean()] for k in KS},
                        index=["level_fail_rate", "levels_failing", "mean_cell_coverage"]).T
    P(fmt(summ))
    P("\nby DIAL (dial 2 - every dial reported), level_fail_rate at each k:")
    by_dial = T.groupby("dial").agg(n=("stat", "size"), **{f"k{k}": (f"fail_k{k}", "mean") for k in KS})
    P(fmt(by_dial.sort_values("n", ascending=False)))
    P("\nby DIAL: mean spread of level means in pooled-SD units (level_max - level_min)/sd:")
    P(fmt(T.groupby("dial").spread_sd.agg(["size", "mean", "median", "max"]).sort_values("mean", ascending=False)))

    k_near = min(KS, key=lambda k: abs(k - k_pub))
    rate_pub = T[f"fail_k{k_near}"].mean()
    P(f"\nAt the anchor's own width (k = {k_pub:.2f}, nearest grid point k = {k_near}): "
      f"level_fail_rate = {rate_pub:.4f} over {len(T)} triples")
    h_common = rate_pub > 0.50
    h_outlier = rate_pub < 0.10
    P(f"H_COMMON {'HOLDS' if h_common else 'FAILS'} (> 50%);  "
      f"H_OUTLIER {'HOLDS' if h_outlier else 'FAILS'} (< 10%)")
    cad_rows = T[T.dial.str.lower().isin({"cad", "cadence", "freq"})]
    if len(cad_rows):
        P(f"the anchor's own dial (cadence/freq): {len(cad_rows)} triples, "
          f"level_fail_rate at k={k_near} = {cad_rows[f'fail_k{k_near}'].mean():.4f}")
    P("\nTHE CUT-DEPTH LADDER, record-wide - the same bar re-applied at increasing cut depth")
    P(f"({len(LADR)} (file, statistic, cut) rows; d1 = one dial, d2 = a dial PAIR, cell = raw cells)")
    lad_tab = LADR.groupby("depth").agg(n=("stat", "size"),
                                        **{f"fail_k{k}": (f"fail_k{k}", "mean") for k in KS})
    P(fmt(lad_tab.reindex(["d1", "d2", "cell"])))
    P("mean SHARE of levels outside the bar, by depth:")
    P(fmt(LADR.groupby("depth")[[f"outrate_k{k}" for k in KS]].mean().reindex(["d1", "d2", "cell"])))
    LADR.to_csv(f"{OUT}.ladder_record.csv.gz", index=False)
    T.to_csv(f"{OUT}.grids.csv.gz", index=False)
    elig.drop(columns=["ctx"]).to_csv(f"{OUT}.census.csv", index=False)

    # ---------------- rule 8, census leg
    P("\n" + "-" * 110)
    P("RULE 8 (WF-CENSUS) - k chosen on IS levels, read once on untouched OOS levels")
    P("-" * 110)
    wf = []
    for p in files:
        head = [h.strip() for h in header_of(p)]
        if "window" not in [h.lower() for h in head]:
            continue
        try:
            df = pd.read_csv(p, nrows=MAX_ROWS, low_memory=False)
        except Exception:
            continue
        wcol = [c for c in df.columns if c.strip().lower() == "window"][0]
        vals = set(str(x).upper() for x in df[wcol].dropna().unique())
        if not ({"IS", "OOS"} <= vals):
            continue
        dials = [c for c in df.columns
                 if c.strip().lower() in DIAL_VOCAB and c != wcol
                 and 2 <= df[c].dropna().nunique() <= 12]
        stats = [c for c in df.columns
                 if c.strip().lower() not in DIAL_VOCAB and not ID_RE.match(str(c))
                 and pd.to_numeric(df[c], errors="coerce").notna().sum() >= 8
                 and pd.to_numeric(df[c], errors="coerce").nunique() >= 5]
        up = df[wcol].astype(str).str.upper()
        for sc in stats:
            v = pd.to_numeric(df[sc], errors="coerce")
            for dc in dials:
                for win, other in (("IS", "OOS"),):
                    a = pd.DataFrame({"v": v, "d": df[dc]})[up == win].dropna()
                    b = pd.DataFrame({"v": v, "d": df[dc]})[up == other].dropna()
                    if len(a) < 4 or len(b) < 4 or a.d.nunique() < 2 or b.d.nunique() < 2:
                        continue
                    m, sd = a.v.mean(), a.v.std(ddof=0)
                    if not np.isfinite(sd) or sd <= 0:
                        continue
                    lm_is = a.groupby("d").v.mean()
                    kstar = next((k for k in KS
                                  if ((lm_is >= m - k * sd) & (lm_is <= m + k * sd)).all()), None)
                    if kstar is None:
                        continue
                    lo, hi = m - kstar * sd, m + kstar * sd     # the IS-fitted bar, frozen
                    lm_oos = b.groupby("d").v.mean()
                    holds = bool(((lm_oos >= lo) & (lm_oos <= hi)).all())
                    wf.append(dict(file=p.name, stat=sc, dial=dc, k_star=kstar,
                                   n_levels_oos=len(lm_oos),
                                   n_fail_oos=int(((lm_oos < lo) | (lm_oos > hi)).sum()),
                                   holds=holds))
    WF = pd.DataFrame(wf)
    if len(WF):
        P(f"{len(WF)} (file, stat, dial) triples carry an IS/OOS window split")
        P(f"IS-fitted bar holds at EVERY OOS level in {int(WF.holds.sum())} of {len(WF)} "
          f"({WF.holds.mean():.1%})")
        P("\nby chosen k*:\n" + fmt(WF.groupby("k_star").agg(n=("holds", "size"), hold_rate=("holds", "mean"))))
        P("\nby dial:\n" + fmt(WF.groupby("dial").agg(n=("holds", "size"), hold_rate=("holds", "mean"))
                               .sort_values("n", ascending=False).head(15)))
        WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    else:
        P("no committed grid carries an IS/OOS window column with >= 2 dial levels on both sides.")

    # ---------------- the book leg
    P("\n" + "-" * 110)
    P("THE BOOK LEG - 270 real books (3 panels x 9 thetas x 5 cadences x 2 constructions)")
    P("-" * 110)
    PX = panels()

    # G1: fast_backtest == engine.backtest
    worst = 0.0
    for nm, (px, _) in PX.items():
        w = book(px, ma_gate(px, 0.0), "RESPREAD")
        for cad in ["D", "W", "M", "Q"]:
            r_fast, t_fast = fast_backtest(px, w, cad)
            eng = engine_backtest(px, w, cost_bps=0.0, freq=cad)
            worst = max(worst, float((r_fast - eng["returns"]).abs().max()),
                        float((t_fast - eng["turnover"]).abs().max()))
    P(f"G1 {'PASS' if worst < BAR_ENGINE else 'FAIL'}  fast_backtest vs engine.backtest, "
      f"3 panels x 4 cadences: worst abs diff {worst:.3e}")

    # G6: live RULES v2 on U56
    px56, spy56 = PX["U56"]
    full56 = pd.concat([px56, spy56.rename("SPY")], axis=1)
    v2w = rules_v2_weights(full56).drop(columns=["SPY"], errors="ignore").reindex(columns=px56.columns).fillna(0.0)
    r_v2 = net(px56, v2w, "W")
    start = px56.index[260]
    c6, s6, d6 = stats_of(r_v2.loc[start:])
    g6 = all(abs(a - b) < BAR_LIVE for a, b in zip((c6, s6, d6), LIVE_PUB))
    P(f"G6 {'PASS' if g6 else 'FAIL'}  live RULES v2 on U56: {c6:.4f} / {s6:.4f} / {d6:.4f} "
      f"vs published {LIVE_PUB}")

    rows = []
    series = {}
    for pn in PANELS:
        px, spy = PX[pn]
        st = px.index[260]
        spy_r = spy.pct_change().fillna(0.0)
        full = pd.concat([px, spy.rename("SPY")], axis=1)
        v2 = rules_v2_weights(full).drop(columns=["SPY"], errors="ignore").reindex(columns=px.columns).fillna(0.0)
        r_v2 = net(px, v2, "W").loc[st:]
        ref = dict(spy=spy_r.loc[st:], v2=r_v2)
        for th in MA_THETA:
            g = ma_gate(px, th)
            for con in CONSTRUCTIONS:
                w = book(px, g, con)
                for cad in CADENCES:
                    r = net(px, w, cad).loc[st:]
                    h = len(r) // 2
                    C, S, DD = stats_of(r)
                    H1, H2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
                    ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
                    Cis, Sis, _ = stats_of(ris)
                    Co, So, DDo = stats_of(roos)
                    b = ref["v2"]
                    bC, bS, bDD = stats_of(b)
                    bH1, bH2 = metrics(b.iloc[:h])["Sharpe"], metrics(b.iloc[h:])["Sharpe"]
                    sp = ref["spy"]
                    sC, sS, sDD = stats_of(sp)
                    sH1, sH2 = metrics(sp.iloc[:h])["Sharpe"], metrics(sp.iloc[h:])["Sharpe"]
                    spo = sp.loc[OOS_START:]
                    soC, soS, soDD = stats_of(spo)
                    p4a = bool(H1 > bH1 and H2 > bH2 and DD >= bDD)
                    p4b = bool(H1 > sH1 and H2 > sH2 and So > soS and DD >= 0.60 * sDD
                               and C >= 0.70 * sC)
                    rows.append(dict(panel=pn, theta=th, conv=con, cad=cad, CAGR=C, Sharpe=S,
                                     MaxDD=DD, H1=H1, H2=H2, IS_CAGR=Cis, IS_Sharpe=Sis,
                                     OOS_CAGR=Co, OOS_Sharpe=So, OOS_MaxDD=DDo,
                                     v2_Sharpe=bS, v2_H1=bH1, v2_H2=bH2, v2_MaxDD=bDD,
                                     spy_Sharpe=sS, spy_H1=sH1, spy_H2=sH2, spy_MaxDD=sDD,
                                     spy_CAGR=sC, spy_OOS_Sharpe=soS, spy_OOS_CAGR=soC,
                                     spy_OOS_MaxDD=soDD, pass4a=p4a, pass4b=p4b))
        series[pn] = ref
        P(f"  {pn}: books done ({len(MA_THETA)*len(CONSTRUCTIONS)*len(CADENCES)})")
    BK = pd.DataFrame(rows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    P(f"\n{len(BK)} books.  4a passers {int(BK.pass4a.sum())}, 4b passers {int(BK.pass4b.sum())}, "
      f"BOTH {int((BK.pass4a & BK.pass4b).sum())}")
    if (BK.pass4a & BK.pass4b).any():
        P("BOTH-path books:\n" + fmt(BK[BK.pass4a & BK.pass4b][
            ["panel", "theta", "conv", "cad", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]))
    P("\n4a/4b by panel:\n" + fmt(BK.groupby("panel")[["pass4a", "pass4b"]].sum()))
    P("\nfull-sample Sharpe by panel x cadence (mean over theta x construction):")
    P(fmt(BK.pivot_table(index="panel", columns="cad", values="Sharpe", aggfunc="mean")[CADENCES]))

    # WF-BOOK: POOLED vs CELL selection
    P("\n" + "-" * 110)
    P("RULE 8 (WF-BOOK) - IS (<= 2016) chooses, OOS (2017-2026) read once; POOLED vs CELL rule")
    P("-" * 110)
    wfb = []
    for pn in PANELS:
        sub = BK[BK.panel == pn]
        spy_is_S = {}
        for cad in CADENCES:
            sp = series[pn]["spy"].loc[:IS_END]
            spy_is_S[cad] = metrics(sp)["Sharpe"]
        pooled_is = sub.groupby(["theta", "conv"]).IS_Sharpe.mean()
        pick_pooled = pooled_is.idxmax()
        ok_cell = []
        for (th, con), grp in sub.groupby(["theta", "conv"]):
            if all(grp[grp.cad == c].IS_Sharpe.iloc[0] > spy_is_S[c] for c in CADENCES):
                ok_cell.append((th, con))
        pick_cell = (max(ok_cell, key=lambda tc: pooled_is[tc]) if ok_cell else None)
        for label, pick in (("POOLED", pick_pooled), ("CELL", pick_cell)):
            if pick is None:
                P(f"{pn} {label}: no (theta, construction) clears the rule in-sample -> no pick")
                wfb.append(dict(panel=pn, rule=label, theta=np.nan, conv="", n_ok=len(ok_cell),
                                OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan))
                continue
            th, con = pick
            g = sub[(sub.theta == th) & (sub.conv == con)]
            wfb.append(dict(panel=pn, rule=label, theta=th, conv=con,
                            n_ok=len(ok_cell) if label == "CELL" else len(pooled_is),
                            OOS_CAGR=g.OOS_CAGR.mean(), OOS_Sharpe=g.OOS_Sharpe.mean(),
                            OOS_MaxDD=g.OOS_MaxDD.mean(),
                            OOS_Sharpe_min=g.OOS_Sharpe.min(), OOS_Sharpe_max=g.OOS_Sharpe.max()))
    WFB = pd.DataFrame(wfb)
    P(fmt(WFB))
    for pn in PANELS:
        r_v2 = series[pn]["v2"].loc[OOS_START:]
        sp = series[pn]["spy"].loc[OOS_START:]
        cv, sv, dv = stats_of(r_v2)
        cs, ss, ds = stats_of(sp)
        P(f"{pn} OOS references: RULES v2 {cv:.2%} / {sv:.4f} / {dv:.2%}   "
          f"SPY {cs:.2%} / {ss:.4f} / {ds:.2%}")
    same = WFB.pivot_table(index="panel", columns="rule", values="theta", dropna=False)
    agree = int((same["POOLED"] == same["CELL"]).sum())
    nopick = int(WFB[(WFB.rule == "CELL") & WFB.theta.isna()].shape[0])
    h_book = bool(agree == len(PANELS))
    P(f"H_BOOK {'HOLDS' if h_book else 'FAILS'}: POOLED and CELL pick the same book on "
      f"{agree} of {len(PANELS)} panels; CELL makes NO pick on {nopick} panel(s), where the "
      f"POOLED rule still trades one.")
    for pn in PANELS:
        rp = WFB[(WFB.panel == pn) & (WFB.rule == "POOLED")].iloc[0]
        rc = WFB[(WFB.panel == pn) & (WFB.rule == "CELL")].iloc[0]
        so = stats_of(series[pn]["spy"].loc[OOS_START:])[1]
        if np.isnan(rc.theta):
            P(f"  {pn}: CELL refuses; POOLED trades theta {rp.theta:+.2f} {rp.conv} -> OOS Sharpe "
              f"{rp.OOS_Sharpe:.4f} vs SPY OOS {so:.4f} "
              f"({'BELOW' if rp.OOS_Sharpe < so else 'above'} SPY)")
        else:
            P(f"  {pn}: both pick theta {rp.theta:+.2f} {rp.conv} -> OOS Sharpe {rp.OOS_Sharpe:.4f} "
              f"vs SPY OOS {so:.4f}")
    WFB.to_csv(f"{OUT}.wfbook.csv", index=False)

    P("\n" + "=" * 110)
    P("SURVIVORSHIP: B136 and SMALL439 are current constituents of their screens; every CAGR, "
      "Sharpe, MaxDD and both KEEP columns in the book leg are optimistic, and the census legs "
      "read numbers other scripts computed on the same panels.")
    P("SCOPE LIMIT: the band extractor reads *.py through five syntactic patterns, so the 80-bar "
      "population is a LOWER BOUND (a bar living only as prose in a .result.md is outside it); "
      f"the grid scan skips artefacts above {MAX_CSV_BYTES/1e6:.0f} MB.")
    P("=" * 110)
    flush_log()


if __name__ == "__main__":
    main()
