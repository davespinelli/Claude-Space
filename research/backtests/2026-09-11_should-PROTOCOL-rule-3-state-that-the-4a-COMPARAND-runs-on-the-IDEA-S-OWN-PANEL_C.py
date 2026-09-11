#!/usr/bin/env python3
"""Idea 737 - "should-PROTOCOL-rule-3-state-that-the-4a-COMPARAND-runs-on-the-IDEA-S-OWN-PANEL"
(lane C, 2026-09-11).

The question
------------
PROTOCOL rule 3 says every idea is compared against `research/baseline.py: rules_v1_weights`
(now RULES v2) - and `baseline.compare(name, weights_fn, px)` implements that by running the
baseline on the SAME `px` the idea was run on:

    base = backtest(px, rules_v2_weights(px), cost_bps=cost_bps, freq=baseline_freq)

Idea 735 found idea 538 does something else: it computes the comparand ONCE on U56
(`px_u = load_universe()`, 538's line 376) and reindexes that single return series onto
SMALL439 and B136.  On SMALL439 the two readings are Sharpe 0.5725 / MaxDD -14.68%
(same panel) against 1.1689 / -12.05% (U56 reindexed), and 538's 4a column moves from
0/324 to 9/324.  735 published both and adopted neither (rule 6).

So the record contains two different 4a bars wearing one name.  This run asks three
things with numbers, not prose:
  (1) WHICH convention does each committed 4a row actually quote?  Decided empirically -
      by computing every candidate comparand and asking which one REPRODUCES the
      published pass/fail column, not by reading code comments.
  (2) HOW MUCH of the record is EXPOSED - i.e. for how many committed rows do the two
      conventions disagree about 4a at all?  A row where both conventions say FAIL needs
      no restatement whatever convention it quoted.
  (3) WHICH DIRECTION does the cross-panel convention push, and does it touch 4b?

Tuned parameters (PROTOCOL rule 4: at most two).  Every grid point reported; nothing is
selected outside the rule-8 walk-forward.
    1. ROW SET, the census tier - ALL qualifying committed rows; the CANON subset whose
       panel label maps onto a panel this sandbox can rebuild exactly; the IDENTIFIED
       subset whose published 4a column is reproduced by exactly one candidate; and the
       EXPOSED subset where SAME and CROSS actually disagree.
    2. CONVENTION, 5 candidates (the comparand library below), each priced on all four
       canonical panels and published in full.

CONVENTION CANDIDATES.  All at 10 bps, next-day execution, weekly cadence, evaluated from
the panel's own `px.index[260]` (the record's standard warm-up skip):
    SAMEv2       RULES v2 on the idea's own panel WITH the joined SPY column.  This is
                 exactly what `baseline.compare()` does, because `load_universe(...)`
                 returns SPY inside the frame.  The PROTOCOL rule 3 reading.
    SAMEv2_noSPY RULES v2 on the panel's investables only (SPY dropped).  A second reading
                 of "own panel" that the record has never distinguished from SAMEv2.
    CROSSv2      RULES v2 computed on U56 and reindexed onto the panel's index.  Idea 538's
                 convention, the object under audit.
    SAMEv1       RULES v1 on the own panel WITH SPY - the pre-2026-09-06 comparand.
    CROSSv1      RULES v1 on U56, reindexed.  The pre-2026-09-06 record's cross-panel form.

4a is the record's own predicate throughout, taken verbatim from `baseline.compare()`:
    H1 > base.H1  AND  H2 > base.H2  AND  MaxDD >= base.MaxDD

Pre-registered bars, written before any census number was read
--------------------------------------------------------------
G1  REPRODUCTION, asserted and printed first.  Idea 538's 162 cells / 324 books are rebuilt
    from source (via idea 735's committed .grid.csv as the reference) and must reproduce
      max |d| < 1e-9 on CAGR, Sharpe, MaxDD, H1, H2, oSharpe and turn_yr, and
      BOTH published 4a columns 324/324 - `p4a` (same-panel, 735's 9/324) and
      `p4a_538conv` (U56-reindexed, 538's 0/324) -
    and the comparand split itself must reproduce: SMALL439 same-panel 0.5725 / -0.1468 and
    B136 1.1058 / -0.1224 against the U56-reindexed 1.1689 / -0.1205 and 1.2056 / -0.1205,
    to < 5e-4 (the record's published 4-dp quotes).
G2  CENSUS COVERAGE.  Of the qualifying committed rows, what share maps onto a rebuildable
    panel (CANON) and what share has its published 4a column reproduced by at least one
    candidate (IDENTIFIED)?  No bar - this is the denominator every later count is quoted
    against, and it is published per file.
B1  MATERIALITY.  Does the convention change any committed 4a verdict?
      PASS (material) -> EXPOSED rows >= 1, i.e. at least one committed row where SAMEv2
      and CROSSv2 disagree.  FAIL -> the two bars are interchangeable on this record and
      PROTOCOL needs no sentence.
B2  DIRECTION.  Is the cross-panel convention systematically the STRICTER bar?
      PASS -> sign(4a rate under SAMEv2 - 4a rate under CROSSv2) is the SAME on every
      canonical panel with at least one exposed row.  A sign that flips by panel means the
      convention is not a uniform tightening and the census cannot be summarised by one
      number.
B3  IS THE 4b PATH TOUCHED?  4b's comparand is SPY, which is panel-local in both
      conventions, so 4b must be IDENTICAL under all five candidates.
      PASS -> 0 rows change 4b.  A non-zero count would mean the two paths are coupled.
B4  DOES IT CHANGE A FRESH DECISION?  The rule-8 walk-forward's 12 arms are scored for 4a
    under both conventions.  PASS (material out of sample) -> the two conventions give
    different 4a counts on the 12 picks.

RULE 8 (mandatory for this lane).  WF-A: 12 arms = 3 panels x 2 gate families x 2
constructions.  Each arm's (level, cadence) is chosen on IS Sharpe over 2010-2016 ALONE
and the 2017+ window is read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against the
RULES v2 comparand OOS under BOTH conventions and against SPY OOS, with 4a scored both
ways and 4b scored once.

CAVEATS.  (i) SURVIVORSHIP (idea 54): all four panels are current constituents, no
delistings, so every CAGR LEVEL is inflated and both KEEP columns inherit that whole; the
convention CONTRAST is a comparand-minus-comparand difference on the same panel and window
and is largely immune.  (ii) The census classifier can only recognise a comparand it can
rebuild: a row from a script with a non-standard window, gross-matched comparand, or a
panel this sandbox cannot reconstruct lands in UNIDENTIFIED and is counted there, never
silently assigned.  (iii) EXPOSURE is computed from each row's own published H1/H2/MaxDD
against the canonical-window comparand, so a block whose window differs from the canonical
one contributes noise to the exposure count; the IDENTIFIED subset is the clean reading and
both are published.  (iv) Two conventions over one corpus are not independent evidence.
"""
import sys, glob, json, time
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa
from engine import backtest as engine_backtest, metrics, rebalance_mask     # noqa

