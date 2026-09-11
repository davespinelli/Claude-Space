#!/usr/bin/env python3
"""IDEA 561 - does any other committed DEPTH-MATCHED control share its gate's RANKING VARIABLE?
Cloud lane, 2026-09-11.

THE QUESTION
------------
Idea 559 found that idea 305's quantile CONTROL ranks names on `dist = px / MA200 - 1` - the
MA gate's OWN variable - so once the control is matched to the gate at EXACT DAILY DEPTH
(k_t = |gate_t| every bar) the two arms select the SAME SET on every bar and the published
SELECTION leg is identically zero, not small.  That is an identity, not a measurement: a
top-k_t cut of `dist` when exactly k_t names have `dist > 0` IS the gate.

This run does two things.
  (1) THE PRICE LEG - proves the degeneracy exactly and prices what a NON-degenerate control
      is worth, by running the gate arm and six depth-matched quantile controls side by side
      on three panels, four cadences and two constructions, under both KEEP paths and rule 8.
  (2) THE CENSUS LEG - scans every committed backtest script for depth-matched gate-vs-
      quantile contrasts and classifies each one's ranker as the gate's own variable (DEGEN),
      a different-window member of the same family (NEAR), or independent (CLEAN).

RANKERS (the control's ranking variable; the gate is always px > MA200)
----------------------------------------------------------------------
    GATE     the gate arm itself, no ranking                (the reference)
    MADIST   px / MA200 - 1        <-- the GATE'S OWN VARIABLE, the degenerate case
    MA50D    px / MA50  - 1        <-- same family, different window (NEAR)
    MOM12    px.shift(21)/px.shift(252) - 1                  (CLEAN)
    R6       px / px.shift(126) - 1                          (CLEAN)
    R3       px / px.shift(63)  - 1                          (CLEAN)
    INVVOL   -(20d realised vol)                             (CLEAN)

SELECTION_pp = 100 x (CAGR(control) - CAGR(gate)) at IDENTICAL daily depth, gross and
construction, so exposure is matched bar by bar and only the NAMES differ.

PRE-REGISTERED GATES (bars fixed before any number was read)
-----------------------------------------------------------
  G0  run() reproduces engine.backtest returns AND turnover                    bar 1e-12
  G1  THE DEGENERACY.  With ranker = MADIST at exact daily depth the selected
      SET equals the gate set on EVERY bar, so the weight matrices, the returns
      and the turnover are identical and SELECTION_pp is zero                   bar EXACT 0
  G2  depth is matched: |control_t| == |gate_t| on every bar for every ranker
      (up to the rankable-count clip, which is reported)                        bar EXACT 0
  G3  the derived cost rung equals a fresh run at that rung (0/10/25 bps)       bar 1e-15

GRID.  2 TUNED PARAMS ONLY: RANKER (6 controls) x CADENCE {D,W,M,Q}.
PANEL {U56,B136,SMALL439} and CONSTRUCTION {DEGROSS,RESPREAD} are REPORTED axes, never
selected over; gross is PINNED at the live 0.75.  3 x 7 x 4 x 2 = 168 runs, every one in
.grid.csv.  Costs 10 bps per unit turnover (0 and 25 derived exactly).  Next-day execution.
No shorting, no leverage.  IS = start..2016-12-31, OOS = 2017-01-01..end, read ONCE (rule 8).

BOTH KEEP PATHS on every book, against that book's own panel:
  4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2
  4b  Sharpe > SPY in BOTH halves AND out of sample, |MaxDD| <= 0.60 x |SPY|, CAGR >= 0.70 x SPY

CENSUS PARAMS (2): SAMPLE {STRICT, WIDE} x MATCHRULE {DAILY, ANY}.  Both reported in full.

SURVIVORSHIP.  B136 and SMALL439 are CURRENT constituents only - dead names are absent, CAGR
is inflated and MaxDD understated.  SELECTION is an arm-minus-arm quantity inside ONE panel at
identical depth, where the bias very largely cancels; the KEEP columns and the rule-8 levels
are NOT protected and are read with that caveat.  The 44 SMALL names with max_1d_move >= 1.0
are dropped (data/small_meta.csv).

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .selection.csv .keeppaths.csv .walkforward.csv .census.csv .rungs.csv
         .console.txt
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
RUNGS = [0, 10, 25]
PANELS = ["U56", "B136", "SMALL439"]
RANKERS = ["GATE", "MADIST", "MA50D", "MOM12", "R6", "R3", "INVVOL"]   # tuned param 1
CADENCES = ["D", "W", "M", "Q"]                                        # tuned param 2
CONSTRUCTIONS = ["DEGROSS", "RESPREAD"]                                # reported
GROSS = 0.75                                                           # pinned, the live gross
FAMILY = {"MADIST": "DEGEN", "MA50D": "NEAR", "MOM12": "CLEAN", "R6": "CLEAN",
          "R3": "CLEAN", "INVVOL": "CLEAN"}
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

BAR_ENGINE = 1e-12
BAR_EXACT = 0.0
BAR_RUNG = 1e-15

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 900)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def run(px, W, freq):
    """engine.backtest's arithmetic, returning the ZERO-COST path and turnover."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    r0 = pd.Series(np.nansum(held * rets, axis=1), index=px.index)
    return r0, pd.Series(turn, index=px.index)


