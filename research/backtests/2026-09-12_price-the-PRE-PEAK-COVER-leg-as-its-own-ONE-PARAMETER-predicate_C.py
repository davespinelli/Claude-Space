#!/usr/bin/env python3
"""Idea 820 - price the PRE-PEAK COVER leg as its own ONE-PARAMETER predicate.
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 820, verbatim)
    Idea 817 found 3 of 813's 15 false positives are removable by NO post-trough rung because
    their de-gross sits BEFORE the control's peak (arm trough 2023-03-10 vs control 2025-04-08,
    cover_RECOVERY exactly 0).  Add cover(window start .. peak-1) <= 0 as a single-conjunct
    alternative and report what IT costs necessity on the same 897-arm corpus, so the two
    candidate missing terms are priced against each other rather than stacked.
    Max 2 params (pre-peak length, family set).

WHAT IS BEING PRICED, STATED BEFORE ANYTHING IS RUN
    813 left 596's predicate one-directional: on the qualifying (long-decline) corpus
    cover(DECLINE) <= 0 is NECESSARY (1.0000) and NOT SUFFICIENT (0.9737, 3 false positives;
    15 over all windows).  817 priced ONE candidate missing conjunct - no de-gross in the k days
    AFTER the control's trough - and found sufficiency returns at EVERY rung while necessity falls
    at EVERY rung (1.0000 -> 0.8919 at the cheapest), i.e. the term is a filter fitted to the
    false positives, not a missing term.  820 prices the OTHER candidate the counterexamples name:
    no de-gross BEFORE the control's peak.  The two are alternatives, so they are reported
    SIDE BY SIDE at every rung and the STACKED form (DECLINE+PRE+POST) is printed ONLY as a
    labelled diagnostic, never as a headline - stacking is what the queue's idea forbids.

    Adding any conjunct can only SHRINK the predicate population, so sufficiency is purchasable
    at will.  The claim is therefore only interesting if all of these hold at the SAME rung, and
    each is pre-registered:
      (1) SUFFICIENCY  P(tie | DECLINE+PRE_m) = 1.0000 on the qualifying corpus;
      (2) POWER        #pred >= 30 there (the record's power bar, unchanged);
      (3) NECESSITY    P(DECLINE+PRE_m | tie) = 1.0000 - the term throws away NO true tie.
                       [LOAD-BEARING: a FAIL means PRE is the same kind of second tune POST was.]
      (4) NON-TRIVIAL  #pred strictly exceeds the count of arms whose cover over the WHOLE window
                       is zero (the predicate must not collapse to "the arm is the control").
    HEADLINE m IS RULE-CHOSEN, NOT PICKED: the SMALLEST rung at which (1) and (2) both hold with
    ALL families.  If none does, none is promoted and that is the report.

THE CORPUS (813's, rebuilt bit-for-bit; 817's cover columns reproduced as a gate)
    book      B(g) = the LIVE form, baseline.rules_v2_weights: every name inside its 200d +/-3%
              band at g/N of NAV, gated-out weight to CASH, weekly, next-day fill, 10 bps.
    clause    a MARKET-level gate s_t in {0,1}; gate OFF => the book de-grosses to cash that week.
    controls  CONTROL-U = B(g) at nominal gross (the tie label is defined against it),
              CONTROL-M = B(g) * c, c set so mean realised gross equals the arm's.
    families  SPYTR / BREADTH / VOL / SPYDD / CORR / DISP, 5 dials each.  SPYDD is the NAMED
              CONFOUND and every rate is reported again with it dropped.
    panels    U56, B136, SMALL (sub-$2B, max_1d_move >= 1.0 dropped first).
    gross     g in {0.50, 0.75, 1.00}.  6 x 5 x 3 = 90 arms per panel, 270 in all, ALL reported.
    windows   the same 7 evaluation windows; a window never slices the data, only the return path.
    QUALIFYING CORPUS = pooled (panel, window) cells whose CONTROL-U binding decline exceeds 60
              trading days - 813 measured 14 cells, 897 scored arms, 111 ties, 114 predicate arms,
              sufficiency 0.9737, 3 false positives.  Reproducing that is gate G5b.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) m, the PRE-PEAK LENGTH: {5, 10, 21, 42, 63, 126, 252, ALL} trading days ending the day
        BEFORE the control's peak.  ALL = window start .. peak-1, the queue's literal definition
        and the degenerate end of the ladder, printed so any trivialisation is visible.
    (2) FAMILY SET: ALL (6 families) vs NO-SPYDD (5, the confound dropped).
    8 x 2 = 16 grid points, EVERY ONE printed and written to .predicates.csv.
    COVER BAR is NOT a third tune: headline eps = 0, the ladder {0, 1e-12, 1e-6, 1e-4, 1e-3}
    printed in full as a reported robustness axis, as 596/811/813/817 did.
    817's POST ladder is recomputed and carried UNCHANGED as the comparand, not as a tune.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_REPRO   the rebuilt corpus reproduces 813's committed cells (897/111/114/0.9737/3 FP and the
              596/811 sub-corpus 141/45/1.0000/1.0000) AND 817's committed cover_PREPEAK and
              cover_POST_k columns to 1e-12.  Gate, not evidence.
    H_SUFF1   some rung m returns P(tie | DECLINE+PRE_m) = 1.0000 on the qualifying corpus,
              ALL families.
    H_POWER   at the headline rung, #pred >= 30.
    H_NEC1    at the headline rung, necessity = 1.0000.  [LOAD-BEARING]
    H_CHEAPER the PRE term costs STRICTLY FEWER true ties than 817's headline POST rung (k = 5,
              which discarded 12) at the first rung where PRE reaches sufficiency 1.0000.  This is
              the head-to-head the queue asks for; a FAIL means PRE is the worse of the two terms.
    H_PLATEAU at least TWO ADJACENT rungs deliver sufficiency 1.0000 with #pred >= 30.
    H_ALLFP   the headline rung excludes ALL 15 false positives over ALL windows.
    H_NONTRIV at the headline rung, #pred exceeds the zero-cover-over-the-window count.
    H_NOSPYDD sufficiency is also 1.0000 at the headline rung with the confound family dropped.
    H_COMPL   the two terms are COMPLEMENTARY, not nested: PRE_ALL removes the 3 false positives
              no POST rung can reach, and POST removes at least one PRE cannot.
    H_MONO    #pred is monotone non-increasing along the m ladder (sanity: a conjunct can only
              remove arms; a violation means the cover windows are mis-built).

GATES (printed first; all must pass before any verdict is read)
    G1  the arm at a never-firing gate is EXACTLY CONTROL-U.
    G2  the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G3  in EVERY (panel, gross, window) the located binding episode reproduces that window's MaxDD.
    G4  CONTROL-M's realised mean gross equals the arm's to <= 1e-3.
    G5a REPRODUCTION: the 596/811 sub-corpus - 141 arms, 45 ties, necessity 1.0000, sufficiency
        1.0000, ties by family SPYTR 0 / BREADTH 12 / VOL 18 / SPYDD 15.
    G5b REPRODUCTION: 813's qualifying corpus - 14 cells, 897 arms, 111 ties, 114 predicate arms,
        sufficiency 0.9737, 3 false positives; 15 false positives over all windows CORR 9 / VOL 3
        / SPYDD 3.
    G7  REPRODUCTION of 817's committed cell file: cover_PRE_ALL == its cover_PREPEAK and every
        cover_POST_k == its own, joined on (panel, window, family, dial, gross), max|d| <= 1e-12.

PROTOCOL RULE 8 (mandatory, run and reported):
    (a) STANDING convention - per (panel, family, gross) the DIAL is chosen on IS (..2016-12-31)
        by IS Sharpe alone, OOS (2017-01-01..) read exactly ONCE, reported as CAGR/Sharpe/MaxDD
        against RULES v2 and SPY on the same window.  Both KEEP paths evaluated on all 270 arms.
    (b) WINDOW-LOCAL - a window ending in 2012 has no 2017+ out-of-sample, so for every non-FULL
        window the dial is also chosen on its FIRST HALF and read once on its SECOND HALF.  A
        stated DEPARTURE from the record's 2016/2017 split, reported beside (a), never instead.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic and the SMALL panel worst (data/SMALL_PANEL_README.md).  The predicate rates are
    within-panel agreement rates, which survivorship moves far less than levels.  Several windows
    are 3-5 years and sit wholly inside a bull leg, so no Sharpe or CAGR read off them is a
    capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .cells.csv       one row per (arm, window): metrics, tie label, every cover leg, 4a/4b
    .predicates.csv  every leg x family set x corpus x the 5-rung cover ladder, all points
    .mladder.csv     the m ladder and the POST comparand on every corpus
    .falsepos.csv    every false positive, with which rung of each term removes it
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
SLUG = "price-the-PRE-PEAK-COVER-leg-as-its-own-ONE-PARAMETER-predicate"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
REF817 = (Path(__file__).resolve().parent /
          ("2026-09-12_is-the-DECLINE-COVER-predicate-SUFFICIENT-ONCE-A-POST-TROUGH-RE-ENTRY-TERM-"
           "IS-ADDED_cloud.cells.csv"))

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

# tuned dial 1: the PRE-PEAK length.  ALL is the queue's literal "window start .. peak-1".
MLADDER = [5, 10, 21, 42, 63, 126, 252, "ALL"]
# 817's ladder, recomputed UNCHANGED as the comparand (not a tune of this run).
KLADDER = [5, 10, 21, 42, 63, 126, 252, "REC", "ALL"]
POST_HEAD = 5          # 817's rule-chosen headline rung, and the number PRE is priced against
POST_HEAD_LOST = 12    # true ties it discarded on the qualifying corpus (817, committed)
EPS_BAR = [0.0, 1e-12, 1e-6, 1e-4, 1e-3]
HEAD_EPS = 0.0
TIE_EPS = 1e-12
LONG_DECLINE = 60
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

T813_596 = dict(n=141, ties=45, nec=1.0, suff=1.0,
                byf={"SPYTR": 0, "BREADTH": 12, "VOL": 18, "SPYDD": 15})
T813_LONG = dict(cells=14, n=897, ties=111, npred=114, suff=0.9737, fp=3)
T813_FPALL = dict(total=15, byfam={"CORR": 9, "VOL": 3, "SPYDD": 3})

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def mcol(m):
    return f"cover_PRE_{m}"


def kcol(k):
    return f"cover_POST_{k}"


# ------------------------------------------------------------------ runner (596/804/811/813/817)
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
    """[lo, hi] of 817's POST-TROUGH window for rung k, within the evaluation window idx."""
    tpos = int(idx.get_indexer([trough])[0])
    if tpos < 0 or tpos + 1 >= len(idx):
        return None, None
    lo = idx[tpos + 1]
    if k == "ALL":
        return lo, idx[-1]
    if k == "REC":
        return (lo, recovery) if recovery > trough else (None, None)
    return lo, idx[min(tpos + int(k), len(idx) - 1)]


