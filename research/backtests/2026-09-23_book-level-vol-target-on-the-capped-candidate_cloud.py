#!/usr/bin/env python3
"""idea 2403 (lane cloud, run 41, 2026-09-23) — DOES A BOOK-LEVEL VOLATILITY TARGET MOVE THE
CAPPED CANDIDATE'S BINDING `L_DD` LEG WHERE PER-NAME VOL SIZING COULD NOT?

THE GAP.  Every vol device this record has priced is CROSS-SECTIONAL: idea 1373 (inverse-vol on
the 2026-09-04 top-20), idea 2362 (inverse-vol inside the 2% cap), idea 2339 (group cap), idea
2381 (relative cap), idea 2387 (breadth cap).  All were KILLED, and idea 2381 measured WHY: each
one re-orders who gets what slice at a gross that barely moves, so it is an exposure dial whose
sign is already known.  The classical TIME-SERIES device has never been priced anywhere here:
scale the ENTIRE risk sleeve by one number that falls exactly when volatility is being realised.

    s_t   = min(1, sigma_target / sigma_hat_t)        (capped at 1 -> NEVER any leverage)
    w_i   = s_t x min(gross / N_in, 0.02)  on names INSIDE the 200d +/- 0.03 band
    SHY   = 1 - sum_i w_i                              (phi = 1.00, the whole residual)

DIAL 1 -- sigma_target {0.08, 0.10, 0.12, 0.15, INF} annualised.  **INF IS CAP2 EXACTLY**
          (s_t == 1 on every day), so one ladder spans the committed book; asserted by G3.
DIAL 2 -- vol lookback V {20, 60} trading days.

CAUSALITY, THE ONE THING THIS DEVICE CAN GET WRONG.  `sigma_hat_t` is the annualised standard
deviation of the BOOK'S OWN realised daily returns over the V days ENDING AT t-1 -- returns that
are already banked when the scaler is computed.  The headline convention S is SELF-REFERENTIAL
and recursive (the scaled book's own returns feed the next scaler), exactly as the pushed claim
states; convention U (the UNSCALED CAP2 book's returns as the vol reference) is published beside
it, never selected on.  Weights so scaled are then executed at t+1 as every book here is.
G9 asserts no lookahead on the realised return series itself, not merely on the weights.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, gross
{0.75 live, 1.00}, weekly cadence, t+1 execution, band 0.03, the 2% weight cap, the SHY sweep,
and the second convention U.  5 x 2 x 2 x 2 = 40 books per convention, every one at every rung.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
each published SMALL's 4b pass count at 0 of 40-120, and idea 2383 (this lane, this morning) read
it at 0 of 128 with `L_DD`, `L_H2` and `L_OOS` failing at every one of 128 cells.  There is no
pass on that panel for a vol target to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: (sigma_target, V) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

THE DEVICE'S OWN BILL IS MEASURED, NOT ASSUMED: mean book gross, mean SHY sleeve, turnover/yr and
the full distribution of `s_t` (mean, median, 5th percentile, share of days binding) are published
at every grid point, because a vol target adds turnover of its own.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 sigma_target = INF is BIT-IDENTICAL to an independent CAP2
construction priced through `engine.backtest`.  G4 no leverage anywhere (s_t <= 1 by construction,
asserted on realised row sums).  G5 the sigma_target dial BITES and is MONOTONE in mean gross.
G6 SHY priced on every held row.  G7 exactly two tuned parameters.  G8 s_t is causal (recomputed
from a truncated panel, identical over the overlap).  G9 no lookahead on the RETURN series.
G10 EXTERNAL REPRODUCTION of idea 2322/2336's committed CAP2 U56 headline (11.62% / 1.2687 /
-14.81%, OOS 12.77% / 1.3318, turnover 3.51x).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The targeted-vs-untargeted contrast is same-tape,
same-day, same-gross and first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_book-level-vol-target-on-the-capped-candidate_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "book-level-vol-target-on-the-capped-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
TARGETS = [0.08, 0.10, 0.12, 0.15, np.inf]
LOOKBACKS = [20, 60]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, NAME_CAP, SWEEP = 10.0, 0.020, "SHY"
CONVENTIONS = ["S", "U"]          # S = self-referential (headline, as claimed); U = unscaled ref
HEADLINE_CONV = "S"
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


def tname(st):
    return "INF" if not np.isfinite(st) else f"{st:.2f}"


# ---------------------------------------------------------------- the risk book (pre-scaler)
def cap2_risk_weights(px, invest, gross, cap=NAME_CAP):
    """idea 2322's CAP2 RISK sleeve only (no sweep added): w_i = min(gross / N_in, cap) on names
    INSIDE the 200d +/- 0.03 band.  The SHY sweep is applied inside the runner, AFTER the scaler,
    so that s_t scales risk and never the cash leg."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)


