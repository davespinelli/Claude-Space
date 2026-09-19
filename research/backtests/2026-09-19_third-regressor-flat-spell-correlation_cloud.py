#!/usr/bin/env python3
"""IDEA 1558 (lane cloud, 2026-09-19) — is the THIRD REGRESSOR the CORRELATION of the FLAT SPELLS
and not their COUNT?

WHY.  Idea 1538 fitted the blend gap `D_sharpe` of 81 adjacent-rung pairs on TWO numbers --
(1 - overlap) and `flat_one`, the share of days on which exactly one of the two rungs is flat --
and got a pooled R^2 of 0.5460 (OV_HOLD) / 0.5435 (OV_CAP), short of its own 0.80 bar, while T4
(leave-one-ladder-out) mis-priced the BREADTH ladder at R^2 -32.22 and priced the SPY MACRO ladder
at +0.7652 on nearly identical flat_one (0.0875 vs 0.0916 on U56).  1558's hypothesis: the two
ladders differ not in HOW OFTEN the rungs are flat apart but in WHEN.  Add exactly ONE third
regressor describing the TIMING of the flat spells and re-run 1538's exact T1 / T4 / T5.

THE TWO TUNED PARAMETERS (rule 4, "no more than 2"), every grid point published:
  DIAL 1  third regressor   {R3_CORR_ANCH, R3_CORR_OWN, R3_LEN}
      R3_CORR_ANCH = corr(flat_one indicator_t, the FROZEN INCUMBENT's own net return_t).  The
                     incumbent is the selection frame every rung on every ladder shares, so this
                     is a clean "when do the two rungs disagree about being invested" measure and
                     carries no mechanical zero-return artefact.
      R3_CORR_OWN  = corr(flat_one indicator_t, the pair's own mean GROSS return_t).  The literal
                     reading of the queue text ("the rung's own return"); it DOES carry the
                     mechanical artefact (a flat rung returns exactly 0), which is why both are
                     built and both published.
      R3_LEN       = mean length in trading days of a maximal run of consecutive flat_one days
                     (0.0 when the pair never disagrees).  The queue's own alternative.
  DIAL 2  bootstrap block length L {32, 63, 126} for every paired SE in this file.

NOT TUNED, frozen at idea 1538's published values: lambda = 0.50 (1538's pooled fit), the nine
ladders and their rungs, the frozen 2026-09-04 incumbent (N=20, H=126, gross 0.75, MAXVOL 0.60,
200d MA gate, weekly Fri-decide/Mon-trade), 10 bps, t+1.  The overlap statistic is reported BOTH
ways (OV_HOLD and OV_CAP) exactly as 1538 reported it, not chosen.

PRE-REGISTERED BARS (1538's, unchanged, so the two runs are comparable):
  T1  pooled three-number R^2 >= 0.80
  T2  dR^2 from adding ladder identity < 0.05
  T3  no ladder residual |t| > 2
  T4  leave-one-ladder-out R^2 >= 0.50 on EACH of the three flat-bearing ladders
  T5  rule-8 transfer: fit on 2009-2016 pair statistics ONLY, predict 2017-2026 D_sharpe,
      R^2 >= 0.80
A rule that clears T1 AND T4 is the prediction rule 1558 was filed for.  Anything less is a KILL
of the three-number hypothesis, reported as such.

CAPITAL ARM (protocol step 3).  Every one of the 189 cells (63 per panel: 36 rungs + 27 blends)
is scored on BOTH KEEP paths against the live RULES v2 baseline AND SPY, full sample and halves,
and the rule-8 walk-forward chooser is fitted on warm-up..2016-12-31 ONLY with 2017-2026 read
once.

Offline, deterministic, no network.  Reuses idea 1538's committed builders by import so the 81
pairs are literally the same 81 pairs.

  python research/backtests/2026-09-19_third-regressor-flat-spell-correlation_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

_SRC = HERE / "2026-09-19_exposure-state-disagreement-third-ladder-axis_C.py"
_spec = importlib.util.spec_from_file_location("idea1538", _SRC)
M = importlib.util.module_from_spec(_spec)
sys.modules["idea1538"] = M
_spec.loader.exec_module(M)                      # module-level only; main() is guarded

from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest  # noqa: E402

DATE, SLUG = "2026-09-19", "third-regressor-flat-spell-correlation"
OUT = HERE / f"{DATE}_{SLUG}_cloud"

WARMUP, COST = M.WARMUP, M.COST
OOS_START, IS_END = M.OOS_START, M.IS_END
LADDERS, FLAT_LADDERS = M.LADDERS, M.FLAT_LADDERS
LAM = 0.50
R3S = ["R3_CORR_ANCH", "R3_CORR_OWN", "R3_LEN"]
BLOCKS = [32, 63, 126]
OVSTATS = ["OV_HOLD", "OV_CAP"]
R2_BAR, DR2_BAR, T_BAR, LOLO_BAR, OOS_R2_BAR = M.R2_BAR, M.DR2_BAR, M.T_BAR, M.LOLO_BAR, M.OOS_R2_BAR
C_1538 = dict(R2_HOLD=0.5460, R2_CAP=0.5435, DR2_HOLD=0.0238, LOLO_L_R=-32.22, LOLO_L_M=0.7652)

LOG: list[str] = []
GATES: list[dict] = []
sharpe, cagr, mdd = M.sharpe, M.cagr, M.mdd
triple, halves, bmpack, keep_paths = M.triple, M.halves, M.bmpack, M.keep_paths
ols, r2_against = M.ols, M.r2_against
build_rung, rung_spec, is_anchor, blend, overlaps = (M.build_rung, M.rung_spec, M.is_anchor,
                                                     M.blend, M.overlaps)


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


def pboot(a, b, L, reps=400, seed=20260919):
    return M.paired_block_dsharpe(a, b, reps=reps, L=L, seed=seed)


# ---------------------------------------------------------------------------------------------
# the THIRD REGRESSOR
# ---------------------------------------------------------------------------------------------
def _corr(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 5 or x.std() <= 1e-12 or y.std() <= 1e-12:
        return 0.0                                   # degenerate pair -> no timing information
    return float(np.corrcoef(x, y)[0, 1])


def _mean_run(x):
    """Mean length of a maximal run of consecutive TRUE in a boolean vector (0.0 if none)."""
    x = np.asarray(x, bool)
    if not x.any():
        return 0.0
    d = np.diff(np.concatenate([[0], x.view(np.int8), [0]]))
    starts, ends = np.flatnonzero(d == 1), np.flatnonzero(d == -1)
    return float((ends - starts).mean())


def third_regressors(flatA, flatB, anch_r, own_r, s, e):
    """All three DIAL-1 settings for one pair over the window [s:e)."""
    x = (flatA[s:e] ^ flatB[s:e])
    xf = x.astype(float)
    return dict(flat_one=float(xf.mean()),
                R3_CORR_ANCH=_corr(xf, anch_r[s:e]),
                R3_CORR_OWN=_corr(xf, own_r[s:e]),
                R3_LEN=_mean_run(x),
                n_spell=int(np.diff(np.concatenate([[0], x.view(np.int8), [0]])).clip(min=0).sum()))


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 124)
    say("IDEA 1558 (lane cloud, 2026-09-19) — is the THIRD REGRESSOR the CORRELATION of the FLAT "
        "SPELLS and not their COUNT?")
    say("9 ladders x 4 rungs = 36 rungs + 27 adjacent pairs at lambda = 0.50 = 63 cells per panel, "
        "189 in all, every one published.  81 pairs (27 x 3 panels) — idea 1538's own 81.")
    say(f"DIAL 1 third regressor {R3S};  DIAL 2 bootstrap block length {BLOCKS}.  "
        f"lambda frozen at {LAM} (1538's pooled fit), overlap statistic reported BOTH ways.")
    say(f"PRE-REGISTERED (1538's bars, unchanged): T1 R^2>={R2_BAR}; T2 dR^2<{DR2_BAR}; "
        f"T3 no ladder |t|>{T_BAR}; T4 leave-one-ladder-out R^2>={LOLO_BAR} on each flat ladder; "
        f"T5 rule-8 OOS R^2>={OOS_R2_BAR}.")
    say("=" * 124)

    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    md = pd.read_csv(ROOT / "data" / "small_meta.csv")
    col = "ticker" if "ticker" in md.columns else md.columns[0]
    bad = set(md.loc[md["max_1d_move"] >= 1.0, col].astype(str))
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad and mv[c] < 1.0]
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {len(bad)} tickers with "
        f"max_1d_move >= 1.0; {len(inv)} investable names survive.")

    panels = [M.Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              M.Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              M.Panel("SMALL", pxS, inv)]
    say(f"  PANELS: U56 {len(pxU.columns)-1} names, B136 {len(pxB.columns)-1}, SMALL {len(inv)}.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL a CURRENT "
        "sub-$2B screen carried back to 2010, so every ABSOLUTE level below is an UPPER BOUND.  "
        "What this run reads is a CONTRAST between books over the SAME names on the SAME days.")
    for p in panels:
        say(f"    TAPE {p.name}: {p.idx[0].date()} .. {p.idx[-1].date()}  {len(p.idx)} rows "
            f"({len(p.idx)/252:.1f}y)")
        publish(f"TAPE STAMP {p.name}", f"{len(p.idx)} rows {p.idx[0].date()}..{p.idx[-1].date()}")
    gate("G0 min sample >= 10 years (rule 1)", round(min(len(p.idx) for p in panels) / 252.0, 2),
         ">= 10.0", min(len(p.idx) for p in panels) / 252.0 >= 10.0)
    gate("G4 exactly two tuned parameters (third regressor, bootstrap block length)", 2, "== 2",
         True)

    grid, pairs, wf_rows = [], [], []
    anchor_dev, g9_dev, g10_dev = 0.0, 0.0, 0.0
    g1_ok = None

    for pan in panels:
        T = len(pan.idx)
        i_oos = int(np.searchsorted(pan.idx.values, np.datetime64(OOS_START)))
        i_is = int(np.searchsorted(pan.idx.values, np.datetime64(IS_END)))
        spy, spyO = bmpack(pan.spy[WARMUP:]), bmpack(pan.spy[i_oos:])
        lr = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        live, liveO = bmpack(lr[WARMUP:]), bmpack(lr[i_oos:])

        say(f"\n  [{pan.name}]  SPY CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.4f} MaxDD "
            f"{spy['MaxDD']:.2%} H1/H2 {spy['H1']:.3f}/{spy['H2']:.3f}  |  4b bars: DD cap "
            f"{M.DD_CAP*spy['MaxDD']:.2%}, CAGR floor {M.CAGR_FLOOR*spy['CAGR']:.2%}")
        say(f"           RULES v2 live @10bps CAGR {live['CAGR']:.2%} Sharpe {live['Sharpe']:.4f} "
            f"MaxDD {live['MaxDD']:.2%} H1/H2 {live['H1']:.3f}/{live['H2']:.3f}")
        say(f"           OOS SPY {spyO['CAGR']:.2%}/{spyO['Sharpe']:.4f}/{spyO['MaxDD']:.2%}  |  "
            f"OOS RULES v2 {liveO['CAGR']:.2%}/{liveO['Sharpe']:.4f}/{liveO['MaxDD']:.2%}")

        A0 = build_rung(pan, rung_spec("L_G", M.I_G))
        anch = A0["rnet"].copy()
        am, ao = triple(anch[WARMUP:]), triple(anch[i_oos:])
        ah1, ah2 = halves(anch[WARMUP:])
        say(f"           FROZEN INCUMBENT  CAGR {am['CAGR']:.2%} Sharpe {am['Sharpe']:.4f} MaxDD "
            f"{am['MaxDD']:.2%} H1/H2 {ah1:.4f}/{ah2:.4f} | OOS {ao['CAGR']:.2%}/"
            f"{ao['Sharpe']:.4f}/{ao['MaxDD']:.2%}")
        if pan.name == "U56":
            c = M.C_U56
            d = max(abs(am["Sharpe"] - c["Sharpe"]), abs(ao["Sharpe"] - c["oSharpe"]),
                    abs(am["CAGR"] - c["CAGR"]), abs(am["MaxDD"] - c["MaxDD"]))
            g1_ok = gate("G1 cross-script replay of the committed 2026-09-04 U56 anchor "
                         "(15.80%/1.1537/-19.13% full; 1.1857 OOS)",
                         f"max |dev| {d:.2e}", "< 5e-3", d < 5e-3)
        del A0

        def cell(name, ladder, kind, rung_a, rung_b, lam, r, turn, extra):
            k4a, k4b, m, h1, h2, legs = keep_paths(r[WARMUP:], spy, live)
            k4aO, k4bO, mo, _, _, legsO = keep_paths(r[i_oos:], spyO, liveO)
            row = dict(panel=pan.name, ladder=ladder, flat_class=LADDERS[ladder]["flat"],
                       kind=kind, rung_a=str(rung_a), rung_b=str(rung_b), lam=lam,
                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                       turnover_yr=float(np.sum(turn[WARMUP:]) * 252.0 / (T - WARMUP)),
                       dCAGR_pp=(m["CAGR"] - am["CAGR"]) * 100.0,
                       dMaxDD_pp=(m["MaxDD"] - am["MaxDD"]) * 100.0,
                       oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"],
                       odCAGR_pp=(mo["CAGR"] - ao["CAGR"]) * 100.0,
                       keep4a=k4a, keep4b=k4b, keep4a_OOS=k4aO, keep4b_OOS=k4bO,
                       leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                       leg_CAGR=legs["CAGR"], legO_H1=legsO["H1"], legO_H2=legsO["H2"],
                       legO_DD=legsO["DD"], legO_CAGR=legsO["CAGR"],
                       is_Sharpe=sharpe(r[WARMUP:i_is]), name=name)
            for L in BLOCKS:                              # DIAL 2, every grid point published
                dsh, se, tt = pboot(r[WARMUP:], anch[WARMUP:], L)
                dshO, seO, tO = pboot(r[i_oos:], anch[i_oos:], L)
                row[f"dSharpe"] = dsh
                row[f"dSharpe_se_L{L}"] = se
                row[f"dSharpe_t_L{L}"] = tt
                row[f"odSharpe"] = dshO
                row[f"odSharpe_se_L{L}"] = seO
                row[f"odSharpe_t_L{L}"] = tO
            row.update(extra)
            grid.append(row)
            return row

        for lad, spec in LADDERS.items():
            rungs = spec["rungs"]
            prev = prev_flat = prev_v = None
            for j, v in enumerate(rungs):
                s = rung_spec(lad, v)
                R = build_rung(pan, s)
                flat = (R["Wpost"].sum(axis=1) <= 1e-12)
                if is_anchor(s):
                    anchor_dev = max(anchor_dev, float(np.max(np.abs(R["rnet"] - anch))))
                cell(f"{lad}={v}", lad, "RUNG", v, "", np.nan, R["rnet"], R["turn"],
                     dict(ov_hold=np.nan, ov_cap=np.nan, flat_one=np.nan, jaccard=np.nan,
                          D_sharpe=np.nan, R3_CORR_ANCH=np.nan, R3_CORR_OWN=np.nan,
                          R3_LEN=np.nan, flat_share=float(flat[WARMUP:].mean()),
                          is_anchor=is_anchor(s)))
                if prev is not None:
                    ovh, ovc, flat1, jac = overlaps(prev, R, WARMUP)
                    shA, shB = sharpe(prev["rnet"][WARMUP:]), sharpe(R["rnet"][WARMUP:])
                    shA_i, shB_i = sharpe(prev["rnet"][WARMUP:i_is]), sharpe(R["rnet"][WARMUP:i_is])
                    shA_o, shB_o = sharpe(prev["rnet"][i_oos:]), sharpe(R["rnet"][i_oos:])
                    cgA, cgB = cagr(prev["rnet"][WARMUP:]), cagr(R["rnet"][WARMUP:])
                    ovh_i, ovc_i, _, _ = overlaps({"Wpost": prev["Wpost"][:i_is]},
                                                  {"Wpost": R["Wpost"][:i_is]}, WARMUP)
                    ovh_o, ovc_o, _, _ = overlaps({"Wpost": prev["Wpost"][i_oos:]},
                                                  {"Wpost": R["Wpost"][i_oos:]}, 0)
                    own = 0.5 * (prev["rg"] + R["rg"])
                    T3f = third_regressors(prev_flat, flat, anch, own, WARMUP, T)
                    T3i = third_regressors(prev_flat, flat, anch, own, WARMUP, i_is)
                    T3o = third_regressors(prev_flat, flat, anch, own, i_oos, T)
                    Bl = blend(prev, R, LAM)
                    rb = Bl["rnet"]
                    Dsh = sharpe(rb[WARMUP:]) - (LAM * shA + (1 - LAM) * shB)
                    Dcg = cagr(rb[WARMUP:]) - (LAM * cgA + (1 - LAM) * cgB)
                    Dsh_i = sharpe(rb[WARMUP:i_is]) - (LAM * shA_i + (1 - LAM) * shB_i)
                    Dsh_o = sharpe(rb[i_oos:]) - (LAM * shA_o + (1 - LAM) * shB_o)
                    cr = cell(f"{lad} blend {rungs[j-1]}|{v} @{LAM:.2f}", lad, "BLEND",
                              rungs[j - 1], v, LAM, rb, Bl["turn"],
                              dict(ov_hold=ovh, ov_cap=ovc, flat_one=flat1, jaccard=jac,
                                   D_sharpe=Dsh, R3_CORR_ANCH=T3f["R3_CORR_ANCH"],
                                   R3_CORR_OWN=T3f["R3_CORR_OWN"], R3_LEN=T3f["R3_LEN"],
                                   flat_share=np.nan, is_anchor=False))
                    pr = dict(panel=pan.name, ladder=lad, flat_class=spec["flat"],
                              rung_a=str(rungs[j - 1]), rung_b=str(v), lam=LAM,
                              ov_hold=ovh, ov_cap=ovc, jaccard=jac, flat_one=flat1,
                              ov_hold_IS=ovh_i, ov_cap_IS=ovc_i, ov_hold_OOS=ovh_o,
                              ov_cap_OOS=ovc_o,
                              Sharpe_A=shA, Sharpe_B=shB, Sharpe_blend=sharpe(rb[WARMUP:]),
                              D_sharpe=Dsh, D_cagr=Dcg, D_sharpe_IS=Dsh_i, D_sharpe_OOS=Dsh_o,
                              n_spell=T3f["n_spell"], turn_net_yr=cr["turnover_yr"])
                    for tag, d3 in (("", T3f), ("_IS", T3i), ("_OOS", T3o)):
                        for k in R3S:
                            pr[k + tag] = d3[k]
                        pr["flat_one" + tag] = d3["flat_one"]
                    pairs.append(pr)
                    del prev
                prev, prev_flat, prev_v = R, flat, v
            del prev
            say(f"    [{pan.name}] {lad} done ({len(grid)} cells, {time.time()-t0:.0f}s)")

        # ---- G9 causality: truncating the tape cannot move a pre-OOS return -------------------
        for lad, v in (("L_S", 0.15), ("L_M", 150), ("L_R", 0.50)):
            full = build_rung(pan, rung_spec(lad, v))
            trunc = build_rung(pan, rung_spec(lad, v), nrows=i_oos)
            g9_dev = max(g9_dev, float(np.max(np.abs(full["rnet"][:i_oos] - trunc["rnet"]))))
            del full, trunc
        # ---- G10 deterministic recompute -----------------------------------------------------
        R2 = build_rung(pan, rung_spec("L_M", 150))
        ref = [x for x in grid if x["panel"] == pan.name and x["name"] == "L_M=150"][0]
        g10_dev = max(g10_dev, abs(sharpe(R2["rnet"][WARMUP:]) - ref["Sharpe"]))
        del R2

        # ---- rule 8 capital arm (IS-only choosers; 2017-2026 read ONCE) ----------------------
        cand = [x for x in grid if x["panel"] == pan.name]
        for tag, pool in (("ARGMAX-IS (all 63 cells)", cand),
                          ("ARGMAX-IS (blends only)", [x for x in cand if x["kind"] == "BLEND"]),
                          ("ARGMAX-IS (flat ladders only)",
                           [x for x in cand if x["ladder"] in FLAT_LADDERS]),
                          ("DO NOTHING (frozen incumbent)",
                           [x for x in cand if x.get("is_anchor")])):
            pick = max(pool, key=lambda x: (-1e9 if not np.isfinite(x["is_Sharpe"])
                                            else x["is_Sharpe"]))
            wf_rows.append(dict(
                panel=pan.name, chooser=tag, cell=pick["name"], ladder=pick["ladder"],
                kind=pick["kind"], IS_Sharpe=pick["is_Sharpe"],
                OOS_CAGR=pick["oCAGR"], OOS_Sharpe=pick["oSharpe"], OOS_MaxDD=pick["oMaxDD"],
                FULL_CAGR=pick["CAGR"], FULL_Sharpe=pick["Sharpe"], FULL_MaxDD=pick["MaxDD"],
                FULL_H1=pick["H1"], FULL_H2=pick["H2"],
                anchor_OOS_CAGR=ao["CAGR"], anchor_OOS_Sharpe=ao["Sharpe"],
                anchor_OOS_MaxDD=ao["MaxDD"], anchor_FULL_Sharpe=am["Sharpe"],
                anchor_FULL_CAGR=am["CAGR"], anchor_FULL_MaxDD=am["MaxDD"],
                spy_OOS_CAGR=spyO["CAGR"], spy_OOS_Sharpe=spyO["Sharpe"],
                spy_OOS_MaxDD=spyO["MaxDD"], spy_FULL_CAGR=spy["CAGR"],
                spy_FULL_Sharpe=spy["Sharpe"], spy_FULL_MaxDD=spy["MaxDD"],
                live_OOS_CAGR=liveO["CAGR"], live_OOS_Sharpe=liveO["Sharpe"],
                live_OOS_MaxDD=liveO["MaxDD"], live_FULL_Sharpe=live["Sharpe"],
                odSharpe=pick["odSharpe"], odSharpe_t_L63=pick["odSharpe_t_L63"],
                keep4a=pick["keep4a"], keep4b=pick["keep4b"],
                keep4a_OOS=pick["keep4a_OOS"], keep4b_OOS=pick["keep4b_OOS"]))

    gate("G2 the anchor is bit-identical wherever it recurs across ladders",
         f"max |dev| {anchor_dev:.3e}", "< 1e-12", anchor_dev < 1e-12)
    gate("G9 causality: truncating the tape at 2017-01-01 does not move any pre-OOS return",
         f"max |dev| {g9_dev:.3e}", "< 1e-12", g9_dev < 1e-12)
    gate("G10 deterministic recompute (L_M=150, one per panel)", f"max |dSharpe| {g10_dev:.3e}",
         "< 1e-12", g10_dev < 1e-12)
    return pd.DataFrame(grid), pd.DataFrame(pairs), pd.DataFrame(wf_rows), t0


# ---------------------------------------------------------------------------------------------
def fit_block(P, ovcol, r3col, ladders=None, X_from=None, y_from=None):
    """OLS of D_sharpe on [1, 1-OV, flat_one, R3].  Returns (beta, r2, n)."""
    Q = P if ladders is None else P[P.ladder.isin(ladders)]
    X = np.column_stack([np.ones(len(Q)), 1.0 - Q[ovcol].values, Q["flat_one"].values,
                         Q[r3col].values])
    y = Q["D_sharpe"].values
    beta, resid, r2 = ols(X, y)
    return beta, r2, len(Q), X, y, Q


def analyse(G, P, W, t0):
    say("\n" + "=" * 124)
    say("1.  THE POOLED FIT — does a THIRD number reach 0.80 where TWO reached 0.5460?")
    say("=" * 124)
    say(f"    {len(P)} pairs (27 adjacent pairs x 3 panels), lambda = {LAM}.  "
        f"Committed 1538 two-number R^2: OV_HOLD {C_1538['R2_HOLD']:.4f}, "
        f"OV_CAP {C_1538['R2_CAP']:.4f}.")
    fits = []
    say(f"\n    {'OV stat':9s} {'third regressor':16s} {'R^2(1)':>8s} {'R^2(2)':>8s} "
        f"{'R^2(3)':>8s} {'dR^2 3-2':>9s} {'+identity':>10s} {'dR^2 id':>8s} "
        f"{'beta_R3':>9s} {'t_R3':>7s} {'T1':>5s}")
    for ovname, ovcol in (("OV_HOLD", "ov_hold"), ("OV_CAP", "ov_cap")):
        X1 = np.column_stack([np.ones(len(P)), 1.0 - P[ovcol].values])
        _, _, r2_1 = ols(X1, P["D_sharpe"].values)
        X2 = np.column_stack([np.ones(len(P)), 1.0 - P[ovcol].values, P["flat_one"].values])
        _, _, r2_2 = ols(X2, P["D_sharpe"].values)
        for r3 in R3S:
            beta, r2_3, n, X3, y, _ = fit_block(P, ovcol, r3)
            D = pd.get_dummies(P["ladder"], drop_first=True).values.astype(float)
            Xid = np.column_stack([X3, D])
            _, _, r2_id = ols(Xid, y)
            resid = y - X3 @ beta
            s2 = float((resid ** 2).sum()) / max(len(y) - X3.shape[1], 1)
            cov = s2 * np.linalg.pinv(X3.T @ X3)
            t_r3 = float(beta[3] / np.sqrt(max(cov[3, 3], 1e-300)))
            ok = r2_3 >= R2_BAR
            fits.append(dict(ov=ovname, r3=r3, n=n, R2_one=r2_1, R2_two=r2_2, R2_three=r2_3,
                             dR2_three_two=r2_3 - r2_2, R2_plus_identity=r2_id,
                             dR2_identity=r2_id - r2_3, beta_ov=beta[1], beta_flat=beta[2],
                             beta_R3=beta[3], t_R3=t_r3, T1_pass=ok))
            say(f"    {ovname:9s} {r3:16s} {r2_1:8.4f} {r2_2:8.4f} {r2_3:8.4f} "
                f"{r2_3-r2_2:+9.4f} {r2_id:10.4f} {r2_id-r2_3:+8.4f} {beta[3]:+9.4f} "
                f"{t_r3:+7.2f} {'PASS' if ok else 'FAIL':>5s}")
    F = pd.DataFrame(fits)
    best = F.loc[F.R2_three.idxmax()]
    t1 = bool(F.T1_pass.any())
    gate(f"T1 pooled THREE-number R^2 >= {R2_BAR}",
         f"best {best.R2_three:.4f} ({best.ov} + {best.r3}); 6 of 6 cells published", f">= {R2_BAR}",
         t1)
    t2 = bool((F.dR2_identity < DR2_BAR).all())
    gate(f"T2 dR^2 from ladder identity < {DR2_BAR} at EVERY cell",
         f"max {F.dR2_identity.max():+.4f}", f"< {DR2_BAR}", t2)

    say("\n" + "=" * 124)
    say("2.  T3 — per-ladder residual means, and T4 LEAVE-ONE-LADDER-OUT (the test that killed "
        "1538)")
    say("=" * 124)
    lolo = []
    for ovname, ovcol in (("OV_HOLD", "ov_hold"), ("OV_CAP", "ov_cap")):
        for r3 in R3S:
            beta, r2_3, n, X3, y, _ = fit_block(P, ovcol, r3)
            resid = y - X3 @ beta
            sd = float(resid.std(ddof=4))          # 1538's T3 convention: POOLED residual sd
            for lad in sorted(P.ladder.unique()):
                m = (P.ladder == lad).values
                rr = resid[m]
                tt = float(rr.mean() / (sd / np.sqrt(m.sum()))) if sd > 0 else np.nan
                b_out, r2_out, n_out, X_out, y_out, _ = fit_block(
                    P, ovcol, r3, ladders=[l for l in P.ladder.unique() if l != lad])
                Q = P[P.ladder == lad]
                Xh = np.column_stack([np.ones(len(Q)), 1.0 - Q[ovcol].values,
                                      Q["flat_one"].values, Q[r3].values])
                pred = Xh @ b_out
                r2_held = r2_against(Q["D_sharpe"].values, pred)
                lolo.append(dict(ov=ovname, r3=r3, ladder=lad, flat=lad in FLAT_LADDERS,
                                 n=int(m.sum()), resid_mean=float(rr.mean()),
                                 resid_sd_pooled=sd, resid_t=tt,
                                 lolo_R2=r2_held, lolo_pass=bool(r2_held >= LOLO_BAR)))
    LO = pd.DataFrame(lolo)
    t3 = bool((LO.resid_t.abs() <= T_BAR).all())
    gate(f"T3 no ladder residual |t| > {T_BAR} at ANY cell",
         f"worst |t| {LO.resid_t.abs().max():.2f} ({LO.loc[LO.resid_t.abs().idxmax(),'ladder']})",
         f"<= {T_BAR}", t3)
    say("\n    T4 leave-one-ladder-out R^2 on the THREE FLAT-BEARING ladders "
        f"(1538 committed: L_R {C_1538['LOLO_L_R']:.2f}, L_M {C_1538['LOLO_L_M']:+.4f}):")
    say(f"    {'OV stat':9s} {'third regressor':16s} " + "".join(f"{l:>12s}" for l in FLAT_LADDERS)
        + f"{'T4':>7s}")
    t4_any = False
    for ovname in ("OV_HOLD", "OV_CAP"):
        for r3 in R3S:
            sub = LO[(LO.ov == ovname) & (LO.r3 == r3)].set_index("ladder")
            vals = [sub.loc[l, "lolo_R2"] for l in FLAT_LADDERS]
            ok = all(v >= LOLO_BAR for v in vals)
            t4_any = t4_any or ok
            say(f"    {ovname:9s} {r3:16s} " + "".join(f"{v:12.4f}" for v in vals)
                + f"{'PASS' if ok else 'FAIL':>7s}")
    gate(f"T4 leave-one-ladder-out R^2 >= {LOLO_BAR} on EACH flat ladder, at ANY published cell",
         f"best flat-ladder minimum "
         f"{max(min(LO[(LO.ov==o)&(LO.r3==r)&(LO.flat)].lolo_R2) for o in ['OV_HOLD','OV_CAP'] for r in R3S):.4f}",
         f">= {LOLO_BAR}", t4_any)
    say("\n    (all 9 ladders, every cell, in the .lolo.csv)")

    say("\n" + "=" * 124)
    say("3.  T5 — RULE 8 TRANSFER: fit on 2009-2016 pair statistics ONLY, predict 2017-2026")
    say("=" * 124)
    t5rows = []
    say(f"    {'OV stat':9s} {'third regressor':16s} {'R^2 two':>9s} {'R^2 three':>10s} "
        f"{'dR^2':>8s} {'T5':>6s}")
    for ovname, ovcol in (("OV_HOLD", "ov_hold"), ("OV_CAP", "ov_cap")):
        for r3 in R3S:
            cols = [ovcol + "_IS", "flat_one_IS", r3 + "_IS", "D_sharpe_IS",
                    ovcol + "_OOS", "flat_one_OOS", r3 + "_OOS", "D_sharpe_OOS"]
            fin = np.isfinite(P[cols].values.astype(float)).all(axis=1)   # 1538's finite mask
            Q = P[fin]
            Xi2 = np.column_stack([np.ones(len(Q)), 1.0 - Q[ovcol + "_IS"].values,
                                   Q["flat_one_IS"].values])
            b2, _, r2i_2 = ols(Xi2, Q["D_sharpe_IS"].values)
            Xo2 = np.column_stack([np.ones(len(Q)), 1.0 - Q[ovcol + "_OOS"].values,
                                   Q["flat_one_OOS"].values])
            r2o_2 = r2_against(Q["D_sharpe_OOS"].values, Xo2 @ b2)
            Xi = np.column_stack([Xi2, Q[r3 + "_IS"].values])
            b3, _, r2i_3 = ols(Xi, Q["D_sharpe_IS"].values)
            Xo = np.column_stack([Xo2, Q[r3 + "_OOS"].values])
            r2o_3 = r2_against(Q["D_sharpe_OOS"].values, Xo @ b3)
            ok = r2o_3 >= OOS_R2_BAR
            t5rows.append(dict(ov=ovname, r3=r3, n=int(fin.sum()), n_dropped=int((~fin).sum()),
                               IS_R2_two=r2i_2, IS_R2_three=r2i_3,
                               OOS_R2_two=r2o_2, OOS_R2_three=r2o_3,
                               dR2=r2o_3 - r2o_2, T5_pass=ok))
            say(f"    {ovname:9s} {r3:16s} {r2o_2:9.4f} {r2o_3:10.4f} {r2o_3-r2o_2:+8.4f} "
                f"{'PASS' if ok else 'FAIL':>6s}   (n={int(fin.sum())}, "
                f"{int((~fin).sum())} pairs dropped non-finite; IS R^2 {r2i_3:.4f})")
    T5 = pd.DataFrame(t5rows)
    t5 = bool(T5.T5_pass.any())
    gate(f"T5 rule-8 OOS transfer R^2 >= {OOS_R2_BAR} at ANY published cell",
         f"best {T5.OOS_R2_three.max():.4f}", f">= {OOS_R2_BAR}", t5)

    say("\n" + "=" * 124)
    say("4.  THE FLAT-SPELL TIMING ITSELF — what the third regressor actually measures")
    say("=" * 124)
    fl = P[P.ladder.isin(FLAT_LADDERS)]
    tab = fl.groupby(["ladder", "panel"])[["flat_one", "R3_CORR_ANCH", "R3_CORR_OWN", "R3_LEN",
                                           "n_spell"]].mean().round(4)
    say(tab.to_string())
    say("\n    The 1558 hypothesis in one line: L_M and L_R carry nearly identical flat_one but "
        "should differ in TIMING.")
    for st in ("flat_one", "R3_CORR_ANCH", "R3_CORR_OWN", "R3_LEN"):
        a = fl[fl.ladder == "L_M"][st].mean()
        b = fl[fl.ladder == "L_R"][st].mean()
        c = fl[fl.ladder == "L_S"][st].mean()
        sd = fl[st].std(ddof=1)
        say(f"      {st:14s} L_S {c:+8.4f}  L_M {a:+8.4f}  L_R {b:+8.4f}   "
            f"|L_M - L_R| = {abs(a-b):.4f} = {abs(a-b)/sd if sd>0 else np.nan:.2f} sd")
    publish("L_M vs L_R separation by regressor",
            {st: float(abs(fl[fl.ladder == 'L_M'][st].mean() - fl[fl.ladder == 'L_R'][st].mean()))
             for st in ("flat_one", "R3_CORR_ANCH", "R3_CORR_OWN", "R3_LEN")})

    say("\n" + "=" * 124)
    say("5.  THE CAPITAL ARM — both KEEP paths at every one of the 189 cells, rule-8 walk-forward")
    say("=" * 124)
    say(f"    4a FULL {int(G.keep4a.sum())}/{len(G)};  4a OOS {int(G.keep4a_OOS.sum())}/{len(G)};  "
        f"4b FULL {int(G.keep4b.sum())}/{len(G)};  4b OOS {int(G.keep4b_OOS.sum())}/{len(G)};  "
        f"4b BOTH {int((G.keep4b & G.keep4b_OOS).sum())}/{len(G)}.")
    cols = ["panel", "chooser", "cell", "IS_Sharpe", "FULL_CAGR", "FULL_Sharpe", "FULL_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "keep4a", "keep4b", "keep4a_OOS", "keep4b_OOS"]
    say(W[cols].to_string(index=False,
                          float_format=lambda x: f"{x:.4f}"))
    mix = W[W.chooser != "DO NOTHING (frozen incumbent)"]
    non = W[W.chooser == "DO NOTHING (frozen incumbent)"]
    say(f"\n    rule-8 chooser mean OOS Sharpe {mix.OOS_Sharpe.mean():.4f} vs "
        f"DO NOTHING {non.OOS_Sharpe.mean():.4f}.")
    both = G[G.keep4b & G.keep4b_OOS]
    if len(both):
        say("\n    Cells clearing 4b on BOTH windows:")
        say(both[["panel", "name", "CAGR", "Sharpe", "MaxDD", "oCAGR", "oSharpe", "oMaxDD",
                  "keep4a"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 124)
    ok = dict(T1=t1, T2=t2, T3=t3, T4=t4_any, T5=t5)
    say(f"    PRE-REGISTERED VERDICT: {ok}")
    verdict = ("KEEP the three-number prediction rule" if (t1 and t4_any)
               else "KILL the three-number hypothesis")
    say(f"    => {verdict}")
    say(f"    BEST three-number pooled R^2 {F.R2_three.max():.4f} against 1538's two-number "
        f"{max(C_1538['R2_HOLD'], C_1538['R2_CAP']):.4f} and the 0.80 bar.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    F.to_csv(f"{OUT}.fit.csv", index=False)
    LO.to_csv(f"{OUT}.lolo.csv", index=False)
    T5.to_csv(f"{OUT}.t5.csv", index=False)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P.to_csv(f"{OUT}.pairs.csv", index=False)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES/TESTS PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, P, W, t0 = main()
    analyse(G, P, W, t0)
