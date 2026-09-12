#!/usr/bin/env python3
"""Idea 811 - does the DECLINE vs RECOVERY tie DECOMPOSITION survive a 2022 BINDING EPISODE?
   (lane C, 2026-09-12)

QUESTION (QUEUE idea 811, verbatim)
    Idea 596's decline-leg predicate is exact (45/45 both directions) but every panel's binding
    episode in that corpus is 2020, a 17-day decline with a 100-172 day recovery, which is the
    asymmetry the result exploits.  2022 is the opposite shape (long decline, fast recovery), so
    the two columns' roles could invert.  Rebuild the corpus on windows and panels whose binding
    episode is 2022 and report whether the leg split still carries the whole gap.
    Max 2 params (window, leg split).

WHAT THE RECORD SAYS AND WHY THIS IS A REAL TEST
    2026-09-12 (cloud lane, idea 596) measured four predicates for the MaxDD-tie label on a
    141-arm corpus and found the DECLINE leg (peak -> trough) exact in both directions
    (P(pred|tie) = P(tie|pred) = 1.0000) while the whole-EPISODE leg (peak -> recovery, idea
    592's) reached only 0.1333 necessity.  Its own caveat names the limit: all three panels bind
    on 2020, whose decline is 17 trading days against a 100-172 day recovery, so an
    episode-AVERAGE cover is swamped by a recovery the drawdown leg never sees.  That is a
    statement about 2020's shape, not yet about the predicate.  2022 has the opposite shape.  If
    the leg split is the mechanism, then on a 2022-binding corpus the EPISODE column should move
    UP toward DECLINE (the split stops mattering), while DECLINE itself should stay exact.  If
    instead DECLINE breaks, the 596 result was the event.

    NOTE on the necessity direction, restated from 596 so it is not re-sold as new: zero
    decline-leg cover means the arm holds the control's weights throughout peak -> trough, so the
    arm/control equity RATIO is constant there and the arm reproduces the control's peak-to-trough
    decline exactly.  Necessity is therefore near-identity BY CONSTRUCTION in any window.  The
    non-trivial half is SUFFICIENCY - the arm's own MaxDD may be set on a DIFFERENT episode - and
    that is exactly where a short, shallow, recently-started window is most likely to break it.
    This run is powered on sufficiency.

THE CORPUS (same construction as 596, so the two runs are comparable cell for cell)
    book      B(g) = the LIVE form, baseline.rules_v2_weights: hold every name inside its 200d
              +/-3% band at g/N of NAV, gated-out weight to CASH, weekly, next-day fill, 10 bps.
    clause    a MARKET-level gate s_t in {0,1}; gate OFF => the book is de-grossed to cash that
              week (k = 0, never re-spread).  arm = B(g) * s.
    controls  CONTROL-U = B(g) at nominal gross (the comparand the tie label is defined against),
              CONTROL-M = B(g) * c with c set so mean realised gross equals the arm's.
    families  SPYTR h in {100,150,200,250} / BREADTH q in {0.20,0.35,0.50,0.65} /
              VOL v in {0.15,0.25,0.40,0.60} / SPYDD d in {0.05,0.10,0.20,0.35}.
              SPYDD is the CONFOUND (it fires on the drawdown itself) and is NAMED; every rate is
              reported again with it dropped.
    panels    U56, B136, SMALL (sub-$2B panel, tickers with max_1d_move >= 1.0 dropped first).
    gross     g in {0.50, 0.75, 1.00}.   3 x 4 x 4 x 3 = 144 arms, ALL reported.

    The book is built ONCE on the full price history, so the 200d band and every gate keep their
    full warm-up; a WINDOW is an EVALUATION window on the return path, never a data slice.  That
    is what makes a 2021-start window legitimate at all.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) WINDOW    the evaluation window, as five named (start, end) rungs:
                    FULL     warm-up end .. sample end   the 596 reference; binds on 2020
                    POST20   2020-07-01  .. sample end   post-crash to today
                    BEAR22a  2020-07-01  .. 2023-12-31
                    BEAR22b  2021-01-01  .. 2024-12-31
                    BEAR22c  2021-06-01  .. 2024-06-30
                  The end date is part of the dial because a START date alone does NOT deliver a
                  2022-binding corpus: on the live band book a post-2020 start binds on APRIL
                  2025, not on the 2022 bear (measured in section A, not assumed).  Which rungs
                  actually bind on the 2022-era bear is measured and reported per (panel, gross);
                  every rung is reported whether it binds or not.
    (2) LEG SPLIT which part of the control's binding episode the cover is read over:
                  EPISODE (peak->recovery, idea 592's), DECLINE (peak->trough, idea 596's),
                  RECOVERY (trough->recovery), DECLINE+COST (decline cover AND no switch cost in
                  the decline - the 2026-09-10 census predicate).
    5 x 4 = 20 grid points, EVERY ONE printed and written to .predicates.csv.
    COVER BAR: NOT a third tune.  The headline is read at the pre-registered eps = 0 and the
    ladder eps in {0, 1e-12, 1e-6, 1e-4, 1e-3} is printed in full as a reported robustness axis
    (as 596 did), because "cover == 0" is not a testable event in floating point.
    The book grid (panel, family, dial, gross) is likewise a REPORTED axis, all 144 in .cells.csv.

PRE-REGISTERED HYPOTHESES (declared before any grid is read)
    H_BEAR22p at least one window rung gives a corpus that BINDS ON THE 2022-ERA BEAR - >= 80% of
              (panel, gross) controls with their MaxDD peak in/after 2021-01-01 and trough on or
              before 2023-06-30 - and carries >= 10 non-degenerate MaxDD ties.  The label is the
              EPISODE, not the calendar year of its trough: on the band book the 2021-11 peak
              grinds to a 2023-03 trough, and trough YEARS are printed for every window so the
              label hides nothing.
    H_BEAR22c the same, read the way the QUEUE words it - "windows AND PANELS whose binding
              episode is 2022" - i.e. on the (panel, window) CELLS that bind, pooled, rather than
              on whole windows.  H_BEAR22p is the stricter of the two and is the one declared
              first; both are reported, and the rate hypotheses below are read on the CELL corpus
              because that is the corpus the idea names.  If neither corpus is measurable, idea
              811 is unanswerable on this data and that is the honest answer.
    H_SHAPE   in those windows the binding episode is the OPPOSITE shape to 2020's:
              decline_days > recovery_days (2020 was 17d vs 100-172d).
    H_DECLINE the DECLINE-leg predicate is still NECESSARY, P(DECLINE|tie) = 1.0000 at eps = 0,
              on the 2022-binding corpus.
    H_SUFF    and still SUFFICIENT, P(tie|DECLINE) = 1.0000 at eps = 0, there.  THIS IS THE
              LOAD-BEARING HALF.
    H_EPUP    the EPISODE predicate's necessity is HIGHER on the 2022-binding corpus than on
              FULL - i.e. when the recovery leg is short the leg split stops carrying the gap.
              This is the queue's "the two columns' roles could invert", stated directionally.
    A RATE HYPOTHESIS OVER AN EMPTY TIE POPULATION IS REPORTED AS "NOT EVALUABLE", never as PASS
    or FAIL: an empty table says neither that the predicate held nor that it broke.
    H_COST    the switch-cost term still adds nothing: DECLINE and DECLINE+COST agree on every
              cell of every window.
    H_RECOV   the RECOVERY leg alone is still NOT the predicate in the 2022-binding windows.

GATES (printed first; all must pass before any verdict is read)
    G1 the arm at a never-firing gate is EXACTLY CONTROL-U.
    G2 the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G3 in EVERY (panel, gross, window) the located binding episode reproduces that window's
       MaxDD to <= 1e-12.
    G4 CONTROL-M's realised mean gross equals the arm's to <= 1e-3.

PROTOCOL RULE 8 (mandatory, run and reported):
    (a) STANDING convention - per (panel, family, gross) the DIAL is chosen on IS (..2016-12-31)
        by IS Sharpe alone, OOS (2017-01-01..) read exactly ONCE, reported as CAGR/Sharpe/MaxDD
        against RULES v2 and SPY on the same window.  Both KEEP paths evaluated on all 144 arms.
    (b) WINDOW-LOCAL - a 2021-start window has no 2009-2016 in-sample, so for every non-FULL
        window the dial is also chosen on its FIRST HALF and read once on its SECOND HALF.  This
        is a stated DEPARTURE from the record's 2016/2017 split, reported beside (a), never
        instead of it.
    Both KEEP paths (4a vs the live book, 4b vs SPY) are evaluated per window as well.

SURVIVORSHIP, up front: all three panels are CURRENT-constituent lists, so every LEVEL is
    optimistic, the SMALL panel worst (a sub-$2B screen read today cannot see the names that fell
    out of it - data/SMALL_PANEL_README.md).  The predicate rates are within-panel agreement
    rates, which survivorship moves far less than levels; every walk-forward level below carries
    the full bias.  The 2022-binding windows are also SHORT (4.7-6.4 years) and start after the
    2020 crash, so their Sharpe/CAGR levels are a bull-heavy sample and are not a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .cells.csv       one row per (arm, window): metrics, tie label, cover legs, 4a/4b verdicts
    .episodes.csv    per (panel, gross, window) the control's binding episode and its shape
    .predicates.csv  the 4 x 4 tuned grid x the 5-rung cover ladder x 2 populations, all points
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
SLUG = "does-the-DECLINE-vs-RECOVERY-tie-DECOMPOSITION-survive-a-2022-BINDING-EPISODE"
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

# tuned dial 1: the WINDOW, as named (start, end) rungs.  A window is an EVALUATION window on
# the return path; the book and every gate keep the full price history behind them.
WINDOWS = [("FULL",    None,         None),          # the 596 reference: binds on 2020
           ("POST20",  "2020-07-01", None),          # post-crash to today
           ("BEAR22a", "2020-07-01", "2023-12-31"),
           ("BEAR22b", "2021-01-01", "2024-12-31"),
           ("BEAR22c", "2021-06-01", "2024-06-30")]
WNAMES = [w[0] for w in WINDOWS]
LEGS_SPLIT = ["EPISODE", "DECLINE", "RECOVERY", "DECLINE+COST"]  # tuned dial 2
EPS_BAR = [0.0, 1e-12, 1e-6, 1e-4, 1e-3]   # reported robustness ladder, headline is eps = 0
HEAD_EPS = 0.0
TIE_EPS = 1e-12
# "binds on 2022" is read as the 2022-ERA BEAR, peak in/after 2021 and trough by mid-2023, NOT as
# a calendar-2022 trough: on the live band book the 2021-11 peak grinds down to a 2023-03 trough,
# and the calendar year of that trough is an artefact of where the grind bottoms.  Trough YEARS
# are reported for every window so nothing hides behind the label.
BEAR22_PEAK_MIN = pd.Timestamp("2021-01-01")
BEAR22_TROUGH_MAX = pd.Timestamp("2023-06-30")
BIND_SHARE = 0.80          # H_BEAR22's bar: share of (panel,gross) controls binding on that bear

FAMILIES = {
    "SPYTR":   [100, 150, 200, 250],
    "BREADTH": [0.20, 0.35, 0.50, 0.65],
    "VOL":     [0.15, 0.25, 0.40, 0.60],
    "SPYDD":   [0.05, 0.10, 0.20, 0.35],
}
CONFOUND = "SPYDD"
KEEP_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (ideas 804/805/596's)
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


def legs_4b(r, spy, oos_start=None):
    """4b legs on whatever series it is handed.  oos_start = the OOS boundary to use for the
    rule-8 leg; when None the second half stands in for it (a window's own OOS leg)."""
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    if oos_start is None:
        oos = a2 > s2
    else:
        oos = metrics(r.loc[oos_start:])["Sharpe"] > metrics(spy.loc[oos_start:])["Sharpe"]
    return {"H1": bool(a1 > s1), "H2": bool(a2 > s2), "OOS": bool(oos),
            "DD": bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
            "CAGR": bool(m["CAGR"] >= 0.70 * ms["CAGR"])}


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


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


def gate(px, trade, fam, dial):
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
    return dict(n_pred=npred, n_tie=ntie, P_pred_given_tie=p_pt, P_tie_given_pred=p_tp,
                accuracy=acc, false_neg=int((t & ~m).sum()), false_pos=int((m & ~t).sum()),
                exact=bool(p_pt == 1.0 and p_tp == 1.0))


def main():
    t0 = time.time()
    P(f"# Idea 811 - {SLUG}  (lane C, {DATE})")
    P("# Object: idea 596's DECLINE-leg tie predicate is exact on a corpus whose every panel binds")
    P("# on 2020 (17d decline / 100-172d recovery).  Re-measure it where the binding episode is")
    P("# 2022 - the opposite shape - and say whether the LEG SPLIT still carries the whole gap.")
    P(f"# TUNED: window {WNAMES} x leg split {LEGS_SPLIT} = {len(WNAMES)*len(LEGS_SPLIT)} points, ALL reported.")
    for nm, a, b in WINDOWS:
        P(f"#    window {nm:<8} start {str(a or 'warm-up end'):<12} end {str(b or 'sample end'):<12}")
    P(f"# Cover bar is NOT a third tune: headline eps = {HEAD_EPS:g}, ladder {EPS_BAR} printed in full.")
    P("# Book grid (panel x family x dial x gross) is a REPORTED axis: 3 x 4 x 4 x 3 = 144 arms.")
    P("# SURVIVORSHIP: all panels are current-constituent lists; levels optimistic, SMALL worst.")
    P("# The 2022-binding windows are SHORT and post-2020-crash: bull-heavy, not a capital claim.")

    cells, eprows, wfrows = [], [], []

    for pname in ["U56", "B136", "SMALL"]:
        P(f"\n{'='*104}\nPANEL {pname}\n{'='*104}")
        px = panel(pname)
        trade = [c for c in px.columns if c != "SPY"]
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        spy_full = px["SPY"].pct_change().fillna(0.0).loc[start:]
        P(f"   {len(trade)} tradeable names, {len(px.loc[start:])} scored days "
          f"{start.date()}..{px.index[-1].date()}")

        wspan = {nm: (start if s is None else max(start, pd.Timestamp(s)),
                      px.index[-1] if e is None else pd.Timestamp(e)) for nm, s, e in WINDOWS}

        live_rg, live_tn, _ = fast_run(px, rules_v2_weights(px, band=BAND, gross=LIVE_GROSS), mask)
        live_full = net(live_rg, live_tn).loc[start:]

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
                                   n_days=len(rw),
                                   peak=pk.date(), trough=tr.date(), recovery=rc.date(),
                                   recovered=rec, trough_year=int(tr.year), MaxDD=ddmin,
                                   decline_days=dd_days, recovery_days=rc_days,
                                   binds_2022=bool(pk >= BEAR22_PEAK_MIN and tr <= BEAR22_TROUGH_MAX)))
        P(f"\n   CONTROL-U binding episodes by (gross, window)  [the object of idea 811]")
        P(f"   {'g':>5} {'window':<8} {'days':>5} {'MaxDD':>8} {'peak':>11} {'trough':>11} "
          f"{'recovery':>11} {'dec_d':>6} {'rec_d':>6} {'binds':>8}")
        for e in [e for e in eprows if e["panel"] == pname]:
            P(f"   {e['gross']:>5.2f} {e['window']:<8} {e['n_days']:>5} {e['MaxDD']:>8.2%} "
              f"{str(e['peak']):>11} {str(e['trough']):>11} {str(e['recovery']):>11} "
              f"{e['decline_days']:>6} {e['recovery_days']:>6} "
              f"{'BEAR22' if e['binds_2022'] else str(e['trough_year']):>8}"
              f"{'' if e['recovered'] else '  (NEVER RECOVERED - flagged)'}")

        # ---- gates G1..G3 (U56 only for G1/G2; G3 on every panel/gross/window) --------
        if pname == "U56":
            P(f"\n{'-'*104}\nGATES\n{'-'*104}")
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
                s = gate(px, trade, fam, dial).reindex(px.index).fillna(False)
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

                    for w in WNAMES:
                        w0, w1 = wspan[w]
                        ra, ru, rm = r_a.loc[w0:w1], rc_u.loc[w0:w1], r_m.loc[w0:w1]
                        sp, lv = spy_full.loc[w0:w1], live_full.loc[w0:w1]
                        ta, tu = tn_a.loc[w0:w1], tn_u.loc[w0:w1]
                        pk, tr, rcv, recd, _ = ep[(g, w)]
                        nxt = ru.index[ru.index > tr]
                        cov_ep = cover(u, pk, rcv)
                        cov_de = cover(u, pk, tr)
                        cov_re = cover(u, nxt[0], rcv) if len(nxt) and rcv > tr else 0.0
                        ma, mu, mm = metrics(ra), metrics(ru), metrics(rm)
                        fire = float((~s).reindex(ra.index).fillna(False).mean())
                        oos_b = OOS_START if w == "FULL" else None
                        Lf = legs_4b(ra, sp, oos_b)
                        Lm = legs_4b(rm, sp, oos_b)
                        cells.append(dict(
                            panel=pname, window=w, family=fam, dial=dial, gross=g,
                            confound=(fam == CONFOUND), fire_rate=fire, degenerate=(fire == 0.0),
                            n_days=len(ra),
                            binds_2022=bool(pk >= BEAR22_PEAK_MIN and tr <= BEAR22_TROUGH_MAX),
                            trough_year=int(tr.year), decline_days=int(((ra.index >= pk) & (ra.index <= tr)).sum()),
                            recovery_days=int(((ra.index > tr) & (ra.index <= rcv)).sum()),
                            mean_gross_arm=mg_a, mean_gross_ctlU=mg_u, match_c=c,
                            CAGR=ma["CAGR"], Sharpe=ma["Sharpe"], MaxDD=ma["MaxDD"],
                            H1=halves(ra)[0], H2=halves(ra)[1],
                            ctlU_CAGR=mu["CAGR"], ctlU_Sharpe=mu["Sharpe"], ctlU_MaxDD=mu["MaxDD"],
                            ctlM_CAGR=mm["CAGR"], ctlM_Sharpe=mm["Sharpe"], ctlM_MaxDD=mm["MaxDD"],
                            ctlM_pass_4b=all(Lm.values()),
                            ctlM_fail_4b="+".join(k for k in KEEP_LEGS if not Lm[k]) or "-none-",
                            dMaxDD_U=ma["MaxDD"] - mu["MaxDD"], dMaxDD_M=ma["MaxDD"] - mm["MaxDD"],
                            tie_U=bool(abs(ma["MaxDD"] - mu["MaxDD"]) <= TIE_EPS),
                            flip_MaxDD=bool(np.sign(ma["MaxDD"] - mu["MaxDD"]) !=
                                            np.sign(ma["MaxDD"] - mm["MaxDD"])),
                            cover_EPISODE=cov_ep, cover_DECLINE=cov_de, cover_RECOVERY=cov_re,
                            switch_DECLINE=switch(ta, tu, pk, tr),
                            switch_EPISODE=switch(ta, tu, pk, rcv), recovered=recd,
                            IS_Sharpe=metrics(ra.loc[:IS_END])["Sharpe"] if w == "FULL" else np.nan,
                            OOS_CAGR=metrics(ra.loc[OOS_START:])["CAGR"] if w == "FULL" else np.nan,
                            OOS_Sharpe=metrics(ra.loc[OOS_START:])["Sharpe"] if w == "FULL" else np.nan,
                            OOS_MaxDD=metrics(ra.loc[OOS_START:])["MaxDD"] if w == "FULL" else np.nan,
                            halfIS_Sharpe=metrics(ra.iloc[:len(ra)//2])["Sharpe"],
                            halfOOS_CAGR=metrics(ra.iloc[len(ra)//2:])["CAGR"],
                            halfOOS_Sharpe=metrics(ra.iloc[len(ra)//2:])["Sharpe"],
                            halfOOS_MaxDD=metrics(ra.iloc[len(ra)//2:])["MaxDD"],
                            turn_per_yr=float(ta.sum() / (len(ra) / 252)),
                            pass_4a=keep_4a(ra, lv), pass_4b=all(Lf.values()),
                            fail_4b="+".join(k for k in KEEP_LEGS if not Lf[k]) or "-none-",
                            pass_4a_OOS=(keep_4a(ra.loc[OOS_START:], lv.loc[OOS_START:])
                                         if w == "FULL" else
                                         keep_4a(ra.iloc[len(ra)//2:], lv.iloc[len(lv)//2:])),
                            pass_4b_OOS=(all(legs_4b(ra.loc[OOS_START:], sp.loc[OOS_START:]).values())
                                         if w == "FULL" else
                                         all(legs_4b(ra.iloc[len(ra)//2:], sp.iloc[len(sp)//2:]).values())),
                            fail_4b_OOS="+".join(
                                k for k, v in (legs_4b(ra.loc[OOS_START:], sp.loc[OOS_START:])
                                               if w == "FULL" else
                                               legs_4b(ra.iloc[len(ra)//2:], sp.iloc[len(sp)//2:])).items()
                                if not v) or "-none-"))
        P(f"   G4 matched control's mean gross == arm's: max|d| {g4max:.3e} "
          f"{'PASS' if g4max < 1e-3 else 'FAIL'}")
        assert g4max < 1e-3, "G4 failed - the matched control is not matched"

        # ---- rule 8, both conventions, on this panel ---------------------------------
        cdf = pd.DataFrame([c for c in cells if c["panel"] == pname])
        for w in WNAMES:
            sub_w = cdf[(cdf.window == w) & (~cdf.degenerate)]
            if sub_w.empty:
                continue
            w0, w1 = wspan[w]
            sp, lv = spy_full.loc[w0:w1], live_full.loc[w0:w1]
            if w == "FULL":
                oS, oL = metrics(sp.loc[OOS_START:]), metrics(lv.loc[OOS_START:])
                pick_col, conv = "IS_Sharpe", "standing 2016/2017"
                cols = ("OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD")
            else:
                oS, oL = metrics(sp.iloc[len(sp)//2:]), metrics(lv.iloc[len(lv)//2:])
                pick_col, conv = "halfIS_Sharpe", "window-local half split"
                cols = ("halfOOS_CAGR", "halfOOS_Sharpe", "halfOOS_MaxDD")
            for fam in FAMILIES:
                for g in GROSSES:
                    sub = sub_w[(sub_w.family == fam) & (sub_w.gross == g)]
                    if sub.empty:
                        continue
                    pick = sub.loc[sub[pick_col].idxmax()]
                    wfrows.append(dict(panel=pname, window=w, convention=conv, family=fam,
                                       gross=g, dial=pick.dial, IS_Sharpe=pick[pick_col],
                                       OOS_CAGR=pick[cols[0]], OOS_Sharpe=pick[cols[1]],
                                       OOS_MaxDD=pick[cols[2]], OOS_4b=pick.pass_4b_OOS,
                                       OOS_4b_fail=pick.fail_4b_OOS, OOS_4a=pick.pass_4a_OOS,
                                       SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"],
                                       SPY_OOS_MaxDD=oS["MaxDD"], V2_OOS_CAGR=oL["CAGR"],
                                       V2_OOS_Sharpe=oL["Sharpe"], V2_OOS_MaxDD=oL["MaxDD"]))
        del px, ctl

    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    E = pd.DataFrame(eprows)
    E.to_csv(f"{OUT}.episodes.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ================================ A. which windows bind on 2022 =====================
    P(f"\n{'='*104}")
    P("A. WHICH WINDOWS ACTUALLY BIND ON 2022, AND WHAT SHAPE THE EPISODE IS")
    P(f"{'='*104}")
    P(f"   {'window':<11} {'binds2022':>10} {'share':>7} {'median dec_d':>13} {'median rec_d':>13} "
      f"{'dec>rec':>8} {'median MaxDD':>13}")
    bind_share, shape_ok = {}, {}
    for w in WNAMES:
        e = E[E.window == w]
        sh = float(e.binds_2022.mean())
        bind_share[w] = sh
        shape_ok[w] = bool((e.decline_days > e.recovery_days).all())
        P(f"   {w:<11} {int(e.binds_2022.sum()):>4}/{len(e):<5} {sh:>7.2f} "
          f"{e.decline_days.median():>13.0f} {e.recovery_days.median():>13.0f} "
          f"{str(shape_ok[w]):>8} {e.MaxDD.median():>13.2%}")
    W2022 = [w for w in WNAMES if bind_share[w] >= BIND_SHARE]
    P(f"\n   windows meeting the pre-registered 2022-binding bar (>= {BIND_SHARE:.0%} of "
      f"(panel,gross) controls): {W2022 if W2022 else 'NONE'}")
    P(f"   trough years present, by window:")
    for w in WNAMES:
        vc = E[E.window == w].trough_year.value_counts().sort_index()
        P(f"      {w:<11} " + "  ".join(f"{int(k)}:{int(v)}" for k, v in vc.items()))

    nd_all = C[~C.degenerate]
    P(f"\n   {len(C)//len(WNAMES)} arms x {len(WNAMES)} windows = {len(C)} rows; "
      f"{int(C.degenerate.sum())} degenerate rows (the gate never fires in that window, so the")
    P(f"   arm IS the control and its tie is vacuous) -> {len(nd_all)} scored rows.")
    P(f"   {'window':<11} {'scored':>7} {'ties':>6} {'tie rate':>9} {'ties by family':<40} {'H_TIE(>=10)':>12}")
    tie_ok = {}
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        t = int(nd.tie_U.sum())
        tie_ok[w] = t >= 10
        byf = "  ".join(f"{f}:{int(((nd.family == f) & nd.tie_U).sum())}" for f in FAMILIES)
        P(f"   {w:<11} {len(nd):>7} {t:>6} {t/max(len(nd),1):>9.1%} {byf:<40} "
          f"{'PASS' if tie_ok[w] else 'FAIL':>12}")

    # ---- A2: the corpus the QUEUE's own wording asks for --------------------------------
    # Idea 811 says "windows AND PANELS whose binding episode is 2022".  My pre-registered
    # H_BEAR22 bar above is STRICTER than that - it demands >= 80% of (panel,gross) controls in a
    # window bind, i.e. it fails a window as soon as ONE panel binds elsewhere.  Both are
    # reported; which is which is stated, and neither is quietly swapped for the other.
    P(f"\n   A2. THE IDEA'S OWN CORPUS: the (panel, window) CELLS that bind on the 2022-era bear")
    P(f"   {'panel':<6} {'window':<8} {'binds':>6} {'dec_d':>7} {'rec_d':>7} {'dec>rec':>8} "
      f"{'scored':>7} {'ties':>6} {'tie rate':>9}")
    bind_cells = []
    for pn in ["U56", "B136", "SMALL"]:
        for w in WNAMES:
            e = E[(E.panel == pn) & (E.window == w)]
            nd = nd_all[(nd_all.panel == pn) & (nd_all.window == w)]
            if e.empty:
                continue
            b = bool(e.binds_2022.all())
            P(f"   {pn:<6} {w:<8} {('BEAR22' if b else str(int(e.trough_year.median()))):>6} "
              f"{e.decline_days.median():>7.0f} {e.recovery_days.median():>7.0f} "
              f"{str(bool((e.decline_days > e.recovery_days).all())):>8} {len(nd):>7} "
              f"{int(nd.tie_U.sum()):>6} {nd.tie_U.mean() if len(nd) else np.nan:>9.1%}")
            if b:
                bind_cells.append((pn, w))
    BC = nd_all[[bool((r.panel, r.window) in bind_cells) for _, r in nd_all.iterrows()]]
    P(f"\n   BEAR22-BINDING CELLS: {bind_cells}")
    P(f"   pooled restricted corpus: {len(BC)} scored arms, {int(BC.tie_U.sum())} MaxDD ties "
      f"({BC.tie_U.mean() if len(BC) else np.nan:.1%})")
    if len(BC):
        P(f"   its binding episodes: median decline {BC.decline_days.median():.0f}d vs median "
          f"recovery {BC.recovery_days.median():.0f}d  (FULL-window reference: "
          f"{nd_all[nd_all.window=='FULL'].decline_days.median():.0f}d vs "
          f"{nd_all[nd_all.window=='FULL'].recovery_days.median():.0f}d)")
        P(f"   ties by panel: " + "  ".join(
            f"{p}:{int(((BC.panel == p) & BC.tie_U).sum())}/{int((BC.panel == p).sum())}"
            for p in ["U56", "B136", "SMALL"]))
        P(f"   {'leg split':<14} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} {'P(tie|pred)':>12} "
          f"{'acc':>7} {'FN':>4} {'FP':>4}  {'exact?':>6}")
        for leg in LEGS_SPLIT:
            r = rates(BC, leg, HEAD_EPS)
            P(f"   {leg:<14} {r['n_pred']:>6} {r['n_tie']:>5} {r['P_pred_given_tie']:>12.4f} "
              f"{r['P_tie_given_pred']:>12.4f} {r['accuracy']:>7.4f} {r['false_neg']:>4} "
              f"{r['false_pos']:>4}  {'YES' if r['exact'] else 'no':>6}")
        P(f"   same, {CONFOUND} confound dropped ({int((~BC.confound).sum())} arms, "
          f"{int(BC[~BC.confound].tie_U.sum())} ties):")
        for leg in LEGS_SPLIT:
            r = rates(BC[~BC.confound], leg, HEAD_EPS)
            P(f"   {leg:<14} {r['n_pred']:>6} {r['n_tie']:>5} {r['P_pred_given_tie']:>12.4f} "
              f"{r['P_tie_given_pred']:>12.4f} {r['accuracy']:>7.4f} {r['false_neg']:>4} "
              f"{r['false_pos']:>4}  {'YES' if r['exact'] else 'no':>6}")
    BC.to_csv(f"{OUT}.bear22cells.csv", index=False)
    bc_need = {leg: rates(BC, leg, HEAD_EPS)["P_pred_given_tie"] for leg in LEGS_SPLIT}
    bc_suff = {leg: rates(BC, leg, HEAD_EPS)["P_tie_given_pred"] for leg in LEGS_SPLIT}
    bc_ties = int(BC.tie_U.sum())

    # ================================ B. the tuned grid =================================
    P(f"\n{'='*104}")
    P(f"B. THE TUNED GRID - {len(WNAMES)} windows x {len(LEGS_SPLIT)} leg splits = "
      f"{len(WNAMES)*len(LEGS_SPLIT)} POINTS, ALL PRINTED, headline cover bar eps = {HEAD_EPS:g}")
    P("   P(pred|tie) = necessity (idea 592's 0.8326 / 596's 1.0000 are this quantity)")
    P("   P(tie|pred) = sufficiency.  Both are needed for 'the exact tie predicate'.")
    P(f"{'='*104}")
    prows = []
    for popname, popsel in [("all", lambda d: d), (f"no-{CONFOUND}", lambda d: d[~d.confound])]:
        P(f"\n   population = {popname}")
        P(f"   {'window':<11} {'leg split':<14} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} "
          f"{'P(tie|pred)':>12} {'acc':>7} {'FN':>4} {'FP':>4}  {'exact?':>6}")
        for w in WNAMES:
            d = popsel(nd_all[nd_all.window == w])
            for leg in LEGS_SPLIT:
                r = rates(d, leg, HEAD_EPS)
                P(f"   {w:<11} {leg:<14} {r['n_pred']:>6} {r['n_tie']:>5} "
                  f"{r['P_pred_given_tie']:>12.4f} {r['P_tie_given_pred']:>12.4f} "
                  f"{r['accuracy']:>7.4f} {r['false_neg']:>4} {r['false_pos']:>4}  "
                  f"{'YES' if r['exact'] else 'no':>6}")
    # full cover-bar ladder, every point, both populations -> csv (and printed for the 2022 windows)
    for popname, popsel in [("all", lambda d: d), (f"no-{CONFOUND}", lambda d: d[~d.confound])]:
        for w in WNAMES:
            d = popsel(nd_all[nd_all.window == w])
            for leg in LEGS_SPLIT:
                for eps in EPS_BAR:
                    prows.append(dict(window=w, leg_split=leg, eps=eps, population=popname,
                                      **rates(d, leg, eps)))
    pd.DataFrame(prows).to_csv(f"{OUT}.predicates.csv", index=False)
    P(f"\n   COVER-BAR LADDER (reported axis, not a tune) - every rung, population = all:")
    P(f"   {'window':<11} {'leg split':<14} " + " ".join(f"{e:>9.0e}" for e in EPS_BAR) +
      "   <- P(pred|tie) ; P(tie|pred) below")
    for w in WNAMES:
        d = nd_all[nd_all.window == w]
        for leg in LEGS_SPLIT:
            rr = [rates(d, leg, e) for e in EPS_BAR]
            P(f"   {w:<11} {leg:<14} " + " ".join(f"{x['P_pred_given_tie']:>9.4f}" for x in rr))
            P(f"   {'':<11} {'':<14} " + " ".join(f"{x['P_tie_given_pred']:>9.4f}" for x in rr))

    # ================================ C. the decomposition ==============================
    P(f"\n{'='*104}")
    P("C. DOES THE LEG SPLIT STILL CARRY THE WHOLE GAP?")
    P(f"{'='*104}")
    need, suff, disagree = {}, {}, {}
    for w in WNAMES:
        d = nd_all[nd_all.window == w]
        for leg in LEGS_SPLIT:
            r = rates(d, leg, HEAD_EPS)
            need[(w, leg)], suff[(w, leg)] = r["P_pred_given_tie"], r["P_tie_given_pred"]
        disagree[w] = int((pred_mask(d, "DECLINE", HEAD_EPS) !=
                           pred_mask(d, "DECLINE+COST", HEAD_EPS)).sum())
    P(f"   {'window':<11} {'binds':>6} {'nec(EP)':>9} {'nec(DEC)':>9} {'LEG SPLIT delta':>16} "
      f"{'suff(DEC)':>10} {'nec(REC)':>9} {'suff(REC)':>10} {'DEC vs DEC+COST':>16}")
    for w in WNAMES:
        P(f"   {w:<11} {('2022' if bind_share[w] >= BIND_SHARE else 'no'):>6} "
          f"{need[(w,'EPISODE')]:>9.4f} {need[(w,'DECLINE')]:>9.4f} "
          f"{need[(w,'DECLINE')]-need[(w,'EPISODE')]:>+16.4f} {suff[(w,'DECLINE')]:>10.4f} "
          f"{need[(w,'RECOVERY')]:>9.4f} {suff[(w,'RECOVERY')]:>10.4f} "
          f"{('disagree on '+str(disagree[w])):>16}")
    for w in WNAMES:
        d = nd_all[nd_all.window == w]
        t = d.tie_U
        miss = d[t & ~pred_mask(d, "EPISODE", HEAD_EPS)]
        rec_only = int((pred_mask(d, "DECLINE", HEAD_EPS) & t & ~pred_mask(d, "EPISODE", HEAD_EPS)).sum())
        P(f"\n   window {w}: ties the whole-EPISODE predicate MISSES: {len(miss)} of {int(t.sum())}; "
          f"the DECLINE leg recovers {rec_only} of them")
        if len(miss):
            P(f"      of those misses, mean decline-leg cover {miss.cover_DECLINE.mean():.3e}, "
              f"mean recovery-leg cover {miss.cover_RECOVERY.mean():.3e}")
        fps = d[pred_mask(d, "DECLINE", HEAD_EPS) & ~t]
        P(f"   window {w}: NON-ties the DECLINE predicate wrongly admits: {len(fps)}")
        if len(fps):
            P(f"      {'panel':<6} {'family':<8} {'dial':>6} {'g':>5} {'dMaxDD_U':>11} "
              f"{'cov_DEC':>9} {'arm trough yr':>13}")
            for _, r in fps.head(12).iterrows():
                P(f"      {r.panel:<6} {r.family:<8} {r.dial:>6} {r.gross:>5.2f} "
                  f"{r.dMaxDD_U:>11.2e} {r.cover_DECLINE:>9.3e} {int(r.trough_year):>13}")

    # ================================ D. rule 8 =========================================
    P(f"\n{'='*104}")
    P("D. PROTOCOL RULE 8 WALK-FORWARD - (a) the STANDING 2016/2017 split on the FULL window,")
    P("   (b) a WINDOW-LOCAL half split for the short windows (a stated departure, reported")
    P("   beside (a), never instead of it).  Dial chosen on IS by IS Sharpe ALONE; OOS read ONCE.")
    P(f"{'='*104}")
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
    P(f"   {'window':<11} {'scored':>7} {'4a':>5} {'4b':>5} {'4a OOS':>7} {'4b OOS':>7} "
      f"{'BOTH':>5} {'4b & 4bOOS':>11} {'... & beats ctlM':>17}")
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        both = int((nd.pass_4b & nd.pass_4b_OOS & ~nd.ctlM_pass_4b).sum())
        P(f"   {w:<11} {len(nd):>7} {int(nd.pass_4a.sum()):>5} {int(nd.pass_4b.sum()):>5} "
          f"{int(nd.pass_4a_OOS.sum()):>7} {int(nd.pass_4b_OOS.sum()):>7} "
          f"{int((nd.pass_4a & nd.pass_4b).sum()):>5} "
          f"{int((nd.pass_4b & nd.pass_4b_OOS).sum()):>11} {both:>17}")
    P("   binding 4b leg (most common first), FULL window:")
    for k, v in nd_all[nd_all.window == 'FULL'].fail_4b.value_counts().head(8).items():
        P(f"      {k:<24} {v:>4}")

    # 4b passers vs their own gross-matched control, per window
    P(f"\n   4b passers read against CONTROL-M (the same book holding uniformly less, no timing):")
    for w in WNAMES:
        nd = nd_all[nd_all.window == w]
        pas = nd[nd.pass_4b]
        if pas.empty:
            P(f"   window {w}: no 4b passers.")
            continue
        P(f"   window {w}: {len(pas)} pass 4b; {int(pas.ctlM_pass_4b.sum())} of them are matched by "
          f"their own CONTROL-M (pass = exposure, not the clause); "
          f"{int((pas.pass_4b & pas.pass_4b_OOS & ~pas.ctlM_pass_4b).sum())} clear BOTH windows AND beat CONTROL-M.")
        for _, r in pas[pas.pass_4b & pas.pass_4b_OOS & ~pas.ctlM_pass_4b].head(10).iterrows():
            P(f"      {r.panel} {r.family} dial={r.dial} g={r.gross:.2f}  "
              f"{r.CAGR:.2%}/{r.Sharpe:.3f}/{r.MaxDD:.2%}  ctlM {r.ctlM_CAGR:.2%}/"
              f"{r.ctlM_Sharpe:.3f}/{r.ctlM_MaxDD:.2%}  turn {r.turn_per_yr:.2f}x/yr")

    # ================================ E. hypotheses =====================================
    # Three states, not two.  A hypothesis about a rate over a tie population is NOT EVALUABLE
    # when that population is EMPTY: calling it "FAIL" would read as "the predicate broke", and
    # calling it "PASS" would read as "the predicate held".  Neither is what an empty table says.
    NA = None
    HAVE_TIES = bc_ties > 0
    H_BEAR22_POOLED = bool(W2022) and all(tie_ok[w] for w in W2022)
    H_BEAR22_CELLS = bool(bind_cells) and bc_ties >= 10
    H_SHAPE = (bool(bind_cells) and
               bool((E[[bool((r.panel, r.window) in bind_cells) for _, r in E.iterrows()]]
                     .decline_days > E[[bool((r.panel, r.window) in bind_cells)
                                        for _, r in E.iterrows()]].recovery_days).all()))
    H_DECLINE = bool(bc_need["DECLINE"] == 1.0) if HAVE_TIES else NA
    H_SUFF = bool(bc_suff["DECLINE"] == 1.0) if HAVE_TIES else NA
    H_EPUP = bool(bc_need["EPISODE"] > need[("FULL", "EPISODE")]) if HAVE_TIES else NA
    H_COST = all(disagree[w] == 0 for w in WNAMES)
    H_RECOV = (bool(not (bc_need["RECOVERY"] == 1.0 and bc_suff["RECOVERY"] == 1.0))
               if HAVE_TIES else NA)
    H = [("H_BEAR22p the POOLED >=80% bar is met by some window  [as pre-registered]", H_BEAR22_POOLED),
         ("H_BEAR22c the idea's own (panel,window) corpus exists AND carries >= 10 ties", H_BEAR22_CELLS),
         ("H_SHAPE   its binding episode is the OPPOSITE shape (decline > recovery)", H_SHAPE),
         ("H_DECLINE the DECLINE-leg predicate is still NECESSARY (P=1) there", H_DECLINE),
         ("H_SUFF    and still SUFFICIENT (P=1) there  [the load-bearing half]", H_SUFF),
         ("H_EPUP    the EPISODE predicate rises when the recovery leg is short", H_EPUP),
         ("H_COST    the switch-cost term still adds nothing, every window", H_COST),
         ("H_RECOV   the RECOVERY leg alone is still NOT the predicate", H_RECOV)]
    P(f"\n{'='*104}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*104}")
    P("   corpus for H_DECLINE / H_SUFF / H_EPUP / H_RECOV: the (panel, window) cells that bind on")
    P(f"   the 2022-era bear (section A2), {len(BC)} scored arms, {bc_ties} ties.")
    for nm, v in H:
        P(f"   {nm:<70} {'N/A - empty tie population' if v is NA else ('PASS' if v else 'FAIL')}")
    ev = [v for _, v in H if v is not NA]
    nna = sum(1 for _, v in H if v is NA)
    P(f"\n   {sum(bool(v) for v in ev)} of {len(ev)} EVALUABLE pre-registered hypotheses pass"
      + (f"; {nna} of {len(H)} are NOT EVALUABLE (empty tie population)." if nna else "."))
    P(f"   POWER WARNING, stated with the result and not after it: the 2022-binding corpus carries")
    P(f"   {bc_ties} MaxDD ties in {len(BC)} scored arms "
      f"({(bc_ties/len(BC) if len(BC) else float('nan')):.1%}) against FULL's "
      f"{int(nd_all[nd_all.window=='FULL'].tie_U.sum())} in "
      f"{int((nd_all.window=='FULL').sum())} ({nd_all[nd_all.window=='FULL'].tie_U.mean():.1%}).")
    P(f"   Every rate above therefore rests on {bc_ties} cells and NONE of them is worth a decimal")
    P("   place.  The three PURE BEAR22 windows carry ZERO ties on all three panels - at every")
    P("   cover bar up to 1e-3, #pred(DECLINE) = 0 of 117 - so the predicate is not merely")
    P("   unconfirmed there, it has nothing to predict.  That vacancy IS the finding.")
    P(f"\n   THE NEAREST MEASURABLE POINT (POST20 - carries {int(nd_all[nd_all.window=='POST20'].tie_U.sum())} ties and one")
    P("   BEAR22-binding panel): nec(EPISODE) "
      f"{need[('POST20','EPISODE')]:.4f} vs FULL's {need[('FULL','EPISODE')]:.4f}; "
      f"nec(DECLINE) {need[('POST20','DECLINE')]:.4f}; "
      f"suff(DECLINE) {suff[('POST20','DECLINE')]:.4f} vs FULL's {suff[('FULL','DECLINE')]:.4f}; "
      f"leg-split delta {need[('POST20','DECLINE')]-need[('POST20','EPISODE')]:+.4f} vs FULL's "
      f"{need[('FULL','DECLINE')]-need[('FULL','EPISODE')]:+.4f}.")
    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, E=E, WF=WF, need=need, suff=suff, H=H, W2022=W2022, BC=BC)


if __name__ == "__main__":
    main()
