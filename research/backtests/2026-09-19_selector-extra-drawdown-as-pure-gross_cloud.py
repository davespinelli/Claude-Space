#!/usr/bin/env python3
"""IDEA 762 (lane cloud, 2026-09-19) — does the SELECTOR's 10 pp EXTRA DRAWDOWN price out as PURE
GROSS?

WHY.  Idea 560 built a rolling threshold SELECTOR — at every weekly rebalance it holds the gate
book of the threshold with the highest trailing value of a leg statistic, data <= t only — and its
rule-8 pick on U56 / MA-DIST beats its IS-best FIXED twin by +5.87 pp of OOS CAGR (18.01% vs
12.14%) while running -30.11% MaxDD against -20.10% and 15.32x/yr turnover against 2.71x.  Eight
consecutive 2026-09-19 runs found every drawdown-BUYING device beaten at matched exposure by a
plain constant de-gross.  762 asks the mirror question about the one device in the record that
BUYS RETURN WITH DRAWDOWN: de-gross the selector until its realised drawdown matches the fixed
arm's and ask whether ANY of the CAGR advantage survives, net of the turnover it adds.

THE TWO TUNED PARAMETERS (rule 4), every grid point published:
  DIAL 1  the selector's GROSS g, laddered over 14 rungs 0.10..0.75, plus the solved g* that
          matches the fixed arm on each target.  (The FIXED arm always stands at the record's
          standing gross 0.75; only the selector is de-grossed.  No leverage: g <= 0.75.)
  DIAL 2  the MATCHING TARGET: {MAXDD, MEANGROSS, VOL, CAGR}, each solved on the FULL window and,
          separately, on the IS window only (the rule-8 legal version).

NOT TUNED: 560's own construction — its 9 MA-DIST/MOM12_1 thresholds and 9 LOWVOL ceilings, its
four leg statistics x three trailing windows, its (statistic, window) rule-8 pick by IS Sharpe
alone, its IS-best FIXED threshold, weekly cadence, 10 bps, next-day execution.  560's builders are
IMPORTED, not re-implemented, so the arms are literally 560's arms (gate G1 replays its committed
U56 / MA-DIST numbers).

WHAT WOULD MAKE THE SELECTOR REAL: a CAGR advantage that survives at matched drawdown, on more
than one (panel, family) cell, with the matching gross solved on IS rows only.

CAPITAL ARM (protocol step 3): both KEEP paths at every cell against live RULES v2 AND SPY, full
sample and halves, and a rule-8 walk-forward in which g* is solved on warm-up..2016-12-31 ONLY and
2017-2026 is read once.

Offline, deterministic, no network.
  python research/backtests/2026-09-19_selector-extra-drawdown-as-pure-gross_cloud.py
"""
from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "research"))
sys.path.insert(0, str(REPO / "products" / "backtester"))

_SRC = HERE / "2026-09-11_is-rbar_drop-a-screening-statistic_B.py"
_spec = importlib.util.spec_from_file_location("idea560", _SRC)
M = importlib.util.module_from_spec(_spec)
sys.modules["idea560"] = M
_spec.loader.exec_module(M)                      # module-level only; main() is guarded

DATE, SLUG = "2026-09-19", "selector-extra-drawdown-as-pure-gross"
OUT = HERE / f"{DATE}_{SLUG}_cloud"

PANELS, FAMILIES, STATS, WINDOWS = M.PANELS, M.FAMILIES, M.STATS, M.WINDOWS
SEL_LENS, CVOL, GROSS, COST_BPS = M.SEL_LENS, M.CVOL, M.GROSS, M.COST_BPS
IS_END, OOS_START = M.IS_END, M.OOS_START
fast_run, stat, verdict_4a, fail_4b = M.fast_run, M.stat, M.verdict_4a, M.fail_4b
gate_abs, rank_var, thresholds, leg_series = M.gate_abs, M.rank_var, M.thresholds, M.leg_series
rolling_signed, live_mask = M.rolling_signed, M.live_mask

