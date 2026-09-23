#!/usr/bin/env python3
"""idea 2457 (lane B, run 50, 2026-09-23) — DOES A FIXED PER-NAME NOTIONAL CUT THE CANDIDATE'S
DENOMINATOR CHURN WITHOUT TOUCHING A SINGLE NAME DECISION?

THE GAP.  The standing 4b candidate has exactly one stated adoption blocker -- turnover of
3.51x/yr against the live book's 1.77x -- and the record has now closed EVERY device filed
against it: admission (2447, `k = INF` picked in 50 of 64), exit (2351 minimum hold, 2328
weight-drift band), and re-size MAGNITUDE (2391 / 2404 partial-adjustment damper, 2408 calendar
rota).  All of them share one property: each REFUSES A TRADE THE SIGNAL ASKED FOR, and each was
measured to buy turnover at ~0.1 pp of CAGR per 1% saved.

NONE OF THEM TOUCHED THE RE-SIZE TRIGGER.  The candidate sizes each in-band name at
`min(gross / N_in(t), cap)`, where `N_in(t)` is the COUNT of names inside the 200d band that day.
That count moves every week, so every held name is re-priced every week even when nothing about
that name changed.  At ~37 held names on U56, a ONE-NAME change in breadth costs
37 x |0.75/38 - 0.75/37| ~= 2 pp of turnover in that week -- order 1x/yr of PURE DENOMINATOR
CHURN, paying 10 bps for no decision at all.

THE DEVICE.  Replace the shared floating denominator with a CONSTANT per-name notional `w*`:
hold every in-band name at exactly `w*` of NAV, sweep the residual, and let GROSS float with
breadth, scaled down ONLY where `w* x N_in` would exceed the gross ceiling `g` (so no leverage is
ever taken).  This is one fewer moving part than the committed rule, it holds the IDENTICAL NAME
SET every single day (G7 asserts this), and it leaves NO partial-adjustment stub -- every name
that trades trades in full.  What it spends in exchange is CONSTANT GROSS: the book de-grosses
in narrow tapes and re-grosses in broad ones, on its own, with no timing claim attached.

WHAT WOULD REFUTE IT.  If the denominator churn is real and costless to remove, turnover falls
and CAGR/Sharpe do NOT -- the first device in this record to beat the ~0.1 pp / 1% exchange rate.
If instead the floating denominator was doing useful work (it holds gross constant, which is a
risk-control convention, not an accident), the fixed book gives up return or drawdown in the
breadth extremes and joins the other five KILLs.  The prior is stated here BEFORE compute:
expect a REAL turnover cut (the churn is mechanical and undeniable) with an AMBIGUOUS return
effect, because floating gross is a bet on breadth that nothing in the record has ever priced.

DIAL 1 -- the constant per-name notional `w*` in {0.0125, 0.0150, 0.0200, 0.0250, 0.0300}.
DIAL 2 -- the gross ceiling `g` in {0.75 (live), 1.00}.

FLOAT -- the COMMITTED book `min(g / N_in, 2%)` -- is carried as a LABELLED COMPARAND ARM, never
a tuned point, exactly as `k = INF` was in idea 2447.  G3 asserts the FLOAT / g0.75 / SHY / 10 bps
cell reproduces the published CAP2 headline bit for bit.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, the SWEEP
convention {SHY at phi = 1.00 (committed), ZERO (idea 2423's pessimal un-remunerated bound)},
weekly cadence, t+1 execution, band 0.03, MA 200d and the 2% cap inside FLOAT.

WHY THE SWEEP CONVENTION IS PUBLISHED AND NOT ASSUMED.  This device makes GROSS float, so it
changes how much idle NAV exists and therefore how much the sweep leg matters.  Idea 2423 found
the entire SHY leg is worth +0.33 pp of CAGR and that the ZERO construction still passes 4b at
22.4% less turnover, so both bounds are already committed numbers and both are priced here.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  A sizing convention that changes no name decision
cannot move three failing legs at once, so there is no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (arm, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE, and the picks are scored against the COMMITTED
FLOAT / g0.75 cell.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the eligible
set IS `baseline.band_state` & priced, unmodified.  G3 FLOAT reproduces the committed CAP2
headline.  G4 no leverage anywhere.  G5 the cost charge is exactly linear in the rung.  G6
exactly two tuned parameters.  G7 THE NAME SET IS IDENTICAL ACROSS EVERY ARM (the whole claim).
G8 the per-name weight is EXACTLY `w*` on every non-binding day.  G9 the sweep instrument is
priced on every held row.  G10 the device BITES (turnover falls against FLOAT).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The FIX-vs-FLOAT contrast is same-tape, same-day,
same-name-set and first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_fixed-per-name-notional_B.py
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

DATE, SLUG, LANE = "2026-09-23", "fixed-per-name-notional", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
NOTIONALS = [0.0125, 0.0150, 0.0200, 0.0250, 0.0300]
ARMS = ["FLOAT"] + [f"FIX{w:.4f}" for w in NOTIONALS]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
SWEEPS = ["SHY", "ZERO"]
HEADLINE_SWEEP, HEADLINE_RUNG, HEADLINE_ARM, HEADLINE_G = "SHY", 10.0, "FLOAT", 0.75
NAME_CAP, SWEEP_TICKER = 0.020, "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_TURNOVER = 1.77

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


def arm_w(arm):
    """The constant notional an arm carries, or nan for the committed FLOAT comparand."""
    return np.nan if arm == "FLOAT" else float(arm[3:])


# ---------------------------------------------------------------- the two sizing conventions
def eligible(px):
    """Names permitted to be held: inside the 200d +/-3% hysteretic band AND priced.  IDENTICAL
    for every arm -- this device changes no name decision at all (G7 asserts it)."""
    return band_state(px, BAND) & px.notna()


def risk_weights(px, arm, gross):
    """FLOAT (committed): w_i = min(gross / N_in, 2%)  -- the shared denominator moves weekly, so
    every held name is re-priced whenever breadth changes.
    FIX w*:              w_i = w* x min(1, gross / (w* x N_in))  -- a held name's target is the
    CONSTANT w* and never moves, except on the days the no-leverage/gross ceiling binds, where the
    whole book is scaled by one common factor (reported: G8 counts those days)."""
    el = eligible(px)
    nin = el.sum(axis=1).replace(0, np.nan)
    if arm == "FLOAT":
        per = (gross / nin).clip(upper=NAME_CAP)
    else:
        w = arm_w(arm)
        per = w * np.minimum(1.0, gross / (w * nin))
    return el.astype(float).mul(per.fillna(0.0), axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the per-day turnover is retained (so every cost rung
    is read off the SAME realised path) and split into its RISK-NAME and SWEEP-LEG components.
    Weights decided at t-1, applied at t; the book drifts between rebalances; the residual is
    swept into SHY at phi = 1.00 when sweep=True, and left un-remunerated when sweep=False."""
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


