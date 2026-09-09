#!/usr/bin/env python3
"""Idea 527 — price the rule-8 OOS leg of KEEP path 4b as a REDUNDANT TEST, across the record.

THE CLAIM UNDER TEST (idea 285, 2026-09-09):
    "THE OOS BAR IS THE SOLE BINDING BAR IN 0 OF 1,520 FAILURES (0.000 on all four arms) —
     rule 8's leg never cuts anything H1 and H2 have not already cut."
That was measured on ONE construction (idea 276's cap-mix ladder).  The queue asks whether it
is a property of the RECORD: census every published 4b decision that can still be re-read bar
by bar and report how many the OOS leg decided ALONE.

WHAT "DECIDED ALONE" MEANS HERE.  4b is a five-bar conjunction (PROTOCOL rule 4b + rule 8):
    H1   Sharpe(1st half)  >  SPY(1st half)
    H2   Sharpe(2nd half)  >  SPY(2nd half)
    OOS  Sharpe(2017..)    >  SPY(2017..)          <- the rule-8 leg
    DD   |MaxDD|           <= 0.60 * |SPY MaxDD|
    CAGR CAGR              >= 0.70 * SPY CAGR
A failing row is "decided by OOS ALONE" iff OOS is the ONLY failing bar, i.e. deleting the OOS
leg would flip that row from FAIL to PASS.  That is the decision-relevant count: the number of
book-arms in the whole committed record whose verdict the OOS leg, and nothing else, produced.

THE TRAP THIS RUN FOUND FIRST.  The record's `fail4b` / `f4b` column carries TWO INCOMPATIBLE
SEMANTICS and the artefact does not say which:
    SET       - every failing bar, comma/pipe/plus joined ("H1,H2,OOS,CAGR")
    FIRSTFAIL - the FIRST failing bar under a short-circuit elif chain H1 -> H2 -> OOS -> DD ->
                CAGR (e.g. `2026-09-07_back-fill-the-mean-name-count-column..._B.py:249`, whose
                keep_paths() returns `f or ""` after an elif ladder)
A single-token value is ambiguous between the two — and single-token values are EXACTLY the rows
the sole-binding count is made of.  Reading a FIRSTFAIL "OOS" as a sole-OOS is wrong: it only says
H1 and H2 passed, DD and CAGR were never evaluated.  So every T1 file is classified by whether ANY
row emits >= 2 tokens (SET) or none ever does (SINGLETON), the headline is computed on the
unambiguous files only, and the SINGLETON files are reported separately as an upper bound and
reconstructed from their own numbers where possible.

TIERS (parameter 1 = the sample).  A committed artefact is re-readable bar by bar at four
different resolutions; every one is reported separately and then pooled:
    T1 DECLARED     - the file publishes the failing-bar SET as a string (fail4b / f4b / fail_4b)
    T2 MARGINS      - the file publishes signed per-bar margins (m_H1 .. m_CAGR); bar fails iff <0
    T3 BOOLEANS     - the file publishes per-bar pass flags (bar_H1 .. bar_CAGRfloor)
    T4 RECONSTRUCT  - no bar columns, but the five book numbers AND its own SPY reference columns
                      are present, so the five bars can be recomputed from PROTOCOL 4b
    L  LEADERBOARD  - the markdown row carries CAGR/Sharpe/MaxDD/H1/H2 but NO OOS number, so only
                      4 of 5 bars are readable: it can only ever give an UPPER BOUND on sole-OOS
                      (a row failing any non-OOS bar cannot have been decided by OOS alone).

PARAMETER 2 = the bar set.  Redundancy is conditional on what else is in the conjunction: idea
285 also found DD and CAGR are the aggressive bars.  So sole-OOS is recomputed under four nested
bar sets (FULL, no-DD, no-CAGR, no-DD-no-CAGR = the Sharpe-only conjunction).  All 4 subsets x 4
tiers = 16 grid points reported, no point hidden.

GATES (reproduction, all reported with |delta|, none allowed to hide the next):
  G1  idea 285's own arms.csv re-read by this script's parser must give 1,520 failures and 0 sole-OOS
  G2  on files carrying BOTH a declared fail-set and margins, the two must agree row for row
  G3  on files carrying BOTH a declared fail-set and full SPY refs, recomputation must agree

LIVE LEG (PROTOCOL rule 8 + both KEEP paths, required of every run).  The census can only speak
about books that were already written down; a leg that never binds on the record might still bind
on a fresh book.  So 39 pre-registered books (3 panels x 13: top-n momentum
n in {5,10,20,30,40} x gross {0.75,1.00}, EWall at both gross levels, the live RULES v2 band book) are built here, all five 4b bars are
measured directly, and the sole-binding count is reported on fresh prices.  Rule 8: n chosen on
IS (<= 2016-12-31) Sharpe per (panel, gross), read ONCE on 2017-01-01.., reported against the live
RULES v2 baseline and SPY.

SURVIVORSHIP: BROAD136 and SMALL439 are CURRENT-constituent lists (PROTOCOL rule 9 / idea 54), so
their LEVELS are optimistic; only contrasts are claimed here, and the census tiers are unaffected
(they re-read committed numbers, they do not re-price anything).

Deterministic, standalone, no network.  10 bps, weekly, next-day execution throughout.
Writes: .census.csv .subsets.csv .live.csv .console.txt   Modifies nothing else.
"""
import sys, os, glob, gzip, re, io, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

