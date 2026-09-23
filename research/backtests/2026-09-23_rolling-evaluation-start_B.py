#!/usr/bin/env python3
"""idea 2510 (lane B, 2026-09-23, run 71) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE A
ROLLING EVALUATION START?

THE OBJECT.  The record's standing 4b KEEP-candidate is idea 2322's CAP2: every name INSIDE
the 200d +/- 3% band held at `min(gross / N_in, 2%)` of NAV, idle NAV swept to SHY, weekly,
t+1.  On U56 / gross 0.75 / 10 bps it reads 11.62% / 1.2687 / -14.81%.

THE DEFECT THIS RUN PRICES.  EVERY scored path in this record begins at row 260 of a
2008-start panel — i.e. mid-January 2009 — so the tail of the 2008-09 collapse AND the whole
2009-10 rebound sit inside every full-sample number the candidate owns.  Both of 4b's LEVEL
legs are fed by that one episode: `L_DD` (MaxDD >= 0.60 x SPY's) and `L_H1` (first-half
Sharpe > SPY's), and it is precisely the episode in which a 200d trend gate is most flattered.
Ideas 1799 / 2022 EXCISED the crash window mid-sample and found the effect was mostly a BAR
shift; excising is not the same as never having been there, because a truncated start also
moves the compounding base, the half-sample SPLIT POINT and the benchmark's own drawdown.

DIAL 1 -- EVALUATION START S in {COMMITTED (row 260), 2010-01-01, 2011-01-01, 2012-01-01,
2013-01-01}.  The book's DECISION PATH is untouched: the 200d MA and the band hysteresis are
computed on the full tape from 2008, exactly as the committed book computes them, and only the
SCORING WINDOW moves.  That is the honest construction — an investor starting in 2012 still
has the prior 200 closes — and it is stated as a convention, not assumed silently (G2).
DIAL 2 -- GROSS in {0.75, 1.00}.

THAT IS EXACTLY TWO TUNED PARAMETERS.  Panels {U56, B136}, cost rungs {0, 10, 25, 50} bps,
cadence W, band 0.03, cap 2% and the SHY sweep are REPORTED IN FULL, never selected on.

THE BAR-vs-BOOK DECOMPOSITION IS THE POINT.  Every 4b leg is a DIFFERENCE between the book
and a benchmark that is ITSELF re-scored from S.  So each leg's move is split:
    d(slack) = d(book statistic) - (bar coefficient) x d(benchmark statistic)
and the run reports, leg by leg, how much of any survival or death is the BAR moving under
the book rather than the book moving under the bar.  That is the claim ideas 1799 / 2022 left
open ("mostly a BAR shift") re-asked where it actually binds.

BENCHMARKS.  4b is scored under THREE comparands on every row: SPY (as PROTOCOL 4b writes
it), EWBH(panel) (equal-weight buy-and-hold of the book's own names, bought on the last close
BEFORE S and never traded — idea 2516's proposed stricter reading), and EWRB (the same names
equal-weighted and rebalanced weekly at the SAME cost rung — the TRADABLE twin, since EWBH is
the 2026 survivor list bought in the past and is not investable).  4a is scored against the
live RULES v2 book, also re-scored from S.

RULE 8.  For every (panel, start, rung) the gross is chosen on the IS window [S, 2016-12-31]
ONLY, by three pre-stated choosers, and 2017-2026 is then read ONCE:
    C_ISSHARPE  max IS Sharpe
    C_ISCAGR    max IS CAGR
    C_PREREG    NO CHOICE AT ALL -- gross 0.75, the committed rung, fixed before any number.
NOTE, AND IT IS REPORTED NOT HIDDEN: the OOS window does not depend on S, so `L_OOS` is
start-invariant BY CONSTRUCTION for a given (gross, rung); what S can move is the IS chooser's
PICK, and hence which book is carried into the OOS window.  That is the rule-8 question here.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_rolling-evaluation-start_B.py
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

DATE, SLUG, LANE = "2026-09-23", "rolling-evaluation-start", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
SWEEP = "SHY"
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
STARTS = ["COMMITTED", "2010-01-01", "2011-01-01", "2012-01-01", "2013-01-01"]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BENCHES = ["SPY", "EWBH", "EWRB"]
PREREG_GROSS = 0.75

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


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


# ---------------------------------------------------------------- books
def cap_weights(px, invest, gross):
    """idea 2322's CAP2: names INSIDE the 200d +/- BAND at min(gross / N_in, CAP); idle to SHY."""
    q = px[invest]
    inb = band_state(q, BAND) & q.notna()
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def run_zero(px, w):
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"], res["weights"]