def pre_bounds(idx: pd.DatetimeIndex, peak, m):
    """[lo, hi] of the PRE-PEAK window for rung m: the m days ENDING the day before the peak.
    m == 'ALL' is the queue's literal leg, window start .. peak-1.  A peak on the first scored
    day has NO pre-peak room at all, which is vacuously clean and reported as cover 0."""
    ppos = int(idx.get_indexer([peak])[0])
    if ppos <= 0:
        return None, None
    hi = idx[ppos - 1]
    lo = idx[0] if m == "ALL" else idx[max(0, ppos - int(m))]
    return lo, hi


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
    """legs:
       DECLINE              cover(peak..trough) <= eps            (813/596's, the base)
       PRE:<m>              DECLINE AND cover(pre-peak m) <= eps  (820's candidate term)
       PREONLY:<m>          cover(pre-peak m) <= eps ALONE        (the other reading, reported)
       POST:<k>             DECLINE AND cover(trough+1..+k) <= eps (817's, the comparand)
       STACK:<m>|<k>        DECLINE AND PRE_m AND POST_k          (DIAGNOSTIC ONLY, never headline)
    """
    if leg == "DECLINE":
        return df.cover_DECLINE <= eps
    if leg == "EPISODE":
        return df.cover_EPISODE <= eps
    if leg == "RECOVERY":
        return df.cover_RECOVERY <= eps
    if leg == "DECLINE+COST":
        return (df.cover_DECLINE <= eps) & (df.switch_DECLINE <= eps)
    if leg.startswith("PREONLY:"):
        return df[mcol(leg.split(":", 1)[1])] <= eps
    if leg.startswith("PRE:"):
        body = leg.split(":", 1)[1]
        cost = body.endswith("+COST")
        m = body[:-5] if cost else body
        out = (df.cover_DECLINE <= eps) & (df[mcol(m)] <= eps)
        if cost:
            out = out & (df.switch_DECLINE <= eps)
        return out
    if leg.startswith("POST:"):
        body = leg.split(":", 1)[1]
        cost = body.endswith("+COST")
        k = body[:-5] if cost else body
        out = (df.cover_DECLINE <= eps) & (df[kcol(k)] <= eps)
        if cost:
            out = out & (df.switch_DECLINE <= eps)
        return out
    if leg.startswith("STACK:"):
        m, k = leg.split(":", 1)[1].split("|")
        return (df.cover_DECLINE <= eps) & (df[mcol(m)] <= eps) & (df[kcol(k)] <= eps)
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
    P(f"# Idea 820 - {SLUG}  (lane C, {DATE})")
    P("# Object: 813 left the tie predicate one-directional; 817 priced the POST-TROUGH conjunct")
    P("# and found it buys sufficiency only by spending necessity.  820 prices the OTHER candidate")
    P("# term the counterexamples name - NO DE-GROSS BEFORE THE CONTROL'S PEAK - on the same")
    P("# corpus, side by side with POST, NEVER stacked with it.")
    P(f"# TUNED: m {MLADDER} x family set [ALL, NO-{CONFOUND}] = {len(MLADDER)*2} points, all printed.")
    P(f"# Cover bar is NOT a third tune: headline eps = {HEAD_EPS:g}, ladder {EPS_BAR} printed.")
    P("# HEADLINE RUNG IS RULE-CHOSEN: smallest m with sufficiency 1.0000 AND "
      f"#pred >= {PRED_BAR} on the qualifying corpus, ALL families.  If none, none is promoted.")
    P("# H_NEC1 is load-bearing and stated in the direction that would falsify 820, exactly as 817.")
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
                pre_days = int((rw.index < pk).sum())
                ep[(g, w)] = (pk, tr, rc, rec, ddmin)
                eprows.append(dict(panel=pname, gross=g, window=w,
                                   win_start=rw.index[0].date(), win_end=rw.index[-1].date(),
                                   n_days=len(rw), peak=pk.date(), trough=tr.date(),
                                   recovery=rc.date(), recovered=rec, trough_year=int(tr.year),
                                   MaxDD=ddmin, decline_days=dd_days, recovery_days=rc_days,
                                   days_before_peak=pre_days,
                                   days_after_trough=int((rw.index > tr).sum()),
                                   long_decline=bool(dd_days > LONG_DECLINE)))
        P(f"\n   CONTROL-U binding episodes by (gross, window), with the room EACH term has:")
        P(f"   {'g':>5} {'window':<7} {'days':>5} {'MaxDD':>8} {'peak':>11} {'trough':>11} "
          f"{'pre_d':>6} {'dec_d':>6} {'rec_d':>6} {'after_tr':>9} {'>60d?':>6}")
        for e in [e for e in eprows if e["panel"] == pname]:
            P(f"   {e['gross']:>5.2f} {e['window']:<7} {e['n_days']:>5} {e['MaxDD']:>8.2%} "
              f"{str(e['peak']):>11} {str(e['trough']):>11} {e['days_before_peak']:>6} "
              f"{e['decline_days']:>6} {e['recovery_days']:>6} {e['days_after_trough']:>9} "
              f"{'LONG' if e['long_decline'] else 'short':>6}"
              f"{'' if e['recovered'] else '  (NEVER RECOVERED - flagged)'}")

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
                        pre = {}
                        for m_ in MLADDER:
                            lo, hi = pre_bounds(idx, pk, m_)
                            pre[mcol(m_)] = cover(u, lo, hi)
                        post = {}
                        for k in KLADDER:
                            lo, hi = post_bounds(idx, tr, rcv, k)
                            post[kcol(k)] = cover(u, lo, hi)
                        ppos = int(idx.get_indexer([pk])[0])
                        cov_pre_all = cover(u, idx[0], idx[ppos - 1]) if ppos > 0 else 0.0
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
                            days_before_peak=int((idx < pk).sum()),
                            decline_days=int(((idx >= pk) & (idx <= tr)).sum()),
                            recovery_days=int(((idx > tr) & (idx <= rcv)).sum()),
                            days_after_trough=int((idx > tr).sum()),
                            long_decline=bool(int(((idx >= pk) & (idx <= tr)).sum()) > LONG_DECLINE),
                            trough_year=int(tr.year), ctl_peak=str(pk.date()),
                            ctl_trough=str(tr.date()),
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
                            cover_PREPEAK=cov_pre_all, cover_WINDOW=cov_win, **pre, **post,
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

    # ================================ G5 / G7 reproduction ==============================
    P(f"\n{'='*112}")
    P("G5/G7 REPRODUCTION GATES - nothing below is read until this run reproduces 813's committed")
    P("   cells and 817's committed cover columns exactly.")
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

    # G7: 817's committed cell file, joined key-for-key
    g7 = True
    if REF817.exists():
        ref = pd.read_csv(REF817)
        keys = ["panel", "window", "family", "dial", "gross"]
        j = C.merge(ref, on=keys, suffixes=("", "_817"), how="inner")
        P(f"   G7  joined {len(j)} of {len(C)} rows onto 817's committed cell file")
        pairs = [(mcol("ALL"), "cover_PREPEAK_817"), ("cover_DECLINE", "cover_DECLINE_817"),
                 ("tie_U", "tie_U_817")] + [(kcol(k), f"{kcol(k)}_817") for k in KLADDER]
        for a, bb in pairs:
            if bb not in j.columns:
                P(f"   G7  {a:<18} column {bb} absent in the reference - SKIPPED")
                continue
            d = float(np.abs(j[a].astype(float) - j[bb].astype(float)).max())
            okc = d < 1e-12 and len(j) == len(C)
            g7 &= okc
            P(f"   G7  {a:<18} vs 817's {bb:<22} max|d| {d:.3e}  {'PASS' if okc else 'FAIL'}")
    else:
        g7 = False
        P(f"   G7  FAIL - 817's committed cell file not found at {REF817.name}")
    g5 &= g7
    P(f"   G5/G7 {'PASS' if g5 else 'FAIL'} - this run stands on 813's corpus and 817's columns.")
    assert g5, "a reproduction gate failed - this run does not reproduce the corpus it extends"

    # ================================ A. the m ladder ===================================
    P(f"\n{'='*112}")
    P("A. THE TUNED GRID - m ladder x family set, ALL 16 POINTS PRINTED, on every corpus, with")
    P("   813's bare DECLINE and 817's POST comparand printed in the same table.")
    P(f"   PRE_m  = cover(DECLINE) <= {HEAD_EPS:g} AND cover(peak-m .. peak-1) <= {HEAD_EPS:g}")
    P(f"   PRE_ALL= the queue's literal leg: cover(window start .. peak-1) <= {HEAD_EPS:g}")
    P(f"{'='*112}")
    CORPORA = [("QUALIFY (long-decline)", LC),
               ("FULL (596/811 reference)", nd_all[nd_all.window == "FULL"]),
               ("POST20 (811's break)", nd_all[nd_all.window == "POST20"]),
               ("ALL WINDOWS POOLED", nd_all)]
    POPS = [("ALL", lambda d: d), (f"NO-{CONFOUND}", lambda d: d[~d.confound])]
    mrows = []
    for cname, cdf0 in CORPORA:
        for popname, popsel in POPS:
            d = popsel(cdf0)
            P(f"\n   corpus {cname}   family set {popname}   (n {len(d)}, ties {int(d.tie_U.sum())})")
            P(f"   {'leg':<18} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} {'P(tie|pred)':>12} "
              f"{'FN':>4} {'FP':>4} {'both=1?':>8}")
            legs = ([("DECLINE", "DECLINE (813)")] +
                    [(f"PRE:{m_}", f"+PRE m={m_}") for m_ in MLADDER] +
                    [(f"PREONLY:{m_}", f"PRE m={m_} ALONE") for m_ in MLADDER] +
                    [(f"POST:{k}", f"+POST k={k} (817)") for k in KLADDER])
            for leg, lab in legs:
                r = rates(d, leg, HEAD_EPS)
                mrows.append(dict(corpus=cname, family_set=popname, leg=lab, raw_leg=leg, **r))
                P(f"   {lab:<18} {r['n_pred']:>6} {r['n_tie']:>5} "
                  f"{r['P_pred_given_tie']:>12.4f} {r['P_tie_given_pred']:>12.4f} "
                  f"{r['false_neg']:>4} {r['false_pos']:>4} "
                  f"{('YES' if r['exact'] else 'no'):>8}")
    ML = pd.DataFrame(mrows)
    ML.to_csv(f"{OUT}.mladder.csv", index=False)

    prows = []
    for cname, cdf0 in CORPORA:
        for popname, popsel in POPS:
            d = popsel(cdf0)
            for leg in (["DECLINE", "RECOVERY", "EPISODE", "DECLINE+COST"] +
                        [f"PRE:{m_}" for m_ in MLADDER] +
                        [f"PRE:{m_}+COST" for m_ in MLADDER] +
                        [f"PREONLY:{m_}" for m_ in MLADDER] +
                        [f"POST:{k}" for k in KLADDER] +
                        [f"STACK:ALL|{k}" for k in KLADDER]):
                for eps in EPS_BAR:
                    prows.append(dict(corpus=cname, family_set=popname, leg=leg, eps=eps,
                                      **rates(d, leg, eps)))
    pd.DataFrame(prows).to_csv(f"{OUT}.predicates.csv", index=False)

    P(f"\n{'-'*112}")
    P(f"   HEADLINE RUNG by the PRE-STATED rule: smallest m with sufficiency == 1.0000 AND")
    P(f"   #pred >= {PRED_BAR} on QUALIFY with ALL families.")
    qual = [(m_, rates(LC, f"PRE:{m_}", HEAD_EPS)) for m_ in MLADDER]
    ok_rungs = [m_ for m_, r in qual if r["P_tie_given_pred"] == 1.0 and r["n_pred"] >= PRED_BAR]
    suff1_rungs = [m_ for m_, r in qual if r["P_tie_given_pred"] == 1.0]
    HEAD_M = ok_rungs[0] if ok_rungs else (suff1_rungs[0] if suff1_rungs else None)
    if ok_rungs:
        P(f"   rungs meeting BOTH bars: {ok_rungs}   -> HEADLINE m = {HEAD_M}")
    elif suff1_rungs:
        P(f"   NO rung meets both bars.  Rungs reaching sufficiency 1.0000 at all: {suff1_rungs} "
          f"(all UNDERPOWERED, #pred < {PRED_BAR}).  m = {HEAD_M} is carried ONLY to report what "
          f"it costs; it is NOT promoted.")
    else:
        P(f"   NO rung of the m ladder reaches sufficiency 1.0000 on the qualifying corpus.")
    plateau = any(MLADDER[i] in ok_rungs and MLADDER[i + 1] in ok_rungs
                  for i in range(len(MLADDER) - 1))

    # ================================ B. the head-to-head ===============================
    P(f"\n{'='*112}")
    P("B. THE HEAD-TO-HEAD - what EACH candidate term costs NECESSITY on the SAME 897-arm corpus.")
    P("   A tie the conjunct excludes is a TRUE TIE thrown away: a false NEGATIVE the bare DECLINE")
    P("   predicate did not have.  This is the measurement idea 820 asks for.")
    P(f"{'='*112}")
    P(f"   {'term':<16} {'#pred':>6} {'nec P(pred|tie)':>16} {'ties LOST':>10} "
      f"{'suff P(tie|pred)':>17} {'FP left':>8} {'#pred>=30':>10}")
    for m_, r in qual:
        lost = lc_r["n_tie"] - int((pred_mask(LC, f"PRE:{m_}", HEAD_EPS) & LC.tie_U).sum())
        P(f"   {'PRE m=' + str(m_):<16} {r['n_pred']:>6} {r['P_pred_given_tie']:>16.4f} {lost:>10} "
          f"{r['P_tie_given_pred']:>17.4f} {r['false_pos']:>8} "
          f"{('yes' if r['n_pred'] >= PRED_BAR else 'NO'):>10}")
    post_qual = [(k, rates(LC, f"POST:{k}", HEAD_EPS)) for k in KLADDER]
    for k, r in post_qual:
        lost = lc_r["n_tie"] - int((pred_mask(LC, f"POST:{k}", HEAD_EPS) & LC.tie_U).sum())
        P(f"   {'POST k=' + str(k) + ' (817)':<16} {r['n_pred']:>6} {r['P_pred_given_tie']:>16.4f} "
          f"{lost:>10} {r['P_tie_given_pred']:>17.4f} {r['false_pos']:>8} "
          f"{('yes' if r['n_pred'] >= PRED_BAR else 'NO'):>10}")
    P(f"   {'DECLINE (813)':<16} {lc_r['n_pred']:>6} {lc_r['P_pred_given_tie']:>16.4f} "
      f"{0:>10} {lc_r['P_tie_given_pred']:>17.4f} {lc_r['false_pos']:>8} "
      f"{('yes' if lc_r['n_pred'] >= PRED_BAR else 'NO'):>10}")

    pre_lost_head = (lc_r["n_tie"] - int((pred_mask(LC, f"PRE:{HEAD_M}", HEAD_EPS) & LC.tie_U).sum())
                     if HEAD_M is not None else None)
    P(f"\n   817's headline POST rung (k = {POST_HEAD}) discarded {POST_HEAD_LOST} true ties "
      f"(committed).  This run's POST k={POST_HEAD} discards "
      f"{lc_r['n_tie'] - int((pred_mask(LC, f'POST:{POST_HEAD}', HEAD_EPS) & LC.tie_U).sum())}.")
    if HEAD_M is not None:
        P(f"   820's headline PRE rung (m = {HEAD_M}) discards {pre_lost_head} true ties.")

    n_zero_window = int((LC.cover_WINDOW <= HEAD_EPS).sum())
    P(f"\n   TRIVIALISATION REFERENCE: {n_zero_window} of {len(LC)} qualifying arms have ZERO cover")
    P(f"   over the WHOLE window - those arms ARE CONTROL-U and tie by construction.  Any rung")
    P(f"   whose #pred equals that number has collapsed onto them and predicts nothing.")

    P(f"\n   THE STACKED FORM, printed as a DIAGNOSTIC ONLY (the queue asks for the two terms")
    P(f"   priced AGAINST each other, not stacked; no stacked row is promoted anywhere):")
    P(f"   {'leg':<26} {'#pred':>6} {'nec':>8} {'suff':>8} {'FP':>4}")
    for k in KLADDER:
        r = rates(LC, f"STACK:ALL|{k}", HEAD_EPS)
        P(f"   {'DECLINE+PRE_ALL+POST_' + str(k):<26} {r['n_pred']:>6} "
          f"{r['P_pred_given_tie']:>8.4f} {r['P_tie_given_pred']:>8.4f} {r['false_pos']:>4}")

    # ================================ C. the false positives ============================
    P(f"\n{'='*112}")
    P("C. THE FALSE POSITIVES - 813's 15, and which rung of WHICH term removes each one.")
    P(f"{'='*112}")
    P(f"   {len(FP_DEC)} false positives of the bare DECLINE predicate over all "
      f"{len(nd_all)} scored arm-windows.")
    P(f"   by family:  " + "  ".join(f"{f}:{int((FP_DEC.family == f).sum())}" for f in FAMILIES))
    P(f"\n   {'panel':<6} {'window':<7} {'family':<8} {'dial':>6} {'g':>5} {'dMaxDD_U':>10} "
      f"{'ctl peak':>11} {'ctl trough':>11} {'arm trough':>11} {'cov_PRE_ALL':>12} "
      f"{'PRE removes?':>13} {'POST removes?':>14}")
    pre_rm, post_rm = {}, {}
    for _, r in FP_DEC.sort_values(["family", "window"]).iterrows():
        kk = (r.panel, r.window, r.family, r.dial, r.gross)
        rm_pre = [str(m_) for m_ in MLADDER if r[mcol(m_)] > HEAD_EPS]
        rm_post = [str(k) for k in KLADDER if r[kcol(k)] > HEAD_EPS]
        pre_rm[kk], post_rm[kk] = rm_pre, rm_post
        P(f"   {r.panel:<6} {r.window:<7} {r.family:<8} {r.dial:>6} {r.gross:>5.2f} "
          f"{r.dMaxDD_U:>10.2%} {r.ctl_peak:>11} {r.ctl_trough:>11} {r.arm_trough:>11} "
          f"{r.cover_PREPEAK:>12.4f} "
          f"{('m>=' + rm_pre[0] if rm_pre else 'NEVER'):>13} "
          f"{('k>=' + rm_post[0] if rm_post else 'NEVER'):>14}")
    pre_never = [k for k, v in pre_rm.items() if not v]
    post_never = [k for k, v in post_rm.items() if not v]
    pre_all_rm = len(FP_DEC) - len(pre_never)
    post_all_rm = len(FP_DEC) - len(post_never)
    P(f"\n   removable by SOME rung:  PRE {pre_all_rm} of {len(FP_DEC)};  "
      f"POST {post_all_rm} of {len(FP_DEC)}.")
    P(f"   PRE reaches {len([k for k in post_never if pre_rm[k]])} of the "
      f"{len(post_never)} false positives NO POST rung can reach.")
    P(f"   POST reaches {len([k for k in pre_never if post_rm[k]])} of the "
      f"{len(pre_never)} false positives NO PRE rung can reach.")
    P(f"   neither term reaches {len([k for k in pre_never if k in post_never])}.")
    if HEAD_M is not None:
        still = FP_DEC[FP_DEC[mcol(HEAD_M)] <= HEAD_EPS]
        P(f"   at the headline rung m = {HEAD_M}: {len(FP_DEC) - len(still)} of {len(FP_DEC)} "
          f"removed, {len(still)} survive over all windows.")
    FP_DEC.to_csv(f"{OUT}.falsepos.csv", index=False)
    cost_dis = {m_: int((pred_mask(nd_all, f"PRE:{m_}", HEAD_EPS) !=
                         pred_mask(nd_all, f"PRE:{m_}+COST", HEAD_EPS)).sum()) for m_ in MLADDER}
    P(f"\n   PRE_m vs PRE_m+COST disagreements over all scored cells: " +
      "  ".join(f"{m_}:{v}" for m_, v in cost_dis.items()))

    P(f"\n   COVER-BAR LADDER (reported axis, not a tune), corpus QUALIFY, family set ALL:")
    P(f"   {'leg':<16} " + " ".join(f"{e:>10.0e}" for e in EPS_BAR) +
      "     <- P(tie|pred); #pred below")
    for leg, lab in ([("DECLINE", "DECLINE")] + [(f"PRE:{m_}", f"+PRE {m_}") for m_ in MLADDER]):
        rr = [rates(LC, leg, e) for e in EPS_BAR]
        P(f"   {lab:<16} " + " ".join(f"{x['P_tie_given_pred']:>10.4f}" for x in rr))
        P(f"   {'':<16} " + " ".join(f"{x['n_pred']:>10d}" for x in rr))

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
    if HEAD_M is not None:
        hr = rates(LC, f"PRE:{HEAD_M}", HEAD_EPS)
        hr_x = rates(LC[~LC.confound], f"PRE:{HEAD_M}", HEAD_EPS)
        n_still_fp = int((pred_mask(nd_all, f"PRE:{HEAD_M}", HEAD_EPS) & ~nd_all.tie_U).sum())
    else:
        hr = hr_x = dict(n_pred=0, P_pred_given_tie=np.nan, P_tie_given_pred=np.nan)
        n_still_fp = len(FP_DEC)
    mono = all(rates(LC, f"PRE:{MLADDER[i]}", HEAD_EPS)["n_pred"] >=
               rates(LC, f"PRE:{MLADDER[i+1]}", HEAD_EPS)["n_pred"]
               for i in range(len(MLADDER) - 1))
    cheaper = (bool(pre_lost_head < POST_HEAD_LOST) if HEAD_M is not None else NA)

    H = [("H_REPRO   this run reproduces 813's corpus and 817's columns (G5a/G5b/G7)", bool(g5)),
         ("H_SUFF1   some rung m returns sufficiency 1.0000 on QUALIFY, ALL families",
          bool(len(suff1_rungs) > 0)),
         (f"H_POWER   at the headline rung #pred >= {PRED_BAR}",
          bool(hr["n_pred"] >= PRED_BAR) if HEAD_M is not None else NA),
         ("H_NEC1    at the headline rung necessity = 1.0000 [LOAD-BEARING]",
          bool(hr["P_pred_given_tie"] == 1.0) if HEAD_M is not None else NA),
         (f"H_CHEAPER PRE's headline rung discards FEWER true ties than 817's POST k={POST_HEAD} "
          f"({POST_HEAD_LOST})", cheaper),
         ("H_PLATEAU two ADJACENT rungs meet sufficiency 1.0000 AND the power bar", bool(plateau)),
         ("H_ALLFP   the headline rung removes ALL 15 false positives, every window",
          bool(n_still_fp == 0) if HEAD_M is not None else NA),
         ("H_NONTRIV at the headline rung #pred exceeds the zero-cover-all-window count",
          bool(hr["n_pred"] > n_zero_window) if HEAD_M is not None else NA),
         (f"H_NOSPYDD sufficiency is 1.0000 at the headline rung with {CONFOUND} dropped",
          bool(hr_x["P_tie_given_pred"] == 1.0) if HEAD_M is not None else NA),
         ("H_COMPL   the terms are COMPLEMENTARY: PRE reaches FPs POST cannot and vice versa",
          bool(len([k for k in post_never if pre_rm[k]]) > 0
               and len([k for k in pre_never if post_rm[k]]) > 0)),
         ("H_MONO    #pred is monotone non-increasing along the m ladder", bool(mono))]

    P(f"\n{'='*112}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*112}")
    P(f"   corpus: the pooled long-decline cells ({len(long_cells)} (panel,window) cells, "
      f"{len(LC)} scored arms, {lc_r['n_tie']} ties, {lc_r['n_pred']} DECLINE-predicate arms).")
    P(f"   headline rung: m = {HEAD_M}" + ("" if ok_rungs else "  (NOT PROMOTED - fails a bar)")
      + f";  rungs reaching sufficiency 1.0000: {suff1_rungs or 'none'}")
    for nm, v in H:
        P(f"   {nm:<78} {'N/A - no qualifying rung' if v is NA else ('PASS' if v else 'FAIL')}")
    ev = [v for _, v in H if v is not NA]
    nna = sum(1 for _, v in H if v is NA)
    P(f"\n   {sum(bool(v) for v in ev)} of {len(ev)} EVALUABLE pre-registered hypotheses pass"
      + (f"; {nna} of {len(H)} are NOT EVALUABLE." if nna else "."))

    P(f"\n   THE ANSWER, in the three numbers the idea asks for, on the qualifying corpus:")
    P(f"   {'leg':<20} {'#pred':>6} {'necessity':>10} {'sufficiency':>12} {'two-directional?':>17}")
    for leg, lab in ([("DECLINE", "DECLINE (813)")] +
                     [(f"PRE:{m_}", f"+PRE m={m_}") for m_ in MLADDER] +
                     [(f"POST:{k}", f"+POST k={k} (817)") for k in KLADDER]):
        r = rates(LC, leg, HEAD_EPS)
        P(f"   {lab:<20} {r['n_pred']:>6} {r['P_pred_given_tie']:>10.4f} "
          f"{r['P_tie_given_pred']:>12.4f} {('YES' if r['exact'] else 'no'):>17}")
    P(f"\n   4b passers clearing BOTH windows and beating CONTROL-M, all windows: {clean_total}")
    P(f"   rule-8 picks passing 4b OOS: {int(WF.OOS_4b.sum())} of {len(WF)};  "
      f"4a OOS: {int(WF.OOS_4a.sum())} of {len(WF)}")

    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, E=E, WF=WF, LC=LC, FP=FP_DEC, H=H, HEAD_M=HEAD_M, ML=ML)


if __name__ == "__main__":
    main()
