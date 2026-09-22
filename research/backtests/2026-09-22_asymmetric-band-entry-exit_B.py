#!/usr/bin/env python3
"""Idea 2241 (lane B, 2026-09-22): does an ASYMMETRIC 200d BAND clear 4b where the
SYMMETRIC one cannot?

RULES v2 clause 2 uses ONE constant for both edges of the 200d band (+/-3%).  This script
splits it into two:

    IN   when  px >  ma * (1 + b_in)     (ENTRY LAG: confirmation demanded before paying
                                          for exposure)
    OUT  when  px <  ma * (1 - b_out)    (EXIT PATIENCE: how much of the unused drawdown
                                          budget the book spends holding through a dip)
    else previous state; OUT before 200 closes exist.

b_in = b_out = 0.03 is exactly the live book (gate G1).  Sizing, cadence and gross are the
live ones and are NOT tuned: gross = 0.75 / N over names priced that day, weekly.

TUNED PARAMETERS: exactly two, b_in and b_out.
REPORTED, NEVER SELECTED: cost rung {0, 5, 10, 25, 50} bps, panel {U56, B136}, cadence W.

Deliverables (PROTOCOL rules 3, 4, 5, 8, 9):
  * every grid point published, both KEEP paths (4a and 4b), at every cost rung;
  * rule-8 walk-forward: parameters chosen on 2009-2016 IS ONLY, 2017-2026 read once;
  * comparands = live RULES v2 baseline and SPY buy-and-hold, identical windows/costs.

Run:  python3 research/backtests/2026-09-22_asymmetric-band-entry-exit_B.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics                              # noqa: E402

STEM = Path(__file__).with_suffix("")
GROSS = 0.75                      # live RULES v2 sizing, not tuned
FREQ = "W"                        # live cadence, not tuned
COSTS = [0, 5, 10, 25, 50]        # 10 bps is the PROTOCOL rung; the rest are reported
B_IN = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08]
B_OUT = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
IS_END = "2016-12-31"             # rule 8: parameters chosen on 2009-2016 only
OOS_START = "2017-01-01"

_log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s); _log_lines.append(s)


# ----------------------------------------------------------------------------- mechanics
def asym_band_state(px: pd.DataFrame, b_in: float, b_out: float) -> pd.DataFrame:
    """RULES v2 clause 2 with the two edges separated.  b_in = b_out reproduces band_state."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b_in), 1.0).mask(px < ma * (1 - b_out), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def asym_weights(px: pd.DataFrame, b_in: float, b_out: float, gross: float = GROSS) -> pd.DataFrame:
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(asym_band_state(px, b_in, b_out), 0.0)


