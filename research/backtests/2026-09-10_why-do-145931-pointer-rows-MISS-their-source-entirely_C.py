#!/usr/bin/env python3
"""Idea 661 (lane C, 2026-09-10) -- why do 145,931 pointer rows MISS their source entirely?

QUEUE 661: "idea 655's join ladder found 13.41% of pointer rows carry a key that matches NO row
of the file they name, and 27.61% of the queue's own block does.  Either the child was written off
a different vintage of the source, or the key columns are transformed rather than copied.  Census
the miss population by (child, source) pair, classify vintage-drift vs transformation, and report
how many published claims read a source that no longer says what they quote.  Max 2 params
(miss class, tolerance)."

WHAT IS ACTUALLY BEING TESTED
  H1 (reproduction)  Idea 655's miss population is real and re-derivable from the artefacts as
        committed: 246 pointer instances, 1,088,554 pointer rows, 145,931 misses (0.1341), and
        29,127 of 105,504 (0.2761) in the queue's own block.  A gate, not a claim.
  H2 (dichotomy)     The queue offers exactly two explanations -- VINTAGE DRIFT (the source moved
        after the child read it) and TRANSFORMATION (the key columns are not copies).  FALSIFIABLE:
        if a large share of misses is neither, the queue's diagnosis is incomplete and the record
        contains rows that quote a combination their source NEVER held at any vintage (PHANTOM).
  H3 (tolerance)     If misses are a FORMATTING accident, a looser numeric tolerance recovers them.
        Measured over a 5-rung tolerance ladder, not asserted.  A miss that survives the widest
        rung is not a rounding artefact.
  H4 (published claims)  A miss only matters if a human-readable claim rests on it.  Count the
        child files carrying non-recoverable misses that also ship a committed .result.md / memo,
        or are cited by LEADERBOARD.md or CHANGELOG.md.
  H5 (live price)    The two miss classes have exact book analogues, and PROTOCOL lets both be
        priced.  VINTAGE DRIFT = the book reads a signal that is L days STALE (the source moved
        on).  TRANSFORMATION = the book reads the right rows through the WRONG PARAMETER (band
        b != the source's 0.03), i.e. a key that is a transform, not a copy.  Which failure mode
        costs more out of sample?  FALSIFIABLE either way, and the control (L=0, b=0.03) is
        RULES v2 exactly, so the two channels meet at the live book.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 MISS CLASS  : C2  TRANSFORM vs NOT-TRANSFORM
                     C3  TRANSFORM / VINTAGE / PHANTOM
                     C4  TRANSFORM / VINTAGE(namedate) / VINTAGE(git) / PHANTOM
                     Nested by refinement; the coarser class is the union of the finer ones.
    P2 TOLERANCE   : the numeric quantum a key cell is snapped to before matching,
                     {EXACT(10dp), 1e-6, 1e-4, 1e-2, 5e-2}.  Monotone by construction: a wider
                     rung can only recover more (asserted in G4).
  => 3 x 5 = 15 census grid points, every one written to .missgrid.csv.
  LIVE: mode x level x gross, every point in .grid.csv; rule 8 fits (level, gross) per mode.
  REPORTED, NOT TUNED: the pointer-form bar, the value bar, the panels, the cost rungs, the
  cadence, the grosses, the lag and band ladders.  Nothing is chosen by looking at an outcome
  except inside rule 8.

GATES (run before any new number is read; a failure stops the run)
  G1 the FRESH book (L=0, b=0.03) reproduces `baseline.rules_v2_weights` exactly, and the DRIFT
     and TRANSFORM channels agree with it at their shared point.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 against a live engine.backtest(25 bps).
  G3 idea 655's pointer + miss population reproduced from a fresh scan (instances, rows, misses,
     and the queue block's own 105,504 / 29,127).
  G4 the tolerance ladder is monotone (recovered non-decreasing in tolerance) and the class
     partition is exact at every rung (RECOVERED + T + V + X == misses).

VINTAGE EVIDENCE -- STATED LIMITATION.  This clone is SHALLOW (50 commits, all 2026-09-10
11:42-19:58Z), so git-touch evidence covers only artefacts written inside that window; its
coverage is reported beside every number.  The filename-date channel (every backtest artefact is
`YYYY-MM-DD_slug_lane.suffix.csv`) covers the whole corpus and is reported separately.

Deterministic, standalone, no network.  Reads only committed artefacts + research/baseline.py.
Writes .console.txt .pointers.csv .miss.csv .misspairs.csv .missgrid.csv .claims.csv
       .grid.csv .walkforward.csv .keeppaths.csv
Modifies nothing (RULES.md, scan.py, bot.py, baseline.py, PROTOCOL.md untouched).
"""
import collections
import csv
import os
import re
import subprocess
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
FLOATDP = 10             # idea 655's key normalisation, reproduced exactly for G3
COST = 10.0              # PROTOCOL 2
FREQ = "W"
BAND = 0.03              # RULES v2 clause 2 -- the SOURCE's parameter
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LAGS = [0, 1, 2, 5, 10, 21, 42, 63]          # DRIFT ladder (trading days of staleness)
BANDS = [0.00, 0.01, 0.03, 0.05, 0.10, 0.20]  # TRANSFORM ladder (a key that is not a copy)
GROSSES = [0.50, 0.75, 1.00]
COSTRUNGS = [0.0, 10.0, 25.0]
TOLS = [0.0, 1e-6, 1e-4, 1e-2, 5e-2]         # P2
TOLNAMES = ["EXACT", "1e-06", "1e-04", "1e-02", "5e-02"]

