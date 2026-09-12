#!/usr/bin/env python3
"""Idea 810 (cloud lane, 2026-09-12) - price the U56 / MA-BAND / g=1.00 VOL-gated book against its
GROSS-MATCHED CONTROL as the PRIMARY comparand.

QUESTION
--------
Idea 596 ran 144 gated arms and killed all of them on the right bar: 7 cleared PROTOCOL 4b on the
full sample, but 6 of the 7 are matched by a CONTROL-M that holds uniformly less with **no timing at
all** and passes 4b too, so 4b certified the exposure, not the clause.  One cell was recorded as a
loose end:

    U56 / 200d +/-3% band / g = 1.00 / VOL gate at 0.25
    arm      CAGR 11.08%  Sharpe 1.210  MaxDD  -9.57%
    CONTROL-M                    1.202  MaxDD -15.11%

i.e. at an equal Sharpe the arm cut the drawdown by 5.54 pp against its own gross-matched control -
an effect 4b structurally cannot see, because 4b's Sharpe legs are read against SPY and its DD leg is
a floor (>= 0.60 x SPY's), not a comparison with the control.  Idea 596 filed that cell as a
PRE-REGISTRATION TARGET, not a candidate, because the panel, the family and the gross were read off a
144-cell grid after the fact.  This run is that pre-registration.

WHAT IS PRE-REGISTERED (fixed before any number in this file was read)
    * the CELL: panel U56, book `baseline.rules_v2_weights` (200d +/-3% band, g/N of NAV, gated-out
      weight to CASH), gross g = 1.00, weekly, t+1 fill; gate family VOL (SPY 20d realised vol
      <= dial), dial 0.25, gate OFF => whole book to cash.
    * the HEADLINE COMPARAND: **CONTROL-M**, the same book x a constant so its mean realised gross
      equals the arm's.  Not SPY, not RULES v2 - those are reported, but the claim is about the
      clause, and only a gross-matched control can see a clause.
    * the HEADLINE STATISTIC: **dMaxDD_M = MaxDD(arm) - MaxDD(CONTROL-M)** (MaxDD is negative, so
      POSITIVE = the arm is shallower), reported beside dSharpe_M and dCAGR_M at every grid point.
    * the DECIDING TEST: rule 8.  The dial is chosen on the IS window alone by the IS value of the
      headline statistic, and the OOS dMaxDD_M is read ONCE.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue's own: dial, cost)
    1. dial in {0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60}   (8 rungs; 0.25 is the pre-reg cell)
    2. cost in {0, 5, 10, 25, 50} bps                              (5 rungs; 10 is PROTOCOL's)
All 8 x 5 = 40 points are reported.  REPORTED-NEVER-SELECTED axes: execution lag (t+1, t+2), window
(FULL / IS / OOS), and the 5 weekday offsets of the convention floor.  Nothing is picked on those.

PRE-REGISTERED HYPOTHESES (written before any credited number was read)
    H_REPRO  : at the pre-registered cell (dial 0.25, 10 bps, t+1) this file reproduces idea 596's
               committed numbers - arm CAGR 11.08% / Sharpe 1.210 / MaxDD -9.57%, CONTROL-M Sharpe
               1.202 / MaxDD -15.11% - to 1e-4 in Sharpe and 5e-4 in CAGR/MaxDD.  Same sandbox, same
               committed price cache, same runner: this is a HARD bar, not a drift tolerance.
    H_SIGN   : dMaxDD_M > 0 at the pre-registered cell at 10 bps.  (Reproduction leg; it should pass.)
    H_DIAL   : the DD advantage is not a one-dial artefact - dMaxDD_M > 0 at a MAJORITY of the 8
               dial rungs at 10 bps, and the rungs where it holds are CONTIGUOUS.
    H_COST   : dMaxDD_M is cost-insensitive (both books pay costs), |dMaxDD_M(50bps) -
               dMaxDD_M(0bps)| < 1.0 pp at the pre-registered dial, while dSharpe_M decays
               monotonically in cost.
    H_FLOOR  : the "equal Sharpe" in idea 596's reading is a FLOOR statement.  |dSharpe_M| at the
               pre-registered cell is INSIDE the convention floor (the max-min Sharpe spread of the
               same two books over the 5 weekday offsets of the same 5-day rebalance schedule),
               while |dMaxDD_M| is OUTSIDE the same floor measured in MaxDD.  If both are inside,
               the DD effect is a convention artefact and the cell dies here.
    H_WF     : rule 8.  Picking the dial on the IS window alone by IS dMaxDD_M gives a POSITIVE OOS
               dMaxDD_M, read once.  A DD edge that does not survive its own walk-forward is not a
               DD edge.
    H_4b     : the honest control, reproducing idea 596's kill - at the pre-registered cell BOTH the
               arm and CONTROL-M pass 4b, i.e. 4b does not separate them.

GATES (printed before any verdict is read)
    G1 a never-firing gate reproduces CONTROL-U exactly                         bar 1e-12
    G2 this file's fast runner == products/backtester/engine.backtest           bar 1e-9
    G3 CONTROL-M's mean realised gross == the arm's                             bar 1e-3
    G4 determinism: the whole grid recomputed, max abs diff                     bar 0

KEEP PATHS: 4a (vs RULES v2 live) and 4b (vs SPY) are evaluated for the arm AND for CONTROL-M at
every one of the 40 grid points, on FULL and OOS windows, and the counts reported.

SURVIVORSHIP: U56 is a current-constituent list (research/universe.json), so every level here is
optimistic.  The headline statistic is a WITHIN-PANEL difference between two books on the same names,
which survivorship moves far less than it moves levels; the walk-forward levels carry the full bias.

Deterministic, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import backtest, metrics, rebalance_mask          # noqa: E402

DATE = "2026-09-12"
SLUG = "price-the-U56-MA-BAND-g1.00-LIGHT-OVERLAY-against-its-GROSS-MATCHED-CONTROL"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ------------------------------------------------------------------ pinned cell (pre-registered)
PANEL = "U56"
BAND = 0.03
GROSS = 1.00
FAMILY = "VOL"
DIAL0 = 0.25
FREQ = "W"
LAG0 = 1
COST0 = 10.0
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LIVE_GROSS = 0.75                      # RULES v2 as it runs live

# ------------------------------------------------------------------ the two tuned ladders
DIALS = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
LAGS = [1, 2]                          # reported, never selected
KEEP_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

# idea 596's committed numbers at the pre-registered cell (H_REPRO)
P596 = dict(CAGR=0.1108, Sharpe=1.210, MaxDD=-0.0957, ctlM_Sharpe=1.202, ctlM_MaxDD=-0.1511)
REPRO_SH, REPRO_LVL = 1e-4, 5e-4

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


# ------------------------------------------------------------------ runner (ideas 596/804/805's)
def fast_run(prices, weights, mask, lag):
    """(gross return path before costs, turnover path, realised gross path)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(lag).fillna(0.0).values
    mk = mask.shift(lag, fill_value=False).values.copy()
    mk[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (pd.Series((held * rets).sum(axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series(held.sum(axis=1), index=idx))


def net(rg, tn, cost):
    return rg - tn * cost / 1e4


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def legs_4b(r, spy, lo=None, hi=None):
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    oos = (a2 > s2) if (lo or hi) else (
        metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"])
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2), "OOS": bool(oos),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def keep_4a(r, b, lo=None, hi=None):
    rr, bb = r.loc[lo:hi], b.loc[lo:hi]
    a1, a2 = halves(rr)
    b1, b2 = halves(bb)
    return bool(a1 > b1 and a2 > b2 and metrics(rr)["MaxDD"] >= metrics(bb)["MaxDD"])


def fails(L):
    return "+".join(k for k in KEEP_LEGS if not L[k]) or "-none-"


def vol_gate(px, dial):
    """The VOL family, verbatim from idea 596: SPY 20d realised vol <= dial.  True = hold."""
    spy = px["SPY"]
    return (spy.pct_change().rolling(20).std() * np.sqrt(252) <= dial)


def offset_mask(idx, k):
    """The k-th phase of a 5-trading-day rebalance schedule (the convention floor's axis)."""
    return pd.Series(np.arange(len(idx)) % 5 == k, index=idx)


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 110)
    P(f"# Idea 810 - {SLUG}  (cloud lane, {DATE})")
    P("=" * 110)
    P("# PRE-REGISTERED CELL: U56 / rules_v2 200d +/-3% band / g=1.00 / VOL gate / weekly / t+1.")
    P("# HEADLINE COMPARAND: CONTROL-M (same book x a constant matching the arm's mean realised")
    P("#   gross).  HEADLINE STATISTIC: dMaxDD_M = MaxDD(arm) - MaxDD(CONTROL-M), positive = the")
    P("#   arm is shallower.  SPY and RULES v2 are reported but are NOT the claim.")
    P(f"# TUNED: dial {DIALS} x cost {COSTS} = {len(DIALS)*len(COSTS)} points, ALL reported.")
    P("# REPORTED-NEVER-SELECTED: lag (t+1,t+2), window (FULL/IS/OOS), 5 weekday offsets.")
    P("# HYPOTHESES: H_REPRO H_SIGN H_DIAL H_COST H_FLOOR H_WF H_4b - all fixed before any number.")
    P("# SURVIVORSHIP: U56 is a current-constituent list; levels are optimistic.  The headline is a")
    P("#   within-panel difference between two books on the same names, which the bias moves less.")

    px = load_universe().dropna(how="all").ffill()
    trade = [c for c in px.columns if c != "SPY"]
    mask = rebalance_mask(px.index, FREQ)
    start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    P(f"\nPanel U56: {len(trade)} tradeable names + SPY, {len(px.loc[start:])} scored days "
      f"{start.date()}..{px.index[-1].date()}")

    Wb = rules_v2_weights(px, band=BAND, gross=GROSS)          # CONTROL-U weights (ungated)
    Wlive = rules_v2_weights(px, band=BAND, gross=LIVE_GROSS)  # RULES v2 as it runs live

    # ------------------------------------------------------------------ gates
    P(f"\n{'-'*110}\nGATES\n{'-'*110}")
    rg_u, tn_u, gr_u = fast_run(px, Wb, mask, LAG0)
    never = Wb.mul(pd.Series(1.0, index=px.index), axis=0)      # gate always ON
    rg_n, tn_n, _ = fast_run(px, never, mask, LAG0)
    g1 = max(float(np.abs((net(rg_n, tn_n, COST0) - net(rg_u, tn_u, COST0)).loc[start:].values).max()),
             float(np.abs((tn_n - tn_u).loc[start:].values).max()))
    eng = backtest(px, Wb, cost_bps=COST0, freq=FREQ)
    g2 = float(np.abs((net(rg_n, tn_n, COST0) - eng["returns"]).loc[start:].values).max())
    for nm, v, ok in [("G1 never-firing gate == CONTROL-U exactly", f"max|d| {g1:.3e}", g1 < 1e-12),
                      ("G2 fast_run == engine.backtest", f"max|d| {g2:.3e}", g2 < 1e-9)]:
        P(f"   {nm:<52} {v:<22} {'PASS' if ok else 'FAIL'}")
    assert g1 < 1e-12 and g2 < 1e-9, "a gate failed - no verdict is read"

    # ------------------------------------------------------------------ the grid
    rows = []
    g3max = 0.0
    gr_u_s = gr_u.loc[start:]
    mg_u = float(gr_u_s.mean())

    for lag in LAGS:
        rg_ul, tn_ul, gr_ul = fast_run(px, Wb, mask, lag)
        rg_lv, tn_lv, _ = fast_run(px, Wlive, mask, lag)
        mg_ul = float(gr_ul.loc[start:].mean())
        for dial in DIALS:
            s = vol_gate(px, dial).reindex(px.index).fillna(False)
            Wa = Wb.mul(s.astype(float), axis=0)
            rg_a, tn_a, gr_a = fast_run(px, Wa, mask, lag)
            mg_a = float(gr_a.loc[start:].mean())
            c = mg_a / mg_ul if mg_ul > 0 else 1.0
            rg_m, tn_m, gr_m = fast_run(px, Wb * c, mask, lag)
            g3max = max(g3max, abs(float(gr_m.loc[start:].mean()) - mg_a))
            fire = float((~s).loc[start:].mean())
            for cost in COSTS:
                r_a = net(rg_a, tn_a, cost).loc[start:]
                r_m = net(rg_m, tn_m, cost).loc[start:]
                r_u = net(rg_ul, tn_ul, cost).loc[start:]
                live = net(rg_lv, tn_lv, cost).loc[start:]
                ma, mm, mu = metrics(r_a), metrics(r_m), metrics(r_u)
                mai, mao = metrics(r_a.loc[:IS_END]), metrics(r_a.loc[OOS_START:])
                mmi, mmo = metrics(r_m.loc[:IS_END]), metrics(r_m.loc[OOS_START:])
                La, Lm = legs_4b(r_a, spy), legs_4b(r_m, spy)
                Lao, Lmo = legs_4b(r_a, spy, OOS_START, None), legs_4b(r_m, spy, OOS_START, None)
                rows.append(dict(
                    lag=lag, dial=dial, cost=cost, fire_rate=fire,
                    mean_gross_arm=mg_a, mean_gross_ctlU=mg_ul, match_c=c,
                    CAGR=ma["CAGR"], Sharpe=ma["Sharpe"], MaxDD=ma["MaxDD"],
                    H1=halves(r_a)[0], H2=halves(r_a)[1],
                    IS_CAGR=mai["CAGR"], IS_Sharpe=mai["Sharpe"], IS_MaxDD=mai["MaxDD"],
                    OOS_CAGR=mao["CAGR"], OOS_Sharpe=mao["Sharpe"], OOS_MaxDD=mao["MaxDD"],
                    ctlM_CAGR=mm["CAGR"], ctlM_Sharpe=mm["Sharpe"], ctlM_MaxDD=mm["MaxDD"],
                    ctlM_IS_MaxDD=mmi["MaxDD"], ctlM_OOS_MaxDD=mmo["MaxDD"],
                    ctlM_IS_Sharpe=mmi["Sharpe"], ctlM_OOS_Sharpe=mmo["Sharpe"],
                    ctlM_OOS_CAGR=mmo["CAGR"],
                    ctlU_CAGR=mu["CAGR"], ctlU_Sharpe=mu["Sharpe"], ctlU_MaxDD=mu["MaxDD"],
                    # ---- the headline statistic, and its two companions
                    dMaxDD_M=ma["MaxDD"] - mm["MaxDD"],
                    dSharpe_M=ma["Sharpe"] - mm["Sharpe"],
                    dCAGR_M=ma["CAGR"] - mm["CAGR"],
                    IS_dMaxDD_M=mai["MaxDD"] - mmi["MaxDD"],
                    OOS_dMaxDD_M=mao["MaxDD"] - mmo["MaxDD"],
                    IS_dSharpe_M=mai["Sharpe"] - mmi["Sharpe"],
                    OOS_dSharpe_M=mao["Sharpe"] - mmo["Sharpe"],
                    dMaxDD_U=ma["MaxDD"] - mu["MaxDD"],
                    turn_per_yr=float(tn_a.loc[start:].sum() / (len(r_a) / 252)),
                    ctlM_turn_per_yr=float(tn_m.loc[start:].sum() / (len(r_m) / 252)),
                    arm_4a=keep_4a(r_a, live), arm_4b=all(La.values()), arm_fail_4b=fails(La),
                    arm_4a_OOS=keep_4a(r_a, live, OOS_START, None), arm_4b_OOS=all(Lao.values()),
                    ctlM_4a=keep_4a(r_m, live), ctlM_4b=all(Lm.values()), ctlM_fail_4b=fails(Lm),
                    ctlM_4b_OOS=all(Lmo.values())))
    P(f"   {'G3 CONTROL-M mean gross == arm mean gross':<52} {f'max|d| {g3max:.3e}':<22} "
      f"{'PASS' if g3max < 1e-3 else 'FAIL'}")
    assert g3max < 1e-3, "G3 failed - the matched control is not matched"
    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)

    # determinism
    chk = []
    for dial in DIALS:
        s = vol_gate(px, dial).reindex(px.index).fillna(False)
        rg_a, tn_a, _ = fast_run(px, Wb.mul(s.astype(float), axis=0), mask, LAG0)
        chk.append(metrics(net(rg_a, tn_a, COST0).loc[start:])["Sharpe"])
    g4 = float(np.abs(np.array(chk) -
                      grid[(grid.lag == LAG0) & (grid.cost == COST0)].sort_values("dial")
                      .Sharpe.values).max())
    P(f"   {'G4 determinism (grid recomputed)':<52} {f'max|d| {g4:.3e}':<22} "
      f"{'PASS' if g4 == 0.0 else 'FAIL'}")

    # ------------------------------------------------------------------ H_REPRO
    P(f"\n{'-'*110}\nH_REPRO - does this file reproduce idea 596's committed cell?\n{'-'*110}")
    cell = grid[(grid.lag == LAG0) & (grid.cost == COST0) & (grid.dial == DIAL0)].iloc[0]
    rep = [("arm CAGR", cell.CAGR, P596["CAGR"], REPRO_LVL),
           ("arm Sharpe", cell.Sharpe, P596["Sharpe"], REPRO_SH),
           ("arm MaxDD", cell.MaxDD, P596["MaxDD"], REPRO_LVL),
           ("ctlM Sharpe", cell.ctlM_Sharpe, P596["ctlM_Sharpe"], REPRO_SH),
           ("ctlM MaxDD", cell.ctlM_MaxDD, P596["ctlM_MaxDD"], REPRO_LVL)]
    repro_ok = True
    P(f"   {'quantity':<14} {'this run':>12} {'idea 596':>12} {'|d|':>12} {'bar':>10}  verdict")
    for nm, a, b, bar in rep:
        d = abs(a - b)
        ok = d <= bar
        repro_ok &= ok
        P(f"   {nm:<14} {a:>12.4f} {b:>12.4f} {d:>12.2e} {bar:>10.0e}  {'PASS' if ok else 'FAIL'}")
    P(f"   H_REPRO -> {'PASS' if repro_ok else 'FAIL'}"
      + ("" if repro_ok else "   (idea 596's committed cell does NOT reproduce; every"
                             " downstream reading below is of THIS run's numbers, not of its)"))

    # ------------------------------------------------------------------ the full grid
    P(f"\n{'-'*110}\nTHE GRID - all 40 tuned points at t+1 (headline: dMaxDD_M, pp)\n{'-'*110}")
    at1 = grid[grid.lag == 1]
    P("   dMaxDD_M (pp, POSITIVE = arm shallower than its own gross-matched control)")
    piv = at1.pivot(index="dial", columns="cost", values="dMaxDD_M") * 100
    P("   " + piv.to_string(float_format=lambda x: f"{x:+.2f}").replace("\n", "\n   "))
    P("\n   dSharpe_M (POSITIVE = arm better)")
    pv2 = at1.pivot(index="dial", columns="cost", values="dSharpe_M")
    P("   " + pv2.to_string(float_format=lambda x: f"{x:+.3f}").replace("\n", "\n   "))
    P("\n   fire rate (share of days the gate is OFF) and mean realised gross, by dial")
    for d in DIALS:
        rw = at1[(at1.dial == d) & (at1.cost == COST0)].iloc[0]
        P(f"     dial {d:.2f}: OFF {rw.fire_rate:6.2%}   mean gross arm {rw.mean_gross_arm:.4f} "
          f"vs CONTROL-U {rw.mean_gross_ctlU:.4f}   match c {rw.match_c:.4f}   "
          f"turnover/yr arm {rw.turn_per_yr:.2f} vs ctlM {rw.ctlM_turn_per_yr:.2f}")

    # ------------------------------------------------------------------ H_SIGN / H_DIAL / H_COST
    P(f"\n{'-'*110}\nH_SIGN / H_DIAL / H_COST\n{'-'*110}")
    h_sign = bool(cell.dMaxDD_M > 0)
    P(f"   H_SIGN  dMaxDD_M at the pre-registered cell = {cell.dMaxDD_M*100:+.2f} pp "
      f"-> {'PASS' if h_sign else 'FAIL'}")
    at10 = at1[at1.cost == COST0].sort_values("dial")
    pos = at10.dMaxDD_M.values > 0
    npos = int(pos.sum())
    idxs = np.flatnonzero(pos)
    contig = bool(len(idxs) and idxs[-1] - idxs[0] + 1 == len(idxs))
    h_dial = bool(npos > len(DIALS) / 2 and contig)
    P(f"   H_DIAL  dMaxDD_M > 0 at {npos} of {len(DIALS)} dial rungs (10 bps), "
      f"contiguous={contig} -> {'PASS' if h_dial else 'FAIL'}")
    P("           by dial: " + "  ".join(
        f"{d:.2f}:{v*100:+.2f}" for d, v in zip(at10.dial, at10.dMaxDD_M)))
    cd = at1[at1.dial == DIAL0].sort_values("cost")
    spread = float(abs(cd[cd.cost == 50.0].dMaxDD_M.iloc[0] - cd[cd.cost == 0.0].dMaxDD_M.iloc[0]))
    dsh = cd.dSharpe_M.values
    mono = bool(np.all(np.diff(dsh) <= 1e-12))
    h_cost = bool(spread < 0.01 and mono)
    P(f"   H_COST  |dMaxDD_M(50) - dMaxDD_M(0)| = {spread*100:.3f} pp (bar 1.00 pp); "
      f"dSharpe_M monotone decreasing in cost = {mono} -> {'PASS' if h_cost else 'FAIL'}")
    P("           by cost: " + "  ".join(
        f"{int(c)}bps dDD {v*100:+.2f}pp dSh {s:+.3f}" for c, v, s in
        zip(cd.cost, cd.dMaxDD_M, cd.dSharpe_M)))

    # ------------------------------------------------------------------ H_FLOOR
    P(f"\n{'-'*110}\nH_FLOOR - the convention floor of these two books (5 weekday offsets)\n{'-'*110}")
    s0 = vol_gate(px, DIAL0).reindex(px.index).fillna(False)
    Wa0 = Wb.mul(s0.astype(float), axis=0)
    floor_rows = []
    for k in range(5):
        mk = offset_mask(px.index, k)
        rg_a, tn_a, gr_a = fast_run(px, Wa0, mk, LAG0)
        mg = float(gr_a.loc[start:].mean())
        rg_uo, tn_uo, gr_uo = fast_run(px, Wb, mk, LAG0)
        ck = mg / float(gr_uo.loc[start:].mean())
        rg_mo, tn_mo, _ = fast_run(px, Wb * ck, mk, LAG0)
        ra = net(rg_a, tn_a, COST0).loc[start:]
        rm = net(rg_mo, tn_mo, COST0).loc[start:]
        floor_rows.append(dict(offset=k, arm_Sharpe=metrics(ra)["Sharpe"],
                               arm_MaxDD=metrics(ra)["MaxDD"],
                               ctlM_Sharpe=metrics(rm)["Sharpe"],
                               ctlM_MaxDD=metrics(rm)["MaxDD"],
                               dSharpe_M=metrics(ra)["Sharpe"] - metrics(rm)["Sharpe"],
                               dMaxDD_M=metrics(ra)["MaxDD"] - metrics(rm)["MaxDD"]))
    fl = pd.DataFrame(floor_rows)
    fl.to_csv(f"{OUT}.floor.csv", index=False)
    fs = float(fl[["arm_Sharpe", "ctlM_Sharpe"]].values.max() -
               fl[["arm_Sharpe", "ctlM_Sharpe"]].values.min())
    fd = float(fl[["arm_MaxDD", "ctlM_MaxDD"]].values.max() -
               fl[["arm_MaxDD", "ctlM_MaxDD"]].values.min())
    P("   " + fl.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P(f"\n   convention floor  Sharpe {fs:.4f}   MaxDD {fd*100:.2f} pp"
      f"   (max-min over the 5 offsets of the SAME two books)")
    P(f"   measured at the pre-registered cell: |dSharpe_M| {abs(cell.dSharpe_M):.4f}, "
      f"|dMaxDD_M| {abs(cell.dMaxDD_M)*100:.2f} pp")
    sh_inside = abs(cell.dSharpe_M) < fs
    dd_outside = abs(cell.dMaxDD_M) > fd
    h_floor = bool(sh_inside and dd_outside)
    P(f"   Sharpe gap INSIDE its floor = {sh_inside}; MaxDD gap OUTSIDE its floor = {dd_outside}")
    P(f"   H_FLOOR -> {'PASS' if h_floor else 'FAIL'}")
    P(f"   sign of dMaxDD_M across the 5 offsets: " +
      "  ".join(f"{int(r.offset)}:{r.dMaxDD_M*100:+.2f}" for r in fl.itertuples()) +
      f"   (all positive = {bool((fl.dMaxDD_M > 0).all())})")

    # ------------------------------------------------------------------ H_4b
    P(f"\n{'-'*110}\nH_4b - does 4b separate the arm from its own gross-matched control?\n{'-'*110}")
    P(f"   at the pre-registered cell: arm 4b={bool(cell.arm_4b)} (fails {cell.arm_fail_4b}), "
      f"CONTROL-M 4b={bool(cell.ctlM_4b)} (fails {cell.ctlM_fail_4b})")
    h_4b = bool(cell.arm_4b and cell.ctlM_4b)
    P(f"   H_4b (both pass, so 4b does not see the clause) -> {'PASS' if h_4b else 'FAIL'}")
    P(f"   over all 40 points at t+1: arm 4b {int(at1.arm_4b.sum())}, ctlM 4b "
      f"{int(at1.ctlM_4b.sum())}, arm 4b AND ctlM fails 4b "
      f"{int((at1.arm_4b & ~at1.ctlM_4b).sum())}  <- the only cells where 4b sees the clause")
    P(f"   KEEP paths over all 40 points at t+1: 4a arm {int(at1.arm_4a.sum())}, "
      f"4b arm {int(at1.arm_4b.sum())}, BOTH {int((at1.arm_4a & at1.arm_4b).sum())}; "
      f"OOS window 4a {int(at1.arm_4a_OOS.sum())}, 4b {int(at1.arm_4b_OOS.sum())}")
    P(f"   at t+2 (1-day delayed execution, reported): arm 4b "
      f"{int(grid[grid.lag == 2].arm_4b.sum())} of 40, dMaxDD_M at the pre-reg cell "
      f"{float(grid[(grid.lag == 2) & (grid.cost == COST0) & (grid.dial == DIAL0)].dMaxDD_M.iloc[0])*100:+.2f} pp")

    # ------------------------------------------------------------------ H_WF (rule 8)
    P(f"\n{'-'*110}\nRULE 8 WALK-FORWARD - dial chosen on IS alone, OOS read once\n{'-'*110}")
    wf = []
    for lag in LAGS:
        for cost in COSTS:
            sub = grid[(grid.lag == lag) & (grid.cost == cost)].sort_values("dial")
            for sel_name, col, best in [("IS dMaxDD_M (the headline statistic)", "IS_dMaxDD_M", "max"),
                                        ("IS Sharpe (the record's usual selector)", "IS_Sharpe", "max")]:
                pick = sub.loc[sub[col].idxmax()] if best == "max" else sub.loc[sub[col].idxmin()]
                wf.append(dict(lag=lag, cost=cost, selector=sel_name, dial_star=pick.dial,
                               IS_stat=pick[col], OOS_dMaxDD_M=pick.OOS_dMaxDD_M,
                               OOS_dSharpe_M=pick.OOS_dSharpe_M, OOS_CAGR=pick.OOS_CAGR,
                               OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               OOS_4b=pick.arm_4b_OOS, OOS_4a=pick.arm_4a_OOS,
                               ctlM_OOS_4b=pick.ctlM_4b_OOS))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("   " + wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    head = wfd[(wfd.lag == 1) & (wfd.cost == COST0) &
               (wfd.selector == "IS dMaxDD_M (the headline statistic)")].iloc[0]
    h_wf = bool(head.OOS_dMaxDD_M > 0)
    P(f"\n   HEADLINE rule-8 read (t+1, 10 bps, dial picked on IS by IS dMaxDD_M):")
    P(f"     dial* = {head.dial_star:.2f} (IS dMaxDD_M {head.IS_stat*100:+.2f} pp)  ->  "
      f"OOS dMaxDD_M {head.OOS_dMaxDD_M*100:+.2f} pp, OOS dSharpe_M {head.OOS_dSharpe_M:+.3f}")
    P(f"   H_WF (OOS dMaxDD_M > 0) -> {'PASS' if h_wf else 'FAIL'}")
    P(f"   share of the 20 (lag x cost x selector)/2 walk-forward picks with OOS dMaxDD_M > 0: "
      f"{int((wfd.OOS_dMaxDD_M > 0).sum())} of {len(wfd)}")

    # OOS levels against the two mandated comparands
    rg_lv, tn_lv, _ = fast_run(px, Wlive, mask, LAG0)
    live10 = net(rg_lv, tn_lv, COST0).loc[start:]
    ml, ms = metrics(live10.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
    pk = grid[(grid.lag == 1) & (grid.cost == COST0) & (grid.dial == head.dial_star)].iloc[0]
    P(f"\n   OOS (2017-01-01..) levels of the rule-8 book vs the two mandated comparands:")
    P(f"     rule-8 arm (dial {head.dial_star:.2f})  CAGR {pk.OOS_CAGR:7.2%}  Sharpe "
      f"{pk.OOS_Sharpe:6.3f}  MaxDD {pk.OOS_MaxDD:7.2%}")
    P(f"     its own CONTROL-M          CAGR {pk.ctlM_OOS_CAGR:7.2%}  Sharpe "
      f"{pk.ctlM_OOS_Sharpe:6.3f}  MaxDD {pk.ctlM_OOS_MaxDD:7.2%}")
    P(f"     RULES v2 baseline (live)   CAGR {ml['CAGR']:7.2%}  Sharpe {ml['Sharpe']:6.3f}  "
      f"MaxDD {ml['MaxDD']:7.2%}")
    P(f"     SPY buy-and-hold           CAGR {ms['CAGR']:7.2%}  Sharpe {ms['Sharpe']:6.3f}  "
      f"MaxDD {ms['MaxDD']:7.2%}")
    mf_a = metrics(net(*fast_run(px, Wb.mul(vol_gate(px, head.dial_star).reindex(px.index)
                                            .fillna(False).astype(float), axis=0),
                                 mask, LAG0)[:2], COST0).loc[start:])
    P(f"     FULL sample, same book:    CAGR {mf_a['CAGR']:7.2%}  Sharpe {mf_a['Sharpe']:6.3f}  "
      f"MaxDD {mf_a['MaxDD']:7.2%}   halves {pk.H1:.3f} / {pk.H2:.3f}")
    mfl, mfs = metrics(live10), metrics(spy)
    P(f"     FULL sample, RULES v2:     CAGR {mfl['CAGR']:7.2%}  Sharpe {mfl['Sharpe']:6.3f}  "
      f"MaxDD {mfl['MaxDD']:7.2%}")
    P(f"     FULL sample, SPY:          CAGR {mfs['CAGR']:7.2%}  Sharpe {mfs['Sharpe']:6.3f}  "
      f"MaxDD {mfs['MaxDD']:7.2%}")
    P(f"     KEEP paths for that book: 4a {bool(pk.arm_4a)}, 4b {bool(pk.arm_4b)} "
      f"(fails {pk.arm_fail_4b}); its CONTROL-M 4b {bool(pk.ctlM_4b)}")

    # ------------------------------------------------------------------ verdict
    P(f"\n{'='*110}\nVERDICT\n{'='*110}")
    H = dict(H_REPRO=repro_ok, H_SIGN=h_sign, H_DIAL=h_dial, H_COST=h_cost,
             H_FLOOR=h_floor, H_WF=h_wf, H_4b=h_4b)
    for k, v in H.items():
        P(f"   {k:<10} {'PASS' if v else 'FAIL'}")
    npass = sum(H.values())
    P(f"   {npass} of {len(H)} pre-registered hypotheses pass.")
    keep = bool(h_wf and h_floor and h_dial and cell.arm_4b and not cell.ctlM_4b)
    P(f"   KEEP requires: the DD effect survives rule 8 AND clears its own convention floor AND is")
    P(f"   contiguous in the dial AND the arm passes 4b where its gross-matched control does not.")
    P(f"   -> {'KEEP-candidate' if keep else 'NOT a KEEP'}")
    pd.DataFrame([H]).to_csv(f"{OUT}.hypotheses.csv", index=False)

    P(f"\n   elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
