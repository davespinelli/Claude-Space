#!/usr/bin/env python3
"""Idea 787 (lane B, 2026-09-11) — does ANY standing 4b candidate clear an EQUAL-WEIGHT bar?

Idea 742 priced ONE standing 4b candidate (the RULES v2 band book at gross 1.00) against an
equal-weight basket of its own panel and found its 4b pass is a COMPARAND fact: it survives 0 of 9
equal-weight cells, and the leg that binds is the CAGR FLOOR (U56 -1.00 pp/yr full, -0.35 pp OOS).

That is a one-book result, and it is the WEAKEST possible test of the shelf: the band book is a
de-grossing book whose Sharpe is flat in gross and whose whole CAGR case is cash weight. The
record's OTHER standing memo candidates are RETURN books (the U56 QUANTILE-50 RESPREAD memo runs
15.47% CAGR against the band book's 11.55%), and the CAGR floor is exactly the leg they might
clear. So this run re-prices the WHOLE standing shelf, as families, against BOTH bars.

Two tuned parameters, every grid point reported: (dial, panel). The FAMILY axis is a structural
enumeration of the record's committed memos, not a tuned dimension; the six families are named in
the header of FAMILIES below with the memo each comes from.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine applies weights at t+1), no
shorting, no leverage (gross <= 1.00), warm-up skip of 260 rows, rule 8 walk-forward throughout
(dial picked on IS <= 2016-12-31 alone, 2017-01-01 -> end read once), both KEEP paths evaluated.

FRAME: SPY is held OUT of every book and every bar as a pure benchmark column (memo line 9c's
"SPY-free frame"); it is the convention the standing memo's published digits reproduce under.

BARS (three, all reported): B_SPY (the PROTOCOL 4b comparand), B_EW742 (idea 742's own bar:
equal-weight the panel's tradables, DAILY rebalance, 0 bps) and B_EWW10 (the same basket at the
books' own cadence and cost: WEEKLY, 10 bps). B_EWW10 is the WEAKER of the two equal-weight bars on
both panels, so any KILL stated against it is the conservative statement.

Outputs (all beside this script):
  *.grid.csv         one row per (panel, family, dial): full/halves/OOS metrics + both 4b verdicts
  *.bars.csv         the two bars per panel, full/halves/OOS
  *.walkforward.csv  the rule-8 pick per (panel, family) and its untouched OOS read
  *.keeppaths.csv    4a and 4b(SPY) and 4b(EW) verdicts per cell with the binding leg named
  *.gates.csv        the six pre-registered gates
  *.result.md        the answer
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa: E402

HERE = Path(__file__).resolve().parent
STEM = Path(__file__).stem
COST = 10.0
WARMUP = 260
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
GROSS_LADDER = [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]


# ---------------------------------------------------------------- fast backtester (gated vs engine)
def fast_backtest(px: pd.DataFrame, w: pd.DataFrame, cost_bps=COST, freq="W") -> dict:
    """Numpy transcription of engine.backtest. Same drift, same t+1, same cost model."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    held = np.zeros_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(px.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index)}


# ---------------------------------------------------------------- book constructors
def _priced(px):
    return px.notna().astype(float)


def _respread(mask_df: pd.DataFrame, gross: float) -> pd.DataFrame:
    m = mask_df.astype(float)
    return gross * m.div(m.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ma_dist(px):
    return px / px.rolling(200).mean() - 1.0


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def b_band_dg(px, g):
    """RULES v2 exactly: band gate, g/N over ALL priced names, gated weight -> CASH."""
    e = _priced(px)
    ew = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, 0.03), 0.0)


def b_band_resp(px, g):
    """Same gate, gross RESPREAD over the IN names (idea 81's different, unpriced book)."""
    return _respread(band_state(px, 0.03), g)


def b_quant_resp(px, q):
    """Memo 2026-09-11_u56-quantile50-respread-M: top q by close/MA200-1, respread at 0.75."""
    d = ma_dist(px)
    r = d.rank(axis=1, pct=True, ascending=False)
    sel = (r <= q) & d.notna()
    return _respread(sel, 0.75)


def b_topn_resp(px, n):
    """Memos 2026-09-07 u56-top20-*: RULES v1 eligibility, top n by MA distance, respread 0.75."""
    d = ma_dist(px)
    elig = d.where((px > px.rolling(200).mean()) & (vol20(px) < 0.60))
    sel = elig.rank(axis=1, ascending=False) <= n
    return _respread(sel, 0.75)