def gross_returns(px: pd.DataFrame, w: pd.DataFrame):
    """One engine.backtest pass; returns the COST-FREE return line plus turnover, so every
    cost rung is a pure subtraction (held weights do not depend on cost_bps)."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"], res["weights"]


def net(r0: pd.Series, to: pd.Series, bps: float) -> pd.Series:
    return r0 - to * bps / 1e4


def win(s: pd.Series, kind: str, start) -> pd.Series:
    s = s.loc[start:]
    if kind == "FULL": return s
    if kind == "H1":   return s.iloc[: len(s) // 2]
    if kind == "H2":   return s.iloc[len(s) // 2:]
    if kind == "IS":   return s.loc[:IS_END]
    if kind == "OOS":  return s.loc[OOS_START:]
    raise ValueError(kind)


def stats(s: pd.Series) -> dict:
    m = metrics(s)
    return {"CAGR": m["CAGR"], "Sharpe": m["Sharpe"], "MaxDD": m["MaxDD"]}


# ------------------------------------------------------------------------------ the grid
def run_panel(panel: str, px: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    start = px.index[260]                                    # same warm-up skip as compare()
    log(f"\n=== PANEL {panel}: {px.shape[1]} names, {px.index[0].date()} -> {px.index[-1].date()}, "
        f"scored from {start.date()} ===")

    b0, t0, _ = gross_returns(px, rules_v2_weights(px, band=0.03, gross=GROSS))
    spy = px["SPY"].pct_change().fillna(0.0)

    # ---- gates
    gates = []
    g1 = float(np.abs(asym_weights(px, 0.03, 0.03) - rules_v2_weights(px, 0.03, GROSS)).max().max())
    gates.append(("G1 b_in=b_out=0.03 reproduces baseline.rules_v2_weights (max |dw|)", g1, g1 == 0.0))
    g2 = float(np.abs(asym_band_state(px, 0.03, 0.03).astype(float)
                      - band_state(px, 0.03).astype(float)).max().max())
    gates.append(("G2 asym_band_state == baseline.band_state at b_in=b_out (max |ds|)", g2, g2 == 0.0))
    rb = net(b0, t0, 10.0)
    ra = net(*gross_returns(px, asym_weights(px, 0.03, 0.03))[:2], 10.0)
    g3 = float(np.abs(win(ra, "FULL", start) - win(rb, "FULL", start)).max())
    gates.append(("G3 asym return line == baseline return line at b_in=b_out=0.03, 10 bps", g3, g3 < 1e-15))
    # monotonicity sanity: looser band (lower b_in, higher b_out) must not REDUCE exposure
    ex_tight = asym_weights(px, 0.08, 0.00).sum(axis=1).loc[start:].mean()
    ex_loose = asym_weights(px, 0.00, 0.12).sum(axis=1).loc[start:].mean()
    gates.append(("G4 mean exposure loose(0.00/0.12) > tight(0.08/0.00)",
                  f"{ex_loose:.4f} > {ex_tight:.4f}", ex_loose > ex_tight))
    g5 = float(np.abs(t0.loc[start:]).sum())
    gates.append(("G5 baseline turnover is non-degenerate (sum |turnover| > 0)", g5, g5 > 0))

    # ---- comparand statistics, one per cost rung / window
    comp = {}
    for c in COSTS:
        rbc = net(b0, t0, c)
        for w in ("FULL", "H1", "H2", "IS", "OOS"):
            comp[("BASE", c, w)] = stats(win(rbc, w, start))
            comp[("SPY", c, w)] = stats(win(spy, w, start))   # SPY is buy-and-hold: no cost rung

    rows = []
    for bi in B_IN:
        for bo in B_OUT:
            w = asym_weights(px, bi, bo)
            r0, to, held = gross_returns(px, w)
            expo = held.sum(axis=1).loc[start:].mean()
            ann_to = to.loc[start:].sum() / (len(to.loc[start:]) / 252)
            for c in COSTS:
                rc = net(r0, to, c)
                s = {k: stats(win(rc, k, start)) for k in ("FULL", "H1", "H2", "IS", "OOS")}
                B = {k: comp[("BASE", c, k)] for k in s}
                S = {k: comp[("SPY", c, k)] for k in s}
                # ---- KEEP path 4a: beat the live book in BOTH halves, MaxDD no worse
                a1 = s["H1"]["Sharpe"] > B["H1"]["Sharpe"]
                a2 = s["H2"]["Sharpe"] > B["H2"]["Sharpe"]
                a3 = s["FULL"]["MaxDD"] >= B["FULL"]["MaxDD"]
                # ---- KEEP path 4b: beat SPY in both halves AND OOS, DD <= 60% SPY, CAGR >= 70% SPY
                b1 = s["H1"]["Sharpe"] > S["H1"]["Sharpe"]
                b2 = s["H2"]["Sharpe"] > S["H2"]["Sharpe"]
                b3 = s["OOS"]["Sharpe"] > S["OOS"]["Sharpe"]
                bF_dd = s["FULL"]["MaxDD"] >= 0.60 * S["FULL"]["MaxDD"]
                bF_cg = s["FULL"]["CAGR"] >= 0.70 * S["FULL"]["CAGR"]
                bO_dd = s["OOS"]["MaxDD"] >= 0.60 * S["OOS"]["MaxDD"]
                bO_cg = s["OOS"]["CAGR"] >= 0.70 * S["OOS"]["CAGR"]
                row = dict(panel=panel, b_in=bi, b_out=bo, cost_bps=c,
                           mean_exposure=expo, ann_turnover=ann_to)
                for k in ("FULL", "H1", "H2", "IS", "OOS"):
                    row[f"CAGR_{k}"] = s[k]["CAGR"]; row[f"Sharpe_{k}"] = s[k]["Sharpe"]
                    row[f"MaxDD_{k}"] = s[k]["MaxDD"]
                row.update(a_H1=a1, a_H2=a2, a_DD=a3, pass4a=bool(a1 and a2 and a3),
                           b_H1=b1, b_H2=b2, b_OOS=b3,
                           bF_DD=bF_dd, bF_CAGR=bF_cg, bO_DD=bO_dd, bO_CAGR=bO_cg,
                           pass4b_FULL=bool(b1 and b2 and b3 and bF_dd and bF_cg),
                           pass4b_OOS=bool(b1 and b2 and b3 and bO_dd and bO_cg))
                rows.append(row)
        log(f"  b_in={bi:.2f} done ({len(rows)} rows)")

    grid = pd.DataFrame(rows)
    ref = {(k, c, w): v for (k, c, w), v in comp.items()}
    return grid, ref


# --------------------------------------------------------------------------------- main
def main():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    grids, refs, all_gates = [], {}, []
    for name, px in panels.items():
        g, ref = run_panel(name, px)
        grids.append(g); refs[name] = ref
    grid = pd.concat(grids, ignore_index=True)
    grid.to_csv(f"{STEM}.grid.csv", index=False)

    # ------------------------------------------------------------------ gates (re-run, logged)
    gate_rows = []
    for name, px in panels.items():
        start = px.index[260]
        g1 = float(np.abs(asym_weights(px, 0.03, 0.03) - rules_v2_weights(px, 0.03, GROSS)).max().max())
        g2 = float(np.abs(asym_band_state(px, 0.03, 0.03).astype(float)
                          - band_state(px, 0.03).astype(float)).max().max())
        b0, t0, _ = gross_returns(px, rules_v2_weights(px, band=0.03, gross=GROSS))
        r0, ta, _ = gross_returns(px, asym_weights(px, 0.03, 0.03))
        g3 = float(np.abs(net(r0, ta, 10.0).loc[start:] - net(b0, t0, 10.0).loc[start:]).max())
        ex_t = asym_weights(px, 0.08, 0.00).sum(axis=1).loc[start:].mean()
        ex_l = asym_weights(px, 0.00, 0.12).sum(axis=1).loc[start:].mean()
        sub = grid[(grid.panel == name) & (grid.cost_bps == 10)]
        base_row = sub[(sub.b_in == 0.03) & (sub.b_out == 0.03)].iloc[0]
        bstat = refs[name][("BASE", 10, "FULL")]
        g6 = abs(base_row.Sharpe_FULL - bstat["Sharpe"])
        for k, v, ok in [
            ("G1 b_in=b_out=0.03 == rules_v2_weights (max |dw|)", g1, g1 == 0.0),
            ("G2 asym_band_state == band_state at b_in=b_out (max |ds|)", g2, g2 == 0.0),
            ("G3 return line identical at b_in=b_out=0.03, 10 bps (max |dr|)", g3, g3 < 1e-15),
            ("G4 exposure loose(0.00/0.12) > tight(0.08/0.00)", f"{ex_l:.4f} vs {ex_t:.4f}", ex_l > ex_t),
            ("G5 grid's own 0.03/0.03 cell == comparand baseline Sharpe (FULL)", g6, g6 < 1e-12),
            ("G6 grid is complete (42 cells x 5 cost rungs)", len(sub) * len(COSTS),
             len(grid[grid.panel == name]) == len(B_IN) * len(B_OUT) * len(COSTS)),
        ]:
            gate_rows.append(dict(panel=name, gate=k, value=v, PASS=bool(ok)))
    gates = pd.DataFrame(gate_rows)
    gates.to_csv(f"{STEM}.gates.csv", index=False)
    log("\n=== GATES ===")
    log(gates.to_string(index=False))
    log(f"GATES: {int(gates.PASS.sum())} of {len(gates)} PASS")

    # ------------------------------------------------------- comparands, published in full
    log("\n=== COMPARANDS (identical windows, identical cost rungs; SPY is buy-and-hold) ===")
    crows = []
    for p in panels:
        for k in ("BASE", "SPY"):
            for c in COSTS:
                for w in ("FULL", "H1", "H2", "IS", "OOS"):
                    d = refs[p][(k, c, w)]
                    crows.append(dict(panel=p, comparand=k, cost_bps=c, window=w, **d))
    comp = pd.DataFrame(crows)
    comp.to_csv(f"{STEM}.comparands.csv", index=False)
    log(comp[(comp.cost_bps == 10) & (comp.window.isin(["FULL", "H1", "H2", "IS", "OOS"]))]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------- rule 8 walk-forward
    log("\n=== RULE 8 WALK-FORWARD (parameters from 2009-2016 IS ONLY; 2017-2026 read once) ===")
    wf = []
    for p in panels:
        for c in COSTS:
            sub = grid[(grid.panel == p) & (grid.cost_bps == c)].copy()
            choosers = {
                "C_IS_SHARPE": sub.sort_values("Sharpe_IS", ascending=False).iloc[0],
                "C_ZERO_PARAM_live": sub[(sub.b_in == 0.03) & (sub.b_out == 0.03)].iloc[0],
            }
            # IS-legal 4a / 4b filters: judged on the IS window only
            isb = sub[(sub.Sharpe_IS > 0)]
            is4a = sub[sub.apply(lambda r: r.Sharpe_IS > refs[p][("BASE", c, "IS")]["Sharpe"]
                                 and r.MaxDD_IS >= refs[p][("BASE", c, "IS")]["MaxDD"], axis=1)]
            is4b = sub[sub.apply(lambda r: r.Sharpe_IS > refs[p][("SPY", c, "IS")]["Sharpe"]
                                 and r.MaxDD_IS >= 0.60 * refs[p][("SPY", c, "IS")]["MaxDD"]
                                 and r.CAGR_IS >= 0.70 * refs[p][("SPY", c, "IS")]["CAGR"], axis=1)]
            if len(is4a): choosers["C_IS_SHARPE_among_IS4a"] = is4a.sort_values("Sharpe_IS", ascending=False).iloc[0]
            if len(is4b): choosers["C_IS_SHARPE_among_IS4b"] = is4b.sort_values("Sharpe_IS", ascending=False).iloc[0]
            _ = isb
            for cname, r in choosers.items():
                B = refs[p][("BASE", c, "OOS")]; S = refs[p][("SPY", c, "OOS")]
                wf.append(dict(panel=p, cost_bps=c, chooser=cname, b_in=r.b_in, b_out=r.b_out,
                               n_IS4a=len(is4a), n_IS4b=len(is4b),
                               Sharpe_IS=r.Sharpe_IS, CAGR_OOS=r.CAGR_OOS, Sharpe_OOS=r.Sharpe_OOS,
                               MaxDD_OOS=r.MaxDD_OOS,
                               BASE_CAGR_OOS=B["CAGR"], BASE_Sharpe_OOS=B["Sharpe"], BASE_MaxDD_OOS=B["MaxDD"],
                               SPY_CAGR_OOS=S["CAGR"], SPY_Sharpe_OOS=S["Sharpe"], SPY_MaxDD_OOS=S["MaxDD"],
                               beats_base_OOS_Sharpe=bool(r.Sharpe_OOS > B["Sharpe"]),
                               beats_SPY_OOS_Sharpe=bool(r.Sharpe_OOS > S["Sharpe"]),
                               OOS_DDcap=bool(r.MaxDD_OOS >= 0.60 * S["MaxDD"]),
                               OOS_CAGRfloor=bool(r.CAGR_OOS >= 0.70 * S["CAGR"]),
                               pass4a=bool(r.pass4a), pass4b_FULL=bool(r.pass4b_FULL),
                               pass4b_OOS=bool(r.pass4b_OOS)))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{STEM}.walkforward.csv", index=False)
    log(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------------ verdicts
    log("\n=== KEEP-PATH COUNTS over the published grid (42 cells x 5 cost rungs x 2 panels) ===")
    for p in panels:
        s = grid[grid.panel == p]
        log(f"{p}: 4a {int(s.pass4a.sum())}/{len(s)}   4b_FULL {int(s.pass4b_FULL.sum())}/{len(s)}   "
            f"4b_OOS {int(s.pass4b_OOS.sum())}/{len(s)}")
        for c in COSTS:
            sc = s[s.cost_bps == c]
            log(f"   {c:>2} bps: 4a {int(sc.pass4a.sum()):>2}/42  4b_FULL {int(sc.pass4b_FULL.sum()):>2}/42  "
                f"4b_OOS {int(sc.pass4b_OOS.sum()):>2}/42")

    log("\n=== WHICH 4b LEG BINDS (10 bps, FULL-window legs, over all 42 cells x 2 panels) ===")
    s10 = grid[grid.cost_bps == 10]
    fails = s10[~s10.pass4b_FULL]
    for leg in ("b_H1", "b_H2", "b_OOS", "bF_DD", "bF_CAGR"):
        log(f"   {leg:<8} fails in {int((~fails[leg]).sum()):>3} of {len(fails)} 4b_FULL-fail rows "
            f"({(~fails[leg]).mean():.1%})")

    log("\n=== THE LIVE CELL vs THE BEST CELL ON EACH AXIS (10 bps, FULL) ===")
    for p in panels:
        s = grid[(grid.panel == p) & (grid.cost_bps == 10)]
        live = s[(s.b_in == 0.03) & (s.b_out == 0.03)].iloc[0]
        bc = s.sort_values("CAGR_FULL", ascending=False).iloc[0]
        bs = s.sort_values("Sharpe_FULL", ascending=False).iloc[0]
        log(f"{p} LIVE  b_in=0.03 b_out=0.03: CAGR {live.CAGR_FULL:.2%} Sharpe {live.Sharpe_FULL:.4f} "
            f"MaxDD {live.MaxDD_FULL:.2%} expo {live.mean_exposure:.3f} turn {live.ann_turnover:.2f}/yr")
        log(f"{p} maxCAGR b_in={bc.b_in:.2f} b_out={bc.b_out:.2f}: CAGR {bc.CAGR_FULL:.2%} "
            f"Sharpe {bc.Sharpe_FULL:.4f} MaxDD {bc.MaxDD_FULL:.2%} expo {bc.mean_exposure:.3f} "
            f"turn {bc.ann_turnover:.2f}/yr")
        log(f"{p} maxSharpe b_in={bs.b_in:.2f} b_out={bs.b_out:.2f}: CAGR {bs.CAGR_FULL:.2%} "
            f"Sharpe {bs.Sharpe_FULL:.4f} MaxDD {bs.MaxDD_FULL:.2%} expo {bs.mean_exposure:.3f} "
            f"turn {bs.ann_turnover:.2f}/yr")
        S = refs[p][("SPY", 10, "FULL")]
        log(f"{p} 4b bars FULL: CAGR floor {0.70 * S['CAGR']:.2%}, DD cap {0.60 * S['MaxDD']:.2%}, "
            f"SPY Sharpe {S['Sharpe']:.4f}")

    Path(f"{STEM}.log.txt").write_text("\n".join(_log_lines) + "\n")
    print(f"\nwrote {STEM}.grid.csv / .comparands.csv / .walkforward.csv / .gates.csv / .log.txt")


if __name__ == "__main__":
    main()