def rung(r0, turn, c):
    return r0 - turn * c / 1e4


def ma_gate(px):
    """The gate every arm is matched to: px above its 200d mean, on live bars."""
    return (px > px.rolling(200).mean()) & live_mask(px)


def ranker(px, kind):
    lm = live_mask(px)
    if kind == "MADIST":
        s = px / px.rolling(200).mean() - 1
    elif kind == "MA50D":
        s = px / px.rolling(50).mean() - 1
    elif kind == "MOM12":
        s = px.shift(21) / px.shift(252) - 1
    elif kind == "R6":
        s = px / px.shift(126) - 1
    elif kind == "R3":
        s = px / px.shift(63) - 1
    elif kind == "INVVOL":
        s = -(px.pct_change().rolling(20).std() * np.sqrt(252))
    else:
        raise ValueError(kind)
    return s.where(lm)


def daily_matched(sig, gate, lm):
    """idea 559's exact daily match: take the top k_t names by `sig`, k_t = |gate_t| every
    bar, clipped to the count of rankable names that day."""
    k_gate = gate.sum(axis=1)
    kt = np.minimum(k_gate, sig.notna().sum(axis=1))
    sel = sig.rank(axis=1, ascending=False, method="first").le(kt, axis=0).fillna(False) & lm
    return sel, k_gate, kt


def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ census
MATCH_PAT = {
    "DAILY": re.compile(r"daily_matched|k_ma|exact daily depth|k_t\s*=\s*k_|"
                        r"matched.{0,12}depth|depth.{0,12}match", re.I),
    "ANY": re.compile(r"daily_matched|k_ma|matched|depth|quantile|top-?k|\.le\(k", re.I),
}
GATEVAR_PAT = re.compile(r"rolling\(\s*200\s*\)\s*\.mean\(\)|ma200|MA-DIST|MADIST|"
                         r"px\s*/\s*ma\s*-\s*1|dist\s*=\s*px\s*/", re.I)
QUANT_PAT = re.compile(r"rank\(axis=1|quantile|\.le\(k|top-?k", re.I)
NEAR_PAT = re.compile(r"rolling\(\s*(?!200)\d+\s*\)\s*\.mean\(\)", re.I)
CLEAN_PAT = re.compile(r"shift\(\s*252\s*\)|shift\(\s*126\s*\)|shift\(\s*63\s*\)|"
                       r"rolling\(\s*20\s*\)\s*\.std\(\)|vol20", re.I)


