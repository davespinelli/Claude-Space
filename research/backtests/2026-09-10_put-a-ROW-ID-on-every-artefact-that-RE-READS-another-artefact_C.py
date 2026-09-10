#!/usr/bin/env python3
"""Idea 655 (lane C, 2026-09-10) -- put a ROW ID on every artefact that RE-READS another artefact.

QUEUE 655: "idea 653 found the record's single largest unreadable block (105,303 rows, 97.7% of
all panel-unstated rows) is dark not for want of a panel column but because its `file` pointer
carries no row id and 99.7% of its sources are multi-panel.  Census every committed CSV whose
columns include a file/source pointer, report how many can be joined row-wise to their source,
and price a `src_rowid` convention.  INFRASTRUCTURE; max 2 params (pointer form, join strictness)."

WHAT IS ACTUALLY BEING TESTED
  H1 (population)   The record's re-reading artefacts are a countable population: committed CSVs
        that carry a column whose VALUES name another committed artefact.  Measured, not asserted:
        a header regex alone is not evidence (`parent_gross` is a number), so every instance must
        clear a value-resolution bar as well.
  H2 (darkness)     A pointer without a row id leaves the row unaddressable.  FALSIFIABLE: if the
        child's own non-pointer columns already pick out exactly one source row, the block is not
        dark at all and the queue's diagnosis of 653's 105,303 rows is wrong.
  H3 (price)        A `src_rowid` convention is cheap relative to what it recovers.  Both sides are
        counted: rows it would newly address, and bytes it would add to the corpus.
  H4 (live cost)    ROW-LEVEL resolution is worth paying for where PROTOCOL lets anything be paid
        for -- in a book.  The artefact question "do you know WHICH row, or only HOW MANY?" has an
        exact price analogue: a gate that knows WHICH names are in their 200d band (RULES v2, row
        resolution) vs one that knows only WHAT SHARE of them are (breadth, aggregate resolution)
        vs one that has both.  If aggregate resolution matches row resolution out of sample, then
        row identity is cosmetic in the only place the record can price it.  FALSIFIABLE either way.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 POINTER FORM  : STRICT (header is exactly one of file/files/src/source/path/artefact and
                               >=VALBAR of its values resolve to a committed artefact)
                       LOOSE  (header matches the record's pointer vocabulary -- adds stem, script,
                               parent, join_file, line_src, ... -- same value bar)
                       VALUE  (ANY column, whatever its header, clearing the same value bar)
                       Nested by construction: STRICT c LOOSE c VALUE (asserted in G4).
    P2 JOIN STRICTNESS: J0 RESOLVE     the pointer names a committed artefact (no row identity)
                        J1 KEY-UNIQUE  the child row's shared-column key tuple matches EXACTLY ONE
                                       row of the source (the join a reader could actually do)
                        J2 ROWID       the child carries an explicit row-id column
                        Nested downward in what they admit; all three reported at every P1 level.
  => 3 x 3 = 9 grid points, every one written to .censusgrid.csv.
  REPORTED, NOT TUNED: the value bar, the float normalisation tolerance, the live grid's panels,
  modes, thresholds, grosses, cadence and cost rungs.  Nothing is chosen by looking at an outcome
  except inside rule 8.

GATES (run before any new number is read; a failure stops the run)
  G1 the ROW-resolution book reproduces `baseline.rules_v2_weights` exactly (weights AND returns).
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 against a live engine.backtest(25 bps).
  G3 idea 653's ladder is reproduced off its OWN committed artefacts: 96 pinned blocks, 370,102
     rows, 107,816 unstated at L0, 105,303 at L4, and the survivor is ONE file.  Its row count is
     then recounted independently from the CSV itself.
  G4 the P1 ladder is nested (STRICT c LOOSE c VALUE) on instances and on rows.

Deterministic, standalone, no network, ~6 min.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .pointers.csv .censusgrid.csv .join.csv .pricing.csv .grid.csv
       .walkforward.csv .keeppaths.csv
Modifies nothing (RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md untouched).
"""
import collections
import csv
import os
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
VALBAR = 0.50            # share of a column's non-empty values that must resolve to an artefact
FLOATDP = 10             # decimal places a numeric cell is rounded to before keying
COST = 10.0              # PROTOCOL 2
FREQ = "W"
BAND = 0.03              # RULES v2 clause 2
IS_END, OOS_START = "2016-12-31", "2017-01-01"
THETAS = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
GROSSES = [0.50, 0.75, 1.00]
MODES = ["ROW", "AGG", "HYB"]
COSTRUNGS = [0.0, 10.0, 25.0]
ROWID_BYTES = 6          # "12345," -- the per-row cost of the proposed convention