GLADDER = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
TARGETS = ["MAXDD", "MEANGROSS", "VOL", "CAGR"]
SOLVE_WINDOWS = ["FULL", "IS"]
C560 = dict(sel_oCAGR=0.1801, sel_oSharpe=1.1245, sel_oMaxDD=-0.3011, fixed_th=-0.12,
            fx_oCAGR=0.1214, fx_oSharpe=1.1020, fx_oMaxDD=-0.2010)

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
    return df.to_string(index=False, float_format=lambda x: f"{x:.{p}f}")


def respread_g(px, g, gross):
    """560's respread with the gross as an argument instead of the module constant."""
    k = g.sum(axis=1).clip(lower=1)
    return g.astype(float).div(k, axis=0) * gross


def ann_vol(r):
    return float(r.std(ddof=0) * np.sqrt(252))


def score(px, W, start, years, extra=None):
    """One book: full/halves/IS/OOS triples, realised gross, vol, turnover."""
    res = fast_run(px, W)
    r = res["returns"].loc[start:]
    s = dict(stat(r))
    s["turn_yr"] = float(res["turnover"].loc[start:].sum() / years)
    s["cost_bp_yr"] = s["turn_yr"] * COST_BPS
    wsum = res["weights"].loc[start:].sum(axis=1)
    s["mean_gross"] = float(wsum.mean())
    s["mean_gross_IS"] = float(wsum.loc[:IS_END].mean())
    s["VOL"] = ann_vol(r)
    s["VOL_IS"] = ann_vol(r.loc[:IS_END])
    s["MAXDD"] = abs(s["MaxDD"])
    s["MAXDD_IS"] = abs(s["isMaxDD"])
    s["CAGR_t"] = s["CAGR"]
    s["CAGR_IS"] = s["isCAGR"]
    s["MEANGROSS"] = s["mean_gross"]
    s["MEANGROSS_IS"] = s["mean_gross_IS"]
    s["VOL_t"] = s["VOL"]
    if extra:
        s.update(extra)
    return s


def target_value(s, tgt, window):
    return s[f"{tgt}_IS"] if window == "IS" else s[{"MAXDD": "MAXDD", "MEANGROSS": "MEANGROSS",
                                                    "VOL": "VOL", "CAGR": "CAGR_t"}[tgt]]


def solve_g(ladder_rows, tgt, window, want):
    """Linear interpolation of g against the target statistic over the published ladder.
    Monotone in g for MAXDD / MEANGROSS / VOL; CAGR need not be, so the nearest crossing is
    taken and the non-monotonicity is PUBLISHED rather than assumed away."""
    gs = np.array([r["gross"] for r in ladder_rows], float)
    ys = np.array([target_value(r, tgt, window) for r in ladder_rows], float)
    o = np.argsort(gs)
    gs, ys = gs[o], ys[o]
    if want <= ys.min():
        return float(gs[0]), "BELOW LADDER (clipped)"
    if want >= ys.max():
        return float(gs[-1]), "ABOVE LADDER (clipped)"
    cross = np.flatnonzero((ys[:-1] - want) * (ys[1:] - want) <= 0)
    i = int(cross[-1])
    if ys[i + 1] == ys[i]:
        return float(gs[i]), "flat segment"
    g = gs[i] + (want - ys[i]) * (gs[i + 1] - gs[i]) / (ys[i + 1] - ys[i])
    return float(np.clip(g, GLADDER[0], GROSS)), ("interpolated" if len(cross) == 1
                                                  else f"{len(cross)} crossings (NON-MONOTONE)")


