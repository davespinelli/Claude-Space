#!/usr/bin/env python3
"""idea 2370 (lane B, run 15, 2026-09-23) — does an ELIGIBILITY VOLATILITY CEILING buy the
CAPPED CANDIDATE the DRAWDOWN its B136 leg needs?

THE OBJECT.  RULES v1 carried a `max_vol` ELIGIBILITY ceiling (`rules_v1_weights(..., max_vol
= 0.60)`: drop any name whose 20d annualised vol exceeds 0.60) and RULES v2 DROPPED it.  Idea
2300's `CAND` (every name INSIDE the 200d +/-3% band held at `gross / N_in` of NAV, idle NAV
swept to SHY at phi = 1.00) and idea 2322's capped refinement `CAP2` (the same book with a
2.0% per-name cap) both INHERIT the drop, so the standing 4b candidate admits a name at 2% of
NAV whatever its realised vol.  The record priced a max-vol ceiling against the band on the
UNCAPPED book (2026-09-22 `maxvol-ceiling-as-a-cost_C`, `maxvol-x-band-cross_cloud`) and never
with the per-name cap and the SHY sweep attached, where a REJECTED name de-grosses into a PAID
sleeve rather than into 0%.

THE BOOK.       elig_i = (name INSIDE the 200d +/-3% band) AND (vol_L_i < v),
                held at `gross / N` capped at the per-name cap, idle NAV swept to SHY.
                v = INF IS CAP2 / CAND exactly (gate G1), so one ladder spans the known book.

DIAL 1 -- vol ceiling v {0.30, 0.40, 0.60, INF}.  0.60 is RULES v1's own committed constant.
DIAL 2 -- vol lookback L {20, 60} trading days.   20 is RULES v1's own committed window.

REPORTED, NEVER SELECTED ON: the DENOMINATOR CONVENTION (DEGROSS: N = N_in, so a rejected
name's slot sweeps to SHY -- the convention idea 2370 names; RESPREAD: N = N_elig, so the
survivors absorb it and gross is held), book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56,
B136}, gross {0.75 (live), 1.00}, 4 cost rungs (0/10/25/50 bps), weekly cadence, band 0.03,
t+1 execution and the SHY sweep.
4 v x 2 L x 2 denom x 2 books x 2 gross x 2 panels = 128 books, every one published at every
rung = 512 rows.  SMALL is NOT priced and the reason is stated rather than buried: ideas 2318
/ 2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass
there for an eligibility device to keep.

THE IDEA'S OWN PREMISE IS TESTED, NOT ASSUMED.  "A vol ceiling is the cheapest DD device the
record has not priced under the cap" is a claim about DRAWDOWN BOUGHT PER POINT OF CAGR, so
section C publishes dMaxDD, dCAGR and the CAGR-per-DD exchange rate at every rung, and the
pre-stated falsifier is explicit: the ceiling EARNS its keep only if some cell is BOTH
shallower in drawdown than v = INF AND still clears the 4b CAGR floor -- and, for the claim
the idea was actually filed on, only if it FLIPS B136's binding leg without breaking another.
Unlike a sizing dial the ceiling is ALLOWED to move the held set; section E publishes the
rejection rate, N_in vs N_elig, realised risk gross, the SHY weight and the held-set fidelity
so the size of the surgery is visible at every rung.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (v, L) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_eligibility-vol-ceiling-on-the-capped-candidate_B.py
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

DATE, SLUG, LANE = "2026-09-23", "eligibility-vol-ceiling-on-the-capped-candidate", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
VS = [0.30, 0.40, 0.60, np.inf]          # DIAL 1 — 0.60 is RULES v1's own constant
LOOKBACKS = [20, 60]                     # DIAL 2 — 20 is RULES v1's own window
DENOMS = ["DEGROSS", "RESPREAD"]         # reported, never selected on
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
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


def vtag(v):
    return "INF" if not np.isfinite(v) else f"{v:.2f}"


# ---------------------------------------------------------------- the books
def cap_weights(px, invest, cap, gross):
    """idea 2322's CAP2 / idea 2300's CAND, verbatim from the committed lane-cloud script."""
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


def ceiling_weights(px, invest, cap, gross, v, L, denom):
    """RULES v1's dropped `max_vol` eligibility clause re-attached AHEAD of the cap.

    DEGROSS  : N = N_in    (a rejected name's slot sweeps to SHY — idea 2370's own wording)
    RESPREAD : N = N_elig  (the survivors absorb it; risk gross is held at `gross`)
    v = INF collapses both conventions onto the committed book (gates G1 / G11).
    """
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    vol = q.pct_change().rolling(L).std() * np.sqrt(252)     # RULES v1's own statistic, UNCLIPPED
    elig = inb & (vol < v) if np.isfinite(v) else inb
    n = (inb if denom == "DEGROSS" else elig).sum(axis=1).replace(0, np.nan)
    per = gross / n
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=q.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = elig.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w, inb, elig, vol


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
    say("=== idea 2370 (lane B, run 15) — does an ELIGIBILITY VOLATILITY CEILING buy the CAPPED CANDIDATE the DRAWDOWN its B136 leg needs? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 vol ceiling v {[vtag(v) for v in VS]}   DIAL 2 vol lookback L {LOOKBACKS}")
    say(f"    REPORTED not selected: denominator {DENOMS}  book {list(BOOKS)}  panels U56/B136  gross {GROSSES}  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "vol ceiling v, vol lookback L", "2", True)
    publish("G13 RULES v1's own committed constants are ON the ladder",
            "max_vol = 0.60 is a v rung and its 20d window is an L rung (inherited, not tuned)")

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

    # ---- G1: v = INF IS the committed book, bit-for-bit, under BOTH denominator conventions
    for bk, cap in BOOKS.items():
        for dn in DENOMS:
            for L in LOOKBACKS:
                w0, _, _, _ = ceiling_weights(px_u, panels["U56"][1], cap, 0.75, np.inf, L, dn)
                wc = cap_weights(px_u, panels["U56"][1], cap, 0.75)
                d1 = float((w0 - wc).abs().max().max())
                gate(f"G1 v=INF reproduces the committed book ({bk}, {dn}, U56, g=0.75, L={L})",
                     f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---- G7: vol is never NaN where the band is IN (so a finite ceiling REJECTS, never ABSTAINS)
    for nm, (px, invest) in panels.items():
        for L in LOOKBACKS:
            _, inb, _, vol = ceiling_weights(px, invest, 0.020, 0.75, 0.60, L, "DEGROSS")
            bad = int((inb & vol.isna()).values.sum())
            gate(f"G7 vol defined on every in-band cell ({nm}, L={L})",
                 f"{bad} in-band cells with undefined vol", "0", bad == 0)

    # ---- G10: no lookahead — weights up to a cut date are invariant to the future tape
    cut = "2018-06-29"
    px2 = px_u.copy()
    px2.loc[px2.index > cut] = px2.loc[px2.index > cut] * 1.5
    wa, _, _, _ = ceiling_weights(px_u, panels["U56"][1], 0.020, 0.75, 0.40, 20, "DEGROSS")
    wb, _, _, _ = ceiling_weights(px2, panels["U56"][1], 0.020, 0.75, 0.40, 20, "DEGROSS")
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
                for dn in DENOMS:
                    # the CONTROL for this group: v = INF at the shorter L, i.e. the COMMITTED book
                    wref, _, _, _ = ceiling_weights(px, invest, cap, gross, np.inf, LOOKBACKS[0], dn)
                    ref_state = (run(px, wref)["held"].drop(columns=[SWEEP]).loc[win].values > 1e-12)
                    for L in LOOKBACKS:
                        for v in VS:
                            w, inb, elig, vol = ceiling_weights(px, invest, cap, gross, v, L, dn)
                            res = run(px, w)
                            hw = res["held"].drop(columns=[SWEEP]).loc[win]
                            state = (hw.values > 1e-12)
                            pos = hw.values[hw.values > 1e-12]
                            capped = (np.abs(hw.values - (np.inf if cap == "INF" else float(cap))) < 1e-9)
                            nin = inb.loc[win].sum(axis=1)
                            nel = elig.loc[win].sum(axis=1)
                            rej = float((inb & ~elig).loc[win].values.sum() / max(1, inb.loc[win].values.sum()))
                            wt_rows.append(dict(panel=pname, book=bk, gross=gross, denom=dn, lookback=L,
                                                v=v, vtag=vtag(v),
                                                turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                                heldset_fidelity_vs_INF=float((state == ref_state).mean()),
                                                mean_N_in=float(nin.mean()), mean_N_elig=float(nel.mean()),
                                                reject_rate=rej,
                                                mean_names_held=float(state.sum(axis=1).mean()),
                                                capped_share=float(capped.sum() / max(1, state.sum())),
                                                max_name_w=float(pos.max()) if len(pos) else 0.0,
                                                med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                                mean_risk_gross=float(hw.values.sum(axis=1).mean()),
                                                mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                                max_row_sum=float(res["held"].sum(axis=1).max())))
                            for rung in RUNGS:
                                r = priced(res, rung).loc[win]
                                r_oos = r.loc[OOS_START:]
                                h1, h2 = halves(r)
                                rows.append(dict(panel=pname, book=bk, gross=gross, denom=dn, lookback=L,
                                                 v=v, vtag=vtag(v), cost_bps=rung,
                                                 CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                                 H1=h1, H2=h2,
                                                 IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                                 OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                                 spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                                 base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                                 **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(wt_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.weights.csv", index=False)

    # ---- G2 / G3: external reproduction of the two committed headlines at v = INF
    sel = (df.panel == "U56") & (df.gross == 0.75) & (df.vtag == "INF") & (df.lookback == 20) \
        & (df.denom == "DEGROSS") & (df.cost_bps == HEADLINE_RUNG)
    h = df[sel & (df.book == "CAP2")].iloc[0]
    t2 = tf[(tf.panel == "U56") & (tf.book == "CAP2") & (tf.gross == 0.75) & (tf.vtag == "INF")
            & (tf.lookback == 20) & (tf.denom == "DEGROSS")].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[sel & (df.book == "CAND")].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (128 books)", f"max row gross {tf.max_row_sum.max():.9f}",
         "<= 1+1e-9", tf.max_row_sum.max() <= 1 + 1e-9)

    # ---- G5 / G12: the dial BITES and is MONOTONE in v
    bites, mono = [], []
    for (pn, bk, g, dn, L), grp in tf.groupby(["panel", "book", "gross", "denom", "lookback"]):
        s = grp.sort_values("v")
        bites.append(float(s.iloc[0].mean_N_elig) < float(s.iloc[-1].mean_N_elig) - 1e-9)
        mono.append(bool((s.mean_N_elig.diff().dropna() >= -1e-9).all()))
    gate("G5 the v dial BITES (mean N_elig at v=0.30 strictly below v=INF)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross, denom, L) cells", f"{len(bites)} of {len(bites)}", all(bites))
    gate("G12 N_elig is MONOTONE NON-DECREASING in v (a looser ceiling can only admit more)",
         f"{sum(mono)} of {len(mono)} cells", f"{len(mono)} of {len(mono)}", all(mono))
    same = []
    for (pn, bk, g, L), grp in df[(df.vtag == "INF") & (df.cost_bps == HEADLINE_RUNG)].groupby(
            ["panel", "book", "gross", "lookback"]):
        a = grp[grp.denom == "DEGROSS"].iloc[0]; b = grp[grp.denom == "RESPREAD"].iloc[0]
        same.append(abs(a.Sharpe - b.Sharpe) < 1e-12 and abs(a.CAGR - b.CAGR) < 1e-12)
    fidmin = tf[tf.vtag != "INF"].groupby(["panel", "book", "gross", "denom"]).heldset_fidelity_vs_INF.min()
    fidinf = tf[(tf.vtag == "INF") & (tf.lookback == LOOKBACKS[0])].heldset_fidelity_vs_INF
    gate("G14 the CONTROL is its own reference (v=INF, L=20 held-set fidelity == 100%)",
         f"min over the 16 (panel, book, gross, denom) controls {fidinf.min():.8%}", "== 100%",
         float(fidinf.min()) == 1.0)
    publish("G15 the ceiling MOVES the held set (it is an ELIGIBILITY device, not a sizing dial)",
            f"finite-v held-set fidelity vs the committed book spans "
            f"[{tf[tf.vtag != 'INF'].heldset_fidelity_vs_INF.min():.2%}, "
            f"{tf[tf.vtag != 'INF'].heldset_fidelity_vs_INF.max():.2%}]; min per group {fidmin.min():.2%}")

    gate("G11 the two denominator conventions COLLAPSE at v = INF (N_in == N_elig when nothing is rejected)",
         f"{sum(same)} of {len(same)} cells identical to 1e-12", f"{len(same)} of {len(same)}", all(same))

    # ---------------------------------------------------------------- A. full grid
    say(f"\n=== A. THE FULL GRID AT THE HEADLINE RUNG ({HEADLINE_RUNG:.0f} bps) — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            for dn in DENOMS:
                say(f"\n  {pname} / {bk} / {dn}")
                say("    v      L  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                    " legs H1/H2/OOS/DD/CAGR | turn/yr  rej%   N_held  maxw")
                for gross in GROSSES:
                    for L in LOOKBACKS:
                        for v in VS:
                            r = df[(df.panel == pname) & (df.book == bk) & (df.denom == dn) & (df.gross == gross)
                                   & (df.lookback == L) & (df.vtag == vtag(v)) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                            c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.denom == dn) & (tf.gross == gross)
                                   & (tf.lookback == L) & (tf.vtag == vtag(v))].iloc[0]
                            lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                            say(f"  {vtag(v):>5s} {L:4d}  {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                                f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                                f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                                f" {c.turnover_yr:7.2f} {c.reject_rate:6.2%} {c.mean_names_held:7.2f} {c.max_name_w:6.2%}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (4 v x 2 L x 2 denom x 2 gross x 2 books x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, v) over 4 rungs x 2 gross x 2 L x 2 denom:")
    for bk in BOOKS:
        for pname in panels:
            line = "  ".join(f"v{vtag(v):>4s} {int(df[(df.book == bk) & (df.panel == pname) & (df.vtag == vtag(v))].pass4b.sum()):2d}/32"
                             for v in VS)
            say(f"    {bk:5s} {pname:5s}  {line}")
    say("\n  4b pass counts by (panel, denom, v) at the headline rung, gross 0.75, both books x both L:")
    for pname in panels:
        for dn in DENOMS:
            sub = df[(df.panel == pname) & (df.denom == dn) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
            line = "  ".join(f"v{vtag(v):>4s} {int(sub[sub.vtag == vtag(v)].pass4b.sum())}/4" for v in VS)
            say(f"    {pname:5s} {dn:8s}  {line}")

    # ---------------------------------------------------------------- C. what the ceiling buys
    say("\n=== C. WHAT THE CEILING BUYS: each v minus v=INF, same (panel, book, gross, denom, L, rung) ===")
    for pname in panels:
        for bk in BOOKS:
            for dn in DENOMS:
                for L in LOOKBACKS:
                    say(f"\n  {pname} / {bk} / {dn} / gross 0.75 / L={L}")
                    say("    v      turn/yr  dturn%  | dCAGR @0bps  @10bps  @25bps  @50bps | dSharpe@10  dOOS_Sh@10  dMaxDD@10  CAGR/DD")
                    ref = {rg: df[(df.panel == pname) & (df.book == bk) & (df.denom == dn) & (df.gross == 0.75)
                                  & (df.lookback == L) & (df.vtag == "INF") & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                    t0r = tf[(tf.panel == pname) & (tf.book == bk) & (tf.denom == dn) & (tf.gross == 0.75)
                             & (tf.lookback == L) & (tf.vtag == "INF")].iloc[0]
                    for v in VS:
                        c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.denom == dn) & (tf.gross == 0.75)
                               & (tf.lookback == L) & (tf.vtag == vtag(v))].iloc[0]
                        r = {rg: df[(df.panel == pname) & (df.book == bk) & (df.denom == dn) & (df.gross == 0.75)
                                    & (df.lookback == L) & (df.vtag == vtag(v)) & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                        ddd = r[10.0].MaxDD - ref[10.0].MaxDD
                        ratio = (r[10.0].CAGR - ref[10.0].CAGR) / ddd if abs(ddd) > 1e-9 else np.nan
                        say(f"  {vtag(v):>5s} {c.turnover_yr:8.2f} {c.turnover_yr / t0r.turnover_yr - 1:+7.1%}  |" +
                            "".join(f" {r[rg].CAGR - ref[rg].CAGR:+11.2%}" for rg in RUNGS) +
                            f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}"
                            f" {ddd:+10.2%} {ratio:8.2f}")

    say("\n  THE IDEA'S OWN TEST 1 — is there ANY cell that is BOTH shallower in drawdown AND higher in CAGR than v=INF?")
    for rung in RUNGS:
        n_both = n_tot = n_shal = 0
        for (pn, bk, g, dn, L), grp in df[df.cost_bps == rung].groupby(["panel", "book", "gross", "denom", "lookback"]):
            z = grp[grp.vtag == "INF"].iloc[0]
            for _, r in grp[grp.vtag != "INF"].iterrows():
                n_tot += 1
                if r.MaxDD > z.MaxDD:
                    n_shal += 1
                    if r.CAGR > z.CAGR:
                        n_both += 1
        say(f"   {rung:5.1f} bps: {n_shal} of {n_tot} finite-v cells are SHALLOWER; {n_both} of {n_tot} are shallower AND higher-CAGR")

    say("\n  THE IDEA'S OWN TEST 2 — does the ceiling FLIP a 4b FAIL at v=INF into a 4b PASS (the claim it was filed on)?")
    flips, unflips = [], []
    for (pn, bk, g, dn, L, rg), grp in df.groupby(["panel", "book", "gross", "denom", "lookback", "cost_bps"]):
        z = grp[grp.vtag == "INF"].iloc[0]
        for _, r in grp[grp.vtag != "INF"].iterrows():
            if (not z.pass4b) and r.pass4b:
                flips.append((pn, bk, g, dn, L, rg, r.vtag))
            if z.pass4b and (not r.pass4b):
                unflips.append((pn, bk, g, dn, L, rg, r.vtag))
    say(f"   FAIL -> PASS flips: {len(flips)} of 384 finite-v rows" + (f"  {flips}" if flips else ""))
    say(f"   PASS -> FAIL breaks: {len(unflips)} of 384 finite-v rows")
    say("\n  THE B136 CLAIM SPECIFICALLY — which legs bind at v=INF, and does any finite v repair them?")
    for bk in BOOKS:
        for g in GROSSES:
            for rg in RUNGS:
                z = df[(df.panel == "B136") & (df.book == bk) & (df.gross == g) & (df.denom == "DEGROSS")
                       & (df.lookback == 20) & (df.vtag == "INF") & (df.cost_bps == rg)].iloc[0]
                zl = "".join("1" if z[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                fin = df[(df.panel == "B136") & (df.book == bk) & (df.gross == g) & (df.vtag != "INF")
                         & (df.cost_bps == rg)]
                say(f"   B136 {bk:5s} g{g:.2f} {rg:5.1f}bps  v=INF legs {zl} 4b {'Y' if z.pass4b else '.'}"
                    f"  | finite-v rows passing 4b: {int(fin.pass4b.sum())}/{len(fin)}"
                    f"  | best finite-v MaxDD {fin.MaxDD.max():7.2%} (v=INF {z.MaxDD:7.2%})"
                    f"  | best finite-v CAGR {fin.CAGR.max():6.2%} (floor {CAGR_FLOOR * z.spy_CAGR:6.2%})")

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (v, L) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
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
                for dn in DENOMS:
                    for rung in RUNGS:
                        dd = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross)
                                & (df.denom == dn) & (df.cost_bps == rung)]
                        und = dd[(dd.vtag == "INF") & (dd.lookback == 20)].iloc[0]
                        for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                            pick = dd.loc[dd[col].idxmax()]
                            wf.append(dict(panel=pname, book=bk, gross=gross, denom=dn, cost_bps=rung, chooser=chooser,
                                           pick_v=pick.vtag, pick_L=pick.lookback,
                                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                           pick_pass4b=bool(pick.pass4b), pick_is_inf=bool(pick.vtag == "INF"),
                                           inf_OOS_CAGR=und.OOS_CAGR, inf_OOS_Sharpe=und.OOS_Sharpe,
                                           inf_OOS_MaxDD=und.OOS_MaxDD,
                                           beats_inf_OOS_Sharpe=bool(pick.OOS_Sharpe > und.OOS_Sharpe),
                                           beats_inf_OOS_MaxDD=bool(pick.OOS_MaxDD > und.OOS_MaxDD),
                                           base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                           spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                           beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                                           beats_live_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                            say(f"  {pname:5s} {bk:5s} {dn:8s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} -> v {pick.vtag:>4s} L {int(pick.lookback):2d} |"
                                f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                                f" v=INF L=20 OOS {und.OOS_CAGR:6.2%} / {und.OOS_Sharpe:.4f} / {und.OOS_MaxDD:7.2%} |"
                                f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} | SPY OOS {cagr(spy_oos):6.2%} /"
                                f" {sharpe(spy_oos):.4f} | full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on v = INF (NO ceiling, i.e. the committed book): {int(wfd.pick_is_inf.sum())} of {len(wfd)}")
    say(f"  picks beating the v=INF book's OOS Sharpe:         {int(wfd.beats_inf_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating the v=INF book's OOS MaxDD (shallower): {int(wfd.beats_inf_OOS_MaxDD.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                    {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating the LIVE book's OOS Sharpe:          {int(wfd.beats_live_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:        {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over v: " + "  ".join(f"v{vtag(v):>4s} {int((wfd.pick_v == vtag(v)).sum())}" for v in VS))
    say("  pick distribution over L: " + "  ".join(f"L{L} {int((wfd.pick_L == L).sum())}" for L in LOOKBACKS))
    say("\n  OOS medians over the 64 picks vs the 64 matched v=INF controls:")
    say(f"    pick  OOS CAGR {wfd.OOS_CAGR.median():6.2%}  Sharpe {wfd.OOS_Sharpe.median():.4f}  MaxDD {wfd.OOS_MaxDD.median():7.2%}")
    say(f"    v=INF OOS CAGR {wfd.inf_OOS_CAGR.median():6.2%}  Sharpe {wfd.inf_OOS_Sharpe.median():.4f}  MaxDD {wfd.inf_OOS_MaxDD.median():7.2%}")

    # ---------------------------------------------------------------- E. the premise / mechanics
    say("\n=== E. THE SURGERY, MEASURED — how much of the book a ceiling actually removes (gross 0.75) ===")
    for pname in panels:
        for bk in BOOKS:
            for dn in DENOMS:
                for L in LOOKBACKS:
                    say(f"\n  {pname} / {bk} / {dn} / L={L}")
                    say("    v      rej%   N_in   N_elig  N_held  capped%   max w    med w   risk gross  mean SHY  turn/yr  fid vs INF")
                    for v in VS:
                        c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.denom == dn) & (tf.gross == 0.75)
                               & (tf.lookback == L) & (tf.vtag == vtag(v))].iloc[0]
                        say(f"  {vtag(v):>5s} {c.reject_rate:7.2%} {c.mean_N_in:7.2f} {c.mean_N_elig:8.2f} {c.mean_names_held:7.2f}"
                            f" {c.capped_share:8.2%} {c.max_name_w:7.3%} {c.med_name_w:8.3%} {c.mean_risk_gross:11.4f}"
                            f" {c.mean_sweep_w:9.2%} {c.turnover_yr:8.2f} {c.heldset_fidelity_vs_INF:11.2%}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .weights.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