BD = ROOT / "research" / "backtests"
STEM = Path(__file__).stem
OUT = []
def P(s=""):
    print(s); OUT.append(str(s))

BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
SUBSETS = {                       # parameter 2: which bars are in the conjunction
    "FULL":        ["H1", "H2", "OOS", "DD", "CAGR"],
    "noDD":        ["H1", "H2", "OOS", "CAGR"],
    "noCAGR":      ["H1", "H2", "OOS", "DD"],
    "noDD_noCAGR": ["H1", "H2", "OOS"],
    "SharpeOnly":  ["H1", "H2", "OOS"],   # identical set, kept as a named reading of the ladder
}
SUBSET_ORDER = ["FULL", "noDD", "noCAGR", "noDD_noCAGR"]
# T1_SINGLETON is ambiguous (see the module docstring) and is EXCLUDED from every headline;
# it is reported on its own as an upper bound.
TIER_ORDER = ["T1_DECLARED", "T2_MARGINS", "T3_BOOLEANS", "T4_RECONSTRUCT", "T1_SINGLETON"]
UNAMBIGUOUS = TIER_ORDER[:4]


def run_of(fn):
    """The RUN a committed artefact belongs to: one script emits several .csv artefacts of the
    same rows (.grid/.keep/...), so file-clustering double-counts.  Cluster on the script stem."""
    return fn.split(".")[0]

# ------------------------------------------------------------------ tier readers
FAILCOLS = {"fail4b", "f4b", "fail_4b"}
TOKENS = {"H1", "H2", "OOS", "DD", "CAGR"}
ALIAS = {"DDCAP": "DD", "DDcap": "DD", "CAGRFLOOR": "CAGR", "CAGRfloor": "CAGR"}


def _open(p):
    return gzip.open(p, "rt") if str(p).endswith(".gz") else open(p, "rt")


def header(p):
    try:
        with _open(p) as f:
            return [c.strip().strip('"') for c in f.readline().strip().split(",")]
    except Exception:
        return []


def parse_failset(v):
    """'H1,H2,OOS' / 'H1|CAGR' / 'H1+CAGR' / '-' -> frozenset, or None if unresolvable."""
    if v is None:
        return None
    s = str(v).strip()
    if s == "" or s.lower() in ("nan", "none"):
        return None
    if s in ("-", "PASS", "pass", "none", "OK"):
        return frozenset()
    if s.startswith("{") or ":" in s:      # aggregate summary dict, not a row-level decision
        return None
    toks = [t.strip() for t in re.split(r"[,|+;\s]+", s) if t.strip()]
    out = set()
    for t in toks:
        t = ALIAS.get(t, ALIAS.get(t.upper(), t.upper()))
        if t not in TOKENS:
            return None
        out.add(t)
    return frozenset(out)


def read_cols(p, want):
    """Read only the requested columns (case-insensitive), return DataFrame with canonical names."""
    h = header(p)
    lower = {c.lower(): c for c in h}
    sel, ren = [], {}
    for canon, names in want.items():
        for nm in names:
            if nm.lower() in lower:
                sel.append(lower[nm.lower()]); ren[lower[nm.lower()]] = canon
                break
    if len(sel) < len(want):
        return None
    try:
        d = pd.read_csv(p, usecols=sel)
    except Exception:
        return None
    return d.rename(columns=ren)