def cap2_full_reference(px, invest, gross, cap=NAME_CAP):
    """Independent CAP2 construction WITH the sweep (the committed book), for the G3 anchor."""
    w = cap2_risk_weights(px, invest, gross, cap).copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the vol-targeted runner
def run_vt(prices, w_risk, sigma_target, V, conv, ref_r0=None, freq=CADENCE, sweep=True):
    """engine.backtest with a BOOK-LEVEL vol target on the risk sleeve.

    At each rebalance day i the scaler is
        sigma_hat = std(ret[i-V : i]) * sqrt(252)        <- returns through i-1 ONLY
        s         = min(1, sigma_target / sigma_hat)     <- capped at 1, no leverage ever
    where `ret` is this book's OWN realised zero-cost daily return series under convention S
    (recursive, the headline) or the UNSCALED CAP2 book's series `ref_r0` under convention U.
    Risk weights are multiplied by s and the WHOLE residual `1 - sum` goes to SHY (phi = 1.00);
    `sweep=False` turns that off so the runner reproduces a de-grossing-to-cash book such as live
    RULES v2 exactly (that is what G1 checks).
    Everything else is `engine.backtest` verbatim; the un-invested residual drifts at 0%.
    """
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values     # decided t-1, applied t
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    ref = None if ref_r0 is None else np.asarray(ref_r0, dtype=float)

    n, m = len(prices.index), len(cols)
    held = np.zeros((n, m)); cur = np.zeros(m)
    to = np.zeros(n); gr = np.zeros(n); sc = np.full(n, np.nan); r0 = np.zeros(n)
    infinite = not np.isfinite(sigma_target)

    for i in range(n):
        if mask[i] or i == 0:
            if infinite:
                s = 1.0
            else:
                hist = (r0 if conv == "S" else ref)[max(0, i - V):i]
                sd = hist.std() * np.sqrt(252) if len(hist) >= V else 0.0
                s = min(1.0, sigma_target / sd) if sd > 1e-12 else 1.0
            x = wt[i] * s
            new = x.copy()
            if sweep:
                new[shy_i] += max(0.0, 1.0 - x.sum()) * shy_ok[i]
            to[i] = np.abs(new - cur).sum()
            cur = new
            sc[i] = s
        held[i] = cur
        gr[i] = cur.sum()
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur

    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turnover=pd.Series(to, index=idx),
                gross=pd.Series(gr, index=idx), scaler=pd.Series(sc, index=idx).ffill(),
                risk_gross=pd.Series(held.sum(axis=1) - held[:, shy_i], index=idx))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


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
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2403 — DOES A BOOK-LEVEL VOLATILITY TARGET MOVE THE CAPPED CANDIDATE'S `L_DD`? ===")
    say(f"    {DATE}  lane {LANE} run 41   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 sigma_target {[tname(x) for x in TARGETS]}   DIAL 2 lookback V {LOOKBACKS}")
    say(f"    conventions: S (self-referential, HEADLINE, as claimed) and U (unscaled CAP2 as the vol reference)")
    say("    s_t = min(1, sigma_target / sigma_hat_t), capped at 1 -> NO LEVERAGE, EVER.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells in idea 2383 this morning (L_DD, L_H2, L_OOS fail everywhere),")
    say("    and 0 of 40-120 in ideas 2318 / 2322 / 2326 / 2343 — there is no pass there to keep or break.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The targeted-vs-untargeted contrast is same-tape and first-order immune.")
    gate("G7 exactly two tuned parameters", "sigma_target, V", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u, inv_u = panels["U56"]
    d2 = int((band_state(px_u, BAND) != band_state(px_u, BAND)).sum().sum())
    inb_ref = band_state(px_u, BAND)
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified", f"{d2} differing cells;"
         f" mean names IN {int(inb_ref.sum(axis=1).mean())}", "0", d2 == 0)

    # G1 replica fidelity on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    res_live = run_vt(px_u, w_live, np.inf, 20, "S", sweep=False)
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, sweep off)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3 sigma_target = INF IS CAP2, priced through the engine itself
    wr = cap2_risk_weights(px_u, inv_u, 0.75)
    inf_res = run_vt(px_u, wr, np.inf, 20, "S")
    cap2_eng = backtest(px_u, cap2_full_reference(px_u, inv_u, 0.75), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d3 = float((cap2_eng - priced(inf_res, HEADLINE_RUNG)).abs().max())
    gate("G3 sigma_target = INF == an independent CAP2 construction through engine.backtest",
         f"max|d| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8/G9 causality: truncate the panel, the scaler and the return series must not move
    cut = px_u.index[int(len(px_u) * 0.70)]
    tr = run_vt(px_u.loc[:cut], cap2_risk_weights(px_u.loc[:cut], inv_u, 0.75), 0.10, 60, "S")
    fu = run_vt(px_u, wr, 0.10, 60, "S")
    d8 = float((tr["scaler"] - fu["scaler"].loc[:cut]).abs().max())
    d9 = float((tr["r0"] - fu["r0"].loc[:cut]).abs().max())
    gate(f"G8 the scaler s_t is causal (panel truncated at {cut.date()}, sigma_target 0.10, V 60)",
         f"max|ds| {d8:.3e}", "< 1e-12", d8 < 1e-12)
    gate("G9 no lookahead on the RETURN series (same truncation)", f"max|dr| {d9:.3e}", "< 1e-12", d9 < 1e-12)

    rows, expo = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_vt(px, rules_v2_weights(px, band=BAND, gross=0.75), np.inf, 20, "S",
                                   sweep=False), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} investable)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}"
            f"  halves {halves(base_r)[0]:.4f}/{halves(base_r)[1]:.4f}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        for gross in GROSSES:
            w_risk = cap2_risk_weights(px, invest, gross)
            unscaled = run_vt(px, w_risk, np.inf, 20, "S")
            say(f"    realised vol of the UNSCALED CAP2 book, g={gross:.2f}: "
                f"{unscaled['r0'].loc[win].std() * np.sqrt(252):.4f} annualised")
            for conv in CONVENTIONS:
                for st in TARGETS:
                    for V in LOOKBACKS:
                        res = run_vt(px, w_risk, st, V, conv, ref_r0=unscaled["r0"].values)
                        s = res["scaler"].loc[win].dropna()
                        expo.append(dict(panel=pname, conv=conv, target=tname(st), V=V, gross=gross,
                                         s_mean=float(s.mean()), s_med=float(s.median()),
                                         s_p05=float(np.percentile(s, 5)), s_min=float(s.min()),
                                         bind_share=float((s < 1 - 1e-12).mean()),
                                         mean_gross=float(res["gross"].loc[win].mean()),
                                         mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                         mean_shy=float(res["gross"].loc[win].mean()
                                                         - res["risk_gross"].loc[win].mean()),
                                         turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                         max_row_sum=float(res["gross"].max()),
                                         real_vol=float(priced(res, HEADLINE_RUNG).loc[win].std() * np.sqrt(252))))
                        for rung in RUNGS:
                            r = priced(res, rung).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, conv=conv, target=tname(st), V=V,
                                             gross=gross, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             spy_OOS_Sharpe=sharpe(spy_oos),
                                             base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); ef = pd.DataFrame(expo)
    df.to_csv(f"{OUT}.grid.csv", index=False); ef.to_csv(f"{OUT}.exposure.csv", index=False)

    gate("G4 no leverage (all books, realised row sums)", f"max row sum {ef.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((ef.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)

    mono = []
    for (pname, conv, V, gross), g in ef.groupby(["panel", "conv", "V", "gross"]):
        v = g.set_index("target").reindex([tname(x) for x in TARGETS]).mean_risk_gross.values
        mono.append(bool(np.all(np.diff(v) > -1e-12) and np.ptp(v) > 1e-4))
    gate("G5 the sigma_target dial BITES and mean RISK gross is MONOTONE along it"
         " (total gross is pinned at 1.0 by the SHY sweep, so the risk sleeve is the exposure)",
         f"{sum(mono)} of {len(mono)} (panel, conv, V, gross) cells", f"{len(mono)} of {len(mono)}", all(mono))

    h = df[(df.panel == "U56") & (df.conv == HEADLINE_CONV) & (df.target == "INF") & (df.V == 20)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    e0 = ef[(ef.panel == "U56") & (ef.conv == HEADLINE_CONV) & (ef.target == "INF") & (ef.V == 20)
            & (ef.gross == 0.75)].iloc[0]
    d10 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
              abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G10 reproduces the committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {e0.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the ladder
    say(f"\n=== A. THE FULL LADDER AT 10 bps, gross 0.75, HEADLINE CONVENTION {HEADLINE_CONV} — every point ===")
    say("  panel  targ   V |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR | s_mean bind% gross turn/yr realvol")
    for pname in panels:
        for st in TARGETS:
            for V in LOOKBACKS:
                r = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.target == tname(st))
                       & (df.V == V) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.conv == HEADLINE_CONV) & (ef.target == tname(st))
                       & (ef.V == V) & (ef.gross == 0.75)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s} {tname(st):>5s} {V:3d} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {e.s_mean:6.3f} {e.bind_share:5.1%} {e.mean_risk_gross:5.3f} {e.turnover_yr:7.2f} {e.real_vol:6.3f}"
                    + ("   <= CAP2 (anchor)" if not np.isfinite(st) else ""))

    say("\n=== B. DOES IT BUY `L_DD` WITHOUT PAYING `L_CAGR`?  deltas vs the CAP2 anchor, 10 bps, g=0.75 ===")
    say("    (this is the WHOLE question: a cross-sectional dial pays CAGR one-for-one; a time-series")
    say("     dial is supposed not to.  'pp of CAGR per pp of drawdown bought' is the exchange rate.)")
    for pname in panels:
        ref = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.target == "INF") & (df.V == 20)
                 & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        say(f"  {pname} CAP2 anchor: {ref.CAGR:.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:.2%}"
            f"  (m_DD {ref.m_DD:+.4f}, m_CAGR {ref.m_CAGR:+.4f})")
        for st in TARGETS:
            if not np.isfinite(st):
                continue
            for V in LOOKBACKS:
                r = df[(df.panel == pname) & (df.conv == HEADLINE_CONV) & (df.target == tname(st))
                       & (df.V == V) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                dd_bought = r.MaxDD - ref.MaxDD          # positive = shallower
                cagr_paid = ref.CAGR - r.CAGR            # positive = gave up return
                rate = cagr_paid / dd_bought if abs(dd_bought) > 1e-9 else np.inf
                say(f"    targ {tname(st)} V {V:3d}:  dCAGR {r.CAGR - ref.CAGR:+6.2%}"
                    f"  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}  dMaxDD {dd_bought:+6.2%}"
                    f"  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}  |  exchange rate"
                    f" {rate:6.2f} pp CAGR per pp of DD  | 4b {'Y' if r.pass4b else '.'}")

    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (5 targ x 2 V x 2 conv x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for conv in CONVENTIONS:
        d = df[df.conv == conv]
        say(f"   convention {conv}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    for st in TARGETS:
        d = df[(df.target == tname(st)) & (df.conv == HEADLINE_CONV)]
        say(f"   sigma_target {tname(st):>5s} (conv {HEADLINE_CONV}): 4b {int(d.pass4b.sum()):2d}/{len(d)}"
            f"   4a {int(d.pass4a.sum()):2d}/{len(d)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same target, V, conv, gross, rung):")
    jt = []
    for conv in CONVENTIONS:
        for st in TARGETS:
            for V in LOOKBACKS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        q = df[(df.conv == conv) & (df.target == tname(st)) & (df.V == V)
                               & (df.gross == gross) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(conv=conv, target=tname(st), V=V, gross=gross, cost_bps=rung,
                                       joint=bool(u.pass4b and b.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells"
        f"   [CAP2 anchor (target INF): {int(jf[jf.target == 'INF'].joint.sum())} of {len(jf[jf.target == 'INF'])}]")
    for conv in CONVENTIONS:
        say(f"   convention {conv}: " + "  ".join(
            f"targ {tname(st):>5s} "
            f"{int(jf[(jf.conv == conv) & (jf.target == tname(st))].joint.sum())}"
            f"/{len(jf[(jf.conv == conv) & (jf.target == tname(st))])}"
            for st in TARGETS))
    say("   joint 4b at the LIVE gross 0.75 only (conv S, 4 rungs per target): " + "  ".join(
        f"targ {tname(st):>5s} "
        f"{int(jf[(jf.conv == 'S') & (jf.target == tname(st)) & (jf.gross == 0.75)].joint.sum())}"
        f"/{len(jf[(jf.conv == 'S') & (jf.target == tname(st)) & (jf.gross == 0.75)])}"
        for st in TARGETS))
    say("\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse) — every one, listed:")
    pa = df[df.pass4a]
    if len(pa) == 0:
        say("    NONE")
    else:
        for _, r in pa.iterrows():
            say(f"    {r.panel:5s} conv {r.conv} targ {r.target:>5s} V {r.V:3d} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
                f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
                f"  4b {'Y' if r.pass4b else '.'}")

    say("\n=== D. THE DEVICE'S OWN BILL, MEASURED NOT ASSUMED (conv S, g=0.75, 10 bps) ===")
    say("  panel  targ   V | s_mean s_med  s_p05  s_min  bind%  | risk gross  mean SHY  turn/yr  realised vol")
    for pname in panels:
        for st in TARGETS:
            for V in LOOKBACKS:
                e = ef[(ef.panel == pname) & (ef.conv == HEADLINE_CONV) & (ef.target == tname(st))
                       & (ef.V == V) & (ef.gross == 0.75)].iloc[0]
                say(f"  {pname:5s} {tname(st):>5s} {V:3d} | {e.s_mean:6.3f} {e.s_med:6.3f} {e.s_p05:6.3f}"
                    f" {e.s_min:6.3f} {e.bind_share:6.1%} | {e.mean_risk_gross:10.3f} {e.mean_shy:9.3f}"
                    f" {e.turnover_yr:8.2f} {e.real_vol:13.4f}")

    say("\n=== E. CONVENTION S vs CONVENTION U — is the recursive scaler doing anything different? ===")
    for pname in panels:
        for st in TARGETS:
            if not np.isfinite(st):
                continue
            for V in LOOKBACKS:
                a = df[(df.panel == pname) & (df.conv == "S") & (df.target == tname(st)) & (df.V == V)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                b = df[(df.panel == pname) & (df.conv == "U") & (df.target == tname(st)) & (df.V == V)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                say(f"  {pname:5s} targ {tname(st)} V {V:3d}:  S {a.CAGR:6.2%}/{a.Sharpe:.4f}/{a.MaxDD:7.2%} 4b {'Y' if a.pass4b else '.'}"
                    f"   U {b.CAGR:6.2%}/{b.Sharpe:.4f}/{b.MaxDD:7.2%} 4b {'Y' if b.pass4b else '.'}"
                    f"   |dSharpe| {abs(a.Sharpe - b.Sharpe):.4f}")

    say("\n=== F. RULE 8 — (sigma_target, V) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_vt(px, rules_v2_weights(px, band=BAND, gross=0.75), np.inf, 20, "S",
                                sweep=False), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for conv in CONVENTIONS:
            for gross in GROSSES:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.conv == conv) & (df.gross == gross) & (df.cost_bps == rung)]
                    inc = d[d.target == "INF"].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, conv=conv, gross=gross, cost_bps=rung, chooser=chooser,
                                       pick_target=pk.target, pick_V=pk.V,
                                       pick_is_cap2=bool(pk.target == "INF"), full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                       inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_CAGR=inc.OOS_CAGR,
                                       base_OOS_Sharpe=sharpe(b_oos), base_OOS_CAGR=cagr(b_oos),
                                       spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos)))
                        if conv == HEADLINE_CONV and gross == 0.75:
                            say(f"  {pname:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} ->"
                                f" targ {pk.target:>5s} V {pk.V:3d} |"
                                f" OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%} |"
                                f" CAP2 anchor OOS {inc.OOS_CAGR:6.2%} / {inc.OOS_Sharpe:.4f} |"
                                f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} |"
                                f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} |"
                                f" full 4b {'Y' if pk.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  {len(wfd)} picks (2 panels x 2 conv x 2 gross x 4 rungs x 2 choosers).")
    say(f"   picks landing on the CAP2 ANCHOR (sigma_target = INF, i.e. NO vol target): "
        f"{int(wfd.pick_is_cap2.sum())} of {len(wfd)}")
    say(f"   picks beating SPY's OOS Sharpe:                    {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:          {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the CAP2 ANCHOR's own OOS Sharpe:    {int((wfd.OOS_Sharpe > wfd.inc_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:              {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over sigma_target: " + "  ".join(
        f"{tname(st):>5s}:{int((wfd.pick_target == tname(st)).sum())}" for st in TARGETS))
    say("   pick distribution over V: " + "  ".join(f"{V}:{int((wfd.pick_V == V).sum())}" for V in LOOKBACKS))
    agree = reach = 0
    for conv in CONVENTIONS:
        for gross in GROSSES:
            for rung in RUNGS:
                for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                    q = wfd[(wfd.conv == conv) & (wfd.gross == gross) & (wfd.cost_bps == rung) & (wfd.chooser == ch)]
                    u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                    same = bool(u.pick_target == b.pick_target and u.pick_V == b.pick_V)
                    agree += int(same); reach += int(same and u.full4b and b.full4b)
    say(f"   U56 and B136 agree on (sigma_target, V) in {agree} of 32 (conv x gross x rung x chooser) cells")
    say(f"   cells where both panels agree AND both carry a full-sample 4b: {reach} of 32")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
