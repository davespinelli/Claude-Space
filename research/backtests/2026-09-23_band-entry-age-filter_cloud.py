#!/usr/bin/env python3
"""idea 2439 (lane cloud, run 55, 2026-09-23) — does a BAND ENTRY-AGE FILTER cut the CAPPED
candidate's TURNOVER where every EXIT-SIDE device failed?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (every name INSIDE the 200d +/-3% band held
at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b KEEP-candidate;
idea 2322 added a 2.0% per-name cap (`CAP2`).  Its ONE stated adoption blocker is realised
turnover: 3.51 turns/yr against the live book's 1.77 (re-measured 2.79 by idea 2463).

THE DEVICE.  Every turnover device the record has closed acts on the EXIT or the RE-SIZE:
the weight-drift no-trade band (2328), the minimum hold (2351), the partial-adjustment damper
(2391 / 2404), the calendar rota (2408), book width (2467), band width (2318 / 2343).  AGE
acts on ADMISSION and nothing else:

    a name may be held only once its 200d band state has been IN continuously for `a`
    sessions (today included).  The exit side is untouched.  Weights are the committed
    `min(gross / N_adm, cap)` and the residual still sweeps to SHY at phi = 1.00.

Rationale as filed: a name admitted on day 1 of a crossing is the one most likely to cross
back, so the cheapest turnover may be the trade never opened — and if admission age also
delays entry into the 2009 / 2020 rebounds it shows up directly in `L_DD` and `L_CAGR`.

DIAL 1 -- entry age `a` {0 (committed), 5, 10, 21, 42} trading days.  `a = 0` IS CAP2/CAND
          exactly (gate G1), so one ladder spans the known book.
DIAL 2 -- gross ceiling `g` {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03, MA 200d, t+1 execution, the
phi = 1.00 SHY sweep.  5 x 2 x 2 x 2 = 40 weight paths, every one published at every rung
= 160 rows.  SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 /
2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass
there to keep.

THE RUN IS NOT VIRGIN AND SAYS SO BEFORE IT STARTS.  Idea 2463 (lane C, run 54) re-implemented
AGE as one of nine devices inside a cross-device frontier engine and published 64 CAP2 rows
plus a pooled median of -0.064 pp of CAGR per 1% of turnover saved, reading AGE a DE-GROSSER.
It never closed 2439 on its own terms (no '## Done' entry, no LEADERBOARD row, no walk-forward
of the age dial).  This run therefore (a) treats 2463's 64 published AGE rows as a CROSS-LANE
REPRODUCTION GATE (G11, asserted to 1e-9), (b) adds the `CAND` book, the `a = 0` anchor and
the exposure decomposition 2463 did not publish per cell, and (c) runs rule 8 on the age dial
itself.  Anything it confirms is labelled a CONFIRMATION, not a discovery.

THE DEVICE'S OWN BILL IS MEASURED, NOT ASSUMED.  Section E publishes, at every (panel, book,
gross, a): realised turnover/yr, mean realised RISK gross, mean names held, mean band-IN count,
mean sweep weight, max/median per-name weight, and the admission LAG (held cells the band says
are IN but the age filter blocks).  A turnover cut bought by holding less is not a turnover cut.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (a, g) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_band-entry-age-filter_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "band-entry-age-filter", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
AGES = [0, 5, 10, 21, 42]
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
FRONTIER = Path(__file__).resolve().parent / "2026-09-23_cagr-per-turnover-frontier_C.grid.csv"

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
def admitted(px, invest, age):
    """The admitted set under an entry age of `age` sessions.  `base` is clause-2's hysteresis
    state (baseline.band_state), so a held name's state stays True through a whole spell and
    the age is served once, at entry; a name that leaves the band must serve it again.
    Definition is idea 2463's verbatim, so the two lanes are comparable cell for cell."""
    q = px[invest]
    pr = q.notna()
    base = band_state(q, BAND) & pr
    adm = base
    if age:
        adm = adm & (base.astype(float).rolling(int(age)).sum() >= int(age))
    return adm, base


