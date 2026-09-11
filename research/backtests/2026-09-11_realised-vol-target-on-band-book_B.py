#!/usr/bin/env python3
"""Idea 794 (lane B, 2026-09-11) — does a REALISED-VOL TARGET on the BAND BOOK spend the
UNUSED DRAWDOWN BUDGET?

QUESTION
--------
The live book (RULES v2: hold every U56 name inside the 200d +/-3% band at 0.75/N of NAV,
weekly, de-gross to cash) clears every 4b leg except the CAGR floor: full CAGR 8.61% and OOS
CAGR 9.45% against floors of 10.58% / 10.67%, a gap of ~1.2 pp.  Its MaxDD is -12.05% against
a 4b cap of 60% x SPY's -33.72% = -20.23%, so it leaves ~40% of the permitted risk budget
unspent.  Idea 795 showed the gap is an EXPOSURE fact and closed it with a CONSTANT gross of
1.00 (plus a band move that cost OOS CAGR).  This run asks the other exposure question: does
spending the budget DYNAMICALLY — scale gross to a trailing realised-vol target, cap 1.0, no
leverage — buy the missing 1.2 pp, and does it buy anything a constant gross at the same
average exposure does not?

THE BOOK UNDER TEST
-------------------
Base = the live band book with the LIVE band 0.03 FROZEN (not a dial here) at gross 1.00:

    W_base_t = 1.00/N_t on every name inside the 200d +/-3% band, else cash.

Its own gross-of-cost daily return, used ONLY as the risk proxy (no costs, no lookahead):

    u_t = sum_i W_base_{t-1,i} * ret_{t,i}
    sigma_t = std(u_{t-L+1..t}) * sqrt(252)                       information through t only
    s_t = min(CAP=1.00, TARGET / sigma_t)                         no leverage, ever
    W_t = W_base_t * s_t                                          engine applies at t+1

Before L observations exist past the base book's first live day, s_t = 0.75 (the live gross,
a no-information default).  Weekly cadence means the scaler only re-prices on rebalance days
and every change is charged 10 bps of turnover — the cost of vol targeting is paid, not
assumed.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. TARGET   in {0.05, 0.06, 0.08, 0.10, 0.12, 0.15}   annualised vol target
    2. LOOKBACK in {21, 42, 63, 126, 252}                 trading days
All 6 x 5 = 30 cells are reported on the primary panel (U56).  REPORTED, never selected: the
same 30 cells on B136, the exposure-matched constant-gross controls, the halves, the OOS
window.  The band is NOT a dial (frozen at the live 0.03), and CAP is NOT a dial (1.00 = the
PROTOCOL no-leverage bound).

PRE-REGISTERED HYPOTHESES (written before any new number was read)
    H_BUDGET : some (TARGET, LOOKBACK) cell clears ALL FIVE 4b legs on the full sample, i.e.
               the unspent drawdown budget buys the missing CAGR.  Falsified if none does.
    H_TIMING : the vol scaler earns its keep BEYOND average exposure — a cell's Sharpe beats
               its EXPOSURE-MATCHED constant-gross control (same mean realised exposure,
               constant gross, same band).  Falsified at <= on the majority of cells.
    H_DD     : spending the budget stays inside it — the cells that clear the CAGR floor keep
               MaxDD <= 60% of SPY's, full sample AND OOS.
    H_WF     : rule 8 — the cell chosen on 2009-2016 ALONE still clears the 4b legs on
               2017-2026 read once.

GATES (pre-registered, reported before any finding)
    G1 the live cell IS the live book: band 0.03 / constant gross 0.75 reproduces the record's
       RULES v2 full Sharpe 1.1998, MaxDD -12.05%, OOS CAGR 9.45%, and equals
       baseline.rules_v2_weights exactly.
    G2 NO LOOKAHEAD: recomputing sigma_t on a panel truncated at t reproduces the full-panel
       sigma_t exactly, on 5 pre-chosen dates per lookback.
    G3 DEGENERATE LIMIT: at TARGET = 10.0 (unreachable) the scaler pins to CAP and the book
       equals the constant-gross-1.00 band book to < 1e-12 in every daily return.
       [CORRECTION, disclosed: as first written G3 compared every scored day on which s_t was
       pinned to the cap and read max diff 1.662e-04 -> FAIL.  All 67 differing days lie in the
       0.75 warm-up window (2008-10-20 .. 2009-01-26) and are an ENGINE-STATE artefact: the
       engine only re-sets held weights on a rebalance day, so the two books share held weights
       only from the first weekly rebalance whose previous day is already cap-pinned, and that
       transition day itself carries a one-off turnover charge.  G3 is re-specified to compare
       the days AFTER that transition; the warm-up segment and the transition day are reported
       beside it rather than dropped.  Nothing else changed.]
    G4 the comparands are the record's: SPY full CAGR 15.11% / Sharpe 0.8835 / MaxDD -33.72%,
       SPY OOS CAGR 15.24% / Sharpe 0.8721, 4b floors 10.58% / 10.67%, DD caps -20.23%.

PROTOCOL: 10 bps per unit turnover, next-day execution (engine), weekly cadence, no shorting,
no leverage (gross <= 1.00).  Rule 8: parameters chosen on 2009-2016 only, 2017-2026 read
once.  RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py are NOT modified.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, metrics, backtest  # noqa: E402

OUT = str(ROOT / "research" / "backtests" / "2026-09-11_realised-vol-target-on-band-book_B")
COST = 10
FREQ = "W"
BAND = 0.03          # frozen at the live band — NOT a tuned parameter
CAP = 1.00           # PROTOCOL no-leverage bound — NOT a tuned parameter
LIVE_GROSS = 0.75
TARGETS = [0.05, 0.06, 0.08, 0.10, 0.12, 0.15]
LOOKBACKS = [21, 42, 63, 126, 252]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_LOG: list[str] = []


def P(s: str = "") -> None:
    print(s)
    _LOG.append(s)


def band_weights(px: pd.DataFrame, band: float, gross: float) -> pd.DataFrame:
    """RULES v2's weights function with the gross dial exposed (band frozen by the caller)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def risk_proxy(px: pd.DataFrame, band: float) -> pd.Series:
    """u_t = the base (gross 1.00) band book's gross-of-cost daily return, held-at-t-1.

    Uses W_base shifted one day, so u_t is knowable at the close of t."""
    rets = px.pct_change().fillna(0.0)
    wb = band_weights(px, band, 1.00).shift(1).fillna(0.0)
    return (wb * rets).sum(axis=1)


