#!/usr/bin/env python3
"""QUEUE idea 243 — locate-the-n-ceiling-above-60 (cloud, 2026-09-08).

QUESTION (queue, verbatim intent)
  Idea 240 moved the grid edge from 20 to 60 and 3 of 7 panels went straight to the new top;
  the width curve is still unbounded for panels with >= 60 eligible names.  Run n in
  {60, 90, 120, 180} on B136 / BSTK100 / SMALL484 under the CONSTANT-GROSS (NORM) convention
  only, and report whether an interior OOS optimum exists at all or the book converges to
  EWall.

WHAT THIS RUN ADDS TO THE CONCURRENT LANE-C RUN (idea 461, committed 2026-09-08 as
`2026-09-08_does-the-width-convergence-hold-past-n40_C`)
  Lane C ran n in {5,10,20,40,60,90,120,180} x {FIXED, NORM} on U56 / B136 / SMALL439 and
  found the width ladder is monotone only on 5 <= n <= 40 and REVERSES past n ~ 20-40.  It
  did NOT run BSTK100 — the panel idea 243 names, and the one panel in the record's list that
  is single stocks only (no ETF share, idea 312's confound).  Nor did it answer 243's exact
  question, which is not "where does the excess reach zero" but "does an INTERIOR OOS OPTIMUM
  exist at all, or does the book converge to EWall".  This run:
    * adds BSTK100 (universe_broad.json minus every ETF in universe.json's broad/sectors/
      bonds_fx_commod groups) and refines the ladder to 13 widths so an interior argmax can
      actually be LOCATED rather than inferred from a 4-point grid;
    * adds the ladder's TRUE limit as an explicit arm.  Under NORM, RANKED(n) with
      n >= n_elig(t) IS the equal-weight book over the ELIGIBLE set.  So the ladder does NOT
      converge to EWall — it converges to EW_ELIG, a DIFFERENT book (EWall holds the gated-out
      names too).  EW_ELIG is computed exactly and gate G3 asserts the identity;
    * answers the interior question separately on the full sample and OOS, and under rule 8.

  Lane C's committed grid is RE-EXECUTED here as gate G2.  That is a determinism / data-
  stability check, NOT an independent replication: this script IMPORTS lane C's module and
  uses its `simulate`, `ranked_weights` and `ew_weights` verbatim, so agreement is expected
  by construction and only a data revision could break it.  Stated so no one reads G2 as
  corroboration.

TUNED PARAMETERS: ONE — n, the ranked book's width (13 levels, all reported).  The queue
  pins the convention (NORM), so it is not a dial here; FIXED is run only inside G2.  Panel
  and cost rung are reporting axes, printed at every value, never selected on.

FIXED AND PRE-REGISTERED (all inherited from lane C / idea 239 so the ladders are comparable)
  gross 0.75; weekly cadence; gate = plain 200d MA; vol cap vol20 < 0.60; composite = 12-1 +
  6m + 3m rank average, no vol scaling; de-gross convention (gated-out weight to cash);
  cost rungs {0, 10, 25} bps derived exactly from one 0-bps run per arm
  (net(c) = gross - turn*c/1e4); 10 bps is the verdict rung (PROTOCOL 2); next-day execution.
  Rule 8: n chosen on <= 2016-12-31 by IS Sharpe, 2017-2026 read ONCE.

SURVIVORSHIP: B136 and BSTK100 are the CURRENT constituents of research/universe_broad.json
  and SMALL439 is the sub-$2B screen's survivors since 2010 with the 44 tickers whose
  data/small_meta.csv max_1d_move >= 1.0 dropped (PROTOCOL 9, data/SMALL_PANEL_README.md).
  Levels are upward-biased and not achievable; every reading here is a WITHIN-PANEL contrast
  between books on the same days, which cancels most but not all of that bias.

Artefacts: .console.txt .ladder.csv .walkforward.csv .keep.csv .result.md
Nothing outside research/ is touched; RULES.md, scan.py, bot.py, baseline.py untouched.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

OUT = ROOT / "research" / "backtests"
STEM = "2026-09-08_locate-the-n-ceiling-above-60_cloud"
LANEC = "2026-09-08_does-the-width-convergence-hold-past-n40_C"

_LINES: list[str] = []


def say(*a) -> None:
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


def flush() -> None:
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LINES) + "\n")


def _load(stem, mod):
    spec = importlib.util.spec_from_file_location(mod, OUT / f"{stem}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = _load(LANEC, "laneC")
simulate = C.simulate
week_mask = C.week_mask
ranked_weights = C.ranked_weights
ew_weights = C.ew_weights
overlap = C.overlap
net = C.net
stats = C.stats
bars_4a = C.bars_4a
bars_4b = C.bars_4b
GROSS = C.GROSS
MAX_VOL = C.MAX_VOL
IS_END = C.IS_END
OOS_START = C.OOS_START

NS = [5, 10, 20, 30, 40, 50, 60, 75, 90, 120, 150, 180, 240]     # the one tuned dial
RUNGS = [0, 10, 25]
VERDICT_RUNG = 10


def signals(px, invest):
    """composite / above / vol20 over the INVESTABLE columns only, re-indexed onto px's
    columns with the non-investable ones blanked.  The composite is lane C's exact
    construction (`score(.., vol_scale=False)` divided by its trend factor), computed on the
    investable frame so the cross-sectional ranks are the book's own."""
    sub = px[invest]
    s_ns, above, vol20 = score(sub, vol_scale=False)
    comp = s_ns / (0.5 + 0.5 * above.astype(float))
    r = lambda d, fill: d.reindex(columns=px.columns).fillna(fill)
    return r(comp, np.nan), r(above, False).astype(bool), r(vol20, np.nan)