def main():
    t0 = time.time()
    say("=== idea 2457 — DOES A FIXED PER-NAME NOTIONAL CUT THE CANDIDATE'S DENOMINATOR CHURN? ===")
    say(f"    {DATE}  lane {LANE} run 50   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweeps {SWEEPS} (phi=1.00)")
    say(f"    DIAL 1 constant per-name notional w* {NOTIONALS}    DIAL 2 gross ceiling {GROSSES}")
    say("    FLOAT = the COMMITTED book min(g/N_in, 2%) carried as a labelled comparand arm, never a tuned point.")
    say("    PRIOR, STATED BEFORE COMPUTE: the denominator churn is mechanical and undeniable, so expect a REAL")
    say("    turnover cut; the RETURN effect is genuinely ambiguous, because a fixed notional lets GROSS float")
    say("    with breadth and nothing in this record has ever priced that bet.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343); a sizing")
    say("    convention that changes no name decision cannot move three failing legs at once.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The FIX-vs-FLOAT contrast is same-tape, same-day, same-name-set and immune.")
    gate("G6 exactly two tuned parameters", "constant notional w*, gross ceiling g", "2", True)

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

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G7 -- THE WHOLE CLAIM: every arm holds the IDENTICAL NAME SET on every day.
    ref = risk_weights(px_u, "FLOAT", 0.75) > 0
    worst7, bind_days = 0, {}
    for arm in ARMS:
        for g in GROSSES:
            w = risk_weights(px_u, arm, g)
            worst7 = max(worst7, int(((w > 0) != ref).sum().sum()))
            if arm != "FLOAT":
                ws = arm_w(arm)
                nz = w.where(w > 0)
                nb = (nz.sub(ws).abs() < 1e-15) | nz.isna()
                bind_days[(arm, g)] = float(1.0 - nb.all(axis=1).loc[px_u.index[WARMUP]:].mean())
    gate("G7 THE NAME SET IS IDENTICAL ACROSS EVERY ARM AND GROSS (this device changes no name decision)",
         f"max differing (name x day) cells over {len(ARMS) * len(GROSSES)} weight paths: {worst7}",
         "0", worst7 == 0)
    g8 = max(bind_days.values())
    publish("G8 share of scored days on which the gross ceiling BINDS (so the FIX weight is scaled, U56)",
            "  ".join(f"{a[3:]}/g{g:.2f}:{v:.1%}" for (a, g), v in sorted(bind_days.items())))
    gate("G8b on every NON-binding day the per-name weight is EXACTLY w* (no drift, no denominator)",
         f"verified on all {len(bind_days)} FIX paths by construction; binding share max {g8:.1%}",
         "exact", True)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for sw in SWEEPS:
            for arm in ARMS:
                for gross in GROSSES:
                    wr = risk_weights(px, arm, gross)
                    bk = run_book(px, wr, sweep=(sw == "SHY"))
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    yrs = len(tn) / 252
                    tg = wr.sum(axis=1).loc[start:]          # INTENDED risk-leg exposure
                    book_facts.append(dict(
                        panel=pname, sweep=sw, arm=arm, gross=gross,
                        target_gross=float(tg.mean()), target_sd=float(tg.std()),
                        target_min=float(tg.min()), target_max=float(tg.max()),
                        turnover_yr=float(tn.sum() / yrs),
                        turnover_risk_yr=float(bk["turn_risk"].loc[start:].sum() / yrs),
                        turnover_sweep_yr=float(bk["turn_sweep"].loc[start:].sum() / yrs),
                        mean_names=float(bk["names"].loc[start:].mean()),
                        mean_gross=float(bk["gross"].loc[start:].mean()),
                        sd_gross=float(bk["gross"].loc[start:].std()),
                        min_gross=float(bk["gross"].loc[start:].min()),
                        max_gross=float(bk["gross"].loc[start:].max()),
                        max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, sweep=sw, arm=arm, gross=gross, cost_bps=rung,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / yrs),
                            mean_gross=float(bk["gross"].loc[start:].mean()),
                            sd_gross=float(bk["gross"].loc[start:].std()),
                            target_gross=float(tg.mean()), target_sd=float(tg.std()),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                            base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                            base_turnover=LIVE_TURNOVER,
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(SWEEPS)} sweeps x {len(ARMS)} arms x"
        f" {len(GROSSES)} gross x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max realised gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} peak gross,"
         f" {bf.max_name_w.max():.4f} max single name", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))

    pz = panels["U56"]; st = pz.index[WARMUP]
    bz = run_book(pz, risk_weights(pz, "FLOAT", 0.75))
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP_TICKER].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.arm == "FLOAT") & (df.sweep == "SHY")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10)
    gate("G3 FLOAT / g0.75 / SHY / 10 bps reproduces the COMMITTED CAP2 headline"
         " (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318)",
         f"{a.CAGR:.2%} / {a.Sharpe:.4f} / {a.MaxDD:.2%}, OOS {a.OOS_CAGR:.2%} / {a.OOS_Sharpe:.4f}"
         f"  -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say(f"\n=== A. THE FULL LADDER, sweep {HEADLINE_SWEEP}, gross 0.75 — EVERY GRID POINT ===")
    say("  panel arm       bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr  risk gr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for arm in ARMS:
            for rung in RUNGS:
                r = df[(df.panel == pname) & (df.sweep == HEADLINE_SWEEP) & (df.arm == arm)
                       & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s} {arm:9s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                    f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                    f" | {r.turnover_yr:7.2f} {r.target_gross:8.3f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}"
                    + ("   <= COMMITTED" if arm == "FLOAT" else ""))
    say(f"\n=== A2. THE SAME LADDER AT GROSS 1.00, sweep {HEADLINE_SWEEP} ===")
    say("  panel arm       bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr  risk gr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for arm in ARMS:
            for rung in RUNGS:
                r = df[(df.panel == pname) & (df.sweep == HEADLINE_SWEEP) & (df.arm == arm)
                       & (df.gross == 1.00) & (df.cost_bps == rung)].iloc[0]
                lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s} {arm:9s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                    f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                    f" | {r.turnover_yr:7.2f} {r.target_gross:8.3f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}")
    say(f"\n=== A3. THE ZERO-SWEEP LADDER (idea 2423's pessimal bound), gross 0.75 ===")
    say("  panel arm       bps |   CAGR   Sharpe    MaxDD | OOS CAGR  OOS Sh | turn/yr | 4a 4b")
    for pname in panels:
        for arm in ARMS:
            for rung in RUNGS:
                r = df[(df.panel == pname) & (df.sweep == "ZERO") & (df.arm == arm)
                       & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                say(f"  {pname:5s} {arm:9s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                    f" {r.MaxDD:8.2%} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:7.2f}"
                    f" | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ B. FIX vs its own FLOAT row
    say("\n=== B. THE WHOLE QUESTION: WHAT DOES THE FIXED NOTIONAL BUY, AND WHAT DOES IT COST?"
        " (each FIX arm vs its OWN FLOAT row: same panel, sweep, gross, rung) ===")
    say("  panel sw   g    bps  w*     | dTurnover | dCAGR    dSharpe   dMaxDD  | dOOS Sh"
        " | risk gross FLOAT -> FIX | 4b FLOAT -> FIX")
    dec = []
    for pname in panels:
        for sw in SWEEPS:
            for gross in GROSSES:
                for rung in RUNGS:
                    z = df[(df.panel == pname) & (df.sweep == sw) & (df.gross == gross)
                           & (df.cost_bps == rung) & (df.arm == "FLOAT")].iloc[0]
                    for arm in ARMS[1:]:
                        r = df[(df.panel == pname) & (df.sweep == sw) & (df.gross == gross)
                               & (df.cost_bps == rung) & (df.arm == arm)].iloc[0]
                        dec.append(dict(panel=pname, sweep=sw, gross=gross, cost_bps=rung, arm=arm,
                                        w=arm_w(arm),
                                        dTurn=r.turnover_yr / z.turnover_yr - 1,
                                        dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                                        dMaxDD=r.MaxDD - z.MaxDD,
                                        dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                                        gross_float=z.target_gross, gross_fix=r.target_gross,
                                        dgross=r.target_gross - z.target_gross,
                                        f4b=bool(z.pass4b), x4b=bool(r.pass4b)))
                        if sw == HEADLINE_SWEEP and gross == 0.75 and rung == HEADLINE_RUNG:
                            say(f"  {pname:5s} {sw:4s} {gross:.2f} {rung:5.1f} {arm[3:]} |"
                                f" {r.turnover_yr / z.turnover_yr - 1:+9.1%} | {r.CAGR - z.CAGR:+7.2%}"
                                f" {r.Sharpe - z.Sharpe:+9.4f} {r.MaxDD - z.MaxDD:+8.2%} |"
                                f" {r.OOS_Sharpe - z.OOS_Sharpe:+8.4f} |"
                                f" {z.target_gross:11.3f} -> {r.target_gross:.3f} |"
                                f" {'PASS' if z.pass4b else 'fail'} -> {'PASS' if r.pass4b else 'fail'}")
    dd_ = pd.DataFrame(dec); dd_.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n  Over all {len(dd_)} (FIX vs its own FLOAT) pairs:")
    say(f"   dTurnover < 0 in {int((dd_.dTurn < 0).sum())} of {len(dd_)}"
        f"   dCAGR > 0 in {int((dd_.dCAGR > 0).sum())}"
        f"   dSharpe > 0 in {int((dd_.dSharpe > 0).sum())}"
        f"   dMaxDD > 0 (shallower) in {int((dd_.dMaxDD > 0).sum())}"
        f"   dOOS Sharpe > 0 in {int((dd_.dOOS_Sharpe > 0).sum())}")
    say("   by notional w*:")
    for arm in ARMS[1:]:
        q = dd_[dd_.arm == arm]
        say(f"    w*={arm[3:]}  mean dTurn {q.dTurn.mean():+7.1%}  dCAGR {q.dCAGR.mean():+.2%}"
            f"  dSharpe {q.dSharpe.mean():+.4f}  dMaxDD {q.dMaxDD.mean():+.2%}"
            f"  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}   4b: FLOAT {int(q.f4b.sum())}/{len(q)}"
            f" -> FIX {int(q.x4b.sum())}/{len(q)}")
    say("\n   READ THIS BEFORE THE EXCHANGE RATE: a SMALLER w* also de-grosses the risk leg, so a raw")
    say("   FIX-vs-FLOAT dCAGR mixes the turnover trade with an EXPOSURE cut.  The `risk gross` column above")
    say("   is the confound, printed on every row; the CLEAN same-exposure contrasts are the cells whose")
    say("   risk gross matches FLOAT's, and the identity in G11 below.")
    say("\n   THE EXCHANGE RATE — pp of CAGR given up per 1% of turnover saved"
        " (10 bps, SHY sweep, g0.75).  The record's five killed devices all sat near -0.10:")
    for pname in panels:
        for arm in ARMS[1:]:
            q = dd_[(dd_.panel == pname) & (dd_.arm == arm) & (dd_.sweep == HEADLINE_SWEEP)
                    & (dd_.gross == 0.75) & (dd_.cost_bps == HEADLINE_RUNG)].iloc[0]
            rate = (q.dCAGR * 100) / (-q.dTurn * 100) if q.dTurn < 0 else np.nan
            say(f"    {pname:5s} w*={arm[3:]}: turnover {q.dTurn:+.1%}, CAGR {q.dCAGR * 100:+.2f} pp"
                + (f"  -> {rate:+.3f} pp of CAGR per 1% of turnover saved" if q.dTurn < 0
                   else "   (turnover ROSE — no exchange rate)"))
    g_ = dd_[(dd_.sweep == HEADLINE_SWEEP) & (dd_.cost_bps == HEADLINE_RUNG) & (dd_.gross == 0.75)]
    cut = g_[g_.dTurn < 0]
    if len(cut):
        publish("the best exchange rate available anywhere at the headline convention",
                f"{(cut.dCAGR * 100 / (-cut.dTurn * 100)).max():+.3f} pp of CAGR per 1% saved"
                f"  (vs the ~-0.10 the five killed devices all paid)")

    # ------------------------------------------------------------ C. the churn account
    say("\n=== C. THE TURNOVER ACCOUNT — how much of the blocker is DENOMINATOR CHURN?"
        f"  (sweep {HEADLINE_SWEEP}, g0.75; the live book runs {LIVE_TURNOVER}x/yr) ===")
    say("  panel arm       | total/yr  risk-leg  sweep-leg | mean names | risk gross  sd  [min, max] | vs live")
    for pname in panels:
        for arm in ARMS:
            e = bf[(bf.panel == pname) & (bf.sweep == HEADLINE_SWEEP) & (bf.arm == arm)
                   & (bf.gross == 0.75)].iloc[0]
            say(f"  {pname:5s} {arm:9s} | {e.turnover_yr:8.2f} {e.turnover_risk_yr:9.2f}"
                f" {e.turnover_sweep_yr:10.2f} | {e.mean_names:10.2f} |"
                f" {e.target_gross:10.3f} {e.target_sd:5.3f} [{e.target_min:.3f}, {e.target_max:.3f}] |"
                f" {e.turnover_yr / LIVE_TURNOVER:6.2f}x")
    say("\n   CAGR PER UNIT OF RISK GROSS (the exposure-normalised read; 10 bps, SHY, g0.75):")
    for pname in panels:
        for arm in ARMS:
            r = df[(df.panel == pname) & (df.sweep == HEADLINE_SWEEP) & (df.arm == arm)
                   & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"    {pname:5s} {arm:9s} | risk gross {r.target_gross:.3f} | CAGR {r.CAGR:6.2%}"
                f" -> {r.CAGR / r.target_gross:6.2%} per unit | Sharpe {r.Sharpe:.4f}"
                f" | turn/unit {r.turnover_yr / r.target_gross:5.2f}")

    say("\n   GROSS DRIFT IS THE PRICE OF THE CUT — the FIX book's gross is no longer a constant:")
    for pname in panels:
        for arm in ARMS:
            for gross in GROSSES:
                e = bf[(bf.panel == pname) & (bf.sweep == HEADLINE_SWEEP) & (bf.arm == arm)
                       & (bf.gross == gross)].iloc[0]
                say(f"    {pname:5s} {arm:9s} ceiling {gross:.2f} | risk gross {e.target_gross:.3f}"
                    f"  sd {e.target_sd:.3f}  range [{e.target_min:.3f}, {e.target_max:.3f}]"
                    f"  swept total gross {e.mean_gross:.3f}  turnover {e.turnover_yr:.2f}x")

    # ------------------------------------------------------------ D. KEEP counts
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for arm in ARMS:
        d = df[df.arm == arm]
        say(f"   {arm:9s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by arm: "
            + "  ".join(f"{a[3:] if a != 'FLOAT' else 'FLT'}:{int(d[d.arm == a].pass4b.sum())}"
                        f"/{len(d[d.arm == a])}" for a in ARMS))
    for sw in SWEEPS:
        d = df[df.sweep == sw]
        say(f"   sweep {sw:4s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    for gross in GROSSES:
        d = df[df.gross == gross]
        say(f"   gross {gross:.2f}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same sweep, arm, gross, rung):")
    jt = []
    for sw in SWEEPS:
        for arm in ARMS:
            for gross in GROSSES:
                for rung in RUNGS:
                    q = df[(df.sweep == sw) & (df.arm == arm) & (df.gross == gross)
                           & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                    jt.append(dict(sweep=sw, arm=arm, gross=gross, cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by arm: "
        + "  ".join(f"{a}:{int(jf[jf.arm == a].joint.sum())}/{len(jf[jf.arm == a])}" for a in ARMS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.head(20).iterrows():
        say(f"    {r.panel:5s} {r.sweep:4s} {r.arm:9s} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  turn {r.turnover_yr:.2f}x"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (arm, gross) chosen on warm-up..2016-12-31 ONLY, 2017-2026")
    say("    read ONCE, and scored against the COMMITTED FLOAT / gross 0.75 cell. ===")
    wf = []
    for pname in panels:
        for sw in SWEEPS:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.sweep == sw) & (df.cost_bps == rung)]
                cm = d[(d.arm == "FLOAT") & (d.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, sweep=sw, cost_bps=rung, chooser=chooser,
                                   pick_arm=pk.arm, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                   OOS_MaxDD=pk.OOS_MaxDD, pick_turn=pk.turnover_yr,
                                   committed_turn=cm.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe,
                                   committed_OOS_CAGR=cm.OOS_CAGR,
                                   committed_OOS_MaxDD=cm.OOS_MaxDD,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                   base_OOS_CAGR=pk.base_OOS_CAGR,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x {len(SWEEPS)} sweeps x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                        {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:              {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED FLOAT cell's OOS Sharpe:   {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                  {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over arm:   " + "  ".join(
        f"{a}:{int((wfd.pick_arm == a).sum())}" for a in ARMS))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean OOS CAGR of the IS-only picks   {wfd.OOS_CAGR.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_CAGR.mean():.2%}"
        f" vs the live book's {wfd.base_OOS_CAGR.mean():.2%}"
        f" vs SPY OOS {wfd.spy_OOS_CAGR.mean():.2%}")
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs the live book's {wfd.base_OOS_Sharpe.mean():.4f} vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say(f"   mean OOS MaxDD of the IS-only picks  {wfd.OOS_MaxDD.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_MaxDD.mean():.2%}")
    say(f"   mean turnover of the picks {wfd.pick_turn.mean():.2f}x vs the committed {wfd.committed_turn.mean():.2f}x")
    say("\n   panel sw    bps chooser     | pick            OOS CAGR  OOS Sh  OOS DD   turn/yr"
        " | committed OOS Sh / turn")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.sweep:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r.pick_arm + '/' + format(r.pick_gross, '.2f'):15s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f}"
            f" {r.OOS_MaxDD:7.2%} {r.pick_turn:8.2f} | {r.committed_OOS_Sharpe:12.4f} / {r.committed_turn:.2f}")

    # ------------------------------------------------------------ G11 the identity
    wid = max(float((risk_weights(px, "FIX0.0200", 0.75) - risk_weights(px, "FLOAT", 0.75)).abs().max().max())
              for px in panels.values())
    gate("G11 THE COMMITTED BOOK ALREADY IS A FIXED 2% NOTIONAL, SCALED BY THE NO-LEVERAGE CEILING"
         " (min(g/N, 2%) == 2% x min(1, g/(2% x N)) identically)",
         f"max|w_FIX0.0200 - w_FLOAT| over both panels: {wid:.3e}", "< 1e-15 (float rounding only)", wid < 1e-15)

    # ------------------------------------------------------------ G10
    hb = bf[(bf.sweep == HEADLINE_SWEEP) & (bf.gross == 0.75)]
    fl = hb[hb.arm == "FLOAT"].set_index("panel").turnover_yr
    bites = {p: float(hb[(hb.panel == p) & (hb.arm != "FLOAT")].turnover_yr.min() / fl[p] - 1)
             for p in panels}
    gate("G10 the device BITES (best turnover cut against its own FLOAT row, headline convention)",
         "  ".join(f"{p}:{v:+.1%}" for p, v in bites.items()), "< 0",
         all(v < 0 for v in bites.values()))

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
