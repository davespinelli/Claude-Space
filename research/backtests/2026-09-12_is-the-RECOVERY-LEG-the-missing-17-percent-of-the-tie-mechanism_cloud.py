#!/usr/bin/env python3
"""Idea 596 - is the RECOVERY LEG the missing 17 percent of the tie mechanism?
   (cloud lane, 2026-09-12)

QUESTION (QUEUE idea 596, verbatim)
    Idea 592 found BIND == 0 (the clause never de-grossed through the control's binding
    drawdown episode) explains 83.26% of the MaxDD ties, with 229 ties carrying non-zero
    binding-episode cover.  Split each binding episode at its trough and test whether cover of
    the DECLINE leg alone closes the gap, which would make 'de-grossed before the trough' the
    exact tie predicate.  Max 2 params (leg split, cover bar).

WHAT THE RECORD ALREADY SAYS, AND WHY THIS RUN IS STILL A MEASUREMENT
    Idea 592's episodes are MAXIMAL UNDERWATER INTERVALS, peak -> trough -> RECOVERY: its BIND
    cover averages over the whole interval, recovery included.  The later census
    (2026-09-10_census-the-record-for-MaxDD-comparisons-that-are-EXACT-TIES_cloud) reported
    P(struct | tie) = 1.0000 on the real cells with a DIFFERENT predicate - no de-gross AND no
    switch cost inside peak -> TROUGH - and concluded 592's 83.26% was the shuffle population's
    number.  So the record now carries TWO changes at once between a 0.8326 predicate and a
    1.0000 one:
        (a) the WINDOW narrowed, peak->recovery  ->  peak->trough   (idea 596's hypothesis)
        (b) a SWITCH-COST term was added
    and nothing on the record says which of the two closes the gap.  That decomposition is this
    run's object, and it is answerable only by measuring (a) alone.

POPULATION: FRESH, NOT A BIT-REPRODUCTION (stated, with the reason)
    Idea 592's 83.26% lives on its BLOCK-SHUFFLE population.  This run does NOT rebuild those
    shuffles.  A predicate claimed to be EXACT is a claim about the predicate, not about the
    sample it was found on, so the stronger test is a population the predicate was not
    discovered on.  This run therefore builds its own clause/control corpus from scratch and
    reports the whole-episode predicate's rate on it beside the decline-leg one, so the
    comparison (a) is internal to one population and needs no cross-population splice.  The
    cost of this choice is stated: a rate measured here is NOT comparable to 0.8326 as a
    number, only the ORDERING of the predicates within this run is.

THE CORPUS
    book      B(g) = the LIVE form, baseline.rules_v2_weights: hold every name inside its 200d
              +/-3% band at g/N of NAV, N = instruments priced that day, gated-out weight to
              CASH, weekly cadence, next-day fill, 10 bps.
    clause    a MARKET-level gate state s_t in {0, 1}.  Gate OFF  =>  the whole book is
              de-grossed to CASH that week (k = 0, the record's DEGROSS convention, never
              re-spread).  arm = B(g) * s.
    controls  CONTROL-U  = B(g) at its nominal gross (the record's published comparand), and
              CONTROL-M  = B(g) * c, c = mean realised gross of the arm / mean realised gross of
              CONTROL-U - the same control "holding uniformly less".  Both are run, because the
              tie population is defined against CONTROL-U and the record's matched convention
              is what made ties interesting in the first place.
    families  SPYTR    gate ON when SPY > its own h-day mean,     h in {100, 150, 200, 250}
              BREADTH  gate ON when the share of panel names above their own 200d mean >= q,
                       q in {0.20, 0.35, 0.50, 0.65}
              VOL      gate ON when SPY vol20 <= v,               v in {0.15, 0.25, 0.40, 0.60}
              SPYDD    gate ON when SPY's drawdown from its running max >= -d,
                       d in {0.05, 0.10, 0.20, 0.35}
              SPYDD is the CONFOUND and is named as one: it fires on the drawdown itself, so it
              is mechanically aligned with the control's episodes.  Every rate below is reported
              pooled AND with SPYDD excluded.
    panels    U56 (55 tradeable), B136 (136 large caps), SMALL (the sub-$2B panel with every
              ticker whose data/small_meta.csv max_1d_move >= 1.0 DROPPED first).
    gross     g in {0.50, 0.75, 1.00}.
    4 families x 4 dials x 3 gross x 3 panels = 144 arms, ALL reported.

TUNED PARAMETERS: TWO, exactly the two the queue names, and both belong to the PREDICATE:
    (1) LEG SPLIT   which part of the control's binding episode the cover is read over:
                    EPISODE (peak->recovery, idea 592's), DECLINE (peak->trough, idea 596's),
                    RECOVERY (trough->recovery), DECLINE+COST (decline cover AND no switch cost
                    inside the decline - the 2026-09-10 predicate, included so the decomposition
                    is complete).
    (2) COVER BAR   eps in {0, 1e-12, 1e-6, 1e-4, 1e-3}: "cover == 0" is not a testable event in
                    floating point, so the bar is a reported ladder, not a hidden choice.
    4 x 5 = 20 grid points, every one printed and written to .predicates.csv.
    The book grid (panel, family, dial, gross) is a REPORTED axis, not a dial: all 144 arms
    appear in .cells.csv.  Rule 8's dial pick is PROTOCOL's own selector, not a third tune.

PRE-REGISTERED HYPOTHESES (declared before the grid is read)
    H_TIE     : the corpus contains MaxDD ties at all (>= 10 non-degenerate ties).  If it does
                not, no predicate is distinguishable here and that is the honest answer.
    H_EP_GAP  : the whole-episode predicate is NOT exact on this corpus, i.e. P(EPISODE | tie)
                < 1.0000 at eps = 0 - there is a gap for the leg split to close.
    H_DECLINE : the decline-leg predicate IS exact: P(DECLINE | tie) = 1.0000 at eps = 0.
                THIS IS IDEA 596'S HYPOTHESIS.
    H_SUFF    : the decline leg is also SUFFICIENT, P(tie | DECLINE) = 1.0000 - i.e. the
                predicate is an identity and not merely necessary.
    H_COST    : the switch-cost term adds nothing once the window is the decline leg
                (DECLINE and DECLINE+COST agree on every cell).  If it DOES add something, the
                2026-09-10 predicate's exactness is the cost term's doing, not the leg split's.
    H_RECOV   : the recovery leg alone is NOT the predicate (P(tie | RECOVERY) < 1.0000) - the
                control reading that stops "any window works" from passing as a finding.

GATES (printed first; all must pass before any verdict is read)
    G1  the arm at a never-firing dial is EXACTLY the control (the clause is a real clause).
    G2  the vectorised runner reproduces products/backtester/engine.backtest to <= 1e-9.
    G3  the binding episode contains the control's MaxDD trough and reproduces its MaxDD to
        <= 1e-12 (the DD leg really is decided inside it).
    G4  the matched control's realised mean gross equals the arm's to <= 1e-3 (the match is a
        match).

RULE 8 (PROTOCOL rule 8, mandatory): per (panel, family, gross) the DIAL is chosen on
    IS (..2016-12-31) by IS Sharpe ALONE, ties -> first dial; OOS (2017-01-01..) is read exactly
    once and reported against RULES v2 and SPY on the same window.  Both KEEP paths (4a vs the
    live book, 4b vs SPY) are evaluated on every one of the 144 arms, full sample and OOS.

SURVIVORSHIP, stated up front: all three panels are CURRENT-constituent lists, so every LEVEL
    is optimistic.  The SMALL panel is the worst case - a sub-$2B screen read today cannot see
    the names that fell out of it - and its own README says so.  What this run measures is a
    PREDICATE's agreement with a tie label inside each panel, which survivorship moves far less
    than it moves levels; the walk-forward levels below carry the full caveat.

Outputs (all committed under research/backtests/):
    .console.txt     full log
    .cells.csv       one row per arm: metrics, tie label, cover legs, 4a/4b verdicts
    .predicates.csv  the 4 x 5 predicate grid, every point
    .episodes.csv    per (panel, gross) the control's binding episode: peak, trough, recovery
    .walkforward.csv rule-8 IS picks and the OOS read vs RULES v2 and SPY
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
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask              # noqa: E402

DATE = "2026-09-12"
SLUG = "is-the-RECOVERY-LEG-the-missing-17-percent-of-the-tie-mechanism"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

FREQ = "W"
LAG = 1
COST = 10
BAND = 0.03
GROSSES = [0.50, 0.75, 1.00]
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SMALL_MAXMOVE = 1.0                      # mandated filter on data/small_meta.csv

LEGS_SPLIT = ["EPISODE", "DECLINE", "RECOVERY", "DECLINE+COST"]   # tuned dial 1
EPS_BAR = [0.0, 1e-12, 1e-6, 1e-4, 1e-3]                          # tuned dial 2
TIE_EPS = 1e-12                           # what "MaxDD tie" means, stated not hidden

FAMILIES = {
    "SPYTR":   [100, 150, 200, 250],
    "BREADTH": [0.20, 0.35, 0.50, 0.65],
    "VOL":     [0.15, 0.25, 0.40, 0.60],
    "SPYDD":   [0.05, 0.10, 0.20, 0.35],   # the confound, named
}
CONFOUND = "SPYDD"
KEEP_LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ runner (ideas 804/805's)
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


def legs_4b(r, spy, lo=None, hi=None, oos_leg_window=True):
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


# ------------------------------------------------------------------ episodes
def binding_episode(r: pd.Series):
    """(peak, trough, recovery) of the control's MaxDD episode.  recovery = the first day after
    the trough at which equity regains the peak, or the last day of the sample if it never does
    (that case is flagged, not silently treated as a recovery)."""
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
    """Turnover the arm pays inside the window that the control does not (the switch cost)."""
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
    """Market-level gate state, True = ON (hold the book), False = de-gross to cash."""
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


def main():
    t0 = time.time()
    P(f"# Idea 596 - {SLUG}  (cloud lane, {DATE})")
    P("# Object: DECOMPOSE the record's move from a 0.8326 tie predicate (idea 592, window")
    P("# peak->RECOVERY) to a 1.0000 one (2026-09-10 census, window peak->TROUGH *plus* a")
    P("# switch-cost term) into its two changes, and say which one closes the gap.")
    P(f"# TUNED: leg split {LEGS_SPLIT} x cover bar {EPS_BAR} = {len(LEGS_SPLIT)*len(EPS_BAR)} points, all reported.")
    P(f"# Book grid (panel x family x dial x gross) is a REPORTED axis: 3 x 4 x 4 x 3 = 144 arms.")
    P("# SURVIVORSHIP: all three panels are current-constituent lists; every level is optimistic,")
    P("# the SMALL panel worst of all.  The predicate rates are within-panel agreement rates.")

    cells, eprows, wfrows = [], [], []
    gate_vals = {}

    for pname in ["U56", "B136", "SMALL"]:
        P(f"\n{'='*100}\nPANEL {pname}\n{'='*100}")
        px = panel(pname)
        trade = [c for c in px.columns if c != "SPY"]
        mask = rebalance_mask(px.index, FREQ)
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        P(f"   {len(trade)} tradeable names, {len(px.loc[start:])} scored days "
          f"{start.date()}..{px.index[-1].date()}")

        # live comparand (RULES v2 at its own live gross 0.75)
        live_rg, live_tn, _ = fast_run(px, rules_v2_weights(px, band=BAND, gross=0.75), mask)
        live = net(live_rg, live_tn).loc[start:]

        # controls, one per gross
        ctl: dict[float, tuple] = {}
        for g in GROSSES:
            Wb = rules_v2_weights(px, band=BAND, gross=g)
            rg, tn, gr = fast_run(px, Wb, mask)
            r = net(rg, tn).loc[start:]
            ctl[g] = (r, tn.loc[start:], gr.loc[start:], Wb)
            pk, tr, rc, rec, ddmin = binding_episode(r)
            eprows.append(dict(panel=pname, gross=g, peak=pk.date(), trough=tr.date(),
                               recovery=rc.date(), recovered=rec, MaxDD=ddmin,
                               decline_days=int(((r.index >= pk) & (r.index <= tr)).sum()),
                               recovery_days=int(((r.index > tr) & (r.index <= rc)).sum())))
            P(f"   CONTROL-U g={g:.2f}: CAGR {metrics(r)['CAGR']:.2%} Sharpe {metrics(r)['Sharpe']:.3f} "
              f"MaxDD {ddmin:.2%}  binding episode {pk.date()} -> {tr.date()} -> {rc.date()}"
              f"{'' if rec else '  (NEVER RECOVERED in sample - flagged)'}  "
              f"decline {eprows[-1]['decline_days']}d / recovery {eprows[-1]['recovery_days']}d")

        # ---- gates ---------------------------------------------------------------------
        if pname == "U56":
            P(f"\n{'-'*100}\nGATES\n{'-'*100}")
            g = 0.75
            _, _, _, Wb = ctl[g]
            never = Wb.mul(pd.Series(1.0, index=px.index), axis=0)            # gate always ON
            rg_n, tn_n, _ = fast_run(px, never, mask)
            g1 = max(float(np.abs((net(rg_n, tn_n).loc[start:] - ctl[g][0]).values).max()),
                     float(np.abs((tn_n.loc[start:] - ctl[g][1]).values).max()))
            eng = backtest(px, Wb, cost_bps=COST, freq=FREQ)
            g2 = float(np.abs((net(rg_n, tn_n) - eng["returns"]).loc[start:].values).max())
            rr = ctl[g][0]
            pk, tr, rc, _, ddm = binding_episode(rr)
            eq = (1 + rr).cumprod()
            g3 = abs((eq.loc[tr] / eq.loc[pk] - 1.0) - ddm)
            gate_vals = dict(g1=g1, g2=g2, g3=g3)
            for nm, v, ok in [("G1 never-firing arm == CONTROL-U exactly", f"max|d| {g1:.3e}", g1 < 1e-12),
                              ("G2 fast_run == engine.backtest", f"max|d| {g2:.3e}", g2 < 1e-9),
                              ("G3 binding episode reproduces the control's MaxDD", f"|d| {g3:.3e}", g3 < 1e-12)]:
                P(f"   {nm:<48} {v:<20} {'PASS' if ok else 'FAIL'}")
            assert g1 < 1e-12 and g2 < 1e-9 and g3 < 1e-12, "a gate failed - no verdict is read"

        # ---- arms ----------------------------------------------------------------------
        g4max = 0.0
        for fam, dials in FAMILIES.items():
            for dial in dials:
                s = gate(px, trade, fam, dial).reindex(px.index).fillna(False)
                fire_rate = float((~s).loc[start:].mean())        # share of days de-grossed
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
                    pk, tr, rcv, recd, _ = binding_episode(rc_u)
                    nxt = rc_u.index[rc_u.index > tr]
                    cov_ep = cover(u, pk, rcv)
                    cov_de = cover(u, pk, tr)
                    cov_re = cover(u, nxt[0], rcv) if len(nxt) and rcv > tr else 0.0
                    sw_de = switch(tn_a, tn_u, pk, tr)
                    sw_ep = switch(tn_a, tn_u, pk, rcv)

                    Lm_f = legs_4b(r_m, spy)
                    Lm_o = legs_4b(r_m, spy, OOS_START, None)
                    ma, mu, mm = metrics(r_a), metrics(rc_u), metrics(r_m)
                    tie_u = abs(ma["MaxDD"] - mu["MaxDD"]) <= TIE_EPS
                    degen = fire_rate == 0.0
                    Lf = legs_4b(r_a, spy)
                    Lo = legs_4b(r_a, spy, OOS_START, None)
                    mi, mo = metrics(r_a.loc[:IS_END]), metrics(r_a.loc[OOS_START:])
                    cells.append(dict(
                        panel=pname, family=fam, dial=dial, gross=g, confound=(fam == CONFOUND),
                        fire_rate=fire_rate, degenerate=degen, mean_gross_arm=mg_a,
                        mean_gross_ctlU=mg_u, match_c=c,
                        CAGR=ma["CAGR"], Sharpe=ma["Sharpe"], MaxDD=ma["MaxDD"],
                        H1=halves(r_a)[0], H2=halves(r_a)[1],
                        IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                        OOS_MaxDD=mo["MaxDD"], turn_per_yr=float(tn_a.sum() / (len(r_a) / 252)),
                        ctlU_MaxDD=mu["MaxDD"], ctlM_MaxDD=mm["MaxDD"],
                        ctlM_CAGR=mm["CAGR"], ctlM_Sharpe=mm["Sharpe"],
                        ctlM_pass_4b=all(Lm_f.values()), ctlM_pass_4b_OOS=all(Lm_o.values()),
                        ctlM_fail_4b="+".join(k for k in KEEP_LEGS if not Lm_f[k]) or "-none-",
                        dMaxDD_U=ma["MaxDD"] - mu["MaxDD"], dMaxDD_M=ma["MaxDD"] - mm["MaxDD"],
                        tie_U=tie_u, flip_MaxDD=bool(np.sign(ma["MaxDD"] - mu["MaxDD"]) !=
                                                     np.sign(ma["MaxDD"] - mm["MaxDD"])),
                        cover_EPISODE=cov_ep, cover_DECLINE=cov_de, cover_RECOVERY=cov_re,
                        switch_DECLINE=sw_de, switch_EPISODE=sw_ep, recovered=recd,
                        pass_4a=keep_4a(r_a, live), pass_4b=all(Lf.values()),
                        fail_4b="+".join(k for k in KEEP_LEGS if not Lf[k]) or "-none-",
                        pass_4a_OOS=keep_4a(r_a, live, OOS_START, None),
                        pass_4b_OOS=all(Lo.values()),
                        fail_4b_OOS="+".join(k for k in KEEP_LEGS if not Lo[k]) or "-none-"))
        P(f"   G4 matched control's mean gross == arm's: max|d| {g4max:.3e} "
          f"{'PASS' if g4max < 1e-3 else 'FAIL'}")
        assert g4max < 1e-3, "G4 failed - the matched control is not matched"

        # ---- rule 8 on this panel ------------------------------------------------------
        cdf = pd.DataFrame(cells)
        cdf = cdf[cdf.panel == pname]
        oS, oL = metrics(spy.loc[OOS_START:]), metrics(live.loc[OOS_START:])
        for fam in FAMILIES:
            for g in GROSSES:
                sub = cdf[(cdf.family == fam) & (cdf.gross == g)]
                sub = sub[~sub.degenerate]
                if sub.empty:
                    continue
                pick = sub.loc[sub.IS_Sharpe.idxmax()]
                wfrows.append(dict(panel=pname, family=fam, gross=g, dial=pick.dial,
                                   IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                                   OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   OOS_4b=pick.pass_4b_OOS, OOS_4b_fail=pick.fail_4b_OOS,
                                   OOS_4a=pick.pass_4a_OOS,
                                   SPY_OOS_CAGR=oS["CAGR"], SPY_OOS_Sharpe=oS["Sharpe"],
                                   SPY_OOS_MaxDD=oS["MaxDD"], V2_OOS_CAGR=oL["CAGR"],
                                   V2_OOS_Sharpe=oL["Sharpe"], V2_OOS_MaxDD=oL["MaxDD"]))

    C = pd.DataFrame(cells)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    pd.DataFrame(eprows).to_csv(f"{OUT}.episodes.csv", index=False)
    WF = pd.DataFrame(wfrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ================================ the predicate grid ================================
    P(f"\n{'='*100}")
    P("A. THE TIE POPULATION")
    P(f"{'='*100}")
    nd = C[~C.degenerate]
    P(f"   {len(C)} arms built; {int(C.degenerate.sum())} DEGENERATE (the gate never fires, so the")
    P(f"   arm IS the control and its tie is vacuous) -> {len(nd)} scored arms.")
    ties = nd[nd.tie_U]
    P(f"   MaxDD ties vs CONTROL-U at |d| <= {TIE_EPS:g}: {len(ties)} of {len(nd)} "
      f"({len(ties)/max(len(nd),1):.1%})")
    P(f"   MaxDD sign FLIPS (unmatched vs matched, idea 581's label): {int(nd.flip_MaxDD.sum())}")
    P(f"   ties by panel: " + "  ".join(f"{p}:{int((ties.panel==p).sum())}/{int((nd.panel==p).sum())}"
                                        for p in ["U56", "B136", "SMALL"]))
    P(f"   ties by family: " + "  ".join(f"{f}:{int((ties.family==f).sum())}" for f in FAMILIES))
    H_TIE = len(ties) >= 10
    P(f"   H_TIE (>= 10 non-degenerate ties, so the predicates are distinguishable at all): "
      f"{'PASS' if H_TIE else 'FAIL'}")

    P(f"\n{'='*100}")
    P(f"B. THE PREDICATE GRID - {len(LEGS_SPLIT)} leg splits x {len(EPS_BAR)} cover bars, ALL {len(LEGS_SPLIT)*len(EPS_BAR)} POINTS")
    P("   P(pred|tie) = necessity (idea 592's 0.8326 is this quantity on ITS population)")
    P("   P(tie|pred) = sufficiency.  Both are needed for 'the exact tie predicate'.")
    P(f"{'='*100}")

    def pred_mask(df, leg, eps):
        if leg == "EPISODE":
            return df.cover_EPISODE <= eps
        if leg == "DECLINE":
            return df.cover_DECLINE <= eps
        if leg == "RECOVERY":
            return df.cover_RECOVERY <= eps
        return (df.cover_DECLINE <= eps) & (df.switch_DECLINE <= eps)

    prows = []
    P(f"   {'leg split':<14} {'eps':>8} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} "
      f"{'P(tie|pred)':>12} {'acc':>7} {'FN':>4} {'FP':>4}  {'exact?':>6}")
    for leg in LEGS_SPLIT:
        for eps in EPS_BAR:
            m = pred_mask(nd, leg, eps)
            t = nd.tie_U
            npred, ntie = int(m.sum()), int(t.sum())
            p_pt = float((m & t).sum() / ntie) if ntie else np.nan
            p_tp = float((m & t).sum() / npred) if npred else np.nan
            acc = float(((m & t) | (~m & ~t)).mean())
            fn, fp = int((t & ~m).sum()), int((m & ~t).sum())
            exact = (p_pt == 1.0) and (p_tp == 1.0)
            prows.append(dict(leg_split=leg, eps=eps, n_pred=npred, n_tie=ntie,
                              P_pred_given_tie=p_pt, P_tie_given_pred=p_tp, accuracy=acc,
                              false_neg=fn, false_pos=fp, exact=exact, population="all"))
            P(f"   {leg:<14} {eps:>8.0e} {npred:>6} {ntie:>5} {p_pt:>12.4f} {p_tp:>12.4f} "
              f"{acc:>7.4f} {fn:>4} {fp:>4}  {'YES' if exact else 'no':>6}")
    # same grid with the confound family dropped
    ex = nd[~nd.confound]
    P(f"\n   SAME GRID with the {CONFOUND} confound family DROPPED ({len(ex)} arms, "
      f"{int(ex.tie_U.sum())} ties)")
    P(f"   {'leg split':<14} {'eps':>8} {'#pred':>6} {'#tie':>5} {'P(pred|tie)':>12} "
      f"{'P(tie|pred)':>12} {'acc':>7} {'FN':>4} {'FP':>4}  {'exact?':>6}")
    for leg in LEGS_SPLIT:
        for eps in EPS_BAR:
            m = pred_mask(ex, leg, eps)
            t = ex.tie_U
            npred, ntie = int(m.sum()), int(t.sum())
            p_pt = float((m & t).sum() / ntie) if ntie else np.nan
            p_tp = float((m & t).sum() / npred) if npred else np.nan
            acc = float(((m & t) | (~m & ~t)).mean())
            fn, fp = int((t & ~m).sum()), int((m & ~t).sum())
            exact = (p_pt == 1.0) and (p_tp == 1.0)
            prows.append(dict(leg_split=leg, eps=eps, n_pred=npred, n_tie=ntie,
                              P_pred_given_tie=p_pt, P_tie_given_pred=p_tp, accuracy=acc,
                              false_neg=fn, false_pos=fp, exact=exact, population=f"no-{CONFOUND}"))
            P(f"   {leg:<14} {eps:>8.0e} {npred:>6} {ntie:>5} {p_pt:>12.4f} {p_tp:>12.4f} "
              f"{acc:>7.4f} {fn:>4} {fp:>4}  {'YES' if exact else 'no':>6}")
    pd.DataFrame(prows).to_csv(f"{OUT}.predicates.csv", index=False)

    at0 = {leg: pred_mask(nd, leg, 0.0) for leg in LEGS_SPLIT}
    t = nd.tie_U
    need = {leg: (float((at0[leg] & t).sum() / t.sum()) if t.sum() else np.nan) for leg in LEGS_SPLIT}
    suff = {leg: (float((at0[leg] & t).sum() / at0[leg].sum()) if at0[leg].sum() else np.nan)
            for leg in LEGS_SPLIT}
    H_EP_GAP = bool(need["EPISODE"] < 1.0)
    H_DECLINE = bool(need["DECLINE"] == 1.0)
    H_SUFF = bool(suff["DECLINE"] == 1.0)
    H_COST = bool((at0["DECLINE"] == at0["DECLINE+COST"]).all())
    H_RECOV = bool(not (need["RECOVERY"] == 1.0 and suff["RECOVERY"] == 1.0))

    P(f"\n{'='*100}")
    P("C. THE DECOMPOSITION the record is missing: which change closes the gap?")
    P(f"{'='*100}")
    P(f"   at eps = 0, pooled over all {len(nd)} scored arms ({int(t.sum())} ties):")
    for leg in LEGS_SPLIT:
        P(f"      {leg:<14} P(pred|tie) {need[leg]:.4f}   P(tie|pred) {suff[leg]:.4f}   "
          f"#pred {int(at0[leg].sum()):>4}")
    P(f"   EPISODE -> DECLINE moves necessity by {need['DECLINE']-need['EPISODE']:+.4f} "
      f"(this is change (a), the LEG SPLIT - idea 596's hypothesis)")
    P(f"   DECLINE -> DECLINE+COST moves necessity by {need['DECLINE+COST']-need['DECLINE']:+.4f} "
      f"and sufficiency by {suff['DECLINE+COST']-suff['DECLINE']:+.4f} "
      f"(this is change (b), the SWITCH-COST term)")
    n_disagree = int((at0["DECLINE"] != at0["DECLINE+COST"]).sum())
    P(f"   cells where DECLINE and DECLINE+COST disagree: {n_disagree}")

    # the cells the whole-episode predicate gets wrong - what idea 596 is asking about
    miss = nd[t & ~at0["EPISODE"]]
    P(f"\n   TIES the whole-episode predicate MISSES (592's residual): {len(miss)}")
    if len(miss):
        P(f"   {'panel':<6} {'family':<8} {'dial':>6} {'gross':>6} {'cov_EP':>9} {'cov_DEC':>9} "
          f"{'cov_REC':>9} {'sw_DEC':>8}")
        for _, r in miss.iterrows():
            P(f"   {r.panel:<6} {r.family:<8} {r.dial:>6} {r.gross:>6.2f} {r.cover_EPISODE:>9.3e} "
              f"{r.cover_DECLINE:>9.3e} {r.cover_RECOVERY:>9.3e} {r.switch_DECLINE:>8.3e}")
        P(f"   of these, the DECLINE-leg predicate recovers {int((at0['DECLINE'] & t & ~at0['EPISODE']).sum())}"
          f" of {len(miss)} - i.e. their cover sits ENTIRELY in the recovery leg.")
    fps = nd[at0["DECLINE"] & ~t]
    P(f"\n   NON-ties the DECLINE predicate wrongly admits: {len(fps)}")
    if len(fps):
        P(f"   {'panel':<6} {'family':<8} {'dial':>6} {'gross':>6} {'dMaxDD_U':>10} {'cov_DEC':>9} {'sw_DEC':>9}")
        for _, r in fps.head(20).iterrows():
            P(f"   {r.panel:<6} {r.family:<8} {r.dial:>6} {r.gross:>6.2f} {r.dMaxDD_U:>10.2e} "
              f"{r.cover_DECLINE:>9.3e} {r.switch_DECLINE:>9.3e}")

    # ================================ rule 8 ============================================
    P(f"\n{'='*100}")
    P(f"D. RULE 8 WALK-FORWARD - dial chosen on IS (..{IS_END}) by IS Sharpe ALONE per")
    P(f"   (panel, family, gross); OOS ({OOS_START}..) read ONCE.  {COST} bps, weekly, lag {LAG}.")
    P(f"{'='*100}")
    P(f"   {'panel':<6} {'family':<8} {'gross':>6} {'dial':>6} {'ISSh':>6} {'OOSCAGR':>9} "
      f"{'OOSSh':>7} {'OOSDD':>8}  {'fail4b(OOS)':<16} {'4bOOS':>6} {'4aOOS':>6}")
    for _, r in WF.iterrows():
        P(f"   {r.panel:<6} {r.family:<8} {r.gross:>6.2f} {r.dial:>6} {r.IS_Sharpe:>6.3f} "
          f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>7.3f} {r.OOS_MaxDD:>8.2%}  {r.OOS_4b_fail:<16} "
          f"{'PASS' if r.OOS_4b else 'fail':>6} {'PASS' if r.OOS_4a else 'fail':>6}")
    P(f"\n   comparands on the OOS window, per panel:")
    for p in ["U56", "B136", "SMALL"]:
        s = WF[WF.panel == p]
        if s.empty:
            continue
        r = s.iloc[0]
        P(f"      {p:<6} SPY {r.SPY_OOS_CAGR:>7.2%} / {r.SPY_OOS_Sharpe:.3f} / {r.SPY_OOS_MaxDD:>7.2%}"
          f"      RULES v2 {r.V2_OOS_CAGR:>7.2%} / {r.V2_OOS_Sharpe:.3f} / {r.V2_OOS_MaxDD:>7.2%}")
    P(f"\n   rule-8 picks passing 4b OOS: {int(WF.OOS_4b.sum())} of {len(WF)};  "
      f"4a OOS: {int(WF.OOS_4a.sum())} of {len(WF)}")
    P(f"   over all {len(nd)} scored arms: 4a {int(nd.pass_4a.sum())} / 4b {int(nd.pass_4b.sum())} "
      f"(full sample), 4a {int(nd.pass_4a_OOS.sum())} / 4b {int(nd.pass_4b_OOS.sum())} (OOS window); "
      f"BOTH paths {int((nd.pass_4a & nd.pass_4b).sum())}")
    P("   binding 4b leg (full sample), most common first:")
    for k, v in nd.fail_4b.value_counts().head(10).items():
        P(f"      {k:<22} {v:>4}")

    # ============== E. the 4b passers this corpus threw up, against their OWN control =====
    P(f"\n{'='*100}")
    P("E. THE 4b PASSERS THIS CORPUS THREW UP - and the only question that matters about them:")
    P("   IS THE PASS TIMING, OR IS IT EXPOSURE?  Each arm is read against CONTROL-M, its own")
    P("   gross-matched control - the SAME book holding uniformly less, no timing at all.  The")
    P("   record's standing lesson (ideas 502 / 504 / 767) is that a gross-matched blend often")
    P("   clears 4b by itself; where it does, the arm's pass is its exposure, not its clause.")
    P(f"{'='*100}")
    pas = nd[nd.pass_4b]
    P(f"   {len(pas)} of {len(nd)} arms pass 4b on the full sample; "
      f"{int((nd.pass_4b & nd.pass_4b_OOS).sum())} pass on the full sample AND out of sample.")
    if len(pas):
        P(f"   {'panel':<6} {'family':<8} {'dial':>5} {'g':>5} {'mgross':>7} {'CAGR':>7} {'Sh':>6} "
          f"{'MaxDD':>8} {'H1':>6} {'H2':>6} {'OOSCAGR':>8} {'OOSSh':>6} {'turn':>5} "
          f"{'4bOOS':>6} | {'ctlM CAGR':>9} {'ctlM Sh':>7} {'ctlM DD':>8} {'ctlM4b':>7} {'ctlM4bOOS':>9}")
        for _, r in pas.iterrows():
            P(f"   {r.panel:<6} {r.family:<8} {r.dial:>5} {r.gross:>5.2f} {r.mean_gross_arm:>7.3f} "
              f"{r.CAGR:>7.2%} {r.Sharpe:>6.3f} {r.MaxDD:>8.2%} {r.H1:>6.3f} {r.H2:>6.3f} "
              f"{r.OOS_CAGR:>8.2%} {r.OOS_Sharpe:>6.3f} {r.turn_per_yr:>5.2f} "
              f"{'PASS' if r.pass_4b_OOS else 'fail':>6} | {r.ctlM_CAGR:>9.2%} {r.ctlM_Sharpe:>7.3f} "
              f"{r.ctlM_MaxDD:>8.2%} {'PASS' if r.ctlM_pass_4b else 'fail':>7} "
              f"{'PASS' if r.ctlM_pass_4b_OOS else 'fail':>9}")
        n_timing = int((pas.pass_4b & ~pas.ctlM_pass_4b).sum())
        P(f"\n   arms whose 4b pass their gross-matched control does NOT share: {n_timing} of {len(pas)}")
        P(f"   arms whose control-M ALSO passes 4b (the pass is exposure, not the clause): "
          f"{int(pas.ctlM_pass_4b.sum())} of {len(pas)}")
        wf_pass = WF[WF.OOS_4b]
        P(f"\n   of the {len(WF)} rule-8 picks, {len(wf_pass)} pass 4b OOS; cross-referencing each")
        P("   against its own full-sample row and its gross-matched control:")
        for _, w in wf_pass.iterrows():
            row = nd[(nd.panel == w.panel) & (nd.family == w.family) &
                     (nd.gross == w.gross) & (nd.dial == w.dial)].iloc[0]
            P(f"      {w.panel} {w.family} g={w.gross:.2f} dial={w.dial}: full 4b "
              f"{'PASS' if row.pass_4b else 'fail'} ({row.fail_4b}), full "
              f"{row.CAGR:.2%}/{row.Sharpe:.3f}/{row.MaxDD:.2%}; ctlM 4b "
              f"{'PASS' if row.ctlM_pass_4b else 'fail'} ({row.ctlM_fail_4b})")
        both = nd[nd.pass_4b & nd.pass_4b_OOS & ~nd.ctlM_pass_4b]
        P(f"\n   ARMS CLEARING 4b ON BOTH WINDOWS *AND* BEATING THEIR OWN GROSS-MATCHED CONTROL: "
          f"{len(both)}")
        if len(both):
            for _, r in both.iterrows():
                isp = WF[(WF.panel == r.panel) & (WF.family == r.family) & (WF.gross == r.gross)]
                picked = (not isp.empty) and bool(isp.iloc[0].dial == r.dial)
                P(f"      {r.panel} {r.family} dial={r.dial} g={r.gross:.2f}  "
                  f"{r.CAGR:.2%}/{r.Sharpe:.3f}/{r.MaxDD:.2%}  OOS {r.OOS_CAGR:.2%}/"
                  f"{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.2%}  turn {r.turn_per_yr:.2f}x/yr  "
                  f"mean gross {r.mean_gross_arm:.3f}  "
                  f"{'*** IS THE RULE-8 IS PICK AT ITS (panel, family, gross) ***' if picked else 'not the rule-8 pick'}")
        P("\n   HONESTY NOTE, stated before any memo is written: these rows were read off a")
        P(f"   {len(C)}-cell grid.  Rule 8 selected only the DIAL; the panel, the family and the")
        P("   gross were read off the grid after the fact, which is exactly the failure mode")
        P("   idea 806 documented in this same sprint.  Nothing here is a KEEP; the most any of")
        P("   it can be is a PRE-REGISTRATION TARGET, and it is filed as one.")

    # ================================ verdict ===========================================
    H = [("H_TIE      the corpus carries >= 10 non-degenerate MaxDD ties", H_TIE),
         ("H_EP_GAP   the whole-episode predicate is NOT exact here", H_EP_GAP),
         ("H_DECLINE  the DECLINE-leg predicate is NECESSARY (P=1)", H_DECLINE),
         ("H_SUFF     the DECLINE-leg predicate is SUFFICIENT (P=1)", H_SUFF),
         ("H_COST     the switch-cost term adds nothing over the leg split", H_COST),
         ("H_RECOV    the RECOVERY leg alone is NOT the predicate", H_RECOV)]
    P(f"\n{'='*100}")
    P("PRE-REGISTERED HYPOTHESES")
    P(f"{'='*100}")
    for nm, v in H:
        P(f"   {nm:<60} {'PASS' if v else 'FAIL'}")
    P(f"\n   {sum(bool(v) for _, v in H)} of {len(H)} pre-registered hypotheses pass.")
    P(f"\nRUNTIME {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(C=C, WF=WF, need=need, suff=suff, H=H, ties=ties, nd=nd, miss=miss)


if __name__ == "__main__":
    main()
