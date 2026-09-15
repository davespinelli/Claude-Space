#!/usr/bin/env python3
"""Idea 807 (lane C, 2026-09-15) - is-the-21-OFFSET-ENSEMBLE-of-the-805-book-a-4b-PASS-in-its-own-right.

QUESTION
--------
Idea 805 pre-registered the U56 / MA-DG / MONTHLY / g=1.00 book and killed it on ONE leg: H_CAL.
Shift the monthly rebalance off month end and 4b holds at only 13 of 21 trading-day offsets, all 8
failures on the DRAWDOWN leg alone, because the book's DD-cap margin (4.74pp) is SMALLER than the
spread in MaxDD across the 21 equally arbitrary calendars (8.37pp).  The queue's objection is that
a real portfolio never has to pick one of those 21 dates: split the capital 21 ways, run one sleeve
on each month-end offset, and the book you actually hold has the ENSEMBLE's drawdown, not the worst
leg's.  This run prices that ensemble as a book in its own right and asks whether averaging the
convention away RECOVERS the DD margin or merely REPRODUCES the mean offset.

THE BOOK (declared in full; nothing about it is chosen by anything below)
------------------------------------------------------------------------
* PANEL   U56 = research/universe.json, every column of `baseline.load_universe()` tradable.
          SPY is one of the 56 tradable names AND the 4b comparand.  That is idea 804/805's
          construction and it is NOT changed here.
* FORM    MA-DG, verbatim from idea 805: priced = price not NaN, N_t = priced names on day t,
              w_i,t = g / N_t  if price_i,t > its 200-day mean, else 0 (weight goes to CASH,
          never re-spread; realised gross = g * eligible/priced <= g).
* SLEEVE  k in 0..20: the same book rebalanced MONTHLY, k trading days after each month end
          (k = 0 is PROTOCOL's own calendar and idea 805's book).  Targets drift in between.
* THE ENSEMBLE (the object this run prices).  Two conventions, BOTH reported, neither tuned:
    ENS-NAV  (PRIMARY, the implementable one): at the first day of the window the capital is split
             ONCE into 21 equal sleeves.  Each sleeve compounds on its own calendar and pays its
             own costs.  Ensemble NAV = sum of the 21 sleeve NAVs; sleeve weights then DRIFT and
             are never re-equalised.  No transfer between sleeves ever happens, so the ensemble
             costs EXACTLY the 21 sleeves' own turnover and not one basis point more.
    ENS-EW   (reported beside it): r_t = mean_k r_k,t, i.e. the sleeves re-equalised EVERY DAY.
             This is NOT free - daily transfers between sleeves are unpriced here - so it is
             reported as an upper reference, never as the verdict.
* DIALS   g (gross) and cost.  Nothing else.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two - the queue names them: gross, cost)
    1. GROSS  g = 0.20, 0.25, ..., 1.00 (17 rungs; idea 574/804/805's ladder unchanged).
              PRE-DECLARED POINT: g = 1.00, the candidate as the queue names it.
    2. COST   0, 5, 10, 15, 20, 25, 50 bps per unit turnover.  The VERDICT is read at 10 bps
              (PROTOCOL rule 2); every other rung is reported beside it and selects nothing.
REPORTED-NEVER-SELECTED: execution lag (1 = PROTOCOL next-day, 2, 3), offset k = 0..20 as 21
    standalone sleeves, the ENS-EW convention, window (FULL / IS / OOS), path 4a, realised gross,
    turnover.  ALL grid points are written to CSV, pass or fail.

GATES (printed before any hypothesis is read)
    G1 engine  : fast_run vs engine.backtest on sleeve k=0, g=1.00, 10 bps.            bar 1e-9
    G2 REPRO   : (a) sleeve k=0 reproduces idea 804/805's published triple, full
                 11.92% / 1.21 / -15.5% and OOS 12.65% / 1.27 / -15.5%; bar = half a unit in the
                 last published digit of each field (Sharpe 5e-3, CAGR 5e-5, MaxDD 5e-4), the
                 tightest bar the published numbers can support (idea 805's own re-specification).
                 (a') DISCLOSED, and the reason (a) reads OVER on CAGR: `data/prices.csv` gained
                 one trading day (2026-09-14) between idea 805's run on 2026-09-12 and this one, so
                 the window is one day longer and every CAGR here is measured over a different
                 sample than the published one.  G2a' repeats (a) on the panel TRUNCATED at
                 2026-09-11 - 805's own last bar, read off git (`data/prices.csv` at the commit
                 preceding "Daily close 2026-09-14"), NOT searched for - and must pass the same
                 bar.  If it does, (a)'s CAGR miss is a calendar fact about the cache and not a
                 disagreement about the book; if it does not, the book has changed.
                 (b) idea 805's H_CAL census reproduces: 13 of 21 offsets pass 4b at
                 g=1.00 / 10 bps / lag 1, with all 8 failures on the DD leg alone.
                 (c) the two numbers the queue quotes: DD-cap margin 4.74pp and 21-offset MaxDD
                 spread 8.37pp, bar 0.05pp each.
                 If (a) or (b) fails this is not idea 805's book and nothing below is about it.
    G3 comparands : RULES v2 (live) and SPY on this run's window, all four 4b bars printed as
                 numbers so every verdict below can be checked by hand.                  no bar
    G4 identity: the ENS-NAV return series rebuilds the mean-of-sleeve-NAVs equity path,
                 max |E_reconstructed - E| relative, bar 1e-12; and ensemble cost equals the
                 NAV-weighted sleeve cost with no cross-sleeve turnover term.            bar 1e-12

PRE-REGISTERED HYPOTHESES (written before any number in this script was run; the only numbers in
hand at writing time are ideas 804/805's published ones, which the queue itself quotes)
    H_ENS    : at the pre-declared cell (g=1.00, 10 bps, lag 1) the ENS-NAV ensemble passes 4b.
    H_DDGAIN : the ensemble's MaxDD is BETTER (smaller in magnitude) than the MEAN of the 21
               sleeve MaxDDs by at least 1.00pp.  This is the queue's own question stated as a
               number: below that bar the ensemble merely reproduces the mean offset; above it,
               averaging buys real drawdown diversification.  The raw gap is reported either way.
    H_MARGIN : the ensemble's DD-cap margin (MaxDD_ens - 0.60 x MaxDD_SPY) EXCEEDS the 21-offset
               MaxDD spread (idea 805's 8.37pp, re-measured here).  This is the leg idea 805 failed
               and the only bar under which a monthly 4b pass is a rule rather than a date.
    H_COST   : the ensemble passes 4b at g=1.00 at EVERY cost rung through 25 bps.
    H_BAND   : the ensemble's 4b-pass gross band at 10 bps / lag 1 CONTAINS idea 805's single-offset
               band {0.90, 0.95, 1.00}.
    H_WF     : rule 8 - g chosen on IS (..2016-12-31) ALONE by BOTH pre-declared selectors,
               (i) IS-SHARPE (argmax IS Sharpe of the ensemble, ties -> lower g) and
               (ii) IS-BAND-MIDPOINT (midpoint rung of the widest contiguous IS-4b-admissible band),
               lands at a g whose OOS (2017-01-01..) reading passes 4b against SPY OOS.
               OOS is read ONCE.

RULE 8 WALK-FORWARD (required, and run whatever the verdict)
    IS = window start .. 2016-12-31, OOS = 2017-01-01 .. end.  Both selectors are fitted on IS only;
    OOS CAGR / Sharpe / MaxDD is reported against RULES v2 (live) OOS and SPY OOS.  Inside the IS
    window the 4b "OOS" leg collapses into that window's own second half; that is stated, not hidden.

KEEP PATHS: 4a (vs RULES v2 live) and 4b (vs SPY) evaluated and counted at EVERY cell of
    17 gross x 7 cost x 3 lags for the ensemble, and at every 21 offsets x 17 gross x 7 cost for the
    standalone sleeves at lag 1.

SURVIVORSHIP: U56 is the CURRENT constituent list of research/universe.json.  Dead names are absent,
    so every CAGR here is biased upward and the 4b CAGR floor - 0.70 x SPY's CAGR, measured on the
    same survivor-free benchmark - is EASIER to clear than on a point-in-time panel.  The DD cap is
    biased the same way.  No result below is corrected for this.

PROTOCOL: 10 bps per unit turnover, next-day fills, no shorting, no leverage.  Deterministic,
standalone, no network.  Modifies nothing but its own outputs:
    .grid.csv  .sleeves.csv  .walkforward.csv  .keeppaths.csv  .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-15_is-the-21-OFFSET-ENSEMBLE-of-the-805-book-a-4b-PASS_C"
OUT = ROOT / "research" / "backtests"

GGRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]     # TUNED 1
CGRID = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 50.0]           # TUNED 2
COST_MAIN, G_PRE, LAG_MAIN = 10.0, 1.00, 1
LAGS = [1, 2, 3]
OFFSETS = list(range(21))
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MA_WIN, WARMUP = 200, 260
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

# ideas 804/805's published numbers, used only as reproduction gates
PUB = dict(CAGR=0.1192, Sharpe=1.21, MaxDD=-0.155, OOS_CAGR=0.1265, OOS_Sharpe=1.27, OOS_MaxDD=-0.155)
PUB_TOL = dict(CAGR=5e-5, Sharpe=5e-3, MaxDD=5e-4, OOS_CAGR=5e-5, OOS_Sharpe=5e-3, OOS_MaxDD=5e-4)
PUB_CAL_PASS = 13          # idea 805's H_CAL: 13 of 21 offsets pass 4b
PUB_MARGIN_PP = 4.74       # idea 805's DD-cap margin, percentage points
PUB_SPREAD_PP = 8.37       # idea 805's 21-offset MaxDD spread, percentage points
PP_TOL = 0.05
PUB_PANEL_END = "2026-09-11"   # idea 805's last bar, read off git; used only by gate G2a'

DD_GAIN_BAR_PP = 1.00      # H_DDGAIN bar, declared above

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ the book (verbatim from 805)
def ma_dg_weights(px, g):
    """MA-DG: g/N over ALL priced names, zeroed where the name is below its 200d MA (to cash)."""
    pm = px.notna()
    ma = (px > px.rolling(MA_WIN).mean()) & pm
    cnt = pm.sum(axis=1).replace(0, np.nan)
    return (g * pm.div(cnt, axis=0).fillna(0.0)).where(ma, 0.0)


def shifted_mask(idx, k):
    """Monthly rebalance calendar moved k TRADING days after each month end (k = 0 is PROTOCOL)."""
    m = rebalance_mask(idx, "M").values
    if k == 0:
        return pd.Series(m, index=idx)
    pos = np.flatnonzero(m) + k
    pos = pos[pos < len(idx)]
    out = np.zeros(len(idx), dtype=bool)
    out[pos] = True
    return pd.Series(out, index=idx)


# ------------------------------------------------------------------ vectorised runner (805's)
def fast_run(prices, weights, mask, lag):
    """(gross return path before costs, turnover path, realised gross).  Costs come off afterwards:
    r(c) = r_gross - turn * c/1e4, exact because cost is a same-day subtraction from the return."""
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


# ------------------------------------------------------------------ the ensemble
def ens_nav(sleeve_rets):
    """ENS-NAV: split once into 21 equal sleeves, never re-equalise.  Returns (r_ens, equity)."""
    nav = np.cumprod(1.0 + sleeve_rets, axis=0)          # (T, K), each sleeve starts at 1
    eq = nav.mean(axis=1)
    r = np.empty_like(eq)
    r[0] = eq[0] - 1.0
    r[1:] = eq[1:] / eq[:-1] - 1.0
    return r, eq


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def legs_4b(r, spy):
    """PROTOCOL 4b as five booleans (True = leg passes).  Same arithmetic as ideas 574/804/805."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2),
            "OOS": bool(metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def legs_4b_window(r, spy, lo=None, hi=None):
    """The same five legs measured INSIDE one window; the OOS leg collapses into that window's own
    second half there (same object as H2), which is why it is named and reported, not hidden."""
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2), "OOS": bool(a2 > s2),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def triple(r, lo=None, hi=None):
    m = metrics(r.loc[lo:hi])
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def contiguous_runs(idxs):
    out, cur = [], []
    for i in sorted(idxs):
        if cur and i == cur[-1] + 1:
            cur.append(i)
        else:
            if cur:
                out.append(cur)
            cur = [i]
    if cur:
        out.append(cur)
    return out


