#!/usr/bin/env python3
"""Idea 741 - "restate-the-58529-v1-EXPOSED-rows-of-the-PRE-2026-09-06-record"
(lane C, 2026-09-11).

The question
------------
Idea 737 censused every committed 4a row for comparand convention and found that the
*v1* pair (SAMEv1, the RULES v1 book on the idea's own panel, vs CROSSv1, the RULES v1
book computed once on U56 and reindexed) disagrees on 58,529 rows - 15.16% of the 386,109
CANON rows - against 2,949 rows (0.76%) for the v2 pair.  It attributed the 20x to RULES
v1's drawdown: v1 runs MaxDD -13.8% on U56 against -44.8% on SMALL484, so the 4a MaxDD leg
(`row.MaxDD >= base.MaxDD`) is a very different bar depending on which panel the comparand
was built on.

737 stopped at the exposure count.  This run does what the queue asked: re-read those rows
on the SAME-PANEL v1 comparand and say how many published verdicts the old record loses or
gains.

"Lose" and "gain" are defined against the row's OWN PUBLISHED 4a column, not against a
recomputed one:
    LOST   = published PASS, restated FAIL
    GAINED = published FAIL, restated PASS
so a row whose published column already agrees with the same-panel bar costs nothing to
restate whatever convention its author intended.

Tuned parameters (PROTOCOL rule 4: at most two).  Every grid point reported; nothing is
selected outside the rule-8 walk-forward.
    1. ROW SET, 6 tiers - CANON737 (737's filter verbatim, the G1 population); V1ERA
       (CANON rows from files dated before 2026-09-06, the date RULES v2 went live);
       V1ERA6 (the same with 2026-09-06 itself folded in, because that day is the
       transition and the empirical match rates are ambiguous on it); V1ERA_EXPOSED (the
       v1-era rows where SAMEv1 and CROSSv1 actually disagree - the only rows whose verdict
       CAN move); V1ERA_IDENT (v1-era blocks whose published 4a column is reproduced
       exactly by at least one candidate - the clean reading); and V1ERA_UNIQ_CROSSv1
       (blocks provably quoting the cross-panel v1 comparand - the rows that MUST be
       restated if any must).
    2. CONVENTION, 6 candidates priced on all four canonical panels and published in full:
       SAMEv2, SAMEv2_noSPY, CROSSv2 (737's three) plus SAMEv1, SAMEv1_noSPY, CROSSv1.

All comparands: 10 bps, next-day execution (the engine's t+1), weekly cadence, evaluated
from the panel's own `px.index[260]` - the record's standard warm-up skip.  4a is the
record's own predicate, taken verbatim from `baseline.compare()`:
    H1 > base.H1  AND  H2 > base.H2  AND  MaxDD >= base.MaxDD

Pre-registered bars, written before any 741 number was read
-----------------------------------------------------------
G1  REPRODUCTION, asserted and printed first.  737's census is re-run with its filter
    verbatim and must reproduce its committed summary.json INTEGERS EXACTLY:
    qual_files 375, qual_rows 433,949, canon_rows 386,109, blocks_canon 1,018,
    exposed_v1 58,529, exposed_rows 2,949, flip_F2T 2,944, flip_T2F 5, exposed_spy 1,079;
    and 737's 324-book grid must rebuild to max |d| < 1e-9 on 7 columns.
G2  VINTAGE.  Per filename date, the row-weighted share of published 4a cells each of the
    6 candidates reproduces.  No bar - this is what licenses calling the pre-2026-09-06
    files "the v1 record" rather than asserting it.
B1  IS THE 58,529 ACTUALLY THE OLD RECORD?  The queue's title says "of the PRE-2026-09-06
    record".  PASS -> at least 50% of the 58,529 v1-exposed rows sit in pre-2026-09-06
    files.  FAIL -> the exposure is overwhelmingly a counterfactual on rows that never
    quoted a v1 comparand at all, and the restatement question is much smaller than the
    headline number.
B2  IS THERE ANYTHING TO RESTATE?  PASS -> at least one v1-era block is UNIQUELY
    identified as CROSSv1, i.e. provably quotes the cross-panel v1 bar.  FAIL -> no
    committed pre-2026-09-06 block can be shown to have used the convention under audit,
    so no published verdict is established to be wrong.
B3  WHICH LEG BINDS?  PASS -> the MaxDD leg explains >= 50% of the 58,529 v1 flips, as
    737's -13.8% / -44.8% mechanism predicts.  FAIL -> the mechanism is mis-attributed.
B4  4b UNTOUCHED.  4b's legs read SPY and the row itself only.  PASS -> 0 rows change 4b
    across all 6 candidates.
B5  DOES IT CHANGE A FRESH DECISION?  The rule-8 walk-forward's 12 arms are scored for 4a
    under all 6 conventions.  PASS -> SAMEv1 and CROSSv1 give different 4a counts on the
    12 out-of-sample picks.

RULE 8 (mandatory for this lane).  12 arms = 3 panels x 2 gate families x 2 constructions.
Each arm's (level, cadence) is chosen on IS Sharpe over 2010-2016 ALONE and the 2017+
window is read ONCE.  OOS CAGR / Sharpe / MaxDD are reported against the RULES v2
same-panel comparand OOS, the RULES v1 same-panel comparand OOS, the v1 CROSS comparand
OOS and SPY OOS, with 4a scored six ways and 4b scored once.

CAVEATS.  (i) SURVIVORSHIP (idea 54): all four panels are current constituents, no
delistings, so every CAGR LEVEL is inflated; the convention CONTRAST is a
comparand-minus-comparand difference on the same panel and window and is largely immune.
(ii) A "row" here is a grid cell in a committed CSV, not a headline claim.  A block of 480
cells is one idea; LOST/GAINED counts are cell counts and the per-block table is the right
place to read claim-level impact.  (iii) The classifier can only recognise a comparand it
can REBUILD.  Idea 739 showed 133 blocks / 103,736 rows reach no knob setting of the
PROTOCOL book at all (non-standard window, gross-matched comparand, unrebuildable panel);
those land in UNIDENTIFIED and are counted there, never silently assigned.  On such a block
LOST/GAINED measured against the published column is contaminated by whatever the block's
real comparand was, which is why V1ERA_IDENT is published as the clean reading beside the
raw one.  (iv) Six conventions over one corpus are not six independent experiments.
"""
import sys, glob, json, time
from pathlib import Path
import numpy as np, pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa
from engine import metrics, rebalance_mask                                   # noqa

