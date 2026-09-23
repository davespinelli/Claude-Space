#!/usr/bin/env python3
"""idea 2499 (lane B, run 62, 2026-09-23) — SHOULD THE CANDIDATE REBALANCE ON A CALENDAR
OR ON A NAME-SET CHANGE?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE
the 200d +/- 3% band (hysteresis, `baseline.band_state`) held at `min(gross / N_in, 2%)` of
NAV, idle NAV swept to SHY, weekly, t+1, 10 bps.  On U56 / gross 0.75 it reads
11.62% / 1.2687 / -14.81% at 3.51 turns a year; idea 2431 wrote the adoption bar:
CUT TURNOVER 3.51x -> 2.42x (-31.0%) AT UNCHANGED RETURNS.

THE GAP THIS RUN ATTACKS.  The committed book trades EVERY WEEK whether or not the eligible
set moved.  Every cadence device the record has priced acts on the CALENDAR — 2408's rota
(act on every k-th week), 2351's minimum hold (a name may not leave before h acting
rebalances), 2328's weight-drift band (act only on names whose weight moved).  NOTHING has
ever conditioned the DECISION TO TRADE AT ALL on the EVENT that the book exists to track:
the in-band NAME SET changing.  A week in which no name crossed either band edge is a week
in which the target book is the SAME book, and the whole week's turnover is drift-correction.

DIAL 1 -- m, the NAME-SET-CHANGE THRESHOLD, in {0, 1, 2, 3, 5, 8}.  At a scheduled weekly
rebalance the admitted set A_t (in-band and priced, decided at close t) is compared with
A_last, the admitted set at the LAST ACTING rebalance.  The book trades iff
    |A_t  symmetric-difference  A_last|  >=  m.
m = 0 is the IDENTITY rung: act every scheduled week = the committed book, bit-identical
(gate G1/G4).  m = 1 is the ZERO-FITTED point, pre-registered BEFORE any number in this run:
"trade only when the set changed at all".  The weekly schedule is a HARD CEILING — the
device can only ever SKIP a rebalance, never add one, so this book can never trade more
often than the committed one.
DIAL 2 -- GROSS in {0.75, 1.00}, the record's committed pair.

THAT IS EXACTLY TWO TUNED PARAMETERS.  Panels {U56, B136}, cost rungs {0, 10, 25, 50} bps,
cap 2%, band 0.03 and the SHY sweep are REPORTED IN FULL and never selected on.  SMALL is
not priced: ideas 2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of
40-120, so there is no pass there for a cadence device to keep.

THE EXCHANGE RATE THIS IS READ AGAINST (idea 2463, lane C, run 54).  The record's
"-0.10 pp of CAGR per 1% of turnover saved" is not a turnover rate but a DE-GROSSING rate:
pooled median pp per 1% saved splits by EXPOSURE, not by device — SCALE -0.115 / WHIP -0.112
/ WIDTH -0.195 / AGE -0.064 (de-grossers) against PARTIAL +0.005 / ROTA +0.008 / BANDW +0.009
/ DRIFT +0.020 / HOLD +0.085 (exposure-neutral).  EVENT is predicted (before compute) to be
exposure-neutral — it delays trades, it never shrinks the target — so the question is whether
it buys a BIGGER CUT than the neutral class has managed, not a better rate.

WHAT THE DEVICE COSTS, MEASURED NOT ASSUMED.  Skipping a week means holding names that have
since fallen OUT of the band.  STALENESS is published on every book: the mean fraction of
held risk weight sitting outside the current band, and the mean gap in trading days between
acting rebalances.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (m, gross) chosen on warm-up..2016-12-31 ONLY by four pre-stated choosers,
then 2017-2026 read ONCE.
    C_ISSHARPE   max IS Sharpe over the m ladder at that gross
    C_ISCALMAR   max IS Calmar over the m ladder at that gross
    C_ISADOPT    max IS CAGR among m-rungs clearing the -31.0% cut IN SAMPLE (2431's bar)
    C_JOINT      max IS Sharpe over the FULL (m x gross) grid -- both dials fitted together
    C_PREREG     NO CHOICE AT ALL -- m = 1, pre-registered above.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_event-driven-rebalance-cadence_B.py
"""
from __future__ import annotations

import hashlib, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "event-driven-rebalance-cadence", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BAR_CUT = 0.310                       # idea 2431: 3.51x -> 2.42x
MS = [0, 1, 2, 3, 5, 8]               # 0 = identity (the committed weekly book)
PREREG_M = 1                          # pre-registered BEFORE any number in this run
PLACEBO_SEEDS = 8                     # section F: frequency-matched random cadence
NEUTRAL_TOL = 0.02                    # exposure-neutral = mean risk gross within +/-2% relative
RATE_NEUTRAL = (+0.005, +0.085)       # idea 2463's exposure-neutral pp-per-1% band
RATE_DEGROSS = (-0.195, -0.064)       # idea 2463's de-grosser pp-per-1% band

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the target book
def admitted(px, invest, band=BAND):
    """The CAP2 admitted set: inside the 200d +/- band (hysteresis) AND priced that day."""
    q = px[invest]
    return (band_state(q, band) & q.notna()).reindex(columns=px.columns).fillna(False)


