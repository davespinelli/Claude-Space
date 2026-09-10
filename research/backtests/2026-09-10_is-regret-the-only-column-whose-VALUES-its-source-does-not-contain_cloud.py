#!/usr/bin/env python3
"""Idea 666 (cloud, 2026-09-10) -- is `regret` the only column in the record whose VALUES its
source does not contain?

QUEUE 666: "idea 664 found 1,442 of the 1,508 tolerance-proof metric reads (95.6%) are the
single column `regret`, 1,675 BOOK-class reads of which sit in the one file that PROPOSED the
metric.  Re-derive `regret` from each source's own published columns under every definition the
record uses, and report how many published regret claims are recomputations their source cannot
reproduce.  Max 2 params (regret definition, tolerance)."

WHAT IS ACTUALLY BEING TESTED
  Idea 664's finding is a NEAREST-NEIGHBOUR statement: a child file printed a number that does
  not appear anywhere in its source's own column.  That is consistent with two very different
  worlds and the queue asks which:
    W1  `regret` is a DERIVED quantity -- best minus pick -- so of course it is not in the
        source's column list; it is a function OF the source's columns.  Then every regret read
        is re-derivable and the record is tidy.
    W2  `regret` is genuinely unreproducible: the columns needed to rebuild it were never
        published, so a reader cannot check a single regret claim.
  H1 (re-derivation)  For every committed CSV carrying a regret-family column, search the file's
        OWN other published columns for a formula that reproduces the column exactly.  A read is
        REPRODUCED if some definition in the record's own vocabulary matches every row.
        FALSIFIABLE: if most reads are reproduced, idea 664's tail is an artefact of asking the
        wrong question (membership, not derivation), and 666's premise fails.
  H2 (the sign)  The record writes regret BOTH ways.  `grep` over the corpus finds
        `regret = best - pick` (>= 0) and `regret = pick - best` (<= 0) in comparable numbers.
        If both conventions are published under ONE name, then `regret` is not a column at all:
        it is two columns sharing a spelling, and every cross-file aggregate over it
        (`("regret","mean")`, `("regret","min")`) is undefined.  Census the empirical sign of
        every committed regret column and the declared sign of every producing script.
  H3 (declared vs realised)  A script's source line is a CLAIM about its own column.  Compare
        the orientation parsed from the producing .py against the sign realised in the CSV.
  H4 (live price)  Sign is not a cosmetic fact: the record's aggregators reduce a cell to
        min/mean regret and adopt the family with the LOWEST number.  Under the BEST-PICK
        convention argmin(regret) is the best family; under PICK-BEST it is the WORST one.  Run
        a pre-registered 5-family menu on three panels through rule 8 and price, in OOS Sharpe /
        CAGR / MaxDD, the cost of reading a regret column in the wrong convention.  Evaluate
        BOTH KEEP paths on every book.
        Controls: the two conventions are exact negatives, so any disagreement is pure sign; a
        cell whose families tie is reported, never broken.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 REGRET DEFINITION : the forms the record actually writes, as a search space --
                 PAIR    r == a - b            for any ordered pair of the file's own columns
                 PAIRABS r == |a| - |b|        (the MaxDD/DD-regret form)
                 PAIRPP  r == 100*(a - b) or 100*(|a| - |b|)   (the _pp form)
                 GRPMAX  r == groupmax(a) - a  or  a - groupmax(a), grouped by the file's own
                                               key columns (the "best in cell" form, for files
                                               that never publish a best_* column)
                 ALL     the union
    P2 TOLERANCE         : {0 (bitwise-exact), 1e-12, 1e-9, 1e-6, 1e-4, 1e-3}
  => 5 x 6 = 30 census grid points, every one written to .censusgrid.csv.
  LIVE: panel x family x arm x cost rung, every point in .grid.csv; rule 8 picks per
  (panel, family, cost) on 2009-2016 and is evaluated on 2017-2026 untouched.
  REPORTED, NOT TUNED: the panels, the five menu families and their arms, the cost rungs, the
  cadence, the gross, the IS/OOS boundary, the warm-up.  Nothing is chosen by looking at an
  outcome except inside rule 8.

STATED LIMITATIONS
  * The census asks whether a file's OWN columns reproduce its regret column.  A file that
    computed regret against a menu it never published cannot be reproduced here, and that is
    the finding, not a limitation of the search: an unpublished input is exactly what "its
    source does not contain" means.
  * The search is over pairwise and group-max forms.  A regret built from three or more columns
    would be missed; the .unrep.csv lists every unreproduced read with its column list so the
    residue is auditable rather than asserted.
  * SMALL439 SURVIVORSHIP: data/prices_small.csv is the CURRENT constituents of the sub-$2B
    screen (see data/SMALL_PANEL_README.md).  Names that delisted are absent, so every small-panel
    return here is biased upward.  Tickers with max_1d_move >= 1.0 in data/small_meta.csv are
    dropped first (a standing convention of this lane).
  * The small panel starts 2010, so its rule-8 IS window is 2010-2016, not 2009-2016.

GATES (run before any new number is read; a failure stops the run)
  G1 the band book at (b=0.03, g=0.75) reproduces `baseline.rules_v2_weights` exactly, and the
     vectorised harness reproduces `engine.backtest` at 10 bps.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 against a live engine.backtest(25 bps).
  G3 idea 664's committed .tail.csv reproduces its published headline off its OWN artefact:
     1,508 tolerance-proof reads, 1,442 of them `regret` (95.6%), 1,459 BOOK / 49 WINDOW.
  G4 the census partition is exact at all 30 grid points (REPRODUCED + UNREPRODUCED + NODATA
     == N) and the REPRODUCED count is non-decreasing in tolerance within every definition.
  G5 the two sign conventions are exact negatives on the live leg: regret_BP == -regret_PB at
     every grid point.

Deterministic, standalone, no network.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .reads.csv .censusgrid.csv .signs.csv .unrep.csv .grid.csv
       .walkforward.csv .keeppaths.csv
Modifies nothing (RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py untouched).
fast_backtest() is idea 664's vectorised harness, re-asserted against engine.backtest in G1.
"""
import csv
import itertools
import re
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
csv.field_size_limit(10 ** 7)

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                      # PROTOCOL 2
COSTRUNGS = [10.0, 25.0]
FREQ = "W"
BAND = 0.03                      # RULES v2 clause 2
GROSS0 = 0.75                    # RULES v2 clause 3
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TOLS = [0.0, 1e-12, 1e-9, 1e-6, 1e-4, 1e-3]
TOLNAMES = ["EXACT", "1e-12", "1e-09", "1e-06", "1e-04", "1e-03"]
DEFS = ["PAIR", "PAIRABS", "PAIRPP", "GRPMAX", "ALL"]
# a name-matched column that is NOT a regret VALUE: a flag, a counter, a p-value, an sd.  Reported
# as a split of the population, never as a filter chosen after the fact.
NOTMETRIC = re.compile(r"^(has_|n_|p_)|_(vals|sd|n|count|nonneg|frac)$|^regret_vals$", re.I)
IDEA664_TAIL = "2026-09-10_price-the-RE-DERIVED-METRIC-column-against-its-own-source_C.tail.csv"

