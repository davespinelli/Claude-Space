#!/usr/bin/env python3
"""
IDEA 670 -- is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone                  (lane C)
==========================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 668's entire GROSS 4b footprint is 16 points at g >= 0.95 with 0 at g=0.75 and 0 at
  g <= 0.60, while Sharpe is flat across the whole ladder to three decimals (worst flip
  0.0018/0.0030 OOS Sharpe).  Test 657's question as ONE experiment: hold gross MATCHED
  across every arm and re-run 4b, reporting how many of the record's committed 4b passes
  survive when exposure cannot buy the CAGR floor.  Max 2 params (gross grid, panel).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)  : GROSS g (the ladder rung) and PANEL.
  NOT TUNED  : cost 10 bps (PROTOCOL 2); cadence W (RULES v2) except on the one arm where
               cadence IS the arm's definition (BAND03_M, a fixed companion, not a swept
               dial); band 0.03 (RULES v2) and 0.08 (idea 664's committed IS pick); n in
               {5,10,20} and vol cap 0.60/OFF -- all are the record's OWN committed arm
               definitions, restated, never chosen by looking at an outcome; warm-up 260
               rows; IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL 8).
               The ARM LIST is a census of the record's committed 4b-passing families, not
               a search: every arm below is named in a committed artefact (cited inline).

THE DESIGN
----------
  Ten ARMS, each a book whose weights are exactly g x (its g=1.00 weights) -- gate G5 asserts
  that scaling identity to 0.0, so on this grid "gross" is pure exposure and nothing else:

    BAND03      RULES v2 live band book, band 0.03, W            baseline.rules_v2_weights
    BAND08      band 0.08, W                                      idea 664's committed IS pick
    BAND03_M    band 0.03, MONTHLY                                668's CADENCE dial companion
    CAND20_VS   top-20 composite rank, vol scaler ON, cap 0.60    668's N dial (14 of its 4b)
    CAND20      top-20 composite rank, NO vol scaler, cap 0.60    the 2026-09-04 KEEP 4b book
    CAND10      top-10, no vol scaler, cap 0.60                   width companion
    CAND05      top-5,  no vol scaler, cap 0.60                   RULES v1's width
    CAND20_NOCAP top-20, no vol scaler, cap OFF                   668's VOLCAP dial (2 of its 4b)
    EWELIG      equal-weight EVERY eligible name (>200d, vol20<0.60)  2026-09-03 memo Finding 2
    SPYBH       g x SPY, weekly                                   the ZERO-SIGNAL exposure control

  SPYBH is the load-bearing control: it carries no signal at all, so whatever part of the 4b
  verdict it can move by turning g is, by construction, exposure and not edge.

  Every arm is run at EVERY rung of the gross ladder {0.20 .. 1.00} on both panels and the
  4b verdict is DECOMPOSED INTO ITS FIVE LEGS, reported separately at every point:
     L1 H1 Sharpe > SPY H1      L2 H2 Sharpe > SPY H2      L3 OOS Sharpe > SPY OOS
     L4 |MaxDD| <= 0.60 |MaxDD_SPY|                        L5 CAGR >= 0.70 CAGR_SPY
  The queue's claim is a claim about WHICH LEG MOVES WITH g.  Legs, not the conjunction, are
  the only way to answer it, and the conjunction is reported too (pass4b), with 4a beside it.

  MATCHED-GROSS SURVIVAL (the queue's count): for every (panel, arm) that passes 4b at ANY
  rung, does it still pass when g is held at the live constant 0.75, and at every rung?

  CASH-RATE COUNTERFACTUAL: the engine pays 0% on the de-grossed sleeve, so at g<1 the CAGR
  floor is mechanically harder.  For every failing point the run publishes the flat cash rate
  that would flip L5, = (0.70 CAGR_SPY - CAGR) / mean cash share.  This is a DIAGNOSTIC, not
  a tuned parameter and not a claim: open idea 642 PARKs the real T-bill path for lack of data.

PANELS (PROTOCOL 9 survivorship)
--------------------------------
  U56  research/universe.json          B136  research/universe_broad.json
  B136 is TODAY'S constituents; every B136 LEVEL below is biased upward.  The claims this run
  makes are about which 4b LEG moves with g inside a panel, which survivorship biases far less
  than it biases a level, but no B136 level here is a tradeable estimate.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
--------------------------------------------------------------------
  G1  fast_backtest == engine.backtest @10 bps                       bar 1e-12
  G2  band_book(0.03,0.75) == baseline.rules_v2_weights              bar 0.0 (exact)
  G3  idea 668's COMMITTED GROSS-dial rows reproduce (both panels, 5 rungs, 6 metrics)  5e-4
  G4  the gross ladder contains the live constant 0.75 and the full-exposure rung 1.00
  G5  weights(g) == g * weights(1.00) exactly, every arm, both panels    bar 0.0
  G6  SPYBH at g=1.00 tracks SPY buy-and-hold                         bar 0.01 Sharpe

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated at EVERY grid point and all points are reported.  Rule 8 is
  run with TWO pre-registered choosers (IS-Sharpe argmax, and the 2026-09-03 memo's own
  "smallest G that clears the 4b DD cap and CAGR floor" rule read on IS only).  Nothing is
  promoted on a leg-decomposition result.  A documented KILL is the expected outcome.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                     # PROTOCOL 2
FREQ0 = "W"                     # RULES v2 cadence
BAND0, BAND1 = 0.03, 0.08       # RULES v2 clause 2 / idea 664's committed IS pick
GROSS0 = 0.75                   # RULES v2 clause 3 -- the "matched gross" the queue asks about
MAXVOL = 0.60                   # RULES v1/v2 eligibility cap
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]      # idea 668's own ladder, verbatim

# idea 668's COMMITTED GROSS-dial grid rows
# (research/backtests/2026-09-10_is-the-PICK-FLIP-rate-of-0.50-a-property-of-the-BAND-LADDER-
#  or-of-every-dial_cloud.grid.csv, dial == GROSS; the band book at band=0.03)
IDEA668 = {
    "U56": {
        1.00: dict(CAGR=0.115239, Sharpe=1.199628, MaxDD=-0.159110, H1=1.235383, H2=1.171087,
                   OOS_Sharpe=1.273958),
        0.95: dict(CAGR=0.109406, Sharpe=1.199676, MaxDD=-0.151463, H1=1.235290, H2=1.171249,
                   OOS_Sharpe=1.274112),
        0.85: dict(CAGR=0.097756, Sharpe=1.199754, MaxDD=-0.136071, H1=1.235084, H2=1.171555,
                   OOS_Sharpe=1.274402),
        0.75: dict(CAGR=0.086132, Sharpe=1.199807, MaxDD=-0.120549, H1=1.234855, H2=1.171836,
                   OOS_Sharpe=1.274666),
        0.20: dict(CAGR=0.022761, Sharpe=1.199725, MaxDD=-0.032858, H1=1.233246, H2=1.172995,
                   OOS_Sharpe=1.275714),
    },
    "B136": {
        1.00: dict(CAGR=0.107246, Sharpe=1.105693, MaxDD=-0.161577, H1=1.230097, H2=0.983302,
                   OOS_Sharpe=1.117412),
        0.95: dict(CAGR=0.101854, Sharpe=1.105724, MaxDD=-0.153809, H1=1.229903, H2=0.983530,
                   OOS_Sharpe=1.117643),
        0.85: dict(CAGR=0.091075, Sharpe=1.105769, MaxDD=-0.138174, H1=1.229497, H2=0.983969,
                   OOS_Sharpe=1.118088),
        0.75: dict(CAGR=0.080303, Sharpe=1.105790, MaxDD=-0.122408, H1=1.229068, H2=0.984385,
                   OOS_Sharpe=1.118508),
        0.20: dict(CAGR=0.021302, Sharpe=1.105535, MaxDD=-0.033357, H1=1.226348, H2=0.986308,
                   OOS_Sharpe=1.120433),
    },
}
# idea 668's committed SPY OOS references, same file
IDEA668_SPY = {"U56": dict(OOS_Sharpe=0.872123, OOS_CAGR=0.152372, OOS_MaxDD=-0.337173),
               "B136": dict(OOS_Sharpe=0.882024, OOS_CAGR=0.154504, OOS_MaxDD=-0.337160)}

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 1.  ENGINE  (vectorised equivalent of engine.backtest, asserted against it in G1)
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ0, cost=COST, want_exposure=False):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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
    gross_r = (held * rets).sum(axis=1)
    r = pd.Series(gross_r - turn * cost / 1e4, index=idx)
    if want_exposure:
        return r, pd.Series(held.sum(axis=1), index=idx), pd.Series(turn, index=idx)
    return r


def M0(r):
    vol = r.std() * np.sqrt(252)
    return (r.mean() * 252) / vol if vol else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    h = len(r) // 2
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


# ================================================================================================
# 2.  THE TEN ARMS  (each returns weights at gross g; G5 asserts weights(g) == g*weights(1.0))
# ================================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, sc, above, vol20, n, gross, max_vol):
    elig = sc.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(gross / k, axis=0)).fillna(0.0)


def elig_ew_book(px, above, vol20, gross, max_vol):
    """2026-09-03 memo Finding 2: equal-weight EVERY eligible name at gross g."""
    sel = (above & (vol20 < max_vol) & px.notna()).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(gross / k, axis=0)).fillna(0.0)


def spy_book(px, gross):
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    w["SPY"] = float(gross)
    return w.where(px.notna().reindex(columns=w.columns).fillna(False), 0.0)


ARMS = ["BAND03", "BAND08", "BAND03_M", "CAND20_VS", "CAND20", "CAND10", "CAND05",
        "CAND20_NOCAP", "EWELIG", "SPYBH"]
ARM_FREQ = {a: ("M" if a == "BAND03_M" else FREQ0) for a in ARMS}
ARM_SRC = {
    "BAND03": "RULES v2 live (baseline.rules_v2_weights)",
    "BAND08": "idea 664 committed IS pick on the BAND dial",
    "BAND03_M": "idea 668 CADENCE dial companion",
    "CAND20_VS": "idea 668 N dial (vol scaler ON, as baseline.score)",
    "CAND20": "2026-09-04 KEEP 4b: top-20 equal weight, NO vol scaler",
    "CAND10": "width companion of the KEEP 4b book",
    "CAND05": "RULES v1 book width",
    "CAND20_NOCAP": "idea 668 VOLCAP dial, cap OFF",
    "EWELIG": "2026-09-03 memo Finding 2 (equal-weight all eligible)",
    "SPYBH": "ZERO-SIGNAL exposure control",
}


def arm_weights(px, pre, arm, g):
    sc_v, sc_n, above, vol20 = pre
    if arm == "BAND03":
        return band_book(px, BAND0, g)
    if arm == "BAND08":
        return band_book(px, BAND1, g)
    if arm == "BAND03_M":
        return band_book(px, BAND0, g)
    if arm == "CAND20_VS":
        return ranked_book(px, sc_v, above, vol20, 20, g, MAXVOL)
    if arm == "CAND20":
        return ranked_book(px, sc_n, above, vol20, 20, g, MAXVOL)
    if arm == "CAND10":
        return ranked_book(px, sc_n, above, vol20, 10, g, MAXVOL)
    if arm == "CAND05":
        return ranked_book(px, sc_n, above, vol20, 5, g, MAXVOL)
    if arm == "CAND20_NOCAP":
        return ranked_book(px, sc_n, above, vol20, 20, g, 9.99)
    if arm == "EWELIG":
        return elig_ew_book(px, above, vol20, g, MAXVOL)
    if arm == "SPYBH":
        return spy_book(px, g)
    raise KeyError(arm)


def prep(px):
    sc_v, above, vol20 = score(px, vol_scale=True)
    sc_n, _, _ = score(px, vol_scale=False)
    return sc_v, sc_n, above, vol20


# ================================================================================================
# 3.  PROTOCOL 4a / 4b, decomposed into legs
# ================================================================================================
def legs(r, base, spy):
    m, mb, ms = M(r), M(base), M(spy)
    oos_s, oos_b = M0(r.loc[OOS_START:]), M0(spy.loc[OOS_START:])
    L = dict(L1_H1=bool(m["H1"] > ms["H1"]), L2_H2=bool(m["H2"] > ms["H2"]),
             L3_OOS=bool(oos_s > oos_b),
             L4_DDcap=bool(abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"])),
             L5_CAGRfloor=bool(m["CAGR"] >= 0.70 * ms["CAGR"]))
    p4b = all(L.values())
    p4a = bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])
    return L, p4a, p4b, m, ms


# ================================================================================================
# 4.  GATES
# ================================================================================================
def gates(panels, pres):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run and printed before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights   : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= (g2 == 0.0)

    slow = backtest(px, w, cost_bps=COST, freq=FREQ0)["returns"]
    fast = fast_backtest(px, w, FREQ0, COST)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps            : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= (g1 < 1e-12)

    P("  G3 idea 668's COMMITTED GROSS-dial rows (band 0.03, W, 10 bps), bar 5e-4.")
    P("     668 itself reported the tape moves between runs, so the gate is tried on today's")
    P("     tape AND on truncations and the reproducing vintage is NAMED (bears on idea 517).")
    g3rows = []
    for pn, pxp in panels.items():
        best, best_tag = None, None
        for end in (None, "2026-09-10", "2026-09-09", "2026-09-08", "2026-09-04"):
            q = pxp if end is None else pxp.loc[:end]
            if len(q) < WARM + 500:
                continue
            st = q.index[WARM]
            spy = q["SPY"].pct_change().fillna(0).loc[st:]
            worst, det = 0.0, {}
            for g, e in IDEA668[pn].items():
                r = fast_backtest(q, band_book(q, BAND0, g), FREQ0, COST).loc[st:]
                m = M(r)
                d = {k: abs(m[k] - e[k]) for k in ("CAGR", "Sharpe", "MaxDD", "H1", "H2")}
                d["OOS_Sharpe"] = abs(M0(r.loc[OOS_START:]) - e["OOS_Sharpe"])
                worst = max(worst, max(d.values()))
                det[g] = d
            ds = abs(M0(spy.loc[OOS_START:]) - IDEA668_SPY[pn]["OOS_Sharpe"])
            worst = max(worst, ds)
            tag = "today" if end is None else f"<= {end}"
            P(f"     {pn:<5} {tag:<13} last {q.index[-1].date()}  max|d| over 5 rungs x 6 "
              f"metrics + SPY = {worst:.3e}")
            g3rows.append(dict(panel=pn, vintage=tag, last=str(q.index[-1].date()),
                               max_abs_dev=worst, spy_oos_dev=ds))
            if best is None or worst < best:
                best, best_tag = worst, tag
        P(f"     {pn:<5} best vintage {best_tag}  max|d| {best:.3e}  "
          f"{'PASS' if best < 5e-4 else 'FAIL'}")
        ok &= best < 5e-4
    dump(pd.DataFrame(g3rows), "gate3")

    P(f"  G4 ladder contains live 0.75 and full 1.00              : "
      f"{'PASS' if (GROSS0 in GROSSES and 1.00 in GROSSES) else 'FAIL'}")
    ok &= (GROSS0 in GROSSES and 1.00 in GROSSES)

    worst5 = 0.0
    for pn, pxp in panels.items():
        for arm in ARMS:
            w1 = arm_weights(pxp, pres[pn], arm, 1.00).values
            for g in (0.20, 0.75):
                wg = arm_weights(pxp, pres[pn], arm, g).values
                worst5 = max(worst5, float(np.nanmax(np.abs(wg - g * w1))))
    P(f"  G5 weights(g) == g*weights(1.00), 10 arms x 2 panels    : {worst5:.3e}  "
      f"{'PASS' if worst5 == 0.0 else 'FAIL'}  (pre-registered bar: exact 0.0)")
    P("     CORRECTION, stated not hidden: the exact-0.0 bar was MIS-SET BY THIS RUN.  The two")
    P("     sides divide by the name count in a different order (g/k vs g*(1/k)), so they differ")
    P("     in the last bit of a double and can never be bit-identical.  Re-read at the SAME")
    P("     float bar G1 uses for the same reason (1e-12):")
    P(f"     G5' weights(g) == g*weights(1.00) at bar 1e-12         : {worst5:.3e}  "
      f"{'PASS' if worst5 < 1e-12 else 'FAIL'}")
    ok &= (worst5 < 1e-12)

    st = px.index[WARM]
    rs = fast_backtest(px, spy_book(px, 1.00), FREQ0, COST).loc[st:]
    spy = px["SPY"].pct_change().fillna(0).loc[st:]
    g6 = abs(M0(rs) - M0(spy))
    P(f"  G6 SPYBH(g=1.00) tracks SPY buy-and-hold (Sharpe)       : {g6:.3e}  "
      f"{'PASS' if g6 < 0.01 else 'FAIL'}")
    ok &= (g6 < 0.01)

    P(f"  GATES: {'ALL PASS' if ok else 'AT LEAST ONE FAIL -- reported, not hidden'}")
    P()
    return ok


# ================================================================================================
# 5.  THE GRID
# ================================================================================================
def run_grid(panels, pres):
    rows = []
    for pn, px in panels.items():
        st = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[st:]
        base = fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ0, COST).loc[st:]
        ms = M(spy)
        oos_spy = M(spy.loc[OOS_START:])
        for arm in ARMS:
            for g in GROSSES:
                w = arm_weights(px, pres[pn], arm, g)
                r, expo, turn = fast_backtest(px, w, ARM_FREQ[arm], COST, want_exposure=True)
                r, expo = r.loc[st:], expo.loc[st:]
                L, p4a, p4b, m, _ = legs(r, base, spy)
                cash = float(1.0 - expo.mean())
                need = (0.70 * ms["CAGR"] - m["CAGR"]) / cash if cash > 1e-9 else np.nan
                mo = M(r.loc[OOS_START:])
                mi = M(r.loc[:IS_END])
                rows.append(dict(
                    panel=pn, arm=arm, gross=g, freq=ARM_FREQ[arm],
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"], SPY_MaxDD=ms["MaxDD"],
                    SPY_H1=ms["H1"], SPY_H2=ms["H2"], SPY_OOS_Sharpe=oos_spy["Sharpe"],
                    SPY_OOS_CAGR=oos_spy["CAGR"], SPY_OOS_MaxDD=oos_spy["MaxDD"],
                    mean_exposure=float(expo.mean()), cash_share=cash,
                    turnover_yr=float(turn.loc[st:].sum() / (len(r) / 252)),
                    cash_rate_to_flip_L5=need, **L, pass4a=p4a, pass4b=p4b))
    return pd.DataFrame(rows)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    k = np.isfinite(a) & np.isfinite(b)
    if k.sum() < 3:
        return np.nan
    ra = pd.Series(a[k]).rank().values
    rb = pd.Series(b[k]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# ================================================================================================
# 6.  RULE 8 -- WALK-FORWARD, TWO PRE-REGISTERED CHOOSERS
# ================================================================================================
def walkforward(grid):
    """Choose g on 2009-2016 only; evaluate 2017-2026 untouched (PROTOCOL 8).
       CH_SHARPE : argmax IS Sharpe, ties to the SMALLEST g.
       CH_MEMO   : the 2026-09-03 memo's own live rule -- the SMALLEST g whose IS MaxDD is
                   within 60% of SPY's IS MaxDD and IS CAGR >= 70% of SPY's IS CAGR; if none
                   qualifies, keep 0.75 (the memo's stated fallback).  Never looks past IS_END.
    """
    rows = []
    for (pn, arm), d in grid.groupby(["panel", "arm"]):
        d = d.sort_values("gross")
        is_spy_c = d["IS_SPY_CAGR"].iloc[0]
        is_spy_d = d["IS_SPY_MaxDD"].iloc[0]
        for chooser in ("CH_SHARPE", "CH_MEMO"):
            if chooser == "CH_SHARPE":
                pick = float(d.sort_values(["IS_Sharpe", "gross"],
                                           ascending=[False, True])["gross"].iloc[0])
            else:
                q = d[(d["IS_MaxDD"].abs() <= 0.60 * abs(is_spy_d))
                      & (d["IS_CAGR"] >= 0.70 * is_spy_c)]
                pick = float(q["gross"].min()) if len(q) else GROSS0
            row = d[d["gross"] == pick].iloc[0]
            rows.append(dict(panel=pn, arm=arm, chooser=chooser, pick_gross=pick,
                             OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                             OOS_MaxDD=row["OOS_MaxDD"],
                             SPY_OOS_CAGR=row["SPY_OOS_CAGR"],
                             SPY_OOS_Sharpe=row["SPY_OOS_Sharpe"],
                             SPY_OOS_MaxDD=row["SPY_OOS_MaxDD"],
                             BASE_OOS_CAGR=row["BASE_OOS_CAGR"],
                             BASE_OOS_Sharpe=row["BASE_OOS_Sharpe"],
                             BASE_OOS_MaxDD=row["BASE_OOS_MaxDD"],
                             beat_SPY=bool(row["OOS_Sharpe"] > row["SPY_OOS_Sharpe"]),
                             beat_LIVE=bool(row["OOS_Sharpe"] > row["BASE_OOS_Sharpe"]),
                             pass4a=bool(row["pass4a"]), pass4b=bool(row["pass4b"]),
                             best_OOS_on_ladder=float(d["OOS_Sharpe"].max()),
                             worst_OOS_on_ladder=float(d["OOS_Sharpe"].min())))
    return pd.DataFrame(rows)


# ================================================================================================
def main():
    P("#" * 100)
    P("# IDEA 670 -- is-the-GROSS-dial-s-4b-FOOTPRINT-the-CAGR-FLOOR-alone   (lane C, "
      f"{pd.Timestamp.today().date()})")
    P("#" * 100)
    P(__doc__.split("THE QUEUE'S QUESTION")[1].split("PRE-REGISTERED GATES")[0].rstrip())
    P()

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for pn, px in panels.items():
        P(f"  panel {pn:<5} {px.shape[1]:>4} columns  {px.index[0].date()} .. "
          f"{px.index[-1].date()}  ({len(px)} rows)")
    pres = {pn: prep(px) for pn, px in panels.items()}
    P()

    gates_ok = gates(panels, pres)

    P("=" * 100)
    P("(B) THE GRID -- 10 arms x 8 gross rungs x 2 panels = 160 points, ALL REPORTED")
    P("=" * 100)
    grid = run_grid(panels, pres)

    # IS SPY references and the live-book OOS reference, joined for the walk-forward
    for pn, px in panels.items():
        st = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[st:]
        base = fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ0, COST).loc[st:]
        mis = M(spy.loc[:IS_END])
        mb = M(base.loc[OOS_START:])
        k = grid["panel"] == pn
        grid.loc[k, "IS_SPY_CAGR"] = mis["CAGR"]
        grid.loc[k, "IS_SPY_MaxDD"] = mis["MaxDD"]
        grid.loc[k, "IS_SPY_Sharpe"] = mis["Sharpe"]
        grid.loc[k, "BASE_OOS_CAGR"] = mb["CAGR"]
        grid.loc[k, "BASE_OOS_Sharpe"] = mb["Sharpe"]
        grid.loc[k, "BASE_OOS_MaxDD"] = mb["MaxDD"]
    dump(grid, "grid")

    P()
    P("  FULL GRID (CAGR / Sharpe / MaxDD / 4b legs).  L1 H1>SPY  L2 H2>SPY  L3 OOS>SPY")
    P("  L4 |DD|<=60%|SPY DD|  L5 CAGR>=70% SPY CAGR.")
    for pn in panels:
        P()
        P(f"  --- panel {pn}  (SPY: CAGR {grid[grid.panel==pn].SPY_CAGR.iloc[0]:.4%}  "
          f"Sharpe {grid[grid.panel==pn].SPY_Sharpe.iloc[0]:.4f}  "
          f"MaxDD {grid[grid.panel==pn].SPY_MaxDD.iloc[0]:.4%}  "
          f"=> floor {0.70*grid[grid.panel==pn].SPY_CAGR.iloc[0]:.4%}  "
          f"cap {0.60*abs(grid[grid.panel==pn].SPY_MaxDD.iloc[0]):.4%}) ---")
        P(f"  {'arm':<13}{'g':>6}{'CAGR':>9}{'Sharpe':>9}{'MaxDD':>9}{'H1':>8}{'H2':>8}"
          f"{'OOSsh':>8}  L1 L2 L3 L4 L5  4a 4b")
        for arm in ARMS:
            for _, r in grid[(grid.panel == pn) & (grid.arm == arm)].sort_values("gross").iterrows():
                f = lambda b: " Y" if b else " ."
                P(f"  {arm:<13}{r.gross:>6.2f}{r.CAGR:>9.2%}{r.Sharpe:>9.4f}{r.MaxDD:>9.2%}"
                  f"{r.H1:>8.3f}{r.H2:>8.3f}{r.OOS_Sharpe:>8.3f}  "
                  f"{f(r.L1_H1)} {f(r.L2_H2)} {f(r.L3_OOS)} {f(r.L4_DDcap)} {f(r.L5_CAGRfloor)}  "
                  f"{f(r.pass4a)} {f(r.pass4b)}")

    # ------------------------------------------------------------------ (C) which leg moves
    P()
    P("=" * 100)
    P("(C) WHICH 4b LEG MOVES WITH GROSS  -- pass share of each leg at each rung, pooled over")
    P("    10 arms x 2 panels (n = 20 per rung)")
    P("=" * 100)
    LEGN = ["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"]
    legtab = grid.groupby("gross")[LEGN + ["pass4a", "pass4b"]].mean().reset_index()
    P(f"  {'g':>6}" + "".join(f"{c:>14}" for c in LEGN) + f"{'4a':>8}{'4b':>8}")
    for _, r in legtab.iterrows():
        P(f"  {r.gross:>6.2f}" + "".join(f"{r[c]:>14.3f}" for c in LEGN)
          + f"{r.pass4a:>8.3f}{r.pass4b:>8.3f}")
    P()
    P("  Spearman(leg pass share, g) over the 8 rungs, and the SPREAD of the share:")
    for c in LEGN + ["pass4b"]:
        rho = spearman(legtab["gross"], legtab[c])
        rs = "CONSTANT (rho undefined)" if not np.isfinite(rho) else f"rho {rho:+.4f}          "
        P(f"    {c:<14} {rs}   share {legtab[c].min():.3f} -> {legtab[c].max():.3f}"
          f"   spread {legtab[c].max()-legtab[c].min():.3f}")
    dump(legtab, "legs")

    # ------------------------------------------------------------------ (D) Sharpe flatness
    P()
    P("=" * 100)
    P("(D) IS THE LADDER FLAT IN SHARPE?  per (panel, arm): max|dSharpe| across the 8 rungs")
    P("=" * 100)
    fl = []
    for (pn, arm), d in grid.groupby(["panel", "arm"]):
        d = d.sort_values("gross")
        fl.append(dict(panel=pn, arm=arm,
                       Sharpe_min=d.Sharpe.min(), Sharpe_max=d.Sharpe.max(),
                       d_Sharpe=d.Sharpe.max() - d.Sharpe.min(),
                       d_OOS_Sharpe=d.OOS_Sharpe.max() - d.OOS_Sharpe.min(),
                       d_CAGR=d.CAGR.max() - d.CAGR.min(),
                       d_MaxDD=abs(d.MaxDD).max() - abs(d.MaxDD).min(),
                       rho_Sharpe_g=spearman(d.gross, d.Sharpe),
                       rho_CAGR_g=spearman(d.gross, d.CAGR),
                       rho_absDD_g=spearman(d.gross, abs(d.MaxDD))))
    fl = pd.DataFrame(fl).sort_values(["panel", "arm"])
    P(f"  {'panel':<6}{'arm':<14}{'dSharpe':>10}{'dOOSsh':>10}{'dCAGR':>10}{'d|DD|':>10}"
      f"{'rho(Sh,g)':>11}{'rho(CAGR,g)':>13}{'rho(|DD|,g)':>13}")
    for _, r in fl.iterrows():
        P(f"  {r.panel:<6}{r.arm:<14}{r.d_Sharpe:>10.4f}{r.d_OOS_Sharpe:>10.4f}"
          f"{r.d_CAGR:>10.2%}{r.d_MaxDD:>10.2%}{r.rho_Sharpe_g:>11.3f}"
          f"{r.rho_CAGR_g:>13.3f}{r.rho_absDD_g:>13.3f}")
    P(f"  MEDIAN  dSharpe {fl.d_Sharpe.median():.4f}   dCAGR {fl.d_CAGR.median():.2%}   "
      f"d|DD| {fl.d_MaxDD.median():.2%}   |  MAX dSharpe {fl.d_Sharpe.max():.4f} "
      f"({fl.loc[fl.d_Sharpe.idxmax(),'panel']}/{fl.loc[fl.d_Sharpe.idxmax(),'arm']})")
    P(f"  rho(CAGR,g) == +1.000 on {int((fl.rho_CAGR_g > 0.999).sum())}/{len(fl)} arms;  "
      f"rho(|DD|,g) == +1.000 on {int((fl.rho_absDD_g > 0.999).sum())}/{len(fl)};  "
      f"|rho(Sharpe,g)| >= 0.9 on {int((fl.rho_Sharpe_g.abs() >= 0.9).sum())}/{len(fl)}")
    dump(fl, "flatness")

    # ------------------------------------------------------------------ (E) matched-gross survival
    P()
    P("=" * 100)
    P("(E) MATCHED-GROSS SURVIVAL -- the queue's count.  For every (panel, arm) that passes 4b")
    P("    at ANY rung: does it still pass at the LIVE matched gross 0.75, and at EVERY rung?")
    P("=" * 100)
    sv = []
    for (pn, arm), d in grid.groupby(["panel", "arm"]):
        d = d.sort_values("gross")
        anyp = bool(d.pass4b.any())
        at75 = bool(d[d.gross == GROSS0].pass4b.iloc[0])
        allp = bool(d.pass4b.all())
        pg = sorted(d[d.pass4b].gross.tolist())
        sv.append(dict(panel=pn, arm=arm, n_pass4b=int(d.pass4b.sum()), any4b=anyp,
                       pass_at_0p75=at75, pass_at_all_g=allp,
                       min_pass_g=(min(pg) if pg else np.nan),
                       max_pass_g=(max(pg) if pg else np.nan),
                       n_pass4a=int(d.pass4a.sum()),
                       passing_grosses=";".join(f"{x:.2f}" for x in pg)))
    sv = pd.DataFrame(sv).sort_values(["panel", "arm"])
    P(f"  {'panel':<6}{'arm':<14}{'#4b/8':>7}{'#4a/8':>7}{'@0.75':>8}{'@all g':>8}"
      f"   passing grosses")
    for _, r in sv.iterrows():
        P(f"  {r.panel:<6}{r.arm:<14}{r.n_pass4b:>7}{r.n_pass4a:>7}"
          f"{('Y' if r.pass_at_0p75 else '.'):>8}{('Y' if r.pass_at_all_g else '.'):>8}"
          f"   {r.passing_grosses or '(none)'}")
    nany = int(sv.any4b.sum())
    P()
    P(f"  ARMS WITH A 4b PASS AT SOME GROSS         : {nany}/{len(sv)}")
    P(f"  ... that survive at the MATCHED live 0.75 : {int(sv.pass_at_0p75.sum())}/{nany}"
      if nany else "  (no arm passes at any gross)")
    P(f"  ... that survive at EVERY rung            : {int(sv.pass_at_all_g.sum())}/{nany}"
      if nany else "")
    P(f"  minimum passing gross over all arms       : "
      f"{np.nanmin(sv.min_pass_g) if nany else float('nan'):.2f}")
    P(f"  TOTAL 4b points {int(grid.pass4b.sum())}/{len(grid)};  "
      f"TOTAL 4a points {int(grid.pass4a.sum())}/{len(grid)};  "
      f"BOTH {int((grid.pass4a & grid.pass4b).sum())}/{len(grid)}")
    dump(sv, "survival")

    # ------------------------------------------------------------------ (F) the zero-signal control
    P()
    P("=" * 100)
    P("(F) THE ZERO-SIGNAL CONTROL -- what can g buy with NO edge at all?  (arm SPYBH)")
    P("=" * 100)
    for pn in panels:
        d = grid[(grid.panel == pn) & (grid.arm == "SPYBH")].sort_values("gross")
        P(f"  {pn}:  " + "  ".join(
            f"g{r.gross:.2f}[{'4b' if r.pass4b else '--'}|L4{'Y' if r.L4_DDcap else '.'}"
            f"L5{'Y' if r.L5_CAGRfloor else '.'}]" for _, r in d.iterrows()))
        q = d[d.L5_CAGRfloor]
        P(f"        smallest g clearing the CAGR FLOOR with no signal : "
          f"{q.gross.min() if len(q) else float('nan'):.2f}")
        q = d[d.L4_DDcap]
        P(f"        largest  g still inside the DD CAP with no signal : "
          f"{q.gross.max() if len(q) else float('nan'):.2f}")
    P()
    P("  THE TWO LEGS DEFINE A GROSS WINDOW.  L4 (DD cap) is satisfied at LOW g, L5 (CAGR floor)")
    P("  at HIGH g, so 4b can only live in the overlap.  Per (panel, arm): the largest g inside")
    P("  the cap, the smallest g clearing the floor, and whether the window is OPEN:")
    win = []
    for (pn, arm), d in grid.groupby(["panel", "arm"]):
        d = d.sort_values("gross")
        c = d[d.L4_DDcap].gross.max() if d.L4_DDcap.any() else np.nan
        f5 = d[d.L5_CAGRfloor].gross.min() if d.L5_CAGRfloor.any() else np.nan
        w = (np.nan if (not np.isfinite(c) or not np.isfinite(f5)) else c - f5)
        win.append(dict(panel=pn, arm=arm, g_max_in_DDcap=c, g_min_over_CAGRfloor=f5,
                        window_width=w, window_open=bool(np.isfinite(w) and w >= 0),
                        n_pass4b=int(d.pass4b.sum())))
    win = pd.DataFrame(win).sort_values(["panel", "arm"])
    P(f"  {'panel':<6}{'arm':<14}{'g<=cap':>9}{'g>=floor':>10}{'width':>9}{'open':>7}{'#4b':>6}")
    for _, r in win.iterrows():
        P(f"  {r.panel:<6}{r.arm:<14}{r.g_max_in_DDcap:>9.2f}{r.g_min_over_CAGRfloor:>10.2f}"
          f"{r.window_width:>9.2f}{('Y' if r.window_open else '.'):>7}{r.n_pass4b:>6}")
    P(f"  window OPEN on {int(win.window_open.sum())}/{len(win)} (panel, arm) cells; "
      f"CLOSED on {int((~win.window_open).sum())} -- including the zero-signal control on BOTH "
      f"panels (width {float(win[win.arm=='SPYBH'].window_width.iloc[0]):+.2f}).")
    P("  The width of that window IS the edge test: a book with no edge has a NEGATIVE width,")
    P("  and every 4b pass on this grid is a book whose window opened.")
    dump(win, "window")

    # ------------------------------------------------------------------ (G) cash-rate counterfactual
    P()
    P("=" * 100)
    P("(G) CASH-RATE COUNTERFACTUAL (DIAGNOSTIC, not a claim -- open idea 642 PARKs the real")
    P("    T-bill path).  The engine pays 0% on the de-grossed sleeve.  For every point that")
    P("    FAILS the CAGR floor, the flat cash rate that would flip L5:")
    P("=" * 100)
    fail5 = grid[~grid.L5_CAGRfloor].copy()
    P(f"  points failing L5: {len(fail5)}/{len(grid)}")
    P(f"  {'g':>6}{'n_fail':>8}{'med cash share':>16}{'med rate to flip':>18}"
      f"{'min':>9}{'max':>9}")
    for g, d in fail5.groupby("gross"):
        P(f"  {g:>6.2f}{len(d):>8}{d.cash_share.median():>16.3f}"
          f"{d.cash_rate_to_flip_L5.median():>18.2%}{d.cash_rate_to_flip_L5.min():>9.2%}"
          f"{d.cash_rate_to_flip_L5.max():>9.2%}")
    plaus = fail5[(fail5.cash_rate_to_flip_L5 > 0) & (fail5.cash_rate_to_flip_L5 <= 0.05)]
    P(f"  L5 failures a <=5%/yr flat cash rate would flip: {len(plaus)}/{len(fail5)}")
    if len(plaus):
        P("    " + ", ".join(f"{r.panel}/{r.arm}@g{r.gross:.2f}({r.cash_rate_to_flip_L5:.2%})"
                             for _, r in plaus.sort_values("cash_rate_to_flip_L5").head(12).iterrows()))

    # ------------------------------------------------------------------ (H) rule 8
    P()
    P("=" * 100)
    P("(H) PROTOCOL RULE 8 -- WALK-FORWARD.  g chosen on 2009-2016 only, evaluated 2017-2026.")
    P("    Two pre-registered choosers, both reported at every (panel, arm).")
    P("=" * 100)
    wf = walkforward(grid)
    dump(wf, "walkforward")
    P(f"  {'panel':<6}{'arm':<14}{'chooser':<11}{'pick g':>8}{'OOS CAGR':>10}{'OOS Sh':>9}"
      f"{'OOS DD':>9}{'SPY Sh':>9}{'LIVE Sh':>9}{'>SPY':>6}{'>LIVE':>7}{'4b':>4}")
    for _, r in wf.sort_values(["panel", "arm", "chooser"]).iterrows():
        P(f"  {r.panel:<6}{r.arm:<14}{r.chooser:<11}{r.pick_gross:>8.2f}{r.OOS_CAGR:>10.2%}"
          f"{r.OOS_Sharpe:>9.3f}{r.OOS_MaxDD:>9.2%}{r.SPY_OOS_Sharpe:>9.3f}"
          f"{r.BASE_OOS_Sharpe:>9.3f}{('Y' if r.beat_SPY else '.'):>6}"
          f"{('Y' if r.beat_LIVE else '.'):>7}{('Y' if r.pass4b else '.'):>4}")
    for ch, d in wf.groupby("chooser"):
        P()
        P(f"  {ch}: picks g=1.00 on {int((d.pick_gross==1.0).sum())}/{len(d)}, "
          f"g<=0.75 on {int((d.pick_gross<=0.75).sum())}/{len(d)};  "
          f"beat SPY OOS {int(d.beat_SPY.sum())}/{len(d)};  "
          f"beat LIVE book OOS {int(d.beat_LIVE.sum())}/{len(d)};  "
          f"4b {int(d.pass4b.sum())}/{len(d)};  4a {int(d.pass4a.sum())}/{len(d)}")
        P(f"    mean OOS CAGR {d.OOS_CAGR.mean():.2%} vs SPY {d.SPY_OOS_CAGR.iloc[0]:.2%} / "
          f"LIVE {d.BASE_OOS_CAGR.iloc[0]:.2%};  mean OOS Sharpe {d.OOS_Sharpe.mean():.3f} "
          f"vs SPY {d.SPY_OOS_Sharpe.iloc[0]:.3f} / LIVE {d.BASE_OOS_Sharpe.iloc[0]:.3f};  "
          f"mean OOS MaxDD {d.OOS_MaxDD.mean():.2%} vs SPY {d.SPY_OOS_MaxDD.iloc[0]:.2%} / "
          f"LIVE {d.BASE_OOS_MaxDD.iloc[0]:.2%}")
    a, b = wf[wf.chooser == "CH_SHARPE"].set_index(["panel", "arm"]), \
        wf[wf.chooser == "CH_MEMO"].set_index(["panel", "arm"])
    agree = (a.pick_gross == b.reindex(a.index).pick_gross).mean()
    P()
    P(f"  the two choosers agree on the pick in {agree:.1%} of the {len(a)} (panel, arm) cells; "
      f"median |d OOS Sharpe| between them "
      f"{float((a.OOS_Sharpe - b.reindex(a.index).OOS_Sharpe).abs().median()):.4f}")

    # ------------------------------------------------------------------ verdict
    P()
    P("=" * 100)
    P("(I) VERDICT")
    P("=" * 100)
    l5 = legtab.L5_CAGRfloor
    l4 = legtab.L4_DDcap
    sh_legs = legtab[["L1_H1", "L2_H2", "L3_OOS"]]
    P(f"  CAGR-floor leg L5 share {l5.min():.3f} -> {l5.max():.3f} (rho vs g "
      f"{spearman(legtab.gross, l5):+.3f});  DD-cap leg L4 {l4.max():.3f} -> {l4.min():.3f} "
      f"(rho {spearman(legtab.gross, l4):+.3f})")
    P(f"  Sharpe legs L1/L2/L3 spread across the whole ladder: "
      + ", ".join(f"{c} {sh_legs[c].max()-sh_legs[c].min():.3f}" for c in sh_legs.columns))
    P(f"  4b points {int(grid.pass4b.sum())}/{len(grid)}; 4a {int(grid.pass4a.sum())}/{len(grid)}; "
      f"BOTH {int((grid.pass4a & grid.pass4b).sum())}/{len(grid)}.  "
      f"Nothing is promoted on a leg-decomposition result.")
    P("  VERDICT: see the .result.md memo written beside this script.")
    P(f"  GATES: {'ALL PASS' if gates_ok else 'SEE ABOVE -- a gate failed and is reported'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
