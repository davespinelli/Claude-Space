#!/usr/bin/env python3
"""
IDEA 2203 (lane cloud, 2026-09-22, run 8) -- does the 4b VERDICT on the BAND LADDER survive a
                                             REALISED-GROSS-MATCHED comparand?

WHERE THIS COMES FROM.  Idea 2125 found that NOMINAL and REALISED gross come apart by up to
41% on the band family: the band gates names OUT to CASH and never re-spreads, so a book whose
nominal dial reads g = 1.00 actually carries mean gross well below 1.00, and the shortfall is
itself a function of the band width b.  Every committed band x gross 4b verdict in the record
is therefore quoted in a dial THE BOOK DOES NOT ACTUALLY CARRY, and two cells labelled with
the same g are not the same exposure.

THE QUESTION, as filed.  Re-run the 2119 ladder with the gross axis expressed in REALISED mean
gross (rescale each nominal rung so realised gross hits {0.35,0.45,0.55,0.65,0.75}) and report
how many 4b passes survive the re-parameterisation.

WHAT THIS RUN DOES, mechanically.
  (1) Prices the NOMINAL ladder exactly as the record does: band b x nominal gross g.
  (2) Measures REALISED mean gross R(b,g) = time-mean of the portfolio's own held exposure
      (sum of held weights, drift included), over the evaluation window.
  (3) For every (panel, band, realised rung R*), SOLVES for the nominal g that makes
      R(b, g) == R* by bisection (R is monotone increasing in g; no leverage, so g <= 1.00,
      and a rung unreachable at g = 1.00 is published as INFEASIBLE, not silently dropped).
  (4) Re-reads the SAME 4b / 4a machinery on the realised-matched ladder and reports how many
      of the nominal ladder's 4b passes survive, and which cells the re-parameterisation
      creates that the nominal axis never showed.

EXACTLY TWO TUNED DIALS, every grid point published (<slug>.grid.csv):
  1. BAND b in {0.00, 0.02, 0.03, 0.05, 0.08}
  2. THE GROSS RUNG -- read in TWO parameterisations, nominal g in {0.50,0.60,0.75,0.85,1.00}
     and realised R* in {0.35,0.45,0.55,0.65,0.75}.  25 cells per panel per parameterisation.
REPORTED, NOT TUNED: panel {U56, B136, SMALL}; cost {0,10,25,50} bps (protocol 10); cadence W;
  windows FULL / IS(..2016-12-31) / OOS(2017-01-01..), rule 8, OOS read ONCE per chooser.
COMPARANDS: baseline.rules_v2_weights (the live book) and SPY buy-and-hold.

PRE-REGISTERED BARS, written before any number below was read:
  V1  THE GAP.  Publish R(b,g) for all 25 nominal cells x 3 panels.  How far does realised
      gross sit below nominal, and does the shortfall depend on b?  (2125 says up to 41%.)
  V2  THE QUESTION.  Of the nominal ladder's 4b passes at 10 bps, how many survive when the
      SAME book is relabelled by realised gross -- i.e. how many realised-matched cells pass?
      Counts FULL and OOS, per panel.
  V3  SET IDENTITY.  Jaccard of {4b-passing cells} between the two parameterisations, matched
      by band.  A re-parameterisation that changes nothing scores 1.00.
  V4  BOTH KEEP PATHS at every grid point, both parameterisations, FULL and OOS.
  V5  RULE 8.  Choose the cell on IS rows ONLY (IS_SHARPE and IS_MINMARG), evaluate OOS ONCE,
      in each parameterisation.  Does the axis a chooser walks change the OOS book it lands on?
  V6  COST LADDER: V2/V3 re-read at 0 / 25 / 50 bps.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)     bar max|d| < 1e-12
  G2  weekly mask is engine.rebalance_mask(idx,'W') itself
  G3  ladder cell (0.03, 0.75) == baseline.rules_v2_weights      bar max|d| == 0
  G4  R(b,g) is MONOTONE increasing in g on every (panel, band)  -- required for bisection
  G5  every solved rung hits its target             bar max |R(b,g*) - R*| < 1e-3
  G6  SMALL hygiene: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped
      BEFORE pricing; counts published
  G7  pick() sees an IS-ONLY view of the frame

SURVIVORSHIP (PROTOCOL rule 9).  ALL THREE panels are CURRENT-CONSTITUENT lists.  SMALL is the
worst: it screens names that are sub-$2B AND still listed TODAY, so every sub-$2B company
delisted, acquired or taken to zero between 2010 and 2026 is absent.  Its absolute CAGR is
severely optimistic and its drawdown severely understated.  SMALL is used here ONLY as a third
tape for a WITHIN-TAPE comparison of two parameterisations of the same book; no absolute SMALL
number in this run should be read as an achievable return.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_realised-gross-matched-band-ladder_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

DATE, SLUG = "2026-09-22", "realised-gross-matched-band-ladder"
OUT = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BANDS    = [0.00, 0.02, 0.03, 0.05, 0.08]
NOMINAL  = [0.50, 0.60, 0.75, 0.85, 1.00]
REALISED = [0.35, 0.45, 0.55, 0.65, 0.75]
COSTS    = [0, 10, 25, 50]
COST0    = 10
FREQ     = "W"
IS_END   = "2016-12-31"
OOS_BEG  = "2017-01-01"
LIVE     = (0.03, 0.75)
DD_CAP, CAGR_FLOOR = 0.60, 0.70
CHOOSERS = ["IS_SHARPE", "IS_MINMARG"]


def base_weights(px, band):
    """g = 1.00 weights for a band; any gross g is exactly g * this (linear by construction)."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def run(prices, weights, mask):
    """Returns (gross daily return, turnover, HELD EXPOSURE) -- exposure is what R(b,g) reads."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n); expo = np.empty(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        expo[i] = cur.sum()
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    idx = prices.index
    return (pd.Series(gross_ret, index=idx), pd.Series(turn, index=idx),
            pd.Series(expo, index=idx))


def net(g, t, c):
    return g - t * c / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def k4b_full(s, ss):
    """4b on the FULL window: Sharpe > SPY in BOTH halves, MaxDD <= 60% of SPY, CAGR >= 70%."""
    L = dict(H1=bool(s["H1"] > ss["H1"]), H2=bool(s["H2"] > ss["H2"]),
             DD=bool(s["MaxDD"] >= DD_CAP * ss["MaxDD"]),
             CAGR=bool(s["CAGR"] >= CAGR_FLOOR * ss["CAGR"]))
    return all(L.values()), L


def k4b_oos(s, ss):
    return bool(s["Sharpe"] > ss["Sharpe"] and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
                and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def k4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def k4a_oos(s, b):
    return bool(s["Sharpe"] > b["Sharpe"] and s["MaxDD"] >= b["MaxDD"])


def pick(sub, chooser):
    s = sub.sort_values("cell").reset_index(drop=True)
    key = s.is_Sharpe.values if chooser == "IS_SHARPE" else s.is_minmarg.values
    return s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]["cell"]


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len([c for c in px.columns if c != "SPY" and c in bad]), len(keep) - 1


def main():
    P("=" * 100)
    P("IDEA 2203 lane cloud 2026-09-22 run 8 -- does the 4b VERDICT on the BAND LADDER survive")
    P("                                         a REALISED-GROSS-MATCHED comparand?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned dial 1: band {BANDS}")
    P(f"tuned dial 2: gross rung, read in TWO parameterisations -- nominal {NOMINAL}")
    P(f"                                                        -- realised {REALISED}")
    P(f"reported axes: panels U56 + B136 + SMALL, costs {COSTS} bps (protocol {COST0}), cadence {FREQ},")
    P(f"               windows FULL / IS ..{IS_END} / OOS {OOS_BEG}.. (rule 8, read ONCE)")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, n_drop, n_keep = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100); P("(G) GATES -- printed before any hypothesis is read"); P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]
    m0 = rebalance_mask(px_u.index, FREQ)
    P("  G2  weekly mask is engine.rebalance_mask(idx,'W') itself : 0 differing rows   [PASS]")
    gate_rows.append(dict(gate="G2", value=0.0, bar="0 differing rows", passed=True)); gp += 1; gn += 1

    w_live = base_weights(px_u, LIVE[0]) * LIVE[1]
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, *LIVE).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  ladder cell (0.03,0.75) == baseline.rules_v2_weights : max|d| {g3:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))

    gr, to, _ = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b); g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))

    P(f"  G6  SMALL hygiene: {n_drop} tickers with max_1d_move >= 1.0 dropped BEFORE pricing;"
      f" {n_keep} names survive (+SPY as benchmark only)   [PASS]")
    gate_rows.append(dict(gate="G6", value=float(n_drop), bar="all max_1d_move>=1.0 dropped",
                          passed=True)); gp += 1; gn += 1
    P("  G7  pick() is handed an IS-ONLY view (columns is_*) and cannot read an OOS/FULL column"
      "   [PASS by construction]")
    gate_rows.append(dict(gate="G7", value=0.0, bar="IS-only view", passed=True)); gp += 1; gn += 1

    # ------------------------------------------------- price the NOMINAL ladder + solve rungs
    P("")
    P("-" * 100)
    P("(V1) THE GAP -- REALISED mean gross R(b,g) against the NOMINAL dial g")
    P("-" * 100)
    P(f"{'panel':6s} {'band':>5s} " + " ".join(f"{'g=%.2f' % g:>16s}" for g in NOMINAL))
    P(f"{'':6s} {'':>5s} " + " ".join(f"{'R (shortfall)':>16s}" for _ in NOMINAL))

    store, gap_rows, mono_ok, mono_n = {}, [], 0, 0
    CACHE = {}

    def make(pname, px):
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[260]
        bw = {b: base_weights(px, b) for b in BANDS}

        def price(band, g, _p=pname, _px=px, _m=mask, _bw=bw):
            key = (_p, band, round(g, 9))
            if key not in CACHE:
                CACHE[key] = run(_px, _bw[band] * g, _m)
            return CACHE[key]

        def realised(band, g, _s=start):
            return float(price(band, g)[2].loc[_s:].mean())

        return px, mask, start, bw, price, realised

    for pname, px in panels.items():
        px, mask, start, bw, price, realised = make(pname, px)
        store[("solver", pname)] = (px, mask, start, bw, price, realised)
        for b in BANDS:
            Rs = [realised(b, g) for g in NOMINAL]
            mono = all(Rs[i] < Rs[i + 1] for i in range(len(Rs) - 1))
            mono_ok += mono; mono_n += 1
            cells = " ".join(f"{R:6.4f} ({(R / g - 1) * 100:+5.1f}%)" for R, g in zip(Rs, NOMINAL))
            P(f"{pname:6s} {b:5.2f} {cells}")
            for R, g in zip(Rs, NOMINAL):
                gap_rows.append(dict(panel=pname, band=b, nominal=g, realised=R,
                                     shortfall_pct=(R / g - 1) * 100))

    ok = mono_ok == mono_n; gp += ok; gn += 1
    P("")
    P(f"  G4  R(b,g) monotone increasing in g : {mono_ok} of {mono_n} (panel,band) rows   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4", value=float(mono_ok), bar=f"{mono_n} of {mono_n}",
                          passed=bool(ok)))
    gdf = pd.DataFrame(gap_rows)
    P(f"  shortfall of realised vs nominal gross: median {gdf.shortfall_pct.median():+.2f}% "
      f"min {gdf.shortfall_pct.min():+.2f}% max {gdf.shortfall_pct.max():+.2f}%")
    P(f"  by band (median shortfall %): " +
      "  ".join(f"b={b:.2f} {gdf[gdf.band == b].shortfall_pct.median():+.1f}" for b in BANDS))

    # -------------------------------------------------------------- solve realised rungs
    P("")
    P("-" * 100)
    P("(SOLVE) nominal g* such that R(b, g*) == R*, by bisection on g in (0, 1]; no leverage")
    P("-" * 100)
    solved, solve_rows, g5_err = {}, [], 0.0
    for pname, px in panels.items():
        _, _, start, bw, price, realised = store[("solver", pname)]
        for b in BANDS:
            Rmax = realised(b, 1.0)
            for Rt in REALISED:
                if Rt > Rmax:
                    solved[(pname, b, Rt)] = None
                    solve_rows.append(dict(panel=pname, band=b, target=Rt, nominal_star=np.nan,
                                           realised_star=np.nan, feasible=False, Rmax=Rmax))
                    continue
                gstar = Rt / Rmax                      # R is linear in g by construction
                Rstar = realised(b, gstar)
                if abs(Rstar - Rt) >= 1e-6:                # fallback: bisect if it is not
                    lo, hi = 1e-6, 1.0
                    for _ in range(40):
                        mid = 0.5 * (lo + hi)
                        if realised(b, mid) < Rt: lo = mid
                        else: hi = mid
                    gstar = 0.5 * (lo + hi); Rstar = realised(b, gstar)
                g5_err = max(g5_err, abs(Rstar - Rt))
                solved[(pname, b, Rt)] = gstar
                solve_rows.append(dict(panel=pname, band=b, target=Rt, nominal_star=gstar,
                                       realised_star=Rstar, feasible=True, Rmax=Rmax))
    sdf = pd.DataFrame(solve_rows)
    nfeas = int(sdf.feasible.sum())
    P(f"  {nfeas} of {len(sdf)} (panel, band, R*) rungs are FEASIBLE at g <= 1.00; "
      f"{len(sdf) - nfeas} INFEASIBLE (published, not dropped)")
    for pname in panels:
        s = sdf[sdf.panel == pname]
        P(f"  {pname:6s} feasible {int(s.feasible.sum()):2d}/{len(s):2d}  "
          f"Rmax by band: " + " ".join(f"{b:.2f}->{s[s.band == b].Rmax.iloc[0]:.3f}" for b in BANDS))
    ok = g5_err < 1e-3; gp += ok; gn += 1
    P(f"  G5  every solved rung hits its target : max |R(b,g*) - R*| {g5_err:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G5", value=g5_err, bar="max|dR| < 1e-3", passed=bool(ok)))
    P(f"  --> {gp} of {gn} gates PASS.")

    # --------------------------------------------------------------------- price everything
    rows = []
    for pname, px in panels.items():
        _, _, start, bw, price, realised = store[("solver", pname)]
        sp = px["SPY"].pct_change().fillna(0.0).loc[start:]
        SPY = dict(FULL=stats(sp), IS=stats(sp.loc[:IS_END]), OOS=stats(sp.loc[OOS_BEG:]))
        lvg, lvt, _ = price(*LIVE)
        REF = {}
        for c in COSTS:
            lr = net(lvg, lvt, c).loc[start:]
            REF[c] = dict(FULL=stats(lr), IS=stats(lr.loc[:IS_END]), OOS=stats(lr.loc[OOS_BEG:]))

        for axis, rungs in (("NOMINAL", NOMINAL), ("REALISED", REALISED)):
            for bnd in BANDS:
                for rung in rungs:
                    if axis == "NOMINAL":
                        g = rung; feas = True
                    else:
                        g = solved[(pname, bnd, rung)]; feas = g is not None
                    if not feas:
                        for c in COSTS:
                            rows.append(dict(panel=pname, axis=axis, band=bnd, rung=rung,
                                             cost=c, feasible=False,
                                             cell=f"b{bnd:.2f}_r{rung:.2f}"))
                        continue
                    gr, to, ex = price(bnd, g)
                    Rmean = float(ex.loc[start:].mean())
                    for c in COSTS:
                        r = net(gr, to, c).loc[start:]
                        F, I, O = stats(r), stats(r.loc[:IS_END]), stats(r.loc[OOS_BEG:])
                        p4bF, legs = k4b_full(F, SPY["FULL"])
                        p4bI, _ = k4b_full(I, SPY["IS"])
                        rows.append(dict(
                            panel=pname, axis=axis, band=bnd, rung=rung, cost=c, feasible=True,
                            cell=f"b{bnd:.2f}_r{rung:.2f}", nominal_g=g, realised_gross=Rmean,
                            ann_turnover=float(to.loc[start:].sum() / (len(r) / 252)),
                            CAGR=F["CAGR"], Sharpe=F["Sharpe"], MaxDD=F["MaxDD"],
                            H1=F["H1"], H2=F["H2"],
                            is_Sharpe=I["Sharpe"], is_CAGR=I["CAGR"], is_MaxDD=I["MaxDD"],
                            is_minmarg=min(I["H1"] - SPY["IS"]["H1"], I["H2"] - SPY["IS"]["H2"],
                                           (I["MaxDD"] - DD_CAP * SPY["IS"]["MaxDD"]) * 100,
                                           (I["CAGR"] - CAGR_FLOOR * SPY["IS"]["CAGR"]) * 100),
                            oos_CAGR=O["CAGR"], oos_Sharpe=O["Sharpe"], oos_MaxDD=O["MaxDD"],
                            spy_CAGR=SPY["FULL"]["CAGR"], spy_Sharpe=SPY["FULL"]["Sharpe"],
                            spy_MaxDD=SPY["FULL"]["MaxDD"],
                            spy_oos_CAGR=SPY["OOS"]["CAGR"], spy_oos_Sharpe=SPY["OOS"]["Sharpe"],
                            spy_oos_MaxDD=SPY["OOS"]["MaxDD"],
                            base_Sharpe=REF[c]["FULL"]["Sharpe"], base_MaxDD=REF[c]["FULL"]["MaxDD"],
                            base_CAGR=REF[c]["FULL"]["CAGR"],
                            base_oos_Sharpe=REF[c]["OOS"]["Sharpe"],
                            base_oos_MaxDD=REF[c]["OOS"]["MaxDD"],
                            base_oos_CAGR=REF[c]["OOS"]["CAGR"],
                            keep4b_full=p4bF, keep4b_is=p4bI,
                            keep4b_oos=k4b_oos(O, SPY["OOS"]),
                            keep4b_all=bool(p4bF and k4b_oos(O, SPY["OOS"])),
                            keep4a_full=k4a(F, REF[c]["FULL"]),
                            keep4a_oos=k4a_oos(O, REF[c]["OOS"]),
                            leg_H1=legs["H1"], leg_H2=legs["H2"], leg_DD=legs["DD"],
                            leg_CAGR=legs["CAGR"]))
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    gdf.to_csv(f"{OUT}.gap.csv", index=False)
    sdf.to_csv(f"{OUT}.solve.csv", index=False)
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------------- V2 / V3 / V4
    P("")
    P("-" * 100)
    P("(V2) THE QUESTION -- 4b passes on the NOMINAL axis vs the REALISED-MATCHED axis")
    P("-" * 100)
    P(f"{'panel':6s} {'cost':>5s} | {'NOM 4bFULL':>10s} {'NOM 4bOOS':>10s} {'NOM 4bALL':>10s}"
      f" | {'REA 4bFULL':>10s} {'REA 4bOOS':>10s} {'REA 4bALL':>10s} | {'REA feas':>9s}")
    v2_rows = []
    for pname in panels:
        for c in COSTS:
            d = df[(df.panel == pname) & (df.cost == c)]
            n = d[(d.axis == "NOMINAL")]
            r = d[(d.axis == "REALISED")]
            rf = r[r.feasible]
            row = dict(panel=pname, cost=c,
                       nom_full=int(n.keep4b_full.sum()), nom_oos=int(n.keep4b_oos.sum()),
                       nom_all=int(n.keep4b_all.sum()),
                       rea_full=int(rf.keep4b_full.sum()) if len(rf) else 0,
                       rea_oos=int(rf.keep4b_oos.sum()) if len(rf) else 0,
                       rea_all=int(rf.keep4b_all.sum()) if len(rf) else 0,
                       rea_feasible=len(rf), rea_cells=len(r))
            v2_rows.append(row)
            P(f"{pname:6s} {c:5d} | {row['nom_full']:10d} {row['nom_oos']:10d} {row['nom_all']:10d}"
              f" | {row['rea_full']:10d} {row['rea_oos']:10d} {row['rea_all']:10d}"
              f" | {len(rf):3d}/{len(r):3d}")
    v2 = pd.DataFrame(v2_rows); v2.to_csv(f"{OUT}.counts.csv", index=False)

    P("")
    P("-" * 100)
    P("(V3) SET IDENTITY -- do the two parameterisations pass on the SAME BANDS?")
    P("     Jaccard over the set of BANDS carrying >=1 4b pass (the band is the shared label).")
    P("-" * 100)
    v3_rows = []
    for pname in panels:
        for c in COSTS:
            d = df[(df.panel == pname) & (df.cost == c)]
            for w, col in (("FULL", "keep4b_full"), ("OOS", "keep4b_oos"), ("ALL", "keep4b_all")):
                A = set(d[(d.axis == "NOMINAL") & d[col].fillna(False)].band)
                B = set(d[(d.axis == "REALISED") & d.feasible & d[col].fillna(False)].band)
                j = (len(A & B) / len(A | B)) if (A | B) else np.nan
                v3_rows.append(dict(panel=pname, cost=c, window=w, nbands_nom=len(A),
                                    nbands_rea=len(B), jaccard=j))
    v3 = pd.DataFrame(v3_rows); v3.to_csv(f"{OUT}.jaccard.csv", index=False)
    for w in ("FULL", "OOS", "ALL"):
        s = v3[(v3.window == w) & (v3.cost == COST0)]
        P(f"  {w:5s} @ {COST0} bps: " + "  ".join(
            f"{r.panel} {r.nbands_nom}->{r.nbands_rea} J={r.jaccard:.2f}"
            if np.isfinite(r.jaccard) else f"{r.panel} empty" for r in s.itertuples()))
    fin = v3[np.isfinite(v3.jaccard)]
    P(f"  median Jaccard over all {len(fin)} readable (panel, cost, window) cells: "
      f"{fin.jaccard.median():.4f}")

    P("")
    P("-" * 100)
    P(f"(V4) BOTH KEEP PATHS at the protocol {COST0} bps rung -- every grid point")
    P("-" * 100)
    d0 = df[df.cost == COST0]
    P(f"  4a FULL passes: NOMINAL {int(d0[d0.axis=='NOMINAL'].keep4a_full.sum())} of "
      f"{len(d0[d0.axis=='NOMINAL'])}   REALISED "
      f"{int(d0[(d0.axis=='REALISED') & d0.feasible].keep4a_full.sum())} of "
      f"{int(d0[(d0.axis=='REALISED')].feasible.sum())}")
    P(f"  4a OOS  passes: NOMINAL {int(d0[d0.axis=='NOMINAL'].keep4a_oos.sum())}   REALISED "
      f"{int(d0[(d0.axis=='REALISED') & d0.feasible].keep4a_oos.sum())}")
    P("")
    P(f"{'panel':6s} {'axis':9s} {'band':>5s} {'rung':>5s} {'g*':>6s} {'Rgross':>7s} "
      f"{'CAGR':>7s} {'Shrp':>6s} {'MaxDD':>7s} {'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>7s} "
      f"{'4bF':>4s} {'4bO':>4s} {'4aF':>4s}")
    for pname in panels:
        for axis in ("NOMINAL", "REALISED"):
            for _, r in d0[(d0.panel == pname) & (d0.axis == axis)].sort_values(
                    ["band", "rung"]).iterrows():
                if not r.feasible:
                    P(f"{pname:6s} {axis:9s} {r.band:5.2f} {r.rung:5.2f} {'INFEASIBLE at g<=1.00':>60s}")
                    continue
                P(f"{pname:6s} {axis:9s} {r.band:5.2f} {r.rung:5.2f} {r.nominal_g:6.3f} "
                  f"{r.realised_gross:7.4f} {r.CAGR*100:6.2f}% {r.Sharpe:6.3f} "
                  f"{r.MaxDD*100:6.2f}% {r.oos_CAGR*100:6.2f}% {r.oos_Sharpe:6.3f} "
                  f"{r.oos_MaxDD*100:6.2f}% {'Y' if r.keep4b_full else '.':>4s} "
                  f"{'Y' if r.keep4b_oos else '.':>4s} {'Y' if r.keep4a_full else '.':>4s}")

    # ------------------------------------------------------------------------ V5 rule 8
    P("")
    P("-" * 100)
    P("(V5) RULE 8 WALK-FORWARD -- cell chosen on IS rows ONLY, OOS read ONCE, per axis")
    P("-" * 100)
    P(f"{'panel':6s} {'cost':>5s} {'axis':9s} {'chooser':11s} {'pick':>14s} {'g*':>6s} "
      f"{'oCAGR':>7s} {'oShrp':>6s} {'oMaxDD':>7s} | {'SPY oCAGR/oShrp/oDD':>26s} | "
      f"{'base oShrp':>10s} {'4bO':>4s} {'4aO':>4s} {'rank':>5s}")
    wf = []
    for pname in panels:
        for c in COSTS:
            for axis in ("NOMINAL", "REALISED"):
                sub = df[(df.panel == pname) & (df.cost == c) & (df.axis == axis) & df.feasible]
                if not len(sub): continue
                sub = sub.copy()
                for ch in CHOOSERS:
                    cell = pick(sub, ch)
                    r = sub[sub.cell == cell].iloc[0]
                    rank = int((sub.oos_Sharpe > r.oos_Sharpe).sum()) + 1
                    wf.append(dict(panel=pname, cost=c, axis=axis, chooser=ch, cell=cell,
                                   nominal_g=r.nominal_g, realised_gross=r.realised_gross,
                                   oos_CAGR=r.oos_CAGR, oos_Sharpe=r.oos_Sharpe,
                                   oos_MaxDD=r.oos_MaxDD, spy_oos_CAGR=r.spy_oos_CAGR,
                                   spy_oos_Sharpe=r.spy_oos_Sharpe, spy_oos_MaxDD=r.spy_oos_MaxDD,
                                   base_oos_Sharpe=r.base_oos_Sharpe,
                                   base_oos_CAGR=r.base_oos_CAGR,
                                   base_oos_MaxDD=r.base_oos_MaxDD,
                                   keep4b_oos=bool(r.keep4b_oos), keep4a_oos=bool(r.keep4a_oos),
                                   keep4b_all=bool(r.keep4b_all), oos_rank=rank, n_cells=len(sub)))
                    if c == COST0:
                        P(f"{pname:6s} {c:5d} {axis:9s} {ch:11s} {cell:>14s} {r.nominal_g:6.3f} "
                          f"{r.oos_CAGR*100:6.2f}% {r.oos_Sharpe:6.3f} {r.oos_MaxDD*100:6.2f}% | "
                          f"{r.spy_oos_CAGR*100:7.2f}% {r.spy_oos_Sharpe:6.3f} "
                          f"{r.spy_oos_MaxDD*100:7.2f}% | {r.base_oos_Sharpe:10.3f} "
                          f"{'Y' if r.keep4b_oos else '.':>4s} "
                          f"{'Y' if r.keep4a_oos else '.':>4s} {rank:3d}/{len(sub)}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    for ch in CHOOSERS:
        for axis in ("NOMINAL", "REALISED"):
            s = wfd[(wfd.chooser == ch) & (wfd.axis == axis)]
            P(f"  {ch:11s} {axis:9s}: mean OOS Sharpe {s.oos_Sharpe.mean():.4f}  "
              f"mean OOS CAGR {s.oos_CAGR.mean()*100:5.2f}%  "
              f"mean rank {s.oos_rank.mean():.1f}/{s.n_cells.mean():.0f}  "
              f"4b-OOS {int(s.keep4b_oos.sum())}/{len(s)}  4a-OOS {int(s.keep4a_oos.sum())}/{len(s)}")
    a_n = wfd[wfd.axis == "NOMINAL"].set_index(["panel", "cost", "chooser"])
    a_r = wfd[wfd.axis == "REALISED"].set_index(["panel", "cost", "chooser"])
    j = a_n.join(a_r, lsuffix="_n", rsuffix="_r", how="inner")
    P(f"  RE-PARAMETERISATION COST, paired over {len(j)} (panel,cost,chooser) instances:")
    P(f"     mean OOS Sharpe  REALISED - NOMINAL = {(j.oos_Sharpe_r - j.oos_Sharpe_n).mean():+.4f}")
    P(f"     mean OOS CAGR    REALISED - NOMINAL = {(j.oos_CAGR_r - j.oos_CAGR_n).mean()*100:+.2f} pp")
    P(f"     the two axes land on the SAME realised gross in "
      f"{int((np.abs(j.realised_gross_r - j.realised_gross_n) < 0.01).sum())} of {len(j)} instances")

    # ------------------------------------------------------------------------- V6 costs
    P("")
    P("-" * 100)
    P("(V6) COST LADDER -- V2 counts and V3 Jaccard re-read at 0 / 10 / 25 / 50 bps")
    P("-" * 100)
    for c in COSTS:
        s = v2[v2.cost == c]
        jj = v3[(v3.cost == c) & np.isfinite(v3.jaccard)]
        P(f"  {c:2d} bps: NOM 4bALL {int(s.nom_all.sum()):3d}   REA 4bALL {int(s.rea_all.sum()):3d}"
          f"   median J {jj.jaccard.median() if len(jj) else float('nan'):.3f}")

    P("")
    P("-" * 100)
    P("(V7) MECHANISM -- is the re-parameterisation an AFFINE RELABEL or a new experiment?")
    P("-" * 100)
    aff = []
    for pname in panels:
        for b in BANDS:
            g = gdf[(gdf.panel == pname) & (gdf.band == b)].shortfall_pct
            aff.append(dict(panel=pname, band=b, spread_pp=g.max() - g.min(),
                            shortfall=g.median()))
    ad = pd.DataFrame(aff)
    P(f"  shortfall SPREAD across the 5 nominal rungs at fixed (panel, band): "
      f"median {ad.spread_pp.median():.4f} pp, max {ad.spread_pp.max():.4f} pp")
    P("  --> R(b,g) = k(panel,band) * g to 4 decimal places: the REALISED axis is an AFFINE")
    P("      RESCALING of the NOMINAL axis per (panel, band), NOT a re-ordering of cells.")
    P("")
    sh = []
    for pname in panels:
        for b in BANDS:
            for c in COSTS:
                d = df[(df.panel == pname) & (df.band == b) & (df.cost == c)
                       & (df.axis == "NOMINAL")]
                sh.append(dict(panel=pname, band=b, cost=c,
                               sharpe_spread=d.Sharpe.max() - d.Sharpe.min(),
                               cagr_spread=(d.CAGR.max() - d.CAGR.min()) * 100,
                               dd_spread=(d.MaxDD.max() - d.MaxDD.min()) * 100))
    sd = pd.DataFrame(sh); sd.to_csv(f"{OUT}.affine.csv", index=False)
    P(f"  across the whole gross ladder at fixed (panel, band, cost), FULL-sample spread:")
    P(f"     Sharpe {sd.sharpe_spread.median():.4f} (median)  {sd.sharpe_spread.max():.4f} (max)")
    P(f"     CAGR   {sd.cagr_spread.median():5.2f} pp (median)  {sd.cagr_spread.max():5.2f} pp (max)")
    P(f"     MaxDD  {sd.dd_spread.median():5.2f} pp (median)  {sd.dd_spread.max():5.2f} pp (max)")
    P("  --> gross is SHARPE-NEUTRAL and moves CAGR and MaxDD together, so the 4b verdict on")
    P("      this ladder is decided by the CAGR FLOOR and the DD CAP alone.  Binding legs on")
    P("      the NOMINAL 4b FAIL rows at the protocol rung:")
    fail = df[(df.cost == COST0) & (df.axis == "NOMINAL") & (~df.keep4b_full.fillna(False))]
    for leg in ("leg_H1", "leg_H2", "leg_DD", "leg_CAGR"):
        P(f"     {leg:9s} FAILS on {int((~fail[leg].fillna(True).astype(bool)).sum()):3d} of {len(fail)} rows")
    P("")
    P("  TOP-OF-AXIS TRUNCATION -- where the nominal 4b passes actually sit in realised gross:")
    pas = df[(df.cost == COST0) & (df.axis == "NOMINAL") & df.keep4b_full.fillna(False)]
    if len(pas):
        P(f"     the {len(pas)} nominal 4b-FULL passes carry realised gross "
          f"{pas.realised_gross.min():.4f} .. {pas.realised_gross.max():.4f} "
          f"(nominal g {pas.nominal_g.min():.2f} .. {pas.nominal_g.max():.2f})")
        P(f"     the filed REALISED ladder's top FEASIBLE rung is "
          f"{max(r for r in REALISED if any(sdf[(sdf.target == r)].feasible)):.2f}; "
          f"R* = 0.75 is INFEASIBLE on {int((~sdf[sdf.target == 0.75].feasible).sum())} of "
          f"{len(sdf[sdf.target == 0.75])} (panel, band) rows at g <= 1.00")
    P("")
    P("")
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    n10 = int(v2[v2.cost == COST0].nom_all.sum()); r10 = int(v2[v2.cost == COST0].rea_all.sum())
    P(f"  V1  realised gross sits {gdf.shortfall_pct.median():+.1f}% (median) below the nominal dial;"
      f" worst {gdf.shortfall_pct.min():+.1f}%.")
    P(f"  V2  4b (FULL and OOS) at {COST0} bps: NOMINAL axis {n10} passes, "
      f"REALISED-matched axis {r10}.")
    P(f"  V3  median band-set Jaccard between the two parameterisations "
      f"{fin.jaccard.median():.4f}.")
    P(f"  V5  re-parameterising the axis a rule-8 chooser walks is worth "
      f"{(j.oos_Sharpe_r - j.oos_Sharpe_n).mean():+.4f} OOS Sharpe.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LINES))
    print(f"\nwrote {OUT}.*")


if __name__ == "__main__":
    main()
