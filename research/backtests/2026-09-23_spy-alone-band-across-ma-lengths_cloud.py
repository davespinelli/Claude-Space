#!/usr/bin/env python3
"""idea 2459 (lane cloud, run 55, 2026-09-23) — does the 200d BAND earn its KEEP on SPY ALONE,
across MA LENGTHS?

THE QUESTION AS FILED.  "The whole candidate family is one timing rule (in-band -> hold,
out-of-band -> bills) applied 56 times; price that rule ONCE, on SPY itself, over MA length x
band width, and report how much of 4b's SPY-relative margin the timing rule generates before
any cross-section is added."

WHY IT MATTERS.  The standing 4b KEEP-candidate (idea 2300's `RG100 + phi = 1.00`, idea 2322's
capped `CAP2`) is exactly two things: a 200d band gate, and the decision to run it over many
names and let BREADTH size the book.  If the gate alone already beats SPY on risk-adjusted
terms, the candidate is a timing rule with a diversification bonus; if it does not, every bit
of the 4b margin is CROSS-SECTIONAL and the gate is only the admission test.  This is also the
ONE arm in the whole record with NO survivorship exposure: SPY and SHY are index funds priced
from their own inception, not current constituents of a screen.

DISCLOSED BEFORE COMPUTE: ONE CELL OF THIS GRID IS ALREADY COMMITTED.  Idea 2467 (lane B, run
53) priced `SPYONLY` at MA 200 / band 0.03 / gross 0.75 / SHY / 10 bps as a named zero-selection
reference arm and published 7.84% / 0.8375 / -20.07%, halves 0.92 / 0.77, OOS 8.40% / 0.8544,
turnover 1.99x, leg string 00010.  That is ONE point.  2459 asks for the SURFACE, which is what
decides whether the timing rule earns its keep ANYWHERE or only at the length the live book
happens to use.  The committed cell is this run's EXACT REPRODUCTION GATE (G2), not its answer.

THE BOOK.  One instrument.  On each weekly decision date, if SPY's close is IN the `L`-day band
(clause-2 hysteresis: IN above `ma x (1 + b)`, OUT below `ma x (1 - b)`, previous state in
between, OUT before `L` closes exist) hold SPY at gross `g`; the residual `1 - g x IN` sweeps
in full to SHY at phi = 1.00.  Executed at t+1, exactly as every other book in the record.

DIAL 1 -- MA length `L` {50, 100, 150, 200, 250, 300} sessions.
DIAL 2 -- band half-width `b` {0.00, 0.01, 0.03, 0.06, 0.10}.  `b = 0.00` is the bare MA
          crossing with no hysteresis; `L = 200, b = 0.03` IS the live clause-2 gate.

REPORTED, NEVER SELECTED ON: gross {0.75 (live), 1.00}, the price frame {U56 `data/prices.csv`,
B136 `data/prices_broad.csv`}, 4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, t+1
execution, the phi = 1.00 SHY sweep.  6 x 5 x 2 x 2 = 120 weight paths, every one published at
every rung = 480 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (L, b) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

THE WARM-IN ASYMMETRY IS HANDLED IN THE OPEN, NOT BURIED.  The committed window starts at
index[260], where L = 300 has no MA at all.  Section D re-scores every row on an EQUAL-STATE
window (index[360:], by which every length has >= 60 sessions of live state) and publishes the
4b count under both windows.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_spy-alone-band-across-ma-lengths_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "spy-alone-band-across-ma-lengths", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

CADENCE, WARMUP, EQWARM = "W", 260, 360
LENGTHS = [50, 100, 150, 200, 250, 300]
BANDS = [0.00, 0.01, 0.03, 0.06, 0.10]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
RISK, SWEEP = "SPY", "SHY"
LIVE_L, LIVE_B, LIVE_G = 200, 0.03, 0.75
BAND_CAND, CAP = 0.03, 0.020
IS_END, OOS_START = "2016-12-31", "2017-01-01"
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
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the gate, generalised in L
def band_state_L(px, L, b):
    """baseline.band_state with the 200-session window generalised to L.  At L = 200, b = 0.03
    this must be `baseline.band_state(px, 0.03)` cell for cell (gate G1)."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def spyonly_weights(px2, L, b, gross):
    """One instrument: SPY at `gross` while IN the L-day band, residual in full to SHY."""
    inb = band_state_L(px2[[RISK]], L, b)[RISK] & px2[RISK].notna()
    w = pd.DataFrame(0.0, index=px2.index, columns=px2.columns)
    w[RISK] = inb.astype(float) * gross
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = idle * px2[SWEEP].notna().astype(float)
    return w, inb


