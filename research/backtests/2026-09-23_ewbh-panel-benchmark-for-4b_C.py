#!/usr/bin/env python3
"""idea 2516 (lane C, 2026-09-23) — IS 4b's SPY COMPARAND THE RIGHT BENCHMARK FOR A
SURVIVORSHIP-SELECTED PANEL?

THE QUESTION.  PROTOCOL rule 4b scores every book against SPY: a cap-weighted index of the
POINT-IN-TIME market, rebalanced by the index provider, with no survivorship contamination.
The book itself picks from `research/universe.json` (U56) / `research/universe_broad.json`
(B136) — lists of CURRENT constituents held back to 2008 (rule 9; idea 2435).  The two
comparands therefore differ in TWO ways at once: the RULE (a 200d band gate at gross g with a
SHY sweep, vs buy-and-hold) and the PANEL (a 2026 survivor list, vs the market as it was).

The like-for-like comparand is the EQUAL-WEIGHT BUY-AND-HOLD OF THE BOOK'S OWN PANEL: the
identical names, the identical tape, the identical days, the identical survivorship draw.
Book minus EWBH is the RULE's contribution with the panel's luck differenced out.  Book minus
SPY is that PLUS the panel's luck.  This run measures the difference.

DIAL 1 -- benchmark B in {SPY, EWBH, EWBH_NOSWEEP, EWRB, EWBH_MEGA20}.  SPY is the protocol
          incumbent; EWBH is the pre-stated like-for-like substitute; the other three are
          reported construction sensitivities, never selected on.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (idea 2322's 2% cap), CAND (idea 2300's uncapped
RG100+phi), LIVEV2 (`baseline.rules_v2_weights`, the live book)}, panels {U56, B136}, 4 cost
rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03, t+1 execution, SHY sweep.
3 x 2 x 2 x 4 = 48 book-rows, each re-scored under all 5 benchmarks = 240 published scorings.

WHAT IS DELIVERED (the idea's three asks):
  (1) HOW MANY committed 4b passes survive the SPY -> EWBH substitution (census over the 48
      rows this run reconstructs — NOT over the record's markdown, which this run cannot
      re-price; that limit is stated in the log rather than hidden).
  (2) WHICH LEG BINDS FIRST under each benchmark (leg-failure census + slack ranking).
  (3) HOW LARGE the SPY-minus-EWBH BENCHMARK GAP itself is, per panel, full / H1 / H2 / OOS.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
— benchmark-independent, reported once — and 4b under each benchmark in turn.
RULE 8: (book, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), 2017-2026 then read ONCE, and the OOS 4b verdict taken under every
benchmark.  The chooser never sees a benchmark, so any change in the rule-8 verdict is the
BENCHMARK moving, not the pick.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ewbh-panel-benchmark-for-4b_C.py
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

DATE, SLUG, LANE = "2026-09-23", "ewbh-panel-benchmark-for-4b", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF", "LIVEV2": None}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BENCHES = ["SPY", "EWBH", "EWBH_NOSWEEP", "EWRB", "EWBH_MEGA20"]
PRIMARY_BENCH = "EWBH"
MEGA20 = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "BRK-B", "JPM",
          "LLY", "UNH", "V", "XOM", "COST", "NFLX", "AMD", "CRM", "ORCL", "PLTR"]

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
def cagr(r):
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


# ---------------------------------------------------------------- the books
def cap_weights(px, invest, cap, gross):
    """idea 2322's CAP2 / idea 2300's CAND: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- BAND; idle NAV swept to SHY (phi = 1.00).  cap='INF' is the uncapped candidate."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = gross / nin
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=q.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def book_weights(px, invest, book, gross):
    if book == "LIVEV2":
        return rules_v2_weights(px[invest], band=BAND, gross=gross).reindex(columns=px.columns).fillna(0.0)
    return cap_weights(px, invest, BOOKS[book], gross)


def run_zero(px, w):
    """One cost-free pass; every rung is then priced from (gross returns, turnover)."""
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"]


def priced(r0, turn, bps):
    return r0 - turn * bps / 1e4