def age_weights(px, invest, cap, gross, age):
    adm, base = admitted(px, invest, age)
    nadm = adm.sum(axis=1).replace(0, np.nan)
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=adm.index)
    per = pd.concat([gross / nadm, c], axis=1).min(axis=1)
    w = adm.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w, adm, base


def cap_weights_independent(px, invest, cap, gross):
    """An INDEPENDENT construction of idea 2322's CAP2 / idea 2300's CAND with no reference to
    the age code path at all — the object gate G1 asserts `a = 0` against."""
    q = px[invest]
    inb = band_state(q, BAND) & q.notna()
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, np.inf if cap == "INF" else float(cap))
    w = inb.astype(float).mul(pd.Series(per, index=q.index).fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def run(px, w, freq=CADENCE):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return dict(r0=res["returns"], turnover=res["turnover"], held=res["weights"])


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


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


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


def main():
    t0 = time.time()
    say("=== idea 2439 (lane cloud, run 55) — does a BAND ENTRY-AGE FILTER cut the capped candidate's 3.51x turnover? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  MA 200d  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 entry age a {AGES} sessions   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "entry age a, gross g", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G9 all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead} -> {len(invest) - len(dead)} priced names")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: a = 0 IS the committed book, bit-for-bit, against an INDEPENDENT construction
    for pn, (px, invest) in panels.items():
        for bk, cap in BOOKS.items():
            for g in GROSSES:
                w0, _, _ = age_weights(px, invest, cap, g, 0)
                wc = cap_weights_independent(px, invest, cap, g)
                d1 = float((w0 - wc).abs().max().max())
                r_eng = backtest(px, wc, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                d1b = float((r_eng - priced(run(px, w0), HEADLINE_RUNG)).abs().max())
                gate(f"G1 a=0 == an independent CAP/CAND construction ({pn}, {bk}, g={g:.2f})",
                     f"max|dw| {d1:.3e}; max|dr| vs engine.backtest {d1b:.3e}", "< 1e-12",
                     d1 < 1e-12 and d1b < 1e-12)

    # ---- G10: no lookahead — weights up to a cut date are invariant to the future tape
    px_u, inv_u = panels["U56"]
    cut = "2018-06-29"
    px2 = px_u.copy()
    px2.loc[px2.index > cut] = px2.loc[px2.index > cut] * 1.5
    wa, _, _ = age_weights(px_u, inv_u, 0.020, 0.75, 21)
    wb, _, _ = age_weights(px2, inv_u, 0.020, 0.75, 21)
    dlk = float((wa.loc[:cut] - wb.loc[:cut]).abs().max().max())
    gate("G10 no lookahead (future tape x1.5 after 2018-06-29 leaves every earlier weight identical)",
         f"max|dw| on rows <= {cut}: {dlk:.3e}", "< 1e-15", dlk < 1e-15)

    # ---- G12: the dial binds in the direction it claims — no admitted spell shorter than `a`
    #      and admission is a SUBSET of the band state at every age.
    viol_sub, viol_len = 0, 0
    for a in AGES[1:]:
        adm, base = admitted(px_u, inv_u, a)
        viol_sub += int((adm & ~base).values.sum())
        av = adm.values
        bv = base.values
        for j in range(av.shape[1]):
            starts = np.flatnonzero(av[1:, j] & ~av[:-1, j]) + 1
            for s0 in starts:                      # every admission must sit on >= a in-band days
                if not bv[max(0, s0 - a + 1):s0 + 1, j].all():
                    viol_len += 1
    gate("G12 the age filter binds (admitted is a subset of the band state; every admission carries a in-band days)",
         f"{viol_sub} subset violations, {viol_len} short admissions over a in {AGES[1:]}", "0 and 0",
         viol_sub == 0 and viol_len == 0)

    # ---------------------------------------------------------------- the grid
    rows, ex_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        publish(f"{pname} SPY bars", f"CAGR {cagr(spy):.4%}  Sharpe {sharpe(spy):.4f}  MaxDD {maxdd(spy):.4%}"
                                     f"  halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}"
                                     f"  OOS {cagr(spy_oos):.4%}/{sharpe(spy_oos):.4f}"
                                     f"  4b bars: DD >= {DD_CAP * maxdd(spy):.4%}, CAGR >= {CAGR_FLOOR * cagr(spy):.4%}")
        publish(f"{pname} live RULES v2 bars", f"CAGR {cagr(base_r):.4%}  Sharpe {sharpe(base_r):.4f}"
                                               f"  MaxDD {maxdd(base_r):.4%}  halves {halves(base_r)[0]:.4f}/{halves(base_r)[1]:.4f}")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                for a in AGES:
                    w, adm, base = age_weights(px, invest, cap, gross, a)
                    res = run(px, w)
                    hw = res["held"].drop(columns=[SWEEP]).loc[win]
                    pos = hw.values[hw.values > 1e-12]
                    admv, basev = adm.loc[win].values, base.loc[win].values
                    ex_rows.append(dict(panel=pname, book=bk, gross=gross, age=a,
                                        turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                        mean_names_adm=float(admv.sum(axis=1).mean()),
                                        mean_names_band=float(basev.sum(axis=1).mean()),
                                        blocked_share=float((basev & ~admv).sum() / max(1, basev.sum())),
                                        mean_risk_gross=float(hw.values.sum(axis=1).mean()),
                                        mean_gross=float(res["held"].loc[win].sum(axis=1).mean()),
                                        mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                                        med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                        max_row_sum=float(res["held"].sum(axis=1).max())))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, book=bk, gross=gross, age=a, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                         mean_risk_gross=float(hw.values.sum(axis=1).mean()),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); ef = pd.DataFrame(ex_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); ef.to_csv(f"{OUT}.exposure.csv", index=False)

    # ---- G2: external reproduction of the committed U56 headline at a = 0
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75) & (df.age == 0)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    tgt = dict(CAGR=0.1162, Sharpe=1.2687, MaxDD=-0.1481, OOS_CAGR=0.1277, OOS_Sharpe=1.3318, turnover_yr=3.51)
    d2 = max(abs(h[k] - v) for k, v in tgt.items())
    gate("G2 reproduces the committed CAP2 U56 headline (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, 3.51x)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" {h.turnover_yr:.2f}x; max|d| {d2:.3e}", "< 5e-3 (price-cache vintage residual)", d2 < 5e-3)

    # ---- G11: CROSS-LANE reproduction of idea 2463's 64 published AGE rows (CAP2 only)
    if FRONTIER.exists():
        fr = pd.read_csv(FRONTIER)
        fr = fr[(fr.device == "AGE")].copy()
        mine = df[df.book == "CAP2"].copy()
        m = fr.merge(mine, left_on=["panel", "gross", "strength", "cost_bps"],
                     right_on=["panel", "gross", "age", "cost_bps"], suffixes=("_C", "_here"))
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe"]
        dmax = max(float((m[f"{c}_C"] - m[f"{c}_here"]).abs().max()) for c in cols)
        gate("G11 cross-lane reproduction of idea 2463's published AGE rows (lane C, run 54)",
             f"{len(m)} of 64 rows matched, max|d| over {cols} = {dmax:.3e}", "64 rows, < 1e-9",
             len(m) == 64 and dmax < 1e-9)
    else:
        gate("G11 cross-lane reproduction of idea 2463's AGE rows", "frontier grid not on disk", "present", False)

    # ---- G4: no leverage anywhere
    gate("G4 no leverage (max row sum over all 40 weight paths)", f"{ef.max_row_sum.max():.9f}", "<= 1.0 + 1e-9",
         ef.max_row_sum.max() <= 1.0 + 1e-9)

    # ---- G5: the dial bites and in which direction
    bite = ef[(ef.book == "CAP2") & (ef.gross == 0.75)].pivot(index="age", columns="panel", values="mean_names_adm")
    gate("G5 the dial bites (mean admitted names strictly falls with a, both panels)",
         "; ".join(f"{p}: " + " -> ".join(f"{v:.2f}" for v in bite[p]) for p in bite.columns),
         "strictly decreasing", bool(all(bite[p].is_monotonic_decreasing and bite[p].nunique() == len(AGES)
                                         for p in bite.columns)))

    # ---------------------------------------------------------------- section E: the bill
    say("\n=== E. THE DEVICE'S OWN BILL (CAP2, gross 0.75, headline rung) ===")
    say("  panel  a   turn/yr   d_turn    names_adm  names_band  blocked  risk_gross  sweep_w  max_w   CAGR    dCAGR   pp/1%")
    for pname in panels:
        e = ef[(ef.panel == pname) & (ef.book == "CAP2") & (ef.gross == 0.75)].set_index("age")
        g = df[(df.panel == pname) & (df.book == "CAP2") & (df.gross == 0.75)
               & (df.cost_bps == HEADLINE_RUNG)].set_index("age")
        t0_, c0_ = e.loc[0, "turnover_yr"], g.loc[0, "CAGR"]
        for a in AGES:
            dt = (e.loc[a, "turnover_yr"] / t0_ - 1) * 100
            dc = (g.loc[a, "CAGR"] - c0_) * 100
            rate = dc / (-dt) if abs(dt) > 1e-9 else np.nan
            say(f"  {pname:5s} {a:3d}  {e.loc[a,'turnover_yr']:7.3f}  {dt:+7.2f}%  {e.loc[a,'mean_names_adm']:8.2f}"
                f"  {e.loc[a,'mean_names_band']:10.2f}  {e.loc[a,'blocked_share']:7.3f}"
                f"  {e.loc[a,'mean_risk_gross']:10.4f}  {e.loc[a,'mean_sweep_w']:7.4f}"
                f"  {e.loc[a,'max_name_w']:6.4f}  {g.loc[a,'CAGR']:6.2%}  {dc:+6.2f}  {rate:+6.3f}")

    # ---- the adoption bar (idea 2431): -31.0% of turnover at unchanged returns
    bar_rows = []
    for (pn, bk, gr), sub in ef.groupby(["panel", "book", "gross"]):
        s = sub.set_index("age")
        g = df[(df.panel == pn) & (df.book == bk) & (df.gross == gr)
               & (df.cost_bps == HEADLINE_RUNG)].set_index("age")
        for a in AGES[1:]:
            bar_rows.append(dict(panel=pn, book=bk, gross=gr, age=a,
                                 d_turn_pct=(s.loc[a, "turnover_yr"] / s.loc[0, "turnover_yr"] - 1) * 100,
                                 d_CAGR_pp=(g.loc[a, "CAGR"] - g.loc[0, "CAGR"]) * 100,
                                 d_risk_gross=s.loc[a, "mean_risk_gross"] - s.loc[0, "mean_risk_gross"],
                                 clears_bar=bool((s.loc[a, "turnover_yr"] / s.loc[0, "turnover_yr"] - 1) * 100 <= -31.0
                                                 and g.loc[a, "CAGR"] >= g.loc[0, "CAGR"])))
    bf = pd.DataFrame(bar_rows); bf.to_csv(f"{OUT}.bar.csv", index=False)
    publish("idea 2431's adoption bar (-31.0% turnover at dCAGR >= 0), cleared by",
            f"{int(bf.clears_bar.sum())} of {len(bf)} age arms; best turnover cut {bf.d_turn_pct.min():+.2f}%"
            f" at dCAGR {bf.loc[bf.d_turn_pct.idxmin(), 'd_CAGR_pp']:+.2f} pp")
    med_rate = float(np.median([r.d_CAGR_pp / (-r.d_turn_pct) for r in bf.itertuples() if r.d_turn_pct < -1e-9]))
    publish("pooled median pp of CAGR per 1% of turnover saved (this run's AGE reading)",
            f"{med_rate:+.4f} (idea 2463 published -0.064 for AGE pooled over its own strength set)")

    # ---------------------------------------------------------------- KEEP paths
    say("\n=== F. KEEP PATHS OVER ALL 160 ROWS ===")
    say(f"  4b {int(df.pass4b.sum())} of {len(df)};  4a {int(df.pass4a.sum())} of {len(df)}")
    for k in ("panel", "book", "gross", "age", "cost_bps"):
        say(f"    by {k}: " + "  ".join(f"{v}:{int(s.pass4b.sum())}/{len(s)}" for v, s in df.groupby(k)))
    for leg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"    4b leg {leg} fails on {int((~df[leg]).sum())} of {len(df)} rows")
    joint = []
    for (bk, gr, a, c), s in df.groupby(["book", "gross", "age", "cost_bps"]):
        if len(s) == 2 and bool(s.pass4b.all()):
            joint.append((bk, gr, a, c))
    say(f"  JOINT both-panel 4b: {len(joint)} of {len(df) // 2} cells")
    say("    " + ", ".join(f"{bk}/g{gr:.2f}/a{a}/{int(c)}bps" for bk, gr, a, c in joint) if joint else "    (none)")

    # ---------------------------------------------------------------- rule 8
    say("\n=== G. RULE 8 WALK-FORWARD — (a, g) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        base_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for rung in RUNGS:
                sub = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung)]
                anch = sub[(sub.age == 0) & (sub.gross == 0.75)].iloc[0]
                for cn, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = sub.loc[sub[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=cn,
                                   pick_age=int(pick.age), pick_gross=float(pick.gross),
                                   OOS_CAGR=float(pick.OOS_CAGR), OOS_Sharpe=float(pick.OOS_Sharpe),
                                   OOS_MaxDD=float(pick.OOS_MaxDD), turnover_yr=float(pick.turnover_yr),
                                   anchor_OOS_CAGR=float(anch.OOS_CAGR), anchor_OOS_Sharpe=float(anch.OOS_Sharpe),
                                   anchor_turnover=float(anch.turnover_yr),
                                   d_OOS_Sharpe=float(pick.OOS_Sharpe - anch.OOS_Sharpe),
                                   beats_SPY_OOS=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                   beats_live_OOS=bool(pick.OOS_Sharpe > sharpe(base_oos)),
                                   SPY_OOS_Sharpe=sharpe(spy_oos), live_OOS_Sharpe=sharpe(base_oos),
                                   full_pass4b=bool(pick.pass4b)))
    wdf = pd.DataFrame(wf); wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wdf)} picks: age 0 in {int((wdf.pick_age == 0).sum())}, "
        + ", ".join(f"a{a} in {int((wdf.pick_age == a).sum())}" for a in AGES[1:]))
    say(f"  mean d(OOS Sharpe) vs the committed a=0/g0.75 anchor {wdf.d_OOS_Sharpe.mean():+.4f};"
        f" picks beat the anchor OOS in {int((wdf.d_OOS_Sharpe > 0).sum())} of {len(wdf)}")
    say(f"  picks beat SPY OOS Sharpe in {int(wdf.beats_SPY_OOS.sum())} of {len(wdf)};"
        f" the live book's in {int(wdf.beats_live_OOS.sum())} of {len(wdf)};"
        f" carry a full-sample 4b in {int(wdf.full_pass4b.sum())} of {len(wdf)}")
    say(f"  mean turnover at the pick {wdf.turnover_yr.mean():.3f}x vs the anchor's {wdf.anchor_turnover.mean():.3f}x")
    publish("RULE 8 age-dial pick distribution",
            ", ".join(f"a={a}: {int((wdf.pick_age == a).sum())}" for a in AGES))

    # ---------------------------------------------------------------- close
    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gdf.pass_.sum()); ntot = len(gdf)
    say(f"\n=== GATES: {npass} of {ntot} pass ===")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {bool(gdf.pass_.all())}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
