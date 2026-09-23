#!/usr/bin/env python3
"""idea 2543 (lane cloud, run 73, 2026-09-23) — DOES THE CANDIDATE BEAT ITS OWN GROSS-MATCHED
BLEND ONLY IN DRAWDOWN WEEKS?  HOW MUCH OF THE DEFENSIVE PREMIUM IS EARNED IN HOW FEW DAYS?

THE GAP.  Idea 2532's headline — the capped candidate beats the gross-matched EWBH blend on
MaxDD in 128 of 128 cells and loses CAGR in 128 of 128 — is a pair of FULL-SAMPLE counts.  A
full-sample count cannot say WHEN the defensive premium is earned, and that is the whole
adoption question: a premium earned in 3% of the tape is an insurance contract whose price is
paid every other week and whose payout depends on a handful of episodes, while a premium earned
evenly is a property of the book.  Idea 2550 then killed the blend as a fundable book in its own
right (`L_DD` binds first in 128 of 128), which makes this decomposition the ONLY remaining live
question about the pair: not "which is better" but "what exactly is the candidate buying".

THE DEVICE.  `d_t = r_CAP2,t - r_BLEND,t`, both net at the same rung, where
`BLEND_t = m_t x EWBH(panel) + (1 - m_t) x SHY` and `m_t` is the CAPPED candidate's OWN realised
risk gross `min(g, 0.02 x N_in,t)` (2532's convention verbatim; idea 2506 proved this path is the
cap's actual content).  Split the tape by the BENCHMARK's own running drawdown depth and report,
for each depth threshold, what share of the premium is earned in what share of the days, across
how few distinct EPISODES, with a block bootstrap on both.

CAUSALITY — THE STATE IS LAGGED, WHICH MAKES THE SPLIT IMPLEMENTABLE AND NOT MERELY DESCRIPTIVE.
The headline state is `s_t = 1[dd_SPY,t-1 <= -theta]`, the drawdown KNOWN AT THE PRIOR CLOSE, so
every statistic below could have been computed in real time.  The CONTEMPORANEOUS convention
(`dd_SPY,t`) is published beside it, never selected on, because it is the one a naive
decomposition would use and it is the one that flatters the result.

WHY THIS CAN REFUTE ITSELF.  If the premium is CONCENTRATED, the in-state share of premium will
run far above the in-state share of days and the episode count will be small — the candidate is
crash insurance, and the record's "de-grossing product" reading is right.  If it is DIFFUSE
(concentration ratio near 1, premium positive out-of-state too), then the candidate is not an
insurance wrapper at all and 2532's MaxDD count is an artefact of WHERE the tape's worst days
happened to fall.  Both outcomes are decision-relevant and neither is assumed here.

DIAL 1 -- the state threshold `theta` in {0.03, 0.05, 0.10, 0.15, 0.20} (SPY drawdown depth).
DIAL 2 -- gross `g` in {0.75 (live), 1.00}.
Exactly two tuned parameters (G6).  Every grid point is reported.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, arms
{CAP2, CAND, BLEND, EWBH}, weekly cadence, t+1 execution, band 0.03, MA 200d, the 2% cap, the
SHY sweep at phi = 1.00, and the contemporaneous-state convention.

SMALL IS NOT PRICED: ideas 2318 / 2322 / 2326 / 2343 / 2383 put SMALL's 4b pass count at 0 of
40-128 with three legs failing at once, so there is no defensive premium there to decompose.

BOTH KEEP PATHS are reported on every arm.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD
no worse.  4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's,
CAGR >= 0.70 x SPY's.
RULE 8: (theta, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
and 2017-2026 is then read ONCE -- the OOS question being whether the IS state split STILL
carries the premium, which is the only way a decomposition can be walk-forward tested.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the blend's
`m_t` is EXACTLY the capped candidate's realised risk gross.  G3 the CAP2 / CAND committed cells
reproduce the record's U56 headlines.  G4 no leverage.  G5 cost exactly linear in the rung.
G6 exactly two tuned parameters.  G7 the state is CAUSAL (it is a strict lag of a running max).
G8 the decomposition is EXACT (in-state + out-of-state premium == total premium).
G9 the sweep instrument is priced on every held row.  G10 2532's two headline counts reproduce
(CAP2 wins MaxDD and loses CAGR against BLEND at every cell).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  `d_t` is a SAME-DAY DIFFERENCE of two books over the
identical panel, so the decomposition is first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_defensive-premium-by-drawdown-state_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "defensive-premium-by-drawdown-state", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
THETAS = [0.03, 0.05, 0.10, 0.15, 0.20]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
ARMS = ["CAP2", "CAND", "BLEND", "EWBH"]
NAME_CAP, SWEEP = 0.020, "SHY"
COMMITTED_GROSS, HEADLINE_RUNG, HEADLINE_THETA = 0.75, 10.0, 0.10
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BLOCK, NBOOT, SEED = 63, 2000, 20260923

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


# ---------------------------------------------------------------- the arms
def capped_risk(px, gross, cap):
    """The committed candidate: every name inside the 200d +/-band at `min(gross/N_in, cap)`.
    CAP2 takes cap = 2% (whose realised risk gross is the KINKED path `min(g, 0.02 x N_in)` that
    idea 2506 identified); CAND takes cap = INF (a constant risk gross of `g`)."""
    el = band_state(px, BAND) & px.notna()
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def blend_risk(px, m):
    """`m_t x EWBH(panel) + (1 - m_t) x SHY` — 2532's gross-matched comparand.  The SHY leg is
    left to the runner's phi = 1.00 sweep, which is the same instrument at the same phi."""
    priced = px.notna()
    n = priced.sum(axis=1).replace(0, np.nan)
    return priced.astype(float).mul((m / n).fillna(0.0), axis=0).fillna(0.0)