# ---------------------------------------------------------------- the benchmarks
def ewbh(px, cols, start):
    """EQUAL-WEIGHT BUY-AND-HOLD: 1/N of NAV into every name PRICED on the last warm-up close,
    then never traded again (weights drift with prices).  Zero cost, fully invested — exactly
    the convention PROTOCOL 4b already uses for its SPY comparand, including the return ON the
    first scored day (gate G3 reproduces `px['SPY'].pct_change()` to float precision).  Names
    that IPO after the purchase are NOT bought (a real buy-and-hold cannot buy them)."""
    pos = px.index.get_loc(start)
    q = px[cols].iloc[pos - 1:]
    live = q.iloc[0].notna()
    q = q.loc[:, live]
    val = (q / q.iloc[0]).mean(axis=1)
    return val.pct_change().dropna(), int(live.sum()), int((~live).sum())


def ewrb(px, cols, bps):
    """EQUAL-WEIGHT, WEEKLY-REBALANCED across the names priced that day, charged at the SAME
    cost rung as the book it is scored against — the tradable twin of EWBH."""
    e = pd.DataFrame(1.0, index=px.index, columns=cols).where(px[cols].notna(), 0.0)
    w = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return res["returns"], res["turnover"]


# ---------------------------------------------------------------- the KEEP paths
def legs_4b(r, b):
    """4b under benchmark b: Sharpe > b in BOTH halves AND out of sample, MaxDD >= 0.60 x b's,
    CAGR >= 0.70 x b's.  Slacks are returned so 'which leg binds first' is measured, not
    guessed."""
    r1, r2 = halves(r); b1, b2 = halves(b)
    ro, bo = r.loc[OOS_START:], b.loc[OOS_START:]
    m = dict(
        L_H1=sharpe(r1) - sharpe(b1),
        L_H2=sharpe(r2) - sharpe(b2),
        L_OOS=sharpe(ro) - sharpe(bo),
        L_DD=maxdd(r) - DD_CAP * maxdd(b),
        L_CAGR=cagr(r) - CAGR_FLOOR * cagr(b),
    )
    ok = {k: bool(v > 0) for k, v in m.items()}
    return dict(pass4b=all(ok.values()), **{k: ok[k] for k in m}, **{f"m_{k}": float(v) for k, v in m.items()})


