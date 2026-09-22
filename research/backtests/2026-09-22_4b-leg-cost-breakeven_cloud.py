#!/usr/bin/env python3
"""Idea 2270 (lane cloud, 2026-09-22): what COST RUNG does the STANDING CANDIDATE's 4b
PASS actually LIVE ON?

Idea 2264 left the record's standing 4b candidate -- the live RULES v2 band book on U56 at
`gross = 1.00`, weekly, t+1 -- passing 4b FULL and OOS at 0 / 5 / 10 / 25 bps and missing
the FULL CAGR floor by 0.11 pp at 50 bps.  A verdict quoted at four sampled rungs is not a
cost result.  This run replaces the sampled verdict with a BREAKEVEN: for every leg of 4b
(and of 4a), on every rung of the gross ladder and every panel, it publishes the exact cost
in bps at which that leg dies.

THE PREMISE IS TESTED, NOT ASSUMED.  The queue line asserts the margin is "exactly linear
in bps at fixed turnover" because the engine never feeds cost back into positions.  The
first half of that is true and is verified as gate G1: held weights and the turnover series
are cost-invariant, so r_t(c) = r0_t - to_t * c / 1e4 EXACTLY.  The second half is false for
CAGR and for MaxDD, which are non-linear functionals of the return path.  This run therefore
publishes BOTH
  (i)  the EXACT breakeven, by bisection on the true metric to 0.01 bps, and
  (ii) the ANALYTIC first-order breakeven implied by the turnover identity
         dCAGR/dc  ~= -(annual turnover) / 1e4          per bp
         dSharpe/dc ~= -(annual turnover) / 1e4 / vol   per bp
and reports the error between them, so the record learns how far the linear shorthand can
be trusted.

CONSTRUCTION
  BOOK: `baseline.rules_v2_weights(px, band=0.03, gross=g)` -- the live book, unchanged in
  every clause except size.  Weekly and monthly cadence, t+1, gated-out weight to cash.
  TUNED PARAMETERS: exactly two, GROSS g and PANEL.  The COST LADDER is the axis under test
  and every rung is published; cadence and band are reported, not tuned.
  LADDER: g in {0.25 .. 1.50 step 0.125} (11 rungs, 2264's own ladder).  Rungs above 1.00
  are published but flagged LEVERED and excluded from any candidate (PROTOCOL rule 2).
  PANELS: U56, B136, SMALL (survivorship-screened; see the caveat below).
  COSTS: a dense 0 .. 100 bps ladder in 1 bps steps, reconstructed exactly.

  4b legs (PROTOCOL rule 4b):  L_H1, L_H2 (Sharpe > SPY in each half), L_OOS (Sharpe > SPY
  out of sample), L_DD (MaxDD >= 0.60 x SPY's), L_CAGR (CAGR >= 0.70 x SPY's), plus the
  OOS-window forms L_DD_OOS / L_CAGR_OOS used by the 4b-OOS reading.
  4a legs: L4a_H1, L4a_H2 (Sharpe > live RULES v2 in each half), L4a_DD.
  SPY is a cost-free buy-and-hold comparand, so every 4b BAR is cost-invariant and each 4b
  leg's margin is monotone decreasing in cost; the 4a bars move WITH the book, so a 4a leg's
  cost derivative is a turnover DIFFERENCE and can carry either sign.  Both are published.

  RULE 8 (2017-2026 read ONCE): g chosen on 2009-2016 only, by (a) 2264's IS-only
  drawdown-budget chooser at kappa = 0.60 under the no-leverage cap and (b) the record's
  habitual IS-Sharpe chooser.  The chosen cell's OOS breakeven bps is published.

SURVIVORSHIP CAVEAT: U56 / B136 are 2026 constituents held from 2008 and SMALL is the
current-constituent sub-$2B screen (data/SMALL_PANEL_README.md), tickers with
max_1d_move >= 1.0 in data/small_meta.csv dropped first.  Every CAGR level here is
optimistic and both 4b level legs are easier than on a point-in-time panel; a breakeven bps
computed on such a panel is an UPPER bound on the real one.

Run: python3 research/backtests/2026-09-22_4b-leg-cost-breakeven_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa
from engine import backtest                                               # noqa

WARMUP    = 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END    = pd.Timestamp("2016-12-31")
BAND      = 0.03
GROSSES   = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00, 1.125, 1.25, 1.375, 1.50]
CADENCES  = ["W", "M"]
DENSE     = list(range(0, 101))          # bps, every rung published
SAMPLED   = [0, 5, 10, 25, 50]           # 2264's own four-plus-one rungs
HEADLINE  = 10
KAPPA     = 0.60                         # PROTOCOL 4b's own delta, pre-registered 2026-09-04
CAP       = 1.00                         # PROTOCOL rule 2, no leverage
OUT = ROOT / "research" / "backtests" / "2026-09-22_4b-leg-cost-breakeven_cloud"

# ---------------------------------------------------------------- metrics
def sharpe(r): s = r.std(); return r.mean() * 252 / (s * np.sqrt(252)) if s > 0 else np.nan
def maxdd(r):  e = (1 + r).cumprod(); return float((e / e.cummax() - 1).min())
def cagr(r):   e = (1 + r).cumprod(); return float(e.iloc[-1] ** (252 / len(r)) - 1)
def vol(r):    return float(r.std() * np.sqrt(252))

def at_cost(r0, to, bps): return r0 - to * bps / 1e4

# ---------------------------------------------------------------- legs
def legs(r, spy, v2):
    """Every 4b and 4a leg as a MARGIN (>= 0 means the leg passes)."""
    h  = len(r) // 2
    o  = r.loc[OOS_START:]
    so = spy.loc[OOS_START:]
    vh = len(v2) // 2
    return {
        "L_H1":       sharpe(r.iloc[:h]) - sharpe(spy.iloc[:h]),
        "L_H2":       sharpe(r.iloc[h:]) - sharpe(spy.iloc[h:]),
        "L_OOS":      sharpe(o) - sharpe(so),
        "L_DD":       maxdd(r) - 0.60 * maxdd(spy),
        "L_CAGR":     cagr(r) - 0.70 * cagr(spy),
        "L_DD_OOS":   maxdd(o) - 0.60 * maxdd(so),
        "L_CAGR_OOS": cagr(o) - 0.70 * cagr(so),
        "L4a_H1":     sharpe(r.iloc[:h]) - sharpe(v2.iloc[:vh]),
        "L4a_H2":     sharpe(r.iloc[h:]) - sharpe(v2.iloc[vh:]),
        "L4a_DD":     maxdd(r) - maxdd(v2),
    }

B4  = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
B4O = ["L_OOS", "L_DD_OOS", "L_CAGR_OOS"]
A4  = ["L4a_H1", "L4a_H2", "L4a_DD"]

def margins_at(r0, to, c, spy, v2_r0, v2_to):
    return legs(at_cost(r0, to, c), spy, at_cost(v2_r0, v2_to, c))

def breakeven(r0, to, leg, spy, v2_r0, v2_to, lo=0.0, hi=400.0, tol=1e-2):
    """Exact bps at which `leg` crosses zero, by bisection on the TRUE metric.
    Returns (bps, status): 'alive>hi' if it still passes at hi, 'dead<=lo' if already failing."""
    m_lo = margins_at(r0, to, lo, spy, v2_r0, v2_to)[leg]
    if not (m_lo >= 0): return (np.nan, "dead_at_zero")
    m_hi = margins_at(r0, to, hi, spy, v2_r0, v2_to)[leg]
    if m_hi >= 0: return (np.nan, f"alive_beyond_{hi:.0f}")
    a, b = lo, hi
    while b - a > tol:
        mid = (a + b) / 2
        if margins_at(r0, to, mid, spy, v2_r0, v2_to)[leg] >= 0: a = mid
        else: b = mid
    return ((a + b) / 2, "crosses")

# ---------------------------------------------------------------- panels
def panels():
    out = {"U56": load_universe(), "B136": load_universe(broad=True)}
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    out["SMALL"] = px[[c for c in px.columns if c == "SPY" or c not in bad]]
    return out

# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    P = panels()
    dense_rows, be_rows, gates, wf, series = [], [], [], [], {}

    for pname, px in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for freq in CADENCES:
            v2 = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75), cost_bps=0.0, freq=freq)
            v2_r0, v2_to = v2["returns"].loc[start:], v2["turnover"].loc[start:]
            for g in GROSSES:
                res = backtest(px, rules_v2_weights(px, band=BAND, gross=g), cost_bps=0.0, freq=freq)
                r0, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                series[(pname, freq, g)] = (r0, to, v2_r0, v2_to, spy)
                yrs = len(r0) / 252
                ann_to = float(to.sum() / yrs)
                v2_ann = float(v2_to.sum() / yrs)

                # ---- dense cost ladder, every rung published
                for c in DENSE:
                    m = margins_at(r0, to, c, spy, v2_r0, v2_to)
                    r = at_cost(r0, to, c)
                    row = dict(panel=pname, freq=freq, gross=g, cost_bps=c,
                               levered=g > CAP, ann_turnover=ann_to, v2_ann_turnover=v2_ann,
                               CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                               OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                               OOS_MaxDD=maxdd(r.loc[OOS_START:]))
                    row.update(m)
                    row["pass_4b"]     = all(m[k] >= 0 for k in B4)
                    row["pass_4b_oos"] = all(m[k] >= 0 for k in B4O)
                    row["pass_4a"]     = all(m[k] >= 0 for k in A4)
                    dense_rows.append(row)

                # ---- exact + analytic breakevens, per leg
                m0 = margins_at(r0, to, HEADLINE, spy, v2_r0, v2_to)
                r10 = at_cost(r0, to, HEADLINE)
                v_full = vol(r10); v_oos = vol(r10.loc[OOS_START:])
                to_oos = float(to.loc[OOS_START:].sum() / (len(r10.loc[OOS_START:]) / 252))
                slopes = {  # analytic d(margin)/d(bps), first order at fixed turnover
                    "L_H1":       -(ann_to / 1e4) / vol(r10.iloc[:len(r10)//2]),
                    "L_H2":       -(ann_to / 1e4) / vol(r10.iloc[len(r10)//2:]),
                    "L_OOS":      -(to_oos / 1e4) / v_oos,
                    "L_DD":       np.nan,
                    "L_CAGR":     -(ann_to / 1e4),
                    "L_DD_OOS":   np.nan,
                    "L_CAGR_OOS": -(to_oos / 1e4),
                    "L4a_H1":     -((ann_to - v2_ann) / 1e4) / vol(r10.iloc[:len(r10)//2]),
                    "L4a_H2":     -((ann_to - v2_ann) / 1e4) / vol(r10.iloc[len(r10)//2:]),
                    "L4a_DD":     np.nan,
                }
                for leg in B4 + ["L_DD_OOS", "L_CAGR_OOS"] + A4:
                    be, status = breakeven(r0, to, leg, spy, v2_r0, v2_to)
                    sl = slopes[leg]
                    ana = HEADLINE + m0[leg] / abs(sl) if (sl == sl and sl < 0 and m0[leg] >= 0) else np.nan
                    be_rows.append(dict(panel=pname, freq=freq, gross=g, levered=g > CAP, leg=leg,
                                        margin_at_10bps=m0[leg], exact_breakeven_bps=be,
                                        status=status, analytic_slope_per_bp=sl,
                                        analytic_breakeven_bps=ana,
                                        analytic_error_bps=(ana - be) if (ana == ana and be == be) else np.nan,
                                        ann_turnover=ann_to))
            print(f"[{pname}/{freq}] ladder done ({time.time()-t0:.0f}s)")

    D = pd.DataFrame(dense_rows); D.to_csv(f"{OUT}.grid.csv.gz", index=False, compression="gzip")
    BE = pd.DataFrame(be_rows);   BE.to_csv(f"{OUT}.breakeven.csv", index=False)

    # ---- G1: cost reconstruction is exact (the premise's TRUE half)
    for (pname, freq, g), (r0, to, _, _, _) in list(series.items())[:6]:
        px = P[pname]; start = px.index[WARMUP]
        direct = backtest(px, rules_v2_weights(px, band=BAND, gross=g), cost_bps=HEADLINE,
                          freq=freq)["returns"].loc[start:]
        err = float(np.abs(direct.values - at_cost(r0, to, HEADLINE).values).max())
        gates.append(dict(gate="G1_cost_reconstruction_exact", cell=f"{pname}/{freq}/g={g}",
                          value=err, ok=bool(err < 1e-15)))

    # ---- G2 / G3: reproduce 2264's published headline cell
    r0, to, v2_r0, v2_to, spy = series[("U56", "W", 1.00)]
    r10 = at_cost(r0, to, HEADLINE); r50 = at_cost(r0, to, 50)
    v210 = at_cost(v2_r0, v2_to, HEADLINE)
    pub = dict(CAGR=0.1153, Sharpe=1.2009, MaxDD=-0.1591, OOS_CAGR=0.1267, OOS_Sharpe=1.2760,
               TO=2.35, v2_CAGR=0.0862, v2_Sharpe=1.2010, v2_MaxDD=-0.1205,
               spy_CAGR=0.1514, spy_Sharpe=0.8851, spy_MaxDD=-0.3372)
    got = dict(CAGR=cagr(r10), Sharpe=sharpe(r10), MaxDD=maxdd(r10),
               OOS_CAGR=cagr(r10.loc[OOS_START:]), OOS_Sharpe=sharpe(r10.loc[OOS_START:]),
               TO=float(to.sum() / (len(r10) / 252)),
               v2_CAGR=cagr(v210), v2_Sharpe=sharpe(v210), v2_MaxDD=maxdd(v210),
               spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy))
    for k in pub:
        gates.append(dict(gate="G2_reproduce_2264", cell=k, value=abs(got[k] - pub[k]),
                          ok=bool(abs(got[k] - pub[k]) < (0.02 if k == "TO" else 2e-3)),
                          note=f"published {pub[k]}, got {got[k]:.4f}"))
    miss = cagr(r50) - 0.70 * cagr(spy)
    gates.append(dict(gate="G3_50bps_FULL_CAGR_miss_pp", cell="U56/W/g=1.00",
                      value=miss * 100, ok=bool(abs(miss * 100 + 0.11) < 0.05),
                      note="2264 published a 0.11 pp miss (10.49% vs 10.60%); "
                           f"got {cagr(r50)*100:.2f}% vs floor {70*cagr(spy):.2f}%"))

    # ---- G4: every 4b leg's margin is monotone non-increasing in cost (SPY bar is cost-free)
    bad = 0
    for (pname, freq, g), _ in series.items():
        sub = D[(D.panel == pname) & (D.freq == freq) & (D.gross == g)].sort_values("cost_bps")
        for leg in B4 + ["L_DD_OOS", "L_CAGR_OOS"]:
            d = np.diff(sub[leg].values)
            if (d > 1e-12).any(): bad += 1
    gates.append(dict(gate="G4_4b_leg_margins_monotone_in_cost", cell="ALL",
                      value=bad, ok=bool(bad == 0),
                      note=f"{bad} of {len(series)*7} (book,leg) paths non-monotone"))

    # ---- RULE 8: g chosen on 2009-2016 ONLY; 2017-2026 read once
    for pname in P:
        for freq in CADENCES:
            for c in SAMPLED:
                spy = series[(pname, freq, GROSSES[0])][4]
                is_spy_dd = maxdd(spy.loc[:IS_END])
                pick_dd, pick_sh, best_sh = None, None, -np.inf
                for g in GROSSES:
                    if g > CAP: continue
                    r0, to, v2_r0, v2_to, _ = series[(pname, freq, g)]
                    ir = at_cost(r0, to, c).loc[:IS_END]
                    if maxdd(ir) >= KAPPA * is_spy_dd: pick_dd = g      # largest legal g
                    s = sharpe(ir)
                    if s > best_sh: best_sh, pick_sh = s, g
                for cname, g in (("C_DDB060", pick_dd), ("C_SHARPE", pick_sh)):
                    if g is None:
                        wf.append(dict(panel=pname, freq=freq, cost_bps=c, chooser=cname,
                                       chosen_gross=np.nan, abstain=True)); continue
                    r0, to, v2_r0, v2_to, spy = series[(pname, freq, g)]
                    r = at_cost(r0, to, c); v2r = at_cost(v2_r0, v2_to, c)
                    m = legs(r, spy, v2r)
                    be_cagr, st1 = breakeven(r0, to, "L_CAGR", spy, v2_r0, v2_to)
                    be_dd,  st2 = breakeven(r0, to, "L_DD",   spy, v2_r0, v2_to)
                    be_oos, st3 = breakeven(r0, to, "L_OOS",  spy, v2_r0, v2_to)
                    be_co,  st4 = breakeven(r0, to, "L_CAGR_OOS", spy, v2_r0, v2_to)
                    legbe = [x for x in (be_cagr, be_dd, be_oos) if x == x]
                    wf.append(dict(panel=pname, freq=freq, cost_bps=c, chooser=cname, abstain=False,
                                   chosen_gross=g,
                                   FULL_CAGR=cagr(r), FULL_Sharpe=sharpe(r), FULL_MaxDD=maxdd(r),
                                   OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                   OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                   v2_OOS_Sharpe=sharpe(v2r.loc[OOS_START:]),
                                   spy_OOS_CAGR=cagr(spy.loc[OOS_START:]),
                                   spy_OOS_Sharpe=sharpe(spy.loc[OOS_START:]),
                                   spy_OOS_MaxDD=maxdd(spy.loc[OOS_START:]),
                                   pass_4b=all(m[k] >= 0 for k in B4),
                                   pass_4b_oos=all(m[k] >= 0 for k in B4O),
                                   pass_4a=all(m[k] >= 0 for k in A4),
                                   be_L_CAGR=be_cagr, be_L_DD=be_dd, be_L_OOS=be_oos,
                                   be_L_CAGR_OOS=be_co,
                                   death_bps_4b=min(legbe) if legbe else np.nan))
    W = pd.DataFrame(wf); W.to_csv(f"{OUT}.walkforward.csv", index=False)
    Gt = pd.DataFrame(gates); Gt.to_csv(f"{OUT}.gates.csv", index=False)

    # ---- summary
    print(f"\n=== {len(D)} dense cells published; {len(BE)} leg-breakevens ===")
    print("\n-- THE STANDING CANDIDATE (U56 / W / g=1.00): breakeven bps by leg --")
    print(BE[(BE.panel == "U56") & (BE.freq == "W") & (BE.gross == 1.00)]
          .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    unl = BE[~BE.levered]
    print("\n-- 4b DEATH RUNG (min breakeven over the five 4b legs), unlevered cells --")
    dr = (unl[unl.leg.isin(B4)].groupby(["panel", "freq", "gross"])
          .agg(death_bps=("exact_breakeven_bps", "min"),
               binding=("exact_breakeven_bps", lambda s: unl.loc[s.idxmin(), "leg"] if s.notna().any() else "none"),
               dead_at_zero=("status", lambda s: (s == "dead_at_zero").sum())).reset_index())
    print(dr.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    print("\n-- which leg binds first, over unlevered cells that are alive at 0 bps --")
    print(dr[dr.dead_at_zero == 0]["binding"].value_counts().to_string())
    print("\n-- linearity of the shorthand: analytic minus exact breakeven (bps) --")
    e = BE.dropna(subset=["analytic_error_bps"])
    print(e.groupby("leg")["analytic_error_bps"].describe()[["count", "mean", "50%", "min", "max"]]
          .to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n-- 4b / 4b-OOS / 4a pass counts at the sampled rungs (unlevered) --")
    du = D[~D.levered & D.cost_bps.isin(SAMPLED)]
    print(du.groupby(["panel", "freq", "cost_bps"])[["pass_4b", "pass_4b_oos", "pass_4a"]].sum().to_string())
    print("\n-- RULE 8 (g chosen on 2009-2016 only; 2017-2026 read once) --")
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n-- GATES --"); print(Gt.to_string(index=False))
    print(f"\ndone in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