def ew_elig_weights(comp, above, vol20):
    """EW_ELIG: equal weight over every ELIGIBLE name at GROSS/n_elig — the NORM ladder's
    limit as n -> infinity, and a DIFFERENT book from EW_ALL (which holds the gated-out
    names too)."""
    e = (above & (vol20 < MAX_VOL) & comp.notna()).astype(float)
    k = e.sum(axis=1).replace(0, np.nan)
    return GROSS * e.div(k, axis=0).fillna(0.0)


# ------------------------------------------------------------------ panels
def build_panels():
    """(name, prices, investable columns).

    SPY is a genuine constituent of universe.json's `broad` group, so it is INVESTABLE on U56
    and B136 — lane C's convention, kept so its committed grid can be re-executed.  It is NOT
    investable on BSTK100 (single stocks only, by the panel's own definition) or on SMALL439
    (baseline.load_universe(small=True) joins SPY as a BENCHMARK, never a constituent — see its
    docstring).  Part (0) prices what that difference is worth on the small panel."""
    u56 = load_universe()
    b136 = load_universe(broad=True)
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    etf = set(U["broad"]) | set(U["sectors"]) | set(U["bonds_fx_commod"])
    stk = [c for c in b136.columns if c != "SPY" and c not in etf]
    bstk = b136[[c for c in b136.columns if c in stk or c == "SPY"]]
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv", index_col=0)
    sm = load_universe(small=True)
    keep = [c for c in sm.columns if c == "SPY" or meta.max_1d_move.get(c, 0) < 1.0]
    small = sm[keep]
    return [("B136", b136, list(b136.columns)),
            ("BSTK100", bstk, stk),
            ("SMALL439", small, [c for c in small.columns if c != "SPY"]),
            ("SMALL439+SPY", small, list(small.columns)),   # lane C's convention, for G2/part 0
            ("U56", u56, list(u56.columns))]


# ------------------------------------------------------------------ one arm
def arm_row(px, pname, name, W, Wctrl, Wel, rb, spy_s, spy_oos, v2_s, refs):
    g, t, inv = simulate(px, W, rb)
    st = px.index[260]
    out = []
    for bps in RUNGS:
        r = net(g, t, bps).loc[st:]
        s = stats(r)
        oos = metrics(r.loc[OOS_START:])
        iss = metrics(r.loc[:IS_END])["Sharpe"]
        row = dict(panel=pname, arm=name, bps=bps,
                   real_gross=float(inv.loc[st:].mean()),
                   turn_yr=float(t.loc[st:].sum() / (len(t.loc[st:]) / 252)),
                   CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"], H1=s["H1"], H2=s["H2"],
                   IS_Sharpe=iss, OOS_Sharpe=oos["Sharpe"], OOS_CAGR=oos["CAGR"],
                   OOS_MaxDD=oos["MaxDD"],
                   ov_all=overlap(W, Wctrl, rb), ov_elig=overlap(W, Wel, rb),
                   fail4a=bars_4a(s, refs[bps]["v2"]),
                   fail4b=bars_4b(s, refs[bps]["spy"], oos["Sharpe"], refs[bps]["spy_oos"]))
        out.append(row)
    return out


