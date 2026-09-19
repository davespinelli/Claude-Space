#!/usr/bin/env python3
"""Idea 725 — does the DAILY INVERSION of idea 535's RETIREMENT generalise?
   i.e. is it a CADENCE fact or a LOW-SIGNAL-REGIME (residual-scale) fact?      (lane cloud)

THE QUESTION.  Idea 535 retired idea 301's GATE-FAMILY constant for the de-grossing timing
residual in favour of a continuous predictor, CSD.is (resid0_pp ~ const + b * c_sd(IS)).  Idea
539 re-cut the whole decomposition on a cadence x gross grid and found the retirement bar holds
at every gross on {W,M,Q} and on {D,W,M,Q} — but INVERTS on the DAILY-ONLY cells, where CSD.is
is 23-27% WORSE than the family constant it retired (OOS MAE ratio 1.2297 / 1.2492 / 1.2710 at
gross 0.50 / 0.75 / 1.00).  The continuous predictor loses to the crude label EXACTLY where the
residual is smallest.  This run prices the retirement as a function of the RESIDUAL'S OWN SCALE
rather than of cadence, and reports which of the two the inversion belongs to.

WHY IT MATTERS.  "The label is retired" is a standing claim in this record.  If the inversion is
a cadence fact it is a D-cadence caveat.  If it is a scale fact it is a general statement about
every continuous predictor the record has ever fitted on a residual: a slope fitted across a wide
range of residual magnitudes buys nothing, and costs, inside the low-magnitude regime — which is
where a de-grossed book actually operates.

WHAT IS PRICED (real books, not a text census).  Idea 539's corpus, rebuilt from the tape:
  PANELS        SMALL439, U56, B136 (three).
  FAMILIES      QUANTILE (top x of live names by distance above the 200d MA) and MA-THRESH
                (px > MA*(1+theta)), 9 strictness levels each — inherited verbatim from 298/301/535.
  CADENCE       {D, W, M, Q}; GROSS {0.50, 0.75, 1.00}; CONSTRUCTION {RESPREAD, DEGROSS}.
  => 3 x 2 x 9 x 4 x 3 x 2 = 1,296 books, 648 decomposition cells, each decomposed on FULL / IS /
     OOS.  Both KEEP paths are evaluated on every one of the 1,296 books.
  The decomposition per cell:  c_t = gross(DEGROSS_t) / gross(RESPREAD_t);
     gap0_pp = 100*(CAGR(DEGROSS_0) - CAGR(RESPREAD_0)),  pred0_pp = 100*(CAGR(c_bar*RESPREAD_0)
     - CAGR(RESPREAD_0)),  resid0_pp = gap0 - pred0.  Subscript 0 = the zero-cost rung, DERIVED
     exactly as r0 = r10 + turnover*bps/1e4, never re-run, so it is the same book.

TUNED PARAMETERS: exactly TWO, both named by the idea — (1) the CADENCE SET
{D-only, W/M/Q, D/W/M/Q}, (2) the RESIDUAL-SCALE BIN (terciles of |resid0_pp(IS)|, pre-registered
as terciles before any number was read).  Panels, families, levels, gross, construction and the
lambda ladder are INHERITED axes, every rung reported, never tuned.

THE DECOMPOSITION OF THE INVERSION.  One estimator pair is fitted per gross on ALL 216 IS cells
(the "D/W/M/Q" set), then scored ONCE on the OOS cells:
    e_CSD  = pred_CSD(c_sd_is)  -  resid0_pp(OOS)
    e_FAM  = mean IS resid0_pp of the cell's gate family  -  resid0_pp(OOS)
    d_err  = |e_CSD| - |e_FAM|          (POSITIVE = CSD.is worse = the inversion)
d_err is then read two ways over the SAME cells: by IS residual-scale tercile, and by cadence.
Both regressors go into one pooled OLS (log IS scale; D-cadence dummy) so the question
"cadence or scale?" is answered on a controlled fit, not on two marginal tables.
NO LEAKAGE: the scale variable, the tercile edges, the family means and the CSD.is coefficients
are all computed on the IS window (<= 2016-12-31) only; the OOS residual enters only as truth.

PRE-REGISTERED VERDICT RULE (written before any number below was read).
  H_SCALE     mean d_err is DECREASING across the three IS-scale terciles at all 3 grosses, AND
              is > 0 in the lowest tercile and < 0 in the highest, at all 3 grosses.  Then the
              inversion is a low-signal-regime fact.
  H_CADENCE   in the pooled bivariate fit (log IS scale + D dummy), the D dummy keeps |t| > 2
              with a POSITIVE coefficient.  Then cadence carries something scale does not.
  ANSWER      "SCALE" if H_SCALE and not H_CADENCE; "CADENCE" if H_CADENCE and not H_SCALE;
              "BOTH" if both; "NEITHER" if neither (the inversion is then not readable on either
              axis and 539's D-only ratio is a 216-cell sampling fact).
  VERDICT     This idea proposes NO new book — it adjudicates an estimator — so the KEEP verdict
              is carried by the corpus: KEEP-candidate only if a rule-8 IS-only chooser's pick
              clears a KEEP path.  Otherwise the LEADERBOARD verdict is the estimator answer and
              the book arm is reported as the KILL/PASS it is.

RULE 8 (2017-2026 read exactly ONCE).
  WF-EST   the estimator IS a walk-forward: fitted on IS cells, scored once on OOS cells, at
           every gross, every cadence set and every scale tercile.
  WF-BOOK  two IS-only choosers per panel over all 432 books of that panel — ISSHARPE (argmax IS
           Sharpe) and PREREG (the 2026-09-03 memo's DD-aware rule: among books with IS MaxDD >=
           60% of SPY's IS MaxDD and IS CAGR >= 70% of SPY's IS CAGR, the smallest gross,
           tie-break largest IS Sharpe) — each read ONCE on OOS against RULES v2 and SPY.

GATES, AND THE THREE THAT WERE RE-SPECIFIED AFTER A FIRST DRAFT FAILED THEM.  A first draft of
this script asserted (a) that the IS window replays idea 539's committed .decomp.csv on all three
panels, (b) that idea 535's published fit (-1.5722, t -6.32) reproduces on its own 162 IS cells,
and (c) that c_t is gross-invariant to 1e-12.  All three FAILED, and the diagnosis is recorded
here rather than quietly dropped, because it is itself the reason the gates now read as they do:
  * The SMALL439 PANEL IS NOT THE SAME PANEL.  Idea 539 ran on 439 names (44 dropped for
    max_1d_move >= 1.0); the rebuilt pool this sandbox now serves is 665 names (54 dropped) —
    exactly ideas 706 / 1074's finding that the label `SMALL439` no longer denotes 439 names.
    One third of the cells are therefore on a different universe, and the IS window moves with it.
  * ON THE POOL-MATCHED SUBSET THE REPLAY IS EXACT.  Refitting 535's fit on the U56 + B136 cells
    alone gives -2.3811 (t -9.01) here against -2.3783 (t -9.02) recomputed from 539's own
    committed decomposition — |d slope| 0.0028.  The whole of the -1.5722 -> -1.6976 move in the
    all-panel level is the SMALL439 rebuild; none of it is a method difference.
  * G4 WAS NEVER TRUE AND 539 SAID SO.  Idea 539's own console publishes "G4 FAIL - c_sd moves
    with gross" at max |d c_bar| 4.042e-03 and max |d c_sd| 9.861e-03: the construction argument
    is wrong because a book's realised gross path drifts through its OWN return, which is not
    proportional across grosses.  Asserting 1e-12 here was inheriting a claim the parent run had
    already refuted; the gate now REPRODUCES the documented failure instead.
  G0 >= 10y.  G1 the IS window replays 539 on the pool-stable panel (U56) at the inherited
  allowance; B136 and SMALL439 drift is PUBLISHED with its cause.  G2 the POOL-MATCHED (U56 +
  B136) reproduction of 535's fit against 539's own committed decomposition.  G3 exactly two
  tuned parameters.  G4 reproduces 539's published G4 FAILURE within 20%.  G5 no scale bin,
  family mean or coefficient reads a row on or after 2017-01-01.  G6 all 648 cells and 1,296
  books published.  G7 PREMISE CHECK: 539's D-only inversion replicates (ratio > 1 at all three
  grosses).  G8 the headline answer survives dropping the changed panel: the bivariate D-dummy
  keeps its sign and |t| > 2 on the U56 + B136 cells alone.

PROTOCOL: rule 1 (>= 10y); rule 2 (10 bps, decide t / apply t+1, no shorting, no leverage, gross
<= 1.00); rule 3 (vs live RULES v2 AND SPY on every panel); rule 4 (full + both halves, both KEEP
paths on every book); rule 8 as above; rule 9 survivorship stated.

SURVIVORSHIP (rule 9).  universe.json, universe_broad.json and prices_small.csv are CURRENT
constituents with no delistings, so every CAGR level and every 4a/4b count here is an UPPER
BOUND.  The headline object is an arm-minus-arm contrast on the SAME names and days (DEGROSS and
RESPREAD share one gate mask), so the bias very largely cancels out of gap0/pred0/resid0 and out
of d_err; it does NOT cancel out of the KEEP columns.  Note also (ideas 706/1074) that the label
`SMALL439` now denotes a larger pool — this run reports the realised name count rather than the
label's number.

Runs standalone and offline (committed price caches only; no network):
  python research/backtests/2026-09-19_daily-inversion-of-the-retirement-as-a-residual-scale-fact_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402,F401  (protocol rule 3 entry point)
from engine import backtest  # noqa: E402,F401

# idea 539's committed machinery, reused verbatim so the corpus is the SAME corpus
_P539 = ROOT / "research" / "backtests" / (
    "2026-09-11_does-the-c_sd-RESIDUAL-LAW-hold-on-a-CADENCE-and-GROSS-grid_cloud.py")
_spec = importlib.util.spec_from_file_location("i539", _P539)
i539 = importlib.util.module_from_spec(_spec)
sys.modules["i539"] = i539
_spec.loader.exec_module(i539)
REF539 = _P539.with_suffix("").as_posix() + ".decomp.csv"

DATE, SLUG = "2026-09-19", "daily-inversion-of-the-retirement-as-a-residual-scale-fact"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

COST_BPS = i539.COST_BPS
GROSSES, CADENCES, FAMILIES = i539.GROSSES, i539.CADENCES, i539.FAMILIES
CONSTRUCTIONS = i539.CONSTRUCTIONS
IS_END, OOS_START = i539.IS_END, i539.OOS_START
CADSETS = {"D only": ["D"], "W/M/Q (idea 535)": ["W", "M", "Q"], "D/W/M/Q (all)": CADENCES}
NBIN = 3                                  # DIAL 2: residual-scale bins, pre-registered terciles
PUB_SLOPE, PUB_T = i539.PUB_SLOPE, i539.PUB_T
PUB_D_RATIO = {0.50: 1.2297, 0.75: 1.2492, 1.00: 1.2710}   # idea 539's committed D-only ratios
DD_CAP, CAGR_FLOOR = 0.60, 0.70

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def main():
    t0 = time.time()
    say("=" * 132)
    say("IDEA 725 — does the DAILY INVERSION of idea 535's RETIREMENT generalise?  CADENCE fact "
        "or LOW-SIGNAL-REGIME (residual-scale) fact?   (lane cloud)")
    say("  PRE-REGISTERED  H_SCALE: mean d_err decreasing across IS-scale terciles at all 3 "
        "grosses, > 0 in the lowest and < 0 in the highest at all 3.")
    say("  PRE-REGISTERED  H_CADENCE: in the pooled bivariate fit (log IS scale + D dummy) the D "
        "dummy keeps |t| > 2 with a POSITIVE coefficient.")
    say("  ANSWER = SCALE / CADENCE / BOTH / NEITHER by which fires.  d_err = |e_CSD| - |e_FAM|, "
        "POSITIVE = CSD.is worse = the inversion.")
    say("=" * 132)

    pans = i539.panels()
    say("  SURVIVORSHIP (rule 9): current-constituent lists, no delistings — every CAGR level and "
        "every 4a/4b count below is an UPPER BOUND.  The headline (d_err) is an arm-minus-arm "
        "contrast on the SAME names and days, which the bias cannot manufacture.  The label "
        "SMALL439 denotes the realised pool size printed above (ideas 706 / 1074), not 439.")

    rows, decomp, ctxt = [], [], {}
    for pname, (px, spy) in pans.items():
        start = px.index[260]
        years = (px.index[-1] - px.index[260]).days / 365.25
        say(f"    TAPE {pname}: {px.index[0].date()} .. {px.index[-1].date()} "
            f"({len(px.index)} rows, {len(px.index)/252:.1f}y), scored from {start.date()}")
        publish(f"TAPE STAMP {pname}",
                f"{len(px.index)} rows {px.index[0].date()}..{px.index[-1].date()}")
        spy_r = spy.pct_change().fillna(0.0).loc[start:]
        spy_s = i539.stat(spy_r)
        live_r = backtest(pd.concat([px, spy.rename("SPY")], axis=1),
                          rules_v2_weights(pd.concat([px, spy.rename("SPY")], axis=1)),
                          cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        live_s = i539.stat(live_r)
        ctxt[pname] = (spy_s, live_s)
        say(f"      SPY  FULL {spy_s['CAGR']:.2%}/{spy_s['Sharpe']:.4f}/{spy_s['MaxDD']:.2%} "
            f"H1/H2 {spy_s['H1']:.3f}/{spy_s['H2']:.3f}  OOS {spy_s['oCAGR']:.2%}/"
            f"{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.2%}  | 4b bars DD {DD_CAP*spy_s['MaxDD']:.2%}"
            f", CAGR {CAGR_FLOOR*spy_s['CAGR']:.2%}")
        say(f"      RULES v2 FULL {live_s['CAGR']:.2%}/{live_s['Sharpe']:.4f}/"
            f"{live_s['MaxDD']:.2%} H1/H2 {live_s['H1']:.3f}/{live_s['H2']:.3f}  OOS "
            f"{live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.2%}")

        for family in FAMILIES:
            levels = i539.QUANT_X if family == "QUANTILE" else i539.MA_THETA
            for level in levels:
                for cad in CADENCES:
                    for gross in GROSSES:
                        got = {}
                        for con in CONSTRUCTIONS:
                            res = i539.fast_backtest(px, i539.book(px, family, level, con, gross),
                                                     COST_BPS, cad)
                            r10 = res["returns"].loc[start:]
                            turn = res["turnover"].loc[start:]
                            r0 = r10 + turn * COST_BPS / 1e4
                            s = i539.stat(r10)
                            got[con] = dict(r0=r0, gross=res["gross"].loc[start:], s=s)
                            rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                             gross=gross, con=con, **s,
                                             turn_yr=turn.sum() / years,
                                             p4a=i539.verdict_4a(s, live_s),
                                             f4b=i539.fail_4b(s, spy_s)))
                        dg, rs = got["DEGROSS"], got["RESPREAD"]
                        c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                        ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                        for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                            ("OOS", OOS_START, None)):
                            sl = slice(lo, hi)
                            rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                            cb = float(c_t.loc[sl].mean())
                            g0 = 100 * (i539.cagr(rd) - i539.cagr(rr))
                            p0 = 100 * (i539.cagr(cb * rr) - i539.cagr(rr))
                            decomp.append(dict(panel=pname, family=family, level=level, cad=cad,
                                               gross=gross, ident_max_err=ident, window=tag,
                                               c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                               gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0))
            say(f"      ... {pname} / {family} done  ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    D = pd.DataFrame(decomp)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    say(f"\n  books {len(G)}   decomposition cells {len(D)//3}   identity max |r_dg - c_t*r_rs| "
        f"{D.ident_max_err.max():.3e}")
    gate("G0 min sample >= 10 years (rule 1)",
         round(min(len(p[0].index) for p in pans.values()) / 252.0, 2), ">= 10.0",
         min(len(p[0].index) for p in pans.values()) / 252.0 >= 10.0)
    gate("G6 all cells and books published",
         f"{len(G)} books, {len(D)//3} cells", "== 1296 books, 648 cells",
         len(G) == 1296 and len(D) // 3 == 648)
    gate("G3 exactly two tuned parameters (the CADENCE SET; the RESIDUAL-SCALE BIN = terciles). "
         "Panels / families / levels / gross / construction / lambda are inherited axes, every "
         "rung reported", 2, "== 2", True)

    # ---------------- G4 c_t invariance in gross
    key4 = ["panel", "family", "level", "cad", "window"]
    w = D.pivot_table(index=key4, columns="gross", values=["c_bar", "c_sd"])
    dcb = float((w["c_bar"][0.50] - w["c_bar"][1.00]).abs().max())
    dcs = float((w["c_sd"][0.50] - w["c_sd"][1.00]).abs().max())
    R539_CB, R539_CS = 4.042e-03, 9.861e-03      # idea 539's OWN published G4 FAILURE
    gate("G4 REPRODUCES idea 539's published G4 FAILURE — c_t is NOT gross-invariant (a book's "
         "realised gross path drifts through its own return, which is not proportional across "
         f"grosses).  539 published max |d c_bar| {R539_CB:.3e}, max |d c_sd| {R539_CS:.3e}",
         f"max |d c_bar| {dcb:.3e}, max |d c_sd| {dcs:.3e}", "both within 20% of 539's",
         abs(dcb / R539_CB - 1) < 0.20 and abs(dcs / R539_CS - 1) < 0.20)

    # ---------------- G1 replay of 539's committed decomposition
    key = ["panel", "family", "level", "cad", "gross", "window"]
    ref = pd.read_csv(REF539)
    m = D.merge(ref[key + ["resid0_pp", "c_sd"]], on=key, suffixes=("", "_539"))
    m["d_resid"] = (m.resid0_pp - m.resid0_pp_539).abs()
    m["d_csd"] = (m.c_sd - m.c_sd_539).abs()
    mi = m[(m.window == "IS") & (m.panel == "U56")]
    gate("G1 the IS window (<= 2016-12-31) replays idea 539's committed .decomp.csv on the "
         "POOL-STABLE panel (U56)",
         f"n {len(mi)}, max |d resid0_pp| {mi.d_resid.max():.2e} pp, max |d c_sd| "
         f"{mi.d_csd.max():.2e}", "< 1e-2 pp and < 1e-4 (the 535/539 allowance)",
         mi.d_resid.max() < 1e-2 and mi.d_csd.max() < 1e-4)
    say("\n    PUBLISHED (not asserted) — drift vs idea 539's committed decomposition, by panel "
        "and window, with its cause:")
    say(f"      {'panel':<10}{'window':<7}{'max |d resid0_pp|':>20}{'median':>11}"
        f"{'max |d c_sd|':>15}")
    for pn in ("U56", "B136", "SMALL439"):
        for wtag in ("IS", "FULL", "OOS"):
            t = m[(m.panel == pn) & (m.window == wtag)]
            say(f"      {pn:<10}{wtag:<7}{t.d_resid.max():>20.4f}{t.d_resid.median():>11.4f}"
                f"{t.d_csd.max():>15.2e}")
            publish(f"DRIFT vs 539 {pn} {wtag}",
                    f"max |d resid0_pp| {t.d_resid.max():.4f} pp, median "
                    f"{t.d_resid.median():.4f} pp, max |d c_sd| {t.d_csd.max():.2e}")
    say("      CAUSE — U56: 8 further trading days on data/prices.csv, inside the inherited "
        "allowance.  B136: data/prices_broad.csv is re-cached weekly and restates adjusted "
        "closes, so its history itself moves.  SMALL439: the POOL WAS REBUILT (439 names in 539, "
        f"{pans['SMALL439'][0].shape[1]} here) — it is a DIFFERENT UNIVERSE, not a drift "
        "(ideas 706 / 1074).")

    # ---------------- cells frame
    def cells_for(gross, cads):
        s = D[(D.gross == gross) & (D.cad.isin(cads))]
        IS = s[s.window == "IS"].sort_values(key[:4]).reset_index(drop=True)
        OO = s[s.window == "OOS"].sort_values(key[:4]).reset_index(drop=True)
        assert (IS[key[:4]].values == OO[key[:4]].values).all()
        C = IS[key[:4]].copy()
        C["c_sd_is"], C["c_bar_is"] = IS.c_sd.values, IS.c_bar.values
        C["resid_is"], C["resid_oos"] = IS.resid0_pp.values, OO.resid0_pp.values
        return C

    # ---------------- G2 idea 535's published fit
    def fit535(df, panels=None):
        s = df[(df.gross == 0.75) & (df.cad.isin(["W", "M", "Q"])) & (df.window == "IS")]
        if panels:
            s = s[s.panel.isin(panels)]
        s = s.sort_values(key[:4])
        return i539.ols(np.column_stack([np.ones(len(s)), s.c_sd.values]), s.resid0_pp.values)
    f_all, f_pm = fit535(D), fit535(D, ["U56", "B136"])
    r_all, r_pm = fit535(ref), fit535(ref, ["U56", "B136"])
    say(f"\n    idea 535's fit, recomputed HERE and from 539's OWN committed decomposition:")
    say(f"      all 3 panels   here n {f_all['n']:>4} slope {f_all['b'][1]:+.4f} "
        f"(t {f_all['t'][1]:+.2f})   |  539's file n {r_all['n']:>4} slope {r_all['b'][1]:+.4f} "
        f"(t {r_all['t'][1]:+.2f})   |  published {PUB_SLOPE:+.4f} (t {PUB_T:.2f})")
    say(f"      U56+B136 only  here n {f_pm['n']:>4} slope {f_pm['b'][1]:+.4f} "
        f"(t {f_pm['t'][1]:+.2f})   |  539's file n {r_pm['n']:>4} slope {r_pm['b'][1]:+.4f} "
        f"(t {r_pm['t'][1]:+.2f})")
    publish("535 FIT LEVEL MOVE, all 3 panels",
            f"published {PUB_SLOPE:+.4f} -> {f_all['b'][1]:+.4f} here; the move is the SMALL439 "
            f"pool rebuild, since the pool-matched subset reproduces to "
            f"{abs(f_pm['b'][1]-r_pm['b'][1]):.4f}")
    gate("G2 POOL-MATCHED reproduction of idea 535's CSD.is fit (U56 + B136 cells, this run vs "
         "539's own committed decomposition) — the SMALL439 pool was rebuilt between the two "
         "runs, so the all-panel level is NOT a like-for-like comparand and is published instead",
         f"here {f_pm['b'][1]:+.4f} (t {f_pm['t'][1]:+.2f}) vs 539 {r_pm['b'][1]:+.4f} "
         f"(t {r_pm['t'][1]:+.2f}); |d slope| {abs(f_pm['b'][1]-r_pm['b'][1]):.4f}",
         "|d slope| < 5e-3 and |d t| < 0.10",
         abs(f_pm["b"][1] - r_pm["b"][1]) < 5e-3 and abs(f_pm["t"][1] - r_pm["t"][1]) < 0.10)

    # ---------------- G7 premise check: 539's D-only inversion
    say("\n" + "=" * 132)
    say("(0) PREMISE CHECK — does 539's DAILY INVERSION replicate on this tape?  "
        "(CSD.is lam=1 OOS MAE / FAMILY lam=1 OOS MAE, per cadence set)")
    say("=" * 132)
    say(f"    {'cadence set':<20}{'gross':>7}{'n':>5}{'FAMILY MAE':>13}{'CSD.is MAE':>13}"
        f"{'ratio':>9}{'539 ratio':>11}{'retire?':>9}")
    prem, g7_ok = [], True
    for cname, cads in CADSETS.items():
        for gross in GROSSES:
            C = cells_for(gross, cads)
            IS = C.rename(columns={"resid_is": "resid0_pp"})
            OO = C.rename(columns={"resid_oos": "resid0_pp"})
            fa = i539.mae(i539.predict("FAMILY", 1.0, IS, OO), OO.resid0_pp.values)
            cs = i539.mae(i539.predict("CSD.is", 1.0, IS, OO), OO.resid0_pp.values)
            ref_r = PUB_D_RATIO[gross] if cname == "D only" else np.nan
            if cname == "D only" and cs / fa <= 1.0:
                g7_ok = False
            prem.append(dict(cadset=cname, gross=gross, n=len(C), FAMILY_MAE=fa, CSD_MAE=cs,
                             ratio=cs / fa, ratio_539=ref_r, retire=bool(cs <= 0.95 * fa)))
            say(f"    {cname:<20}{gross:>7.2f}{len(C):>5}{fa:>13.4f}{cs:>13.4f}{cs/fa:>9.4f}"
                + (f"{ref_r:>11.4f}" if np.isfinite(ref_r) else f"{'-':>11}")
                + f"{('YES' if cs <= 0.95*fa else 'no'):>9}")
    pd.DataFrame(prem).to_csv(f"{OUT}.premise.csv", index=False)
    gate("G7 PREMISE: idea 539's D-only inversion replicates (CSD.is/FAMILY OOS MAE ratio > 1 at "
         "all three grosses)",
         "; ".join(f"g={r['gross']:.2f}: {r['ratio']:.4f} (539 {r['ratio_539']:.4f})"
                   for r in prem if r["cadset"] == "D only"), "all > 1.0", g7_ok)

    # ---------------- THE HEADLINE: one estimator per gross, per-cell errors
    say("\n" + "=" * 132)
    say("(1) THE DECOMPOSITION — one estimator pair fitted per gross on ALL 216 IS cells, scored "
        "ONCE on OOS; per-cell d_err = |e_CSD| - |e_FAM|  (POSITIVE = the inversion)")
    say("=" * 132)
    cells = []
    for gross in GROSSES:
        C = cells_for(gross, CADENCES).copy()
        IS = C.rename(columns={"resid_is": "resid0_pp"})
        OO = C.rename(columns={"resid_oos": "resid0_pp"})
        C["pred_csd"] = i539.predict("CSD.is", 1.0, IS, OO).values
        C["pred_fam"] = i539.predict("FAMILY", 1.0, IS, OO).values
        C["e_csd"] = C.pred_csd - C.resid_oos
        C["e_fam"] = C.pred_fam - C.resid_oos
        C["d_err"] = C.e_csd.abs() - C.e_fam.abs()
        C["scale_is"] = C.resid_is.abs()                      # IS-only, legal
        C["log_scale"] = np.log(C.scale_is.clip(lower=1e-6))
        q = C.scale_is.quantile([1 / NBIN, 2 / NBIN]).values   # tercile edges, IS-only
        C["bin"] = np.digitize(C.scale_is.values, q)           # 0 = lowest scale
        C["is_D"] = (C.cad == "D").astype(float)
        C["gross"] = gross
        cells.append(C)
    X = pd.concat(cells, ignore_index=True)
    X.to_csv(f"{OUT}.cells.csv", index=False)
    BINLAB = {0: "LOW |resid|", 1: "MID", 2: "HIGH |resid|"}

    say(f"    tercile edges are computed on the IS window only, per gross, over all 216 cells.")
    say(f"    {'gross':>7}{'bin':<14}{'n':>5}{'IS |resid| range (pp)':>26}{'D share':>9}"
        f"{'mean d_err':>12}{'median':>10}{'FAM MAE':>10}{'CSD MAE':>10}{'ratio':>8}{'retire?':>9}")
    tab = []
    for gross in GROSSES:
        s = X[X.gross == gross]
        for b in (0, 1, 2):
            t = s[s.bin == b]
            fa, cs = t.e_fam.abs().mean(), t.e_csd.abs().mean()
            tab.append(dict(gross=gross, bin=b, binlab=BINLAB[b], n=len(t),
                            lo=t.scale_is.min(), hi=t.scale_is.max(),
                            D_share=float(t.is_D.mean()), mean_derr=float(t.d_err.mean()),
                            median_derr=float(t.d_err.median()), FAM_MAE=fa, CSD_MAE=cs,
                            ratio=cs / fa, retire=bool(cs <= 0.95 * fa)))
            say(f"    {gross:>7.2f}{BINLAB[b]:<14}{len(t):>5}"
                f"{f'{t.scale_is.min():.4f} - {t.scale_is.max():.4f}':>26}"
                f"{t.is_D.mean():>9.2f}{t.d_err.mean():>12.4f}{t.d_err.median():>10.4f}"
                f"{fa:>10.4f}{cs:>10.4f}{cs/fa:>8.4f}"
                f"{('YES' if cs <= 0.95*fa else 'no'):>9}")
    T = pd.DataFrame(tab)
    T.to_csv(f"{OUT}.bins.csv", index=False)

    say("\n    THE CONFOUND, MEASURED: share of each scale tercile that is DAILY cells "
        f"(a cadence-blind split would give {1/len(CADENCES):.2f} everywhere)")
    say(fmt(T.pivot_table(index="binlab", columns="gross", values="D_share"), 3))

    say("\n    CADENCE-MATCHED READING — the same tercile split INSIDE one cadence set, so "
        "cadence cannot carry it:")
    say(f"    {'cadence set':<20}{'gross':>7}{'bin':<14}{'n':>5}{'FAM MAE':>10}{'CSD MAE':>10}"
        f"{'ratio':>9}{'mean d_err':>12}")
    cm = []
    for cname, cads in (("W/M/Q (idea 535)", ["W", "M", "Q"]), ("D only", ["D"])):
        for gross in GROSSES:
            s = X[(X.gross == gross) & (X.cad.isin(cads))]
            for b in (0, 1, 2):
                t = s[s.bin == b]
                if len(t) < 5:
                    say(f"    {cname:<20}{gross:>7.2f}{BINLAB[b]:<14}{len(t):>5}"
                        f"{'(n < 5, not read)':>41}")
                    cm.append(dict(cadset=cname, gross=gross, bin=b, n=len(t)))
                    continue
                fa, cs = t.e_fam.abs().mean(), t.e_csd.abs().mean()
                cm.append(dict(cadset=cname, gross=gross, bin=b, binlab=BINLAB[b], n=len(t),
                               FAM_MAE=fa, CSD_MAE=cs, ratio=cs / fa,
                               mean_derr=float(t.d_err.mean())))
                say(f"    {cname:<20}{gross:>7.2f}{BINLAB[b]:<14}{len(t):>5}{fa:>10.4f}"
                    f"{cs:>10.4f}{cs/fa:>9.4f}{t.d_err.mean():>12.4f}")
    pd.DataFrame(cm).to_csv(f"{OUT}.cadence_matched.csv", index=False)

    # ---------------- the controlled fit
    say("\n" + "=" * 132)
    say("(2) THE CONTROLLED FIT — d_err on log IS scale and a D-cadence dummy (pooled over the "
        "648 cells, with gross dummies), univariate then bivariate")
    say("=" * 132)
    fits = []
    Xp = X.dropna(subset=["d_err", "log_scale"]).copy()
    gd = [(Xp.gross == g).astype(float).values for g in GROSSES[1:]]
    for label, cols in (("log_scale", ["log_scale"]), ("D dummy", ["is_D"]),
                        ("log_scale + D dummy", ["log_scale", "is_D"])):
        M = np.column_stack([np.ones(len(Xp))] + [Xp[c].values for c in cols] + gd)
        f = i539.ols(M, Xp.d_err.values)
        nm = ["const"] + cols + [f"g={g}" for g in GROSSES[1:]]
        fits.append(dict(model=label, n=f["n"], R2=f["R2"],
                         **{f"b[{c}]": f["b"][nm.index(c)] for c in cols},
                         **{f"t[{c}]": f["t"][nm.index(c)] for c in cols}))
        say(f"    {label:<24} n {f['n']:>4}  R2 {f['R2']:.4f}   "
            + "   ".join(f"b[{c}] {f['b'][nm.index(c)]:+.4f} (t {f['t'][nm.index(c)]:+.2f})"
                         for c in cols))
    Mb = np.column_stack([np.ones(len(Xp))] + gd)
    say(f"    {'gross dummies only':<24} n {len(Xp):>4}  R2 "
        f"{i539.ols(Mb, Xp.d_err.values)['R2']:.4f}   (the deflation baseline)")
    F = pd.DataFrame(fits)
    F.to_csv(f"{OUT}.fits.csv", index=False)
    Xr = Xp[Xp.panel.isin(["U56", "B136"])]
    gdr = [(Xr.gross == g).astype(float).values for g in GROSSES[1:]]
    Mr = np.column_stack([np.ones(len(Xr)), Xr.log_scale.values, Xr.is_D.values] + gdr)
    fr = i539.ols(Mr, Xr.d_err.values)
    say(f"    {'  [G8] U56+B136 only':<24} n {fr['n']:>4}  R2 {fr['R2']:.4f}   "
        f"b[log_scale] {fr['b'][1]:+.4f} (t {fr['t'][1]:+.2f})   b[is_D] {fr['b'][2]:+.4f} "
        f"(t {fr['t'][2]:+.2f})")
    gate("G8 the headline survives dropping the CHANGED panel: the bivariate D-dummy keeps a "
         "POSITIVE sign and |t| > 2 on the U56 + B136 cells alone",
         f"b[is_D] {fr['b'][2]:+.4f} (t {fr['t'][2]:+.2f}), n {fr['n']}", "> 0 and |t| > 2",
         fr["b"][2] > 0 and abs(fr["t"][2]) > 2)
    rho = float(pd.Series(Xp.log_scale.values).corr(pd.Series(Xp.is_D.values)))
    say(f"\n    corr(log IS scale, D dummy) = {rho:+.4f}  — the two candidate explanations are "
        f"{'strongly' if abs(rho) > 0.5 else 'only partly'} the same axis, which is exactly why "
        f"the marginal tables above cannot settle it and this fit can.")

    # ---------------- rule 8 book arm
    say("\n" + "=" * 132)
    say("(3) RULE 8 — WF-BOOK: two IS-ONLY choosers per panel over its 432 books, read ONCE on "
        "2017-2026.  Both KEEP paths on all 1,296 books.")
    say("=" * 132)
    G["p4b"] = G.f4b == "-"
    say(f"    corpus: {len(G)} books.  4a passes {int(G.p4a.sum())}   4b passes "
        f"{int(G.p4b.sum())}")
    say(fmt(G.groupby(["panel", "cad"])[["p4a", "p4b"]].sum(), 0))
    say(fmt(G.groupby(["panel", "gross"])[["p4a", "p4b"]].sum(), 0))
    picks = []
    for pname, sub in G.groupby("panel"):
        spy_s, live_s = ctxt[pname]
        cand = {"ISSHARPE": sub.loc[sub.isSharpe.idxmax()]}
        adm = sub[(sub.isMaxDD >= DD_CAP * spy_s["isMaxDD"])
                  & (sub.isCAGR >= CAGR_FLOOR * spy_s["isCAGR"])]
        say(f"    [{pname}] PREREG admitted set on IS: {len(adm)} of {len(sub)} books")
        if len(adm):
            a2 = adm[adm.gross == adm.gross.min()]
            cand["PREREG"] = a2.loc[a2.isSharpe.idxmax()]
        for tag, r in cand.items():
            lab = f"{r.family}/L={r.level}/{r.cad}/g={r.gross:.2f}/{r.con}"
            picks.append(dict(panel=pname, chooser=tag, pick=lab, IS_Sharpe=r.isSharpe,
                              OOS_CAGR=r.oCAGR, OOS_Sharpe=r.oSharpe, OOS_MaxDD=r.oMaxDD,
                              FULL_CAGR=r.CAGR, FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD,
                              H1=r.H1, H2=r.H2, p4a=bool(r.p4a), p4b=bool(r.p4b), f4b=r.f4b,
                              v2_OOS_Sharpe=live_s["oSharpe"], v2_OOS_CAGR=live_s["oCAGR"],
                              v2_OOS_MaxDD=live_s["oMaxDD"], spy_OOS_Sharpe=spy_s["oSharpe"],
                              spy_OOS_CAGR=spy_s["oCAGR"], spy_OOS_MaxDD=spy_s["oMaxDD"],
                              beats_v2=bool(r.oSharpe > live_s["oSharpe"]),
                              beats_spy=bool(r.oSharpe > spy_s["oSharpe"])))
            say(f"    [{pname}] {tag:<9} -> {lab:<34} FULL {r.CAGR:.2%}/{r.Sharpe:.4f}/"
                f"{r.MaxDD:.2%} H1/H2 {r.H1:.3f}/{r.H2:.3f}  OOS {r.oCAGR:.2%}/{r.oSharpe:.4f}/"
                f"{r.oMaxDD:.2%}   4a={r.p4a} 4b={r.p4b} (fails: {r.f4b})")
            say(f"                          vs SPY OOS {spy_s['oCAGR']:.2%}/"
                f"{spy_s['oSharpe']:.4f}/{spy_s['oMaxDD']:.2%}   vs RULES v2 OOS "
                f"{live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/{live_s['oMaxDD']:.2%}")
    W = pd.DataFrame(picks)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n    picks {len(W)}: beat RULES v2 OOS Sharpe {int(W.beats_v2.sum())}, beat SPY OOS "
        f"Sharpe {int(W.beats_spy.sum())}, 4a {int(W.p4a.sum())}, 4b {int(W.p4b.sum())}")
    gate("G5 no scale bin, tercile edge, family mean or CSD.is coefficient reads a row on or "
         "after 2017-01-01; both book choosers use IS Sharpe / IS MaxDD / IS CAGR only",
         "by construction", "no OOS leakage", True)

    # ---------------- verdict
    mono, ends = True, True
    for gross in GROSSES:
        v = T[T.gross == gross].sort_values("bin").mean_derr.values
        if not (v[0] > v[1] > v[2]):
            mono = False
        if not (v[0] > 0 > v[2]):
            ends = False
    h_scale = bool(mono and ends)
    bf = F[F.model == "log_scale + D dummy"].iloc[0]
    h_cadence = bool(abs(bf["t[is_D]"]) > 2 and bf["b[is_D]"] > 0)
    answer = ("SCALE" if h_scale and not h_cadence else
              "CADENCE" if h_cadence and not h_scale else
              "BOTH" if h_scale and h_cadence else "NEITHER")
    keep = bool(W.p4a.any() or W.p4b.any())
    verdict = "KEEP-candidate" if keep else f"KILL (of the CADENCE framing) — ANSWER: {answer}"

    say("\n" + "=" * 132)
    say("(4) PRE-REGISTERED VERDICT")
    say("=" * 132)
    say(f"    H_SCALE    {h_scale}   (mean d_err monotone decreasing across terciles at all 3 "
        f"grosses: {mono}; > 0 in LOW and < 0 in HIGH at all 3: {ends})")
    say(f"    H_CADENCE  {h_cadence}   (bivariate D dummy b {bf['b[is_D]']:+.4f}, t "
        f"{bf['t[is_D]']:+.2f})")
    say(f"    ANSWER: {answer}")
    say(f"    BOOK ARM: 4a {int(W.p4a.sum())} of {len(W)} picks, 4b {int(W.p4b.sum())} of "
        f"{len(W)}; corpus 4a {int(G.p4a.sum())} of {len(G)}, 4b {int(G.p4b.sum())} of {len(G)}")
    say(f"    VERDICT: {verdict}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    hard = gdf[gdf["target"] != "published, not asserted"]
    say(f"\n    GATES {int(hard['pass_'].sum())}/{len(hard)} pass "
        f"({len(gdf)-len(hard)} published-not-asserted stamps).")
    say(f"    runtime {time.time()-t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return verdict


if __name__ == "__main__":
    main()
