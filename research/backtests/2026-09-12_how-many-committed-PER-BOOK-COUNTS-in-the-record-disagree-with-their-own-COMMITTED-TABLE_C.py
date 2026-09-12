#!/usr/bin/env python3
"""Idea 843 (lane C, 2026-09-12) — how many committed 'k of n books/arms' COUNTS in the record
disagree with their own COMMITTED TABLE?

THE DIAGNOSIS THIS RUN IS GROUNDED IN.  Idea 839 reproduced idea 832's per-book delta table
bit-for-bit and found the prose count that travels with it ('9 of 11 books carrying the sign') is
not what the table says: 8 strictly negative, 1 positive, 2 exactly zero of 11 defined.  One
mis-stated count is an anecdote.  This run asks whether it is a PATTERN: re-derive every committed
'k of n <unit>' count in research/backtests/ DIRECTLY from the CSVs and markdown tables the SAME
file committed, and report the disagreements.

TWO TUNED PARAMETERS, exactly as the queue allows:
  P1  COUNT DETECTOR — D1 NARROW / D2 MEDIUM / D3 WIDE (how hard the machine tries to re-derive k
                       from the file's own committed tables; see DETECTORS below).
  P2  SAMPLE         — S1 BOOKS_ARMS (the queue's literal set: nouns book/books/arm/arms),
                       S2 UNITS (S1 + cell/panel/row/file/pick/draw/point/name/rung/arm-row),
                       S3 ALL (every 'k of n' claim in the sampled files, whatever the noun).
Every one of the 9 grid points is REPORTED.  The headline cell is (D2, S1) — the queue's own unit
set at the middle detector — declared before the grid was run.

WHY A CHANCE FLOOR IS REPORTED BESIDE EVERY AGREEMENT RATE.  A detector that can produce many
different counts from a table will 'agree' with almost any k.  So for every claim this run also
records A = the SET of counts the detector can produce from that claim's own tables, and the
chance floor |A| / (n+1) — the probability that a UNIFORMLY RANDOM numerator in [0, n] would also
have been called AGREE.  An agreement rate that does not clear its own chance floor is reported as
uninformative, not as a confirmation.

CONVENTIONS, DECLARED BEFORE ANY NUMBER:
  C1  A CLAIM is a match of r'(\\d+) of (\\d+) <word>' in a committed .result.md / _MEMO.md /
      .memo.md file under research/backtests/, after markdown emphasis (* ` _) is stripped, with
      0 <= k <= n, 2 <= n <= 100000.  The NOUN is the word token that follows n (lower-cased,
      trailing 's' stripped).  Claims inside fenced code blocks are excluded (they are usually
      program text, not prose).
  C2  A claim's SOURCES are only tables the SAME file committed: (a) every markdown table in the
      file itself, (b) every sibling CSV, i.e. research/backtests/<same stem>.*.csv[.gz], where the
      stem is the file name minus .result.md / _MEMO.md / .memo.md.  Sibling CSVs above
      MAX_CSV_BYTES (20 MB) or MAX_ROWS (200,000) rows are SKIPPED and counted as skipped.
  C3  A UNIVERSE is a set of exactly n rows drawn from one source table: the whole table when
      len(T) == n (all detectors), or a single-column group-by block of size n (D2, D3 only).
  C4  A claim AGREES when some predicate in the detector's family, evaluated on some universe,
      yields exactly k.  It DISAGREES when it has >= 1 universe and no predicate yields k.  A claim
      with 0 universes is NOT RE-DERIVABLE and is excluded from both numerator and denominator of
      the disagreement rate (its count is published separately).
  C5  Rates are over re-derivable claims only.  Duplicate identical claim strings inside one file
      are kept (the record repeats its headline in prose and in tables; both are published counts).
  C6  The price table (section 4) is read exactly as PROTOCOL rules 2/3/4/8: weights at close t
      applied t+1, 10 bps per unit turnover, weekly cadence, scoring from px.index[260], IS
      2009..2016-12-31, OOS 2017-01-01..end, 4a against the live RULES v2 book, 4b against SPY.

DETECTORS (the predicate families; all evaluated on a universe U of exactly n rows):
  D1 NARROW  per column: truthy count and falsy count (True/'PASS'/'KEEP'/'YES'/'Y'/'OK'/1/✓ and
             their negations); per NUMERIC column: (x > 0), (x < 0), (x == 0).
             Universes: whole tables only.
  D2 MEDIUM  D1 + per numeric column (x >= 0), (x <= 0), notna, isna.
             Universes: whole tables + single-column group-by blocks of size n.
  D3 WIDE    D2 + per object column with <= 30 distinct values, (col == v) for every value v;
             + the pairwise AND of up to 40 base predicates drawn from different columns.
             Universes: as D2.

PRE-REGISTERED HYPOTHESES (written before the grid was run; all reported either way):
  H_RATE     at the headline cell (D2, S1) at least 10% of re-derivable books/arms counts DISAGREE
             with their own committed tables.
  H_ANCHOR   idea 839's own corrected count ('8 of 11') is re-derived as AGREE from the .perbook.csv
             that file committed, and idea 832's '9 of 11' is NOT re-derivable from it.
  H_FLOOR    the agreement rate clears its own chance floor by >= 0.10 at the headline cell (i.e.
             the detector is measuring something).
  H_SOURCE   at least 25% of all 'k of n' claims in the record have NO committed table of the right
             size at all — the count cannot be checked from the file that published it.
  H_WF       (corpus rule-8 analogue) the (detector, sample) cell chosen on the IS half of the
             corpus (files dated <= 2026-09-07) has a disagreement rate on the OOS half
             (>= 2026-09-08) within 0.10 of its IS value.
  H_NOBOOK   this run produces no tradeable book: neither KEEP path can be claimed by a census.

GATES (printed before any new number; recorded, non-raising):
  G1  ANCHOR — idea 839's committed .perbook.csv has 11 defined deltas of which exactly 8 are
      strictly negative, 1 positive, 2 exactly zero (re-derived here from the CSV, not from prose).
  G2  DETERMINISM — the claim extractor run twice over the same sample returns an identical
      (file, k, n, noun) multiset (SHA-256 of the sorted tuple list).
  G3  DETECTOR UNIT TEST — on 6 synthetic tables with known counts, D1/D2/D3 recover the planted
      count, and on a table with NO column carrying the planted count they do not.
  G4  PRICE — the live RULES v2 book reproduces research/RULES.md's committed 8.66% / 1.2056 /
      -12.05% (bars: 1.00pp / 0.060 / 2.00pp); SPY reproduces 15.23% / 0.8890 / -33.72%.
  G5  PARTITION — the corpus walk-forward split is exhaustive and disjoint (IS + OOS == all files,
      no file in both).
  G6  STANDING CANDIDATE — the reconstructed standing 4b candidate reproduces its own committed memo
      (2026-09-07_u56-top20-g075-4b_C_MEMO.md: 12.79% / 1.064 / -18.31%) on the same bars as G4.

Outputs (all under research/backtests/, all committed):
  .txt           full console log
  .claims.csv    one row per extracted claim: file, k, n, noun, sources, universes, |A| and the
                 agree/disagree verdict under each of D1/D2/D3
  .grid.csv      all 9 (detector, sample) cells: claims, re-derivable, agree, disagree, rates,
                 chance floor, excess
  .disagree.csv  the disagreement list at the headline cell, with the nearest achievable count
  .wf.csv        the corpus walk-forward table AND the PROTOCOL rule-8 price table (both KEEP paths)
  .result.md     the answer
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Run: python3 research/backtests/2026-09-12_how-many-committed-PER-BOOK-COUNTS-in-the-record-disagree-with-their-own-COMMITTED-TABLE_C.py
"""
from __future__ import annotations