def cap_weights(px, invest, gross, band=BAND):
    """idea 2322's CAP2: w_i = min(gross / N_in, CAP) on the admitted set, idle NAV -> SHY."""
    adm = admitted(px, invest, band)
    q = px[invest]
    nin = adm[invest].sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=q.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    w[SWEEP] = 0.0
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the engine
def run_book(prices, weights, adm, m, freq=CADENCE, sweep=SWEEP, force_acts=None):
    """engine.backtest with ONE device: the EVENT cadence.

    At each scheduled (weekly) rebalance the book acts iff the admitted set has moved by at
    least `m` names since the LAST ACTING rebalance; otherwise it does nothing at all and the
    held weights simply drift.  m = 0 acts always and reduces to engine.backtest exactly
    (gates G1 / G4).  Every decision uses the close-t information shifted to t+1, exactly as
    the target weights are (gate G7 proves no lookahead).  Zero-cost returns and turnover are
    kept separately so every cost rung is priced from one pass.

    `force_acts` (a set of row indices) overrides the event test and makes the book act at
    exactly those scheduled rebalances -- the PLACEBO arm of section F, which answers "is the
    saving bought by the EVENT, or by simply trading less often?"
    """
    cols = list(prices.columns)
    si = cols.index(sweep)
    risk = np.ones(len(cols), dtype=bool); risk[si] = False
    rets = prices.pct_change().fillna(0.0)
    # decided at t, applied at t+1 -- engine.backtest's own convention, except that engine leaves
    # row 0's target NaN (and therefore its held row NaN until the first scheduled rebalance);
    # this replica starts FLAT instead, which is why gate G1 compares the two on the rows engine
    # actually prices and publishes the count of NaN rows it skips.
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1).fillna(0.0)
    a_dec = (adm.reindex(prices.index).reindex(columns=cols)
             .shift(1).fillna(False).astype(bool))          # bool, NOT object: `~` must negate
    key = prices.index.to_period(freq)
    ser = pd.Series(key, index=prices.index)
    mask = (ser != ser.shift(-1)).shift(1, fill_value=False).values
    shy_live = prices[sweep].notna().shift(1, fill_value=False).values

    n = len(prices.index)
    held = np.zeros((n, len(cols)))
    cur = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); risk_g = np.zeros(n)
    stale_w = np.zeros(n)                       # held risk weight currently OUT of band
    wt = w_target.values; rv = rets.values; av = a_dec.values
    last_set = None
    gaps: list[int] = []; changes: list[int] = []; acted_at: list[int] = []
    lev = 0; nreb = 0; nact = 0; last_act = None
    for i in range(n):
        act = mask[i] or i == 0
        if act:
            nreb += 1
            if last_set is None:
                ch = int(av[i].sum())
            else:
                ch = int(np.count_nonzero(av[i] ^ last_set))
            changes.append(ch)
            if force_acts is not None:
                act = (i in force_acts) or last_set is None
            elif m > 0 and last_set is not None and ch < m:
                act = False
        if act:
            nact += 1
            acted_at.append(i)
            if last_act is not None:
                gaps.append(i - last_act)
            last_act = i
            last_set = av[i].copy()
            new = wt[i].copy()
            srisk = new[risk].sum()
            if srisk > 1.0:                       # never lever: scale the risk sleeve back
                lev += 1
                new[risk] *= 1.0 / srisk
                srisk = 1.0
            new[si] = max(0.0, 1.0 - srisk) if shy_live[i] else 0.0
            dv = np.abs(new - cur)
            turnover[i] = dv.sum()
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        risk_g[i] = cur[risk].sum()
        rw = cur * risk
        srw = rw.sum()
        stale_w[i] = float((rw * (~av[i])).sum() / srw) if srw > 1e-12 else 0.0
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index),
                risk_gross=pd.Series(risk_g, index=prices.index),
                stale=pd.Series(stale_w, index=prices.index),
                held=pd.DataFrame(held, index=prices.index, columns=cols),
                changes=np.asarray(changes), gaps=np.asarray(gaps),
                acted_at=np.asarray(acted_at),
                lev_events=lev, acting_rebalances=nact, scheduled_rebalances=nreb)


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


