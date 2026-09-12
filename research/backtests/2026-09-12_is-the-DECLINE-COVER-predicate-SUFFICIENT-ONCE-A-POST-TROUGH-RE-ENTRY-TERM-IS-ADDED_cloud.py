#!/usr/bin/env python3
"""Idea 817 - is the DECLINE COVER predicate SUFFICIENT once a POST-TROUGH RE-ENTRY term is added?
   (cloud lane, 2026-09-12, idea 1 of 2)

QUESTION (QUEUE idea 817, verbatim)
    Idea 813 broke 596's sufficiency leg with 5 distinct configurations and every one has the same
    shape: the gate sits out the control's decline, fires AFTER the trough, and rides a later
    decline deeper (arm deeper than control in 15 of 15, different trough date in 12 of 15).  Add
    a post-trough re-entry term to the predicate (cover(DECLINE) = 0 AND no de-gross in the k days
    after the trough, k a reported axis) and measure whether sufficiency returns to 1.0000 without
    the term becoming a second tune.  Max 2 params (k, family set).

WHAT "WITHOUT BECOMING A SECOND TUNE" HAS TO MEAN, STATED BEFORE ANYTHING IS RUN
    Adding a conjunct can only SHRINK the predicate population, so sufficiency P(tie|pred) is
    purchasable at will: take k large enough and #pred collapses onto the arms that never de-gross
    at all, which ARE the control and tie trivially.  A term that buys sufficiency that way has
    bought nothing.  The claim is therefore only interesting if all four of these hold at the SAME
    rung, and each is a separate pre-registered bar:
      (1) SUFFICIENCY  P(tie | DECLINE+POST_k) = 1.0000 on the qualifying corpus;
      (2) POWER        #pred >= 30 there - the queue's own power bar, unchanged;
      (3) NECESSITY    P(DECLINE+POST_k | tie) = 1.0000 - the term throws away NO true tie.  This
                       is the LOAD-BEARING one.  Necessity of the bare DECLINE predicate is near
                       identity by construction; if the POST term costs necessity, then it is not
                       a missing term in the predicate, it is a filter fitted to the false
                       positives, i.e. exactly the "second tune" the queue forbids;
      (4) NON-TRIVIAL  #pred strictly exceeds the number of arms whose de-gross cover over the
                       WHOLE window is zero - the term must not reduce the predicate to "the arm
                       is the control".
    HEADLINE k IS CHOSEN BY A RULE DECLARED HERE, NOT BY LOOKING: the SMALLEST rung of the ladder
    at which (1) and (2) both hold with ALL families.  If no rung does, that is reported and no
    rung is promoted.

THE CORPUS (idea 813's, rebuilt bit-for-bit, so every number is directly comparable)
    book      B(g) = the LIVE form, baseline.rules_v2_weights: hold every name inside its 200d
              +/-3% band at g/N of NAV, gated-out weight to CASH, weekly, next-day fill, 10 bps.
    clause    a MARKET-level gate s_t in {0,1}; gate OFF => the book is de-grossed to cash that
              week (k = 0, never re-spread).  arm = B(g) * s.
    controls  CONTROL-U = B(g) at nominal gross (the comparand the tie label is defined against),
              CONTROL-M = B(g) * c, c set so mean realised gross equals the arm's.
    families  SPYTR / BREADTH / VOL / SPYDD / CORR / DISP, 5 dials each (813's widened ladder).
              SPYDD is the NAMED CONFOUND; every rate is reported again with it dropped.
    panels    U56, B136, SMALL (sub-$2B, tickers with max_1d_move >= 1.0 dropped first).
    gross     g in {0.50, 0.75, 1.00}.   6 x 5 x 3 = 90 arms per panel, 270 in all, ALL reported.
    windows   the same 7 evaluation windows; a window never slices the data, only the return path.
    QUALIFYING CORPUS = the pooled (panel, window) cells whose CONTROL-U binding decline leg
              exceeds 60 trading days - 813 measured this at 14 of 21 cells, 897 scored arms,
              111 ties, 114 DECLINE-predicate arms, P(tie|DECLINE) = 0.9737 with 3 false positives.
              Reproducing that cell exactly is gate G5b; nothing is read until it passes.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) k, the POST-TROUGH WINDOW: {5, 10, 21, 42, 63, 126, 252, REC, ALL} trading days after the
        control's trough.  REC = trough+1 .. the control's recovery date (813's RECOVERY leg,
        carried so the new ladder nests the old reading).  ALL = trough+1 .. window end, the
        degenerate end of the ladder, printed precisely so the trivialisation is visible.
    (2) FAMILY SET: ALL (6 families) vs NO-SPYDD (5, the confound dropped).
    9 x 2 = 18 grid points, EVERY ONE printed and written to .predicates.csv.
    COVER BAR is NOT a third tune: headline eps = 0, the ladder {0, 1e-12, 1e-6, 1e-4, 1e-3}
    printed in full as a reported robustness axis, as 596/811/813 did.
    PRE-PEAK COVER is a reported DIAGNOSTIC, never a conjunct: it is how a surviving false
    positive is explained, not how one is removed.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_REPRO   the rebuilt corpus reproduces 813's committed long-decline cell (897 scored arms,
              111 ties, 114 predicate arms, P(tie|DECLINE) = 0.9737, 3 false positives) and its
              596/811 sub-corpus (141 arms, 45 ties, 1.0000 / 1.0000).  Gate, not evidence.
    H_SUFF1   some rung k of the ladder returns P(tie | DECLINE+POST_k) = 1.0000 on the
              qualifying corpus with ALL families.
    H_POWER   at the headline rung, #pred >= 30.
    H_NEC1    at the headline rung, necessity P(DECLINE+POST_k | tie) = 1.0000 - the term
              excludes no true tie.  [LOAD-BEARING: FAIL here means the term is a second tune.]
    H_PLATEAU at least TWO ADJACENT rungs deliver sufficiency 1.0000 with #pred >= 30 - a single
              qualifying rung is a knife edge, not a term.
    H_ALLFP   the headline rung excludes ALL 15 false positives 813 found over ALL windows, not
              only the 3 on the qualifying corpus.
    H_NONTRIV at the headline rung, #pred is strictly greater than the number of arms whose cover
              over the WHOLE window is zero (the predicate is not "arm == control").
    H_NOSPYDD sufficiency is also 1.0000 at the headline rung with the confound family dropped.
    H_COST    the switch-cost term still adds nothing: DECLINE+POST_k and DECLINE+POST_k+COST
              agree on every scored cell of every window (811/813 both read 0 disagreements).
    H_MONO    #pred is monotone non-increasing along the k ladder (a sanity leg: the conjunct can
              only remove arms; a violation means the cover windows are mis-built).

GATES (printed first; all must pass before any verdict is read)
    G1  the arm at a never-firing gate is EXACTLY CONTROL-U.
    G2  the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G3  in EVERY (panel, gross, window) the located binding episode reproduces that window's
        MaxDD to <= 1e-12.
    G4  CONTROL-M's realised mean gross equals the arm's to <= 1e-3.
    G5a REPRODUCTION: the 596/811 sub-corpus on FULL returns 141 arms, 45 ties, necessity 1.0000,
        sufficiency 1.0000, ties by family SPYTR 0 / BREADTH 12 / VOL 18 / SPYDD 15.
    G5b REPRODUCTION: 813's qualifying corpus - 14 long-decline cells, 897 scored arms, 111 ties,
        114 predicate arms, sufficiency 0.9737, 3 false positives; 15 false positives over all
        windows split CORR 9 / VOL 3 / SPYDD 3.
    G6  NESTING: POST_REC reproduces 813's RECOVERY leg exactly on every scored cell.

PROTOCOL RULE 8 (mandatory, run and reported):
    (a) STANDING convention - per (panel, family, gross) the DIAL is chosen on IS (..2016-12-31)
        by IS Sharpe alone, OOS (2017-01-01..) read exactly ONCE, reported as CAGR/Sharpe/MaxDD
        against RULES v2 and SPY on the same window.  Both KEEP paths evaluated on all 270 arms.
    (b) WINDOW-LOCAL - a window ending in 2012 has no 2017+ out-of-sample, so for every non-FULL
        window the dial is also chosen on its FIRST HALF and read once on its SECOND HALF.  A
        stated DEPARTURE from the record's 2016/2017 split, reported beside (a), never instead.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and the SMALL panel worst (a sub-$2B screen read today cannot see the names that
    fell out of it - data/SMALL_PANEL_README.md).  The predicate rates are within-panel agreement
    rates, which survivorship moves far less than levels.  Several windows are 3-5 years and sit
    wholly inside a bull leg, so no Sharpe or CAGR read off them is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .cells.csv       one row per (arm, window): metrics, tie label, every cover leg, 4a/4b
    .predicates.csv  the 9 x 2 tuned grid x the 5-rung cover ladder, all points
    .kladder.csv     the k ladder on every corpus, with #pred / necessity / sufficiency / FP
    .falsepos.csv    every false positive of DECLINE and of DECLINE+POST_headline, with family
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
SLUG = "is-the-DECLINE-COVER-predicate-SUFFICIENT-ONCE-A-POST-TROUGH-RE-ENTRY-TERM-IS-ADDED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ = "W"
LAG = 1
COST = 10
BAND = 0.03
GROSSES = [0.50, 0.75, 1.00]
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SMALL_MAXMOVE = 1.0
LIVE_GROSS = 0.75

WINDOWS = [("FULL",   None,         None),
           ("PRE20",  None,         "2019-12-31"),
           ("E2011",  None,         "2012-12-31"),
           ("E2015",  "2013-01-01", "2017-12-31"),
           ("E2018",  "2016-01-01", "2019-12-31"),
           ("POST20", "2020-07-01", None),
           ("BEAR22", "2021-01-01", "2024-12-31")]
WNAMES = [w[0] for w in WINDOWS]

# tuned dial 1: the POST-TROUGH window.  REC and ALL are the two named ends of the ladder.
KLADDER = [5, 10, 21, 42, 63, 126, 252, "REC", "ALL"]
EPS_BAR = [0.0, 1e-12, 1e-6, 1e-4, 1e-3]
HEAD_EPS = 0.0
TIE_EPS = 1e-12
LONG_DECLINE = 60
TIE_BAR = 30
PRED_BAR = 30

FAMILIES = {
    "SPYTR":   [50, 100, 150, 200, 250],
    "BREADTH": [0.05, 0.20, 0.35, 0.50, 0.65],
    "VOL":     [0.15, 0.25, 0.40, 0.60, 0.90],
    "SPYDD":   [0.05, 0.10, 0.20, 0.35, 0.45],
    "CORR":    [0.20, 0.30, 0.40, 0.55, 0.75],
    "DISP":    [0.10, 0.15, 0.20, 0.30, 0.50],
}
BASE_FAMILIES = {"SPYTR": [100, 150, 200, 250], "BREADTH": [0.20, 0.35, 0.50, 0.65],
                 "VOL": [0.15, 0.25, 0.40, 0.60], "SPYDD": [0.05, 0.10, 0.20, 0.35]}
CONFOUND = "SPYDD"
KEEP_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
CORR_W = 60
DISP_W = 60

# idea 813's committed readings, used as reproduction gates G5a / G5b
T813_596 = dict(n=141, ties=45, nec=1.0, suff=1.0,
                byf={"SPYTR": 0, "BREADTH": 12, "VOL": 18, "SPYDD": 15})
T813_LONG = dict(cells=14, n=897, ties=111, npred=114, suff=0.9737, fp=3)
T813_FPALL = dict(total=15, byfam={"CORR": 9, "VOL": 3, "SPYDD": 3})

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def kcol(k):
    return f"cover_POST_{k}"


# ------------------------------------------------------------------ runner (596/804/811/813's)
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


# ------------------------------------------------------------------ episodes and cover legs
def binding_episode(r: pd.Series):
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
    if lo is None or hi is None or hi < lo:
        return 0.0
    w = u.loc[lo:hi]
    if len(w) == 0:
        return 0.0
    return float((1.0 - w).clip(lower=0.0).mean())


def switch(tn_arm: pd.Series, tn_ctl: pd.Series, lo, hi):
    if lo is None or hi is None or hi < lo:
        return 0.0
    a, c = tn_arm.loc[lo:hi], tn_ctl.loc[lo:hi]
    return float(np.abs(a - c).sum())


def post_bounds(idx: pd.DatetimeIndex, trough, recovery, k):
    """[lo, hi] of the POST-TROUGH window for rung k, within the evaluation window idx."""
    tpos = int(idx.get_indexer([trough])[0])
    if tpos < 0 or tpos + 1 >= len(idx):
        return None, None                      # trough is the last scored day: vacuously clean
    lo = idx[tpos + 1]
    if k == "ALL":
        return lo, idx[-1]
    if k == "REC":
        return (lo, recovery) if recovery > trough else (None, None)
    return lo, idx[min(tpos + int(k), len(idx) - 1)]


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


# ------------------------------------------------------------------ predicates
def pred_mask(df, leg, eps):
    """leg is 'DECLINE', 'RECOVERY', 'EPISODE', or 'POST:<k>' / 'POST:<k>+COST'."""
    if leg == "EPISODE":
        return df.cover_EPISODE <= eps
    if leg == "DECLINE":
        return df.cover_DECLINE <= eps
    if leg == "RECOVERY":
        return df.cover_RECOVERY <= eps
    if leg == "DECLINE+COST":
        return (df.cover_DECLINE <= eps) & (df.switch_DECLINE <= eps)
    if leg.startswith("POST:"):
        body = leg[5:]
        cost = body.endswith("+COST")
        k = body[:-5] if cost else body
        m = (df.cover_DECLINE <= eps) & (df[kcol(k)] <= eps)
        if cost:
            m = m & (df.switch_DECLINE <= eps)
        return m
    raise ValueError(leg)


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
    P(f"# Idea 817 - {SLUG}  (cloud, {DATE})")
    P("# Object: idea 813 broke 596's sufficiency leg with 15 false positives whose shape it named")
    P("# - hold through the control's decline, de-gross AFTER the trough, ride a later decline")
    P("# deeper.  817 asks whether the predicate's MISSING TERM is a post-trough re-entry clause.")
    P(f"# TUNED: k {KLADDER} x family set [ALL, NO-{CONFOUND}] = {len(KLADDER)*2} points, ALL reported.")
    P(f"# Cover bar is NOT a third tune: headline eps = {HEAD_EPS:g}, ladder {EPS_BAR} printed in full.")
    P("# HEADLINE RUNG IS RULE-CHOSEN, NOT PICKED: smallest k with sufficiency 1.0000 AND")
    P(f"#   #pred >= {PRED_BAR} on the qualifying corpus, ALL families.  If none, none is promoted.")
    P("# A term that buys sufficiency by COSTING NECESSITY is a second tune, not a missing term;")
    P("# H_NEC1 is the load-bearing bar and it is stated in the direction that would falsify 817.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")

    cells, eprows, wfrows = [], [], []

    for pname in ["U56", "B136", "SMALL"]:
        P(f"\n{'='*112}\nPANEL {pname}\n{'='*112}")
        px = panel(pname)
        trade = [c for c in px.columns if c != "SPY"]
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        R = px[trade].pct_change()
        cache = {"corr": avg_pair_corr(R).reindex(px.index),
                 "disp": (px[trade] / px[trade].shift(DISP_W) - 1.0).std(axis=1).reindex(px.index)}
        P(f"   {len(trade)} tradeable names, {len(px.loc[start:])} scored days "
          f"{start.date()}..{px.index[-1].date()}")

        wspan = {nm: (start if s is None else max(start, pd.Timestamp(s)),
                      px.index[-1] if e is None else min(px.index[-1], pd.Timestamp(e)))
                 for nm, s, e in WINDOWS}

        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        live_rg, live_tn, _ = fast_run(px, rules_v2_weights(px, band=BAND, gross=LIVE_GROSS), mask)
        live_full = net(live_rg, live_tn).loc[start:]

        WS = {}
        for w in WNAMES:
            w0, w1 = wspan[w]
            sp, lv = spy_full.loc[w0:w1], live_full.loc[w0:w1]
            WS[w] = dict(spy=series_stats(sp), live=series_stats(lv), sp=sp, lv=lv,
                         spy_oos_sharpe=(metrics(sp.loc[OOS_START:])["Sharpe"]
                                         if w == "FULL" else np.nan))

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
                                   days_after_trough=int((rw.index > tr).sum()),
                                   long_decline=bool(dd_days > LONG_DECLINE)))
        P(f"\n   CONTROL-U binding episodes by (gross, window), with the room the POST term has:")
        P(f"   {'g':>5} {'window':<7} {'days':>5} {'MaxDD':>8} {'peak':>11} {'trough':>11} "
          f"{'dec_d':>6} {'rec_d':>6} {'after_tr':>9} {'>60d?':>6}")
        for e in [e for e in eprows if e["panel"] == pname]:
            P(f"   {e['gross']:>5.2f} {e['window']:<7} {e['n_days']:>5} {e['MaxDD']:>8.2%} "
              f"{str(e['peak']):>11} {str(e['trough']):>11} {e['decline_days']:>6} "
              f"{e['recovery_days']:>6} {e['days_after_trough']:>9} "
              f"{'LONG' if e['long_decline'] else 'short':>6}"
              f"{'' if e['recovered'] else '  (NEVER RECOVERED - flagged)'}")

        # ---- gates G1..G3 ------------------------------------------------------------
        if pname == "U56":
            P(f"\n{'-'*112}\nGATES\n{'-'*112}")
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
                        idx = ra.index
                        nxt = idx[idx > tr]
                        cov_ep = cover(u, pk, rcv)
                        cov_de = cover(u, pk, tr)
                        cov_re = cover(u, nxt[0], rcv) if len(nxt) and rcv > tr else 0.0
                        # the POST-TROUGH ladder (tuned dial 1)
                        post = {}
                        for k in KLADDER:
                            lo, hi = post_bounds(idx, tr, rcv, k)
                            post[kcol(k)] = cover(u, lo, hi)
                        # reported DIAGNOSTICS, never conjuncts
                        ppos = int(idx.get_indexer([pk])[0])
                        cov_pre = cover(u, idx[0], idx[ppos - 1]) if ppos > 0 else 0.0
                        cov_win = cover(u, idx[0], idx[-1])
                        ma, mu, mm = metrics(ra), metrics(ru), metrics(rm)
                        fire = float((~s).reindex(idx).fillna(False).mean())
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
                            decline_days=int(((idx >= pk) & (idx <= tr)).sum()),
                            recovery_days=int(((idx > tr) & (idx <= rcv)).sum()),
                            days_after_trough=int((idx > tr).sum()),
                            long_decline=bool(int(((idx >= pk) & (idx <= tr)).sum()) > LONG_DECLINE),
                            trough_year=int(tr.year), ctl_trough=str(tr.date()),
                            arm_trough=str(arm_tr.date()), arm_trough_year=int(arm_tr.year),
                            arm_peak=str(arm_pk.date()),
                            same_episode=bool(arm_tr == tr),
                            arm_dd_before_ctl_peak=bool(arm_tr < pk),
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
                            cover_PREPEAK=cov_pre, cover_WINDOW=cov_win, **post,
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
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    nd_all = C[~C.degenerate]
    P(f"\n   scored rows: {len(nd_all)} of {len(C)} ({int(C.degenerate.sum())} DEGENERATE - the gate")
    P(f"   never fires in that window, so the arm IS the control and its tie is vacuous).")
    P(f"   {int(nd_all.allcash.sum())} of the scored rows are ALL-CASH in their window; kept and")
    P(f"   disclosed, never netted, because the 596/811/813 corpus is defined on fire_rate == 0.")

    # ================================ G5 / G6 reproduction ==============================
    P(f"\n{'='*112}")
    P("G5 REPRODUCTION GATES - nothing below is read until this run reproduces idea 813's")
    P("   committed cells exactly.  G5a is the 596/811 sub-corpus, G5b the qualifying corpus.")
    P(f"{'='*112}")
    b = nd_all[(nd_all.window == "FULL") & nd_all.in_596_corpus]
    r596 = rates(b, "DECLINE", HEAD_EPS)
    byf = {f: int(((b.family == f) & b.tie_U).sum()) for f in BASE_FAMILIES}
    g5 = True
    for nm, got, want in [("scored arms", len(b), T813_596["n"]),
                          ("MaxDD ties", r596["n_tie"], T813_596["ties"]),
                          ("necessity P(pred|tie)", r596["P_pred_given_tie"], T813_596["nec"]),
                          ("sufficiency P(tie|pred)", r596["P_tie_given_pred"], T813_596["suff"])]:
        ok = abs(got - want) < 1e-12
        g5 &= ok
        P(f"   G5a {nm:<24} got {got!s:>8}   committed {want!s:>8}   {'PASS' if ok else 'FAIL'}")
    ok = byf == T813_596["byf"]
    g5 &= ok
    P(f"   G5a {'ties by family':<24} got {byf}   {'PASS' if ok else 'FAIL'}")

    # qualifying corpus, built exactly as 813 did
    long_cells = []
    for pn in ["U56", "B136", "SMALL"]:
        for w in WNAMES:
            e = E[(E.panel == pn) & (E.window == w)]
            if not e.empty and bool(e.long_decline.all()):
                long_cells.append((pn, w))
    key = list(zip(nd_all.panel, nd_all.window))
    LC = nd_all[[k in long_cells for k in key]].copy()
    lc_r = rates(LC, "DECLINE", HEAD_EPS)
    FP_DEC = nd_all[pred_mask(nd_all, "DECLINE", HEAD_EPS) & ~nd_all.tie_U].copy()
    fp_byfam = {f: int((FP_DEC.family == f).sum()) for f in FAMILIES if (FP_DEC.family == f).any()}
    for nm, got, want in [("long-decline cells", len(long_cells), T813_LONG["cells"]),
                          ("scored arms", len(LC), T813_LONG["n"]),
                          ("MaxDD ties", lc_r["n_tie"], T813_LONG["ties"]),
                          ("DECLINE-predicate arms", lc_r["n_pred"], T813_LONG["npred"]),
                          ("sufficiency (4dp)", round(lc_r["P_tie_given_pred"], 4), T813_LONG["suff"]),
                          ("false positives", lc_r["false_pos"], T813_LONG["fp"])]:
        ok = abs(got - want) < 1e-9
        g5 &= ok
        P(f"   G5b {nm:<24} got {got!s:>8}   committed {want!s:>8}   {'PASS' if ok else 'FAIL'}")
    ok = (len(FP_DEC) == T813_FPALL["total"]) and (fp_byfam == T813_FPALL["byfam"])
    g5 &= ok
    P(f"   G5b {'FP over all windows':<24} got {len(FP_DEC)} {fp_byfam}   "
      f"committed {T813_FPALL['total']} {T813_FPALL['byfam']}   {'PASS' if ok else 'FAIL'}")
    g6 = float(np.abs(nd_all[kcol('REC')] - nd_all.cover_RECOVERY).max())
    P(f"   G6  POST_REC nests 813's RECOVERY leg: max|d| {g6:.3e} {'PASS' if g6 < 1e-12 else 'FAIL'}")
    g5 &= g6 < 1e-12
    P(f"   G5/G6 {'PASS' if g5 else 'FAIL'} - this run stands on 813's corpus, not a new one.")
    assert g5, "a reproduction gate failed - this run does not reproduce the corpus it extends"

    # ================================ A. the k ladder ===================================
    P(f"\n{'='*112}")
    P("A. THE TUNED GRID - k ladder x family set, ALL 18 POINTS PRINTED, on every corpus.")
    P(f"   predicate = cover(DECLINE) <= {HEAD_EPS:g} AND cover(trough+1 .. trough+k) <= {HEAD_EPS:g}")
    P(f"   k = REC stops at the control's recovery date; k = ALL runs to the window end (the")
    P("   degenerate end, printed so the trivialisation is visible rather than hidden).")
    P(f"{'='*112}")
    CORPORA = [("QUALIFY (long-decline)", LC),
               ("FULL (596/811 reference)", nd_all[nd_all.window == "FULL"]),
               ("POST20 (811's break)", nd_all[nd_all.window == "POST20"]),
               ("ALL WINDOWS POOLED", nd_all)]
    POPS = [("ALL", lambda d: d), (f"NO-{CONFOUND}", lambda d: d[~d.confound])]
    krows = []
    for cname, cdf0 in CORPORA:
        for popname, popsel in POPS:
            d = popsel(cdf0)
            P(f"\n   corpus {cname}   family set {popname}   (n {len(d)}, ties {int(d.tie_U.sum())})")
            P(f"   {'leg':<14} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} {'P(tie|pred)':>12} "
              f"{'FN':>4} {'FP':>4} {'both=1?':>8}")
            for leg, lab in ([("DECLINE", "DECLINE (813)")] +
                             [(f"POST:{k}", f"+POST k={k}") for k in KLADDER]):
                r = rates(d, leg, HEAD_EPS)
                krows.append(dict(corpus=cname, family_set=popname, leg=lab, k=(
                    "-" if leg == "DECLINE" else leg[5:]), **r))
                P(f"   {lab:<14} {r['n_pred']:>6} {r['n_tie']:>5} "
                  f"{r['P_pred_given_tie']:>12.4f} {r['P_tie_given_pred']:>12.4f} "
                  f"{r['false_neg']:>4} {r['false_pos']:>4} "
                  f"{('YES' if r['exact'] else 'no'):>8}")
    KL = pd.DataFrame(krows)
    KL.to_csv(f"{OUT}.kladder.csv", index=False)

    prows = []
    for cname, cdf0 in CORPORA:
        for popname, popsel in POPS:
            d = popsel(cdf0)
            for leg in (["DECLINE", "RECOVERY", "EPISODE", "DECLINE+COST"] +
                        [f"POST:{k}" for k in KLADDER] + [f"POST:{k}+COST" for k in KLADDER]):
                for eps in EPS_BAR:
                    prows.append(dict(corpus=cname, family_set=popname, leg=leg, eps=eps,
                                      **rates(d, leg, eps)))
    pd.DataFrame(prows).to_csv(f"{OUT}.predicates.csv", index=False)

    # ---- the rule-chosen headline rung ----------------------------------------------
    P(f"\n{'-'*112}")
    P(f"   HEADLINE RUNG by the PRE-STATED rule: smallest k with sufficiency == 1.0000 AND")
    P(f"   #pred >= {PRED_BAR} on QUALIFY with ALL families.")
    qual = []
    for k in KLADDER:
        r = rates(LC, f"POST:{k}", HEAD_EPS)
        qual.append((k, r))
    ok_rungs = [k for k, r in qual if r["P_tie_given_pred"] == 1.0 and r["n_pred"] >= PRED_BAR]
    suff1_rungs = [k for k, r in qual if r["P_tie_given_pred"] == 1.0]
    HEAD_K = ok_rungs[0] if ok_rungs else (suff1_rungs[0] if suff1_rungs else None)
    if ok_rungs:
        P(f"   rungs meeting BOTH bars: {ok_rungs}   -> HEADLINE k = {HEAD_K}")
    elif suff1_rungs:
        P(f"   NO rung meets both bars.  Rungs reaching sufficiency 1.0000 at all: {suff1_rungs} "
          f"(all UNDERPOWERED, #pred < {PRED_BAR}).")
        P(f"   The smallest of them, k = {HEAD_K}, is carried ONLY to report what it costs; it is "
          f"NOT promoted.")
    else:
        P(f"   NO rung of the ladder reaches sufficiency 1.0000 on the qualifying corpus.")

    # plateau: two ADJACENT rungs both meeting both bars
    plateau = any(KLADDER[i] in ok_rungs and KLADDER[i + 1] in ok_rungs
                  for i in range(len(KLADDER) - 1))

    # ================================ B. what the term costs ============================
    P(f"\n{'='*112}")
    P("B. WHAT THE TERM COSTS - the necessity leg.  A tie whose arm de-grosses AFTER the trough")
    P("   is a TRUE TIE the POST term throws away; each one is a false NEGATIVE that the bare")
    P("   DECLINE predicate did not have.  This is the load-bearing measurement of idea 817.")
    P(f"{'='*112}")
    P(f"   {'k':<6} {'#pred':>6} {'nec P(pred|tie)':>16} {'ties LOST':>10} {'suff P(tie|pred)':>17} "
      f"{'FP left':>8} {'#pred>=30':>10}")
    base_nec = lc_r["P_pred_given_tie"]
    for k, r in qual:
        lost = lc_r["n_tie"] - int((pred_mask(LC, f"POST:{k}", HEAD_EPS) & LC.tie_U).sum())
        P(f"   {str(k):<6} {r['n_pred']:>6} {r['P_pred_given_tie']:>16.4f} {lost:>10} "
          f"{r['P_tie_given_pred']:>17.4f} {r['false_pos']:>8} "
          f"{('yes' if r['n_pred'] >= PRED_BAR else 'NO'):>10}")
    P(f"   (bare DECLINE on the same corpus: #pred {lc_r['n_pred']}, necessity {base_nec:.4f}, "
      f"sufficiency {lc_r['P_tie_given_pred']:.4f}, FP {lc_r['false_pos']})")
    n_zero_window = int((LC.cover_WINDOW <= HEAD_EPS).sum())
    P(f"\n   TRIVIALISATION REFERENCE: {n_zero_window} of {len(LC)} qualifying arms have ZERO cover")
    P(f"   over the WHOLE window - those arms ARE CONTROL-U and tie by construction.  Any rung")
    P(f"   whose #pred equals that number has collapsed onto them and predicts nothing.")

    # ================================ C. the false positives ============================
    P(f"\n{'='*112}")
    P("C. THE FALSE POSITIVES - 813's 15, and which of them the POST term actually removes.")
    P(f"{'='*112}")
    P(f"   {len(FP_DEC)} false positives of the bare DECLINE predicate over all "
      f"{len(nd_all)} scored arm-windows.")
    P(f"   by family:  " + "  ".join(f"{f}:{int((FP_DEC.family == f).sum())}" for f in FAMILIES))
    P(f"\n   {'panel':<6} {'window':<7} {'family':<8} {'dial':>6} {'g':>5} {'dMaxDD_U':>10} "
      f"{'ctl trough':>11} {'arm trough':>11} {'cov_PRE':>8} {'cov_REC':>8} {'armDD<peak':>11} "
      f"{'removed by POST?':>17}")
    fp_removed = {}
    for _, r in FP_DEC.sort_values(["family", "window"]).iterrows():
        rem = [str(k) for k in KLADDER if r[kcol(k)] > HEAD_EPS]
        fp_removed[(r.panel, r.window, r.family, r.dial, r.gross)] = rem
        tag = (f"k>={rem[0]}" if rem else "NEVER")
        P(f"   {r.panel:<6} {r.window:<7} {r.family:<8} {r.dial:>6} {r.gross:>5.2f} "
          f"{r.dMaxDD_U:>10.2%} {r.ctl_trough:>11} {r.arm_trough:>11} {r.cover_PREPEAK:>8.4f} "
          f"{r.cover_RECOVERY:>8.4f} {str(r.arm_dd_before_ctl_peak):>11} {tag:>17}")
    never_removed = [k for k, v in fp_removed.items() if not v]
    P(f"\n   {len(FP_DEC) - len(never_removed)} of {len(FP_DEC)} false positives are removed by SOME")
    P(f"   rung of the POST ladder; {len(never_removed)} are NOT removable by ANY rung.")
    if never_removed:
        P(f"   The unremovable ones are the diagnostic: an arm whose OWN MaxDD sits BEFORE the")
        P(f"   control's peak de-grossed before the episode even began, so no post-trough clause")
        P(f"   can reach it.  arm_dd_before_ctl_peak on those rows: "
          f"{int(FP_DEC[[not fp_removed[(r.panel, r.window, r.family, r.dial, r.gross)] for _, r in FP_DEC.iterrows()]].arm_dd_before_ctl_peak.sum())}"
          f" of {len(never_removed)}.")
    if HEAD_K is not None:
        stillfp = FP_DEC[FP_DEC[kcol(HEAD_K)] <= HEAD_EPS]
        P(f"\n   at the headline rung k = {HEAD_K}: {len(FP_DEC) - len(stillfp)} of {len(FP_DEC)} "
          f"removed, {len(stillfp)} survive over all windows.")
    FP_DEC.to_csv(f"{OUT}.falsepos.csv", index=False)
    cost_dis = {k: int((pred_mask(nd_all, f"POST:{k}", HEAD_EPS) !=
                        pred_mask(nd_all, f"POST:{k}+COST", HEAD_EPS)).sum()) for k in KLADDER}
    P(f"\n   POST_k vs POST_k+COST disagreements over all scored cells: " +
      "  ".join(f"{k}:{v}" for k, v in cost_dis.items()))

    P(f"\n   COVER-BAR LADDER (reported axis, not a tune), corpus QUALIFY, family set ALL:")
    P(f"   {'leg':<14} " + " ".join(f"{e:>10.0e}" for e in EPS_BAR) + "     <- P(tie|pred); #pred below")
    for leg, lab in [("DECLINE", "DECLINE")] + [(f"POST:{k}", f"+POST {k}") for k in KLADDER]:
        rr = [rates(LC, leg, e) for e in EPS_BAR]
        P(f"   {lab:<14} " + " ".join(f"{x['P_tie_given_pred']:>10.4f}" for x in rr))
        P(f"   {'':<14} " + " ".join(f"{x['n_pred']:>10d}" for x in rr))

    # ================================ D. rule 8 =========================================
    P(f"\n{'='*112}")
    P("D. PROTOCOL RULE 8 WALK-FORWARD - (a) the STANDING 2016/2017 split on the FULL window,")
    P("   (b) a WINDOW-LOCAL half split for the short windows (a stated departure, reported")
    P("   beside (a), never instead of it).  Dial chosen on IS by IS Sharpe ALONE; OOS read ONCE.")
    P(f"{'='*112}")
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
    clean_total = 0
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        pas = nd[nd.pass_4b]
        if pas.empty:
            P(f"   window {w}: no 4b passers.")
            continue
        clean = pas[pas.pass_4b & pas.pass_4b_OOS & ~pas.ctlM_pass_4b]
        clean_total += len(clean)
        P(f"   window {w}: {len(pas)} pass 4b; {int(pas.ctlM_pass_4b.sum())} of them are matched by "
          f"their own CONTROL-M (pass = exposure, not the clause); {len(clean)} clear BOTH windows "
          f"AND beat CONTROL-M.")
        for _, r in clean.head(8).iterrows():
            P(f"      {r.panel} {r.family} dial={r.dial} g={r.gross:.2f}  "
              f"{r.CAGR:.2%}/{r.Sharpe:.3f}/{r.MaxDD:.2%}  ctlM {r.ctlM_CAGR:.2%}/"
              f"{r.ctlM_Sharpe:.3f}/{r.ctlM_MaxDD:.2%}  turn {r.turn_per_yr:.2f}x/yr")

    # ================================ E. hypotheses =====================================
    NA = None
    if HEAD_K is not None:
        hr = rates(LC, f"POST:{HEAD_K}", HEAD_EPS)
        hr_x = rates(LC[~LC.confound], f"POST:{HEAD_K}", HEAD_EPS)
        n_still_fp = int((pred_mask(nd_all, f"POST:{HEAD_K}", HEAD_EPS) & ~nd_all.tie_U).sum())
        n_zero_head = int((LC.cover_WINDOW <= HEAD_EPS).sum())
    else:
        hr = hr_x = dict(n_pred=0, P_pred_given_tie=np.nan, P_tie_given_pred=np.nan)
        n_still_fp, n_zero_head = len(FP_DEC), n_zero_window
    mono = all(rates(LC, f"POST:{KLADDER[i]}", HEAD_EPS)["n_pred"] >=
               rates(LC, f"POST:{KLADDER[i+1]}", HEAD_EPS)["n_pred"]
               for i in range(len(KLADDER) - 1))

    H = [("H_REPRO   this run reproduces 813's committed corpus (gates G5a/G5b/G6)", bool(g5)),
         ("H_SUFF1   some rung k returns sufficiency 1.0000 on QUALIFY, ALL families",
          bool(len(suff1_rungs) > 0)),
         (f"H_POWER   at the headline rung #pred >= {PRED_BAR}",
          bool(hr["n_pred"] >= PRED_BAR) if HEAD_K is not None else NA),
         ("H_NEC1    at the headline rung necessity = 1.0000 [LOAD-BEARING]",
          bool(hr["P_pred_given_tie"] == 1.0) if HEAD_K is not None else NA),
         ("H_PLATEAU two ADJACENT rungs meet sufficiency 1.0000 AND the power bar", bool(plateau)),
         ("H_ALLFP   the headline rung removes ALL of 813's false positives, every window",
          bool(n_still_fp == 0) if HEAD_K is not None else NA),
         ("H_NONTRIV at the headline rung #pred exceeds the zero-cover-all-window count",
          bool(hr["n_pred"] > n_zero_head) if HEAD_K is not None else NA),
         (f"H_NOSPYDD sufficiency is 1.0000 at the headline rung with {CONFOUND} dropped",
          bool(hr_x["P_tie_given_pred"] == 1.0) if HEAD_K is not None else NA),
         ("H_COST    POST_k and POST_k+COST agree on every scored cell, every rung",
          all(v == 0 for v in cost_dis.values())),
         ("H_MONO    #pred is monotone non-increasing along the k ladder", bool(mono))]

    P(f"\n{'='*112}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*112}")
    P(f"   corpus: the pooled long-decline cells ({len(long_cells)} (panel,window) cells, "
      f"{len(LC)} scored arms, {lc_r['n_tie']} ties, {lc_r['n_pred']} DECLINE-predicate arms).")
    P(f"   headline rung: k = {HEAD_K}" + ("" if ok_rungs else "  (NOT PROMOTED - fails the power bar)")
      + f";  rungs reaching sufficiency 1.0000: {suff1_rungs or 'none'}")
    for nm, v in H:
        P(f"   {nm:<72} {'N/A - no qualifying rung' if v is NA else ('PASS' if v else 'FAIL')}")
    ev = [v for _, v in H if v is not NA]
    nna = sum(1 for _, v in H if v is NA)
    P(f"\n   {sum(bool(v) for v in ev)} of {len(ev)} EVALUABLE pre-registered hypotheses pass"
      + (f"; {nna} of {len(H)} are NOT EVALUABLE." if nna else "."))

    P(f"\n   THE ANSWER, in the three numbers the idea asks for, on the qualifying corpus:")
    P(f"   {'leg':<16} {'#pred':>6} {'necessity':>10} {'sufficiency':>12} {'two-directional?':>17}")
    for leg, lab in [("DECLINE", "DECLINE (813)")] + [(f"POST:{k}", f"+POST k={k}") for k in KLADDER]:
        r = rates(LC, leg, HEAD_EPS)
        P(f"   {lab:<16} {r['n_pred']:>6} {r['P_pred_given_tie']:>10.4f} "
          f"{r['P_tie_given_pred']:>12.4f} {('YES' if r['exact'] else 'no'):>17}")
    P(f"\n   4b passers clearing BOTH windows and beating CONTROL-M, all windows: {clean_total}")
    P(f"   rule-8 picks passing 4b OOS: {int(WF.OOS_4b.sum())} of {len(WF)};  "
      f"4a OOS: {int(WF.OOS_4a.sum())} of {len(WF)}")

    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, E=E, WF=WF, LC=LC, FP=FP_DEC, H=H, HEAD_K=HEAD_K, KL=KL)


if __name__ == "__main__":
    main()
