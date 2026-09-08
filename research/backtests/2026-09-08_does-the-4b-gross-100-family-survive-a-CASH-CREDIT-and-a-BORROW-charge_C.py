#!/usr/bin/env python3
"""Idea 442 — does-the-4b-gross-1.00-family-survive-a-CASH-CREDIT-and-a-BORROW-charge
(lane C, 2026-09-08)

QUESTION (queue, verbatim intent)
  Idea 439's 126-book grid put ALL 19 of its 4b passes at gross 1.00 (the live book's 25%
  cash carve-out removed) on U56 and B136 and 0 on SMALL439.  Every one of those books was
  priced with cash earning ZERO — the record's standing convention, flagged by open idea
  406.  Price that family against the live gross 0.75 book under idea 406's cash-credit
  conventions (0 / 150 / 300 bps) and say whether the whole 4b margin is the carve-out.

WHY THE CONVENTION IS NOT NEUTRAL
  RULES v2 de-grosses: gated-out weight goes to CASH, never re-spread.  So EVERY book here
  holds cash on most days, and the nominal gross dial is really a dial on HOW MUCH cash.
  Realised gross of the live U56 band-3 book is ~0.53 (0.75 nominal x ~0.71 admission), of
  the same book at nominal 1.00 ~0.71.  Pricing cash at 0 therefore taxes the low-gross
  arms by construction, and idea 439's "all 19 passes are at gross 1.00" could be nothing
  but that tax.  The symmetric completion is a BORROW charge: if cash pays r, then gross
  above 1.00 must PAY r.  Both are the same line of arithmetic, so the grid is extended
  past 1.00 to make the charge bite.

TWO TUNED PARAMETERS, ALL GRID POINTS REPORTED
  P1  GROSS in {0.50, 0.75, 1.00, 1.25, 1.50} — idea 439's three rungs plus two levered
      rungs so the borrow leg is exercised at all.
  P2  RATE in {0, 150, 300} bps/yr, applied SYMMETRICALLY (credit on cash, charge on
      borrow): dr_t = (rate/1e4)/252 * (1 - G_t), G_t = realised gross that day.
      rate = 0 is idea 439's own convention and must reproduce it exactly.
  Nothing else is tuned.  Panel {U56, B136, SMALL439}, cadence {W, M} and band width
  {0, .02, .03, .05, .08, .12, .20} are idea 439's REPORTED axes, imported unchanged and
  published in full: 3 x 5 x 2 x 7 = 210 books x 3 rates = 630 priced books, every one in
  .grid.csv and .keeppaths.csv.

TWO SHARPE READINGS (the crux, declared before any number is read)
  RAW     the record's convention: Sharpe = mean/vol with rf = 0.  Under RAW a cash credit
          is free return for the book and SPY gets nothing (SPY's G_t == 1, so the same
          formula credits it exactly 0).  This is the reading idea 406 proposes.
  EXCESS  the same rate is the risk-free rate for EVERYONE: subtract rate/252 from every
          daily series, SPY and both baselines included.  Algebraically the book's excess
          return collapses to r_t - rate*G_t/252 — i.e. the honest reading CHARGES a book
          for the capital it puts to work instead of paying it for the capital it does not.
  Both readings are computed for every one of the 630 books and both 4b verdicts published.
  A finding that only holds under RAW is a finding about the numeraire, not the book.

TWO EXTRA CONVENTIONS (reported, never selected on)
  ASYM  credit 0 / borrow 300 — idea 406's literal description of what idea 402 did.
  REAL  credit 150 / borrow 300 — a retail prime-broker shape.

RULE 8 (PROTOCOL 8)
  For each (panel, cadence, rate, reading) the pair (gross, band) is chosen on IS <=
  2016-12-31 by IS Sharpe alone and 2017-2026 is read ONCE, against RULES v2 (live), RULES
  v1 and SPY under the SAME convention.  Reported as OOS CAGR / Sharpe / MaxDD.

GATES (all asserted, printed with their errors)
  G1  fast_backtest == engine.backtest on RULES v2 / U56.
  G2  the rate-0 grid reproduces idea 439's committed .keeppaths.csv on its own 126 books.
  G3  rate 0 is an exact no-op on the credit path.
  G4  SPY's realised gross is identically 1, so RAW credits it exactly 0.

Costs 10 bps, weights at t applied at t+1 (PROTOCOL 2).
SURVIVORSHIP: B136 and SMALL439 are current constituents only — levels overstated; read
the WITHIN-panel gross/rate contrasts, which share the panel.
Artefacts: .console.txt, .grid.csv, .keeppaths.csv, .margin.csv, .grossband.csv,
           .breakeven.csv, .walkforward.csv, .extraconv.csv, .result.md.
           Nothing outside research/ is touched.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask  # noqa

BT = ROOT / "research" / "backtests"
STEM = "2026-09-08_does-the-4b-gross-100-family-survive-a-CASH-CREDIT-and-a-BORROW-charge_C"
REF = BT / "2026-09-08_census-every-CROSSING-in-the-record-for-dial-heterogeneity_C.keeppaths.csv"
LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ grid (idea 439's axes)
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
GROSSES = [0.50, 0.75, 1.00, 1.25, 1.50]          # P1
RATES = [0.0, 150.0, 300.0]                        # P2 (bps/yr, symmetric)
EXTRA = {"ASYM(0/300)": (0.0, 300.0), "REAL(150/300)": (150.0, 300.0)}
CADENCES = ["W", "M"]
COST_BPS = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LIVE_BAND, LIVE_GROSS = 0.03, 0.75


def fast_backtest(px, W, cost_bps=COST_BPS, freq="W"):
    """engine.backtest arithmetic, numpy inner loop; also returns the realised gross path."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); held = np.empty((n, k)); to = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - to * cost_bps / 1e4
    return pd.Series(port, index=px.index), pd.Series(held.sum(axis=1), index=px.index)


