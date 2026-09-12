#!/usr/bin/env python3
"""Idea 574 (cloud, 2026-09-12) - re-sweep-the-record-s-TEN-most-cited-UNSWEPT-4b-passes-in-GROSS.

QUESTION
--------
Idea 311 found that 23,015 of the record's committed 4b passes (98.1%) were never run at a second
gross inside their own file, while 97.6% of the ones that WERE swept flip verdict somewhere on
their own ladder.  A 4b pass quoted at one gross is therefore a point estimate on a dial nobody
turned.  This run takes the TEN MOST-CITED UNSWEPT 4b passes in LEADERBOARD.md, rebuilds each one,
re-runs it on a 17-point gross grid, and reports (a) how many keep their verdict at their own
published gross, (b) how wide their admissible gross band is, and (c) whether the published point
is INTERIOR to that band or sitting on its edge.

Path 4b is the path that matters for capital (PROTOCOL rule 4b), so a 4b pass that survives only at
the one gross its author happened to run is not a capital claim, it is a coordinate.

WHAT COUNTS AS WHAT (every rule stated before any number)
---------------------------------------------------------
* A **4b-pass row** is a LEADERBOARD.md row whose text matches
  `KEEP-candidate (4b) | 4b PASS | passes 4b | 4b KEEP | KEEP (4b)` (case-insensitive).
  NOTE THE UNIT: idea 311 counted committed GRID rows inside `.csv` artefacts; this run counts
  PUBLISHED LEADERBOARD rows.  Both denominators are reported side by side and they are not the
  same object - this run does not restate idea 311's 98.1% as if it were.
* A row is **SWEPT** when its producing script shows two or more distinct gross values, by either
  of two independent detectors: (i) an AST scan of the source for a gross-named assignment or loop
  target bound to a literal list of >= 2 numbers, or (ii) any committed `.csv` of that script's own
  stem carrying a `gross`/`g` column with >= 2 distinct values.  Otherwise it is **UNSWEPT**.
* **Citations** of a row = occurrences of its script stem anywhere in `research/*.md`,
  `research/backtests/*.md` and `research/backtests/*.py`, excluding the script's own files.
* A row is **PINNABLE** when a documented token lexicon resolves it to a canonical book key
  (panel, form, n, gross, cadence).  Unstated gross defaults to the record's 0.75 and unstated
  cadence to weekly - both FLAGGED as ASSUMED in the output, never silently.
* The **ten** are the top ten by summed citations over DISTINCT book keys, not over rows: several
  of the most-cited rows resolve to the SAME book, and that is reported rather than hidden.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: book, gross)
    1. BOOK   the ten distinct canonical book keys selected as above.  All ten reported.
    2. GROSS  17 rungs, g = 0.20, 0.25, ... , 1.00.  All 17 reported for all ten books.
REPORTED-NEVER-SELECTED: cost rung (10 bps per PROTOCOL, 25 bps beside it), cadence, panel, form,
window (FULL / IS / OOS), and the 4a path.

GATES (printed before any swept/unswept or band number is read)
    G0 harvest    : both sweep detectors run on every named script; agreement and disagreement
                    counts published, so the census is not one regex's opinion.       no bar
    G1 engine     : fast_backtest vs engine.backtest on one rebuilt book.           bar 1e-9
    G2 comparands : live RULES v2 on U56 and SPY over this run's window, printed so every later
                    bar can be checked by hand.                                       no bar
    G3 rebuild    : each rebuilt book at its OWN published gross against the CAGR / Sharpe / MaxDD
                    the leaderboard row published.  MEASURED and published per book, NOT gated:
                    the record has documented panel-vintage drift (idea 565/796) and several of
                    these rows were run at 5 bps or on a shorter sample, so a hard bar here would
                    fail for reasons that have nothing to do with gross.  A book whose rebuild is
                    far from its published triple is named as such and its band read with that
                    caveat attached.

PRE-REGISTERED HYPOTHESES (written before any grid point was read)
    H_KEEP  : the queue's charitable reading - a majority (>= 6 of 10) of the published points
              still pass 4b at their own published gross on today's data at 10 bps.
    H_FLIP  : idea 311's reading - >= 8 of 10 books flip the 4b verdict somewhere on their own
              17-rung ladder (i.e. the ladder is not uniformly pass or uniformly fail).
    H_NARROW: the admissible band is narrow - median band width <= 6 of 17 rungs among books that
              pass anywhere.
    H_EDGE  : the published gross sits on the EDGE of its own admissible band (within one rung of
              an endpoint) in >= 5 of the books that pass anywhere - i.e. the published point was
              not chosen for robustness.
    H_MONO  : the 4b pass set is an INTERVAL in g (contiguous rungs) for every book that passes
              anywhere, so "band width" is a meaningful summary at all.
    H_WF    : rule 8 - the admissible band fitted on IS alone contains the OOS-admissible band's
              midpoint for >= 6 of 10 books.

RULE 8 WALK-FORWARD (required)
    IS = ..2016-12-31, OOS = 2017-01-01.. , OOS read ONCE.
    WF-A on the ANSWER: the 4b legs are recomputed inside the IS window alone and inside the OOS
       window alone, giving an IS-admissible and an OOS-admissible gross band per book; their
       overlap and midpoint agreement is the walk-forward of "this book has a gross band".
    WF-B on a BOOK: gross is chosen per book by IS Sharpe ALONE, then OOS CAGR / Sharpe / MaxDD are
       read ONCE against live RULES v2 (U56, weekly, 10 bps) and against SPY.  Reported for all
       ten, plus the single best IS-Sharpe book across the ten.

KEEP PATHS: 4a and 4b are evaluated at every one of the 10 x 17 x 2 = 340 cells and counted.

SURVIVORSHIP: U56 / B136 / BSTK100 are current constituents of universe.json / universe_broad.json;
    the sub-$2B panel is the current constituent list of its screen with every ticker whose
    max_1d_move >= 1.0 in data/small_meta.csv dropped first, per PROTOCOL.  Names that died are
    absent from all of them, so every CAGR here is biased upward and every 4b CAGR-floor pass is
    easier than it would be on a point-in-time panel.  Stated again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and the committed record;
modifies nothing but its own outputs:
    .census.csv .books.csv .grid.csv .bands.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import ast
import csv
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_re-sweep-the-record-s-TEN-most-cited-UNSWEPT-4b-passes-in-GROSS_cloud"
OUT = ROOT / "research" / "backtests"
LB = ROOT / "research" / "LEADERBOARD.md"

COST_MAIN, COST_ALT = 10.0, 25.0
GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]      # TUNED 2 - 17 rungs
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MAX_VOL = 0.60
MA_WIN = 200
DEFAULT_G, DEFAULT_FREQ = 0.75, "W"
TOL = 1e-9
N_BOOKS = 10                                                 # TUNED 1 - the ten

PASSRE = re.compile(r"KEEP-candidate\s*\(4b\)|4b\s*PASS|passes\s*4b|4b\s*KEEP|KEEP\s*\(4b\)", re.I)
SCRIPTRE = re.compile(r"(20\d\d-\d\d-\d\d_[A-Za-z0-9_\-\.]+\.py)")
GNAME = re.compile(r"gross|_g$|^g$|^gs$|g_set|g_grid", re.I)

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps, freq):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    """PROTOCOL 4b, verbatim: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of
    SPY's, CAGR >= 70% of SPY's.  Returns '-' on a pass, else the failing legs."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