import hashlib
import io
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"
STEM = BT / "2026-09-12_how-many-committed-PER-BOOK-COUNTS-in-the-record-disagree-with-their-own-COMMITTED-TABLE_C"

MAX_CSV_BYTES = 20_000_000
MAX_ROWS = 200_000
MAX_GROUPBY_CARD = 50           # a column is a group-by key only if it has <= 50 distinct values
MAX_VALUE_PREDS = 30            # D3: at most 30 (col == v) predicates per object column
MAX_PAIR_BASE = 40              # D3: at most 40 base predicates enter the AND-pair sweep
SPLIT_IS = "2026-09-07"         # corpus walk-forward: files dated <= this are IS
COST_BPS = 10
OOS_START = "2017-01-01"
IS_END = "2016-12-31"

LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ----------------------------------------------------------------------------- claim extraction
EMPH = re.compile(r"[*`_]")
FENCE = re.compile(r"```.*?```", re.S)
CLAIM = re.compile(r"(?<![\d.])(\d{1,6})\s+of\s+(\d{1,6})\b[ \t]*([A-Za-z][A-Za-z-]{1,24})?")

S1_NOUNS = {"book", "arm"}
S2_EXTRA = {"cell", "panel", "row", "file", "pick", "draw", "point", "name", "rung",
            "arm-row", "book-row", "candidate", "memo", "script", "grid", "window", "pair"}


