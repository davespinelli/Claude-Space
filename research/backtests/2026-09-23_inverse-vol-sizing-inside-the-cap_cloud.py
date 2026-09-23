#!/usr/bin/env python3
"""idea 2362 (lane cloud, run 37, 2026-09-23) — does INVERSE-VOL SIZING INSIDE THE 2% CAP
move the CAPPED candidate's 4b legs?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  Idea 1373 priced inverse-vol
slot weighting on the 2026-09-04 top-20 incumbent and KILLED it (-3.40 pp of CAGR at p = 1
for drawdown the 4b bar did not need); idea 1264 found the chooser picks equal weight at 4 of
4 large-cap cells.  NEITHER ran under a HARD PER-NAME CAP, and the cap changes the question:
CAP2 already truncates the TOP of the weight distribution at 2%, so inverse-vol can only
re-order the UNCAPPED tail, and the residual it frees sweeps to SHY rather than
re-concentrating.  If a cap makes inverse-vol cheap the device changes sign; if it still
costs CAGR one-for-one under the cap that is a clean KILL of vol sizing as a class here.

THE BOOK.       w_raw_i = vol_i^(-p) on names INSIDE the 200d +/- 3% band,
                renormalised so the risk sleeve sums to `gross`,
                then CLIPPED at the per-name cap, idle NAV swept to SHY (phi = 1.00).
                p = 0 IS CAP2 exactly (gate G1), so one ladder spans the known book.

DIAL 1 -- vol exponent p {0.0, 0.5, 1.0, 1.5}.
DIAL 2 -- vol lookback L {20, 60} trading days.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
gross {0.75 (live), 1.00}, 4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03,
t+1 execution, the SHY sweep, and the 0.08 vol floor inherited from `baseline.score`.
4 x 2 x 2 x 2 x 2 = 64 books, every one published at every rung = 256 rows.
SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there for a
sizing device to keep.

THE IDEA'S OWN PREMISE IS TESTED, NOT ASSUMED.  "Inverse-vol can only re-order the UNCAPPED
tail" is a claim about the weight distribution, so section E publishes the CAPPED SHARE (what
fraction of held (day, name) cells sit exactly at the cap), the max and median name weight,
the realised gross and the sweep weight at every p — and the HELD SET is shown to be
invariant in p (a sizing dial must not move the IN/OUT set).

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (p, L) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_inverse-vol-sizing-inside-the-cap_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "inverse-vol-sizing-inside-the-cap", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
PS = [0.0, 0.5, 1.0, 1.5]
LOOKBACKS = [20, 60]
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
VOL_FLOOR = 0.08                       # baseline.score's own floor, inherited not tuned
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


# ---------------------------------------------------------------- the books
def cap_weights(px, invest, cap, gross):
    """idea 2322's CAP2 / idea 2300's CAND, verbatim from the committed lane-B script."""
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


def ivol_weights(px, invest, cap, gross, p, L):
    """w_raw_i = vol_i^(-p) inside the band, renormalised to `gross`, clipped at `cap`,
    residual swept to SHY.  p = 0 collapses to cap_weights (gate G1)."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    vol = (q.pct_change().rolling(L).std() * np.sqrt(252)).clip(lower=VOL_FLOOR)
    ok = inb & vol.notna()
    if p == 0.0:
        raw = ok.astype(float)
    else:
        raw = vol.where(ok).pow(-p).where(ok, 0.0).fillna(0.0)
    tot = raw.sum(axis=1).replace(0.0, np.nan)
    w = raw.div(tot, axis=0) * gross
    if cap != "INF":
        w = w.clip(upper=float(cap))
    w = w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w, inb, ok


