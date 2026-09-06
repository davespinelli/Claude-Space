#!/usr/bin/env python3
"""QUEUE idea 250 — locate-the-band-width-ceiling (cloud, 2026-09-06).

Question (pre-registered, copied from QUEUE.md before any number below was read)
-------------------------------------------------------------------------------
Idea 74's PARK by-product (u56 EWALL0 + a 12% MA re-entry band: 14.1% / 1.233 / -19.4%,
OOS 1.272, 1.9x turnover, exchange rate -0.26 pp/pp) sits at the WIDEST point of idea
74's band ladder, with Sharpe monotone in width and turnover falling 6.4x -> 1.9x.  That
is a grid edge, exactly like idea 240's n.  Two questions, both stated so they can fail:

  Q1  DOES AN INTERIOR OPTIMUM EXIST AT ALL?  Run band width in {12, 16, 20, 25, 30}%
      (idea 74's published rungs 3/5/8% carried along as context) on u56 / B136 /
      SMALL484 under the constant-gross convention.  If the Sharpe argmax lands at 30%
      in every cell, the ladder is still unbounded and the "12% is best" reading was an
      artefact of where idea 74 stopped looking.  An interior argmax at 16-25% in the
      large-cap cells is the finding the queue is hoping for.

  Q2  DOES THE BROAD-PANEL DRAWDOWN FAILURE CLOSE ANYWHERE ON THE LADDER?  Idea 74's
      broad cell failed 4b on DD at -21.7% against the -20.2% cap.  A wider band holds
      names through deeper dips, so the naive prediction is that the margin gets WORSE,
      not better, as width rises.  Reported at every rung and both cost rungs.

Pre-registered secondary reads (reported, never selected on)
  * The mechanism behind any ceiling: at some width the band stops being a gate at all
    because no name ever crosses out.  `exit_frac` (share of name-days the gate holds
    OUT of the book) and `flips` (crossings per name per year) are printed at every
    rung, so a flat Sharpe tail can be told apart from a genuine optimum.
  * The exchange rate against the no-instrument control (idea 74's axis) at every rung.
  * Both KEEP paths (4a and 4b) at every one of the reported points.

Design (PROTOCOL rules 1-9)
---------------------------
Universes : u56    = load_universe()              (56 names + SPY)
            B136   = load_universe(broad=True)    (136 names)
            SMALL484 = load_universe(small=True) with the max_1d_move >= 1.0 screen of
            data/small_meta.csv applied FIRST (PROTOCOL/queue requirement).
            SURVIVORSHIP: all three lists are CURRENT CONSTITUENTS.  Delisted and
            acquired names are absent, which flatters every stay-invested setting — and
            a wide re-entry band is the most stay-invested setting on the ladder.  So
            this run's bias points TOWARD the wide end: a finding that the ladder keeps
            improving out to 30% is exactly what survivorship would manufacture, and is
            reported as suspect rather than as an edge.  A finding AGAINST the wide end
            is, if anything, understated.
Books     : idea 245's two INSTRUMENT-FREE base books, IMPORTED not re-implemented —
            EWALL0 (equal-weight every name, no gates; idea 74's PARK book) and CAND20
            (top-20 by composite, no gates).  Both at GROSS = 0.75, and `apply_gate`
            re-normalises the survivors back to GROSS: that IS the constant-gross
            convention idea 250 asks for (idea 244's channel is closed by construction).
Params    : exactly ONE tuned dimension — band width b in
            {3, 5, 8, 12, 16, 20, 25, 30} %.  Panel (3), book (2) and cost (2) are
            REPORTED at every value and never selected on.  ALL 8 x 3 x 2 x 2 = 96
            points are printed.
Costs     : 10 bps (PROTOCOL, verdicts read here) and 25 bps, applied analytically
            (net = gross - turnover * bps/1e4), exact because the held path does not
            depend on cost_bps.
Execution : PROTOCOL rule 2 — the gate is read at close t and executed at close t+1
            (idea 245's simulator shifts the target by one bar).  Weekly rebalance.
Baseline  : RULES v1 weekly on the same panel (4a) and SPY buy-and-hold (4b).  BOTH KEEP
            paths evaluated for every point.
Rule 8    : the band width is chosen on 2009-2016 IS ONLY, and 2017-2026 is read once.
            Four selectors: SEL-IS (argmax IS Sharpe), SEL-4b (argmax IS Sharpe among
            widths clearing the IS-readable 4b bars, abstains if none), PIN12 (idea 74's
            published width, not chosen) and CTL (the no-band control).  OOS CAGR /
            Sharpe / MaxDD reported against the control's, RULES v1's and SPY's OOS.

Reproduction gates, asserted before any new number is read
  [A] idea 245's own harness ([A] engine equivalence, [B] dg lever, [C] idea 94's stop).
  [D] this script's band arm at level 0.12 on u56 / EWALL0 / 10 bps reproduces idea 74's
      published PARK row (14.1% / 1.233 / -19.4%, OOS 1.272, 1.9x turnover) to the
      precision it was published at.
  [E] the band ladder is nested: a wider band can only be OUT of a name on a subset of
      the days a narrower one is out is NOT true in general (the band is a hysteresis
      state machine, not a threshold), so instead the weaker invariant is asserted —
      exit_frac is non-increasing in width, and asserted only as a REPORTED monotonicity
      check, printed whether it holds or not.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-06_locate-the-band-width-ceiling_cloud"
OUT = ROOT / "research" / "backtests"
SCRIPT = f"research/backtests/{STEM}.py"

# --- import idea 245's module (base books, simulator, band instrument) ---------
_p245 = OUT / "2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py"
_spec = importlib.util.spec_from_file_location("i245", _p245)
i245 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(i245)
run, gate_mask, apply_gate = i245.run, i245.gate_mask, i245.apply_gate
BASE_BOOKS, harness = i245.BASE_BOOKS, i245.harness
m, halves, at_cost, turn_per_yr = i245.m, i245.halves, i245.at_cost, i245.turn_per_yr
fail4a, fail4b = i245.fail4a, i245.fail4b
GROSS, FREQ = i245.GROSS, i245.FREQ

BANDS = [0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30]   # THE one tuned parameter
NEW = [0.12, 0.16, 0.20, 0.25, 0.30]                        # the queue's rungs
COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PIN = 0.12                                                  # idea 74's published point

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flip_stats(mask):
    """(share of name-days OUT of the book, crossings per name per year)."""
    mk = mask.astype(float)
    n_days, n_names = mk.shape
    flips = float(mk.diff().abs().sum().sum())
    return 1.0 - float(mk.values.mean()), flips / max(n_names, 1) / (n_days / 252.0)


def panels():
    out = {}
    px = load_universe()
    out["u56"] = px
    P(f"  u56      {px.shape[1]:4d} columns  {px.index[0].date()} -> {px.index[-1].date()}")
    pb = load_universe(broad=True)
    out["B136"] = pb
    P(f"  B136     {pb.shape[1]:4d} columns  {pb.index[0].date()} -> {pb.index[-1].date()}")
    ps = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in ps.columns if c != "SPY" and c not in bad]
    dropped = len([c for c in ps.columns if c != "SPY" and c in bad])
    ps = ps[keep + ["SPY"]].dropna(how="all").ffill()
    out["SMALL484"] = ps
    P(f"  SMALL484 {ps.shape[1]:4d} columns ({len(keep)} tradable, dropped {dropped} with "
      f"max_1d_move >= 1.0)  {ps.index[0].date()} -> {ps.index[-1].date()}")
    P("  SURVIVORSHIP (PROTOCOL rule 9 / idea 54): all three are current-constituent lists; "
      "no delisted or acquired names.  That bias flatters the WIDE end of this ladder.")
    return out


def main():
    P("=" * 190)
    P("IDEA 250 — LOCATE THE BAND-WIDTH CEILING.  Idea 74 stopped at 12%; does an interior "
      "optimum exist above it, and does the broad-panel DD failure close anywhere?")
    P(f"  one tuned parameter: band width in {[f'{b:.0%}' for b in BANDS]}  "
      f"(idea 74's rungs 3/5/8% carried as context; {[f'{b:.0%}' for b in NEW]} are new)")
    P(f"  3 panels x 2 books x {len(COSTS)} cost rungs x {len(BANDS)} widths = "
      f"{3*2*len(COSTS)*len(BANDS)} reported points.  Constant-gross convention "
      f"(survivors re-normalised to GROSS = {GROSS}).  Weekly, t+1 execution.")
    P("=" * 190)

    PX = {}
    P("\npanels:")
    PX = panels()

    P("\n" + "=" * 190)
    P("HARNESS GATE [A] — idea 245's own reproduction gates on u56 (engine equivalence, dg "
      "lever, idea 94 stop):")
    harness(PX["u56"])

    ROWS, REF, MASKS = [], {}, []
    for pname, px in PX.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        sc, ss, sdd = m(spy)
        s1, s2 = halves(spy)
        spy_oos = m(spy.loc[OOS_START:])
        spy_is = m(spy.loc[:IS_END])
        s1i, s2i = halves(spy.loc[:IS_END])
        v1 = backtest(px, rules_v1_weights(px), cost_bps=PROTO_COST, freq=FREQ)["returns"].loc[start:]
        REF[pname] = dict(spy=spy, spy_oos_sh=spy_oos[1], v1=v1, start=start,
                          cap=0.60 * sdd, floor=0.70 * sc,
                          cap_is=0.60 * spy_is[2], floor_is=0.70 * spy_is[0],
                          s1i=s1i, s2i=s2i, spy_is_oos=None)
        P(f"\n{'='*190}\nPANEL {pname}: eval {start.date()} -> {px.index[-1].date()}")
        P(f"  SPY  {sc:.2%} / {ss:.3f} / {sdd:.2%}   halves {s1:.3f}/{s2:.3f}   "
          f"OOS {spy_oos[0]:.2%} / {spy_oos[1]:.3f} / {spy_oos[2]:.2%}")
        P(f"  4b bars: Sharpe > {s1:.3f} (H1) / {s2:.3f} (H2) / {spy_oos[1]:.3f} (OOS);  "
          f"MaxDD >= {0.60*sdd:.2%};  CAGR >= {0.70*sc:.2%}")
        mv, mvo = m(v1), m(v1.loc[OOS_START:])
        P(f"  RULES v1 @10bps  {mv[0]:.2%} / {mv[1]:.3f} / {mv[2]:.2%}   halves "
          f"{halves(v1)[0]:.3f}/{halves(v1)[1]:.3f}   OOS {mvo[0]:.2%} / {mvo[1]:.3f} / {mvo[2]:.2%}")

        for b in BANDS:
            mk = gate_mask(px, "band", b)
            ef, fl = flip_stats(mk.loc[start:])
            MASKS.append(dict(panel=pname, band=b, exit_frac=ef, flips_per_name_yr=fl))

        for bname, wfn in BASE_BOOKS.items():
            w = wfn(px)
            cg, ct, ci, _ = run(px, w)                       # no-band control
            cg, ct, ci = cg.loc[start:], ct.loc[start:], ci.loc[start:]
            for b in [None] + BANDS:
                if b is None:
                    gg, tt, ii = cg, ct, ci
                else:
                    r = run(px, apply_gate(w, gate_mask(px, "band", b)))
                    gg, tt, ii = r[0].loc[start:], r[1].loc[start:], r[2].loc[start:]
                for c in COSTS:
                    rr = at_cost(gg, tt, c)
                    cc = at_cost(cg, ct, c)
                    cagr, sh, dd = m(rr)
                    h1, h2 = halves(rr)
                    o = m(rr.loc[OOS_START:])
                    i_ = m(rr.loc[:IS_END])
                    ih1, ih2 = halves(rr.loc[:IS_END])
                    c_cagr, _, c_dd = m(cc)
                    bought = 100 * (dd - c_dd)               # pp of MaxDD bought (>0 = shallower)
                    paid = 100 * (c_cagr - cagr)
                    f4a = fail4a(rr, REF[pname]["v1"] if c == PROTO_COST else REF[pname]["v1"])
                    f4b = fail4b(rr, spy, o[1], REF[pname]["spy_oos_sh"])
                    ROWS.append(dict(
                        panel=pname, book=bname, cost=c,
                        band=(np.nan if b is None else b),
                        CAGR=cagr, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                        OOS_CAGR=o[0], OOS_Sharpe=o[1], OOS_MaxDD=o[2],
                        IS_CAGR=i_[0], IS_Sharpe=i_[1], IS_MaxDD=i_[2], IS_H1=ih1, IS_H2=ih2,
                        TO=turn_per_yr(tt), gross_mean=float(ii.mean()),
                        dd_margin_pp=100 * (dd - REF[pname]["cap"]),
                        cagr_margin_pp=100 * (cagr - REF[pname]["floor"]),
                        bought_pp=bought, paid_pp=paid,
                        rate=(paid / bought if bought > 1e-9 else np.nan),
                        fail4a=",".join(f4a) or "-", fail4b=",".join(f4b) or "-",
                        pass4a=(not f4a), pass4b=(not f4b)))
            P(f"  ... {pname}/{bname} done")

    D = pd.DataFrame(ROWS)
    D.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    M = pd.DataFrame(MASKS)
    M.to_csv(OUT / f"{STEM}.gate.csv", index=False)

    # ---------------------------------------------------------------- gate [D]
    P("\n" + "=" * 190)
    P("HARNESS GATE [D] — reproduce idea 74's published PARK row before anything new is read")
    r = D[(D.panel == "u56") & (D.book == "EWALL0") & (D.cost == PROTO_COST) &
          (D.band == PIN)].iloc[0]
    exp = (0.141, 1.233, -0.194, 1.272, 1.9)
    got = (r.CAGR, r.Sharpe, r.MaxDD, r.OOS_Sharpe, r.TO)
    ok = (abs(got[0] - exp[0]) < 1e-3 and abs(got[1] - exp[1]) < 2e-3 and
          abs(got[2] - exp[2]) < 1e-3 and abs(got[3] - exp[3]) < 2e-3 and
          abs(got[4] - exp[4]) < 0.06)
    P(f"  u56/EWALL0/band 12%/10bps: {r.CAGR:.1%} / {r.Sharpe:.3f} / {r.MaxDD:.1%}  "
      f"OOS Sharpe {r.OOS_Sharpe:.3f}  turnover {r.TO:.2f}x")
    P(f"  idea 74 published:         14.1% / 1.233 / -19.4%  OOS Sharpe 1.272  turnover 1.9x  "
      f"-> {'PASS' if ok else 'FAIL'}")
    assert ok, (got, exp)

    # ---------------------------------------------------------------- gate [E] / mechanism
    P("\n" + "=" * 190)
    P("GATE [E] / MECHANISM — how much gate is left at each width.  exit_frac = share of "
      "name-days the band holds OUT of the book; flips = crossings per name per year.")
    P(M.pivot(index="band", columns="panel", values="exit_frac").to_string(
        float_format=lambda x: f"{x:.4f}"))
    P("\n  flips per name per year:")
    P(M.pivot(index="band", columns="panel", values="flips_per_name_yr").to_string(
        float_format=lambda x: f"{x:.3f}"))
    for pn, g in M.groupby("panel"):
        g = g.sort_values("band")
        mono = bool((g.exit_frac.diff().dropna() <= 1e-12).all())
        P(f"  exit_frac monotone non-increasing in width on {pn}: {mono} "
          f"({g.exit_frac.iloc[0]:.4f} at 3% -> {g.exit_frac.iloc[-1]:.4f} at 30%)")

    # ---------------------------------------------------------------- Q1
    P("\n" + "=" * 190)
    P("Q1 — THE FULL LADDER, EVERY POINT.  band = NaN is the no-band control.")
    cols = ["band", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "TO", "gross_mean", "bought_pp", "paid_pp", "rate",
            "dd_margin_pp", "cagr_margin_pp", "fail4a", "fail4b"]
    for pn in PX:
        for bk in BASE_BOOKS:
            for c in COSTS:
                S = D[(D.panel == pn) & (D.book == bk) & (D.cost == c)].sort_values(
                    "band", na_position="first")
                P(f"\n--- {pn} / {bk} / {c} bps ---")
                P(S[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 190)
    P("Q1 VERDICT — WHERE IS THE SHARPE ARGMAX?  (edge = 30%, the new grid top; an argmax at "
      "16-25% is an INTERIOR optimum, which is what idea 250 asks for.)")
    B = D[D.band.notna()]
    arg = B.loc[B.groupby(["panel", "book", "cost"]).Sharpe.idxmax(),
                ["panel", "book", "cost", "band", "Sharpe", "OOS_Sharpe", "MaxDD", "TO"]]
    arg["at_new_edge"] = arg.band == max(BANDS)
    arg["interior"] = (~arg.band.isin([min(BANDS), max(BANDS)]))
    P(arg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  argmax at the NEW grid edge (30%) in {int(arg.at_new_edge.sum())}/{len(arg)} cells; "
      f"INTERIOR in {int(arg.interior.sum())}/{len(arg)}.")
    P("\n  the same argmax on OOS Sharpe (reported, not a selector):")
    argo = B.loc[B.groupby(["panel", "book", "cost"]).OOS_Sharpe.idxmax(),
                 ["panel", "book", "cost", "band", "OOS_Sharpe"]]
    P(argo.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  Sharpe by width, mean over the 12 (panel, book, cost) cells, and per panel:")
    P(B.pivot_table(index="band", columns="panel", values="Sharpe", aggfunc="mean").to_string(
        float_format=lambda x: f"{x:.4f}"))
    P("\n  is Sharpe still MONOTONE in width above 12%?  (Spearman of Sharpe on width over the "
      "5 new rungs, per cell; +1 = still climbing to the edge)")
    sp = []
    for (pn, bk, c), g in B[B.band >= PIN].groupby(["panel", "book", "cost"]):
        g = g.sort_values("band")
        sp.append(dict(panel=pn, book=bk, cost=c,
                       rho=float(np.corrcoef(g.band.rank(), g.Sharpe.rank())[0, 1]),
                       Sharpe_12=float(g.Sharpe.iloc[0]), Sharpe_30=float(g.Sharpe.iloc[-1]),
                       d_12_to_30=float(g.Sharpe.iloc[-1] - g.Sharpe.iloc[0])))
    SP = pd.DataFrame(sp)
    P(SP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  mean rho {SP.rho.mean():+.3f};  Sharpe rises from 12% to 30% in "
      f"{int((SP.d_12_to_30 > 0).sum())}/{len(SP)} cells (mean {SP.d_12_to_30.mean():+.4f}).")

    # ---------------------------------------------------------------- Q2
    P("\n" + "=" * 190)
    P("Q2 — DOES THE BROAD-PANEL DRAWDOWN FAILURE CLOSE ANYWHERE ON THE LADDER?")
    P("  dd_margin_pp = MaxDD - 0.60 x SPY MaxDD, in pp.  POSITIVE = inside the 4b cap.")
    for bk in BASE_BOOKS:
        for c in COSTS:
            S = D[(D.panel == "B136") & (D.book == bk) & (D.cost == c)].sort_values(
                "band", na_position="first")
            P(f"\n--- B136 / {bk} / {c} bps ---")
            P(S[["band", "MaxDD", "dd_margin_pp", "CAGR", "cagr_margin_pp", "Sharpe",
                 "H1", "H2", "OOS_Sharpe", "fail4b"]].to_string(
                    index=False, float_format=lambda x: f"{x:.4f}"))
    closed = D[(D.panel == "B136") & (D.band.notna()) & (D.dd_margin_pp > 0)]
    P(f"\n  B136 points inside the DD cap at ANY width: {len(closed)} of "
      f"{len(D[(D.panel=='B136') & D.band.notna()])}.")
    if len(closed):
        P(closed[["book", "cost", "band", "MaxDD", "dd_margin_pp", "fail4b"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  4b failure reasons by width on B136 (which bar binds where):")
    P(D[(D.panel == "B136") & D.band.notna()].pivot_table(
        index="band", columns=["book", "cost"], values="fail4b", aggfunc="first").to_string())

    # ---------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 190)
    P("BOTH KEEP PATHS OVER THE WHOLE LADDER (PROTOCOL rule 4).")
    P(B.groupby("band").agg(points=("Sharpe", "size"), pass4a=("pass4a", "sum"),
                            pass4b=("pass4b", "sum"), Sharpe=("Sharpe", "mean"),
                            CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                            OOS_Sharpe=("OOS_Sharpe", "mean"), TO=("TO", "mean")
                            ).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  every 4b PASS in the grid:")
    K = D[D.pass4b]
    if len(K):
        P(K[["panel", "book", "cost", "band", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "OOS_Sharpe", "TO", "pass4a"]].to_string(index=False,
                                                      float_format=lambda x: f"{x:.4f}"))
    else:
        P("  none.")
    P("\n  every 4a PASS in the grid:")
    K4 = D[D.pass4a]
    P(("  none." if not len(K4) else
       K4[["panel", "book", "cost", "band", "Sharpe", "MaxDD", "H1", "H2", "fail4b"]].to_string(
           index=False, float_format=lambda x: f"{x:.4f}")))

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 190)
    P("PROTOCOL RULE 8 — WALK-FORWARD.  Width chosen on 2009-2016 ONLY; 2017-2026 read once.")
    P("  SEL-IS  argmax IS Sharpe over the 8 widths      SEL-4b  argmax IS Sharpe among widths")
    P("  PIN12   idea 74's published 12%, not chosen             clearing the IS-readable 4b bars")
    P("  CTL     the no-band control (do nothing)")
    WF = []
    for (pn, bk, c), S in D[D.band.notna()].groupby(["panel", "book", "cost"]):
        R = REF[pn]
        adm = S[(S.IS_MaxDD >= R["cap_is"]) & (S.IS_CAGR > R["floor_is"]) &
                (S.IS_H1 > R["s1i"]) & (S.IS_H2 > R["s2i"])]
        ctl = D[(D.panel == pn) & (D.book == bk) & (D.cost == c) & (D.band.isna())].iloc[0]
        v1o = m(R["v1"].loc[OOS_START:])
        spyo = m(R["spy"].loc[OOS_START:])
        picks = {"SEL-IS": S.loc[S.IS_Sharpe.idxmax()],
                 "SEL-4b": (adm.loc[adm.IS_Sharpe.idxmax()] if len(adm) else None),
                 "PIN12": S[S.band == PIN].iloc[0],
                 "CTL": ctl}
        for sel, r in picks.items():
            base = dict(panel=pn, book=bk, cost=c, sel=sel,
                        spy_OOS_Sharpe=spyo[1], spy_OOS_CAGR=spyo[0], spy_OOS_MaxDD=spyo[2],
                        v1_OOS_Sharpe=v1o[1], v1_OOS_CAGR=v1o[0], v1_OOS_MaxDD=v1o[2],
                        ctl_OOS_Sharpe=ctl.OOS_Sharpe)
            if r is None:
                WF.append(dict(base, band=np.nan, OOS_CAGR=np.nan, OOS_Sharpe=np.nan,
                               OOS_MaxDD=np.nan, pass4a=False, pass4b=False))
                continue
            WF.append(dict(base, band=r.band, OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                           OOS_MaxDD=r.OOS_MaxDD, pass4a=bool(r.pass4a), pass4b=bool(r.pass4b)))
    W = pd.DataFrame(WF)
    W["beat_SPY"] = W.OOS_Sharpe > W.spy_OOS_Sharpe
    W["beat_v1"] = W.OOS_Sharpe > W.v1_OOS_Sharpe
    W["beat_CTL"] = W.OOS_Sharpe > W.ctl_OOS_Sharpe
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  widths chosen on the IS window:")
    P(W[W.sel.isin(["SEL-IS", "SEL-4b"])].pivot_table(
        index=["panel", "book"], columns=["sel", "cost"], values="band").to_string(
            float_format=lambda x: f"{x:.3f}"))
    P("\n  OOS outcome by selector, mean over the 12 (panel, book, cost) cells:")
    P(W.groupby("sel").agg(cells=("band", lambda s: int(s.notna().sum())),
                           mean_band=("band", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                           OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_MaxDD=("OOS_MaxDD", "mean"),
                           beat_SPY=("beat_SPY", "sum"), beat_v1=("beat_v1", "sum"),
                           beat_CTL=("beat_CTL", "sum"), pass4a=("pass4a", "sum"),
                           pass4b=("pass4b", "sum")).to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  per-cell walk-forward, every selector:")
    P(W[["panel", "book", "cost", "sel", "band", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "spy_OOS_Sharpe", "v1_OOS_Sharpe", "ctl_OOS_Sharpe", "beat_SPY", "beat_v1",
         "beat_CTL", "pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  does the IS chooser beat doing nothing OOS?  (SEL-IS minus CTL, per cell)")
    piv = W.pivot_table(index=["panel", "book", "cost"], columns="sel", values="OOS_Sharpe")
    piv["SELIS_minus_CTL"] = piv["SEL-IS"] - piv["CTL"]
    piv["SELIS_minus_PIN12"] = piv["SEL-IS"] - piv["PIN12"]
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"  mean SEL-IS - CTL = {piv.SELIS_minus_CTL.mean():+.4f} "
      f"({int((piv.SELIS_minus_CTL > 0).sum())}/{len(piv)} cells positive);  "
      f"mean SEL-IS - PIN12 = {piv.SELIS_minus_PIN12.mean():+.4f} "
      f"({int((piv.SELIS_minus_PIN12 > 0).sum())}/{len(piv)} positive).")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nwrote {STEM}.grid.csv / .gate.csv / .walkforward.csv / .console.txt")


if __name__ == "__main__":
    main()