OUT = Path(__file__).with_suffix("")
SELF = OUT.name                       # this run's own outputs are excluded from the census
COST_BPS, GROSS = 10, 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
V2_LIVE = "2026-09-06"                # RULES v2 went live this day (baseline.py docstring)
CONVENTIONS = ["SAMEv2", "SAMEv2_noSPY", "CROSSv2", "SAMEv1", "SAMEv1_noSPY", "CROSSv1"]
V1_PAIR = ("SAMEv1", "CROSSv1")

REF737 = REPO / "research" / "backtests" / (
    "2026-09-11_should-PROTOCOL-rule-3-state-that-the-4a-COMPARAND-runs-on-the-IDEA-S-OWN-PANEL_C")
G1_REF = dict(qual_files=375, qual_rows=433949, canon_rows=386109, blocks_canon=1018,
              exposed_v1=58529, exposed_rows=2949, flip_F2T=2944, flip_T2F=5,
              exposed_spy=1079)
G1_TOL = 1e-9
B1_BAR, B3_BAR = 0.50, 0.50

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def flush_log():
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


# ------------------------------------------------------------------ machinery (the record's own)
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


PANEL_MAP = {            # 737's map verbatim; anything else is UNMAPPED and counted as such
    "u56": "U56", "U56": "U56", "MAIN": "U56", "U55": "U56",
    "broad": "B136", "B136": "B136", "BROAD136": "B136", "broad136": "B136", "BROAD": "B136",
    "SMALL439": "SMALL439", "small439": "SMALL439",
    "small": "SMALL484", "SMALL": "SMALL484", "SMALL484": "SMALL484",
}
A4_COLS = ["pass4a", "p4a", "f4a", "pass_4a", "keep4a", "fail4a"]
A4_NEG = {"f4a", "fail4a"}
B4_COLS = ["pass4b", "p4b", "f4b", "pass_4b", "keep4b", "fail4b"]