def b_ewelig(px, g):
    """2026-09-03 RECOMMENDATION Finding 2 / memo 2026-09-07_eligible-equal-weight-v2:
    equal-weight EVERY eligible name (above 200d, vol20 < 0.60) at gross g, respread."""
    sel = (px > px.rolling(200).mean()) & (vol20(px) < 0.60) & px.notna()
    return _respread(sel, g)


def b_magate_full(px, g):
    """Memo 2026-09-08_u56-ewall-magate-fullgross: plain 200d gate, no vol filter, respread g."""
    sel = (px > px.rolling(200).mean()) & px.notna()
    return _respread(sel, g)


def b_ewbar(px, g=1.00):
    """B_EW — idea 742's bar: equal-weight the panel's own tradables, weekly, gross 1.00, 10 bps."""
    return _respread(px.notna(), g)


FAMILIES = [
    # (name, builder, dial values, cadence, memo source)
    ("BAND-DG",    b_band_dg,    GROSS_LADDER,                         "W", "2026-09-10/11 rules-v2-at-gross-1.00 (the standing candidate; g=0.75 is the LIVE book)"),
    ("BAND-RESP",  b_band_resp,  GROSS_LADDER,                         "W", "idea 81's respread variant of the same gate"),
    ("QUANT-RESP", b_quant_resp, [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80], "M", "2026-09-11_u56-quantile50-respread-M_4b_B_MEMO"),
    ("TOPN-RESP",  b_topn_resp,  [5, 10, 15, 20, 30, 40],              "W", "2026-09-07_u56-top20-g075-4b_C / u56-top20-band-m20_4b_B"),
    ("EWELIG",     b_ewelig,     GROSS_LADDER,                         "W", "2026-09-03 RECOMMENDATION Finding 2 / 2026-09-07_eligible-equal-weight-v2_B"),
    ("MAGATE",     b_magate_full, GROSS_LADDER,                        "W", "2026-09-08_u56-ewall-magate-fullgross_KEEP_MEMO"),
]