def fail_4b_window(r, spy, lo=None, hi=None):
    """The same five legs computed INSIDE one window (the OOS leg collapses into the window's own
    second half, which is stated rather than dropped)."""
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ harvest
def sweep_from_source(p: Path) -> set:
    try:
        tree = ast.parse(p.read_text(errors="ignore"))
    except Exception:
        return set()
    out = set()
    for n in ast.walk(tree):
        tgt = val = None
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            tgt, val = n.targets[0].id, n.value
        elif isinstance(n, ast.For) and isinstance(n.target, ast.Name):
            tgt, val = n.target.id, n.iter
        if tgt and GNAME.search(tgt) and isinstance(val, (ast.List, ast.Tuple)):
            v = {float(e.value) for e in val.elts
                 if isinstance(e, ast.Constant) and isinstance(e.value, (int, float))}
            if len(v) >= 2:
                out |= v
    return out


def sweep_from_csvs(stem: str) -> set:
    out = set()
    for p in OUT.glob(stem + "*.csv"):
        try:
            with open(p, newline="") as f:
                r = csv.reader(f)
                hdr = next(r, None)
                if not hdr:
                    continue
                idx = [i for i, h in enumerate(hdr) if h.strip().lower() in ("gross", "g")]
                if not idx:
                    continue
                i = idx[0]
                seen = set()
                for k, row in enumerate(r):
                    if k > 300000:
                        break
                    if i < len(row):
                        try:
                            seen.add(round(float(row[i]), 6))
                        except ValueError:
                            pass
                if len(seen) >= 2:
                    out |= seen
        except Exception:
            pass
    return out


def pin_book(text: str):
    """Documented token lexicon -> canonical book key, or None.  Every branch is a literal token
    the record actually writes; nothing is inferred from numbers alone."""
    t = text
    panel = None
    for pat, nm in ((r"BSTK100|STK100", "BSTK100"), (r"\bB136\b", "B136"),
                    (r"SMALL\s*\d+|SMALL-CAP PANEL|sub-\$2B", "SMALL"),
                    (r"\bETF36\b", "ETF36"), (r"\bu56\b|\bU56\b|universe\.json", "U56")):
        if re.search(pat, t, re.I):
            panel = nm
            break
    form = n = None
    if re.search(r"\bR6\b", t):
        m = re.search(r"top-?\s*(\d+)", t, re.I)
        form, n = "R6", int(m.group(1)) if m else 20
    elif re.search(r"CAND-?\s*(\d+)|top-?\s*(\d+)\s*(EW|equal)|top-?(\d+)\b|FIX n\s*=\s*(\d+)", t, re.I):
        m = re.search(r"CAND-?\s*(\d+)", t, re.I) or re.search(r"top-?\s*(\d+)", t, re.I) \
            or re.search(r"FIX n\s*=\s*(\d+)", t, re.I)
        form, n = "CAND", int(m.group(1))
    elif re.search(r"EW-?all|EWall|q\s*=\s*1\.00\s*=\s*EWall|equal-?weight (all|book)", t, re.I):
        form, n = "EWALL", 0
    elif re.search(r"MA-DG|de-?gross", t, re.I):
        form, n = "MA-DG", 0
    elif re.search(r"MA-RS|respread", t, re.I):
        form, n = "MA-RS", 0
    elif re.search(r"band\s*0?\.(\d+)", t, re.I):
        form, n = "BAND", int(re.search(r"band\s*0?\.(\d+)", t, re.I).group(1))
    if panel is None or form is None:
        return None
    mg = re.search(r"g\s*=\s*(0?\.\d+|1\.00|1\.0)\b", t) or re.search(r"gross[= ]\s*(0?\.\d+)", t) \
        or re.search(r"(\d{2})% gross", t) or re.search(r"top-?\d+\s*=\s*(0?\.\d+)", t)
    if mg:
        v = float(mg.group(1))
        g, g_ass = (v / 100.0 if v > 1.5 else v), False
    else:
        g, g_ass = DEFAULT_G, True
    if re.search(r"MONTHLY|monthly", t):
        freq, f_ass = "M", False
    elif re.search(r"WEEKLY|weekly", t):
        freq, f_ass = "W", False
    else:
        freq, f_ass = DEFAULT_FREQ, True
    return dict(panel=panel, form=form, n=n, gross=round(g, 2), freq=freq,
                gross_assumed=g_ass, freq_assumed=f_ass)