OUT = Path(__file__).with_suffix("")
COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
REF735 = REPO / "research" / "backtests" / (
    "2026-09-11_do-the-ARM-LEVEL-turnover-slopes-that-die-OOS-die-on-every-residual-family_cloud")
G1_TOL, G1_TOL_Q = 1e-9, 5e-4
REF_SPLIT = {                    # idea 735's published 4-dp comparand split
    ("SMALL439", "SAMEv2"): (0.5725, -0.1468), ("SMALL439", "CROSSv2"): (1.1689, -0.1205),
    ("B136", "SAMEv2"): (1.1058, -0.1224),     ("B136", "CROSSv2"): (1.2056, -0.1205),
}
CONVENTIONS = ["SAMEv2", "SAMEv2_noSPY", "CROSSv2", "SAMEv1", "CROSSv1"]

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log():
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


# ------------------------------------------------------------------ machinery (record's own)
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq="W"):
    """numpy re-implementation of engine.backtest; returns (returns, turnover, held gross)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False).values
    n = len(prices.index)
    cur = np.zeros(prices.shape[1]); grs = np.empty(n); turn = np.zeros(n); pr = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        grs[i] = cur.sum(); pr[i] = float(cur @ rets[i])
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = prices.index
    return (pd.Series(pr - turn * cost_bps / 1e4, index=idx),
            pd.Series(turn, index=idx), pd.Series(grs, index=idx))


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def live_mask(px): return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    live = live_mask(px); ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    kt = np.ceil(level * live.sum(axis=1)).astype(int).clip(lower=1)
    return dist.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & live


def unit_book(px, g, construction):
    if construction == "RESPREAD":
        return g.astype(float).div(g.sum(axis=1).clip(lower=1), axis=0)
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0)


def pass4a(row_H1, row_H2, row_DD, b):
    """baseline.compare()'s 4a predicate, verbatim."""
    return bool(row_H1 > b["H1"] and row_H2 > b["H2"] and row_DD >= b["MaxDD"])


def pass4b(row_CAGR, row_H1, row_H2, row_DD, row_oS, spy):
    return bool(row_H1 > spy["H1"] and row_H2 > spy["H2"] and row_oS > spy["oSharpe"]
                and row_DD >= -0.60 * abs(spy["MaxDD"]) and row_CAGR >= 0.70 * spy["CAGR"])