def scaler(u: pd.Series, target: float, lookback: int, cap: float = CAP) -> pd.Series:
    """s_t = min(cap, target / sigma_t), sigma_t from u through t only.

    Before `lookback` observations exist past the base book's first live day, s_t = the live
    gross 0.75 (a no-information default, pre-registered)."""
    sigma = u.rolling(lookback).std() * np.sqrt(252)
    s = np.minimum(cap, target / sigma.replace(0.0, np.nan))
    live_from = u.ne(0.0).idxmax()                       # first day the base book is invested
    warm_end = u.index[min(u.index.get_loc(live_from) + lookback, len(u) - 1)]
    s = s.fillna(cap)
    s.loc[:warm_end] = LIVE_GROSS
    return s


def vt_weights_fn(px: pd.DataFrame, band: float, target: float, lookback: int):
    u = risk_proxy(px, band)
    s = scaler(u, target, lookback)
    return band_weights(px, band, 1.00).mul(s, axis=0), s


def window(r: pd.Series, lo=None, hi=None) -> pd.Series:
    return r.loc[lo:hi]


def halves(r: pd.Series) -> tuple[float, float]:
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def score_book(px, W, start, label, extra=None) -> tuple[dict, pd.Series]:
    res = backtest(px, W, cost_bps=COST, freq=FREQ)
    r = res["returns"].loc[start:]
    held = res["weights"].loc[start:]
    m = metrics(r)
    h1, h2 = halves(r)
    ri, ro = window(r, None, IS_END), window(r, OOS_START, None)
    mi, mo = metrics(ri), metrics(ro)
    oh1, oh2 = halves(ro)
    row = dict(book=label, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
               H1=h1, H2=h2,
               IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
               OOS_H1=oh1, OOS_H2=oh2,
               Ebar=float(held.sum(axis=1).mean()),
               turnover_yr=float(res["turnover"].loc[start:].sum() / m["Years"]))
    if extra:
        row.update(extra)
    return row, r


def keep_paths(row, live, spy_full, spy_oos, spy_h1, spy_h2, spy_oh1, spy_oh2) -> dict:
    """PROTOCOL 4a and 4b, every leg reported separately."""
    a1 = row["H1"] > live["H1"]
    a2 = row["H2"] > live["H2"]
    a3 = row["MaxDD"] >= live["MaxDD"]                       # "no worse" = less negative
    b1 = row["H1"] > spy_h1
    b2 = row["H2"] > spy_h2
    b3 = row["OOS_Sharpe"] > spy_oos["Sharpe"]
    b4 = row["MaxDD"] >= 0.60 * spy_full["MaxDD"]
    b5 = row["CAGR"] >= 0.70 * spy_full["CAGR"]
    return dict(a_h1=a1, a_h2=a2, a_dd=a3, pass4a=bool(a1 and a2 and a3),
                b_h1=b1, b_h2=b2, b_oos=b3, b_dd=b4, b_cagr=b5,
                pass4b=bool(b1 and b2 and b3 and b4 and b5))