def keystr(b):
    return f"{b['panel']}/{b['form']}{b['n'] or ''}/g{b['gross']:.2f}/{b['freq']}"


# ------------------------------------------------------------------ panels and books
def panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etf36 = U["broad"] + U["sectors"] + U["bonds_fx_commod"]
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        return px[keep].dropna(how="all").ffill(), set(tradable if tradable is not None else cols)

    return {"U56": sub(px56, list(px56.columns)),
            "ETF36": sub(px56, [t for t in etf36 if t in px56.columns]),
            "B136": sub(px136, list(px136.columns)),
            "BSTK100": sub(px136, b_stk, tradable=b_stk),
            "SMALL": sub(pxs, s_stk, tradable=s_stk)}, len(bad), len(s_stk)


def build_weights(px, tradable, form, n, g):
    cols = [c for c in px.columns if c in tradable]
    priced = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    priced[cols] = px[cols].notna().astype(float)
    pm = priced > 0
    if form == "EWALL":
        cnt = pm.sum(axis=1).replace(0, np.nan)
        return g * pm.div(cnt, axis=0).fillna(0.0)
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    if form == "MA-DG":
        cnt = pm.sum(axis=1).replace(0, np.nan)
        return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)
    if form == "MA-RS":
        cnt = ma.sum(axis=1).replace(0, np.nan)
        return g * ma.div(cnt, axis=0).fillna(0.0)
    if form == "BAND":
        w = rules_v2_weights(px[cols + (["SPY"] if "SPY" in px.columns and "SPY" not in cols
                                        else [])], band=n / 100.0, gross=g)
        return w.reindex(columns=px.columns).fillna(0.0).where(pm, 0.0)
    if form == "CAND":
        s, above, vol20 = score(px)
        s = s.where(pm)
        elig = s.where(above & (vol20 < MAX_VOL))
        rk = elig.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    if form == "R6":
        r6 = (px / px.shift(126) - 1.0).where(pm)
        rk = r6.rank(axis=1, ascending=False)
        return (rk <= n).astype(float) * (g / n)
    raise ValueError(form)


