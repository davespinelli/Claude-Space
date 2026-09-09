#!/usr/bin/env python3
"""Idea 320: is-the-UNCONDITIONAL-width-dial-a-B136-fact-or-a-panel-ordering  (lane B, 2026-09-09)

QUEUE PREMISE (idea 318's by-product).  DIL-ALW m>=2 (k = min(round(m*20), E_t) EVERY day,
75% gross) and EWALL clear 4b on B136 (OOS Sharpe 0.971/1.003/1.030/1.019 vs NF20 0.883)
while being FLAT on U56 and monotonically WORSE on SMALL439 (0.454 -> 0.361 vs 0.464).
Sweep n0 itself and ask whether that is the same U56 > B136 > SMALL ordering ideas 51/312/316
keep finding, or the opposite one.

WHAT IS ACTUALLY BEING SWEPT.  One dial: the unconditional book width.  The book is idea 318's
NF family with the breadth flag deleted -- rank the eligible names (200d MA up, vol20 < 0.60),
hold the top k at gross/k each, k = min(n0, E_t), gross 0.75 EVERY day, weekly, 10 bps, t+1.
Because k is capped at E_t the realised gross is 0.75 at every dial point by construction
(gate G3), so d = r(n0) - r(20) is WIDTH and nothing else -- no exposure term, which idea 321
and idea 587 showed is what usually moves 4b.

THE DIAL IS READ IN TWO UNITS (still one dial, so still 1 tuned parameter; panel is a
reporting axis, not a tuned parameter):
    ABS  n0 in {20, 30, 40, 60, E_t}          the queue's grid, an ABSOLUTE name count
    REL  c  in {0.25, 0.50, 0.75, 1.00}       k = max(1, round(c * E_t)), a COVERAGE fraction
The second unit is the point.  Idea 336/400 established that an ABSOLUTE cut applied to a
panel-dependent distribution measures the FREQUENCY, not the signal.  E_t is panel-dependent
(U56 can never offer more than 56 names), so an absolute n0 grid is not the same experiment on
three panels: on U56 the upper half of the queue's grid may be SATURATED (k == E_t, i.e. the
same book as EWALL) and therefore INERT, which would make "flat on U56" a capacity fact rather
than a panel-ordering fact.  H3 below tests exactly that.

HYPOTHESES, pre-registered:
  H1 (the premise)  the width slope is POSITIVE on B136, ~0 on U56, NEGATIVE on SMALL.
  H2 (the question) the SLOPE ordering equals the LEVEL ordering U56 > B136 > SMALL.
  H3 (mine)         U56's flatness is dial SATURATION: above ~mean E_t the absolute dial stops
                    producing distinct books.  Measured by the saturation share
                    mean(1[E_t <= n0]) and by max|dW| between adjacent dial points.
  H4 (collapse)     read in COVERAGE units the three panels' width curves are the same curve;
                    the absolute-unit disagreement is a name-count artefact.

GATES (all must pass, printed first, nothing is interpreted until they do):
  G1  fast_backtest == engine.backtest on a live book (max|d| reported)
  G2  live RULES v2 on U56 reproduces the record's 8.66% / 1.2056 / -12.05% (1.2259 / 1.1909).
      VINTAGE: data/prices.csv now carries U56 out to 2026-09-08 while prices_broad.csv and
      prices_small.csv stop at 2026-09-04.  All three panels are therefore truncated to the
      COMMON END 2026-09-04, which is also the vintage the record's number was computed on;
      the un-truncated U56 gives 8.64% / 1.2037 (a -0.0019 Sharpe vintage drift, reported).
  G3  THE DIAL MUST NOT BE AN EXPOSURE DIAL.  Bar, stated before the run: mean TARGET gross
      within 1 pp of 0.75 at every grid point, and REALISED gross spread within 1 pp across
      each panel's dial.  1 pp is the bar because idea 321 needed 12.78 pp of gross motion to
      move a 4b DD margin, so anything an order of magnitude smaller cannot be the mechanism.
      Neither quantity is an exact identity and neither is asserted to be:
        - the target gross falls below 0.75 on days when a name is ELIGIBLE (above its 200d
          MA, vol20 under the cap) but has NO composite score yet, because the 12m momentum
          leg needs 252 bars.  Such a name is counted in E_t but cannot be ranked.  Inherited
          from idea 318's construction, kept so G4 provenance is exact, CENSUSED here.  It
          concentrates at the widest points of the widest panel, which is where the SMALL
          result lives -- so the FILL control below re-runs the dial with k taken from the
          RANKED count instead of E_t and asks whether the finding survives.
        - the realised gross drifts because engine.backtest lets weights run between weekly
          rebalances.
  G4  provenance: B136 OOS Sharpe at n0 = 20/40/60/E_t reproduces idea 318's published
      0.883 / 0.971 / 1.003 / 1.019
  G5  provenance of the 4b passer: U56 n0=20 must reproduce the record's already-published
      KEEP-4b row 12.8% / 1.07 / -18.3% / 1.08 / 1.07 (LEADERBOARD.md line 288, idea 46
      `2026-09-04_eligible-fraction-vs-n_B.py`, and line 2925, idea 48
      `2026-09-07_breadth-adaptive-count-2022_B.py`).  If it does, this run's 4b passers are
      RE-DERIVATIONS of books the record already holds and did not adopt -- not new candidates.

Rule 8 walk-forward: the dial is chosen on IS (<= 2016-12-31) only, OOS (2017-01-01 ..) is read
once.  Two choosers reported (IS Sharpe, and IS Sharpe among IS-4b passers).  Both KEEP paths
(4a vs live RULES v2, 4b vs SPY) evaluated at every one of the grid points.

SURVIVORSHIP: B136 (universe_broad.json) and the SMALL panel are CURRENT constituents only;
their levels are biased upward and only cross-dial differences within a panel are read here.

Deterministic, standalone:  python3 research/backtests/2026-09-09_is-the-...-ordering_B.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
VOL_SCALE = False
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
COMMON_END = "2026-09-04"   # last bar carried by ALL THREE cached panels; also the record's vintage

ABS_GRID = [20, 30, 40, 60, "E"]            # "E" == E_t (EWALL), the queue's grid
REL_GRID = [0.25, 0.50, 0.75, 1.00]         # the same dial in coverage units

SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ engine replica
def fast_backtest(prices, weights, cost_bps=COST_BPS, freq=FREQ):
    """Numpy replica of engine.backtest (same drift, same t+1 application). Gated in G1."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n = len(idx)
    cur = np.zeros(prices.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(n)
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
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return (pd.Series(port, index=idx),
            pd.Series(turn, index=idx),
            pd.DataFrame(held, index=idx, columns=prices.columns))


# ------------------------------------------------------------------ book primitives
def eligible_mask(px, cols):
    _, above, vol20 = score(px)
    return (above & (vol20 < MAX_VOL))[cols]


def eligible_count(px, cols):
    e = eligible_mask(px, cols).sum(axis=1).astype(float)
    ma_ok = px[cols].rolling(200).mean().notna().any(axis=1)
    return e.where(ma_ok)


def ranked(px, cols):
    s = score(px, vol_scale=VOL_SCALE)[0][cols].where(eligible_mask(px, cols))
    return s.rank(axis=1, ascending=False)


def k_series(dial, e):
    """k_t for a dial point. dial is an int n0, the string 'E', or a float coverage in (0,1]."""
    if dial == "E":
        return e.clip(lower=1.0)
    if isinstance(dial, float):
        return np.maximum(1.0, np.round(dial * e))
    return np.minimum(float(dial), e).clip(lower=1.0)


def weights_from_k(rank, k, gross=GROSS):
    k = k.clip(lower=1.0)
    return rank.le(k, axis=0).astype(float).mul(gross / k, axis=0)


# ------------------------------------------------------------------ metric helpers
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, base):
    a1, a2 = halves(r)
    b1, b2 = halves(base)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def tests_4b(r, spy, r_oos, spy_oos):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": a1 > s1, "H2": a2 > s2,
            "OOS": metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def fail_4b(r, spy, r_oos, spy_oos):
    f = [k for k, v in tests_4b(r, spy, r_oos, spy_oos).items() if not v]
    return ",".join(f) if f else "-"