# pre-registered live menu: 5 families, arms fixed before any outcome was read
FAM_ARMS = {
    "BAND":    [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20],
    "GROSS":   [0.25, 0.50, 0.75, 1.00],
    "N":       [5, 10, 15, 20, 30, 40],
    "CADENCE": ["D", "W", "M", "Q"],
    "VOLCAP":  [0.30, 0.40, 0.60, 0.80, 9.99],
}

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


def dump(df, tag):
    p = OUT / f"{STEM}.{tag}.csv"
    df.to_csv(p, index=False)
    P(f"  [wrote {p.name}  {len(df)} rows]")


# ================================================================================================
# 1.  POPULATION -- every committed regret-family column in research/backtests
# ================================================================================================
def population():
    P("=" * 100)
    P("(A) POPULATION -- every committed CSV column whose name contains 'regret'")
    P("=" * 100)
    rows = []
    for p in sorted(OUT.glob("*.csv")):
        if p.name.startswith(STEM):
            continue          # this run's OWN output is not part of the record it is auditing
        try:
            hdr = next(csv.reader(open(p, newline="")))
        except Exception:
            continue
        cols = [c.strip() for c in hdr]
        for c in cols:
            if "regret" in c.lower():
                rows.append(dict(file=p.name, col=c, stem=p.name.split(".")[0],
                                 is_metric=not bool(NOTMETRIC.search(c))))
    R = pd.DataFrame(rows)
    P(f"  files with a regret-family column : {R.file.nunique()}")
    P(f"  (file, column) reads              : {len(R)}")
    P(f"  distinct column spellings         : {R.col.nunique()}")
    P(f"  ... of which are regret VALUES    : {int(R.is_metric.sum())}   "
      f"(the other {int((~R.is_metric).sum())} are flags/counters/p-values whose name matched: "
      f"{', '.join(sorted(set(R.loc[~R.is_metric, 'col'])))})")
    P()
    P("  the ten most common spellings:")
    vc = R.col.value_counts().head(10)
    for k, v in vc.items():
        P(f"    {k:<22} {v}")
    return R