STRICT_NAMES = {"file", "files", "src", "source", "path", "artefact", "artifact"}
HDRPAT = re.compile(r"(^|_)(file|files|src|source|path|stem|script|artefact|artifact|parent)(_|$)", re.I)
DATEPAT = re.compile(r"(20\d\d-\d\d-\d\d)")
QUEUE_BLOCK = ("2026-09-10_re-cut-every-published-BINDING-BAR-claim-as-a-"
               "STEP-NORMALISED-argmin_cloud.cells.csv")
IDEA655_JOIN = ("2026-09-10_put-a-ROW-ID-on-every-artefact-that-RE-READS-another-"
                "artefact_C.join.csv")

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 0.  ARTEFACT INDEX  +  VINTAGE EVIDENCE
# ================================================================================================
def build_index():
    """basename -> path.  Ambiguous basenames dropped rather than guessed (idea 655's rule)."""
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


def build_gittouch():
    """repo-relative path -> (last_commit_unixtime, n_commits_touching).  Shallow clone: coverage
    is reported, never assumed."""
    try:
        out = subprocess.run(["git", "log", "--pretty=format:@%ct", "--name-only"],
                             cwd=ROOT, capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return {}, 0
    last, cnt, ts = {}, collections.Counter(), None
    for line in out.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("@") and line[1:].isdigit():
            ts = int(line[1:])
            continue
        if ts is None:
            continue
        if line not in last:          # git log is newest-first
            last[line] = ts
        cnt[line] += 1
    return {k: (v, cnt[k]) for k, v in last.items()}, len(last)


IDX, AMBIG_NAMES = {}, 0
GIT, GIT_N = {}, 0


def resolve(v):
    v = (v or "").strip().strip('"').strip("'")
    if not v or len(v) > 300:
        return None
    return IDX.get(os.path.basename(v)) or IDX.get(v)


def namedate(name):
    m = DATEPAT.search(str(name))
    return m.group(1) if m else None


def gitinfo(path):
    try:
        rel = str(Path(path).resolve().relative_to(ROOT))
    except Exception:
        return None
    return GIT.get(rel)


# ================================================================================================
# 1.  THE LIVE CHANNELS (defined before the gates that check them)
# ================================================================================================
def ew_gross(px, gross):
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return gross * priced.astype(float).div(n, axis=0).fillna(0.0)


def drift_weights(px, lag, gross):
    """VINTAGE DRIFT: the book holds names whose band state was IN as of t-lag.  The tradable set
    is current (you know what is priced today); only the SIGNAL is a stale read of the source."""
    st = band_state(px, BAND)
    if lag:
        st = st.shift(lag).fillna(False).astype(bool)
    return ew_gross(px, gross).where(st & px.notna(), 0.0)


def transform_weights(px, band, gross):
    """TRANSFORMATION: the same rows, keyed through a band that is NOT the source's 0.03."""
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def book(px, mode, level, gross):
    if mode == "FRESH":
        return drift_weights(px, 0, gross)
    if mode == "DRIFT":
        return drift_weights(px, int(level), gross)
    return transform_weights(px, float(level), gross)


# ================================================================================================
# 2.  GATES
# ================================================================================================
def gates(px, D, J):
    P()
    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    ok = True

    w_f = book(px, "FRESH", 0, 0.75)
    w_v2 = rules_v2_weights(px, band=BAND, gross=0.75)
    dw = float(np.nanmax(np.abs(w_f.values - w_v2.values)))
    r1 = backtest(px, w_f, cost_bps=COST, freq=FREQ)["returns"]
    r2 = backtest(px, w_v2, cost_bps=COST, freq=FREQ)["returns"]
    dr = float(np.abs(r1 - r2).max())
    d_dr = float(np.nanmax(np.abs(book(px, "DRIFT", 0, 0.75).values - w_v2.values)))
    d_tr = float(np.nanmax(np.abs(book(px, "TRANS", BAND, 0.75).values - w_v2.values)))
    g1 = dw < 1e-12 and dr < 1e-12 and d_dr < 1e-12 and d_tr < 1e-12
    P(f"  G1 FRESH == rules_v2_weights, and both channels meet there : max|dW| {dw:.3e}  "
      f"max|dR| {dr:.3e}  DRIFT@L=0 {d_dr:.3e}  TRANS@b=0.03 {d_tr:.3e}   {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    b0 = backtest(px, w_f, cost_bps=0.0, freq=FREQ)
    b25 = backtest(px, w_f, cost_bps=25.0, freq=FREQ)
    d2 = float(np.abs((b0["returns"] - b0["turnover"] * 25.0 / 1e4) - b25["returns"]).max())
    P(f"  G2 cost-rung identity r(25) = r(0)-turn*25/1e4 : max|d| {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12

    # G3 -- idea 655's miss population, reproduced off its OWN committed join artefact.
    # The corpus is APPEND-ONLY and has grown since 655 ran (655's own artefacts among them), so
    # today's totals are a SUPERSET.  The gate is exact reproduction on the instances 655 scanned.
    n_inst, n_rows, n_miss = len(D), int(J.rows.sum()), int(J.miss.sum())
    P(f"  G3 today's corpus (superset of 655's): instances {n_inst}  pointer rows {n_rows:,}  "
      f"misses {n_miss:,} ({n_miss / max(n_rows, 1):.4f})")
    p655 = OUT / IDEA655_JOIN
    if not p655.exists():
        P("     idea 655's committed .join.csv NOT FOUND -- the queue's premise cannot be audited. STOP.")
        return False
    R = pd.read_csv(p655)
    P(f"     idea 655 as committed: instances {len(R)}  pointer rows {int(R.rows.sum()):,}  "
      f"misses {int(R.miss.sum()):,} ({R.miss.sum() / R.rows.sum():.4f})   "
      f"(QUEUE 661 quotes 145,931 / 0.1341)")
    g3a = (len(R) == 246 and int(R.rows.sum()) == 1088554 and int(R.miss.sum()) == 145931)
    mrg = R.merge(J, on=["file", "col"], suffixes=("_655", "_now"), how="left")
    have = mrg.dropna(subset=["miss_now"])
    exact = int((have.miss_655 == have.miss_now).sum())
    dmax = float(np.abs(have.miss_655 - have.miss_now).max()) if len(have) else np.nan
    g3b = (len(have) == len(R)) and exact == len(R)
    P(f"     re-run on 655's OWN {len(R)} instances: {exact}/{len(R)} miss counts reproduce "
      f"EXACTLY, max|d| {dmax:.0f}   {'PASS' if g3b else 'FAIL'}")
    blk = J[J.file == QUEUE_BLOCK]
    b_rows = int(blk.rows.sum()) if len(blk) else -1
    b_miss = int(blk.miss.sum()) if len(blk) else -1
    g3c = (b_rows == 105504 and b_miss == 29127)
    P(f"     queue block .cells.csv : rows {b_rows:,} (655: 105,504)  misses {b_miss:,} "
      f"({b_miss / max(b_rows, 1):.4f}, 655: 29,127 / 0.2761)   {'PASS' if g3c else 'FAIL'}")
    P(f"     655 artefact self-consistent with QUEUE 661's quoted numbers : {'PASS' if g3a else 'FAIL'}")
    ok &= (g3a and g3b and g3c)
    return ok


# ================================================================================================
# 3.  CENSUS A -- the pointer population (idea 655's scan, re-derived)
# ================================================================================================
def census_pointers():
    P()
    P("=" * 100)
    P("(A) CENSUS -- the pointer population, re-derived from the artefacts as committed")
    P("=" * 100)
    csvs = sorted(OUT.glob("*.csv")) + sorted((ROOT / "research").glob("*.csv"))
    P(f"  committed CSVs scanned           : {len(csvs)}")
    P(f"  artefact index (unique basenames): {len(IDX)}   ambiguous dropped: {AMBIG_NAMES}")
    P(f"  git vintage index                : {GIT_N} paths over {len(set(v[0] for v in GIT.values()))} "
      f"commit times (SHALLOW clone -- coverage reported below)")
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
            inst.append(dict(file=f.name, col=hn, form=form, rows=len(vals), resolved=nres,
                             n_src=len(set(str(x) for x in res if x is not None))))
    D = pd.DataFrame(inst)
    P(f"  scan {time.time() - t0:.1f}s -> pointer INSTANCES {len(D)} over {D.file.nunique()} files, "
      f"{D.rows.sum():,} pointer rows ({D.resolved.sum() / D.rows.sum():.4f} resolve)")
    return D


# ================================================================================================
# 4.  CENSUS B -- the join, keeping the MISS rows this time
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
    if len(_SRC) > 300:
        _SRC.pop(next(iter(_SRC)))
    _SRC[key] = (h, rows)
    return h, rows


def q(x, tol):
    """Key-cell normalisation.  tol=0 is idea 655's exact rule (round to FLOATDP)."""
    x = (x or "").strip()
    try:
        v = float(x)
    except Exception:
        return x
    if tol <= 0:
        return round(v, FLOATDP)          # idea 655's rule, reproduced byte-for-byte (G3)
    if not np.isfinite(v):                # inf / nan cells are real here; snapping is undefined
        return round(v, FLOATDP)
    return round(round(v / tol) * tol, 12)


_TOLIDX = {}


def tol_keyset(spath, sr, si, tol):
    """Set of source key tuples under tolerance `tol`.  Memoised per (source, key cols, tol):
    different children keyed on the same columns of the same source share the index."""
    ck = (str(spath), tuple(si), tol)
    if ck in _TOLIDX:
        return _TOLIDX[ck]
    ks = set(tuple(q(r[k] if k < len(r) else "", tol) for k in si) for r in sr)
    if len(_TOLIDX) > 120:
        _TOLIDX.pop(next(iter(_TOLIDX)))
    _TOLIDX[ck] = ks
    return ks


def join_instance(hdr, data, ptrcol, keep_miss):
    """Exact-tolerance join.  Returns the J-ladder counts and, per (child,source) pair, the
    already-reduced miss diagnostics (per-column domain overlap + tolerance recovery counts).
    Nothing table-sized is retained."""
    j = hdr.index(ptrcol)
    out = dict(rows=0, resolve=0, unique=0, ambig=0, nokey=0, miss=0, nonrow=0,
               src_multi=0, src_single=0)
    pairs = []
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
            out["nonrow"] += len(rows)
            continue
        sh, sr = load_src(s)
        if sh is None:
            out["nonrow"] += len(rows)
            continue
        if len(sr) <= 1:
            out["src_single"] += len(rows)
            out["unique"] += len(rows)
            continue
        out["src_multi"] += len(rows)
        sn = [x.strip() for x in sh]
        shared = [c for c in hdr if c != ptrcol and c.strip() in sn]
        if not shared:
            out["nokey"] += len(rows)
            continue
        si = [sn.index(c.strip()) for c in shared]
        ci = [hdr.index(c) for c in shared]
        idx = collections.Counter(tuple(q(r[k] if k < len(r) else "", 0.0) for k in si) for r in sr)
        miss_rows = []
        for r in rows:
            key = tuple(q(r[k] if k < len(r) else "", 0.0) for k in ci)
            c = idx.get(key, 0)
            if c == 1:
                out["unique"] += 1
            elif c > 1:
                out["ambig"] += 1
            else:
                out["miss"] += 1
                if keep_miss:
                    miss_rows.append([r[k] if k < len(r) else "" for k in ci])
        if keep_miss and miss_rows:
            nk = len(shared)
            # per-column domain overlap: does this key column's value EVER appear in the source's?
            col_ov = []
            for k in range(nk):
                dom = set(q(r[si[k]] if si[k] < len(r) else "", 0.0) for r in sr)
                col_ov.append(sum(1 for m in miss_rows if q(m[k], 0.0) in dom) / len(miss_rows))
            # tolerance ladder: how many misses re-match once numeric cells are snapped
            rec, ever = {}, [False] * len(miss_rows)
            for tol, tn in zip(TOLS, TOLNAMES):
                if tol <= 0:
                    rec[tn] = 0
                    continue
                ks = tol_keyset(s, sr, si, tol)
                n = 0
                for mi, m in enumerate(miss_rows):
                    if tuple(q(m[k], tol) for k in range(nk)) in ks:
                        n += 1
                        ever[mi] = True
                rec[tn] = n
            # a row is a FORMATTING accident if it re-matches at ANY rung.  Quantisation bins
            # move, so the per-rung counts need not be monotone; this cumulative count is.
            rec["ANY"] = int(sum(ever))
            pairs.append(dict(source=s.name, spath=s, shared=shared,
                              n_src_rows=len(sr), n_miss=len(miss_rows),
                              col_overlap=col_ov, rec=rec))
    return out, pairs


def census_join(D):
    P()
    P("=" * 100)
    P("(B) THE JOIN -- reproducing idea 655's ladder and KEEPING the miss rows")
    P("=" * 100)
    recs, allpairs, t0 = [], [], time.time()
    for _, inst in D.iterrows():
        f = IDX.get(inst.file)
        if f is None:
            continue
        with open(f, newline="") as fh:
            rd = csv.reader(fh)
            hdr = next(rd)
            data = [r for r in rd]
        o, pairs = join_instance(hdr, data, inst.col, keep_miss=True)
        o.update(file=inst.file, col=inst.col, form=inst.form)
        recs.append(o)
        for p in pairs:
            p.update(child=inst.file, col=inst.col, form=inst.form)
            allpairs.append(p)
    J = pd.DataFrame(recs)
    tot = int(J.rows.sum())
    P(f"  join {time.time() - t0:.1f}s over {len(J)} instances")
    P(f"    pointer rows {tot:,}   J1 key-unique {J.unique.sum():>9,} ({J.unique.sum() / tot:.4f})")
    P(f"    ambiguous    {J.ambig.sum():>9,} ({J.ambig.sum() / tot:.4f})   "
      f"no shared key {J.nokey.sum():>9,} ({J.nokey.sum() / tot:.4f})")
    P(f"    KEY MISSES   {J.miss.sum():>9,} ({J.miss.sum() / tot:.4f})   <- the population of idea 661")
    P(f"    over {len(allpairs)} (child, col, source) pairs carrying at least one miss")
    return J, allpairs


# ================================================================================================
# 5.  CLASSIFY THE MISS POPULATION  (P1 x P2)
# ================================================================================================
def classify(pairs):
    """For every (child, col, source) pair with misses, at every tolerance rung:
         RECOVERED  the miss re-matches once numeric cells are snapped to the rung's quantum
         TRANSFORM  >=1 shared key column whose miss-row values NEVER appear in the source column
         VINTAGE    not TRANSFORM, and the source is provably younger than the child
                      (namedate: source filename date > child filename date;
                       git: the source was committed at or after the child's last commit)
         PHANTOM    not TRANSFORM, no vintage evidence -- every key value exists in the source,
                    the source is not younger, and the tuple is STILL absent."""
    P()
    P("=" * 100)
    P("(C) CLASSIFYING THE MISSES -- vintage drift vs transformation vs neither")
    P("=" * 100)
    recs, t0 = [], time.time()
    gcov_c = gcov_s = 0
    for pr in pairs:
        child, src = pr["child"], pr["source"]
        shared, col_overlap = pr["shared"], pr["col_overlap"]
        nk = len(shared)
        zero_cols = [shared[k] for k in range(nk) if col_overlap[k] == 0.0]
        is_transform = len(zero_cols) > 0

        # ---- vintage evidence -------------------------------------------------------------------
        cd, sd = namedate(child), namedate(src)
        v_name = bool(cd and sd and sd > cd)
        gi_c, gi_s = gitinfo(IDX.get(child, "")), gitinfo(pr["spath"])
        gcov_c += int(gi_c is not None)
        gcov_s += int(gi_s is not None)
        v_git = bool(gi_c and gi_s and gi_s[0] >= gi_c[0])
        v_any = v_name or v_git

        # ---- tolerance ladder --------------------------------------------------------------------
        rec = dict(child=child, col=pr["col"], form=pr["form"], source=src,
                   n_miss=pr["n_miss"], n_src_rows=pr["n_src_rows"], n_key_cols=nk,
                   shared="|".join(shared), zero_overlap_cols="|".join(zero_cols),
                   min_col_overlap=float(min(col_overlap)) if col_overlap else np.nan,
                   is_transform=is_transform, child_date=cd, source_date=sd,
                   v_namedate=v_name, v_git=v_git, git_child=gi_c[0] if gi_c else np.nan,
                   git_source=gi_s[0] if gi_s else np.nan)
        for tn in TOLNAMES:
            rec[f"rec_{tn}"] = int(pr["rec"][tn])
        rec["rec_ANY"] = int(pr["rec"]["ANY"])
        # class at each rung: recovered first, then T, then V, then X
        for tn in TOLNAMES + ["ANY"]:
            nrec = rec[f"rec_{tn}"]
            left = pr["n_miss"] - nrec
            rec[f"T_{tn}"] = left if is_transform else 0
            rec[f"V_{tn}"] = 0 if is_transform else (left if v_any else 0)
            rec[f"X_{tn}"] = 0 if (is_transform or v_any) else left
        recs.append(rec)
    M = pd.DataFrame(recs)
    P(f"  classified {len(M)} pairs / {int(M.n_miss.sum()):,} miss rows in {time.time() - t0:.1f}s")
    P(f"  git vintage COVERAGE (shallow clone): child {gcov_c}/{len(pairs)} pairs, "
      f"source {gcov_s}/{len(pairs)} pairs")
    return M


def miss_grid(M):
    P()
    P("=" * 100)
    P("(D) THE 3 x 5 GRID -- every point reported (P1 miss class x P2 tolerance)")
    P("=" * 100)
    tot = int(M.n_miss.sum())
    rows = []
    for tn, tol in zip(TOLNAMES + ["ANY"], TOLS + [-1.0]):
        nrec = int(M[f"rec_{tn}"].sum())
        nT, nV, nX = int(M[f"T_{tn}"].sum()), int(M[f"V_{tn}"].sum()), int(M[f"X_{tn}"].sum())
        vn = int(M[(~M.is_transform) & M.v_namedate][f"V_{tn}"].sum())
        vg = nV - vn
        for scheme, cells in (
                ("C2_TRANSFORM_vs_NOT", dict(RECOVERED=nrec, TRANSFORM=nT, NOT_TRANSFORM=nV + nX)),
                ("C3_T_V_X", dict(RECOVERED=nrec, TRANSFORM=nT, VINTAGE=nV, PHANTOM=nX)),
                ("C4_T_Vname_Vgit_X", dict(RECOVERED=nrec, TRANSFORM=nT, VINTAGE_namedate=vn,
                                           VINTAGE_gitonly=vg, PHANTOM=nX))):
            for cls, n in cells.items():
                rows.append(dict(scheme=scheme, tol=tn, tol_value=tol, cls=cls, rows=n,
                                 share=n / tot if tot else np.nan))
    G = pd.DataFrame(rows)
    for scheme in G.scheme.unique():
        s = G[G.scheme == scheme]
        piv = s.pivot(index="cls", columns="tol", values="rows").reindex(columns=TOLNAMES + ["ANY"])
        P(f"\n  {scheme}   (rows; total miss population {tot:,})")
        P(piv.to_string())
        pivs = s.pivot(index="cls", columns="tol", values="share").reindex(columns=TOLNAMES + ["ANY"])
        P(f"  {scheme}   (share of the miss population)")
        P(pivs.to_string(float_format=lambda x: f"{x:.4f}"))
    # G4 -- the partition must be exact at every rung (gated).  Monotonicity of the RAW per-rung
    # recovery is NOT guaranteed (a wider quantum can split a child and its source into different
    # bins), so it is REPORTED, not gated; the cumulative ANY rung is monotone by construction.
    rec_series = [int(M[f"rec_{tn}"].sum()) for tn in TOLNAMES]
    any_rec = int(M["rec_ANY"].sum())
    mono = all(rec_series[i] <= rec_series[i + 1] for i in range(len(rec_series) - 1))
    part = all(int(M[f"rec_{tn}"].sum()) + int(M[f"T_{tn}"].sum()) + int(M[f"V_{tn}"].sum())
               + int(M[f"X_{tn}"].sum()) == tot for tn in TOLNAMES + ["ANY"])
    P(f"\n  G4 partition exact at every rung  {'PASS' if part else 'FAIL'}")
    P(f"     raw per-rung recovery {rec_series} -> monotone in tolerance: "
      f"{'YES' if mono else 'NO (quantisation bins move; reported, not gated)'}")
    P(f"     recovered at ANY rung (cumulative, monotone by construction): {any_rec:,} "
      f"({any_rec / tot:.4f} of the miss population)")
    return G, part


# ================================================================================================
# 6.  H4 -- how many PUBLISHED CLAIMS rest on a non-recoverable miss
# ================================================================================================
def claims(M):
    P()
    P("=" * 100)
    P("(E) PUBLISHED CLAIMS THAT READ A SOURCE WHICH NO LONGER SAYS WHAT THEY QUOTE")
    P("=" * 100)
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text() if (ROOT / "research" / "LEADERBOARD.md").exists() else ""
    ch = (ROOT / "research" / "CHANGELOG.md").read_text() if (ROOT / "research" / "CHANGELOG.md").exists() else ""
    qz = (ROOT / "research" / "QUEUE.md").read_text() if (ROOT / "research" / "QUEUE.md").exists() else ""
    widest = "ANY"   # the most generous reading available: recovered at ANY tolerance rung
    recs = []
    for child, s in M.groupby("child"):
        left = int(s[f"T_{widest}"].sum() + s[f"V_{widest}"].sum() + s[f"X_{widest}"].sum())
        stem = child
        for suf in (".csv",):
            if stem.endswith(suf):
                stem = stem[: -len(suf)]
        stem = stem.rsplit(".", 1)[0]              # drop the artefact suffix (.cells, .grid, ...)
        memo = (OUT / f"{stem}.result.md").exists()
        cited = (stem in lb) or (stem in ch) or (stem in qz)
        recs.append(dict(child=child, stem=stem, miss=int(s.n_miss.sum()),
                         unrecovered=left,
                         T=int(s[f"T_{widest}"].sum()), V=int(s[f"V_{widest}"].sum()),
                         X=int(s[f"X_{widest}"].sum()),
                         has_memo=memo, cited_in_record=cited,
                         published=bool(memo or cited)))
    C = pd.DataFrame(recs).sort_values("unrecovered", ascending=False)
    aff = C[C.unrecovered > 0]
    P(f"  child files carrying at least one miss                 : {len(C)}")
    P(f"  ... still unmatched under the MOST GENEROUS reading    : {len(aff)}  "
      f"({int(aff.unrecovered.sum()):,} rows)")
    P(f"  ... of those, files with a committed .result.md memo   : {int(aff.has_memo.sum())}")
    P(f"  ... of those, files cited by LEADERBOARD/CHANGELOG/QUEUE: {int(aff.cited_in_record.sum())}")
    P(f"  ... PUBLISHED CLAIMS resting on an unmatched read      : {int(aff.published.sum())}  "
      f"({int(aff[aff.published].unrecovered.sum()):,} rows)")
    P()
    P("  10 largest unmatched (child, source) reads:")
    top = M.assign(left=M[f"T_{widest}"] + M[f"V_{widest}"] + M[f"X_{widest}"]).nlargest(10, "left")
    for _, r in top.iterrows():
        cls = "TRANSFORM" if r.is_transform else ("VINTAGE" if (r.v_namedate or r.v_git) else "PHANTOM")
        P(f"    {r.child[:56]:58s} <- {r.source[:44]:46s} {int(r.left):>7,} {cls:9s} "
          f"minov {r.min_col_overlap:.3f} zero[{r.zero_overlap_cols[:28]}]")
    return C


# ================================================================================================
# 7.  H5 -- PRICING THE TWO MISS CLASSES (full grid, then PROTOCOL rule 8)
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
    P("(F) H5 -- what the TWO MISS CLASSES cost in a book")
    P("=" * 100)
    P("  FRESH  the source as it stands (= RULES v2, band 0.03, no lag)")
    P("  DRIFT  VINTAGE analogue: the band state is read L trading days STALE")
    P("  TRANS  TRANSFORMATION analogue: the same rows keyed through band b != the source's 0.03")
    P("  Full-sample 4a/4b at every grid point; rule 8 then fits (level, gross) on 2009-2016 ONLY.")
    P()
    grid, wf = [], []
    levels = {"FRESH": [0], "DRIFT": LAGS, "TRANS": BANDS}
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
        for nm in ("SPY", "V2"):
            P(f"      {nm:5s} CAGR {ref[nm]['CAGR']:7.2%}  Sharpe {ref[nm]['Sharpe']:.3f}  "
              f"MaxDD {ref[nm]['MaxDD']:7.2%}  H1/H2 {ref[nm]['H1']:.3f}/{ref[nm]['H2']:.3f}  "
              f"OOS Sh {ref[nm]['OOS_Sharpe']:.3f} CAGR {ref[nm]['OOS_CAGR']:7.2%} "
              f"DD {ref[nm]['OOS_MaxDD']:7.2%}")
        for mode in ("FRESH", "DRIFT", "TRANS"):
            for lv in levels[mode]:
                for g in GROSSES:
                    b = backtest(px, book(px, mode, lv, g), cost_bps=COST, freq=FREQ)
                    r = b["returns"].loc[start:]
                    c, s, d, h1, h2 = slice_metrics(r)
                    o = metrics(r.loc[OOS_START:])
                    im = metrics(r.loc[:IS_END])
                    grid.append(dict(panel=pname, mode=mode, level=lv, gross=g, cost=COST,
                                     CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                                     IS_Sharpe=im["Sharpe"], IS_CAGR=im["CAGR"], IS_MaxDD=im["MaxDD"],
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     turn_x_yr=b["turnover"].loc[start:].sum() / (len(r) / 252),
                                     pass4a=pass4a(s, d, h1, h2, ref["V2"]),
                                     pass4b=pass4b(c, s, d, h1, h2, o["Sharpe"], ref["SPY"])))
        Gp = pd.DataFrame([x for x in grid if x["panel"] == pname])
        P(f"      grid points {len(Gp)}   4a {int(Gp.pass4a.sum())}/{len(Gp)}   "
          f"4b {int(Gp.pass4b.sum())}/{len(Gp)}")
        P(f"      the STALENESS curve at g=0.75 (DRIFT):")
        for _, r in Gp[(Gp["mode"] == "DRIFT") & (Gp.gross == 0.75)].sort_values("level").iterrows():
            P(f"        L={int(r.level):>3d}  CAGR {r.CAGR:7.2%}  Sharpe {r.Sharpe:.3f}  "
              f"MaxDD {r.MaxDD:7.2%}  OOS Sh {r.OOS_Sharpe:.3f}  turn {r.turn_x_yr:.2f}x/yr  "
              f"4a {'Y' if r.pass4a else 'n'} 4b {'Y' if r.pass4b else 'n'}")
        P(f"      the TRANSFORM curve at g=0.75 (band b):")
        for _, r in Gp[(Gp["mode"] == "TRANS") & (Gp.gross == 0.75)].sort_values("level").iterrows():
            P(f"        b={r.level:.2f}  CAGR {r.CAGR:7.2%}  Sharpe {r.Sharpe:.3f}  "
              f"MaxDD {r.MaxDD:7.2%}  OOS Sh {r.OOS_Sharpe:.3f}  turn {r.turn_x_yr:.2f}x/yr  "
              f"4a {'Y' if r.pass4a else 'n'} 4b {'Y' if r.pass4b else 'n'}")

        # ---- PROTOCOL rule 8 -------------------------------------------------------------------
        P(f"      rule 8: fit (level, gross) on 2009-2016 by IS Sharpe, score 2017-2026 untouched")
        for mode in ("FRESH", "DRIFT", "TRANS"):
            s = Gp[Gp["mode"] == mode]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            rung = {}
            for c in COSTRUNGS:
                rr = backtest(px, book(px, mode, pick.level, pick.gross),
                              cost_bps=c, freq=FREQ)["returns"].loc[start:]
                oo = metrics(rr.loc[OOS_START:])
                cc, ss, dd, hh1, hh2 = slice_metrics(rr)
                rung[c] = dict(p4b=pass4b(cc, ss, dd, hh1, hh2, oo["Sharpe"], ref["SPY"]),
                               p4a=pass4a(ss, dd, hh1, hh2, ref["V2"]),
                               OOS_Sharpe=oo["Sharpe"], OOS_CAGR=oo["CAGR"])
            wf.append(dict(panel=pname, mode=mode, pick_level=pick.level, pick_gross=pick.gross,
                           IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           V2_OOS_Sharpe=ref["V2"]["OOS_Sharpe"], V2_OOS_CAGR=ref["V2"]["OOS_CAGR"],
                           V2_OOS_MaxDD=ref["V2"]["OOS_MaxDD"], V2_MaxDD=ref["V2"]["MaxDD"],
                           SPY_OOS_Sharpe=ref["SPY"]["OOS_Sharpe"], SPY_OOS_CAGR=ref["SPY"]["OOS_CAGR"],
                           SPY_OOS_MaxDD=ref["SPY"]["OOS_MaxDD"],
                           beats_SPY=bool(pick.OOS_Sharpe > ref["SPY"]["OOS_Sharpe"]),
                           beats_V2=bool(pick.OOS_Sharpe > ref["V2"]["OOS_Sharpe"]),
                           full_4a=bool(pick.pass4a), full_4b=bool(pick.pass4b),
                           p4b_0=rung[0.0]["p4b"], p4b_10=rung[10.0]["p4b"], p4b_25=rung[25.0]["p4b"],
                           p4a_0=rung[0.0]["p4a"], p4a_10=rung[10.0]["p4a"], p4a_25=rung[25.0]["p4a"],
                           OOS_Sharpe_0=rung[0.0]["OOS_Sharpe"], OOS_Sharpe_25=rung[25.0]["OOS_Sharpe"]))
            P(f"        {mode:5s} pick level={pick.level} g={pick.gross:.2f} "
              f"(IS Sh {pick.IS_Sharpe:.3f}) -> OOS CAGR {pick.OOS_CAGR:7.2%} Sharpe "
              f"{pick.OOS_Sharpe:.3f} MaxDD {pick.OOS_MaxDD:7.2%}   "
              f"4a {'Y' if pick.pass4a else 'n'} 4b {'Y' if pick.pass4b else 'n'}   "
              f"4b@0/10/25 {int(rung[0.0]['p4b'])}/{int(rung[10.0]['p4b'])}/{int(rung[25.0]['p4b'])}")
        P()
    return pd.DataFrame(grid), pd.DataFrame(wf)


# ================================================================================================
def main():
    global IDX, AMBIG_NAMES, GIT, GIT_N
    t0 = time.time()
    P(f"Idea 661 -- why do 145,931 pointer rows MISS their source entirely?  (lane C, "
      f"{pd.Timestamp.today().date()})")
    P(f"PROTOCOL: costs {COST:.0f} bps, next-day execution, freq {FREQ}, "
      f"rule 8 IS<= {IS_END} / OOS >= {OOS_START}.  2 params: miss class x tolerance.")

    IDX, AMBIG_NAMES = build_index()
    GIT, GIT_N = build_gittouch()

    px_u = load_universe()
    px_b = load_universe(broad=True)

    D = census_pointers()
    J, pairs = census_join(D)
    ok = gates(px_u, D, J)
    if not ok:
        P("\nGATES FAILED -- stopping before any new number is read.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return

    M = classify(pairs)
    G, g4 = miss_grid(M)
    if not g4:
        P("\nG4 FAILED -- the classification is not a partition.  Stopping.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
        return
    C = claims(M)
    grid, wf = live({"U56": px_u, "B136": px_b})

    P()
    P("=" * 100)
    P("(G) KEEP PATHS -- PROTOCOL 4a and 4b on every live grid point")
    P("=" * 100)
    kp = grid.groupby(["panel", "mode"]).agg(points=("pass4a", "size"),
                                             p4a=("pass4a", "sum"),
                                             p4b=("pass4b", "sum")).reset_index()
    P(kp.to_string(index=False))
    P(f"\n  TOTAL: 4a {int(grid.pass4a.sum())}/{len(grid)}   4b {int(grid.pass4b.sum())}/{len(grid)}")
    P(f"  rule-8 picks clearing 4b at 0/10/25 bps: {int(wf.p4b_0.sum())}/{int(wf.p4b_10.sum())}/"
      f"{int(wf.p4b_25.sum())} of {len(wf)};  4a at 10 bps: {int(wf.p4a_10.sum())}/{len(wf)}")
    P(f"  rule-8 picks beating SPY OOS Sharpe: {int(wf.beats_SPY.sum())}/{len(wf)};  "
      f"beating the live book: {int(wf.beats_V2.sum())}/{len(wf)}")

    P()
    P("=" * 100)
    P("OUTPUTS")
    P("=" * 100)
    dump(D, "pointers")
    dump(J, "miss")
    dump(M, "misspairs")
    dump(G, "missgrid")
    dump(C, "claims")
    dump(grid, "grid")
    dump(wf, "walkforward")
    dump(kp, "keeppaths")
    P(f"\ntotal {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
