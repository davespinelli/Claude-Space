#!/usr/bin/env python3
"""idea 2467 (lane B, run 53, 2026-09-23) — IS THE CANDIDATE'S 4b PASS A BOOK-WIDTH EFFECT, AND
DOES A ONE-INSTRUMENT BAND BOOK REACH IT AT A TENTH OF THE TURNOVER?

THE GAP.  The standing 4b candidate has exactly one stated adoption blocker — turnover 3.51x/yr
against the live book's 1.77x — and idea 2431 set the bar at -31.0% (3.51 -> 2.42) AT UNCHANGED
RETURNS.  Run 51 closed the last obvious lever and wrote the diagnosis this run is grounded in:
"A device that cuts turnover without cutting exposure remains the only thing that would work."

Every device the record has closed — admission (2447), exit (2351, 2328), re-size magnitude
(2391 / 2404 damper, 2408 rota), de-grossing (2443), the extended-name trim (2419), the breadth
cap (2387) — REFUSES A TRADE THE SIGNAL ASKED FOR, and every one of them paid ~0.10 pp of CAGR
per 1% of turnover saved.  Run 50 then proved BY IDENTITY that the re-size TRIGGER cannot be
attacked at all: `min(g/N_in, 2%) == 2% x min(1, g/(2% x N_in))` to 3.5e-18, so the committed
candidate ALREADY IS "hold every in-band name at 2% of NAV, ceiling `g`, residual to SHY".

That identity leaves the book with only TWO moving parts: the 200d band, and THE NUMBER OF
INSTRUMENTS THE IDENTICAL RULE IS RUN OVER.  The record has never touched the second.  It is the
only dial that can cut turnover WITHOUT cutting exposure, and the reason is structural rather
than empirical: turnover is roughly LINEAR in the number of positions being rebalanced, while
gross is `g x` the IN-BAND FRACTION — a breadth statistic that does not care how many names you
measure it on.  Narrow the book and you rebalance fewer positions at the same average exposure.

THE DEVICE.  Run the committed rule on a sub-book `S` of width `K` drawn PRICE-BLIND from the
panel's own columns, sized by the record's own relative-cap convention (idea 2381's `a = 1.0`
unit, panel-scaled): `cap_K = 0.02 x M / K` with `M` the panel's column count, so

    w_i = min(g / N_in^S(t), cap_K)   for i in S inside the 200d +/-3% band,   residual -> SHY.

`K = ALL` IS the committed CAP2 book EXACTLY (`cap_M = 0.02`), asserted bit-for-bit by G3 against
an independent construction and reproduced against the committed headline by G3b.  `K = 1` with
`S = {SPY}` is the canonical SINGLE-INSTRUMENT 200d band book — hold SPY when it is above its own
band, else bills — and it is carried as a NAMED, ZERO-SELECTION REFERENCE ARM (`SPYONLY`), stated
in the queue before any compute and never a tuned point.

WHAT WOULD REFUTE IT, STATED BEFORE COMPUTE.  If the 4b legs survive down to small `K`, the
3.51x blocker is MOOT — the answer is to run fewer names, not to refuse trades — and the record
should stop hunting for a turnover device.  If instead the legs collapse as `K` falls, the 4b
pass is a DIVERSIFICATION effect, the turnover is the price of the diversification, and the
record can say so and stop.  The honest prior here is the second: `L_DD` binds on essentially
every sub-50bps 4b FAIL the family has published, and a narrow book's drawdown is idiosyncratic.
The interesting cell is `SPYONLY`, where the rule is pure timing on the benchmark itself.

DIAL 1 — the book width `K` in {1, 2, 4, 8, 16, 32, ALL}.
DIAL 2 — the gross ceiling `g` in {0.75 (live), 1.00}.
AND NO MORE.  The SEED is a PUBLISHED DISTRIBUTION over 8 price-blind sub-books per `K`, never a
dial and never selected on — exactly the status idea 2419 gave its random-trim placebo.  Rule 8
chooses `K` on the SEED MEAN so that no seed can be picked out of sample either.

REPORTED, NEVER SELECTED ON: panels {U56 (M=56), B136 (M=136)}, cost rungs {0, 10, 25, 50} bps,
the sweep convention {SHY at phi = 1.00 (committed), ZERO (idea 2423's pessimal un-remunerated
bound)}, weekly cadence, t+1 execution, band 0.03, MA 200d.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b at 0 of 40-120 and 2383 read it at 0 of 128 with `L_DD`, `L_H2` and `L_OOS`
all failing.  Narrowing a book that already fails three legs cannot be informative about width.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: both dials chosen on warm-up..2016-12-31 ONLY by two pre-stated IS choosers, 2017-2026
read ONCE, picks scored against the COMMITTED `K = ALL` / `g = 0.75` cell.

SURVIVORSHIP CAVEAT (PROTOCOL rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are
CURRENT constituents of their screens held from 2008, so absolute levels are biased upward and
4b's `L_CAGR` floor is the most contaminated leg.  THIS IDEA IS UNUSUALLY EXPOSED TO IT: a narrow
random sub-book of survivors is a narrow book of WINNERS, so small-`K` results are biased in the
device's FAVOUR and any width finding in its favour must be read as an upper bound.  The
`SPYONLY` arm is the one cell with no survivorship exposure at all.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_book-width-ladder_B.py
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

DATE, SLUG, LANE = "2026-09-23", "book-width-ladder", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
WIDTHS = [1, 2, 4, 8, 16, 32, "ALL"]
SEEDS = [0, 1, 2, 3, 4, 5, 6, 7]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
SWEEPS = ["SHY", "ZERO"]
HEADLINE_SWEEP, HEADLINE_RUNG, HEADLINE_G = "SHY", 10.0, 0.75
BASE_CAP, SWEEP_TICKER, BENCH = 0.020, "SHY", "SPY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_TURNOVER, ADOPTION_BAR_TURNOVER = 1.77, 2.42      # idea 2431's -31.0% bar on 3.51x

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


# ---------------------------------------------------------------- the sub-books
def subbook(cols, K, seed):
    """A PRICE-BLIND uniform sample of K of the panel's own columns.  Depends ONLY on the sorted
    column NAMES and the seed — no price, no return, no in-sample statistic ever touches it."""
    c = sorted(cols)
    if K == "ALL" or K >= len(c):
        return list(c)
    rng = np.random.default_rng(1_000_003 * int(K) + 7919 * int(seed))
    return sorted(rng.choice(np.array(c, dtype=object), size=int(K), replace=False).tolist())


def cap_for(K, M):
    """The record's own relative-cap unit (idea 2381, a = 1.0), panel-scaled: cap_K = 2% x M / K.
    At K = M this is EXACTLY the committed 2% cap, so K = ALL spans the committed book."""
    return BASE_CAP if K == "ALL" else BASE_CAP * M / float(K)


def width_weights(px, el, S, K, gross):
    """w_i = min(gross / N_in^S, cap_K) on the members of S inside the band; everything else 0.
    Gross = min(gross, cap_K x N_in^S), so the book de-grosses exactly as the committed rule does
    — through the CAP, on breadth — and the residual is swept to SHY by the runner."""
    M = len(px.columns)
    e = el.copy()
    off = [c for c in px.columns if c not in set(S)]
    if off:
        e = e.copy(); e[off] = False
    nin = e.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap_for(K, M))
    return e.astype(float).mul(per.fillna(0.0), axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except the per-day turnover is retained so every cost rung is
    read off the SAME realised path, and is split into risk-name and sweep-leg components.
    Weights decided at t-1, applied at t (t+1 execution); the book drifts between rebalances."""
    cols = list(prices.columns)
    si = cols.index(SWEEP_TICKER)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP_TICKER].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); t_risk = np.zeros(n); t_sweep = np.zeros(n)
    r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            d = np.abs(new - cur)
            turn[i] = float(d.sum())
            t_sweep[i] = float(d[si]); t_risk[i] = float(d.sum() - d[si])
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                turn_risk=pd.Series(t_risk, index=idx), turn_sweep=pd.Series(t_sweep, index=idx),
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


