#!/usr/bin/env python3
"""Idea 813 - does TIE SUFFICIENCY break outside the SPYDD CONFOUND on any corpus with 30+ ties?
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 813, verbatim)
    Idea 811's POST20 window broke idea 596's sufficiency leg for the first time (1.0000 ->
    0.8000, 3 false positives, arms whose own MaxDD sits on the 2025 episode) but all three sit
    in the SPYDD family the corpus names as its confound, and the break vanishes when that family
    is dropped (12 of 12).  Build a corpus with >= 30 ties and a decline leg longer than 60
    trading days and test whether sufficiency breaks outside the confound.
    Max 2 params (window, family set).

WHAT IS BEING TESTED, STATED SO THE TWO HALVES ARE NOT CONFLATED
    The tie label is  |MaxDD(arm) - MaxDD(CONTROL-U)| <= 1e-12.  The predicate is  cover(DECLINE)
    = 0, i.e. the arm never de-grosses anywhere inside the control's peak -> trough leg.
      NECESSITY  P(pred | tie) is near-IDENTITY BY CONSTRUCTION: an arm that holds the control's
                 weights through peak -> trough reproduces that decline exactly, so a tie can
                 hardly happen any other way.  596 and 811 both read 1.0000 and so does this run;
                 it is a sanity leg, not evidence.
      SUFFICIENCY P(tie | pred) is the EMPIRICAL half and the only one at issue here.  It fails
                 when an arm holds through the control's decline but its OWN MaxDD is set deeper
                 on a DIFFERENT episode.  596 published 1.0000 with 0 counterexamples; 811 found
                 3 and every one is SPYDD, the family that gates on the drawdown itself.
    So the open question is narrow and answerable: are there false positives OUTSIDE SPYDD, on a
    corpus that (a) is big enough to see them (>= 30 ties) and (b) has a LONG decline leg (> 60
    trading days), which is where 811 argues the predicate should have nothing to predict.

THE STANDING OBSTACLE THIS RUN HAS TO BEAT (and may not)
    811's finding was a VACANCY: across a 302-336 day grinding decline every gate in every family
    fires somewhere inside it, so #pred(DECLINE) = 0 of 117 in all three pure BEAR22 windows and
    there is nothing to score.  A corpus with >= 30 ties AND a > 60-day decline therefore cannot
    be conjured by picking a window alone.  Two pre-registered widenings are used, both of them
    REPORTED AXES and neither a tuned parameter:
      (i)  the dial ladder is extended by ONE rung per family toward the LOOSE end (a gate that
           fires rarely, and mostly not inside a decline, is exactly the arm that can hold through
           peak -> trough and still fire somewhere), 5 rungs per family instead of 4;
      (ii) two further MARKET-state families from the record's own vocabulary (idea 606's CORR and
           DISP) join the four of 596/811, 6 families instead of 4.
    Both widenings are declared here, before any grid is read, and every arm they add is printed.
    The 596/811 SUB-CORPUS (4 families x their original 4 dials) is carried through the whole run
    as a REPRODUCTION GATE (G5) so the widening cannot quietly move the published numbers.

THE CORPUS (same construction as 596/811, so cells are comparable)
    book      B(g) = the LIVE form, baseline.rules_v2_weights: hold every name inside its 200d
              +/-3% band at g/N of NAV, gated-out weight to CASH, weekly, next-day fill, 10 bps.
    clause    a MARKET-level gate s_t in {0,1}; gate OFF => the book is de-grossed to cash that
              week (k = 0, never re-spread).  arm = B(g) * s.
    controls  CONTROL-U = B(g) at nominal gross (the comparand the tie label is defined against),
              CONTROL-M = B(g) * c with c set so mean realised gross equals the arm's.
    families  SPYTR h in {50,100,150,200,250} / BREADTH q in {0.05,0.20,0.35,0.50,0.65} /
              VOL v in {0.15,0.25,0.40,0.60,0.90} / SPYDD d in {0.05,0.10,0.20,0.35,0.45} /
              CORR c in {0.20,0.30,0.40,0.55,0.75} / DISP s in {0.10,0.15,0.20,0.30,0.50}.
              SPYDD is the CONFOUND (it gates on the drawdown itself) and is NAMED; every rate is
              reported again with it dropped - that is tuned dial (2).
    panels    U56, B136, SMALL (sub-$2B panel, tickers with max_1d_move >= 1.0 dropped first).
    gross     g in {0.50, 0.75, 1.00}.   6 x 5 x 3 = 90 arms per panel, 270 in all, ALL reported.

    The book is built ONCE on the full price history, so the 200d band and every gate keep their
    full warm-up; a WINDOW is an EVALUATION window on the return path, never a data slice.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) WINDOW    seven named (start, end) rungs, chosen so that several of them are expected to
                  bind on a LONG decline; which ones actually do is MEASURED in section A and
                  reported whether they do or not:
                    FULL    warm-up end .. sample end   the 596/811 reference; binds on 2020
                    PRE20   warm-up end .. 2019-12-31
                    E2011   warm-up end .. 2012-12-31
                    E2015   2013-01-01  .. 2017-12-31
                    E2018   2016-01-01  .. 2019-12-31
                    POST20  2020-07-01  .. sample end   811's break window
                    BEAR22  2021-01-01  .. 2024-12-31   811's empty window
    (2) FAMILY SET  ALL (6 families) vs NO-SPYDD (5 families, the confound dropped).
    7 x 2 = 14 grid points, EVERY ONE printed and written to .predicates.csv.
    COVER BAR: NOT a third tune.  Headline is the pre-registered eps = 0; the ladder
    eps in {0, 1e-12, 1e-6, 1e-4, 1e-3} is printed in full as a reported robustness axis, as
    596 and 811 did, because "cover == 0" is not a testable event in floating point.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_CORPUS   a QUALIFYING corpus exists: pooled (panel, window, gross) cells whose control's
               binding DECLINE leg is > 60 trading days, carrying >= 30 non-degenerate MaxDD
               ties.  This is the queue's own existence bar and it is the first thing measured.
    H_CORPUSX  the same corpus still carries >= 30 ties with SPYDD dropped.  Without this the
               question cannot be answered at strength however the rates read.
    H_PRED     that corpus carries >= 30 arms satisfying the DECLINE predicate (#pred >= 30) -
               811's vacancy does NOT generalise to every long decline.  A sufficiency rate over
               an EMPTY predicate population is NOT EVALUABLE, never PASS and never FAIL.
    H_NEC      necessity P(pred | tie) = 1.0000 on the qualifying corpus (the construction leg).
    H_SUFF     sufficiency P(tie | pred) = 1.0000 on the qualifying corpus with ALL families -
               596's claim, restated on a long-decline corpus.
    H_BREAK    THE LOAD-BEARING ONE, and it is stated in the direction that would falsify 596:
               sufficiency BREAKS OUTSIDE THE CONFOUND - at least one false positive whose family
               is NOT SPYDD exists on the qualifying corpus at eps = 0.  PASS means 596's
               sufficiency leg has a clean counterexample; FAIL means it survives its first
               properly powered test outside the confound.
    H_CONFSHARE if false positives exist at all, SPYDD's share of them is > its share of the
               predicate population - i.e. the confound really is where the breaks concentrate,
               which is what 811 asserted from 3 cells.
    H_LONG     the tie RATE on long-decline cells is strictly below the FULL window's - 811's
               "a gate can sit out a 17-day crash, not a year-long grind" generalises beyond 2022.
    H_COST     the switch-cost term still adds nothing: DECLINE and DECLINE+COST agree on every
               scored cell of every window (811 read 0 disagreements at all 5 rungs).

GATES (printed first; all must pass before any verdict is read)
    G1 the arm at a never-firing gate is EXACTLY CONTROL-U.
    G2 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G3 in EVERY (panel, gross, window) the located binding episode reproduces that window's
       MaxDD to <= 1e-12.
    G4 CONTROL-M's realised mean gross equals the arm's to <= 1e-3.
    G5 REPRODUCTION: the 596/811 sub-corpus (4 families x their original 4 dials) on the FULL
       window returns 811's committed reading - 141 scored arms, 45 ties, necessity 1.0000,
       sufficiency 1.0000, ties by family SPYTR 0 / BREADTH 12 / VOL 18 / SPYDD 15.

PROTOCOL RULE 8 (mandatory, run and reported):
    (a) STANDING convention - per (panel, family, gross) the DIAL is chosen on IS (..2016-12-31)
        by IS Sharpe alone, OOS (2017-01-01..) read exactly ONCE, reported as CAGR/Sharpe/MaxDD
        against RULES v2 and SPY on the same window.  Both KEEP paths evaluated on all 270 arms.
    (b) WINDOW-LOCAL - a window that ends in 2012 has no 2017+ out-of-sample, so for every
        non-FULL window the dial is also chosen on its FIRST HALF and read once on its SECOND
        HALF.  A stated DEPARTURE from the record's 2016/2017 split, reported beside (a).

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic, the SMALL panel worst (a sub-$2B screen read today cannot see the names that fell
    out of it - data/SMALL_PANEL_README.md).  The predicate rates are within-panel agreement
    rates, which survivorship moves far less than levels.  The short windows are 3-5 years and
    several are wholly inside a bull leg, so no Sharpe or CAGR read off them is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .cells.csv       one row per (arm, window): metrics, tie label, cover legs, 4a/4b verdicts
    .episodes.csv    per (panel, gross, window) the control's binding episode and its shape
    .predicates.csv  the 7 x 2 tuned grid x 4 leg splits x the 5-rung cover ladder, all points
    .falsepos.csv    every false positive of the DECLINE predicate, with its family
    .walkforward.csv rule-8 (a) standing and (b) window-local picks and their OOS reads
    .result.md       the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

DATE = "2026-09-12"
SLUG = "does-TIE-SUFFICIENCY-break-outside-the-SPYDD-CONFOUND-on-any-corpus-with-30-PLUS-TIES"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

FREQ = "W"
LAG = 1
COST = 10
BAND = 0.03
GROSSES = [0.50, 0.75, 1.00]
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SMALL_MAXMOVE = 1.0
LIVE_GROSS = 0.75

# tuned dial 1: the WINDOW.  A window is an EVALUATION window on the return path; the book and
# every gate keep the full price history behind them.
WINDOWS = [("FULL",   None,         None),
           ("PRE20",  None,         "2019-12-31"),
           ("E2011",  None,         "2012-12-31"),
           ("E2015",  "2013-01-01", "2017-12-31"),
           ("E2018",  "2016-01-01", "2019-12-31"),
           ("POST20", "2020-07-01", None),
           ("BEAR22", "2021-01-01", "2024-12-31")]
WNAMES = [w[0] for w in WINDOWS]

LEGS_SPLIT = ["EPISODE", "DECLINE", "RECOVERY", "DECLINE+COST"]
EPS_BAR = [0.0, 1e-12, 1e-6, 1e-4, 1e-3]   # reported robustness ladder, headline is eps = 0
HEAD_EPS = 0.0
TIE_EPS = 1e-12
LONG_DECLINE = 60          # the queue's bar, in trading days
TIE_BAR = 30               # the queue's bar, in ties
PRED_BAR = 30

# 6 families x 5 dials.  The 596/811 rungs are marked; the 5th rung of each family and the two
# extra families are the pre-registered WIDENING described in the header, not a tune.
FAMILIES = {
    "SPYTR":   [50, 100, 150, 200, 250],
    "BREADTH": [0.05, 0.20, 0.35, 0.50, 0.65],
    "VOL":     [0.15, 0.25, 0.40, 0.60, 0.90],
    "SPYDD":   [0.05, 0.10, 0.20, 0.35, 0.45],
    "CORR":    [0.20, 0.30, 0.40, 0.55, 0.75],
    "DISP":    [0.10, 0.15, 0.20, 0.30, 0.50],
}
# the exact 596/811 corpus, kept for the reproduction gate G5
BASE_FAMILIES = {"SPYTR": [100, 150, 200, 250], "BREADTH": [0.20, 0.35, 0.50, 0.65],
                 "VOL": [0.15, 0.25, 0.40, 0.60], "SPYDD": [0.05, 0.10, 0.20, 0.35]}
CONFOUND = "SPYDD"
KEEP_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
CORR_W = 60
DISP_W = 60

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (ideas 596/804/811's)
def fast_run(prices, weights, mask, lag=LAG):
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


def net(rg, tn, cost=COST):
    return rg - tn * cost / 1e4


# ------------------------------------------------------------------ PROTOCOL rule 4
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def legs_4b(r, spy_stats, r_oos=None, spy_oos_sharpe=None):
    """4b legs against pre-computed SPY statistics for this window."""
    a1, a2 = halves(r)
    m = metrics(r)
    if r_oos is None:
        oos = a2 > spy_stats["h2"]
    else:
        oos = metrics(r_oos)["Sharpe"] > spy_oos_sharpe
    return {"H1": bool(a1 > spy_stats["h1"]), "H2": bool(a2 > spy_stats["h2"]), "OOS": bool(oos),
            "DD": bool(m["MaxDD"] >= 0.60 * spy_stats["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * spy_stats["CAGR"])}


def keep_4a(r, live_stats):
    a1, a2 = halves(r)
    return bool(a1 > live_stats["h1"] and a2 > live_stats["h2"]
                and metrics(r)["MaxDD"] >= live_stats["MaxDD"])


def series_stats(r):
    m = metrics(r)
    h1, h2 = halves(r)
    return {"h1": h1, "h2": h2, "MaxDD": m["MaxDD"], "CAGR": m["CAGR"], "Sharpe": m["Sharpe"]}


# ------------------------------------------------------------------ episodes
def binding_episode(r: pd.Series):
    """(peak, trough, recovery, recovered, MaxDD) of the MaxDD episode of r."""
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    trough = dd.idxmin()
    peak = eq.loc[:trough].idxmax()
    after = eq.loc[trough:]
    rec_mask = after >= eq.loc[peak]
    if rec_mask.any():
        recovery, recovered = rec_mask.idxmax(), True
    else:
        recovery, recovered = eq.index[-1], False
    return peak, trough, recovery, recovered, float(dd.min())


def cover(u: pd.Series, lo, hi):
    """Mean de-gross depth 1 - u over [lo, hi] inclusive.  u = armGross / controlGross."""
    w = u.loc[lo:hi]
    if len(w) == 0:
        return np.nan
    return float((1.0 - w).clip(lower=0.0).mean())


def switch(tn_arm: pd.Series, tn_ctl: pd.Series, lo, hi):
    a, c = tn_arm.loc[lo:hi], tn_ctl.loc[lo:hi]
    return float(np.abs(a - c).sum())


# ------------------------------------------------------------------ panels and gates
def panel(name):
    if name == "U56":
        px = load_universe()
    elif name == "B136":
        px = load_universe(broad=True)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= SMALL_MAXMOVE, "ticker"])
        drop = [c for c in px.columns if c in bad and c != "SPY"]
        px = px.drop(columns=drop)
        P(f"   SMALL panel: dropped {len(drop)} tickers with max_1d_move >= {SMALL_MAXMOVE} "
          f"(data/small_meta.csv), {len([c for c in px.columns if c != 'SPY'])} left")
    return px.dropna(how="all").ffill()


def avg_pair_corr(R: pd.DataFrame, w=CORR_W):
    """Trailing average pairwise correlation from the equal-weight aggregate identity
       Var(mean) = (1/N^2)[ sum var_i + sum_{i!=j} rho_ij s_i s_j ].
       Uses only names priced on each date; trailing only, no look-ahead."""
    sig = R.rolling(w).std()
    n = sig.notna().sum(axis=1)
    s1 = sig.sum(axis=1, min_count=1)
    s2 = (sig ** 2).sum(axis=1, min_count=1)
    m = R.mean(axis=1)
    sm = m.rolling(w).std()
    num = (n ** 2) * (sm ** 2) - s2
    den = (s1 ** 2) - s2
    return (num / den.replace(0, np.nan)).clip(-1.0, 1.0)


def gate(px, trade, fam, dial, cache):
    spy = px["SPY"]
    if fam == "SPYTR":
        return spy > spy.rolling(int(dial)).mean()
    if fam == "BREADTH":
        q = px[trade]
        above = q > q.rolling(200).mean()
        share = above.sum(axis=1) / q.notna().sum(axis=1).replace(0, np.nan)
        return share.fillna(0.0) >= dial
    if fam == "VOL":
        return spy.pct_change().rolling(20).std() * np.sqrt(252) <= dial
    if fam == "SPYDD":
        return (spy / spy.cummax() - 1.0) >= -dial
    if fam == "CORR":
        return cache["corr"] <= dial
    if fam == "DISP":
        return cache["disp"] <= dial
    raise ValueError(fam)


def pred_mask(df, leg, eps):
    if leg == "EPISODE":
        return df.cover_EPISODE <= eps
    if leg == "DECLINE":
        return df.cover_DECLINE <= eps
    if leg == "RECOVERY":
        return df.cover_RECOVERY <= eps
    return (df.cover_DECLINE <= eps) & (df.switch_DECLINE <= eps)


def rates(df, leg, eps):
    m, t = pred_mask(df, leg, eps), df.tie_U
    npred, ntie = int(m.sum()), int(t.sum())
    p_pt = float((m & t).sum() / ntie) if ntie else np.nan
    p_tp = float((m & t).sum() / npred) if npred else np.nan
    acc = float(((m & t) | (~m & ~t)).mean()) if len(df) else np.nan
    return dict(n=len(df), n_pred=npred, n_tie=ntie, P_pred_given_tie=p_pt,
                P_tie_given_pred=p_tp, accuracy=acc, false_neg=int((t & ~m).sum()),
                false_pos=int((m & ~t).sum()),
                exact=bool(p_pt == 1.0 and p_tp == 1.0))


def main():
    t0 = time.time()
    P(f"# Idea 813 - {SLUG}  (lane C, {DATE})")
    P("# Object: idea 596's tie SUFFICIENCY leg P(tie|DECLINE)=1.0000 has never been tested on a")
    P("# corpus that is both POWERED (>= 30 ties) and LONG-DECLINE (> 60 trading days); 811's only")
    P("# counterexamples were all SPYDD, the family its own corpus names as the confound.")
    P(f"# TUNED: window {WNAMES} x family set [ALL, NO-{CONFOUND}] = {len(WNAMES)*2} points, ALL reported.")
    for nm, a, b in WINDOWS:
        P(f"#    window {nm:<7} start {str(a or 'warm-up end'):<12} end {str(b or 'sample end'):<12}")
    P(f"# Cover bar is NOT a third tune: headline eps = {HEAD_EPS:g}, ladder {EPS_BAR} printed in full.")
    P("# Book grid (panel x family x dial x gross) is a REPORTED axis: 3 x 6 x 5 x 3 = 270 arms.")
    P("# PRE-REGISTERED WIDENING (declared, not tuned): one extra LOOSE dial per family and two")
    P("# extra families (CORR, DISP, idea 606's) - because 811's vacancy is that every gate fires")
    P("# somewhere inside a long decline, and only a rarely-firing gate can hold through one.")
    P("# The 596/811 sub-corpus is carried as reproduction gate G5 so the widening cannot move it.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    cells, eprows, wfrows = [], [], []

    for pname in ["U56", "B136", "SMALL"]:
        P(f"\n{'='*108}\nPANEL {pname}\n{'='*108}")
        px = panel(pname)
        trade = [c for c in px.columns if c != "SPY"]
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        R = px[trade].pct_change()
        cache = {"corr": avg_pair_corr(R).reindex(px.index),
                 "disp": (px[trade] / px[trade].shift(DISP_W) - 1.0).std(axis=1).reindex(px.index)}
        P(f"   {len(trade)} tradeable names, {len(px.loc[start:])} scored days "
          f"{start.date()}..{px.index[-1].date()}")
        P(f"   CORR state (trailing {CORR_W}d avg pairwise): median {cache['corr'].loc[start:].median():.3f} "
          f"p05 {cache['corr'].loc[start:].quantile(0.05):.3f} p95 {cache['corr'].loc[start:].quantile(0.95):.3f}")
        P(f"   DISP state (x-sec std of {DISP_W}d returns): median {cache['disp'].loc[start:].median():.3f} "
          f"p05 {cache['disp'].loc[start:].quantile(0.05):.3f} p95 {cache['disp'].loc[start:].quantile(0.95):.3f}")

        wspan = {nm: (start if s is None else max(start, pd.Timestamp(s)),
                      px.index[-1] if e is None else min(px.index[-1], pd.Timestamp(e)))
                 for nm, s, e in WINDOWS}

        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        live_rg, live_tn, _ = fast_run(px, rules_v2_weights(px, band=BAND, gross=LIVE_GROSS), mask)
        live_full = net(live_rg, live_tn).loc[start:]

        # per-window comparand statistics, computed ONCE
        WS = {}
        for w in WNAMES:
            w0, w1 = wspan[w]
            sp, lv = spy_full.loc[w0:w1], live_full.loc[w0:w1]
            WS[w] = dict(spy=series_stats(sp), live=series_stats(lv), sp=sp, lv=lv,
                         spy_oos_sharpe=(metrics(sp.loc[OOS_START:])["Sharpe"] if w == "FULL" else np.nan))

        # ---- controls, one per gross; binding episode per (gross, window) -------------
        ctl: dict[float, tuple] = {}
        ep: dict[tuple, tuple] = {}
        for g in GROSSES:
            Wb = rules_v2_weights(px, band=BAND, gross=g)
            rg, tn, gr = fast_run(px, Wb, mask)
            r = net(rg, tn).loc[start:]
            ctl[g] = (r, tn.loc[start:], gr.loc[start:], Wb)
            for w in WNAMES:
                w0, w1 = wspan[w]
                rw = r.loc[w0:w1]
                pk, tr, rc, rec, ddmin = binding_episode(rw)
                dd_days = int(((rw.index >= pk) & (rw.index <= tr)).sum())
                rc_days = int(((rw.index > tr) & (rw.index <= rc)).sum())
                ep[(g, w)] = (pk, tr, rc, rec, ddmin)
                eprows.append(dict(panel=pname, gross=g, window=w,
                                   win_start=rw.index[0].date(), win_end=rw.index[-1].date(),
                                   n_days=len(rw), peak=pk.date(), trough=tr.date(),
                                   recovery=rc.date(), recovered=rec, trough_year=int(tr.year),
                                   MaxDD=ddmin, decline_days=dd_days, recovery_days=rc_days,
                                   long_decline=bool(dd_days > LONG_DECLINE)))
        P(f"\n   CONTROL-U binding episodes by (gross, window)  [the object of idea 813]")
        P(f"   {'g':>5} {'window':<7} {'days':>5} {'MaxDD':>8} {'peak':>11} {'trough':>11} "
          f"{'recovery':>11} {'dec_d':>6} {'rec_d':>6} {'>60d?':>6}")
        for e in [e for e in eprows if e["panel"] == pname]:
            P(f"   {e['gross']:>5.2f} {e['window']:<7} {e['n_days']:>5} {e['MaxDD']:>8.2%} "
              f"{str(e['peak']):>11} {str(e['trough']):>11} {str(e['recovery']):>11} "
              f"{e['decline_days']:>6} {e['recovery_days']:>6} "
              f"{'LONG' if e['long_decline'] else 'short':>6}"
              f"{'' if e['recovered'] else '  (NEVER RECOVERED - flagged)'}")

        # ---- gates G1..G3 ------------------------------------------------------------
        if pname == "U56":
            P(f"\n{'-'*108}\nGATES\n{'-'*108}")
            g = LIVE_GROSS
            _, _, _, Wb = ctl[g]
            never = Wb.mul(pd.Series(1.0, index=px.index), axis=0)
            rg_n, tn_n, _ = fast_run(px, never, mask)
            g1 = max(float(np.abs((net(rg_n, tn_n).loc[start:] - ctl[g][0]).values).max()),
                     float(np.abs((tn_n.loc[start:] - ctl[g][1]).values).max()))
            eng = backtest(px, Wb, cost_bps=COST, freq=FREQ)
            g2 = float(np.abs((net(rg_n, tn_n) - eng["returns"]).loc[start:].values).max())
            for nm, v, ok in [("G1 never-firing arm == CONTROL-U exactly", f"max|d| {g1:.3e}", g1 < 1e-12),
                              ("G2 fast_run == engine.backtest", f"max|d| {g2:.3e}", g2 < 1e-9)]:
                P(f"   {nm:<52} {v:<20} {'PASS' if ok else 'FAIL'}")
            assert g1 < 1e-12 and g2 < 1e-9, "a gate failed - no verdict is read"
        g3max = 0.0
        for g in GROSSES:
            for w in WNAMES:
                rw = ctl[g][0].loc[wspan[w][0]:wspan[w][1]]
                pk, tr, _, _, ddm = ep[(g, w)]
                eq = (1 + rw).cumprod()
                g3max = max(g3max, abs((eq.loc[tr] / eq.loc[pk] - 1.0) - ddm))
        P(f"   G3 every (gross,window) binding episode reproduces its MaxDD: max|d| {g3max:.3e} "
          f"{'PASS' if g3max < 1e-12 else 'FAIL'}")
        assert g3max < 1e-12, "G3 failed - no verdict is read"

        # ---- arms --------------------------------------------------------------------
        g4max = 0.0
        for fam, dials in FAMILIES.items():
            for dial in dials:
                s = gate(px, trade, fam, dial, cache).reindex(px.index).fillna(False)
                for g in GROSSES:
                    rc_u, tn_u, gr_u, Wb = ctl[g]
                    Wa = Wb.mul(s.astype(float), axis=0)
                    rg_a, tn_a, gr_a = fast_run(px, Wa, mask)
                    r_a, tn_a, gr_a = net(rg_a, tn_a).loc[start:], tn_a.loc[start:], gr_a.loc[start:]
                    mg_a, mg_u = float(gr_a.mean()), float(gr_u.mean())
                    c = mg_a / mg_u if mg_u > 0 else 1.0
                    rg_m, tn_m, gr_m = fast_run(px, Wb * c, mask)
                    r_m, gr_m = net(rg_m, tn_m).loc[start:], gr_m.loc[start:]
                    g4max = max(g4max, abs(float(gr_m.mean()) - mg_a))
                    u = (gr_a / gr_u.replace(0, np.nan)).fillna(1.0)
                    in_base = fam in BASE_FAMILIES and dial in BASE_FAMILIES[fam]

                    for w in WNAMES:
                        w0, w1 = wspan[w]
                        ra, ru, rm = r_a.loc[w0:w1], rc_u.loc[w0:w1], r_m.loc[w0:w1]
                        ta, tu = tn_a.loc[w0:w1], tn_u.loc[w0:w1]
                        pk, tr, rcv, recd, _ = ep[(g, w)]
                        nxt = ru.index[ru.index > tr]
                        cov_ep = cover(u, pk, rcv)
                        cov_de = cover(u, pk, tr)
                        cov_re = cover(u, nxt[0], rcv) if len(nxt) and rcv > tr else 0.0
                        ma, mu, mm = metrics(ra), metrics(ru), metrics(rm)
                        fire = float((~s).reindex(ra.index).fillna(False).mean())
                        ws = WS[w]
                        if w == "FULL":
                            Lf = legs_4b(ra, ws["spy"], ra.loc[OOS_START:], ws["spy_oos_sharpe"])
                            Lm = legs_4b(rm, ws["spy"], rm.loc[OOS_START:], ws["spy_oos_sharpe"])
                            oos_a, oos_live = ra.loc[OOS_START:], ws["lv"].loc[OOS_START:]
                            oos_spy_stats = series_stats(ws["sp"].loc[OOS_START:])
                            oos_live_stats = series_stats(oos_live)
                        else:
                            Lf, Lm = legs_4b(ra, ws["spy"]), legs_4b(rm, ws["spy"])
                            oos_a, oos_live = ra.iloc[len(ra)//2:], ws["lv"].iloc[len(ws["lv"])//2:]
                            oos_spy_stats = series_stats(ws["sp"].iloc[len(ws["sp"])//2:])
                            oos_live_stats = series_stats(oos_live)
                        mo = metrics(oos_a)
                        Lo = legs_4b(oos_a, oos_spy_stats)
                        arm_pk, arm_tr, _, _, _ = binding_episode(ra)
                        cells.append(dict(
                            panel=pname, window=w, family=fam, dial=dial, gross=g,
                            confound=(fam == CONFOUND), in_596_corpus=bool(in_base),
                            fire_rate=fire, degenerate=(fire == 0.0), allcash=(fire == 1.0),
                            n_days=len(ra),
                            decline_days=int(((ra.index >= pk) & (ra.index <= tr)).sum()),
                            recovery_days=int(((ra.index > tr) & (ra.index <= rcv)).sum()),
                            long_decline=bool(int(((ra.index >= pk) & (ra.index <= tr)).sum()) > LONG_DECLINE),
                            trough_year=int(tr.year), arm_trough=str(arm_tr.date()),
                            arm_trough_year=int(arm_tr.year),
                            same_episode=bool(arm_tr == tr),
                            mean_gross_arm=mg_a, mean_gross_ctlU=mg_u, match_c=c,
                            CAGR=ma["CAGR"], Sharpe=ma["Sharpe"], MaxDD=ma["MaxDD"],
                            H1=halves(ra)[0], H2=halves(ra)[1],
                            ctlU_CAGR=mu["CAGR"], ctlU_Sharpe=mu["Sharpe"], ctlU_MaxDD=mu["MaxDD"],
                            ctlM_CAGR=mm["CAGR"], ctlM_Sharpe=mm["Sharpe"], ctlM_MaxDD=mm["MaxDD"],
                            ctlM_pass_4b=all(Lm.values()),
                            ctlM_fail_4b="+".join(k for k in KEEP_LEGS if not Lm[k]) or "-none-",
                            dMaxDD_U=ma["MaxDD"] - mu["MaxDD"], dMaxDD_M=ma["MaxDD"] - mm["MaxDD"],
                            tie_U=bool(abs(ma["MaxDD"] - mu["MaxDD"]) <= TIE_EPS),
                            cover_EPISODE=cov_ep, cover_DECLINE=cov_de, cover_RECOVERY=cov_re,
                            switch_DECLINE=switch(ta, tu, pk, tr),
                            switch_EPISODE=switch(ta, tu, pk, rcv), recovered=recd,
                            IS_Sharpe=(metrics(ra.loc[:IS_END])["Sharpe"] if w == "FULL"
                                       else metrics(ra.iloc[:len(ra)//2])["Sharpe"]),
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            turn_per_yr=float(ta.sum() / (len(ra) / 252)),
                            pass_4a=keep_4a(ra, ws["live"]), pass_4b=all(Lf.values()),
                            fail_4b="+".join(k for k in KEEP_LEGS if not Lf[k]) or "-none-",
                            pass_4a_OOS=keep_4a(oos_a, oos_live_stats),
                            pass_4b_OOS=all(Lo.values()),
                            fail_4b_OOS="+".join(k for k, v in Lo.items() if not v) or "-none-"))
        P(f"   G4 matched control's mean gross == arm's: max|d| {g4max:.3e} "
          f"{'PASS' if g4max < 1e-3 else 'FAIL'}")
        assert g4max < 1e-3, "G4 failed - the matched control is not matched"

        # ---- rule 8, both conventions, on this panel ---------------------------------
        cdf = pd.DataFrame([c for c in cells if c["panel"] == pname])
        for w in WNAMES:
            sub_w = cdf[(cdf.window == w) & (~cdf.degenerate)]
            if sub_w.empty:
                continue
            ws = WS[w]
            if w == "FULL":
                oS = series_stats(ws["sp"].loc[OOS_START:])
                oL = series_stats(ws["lv"].loc[OOS_START:])
                conv = "standing 2016/2017"
            else:
                oS = series_stats(ws["sp"].iloc[len(ws["sp"])//2:])
                oL = series_stats(ws["lv"].iloc[len(ws["lv"])//2:])
                conv = "window-local half split"
            for fam in FAMILIES:
                for g in GROSSES:
                    sub = sub_w[(sub_w.family == fam) & (sub_w.gross == g)]
                    if sub.empty or sub.IS_Sharpe.isna().all():
                        continue
                    pick = sub.loc[sub.IS_Sharpe.idxmax()]
                    wfrows.append(dict(panel=pname, window=w, convention=conv, family=fam,
                                       gross=g, dial=pick.dial, IS_Sharpe=pick.IS_Sharpe,
                                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                       OOS_MaxDD=pick.OOS_MaxDD, OOS_4b=pick.pass_4b_OOS,
                                       OOS_4b_fail=pick.fail_4b_OOS, OOS_4a=pick.pass_4a_OOS,
                                       SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"],
                                       SPY_OOS_MaxDD=oS["MaxDD"], V2_OOS_CAGR=oL["CAGR"],
                                       V2_OOS_Sharpe=oL["Sharpe"], V2_OOS_MaxDD=oL["MaxDD"]))
        del px, ctl, WS

    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    E = pd.DataFrame(eprows)
    E.to_csv(f"{OUT}.episodes.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    nd_all = C[~C.degenerate]
    P(f"\n   scored rows: {len(nd_all)} of {len(C)} ({int(C.degenerate.sum())} DEGENERATE - the gate")
    P(f"   never fires in that window, so the arm IS the control and its tie is vacuous).")
    P(f"   of the scored rows, {int(nd_all.allcash.sum())} are ALL-CASH in their window (the gate")
    P(f"   never turns ON): they are kept, never tie, never satisfy the predicate, and their")
    P(f"   Sharpe legs are NaN, so they fail both KEEP paths by construction.  Count disclosed,")
    P(f"   not netted, because the 596/811 corpus is defined on fire_rate == 0 alone (G5).")

    # ================================ G5 reproduction gate ==============================
    P(f"\n{'='*108}")
    P("G5 REPRODUCTION GATE - the 596/811 sub-corpus (4 families x their original 4 dials) on the")
    P("   FULL window must return idea 811's committed reading before the widening is read.")
    P(f"{'='*108}")
    b = nd_all[(nd_all.window == "FULL") & nd_all.in_596_corpus]
    r596 = rates(b, "DECLINE", HEAD_EPS)
    byf = {f: int(((b.family == f) & b.tie_U).sum()) for f in BASE_FAMILIES}
    tgt = dict(n=141, ties=45, nec=1.0, suff=1.0, byf={"SPYTR": 0, "BREADTH": 12, "VOL": 18, "SPYDD": 15})
    checks = [("scored arms", len(b), tgt["n"]), ("MaxDD ties", r596["n_tie"], tgt["ties"]),
              ("necessity P(pred|tie)", r596["P_pred_given_tie"], tgt["nec"]),
              ("sufficiency P(tie|pred)", r596["P_tie_given_pred"], tgt["suff"])]
    g5 = True
    for nm, got, want in checks:
        ok = (abs(got - want) < 1e-12)
        g5 &= ok
        P(f"   {nm:<26} got {got!s:>8}   committed {want!s:>8}   {'PASS' if ok else 'FAIL'}")
    ok = byf == tgt["byf"]
    g5 &= ok
    P(f"   {'ties by family':<26} got {byf}   committed {tgt['byf']}   {'PASS' if ok else 'FAIL'}")
    P(f"   G5 {'PASS' if g5 else 'FAIL'} - the widening does not move idea 811's published cell.")
    assert g5, "G5 failed - this run does not reproduce the corpus it claims to extend"

    # ================================ A. the corpus =====================================
    P(f"\n{'='*108}")
    P(f"A. DOES A QUALIFYING CORPUS EXIST?  (>= {TIE_BAR} ties AND a decline leg > {LONG_DECLINE} trading days)")
    P(f"{'='*108}")
    P(f"   {'window':<8} {'long-decl cells':>16} {'median dec_d':>13} {'median rec_d':>13} "
      f"{'scored':>7} {'ties':>6} {'tie rate':>9} {'#pred':>6} {'FP':>4}")
    for w in WNAMES:
        e = E[E.window == w]
        nd = nd_all[nd_all.window == w]
        r = rates(nd, "DECLINE", HEAD_EPS)
        P(f"   {w:<8} {int(e.long_decline.sum()):>7}/{len(e):<8} {e.decline_days.median():>13.0f} "
          f"{e.recovery_days.median():>13.0f} {len(nd):>7} {r['n_tie']:>6} "
          f"{r['n_tie']/max(len(nd),1):>9.1%} {r['n_pred']:>6} {r['false_pos']:>4}")

    P(f"\n   A2. the (panel, window) CELLS and whether their binding decline is LONG:")
    P(f"   {'panel':<6} {'window':<7} {'dec_d':>7} {'rec_d':>7} {'LONG?':>6} {'scored':>7} "
      f"{'ties':>6} {'#pred':>6} {'FP':>4} {'FP not-SPYDD':>13}")
    long_cells = []
    for pn in ["U56", "B136", "SMALL"]:
        for w in WNAMES:
            e = E[(E.panel == pn) & (E.window == w)]
            nd = nd_all[(nd_all.panel == pn) & (nd_all.window == w)]
            if e.empty:
                continue
            lg = bool(e.long_decline.all())
            r = rates(nd, "DECLINE", HEAD_EPS)
            fpx = nd[pred_mask(nd, "DECLINE", HEAD_EPS) & ~nd.tie_U]
            P(f"   {pn:<6} {w:<7} {e.decline_days.median():>7.0f} {e.recovery_days.median():>7.0f} "
              f"{('LONG' if lg else 'short'):>6} {len(nd):>7} {r['n_tie']:>6} {r['n_pred']:>6} "
              f"{r['false_pos']:>4} {int((~fpx.confound).sum()):>13}")
            if lg:
                long_cells.append((pn, w))
    key = list(zip(nd_all.panel, nd_all.window))
    LC = nd_all[[k in long_cells for k in key]]
    lc_r = rates(LC, "DECLINE", HEAD_EPS) if len(LC) else rates(nd_all.head(0), "DECLINE", HEAD_EPS)
    P(f"\n   LONG-DECLINE CELLS ({len(long_cells)} of {3*len(WNAMES)}): {long_cells}")
    P(f"   pooled QUALIFYING CORPUS: {len(LC)} scored arms, {lc_r['n_tie']} MaxDD ties "
      f"({lc_r['n_tie']/max(len(LC),1):.1%}), {lc_r['n_pred']} satisfy the DECLINE predicate.")
    P(f"   (the pooled corpus re-uses arms across OVERLAPPING windows; that is stated, not netted)")
    if len(LC):
        P(f"   its binding episodes: median decline {LC.decline_days.median():.0f}d vs median "
          f"recovery {LC.recovery_days.median():.0f}d   (FULL reference: "
          f"{nd_all[nd_all.window=='FULL'].decline_days.median():.0f}d / "
          f"{nd_all[nd_all.window=='FULL'].recovery_days.median():.0f}d)")
        P(f"   ties by family: " + "  ".join(
            f"{f}:{int(((LC.family == f) & LC.tie_U).sum())}" for f in FAMILIES))
        P(f"   #pred by family: " + "  ".join(
            f"{f}:{int((pred_mask(LC,'DECLINE',HEAD_EPS) & (LC.family == f)).sum())}" for f in FAMILIES))
    LC.to_csv(f"{OUT}.longcells.csv", index=False)

    # ================================ B. the tuned grid =================================
    P(f"\n{'='*108}")
    P(f"B. THE TUNED GRID - {len(WNAMES)} windows x 2 family sets = {len(WNAMES)*2} POINTS, ALL PRINTED,")
    P(f"   headline cover bar eps = {HEAD_EPS:g}.  Leg split is held at DECLINE (596's) here and the")
    P(f"   other three legs are in .predicates.csv.")
    P(f"{'='*108}")
    POPS = [("ALL", lambda d: d), (f"NO-{CONFOUND}", lambda d: d[~d.confound])]
    for popname, popsel in POPS:
        P(f"\n   family set = {popname}")
        P(f"   {'window':<8} {'scored':>7} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} "
          f"{'P(tie|pred)':>12} {'acc':>7} {'FN':>4} {'FP':>4}  {'exact?':>6}")
        for w in WNAMES:
            d = popsel(nd_all[nd_all.window == w])
            r = rates(d, "DECLINE", HEAD_EPS)
            P(f"   {w:<8} {r['n']:>7} {r['n_pred']:>6} {r['n_tie']:>5} "
              f"{r['P_pred_given_tie']:>12.4f} {r['P_tie_given_pred']:>12.4f} "
              f"{r['accuracy']:>7.4f} {r['false_neg']:>4} {r['false_pos']:>4}  "
              f"{'YES' if r['exact'] else 'no':>6}")
        d = popsel(LC)
        r = rates(d, "DECLINE", HEAD_EPS)
        P(f"   {'QUALIFY':<8} {r['n']:>7} {r['n_pred']:>6} {r['n_tie']:>5} "
          f"{r['P_pred_given_tie']:>12.4f} {r['P_tie_given_pred']:>12.4f} {r['accuracy']:>7.4f} "
          f"{r['false_neg']:>4} {r['false_pos']:>4}  {'YES' if r['exact'] else 'no':>6}   "
          f"<- the pooled long-decline corpus")

    prows = []
    for popname, popsel in POPS:
        for w in WNAMES + ["QUALIFY"]:
            d = popsel(LC if w == "QUALIFY" else nd_all[nd_all.window == w])
            for leg in LEGS_SPLIT:
                for eps in EPS_BAR:
                    prows.append(dict(window=w, family_set=popname, leg_split=leg, eps=eps,
                                      **rates(d, leg, eps)))
    pd.DataFrame(prows).to_csv(f"{OUT}.predicates.csv", index=False)
    P(f"\n   COVER-BAR LADDER (reported axis, not a tune), leg = DECLINE, family set = ALL:")
    P(f"   {'window':<8} " + " ".join(f"{e:>10.0e}" for e in EPS_BAR) +
      "     <- P(tie|pred) ; #pred below")
    for w in WNAMES + ["QUALIFY"]:
        d = LC if w == "QUALIFY" else nd_all[nd_all.window == w]
        rr = [rates(d, "DECLINE", e) for e in EPS_BAR]
        P(f"   {w:<8} " + " ".join(f"{x['P_tie_given_pred']:>10.4f}" for x in rr))
        P(f"   {'':<8} " + " ".join(f"{x['n_pred']:>10d}" for x in rr))

    # ================================ C. the false positives ============================
    P(f"\n{'='*108}")
    P("C. THE FALSE POSITIVES - every arm that holds through the control's decline and STILL does")
    P("   not tie.  This is the whole of the sufficiency question; the family column is the answer.")
    P(f"{'='*108}")
    FP = nd_all[pred_mask(nd_all, "DECLINE", HEAD_EPS) & ~nd_all.tie_U].copy()
    FP.to_csv(f"{OUT}.falsepos.csv", index=False)
    P(f"   {len(FP)} false positives over all {len(nd_all)} scored arm-windows "
      f"({len(nd_all[pred_mask(nd_all,'DECLINE',HEAD_EPS)])} satisfy the predicate).")
    if len(FP):
        P(f"   by family:  " + "  ".join(f"{f}:{int((FP.family == f).sum())}" for f in FAMILIES))
        P(f"   by window:  " + "  ".join(f"{w}:{int((FP.window == w).sum())}" for w in WNAMES))
        P(f"   by panel:   " + "  ".join(f"{p}:{int((FP.panel == p).sum())}" for p in ["U56", "B136", "SMALL"]))
        P(f"   on LONG-decline cells: {int(FP.long_decline.sum())};  of those, "
          f"not-{CONFOUND}: {int((FP.long_decline & ~FP.confound).sum())}")
        P(f"\n   {'panel':<6} {'window':<7} {'family':<8} {'dial':>6} {'g':>5} {'dec_d':>6} "
          f"{'dMaxDD_U':>10} {'ctl trough':>11} {'arm trough':>11} {'fire':>6}")
        for _, r in FP.sort_values(["long_decline", "family"], ascending=[False, True]).head(40).iterrows():
            P(f"   {r.panel:<6} {r.window:<7} {r.family:<8} {r.dial:>6} {r.gross:>5.2f} "
              f"{r.decline_days:>6} {r.dMaxDD_U:>10.2%} {int(r.trough_year):>11} "
              f"{r.arm_trough:>11} {r.fire_rate:>6.1%}")
        P(f"\n   mechanism check - in a false positive the arm's OWN MaxDD sits on a DIFFERENT")
        P(f"   episode than the control's: {int((~FP.same_episode).sum())} of {len(FP)} have a")
        P(f"   different trough date, and the arm is DEEPER in {int((FP.dMaxDD_U < 0).sum())} of {len(FP)}.")
    disagree = {w: int((pred_mask(nd_all[nd_all.window == w], "DECLINE", HEAD_EPS) !=
                        pred_mask(nd_all[nd_all.window == w], "DECLINE+COST", HEAD_EPS)).sum())
                for w in WNAMES}
    P(f"\n   DECLINE vs DECLINE+COST disagreements by window: " +
      "  ".join(f"{w}:{v}" for w, v in disagree.items()))

    # ================================ D. rule 8 =========================================
    P(f"\n{'='*108}")
    P("D. PROTOCOL RULE 8 WALK-FORWARD - (a) the STANDING 2016/2017 split on the FULL window,")
    P("   (b) a WINDOW-LOCAL half split for the short windows (a stated departure, reported")
    P("   beside (a), never instead of it).  Dial chosen on IS by IS Sharpe ALONE; OOS read ONCE.")
    P(f"{'='*108}")
    for w in WNAMES:
        sub = WF[WF.window == w]
        if sub.empty:
            continue
        P(f"\n   window {w}  ({sub.iloc[0].convention})")
        P(f"   {'panel':<6} {'family':<8} {'g':>5} {'dial':>6} {'ISSh':>6} {'OOSCAGR':>9} "
          f"{'OOSSh':>7} {'OOSDD':>8}  {'fail4b(OOS)':<18} {'4bOOS':>6} {'4aOOS':>6}")
        for _, r in sub.iterrows():
            P(f"   {r.panel:<6} {r.family:<8} {r.gross:>5.2f} {r.dial:>6} {r.IS_Sharpe:>6.3f} "
              f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%}  "
              f"{r.OOS_4b_fail:<18} {'PASS' if r.OOS_4b else 'fail':>6} "
              f"{'PASS' if r.OOS_4a else 'fail':>6}")
        P(f"   comparands on this OOS window, per panel:")
        for p in ["U56", "B136", "SMALL"]:
            s = sub[sub.panel == p]
            if s.empty:
                continue
            r = s.iloc[0]
            P(f"      {p:<6} SPY {r.SPY_OOS_CAGR:>7.2%} / {r.SPY_OOS_Sharpe:.3f} / "
              f"{r.SPY_OOS_MaxDD:>7.2%}      RULES v2 {r.V2_OOS_CAGR:>7.2%} / "
              f"{r.V2_OOS_Sharpe:.3f} / {r.V2_OOS_MaxDD:>7.2%}")
        P(f"   rule-8 picks passing 4b OOS: {int(sub.OOS_4b.sum())} of {len(sub)};  "
          f"4a OOS: {int(sub.OOS_4a.sum())} of {len(sub)}")

    P(f"\n   BOTH KEEP PATHS over all scored arms, per window:")
    P(f"   {'window':<8} {'scored':>7} {'4a':>5} {'4b':>5} {'4a OOS':>7} {'4b OOS':>7} "
      f"{'BOTH':>5} {'4b & 4bOOS':>11} {'... & beats ctlM':>17}")
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        both = int((nd.pass_4b & nd.pass_4b_OOS & ~nd.ctlM_pass_4b).sum())
        P(f"   {w:<8} {len(nd):>7} {int(nd.pass_4a.sum()):>5} {int(nd.pass_4b.sum()):>5} "
          f"{int(nd.pass_4a_OOS.sum()):>7} {int(nd.pass_4b_OOS.sum()):>7} "
          f"{int((nd.pass_4a & nd.pass_4b).sum()):>5} "
          f"{int((nd.pass_4b & nd.pass_4b_OOS).sum()):>11} {both:>17}")
    P("   binding 4b leg (most common first), FULL window:")
    for k, v in nd_all[nd_all.window == 'FULL'].fail_4b.value_counts().head(8).items():
        P(f"      {k:<24} {v:>4}")
    P(f"\n   4b passers read against CONTROL-M (the same book holding uniformly less, no timing):")
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        pas = nd[nd.pass_4b]
        if pas.empty:
            P(f"   window {w}: no 4b passers.")
            continue
        clean = pas[pas.pass_4b & pas.pass_4b_OOS & ~pas.ctlM_pass_4b]
        P(f"   window {w}: {len(pas)} pass 4b; {int(pas.ctlM_pass_4b.sum())} of them are matched by "
          f"their own CONTROL-M (pass = exposure, not the clause); {len(clean)} clear BOTH windows "
          f"AND beat CONTROL-M.")
        for _, r in clean.head(8).iterrows():
            P(f"      {r.panel} {r.family} dial={r.dial} g={r.gross:.2f}  "
              f"{r.CAGR:.2%}/{r.Sharpe:.3f}/{r.MaxDD:.2%}  ctlM {r.ctlM_CAGR:.2%}/"
              f"{r.ctlM_Sharpe:.3f}/{r.ctlM_MaxDD:.2%}  turn {r.turn_per_yr:.2f}x/yr")

    # ================================ E. hypotheses =====================================
    NA = None
    lcx = LC[~LC.confound] if len(LC) else LC
    lcx_r = rates(lcx, "DECLINE", HEAD_EPS) if len(lcx) else dict(n_tie=0, n_pred=0, false_pos=0,
                                                                  P_pred_given_tie=np.nan,
                                                                  P_tie_given_pred=np.nan)
    HAVE_PRED = lc_r["n_pred"] > 0
    HAVE_TIES = lc_r["n_tie"] > 0
    full_tie_rate = float(nd_all[nd_all.window == "FULL"].tie_U.mean())
    lc_tie_rate = float(LC.tie_U.mean()) if len(LC) else np.nan
    fp_long_nonconf = int((FP.long_decline & ~FP.confound).sum()) if len(FP) else 0
    pred_all = nd_all[pred_mask(nd_all, "DECLINE", HEAD_EPS)]
    conf_share_pred = float(pred_all.confound.mean()) if len(pred_all) else np.nan
    conf_share_fp = float(FP.confound.mean()) if len(FP) else np.nan

    H = [("H_CORPUS  a long-decline corpus with >= 30 MaxDD ties EXISTS",
          bool(lc_r["n_tie"] >= TIE_BAR)),
         (f"H_CORPUSX the same corpus still carries >= 30 ties with {CONFOUND} dropped",
          bool(lcx_r["n_tie"] >= TIE_BAR)),
         ("H_PRED    that corpus carries >= 30 arms satisfying the DECLINE predicate",
          bool(lc_r["n_pred"] >= PRED_BAR)),
         ("H_NEC     necessity P(pred|tie) = 1.0000 there (the construction leg)",
          bool(lc_r["P_pred_given_tie"] == 1.0) if HAVE_TIES else NA),
         ("H_SUFF    sufficiency P(tie|pred) = 1.0000 there, ALL families (596's claim)",
          bool(lc_r["P_tie_given_pred"] == 1.0) if HAVE_PRED else NA),
         (f"H_BREAK   sufficiency BREAKS OUTSIDE {CONFOUND} on that corpus [LOAD-BEARING]",
          bool(fp_long_nonconf > 0) if HAVE_PRED else NA),
         (f"H_CONFSHR {CONFOUND}'s share of false positives exceeds its share of #pred",
          bool(conf_share_fp > conf_share_pred) if len(FP) else NA),
         ("H_LONG    the tie RATE on long-decline cells is below the FULL window's",
          bool(lc_tie_rate < full_tie_rate) if len(LC) else NA),
         ("H_COST    DECLINE and DECLINE+COST agree on every scored cell, every window",
          all(v == 0 for v in disagree.values()))]

    P(f"\n{'='*108}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*108}")
    P(f"   corpus for H_NEC / H_SUFF / H_BREAK / H_LONG: the pooled long-decline cells")
    P(f"   ({len(long_cells)} (panel,window) cells, {len(LC)} scored arms, {lc_r['n_tie']} ties, "
      f"{lc_r['n_pred']} predicate arms).")
    for nm, v in H:
        P(f"   {nm:<72} {'N/A - empty population' if v is NA else ('PASS' if v else 'FAIL')}")
    ev = [v for _, v in H if v is not NA]
    nna = sum(1 for _, v in H if v is NA)
    P(f"\n   {sum(bool(v) for v in ev)} of {len(ev)} EVALUABLE pre-registered hypotheses pass"
      + (f"; {nna} of {len(H)} are NOT EVALUABLE (empty population)." if nna else "."))
    P(f"\n   POWER, stated with the result: qualifying corpus {len(LC)} scored arms, "
      f"{lc_r['n_tie']} ties ({lc_tie_rate:.1%}), {lc_r['n_pred']} predicate arms, "
      f"{lc_r['false_pos']} false positives")
    P(f"   ({int((FP.long_decline & ~FP.confound).sum()) if len(FP) else 0} of them outside "
      f"{CONFOUND}).  FULL window for reference: "
      f"{int(nd_all[nd_all.window=='FULL'].tie_U.sum())} ties in "
      f"{int((nd_all.window=='FULL').sum())} ({full_tie_rate:.1%}).")
    P(f"   {CONFOUND} share of #pred {conf_share_pred:.4f} vs its share of false positives "
      f"{conf_share_fp:.4f} (over ALL windows).")
    P(f"\n   SUFFICIENCY, the number the idea asks for, on every corpus this run built:")
    P(f"   {'corpus':<26} {'ALL families':>28} {'NO-'+CONFOUND:>28}")
    for nm, d in [("FULL (596/811 reference)", nd_all[nd_all.window == "FULL"]),
                  ("POST20 (811's break)", nd_all[nd_all.window == "POST20"]),
                  ("pooled long-decline", LC),
                  ("all windows pooled", nd_all)]:
        a, x = rates(d, "DECLINE", HEAD_EPS), rates(d[~d.confound], "DECLINE", HEAD_EPS)
        P(f"   {nm:<26} {a['P_tie_given_pred']:>12.4f} (n_pred {a['n_pred']:>4}, FP {a['false_pos']:>3}) "
          f"{x['P_tie_given_pred']:>12.4f} (n_pred {x['n_pred']:>4}, FP {x['false_pos']:>3})")

    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, E=E, WF=WF, LC=LC, FP=FP, H=H)


if __name__ == "__main__":
    main()