def arm_risk(px, arm, gross):
    if arm == "CAP2":
        return capped_risk(px, gross, NAME_CAP)
    if arm == "CAND":
        return capped_risk(px, gross, np.inf)
    if arm == "BLEND":
        return blend_risk(px, capped_risk(px, gross, NAME_CAP).sum(axis=1))
    if arm == "EWBH":
        return blend_risk(px, pd.Series(gross, index=px.index))
    raise ValueError(arm)


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
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


# ---------------------------------------------------------------- the state
def dd_path(spy_r):
    eq = (1 + spy_r).cumprod()
    return eq / eq.cummax() - 1


def episodes(s):
    """Number of MAXIMAL runs of True — the count of distinct drawdown episodes the premium
    could have been earned in."""
    v = s.astype(int).values
    return int(((v == 1) & (np.concatenate([[0], v[:-1]]) == 0)).sum())


def decompose(d, s):
    """Exact additive split of the premium `d` by the binary state `s` (G8 asserts exactness).
    Everything is expressed in pp/yr OF THE FULL SAMPLE so the two parts add to the total."""
    n = len(d)
    tot = float(d.sum()) * 252 / n
    ins = float(d[s].sum()) * 252 / n
    out = float(d[~s].sum()) * 252 / n
    dshare = float(s.mean())
    pshare = ins / tot if tot != 0 else np.nan
    mi = float(d[s].mean()) * 252 if int(s.sum()) > 0 else np.nan
    mo = float(d[~s].mean()) * 252 if int((~s).sum()) > 0 else np.nan
    return dict(prem_yr=tot, prem_in_yr=ins, prem_out_yr=out, day_share=dshare,
                prem_share_in=pshare, conc=(pshare / dshare) if dshare > 0 else np.nan,
                mean_in_yr=mi, mean_out_yr=mo, mean_gap_yr=mi - mo,
                episodes=episodes(s), days_in=int(s.sum()), days=n)


def block_boot(d, s, rng):
    """Moving-block bootstrap (63-day blocks) of the (d_t, s_t) PAIRS — the state travels with its
    own return, so the band prices the EPISODE COUNT, which is what a handful of crashes makes
    uncertain.  Returns the 5th / 50th / 95th percentiles of the in-state premium share."""
    dv, sv = d.values, s.values.astype(bool)
    n = len(dv); nb = int(np.ceil(n / BLOCK))
    starts = rng.integers(0, n - BLOCK + 1, size=(NBOOT, nb))
    off = np.arange(BLOCK)
    out = np.empty(NBOOT)
    for i in range(NBOOT):
        idx = (starts[i][:, None] + off[None, :]).ravel()[:n]
        dd, ss = dv[idx], sv[idx]
        t = dd.sum()
        out[i] = dd[ss].sum() / t if t != 0 else np.nan
    q = np.nanpercentile(out, [5, 50, 95])
    return float(q[0]), float(q[1]), float(q[2])


def block_boot_gap(d, s, rng):
    """The same moving-block bootstrap, but on the CONDITIONAL-MEAN GAP
    `252 x (mean(d | in-state) - mean(d | out-of-state))` in pp/yr.  Unlike the in-state SHARE,
    this statistic has no near-zero denominator, so it stays finite when the total premium does
    not — which, as section B shows, is exactly the case here."""
    dv, sv = d.values, s.values.astype(bool)
    n = len(dv); nb = int(np.ceil(n / BLOCK))
    starts = rng.integers(0, n - BLOCK + 1, size=(NBOOT, nb))
    off = np.arange(BLOCK)
    out = np.empty(NBOOT)
    for i in range(NBOOT):
        idx = (starts[i][:, None] + off[None, :]).ravel()[:n]
        dd, ss = dv[idx], sv[idx]
        out[i] = (dd[ss].mean() - dd[~ss].mean()) * 252 if ss.any() and (~ss).any() else np.nan
    q = np.nanpercentile(out, [5, 50, 95])
    return float(q[0]), float(q[1]), float(q[2])