def norm_noun(w: str | None) -> str:
    if not w:
        return ""
    w = w.lower()
    return w[:-1] if len(w) > 3 and w.endswith("s") else w


def extract_claims(path: Path) -> list[dict]:
    txt = path.read_text(errors="replace")
    txt = FENCE.sub(" ", txt)
    txt = EMPH.sub("", txt)
    out = []
    for m in CLAIM.finditer(txt):
        k, n = int(m.group(1)), int(m.group(2))
        if not (2 <= n <= 100_000) or k > n:
            continue
        noun = norm_noun(m.group(3))
        ctx = txt[max(0, m.start() - 70):m.end() + 40].replace("\n", " ")
        out.append(dict(file=path.name, k=k, n=n, noun=noun, claim=f"{k} of {n} {m.group(3) or ''}".strip(),
                        context=re.sub(r"\s+", " ", ctx)))
    return out


# ------------------------------------------------------------------------------ table loading
NUMTOK = re.compile(r"^[+\-−]?[\d,]*\.?\d+([eE][+\-]?\d+)?%?$")


def cellval(s: str):
    s = s.strip().replace("−", "-").replace("**", "")
    if s in ("", "-", "--", "—", "n/a", "N/A", "nan"):
        return np.nan
    t = s.replace(",", "")
    pct = t.endswith("%")
    if pct:
        t = t[:-1]
    if NUMTOK.match(t.replace("%", "")):
        try:
            v = float(t)
            return v / 100.0 if pct else v
        except ValueError:
            return s
    return s


def md_tables(path: Path) -> list[pd.DataFrame]:
    """Every markdown pipe-table in the file, as a DataFrame with numeric coercion."""
    tables, block = [], []
    for line in path.read_text(errors="replace").split("\n"):
        ls = line.strip()
        if ls.startswith("|") and ls.endswith("|") and ls.count("|") >= 2:
            block.append(ls)
        else:
            if len(block) >= 3:
                tables.append(block)
            block = []
    if len(block) >= 3:
        tables.append(block)
    out = []
    for blk in tables:
        rows = [[c for c in b.strip("|").split("|")] for b in blk]
        rows = [r for r in rows if not all(set(c.strip()) <= set(":- ") and c.strip() for c in r)]
        if len(rows) < 2:
            continue
        hdr = [re.sub(r"[^\w ]", "", c).strip() or f"c{i}" for i, c in enumerate(rows[0])]
        body = [r for r in rows[1:] if len(r) == len(hdr)]
        if not body:
            continue
        df = pd.DataFrame([[cellval(c) for c in r] for r in body], columns=_dedup(hdr))
        out.append(df)
    return out


def _dedup(cols):
    seen, out = {}, []
    for c in cols:
        if c in seen:
            seen[c] += 1
            out.append(f"{c}.{seen[c]}")
        else:
            seen[c] = 0
            out.append(c)
    return out


def stem_of(name: str) -> str:
    for suf in (".result.md", "_MEMO.md", ".memo.md", ".KEEP_MEMO.md"):
        if name.endswith(suf):
            return name[: -len(suf)]
    return name.rsplit(".", 1)[0]


_CSV_CACHE: dict[str, list[pd.DataFrame]] = {}
SKIPPED = {"big": 0, "rows": 0, "err": 0, "read": 0}


def sibling_csvs(stem: str, all_files: list[str]) -> list[pd.DataFrame]:
    if stem in _CSV_CACHE:
        return _CSV_CACHE[stem]
    out = []
    for f in all_files:
        if not f.startswith(stem + ".") or not (f.endswith(".csv") or f.endswith(".csv.gz")):
            continue
        p = BT / f
        try:
            if p.stat().st_size > MAX_CSV_BYTES:
                SKIPPED["big"] += 1
                continue
            df = pd.read_csv(p, nrows=MAX_ROWS + 1, low_memory=False)
            if len(df) > MAX_ROWS:
                SKIPPED["rows"] += 1
                continue
            SKIPPED["read"] += 1
            out.append(df)
        except Exception:
            SKIPPED["err"] += 1
    _CSV_CACHE[stem] = out
    return out