# ---------------------------------------------------------------- metric helpers
def triple(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = triple(r)
    return dict(CAGR=c, Sharpe=s, MaxDD=d,
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def oos_row(r):
    o = r.loc[OOS_START:]
    c, s, d = triple(o)
    return dict(oos_CAGR=c, oos_Sharpe=s, oos_MaxDD=d)


def is_sharpe(r):
    return metrics(r.loc[:IS_END])["Sharpe"]


def path_4a(cand, base):
    """PROTOCOL 4a: Sharpe > live rules in BOTH halves AND MaxDD no worse."""
    legs = {"H1": cand["H1"] > base["H1"], "H2": cand["H2"] > base["H2"],
            "MaxDD": cand["MaxDD"] >= base["MaxDD"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


def path_4b(cand, bar):
    """PROTOCOL 4b: Sharpe > bar in BOTH halves AND OOS, MaxDD <= 60% of bar's, CAGR >= 70%."""
    legs = {"H1": cand["H1"] > bar["H1"],
            "H2": cand["H2"] > bar["H2"],
            "OOS": cand["oos_Sharpe"] > bar["oos_Sharpe"],
            "DD": cand["MaxDD"] >= 0.60 * bar["MaxDD"],
            "CAGR": cand["CAGR"] >= 0.70 * bar["CAGR"]}
    return all(legs.values()), ",".join(k for k, v in legs.items() if not v)


# ---------------------------------------------------------------- run
def panel(broad):
    px = load_universe(broad=broad)
    tradables = [c for c in px.columns if c != "SPY"]
    frame = px[tradables].copy()
    start = px.index[WARMUP]
    return px, frame, start


def scored(res, start):
    return res["returns"].loc[start:]


def main():
    gates, grid, bars_rows, wf_rows, keep_rows = [], [], [], [], []

    for broad in (False, True):
        pname = "B136" if broad else "U56"
        px, frame, start = panel(broad)
        print(f"\n=== {pname}: {frame.shape[1]} tradables, {px.index[0].date()}..{px.index[-1].date()}, "
              f"scored from {start.date()}")

        # -------- gates (U56 only for the reproduction ones; G1/G6 on both panels)
        if not broad:
            # G2: b_band_dg(0.75) IS baseline.rules_v2_weights on the full frame
            g2 = float(np.nanmax(np.abs(
                b_band_dg(px, 0.75).values - rules_v2_weights(px).values)))
            gates.append(dict(gate="G2 b_band_dg(0.75) == baseline.rules_v2_weights (full frame)",
                              value=g2, bar=0.0, passed=g2 == 0.0))

        # G1: fast_backtest vs engine.backtest on real books, returns AND turnover
        for nm, w, fq in [("BAND-DG g0.75", b_band_dg(frame, 0.75), "W"),
                          ("QUANT-RESP q0.50", b_quant_resp(frame, 0.50), "M"),
                          ("EWELIG g0.75", b_ewelig(frame, 0.75), "W")]:
            f = fast_backtest(frame, w, COST, fq)
            e = engine_backtest(frame, w, cost_bps=COST, freq=fq)
            dr = float(np.nanmax(np.abs(f["returns"].values - e["returns"].values)))
            dt_ = float(np.nanmax(np.abs(f["turnover"].values - e["turnover"].values)))
            gates.append(dict(gate=f"G1 {pname} fast vs engine [{nm}] max|dr| / max|dturn|",
                              value=max(dr, dt_), bar=1e-12, passed=max(dr, dt_) < 1e-12))

        # G6: cost-rung identity r(25) = r(0) - turnover*25/1e4
        w0 = b_band_dg(frame, 0.75)
        r0 = fast_backtest(frame, w0, 0.0, "W")
        r25 = fast_backtest(frame, w0, 25.0, "W")
        d6 = float(np.nanmax(np.abs(
            (r0["returns"] - r0["turnover"] * 25 / 1e4 - r25["returns"]).values)))
        gates.append(dict(gate=f"G6 {pname} cost-rung identity r(25)=r(0)-turn*25/1e4",
                          value=d6, bar=1e-12, passed=d6 < 1e-12))

        # -------- the two bars
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        ewb = b_ewbar(frame, 1.00)
        ew742_r = scored(fast_backtest(frame, ewb, 0.0, "D"), start)     # idea 742's B_EW
        eww10_r = scored(fast_backtest(frame, ewb, COST, "W"), start)    # cost/cadence-matched
        bar_defs = {"B_SPY": spy_r, "B_EW742": ew742_r, "B_EWW10": eww10_r}
        bars = {}
        for bn, br in bar_defs.items():
            row = {**full_row(br), **oos_row(br)}
            bars[bn] = row
            bars_rows.append(dict(panel=pname, bar=bn, **row))
            print(f"  bar {bn:6s} CAGR {row['CAGR']:7.2%} Sharpe {row['Sharpe']:.4f} "
                  f"MaxDD {row['MaxDD']:7.2%} halves {row['H1']:.4f}/{row['H2']:.4f} "
                  f"| OOS {row['oos_CAGR']:7.2%} / {row['oos_Sharpe']:.4f} / {row['oos_MaxDD']:7.2%}")

        if not broad:
            # G3 PROTOCOL bar reproduction (idea 742's G2): U56 SPY b&h 15.11/0.8835/-33.72
            g3 = max(abs(bars["B_SPY"]["CAGR"] - 0.1511), abs(bars["B_SPY"]["Sharpe"] - 0.8835),
                     abs(bars["B_SPY"]["MaxDD"] + 0.3372))
            gates.append(dict(gate="G3 U56 SPY b&h == idea 742 (15.11% / 0.8835 / -33.72%)",
                              value=g3, bar=5e-4, passed=g3 < 5e-4))
            # G4 equal-weight bar reproduction (idea 742's own B_EW row: DAILY, 0 bps)
            b = bars["B_EW742"]
            g4 = max(abs(b["CAGR"] - 0.1794), abs(b["Sharpe"] - 1.1357), abs(b["MaxDD"] + 0.2887),
                     abs(b["H1"] - 1.2129), abs(b["H2"] - 1.0743),
                     abs(b["oos_CAGR"] - 0.1864), abs(b["oos_Sharpe"] - 1.1448))
            gates.append(dict(gate="G4 U56 B_EW742 == idea 742 (17.94% / 1.1357 / -28.87% / 1.2129 / "
                                   "1.0743 / OOS 18.64% / 1.1448)",
                              value=g4, bar=5e-4, passed=g4 < 5e-4))
            # G4b the two EW bars are distinct and B_EWW10 is the WEAKER (conservative) one
            g4b = bars["B_EW742"]["Sharpe"] - bars["B_EWW10"]["Sharpe"]
            gates.append(dict(gate="G4b U56 Sharpe(B_EW742) - Sharpe(B_EWW10) > 0 "
                                   "(the weekly/10bps bar is the weaker bar)",
                              value=g4b, bar=0.0, passed=g4b > 0.0))

        # -------- the live baseline (4a comparand): RULES v2 band, gross 0.75, weekly
        live_r = scored(fast_backtest(frame, b_band_dg(frame, 0.75), COST, "W"), start)
        live = {**full_row(live_r), **oos_row(live_r)}
        print(f"  LIVE   CAGR {live['CAGR']:7.2%} Sharpe {live['Sharpe']:.4f} "
              f"MaxDD {live['MaxDD']:7.2%} halves {live['H1']:.4f}/{live['H2']:.4f} "
              f"| OOS {live['oos_CAGR']:7.2%} / {live['oos_Sharpe']:.4f}")

        # -------- the grid
        for fam, fn, dials, freq, src in FAMILIES:
            cells = []
            for dv in dials:
                r = scored(fast_backtest(frame, fn(frame, dv), COST, freq), start)
                row = {**full_row(r), **oos_row(r)}
                row["IS_Sharpe"] = is_sharpe(r)
                ok4a, miss4a = path_4a(row, live)
                ok_spy, miss_spy = path_4b(row, bars["B_SPY"])
                ok_e742, miss_e742 = path_4b(row, bars["B_EW742"])
                ok_ew, miss_ew = path_4b(row, bars["B_EWW10"])
                cell = dict(panel=pname, family=fam, dial=dv, cadence=freq, **row,
                            p4a=ok4a, p4a_miss=miss4a,
                            p4b_SPY=ok_spy, p4b_SPY_miss=miss_spy,
                            p4b_EW742=ok_e742, p4b_EW742_miss=miss_e742,
                            p4b_EWW10=ok_ew, p4b_EWW10_miss=miss_ew, memo=src)
                cells.append(cell)
                grid.append(cell)
                keep_rows.append({k: cell[k] for k in
                                  ("panel", "family", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                   "oos_Sharpe", "p4a", "p4a_miss", "p4b_SPY", "p4b_SPY_miss",
                                   "p4b_EW742", "p4b_EW742_miss", "p4b_EWW10", "p4b_EWW10_miss")})
                print(f"  {fam:11s} {str(dv):>5s} CAGR {row['CAGR']:7.2%} Sh {row['Sharpe']:.4f} "
                      f"DD {row['MaxDD']:7.2%} h {row['H1']:.3f}/{row['H2']:.3f} "
                      f"OOS {row['oos_CAGR']:7.2%}/{row['oos_Sharpe']:.4f} "
                      f"| 4a {'P' if ok4a else '.':s} 4bSPY {'P' if ok_spy else '.':s}"
                      f"({miss_spy}) 4bEW742 {'P' if ok_e742 else '.':s}({miss_e742})"
                      f" 4bEWW10 {'P' if ok_ew else '.':s}({miss_ew})")

            # -------- rule 8: dial picked on IS Sharpe alone, OOS read once
            best = max(cells, key=lambda c: c["IS_Sharpe"])
            wf_rows.append(dict(panel=pname, family=fam, pick=best["dial"], cadence=freq,
                                IS_Sharpe=best["IS_Sharpe"],
                                oos_CAGR=best["oos_CAGR"], oos_Sharpe=best["oos_Sharpe"],
                                oos_MaxDD=best["oos_MaxDD"],
                                bar_SPY_oos_CAGR=bars["B_SPY"]["oos_CAGR"],
                                bar_SPY_oos_Sharpe=bars["B_SPY"]["oos_Sharpe"],
                                bar_EW742_oos_CAGR=bars["B_EW742"]["oos_CAGR"],
                                bar_EW742_oos_Sharpe=bars["B_EW742"]["oos_Sharpe"],
                                bar_EWW10_oos_CAGR=bars["B_EWW10"]["oos_CAGR"],
                                bar_EWW10_oos_Sharpe=bars["B_EWW10"]["oos_Sharpe"],
                                live_oos_CAGR=live["oos_CAGR"], live_oos_Sharpe=live["oos_Sharpe"],
                                p4b_SPY=best["p4b_SPY"], p4b_SPY_miss=best["p4b_SPY_miss"],
                                p4b_EW742=best["p4b_EW742"], p4b_EW742_miss=best["p4b_EW742_miss"],
                                p4b_EWW10=best["p4b_EWW10"], p4b_EWW10_miss=best["p4b_EWW10_miss"],
                                p4a=best["p4a"]))

        # G5 (U56 only): the standing candidate's own memo digits, BAND-DG g1.00
        if not broad:
            c = [g for g in grid if g["panel"] == "U56" and g["family"] == "BAND-DG"
                 and g["dial"] == 1.00][0]
            g5 = max(abs(c["CAGR"] - 0.1155), abs(c["Sharpe"] - 1.2067), abs(c["MaxDD"] + 0.1570),
                     abs(c["H1"] - 1.2405), abs(c["H2"] - 1.1798))
            gates.append(dict(gate="G5 U56 BAND-DG g1.00 == standing memo line 3 "
                                   "(11.55% / 1.2067 / -15.70% / 1.2405 / 1.1798)",
                              value=g5, bar=5e-4, passed=g5 < 5e-4))

    # ---------------------------------------------------------------- write
    G = pd.DataFrame(grid)
    B = pd.DataFrame(bars_rows)
    W = pd.DataFrame(wf_rows)
    K = pd.DataFrame(keep_rows)
    GT = pd.DataFrame(gates)
    G.to_csv(HERE / f"{STEM}.grid.csv", index=False)
    B.to_csv(HERE / f"{STEM}.bars.csv", index=False)
    W.to_csv(HERE / f"{STEM}.walkforward.csv", index=False)
    K.to_csv(HERE / f"{STEM}.keeppaths.csv", index=False)
    GT.to_csv(HERE / f"{STEM}.gates.csv", index=False)

    print("\n=== GATES")
    print(GT.to_string(index=False))
    print("\n=== HEADLINE")
    n = len(G)
    print(f"cells: {n}   4a pass: {int(G['p4a'].sum())}   "
          f"4b vs SPY: {int(G['p4b_SPY'].sum())}   "
          f"4b vs EW742: {int(G['p4b_EW742'].sum())}   "
          f"4b vs EWW10: {int(G['p4b_EWW10'].sum())}")
    both = G[G["p4b_SPY"] & (G["p4b_EW742"] | G["p4b_EWW10"])]
    print(f"pass SPY *and* either EW bar: {len(both)}")
    if len(both):
        print(both[["panel", "family", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                    "oos_CAGR", "oos_Sharpe"]].to_string(index=False))
    print("\n--- binding leg among the 4b-vs-SPY passers when re-scored on B_EWW10 (weaker EW bar)")
    sp = G[G["p4b_SPY"]]
    print(sp["p4b_EWW10_miss"].value_counts().to_string())
    print("\n--- per-panel 4b pass counts by bar")
    print(G.groupby("panel")[["p4b_SPY", "p4b_EW742", "p4b_EWW10"]].sum().to_string())
    print("\n--- per-family 4b-vs-SPY pass counts (of cells)")
    print(G.groupby("family")[["p4b_SPY", "p4b_EW742", "p4b_EWW10"]].sum().to_string())
    print("\n=== WALK-FORWARD (rule 8: dial on IS <= 2016 only, OOS 2017+ read once)")
    print(W.to_string(index=False))

    # ---------------------------------------------------------------- appendix, no new tuning
    # On a de-grossing book at a zero cash rate, gross is a pure scale on BOTH CAGR-ish level and
    # drawdown, so the BAND-DG ladder already pins the gross at which it would clear the EW bar's
    # two level legs. Read it off the committed ladder by OLS through the ladder's own points;
    # PROTOCOL rule 2 caps gross at 1.00, so g* > 1.00 means the pass is unreachable, not missing.
    app = []
    for pname in ("U56", "B136"):
        bar = B[(B.panel == pname) & (B.bar == "B_EWW10")].iloc[0]
        lad = G[(G.panel == pname) & (G.family == "BAND-DG")].sort_values("dial")
        g = lad["dial"].values
        # CAGR and MaxDD are near-linear in g; solve each leg by linear fit through the 7 rungs
        a_c, b_c = np.polyfit(g, lad["CAGR"].values, 1)
        a_d, b_d = np.polyfit(g, lad["MaxDD"].values, 1)
        g_cagr = (0.70 * bar["CAGR"] - b_c) / a_c          # gross needed to clear the CAGR floor
        g_dd = (0.60 * bar["MaxDD"] - b_d) / a_d           # gross at which the DD cap is breached
        app.append(dict(panel=pname, g_needed_for_CAGR_floor=g_cagr, g_breaching_DD_cap=g_dd,
                        feasible_under_PROTOCOL2=(g_cagr <= 1.00),
                        window_nonempty=(g_cagr < g_dd),
                        fit_r2_CAGR=float(np.corrcoef(g, lad["CAGR"].values)[0, 1] ** 2),
                        fit_r2_MaxDD=float(np.corrcoef(g, lad["MaxDD"].values)[0, 1] ** 2)))
    A = pd.DataFrame(app)
    A.to_csv(HERE / f"{STEM}.grossappendix.csv", index=False)
    print("\n=== APPENDIX — the gross the BAND-DG book would need to clear the EW bar's level legs")
    print(A.to_string(index=False))
    print("\nAll grid points are in", (HERE / f'{STEM}.grid.csv').name)


if __name__ == "__main__":
    main()
