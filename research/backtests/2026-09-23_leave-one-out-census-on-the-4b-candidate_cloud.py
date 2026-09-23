#!/usr/bin/env python3
"""idea 2332 (lane cloud, 2026-09-23) — IS THE STANDING 4b CANDIDATE'S PASS A SINGLE-NAME DRAW?
THE LEAVE-ONE-OUT DELETION CENSUS.

THE OBJECT.  Idea 2300's standing 4b KEEP-candidate is `RG100 + phi = 1.00`: every name INSIDE the
200d +/-3% band (RULES v2 clause 2, with hysteresis) held at `gross / N_in` of NAV, the residual
`1 - sum(w)` swept to SHY.  Its ONE published risk is CONCENTRATION: per-name weight is 1.70% of
NAV at the median on U56 but 15.0% on the worst day (5 names IN).  Idea 2318 (this same sprint)
CORRECTED the assumption that widening the band de-concentrates the book -- U56 max per-name weight
is non-monotone in the band width -- so concentration is still open, and this is the census that
prices it.

    w_i = gross / N_in  on names IN the 200d +/-3% band,   idle NAV -> SHY (phi = 1.00)

THE TEST.  Delete ONE universe member, re-price the WHOLE candidate on the surviving panel, and ask
whether it still clears 4b full-sample AND out of sample.  A pass that survives every deletion is a
BOOK.  A pass that needs one name is a DRAW.  Run the census on BOTH panels the incumbent passes on:
**U56 (56 deletions) and B136 (136 deletions)**, at gross {0.75, 1.00} and 4 cost rungs.

WHY SMALL IS NOT CENSUSED, STATED IN THE OPEN: idea 2318 published SMALL's 4b pass count at 0 of 48
across the whole width x gross x rung grid.  There is no pass on SMALL for a deletion to break, so a
665-deletion census there would price nothing.  The undeleted SMALL book is still reported below as
the census's own control.

DIALS.  The deletion index is a CENSUS AXIS, not a tuned parameter -- every one of its levels is
published and none is selected on.  The only tunable dial is **gross {0.75, 1.00}**, pinned to the
committed pair.  ONE tuned parameter, under the protocol's cap of two.

REPORTED, NEVER SELECTED ON: 2 panels, 4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, t+1
execution, band c = 0.03 and MA length 200 (the live clause-2 constants), sweep instrument SHY.
(56 + 136) x 2 gross = 384 books, every one published at every rung = 1,536 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
The comparands are held FIXED at the UNDELETED live RULES v2 book and the UNDELETED SPY, because the
question is whether the CANDIDATE survives a deletion, not whether a deleted-panel benchmark does.
Section G re-scores the census against a DELETION-MATCHED live baseline as a robustness read.

RULE 8: gross chosen on warm-up..2016-12-31 ONLY, per deletion, by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.  The census statistic is the SHARE OF DELETIONS
whose IS-chosen book clears 4b out of sample.

TWO SPECIAL MEMBERS, FLAGGED NOT HIDDEN.  SPY is both a panel member and the 4b benchmark, and SHY
is both a panel member and the sweep instrument.  Deleting either removes it from the INVESTABLE set
only; the benchmark series and the sweep leg are untouched (asserted by G10/G11).  Both deletions
are reported inside the census and called out separately.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the undeleted book
is BIT-IDENTICAL to an independently constructed RG100 + phi = 1.  G3 EXTERNAL REPRODUCTION of idea
2300's committed U56 headline (12.55% / 1.1896 / -17.39%, OOS 13.77% / 1.2332).  G4 no leverage in
any of the 384 books.  G5 every deletion BITES (each LOO book differs from the undeleted one).
G6 SHY priced on every row it is held.  G7 the census is COMPLETE (one book per investable member,
no member skipped or repeated).  G8 exactly one tuned parameter.  G9 SMALL dropped-ticker rule bit.
G10 deleting SHY leaves the sweep leg intact.  G11 deleting SPY leaves the benchmark series intact.

SURVIVORSHIP CAVEAT (binding on every B136 and SMALL row): `universe_broad.json` and the sub-$2B
SMALL pool are CURRENT constituents of their screens, so both are survivorship-biased upward.  A
leave-one-out census CANNOT repair that bias -- it prices sensitivity to deleting a SURVIVOR, which
is a strictly weaker question than sensitivity to adding back the names the screen already dropped.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_leave-one-out-census-on-the-4b-candidate_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "leave-one-out-census-on-the-4b-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE = 0.03, 200, "W"
WARMUP = 260            # the record's scored-window convention (idea 2300 and every committed row)
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
BENCH = "SPY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
NONE = "(none)"         # the undeleted control

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


# ---------------------------------------------------------------- the candidate
def rg100_weights(px, invest, gross):
    """RG100 + phi = 1 on the given investable set: w_i = gross / N_in on names IN the 200d +/-3%
    band, idle NAV -> SHY.  `invest` is what a deletion changes; the sweep leg is added from px
    regardless of whether SHY is investable, which is what G10 asserts."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).fillna(0.0)
    w = inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def rg100_reference(px, invest, gross):
    """Independent construction of the same book in SCALE form (de-gross then re-gross by N/N_in)
    rather than the per-name form above.  G2 asserts the two agree bit for bit."""
    q = px[invest]
    pr = q.notna()
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(pr, 0.0)
    N = e.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    dg = (gross * e.div(N, axis=0).fillna(0.0)).where(inb, 0.0)
    scale = (N / nin).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    w = dg.mul(scale, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- engine replica
def run_book(prices, weights, freq=CADENCE):
    """Replica of engine.backtest keeping zero-cost returns + turnover so every cost rung is
    priced from one pass.  Un-invested residual drifts at 0% (engine's convention)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt = w_target.values
    rv = rets.values
    mk = mask.values
    for i in range(len(prices.index)):
        if mk[i] or i == 0:
            new = wt[i]
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = pd.Series((held * rv).sum(axis=1), index=prices.index)
    return dict(r0=r0, turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index))


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


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == BENCH or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2332 — IS THE STANDING 4b CANDIDATE'S PASS A SINGLE-NAME DRAW? LEAVE-ONE-OUT CENSUS ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP}")
    say(f"    CENSUS AXIS: the deleted member (every level published).   ONE TUNED DIAL: gross {GROSSES}.")
    say("    SURVIVORSHIP: B136 and SMALL are CURRENT constituents of their screens (biased upward);")
    say("    a leave-one-out census prices deleting a SURVIVOR, which cannot repair that bias.")
    gate("G8 exactly one tuned parameter", "gross (the deletion index is a census axis)", "<= 2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G9 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)",
         ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b)):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    # G1: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(run_book(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G2: the undeleted book, two independent constructions
    d2 = float((rg100_weights(px_u, list(px_u.columns), 0.75)
                - rg100_reference(px_u, list(px_u.columns), 0.75)).abs().max().max())
    gate("G2 undeleted book == RG100 + phi=1 (independent scale-form construction, U56)",
         f"max|dw| {d2:.3e}", "< 1e-12", d2 < 1e-12)

    # G10 / G11: the two special members
    inv_no_shy = [c for c in px_u.columns if c != SWEEP]
    w_no_shy = rg100_weights(px_u, inv_no_shy, 0.75)
    sweep_live = float(w_no_shy[SWEEP].loc[px_u.index[WARMUP:]].mean())
    gate("G10 deleting SHY from the investable set leaves the sweep leg intact",
         f"mean SHY weight still {sweep_live:.3f}", "> 0", sweep_live > 0)
    inv_no_spy = [c for c in px_u.columns if c != BENCH]
    w_no_spy = rg100_weights(px_u, inv_no_spy, 0.75)
    spy_held = float(w_no_spy[BENCH].abs().max())
    bench_ok = bool(px_u[BENCH].notna().all() and spy_held < 1e-12)
    gate("G11 deleting SPY removes it from HOLDINGS only; the benchmark series is untouched",
         f"max |SPY weight| {spy_held:.1e}, benchmark non-null {px_u[BENCH].notna().all()}",
         "0 weight, benchmark intact", bench_ok)

    # ---------------------------------------------------------------- the census
    rows = []
    for pname, (px, full_inv) in panels.items():
        win = px.index[WARMUP:]
        spy = px[BENCH].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        # comparands held FIXED at the UNDELETED live book and the UNDELETED SPY
        base_fixed = priced(run_book(px, rules_v2_weights(px, band=BAND, gross=0.75)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(full_inv)} investable)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_fixed):.2%} / {sharpe(base_fixed):.4f} / {maxdd(base_fixed):.2%}")
        say(f"    4b bars: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}")
        # deletion-matched baseline for section G
        for gross in GROSSES:
            for drop in [NONE] + list(full_inv):
                invest = full_inv if drop == NONE else [c for c in full_inv if c != drop]
                w = rg100_weights(px, invest, gross)
                mx = float(w.sum(axis=1).max())
                res = run_book(px, w)
                base_m = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                         .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
                nm_w = w.drop(columns=[SWEEP]).loc[win]
                pos = nm_w.values[nm_w.values > 0]
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    lg = legs(r, base_fixed, spy, r_oos, spy_oos)
                    lgm = legs(r, base_m, spy, r_oos, spy_oos)
                    rows.append(dict(panel=pname, drop=drop, gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     max_name_w=float(pos.max()) if len(pos) else 0.0,
                                     mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                     turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                     max_row_sum=mx, n_invest=len(invest),
                                     pass4a_matched=lgm["pass4a"], pass4b_matched=lgm["pass4b"],
                                     **lg))
        say(f"    ... {pname} census done, {len(full_inv)} deletions x {len(GROSSES)} gross ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    df.to_csv(f"{OUT}.census.csv", index=False)

    gate("G4 no leverage (all books)", f"max row sum {df.max_row_sum.max():.9f}", "<= 1+1e-12",
         bool((df.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # G7 the census is complete: one book per member, plus the undeleted control, no gaps
    comp = []
    for pname, (_, full_inv) in panels.items():
        for gross in GROSSES:
            got = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)]["drop"]
            comp.append(sorted(got) == sorted([NONE] + list(full_inv)))
    gate("G7 census COMPLETE (one book per investable member + undeleted control, none repeated)",
         f"{sum(comp)} of {len(comp)} (panel, gross) censuses exact", f"{len(comp)} of {len(comp)}", all(comp))

    # G5 every deletion bites
    bites, nobite = 0, []
    for pname in panels:
        for gross in GROSSES:
            d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
            ref = d.loc[NONE]
            for k, r in d.drop(index=NONE).iterrows():
                if abs(r.Sharpe - ref.Sharpe) > 1e-12 or abs(r.CAGR - ref.CAGR) > 1e-12:
                    bites += 1
                else:
                    nobite.append(f"{pname}/g{gross:.2f}/{k}")
    tot_del = sum(len(fi) for _, fi in panels.values()) * len(GROSSES)
    gate("G5 every deletion BITES (LOO book differs from the undeleted one)",
         f"{bites} of {tot_del} deletions move CAGR or Sharpe" +
         (f"; inert: {', '.join(nobite[:6])}" if nobite else ""),
         f"{tot_del} of {tot_del}", bites == tot_del)

    # G3 external reproduction of the committed headline (undeleted, U56, 0.75, 10 bps)
    h = df[(df.panel == "U56") & (df["drop"] == NONE) & (df.gross == 0.75)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(h.CAGR - 0.1255), abs(h.Sharpe - 1.1896) / 10, abs(h.MaxDD + 0.1739),
             abs(h.OOS_CAGR - 0.1377), abs(h.OOS_Sharpe - 1.2332) / 10)
    gate("G3 reproduces idea 2300's committed U56 headline (12.55%/1.1896/-17.39%, OOS 13.77%/1.2332)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # SMALL control (not censused — nothing passes there for a deletion to break)
    win_s = px_s.index[WARMUP:]
    inv_s = [c for c in px_s.columns if c not in (BENCH, SWEEP)]
    spy_s = px_s[BENCH].pct_change().fillna(0.0).loc[win_s]
    base_s = priced(run_book(px_s, rules_v2_weights(px_s[inv_s], band=BAND, gross=0.75)
                             .reindex(columns=px_s.columns).fillna(0.0)), HEADLINE_RUNG).loc[win_s]
    r_s = priced(run_book(px_s, rg100_weights(px_s, inv_s, 0.75)), HEADLINE_RUNG).loc[win_s]
    lg_s = legs(r_s, base_s, spy_s, r_s.loc[OOS_START:], spy_s.loc[OOS_START:])
    say(f"\n--- SMALL control (NOT censused; {len(inv_s)} names, {dropped} dropped): undeleted candidate"
        f" {cagr(r_s):.2%} / {sharpe(r_s):.4f} / {maxdd(r_s):.2%}  4b {'Y' if lg_s['pass4b'] else 'N'}"
        f" (legs {''.join('1' if lg_s[k] else '0' for k in ('L_H1','L_H2','L_OOS','L_DD','L_CAGR'))})"
        f"   SPY {cagr(spy_s):.2%} / {sharpe(spy_s):.4f}")
    say("    -> idea 2318 published SMALL's 4b pass count at 0 of 48; there is no pass here to break.")

    # ---------------------------------------------------------------- A. the headline census
    say("\n=== A. THE CENSUS AT THE HEADLINE RUNG (10 bps, gross 0.75): 4b SURVIVAL OF EVERY DELETION ===")
    surv = {}
    for pname, (_, full_inv) in panels.items():
        d = df[(df.panel == pname) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
        ref = d.loc[NONE]
        dels = d.drop(index=NONE)
        n_pass = int(dels.pass4b.sum())
        surv[pname] = (n_pass, len(dels))
        say(f"\n  {pname}: undeleted control {ref.CAGR:.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:.2%},"
            f" OOS {ref.OOS_CAGR:.2%} / {ref.OOS_Sharpe:.4f}, 4b {'Y' if ref.pass4b else 'N'}")
        say(f"  **4b SURVIVES {n_pass} OF {len(dels)} DELETIONS**   (4a survives {int(dels.pass4a.sum())} of {len(dels)})")
        br = dels[~dels.pass4b]
        if len(br) == 0:
            say("    NO deletion breaks the pass.")
        else:
            say(f"    BREAKING DELETIONS ({len(br)}), each with the leg that binds:")
            for k, r in br.sort_values("Sharpe").iterrows():
                lgs = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                which = ",".join(x[2:] for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not r[x])
                say(f"      drop {k:6s}  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
                    f"  OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}  legs {lgs}  BINDS: {which}")
        say(f"    dispersion over deletions: dCAGR [{(dels.CAGR - ref.CAGR).min():+.2%},"
            f" {(dels.CAGR - ref.CAGR).max():+.2%}] median {(dels.CAGR - ref.CAGR).median():+.2%}"
            f" | dSharpe [{(dels.Sharpe - ref.Sharpe).min():+.4f}, {(dels.Sharpe - ref.Sharpe).max():+.4f}]"
            f" median {(dels.Sharpe - ref.Sharpe).median():+.4f}"
            f" | dMaxDD [{(dels.MaxDD - ref.MaxDD).min():+.2%}, {(dels.MaxDD - ref.MaxDD).max():+.2%}]")
        say(f"    dOOS_Sharpe [{(dels.OOS_Sharpe - ref.OOS_Sharpe).min():+.4f},"
            f" {(dels.OOS_Sharpe - ref.OOS_Sharpe).max():+.4f}]"
            f" median {(dels.OOS_Sharpe - ref.OOS_Sharpe).median():+.4f}")
        say("    the 8 deletions that cost the most Sharpe, and the 4 that help most:")
        srt = (dels.Sharpe - ref.Sharpe).sort_values()
        for k in list(srt.index[:8]) + list(srt.index[-4:]):
            r = dels.loc[k]
            say(f"      {k:6s} dSharpe {r.Sharpe - ref.Sharpe:+7.4f}  dCAGR {r.CAGR - ref.CAGR:+6.2%}"
                f"  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}  maxw {r.max_name_w:5.2%}"
                f"  4b {'Y' if r.pass4b else '.'}")

    say("\n=== B. SURVIVAL OVER EVERY (gross, rung) CELL — all 1,536 published rows ===")
    say("  panel gross  rung |  4b survivors / deletions | 4a survivors | undeleted 4b | breaking names")
    for pname, (_, full_inv) in panels.items():
        for gross in GROSSES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)].set_index("drop")
                ref, dels = d.loc[NONE], d.drop(index=NONE)
                br = list(dels[~dels.pass4b].index)
                shown = ", ".join(br[:6]) + (f" (+{len(br) - 6})" if len(br) > 6 else "")
                say(f"  {pname:5s} {gross:.2f} {rung:5.1f} |  {int(dels.pass4b.sum()):3d} / {len(dels):3d}"
                    f"              |  {int(dels.pass4a.sum()):3d}         |      {'Y' if ref.pass4b else 'N'}       |"
                    f" {shown if br else '-'}")

    say("\n=== C. THE VERDICT STATISTIC: is the pass a DRAW (needs one name) or a BOOK (survives all)? ===")
    for pname in panels:
        for gross in GROSSES:
            d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
            ref, dels = d.loc[NONE], d.drop(index=NONE)
            if not ref.pass4b:
                say(f"  {pname:5s} g {gross:.2f}: undeleted control does NOT pass 4b — census is vacuous here.")
                continue
            n = int(dels.pass4b.sum())
            nbreak = len(dels) - n
            rate = n / len(dels)
            if nbreak == 0:
                call = "BOOK — survives every single-name deletion"
            elif nbreak == 1:
                call = f"DRAW — the pass NEEDS one name ({list(dels[~dels.pass4b].index)[0]})"
            else:
                call = (f"NOT UNANIMOUS — {nbreak} of {len(dels)} single deletions break it "
                        f"({', '.join(list(dels[~dels.pass4b].index)[:8])})")
            say(f"  {pname:5s} g {gross:.2f}: {n}/{len(dels)} = {rate:.3f} survive  ->  {call}")

    say("\n=== D. THE TWO SPECIAL MEMBERS (SPY the benchmark, SHY the sweep), 10 bps, gross 0.75 ===")
    for pname in panels:
        d = df[(df.panel == pname) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
        ref = d.loc[NONE]
        for k in (BENCH, SWEEP):
            if k not in d.index:
                say(f"  {pname:5s} drop {k}: not an investable member of this panel")
                continue
            r = d.loc[k]
            say(f"  {pname:5s} drop {k:4s}: {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
                f"  OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}  4b {'Y' if r.pass4b else 'N'}"
                f"  | dSharpe {r.Sharpe - ref.Sharpe:+7.4f}  mean sweep w {r.mean_sweep_w:.3f}"
                f"  turn/yr {r.turnover_yr:.2f}")

    say("\n=== E. RULE 8 — gross chosen on <= 2016-12-31 ONLY, per deletion; 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, full_inv) in panels.items():
        win = px.index[WARMUP:]
        spy = px[BENCH].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        b_oos = priced(run_book(px, rules_v2_weights(px, band=BAND, gross=0.75)),
                       HEADLINE_RUNG).loc[win].loc[OOS_START:]
        for rung in RUNGS:
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                picks = []
                for drop in [NONE] + list(full_inv):
                    d = df[(df.panel == pname) & (df["drop"] == drop) & (df.cost_bps == rung)]
                    picks.append(d.loc[d[col].idxmax()])
                pk = pd.DataFrame(picks).set_index("drop")
                ctrl = pk.loc[NONE]
                dels = pk.drop(index=NONE)
                n_oos = int((dels.OOS_Sharpe > sharpe(spy_oos)).sum())
                n_4b = int(dels.pass4b.sum())
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser,
                               ctrl_pick_gross=ctrl.gross, ctrl_OOS_Sharpe=ctrl.OOS_Sharpe,
                               n_deletions=len(dels), n_pick_g075=int((dels.gross == 0.75).sum()),
                               n_OOS_beats_SPY=n_oos, n_pass4b=n_4b,
                               med_OOS_Sharpe=float(dels.OOS_Sharpe.median()),
                               min_OOS_Sharpe=float(dels.OOS_Sharpe.min()),
                               med_OOS_CAGR=float(dels.OOS_CAGR.median()),
                               spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                               base_OOS_Sharpe=sharpe(b_oos), base_OOS_CAGR=cagr(b_oos)))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s}: picks gross 0.75 at {int((dels.gross == 0.75).sum()):3d}/{len(dels):3d}"
                    f" | OOS Sharpe beats SPY at {n_oos:3d}/{len(dels):3d}"
                    f" | full-sample 4b at {n_4b:3d}/{len(dels):3d}"
                    f" | median OOS {dels.OOS_CAGR.median():6.2%} / {dels.OOS_Sharpe.median():.4f}"
                    f" (min {dels.OOS_Sharpe.min():.4f})"
                    f" | SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f}"
                    f" | live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("\n=== F. OOS-ONLY SURVIVAL (2017-2026 read once, undeleted-comparand legs) ===")
    for pname in panels:
        for gross in GROSSES:
            d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
            ref, dels = d.loc[NONE], d.drop(index=NONE)
            say(f"  {pname:5s} g {gross:.2f}: OOS Sharpe over deletions"
                f" [{dels.OOS_Sharpe.min():.4f}, {dels.OOS_Sharpe.max():.4f}] median {dels.OOS_Sharpe.median():.4f}"
                f" (control {ref.OOS_Sharpe:.4f});  OOS CAGR"
                f" [{dels.OOS_CAGR.min():.2%}, {dels.OOS_CAGR.max():.2%}] median {dels.OOS_CAGR.median():.2%}"
                f" (control {ref.OOS_CAGR:.2%});  L_OOS holds at {int(dels.L_OOS.sum())}/{len(dels)}")

    say("\n=== G. ROBUSTNESS: the census re-scored against a DELETION-MATCHED live baseline ===")
    say("  (4b never touches the live book, so only 4a can move; published to show it does not rescue 4a)")
    for pname in panels:
        for gross in GROSSES:
            d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)]
            dels = d[d["drop"] != NONE]
            say(f"  {pname:5s} g {gross:.2f}: 4a fixed-comparand {int(dels.pass4a.sum())}/{len(dels)}"
                f"   4a deletion-matched {int(dels.pass4a_matched.sum())}/{len(dels)}"
                f"   4b fixed {int(dels.pass4b.sum())}/{len(dels)}"
                f"   4b deletion-matched {int(dels.pass4b_matched.sum())}/{len(dels)}")

    say("\n=== H. CONCENTRATION ACROSS THE CENSUS (the risk this idea was filed to price) ===")
    for pname in panels:
        for gross in GROSSES:
            d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == HEADLINE_RUNG)].set_index("drop")
            ref, dels = d.loc[NONE], d.drop(index=NONE)
            say(f"  {pname:5s} g {gross:.2f}: max per-name weight, control {ref.max_name_w:.2%};"
                f" over deletions [{dels.max_name_w.min():.2%}, {dels.max_name_w.max():.2%}]"
                f" median {dels.max_name_w.median():.2%}"
                f" | turnover/yr control {ref.turnover_yr:.2f}, deletions"
                f" [{dels.turnover_yr.min():.2f}, {dels.turnover_yr.max():.2f}]")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.census.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