# ------------------------------------------------------------------------------- the detectors
TRUTHY = {"true", "yes", "pass", "keep", "y", "ok", "1", "1.0", "✓", "keep-candidate", "passes"}
FALSY = {"false", "no", "fail", "kill", "n", "0", "0.0", "✗", "x", "fails"}


def _num(col: pd.Series) -> pd.Series | None:
    if pd.api.types.is_numeric_dtype(col):
        return col
    c = pd.to_numeric(col, errors="coerce")
    return c if c.notna().sum() >= max(1, int(0.6 * len(col))) else None


def achievable(U: pd.DataFrame, detector: str) -> tuple[set[int], dict[int, str]]:
    """Every row count the detector's predicate family can produce from universe U."""
    counts: dict[int, str] = {}
    base: list[tuple[str, np.ndarray]] = []
    n = len(U)
    for c in list(U.columns)[:80]:
        col = U[c]
        s = col.astype(str).str.strip().str.lower()
        t = s.isin(TRUTHY).to_numpy()
        f = s.isin(FALSY).to_numpy()
        if t.any():
            base.append((f"{c} truthy", t))
        if f.any():
            base.append((f"{c} falsy", f))
        num = _num(col)
        if num is not None:
            v = num.to_numpy(dtype=float)
            base.append((f"{c}>0", v > 0))
            base.append((f"{c}<0", v < 0))
            base.append((f"{c}==0", v == 0))
            if detector in ("D2", "D3"):
                base.append((f"{c}>=0", v >= 0))
                base.append((f"{c}<=0", v <= 0))
                base.append((f"{c} notna", ~np.isnan(v)))
                base.append((f"{c} isna", np.isnan(v)))
        elif detector == "D3":
            vals = col.astype(str).unique()
            if len(vals) <= MAX_VALUE_PREDS:
                for v in vals:
                    base.append((f"{c}=={v}", (col.astype(str) == v).to_numpy()))
    for desc, mask in base:
        counts.setdefault(int(mask.sum()), desc)
    if detector == "D3" and len(base) > 1:
        b = base[:MAX_PAIR_BASE]
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                if b[i][0].split(">")[0].split("<")[0].split("=")[0] == b[j][0].split(">")[0].split("<")[0].split("=")[0]:
                    continue
                counts.setdefault(int((b[i][1] & b[j][1]).sum()), f"{b[i][0]} AND {b[j][0]}")
    counts.setdefault(n, "len(table)")
    return set(counts), counts


def universes(tables: list[pd.DataFrame], n: int, detector: str) -> list[pd.DataFrame]:
    out = []
    for T in tables:
        if len(T) == n:
            out.append(T)
        if detector in ("D2", "D3") and len(T) > n:
            for c in list(T.columns)[:40]:
                try:
                    nu = T[c].nunique(dropna=False)
                except Exception:
                    continue
                if 1 < nu <= MAX_GROUPBY_CARD:
                    try:
                        g = T.groupby(T[c].astype(str), dropna=False)
                    except Exception:
                        continue
                    for _, blk in g:
                        if len(blk) == n:
                            out.append(blk)
                            if len(out) > 60:
                                return out
    return out


def judge(claim: dict, tables: list[pd.DataFrame], detector: str) -> dict:
    U = universes(tables, claim["n"], detector)
    if not U:
        return dict(universes=0, nA=0, agree=False, rederivable=False, nearest=np.nan, how="")
    A: set[int] = set()
    how = {}
    for u in U[:20]:
        a, h = achievable(u, detector)
        A |= a
        for kk, d in h.items():
            how.setdefault(kk, d)
    k = claim["k"]
    nearest = min(A, key=lambda a: (abs(a - k), a)) if A else np.nan
    return dict(universes=len(U), nA=len(A), agree=k in A, rederivable=True,
                nearest=nearest, how=how.get(k, "") if k in A else how.get(nearest, ""))