def run(px, w, freq=CADENCE):
    """engine.backtest at ZERO cost; every rung is then priced from one pass."""
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
    say("=== idea 2362 (lane cloud, run 37) — does INVERSE-VOL SIZING INSIDE THE 2% CAP move the CAPPED candidate's 4b legs? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)  vol floor {VOL_FLOOR}")
    say(f"    DIAL 1 exponent p {PS}   DIAL 2 vol lookback L {LOOKBACKS}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  gross {GROSSES}  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "vol exponent p, vol lookback L", "2", True)

    panels = {}
    px_u = load_universe()
    px_b = load_universe(broad=True)
    for nm, px in (("U56", px_u), ("B136", px_b)):
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

    # ---- G1: p = 0 IS the committed book, bit-for-bit
    for bk, cap in BOOKS.items():
        for L in LOOKBACKS:
            w0, inb, ok = ivol_weights(px_u, panels["U56"][1], cap, 0.75, 0.0, L)
            wc = cap_weights(px_u, panels["U56"][1], cap, 0.75)
            d1 = float((w0 - wc).abs().max().max())
            gate(f"G1 p=0 reproduces the committed book ({bk}, U56, g=0.75, L={L})",
                 f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G7: vol is never NaN where the band is IN (so `ok` == `inb` and p=0 is exact)
    for nm, (px, invest) in panels.items():
        for L in LOOKBACKS:
            _, inb, ok = ivol_weights(px, invest, 0.020, 0.75, 1.0, L)
            bad = int((inb & ~ok).values.sum())
            gate(f"G7 vol defined on every in-band cell ({nm}, L={L})",
                 f"{bad} in-band cells with undefined vol", "0", bad == 0)

    # ---- G10: no lookahead — weights up to a cut date are invariant to the future tape
    cut = "2018-06-29"
    px2 = px_u.copy()
    px2.loc[px2.index > cut] = px2.loc[px2.index > cut] * 1.5
    wa, _, _ = ivol_weights(px_u, panels["U56"][1], 0.020, 0.75, 1.0, 20)
    wb, _, _ = ivol_weights(px2, panels["U56"][1], 0.020, 0.75, 1.0, 20)
    dlk = float((wa.loc[:cut] - wb.loc[:cut]).abs().max().max())
    gate("G10 no lookahead (future tape x1.5 after 2018-06-29 leaves every earlier weight identical)",
         f"max|dw| on rows <= {cut}: {dlk:.3e}", "< 1e-15", dlk < 1e-15)

    # ---------------------------------------------------------------- the grid
    rows, wt_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                       .reindex(columns=px.columns).fillna(0.0))
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                ref_state = None
                for L in LOOKBACKS:
                    for p in PS:
                        w, inb, ok = ivol_weights(px, invest, cap, gross, p, L)
                        res = run(px, w)
                        hw = res["held"].drop(columns=[SWEEP]).loc[win]
                        state = (hw.values > 1e-12)
                        if ref_state is None:
                            ref_state = state
                        pos = hw.values[hw.values > 1e-12]
                        capped = (np.abs(hw.values - (np.inf if cap == "INF" else float(cap))) < 1e-9)
                        wt_rows.append(dict(panel=pname, book=bk, gross=gross, lookback=L, p=p,
                                            turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                            heldset_fidelity=float((state == ref_state).mean()),
                                            mean_names_in=float(state.sum(axis=1).mean()),
                                            capped_share=float(capped.sum() / max(1, state.sum())),
                                            max_name_w=float(pos.max()) if len(pos) else 0.0,
                                            med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                            min_name_w=float(pos.min()) if len(pos) else 0.0,
                                            mean_gross=float(res["held"].loc[win].sum(axis=1).mean()),
                                            mean_risk_gross=float(hw.values.sum(axis=1).mean()),
                                            mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                            max_row_sum=float(res["held"].sum(axis=1).max())))
                        for rung in RUNGS:
                            r = priced(res, rung).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bk, gross=gross, lookback=L, p=p, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(wt_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.weights.csv", index=False)

    # ---- G2 / G3: external reproduction of the two committed headlines at p = 0
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75) & (df.p == 0.0)
           & (df.lookback == 20) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    t2 = tf[(tf.panel == "U56") & (tf.book == "CAP2") & (tf.gross == 0.75) & (tf.p == 0.0) & (tf.lookback == 20)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == 0.75) & (df.p == 0.0)
            & (df.lookback == 20) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (64 books)", f"max row gross {tf.max_row_sum.max():.9f}",
         "<= 1+1e-9", tf.max_row_sum.max() <= 1 + 1e-9)

    # ---- G5: the dial BITES on the weight distribution
    bites = []
    for (pn, bk, g, L), grp in tf.groupby(["panel", "book", "gross", "lookback"]):
        v = grp.sort_values("p")
        bites.append(float(v.iloc[-1].min_name_w) < float(v.iloc[0].min_name_w) - 1e-12)
    gate("G5 the p dial BITES (min held name weight at p=1.5 strictly below p=0)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross, L) cells", f"{len(bites)} of {len(bites)}", all(bites))
    fid = tf.groupby(["panel", "book", "gross"]).heldset_fidelity.min()
    gate("G11 the HELD SET is invariant in p and L (a sizing dial must not move the IN/OUT set)",
         f"min held-set fidelity over all 64 books {fid.min():.8%}", "== 100%", float(fid.min()) == 1.0)

    # ---------------------------------------------------------------- A. full grid
    say(f"\n=== A. THE FULL GRID AT THE HEADLINE RUNG ({HEADLINE_RUNG:.0f} bps) — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk}")
            say("    p     L  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                " legs H1/H2/OOS/DD/CAGR | turn/yr  capped%  maxw   minw")
            for gross in GROSSES:
                for L in LOOKBACKS:
                    for p in PS:
                        r = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.lookback == L)
                               & (df.p == p) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                        c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross)
                               & (tf.lookback == L) & (tf.p == p)].iloc[0]
                        lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                        say(f"  {p:4.1f} {L:4d}  {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                            f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                            f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                            f" {c.turnover_yr:7.2f} {c.capped_share:7.2%} {c.max_name_w:6.2%} {c.min_name_w:6.3%}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (4 p x 2 L x 2 gross x 2 books x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, p) over 4 rungs x 2 gross x 2 L:")
    for bk in BOOKS:
        for pname in panels:
            line = "  ".join(f"p{p:.1f} {int(df[(df.book == bk) & (df.panel == pname) & (df.p == p)].pass4b.sum()):2d}/16"
                             for p in PS)
            say(f"    {bk:5s} {pname:5s}  {line}")

    # ---------------------------------------------------------------- C. what p buys
    say("\n=== C. WHAT INVERSE-VOL BUYS: each p minus p=0, same (panel, book, gross, L, rung) ===")
    for pname in panels:
        for bk in BOOKS:
            for L in LOOKBACKS:
                say(f"\n  {pname} / {bk} / gross 0.75 / L={L}")
                say("    p     turn/yr  dturn%  | dCAGR @0bps  @10bps  @25bps  @50bps | dSharpe@10  dOOS_Sh@10  dMaxDD@10  CAGR/DD")
                ref = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lookback == L)
                              & (df.p == 0.0) & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                t0r = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75)
                         & (tf.lookback == L) & (tf.p == 0.0)].iloc[0]
                for p in PS:
                    c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75)
                           & (tf.lookback == L) & (tf.p == p)].iloc[0]
                    r = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == 0.75) & (df.lookback == L)
                                & (df.p == p) & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                    ddd = r[10.0].MaxDD - ref[10.0].MaxDD
                    ratio = (r[10.0].CAGR - ref[10.0].CAGR) / ddd if abs(ddd) > 1e-9 else np.nan
                    say(f"  {p:4.1f} {c.turnover_yr:8.2f} {c.turnover_yr / t0r.turnover_yr - 1:+7.1%}  |" +
                        "".join(f" {r[rg].CAGR - ref[rg].CAGR:+11.2%}" for rg in RUNGS) +
                        f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}"
                        f" {ddd:+10.2%} {ratio:8.2f}")

    say("\n  THE IDEA'S OWN TEST — is there ANY cell that is BOTH shallower in drawdown AND higher in CAGR than p=0?")
    for rung in RUNGS:
        n_both = n_tot = 0
        for (pn, bk, g, L), grp in df[df.cost_bps == rung].groupby(["panel", "book", "gross", "lookback"]):
            z = grp[grp.p == 0.0].iloc[0]
            for _, r in grp[grp.p > 0].iterrows():
                n_tot += 1
                if r.MaxDD > z.MaxDD and r.CAGR > z.CAGR:
                    n_both += 1
        say(f"   {rung:5.1f} bps: {n_both} of {n_tot} (p>0) cells beat p=0 on BOTH MaxDD and CAGR")

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (p, L) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    dd = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.cost_bps == rung)]
                    und = dd[(dd.p == 0.0) & (dd.lookback == 20)].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pick = dd.loc[dd[col].idxmax()]
                        wf.append(dict(panel=pname, book=bk, gross=gross, cost_bps=rung, chooser=chooser,
                                       pick_p=pick.p, pick_L=pick.lookback,
                                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                       pick_pass4b=bool(pick.pass4b), pick_is_p0=bool(pick.p == 0.0),
                                       eq_OOS_CAGR=und.OOS_CAGR, eq_OOS_Sharpe=und.OOS_Sharpe,
                                       beats_equal_OOS_Sharpe=bool(pick.OOS_Sharpe > und.OOS_Sharpe),
                                       base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                       spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                       beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos))))
                        say(f"  {pname:5s} {bk:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} -> p {pick.p:.1f} L {int(pick.lookback):2d} |"
                            f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                            f" p=0 L=20 OOS {und.OOS_CAGR:6.2%} / {und.OOS_Sharpe:.4f} |"
                            f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} /"
                            f" {sharpe(spy_oos):.4f} | full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on p = 0 (EQUAL weight, i.e. the committed book): {int(wfd.pick_is_p0.sum())} of {len(wfd)}")
    say(f"  picks beating the EQUAL-WEIGHT book's OOS Sharpe:  {int(wfd.beats_equal_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                    {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:        {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over p: " + "  ".join(f"p{p:.1f} {int((wfd.pick_p == p).sum())}" for p in PS))
    say("  pick distribution over L: " + "  ".join(f"L{L} {int((wfd.pick_L == L).sum())}" for L in LOOKBACKS))

    # ---------------------------------------------------------------- E. the premise
    say("\n=== E. THE IDEA'S OWN PREMISE — 'the cap already truncates the top, so p only re-orders the tail' ===")
    say("  (gross 0.75; capped% = share of held (day,name) cells sitting exactly at the cap)")
    for pname in panels:
        for bk in BOOKS:
            for L in LOOKBACKS:
                say(f"\n  {pname} / {bk} / L={L}")
                say("    p    capped%   max w    med w    min w   mean N_in  mean risk gross  mean SHY  turn/yr")
                for p in PS:
                    c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75)
                           & (tf.lookback == L) & (tf.p == p)].iloc[0]
                    say(f"  {p:4.1f} {c.capped_share:8.2%} {c.max_name_w:7.3%} {c.med_name_w:8.3%} {c.min_name_w:8.3%}"
                        f" {c.mean_names_in:10.2f} {c.mean_risk_gross:15.4f} {c.mean_sweep_w:9.2%} {c.turnover_yr:8.2f}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .weights.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