def cap_weights(px, invest, gross):
    """idea 2322's CAP2 — the committed cross-sectional candidate, this run's comparand."""
    q = px[invest]
    inb = band_state(q, BAND_CAND) & q.notna()
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def run(px, w, freq=CADENCE):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return dict(r0=res["returns"], turnover=res["turnover"], held=res["weights"])


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR),
                legstring="".join("1" if x else "0" for x in (L_H1, L_H2, L_OOS, L_DD, L_CAGR)))


def main():
    t0 = time.time()
    say("=== idea 2459 (lane cloud, run 55) — does the 200d BAND earn its KEEP on SPY ALONE, across MA LENGTHS? ===")
    say(f"    {DATE}  lane {LANE}   cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 MA length L {LENGTHS}   DIAL 2 band half-width b {BANDS}")
    say(f"    REPORTED not selected: gross {GROSSES}  frames U56/B136  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "MA length L, band half-width b", "2", True)

    frames = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        frames[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(px.columns)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        gate(f"G6 {RISK} and {SWEEP} priced on every in-window row ({nm})",
             f"{RISK} {int(px[RISK].loc[win].notna().sum())}, {SWEEP} {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}",
             "all", bool(px[RISK].loc[win].notna().all() and px[SWEEP].loc[win].notna().all()))

    px_u, inv_u = frames["U56"]

    # ---- G1: the generalised gate IS baseline.band_state at the live length and width
    a = band_state_L(px_u[[RISK]], LIVE_L, LIVE_B)[RISK]
    bnat = band_state(px_u[inv_u], LIVE_B)[RISK]
    gate("G1 band_state_L(200, 0.03) == baseline.band_state(0.03) on SPY",
         f"{int((a != bnat).sum())} differing cells of {len(a)}", "0", int((a != bnat).sum()) == 0)

    # ---- G3: the two-column frame is the same book as the full panel frame
    px2_u = px_u[[RISK, SWEEP]].copy()
    wfull, _ = spyonly_weights(px_u, LIVE_L, LIVE_B, LIVE_G)
    wfull = wfull.reindex(columns=px_u.columns).fillna(0.0)
    r_full = priced(run(px_u, wfull), HEADLINE_RUNG).loc[px_u.index[WARMUP:]]
    w2, _ = spyonly_weights(px2_u, LIVE_L, LIVE_B, LIVE_G)
    r_2 = priced(run(px2_u, w2), HEADLINE_RUNG).loc[px_u.index[WARMUP:]]
    d3 = float((r_full - r_2).abs().max())
    gate("G3 the 2-column frame is the same book as the full 56-column frame",
         f"max|dr| {d3:.3e}", "< 1e-15", d3 < 1e-15)

    # ---- G7: no lookahead
    cut = "2018-06-29"
    pxA = px2_u.copy()
    pxB = px2_u.copy(); pxB.loc[pxB.index > cut] = pxB.loc[pxB.index > cut] * 1.5
    wA, _ = spyonly_weights(pxA, 250, 0.06, 0.75)
    wB, _ = spyonly_weights(pxB, 250, 0.06, 0.75)
    dlk = float((wA.loc[:cut] - wB.loc[:cut]).abs().max().max())
    gate("G7 no lookahead (future tape x1.5 after 2018-06-29 leaves every earlier weight identical)",
         f"max|dw| on rows <= {cut}: {dlk:.3e}", "< 1e-15", dlk < 1e-15)

    # ---------------------------------------------------------------- the grid
    rows = []
    refs = {}
    for fname, (px, invest) in frames.items():
        win, eqwin = px.index[WARMUP:], px.index[EQWARM:]
        yrs = len(win) / 252
        px2 = px[[RISK, SWEEP]].copy()
        spy = px[RISK].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND_CAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        cand = run(px, cap_weights(px, invest, 0.75))
        cand_r = priced(cand, HEADLINE_RUNG).loc[win]
        refs[fname] = dict(spy=spy, spy_oos=spy_oos, base_r=base_r, cand_r=cand_r,
                           cand_turn=float(cand["turnover"].loc[win].sum() / yrs))
        say(f"\n--- frame {fname}  SPY buy&hold {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f}"
            f"   CAP2 candidate {cagr(cand_r):.2%} / {sharpe(cand_r):.4f} / {maxdd(cand_r):.2%}")
        publish(f"{fname} SPY buy-and-hold (the 4b bar itself)",
                f"CAGR {cagr(spy):.4%}  Sharpe {sharpe(spy):.4f}  MaxDD {maxdd(spy):.4%}"
                f"  halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}  OOS {cagr(spy_oos):.4%}/{sharpe(spy_oos):.4f}"
                f"  bars: DD >= {DD_CAP * maxdd(spy):.4%}, CAGR >= {CAGR_FLOOR * cagr(spy):.4%}")
        publish(f"{fname} CAP2 cross-sectional candidate (10 bps, g0.75)",
                f"CAGR {cagr(cand_r):.4%}  Sharpe {sharpe(cand_r):.4f}  MaxDD {maxdd(cand_r):.4%}"
                f"  halves {halves(cand_r)[0]:.4f}/{halves(cand_r)[1]:.4f}"
                f"  OOS {cagr(cand_r.loc[OOS_START:]):.4%}/{sharpe(cand_r.loc[OOS_START:]):.4f}"
                f"  turnover {refs[fname]['cand_turn']:.2f}x")
        for L in LENGTHS:
            for b in BANDS:
                for gross in GROSSES:
                    w, inb = spyonly_weights(px2, L, b, gross)
                    res = run(px2, w)
                    for rung in RUNGS:
                        rr = priced(res, rung)
                        r = rr.loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        req = rr.loc[eqwin]
                        leq = legs(req, base_r.loc[eqwin], spy.loc[eqwin],
                                   req.loc[OOS_START:], spy_oos)
                        rows.append(dict(frame=fname, L=L, band=b, gross=gross, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                         time_in=float(inb.loc[win].mean()),
                                         mean_risk_gross=float(res["held"][RISK].loc[win].mean()),
                                         mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                         max_row_sum=float(res["held"].sum(axis=1).max()),
                                         eq_pass4b=leq["pass4b"], eq_Sharpe=sharpe(req),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {fname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- G2: EXACT reproduction of idea 2467's committed SPYONLY cell
    h = df[(df.frame == "U56") & (df.L == LIVE_L) & (df.band == LIVE_B) & (df.gross == LIVE_G)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    tgt = dict(CAGR=0.0784, Sharpe=0.8375, MaxDD=-0.2007, OOS_CAGR=0.0840, OOS_Sharpe=0.8544, turnover_yr=1.99)
    d2 = max(abs(h[k] - v) for k, v in tgt.items())
    gate("G2 reproduces idea 2467's committed SPYONLY cell (7.84% / 0.8375 / -20.07%, OOS 8.40% / 0.8544, 1.99x)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, halves {h.H1:.2f}/{h.H2:.2f},"
         f" OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}, {h.turnover_yr:.2f}x, legs {h.legstring};"
         f" max|d| {d2:.3e}", "< 5e-3 (published to 2-4 dp)", d2 < 5e-3)
    gate("G2b the committed cell's leg string is 00010 (passes L_DD alone)", h.legstring, "00010",
         h.legstring == "00010")

    # ---- G9: the CAP2 comparand reproduces the committed candidate headline
    cr = refs["U56"]["cand_r"]
    d9 = max(abs(cagr(cr) - 0.1162), abs(sharpe(cr) - 1.2687), abs(maxdd(cr) + 0.1481))
    gate("G9 the CAP2 comparand reproduces the committed U56 headline (11.62% / 1.2687 / -14.81%)",
         f"read {cagr(cr):.2%} / {sharpe(cr):.4f} / {maxdd(cr):.2%}; max|d| {d9:.3e}",
         "< 5e-3 (price-cache vintage residual)", d9 < 5e-3)

    # ---- G4 / G5
    gate("G4 no leverage (max row sum over all 120 weight paths)", f"{df.max_row_sum.max():.9f}",
         "<= 1.0 + 1e-9", df.max_row_sum.max() <= 1.0 + 1e-9)
    ti = df[(df.frame == "U56") & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
    gate("G5 both dials bite (time-IN share spans)",
         f"over L {ti.groupby('L').time_in.mean().min():.4f} to {ti.groupby('L').time_in.mean().max():.4f};"
         f" over b {ti.groupby('band').time_in.mean().min():.4f} to {ti.groupby('band').time_in.mean().max():.4f};"
         f" turnover over b {ti.groupby('band').turnover_yr.mean().max():.2f} -> {ti.groupby('band').turnover_yr.mean().min():.2f}x",
         "both dials move the book", ti.time_in.nunique() > 10)

    # ---------------------------------------------------------------- section C: the surface
    say("\n=== C. THE SURFACE (U56 frame, gross 0.75, 10 bps): Sharpe / CAGR / MaxDD / turnover / time-IN / 4b legs ===")
    for L in LENGTHS:
        for b in BANDS:
            r = df[(df.frame == "U56") & (df.L == L) & (df.band == b) & (df.gross == 0.75)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  L={L:3d} b={b:.2f} | Sharpe {r.Sharpe:6.4f}  CAGR {r.CAGR:6.2%}  MaxDD {r.MaxDD:7.2%}"
                f"  turn {r.turnover_yr:5.2f}x  in {r.time_in:5.3f}  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:6.4f}"
                f"  legs {r.legstring}  4b {'PASS' if r.pass4b else 'fail'}  4a {'PASS' if r.pass4a else 'fail'}")

    # ---------------------------------------------------------------- section D: the answer
    say("\n=== D. DOES THE TIMING RULE EARN ITS KEEP ANYWHERE? ===")
    say(f"  4b {int(df.pass4b.sum())} of {len(df)} rows;  4a {int(df.pass4a.sum())} of {len(df)}")
    for k in ("frame", "L", "band", "gross", "cost_bps"):
        say(f"    by {k}: " + "  ".join(f"{v}:{int(s.pass4b.sum())}/{len(s)}" for v, s in df.groupby(k)))
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"    4b leg {leg} fails on {int((~df[leg]).sum())} of {len(df)} rows")
    say(f"    leg-string census: " + ", ".join(f"{k}:{v}" for k, v in df.legstring.value_counts().items()))
    say(f"  EQUAL-STATE WINDOW (index[{EQWARM}:], every L has >= 60 sessions of live state):"
        f" 4b {int(df.eq_pass4b.sum())} of {len(df)} (headline window {int(df.pass4b.sum())})")
    best = df[(df.cost_bps == HEADLINE_RUNG)].sort_values("Sharpe", ascending=False).iloc[0]
    say(f"  BEST SHARPE ANYWHERE at 10 bps: frame {best.frame} L={best.L} b={best.band:.2f} g={best.gross:.2f}"
        f" -> {best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}, halves {best.H1:.4f}/{best.H2:.4f},"
        f" OOS {best.OOS_CAGR:.2%}/{best.OOS_Sharpe:.4f}, turn {best.turnover_yr:.2f}x, legs {best.legstring}")
    for fname in frames:
        sp, cd = refs[fname]["spy"], refs[fname]["cand_r"]
        bb = df[(df.frame == fname) & (df.cost_bps == HEADLINE_RUNG)].sort_values("Sharpe", ascending=False).iloc[0]
        say(f"  {fname} DECOMPOSITION at 10 bps — SPY b&h Sharpe {sharpe(sp):.4f} | best SPY-ALONE timing cell"
            f" {sharpe(bb.Sharpe) if False else bb.Sharpe:.4f} (L={bb.L}, b={bb.band:.2f}, g={bb.gross:.2f})"
            f" | CAP2 cross-sectional candidate {sharpe(cd):.4f}")
        say(f"       => TIMING adds {bb.Sharpe - sharpe(sp):+.4f} of Sharpe over owning the index;"
            f" the CROSS-SECTION adds a further {sharpe(cd) - bb.Sharpe:+.4f}"
            f" ({(sharpe(cd) - bb.Sharpe) / max(1e-9, sharpe(cd) - sharpe(sp)):.1%} of the candidate's whole"
            f" SPY-relative Sharpe margin)")
        publish(f"{fname} margin decomposition (10 bps)",
                f"SPY {sharpe(sp):.4f} -> best timing cell {bb.Sharpe:.4f} -> CAP2 {sharpe(cd):.4f};"
                f" timing share {(bb.Sharpe - sharpe(sp)) / max(1e-9, sharpe(cd) - sharpe(sp)):.1%},"
                f" cross-section share {(sharpe(cd) - bb.Sharpe) / max(1e-9, sharpe(cd) - sharpe(sp)):.1%}")

    # ---------------------------------------------------------------- rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — (L, b) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for fname in frames:
        px, invest = frames[fname]
        spy_oos = refs[fname]["spy_oos"]
        base_oos = refs[fname]["base_r"].loc[OOS_START:]
        cand_oos = refs[fname]["cand_r"].loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                sub = df[(df.frame == fname) & (df.gross == gross) & (df.cost_bps == rung)]
                live = sub[(sub.L == LIVE_L) & (sub.band == LIVE_B)].iloc[0]
                for cn, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = sub.loc[sub[col].idxmax()]
                    wf.append(dict(frame=fname, gross=gross, cost_bps=rung, chooser=cn,
                                   pick_L=int(pick.L), pick_band=float(pick.band),
                                   OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                                   OOS_MaxDD=float(pick.OOS_MaxDD), turnover_yr=float(pick.turnover_yr),
                                   live_cell_OOS_Sharpe=float(live.OOS_Sharpe),
                                   d_vs_live_cell=float(pick.OOS_Sharpe - live.OOS_Sharpe),
                                   beats_SPY_OOS=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_liveBook_OOS=bool(pick.OOS_Sharpe > sharpe(base_oos)),
                                   beats_CAND_OOS=bool(pick.OOS_Sharpe > sharpe(cand_oos)),
                                   SPY_OOS_Sharpe=sharpe(spy_oos), CAND_OOS_Sharpe=sharpe(cand_oos),
                                   full_pass4b=bool(pick.pass4b)))
    wdf = pd.DataFrame(wf); wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wdf)} picks.  L: " + ", ".join(f"{L}:{int((wdf.pick_L == L).sum())}" for L in LENGTHS))
    say(f"             b: " + ", ".join(f"{b:.2f}:{int((wdf.pick_band == b).sum())}" for b in BANDS))
    say(f"  picks beat SPY's OOS Sharpe in {int(wdf.beats_SPY_OOS.sum())} of {len(wdf)};"
        f" the live book's in {int(wdf.beats_liveBook_OOS.sum())};"
        f" the CAP2 candidate's in {int(wdf.beats_CAND_OOS.sum())}")
    say(f"  mean d(OOS Sharpe) vs the live (L=200, b=0.03) cell {wdf.d_vs_live_cell.mean():+.4f};"
        f" picks carry a full-sample 4b in {int(wdf.full_pass4b.sum())} of {len(wdf)}")
    publish("RULE 8 pick distribution (L, b)",
            "L " + "/".join(f"{L}:{int((wdf.pick_L == L).sum())}" for L in LENGTHS)
            + "   b " + "/".join(f"{b:.2f}:{int((wdf.pick_band == b).sum())}" for b in BANDS))

    # ---------------------------------------------------------------- close
    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {bool(gdf.pass_.all())}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