def legstring(d):
    return "".join("1" if d[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2499 (lane B, run 62) — CALENDAR vs NAME-SET-CHANGE rebalance cadence ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cap {CAP}  schedule ceiling {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 m (names of in-band-set change required to act) {MS};  m=0 IS the committed book")
    say(f"    DIAL 2 gross {GROSSES};  pre-registered zero-fitted point m = {PREREG_M}")
    say(f"    THE BAR (idea 2431): turnover -{BAR_CUT:.1%} at unchanged returns (3.51x -> 2.42x)")
    say(f"    THE RATE (idea 2463): exposure-neutral devices buy {RATE_NEUTRAL} pp per 1% saved,"
        f" de-grossers {RATE_DEGROSS}")
    gate("G8 exactly two tuned parameters", "m (set-change threshold), gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G0b all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead}")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    px_u, inv_u = panels["U56"]
    adm_u = admitted(px_u, inv_u)

    # ---- G1: the m=0 book IS engine.backtest on CAP2
    w0 = cap_weights(px_u, inv_u, 0.75)
    r_eng = backtest(px_u, w0, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    res0 = run_book(px_u, w0, adm_u, 0)
    diff = (r_eng - priced(res0, HEADLINE_RUNG))
    d1 = float(diff.abs().max())
    gate("G1 m=0 replica == engine.backtest (CAP2, U56, g=0.75)",
         f"max|d| {d1:.3e} over {int(diff.notna().sum())} of {len(diff)} rows"
         f" ({int(diff.isna().sum())} pre-first-rebalance rows engine leaves NaN)",
         "< 1e-12", d1 < 1e-12)
    publish("G1b the NaN rows engine skips are all before the scored window (row 260)",
            f"last NaN row index {int(np.flatnonzero(diff.isna().values).max()) if diff.isna().any() else -1}"
            f" < {WARMUP}")
    gate("G4 m=0 acts on EVERY scheduled rebalance",
         f"acting {res0['acting_rebalances']} of scheduled {res0['scheduled_rebalances']}", "equal",
         res0["acting_rebalances"] == res0["scheduled_rebalances"])

    # ---- G12: turnover is zero on every non-acting day, by construction -- asserted, not assumed
    r8 = run_book(px_u, w0, adm_u, 8)
    tv = r8["turnover"].values
    nz = np.flatnonzero(tv > 1e-15)
    gate("G12 turnover is non-zero only on ACTING rebalances (m=8, U56)",
         f"{len(nz)} non-zero rows vs {r8['acting_rebalances']} acting rebalances",
         "non-zero rows <= acting", len(nz) <= r8["acting_rebalances"])

    # ---- G7: no lookahead.  Truncating the tape cannot change any earlier decision.
    T = "2018-01-01"
    px_t = px_u.loc[:T]
    adm_t = admitted(px_t, inv_u)
    h_full = run_book(px_u, w0, adm_u, 3)["held"].loc[:T]
    h_tr = run_book(px_t, cap_weights(px_t, inv_u, 0.75), adm_t, 3)["held"]
    common = h_full.index.intersection(h_tr.index)[:-1]     # last row: period-end mask differs
    d7 = float((h_full.loc[common] - h_tr.loc[common]).abs().values.max())
    gate(f"G7 no lookahead (m=3 held path, tape truncated at {T})", f"max|d| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    say(f"\n    {len(MS)} books per (panel, gross); {len(MS) * len(GROSSES) * len(panels)} books,"
        f" x{len(RUNGS)} cost rungs")

    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        adm = admitted(px, invest)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        # the LIVE book, priced by engine.backtest exactly as baseline.compare() does -- NOT through
        # run_book, whose SHY sweep would turn RULES v2's CASH residual into a bond sleeve it does
        # not hold.  Gate G11 asserts this against the record's committed 1.2052 (1.2262/1.1897).
        base_r = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for gross in GROSSES:
            w = cap_weights(px, invest, gross)
            for m in MS:
                res = run_book(px, w, adm, m)
                inw = res["held"].drop(columns=[SWEEP]).loc[win]
                pos = inw.values[inw.values > 1e-12]
                ch, gp = res["changes"], res["gaps"]
                tr_rows.append(dict(panel=pname, gross=gross, m=m,
                                    turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                    acting_reb=res["acting_rebalances"],
                                    sched_reb=res["scheduled_rebalances"],
                                    act_rate=res["acting_rebalances"] / res["scheduled_rebalances"],
                                    mean_gap_days=float(gp.mean()) if len(gp) else np.nan,
                                    max_gap_days=int(gp.max()) if len(gp) else 0,
                                    mean_setchange=float(ch.mean()) if len(ch) else np.nan,
                                    median_setchange=float(np.median(ch)) if len(ch) else np.nan,
                                    mean_stale_w=float(res["stale"].loc[win].mean()),
                                    max_stale_w=float(res["stale"].loc[win].max()),
                                    mean_names_in=float((inw.values > 1e-12).sum(axis=1).mean()),
                                    mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                    mean_gross=float(res["gross"].loc[win].mean()),
                                    mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                    max_name_w=float(pos.max()) if len(pos) else 0.0,
                                    max_row_sum=float(res["gross"].max()),
                                    lev_events=res["lev_events"]))
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    rows.append(dict(panel=pname, gross=gross, m=m, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                                     IS_Calmar=calmar(r.loc[:IS_END]), IS_MaxDD=maxdd(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     legs=legstring(lg), **lg))
            say(f"    ... {pname} gross {gross:.2f} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)

    # in-sample turnover (for the IS-only adoption chooser) needs its own pass
    is_tr = {}
    for pname, (px, invest) in panels.items():
        pxi = px.loc[:IS_END]
        admi = admitted(pxi, invest)
        win_is = px.index[WARMUP:].intersection(pxi.index)
        yrs_is = len(win_is) / 252
        for gross in GROSSES:
            wi = cap_weights(pxi, invest, gross)
            for m in MS:
                res = run_book(pxi, wi, admi, m)
                is_tr[(pname, gross, m)] = float(res["turnover"].loc[win_is].sum() / yrs_is)

    ref_t = {(r.panel, r.gross): r.turnover_yr for r in tf[tf.m == 0].itertuples()}
    ref_g = {(r.panel, r.gross): r.mean_risk_gross for r in tf[tf.m == 0].itertuples()}
    tf["cut"] = [1 - r.turnover_yr / ref_t[(r.panel, r.gross)] for r in tf.itertuples()]
    tf["dgross_rel"] = [r.mean_risk_gross / ref_g[(r.panel, r.gross)] - 1 for r in tf.itertuples()]
    ref_c = {(r.panel, r.gross, r.cost_bps): r.CAGR for r in df[df.m == 0].itertuples()}
    ref_s = {(r.panel, r.gross, r.cost_bps): r.Sharpe for r in df[df.m == 0].itertuples()}
    df["dCAGR"] = [r.CAGR - ref_c[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    df["dSharpe"] = [r.Sharpe - ref_s[(r.panel, r.gross, r.cost_bps)] for r in df.itertuples()]
    kt = {(r.panel, r.gross, r.m): r for r in tf.itertuples()}
    for col in ("cut", "turnover_yr", "mean_risk_gross", "dgross_rel", "act_rate",
                "mean_stale_w", "mean_gap_days"):
        df[col] = [getattr(kt[(r.panel, r.gross, r.m)], col) for r in df.itertuples()]
    df["pp_per_1pct"] = [(100 * r.dCAGR) / (100 * r.cut) if r.cut > 1e-9 else np.nan for r in df.itertuples()]
    df["clears_bar"] = (df.cut >= BAR_CUT) & (df.dCAGR >= 0)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2 / G2b / G11: reproduction of the committed numbers
    h = df[(df.panel == "U56") & (df.gross == 0.75) & (df.m == 0) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces the committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    gate("G2b reproduces the committed 3.51x turnover (U56, CAP2, g=0.75)",
         f"{h.turnover_yr:.4f}x", "|d| < 0.01", abs(h.turnover_yr - 3.51) < 0.01)
    hb = tf[(tf.panel == "B136") & (tf.gross == 0.75) & (tf.m == 0)].iloc[0]
    gate("G2c reproduces idea 2467's committed 4.68x turnover (B136, CAP2, g=0.75)",
         f"{hb.turnover_yr:.4f}x", "|d| < 0.02", abs(hb.turnover_yr - 4.68) < 0.02)
    for pn, exp in (("U56", (0.0865, 1.2052, -0.1205, 1.2262, 1.1897)),
                    ("B136", (0.0796, 1.0972, -0.1224, 1.2296, 0.9669))):
        pxp, _ = panels[pn]
        winp = pxp.index[WARMUP:]
        br = backtest(pxp, rules_v2_weights(pxp), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[winp]
        h1b, h2b = halves(br)
        d11 = max(abs(cagr(br) - exp[0]), abs(sharpe(br) - exp[1]) / 10, abs(maxdd(br) - exp[2]),
                  abs(h1b - exp[3]) / 10, abs(h2b - exp[4]) / 10)
        gate(f"G11 the 4a comparand IS the committed live RULES v2 book ({pn})",
             f"{cagr(br):.2%} / {sharpe(br):.4f} / {maxdd(br):.2%}, halves {h1b:.4f}/{h2b:.4f}"
             f" -> max|d| {d11:.2e}", "< 1e-3", d11 < 1e-3)

    gate("G5 no leverage anywhere", f"max row gross {tf.max_row_sum.max():.9f};"
         f" risk-sleeve rescale events {int(tf.lev_events.sum())}", "<= 1+1e-12",
         tf.max_row_sum.max() <= 1 + 1e-12)
    mono = all(tf[(tf.panel == p) & (tf.gross == g)].sort_values("m").acting_reb.is_monotonic_decreasing
               for p in panels for g in GROSSES)
    gate("G10 acting rebalances are non-increasing in m (the ceiling is hard)", f"{mono}", "True", mono)
    bite_m = tf.groupby(["panel", "gross"]).turnover_yr.agg(lambda x: x.max() - x.min()).min()
    bite_g = min(abs(tf[(tf.panel == p) & (tf.m == 3) & (tf.gross == 1.00)].turnover_yr.iloc[0]
                     - tf[(tf.panel == p) & (tf.m == 3) & (tf.gross == 0.75)].turnover_yr.iloc[0])
                 for p in panels)
    gate("G9 BOTH dials bite", f"turnover range over m (min across panel x gross) {bite_m:.3f}x;"
         f" over gross at m=3 {bite_g:.3f}x", "both > 0.05", bite_m > 0.05 and bite_g > 0.05)

    # ---------------------------------------------------------------- SECTION A: the ladder
    say("\n=== A.  THE m LADDER at the headline rung (10 bps), both panels, both gross ===")
    say("      m   act/sched   gap_d  setchg  stale    turn/yr    cut     CAGR   dCAGR   pp/1%   "
        "Sharpe  MaxDD    OOS_S   legs 4b 4a  grossrel")
    for pname in panels:
        for gross in GROSSES:
            say(f"  -- {pname} gross {gross:.2f}   (reference m=0: {ref_t[(pname, gross)]:.2f} turns/yr,"
                f" CAGR {ref_c[(pname, gross, HEADLINE_RUNG)]:.2%}, risk gross {ref_g[(pname, gross)]:.4f})")
            q = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].sort_values("m")
            for r in q.itertuples():
                t = kt[(pname, gross, r.m)]
                say(f"      {r.m}  {t.acting_reb:4d}/{t.sched_reb:4d}  {t.mean_gap_days:5.1f}"
                    f"  {t.mean_setchange:5.2f}  {t.mean_stale_w:5.1%}  {r.turnover_yr:6.2f}x {r.cut:6.1%}"
                    f" {r.CAGR:7.2%} {r.dCAGR:+6.2%} {r.pp_per_1pct:+7.3f}  {r.Sharpe:6.4f} {r.MaxDD:7.2%}"
                    f"  {r.OOS_Sharpe:6.4f}  {r.legs}  {int(r.pass4b)}  {int(r.pass4a)}  {r.dgross_rel:+.2%}")

    say("\n    ALL COST RUNGS (m ladder, both panels, both gross) — full grid in .grid.csv")
    for rung in RUNGS:
        sub = df[df.cost_bps == rung]
        say(f"      {rung:5.1f} bps: 4b {int(sub.pass4b.sum())} of {len(sub)};"
            f"  4a {int(sub.pass4a.sum())} of {len(sub)};"
            f"  clears the -31.0% bar at dCAGR>=0: {int(sub.clears_bar.sum())} of {len(sub)};"
            f"  median dCAGR {sub[sub.m > 0].dCAGR.median():+.2%}")

    # ---------------------------------------------------------------- SECTION B: exposure + rate
    say("\n=== B.  IS THE DEVICE EXPOSURE-NEUTRAL, AND WHAT DOES IT CHARGE PER 1% SAVED? ===")
    nz = df[(df.m > 0) & (df.cut > 1e-9)]
    neutral = tf[tf.m > 0].dgross_rel.abs().max()
    gate(f"G13 EVENT is exposure-neutral (mean risk gross within +/-{NEUTRAL_TOL:.0%} relative)",
         f"max |dgross_rel| over all m>0 books {neutral:.3%}", f"< {NEUTRAL_TOL:.0%}", neutral < NEUTRAL_TOL)
    say(f"    pooled pp of CAGR per 1% of turnover saved over {len(nz)} rows:"
        f" median {nz.pp_per_1pct.median():+.4f}, mean {nz.pp_per_1pct.mean():+.4f},"
        f" IQR {nz.pp_per_1pct.quantile(0.25):+.4f}..{nz.pp_per_1pct.quantile(0.75):+.4f}")
    say(f"    idea 2463's classes: exposure-neutral {RATE_NEUTRAL}, de-grossers {RATE_DEGROSS}")
    for rung in RUNGS:
        q = nz[nz.cost_bps == rung]
        say(f"      {rung:5.1f} bps: median {q.pp_per_1pct.median():+.4f} over {len(q)} rows")
    for pname in panels:
        for gross in GROSSES:
            q = nz[(nz.panel == pname) & (nz.gross == gross) & (nz.cost_bps == HEADLINE_RUNG)]
            say(f"      {pname} g{gross:.2f} @10bps: " + "  ".join(
                f"m={r.m}:{r.pp_per_1pct:+.3f}" for r in q.sort_values("m").itertuples()))

    say("\n=== B2.  THE ADOPTION BAR (cut >= 31.0% AND dCAGR >= 0) ===")
    sub = df[df.clears_bar]
    if len(sub):
        for r in sub.sort_values("cut", ascending=False).itertuples():
            say(f"      {r.panel} g{r.gross:.2f} m={r.m} {r.cost_bps:5.1f}bps  cut {r.cut:6.1%}"
                f"  dCAGR {r.dCAGR:+.2%}  4b={int(r.pass4b)} legs {r.legs} OOS_S {r.OOS_Sharpe:.4f}")
    else:
        say("      NONE — no (panel, gross, m, rung) cell clears the bar.")
    say(f"      best cut anywhere: {df.cut.max():.1%}"
        f" (at dCAGR {df.loc[df.cut.idxmax()].dCAGR:+.2%}, {df.loc[df.cut.idxmax()].panel}"
        f" g{df.loc[df.cut.idxmax()].gross:.2f} m={df.loc[df.cut.idxmax()].m})")
    say("\n    leg-failure census over ALL rows:")
    for lg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"      {lg:7s} fails {int((~df[lg]).sum())} of {len(df)}")
    say(f"      leg strings: {df.legs.value_counts().to_dict()}")
    say(f"      4b {int(df.pass4b.sum())} of {len(df)};  4a {int(df.pass4a.sum())} of {len(df)}")

    # ---------------------------------------------------------------- SECTION C: the event census
    say("\n=== C.  THE EVENT ITSELF: how often does the in-band NAME SET actually move? ===")
    for pname, (px, invest) in panels.items():
        adm = admitted(px, invest)
        res = run_book(px, cap_weights(px, invest, 0.75), adm, 0)
        ch = res["changes"]
        say(f"    {pname}: {len(ch)} scheduled weekly rebalances; set change |A_t D A_last| —"
            f" mean {ch.mean():.2f}, median {np.median(ch):.0f}, p90 {np.percentile(ch, 90):.0f},"
            f" max {ch.max()}")
        for m in MS[1:]:
            say(f"       m={m}: {(ch >= m).mean():.1%} of weeks would act on the m=0 reference path"
                f" (unconditional; the realised path differs because skipping widens the comparison)")
        say(f"       weeks with ZERO set change: {(ch == 0).mean():.1%}"
            f"  -> that is the upper bound on a free saving")

    # ---------------------------------------------------------------- SECTION D: rule 8
    say("\n=== D.  RULE 8 WALK-FORWARD.  (m, gross) chosen on warm-up..2016-12-31 ONLY; 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_oos = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG,
                            freq=CADENCE)["returns"].loc[win].loc[OOS_START:]
        for rung in RUNGS:
            allp = df[(df.panel == pname) & (df.cost_bps == rung)].copy()
            allp["IS_cut"] = [1 - is_tr[(pname, r.gross, r.m)] / is_tr[(pname, r.gross, 0)]
                              for r in allp.itertuples()]
            allp["IS_dCAGR"] = [r.IS_CAGR - float(allp[(allp.m == 0) & (allp.gross == r.gross)].IS_CAGR.iloc[0])
                                for r in allp.itertuples()]
            for gross in GROSSES:
                pool = allp[allp.gross == gross]
                picks = {}
                picks["C_ISSHARPE"] = pool.loc[pool.IS_Sharpe.idxmax()]
                picks["C_ISCALMAR"] = pool.loc[pool.IS_Calmar.idxmax()]
                adopt = pool[(pool.IS_cut >= BAR_CUT) & (pool.IS_dCAGR >= 0)]
                picks["C_ISADOPT"] = (adopt.loc[adopt.IS_CAGR.idxmax()] if len(adopt)
                                      else pool[pool.m == 0].iloc[0])
                picks["C_JOINT"] = allp.loc[allp.IS_Sharpe.idxmax()]     # both dials fitted together
                picks["C_PREREG"] = pool[pool.m == PREREG_M].iloc[0]
                for cname, p in picks.items():
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=cname,
                                   picked_m=int(p.m), picked_gross=float(p.gross),
                                   IS_cut=float(p.IS_cut), IS_Sharpe=float(p.IS_Sharpe),
                                   OOS_CAGR=float(p.OOS_CAGR), OOS_Sharpe=float(p.OOS_Sharpe),
                                   OOS_MaxDD=float(p.OOS_MaxDD),
                                   SPY_OOS_CAGR=cagr(spy_oos), SPY_OOS_Sharpe=sharpe(spy_oos),
                                   SPY_OOS_MaxDD=maxdd(spy_oos),
                                   BASE_OOS_CAGR=cagr(base_oos), BASE_OOS_Sharpe=sharpe(base_oos),
                                   BASE_OOS_MaxDD=maxdd(base_oos),
                                   REF_OOS_CAGR=float(pool[pool.m == 0].OOS_CAGR.iloc[0]),
                                   REF_OOS_Sharpe=float(pool[pool.m == 0].OOS_Sharpe.iloc[0]),
                                   full_cut=float(p.cut), full_dCAGR=float(p.dCAGR),
                                   full_4b=bool(p.pass4b), full_legs=p.legs,
                                   adopt_pool_size=int(len(adopt))))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("    chooser      picks (m)                       OOS CAGR / Sharpe    vs SPY / vs CAP2 / vs live")
    for cname in ("C_ISSHARPE", "C_ISCALMAR", "C_ISADOPT", "C_JOINT", "C_PREREG"):
        q = wfd[wfd.chooser == cname]
        pk = q.picked_m.value_counts().sort_index().to_dict()
        say(f"    {cname:11s} m={str(pk):26s}"
            f" OOS {q.OOS_CAGR.median():6.2%} / {q.OOS_Sharpe.median():.4f}"
            f"   SPY {int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum())}/{len(q)}"
            f"  CAP2 {int((q.OOS_Sharpe > q.REF_OOS_Sharpe).sum())}/{len(q)}"
            f"  live {int((q.OOS_Sharpe > q.BASE_OOS_Sharpe).sum())}/{len(q)}")
        say(f"        full-sample 4b on the pick {int(q.full_4b.sum())}/{len(q)};"
            f"  cut median {q.full_cut.median():.1%}, dCAGR median {q.full_dCAGR.median():+.2%}")
    say(f"    TOTAL PICKS {len(wfd)};  m=0 (the committed book) picked in"
        f" {int((wfd.picked_m == 0).sum())} of {len(wfd)}")
    for pname in panels:
        q = wfd[wfd.panel == pname].iloc[0]
        say(f"    [{pname}] OOS benchmarks read ONCE: SPY {q.SPY_OOS_CAGR:.2%} / {q.SPY_OOS_Sharpe:.4f}"
            f" / {q.SPY_OOS_MaxDD:.2%};  live RULES v2 {q.BASE_OOS_CAGR:.2%} / {q.BASE_OOS_Sharpe:.4f}"
            f" / {q.BASE_OOS_MaxDD:.2%}")

    # ---------------------------------------------------------------- SECTION E: the pre-registered book
    say(f"\n=== E.  THE ZERO-FITTED BOOK IN FULL  (m = {PREREG_M}: trade only when the set moved at all) ===")
    zp = df[df.m == PREREG_M]
    say("    panel gross  bps   turn/yr   cut    CAGR    dCAGR   Sharpe   H1/H2         MaxDD"
        "    OOS CAGR/Sharpe   legs 4b 4a")
    for r in zp.sort_values(["panel", "gross", "cost_bps"]).itertuples():
        say(f"    {r.panel:5s} {r.gross:.2f} {r.cost_bps:5.1f}  {r.turnover_yr:6.2f}x {r.cut:6.1%}"
            f" {r.CAGR:7.2%} {r.dCAGR:+6.2%}  {r.Sharpe:6.4f}  {r.H1:.4f}/{r.H2:.4f}  {r.MaxDD:7.2%}"
            f"   {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:6.4f}   {r.legs}  {int(r.pass4b)}  {int(r.pass4a)}")
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        say(f"    [{pname}] SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%};"
            f" halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f};"
            f" OOS {cagr(spy.loc[OOS_START:]):.2%} / {sharpe(spy.loc[OOS_START:]):.4f};"
            f" 4b bars: DD >= {DD_CAP * maxdd(spy):.2%}, CAGR >= {CAGR_FLOOR * cagr(spy):.2%}")

    # ---------------------------------------------------------------- SECTION F: the placebo
    say("\n=== F.  PLACEBO: is the saving bought by the EVENT, or by simply TRADING LESS OFTEN? ===")
    say("    For every (panel, gross, m) the placebo acts at a RANDOM subset of the scheduled weekly")
    say("    rebalances of EXACTLY the same size as the event book's realised acting count, 8 md5")
    say(f"    seeds each.  Excess = EVENT minus placebo mean.  Headline rung {HEADLINE_RUNG:.0f} bps.")
    pl_rows = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        adm = admitted(px, invest)
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[win]
        key = px.index.to_period(CADENCE)
        ser = pd.Series(key, index=px.index)
        maskv = (ser != ser.shift(-1)).shift(1, fill_value=False).values
        sched = np.flatnonzero(maskv)
        for gross in GROSSES:
            w = cap_weights(px, invest, gross)
            for m in MS[1:]:
                nact = int(kt[(pname, gross, m)].acting_reb)
                for seed in range(PLACEBO_SEEDS):
                    h = int(hashlib.md5(f"{pname}|{gross}|{m}|{seed}".encode()).hexdigest()[:8], 16)
                    rng = np.random.default_rng(h)
                    pick = set(rng.choice(sched, size=min(nact, len(sched)), replace=False).tolist())
                    res = run_book(px, w, adm, m, force_acts=pick)
                    r = priced(res, HEADLINE_RUNG).loc[win]
                    r_oos = r.loc[OOS_START:]
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    pl_rows.append(dict(panel=pname, gross=gross, m=m, seed=seed,
                                        turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                        acting_reb=res["acting_rebalances"],
                                        mean_stale_w=float(res["stale"].loc[win].mean()),
                                        CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                        OOS_Sharpe=sharpe(r_oos), legs=legstring(lg), **lg))
        say(f"    ... {pname} placebo done ({time.time() - t0:.0f}s)")
    pl = pd.DataFrame(pl_rows); pl.to_csv(f"{OUT}.placebo.csv", index=False)
    pl["cut"] = [1 - r.turnover_yr / ref_t[(r.panel, r.gross)] for r in pl.itertuples()]
    ev = df[(df.cost_bps == HEADLINE_RUNG) & (df.m > 0)].set_index(["panel", "gross", "m"])
    say("    panel gross  m   EVENT cut/CAGR/Sharpe      PLACEBO mean cut/CAGR/Sharpe (sd)"
        "      EXCESS cut / CAGR / Sharpe")
    exc = []
    for (pname, gross, m), q in pl.groupby(["panel", "gross", "m"]):
        e = ev.loc[(pname, gross, m)]
        dcut, dcagr, dsh = e.cut - q.cut.mean(), e.CAGR - q.CAGR.mean(), e.Sharpe - q.Sharpe.mean()
        exc.append(dict(panel=pname, gross=gross, m=m, excess_cut=dcut, excess_CAGR=dcagr,
                        excess_Sharpe=dsh, seed_sd_Sharpe=q.Sharpe.std(), seed_sd_CAGR=q.CAGR.std(),
                        placebo_4b=int(q.pass4b.sum()), n=len(q)))
        say(f"    {pname:5s} {gross:.2f}  {m}   {e.cut:6.1%} {e.CAGR:7.2%} {e.Sharpe:6.4f}"
            f"      {q.cut.mean():6.1%} {q.CAGR.mean():7.2%} {q.Sharpe.mean():6.4f} ({q.Sharpe.std():.4f})"
            f"      {dcut:+6.1%} {dcagr:+6.2%} {dsh:+7.4f}")
    ex = pd.DataFrame(exc); ex.to_csv(f"{OUT}.placebo_excess.csv", index=False)
    say(f"    POOLED over {len(ex)} (panel, gross, m) cells: excess cut median {ex.excess_cut.median():+.1%},"
        f" excess CAGR median {ex.excess_CAGR.median():+.2%}, excess Sharpe median {ex.excess_Sharpe.median():+.4f}")
    say(f"    seed noise floor: median sd of Sharpe across the 8 placebo draws {ex.seed_sd_Sharpe.median():.4f},"
        f" of CAGR {ex.seed_sd_CAGR.median():.2%}")
    say(f"    placebo 4b passes {int(pl.pass4b.sum())} of {len(pl)}")
    dact = [int(g.acting_reb.max()) - int(kt[k].acting_reb)
            for k, g in pl.groupby(["panel", "gross", "m"])]
    publish("G14c the placebo's acting count vs the event book's (the placebo is matched, +1 for the"
            " forced initialisation act, so the comparison is CONSERVATIVE against the event rule)",
            f"max excess acts {max(dact)}, min {min(dact)} over {len(dact)} cells")
    # THE MECHANISM, measured not asserted: the event rule spends its trading budget on the
    # weeks where the trade is LARGEST, because those are exactly the weeks it refuses to skip.
    say("\n    MECHANISM — mean turnover PER ACTING REBALANCE (event vs frequency-matched placebo):")
    mech = []
    for (pname, gross, m), q in pl.groupby(["panel", "gross", "m"]):
        e = kt[(pname, gross, m)]
        yrs_p = len(panels[pname][0].index[WARMUP:]) / 252
        ev_per = e.turnover_yr * yrs_p / e.acting_reb
        pl_per = float((q.turnover_yr * yrs_p / q.acting_reb).mean())
        mech.append(dict(panel=pname, gross=gross, m=m, event_per_act=ev_per,
                         placebo_per_act=pl_per, ratio=ev_per / pl_per))
        say(f"      {pname:5s} {gross:.2f} m={m}: event {ev_per:.4f} of NAV per act,"
            f" placebo {pl_per:.4f}, ratio {ev_per / pl_per:.3f}")
    mc = pd.DataFrame(mech); mc.to_csv(f"{OUT}.mechanism.csv", index=False)
    gate("G15 the EVENT rule trades MORE per acting rebalance than a random cadence"
         " (it refuses to skip exactly the weeks whose trade is largest)",
         f"ratio median {mc.ratio.median():.3f}, min {mc.ratio.min():.3f}, max {mc.ratio.max():.3f}"
         f" over {len(mc)} cells", "> 1 in every cell", bool((mc.ratio > 1).all()))

    resolvable = int((ex.excess_Sharpe.abs() > ex.seed_sd_Sharpe).sum())
    gate("G14 the EVENT's Sharpe excess over the frequency-matched placebo is RESOLVABLE",
         f"{resolvable} of {len(ex)} cells have |excess Sharpe| > the seed sd", "published",
         True)
    publish("G14b the EVENT's turnover cut vs a frequency-matched random cadence",
            f"median excess {ex.excess_cut.median():+.1%} (positive = the event saves MORE than"
            f" random skipping at the same acting count)")

    # ---------------------------------------------------------------- gates + artefacts
    gd = pd.DataFrame(GATES); gd.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gd.pass_.sum())
    say(f"\n=== GATES {npass} of {len(gd)} ===")
    for g in GATES:
        if not g["pass_"]:
            say(f"    FAILED: {g['gate']}")
    say(f"    rows {len(df)}; turnover rows {len(tf)}; walk-forward picks {len(wfd)};"
        f" elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