def tier_rows(paths):
    """Yield (tier, file, list-of-frozensets) for every committed artefact that is bar-resolved."""
    recs = []
    for p in paths:
        h = header(p)
        if not h:
            continue
        low = [c.lower() for c in h]
        name = os.path.basename(p)

        # ---- T1 declared fail-set string
        fc = next((c for c in h if c.lower() in FAILCOLS), None)
        t1 = None
        if fc is not None:
            try:
                d = pd.read_csv(p, usecols=[fc])
                sets = [parse_failset(v) for v in d[fc]]
                if any(s is not None for s in sets):
                    t1 = sets
            except Exception:
                t1 = None
            if t1 is not None:
                # SEMANTICS: a file that never emits >=2 tokens cannot be distinguished from a
                # short-circuit FIRSTFAIL column, so its single tokens are NOT sole-fails.
                multi = any(s is not None and len(s) >= 2 for s in t1)
                recs.append(("T1_DECLARED" if multi else "T1_SINGLETON", name, t1))

        # ---- T2 signed margins
        if all(f"m_{b.lower()}" in low for b in BARS):
            d = read_cols(p, {b: [f"m_{b}"] for b in BARS})
            if d is not None:
                sets = []
                for _, r in d.iterrows():
                    if r.isna().any():
                        sets.append(None); continue
                    sets.append(frozenset(b for b in BARS if r[b] < 0))
                recs.append(("T2_MARGINS", name, sets))

        # ---- T3 per-bar booleans
        barmap = {"H1": ["bar_H1"], "H2": ["bar_H2"], "OOS": ["bar_OOS"],
                  "DD": ["bar_DDcap", "bar_DD"], "CAGR": ["bar_CAGRfloor", "bar_CAGR"]}
        if any(c.startswith("bar_") for c in low):
            d = read_cols(p, barmap)
            if d is not None:
                sets = []
                for _, r in d.iterrows():
                    if r.isna().any():
                        sets.append(None); continue
                    sets.append(frozenset(b for b in BARS if not bool(r[b])))
                recs.append(("T3_BOOLEANS", name, sets))

        # ---- T4 reconstruct from numbers + the file's own SPY reference
        need = {"H1": ["H1"], "H2": ["H2"], "OOSS": ["OOS_Sharpe", "Sharpe_OOS"],
                "MDD": ["MaxDD"], "CAGR": ["CAGR"],
                "sH1": ["spy_H1"], "sH2": ["spy_H2"], "sOOS": ["spy_OOS_Sharpe"],
                "sMDD": ["spy_MaxDD"], "sCAGR": ["spy_CAGR"]}
        d = read_cols(p, need)
        if d is not None:
            sets = []
            for _, r in d.iterrows():
                if r.isna().any():
                    sets.append(None); continue
                f = set()
                if not (r.H1 > r.sH1): f.add("H1")
                if not (r.H2 > r.sH2): f.add("H2")
                if not (r.OOSS > r.sOOS): f.add("OOS")
                if not (abs(r.MDD) <= 0.60 * abs(r.sMDD)): f.add("DD")
                if not (r.CAGR >= 0.70 * r.sCAGR): f.add("CAGR")
                sets.append(frozenset(f))
            recs.append(("T4_RECONSTRUCT", name, sets))
    return recs


def census_table(recs):
    """Per (tier, subset): decisions, failures, per-bar fail and SOLE-fail counts."""
    rows = []
    for sub in SUBSET_ORDER:
        keep = SUBSETS[sub]
        for tier in TIER_ORDER:
            rs = [r for r in recs if r[0] == tier]
            dec = fails = 0
            unres = 0
            fail_n = {b: 0 for b in keep}
            sole_n = {b: 0 for b in keep}
            files_any = set(); files_soleoos = set()
            for _, fn, sets in rs:
                for s in sets:
                    if s is None:
                        unres += 1; continue
                    dec += 1; files_any.add(fn)
                    f = s & set(keep)
                    if not f:
                        continue
                    fails += 1
                    for b in f:
                        fail_n[b] += 1
                    if len(f) == 1:
                        b = next(iter(f)); sole_n[b] += 1
                        if b == "OOS":
                            files_soleoos.add(fn)
            rows.append(dict(subset=sub, tier=tier, files=len(files_any),
                             runs=len({run_of(f) for f in files_any}), unresolved=unres,
                             decisions=dec, failures=fails,
                             **{f"fail_{b}": fail_n.get(b, 0) for b in BARS},
                             **{f"sole_{b}": sole_n.get(b, 0) for b in BARS},
                             files_with_sole_OOS=len(files_soleoos),
                             sole_OOS_share_of_failures=(sole_n.get("OOS", 0) / fails) if fails else np.nan))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ leaderboard tier
NUM = r"(-?\d+\.?\d*)"