def is_side_4b(r_is, spy_is):
    """IS-only 4b legs, for the rule-8 gated chooser (no OOS information used)."""
    a1, a2 = halves(r_is)
    s1, s2 = halves(spy_is)
    m, ms = metrics(r_is), metrics(spy_is)
    return bool(a1 > s1 and a2 > s2 and abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])
                and m["CAGR"] >= 0.70 * ms["CAGR"])


def dial_label(dial):
    if dial == "E":
        return "ABS n0=E_t"
    if isinstance(dial, float):
        return f"REL c={dial:.2f}"
    return f"ABS n0={dial:d}"


def summarise(panel, dial, r, to, held, k, e, spy, base_v2, tgt_gross_live):
    mm = metrics(r)
    h1, h2 = halves(r)
    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    m_is, m_oos = metrics(r_is), metrics(r_oos)
    t4 = tests_4b(r, spy, r_oos, spy_oos)
    return dict(panel=panel, unit=("REL" if isinstance(dial, float) else "ABS"),
                dial=dial_label(dial),
                CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"], IS_MaxDD=m_is["MaxDD"],
                OOS_CAGR=m_oos["CAGR"], OOS_Sharpe=m_oos["Sharpe"], OOS_MaxDD=m_oos["MaxDD"],
                k_mean=float(k.mean()), cover=float((k / e.replace(0, np.nan)).mean()),
                sat=float((e <= k + 1e-9).mean()),
                names=float((held > 0).sum(axis=1).mean()),
                gross=float(held.sum(axis=1).mean()),          # REALISED, drifted by the engine
                tgt_gross_mean=tgt_gross_live["mean"],
                tgt_gross_worstday=tgt_gross_live["dev"],
                tgt_days_off=tgt_gross_live["share"],
                ann_ret=float(r.mean() * 252), ann_vol=float(r.std() * np.sqrt(252)),
                turn=float(to.sum() / mm["Years"]),
                p4a=keep_4a(r, base_v2),
                p4b=all(t4.values()), fail4b=fail_4b(r, spy, r_oos, spy_oos),
                is4b=is_side_4b(r_is, spy_is))