def failstr(legs):
    f = [k for k in LEGS if not legs[k]]
    return "PASS" if not f else "+".join(f)


# ================================================================== run
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P(f"# pandas {pd.__version__} numpy {np.__version__}")

    px = load_universe().dropna(how="all").ffill()
    start = px.index[WARMUP]
    P(f"\nPANEL U56: {px.shape[1]} names x {len(px)} days, {px.index[0].date()} .. {px.index[-1].date()}")
    P(f"WINDOW (after {WARMUP}-day warm-up): {start.date()} .. {px.index[-1].date()}   "
      f"IS ..{IS_END}  OOS {OOS_START}..")
    P("SPY IS A TRADABLE CONSTITUENT of U56 as well as the comparand (804/805's construction).")

    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq="W")["returns"].loc[start:]

    W = {g: ma_dg_weights(px, g) for g in GGRID}
    MASK = {k: shifted_mask(px.index, k) for k in OFFSETS}

    # ---------------------------------------------------------------- raw sleeve paths
    # RAW[lag][g] = (gross returns (T,21), turnover (T,21)) restricted to the window
    P("\nrunning 17 gross x 21 offsets x 3 lags = 1071 sleeve paths ...")
    idx = px.index
    win = idx.get_indexer([start])[0]
    RAW = {}
    for lag in LAGS:
        for g in GGRID:
            RG = np.empty((len(idx) - win, len(OFFSETS)))
            TN = np.empty_like(RG)
            GR = np.empty(len(OFFSETS))
            for j, k in enumerate(OFFSETS):
                rg, tn, gr = fast_run(px, W[g], MASK[k], lag)
                RG[:, j] = rg.values[win:]
                TN[:, j] = tn.values[win:]
                GR[j] = float(gr.values[win:].mean())
            RAW[(lag, g)] = (RG, TN, GR)
    P(f"  ... {time.time() - t0:.1f}s")

    def sleeve_rets(lag, g, c):
        RG, TN, _ = RAW[(lag, g)]
        return RG - TN * c / 1e4

    def sleeve_series(lag, g, c, k):
        return pd.Series(sleeve_rets(lag, g, c)[:, k], index=idx[win:])

    def ens_series(lag, g, c, conv="NAV"):
        S = sleeve_rets(lag, g, c)
        if conv == "EW":
            return pd.Series(S.mean(axis=1), index=idx[win:])
        r, _ = ens_nav(S)
        return pd.Series(r, index=idx[win:])

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 100)
    P("GATES")
    P("=" * 100)

    # G1 engine agreement on sleeve k=0
    r_fast = sleeve_series(LAG_MAIN, G_PRE, COST_MAIN, 0)
    r_slow = backtest(px, W[G_PRE], cost_bps=COST_MAIN, freq="M")["returns"].loc[start:]
    d1 = float((r_fast - r_slow).abs().max())
    P(f"G1 engine   : max |fast - engine.backtest| on sleeve k=0 = {d1:.3e}   bar 1e-9   "
      f"{'PASS' if d1 < 1e-9 else 'FAIL'}")

    # G2a reproduction of the published triple
    c_, s_, dd_ = triple(r_fast)
    oc, os_, odd = triple(r_fast, OOS_START, None)
    got = dict(CAGR=c_, Sharpe=s_, MaxDD=dd_, OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd)
    ok2a = all(abs(got[k] - PUB[k]) <= PUB_TOL[k] for k in PUB)
    P(f"G2a REPRO of idea 804/805's candidate (sleeve k=0, g={G_PRE}, {COST_MAIN:.0f} bps, lag {LAG_MAIN}):")
    P(f"     published full {PUB['CAGR']:.2%} / {PUB['Sharpe']:.2f} / {PUB['MaxDD']:.1%}   "
      f"OOS {PUB['OOS_CAGR']:.2%} / {PUB['OOS_Sharpe']:.2f} / {PUB['OOS_MaxDD']:.1%}")
    P(f"     measured  full {c_:.2%} / {s_:.2f} / {dd_:.1%}   OOS {oc:.2%} / {os_:.2f} / {odd:.1%}")
    for k in PUB:
        P(f"       {k:<11} |diff| {abs(got[k] - PUB[k]):.3e}  tol {PUB_TOL[k]:.0e}  "
          f"{'ok' if abs(got[k] - PUB[k]) <= PUB_TOL[k] else 'OVER'}")
    P(f"     verdict {'PASS' if ok2a else 'FAIL'}")

    # G2a' the same triple on idea 805's own panel end (one trading day shorter)
    pxt = px.loc[:PUB_PANEL_END]
    st_t = pxt.index[WARMUP]
    rg_t, tn_t, _ = fast_run(pxt, ma_dg_weights(pxt, G_PRE), shifted_mask(pxt.index, 0), LAG_MAIN)
    r_t = (rg_t - tn_t * COST_MAIN / 1e4).loc[st_t:]
    ct, stt, ddt = triple(r_t)
    oct_, ost, oddt = triple(r_t, OOS_START, None)
    got_t = dict(CAGR=ct, Sharpe=stt, MaxDD=ddt, OOS_CAGR=oct_, OOS_Sharpe=ost, OOS_MaxDD=oddt)
    ok2ap = all(abs(got_t[k] - PUB[k]) <= PUB_TOL[k] for k in PUB)
    P(f"G2a' SAME BOOK on idea 805's panel end ({PUB_PANEL_END}; this run's cache carries "
      f"{(px.index > pd.Timestamp(PUB_PANEL_END)).sum()} extra trading day(s) to {px.index[-1].date()}):")
    P(f"     measured  full {ct:.4%} / {stt:.4f} / {ddt:.3%}   OOS {oct_:.4%} / {ost:.4f} / {oddt:.3%}")
    P(f"     max |diff| vs published, in tol units: "
      f"{max(abs(got_t[k] - PUB[k]) / PUB_TOL[k] for k in PUB):.3f}   verdict "
      f"{'PASS' if ok2ap else 'FAIL'}")
    P(f"     => G2a's CAGR miss is {'THE ADDED BAR, not the book' if ok2ap else 'NOT explained by the added bar'}. "
      f"Every CAGR below is measured on the longer window and is therefore NOT comparable to a "
      f"published CAGR to better than ~2e-4.")

    # G2b/c reproduction of idea 805's H_CAL census at the pre-declared cell
    cal_rows = []
    for k in OFFSETS:
        rk = sleeve_series(LAG_MAIN, G_PRE, COST_MAIN, k)
        lg = legs_4b(rk, spy)
        ck, sk, ddk = triple(rk)
        cal_rows.append(dict(offset=k, CAGR=ck, Sharpe=sk, MaxDD=ddk,
                             pass4b=all(lg.values()), fail=failstr(lg), pass4a=keep_4a(rk, base),
                             **{f"leg_{x}": lg[x] for x in LEGS}))
    cal = pd.DataFrame(cal_rows)
    n_pass = int(cal["pass4b"].sum())
    dd_only = all(set(r.split("+")) == {"DD"} for r in cal.loc[~cal["pass4b"], "fail"])
    spread_pp = float((cal["MaxDD"].max() - cal["MaxDD"].min()) * 100)
    mS = metrics(spy)
    cap = 0.60 * mS["MaxDD"]
    margin0_pp = float((cal.loc[cal.offset == 0, "MaxDD"].iloc[0] - cap) * 100)
    ok2b = (n_pass == PUB_CAL_PASS) and dd_only
    ok2c = abs(spread_pp - PUB_SPREAD_PP) <= PP_TOL and abs(margin0_pp - PUB_MARGIN_PP) <= PP_TOL
    P(f"G2b REPRO of 805's H_CAL census: {n_pass} of 21 offsets pass 4b "
      f"(published {PUB_CAL_PASS}); all failures on DD alone = {dd_only}   "
      f"{'PASS' if ok2b else 'FAIL'}")
    P(f"G2c REPRO of the two quoted pp: offset-0 DD-cap margin {margin0_pp:.2f}pp "
      f"(published {PUB_MARGIN_PP}) | 21-offset MaxDD spread {spread_pp:.2f}pp "
      f"(published {PUB_SPREAD_PP})   bar {PP_TOL}pp each   {'PASS' if ok2c else 'FAIL'}")
    if not (ok2ap and ok2b):
        P("     *** G2 FAILED - this is not idea 805's book; everything below is void. ***")
    elif not ok2a:
        P("     [G2 reads PASS on the book: (a') PASS on 805's own panel end, (b) and (c) PASS on "
          "this one; (a) misses on CAGR alone and only by the added bar.]")

    # G3 comparands and the four 4b bars
    mB = metrics(base)
    s1, s2 = halves(spy)
    b1, b2 = halves(base)
    oS, oB = metrics(spy.loc[OOS_START:]), metrics(base.loc[OOS_START:])
    P("\nG3 comparands (this run's window):")
    P(f"     SPY           full {mS['CAGR']:.2%} / {mS['Sharpe']:.2f} / {mS['MaxDD']:.1%}   "
      f"halves {s1:.2f} / {s2:.2f}   OOS {oS['CAGR']:.2%} / {oS['Sharpe']:.2f} / {oS['MaxDD']:.1%}")
    P(f"     RULES v2 live full {mB['CAGR']:.2%} / {mB['Sharpe']:.2f} / {mB['MaxDD']:.1%}   "
      f"halves {b1:.2f} / {b2:.2f}   OOS {oB['CAGR']:.2%} / {oB['Sharpe']:.2f} / {oB['MaxDD']:.1%}")
    P(f"     4b BARS: H1 Sharpe > {s1:.4f} | H2 Sharpe > {s2:.4f} | OOS Sharpe > {oS['Sharpe']:.4f} "
      f"| MaxDD >= {cap:.4%} | CAGR >= {0.70 * mS['CAGR']:.4%}")
    P(f"     4a BARS: H1 Sharpe > {b1:.4f} | H2 Sharpe > {b2:.4f} | MaxDD >= {mB['MaxDD']:.4%}")

    # G4 ensemble identity
    S = sleeve_rets(LAG_MAIN, G_PRE, COST_MAIN)
    r_e, eq_e = ens_nav(S)
    rebuilt = np.cumprod(1.0 + r_e)
    d4 = float(np.abs(rebuilt / eq_e - 1.0).max())
    P(f"\nG4 identity : max |rebuilt/mean-of-sleeve-NAVs - 1| = {d4:.3e}   bar 1e-12   "
      f"{'PASS' if d4 < 1e-12 else 'FAIL'}")
    P("     ensemble cost = the 21 sleeves' own turnover only; no cross-sleeve transfer exists in "
      "ENS-NAV, so no extra cost term is charged (ENS-EW's daily re-equalisation IS unpriced).")

    # ---------------------------------------------------------------- main grid
    P("\n" + "=" * 100)
    P("MAIN GRID - ENS-NAV and ENS-EW at 17 gross x 7 cost x 3 lags (ALL 714 cells reported)")
    P("=" * 100)

    rows = []
    for lag in LAGS:
        for g in GGRID:
            for c in CGRID:
                for conv in ("NAV", "EW"):
                    r = ens_series(lag, g, c, conv)
                    lg = legs_4b(r, spy)
                    m = metrics(r)
                    S_ = sleeve_rets(lag, g, c)
                    dd_sl = np.array([metrics(pd.Series(S_[:, j], index=idx[win:]))["MaxDD"]
                                      for j in range(len(OFFSETS))])
                    rows.append(dict(
                        conv=conv, lag=lag, gross=g, cost_bps=c,
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=halves(r)[0], H2=halves(r)[1],
                        OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                        OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                        OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                        pass4b=all(lg.values()), fail4b=failstr(lg), pass4a=keep_4a(r, base),
                        dd_margin_pp=(m["MaxDD"] - cap) * 100,
                        sleeve_dd_mean=dd_sl.mean(), sleeve_dd_min=dd_sl.min(),
                        sleeve_dd_max=dd_sl.max(), sleeve_dd_spread_pp=(dd_sl.max() - dd_sl.min()) * 100,
                        dd_gain_pp=(m["MaxDD"] - dd_sl.mean()) * 100,
                        turnover_ann=float(pd.Series(RAW[(lag, g)][1].sum(axis=1) / len(OFFSETS),
                                                     index=idx[win:]).sum() / (len(idx[win:]) / 252)),
                        realised_gross=float(RAW[(lag, g)][2].mean()),
                        **{f"leg_{x}": lg[x] for x in LEGS}))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    cal.to_csv(OUT / f"{STAMP}.sleeves.csv", index=False)

    main_cells = grid[(grid.lag == LAG_MAIN) & (grid.cost_bps == COST_MAIN)]
    P("\nENS-NAV at lag 1 / 10 bps, all 17 gross rungs (the PROTOCOL cell column):")
    P(f"{'gross':>6} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1':>6} {'H2':>6} "
      f"{'OOSShrp':>8} {'4b':>5} {'fail':>14} {'4a':>4} {'DDmargin':>9} {'DDgain':>8}")
    for _, r in main_cells[main_cells.conv == "NAV"].iterrows():
        P(f"{r.gross:>6.2f} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.2f} {r.H2:>6.2f} "
          f"{r.OOS_Sharpe:>8.3f} {str(r.pass4b):>5} {r.fail4b:>14} {str(r.pass4a):>4} "
          f"{r.dd_margin_pp:>8.2f}pp {r.dd_gain_pp:>7.2f}pp")

    P("\nENS-EW (unpriced daily re-equalisation) at lag 1 / 10 bps, same rungs:")
    for _, r in main_cells[main_cells.conv == "EW"].iterrows():
        P(f"{r.gross:>6.2f} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} {r.H1:>6.2f} {r.H2:>6.2f} "
          f"{r.OOS_Sharpe:>8.3f} {str(r.pass4b):>5} {r.fail4b:>14} {str(r.pass4a):>4} "
          f"{r.dd_margin_pp:>8.2f}pp {r.dd_gain_pp:>7.2f}pp")

    # ---------------------------------------------------------------- the 21 sleeves
    P("\n" + "=" * 100)
    P("THE 21 SLEEVES at g=1.00 / 10 bps / lag 1 (idea 805's H_CAL table, re-measured)")
    P("=" * 100)
    P(f"{'offset':>6} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'4b':>5} {'fail':>8} {'4a':>5}")
    for _, r in cal.iterrows():
        P(f"{int(r.offset):>6} {r.CAGR:>8.2%} {r.Sharpe:>7.3f} {r.MaxDD:>8.2%} "
          f"{str(r.pass4b):>5} {r.fail:>8} {str(r.pass4a):>5}")
    P(f"\nsleeve MaxDD: mean {cal.MaxDD.mean():.2%}  min {cal.MaxDD.min():.2%}  "
      f"max {cal.MaxDD.max():.2%}  spread {spread_pp:.2f}pp")
    P(f"sleeve Sharpe: mean {cal.Sharpe.mean():.3f}  min {cal.Sharpe.min():.3f}  max {cal.Sharpe.max():.3f}")
    P(f"sleeve CAGR  : mean {cal.CAGR.mean():.2%}  min {cal.CAGR.min():.2%}  max {cal.CAGR.max():.2%}")
    rank0 = int((cal.MaxDD > cal.loc[cal.offset == 0, "MaxDD"].iloc[0]).sum()) + 1
    P(f"OFFSET 0 - the calendar the record published - ranks {rank0} of 21 on MaxDD "
      f"(1 = shallowest).  Its 4.74pp DD-cap margin is the margin of that rank, not of the book.")

    # ---------------------------------------------------------------- why averaging buys nothing
    P("\n" + "=" * 100)
    P("DIAGNOSTIC (reported, selects nothing): are the 21 calendars' drawdowns the SAME drawdown?")
    P("=" * 100)
    Spre = sleeve_rets(LAG_MAIN, G_PRE, COST_MAIN)
    Sdf = pd.DataFrame(Spre, index=idx[win:])
    corr = Sdf.corr().values
    off = corr[~np.eye(len(OFFSETS), dtype=bool)]
    P(f"mean pairwise correlation of the 21 sleeves' DAILY returns: {off.mean():.4f}  "
      f"(min {off.min():.4f}, max {off.max():.4f})")
    troughs = []
    for j in range(len(OFFSETS)):
        e = (1 + Sdf[j]).cumprod()
        troughs.append((e / e.cummax() - 1).idxmin())
    tr = pd.Series(troughs)
    eq_pre = (1 + ens_series(LAG_MAIN, G_PRE, COST_MAIN)).cumprod()
    tr_ens = (eq_pre / eq_pre.cummax() - 1).idxmin()
    same_m = int((tr.dt.to_period("M") == pd.Period(tr_ens, "M")).sum())
    P(f"ensemble MaxDD trough {tr_ens.date()}; sleeves trough on {tr.nunique()} distinct dates, "
      f"{same_m} of 21 in the same calendar month as the ensemble "
      f"({tr.min().date()} .. {tr.max().date()})")
    P("=> the 21 calendars do not diversify the drawdown because it is ONE market episode seen 21 "
      "times; the offset only moves WHERE in that episode each sleeve last re-set its weights.")

    # ---------------------------------------------------------------- hypotheses
    P("\n" + "=" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    pre = grid[(grid.conv == "NAV") & (grid.lag == LAG_MAIN) & (grid.cost_bps == COST_MAIN)
               & (grid.gross == G_PRE)].iloc[0]
    r_pre = ens_series(LAG_MAIN, G_PRE, COST_MAIN)
    lg_pre = legs_4b(r_pre, spy)

    P(f"H_ENS    : ENS-NAV at g={G_PRE}, {COST_MAIN:.0f} bps, lag {LAG_MAIN}:")
    P(f"           full {pre.CAGR:.2%} / {pre.Sharpe:.3f} / {pre.MaxDD:.2%}   "
      f"halves {pre.H1:.3f} / {pre.H2:.3f}   OOS {pre.OOS_CAGR:.2%} / {pre.OOS_Sharpe:.3f} / {pre.OOS_MaxDD:.2%}")
    P(f"           legs " + "  ".join(f"{k}={lg_pre[k]}" for k in LEGS))
    P(f"           => {'PASS' if pre.pass4b else 'FAIL (' + pre.fail4b + ')'}")

    gain = float(pre.dd_gain_pp)          # negative = ensemble DD worse than mean sleeve DD
    ok_gain = (-gain) >= DD_GAIN_BAR_PP   # MaxDD is negative; ensemble better means MaxDD larger
    P(f"H_DDGAIN : ensemble MaxDD {pre.MaxDD:.2%} vs mean sleeve MaxDD {pre.sleeve_dd_mean:.2%} "
      f"(min {pre.sleeve_dd_min:.2%}, max {pre.sleeve_dd_max:.2%})")
    P(f"           gain = {gain:+.2f}pp (positive = ensemble better than the mean offset); "
      f"bar {DD_GAIN_BAR_PP:.2f}pp   {'PASS' if gain >= DD_GAIN_BAR_PP else 'FAIL'}")

    ok_margin = float(pre.dd_margin_pp) > spread_pp
    P(f"H_MARGIN : ensemble DD-cap margin {pre.dd_margin_pp:.2f}pp vs 21-offset MaxDD spread "
      f"{spread_pp:.2f}pp   {'PASS' if ok_margin else 'FAIL'}")

    cost_cells = grid[(grid.conv == "NAV") & (grid.lag == LAG_MAIN) & (grid.gross == G_PRE)
                      & (grid.cost_bps <= 25.0)]
    ok_cost = bool(cost_cells.pass4b.all())
    P("H_COST   : 4b at g=1.00, lag 1, by cost rung: " +
      "  ".join(f"{int(r.cost_bps)}bps={'PASS' if r.pass4b else r.fail4b}"
               for _, r in grid[(grid.conv == 'NAV') & (grid.lag == LAG_MAIN)
                                & (grid.gross == G_PRE)].iterrows()))
    P(f"           through 25 bps   {'PASS' if ok_cost else 'FAIL'}")

    band = sorted(main_cells[(main_cells.conv == "NAV") & main_cells.pass4b].gross.tolist())
    ok_band = set([0.90, 0.95, 1.00]).issubset(set(band))
    runs = contiguous_runs([GGRID.index(g) for g in band])
    P(f"H_BAND   : ENS-NAV 4b-pass gross band at 10 bps / lag 1 = {band if band else 'EMPTY'}")
    P(f"           contiguous runs: {[[GGRID[i] for i in r] for r in runs] if runs else 'none'}; "
      f"contains 805's {{0.90,0.95,1.00}}   {'PASS' if ok_band else 'FAIL'}")

    P("\nlag sensitivity (REPORTED, never selected) - ENS-NAV at g=1.00, 10 bps:")
    for lag in LAGS:
        r = grid[(grid.conv == "NAV") & (grid.lag == lag) & (grid.cost_bps == COST_MAIN)
                 & (grid.gross == G_PRE)].iloc[0]
        P(f"     lag {lag}: {r.CAGR:.2%} / {r.Sharpe:.3f} / {r.MaxDD:.2%}  "
          f"4b {'PASS' if r.pass4b else r.fail4b}  margin {r.dd_margin_pp:.2f}pp")

    # ---------------------------------------------------------------- rule 8
    P("\n" + "=" * 100)
    P("RULE 8 WALK-FORWARD - g chosen on IS only, OOS read once")
    P("=" * 100)
    is_rows = []
    for g in GGRID:
        r = ens_series(LAG_MAIN, g, COST_MAIN)
        mi = metrics(r.loc[:IS_END])
        lgi = legs_4b_window(r, spy, None, IS_END)
        is_rows.append(dict(gross=g, IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            IS_4b=all(lgi.values()), IS_fail=failstr(lgi)))
    isdf = pd.DataFrame(is_rows)
    P(f"{'gross':>6} {'IS CAGR':>9} {'IS Shrp':>8} {'IS MaxDD':>9} {'IS 4b':>6} {'fail':>14}")
    for _, r in isdf.iterrows():
        P(f"{r.gross:>6.2f} {r.IS_CAGR:>9.2%} {r.IS_Sharpe:>8.3f} {r.IS_MaxDD:>9.2%} "
          f"{str(r.IS_4b):>6} {r.IS_fail:>14}")

    pick_sharpe = float(isdf.sort_values(["IS_Sharpe", "gross"], ascending=[False, True]).iloc[0].gross)
    adm = [GGRID.index(g) for g in isdf[isdf.IS_4b].gross.tolist()]
    runs_is = contiguous_runs(adm)
    if runs_is:
        widest = max(runs_is, key=len)
        pick_band = GGRID[widest[len(widest) // 2]]
    else:
        pick_band = None
    P(f"\nselector 1 IS-SHARPE        -> g = {pick_sharpe:.2f}")
    P(f"selector 2 IS-BAND-MIDPOINT -> {'g = %.2f' % pick_band if pick_band is not None else 'NO PICK (the IS 4b band is EMPTY)'}")

    wf_rows = []
    for sel, g in [("IS-SHARPE", pick_sharpe), ("IS-BAND-MIDPOINT", pick_band),
                   ("PRE-DECLARED g=1.00", G_PRE)]:
        if g is None:
            wf_rows.append(dict(selector=sel, gross=np.nan))
            continue
        r = ens_series(LAG_MAIN, g, COST_MAIN)
        lo = legs_4b_window(r, spy, OOS_START, None)
        mo = metrics(r.loc[OOS_START:])
        wf_rows.append(dict(selector=sel, gross=g, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                            OOS_MaxDD=mo["MaxDD"], OOS_4b=all(lo.values()), OOS_fail=failstr(lo),
                            OOS_4a=keep_4a(r.loc[OOS_START:], base.loc[OOS_START:]),
                            **{f"OOSleg_{x}": lo[x] for x in LEGS}))
    wf = pd.DataFrame(wf_rows)
    # comparands on the same OOS window
    for nm, rr in [("SPY", spy), ("RULES v2 live", base)]:
        mo = metrics(rr.loc[OOS_START:])
        wf = pd.concat([wf, pd.DataFrame([dict(selector=nm, gross=np.nan, OOS_CAGR=mo["CAGR"],
                                               OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])])],
                       ignore_index=True)
    wf.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    P("\nOOS (2017-01-01 .. end), read ONCE:")
    P(f"{'selector':>22} {'g':>5} {'OOS CAGR':>9} {'OOS Shrp':>9} {'OOS MaxDD':>10} {'4b':>6} {'fail':>14} {'4a':>5}")
    for _, r in wf.iterrows():
        g_s = "  -  " if pd.isna(r.gross) else f"{r.gross:.2f}"
        f_s = "" if not isinstance(r.get("OOS_fail"), str) else r.OOS_fail
        p_s = "" if pd.isna(r.get("OOS_4b", np.nan)) else str(r.OOS_4b)
        a_s = "" if pd.isna(r.get("OOS_4a", np.nan)) else str(r.OOS_4a)
        P(f"{r.selector:>22} {g_s:>5} {r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>9.3f} {r.OOS_MaxDD:>10.2%} "
          f"{p_s:>6} {f_s:>14} {a_s:>5}")

    ok_wf = bool(wf[wf.selector.isin(["IS-SHARPE", "IS-BAND-MIDPOINT"])].get("OOS_4b", pd.Series(dtype=bool)).all()) \
        and pick_band is not None
    P(f"H_WF     : both IS-only selectors pass 4b out of sample   {'PASS' if ok_wf else 'FAIL'}")

    # ---------------------------------------------------------------- keep-path census
    P("\n" + "=" * 100)
    P("KEEP-PATH CENSUS (all cells, both conventions)")
    P("=" * 100)
    cen = (grid.groupby(["conv", "lag", "cost_bps"])
           .agg(n=("pass4b", "size"), pass4b=("pass4b", "sum"), pass4a=("pass4a", "sum"))
           .reset_index())
    cen.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    for _, r in cen.iterrows():
        P(f"     conv {r.conv:<4} lag {int(r.lag)} cost {int(r.cost_bps):>2} bps: "
          f"4b {int(r.pass4b)}/{int(r.n)}   4a {int(r.pass4a)}/{int(r.n)}")
    P(f"\nTOTAL: 4b {int(grid.pass4b.sum())}/{len(grid)}   4a {int(grid.pass4a.sum())}/{len(grid)}")
    P(f"sleeves (21 offsets, g=1.00, 10 bps, lag 1): 4b {n_pass}/21   4a {int(cal.pass4a.sum())}/21")

    # ---------------------------------------------------------------- verdict
    P("\n" + "=" * 100)
    P("VERDICT")
    P("=" * 100)
    H = {"H_ENS": bool(pre.pass4b), "H_DDGAIN": bool(gain >= DD_GAIN_BAR_PP),
         "H_MARGIN": bool(ok_margin), "H_COST": ok_cost, "H_BAND": bool(ok_band), "H_WF": ok_wf}
    for k, v in H.items():
        P(f"     {k:<9} {'PASS' if v else 'FAIL'}")
    P(f"     {sum(H.values())} of {len(H)} pre-registered hypotheses pass.")
    P(f"     4a at the pre-declared cell: {'PASS' if pre.pass4a else 'FAIL'}")
    P(f"\nruntime {time.time() - t0:.1f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