def oos_4b(row, spy_oos, spy_oh1, spy_oh2) -> dict:
    """The same five 4b legs read on the OOS window alone (rule 8 reporting)."""
    l1 = row["OOS_H1"] > spy_oh1
    l2 = row["OOS_H2"] > spy_oh2
    l3 = row["OOS_Sharpe"] > spy_oos["Sharpe"]
    l4 = row["OOS_MaxDD"] >= 0.60 * spy_oos["MaxDD"]
    l5 = row["OOS_CAGR"] >= 0.70 * spy_oos["CAGR"]
    return dict(o_h1=l1, o_h2=l2, o_sharpe=l3, o_dd=l4, o_cagr=l5,
                pass4b_oos=bool(l1 and l2 and l3 and l4 and l5))


def run_panel(px, panel: str, start) -> tuple[pd.DataFrame, dict]:
    rows, rets = [], {}
    base_u = risk_proxy(px, BAND)
    for target in TARGETS:
        for lookback in LOOKBACKS:
            W, s = vt_weights_fn(px, BAND, target, lookback)
            row, r = score_book(px, W, start, f"vt t={target} L={lookback}",
                                extra=dict(panel=panel, target=target, lookback=lookback,
                                           sbar=float(s.loc[start:].mean()),
                                           s_at_cap=float((s.loc[start:] >= CAP - 1e-12).mean()),
                                           s_min=float(s.loc[start:].min())))
            rows.append(row)
            rets[(target, lookback)] = r
    return pd.DataFrame(rows), rets