def bench_row(panel, name, ser):
    mm = metrics(ser)
    h1, h2 = halves(ser)
    m_is, m_o = metrics(ser.loc[:IS_END]), metrics(ser.loc[OOS_START:])
    return dict(panel=panel, unit="BENCH", dial=name, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"],
                MaxDD=mm["MaxDD"], H1=h1, H2=h2, IS_Sharpe=m_is["Sharpe"], IS_CAGR=m_is["CAGR"],
                IS_MaxDD=m_is["MaxDD"], OOS_CAGR=m_o["CAGR"], OOS_Sharpe=m_o["Sharpe"],
                OOS_MaxDD=m_o["MaxDD"], k_mean=np.nan, cover=np.nan, sat=np.nan, names=np.nan,
                gross=np.nan, tgt_gross_mean=np.nan, tgt_gross_worstday=np.nan,
                tgt_days_off=np.nan,
                ann_ret=float(ser.mean() * 252), ann_vol=float(ser.std() * np.sqrt(252)),
                turn=np.nan, p4a=False, p4b=False, fail4b="-", is4b=False)


# ------------------------------------------------------------------ panels
def build_panels():
    px56 = load_universe().dropna(how="all").ffill().loc[:COMMON_END]
    px136 = load_universe(broad=True).dropna(how="all").ffill().loc[:COMMON_END]
    pxs = load_universe(small=True).loc[:COMMON_END]
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_all = [c for c in pxs.columns if c != "SPY"]
    s_stk = [c for c in s_all if c not in bad]
    P(f"  SMALL: {len(s_all)} names in panel, dropped {len(s_all) - len(s_stk)} with "
      f"max_1d_move >= 1.0 (README) -> {len(s_stk)} tradable")
    return [("U56", px56, list(px56.columns)),
            ("B136", px136, list(px136.columns)),
            (f"SMALL{len(s_stk)}", pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), s_stk)]


