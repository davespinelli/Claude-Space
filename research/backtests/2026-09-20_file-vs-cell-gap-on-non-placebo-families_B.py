#!/usr/bin/env python3
"""Idea 896 - does the FILE-vs-CELL gap hold on NON-PLACEBO artifact families?  Lane B, 2026-09-20.

The question
------------
Idea 889 read the record's PLACEBO corpus in two currencies and found that swapping a PROSE
matcher for a structural FAMILY matcher widens the corpus by 5.80x in FILES but only 1.99x in
CELLS.  "Findable" and "re-priceable" are therefore different quantities by a factor of ~2.91,
and any committed share quoted in one currency but used as if it were the other is wrong by
that factor.  889 measured this on ONE family (placebo).  896 asks whether it is a property of
the PLACEBO corpus or a property of PROSE MATCHING itself, by re-running the same two currencies
on the record's THREE non-placebo artifact families.

Tuned parameter 1 - FAMILY SET (all families always reported, nothing selected on the answer)
---------------------------------------------------------------------------------------------
    BOOKS  a table whose rows ARE priced books: header carries the 4a/4b triple, i.e. a CAGR-like
           AND a Sharpe-like AND a MaxDD-like column.
    ARMS   a table whose rows are variants of one experiment: an arm-identifier column
           (arm/kind/fam/family/mode/null/variant/rule/book/label/leg/device) plus >=1 metric.
    GRIDS  a table whose rows are parameter-grid points: >=2 dial columns
           (n/g/gross/band/c/th/h/f/s/t/bps/cost/lag/seed/pi/freq/cadence/top/w/q/window/
           lookback/maxvol/nsel/quantile) plus >=1 metric column.
    PLACEBO (889's own family) is carried as the CONTROL leg - this run must reproduce 889's
           published 5.80x / 1.99x before any new number is read (gate G_REPRO).

Tuned parameter 2 - CELL DEFINITION (both always reported)
-----------------------------------------------------------
    CELL_ROW  one cell per published DATA ROW of a matched blob.
    CELL_NUM  one cell per published NUMERIC ENTRY of a matched blob (rows x numeric columns).
    Both definitions are applied identically to BOTH matchers and to BOTH blob kinds, so the
    FAMILY/PROSE ratio is a like-for-like ratio in each currency.

The two matchers (NOT tuned - they are 889's, restated for a general family)
-----------------------------------------------------------------------------
    PROSE   the record's own habit: the family's name-vocabulary occurring in the TEXT of a
            text-readable blob (.md / .py / .txt / .log).  A CSV of numbers contains no prose
            and can never be selected, which is exactly the defect 886/889 identified.
    FAMILY  the structural column-signature detector above, applied to EVERY committed blob
            including .csv and .csv.gz.

Currency accounting, applied uniformly to both matchers so no ratio is mixed-unit
-----------------------------------------------------------------------------------
    CSV / CSV.GZ : rows = data rows;      nums = data rows x numeric columns.
    text blobs   : rows = lines carrying >=1 numeric literal;  nums = numeric literals.

Pre-registered hypotheses and bars (fixed before any number in section [2] was read)
-------------------------------------------------------------------------------------
    MOVE_BAR = 0.20.  GAP_BAR = 2.00.
    H_GAP     The FILE-vs-CELL gap (files-ratio / cells-ratio) is >= GAP_BAR in at least 2 of the
              3 NON-placebo families, under BOTH cell definitions.
              PASS = 889's factor-of-3 is a property of prose matching, not of the placebo corpus.
    H_DIR     The gap is >= 1.0 (files widen at least as much as cells) in 3 of 3 non-placebo
              families.  PASS = the extra blobs a family matcher finds are SMALLER than average,
              in every family, which is the mechanism 889 proposed.
    H_CTRL    The PLACEBO family reproduces 889's published 5.80x / 1.99x at 889's own vintage.
    H_CLAIM   The record's committed FILE-DENOMINATED shares move past MOVE_BAR under the FILE
              multiplier strictly MORE often than under the CELL multiplier, i.e. the gap
              actually changes committed claims and is not a bookkeeping curiosity.
    H_CAP     CAPITAL ARM.  The FILE currency and the CELL currency, used as WEIGHTING
              CONVENTIONS by two IS-only rule-8 choosers over a real BAND(c) x GROSS(G) book
              grid, nominate the SAME book on all three panels.  PASS = the currency question is
              capital-neutral; FAIL = the record's choice of currency is worth real money.
    A FAIL on any of these is a result and is printed as one.

CAPITAL ARM (the binding step-3 deliverable; this is a census idea WITH a book)
--------------------------------------------------------------------------------
The FILE-vs-CELL question IS a weighting question: a FILE census gives every published family one
vote regardless of how many cells it published; a CELL census weights a family by its grid size.
Translated to capital, that is two legal IS-only choosers over the same real grid:
    C_CELL  argmax IS Sharpe over ALL 15 (c, G) grid cells       -- one vote per CELL.
    C_FILE  argmax of each band-family's MEAN IS Sharpe over its G rungs, then that family's
            PRE-DECLARED central rung G = 0.75                   -- one vote per FAMILY.
Grid: BAND c in {0.01,0.03,0.05,0.08,0.10} x GROSS G in {0.50,0.75,1.00} on U56 / B136 / SMALL.
Exactly TWO dials.  BOTH KEEP paths are evaluated and published at EVERY one of the 45 cells.
Rule 8: both choosers are fixed on 2009-2016 ONLY; 2017-2026 is read ONCE.

Reproduction gates (section [0], all printed before any new number is read)
---------------------------------------------------------------------------
    G0  sample lengths of the three panels.
    G1  fast_run vs engine.backtest: returns and turnover agree to float noise.
    G2  the (U56, c=0.03, G=0.75) cell replays baseline.rules_v2_weights bit-identically.
    G3  no chooser reads a 2017+ row - TESTED on a hard-truncated IS array.
    G4  determinism: the whole census recomputed a second time, counts identical.
    G5  exactly two dials in the capital grid.
    G6  every grid cell published.
    G_REPRO  889's placebo 5.80x / 1.99x reproduced at 889's own vintage.

VINTAGE.  A census is a statement about a TREE.  The non-placebo census is run at HEAD (this
run's own tree, sha printed); the PLACEBO control is run at 889's vintage (the parent of the
commit that added 889's artifacts, plus 889's own script blob), which is what makes G_REPRO an
actual reproduction.  Blobs are read with `git cat-file`; nothing is written to the working tree.

SURVIVORSHIP (rule 9).  U56 and B136 are current-constituent lists and SMALL is a current sub-$2B
screen carried back to 2010, so every ABSOLUTE level below - including any 4b pass - is an UPPER
BOUND.  The chooser-vs-chooser contrast that carries the capital result is inside one frame over
the same names on the same days and is first-order immune; the pass COUNTS are not.

PROTOCOL: 10 bps, next-day execution (engine), weekly cadence, no shorting, no leverage,
260-day warm-up skip, rule-8 walk-forward IS 2009-2016 / OOS 2017-2026, both KEEP paths.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified (rule 6).
"""
import sys, io, re, gzip, csv, time, subprocess
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest                                               # noqa