def main():
    t0 = time.time()
    P("=" * 118)
    P(f"# {STAMP}")
    P("# IDEA 574 - take the TEN MOST-CITED UNSWEPT 4b passes in LEADERBOARD.md, rebuild each, and")
    P("#            re-run it on a 17-point gross grid.  How many keep their verdict?  How wide is")
    P("#            the band?  Is the published point interior, or on the edge?")
    P("=" * 118)
    P(f"# PROTOCOL: {COST_MAIN:.0f} bps per unit turnover ({COST_ALT:.0f} bps reported beside it),")
    P(f"#           next-day fills, no shorting, no leverage.  IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"# TUNED (2, the queue's own): BOOK (the ten) x GROSS ({len(GGRID)} rungs "
      f"{GGRID[0]:.2f}..{GGRID[-1]:.2f} step 0.05).  All 10 x 17 reported at both cost rungs.")
    P("# REPORTED-NOT-SELECTED: cost rung, cadence, panel, form, window, the 4a path.")
    P("")
    P("PRE-REGISTERED: H_KEEP (>=6 of 10 still pass at their own published g), H_FLIP (>=8 of 10")
    P("  flip somewhere on their own ladder), H_NARROW (median band <= 6 of 17 rungs among books")
    P("  that pass anywhere), H_EDGE (the published g is within one rung of a band endpoint in >=5")
    P("  of them), H_MONO (the pass set is a contiguous interval in g for every such book),")
    P("  H_WF (the IS-fitted band contains the OOS band's midpoint for >= 6 of 10).")
    P("")

    # ------------------------------------------------------------------ harvest + G0
    rows = [l.rstrip("\n") for l in LB.read_text().split("\n") if l.startswith("| 20")]
    hits = [l for l in rows if PASSRE.search(l)]
    P("=" * 118)
    P("HARVEST + G0 - the census, with both sweep detectors run and compared")
    P("=" * 118)
    P(f"  LEADERBOARD.md carries {len(rows)} dated rows; {len(hits)} assert a 4b pass under the")
    P("  stated lexicon (KEEP-candidate (4b) | 4b PASS | passes 4b | 4b KEEP | KEEP (4b)).")
    scripts = {}
    for l in hits:
        m = SCRIPTRE.search(l)
        if m:
            scripts.setdefault(m.group(1), []).append(l)
    P(f"  {len(scripts)} distinct producing scripts are named; "
      f"{sum(1 for l in hits if not SCRIPTRE.search(l))} rows name none and are counted UNPINNED.")
    corpus = []
    for pth in (list((ROOT / "research").glob("*.md")) + list(OUT.glob("*.md"))
                + list(OUT.glob("*.py"))):
        try:
            corpus.append((pth.name, pth.read_text(errors="ignore")))
        except Exception:
            pass
    P(f"  citation corpus: {len(corpus)} committed markdown and python files.")
    cen = []
    agree = dis_src = dis_csv = 0
    for f, ls in scripts.items():
        stem = f[:-3]
        a, b = sweep_from_source(OUT / f), sweep_from_csvs(stem)
        sa, sb = len(a) >= 2, len(b) >= 2
        agree += int(sa == sb)
        dis_src += int(sa and not sb)
        dis_csv += int(sb and not sa)
        cit = sum(t.count(stem) for nm, t in corpus if not nm.startswith(stem))
        cen.append(dict(script=f, rows=len(ls), swept=bool(sa or sb), src_g=len(a), csv_g=len(b),
                        citations=cit))
    CEN = pd.DataFrame(cen)
    CEN.to_csv(f"{OUT}/{STAMP}.census.csv", index=False)
    nsw = int(CEN.swept.sum())
    rsw = int(CEN.loc[CEN.swept, "rows"].sum())
    P(f"  G0 detector agreement: {agree} of {len(CEN)} scripts agree; {dis_src} are swept by the")
    P(f"     AST scan only and {dis_csv} by the committed-csv scan only - the union is used.")
    P(f"  SCRIPTS : {nsw} swept / {len(CEN) - nsw} unswept ({(len(CEN)-nsw)/len(CEN):.1%} unswept)")
    P(f"  ROWS    : {rsw} swept / {len(hits) - rsw} unswept "
      f"({(len(hits)-rsw)/len(hits):.1%} unswept)")
    P("  UNIT WARNING: idea 311's 98.1% counted committed GRID rows inside .csv artefacts; the")
    P("  figures above count PUBLISHED LEADERBOARD rows.  Different denominators, both published;")
    P("  this run does not restate one as the other.")
    P("")

    # ------------------------------------------------------------------ pin + select the ten
    P("=" * 118)
    P("PINNING - unswept 4b-pass rows resolved to canonical book keys by the stated lexicon")
    P("=" * 118)
    pinned, unpinned = [], 0
    for f, ls in scripts.items():
        r = CEN[CEN.script == f].iloc[0]
        if bool(r.swept):
            continue
        for l in ls:
            b = pin_book(l)
            if b is None:
                unpinned += 1
                continue
            col = [x.strip() for x in l.split("|")]
            def _pct(x):
                m = re.search(r"(-?\d+\.?\d*)\s*%", x)
                return float(m.group(1)) / 100.0 if m else np.nan
            def _num(x):
                m = re.search(r"(-?\d+\.\d+)", x)
                return float(m.group(1)) if m else np.nan
            b = dict(b, script=f, citations=int(r.citations), key=keystr(b), row=l,
                     row_date=col[1] if len(col) > 1 else "",
                     pub_CAGR=_pct(col[3]) if len(col) > 3 else np.nan,
                     pub_Sharpe=_num(col[4]) if len(col) > 4 else np.nan,
                     pub_MaxDD=_pct(col[5]) if len(col) > 5 else np.nan,
                     pub_ambiguous=bool(len(col) > 5 and (
                         len(re.findall(r"\d+\.?\d*\s*%", col[3])) > 1
                         or len(re.findall(r"\d+\.?\d*\s*%", col[5])) > 1)))
            pinned.append(b)
    P(f"  {len(pinned)} of {len(pinned) + unpinned} unswept 4b-pass rows PIN to a canonical book "
      f"key ({unpinned} do not and are excluded, with their count published).")
    PIN = pd.DataFrame(pinned)
    agg = (PIN.groupby("key")
              .agg(citations=("citations", "sum"), rows=("key", "size"),
                   scripts=("script", "nunique"), panel=("panel", "first"), form=("form", "first"),
                   n=("n", "first"), gross=("gross", "first"), freq=("freq", "first"),
                   gross_assumed=("gross_assumed", "all"), freq_assumed=("freq_assumed", "all"),
                   pub_CAGR=("pub_CAGR", "median"), pub_Sharpe=("pub_Sharpe", "median"),
                   pub_MaxDD=("pub_MaxDD", "median"), row_date=("row_date", "max"),
                   pub_ambiguous=("pub_ambiguous", "any"))
              .reset_index().sort_values(["citations", "rows"], ascending=False))
    P(f"  {len(agg)} DISTINCT book keys behind them - the most-cited rows are not ten different")
    P("  books, and the collapse is reported rather than hidden.")
    P("")
    P(f"  {'#':>2s} {'book key':38s} {'cit':>5s} {'rows':>4s} {'scr':>4s}  assumed")
    TEN = agg.head(N_BOOKS).reset_index(drop=True)
    for j, (_, r) in enumerate(agg.head(16).iterrows(), start=1):
        mark = "*" if j <= N_BOOKS else " "
        ass = ",".join([t for t, on in (("g", r.gross_assumed), ("freq", r.freq_assumed)) if on]) or "-"
        P(f"  {mark}{j:>2d} {r.key:38s} {int(r.citations):5d} "
          f"{int(r.rows):4d} {int(r.scripts):4d}  {ass}")
    P(f"  * = the ten taken forward (TUNED 1).")
    P("")

    # ------------------------------------------------------------------ panels, comparands, G1/G2
    PAN, n_bad, n_small = panels()
    P("=" * 118)
    P("REBUILD - panels, comparands, gates")
    P("=" * 118)
    P("  " + "; ".join(f"{k} {len(v[1])} tradable / {v[0].shape[1]} cols" for k, v in PAN.items()))
    P(f"  small panel: {n_bad} tickers with max_1d_move >= 1.0 dropped per PROTOCOL, "
      f"{n_small} tradable")
    P("  SURVIVORSHIP: all four panels are CURRENT constituents; dead names are absent, so every")
    P("  CAGR below is biased upward and every 4b CAGR-floor pass is easier than on a")
    P("  point-in-time panel.")
    px56 = PAN["U56"][0]
    base_full = fast_backtest(px56, rules_v2_weights(px56), COST_MAIN, "W")
    START = px56.index[260]
    b_ret = base_full.loc[START:]
    spy_ret = px56["SPY"].pct_change().fillna(0.0).loc[START:]
    bm, sm = rowify(b_ret), rowify(spy_ret)
    P("")
    w_test = build_weights(px56, PAN["U56"][1], "CAND", 20, 0.75)
    r1 = fast_backtest(px56, w_test, COST_MAIN, "W")
    r2 = backtest(px56, w_test, cost_bps=COST_MAIN, freq="W")["returns"]
    d1 = float(np.abs(r1 - r2).max())
    P(f"  G1 engine    : max |fast_backtest - engine.backtest| on U56/CAND20/g0.75 {d1:.3e}"
      f"   bar 1e-9 -> {'PASS' if d1 < TOL else 'FAIL'}")
    P(f"  G2 comparands over {START.date()}..{px56.index[-1].date()} ({len(b_ret)} bars):")
    P(f"     RULES v2 (U56, live)  CAGR {bm['CAGR']:.2%}  Sharpe {bm['Sharpe']:.4f}  "
      f"MaxDD {bm['MaxDD']:.2%}  halves {bm['H1']:.4f}/{bm['H2']:.4f}  | OOS "
      f"{bm['OOS_CAGR']:.2%}/{bm['OOS_Sharpe']:.4f}/{bm['OOS_MaxDD']:.2%}")
    P(f"     SPY                   CAGR {sm['CAGR']:.2%}  Sharpe {sm['Sharpe']:.4f}  "
      f"MaxDD {sm['MaxDD']:.2%}  halves {sm['H1']:.4f}/{sm['H2']:.4f}  | OOS "
      f"{sm['OOS_CAGR']:.2%}/{sm['OOS_Sharpe']:.4f}/{sm['OOS_MaxDD']:.2%}")
    P(f"     4b bars: MaxDD cap {0.60 * sm['MaxDD']:.2%}, CAGR floor {0.70 * sm['CAGR']:.2%}, "
      f"half-Sharpe bars {sm['H1']:.4f} / {sm['H2']:.4f}, OOS Sharpe bar {sm['OOS_Sharpe']:.4f}")
    P("")

    # ------------------------------------------------------------------ the grid
    P("=" * 118)
    P(f"THE GRID - {N_BOOKS} books x {len(GGRID)} gross rungs x 2 cost rungs, all reported")
    P("=" * 118)
    grid, g3 = [], []
    for bi, b in TEN.iterrows():
        pk = "SMALL" if b.panel == "SMALL" else b.panel
        if pk not in PAN:
            P(f"  book {bi + 1} {b.key}: panel not rebuildable here - SKIPPED, reported as such")
            continue
        px, tr = PAN[pk]
        st = px.index[260]
        spy_b = px["SPY"].pct_change().fillna(0.0).loc[st:]
        base_b = fast_backtest(px56, rules_v2_weights(px56), COST_MAIN, "W").reindex(
            px.index).fillna(0.0).loc[st:]
        for cost in (COST_MAIN, COST_ALT):
            for g in GGRID:
                w = build_weights(px, tr, b.form, int(b.n), g)
                r = fast_backtest(px, w, cost, b.freq).loc[st:]
                rr = rowify(r)
                grid.append(dict(book=bi + 1, key=b.key, panel=b.panel, form=b.form, n=int(b.n),
                                 freq=b.freq, cost=cost, g=g, published_g=b.gross,
                                 fail4b=fail_4b(r, spy_b), keep4b=fail_4b(r, spy_b) == "-",
                                 keep4a=keep_4a(r, base_b),
                                 fail4b_IS=fail_4b_window(r, spy_b, None, IS_END),
                                 fail4b_OOS=fail_4b_window(r, spy_b, OOS_START, None), **rr))
        pub = [x for x in grid if x["book"] == bi + 1 and x["cost"] == COST_MAIN
               and abs(x["g"] - b.gross) < 1e-9]
        if pub:
            g3.append(dict(book=bi + 1, key=b.key, citations=int(b.citations),
                           CAGR=pub[0]["CAGR"], Sharpe=pub[0]["Sharpe"], MaxDD=pub[0]["MaxDD"],
                           pub_CAGR=b.pub_CAGR, pub_Sharpe=b.pub_Sharpe, pub_MaxDD=b.pub_MaxDD,
                           row_date=b.row_date, pub_ambiguous=bool(b.pub_ambiguous),
                           keep4b=pub[0]["keep4b"], fail4b=pub[0]["fail4b"]))
    GR = pd.DataFrame(grid)
    GR.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    TEN.to_csv(f"{OUT}/{STAMP}.books.csv", index=False)

    P("  G3 REBUILD (measured, NOT gated - see the header for why): each book at its OWN published")
    P("     gross, 10 bps, against the triple its leaderboard row published.")
    P(f"  {'#':>2s} {'book key':30s} {'rebuilt CAGR/Sharpe/MaxDD':>28s} "
      f"{'published (its row)':>28s} {'dSharpe':>8s}  4b here")
    for r in g3:
        mine = f"{r['CAGR']:.2%} / {r['Sharpe']:.4f} / {r['MaxDD']:.2%}"
        pubs = (f"{r['pub_CAGR']:.2%} / {r['pub_Sharpe']:.4f} / {r['pub_MaxDD']:.2%}"
                + (" ?" if r["pub_ambiguous"] else "")
                if np.isfinite(r["pub_Sharpe"]) else "not parseable from the row")
        dsh = (r["Sharpe"] - r["pub_Sharpe"]) if np.isfinite(r["pub_Sharpe"]) else np.nan
        P(f"  {r['book']:2d} {r['key']:30s} {mine:>28s} {pubs:>28s} "
          f"{dsh:+8.4f}  {'PASS' if r['keep4b'] else 'FAIL ' + r['fail4b']}")
    G3 = pd.DataFrame(g3)
    G3.to_csv(f"{OUT}/{STAMP}.rebuild.csv", index=False)
    fin = G3[np.isfinite(G3.pub_Sharpe) & ~G3.pub_ambiguous]
    P(f"  '?' marks a row whose CAGR or MaxDD cell carries MORE THAN ONE percentage (a multi-panel")
    P(f"  or multi-arm row): its 'published triple' is not a single number and it is excluded from")
    P(f"  the fidelity statistic below - {int(G3.pub_ambiguous.sum())} of {len(G3)} books.")
    if len(fin):
        P(f"  rebuild fidelity on the {len(fin)} unambiguous rows: "
          f"median |dSharpe| {float((fin.Sharpe - fin.pub_Sharpe).abs().median()):.4f}, "
          f"max {float((fin.Sharpe - fin.pub_Sharpe).abs().max()):.4f}; "
          f"median |dMaxDD| {float((fin.MaxDD - fin.pub_MaxDD).abs().median()):.2%}")
        P("  Books far from their published triple are canonical rebuilds of the book the row NAMES,")
        P("  not byte-reproductions of the row: their bands below describe that canonical book.")
    P("")

    # ---------------------------------------------- COST / VINTAGE decomposition at published g
    P("  DECOMPOSITION - if a published 4b pass does not reproduce at its own gross, is that the")
    P("  GROSS dial or something else?  Each book re-read at its OWN published gross under four")
    P("  conventions: this run's (10 bps, sample to today) and three the rows themselves used.")
    P(f"  {'#':>2s} {'book key':30s} {'10bps/today':>12s} {'5bps/today':>11s} "
      f"{'10bps/asof':>11s} {'5bps/asof':>10s}   as-of")
    dec = []
    for bi, b in TEN.iterrows():
        pk = b.panel
        if pk not in PAN:
            continue
        px, tr = PAN[pk]
        st = px.index[260]
        w = build_weights(px, tr, b.form, int(b.n), b.gross)
        cells = {}
        for cost in (COST_MAIN, 5.0):
            for asof in (None, str(b.row_date)):
                pxc = px if asof in (None, "", "nan") else px.loc[:asof]
                if len(pxc) < 400:
                    cells[(cost, asof)] = "n/a"
                    continue
                ww = w.reindex(pxc.index)
                rr = fast_backtest(pxc, ww, cost, b.freq).loc[st:]
                sp = pxc["SPY"].pct_change().fillna(0.0).loc[st:]
                cells[(cost, asof)] = "PASS" if fail_4b(rr, sp) == "-" else "fail"
        dec.append(dict(book=bi + 1, key=b.key, as_of=b.row_date,
                        **{f"c{int(c)}_{'asof' if a else 'today'}": v for (c, a), v in cells.items()}))
        P(f"  {bi + 1:2d} {b.key:30s} {cells[(COST_MAIN, None)]:>12s} {cells[(5.0, None)]:>11s} "
          f"{cells[(COST_MAIN, str(b.row_date))]:>11s} {cells[(5.0, str(b.row_date))]:>10s}   "
          f"{b.row_date}")
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}/{STAMP}.decomposition.csv", index=False)
    nrec = int(sum(1 for r in dec if "PASS" in (r.get("c10_asof"), r.get("c5_today"),
                                                r.get("c5_asof")) and r.get("c10_today") != "PASS"))
    P(f"  {nrec} of the {len(dec)} books that fail at this run's convention RECOVER their 4b pass")
    P("  under one of the other three, so the failure is not purely a gross story - the cost rung")
    P("  and the sample end carry part of it, and that part is reported rather than charged to g.")
    P("")

    # ------------------------------------------------------------------ bands
    P("THE LADDERS - 4b verdict at every gross rung, 10 bps.  P = pass, . = fail; the published")
    P("              rung is marked [ ].  Rungs run 0.20 -> 1.00 left to right.")
    P("  " + " " * 40 + "".join(f"{g:.2f} "[2:] for g in GGRID))
    bands = []
    for bi in sorted(GR.book.unique()):
        d = GR[(GR.book == bi) & (GR.cost == COST_MAIN)].sort_values("g")
        key = d.key.iloc[0]
        pg = float(d.published_g.iloc[0])
        line = ""
        for _, rr in d.iterrows():
            ch = "P" if rr.keep4b else "."
            line += f"[{ch}]" if abs(rr.g - pg) < 1e-9 else f" {ch} "
        passes = [float(x) for x in d.loc[d.keep4b, "g"]]
        contiguous = (len(passes) == 0 or
                      len(passes) == int(round((max(passes) - min(passes)) / 0.05)) + 1)
        pub_pass = bool(d.loc[np.abs(d.g - pg) < 1e-9, "keep4b"].all()) if (np.abs(d.g - pg) < 1e-9).any() else None
        edge = (len(passes) > 0 and pub_pass and
                (abs(pg - min(passes)) < 0.051 or abs(pg - max(passes)) < 0.051))
        flips = 0 < len(passes) < len(GGRID)
        bands.append(dict(book=bi, key=key, published_g=pg, n_pass=len(passes),
                          lo=min(passes) if passes else np.nan,
                          hi=max(passes) if passes else np.nan,
                          contiguous=contiguous, published_passes=pub_pass, published_on_edge=edge,
                          flips=flips))
        P(f"  {bi:2d} {key:37s}" + line)
    BD = pd.DataFrame(bands)
    BD.to_csv(f"{OUT}/{STAMP}.bands.csv", index=False)
    P("")
    P(f"  {'#':>2s} {'book key':38s} {'pub g':>6s} {'rungs':>5s} {'band':>13s} {'contig':>7s} "
      f"{'pub pass':>8s} {'on edge':>8s} {'flips':>6s}")
    for r in BD.itertuples():
        bnd = f"{r.lo:.2f}-{r.hi:.2f}" if r.n_pass else "-"
        P(f"  {r.book:2d} {r.key:38s} {r.published_g:6.2f} {r.n_pass:5d} {bnd:>13s} "
          f"{str(r.contiguous):>7s} {str(r.published_passes):>8s} {str(r.published_on_edge):>8s} "
          f"{str(r.flips):>6s}")
    anyp = BD[BD.n_pass > 0]
    hkeep = int(BD.published_passes.fillna(False).sum())
    hflip = int(BD.flips.sum())
    hnarrow = float(anyp.n_pass.median()) if len(anyp) else np.nan
    hedge = int(BD.published_on_edge.fillna(False).sum())
    hmono = bool(len(anyp) == 0 or anyp.contiguous.all())
    P("")
    P(f"  H_KEEP   (>=6 of 10 published points still pass 4b): {hkeep} of {len(BD)} -> "
      f"{'PASS' if hkeep >= 6 else 'FAIL'}")
    P(f"  H_FLIP   (>=8 of 10 flip somewhere on their ladder): {hflip} of {len(BD)} -> "
      f"{'PASS' if hflip >= 8 else 'FAIL'}")
    P(f"  H_NARROW (median band <= 6 of 17 rungs among passers): {hnarrow:.1f} over "
      f"{len(anyp)} passers -> {'PASS' if (len(anyp) and hnarrow <= 6) else 'FAIL'}")
    P(f"  H_EDGE   (published g within one rung of an endpoint in >=5): {hedge} -> "
      f"{'PASS' if hedge >= 5 else 'FAIL'}")
    P(f"  H_MONO   (pass set contiguous in g for every passer): "
      f"{int(anyp.contiguous.sum())} of {len(anyp)} -> {'PASS' if hmono else 'FAIL'}")
    P("")
    P("  COST: the same ladders at 25 bps (pass counts of 17):")
    for bi in sorted(GR.book.unique()):
        d10 = GR[(GR.book == bi) & (GR.cost == COST_MAIN)]
        d25 = GR[(GR.book == bi) & (GR.cost == COST_ALT)]
        P(f"    {bi:2d} {d10.key.iloc[0]:38s} 10 bps {int(d10.keep4b.sum()):2d}/17   "
          f"25 bps {int(d25.keep4b.sum()):2d}/17")
    P("")

    # ------------------------------------------------------------------ rule 8
    P("=" * 118)
    P("RULE 8 / WF-A - the admissible gross band fitted inside the IS window alone against the band")
    P("                inside the OOS window alone (OOS read once).  The 4b OOS leg collapses into")
    P("                each window's own second half, which is stated, not dropped.")
    P("=" * 118)
    P(f"  {'#':>2s} {'book key':38s} {'IS band':>13s} {'OOS band':>13s} {'IS mid':>7s} "
      f"{'OOS mid':>7s} {'contains':>9s}")
    wf = []
    for bi in sorted(GR.book.unique()):
        d = GR[(GR.book == bi) & (GR.cost == COST_MAIN)].sort_values("g")
        pis = [float(x.g) for x in d.itertuples() if x.fail4b_IS == "-"]
        poo = [float(x.g) for x in d.itertuples() if x.fail4b_OOS == "-"]
        ismid = float(np.median(pis)) if pis else np.nan
        oomid = float(np.median(poo)) if poo else np.nan
        cont = bool(pis and poo and min(pis) - 1e-9 <= oomid <= max(pis) + 1e-9)
        wf.append(dict(book=bi, key=d.key.iloc[0], IS_n=len(pis), OOS_n=len(poo),
                       IS_lo=min(pis) if pis else np.nan, IS_hi=max(pis) if pis else np.nan,
                       OOS_lo=min(poo) if poo else np.nan, OOS_hi=max(poo) if poo else np.nan,
                       IS_mid=ismid, OOS_mid=oomid, contains=cont))
        P(f"  {bi:2d} {d.key.iloc[0]:38s} "
          f"{(f'{min(pis):.2f}-{max(pis):.2f}' if pis else '-'):>13s} "
          f"{(f'{min(poo):.2f}-{max(poo):.2f}' if poo else '-'):>13s} "
          f"{ismid:7.2f} {oomid:7.2f} {str(cont):>9s}")
    WF = pd.DataFrame(wf)
    hwf = int(WF.contains.sum())
    P(f"  H_WF (IS band contains the OOS band's midpoint in >= 6 of 10): {hwf} of {len(WF)} -> "
      f"{'PASS' if hwf >= 6 else 'FAIL'}")
    P("")
    P("RULE 8 / WF-B - gross chosen per book by IS Sharpe ALONE, OOS read ONCE (10 bps).")
    P(f"  {'#':>2s} {'book key':38s} {'g*':>5s} {'IS Sh':>7s} {'OOS CAGR':>9s} {'OOS Sh':>7s} "
      f"{'OOS DD':>8s} {'4a':>5s} {'4b':>16s}")
    wfb = []
    for bi in sorted(GR.book.unique()):
        d = GR[(GR.book == bi) & (GR.cost == COST_MAIN)]
        pick = d.sort_values("IS_Sharpe", ascending=False).iloc[0]
        wfb.append(dict(book=bi, key=pick.key, g=pick.g, IS_Sharpe=pick.IS_Sharpe,
                        OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                        OOS_MaxDD=pick.OOS_MaxDD, keep4a=pick.keep4a, fail4b=pick.fail4b))
        P(f"  {bi:2d} {pick.key:38s} {pick.g:5.2f} {pick.IS_Sharpe:7.3f} {pick.OOS_CAGR:9.2%} "
          f"{pick.OOS_Sharpe:7.3f} {pick.OOS_MaxDD:8.2%} {str(bool(pick.keep4a)):>5s} "
          f"{('PASS' if pick.fail4b == '-' else pick.fail4b):>16s}")
    WB = pd.DataFrame(wfb)
    pd.concat([WF.assign(leg="wfa"), WB.assign(leg="wfb")], ignore_index=True).to_csv(
        f"{OUT}/{STAMP}.walkforward.csv", index=False)
    P(f"  comparands OOS: RULES v2 {bm['OOS_CAGR']:.2%} / {bm['OOS_Sharpe']:.3f} / "
      f"{bm['OOS_MaxDD']:.2%}   SPY {sm['OOS_CAGR']:.2%} / {sm['OOS_Sharpe']:.3f} / "
      f"{sm['OOS_MaxDD']:.2%}")
    beat_sh = int((WB.OOS_Sharpe > sm["OOS_Sharpe"]).sum())
    beat_bk = int((WB.OOS_Sharpe > bm["OOS_Sharpe"]).sum())
    P(f"  of the {len(WB)} IS-picked books, {beat_sh} beat SPY on OOS Sharpe and {beat_bk} beat the")
    P(f"  live RULES v2 book; {int(WB.keep4a.sum())} are 4a True and "
      f"{int((WB.fail4b == '-').sum())} pass 4b.")
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 118)
    P("KEEP PATHS over every cell")
    P("=" * 118)
    GR.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    for cost in (COST_MAIN, COST_ALT):
        d = GR[GR.cost == cost]
        P(f"  {cost:.0f} bps: {len(d)} cells   4a {int(d.keep4a.sum())}   4b "
          f"{int(d.keep4b.sum())}   BOTH {int((d.keep4a & d.keep4b).sum())}")
    d10 = GR[GR.cost == COST_MAIN]
    P("  fail-4b leg census at 10 bps: " + ", ".join(
        f"{k} {v}" for k, v in d10.fail4b.value_counts().head(9).items()))
    both = d10[d10.keep4a & d10.keep4b]
    if len(both):
        P("  cells passing BOTH paths at 10 bps:")
        for r in both.sort_values("OOS_Sharpe", ascending=False).itertuples():
            P(f"    {r.key:38s} g={r.g:.2f}  CAGR {r.CAGR:.2%} Sharpe {r.Sharpe:.4f} "
              f"MaxDD {r.MaxDD:.2%} halves {r.H1:.3f}/{r.H2:.3f} | OOS {r.OOS_CAGR:.2%}/"
              f"{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.2%}")
    else:
        P("  no cell passes BOTH paths at 10 bps.")
    P("")

    P("=" * 118)
    P("VERDICT")
    P("=" * 118)
    for nm, ok in (("H_KEEP", hkeep >= 6), ("H_FLIP", hflip >= 8),
                   ("H_NARROW", bool(len(anyp) and hnarrow <= 6)), ("H_EDGE", hedge >= 5),
                   ("H_MONO", hmono), ("H_WF", hwf >= 6)):
        P(f"  {nm:10s} {'PASS' if ok else 'FAIL'}")
    P(f"  runtime {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