def main():
    t0 = time.time()
    P("=" * 104)
    P("IDEA 741  restate the 58,529 v1-EXPOSED rows of the PRE-2026-09-06 record")
    P("lane C, 2026-09-11.  10 bps, next-day execution (engine), gross 0.75 on the book population.")
    P(f"two tuned parameters: ROW SET (6 census tiers) x CONVENTION ({len(CONVENTIONS)} candidates).")
    P("every grid point published; selection only inside the rule-8 walk-forward.")
    P("=" * 104)
    P("pre-registered bars:")
    P(f"  G1 REPRODUCTION   737's census integers EXACTLY ({G1_REF}); its 324-book grid to < {G1_TOL}")
    P("  G2 VINTAGE        per-date match rate of all 6 candidates (no bar; licenses the era cut)")
    P(f"  B1 IS IT THE OLD RECORD?  PASS iff >= {B1_BAR:.0%} of the 58,529 v1-exposed rows are pre-{V2_LIVE}")
    P("  B2 ANYTHING TO RESTATE?   PASS iff >= 1 v1-era block is UNIQUELY identified as CROSSv1")
    P(f"  B3 WHICH LEG BINDS?       PASS iff MaxDD explains >= {B3_BAR:.0%} of the v1 flips")
    P("  B4 4b UNTOUCHED           PASS iff 0 rows change 4b across all 6 candidates")
    P("  B5 FRESH DECISION         PASS iff SAMEv1 and CROSSv1 give different 4a counts on the 12 picks")
    flush_log()

    PN = build_panels()

    # ------------------------------------------------------------ comparand library
    P("\n" + "=" * 104)
    P("COMPARAND LIBRARY: 6 conventions x 4 canonical panels (10 bps, W, from px.index[260])")
    P("=" * 104)
    pu = load_universe()                       # U56 WITH SPY, exactly as load_universe returns it
    cross_v2, _, _ = fast_backtest(pu, rules_v2_weights(pu), COST_BPS, "W")
    cross_v1, _, _ = fast_backtest(pu, rules_v1_weights(pu), COST_BPS, "W")
    COMP, SPYS, crows = {}, {}, []
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        pxj = px.join(spy_px.rename("SPY"))
        series = {
            "SAMEv2":       fast_backtest(pxj, rules_v2_weights(pxj), COST_BPS, "W")[0],
            "SAMEv2_noSPY": fast_backtest(px,  rules_v2_weights(px),  COST_BPS, "W")[0],
            "CROSSv2":      cross_v2.reindex(px.index).fillna(0.0),
            "SAMEv1":       fast_backtest(pxj, rules_v1_weights(pxj), COST_BPS, "W")[0],
            "SAMEv1_noSPY": fast_backtest(px,  rules_v1_weights(px),  COST_BPS, "W")[0],
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

    P("\n  the MECHANISM the queue attributes the 20x to - RULES v1 MaxDD by panel:")
    for pname in PN:
        P(f"    {pname:9} SAMEv1 MaxDD {COMP[(pname,'SAMEv1')]['MaxDD']:8.4f}   "
          f"CROSSv1 MaxDD {COMP[(pname,'CROSSv1')]['MaxDD']:8.4f}   "
          f"spread {COMP[(pname,'SAMEv1')]['MaxDD'] - COMP[(pname,'CROSSv1')]['MaxDD']:+8.4f}")
    for pname in PN:
        P(f"    {pname:9} SAMEv2 MaxDD {COMP[(pname,'SAMEv2')]['MaxDD']:8.4f}   "
          f"CROSSv2 MaxDD {COMP[(pname,'CROSSv2')]['MaxDD']:8.4f}   "
          f"spread {COMP[(pname,'SAMEv2')]['MaxDD'] - COMP[(pname,'CROSSv2')]['MaxDD']:+8.4f}")
    flush_log()

    # ------------------------------------------------------------ G1a: 737's 324-book grid
    P("\n" + "=" * 104)
    P("G1 REPRODUCTION GATE (asserted before any 741 number is read)")
    P("=" * 104)
    books = []
    for pname in ["U56", "B136", "SMALL439"]:
        px, _ = PN[pname]
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
                        books.append(dict(panel=pname, family=family, level=level, cad=cad,
                                          con=con, turn_yr=turn.sum() / yrs, **stat(r)))
        P(f"  rebuilt {pname}: {len([b for b in books if b['panel']==pname])} books "
          f"({time.time()-t0:.0f}s)")
        flush_log()
    G = pd.DataFrame(books)
    ref = pd.read_csv(str(REF737) + ".grid.csv")
    key = ["panel", "family", "level", "cad", "con"]
    M = G.merge(ref, on=key, suffixes=("", "_ref"), validate="one_to_one")
    assert len(M) == 324, f"merge against 737's grid gave {len(M)} rows, expected 324"
    g1cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe", "turn_yr"]
    g1max = {c: float(np.max(np.abs(M[c] - M[c + "_ref"]))) for c in g1cols}
    g1_books = all(v < G1_TOL for v in g1max.values())
    P("  324-book rebuild vs 737's committed .grid.csv: " + "  ".join(f"{c} {g1max[c]:.3e}" for c in g1cols))
    P(f"    bar {G1_TOL} -> {'PASS' if g1_books else 'FAIL'}")
    flush_log()

    # ------------------------------------------------------------ CENSUS (737's filter verbatim)
    P("\n  re-running 737's census with its filter verbatim (this run's own outputs excluded)")
    files = sorted(f for f in glob.glob(str(REPO / "research" / "backtests" / "*.csv"))
                   if not Path(f).name.startswith(SELF))
    crecs, unmapped = [], {}
    n_qual_files = n_qual_rows = 0
    ROWS = []                       # row-level detail for the v1-era restatement
    NROWS, NADROP = {}, {}          # per-file len(df) and rows lost to a NA panel label
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
        if df["panel"].nunique() < 2: continue
        n_qual_files += 1; n_qual_rows += len(df)
        fname = Path(f).name
        fdate = fname[:10]
        NROWS[fname] = len(df)
        # a NA panel label survives .astype(str) as pandas NA and is DROPPED by groupby, so
        # len(df) can exceed the summed block sizes; that gap is tracked, never absorbed.
        NADROP[fname] = int(len(df) - df.groupby("panel").size().sum())
        b4 = next((c for c in B4_COLS if c in cols), None)
        pub = df[a4].astype(str).str.strip().str.lower().map(
            {"true": True, "false": False, "1": True, "0": False, "1.0": True, "0.0": False})
        if a4 in A4_NEG: pub = ~pub.astype("boolean")
        for pname, sub in df.groupby("panel"):
            canon = PANEL_MAP.get(pname)
            if canon is None:
                unmapped[pname] = unmapped.get(pname, 0) + len(sub)
                crecs.append(dict(file=fname, date=fdate, panel_label=pname, canon="", n=len(sub),
                                  a4col=a4, mapped=False, identified="", n_exact=0, n_exposed=0,
                                  n_flip_F2T=0, n_flip_T2F=0, n_exposed_v1=0, n_flip_v1_F2T=0,
                                  n_flip_v1_T2F=0, n_exposed_spy=0, pub_rate=np.nan))
                continue
            H1, H2, DD = sub.H1.values, sub.H2.values, sub.MaxDD.values
            pv = pub.loc[sub.index]
            rec = dict(file=fname, date=fdate, panel_label=pname, canon=canon, n=len(sub),
                       a4col=a4, mapped=True, has4b=b4 is not None)
            got = {}
            for cv in CONVENTIONS:
                b = COMP[(canon, cv)]
                got[cv] = (H1 > b["H1"]) & (H2 > b["H2"]) & (DD >= b["MaxDD"])
                rec[f"rate_{cv}"] = float(np.mean(got[cv]))
                rec[f"match_{cv}"] = (float(np.mean(got[cv] == pv.values))
                                      if pv.notna().all() else np.nan)
            exact = [cv for cv in CONVENTIONS if rec.get(f"match_{cv}") == 1.0]
            rec["identified"] = "|".join(exact); rec["n_exact"] = len(exact)
            same, cross = got["SAMEv2"], got["CROSSv2"]
            rec["n_exposed"] = int(np.sum(same != cross))
            rec["n_flip_F2T"] = int(np.sum(same & ~cross))
            rec["n_flip_T2F"] = int(np.sum(~same & cross))
            s1, c1 = got["SAMEv1"], got["CROSSv1"]
            rec["n_exposed_v1"] = int(np.sum(s1 != c1))
            rec["n_flip_v1_F2T"] = int(np.sum(s1 & ~c1))
            rec["n_flip_v1_T2F"] = int(np.sum(~s1 & c1))
            rec["n_exposed_spy"] = int(np.sum(got["SAMEv2"] != got["SAMEv2_noSPY"]))
            rec["n_exposed_spy_v1"] = int(np.sum(got["SAMEv1"] != got["SAMEv1_noSPY"]))
            rec["pub_rate"] = float(pv.mean()) if pv.notna().all() else np.nan
            # which 4a leg binds on the v1 flips.  A flip is one convention PASSing and the
            # other FAILing, so the informative leg is the one that fails on the FAILING
            # side: for a SAMEv1-PASS / CROSSv1-FAIL row that is a CROSSv1 leg, and vice versa.
            bs, bc = COMP[(canon, "SAMEv1")], COMP[(canon, "CROSSv1")]
            fl = s1 != c1
            f2t, t2f = s1 & ~c1, ~s1 & c1           # F2T: cross FAILs; T2F: same FAILs
            for lg, key, cmpf in (("H1", "H1", lambda v, b: v > b), ("H2", "H2", lambda v, b: v > b),
                                  ("DD", "MaxDD", lambda v, b: v >= b)):
                vals = {"H1": H1, "H2": H2, "MaxDD": DD}[key]
                fail_cross = ~cmpf(vals, bc[key]); fail_same = ~cmpf(vals, bs[key])
                rec[f"v1_leg_{lg}"] = int(np.sum(f2t & fail_cross) + np.sum(t2f & fail_same))
                rec[f"v1f2t_leg_{lg}"] = int(np.sum(f2t & fail_cross))
            # LOST / GAINED against the row's own published column, per convention
            if pv.notna().all():
                pvv = pv.values.astype(bool)
                for cv in CONVENTIONS:
                    rec[f"lost_{cv}"] = int(np.sum(pvv & ~got[cv]))
                    rec[f"gain_{cv}"] = int(np.sum(~pvv & got[cv]))
                # restricted to the rows the v1 convention can actually move
                rec["exp_lost_SAMEv1"] = int(np.sum(fl & pvv & ~s1))
                rec["exp_gain_SAMEv1"] = int(np.sum(fl & ~pvv & s1))
                rec["exp_lost_CROSSv1"] = int(np.sum(fl & pvv & ~c1))
                rec["exp_gain_CROSSv1"] = int(np.sum(fl & ~pvv & c1))
                rec["pub_on_exposed"] = int(np.sum(fl & pvv))
            crecs.append(rec)
            if fdate <= V2_LIVE and rec["n_exposed_v1"] > 0:
                ROWS.append(pd.DataFrame(dict(
                    file=fname, date=fdate, canon=canon,
                    published=(pv.values.astype(object) if pv.notna().all() else np.nan),
                    SAMEv1=s1, CROSSv1=c1, H1=H1, H2=H2, MaxDD=DD)).loc[fl])
    C = pd.DataFrame(crecs)
    C.to_csv(OUT.with_suffix(".census.csv"), index=False)
    mapped = C[C.mapped == True].copy()                                        # noqa: E712

    # 737's census population is the corpus AS IT STOOD WHEN 737 RAN.  The corpus has grown
    # since (this lane and the cloud lane committed more CSVs today), so the reproduction gate
    # is asserted on 737's OWN FILE SET, read off its committed census, and the current corpus
    # is reported beside it as the working population.
    ref_files = set(pd.read_csv(str(REF737) + ".census.csv").file.astype(str))
    C737 = C[C.file.isin(ref_files)]
    m737 = C737[C737.mapped == True]                                           # noqa: E712
    got737 = dict(qual_files=int(C737.file.nunique()),
                  qual_rows=int(sum(v for k, v in NROWS.items() if k in ref_files)),
                  canon_rows=int(m737.n.sum()), blocks_canon=int(len(m737)),
                  exposed_v1=int(m737.n_exposed_v1.sum()),
                  exposed_rows=int(m737.n_exposed.sum()),
                  flip_F2T=int(m737.n_flip_F2T.sum()), flip_T2F=int(m737.n_flip_T2F.sum()),
                  exposed_spy=int(m737.n_exposed_spy.sum()))
    P(f"\n  census reproduction on 737's OWN file set ({len(ref_files)} files named in its "
      f"committed .census.csv), against its committed summary.json:")
    g1_cens = True
    for k, v in G1_REF.items():
        ok = got737[k] == v; g1_cens &= ok
        P(f"    {k:13} got {got737[k]:>7d}  ref {v:>7d}  {'OK' if ok else 'MISMATCH'}")
    P(f"    v1 flips: cross-FAIL->same-PASS {int(m737.n_flip_v1_F2T.sum())}, "
      f"cross-PASS->same-FAIL {int(m737.n_flip_v1_T2F.sum())} (737 published 58,340 / 189)")
    # the queue's stated mechanism, verified to the published digit
    dd_u56, dd_s484 = COMP[("U56", "SAMEv1")]["MaxDD"], COMP[("SMALL484", "SAMEv1")]["MaxDD"]
    g1_mech = abs(dd_u56 - (-0.138)) < 5e-4 and abs(dd_s484 - (-0.448)) < 5e-4
    P(f"    queue's mechanism: RULES v1 MaxDD {dd_u56:.4f} on U56 vs {dd_s484:.4f} on SMALL484 "
      f"(queue says -13.8% / -44.8%) -> {'OK' if g1_mech else 'MISMATCH'}")
    P(f"\n  the CURRENT corpus (the working population for every later number): "
      f"{n_qual_files} qualifying files, {n_qual_rows} rows, {int(mapped.n.sum())} CANON rows in "
      f"{len(mapped)} blocks, v1-exposed {int(mapped.n_exposed_v1.sum())} "
      f"(F2T {int(mapped.n_flip_v1_F2T.sum())}, T2F {int(mapped.n_flip_v1_T2F.sum())}), "
      f"v2-exposed {int(mapped.n_exposed.sum())}")
    G1 = bool(g1_books and g1_cens and g1_mech)
    P(f"  G1 OVERALL: {'PASS' if G1 else 'FAIL'} (books {'ok' if g1_books else 'FAIL'}, "
      f"census {'ok' if g1_cens else 'FAIL'}, mechanism {'ok' if g1_mech else 'FAIL'})")
    P(f"  UNMAPPED panel labels: {len(unmapped)} distinct, {sum(unmapped.values())} rows; "
      f"rows dropped by a NA panel label (counted in qual_rows, absent from every block): "
      f"{sum(NADROP.values())} in {sum(1 for v in NADROP.values() if v)} file(s)")
    flush_log()

    # ------------------------------------------------------------ G2 VINTAGE
    P("\n" + "=" * 104)
    P("G2 VINTAGE: which convention does each filename DATE reproduce?  (row-weighted match rate)")
    P("=" * 104)
    mm = mapped.dropna(subset=[f"match_{cv}" for cv in CONVENTIONS])
    P(f"  {'date':11} {'rows':>7} " + " ".join(f"{cv:>13}" for cv in CONVENTIONS) + "   best")
    vint = []
    for d, g in mm.groupby("date"):
        w = {cv: float((g[f"match_{cv}"] * g.n).sum() / g.n.sum()) for cv in CONVENTIONS}
        best = max(w, key=w.get)
        P(f"  {d:11} {int(g.n.sum()):7d} " + " ".join(f"{w[cv]:13.4f}" for cv in CONVENTIONS)
          + f"   {best}")
        vint.append(dict(date=d, rows=int(g.n.sum()), best=best, **w))
    pd.DataFrame(vint).to_csv(OUT.with_suffix(".vintage.csv"), index=False)
    P(f"  -> the era cut at {V2_LIVE} is validated iff the pre-cut dates read a v1 candidate as "
      "best and the post-cut dates read a v2 one.")
    flush_log()

    # ------------------------------------------------------------ ROW SETS
    mapped["era"] = np.where(mapped.date < V2_LIVE, "V1ERA", "V2ERA")
    v1era = mapped[mapped.date < V2_LIVE]
    v1era6 = mapped[mapped.date <= V2_LIVE]
    v1exp = v1era[v1era.n_exposed_v1 > 0]
    v1ident = v1era[v1era.n_exact > 0]
    v1uniq_cross = v1era[v1era.identified == "CROSSv1"]

    P("\n" + "=" * 104)
    P("B1  IS THE 58,529 ACTUALLY THE PRE-2026-09-06 RECORD?")
    P("=" * 104)
    tot_exp = int(mapped.n_exposed_v1.sum())
    by_era = mapped.groupby("era").agg(blocks=("n", "size"), rows=("n", "sum"),
                                       exp_v1=("n_exposed_v1", "sum"),
                                       f2t=("n_flip_v1_F2T", "sum"), t2f=("n_flip_v1_T2F", "sum"))
    P(f"  {'era':7} {'blocks':>7} {'rows':>8} {'v1-exposed':>11} {'share of 58,529':>16} "
      f"{'cross-FAIL->same-PASS':>22} {'reverse':>8}")
    for e, r in by_era.iterrows():
        P(f"  {e:7} {int(r.blocks):7d} {int(r.rows):8d} {int(r.exp_v1):11d} "
          f"{r.exp_v1/max(tot_exp,1):16.2%} {int(r.f2t):22d} {int(r.t2f):8d}")
    share_v1era = float(by_era.loc["V1ERA", "exp_v1"] / max(tot_exp, 1)) if "V1ERA" in by_era.index else 0.0
    B1 = share_v1era >= B1_BAR
    P(f"  share of the v1-exposed rows that are pre-{V2_LIVE}: {share_v1era:.2%} vs bar {B1_BAR:.0%}")
    P(f"  B1: {'PASS' if B1 else 'FAIL'} - "
      + ("the exposure IS the old record" if B1 else
         "the exposure is overwhelmingly a COUNTERFACTUAL on v2-era rows that never quoted a v1 comparand"))
    P("\n  v1 exposure by canonical panel (all eras):")
    bp = mapped.groupby("canon").agg(rows=("n", "sum"), exp_v1=("n_exposed_v1", "sum"),
                                     f2t=("n_flip_v1_F2T", "sum"), t2f=("n_flip_v1_T2F", "sum"),
                                     exp_v2=("n_exposed", "sum"))
    for p, r in bp.iterrows():
        P(f"    {p:9} rows {int(r.rows):7d}  v1-exposed {int(r.exp_v1):6d} ({r.exp_v1/max(r.rows,1):6.2%})"
          f"  v2-exposed {int(r.exp_v2):5d} ({r.exp_v2/max(r.rows,1):6.2%})"
          f"  F2T {int(r.f2t):6d} T2F {int(r.t2f):4d}")
    P("    U56 is exactly 0 by construction: on U56, CROSSv1 IS SAMEv1 (same frame, same book).")
    flush_log()

    # ------------------------------------------------------------ B2 RESTATEMENT
    P("\n" + "=" * 104)
    P("B2  RESTATEMENT: how many PUBLISHED verdicts does the old record lose or gain?")
    P("     LOST = published PASS -> restated FAIL;  GAINED = published FAIL -> restated PASS")
    P("=" * 104)
    tiers = {
        "CANON737": mapped,
        "V1ERA": v1era,
        "V1ERA6": v1era6,
        "V1ERA_EXPOSED": v1exp,
        "V1ERA_IDENT": v1ident,
        "V1ERA_UNIQ_CROSSv1": v1uniq_cross,
    }
    tr = []
    P(f"  {'tier':20} {'blocks':>7} {'rows':>8} {'scorable':>9} {'pub PASS':>9} | "
      + " ".join(f"{cv[:11]:>13}" for cv in CONVENTIONS))
    P(f"  {'':20} {'':>7} {'':>8} {'':>9} {'':>9} | "
      + " ".join(f"{'lost/gain':>13}" for _ in CONVENTIONS))
    for tname, T in tiers.items():
        sc = T.dropna(subset=["pub_rate"])
        nrows = int(T.n.sum()); nsc = int(sc.n.sum())
        npub = int((sc.pub_rate * sc.n).sum()) if nsc else 0
        cells = []
        d = dict(tier=tname, blocks=len(T), rows=nrows, scorable=nsc, pub_pass=npub)
        for cv in CONVENTIONS:
            lo = int(sc[f"lost_{cv}"].sum()) if nsc else 0
            ga = int(sc[f"gain_{cv}"].sum()) if nsc else 0
            cells.append(f"{lo:6d}/{ga:6d}")
            d[f"lost_{cv}"], d[f"gain_{cv}"] = lo, ga
        P(f"  {tname:20} {len(T):7d} {nrows:8d} {nsc:9d} {npub:9d} | " + " ".join(cells))
        tr.append(d)
    pd.DataFrame(tr).to_csv(OUT.with_suffix(".restate.csv"), index=False)

    P("\n  the same, restricted to the rows the v1 convention CAN move (SAMEv1 != CROSSv1):")
    for tname in ["CANON737", "V1ERA", "V1ERA6", "V1ERA_EXPOSED", "V1ERA_IDENT"]:
        sc = tiers[tname].dropna(subset=["pub_rate"])
        if not len(sc): P(f"    {tname:20} no scorable block"); continue
        ex = int(sc.n_exposed_v1.sum()); pe = int(sc.pub_on_exposed.sum())
        P(f"    {tname:20} exposed rows {ex:6d}  published PASS among them {pe:6d}  "
          f"SAMEv1 lost/gain {int(sc.exp_lost_SAMEv1.sum()):5d}/{int(sc.exp_gain_SAMEv1.sum()):5d}  "
          f"CROSSv1 lost/gain {int(sc.exp_lost_CROSSv1.sum()):5d}/{int(sc.exp_gain_CROSSv1.sum()):5d}")

    P("\n  IDENTIFICATION of the v1-era blocks (which comparand does the old record provably quote?):")
    idc = {}
    for _, r in v1era.iterrows():
        idc[r.identified if r.identified else "<none>"] = \
            idc.get(r.identified if r.identified else "<none>", 0) + int(r.n)
    for k, v in sorted(idc.items(), key=lambda kv: -kv[1]):
        P(f"    {k if k else '<none>':52} {v:7d} rows")
    uniq_v1 = v1era[v1era.n_exact == 1]
    P(f"    v1-era blocks UNIQUELY identified: {len(uniq_v1)} ({int(uniq_v1.n.sum())} rows) -> "
      + (", ".join(f"{k} {int(g.n.sum())}" for k, g in uniq_v1.groupby('identified')) or "none"))
    B2 = len(v1uniq_cross) >= 1
    P(f"  B2: {'PASS' if B2 else 'FAIL'} - v1-era blocks uniquely identified as CROSSv1: "
      f"{len(v1uniq_cross)} ({int(v1uniq_cross.n.sum())} rows)")
    if not B2:
        P("      -> NO committed pre-2026-09-06 block can be shown to have used the cross-panel v1")
        P("         comparand, so NO published verdict is established to need restating.")

    # the CLAIM-level reading: a block is one idea, a row is one grid cell
    P("\n  CLAIM-LEVEL (a block is one idea, a row is one of its grid cells):")
    for tname in ["V1ERA", "V1ERA_IDENT"]:
        sc = tiers[tname].dropna(subset=["pub_rate"])
        if not len(sc): continue
        for cv in V1_PAIR:
            touched = sc[(sc[f"lost_{cv}"] > 0) | (sc[f"gain_{cv}"] > 0)]
            P(f"    {tname:14} restated on {cv:8}: {len(touched):3d} of {len(sc):3d} blocks change at "
              f"least one cell ({len(touched)/max(len(sc),1):6.1%}); blocks that LOSE a published "
              f"PASS {int((sc[f'lost_{cv}'] > 0).sum()):3d}")

    P("\n  every v1-era block with v1 exposure, restated (published rate -> same-panel v1 rate):")
    P(f"    {'file':70} {'panel':9} {'n':>6} {'exp':>5} {'pub':>7} {'SAMEv1':>7} {'CROSSv1':>7} "
      f"{'lost':>5} {'gain':>5} {'ident':>22}")
    for _, r in v1exp.sort_values("n_exposed_v1", ascending=False).iterrows():
        pr = f"{r.pub_rate:.4f}" if pd.notna(r.pub_rate) else "   n/a"
        lo = f"{int(r.lost_SAMEv1):5d}" if pd.notna(r.pub_rate) else "  n/a"
        ga = f"{int(r.gain_SAMEv1):5d}" if pd.notna(r.pub_rate) else "  n/a"
        P(f"    {r.file[:70]:70} {r.panel_label:9} {int(r.n):6d} {int(r.n_exposed_v1):5d} {pr:>7} "
          f"{r['rate_SAMEv1']:7.4f} {r['rate_CROSSv1']:7.4f} {lo} {ga} "
          f"{(r.identified or '-')[:22]:>22}")
    flush_log()

    # ------------------------------------------------------------ B3 LEG
    P("\n" + "=" * 104)
    P("B3  WHICH 4a LEG BINDS on the v1 flips?  (the leg that FAILS on the failing side:")
    P("     a SAMEv1-PASS / CROSSv1-FAIL row is scored on its CROSSv1 legs, and vice versa)")
    P("=" * 104)
    lh1, lh2, ldd = (int(mapped.v1_leg_H1.sum()), int(mapped.v1_leg_H2.sum()),
                     int(mapped.v1_leg_DD.sum()))
    P(f"  over all {tot_exp} v1-exposed rows: H1 binds {lh1} ({lh1/max(tot_exp,1):.2%}), "
      f"H2 {lh2} ({lh2/max(tot_exp,1):.2%}), MaxDD {ldd} ({ldd/max(tot_exp,1):.2%})")
    P("  (legs are not exclusive: a row can fail several)")
    B3 = ldd / max(tot_exp, 1) >= B3_BAR
    P(f"  B3: {'PASS' if B3 else 'FAIL'} - MaxDD share {ldd/max(tot_exp,1):.2%} vs bar {B3_BAR:.0%}")
    P(f"  {'panel':9} {'exposed':>8} {'H1':>8} {'H2':>8} {'MaxDD':>8} | MaxDD spread SAMEv1-CROSSv1")
    for p, g in mapped.groupby("canon"):
        e = int(g.n_exposed_v1.sum())
        if not e: continue
        P(f"  {p:9} {e:8d} {int(g.v1_leg_H1.sum()):8d} {int(g.v1_leg_H2.sum()):8d} "
          f"{int(g.v1_leg_DD.sum()):8d} | "
          f"{COMP[(p,'SAMEv1')]['MaxDD'] - COMP[(p,'CROSSv1')]['MaxDD']:+.4f}")
    flush_log()

    # ------------------------------------------------------------ 324-book audit population
    P("\n" + "=" * 104)
    P("THE AUDIT POPULATION (737's 324 books): 4a under every convention, 4b once")
    P("=" * 104)
    for cv in CONVENTIONS:
        G[f"p4a_{cv}"] = [pass4a(r.H1, r.H2, r.MaxDD, COMP[(r.panel, cv)]) for r in G.itertuples()]
    G["p4b"] = [pass4b(r.CAGR, r.H1, r.H2, r.MaxDD, r.oSharpe, SPYS[r.panel]) for r in G.itertuples()]
    P(f"  {'convention':14} {'4a ALL':>8} " + " ".join(f"{p:>10}" for p in ["U56", "B136", "SMALL439"]))
    for cv in CONVENTIONS:
        per = G.groupby("panel")[f"p4a_{cv}"].sum()
        P(f"  {cv:14} {int(G[f'p4a_{cv}'].sum()):8d} "
          + " ".join(f"{int(per.get(p,0)):10d}" for p in ["U56", "B136", "SMALL439"]))
    P(f"  4b (SPY comparand, panel-local in every convention): {int(G.p4b.sum())}/324  "
      + " ".join(f"{p}={int(G.groupby('panel').p4b.sum().get(p,0))}" for p in ["U56","B136","SMALL439"]))
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)

    b4_changes = 0
    ref4b = G.p4b.values
    for cv in CONVENTIONS:
        chk = np.array([pass4b(r.CAGR, r.H1, r.H2, r.MaxDD, r.oSharpe, SPYS[r.panel])
                        for r in G.itertuples()])
        b4_changes += int(np.sum(chk != ref4b))
    B4 = b4_changes == 0
    P(f"\n  B4 4b UNTOUCHED: rows whose 4b changes across the 6 candidates: {b4_changes} -> "
      f"{'PASS' if B4 else 'FAIL'}")
    flush_log()

    # ------------------------------------------------------------ RULE 8
    P("\n" + "=" * 104)
    P("RULE 8 WALK-FORWARD: 12 arms = 3 panels x 2 families x 2 constructions.")
    P("  (level, cadence) chosen on IS Sharpe 2010..2016 ALONE; 2017+ read ONCE.")
    P("=" * 104)
    wf = []
    for pname in ["U56", "B136", "SMALL439"]:
        for family in FAMILIES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == pname) & (G.family == family) & (G.con == con)]
                pk = sub.loc[sub.isSharpe.idxmax()]
                wf.append(dict(panel=pname, family=family, con=con, level=pk.level, cad=pk.cad,
                               isSharpe=pk.isSharpe, oCAGR=pk.oCAGR, oSharpe=pk.oSharpe,
                               oMaxDD=pk.oMaxDD, CAGR=pk.CAGR, Sharpe=pk.Sharpe, MaxDD=pk.MaxDD,
                               H1=pk.H1, H2=pk.H2,
                               **{f"p4a_{cv}": bool(pk[f"p4a_{cv}"]) for cv in CONVENTIONS},
                               p4b=bool(pk.p4b)))
    W = pd.DataFrame(wf)
    P(f"  {'panel':9} {'family':10} {'con':9} {'lvl':>6} {'cad':>3} {'isS':>7} | {'oCAGR':>7} "
      f"{'oSharpe':>7} {'oMaxDD':>7} | {'4a S1':>6} {'4a C1':>6} {'4a S2':>6} {'4b':>5}")
    for r in W.itertuples():
        P(f"  {r.panel:9} {r.family:10} {r.con:9} {r.level:6.2f} {r.cad:>3} {r.isSharpe:7.4f} | "
          f"{r.oCAGR:7.4f} {r.oSharpe:7.4f} {r.oMaxDD:7.4f} | {str(r.p4a_SAMEv1):>6} "
          f"{str(r.p4a_CROSSv1):>6} {str(r.p4a_SAMEv2):>6} {str(r.p4b):>5}")
    P("\n  OOS comparands the 12 picks are judged against:")
    P(f"  {'panel':9} " + " ".join(f"{cv[:12]:>13}" for cv in CONVENTIONS) + f" {'SPY':>13}")
    for pname in ["U56", "B136", "SMALL439"]:
        P(f"  {pname:9} " + " ".join(f"{COMP[(pname,cv)]['oSharpe']:13.4f}" for cv in CONVENTIONS)
          + f" {SPYS[pname]['oSharpe']:13.4f}")
    for cv in CONVENTIONS:
        W[f"beats_{cv}_oos"] = [r.oSharpe > COMP[(r.panel, cv)]["oSharpe"] for r in W.itertuples()]
    W["beats_spy_oos"] = [r.oSharpe > SPYS[r.panel]["oSharpe"] for r in W.itertuples()]
    W["spy_oCAGR"] = [SPYS[r.panel]["oCAGR"] for r in W.itertuples()]
    W["spy_oMaxDD"] = [SPYS[r.panel]["oMaxDD"] for r in W.itertuples()]
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    P(f"\n  OOS Sharpe {W.oSharpe.min():.4f}..{W.oSharpe.max():.4f}; OOS CAGR "
      f"{W.oCAGR.min():.2%}..{W.oCAGR.max():.2%}; OOS MaxDD {W.oMaxDD.min():.2%}..{W.oMaxDD.max():.2%}")
    P("  beats OOS Sharpe: " + ", ".join(f"{cv} {int(W[f'beats_{cv}_oos'].sum())}/12" for cv in CONVENTIONS)
      + f", SPY {int(W.beats_spy_oos.sum())}/12")
    n_s1, n_c1 = int(W.p4a_SAMEv1.sum()), int(W.p4a_CROSSv1.sum())
    P("  4a on the 12 picks: " + ", ".join(f"{cv} {int(W[f'p4a_{cv}'].sum())}/12" for cv in CONVENTIONS)
      + f"; 4b {int(W.p4b.sum())}/12")
    B5 = n_s1 != n_c1
    P(f"  B5: {'PASS (the v1 convention changes a fresh decision)' if B5 else 'FAIL (same count)'}")
    flush_log()

    # ------------------------------------------------------------ verdict
    P("\n" + "=" * 104)
    P("BOTH KEEP PATHS")
    P("=" * 104)
    for cv in CONVENTIONS:
        P(f"  4a {cv:14} {int(G[f'p4a_{cv}'].sum()):3d}/324 (audit population)   "
          f"{int(W[f'p4a_{cv}'].sum()):2d}/12 (rule-8 picks)")
    P(f"  4b (convention-invariant) {int(G.p4b.sum())}/324 (audit)   {int(W.p4b.sum())}/12 (rule-8)")
    P("\nGATES: G1 %s | B1 %s | B2 %s | B3 %s | B4 %s | B5 %s" %
      tuple("PASS" if x else "FAIL" for x in (G1, B1, B2, B3, B4, B5)))

    sc_all = mapped.dropna(subset=["pub_rate"])
    sc_v1 = v1era.dropna(subset=["pub_rate"])
    summ = dict(G1=G1, B1=B1, B2=B2, B3=B3, B4=B4, B5=B5,
                **got737,
                flip_v1_F2T=int(mapped.n_flip_v1_F2T.sum()),
                flip_v1_T2F=int(mapped.n_flip_v1_T2F.sum()),
                v1era_blocks=int(len(v1era)), v1era_rows=int(v1era.n.sum()),
                v1era_exposed=int(v1era.n_exposed_v1.sum()),
                v1era_share_of_exposed=round(share_v1era, 6),
                v1era6_exposed=int(v1era6.n_exposed_v1.sum()),
                v1era_scorable_rows=int(sc_v1.n.sum()),
                v1era_lost_SAMEv1=int(sc_v1.lost_SAMEv1.sum()),
                v1era_gain_SAMEv1=int(sc_v1.gain_SAMEv1.sum()),
                v1era_lost_CROSSv1=int(sc_v1.lost_CROSSv1.sum()),
                v1era_gain_CROSSv1=int(sc_v1.gain_CROSSv1.sum()),
                v1era_exp_lost_SAMEv1=int(sc_v1.exp_lost_SAMEv1.sum()),
                v1era_exp_gain_SAMEv1=int(sc_v1.exp_gain_SAMEv1.sum()),
                v1era_blocks_uniq_CROSSv1=int(len(v1uniq_cross)),
                v1era_rows_uniq_CROSSv1=int(v1uniq_cross.n.sum()),
                v1era_blocks_identified=int(len(v1ident)),
                v1era_rows_identified=int(v1ident.n.sum()),
                all_lost_SAMEv1=int(sc_all.lost_SAMEv1.sum()),
                all_gain_SAMEv1=int(sc_all.gain_SAMEv1.sum()),
                leg_H1=lh1, leg_H2=lh2, leg_DD=ldd,
                p4b_324=int(G.p4b.sum()), wf_4b=int(W.p4b.sum()),
                corpus_qual_files=n_qual_files, corpus_qual_rows=int(n_qual_rows),
                corpus_canon_rows=int(mapped.n.sum()), corpus_blocks=int(len(mapped)),
                corpus_exposed_v1=tot_exp,
                **{f"p4a_{cv}_324": int(G[f"p4a_{cv}"].sum()) for cv in CONVENTIONS},
                **{f"wf_4a_{cv}": int(W[f"p4a_{cv}"].sum()) for cv in CONVENTIONS},
                runtime_s=round(time.time() - t0, 1))
    OUT.with_suffix(".summary.json").write_text(json.dumps(summ, indent=2, default=str))
    P(f"\nruntime {summ['runtime_s']}s")
    flush_log()
    return summ


if __name__ == "__main__":
    main()