STRICT_NAMES = {"file", "files", "src", "source", "path", "artefact", "artifact"}
HDRPAT = re.compile(r"(^|_)(file|files|src|source|path|stem|script|artefact|artifact|parent)(_|$)", re.I)
ROWIDPAT = re.compile(
    r"^(src_?row(_?id)?|source_?row(_?id)?|row(_?id|_?no|_?num|_?idx)?|rowid"
    r"|line(_?no|_?num)?|lineno|idx|index|i|orig_row)$", re.I)

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 0.  ARTEFACT INDEX
# ================================================================================================
def build_index():
    """basename -> path, over every committed artefact the record can point at.

    Ambiguous basenames (same name under two directories) are dropped rather than guessed."""
    seen = collections.defaultdict(list)
    for base in ("research", "products", "docs"):
        d = ROOT / base
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                seen[p.name].append(p)
    for p in ROOT.glob("*.md"):
        seen[p.name].append(p)
    idx, amb = {}, 0
    for name, paths in seen.items():
        if len(paths) == 1:
            idx[name] = paths[0]
        else:
            bt = [q for q in paths if q.parent.name == "backtests"]
            if len(bt) == 1:
                idx[name] = bt[0]
            else:
                amb += 1
    return idx, amb


IDX, AMBIG_NAMES = {}, 0


def resolve(v):
    v = (v or "").strip().strip('"').strip("'")
    if not v or len(v) > 300:
        return None
    return IDX.get(os.path.basename(v)) or IDX.get(v)


# ================================================================================================
# 1.  GATES
# ================================================================================================
def row_weights(px, gross, band=BAND):
    """ROW resolution: hold every name whose OWN band state is IN, gross/N of NAV, cash otherwise."""
    priced = px.notna()
    inb = band_state(px, band) & priced
    n = priced.sum(axis=1).replace(0, np.nan)
    ew = gross * priced.astype(float).div(n, axis=0).fillna(0.0)
    return ew.where(inb, 0.0)


def breadth(px, band=BAND):
    priced = px.notna()
    inb = band_state(px, band) & priced
    return (inb.sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)).fillna(0.0)


def agg_weights(px, theta, gross, band=BAND):
    """AGGREGATE resolution: knows only HOW MANY names are in band, never WHICH.  Holds the whole
    priced panel equal-weighted at `gross` when breadth >= theta, else all cash."""
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    ew = gross * priced.astype(float).div(n, axis=0).fillna(0.0)
    return ew.mul((breadth(px, band) >= theta).astype(float), axis=0)


def hyb_weights(px, theta, gross, band=BAND):
    """BOTH resolutions: the row-level book, switched off entirely when breadth < theta."""
    return row_weights(px, gross, band).mul((breadth(px, band) >= theta).astype(float), axis=0)


def book(px, mode, theta, gross):
    if mode == "ROW":
        return row_weights(px, gross)
    if mode == "AGG":
        return agg_weights(px, theta, gross)
    return hyb_weights(px, theta, gross)