def census(files, sample, matchrule):
    """Classify each committed script that runs a depth-matched gate-vs-quantile contrast by
    whether the CONTROL's ranking variable is the GATE's own variable.

    DEGEN : the file's ranker expression is the gate variable itself (px/MA200 - 1).
    NEAR  : ranker is a different-window member of the same moving-average family.
    CLEAN : ranker is an independent variable (momentum / vol).
    Heuristic, source-regex based - the patterns are printed so the classification is
    reproducible and falsifiable; it is a LOWER bound on DEGEN, not a proof for any one file.
    """
    out = []
    mp = MATCH_PAT[matchrule]
    for f in files:
        try:
            t = f.read_text(errors="ignore")
        except Exception:
            continue
        if not mp.search(t):
            continue
        if not QUANT_PAT.search(t):
            continue
        if sample == "STRICT" and "daily_matched" not in t and not re.search(r"k_ma", t):
            continue
        gv, nr, cl = bool(GATEVAR_PAT.search(t)), bool(NEAR_PAT.search(t)), bool(CLEAN_PAT.search(t))
        kind = "DEGEN" if gv and not cl else ("NEAR" if nr and not cl else
                                              ("CLEAN" if cl else "UNCLASSIFIED"))
        out.append(dict(file=f.name, sample=sample, matchrule=matchrule, kind=kind,
                        gatevar=gv, nearfam=nr, cleanvar=cl, bytes=len(t)))
    return out