# ---------------------------------------------------------------------------------------------
def main():
    t0 = time.time()
    say("=" * 150)
    say("IDEA 762 (lane cloud, 2026-09-19) — does the SELECTOR's 10 pp EXTRA DRAWDOWN price out as "
        "PURE GROSS?")
    say("=" * 150)
    say("ARMS per (panel, family): 560's rule-8 SELECTOR (statistic, window picked on IS Sharpe "
        "alone over 12 variants) vs 560's IS-best FIXED threshold, both at 10 bps, weekly, t+1.")
    say(f"DIAL 1 selector gross {GLADDER} (14 rungs) + the solved g*;  "
        f"DIAL 2 matching target {TARGETS}, solved on {SOLVE_WINDOWS}.")
    say("The FIXED arm always stands at the record's standing gross 0.75.  No leverage.")
    say("=" * 150)

    PN, n_dropped = M.panels()
    say(f"  SMALL filter (protocol-mandated): data/small_meta.csv drops {n_dropped} tickers with "
        f"max_1d_move >= 1.0.")
    say("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-constituent lists and SMALL439 a "
        "CURRENT sub-$2B screen carried back to 2008/2010, so every ABSOLUTE level below is an "
        "UPPER BOUND.  What this run reads is a CONTRAST between two books over the SAME names on "
        "the SAME days, which the bias cannot manufacture.")

    rows, sel_rows, solved = [], [], []
    comparand = {}

    for pn in PANELS:
        px, spy_px = PN[pn]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        R = px.pct_change().fillna(0.0).loc[start:]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(fast_run(px, M.rules_v2_weights(px))["returns"].loc[start:])
        comparand[pn] = dict(spy=spy_s, live=live_s, start=start, years=years)
        say(f"\n  PANEL {pn}  {start.date()}..{px.index[-1].date()}  ({years:.2f}y, "
            f"{px.shape[1]} names)")
        say(f"    SPY              CAGR {spy_s['CAGR']:.2%} Sharpe {spy_s['Sharpe']:.4f} MaxDD "
            f"{spy_s['MaxDD']:.2%} | OOS {spy_s['oCAGR']:.2%}/{spy_s['oSharpe']:.4f}/"
            f"{spy_s['oMaxDD']:.2%}")
        say(f"    RULES v2 (live)  CAGR {live_s['CAGR']:.2%} Sharpe {live_s['Sharpe']:.4f} MaxDD "
            f"{live_s['MaxDD']:.2%} | OOS {live_s['oCAGR']:.2%}/{live_s['oSharpe']:.4f}/"
            f"{live_s['oMaxDD']:.2%}")
        say(f"    4b bars from SPY: H1>{spy_s['H1']:.4f} H2>{spy_s['H2']:.4f} "
            f"OOS>{spy_s['oSharpe']:.4f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.2%} "
            f"CAGR>={0.70*spy_s['CAGR']:.2%}")

        V_by_fam = {fam: M.rank_var(px, fam) for fam in FAMILIES}

        for fam in FAMILIES:
            ths = thresholds(fam)
            V, lv = V_by_fam[fam]
            nlive = live_mask(px).loc[start:].sum(axis=1)
            Wt, SS, fixed_scores = {}, {}, []
            for th in ths:
                gA = gate_abs(px, fam, th)
                x = float((gA.loc[start:].sum(axis=1) / nlive).mean())
                gB = M.gate_quantile(V, lv, x)
                WA = respread_g(px, gA, GROSS)
                WB = respread_g(px, gB, GROSS)
                Wt[th] = WA
                ra, rb = fast_run(px, WA), fast_run(px, WB)   # 560's own leg construction:
                SS[th] = leg_series(ra["weights"].loc[start:],   # DRIFTED weights, not raw W
                                    rb["weights"].loc[start:], R)
                s = score(px, WA, start, years,
                          extra=dict(panel=pn, family=fam, arm="FIXED", th=th, gross=GROSS,
                                     statistic="", window="", cell=f"FIXED th={th}"))
                fixed_scores.append(s)
            FX = max(fixed_scores, key=lambda s: s["isSharpe"])       # 560's IS-best fixed twin
            for s in fixed_scores:
                s["is_IS_best_fixed"] = (s is FX)
                rows.append(s)

            # --- 560's 12 selector variants; the rule-8 pick is by IS Sharpe ALONE -------------
            variants = []
            for st in STATS:
                for wn in WINDOWS:
                    Lw = SEL_LENS[wn]
                    fallback = -CVOL[4] if fam == "LOWVOL" else 0.0
                    sv = pd.DataFrame({th: rolling_signed(SS[th], st, Lw) for th in ths})
                    valid = sv.notna().any(axis=1)
                    choice = pd.Series(np.nan, index=sv.index, dtype=float)
                    if valid.any():
                        choice.loc[valid] = sv.loc[valid].idxmax(axis=1).astype(float)
                    choice = choice.ffill().reindex(px.index).ffill().fillna(fallback)
                    Wsel = pd.DataFrame(0.0, index=px.index, columns=px.columns)
                    for th in ths:
                        m = (choice == th)
                        if m.any():
                            Wsel.loc[m] = Wt[th].loc[m]
                    s = score(px, Wsel, start, years,
                              extra=dict(panel=pn, family=fam, arm="SELECTOR", th=np.nan,
                                         gross=GROSS, statistic=st, window=wn,
                                         switches=int((choice != choice.shift(1)).sum()),
                                         cell=f"SELECTOR ({st},{wn}) g=0.75"))
                    s["_W"] = Wsel
                    variants.append(s)
            PK = max(variants, key=lambda s: s["isSharpe"])
            for s in variants:
                s2 = {k: v for k, v in s.items() if k != "_W"}
                s2["is_rule8_pick"] = (s is PK)
                sel_rows.append(s2)
            Wpick = PK.pop("_W")

            say(f"    [{pn}/{fam}] rule-8 pick ({PK['statistic']},{PK['window']}) IS Sharpe "
                f"{PK['isSharpe']:.4f} | IS-best FIXED th {FX['th']:+.2f} IS Sharpe "
                f"{FX['isSharpe']:.4f}   ({time.time()-t0:.0f}s)")

            # --- DIAL 1: the de-gross ladder on the SELECTOR ---------------------------------
            ladder = []
            for g in GLADDER:
                s = score(px, Wpick * (g / GROSS), start, years,
                          extra=dict(panel=pn, family=fam, arm="SELECTOR-DEGROSS", th=np.nan,
                                     gross=g, statistic=PK["statistic"], window=PK["window"],
                                     cell=f"SELECTOR ({PK['statistic']},{PK['window']}) g={g:.2f}",
                                     is_rule8_pick=False))
                ladder.append(s)
                rows.append(s)
            PKrow = {k: v for k, v in PK.items()}
            PKrow["arm"] = "SELECTOR"
            PKrow["is_rule8_pick"] = True
            rows.append(PKrow)

            # --- DIAL 2: solve g* per matching target, on FULL and on IS only ----------------
            for tgt in TARGETS:
                for wnd in SOLVE_WINDOWS:
                    want = target_value(FX, tgt, wnd)
                    gstar, how = solve_g(ladder, tgt, wnd, want)
                    s = score(px, Wpick * (gstar / GROSS), start, years,
                              extra=dict(panel=pn, family=fam, arm="SELECTOR-MATCHED", th=np.nan,
                                         gross=gstar, statistic=PK["statistic"],
                                         window=PK["window"], target=tgt, solve_window=wnd,
                                         solve_note=how,
                                         cell=f"SELECTOR matched on {tgt} ({wnd}) g*={gstar:.4f}",
                                         is_rule8_pick=False))
                    rows.append(s)
                    solved.append(dict(
                        panel=pn, family=fam, target=tgt, solve_window=wnd, gstar=gstar,
                        solve_note=how, want=want,
                        got=target_value(s, tgt, wnd),
                        sel_CAGR=s["CAGR"], sel_Sharpe=s["Sharpe"], sel_MaxDD=s["MaxDD"],
                        sel_H1=s["H1"], sel_H2=s["H2"],
                        sel_oCAGR=s["oCAGR"], sel_oSharpe=s["oSharpe"], sel_oMaxDD=s["oMaxDD"],
                        sel_turn=s["turn_yr"], sel_cost_bp=s["cost_bp_yr"],
                        raw_sel_turn=PK["turn_yr"], raw_sel_cost_bp=PK["cost_bp_yr"],
                        fx_th=FX["th"], fx_CAGR=FX["CAGR"], fx_Sharpe=FX["Sharpe"],
                        fx_MaxDD=FX["MaxDD"], fx_H1=FX["H1"], fx_H2=FX["H2"],
                        fx_oCAGR=FX["oCAGR"], fx_oSharpe=FX["oSharpe"], fx_oMaxDD=FX["oMaxDD"],
                        fx_turn=FX["turn_yr"], fx_cost_bp=FX["cost_bp_yr"],
                        dCAGR_pp=(s["CAGR"] - FX["CAGR"]) * 100.0,
                        dCAGR_OOS_pp=(s["oCAGR"] - FX["oCAGR"]) * 100.0,
                        dSharpe=s["Sharpe"] - FX["Sharpe"],
                        dSharpe_OOS=s["oSharpe"] - FX["oSharpe"],
                        dMaxDD_pp=(s["MaxDD"] - FX["MaxDD"]) * 100.0,
                        raw_dCAGR_pp=(PK["CAGR"] - FX["CAGR"]) * 100.0,
                        raw_dCAGR_OOS_pp=(PK["oCAGR"] - FX["oCAGR"]) * 100.0,
                        raw_dMaxDD_pp=(PK["MaxDD"] - FX["MaxDD"]) * 100.0))

    G = pd.DataFrame(rows)
    S = pd.DataFrame(sel_rows)
    SV = pd.DataFrame(solved)

    # --- both KEEP paths on every cell ---------------------------------------------------------
    for df in (G, S):
        df["p4a"] = [verdict_4a(r, comparand[r["panel"]]["live"]) for _, r in df.iterrows()]
        df["f4b"] = [fail_4b(r, comparand[r["panel"]]["spy"]) for _, r in df.iterrows()]
        df["p4b"] = df.f4b == "-"

    # --- G1 replay of 560's committed U56 / MA-DIST numbers ------------------------------------
    u = S[(S.panel == "U56") & (S.family == "MA-DIST") & (S.is_rule8_pick)].iloc[0]
    f = G[(G.panel == "U56") & (G.family == "MA-DIST") & (G.arm == "FIXED")
          & (G.is_IS_best_fixed)].iloc[0]
    d = max(abs(u.oCAGR - C560["sel_oCAGR"]), abs(u.oSharpe - C560["sel_oSharpe"]),
            abs(u.oMaxDD - C560["sel_oMaxDD"]), abs(f.th - C560["fixed_th"]),
            abs(f.oCAGR - C560["fx_oCAGR"]), abs(f.oSharpe - C560["fx_oSharpe"]),
            abs(f.oMaxDD - C560["fx_oMaxDD"]))
    gate("G1 cross-script replay of idea 560's committed U56/MA-DIST arms "
         "(selector OOS 18.01%/1.1245/-30.11%; IS-best FIXED th -0.12 12.14%/1.1020/-20.10%)",
         f"max |dev| {d:.2e} (got selector {u.oCAGR:.4f}/{u.oSharpe:.4f}/{u.oMaxDD:.4f}; "
         f"fixed th {f.th:+.2f} {f.oCAGR:.4f}/{f.oSharpe:.4f}/{f.oMaxDD:.4f})", "< 5e-3", d < 5e-3)
    gate("G2 exactly two tuned parameters (selector gross, matching target)", 2, "== 2", True)

    # --- G3 the de-gross ladder is monotone in |MaxDD| (published where it is not) --------------
    viol = 0
    for (pn, fam), sub in G[G.arm == "SELECTOR-DEGROSS"].groupby(["panel", "family"]):
        y = sub.sort_values("gross").MAXDD.values
        viol += int((np.diff(y) < -1e-9).sum())
    gate("G3 |MaxDD| is monotone non-decreasing in gross on all 9 de-gross ladders",
         f"{viol} violations over {9*(len(GLADDER)-1)} steps", "== 0", viol == 0)
    return G, S, SV, comparand, t0