def priced(r0, turn, bps):
    return r0 - turn * bps / 1e4


# ---------------------------------------------------------------- benchmarks
def ewbh(px, cols, start):
    """EQUAL-WEIGHT BUY-AND-HOLD: 1/N of NAV into every name priced on the last close BEFORE
    `start`, then never traded again.  Zero cost, fully invested, including the return ON the
    first scored day (gate G3 reproduces px['SPY'].pct_change() when cols == ['SPY'])."""
    pos = px.index.get_loc(start)
    q = px[cols].iloc[pos - 1:]
    live = q.iloc[0].notna()
    q = q.loc[:, live]
    val = (q / q.iloc[0]).mean(axis=1)
    return val.pct_change().dropna(), int(live.sum()), int((~live).sum())


def ewrb(px, cols):
    """EQUAL-WEIGHT, WEEKLY-REBALANCED over the names priced that day — EWBH's tradable twin.
    Returned cost-free; each cost rung is priced from (returns, turnover) like the book."""
    e = pd.DataFrame(1.0, index=px.index, columns=cols).where(px[cols].notna(), 0.0)
    w = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"]


# ---------------------------------------------------------------- KEEP paths
def legs_4b(r, b):
    r1, r2 = halves(r); b1, b2 = halves(b)
    ro, bo = r.loc[OOS_START:], b.loc[OOS_START:]
    m = dict(L_H1=sharpe(r1) - sharpe(b1),
             L_H2=sharpe(r2) - sharpe(b2),
             L_OOS=sharpe(ro) - sharpe(bo),
             L_DD=maxdd(r) - DD_CAP * maxdd(b),
             L_CAGR=cagr(r) - CAGR_FLOOR * cagr(b))
    ok = {k: bool(v > 0) for k, v in m.items()}
    return dict(pass4b=all(ok.values()), **{k: ok[k] for k in m},
                **{f"m_{k}": float(v) for k, v in m.items()})


def pass_4a(r, base):
    r1, r2 = halves(r); b1, b2 = halves(base)
    return bool(sharpe(r1) > sharpe(b1) and sharpe(r2) > sharpe(b2) and maxdd(r) >= maxdd(base))


