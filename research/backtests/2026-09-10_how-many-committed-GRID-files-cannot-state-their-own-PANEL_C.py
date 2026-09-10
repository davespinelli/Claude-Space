#!/usr/bin/env python3
"""Idea 653 — how many committed GRID files cannot state their own PANEL?  (lane C, 2026-09-10)

QUEUE 653: "idea 480 found 7 of 96 committed five-margin blocks (107,816 of 370,102 rows) carry
no mappable panel column, so no noise-unit reading of them is possible at all.  Audit which of
those files' published claims depend on a panel-relative quantity, and whether the panel is
recoverable from the parent script rather than the CSV.  INFRASTRUCTURE-adjacent; max 2 params."

WHAT IS ACTUALLY BEING TESTED
  H1 (recoverability)  The panel of an "unstated" block is recoverable from the artefact set the
        record already commits — a wider alias vocabulary, a non-`panel` label column in the SAME
        CSV, a same-stem sibling CSV, the parent .py, or a `file` column pointing at a source
        CSV.  FALSIFIABLE: if the ladder leaves the 107,816 rows unrecovered, the queue's premise
        stands and the record needs a PROTOCOL line requiring a panel stamp.
  H2 (exposure)  The published claims made off those seven files depend on a PANEL-RELATIVE
        quantity, so the missing stamp is load-bearing rather than cosmetic.  FALSIFIABLE: if the
        claims are all within-file absolute statements, nothing was ever at risk.
  H3 (payoff)  Once recovered, the binding bar of those blocks read in panel-noise units differs
        from the RAW reading — i.e. the recovery buys a different answer, not just a label.
        FALSIFIABLE: if the modal bar is unchanged, the recovery is bookkeeping.
  H4 (live cost)  A missing or WRONG panel stamp costs a rule-8 book chooser real out-of-sample
        performance.  On a fresh 4-panel grid, a selector that ranks arms by their IS binding
        margin in the arm's OWN panel-noise units is compared against (i) the RAW selector that
        needs no panel at all and (ii) a MIS-STAMPED selector that divides by another panel's
        noise.  FALSIFIABLE: if all three pick the same book, the stamp is cosmetic in the only
        place PROTOCOL lets anything be chosen.

AXES, AND WHAT IS EVER SELECTED ON (PROTOCOL 4, "no more than 2 tuned parameters")
    P1 RECOVERY SOURCE : L0 DECLARED (idea 480's own 3-key mapper, the incumbent)
                         L1 +ALIAS      (same column, alias vocabulary widened to every panel key
                                         the record actually writes — census-derived, not guessed)
                         L2 +LABEL      (any OTHER column in the same CSV whose VALUES name a panel)
                         L3 +SIBLING    (a same-stem CSV that carries a single-valued panel column)
                         L4 +SCRIPT     (the parent .py builds exactly one panel)
                         L5 +TRANSITIVE (a `file`/`src` column naming a committed CSV; recurse)
                         All six levels reported; the ladder is monotone by construction.
    P2 CLAIM READING   : LOOSE  (a published sentence naming the file/idea and any panel word)
                         STRICT (the sentence's QUANTITY is panel-relative: noise units, a per-
                                 panel scale, a cross-panel ordering, or a named-panel contrast)
                         Both reported for every file.
  REPORTED, NOT TUNED: the four panels, the fresh grid's books / bands / grosses, the cost rungs,
  and the null's draw count.  Nothing is chosen by looking at an outcome except in rule 8.

GATES (run before any new number is read)
  G1 the vectorised runner vs `engine.backtest` on the evaluated slice, returns AND turnover, on
     all four panels.
  G2 the cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live `engine.backtest(cost_bps=25)`.
  G3 idea 480's OWN A3 census is reproduced exactly off the committed CSVs: 96 blocks, 370,102
     rows, 7 files with an unstated panel, 107,816 unstated rows.  If this does not reproduce,
     the queue's premise cannot be audited and the run stops.
  G4 MONOTONE + NON-CONTRADICTORY: every level of the ladder is a superset of the one below, and
     on a row L0 already labels, no higher level assigns a DIFFERENT panel (0 disagreements).
  G5 the fresh null returns exactly 0 dispersion when the draw is the whole panel (a degenerate
     draw has no noise), so sd_null is measuring draw dispersion and nothing else.

CAVEATS CARRIED
  * The census reads COMMITTED CSVs only; a claim made in prose and never written to a CSV is
    invisible to the block census, which is why the prose leg (P2) is run separately over
    CHANGELOG.md / LEADERBOARD.md / QUEUE.md and each stem's own .result.md.
  * A header/value regex cannot tell a claim from a statistic ABOUT a claim; LOOSE is reported
    beside STRICT as an upper bound rather than one being chosen.
  * SURVIVORSHIP (PROTOCOL 9, idea 54): u56 / broad / bstk100 are today's constituents and
    SMALL439 is the sub-$2B screen's SURVIVORS; every CAGR here is inflated and every 4b CAGR
    floor is generous.  Only within-panel contrasts are read as edges.
  * `bstk100` is the broad panel minus every ETF with SPY held out (idea 542's construction,
    reproduced verbatim here); it has no ETFs and therefore no sleeve books.
  * MaxDD is one number off one path (idea 321) and the 4b DD cap turns on exactly that number.
  * Idea 126: t+1 execution, no lag band.  Idea 38: u56/broad carry the calendar-day index.
  * idea 480's committed `.scales.csv` recovers a scale for B136 and U56 only, so its own
    noise-unit reading never reached SMALL439 at all — that limit is inherited and reported.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .ladder.csv, .blocks.csv,
.prose.csv, .payoff.csv, .grid.csv, .keeppaths.csv, .walkforward.csv next to itself.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask              # noqa: E402

STEM = "2026-09-10_how-many-committed-GRID-files-cannot-state-their-own-PANEL_C"
BT = ROOT / "research" / "backtests"
OUT = BT
I480 = BT / "2026-09-10_state-the-UNIT-on-every-binding-bar-claim-in-the-record_B.blocks.csv"

BARS = ["H1", "H2", "OOS", "DD", "CAGR"]
FREQ = "W"
COST = 10.0
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60                 # 4b CAGR floor / DD cap fractions of SPY
NDRAW, KFRAC, SEED = 120, 0.5, 653      # the panel-noise null: equal-weight half-panel draws

PANELS = ["u56", "broad", "small", "bstk100"]
REC = {"u56": "U56", "broad": "B136", "small": "SMALL439", "bstk100": "BSTK100"}
BOOKS = ["EWALL", "TOP20", "LOWVOL20"]
BANDS = [0.00, 0.02, 0.04, 0.06]
GROSSES = [0.50, 0.75, 1.00]
NTOP = 20

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG: list[str] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# =====================================================================================
# vectorised runner (segment-exact vs engine.backtest at zero cost)
# =====================================================================================
def fast_bt(px: pd.DataFrame, W: pd.DataFrame, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    w_t = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    reb = np.unique(np.concatenate(([0], np.flatnonzero(mask))))
    port = np.zeros(n)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for si, i0 in enumerate(reb):
        i1 = reb[si + 1] if si + 1 < len(reb) else n
        if i1 <= i0:
            continue
        new = w_t[i0]
        turn[i0] = np.abs(new - cur).sum()
        A = new[None, :] * np.cumprod(1.0 + rets[i0:i1], axis=0)
        S = A.sum(axis=1) + (1.0 - new.sum())
        port[i0:i1] = S / np.concatenate(([1.0], S[:-1])) - 1.0
        cur = A[-1] / S[-1]
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


# =====================================================================================
# panels
# =====================================================================================
def etf_set():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return {t for g, v in U.items() if g != "megacap" for t in v} - {"BTC-USD", "ETH-USD"}


def get_panels():
    P = {}
    P["u56"] = load_universe()
    P["broad"] = load_universe(broad=True)
    sp = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    P["small"] = sp[[c for c in sp.columns if c == "SPY" or c not in bad]]
    b = load_universe(broad=True)
    keep = [c for c in b.columns if c not in etf_set() or c == "SPY"]
    P["bstk100"] = b[keep]
    return P


def investable(pk, px):
    """SPY is the benchmark, never a constituent, on small and bstk100 (idea 542)."""
    return [c for c in px.columns if not (pk in ("small", "bstk100") and c == "SPY")]


def composite(sub):
    mom = sub.shift(21) / sub.shift(252) - 1
    r6 = sub / sub.shift(126) - 1
    r3 = sub / sub.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def book_weights(px, cols, book, gross):
    sub = px[cols]
    if book == "EWALL":
        e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
        W = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif book == "TOP20":
        W = (composite(sub).rank(axis=1, ascending=False) <= NTOP).astype(float) * (gross / NTOP)
    elif book == "LOWVOL20":
        v = sub.pct_change().rolling(60).std()
        W = (v.rank(axis=1, ascending=True) <= NTOP).astype(float) * (gross / NTOP)
    else:
        raise ValueError(book)
    return W.reindex(columns=px.columns).fillna(0.0)


# =====================================================================================
# metric helpers (PROTOCOL 4b verbatim)
# =====================================================================================
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_of(spy, which="full"):
    s = spy if which == "full" else spy.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    return dict(s1=metrics(s.iloc[:h])["Sharpe"], s2=metrics(s.iloc[h:])["Sharpe"],
                sdd=m["MaxDD"], scagr=m["CAGR"],
                soos=metrics(spy.loc[OOS_START:])["Sharpe"] if which == "full" else np.nan)


def margins(r, b, which="full"):
    s = r if which == "full" else r.loc[:IS_END]
    h = len(s) // 2
    m = metrics(s)
    d = dict(H1=metrics(s.iloc[:h])["Sharpe"] - b["s1"],
             H2=metrics(s.iloc[h:])["Sharpe"] - b["s2"],
             DD=DELTA * abs(b["sdd"]) - abs(m["MaxDD"]),
             CAGR=m["CAGR"] - PHI * b["scagr"])
    d["OOS"] = (metrics(r.loc[OOS_START:])["Sharpe"] - b["soos"]) if which == "full" else np.nan
    return d


def pass4a(r, base):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


# =====================================================================================
# the panel-noise null (idea 480's second null, rebuilt for all FOUR panels)
# =====================================================================================
def null_scales(panels):
    """sd over NDRAW equal-weight half-panel draws held inside the live 200d band, of each of
    the five 4b margins.  Deterministic in (panel, SEED).  This is the scale a noise-unit
    reading divides by — and it exists only if you know which panel the row came from."""
    say("\n" + "-" * 100)
    say(f"PANEL-NOISE NULL — {NDRAW} equal-weight half-panel draws per panel inside the live "
        f"200d band, seed {SEED}")
    say("-" * 100)
    rows, deg = [], []
    for pk in PANELS:
        px = panels[pk]
        cols = investable(pk, px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b = bars_of(spy)
        bst = band_state(px[cols], 0.03)
        rng = np.random.default_rng(SEED)
        k = max(2, int(round(KFRAC * len(cols))))
        M = []
        for _ in range(NDRAW):
            pick = list(rng.choice(cols, size=k, replace=False))
            e = pd.DataFrame(1.0, index=px.index, columns=pick).where(px[pick].notna(), 0.0)
            W = 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            W = W.where(bst[pick], 0.0).reindex(columns=px.columns).fillna(0.0)
            r, t = fast_bt(px, W)
            r = (r - t * COST / 1e4).loc[start:]
            M.append(margins(r, b))
        D = pd.DataFrame(M)
        rows.append(dict(panel=REC[pk], k=k, n_names=len(cols), ndraw=NDRAW,
                         **{f"sd_{c}": float(D[c].std(ddof=1)) for c in BARS}))
        # G5: a degenerate draw (the whole panel, every draw identical) must have zero dispersion
        e = pd.DataFrame(1.0, index=px.index, columns=cols).where(px[cols].notna(), 0.0)
        W = 0.75 * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        W = W.where(bst, 0.0).reindex(columns=px.columns).fillna(0.0)
        r, t = fast_bt(px, W)
        r = (r - t * COST / 1e4).loc[start:]
        m1 = margins(r, b)
        deg.append(max(abs(m1[c] - m1[c]) for c in BARS))
    S = pd.DataFrame(rows).set_index("panel")
    say(S.to_string(float_format=lambda x: f"{x:.5f}"))
    say(f"  G5 degenerate-draw dispersion (whole panel, no randomness): {max(deg):.3e}   "
        f"{'PASS' if max(deg) < 1e-12 else 'FAIL'}")
    return S, max(deg)


# =====================================================================================
# THE LADDER — six recovery levels
# =====================================================================================
# L0: idea 480's own mapper, verbatim (3 keys, columns named panel/universe/uni).
L0_ALIAS = {"u56": "U56", "universe.json(56)": "U56", "universe.json": "U56",
            "broad": "B136", "broad136": "B136", "universe_broad.json": "B136",
            "universe_broad(136)": "B136",
            "small": "SMALL439", "small439": "SMALL439"}
L0_COLS = ("panel", "universe", "uni")

# L1: the alias vocabulary WIDENED to every panel key the record actually writes.  The extra
# keys are census-derived (part_vocab below prints the whole vocabulary before it is used), not
# guessed: `bstk100` is idea 542's fourth panel, documented in its own parent script.
L1_EXTRA = {"bstk100": "BSTK100", "bstk": "BSTK100", "broad_noetf": "BSTK100",
            "u56/broad": None, "pooled": None, "all": None, "": None, "nan": None}
# L2: values ANYWHERE in a row that name a panel (label columns like `arm`, `src_`, `stem`).
L2_PAT = [(re.compile(r"\bu56\b", re.I), "U56"),
          (re.compile(r"\bb136\b", re.I), "B136"),
          (re.compile(r"\bbroad\b", re.I), "B136"),
          (re.compile(r"\bsmall439\b", re.I), "SMALL439"),
          (re.compile(r"\bsmall\b", re.I), "SMALL439"),
          (re.compile(r"\bbstk100\b", re.I), "BSTK100")]
LEVELS = ["L0_DECLARED", "L1_ALIAS", "L2_LABEL", "L3_SIBLING", "L4_SCRIPT", "L5_TRANSITIVE"]


def map_l0(v):
    v = str(v).strip()
    return L0_ALIAS.get(v.lower(), v if v in ("U56", "B136", "SMALL439") else None)


def map_l1(v):
    v = str(v).strip()
    hit = map_l0(v)
    if hit:
        return hit
    lv = v.lower()
    if lv in L1_EXTRA:
        return L1_EXTRA[lv]
    return v if v in ("U56", "B136", "SMALL439", "BSTK100") else None


def map_l2_value(v):
    s = str(v)
    hits = {tag for pat, tag in L2_PAT if pat.search(s)}
    return hits.pop() if len(hits) == 1 else None


def block_files():
    """Every committed CSV carrying a COMPLETE five-margin block and >= 8 rows — idea 480's A3
    population, rebuilt by the same rule so G3 is a real reproduction."""
    out = []
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(STEM + "."):
            continue        # a census must never read its own output (self-reference, idea 313)
        try:
            hdr = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            continue
        cols = set(hdr)
        suf = ("" if {f"m_{b}" for b in BARS} <= cols else
               ("_" if {f"m_{b}_" for b in BARS} <= cols else None))
        if suf is None:
            continue
        out.append((f, hdr, suf))
    return out


def sibling_panel(stem):
    """L3 — a same-stem committed CSV carrying a panel column with exactly ONE distinct
    mappable value: the run was a single-panel run and said so somewhere else in its own set."""
    vals = set()
    for g in sorted(BT.glob(f"{stem}.*.csv")):
        try:
            hdr = pd.read_csv(g, nrows=0).columns.tolist()
        except Exception:
            continue
        pc = [c for c in hdr if c.lower().strip("_") in L0_COLS]
        if not pc:
            continue
        try:
            d = pd.read_csv(g, usecols=pc[:1])
        except Exception:
            continue
        vals |= {map_l1(v) for v in d[pc[0]].dropna().unique()}
    vals -= {None}
    return vals.pop() if len(vals) == 1 else None


PANEL_CALL = [(re.compile(r"load_universe\s*\(\s*small\s*=\s*True"), "SMALL439"),
              (re.compile(r"load_universe\s*\(\s*broad\s*=\s*True"), "B136"),
              (re.compile(r"load_universe\s*\(\s*\)"), "U56"),
              (re.compile(r"\bbstk100\b"), "BSTK100")]


def script_panel(stem):
    """L4 — the parent .py.  Assign only when the script's panel evidence is UNANIMOUS: it builds
    exactly one panel (one distinct load_universe flavour) or its own filename names one."""
    p = BT / f"{stem}.py"
    if not p.exists():
        return None, "no-parent-script"
    try:
        src = p.read_text(errors="ignore")
    except Exception:
        return None, "unreadable"
    src_nodoc = re.sub(r'"""».*?"""', "", src, flags=re.S)
    hits = {tag for pat, tag in PANEL_CALL if pat.search(src_nodoc)}
    if len(hits) == 1:
        return hits.pop(), "unanimous-load_universe"
    fn = {tag for pat, tag in L2_PAT if pat.search(stem)}
    if len(fn) == 1:
        return fn.pop(), "filename"
    return None, f"ambiguous({'|'.join(sorted(hits)) or 'none'})"


SRC_COLS = ("file", "src", "src_", "source", "stem", "parent")


def build_ladder(files):
    """Return, per block file, the per-row panel label at each of the six levels."""
    recs, rowlab = [], {}
    # Pass 1 — every block file's own per-row L0/L1/L2 labels.
    for f, hdr, suf in files:
        mcols = [f"m_{b}{suf}" for b in BARS]
        pc = [c for c in hdr if c.lower().strip("_") in L0_COLS]
        lab = [c for c in hdr if c.lower().strip("_") in
               ("arm", "book", "src_", "src", "stem", "file", "kind", "name", "panel_")]
        use = list(dict.fromkeys(mcols + pc[:1] + lab))
        try:
            d = pd.read_csv(f, usecols=[c for c in use if c in hdr], low_memory=False)
        except Exception:
            continue
        d = d.dropna(subset=[c for c in mcols if c in d.columns])
        if len(d) < 8:
            continue
        n = len(d)
        l0 = (d[pc[0]].map(map_l0) if pc else pd.Series([None] * n, index=d.index))
        l1 = (d[pc[0]].map(map_l1) if pc else pd.Series([None] * n, index=d.index))
        l2 = l1.copy()
        need = l2.isna()
        if need.any() and lab:
            cand = d.loc[need, [c for c in lab if c in d.columns]].astype(str).agg(" ".join, axis=1)
            l2.loc[need] = cand.map(map_l2_value)
        stem = f.name.split(".")[0]
        sib = sibling_panel(stem)
        l3 = l2.where(l2.notna(), sib)
        scr, why = script_panel(stem)
        l4 = l3.where(l3.notna(), scr)
        recs.append(dict(file=f.name, stem=stem, n=n, suf=suf,
                         has_panel_col=bool(pc), label_cols="|".join(lab),
                         sibling=sib, script=scr, script_why=why,
                         L0_DECLARED=int(l0.notna().sum()), L1_ALIAS=int(l1.notna().sum()),
                         L2_LABEL=int(l2.notna().sum()), L3_SIBLING=int(l3.notna().sum()),
                         L4_SCRIPT=int(l4.notna().sum()),
                         l0_vals="|".join(sorted({str(x) for x in l0.dropna().unique()})),
                         l4_vals="|".join(sorted({str(x) for x in l4.dropna().unique()}))))
        rowlab[f.name] = dict(d=d, l0=l0, l4=l4, mcols=mcols)
    A = pd.DataFrame(recs)
    # Pass 2 — L5 TRANSITIVE: a `file`/`src` column naming another committed CSV whose own L4
    # label is single-valued.  Resolved AFTER pass 1 so the target's label already exists.
    l4_by_file = {r.file: (r.l4_vals.split("|") if r.l4_vals else []) for r in A.itertuples()}
    l5_counts = {}
    for f, hdr, suf in files:
        nm = f.name
        if nm not in rowlab:
            continue
        st = rowlab[nm]
        l5 = st["l4"].copy()
        need = l5.isna()
        srcc = [c for c in hdr if c.lower().strip("_") in SRC_COLS and c in st["d"].columns]
        if need.any() and srcc:
            def resolve(v):
                vs = str(v).strip()
                cands = l4_by_file.get(vs)
                if cands is None:
                    hit = [k for k in l4_by_file if k.startswith(vs.split(".")[0])]
                    cands = l4_by_file[hit[0]] if len(hit) == 1 else None
                if cands and len(cands) == 1:
                    return cands[0]
                return map_l2_value(vs)
            l5.loc[need] = st["d"].loc[need, srcc[0]].map(resolve)
        st["l5"] = l5
        l5_counts[nm] = int(l5.notna().sum())
    A["L5_TRANSITIVE"] = A.file.map(l5_counts).fillna(A.L4_SCRIPT).astype(int)
    return A, rowlab


# =====================================================================================
# PART B — do the published claims depend on a panel-relative quantity?
# =====================================================================================
REL_STRICT = re.compile(
    r"noise unit|panel[- ]noise|panel-relative|in noise|z-score|per-panel|per panel|"
    r"sd_null|noise floor|orders the (three )?panels|cross-panel|across panels|"
    r"panel fact|panel of origin|U56|B136|SMALL439|BSTK100|relative to (its|the) panel", re.I)
REL_LOOSE = re.compile(r"panel|universe|u56|b136|small439|bstk100|broad", re.I)
NUMBER = re.compile(r"-?\d+\.?\d*\s*(%|bps|pp|x\b)|\b\d+\.\d{2,}\b")


def prose_sources():
    src = {}
    for nm in ("CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md"):
        p = ROOT / "research" / nm
        if p.exists():
            src[nm] = p.read_text(errors="ignore")
    return src


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", text) if len(s.strip()) > 40]


def part_prose(targets):
    say("\n" + "=" * 100)
    say("PART B — P2 CLAIM READING: do the seven files' PUBLISHED claims depend on a "
        "PANEL-RELATIVE quantity?")
    say("=" * 100)
    src = prose_sources()
    rows = []
    for stem in targets:
        idea = None
        m = re.search(rf"idea (\d+) {re.escape(stem.split('_', 1)[1].rsplit('_', 1)[0])}",
                      src.get("CHANGELOG.md", ""))
        if m:
            idea = m.group(1)
        slug = stem.split("_", 1)[1].rsplit("_", 1)[0]
        pool = dict(src)
        own = BT / f"{stem}.result.md"
        if own.exists():
            pool["own.result.md"] = own.read_text(errors="ignore")
        for where, text in pool.items():
            for s in sentences(text):
                names = (slug in s) or (idea and re.search(rf"\bidea {idea}\b", s))
                if not names:
                    continue
                loose = bool(REL_LOOSE.search(s))
                strict = bool(REL_STRICT.search(s)) and bool(NUMBER.search(s))
                rows.append(dict(stem=stem, idea=idea, where=where, loose=loose, strict=strict,
                                 sentence=s[:400]))
    PR = pd.DataFrame(rows)
    if PR.empty:
        say("  no published sentence names any of the seven files.")
        return PR
    say(f"  sentences naming one of the {len(targets)} files across CHANGELOG / LEADERBOARD / "
        f"QUEUE / own .result.md: {len(PR)}")
    g = PR.groupby("stem").agg(n=("loose", "size"), LOOSE=("loose", "sum"),
                               STRICT=("strict", "sum"))
    g["LOOSE_share"] = g.LOOSE / g.n
    g["STRICT_share"] = g.STRICT / g.n
    say(g.to_string(float_format=lambda x: f"{x:.3f}"))
    say(f"\n  POOLED: LOOSE {int(PR.loose.sum())}/{len(PR)} = {PR.loose.mean():.3f}   "
        f"STRICT {int(PR.strict.sum())}/{len(PR)} = {PR.strict.mean():.3f}")
    say("  files with at least ONE strict panel-relative published claim: "
        f"{int((g.STRICT > 0).sum())}/{len(g)}")
    return PR


# =====================================================================================
# PART C — payoff: does recovery change the binding bar?
# =====================================================================================
def part_payoff(A, rowlab, S):
    say("\n" + "=" * 100)
    say("PART C — PAYOFF: with the panel recovered, does the block's BINDING BAR move?")
    say("=" * 100)
    sd = {p: S.loc[p, [f"sd_{b}" for b in BARS]].values for p in S.index}
    rows = []
    for nm, st in rowlab.items():
        d, mcols = st["d"], st["mcols"]
        M = d[mcols].values.astype(float)
        raw = np.array(BARS)[M.argmin(axis=1)]
        for lvl, lab in (("L0_DECLARED", st["l0"]), ("L5_TRANSITIVE", st.get("l5", st["l4"]))):
            lv = lab.values
            ok = np.array([p in sd for p in lv])
            if not ok.any():
                rows.append(dict(file=nm, level=lvl, n=len(d), n_conv=0,
                                 raw_modal=pd.Series(raw).value_counts().index[0],
                                 noise_modal=None, flip=np.nan))
                continue
            Z = np.full(M.shape, np.nan)
            for i in np.flatnonzero(ok):
                Z[i] = M[i] / sd[lv[i]]
            nz = np.array(BARS)[np.where(ok[:, None], Z, 0.0).argmin(axis=1)]
            rows.append(dict(file=nm, level=lvl, n=len(d), n_conv=int(ok.sum()),
                             raw_modal=pd.Series(raw).value_counts().index[0],
                             noise_modal=pd.Series(nz[ok]).value_counts().index[0],
                             flip=float((raw[ok] != nz[ok]).mean())))
    P = pd.DataFrame(rows)
    for lvl in ("L0_DECLARED", "L5_TRANSITIVE"):
        s = P[P.level == lvl]
        conv = s[s.n_conv > 0]
        say(f"  {lvl:<14}  convertible files {len(conv):>3}/{len(s)}   convertible rows "
            f"{int(s.n_conv.sum()):>7,}/{int(s.n.sum()):,}   "
            f"files whose MODAL bar flips RAW->NOISE "
            f"{int((conv.raw_modal != conv.noise_modal).sum())}/{len(conv)} "
            f"({(conv.raw_modal != conv.noise_modal).mean() if len(conv) else float('nan'):.3f})   "
            f"cell-level median flip {conv.flip.median() if len(conv) else float('nan'):.3f}")
    say("\n  modal binding bar of every convertible block:")
    for lvl in ("L0_DECLARED", "L5_TRANSITIVE"):
        s = P[(P.level == lvl) & (P.n_conv > 0)]
        for nmv, col in (("RAW", "raw_modal"), ("NOISE", "noise_modal")):
            vc = s[col].value_counts()
            say(f"    {lvl:<14} {nmv:<6} " + "  ".join(f"{k} {v}" for k, v in vc.items()))
    return P


# =====================================================================================
# GATES
# =====================================================================================
def gates(panels):
    say("=" * 100)
    say("GATES (run before any new number is read)")
    say("=" * 100)
    ok = True
    dmax = tmax = rmax = 0.0
    for pk in PANELS:
        px = panels[pk]
        cols = investable(pk, px)
        W = book_weights(px, cols, "TOP20", 0.75)
        ref = backtest(px, W, cost_bps=0.0, freq=FREQ)
        r, t = fast_bt(px, W)
        sl = px.index[260:]
        dmax = max(dmax, float(np.abs(ref["returns"].loc[sl].values - r.loc[sl].values).max()))
        tmax = max(tmax, float(np.abs(ref["turnover"].loc[sl].values - t.loc[sl].values).max()))
        ref25 = backtest(px, W, cost_bps=25.0, freq=FREQ)["returns"].loc[sl]
        rmax = max(rmax, float(np.abs(((r - t * 25.0 / 1e4).loc[sl] - ref25).values).max()))
        say(f"  {pk:<8} names {len(cols):>4}  span {px.index[0].date()} -> {px.index[-1].date()}")
    say(f"  G1 fast_bt vs engine.backtest : returns {dmax:.3e}  turnover {tmax:.3e}   "
        f"{'PASS' if dmax < 1e-12 and tmax < 1e-12 else 'FAIL'}")
    say(f"  G2 cost-rung identity @25 bps : {rmax:.3e}   {'PASS' if rmax < 1e-12 else 'FAIL'}")
    ok &= dmax < 1e-12 and tmax < 1e-12 and rmax < 1e-12
    return ok


def gate_g3(A):
    """G3 is VINTAGE-PINNED (ideas 328/514: a census gate must name the tree it ran on).  The
    reproduction is required on exactly the 96 files idea 480's committed `.blocks.csv` could
    see; today's tree carries more, and the delta is reported beside it rather than folded in."""
    say("\n  G3 — idea 480's A3 block census reproduced off the committed CSVs (VINTAGE-PINNED):")
    if not I480.exists():
        say("     idea 480's .blocks.csv is not committed — G3 cannot run.  FAIL")
        return False, None, None, None
    B = pd.read_csv(I480)
    ref = dict(files=len(B), rows=int(B.n.sum()),
               unstated_files=int((B.n_panel_unstated > 0).sum()),
               unstated_rows=int(B.n_panel_unstated.sum()))
    exp = dict(files=96, rows=370102, unstated_files=7, unstated_rows=107816)
    pin = A[A.file.isin(set(B.file))].copy()
    got = dict(files=len(pin), rows=int(pin.n.sum()),
               unstated_files=int((pin.n - pin.L0_DECLARED > 0).sum()),
               unstated_rows=int((pin.n - pin.L0_DECLARED).sum()))
    for k in exp:
        say(f"     {k:<16} pinned {got[k]:>8,}   idea 480 committed {ref[k]:>8,}   "
            f"queue {exp[k]:>8,}")
    mg = pin.merge(B[["file", "n", "n_panel_unstated"]], on="file", suffixes=("", "_480"))
    drift_n = int((mg.n != mg.n_480).sum())
    drift_u = int(((mg.n - mg.L0_DECLARED) != mg.n_panel_unstated).sum())
    say(f"     per-file row-count drift {drift_n}/{len(mg)}   per-file unstated-count drift "
        f"{drift_u}/{len(mg)}   (0 required)")
    new = A[~A.file.isin(set(B.file))]
    say(f"     files added to the tree SINCE idea 480 ran: {len(new)} "
        f"({int(new.n.sum()):,} rows, {int((new.n - new.L0_DECLARED).sum()):,} unstated) — "
        f"reported, not folded into the gate")
    good = (all(got[k] == exp[k] for k in exp) and all(ref[k] == exp[k] for k in exp)
            and drift_n == 0 and drift_u == 0 and len(B.file) == B.file.nunique())
    say(f"     G3 {'PASS' if good else 'FAIL'}")
    return good, got, ref, pin


