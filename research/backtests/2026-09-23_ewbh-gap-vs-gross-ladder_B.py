#!/usr/bin/env python3
"""idea 2528 (lane B, run 68, 2026-09-23) — DOES THE EWBH GAP CLOSE AT HIGHER GROSS, OR IS IT
A RULE DEFICIT?

THE GAP.  Idea 2516 replaced rule 4b's SPY comparand with the panel's OWN equal-weight
buy-and-hold (EWBH) and every one of the record's committed capped-family 4b passes vanished.
Idea 2532 then matched the blend to the candidate's realised gross and found the candidate ahead
on MaxDD in 128 of 128 rows and behind on CAGR in 128 of 128 — "a drawdown product and nothing
else".  BOTH comparisons charge the candidate with an EXPOSURE difference: every committed
capped book runs gross 0.75-1.00 and parks the rest in SHY, while EWBH runs gross 1.00 all day.
That mixes a RULE difference with an EXPOSURE difference in the direction that flatters EWBH on
CAGR and flatters the rule on MaxDD.

THE QUESTION, AS THE QUEUE WROTE IT.  Sweep the candidate's gross UP the ladder and report, at
each (panel, cap, cost rung), the gross at which the book's CAGR REACHES EWBH's and what its
MaxDD is there.  If no attainable gross closes the CAGR gap at a MaxDD the 4b DD leg would
accept, the deficit is in the RULE and the capped family is finished as a capital candidate.

DIAL 1 -- gross g in {0.75 (live), 1.00, 1.25, 1.50}.
DIAL 2 -- per-name cap in {0.015, 0.020 (idea 2322's CAP2, the standing candidate), 0.030, INF
          (2300/2332's uncapped CAND)}.
EXACTLY TWO TUNED PARAMETERS.  NO LEVERAGE ABOVE 1.00 AT THE BOOK LEVEL: the SHY sleeve funds
every rise in gross, and if the risk sleeve would exceed 1.00 of NAV it is scaled back to 1.00
(gate G4).  At g = 0.75 / cap 0.020 the scale-back is a no-op, so the committed CAP2 headline is
reproduced exactly (gate G3).

PUBLISHED AXES, NEVER SELECTED ON: panels {U56, B136}; cost rungs {0, 10, 25, 50} bps; weekly
cadence; t+1 execution; band 0.03; MA 200d; SHY sweep at phi = 1.00.

COMPARANDS, ALL SCORED ON EVERY LEG, NONE SELECTED ON.
  SPY        -- PROTOCOL rule 4b as written.
  EWBH       -- idea 2516's comparand: equal weight over every panel column priced on the first
                scored day, bought once and never rebalanced, gross 1.00.  THE HEADLINE.
  EWBH_NOSWEEP -- the same with the sweep instrument SHY excluded.  Reported for contrast.
  RULES v2   -- the live book (PROTOCOL 4a).

TWO BARS AT EVERY COMPARAND, because 4b's constants were calibrated to SPY.
  4b-PROTO   Sharpe > X in BOTH halves AND out of sample, MaxDD >= 0.60 x X's, CAGR >= 0.70 x X's.
  4b-STRICT  Sharpe > X in both halves AND OOS, MaxDD no worse than X's, CAGR no lower than X's.

RULE 8.  (g, cap) fitted on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE = max IS Sharpe, C_ISCAGR = max IS CAGR); 2017-2026 then read ONCE.  Neither chooser
ever sees a benchmark, an OOS number or a MaxDD.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ewbh-gap-vs-gross-ladder_B.py
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

DATE, SLUG, LANE = "2026-09-23", "ewbh-gap-vs-gross-ladder", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP, SWEEP = 0.03, "W", 260, "SHY"
GROSSES = [0.75, 1.00, 1.25, 1.50]
CAPS = [0.015, 0.020, 0.030, np.inf]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
# the committed U56 CAP2 headline (idea 2322, g 0.75 / cap 0.020 / W / 10 bps)
COMMITTED = dict(CAGR=0.1162, Sharpe=1.2687, MaxDD=-0.1481)

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


# ---------------------------------------------------------------- the book
def cap_weights(px, gross, cap):
    """idea 2322's capped band book, with the no-leverage clip the gross ladder requires.

    admitted = inside the 200d +/- BAND band (hysteresis, baseline.band_state) and priced;
    w_i = min(gross / N_in, cap); if the risk sleeve would exceed 1.00 of NAV it is scaled back
    to exactly 1.00 (never levered); idle NAV swept to SHY.
    """
    adm = band_state(px, BAND) & px.notna()
    nin = adm.sum(axis=1).replace(0, np.nan)
    per = gross / nin
    if np.isfinite(cap):
        per = pd.concat([per, pd.Series(cap, index=px.index)], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    s = w.sum(axis=1)
    w = w.mul((1.0 / s.replace(0, np.nan)).clip(upper=1.0).fillna(1.0), axis=0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def ewbh_returns(px, cols, start):
    """Equal weight over `cols` on the first scored day, bought once, never rebalanced."""
    q = px.loc[start:, cols]
    eq = (q / q.iloc[0]).mean(axis=1)
    r = eq.pct_change().fillna(0.0)
    return r


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
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs_proto(r, x, r_oos, x_oos):
    h1, h2 = halves(r); s1, s2 = halves(x)
    L = dict(L_H1=h1 > s1, L_H2=h2 > s2, L_OOS=sharpe(r_oos) > sharpe(x_oos),
             L_DD=maxdd(r) >= DD_CAP * maxdd(x), L_CAGR=cagr(r) >= CAGR_FLOOR * cagr(x))
    L = {k: bool(v) for k, v in L.items()}
    L["pass"] = all(L.values())
    return L


def legs_strict(r, x, r_oos, x_oos):
    h1, h2 = halves(r); s1, s2 = halves(x)
    L = dict(L_H1=h1 > s1, L_H2=h2 > s2, L_OOS=sharpe(r_oos) > sharpe(x_oos),
             L_DD=maxdd(r) >= maxdd(x), L_CAGR=cagr(r) >= cagr(x))
    L = {k: bool(v) for k, v in L.items()}
    L["pass"] = all(L.values())
    return L


def legstr(d):
    return "".join("1" if d[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))


def capname(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    say("=== idea 2528 (lane B, run 68) — DOES THE EWBH GAP CLOSE AT HIGHER GROSS? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    DIAL 1 gross {GROSSES}    DIAL 2 cap {[capname(c) for c in CAPS]}")
    gate("G5 exactly two tuned parameters", "gross g, per-name cap", "2", True)

    rows, wf, gapsum = [], [], []
    SERIES: dict = {}

    for panel, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        start = px.index[WARMUP]
        yrs = (px.index[-1] - start).days / 365.25
        gate(f"G0 >= 10y ({panel})", f"{yrs:.1f}y, {px.shape[1]} cols, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({panel})",
             f"{int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

        # ---- comparands
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        live0 = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=CADENCE)
        live_t = live0["turnover"].loc[start:]
        live_r0 = live0["returns"].loc[start:]

        cols_all = [c for c in px.columns if pd.notna(px[c].loc[start])]
        cols_nos = [c for c in cols_all if c != SWEEP]
        ew_r0 = ewbh_returns(px, cols_all, start)
        ewn_r0 = ewbh_returns(px, cols_nos, start)
        ew_t = pd.Series(0.0, index=ew_r0.index); ew_t.iloc[0] = 1.0     # one trade, at inception
        gate(f"G7 EWBH trades exactly once ({panel})",
             f"turnover total {float(ew_t.sum()):.3f}, non-zero days {int((ew_t > 0).sum())}",
             "1.000 / 1 day", abs(float(ew_t.sum()) - 1.0) < 1e-12 and int((ew_t > 0).sum()) == 1)
        publish(f"EWBH composition ({panel})",
                f"{len(cols_all)} columns priced at {start.date()} (incl. SPY/SHY); NOSWEEP {len(cols_nos)}")

        # ---- the ladder
        books = {}
        for cap in CAPS:
            for g in GROSSES:
                w = cap_weights(px, g, cap)
                tot = w.sum(axis=1).loc[start:]
                if not gate(f"G4 no leverage ({panel}, cap {capname(cap)}, g {g:.2f})",
                            f"max book gross {float(tot.max()):.6f}", "<= 1.0 + 1e-9",
                            float(tot.max()) <= 1.0 + 1e-9):
                    pass
                res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
                books[(cap, g)] = dict(r0=res["returns"].loc[start:], turn=res["turnover"].loc[start:],
                                       risk=(w.drop(columns=[SWEEP]).sum(axis=1)).loc[start:])

        # ---- G9: the ladder SATURATES.  Above g = 1.00 the no-leverage clip (cap INF) or the
        # per-name cap (finite cap) binds on every day, so the rungs are BIT-IDENTICAL and the
        # ladder has only TWO distinct rungs.  This is a property of the idea as written
        # ("no leverage above 1.0 at the BOOK level"), not an implementation choice.
        for cap in CAPS:
            base = books[(cap, 1.00)]["r0"]
            d = max(float((books[(cap, g)]["r0"] - base).abs().max()) for g in (1.25, 1.50))
            gate(f"G9 ladder saturates above g=1.00 ({panel}, cap {capname(cap)})",
                 f"max|r(g) - r(1.00)| over g in (1.25, 1.50) = {d:.3e}",
                 "< 1e-12 (numerically identical; float re-association only)", d < 1e-12)
        d075 = float((books[(0.020, 0.75)]["r0"] - books[(0.020, 1.00)]["r0"]).abs().max())
        publish(f"distinct rungs on the gross ladder ({panel})",
                f"2 of 4 (g=0.75 differs from g>=1.00 by max|dr| {d075:.3e}; 1.25 and 1.50 add nothing)")

        # ---- G3: the committed CAP2 headline, and G8: cost linearity
        b = books[(0.020, 0.75)]
        r10 = b["r0"] - b["turn"] * HEADLINE_RUNG / 1e4
        if panel == "U56":
            d = max(abs(cagr(r10) - COMMITTED["CAGR"]), abs(sharpe(r10) - COMMITTED["Sharpe"]) / 10,
                    abs(maxdd(r10) - COMMITTED["MaxDD"]))
            gate("G3 committed U56 CAP2 headline reproduced",
                 f"CAGR {cagr(r10):.4%} / Sharpe {sharpe(r10):.4f} / MaxDD {maxdd(r10):.4%} "
                 f"vs committed {COMMITTED['CAGR']:.2%} / {COMMITTED['Sharpe']:.4f} / {COMMITTED['MaxDD']:.2%}",
                 "< 5e-4", d < 5e-4)
        r_eng = backtest(px, cap_weights(px, 0.75, 0.020), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        dl = float((r_eng - r10).abs().max())
        gate(f"G8 cost linearity ({panel})", f"max|d| {dl:.3e}", "< 1e-12", dl < 1e-12)

        # ---- score every cell at every rung
        for bps in RUNGS:
            spy_r = spy
            ew_r = ew_r0 - ew_t * bps / 1e4
            ewn_r = ewn_r0 - ew_t * bps / 1e4
            live_r = live_r0 - live_t * bps / 1e4
            oos = lambda s: s.loc[OOS_START:]
            for cap in CAPS:
                cagrs = {}
                for g in GROSSES:
                    bk = books[(cap, g)]
                    r = bk["r0"] - bk["turn"] * bps / 1e4
                    P_spy = legs_proto(r, spy_r, oos(r), oos(spy_r))
                    S_ew = legs_strict(r, ew_r, oos(r), oos(ew_r))
                    P_ew = legs_proto(r, ew_r, oos(r), oos(ew_r))
                    S_ewn = legs_strict(r, ewn_r, oos(r), oos(ewn_r))
                    h1, h2 = halves(r); l1, l2 = halves(live_r)
                    p4a = bool(h1 > l1 and h2 > l2 and maxdd(r) >= maxdd(live_r))
                    cagrs[g] = (cagr(r), maxdd(r), P_spy["L_DD"])
                    if bps == HEADLINE_RUNG: SERIES[(panel, capname(cap), g)] = r
                    rows.append(dict(panel=panel, cap=capname(cap), gross=g, bps=bps,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                     H1=h1, H2=h2, OOS_Sharpe=sharpe(oos(r)), OOS_CAGR=cagr(oos(r)),
                                     OOS_MaxDD=maxdd(oos(r)), turnover_per_yr=float(bk["turn"].sum()) / (len(r) / 252),
                                     mean_risk_gross=float(bk["risk"].mean()),
                                     pass4a=p4a, pass4b_SPY=P_spy["pass"], legs4b_SPY=legstr(P_spy),
                                     pass4b_EWBH_proto=P_ew["pass"], legs4b_EWBH_proto=legstr(P_ew),
                                     pass4b_EWBH_strict=S_ew["pass"], legs4b_EWBH_strict=legstr(S_ew),
                                     pass4b_EWBHNOSWEEP_strict=S_ewn["pass"]))
                # the idea's own headline: the gross at which CAGR reaches EWBH's
                target = cagr(ew_r)
                reach = [g for g in GROSSES if cagrs[g][0] >= target]
                gmin = min(reach) if reach else None
                gapsum.append(dict(panel=panel, cap=capname(cap), bps=bps, EWBH_CAGR=target,
                                   EWBH_MaxDD=maxdd(ew_r), SPY_CAGR=cagr(spy_r), SPY_MaxDD=maxdd(spy_r),
                                   g_reaching_EWBH_CAGR=(gmin if gmin is not None else np.nan),
                                   CAGR_at_that_g=(cagrs[gmin][0] if gmin else np.nan),
                                   MaxDD_at_that_g=(cagrs[gmin][1] if gmin else np.nan),
                                   DDleg_ok_there=(bool(cagrs[gmin][2]) if gmin else False),
                                   best_CAGR_on_ladder=max(v[0] for v in cagrs.values()),
                                   CAGR_shortfall_at_best=max(v[0] for v in cagrs.values()) - target))

            # ---- rule 8 at this rung: (g, cap) fitted on IS only
            def rr(cap, g):
                bk = books[(cap, g)]
                return bk["r0"] - bk["turn"] * bps / 1e4
            grid = [(cap, g) for cap in CAPS for g in GROSSES]
            IS = {(c, g): rr(c, g).loc[:IS_END] for c, g in grid}
            for chooser, fn in (("C_ISSHARPE", sharpe), ("C_ISCAGR", cagr)):
                pick = max(grid, key=lambda k: fn(IS[k]))
                ro = rr(*pick).loc[OOS_START:]
                wf.append(dict(panel=panel, bps=bps, chooser=chooser,
                               pick_cap=capname(pick[0]), pick_gross=pick[1],
                               OOS_CAGR=cagr(ro), OOS_Sharpe=sharpe(ro), OOS_MaxDD=maxdd(ro),
                               SPY_OOS_CAGR=cagr(oos(spy_r)), SPY_OOS_Sharpe=sharpe(oos(spy_r)),
                               SPY_OOS_MaxDD=maxdd(oos(spy_r)),
                               EWBH_OOS_CAGR=cagr(oos(ew_r)), EWBH_OOS_Sharpe=sharpe(oos(ew_r)),
                               EWBH_OOS_MaxDD=maxdd(oos(ew_r)),
                               LIVE_OOS_CAGR=cagr(oos(live_r)), LIVE_OOS_Sharpe=sharpe(oos(live_r)),
                               LIVE_OOS_MaxDD=maxdd(oos(live_r)),
                               beats_SPY_OOS=bool(sharpe(ro) > sharpe(oos(spy_r))),
                               beats_EWBH_OOS_Sharpe=bool(sharpe(ro) > sharpe(oos(ew_r))),
                               beats_EWBH_OOS_CAGR=bool(cagr(ro) >= cagr(oos(ew_r))),
                               beats_LIVE_OOS=bool(sharpe(ro) > sharpe(oos(live_r)))))

        # ---- panel benchmark table at the headline rung
        ew_h = ew_r0 - ew_t * HEADLINE_RUNG / 1e4
        live_h = live_r0 - live_t * HEADLINE_RUNG / 1e4
        say(f"\n--- {panel}: comparands at {HEADLINE_RUNG:.0f} bps (scored from {start.date()}) ---")
        for nm, s in (("SPY", spy), ("EWBH", ew_h), ("EWBH_NOSWEEP", ewn_r0 - ew_t * HEADLINE_RUNG / 1e4),
                      ("RULES v2 (live)", live_h)):
            h1, h2 = halves(s)
            say(f"    {nm:16s} CAGR {cagr(s):7.2%}  Sharpe {sharpe(s):6.4f}  MaxDD {maxdd(s):7.2%}  "
                f"H1/H2 {h1:5.2f}/{h2:5.2f}  OOS Sharpe {sharpe(s.loc[OOS_START:]):6.4f}  OOS CAGR {cagr(s.loc[OOS_START:]):7.2%}")

    df = pd.DataFrame(rows); gp = pd.DataFrame(gapsum); wfd = pd.DataFrame(wf)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    gp.to_csv(f"{OUT}.gap.csv", index=False)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)

    # ---------------------------------------------------------------- headline reporting
    say(f"\n=== THE GROSS LADDER AT {HEADLINE_RUNG:.0f} bps (the headline rung) ===")
    h = df[df.bps == HEADLINE_RUNG]
    for panel in ("U56", "B136"):
        say(f"\n--- {panel} ---")
        say("     cap    gross     CAGR   Sharpe    MaxDD    H1/H2      OOS_Sh   turn/yr  risk_g  4a  4bSPY  4bEWBHstrict")
        for _, r in h[h.panel == panel].iterrows():
            say(f"    {r['cap']:>5s}   {r['gross']:.2f}  {r['CAGR']:7.2%}  {r['Sharpe']:6.4f}  {r['MaxDD']:7.2%}  "
                f"{r['H1']:5.2f}/{r['H2']:5.2f}  {r['OOS_Sharpe']:6.4f}  {r['turnover_per_yr']:6.2f}x  "
                f"{r['mean_risk_gross']:5.3f}   {int(r['pass4a'])}    {int(r['pass4b_SPY'])} {r['legs4b_SPY']}   "
                f"{int(r['pass4b_EWBH_strict'])} {r['legs4b_EWBH_strict']}")

    say("\n=== THE IDEA'S OWN QUESTION: THE GROSS AT WHICH THE BOOK'S CAGR REACHES EWBH's ===")
    say("    panel   cap   bps   EWBH_CAGR   best_CAGR_on_ladder   shortfall   g_reaching   MaxDD_there   DDleg_ok")
    for _, r in gp.iterrows():
        gg = "none" if not np.isfinite(r["g_reaching_EWBH_CAGR"]) else f"{r['g_reaching_EWBH_CAGR']:.2f}"
        md = "   n/a  " if not np.isfinite(r["MaxDD_at_that_g"]) else f"{r['MaxDD_at_that_g']:7.2%}"
        say(f"    {r['panel']:5s} {r['cap']:>5s} {r['bps']:5.0f}   {r['EWBH_CAGR']:7.2%}      {r['best_CAGR_on_ladder']:7.2%}"
            f"         {r['CAGR_shortfall_at_best']:+7.2%}      {gg:>5s}      {md}     {int(bool(r['DDleg_ok_there']))}")
    n_close = int(np.isfinite(gp["g_reaching_EWBH_CAGR"]).sum())
    n_close_ok = int((np.isfinite(gp["g_reaching_EWBH_CAGR"]) & gp["DDleg_ok_there"]).sum())
    say(f"\n    CELLS WHERE SOME ATTAINABLE GROSS CLOSES THE CAGR GAP: {n_close} of {len(gp)}"
        f"   ... AND AT A MaxDD THE 4b DD LEG ACCEPTS: {n_close_ok} of {len(gp)}")
    publish("gross-ladder closes the EWBH CAGR gap", f"{n_close} of {len(gp)} (panel x cap x rung) cells")
    publish("...at a 4b-acceptable MaxDD", f"{n_close_ok} of {len(gp)} cells")

    # ---------------------------------------------------------------- the leverage counterfactual
    say("\n=== THE LEVERAGE COUNTERFACTUAL (PUBLISHED, NOT PROPOSED — PROTOCOL rule 2 forbids it) ===")
    say("    The ladder cannot exceed 1.00 book gross, so ask instead: what MULTIPLE L of the")
    say("    book's daily return would be needed to reach EWBH's CAGR, and what MaxDD does it carry?")
    say("    Financing is charged at ZERO, which is generous to the book.")
    say("    panel   cap   L_needed   CAGR at L   MaxDD at L   EWBH MaxDD   Sharpe at L (unchanged)")
    lev_rows = []
    hh = df[df.bps == HEADLINE_RUNG]
    for panel in ("U56", "B136"):
        for cap in [capname(c) for c in CAPS]:
            sub = hh[(hh.panel == panel) & (hh.cap == cap)]
            best = sub.loc[sub.CAGR.idxmax()]
            key = (panel, cap, best["gross"])
            r = SERIES[key]
            tgt = float(gp[(gp.panel == panel) & (gp.cap == cap) & (gp.bps == HEADLINE_RUNG)].EWBH_CAGR.iloc[0])
            lo, hi = 1.0, 8.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if cagr(mid * r) < tgt: lo = mid
                else: hi = mid
            L = 0.5 * (lo + hi)
            ewdd = float(gp[(gp.panel == panel) & (gp.cap == cap) & (gp.bps == HEADLINE_RUNG)].EWBH_MaxDD.iloc[0])
            lev_rows.append(dict(panel=panel, cap=cap, gross=best["gross"], L_needed=L,
                                 CAGR_at_L=cagr(L * r), MaxDD_at_L=maxdd(L * r), EWBH_MaxDD=ewdd,
                                 Sharpe_at_L=sharpe(L * r)))
            say(f"    {panel:5s} {cap:>5s}    {L:5.2f}x    {cagr(L * r):7.2%}     {maxdd(L * r):7.2%}     {ewdd:7.2%}      {sharpe(L * r):6.4f}")
    pd.DataFrame(lev_rows).to_csv(f"{OUT}.leverage.csv", index=False)
    say(f"    MEDIAN LEVERAGE NEEDED: {np.median([r['L_needed'] for r in lev_rows]):.2f}x; "
        f"MaxDD at that leverage is worse than EWBH's in "
        f"{sum(1 for r in lev_rows if r['MaxDD_at_L'] < r['EWBH_MaxDD'])} of {len(lev_rows)} cells.")

    say("\n=== BOTH KEEP PATHS OVER ALL ROWS ===")
    say(f"    rows {len(df)}   4a {int(df.pass4a.sum())}   4b vs SPY {int(df.pass4b_SPY.sum())}   "
        f"4b-PROTO vs EWBH {int(df.pass4b_EWBH_proto.sum())}   4b-STRICT vs EWBH {int(df.pass4b_EWBH_strict.sum())}   "
        f"4b-STRICT vs EWBH_NOSWEEP {int(df.pass4b_EWBHNOSWEEP_strict.sum())}")
    for panel in ("U56", "B136"):
        d = df[df.panel == panel]
        say(f"    {panel}: 4a {int(d.pass4a.sum())}/{len(d)}   4bSPY {int(d.pass4b_SPY.sum())}/{len(d)}   "
            f"4bEWBHproto {int(d.pass4b_EWBH_proto.sum())}/{len(d)}   4bEWBHstrict {int(d.pass4b_EWBH_strict.sum())}/{len(d)}")
    say("    binding leg counts on the 4b-vs-SPY FAILS (L_H1 L_H2 L_OOS L_DD L_CAGR):")
    f = df[~df.pass4b_SPY]
    if len(f):
        cnt = np.zeros(5, int)
        for s in f.legs4b_SPY:
            for i, ch in enumerate(s):
                cnt[i] += (ch == "0")
        say(f"      {dict(zip(['L_H1','L_H2','L_OOS','L_DD','L_CAGR'], cnt.tolist()))} over {len(f)} fail rows")
    f2 = df[~df.pass4b_EWBH_strict]
    cnt2 = np.zeros(5, int)
    for s in f2.legs4b_EWBH_strict:
        for i, ch in enumerate(s):
            cnt2[i] += (ch == "0")
    say(f"    binding leg counts on the 4b-STRICT-vs-EWBH FAILS: "
        f"{dict(zip(['L_H1','L_H2','L_OOS','L_DD','L_CAGR'], cnt2.tolist()))} over {len(f2)} fail rows")
    say(f"    rows ahead of EWBH on CAGR: {int((df.CAGR.values >= [gp[(gp.panel==r.panel)&(gp.cap==r.cap)&(gp.bps==r.bps)].EWBH_CAGR.iloc[0] for r in df.itertuples()]).sum())} of {len(df)}")

    say("\n=== RULE 8 (walk-forward): (g, cap) fitted on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    say("    panel  bps  chooser      pick(cap,g)     OOS CAGR / Sharpe / MaxDD      vs SPY OOS            vs EWBH OOS           vs LIVE OOS")
    for _, r in wfd.iterrows():
        say(f"    {r['panel']:5s} {r['bps']:4.0f}  {r['chooser']:10s}  ({r['pick_cap']:>5s}, {r['pick_gross']:.2f})   "
            f"{r['OOS_CAGR']:7.2%} / {r['OOS_Sharpe']:6.4f} / {r['OOS_MaxDD']:7.2%}   "
            f"{r['SPY_OOS_CAGR']:7.2%}/{r['SPY_OOS_Sharpe']:6.4f}/{r['SPY_OOS_MaxDD']:7.2%}  "
            f"{r['EWBH_OOS_CAGR']:7.2%}/{r['EWBH_OOS_Sharpe']:6.4f}/{r['EWBH_OOS_MaxDD']:7.2%}  "
            f"{r['LIVE_OOS_CAGR']:7.2%}/{r['LIVE_OOS_Sharpe']:6.4f}/{r['LIVE_OOS_MaxDD']:7.2%}")
    say(f"    picks beating SPY OOS Sharpe: {int(wfd.beats_SPY_OOS.sum())} of {len(wfd)}; "
        f"beating EWBH OOS Sharpe: {int(wfd.beats_EWBH_OOS_Sharpe.sum())} of {len(wfd)}; "
        f"EWBH OOS CAGR: {int(wfd.beats_EWBH_OOS_CAGR.sum())} of {len(wfd)}; "
        f"LIVE OOS Sharpe: {int(wfd.beats_LIVE_OOS.sum())} of {len(wfd)}")

    ng = pd.DataFrame(GATES)
    say(f"\nGATES {int(ng.pass_.sum())} of {len(ng)} PASS")
    say(f"SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; the CAGR legs")
    say(f"    (the book's and EWBH's alike) are contaminated. The gross-vs-gross contrast is same-tape,")
    say(f"    same-names, same-days and first-order immune.")
    say(f"\nelapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