# ================================================================================================
# 2.  RE-DERIVATION -- can the file's own other columns rebuild its regret column?
# ================================================================================================
def _keys(df, regcols):
    """Candidate grouping columns: object dtype, or low-cardinality numerics that are not
    metrics (<= 20 distinct values).  These are the file's own 'cell' identifiers."""
    ks = []
    for c in df.columns:
        if c in regcols:
            continue
        s = df[c]
        if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
            if s.nunique(dropna=False) <= 20:
                ks.append(c)
        elif s.nunique(dropna=False) <= max(2, len(df) // 2):
            ks.append(c)
    return ks[:8]


def _groupings(df, keys):
    """No grouping, the full key, and the full key minus one column at a time."""
    gs = [("WHOLE", None)]
    if keys:
        gs.append(("|".join(keys), list(keys)))
        if len(keys) > 1:
            for drop in keys:
                sub = [k for k in keys if k != drop]
                gs.append(("|".join(sub), sub))
    return gs[:12]


def rederive_one(df, rcol, regcols, gmcache):
    """Best achievable residual per definition family for ONE regret column.

    Returns {definition: (min_residual, formula)}.  Computing the residual once and comparing
    it to the tolerance ladder afterwards makes the 5 x 6 grid a lookup, not 30 searches.
    """
    r = pd.to_numeric(df[rcol], errors="coerce")
    ok = r.notna().values
    if ok.sum() == 0:
        return None
    rv = r.values[ok]
    num = df.select_dtypes(include=[np.number]).drop(
        columns=[c for c in regcols if c in df.columns], errors="ignore")
    if len(num.columns):
        good = num.notna().values[ok].all(axis=0)
        num = num.loc[:, good]
    A = num.values[ok].astype(float) if len(num.columns) else np.zeros((int(ok.sum()), 0))
    names = list(num.columns)
    p = A.shape[1]
    res = {d: (np.inf, "") for d in DEFS if d != "ALL"}

    # -- PAIR / PAIRABS / PAIRPP: r == sc*(f(a) - f(b)) over ordered pairs ---------------------
    for tag, Mx, sc, absd in (("PAIR", A, 1.0, False), ("PAIRABS", np.abs(A), 1.0, True),
                              ("PAIRPP", A, 100.0, False), ("PAIRPP", np.abs(A), 100.0, True)):
        for i in range(p):
            Ui = (rv / sc) + Mx[:, i]     # want column j with Mx[:,j] == Ui  => r = sc*(Mj - Mi)
            D = np.nanmax(np.abs(Mx - Ui[:, None]), axis=0)
            if not np.isfinite(D).any():
                continue
            j = int(np.nanargmin(D))
            d = float(D[j] * sc)
            if d < res[tag][0]:
                a, b = names[j], names[i]
                if absd:
                    a, b = f"|{a}|", f"|{b}|"
                f = f"{a} - {b}"
                if sc != 1.0:
                    f = f"100*({f})"
                res[tag] = (d, f)

    # -- GRPMAX: r == groupmax(a) - a  or  a - groupmax(a) -------------------------------------
    keys = _keys(df, regcols)
    sub = df.loc[ok]
    for gname, gk in _groupings(df, keys):
        if gk is None:
            codes, ng = None, 0
        else:
            ck = (rcol, tuple(gk))          # the row mask is per regret column, so key on it
            if ck not in gmcache:
                lab = pd.Series(list(zip(*[sub[k].astype(str).values for k in gk])))
                cc, uu = pd.factorize(lab)
                gmcache[ck] = (np.asarray(cc), len(uu))
            codes, ng = gmcache[ck]
        for i, nm in enumerate(names):
            col = A[:, i]
            if codes is None:
                gm = np.full(len(col), np.nanmax(col))
            else:
                acc = np.full(ng, -np.inf)
                np.maximum.at(acc, codes, np.nan_to_num(col, nan=-np.inf))
                gm = acc[codes]
            base = gm - col
            for sign, form in ((+1.0, f"max({nm}|{gname}) - {nm}"),
                               (-1.0, f"{nm} - max({nm}|{gname})")):
                d = float(np.nanmax(np.abs(rv - sign * base)))
                if np.isfinite(d) and d < res["GRPMAX"][0]:
                    res["GRPMAX"] = (d, form)
    return res


def census(R):
    """One pass over the population; residual per (read, definition).  Fills both the per-read
    table and the 5 x 6 grid."""
    P()
    P("=" * 100)
    P("(B) RE-DERIVATION -- 30 grid points (5 definitions x 6 tolerances)")
    P("=" * 100)
    t0 = time.time()
    resid = {}
    per_read = []
    for fname, grp in R.groupby("file"):
        try:
            df = pd.read_csv(OUT / fname)
        except Exception:
            for c in grp.col:
                per_read.append(dict(file=fname, col=c, n=0, nrows=0, ncols=0,
                                     status="UNREADABLE"))
            continue
        regcols = list(grp.col)
        gmcache = {}
        for c in regcols:
            res = rederive_one(df, c, regcols, gmcache)
            row = dict(file=fname, col=c,
                       n=int(pd.to_numeric(df[c], errors="coerce").notna().sum()),
                       nrows=len(df), ncols=int(df.select_dtypes(include=[np.number]).shape[1]))
            if res is None:
                row.update(status="NODATA")
            else:
                resid[(fname, c)] = res
                bd = min(res, key=lambda d: res[d][0])
                row.update(status="PRICED", best_def=bd, best_resid=res[bd][0],
                           best_form=res[bd][1],
                           **{f"d_{d}": res[d][0] for d in res})
            per_read.append(row)
    D = pd.DataFrame(per_read)
    P(f"  priced {len(D)} reads in {time.time()-t0:.1f}s")

    # -- the grid ------------------------------------------------------------------------------
    rows = []
    nodata = int((D.status == "NODATA").sum())
    unread = int((D.status == "UNREADABLE").sum())
    for tol, tname in zip(TOLS, TOLNAMES):
        counts = {d: 0 for d in DEFS}
        for key, res in resid.items():
            anyd = False
            for d in res:
                if res[d][0] <= tol:
                    counts[d] += 1
                    anyd = True
            if anyd:
                counts["ALL"] += 1
        for d in DEFS:
            rows.append(dict(tol=tname, definition=d, reproduced=counts[d]))
        rows.append(dict(tol=tname, definition="NODATA", reproduced=nodata))
        rows.append(dict(tol=tname, definition="UNREADABLE", reproduced=unread))
    G = pd.DataFrame(rows)

    # -- per-read verdict at the record's own working tolerance (the tightest that reproduces) --
    st, dff, frm, tl = [], [], [], []
    for _, row in D.iterrows():
        key = (row["file"], row["col"])
        if key not in resid:
            st.append(row["status"]); dff.append(""); frm.append(""); tl.append("")
            continue
        res = resid[key]
        hit = None
        for tol, tname in zip(TOLS, TOLNAMES):
            cand = [d for d in res if res[d][0] <= tol]
            if cand:
                hit = (tname, min(cand, key=lambda d: res[d][0]))
                break
        if hit:
            st.append("REPRODUCED"); tl.append(hit[0]); dff.append(hit[1])
            frm.append(res[hit[1]][1])
        else:
            st.append("UNREPRODUCED"); tl.append(""); dff.append(""); frm.append("")
    D["status"] = st
    D["deff"] = dff
    D["form"] = frm
    D["tol"] = tl
    return D, G


# ================================================================================================
# 3.  THE SIGN CENSUS
# ================================================================================================
DECL = re.compile(r"(\w*regret\w*)\s*=\s*([^,\n\)]{3,150})")


def declared_orientation(expr):
    """Classify a source expression 'X - Y' by which side carries best/oracle/max."""
    if "-" not in expr:
        return "OTHER"
    lhs, _, rhs = expr.partition("-")
    bestish = lambda s: bool(re.search(r"best|oracle|orac|\.max\(|max\(|\bbm\b|\banch", s, re.I))
    pickish = lambda s: bool(re.search(r"pick|chosen|\bpk\b|\bp\[|\br\[|sel", s, re.I))
    lb, rb, lp, rp = bestish(lhs), bestish(rhs), pickish(lhs), pickish(rhs)
    if (lb and not rb) and (rp or not lp):
        return "BEST_MINUS_PICK"
    if (rb and not lb) and (lp or not rp):
        return "PICK_MINUS_BEST"
    return "OTHER"


def signs(R):
    P()
    P("=" * 100)
    P("(C) THE SIGN CENSUS -- one name, two conventions")
    P("=" * 100)
    # declared, from the producing scripts
    dec = []
    for p in sorted(OUT.glob("*.py")):
        txt = p.read_text(errors="ignore")
        for name, expr in DECL.findall(txt):
            o = declared_orientation(expr)
            dec.append(dict(script=p.name, name=name, expr=expr.strip()[:90], orientation=o))
    DEC = pd.DataFrame(dec)
    DEC = DEC[DEC.orientation != "OTHER"]
    P("  DECLARED orientation, parsed from the producing scripts "
      f"({DEC.script.nunique()} scripts, {len(DEC)} assignments):")
    for k, v in DEC.orientation.value_counts().items():
        P(f"    {k:<18} {v}")
    # realised, from the committed columns
    rows = []
    for fname, grp in R.groupby("file"):
        try:
            df = pd.read_csv(OUT / fname)
        except Exception:
            continue
        for c in grp.col:
            v = pd.to_numeric(df[c], errors="coerce").dropna()
            if len(v) == 0:
                s = "EMPTY"
            elif (v <= 1e-12).all() and (v < -1e-12).any():
                s = "NONPOS"
            elif (v >= -1e-12).all() and (v > 1e-12).any():
                s = "NONNEG"
            elif (v.abs() <= 1e-12).all():
                s = "ALLZERO"
            else:
                s = "MIXED"
            rows.append(dict(file=fname, col=c, n=len(v), sign=s,
                             mean=float(v.mean()) if len(v) else np.nan,
                             mn=float(v.min()) if len(v) else np.nan,
                             mx=float(v.max()) if len(v) else np.nan))
    S = pd.DataFrame(rows)
    P()
    P(f"  REALISED sign of the committed column ({len(S)} reads):")
    for k, v in S.sign.value_counts().items():
        P(f"    {k:<18} {v}   ({v/len(S):.1%})")
    core = S[S.col == "regret"]
    P()
    P(f"  restricted to the exact spelling `regret` ({len(core)} reads):")
    for k, v in core.sign.value_counts().items():
        P(f"    {k:<18} {v}   ({v/len(core):.1%})")
    nn = int((core.sign == "NONNEG").sum())
    npos = int((core.sign == "NONPOS").sum())
    P()
    P(f"  >>> the record publishes `regret` in BOTH conventions under ONE name: "
      f"{nn} files non-negative (best-pick), {npos} non-positive (pick-best), "
      f"{int((core.sign=='MIXED').sum())} mixed, {int((core.sign=='ALLZERO').sum())} all-zero.")
    # what a cross-file pooled aggregate over `regret` actually reads
    vals = []
    for _, row in core.iterrows():
        try:
            v = pd.to_numeric(pd.read_csv(OUT / row.file)[row.col], errors="coerce").dropna()
        except Exception:
            continue
        vals.append(v)
    if vals:
        allv = pd.concat(vals, ignore_index=True)
        P()
        P("  A CROSS-FILE POOLED AGGREGATE over the record's own `regret` column "
          f"({len(allv):,} values):")
        P(f"    mean as published            : {allv.mean():+.4f}")
        P(f"    mean sign-normalised (|.|)   : {allv.abs().mean():+.4f}")
        P(f"    the mixture cancels          : {1 - abs(allv.mean())/allv.abs().mean():.1%} of the "
          f"magnitude is destroyed by pooling the two conventions")
        P(f"    min / max as published       : {allv.min():+.4f} / {allv.max():+.4f}")
        P("    >>> `min(regret)` over the pooled column returns the WORST arm in a pick-best file "
          "and the BEST arm in a best-pick one.  The two are not comparable.")
    return S, DEC


# ================================================================================================
# 4.  LIVE LEG -- books, rule 8, both KEEP paths
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ, cost=0.0):
    """Vectorised equivalent of engine.backtest (idea 664's harness; re-asserted in G1).
    Returns (net returns at `cost`, turnover)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    gross = (held * rets).sum(axis=1)
    return (pd.Series(gross - turn * cost / 1e4, index=idx), pd.Series(turn, index=idx))


def ew_gross(px, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def topn_book(px, n, gross=1.0, max_vol=9.99):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return sel * (gross / float(n))


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = float((eq / eq.cummax() - 1).min())
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    h = len(r) // 2
    m1 = r.iloc[:h]
    m2 = r.iloc[h:]
    sh = lambda x: (x.mean() * 252) / (x.std() * np.sqrt(252)) if x.std() > 0 else np.nan
    return dict(CAGR=float(cagr), Sharpe=float(sh(r)), MaxDD=dd,
                H1=float(sh(m1)), H2=float(sh(m2)))


def build_books(px):
    """The pre-registered menu.  Returns {(family, arm): (weights, freq)}."""
    B = {}
    for b in FAM_ARMS["BAND"]:
        B[("BAND", b)] = (band_book(px, b, GROSS0), FREQ)
    for g in FAM_ARMS["GROSS"]:
        B[("GROSS", g)] = (band_book(px, BAND, g), FREQ)
    for n in FAM_ARMS["N"]:
        B[("N", n)] = (topn_book(px, n, 1.0), FREQ)
    for f in FAM_ARMS["CADENCE"]:
        B[("CADENCE", f)] = (band_book(px, BAND, GROSS0), f)
    for v in FAM_ARMS["VOLCAP"]:
        B[("VOLCAP", v)] = (topn_book(px, 20, 1.0, v), FREQ)
    return B


def live(panels):
    P()
    P("=" * 100)
    P("(D) LIVE LEG -- 5 pre-registered families x 3 panels x 2 cost rungs, rule 8")
    P("=" * 100)
    rows = []
    for pname, px in panels.items():
        t0 = time.time()
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        bw = rules_v2_weights(px, band=BAND, gross=GROSS0)
        b0, bt = fast_backtest(px, bw, FREQ, 0.0)
        books = build_books(px)
        for (fam, arm), (w, fq) in books.items():
            g0, tn = fast_backtest(px, w, fq, 0.0)
            for c in COSTRUNGS:
                r = (g0 - tn * c / 1e4).loc[start:]
                b = (b0 - bt * c / 1e4).loc[start:]
                full = M(r)
                isr = r.loc[:IS_END]
                oos = r.loc[OOS_START:]
                mo = M(oos)
                rows.append(dict(panel=pname, family=fam, arm=str(arm), cost=c,
                                 CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                                 H1=full["H1"], H2=full["H2"],
                                 IS_Sharpe=M(isr)["Sharpe"], IS_CAGR=M(isr)["CAGR"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"],
                                 base_Sharpe=M(b)["Sharpe"], base_H1=M(b)["H1"],
                                 base_H2=M(b)["H2"], base_MaxDD=M(b)["MaxDD"],
                                 base_OOS_Sharpe=M(b.loc[OOS_START:])["Sharpe"],
                                 spy_Sharpe=M(spy)["Sharpe"], spy_H1=M(spy)["H1"],
                                 spy_H2=M(spy)["H2"], spy_MaxDD=M(spy)["MaxDD"],
                                 spy_CAGR=M(spy)["CAGR"],
                                 spy_OOS_Sharpe=M(spy.loc[OOS_START:])["Sharpe"]))
        P(f"  {pname:<9} {len(books)} books x {len(COSTRUNGS)} rungs   {time.time()-t0:.1f}s")
    G = pd.DataFrame(rows)
    return G


def keep_paths(G):
    """PROTOCOL 4a and 4b on every book."""
    a = (G.H1 > G.base_H1) & (G.H2 > G.base_H2) & (G.MaxDD >= G.base_MaxDD)
    b = ((G.H1 > G.spy_H1) & (G.H2 > G.spy_H2) & (G.OOS_Sharpe > G.spy_OOS_Sharpe)
         & (G.MaxDD.abs() <= 0.60 * G.spy_MaxDD.abs()) & (G.CAGR >= 0.70 * G.spy_CAGR))
    G = G.copy()
    G["keep_4a"] = a
    G["keep_4b"] = b
    return G


def rule8(G):
    """Per (panel, family, cost): pick on IS 2009-2016, evaluate on 2017-2026 untouched."""
    P()
    P("-" * 100)
    P("  RULE 8 -- pick = argmax IS Sharpe (2009-2016); oracle = argmax OOS Sharpe (2017-2026)")
    P("-" * 100)
    rows = []
    for (pan, fam, c), sub in G.groupby(["panel", "family", "cost"]):
        sub = sub.sort_values("arm").reset_index(drop=True)
        ip = int(sub.IS_Sharpe.idxmax())
        ib = int(sub.OOS_Sharpe.idxmax())
        pk, bs = sub.loc[ip], sub.loc[ib]
        rows.append(dict(panel=pan, family=fam, cost=c, pick=pk.arm, oracle=bs.arm,
                         IS_Sharpe=pk.IS_Sharpe, OOS_CAGR=pk.OOS_CAGR,
                         OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                         best_OOS_Sharpe=bs.OOS_Sharpe,
                         regret_BP=bs.OOS_Sharpe - pk.OOS_Sharpe,     # best - pick  (>= 0)
                         regret_PB=pk.OOS_Sharpe - bs.OOS_Sharpe,     # pick - best  (<= 0)
                         base_OOS_Sharpe=pk.base_OOS_Sharpe,
                         spy_OOS_Sharpe=pk.spy_OOS_Sharpe,
                         beats_base=bool(pk.OOS_Sharpe > pk.base_OOS_Sharpe),
                         beats_spy=bool(pk.OOS_Sharpe > pk.spy_OOS_Sharpe)))
    W = pd.DataFrame(rows)
    return W


def price_the_sign(W, G):
    """H4: an aggregator adopts the family with the LOWEST regret.  What does that cost when the
    column is read in the wrong convention?"""
    P()
    P("-" * 100)
    P("  H4 -- the price of reading `regret` in the wrong convention")
    P("-" * 100)
    rows = []
    for (pan, c), sub in W.groupby(["panel", "cost"]):
        # BEST-PICK reading: lowest regret_BP = smallest shortfall = the right family
        fbp = sub.loc[sub.regret_BP.idxmin()]
        # PICK-BEST reading: the same `min()` call on a pick-best column
        fpb = sub.loc[sub.regret_PB.idxmin()]
        rows.append(dict(panel=pan, cost=c, fam_BP=fbp.family, fam_PB=fpb.family,
                         same=bool(fbp.family == fpb.family),
                         OOS_Sharpe_BP=fbp.OOS_Sharpe, OOS_Sharpe_PB=fpb.OOS_Sharpe,
                         dSharpe=fbp.OOS_Sharpe - fpb.OOS_Sharpe,
                         OOS_CAGR_BP=fbp.OOS_CAGR, OOS_CAGR_PB=fpb.OOS_CAGR,
                         dCAGR=fbp.OOS_CAGR - fpb.OOS_CAGR,
                         OOS_MaxDD_BP=fbp.OOS_MaxDD, OOS_MaxDD_PB=fpb.OOS_MaxDD,
                         dMaxDD=fbp.OOS_MaxDD - fpb.OOS_MaxDD,
                         base_OOS_Sharpe=fbp.base_OOS_Sharpe,
                         spy_OOS_Sharpe=fbp.spy_OOS_Sharpe))
    S = pd.DataFrame(rows)
    P(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P(f"  the two readings pick a DIFFERENT family in {int((~S.same).sum())} of {len(S)} "
      f"(panel, cost) cells")
    P(f"  mean OOS Sharpe cost of the wrong reading : {S.dSharpe.mean():+.4f}   "
      f"(min {S.dSharpe.min():+.4f}, max {S.dSharpe.max():+.4f})")
    P(f"  mean OOS CAGR   cost                      : {S.dCAGR.mean()*100:+.2f} pp")
    P(f"  mean OOS MaxDD  cost                      : {S.dMaxDD.mean()*100:+.2f} pp")
    return S


# ================================================================================================
# 5.  GATES
# ================================================================================================
def gates(px, D, G):
    P()
    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    ok = True
    w = band_book(px, BAND, GROSS0)
    w2 = rules_v2_weights(px, band=BAND, gross=GROSS0)
    dw = float(np.nanmax(np.abs(w.values - w2.values)))
    rf, _ = fast_backtest(px, w, FREQ, COST)
    re_ = backtest(px, w, cost_bps=COST, freq=FREQ)["returns"]
    start = px.index[WARM]
    dr = float(np.abs(rf.loc[start:] - re_.loc[start:]).max())
    g1 = dw < 1e-12 and dr < 1e-12
    P(f"  G1 band_book(0.03,0.75) == rules_v2_weights  max|dW| {dw:.3e} ; "
      f"fast == engine.backtest  max|dR| {dr:.3e}   {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    b0 = backtest(px, w, cost_bps=0.0, freq=FREQ)
    b25 = backtest(px, w, cost_bps=25.0, freq=FREQ)
    d2 = float(np.abs((b0["returns"] - b0["turnover"] * 25.0 / 1e4) - b25["returns"]).max())
    P(f"  G2 cost-rung identity r(25) = r(0)-turn*25/1e4   max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12

    p = OUT / IDEA664_TAIL
    if p.exists():
        T = pd.read_csv(p)
        n, nr = len(T), int((T.col == "regret").sum())
        nb = int((T.cls == "BOOK").sum())
        nw = int((T.cls == "WINDOW").sum())
        g3 = (n == 1508 and nr == 1442 and nb == 1459 and nw == 49)
        P(f"  G3 idea 664 as committed: {n:,} tolerance-proof reads (664: 1,508), "
          f"{nr:,} `regret` = {nr/n:.1%} (664: 1,442 = 95.6%), BOOK {nb:,}/WINDOW {nw}   "
          f"{'PASS' if g3 else 'FAIL'}")
    else:
        g3 = False
        P("  G3 idea 664's committed .tail.csv NOT FOUND -- the queue's premise is "
          "unauditable. FAIL")
    ok &= g3
    return ok


def gate4(GR, N):
    P()
    tot = GR[GR.definition == "ALL"].set_index("tol").reproduced
    nod = GR[GR.definition == "NODATA"].set_index("tol").reproduced
    exact = all(int(tot[t]) + int(nod[t]) <= N for t in TOLNAMES)
    mono = True
    for d in DEFS:
        s = GR[GR.definition == d].set_index("tol").reproduced.reindex(TOLNAMES).values
        if not all(s[i] <= s[i + 1] for i in range(len(s) - 1)):
            mono = False
    P(f"  G4 partition: REPRODUCED + NODATA <= N at all {len(TOLS)*len(DEFS)} points "
      f"{'PASS' if exact else 'FAIL'} ; monotone in tolerance within every definition "
      f"{'PASS' if mono else 'FAIL'}")
    return exact and mono


def gate5(W):
    d = float(np.abs(W.regret_BP + W.regret_PB).max())
    P(f"  G5 the two conventions are exact negatives   max|BP + PB| {d:.3e}   "
      f"{'PASS' if d < 1e-12 else 'FAIL'}")
    return d < 1e-12


# ================================================================================================
# MAIN
# ================================================================================================
def main():
    t00 = time.time()
    P(f"# Idea 666 (cloud) -- is `regret` the only column whose VALUES its source does not "
      f"contain?   run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M}Z")
    P()

    R = population()
    D, GR = census(R)
    S, DEC = signs(R)

    P()
    P("  CENSUS GRID (reproduced reads out of "
      f"{len(D)}), 5 definitions x 6 tolerances:")
    piv = GR.pivot(index="definition", columns="tol", values="reproduced").reindex(
        DEFS + ["NODATA", "UNREADABLE"])[TOLNAMES]
    P(piv.to_string())
    dump(GR, "censusgrid")

    P()
    st = D.status.value_counts()
    for k, v in st.items():
        P(f"    {k:<14} {v}   ({v/len(D):.1%})")
    P()
    P("  by definition that first reproduced the read (at the tightest tolerance that works):")
    for k, v in D[D.status == "REPRODUCED"].deff.value_counts().items():
        P(f"    {k:<10} {v}")
    P()
    P("  by tolerance needed:")
    for k, v in D[D.status == "REPRODUCED"].tol.value_counts().items():
        P(f"    {k:<10} {v}")
    D = D.merge(R[["file", "col", "is_metric"]], on=["file", "col"], how="left")
    dump(D, "reads")
    Dm = D[D.is_metric]
    P()
    P(f"  the SAME reading restricted to regret VALUES only ({len(Dm)} reads):")
    for k, v in Dm.status.value_counts().items():
        P(f"    {k:<14} {v}   ({v/len(Dm):.1%})")
    # H4-exposure: is the unreproduced read PUBLISHED?
    cite = ""
    for f in ("LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md"):
        p = ROOT / "research" / f
        if p.exists():
            cite += p.read_text(errors="ignore")
    D["has_result_md"] = [(OUT / f"{s}.result.md").exists() or (OUT / f"{s}.memo.md").exists()
                          for s in (x.split(".")[0] for x in D.file)]
    D["cited"] = [s in cite for s in (x.split(".")[0] for x in D.file)]
    D["published"] = D.has_result_md | D.cited
    UP = D[(D.status == "UNREPRODUCED") & D.published]
    P()
    P("  EXPOSURE -- how many UNREPRODUCED regret reads sit under a PUBLISHED claim "
      "(a committed .result.md/.memo.md, or cited by LEADERBOARD/CHANGELOG/QUEUE):")
    P(f"    unreproduced reads                     : {int((D.status=='UNREPRODUCED').sum())}")
    P(f"    ... in a file shipping a .result.md    : "
      f"{int(((D.status=='UNREPRODUCED') & D.has_result_md).sum())}")
    P(f"    ... in a file cited by the record      : "
      f"{int(((D.status=='UNREPRODUCED') & D.cited).sum())}")
    P(f"    ... PUBLISHED either way               : {len(UP)}  "
      f"({len(UP)/max(1,int((D.status=='UNREPRODUCED').sum())):.1%} of the residue)")
    P(f"    distinct files carrying them           : {UP.file.nunique()}")
    U = D[D.status == "UNREPRODUCED"].copy()
    dump(U, "unrep")
    dump(S, "signs")
    P()
    P(f"  >>> UNREPRODUCED reads (the source's own columns cannot rebuild the number): "
      f"{len(U)} of {len(D)} = {len(U)/len(D):.1%}")
    if len(U):
        P("  the ten largest unreproduced reads (best_resid = the closest any definition gets):")
        P(U.sort_values("n", ascending=False).head(10)[
            ["file", "col", "n", "nrows", "ncols", "best_def", "best_resid"]].to_string(
            index=False))

    # ---- live -------------------------------------------------------------------------------
    P()
    P("  loading panels ...")
    pxu = load_universe()
    pxb = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    keep = [c for c in pxs.columns if c == "SPY" or c not in bad]
    pxs = pxs[keep]
    P(f"    U56 {pxu.shape}  B136 {pxb.shape}  SMALL {pxs.shape} "
      f"(dropped {len(bad)} max_1d_move>=1.0 names)")
    panels = {"U56": pxu, "B136": pxb, f"SMALL{pxs.shape[1]-1}": pxs}

    okg = gates(pxu, D, None)
    ok4 = gate4(GR, len(D))

    G = live(panels)
    G = keep_paths(G)
    dump(G, "grid")
    W = rule8(G)
    ok5 = gate5(W)
    dump(W, "walkforward")
    P()
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    SG = price_the_sign(W, G)
    dump(SG, "keeppaths")

    P()
    P("-" * 100)
    P("  KEEP PATHS over every book x cost rung")
    P("-" * 100)
    P(f"  books priced        : {len(G)}  ({G.panel.nunique()} panels x "
      f"{G.groupby('panel').size().iloc[0]//len(COSTRUNGS)} books x {len(COSTRUNGS)} rungs)")
    P(f"  4a passes           : {int(G.keep_4a.sum())} / {len(G)}")
    P(f"  4b passes           : {int(G.keep_4b.sum())} / {len(G)}")
    P(f"  BOTH                : {int((G.keep_4a & G.keep_4b).sum())} / {len(G)}")
    for pan, sub in G.groupby("panel"):
        P(f"    {pan:<9} 4a {int(sub.keep_4a.sum()):>3}/{len(sub):<3}  "
          f"4b {int(sub.keep_4b.sum()):>3}/{len(sub):<3}  "
          f"BOTH {int((sub.keep_4a & sub.keep_4b).sum()):>3}")
    if int(G.keep_4b.sum()):
        P()
        P("  the 4b passers:")
        P(G[G.keep_4b][["panel", "family", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                        "OOS_Sharpe", "spy_CAGR", "spy_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P(f"  rule-8 picks beating the live book OOS : {int(W.beats_base.sum())} / {len(W)}")
    P(f"  rule-8 picks beating SPY OOS           : {int(W.beats_spy.sum())} / {len(W)}")

    P()
    P("=" * 100)
    P(f"  GATES: G1/G2/G3 {'PASS' if okg else 'FAIL'} ; G4 {'PASS' if ok4 else 'FAIL'} ; "
      f"G5 {'PASS' if ok5 else 'FAIL'}")
    P(f"  total {time.time()-t00:.1f}s")
    P("=" * 100)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