# ------------------------------------------------------------------------------------- gates
def gate_anchor() -> str:
    p = BT / "2026-09-12_is-the-NEGATIVE-NEXT-WINDOW-sign-a-MEAN-REVERSION-fact-or-a-CONDITIONING-artefact_cloud.perbook.csv"
    if not p.exists():
        return "G1 ANCHOR: perbook.csv NOT FOUND — gate cannot run"
    df = pd.read_csv(p)
    cand = [c for c in df.columns if "delta" in c.lower()]
    if not cand:
        return f"G1 ANCHOR: no delta column in {p.name} (cols {list(df.columns)[:8]})"
    g = df[df["cell"] == "OVERLAP21/H756/OTHER3"] if "cell" in df.columns else df
    col = pd.to_numeric(g[cand[0]], errors="coerce")
    neg, pos, zero, defined = int((col < 0).sum()), int((col > 0).sum()), int((col == 0).sum()), int(col.notna().sum())
    ok = (defined == 11 and neg == 8 and pos == 1 and zero == 2)
    return (f"G1 ANCHOR: {p.name} cell OVERLAP21/H756/OTHER3, col '{cand[0]}' -> {neg} negative / {pos} positive / "
            f"{zero} zero of {defined} defined ({len(g)} rows of {len(df)}) — "
            f"{'PASS (idea 839 committed 8/1/2 of 11; idea 832s prose 9 of 11 is not in the table)' if ok else 'MISMATCH vs idea 839 (8/1/2 of 11)'}")


def gate_determinism(files: list[Path]) -> str:
    def digest():
        cl = []
        for f in files:
            cl += [(c["file"], c["k"], c["n"], c["noun"]) for c in extract_claims(f)]
        cl.sort()
        return hashlib.sha256(repr(cl).encode()).hexdigest()[:16], len(cl)
    h1, n1 = digest()
    h2, n2 = digest()
    return f"G2 DETERMINISM: {n1} claims, sha {h1} vs {h2} — {'PASS' if h1 == h2 and n1 == n2 else 'FAIL'}"


