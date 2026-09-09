#!/usr/bin/env python3
"""Idea 306 - "is-the-MA-threshold-edge-a-CONSTANT-GROSS-effect" (cloud, 2026-09-09).

The question
------------
Idea 300's attribution says the MA-THRESHOLD form beats its matched constant-depth twin by
**+1.09 pp/yr of CAGR and +0.048 of Sharpe when the book is RESPREAD** (exposure pinned at the
target gross, so the gate can only choose WHICH names are held, never HOW MUCH is invested) -
and that the whole of that edge disappears once the same gate is run DEGROSS (gated weight
goes to cash).  Read literally, that says the MA threshold contains a genuine SELECTION edge
which de-grossing then throws away as cash drag.

That reading has never been tested at more than one gross.  It matters for capital, because if
the edge is real it is a pinned-exposure effect that should be there at 0.50, 0.75 and 1.00
gross alike; and if instead it only appears at the one gross the record happens to run (0.75)
it is a dial placement, not an edge.  It also has never been costed at the pair level: the MA
arm and the constant-depth arm do NOT trade the same amount, and a selection edge that is
smaller than the extra turnover it buys is not an edge at all.

So: run the pair directly, MA-THRESH minus matched QUANTILE-M, across cadence and gross,
under BOTH constructions, at 10 bps AND at an exactly derived 0 bps, and report whether the
edge survives costs at ANY gross.

Pre-registered hypotheses and bars (written before any number was read)
----------------------------------------------------------------------
H_EDGE_IS_REAL.  The MA form carries a selection edge that is present whenever exposure is
    pinned, at every gross.
    BAR (all four clauses, on RESPREAD, at 10 bps, pooled over the 9 thetas x 5 cadences of
    each panel x gross cell):
      (1) mean dSharpe = Sharpe(MA) - Sharpe(QM) > 0 at ALL THREE gross levels, on the panel
          the claim was measured on (SMALL439), and the sign is the same on U56 and B136;
      (2) mean dCAGR >= +0.50 pp/yr at all three gross (half of idea 300's published +1.09);
      (3) the sign survives rule 8: OOS (2017-2026) mean dSharpe > 0 at all three gross after
          (theta, cadence) is chosen on 2010..2016 only;
      (4) costs do not eat it: mean dCAGR at 10 bps >= 50% of mean dCAGR at 0 bps, i.e. the
          selection edge is bigger than the extra turnover it buys.
H_EDGE_IS_A_DIAL_PLACEMENT.  Any clause fails; the report then says at WHICH gross, WHICH
    cadence and by how much, and quotes the breakeven bps of the pair.
The two are exhaustive and mutually exclusive.

Secondary, reported either way (the queue's own framing, "a CONSTANT-GROSS effect"):
  * is dSharpe INVARIANT in gross?  Idea 311 found Sharpe itself has a span <= 0.005 across the
    gross dial for unlevered scalar books.  If dSharpe is likewise flat in g, then "constant
    gross" is not what creates the edge and the DEGROSS loss is a pure cash-dilution effect,
    not evidence against selection.  Reported as the span of mean dSharpe over g and as an OLS
    slope on g.
  * BREAKEVEN BPS of the pair: dCAGR0 / d(turnover), the cost level at which the MA arm's extra
    trading exactly cancels its 0-bps edge.  If that number is below 10 bps the edge is already
    spent at the record's own cost assumption.

G0 - reproduction / validity gates, asserted and printed BEFORE any headline number
-----------------------------------------------------------------------------------
G0.1  Local cadence-extended runner == engine.backtest at D/W/M/Q on all three panels, max
      |dr_t| < 1e-15 (engine has no "A"; PROTOCOL forbids editing it).
G0.2  Idea 300/307's matching must reproduce: |mask fraction(QUANTILE-M) - mask fraction(MA)|
      < 0.01 at all 9 thetas on every panel.  Every number here is "at matched mean depth", so
      that claim has to be true before anything is read.
G0.3  Idea 300's committed .decomp.csv CAGR_rs0 (the 0-bps RESPREAD CAGR) must reproduce on
      SMALL439 at gross 0.75 for both families, all 9 thetas, W/M/Q: max |d CAGR| < 1e-9.
      This is what ties my RESPREAD arm to the arm the +1.09 pp/yr claim was computed on.

Design
------
PANELS (3): SMALL439 (the panel idea 300 measured the claim on; 483 sub-$2B names less the 44
      with max_1d_move >= 1.0), U56 (the live panel), B136.  SPY is benchmark only, never
      investable.  SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents of their screens -
      no delistings - so CAGR LEVELS are inflated and the 4a/4b columns inherit that whole.
      The headline is a PAIR DIFFERENCE on the same names, same ranking and same days, which
      the bias very largely leaves alone.

ARMS: MA-THRESH   IN where close > ma200*(1+theta)                     (depth moves with market)
      QUANTILE-M  IN the top ceil(x*n_t) by dist = close/ma200 - 1, x = the MA arm's OWN mean
                  mask fraction at that theta                          (constant depth, same rank)
CONSTRUCTIONS: RESPREAD (w = g/k_t on held names, exposure pinned at g)   <- where the edge is claimed
               DEGROSS  (w = g/n_t, gated weight to cash)                 <- the contrast

Tuned parameters (PROTOCOL rule 4: at most two)
      1. gross     {0.50, 0.75, 1.00}
      2. cadence   {D, W, M, Q, A}
      theta is a REPORTED axis, all 9 of idea 300's values, never selected outside the rule-8
      walk-forward; x is a deterministic function of theta (the matching), not a dial.
      Grid: 9 theta x 5 cadence x 3 gross x 2 arms x 2 constructions = 540 books per panel,
      1,620 books in total.  10 bps, next-day execution, no shorting, no leverage.  The 0-bps
      rung is DERIVED exactly (r0 = r10 + turnover*bps/1e4), never re-run.

Rule 8 walk-forward
      WF-A  per (panel, gross, construction): choose (theta, cadence) on IS 2010..2016-12-31 by
            IS Sharpe of the MA arm, read OOS 2017-01-01..2026 ONCE, and report the OOS PAIR
            difference at that same (theta, cadence) - the honest version of "would I have had
            the edge?".
      WF-B  OOS levels of the chosen MA book vs RULES v2 (live), SPY and the matched QM book.
      WF-C  does the IS pair difference predict the OOS pair difference better than a hard zero?
            MAE in pp/yr per panel x gross, against the zero baseline.

Verdicts: both KEEP paths on every one of the 1,620 books.
      4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
      4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .pairs.csv .walkforward.csv .leaderboard.txt .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

COST_BPS = 10
GROSSES = [0.50, 0.75, 1.00]
CADENCES = ["D", "W", "M", "Q", "A"]
THETAS = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]   # idea 300's grid verbatim
FAMILIES = ["MA-THRESH", "QUANTILE-M"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# pre-registered bars
BAR_DCAGR = 0.50            # pp/yr, clause (2)
BAR_COST_SHARE = 0.50       # clause (4): 10-bps edge as a share of the 0-bps edge
BAR_ENGINE = 1e-15
BAR_MASK_TOL = 0.01
BAR_REPRO = 1e-9

PRIOR300 = REPO / "research" / "backtests" / \
    "2026-09-06_does-a-pure-exposure-gate-exist-on-the-small-panel_C.decomp.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def tstat(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


# ---------------------------------------------------------------- cadence + local engine
def cad_mask(idx, cad):
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def bt(prices, weights, cost_bps=COST_BPS, cad="W"):
    """engine.backtest's loop with the cadence mask swapped for one that also knows "A"."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = cad_mask(prices.index, cad).shift(1, fill_value=False)
    wv, rv, mv = w_target.values, rets.values, mask.values
    hv = np.zeros_like(wv)
    tv = np.zeros(len(prices.index))
    cur = np.zeros(len(prices.columns))
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wv[i]
            tv[i] = np.abs(new - cur).sum()
            cur = new
        hv[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    held = pd.DataFrame(hv, index=prices.index, columns=prices.columns)
    turnover = pd.Series(tv, index=prices.index)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "weights": held, "turnover": turnover}


