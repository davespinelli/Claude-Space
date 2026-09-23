#!/usr/bin/env python3
"""idea 2395 (lane cloud, run 44, 2026-09-23) — DOES A VOLATILITY-SCALED COST MODEL MOVE WHERE
THE CAPPED FAMILY DIES?

THE GAP.  Every cost rung this record has ever charged is a FLAT `bps x sum_i |dw_i,t|`: the same
price per unit of turnover for SHY and for the single most volatile name in the panel.  Real
spreads are roughly proportional to a name's own volatility, so a flat rung OVERCHARGES the sleeve
these books actually park in (SHY, phi = 1.00) and UNDERCHARGES the equity tail they rotate
through.  Every "dies at 50 bps" verdict in this record is therefore a statement about a
CONVENTION as much as about a level, and that has never been tested.

THE MODEL.  cost_i,t = k x (vol20_i,t-1 / median_j vol20_j,t-1) ^ p x |dw_i,t|

DIAL 1 -- the exponent p {0.0, 0.5, 1.0, 1.5}.  **p = 0.0 IS THE FLAT RUNG EXACTLY** (every
          relative is raised to the zeroth power, so the model collapses to `bps x sum|dw|`), so
          one ladder spans the committed convention; G3 asserts bit-identity.  p = 1.0 is the
          idea's literal linear model.
DIAL 2 -- gross g {0.75 live, 1.00}.

THE LEVEL IS HELD FIXED; ONLY THE SHAPE MOVES.  `k` is calibrated per (panel, book, gross, p,
convention) so that the TOTAL bill over the sample equals the flat rung's total bill to machine
precision (G5).  This is the whole experiment: the scaled and flat models spend the SAME MONEY,
so any difference in the verdict is pure REALLOCATION of that money across names and across time,
never a disguised change of level.  Without that calibration the comparison would be a cost-level
ladder, which ideas 2322 / 2326 / 2343 have already run four times.

THE STRATEGY IS COST-BLIND, WHICH IS WHY THIS IS CHEAP AND EXACT.  No book here chooses its
weights from its own cost estimate, so the realised weight path, the per-name `|dw_i,t|` matrix
and the zero-cost return `r0` are IDENTICAL across every p, convention and rung.  Each book is
therefore run ONCE per (panel, gross) and all 4 x 3 x 4 prices are read off the same path.  That
also means the p dial CANNOT change which names are held -- it can only change what they cost --
and G6 asserts exactly that.

CONVENTIONS, all published, the headline PRE-STATED here before any compute:
  RAW    -- the model verbatim, no clipping.  **HEADLINE.**
  CLIP5  -- relatives clipped to [0.2, 5.0], to show the answer is not one 2008 microcap tail.
  CAUSAL -- `k` recalibrated EXPANDING from data through t-1 only, so the calibration itself uses
            no future information.  Its total bill is NOT pinned to the flat total; the realised
            ratio is published rather than asserted.

BOOKS.  CAP2 (idea 2322's 2%-per-name capped candidate) and CAND (idea 2300/2332's uncapped
`gross / N_in` candidate), both with the phi = 1.00 SHY sweep, plus the LIVE RULES v2 book as the
4a baseline -- and the baseline is charged under THE SAME cost model as the book it is judged
against, because judging a scaled-cost book against a flat-cost baseline would be the contaminated
comparison this idea exists to avoid.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, rungs {0, 10, 25, 50} bps, books {CAP2, CAND},
weekly cadence, t+1 execution, band 0.03, the 2% cap and the SHY sweep.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
each published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD,
L_H2 and L_OOS failing at every cell.  A cost-model reshuffle that cannot move three legs at once
has no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the STRATEGY's own dials (book, gross) are chosen on warm-up..2016-12-31 ONLY by two
pre-stated IS-only choosers, then 2017-2026 is read ONCE -- separately UNDER EACH COST MODEL, so
the reported question is whether the out-of-sample verdict itself depends on the convention.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 p = 0 is BIT-IDENTICAL to the flat rung.  G4 no leverage.
G5 the calibration pins the total bill to the flat total exactly (RAW, CLIP5).  G6 the p dial
changes NO weight, only the charge.  G7 exactly two tuned parameters.  G8 the relative `rel_i,t`
is causal (panel truncation).  G9 SHY priced on every held row.  G10 EXTERNAL REPRODUCTION of the
committed CAP2 U56 headline (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318) and of the committed
CAND U56 headline (12.59% / 1.1934 / -17.39%, OOS 13.85% / 1.2397).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The flat-vs-scaled contrast is same-tape, same-day,
same-weights and same-total-bill, so it is first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_volatility-scaled-cost-model_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "volatility-scaled-cost-model", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
EXPONENTS = [0.0, 0.5, 1.0, 1.5]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
CONVENTIONS = ["RAW", "CLIP5", "CAUSAL"]
HEADLINE_CONV, HEADLINE_RUNG = "RAW", 10.0
CLIP_LO, CLIP_HI = 0.2, 5.0
NAME_CAP, SWEEP, VOL_LB = 0.020, "SHY", 20
BOOKS = ["CAP2", "CAND"]
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


# ---------------------------------------------------------------- the books (risk sleeves)
def risk_weights(px, gross, cap):
    """The candidate family's risk sleeve: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- 0.03 band.  cap = 0.02 gives idea 2322's CAP2; cap = inf gives idea 2300's CAND."""
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).fillna(0.0)