def pass_4a(r, base):
    r1, r2 = halves(r); b1, b2 = halves(base)
    return bool(sharpe(r1) > sharpe(b1) and sharpe(r2) > sharpe(b2) and maxdd(r) >= maxdd(base))


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2516 (lane C, run 66) — is 4b's SPY comparand the right benchmark for a survivorship-selected panel? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 benchmark {BENCHES} (primary substitute {PRIMARY_BENCH})   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}")
    gate("G10 exactly two tuned parameters", "benchmark, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        win = px.index[WARMUP:]
        panels[nm] = (px, invest, win)
        yrs = (px.index[-1] - win[0]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows, scored from {win[0].date()}",
             ">= 10y", yrs >= 10)
        gate(f"G1 sweep {SWEEP} priced on every scored row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G2 all-NaN columns in {nm} (idea 2332's defect, carried forward)", f"{len(dead)}: {dead}")

    # ---- G3: the EWBH machinery on a single column IS that column's buy-and-hold
    px_u, inv_u, win_u = panels["U56"]
    e1, n1, _ = ewbh(px_u, ["SPY"], win_u[0])
    d3 = float((e1 - px_u["SPY"].pct_change().fillna(0.0).loc[win_u[0]:]).abs().max())
    gate("G3 ewbh(['SPY']) == SPY buy-and-hold", f"max|d| {d3:.3e} over {n1} name", "< 1e-15", d3 < 1e-15)

    # ---------------------------------------------------------------- benchmarks per panel
    B = {}
    for pname, (px, invest, win) in panels.items():
        start = win[0]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        b_all, n_all, miss_all = ewbh(px, invest, start)
        nosw = [c for c in invest if c != SWEEP]
        b_nos, n_nos, _ = ewbh(px, nosw, start)
        mega = [c for c in MEGA20 if c in invest]
        b_meg, n_meg, miss_meg = ewbh(px, mega, start)
        r0_rb, tu_rb = ewrb(px, invest, 0.0)
        B[pname] = dict(SPY=lambda bps, s=spy: s,
                        EWBH=lambda bps, s=b_all.loc[win]: s,
                        EWBH_NOSWEEP=lambda bps, s=b_nos.loc[win]: s,
                        EWRB=lambda bps, r=r0_rb, t=tu_rb, w=win: priced(r, t, bps).loc[w],
                        EWBH_MEGA20=lambda bps, s=b_meg.loc[win]: s)
        publish(f"G4 EWBH cohort ({pname})",
                f"EWBH {n_all} of {len(invest)} names bought at {start.date()} ({miss_all} not yet priced); "
                f"EWBH_NOSWEEP {n_nos}; EWBH_MEGA20 {n_meg} of {len(mega)} ({miss_meg} not yet priced); "
                f"EWRB turnover {float(tu_rb.loc[win].sum()/(len(win)/252)):.2f}x/yr")
        for bn in BENCHES:
            s = B[pname][bn](HEADLINE_RUNG)
            so, s1, s2 = s.loc[OOS_START:], *halves(s)
            say(f"    BENCH {pname:5s} {bn:13s} CAGR {cagr(s):7.2%}  Sharpe {sharpe(s):7.4f}  "
                f"MaxDD {maxdd(s):7.2%}  H1/H2 {sharpe(s1):.4f}/{sharpe(s2):.4f}  OOS {cagr(so):7.2%}/{sharpe(so):.4f}/{maxdd(so):7.2%}")

    # ---------------------------------------------------------------- the grid
    rows, bench_rows = [], []
    for pname, (px, invest, win) in panels.items():
        yrs = len(win) / 252
        base_r0, base_tu = run_zero(px, book_weights(px, invest, "LIVEV2", 0.75))
        base_r = priced(base_r0, base_tu, HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} cols)  live RULES v2 @10bps "
            f"{cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for book in BOOKS:
            for gross in GROSSES:
                r0, tu = run_zero(px, book_weights(px, invest, book, gross))
                for bps in RUNGS:
                    r = priced(r0, tu, bps).loc[win]
                    row = dict(panel=pname, book=book, gross=gross, bps=bps,
                               CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                               H1=sharpe(halves(r)[0]), H2=sharpe(halves(r)[1]),
                               OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                               OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                               turnover_yr=float(tu.loc[win].sum() / yrs),
                               pass4a=pass_4a(r, base_r))
                    for bn in BENCHES:
                        L = legs_4b(r, B[pname][bn](bps))
                        for k, v in L.items():
                            row[f"{bn}:{k}"] = v
                    rows.append(row)
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    say(f"\n[grid] {len(G)} book-rows x {len(BENCHES)} benchmarks = {len(G)*len(BENCHES)} published scorings")

    # ---- G5 / G6: the committed headlines
    c = G[(G.panel == "U56") & (G.book == "CAP2") & (G.gross == 0.75) & (G.bps == 10.0)].iloc[0]
    d5 = max(abs(c.CAGR - 0.1162), abs(c.Sharpe - 1.2687), abs(c.MaxDD + 0.1481))
    gate("G5 committed CAP2 U56 g0.75 @10bps headline (11.62% / 1.2687 / -14.81%)",
         f"{c.CAGR:.2%} / {c.Sharpe:.4f} / {c.MaxDD:.2%}, max|d| {d5:.2e}", "< 5e-4", d5 < 5e-4)
    gate("G6 the standing candidate still passes 4b under SPY", f"{bool(c['SPY:pass4b'])}", "True",
         bool(c["SPY:pass4b"]))
    lv = G[(G.panel == "U56") & (G.book == "LIVEV2") & (G.gross == 0.75) & (G.bps == 10.0)].iloc[0]
    publish("G7 live RULES v2 comparand (U56 g0.75 @10bps)",
            f"{lv.CAGR:.2%} / {lv.Sharpe:.4f} / {lv.MaxDD:.2%}, OOS {lv.OOS_CAGR:.2%} / {lv.OOS_Sharpe:.4f}")

    # ---- the exposure asymmetry is UNCHANGED by the substitution, and that is stated, not buried
    for pname, (px, invest, win) in panels.items():
        for book in ("CAP2", "LIVEV2"):
            w = book_weights(px, invest, book, 0.75)
            risk = w.drop(columns=[SWEEP]).sum(axis=1).loc[win]
            publish(f"G8 mean invested RISK gross, {book} g0.75 ({pname})",
                    f"{risk.mean():.4f} (SHY sleeve {w[SWEEP].loc[win].mean():.4f}) vs EVERY benchmark here at 1.00 "
                    f"— SPY and EWBH carry the SAME exposure asymmetry, so the substitution moves the PANEL only")

    # ================================================================ ASK 3: the benchmark gap
    say("\n=== ASK 3 — HOW BIG IS THE SPY-minus-EWBH BENCHMARK GAP ITSELF? ===")
    for pname in panels:
        spy = B[pname]["SPY"](HEADLINE_RUNG)
        for bn in BENCHES[1:]:
            s = B[pname][bn](HEADLINE_RUNG)
            r1s, r2s = halves(spy); r1b, r2b = halves(s)
            bench_rows.append(dict(panel=pname, bench=bn,
                                   dCAGR=cagr(spy) - cagr(s), dSharpe=sharpe(spy) - sharpe(s),
                                   dMaxDD=maxdd(spy) - maxdd(s),
                                   dH1=sharpe(r1s) - sharpe(r1b), dH2=sharpe(r2s) - sharpe(r2b),
                                   dOOS=sharpe(spy.loc[OOS_START:]) - sharpe(s.loc[OOS_START:]),
                                   dOOS_CAGR=cagr(spy.loc[OOS_START:]) - cagr(s.loc[OOS_START:]),
                                   DD_cap_SPY=DD_CAP * maxdd(spy), DD_cap_alt=DD_CAP * maxdd(s),
                                   CAGR_floor_SPY=CAGR_FLOOR * cagr(spy), CAGR_floor_alt=CAGR_FLOOR * cagr(s)))
            say(f"    SPY - {bn:13s} ({pname:5s})  dCAGR {bench_rows[-1]['dCAGR']:+7.2%}  "
                f"dSharpe {bench_rows[-1]['dSharpe']:+7.4f}  dMaxDD {bench_rows[-1]['dMaxDD']:+7.2%}  "
                f"dH1 {bench_rows[-1]['dH1']:+.4f}  dH2 {bench_rows[-1]['dH2']:+.4f}  dOOS {bench_rows[-1]['dOOS']:+.4f}  "
                f"| 4b bars: DD cap {bench_rows[-1]['DD_cap_SPY']:.2%} -> {bench_rows[-1]['DD_cap_alt']:.2%}, "
                f"CAGR floor {bench_rows[-1]['CAGR_floor_SPY']:.2%} -> {bench_rows[-1]['CAGR_floor_alt']:.2%}")
    pd.DataFrame(bench_rows).to_csv(f"{OUT}.benchgap.csv", index=False)

    # ================================================================ ASK 1: does the pass survive?
    say("\n=== ASK 1 — HOW MANY 4b PASSES SURVIVE THE SPY -> EWBH SUBSTITUTION? ===")
    say(f"    SCOPE, stated not hidden: the census runs over the {len(G)} book-rows THIS RUN reconstructs")
    say("    (CAP2 / CAND / LIVEV2 x 2 panels x 2 gross x 4 rungs), which is the standing candidate")
    say("    family itself.  The record's other committed 4b passes live in other scripts' books and")
    say("    are NOT re-priced here; no claim is made about them.")
    surv = []
    for bn in BENCHES:
        n = int(G[f"{bn}:pass4b"].sum())
        say(f"    4b PASSES under {bn:13s}: {n:3d} of {len(G)}")
    keep = G["SPY:pass4b"]
    for bn in BENCHES[1:]:
        both = int((keep & G[f"{bn}:pass4b"]).sum())
        lost = int((keep & ~G[f"{bn}:pass4b"]).sum())
        gained = int((~keep & G[f"{bn}:pass4b"]).sum())
        surv.append(dict(bench=bn, spy_pass=int(keep.sum()), survive=both, lost=lost, gained=gained,
                         survival_rate=both / max(int(keep.sum()), 1)))
        say(f"    SPY-pass -> {bn:13s}: SURVIVE {both} of {int(keep.sum())} "
            f"({both/max(int(keep.sum()),1):.1%}), LOST {lost}, NEWLY GAINED {gained}")
    pd.DataFrame(surv).to_csv(f"{OUT}.survival.csv", index=False)

    say("\n    per-cell census on the PRIMARY substitute (SPY -> EWBH), all 48 rows:")
    say("    panel book   g    bps | SPY 4b | EWBH 4b | legs failing under EWBH")
    for _, r in G.iterrows():
        f = [k for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not r[f"{PRIMARY_BENCH}:{k}"]]
        say(f"    {r.panel:5s} {r.book:6s} {r.gross:.2f} {r.bps:5.1f} | "
            f"{'PASS' if r['SPY:pass4b'] else '    ':4s}   | {'PASS' if r[f'{PRIMARY_BENCH}:pass4b'] else '    ':4s}    | "
            f"{','.join(f) if f else '-'}")

    # ================================================================ ASK 2: which leg binds first
    say("\n=== ASK 2 — WHICH LEG BINDS FIRST UNDER EACH BENCHMARK? ===")
    leg_rows = []
    for bn in BENCHES:
        fails = {k: int((~G[f"{bn}:{k}"]).sum()) for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")}
        # binding leg = the failing leg with the SMALLEST |slack| among failures of each row
        binders = []
        for _, r in G.iterrows():
            f = [(k, r[f"{bn}:m_{k}"]) for k in fails if not r[f"{bn}:{k}"]]
            if f:
                binders.append(min(f, key=lambda kv: -kv[1])[0])   # least negative slack = first to bind
        bc = pd.Series(binders).value_counts().to_dict() if binders else {}
        leg_rows.append(dict(bench=bn, n_fail_rows=len(binders), **{f"fail_{k}": v for k, v in fails.items()},
                             **{f"binds_{k}": bc.get(k, 0) for k in fails}))
        say(f"    {bn:13s} rows failing 4b {len(binders):3d}  | leg failures {fails}  | FIRST-BINDING leg {bc}")
        med = {k: float(G[f"{bn}:m_{k}"].median()) for k in fails}
        say(f"    {'':13s} median slack per leg (positive = clears): "
            + "  ".join(f"{k} {v:+.4f}" for k, v in med.items()))
    pd.DataFrame(leg_rows).to_csv(f"{OUT}.legs.csv", index=False)

    # ================================================================ RULE 8
    say("\n=== RULE 8 WALK-FORWARD — (book, gross) fitted on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest, win) in panels.items():
        cache = {}
        for book in BOOKS:
            for gross in GROSSES:
                r0, tu = run_zero(px, book_weights(px, invest, book, gross))
                cache[(book, gross)] = (r0, tu)
        base_r0, base_tu = cache[("LIVEV2", 0.75)]
        for bps in RUNGS:
            base_r = priced(base_r0, base_tu, bps).loc[win]
            base_oos = base_r.loc[OOS_START:]
            cands = {}
            for k, (r0, tu) in cache.items():
                r = priced(r0, tu, bps).loc[win]
                cands[k] = (r.loc[:IS_END], r.loc[OOS_START:])
            picks = {
                "C_ISSHARPE": max(cands, key=lambda k: sharpe(cands[k][0])),
                "C_ISCALMAR": max(cands, key=lambda k: cagr(cands[k][0]) / abs(maxdd(cands[k][0]))),
            }
            for ch, pk in picks.items():
                ro = cands[pk][1]
                rec = dict(panel=pname, bps=bps, chooser=ch, pick_book=pk[0], pick_gross=pk[1],
                           IS_Sharpe=sharpe(cands[pk][0]),
                           OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                           base_OOS_CAGR=cagr(base_oos), base_OOS_Sharpe=sharpe(base_oos),
                           base_OOS_MaxDD=maxdd(base_oos))
                for bn in BENCHES:
                    b = B[pname][bn](bps)
                    bo = b.loc[OOS_START:]
                    rec[f"{bn}:OOS_Sharpe"] = sharpe(bo)
                    rec[f"{bn}:OOS_CAGR"] = cagr(bo)
                    rec[f"{bn}:OOS_MaxDD"] = maxdd(bo)
                    rec[f"{bn}:beats_OOS_Sharpe"] = bool(sharpe(ro) > sharpe(bo))
                    # OOS-only 4b legs (level bars read on the OOS window itself)
                    rec[f"{bn}:OOS_4b"] = bool(sharpe(ro) > sharpe(bo) and maxdd(ro) > DD_CAP * maxdd(bo)
                                               and cagr(ro) > CAGR_FLOOR * cagr(bo))
                    rec[f"{bn}:FULL_4b"] = bool(G[(G.panel == pname) & (G.book == pk[0]) &
                                                  (G.gross == pk[1]) & (G.bps == bps)].iloc[0][f"{bn}:pass4b"])
                wf.append(rec)
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"    {len(W)} picks (2 panels x 4 rungs x 2 choosers)")
    say(f"    picks: book {W.pick_book.value_counts().to_dict()}   gross {W.pick_gross.value_counts().to_dict()}")
    say("    THE PICK NEVER SEES A BENCHMARK, so any verdict change below is the BENCHMARK moving, not the pick.")
    for bn in BENCHES:
        say(f"    {bn:13s}: picks beating its OOS Sharpe {int(W[f'{bn}:beats_OOS_Sharpe'].sum()):2d} of {len(W)}   "
            f"OOS-window 4b {int(W[f'{bn}:OOS_4b'].sum()):2d} of {len(W)}   "
            f"full-sample 4b of the picked cell {int(W[f'{bn}:FULL_4b'].sum()):2d} of {len(W)}")
    say(f"    picks beating the LIVE book's OOS Sharpe: {int((W.OOS_Sharpe > W.base_OOS_Sharpe).sum())} of {len(W)}")
    for _, r in W.iterrows():
        say(f"    WF {r.panel:5s} {r.bps:5.1f}bps {r.chooser:11s} -> {r.pick_book:6s} g{r.pick_gross:.2f} | "
            f"OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%} | "
            f"live v2 OOS {r.base_OOS_CAGR:7.2%} / {r.base_OOS_Sharpe:.4f} / {r.base_OOS_MaxDD:7.2%} | "
            f"SPY OOS {r['SPY:OOS_CAGR']:7.2%} / {r['SPY:OOS_Sharpe']:.4f} / {r['SPY:OOS_MaxDD']:7.2%} | "
            f"EWBH OOS {r['EWBH:OOS_CAGR']:7.2%} / {r['EWBH:OOS_Sharpe']:.4f} / {r['EWBH:OOS_MaxDD']:7.2%} | "
            f"4b SPY {'Y' if r['SPY:OOS_4b'] else 'n'} EWBH {'Y' if r['EWBH:OOS_4b'] else 'n'}")

    # ================================================================ 4a
    deg = G[G.pass4a & (G.book == "LIVEV2") & (G.gross == 0.75) & (G.bps < HEADLINE_RUNG)]
    say(f"\n=== PATH 4a (benchmark-independent, vs live RULES v2 @10bps): {int(G.pass4a.sum())} of {len(G)} rows ===")
    say(f"    and {len(deg)} of those {int(G.pass4a.sum())} are DEGENERATE — the live book itself priced at a")
    say("    CHEAPER rung than its own comparand, which is not a pass.  Genuine 4a: "
        f"{int(G.pass4a.sum()) - len(deg)} of {len(G)}.")

    # the headline cell's leg-by-leg slack, for the record
    c2 = G[(G.panel == "U56") & (G.book == "CAP2") & (G.gross == 0.75) & (G.bps == 10.0)].iloc[0]
    for bn in BENCHES:
        say(f"    HEADLINE U56 CAP2 g0.75 @10bps under {bn:13s}: 4b {'PASS' if c2[f'{bn}:pass4b'] else 'FAIL'}  slacks "
            + "  ".join(f"{k} {float(c2[f'{bn}:m_{k}']):+.4f}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))

    # ---------------------------------------------------------------- close
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say(f"\n[gates] {npass} of {len(GATES)} pass/publish   [runtime] {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