def run():
    pd.set_option("display.width", 250)
    say(f"# research/backtests/{STEM}.py")
    say("# QUEUE idea 243 — does an INTERIOR OOS optimum exist above n=60 under the "
        "constant-gross (NORM) convention, or does the ranked book converge?")
    say("# ONE tuned dial: n (13 levels, ALL reported). Panels and cost rungs are reporting "
        "axes. Verdict rung 10 bps.")

    PANELS = build_panels()
    rows, wf, meta_rows = [], [], []

    for pname, px, invest in PANELS:
        names = [c for c in px.columns if c != "SPY"]
        rb = week_mask(px.index)
        st = px.index[260]
        comp, above, vol20 = signals(px, invest)
        elig_ct = (above & (vol20 < MAX_VOL) & comp.notna()).sum(axis=1)

        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        spy_s = stats(spy)
        spy_oos = metrics(spy.loc[OOS_START:])["Sharpe"]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=VERDICT_RUNG, freq="W")["returns"].loc[st:]
        refs = {}
        for bps in RUNGS:
            v2b = backtest(px, rules_v2_weights(px), cost_bps=bps, freq="W")["returns"].loc[st:]
            refs[bps] = dict(v2=stats(v2b), spy=spy_s, spy_oos=spy_oos,
                             v2_oos=metrics(v2b.loc[OOS_START:])["Sharpe"])

        Wctrl = ew_weights(px[invest]).reindex(columns=px.columns).fillna(0.0)
        Wel = ew_elig_weights(comp, above, vol20).fillna(0.0)

        say(f"\n=== PANEL {pname}: {len(invest)} investable of {len(names)} names + SPY, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, eligible names/day mean {elig_ct.loc[st:].mean():.1f} "
            f"(p05 {elig_ct.loc[st:].quantile(0.05):.0f}, median {elig_ct.loc[st:].median():.0f}, "
            f"max {elig_ct.loc[st:].max():.0f}) ===")
        meta_rows.append(dict(panel=pname, n_names=len(invest),
                              elig_mean=float(elig_ct.loc[st:].mean()),
                              elig_p95=float(elig_ct.loc[st:].quantile(0.95)),
                              elig_max=float(elig_ct.loc[st:].max()),
                              spy_Sharpe=spy_s["Sharpe"], spy_CAGR=spy_s["CAGR"],
                              spy_MaxDD=spy_s["MaxDD"], spy_OOS_Sharpe=spy_oos,
                              v2_Sharpe=refs[10]["v2"]["Sharpe"], v2_OOS_Sharpe=refs[10]["v2_oos"]))

        rows += arm_row(px, pname, "EW_ALL", Wctrl, Wctrl, Wel, rb, spy_s, spy_oos, v2, refs)
        rows += arm_row(px, pname, "EW_ELIG", Wel, Wctrl, Wel, rb, spy_s, spy_oos, v2, refs)
        for n in NS:
            W = ranked_weights(comp, above, vol20, n, "NORM").fillna(0.0)
            rows += arm_row(px, pname, f"NORM{n}", W, Wctrl, Wel, rb, spy_s, spy_oos, v2, refs)

    L = pd.DataFrame(rows)
    L["n"] = L.arm.str.extract(r"NORM(\d+)").astype(float)
    M = pd.DataFrame(meta_rows).set_index("panel")
    L.to_csv(OUT / f"{STEM}.ladder.csv", index=False)

    # ---------------------------------------------------------------- gates
    say("\n=== HARNESS GATES ===")
    # G1 EW_ALL vs engine.backtest
    px = {a: b for a, b, _ in PANELS}["B136"]
    Wg = ew_weights(px).reindex(columns=px.columns).fillna(0.0)
    g, t, _ = simulate(px, Wg, week_mask(px.index))
    ref = backtest(px, Wg, cost_bps=0.0, freq="W")["returns"]
    say(f"G1 simulate(EW_ALL) vs engine.backtest on B136: max|dret| "
        f"{float(np.abs(g - ref).max()):.3e}")
    assert float(np.abs(g - ref).max()) < 1e-12

    # G3 the identity that makes EW_ELIG the ladder's limit
    worst = 0.0
    for pname, px, invest in PANELS:
        comp, above, vol20 = signals(px, invest)
        big = ranked_weights(comp, above, vol20, 10_000, "NORM").fillna(0.0)
        el = ew_elig_weights(comp, above, vol20).fillna(0.0)
        worst = max(worst, float(np.abs(big.values - el.values).max()))
    say(f"G3 IDENTITY  NORM(n -> inf) == EW_ELIG   max|dw| {worst:.3e}  (4 panels)")
    assert worst < 1e-12
    say("   -> under NORM the ladder's limit is the EQUAL-WEIGHT ELIGIBLE book, NOT EWall: "
        "EWall holds the gated-out names, EW_ELIG does not. 'Converges to EWall' is false by "
        "construction; what has to be tested is convergence to EW_ELIG.")

    # G2 re-execution of lane C's committed NORM grid (same code, so a determinism check only)
    lc = pd.read_csv(OUT / f"{LANEC}.grid.csv")
    lcn = lc[(lc.conv == "NORM") & lc.n.notna()].copy()
    lcn["panel"] = lcn.panel.replace({"SMALL439": "SMALL439+SPY"})   # lane C holds SPY there
    mine = L[L.arm.str.startswith("NORM")].copy()
    j = lcn.merge(mine, left_on=["panel", "n", "bps"], right_on=["panel", "n", "bps"],
                  suffixes=("_C", ""))
    if len(j):
        say(f"G2 RE-EXECUTION of lane C's committed NORM grid, {len(j)} shared (panel, n, rung) "
            f"cells: max|dSharpe| {float(np.abs(j.Sharpe - j.Sharpe_C).max()):.3e}  "
            f"max|dCAGR| {float(np.abs(j.CAGR - j.CAGR_C).max()):.3e}  "
            f"max|dOOS_Sharpe| {float(np.abs(j.OOS_Sharpe - j.OOS_Sharpe_C).max()):.3e}")
        say("   NOT independent corroboration: lane C's module is IMPORTED and its functions "
            "are used verbatim, so only a data revision could move these.")
        assert float(np.abs(j.Sharpe - j.Sharpe_C).max()) < 1e-9

    # ---------------------------------------------------------------- (0) SPY in the book
    say("\n=== (0) IS SPY IN THE BOOK? — the small panel's joined BENCHMARK, priced ===")
    say("    baseline.load_universe(small=True) joins SPY as a benchmark, NOT a constituent, "
        "but lane C's")
    say("    ladder ranks and holds every column, SPY included. Same code, same data, the only "
        "difference")
    say("    being whether SPY may be bought (SMALL439+SPY = lane C's convention):")
    a = L[(L.panel == "SMALL439") & (L.bps == VERDICT_RUNG)].set_index("arm")
    b = L[(L.panel == "SMALL439+SPY") & (L.bps == VERDICT_RUNG)].set_index("arm")
    cmp_ = pd.DataFrame({"Sharpe_noSPY": a.Sharpe, "Sharpe_laneC": b.Sharpe,
                         "d_Sharpe": b.Sharpe - a.Sharpe,
                         "CAGR_noSPY": a.CAGR, "CAGR_laneC": b.CAGR,
                         "d_CAGR": b.CAGR - a.CAGR,
                         "OOS_noSPY": a.OOS_Sharpe, "OOS_laneC": b.OOS_Sharpe,
                         "d_OOS": b.OOS_Sharpe - a.OOS_Sharpe}).loc[
        ["EW_ALL", "EW_ELIG"] + [f"NORM{n}" for n in NS]]
    say(cmp_.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"    max |d Sharpe| {float(cmp_.d_Sharpe.abs().max()):.4f} at "
        f"{cmp_.d_Sharpe.abs().idxmax()}; max |d OOS Sharpe| "
        f"{float(cmp_.d_OOS.abs().max()):.4f} at {cmp_.d_OOS.abs().idxmax()}. "
        f"The narrow arms are where a single benchmark holding is worth 1/n of the book.")

    # ---------------------------------------------------------------- (1) the ladder
    say("\n=== (1) THE NORM LADDER, every grid point, verdict rung 10 bps ===")
    for pname, _, _ in PANELS:
        sub = L[(L.panel == pname) & (L.bps == VERDICT_RUNG)].copy()
        ctl = sub[sub.arm == "EW_ALL"].iloc[0]
        el = sub[sub.arm == "EW_ELIG"].iloc[0]
        sub["exc_all"] = sub.Sharpe - ctl.Sharpe
        sub["exc_elig"] = sub.Sharpe - el.Sharpe
        sub["exc_all_OOS"] = sub.OOS_Sharpe - ctl.OOS_Sharpe
        sub["exc_elig_OOS"] = sub.OOS_Sharpe - el.OOS_Sharpe
        say(f"\n--- {pname} (SPY {M.loc[pname].spy_Sharpe:.4f}, OOS "
            f"{M.loc[pname].spy_OOS_Sharpe:.4f}; RULES v2 {M.loc[pname].v2_Sharpe:.4f}, OOS "
            f"{M.loc[pname].v2_OOS_Sharpe:.4f}) ---")
        say(sub[["arm", "real_gross", "turn_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "IS_Sharpe", "OOS_Sharpe", "ov_all", "ov_elig", "exc_all", "exc_elig",
                 "exc_all_OOS", "exc_elig_OOS", "fail4a", "fail4b"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- (2) interior optimum
    say("\n=== (2) DOES AN INTERIOR OPTIMUM EXIST? (argmax over the 13-point n ladder; "
        "'interior' = neither n=5 nor n=240) ===")
    irows = []
    for pname, _, _ in PANELS:
        for bps in RUNGS:
            sub = L[(L.panel == pname) & (L.bps == bps) & L.arm.str.startswith("NORM")]
            ctl = L[(L.panel == pname) & (L.bps == bps) & (L.arm == "EW_ALL")].iloc[0]
            el = L[(L.panel == pname) & (L.bps == bps) & (L.arm == "EW_ELIG")].iloc[0]
            a_full = sub.loc[sub.Sharpe.idxmax()]
            a_oos = sub.loc[sub.OOS_Sharpe.idxmax()]
            a_is = sub.loc[sub.IS_Sharpe.idxmax()]
            irows.append(dict(
                panel=pname, bps=bps,
                argmax_full=int(a_full.n), full_Sharpe=a_full.Sharpe,
                interior_full=5 < a_full.n < 240,
                argmax_OOS=int(a_oos.n), OOS_Sharpe=a_oos.OOS_Sharpe,
                interior_OOS=5 < a_oos.n < 240,
                argmax_IS=int(a_is.n),
                best_minus_elig=a_full.Sharpe - el.Sharpe,
                bestOOS_minus_eligOOS=a_oos.OOS_Sharpe - el.OOS_Sharpe,
                best_minus_ewall=a_full.Sharpe - ctl.Sharpe,
                bestOOS_minus_ewallOOS=a_oos.OOS_Sharpe - ctl.OOS_Sharpe,
                elig_Sharpe=el.Sharpe, elig_OOS=el.OOS_Sharpe,
                ewall_Sharpe=ctl.Sharpe, ewall_OOS=ctl.OOS_Sharpe,
                ov_elig_at_n240=float(sub[sub.n == 240].ov_elig.iloc[0]),
                ov_all_at_n240=float(sub[sub.n == 240].ov_all.iloc[0])))
    I = pd.DataFrame(irows)
    say(I.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\n  INTERIOR full-sample argmax in {int(I.interior_full.astype(bool).sum())} of "
        f"{len(I)} (panel, rung) cells; INTERIOR OOS argmax in "
        f"{int(I.interior_OOS.astype(bool).sum())} of {len(I)}.")
    say(f"  The best n on the ladder beats EW_ELIG (the ladder's own limit) full-sample in "
        f"{int((I.best_minus_elig > 0).sum())} of {len(I)} and OOS in "
        f"{int((I.bestOOS_minus_eligOOS > 0).sum())} of {len(I)} — and that is the ORACLE n, "
        f"chosen with the answer in hand.")
    say(f"  Against EW_ALL: full {int((I.best_minus_ewall > 0).sum())}/{len(I)}, "
        f"OOS {int((I.bestOOS_minus_ewallOOS > 0).sum())}/{len(I)}.")

    # convergence: how fast does overlap with EW_ELIG go to 1
    say("\n  CONVERGENCE (overlap with EW_ELIG / with EW_ALL, 10 bps):")
    piv = L[(L.bps == VERDICT_RUNG) & L.arm.str.startswith("NORM")].pivot(
        index="panel", columns="n", values="ov_elig")
    say("   overlap vs EW_ELIG\n" + piv.to_string(float_format=lambda x: f"{x:.3f}"))
    piv2 = L[(L.bps == VERDICT_RUNG) & L.arm.str.startswith("NORM")].pivot(
        index="panel", columns="n", values="ov_all")
    say("   overlap vs EW_ALL\n" + piv2.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- (3) rule 8
    say("\n=== (3) RULE 8 — n chosen on <= 2016 by IS Sharpe, 2017-2026 read ONCE ===")
    for pname, _, _ in PANELS:
        for bps in RUNGS:
            sub = L[(L.panel == pname) & (L.bps == bps) & L.arm.str.startswith("NORM")]
            ctl = L[(L.panel == pname) & (L.bps == bps) & (L.arm == "EW_ALL")].iloc[0]
            el = L[(L.panel == pname) & (L.bps == bps) & (L.arm == "EW_ELIG")].iloc[0]
            pick = sub.loc[sub.IS_Sharpe.idxmax()]
            orac = sub.loc[sub.OOS_Sharpe.idxmax()]
            wf.append(dict(panel=pname, bps=bps, pick_n=int(pick.n), IS_Sharpe=pick.IS_Sharpe,
                           IS_elig=el.IS_Sharpe, IS_ewall=ctl.IS_Sharpe,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_MaxDD=pick.OOS_MaxDD, oracle_n=int(orac.n),
                           oracle_OOS=orac.OOS_Sharpe,
                           OOS_elig=el.OOS_Sharpe, OOS_elig_CAGR=el.OOS_CAGR,
                           OOS_ewall=ctl.OOS_Sharpe, OOS_ewall_CAGR=ctl.OOS_CAGR,
                           v2_OOS=M.loc[pname].v2_OOS_Sharpe, spy_OOS=M.loc[pname].spy_OOS_Sharpe,
                           beats_elig=pick.OOS_Sharpe > el.OOS_Sharpe,
                           beats_ewall=pick.OOS_Sharpe > ctl.OOS_Sharpe,
                           beats_v2=pick.OOS_Sharpe > M.loc[pname].v2_OOS_Sharpe,
                           beats_spy=pick.OOS_Sharpe > M.loc[pname].spy_OOS_Sharpe,
                           IS_pick_beats_IS_elig=pick.IS_Sharpe > el.IS_Sharpe,
                           fail4a=pick.fail4a, fail4b=pick.fail4b))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for col, what in [("beats_elig", "EW_ELIG (the ladder's own limit)"),
                      ("beats_ewall", "EW_ALL"), ("beats_v2", "RULES v2 (live)"),
                      ("beats_spy", "SPY")]:
        s = W[col].astype(bool)
        say(f"  IS-chosen n beats {what} OOS in {int(s.sum())} of {len(s)} (panel, rung) cells")
    say(f"  IS pick == OOS oracle in {int((W.pick_n == W.oracle_n).sum())} of {len(W)}; "
        f"mean OOS Sharpe regret vs the oracle {float((W.oracle_OOS - W.OOS_Sharpe).mean()):+.4f}")
    say(f"  the IS-chosen n has a HIGHER IS Sharpe than EW_ELIG in "
        f"{int(W.IS_pick_beats_IS_elig.astype(bool).sum())} of {len(W)} cells — i.e. the "
        f"chooser had a reason to rank at all in only that many.")

    # ---------------------------------------------------------------- (4) keep paths
    say("\n=== (4) BOTH KEEP PATHS, every arm and rung (4a vs LIVE RULES v2, 4b vs SPY) ===")
    K = L.copy()
    K["pass4a"] = K.fail4a == ""
    K["pass4b"] = K.fail4b == ""
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    say(f"  4a {int(K.pass4a.sum())} of {len(K)} rows;  4b {int(K.pass4b.sum())} of {len(K)}")
    say(K.groupby(["panel"])[["pass4a", "pass4b"]].sum().astype(int).to_string())
    if K.pass4b.any():
        say("\n  4b passers:")
        say(K[K.pass4b][["panel", "arm", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "real_gross", "turn_yr"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say("  (each 4b passer's own EW_ELIG and EW_ALL controls, same panel and rung, are in "
            "the ladder table above — read the excess columns before treating any of these as "
            "a candidate.)")

    say("\nSURVIVORSHIP: B136 / BSTK100 are current constituents of universe_broad.json and "
        "SMALL439 is the sub-$2B screen's survivors since 2010 (44 tickers with max_1d_move "
        ">= 1.0 dropped). Levels are upward-biased and not achievable; every reading here is a "
        "within-panel contrast between books on the same days.")
    say(f"\nwrote {STEM}.ladder.csv / .walkforward.csv / .keep.csv")
    flush()


if __name__ == "__main__":
    run()