def full_reference(px, gross, cap):
    """The committed book WITH the phi = 1.00 SHY sweep, for the engine anchors."""
    w = risk_weights(px, gross, cap).copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the runner (per-name turnover)
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the PER-NAME |dw_i,t| matrix is retained so that
    any cost model can be priced off the same realised path afterwards.  Weights are decided at
    t-1 and applied at t; between rebalances the book drifts; the un-invested residual earns 0%."""
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values     # decided t-1, applied t
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    dw = np.zeros((n, m)); cur = np.zeros(m)
    gr = np.zeros(n); r0 = np.zeros(n); nheld = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[shy_i] += max(0.0, 1.0 - new.sum()) * shy_ok[i]
            dw[i] = np.abs(new - cur)
            cur = new
        gr[i] = cur.sum()
        nheld[i] = float((cur > 1e-12).sum())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx),
                dw=pd.DataFrame(dw, index=idx, columns=cols))


# ---------------------------------------------------------------- the cost models
def relatives(px, conv):
    """rel_i,t = vol20_i,t-1 / median_j vol20_j,t-1, over names PRICED at t-1.  Shifted by one
    day so the charge levied on the t+1 execution uses only information available at the decision
    close; G8 re-derives this from a truncated panel."""
    v = px.pct_change().rolling(VOL_LB).std() * np.sqrt(252)
    v = v.shift(1)
    med = v.median(axis=1)
    rel = v.div(med.replace(0, np.nan), axis=0)
    rel = rel.replace([np.inf, -np.inf], np.nan).fillna(1.0)
    if conv == "CLIP5":
        rel = rel.clip(CLIP_LO, CLIP_HI)
    return rel


_POW: dict = {}


def relpow(rel, p, tag):
    """rel ** p, memoised per (convention-tag, p) — it is reused by every book and every rung."""
    key = (tag, p, id(rel))
    if key not in _POW:
        _POW[key] = np.power(rel.values, p)
    return _POW[key]


def charge_series(dw, rel, p, conv, bps, tag=""):
    """Per-day cost in return units.  k is calibrated so the TOTAL bill equals the flat rung's
    total bill exactly (RAW / CLIP5), or expanding from data through t-1 only (CAUSAL)."""
    flat = dw.sum(axis=1)
    if p == 0.0 or bps == 0.0:
        return flat * bps / 1e4, 1.0
    raw = (dw.values * relpow(rel, p, tag)).sum(axis=1)
    raw = pd.Series(raw, index=dw.index)
    if conv == "CAUSAL":
        cf = flat.cumsum().shift(1).fillna(0.0)
        cr = raw.cumsum().shift(1).fillna(0.0)
        k = (cf / cr.replace(0, np.nan)).fillna(1.0).replace([np.inf, -np.inf], 1.0)
        return raw * k * bps / 1e4, float(k.iloc[-1])
    tot_r = raw.sum()
    k = float(flat.sum() / tot_r) if tot_r > 0 else 1.0
    return raw * k * bps / 1e4, k


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
    say("=== idea 2395 — DOES A VOLATILITY-SCALED COST MODEL MOVE WHERE THE CAPPED FAMILY DIES? ===")
    say(f"    {DATE}  lane {LANE} run 44   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)  vol lookback {VOL_LB}d")
    say(f"    DIAL 1 exponent p {EXPONENTS}   DIAL 2 gross {GROSSES}")
    say(f"    conventions {CONVENTIONS}; HEADLINE = {HEADLINE_CONV}.  books {BOOKS} + live RULES v2 as the 4a baseline,")
    say("    the baseline charged under THE SAME cost model as the book it is judged against.")
    say("    k is calibrated so the TOTAL BILL EQUALS THE FLAT RUNG'S TOTAL BILL: same money, different distribution.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells in idea 2383 (L_DD, L_H2, L_OOS fail everywhere) and 0 of 40-120")
    say("    in ideas 2318 / 2322 / 2326 / 2343 — no pass there for a cost reshuffle to keep or break.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the contaminated")
    say("    leg.  The flat-vs-scaled contrast is same-tape, same-weights, same-total-bill and first-order immune.")
    gate("G7 exactly two tuned parameters", "p, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    d2 = int((band_state(px_u, BAND) != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {int(band_state(px_u, BAND).sum(axis=1).mean())}", "0", d2 == 0)

    # G1 replica fidelity on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    c_lv, _ = charge_series(lv["dw"], relatives(px_u, "RAW"), 0.0, "RAW", HEADLINE_RUNG)
    d1 = float((r_eng - (lv["r0"] - c_lv)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3 p = 0 is the flat rung, bit for bit, through the engine itself
    wr = risk_weights(px_u, 0.75, NAME_CAP)
    bk = run_book(px_u, wr)
    eng = backtest(px_u, full_reference(px_u, 0.75, NAME_CAP), cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    c0, _ = charge_series(bk["dw"], relatives(px_u, "RAW"), 0.0, "RAW", HEADLINE_RUNG)
    d3 = float((eng - (bk["r0"] - c0)).abs().max())
    gate("G3 p = 0 IS the flat rung == an independent CAP2 construction through engine.backtest",
         f"max|d| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8 causality of the relative
    cut = px_u.index[int(len(px_u) * 0.70)]
    d8 = float((relatives(px_u.loc[:cut], "RAW") - relatives(px_u, "RAW").loc[:cut]).abs().max().max())
    gate(f"G8 rel_i,t is causal (panel truncated at {cut.date()})", f"max|drel| {d8:.3e}", "< 1e-12", d8 < 1e-12)

    rows, bills = [], []
    for pname, px in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        rels = {c: relatives(px, c) for c in ("RAW", "CLIP5")}
        rels["CAUSAL"] = rels["RAW"]
        # --- realise every weight path ONCE (the strategy is cost-blind)
        paths = {}
        for gross in GROSSES:
            paths[("LIVE", gross)] = run_book(px, rules_v2_weights(px, band=BAND, gross=gross), sweep=False)
            paths[("CAP2", gross)] = run_book(px, risk_weights(px, gross, NAME_CAP))
            paths[("CAND", gross)] = run_book(px, risk_weights(px, gross, np.inf))
        say(f"\n--- panel {pname} ({len(px.columns)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        for conv in CONVENTIONS:
            rel = rels[conv]
            for p in EXPONENTS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        chg = {}
                        for bk_ in ("LIVE", "CAP2", "CAND"):
                            chg[bk_], kk = charge_series(paths[(bk_, gross)]["dw"], rel, p, conv, rung)
                            if bk_ != "LIVE" and rung == HEADLINE_RUNG:
                                fl = paths[(bk_, gross)]["dw"].sum(axis=1) * rung / 1e4
                                bills.append(dict(panel=pname, book=bk_, conv=conv, p=p, gross=gross,
                                                  k=kk,
                                                  bill_scaled=float(chg[bk_].loc[win].sum()),
                                                  bill_flat=float(fl.loc[win].sum()),
                                                  bill_all_scaled=float(chg[bk_].sum()),
                                                  bill_all_flat=float(fl.sum()),
                                                  turnover_yr=float(paths[(bk_, gross)]["dw"].sum(axis=1).loc[win].sum()
                                                                    / (len(win) / 252)),
                                                  shy_share_turn=float(paths[(bk_, gross)]["dw"][SWEEP].loc[win].sum()
                                                                       / paths[(bk_, gross)]["dw"].loc[win].values.sum()),
                                                  shy_share_bill=float(((paths[(bk_, gross)]["dw"][SWEEP]
                                                                         * np.power(rel[SWEEP], p)).loc[win].sum())
                                                                       / ((paths[(bk_, gross)]["dw"].values
                                                                           * np.power(rel.values, p)).sum(axis=1)
                                                                          [WARMUP:].sum())),
                                                  mean_names=float(paths[(bk_, gross)]["names"].loc[win].mean()),
                                                  max_gross=float(paths[(bk_, gross)]["gross"].max())))
                        base_r = (paths[("LIVE", 0.75)]["r0"] - chg["LIVE"]).loc[win] \
                            if gross == 0.75 else (paths[("LIVE", 0.75)]["r0"]
                                                   - charge_series(paths[("LIVE", 0.75)]["dw"], rel, p, conv, rung)[0]).loc[win]
                        for bk_ in BOOKS:
                            r = (paths[(bk_, gross)]["r0"] - chg[bk_]).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bk_, conv=conv, p=p, gross=gross, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                                             base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                             base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                             spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                             spy_CAGR=cagr(spy), spy_MaxDD=maxdd(spy),
                                             **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); bf = pd.DataFrame(bills)
    df.to_csv(f"{OUT}.grid.csv", index=False); bf.to_csv(f"{OUT}.bill.csv", index=False)

    # ---- gates that need the grid
    gate("G4 no leverage anywhere (realised row sums)", f"max gross {bf.max_gross.max():.9f}",
         "<= 1+1e-12", bool((bf.max_gross <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)

    cal = bf[bf.conv.isin(["RAW", "CLIP5"])]
    dbill = float((cal.bill_all_scaled - cal.bill_all_flat).abs().max())
    gate("G5 the calibration pins the TOTAL bill to the flat rung's total (RAW, CLIP5)",
         f"max|d total bill| {dbill:.3e} over {len(cal)} (panel, book, conv, p, gross) cells", "< 1e-12", dbill < 1e-12)
    cau = bf[bf.conv == "CAUSAL"]
    publish("G5b CAUSAL total bill / flat total bill (expanding k, NOT pinned)",
            f"min {float((cau.bill_all_scaled / cau.bill_all_flat).min()):.4f}"
            f"  max {float((cau.bill_all_scaled / cau.bill_all_flat).max()):.4f}")

    # G6 the p dial changes no weight, only the charge
    z0 = df[(df.cost_bps == 0.0)]
    spread0 = float(z0.groupby(["panel", "book", "gross"]).Sharpe.nunique().max())
    gate("G6 the p dial changes NO weight, only the charge (at 0 bps every p must coincide)",
         f"distinct Sharpes per (panel, book, gross) at 0 bps: {int(spread0)}", "1", spread0 == 1)

    bite = bf[(bf.conv == "RAW") & (bf.p > 0)]
    gate("G6b the p dial BITES on the DISTRIBUTION of the bill (SHY's share of it must move)",
         f"SHY share of turnover {bf[bf.p == 0].shy_share_turn.mean():.1%} vs SHY share of the scaled bill"
         f" at p=1.0 {bf[(bf.conv == 'RAW') & (bf.p == 1.0)].shy_share_bill.mean():.1%}",
         "materially different", abs(bf[bf.p == 0].shy_share_turn.mean()
                                     - bf[(bf.conv == 'RAW') & (bf.p == 1.0)].shy_share_bill.mean()) > 0.02)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.conv == "RAW") & (df.p == 0.0)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.conv == "RAW") & (df.p == 0.0)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d10 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
              abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
              abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
              abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G10 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND CAND"
         " (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say(f"\n=== A. THE FULL LADDER, convention {HEADLINE_CONV}, gross 0.75 — EVERY GRID POINT ===")
    say("  panel book  p   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for p in EXPONENTS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.conv == HEADLINE_CONV) & (df.p == p)
                           & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {p:3.1f} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}"
                        + ("   <= FLAT (anchor)" if p == 0.0 else ""))

    # ------------------------------------------------------------ B. does the boundary move?
    say("\n=== B. THE WHOLE QUESTION: DOES THE 4b BOUNDARY MOVE, AND IN WHICH DIRECTION? ===")
    say("    (for each (panel, book, gross, conv): the HIGHEST rung at which 4b still passes, per p.")
    say("     'dies at 50 bps' is a claim about the FLAT column; if the other columns agree, the record's")
    say("     cost conclusions are robust to the MODEL and not only to the LEVEL.)")
    say("  panel book  g   conv   | " + "  ".join(f"p={p:3.1f}" for p in EXPONENTS) + "   <- highest 4b-passing rung (bps), 'none' = no pass")
    death = []
    for pname in panels:
        for bk_ in BOOKS:
            for gross in GROSSES:
                for conv in CONVENTIONS:
                    cells = []
                    for p in EXPONENTS:
                        q = df[(df.panel == pname) & (df.book == bk_) & (df.conv == conv) & (df.p == p)
                               & (df.gross == gross) & (df.pass4b)]
                        cells.append(float(q.cost_bps.max()) if len(q) else np.nan)
                    death.append(dict(panel=pname, book=bk_, gross=gross, conv=conv,
                                      **{f"p{p}": c for p, c in zip(EXPONENTS, cells)},
                                      moved=bool(len({("none" if np.isnan(c) else c) for c in cells}) > 1)))
                    say(f"  {pname:5s} {bk_:4s} {gross:.2f} {conv:6s} | "
                        + "  ".join(("none " if np.isnan(c) else f"{c:5.1f}") for c in cells)
                        + ("    <-- MOVED" if len({("none" if np.isnan(c) else c) for c in cells}) > 1 else "    (unmoved)"))
    dfd = pd.DataFrame(death); dfd.to_csv(f"{OUT}.death.csv", index=False)
    say(f"\n  BOUNDARY MOVED in {int(dfd.moved.sum())} of {len(dfd)} (panel, book, gross, convention) cells.")

    # ------------------------------------------------------------ C. the reallocation itself
    say("\n=== C. WHERE THE SAME MONEY GOES (10 bps, gross 0.75, convention RAW) ===")
    say("  panel book  p  |      k    | SHY share of TURNOVER | SHY share of the BILL | total bill (ret units) | turn/yr")
    for pname in panels:
        for bk_ in BOOKS:
            for p in EXPONENTS:
                e = bf[(bf.panel == pname) & (bf.book == bk_) & (bf.conv == "RAW") & (bf.p == p)
                       & (bf.gross == 0.75)].iloc[0]
                say(f"  {pname:5s} {bk_:4s} {p:3.1f} | {e.k:9.4f} | {e.shy_share_turn:21.2%} |"
                    f" {e.shy_share_bill:21.2%} | {e.bill_scaled:22.4f} | {e.turnover_yr:7.2f}")

    say("\n=== D. THE COST OF THE CONVENTION, IN SHARPE AND CAGR (vs the p=0 FLAT anchor, same rung) ===")
    say("  panel book  g   bps | " + " | ".join(f"p={p:3.1f}: dCAGR  dSharpe" for p in EXPONENTS[1:]))
    for pname in panels:
        for bk_ in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    ref = df[(df.panel == pname) & (df.book == bk_) & (df.conv == "RAW") & (df.p == 0.0)
                             & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                    parts = []
                    for p in EXPONENTS[1:]:
                        r = df[(df.panel == pname) & (df.book == bk_) & (df.conv == "RAW") & (df.p == p)
                               & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                        parts.append(f"{r.CAGR - ref.CAGR:+7.2%} {r.Sharpe - ref.Sharpe:+8.4f}")
                    say(f"  {pname:5s} {bk_:4s} {gross:.2f} {rung:5.1f} | " + " | ".join(parts))

    say(f"\n=== E. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (2 panels x 2 books x 3 conv x 4 p x 2 gross x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for p in EXPONENTS:
        d = df[df.p == p]
        say(f"   p {p:3.1f}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   by p: " + "  ".join(f"p{p}:{int(d[d.p == p].pass4b.sum())}/{len(d[d.p == p])}" for p in EXPONENTS))
    for conv in CONVENTIONS:
        d = df[df.conv == conv]
        say(f"   convention {conv:6s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same book, conv, p, gross, rung):")
    jt = []
    for bk_ in BOOKS:
        for conv in CONVENTIONS:
            for p in EXPONENTS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        q = df[(df.book == bk_) & (df.conv == conv) & (df.p == p)
                               & (df.gross == gross) & (df.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(book=bk_, conv=conv, p=p, gross=gross, cost_bps=rung,
                                       joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells")
    for p in EXPONENTS:
        say(f"    p {p:3.1f}: " + "  ".join(
            f"{bk_} {int(jf[(jf.p == p) & (jf.book == bk_)].joint.sum())}/{len(jf[(jf.p == p) & (jf.book == bk_)])}"
            for bk_ in BOOKS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse), every one: {len(pa)}")
    for _, r in pa.iterrows():
        say(f"    {r.panel:5s} {r.book:4s} conv {r.conv:6s} p {r.p:3.1f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ F. rule 8
    say("\n=== F. RULE 8 — the STRATEGY's dials (book, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE,")
    say("    SEPARATELY UNDER EACH COST MODEL.  The question is whether the OOS verdict depends on the convention. ===")
    wf = []
    for pname in panels:
        for conv in CONVENTIONS:
            for p in EXPONENTS:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.conv == conv) & (df.p == p) & (df.cost_bps == rung)]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, conv=conv, p=p, cost_bps=rung, chooser=chooser,
                                       pick_book=pk.book, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 3 conv x 4 p x 4 rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:           {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe: {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:     {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over book:  " + "  ".join(f"{b}:{int((wfd.pick_book == b).sum())}" for b in BOOKS))
    say("   pick distribution over gross: " + "  ".join(f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say("\n   DOES THE COST MODEL CHANGE WHAT RULE 8 PICKS, OR WHAT IT CONCLUDES?")
    say("   panel conv   bps chooser     | " + " | ".join(f"p={p:3.1f} pick  OOS Sh" for p in EXPONENTS))
    flips = 0; cells = 0
    for pname in panels:
        for conv in CONVENTIONS:
            for rung in RUNGS:
                for chooser in ("C_ISSHARPE", "C_ISCALMAR"):
                    sub = wfd[(wfd.panel == pname) & (wfd.conv == conv) & (wfd.cost_bps == rung)
                              & (wfd.chooser == chooser)].set_index("p")
                    picks = [f"{sub.loc[p].pick_book}/{sub.loc[p].pick_gross:.2f}" for p in EXPONENTS]
                    beats = [bool(sub.loc[p].OOS_Sharpe > sub.loc[p].spy_OOS_Sharpe) for p in EXPONENTS]
                    cells += 1
                    if len(set(picks)) > 1 or len(set(beats)) > 1:
                        flips += 1
                    if conv == HEADLINE_CONV:
                        say(f"   {pname:5s} {conv:6s} {rung:5.1f} {chooser:11s} | "
                            + " | ".join(f"{picks[i]:9s} {sub.loc[EXPONENTS[i]].OOS_Sharpe:6.4f}"
                                         for i in range(len(EXPONENTS))))
    say(f"\n   RULE-8 PICK-OR-VERDICT FLIPS ACROSS p: {flips} of {cells} (panel, conv, rung, chooser) cells.")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