# ================================================================== main
def main():
    P("=" * 170)
    P("IDEA 561 - does any other committed DEPTH-MATCHED control share its gate's RANKING "
      "VARIABLE?   (cloud lane, 2026-09-11)")
    P("=" * 170)
    P("PROTOCOL: 10 bps per unit turnover (0/25 derived exactly and reported), next-day")
    P(f"execution, no shorting, no leverage.  IS = start..{IS_END}, OOS = {OOS_START}..end.")
    P(f"2 tuned params: RANKER {RANKERS[1:]} x CADENCE {CADENCES}.")
    P(f"PANEL {PANELS} and CONSTRUCTION {CONSTRUCTIONS} are REPORTED axes, never selected")
    P(f"over; gross PINNED at the live {GROSS}.  Both KEEP paths on every book; every grid")
    P("point in .grid.csv.  Census params: SAMPLE {STRICT,WIDE} x MATCHRULE {DAILY,ANY}.")
    P("SURVIVORSHIP: B136/SMALL439 are current constituents only; CAGR inflated, MaxDD")
    P("understated.  SELECTION is depth-matched inside one panel and largely immune; the")
    P("KEEP columns and rule-8 levels are not.")
    flush_log()

    u, b = load_universe(), load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    PN = {"U56": (u.drop(columns=["SPY"]), u["SPY"]),
          "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
          "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])}
    P("\nPanels: " + "  ".join(f"{k} {v[0].shape[1]}x{len(v[0])}" for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    # ------------------------------------------------------------------ gates
    P("\n" + "=" * 170)
    P("PRE-REGISTERED GATES")
    P("=" * 170)
    g0 = g3 = 0.0
    for pn in PANELS:
        px = PN[pn][0]
        W = rules_v2_weights(px)
        for freq in ("D", "W", "Q"):
            a = backtest(px, W, cost_bps=COST_BPS, freq=freq)
            r0, tn = run(px, W, freq)
            g0 = max(g0, float((a["returns"] - rung(r0, tn, COST_BPS)).abs().max()),
                     float((a["turnover"] - tn).abs().max()))
            for c in RUNGS:
                g3 = max(g3, float((backtest(px, W, cost_bps=c, freq=freq)["returns"]
                                    - rung(r0, tn, c)).abs().max()))
    P(f"  G0  run() vs engine.backtest (returns AND turnover)      max |d| = {g0:.3e}"
      f"   bar {BAR_ENGINE:.0e}   {'PASS' if g0 <= BAR_ENGINE else 'FAIL'}")
    P(f"  G3  derived cost rung vs a fresh run (rungs {RUNGS})     max |d| = {g3:.3e}"
      f"   bar {BAR_RUNG:.0e}   {'PASS' if g3 <= BAR_RUNG else 'FAIL'}")

    g1_set = g1_ret = g1_trn = 0.0
    g2_depth = 0.0
    clipped = []
    for pn in PANELS:
        px = PN[pn][0]
        lm, gm = live_mask(px), ma_gate(px)
        for rk in RANKERS[1:]:
            sel, k_gate, kt = daily_matched(ranker(px, rk), gm, lm)
            g2_depth = max(g2_depth, float((sel.sum(axis=1) - kt).abs().max()))
            clipped.append(dict(panel=pn, ranker=rk, bars=len(kt),
                                clipped=int((kt < k_gate).sum()),
                                clip_share=float((kt < k_gate).mean())))
            if rk == "MADIST":
                g1_set = max(g1_set, float((sel.astype(int) - gm.astype(int)).abs().values.max()))
                for con in CONSTRUCTIONS:
                    Wg, Ws = book(px, gm, con), book(px, sel, con)
                    for cad in ("D", "W", "Q"):
                        rg, tg = run(px, Wg, cad)
                        rs, ts = run(px, Ws, cad)
                        g1_ret = max(g1_ret, float((rg - rs).abs().max()))
                        g1_trn = max(g1_trn, float((tg - ts).abs().max()))
    P(f"  G1  DEGENERACY: MADIST-ranked control == the GATE, cell by cell")
    P(f"        max |d selected-set| = {g1_set:.3e}   max |d returns| = {g1_ret:.3e}"
      f"   max |d turnover| = {g1_trn:.3e}   bar EXACT 0   "
      f"{'PASS' if max(g1_set, g1_ret, g1_trn) <= BAR_EXACT else 'FAIL'}")
    P(f"  G2  depth matched: |control_t| == k_t on every bar, every ranker, every panel"
      f"   max |d| = {g2_depth:.3e}   bar EXACT 0   "
      f"{'PASS' if g2_depth <= BAR_EXACT else 'FAIL'}")
    CL = pd.DataFrame(clipped)
    P("\n  the rankable-count clip (bars where a ranker has fewer live values than k_gate):")
    P(CL.pivot_table(index="panel", columns="ranker", values="clip_share")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ grid
    P("\n" + "=" * 170)
    P("THE GRID - every point reported")
    P("=" * 170)
    rows, bench = [], {}
    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        bench[pn] = dict(SPY=stat(spy_px.pct_change().fillna(0).loc[start:]),
                         RULESv2=stat(backtest(px, rules_v2_weights(px), cost_bps=COST_BPS,
                                               freq="W")["returns"].loc[start:]))
        lm, gm = live_mask(px), ma_gate(px)
        sets = {"GATE": gm}
        for rk in RANKERS[1:]:
            sets[rk], _, _ = daily_matched(ranker(px, rk), gm, lm)
        for rk in RANKERS:
            for con in CONSTRUCTIONS:
                W = book(px, sets[rk], con)
                for cad in CADENCES:
                    r0, tn = run(px, W, cad)
                    r0, tn = r0.loc[start:], tn.loc[start:]
                    st = stat(rung(r0, tn, COST_BPS))
                    row = dict(panel=pn, ranker=rk, family=FAMILY.get(rk, "-"), con=con,
                               cad=cad, turn=float(tn.sum()), **st)
                    for c in RUNGS:
                        m = metrics(rung(r0, tn, c))
                        row[f"Sharpe{c}"], row[f"CAGR{c}"] = m["Sharpe"], m["CAGR"]
                    rows.append(row)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"  {len(G)} runs = {len(PANELS)} panels x {len(RANKERS)} arms x "
      f"{len(CONSTRUCTIONS)} constructions x {len(CADENCES)} cadences, gross pinned "
      f"{GROSS}.  Written to .grid.csv")
    P("\n  full-sample Sharpe by arm and cadence (mean over panels x constructions):")
    P(G.pivot_table(index="ranker", columns="cad", values="Sharpe")
      .reindex(RANKERS).to_string(float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ selection
    P("\n" + "=" * 170)
    P("A.  THE SELECTION LEG - control minus gate at IDENTICAL daily depth")
    P("=" * 170)
    base = G.loc[G.ranker == "GATE"].set_index(["panel", "con", "cad"])
    S = G.loc[G.ranker != "GATE"].copy()
    S["gate_CAGR"] = S.set_index(["panel", "con", "cad"]).index.map(base["CAGR"])
    S["gate_Sharpe"] = S.set_index(["panel", "con", "cad"]).index.map(base["Sharpe"])
    S["gate_oCAGR"] = S.set_index(["panel", "con", "cad"]).index.map(base["oCAGR"])
    S["SEL_pp"] = (S["CAGR"] - S["gate_CAGR"]) * 100
    S["dSharpe"] = S["Sharpe"] - S["gate_Sharpe"]
    S["oSEL_pp"] = (S["oCAGR"] - S["gate_oCAGR"]) * 100
    S.to_csv(f"{OUT}.selection.csv", index=False)
    P("  SELECTION_pp = 100 x (CAGR_control - CAGR_gate), same depth / gross / construction:")
    P(S.groupby(["family", "ranker"]).agg(
        n=("SEL_pp", "size"), med_SEL_pp=("SEL_pp", "median"), min_SEL_pp=("SEL_pp", "min"),
        max_SEL_pp=("SEL_pp", "max"), max_abs=("SEL_pp", lambda x: x.abs().max()),
        med_dSharpe=("dSharpe", "median"), med_oSEL_pp=("oSEL_pp", "median")
    ).to_string(float_format=lambda x: f"{x:.4f}"))
    deg = S.loc[S.ranker == "MADIST"]
    P(f"\n  THE DEGENERACY, priced: over all {len(deg)} MADIST cells "
      f"max |SELECTION_pp| = {deg.SEL_pp.abs().max():.3e}, max |dSharpe| = "
      f"{deg.dSharpe.abs().max():.3e}, max |OOS SELECTION_pp| = {deg.oSEL_pp.abs().max():.3e}"
      f"  -> {'IDENTICALLY ZERO' if deg.SEL_pp.abs().max() == 0 else 'NOT ZERO'}.")
    nd = S.loc[S.ranker != "MADIST"]
    P(f"  A NON-degenerate control on the same grid moves CAGR by a median "
      f"{nd.SEL_pp.abs().median():.4f} pp (max {nd.SEL_pp.abs().max():.4f}) and Sharpe by a "
      f"median {nd.dSharpe.abs().median():.4f} (max {nd.dSharpe.abs().max():.4f}).")
    P(f"  So the ratio of a degenerate SELECTION leg to a real one is EXACTLY 0 : "
      f"{nd.SEL_pp.abs().median():.4f} pp.  Any published SELECTION leg whose control ranks on")
    P("  the gate's own variable at exact depth is an ARITHMETIC IDENTITY, not a measurement.")
    P("\n  by panel x ranker (median SELECTION_pp):")
    P(S.pivot_table(index="ranker", columns="panel", values="SEL_pp")
      .reindex(RANKERS[1:]).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  by cadence x ranker (median SELECTION_pp):")
    P(S.pivot_table(index="ranker", columns="cad", values="SEL_pp")
      .reindex(RANKERS[1:]).to_string(float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ census
    P("\n" + "=" * 170)
    P("B.  THE CENSUS - committed scripts running a depth-matched gate-vs-quantile contrast")
    P("=" * 170)
    files = sorted((REPO / "research" / "backtests").glob("*.py"))
    files = [f for f in files if f.name != Path(__file__).name]
    P(f"  {len(files)} committed backtest scripts scanned (this file excluded).")
    P("  patterns (printed so the classification is reproducible and falsifiable):")
    P(f"    MATCH  DAILY = {MATCH_PAT['DAILY'].pattern}")
    P(f"    MATCH  ANY   = {MATCH_PAT['ANY'].pattern}")
    P(f"    QUANT        = {QUANT_PAT.pattern}")
    P(f"    GATEVAR      = {GATEVAR_PAT.pattern}")
    P(f"    NEARFAM      = {NEAR_PAT.pattern}")
    P(f"    CLEANVAR     = {CLEAN_PAT.pattern}")
    C = []
    for sample in ("STRICT", "WIDE"):
        for mr in ("DAILY", "ANY"):
            C += census(files, sample, mr)
    C = pd.DataFrame(C)
    C.to_csv(f"{OUT}.census.csv", index=False)
    P(f"\n  counts by (sample, matchrule) x classification:")
    P(C.pivot_table(index=["sample", "matchrule"], columns="kind", values="file",
                    aggfunc="count", fill_value=0).to_string())
    for sample in ("STRICT", "WIDE"):
        for mr in ("DAILY", "ANY"):
            sub = C.loc[(C["sample"] == sample) & (C.matchrule == mr)]
            if not len(sub):
                continue
            d = int((sub.kind == "DEGEN").sum())
            P(f"    {sample:7s}/{mr:5s}: {len(sub):4d} contrast files, DEGEN {d} "
              f"({d/len(sub):.1%}), NEAR {int((sub.kind=='NEAR').sum())}, "
              f"CLEAN {int((sub.kind=='CLEAN').sum())}, "
              f"UNCLASSIFIED {int((sub.kind=='UNCLASSIFIED').sum())}")
    hdr = C.loc[(C["sample"] == "STRICT") & (C.matchrule == "DAILY")]
    if len(hdr):
        P(f"\n  THE HEADLINE CENSUS (STRICT/DAILY - files that literally run an exact daily")
        P(f"  depth match): {len(hdr)} files, of which {int((hdr.kind=='DEGEN').sum())} rank "
          f"their control on the GATE'S OWN VARIABLE and carry a degenerate SELECTION leg.")
        P(hdr[["file", "kind", "gatevar", "nearfam", "cleanvar"]].head(40)
          .to_string(index=False))
    P("\n  CAVEAT: this is a source-regex classifier, so DEGEN is a LOWER bound (a file whose")
    P("  ranker is the gate variable but ALSO mentions a momentum term is scored CLEAN) and")
    P("  UNCLASSIFIED files are not evidence either way.  The PRICE leg above, not the")
    P("  classifier, is what establishes that the degenerate case is an exact identity.")
    flush_log()

    # ------------------------------------------------------------------ keep paths
    P("\n" + "=" * 170)
    P("C.  BOTH KEEP PATHS ON EVERY BOOK")
    P("=" * 170)
    K = []
    for _, r in G.iterrows():
        s = r.to_dict()
        bm, sp = bench[r.panel]["RULESv2"], bench[r.panel]["SPY"]
        K.append(dict(panel=r.panel, ranker=r.ranker, family=r.family, con=r.con, cad=r.cad,
                      CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                      oCAGR=r.oCAGR, oSharpe=r.oSharpe, oMaxDD=r.oMaxDD,
                      keep4a=verdict_4a(s, bm), fail4b=fail_4b(s, sp)))
    K = pd.DataFrame(K)
    K["keep4b"] = K.fail4b == "-"
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    for p in PANELS:
        bm, sp = bench[p]["RULESv2"], bench[p]["SPY"]
        P(f"    {p:9s} RULES v2  CAGR {bm['CAGR']:7.2%}  Sharpe {bm['Sharpe']:.4f} "
          f"({bm['H1']:.4f}/{bm['H2']:.4f})  MaxDD {bm['MaxDD']:7.2%} | OOS "
          f"{bm['oCAGR']:7.2%}/{bm['oSharpe']:.4f}/{bm['oMaxDD']:7.2%}")
        P(f"    {'':9s} SPY       CAGR {sp['CAGR']:7.2%}  Sharpe {sp['Sharpe']:.4f} "
          f"({sp['H1']:.4f}/{sp['H2']:.4f})  MaxDD {sp['MaxDD']:7.2%} | OOS "
          f"{sp['oCAGR']:7.2%}/{sp['oSharpe']:.4f}/{sp['oMaxDD']:7.2%}")
    P(f"\n  4a PASS {int(K.keep4a.sum())}/{len(K)}    4b PASS {int(K.keep4b.sum())}/{len(K)}")
    P("\n  by arm:")
    P(K.groupby(["family", "ranker"]).agg(n=("keep4a", "size"), pass4a=("keep4a", "sum"),
                                          pass4b=("keep4b", "sum"))
      .reindex([(FAMILY.get(r, "-"), r) for r in RANKERS]).to_string())
    P("\n  4b fail tokens (SET semantics, every failing bar listed):")
    P(K.fail4b.value_counts().to_string())
    if K.keep4b.any():
        P("\n  every 4b passer:")
        P(K.loc[K.keep4b, ["panel", "ranker", "family", "con", "cad", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2", "oCAGR", "oSharpe", "oMaxDD"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if K.keep4a.any():
        P(f"\n  every 4a passer ({int(K.keep4a.sum())}):")
        P(K.loc[K.keep4a, ["panel", "ranker", "family", "con", "cad", "CAGR", "Sharpe",
                           "MaxDD", "H1", "H2"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    flush_log()

    # ------------------------------------------------------------------ rule 8
    P("\n" + "=" * 170)
    P("D.  RULE 8 WALK-FORWARD - (ranker, cadence) chosen on IS Sharpe ALONE, OOS read ONCE")
    P("=" * 170)
    WF = []
    for (pn, con), grp in G.groupby(["panel", "con"]):
        for pool, label in ((grp, "ALL-ARMS"), (grp.loc[grp.ranker != "MADIST"], "NON-DEGEN")):
            pick = pool.loc[pool.isSharpe.idxmax()]
            bm, sp = bench[pn]["RULESv2"], bench[pn]["SPY"]
            so = dict(H1=pick.oSharpe, H2=pick.oSharpe, Sharpe=pick.oSharpe, CAGR=pick.oCAGR,
                      MaxDD=pick.oMaxDD, oSharpe=pick.oSharpe)
            bo = dict(H1=bm["oSharpe"], H2=bm["oSharpe"], MaxDD=bm["oMaxDD"])
            spo = dict(H1=sp["oSharpe"], H2=sp["oSharpe"], MaxDD=sp["oMaxDD"],
                       CAGR=sp["oCAGR"], oSharpe=sp["oSharpe"])
            WF.append(dict(panel=pn, con=con, pool=label, pick_ranker=pick.ranker,
                           pick_cad=pick.cad, isSharpe=pick.isSharpe, oCAGR=pick.oCAGR,
                           oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                           base_oCAGR=bm["oCAGR"], base_oSharpe=bm["oSharpe"],
                           base_oMaxDD=bm["oMaxDD"], spy_oCAGR=sp["oCAGR"],
                           spy_oSharpe=sp["oSharpe"], spy_oMaxDD=sp["oMaxDD"],
                           oos4a=verdict_4a(so, bo), oos4b_fail=fail_4b(so, spo)))
    WF = pd.DataFrame(WF)
    WF["oos4b"] = WF.oos4b_fail == "-"
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"  {len(WF)} selector cells (panel x construction x pool), each choosing one of "
      f"{len(RANKERS)*len(CADENCES)} (arm,cadence) points on IS Sharpe alone.")
    P(WF[["panel", "con", "pool", "pick_ranker", "pick_cad", "isSharpe", "oCAGR", "oSharpe",
          "oMaxDD", "base_oSharpe", "spy_oSharpe", "oos4a", "oos4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  OOS 4a PASS {int(WF.oos4a.sum())}/{len(WF)}   OOS 4b PASS "
      f"{int(WF.oos4b.sum())}/{len(WF)}")
    P("  OOS 4b fail tokens: " + WF.oos4b_fail.value_counts().to_string().replace("\n", " | "))
    P(f"  the IS selector chooses the DEGENERATE arm (MADIST, i.e. the gate itself) in "
      f"{int((WF.loc[WF.pool=='ALL-ARMS'].pick_ranker.isin(['MADIST','GATE'])).sum())} of "
      f"{int((WF.pool=='ALL-ARMS').sum())} ALL-ARMS cells.")
    P("\n  OOS levels vs benchmarks, best NON-DEGEN cell per panel (by OOS Sharpe):")
    for p in PANELS:
        w = WF.loc[(WF.panel == p) & (WF.pool == "NON-DEGEN")].sort_values(
            "oSharpe", ascending=False).iloc[0]
        P(f"    {p:9s} best {w.pick_ranker}/{w.con} @ {w.pick_cad}  OOS CAGR {w.oCAGR:7.2%} "
          f"Sharpe {w.oSharpe:.4f} MaxDD {w.oMaxDD:7.2%}   vs RULES v2 "
          f"{w.base_oCAGR:7.2%}/{w.base_oSharpe:.4f}/{w.base_oMaxDD:7.2%}   vs SPY "
          f"{w.spy_oCAGR:7.2%}/{w.spy_oSharpe:.4f}/{w.spy_oMaxDD:7.2%}")
    flush_log()

    # ------------------------------------------------------------------ rungs
    P("\n" + "=" * 170)
    P("E.  COST RUNGS - the SELECTION leg at 0 / 10 / 25 bps")
    P("=" * 170)
    R = []
    for c in RUNGS:
        bb = G.loc[G.ranker == "GATE"].set_index(["panel", "con", "cad"])[f"CAGR{c}"]
        ss = G.loc[G.ranker != "GATE"].copy()
        ss["sel"] = (ss[f"CAGR{c}"] - ss.set_index(["panel", "con", "cad"]).index.map(bb)) * 100
        for fam in ("DEGEN", "NEAR", "CLEAN"):
            f = ss.loc[ss.family == fam]
            R.append(dict(bps=c, family=fam, n=len(f), med_SEL_pp=float(f.sel.median()),
                          max_abs_SEL_pp=float(f.sel.abs().max())))
    R = pd.DataFrame(R)
    R.to_csv(f"{OUT}.rungs.csv", index=False)
    P(R.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  (DEGEN is exactly 0.0000 at every rung by construction - the identity survives cost,")
    P("   because the two arms hold the same names at the same weights and trade identically.)")

    # ------------------------------------------------------------------ verdict
    P("\n" + "=" * 170)
    P("VERDICT")
    P("=" * 170)
    P(f"  The degenerate control's SELECTION leg is EXACTLY 0 at every one of the {len(deg)} "
      f"cells and every cost rung; a real control on the same grid is worth a median "
      f"{nd.SEL_pp.abs().median():.4f} pp.")
    P(f"  KEEP: 4b {int(K.keep4b.sum())}/{len(K)}, 4a {int(K.keep4a.sum())}/{len(K)}; under "
      f"rule 8 OOS 4b {int(WF.oos4b.sum())}/{len(WF)}, OOS 4a {int(WF.oos4a.sum())}/{len(WF)}.")
    flush_log()
    P("\nwrote: " + ", ".join(f"{OUT.name}{e}" for e in
                              (".grid.csv", ".selection.csv", ".census.csv", ".keeppaths.csv",
                               ".walkforward.csv", ".rungs.csv", ".console.txt")))
    flush_log()


if __name__ == "__main__":
    main()