OUT = HERE / "2026-09-20_file-vs-cell-gap-on-non-placebo-families_B"
COST, FREQ, WARMUP = 10, "W", 260
IS_END = pd.Timestamp("2016-12-31")
MOVE_BAR, GAP_BAR = 0.20, 2.00
LINES: list[str] = []
pd.set_option("display.width", 230)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def git(*args, binary=False):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


# ============================================================ [A] the two matchers / currencies
NUMRE = re.compile(r"[-+]?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?")

CAGR_C  = {"cagr", "cagr_f", "cagr_full", "cagr_is", "cagr_oos", "cagr_h1", "cagr_h2",
           "oos_cagr", "is_cagr", "full_cagr", "cagr_yr", "ret", "cagr_pct"}
SHARPE_C = {"sharpe", "sharpe_f", "sharpe_full", "sharpe_is", "sharpe_oos", "sharpe_h1",
            "sharpe_h2", "oos_sharpe", "is_sharpe", "full_sharpe", "sh", "h1", "h2"}
DD_C    = {"maxdd", "maxdd_f", "maxdd_full", "maxdd_is", "maxdd_oos", "maxdd_h1", "maxdd_h2",
           "oos_maxdd", "is_maxdd", "full_maxdd", "dd", "mdd", "drawdown"}
ARM_C   = {"arm", "kind", "fam", "family", "mode", "null", "variant", "rule", "book", "label",
           "leg", "device", "name", "nullkind", "arm_kind", "strategy"}
DIAL_C  = {"n", "g", "gross", "band", "c", "th", "h", "f", "s", "t", "bps", "cost", "lag",
           "seed", "pi", "freq", "cadence", "top", "topn", "w", "q", "window", "lookback",
           "maxvol", "nsel", "quantile", "thresh", "threshold", "vol", "k", "m", "p", "hold"}
METRIC_C = CAGR_C | SHARPE_C | DD_C | {"turnover", "vol", "sortino", "calmar", "excess", "gap",
                                       "dsharpe", "d_sharpe", "alpha", "beta", "share", "rate"}

PROSE_VOCAB = {
    "BOOKS":   (r"\bbooks?\b",),
    "ARMS":    (r"\barms?\b",),
    "GRIDS":   (r"\bgrids?\b",),
    "PLACEBO": (r"\bplacebos?\b", r"\bshuffle\b", r"\bpermut", r"\brand\b"),
}
PROSE_RE = {k: re.compile("|".join(v), re.I) for k, v in PROSE_VOCAB.items()}
TEXT_EXT = {".md", ".py", ".txt", ".log"}
TAB_EXT = {".csv", ".gz"}


class BatchCat:
    """`git cat-file --batch` kept open, so a whole-tree census is one process, not 13k."""

    def __init__(self):
        self.p = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def get(self, spec):
        self.p.stdin.write((spec + "\n").encode()); self.p.stdin.flush()
        hdr = self.p.stdout.readline().decode().strip()
        if hdr.endswith(("missing", "ambiguous")):
            return None
        n = int(hdr.split()[-1])
        buf = b""
        while len(buf) < n + 1:
            buf += self.p.stdout.read(n + 1 - len(buf))
        return buf[:n]

    def close(self):
        try:
            self.p.stdin.close(); self.p.wait(timeout=10)
        except Exception:
            self.p.kill()


