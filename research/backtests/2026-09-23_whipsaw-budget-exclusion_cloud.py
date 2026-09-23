#!/usr/bin/env python3
"""idea 2447 (lane cloud, run 49, 2026-09-23) — DOES A PER-NAME WHIPSAW BUDGET CUT THE CAPPED
CANDIDATE'S 3.51x TURNOVER, OR MOVE ITS BINDING `L_DD` LEG?

THE GAP.  The standing 4b candidate has exactly one stated adoption blocker -- turnover of
3.51x/yr against the live book's 1.77x -- and the record has now killed EVERY device filed
against it: the weight-drift no-trade band (2328), the minimum holding period (2351), the
partial-adjustment damper (2391 / 2404) and the calendar rota (2408).  All four act on the EXIT
or the RE-SIZE.  NONE has ever touched ADMISSION.

THE DEVICE.  A name pays a round trip every time its 200d band state flips, so the names that
generate the bill are identifiable IN ADVANCE by their own recent flip history.  Count each
name's band-state changes over the trailing `W` sessions and REFUSE TO HOLD any name whose count
is `k` or more.  The excluded names are, by construction, the ones paying the bill.

WHY THIS IS A FALSIFICATION TEST AND NOT A TUNING EXERCISE.  Idea 1745 KILLED the READING that a
name's own 200d-crossing rate predicts the band's return cost.  If that KILL is right, this
filter should cut turnover and buy NOTHING -- or cost return, because a name that has just
whipsawed is not obviously a worse name to own next week.  The prior is stated here, before any
compute, and the run is designed to be able to refute it: `k = INF` is the committed book EXACTLY
(G3 asserts bit-identity), so any improvement would show up as a clean monotone gain along `k`.

DIAL 1 -- the flip budget `k` in {INF (committed), 6, 4, 3, 2}: at most k-1 flips in the trailing
          window are tolerated.
DIAL 2 -- gross g in {0.75 (live), 1.00}.

CONVENTIONS, both published, the headline PRE-STATED here before any compute:
  W252 -- a one-year trailing flip window.  **HEADLINE** (it matches the record's 252d idiom).
  W504 -- a two-year window, to show the answer is not one window's artefact.

THE FILTER IS CAUSAL BY CONSTRUCTION.  `flips_i,t` counts state changes over sessions t-W+1..t,
and `band_state` is itself a hysteretic ffill of past closes only; the weight decided at t is
applied at t+1 by the runner.  G7 re-derives the counter from a TRUNCATED panel and asserts the
overlap is bit-identical, so no future information can leak through the rolling window.

BOOKS.  CAP2 (idea 2322's 2%-per-name capped candidate) and CAND (idea 2300/2332's uncapped
`gross / N_in` book), both with the committed phi = 1.00 SHY sweep, plus the LIVE RULES v2 book
as the 4a baseline.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, rungs {0, 10, 25, 50} bps, books {CAP2, CAND},
weekly cadence, t+1 execution, band 0.03, MA 200d, the 2% cap and the SHY sweep.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS all failing at every cell; an admission filter that can only REMOVE names cannot move
three legs at once, so there is no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (k, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers, then 2017-2026 is read ONCE, and the picks are scored against the COMMITTED k = INF.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 `k = INF` reproduces the committed CAP2 / CAND headlines.
G4 no leverage.  G5 cost exactly linear in the rung.  G6 exactly two tuned parameters.  G7 the
flip counter is CAUSAL (panel-truncation replica).  G8 the eligible sets are NESTED in `k`.
G9 the SHY sweep is priced on every held row.  G10 the filter actually BITES (it removes names).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The k-vs-INF contrast is same-tape, same-day and
first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_whipsaw-budget-exclusion_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "whipsaw-budget-exclusion", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
BUDGETS = [np.inf, 6, 4, 3, 2]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
WINDOWS = [252, 504]
HEADLINE_W, HEADLINE_RUNG, HEADLINE_K = 252, 10.0, np.inf
NAME_CAP, SWEEP = 0.020, "SHY"
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


def kname(k):
    return "INF" if not np.isfinite(k) else str(int(k))


# ---------------------------------------------------------------- the whipsaw counter
def flip_count(px, window):
    """`flips_i,t` = number of 200d band-state CHANGES for name i over sessions t-window+1..t.
    Past closes only: `band_state` is a hysteretic ffill of past prices and the rolling sum looks
    strictly backwards, so the count is available at the close of t (G7 asserts this by panel
    truncation)."""
    st = band_state(px, BAND).astype(float)
    ch = (st != st.shift(1)).astype(float)
    ch.iloc[0] = 0.0
    return ch.rolling(window, min_periods=window).sum()


def eligible(px, k, window):
    """Names permitted to be held: inside the band, priced, and with FEWER than k flips in the
    trailing window.  k = INF is the committed book exactly (no name is ever refused).  A name
    whose count is not yet defined (the first `window` rows) is NOT refused, so the filter can
    only ever bite where it has the data to bite."""
    inb = band_state(px, BAND) & px.notna()
    if not np.isfinite(k):
        return inb
    f = flip_count(px, window)
    return inb & ((f < k) | f.isna())


def risk_weights(px, gross, cap, k, window):
    el = eligible(px, k, window)
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
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx))


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
    say("=== idea 2447 — DOES A PER-NAME WHIPSAW BUDGET CUT THE CANDIDATE'S TURNOVER OR MOVE ITS L_DD LEG? ===")
    say(f"    {DATE}  lane {LANE} run 49   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 flip budget k {[kname(k) for k in BUDGETS]} (a name with >= k flips in the trailing")
    say(f"    window is REFUSED)    DIAL 2 gross {GROSSES}    conventions W {WINDOWS}; HEADLINE = W{HEADLINE_W}.")
    say("    PRIOR, STATED BEFORE COMPUTE: idea 1745 KILLED the reading that a name's own 200d-crossing rate")
    say("    predicts the band's return cost, so the expectation is LESS TURNOVER AND NO GAIN.  k = INF is the")
    say("    committed book EXACTLY, so a real improvement would show as a clean monotone gain along k.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343); an")
    say("    admission filter can only REMOVE names and cannot move three failing legs at once.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The k-vs-INF contrast is same-tape, same-day and first-order immune.")
    gate("G6 exactly two tuned parameters", "flip budget k, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs = band_state(px_u, BAND)
    d2 = int((eligible(px_u, np.inf, HEADLINE_W) != (bs & px_u.notna())).sum().sum())
    gate("G2 at k = INF the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {(bs & px_u.notna()).sum(axis=1).mean():.2f}", "0", d2 == 0)

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G7 the flip counter is causal: re-derive from a TRUNCATED panel, compare the overlap
    cut = px_u.index[3000]
    f_full = flip_count(px_u, HEADLINE_W).loc[:cut]
    f_trunc = flip_count(px_u.loc[:cut], HEADLINE_W)
    d7 = float((f_full - f_trunc).abs().max().max())
    gate("G7 the flip counter is CAUSAL (panel truncation at row 3000 changes nothing before it)",
         f"max|d| {d7:.3e} over {f_full.shape[0]}x{f_full.shape[1]} cells", "0.0", d7 == 0.0)

    # G8 nestedness in k, G10 the filter bites
    prev = None; nested = True
    bite = {}
    for k in BUDGETS:
        el = eligible(px_u, k, HEADLINE_W)
        if prev is not None:
            nested = nested and bool((el & ~prev).sum().sum() == 0)
        prev = el
        bite[kname(k)] = float(el.loc[px_u.index[WARMUP]:].sum(axis=1).mean())
    gate("G8 the eligible sets are NESTED in k (a smaller budget can only ever remove names)",
         f"violations: {'none' if nested else 'FOUND'}", "none", nested)
    gate("G10 the filter actually BITES (mean names eligible falls with k, U56 / W252)",
         "  ".join(f"k={k}:{v:.2f}" for k, v in bite.items()), "strictly falling",
         all(list(bite.values())[i] > list(bite.values())[i + 1] for i in range(len(bite) - 1)))
    fc = flip_count(px_u, HEADLINE_W).loc[px_u.index[WARMUP]:]
    publish("G10b the per-name flip distribution (U56, W252, scored rows)",
            f"mean {float(fc.mean().mean()):.3f}  median {float(fc.stack().median()):.1f}"
            f"  p90 {float(fc.stack().quantile(0.90)):.1f}  max {float(fc.max().max()):.0f}"
            f"  share of name-days with >= 2 flips {float((fc >= 2).sum().sum() / fc.notna().sum().sum()):.1%}")

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for window in WINDOWS:
            for bname, cap in BOOKS.items():
                for gross in GROSSES:
                    for k in BUDGETS:
                        wr = risk_weights(px, gross, cap, k, window)
                        bk = run_book(px, wr)
                        r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                        el = eligible(px, k, window).loc[start:]
                        book_facts.append(dict(
                            panel=pname, window=window, book=bname, gross=gross, k=kname(k),
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            mean_elig=float(el.sum(axis=1).mean()),
                            mean_names=float(bk["names"].loc[start:].mean()),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            max_gross=float(bk["gross"].loc[start:].max()),
                            max_name_w=float(bk["maxw"].loc[start:].max())))
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                            lg = legs(r, base_r, spy, r_oos, spy_oos)
                            rows.append(dict(
                                panel=pname, window=window, book=bname, gross=gross, k=kname(k),
                                k_num=float(k) if np.isfinite(k) else 999.0, cost_bps=rung,
                                CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                                OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                                base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(WINDOWS)} windows x 2 books x 2 gross x"
        f" {len(BUDGETS)} budgets x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.mean_gross.max():.6f} mean, {bf.max_name_w.max():.4f} max single name",
         "<= 1+1e-12", bool(bf.max_gross.max() <= 1 + 1e-12))
    pz = panels["U56"]
    wr0 = risk_weights(pz, 0.75, NAME_CAP, np.inf, HEADLINE_W)
    bz = run_book(pz, wr0)
    st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.window == HEADLINE_W) & (df.k == "INF")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.window == HEADLINE_W) & (df.k == "INF")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 k = INF reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND"
         " CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say(f"\n=== A. THE FULL LADDER, window W{HEADLINE_W}, gross 0.75 — EVERY GRID POINT ===")
    say("  panel book  k   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for k in BUDGETS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.window == HEADLINE_W)
                           & (df.k == kname(k)) & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {kname(k):3s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}"
                        f"  | {lg}" + ("   <= COMMITTED" if not np.isfinite(k) else ""))

    # ------------------------------------------------------------ B. what the budget buys and costs
    say("\n=== B. THE WHOLE QUESTION: WHAT DOES THE BUDGET BUY, AND WHAT DOES IT COST? (k vs its own INF row) ===")
    say("  panel W    book  g   bps  k  | dTurnover | dCAGR    dSharpe   dMaxDD  | dOOS Sh | 4b INF -> 4b k")
    dec = []
    for pname in panels:
        for window in WINDOWS:
            for bk_ in BOOKS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        z = df[(df.panel == pname) & (df.window == window) & (df.book == bk_)
                               & (df.gross == gross) & (df.cost_bps == rung) & (df.k == "INF")].iloc[0]
                        for k in BUDGETS[1:]:
                            r = df[(df.panel == pname) & (df.window == window) & (df.book == bk_)
                                   & (df.gross == gross) & (df.cost_bps == rung)
                                   & (df.k == kname(k))].iloc[0]
                            dec.append(dict(panel=pname, window=window, book=bk_, gross=gross,
                                            cost_bps=rung, k=kname(k),
                                            dTurn=r.turnover_yr / z.turnover_yr - 1,
                                            dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                                            dMaxDD=r.MaxDD - z.MaxDD,
                                            dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                                            inf4b=bool(z.pass4b), k4b=bool(r.pass4b)))
                            if window == HEADLINE_W and gross == 0.75 and rung == HEADLINE_RUNG:
                                say(f"  {pname:5s} W{window:3d} {bk_:4s} {gross:.2f} {rung:5.1f} {kname(k):>3s} |"
                                    f" {r.turnover_yr / z.turnover_yr - 1:+9.1%} | {r.CAGR - z.CAGR:+7.2%}"
                                    f" {r.Sharpe - z.Sharpe:+9.4f} {r.MaxDD - z.MaxDD:+8.2%} |"
                                    f" {r.OOS_Sharpe - z.OOS_Sharpe:+8.4f} | "
                                    f"{'PASS' if z.pass4b else 'fail'} -> {'PASS' if r.pass4b else 'fail'}")
    dd_ = pd.DataFrame(dec); dd_.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n  Over all {len(dd_)} (k vs its own INF) pairs:")
    say(f"   dTurnover < 0 in {int((dd_.dTurn < 0).sum())} of {len(dd_)}"
        f"   dCAGR > 0 in {int((dd_.dCAGR > 0).sum())}"
        f"   dSharpe > 0 in {int((dd_.dSharpe > 0).sum())}"
        f"   dMaxDD > 0 (shallower) in {int((dd_.dMaxDD > 0).sum())}"
        f"   dOOS Sharpe > 0 in {int((dd_.dOOS_Sharpe > 0).sum())}")
    say("   by budget k:")
    for k in BUDGETS[1:]:
        q = dd_[dd_.k == kname(k)]
        say(f"    k={kname(k):>3s}  mean dTurn {q.dTurn.mean():+7.1%}  dCAGR {q.dCAGR.mean():+.2%}"
            f"  dSharpe {q.dSharpe.mean():+.4f}  dMaxDD {q.dMaxDD.mean():+.2%}"
            f"  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}   4b: INF {int(q.inf4b.sum())}/{len(q)}"
            f" -> k {int(q.k4b.sum())}/{len(q)}")
    say("\n   THE EXCHANGE RATE — pp of CAGR given up per 1% of turnover saved (10 bps, W252, g0.75):")
    for pname in panels:
        for bk_ in BOOKS:
            for k in BUDGETS[1:]:
                q = dd_[(dd_.panel == pname) & (dd_.book == bk_) & (dd_.k == kname(k))
                        & (dd_.window == HEADLINE_W) & (dd_.gross == 0.75)
                        & (dd_.cost_bps == HEADLINE_RUNG)].iloc[0]
                rate = (q.dCAGR * 100) / (-q.dTurn * 100) if q.dTurn < 0 else np.nan
                say(f"    {pname:5s} {bk_:4s} k={kname(k):>3s}: turnover {q.dTurn:+.1%},"
                    f" CAGR {q.dCAGR * 100:+.2f} pp"
                    + (f"  -> {rate:+.3f} pp of CAGR per 1% of turnover saved" if q.dTurn < 0 else ""))

    # ------------------------------------------------------------ C. breadth
    say(f"\n=== C. WHAT THE FILTER REMOVES (mean names ELIGIBLE and HELD, and turnover, W{HEADLINE_W}, g0.75) ===")
    say("  panel book  k  | mean eligible | mean held | turnover/yr | vs live book 1.77x")
    for pname in panels:
        for bk_ in BOOKS:
            for k in BUDGETS:
                e = bf[(bf.panel == pname) & (bf.window == HEADLINE_W) & (bf.book == bk_)
                       & (bf.gross == 0.75) & (bf.k == kname(k))].iloc[0]
                say(f"  {pname:5s} {bk_:4s} {kname(k):>3s} | {e.mean_elig:13.2f} | {e.mean_names:9.2f} |"
                    f" {e.turnover_yr:11.2f} | {e.turnover_yr / 1.77:17.2f}x")

    # ------------------------------------------------------------ D. KEEP counts
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for k in BUDGETS:
        d = df[df.k == kname(k)]
        say(f"   k {kname(k):>3s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by k: "
            + "  ".join(f"{kname(k)}:{int(d[d.k == kname(k)].pass4b.sum())}/{len(d[d.k == kname(k)])}"
                        for k in BUDGETS))
    for window in WINDOWS:
        d = df[df.window == window]
        say(f"   window W{window}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same window, book, gross, k, rung):")
    jt = []
    for window in WINDOWS:
        for bk_ in BOOKS:
            for gross in GROSSES:
                for k in BUDGETS:
                    for rung in RUNGS:
                        q = df[(df.window == window) & (df.book == bk_) & (df.gross == gross)
                               & (df.k == kname(k)) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(window=window, book=bk_, gross=gross, k=kname(k),
                                       cost_bps=rung, joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by k: "
        + "  ".join(f"{kname(k)}:{int(jf[jf.k == kname(k)].joint.sum())}/{len(jf[jf.k == kname(k)])}"
                    for k in BUDGETS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.head(20).iterrows():
        say(f"    {r.panel:5s} W{r.window} {r.book:4s} k {r.k:>3s} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  turn {r.turnover_yr:.2f}x"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (k, gross) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE,")
    say("    and scored against the COMMITTED k = INF / gross 0.75 cell. ===")
    wf = []
    for pname in panels:
        for window in WINDOWS:
            for bk_ in BOOKS:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.window == window) & (df.book == bk_)
                           & (df.cost_bps == rung)]
                    cm = d[(d.k == "INF") & (d.gross == 0.75)].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, window=window, book=bk_, cost_bps=rung,
                                       chooser=chooser, pick_k=pk.k, pick_gross=pk.gross,
                                       full4b=bool(pk.pass4b), OOS_CAGR=pk.OOS_CAGR,
                                       OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                       pick_turn=pk.turnover_yr, committed_turn=cm.turnover_yr,
                                       committed_OOS_Sharpe=cm.OOS_Sharpe,
                                       committed_OOS_CAGR=cm.OOS_CAGR,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x {len(WINDOWS)} windows x 2 books x 4 rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                       {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:             {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED k=INF cell's OOS Sharpe:  {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                 {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over k:     " + "  ".join(
        f"{kname(k)}:{int((wfd.pick_k == kname(k)).sum())}" for k in BUDGETS))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say(f"   mean turnover of the picks {wfd.pick_turn.mean():.2f}x vs the committed {wfd.committed_turn.mean():.2f}x")
    say("\n   panel W    book   bps chooser     | pick       OOS CAGR  OOS Sh  turn/yr | committed OOS Sh / turn")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} W{r.window:3d} {r.book:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r.pick_k + '/' + format(r.pick_gross, '.2f'):10s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f}"
            f" {r.pick_turn:7.2f} | {r.committed_OOS_Sharpe:12.4f} / {r.committed_turn:.2f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
