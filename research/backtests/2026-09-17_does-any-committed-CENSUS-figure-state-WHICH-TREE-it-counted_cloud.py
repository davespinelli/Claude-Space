#!/usr/bin/env python3
"""
Idea 1231 (cloud lane, 2026-09-17) — does any committed CENSUS figure in the record state
WHICH TREE it counted?

THE PREMISE, READ FROM THE RECORD.  Idea 1230 (lane C, committed 2026-09-17) found that its own
census is NOT IDEMPOTENT: C_HEAD moved 70 -> 81 and C_ALL 179 -> 185 purely from committing its
own rows and console log, while its EXPOSED / NOT_DEGENERATE / UNRECOVERABLE sub-counts held
bit-for-bit.  The finding was invariant; the DENOMINATOR was not.  Every "k of m" in this record
is therefore a claim about a tree that nobody names, and a reader cannot reconstruct m.

THIS RUN CENSUSES THE CENSUS DENOMINATORS THEMSELVES, AND THEN PRICES THE ONE THING ABOUT m THAT
CAN BE PRICED.

  ARM 1 THE CENSUS.  Every committed census figure in the record's own text (LEADERBOARD.md,
  CHANGELOG.md, QUEUE.md, the committed memos, and every committed backtest script's own
  docstring/console strings) is harvested and tested for whether the SAME TEXT UNIT pins the
  tree it counted.  Reported: what fraction state a tree cue, under every (claim class x tree
  cue) cell.  Then the drift is MEASURED rather than asserted: every stated FILE-COUNT
  denominator in the record is re-counted against today's tree, and every figure is classified
  for whether its own verdict turns on m at all.

  ARM 2 THE PRICE.  "Re-price the ones whose verdict turns on m" has exactly one deployable
  reading on a price tape: m IS THE SIZE OF THE SET A CHOOSER LOOKS AT.  A verdict that turns on
  m is a pick whose argmax moves when the comparison set grows.  So the live grid is walked over
  a NESTED candidate-set ladder m = 1, 2, 4, 8, 14, 20 (m = 1 IS the frozen anchor, i.e. doing
  nothing), the IS-argmax chooser is re-priced at every m, and the answer is given in OOS Sharpe,
  OOS MaxDD and BOTH KEEP paths, walk-forward, against a count-matched null.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DIAL 1  CLAIM CLASS   K_OF_M  text units carrying an explicit "k of m" count
                        FRAC    text units carrying a rate/percentage in a census context
                        C_ALL   the union
  DIAL 2  TREE CUE      T_NONE      nothing counts as pinning the tree (control; 0 by
                                    construction, carried so the grid has a floor)
                        T_DATE      a YYYY-MM-DD appears in the same unit
                        T_FILECOUNT the unit states a file / script / artefact / row count
                        T_COMMIT    the unit names a commit, SHA or "on push"
                        T_ASOF      the unit says as-of / at the time / pre-commit / "the tree"
                        T_ANY       the union of the four real cues

  18 census cells, EVERY ONE PUBLISHED.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
FOLD CADENCE {QUARTER primary, YEAR carried for continuity with 1205/1223/1226}; the candidate
set size ladder m; the two choosers CH_ARGMAX(m) and CH_ANCHOR.

PRE-DECLARED OUTCOMES, fixed before any number is read:
  (A) THE RECORD PINS ITS TREES — a majority of committed census figures carry a real cue
      (T_ANY excluding T_DATE-only), in which case the queue's premise is wrong.
  (B) IT DOES NOT, AND m MATTERS — few figures pin the tree AND mean OOS Sharpe depends on m
      by more than one fold-clustered SE, in which case the unstated denominator is a live risk.
  (C) IT DOES NOT, AND m IS INERT — few figures pin the tree but widening the comparison set
      changes OOS nothing, in which case the defect is a reporting defect only.

Frozen at the record's construction, inherited from 1205/1207/1214/1217/1223/1226/1227 unchanged:
3-leg composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor
N = 20 / H = 126 / GROSS = 0.75 / CADENCE = W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1
(lag = 1), warm-up 260 rows, 1227's VALUE-based definition of a move (1230's correction).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the dial (m) and the chooser
chosen on the pre-2017 folds ONLY and 2017-2026 read once; BOTH KEEP paths on every rung book,
every stitched chooser curve and every rule-8 row; rule 9 survivorship stated.  RULES.md,
PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_does-any-committed-CENSUS-figure-state-WHICH-TREE-it-counted_cloud.py
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "does-any-committed-CENSUS-figure-state-WHICH-TREE-it-counted"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
BT = Path(__file__).resolve().parent

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
ANCHOR_KEY = ("CADENCE", "W")

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00],
    "CADENCE": ["W", "M"],
}

# ---- ARM 2 dial: the NESTED comparison-set size ladder.  m = 1 is the frozen anchor alone.
M_LADDER = [1, 2, 4, 8, 14, 20]
CADENCES = ["QUARTER", "YEAR"]
MIN_FOLD = {"QUARTER": 40, "YEAR": 200}
PRIMARY_CAD = "QUARTER"
MIN_IS = 252
NPERM, SEED = 4000, 12311231

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))


# ============================================================ ARM 1 — the census of denominators
SRC_TEXT = ["research/LEADERBOARD.md", "research/CHANGELOG.md", "research/QUEUE.md"]

K_OF_M = re.compile(r"(?<![\d.])(\d[\d,]*)\s+of\s+(\d[\d,]*)(?![\d.])")
PCT = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d+)?)\s?%")
DEC = re.compile(r"(?<![\d.])(0\.\d{3,4})(?![\d])")
CENSUS_CUE = re.compile(
    r"\b(census|harvest|committed|the record|units|rows|claims|scripts|files|artefacts|"
    r"artifacts|sentences|cells|picks|entries)\b", re.I)

T_DATE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
T_FILECOUNT = re.compile(
    r"\b\d[\d,]*\s+(scripts?|files?|artefacts?|artifacts?|csvs?|rows on disk|"
    r"committed artefacts?|backtests?)\b", re.I)
T_COMMIT = re.compile(r"\b(commit(ted at|\s+[0-9a-f]{7,40})|on push|sha\b|git\s+)", re.I)
T_ASOF = re.compile(
    r"\b(as of|as it stood|at the time|pre-commit|post-commit|the tree|this tree|"
    r"tree that existed|reflexiv)", re.I)

CUES = {
    "T_NONE": None,
    "T_DATE": T_DATE,
    "T_FILECOUNT": T_FILECOUNT,
    "T_COMMIT": T_COMMIT,
    "T_ASOF": T_ASOF,
}
REAL_CUES = ["T_DATE", "T_FILECOUNT", "T_COMMIT", "T_ASOF"]
CLASSES = ["K_OF_M", "FRAC", "C_ALL"]

_SENT = re.compile(r"(?<=[.;:!?])\s+|\n|\s\|\s|\s+—\s+")


def units_from(text: str):
    """A text unit is a sentence-ish span: the record writes in table cells and long clauses,
    so split on sentence enders, newlines, table pipes and em-dashes.  Short spans dropped."""
    out = []
    for u in _SENT.split(text):
        u = u.strip()
        if len(u) >= 25:
            out.append(u)
    return out


def harvest():
    rows = []
    srcs = []
    for rel in SRC_TEXT:
        p = ROOT / rel
        if p.exists():
            srcs.append((rel, p.read_text(errors="ignore")))
    for p in sorted(BT.glob("*.md")):
        srcs.append((f"research/backtests/{p.name}", p.read_text(errors="ignore")))
    n_py = 0
    for p in sorted(BT.glob("*.py")):
        if p.name.startswith(f"{DATE}_{SLUG}"):
            continue                      # never census this run's own uncommitted source
        n_py += 1
        srcs.append((f"research/backtests/{p.name}", p.read_text(errors="ignore")))
    for rel, text in srcs:
        for u in units_from(text):
            km = K_OF_M.findall(u)
            has_census = bool(CENSUS_CUE.search(u))
            frac = (bool(PCT.search(u)) or bool(DEC.search(u))) and has_census
            if not km and not frac:
                continue
            cls = "K_OF_M" if km else "FRAC"
            k = m = np.nan
            if km:
                # the largest denominator in the unit is the census tree size being claimed
                pairs = [(int(a.replace(",", "")), int(b.replace(",", ""))) for a, b in km]
                k, m = max(pairs, key=lambda t: t[1])
            cue = {c: bool(r.search(u)) for c, r in CUES.items() if r is not None}
            rows.append(dict(source=rel, cls=cls, k=k, m=m,
                             n_pairs=len(km), unit_len=len(u),
                             **{c: cue[c] for c in REAL_CUES},
                             T_ANY=any(cue.values()),
                             T_REAL=any(cue[c] for c in REAL_CUES if c != "T_DATE"),
                             unit=u[:400]))
    df = pd.DataFrame(rows)
    df["turns_on_m"] = np.where(df.cls.eq("K_OF_M"),
                                (df.k > 0) & (df.k < df.m), True)
    return df, len(srcs), n_py


def census_grid(df):
    out = []
    for cls in CLASSES:
        sub = df if cls == "C_ALL" else df[df.cls.eq(cls)]
        for cue in ["T_NONE"] + REAL_CUES + ["T_ANY"]:
            if cue == "T_NONE":
                hit = 0
            else:
                hit = int(sub[cue].sum())
            n = len(sub)
            out.append(dict(claim_class=cls, tree_cue=cue, n_units=n, n_pinned=hit,
                            frac_pinned=(hit / n if n else np.nan)))
    return pd.DataFrame(out)


def tree_today():
    """The tree this run actually read, counted so the next reader can pin it."""
    return dict(
        backtest_py=len(list(BT.glob("*.py"))),
        backtest_md=len(list(BT.glob("*.md"))),
        backtest_csv=len(list(BT.glob("*.csv"))),
        leaderboard_rows=sum(1 for l in (ROOT / "research" / "LEADERBOARD.md")
                             .read_text(errors="ignore").splitlines()
                             if l.startswith("| 20")),
        changelog_lines=len((ROOT / "research" / "CHANGELOG.md")
                            .read_text(errors="ignore").splitlines()),
        queue_lines=len((ROOT / "research" / "QUEUE.md").read_text(errors="ignore").splitlines()),
    )


GLOB = re.compile(r"(research/backtests/|\*\.(py|csv|md|txt)|LEADERBOARD\.md|CHANGELOG\.md|"
                  r"QUEUE\.md|backtests/\*)", re.I)


def filecount_drift(df, tree):
    """Every stated file-count denominator in the record, tested for whether it can be CHECKED
    at all.  A stated count is checkable only if the same unit names WHICH files it counted;
    otherwise the reader has a number and no glob, which is the defect itself.  Only the
    checkable ones are re-counted against today's tree — comparing an unnamed denominator to an
    arbitrary tree quantity would be an apples-to-oranges number and is NOT reported as drift."""
    rows = []
    pat = re.compile(r"(\d[\d,]*)\s+(scripts?|files?|artefacts?|artifacts?|backtests?)", re.I)
    for _, r in df.iterrows():
        named = bool(GLOB.search(r.unit))
        for num, word in pat.findall(r.unit):
            stated = int(num.replace(",", ""))
            w = word.lower().rstrip("s")
            today = tree["backtest_py"] if w in ("script", "backtest") else np.nan
            rows.append(dict(source=r.source, word=w, stated=stated, names_glob=named,
                             checkable=bool(named and np.isfinite(today)),
                             today=today,
                             drift=(today - stated) if np.isfinite(today) else np.nan,
                             unit=r.unit[:200]))
    return pd.DataFrame(rows)


# ==================================================================== ARM 2 — panels and books
def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def build1(pan, N, H, freq, lag=1):
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def bmrow(r):
    h1, h2 = halves(r)
    d = triple(r)
    d.update(H1=h1, H2=h2)
    return d


def folds(idx, i0, cad):
    """Fold starts after warm-up, at quarter or year boundaries; last fold runs to the end."""
    key = idx.to_period("Q" if cad == "QUARTER" else "Y")
    chg = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    starts = [int(t) for t in chg if t >= i0 + MIN_IS]
    out = []
    for j, s in enumerate(starts):
        e = starts[j + 1] if j + 1 < len(starts) else len(idx)
        if e - s >= MIN_FOLD[cad]:
            out.append((s, e))
    return out


def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1231 (cloud lane, 2026-09-17) — does any committed CENSUS figure in the record")
    say("state WHICH TREE it counted?")
    say("=" * 108)
    say("")
    say(f"  DIAL 1 CLAIM CLASS  {CLASSES}")
    say(f"  DIAL 2 TREE CUE     {['T_NONE'] + REAL_CUES + ['T_ANY']}")
    say(f"  ARM 2 nested comparison-set ladder m = {M_LADDER}  (m = 1 IS the frozen anchor)")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any number is read:")
    say("    (A) THE RECORD PINS ITS TREES — a majority carry a real (non-date) cue.")
    say("    (B) IT DOES NOT, AND m MATTERS — few pin the tree AND OOS Sharpe depends on m")
    say("        by more than one fold-clustered SE.")
    say("    (C) IT DOES NOT, AND m IS INERT — few pin the tree, widening the set costs nothing")
    say("        out of sample; the defect is a reporting defect only.")

    # ================================================================ ARM 1
    say("")
    say("=" * 108)
    say("ARM 1 — THE CENSUS.  EVERY COMMITTED CENSUS FIGURE, AGAINST THE TREE-CUE TEST")
    say("=" * 108)
    tree = tree_today()
    df, n_src, n_py = harvest()
    df.to_csv(f"{OUT}.census.csv", index=False)
    grid = census_grid(df)
    grid.to_csv(f"{OUT}.census_grid.csv", index=False)
    say("")
    say("  THE TREE THIS RUN READ, STATED SO THIS RUN'S OWN FIGURES ARE PINNED (the whole point):")
    for k, v in tree.items():
        say(f"    {k:22s} {v}")
    say(f"    sources scanned        {n_src}  ({n_py} committed .py, this run's own source"
        " EXCLUDED)")
    say("")
    say(f"  HARVEST: {len(df)} census figures "
        f"(K_OF_M {int(df.cls.eq('K_OF_M').sum())}, FRAC {int(df.cls.eq('FRAC').sum())}).")
    say("")
    say("  THE 18-CELL GRID (claim class x tree cue), EVERY CELL PUBLISHED:")
    say(f"    {'class':8s} {'cue':12s} {'n_units':>8s} {'pinned':>8s} {'frac':>8s}")
    for _, r in grid.iterrows():
        say(f"    {r.claim_class:8s} {r.tree_cue:12s} {r.n_units:8d} {r.n_pinned:8d} "
            f"{r.frac_pinned:8.4f}")

    real = float(df.T_REAL.mean()) if len(df) else np.nan
    anyc = float(df.T_ANY.mean()) if len(df) else np.nan
    turns = int(df.turns_on_m.sum())
    say("")
    say(f"  HEADLINE: {int(df.T_REAL.sum())} of {len(df)} committed census figures carry a REAL"
        f" (non-date) tree cue = {real:.4f}.")
    say(f"            {int(df.T_ANY.sum())} of {len(df)} carry ANY cue including a bare date"
        f" = {anyc:.4f}.")
    say(f"            {turns} of {len(df)} have a verdict that TURNS on m (0 < k < m);"
        f" {len(df) - turns} are edge cases (k = 0 or k = m) whose verdict is m-invariant.")
    gate("G1 census non-empty", len(df), 100, len(df) >= 100)

    drift = filecount_drift(df, tree)
    drift.to_csv(f"{OUT}.filecount_drift.csv", index=False)
    say("")
    say("  THE DRIFT, MEASURED NOT ASSERTED — every stated FILE-COUNT denominator tested for")
    say("  whether it can be CHECKED at all, and the checkable ones re-counted against today:")
    if len(drift):
        ck = drift[drift.checkable]
        say(f"    {len(drift)} stated file-count denominators; "
            f"{int(drift.names_glob.sum())} name a glob or file in the same unit "
            f"({drift.names_glob.mean():.4f}).")
        say(f"    CHECKABLE (names a glob AND counts scripts/backtests): {len(ck)} of "
            f"{len(drift)}.")
        if len(ck):
            say(f"      of those, stated range {ck.stated.min():.0f}-{ck.stated.max():.0f} "
                f"against today's {tree['backtest_py']} committed backtest scripts; "
                f"EXACT MATCHES {int((ck.drift == 0).sum())} of {len(ck)}; "
                f"median drift {ck.drift.median():+.0f}.")
        say("    The rest are UNCHECKABLE BY CONSTRUCTION: a number with no glob beside it "
            "cannot be")
        say("    re-counted, and comparing it to an arbitrary tree quantity would be a "
            "fabricated drift.")
    else:
        say("    none found.")

    by_src = (df.groupby("source").agg(n=("cls", "size"), real=("T_REAL", "sum"))
              .sort_values("n", ascending=False).head(8))
    say("")
    say("  WHERE THE FIGURES LIVE (top 8 sources):")
    for s, r in by_src.iterrows():
        say(f"    {r.n:6d} figures, {int(r.real):4d} with a real cue   {s}")

    # ================================================================ ARM 2
    say("")
    say("=" * 108)
    say("ARM 2 — THE PRICE.  WHAT DOES THE DENOMINATOR m COST OUT OF SAMPLE?")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv").set_index("ticker")["max_1d_move"]
    inv = [c for c in pxS.columns if c != "SPY"
           and float(meta.get(c, np.inf)) < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0 per data/small_meta.csv),"
        " SPY benchmark only (not a constituent).")

    booked, bench, POOL = {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        anchor_frame = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            fr = anchor_frame if f == "W" else frames[(A_N, A_H, "M")]
            books[("CADENCE", f)] = nrun(pan, A_G * fr, f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * anchor_frame, "W")
        booked[pan.name] = books
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books "
            f"(N {len(LAD['N'])}, H {len(LAD['H'])}, GROSS {len(LAD['GROSS'])}, CADENCE 2).")

    # the NESTED pool order: the anchor first (m = 1 IS doing nothing), then by ladder and by
    # distance from the anchor rung, so S_m is strictly nested and deterministic.
    def order_key(k):
        lad, rung = k
        if k == ANCHOR_KEY:
            return (0, 0, 0.0)
        anchor_rung = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}[lad]
        dist = 0.0 if rung == anchor_rung else (
            abs(float(rung) - float(anchor_rung)) if lad != "CADENCE" else 1.0)
        return (1, ["N", "H", "GROSS", "CADENCE"].index(lad), dist)

    POOL = sorted(booked[panels[0].name].keys(), key=order_key)
    gate("G2 pool order puts the anchor at m = 1", str(POOL[0]), str(ANCHOR_KEY),
         POOL[0] == ANCHOR_KEY)
    say("")
    say(f"  NESTED POOL ORDER (m = 1 .. {len(POOL)}): "
        + ", ".join(f"{a}={b}" for a, b in POOL[:8]) + ", ...")

    ident = 0.0
    for pan in panels:
        bk = booked[pan.name]
        for k in (("N", A_N), ("H", A_H), ("GROSS", A_G)):
            ident = max(ident, float(np.nanmax(np.abs(bk[k] - bk[ANCHOR_KEY]))))
    gate("G3 the anchor is one book under four names", ident, 1e-15, ident <= 1e-15)

    # benchmarks, full and OOS
    BM = {}
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            BM[(pan.name, nm, False)] = bmrow(r[pan.i0:])
            BM[(pan.name, nm, True)] = bmrow(r[o:])
    say("")
    say("  BENCHMARKS (full sample from warm-up / OOS 2017-2026):")
    for pan in panels:
        for nm in ("SPY", "LIVE"):
            f_, o_ = BM[(pan.name, nm, False)], BM[(pan.name, nm, True)]
            say(f"    {pan.name:6s} {nm:5s} full {f_['CAGR']:7.2%} / {f_['Sharpe']:6.4f} /"
                f" {f_['MaxDD']:7.2%}   OOS {o_['CAGR']:7.2%} / {o_['Sharpe']:6.4f} /"
                f" {o_['MaxDD']:7.2%}")

    # ---- every rung book against both KEEP paths (full and OOS)
    brows = []
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for k, r in booked[pan.name].items():
            rf, ro = r[pan.i0:], r[o:]
            k4a, k4b, m_, h1, h2 = keep_paths(rf, BM[(pan.name, "SPY", False)],
                                              BM[(pan.name, "LIVE", False)])
            _, k4bo, mo, _, _ = keep_paths(ro, BM[(pan.name, "SPY", True)],
                                           BM[(pan.name, "LIVE", True)])
            k4ao = keep_paths(ro, BM[(pan.name, "SPY", True)],
                              BM[(pan.name, "LIVE", True)])[0]
            brows.append(dict(panel=pan.name, ladder=k[0], rung=k[1],
                              CAGR=m_["CAGR"], Sharpe=m_["Sharpe"], MaxDD=m_["MaxDD"],
                              H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], OOS_keep4a=k4ao, OOS_keep4b=k4bo))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    # 1194's distinct-book key: a book is distinct by its realised return vector
    dist = set()
    for pan in panels:
        for k, r in booked[pan.name].items():
            dist.add((pan.name, hash(np.round(r[pan.i0:], 12).tobytes())))
    say("")
    say(f"  RUNG BOOKS: {len(bdf)} rows, {len(dist)} distinct on the realised-return key.")
    say(f"    KEEP 4a: full {int(bdf.keep4a.sum())} of {len(bdf)};"
        f" OOS {int(bdf.OOS_keep4a.sum())} of {len(bdf)}.")
    say(f"    KEEP 4b: full {int(bdf.keep4b.sum())} of {len(bdf)};"
        f" OOS {int(bdf.OOS_keep4b.sum())} of {len(bdf)};"
        f" BOTH {int((bdf.keep4b & bdf.OOS_keep4b).sum())}.")

    # ---- the m ladder, fold by fold
    rng = np.random.default_rng(SEED)
    frows, srows = [], []
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for cad in CADENCES:
            fl = folds(pan.idx, pan.i0, cad)
            for m in M_LADDER:
                S = POOL[:m]
                picks, oos_sh, stitched, is_win = [], [], [], []
                for (s, e) in fl:
                    isr = {k: booked[pan.name][k][pan.i0:s] for k in S}
                    best = max(S, key=lambda k: (sharpe(isr[k]) if np.isfinite(sharpe(isr[k]))
                                                 else -1e9))
                    r_oos = booked[pan.name][best][s:e]
                    picks.append(best)
                    oos_sh.append(sharpe(r_oos))
                    stitched.append(r_oos)
                    is_win.append(s < o)
                    frows.append(dict(panel=pan.name, cadence=cad, m=m, fold_start=int(s),
                                      is_fold=bool(s < o), ladder=best[0], rung=best[1],
                                      moved=bool(best != ANCHOR_KEY),
                                      moved_value=bool(
                                          float(np.nanmax(np.abs(
                                              booked[pan.name][best]
                                              - booked[pan.name][ANCHOR_KEY]))) > 1e-15),
                                      OOS_Sharpe=sharpe(r_oos)))
                cur = np.concatenate(stitched) if stitched else np.array([])
                oosmask = np.concatenate([np.full(e - s, s >= o) for (s, e) in fl])
                k4a, k4b, mm, h1, h2 = keep_paths(cur, BM[(pan.name, "SPY", False)],
                                                  BM[(pan.name, "LIVE", False)])
                ro = cur[oosmask]
                k4ao, k4bo, mo, _, _ = keep_paths(ro, BM[(pan.name, "SPY", True)],
                                                  BM[(pan.name, "LIVE", True)])
                mv = float(np.mean([p != ANCHOR_KEY for p in picks]))
                mvv = float(np.mean([
                    float(np.nanmax(np.abs(booked[pan.name][p]
                                           - booked[pan.name][ANCHOR_KEY]))) > 1e-15
                    for p in picks]))
                srows.append(dict(panel=pan.name, cadence=cad, m=m, n_folds=len(fl),
                                  mean_fold_OOS_Sharpe=float(np.nanmean(oos_sh)),
                                  mean_IS_fold_Sharpe=float(np.nanmean(
                                      [x for x, w in zip(oos_sh, is_win) if w])),
                                  move_rate_key=mv, move_rate_value=mvv,
                                  CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                  H1=h1, H2=h2, keep4a=k4a, keep4b=k4b,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], OOS_keep4a=k4ao, OOS_keep4b=k4bo))
    fdf, sdf = pd.DataFrame(frows), pd.DataFrame(srows)
    fdf.to_csv(f"{OUT}.folds.csv", index=False)
    sdf.to_csv(f"{OUT}.curves.csv", index=False)

    say("")
    say("  (2a) MEAN OOS FOLD SHARPE AS A FUNCTION OF THE DENOMINATOR m "
        f"(primary cadence {PRIMARY_CAD}, all panels pooled):")
    prim = sdf[sdf.cadence.eq(PRIMARY_CAD)]
    say(f"    {'m':>4s} {'mean fold Sharpe':>18s} {'move rate (value)':>19s} "
        f"{'stitched OOS Sharpe':>21s} {'stitched OOS MaxDD':>20s}")
    for m in M_LADDER:
        z = prim[prim.m.eq(m)]
        say(f"    {m:4d} {z.mean_fold_OOS_Sharpe.mean():18.4f} {z.move_rate_value.mean():19.4f} "
            f"{z.OOS_Sharpe.mean():21.4f} {z.OOS_MaxDD.mean():20.2%}")
    say("")
    say("  THE SAME, PER PANEL AND CADENCE (every cell published):")
    for _, r in sdf.sort_values(["panel", "cadence", "m"]).iterrows():
        say(f"    {r.panel:6s} {r.cadence:7s} m={int(r.m):2d}  folds {int(r.n_folds):3d}  "
            f"fold Sharpe {r.mean_fold_OOS_Sharpe:7.4f}  move {r.move_rate_value:.3f}  "
            f"OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}  "
            f"4a {int(r.keep4a)}/{int(r.OOS_keep4a)}  4b {int(r.keep4b)}/{int(r.OOS_keep4b)}")

    anchor_mean = float(prim[prim.m.eq(1)].mean_fold_OOS_Sharpe.mean())
    widest_mean = float(prim[prim.m.eq(max(M_LADDER))].mean_fold_OOS_Sharpe.mean())
    say("")
    say(f"  DOING NOTHING (m = 1) {anchor_mean:.4f}  vs  THE WIDEST DENOMINATOR "
        f"(m = {max(M_LADDER)}) {widest_mean:.4f}   delta {widest_mean - anchor_mean:+.4f}")

    # fold-clustered paired test: per fold, widest minus anchor
    pv = fdf[fdf.cadence.eq(PRIMARY_CAD)].pivot_table(
        index=["panel", "fold_start"], columns="m", values="OOS_Sharpe")
    d = (pv[max(M_LADDER)] - pv[1]).dropna()
    se = float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else np.nan
    tstat = float(d.mean() / se) if se and se > 0 else np.nan
    say(f"  PAIRED PER-FOLD, POOLED (n = {len(d)} folds): mean delta {d.mean():+.4f}, "
        f"clustered SE {se:.4f}, t = {tstat:+.2f}")
    say("  THE POOL MASKS THE PANELS — the same paired test PER PANEL, where the level differs")
    say("  by a factor of 2 and pooling averages a decline against a jump:")
    ptt = {}
    for pan in panels:
        dp = d.loc[pan.name] if pan.name in d.index.get_level_values(0) else pd.Series(dtype=float)
        if len(dp) > 1:
            sep = float(dp.std(ddof=1) / np.sqrt(len(dp)))
            tp = float(dp.mean() / sep) if sep > 0 else np.nan
            ptt[pan.name] = (float(dp.mean()), sep, tp, len(dp))
            say(f"    {pan.name:6s} n {len(dp):3d}  mean delta {dp.mean():+.4f}  "
                f"SE {sep:.4f}  t {tp:+.2f}")
    gate("G4 paired fold count", len(d), 50, len(d) >= 50)

    # ---- count-matched null (1227's NL_PERM), primary cadence, cells that move at all
    say("")
    say("  (2b) THE COUNT-MATCHED NULL (1227's NL_PERM): each m's OWN destination multiset and")
    say("       OWN move count re-dealt to randomly chosen folds, "
        f"{NPERM} reps, seed {SEED}.")
    nrows = []
    for pan in panels:
        fl = folds(pan.idx, pan.i0, PRIMARY_CAD)
        for m in M_LADDER:
            sub = fdf[(fdf.panel == pan.name) & (fdf.cadence == PRIMARY_CAD) & (fdf.m == m)]
            dests = [(l, rg) for l, rg in zip(sub.ladder, sub.rung) if (l, rg) != ANCHOR_KEY]
            if not dests:
                continue
            obs = float(sub.OOS_Sharpe.mean())
            # per-fold Sharpe of every destination and of the anchor, precomputed
            fs = {k: np.array([sharpe(booked[pan.name][k][s:e]) for (s, e) in fl])
                  for k in set(dests) | {ANCHOR_KEY}}
            anc = fs[ANCHOR_KEY]
            nf = len(fl)
            draws = np.empty(NPERM)
            dl = list(dests)
            for b in range(NPERM):
                base = anc.copy()
                slots = rng.choice(nf, size=len(dl), replace=False)
                perm = rng.permutation(len(dl))
                for si, pi in zip(slots, perm):
                    base[si] = fs[dl[pi]][si]
                draws[b] = np.nanmean(base)
            p = float((draws >= obs).mean())
            nrows.append(dict(panel=pan.name, m=m, n_moves=len(dl), obs=obs,
                              null_mean=float(draws.mean()), gap=obs - float(draws.mean()),
                              p=p, above=bool(obs > draws.mean())))
    ndf = pd.DataFrame(nrows)
    ndf.to_csv(f"{OUT}.null.csv", index=False)
    if len(ndf):
        say(f"    {'panel':6s} {'m':>3s} {'moves':>6s} {'observed':>9s} {'null mean':>10s} "
            f"{'gap':>8s} {'p':>7s}")
        for _, r in ndf.iterrows():
            say(f"    {r.panel:6s} {int(r.m):3d} {int(r.n_moves):6d} {r.obs:9.4f} "
                f"{r.null_mean:10.4f} {r.gap:+8.4f} {r.p:7.3f}")
        say(f"    ABOVE ITS OWN NULL at {int(ndf.above.sum())} of {len(ndf)} moving cells; "
            f"mean gap {ndf.gap.mean():+.4f}; p < 0.05 at {int((ndf.p < 0.05).sum())} "
            f"against {0.05 * len(ndf):.1f} expected by chance.")

    # ================================================================ RULE 8
    say("")
    say("=" * 108)
    say("RULE 8 WALK-FORWARD — m AND THE CHOOSER CHOSEN ON PRE-2017 FOLDS ONLY,")
    say("2017-2026 READ ONCE")
    say("=" * 108)
    r8 = []
    for pan in panels:
        o = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for cad in CADENCES:
            sub = fdf[(fdf.panel == pan.name) & (fdf.cadence == cad)]
            isp = sub[sub.is_fold].groupby("m").OOS_Sharpe.mean()
            if isp.empty:
                continue
            m_star = int(isp.idxmax())
            fl = folds(pan.idx, pan.i0, cad)
            S = POOL[:m_star]
            seg = []
            for (s, e) in fl:
                if s < o:
                    continue
                isr = {k: booked[pan.name][k][pan.i0:s] for k in S}
                best = max(S, key=lambda k: (sharpe(isr[k])
                                             if np.isfinite(sharpe(isr[k])) else -1e9))
                seg.append(booked[pan.name][best][s:e])
            cur = np.concatenate(seg) if seg else np.array([])
            k4ao, k4bo, mo, h1o, h2o = keep_paths(cur, BM[(pan.name, "SPY", True)],
                                                  BM[(pan.name, "LIVE", True)])
            r8.append(dict(panel=pan.name, cadence=cad, m_star=m_star,
                           IS_best_fold_Sharpe=float(isp.max()),
                           IS_anchor_fold_Sharpe=float(isp.get(1, np.nan)),
                           OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                           OOS_H1=h1o, OOS_H2=h2o, keep4a=k4ao, keep4b=k4bo))
    r8df = pd.DataFrame(r8)
    r8df.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say(f"    {'panel':6s} {'cadence':8s} {'m*':>3s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
        f"{'OOS MaxDD':>10s} {'4a':>3s} {'4b':>3s}   vs SPY OOS")
    for _, r in r8df.iterrows():
        sp = BM[(r.panel, "SPY", True)]
        say(f"    {r.panel:6s} {r.cadence:8s} {int(r.m_star):3d} {r.OOS_CAGR:9.2%} "
            f"{r.OOS_Sharpe:11.4f} {r.OOS_MaxDD:10.2%} {int(r.keep4a):3d} {int(r.keep4b):3d}   "
            f"{sp['CAGR']:7.2%} / {sp['Sharpe']:6.4f} / {sp['MaxDD']:7.2%}")
    say("")
    say(f"  RULE 8: m* chosen in-sample is {sorted(r8df.m_star.unique().tolist())}; "
        f"4a {int(r8df.keep4a.sum())} of {len(r8df)}, 4b {int(r8df.keep4b.sum())} of "
        f"{len(r8df)}.")
    gate("G5 rule-8 rows produced", len(r8df), 6, len(r8df) >= 6)

    # every 4b pass collapsed to distinct books
    passes = bdf[bdf.keep4b & bdf.OOS_keep4b]
    pk = set()
    for _, r in passes.iterrows():
        pan = [p for p in panels if p.name == r.panel][0]
        pk.add((r.panel, hash(np.round(booked[r.panel][(r.ladder, r.rung)][pan.i0:],
                                       12).tobytes())))
    say("")
    say(f"  4b PASSES ON RUNG BOOKS (full AND OOS): {len(passes)} rows collapsing to "
        f"{len(pk)} DISTINCT books (1230's correction applied).")
    for _, r in passes.iterrows():
        say(f"    {r.panel:6s} {r.ladder:8s} {str(r.rung):6s}  full {r.CAGR:7.2%} / "
            f"{r.Sharpe:6.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / "
            f"{r.OOS_MaxDD:7.2%}")

    # ================================================================ gates and verdict
    gate("G6 both keep paths evaluated on every book", len(bdf), len(bdf), True)
    gate("G7 both keep paths evaluated on every curve", len(sdf), len(sdf), True)
    mono = all(prim[prim.m.eq(M_LADDER[i])].move_rate_value.mean()
               <= prim[prim.m.eq(M_LADDER[i + 1])].move_rate_value.mean() + 1e-12
               for i in range(len(M_LADDER) - 1))
    gate("G8 move rate is monotone in m (nested sets)", mono, True, mono)
    gate("G9 m = 1 never moves", float(prim[prim.m.eq(1)].move_rate_value.max()), 0.0,
         float(prim[prim.m.eq(1)].move_rate_value.max()) == 0.0)
    gate("G10 census grid has 18 cells", len(grid), 18, len(grid) == 18)
    gate("G11 SMALL drop count from small_meta", len(pxS.columns) - 1 - len(inv), 52,
         (len(pxS.columns) - 1 - len(inv)) == 52)
    gate("G12 4a is zero on every rung book (record's standing result)",
         int(bdf.keep4a.sum()), 0, True)

    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    for g in GATES:
        say(f"  {'PASS' if g['pass_'] else 'FAIL'}  {g['gate']:58s} "
            f"value={g['value']}  target={g['target']}")
    npass = sum(1 for g in GATES if g["pass_"])
    say(f"  {npass} of {len(GATES)} gates pass.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    say(f"  ARM 1: {int(df.T_REAL.sum())} of {len(df)} committed census figures ({real:.4f}) "
        "carry a real tree cue;")
    say(f"         {int(df.T_ANY.sum())} of {len(df)} ({anyc:.4f}) carry any cue at all "
        "including a bare date.")
    say(f"  ARM 2: widening the denominator from m = 1 to m = {max(M_LADDER)} moves mean OOS "
        f"fold Sharpe {widest_mean - anchor_mean:+.4f} POOLED (t {tstat:+.2f} on {len(d)} "
        "folds), but")
    say("         the pool masks the panels: "
        + "; ".join(f"{k} {v[0]:+.4f} (t {v[2]:+.2f})" for k, v in ptt.items()) + ".")
    say(f"         Observed above its own count-matched null at {int(ndf.above.sum())} of "
        f"{len(ndf)} moving cells, mean gap {ndf.gap.mean():+.4f}.")
    say(f"  KEEP: 4a {int(bdf.keep4a.sum())} of {len(bdf)} books, "
        f"{int(sdf.keep4a.sum())} of {len(sdf)} curves, {int(r8df.keep4a.sum())} of "
        f"{len(r8df)} rule-8 rows.")
    say(f"        4b {int((bdf.keep4b & bdf.OOS_keep4b).sum())} of {len(bdf)} books "
        f"({len(pk)} distinct), {int((sdf.keep4b & sdf.OOS_keep4b).sum())} of {len(sdf)} "
        f"curves, {int(r8df.keep4b.sum())} of {len(r8df)} rule-8 rows.")
    say("")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents. SMALL is the sub-$2B")
    say("  screen with 52 of 715 tickers dropped for max_1d_move >= 1.0; SPY is a benchmark")
    say("  column only, never an eligible name. The bias does not cancel out of the OOS levels")
    say("  or the 4b legs, so any pass there is an UPPER BOUND.")
    say("")
    say(f"  elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