def apply_rate(r, G, credit, borrow=None):
    """Credit cash at `credit` bps and charge borrow at `borrow` bps (default = credit).
    dr_t = rate_t/252 * (1 - G_t), rate_t = credit where G_t <= 1 else borrow."""
    if borrow is None:
        borrow = credit
    c = np.where(G.values <= 1.0, credit, borrow) / 1e4 / 252.0
    return r + pd.Series(c * (1.0 - G.values), index=r.index)


def csd(r):
    """CAGR, Sharpe (rf=0 on whatever series is passed), MaxDD."""
    r = np.asarray(r, float)
    if len(r) < 60:
        return (np.nan,) * 3
    eq = np.cumprod(1 + r); yrs = len(r) / 252
    dd = eq / np.maximum.accumulate(eq) - 1
    vol = r.std() * np.sqrt(252)
    return (eq[-1] ** (1 / yrs) - 1, (r.mean() * 252) / vol if vol else np.nan, dd.min())


def profile(r):
    """Full CAGR/Sharpe/MaxDD + halves + IS/OOS on one daily return series."""
    fc, fs, fd = csd(r.values)
    h = len(r) // 2
    _, h1, _ = csd(r.iloc[:h].values)
    _, h2, _ = csd(r.iloc[h:].values)
    ic, iss, idd = csd(r.loc[:IS_END].values)
    oc, oss, odd = csd(r.loc[OOS_START:].values)
    return dict(CAGR=fc, Sharpe=fs, MaxDD=fd, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=iss, OOS_CAGR=oc, OOS_Sharpe=oss, OOS_MaxDD=odd)