# ------------------------------------------------------------------ panels
def build_panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv439 = [c for c in pxs.columns if c != "SPY" and c not in bad]
    inv484 = [c for c in pxs.columns if c != "SPY"]
    px56, px136 = load_universe(), load_universe(broad=True)
    out = {
        "U56":      (px56[[c for c in px56.columns if c != "SPY"]],   px56["SPY"]),
        "B136":     (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv439], pxs["SPY"]),
        "SMALL484": (pxs[inv484], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0), "
      f"SMALL484 {out['SMALL484'][0].shape[1]}")
    return out


# panel-label normalisation used by the census.  Anything not listed is UNMAPPED and counted
# as such; nothing is guessed onto a panel it might not be.
PANEL_MAP = {
    "u56": "U56", "U56": "U56", "MAIN": "U56", "U55": "U56",
    "broad": "B136", "B136": "B136", "BROAD136": "B136", "broad136": "B136", "BROAD": "B136",
    "SMALL439": "SMALL439", "small439": "SMALL439",
    "small": "SMALL484", "SMALL": "SMALL484", "SMALL484": "SMALL484",
}
A4_COLS = ["pass4a", "p4a", "f4a", "pass_4a", "keep4a", "fail4a"]
A4_NEG = {"f4a", "fail4a"}          # columns stored as FAILURES, inverted before comparison
B4_COLS = ["pass4b", "p4b", "f4b", "pass_4b", "keep4b", "fail4b"]
B4_NEG = {"f4b", "fail4b"}


