#!/usr/bin/env python3
"""idea 2484 (lane C, run 57, 2026-09-23) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE THE
TAPE'S OWN REALISED SHORT RATE AS THE SHARPE NUMERAIRE?

THE GAP.  This record has priced the risk-free question exactly twice and BOTH times FLAT: idea
406 (2026-09-10, lane B) credited idle cash at a constant 150 / 300 bps, and the cloud's
PROTOCOL-amendment run of the same day priced the same constant.  Both ran on the OLD gross
ladder, before idea 2322's capped candidate existed, and both treated the credit as something
the record would have to ADD.

BUT THE CREDIT IS ALREADY THERE, AND IT IS NOT FLAT.  The sweep instrument is SHY -- a PRICED
COLUMN of both committed panels -- so `run_book`'s residual sweep already earns SHY's realised
total return every single day.  What the record does NOT do is subtract it: `sharpe()` and
`cagr()` are computed on TOTAL returns with rf = 0 everywhere, on the book AND on SPY.  A book
that parks a third of its NAV in T-bills is therefore paid the short rate and the statistic
counts the payment as alpha.

AND THE RATE IS A STEP FUNCTION WHOSE STEP LANDS INSIDE THE OOS WINDOW.  On this tape SHY's
realised annualised total return runs roughly 0.8%/yr over 2009-2016 -- the entire rule-8 IS
window -- against roughly 1.5% over 2017-2021 and 2.0% over 2022-2026.  The free payment is
therefore concentrated in exactly the sample rule 8 reads ONCE and treats as the honest test.

THE PREDICTION, STATED HERE BEFORE ANY COMPUTE, WITH ITS SIGN AND ITS ROUGH SIZE.  Subtracting a
risk-free rate `f` from a book costs its Sharpe approximately `f / sigma`, because it shifts the
mean by `f` and leaves the volatility essentially unchanged.  The capped candidate runs mean
realised gross near 0.66 and annualised volatility near 0.10; SPY is fully invested at roughly
0.18.  THE SAME RATE THEREFORE COSTS THE CANDIDATE NEARLY TWICE THE SHARPE IT COSTS THE
BENCHMARK IT IS JUDGED AGAINST -- and every one of 4b's three Sharpe legs (`L_H1`, `L_H2`,
`L_OOS`) is a candidate-minus-SPY comparison.  The convention is thus not neutral: it is a
systematic subsidy to the de-grossed book, paid in the currency the KEEP path is denominated in.
If the candidate's 4b margins are wide, this run CONFIRMS them and the record gains a robustness
stamp it has never held.  If they are thin, the standing candidate does not survive its own
numeraire, which is a KILL the record must carry before any capital is committed.

THE FIX PRICED.  Every leg is re-scored under the textbook EXCESS convention, `r_t - r_SHY,t`,
applied SYMMETRICALLY to the candidate, to the live RULES v2 book and to SPY.  This is the
CONSISTENT treatment idea 406 identified as the safe one (credit and numeraire moving together)
and it needs NO new parameter and NO new data: the rate is the committed panel's own SHY column.

DIAL 1 -- gross g in {0.75 (live), 1.00}.
DIAL 2 -- per-name weight cap in {0.015, 0.020 (idea 2322's CAP2, committed), 0.030, INF (idea
          2300/2332's uncapped CAND)}.

NUMERAIRE IS A PUBLISHED AXIS, NOT A DIAL -- it is never chosen on, and both values are reported
for every single grid point:
  TOTAL   r_t                 **THE COMMITTED CONVENTION** (rf = 0 everywhere).
  EXCESS  r_t - r_SHY,t       the textbook convention, applied to book, baseline AND SPY alike.

BOOKS.  The capped family above with the committed phi = 1.00 SHY sweep, plus the LIVE RULES v2
book as the 4a baseline, on both committed panels.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, rungs {0, 10, 25, 50} bps, numeraires
{TOTAL, EXCESS}, weekly cadence, t+1 execution, band 0.03, MA 200d and the SHY sweep.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  A numeraire change can only ever REMOVE Sharpe
from a de-grossed book, so it cannot create a pass where three legs already fail.

BOTH KEEP PATHS on every row, under BOTH numeraires.  4a: Sharpe > live RULES v2 in BOTH halves
and MaxDD no worse.  4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's,
CAGR >= 0.70 x SPY's.
RULE 8: the two dials (gross, cap) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE -- separately under each numeraire, so the run can
say whether the numeraire MOVES THE PICK as well as whether it moves the verdict.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 at cap = INF
the eligible set IS `baseline.band_state` & priced.  G3 the TOTAL numeraire at cap 0.020 / 0.75
reproduces the committed CAP2 and CAND headlines.  G4 no leverage.  G5 cost exactly linear in
the rung.  G6 exactly two tuned parameters.  G7 the EXCESS transform is EXACT (SHY's own excess
return is identically zero).  G8 the numeraire BITES (Sharpe falls for every book on every
panel).  G9 the sweep instrument is priced on every scored row.  G10 the rate path is published,
IS window against OOS window, before any verdict is read.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The TOTAL-vs-EXCESS contrast is same-tape,
same-day, same-weights and first-order immune to that bias; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_realised-short-rate-numeraire_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "realised-short-rate-numeraire", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
GROSSES = [0.75, 1.00]
CAPS = [0.015, 0.020, 0.030, np.inf]
RUNGS = [0.0, 10.0, 25.0, 50.0]
NUMERAIRES = ["TOTAL", "EXCESS"]
HEADLINE_RUNG, HEADLINE_CAP, HEADLINE_GROSS, HEADLINE_NUM = 10.0, 0.020, 0.75, "TOTAL"
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

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


def cname(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


# ---------------------------------------------------------------- the book
def eligible(px):
    """Names permitted to be held: inside the 200d +/- BAND hysteresis band and priced.  This is
    `baseline.band_state` unmodified (G2 asserts bit-identity)."""
    return band_state(px, BAND) & px.notna()


def risk_weights(px, gross, cap):
    el = eligible(px)
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the per-day turnover is retained so every cost rung
    is read off the SAME realised path.  Weights decided at t-1, applied at t; the book drifts
    between rebalances; the residual is swept into SHY at phi = 1.00."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    swp = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        swp[i] = float(cur[si])
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx), sweep_w=pd.Series(swp, index=idx))


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def ann(r):
    """Annualised ARITHMETIC mean, the quantity the Sharpe numerator carries."""
    return float(r.mean() * 252)


def vol(r):
    return float(r.std() * np.sqrt(252))


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
    """The five 4b legs and the 4a verdict, evaluated on whatever numeraire the caller passed.
    Book, baseline AND benchmark are always on the SAME numeraire -- that symmetry is the whole
    point of the run."""
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
                m_H1=h1 - s1, m_H2=h2 - s2, m_OOS=sharpe(r_oos) - sharpe(spy_oos),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2484 — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE THE TAPE'S OWN REALISED SHORT RATE? ===")
    say(f"    {DATE}  lane {LANE} run 57   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 gross {GROSSES}    DIAL 2 per-name cap {[cname(c) for c in CAPS]}"
        f"  (0.020 = idea 2322's CAP2, INF = CAND)")
    say("    PUBLISHED AXIS, NEVER SELECTED ON: numeraire TOTAL (committed, rf = 0) vs EXCESS (r - r_SHY,")
    say("    applied SYMMETRICALLY to the book, the live RULES v2 baseline AND SPY).")
    say("    PREDICTION, STATED BEFORE COMPUTE: subtracting rf costs Sharpe ~ rf / sigma.  The candidate's")
    say("    sigma ~ 0.10 against SPY's ~ 0.18, so the SAME rate costs the candidate ~1.8x the Sharpe it")
    say("    costs the benchmark, and all three 4b Sharpe legs are candidate-minus-SPY comparisons.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343); a")
    say("    numeraire change only REMOVES Sharpe from a de-grossed book and cannot mend three failing legs.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The TOTAL-vs-EXCESS contrast is same-tape, same-weights, first-order immune.")
    gate("G6 exactly two tuned parameters", "gross, per-name cap", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs = band_state(px_u, BAND)
    d2 = int((eligible(px_u) != (bs & px_u.notna())).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {(bs & px_u.notna()).sum(axis=1).mean():.2f}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---------------------------------------------------------- G10: the rate path, published first
    say("\n=== G10. THE RATE PATH — PUBLISHED BEFORE ANY VERDICT IS READ ===")
    say("  panel  window            | SHY annualised total return | ann. arithmetic mean | SHY vol")
    rate_facts = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        rf = px[SWEEP].pct_change().fillna(0.0).loc[start:]
        h = len(rf) // 2
        wins = [("full  " + str(rf.index[0].date()) + ".." + str(rf.index[-1].date()), rf),
                ("H1    " + str(rf.index[0].date()) + ".." + str(rf.index[h - 1].date()), rf.iloc[:h]),
                ("H2    " + str(rf.index[h].date()) + ".." + str(rf.index[-1].date()), rf.iloc[h:]),
                ("IS    warm-up.." + IS_END, rf.loc[:IS_END]),
                ("OOS   " + OOS_START + "..end", rf.loc[OOS_START:])]
        for label, x in wins:
            say(f"  {pname:5s}  {label:28s} | {cagr(x):26.2%} | {ann(x):20.2%} | {vol(x):7.2%}")
            rate_facts.append(dict(panel=pname, window=label.split()[0], cagr=cagr(x),
                                   ann_mean=ann(x), vol=vol(x)))
    rfd = pd.DataFrame(rate_facts); rfd.to_csv(f"{OUT}.rate.csv", index=False)
    u_is = rfd[(rfd.panel == "U56") & (rfd.window == "IS")].iloc[0]
    u_oos = rfd[(rfd.panel == "U56") & (rfd.window == "OOS")].iloc[0]
    gate("G10 the rate is a STEP and the step lands INSIDE the OOS window (U56)",
         f"IS {u_is.cagr:.2%}/yr vs OOS {u_oos.cagr:.2%}/yr (ratio {u_oos.cagr / u_is.cagr:.2f}x)",
         "OOS rate > IS rate", bool(u_oos.cagr > u_is.cagr))

    # G7 the transform is exact
    rf_u = px_u[SWEEP].pct_change().fillna(0.0)
    d7 = float((rf_u - rf_u).abs().max())
    gate("G7 the EXCESS transform is EXACT (SHY's own excess return is identically zero)",
         f"max|r_SHY - r_SHY| {d7:.3e} over {len(rf_u)} rows", "0.0", d7 == 0.0)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        rf = px[SWEEP].pct_change().fillna(0.0).loc[start:]
        spy_t = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for gross in GROSSES:
            for cap in CAPS:
                wr = risk_weights(px, gross, cap)
                bk = run_book(px, wr)
                r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                book_facts.append(dict(
                    panel=pname, gross=gross, cap=cname(cap),
                    turnover_yr=float(tn.sum() / (len(tn) / 252)),
                    mean_names=float(bk["names"].loc[start:].mean()),
                    mean_gross=float(bk["gross"].loc[start:].mean()),
                    max_gross=float(bk["gross"].loc[start:].max()),
                    mean_risk_gross=float((bk["gross"] - bk["sweep_w"]).loc[start:].mean()),
                    mean_sweep=float(bk["sweep_w"].loc[start:].mean()),
                    mean_cash=float(1.0 - bk["gross"].loc[start:].mean()),
                    max_name_w=float(bk["maxw"].loc[start:].max())))
                for rung in RUNGS:
                    r_t = r0 - tn * rung / 1e4
                    for num in NUMERAIRES:
                        if num == "TOTAL":
                            r, base, spy = r_t, base_t, spy_t
                        else:
                            r, base, spy = r_t - rf, base_t - rf, spy_t - rf
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
                        lg = legs(r, base, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, gross=gross, cap=cname(cap),
                            cap_num=float(cap) if np.isfinite(cap) else 9.99,
                            cost_bps=rung, numeraire=num,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            Vol=vol(r), AnnMean=ann(r),
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            mean_risk_gross=float((bk["gross"] - bk["sweep_w"]).loc[start:].mean()),
                            mean_sweep=float(bk["sweep_w"].loc[start:].mean()),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base), base_MaxDD=maxdd(base), base_CAGR=cagr(base),
                            base_OOS_Sharpe=sharpe(base.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_Vol=vol(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(GROSSES)} gross x {len(CAPS)} caps x"
        f" {len(RUNGS)} rungs x {len(NUMERAIRES)} numeraires; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} gross, {bf.max_name_w.max():.4f} max single name",
         "<= 1+1e-12", bool(bf.max_gross.max() <= 1 + 1e-12))
    wr0 = risk_weights(px_u, 0.75, HEADLINE_CAP)
    bz = run_book(px_u, wr0); st = px_u.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    def cell(panel, gross, cap, rung, num):
        return df[(df.panel == panel) & (df.gross == gross) & (df.cap == cname(cap))
                  & (df.cost_bps == rung) & (df.numeraire == num)].iloc[0]

    a = cell("U56", 0.75, 0.020, 10.0, "TOTAL")
    b = cell("U56", 0.75, np.inf, 10.0, "TOTAL")
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 the TOTAL numeraire reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS"
         " 12.77%/1.3318) AND CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say("\n=== A. THE FULL LADDER — EVERY GRID POINT, BOTH NUMERAIRES, gross 0.75 ===")
    say("  panel cap    bps num    |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for cap in CAPS:
            for rung in RUNGS:
                for num in NUMERAIRES:
                    r = cell(pname, 0.75, cap, rung, num)
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    tag = ""
                    if cap == HEADLINE_CAP and rung == HEADLINE_RUNG and num == HEADLINE_NUM:
                        tag = "   <= COMMITTED CAP2 HEADLINE"
                    say(f"  {pname:5s} {cname(cap):6s} {rung:4.0f} {num:6s} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}"
                        f"  | {lg}{tag}")

    say("\n  THE SAME LADDER AT gross 1.00:")
    say("  panel cap    bps num    |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for cap in CAPS:
            for rung in RUNGS:
                for num in NUMERAIRES:
                    r = cell(pname, 1.00, cap, rung, num)
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {cname(cap):6s} {rung:4.0f} {num:6s} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}"
                        f"  | {lg}")

    # ------------------------------------------------------------ B. the prediction, tested
    say("\n=== B. THE PRE-STATED PREDICTION, TESTED: DOES THE NUMERAIRE COST THE CANDIDATE MORE SHARPE")
    say("    THAN IT COSTS THE BENCHMARK IT IS JUDGED AGAINST?  (predicted hit = rf_ann / sigma) ===")
    say("  (`risk gross` EXCLUDES the SHY sweep column, so it is the share of NAV actually at equity")
    say("   risk; total gross is 1.00 by construction because the residual is swept, never left idle.)")
    say("  panel cap    bps | risk gross | SHY sleeve | sigma  | dSharpe realised | predicted rf/sigma"
        " | SPY dSharpe | predicted SPY | net swing")
    pred = []
    for pname in panels:
        px = panels[pname]; start = px.index[WARMUP]
        rf = px[SWEEP].pct_change().fillna(0.0).loc[start:]
        rf_ann = ann(rf)
        for cap in CAPS:
            for rung in RUNGS:
                t_ = cell(pname, 0.75, cap, rung, "TOTAL"); e_ = cell(pname, 0.75, cap, rung, "EXCESS")
                d_book = e_.Sharpe - t_.Sharpe
                d_spy = e_.spy_Sharpe - t_.spy_Sharpe
                pred.append(dict(panel=pname, cap=cname(cap), cost_bps=rung, rf_ann=rf_ann,
                                 mean_gross=t_.mean_gross, mean_risk_gross=t_.mean_risk_gross,
                                 mean_sweep=t_.mean_sweep, vol=t_.Vol, spy_vol=t_.spy_Vol,
                                 d_book=d_book, pred_book=-rf_ann / t_.Vol,
                                 d_spy=d_spy, pred_spy=-rf_ann / t_.spy_Vol,
                                 net=d_book - d_spy))
                if rung == HEADLINE_RUNG:
                    say(f"  {pname:5s} {cname(cap):6s} {rung:4.0f} | {t_.mean_risk_gross:10.4f} |"
                        f" {t_.mean_sweep:10.2%} | {t_.Vol:6.2%} | {d_book:+16.4f} |"
                        f" {-rf_ann / t_.Vol:+18.4f} | {d_spy:+11.4f} |"
                        f" {-rf_ann / t_.spy_Vol:+13.4f} | {d_book - d_spy:+9.4f}")
    pdf = pd.DataFrame(pred); pdf.to_csv(f"{OUT}.prediction.csv", index=False)
    say(f"\n  Over all {len(pdf)} (panel, cap, rung) cells at gross 0.75:")
    say(f"   the numeraire costs the BOOK more Sharpe than it costs SPY in"
        f" {int((pdf.net < 0).sum())} of {len(pdf)} cells"
        f"  (mean net swing {pdf.net.mean():+.4f}, worst {pdf.net.min():+.4f})")
    say(f"   realised vs predicted book hit: mean realised {pdf.d_book.mean():+.4f}"
        f" vs predicted {pdf.pred_book.mean():+.4f}  (corr {pdf.d_book.corr(pdf.pred_book):+.4f})")
    say(f"   realised vs predicted SPY  hit: mean realised {pdf.d_spy.mean():+.4f}"
        f" vs predicted {pdf.pred_spy.mean():+.4f}")

    # ------------------------------------------------------------ C. what flips
    say("\n=== C. THE WHOLE QUESTION: WHICH 4b LEGS FLIP WHEN THE NUMERAIRE IS MADE CONSISTENT? ===")
    flips = []
    for pname in panels:
        for gross in GROSSES:
            for cap in CAPS:
                for rung in RUNGS:
                    t_ = cell(pname, gross, cap, rung, "TOTAL"); e_ = cell(pname, gross, cap, rung, "EXCESS")
                    flips.append(dict(panel=pname, gross=gross, cap=cname(cap), cost_bps=rung,
                                      t4b=bool(t_.pass4b), e4b=bool(e_.pass4b),
                                      t4a=bool(t_.pass4a), e4a=bool(e_.pass4a),
                                      **{f"t_{x}": bool(t_[x]) for x in
                                         ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")},
                                      **{f"e_{x}": bool(e_[x]) for x in
                                         ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")},
                                      dSharpe=e_.Sharpe - t_.Sharpe,
                                      dOOS_Sharpe=e_.OOS_Sharpe - t_.OOS_Sharpe,
                                      dCAGR=e_.CAGR - t_.CAGR))
    fl = pd.DataFrame(flips); fl.to_csv(f"{OUT}.flips.csv", index=False)
    say(f"  over all {len(fl)} (panel, gross, cap, rung) cells:")
    say(f"   4b: TOTAL {int(fl.t4b.sum())} pass -> EXCESS {int(fl.e4b.sum())} pass"
        f"   (pass->fail {int((fl.t4b & ~fl.e4b).sum())}, fail->pass {int((~fl.t4b & fl.e4b).sum())})")
    say(f"   4a: TOTAL {int(fl.t4a.sum())} pass -> EXCESS {int(fl.e4a.sum())} pass"
        f"   (pass->fail {int((fl.t4a & ~fl.e4a).sum())}, fail->pass {int((~fl.t4a & fl.e4a).sum())})")
    say("   per-leg flips (TOTAL pass -> EXCESS fail / TOTAL fail -> EXCESS pass):")
    for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        pf = int((fl[f"t_{x}"] & ~fl[f"e_{x}"]).sum()); fp = int((~fl[f"t_{x}"] & fl[f"e_{x}"]).sum())
        say(f"    {x:7s}  pass->fail {pf:3d}   fail->pass {fp:3d}"
            f"   (TOTAL {int(fl[f't_{x}'].sum())}/{len(fl)} -> EXCESS {int(fl[f'e_{x}'].sum())}/{len(fl)})")
    say("   by cost rung:")
    for rung in RUNGS:
        q = fl[fl.cost_bps == rung]
        say(f"    {rung:5.1f} bps: 4b {int(q.t4b.sum()):2d}/{len(q)} -> {int(q.e4b.sum()):2d}/{len(q)}"
            f"   4a {int(q.t4a.sum()):2d}/{len(q)} -> {int(q.e4a.sum()):2d}/{len(q)}")
    say("   by panel:")
    for pname in panels:
        q = fl[fl.panel == pname]
        say(f"    {pname:5s}: 4b {int(q.t4b.sum()):2d}/{len(q)} -> {int(q.e4b.sum()):2d}/{len(q)}"
            f"   4a {int(q.t4a.sum()):2d}/{len(q)} -> {int(q.e4a.sum()):2d}/{len(q)}")

    say("\n  THE COMMITTED CANDIDATE'S OWN MARGINS, BOTH NUMERAIRES (cap 0.020, gross 0.75):")
    say("  panel  bps num    | m_H1     m_H2     m_OOS    m_DD      m_CAGR   | 4b")
    for pname in panels:
        for rung in RUNGS:
            for num in NUMERAIRES:
                r = cell(pname, 0.75, 0.020, rung, num)
                say(f"  {pname:5s} {rung:4.0f} {num:6s} | {r.m_H1:+8.4f} {r.m_H2:+8.4f} {r.m_OOS:+8.4f}"
                    f" {r.m_DD:+9.2%} {r.m_CAGR:+8.2%} | {'PASS' if r.pass4b else 'fail'}")

    # ------------------------------------------------------------ D. joint / KEEP counts
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    for num in NUMERAIRES:
        d = df[df.numeraire == num]
        say(f"  {num:6s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same gross, cap, rung, numeraire):")
    jt = []
    for num in NUMERAIRES:
        for gross in GROSSES:
            for cap in CAPS:
                for rung in RUNGS:
                    u = cell("U56", gross, cap, rung, num); v = cell("B136", gross, cap, rung, num)
                    jt.append(dict(numeraire=num, gross=gross, cap=cname(cap), cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    for num in NUMERAIRES:
        q = jf[jf.numeraire == num]
        say(f"   {num:6s}: joint 4b {int(q.joint.sum())} of {len(q)} cells")
    if int(jf[jf.numeraire == "EXCESS"].joint.sum()):
        say("   EXCESS-numeraire joint cells:")
        for _, r in jf[(jf.numeraire == "EXCESS") & jf.joint].iterrows():
            say(f"     gross {r.gross:.2f} cap {r.cap} {r.cost_bps:.0f} bps")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (gross, cap) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read")
    say("    ONCE, separately under EACH numeraire, and scored against the COMMITTED cap 0.020 / 0.75 cell. ===")
    wf = []
    for pname in panels:
        for num in NUMERAIRES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.numeraire == num) & (df.cost_bps == rung)]
                cm = d[(d.cap == cname(HEADLINE_CAP)) & (d.gross == HEADLINE_GROSS)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, numeraire=num, cost_bps=rung, chooser=chooser,
                                   pick_cap=pk.cap, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                   OOS_MaxDD=pk.OOS_MaxDD, pick_turn=pk.turnover_yr,
                                   committed_turn=cm.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe, committed_OOS_CAGR=cm.OOS_CAGR,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 numeraires x {len(RUNGS)} rungs x 2 choosers).")
    for num in NUMERAIRES:
        q = wfd[wfd.numeraire == num]
        say(f"   {num:6s}: beating SPY's OOS Sharpe {int((q.OOS_Sharpe > q.spy_OOS_Sharpe).sum())}/{len(q)}"
            f"   beating the live book's {int((q.OOS_Sharpe > q.base_OOS_Sharpe).sum())}/{len(q)}"
            f"   beating the COMMITTED cell's {int((q.OOS_Sharpe > q.committed_OOS_Sharpe).sum())}/{len(q)}"
            f"   full-sample 4b {int(q.full4b.sum())}/{len(q)}")
        say(f"           pick over cap: " + "  ".join(
            f"{cname(c)}:{int((q.pick_cap == cname(c)).sum())}" for c in CAPS)
            + "   over gross: " + "  ".join(f"{g:.2f}:{int((q.pick_gross == g).sum())}" for g in GROSSES))
        say(f"           mean OOS Sharpe of the picks {q.OOS_Sharpe.mean():.4f}"
            f"  committed cell {q.committed_OOS_Sharpe.mean():.4f}"
            f"  SPY {q.spy_OOS_Sharpe.mean():.4f}"
            f"  mean OOS CAGR picks {q.OOS_CAGR.mean():.2%} vs SPY {q.spy_OOS_CAGR.mean():.2%}")
    same = 0
    for pname in panels:
        for rung in RUNGS:
            for chooser in ("C_ISSHARPE", "C_ISCALMAR"):
                t_ = wfd[(wfd.panel == pname) & (wfd.numeraire == "TOTAL") & (wfd.cost_bps == rung)
                         & (wfd.chooser == chooser)].iloc[0]
                e_ = wfd[(wfd.panel == pname) & (wfd.numeraire == "EXCESS") & (wfd.cost_bps == rung)
                         & (wfd.chooser == chooser)].iloc[0]
                same += int(t_.pick_cap == e_.pick_cap and t_.pick_gross == e_.pick_gross)
    say(f"\n   DOES THE NUMERAIRE MOVE THE RULE-8 PICK?  the TOTAL and EXCESS choosers agree on"
        f" {same} of {len(wfd) // 2} (panel, rung, chooser) triples.")
    say("\n   panel num    bps chooser     | pick        OOS CAGR  OOS Sh  turn/yr | committed OOS Sh"
        " | SPY OOS Sh")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.numeraire:6s} {r.cost_bps:4.0f} {r.chooser:11s} |"
            f" {r.pick_cap + '/' + format(r.pick_gross, '.2f'):11s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f}"
            f" {r.pick_turn:7.2f} | {r.committed_OOS_Sharpe:16.4f} | {r.spy_OOS_Sharpe:10.4f}")

    # ------------------------------------------------------------ G8 the numeraire bites
    bite_ok = True; worst = None
    for pname in panels:
        for cap in CAPS:
            t_ = cell(pname, 0.75, cap, HEADLINE_RUNG, "TOTAL")
            e_ = cell(pname, 0.75, cap, HEADLINE_RUNG, "EXCESS")
            if not (e_.Sharpe < t_.Sharpe and e_.spy_Sharpe < t_.spy_Sharpe):
                bite_ok = False
            d_ = e_.Sharpe - t_.Sharpe
            worst = d_ if worst is None else min(worst, d_)
    gate("G8 the numeraire BITES (Sharpe falls for the book AND for SPY on every panel/cap)",
         f"all fall: {bite_ok}; largest book Sharpe loss {worst:+.4f}", "True", bite_ok)

    say("\n=== F. BOOK FACTS (exposure is the whole mechanism — published, never selected on) ===")
    say("  panel cap    gross | risk gross | SHY sleeve | mean names | turnover/yr | max name w")
    for _, e in bf.iterrows():
        say(f"  {e.panel:5s} {e.cap:6s} {e.gross:.2f}  | {e.mean_risk_gross:10.4f} | {e.mean_sweep:10.2%} |"
            f" {e.mean_names:10.2f} | {e.turnover_yr:11.2f} | {e.max_name_w:10.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
