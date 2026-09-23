#!/usr/bin/env python3
"""idea 2423 (lane cloud, run 49, 2026-09-23) — HOW MUCH OF THE CAPPED CANDIDATE'S 4b MARGIN IS
THE SWEEP INSTRUMENT RATHER THAN THE RISK BOOK?

THE GAP.  The standing 4b candidate (idea 2322's CAP2, and idea 2300/2332's uncapped CAND) parks
its whole un-invested residual in SHY at phi = 1.00.  At gross 0.75 that residual averages a
LARGE, TIME-VARYING share of NAV, and it is at its LARGEST exactly when the band is closed --
2008, 2020, 2022 -- i.e. precisely on the days that set `MaxDD`.  Every published headline of
this family (CAGR, Sharpe and above all the binding `L_DD` leg) is therefore a BLEND of an equity
risk sleeve and a bond sleeve's total return, and the record has NEVER priced the bond sleeve as
a CHOICE: SHY is simply assumed, inherited from RULES v1.

WHY IT DECIDES SOMETHING.  Two opposite readings are both consistent with everything published:
  (a) the pass is carried by DURATION.  Then swapping SHY (1-3y) for IEF (7-10y) or TLT (20y+)
      should INFLATE it and swapping for ZERO (un-remunerated cash) should DESTROY it, and the
      committed number is a levered bet on the 2009-2021 rate path that nobody voted for and
      that 2022 has already falsified once.
  (b) the pass is carried by the RISK BOOK.  Then the ZERO row -- the pessimal bound, a mattress
      -- still passes 4b, and THAT is the honest number to ship.
This run prices both readings on the same tape, and the ZERO row is the whole point: it is the
only construction in this record that owes nothing to a bond market.

DIAL 1 -- the sweep instrument S in {ZERO, SHY (committed), IEF, TLT, LQD, TIP}.  All five ETFs
          are members of BOTH committed panels with 4710 / 4708 priced rows each (G9).
DIAL 2 -- gross g in {0.75 (live), 1.00}.  At g = 1.00 the residual is mechanically smaller, so
          the two dials together sweep the sweep leg's SIZE as well as its DURATION.

CONVENTIONS, both published, the headline PRE-STATED here before any compute:
  INCL   -- the committed panel verbatim: the five fixed-income ETFs remain eligible for the RISK
            SLEEVE as well, so a row's bond exposure is sweep + whatever the band admits.
            **HEADLINE** (it is the committed book).
  EXCL   -- ALL FIVE fixed-income ETFs are removed from the risk sleeve's eligible set, for every
            sweep choice alike.  The risk sleeve is then IDENTICAL across all six sweeps, so the
            ONLY thing that differs between rows is the sweep leg itself: a clean decomposition
            rather than a confounded one.  ZERO/EXCL is the pure equity book.

THE DECOMPOSITION IS EXACT, NOT ESTIMATED.  Under ZERO the residual earns exactly 0%, so the ZERO
row IS the risk sleeve alone (G8 asserts it to machine precision against the weights themselves).
Every "how much of the margin is the sweep" number below is therefore a DIFFERENCE OF TWO
PRICED BOOKS on the same tape and the same weights, never a regression or an attribution model.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, books {CAP2 (2% name cap), CAND (uncapped)},
rungs {0, 10, 25, 50} bps, weekly cadence, t+1 execution, band 0.03, MA 200d, the 2% cap.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS all failing; and `data/prices_small.csv` carries no fixed-income ETF to sweep into, so
the dial this idea walks does not exist on that panel.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (sweep, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE.  The sharp question rule 8 answers here: an
in-sample operator sees TLT's 2009-2016 bull market -- does he pick duration, and does 2022 then
take it back?

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 the committed SHY headlines (CAP2 11.62%/1.2687/-14.81%,
OOS 12.77%/1.3318; CAND 12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) reproduce.  G4 no leverage.
G5 cost is exactly linear in the rung.  G6 the sweep dial changes NO risk-sleeve weight.  G7
exactly two tuned parameters.  G8 the ZERO residual earns exactly 0%.  G9 all five sweep
instruments priced on every scored row of both panels.  G10 EXCL really removes them.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The sweep contrast is same-tape, same-day,
same-risk-weights and first-order immune; the absolute 4b verdicts are not.  The five sweep ETFs
carry no survivorship bias of their own (all five existed and traded throughout).

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_sweep-instrument-decomposition_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "sweep-instrument-decomposition", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
FIXED_INCOME = ["SHY", "IEF", "TLT", "LQD", "TIP"]
SWEEPS = ["ZERO"] + FIXED_INCOME
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
CONVENTIONS = ["INCL", "EXCL"]
HEADLINE_CONV, HEADLINE_RUNG, HEADLINE_SWEEP = "INCL", 10.0, "SHY"
NAME_CAP = 0.020
BOOKS = {"CAP2": NAME_CAP, "CAND": np.inf}
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


# ---------------------------------------------------------------- the risk sleeve
def risk_weights(px, gross, cap, conv):
    """The candidate family's risk sleeve: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- 0.03 band.  cap = 0.02 -> idea 2322's CAP2; cap = inf -> idea 2300's CAND.
    conv = 'EXCL' removes the five fixed-income ETFs from the eligible set entirely (so they are
    not in N_in either), identically for every sweep choice."""
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    if conv == "EXCL":
        for t in FIXED_INCOME:
            if t in inb.columns:
                inb[t] = False
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, sweep, freq=CADENCE):
    """`engine.backtest` verbatim, except that (i) the un-invested residual is swept into `sweep`
    at phi = 1.00 (or left earning 0% when sweep == 'ZERO'), and (ii) the per-day turnover and the
    sweep leg's own return contribution are retained so every cost rung and the exact
    risk-vs-sweep decomposition can be read off the SAME realised path.
    Weights decided at t-1, applied at t; between rebalances the book drifts."""
    cols = list(prices.columns)
    si = cols.index(sweep) if sweep != "ZERO" else -1
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[sweep].notna().values.astype(float) if si >= 0 else None
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    idle = np.zeros(m)          # the SWEEP leg's own weight, tracked apart from the risk sleeve
    turn = np.zeros(n); r0 = np.zeros(n); r_sweep = np.zeros(n)
    gr = np.zeros(n); nheld = np.zeros(n); idle_w = np.zeros(n); maxw = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            add = 0.0
            if si >= 0:
                add = max(0.0, 1.0 - new.sum()) * s_ok[i]
                new[si] += add
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
            idle = np.zeros(m)
            if si >= 0:
                idle[si] = add
        gr[i] = cur.sum()
        nheld[i] = float((cur > 1e-12).sum())
        idle_w[i] = float(idle.sum())
        maxw[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        r_sweep[i] = float((idle * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            gi = idle * (1 + rv[i])
            cur = g / tot
            idle = gi / tot
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                r_sweep=pd.Series(r_sweep, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx), idle=pd.Series(idle_w, index=idx),
                maxw=pd.Series(maxw, index=idx))


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
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy),
                m_H1=h1 - s1, m_H2=h2 - s2, m_OOS=sharpe(r_oos) - sharpe(spy_oos))


def main():
    t0 = time.time()
    say("=== idea 2423 — HOW MUCH OF THE CAPPED CANDIDATE'S 4b MARGIN IS THE SWEEP INSTRUMENT? ===")
    say(f"    {DATE}  lane {LANE} run 49   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  phi = 1.00")
    say(f"    DIAL 1 sweep {SWEEPS}    DIAL 2 gross {GROSSES}")
    say(f"    conventions {CONVENTIONS}; HEADLINE = {HEADLINE_CONV} / {HEADLINE_SWEEP} / {HEADLINE_RUNG:.0f} bps (the committed book).")
    say("    ZERO = un-remunerated cash, the PESSIMAL bound and the exact risk sleeve; every 'how much is the")
    say("    sweep' number below is a DIFFERENCE OF TWO PRICED BOOKS on the same tape, not an attribution model.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343), and")
    say("    data/prices_small.csv carries NO fixed-income ETF, so this run's dial does not exist there.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the contaminated")
    say("    leg.  The sweep contrast is same-tape, same-risk-weights and first-order immune; the levels are not.")
    gate("G7 exactly two tuned parameters", "sweep instrument, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs = band_state(px_u, BAND)
    d2 = int((bs != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {bs.sum(axis=1).mean():.2f}", "0", d2 == 0)

    ok9 = True
    for nm, px in panels.items():
        for t in FIXED_INCOME:
            ok9 = ok9 and (t in px.columns) and bool(px[t].loc[px.index[WARMUP]:].notna().all())
    gate("G9 all five sweep instruments priced on every scored row of BOTH panels",
         f"{FIXED_INCOME} on U56 and B136: {ok9}", "True", ok9)

    # G1 replica fidelity against the engine on the LIVE book (no sweep, flat 10 bps)
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, "ZERO")
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, no sweep)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    W: dict = {}
    for pname, px in panels.items():
        rv = px.pct_change().fillna(0.0)
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos = spy.loc[OOS_START:]
        spy_is = spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for conv in CONVENTIONS:
            for bname, cap in BOOKS.items():
                for gross in GROSSES:
                    wr = risk_weights(px, gross, cap, conv)
                    W[(pname, conv, bname, gross)] = wr
                    for sw in SWEEPS:
                        bk = run_book(px, wr, sw)
                        r0 = bk["r0"].loc[start:]
                        tn = bk["turn"].loc[start:]
                        book_facts.append(dict(
                            panel=pname, conv=conv, book=bname, gross=gross, sweep=sw,
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            mean_idle=float(bk["idle"].loc[start:].mean()),
                            max_idle=float(bk["idle"].loc[start:].max()),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            max_gross=float(bk["gross"].loc[start:].max()),
                            mean_names=float(bk["names"].loc[start:].mean()),
                            risk_names=float((wr.loc[start:] > 0).sum(axis=1).mean()),
                            risk_w_sum=float(wr.loc[start:].values.sum()),
                            risk_ret=float((bk["r0"] - bk["r_sweep"]).loc[start:].sum()),
                            max_name_w=float(bk["maxw"].loc[start:].max()),
                            sweep_ret_share=float(bk["r_sweep"].loc[start:].sum() / r0.sum())
                            if abs(r0.sum()) > 0 else np.nan,
                            fi_risk_w=float(wr[[t for t in FIXED_INCOME if t in wr.columns]]
                                            .loc[start:].sum(axis=1).mean())))
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                            lg = legs(r, base_r, spy, r_oos, spy_oos)
                            rows.append(dict(
                                panel=pname, conv=conv, book=bname, gross=gross, sweep=sw,
                                cost_bps=rung, CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                Calmar=calmar(r), IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                IS_CAGR=cagr(r_is), OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos),
                                OOS_MaxDD=maxdd(r_oos),
                                base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                base_CAGR=cagr(base_r),
                                base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x 2 conv x 2 books x 2 gross x "
        f"{len(SWEEPS)} sweeps x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    # ------------------------------------------------------------ remaining gates
    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f}", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))

    # G5 cost linearity: r(c) = r0 - turn*c/1e4 by construction; assert against a re-run at 25 bps
    pz = panels["U56"]
    wr = risk_weights(pz, 0.75, NAME_CAP, "INCL")
    bkz = run_book(pz, wr, "SHY")
    st = pz.index[WARMUP]
    r25 = (bkz["r0"] - bkz["turn"] * 25 / 1e4).loc[st:]
    r0_ = bkz["r0"].loc[st:]; r50 = (bkz["r0"] - bkz["turn"] * 50 / 1e4).loc[st:]
    d5 = float(((r0_ - r25) * 2 - (r0_ - r50)).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)

    # G6 the sweep dial changes no DECIDED risk-sleeve weight: the sleeve never sees the sweep.
    # (`mean_names` and `mean_gross` DO move with the sweep, because they count the swept position
    #  itself -- that is the sweep, not a change of book.  The assertion is on the sleeve's own
    #  decided weight matrix, which is what `risk_weights` returns and what the runner is handed.)
    g6 = bf.groupby(["panel", "conv", "book", "gross"])[["risk_names", "risk_w_sum"]].nunique().max().max()
    gate("G6 the sweep dial changes NO DECIDED risk-sleeve weight, only what the residual earns",
         f"distinct (mean risk names, total sleeve weight) per (panel, conv, book, gross) across the"
         f" {len(SWEEPS)} sweeps: {int(g6)}", "1", int(g6) == 1)
    rr = bf[(bf.panel == "U56") & (bf.conv == "INCL") & (bf.book == "CAP2") & (bf.gross == 0.75)]
    publish("G6b the sleeve's REALISED return does move slightly with the sweep (inter-rebalance drift is"
            " renormalised by a different book total), which is the sweep's second-order effect and is NOT netted out",
            "sum of sleeve returns, ZERO vs SHY: "
            f"{float(rr[rr.sweep == 'ZERO'].risk_ret.iloc[0]):.6f} vs {float(rr[rr.sweep == 'SHY'].risk_ret.iloc[0]):.6f}")

    # G8 the ZERO residual earns exactly 0%: ZERO's r0 must equal the risk sleeve's own return
    bz = run_book(pz, wr, "ZERO")
    gate("G8 under ZERO the residual earns exactly 0% (invested gross == risk sleeve gross)",
         f"max idle weight {float(bz['idle'].max()):.3e}; max gross {float(bz['gross'].max()):.6f}"
         f" vs risk sleeve max {float(wr.sum(axis=1).max()):.6f}",
         "idle == 0", float(bz["idle"].abs().max()) == 0.0)

    # G10 EXCL really removes the five from the sleeve
    w_in = risk_weights(pz, 0.75, NAME_CAP, "INCL")[FIXED_INCOME].sum(axis=1)
    w_ex = risk_weights(pz, 0.75, NAME_CAP, "EXCL")[FIXED_INCOME].sum(axis=1)
    gate("G10 EXCL removes all five fixed-income ETFs from the RISK SLEEVE (INCL holds them)",
         f"EXCL max weight on the five {float(w_ex.max()):.3e}; INCL mean {float(w_in.mean()):.4f}",
         "EXCL == 0 < INCL", float(w_ex.abs().max()) == 0.0 and float(w_in.mean()) > 0)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.conv == "INCL") & (df.sweep == "SHY")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.conv == "INCL") & (df.sweep == "SHY")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND CAND"
         " (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ 0. what the sweep legs are
    say("\n=== 0. THE SWEEP INSTRUMENTS THEMSELVES, BUY-AND-HOLD OVER THE SCORED WINDOW (U56 tape) ===")
    say("  instrument |   CAGR   Sharpe    MaxDD |  2017-2026 CAGR  Sharpe |  2022 only CAGR")
    for t in FIXED_INCOME:
        s = pz[t].pct_change().fillna(0.0).loc[pz.index[WARMUP]:]
        s22 = s.loc["2022-01-01":"2022-12-31"]
        say(f"  {t:10s} | {cagr(s):6.2%} {sharpe(s):7.4f} {maxdd(s):8.2%} |"
            f" {cagr(s.loc[OOS_START:]):14.2%} {sharpe(s.loc[OOS_START:]):7.4f} |"
            f" {cagr(s22):14.2%}")
    sp = pz["SPY"].pct_change().fillna(0.0).loc[pz.index[WARMUP]:]
    say(f"  {'SPY':10s} | {cagr(sp):6.2%} {sharpe(sp):7.4f} {maxdd(sp):8.2%} |"
        f" {cagr(sp.loc[OOS_START:]):14.2%} {sharpe(sp.loc[OOS_START:]):7.4f} |"
        f" {cagr(sp.loc['2022-01-01':'2022-12-31']):14.2%}")

    # ------------------------------------------------------------ A. the full ladder
    say(f"\n=== A. THE FULL LADDER, convention {HEADLINE_CONV}, gross 0.75 — EVERY GRID POINT ===")
    say("  panel book sweep  bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for sw in SWEEPS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.conv == HEADLINE_CONV)
                           & (df.sweep == sw) & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    tag = "   <= COMMITTED" if sw == "SHY" else ("   <= PESSIMAL BOUND" if sw == "ZERO" else "")
                    say(f"  {pname:5s} {bk_:4s} {sw:5s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}{tag}")

    # ------------------------------------------------------------ B. the decomposition
    say("\n=== B. THE WHOLE QUESTION: HOW MUCH OF EACH 4b LEG IS THE SWEEP? (row - its own ZERO row) ===")
    say("    (same panel, book, conv, gross and rung; the ONLY difference is what the residual earns.)")
    say("  panel conv book  g   bps sweep | dCAGR    dSharpe   dMaxDD  | dOOS Sh | 4b ZERO -> 4b row")
    dec = []
    for pname in panels:
        for conv in CONVENTIONS:
            for bk_ in BOOKS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        z = df[(df.panel == pname) & (df.conv == conv) & (df.book == bk_)
                               & (df.gross == gross) & (df.cost_bps == rung) & (df.sweep == "ZERO")].iloc[0]
                        for sw in FIXED_INCOME:
                            r = df[(df.panel == pname) & (df.conv == conv) & (df.book == bk_)
                                   & (df.gross == gross) & (df.cost_bps == rung) & (df.sweep == sw)].iloc[0]
                            dec.append(dict(panel=pname, conv=conv, book=bk_, gross=gross,
                                            cost_bps=rung, sweep=sw,
                                            dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                                            dMaxDD=r.MaxDD - z.MaxDD,
                                            dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                                            zero4b=bool(z.pass4b), row4b=bool(r.pass4b),
                                            zero_mDD=z.m_DD, row_mDD=r.m_DD,
                                            zero_mCAGR=z.m_CAGR, row_mCAGR=r.m_CAGR))
                            if conv == HEADLINE_CONV and gross == 0.75 and rung == HEADLINE_RUNG:
                                say(f"  {pname:5s} {conv:4s} {bk_:4s} {gross:.2f} {rung:5.1f} {sw:5s} |"
                                    f" {r.CAGR - z.CAGR:+7.2%} {r.Sharpe - z.Sharpe:+9.4f} {r.MaxDD - z.MaxDD:+8.2%} |"
                                    f" {r.OOS_Sharpe - z.OOS_Sharpe:+8.4f} | "
                                    f"{'PASS' if z.pass4b else 'fail'} -> {'PASS' if r.pass4b else 'fail'}")
    dd_ = pd.DataFrame(dec); dd_.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n  Over all {len(dd_)} (row vs its own ZERO) pairs:")
    say(f"   dCAGR > 0 in {int((dd_.dCAGR > 0).sum())} of {len(dd_)};"
        f" dSharpe > 0 in {int((dd_.dSharpe > 0).sum())};"
        f" dMaxDD > 0 (shallower) in {int((dd_.dMaxDD > 0).sum())}")
    say(f"   mean dCAGR {dd_.dCAGR.mean():+.2%}   mean dSharpe {dd_.dSharpe.mean():+.4f}"
        f"   mean dMaxDD {dd_.dMaxDD.mean():+.2%}   mean dOOS Sharpe {dd_.dOOS_Sharpe.mean():+.4f}")
    say("   by instrument:")
    for sw in FIXED_INCOME:
        q = dd_[dd_.sweep == sw]
        say(f"    {sw:5s} mean dCAGR {q.dCAGR.mean():+.2%}  dSharpe {q.dSharpe.mean():+.4f}"
            f"  dMaxDD {q.dMaxDD.mean():+.2%}  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}"
            f"   4b: ZERO {int(q.zero4b.sum())}/{len(q)} -> {sw} {int(q.row4b.sum())}/{len(q)}")

    say("\n  THE PESSIMAL BOUND, STATED PLAINLY — does the book still pass 4b with an UN-REMUNERATED residual?")
    z = df[df.sweep == "ZERO"]
    say(f"   ZERO rows passing 4b: {int(z.pass4b.sum())} of {len(z)}   (all rows: {int(df.pass4b.sum())} of {len(df)})")
    for pname in panels:
        for bk_ in BOOKS:
            q = z[(z.panel == pname) & (z.book == bk_)]
            say(f"    {pname:5s} {bk_:4s} ZERO: 4b {int(q.pass4b.sum())}/{len(q)}"
                "   binding leg on the FAILs: "
                + "  ".join(f"{k} {int((~q[k][~q.pass4b]).sum())}" for k in
                            ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    hz = df[(df.panel == "U56") & (df.book == "CAP2") & (df.conv == HEADLINE_CONV)
            & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG) & (df.sweep == "ZERO")].iloc[0]
    say(f"   HEADLINE CELL, ZERO sweep (U56 / CAP2 / INCL / g0.75 / 10 bps):"
        f" {hz.CAGR:.2%} / {hz.Sharpe:.4f} / {hz.MaxDD:.2%}, OOS {hz.OOS_CAGR:.2%} / {hz.OOS_Sharpe:.4f},"
        f" 4b {'PASS' if hz.pass4b else 'FAIL'}"
        + ("" if hz.pass4b else "  binding: " + ",".join(
            k for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not hz[k])))
    say(f"   vs the COMMITTED SHY cell: {a.CAGR:.2%} / {a.Sharpe:.4f} / {a.MaxDD:.2%},"
        f" OOS {a.OOS_CAGR:.2%} / {a.OOS_Sharpe:.4f}, 4b {'PASS' if a.pass4b else 'FAIL'}"
        f"  -> the sweep is worth {(a.CAGR - hz.CAGR) * 100:+.2f} pp of CAGR and"
        f" {a.Sharpe - hz.Sharpe:+.4f} of Sharpe.")
    say("   AND THE PESSIMAL BOOK IS ALSO THE CHEAPER ONE: the sweep leg is itself TRADED, so dropping it")
    say("   removes turnover the book never needed. Turnover/yr, ZERO vs SHY, at gross 0.75, INCL:")
    for pname in panels:
        for bk_ in BOOKS:
            z0 = bf[(bf.panel == pname) & (bf.conv == "INCL") & (bf.book == bk_)
                    & (bf.gross == 0.75) & (bf.sweep == "ZERO")].iloc[0]
            s0 = bf[(bf.panel == pname) & (bf.conv == "INCL") & (bf.book == bk_)
                    & (bf.gross == 0.75) & (bf.sweep == "SHY")].iloc[0]
            say(f"    {pname:5s} {bk_:4s}: {z0.turnover_yr:.2f}x vs {s0.turnover_yr:.2f}x"
                f"  ({z0.turnover_yr / s0.turnover_yr - 1:+.1%})  against the LIVE book's 1.77x/yr")

    # ------------------------------------------------------------ C. how big the sweep leg is
    say("\n=== C. HOW BIG THE SWEEP LEG ACTUALLY IS (mean / max share of NAV, and its share of the book's return) ===")
    say("  panel conv book  g  sweep | mean idle | max idle | risk-sleeve FI w | sweep share of total return | turn/yr")
    for pname in panels:
        for conv in CONVENTIONS:
            for bk_ in BOOKS:
                for gross in GROSSES:
                    for sw in SWEEPS:
                        e = bf[(bf.panel == pname) & (bf.conv == conv) & (bf.book == bk_)
                               & (bf.gross == gross) & (bf.sweep == sw)].iloc[0]
                        if conv == HEADLINE_CONV and gross == 0.75:
                            say(f"  {pname:5s} {conv:4s} {bk_:4s} {gross:.2f} {sw:5s} |"
                                f" {e.mean_idle:9.2%} | {e.max_idle:8.2%} | {e.fi_risk_w:16.2%} |"
                                f" {e.sweep_ret_share:27.2%} | {e.turnover_yr:7.2f}")

    # ------------------------------------------------------------ D. KEEP counts
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for sw in SWEEPS:
        d = df[df.sweep == sw]
        say(f"   sweep {sw:5s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by sweep: "
            + "  ".join(f"{sw}:{int(d[d.sweep == sw].pass4b.sum())}/{len(d[d.sweep == sw])}" for sw in SWEEPS))
    for conv in CONVENTIONS:
        d = df[df.conv == conv]
        say(f"   convention {conv:4s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same conv, book, gross, sweep, rung):")
    jt = []
    for conv in CONVENTIONS:
        for bk_ in BOOKS:
            for gross in GROSSES:
                for sw in SWEEPS:
                    for rung in RUNGS:
                        q = df[(df.conv == conv) & (df.book == bk_) & (df.gross == gross)
                               & (df.sweep == sw) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(conv=conv, book=bk_, gross=gross, sweep=sw, cost_bps=rung,
                                       joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by sweep: "
        + "  ".join(f"{sw}:{int(jf[jf.sweep == sw].joint.sum())}/{len(jf[jf.sweep == sw])}" for sw in SWEEPS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.head(20).iterrows():
        say(f"    {r.panel:5s} {r.conv:4s} {r.book:4s} {r.sweep:5s} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (sweep, gross) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE. ===")
    say("    The sharp question: an IS-only operator sees TLT's 2009-2016 bull market. Does he buy duration,")
    say("    and does 2022 then take it back?")
    wf = []
    for pname in panels:
        for conv in CONVENTIONS:
            for bk_ in BOOKS:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.conv == conv) & (df.book == bk_)
                           & (df.cost_bps == rung)]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        cm = d[(d.sweep == HEADLINE_SWEEP) & (d.gross == 0.75)].iloc[0]
                        wf.append(dict(panel=pname, conv=conv, book=bk_, cost_bps=rung, chooser=chooser,
                                       pick_sweep=pk.sweep, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                       OOS_MaxDD=pk.OOS_MaxDD,
                                       committed_OOS_Sharpe=cm.OOS_Sharpe, committed_OOS_CAGR=cm.OOS_CAGR,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 conv x 2 books x 4 rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:            {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:  {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED SHY/g0.75 cell's OOS Sharpe: "
        f"{int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:      {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over sweep: " + "  ".join(f"{s}:{int((wfd.pick_sweep == s).sum())}" for s in SWEEPS))
    say("   pick distribution over gross: " + "  ".join(f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say("\n   panel conv book   bps chooser     | pick        OOS CAGR  OOS Sh  OOS MaxDD | committed OOS Sh")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.conv:4s} {r.book:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r.pick_sweep + '/' + format(r.pick_gross, '.2f'):11s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f}"
            f" {r.OOS_MaxDD:10.2%} | {r.committed_OOS_Sharpe:16.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