# ---------------------------------------------------------------- panels / books
def panels():
    out = {}
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out["SMALL439"] = (s[[c for c in s.columns if c != "SPY" and c not in bad]], s["SPY"])
    u = load_universe()
    out["U56"] = (u.drop(columns=["SPY"]), u["SPY"])
    b = load_universe(broad=True)
    out["B136"] = (b.drop(columns=["SPY"], errors="ignore"), b["SPY"])
    return out, len(bad)


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    live = live_mask(px)
    dist = (px / px.rolling(200).mean() - 1).where(live)
    kt = np.ceil(x * live.sum(axis=1)).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, g, construction, gross):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], Vol=m["Vol"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


# ---------------------------------------------------------------- main
def main():
    P("=" * 185)
    P("Idea 306  is-the-MA-threshold-edge-a-CONSTANT-GROSS-effect  (cloud) | " + Path(__file__).name)
    P("=" * 185)
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly), next-day execution, no shorting/leverage.")
    P(f"tuned dials (2): gross {GROSSES} x cadence {CADENCES}.  theta is a REPORTED axis "
      f"({len(THETAS)} values, idea 300's grid verbatim), never selected outside rule 8.")
    P("grid: 9 theta x 5 cadence x 3 gross x 2 arms x 2 constructions = 540 books per panel, "
      "1,620 in total.  ALL reported.")
    P("pre-registered bars (written before any number was read):")
    P(f"  H_EDGE_IS_REAL : RESPREAD, 10 bps - (1) mean dSharpe > 0 at all 3 gross on SMALL439 "
      f"with the same sign on U56/B136; (2) mean dCAGR >= +{BAR_DCAGR} pp/yr at all 3 gross; "
      f"(3) the sign survives rule-8 OOS at all 3 gross; (4) 10-bps dCAGR >= "
      f"{BAR_COST_SHARE:.0%} of 0-bps dCAGR.")
    P("  H_EDGE_IS_A_DIAL_PLACEMENT : any clause fails -> report which gross/cadence and the "
      "pair's breakeven bps.")
    P("SURVIVORSHIP: SMALL439 and B136 are CURRENT constituents (no delistings). CAGR LEVELS "
      "inflated; the pair difference is on the same names/days and very largely immune; the "
      "4a/4b columns are NOT.")
    flush_log()

    PN, n_dropped = panels()
    META = {}
    P("\nPANELS")
    for name, (px, _) in PN.items():
        P(f"  {name:9s} {px.shape[1]:3d} investable names, {px.index[0].date()}..{px.index[-1].date()}, "
          f"{len(px)} bars  (SPY benchmark only, never investable)")
    P(f"  SMALL439 drops {n_dropped} names with max_1d_move >= 1.0 per data/small_meta.csv")

    px_u = load_universe()
    live_r_full = engine_backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                                  freq="W")["returns"]

    # --------------------------------------------- G0.1
    P("\n" + "=" * 185)
    P("G0.1  LOCAL CADENCE-EXTENDED RUNNER vs engine.backtest (read before anything else)")
    P("=" * 185)
    g01 = []
    for name, (px, _) in PN.items():
        probe = book(px, ma_gate(px, 0.0), "RESPREAD", 0.75)
        for cad in ["D", "W", "M", "Q"]:
            a = engine_backtest(px, probe, cost_bps=COST_BPS, freq=cad)["returns"]
            b = bt(px, probe, cost_bps=COST_BPS, cad=cad)["returns"]
            g01.append(dict(panel=name, cad=cad, max_abs_dr=float((a - b).abs().max()),
                            mask_diff_bars=int((cad_mask(px.index, cad).values
                                                != engine_mask(px.index, cad).values).sum())))
    G01 = pd.DataFrame(g01)
    P(G01.to_string(index=False, float_format=lambda x: f"{x:.3e}"))
    ok_g01 = bool((G01.max_abs_dr < BAR_ENGINE).all() and (G01.mask_diff_bars == 0).all())
    P(f"G0.1 {'PASS' if ok_g01 else 'FAIL'}  worst |dr| {G01.max_abs_dr.max():.3e} at {BAR_ENGINE:.0e}")

    # --------------------------------------------- G0.2 the matching
    P("\n" + "=" * 185)
    P("G0.2  THE MATCHING  x = the MA arm's OWN mean mask fraction at that theta (per panel)")
    P("=" * 185)
    GATES, match = {}, []
    for name, (px, spy_px) in PN.items():
        start = px.index[260]
        nlive = live_mask(px).loc[start:].sum(axis=1)
        for th in THETAS:
            gm = ma_gate(px, th)
            fma = float((gm.loc[start:].sum(axis=1) / nlive).mean())
            gq = quantile_gate(px, fma)
            fq = float((gq.loc[start:].sum(axis=1) / nlive).mean())
            GATES[(name, th)] = {"MA-THRESH": gm, "QUANTILE-M": gq}
            match.append(dict(panel=name, theta=th, x=fma, frac_ma=fma, frac_q=fq,
                              d_frac=fq - fma))
    M = pd.DataFrame(match)
    P(fmt(M.pivot_table(index="theta", columns="panel", values=["x", "d_frac"]), 5))
    ok_g02 = bool(M.d_frac.abs().max() < BAR_MASK_TOL)
    P(f"G0.2 {'PASS' if ok_g02 else 'FAIL'}  worst |d mask fraction| {M.d_frac.abs().max():.5f} "
      f"at {BAR_MASK_TOL}")
    flush_log()

    # --------------------------------------------- the grid
    P("\n" + "=" * 185)
    P("RUNNING THE 1,620-BOOK GRID")
    P("=" * 185)
    rows, pairs = [], []
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_r_full.reindex(px.index).fillna(0.0).loc[start:])
        META[pname] = (spy_s, live_s, start, years)
        for gross in GROSSES:
            for cad in CADENCES:
                for th in THETAS:
                    got = {}
                    for fam in FAMILIES:
                        for con in CONSTRUCTIONS:
                            res = bt(px, book(px, GATES[(pname, th)][fam], con, gross),
                                     cost_bps=COST_BPS, cad=cad)
                            r10 = res["returns"].loc[start:]
                            turn = res["turnover"].loc[start:]
                            r0 = r10 + turn * COST_BPS / 1e4
                            s = stat(r10)
                            got[(fam, con)] = dict(
                                s=s, r0=r0, CAGR0=cagr(r0),
                                isCAGR0=cagr(r0.loc[:IS_END]), oCAGR0=cagr(r0.loc[OOS_START:]),
                                turn_yr=float(turn.sum() / years),
                                gross_mean=float(res["weights"].loc[start:].sum(axis=1).mean()))
                            rows.append(dict(panel=pname, gross=gross, cad=cad, theta=th,
                                             family=fam, con=con, **s,
                                             CAGR0=got[(fam, con)]["CAGR0"],
                                             turn_yr=got[(fam, con)]["turn_yr"],
                                             gross_mean=got[(fam, con)]["gross_mean"],
                                             p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    for con in CONSTRUCTIONS:
                        a, b = got[("MA-THRESH", con)], got[("QUANTILE-M", con)]
                        dt = a["turn_yr"] - b["turn_yr"]
                        d0 = 100 * (a["CAGR0"] - b["CAGR0"])
                        pairs.append(dict(
                            panel=pname, gross=gross, cad=cad, theta=th, con=con,
                            dCAGR_pp=100 * (a["s"]["CAGR"] - b["s"]["CAGR"]),
                            dCAGR0_pp=d0,
                            dSharpe=a["s"]["Sharpe"] - b["s"]["Sharpe"],
                            dMaxDD_pp=100 * (a["s"]["MaxDD"] - b["s"]["MaxDD"]),
                            dVol_pp=100 * (a["s"]["Vol"] - b["s"]["Vol"]),
                            isDSharpe=a["s"]["isSharpe"] - b["s"]["isSharpe"],
                            oDSharpe=a["s"]["oSharpe"] - b["s"]["oSharpe"],
                            isDCAGR_pp=100 * (a["s"]["isCAGR"] - b["s"]["isCAGR"]),
                            oDCAGR_pp=100 * (a["s"]["oCAGR"] - b["s"]["oCAGR"]),
                            oDCAGR0_pp=100 * (a["oCAGR0"] - b["oCAGR0"]),
                            dturn=dt,
                            breakeven_bps=(d0 / 100 / dt * 1e4 if abs(dt) > 1e-9 else np.nan),
                            turn_ma=a["turn_yr"], turn_qm=b["turn_yr"],
                            Sharpe_ma=a["s"]["Sharpe"], Sharpe_qm=b["s"]["Sharpe"],
                            CAGR_ma=a["s"]["CAGR"], CAGR_qm=b["s"]["CAGR"]))
            P(f"  ... {pname} gross {gross:.2f} done ({len(CADENCES) * len(THETAS) * 4} books)")
            flush_log()
        P(f"  {pname}: SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} "
          f"MaxDD {spy_s['MaxDD']:.4f} halves {spy_s['H1']:.3f}/{spy_s['H2']:.3f} "
          f"OOS {spy_s['oSharpe']:.3f} | RULES v2 Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.3f}/{live_s['H2']:.3f}")

    G = pd.DataFrame(rows)
    G["p4b"] = G.f4b == "-"
    PA = pd.DataFrame(pairs)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    PA.to_csv(f"{OUT}.pairs.csv", index=False)

    # --------------------------------------------- G0.3 reproduction of idea 300
    P("\n" + "=" * 185)
    P("G0.3  REPRODUCTION of idea 300's committed RESPREAD 0-bps CAGR (SMALL439, gross 0.75)")
    P("=" * 185)
    ok_g03, note = False, "prior file not found"
    if PRIOR300.exists():
        pr = pd.read_csv(PRIOR300)
        pr = pr[pr.window == "FULL"][["theta", "cad", "family", "CAGR_rs0"]]
        mine = G[(G.panel == "SMALL439") & (G.gross == 0.75) & (G.con == "RESPREAD")
                 & G.cad.isin(["W", "M", "Q"])][["theta", "cad", "family", "CAGR0"]]
        j = pr.merge(mine, on=["theta", "cad", "family"])
        j["d"] = (j.CAGR_rs0 - j.CAGR0).abs()
        ok_g03 = bool(len(j) == 54 and j.d.max() < BAR_REPRO)
        note = f"matched {len(j)}/54 committed cells | worst |d CAGR| {j.d.max():.3e}"
    P(note)
    P(f"G0.3 {'PASS' if ok_g03 else 'FAIL'} at {BAR_REPRO:.0e}")
    P(f"\nGATES: G0.1 {'PASS' if ok_g01 else 'FAIL'} | G0.2 {'PASS' if ok_g02 else 'FAIL'} | "
      f"G0.3 {'PASS' if ok_g03 else 'FAIL'}")
    flush_log()

    # --------------------------------------------- THE HEADLINE
    P("\n" + "=" * 185)
    P("THE HEADLINE - PAIR DIFFERENCE  MA-THRESH minus matched QUANTILE-M, by construction x")
    P("gross (mean over 9 thetas x 5 cadences = 45 cells per entry; t is over those 45 cells)")
    P("=" * 185)
    head = []
    for pn in PN:
        for con in CONSTRUCTIONS:
            for gross in GROSSES:
                d = PA[(PA.panel == pn) & (PA.con == con) & (PA.gross == gross)]
                head.append(dict(panel=pn, con=con, gross=gross, n=len(d),
                                 dCAGR_pp=d.dCAGR_pp.mean(), t_dCAGR=tstat(d.dCAGR_pp),
                                 dCAGR0_pp=d.dCAGR0_pp.mean(),
                                 dSharpe=d.dSharpe.mean(), t_dSharpe=tstat(d.dSharpe),
                                 dMaxDD_pp=d.dMaxDD_pp.mean(),
                                 oDSharpe=d.oDSharpe.mean(), oDCAGR_pp=d.oDCAGR_pp.mean(),
                                 dturn=d.dturn.mean(),
                                 cost_share=(d.dCAGR_pp.mean() / d.dCAGR0_pp.mean()
                                             if abs(d.dCAGR0_pp.mean()) > 1e-9 else np.nan),
                                 n_pos_Sharpe=int((d.dSharpe > 0).sum())))
    H = pd.DataFrame(head)
    P(fmt(H.set_index(["panel", "con", "gross"]), 4))
    flush_log()

    P("\nIS dSharpe INVARIANT IN GROSS?  (the queue's 'constant-gross' framing)")
    inv = []
    for pn in PN:
        for con in CONSTRUCTIONS:
            h = H[(H.panel == pn) & (H.con == con)].set_index("gross")
            gs = np.array(GROSSES, float)
            sl = np.polyfit(gs, h.dSharpe.reindex(GROSSES).values, 1)[0]
            slc = np.polyfit(gs, h.dCAGR_pp.reindex(GROSSES).values, 1)[0]
            inv.append(dict(panel=pn, con=con,
                            dSharpe_span=float(h.dSharpe.max() - h.dSharpe.min()),
                            dSharpe_slope_per_g=float(sl),
                            dCAGR_span_pp=float(h.dCAGR_pp.max() - h.dCAGR_pp.min()),
                            dCAGR_slope_pp_per_g=float(slc)))
    INV = pd.DataFrame(inv).set_index(["panel", "con"])
    P(fmt(INV, 4))
    flush_log()

    P("\nBY CADENCE (RESPREAD only, mean over 9 thetas; the edge's cadence profile)")
    P(fmt(PA[PA.con == "RESPREAD"].pivot_table(index=["panel", "gross"], columns="cad",
                                               values="dSharpe")[CADENCES], 4))
    P("\nsame, dCAGR pp/yr:")
    P(fmt(PA[PA.con == "RESPREAD"].pivot_table(index=["panel", "gross"], columns="cad",
                                               values="dCAGR_pp")[CADENCES], 4))
    P("\nBY THETA (RESPREAD, gross 0.75, mean over cadence) - where in the dial the edge lives:")
    P(fmt(PA[(PA.con == "RESPREAD") & (PA.gross == 0.75)]
          .pivot_table(index="theta", columns="panel", values=["dCAGR_pp", "dSharpe"]), 4))
    flush_log()

    P("\nBREAKEVEN BPS OF THE PAIR  (dCAGR0 / extra turnover; the cost level that cancels the")
    P("0-bps edge.  Negative means the MA arm trades LESS, so costs help it.)")
    bk = PA[PA.con == "RESPREAD"].groupby(["panel", "gross"]).agg(
        mean_dturn=("dturn", "mean"), mean_dCAGR0_pp=("dCAGR0_pp", "mean"),
        median_breakeven_bps=("breakeven_bps", "median"),
        frac_breakeven_below_10=("breakeven_bps",
                                 lambda s: float(((s > 0) & (s < 10)).mean())))
    P(fmt(bk, 4))
    flush_log()

    # --------------------------------------------- pre-registered verdict
    P("\n" + "=" * 185)
    P("PRE-REGISTERED VERDICT  (RESPREAD, 10 bps)")
    P("=" * 185)
    hs = H[H.con == "RESPREAD"].set_index(["panel", "gross"])
    small = hs.loc["SMALL439"]
    c1 = bool((small.dSharpe > 0).all()
              and all((hs.loc[p].dSharpe > 0).all() == (small.dSharpe > 0).all() for p in PN))
    c1_detail = {p: [round(float(hs.loc[(p, g), "dSharpe"]), 4) for g in GROSSES] for p in PN}
    c2 = bool((small.dCAGR_pp >= BAR_DCAGR).all())
    c3 = bool((small.oDSharpe > 0).all())
    cs = small.cost_share
    c4 = bool((cs >= BAR_COST_SHARE).all())
    for k, v, det in (("(1) mean dSharpe > 0 at all 3 gross, same sign on all panels", c1,
                       str(c1_detail)),
                      (f"(2) mean dCAGR >= +{BAR_DCAGR} pp/yr at all 3 gross (SMALL439)", c2,
                       str([round(float(x), 4) for x in small.dCAGR_pp])),
                      ("(3) OOS mean dSharpe > 0 at all 3 gross (SMALL439)", c3,
                       str([round(float(x), 4) for x in small.oDSharpe])),
                      (f"(4) 10-bps dCAGR >= {BAR_COST_SHARE:.0%} of 0-bps dCAGR (SMALL439)", c4,
                       str([round(float(x), 4) for x in cs]))):
        P(f"  {'PASS' if v else 'FAIL':4s}  {k}   {det}")
    holds = bool(c1 and c2 and c3 and c4)
    P("")
    P(f"H_EDGE_IS_REAL            : {'HOLDS' if holds else 'FAILS'}")
    P(f"H_EDGE_IS_A_DIAL_PLACEMENT: {'FAILS' if holds else 'HOLDS'}")
    P("\nidea 300's published claim for reference: RESPREAD MA beats matched QM by +1.09 pp/yr "
      "and +0.048 Sharpe (SMALL439, gross 0.75).")
    ref = hs.loc[("SMALL439", 0.75)]
    P(f"the same cell here (mean over 9 theta x 5 cadence): dCAGR {ref.dCAGR_pp:+.4f} pp/yr, "
      f"dSharpe {ref.dSharpe:+.4f}, OOS dSharpe {ref.oDSharpe:+.4f}")
    w_only = PA[(PA.panel == "SMALL439") & (PA.gross == 0.75) & (PA.con == "RESPREAD")
                & PA.cad.isin(["W", "M", "Q"])]
    P(f"restricted to idea 300's own W/M/Q cadences: dCAGR {w_only.dCAGR_pp.mean():+.4f} pp/yr, "
      f"dSharpe {w_only.dSharpe.mean():+.4f} (n={len(w_only)})")
    flush_log()

    # --------------------------------------------- rule 8
    P("\n" + "=" * 185)
    P("RULE 8 WALK-FORWARD  (IS 2010..2016-12-31 chooses (theta, cadence) by the MA arm's IS")
    P("Sharpe; OOS 2017-01-01..2026 read ONCE at that same cell)")
    P("=" * 185)
    wf = []
    for pn in PN:
        spy_s, live_s, _, _ = META[pn]
        for con in CONSTRUCTIONS:
            for gross in GROSSES:
                sub = G[(G.panel == pn) & (G.con == con) & (G.gross == gross)
                        & (G.family == "MA-THRESH")]
                pick = sub.loc[sub.isSharpe.idxmax()]
                pr = PA[(PA.panel == pn) & (PA.con == con) & (PA.gross == gross)
                        & (PA.theta == pick.theta) & (PA.cad == pick.cad)].iloc[0]
                wf.append(dict(panel=pn, con=con, gross=gross,
                               pick=f"theta={pick.theta:+.2f},cad={pick.cad}",
                               oSharpe_MA=pick.oSharpe, oCAGR_MA=pick.oCAGR,
                               oMaxDD_MA=pick.oMaxDD,
                               oDSharpe_pair=pr.oDSharpe, oDCAGR_pair_pp=pr.oDCAGR_pp,
                               vs_SPY=pick.oSharpe - spy_s["oSharpe"],
                               vs_RULESv2=pick.oSharpe - live_s["oSharpe"],
                               regret=sub.oSharpe.max() - pick.oSharpe))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("\nWF-A/B:")
    P(fmt(WF.set_index(["panel", "con", "gross"]), 4))
    for pn in PN:
        spy_s, live_s, _, _ = META[pn]
        P(f"  {pn:9s} SPY OOS Sharpe {spy_s['oSharpe']:.4f} CAGR {spy_s['oCAGR']:.4f} "
          f"MaxDD {spy_s['oMaxDD']:.4f} | RULES v2 OOS Sharpe {live_s['oSharpe']:.4f} "
          f"CAGR {live_s['oCAGR']:.4f} MaxDD {live_s['oMaxDD']:.4f}")
    P(f"\nOOS pair difference positive in {int((WF.oDSharpe_pair > 0).sum())}/{len(WF)} "
      f"(panel x construction x gross) picks; mean {WF.oDSharpe_pair.mean():+.4f}")

    P("\nWF-C  does the IS pair difference beat a hard ZERO at predicting the OOS pair "
      "difference? (MAE in pp/yr of dCAGR, over the 45 theta x cadence cells)")
    wc = []
    for pn in PN:
        for con in CONSTRUCTIONS:
            for gross in GROSSES:
                d = PA[(PA.panel == pn) & (PA.con == con) & (PA.gross == gross)]
                wc.append(dict(panel=pn, con=con, gross=gross,
                               mean_is=d.isDCAGR_pp.mean(), mean_oos=d.oDCAGR_pp.mean(),
                               MAE_vs_zero=d.oDCAGR_pp.abs().mean(),
                               MAE_vs_IS_cell=(d.oDCAGR_pp - d.isDCAGR_pp).abs().mean(),
                               MAE_vs_IS_const=(d.oDCAGR_pp - d.isDCAGR_pp.mean()).abs().mean(),
                               sign_agree=int((np.sign(d.isDCAGR_pp)
                                               == np.sign(d.oDCAGR_pp)).sum())))
    WC = pd.DataFrame(wc).set_index(["panel", "con", "gross"])
    P(fmt(WC, 4))
    P(f"the IS estimate beats the zero in "
      f"{int((WC.MAE_vs_IS_cell < WC.MAE_vs_zero).sum())}/{len(WC)} cells "
      f"(cellwise) and {int((WC.MAE_vs_IS_const < WC.MAE_vs_zero).sum())}/{len(WC)} "
      f"(IS constant).")
    flush_log()

    # --------------------------------------------- KEEP paths
    P("\n" + "=" * 185)
    P("BOTH KEEP PATHS over all 1,620 books")
    P("=" * 185)
    P(f"4a {int(G.p4a.sum())}/{len(G)} | 4b {int(G.p4b.sum())}/{len(G)} | "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}")
    P("\nby panel x gross:")
    P(fmt(G.groupby(["panel", "gross"])[["p4a", "p4b"]].sum(), 0))
    P("\nby family x construction:")
    P(fmt(G.groupby(["family", "con"])[["p4a", "p4b"]].sum(), 0))
    P("\n4b failing clauses:")
    P(pd.Series([c for s in G.f4b for c in (s.split(",") if s != "-" else [])])
      .value_counts().to_string())
    if int(G.p4b.sum()):
        top = G[G.p4b].sort_values("Sharpe", ascending=False).head(20)
        P("\ntop 20 4b passers by full-sample Sharpe:")
        P(fmt(top[["panel", "gross", "cad", "theta", "family", "con", "CAGR", "Sharpe",
                   "MaxDD", "H1", "H2", "oSharpe", "turn_yr", "p4a"]], 4))
    P("\nbest book per panel by full-sample Sharpe:")
    P(fmt(G.loc[G.groupby("panel").Sharpe.idxmax()].set_index("panel")[
        ["gross", "cad", "theta", "family", "con", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
         "oSharpe", "p4a", "f4b"]], 4))
    flush_log()

    # --------------------------------------------- leaderboard
    P("\n" + "=" * 185)
    P("LEADERBOARD rows")
    P("=" * 185)
    fn = Path(__file__).name
    lb = []
    for pn in PN:
        spy_s, live_s, _, _ = META[pn]
        for gross in GROSSES:
            d = H[(H.panel == pn) & (H.con == "RESPREAD") & (H.gross == gross)].iloc[0]
            sub = G[(G.panel == pn) & (G.gross == gross) & (G.family == "MA-THRESH")
                    & (G.con == "RESPREAD")]
            b = sub.loc[sub.Sharpe.idxmax()]
            v = ("KEEP-candidate" if (b.p4a or b.p4b) else "KILL")
            lb.append(
                f"| 2026-09-09 | idea306 {pn} RESPREAD gross {gross:.2f}: MA-THRESH minus matched "
                f"QUANTILE-M = {d.dCAGR_pp:+.3f} pp/yr (t {d.t_dCAGR:+.2f}), dSharpe "
                f"{d.dSharpe:+.4f} (t {d.t_dSharpe:+.2f}), OOS dSharpe {d.oDSharpe:+.4f}; best MA "
                f"book theta {b.theta:+.2f} cad={b.cad} | {b.CAGR:.1%} | {b.Sharpe:.2f} | "
                f"{b.MaxDD:.1%} | {b.H1:.2f} / {b.H2:.2f} | "
                f"{live_s['Sharpe']:.2f} ({live_s['H1']:.2f}/{live_s['H2']:.2f}) | {v} | {fn} |")
    for r in lb:
        P(r)
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lb) + "\n")

    P("\n" + "=" * 185)
    P("ANSWER")
    P("=" * 185)
    for con in CONSTRUCTIONS:
        for pn in PN:
            h = H[(H.panel == pn) & (H.con == con)].set_index("gross")
            P(f"  {con:9s} {pn:9s} dCAGR pp/yr by gross: " +
              ", ".join(f"{g:.2f}={h.loc[g, 'dCAGR_pp']:+.3f}" for g in GROSSES) +
              " | dSharpe: " + ", ".join(f"{g:.2f}={h.loc[g, 'dSharpe']:+.4f}" for g in GROSSES) +
              " | OOS dSharpe: " +
              ", ".join(f"{g:.2f}={h.loc[g, 'oDSharpe']:+.4f}" for g in GROSSES))
    P(f"H_EDGE_IS_REAL {'HOLDS' if holds else 'FAILS'}; "
      f"H_EDGE_IS_A_DIAL_PLACEMENT {'FAILS' if holds else 'HOLDS'}.")
    P(f"KEEP paths: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}, "
      f"BOTH {int((G.p4a & G.p4b).sum())}/{len(G)}.")
    flush_log()


if __name__ == "__main__":
    main()