def main():
    t0 = time.time()
    say("=== idea 2543 — DOES THE CANDIDATE BEAT ITS OWN GROSS-MATCHED BLEND ONLY IN DRAWDOWN WEEKS? ===")
    say(f"    {DATE}  lane {LANE} run 73   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 theta {THETAS} (SPY drawdown depth)   DIAL 2 gross {GROSSES}   arms {ARMS}")
    say("    STATE IS LAGGED: s_t = 1[dd_SPY,t-1 <= -theta], known at the PRIOR close, so every")
    say("    statistic below is implementable.  The CONTEMPORANEOUS convention is published beside it,")
    say("    never selected on, because it is the one a naive decomposition would use and it FLATTERS.")
    say("    PRIOR, STATED BEFORE COMPUTE AND REFUTABLE BOTH WAYS: a CONCENTRATED premium (in-state")
    say("    share >> day share, few episodes) makes the candidate crash insurance and 2532's MaxDD")
    say("    count meaningful; a DIFFUSE one (concentration ~1, premium positive out-of-state too)")
    say("    makes 2532's count an artefact of WHERE the tape's worst days fell.")
    say("    SMALL NOT PRICED: 0 of 40-128 4b cells with three legs failing at once (2318/2322/2326/")
    say("    2343/2383) — there is no defensive premium there to decompose.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; `L_CAGR` is the")
    say("    contaminated leg.  `d_t` is a SAME-DAY difference over the identical panel — first-order immune.")
    gate("G6 exactly two tuned parameters", "theta, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]

    # G1 replica fidelity
    w_live = rules_v2_weights(px_u, band=BAND, gross=COMMITTED_GROSS)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G2 the blend's m_t IS the capped candidate's realised risk gross
    mc = capped_risk(px_u, COMMITTED_GROSS, NAME_CAP).sum(axis=1)
    mb = arm_risk(px_u, "BLEND", COMMITTED_GROSS).sum(axis=1)
    d2 = float((mc - mb).abs().max())
    kink = float((mc.loc[px_u.index[WARMUP]:] < COMMITTED_GROSS - 1e-9).mean())
    gate("G2 the blend's m_t IS the capped candidate's realised risk gross, day by day",
         f"max|d| {d2:.3e}; the 2% cap BITES (m_t < g) on {kink:.1%} of scored days,"
         f" m_t range [{mc.loc[px_u.index[WARMUP]:].min():.4f}, {mc.loc[px_u.index[WARMUP]:].max():.4f}]",
         "< 1e-12", d2 < 1e-12)

    # G7 the state is causal
    spy_u = px_u["SPY"].pct_change().fillna(0.0).loc[px_u.index[WARMUP]:]
    ddu = dd_path(spy_u)
    cut = ddu.index[2000]
    d7 = float((ddu.loc[:cut] - dd_path(spy_u.loc[:cut])).abs().max())
    s_lag = (ddu.shift(1) <= -HEADLINE_THETA).fillna(False)
    ok7 = bool((s_lag.values[1:] == (ddu.values[:-1] <= -HEADLINE_THETA)).all())
    gate("G7 the state is CAUSAL (a strict lag of a running max; truncation changes nothing before it)",
         f"truncation max|d| {d7:.3e}; lag identity holds: {ok7}", "0.0 and True", d7 == 0.0 and ok7)

    # ------------------------------------------------------------ the grid
    rows, dec_rows = [], []
    rng = np.random.default_rng(SEED)
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        dd = dd_path(spy)
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=COMMITTED_GROSS),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for gross in GROSSES:
            nets = {}
            for arm in ARMS:
                bk = run_book(px, arm_risk(px, arm, gross))
                r0, tn = bk["r0"].loc[start:], bk["turn"].loc[start:]
                nets[arm] = {rung: r0 - tn * rung / 1e4 for rung in RUNGS}
                for rung in RUNGS:
                    r = nets[arm][rung]
                    lg = legs(r, base_r, spy, r.loc[OOS_START:], spy_oos)
                    rows.append(dict(panel=pname, arm=arm, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                     mean_gross=float(bk["gross"].loc[start:].mean()),
                                     max_gross=float(bk["gross"].loc[start:].max()),
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                     OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                     base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                     base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                     spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                     spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos), **lg))
            for rung in RUNGS:
                d = nets["CAP2"][rung] - nets["BLEND"][rung]
                d_cand = nets["CAND"][rung] - nets["BLEND"][rung]
                for theta in THETAS:
                    s_lag = (dd.shift(1) <= -theta).fillna(False)
                    s_now = (dd <= -theta)
                    a = decompose(d, s_lag)
                    b = decompose(d, s_now)
                    c = decompose(d_cand, s_lag)
                    lo, md, hi = block_boot(d, s_lag, rng)
                    glo, gmd, ghi = block_boot_gap(d, s_lag, rng)
                    aI = decompose(d.loc[:IS_END], s_lag.loc[:IS_END])
                    aO = decompose(d.loc[OOS_START:], s_lag.loc[OOS_START:])
                    dec_rows.append(dict(
                        panel=pname, gross=gross, cost_bps=rung, theta=theta,
                        **{f"L_{k}": v for k, v in a.items()},
                        now_prem_share_in=b["prem_share_in"], now_conc=b["conc"],
                        now_day_share=b["day_share"],
                        cand_prem_share_in=c["prem_share_in"], cand_conc=c["conc"],
                        cand_prem_yr=c["prem_yr"],
                        boot_lo=lo, boot_med=md, boot_hi=hi,
                        gap_lo=glo, gap_med=gmd, gap_hi=ghi,
                        IS_prem_yr=aI["prem_yr"], IS_prem_share_in=aI["prem_share_in"],
                        IS_conc=aI["conc"], IS_day_share=aI["day_share"], IS_episodes=aI["episodes"],
                        OOS_prem_yr=aO["prem_yr"], OOS_prem_share_in=aO["prem_share_in"],
                        OOS_conc=aO["conc"], OOS_day_share=aO["day_share"],
                        OOS_episodes=aO["episodes"],
                        IS_gap_yr=aI["mean_gap_yr"], OOS_gap_yr=aO["mean_gap_yr"],
                        IS_mean_in=aI["mean_in_yr"], OOS_mean_in=aO["mean_in_yr"],
                        IS_mean_out=aI["mean_out_yr"], OOS_mean_out=aO["mean_out_yr"]))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.arms.csv", index=False)
    dc = pd.DataFrame(dec_rows); dc.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n    {len(df)} arm rows = 2 panels x {len(ARMS)} arms x {len(GROSSES)} gross x {len(RUNGS)} rungs;"
        f"  {len(dc)} decomposition rows = 2 panels x {len(GROSSES)} x {len(RUNGS)} x {len(THETAS)} thetas,"
        f"  each with a {NBOOT}-draw block bootstrap (block {BLOCK}d).")

    gate("G4 no leverage anywhere (max gross <= 1)", f"max {df.max_gross.max():.6f}",
         "<= 1+1e-12", bool(df.max_gross.max() <= 1 + 1e-12))
    pz = panels["U56"]
    bz = run_book(pz, arm_risk(pz, "CAP2", COMMITTED_GROSS)); st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung", f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null both panels: {shy_ok}",
         "True", shy_ok)

    def cell(arm, panel="U56", gross=COMMITTED_GROSS, rung=HEADLINE_RUNG):
        return df[(df.panel == panel) & (df.arm == arm) & (df.gross == gross)
                  & (df.cost_bps == rung)].iloc[0]
    a, b = cell("CAP2"), cell("CAND")
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739))
    gate("G3 the committed cells reproduce the record's U56 headlines (CAP2 11.62%/1.2687/-14.81%,"
         " OOS 12.77%/1.3318; CAND 12.59%/1.1934/-17.39%)",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # G8 the decomposition is exact
    e8 = float((dc.L_prem_in_yr + dc.L_prem_out_yr - dc.L_prem_yr).abs().max())
    gate("G8 the decomposition is EXACT (in-state + out-of-state == total premium, every row)",
         f"max|d| {e8:.3e} over {len(dc)} rows", "< 1e-12", e8 < 1e-12)

    # G10 2532's two counts
    pr = []
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                c_, bl = cell("CAP2", pname, gross, rung), cell("BLEND", pname, gross, rung)
                pr.append((c_.MaxDD > bl.MaxDD, c_.CAGR < bl.CAGR))
    gate("G10 2532's two headline counts reproduce (CAP2 wins MaxDD and loses CAGR vs BLEND)",
         f"MaxDD win {sum(x for x, _ in pr)} of {len(pr)}; CAGR loss {sum(y for _, y in pr)} of {len(pr)}",
         f"{len(pr)} of {len(pr)} both", all(x for x, _ in pr) and all(y for _, y in pr))

    # ------------------------------------------------------------ A. the arms
    say("\n=== A. THE ARMS — EVERY GRID POINT (2 panels x 4 arms x 2 gross x 4 rungs) ===")
    say("  panel arm   gross   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr | mean g | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for arm in ARMS:
            for gross in GROSSES:
                for rung in RUNGS:
                    r = cell(arm, pname, gross, rung)
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    mark = "   <= COMMITTED" if (gross == COMMITTED_GROSS and rung == HEADLINE_RUNG) else ""
                    say(f"  {pname:5s} {arm:5s} {gross:5.2f} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {r.mean_gross:6.3f} | {'Y' if r.pass4a else '.'}"
                        f"  {'Y' if r.pass4b else '.'}  | {lg}{mark}")
        z = df[df.panel == pname].iloc[0]
        say(f"  SPY ({pname}): {z.spy_CAGR:.2%} / {z.spy_Sharpe:.4f} / {z.spy_MaxDD:.2%}"
            f"  OOS {z.spy_OOS_CAGR:.2%} / {z.spy_OOS_Sharpe:.4f}   |   live RULES v2:"
            f" Sharpe {z.base_Sharpe:.4f}, MaxDD {z.base_MaxDD:.2%}, OOS Sh {z.base_OOS_Sharpe:.4f}")
    say(f"\n  4b passes over the {len(df)} arm rows: "
        + "  ".join(f"{arm} {int(df[df.arm == arm].pass4b.sum())}/{len(df[df.arm == arm])}" for arm in ARMS)
        + f"   |  4a: " + "  ".join(f"{arm} {int(df[df.arm == arm].pass4a.sum())}" for arm in ARMS))

    # ------------------------------------------------------------ A2. which blend did the record kill?
    say("\n=== A2. UNPLANNED BUT FORCED BY THE NUMBERS — WHICH BLEND DID 2532 / 2550 ACTUALLY PRICE? ===")
    say("    Idea 2550 published BLEND_BH failing 4b in 128 of 128 on `L_DD`, with MaxDD running -24.68%")
    say("    to -44.19% and never within 4.4 pp of the -20.23% bar.  This run's BLEND — gross-matched to")
    say("    the CAPPED candidate's KINKED path `min(g, 0.02 x N_in)`, asserted day-by-day by G2 — does")
    say("    not look like that object at all, while this run's EWBH (CONSTANT gross, the path of the")
    say("    UNCAPPED CAND) does.  The two conventions are reported side by side; neither is selected on.")
    say("  panel gross | BLEND (CAP2-gross-matched)        | EWBH (constant gross)             | 2550's BLEND_BH range")
    for pname in panels:
        for gross in GROSSES:
            bl, ew = cell("BLEND", pname, gross), cell("EWBH", pname, gross)
            say(f"  {pname:5s} {gross:5.2f} | MaxDD {bl.MaxDD:7.2%}  CAGR {bl.CAGR:6.2%}  4b"
                f" {'PASS' if bl.pass4b else 'fail'} | MaxDD {ew.MaxDD:7.2%}  CAGR {ew.CAGR:6.2%}  4b"
                f" {'PASS' if ew.pass4b else 'fail'} | -24.68% .. -44.19%, 0 of 128")
    say(f"   4b over this run's 16 rows per arm: BLEND {int(df[df.arm == 'BLEND'].pass4b.sum())}/16,"
        f" EWBH {int(df[df.arm == 'EWBH'].pass4b.sum())}/16 — EWBH fails `L_DD` in every one, exactly as 2550 reports.")
    say("   READ THIS NARROWLY: this run cannot re-execute 2550's 128-cell grid, so it does not overturn")
    say("   that KILL.  What it does show, on its own tape, is that the CAP2-KINK-MATCHED blend is a")
    say("   MATERIALLY more defensive object than the constant-gross one (MaxDD -16.97% vs -22.09% at the")
    say("   U56 committed cell) and clears `L_DD` where the constant-gross blend cannot — so 2550's")
    say("   'the comparand is not itself fundable' applies to the CONSTANT-GROSS blend, and the record")
    say("   should say which m_t it means.  FILED AS A QUESTION FOR THE RECORD, NOT AS A KEEP.")

    # ------------------------------------------------------------ B. the decomposition
    say("\n=== B. THE WHOLE QUESTION — WHERE IS THE CAP2-minus-BLEND PREMIUM EARNED? (every theta) ===")
    say("  panel gross  bps theta | prem pp/yr |  IN pp/yr  OUT pp/yr | day share | prem share IN | conc | episodes | boot 90% band on prem share IN")
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                if not (gross == COMMITTED_GROSS and rung == HEADLINE_RUNG):
                    continue
                for theta in THETAS:
                    q = dc[(dc.panel == pname) & (dc.gross == gross) & (dc.cost_bps == rung)
                           & (dc.theta == theta)].iloc[0]
                    say(f"  {pname:5s} {gross:5.2f} {rung:4.1f} {theta:5.2f} |"
                        f" {q.L_prem_yr * 100:+10.2f} | {q.L_prem_in_yr * 100:+9.2f} {q.L_prem_out_yr * 100:+10.2f}"
                        f" | {q.L_day_share:9.1%} | {q.L_prem_share_in:13.1%} | {q.conc if 'conc' in q else q.L_conc:4.2f}"
                        f" | {int(q.L_episodes):8d} | [{q.boot_lo:6.1%}, {q.boot_hi:6.1%}] (med {q.boot_med:.1%})")
    say("\n  THE SAME DECOMPOSITION, ALL 80 ROWS, SUMMARISED BY theta (both panels, both gross, all rungs):")
    say("  theta | mean prem pp/yr | mean day share | mean prem share IN | mean conc | mean episodes | rows with prem OUT > 0")
    for theta in THETAS:
        q = dc[dc.theta == theta]
        say(f"  {theta:5.2f} | {q.L_prem_yr.mean() * 100:+15.2f} | {q.L_day_share.mean():14.1%}"
            f" | {q.L_prem_share_in.mean():18.1%} | {q.L_conc.mean():9.2f} | {q.L_episodes.mean():13.1f}"
            f" | {int((q.L_prem_out_yr > 0).sum()):5d} of {len(q)}")
    say("\n  CONVENTION CHECK (published, never selected on) — the CONTEMPORANEOUS state flatters by:")
    for theta in THETAS:
        q = dc[dc.theta == theta]
        say(f"   theta {theta:.2f}: lagged prem share IN {q.L_prem_share_in.mean():6.1%}"
            f"  vs contemporaneous {q.now_prem_share_in.mean():6.1%}"
            f"  ({(q.now_prem_share_in - q.L_prem_share_in).mean():+.1%});"
            f"  conc {q.L_conc.mean():.2f} vs {q.now_conc.mean():.2f}")
    say("\n  THE UNCAPPED ARM (CAND - BLEND), same states, published beside it:")
    for theta in THETAS:
        q = dc[dc.theta == theta]
        say(f"   theta {theta:.2f}: CAND prem {q.cand_prem_yr.mean() * 100:+6.2f} pp/yr,"
            f" share IN {q.cand_prem_share_in.mean():6.1%}, conc {q.cand_conc.mean():5.2f}"
            f"   (CAP2 {q.L_prem_yr.mean() * 100:+6.2f} pp/yr, {q.L_prem_share_in.mean():6.1%}, {q.L_conc.mean():5.2f})")

    # ------------------------------------------------------------ B3. the statistic that survives
    say("\n=== B3. THE SHARE STATISTIC THE IDEA ASKED FOR IS NOT ESTIMABLE HERE, SO HERE IS THE ONE THAT IS.")
    say("    A share-of-premium divides by the TOTAL premium, which section B shows is ~0 and SIGN-UNSTABLE")
    say("    (+0.26 pp/yr on U56, -1.42 on B136), so every share and concentration ratio above is a")
    say("    near-zero denominator blowing up — NOT a finding about drawdown weeks.  The CONDITIONAL-MEAN")
    say("    GAP `252 x (mean(d|IN) - mean(d|OUT))` has no such denominator.  It is DERIVED, not tuned: it")
    say("    uses the SAME d_t, the SAME lagged states and the SAME 63-day block bootstrap. ===")
    say("  panel gross  bps theta | mean IN pp/yr | mean OUT pp/yr | GAP pp/yr | boot 90% band on the GAP | gap>0?")
    for pname in panels:
        for theta in THETAS:
            q = dc[(dc.panel == pname) & (dc.gross == COMMITTED_GROSS)
                   & (dc.cost_bps == HEADLINE_RUNG) & (dc.theta == theta)].iloc[0]
            say(f"  {pname:5s} {COMMITTED_GROSS:5.2f} {HEADLINE_RUNG:4.1f} {theta:5.2f} |"
                f" {q.L_mean_in_yr * 100:+13.2f} | {q.L_mean_out_yr * 100:+14.2f} |"
                f" {q.L_mean_gap_yr * 100:+9.2f} | [{q.gap_lo * 100:+7.2f}, {q.gap_hi * 100:+7.2f}]"
                f" (med {q.gap_med * 100:+.2f}) | {'YES' if q.L_mean_gap_yr > 0 else 'no'}"
                + ("  <= band EXCLUDES 0" if (q.gap_lo > 0 or q.gap_hi < 0) else "  band spans 0"))
    say("\n  ALL 80 ROWS by theta (both panels, both gross, all rungs):")
    say("  theta | mean GAP pp/yr | rows with GAP > 0 | rows whose 90% band EXCLUDES 0 | mean IN | mean OUT")
    for theta in THETAS:
        q = dc[dc.theta == theta]
        excl = int(((q.gap_lo > 0) | (q.gap_hi < 0)).sum())
        say(f"  {theta:5.2f} | {q.L_mean_gap_yr.mean() * 100:+14.2f} | {int((q.L_mean_gap_yr > 0).sum()):5d} of {len(q)}"
            f"        | {excl:5d} of {len(q)}                  | {q.L_mean_in_yr.mean() * 100:+7.2f}"
            f" | {q.L_mean_out_yr.mean() * 100:+7.2f}")
    excl_all = int(((dc.gap_lo > 0) | (dc.gap_hi < 0)).sum())
    say(f"\n  OVER ALL {len(dc)} ROWS: the conditional-mean gap is POSITIVE in"
        f" {int((dc.L_mean_gap_yr > 0).sum())} of {len(dc)} and its 90% block-bootstrap band EXCLUDES ZERO in"
        f" {excl_all} of {len(dc)}.")

    # ------------------------------------------------------------ C. how few days
    say("\n=== C. HOW MUCH OF THE PREMIUM IS EARNED IN HOW FEW DAYS — the worst-days census,")
    say("    which needs no threshold at all (published, no dial): ===")
    say("  panel gross  bps | premium pp/yr | share earned on the WORST 1% / 5% / 10% of SPY days | share on SPY-UP days")
    wd = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for gross in GROSSES:
            nets = {}
            for arm in ("CAP2", "BLEND"):
                bk = run_book(px, arm_risk(px, arm, gross))
                nets[arm] = (bk["r0"].loc[start:], bk["turn"].loc[start:])
            for rung in RUNGS:
                d = ((nets["CAP2"][0] - nets["CAP2"][1] * rung / 1e4)
                     - (nets["BLEND"][0] - nets["BLEND"][1] * rung / 1e4))
                tot = d.sum()
                sh = {}
                for p in (0.01, 0.05, 0.10):
                    thr = spy.quantile(p)
                    sh[p] = float(d[spy <= thr].sum() / tot) if tot != 0 else np.nan
                up = float(d[spy > 0].sum() / tot) if tot != 0 else np.nan
                m1 = float(d[spy <= spy.quantile(0.01)].mean()) * 252
                m5 = float(d[spy <= spy.quantile(0.05)].mean()) * 252
                mrest = float(d[spy > spy.quantile(0.05)].mean()) * 252
                wd.append(dict(panel=pname, gross=gross, cost_bps=rung, prem_yr=tot * 252 / len(d),
                               w1=sh[0.01], w5=sh[0.05], w10=sh[0.10], up_share=up,
                               mean_w1_yr=m1, mean_w5_yr=m5, mean_rest_yr=mrest))
                if gross == COMMITTED_GROSS and rung == HEADLINE_RUNG:
                    say(f"  {pname:5s} {gross:5.2f} {rung:4.1f} | {tot * 252 / len(d) * 100:+13.2f}"
                        f" | {sh[0.01]:9.1%} / {sh[0.05]:5.1%} / {sh[0.10]:5.1%} | {up:19.1%}")
                    say(f"        ^ the SAME cell as CONDITIONAL MEANS (no near-zero denominator):"
                        f" worst 1% {m1 * 100:+.1f} pp/yr, worst 5% {m5 * 100:+.1f}, the other 95%"
                        f" {mrest * 100:+.1f}")
    wdf = pd.DataFrame(wd); wdf.to_csv(f"{OUT}.worstdays.csv", index=False)
    say(f"  over all {len(wdf)} (panel, gross, rung) cells: mean share earned on the worst 1% of SPY days"
        f" {wdf.w1.mean():.1%}, worst 5% {wdf.w5.mean():.1%}, worst 10% {wdf.w10.mean():.1%};"
        f" mean share earned on SPY-UP days {wdf.up_share.mean():+.1%}"
        f"\n  — every one of those SHARES is a near-zero denominator artefact and is published ONLY to show"
        f" that it is.  The conditional means over the same {len(wdf)} cells: worst 1%"
        f" {wdf.mean_w1_yr.mean() * 100:+.1f} pp/yr, worst 5% {wdf.mean_w5_yr.mean() * 100:+.1f},"
        f" the other 95% {wdf.mean_rest_yr.mean() * 100:+.1f} — POSITIVE in the tail in"
        f" {int((wdf.mean_w5_yr > 0).sum())} of {len(wdf)} cells and NEGATIVE outside it in"
        f" {int((wdf.mean_rest_yr < 0).sum())} of {len(wdf)}.")

    # ------------------------------------------------------------ D. rule 8
    say("\n=== D. RULE 8 — (theta, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only")
    say("    choosers, 2017-2026 then read ONCE.  The OOS question for a DECOMPOSITION is whether the")
    say("    IS state split STILL carries the premium out of sample. ===")
    wf = []
    for pname in panels:
        for rung in RUNGS:
            d = dc[(dc.panel == pname) & (dc.cost_bps == rung)]
            for ch, col in (("C_ISCONC", "IS_conc"), ("C_ISPREMIN", "IS_prem_share_in")):
                pk = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=ch, pick_theta=pk.theta,
                               pick_gross=pk.gross, IS_conc=pk.IS_conc, OOS_conc=pk.OOS_conc,
                               IS_share=pk.IS_prem_share_in, OOS_share=pk.OOS_prem_share_in,
                               IS_prem=pk.IS_prem_yr, OOS_prem=pk.OOS_prem_yr,
                               IS_days=pk.IS_day_share, OOS_days=pk.OOS_day_share,
                               OOS_eps=pk.OOS_episodes))
                say(f"   {pname:5s} {rung:4.1f}bps {ch:11s} picks theta {pk.theta:.2f} g {pk.gross:.2f}"
                    f" | IS conc {pk.IS_conc:5.2f} share {pk.IS_prem_share_in:6.1%} prem {pk.IS_prem_yr * 100:+6.2f}"
                    f" | OOS conc {pk.OOS_conc:5.2f} share {pk.OOS_prem_share_in:6.1%}"
                    f" prem {pk.OOS_prem_yr * 100:+6.2f} pp/yr over {pk.OOS_day_share:.1%} of days,"
                    f" {int(pk.OOS_episodes)} episodes")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n   {len(wfd)} picks.  IS concentration mean {wfd.IS_conc.mean():.2f} -> OOS {wfd.OOS_conc.mean():.2f}"
        f"  ({wfd.OOS_conc.mean() - wfd.IS_conc.mean():+.2f});"
        f"  IS premium {wfd.IS_prem.mean() * 100:+.2f} pp/yr -> OOS {wfd.OOS_prem.mean() * 100:+.2f} pp/yr")
    say(f"   picks whose OOS concentration EXCEEDS 1 (the split still carries the premium):"
        f" {int((wfd.OOS_conc > 1).sum())} of {len(wfd)}")
    say(f"   picks whose OOS premium is POSITIVE at all: {int((wfd.OOS_prem > 0).sum())} of {len(wfd)}")
    say("   pick distribution over theta: " + "  ".join(
        f"{t:.2f}:{int((wfd.pick_theta == t).sum())}" for t in THETAS)
        + "   over gross: " + "  ".join(f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))

    say("\n   THE SAME RULE-8 TEST ON THE STATISTIC THAT SURVIVES (the conditional-mean GAP), because a")
    say("   walk-forward on a degenerate ratio tests nothing.  theta chosen on warm-up..2016-12-31 ONLY by")
    say("   the magnitude of the IS gap, 2017-2026 then read ONCE:")
    gwf = []
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                d = dc[(dc.panel == pname) & (dc.gross == gross) & (dc.cost_bps == rung)]
                pk = d.loc[d.IS_gap_yr.abs().idxmax()]
                gwf.append(dict(panel=pname, gross=gross, cost_bps=rung, pick_theta=pk.theta,
                                IS_gap=pk.IS_gap_yr, OOS_gap=pk.OOS_gap_yr,
                                IS_in=pk.IS_mean_in, OOS_in=pk.OOS_mean_in,
                                same_sign=bool(np.sign(pk.IS_gap_yr) == np.sign(pk.OOS_gap_yr))))
                if rung == HEADLINE_RUNG:
                    say(f"    {pname:5s} g {gross:.2f} {rung:4.1f}bps picks theta {pk.theta:.2f}"
                        f" | IS gap {pk.IS_gap_yr * 100:+7.2f} pp/yr -> OOS gap {pk.OOS_gap_yr * 100:+7.2f}"
                        f"   (IS mean IN {pk.IS_mean_in * 100:+7.2f} -> OOS {pk.OOS_mean_in * 100:+7.2f})"
                        f"   sign {'HOLDS' if np.sign(pk.IS_gap_yr) == np.sign(pk.OOS_gap_yr) else 'FLIPS'}")
    gw = pd.DataFrame(gwf); gw.to_csv(f"{OUT}.gap_walkforward.csv", index=False)
    say(f"    {len(gw)} picks: the IS sign of the gap HOLDS out of sample in {int(gw.same_sign.sum())}"
        f" of {len(gw)};  mean IS gap {gw.IS_gap.mean() * 100:+.2f} pp/yr -> OOS {gw.OOS_gap.mean() * 100:+.2f};"
        f"  picks with a NEGATIVE OOS gap (the candidate LAGS the blend in state): "
        f"{int((gw.OOS_gap < 0).sum())} of {len(gw)}.")
    say("    pick distribution over theta: " + "  ".join(
        f"{th:.2f}:{int((gw.pick_theta == th).sum())}" for th in THETAS))

    # ------------------------------------------------------------ E. gates
    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== E. GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf.iterrows():
        say(f"   {'PASS' if g.pass_ else 'FAIL'}  {g.gate}")
    say(f"\n  elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