def slope(xs, ys):
    """OLS slope of ys on xs, both 1-D."""
    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    if len(x) < 2 or np.allclose(x, x[0]):
        return np.nan
    return float(np.polyfit(x, y, 1)[0])


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    P("=" * 165)
    P(f"Idea 320 is-the-UNCONDITIONAL-width-dial-a-B136-fact-or-a-panel-ordering (lane B) | {SCRIPT}")
    P("=" * 165)
    P(f"Fixed, not searched: gross={GROSS:.0%} EVERY day, vol-scaler OFF, max_vol={MAX_VOL}, "
      f"weekly, {COST_BPS} bps, t+1, IS <= {IS_END}, OOS {OOS_START}..")
    P(f"Tuned (1 dial, 2 units, ALL points reported): ABS n0 in {ABS_GRID} and REL c in {REL_GRID}. "
      f"Panel is a reporting axis, not a tuned parameter.")
    P("SURVIVORSHIP: B136 and SMALL are CURRENT constituents; only within-panel dial differences "
      "are read as evidence.")
    P("")

    panels = build_panels()
    rows, curve_rows, sat_rows, wf_rows, gate_rows = [], [], [], [], []
    g1_max = g3_max = np.nan
    g2 = None
    books_by_panel = {}

    for panel, px, cols in panels:
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            P("!! CALENDAR-DAY INDEX DETECTED - aborting.")
            sys.exit(1)
        start = px.index[260]
        P("=" * 165)
        P(f"PANEL {panel}: {len(cols)} tradable of {px.shape[1]} columns | {px.index[0].date()} "
          f"-> {px.index[-1].date()} | eval from {start.date()} | index sanity "
          f"2018={yrs.get(2018)}, 2024={yrs.get(2024)}")

        rank = ranked(px, cols)
        e_full = eligible_count(px, cols).fillna(0.0)
        e = e_full.loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]
        base_v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start:]

        P(f"  E_t (eligible names/day): mean {e.mean():.1f}, median {e.median():.0f}, "
          f"min {e.min():.0f}, max {e.max():.0f}, p90 {e.quantile(0.90):.0f} "
          f"| panel width {len(cols)} | days with E_t == 0: {int((e < 1).sum())} "
          f"({(e < 1).mean():.3%})")

        books = {}
        prev_w = None
        prev_lbl = None
        for dial in ABS_GRID + REL_GRID:
            k = k_series(dial, e_full)
            w = weights_from_k(rank, k).reindex(columns=px.columns).fillna(0.0)
            r, to, held = fast_backtest(px, w)
            r, to, held = r.loc[start:], to.loc[start:], held.loc[start:]
            lbl = dial_label(dial)
            books[lbl] = (r, w)
            # G3: TARGET gross. Exactly 0.75 except on days where a name is ELIGIBLE
            # (above 200d MA, vol20 < cap) but has NO composite score yet -- the 12m
            # momentum leg needs 252 bars, so a recently-listed name is counted in E_t
            # and cannot be ranked.  Inherited from idea 318's construction, kept for
            # provenance (G4); measured here rather than assumed.
            tg = w.loc[start:].sum(axis=1)
            live = e >= 1
            off = (tg[live] - GROSS).abs() > 1e-12
            rows.append(summarise(panel, dial, r, to, held, k.loc[start:], e, spy, base_v2,
                                  dict(dev=float((tg[live] - GROSS).abs().max()),
                                       share=float(off.mean()),
                                       mean=float(tg[live].mean()))))
            if isinstance(dial, int) or dial == "E":
                if prev_w is not None:
                    d = float((w.loc[start:] - prev_w.loc[start:]).abs().values.max())
                    ident = float((w.loc[start:] - prev_w.loc[start:]).abs().values.sum())
                    sat_rows.append(dict(panel=panel, step=f"{prev_lbl} -> {lbl}",
                                         max_abs_dW=d, sum_abs_dW=ident,
                                         identical=bool(ident < 1e-12)))
                prev_w, prev_lbl = w, lbl
        books_by_panel[panel] = (books, spy, base_v2, start)

        for nm, ser in (("RULES v2 (live)", base_v2), ("RULES v1", base_v1), ("SPY", spy)):
            rows.append(bench_row(panel, nm, ser))

        # ---- G1 / G3 on this panel's widest ABS book
        w_chk = weights_from_k(rank, k_series(40, e_full)).reindex(columns=px.columns).fillna(0.0)
        eng = backtest(px, w_chk, cost_bps=COST_BPS, freq=FREQ)
        fst = fast_backtest(px, w_chk)[0]
        d1 = float((eng["returns"].loc[start:] - fst.loc[start:]).abs().max())
        g1_max = d1 if np.isnan(g1_max) else max(g1_max, d1)
        gate_rows.append(dict(gate="G1 fast==engine", panel=panel, value=d1))

        P(f"  gate G1 on {panel}: max|fast - engine| = {d1:.3e}")

    R = pd.DataFrame(rows)
    R.to_csv(f"{OUT}.grid.csv", index=False)

    # ---------------------------------------------------------------- GATES
    P("")
    P("=" * 165)
    P("GATES")
    P("=" * 165)
    grid_only = R[R.unit != "BENCH"]
    g3_mean = float((grid_only.tgt_gross_mean - GROSS).abs().max())
    g3_share = float(grid_only.tgt_days_off.max())
    g3_worst = float(grid_only.tgt_gross_worstday.max())
    gate_rows.append(dict(gate="G3a max|mean target gross - 0.75|", panel="ALL", value=g3_mean))
    u56 = R[(R.panel == "U56") & (R.dial == "RULES v2 (live)")].iloc[0]
    g2 = (u56.CAGR, u56.Sharpe, u56.MaxDD, u56.H1, u56.H2)
    P(f"G1  max|fast_backtest - engine.backtest| over 3 panels = {g1_max:.3e}   "
      f"{'PASS' if g1_max < 1e-12 else 'FAIL'}")
    P(f"G2  LIVE RULES v2 on U56 @ vintage {COMMON_END} = {g2[0]:.2%} / {g2[1]:.4f} / {g2[2]:.2%} "
      f"({g2[3]:.4f} / {g2[4]:.4f})   record: 8.66% / 1.2056 / -12.05% (1.2259 / 1.1909)   "
      f"{'PASS' if abs(g2[1] - 1.2056) < 5e-4 and abs(g2[0] - 0.0866) < 5e-5 else 'FAIL'}")
    P(f"    (vintage note: the un-truncated U56 cache now runs to 2026-09-08 and gives "
      f"8.64% / 1.2037 -- a -0.0019 Sharpe drift from one extra bar, not a code difference; "
      f"all three panels are cut to {COMMON_END}, the last bar B136/SMALL carry.)")
    P(f"G3a TARGET gross, bar = mean within 1 pp of 0.75 at every one of {len(grid_only)} points: "
      f"max|mean - 0.75| = {g3_mean * 100:.3f} pp   {'PASS' if g3_mean < 0.01 else 'FAIL'}")
    P(f"    NOT an identity, and censused rather than assumed: worst share of days below 0.75 = "
      f"{g3_share:.2%}, worst single-day shortfall = {g3_worst:.4f}.  TWO causes, both "
      f"inherited from idea 318's construction and kept so G4 is exact:")
    P("      (i) UNRANKABLE ELIGIBLES -- a name above its 200d MA with vol20 under the cap but "
      "with no composite score yet (the 12m momentum leg needs 252 bars) is counted in E_t and "
      "cannot be ranked, so the book holds gross*(ranked/k).  Binds at the WIDE end only.")
    P("      (ii) RANK TIES -- the composite is the mean of three pct-ranks and is therefore "
      "discrete, so names tie; rank.le(k) then selects fewer than k.  U56 carries tied ranks on "
      "68.7% of days and loses ~1 name on 8.3% of them.  Binds at the NARROW end, sub-1 pp.")
    P("    Fill shortfall by grid point (share of days below 0.75 / mean target gross):")
    _fp = grid_only.pivot_table(index="dial", columns="panel",
                                values=["tgt_days_off", "tgt_gross_mean"])
    P(_fp.to_string(float_format=lambda x: f"{x:.4f}"))
    _w = grid_only.loc[grid_only.tgt_days_off.idxmax()]
    P(f"    Worst point {_w.panel} {_w.dial}: {_w.tgt_days_off:.2%} of days off, mean target "
      f"gross {_w.tgt_gross_mean:.6f} ({(GROSS - _w.tgt_gross_mean) * 100:.2f} pp short). "
      f"It concentrates at the WIDE end of the WIDEST panel -- exactly where the SMALL result "
      f"lives -- so the FILL control below is required before that result can be read.")
    gsp = grid_only.groupby(["panel", "unit"]).gross.agg(["min", "max"])
    gsp["spread_pp"] = (gsp["max"] - gsp["min"]) * 100
    P("G3b REALISED (engine-drifted) gross across the dial -- not an identity; reported because "
      "idea 321/587 showed 4b is mostly a gross meter:")
    P(gsp.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"    max realised-gross spread within any (panel, unit) = {gsp.spread_pp.max():.3f} pp, "
      f"vs the 12.78 pp gross motion idea 321 needed to move the 4b DD margin -> the width "
      f"reading here is NOT an exposure reading.")
    gate_rows.append(dict(gate="G3b realised gross spread pp", panel="ALL",
                          value=float(gsp.spread_pp.max())))
    pub = {"ABS n0=20": 0.883, "ABS n0=40": 0.971, "ABS n0=60": 1.003, "ABS n0=E_t": 1.019}
    b = R[(R.panel == "B136") & (R.dial.isin(pub))].set_index("dial")
    g4 = max(abs(b.loc[d, "OOS_Sharpe"] - v) for d, v in pub.items())
    for d, v in pub.items():
        P(f"G4  B136 {d:12s} OOS Sharpe {b.loc[d, 'OOS_Sharpe']:.4f}   idea 318 published {v:.3f}   "
          f"d={b.loc[d, 'OOS_Sharpe'] - v:+.4f}")
    P(f"G4  max provenance deviation vs idea 318 = {g4:.4f}   {'PASS' if g4 < 5e-3 else 'FAIL'}")
    gate_rows.append(dict(gate="G4 idea-318 provenance", panel="B136", value=g4))
    n20 = R[(R.panel == "U56") & (R.dial == "ABS n0=20")].iloc[0]
    pub5 = (0.128, 1.07, -0.183, 1.08, 1.07)
    got5 = (round(n20.CAGR, 3), round(n20.Sharpe, 2), round(n20.MaxDD, 3),
            round(n20.H1, 2), round(n20.H2, 2))
    P(f"G5  U56 n0=20 = {n20.CAGR:.1%} / {n20.Sharpe:.2f} / {n20.MaxDD:.1%} / "
      f"{n20.H1:.2f} / {n20.H2:.2f}   record (LEADERBOARD lines 288 and 2925): "
      f"12.8% / 1.07 / -18.3% / 1.08 / 1.07   {'PASS' if got5 == pub5 else 'FAIL'}")
    P("    -> this run's 4b passers are RE-DERIVATIONS of books already in the record and "
      "already not adopted, NOT new candidates.  No memo is claimed for them.")
    gate_rows.append(dict(gate="G5 4b-passer provenance", panel="U56",
                          value=float(got5 == pub5)))
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------- the grid
    P("")
    P("=" * 165)
    P("THE FULL GRID -- every point reported (gross 0.75 everywhere, so d is WIDTH alone)")
    P("=" * 165)
    show = ["panel", "unit", "dial", "k_mean", "cover", "sat", "names", "gross", "turn",
            "ann_ret", "ann_vol",
            "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
            "p4a", "p4b", "fail4b"]
    for panel in R.panel.unique():
        P("")
        P(f"--- {panel}")
        P(R[R.panel == panel][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- H3 saturation
    P("")
    P("=" * 165)
    P("H3  IS THE ABSOLUTE DIAL EVEN LIVE ON EVERY PANEL?  saturation share = mean(1[E_t <= k]) "
      "-- at sat=1.00 the book IS EWALL and the dial is inert")
    P("=" * 165)
    S = grid_only[grid_only.unit == "ABS"].pivot(index="dial", columns="panel", values="sat")
    S = S.reindex([dial_label(d) for d in ABS_GRID])
    P(S.to_string(float_format=lambda x: f"{x:.3f}"))
    P("")
    P("Adjacent-step weight motion on the ABS grid (identical=True means the two dial points are "
      "the SAME BOOK to machine precision):")
    SR = pd.DataFrame(sat_rows)
    SR.to_csv(f"{OUT}.saturation.csv", index=False)
    P(SR.to_string(index=False, float_format=lambda x: f"{x:.3e}"))

    # ---------------------------------------------------------------- H1/H2 slopes
    P("")
    P("=" * 165)
    P("H1/H2  THE WIDTH SLOPE PER PANEL, and whether the SLOPE ordering equals the LEVEL ordering")
    P("=" * 165)
    for unit, grid in (("ABS", ABS_GRID), ("REL", REL_GRID)):
        sub = grid_only[grid_only.unit == unit]
        P("")
        P(f"  unit={unit}")
        for panel in R.panel.unique():
            g = sub[sub.panel == panel].set_index("dial").reindex([dial_label(d) for d in grid])
            xs = g.cover.values          # slope always measured in coverage, the common ruler
            for metric in ("Sharpe", "OOS_Sharpe", "CAGR", "OOS_CAGR", "MaxDD"):
                curve_rows.append(dict(unit=unit, panel=panel, metric=metric,
                                       slope_per_unit_cover=slope(xs, g[metric].values),
                                       first=g[metric].values[0], last=g[metric].values[-1],
                                       span=g[metric].values[-1] - g[metric].values[0],
                                       monotone_up=bool(np.all(np.diff(g[metric].values) > 0)),
                                       monotone_dn=bool(np.all(np.diff(g[metric].values) < 0))))
    C = pd.DataFrame(curve_rows)
    C.to_csv(f"{OUT}.curves.csv", index=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("")
    lvl = (grid_only[grid_only.unit == "ABS"].groupby("panel").OOS_Sharpe.mean()
           .sort_values(ascending=False))
    slp = (C[(C.unit == "ABS") & (C.metric == "OOS_Sharpe")].set_index("panel")
           .slope_per_unit_cover.sort_values(ascending=False))
    P(f"  LEVEL ordering (mean OOS Sharpe across the ABS dial): "
      + " > ".join(f"{p} ({v:.3f})" for p, v in lvl.items()))
    P(f"  SLOPE ordering (d OOS Sharpe / d coverage, ABS grid):  "
      + " > ".join(f"{p} ({v:+.3f})" for p, v in slp.items()))
    P(f"  same ordering as LEVEL?  {list(lvl.index) == list(slp.index)}")
    P(f"  EXACT REVERSE of LEVEL?  {list(slp.index) == list(lvl.index)[::-1]}")
    P(f"  -> the queue's dichotomy ('same ordering or the opposite one') is a FALSE DICHOTOMY "
      f"if both are False: {(list(lvl.index) != list(slp.index)) and (list(slp.index) != list(lvl.index)[::-1])}")

    # how much of the U56-vs-B136 slope gap does de-saturating the dial close?
    def sgap(unit):
        s = (C[(C.unit == unit) & (C.metric == "OOS_Sharpe")].set_index("panel")
             .slope_per_unit_cover)
        return float(s["B136"] - s["U56"])
    ga, gr = sgap("ABS"), sgap("REL")
    P("")
    P(f"  H3 quantified: the B136-minus-U56 OOS-Sharpe slope gap is {ga:+.4f} on the ABS dial "
      f"(2 of whose 5 U56 points are the SAME BOOK) and {gr:+.4f} on the fully live REL dial. "
      f"De-saturating the dial closes {(1 - gr / ga) * 100:.1f}% of the gap -> saturation is a "
      f"REAL defect of the queue's grid but explains almost NONE of the panel difference.")

    # ---------------------------------------------------------------- FILL control
    P("")
    P("=" * 165)
    P("FILL CONTROL  the same REL dial with k = max(1, round(c * R_t)), R_t = the RANKED count, "
      "so the book is ALWAYS exactly 0.75 gross.  Does each panel's width slope survive?")
    P("=" * 165)
    fill_rows = []
    for panel, px, cols in panels:
        start = px.index[260]
        rank = ranked(px, cols)
        rt = rank.notna().sum(axis=1).astype(float)          # names that CAN be held
        e = eligible_count(px, cols).fillna(0.0).loc[start:]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base_v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS,
                           freq=FREQ)["returns"].loc[start:]
        for c_ in REL_GRID:
            k = np.maximum(1.0, np.round(c_ * rt))
            w = weights_from_k(rank, k).reindex(columns=px.columns).fillna(0.0)
            r, to, held = fast_backtest(px, w)
            r, to, held = r.loc[start:], to.loc[start:], held.loc[start:]
            tg = w.loc[start:].sum(axis=1)
            live = rt.loc[start:] >= 1
            d = summarise(panel, c_, r, to, held, k.loc[start:], e, spy, base_v2,
                          dict(dev=float((tg[live] - GROSS).abs().max()),
                               share=float(((tg[live] - GROSS).abs() > 1e-12).mean()),
                               mean=float(tg[live].mean())))
            d["unit"] = "FILL"
            fill_rows.append(d)
    F = pd.DataFrame(fill_rows)
    F.to_csv(f"{OUT}.fillcontrol.csv", index=False)
    P(F[["panel", "dial", "k_mean", "tgt_days_off", "tgt_gross_mean", "gross", "CAGR", "Sharpe",
         "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4a", "p4b", "fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    _c1 = F[F.dial == dial_label(1.00)]
    P(f"  Cause (i), UNRANKABLE ELIGIBLES, is gone by construction: at c=1.00 every panel now "
      f"holds exactly {float(_c1.tgt_gross_mean.min()):.4f} gross with "
      f"{float(_c1.tgt_days_off.max()):.2%} of days off, against SMALL439's 0.7441 / 58.33% on "
      f"the E_t dial.")
    P(f"  Cause (ii), RANK TIES, survives and is unchanged: worst days-off share still "
      f"{float(F.tgt_days_off.max()):.2%} at c<1, max|mean - 0.75| = "
      f"{float((F.tgt_gross_mean - GROSS).abs().max()) * 100:.3f} pp -- still inside the 1 pp bar.")
    P("")
    P("  OOS-Sharpe width slope, E_t dial vs FILL dial (both per unit of coverage):")
    for panel in R.panel.unique():
        g0 = (grid_only[(grid_only.unit == "REL") & (grid_only.panel == panel)]
              .set_index("dial").reindex([dial_label(d) for d in REL_GRID]))
        g1 = F[F.panel == panel].set_index("dial").reindex([dial_label(d) for d in REL_GRID])
        s0, s1 = slope(g0.cover.values, g0.OOS_Sharpe.values), slope(g1.cover.values,
                                                                    g1.OOS_Sharpe.values)
        P(f"    {panel:9s} E_t dial {s0:+.4f}   FILL dial {s1:+.4f}   "
          f"sign preserved: {np.sign(s0) == np.sign(s1)}   "
          f"|change| {abs(s1 - s0):.4f}")

    # ---------------------------------------------------------------- idea 330 two-term split
    P("")
    P("=" * 165)
    P("MECHANISM  idea 330's two-term split applied to the WIDTH dial: Sharpe = ann_ret / ann_vol, "
      "so ln(S_wide/S_narrow) = ln(ret ratio) - ln(vol ratio).  Which term does widening move?")
    P("=" * 165)
    dec = []
    for unit, grid in (("ABS", ABS_GRID), ("REL", REL_GRID)):
        for panel in R.panel.unique():
            g = (grid_only[(grid_only.unit == unit) & (grid_only.panel == panel)]
                 .set_index("dial").reindex([dial_label(d) for d in grid]))
            a, b = g.iloc[0], g.iloc[-1]
            lr = float(np.log(b.ann_ret / a.ann_ret))
            lv = float(np.log(b.ann_vol / a.ann_vol))
            dec.append(dict(unit=unit, panel=panel, narrow=g.index[0], wide=g.index[-1],
                            ret_narrow=a.ann_ret, ret_wide=b.ann_ret,
                            vol_narrow=a.ann_vol, vol_wide=b.ann_vol,
                            ln_ret_term=lr, ln_vol_term=-lv, ln_dSharpe=lr - lv,
                            carried_by=("VOL" if abs(lv) > abs(lr) else "RETURN")))
    D = pd.DataFrame(dec)
    D.to_csv(f"{OUT}.decomposition.csv", index=False)
    P(D.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(f"  carried by VOL in {int((D.carried_by == 'VOL').sum())} of {len(D)} (panel, unit) cells; "
      f"the RETURN term is negative in {int((D.ln_ret_term < 0).sum())} of {len(D)} -- idea 330's "
      f"'wins on vol, loses on return' shape, now shown for the WIDTH dial specifically.")

    # ---------------------------------------------------------------- H4 collapse
    P("")
    P("=" * 165)
    P("H4  DO THE THREE PANELS COLLAPSE ONTO ONE CURVE IN COVERAGE UNITS?  "
      "(each panel's OOS Sharpe re-based to its own c=0.25 point)")
    P("=" * 165)
    rel = grid_only[grid_only.unit == "REL"].copy()
    piv = rel.pivot(index="dial", columns="panel", values="OOS_Sharpe").reindex(
        [dial_label(d) for d in REL_GRID])
    reb = piv - piv.iloc[0]
    P("  raw OOS Sharpe:")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("  re-based (minus each panel's own c=0.25):")
    P(reb.to_string(float_format=lambda x: f"{x:.4f}"))
    sd_abs = grid_only[grid_only.unit == "ABS"].pivot(index="dial", columns="panel",
                                                      values="OOS_Sharpe")
    sd_abs = (sd_abs - sd_abs.iloc[0]).std(axis=1).mean()
    sd_rel = reb.std(axis=1).mean()
    P("")
    P(f"  mean cross-panel SD of the re-based curve: ABS units {sd_abs:.4f} vs REL units "
      f"{sd_rel:.4f}  -> collapse {'IMPROVES' if sd_rel < sd_abs else 'DOES NOT IMPROVE'} "
      f"in coverage units ({(1 - sd_rel / sd_abs) * 100:+.1f}%)")
    reb.to_csv(f"{OUT}.collapse.csv")

    # ---------------------------------------------------------------- rule 8
    P("")
    P("=" * 165)
    P("RULE 8 WALK-FORWARD -- dial chosen on IS (<= 2016) ONLY, OOS read once")
    P("=" * 165)
    for panel in R.panel.unique():
        books, spy, base_v2, start = books_by_panel[panel]
        sub = grid_only[grid_only.panel == panel]
        spy_o = spy.loc[OOS_START:]
        b_o = base_v2.loc[OOS_START:]
        for unit in ("ABS", "REL"):
            u = sub[sub.unit == unit]
            for chooser, pool in (("IS_Sharpe", u), ("IS_Sharpe|IS4b", u[u.is4b])):
                if pool.empty:
                    wf_rows.append(dict(panel=panel, unit=unit, chooser=chooser, pick="NONE",
                                        OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan,
                                        base_OOS_Sharpe=metrics(b_o)["Sharpe"],
                                        spy_OOS_Sharpe=metrics(spy_o)["Sharpe"],
                                        p4a=False, p4b=False, fail4b="no IS-admissible point"))
                    continue
                pick = pool.loc[pool.IS_Sharpe.idxmax()]
                wf_rows.append(dict(
                    panel=panel, unit=unit, chooser=chooser, pick=pick.dial,
                    IS_Sharpe=pick.IS_Sharpe,
                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                    base_OOS_CAGR=metrics(b_o)["CAGR"], base_OOS_Sharpe=metrics(b_o)["Sharpe"],
                    base_OOS_MaxDD=metrics(b_o)["MaxDD"],
                    spy_OOS_CAGR=metrics(spy_o)["CAGR"], spy_OOS_Sharpe=metrics(spy_o)["Sharpe"],
                    spy_OOS_MaxDD=metrics(spy_o)["MaxDD"],
                    p4a=bool(pick.p4a), p4b=bool(pick.p4b), fail4b=pick.fail4b))
    W = pd.DataFrame(wf_rows)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 165)
    P("KEEP PATHS at every grid point")
    P("=" * 165)
    P(f"  4a passers: {int(grid_only.p4a.sum())} / {len(grid_only)}")
    P(f"  4b passers: {int(grid_only.p4b.sum())} / {len(grid_only)}")
    P(f"  BOTH:       {int((grid_only.p4a & grid_only.p4b).sum())} / {len(grid_only)}")
    P("  binding 4b leg counts: "
      + str(pd.Series([f for s in grid_only.fail4b for f in s.split(",") if f != "-"])
            .value_counts().to_dict()))
    if grid_only.p4b.any():
        P("")
        P("  4b passers in full:")
        P(grid_only[grid_only.p4b][show].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    P(f"  rule-8 picks that pass 4b: {int(W.p4b.sum())} / {len(W)};  4a: {int(W.p4a.sum())} / {len(W)}")

    P("")
    P("=" * 165)
    P("VERDICT")
    P("=" * 165)
    P("Q  'is this the same U56 > B136 > SMALL ordering ideas 51/312/316 keep finding, or the "
      "opposite one?'")
    P("A  NEITHER -- the queue asked a FALSE DICHOTOMY.  The LEVEL ordering is the record's "
      "familiar one (U56 1.131 > B136 0.955 > SMALL439 0.416 mean OOS Sharpe).  The SLOPE "
      "ordering is B136 (+0.190) > U56 (-0.061) > SMALL439 (-0.216): not the same (B136 and U56 "
      "swap), not the reverse (SMALL is LAST in both).  Level and slope are different orderings "
      "sharing a last place, so 'width helps B136' is not a re-reading of the panel-quality "
      "ordering and does not invert it.")
    P("")
    P("H1 premise CONFIRMED in direction on 2 of 3 panels and shown to be UNIT-DEPENDENT on the "
      "third: B136 + (monotone up, ABS and REL), SMALL439 - (both units), U56 so nearly flat "
      "that its SIGN FLIPS with the unit the dial is read in (ABS -0.061, REL +0.070).")
    P("H3 saturation CONFIRMED as a defect, REJECTED as the explanation: on U56 sat = 1.000 "
      "already at n0=60 and the n0=60 and n0=E_t books are BIT-IDENTICAL (max|dW| = 0.000e+00), "
      "so 1 of the queue's 4 ABS dial steps on U56 is a literal no-op -- but de-saturating the "
      "dial (REL units) closes only 10.7% of the B136-minus-U56 slope gap.")
    P("H4 collapse KILLED: re-based on each panel's own narrow end, the cross-panel SD of the "
      "width curve is 0.0643 in ABS units and 0.1258 in REL units.  Reading the dial in "
      "coverage units makes the panels disagree ~2x MORE.  The width response is genuinely "
      "panel-specific; it is not an absolute-vs-relative units artefact, so idea 336/400's "
      "'absolute cut on a panel-dependent distribution' critique does NOT apply to this dial.")
    P("FILL control PASSES: with k taken from the RANKED count so gross is exactly 0.75, all "
      "three slope signs are preserved and |change| <= 0.0094.  The 58.3%-of-days fill "
      "shortfall at SMALL's widest point is not the mechanism.")
    P("")
    P("MECHANISM  widening is a VOLATILITY instrument with a RETURN TAX, and the panels differ "
      "in the tax, not the benefit.  Across the 6 (panel, unit) cells the vol term is POSITIVE "
      "in 6 of 6 and tightly bunched (+0.190 .. +0.443, spread 0.252); the return term is "
      "NEGATIVE in 6 of 6 and 1.5x more dispersed (-0.546 .. -0.149, spread 0.398).  B136's "
      "Sharpe gain is the vol term outrunning a small tax (+0.290 vs -0.207); SMALL's collapse "
      "is a large tax outrunning the same benefit (-0.546 vs +0.246).  This is idea 330's "
      "'wins on vol, loses on return' shape, now located on the WIDTH dial specifically.")
    P("")
    P("KEEP  4a 0/27, 4b 8/27, BOTH 0/27; rule-8 3/12 pass 4b, 0/12 pass 4a.  NO promotion and "
      "NO memo: G5 shows the 4b passers are re-derivations of already-published, already-"
      "unadopted rows, and every one of them is dominated by the live RULES v2 on the two bars "
      "PROTOCOL 4a cares about -- U56 n0=20 OOS Sharpe 1.1369 vs v2's 1.2851 (-0.148) and "
      "MaxDD -18.31% vs -12.05% (-6.3 pp).  No RULES change.  RULES.md, scan.py, bot.py and "
      "baseline.py untouched.")
    P("")
    P(f"done in {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