def gates(px):
    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    ok = True

    # G1 -- ROW resolution IS RULES v2
    w_row, w_v2 = row_weights(px, 0.75), rules_v2_weights(px, band=BAND, gross=0.75)
    dw = float(np.nanmax(np.abs(w_row.values - w_v2.values)))
    r1 = backtest(px, w_row, cost_bps=COST, freq=FREQ)["returns"]
    r2 = backtest(px, w_v2, cost_bps=COST, freq=FREQ)["returns"]
    dr = float(np.abs(r1 - r2).max())
    P(f"  G1 ROW book == rules_v2_weights : max|dW| {dw:.3e}   max|dR| {dr:.3e}   "
      f"{'PASS' if dw < 1e-12 and dr < 1e-12 else 'FAIL'}")
    ok &= dw < 1e-12 and dr < 1e-12

    # G2 -- cost-rung identity
    b0 = backtest(px, w_row, cost_bps=0.0, freq=FREQ)
    b25 = backtest(px, w_row, cost_bps=25.0, freq=FREQ)
    ident = b0["returns"] - b0["turnover"] * 25.0 / 1e4
    d2 = float(np.abs(ident - b25["returns"]).max())
    P(f"  G2 cost-rung identity r(25) = r(0)-turn*25/1e4 : max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12

    # G3 -- idea 653's ladder off its own committed artefacts
    lad = OUT / "2026-09-10_how-many-committed-GRID-files-cannot-state-their-own-PANEL_C.ladder.csv"
    blk = OUT / "2026-09-10_how-many-committed-GRID-files-cannot-state-their-own-PANEL_C.blocks.csv"
    dark_file, dark_rows = None, None
    if lad.exists() and blk.exists():
        L = pd.read_csv(lad)
        L = L[L.population.str.startswith("PINNED")].set_index("level")
        B = pd.read_csv(blk)
        l0, l4 = int(L.loc["L0_DECLARED", "rows_unstated"]), int(L.loc["L4_SCRIPT", "rows_unstated"])
        nf = int(L.loc["L0_DECLARED", "files_total"])
        surv = B[B.L4_SCRIPT.astype(float) < B.n.astype(float)]
        g3 = (nf == 96 and l0 == 107816 and l4 == 105303 and len(surv) == 1)
        dark_file = surv.iloc[0]["file"] if len(surv) == 1 else None
        dark_rows = int(surv.iloc[0]["n"]) - int(surv.iloc[0]["L4_SCRIPT"]) if len(surv) == 1 else None
        P(f"  G3 idea 653 ladder : blocks {nf}  rows_unstated L0 {l0}  L4 {l4}  "
          f"share {l4 / l0:.4f}  survivors {len(surv)}   {'PASS' if g3 else 'FAIL'}")
        P(f"     dark block = {dark_file}  ({dark_rows} rows dark of {int(surv.iloc[0]['n'])})")
        # independent recount straight off the CSV
        p = IDX.get(dark_file)
        if p is not None and p.exists():
            with open(p, newline="") as fh:
                rd = csv.reader(fh)
                next(rd)
                n_re = sum(1 for _ in rd)
            P(f"     independent recount of that CSV : {n_re} rows   "
              f"{'PASS' if n_re == int(surv.iloc[0]['n']) else 'FAIL'}")
            g3 &= n_re == int(surv.iloc[0]["n"])
        ok &= g3
    else:
        P("  G3 idea 653 artefacts NOT FOUND -- the queue's premise cannot be audited.  STOP.")
        ok = False
    return ok, dark_file


# ================================================================================================
# 2.  CENSUS A -- the pointer population (P1)
# ================================================================================================
def census_pointers():
    P()
    P("=" * 100)
    P("(A) CENSUS -- every committed CSV that RE-READS another artefact")
    P("=" * 100)
    csvs = sorted(OUT.glob("*.csv")) + sorted((ROOT / "research").glob("*.csv"))
    P(f"  committed CSVs scanned          : {len(csvs)}")
    P(f"  artefact index (unique basenames): {len(IDX)}   ambiguous basenames dropped: {AMBIG_NAMES}")

    inst, t0 = [], time.time()
    for f in csvs:
        try:
            with open(f, newline="") as fh:
                rd = csv.reader(fh)
                hdr = next(rd, None)
                if not hdr:
                    continue
                data = [r for r in rd]
        except Exception:
            continue
        if not data:
            continue
        rowid_cols = [h.strip() for h in hdr if ROWIDPAT.match(h.strip())]
        # VALUE prefilter: only test a column whose first non-empty cell resolves
        for j, h in enumerate(hdr):
            hn = h.strip()
            first = next((r[j] for r in data if j < len(r) and r[j].strip()), None)
            if first is None or resolve(first) is None:
                continue
            vals = [r[j] for r in data if j < len(r) and r[j].strip()]
            res = [resolve(v) for v in vals]
            nres = sum(1 for x in res if x is not None)
            if nres / len(vals) < VALBAR:
                continue
            form = ("STRICT" if hn.lower() in STRICT_NAMES
                    else "LOOSE" if HDRPAT.search(hn) else "VALUE")
            kinds = collections.Counter(x.suffix.lower() for x in res if x is not None)
            inst.append(dict(file=f.name, col=hn, form=form, rows=len(vals), resolved=nres,
                             n_src=len(set(x for x in res if x is not None)),
                             n_csv=kinds.get(".csv", 0), n_py=kinds.get(".py", 0),
                             n_md=kinds.get(".md", 0),
                             has_rowid_col=bool(rowid_cols), rowid_cols="|".join(rowid_cols)))
    D = pd.DataFrame(inst)
    P(f"  scan time {time.time() - t0:.1f}s")
    P(f"  pointer INSTANCES (column x file) : {len(D)}   over {D.file.nunique()} distinct files")
    P(f"  pointer ROWS                      : {D.rows.sum():,}   "
      f"resolving to a committed artefact: {D.resolved.sum():,} "
      f"({D.resolved.sum() / D.rows.sum():.4f})")
    P()
    P("  by pointer FORM (P1 is CUMULATIVE: STRICT c LOOSE c VALUE):")
    for form in ("STRICT", "LOOSE", "VALUE"):
        s = D[D.form == form]
        P(f"    {form:7s} exclusive  instances {len(s):4d}  files {s.file.nunique():4d}  "
          f"rows {s.rows.sum():>9,}")
    P()
    P("  what the pointers POINT AT (rows):")
    P(f"    -> a committed .csv : {D.n_csv.sum():>9,}  ({D.n_csv.sum() / D.rows.sum():.4f})")
    P(f"    -> a committed .py  : {D.n_py.sum():>9,}  ({D.n_py.sum() / D.rows.sum():.4f})")
    P(f"    -> a committed .md  : {D.n_md.sum():>9,}  ({D.n_md.sum() / D.rows.sum():.4f})")
    P()
    P("  10 largest pointer instances:")
    for _, r in D.nlargest(10, "rows").iterrows():
        P(f"    {r.file[:66]:68s} {r.col:10s} {r.form:6s} rows {r.rows:>7,} srcs {r.n_src:>4d}")
    return D


# ================================================================================================
# 3.  CENSUS B -- the join ladder (P2)
# ================================================================================================
_SRC = {}


def load_src(p):
    key = str(p)
    if key in _SRC:
        return _SRC[key]
    try:
        with open(p, newline="") as fh:
            rd = csv.reader(fh)
            h = next(rd)
            rows = [r for r in rd]
    except Exception:
        h, rows = None, None
    if len(_SRC) > 400:                      # bounded cache, deterministic (insertion order)
        _SRC.pop(next(iter(_SRC)))
    _SRC[key] = (h, rows)
    return h, rows


def nz(x):
    x = (x or "").strip()
    try:
        return round(float(x), FLOATDP)
    except Exception:
        return x


def join_instance(fpath, hdr, data, ptrcol):
    """Classify every pointer row of one instance into the J-ladder."""
    j = hdr.index(ptrcol)
    out = dict(rows=0, resolve=0, unique=0, ambig=0, nokey=0, miss=0, nonrow=0,
               src_multi=0, src_single=0, rowid=0)
    rowid_cols = [h.strip() for h in hdr if ROWIDPAT.match(h.strip())]
    bysrc = collections.defaultdict(list)
    for r in data:
        if j >= len(r) or not r[j].strip():
            continue
        out["rows"] += 1
        s = resolve(r[j])
        if s is None:
            continue
        out["resolve"] += 1
        bysrc[s].append(r)
    for s, rows in bysrc.items():
        if s.suffix.lower() != ".csv":
            out["nonrow"] += len(rows)          # a .py/.md has lines, not rows
            continue
        sh, sr = load_src(s)
        if sh is None:
            out["nonrow"] += len(rows)
            continue
        if len(sr) <= 1:
            out["src_single"] += len(rows)
            out["unique"] += len(rows)          # trivially addressable
            continue
        out["src_multi"] += len(rows)
        shared = [c for c in hdr if c != ptrcol and c.strip() in [x.strip() for x in sh]]
        if not shared:
            out["nokey"] += len(rows)
            continue
        sn = [x.strip() for x in sh]
        si = [sn.index(c.strip()) for c in shared]
        ci = [hdr.index(c) for c in shared]
        idx = collections.Counter(
            tuple(nz(r[k]) if k < len(r) else "" for k in si) for r in sr)
        for r in rows:
            key = tuple(nz(r[k]) if k < len(r) else "" for k in ci)
            c = idx.get(key, 0)
            if c == 1:
                out["unique"] += 1
            elif c > 1:
                out["ambig"] += 1
            else:
                out["miss"] += 1
    if rowid_cols:
        out["rowid"] = out["resolve"]
    return out


def census_join(D):
    P()
    P("=" * 100)
    P("(B) JOIN LADDER -- can the row be addressed at all?")
    P("=" * 100)
    P("  J0 RESOLVE     the pointer names a committed artefact")
    P("  J1 KEY-UNIQUE  the child row's shared-column key tuple hits EXACTLY ONE source row")
    P("  J2 ROWID       the child carries an explicit row-id column")
    P()
    recs, t0 = [], time.time()
    for _, inst in D.iterrows():
        f = IDX.get(inst.file)
        if f is None:
            continue
        with open(f, newline="") as fh:
            rd = csv.reader(fh)
            hdr = next(rd)
            data = [r for r in rd]
        o = join_instance(f, hdr, data, inst.col)
        o.update(file=inst.file, col=inst.col, form=inst.form)
        recs.append(o)
    J = pd.DataFrame(recs)
    P(f"  join time {time.time() - t0:.1f}s over {len(J)} instances")
    P()
    tot = J.rows.sum()
    P(f"  pointer rows                              {tot:>9,}")
    P(f"  J0 resolve to a committed artefact        {J.resolve.sum():>9,}  "
      f"({J.resolve.sum() / tot:.4f})")
    P(f"     ... of which target is NOT row-shaped  {J.nonrow.sum():>9,}  "
      f"({J.nonrow.sum() / tot:.4f})   (.py/.md: a LINE is its row id)")
    P(f"     ... target CSV has exactly 1 row       {J.src_single.sum():>9,}  "
      f"({J.src_single.sum() / tot:.4f})   (trivially addressable)")
    P(f"     ... target CSV has MANY rows           {J.src_multi.sum():>9,}  "
      f"({J.src_multi.sum() / tot:.4f})   <- the population at risk")
    P()
    P(f"  J1 KEY-UNIQUE  (exactly one source row)   {J.unique.sum():>9,}  "
      f"({J.unique.sum() / tot:.4f})")
    P(f"     AMBIGUOUS   (key hits >1 source row)   {J.ambig.sum():>9,}  "
      f"({J.ambig.sum() / tot:.4f})")
    P(f"     NO SHARED KEY COLUMN AT ALL            {J.nokey.sum():>9,}  "
      f"({J.nokey.sum() / tot:.4f})")
    P(f"     KEY MISSES the source entirely         {J.miss.sum():>9,}  "
      f"({J.miss.sum() / tot:.4f})")
    P(f"  J2 ROWID       (explicit row-id column)   {J.rowid.sum():>9,}  "
      f"({J.rowid.sum() / tot:.4f})")
    return J


def census_grid(D, J):
    P()
    P("=" * 100)
    P("(C) THE 3 x 3 GRID -- every point reported (P1 pointer form x P2 join strictness)")
    P("=" * 100)
    rows = []
    ladder = {"STRICT": ["STRICT"], "LOOSE": ["STRICT", "LOOSE"],
              "VALUE": ["STRICT", "LOOSE", "VALUE"]}
    for p1 in ("STRICT", "LOOSE", "VALUE"):
        s = J[J.form.isin(ladder[p1])]
        n_rows = s.rows.sum()
        for p2, col in (("J0_RESOLVE", "resolve"), ("J1_KEYUNIQUE", "unique"), ("J2_ROWID", "rowid")):
            rows.append(dict(pointer_form=p1, join=p2, instances=len(s), files=s.file.nunique(),
                             rows=int(n_rows), addressable=int(s[col].sum()),
                             share=float(s[col].sum() / n_rows) if n_rows else np.nan,
                             at_risk=int(s.src_multi.sum()),
                             at_risk_dark=int(s.src_multi.sum() - (s.unique.sum() - s.src_single.sum()))))
    G = pd.DataFrame(rows)
    P(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    # G4 nesting
    piv = G.pivot(index="join", columns="pointer_form", values="addressable")
    nested = bool((piv["STRICT"] <= piv["LOOSE"]).all() and (piv["LOOSE"] <= piv["VALUE"]).all())
    P(f"\n  G4 P1 ladder nested (STRICT <= LOOSE <= VALUE) on addressable rows : "
      f"{'PASS' if nested else 'FAIL'}")
    return G, nested


# ================================================================================================
# 4.  PRICING THE src_rowid CONVENTION
# ================================================================================================
def pricing(J, dark_file):
    P()
    P("=" * 100)
    P("(D) PRICING a `src_rowid` CONVENTION")
    P("=" * 100)
    tot = J.rows.sum()
    # what it would recover: rows pointing at a MULTI-row CSV that are not already key-unique
    keyed_multi = J.unique.sum() - J.src_single.sum()
    dark = J.src_multi.sum() - keyed_multi
    corpus_bytes = sum(f.stat().st_size for f in OUT.glob("*.csv"))
    add_bytes = tot * ROWID_BYTES
    P(f"  rows at risk (point at a multi-row CSV)   {J.src_multi.sum():>9,}")
    P(f"  ... already KEY-UNIQUE without a row id   {keyed_multi:>9,}  "
      f"({keyed_multi / max(J.src_multi.sum(), 1):.4f})")
    P(f"  ... DARK, recoverable only by a row id    {dark:>9,}  "
      f"({dark / max(J.src_multi.sum(), 1):.4f})")
    P()
    P(f"  cost: {ROWID_BYTES} bytes/row x {tot:,} pointer rows = {add_bytes / 1e6:.2f} MB")
    P(f"        committed backtests/*.csv corpus    = {corpus_bytes / 1e6:.2f} MB")
    P(f"        => +{100 * add_bytes / corpus_bytes:.3f}% of the CSV corpus, "
      f"{dark / max(add_bytes / 1e6, 1e-9):,.0f} dark rows recovered per MB")
    P()
    already = J[J.rowid > 0]
    P(f"  the convention PARTLY EXISTS already: {len(already)} of {len(J)} instances carry a "
      f"row-id-shaped column ({already.rows.sum():,} rows, {already.rows.sum() / tot:.4f})")
    if len(already):
        nonrow_share = already.nonrow.sum() / max(already.rows.sum(), 1)
        P(f"  but {nonrow_share:.4f} of THOSE rows point at a .py/.md -- the record already stamps a "
          f"`line` on SOURCE-CODE pointers and does not stamp a row on CSV pointers.")
    P()
    if dark_file is not None:
        s = J[J.file == dark_file]
        if len(s):
            r = s.iloc[0]
            P(f"  THE QUEUE'S OWN BLOCK -- {dark_file}")
            nr, nu = int(r["rows"]), int(r["unique"])
            na, nk, nm = int(r["ambig"]), int(r["nokey"]), int(r["miss"])
            P(f"    pointer rows {nr:,}   key-unique {nu:,} ({nu / nr:.4f})   "
              f"ambiguous {na:,} ({na / nr:.4f})   no shared key {nk:,} ({nk / nr:.4f})   "
              f"key misses {nm:,} ({nm / nr:.4f})")
            P(f"    => the block is NOT wholly dark: {nu / nr:.1%} of its rows are already "
              f"row-addressable from the artefacts as committed, with no row id at all.")
    return pd.DataFrame([dict(pointer_rows=int(tot), at_risk=int(J.src_multi.sum()),
                              key_unique_multi=int(keyed_multi), dark=int(dark),
                              rowid_bytes=ROWID_BYTES, add_MB=add_bytes / 1e6,
                              corpus_MB=corpus_bytes / 1e6,
                              pct_corpus=100 * add_bytes / corpus_bytes,
                              instances_with_rowid=int(len(already)),
                              rows_with_rowid=int(already.rows.sum()))])


# ================================================================================================
# 5.  H4 -- ROW vs AGGREGATE RESOLUTION, PRICED (full grid, then PROTOCOL rule 8)
# ================================================================================================
def slice_metrics(r):
    m = metrics(r)
    h = len(r) // 2
    return m["CAGR"], m["Sharpe"], m["MaxDD"], metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4b(cagr, sh, dd, h1, h2, oos_sh, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    return bool(h1 > spy["H1"] and h2 > spy["H2"] and oos_sh > spy["OOS_Sharpe"]
                and dd >= 0.60 * spy["MaxDD"] and cagr >= 0.70 * spy["CAGR"])


def pass4a(sh, dd, h1, h2, base):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves, MaxDD no worse."""
    return bool(h1 > base["H1"] and h2 > base["H2"] and dd >= base["MaxDD"])


def live(panels):
    P()
    P("=" * 100)
    P("(E) H4 -- what ROW-LEVEL RESOLUTION is worth in a book")
    P("=" * 100)
    P("  ROW  knows WHICH names are in their 200d +/-3% band (= RULES v2)")
    P("  AGG  knows only HOW MANY (breadth >= theta -> hold the whole priced panel, else cash)")
    P("  HYB  knows both")
    P("  Full-sample 4a/4b at every grid point; rule 8 then fits (theta, gross) on 2009-2016 ONLY.")
    P()
    grid, wf = [], []
    for pname, px in panels.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
        ref = {}
        for nm, r in (("SPY", spy_r), ("V2", base_r)):
            c, s, d, h1, h2 = slice_metrics(r)
            o = metrics(r.loc[OOS_START:])
            ref[nm] = dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2, OOS_Sharpe=o["Sharpe"],
                           OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"])
        P(f"  --- {pname} ({px.shape[1]} cols, {start.date()} -> {px.index[-1].date()}) ---")
        P(f"      SPY   CAGR {ref['SPY']['CAGR']:7.2%}  Sharpe {ref['SPY']['Sharpe']:.3f}  "
          f"MaxDD {ref['SPY']['MaxDD']:7.2%}  H1/H2 {ref['SPY']['H1']:.3f}/{ref['SPY']['H2']:.3f}  "
          f"OOS Sh {ref['SPY']['OOS_Sharpe']:.3f}")
        P(f"      V2    CAGR {ref['V2']['CAGR']:7.2%}  Sharpe {ref['V2']['Sharpe']:.3f}  "
          f"MaxDD {ref['V2']['MaxDD']:7.2%}  H1/H2 {ref['V2']['H1']:.3f}/{ref['V2']['H2']:.3f}  "
          f"OOS Sh {ref['V2']['OOS_Sharpe']:.3f}")

        for mode in MODES:
            thetas = [0.00] if mode == "ROW" else THETAS
            for th in thetas:
                for g in GROSSES:
                    b = backtest(px, book(px, mode, th, g), cost_bps=COST, freq=FREQ)
                    r = b["returns"].loc[start:]
                    c, s, d, h1, h2 = slice_metrics(r)
                    o = metrics(r.loc[OOS_START:])
                    isr = r.loc[:IS_END]
                    im = metrics(isr)
                    grid.append(dict(panel=pname, mode=mode, theta=th, gross=g, cost=COST,
                                     CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                                     IS_Sharpe=im["Sharpe"], IS_CAGR=im["CAGR"], IS_MaxDD=im["MaxDD"],
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     turn_x_yr=b["turnover"].loc[start:].sum() / (len(r) / 252),
                                     pass4a=pass4a(s, d, h1, h2, ref["V2"]),
                                     pass4b=pass4b(c, s, d, h1, h2, o["Sharpe"], ref["SPY"])))
        Gp = pd.DataFrame([x for x in grid if x["panel"] == pname])
        P(f"      grid points {len(Gp)}   4a {int(Gp.pass4a.sum())}/{len(Gp)}   "
          f"4b {int(Gp.pass4b.sum())}/{len(Gp)}")
        for mode in MODES:
            s = Gp[Gp["mode"] == mode]
            P(f"        {mode:4s} n={len(s):3d}  Sharpe [{s.Sharpe.min():.3f}, {s.Sharpe.max():.3f}]  "
              f"CAGR [{s.CAGR.min():7.2%}, {s.CAGR.max():7.2%}]  "
              f"4a {int(s.pass4a.sum())}  4b {int(s.pass4b.sum())}")

        # ---- PROTOCOL rule 8 ---------------------------------------------------------------
        P(f"      rule 8: fit (theta, gross) on 2009-2016 by IS Sharpe, score 2017-2026 untouched")
        for mode in MODES:
            s = Gp[Gp["mode"] == mode]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            # the mode's own no-resolution control at the same gross: AGG theta=0 == buy-and-hold panel
            ctl = Gp[(Gp["mode"] == "AGG") & (Gp.theta == 0.00) & (Gp.gross == pick.gross)].iloc[0]
            rung = {}
            for c in COSTRUNGS:
                rr = backtest(px, book(px, mode, pick.theta, pick.gross),
                              cost_bps=c, freq=FREQ)["returns"].loc[start:]
                oo = metrics(rr.loc[OOS_START:])
                cc, ss, dd, hh1, hh2 = slice_metrics(rr)
                rung[c] = dict(OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"], OOS_MaxDD=oo["MaxDD"],
                               p4b=pass4b(cc, ss, dd, hh1, hh2, oo["Sharpe"], ref["SPY"]),
                               p4a=pass4a(ss, dd, hh1, hh2, ref["V2"]))
            wf.append(dict(panel=pname, mode=mode, pick_theta=pick.theta, pick_gross=pick.gross,
                           IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                           V2_OOS_Sharpe=ref["V2"]["OOS_Sharpe"], V2_OOS_CAGR=ref["V2"]["OOS_CAGR"],
                           V2_OOS_MaxDD=ref["V2"]["MaxDD"],
                           SPY_OOS_Sharpe=ref["SPY"]["OOS_Sharpe"], SPY_OOS_CAGR=ref["SPY"]["OOS_CAGR"],
                           SPY_OOS_MaxDD=ref["SPY"]["OOS_MaxDD"],
                           beats_SPY=bool(pick.OOS_Sharpe > ref["SPY"]["OOS_Sharpe"]),
                           beats_V2=bool(pick.OOS_Sharpe > ref["V2"]["OOS_Sharpe"]),
                           full_4a=bool(pick.pass4a), full_4b=bool(pick.pass4b),
                           p4b_0=rung[0.0]["p4b"], p4b_10=rung[10.0]["p4b"], p4b_25=rung[25.0]["p4b"],
                           p4a_0=rung[0.0]["p4a"], p4a_10=rung[10.0]["p4a"], p4a_25=rung[25.0]["p4a"]))
            P(f"        {mode:4s} pick theta={pick.theta:.2f} g={pick.gross:.2f} "
              f"(IS Sh {pick.IS_Sharpe:.3f}) -> OOS CAGR {pick.OOS_CAGR:7.2%} Sharpe "
              f"{pick.OOS_Sharpe:.3f} MaxDD {pick.OOS_MaxDD:7.2%}   "
              f"4a {'Y' if pick.pass4a else 'n'} 4b {'Y' if pick.pass4b else 'n'}   "
              f"4b@0/10/25 {int(rung[0.0]['p4b'])}/{int(rung[10.0]['p4b'])}/{int(rung[25.0]['p4b'])}")
        P()
    return pd.DataFrame(grid), pd.DataFrame(wf)


# ================================================================================================
def main():
    global IDX, AMBIG_NAMES
    t0 = time.time()
    P(f"Idea 655 -- put a ROW ID on every artefact that RE-READS another artefact  (lane C, "
      f"{pd.Timestamp.today().date()})")
    P(f"PROTOCOL: costs {COST:.0f} bps, next-day execution, freq {FREQ}, "
      f"rule 8 IS<= {IS_END} / OOS >= {OOS_START}.  2 params: pointer form x join strictness.")
    P()
    IDX, AMBIG_NAMES = build_index()

    px_u = load_universe()
    px_b = load_universe(broad=True)
    ok, dark_file = gates(px_u)
    if not ok:
        P("\nGATES FAILED -- stopping before any new number is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return

    D = census_pointers()
    J = census_join(D)
    G, nested = census_grid(D, J)
    PR = pricing(J, dark_file)
    grid, wf = live({"U56": px_u, "B136": px_b})

    P()
    P("=" * 100)
    P("(F) KEEP PATHS -- PROTOCOL 4a and 4b on every live grid point")
    P("=" * 100)
    kp = grid.groupby(["panel", "mode"]).agg(points=("pass4a", "size"),
                                             p4a=("pass4a", "sum"),
                                             p4b=("pass4b", "sum")).reset_index()
    P(kp.to_string(index=False))
    P(f"\n  TOTAL: 4a {int(grid.pass4a.sum())}/{len(grid)}   4b {int(grid.pass4b.sum())}/{len(grid)}")
    P(f"  rule-8 picks that clear 4b at 10 bps: {int(wf.p4b_10.sum())}/{len(wf)};  "
      f"at 25 bps: {int(wf.p4b_25.sum())}/{len(wf)};  4a at 10 bps: {int(wf.p4a_10.sum())}/{len(wf)}")

    P()
    P("=" * 100)
    P("OUTPUTS")
    P("=" * 100)
    dump(D, "pointers")
    dump(J, "join")
    dump(G, "censusgrid")
    dump(PR, "pricing")
    dump(grid, "grid")
    dump(wf, "walkforward")
    dump(kp, "keeppaths")
    P(f"\ntotal {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