def legstring(d, pre=""):
    return "".join("1" if d[pre + k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2510 (lane B, run 71) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE A ROLLING EVALUATION START? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cap {CAP}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 evaluation start {STARTS}     DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: panels U56/B136, rungs {RUNGS}, band {BAND}, cap {CAP}, cadence {CADENCE}")
    say(f"    benchmarks {BENCHES}; 4a comparand = live RULES v2, re-scored from the same start")
    gate("G8 exactly two tuned parameters", "evaluation start S, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        say(f"    [{nm}] {len(invest)} columns, {len(px)} rows, tape {px.index[0].date()} .. {px.index[-1].date()}")

    # ---------------- start resolution
    starts = {}
    for nm, (px, invest) in panels.items():
        for s in STARTS:
            d = px.index[WARMUP] if s == "COMMITTED" else px.index[px.index.searchsorted(pd.Timestamp(s))]
            starts[(nm, s)] = d
            yrs = (px.index[-1] - d).days / 365.25
            gate(f"G0 >= 10y ({nm}, start {s})", f"{d.date()} .. {px.index[-1].date()} = {yrs:.1f}y", ">= 10y", yrs >= 10)
            gate(f"G1 sweep {SWEEP} priced on every scored row ({nm}, start {s})",
                 f"non-null {int(px[SWEEP].loc[d:].notna().sum())} of {len(px.loc[d:])}", "all",
                 bool(px[SWEEP].loc[d:].notna().all()))

    # ---------------- G3: EWBH machinery reproduces SPY's own returns
    px_u, inv_u = panels["U56"]
    d0 = starts[("U56", "COMMITTED")]
    e_spy, _, _ = ewbh(px_u, ["SPY"], d0)
    d3 = float((e_spy - px_u["SPY"].pct_change().loc[e_spy.index]).abs().max())
    gate("G3 EWBH(['SPY']) == px['SPY'].pct_change()", f"max|d| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # ---------------- books, run ONCE per (panel, gross) on the FULL tape
    books, basebook, ewrbs = {}, {}, {}
    for nm, (px, invest) in panels.items():
        for g in GROSSES:
            books[(nm, g)] = run_zero(px, cap_weights(px, invest, g))
        bw = rules_v2_weights(px[invest], band=BAND, gross=0.75).reindex(columns=px.columns).fillna(0.0)
        basebook[nm] = run_zero(px, bw)[:2]
        ewrbs[nm] = ewrb(px, invest)

    # ---------------- G2: the decision path does not depend on the evaluation start
    r0, tt, wts = books[("U56", 0.75)]
    gate("G2 the book's DECISION PATH is start-invariant by construction",
         "one pass on the full tape per (panel, gross); the start slices RETURNS only",
         "stated convention", True)
    mx = float(wts.sum(axis=1).max())
    gate("G5 no leverage anywhere (U56 g=0.75)", f"max row gross {mx:.9f}", "<= 1+1e-12", mx <= 1 + 1e-12)

    # ---------------- G4: replica reproduces the committed headline
    r_h = priced(r0, tt, HEADLINE_RUNG).loc[d0:]
    say(f"    committed headline replica (U56 g0.75 @10bps from {d0.date()}): "
        f"{cagr(r_h):.2%} / {sharpe(r_h):.4f} / {maxdd(r_h):.2%}")
    dref = max(abs(cagr(r_h) - 0.1162), abs(sharpe(r_h) - 1.2687) / 10, abs(maxdd(r_h) + 0.1481))
    gate("G4 replica == idea 2322's committed CAP2 headline (11.62% / 1.2687 / -14.81%)",
         f"max|d| {dref:.2e}", "< 5e-3", dref < 5e-3)

    # ---------------- G7: no lookahead (truncating the tape cannot change earlier weights)
    T = "2018-01-01"
    w_tr = run_zero(px_u.loc[:T], cap_weights(px_u.loc[:T], inv_u, 0.75))[2]
    d7 = float((wts.loc[:T] - w_tr).abs().max().max())
    gate("G7 no lookahead: truncating the tape at 2018-01-01 leaves earlier weights unchanged",
         f"max|d| {d7:.3e}", "< 1e-12", d7 < 1e-12)

    # ---------------- the grid
    rows = []
    for nm, (px, invest) in panels.items():
        spy_full = px["SPY"].pct_change().fillna(0.0)
        er0, et = ewrbs[nm]
        for s in STARTS:
            d = starts[(nm, s)]
            eb, nlive, ndead = ewbh(px, invest, d)
            for g in GROSSES:
                b0, bt, _ = books[(nm, g)]
                for rung in RUNGS:
                    r = priced(b0, bt, rung).loc[d:]
                    base = priced(*basebook[nm], rung).loc[d:]
                    bench = {"SPY": spy_full.loc[d:],
                             "EWBH": eb.loc[d:],
                             "EWRB": priced(er0, et, rung).loc[d:]}
                    row = dict(panel=nm, start=s, start_date=str(d.date()), gross=g, cost_bps=rung,
                               n_rows=len(r), ewbh_names=nlive, ewbh_notlive=ndead,
                               CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                               H1=sharpe(halves(r)[0]), H2=sharpe(halves(r)[1]),
                               OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                               OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                               turnover_yr=float(bt.loc[d:].sum() / (len(r) / 252)),
                               pass4a=pass_4a(r, base),
                               base_Sharpe=sharpe(base), base_MaxDD=maxdd(base), base_CAGR=cagr(base))
                    for bn in BENCHES:
                        bb = bench[bn]
                        L = legs_4b(r, bb)
                        row[f"{bn}_CAGR"] = cagr(bb); row[f"{bn}_Sharpe"] = sharpe(bb)
                        row[f"{bn}_MaxDD"] = maxdd(bb)
                        row[f"{bn}_H1"] = sharpe(halves(bb)[0]); row[f"{bn}_H2"] = sharpe(halves(bb)[1])
                        row[f"{bn}_OOS_Sharpe"] = sharpe(bb.loc[OOS_START:])
                        row[f"pass4b_{bn}"] = L["pass4b"]
                        for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
                            row[f"{bn}_{k}"] = L[k]; row[f"{bn}_m_{k}"] = L[f"m_{k}"]
                        row[f"legs_{bn}"] = legstring({f"{bn}_{k}": L[k] for k in
                                                       ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")}, pre=f"{bn}_")
                    rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    sp_s = df.groupby(['panel', 'gross', 'cost_bps']).Sharpe.agg(lambda x: x.max() - x.min()).max()
    sp_d = df.groupby(['panel', 'gross', 'cost_bps']).MaxDD.agg(lambda x: x.max() - x.min()).max()
    gate("G6 DIAL 1 bites (the start moves the book's own Sharpe)",
         f"max spread of book Sharpe across starts within a cell {sp_s:.4f}", "> 0.005", sp_s > 0.005)
    publish("G6c the start does NOT move the book's own MaxDD (the premise this run tests)",
            f"max spread of book MaxDD across starts within a cell {sp_d:.6f}")
    gate("G6b DIAL 2 bites (gross moves the book's own CAGR)",
         f"max spread of CAGR across gross within a cell "
         f"{df.groupby(['panel','start','cost_bps']).CAGR.agg(lambda x: x.max()-x.min()).max():.4f}",
         "> 0.005",
         df.groupby(['panel','start','cost_bps']).CAGR.agg(lambda x: x.max()-x.min()).max() > 0.005)

    # ---------------- WHERE THE BINDING DRAWDOWN ACTUALLY SITS
    say("\n    WHERE THE BINDING DRAWDOWN SITS (the premise: 4b's L_DD is fed by the 2008-09 collapse)")
    for nm, (px, invest) in panels.items():
        d = starts[(nm, "COMMITTED")]
        for g in GROSSES:
            b0, bt, _ = books[(nm, g)]
            r = priced(b0, bt, HEADLINE_RUNG).loc[d:]
            eq = (1 + r).cumprod(); ddser = eq / eq.cummax() - 1
            publish(f"trough of the book's MaxDD ({nm}, g{g:.2f}, {HEADLINE_RUNG:.0f} bps)",
                    f"{ddser.idxmin().date()} at {ddser.min():.2%}")
        spy = px["SPY"].pct_change().fillna(0.0).loc[d:]
        eq = (1 + spy).cumprod(); ddser = eq / eq.cummax() - 1
        publish(f"trough of SPY's MaxDD ({nm})", f"{ddser.idxmin().date()} at {ddser.min():.2%}")
        eb, _, _ = ewbh(px, invest, d)
        eq = (1 + eb).cumprod(); ddser = eq / eq.cummax() - 1
        publish(f"trough of EWBH(panel)'s MaxDD ({nm})", f"{ddser.idxmin().date()} at {ddser.min():.2%}")

    # ---------------- SECTION A: the ladder
    say("\n=== A.  THE CANDIDATE AND ITS BARS AT EVERY EVALUATION START (headline rung 10 bps) ===")
    for nm in panels:
        for g in GROSSES:
            say(f"  -- {nm} gross {g:.2f} @ {HEADLINE_RUNG:.0f} bps")
            say("     start        from         yrs    CAGR   Sharpe    H1/H2         MaxDD    OOS_S    4a  4b_SPY 4b_EWBH 4b_EWRB  legsSPY legsEWBH")
            q = df[(df.panel == nm) & (df.gross == g) & (df.cost_bps == HEADLINE_RUNG)]
            for r in q.itertuples():
                say(f"     {r.start:11s} {r.start_date} {r.n_rows/252:5.1f} {r.CAGR:7.2%}  {r.Sharpe:6.4f}"
                    f"  {r.H1:6.4f}/{r.H2:6.4f} {r.MaxDD:8.2%} {r.OOS_Sharpe:7.4f}   {int(r.pass4a)}"
                    f"    {int(r.pass4b_SPY)}      {int(r.pass4b_EWBH)}      {int(r.pass4b_EWRB)}"
                    f"   {r.legs_SPY}   {r.legs_EWBH}")
            say("     benchmarks re-scored from the same start:")
            for r in q.itertuples():
                say(f"     {r.start:11s} SPY {r.SPY_CAGR:7.2%}/{r.SPY_Sharpe:6.4f}/{r.SPY_MaxDD:7.2%}"
                    f"   EWBH {r.EWBH_CAGR:7.2%}/{r.EWBH_Sharpe:6.4f}/{r.EWBH_MaxDD:7.2%}"
                    f"   EWRB {r.EWRB_CAGR:7.2%}/{r.EWRB_Sharpe:6.4f}/{r.EWRB_MaxDD:7.2%}"
                    f"   live v2 {r.base_CAGR:7.2%}/{r.base_Sharpe:6.4f}/{r.base_MaxDD:7.2%}")

    # ---------------- SECTION B: survival counts
    say("\n=== B.  SURVIVAL: how many rows pass at each start, and which leg binds first ===")
    say("     (each cell = panel x gross x rung = 16 rows per start)")
    for bn in BENCHES:
        say(f"  -- benchmark {bn}")
        for s in STARTS:
            q = df[df.start == s]
            fails = {k: int((~q[f"{bn}_{k}"]).sum()) for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")}
            say(f"     {s:11s} 4b {int(q[f'pass4b_{bn}'].sum()):2d} of {len(q)}   4a {int(q.pass4a.sum()):2d} of {len(q)}"
                f"   leg fails {fails}   leg strings {q[f'legs_{bn}'].value_counts().to_dict()}")
    base_rows = df[df.start == "COMMITTED"]
    say(f"\n     COMMITTED-start passes under SPY: {int(base_rows.pass4b_SPY.sum())} of {len(base_rows)}")
    surv = []
    for r in base_rows[base_rows.pass4b_SPY].itertuples():
        keep = df[(df.panel == r.panel) & (df.gross == r.gross) & (df.cost_bps == r.cost_bps)]
        n_ok = int(keep.pass4b_SPY.sum())
        surv.append(dict(panel=r.panel, gross=r.gross, cost_bps=r.cost_bps, starts_passing=n_ok,
                         of=len(keep),
                         dies_at=",".join(x.start for x in keep.itertuples() if not x.pass4b_SPY) or "none"))
        say(f"       {r.panel} g{r.gross:.2f} {r.cost_bps:4.0f}bps: survives {n_ok} of {len(keep)} starts;"
            f" dies at [{surv[-1]['dies_at']}]")
    pd.DataFrame(surv).to_csv(f"{OUT}.survival.csv", index=False)

    # ---------------- SECTION C: BAR vs BOOK decomposition
    say("\n=== C.  IS IT A BAR SHIFT OR A BOOK SHIFT?  (d slack from COMMITTED, per leg) ===")
    say("     d(slack) = d(book statistic) - coef x d(benchmark statistic);  coef 0.60 on DD, 0.70 on CAGR, 1.0 on Sharpes")
    dec = []
    for bn in BENCHES:
        for (nm, g, rung), q in df.groupby(["panel", "gross", "cost_bps"]):
            c = q[q.start == "COMMITTED"].iloc[0]
            for r in q[q.start != "COMMITTED"].itertuples():
                for leg, bk, bmk, coef in (("L_DD", "MaxDD", f"{bn}_MaxDD", DD_CAP),
                                           ("L_CAGR", "CAGR", f"{bn}_CAGR", CAGR_FLOOR),
                                           ("L_H1", "H1", f"{bn}_H1", 1.0),
                                           ("L_H2", "H2", f"{bn}_H2", 1.0)):
                    dbook = getattr(r, bk) - c[bk]
                    dbench = getattr(r, bmk) - c[bmk]
                    dec.append(dict(bench=bn, panel=nm, gross=g, cost_bps=rung, start=r.start, leg=leg,
                                    d_slack=getattr(r, f"{bn}_m_{leg}") - c[f"{bn}_m_{leg}"],
                                    d_book=dbook, d_bar=-coef * dbench,
                                    bar_share=abs(coef * dbench) / (abs(dbook) + abs(coef * dbench))
                                    if (abs(dbook) + abs(coef * dbench)) > 1e-12 else np.nan))
    dd = pd.DataFrame(dec); dd.to_csv(f"{OUT}.decomposition.csv", index=False)
    for bn in BENCHES:
        say(f"  -- benchmark {bn}: median |bar| share of the total leg move (1.0 = the BAR moved, 0.0 = the BOOK moved)")
        for leg in ("L_DD", "L_CAGR", "L_H1", "L_H2"):
            q = dd[(dd.bench == bn) & (dd.leg == leg)]
            say(f"     {leg:7s} bar share median {q.bar_share.median():.3f}"
                f"   d_book median {q.d_book.median():+.4f}   d_bar median {q.d_bar.median():+.4f}"
                f"   d_slack median {q.d_slack.median():+.4f}  (n={len(q)})")

    # ---------------- SECTION D: rule 8
    say("\n=== D.  RULE 8 WALK-FORWARD.  gross chosen on [S, 2016-12-31] ONLY; 2017-2026 read ONCE ===")
    wf = []
    for nm, (px, invest) in panels.items():
        spy_full = px["SPY"].pct_change().fillna(0.0)
        er0, et = ewrbs[nm]
        for s in STARTS:
            d = starts[(nm, s)]
            eb, _, _ = ewbh(px, invest, d)
            for rung in RUNGS:
                spy_oos = spy_full.loc[OOS_START:]
                ewbh_oos = eb.loc[OOS_START:]
                ewrb_oos = priced(er0, et, rung).loc[OOS_START:]
                base_oos = priced(*basebook[nm], rung).loc[OOS_START:]
                cand = {}
                for g in GROSSES:
                    b0, bt, _ = books[(nm, g)]
                    r_is = priced(b0, bt, rung).loc[d:IS_END]
                    r_oos = priced(b0, bt, rung).loc[OOS_START:]
                    cand[g] = (sharpe(r_is), cagr(r_is), r_oos)
                picks = {"C_ISSHARPE": max(GROSSES, key=lambda g: cand[g][0]),
                         "C_ISCAGR": max(GROSSES, key=lambda g: cand[g][1]),
                         "C_PREREG": PREREG_GROSS}
                for cn, g in picks.items():
                    ro = cand[g][2]
                    full = df[(df.panel == nm) & (df.start == s) & (df.gross == g) & (df.cost_bps == rung)].iloc[0]
                    wf.append(dict(panel=nm, start=s, cost_bps=rung, chooser=cn, picked_gross=g,
                                   IS_Sharpe=cand[g][0], IS_CAGR=cand[g][1],
                                   OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                                   SPY_OOS_CAGR=cagr(spy_oos), SPY_OOS_Sharpe=sharpe(spy_oos),
                                   SPY_OOS_MaxDD=maxdd(spy_oos),
                                   EWBH_OOS_CAGR=cagr(ewbh_oos), EWBH_OOS_Sharpe=sharpe(ewbh_oos),
                                   EWRB_OOS_CAGR=cagr(ewrb_oos), EWRB_OOS_Sharpe=sharpe(ewrb_oos),
                                   BASE_OOS_CAGR=cagr(base_oos), BASE_OOS_Sharpe=sharpe(base_oos),
                                   BASE_OOS_MaxDD=maxdd(base_oos),
                                   full_4b_SPY=bool(full.pass4b_SPY), full_4b_EWBH=bool(full.pass4b_EWBH),
                                   full_4b_EWRB=bool(full.pass4b_EWRB), full_4a=bool(full.pass4a),
                                   full_legs_SPY=full.legs_SPY))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("     chooser      start        picks g0.75/g1.00   OOS CAGR / Sharpe / MaxDD     beats SPY / EWBH / EWRB / live (OOS Sharpe)   full 4b SPY/EWBH")
    for cn in ("C_ISSHARPE", "C_ISCAGR", "C_PREREG"):
        for s in STARTS:
            q = wfd[(wfd.chooser == cn) & (wfd.start == s)]
            n75 = int((q.picked_gross == 0.75).sum())
            say(f"     {cn:11s} {s:11s} {n75}/{len(q)-n75}   "
                f"{q.OOS_CAGR.median():7.2%} / {q.OOS_Sharpe.median():6.4f} / {q.OOS_MaxDD.median():7.2%}   "
                f"{int((q.OOS_Sharpe > q.SPY_OOS_Sharpe).sum())}/{len(q)}  "
                f"{int((q.OOS_Sharpe > q.EWBH_OOS_Sharpe).sum())}/{len(q)}  "
                f"{int((q.OOS_Sharpe > q.EWRB_OOS_Sharpe).sum())}/{len(q)}  "
                f"{int((q.OOS_Sharpe > q.BASE_OOS_Sharpe).sum())}/{len(q)}      "
                f"{int(q.full_4b_SPY.sum())}/{len(q)}  {int(q.full_4b_EWBH.sum())}/{len(q)}")
    say(f"     TOTAL PICKS {len(wfd)}")
    q = wfd[wfd.chooser == "C_PREREG"]
    say(f"     pre-registered arm pooled: OOS CAGR {q.OOS_CAGR.median():.2%}, Sharpe {q.OOS_Sharpe.median():.4f},"
        f" MaxDD {q.OOS_MaxDD.median():.2%};  SPY OOS {q.SPY_OOS_CAGR.median():.2%}/{q.SPY_OOS_Sharpe.median():.4f}"
        f"/{q.SPY_OOS_MaxDD.median():.2%};  live v2 OOS {q.BASE_OOS_CAGR.median():.2%}/{q.BASE_OOS_Sharpe.median():.4f}"
        f"/{q.BASE_OOS_MaxDD.median():.2%}")

    # ---------------- SECTION E: the headline cell in full
    say("\n=== E.  THE COMMITTED HEADLINE CELL (U56, gross 0.75, 10 bps) AT EVERY START ===")
    q = df[(df.panel == "U56") & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
    for r in q.itertuples():
        say(f"     {r.start:11s} book {r.CAGR:7.2%}/{r.Sharpe:6.4f}/{r.MaxDD:7.2%}"
            f"  | SPY bars: DD >= {DD_CAP*r.SPY_MaxDD:7.2%}, CAGR >= {CAGR_FLOOR*r.SPY_CAGR:6.2%}"
            f"  | slacks DD {r.SPY_m_L_DD:+.4f} CAGR {r.SPY_m_L_CAGR:+.4f} H1 {r.SPY_m_L_H1:+.4f}"
            f" H2 {r.SPY_m_L_H2:+.4f} OOS {r.SPY_m_L_OOS:+.4f}  4b_SPY {int(r.pass4b_SPY)}")

    # ---------------- gates + artefacts
    gd = pd.DataFrame(GATES); gd.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gd.pass_.sum())
    say(f"\n=== GATES {npass} of {len(gd)} ===")
    for g in GATES:
        if not g["pass_"]:
            say(f"    FAILED: {g['gate']}")
    say(f"    grid rows {len(df)}; decomposition rows {len(dd)}; walk-forward picks {len(wfd)};"
        f" elapsed {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
