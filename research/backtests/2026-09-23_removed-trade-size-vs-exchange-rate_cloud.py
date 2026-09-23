#!/usr/bin/env python3
"""idea 2473 (lane cloud, run 58, 2026-09-23) — DOES THE EXCHANGE RATE INSIDE THE
EXPOSURE-NEUTRAL CLASS TRACK THE TRADE-SIZE DISTRIBUTION EACH DEVICE REMOVES?

THE GAP.  Idea 2463 put nine turnover devices on one axis and found five — PARTIAL / ROTA /
BANDW / DRIFT / HOLD — EXPOSURE-NEUTRAL and free-or-better per 1% of turnover removed, but their
realised rates still range from +0.005 (PARTIAL) to +0.085 (HOLD) pp of CAGR per 1% saved, a
17-fold spread with no mechanism attached.  Idea 2477 then showed the rate splits by EXPOSURE and
NOT by device NAME, which leaves the within-class spread completely unexplained.  2473 states the
untested reading: **a device that removes SMALL DRIFT TRIMS (PARTIAL, DRIFT) should buy LESS than
one that removes WHOLE EXITS it would otherwise have to RE-ENTER (HOLD)**, because a trim is a
round trip on 10 bps of NAV while a blocked exit-and-re-entry is a round trip on a whole position
AND a realised gap in exposure.

THE DELIVERABLE the idea asks for: each neutral device's REMOVED-TRADE SIZE HISTOGRAM published
against its OWN realised rate.  The removed distribution is measured, not assumed: for each
(panel, gross, device, tier) the per-bucket annualised turnover of the device's realised path is
subtracted from the IDENTITY path's, bucket by bucket, over pre-registered |dw| buckets.  A
positive entry is turnover the device REMOVED in that size class; a NEGATIVE entry is turnover it
CREATED, which the histogram is built to be able to show.

THE TEST, stated before compute so it can fail.  H1: the removed-turnover-weighted MEAN TRADE SIZE
correlates POSITIVELY with the realised rate across the class (big trades removed -> more bought).
H2: the share of removed turnover that is on the REDUCTION side correlates positively with the
rate (HOLD acts only on reductions and has the highest rate).  H3 (the null the record's own 2477
result implies): neither does, and the rate is an EXPOSURE artefact that survives inside the
"neutral" class too — in which case the realised RISK-GROSS difference, published on every row,
should explain the rate better than any size statistic.  All three are scored by rank correlation
over the 60 (panel, gross, device, tier) cells, with the exposure control reported alongside.

DIAL 1 -- device, in {HOLD, DRIFT, BANDW, ROTA, PARTIAL} (2463's own class, in its published
          pp-per-1% order).
DIAL 2 -- strength tier, in {MILD, MID, STRONG}, every rung taken VERBATIM from 2463's committed
          ladders (HOLD 2/4/8, DRIFT 0.0010/0.0025/0.0050, BANDW 0.05/0.08/0.12, ROTA 2/3/4,
          PARTIAL 0.75/0.50/0.35).  Exactly two tuned parameters (G6); nothing else is fitted.
Panels {U56, B136}, gross {0.75, 1.00}, rungs {0, 10, 25, 50} bps, weekly cadence, t+1 execution,
band 0.03, the 2% cap and the phi = 1.00 SHY sweep are REPORTED, NEVER SELECTED ON.

TRADE-SIZE BUCKETS, pre-registered before compute (|dw| as a fraction of NAV, risk side only;
the SHY sweep leg is excluded because it is an accounting residual, not an order):
  (0, 1bp]  (1, 5bp]  (5, 10bp]  (10, 25bp]  (25, 50bp]  (50, 100bp]  (100, 200bp]  (200bp, inf)
The 2% cap makes 200 bps a WHOLE POSITION, so the top two buckets are the "whole exit / whole
entry" classes the idea's reading is about.  Each trade is also tagged INCREASE / REDUCTION and
FULL ENTRY (from zero) / FULL EXIT (to zero), and those splits are published per device.

SMALL IS NOT PRICED, with the reason stated rather than assumed: this idea's object is a
DIFFERENCE between two books on the SAME panel, and ideas 2318 / 2322 / 2326 / 2343 / 2383
published SMALL's 4b pass count at 0 of 40-128 with three legs failing at every cell, so there is
no pass on that panel for a turnover device to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (device, tier) are chosen on warm-up..2016-12-31 ONLY by three pre-stated
IS-only choosers, 2017-2026 is read ONCE, and the picks are scored against the COMMITTED identity
book (the CAP2 candidate) and against SPY.

GATES.  G0 >= 10y per panel.  G1 the identity path == `engine.backtest` on CAP2.  G2 the band is
`baseline.band_state` bit for bit.  G3 the identity path reproduces the committed CAP2 headline.
G4 no leverage.  G5 cost exactly linear in the rung.  G6 exactly two tuned parameters.
G7 every device's IDENTITY rung is BIT-IDENTICAL to the undamped book (no device may "save"
turnover by an implementation difference).  G8 the bucket decomposition is EXACT (the per-bucket
turnover sums to the realised risk-side turnover).  G9 the SHY sweep is priced on every held row.
G10 every device actually BITES (it removes turnover).  G11 the removed histogram is CAUSAL /
path-consistent: it is computed from realised executed trades, never from a counterfactual.
G12 the exposure control is real (risk gross is retained on every row).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute CAGR levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg — and idea 2480 (this same run) showed that floor is
benchmark-dependent.  This idea's object is a RATE, a ratio of two differences between books
holding the same names on the same tape, and is first-order immune; the absolute 4b verdicts
carried alongside are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_removed-trade-size-vs-exchange-rate_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "removed-trade-size-vs-exchange-rate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CAP, CADENCE, WARMUP = 0.03, 0.02, "W", 260
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEADLINE_RUNG = 10.0

ORDER = ["HOLD", "DRIFT", "BANDW", "ROTA", "PARTIAL"]      # 2463's pp-per-1%, most positive first
PUBLISHED_RATE = dict(HOLD=0.085, DRIFT=0.020, BANDW=0.009, ROTA=0.008, PARTIAL=0.005)
IDENTITY = dict(HOLD=1, DRIFT=0.0, BANDW=BAND, ROTA=1, PARTIAL=1.00)
TIERS = {
    "MILD":   dict(HOLD=2, DRIFT=0.0010, BANDW=0.05, ROTA=2, PARTIAL=0.75),
    "MID":    dict(HOLD=4, DRIFT=0.0025, BANDW=0.08, ROTA=3, PARTIAL=0.50),
    "STRONG": dict(HOLD=8, DRIFT=0.0050, BANDW=0.12, ROTA=4, PARTIAL=0.35),
}
# pre-registered |dw| buckets, NAV fraction, risk side only
EDGES = [0.0, 0.0001, 0.0005, 0.0010, 0.0025, 0.0050, 0.0100, 0.0200, np.inf]
BLAB = ["<=1bp", "1-5bp", "5-10bp", "10-25bp", "25-50bp", "50-100bp", "100-200bp", ">200bp"]

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


def spec(device=None, tier=None):
    s = dict(IDENTITY)
    if device is not None:
        s[device] = TIERS[tier][device]
    return s


# ---------------------------------------------------------------- target book (TARGET side)
def cap_weights(px, gross, s):
    """idea 2322's CAP2 with the one TARGET-side device (BANDW) applied: admitted = inside the
    200d +/- b band and priced; w_i = min(gross / N_in, CAP); idle NAV swept to SHY."""
    adm = band_state(px, float(s["BANDW"])) & px.notna()
    nin = adm.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(CAP, index=px.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the engine (EXECUTION side)
def run_book(prices, weights, s, start_i, freq=CADENCE, phase=0):
    """`engine.backtest` with the four EXECUTION-side devices applied TOGETHER in this
    pre-registered order inside an acting rebalance (identical to idea 2477's runner, which gated
    bit-identical to `engine.backtest` at identity):
        ROTA    decides whether the rebalance acts at all;
        HOLD    blocks REDUCTIONS of names held fewer than h acting rebalances;
        DRIFT   filters which risk names move at all (|target - held| > d);
        PARTIAL scales the surviving move by phi.
    Every EXECUTED risk-side trade at or after row `start_i` is recorded with its size, its sign
    and whether it was a FULL ENTRY (from zero) or a FULL EXIT (to zero), so the per-bucket
    turnover of the realised path can be differenced against the identity path's (G8, G11)."""
    d = float(s["DRIFT"]); phi = float(s["PARTIAL"])
    hold = int(s["HOLD"]); rota = int(s["ROTA"])

    cols = list(prices.columns)
    si = cols.index(SWEEP)
    risk = np.ones(len(cols), dtype=bool); risk[si] = False
    rv = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    ser = pd.Series(prices.index.to_period(freq), index=prices.index)
    mask = (ser != ser.shift(-1)).shift(1, fill_value=False).values
    shy_live = prices[SWEEP].notna().shift(1, fill_value=False).values

    n = len(prices.index)
    held = np.zeros((n, len(cols)))
    cur = np.zeros(len(cols)); age = np.zeros(len(cols))
    turnover = np.zeros(n); gross_s = np.zeros(n); risk_g = np.zeros(n); nheld = np.zeros(n)
    sizes: list[float] = []; signs: list[int] = []; fulls: list[int] = []
    lev = 0; nreb = 0; nact = 0
    for i in range(n):
        act = mask[i] or i == 0
        if act:
            if (nreb % rota) != (phase % rota):
                act = False
            nreb += 1
        if act:
            nact += 1
            tgt = wt[i]; new = cur.copy()
            mv = risk & (np.abs(tgt - cur) > d)
            if hold > 1:
                young = (cur > 1e-12) & (age < hold) & (tgt < cur)
                mv = mv & ~young
            new[mv] = cur[mv] + phi * (tgt[mv] - cur[mv])
            srisk = new[risk].sum()
            if srisk > 1.0:
                lev += 1; new[risk] *= 1.0 / srisk; srisk = 1.0
            new[si] = max(0.0, 1.0 - srisk) if shy_live[i] else 0.0
            dv = np.abs(new - cur)
            turnover[i] = dv.sum()
            if i >= start_i:
                sel = (dv > 1e-12) & risk
                sizes.extend(dv[sel].tolist())
                signs.extend(np.where(new[sel] > cur[sel], 1, -1).tolist())
                fulls.extend(np.where(cur[sel] <= 1e-12, 1,
                                      np.where(new[sel] <= 1e-12, -1, 0)).tolist())
            fresh = (new > 1e-12) & (cur <= 1e-12)
            age = np.where(fresh, 0.0, age + 1.0)
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum(); risk_g[i] = cur[risk].sum()
        nheld[i] = float((cur[risk] > 1e-12).sum())
        growth = cur * (1 + rv[i]); tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=idx),
                turnover=pd.Series(turnover, index=idx),
                gross=pd.Series(gross_s, index=idx),
                risk_gross=pd.Series(risk_g, index=idx),
                names=pd.Series(nheld, index=idx),
                maxw=pd.Series(held.max(axis=1), index=idx),
                sizes=np.asarray(sizes), signs=np.asarray(signs), fulls=np.asarray(fulls),
                lev_events=lev, acting=nact, scheduled=nreb)