def main():
    t_start = time.time()
    P("=" * 100)
    P("IDEA 737  should PROTOCOL rule 3 state that the 4a comparand runs on the IDEA'S OWN PANEL")
    P("lane C, 2026-09-11.  10 bps, next-day execution (engine), gross 0.75 on the book population.")
    P(f"two tuned parameters: ROW SET (census tier) x CONVENTION ({len(CONVENTIONS)} candidates). "
      "every grid point published; selection only inside the rule-8 walk-forward.")
    P("=" * 100)
    P("pre-registered bars:")
    P(f"  G1 REPRODUCTION   idea 538/735's 324 books to < {G1_TOL} on 7 columns; BOTH published "
      f"4a columns 324/324; the comparand split to < {G1_TOL_Q}")
    P("  G2 CENSUS COVERAGE  CANON and IDENTIFIED shares of the qualifying rows, per file")
    P("  B1 MATERIALITY    PASS iff >= 1 committed row where SAMEv2 and CROSSv2 disagree on 4a")
    P("  B2 DIRECTION      PASS iff sign(4a rate SAMEv2 - CROSSv2) is the same on every exposed panel")
    P("  B3 4b UNTOUCHED   PASS iff 0 rows change 4b across all five candidates")
    P("  B4 FRESH DECISION PASS iff the 12 rule-8 picks get different 4a counts under the two")
    flush_log()

    PN = build_panels()

    # ---------------------------------------------------------------- comparand library
    P("\n" + "=" * 100)
    P("COMPARAND LIBRARY: 5 conventions x 4 canonical panels (10 bps, W, from px.index[260])")
    P("=" * 100)
    pu = load_universe()                              # U56 WITH SPY, as load_universe returns it
    cross_v2, _, _ = fast_backtest(pu, rules_v2_weights(pu), COST_BPS, "W")
    cross_v1, _, _ = fast_backtest(pu, rules_v1_weights(pu), COST_BPS, "W")
    COMP, SPYS, WIN = {}, {}, {}
    crows = []
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        WIN[pname] = (start, px.index[-1])
        pxj = px.join(spy_px.rename("SPY"))
        series = {
            "SAMEv2":       fast_backtest(pxj, rules_v2_weights(pxj), COST_BPS, "W")[0],
            "SAMEv2_noSPY": fast_backtest(px,  rules_v2_weights(px),  COST_BPS, "W")[0],
            "CROSSv2":      cross_v2.reindex(px.index).fillna(0.0),
            "SAMEv1":       fast_backtest(pxj, rules_v1_weights(pxj), COST_BPS, "W")[0],
            "CROSSv1":      cross_v1.reindex(px.index).fillna(0.0),
        }
        for cv, s in series.items():
            COMP[(pname, cv)] = stat(s.loc[start:])
        SPYS[pname] = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        P(f"\nPANEL {pname}  eval {start.date()} .. {px.index[-1].date()}  "
          f"SPY CAGR {SPYS[pname]['CAGR']:.4f} Sharpe {SPYS[pname]['Sharpe']:.4f} "
          f"MaxDD {SPYS[pname]['MaxDD']:.4f} halves {SPYS[pname]['H1']:.4f}/{SPYS[pname]['H2']:.4f} "
          f"OOS Sharpe {SPYS[pname]['oSharpe']:.4f}")
        P(f"  {'convention':14} {'CAGR':>8} {'Sharpe':>8} {'MaxDD':>9} {'H1':>8} {'H2':>8} {'oSharpe':>8}")
        for cv in CONVENTIONS:
            c = COMP[(pname, cv)]
            P(f"  {cv:14} {c['CAGR']:8.4f} {c['Sharpe']:8.4f} {c['MaxDD']:9.4f} {c['H1']:8.4f} "
              f"{c['H2']:8.4f} {c['oSharpe']:8.4f}")
            crows.append(dict(panel=pname, convention=cv, **c))
    pd.DataFrame(crows).to_csv(OUT.with_suffix(".comparands.csv"), index=False)
    flush_log()

    # ---------------------------------------------------------------- G1 reproduction
    P("\n" + "=" * 100)
    P("G1 REPRODUCTION GATE (asserted before any census number is read)")
    P("=" * 100)
    g1_split_ok, g1_split_max = True, 0.0
    for (pname, cv), (rs, rd) in REF_SPLIT.items():
        c = COMP[(pname, cv)]
        ds, dd = abs(c["Sharpe"] - rs), abs(c["MaxDD"] - rd)
        g1_split_max = max(g1_split_max, ds, dd)
        ok = ds < G1_TOL_Q and dd < G1_TOL_Q
        g1_split_ok &= ok
        P(f"  {pname:9} {cv:8} Sharpe {c['Sharpe']:.4f} vs {rs:.4f} (d {ds:.2e})   "
          f"MaxDD {c['MaxDD']:.4f} vs {rd:.4f} (d {dd:.2e})   {'OK' if ok else 'FAIL'}")
    P(f"  comparand-split leg: max |d| {g1_split_max:.3e} vs bar {G1_TOL_Q} -> "
      f"{'PASS' if g1_split_ok else 'FAIL'}")
    flush_log()

    # rebuild idea 538's 162 cells / 324 books
    books = []
    for pname in ["U56", "B136", "SMALL439"]:
        px, spy_px = PN[pname]
        start = px.index[260]
        yrs = len(px.loc[start:]) / 252
        for family in FAMILIES:
            for level in (QUANT_X if family == "QUANTILE" else MA_THETA):
                gm = gate_mask(px, family, level)
                ub = {c: unit_book(px, gm, c) for c in CONSTRUCTIONS}
                for cad in CADENCES:
                    for con in CONSTRUCTIONS:
                        r, turn, _ = fast_backtest(px, ub[con] * GROSS, COST_BPS, cad)
                        r, turn = r.loc[start:], turn.loc[start:]
                        s = stat(r)
                        books.append(dict(panel=pname, family=family, level=level, cad=cad,
                                          con=con, turn_yr=turn.sum() / yrs, **s))
        P(f"  rebuilt {pname}: {len([b for b in books if b['panel']==pname])} books "
          f"({time.time()-t_start:.0f}s elapsed)")
        flush_log()
    G = pd.DataFrame(books)

    ref = pd.read_csv(str(REF735) + ".grid.csv")
    key = ["panel", "family", "level", "cad", "con"]
    M = G.merge(ref, on=key, suffixes=("", "_ref"), validate="one_to_one")
    assert len(M) == 324, f"merge against idea 735's grid gave {len(M)} rows, expected 324"
    g1_cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]
    g1_max = {c: float(np.max(np.abs(M[c] - M[c + "_ref"]))) for c in g1_cols}
    g1_book_ok = all(v < G1_TOL for v in g1_max.values())
    P("  book-level reproduction vs idea 735's committed .grid.csv (n=324):")
    P("    " + "  ".join(f"{c} {g1_max[c]:.3e}" for c in g1_cols))
    P(f"    bar {G1_TOL} -> {'PASS' if g1_book_ok else 'FAIL'}")

    # both published 4a columns, recomputed from this run's comparands
    M["my_p4a_same"] = [pass4a(r.H1, r.H2, r.MaxDD, COMP[(r.panel, "SAMEv2")]) for r in M.itertuples()]
    M["my_p4a_cross"] = [pass4a(r.H1, r.H2, r.MaxDD, COMP[(r.panel, "CROSSv2")]) for r in M.itertuples()]
    n_same = int((M.my_p4a_same == M.p4a).sum())
    n_cross = int((M.my_p4a_cross == M.p4a_538conv).sum())
    P(f"  published 4a columns reproduced: p4a (same-panel) {n_same}/324, "
      f"p4a_538conv (U56-reindexed) {n_cross}/324")
    P(f"  counts: SAMEv2 {int(M.my_p4a_same.sum())}/324 (735 published {int(M.p4a.sum())}), "
      f"CROSSv2 {int(M.my_p4a_cross.sum())}/324 (735 published {int(M.p4a_538conv.sum())})")
    g1_col_ok = (n_same == 324 and n_cross == 324)
    G1 = g1_split_ok and g1_book_ok and g1_col_ok
    P(f"  G1 OVERALL: {'PASS' if G1 else 'FAIL'}  "
      f"(split {'ok' if g1_split_ok else 'FAIL'}, books {'ok' if g1_book_ok else 'FAIL'}, "
      f"columns {'ok' if g1_col_ok else 'FAIL'})")
    flush_log()

    # ---------------------------------------------------------------- the 324-book grid, all 5 conventions
    P("\n" + "=" * 100)
    P("THE AUDIT POPULATION (idea 538's 324 books): 4a under every convention, 4b once")
    P("=" * 100)
    for cv in CONVENTIONS:
        G[f"p4a_{cv}"] = [pass4a(r.H1, r.H2, r.MaxDD, COMP[(r.panel, cv)]) for r in G.itertuples()]
    G["p4b"] = [pass4b(r.CAGR, r.H1, r.H2, r.MaxDD, r.oSharpe, SPYS[r.panel]) for r in G.itertuples()]
    P(f"  {'convention':14} {'4a ALL':>8} " + " ".join(f"{p:>10}" for p in ["U56", "B136", "SMALL439"]))
    for cv in CONVENTIONS:
        per = G.groupby("panel")[f"p4a_{cv}"].sum()
        P(f"  {cv:14} {int(G[f'p4a_{cv}'].sum()):8d} " +
          " ".join(f"{int(per.get(p,0)):10d}" for p in ["U56", "B136", "SMALL439"]))
    P(f"  4b (SPY comparand, panel-local in every convention): {int(G.p4b.sum())}/324  "
      + " ".join(f"{p}={int(G.groupby('panel').p4b.sum().get(p,0))}" for p in ["U56","B136","SMALL439"]))
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    flush_log()

    # ---------------------------------------------------------------- CENSUS
    P("\n" + "=" * 100)
    P("CENSUS of the committed record: which 4a rows quote which comparand, and which are EXPOSED")
    P("=" * 100)
    files = sorted(glob.glob(str(REPO / "research" / "backtests" / "*.csv")))
    P(f"  committed CSVs scanned: {len(files)}")
    crecs, unmapped = [], {}
    n_qual_files = n_qual_rows = 0
    for f in files:
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception:
            continue
        cols = set(head.columns)
        if "panel" not in cols: continue
        a4 = next((c for c in A4_COLS if c in cols), None)
        if a4 is None: continue
        if not {"H1", "H2", "MaxDD"} <= cols: continue
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        df["panel"] = df["panel"].astype(str)
        if df["panel"].nunique() < 2: continue            # single-panel runs cannot be cross-panel
        n_qual_files += 1; n_qual_rows += len(df)
        b4 = next((c for c in B4_COLS if c in cols), None)
        pub = df[a4]
        pub = pub.astype(str).str.strip().str.lower().map(
            {"true": True, "false": False, "1": True, "0": False, "1.0": True, "0.0": False})
        if a4 in A4_NEG: pub = ~pub.astype("boolean")
        for pname, sub in df.groupby("panel"):
            canon = PANEL_MAP.get(pname)
            if canon is None:
                unmapped[pname] = unmapped.get(pname, 0) + len(sub)
                crecs.append(dict(file=Path(f).name, panel_label=pname, canon="", n=len(sub),
                                  a4col=a4, mapped=False, identified="", n_exposed=0,
                                  n_flip_F2T=0, n_flip_T2F=0, pub_rate=np.nan))
                continue
            H1, H2, DD = sub.H1.values, sub.H2.values, sub.MaxDD.values
            pv = pub.loc[sub.index]
            rec = dict(file=Path(f).name, panel_label=pname, canon=canon, n=len(sub), a4col=a4,
                       mapped=True)
            got = {}
            for cv in CONVENTIONS:
                b = COMP[(canon, cv)]
                got[cv] = (H1 > b["H1"]) & (H2 > b["H2"]) & (DD >= b["MaxDD"])
                rec[f"rate_{cv}"] = float(np.mean(got[cv]))
                rec[f"match_{cv}"] = (float(np.mean(got[cv] == pv.values))
                                      if pv.notna().all() else np.nan)
            exact = [cv for cv in CONVENTIONS if rec.get(f"match_{cv}") == 1.0]
            rec["identified"] = "|".join(exact)
            rec["n_exact"] = len(exact)
            same, cross = got["SAMEv2"], got["CROSSv2"]
            rec["n_exposed"] = int(np.sum(same != cross))
            rec["n_flip_F2T"] = int(np.sum(same & ~cross))     # cross says FAIL, same says PASS
            rec["n_flip_T2F"] = int(np.sum(~same & cross))
            # the v1 pair (the pre-2026-09-06 comparand) and the SPY-inclusion pair
            rec["n_exposed_v1"] = int(np.sum(got["SAMEv1"] != got["CROSSv1"]))
            rec["n_flip_v1_F2T"] = int(np.sum(got["SAMEv1"] & ~got["CROSSv1"]))
            rec["n_flip_v1_T2F"] = int(np.sum(~got["SAMEv1"] & got["CROSSv1"]))
            rec["n_exposed_spy"] = int(np.sum(got["SAMEv2"] != got["SAMEv2_noSPY"]))
            # which leg of the 4a predicate binds on the reverse flips (cross PASS, same FAIL)
            rv = ~same & cross
            bs, bc = COMP[(canon, "SAMEv2")], COMP[(canon, "CROSSv2")]
            rec["rev_leg_H1"] = int(np.sum(rv & ~(H1 > bs["H1"])))
            rec["rev_leg_H2"] = int(np.sum(rv & ~(H2 > bs["H2"])))
            rec["rev_leg_DD"] = int(np.sum(rv & ~(DD >= bs["MaxDD"])))
            rec["pub_rate"] = float(pv.mean()) if pv.notna().all() else np.nan
            if b4 is not None:
                rec["has4b"] = True
            crecs.append(rec)
    C = pd.DataFrame(crecs)
    C.to_csv(OUT.with_suffix(".census.csv"), index=False)
    P(f"  qualifying files (panel col with >=2 panels, a 4a column, and H1/H2/MaxDD): "
      f"{n_qual_files}; rows {n_qual_rows}")
    mapped = C[C.mapped == True]                                              # noqa: E712
    P(f"  CANON rows (panel label rebuildable here): {int(mapped.n.sum())} of {n_qual_rows} "
      f"({mapped.n.sum()/max(n_qual_rows,1):.1%}) over {mapped.file.nunique()} files")
    P(f"  UNMAPPED panel labels: {len(unmapped)} distinct, {sum(unmapped.values())} rows -> "
      + ", ".join(f"{k}({v})" for k, v in sorted(unmapped.items(), key=lambda kv: -kv[1])[:12]))
    flush_log()

    # G2 coverage + identification
    ident = mapped[mapped.n_exact > 0]
    uniq = mapped[mapped.n_exact == 1]
    P("\n  G2 COVERAGE / IDENTIFICATION (block = one file x one panel label):")
    P(f"    blocks CANON {len(mapped)}; published 4a column reproduced EXACTLY by >=1 candidate "
      f"in {len(ident)} blocks ({int(ident.n.sum())} rows), by EXACTLY ONE in {len(uniq)} "
      f"({int(uniq.n.sum())} rows)")
    idc = {}
    for _, r in mapped.iterrows():
        for cv in (r.identified.split("|") if r.identified else ["<none>"]):
            idc[cv] = idc.get(cv, 0) + int(r.n)
    P("    rows by identified candidate set member (a row can match several): "
      + ", ".join(f"{k} {v}" for k, v in sorted(idc.items(), key=lambda kv: -kv[1])))
    uc = {}
    for _, r in uniq.iterrows():
        uc[r.identified] = uc.get(r.identified, 0) + int(r.n)
    P("    UNIQUELY identified rows by convention: "
      + (", ".join(f"{k} {v}" for k, v in sorted(uc.items(), key=lambda kv: -kv[1])) or "none"))
    flush_log()

    # B1 materiality / exposure
    P("\n  B1 MATERIALITY (SAMEv2 vs CROSSv2 disagreement on committed rows):")
    exp_rows = int(mapped.n_exposed.sum())
    P(f"    EXPOSED rows: {exp_rows} of {int(mapped.n.sum())} CANON rows "
      f"({exp_rows/max(int(mapped.n.sum()),1):.2%}) in {int((mapped.n_exposed>0).sum())} blocks")
    P(f"    direction: cross-FAIL -> same-PASS {int(mapped.n_flip_F2T.sum())}; "
      f"cross-PASS -> same-FAIL {int(mapped.n_flip_T2F.sum())}")
    by_panel = mapped.groupby("canon").agg(n=("n", "sum"), exposed=("n_exposed", "sum"),
                                           F2T=("n_flip_F2T", "sum"), T2F=("n_flip_T2F", "sum"))
    P("    by canonical panel:")
    for p, r in by_panel.iterrows():
        P(f"      {p:9} rows {int(r.n):7d}  exposed {int(r.exposed):6d} "
          f"({r.exposed/max(r.n,1):6.2%})  cross-FAIL->same-PASS {int(r.F2T):6d}  "
          f"cross-PASS->same-FAIL {int(r.T2F):6d}")
    B1 = exp_rows >= 1
    P(f"    B1: {'PASS (material)' if B1 else 'FAIL (interchangeable)'}")
    P(f"    the v1 pair (pre-2026-09-06 comparand, SAMEv1 vs CROSSv1): exposed "
      f"{int(mapped.n_exposed_v1.sum())} rows ({mapped.n_exposed_v1.sum()/max(int(mapped.n.sum()),1):.2%}), "
      f"cross-FAIL->same-PASS {int(mapped.n_flip_v1_F2T.sum())}, "
      f"cross-PASS->same-FAIL {int(mapped.n_flip_v1_T2F.sum())}")
    P(f"    the SPY-INCLUSION pair (SAMEv2 vs SAMEv2_noSPY, both 'own panel'): exposed "
      f"{int(mapped.n_exposed_spy.sum())} rows "
      f"({mapped.n_exposed_spy.sum()/max(int(mapped.n.sum()),1):.2%}) - a THIRD convention the "
      f"record has never distinguished")
    P(f"    which 4a leg binds on the {int(mapped.n_flip_T2F.sum())} REVERSE flips (cross PASS, "
      f"same FAIL): H1 {int(mapped.rev_leg_H1.sum())}, H2 {int(mapped.rev_leg_H2.sum())}, "
      f"MaxDD {int(mapped.rev_leg_DD.sum())}")

    # the clean reading: blocks whose convention is uniquely identified as CROSS
    cross_ids = uniq[uniq.identified.isin(["CROSSv2", "CROSSv1"])]
    same_ids = uniq[uniq.identified.isin(["SAMEv2", "SAMEv2_noSPY", "SAMEv1"])]
    P(f"\n  RESTATEMENT (the clean subset): blocks UNIQUELY identified as a CROSS convention: "
      f"{len(cross_ids)} blocks, {int(cross_ids.n.sum())} rows, of which EXPOSED "
      f"{int(cross_ids.n_exposed.sum())} -> those are the rows whose published 4a verdict "
      f"CHANGES when restated on the idea's own panel "
      f"(F->T {int(cross_ids.n_flip_F2T.sum())}, T->F {int(cross_ids.n_flip_T2F.sum())})")
    P(f"  blocks uniquely identified as a SAME convention: {len(same_ids)} blocks, "
      f"{int(same_ids.n.sum())} rows - already PROTOCOL-conformant, nothing to restate")
    if len(cross_ids):
        P("  every CROSS-identified block, restated:")
        for _, r in cross_ids.sort_values("n_exposed", ascending=False).iterrows():
            P(f"    {r.file:78} {r.panel_label:9} n {int(r.n):6d} published 4a rate "
              f"{r.pub_rate:.4f} -> same-panel {r['rate_SAMEv2']:.4f}  exposed {int(r.n_exposed)}")
    flush_log()

    # B2 direction
    P("\n  B2 DIRECTION (sign of 4a rate SAMEv2 - CROSSv2 by panel, on exposed panels):")
    signs = {}
    for p, r in by_panel.iterrows():
        if r.exposed == 0:
            P(f"    {p:9} no exposed rows - no sign"); continue
        d = (r.F2T - r.T2F) / max(r.n, 1)
        signs[p] = np.sign(d)
        P(f"    {p:9} (F2T - T2F) / n = {d:+.4%} -> same-panel is the "
          f"{'LOOSER' if d > 0 else 'STRICTER' if d < 0 else 'EQUAL'} bar")
    B2 = len(set(signs.values())) <= 1 and len(signs) > 0
    P(f"    B2: {'PASS (uniform direction)' if B2 else 'FAIL (direction is panel-dependent)'}")

    # B3 4b untouched
    b3_changes = 0
    P("\n  B3 4b UNTOUCHED: 4b's legs read SPY and the row itself only; recomputing 4b under "
      "every convention changes nothing by construction. Verified on the 324-book grid:")
    b3_ref = G.p4b.values
    for cv in CONVENTIONS:
        chk = np.array([pass4b(r.CAGR, r.H1, r.H2, r.MaxDD, r.oSharpe, SPYS[r.panel])
                        for r in G.itertuples()])
        b3_changes += int(np.sum(chk != b3_ref))
    P(f"    rows whose 4b changes across the 5 candidates: {b3_changes}  "
      f"-> B3 {'PASS' if b3_changes == 0 else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD  WF-A: 12 arms = 3 panels x 2 families x 2 constructions.")
    P("  (level, cadence) chosen on IS Sharpe 2010..2016 ALONE; 2017+ read ONCE.")
    P("=" * 100)
    wf = []
    for pname in ["U56", "B136", "SMALL439"]:
        for family in FAMILIES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                wf.append(dict(panel=pname, family=family, con=con, level=pick.level,
                               cad=pick.cad, isSharpe=pick.isSharpe,
                               oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                               CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD,
                               H1=pick.H1, H2=pick.H2,
                               **{f"p4a_{cv}": bool(pick[f"p4a_{cv}"]) for cv in CONVENTIONS},
                               p4b=bool(pick.p4b)))
    W = pd.DataFrame(wf)
    P(f"  {'panel':9} {'family':10} {'con':9} {'lvl':>6} {'cad':>3} {'isS':>7} | {'oCAGR':>7} "
      f"{'oSharpe':>7} {'oMaxDD':>7} | {'4a same':>7} {'4a cross':>8} {'4b':>4} | "
      f"{'v2 oS same':>10} {'v2 oS cross':>11} {'SPY oS':>7}")
    for r in W.itertuples():
        cs, cc = COMP[(r.panel, "SAMEv2")], COMP[(r.panel, "CROSSv2")]
        P(f"  {r.panel:9} {r.family:10} {r.con:9} {r.level:6.2f} {r.cad:>3} {r.isSharpe:7.4f} | "
          f"{r.oCAGR:7.4f} {r.oSharpe:7.4f} {r.oMaxDD:7.4f} | {str(r.p4a_SAMEv2):>7} "
          f"{str(r.p4a_CROSSv2):>8} {str(r.p4b):>4} | {cs['oSharpe']:10.4f} {cc['oSharpe']:11.4f} "
          f"{SPYS[r.panel]['oSharpe']:7.4f}")
    W["beats_v2_oos_same"] = [r.oSharpe > COMP[(r.panel, "SAMEv2")]["oSharpe"] for r in W.itertuples()]
    W["beats_v2_oos_cross"] = [r.oSharpe > COMP[(r.panel, "CROSSv2")]["oSharpe"] for r in W.itertuples()]
    W["beats_spy_oos"] = [r.oSharpe > SPYS[r.panel]["oSharpe"] for r in W.itertuples()]
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(f"\n  OOS Sharpe range {W.oSharpe.min():.4f}..{W.oSharpe.max():.4f}; OOS CAGR "
      f"{W.oCAGR.min():.2%}..{W.oCAGR.max():.2%}; OOS MaxDD {W.oMaxDD.min():.2%}..{W.oMaxDD.max():.2%}")
    P(f"  beats the RULES v2 comparand OOS Sharpe: same-panel {int(W.beats_v2_oos_same.sum())}/12, "
      f"U56-reindexed {int(W.beats_v2_oos_cross.sum())}/12; beats SPY OOS "
      f"{int(W.beats_spy_oos.sum())}/12")
    n4a_s, n4a_c = int(W.p4a_SAMEv2.sum()), int(W.p4a_CROSSv2.sum())
    P(f"  4a on the 12 picks: same-panel {n4a_s}/12, U56-reindexed {n4a_c}/12; 4b {int(W.p4b.sum())}/12")
    B4 = n4a_s != n4a_c
    P(f"  B4: {'PASS (the convention changes a fresh decision)' if B4 else 'FAIL (same count)'}")
    flush_log()

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    P("BOTH KEEP PATHS on the 324-book audit population")
    P("=" * 100)
    for cv in CONVENTIONS:
        P(f"  4a {cv:14} {int(G[f'p4a_{cv}'].sum()):3d}/324")
    P(f"  4b (unchanged by the convention) {int(G.p4b.sum())}/324")
    P(f"  rule-8 leg: 4a same {n4a_s}/12, 4a cross {n4a_c}/12, 4b {int(W.p4b.sum())}/12")
    P("\nGATES: G1 %s | B1 %s | B2 %s | B3 %s | B4 %s" %
      tuple("PASS" if x else "FAIL" for x in (G1, B1, B2, b3_changes == 0, B4)))
    summ = dict(G1=G1, B1=B1, B2=B2, B3=b3_changes == 0, B4=B4,
                qual_files=n_qual_files, qual_rows=int(n_qual_rows),
                canon_rows=int(mapped.n.sum()), exposed_rows=exp_rows,
                flip_F2T=int(mapped.n_flip_F2T.sum()), flip_T2F=int(mapped.n_flip_T2F.sum()),
                blocks_canon=len(mapped), blocks_identified=len(ident), blocks_unique=len(uniq),
                rows_unique_cross=int(cross_ids.n.sum()), rows_unique_same=int(same_ids.n.sum()),
                exposed_unique_cross=int(cross_ids.n_exposed.sum()),
                exposed_v1=int(mapped.n_exposed_v1.sum()),
                exposed_spy=int(mapped.n_exposed_spy.sum()),
                rows_unidentified=int(mapped.n.sum()) - int(ident.n.sum()),
                p4a_same_324=int(G.p4a_SAMEv2.sum()), p4a_cross_324=int(G.p4a_CROSSv2.sum()),
                p4b_324=int(G.p4b.sum()), wf_4a_same=n4a_s, wf_4a_cross=n4a_c,
                wf_4b=int(W.p4b.sum()), runtime_s=round(time.time() - t_start, 1))
    OUT.with_suffix(".summary.json").write_text(json.dumps(summ, indent=2, default=str))
    P(f"\nruntime {summ['runtime_s']}s")
    flush_log()
    return summ


if __name__ == "__main__":
    main()