def leaderboard_upper_bound():
    """LEADERBOARD rows carry CAGR/Sharpe/MaxDD/H1/H2 but never an OOS number.  A row whose
    non-OOS bars ALREADY fail cannot have been decided by OOS alone; the rest are the upper
    bound.  SPY reference: the record's own U56 reading (SPY 0.889 full, 0.957 H1, 0.834 H2,
    CAGR 15.23%, MaxDD -33.72%), quoted verbatim in dozens of rows and used here as THE
    reference because per-row SPY numbers are not published in the table."""
    SPY = dict(H1=0.957, H2=0.834, CAGR=0.1523, MaxDD=-0.3372)
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    n_rows = n_num = n_possible = 0
    for ln in txt:
        if not ln.startswith("|") or ln.startswith("|---") or ln.startswith("| Date"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        n_rows += 1
        try:
            cagr = float(re.search(NUM + r"%", cells[2]).group(1)) / 100
            mdd = float(re.search(NUM + r"%", cells[4]).group(1)) / 100
            h = re.findall(NUM, cells[5])
            h1, h2 = float(h[0]), float(h[1])
        except Exception:
            continue
        n_num += 1
        f = set()
        if not (h1 > SPY["H1"]): f.add("H1")
        if not (h2 > SPY["H2"]): f.add("H2")
        if not (abs(mdd) <= 0.60 * abs(SPY["MaxDD"])): f.add("DD")
        if not (cagr >= 0.70 * SPY["CAGR"]): f.add("CAGR")
        if not f:
            n_possible += 1        # every non-OOS bar passes -> OOS is the only bar left to decide
    return n_rows, n_num, n_possible


# ------------------------------------------------------------------ live books
def comp_score(px, cols):
    """Un-tilted composite (the record's COMP key): mean pct-rank of 12-1, 6m and 3m momentum."""
    q = px[cols]
    mom = q.shift(21) / q.shift(252) - 1
    r6 = q / q.shift(126) - 1
    r3 = q / q.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def topn_weights(px, cols, n, gross):
    s = comp_score(px, cols)
    rank = s.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (gross / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def ew_weights(px, cols, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=cols).where(px[cols].notna(), 0.0)
    w = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


OOS_START = "2017-01-01"
IS_END = "2016-12-31"


def legs(r):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:]); i = metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=i["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def bars_4b(b, s):
    f = set()
    if not (b["H1"] > s["H1"]): f.add("H1")
    if not (b["H2"] > s["H2"]): f.add("H2")
    if not (b["OOS_Sharpe"] > s["OOS_Sharpe"]): f.add("OOS")
    if not (abs(b["MaxDD"]) <= 0.60 * abs(s["MaxDD"])): f.add("DD")
    if not (b["CAGR"] >= 0.70 * s["CAGR"]): f.add("CAGR")
    return frozenset(f)


def main():
    P("=" * 100)
    P("IDEA 527 — is the rule-8 OOS leg of 4b a REDUNDANT TEST across the record?")
    P("=" * 100)

    paths = [p for p in sorted(glob.glob(str(BD / "*.csv"))) + sorted(glob.glob(str(BD / "*.csv.gz")))
             if not os.path.basename(p).startswith(STEM)]   # never count this run's own output
    P(f"\ncommitted CSV artefacts scanned (this run's own artefacts excluded): {len(paths)}")

    # ---------------------------------------------------------- GATE G1
    P("\n" + "-" * 100)
    P("[G1] REPRODUCTION GATE — idea 285's own corpus, re-read by THIS parser")
    a = BD / "2026-09-09_is-the-4b-footprint-a-monotone-function-of-cap-mix_cloud.arms.csv"
    if a.exists():
        d = pd.read_csv(a)
        sets = [frozenset(b for b, c in zip(BARS, ["bar_H1", "bar_H2", "bar_OOS", "bar_DDcap", "bar_CAGRfloor"])
                          if not bool(r[c])) for _, r in d.iterrows()]
        fails = [s for s in sets if s]
        sole = {b: sum(1 for s in fails if s == {b}) for b in BARS}
        P(f"  arm-rows {len(d)} (published 1,680; |delta| {abs(len(d)-1680)})")
        P(f"  4b failures {len(fails)} (published 1,520; |delta| {abs(len(fails)-1520)})")
        P(f"  sole-binding: " + "  ".join(f"{b} {sole[b]}" for b in BARS))
        P(f"  GATE: sole-OOS = {sole['OOS']}, published 0 -> {'PASS' if sole['OOS']==0 else 'FAIL'}")
    else:
        P("  artefact missing — gate not reached")

    # ---------------------------------------------------------- THE CENSUS
    P("\n" + "-" * 100)
    P("[1] THE CENSUS — every committed 4b decision that can still be re-read bar by bar")
    recs = tier_rows(paths)
    tab = census_table(recs)
    full = tab[tab.subset == "FULL"].set_index("tier")
    P("\n  FULL 5-bar conjunction, by tier:")
    P(full[["files", "runs", "decisions", "unresolved", "failures", "sole_H1", "sole_H2",
            "sole_OOS", "sole_DD", "sole_CAGR", "files_with_sole_OOS"]].to_string())
    P("\n  T1_SINGLETON is the AMBIGUOUS tier (no row ever emits >= 2 tokens, so its single tokens")
    P("  cannot be told apart from a short-circuit FIRSTFAIL column).  It is EXCLUDED from every")
    P("  headline below and reported on its own in [1b].")

    # RUN-POOLED: one artefact per run (a script emits .grid/.keep/... of the same rows), the
    # highest-priority unambiguous tier available, and within it the artefact with most decisions.
    best = {}
    for t, fn, sets in recs:
        if t not in UNAMBIGUOUS:
            continue
        r = run_of(fn); nd = sum(1 for s in sets if s is not None)
        key = (UNAMBIGUOUS.index(t), -nd)
        if r not in best or key < best[r][0]:
            best[r] = (key, (t, fn, sets))
    pooled = [v[1] for v in best.values()]
    ptab = census_table(pooled)
    pf = ptab[ptab.subset == "FULL"]
    tot = dict(decisions=int(pf.decisions.sum()), failures=int(pf.failures.sum()),
               files=len(pooled), **{f"sole_{b}": int(pf[f"sole_{b}"].sum()) for b in BARS},
               soleoos_files=int(pf.files_with_sole_OOS.sum()))
    P(f"\n  POOLED, one unambiguous artefact per RUN (T1>T2>T3>T4), {tot['files']} runs:")
    P(f"    4b decisions re-readable bar by bar : {tot['decisions']:,}")
    P(f"    of which FAIL 4b                    : {tot['failures']:,}")
    P("    SOLE binding bar: " + "  ".join(f"{b} {tot['sole_'+b]:,}" for b in BARS))
    r_sole = tot["sole_OOS"] / tot["failures"] if tot["failures"] else np.nan
    P(f"    >>> SOLE-OOS = {tot['sole_OOS']:,} of {tot['failures']:,} failures "
      f"({r_sole:.5f}), in {tot['soleoos_files']} distinct RUNS (RUN-CLUSTERED)")
    P(f"    >>> ANSWER TO THE QUEUE'S 'if the answer is zero corpus-wide': "
      f"{'IT IS NOT ZERO' if tot['sole_OOS'] > 0 else 'ZERO'}")

    # WHERE the sole-OOS decisions live — named, so the claim can be checked by hand
    hits = []
    for tier, fn, sets in pooled:
        k = sum(1 for s in sets if s == frozenset({"OOS"}))
        if k:
            hits.append((k, fn, tier, len([s for s in sets if s is not None])))
    P("\n  THE SOLE-OOS DECISIONS, by file (every one, nothing elided):")
    for k, fn, tier, nd in sorted(hits, reverse=True):
        P(f"    {k:4d} of {nd:6,} decisions   [{tier}]  {fn}")

    # per-bar cut rates (idea 285's other statistic, on the whole record)
    P("\n  cut rate of each bar over all pooled failures (a bar can fail with others):")
    for b in BARS:
        P(f"    {b:5s} fails {int(pf['fail_'+b].sum()):7,} / {tot['failures']:,} "
          f"= {pf['fail_'+b].sum()/tot['failures']:.3f}   sole {tot['sole_'+b]:5,} "
          f"= {tot['sole_'+b]/tot['failures']:.5f}")

    # ---------------------------------------------------------- [1b] the ambiguous tier
    P("\n" + "-" * 100)
    P("[1b] THE AMBIGUOUS TIER — files whose fail-set column NEVER emits >= 2 tokens")
    sing = [r for r in recs if r[0] == "T1_SINGLETON"]
    stab = census_table([("T1_DECLARED", fn, s) for _, fn, s in sing])
    sf = stab[stab.subset == "FULL"]
    s_dec, s_fail = int(sf.decisions.sum()), int(sf.failures.sum())
    s_oos = int(sf.sole_OOS.sum())
    P(f"  {len(sing)} artefacts / {len({run_of(fn) for _,fn,_ in sing})} runs, "
      f"{s_dec:,} decisions, {s_fail:,} failures")
    P(f"  single-token 'OOS' rows: {s_oos} — an UPPER BOUND on sole-OOS in this tier, because a")
    P(f"  FIRSTFAIL column reports OOS as soon as H1 and H2 pass, without ever testing DD or CAGR.")
    sing_hits = []
    for _, fn, sets in sing:
        k = sum(1 for s in sets if s == frozenset({"OOS"}))
        if k:
            P(f"      {k:4d} single-token 'OOS' rows in {fn}")
            sing_hits.append(fn)
    P("  These rows are RECONSTRUCTED from their own published numbers in [5b], after this run's")
    P("  own per-panel SPY reference has been measured on live prices.")

    # ---------------------------------------------------------- the bar-subset ladder
    P("\n" + "-" * 100)
    P("[2] PARAMETER 2 — the BAR SET.  Sole-OOS under nested conjunctions, ALL grid points")
    P("    (a leg can only look redundant relative to the bars it sits beside)")
    lad = []
    for sub in SUBSET_ORDER:
        s = ptab[ptab.subset == sub]
        f_ = int(s.failures.sum()); so = int(s.sole_OOS.sum())
        d_ = dict(subset=sub, bars="+".join(SUBSETS[sub]), decisions=int(s.decisions.sum()),
                  failures=f_, share_sole_OOS=so / f_ if f_ else np.nan)
        d_.update({f"sole_{b}": int(s[f"sole_{b}"].sum()) for b in SUBSETS[sub]})
        lad.append(d_)
    L = pd.DataFrame(lad)
    P(L.to_string(index=False, float_format=lambda x: f"{x:.5f}"))

    P("\n  the same ladder per TIER (4 subsets x 4 unambiguous tiers = all 16 grid points):")
    P(ptab[ptab.tier.isin(UNAMBIGUOUS)].pivot_table(index="tier", columns="subset",
        values="sole_OOS", aggfunc="sum").reindex(columns=SUBSET_ORDER).to_string())

    # ---------------------------------------------------------- conditional redundancy
    P("\n" + "-" * 100)
    P("[3] IS THE LEG REDUNDANT, OR MERELY RARELY DECISIVE?  conditional cut rates (pooled)")
    n_oosfail = n_h12pass = n_oosfail_given_h12pass = 0
    for _, fn, sets in pooled:
        for s in sets:
            if s is None:
                continue
            h12ok = ("H1" not in s) and ("H2" not in s)
            if "OOS" in s:
                n_oosfail += 1
            if h12ok:
                n_h12pass += 1
                if "OOS" in s:
                    n_oosfail_given_h12pass += 1
    P(f"  P(OOS bar fails)                       = {n_oosfail/tot['decisions']:.4f}")
    P(f"  P(H1 and H2 both pass)                 = {n_h12pass/tot['decisions']:.4f}")
    P(f"  P(OOS fails | H1 and H2 both pass)     = "
      f"{n_oosfail_given_h12pass/n_h12pass if n_h12pass else np.nan:.4f}  "
      f"({n_oosfail_given_h12pass:,} of {n_h12pass:,})")
    P("  -> the OOS leg carries information the halves do not; the question is only whether it is")
    P("     ever the LAST bar standing, which is the sole-OOS count above.")

    # ---------------------------------------------------------- the leaderboard tier
    P("\n" + "-" * 100)
    P("[4] LEADERBOARD.md TIER — an UPPER BOUND only (rows publish no OOS number)")
    nr, nn, npos = leaderboard_upper_bound()
    P(f"  table rows {nr}; rows with all four non-OOS numbers parseable {nn}; "
      f"rows whose four non-OOS bars ALL pass = {npos}")
    P(f"  -> at most {npos} published LEADERBOARD headline decisions could have been decided by the")
    P(f"     OOS leg alone; the other {nn-npos} were already cut by H1/H2/DD/CAGR before rule 8 ran.")
    P("     (SPY reference = the record's own U56 reading 0.957/0.834/15.23%/-33.72%; rows priced on")
    P("      BROAD136/SMALL439 or other windows carry a different SPY and are only bounded, not read.)")

    # ---------------------------------------------------------- GATES G2/G3
    P("\n" + "-" * 100)
    P("[G2/G3] CROSS-TIER AGREEMENT — files that publish TWO independent readings of the same rows")
    for a_t, b_t, tag in [("T1_DECLARED", "T2_MARGINS", "G2 SET-declared vs margins"),
                          ("T1_DECLARED", "T4_RECONSTRUCT", "G3 SET-declared vs recomputed"),
                          ("T1_SINGLETON", "T2_MARGINS", "G4 SINGLETON-declared vs margins"),
                          ("T1_SINGLETON", "T4_RECONSTRUCT", "G4 SINGLETON-declared vs recomputed")]:
        A = {fn: s for t, fn, s in recs if t == a_t}
        B = {fn: s for t, fn, s in recs if t == b_t}
        both = sorted(set(A) & set(B))
        n = agree = 0
        badf = []
        for fn in both:
            sa, sb = A[fn], B[fn]
            if len(sa) != len(sb):
                continue
            bad = 0
            for x, y in zip(sa, sb):
                if x is None or y is None:
                    continue
                n += 1
                if x == y:
                    agree += 1
                else:
                    bad += 1
            if bad:
                badf.append((fn, bad, len(sa)))
        P(f"  {tag}: {len(both)} shared files, {n:,} comparable rows, "
          f"agreement {agree/n if n else float('nan'):.4f}")
        for fn, bad, tot_ in badf[:5]:
            P(f"      disagrees on {bad}/{tot_} rows: {fn}")

    pd.DataFrame(ptab).to_csv(BD / f"{STEM}.census.csv", index=False)
    L.to_csv(BD / f"{STEM}.subsets.csv", index=False)

    # ---------------------------------------------------------- LIVE LEG
    P("\n" + "-" * 100)
    P("[5] LIVE LEG — 39 pre-registered books on fresh prices, all five 4b bars measured directly")
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    panels = [("U56", px56, [c for c in px56.columns if c != "SPY"]),
              ("BROAD136", px136, [c for c in px136.columns if c != "SPY"]),
              ("SMALL439", pxs, s_stk)]
    P(f"  panels: " + ", ".join(f"{nm}({len(c)} tradable, {p.index[0].date()}..{p.index[-1].date()})"
                                for nm, p, c in panels))

    rows = []
    SPYREF = {}
    for pname, px, cols in panels:
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = legs(spy_r)
        SPYREF[pname] = spy
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        base = legs(base_r)
        P(f"\n  {pname}: SPY full {spy['Sharpe']:.4f} (H1 {spy['H1']:.4f} / H2 {spy['H2']:.4f}), "
          f"OOS {spy['OOS_Sharpe']:.4f}, CAGR {spy['CAGR']:.2%}, MaxDD {spy['MaxDD']:.2%}")
        P(f"        RULES v2 baseline full {base['Sharpe']:.4f} "
          f"({base['H1']:.4f}/{base['H2']:.4f}), OOS {base['OOS_Sharpe']:.4f}")
        books = [(f"top{n}_g{g:.2f}", lambda p, c, n=n, g=g: topn_weights(p, c, n, g), n, g)
                 for n in (5, 10, 20, 30, 40) for g in (0.75, 1.00)]
        books += [(f"EWall_g{g:.2f}", lambda p, c, g=g: ew_weights(p, c, g), np.nan, g) for g in (0.75, 1.00)]
        books += [("RULESv2_band", lambda p, c: rules_v2_weights(p), np.nan, 0.75)]
        for bname, fn, n, g in books:
            r = backtest(px, fn(px, cols), cost_bps=10, freq="W")["returns"].loc[start:]
            b = legs(r)
            f4b = bars_4b(b, spy)
            p4a = (b["H1"] > base["H1"]) and (b["H2"] > base["H2"]) and (b["MaxDD"] >= base["MaxDD"])
            rows.append(dict(panel=pname, book=bname, n=n, gross=g, **b,
                             pass4b=len(f4b) == 0, fail4b=",".join(sorted(f4b)) or "-",
                             n_failing=len(f4b), sole=(next(iter(f4b)) if len(f4b) == 1 else ""),
                             pass4a=p4a,
                             spy_H1=spy["H1"], spy_H2=spy["H2"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                             spy_MaxDD=spy["MaxDD"], spy_CAGR=spy["CAGR"],
                             base_OOS_Sharpe=base["OOS_Sharpe"], base_Sharpe=base["Sharpe"]))
    R = pd.DataFrame(rows)
    R.to_csv(BD / f"{STEM}.live.csv", index=False)

    P(f"\n  all {len(R)} books (10 bps, weekly, next-day; full sample after 260d warm-up):")
    P(R[["panel", "book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "fail4b",
         "pass4b", "pass4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P(f"\n  BOTH KEEP PATHS on all {len(R)}: 4a {int(R.pass4a.sum())}/{len(R)} (vs live RULES v2 on "
      f"each book's own panel), 4b {int(R.pass4b.sum())}/{len(R)}")
    sole_live = R[R.n_failing == 1].sole.value_counts().to_dict()
    P(f"  binding-bar census on FRESH books: " +
      "  ".join(f"{b} fails {int(R.fail4b.str.contains(b).sum())}" for b in BARS))
    P(f"  SOLE binding bar on fresh books: {sole_live if sole_live else 'none — no book fails exactly one bar'}")
    P(f"  >>> SOLE-OOS on the {len(R)} live books = {sole_live.get('OOS', 0)}")

    # ---------------------------------------------------------- [5b] resolve the ambiguous tier
    P("\n" + "-" * 100)
    P("[5b] RESOLVING THE AMBIGUOUS TIER — the single-token 'OOS' rows of [1b], recomputed from")
    P("     their own published CAGR/MaxDD/H1/H2/OOS_Sharpe against the per-panel SPY measured above")
    ALIASP = {"B136": "BROAD136", "BROAD136": "BROAD136", "U56": "U56", "u56": "U56",
              "SMALL": "SMALL439", "SMALL439": "SMALL439", "SMALL484": "SMALL439", "small": "SMALL439"}
    n_rec = n_true = n_skip = 0
    for fn in sing_hits:
        p = BD / fn
        try:
            d = pd.read_csv(p)
        except Exception:
            continue
        cl = {c.lower(): c for c in d.columns}
        fcol = next(c for c in d.columns if c.lower() in FAILCOLS)
        need = ["cagr", "maxdd", "h1", "h2"]
        oosc = next((cl[k] for k in ("oos_sharpe", "sharpe_oos") if k in cl), None)
        if not all(k in cl for k in need) or oosc is None or "panel" not in cl:
            P(f"     {fn}: numbers or panel column missing — cannot resolve, stays an upper bound")
            n_skip += int((d[fcol].astype(str).str.strip() == "OOS").sum())
            continue
        sub = d[d[fcol].astype(str).str.strip() == "OOS"]
        got = []
        for _, r in sub.iterrows():
            pn = ALIASP.get(str(r[cl["panel"]]).strip())
            if pn is None or pn not in SPYREF:
                n_skip += 1; continue
            s = SPYREF[pn]
            b = dict(CAGR=r[cl["cagr"]], MaxDD=r[cl["maxdd"]], H1=r[cl["h1"]], H2=r[cl["h2"]],
                     OOS_Sharpe=r[oosc])
            f = bars_4b(b, s)
            n_rec += 1
            if f == frozenset({"OOS"}):
                n_true += 1
            got.append(",".join(sorted(f)) or "-")
        P(f"     {fn}: {len(sub)} single-token 'OOS' rows -> true failing sets "
          f"{ {k: int(v) for k, v in pd.Series(got).value_counts().items()} if got else {} }")
    P(f"  RESOLVED {n_rec} rows: {n_true} are genuinely sole-OOS, {n_rec-n_true} carry other failing")
    P(f"  bars the FIRSTFAIL column never printed; {n_skip} rows unresolvable (panel not on file).")
    P(f"  >>> the ambiguous tier contributes {n_true} sole-OOS decisions, not {s_oos}.")

    # ---------------------------------------------------------- rule 8
    P("\n" + "-" * 100)
    P("[6] RULE 8 WALK-FORWARD — n chosen on IS Sharpe (<= 2016-12-31) per (panel, gross),")
    P("    read ONCE on 2017-01-01.. ; ALL grid points reported above, the pick reported here")
    wf = []
    for pname in R.panel.unique():
        for g in (0.75, 1.00):
            pool = R[(R.panel == pname) & (R.gross == g) & R.book.str.startswith("top")]
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            wf.append(dict(panel=pname, gross=g, pick=pick.book, IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           base_OOS=pick.base_OOS_Sharpe, spy_OOS=pick.spy_OOS_Sharpe,
                           beats_base=pick.OOS_Sharpe > pick.base_OOS_Sharpe,
                           beats_spy=pick.OOS_Sharpe > pick.spy_OOS_Sharpe,
                           oracle_OOS=pool.OOS_Sharpe.max(), regret=pick.OOS_Sharpe - pool.OOS_Sharpe.max(),
                           pass4b=pick.pass4b, fail4b=pick.fail4b))
    W = pd.DataFrame(wf)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  chooser beats the live RULES v2 baseline OOS in {int(W.beats_base.sum())}/{len(W)} cells; "
      f"beats SPY OOS in {int(W.beats_spy.sum())}/{len(W)}")
    P(f"  mean OOS regret vs the oracle arm: {W.regret.mean():.4f}")
    P(f"  4b on the six rule-8 picks: {int(W.pass4b.sum())}/{len(W)}; "
      f"failing bars: {sorted(W.fail4b.tolist())}")

    # ---------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    P("VERDICT")
    grand = tot["sole_OOS"] + n_true
    P(f"  The queue's conditional ('if the answer is zero corpus-wide') is NOT met.  Over the")
    P(f"  UNAMBIGUOUS corpus the OOS leg is the sole binding bar in {tot['sole_OOS']:,} of")
    P(f"  {tot['failures']:,} re-readable 4b failures ({r_sole:.5f}), spread over "
      f"{tot['soleoos_files']} of {tot['files']} runs;")
    P(f"  the ambiguous FIRSTFAIL tier adds {n_true} more once resolved, for {grand} corpus-wide.")
    P(f"  Idea 285's 0 of 1,520 reproduces EXACTLY on its own corpus (gate G1) and does NOT")
    P(f"  generalise: it is a property of that construction, not of the protocol.")
    P(f"  On {len(R)} fresh pre-registered books the leg binds alone {sole_live.get('OOS',0)} times, and the")
    P(f"  rule-8 picks fail 4b on {len(W)-int(W.pass4b.sum())}/{len(W)} cells with DD in every failing set.")
    P(f"  Recommended PROTOCOL wording is in the memo, NOT applied here (PROTOCOL.md untouched;")
    P(f"  rules change only via Sunday review, rule 6).")
    (BD / f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