def gate_g4(A, rowlab):
    """Monotone ladder + no level contradicts a label L0 already assigned."""
    mono = True
    for i in range(len(LEVELS) - 1):
        bad = int((A[LEVELS[i + 1]] < A[LEVELS[i]]).sum())
        mono &= bad == 0
    dis = 0
    tot = 0
    for nm, st in rowlab.items():
        l0 = st["l0"]
        l5 = st.get("l5", st["l4"])
        m = l0.notna()
        tot += int(m.sum())
        dis += int((l0[m] != l5[m]).sum())
    say(f"\n  G4 ladder monotone across all six levels: {'PASS' if mono else 'FAIL'}")
    say(f"  G4 higher levels contradicting an L0 label: {dis} of {tot:,} L0-labelled rows   "
        f"{'PASS' if dis == 0 else 'FAIL'}")
    return mono and dis == 0


# =====================================================================================
# MAIN
# =====================================================================================
def main():
    T0 = time.time()
    say("=" * 100)
    say("IDEA 653 — how many committed GRID files cannot state their own PANEL?  (lane C)")
    say("=" * 100)
    say("tuned parameter 1 (recovery source): L0 DECLARED / L1 ALIAS / L2 LABEL / L3 SIBLING / "
        "L4 SCRIPT / L5 TRANSITIVE — all six reported")
    say("tuned parameter 2 (claim reading) : LOOSE / STRICT — both reported")
    say(f"reported, not tuned: panels {PANELS}; books {BOOKS}; bands {BANDS}; grosses {GROSSES}; "
        f"rungs {RUNGS} bps; weekly, t+1; IS <= {IS_END}, OOS >= {OOS_START}; null {NDRAW} draws")

    panels = get_panels()
    if not gates(panels):
        say("\n*** GATES FAILED — no new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    say("\n" + "=" * 100)
    say("PART A — P1 RECOVERY LADDER over every committed five-margin block")
    say("=" * 100)
    files = block_files()
    A, rowlab = build_ladder(files)
    A.to_csv(OUT / f"{STEM}.blocks.csv", index=False)
    g3, got, ref, PIN = gate_g3(A)
    if not g3:
        say("\n*** G3 FAILED — idea 480's census does not reproduce; the premise cannot be "
            "audited on today's tree. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        A.to_csv(OUT / f"{STEM}.blocks.csv", index=False)
        return 1
    if not gate_g4(A, rowlab):
        say("\n*** G4 FAILED — the ladder is not monotone or contradicts a declared label. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1

    say("\n  PANEL-COLUMN VOCABULARY the record actually writes (census, before any mapping):")
    vocab = {}
    for f, hdr, suf in files:
        pc = [c for c in hdr if c.lower().strip("_") in L0_COLS]
        if not pc:
            continue
        try:
            d = pd.read_csv(f, usecols=pc[:1], low_memory=False)
        except Exception:
            continue
        for v, c in d[pc[0]].astype(str).value_counts().items():
            vocab[v] = vocab.get(v, 0) + int(c)
    for v, c in sorted(vocab.items(), key=lambda kv: -kv[1]):
        say(f"    {v:<24} {c:>9,}   L0 -> {str(map_l0(v)):<9} L1 -> {str(map_l1(v))}")

    lad = []
    for pop_name, POP in (("PINNED(idea 480)", PIN), ("TODAY", A)):
        tot_rows = int(POP.n.sum())
        say(f"\n  THE LADDER — {pop_name} population ({len(POP)} blocks, {tot_rows:,} rows):")
        say(f"    {'level':<15}{'files w/ any unstated':>24}{'unstated rows':>16}{'share':>9}")
        for lv in LEVELS:
            uf = int((POP.n - POP[lv] > 0).sum())
            ur = int((POP.n - POP[lv]).sum())
            lad.append(dict(population=pop_name, level=lv, files_total=len(POP),
                            files_unstated=uf, rows_total=tot_rows, rows_unstated=ur,
                            share_unstated=ur / tot_rows))
            say(f"    {lv:<15}{uf:>24}{ur:>16,}{ur / tot_rows:>9.4f}")
    L = pd.DataFrame(lad)
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

    targets = sorted(PIN.loc[PIN.n - PIN.L0_DECLARED > 0, "file"])
    stems = sorted({t.split(".")[0] for t in targets})
    say(f"\n  THE SEVEN FILES the queue names, level by level "
        f"(rows still unstated after each level):")
    say(f"    {'file':<92}" + "".join(f"{lv.split('_')[0]:>7}" for lv in LEVELS))
    for _, r in A[A.file.isin(targets)].iterrows():
        say(f"    {r.file:<92}" + "".join(f"{int(r.n - r[lv]):>7,}" for lv in LEVELS))
    say(f"    {'TOTAL':<92}" + "".join(
        f"{int((A.loc[A.file.isin(targets), 'n'] - A.loc[A.file.isin(targets), lv]).sum()):>7,}"
        for lv in LEVELS))
    say("\n  how each of the seven was recovered:")
    for _, r in A[A.file.isin(targets)].iterrows():
        say(f"    {r.file}")
        say(f"        panel col {str(r.has_panel_col):<5} L0 vals [{r.l0_vals}]  "
            f"label cols [{r.label_cols}]")
        say(f"        sibling {str(r.sibling):<9} script {str(r.script):<9} ({r.script_why})  "
            f"final vals [{r.l4_vals}]")

    # ---- why the residual cannot be recovered ---------------------------------------
    say("\n  RESIDUAL DIAGNOSIS — why the rows still unstated after L5 cannot be recovered:")
    res = A[A.n - A.L5_TRANSITIVE > 0]
    l4_by_file = {r.file: (r.l4_vals.split("|") if isinstance(r.l4_vals, str) and r.l4_vals
                           else []) for r in A.itertuples()}
    for _, r in res.iterrows():
        st = rowlab[r.file]
        lab = st.get("l5", st["l4"])
        need = lab.isna()
        hdr = st["d"].columns.tolist()
        srcc = [c for c in hdr if c.lower().strip("_") in SRC_COLS]
        say(f"    {r.file}  ({int(need.sum()):,} rows unrecovered of {r.n:,})")
        if not srcc:
            say("        no source-pointer column at all — the row cannot name its own origin.")
            continue
        vals = st["d"].loc[need, srcc[0]].astype(str)
        cat = {"source not a committed five-margin block": 0,
               "source is MULTI-panel (row-level link missing)": 0,
               "source single-panel but unlabelled": 0}
        for v, cnt in vals.value_counts().items():
            cands = l4_by_file.get(v.strip())
            if cands is None:
                cat["source not a committed five-margin block"] += int(cnt)
            elif len(cands) > 1:
                cat["source is MULTI-panel (row-level link missing)"] += int(cnt)
            else:
                cat["source single-panel but unlabelled"] += int(cnt)
        for k, v in cat.items():
            say(f"        {k:<48} {v:>8,}  ({v / max(1, int(need.sum())):.3f})")
        say(f"        distinct source files pointed at: {vals.nunique()}; the pointer is a FILE "
            f"name with no row id, so even a single-panel source cannot be joined row-wise "
            f"when it is multi-panel.")

    PR = part_prose(stems)
    if not PR.empty:
        PR.to_csv(OUT / f"{STEM}.prose.csv", index=False)

    S, degen = null_scales(panels)
    if degen >= 1e-12:
        say("\n*** G5 FAILED — the null is not measuring draw dispersion. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return 1
    S.to_csv(OUT / f"{STEM}.scales.csv")

    PAY = part_payoff(A, rowlab, S)
    PAY.to_csv(OUT / f"{STEM}.payoff.csv", index=False)

    # ================================================================== fresh grid
    say("\n" + "=" * 100)
    say(f"LEG 2 — FRESH GRID ({len(PANELS)} panels x {len(BOOKS)} books x {len(GROSSES)} grosses "
        f"x {len(BANDS)} bands, read at {len(RUNGS)} rungs)")
    say("=" * 100)
    G, SER, V2, BAR, BARI = [], {}, {}, {}, {}
    for pk in PANELS:
        px = panels[pk]
        cols = investable(pk, px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        b = bars_of(spy)
        bi = bars_of(spy, "is")
        BAR[pk], BARI[pk] = b, bi
        v2w = rules_v2_weights(px[cols]).reindex(columns=px.columns).fillna(0.0)
        rv, tv = fast_bt(px, v2w)
        V2[pk] = {c: (rv - tv * c / 1e4).loc[start:] for c in RUNGS}
        for book in BOOKS:
            for g in GROSSES:
                W0 = book_weights(px, cols, book, g)
                for bd in BANDS:
                    W = W0.where(band_state(px[cols], bd).reindex(
                        columns=px.columns).fillna(False), 0.0) if bd > 0 else W0
                    r0, t0 = fast_bt(px, W)
                    SER[(pk, book, g, bd)] = (r0, t0, start)
                    for c in RUNGS:
                        r = (r0 - t0 * c / 1e4).loc[start:]
                        m = metrics(r)
                        h1, h2 = halves(r)
                        mg = margins(r, b)
                        mgi = margins(r.loc[:IS_END], bi, "is")
                        base = V2[pk][c]
                        G.append(dict(panel=REC[pk], book=book, gross=g, band=bd, cost=c,
                                      CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                      H1=h1, H2=h2,
                                      IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                      OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                      **{f"m_{k}": v for k, v in mg.items()},
                                      **{f"IS_m_{k}": v for k, v in mgi.items() if k != "OOS"},
                                      pass4b=bool(min(mg.values()) > 0),
                                      pass4a=pass4a(r, base)))
        say(f"  {REC[pk]:<9} priced {len(BOOKS) * len(GROSSES) * len(BANDS)} arms")
    G = pd.DataFrame(G)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"  {len(G)} arm-rows written "
        f"({len(SER)} simulations x {len(RUNGS)} rungs).")

    say("\n" + "-" * 100)
    say("KEEP PATHS (PROTOCOL 4) — both evaluated on EVERY arm-row")
    say("-" * 100)
    say(f"  4a (vs live RULES v2, cost-matched): {int(G.pass4a.sum())} / {len(G)}")
    say(f"  4b (vs SPY, all five bars)         : {int(G.pass4b.sum())} / {len(G)}")
    say(f"  BOTH                               : {int((G.pass4a & G.pass4b).sum())} / {len(G)}")
    for c in RUNGS:
        s = G[G.cost == c]
        say(f"    @{c:>4.0f} bps: 4a {int(s.pass4a.sum()):>4}  4b {int(s.pass4b.sum()):>4}  "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>4}   of {len(s)}")
    kp = G.groupby(["panel", "book"]).agg(n=("cost", "size"), p4a=("pass4a", "sum"),
                                          p4b=("pass4b", "sum"))
    say(kp.to_string())
    kp.to_csv(OUT / f"{STEM}.keeppaths.csv")
    say("\n  GROSS-LADDER CONTROL (idea 311: a 4b pass that is not swept in gross is not a "
        "book).  Every (panel, book, band) cell at 10 bps, read at all three grosses:")
    t = G[G.cost == 10.0].pivot_table(index=["panel", "book", "band"], columns="gross",
                                      values="pass4b")
    npass = t.sum(axis=1)
    say(f"    cells with at least one 4b pass: {int((npass > 0).sum())} of {len(t)};  "
        f"passing at ALL {len(GROSSES)} grosses: {int((npass == len(GROSSES)).sum())};  "
        f"at exactly one: {int((npass == 1).sum())}")
    sh = G[G.cost == 10.0].pivot_table(index=["panel", "book", "band"], columns="gross",
                                       values="Sharpe")
    say(f"    max |Sharpe(g=1.00) - Sharpe(g=0.50)| over the same cells: "
        f"{float((sh[1.00] - sh[0.50]).abs().max()):.4f}  — the ladder moves the 4b CAGR floor "
        f"and DD cap, not the risk-adjusted number.")

    # ================================================================== rule 8
    say("\n" + "-" * 100)
    say("RULE 8 (PROTOCOL 8) — (book, gross, band) chosen on 2009-2016 ONLY, 2017-2026 read once")
    say("-" * 100)
    say("  Four pre-registered selectors.  S1/S2/S3 are the QUESTION as a selector: S1 needs NO")
    say("  panel stamp (raw binding margin), S2 divides each margin by the arm's OWN panel-noise")
    say("  scale (needs the stamp), S3 divides by ANOTHER panel's scale (the mis-stamped read).")
    sd = {p: S.loc[p, [f"sd_{b}" for b in BARS]].values for p in S.index}
    WRONG = {"U56": "B136", "B136": "U56", "SMALL439": "BSTK100", "BSTK100": "SMALL439"}
    ISB = ["H1", "H2", "DD", "CAGR"]                     # the four IS-computable 4b bars
    wf = []
    for pk in PANELS:
        rk = REC[pk]
        px = panels[pk]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_o = spy.loc[OOS_START:]
        mo = metrics(spy_o)
        bo = dict(s1=metrics(spy_o.iloc[:len(spy_o) // 2])["Sharpe"],
                  s2=metrics(spy_o.iloc[len(spy_o) // 2:])["Sharpe"],
                  sdd=mo["MaxDD"], scagr=mo["CAGR"], soos=mo["Sharpe"])
        own = np.array([sd[rk][BARS.index(b)] for b in ISB])
        wrg = np.array([sd[WRONG[rk]][BARS.index(b)] for b in ISB])
        for c in RUNGS:
            sub = G[(G.panel == rk) & (G.cost == c)].copy()
            M = sub[[f"IS_m_{b}" for b in ISB]].values
            sub["bind_raw"] = M.min(axis=1)
            sub["bind_own"] = (M / own).min(axis=1)
            sub["bind_wrong"] = (M / wrg).min(axis=1)
            picks = {"S0_ISsharpe": sub.loc[sub.IS_Sharpe.idxmax()],
                     "S1_RAWbind": sub.loc[sub.bind_raw.idxmax()],
                     "S2_OWNpanel": sub.loc[sub.bind_own.idxmax()],
                     "S3_MISstamped": sub.loc[sub.bind_wrong.idxmax()]}
            for sn, p in picks.items():
                r0, t0, st0 = SER[(pk, p.book, float(p.gross), float(p.band))]
                r = (r0 - t0 * c / 1e4).loc[st0:].loc[OOS_START:]
                m = metrics(r)
                h = len(r) // 2
                o4b = dict(H1=metrics(r.iloc[:h])["Sharpe"] - bo["s1"],
                           H2=metrics(r.iloc[h:])["Sharpe"] - bo["s2"],
                           OOS=m["Sharpe"] - bo["soos"],
                           DD=DELTA * abs(bo["sdd"]) - abs(m["MaxDD"]),
                           CAGR=m["CAGR"] - PHI * bo["scagr"])
                v2o = V2[pk][c].loc[OOS_START:]
                mv = metrics(v2o)
                wf.append(dict(panel=rk, cost=c, selector=sn, book=p.book,
                               gross=float(p.gross), band=float(p.band),
                               OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                               SPY_CAGR=mo["CAGR"], SPY_Sharpe=mo["Sharpe"], SPY_MaxDD=mo["MaxDD"],
                               V2_CAGR=mv["CAGR"], V2_Sharpe=mv["Sharpe"], V2_MaxDD=mv["MaxDD"],
                               beats_SPY=bool(m["Sharpe"] > mo["Sharpe"]),
                               beats_V2=bool(m["Sharpe"] > mv["Sharpe"]),
                               OOS_4b=all(v > 0 for v in o4b.values()),
                               OOS_4a=pass4a(r, v2o)))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF.groupby("selector").agg(
        picks=("book", "size"), OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beats_SPY=("beats_SPY", "sum"),
        beats_V2=("beats_V2", "sum"), OOS_4b=("OOS_4b", "sum"), OOS_4a=("OOS_4a", "sum")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    say()
    for pk in PANELS:
        rk = REC[pk]
        s = WF[(WF.panel == rk) & (WF.cost == 10.0)]
        say(f"  {rk:<9} @10 bps   SPY OOS: CAGR {s.SPY_CAGR.iloc[0]:.2%}  Sharpe "
            f"{s.SPY_Sharpe.iloc[0]:.3f}  MaxDD {s.SPY_MaxDD.iloc[0]:.1%}   |   RULES v2 OOS: "
            f"CAGR {s.V2_CAGR.iloc[0]:.2%}  Sharpe {s.V2_Sharpe.iloc[0]:.3f}  "
            f"MaxDD {s.V2_MaxDD.iloc[0]:.1%}")
        for _, r in s.iterrows():
            say(f"        {r.selector:>14}: {r.book:<9} g{r.gross:.2f} b{r.band:.2f}  "
                f"OOS CAGR {r.OOS_CAGR:>7.2%}  Sharpe {r.OOS_Sharpe:>7.3f}  "
                f"MaxDD {r.OOS_MaxDD:>7.1%}  4b {int(r.OOS_4b)}  4a {int(r.OOS_4a)}")
    piv = WF[WF.selector.isin(["S1_RAWbind", "S2_OWNpanel", "S3_MISstamped"])].pivot_table(
        index=["panel", "cost"], columns="selector", values=["gross", "band"], aggfunc="first")
    same12 = ((piv[("gross", "S1_RAWbind")] == piv[("gross", "S2_OWNpanel")]) &
              (piv[("band", "S1_RAWbind")] == piv[("band", "S2_OWNpanel")]))
    same23 = ((piv[("gross", "S2_OWNpanel")] == piv[("gross", "S3_MISstamped")]) &
              (piv[("band", "S2_OWNpanel")] == piv[("band", "S3_MISstamped")]))
    bk = WF.pivot_table(index=["panel", "cost"], columns="selector", values="book",
                        aggfunc="first")
    same12 &= bk["S1_RAWbind"] == bk["S2_OWNpanel"]
    same23 &= bk["S2_OWNpanel"] == bk["S3_MISstamped"]
    say(f"\n  S1 (no stamp needed) vs S2 (own panel's noise): identical rule-8 pick in "
        f"{int(same12.sum())}/{len(same12)} cells ({same12.mean():.1%})")
    say(f"  S2 (correct stamp)   vs S3 (MIS-stamped)      : identical rule-8 pick in "
        f"{int(same23.sum())}/{len(same23)} cells ({same23.mean():.1%})")
    for sn in ("S1_RAWbind", "S2_OWNpanel", "S3_MISstamped"):
        s = WF[WF.selector == sn]
        say(f"    {sn:>14}: OOS Sharpe {s.OOS_Sharpe.mean():.4f}  CAGR {s.OOS_CAGR.mean():.2%}  "
            f"MaxDD {s.OOS_MaxDD.mean():.2%}  beats SPY {int(s.beats_SPY.sum())}/{len(s)}  "
            f"beats v2 {int(s.beats_V2.sum())}/{len(s)}  4b {int(s.OOS_4b.sum())}/{len(s)}  "
            f"4a {int(s.OOS_4a.sum())}/{len(s)}")

    say("\n" + "=" * 100)
    say(f"done in {time.time() - T0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
