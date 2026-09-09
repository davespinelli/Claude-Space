#!/usr/bin/env python3
"""Idea 299 - "pre-register-the-quantile-family-as-a-dial" (cloud lane, 2026-09-09).

The question
------------
Idea 298 PARKed a by-product: U56, top-50% by distance above the 200d MA, equal weight,
MONTHLY, 75% gross, which clears PROTOCOL 4b at 15.53% CAGR / 1.2400 Sharpe / -19.80% MaxDD
(OOS Sharpe 1.2237).  It was PARKed and not KEPT because reaching it needed THREE dials --
gate family, strictness x, AND cadence -- while PROTOCOL rule 4 allows two.

The queue's instruction is exact: re-run with FAMILY and x as THE two pre-registered dials at
the record's WEEKLY default, and require the 4b pass on U56 AND B136, with MaxDD clearing the
cap by more than 1 pp.  That is a harder bar than 4b as written, and it is the whole test:
a book that only clears the drawdown cap by 0.4 pp on one panel and needs a third dial to get
there is a grid artefact, not a rule worth capital.

Design (nothing here is chosen after the fact)
----------------------------------------------
FIXED before the run, at the record's own defaults, never varied:
    cadence   W (weekly)                          <- the record default; the third dial, closed
    book      RESPREAD, i.e. equal weight across the held names at 75% gross (idea 298's book)
    costs     10 bps per unit turnover, next-day execution, no shorting, no leverage
    windows   IS <= 2016-12-31, OOS >= 2017-01-01 (PROTOCOL rule 8)
    panels    U56 and B136 are the two REQUIRED panels; SMALL439 is reported, never required

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. FAMILY, 3 values -- the gate form:
         QUANTILE    hold the top x fraction of live names by distance px/ma200 - 1
         MA-THRESH   hold every name with px > ma200 * (1 + theta)
         QUANTxMA    hold the top x fraction by that distance AND above ma200
                     (the literal reading of idea 298's "top-50%-ABOVE-MA200"; it is the
                      interpolation of the other two and is reported beside them)
    2. x, 9 values -- strictness.  x in {0.20 .. 0.95} for the two quantile families (the
       record's QUANT_X), theta in {+0.30 .. -0.40} for MA-THRESH (the record's MA_THETA).
    3 x 9 x 3 panels = 81 pre-registered books; the DEGROSS construction of each is computed
    and reported as a CONTROL column (162 books in the grid) but is NOT a dial: the KEEP
    claim, if any, may only come from the pre-registered RESPREAD book.

Pre-registered bars, written before any number was read
--------------------------------------------------------
A1  THE QUEUE'S BAR.  Some (family, x) must pass 4b on U56 AND on B136 in the SAME cell, with
    the drawdown cap cleared by > 1.00 pp on BOTH: |MaxDD| <= 0.60*|SPY MaxDD| - 1.00 pp.
    Anything less is PARK or KILL, not KEEP.
A2  RULE 8.  x is chosen inside each family on 2010..2016 IS Sharpe ONLY (pooled over the two
    required panels by mean IS Sharpe, and also per panel, both reported); 2017..end is read
    ONCE.  A KEEP additionally requires the walk-forward-chosen cell to clear 4b's OOS leg on
    both required panels.  A cell that clears A1 only when x is chosen on the full sample is
    PARK, not KEEP.
A3  REPRODUCTION.  The 108 (panel x {QUANTILE, MA-THRESH} x level x W x construction) cells
    that idea 301 has already committed are re-asserted against its .grid.csv at 1e-6 on
    CAGR / Sharpe / MaxDD before any new number is read.  Idea 301 recorded a U56 disagreement
    with idea 298 attributable to the daily drift of data/prices.csv (ideas 513/515); the same
    allowance is stated here, and the gate is reported per panel so it cannot hide.

Also reported, never selected on: a 25 bps cost rung, DERIVED exactly from the same book
(r25 = r10 - turnover * 15/1e4), because the record's 4b passes on U56 have historically been
cost-fragile (idea 460).  It is a robustness column, not a dial.

Verdicts (both KEEP paths, on every one of the 162 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe.json (U56), universe_broad.json (B136) and prices_small.csv.gz
(SMALL439) are CURRENT constituents -- no delistings -- so every CAGR level here is inflated
and both KEEP columns inherit that whole.  SMALL439 additionally drops every ticker with
max_1d_move >= 1.0 in data/small_meta.csv before use.  Any KEEP memo written off this run must
carry that caveat.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .walkforward.csv .a1.csv .console.txt .result.md
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

COST_BPS = 10
COST_BPS_ROBUST = 25
GROSS = 0.75
CADENCE = "W"                     # FIXED: the record default.  The third dial, closed.
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]     # RESPREAD is pre-registered; DEGROSS is a control
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH", "QUANTxMA"]
REQUIRED_PANELS = ["U56", "B136"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

A1_MARGIN_PP = 1.00               # the queue's own bar: clear the DD cap by more than 1 pp
A3_TOL = 1e-6
REF301 = REPO / "research" / "backtests" / (
    "2026-09-09_is-the-gate-timing-residual-a-constant-in-pp-per-year_B.grid.csv")

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 700)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- constructions (idea 298/301)
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for max_1d_move >= 1.0)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    """QUANTILE and MA-THRESH are idea 301's code verbatim; QUANTxMA is their intersection."""
    live = live_mask(px)
    ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(level * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    q = rank.le(kt, axis=0).fillna(False) & live
    if family == "QUANTILE":
        return q
    return q & (px > ma)                                    # QUANTxMA


def book(px, family, level, construction):
    g = gate_mask(px, family, level)
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def bars_4b(s, spy):
    return {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
            "OOS": s["oSharpe"] > spy["oSharpe"],
            "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
            "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}


def fail_4b(s, spy):
    f = [k for k, v in bars_4b(s, spy).items() if not v]
    return ",".join(f) if f else "-"


# ---------------------------------------------------------------- main
def main():
    PN = panels()
    P("=" * 175)
    P("Idea 299 pre-register-the-quantile-family-as-a-dial (cloud) | " + Path(__file__).name)
    P("=" * 175)
    P(f"FIXED: cadence {CADENCE} (record default), book RESPREAD @ gross {GROSS}, costs "
      f"{COST_BPS} bps, next-day execution, IS <= {IS_END}, OOS >= {OOS_START}.")
    P(f"DIALS (2): FAMILY {FAMILIES} x x/theta (9 levels each) = 27 cells per panel; DEGROSS "
      f"is a reported CONTROL, never a dial.  A {COST_BPS_ROBUST} bps rung is DERIVED, not a dial.")
    P(f"A1 (the queue's bar): some (family, x) passes 4b on {REQUIRED_PANELS[0]} AND "
      f"{REQUIRED_PANELS[1]} with the DD cap cleared by > {A1_MARGIN_PP:.2f} pp on both.")
    P("A2 (rule 8): x chosen on IS Sharpe only; OOS read once; the pick must clear 4b's OOS leg.")
    P(f"A3 (reproduction): idea 301's committed weekly cells re-asserted at {A3_TOL} on "
      f"CAGR/Sharpe/MaxDD before any new number is read.")

    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]

    rows, panel_spy, panel_live, panel_ctrl = [], {}, {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        rc = backtest(px, control_book(px), cost_bps=COST_BPS, freq=CADENCE)
        ctrl_s = stat(rc["returns"].loc[start:])
        panel_spy[pname], panel_live[pname], panel_ctrl[pname] = spy_s, live_s, ctrl_s
        P("\n" + "-" * 175)
        P(f"PANEL {pname}: evaluation from {start.date()} ({years:.2f} yrs)"
          f"{'  [REQUIRED]' if pname in REQUIRED_PANELS else '  [reported, not required]'}")
        P(f"  SPY      CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f}")
        P(f"  RULES v2 CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} MaxDD {live_s['MaxDD']:.4f} "
          f"halves {live_s['H1']:.4f}/{live_s['H2']:.4f} OOS Sharpe {live_s['oSharpe']:.4f} "
          f"OOS CAGR {live_s['oCAGR']:.4f}")
        P(f"  EWall {CADENCE} control  CAGR {ctrl_s['CAGR']:.4f} Sharpe {ctrl_s['Sharpe']:.4f} "
          f"MaxDD {ctrl_s['MaxDD']:.4f} OOS Sharpe {ctrl_s['oSharpe']:.4f}")
        cap = 0.60 * abs(spy_s["MaxDD"])
        P(f"  4b bars: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} OOS>{spy_s['oSharpe']:.4f} "
          f"|MaxDD|<={cap:.2%} (A1 needs <={cap-A1_MARGIN_PP/100:.2%}) CAGR>={0.70*spy_s['CAGR']:.2%}")
        flush_log()

        for family in FAMILIES:
            levels = MA_THETA if family == "MA-THRESH" else QUANT_X
            for level in levels:
                g = gate_mask(px, family, level)
                nheld = g.sum(axis=1).loc[start:]
                for con in CONSTRUCTIONS:
                    res = backtest(px, book(px, family, level, con), cost_bps=COST_BPS,
                                   freq=CADENCE)
                    r10 = res["returns"].loc[start:]
                    turn = res["turnover"].loc[start:]
                    r25 = r10 - turn * (COST_BPS_ROBUST - COST_BPS) / 1e4
                    s, s25 = stat(r10), stat(r25)
                    b = bars_4b(s, spy_s)
                    rows.append(dict(
                        panel=pname, family=family, level=level, cad=CADENCE, con=con, **s,
                        gross_mean=float(res["weights"].loc[start:].sum(axis=1).mean()),
                        nheld_mean=float(nheld.mean()), turn_yr=float(turn.sum() / years),
                        p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s),
                        dd_margin_pp=100 * (0.60 * abs(spy_s["MaxDD"]) - abs(s["MaxDD"])),
                        **{f"b4b_{k}": v for k, v in b.items()},
                        Sharpe25=s25["Sharpe"], CAGR25=s25["CAGR"], MaxDD25=s25["MaxDD"],
                        H1_25=s25["H1"], H2_25=s25["H2"], oSharpe25=s25["oSharpe"],
                        f4b_25=fail_4b(s25, spy_s),
                        dSharpe_ctrl=s["Sharpe"] - ctrl_s["Sharpe"],
                        dSharpe_live=s["Sharpe"] - live_s["Sharpe"],
                        spy_Sharpe=spy_s["Sharpe"], spy_oSharpe=spy_s["oSharpe"],
                        spy_MaxDD=spy_s["MaxDD"], spy_CAGR=spy_s["CAGR"],
                        live_oSharpe=live_s["oSharpe"], ctrl_oSharpe=ctrl_s["oSharpe"]))
            P(f"  ... {pname} / {family} done ({len(levels)*len(CONSTRUCTIONS)} books)")
            flush_log()

    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    G["p4b_25"] = G.f4b_25 == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------- A3 reproduction gate, first
    P("\n" + "=" * 175)
    P("A3 REPRODUCTION GATE vs idea 301's committed .grid.csv (asserted before any new number)")
    P("=" * 175)
    key = ["panel", "family", "level", "cad", "con"]
    ref = pd.read_csv(REF301)
    ref = ref[(ref.cad == CADENCE) & (ref.family.isin(["QUANTILE", "MA-THRESH"]))]
    m = G.merge(ref[key + ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]], on=key,
                suffixes=("", "_ref"))
    for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]:
        m[f"d_{c}"] = (m[c] - m[f"{c}_ref"]).abs()
    dcols = [f"d_{c}" for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oSharpe"]]
    P(f"  matched rows: {len(m)} of {len(ref)} committed weekly cells")
    P(fmt(m.groupby("panel")[dcols].max(), 10))
    a3max = float(m[dcols].max().max())
    a3 = a3max < A3_TOL
    P(f"  max |d| over all six columns = {a3max:.3e}  ->  A3 {'PASS' if a3 else 'FAIL'} at {A3_TOL}")
    if not a3:
        P("  A3 FAILED -- the panels that differ are named above; results below are this run's "
          "own recomputation and must not be read as a restatement of idea 301 on those panels.")
    flush_log()

    # ---------------- the full pre-registered grid
    P("\n" + "=" * 175)
    P(f"THE 81 PRE-REGISTERED BOOKS (RESPREAD, {CADENCE}, gross {GROSS}, {COST_BPS} bps) -- "
      f"EVERY grid point, no selection")
    P("=" * 175)
    show = ["family", "level", "nheld_mean", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR",
            "oSharpe", "oMaxDD", "turn_yr", "dd_margin_pp", "p4a", "f4b", "f4b_25"]
    for pname in PN:
        sub = G[(G.panel == pname) & (G.con == "RESPREAD")]
        P(f"\n  PANEL {pname}  (SPY Sharpe {panel_spy[pname]['Sharpe']:.4f}, RULES v2 "
          f"{panel_live[pname]['Sharpe']:.4f}, DD cap {0.6*abs(panel_spy[pname]['MaxDD']):.2%})")
        P(fmt(sub[show].set_index(["family", "level"]), 4))
    P("\n  the DEGROSS control (not a dial; reported so the de-grossed twin of every book is "
      "visible):")
    for pname in PN:
        sub = G[(G.panel == pname) & (G.con == "DEGROSS")]
        P(f"\n  PANEL {pname}")
        P(fmt(sub[show].set_index(["family", "level"]), 4))
    flush_log()

    # ---------------- A1
    P("\n" + "=" * 175)
    P(f"A1 THE QUEUE'S BAR: 4b on {REQUIRED_PANELS} in the SAME (family, x) cell, DD cap "
      f"cleared by > {A1_MARGIN_PP} pp on both")
    P("=" * 175)
    R = G[(G.con == "RESPREAD")]
    piv = []
    for (fam, lv), g in R.groupby(["family", "level"]):
        rec = dict(family=fam, level=lv)
        ok_all, ok_margin = True, True
        for pn in REQUIRED_PANELS:
            row = g[g.panel == pn]
            if len(row) != 1:
                ok_all = False
                continue
            row = row.iloc[0]
            rec[f"{pn}_Sharpe"] = row.Sharpe
            rec[f"{pn}_MaxDD"] = row.MaxDD
            rec[f"{pn}_ddmargin"] = row.dd_margin_pp
            rec[f"{pn}_f4b"] = row.f4b
            ok_all &= bool(row.p4b)
            ok_margin &= bool(row.dd_margin_pp > A1_MARGIN_PP)
        rec["both_4b"] = ok_all
        rec["both_margin"] = ok_margin
        rec["A1"] = ok_all and ok_margin
        piv.append(rec)
    A1 = pd.DataFrame(piv).set_index(["family", "level"])
    A1.to_csv(f"{OUT}.a1.csv")
    P(fmt(A1, 4))
    a1_pass = list(A1.index[A1.A1])
    n_both4b = int(A1.both_4b.sum())
    P(f"\n  cells clearing 4b on BOTH required panels: {n_both4b} of {len(A1)}")
    P(f"  cells ALSO clearing the {A1_MARGIN_PP} pp drawdown margin on both: {len(a1_pass)}"
      f"  ->  A1 {'PASS' if a1_pass else 'FAIL'}")
    if a1_pass:
        P(f"  A1 cells: {a1_pass}")
    # per-panel 4b counts, for the record
    P("\n  4b passes among the 27 pre-registered books per panel (RESPREAD, weekly):")
    P(fmt(R.groupby(["panel", "family"]).p4b.sum().unstack(fill_value=0), 0))
    P("  the same at 25 bps (derived):")
    P(fmt(R.groupby(["panel", "family"]).p4b_25.sum().unstack(fill_value=0), 0))
    P("\n  4b failing-bar counts over the 81 pre-registered books (SET semantics):")
    bar = pd.Series([b for s in R.f4b for b in (s.split(",") if s != "-" else [])]).value_counts()
    P(fmt(bar.to_frame("n_books"), 0))
    flush_log()

    # ---------------- A2 rule 8
    P("\n" + "=" * 175)
    P("A2 RULE 8 WALK-FORWARD: x chosen inside each family on IS Sharpe (<= 2016) ONLY; "
      "2017..end read ONCE")
    P("=" * 175)
    wf = []
    # (a) pooled pick over the two required panels
    pool = R[R.panel.isin(REQUIRED_PANELS)].groupby(["family", "level"]).isSharpe.mean()
    for fam in FAMILIES:
        lv = pool[fam].idxmax()
        for pn in list(PN):
            row = R[(R.panel == pn) & (R.family == fam) & (R.level == lv)].iloc[0]
            spy_s, live_s = panel_spy[pn], panel_live[pn]
            wf.append(dict(pick="POOLED-IS", family=fam, level=lv, panel=pn,
                           isSharpe=row.isSharpe, oCAGR=row.oCAGR, oSharpe=row.oSharpe,
                           oMaxDD=row.oMaxDD, spy_oCAGR=spy_s["oCAGR"],
                           spy_oSharpe=spy_s["oSharpe"], spy_oMaxDD=spy_s["oMaxDD"],
                           live_oCAGR=live_s["oCAGR"], live_oSharpe=live_s["oSharpe"],
                           ctrl_oSharpe=panel_ctrl[pn]["oSharpe"],
                           beats_SPY_oos=row.oSharpe > spy_s["oSharpe"],
                           beats_LIVE_oos=row.oSharpe > live_s["oSharpe"],
                           beats_CTRL_oos=row.oSharpe > panel_ctrl[pn]["oSharpe"],
                           full_Sharpe=row.Sharpe, full_CAGR=row.CAGR, full_MaxDD=row.MaxDD,
                           dd_margin_pp=row.dd_margin_pp, p4a=row.p4a, p4b=row.p4b, f4b=row.f4b))
    # (b) per-panel pick
    for (pn, fam), g in R.groupby(["panel", "family"]):
        row = g.loc[g.isSharpe.idxmax()]
        spy_s, live_s = panel_spy[pn], panel_live[pn]
        wf.append(dict(pick="PANEL-IS", family=fam, level=row.level, panel=pn,
                       isSharpe=row.isSharpe, oCAGR=row.oCAGR, oSharpe=row.oSharpe,
                       oMaxDD=row.oMaxDD, spy_oCAGR=spy_s["oCAGR"],
                       spy_oSharpe=spy_s["oSharpe"], spy_oMaxDD=spy_s["oMaxDD"],
                       live_oCAGR=live_s["oCAGR"], live_oSharpe=live_s["oSharpe"],
                       ctrl_oSharpe=panel_ctrl[pn]["oSharpe"],
                       beats_SPY_oos=row.oSharpe > spy_s["oSharpe"],
                       beats_LIVE_oos=row.oSharpe > live_s["oSharpe"],
                       beats_CTRL_oos=row.oSharpe > panel_ctrl[pn]["oSharpe"],
                       full_Sharpe=row.Sharpe, full_CAGR=row.CAGR, full_MaxDD=row.MaxDD,
                       dd_margin_pp=row.dd_margin_pp, p4a=row.p4a, p4b=row.p4b, f4b=row.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["pick", "family", "panel"])[
        ["level", "isSharpe", "oCAGR", "oSharpe", "oMaxDD", "spy_oCAGR", "spy_oSharpe",
         "live_oSharpe", "ctrl_oSharpe", "beats_SPY_oos", "beats_LIVE_oos", "beats_CTRL_oos",
         "dd_margin_pp", "p4a", "p4b"]], 4))
    req = WF[WF.panel.isin(REQUIRED_PANELS)]
    P(f"\n  on the required panels: WF picks beat SPY OOS {int(req.beats_SPY_oos.sum())}/{len(req)}, "
      f"RULES v2 {int(req.beats_LIVE_oos.sum())}/{len(req)}, the EWall control "
      f"{int(req.beats_CTRL_oos.sum())}/{len(req)}")
    a2_ok = []
    for (pick, fam), g in WF[WF.panel.isin(REQUIRED_PANELS)].groupby(["pick", "family"]):
        if bool(g.p4b.all()) and bool((g.dd_margin_pp > A1_MARGIN_PP).all()):
            a2_ok.append((pick, fam, list(g.level.unique())))
    P(f"  A2: walk-forward-chosen cells clearing 4b + the {A1_MARGIN_PP} pp margin on BOTH "
      f"required panels: {a2_ok if a2_ok else 'none'}  ->  {'PASS' if a2_ok else 'FAIL'}")
    flush_log()

    # ---------------- both KEEP paths over the whole grid
    P("\n" + "=" * 175)
    P("BOTH KEEP PATHS over all 162 books (81 pre-registered RESPREAD + 81 DEGROSS controls)")
    P("=" * 175)
    P(f"  4a passes: {int(G.p4a.sum())} of {len(G)};  4b passes: {int(G.p4b.sum())} of {len(G)};"
      f"  both: {int((G.p4a & G.p4b).sum())};  4b at 25 bps: {int(G.p4b_25.sum())}")
    P(fmt(G.groupby(["panel", "con", "family"])[["p4a", "p4b", "p4b_25"]].sum(), 0))
    if G.p4b.any():
        P("\n  every 4b passer in the grid:")
        P(fmt(G[G.p4b][["panel", "con", "family", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                        "oSharpe", "dd_margin_pp", "p4a", "f4b_25"]], 4))

    # ---------------- verdict
    P("\n" + "=" * 175)
    P("VERDICT")
    P("=" * 175)
    verdict = "KEEP-candidate (4b)" if (a1_pass and a2_ok) else (
        "PARK" if n_both4b else "KILL")
    P(f"  A3 reproduction : {'PASS' if a3 else 'FAIL'} (max |d| {a3max:.3e})")
    P(f"  A1 queue bar    : {'PASS' if a1_pass else 'FAIL'} ({n_both4b} cells clear 4b on both "
      f"required panels; {len(a1_pass)} also clear the {A1_MARGIN_PP} pp DD margin)")
    P(f"  A2 rule 8       : {'PASS' if a2_ok else 'FAIL'}")
    P(f"  VERDICT: {verdict}")
    P("  With cadence CLOSED at the record's weekly default and only (family, x) free, idea "
      "298's PARKed monthly candidate is not reachable as a two-dial rule unless A1 and A2 "
      "both pass above.")
    flush_log()

    # ---------------- result.md
    u = G[(G.panel == "U56") & (G.con == "RESPREAD") & (G.family == "QUANTILE") & (G.level == 0.50)]
    md = ["# Idea 299 — pre-register-the-quantile-family-as-a-dial (cloud, 2026-09-09)", "",
          f"**A3 reproduction {'PASS' if a3 else 'FAIL'}** (max |d| {a3max:.3e} vs idea 301's "
          f"committed weekly cells).", "",
          f"**A1 {'PASS' if a1_pass else 'FAIL'}** — {n_both4b} of {len(A1)} (family, x) cells "
          f"clear 4b on both U56 and B136; {len(a1_pass)} also clear the DD cap by > "
          f"{A1_MARGIN_PP} pp. Cells: {a1_pass if a1_pass else 'none'}.",
          f"**A2 {'PASS' if a2_ok else 'FAIL'}** — walk-forward (x chosen on IS Sharpe only) "
          f"cells clearing both panels: {a2_ok if a2_ok else 'none'}.", "",
          f"**VERDICT: {verdict}**", "",
          "## Idea 298's PARK candidate at the weekly default (U56, QUANTILE, x=0.50)", "", "```",
          fmt(u[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "dd_margin_pp",
                 "f4b", "f4b_25"]], 4), "```", "",
          "## A1 table (every (family, x) cell on the two required panels)", "", "```",
          fmt(A1, 4), "```", "",
          "## A2 rule-8 walk-forward", "", "```",
          fmt(WF.set_index(["pick", "family", "panel"])[
              ["level", "oCAGR", "oSharpe", "oMaxDD", "spy_oSharpe", "live_oSharpe",
               "beats_SPY_oos", "beats_LIVE_oos", "dd_margin_pp", "p4b"]], 4), "```", "",
          f"4a {int(G.p4a.sum())}/{len(G)} books, 4b {int(G.p4b.sum())}/{len(G)}, 4b at 25 bps "
          f"{int(G.p4b_25.sum())}/{len(G)}.", "",
          "SURVIVORSHIP: U56/B136/SMALL439 are current constituents only (no delistings), so "
          "every CAGR level and both KEEP columns are inflated. SMALL439 drops every ticker with "
          "max_1d_move >= 1.0 in data/small_meta.csv.", ""]
    Path(f"{OUT}.result.md").write_text("\n".join(md))
    flush_log()
    P("\nwrote: .grid.csv .a1.csv .walkforward.csv .result.md .console.txt")
    flush_log()


if __name__ == "__main__":
    main()