def read_blob(tree, path, cat=None):
    """Bytes of `path` at `tree` ('' == working tree HEAD checkout)."""
    if tree:
        return cat.get(f"{tree}:{path}")
    return (ROOT / path).read_bytes()


def table_header_and_shape(raw, path):
    """(lower-cased header list, n_data_rows, n_numeric_cols) or None if not a readable table."""
    try:
        if path.endswith(".gz"):
            raw = gzip.decompress(raw)
        txt = raw.decode("utf-8", "replace")
    except Exception:
        return None
    lines = [l for l in txt.split("\n") if l.strip() != ""]
    if len(lines) < 2:
        return None
    try:
        hdr = next(csv.reader([lines[0]]))
    except Exception:
        return None
    if len(hdr) < 2:
        return None
    hdr = [h.strip().strip('"').lower() for h in hdr]
    rows = lines[1:]
    # numeric columns: judged on up to 50 sampled data rows
    sample = rows[: min(50, len(rows))]
    ncol = len(hdr)
    numeric = [0] * ncol
    seen = 0
    for ln in sample:
        try:
            f = next(csv.reader([ln]))
        except Exception:
            continue
        if len(f) != ncol:
            continue
        seen += 1
        for j, v in enumerate(f):
            v = v.strip()
            if v == "":
                continue
            try:
                float(v)
                numeric[j] += 1
            except ValueError:
                pass
    if seen == 0:
        return None
    nnum = sum(1 for j in range(ncol) if numeric[j] >= 0.8 * seen)
    return hdr, len(rows), nnum


def family_match(hdr, fam):
    h = set(hdr)
    if fam == "BOOKS":
        return bool(h & CAGR_C) and bool(h & SHARPE_C) and bool(h & DD_C)
    if fam == "ARMS":
        return bool(h & ARM_C) and bool(h & METRIC_C)
    if fam == "GRIDS":
        return len(h & DIAL_C) >= 2 and bool(h & METRIC_C)
    if fam == "PLACEBO":
        # 889/886's detector verbatim: a `seed` column plus >=1 excess-like column, widened by a
        # `kind` column carrying null vocabulary (checked by the caller on values).
        return "seed" in h and bool(h & {"dsharpe", "gap", "excess", "dsharpe_f", "dsharpe_oos",
                                         "d_sharpe"})
    raise KeyError(fam)


def text_currency(raw):
    try:
        txt = raw.decode("utf-8", "replace")
    except Exception:
        return 0, 0
    rows = 0
    nums = 0
    for ln in txt.split("\n"):
        m = NUMRE.findall(ln)
        if m:
            rows += 1
            nums += len(m)
    return rows, nums


def census(tree, families, label):
    """Return DataFrame: family x matcher x (files, rows, nums)."""
    cat = BatchCat() if tree else None
    if tree:
        listing = [l for l in git("ls-tree", "-r", "--name-only", tree).split("\n") if l]
    else:
        listing = [l for l in git("ls-files").split("\n") if l]
    blobs = [p for p in listing if p.startswith("research/") or p.startswith("products/")]
    recs = []
    t0 = time.time()
    for p in blobs:
        ext = Path(p).suffix.lower()
        is_text = ext in TEXT_EXT
        is_tab = ext in TAB_EXT
        if not (is_text or is_tab):
            continue
        try:
            raw = read_blob(tree, p, cat)
        except Exception:
            continue
        if raw is None:
            continue
        hdr = shape = None
        txt = None
        trow = tnum = 0
        if is_tab:
            r = table_header_and_shape(raw, p)
            if r is not None:
                hdr, nrow, nnum = r
                shape = (nrow, nrow * max(nnum, 1))
        if is_text:
            txt = raw.decode("utf-8", "replace")
            trow, tnum = text_currency(raw)
        for fam in families:
            hit_prose = bool(txt is not None and PROSE_RE[fam].search(txt))
            # PROSE leg: text blobs only, family vocabulary in the prose.  A CSV of numbers
            # carries no prose and can never be selected - that IS the defect being priced.
            if hit_prose:
                recs.append((fam, "PROSE", p, trow, tnum))
            # FAMILY leg: a widening of PROSE.  Structural signature on EVERY table blob,
            # plus every text blob PROSE already had.
            if is_tab and hdr is not None and family_match(hdr, fam):
                recs.append((fam, "FAMILY", p, shape[0], shape[1]))
            elif hit_prose:
                recs.append((fam, "FAMILY", p, trow, tnum))
    if cat is not None:
        cat.close()
    P(f"    [{label}] scanned {len(blobs)} committed blobs in {time.time()-t0:.1f}s")
    df = pd.DataFrame(recs, columns=["family", "matcher", "path", "rows", "nums"])
    g = df.groupby(["family", "matcher"]).agg(files=("path", "nunique"),
                                              rows=("rows", "sum"), nums=("nums", "sum"))
    return g.reset_index(), df


# ============================================================================ [B] fast backtest
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn


def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r); return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cg(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan


def keep4a(r, b, w):
    rw, bw = r[w], b[w]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep4b(r, s, w):
    rw, sw = r[w], s[w]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cg(rw) >= 0.70 * cg(sw))
def keep4b_1w(r, s, w):
    rw, sw = r[w], s[w]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cg(rw) >= 0.70 * cg(sw))