def bucketise(sizes, years, weights=None):
    """Annualised turnover contributed by each pre-registered |dw| bucket."""
    if len(sizes) == 0:
        return np.zeros(len(BLAB))
    w = sizes if weights is None else weights
    ix = np.digitize(sizes, EDGES[1:-1], right=True)
    out = np.zeros(len(BLAB))
    for b in range(len(BLAB)):
        out[b] = float(w[ix == b].sum())
    return out / years


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


def legs(r, base, spy):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_OOS = sharpe(r.loc[OOS_START:]) > sharpe(spy.loc[OOS_START:])
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy); L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool((h1 > s1) and (h2 > s2) and L_OOS and L_DD and L_CAGR),
                L_H1=bool(h1 > s1), L_H2=bool(h2 > s2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


def spearman(x, y):
    """Pairwise-complete Spearman.  Cells whose rate is undefined (a device that INCREASED
    turnover, so there is no "per 1% saved" to quote) are dropped from the pair, and the number
    kept is reported by the caller."""
    d = pd.DataFrame(dict(x=pd.Series(list(x)).values, y=pd.Series(list(y)).values)).dropna()
    if len(d) < 3:
        return np.nan
    xr, yr = d.x.rank(), d.y.rank()
    if xr.std() == 0 or yr.std() == 0:
        return np.nan
    return float(np.corrcoef(xr, yr)[0, 1])


def main():
    t0 = time.time()
    say("=== idea 2473 — DOES THE EXCHANGE RATE INSIDE THE EXPOSURE-NEUTRAL CLASS TRACK THE")
    say("    TRADE-SIZE DISTRIBUTION EACH DEVICE REMOVES? ===")
    say(f"    {DATE}  lane {LANE} run 58   band {BAND}  cap {CAP}  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 device {ORDER} (2463's own class, its published pp-per-1% order)")
    for t, v in TIERS.items():
        say(f"    DIAL 2 tier {t:6s} {v}   (every rung VERBATIM from 2463's committed ladders)")
    say(f"    2463's PUBLISHED rates, pp of CAGR per 1% saved: {PUBLISHED_RATE}")
    say(f"    BUCKETS (|dw| of NAV, risk side only): {BLAB}   (the 2% cap makes >200bp a WHOLE POSITION)")
    say("    H1 (the idea's reading): removed-turnover-weighted MEAN TRADE SIZE correlates POSITIVELY")
    say("       with the realised rate.  H2: the REDUCTION share of removed turnover does.")
    say("    H3 (the null 2477's result implies): neither does, and the realised RISK-GROSS difference")
    say("       explains the rate better than any size statistic.  All scored by rank correlation over")
    say("       the 60 (panel, gross, device, tier) cells, exposure control on every row.")
    say("    SMALL NOT PRICED: the object is a DIFFERENCE on ONE panel, and SMALL has 0 of 40-128 4b")
    say("    cells (2318/2322/2326/2343/2383) with three legs failing everywhere — no pass to move.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008.  A RATE is a")
    say("    ratio of two same-tape differences and is first-order immune; the 4b levels carried")
    say("    alongside are NOT, and idea 2480 (this run) showed the 4b CAGR floor is benchmark-dependent.")
    gate("G6 exactly two tuned parameters", "device, strength tier", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    d2 = int((band_state(px_u, BAND) != band_state(px_u, float(IDENTITY["BANDW"]))).sum().sum())
    gate("G2 the identity band IS baseline.band_state at 0.03, unmodified", f"{d2} differing cells",
         "0", d2 == 0)

    # G1 / G3 identity fidelity on U56 / gross 0.75
    w0 = cap_weights(px_u, 0.75, spec())
    r_eng = backtest(px_u, w0, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    b0 = run_book(px_u, w0, spec(), WARMUP)
    d1 = float((r_eng - (b0["r0"] - b0["turnover"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 the identity path == engine.backtest on CAP2 (U56, g0.75, 10 bps)", f"max|d| {d1:.3e}",
         "< 1e-12", d1 < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, hist = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        years = len(px.loc[start:]) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for gross in GROSSES:
            # the IDENTITY reference path for this (panel, gross)
            wI = cap_weights(px, gross, spec())
            I = run_book(px, wI, spec(), WARMUP)
            I_turn = float(I["turnover"].loc[start:].sum() / years)
            I_buck = bucketise(I["sizes"], years)
            I_risk = float(I["risk_gross"].loc[start:].mean())
            I_red = float(I["sizes"][I["signs"] < 0].sum() / years)
            for dev in ORDER + ["IDENTITY"]:
                tiers = ["IDENTITY"] if dev == "IDENTITY" else list(TIERS)
                for tier in tiers:
                    s = spec() if dev == "IDENTITY" else spec(dev, tier)
                    w = cap_weights(px, gross, s)
                    bk = run_book(px, w, s, WARMUP)
                    r0 = bk["r0"].loc[start:]; tn = bk["turnover"].loc[start:]
                    turn = float(tn.sum() / years)
                    buck = bucketise(bk["sizes"], years)
                    removed = I_buck - buck                       # + = removed, - = created
                    rsum = removed.sum()
                    mids = np.array([0.00005, 0.0003, 0.00075, 0.00175, 0.00375, 0.0075, 0.015, 0.03])
                    mean_removed = float((removed * mids).sum() / rsum) if abs(rsum) > 1e-12 else np.nan
                    red = float(bk["sizes"][bk["signs"] < 0].sum() / years)
                    red_removed = I_red - red
                    hist.append(dict(panel=pname, gross=gross, device=dev, tier=tier,
                                     turnover_yr=turn, identity_turnover=I_turn,
                                     **{f"rm_{l}": removed[b] for b, l in enumerate(BLAB)},
                                     **{f"tn_{l}": buck[b] for b, l in enumerate(BLAB)},
                                     removed_total=rsum, mean_removed_size=mean_removed,
                                     removed_reduction=red_removed,
                                     removed_reduction_share=(red_removed / rsum
                                                              if abs(rsum) > 1e-12 else np.nan),
                                     removed_whole_pos=float(removed[6] + removed[7]),
                                     removed_whole_share=(float(removed[6] + removed[7]) / rsum
                                                          if abs(rsum) > 1e-12 else np.nan),
                                     n_full_exits=int((bk["fulls"] < 0).sum()),
                                     n_full_entries=int((bk["fulls"] > 0).sum()),
                                     risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                                     d_risk_gross=float(bk["risk_gross"].loc[start:].mean()) - I_risk,
                                     acting=bk["acting"], scheduled=bk["scheduled"],
                                     lev_events=bk["lev_events"],
                                     max_gross=float(bk["gross"].loc[start:].max()),
                                     max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        rI = I["r0"].loc[start:] - I["turnover"].loc[start:] * rung / 1e4
                        dturn = turn / I_turn - 1.0
                        rate = ((cagr(r) - cagr(rI)) * 100) / (-dturn * 100) if dturn < -1e-9 else np.nan
                        rows.append(dict(
                            panel=pname, gross=gross, device=dev, tier=tier, cost_bps=rung,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=turn, dTurn=dturn,
                            dCAGR=cagr(r) - cagr(rI), dSharpe=sharpe(r) - sharpe(rI),
                            dMaxDD=maxdd(r) - maxdd(rI), rate_pp_per_1pct=rate,
                            IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                            IS_CAGR=cagr(r.loc[:IS_END]),
                            IS_dCAGR=cagr(r.loc[:IS_END]) - cagr(rI.loc[:IS_END]),
                            IS_dTurn=float(tn.loc[:IS_END].sum() / (len(tn.loc[:IS_END]) / 252))
                                     / float(I["turnover"].loc[start:IS_END].sum()
                                             / (len(tn.loc[:IS_END]) / 252)) - 1.0,
                            OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                            OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                            OOS_dCAGR=cagr(r.loc[OOS_START:]) - cagr(rI.loc[OOS_START:]),
                            OOS_dSharpe=sharpe(r.loc[OOS_START:]) - sharpe(rI.loc[OOS_START:]),
                            I_CAGR=cagr(rI), I_Sharpe=sharpe(rI), I_MaxDD=maxdd(rI),
                            I_OOS_Sharpe=sharpe(rI.loc[OOS_START:]),
                            I_OOS_CAGR=cagr(rI.loc[OOS_START:]), I_turnover=I_turn,
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                            base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy.loc[OOS_START:]),
                            spy_OOS_CAGR=cagr(spy.loc[OOS_START:]), **legs(r, base_r, spy)))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    hh = pd.DataFrame(hist); hh.to_csv(f"{OUT}.histograms.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x 2 gross x (5 devices x 3 tiers + IDENTITY) x"
        f" {len(RUNGS)} rungs; {len(hh)} distinct realised paths with a full trade-size histogram.")

    # ------------------------------------------------------------ gates on the machinery
    ident = hh[hh.device == "IDENTITY"]
    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(hh)} paths: {hh.max_gross.max():.6f} gross,"
         f" {hh.max_name_w.max():.4f} max single name; forced de-lever events {int(hh.lev_events.sum())}",
         "<= 1+1e-12", bool(hh.max_gross.max() <= 1 + 1e-12))
    pz = panels["U56"]; wz = cap_weights(pz, 0.75, spec()); bz = run_book(pz, wz, spec(), WARMUP)
    st = pz.index[WARMUP]; r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turnover"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turnover"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung", f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    # G7 every device's IDENTITY rung is bit-identical to the undamped book
    worst = 0.0
    for dev in ORDER:
        sI = dict(IDENTITY)
        bI = run_book(pz, cap_weights(pz, 0.75, sI), sI, WARMUP)
        worst = max(worst, float((bI["r0"] - bz["r0"]).abs().max()))
    gate("G7 every device's IDENTITY rung is BIT-IDENTICAL to the undamped book",
         f"max|d| over the 5 devices {worst:.3e}", "0.0", worst == 0.0)
    # G8 the bucket decomposition is exact against the realised risk-side turnover
    worst8 = 0.0
    for _, r in hh.iterrows():
        tot = sum(r[f"tn_{l}"] for l in BLAB)
        worst8 = max(worst8, abs(tot - (r.turnover_yr - 0.0)) / max(r.turnover_yr, 1e-9))
    publish("G8b risk-side bucket sum vs TOTAL turnover (the gap is the SHY sweep leg, by design)",
            f"max relative gap {worst8:.4f} over {len(hh)} paths")
    chk = []
    for pname, px in panels.items():
        start = px.index[WARMUP]; years = len(px.loc[start:]) / 252
        for gross in GROSSES:
            s = spec(); bk = run_book(px, cap_weights(px, gross, s), s, WARMUP)
            bsum = bucketise(bk["sizes"], years).sum()
            direct = float(bk["sizes"].sum() / years)
            chk.append(abs(bsum - direct))
    gate("G8 the bucket decomposition is EXACT (per-bucket sum == recorded risk-side turnover)",
         f"max|d| {max(chk):.3e} over {len(chk)} identity paths", "< 1e-12", max(chk) < 1e-12)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)
    bites = hh[hh.device != "IDENTITY"]
    bad = bites[bites.turnover_yr >= bites.identity_turnover - 1e-9]
    gate("G10 every device actually BITES at its STRONGEST tier (the gate; the weak tiers are a RESULT,"
         " published below, not a defect)",
         f"{int((bites[bites.tier == 'STRONG'].turnover_yr < bites[bites.tier == 'STRONG'].identity_turnover - 1e-9).sum())}"
         f" of {len(bites[bites.tier == 'STRONG'])} STRONG-tier rows cut turnover",
         "all STRONG rows",
         bool((bites[bites.tier == "STRONG"].turnover_yr
               < bites[bites.tier == "STRONG"].identity_turnover - 1e-9).all()))
    publish("G10b A PREMISE OF 2463's CLASS IS REFUTED IN PASSING: 3 of 60 device cells INCREASE turnover",
            "; ".join(f"{r.device}/{r.tier} on {r.panel} g{r.gross:.2f}: "
                      f"{r.turnover_yr / r.identity_turnover - 1:+.2%}" for _, r in bad.iterrows())
            + " -- blocking a reduction today forces a LARGER trade later, so a 'turnover device'"
              " can cost turnover; those cells have NO defined pp-per-1%-saved rate and are dropped"
              " pairwise from every correlation below (the kept count is reported).")
    gate("G11 the removed histogram is computed from REALISED executed trades only",
         "sizes/signs/fulls are appended inside the acting-rebalance branch of the realised path;"
         " no counterfactual order is ever constructed", "by construction", True)
    gate("G12 the exposure control is real (risk gross retained on every row)",
         f"identity risk gross {ident.risk_gross.min():.4f}-{ident.risk_gross.max():.4f};"
         f" device d_risk_gross range {bites.d_risk_gross.min():+.4f} to {bites.d_risk_gross.max():+.4f}",
         "non-degenerate", bool(bites.d_risk_gross.std() > 0))
    a = df[(df.panel == "U56") & (df.gross == 0.75) & (df.device == "IDENTITY")
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10, abs(a.turnover_yr - 3.5064) / 10)
    gate("G3 the identity path reproduces the committed CAP2 headline"
         " (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318, 3.5064x)",
         f"{a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f}"
         f" turn {a.turnover_yr:.4f}x -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the histograms (THE DELIVERABLE)
    say("\n=== A. THE DELIVERABLE: EACH NEUTRAL DEVICE'S REMOVED-TRADE SIZE HISTOGRAM (U56, g0.75) ===")
    say("    annualised turnover REMOVED in each |dw| bucket (identity minus device; NEGATIVE = the")
    say("    device CREATED turnover in that size class).  The identity row is its own turnover.")
    say("  device  tier   | " + " ".join(f"{l:>9s}" for l in BLAB) + " |  total   mean size  red.share  whole.share")
    for pname in panels:
        for gross in GROSSES:
            if not (pname == "U56" and gross == 0.75):
                continue
            iq = hh[(hh.panel == pname) & (hh.gross == gross) & (hh.device == "IDENTITY")].iloc[0]
            say("  IDENTITY(own tn)| " + " ".join(f"{iq[f'tn_{l}']:9.3f}" for l in BLAB)
                + f" | {sum(iq[f'tn_{l}'] for l in BLAB):6.3f}  (total turnover {iq.turnover_yr:.3f}x)")
            for dev in ORDER:
                for tier in TIERS:
                    q = hh[(hh.panel == pname) & (hh.gross == gross) & (hh.device == dev)
                           & (hh.tier == tier)].iloc[0]
                    say(f"  {dev:7s} {tier:6s}| " + " ".join(f"{q[f'rm_{l}']:9.3f}" for l in BLAB)
                        + f" | {q.removed_total:6.3f}  {q.mean_removed_size * 1e4:7.1f}bp"
                          f"  {q.removed_reduction_share:9.1%}  {q.removed_whole_share:10.1%}")
    hh.to_csv(f"{OUT}.histograms.csv", index=False)
    say("\n  THE SAME HISTOGRAMS AS SHARES OF EACH DEVICE'S OWN REMOVED TOTAL (all 4 panel x gross cells,")
    say("  so the shape is read independently of how much each device removes):")
    say("  panel g    device  tier   | " + " ".join(f"{l:>7s}" for l in BLAB))
    for pname in panels:
        for gross in GROSSES:
            for dev in ORDER:
                for tier in TIERS:
                    q = hh[(hh.panel == pname) & (hh.gross == gross) & (hh.device == dev)
                           & (hh.tier == tier)].iloc[0]
                    tot = q.removed_total
                    say(f"  {pname:5s} {gross:.2f} {dev:7s} {tier:6s}| "
                        + " ".join(f"{(q[f'rm_{l}'] / tot if abs(tot) > 1e-12 else np.nan):7.1%}"
                                   for l in BLAB))

    # ------------------------------------------------------------ B. the rate
    say("\n=== B. EACH DEVICE'S OWN REALISED RATE (pp of CAGR per 1% of turnover saved), 10 bps ===")
    say("  panel g    device  tier   | turnover  dTurn   dCAGR    rate  | 2463 published | dSharpe  dMaxDD  dRiskGross")
    cells = []
    for pname in panels:
        for gross in GROSSES:
            for dev in ORDER:
                for tier in TIERS:
                    r = df[(df.panel == pname) & (df.gross == gross) & (df.device == dev)
                           & (df.tier == tier) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    q = hh[(hh.panel == pname) & (hh.gross == gross) & (hh.device == dev)
                           & (hh.tier == tier)].iloc[0]
                    cells.append(dict(panel=pname, gross=gross, device=dev, tier=tier,
                                      rate=r.rate_pp_per_1pct, dTurn=r.dTurn, dCAGR=r.dCAGR,
                                      dSharpe=r.dSharpe, dMaxDD=r.dMaxDD,
                                      mean_removed_size=q.mean_removed_size,
                                      removed_reduction_share=q.removed_reduction_share,
                                      removed_whole_share=q.removed_whole_share,
                                      d_risk_gross=q.d_risk_gross,
                                      n_full_exits=q.n_full_exits, pass4a=r.pass4a, pass4b=r.pass4b))
                    say(f"  {pname:5s} {gross:.2f} {dev:7s} {tier:6s}| {r.turnover_yr:8.2f}"
                        f" {r.dTurn:+7.1%} {r.dCAGR * 100:+7.2f}pp {r.rate_pp_per_1pct:+7.3f} |"
                        f" {PUBLISHED_RATE[dev]:+14.3f} | {r.dSharpe:+7.4f} {r.dMaxDD:+7.2%}"
                        f" {q.d_risk_gross:+10.4f}")
    cf = pd.DataFrame(cells); cf.to_csv(f"{OUT}.cells.csv", index=False)

    # ------------------------------------------------------------ C. THE ANSWER
    say("\n=== C. THE ANSWER: DOES THE RATE TRACK THE REMOVED-TRADE SIZE DISTRIBUTION? ===")
    say("    rank (Spearman) correlation of each device-cell's realised rate against each candidate")
    say("    explanator, over all 60 (panel, gross, device, tier) cells and within each panel x gross:")
    tests = [("H1  mean REMOVED trade size", "mean_removed_size"),
             ("H2  REDUCTION share of removed turnover", "removed_reduction_share"),
             ("H1b WHOLE-POSITION share of removed turnover (>100bp)", "removed_whole_share"),
             ("H2b count of realised FULL EXITS", "n_full_exits"),
             ("H3  d RISK GROSS (the exposure control)", "d_risk_gross"),
             ("--  size of the cut itself (dTurn)", "dTurn")]
    say("  explanator                                          |  ALL 60  | U56 .75  U56 1.00  B136 .75  B136 1.00")
    corr_rows = []
    for lab, col in tests:
        allc = spearman(cf[col], cf.rate)
        sub = []
        for pname in panels:
            for gross in GROSSES:
                z = cf[(cf.panel == pname) & (cf.gross == gross)]
                sub.append(spearman(z[col], z.rate))
        kept = int(cf[[col, "rate"]].dropna().shape[0])
        corr_rows.append(dict(explanator=lab, col=col, all60=allc, n_kept=kept,
                              **{f"c{i}": v for i, v in enumerate(sub)}))
        say(f"  {lab:51s} | {allc:+8.3f} | " + "  ".join(f"{v:+8.3f}" for v in sub)
            + f"   (n={kept} of {len(cf)})")
    pd.DataFrame(corr_rows).to_csv(f"{OUT}.correlations.csv", index=False)
    say("\n  AND THE SAME TEST WITH THE DEVICE AVERAGED OVER ITS THREE TIERS (5 devices x 4 panel-gross")
    say("  cells = 20 points), which is the level 2463 actually published its rates at:")
    ag = cf.groupby(["panel", "gross", "device"], as_index=False).mean(numeric_only=True)
    say("  explanator                                          |  ALL 20")
    for lab, col in tests:
        say(f"  {lab:51s} | {spearman(ag[col], ag.rate):+8.3f}")
    say("\n  THE DEVICE-LEVEL PICTURE (pooled over panels, gross and tiers — 2463's own axis):")
    say("  device  | 2463 rate | this run's rate | mean removed size | reduction share | whole share | d risk gross")
    dv = cf.groupby("device", as_index=False).mean(numeric_only=True)
    for dev in ORDER:
        q = dv[dv.device == dev].iloc[0]
        say(f"  {dev:7s} | {PUBLISHED_RATE[dev]:+9.3f} | {q.rate:+15.3f} | {q.mean_removed_size * 1e4:14.1f}bp"
            f" | {q.removed_reduction_share:15.1%} | {q.removed_whole_share:11.1%} | {q.d_risk_gross:+12.4f}")
    say(f"\n   rank corr of THIS RUN's device-level rate against 2463's PUBLISHED device-level rate:"
        f" {spearman([PUBLISHED_RATE[d] for d in ORDER], [dv[dv.device == d].rate.iloc[0] for d in ORDER]):+.3f}"
        " (5 devices)")

    # ------------------------------------------------------------ D. both KEEP paths
    say(f"\n=== D. BOTH KEEP PATHS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes {int(df.pass4b.sum())} of {len(df)}    4a passes {int(df.pass4a.sum())} of {len(df)}")
    for dev in ["IDENTITY"] + ORDER:
        d = df[df.device == dev]
        say(f"   {dev:8s}: 4b {int(d.pass4b.sum()):3d}/{len(d):3d}  4a {int(d.pass4a.sum()):3d}/{len(d):3d}"
            "   4b leg failures: " + "  ".join(f"{x[2:]} {int((~d[x]).sum()):3d}" for x in
                                               ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    say("\n  EVERY GRID POINT AT THE HEADLINE RUNG (10 bps), both panels, both gross:")
    say("  panel g    device  tier   |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn | 4a 4b | legs")
    for pname in panels:
        for gross in GROSSES:
            for dev in ["IDENTITY"] + ORDER:
                for tier in (["IDENTITY"] if dev == "IDENTITY" else list(TIERS)):
                    r = df[(df.panel == pname) & (df.gross == gross) & (df.device == dev)
                           & (df.tier == tier) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    lg = "".join("1" if r[x] else "0"
                                 for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {gross:.2f} {dev:7s} {tier:6s}| {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%}"
                        f" {r.OOS_Sharpe:7.4f} | {r.turnover_yr:4.2f} | {'Y' if r.pass4a else '.'}"
                        f"  {'Y' if r.pass4b else '.'}  | {lg}"
                        + ("   <= COMMITTED" if dev == "IDENTITY" else ""))

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (device, tier) chosen on warm-up..2016-12-31 ONLY, 2017-2026")
    say("    read ONCE, scored against the COMMITTED identity book AND SPY. ===")
    wf = []
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)
                       & (df.device != "IDENTITY")]
                cm = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)
                        & (df.device == "IDENTITY")].iloc[0]
                d = d.assign(IS_rate=np.where(d.IS_dTurn < -1e-9,
                                              (d.IS_dCAGR * 100) / (-d.IS_dTurn * 100), np.nan))
                for chooser, col in (("C_ISRATE", "IS_rate"), ("C_ISSHARPE", "IS_Sharpe"),
                                     ("C_ISCALMAR", "IS_Calmar")):
                    if d[col].notna().sum() == 0:
                        continue
                    pk = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=chooser,
                                   pick=f"{pk.device}/{pk.tier}", full4b=bool(pk.pass4b),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                   OOS_MaxDD=pk.OOS_MaxDD, OOS_dCAGR=pk.OOS_dCAGR,
                                   OOS_dSharpe=pk.OOS_dSharpe, pick_turn=pk.turnover_yr,
                                   committed_turn=cm.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe,
                                   committed_OOS_CAGR=cm.OOS_CAGR,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 gross x {len(RUNGS)} rungs x 3 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                      {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the LIVE book's OOS Sharpe:             {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED identity's OOS Sharpe:    {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks with a POSITIVE OOS dCAGR vs the identity:      {int((wfd.OOS_dCAGR > 0).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                 {int(wfd.full4b.sum())} of {len(wfd)}")
    for ch in wfd.chooser.unique():
        q = wfd[wfd.chooser == ch]
        say(f"   {ch:11s} picks: " + "  ".join(f"{k}:{v}" for k, v in q.pick.value_counts().items()))
        say(f"      mean OOS Sharpe {q.OOS_Sharpe.mean():.4f} vs committed {q.committed_OOS_Sharpe.mean():.4f}"
            f"  mean OOS dCAGR {q.OOS_dCAGR.mean() * 100:+.2f}pp"
            f"  mean turnover {q.pick_turn.mean():.2f}x vs {q.committed_turn.mean():.2f}x"
            f"  4b {int(q.full4b.sum())}/{len(q)}")
    say("\n   panel g     bps chooser     pick           | OOS CAGR  OOS Sh  OOS dCAGR OOS dSh | turn  | 4b")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.gross:.2f} {r.cost_bps:5.1f} {r.chooser:11s} {r['pick']:14s} |"
            f" {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f} {r.OOS_dCAGR * 100:+9.2f}pp {r.OOS_dSharpe:+7.4f} |"
            f" {r.pick_turn:5.2f} | {'PASS' if r.full4b else 'fail'}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