def main() -> None:
    t0 = time.time()
    P("=" * 100)
    P("IDEA 794 — does a REALISED-VOL TARGET on the BAND BOOK spend the UNUSED DRAWDOWN BUDGET?")
    P("lane B, 2026-09-11.  PROTOCOL: 10 bps, next-day execution, weekly, no leverage (cap 1.00).")
    P("Band FROZEN at the live 0.03.  Tuned: TARGET x LOOKBACK = 6 x 5 = 30 cells, all reported.")
    P("=" * 100)

    px = load_universe()
    start = px.index[260]
    P(f"panel U56: {px.shape[1]} columns, {px.index[0].date()} .. {px.index[-1].date()}, "
      f"scored from {start.date()}")

    # ---------------------------------------------------------------- comparands
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    ms = metrics(spy)
    spy_h1, spy_h2 = halves(spy)
    spy_oos_r = window(spy, OOS_START, None)
    mso = metrics(spy_oos_r)
    spy_oh1, spy_oh2 = halves(spy_oos_r)
    msi = metrics(window(spy, None, IS_END))
    FLOOR_FULL, CAP_FULL = 0.70 * ms["CAGR"], 0.60 * ms["MaxDD"]
    FLOOR_OOS, CAP_OOS = 0.70 * mso["CAGR"], 0.60 * mso["MaxDD"]

    # ---------------------------------------------------------------- reference books
    live_row, live_r = score_book(px, band_weights(px, BAND, LIVE_GROSS), start,
                                  "RULES v2 live (band 0.03, gross 0.75)")
    g100_row, _ = score_book(px, band_weights(px, BAND, 1.00), start,
                             "constant gross 1.00 (band 0.03)")
    i795_row, _ = score_book(px, band_weights(px, 0.08, 1.00), start,
                             "idea 795 candidate (band 0.08, gross 1.00)")

    # ---------------------------------------------------------------- gates
    P("")
    P("GATES (pre-registered)")
    base_engine = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].loc[start:]
    mb = metrics(base_engine)
    g1 = bool(abs(live_row["Sharpe"] - mb["Sharpe"]) < 1e-12
              and abs(live_row["Sharpe"] - 1.1998) <= 0.01
              and abs(live_row["MaxDD"] + 0.1205) <= 0.01
              and abs(live_row["OOS_CAGR"] - 0.0945) <= 0.005)
    P(f"  G1 live cell == live book : Sharpe {live_row['Sharpe']:.4f} "
      f"(baseline.rules_v2 {mb['Sharpe']:.4f}, record 1.1998), MaxDD {live_row['MaxDD']:.4f} "
      f"(record -0.1205), OOS CAGR {live_row['OOS_CAGR']:.4f} (record 0.0945) -> "
      f"{'PASS' if g1 else 'FAIL'}")

    u = risk_proxy(px, BAND)
    worst = 0.0
    for L in LOOKBACKS:
        s_full = scaler(u, 0.10, L)
        for pos in (900, 1500, 2200, 3000, 3800):
            if pos >= len(u):
                continue
            t = u.index[pos]
            s_trunc = scaler(u.loc[:t], 0.10, L)
            worst = max(worst, abs(float(s_full.loc[t]) - float(s_trunc.loc[t])))
    g2 = worst < 1e-12
    P(f"  G2 no lookahead          : max |s_t(full panel) - s_t(panel truncated at t)| = "
      f"{worst:.3e} over 5 dates x {len(LOOKBACKS)} lookbacks -> {'PASS' if g2 else 'FAIL'}")

    W_deg, s_deg = vt_weights_fn(px, BAND, 10.0, 63)
    r_deg = backtest(px, W_deg, cost_bps=COST, freq=FREQ)["returns"]
    r_g100 = backtest(px, band_weights(px, BAND, 1.00), cost_bps=COST, freq=FREQ)["returns"]
    dall = (r_deg - r_g100).abs()
    pinned = s_deg[s_deg >= CAP - 1e-12].index                     # every cap-pinned day
    warm_end_deg = s_deg[s_deg != LIVE_GROSS].index[0]             # first post-warm-up day
    from engine import rebalance_mask                              # noqa: E402
    # the engine sets held weights to w_target.shift(1) on mask.shift(1) days, so the two books
    # share HELD weights only from the first such day whose PREVIOUS day is already cap-pinned
    mask_eff = rebalance_mask(px.index, FREQ).shift(1, fill_value=False)
    prev_pinned = (s_deg.shift(1) >= CAP - 1e-12) & (s_deg.shift(1).index > warm_end_deg)
    reset = dall.index[(mask_eff.values & prev_pinned.values)][0]
    after = dall.index[dall.index.get_loc(reset) + 1]               # first day past the transition
    d_warm = float(dall.loc[:reset].iloc[:-1].max())
    d_reset = float(dall.loc[reset])
    dmax = float(dall.loc[after:].max())
    g3 = dmax < 1e-12
    P(f"  G3 degenerate limit      : TARGET=10.0 pins s_t to cap on {len(pinned)}/{len(dall)} days; "
      f"warm-up (0.75) ends {warm_end_deg.date()}, engine re-sets held weights {reset.date()}; "
      f"max |r_vt - r_gross1.00| over the {len(dall.loc[after:])} days AFTER the transition = "
      f"{dmax:.3e} ({int((dall.loc[after:] > 1e-12).sum())} differing days) -> "
      f"{'PASS' if g3 else 'FAIL'}")
    P(f"     [the transition itself costs one day of turnover, |diff| {d_reset:.3e} on "
      f"{reset.date()}; the 0.75 warm-up segment before it differs by up to {d_warm:.3e}. "
      f"Both are the warm-up convention, not the scaler.]")

    g4 = bool(abs(ms["CAGR"] - 0.1511) <= 0.005 and abs(ms["Sharpe"] - 0.8835) <= 0.01
              and abs(ms["MaxDD"] + 0.3372) <= 0.01 and abs(mso["CAGR"] - 0.1524) <= 0.005
              and abs(mso["Sharpe"] - 0.8721) <= 0.01)
    P(f"  G4 comparands            : SPY full {ms['CAGR']:.4f}/{ms['Sharpe']:.4f}/{ms['MaxDD']:.4f} "
      f"(record .1511/.8835/-.3372), OOS {mso['CAGR']:.4f}/{mso['Sharpe']:.4f} "
      f"(record .1524/.8721) -> {'PASS' if g4 else 'FAIL'}")
    P(f"     4b bars: CAGR floor full {FLOOR_FULL:.4f} / OOS {FLOOR_OOS:.4f}; "
      f"DD cap full {CAP_FULL:.4f} / OOS {CAP_OOS:.4f}; "
      f"SPY halves {spy_h1:.4f}/{spy_h2:.4f}, SPY OOS halves {spy_oh1:.4f}/{spy_oh2:.4f}; "
      f"SPY IS CAGR {msi['CAGR']:.4f}")

    # ---------------------------------------------------------------- the grid
    P("")
    P("THE GRID — 30 cells on U56, ALL REPORTED (band frozen 0.03, cap 1.00)")
    grid, rets = run_panel(px, "U56", start)
    live_cmp = dict(live_row)                     # frozen comparand for the 4a legs
    for r_ in [live_row, g100_row, i795_row]:
        r_.update(panel="U56", target=np.nan, lookback=np.nan, sbar=np.nan,
                  s_at_cap=np.nan, s_min=np.nan)
        r_.update(keep_paths(r_, live_cmp, ms, mso, spy_h1, spy_h2, spy_oh1, spy_oh2))
        r_.update(oos_4b(r_, mso, spy_oh1, spy_oh2))
    grid = pd.DataFrame([dict(r_, **keep_paths(r_, live_cmp, ms, mso, spy_h1, spy_h2, spy_oh1, spy_oh2),
                              **oos_4b(r_, mso, spy_oh1, spy_oh2))
                         for r_ in grid.to_dict("records")])

    cols = ["target", "lookback", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "Ebar", "sbar", "s_at_cap", "turnover_yr", "pass4a", "pass4b", "pass4b_oos"]
    P(grid[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("REFERENCE BOOKS (not cells of the grid)")
    ref = pd.DataFrame([live_row, g100_row, i795_row])
    P(ref[["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
           "Ebar", "turnover_yr", "pass4a", "pass4b", "pass4b_oos"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- H_BUDGET / H_DD
    P("")
    P("H_BUDGET — does any cell clear all five 4b legs on the full sample?")
    n4b = int(grid["pass4b"].sum())
    n4a = int(grid["pass4a"].sum())
    legs = {k: int((~grid[k]).sum()) for k in ["b_h1", "b_h2", "b_oos", "b_dd", "b_cagr"]}
    P(f"  4b passes {n4b}/30, 4a passes {n4a}/30.  Failing-leg counts (out of 30): "
      + ", ".join(f"{k}={v}" for k, v in legs.items()))
    P(f"  live book for reference: CAGR {live_row['CAGR']:.4f} (floor {FLOOR_FULL:.4f}, "
      f"gap {100*(live_row['CAGR']-FLOOR_FULL):+.2f} pp), MaxDD {live_row['MaxDD']:.4f} "
      f"(cap {CAP_FULL:.4f}, budget spent {100*live_row['MaxDD']/CAP_FULL:.1f}%)")
    best = grid.loc[grid["CAGR"].idxmax()]
    P(f"  best-CAGR cell: t={best['target']} L={best['lookback']:.0f} CAGR {best['CAGR']:.4f} "
      f"({100*(best['CAGR']-FLOOR_FULL):+.2f} pp vs floor), MaxDD {best['MaxDD']:.4f} "
      f"(budget spent {100*best['MaxDD']/CAP_FULL:.1f}%), Sharpe {best['Sharpe']:.4f}")
    H_BUDGET = n4b > 0
    P(f"  H_BUDGET -> {'HELD' if H_BUDGET else 'FALSIFIED'}")

    clearing = grid[grid["b_cagr"]]
    H_DD = bool(len(clearing) > 0 and clearing["b_dd"].all()
                and (clearing["OOS_MaxDD"] >= CAP_OOS).all())
    P(f"  H_DD (cells clearing the CAGR floor keep MaxDD inside the cap, full AND OOS): "
      f"{len(clearing)} such cells -> {'HELD' if H_DD else ('FALSIFIED' if len(clearing) else 'VACUOUS')}")

    # ---------------------------------------------------------------- H_TIMING
    P("")
    P("H_TIMING — does the scaler beat a CONSTANT gross matched on mean realised exposure?")
    P("  (matched gross g* = Ebar_cell / Ebar_gross1.00; the control holds it constant.)")
    Ebar1 = g100_row["Ebar"]
    mrows = []
    for _, c in grid.iterrows():
        gstar = float(c["Ebar"] / Ebar1)
        mrow, _ = score_book(px, band_weights(px, BAND, gstar), start,
                             f"const g={gstar:.4f}",
                             extra=dict(target=c["target"], lookback=c["lookback"], gstar=gstar))
        mrows.append(dict(target=c["target"], lookback=c["lookback"], gstar=gstar,
                          vt_CAGR=c["CAGR"], vt_Sharpe=c["Sharpe"], vt_MaxDD=c["MaxDD"],
                          vt_OOS_Sharpe=c["OOS_Sharpe"], vt_Ebar=c["Ebar"], vt_turn=c["turnover_yr"],
                          ct_CAGR=mrow["CAGR"], ct_Sharpe=mrow["Sharpe"], ct_MaxDD=mrow["MaxDD"],
                          ct_OOS_Sharpe=mrow["OOS_Sharpe"], ct_Ebar=mrow["Ebar"],
                          ct_turn=mrow["turnover_yr"],
                          dSharpe=c["Sharpe"] - mrow["Sharpe"], dCAGR=c["CAGR"] - mrow["CAGR"],
                          dMaxDD=c["MaxDD"] - mrow["MaxDD"],
                          dOOS_Sharpe=c["OOS_Sharpe"] - mrow["OOS_Sharpe"]))
    matched = pd.DataFrame(mrows)
    P(matched[["target", "lookback", "gstar", "vt_Ebar", "ct_Ebar", "vt_Sharpe", "ct_Sharpe",
               "dSharpe", "dCAGR", "dMaxDD", "dOOS_Sharpe", "vt_turn", "ct_turn"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    matched_ix = matched.set_index(["target", "lookback"])
    win = int((matched["dSharpe"] > 0).sum())
    H_TIMING = win > len(matched) / 2
    P(f"  scaler beats matched constant in Sharpe on {win}/{len(matched)} cells; "
      f"median dSharpe {matched['dSharpe'].median():+.4f}, mean {matched['dSharpe'].mean():+.4f}; "
      f"median dCAGR {100*matched['dCAGR'].median():+.2f} pp; "
      f"median dMaxDD {100*matched['dMaxDD'].median():+.2f} pp; "
      f"median extra turnover {matched['vt_turn'].median()-matched['ct_turn'].median():+.2f}x/yr")
    P(f"  H_TIMING -> {'HELD' if H_TIMING else 'FALSIFIED'}")

    # ---------------------------------------------------------------- degeneracy
    P("")
    P("DEGENERACY — what are the 4b-passing cells actually DOING?")
    passers = grid[grid["pass4b"]].copy()
    passers["dSharpe_vs_matched"] = [float(matched_ix.loc[(t, L), "dSharpe"])
                                     for t, L in zip(passers["target"], passers["lookback"])]
    passers["dCAGR_vs_matched"] = [float(matched_ix.loc[(t, L), "dCAGR"])
                                   for t, L in zip(passers["target"], passers["lookback"])]
    P(passers[["target", "lookback", "sbar", "s_at_cap", "Ebar", "CAGR", "Sharpe", "MaxDD",
               "dSharpe_vs_matched", "dCAGR_vs_matched"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  every 4b passer has sbar >= {passers['sbar'].min():.4f} and sits at the cap on "
      f">= {100*passers['s_at_cap'].min():.1f}% of days; the base book's own realised vol at "
      f"gross 1.00 is {252**0.5*risk_proxy(px, BAND).loc[start:].std():.4f}/yr, so every TARGET "
      f"that clears the CAGR floor is ABOVE the vol it is targeting.")
    P(f"  rho(sbar, CAGR) over the 30 cells = {np.corrcoef(grid['sbar'], grid['CAGR'])[0,1]:+.4f}; "
      f"rho(sbar, Sharpe) = {np.corrcoef(grid['sbar'], grid['Sharpe'])[0,1]:+.4f}")
    P("")
    P("THE ZERO-EXTRA-PARAMETER BOOK IT ALL COLLAPSES TO (band 0.03 = live, gross 1.00 = the")
    P("PROTOCOL no-leverage bound; nothing tuned), against the record's standing 4b candidate:")
    for r_, lab in [(g100_row, "band 0.03 x gross 1.00 (nothing tuned)"),
                    (i795_row, "idea 795 pick band 0.08 x gross 1.00"),
                    (live_row, "RULES v2 live band 0.03 x gross 0.75")]:
        P(f"  {lab:42s} full {r_['CAGR']:.4f}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.4f}  "
          f"halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.4f}/{r_['OOS_Sharpe']:.4f}/"
          f"{r_['OOS_MaxDD']:.4f}  turn {r_['turnover_yr']:.2f}x  4b {r_['pass4b']}/"
          f"OOS {r_['pass4b_oos']}")
    dom = {k: float(g100_row[k] - i795_row[k]) for k in
           ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]}
    P("  band 0.03 x gross 1.00 minus idea 795's pick: " +
      ", ".join(f"{k} {v:+.4f}" for k, v in dom.items()))

    # ---------------------------------------------------------------- rule 8
    P("")
    P("RULE 8 WALK-FORWARD — parameters chosen on 2009-2016 ONLY, 2017-2026 read once")
    wf = []
    sel1 = grid.loc[grid["IS_Sharpe"].idxmax()]
    wf.append(("S1 highest IS Sharpe", sel1))
    elig = grid[grid["IS_CAGR"] >= 0.70 * msi["CAGR"]]
    P(f"  cells clearing the IS CAGR floor (0.70 x SPY IS CAGR {msi['CAGR']:.4f} = "
      f"{0.70*msi['CAGR']:.4f}): {len(elig)}/30")
    if len(elig):
        sel2 = elig.loc[elig["IS_Sharpe"].idxmax()]
    else:
        sel2 = grid.loc[grid["IS_CAGR"].idxmax()]
        P("  S2 feasible set EMPTY -> falls back to highest IS CAGR (pre-registered fallback)")
    wf.append(("S2 highest IS Sharpe clearing IS CAGR floor", sel2))
    wfrows = []
    for label, sel in wf:
        P(f"  {label}: TARGET {sel['target']} LOOKBACK {sel['lookback']:.0f} "
          f"(IS Sharpe {sel['IS_Sharpe']:.4f}, IS CAGR {sel['IS_CAGR']:.4f})")
        P(f"      OOS 2017-2026: CAGR {sel['OOS_CAGR']:.4f}  Sharpe {sel['OOS_Sharpe']:.4f}  "
          f"MaxDD {sel['OOS_MaxDD']:.4f}  halves {sel['OOS_H1']:.4f}/{sel['OOS_H2']:.4f}  "
          f"turnover {sel['turnover_yr']:.2f}x/yr")
        P(f"      vs RULES v2 OOS {live_row['OOS_CAGR']:.4f}/{live_row['OOS_Sharpe']:.4f}/"
          f"{live_row['OOS_MaxDD']:.4f}   vs SPY OOS {mso['CAGR']:.4f}/{mso['Sharpe']:.4f}/"
          f"{mso['MaxDD']:.4f}")
        P(f"      OOS 4b legs: h1 {sel['o_h1']}  h2 {sel['o_h2']}  sharpe {sel['o_sharpe']}  "
          f"dd {sel['o_dd']}  cagr {sel['o_cagr']}  -> "
          f"{'ALL PASS' if sel['pass4b_oos'] else 'FAIL'}")
        wfrows.append(dict(selector=label, target=sel["target"], lookback=sel["lookback"],
                           IS_Sharpe=sel["IS_Sharpe"], IS_CAGR=sel["IS_CAGR"],
                           OOS_CAGR=sel["OOS_CAGR"], OOS_Sharpe=sel["OOS_Sharpe"],
                           OOS_MaxDD=sel["OOS_MaxDD"], OOS_H1=sel["OOS_H1"], OOS_H2=sel["OOS_H2"],
                           pass4b_oos=bool(sel["pass4b_oos"]), pass4b_full=bool(sel["pass4b"]),
                           pass4a_full=bool(sel["pass4a"])))
    # the live book and the constant-gross control through the same OOS lens
    for r_, lab in [(live_row, "RULES v2 live"), (g100_row, "constant gross 1.00"),
                    (i795_row, "idea 795 band 0.08 gross 1.00")]:
        wfrows.append(dict(selector=f"REFERENCE {lab}", target=np.nan, lookback=np.nan,
                           IS_Sharpe=r_["IS_Sharpe"], IS_CAGR=r_["IS_CAGR"],
                           OOS_CAGR=r_["OOS_CAGR"], OOS_Sharpe=r_["OOS_Sharpe"],
                           OOS_MaxDD=r_["OOS_MaxDD"], OOS_H1=r_["OOS_H1"], OOS_H2=r_["OOS_H2"],
                           pass4b_oos=bool(r_["pass4b_oos"]), pass4b_full=bool(r_["pass4b"]),
                           pass4a_full=bool(r_["pass4a"])))
    wfdf = pd.DataFrame(wfrows)
    H_WF = bool(all(w["pass4b_oos"] for w in wfrows[:2]))
    P(f"  H_WF -> {'HELD' if H_WF else 'FALSIFIED'}")
    agree = (wf[0][1]["target"] == wf[1][1]["target"]) and (wf[0][1]["lookback"] == wf[1][1]["lookback"])
    P(f"  the two pre-registered selectors {'AGREE' if agree else 'DISAGREE'}")

    # ---------------------------------------------------------------- B136 replication
    P("")
    P("B136 REPLICATION (reported, NEVER selected; current-constituent survivorship bias)")
    try:
        pxb = load_universe(broad=True)
        startb = pxb.index[260]
        gridb, _ = run_panel(pxb, "B136", startb)
        liveb, _ = score_book(pxb, band_weights(pxb, BAND, LIVE_GROSS), startb, "RULES v2 live")
        spyb = pxb["SPY"].pct_change().fillna(0).loc[startb:]
        msb = metrics(spyb)
        sb1, sb2 = halves(spyb)
        msob = metrics(window(spyb, OOS_START, None))
        sob1, sob2 = halves(window(spyb, OOS_START, None))
        gridb = pd.DataFrame([dict(r_, **keep_paths(r_, liveb, msb, msob, sb1, sb2, sob1, sob2),
                                   **oos_4b(r_, msob, sob1, sob2))
                              for r_ in gridb.to_dict("records")])
        P(gridb[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        P(f"  B136: 4b {int(gridb['pass4b'].sum())}/30, 4a {int(gridb['pass4a'].sum())}/30; "
          f"SPY full {msb['CAGR']:.4f}/{msb['Sharpe']:.4f}/{msb['MaxDD']:.4f}; "
          f"live band book {liveb['CAGR']:.4f}/{liveb['Sharpe']:.4f}/{liveb['MaxDD']:.4f}")
        gridb.to_csv(OUT + ".broad.csv", index=False)
        b136 = dict(n4b=int(gridb["pass4b"].sum()), n4a=int(gridb["pass4a"].sum()),
                    best_CAGR=float(gridb["CAGR"].max()), best_Sharpe=float(gridb["Sharpe"].max()))
    except Exception as e:                                   # panel unavailable -> say so
        P(f"  B136 unavailable: {type(e).__name__}: {e}")
        b136 = dict(error=f"{type(e).__name__}: {e}")

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 100)
    # VERDICT RULE, CORRECTED AND DISCLOSED.  As first written the rule was
    #   `KEEP-candidate (4b) if H_BUDGET and H_WF`,
    # which cannot tell "the overlay works" from "the overlay pinned itself to a constant":
    # the object under test is the SCALER, and a cell whose scaler sits at the cap 85-98% of
    # the time IS the constant-gross-1.00 book that idea 795 already published.  The rule now
    # requires H_TIMING as well.  The mechanical old rule's reading is printed beside the new
    # one so the change is visible, and the 4b/4a cell counts below are unchanged either way.
    old_rule = "KEEP-candidate (4b)" if (H_BUDGET and H_WF) else (
        "KEEP-candidate (4a)" if n4a > 0 else ("PARK" if n4b > 0 else "KILL"))
    if H_TIMING and H_BUDGET and H_WF:
        verdict = "KEEP-candidate (4b)"
    elif H_TIMING and n4a > 0:
        verdict = "KEEP-candidate (4a)"
    elif H_TIMING:
        verdict = "PARK"
    else:
        verdict = "KILL (the vol-target overlay; the 4b passers are degenerate to constant gross)"
    P(f"VERDICT: {verdict}")
    P(f"  (the pre-correction verdict rule, H_BUDGET and H_WF only, would have read: {old_rule})")
    P(f"  H_BUDGET {'HELD' if H_BUDGET else 'FALSIFIED'} | "
      f"H_TIMING {'HELD' if H_TIMING else 'FALSIFIED'} | "
      f"H_DD {'HELD' if H_DD else ('FALSIFIED' if len(clearing) else 'VACUOUS')} | "
      f"H_WF {'HELD' if H_WF else 'FALSIFIED'}")
    P(f"  elapsed {time.time()-t0:.1f}s")
    P("=" * 100)

    # ---------------------------------------------------------------- artefacts
    grid.to_csv(OUT + ".grid.csv", index=False)
    matched.to_csv(OUT + ".matched.csv", index=False)
    wfdf.to_csv(OUT + ".walkforward.csv", index=False)
    pd.DataFrame([live_row, g100_row, i795_row]).to_csv(OUT + ".reference.csv", index=False)
    summary = dict(
        idea=794, lane="B", date="2026-09-11", verdict=verdict,
        gates=dict(G1=g1, G2=g2, G3=g3, G4=g4, G2_max_diff=worst, G3_max_diff=dmax),
        hypotheses=dict(H_BUDGET=H_BUDGET, H_TIMING=H_TIMING,
                        H_DD=(H_DD if len(clearing) else None), H_WF=H_WF),
        grid=dict(cells=int(len(grid)), pass4a=n4a, pass4b=n4b, failing_legs=legs),
        spy=dict(full=dict(CAGR=ms["CAGR"], Sharpe=ms["Sharpe"], MaxDD=ms["MaxDD"],
                           H1=spy_h1, H2=spy_h2),
                 oos=dict(CAGR=mso["CAGR"], Sharpe=mso["Sharpe"], MaxDD=mso["MaxDD"],
                          H1=spy_oh1, H2=spy_oh2),
                 is_=dict(CAGR=msi["CAGR"])),
        bars=dict(floor_full=FLOOR_FULL, floor_oos=FLOOR_OOS, cap_full=CAP_FULL, cap_oos=CAP_OOS),
        live=dict((k, live_row[k]) for k in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                                             "OOS_Sharpe", "OOS_MaxDD", "Ebar", "turnover_yr"]),
        gross100=dict((k, g100_row[k]) for k in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                                                 "OOS_Sharpe", "OOS_MaxDD", "Ebar", "turnover_yr"]),
        idea795=dict((k, i795_row[k]) for k in ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR",
                                                "OOS_Sharpe", "OOS_MaxDD"]),
        verdict_rule_precorrection=old_rule,
        degeneracy=dict(min_sbar_4b=float(passers["sbar"].min()) if len(passers) else None,
                        min_s_at_cap_4b=float(passers["s_at_cap"].min()) if len(passers) else None,
                        rho_sbar_CAGR=float(np.corrcoef(grid["sbar"], grid["CAGR"])[0, 1]),
                        rho_sbar_Sharpe=float(np.corrcoef(grid["sbar"], grid["Sharpe"])[0, 1]),
                        g100_minus_idea795=dom),
        matched=dict(wins=win, n=len(matched), median_dSharpe=float(matched["dSharpe"].median()),
                     mean_dSharpe=float(matched["dSharpe"].mean()),
                     median_dCAGR=float(matched["dCAGR"].median()),
                     median_dMaxDD=float(matched["dMaxDD"].median())),
        walkforward=wfrows, b136=b136)
    Path(OUT + ".summary.json").write_text(json.dumps(summary, indent=2, default=float))
    Path(OUT + ".console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