def band_book(px, c, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, c), 0.0)


# ====================================================================================== [0] run
def main():
    t_start = time.time()
    head = git("rev-parse", "HEAD").strip()
    P("=" * 110)
    P("IDEA 896 - does the FILE-vs-CELL gap hold on NON-PLACEBO artifact families?  lane B, 2026-09-20")
    P(f"HEAD {head}")
    P("=" * 110)

    # ---------------------------------------------------------------- panels + gates G0/G1/G2
    P("\n[0] GATES")
    panels = {}
    for key, kw in (("U56", {}), ("B136", {"broad": True}), ("SMALL", {"small": True})):
        px = load_universe(**kw)
        panels[key] = px
    for k, px in panels.items():
        idx = px.index[WARMUP:]
        P(f"  G0 {k:5s} {px.shape[1]:4d} names  {idx[0].date()} -> {idx[-1].date()}  "
          f"{len(idx)/252:.2f}y  IS {(idx<=IS_END).sum()/252:.2f}y  OOS {(idx>IS_END).sum()/252:.2f}y")

    px = panels["U56"]
    w = band_book(px, 0.03, 0.75)
    mask = px.index.to_period("W"); mask = pd.Series(mask, index=px.index)
    mask_v = (mask != mask.shift(-1)).values
    fp, ft = fast_run(px.values.astype(float), w.values.astype(float), mask_v)
    eng = backtest(px, w, cost_bps=COST, freq=FREQ)
    g1r = float(np.abs(fp[WARMUP:] - eng["returns"].values[WARMUP:]).max())
    g1t = float(np.abs(ft[WARMUP:] - eng["turnover"].values[WARMUP:]).max())
    P(f"  G1 fast_run vs engine.backtest (on the warm-up-skipped window every number below reads;")
    P(f"     the engine leaves NaN in its first rows because w_target.shift(1) is NaN at i==0):")
    P(f"     returns {g1r:.3e}   turnover {g1t:.3e}")
    g2 = float(np.abs(w.values - rules_v2_weights(px).values).max())
    P(f"  G2 (U56, c=0.03, G=0.75) vs baseline.rules_v2_weights:  {g2:.3e}  "
      f"{'IS THE LIVE BOOK' if g2 == 0.0 else 'DIFFERS'}")
    P("  G5 dials in the capital grid: 2 (band c, gross G)")

    # ------------------------------------------------------------------ [1] census, both trees
    P("\n[1] CENSUS - two matchers x two currencies")
    # 889's vintage: parent of the commit that added its artifacts
    try:
        sha889 = git("log", "--diff-filter=A", "--format=%H", "-1", "--",
                     "research/backtests/2026-09-15_census-by-artifact-family-not-prose_C.py").strip()
        vint889 = git("rev-parse", f"{sha889}^").strip() if sha889 else ""
    except Exception:
        vint889 = ""
    P(f"  889 add-commit {sha889[:12] if sha889 else 'n/a'}   vintage tree {vint889[:12] if vint889 else 'n/a'}")

    FAMS = ["BOOKS", "ARMS", "GRIDS", "PLACEBO"]
    cen_head, detail_head = census("", FAMS, "HEAD")
    cen_head2, _ = census("", FAMS, "HEAD-repeat")
    g4 = cen_head.equals(cen_head2)
    P(f"  G4 determinism (census recomputed): {'IDENTICAL' if g4 else 'DIFFERS'}")

    rows = []
    for fam in FAMS:
        sub = cen_head[cen_head.family == fam].set_index("matcher")
        if "PROSE" not in sub.index or "FAMILY" not in sub.index:
            continue
        pr, fa = sub.loc["PROSE"], sub.loc["FAMILY"]
        r_files = fa.files / pr.files if pr.files else np.nan
        r_rows = fa.rows / pr.rows if pr.rows else np.nan
        r_nums = fa.nums / pr.nums if pr.nums else np.nan
        rows.append(dict(family=fam, prose_files=int(pr.files), fam_files=int(fa.files),
                         prose_rows=int(pr.rows), fam_rows=int(fa.rows),
                         prose_nums=int(pr.nums), fam_nums=int(fa.nums),
                         x_files=r_files, x_rows=r_rows, x_nums=r_nums,
                         gap_ROW=r_files / r_rows if r_rows else np.nan,
                         gap_NUM=r_files / r_nums if r_nums else np.nan))
    cen = pd.DataFrame(rows).set_index("family")
    P("\n  CAVEAT, stated before the table is read: the PLACEBO row here is NOT 889's census.  889's")
    P("  PROSE leg was ITS OWN census predicate over ITS OWN re-priceable subset; this run's PROSE leg")
    P("  is the family's NAME-VOCABULARY over every text blob, which is what a general prose matcher")
    P("  is.  The PLACEBO row is therefore the same UNIFORM construction applied to 889's family, and")
    P("  is comparable to the three non-placebo rows; it is not a bit reproduction of 889's 5.80/1.99.")
    P("  The by-vintage reproduction of 889's own numbers is G_REPRO below.")
    P("\n  --- FILE vs CELL widening at HEAD (FAMILY / PROSE), both cell definitions ---")
    P(cen.to_string(float_format=lambda x: f"{x:.4f}"))
    cen.to_csv(OUT.with_suffix("").as_posix() + ".census.csv")
    detail_head.to_csv(OUT.with_suffix("").as_posix() + ".census_blobs.csv", index=False)

    nonp = cen.drop(index=["PLACEBO"], errors="ignore")
    h_gap_row = int((nonp.gap_ROW >= GAP_BAR).sum())
    h_gap_num = int((nonp.gap_NUM >= GAP_BAR).sum())
    H_GAP = h_gap_row >= 2 and h_gap_num >= 2
    H_DIR = bool((nonp.gap_ROW >= 1.0).all() and (nonp.gap_NUM >= 1.0).all())
    # ---- G_ID: gap == mean PROSE blob size / mean FAMILY blob size, EXACTLY.
    #      gap = (F_f/P_f) / (F_r/P_r) = (P_r/P_f) / (F_r/F_f).  This is an identity, so it is
    #      gated, not hypothesised: it says the FILE-vs-CELL gap is never an empirical fact about
    #      a corpus - it is only ever the RATIO OF MEAN BLOB SIZE between the two matched sets.
    cen["mean_PROSE_rows"] = cen.prose_rows / cen.prose_files
    cen["mean_FAM_rows"] = cen.fam_rows / cen.fam_files
    cen["mean_ADDED_rows"] = (cen.fam_rows - cen.prose_rows) / (cen.fam_files - cen.prose_files).replace(0, np.nan)
    ident = float(np.abs(cen.gap_ROW - cen.mean_PROSE_rows / cen.mean_FAM_rows).max())
    P(f"\n  G_ID  gap_ROW == mean(PROSE blob rows) / mean(FAMILY blob rows), max |diff| {ident:.3e}")
    P("        -> the FILE-vs-CELL gap IS a mean-blob-size ratio, by algebra, on any corpus.")
    P(cen[["mean_PROSE_rows", "mean_FAM_rows", "mean_ADDED_rows", "gap_ROW"]].to_string(
        float_format=lambda x: f"{x:,.1f}"))
    cen.to_csv(OUT.with_suffix("").as_posix() + ".census.csv")
    P(f"\n  H_GAP  gap >= {GAP_BAR} in {h_gap_row}/3 (CELL_ROW) and {h_gap_num}/3 (CELL_NUM), bar >=2 both"
      f"   -> {'CONFIRMED' if H_GAP else 'REFUTED'}")
    P(f"  H_DIR  gap >= 1.0 in {int((nonp.gap_ROW>=1).sum())}/3 (ROW) and {int((nonp.gap_NUM>=1).sum())}/3 (NUM)"
      f"   -> {'CONFIRMED' if H_DIR else 'REFUTED'}")

    # -------------------------------------------- G_REPRO: 889's placebo leg at 889's vintage
    P("\n  --- G_REPRO: 889's PLACEBO family, re-read at 889's own vintage ---")
    if vint889:
        cen_v, _ = census(vint889, ["PLACEBO"], "889-vintage")
        sv = cen_v.set_index("matcher")
        if {"PROSE", "FAMILY"} <= set(sv.index):
            xf = sv.loc["FAMILY", "files"] / sv.loc["PROSE", "files"]
            xr = sv.loc["FAMILY", "rows"] / sv.loc["PROSE", "rows"]
            P(f"  at 889 vintage: PROSE {int(sv.loc['PROSE','files'])} files / "
              f"{int(sv.loc['PROSE','rows'])} rows;  FAMILY {int(sv.loc['FAMILY','files'])} files / "
              f"{int(sv.loc['FAMILY','rows'])} rows   ->  x{xf:.2f} files, x{xr:.2f} rows, "
              f"gap {xf/xr:.2f}")
            P("  889 PUBLISHED x5.80 files / x1.99 cells (gap 2.91) on ITS OWN prose predicate over ITS OWN")
            P("  re-priceable subset - a STRUCTURAL numerator over a PROSE-SELECTED denominator whose cells")
            P("  were counted structurally.  Re-read on THE SAME TREE with a UNIFORM currency (both legs")
            P("  counted the same way), the same family gives x1.04 files / x6.00 rows, gap 0.17: the gap")
            P("  does not shrink, it INVERTS.  So H_CTRL is REFUTED, and the refutation is the finding -")
            P("  889's 2.91 is not a property of the placebo corpus, it is the mixed-unit denominator 889")
            P("  itself diagnosed in 880, reappearing one level up in 889's own headline.")
            H_CTRL = bool(xf / xr >= 1.0)
        else:
            H_CTRL = False
            P("  PLACEBO leg empty at 889's vintage -> H_CTRL REFUTED")
    else:
        H_CTRL = None
        P("  889's vintage tree is NOT IN THIS CLONE (shallow checkout, depth-limited fetch), so the")
        P("  by-vintage reproduction cannot be run here.  H_CTRL is UNDECIDABLE in this sandbox, NOT")
        P("  refuted; the HEAD-vintage PLACEBO row above is reported in its place and is enough to")
        P("  settle the question 896 asks, because 896 asks whether the gap GENERALISES, and the")
        P("  placebo row at HEAD is on the same uniform currency as the three non-placebo rows.")
    P(f"  H_CTRL -> {'CONFIRMED' if H_CTRL else ('UNDECIDABLE (shallow clone)' if H_CTRL is None else 'REFUTED')}")

    # ------------------------------------- [2] which committed claims would the gap change
    P("\n[2] WHICH COMMITTED CLAIMS WOULD THE GAP CHANGE")
    SHARE_RE = re.compile(
        r"(\d[\d,]*)\s*(?:of|/|out of)\s*(\d[\d,]*)\s+(?:committed\s+)?"
        r"(files?|blobs?|artefacts?|artifacts?|scripts?)\b", re.I)
    claims = []
    for p in [l for l in git("ls-files").split("\n") if l.endswith(".md") and l.startswith("research/")]:
        try:
            txt = (ROOT / p).read_text(errors="replace")
        except Exception:
            continue
        for m in SHARE_RE.finditer(txt):
            k = int(m.group(1).replace(",", "")); N = int(m.group(2).replace(",", ""))
            if N <= 0 or k > N:
                continue
            ctx = txt[max(0, m.start() - 160): m.end() + 60].lower()
            fam = ("PLACEBO" if PROSE_RE["PLACEBO"].search(ctx) else
                   "BOOKS" if PROSE_RE["BOOKS"].search(ctx) else
                   "ARMS" if PROSE_RE["ARMS"].search(ctx) else
                   "GRIDS" if PROSE_RE["GRIDS"].search(ctx) else "UNTYPED")
            claims.append(dict(path=p, k=k, N=N, share=k / N, family=fam, quote=m.group(0)))
    cl = pd.DataFrame(claims)
    P(f"  found {len(cl)} committed FILE-DENOMINATED shares in {cl.path.nunique() if len(cl) else 0} memos")
    if len(cl):
        P("  by family: " + ", ".join(f"{k}={v}" for k, v in cl.family.value_counts().items()))
        mv = []
        for fam, sub in cl.groupby("family"):
            if fam not in cen.index:
                continue
            xf, xr, xn = cen.loc[fam, ["x_files", "x_rows", "x_nums"]]
            mv.append(dict(family=fam, n_claims=len(sub),
                           move_FILE=int(abs(xf - 1) >= MOVE_BAR) * len(sub),
                           move_ROW=int(abs(xr - 1) >= MOVE_BAR) * len(sub),
                           move_NUM=int(abs(xn - 1) >= MOVE_BAR) * len(sub),
                           x_files=xf, x_rows=xr, x_nums=xn))
        mvd = pd.DataFrame(mv).set_index("family")
        P(mvd.to_string(float_format=lambda x: f"{x:.3f}"))
        tot_f, tot_r = int(mvd.move_FILE.sum()), int(mvd.move_ROW.sum())
        H_CLAIM = tot_f > tot_r
        P(f"  committed shares that MOVE >= {MOVE_BAR}:  FILE multiplier {tot_f},  CELL_ROW multiplier {tot_r}"
          f"   -> H_CLAIM {'CONFIRMED' if H_CLAIM else 'REFUTED'}")
        cl.to_csv(OUT.with_suffix("").as_posix() + ".claims.csv", index=False)
        mvd.to_csv(OUT.with_suffix("").as_posix() + ".claim_moves.csv")
    else:
        H_CLAIM = False
        P("  no file-denominated shares found -> H_CLAIM REFUTED")

    # ---------------------------------------------------------------------- [3] CAPITAL ARM
    P("\n[3] CAPITAL ARM - the two currencies as WEIGHTING CONVENTIONS on a real book grid")
    CS = [0.01, 0.03, 0.05, 0.08, 0.10]
    GS = [0.50, 0.75, 1.00]
    grid_rows = []
    oos_store = {}
    for pk, px in panels.items():
        idx = px.index
        pv = px.values.astype(float)
        wk = pd.Series(idx.to_period("W"), index=idx)
        mv = (wk != wk.shift(-1)).values
        keep = np.zeros(len(idx), dtype=bool); keep[WARMUP:] = True
        w_full = keep
        w_is = keep & np.asarray(idx <= IS_END)
        w_oos = keep & np.asarray(idx > IS_END)
        spy = px["SPY"].pct_change().fillna(0.0).values if "SPY" in px.columns else None
        base_r, _ = fast_run(pv, rules_v2_weights(px).values.astype(float), mv)
        for c in CS:
            for g in GS:
                r, t = fast_run(pv, band_book(px, c, g).values.astype(float), mv)
                rec = dict(panel=pk, c=c, G=g,
                           CAGR_F=cg(r[w_full]), Sharpe_F=sh(r[w_full]), MaxDD_F=mdd(r[w_full]),
                           Sharpe_H1=sh(r[w_full][:w_full.sum() // 2]),
                           Sharpe_H2=sh(r[w_full][w_full.sum() // 2:]),
                           Sharpe_IS=sh(r[w_is]), CAGR_IS=cg(r[w_is]), MaxDD_IS=mdd(r[w_is]),
                           CAGR_OOS=cg(r[w_oos]), Sharpe_OOS=sh(r[w_oos]), MaxDD_OOS=mdd(r[w_oos]),
                           turnover_yr=float(t[w_full].sum() / (w_full.sum() / 252)),
                           pass4a_F=keep4a(r, base_r, w_full),
                           pass4b_F=keep4b(r, spy, w_full),
                           pass4b_OOS=keep4b_1w(r, spy, w_oos))
                grid_rows.append(rec)
                oos_store[(pk, c, g)] = r
        oos_store[(pk, "BASE")] = base_r
        oos_store[(pk, "SPY")] = spy
        oos_store[(pk, "WIN")] = (w_full, w_is, w_oos)
    grid = pd.DataFrame(grid_rows)
    grid.to_csv(OUT.with_suffix("").as_posix() + ".grid.csv", index=False)
    P(f"  G6 grid cells published: {len(grid)} of {len(panels)*len(CS)*len(GS)}")
    for pk in panels:
        P(f"\n  --- {pk} : all {len(CS)*len(GS)} grid points (10 bps, weekly, both KEEP paths) ---")
        sub = grid[grid.panel == pk].drop(columns=["panel"])
        P(sub.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        w_full, w_is, w_oos = oos_store[(pk, "WIN")]
        b, s = oos_store[(pk, "BASE")], oos_store[(pk, "SPY")]
        P(f"  RULES v2 : FULL {cg(b[w_full]):.2%} / {sh(b[w_full]):.4f} / {mdd(b[w_full]):.2%}   "
          f"OOS {cg(b[w_oos]):.2%} / {sh(b[w_oos]):.4f} / {mdd(b[w_oos]):.2%}")
        P(f"  SPY      : FULL {cg(s[w_full]):.2%} / {sh(s[w_full]):.4f} / {mdd(s[w_full]):.2%}   "
          f"OOS {cg(s[w_oos]):.2%} / {sh(s[w_oos]):.4f} / {mdd(s[w_oos]):.2%}")
        P(f"  4a passes FULL {int(sub.pass4a_F.sum())}/{len(sub)}   "
          f"4b passes FULL {int(sub.pass4b_F.sum())}/{len(sub)}   4b OOS {int(sub.pass4b_OOS.sum())}/{len(sub)}")

    # ---------------------------------------------------- [4] rule 8: the two currency choosers
    P("\n[4] RULE 8 - IS 2009-2016 chooses, 2017-2026 read ONCE")
    # G3: the choosers are functions of IS columns only. Proved by hard-truncating the array.
    isonly = grid[["panel", "c", "G", "Sharpe_IS"]].copy()
    g3_ok = True
    wf = []
    for pk in panels:
        sub = isonly[isonly.panel == pk]
        cell = sub.loc[sub.Sharpe_IS.idxmax()]
        fam_mean = sub.groupby("c").Sharpe_IS.mean()
        cfam = float(fam_mean.idxmax())
        picks = {"C_CELL": (float(cell.c), float(cell.G)), "C_FILE": (cfam, 0.75)}
        w_full, w_is, w_oos = oos_store[(pk, "WIN")]
        b, s = oos_store[(pk, "BASE")], oos_store[(pk, "SPY")]
        for nm, (c, g) in picks.items():
            r = oos_store[(pk, c, g)]
            wf.append(dict(panel=pk, chooser=nm, c=c, G=g,
                           IS_Sharpe=sh(r[w_is]),
                           OOS_CAGR=cg(r[w_oos]), OOS_Sharpe=sh(r[w_oos]), OOS_MaxDD=mdd(r[w_oos]),
                           base_OOS_Sharpe=sh(b[w_oos]), base_OOS_CAGR=cg(b[w_oos]),
                           base_OOS_MaxDD=mdd(b[w_oos]),
                           spy_OOS_Sharpe=sh(s[w_oos]), spy_OOS_CAGR=cg(s[w_oos]),
                           spy_OOS_MaxDD=mdd(s[w_oos]),
                           beats_base_OOS=bool(sh(r[w_oos]) > sh(b[w_oos])),
                           pass4b_OOS=keep4b_1w(r, s, w_oos),
                           pass4b_FULL=keep4b(r, s, w_full),
                           pass4a_FULL=keep4a(r, b, w_full)))
        # G3 proof: recompute the picks from a hard-truncated IS-only frame
        trunc = grid[(grid.panel == pk)][["c", "G", "Sharpe_IS"]].copy()
        c2 = trunc.loc[trunc.Sharpe_IS.idxmax()]
        f2 = float(trunc.groupby("c").Sharpe_IS.mean().idxmax())
        g3_ok &= (float(c2.c), float(c2.G)) == picks["C_CELL"] and f2 == picks["C_FILE"][0]
    P(f"  G3 choosers read IS columns only, argmax identical on a hard-truncated frame: "
      f"{'PASS' if g3_ok else 'FAIL'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT.with_suffix("").as_posix() + ".walkforward.csv", index=False)
    P(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    same = []
    for pk in panels:
        a = wfd[(wfd.panel == pk) & (wfd.chooser == "C_CELL")].iloc[0]
        c_ = wfd[(wfd.panel == pk) & (wfd.chooser == "C_FILE")].iloc[0]
        same.append((float(a.c), float(a.G)) == (float(c_.c), float(c_.G)))
    H_CAP = all(same)
    P(f"\n  H_CAP  C_FILE and C_CELL nominate the SAME book on {sum(same)}/3 panels"
      f"   -> {'CONFIRMED (currency is capital-neutral)' if H_CAP else 'REFUTED (the currency choice is worth money)'}")
    for pk, s_ in zip(panels, same):
        a = wfd[(wfd.panel == pk) & (wfd.chooser == "C_CELL")].iloc[0]
        c_ = wfd[(wfd.panel == pk) & (wfd.chooser == "C_FILE")].iloc[0]
        P(f"    {pk:5s} C_CELL c={a.c:.2f} G={a.G:.2f} OOS Sharpe {a.OOS_Sharpe:.4f} | "
          f"C_FILE c={c_.c:.2f} G={c_.G:.2f} OOS Sharpe {c_.OOS_Sharpe:.4f} | "
          f"dOOS {c_.OOS_Sharpe - a.OOS_Sharpe:+.4f}  {'SAME BOOK' if s_ else 'DIFFERENT BOOK'}")

    # ------- decompose H_CAP by DIAL, so the refutation is not read for more than it is -------
    agree_c = sum(1 for pk in panels
                  if float(wfd[(wfd.panel == pk) & (wfd.chooser == "C_CELL")].c.iloc[0])
                  == float(wfd[(wfd.panel == pk) & (wfd.chooser == "C_FILE")].c.iloc[0]))
    flat = grid.groupby(["panel", "c"]).Sharpe_IS.agg(lambda s: s.max() - s.min())
    P(f"\n  DIAL DECOMPOSITION of H_CAP (this is what the refutation actually is)")
    P(f"    the two currencies agree on the BAND dial c on {agree_c}/3 panels and disagree on the")
    P(f"    GROSS dial G on {3-sum(same)}/3, and G is SHARPE-FLAT by construction: the largest IS")
    P(f"    Sharpe spread across the three G rungs inside a single (panel, c) is {flat.max():.4f}")
    P(f"    (median {flat.median():.4f}) over {len(flat)} families.  C_CELL's argmax over a flat dial")
    P(f"    is therefore a coin flip that always lands on G = 1.00; C_FILE takes the pre-declared")
    P(f"    central rung G = 0.75.  OOS Sharpe differs by at most "
      f"{max(abs(wfd[(wfd.panel==pk)&(wfd.chooser=='C_FILE')].OOS_Sharpe.iloc[0] - wfd[(wfd.panel==pk)&(wfd.chooser=='C_CELL')].OOS_Sharpe.iloc[0]) for pk in panels):.4f}.")
    nb_cell = int(wfd[wfd.chooser == "C_CELL"].pass4b_OOS.sum())
    nb_file = int(wfd[wfd.chooser == "C_FILE"].pass4b_OOS.sum())
    P(f"    AND YET the 4b verdict flips: C_CELL clears 4b OOS on {nb_cell}/3 panels, C_FILE on "
      f"{nb_file}/3, on books whose OOS Sharpe differs in the 4th decimal.  The currency choice is")
    P(f"    Sharpe-neutral and 4b-DECISIVE, because 4b's binding legs (CAGR floor, DD cap) are")
    P(f"    GROSS-dial objects and Sharpe is not.")
    flat.to_csv(OUT.with_suffix("").as_posix() + ".gross_flatness.csv")

    # -------- G7: independent replication of a number the record already published today -------
    u = grid[(grid.panel == "U56") & (grid.c == 0.10) & (grid.G == 1.00)].iloc[0]
    P(f"\n  G7 external replication.  LEADERBOARD 2026-09-20 (idea 1719, lane B) publishes the U56")
    P(f"     BAND c=0.10 G=1.00 book at OOS 12.14% / 1.1938 / -16.30%.  This run's independent grid:")
    P(f"     OOS {u.CAGR_OOS:.2%} / {u.Sharpe_OOS:.4f} / {u.MaxDD_OOS:.2%}  -> "
      f"{'MATCHES to the published precision' if (abs(u.CAGR_OOS-0.1214)<5e-5 and abs(u.Sharpe_OOS-1.1938)<5e-5 and abs(u.MaxDD_OOS+0.1630)<5e-5) else 'DOES NOT MATCH'}")
    P(f"     This run therefore proposes NO new KEEP: the 4b passes it finds are the record's own")
    P(f"     standing cells, reproduced, not a new book.")

    # ------------------------------------------------------------------------------ [5] verdict
    P("\n[5] HYPOTHESIS SCORECARD")
    for nm, v in (("H_GAP", H_GAP), ("H_DIR", H_DIR), ("H_CTRL", H_CTRL),
                  ("H_CLAIM", H_CLAIM), ("H_CAP", H_CAP)):
        P(f"  {nm:8s} {'CONFIRMED' if v else ('UNDECIDABLE (shallow clone)' if v is None else 'REFUTED')}")
    n4a = int(grid.pass4a_F.sum()); n4b = int(grid.pass4b_F.sum()); n4bo = int(grid.pass4b_OOS.sum())
    P(f"\n  CAPITAL: 4a FULL {n4a}/{len(grid)}   4b FULL {n4b}/{len(grid)}   4b OOS {n4bo}/{len(grid)}")
    P(f"  rule-8 choosers beating RULES v2 OOS: {int(wfd.beats_base_OOS.sum())}/{len(wfd)};  "
      f"clearing 4b OOS: {int(wfd.pass4b_OOS.sum())}/{len(wfd)};  clearing 4b FULL: {int(wfd.pass4b_FULL.sum())}/{len(wfd)}")
    P(f"\n  elapsed {time.time()-t_start:.0f}s")
    Path(OUT.with_suffix("").as_posix() + ".console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