def band_book(px, band, gross):
    """idea 439's `band_book`, verbatim (RULES v2 form: de-gross, never re-spread)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0) if band > 0 else \
        ew.where(px > px.rolling(200).mean(), 0.0)


def pass4b(row, spy, reading):
    """PROTOCOL 4b, priced under the same convention for the book and for SPY."""
    return bool(row["H1"] > spy["H1"] and row["H2"] > spy["H2"]
                and row["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and abs(row["MaxDD"]) <= 0.60 * abs(spy["MaxDD"])
                and row["CAGR"] >= 0.70 * spy["CAGR"])


def pass4a(row, v2):
    return bool(row["H1"] > v2["H1"] and row["H2"] > v2["H2"] and row["MaxDD"] >= v2["MaxDD"])


# ================================================================================== main
def main():
    P("=" * 118)
    P("IDEA 442 — DOES THE 4b GROSS-1.00 FAMILY SURVIVE A CASH CREDIT AND A BORROW CHARGE?")
    P("lane C, 2026-09-08.  P1 gross {0.50,0.75,1.00,1.25,1.50} x P2 rate {0,150,300} bps.")
    P("Reported axes (idea 439's, unchanged): panel x cadence x band = 42 cells per gross.")
    P("=" * 118)

    panels = {}
    for lab, kw in [("U56", {}), ("B136", dict(broad=True)), ("SMALL439", dict(small=True))]:
        px = load_universe(**kw)
        panels[lab] = px
        P(f"  {lab:10s} {px.shape[1]:4d} cols  {px.index[0].date()} -> {px.index[-1].date()}")

    # ------------------------------------------------------------------------- gate G1
    px0 = panels["U56"]
    W0 = rules_v2_weights(px0)
    a = engine_backtest(px0, W0, cost_bps=COST_BPS, freq="W")["returns"]
    b, g0 = fast_backtest(px0, W0, COST_BPS, "W")
    e1 = float(np.abs(a - b).max())
    P(f"\n  GATE G1  fast_backtest vs engine.backtest (RULES v2 / U56): max |diff| {e1:.3e}")
    assert e1 < 1e-12
    P(f"  GATE G3  rate 0 is a no-op: max |diff| "
      f"{float(np.abs(apply_rate(b, g0, 0.0) - b).max()):.3e}")
    assert float(np.abs(apply_rate(b, g0, 0.0) - b).max()) == 0.0
    P(f"           live U56 band-3 g=0.75 realised gross: mean {g0.iloc[260:].mean():.4f}  "
      f"p05 {g0.iloc[260:].quantile(0.05):.4f}  max {g0.iloc[260:].max():.4f}")

    # ------------------------------------------------ price every book once (rate applied after)
    P("\n" + "=" * 118)
    P("PRICING 210 BOOKS (3 panels x 5 gross x 2 cadence x 7 bands), 10 bps, t+1.")
    P("=" * 118)
    raw = {}          # (panel, gross, cadence, band) -> (returns, gross path), post warm-up
    bench = {}        # (panel, series) -> (returns, gross path)
    for lab, px in panels.items():
        st = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0)
        bench[(lab, "SPY")] = (spy_r.loc[st:], pd.Series(1.0, index=spy_r.index).loc[st:])
        for nm, Wf in [("RULES v2 (live)", rules_v2_weights), ("RULES v1", rules_v1_weights)]:
            r, g = fast_backtest(px, Wf(px), COST_BPS, "W")
            bench[(lab, nm)] = (r.loc[st:], g.loc[st:])
        for cd in CADENCES:
            for bnd in BANDS:
                for gr in GROSSES:
                    r, g = fast_backtest(px, band_book(px, bnd, gr), COST_BPS, cd)
                    raw[(lab, gr, cd, bnd)] = (r.loc[st:], g.loc[st:])
        P(f"  {lab:10s} priced {len([k for k in raw if k[0] == lab])} books")

    # gate G4
    e4 = max(float(np.abs(bench[(l, 'SPY')][1] - 1.0).max()) for l in panels)
    P(f"\n  GATE G4  SPY realised gross deviation from 1.0: {e4:.3e} "
      f"(so RAW credits SPY exactly 0 by the same formula)")
    assert e4 == 0.0

    P("\n  Realised gross by nominal gross (U56, weekly, band 0.03), post warm-up:")
    P(f"  {'nominal':>8s} {'mean':>8s} {'p05':>8s} {'p95':>8s} {'frac days > 1':>14s}")
    for gr in GROSSES:
        g = raw[("U56", gr, "W", 0.03)][1]
        P(f"  {gr:8.2f} {g.mean():8.4f} {g.quantile(0.05):8.4f} {g.quantile(0.95):8.4f} "
          f"{(g > 1).mean():14.3f}")

    # ------------------------------------------------------------------- the 630-book grid
    P("\n" + "=" * 118)
    P("THE GRID — every book x rate x reading (630 books x 2 readings, all points reported)")
    P("=" * 118)
    rows = []
    for (lab, gr, cd, bnd), (r, g) in raw.items():
        for rate in RATES:
            rr = apply_rate(r, g, rate)
            for reading in ("RAW", "EXCESS"):
                s = rr - rate / 1e4 / 252.0 if reading == "EXCESS" else rr
                d = profile(s)
                d.update(panel=lab, gross=gr, cadence=cd, band=bnd, rate=rate,
                         reading=reading, mean_gross=float(g.mean()))
                rows.append(d)
    G = pd.DataFrame(rows)

    brows = []
    for (lab, nm), (r, g) in bench.items():
        for rate in RATES:
            rr = apply_rate(r, g, rate)
            for reading in ("RAW", "EXCESS"):
                s = rr - rate / 1e4 / 252.0 if reading == "EXCESS" else rr
                d = profile(s)
                d.update(panel=lab, series=nm, rate=rate, reading=reading,
                         mean_gross=float(g.mean()))
                brows.append(d)
    B = pd.DataFrame(brows)

    P("\n  Benchmarks under each convention (full-sample CAGR / Sharpe / MaxDD, OOS Sharpe):")
    P(f"  {'panel':9s} {'series':16s} {'rd':7s} {'rate':>5s} {'CAGR':>8s} {'Sharpe':>8s} "
      f"{'MaxDD':>8s} {'OOS Sh':>8s} {'meanG':>7s}")
    for _, x in B.sort_values(["panel", "series", "reading", "rate"]).iterrows():
        P(f"  {x.panel:9s} {x.series:16s} {x.reading:7s} {x.rate:5.0f} {x.CAGR:8.2%} "
          f"{x.Sharpe:8.4f} {x.MaxDD:8.2%} {x.OOS_Sharpe:8.4f} {x.mean_gross:7.4f}")

    # ------------------------------------------------------------------------ gate G2
    ref = pd.read_csv(REF)
    cur = G[(G.rate == 0) & (G.reading == "RAW") & (G.gross <= 1.0)]
    key = ["panel", "gross", "cadence", "band"]
    j = ref.merge(cur, on=key, suffixes=("_ref", "_new"))
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]
    err = max(float(np.abs(j[c + "_ref"] - j[c + "_new"]).max()) for c in cols)
    P(f"\n  GATE G2  reproduction of idea 439's committed 126 books (rate 0, RAW): "
      f"{len(j)} rows matched, max |diff| over {cols} = {err:.3e}")
    assert len(j) == 126 and err < 1e-12

    # ------------------------------------------------------------------- both KEEP paths
    P("\n" + "=" * 118)
    P("BOTH KEEP PATHS on all 630 books (4a vs the LIVE RULES v2 on the book's own panel;")
    P("4b vs SPY: Sharpe > SPY in H1, H2 and OOS, |MaxDD| <= 60% of SPY's, CAGR >= 70%),")
    P("book and comparands priced under the SAME convention.")
    P("=" * 118)
    krows = []
    for _, x in G.iterrows():
        spy = B[(B.panel == x.panel) & (B.series == "SPY") & (B.rate == x.rate)
                & (B.reading == x.reading)].iloc[0]
        v2 = B[(B.panel == x.panel) & (B.series == "RULES v2 (live)") & (B.rate == x.rate)
               & (B.reading == x.reading)].iloc[0]
        krows.append(dict(x, pass4a=pass4a(x, v2), pass4b=pass4b(x, spy, x.reading),
                          spy_H1=spy.H1, spy_H2=spy.H2, spy_OOS=spy.OOS_Sharpe,
                          spy_CAGR=spy.CAGR, spy_MaxDD=spy.MaxDD,
                          v2_H1=v2.H1, v2_H2=v2.H2, v2_MaxDD=v2.MaxDD))
    K = pd.DataFrame(krows)

    P(f"\n  4b passes by reading x rate x gross (each cell out of 42 books):")
    for reading in ("RAW", "EXCESS"):
        P(f"  --- {reading}")
        P(f"  {'rate':>5s} " + " ".join(f"{g:>10.2f}" for g in GROSSES) + f" {'TOTAL':>8s}")
        for rate in RATES:
            s = K[(K.reading == reading) & (K.rate == rate)]
            cells = [int(s[s.gross == g].pass4b.sum()) for g in GROSSES]
            P(f"  {rate:5.0f} " + " ".join(f"{c:>10d}" for c in cells) +
              f" {sum(cells):8d}")
    P(f"\n  4a passes by reading x rate x gross:")
    for reading in ("RAW", "EXCESS"):
        P(f"  --- {reading}")
        P(f"  {'rate':>5s} " + " ".join(f"{g:>10.2f}" for g in GROSSES) + f" {'TOTAL':>8s}")
        for rate in RATES:
            s = K[(K.reading == reading) & (K.rate == rate)]
            cells = [int(s[s.gross == g].pass4a.sum()) for g in GROSSES]
            P(f"  {rate:5.0f} " + " ".join(f"{c:>10d}" for c in cells) + f" {sum(cells):8d}")

    P(f"\n  4b passes by panel (all rates, all gross):")
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            s = K[(K.reading == reading) & (K.rate == rate)]
            by = " ".join(f"{l} {int(s[s.panel == l].pass4b.sum()):d}/{len(s[s.panel == l])}"
                          for l in panels)
            P(f"    {reading:7s} rate {rate:5.0f}   {by}")

    # which binding bar kills the 0.75 family
    P("\n  BINDING BAR on the gross-0.75 family (why each of its 42 books fails 4b), by rate:")
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            s = K[(K.reading == reading) & (K.rate == rate) & (K.gross == 0.75) & (~K.pass4b)]
            bars = dict(H1=0, H2=0, OOS=0, DD=0, CAGR=0)
            for _, x in s.iterrows():
                if x.H1 <= x.spy_H1: bars["H1"] += 1
                if x.H2 <= x.spy_H2: bars["H2"] += 1
                if x.OOS_Sharpe <= x.spy_OOS: bars["OOS"] += 1
                if abs(x.MaxDD) > 0.60 * abs(x.spy_MaxDD): bars["DD"] += 1
                if x.CAGR < 0.70 * x.spy_CAGR: bars["CAGR"] += 1
            P(f"    {reading:7s} rate {rate:5.0f}  fails {len(s):2d}/42  " +
              "  ".join(f"{k} {v}" for k, v in bars.items()))

    # ------------------------------------------------------- the margin: is it the carve-out?
    P("\n" + "=" * 118)
    P("THE MARGIN — gross 1.00 minus gross 0.75 on the SAME (panel, cadence, band) cell,")
    P("42 paired cells per rate x reading.  If the whole 4b margin is the cash carve-out,")
    P("crediting cash should drive these to zero.")
    P("=" * 118)
    mrows = []
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            s = K[(K.reading == reading) & (K.rate == rate)]
            a1 = s[s.gross == 1.00].set_index(["panel", "cadence", "band"])
            a0 = s[s.gross == 0.75].set_index(["panel", "cadence", "band"])
            for k_ in a1.index:
                x, y = a1.loc[k_], a0.loc[k_]
                mrows.append(dict(reading=reading, rate=rate, panel=k_[0], cadence=k_[1],
                                  band=k_[2], dSharpe=x.Sharpe - y.Sharpe,
                                  dCAGR=x.CAGR - y.CAGR, dMaxDD=x.MaxDD - y.MaxDD,
                                  dOOS=x.OOS_Sharpe - y.OOS_Sharpe,
                                  d4b=int(x.pass4b) - int(y.pass4b)))
    M = pd.DataFrame(mrows)
    P(f"\n  {'reading':8s} {'rate':>5s} {'mean dSharpe':>13s} {'>0':>5s} {'mean dCAGR':>11s} "
      f"{'mean dMaxDD':>12s} {'mean dOOS':>10s} {'d4b>0':>6s}")
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            s = M[(M.reading == reading) & (M.rate == rate)]
            P(f"  {reading:8s} {rate:5.0f} {s.dSharpe.mean():+13.4f} "
              f"{(s.dSharpe > 0).mean():5.2f} {s.dCAGR.mean():+11.2%} "
              f"{s.dMaxDD.mean():+12.2%} {s.dOOS.mean():+10.4f} {int((s.d4b > 0).sum()):6d}")

    P("\n  Same margin on the LIVE cell only (band 0.03, weekly) per panel:")
    P(f"  {'panel':9s} {'reading':8s} {'rate':>5s} {'S(1.00)':>8s} {'S(0.75)':>8s} "
      f"{'dSharpe':>8s} {'dCAGR':>8s} {'4b 1.00':>8s} {'4b 0.75':>8s}")
    for lab in panels:
        for reading in ("RAW", "EXCESS"):
            for rate in RATES:
                s = K[(K.reading == reading) & (K.rate == rate) & (K.panel == lab)
                      & (K.cadence == "W") & (K.band == LIVE_BAND)]
                x = s[s.gross == 1.00].iloc[0]; y = s[s.gross == 0.75].iloc[0]
                P(f"  {lab:9s} {reading:8s} {rate:5.0f} {x.Sharpe:8.4f} {y.Sharpe:8.4f} "
                  f"{x.Sharpe - y.Sharpe:+8.4f} {x.CAGR - y.CAGR:+8.2%} "
                  f"{str(bool(x.pass4b)):>8s} {str(bool(y.pass4b)):>8s}")

    # ------------------------------------------- what the 4b bars actually are: a GROSS WINDOW
    P("\n" + "=" * 118)
    P("THE ADMISSIBLE GROSS BAND — Sharpe is ~invariant in gross (idea 311), so on this dial")
    P("4b is two SCALE bars: CAGR >= 0.70 x SPY sets a FLOOR on gross, |MaxDD| <= 0.60 x SPY")
    P("sets a CEILING.  Both solved by linear interpolation between the reported rungs.")
    P("=" * 118)
    arows = []
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            for lab in panels:
                for cd in CADENCES:
                    for bnd in BANDS:
                        s = K[(K.reading == reading) & (K.rate == rate) & (K.panel == lab)
                              & (K.cadence == cd) & (K.band == bnd)].sort_values("gross")
                        gs = s.gross.values
                        spanS = float(s.Sharpe.max() - s.Sharpe.min())

                        def solve(y, target, rising):
                            for i in range(len(y) - 1):
                                a_, b_ = y[i], y[i + 1]
                                if (a_ < target <= b_) if rising else (a_ > target >= b_):
                                    return gs[i] + (gs[i + 1] - gs[i]) * (target - a_) / (b_ - a_)
                            return np.nan

                        floor = solve(s.CAGR.values, 0.70 * s.spy_CAGR.iloc[0], True)
                        ceil = solve(np.abs(s.MaxDD.values), 0.60 * abs(s.spy_MaxDD.iloc[0]), True)
                        h1f = solve(s.H1.values, s.spy_H1.iloc[0], True)
                        arows.append(dict(reading=reading, rate=rate, panel=lab, cadence=cd,
                                          band=bnd, g_floor_CAGR=floor, g_ceil_DD=ceil,
                                          width=ceil - floor if np.isfinite(floor) and
                                          np.isfinite(ceil) else np.nan,
                                          Sharpe_span_over_gross=spanS,
                                          n4b=int(s.pass4b.sum())))
    A = pd.DataFrame(arows)
    P(f"\n  Sharpe span across the 5 gross rungs within a cell (should be ~0 if the dial is")
    P(f"  a pure scalar): median {A.Sharpe_span_over_gross.median():.4f}, "
      f"p95 {A.Sharpe_span_over_gross.quantile(0.95):.4f}, max {A.Sharpe_span_over_gross.max():.4f}")
    P(f"\n  {'reading':8s} {'rate':>5s} {'panel':9s} {'med g floor':>11s} {'med g ceil':>10s} "
      f"{'med width':>10s} {'cells with a band':>18s}")
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            for lab in panels:
                s = A[(A.reading == reading) & (A.rate == rate) & (A.panel == lab)]
                ok = int((s.width > 0).sum())
                P(f"  {reading:8s} {rate:5.0f} {lab:9s} {s.g_floor_CAGR.median():11.3f} "
                  f"{s.g_ceil_DD.median():10.3f} {s.width.median():10.3f} {ok:14d}/{len(s)}")
    P("\n  The live U56 cell (W, band 0.03) — the whole verdict in one line per rate:")
    for reading in ("RAW", "EXCESS"):
        for rate in RATES:
            s = A[(A.reading == reading) & (A.rate == rate) & (A.panel == "U56")
                  & (A.cadence == "W") & (A.band == LIVE_BAND)].iloc[0]
            P(f"    {reading:7s} rate {rate:5.0f}  admissible gross "
              f"[{s.g_floor_CAGR:.3f}, {s.g_ceil_DD:.3f}]  width {s.width:.3f}  "
              f"(live book sits at {LIVE_GROSS:.2f})")
    A.to_csv(BT / f"{STEM}.grossband.csv", index=False)

    # ------------------------------------------------------- breakeven rate (derived, not tuned)
    P("\n" + "=" * 118)
    P("BREAKEVEN CREDIT RATE — the rate at which the gross-0.75 book catches the gross-1.00")
    P("book on each bar, per cell.  Scanned 0..2000 bps in 25 bps steps (derived, not tuned).")
    P("=" * 118)
    scan = np.arange(0, 2001, 25.0)
    brk = []
    for lab, px in panels.items():
        for cd in CADENCES:
            for bnd in BANDS:
                r1, g1 = raw[(lab, 1.00, cd, bnd)]
                r0, g0_ = raw[(lab, 0.75, cd, bnd)]
                for reading in ("RAW", "EXCESS"):
                    got = {}
                    for bar in ("Sharpe", "CAGR", "OOS_Sharpe"):
                        got[bar] = np.nan
                    for c in scan:
                        s1 = apply_rate(r1, g1, c); s0 = apply_rate(r0, g0_, c)
                        if reading == "EXCESS":
                            s1 = s1 - c / 1e4 / 252.0; s0 = s0 - c / 1e4 / 252.0
                        p1, p0 = profile(s1), profile(s0)
                        for bar in ("Sharpe", "CAGR", "OOS_Sharpe"):
                            if np.isnan(got[bar]) and p0[bar] >= p1[bar]:
                                got[bar] = c
                        if all(not np.isnan(v) for v in got.values()):
                            break
                    brk.append(dict(panel=lab, cadence=cd, band=bnd, reading=reading,
                                    be_Sharpe=got["Sharpe"], be_CAGR=got["CAGR"],
                                    be_OOS=got["OOS_Sharpe"]))
    BE = pd.DataFrame(brk)
    P(f"\n  {'reading':8s} {'panel':9s} {'median be Sharpe':>17s} {'median be CAGR':>15s} "
      f"{'median be OOS':>14s} {'cells never':>12s}")
    for reading in ("RAW", "EXCESS"):
        for lab in panels:
            s = BE[(BE.reading == reading) & (BE.panel == lab)]
            never = int(s.be_Sharpe.isna().sum())
            P(f"  {reading:8s} {lab:9s} {s.be_Sharpe.median():17.0f} "
              f"{s.be_CAGR.median():15.0f} {s.be_OOS.median():14.0f} {never:12d}")

    # ----------------------------------------------------------------------- rule 8
    P("\n" + "=" * 118)
    P("RULE 8 WALK-FORWARD — (gross, band) chosen on IS <= 2016 by IS Sharpe, 2017-2026 read")
    P("ONCE.  One row per (panel, cadence, rate, reading); comparands under the same convention.")
    P("=" * 118)
    wf = []
    for lab in panels:
        for cd in CADENCES:
            for rate in RATES:
                for reading in ("RAW", "EXCESS"):
                    s = G[(G.panel == lab) & (G.cadence == cd) & (G.rate == rate)
                          & (G.reading == reading)]
                    pick = s.loc[s.IS_Sharpe.idxmax()]
                    spy = B[(B.panel == lab) & (B.series == "SPY") & (B.rate == rate)
                            & (B.reading == reading)].iloc[0]
                    v2 = B[(B.panel == lab) & (B.series == "RULES v2 (live)")
                           & (B.rate == rate) & (B.reading == reading)].iloc[0]
                    v1 = B[(B.panel == lab) & (B.series == "RULES v1") & (B.rate == rate)
                           & (B.reading == reading)].iloc[0]
                    oracle = s.OOS_Sharpe.max()
                    fixed = s[(s.gross == LIVE_GROSS) & (s.band == LIVE_BAND)].iloc[0]
                    wf.append(dict(panel=lab, cadence=cd, rate=rate, reading=reading,
                                   pick_gross=pick.gross, pick_band=pick.band,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD,
                                   prereg_OOS_Sharpe=fixed.OOS_Sharpe,
                                   prereg_OOS_CAGR=fixed.OOS_CAGR,
                                   spy_OOS_Sharpe=spy.OOS_Sharpe, spy_OOS_CAGR=spy.OOS_CAGR,
                                   spy_OOS_MaxDD=spy.OOS_MaxDD,
                                   v2_OOS_Sharpe=v2.OOS_Sharpe, v2_OOS_CAGR=v2.OOS_CAGR,
                                   v1_OOS_Sharpe=v1.OOS_Sharpe,
                                   oracle_OOS_Sharpe=oracle, regret=oracle - pick.OOS_Sharpe))
    WF = pd.DataFrame(wf)
    P(f"\n  {'panel':9s} {'cd':3s} {'rd':7s} {'rate':>5s} {'pick':>12s} {'OOS CAGR':>9s} "
      f"{'OOS Sh':>8s} {'OOS DD':>8s} {'SPY Sh':>8s} {'v2 Sh':>8s} {'regret':>7s}")
    for _, x in WF.sort_values(["panel", "cadence", "reading", "rate"]).iterrows():
        P(f"  {x.panel:9s} {x.cadence:3s} {x.reading:7s} {x.rate:5.0f} "
          f"{f'g{x.pick_gross:.2f}/b{x.pick_band:.2f}':>12s} {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:8.4f} {x.OOS_MaxDD:8.2%} {x.spy_OOS_Sharpe:8.4f} "
          f"{x.v2_OOS_Sharpe:8.4f} {x.regret:+7.4f}")
    P(f"\n  chooser beats SPY OOS in {int((WF.OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/{len(WF)}, "
      f"RULES v2 OOS in {int((WF.OOS_Sharpe > WF.v2_OOS_Sharpe).sum())}/{len(WF)}, "
      f"the pre-registered live (g0.75/b0.03) in "
      f"{int((WF.OOS_Sharpe > WF.prereg_OOS_Sharpe).sum())}/{len(WF)}; "
      f"mean regret {WF.regret.mean():+.4f}")
    P(f"  chooser picks gross 1.00+ in "
      f"{int((WF.pick_gross >= 1.0).sum())}/{len(WF)} cells "
      f"(RAW {int(((WF.reading == 'RAW') & (WF.pick_gross >= 1.0)).sum())}/{len(WF)//2}, "
      f"EXCESS {int(((WF.reading == 'EXCESS') & (WF.pick_gross >= 1.0)).sum())}/{len(WF)//2})")

    # -------------------------------------------------- extra conventions (reported only)
    P("\n" + "=" * 118)
    P("EXTRA CONVENTIONS (reported, never selected on): ASYM credit 0 / borrow 300 and REAL")
    P("credit 150 / borrow 300, on the LIVE cell (band 0.03, weekly), RAW reading.")
    P("=" * 118)
    P(f"  {'panel':9s} {'convention':14s} " + " ".join(f"{'S@'+f'{g:.2f}':>9s}" for g in GROSSES))
    erows = []
    for lab in panels:
        for nm, (cr, bo) in EXTRA.items():
            out = []
            for gr in GROSSES:
                r, g = raw[(lab, gr, "W", LIVE_BAND)]
                d = profile(apply_rate(r, g, cr, bo))
                out.append(d["Sharpe"])
                erows.append(dict(panel=lab, convention=nm, gross=gr, **d))
            P(f"  {lab:9s} {nm:14s} " + " ".join(f"{v:9.4f}" for v in out))
    E = pd.DataFrame(erows)

    # --------------------------------------------------------------------------- artefacts
    G.to_csv(BT / f"{STEM}.grid.csv", index=False)
    K.to_csv(BT / f"{STEM}.keeppaths.csv", index=False)
    M.to_csv(BT / f"{STEM}.margin.csv", index=False)
    BE.to_csv(BT / f"{STEM}.breakeven.csv", index=False)
    WF.to_csv(BT / f"{STEM}.walkforward.csv", index=False)
    E.to_csv(BT / f"{STEM}.extraconv.csv", index=False)
    (BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\nWrote {STEM}.{{grid,keeppaths,margin,grossband,breakeven,walkforward,extraconv}}.csv + console")
    (BT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