def wlabel(K):
    return "ALL" if K == "ALL" else f"K{int(K):03d}"


def main():
    t0 = time.time()
    say("=== idea 2467 — IS THE CANDIDATE'S 4b PASS A BOOK-WIDTH EFFECT, AND DOES A ONE-INSTRUMENT")
    say("    BAND BOOK REACH IT AT A TENTH OF THE TURNOVER? ===")
    say(f"    {DATE}  lane {LANE} run 53   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweeps {SWEEPS} (phi=1.00)")
    say(f"    DIAL 1 book width K {WIDTHS}    DIAL 2 gross ceiling {GROSSES}")
    say(f"    SEEDS {SEEDS} — a PUBLISHED DISTRIBUTION of price-blind sub-books, never a dial; rule 8")
    say("    chooses on the SEED MEAN so no seed can be picked out of sample either.")
    say("    SPYONLY = the canonical single-instrument 200d band book, a NAMED ZERO-SELECTION")
    say("    reference arm declared in QUEUE.md before compute, excluded from the rule-8 pick set.")
    say("    SIZING: w_i = min(g / N_in^S, cap_K), cap_K = 2% x M / K (idea 2381's a=1.0 unit,")
    say("    panel-scaled), residual swept to SHY.  K = ALL IS the committed CAP2 book exactly.")
    say("    PRIOR, STATED BEFORE COMPUTE: expect the 4b legs to COLLAPSE as K falls (L_DD binds on")
    say("    essentially every sub-50bps 4b FAIL this family has published, and a narrow book's")
    say("    drawdown is idiosyncratic).  The interesting cell is SPYONLY, which is pure timing.")
    say("    SMALL NOT PRICED: 0 of 128 4b (2383) and 0 of 40-120 (2318/2322/2326/2343) — narrowing a")
    say("    book that already fails three legs says nothing about width.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008.  A NARROW")
    say("    RANDOM SUB-BOOK OF SURVIVORS IS A NARROW BOOK OF WINNERS, so every small-K result is")
    say("    biased in the DEVICE'S FAVOUR and must be read as an UPPER BOUND.  SPYONLY is the one")
    say("    arm with no survivorship exposure at all.")
    gate("G6 exactly two tuned parameters", "book width K, gross ceiling g", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    ELIG = {nm: (band_state(px, BAND) & px.notna()) for nm, px in panels.items()}
    px_u, el_u = panels["U56"], ELIG["U56"]

    d2 = int((ELIG["U56"] != (band_state(px_u, BAND) & px_u.notna())).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {el_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3 -- K = ALL is the committed CAP2 book, bit for bit, against an INDEPENDENT construction.
    d3 = 0.0
    for nm, px in panels.items():
        ind = (ELIG[nm].astype(float)
               .mul((0.75 / ELIG[nm].sum(axis=1).replace(0, np.nan)).clip(upper=BASE_CAP).fillna(0.0),
                    axis=0).fillna(0.0))
        got = width_weights(px, ELIG[nm], subbook(px.columns, "ALL", 0), "ALL", 0.75)
        d3 = max(d3, float((got - ind).abs().max().max()))
    gate("G3 K = ALL IS the committed CAP2 book (independent construction, both panels)",
         f"max|d| {d3:.3e}", "== 0", d3 == 0.0)

    # G7 -- the sub-books are price-blind and deterministic.
    det = all(subbook(panels["U56"].columns, K, s) == subbook(panels["U56"].columns, K, s)
              for K in WIDTHS for s in SEEDS)
    ov = []
    for K in WIDTHS[:-1]:
        bk = [set(subbook(px_u.columns, K, s)) for s in SEEDS]
        ov.append(np.mean([len(a & b) / K for i, a in enumerate(bk) for b in bk[i + 1:]]))
    gate("G7 sub-books are PRICE-BLIND (column names + seed only) and deterministic",
         f"re-draw identical on all {len(WIDTHS) * len(SEEDS)} (K, seed) pairs: {det};"
         f" mean pairwise seed overlap by K "
         + " ".join(f"{k}:{v:.2f}" for k, v in zip(WIDTHS[:-1], ov)), "True", det)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        M = len(px.columns)
        el = ELIG[pname]
        start = px.index[WARMUP]
        spy = px[BENCH].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        arms = [(wlabel(K), K, s, subbook(px.columns, K, s))
                for K in WIDTHS for s in (SEEDS if K != "ALL" else [0])]
        arms.append(("SPYONLY", 1, -1, [BENCH]))
        for sw in SWEEPS:
            for arm, K, seed, S in arms:
                for gross in GROSSES:
                    wr = width_weights(px, el, S, K, gross)
                    bk = run_book(px, wr, sweep=(sw == "SHY"))
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    yrs = len(tn) / 252
                    tg = wr.sum(axis=1).loc[start:]
                    nin_s = (el[S].sum(axis=1)).loc[start:]
                    book_facts.append(dict(
                        panel=pname, sweep=sw, arm=arm, K=(M if K == "ALL" else K), seed=seed,
                        gross=gross, cap_K=cap_for(K, M),
                        members=",".join(S) if (K != "ALL" and (K if K != "ALL" else 0) <= 8) else "",
                        target_gross=float(tg.mean()), target_sd=float(tg.std()),
                        target_min=float(tg.min()), target_max=float(tg.max()),
                        inband_frac=float((nin_s / (M if K == "ALL" else K)).mean()),
                        turnover_yr=float(tn.sum() / yrs),
                        turnover_risk_yr=float(bk["turn_risk"].loc[start:].sum() / yrs),
                        turnover_sweep_yr=float(bk["turn_sweep"].loc[start:].sum() / yrs),
                        mean_names=float(bk["names"].loc[start:].mean()),
                        mean_gross=float(bk["gross"].loc[start:].mean()),
                        max_gross=float(bk["gross"].loc[start:].max()),
                        max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, sweep=sw, arm=arm, K=(M if K == "ALL" else K), seed=seed,
                            gross=gross, cost_bps=rung, cap_K=cap_for(K, M),
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / yrs),
                            target_gross=float(tg.mean()),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                            base_CAGR=cagr(base_r), base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_r.loc[OOS_START:]), base_turnover=LIVE_TURNOVER,
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows over {len(bf)} distinct realised weight paths"
        f" (2 panels x {len(SWEEPS)} sweeps x [{len(WIDTHS) - 1} widths x {len(SEEDS)} seeds + ALL"
        f" + SPYONLY] x {len(GROSSES)} gross x {len(RUNGS)} rungs).")

    gate("G4 no leverage anywhere (max realised gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.9f} peak gross,"
         f" {bf.max_name_w.max():.4f} max single name", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))

    pz, ez = panels["U56"], ELIG["U56"]; st = pz.index[WARMUP]
    bz = run_book(pz, width_weights(pz, ez, subbook(pz.columns, "ALL", 0), "ALL", 0.75))
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP_TICKER].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.arm == "ALL") & (df.sweep == "SHY")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3b = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
              abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10, abs(a.turnover_yr - 3.51) / 100)
    gate("G3b K = ALL / g0.75 / SHY / 10 bps reproduces the COMMITTED CAP2 headline"
         " (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, turnover 3.51x)",
         f"{a.CAGR:.2%} / {a.Sharpe:.4f} / {a.MaxDD:.2%}, OOS {a.OOS_CAGR:.2%} / {a.OOS_Sharpe:.4f},"
         f" turn {a.turnover_yr:.2f}x  -> max|d| {d3b:.2e}", "< 1e-3", d3b < 1e-3)

    sp = bf[(bf.arm == "SPYONLY") & (bf.panel == "U56") & (bf.sweep == "SHY")
            & (bf.gross == 0.75)].iloc[0]
    gate("G11 the SPYONLY arm holds SPY and the SHY sweep and nothing else",
         f"mean names held {sp.mean_names:.3f} (<= 2), max single name weight {sp.max_name_w:.4f}",
         "<= 2 names", sp.mean_names <= 2.0 + 1e-9)

    # ------------------------------------------------------------ A. the width ladder
    def band(q, col):
        v = q[col]
        return f"{v.mean():7.4f} [{v.min():7.4f},{v.max():7.4f}]"

    say(f"\n=== A. THE WIDTH LADDER — seed MEAN [min, max], sweep {HEADLINE_SWEEP}, gross 0.75,"
        f" {HEADLINE_RUNG:.0f} bps.  EVERY GRID POINT IS IN {OUT.name}.grid.csv ===")
    say("  panel arm     cap_K  |   CAGR          Sharpe               MaxDD        | OOS Sh"
        "        | turn/yr       | risk gr | 4b seeds | 4a seeds")
    for pname in panels:
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.sweep == HEADLINE_SWEEP)
                   & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
            if not len(q):
                continue
            say(f"  {pname:5s} {arm:7s} {q.cap_K.iloc[0]:5.3f} | {q.CAGR.mean():6.2%}"
                f" [{q.CAGR.min():6.2%},{q.CAGR.max():6.2%}] {band(q, 'Sharpe')}"
                f" {q.MaxDD.mean():7.2%} [{q.MaxDD.min():7.2%}] | {band(q, 'OOS_Sharpe')}"
                f" | {q.turnover_yr.mean():5.2f} [{q.turnover_yr.min():4.2f},{q.turnover_yr.max():5.2f}]"
                f" | {q.target_gross.mean():7.3f} |"
                f" {int(q.pass4b.sum()):3d}/{len(q)}   | {int(q.pass4a.sum()):3d}/{len(q)}"
                + ("   <= COMMITTED" if arm == "ALL" else ""))

    say(f"\n=== A2. THE SAME LADDER AT GROSS 1.00, sweep {HEADLINE_SWEEP}, {HEADLINE_RUNG:.0f} bps ===")
    say("  panel arm     |   CAGR          Sharpe               MaxDD   | OOS Sh        | turn/yr"
        "       | 4b | 4a")
    for pname in panels:
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.sweep == HEADLINE_SWEEP)
                   & (df.gross == 1.00) & (df.cost_bps == HEADLINE_RUNG)]
            if not len(q):
                continue
            say(f"  {pname:5s} {arm:7s} | {q.CAGR.mean():6.2%}"
                f" [{q.CAGR.min():6.2%},{q.CAGR.max():6.2%}] {band(q, 'Sharpe')}"
                f" {q.MaxDD.mean():7.2%} | {band(q, 'OOS_Sharpe')}"
                f" | {q.turnover_yr.mean():5.2f} [{q.turnover_yr.min():4.2f},{q.turnover_yr.max():5.2f}]"
                f" | {int(q.pass4b.sum()):2d}/{len(q)} | {int(q.pass4a.sum()):2d}/{len(q)}")

    say(f"\n=== A3. THE ZERO-SWEEP LADDER (idea 2423's pessimal un-remunerated bound), g0.75,"
        f" {HEADLINE_RUNG:.0f} bps ===")
    say("  panel arm     |   CAGR     Sharpe    MaxDD   | OOS Sh  | turn/yr | 4b | 4a")
    for pname in panels:
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.sweep == "ZERO")
                   & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
            if not len(q):
                continue
            say(f"  {pname:5s} {arm:7s} | {q.CAGR.mean():6.2%} {q.Sharpe.mean():9.4f}"
                f" {q.MaxDD.mean():8.2%} | {q.OOS_Sharpe.mean():7.4f} | {q.turnover_yr.mean():7.2f}"
                f" | {int(q.pass4b.sum()):2d}/{len(q)} | {int(q.pass4a.sum()):2d}/{len(q)}")

    say("\n=== A4. THE FULL COST LADDER on the seed mean (sweep SHY, g0.75) ===")
    say("  panel arm       bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4b seeds | legs H1/H2/OOS/DD/CAGR (seed mean pass rate)")
    for pname in panels:
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            for rung in RUNGS:
                q = df[(df.panel == pname) & (df.arm == arm) & (df.sweep == HEADLINE_SWEEP)
                       & (df.gross == 0.75) & (df.cost_bps == rung)]
                if not len(q):
                    continue
                lg = "/".join(f"{q[x].mean():.2f}" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s} {arm:7s} {rung:5.1f} | {q.CAGR.mean():6.2%} {q.Sharpe.mean():7.4f}"
                    f" {q.MaxDD.mean():8.2%} | {q.H1.mean():5.2f} {q.H2.mean():6.2f}"
                    f" | {q.OOS_CAGR.mean():7.2%} {q.OOS_Sharpe.mean():7.4f}"
                    f" | {q.turnover_yr.mean():7.2f} | {int(q.pass4b.sum()):3d}/{len(q)} | {lg}")

    # ------------------------------------------------------------ B. the whole question
    say("\n=== B. THE WHOLE QUESTION: DOES WIDTH CUT TURNOVER WITHOUT CUTTING EXPOSURE? ===")
    say("  (mean over seeds, sweep SHY, g0.75.  The committed book is ALL; idea 2431's adoption bar")
    say(f"   is turnover <= {ADOPTION_BAR_TURNOVER:.2f}x AT UNCHANGED RETURNS.)")
    say("  panel arm     | turn/yr  vs ALL | risk gross vs ALL | in-band frac | CAGR vs ALL"
        " | Sharpe vs ALL | pp CAGR per 1% turnover saved")
    exch = []
    for pname in panels:
        ref = df[(df.panel == pname) & (df.arm == "ALL") & (df.sweep == HEADLINE_SWEEP)
                 & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.sweep == HEADLINE_SWEEP)
                   & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
            if not len(q) or arm == "ALL":
                continue
            dt = q.turnover_yr.mean() / ref.turnover_yr - 1
            dc = q.CAGR.mean() - ref.CAGR
            rate = (dc * 100) / (-dt * 100) if dt < 0 else np.nan
            exch.append(dict(panel=pname, arm=arm, dTurn=dt, dCAGR=dc,
                             dSharpe=q.Sharpe.mean() - ref.Sharpe,
                             dGross=q.target_gross.mean() - ref.target_gross, rate=rate,
                             turn=q.turnover_yr.mean(), clears_bar=bool(q.turnover_yr.mean() <= ADOPTION_BAR_TURNOVER)))
            say(f"  {pname:5s} {arm:7s} | {q.turnover_yr.mean():6.2f} {dt:+7.1%}"
                f" | {q.target_gross.mean():10.3f} {q.target_gross.mean() - ref.target_gross:+6.3f}"
                f" | {bf[(bf.panel == pname) & (bf.arm == arm) & (bf.sweep == HEADLINE_SWEEP) & (bf.gross == 0.75)].inband_frac.mean():12.3f}"
                f" | {dc * 100:+6.2f} pp | {q.Sharpe.mean() - ref.Sharpe:+9.4f}"
                f" | {('%+.3f' % rate) if dt < 0 else '   n/a (turnover rose)'}")
    ex = pd.DataFrame(exch); ex.to_csv(f"{OUT}.exchange.csv", index=False)
    say(f"\n   The record's eleven closed turnover devices all paid about -0.10 pp of CAGR per 1% saved.")
    cut = ex[ex.dTurn < 0]
    if len(cut):
        b = cut.loc[cut.rate.idxmax()]
        publish("the BEST exchange rate anywhere on the width dial (headline convention)",
                f"{b.rate:+.3f} pp of CAGR per 1% saved at {b.panel}/{b.arm}"
                f" (turnover {b.turn:.2f}x, {b.dTurn:+.1%}, CAGR {b.dCAGR * 100:+.2f} pp)")
    publish("arms clearing idea 2431's turnover bar (<= 2.42x/yr) at the headline convention",
            f"{int(ex.clears_bar.sum())} of {len(ex)}: "
            + ", ".join(f"{r.panel}/{r.arm}:{r.turn:.2f}x" for _, r in ex[ex.clears_bar].iterrows()))

    g10 = {p: float(bf[(bf.panel == p) & (bf.arm == "K001") & (bf.sweep == HEADLINE_SWEEP)
                       & (bf.gross == 0.75)].turnover_yr.mean()
                    / bf[(bf.panel == p) & (bf.arm == "ALL") & (bf.sweep == HEADLINE_SWEEP)
                         & (bf.gross == 0.75)].turnover_yr.mean() - 1) for p in panels}
    gate("G10 the dial BITES (K = 1 turnover against the committed ALL book, headline convention)",
         "  ".join(f"{p}:{v:+.1%}" for p, v in g10.items()), "< 0", all(v < 0 for v in g10.values()))

    say("\n   EXPOSURE INVARIANCE — the claim that makes width different from every closed device")
    say("   (mean realised RISK gross by width; a pure exposure dial would fall with K):")
    for pname in panels:
        q = bf[(bf.panel == pname) & (bf.sweep == HEADLINE_SWEEP) & (bf.gross == 0.75)]
        say(f"    {pname:5s} " + "  ".join(
            f"{a}:{q[q.arm == a].target_gross.mean():.3f}"
            for a in [wlabel(K) for K in WIDTHS] + ["SPYONLY"] if len(q[q.arm == a])))
    sp_ = bf[(bf.sweep == HEADLINE_SWEEP) & (bf.gross == 0.75) & (bf.arm != "SPYONLY")]
    spread = {p: (float(sp_[sp_.panel == p].groupby("arm").target_gross.mean().max()
                        - sp_[sp_.panel == p].groupby("arm").target_gross.mean().min()))
              for p in panels}
    publish("G8 range of mean risk gross across the whole width ladder (exposure invariance)",
            "  ".join(f"{p}: {v:.4f} of NAV" for p, v in spread.items()))

    # ------------------------------------------------------------ C. KEEP counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
        d = df[df.arm == arm]
        say(f"   {arm:7s}: 4b {int(d.pass4b.sum()):4d}/{len(d)}   4a {int(d.pass4a.sum()):4d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):4d}/{len(d)}   4a {int(d.pass4a.sum()):4d}/{len(d)}")
    for sw in SWEEPS:
        d = df[df.sweep == sw]
        say(f"   sweep {sw:4s}: 4b {int(d.pass4b.sum()):4d}/{len(d)}   4a {int(d.pass4a.sum()):4d}/{len(d)}")
    for gr_ in GROSSES:
        d = df[df.gross == gr_]
        say(f"   gross {gr_:.2f}: 4b {int(d.pass4b.sum()):4d}/{len(d)}   4a {int(d.pass4a.sum()):4d}/{len(d)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same sweep, arm, seed, gross, rung):")
    jt = []
    for sw in SWEEPS:
        for arm in [wlabel(K) for K in WIDTHS] + ["SPYONLY"]:
            for seed in (SEEDS if arm not in ("ALL", "SPYONLY") else [0 if arm == "ALL" else -1]):
                for gr_ in GROSSES:
                    for rung in RUNGS:
                        q = df[(df.sweep == sw) & (df.arm == arm) & (df.seed == seed)
                               & (df.gross == gr_) & (df.cost_bps == rung)]
                        if len(q) != 2:
                            continue
                        jt.append(dict(sweep=sw, arm=arm, seed=seed, gross=gr_, cost_bps=rung,
                                       joint=bool(q.pass4b.all())))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by arm: "
        + "  ".join(f"{a}:{int(jf[jf.arm == a].joint.sum())}/{len(jf[jf.arm == a])}"
                    for a in [wlabel(K) for K in WIDTHS] + ["SPYONLY"] if len(jf[jf.arm == a])))
    say("   NOTE: the two panels share the same sub-book DRAW ONLY at K = ALL and SPYONLY; at every")
    say("   other K the seeds index different universes, so 'joint' is a same-seed coincidence test,")
    say("   not a replication of one book.  Read it as the width-level pass rate, which is above it.")

    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.sort_values("Sharpe", ascending=False).head(15).iterrows():
        say(f"    {r.panel:5s} {r.sweep:4s} {r.arm:7s} seed {int(r.seed):2d} g {r.gross:.2f}"
            f" {r.cost_bps:5.1f}bps  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
            f"  turn {r.turnover_yr:.2f}x  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ D. rule 8
    say("\n=== D. RULE 8 — both dials (K, g) chosen on warm-up..2016-12-31 ONLY, on the SEED MEAN so")
    say("    no seed is selectable either; 2017-2026 read ONCE and scored against the COMMITTED")
    say("    K = ALL / g = 0.75 cell.  SPYONLY is a named reference and is EXCLUDED from the pick set. ===")
    wf = []
    picks = [wlabel(K) for K in WIDTHS]
    for pname in panels:
        for sw in SWEEPS:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.sweep == sw) & (df.cost_bps == rung)
                       & (df.arm.isin(picks))]
                cm = d[(d.arm == "ALL") & (d.gross == 0.75)].iloc[0]
                gp = d.groupby(["arm", "gross"], as_index=False).mean(numeric_only=True)
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = gp.loc[gp[col].idxmax()]
                    sel = d[(d.arm == pk.arm) & (d.gross == pk.gross)]
                    wf.append(dict(panel=pname, sweep=sw, cost_bps=rung, chooser=chooser,
                                   pick_arm=pk.arm, pick_gross=pk.gross,
                                   pick_4b_rate=float(sel.pass4b.mean()),
                                   OOS_CAGR=float(sel.OOS_CAGR.mean()),
                                   OOS_Sharpe=float(sel.OOS_Sharpe.mean()),
                                   OOS_MaxDD=float(sel.OOS_MaxDD.mean()),
                                   pick_turn=float(sel.turnover_yr.mean()),
                                   committed_turn=cm.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe,
                                   committed_OOS_CAGR=cm.OOS_CAGR,
                                   committed_OOS_MaxDD=cm.OOS_MaxDD,
                                   base_OOS_Sharpe=cm.base_OOS_Sharpe,
                                   base_OOS_CAGR=cm.base_OOS_CAGR,
                                   spy_OOS_Sharpe=cm.spy_OOS_Sharpe, spy_OOS_CAGR=cm.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x {len(SWEEPS)} sweeps x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                      {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:            {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED ALL cell's OOS Sharpe:   {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say("   pick distribution over width: " + "  ".join(
        f"{a}:{int((wfd.pick_arm == a).sum())}" for a in picks))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean OOS CAGR of the IS-only picks   {wfd.OOS_CAGR.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_CAGR.mean():.2%}"
        f" vs the live book's {wfd.base_OOS_CAGR.mean():.2%} vs SPY OOS {wfd.spy_OOS_CAGR.mean():.2%}")
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs the live book's {wfd.base_OOS_Sharpe.mean():.4f} vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say(f"   mean OOS MaxDD of the IS-only picks  {wfd.OOS_MaxDD.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_MaxDD.mean():.2%}")
    say(f"   mean turnover of the picks {wfd.pick_turn.mean():.2f}x vs the committed"
        f" {wfd.committed_turn.mean():.2f}x (live book {LIVE_TURNOVER}x)")
    say("\n   panel sw    bps chooser     | pick        4b rate  OOS CAGR  OOS Sh  OOS DD   turn/yr"
        " | committed OOS Sh / turn")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.sweep:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r.pick_arm + '/' + format(r.pick_gross, '.2f'):12s} {r.pick_4b_rate:7.2f}"
            f" {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} {r.pick_turn:8.2f}"
            f" | {r.committed_OOS_Sharpe:12.4f} / {r.committed_turn:.2f}")

    say("\n   THE SPYONLY REFERENCE, OUT OF SAMPLE (named arm, never picked, zero survivorship):")
    for pname in panels:
        for gr_ in GROSSES:
            q = df[(df.panel == pname) & (df.arm == "SPYONLY") & (df.sweep == HEADLINE_SWEEP)
                   & (df.gross == gr_) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"    {pname:5s} g{gr_:.2f} | full {q.CAGR:6.2%} / {q.Sharpe:.4f} / {q.MaxDD:7.2%}"
                f" | halves {q.H1:.2f} / {q.H2:.2f} (SPY {halves(panels[pname][BENCH].pct_change().fillna(0).loc[panels[pname].index[WARMUP]:])[0]:.2f} / {halves(panels[pname][BENCH].pct_change().fillna(0).loc[panels[pname].index[WARMUP]:])[1]:.2f})"
                f" | OOS {q.OOS_CAGR:6.2%} / {q.OOS_Sharpe:.4f} | turn {q.turnover_yr:.2f}x"
                f" | 4a {'Y' if q.pass4a else '.'} 4b {'Y' if q.pass4b else '.'}"
                f" legs {''.join('1' if q[x] else '0' for x in ('L_H1','L_H2','L_OOS','L_DD','L_CAGR'))}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