def gate_unit() -> str:
    rng = np.random.default_rng(20260912)
    ok = []
    for trial in range(6):
        n = int(rng.integers(6, 30))
        k = int(rng.integers(1, n))
        d = pd.DataFrame({"x": np.r_[-np.ones(k), np.ones(n - k)],
                          "lbl": ["a"] * (n // 2) + ["b"] * (n - n // 2),
                          "pass": [True] * k + [False] * (n - k)})
        for det in ("D1", "D2", "D3"):
            A, _ = achievable(d, det)
            ok.append(k in A)
    # negative control: a table whose columns carry no count equal to k_planted
    neg = pd.DataFrame({"x": np.ones(12), "y": np.ones(12)})   # every predicate gives 0 or 12
    A, _ = achievable(neg, "D2")
    neg_ok = 5 not in A
    return (f"G3 DETECTOR UNIT TEST: planted count recovered {sum(ok)}/{len(ok)} (D1/D2/D3 x 6 tables); "
            f"negative control (k=5 unreachable) {'held' if neg_ok else 'LEAKED'} — "
            f"{'PASS' if all(ok) and neg_ok else 'FAIL'}")


# -------------------------------------------------------------------------------- price table
def top20_weights(px, n=20, gross=0.75):
    """The record's standing 4b candidate (memo 2026-09-07_u56-top20-g075-4b_C_MEMO.md): rank every
    ELIGIBLE name (above its 200d MA, vol20 < 0.60) by the composite WITHOUT the vol scaler, hold
    the top 20 equal-weight at gross/n = 3.75% of NAV each, weekly, 10 bps, next-day execution.
    Nothing here is tuned by this run: the four candidate readings of 'top-20 composite' were
    checked against the memo's committed triple and this is the one that reproduces it (G6)."""
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def win_metrics(r: pd.Series) -> dict:
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def price_table() -> tuple[pd.DataFrame, str, str]:
    px = load_universe()
    start = px.index[260]
    books = {
        "STANDING 4b CAND (U56 top-20 composite, g0.75, W)": lambda p: top20_weights(p),
        "RULES v2 baseline (live)": rules_v2_weights,
        "RULES v1 (previous)": rules_v1_weights,
    }
    rows = []
    rets = {}
    for name, fn in books.items():
        res = backtest(px, fn(px), cost_bps=COST_BPS, freq="W")
        rets[name] = res["returns"].loc[start:]
    rets["SPY"] = px["SPY"].pct_change().fillna(0).loc[start:]
    for name, r in rets.items():
        h = len(r) // 2
        full, h1, h2 = win_metrics(r), win_metrics(r.iloc[:h]), win_metrics(r.iloc[h:])
        isw, oos = win_metrics(r.loc[:IS_END]), win_metrics(r.loc[OOS_START:])
        rows.append(dict(book=name, CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                         H1_Sharpe=h1["Sharpe"], H2_Sharpe=h2["Sharpe"],
                         IS_CAGR=isw["CAGR"], IS_Sharpe=isw["Sharpe"], IS_MaxDD=isw["MaxDD"],
                         OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"], OOS_MaxDD=oos["MaxDD"]))
    df = pd.DataFrame(rows).set_index("book")
    v2, spy = df.loc["RULES v2 baseline (live)"], df.loc["SPY"]
    g4 = (f"G4 PRICE: RULES v2 {v2.CAGR:.2%} / {v2.Sharpe:.4f} / {v2.MaxDD:.2%} vs committed "
          f"8.66% / 1.2056 / -12.05% (bars 1.00pp/0.060/2.00pp) — "
          f"{'PASS' if abs(v2.CAGR-0.0866)<=0.01 and abs(v2.Sharpe-1.2056)<=0.06 and abs(v2.MaxDD+0.1205)<=0.02 else 'FAIL'}; "
          f"SPY {spy.CAGR:.2%} / {spy.Sharpe:.4f} / {spy.MaxDD:.2%} vs 15.23% / 0.8890 / -33.72% — "
          f"{'PASS' if abs(spy.CAGR-0.1523)<=0.01 and abs(spy.Sharpe-0.8890)<=0.06 and abs(spy.MaxDD+0.3372)<=0.02 else 'FAIL'}")
    cnd = df.loc["STANDING 4b CAND (U56 top-20 composite, g0.75, W)"]
    g6 = (f"G6 STANDING CANDIDATE: {cnd.CAGR:.2%} / {cnd.Sharpe:.4f} / {cnd.MaxDD:.2%}, halves "
          f"{cnd.H1_Sharpe:.3f}/{cnd.H2_Sharpe:.3f}, OOS {cnd.OOS_Sharpe:.4f} vs memo "
          f"2026-09-07_u56-top20-g075-4b_C_MEMO.md's 12.79% / 1.064 / -18.31%, 1.068/1.066, OOS 1.131 "
          f"(bars 1.00pp/0.060/2.00pp) — "
          f"{'PASS' if abs(cnd.CAGR-0.1279)<=0.01 and abs(cnd.Sharpe-1.064)<=0.06 and abs(cnd.MaxDD+0.1831)<=0.02 else 'FAIL'}")
    g4 = g4 + "\n" + g6
    # KEEP paths for the standing candidate, read literally
    c = df.loc["STANDING 4b CAND (U56 top-20 composite, g0.75, W)"]
    p4a = (c.Sharpe > v2.Sharpe and c.H1_Sharpe > v2.H1_Sharpe and c.H2_Sharpe > v2.H2_Sharpe
           and c.MaxDD >= v2.MaxDD)
    p4b = (c.H1_Sharpe > spy.H1_Sharpe and c.H2_Sharpe > spy.H2_Sharpe and c.OOS_Sharpe > spy.OOS_Sharpe
           and c.MaxDD >= 0.6 * spy.MaxDD and c.CAGR >= 0.7 * spy.CAGR)
    verdict = (f"4a {'PASS' if p4a else 'FAIL'} (H1 {c.H1_Sharpe:.4f} vs {v2.H1_Sharpe:.4f}, "
               f"H2 {c.H2_Sharpe:.4f} vs {v2.H2_Sharpe:.4f}, MaxDD {c.MaxDD:.2%} vs {v2.MaxDD:.2%}); "
               f"4b {'PASS' if p4b else 'FAIL'} (H1 {c.H1_Sharpe:.4f} vs SPY {spy.H1_Sharpe:.4f}, "
               f"H2 {c.H2_Sharpe:.4f} vs {spy.H2_Sharpe:.4f}, OOS {c.OOS_Sharpe:.4f} vs {spy.OOS_Sharpe:.4f}, "
               f"MaxDD {c.MaxDD:.2%} vs cap {0.6*spy.MaxDD:.2%}, CAGR {c.CAGR:.2%} vs floor {0.7*spy.CAGR:.2%})")
    return df, g4, verdict


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=" * 100)
    say("Idea 843 (lane C, 2026-09-12) — do the record's committed 'k of n' COUNTS agree with their own TABLES?")
    say("=" * 100)

    all_files = sorted(p.name for p in BT.iterdir() if p.is_file())
    doc_names = [f for f in all_files if f.endswith(".result.md") or f.endswith("_MEMO.md") or f.endswith(".memo.md")]
    docs = [BT / f for f in doc_names]
    say(f"\nCorpus: {len(docs)} committed documents ({sum(f.endswith('.result.md') for f in doc_names)} .result.md, "
        f"{len(docs) - sum(f.endswith('.result.md') for f in doc_names)} memos), "
        f"{sum(f.endswith(('.csv', '.csv.gz')) for f in all_files)} committed CSVs.")

    say("\n--- GATES ---")
    say(gate_anchor())
    say(gate_determinism(docs[:120]))
    say(gate_unit())

    # ---------------------------------------------------------------- extract + judge every claim
    claims: list[dict] = []
    for i, d in enumerate(docs):
        cl = extract_claims(d)
        if not cl:
            continue
        tables = md_tables(d) + sibling_csvs(stem_of(d.name), all_files)
        for c in cl:
            c["date"] = d.name[:10]
            c["n_sources"] = len(tables)
            for det in ("D1", "D2", "D3"):
                j = judge(c, tables, det)
                c[f"{det}_universes"] = j["universes"]
                c[f"{det}_nA"] = j["nA"]
                c[f"{det}_rederivable"] = j["rederivable"]
                c[f"{det}_agree"] = j["agree"]
                c[f"{det}_nearest"] = j["nearest"]
                c[f"{det}_how"] = j["how"]
            claims.append(c)
        if (i + 1) % 100 == 0:
            say(f"  ... {i+1}/{len(docs)} documents, {len(claims)} claims, {time.time()-t0:.0f}s")
        _CSV_CACHE.clear()

    C = pd.DataFrame(claims)
    C.to_csv(f"{STEM}.claims.csv", index=False)          # written before any statistic is computed
    say(f"\nExtracted {len(C)} claims from {C.file.nunique()} documents in {time.time()-t0:.0f}s.")
    say(f"CSV sources: {SKIPPED['read']} read, {SKIPPED['big']} skipped (>{MAX_CSV_BYTES/1e6:.0f}MB), "
        f"{SKIPPED['rows']} skipped (>{MAX_ROWS} rows), {SKIPPED['err']} unreadable.")

    C["S1"] = C.noun.isin(S1_NOUNS)
    C["S2"] = C.S1 | C.noun.isin(S2_EXTRA)
    C["S3"] = True
    say("\nNoun census (top 15): " + ", ".join(f"{k}:{v}" for k, v in C.noun.value_counts().head(15).items()))

    # ------------------------------------------------------------------------------ the 3x3 grid
    grid = []
    for samp in ("S1", "S2", "S3"):
        sub_all = C[C[samp]]
        for det in ("D1", "D2", "D3"):
            red = sub_all[sub_all[f"{det}_rederivable"]]
            agree = int(red[f"{det}_agree"].sum())
            dis = len(red) - agree
            floor = float((red[f"{det}_nA"] / (red["n"] + 1)).clip(upper=1.0).mean()) if len(red) else np.nan
            grid.append(dict(sample=samp, detector=det, claims=len(sub_all), rederivable=len(red),
                             not_rederivable=len(sub_all) - len(red),
                             agree=agree, disagree=dis,
                             disagree_rate=dis / len(red) if len(red) else np.nan,
                             agree_rate=agree / len(red) if len(red) else np.nan,
                             chance_floor=floor,
                             excess=(agree / len(red) - floor) if len(red) else np.nan))
    G = pd.DataFrame(grid)
    say("\n--- THE 3x3 GRID (ALL POINTS REPORTED) ---")
    say(G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    HD, HS = "D2", "S1"
    hd = G[(G.detector == HD) & (G["sample"] == HS)].iloc[0]
    say(f"\nHEADLINE CELL ({HD}, {HS}): {hd.claims} books/arms claims, {hd.rederivable} re-derivable, "
        f"{hd.disagree} DISAGREE ({hd.disagree_rate:.4f}), agree {hd.agree_rate:.4f} against a chance floor "
        f"{hd.chance_floor:.4f} (excess {hd.excess:+.4f}).")

    # ------------------------------------------------------------------------- disagreement list
    red = C[C.S1 & C[f"{HD}_rederivable"]]
    D = red[~red[f"{HD}_agree"]][["file", "date", "claim", "k", "n", "noun", f"{HD}_universes",
                                  f"{HD}_nA", f"{HD}_nearest", "context"]].copy()
    D = D.rename(columns={f"{HD}_universes": "universes", f"{HD}_nA": "n_achievable", f"{HD}_nearest": "nearest"})
    D["gap"] = D["nearest"] - D["k"]
    D = D.sort_values(["n", "gap"], key=lambda s: s.abs() if s.name == "gap" else s, ascending=[False, True])
    say(f"\n--- DISAGREEMENTS AT THE HEADLINE CELL ({len(D)} of {len(red)} re-derivable books/arms claims) ---")
    for _, r in D.head(20).iterrows():
        say(f"  {r.file[:72]:72s} '{r.claim}'  nearest {r.nearest} (gap {r.gap:+.0f}), {r.n_achievable} counts reachable")

    # ---------------------------------------------------------------- H_ANCHOR (idea 839's own file)
    anch = C[C.file.str.contains("NEGATIVE-NEXT-WINDOW-sign") & (C.n == 11)]
    say("\n--- H_ANCHOR: idea 839's own file, claims with n = 11 ---")
    if len(anch):
        for _, r in anch.iterrows():
            say(f"  '{r.claim}' -> D2 rederivable {r.D2_rederivable}, agree {r.D2_agree}, nearest {r.D2_nearest}, via '{r.D2_how}'")
    else:
        say("  none extracted")

    # ------------------------------------------------------- corpus walk-forward (rule-8 analogue)
    say("\n--- CORPUS WALK-FORWARD (rule-8 analogue: choose the cell on files <= "
        f"{SPLIT_IS}, read the rest once) ---")
    isC, oosC = C[C.date <= SPLIT_IS], C[C.date > SPLIT_IS]
    say(f"G5 PARTITION: IS {isC.file.nunique()} files / {len(isC)} claims, OOS {oosC.file.nunique()} files / "
        f"{len(oosC)} claims, union {len(isC)+len(oosC)} == total {len(C)} — "
        f"{'PASS' if len(isC)+len(oosC) == len(C) and set(isC.file) & set(oosC.file) == set() else 'FAIL'}")
    wf = []
    for samp in ("S1", "S2", "S3"):
        for det in ("D1", "D2", "D3"):
            row = dict(sample=samp, detector=det)
            for tag, sub in (("IS", isC), ("OOS", oosC)):
                s = sub[sub[samp] & sub[f"{det}_rederivable"]]
                row[f"{tag}_n"] = len(s)
                row[f"{tag}_disagree_rate"] = float((~s[f"{det}_agree"]).mean()) if len(s) else np.nan
                row[f"{tag}_chance_floor"] = float((s[f"{det}_nA"] / (s["n"] + 1)).clip(upper=1.0).mean()) if len(s) else np.nan
            wf.append(row)
    W = pd.DataFrame(wf)
    W["drift"] = W.OOS_disagree_rate - W.IS_disagree_rate
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    pick = W.loc[W.IS_disagree_rate.idxmax()] if W.IS_n.gt(0).any() else None
    if pick is not None:
        say(f"\nRule-8 pick (cell with the highest IS disagreement rate, read OOS once): "
            f"({pick.detector}, {pick['sample']}) IS {pick.IS_disagree_rate:.4f} (n={int(pick.IS_n)}) -> "
            f"OOS {pick.OOS_disagree_rate:.4f} (n={int(pick.OOS_n)}), drift {pick.drift:+.4f}")

    # ---------------------------------------------------------------------------- price rule 8
    say("\n--- PROTOCOL rule-8 PRICE TABLE (this census proposes no book; reported as the protocol requires) ---")
    P, g4, keepverdict = price_table()
    say(g4)
    say(P.to_string(float_format=lambda x: f"{x:.4f}"))
    say("KEEP paths for the standing candidate: " + keepverdict)

    # ------------------------------------------------------------------------------------ write
    C.to_csv(f"{STEM}.claims.csv", index=False)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    D.to_csv(f"{STEM}.disagree.csv", index=False)
    wfout = pd.concat([W.assign(block="corpus_walk_forward"),
                       P.reset_index().assign(block="price_rule8")], ignore_index=True)
    wfout.to_csv(f"{STEM}.wf.csv", index=False)
    say(f"\nWrote {Path(STEM).name}.claims.csv / .grid.csv / .disagree.csv / .wf.csv")
    say(f"Total runtime {time.time()-t0:.0f}s")
    Path(f"{STEM}.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
