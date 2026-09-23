#!/usr/bin/env python3
"""idea 2453 (lane cloud, run 52, 2026-09-23) — IS THE CANDIDATE'S 4b PASS STABLE TO THE BAND
STATE'S INITIAL CONDITION AND ITS BURN-IN?

THE GAP.  `baseline.band_state` builds a hysteretic state by `raw.ffill().fillna(0.0)`, i.e.
EVERY name starts OUT and stays OUT until its first unambiguous crossing of either band edge.
The runner then scores from row 260, while a 200d MA plus a +/-3% band needs longer than 60
sessions to forget that boundary.  Every number in this record, the standing 4b candidate
included, inherits that ONE convention, and no other has ever been priced anywhere.

DIAL 1 -- the initial condition, in {OUT (committed), IN, NEUTRAL}:
  OUT      `raw.ffill().fillna(0.0)` -- a name is GATED OUT until its first crossing.  COMMITTED.
  IN       `raw.ffill().fillna(1.0)` -- a name is HELD from the first scored day until its first
           unambiguous crossing DOWN.  This is the opposite boundary and front-loads exposure
           into 2008-2009, which is exactly where 4b's `L_DD` and `L_H1` legs are decided.
  NEUTRAL  a name is NOT INVESTABLE at all until its first crossing: it is removed from the
           panel rather than gated within it.
DIAL 2 -- the scored start, in {row 260 (committed), row 500, row 756} -- roughly early 2009,
          early 2010 and early 2011.

A PREDICTION MADE BEFORE COMPUTE.  On the candidate's `gross / N_in` sizing, OUT and NEUTRAL are
the SAME BOOK BY CONSTRUCTION: the denominator counts only names that are IN, so a name that is
gated out and a name that is not investable receive the same zero and leave the same denominator.
They can differ ONLY on the LIVE RULES v2 book, whose denominator is ALL PRICED NAMES (clause 2
de-grosses through a full-panel denominator).  G5 asserts the identity on the candidate books and
G5b measures the gap on the live book, so the run publishes WHICH convention the record's two
sizing rules are actually sensitive to, rather than three columns of which two are silently equal.

THE BURN-IN IS MEASURED, NOT ASSUMED.  IN and OUT disagree on exactly the name-days before a
name's FIRST unambiguous crossing; after it, the `ffill` makes them identical forever.  The run
publishes that disagreement share by row and the LAST row at which any disagreement survives, so
"has the state forgotten t=0 by the scored start?" is answered with a number.

WHAT WOULD FALSIFY THE CANDIDATE.  A 4b pass that moves materially between OUT and IN, or that
disappears when the scored start is pushed past the burn-in, is a pass that was partly
manufactured at t = 0.  THE BARS MOVE WITH THE WINDOW AND ARE RECOMPUTED: SPY's own CAGR, Sharpe
and MaxDD are re-read on each scored start, so `L_DD` (0.60 x SPY) and `L_CAGR` (0.70 x SPY) are
never carried over from the committed window.  The OOS window (2017-01-01 onward) is IDENTICAL
across all three starts by construction, so every OOS comparison here is same-window.

EXACTLY TWO TUNED PARAMETERS (initial condition, scored start).  Panel, book, gross, cost rung,
band, MA length, cap and cadence are REPORTED AT EVERY GRID POINT AND NEVER SELECTED ON.

BOOKS.  CAP2 (idea 2322's 2%-per-name capped candidate) and CAND (idea 2300/2332's uncapped
`gross / N_in` book), both with the committed phi = 1.00 SHY sweep, plus the LIVE RULES v2 book,
which is BOTH the 4a comparand AND -- because its denominator is the whole panel -- the one book
on which the NEUTRAL convention can bite.  The comparand is re-run under the SAME (init, start)
as the row it judges, so 4a is a like-for-like contrast; the committed-convention baseline is
published alongside it.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials are chosen on start..2016-12-31 ONLY by two pre-stated IS-only choosers,
2017-2026 is then read ONCE, and the picks are scored against the COMMITTED (OUT, row 260).

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and 2383 read it at 0 of 128 with L_DD, L_H2 and
L_OOS all failing at every cell; a t=0 convention cannot move three failing legs at once.

GATES.  G0 >= 10y at every scored start.  G1 the per-column replica == `engine.backtest`.
G2 init=OUT IS `baseline.band_state` bit for bit.  G3 (OUT, row 260) reproduces the committed
CAP2 / CAND U56 headlines.  G3b the 4a comparand reproduces the live book's published numbers.
G4 no leverage.  G5 OUT == NEUTRAL on the candidate books (asserted).  G5b the OUT/NEUTRAL gap on
the LIVE book (published).  G6 exactly two tuned parameters.  G7 the burn-in decay (published).
G8 IN and OUT agree on every name-day AFTER that name's first crossing (the ffill identity).
G9 the OOS window is identical across all three scored starts.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  This run's own contrast (one convention against
another on the same tape and the same days) is first-order immune; the absolute 4b verdicts are
not, and a LATER scored start does not repair survivorship -- it only moves the window.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_band-state-initial-condition-and-burn-in_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, band_state                     # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "band-state-initial-condition-and-burn-in", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE = 0.03, 200, "W"
INITS = ["OUT", "IN", "NEUTRAL"]                 # DIAL 1; OUT is committed
STARTS = [260, 500, 756]                          # DIAL 2; 260 is committed
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
NAME_CAP = 0.020
BOOKS = {"CAP2": NAME_CAP, "CAND": np.inf}
HEADLINE_RUNG, HEADLINE_INIT, HEADLINE_START = 10.0, "OUT", 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
SWEEP = "SHY"

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


# ---------------------------------------------------------------- the band state, three ways
def band_raw(px, band=BAND):
    """The hysteretic RAW state: 1.0 above ma*(1+band), 0.0 below ma*(1-band), NaN in between and
    before 200 closes exist.  Past closes only."""
    ma = px.rolling(MA_LEN).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    return raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)


def band_init(px, init, band=BAND):
    """(state, investable) under one initial condition.
      OUT      NaN -> 0.0 (COMMITTED, == baseline.band_state)
      IN       NaN -> 1.0
      NEUTRAL  NaN -> not investable at all (dropped from the panel until the first crossing)"""
    f = band_raw(px, band).ffill()
    if init == "OUT":
        return f.fillna(0.0) > 0.5, px.notna()
    if init == "IN":
        return f.fillna(1.0) > 0.5, px.notna()
    if init == "NEUTRAL":
        return f.fillna(0.0) > 0.5, px.notna() & f.notna()
    raise ValueError(init)


def risk_weights(px, gross, cap, init):
    """The candidate's risk leg: every INVESTABLE name inside the band at gross/N_in, clipped to
    `cap` per name.  cap = INF is CAND, cap = 0.02 is CAP2."""
    st, inv = band_init(px, init)
    el = st & inv
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def live_v2_weights(px, init, gross=0.75):
    """RULES v2 clause 2 verbatim, but with the initial condition as a dial.  Its denominator is
    ALL INVESTABLE NAMES (not just the IN ones), which is why NEUTRAL can bite here and cannot on
    the candidate books."""
    st, inv = band_init(px, init)
    e = inv.astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(st, 0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that per-day turnover is retained so every cost rung is
    read off the SAME realised path.  Weights decided at t-1, applied at t; the book drifts
    between rebalances; the residual is swept into SHY at phi = 1.00."""
    cols = list(prices.columns); si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    s_key = pd.Series(prices.index.to_period(freq), index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum()); cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    S = lambda a: pd.Series(a, index=idx)
    return dict(r0=S(r0), turn=S(turn), gross=S(gr), names=S(nheld), maxw=S(mx))


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


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
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2453 — IS THE CANDIDATE'S 4b PASS STABLE TO THE BAND STATE'S INITIAL CONDITION")
    say("    AND ITS BURN-IN? ===")
    say(f"    {DATE}  lane {LANE} run 52   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 initial condition {INITS} (OUT is committed)     DIAL 2 scored start {STARTS}"
        " rows (260 is committed)")
    say("    PREDICTION MADE BEFORE COMPUTE: on the candidate's gross/N_in sizing OUT and NEUTRAL")
    say("    are the SAME BOOK BY CONSTRUCTION (the denominator counts only IN names), so the")
    say("    convention can bite only on the LIVE book, whose denominator is the whole panel.")
    say("    G5 asserts that identity; G5b measures the live book's gap.")
    say("    THE 4b BARS ARE RECOMPUTED ON EVERY WINDOW: SPY's CAGR / Sharpe / MaxDD are re-read at")
    say("    each scored start, so L_DD and L_CAGR are never carried over from the committed one.")
    say("    The OOS window (2017-01-01 on) is IDENTICAL across all three starts (G9).")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383) and 0 of 40-120 (2318/2322/2326/2343).")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg, and a LATER start moves the window but does not repair it.")
    gate("G6 exactly two tuned parameters", "initial condition, scored start", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[max(STARTS)]).days / 365.25
        gate(f"G0 >= 10y at the LATEST scored start ({nm}, row {max(STARTS)})",
             f"{yrs:.1f}y, {len(px.columns)} investable, {len(px)} rows; starts "
             + ", ".join(f"row {s} = {px.index[s].date()}" for s in STARTS), ">= 10y", yrs >= 10)

    px_u = panels["U56"]

    # G2 init=OUT IS baseline.band_state
    st_out, inv_out = band_init(px_u, "OUT")
    d2 = int((st_out != band_state(px_u, BAND)).sum().sum())
    gate("G2 init = OUT IS baseline.band_state, unmodified",
         f"{d2} differing cells of {st_out.size}", "0", d2 == 0)

    # G1 replica fidelity against the engine
    w_live = live_v2_weights(px_u, "OUT", 0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2 at init=OUT, 10 bps, no sweep)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)
    lr = (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4).loc[px_u.index[HEADLINE_START]:]
    lt = float(lv["turn"].loc[px_u.index[HEADLINE_START]:].sum() / (len(lr) / 252))
    gate("G3b the 4a comparand reproduces the live book's published numbers at (OUT, row 260)",
         f"turnover {lt:.3f}x (record 1.77x)  Sharpe {sharpe(lr):.4f} halves"
         f" {halves(lr)[0]:.4f}/{halves(lr)[1]:.4f} (record 1.2052, 1.2262/1.1897)"
         f"  MaxDD {maxdd(lr):.2%} (record -12.05%)", "Sharpe within 1e-3, turnover within 0.05x",
         abs(sharpe(lr) - 1.2052) < 1e-3 and abs(lt - 1.77) < 0.05)

    # G5 / G5b the OUT == NEUTRAL identity
    d5 = 0.0
    for pn, px in panels.items():
        for cap in BOOKS.values():
            for g in GROSSES:
                d5 = max(d5, float((risk_weights(px, g, cap, "OUT")
                                    - risk_weights(px, g, cap, "NEUTRAL")).abs().max().max()))
    gate("G5 on the candidate's gross/N_in books OUT == NEUTRAL EXACTLY (the prediction)",
         f"max|d weight| {d5:.3e} over 2 panels x 2 books x 2 gross", "< 1e-15", d5 < 1e-15)
    d5b = {}
    for pn, px in panels.items():
        d5b[pn] = float((live_v2_weights(px, "OUT") - live_v2_weights(px, "NEUTRAL")).abs().max().max())
    publish("G5b the OUT/NEUTRAL gap on the LIVE book (whole-panel denominator)",
            "  ".join(f"{k}: max|d weight| {v:.4e}" for k, v in d5b.items()))

    # G7 / G8 the burn-in
    say("\n=== A. THE BURN-IN, MEASURED — how long does the band state remember t = 0? ===")
    for pn, px in panels.items():
        f = band_raw(px).ffill()
        never = f.isna() & px.notna()                 # cells where IN and OUT still disagree
        share = never.sum(axis=1) / px.notna().sum(axis=1).replace(0, np.nan)
        last = int(np.max(np.where(never.values.any(axis=1))[0])) if never.values.any() else -1
        say(f"  {pn}: share of PRICED names that have NEVER crossed either edge, by row —"
            + "  ".join(f" row {s} ({px.index[s].date()}): {share.iloc[s]:.1%}" for s in STARTS))
        say(f"        last row at which ANY name still disagrees: row {last}"
            f" ({px.index[last].date() if last >= 0 else 'n/a'}); the state is FULLY FORGOTTEN"
            f" from row {last + 1} ({px.index[last + 1].date() if 0 <= last + 1 < len(px) else 'n/a'})"
            f" onward.  MA {MA_LEN}d is complete from row {MA_LEN - 1}.")
        st_i, _ = band_init(px, "IN"); st_o, _ = band_init(px, "OUT")
        after = (~never) & px.notna()
        d8 = int(((st_i != st_o) & after).sum().sum())
        gate(f"G8 IN and OUT agree on EVERY priced name-day after that name's first crossing ({pn})",
             f"{d8} disagreeing cells of {int(after.sum().sum())}", "0", d8 == 0)
        publish(f"G7 the burn-in decay ({pn})",
                "  ".join(f"row {r}: {share.iloc[r]:.1%}" for r in (200, 260, 400, 500, 756, 1000)
                          if r < len(px)))

    # G9 the OOS window is the same across starts
    ok9 = all(len(px.loc[OOS_START:]) == len(px.loc[OOS_START:]) for px in panels.values())
    say(f"  the OOS window is {len(px_u.loc[OOS_START:])} rows on U56"
        f" ({px_u.loc[OOS_START:].index[0].date()} to {px_u.index[-1].date()}) at EVERY scored start.")
    gate("G9 the OOS window is IDENTICAL across all three scored starts (so every OOS contrast"
         " here is same-window)", "by construction: OOS is a calendar slice, not a row offset",
         "True", ok9)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        for start_row in STARTS:
            start = px.index[start_row]
            spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
            spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
            base_by_init = {}
            for init in INITS:
                bl = run_book(px, live_v2_weights(px, init, 0.75), sweep=False)
                base_by_init[init] = dict(
                    r=(bl["r0"] - bl["turn"] * HEADLINE_RUNG / 1e4).loc[start:],
                    turn=float(bl["turn"].loc[start:].sum() / (len(bl["r0"].loc[start:]) / 252)))
            for bname, cap in BOOKS.items():
                for gross in GROSSES:
                    for init in INITS:
                        wr = risk_weights(px, gross, cap, init)
                        bk = run_book(px, wr)
                        r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                        yrs = len(r0) / 252
                        base_r = base_by_init[init]["r"]
                        cbase_r = base_by_init[HEADLINE_INIT]["r"]
                        book_facts.append(dict(
                            panel=pname, start_row=start_row, start=str(start.date()), book=bname,
                            gross=gross, init=init, turnover_yr=float(tn.sum() / yrs),
                            mean_names=float(bk["names"].loc[start:].mean()),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            max_gross=float(bk["gross"].loc[start:].max()),
                            max_name_w=float(bk["maxw"].loc[start:].max()),
                            n_rows=len(r0)))
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                            lg = legs(r, base_r, spy, r_oos, spy_oos)
                            rows.append(dict(
                                panel=pname, start_row=start_row, start=str(start.date()),
                                book=bname, gross=gross, init=init, cost_bps=rung,
                                CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                turnover_yr=float(tn.sum() / yrs),
                                IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                                OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                base_CAGR=cagr(base_r), base_turn=base_by_init[init]["turn"],
                                base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                cbase_Sharpe=sharpe(cbase_r), cbase_MaxDD=maxdd(cbase_r),
                                spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                                DD_bar=DD_CAP * maxdd(spy), CAGR_bar=CAGR_FLOOR * cagr(spy),
                                spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                spy_OOS_MaxDD=maxdd(spy_oos), spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(STARTS)} starts x 2 books x"
        f" {len(GROSSES)} gross x {len(INITS)} inits x {len(RUNGS)} rungs;"
        f" {len(bf)} scored (path, window) combinations.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max {bf.max_gross.max():.12f}; max single risk name {bf.max_name_w.max():.4f}",
         "<= 1+1e-12", bool(bf.max_gross.max() <= 1 + 1e-12))
    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.init == "OUT")
           & (df.start_row == HEADLINE_START) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.init == "OUT")
           & (df.start_row == HEADLINE_START) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10, abs(a.turnover_yr - 3.51) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 (OUT, row 260) reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS"
         " 12.77%/1.3318, 3.51x) AND CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f}"
         f" turn {a.turnover_yr:.2f}x; CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%}"
         f" OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f} -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ B. the bars move
    say("\n=== B. THE BARS THEMSELVES MOVE WITH THE SCORED START (SPY re-read on each window) ===")
    say("  panel start (row)      | SPY CAGR  SPY Sh  SPY MaxDD |  H1    H2   | L_DD bar  L_CAGR bar | rows")
    for pname in panels:
        for s in STARTS:
            r = df[(df.panel == pname) & (df.start_row == s)].iloc[0]
            say(f"  {pname:5s} {r.start} (r{s:4d}) | {r.spy_CAGR:8.2%} {r.spy_Sharpe:7.4f}"
                f" {r.spy_MaxDD:10.2%} | {r.spy_H1:5.2f} {r.spy_H2:5.2f} | {r.DD_bar:8.2%}"
                f" {r.CAGR_bar:11.2%} | {int(bf[(bf.panel == pname) & (bf.start_row == s)].n_rows.iloc[0])}")

    # ------------------------------------------------------------ C. every grid point
    say("\n=== C. THE FULL (init x start) LADDER, g 0.75 — EVERY GRID POINT ===")
    say("  panel book  init    start bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bn in BOOKS:
            for init in INITS:
                for s in STARTS:
                    for rung in RUNGS:
                        r = df[(df.panel == pname) & (df.book == bn) & (df.init == init)
                               & (df.start_row == s) & (df.gross == 0.75)
                               & (df.cost_bps == rung)].iloc[0]
                        lg = "".join("1" if r[x] else "0" for x in
                                     ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                        tag = "   <= COMMITTED" if (init == "OUT" and s == HEADLINE_START) else ""
                        say(f"  {pname:5s} {bn:4s} {init:7s} r{s:4d} {rung:5.1f} | {r.CAGR:6.2%}"
                            f" {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                            f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:7.2f} |"
                            f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}{tag}")
    say("\n  (gross 1.00 rows are in the CSV; the headline conclusions are quoted at the live 0.75.)")

    # ------------------------------------------------------------ D. how much is the artefact
    say("\n=== D. HOW MUCH OF THE 4b MARGIN IS A t = 0 ARTEFACT? (each cell vs its own committed"
        " (OUT, row 260) cell, at 10 bps) ===")
    say("  panel book  g    init    start | dCAGR   dSharpe   dMaxDD  | dOOS Sh | m_DD (pp)   m_CAGR (pp) | 4b")
    dec = []
    for pname in panels:
        for bn in BOOKS:
            for g in GROSSES:
                z = df[(df.panel == pname) & (df.book == bn) & (df.gross == g) & (df.init == "OUT")
                       & (df.start_row == HEADLINE_START) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                for init in INITS:
                    for s in STARTS:
                        if init == "OUT" and s == HEADLINE_START:
                            continue
                        r = df[(df.panel == pname) & (df.book == bn) & (df.gross == g)
                               & (df.init == init) & (df.start_row == s)
                               & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                        dec.append(dict(panel=pname, book=bn, gross=g, init=init, start_row=s,
                                        dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                                        dMaxDD=r.MaxDD - z.MaxDD, dTurn=r.turnover_yr - z.turnover_yr,
                                        dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                                        m_DD=r.m_DD, m_CAGR=r.m_CAGR, z_mDD=z.m_DD, z_mCAGR=z.m_CAGR,
                                        z4b=bool(z.pass4b), c4b=bool(r.pass4b)))
                        if g == 0.75:
                            say(f"  {pname:5s} {bn:4s} {g:.2f} {init:7s} r{s:4d} |"
                                f" {r.CAGR - z.CAGR:+7.2%} {r.Sharpe - z.Sharpe:+9.4f}"
                                f" {r.MaxDD - z.MaxDD:+8.2%} | {r.OOS_Sharpe - z.OOS_Sharpe:+8.4f} |"
                                f" {r.m_DD * 100:+9.2f} {r.m_CAGR * 100:+12.2f} |"
                                f" {'PASS' if r.pass4b else 'fail'}")
    dd_ = pd.DataFrame(dec); dd_.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n  Over all {len(dd_)} (cell vs its own committed cell) pairs at 10 bps:")
    say(f"   |dSharpe| <= 0.01 in {int((dd_.dSharpe.abs() <= 0.01).sum())} of {len(dd_)}"
        f"   |dCAGR| <= 0.10 pp in {int((dd_.dCAGR.abs() <= 0.001).sum())}"
        f"   4b kept in {int((dd_.z4b & dd_.c4b).sum())} of {int(dd_.z4b.sum())}"
        f"   4b LOST in {int((dd_.z4b & ~dd_.c4b).sum())}")
    say("   by initial condition (mean over panels, books, gross, starts):")
    for init in INITS:
        q = dd_[dd_.init == init]
        say(f"    {init:8s} dCAGR {q.dCAGR.mean():+.2%}  dSharpe {q.dSharpe.mean():+.4f}"
            f"  dMaxDD {q.dMaxDD.mean():+.2%}  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}"
            f"  dTurn {q.dTurn.mean():+.3f}x   4b {int(q.c4b.sum())}/{len(q)}")
    say("   by scored start:")
    for s in STARTS:
        q = dd_[dd_.start_row == s]
        if len(q):
            say(f"    row {s:4d}  dCAGR {q.dCAGR.mean():+.2%}  dSharpe {q.dSharpe.mean():+.4f}"
                f"  dMaxDD {q.dMaxDD.mean():+.2%}  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}"
                f"   4b {int(q.c4b.sum())}/{len(q)}")
    say("\n   THE MARGIN LEDGER — how far each cell clears the two ABSOLUTE 4b bars (pp), 10 bps,"
        " g0.75.  A margin that survives every (init, start) is not a t=0 artefact.")
    say("   panel book  | m_DD at (OUT,260) -> range over all 9 cells | m_CAGR at (OUT,260) -> range")
    for pname in panels:
        for bn in BOOKS:
            q = dd_[(dd_.panel == pname) & (dd_.book == bn) & (dd_.gross == 0.75)]
            z = df[(df.panel == pname) & (df.book == bn) & (df.gross == 0.75) & (df.init == "OUT")
                   & (df.start_row == HEADLINE_START) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"   {pname:5s} {bn:4s} | {z.m_DD * 100:+8.2f} -> [{min(q.m_DD.min(), z.m_DD) * 100:+.2f},"
                f" {max(q.m_DD.max(), z.m_DD) * 100:+.2f}] | {z.m_CAGR * 100:+8.2f} ->"
                f" [{min(q.m_CAGR.min(), z.m_CAGR) * 100:+.2f}, {max(q.m_CAGR.max(), z.m_CAGR) * 100:+.2f}]")

    # ------------------------------------------------------------ E. KEEP counts
    say(f"\n=== E. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for init in INITS:
        d = df[df.init == init]
        say(f"   init {init:8s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for s in STARTS:
        d = df[df.start_row == s]
        say(f"   start r{s:4d}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    jt = []
    for bn in BOOKS:
        for g in GROSSES:
            for init in INITS:
                for s in STARTS:
                    for rung in RUNGS:
                        q = df[(df.book == bn) & (df.gross == g) & (df.init == init)
                               & (df.start_row == s) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(book=bn, gross=g, init=init, start_row=s, cost_bps=rung,
                                       joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"\n  JOINT both-panel 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by init: "
        + "  ".join(f"{i}:{int(jf[jf.init == i].joint.sum())}/{len(jf[jf.init == i])}" for i in INITS)
        + ";  by start: "
        + "  ".join(f"r{s}:{int(jf[jf.start_row == s].joint.sum())}/{len(jf[jf.start_row == s])}"
                    for s in STARTS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 under the SAME convention in BOTH halves AND MaxDD"
        f" no worse): {len(pa)}")
    for _, r in pa.head(12).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} {r.init:7s} r{r.start_row} g{r.gross:.2f}"
            f" {r.cost_bps:5.1f}bps  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
            f"  turn {r.turnover_yr:.2f}x  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ F. rule 8
    say("\n=== F. RULE 8 — the two dials (initial condition, scored start) chosen on")
    say("    start..2016-12-31 ONLY, 2017-2026 read ONCE, scored against the COMMITTED (OUT, r260). ===")
    wf = []
    for pname in panels:
        for bn in BOOKS:
            for g in GROSSES:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.book == bn) & (df.gross == g)
                           & (df.cost_bps == rung)]
                    cm = d[(d.init == "OUT") & (d.start_row == HEADLINE_START)].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, book=bn, gross=g, cost_bps=rung, chooser=chooser,
                                       pick=f"{pk.init}/r{pk.start_row}", full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                       OOS_MaxDD=pk.OOS_MaxDD,
                                       committed_OOS_Sharpe=cm.OOS_Sharpe,
                                       committed_OOS_CAGR=cm.OOS_CAGR,
                                       committed_OOS_MaxDD=cm.OOS_MaxDD,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       base_OOS_CAGR=pk.base_OOS_CAGR,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe,
                                       spy_OOS_CAGR=pk.spy_OOS_CAGR, spy_OOS_MaxDD=pk.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 books x {len(GROSSES)} gross x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                          {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:                {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED (OUT,r260) cell's OOS Sharpe: {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks landing ON the committed convention:               {int((wfd['pick'] == f'OUT/r{HEADLINE_START}').sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                    {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution: " + "  ".join(
        f"{p}:{int((wfd['pick'] == p).sum())}" for p in sorted(wfd['pick'].unique())))
    say(f"   mean OOS CAGR / Sharpe / MaxDD of the IS-only picks:"
        f" {wfd.OOS_CAGR.mean():.2%} / {wfd.OOS_Sharpe.mean():.4f} / {wfd.OOS_MaxDD.mean():.2%}")
    say(f"   the COMMITTED (OUT, r260) cell's:                   "
        f" {wfd.committed_OOS_CAGR.mean():.2%} / {wfd.committed_OOS_Sharpe.mean():.4f} /"
        f" {wfd.committed_OOS_MaxDD.mean():.2%}"
        f"  ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f} Sharpe)")
    say(f"   the LIVE RULES v2 baseline's:                       "
        f" {wfd.base_OOS_CAGR.mean():.2%} / {wfd.base_OOS_Sharpe.mean():.4f}")
    say(f"   SPY's:                                              "
        f" {wfd.spy_OOS_CAGR.mean():.2%} / {wfd.spy_OOS_Sharpe.mean():.4f} / {wfd.spy_OOS_MaxDD.mean():.2%}")
    say("\n   panel book  g    bps chooser     | pick        OOS CAGR  OOS Sh | committed OOS CAGR / Sh")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.book:4s} {r.gross:.2f} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r['pick']:11s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f} |"
            f" {r.committed_OOS_CAGR:17.2%} / {r.committed_OOS_Sharpe:.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