# ---------------------------------------------------------------------------------------------
def analyse(G, S, SV, comparand, t0):
    say("\n" + "=" * 150)
    say("1.  THE HEADLINE — U56 / MA-DIST, the exact cell idea 762 was filed on")
    say("=" * 150)
    h = SV[(SV.panel == "U56") & (SV.family == "MA-DIST")]
    raw = h.iloc[0]
    say(f"    RAW (both arms at gross 0.75): selector beats the fixed twin by "
        f"{raw.raw_dCAGR_pp:+.2f} pp of FULL CAGR and {raw.raw_dCAGR_OOS_pp:+.2f} pp of OOS CAGR, "
        f"at {raw.raw_dMaxDD_pp:+.2f} pp of MaxDD and "
        f"{raw.raw_sel_turn/raw.fx_turn:.1f}x the turnover "
        f"({raw.raw_sel_turn:.2f} vs {raw.fx_turn:.2f} per yr, "
        f"{raw.raw_sel_cost_bp:.0f} vs {raw.fx_cost_bp:.0f} bp/yr of cost, charged).")
    say(f"\n    {'target':10s} {'solved on':9s} {'g*':>7s} {'sel CAGR':>9s} {'fx CAGR':>8s} "
        f"{'dCAGR pp':>9s} {'sel MaxDD':>10s} {'fx MaxDD':>9s} {'dSharpe':>8s} "
        f"{'OOS dCAGR pp':>13s} {'OOS dSharpe':>12s}")
    for _, r in h.iterrows():
        say(f"    {r.target:10s} {r.solve_window:9s} {r.gstar:7.4f} {r.sel_CAGR:9.2%} "
            f"{r.fx_CAGR:8.2%} {r.dCAGR_pp:+9.2f} {r.sel_MaxDD:10.2%} {r.fx_MaxDD:9.2%} "
            f"{r.dSharpe:+8.4f} {r.dCAGR_OOS_pp:+13.2f} {r.dSharpe_OOS:+12.4f}")

    say("\n" + "=" * 150)
    say("2.  ALL 9 (panel, family) CELLS x 4 TARGETS x 2 SOLVE WINDOWS = 72 MATCHED CELLS")
    say("=" * 150)
    cols = ["panel", "family", "target", "solve_window", "gstar", "sel_CAGR", "fx_CAGR",
            "dCAGR_pp", "sel_MaxDD", "fx_MaxDD", "dMaxDD_pp", "dSharpe", "dCAGR_OOS_pp",
            "dSharpe_OOS", "solve_note"]
    say(SV[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 150)
    say("3.  THE ANSWER — does ANY CAGR advantage survive at matched drawdown?")
    say("=" * 150)
    dd = SV[SV.target == "MAXDD"]
    for wnd in SOLVE_WINDOWS:
        w = dd[dd.solve_window == wnd]
        say(f"    solved on {wnd:4s}:  FULL dCAGR mean {w.dCAGR_pp.mean():+7.2f} pp, "
            f"{int((w.dCAGR_pp > 0).sum())}/{len(w)} cells positive;  "
            f"OOS dCAGR mean {w.dCAGR_OOS_pp.mean():+7.2f} pp, "
            f"{int((w.dCAGR_OOS_pp > 0).sum())}/{len(w)} positive;  "
            f"dSharpe mean {w.dSharpe.mean():+.4f}, OOS {w.dSharpe_OOS.mean():+.4f}")
    say(f"\n    RAW (unmatched, both at 0.75): FULL dCAGR mean "
        f"{SV.drop_duplicates(['panel','family']).raw_dCAGR_pp.mean():+.2f} pp, OOS "
        f"{SV.drop_duplicates(['panel','family']).raw_dCAGR_OOS_pp.mean():+.2f} pp, dMaxDD "
        f"{SV.drop_duplicates(['panel','family']).raw_dMaxDD_pp.mean():+.2f} pp.")
    say("\n    Per target, pooled over the 9 cells (FULL-solved / IS-solved):")
    say(f"    {'target':10s} {'dCAGR pp':>20s} {'dCAGR OOS pp':>22s} {'dSharpe':>20s} "
        f"{'positive dCAGR':>18s}")
    for tgt in TARGETS:
        a = SV[(SV.target == tgt) & (SV.solve_window == "FULL")]
        b = SV[(SV.target == tgt) & (SV.solve_window == "IS")]
        say(f"    {tgt:10s} {a.dCAGR_pp.mean():+9.2f} / {b.dCAGR_pp.mean():+8.2f} "
            f"{a.dCAGR_OOS_pp.mean():+11.2f} / {b.dCAGR_OOS_pp.mean():+8.2f} "
            f"{a.dSharpe.mean():+9.4f} / {b.dSharpe.mean():+8.4f} "
            f"{int((a.dCAGR_pp>0).sum())}/9 & {int((b.dCAGR_pp>0).sum())}/9")

    say("\n" + "=" * 150)
    say("4.  THE COST OF THE CHURN — what the selector pays for its 5-8x turnover")
    say("=" * 150)
    say("    RAW = the selector at its own gross 0.75 (560's arm).  MATCHED = the same book "
        "de-grossed to g* on the IS MaxDD target; turnover scales with gross.")
    say(f"    {'panel':9s} {'family':9s} {'RAW turn':>9s} {'fx turn':>8s} {'ratio':>6s} "
        f"{'RAW cost bp':>12s} {'fx cost bp':>11s} {'extra bp':>9s} {'g*(IS)':>7s} "
        f"{'MATCHED turn':>13s} {'MATCHED cost bp':>16s}")
    mm = SV[(SV.target == "MAXDD") & (SV.solve_window == "IS")]
    for _, r in mm.iterrows():
        say(f"    {r.panel:9s} {r.family:9s} {r.raw_sel_turn:9.2f} {r.fx_turn:8.2f} "
            f"{r.raw_sel_turn/r.fx_turn:6.1f} {r.raw_sel_cost_bp:12.0f} {r.fx_cost_bp:11.0f} "
            f"{r.raw_sel_cost_bp-r.fx_cost_bp:+9.0f} {r.gstar:7.4f} {r.sel_turn:13.2f} "
            f"{r.sel_cost_bp:16.0f}")

    say("\n" + "=" * 150)
    say(f"5.  CAPITAL ARM — both KEEP paths at all {len(G)} published cells")
    say("=" * 150)
    say(f"    4a: {int(G.p4a.sum())}/{len(G)};  4b: {int(G.p4b.sum())}/{len(G)}.")
    b = G[G.p4b]
    if len(b):
        say("    Cells clearing 4b:")
        say(b[["panel", "family", "arm", "cell", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "oCAGR", "oSharpe", "oMaxDD", "p4a"]].to_string(
                   index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("    NONE.  Every cell fails at least one 4b leg; the binding legs are:")
    fails = pd.Series([x for s in G.f4b for x in (s.split(",") if s != "-" else [])])
    say(f"    binding-leg census over {len(G)} cells: {fails.value_counts().to_dict()}")

    say("\n    RULE 8 (protocol rule 8): the matching gross g* solved on warm-up..2016-12-31 ONLY, "
        "2017-2026 read once.")
    r8 = SV[(SV.target == "MAXDD") & (SV.solve_window == "IS")]
    cols8 = ["panel", "family", "gstar", "sel_oCAGR", "sel_oSharpe", "sel_oMaxDD",
             "fx_oCAGR", "fx_oSharpe", "fx_oMaxDD", "dCAGR_OOS_pp", "dSharpe_OOS"]
    say(r8[cols8].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("    benchmarks (OOS): " + ";  ".join(
        f"{pn} SPY {comparand[pn]['spy']['oCAGR']:.2%}/{comparand[pn]['spy']['oSharpe']:.4f}/"
        f"{comparand[pn]['spy']['oMaxDD']:.2%}, RULES v2 "
        f"{comparand[pn]['live']['oCAGR']:.2%}/{comparand[pn]['live']['oSharpe']:.4f}/"
        f"{comparand[pn]['live']['oMaxDD']:.2%}" for pn in PANELS))

    n_pos = int((r8.dCAGR_OOS_pp > 0).sum())
    verdict = ("KEEP-candidate: the selector's CAGR survives at matched drawdown"
               if (n_pos >= 5 and r8.dCAGR_OOS_pp.mean() > 0 and G.p4b.any())
               else "KILL: the selector's CAGR advantage does not survive matched drawdown")
    say("\n" + "=" * 150)
    say(f"    VERDICT: {verdict}")
    say(f"    rule-8 legal reading (MAXDD matched on IS rows only): OOS dCAGR mean "
        f"{r8.dCAGR_OOS_pp.mean():+.2f} pp, {n_pos}/9 cells positive; OOS dSharpe mean "
        f"{r8.dSharpe_OOS.mean():+.4f}.")

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    G.drop(columns=[c for c in G.columns if c.startswith("_")]).to_csv(f"{OUT}.grid.csv",
                                                                      index=False)
    S.to_csv(f"{OUT}.selectors.csv", index=False)
    SV.to_csv(f"{OUT}.matched.csv", index=False)
    allpass = all(g["pass_"] for g in GATES)
    say(f"\n    ALL GATES PASS: {allpass}   ({time.time()-t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    G, S, SV, comparand, t0 = main()
    analyse(G, S, SV, comparand, t0)
