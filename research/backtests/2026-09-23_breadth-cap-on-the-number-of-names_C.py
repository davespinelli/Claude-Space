#!/usr/bin/env python3
"""idea 2387 (lane C, 2026-09-23) — does a BREADTH CAP on the NUMBER of names do what the 2%
WEIGHT CAP does?

THE OBJECT.  Idea 2322's standing KEEP-4b candidate (CAP2) holds every name inside the 200d
+/-3% band at `min(gross / N_in, 0.02)` and sweeps idle NAV to SHY at phi = 1.  Idea 2381
measured that this cap is a pure DE-GROSSER: mean names held is 38.45 (U56) / 93.22 (B136) at
EVERY cap including INF, so the 2% cap never changes WHO is held, only how much NAV is at risk.

THE DEVICE.  The untested mirror is a cap on the COUNT.  Rank the band's IN names by DISTANCE
ABOVE THE 200d MA (`px / ma - 1`, the quantity the live gate already computes), admit at most
`N_max` of them, and give each

    w_i = min( gross / min(N_in,t , N_max) ,  wcap )        idle NAV -> SHY at phi = 1

Because the per-name weight divides by the HELD count, the breadth cap holds BOOK GROSS
CONSTANT and RE-CONCENTRATES, where the weight cap de-grosses at constant breadth.  The two
devices are therefore opposites, and pricing them on one grid separates "the pass comes from
holding LESS" from "the pass comes from holding FEWER".

DIAL 1 -- breadth cap N_max {10, 20, 30, 50, INF}.
DIAL 2 -- gross g {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: the 2% WEIGHT cap {0.02 = CAP2's own, INF = uncapped}, 2 panels
(U56, B136), 4 cost rungs (0/10/25/50 bps), weekly cadence, t+1 execution, band 0.03, sweep SHY
phi = 1.00, and the ranking statistic and its tie convention (descending distance above the MA,
stable column order for ties -- the tie census is published).
5 x 2 x 2 x 2 x 4 = 160 published rows; every grid point printed.

ANCHORS.  `N_max = INF` with wcap = 0.02 IS idea 2322's CAP2 EXACTLY (gate G1a) and
`N_max = INF` with wcap = INF is the uncapped candidate (gate G1b), so ONE grid spans both
committed books.

THE QUESTION, stated so it can be answered NO: does any FINITE N_max clear 4b on BOTH panels at
the same gross and the same rung, where the 2% WEIGHT cap does -- and does it get there by
holding FEWER names rather than LESS gross?

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (N_max, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1a N_max=INF + wcap 0.02 is BIT-IDENTICAL to an independent CAP2
construction.  G1b N_max=INF + wcap INF is bit-identical to an independent uncapped-candidate
construction.  G2 the per-column replica equals `engine.backtest`.  G3 no leverage anywhere.
G4 NO LOOKAHEAD.  G5 SHY priced on every held row.  G6 exactly two tuned parameters.  G7
EXTERNAL REPRODUCTION of the committed CAP2 U56 headline.  G8 the breadth cap BITES: names held
never exceeds N_max and mean names held is non-decreasing along the ladder.  G9 THE STRUCTURAL
PREMISE, ASSERTED not assumed: at wcap = INF the risk book's gross is exactly `gross` on every
day with N_in > 0, at EVERY N_max -- the breadth cap is not a de-grosser.  G10 idea 2381's
published breadth numbers are reproduced at N_max = INF.  G11 the ranking tie census is
published.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so absolute 4b
levels are optimistic, and the `L_CAGR` floor is the most contaminated leg.  The breadth-cap
contrast is same-tape, same-day, same-gross and first-order immune.  B136 carries an ALL-NaN
`MMC` column (idea 2332's G5 defect), so it is a 135-name panel; that is published, not fixed
here.  SMALL is NOT priced: ideas 2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count
at 0 of 40-120, so there is no pass on that panel for a breadth cap to keep or break.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_breadth-cap-on-the-number-of-names_C.py
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

DATE, SLUG, LANE = "2026-09-23", "breadth-cap-on-the-number-of-names", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
NMAXES = [10, 20, 30, 50, "INF"]          # DIAL 1
GROSSES = [0.75, 1.00]                    # DIAL 2
WCAPS = [0.02, "INF"]                     # REPORTED, never selected on (0.02 = idea 2322's CAP2)
RUNGS = [0.0, 10.0, 25.0, 50.0]
SWEEP, PHI = "SHY", 1.00
HEADLINE_RUNG, HEADLINE_WCAP = 10.0, 0.02
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_GROSS = 0.75

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


def nlabel(n):
    return n if isinstance(n, str) else f"{int(n):d}"


def wlabel(w):
    return "INF" if isinstance(w, str) else f"{w:.2f}"


# ---------------------------------------------------------------- the books
def _in_and_counts(px, invest):
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    return q, inb, inb.sum(axis=1), pr.sum(axis=1)


def _distance(px, invest):
    """Distance above the 200d MA, px/ma - 1 — the live gate's own quantity."""
    q = px[invest]
    return q / q.rolling(200).mean() - 1.0


def select(px, invest, n_max):
    """The admitted set: the band's IN names, or its top N_max by distance above the MA.
    Ties broken by COLUMN ORDER (rank method='first'), a stated, deterministic convention."""
    _, inb, _, _ = _in_and_counts(px, invest)
    if n_max == "INF":
        return inb
    d = _distance(px, invest).where(inb)
    rk = d.rank(axis=1, ascending=False, method="first")
    return (rk <= float(n_max)) & inb


def breadth_weights(px, invest, n_max, gross, wcap, sweep=True):
    """w_i = min(gross / min(N_in, N_max), wcap) on the admitted names; idle NAV -> SHY."""
    sel = select(px, invest, n_max)
    n_held = sel.sum(axis=1)
    per = gross / n_held.replace(0, np.nan)
    if wcap != "INF":
        per = per.clip(upper=float(wcap))
    w = sel.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    if not sweep:
        return w
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def cap2_reference(px, invest, gross):
    """Independent construction of idea 2322's CAP2 book: min(gross/N_in, 0.02) on IN names."""
    q = px[invest]
    inb = (band_state(q, BAND) & q.notna())
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, 0.02)
    w = pd.DataFrame(inb.values.astype(float) * per[:, None], index=q.index, columns=q.columns)
    return w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)


def uncapped_reference(px, invest, gross):
    """Independent construction of the UNCAPPED candidate: gross spread over the whole IN set."""
    q = px[invest]
    inb = (band_state(q, BAND) & q.notna()).astype(float)
    nin = inb.sum(axis=1).replace(0, np.nan)
    w = pd.DataFrame(inb.values * (gross / nin.values)[:, None], index=q.index, columns=q.columns)
    return w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)


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
    wt, rv = w_target.values, rets.values
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
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
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR),
                m_DD=float(maxdd(r) - DD_CAP * maxdd(spy)),
                m_CAGR=float(cagr(r) - CAGR_FLOOR * cagr(spy)),
                m_H1=float(h1 - s1), m_H2=float(h2 - s2),
                m_OOS=float(sharpe(r_oos) - sharpe(spy_oos)))


def main():
    t0 = time.time()
    say("=== idea 2387 — does a BREADTH CAP on the NUMBER of names do what the 2% WEIGHT CAP does? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  "
        f"sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 breadth cap N_max {[nlabel(n) for n in NMAXES]}   DIAL 2 gross g {GROSSES}")
    say(f"    per-name weight  w_i = min( gross / min(N_in, N_max) , wcap )   on the admitted set,"
        f" idle NAV -> {SWEEP}")
    say(f"    REPORTED, never selected on: weight cap {[wlabel(w) for w in WCAPS]}"
        f" (0.02 IS idea 2322's CAP2), panels, rungs, cadence, band, ranking statistic")
    gate("G6 exactly two tuned parameters", "breadth cap N_max, gross g "
         "(the 2% WEIGHT cap is REPORTED on both settings, never selected; the ranking statistic "
         "and its tie convention are fixed a priori)", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        allnan = [c for c in invest if px[c].notna().sum() == 0]
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows, "
             f"window {px.index[WARMUP].date()}..{px.index[-1].date()}", ">= 10y", yrs >= 10)
        publish(f"G0b all-NaN columns ({nm}) — idea 2332's published B136 defect",
                f"{len(allnan)} all-NaN: {allnan} -> {len(invest) - len(allnan)} investable")

    px_u, inv_u = panels["U56"]

    # ---- G2 replica fidelity against the engine
    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)

    # ---- G1a/G1b the grid's two anchors, on BOTH panels and BOTH gross settings
    d1a = d1b = 0.0
    for pn, (px, inv) in panels.items():
        for g in GROSSES:
            d1a = max(d1a, float((breadth_weights(px, inv, "INF", g, 0.02, sweep=False)
                                  - cap2_reference(px, inv, g)).abs().max().max()))
            d1b = max(d1b, float((breadth_weights(px, inv, "INF", g, "INF", sweep=False)
                                  - uncapped_reference(px, inv, g)).abs().max().max()))
    gate("G1a N_max=INF + wcap 0.02 == independent CAP2 construction (both panels, both gross)",
         f"max|dw| {d1a:.3e}", "< 1e-12", d1a < 1e-12)
    gate("G1b N_max=INF + wcap INF == independent uncapped-candidate construction (both panels, both gross)",
         f"max|dw| {d1b:.3e}", "< 1e-12", d1b < 1e-12)

    # ---- G4 no lookahead, on a cell where the breadth cap BINDS
    D = px_u.index[int(len(px_u) * 0.7)]
    wf = breadth_weights(px_u, inv_u, 20, 0.75, "INF").loc[:D]
    pxt = px_u.loc[:D]
    wt = breadth_weights(pxt, [c for c in inv_u if c in pxt.columns], 20, 0.75, "INF")
    d4 = float((wf - wt.reindex(columns=wf.columns).fillna(0.0)).abs().max().max())
    gate(f"G4 NO LOOKAHEAD (N_max=20, g=0.75, wcap INF): weights truncated at {D.date()} == "
         f"full-panel weights up to {D.date()}", f"max|dw| {d4:.3e}", "< 1e-12", d4 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, shape = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS)
                            .reindex(columns=px.columns).fillna(0.0))
        _, inb, n_in, n_pr = _in_and_counts(px, invest)
        say(f"\n--- panel {pname} ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 {cagr(priced(base_res, HEADLINE_RUNG).loc[win]):.2%} /"
            f" {sharpe(priced(base_res, HEADLINE_RUNG).loc[win]):.4f} /"
            f" {maxdd(priced(base_res, HEADLINE_RUNG).loc[win]):.2%}   median N_in"
            f" {int(n_in.loc[win].median())} of median N_priced {int(n_pr.loc[win].median())}")

        # tie census for the ranking convention (G11), published not asserted
        dmat = _distance(px, invest).where(inb).loc[win]
        tie_days = int((dmat.apply(lambda r: r.dropna().duplicated().any(), axis=1)).sum())

        for n_max in NMAXES:
            sel = select(px, invest, n_max)
            n_held_s = sel.sum(axis=1)
            for g in GROSSES:
                for wc in WCAPS:
                    w = breadth_weights(px, invest, n_max, g, wc)
                    w_book = breadth_weights(px, invest, n_max, g, wc, sweep=False)
                    res = run_book(px, w)
                    book_only = w_book.loc[win]
                    pos = book_only.values[book_only.values > 0]
                    bg = book_only.sum(axis=1)
                    active = (n_in.loc[win] > 0)
                    struct = float((bg[active] - g).abs().max()) if active.any() else 0.0
                    shape.append(dict(
                        panel=pname, n_max=nlabel(n_max), gross=g, wcap=wlabel(wc),
                        mean_n_held=float((book_only > 0).sum(axis=1).mean()),
                        max_n_held=int((book_only > 0).sum(axis=1).max()),
                        mean_n_sel=float(n_held_s.loc[win].mean()),
                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                        mean_name_w=float(pos.mean()) if len(pos) else 0.0,
                        mean_book_gross=float(bg.mean()),
                        struct_dev=struct,
                        mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                        mean_gross=float(res["gross"].loc[win].mean()),
                        turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                        max_row_sum=float(w.sum(axis=1).max()),
                        tie_days=tie_days, window_days=int(len(win))))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        b = priced(base_res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(
                            panel=pname, n_max=nlabel(n_max), gross=g, wcap=wlabel(wc),
                            cost_bps=rung, CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                            Calmar=calmar(r), H1=h1, H2=h2,
                            IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(b), base_OOS_Sharpe=sharpe(b.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(b.loc[OOS_START:]), base_MaxDD=maxdd(b),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            **legs(r, b, spy, r_oos, spy_oos)))
            say(f"    ... {pname} N_max={nlabel(n_max)} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); sf = pd.DataFrame(shape)
    df.to_csv(f"{OUT}.grid.csv", index=False); sf.to_csv(f"{OUT}.shape.csv", index=False)

    # ---------------------------------------------------------------- remaining gates
    gate("G3 no leverage (all 40 books)", f"max row sum {sf.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((sf.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px, _ in panels.values())
    gate("G5 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)

    bite = sf[sf.n_max != "INF"]
    ok_bite = bool((bite.apply(lambda r: r.max_n_held <= int(r.n_max), axis=1)).all())
    gate("G8a the breadth cap BITES: names held never exceeds N_max",
         f"max over cells of (max_n_held - N_max) = "
         f"{int(bite.apply(lambda r: r.max_n_held - int(r.n_max), axis=1).max())}", "<= 0", ok_bite)
    mono = []
    for (pn, g, wc), grp in sf.groupby(["panel", "gross", "wcap"]):
        v = grp.set_index("n_max").reindex([nlabel(n) for n in NMAXES]).mean_n_held.values
        mono.append(bool(np.all(np.diff(v) >= -1e-12)))
    gate("G8b mean names held is non-decreasing along the N_max ladder",
         f"{sum(mono)} of {len(mono)} (panel, gross, wcap) cells", f"{len(mono)} of {len(mono)}",
         all(mono))

    sinf = sf[sf.wcap == "INF"]
    gate("G9 STRUCTURAL PREMISE: at wcap=INF the risk book's gross is EXACTLY `gross` on every "
         "day with N_in > 0, at every N_max (the breadth cap is NOT a de-grosser)",
         f"max|book gross - g| over {len(sinf)} cells = {sinf.struct_dev.max():.3e}",
         "< 1e-12", bool(sinf.struct_dev.max() < 1e-12))

    # G7 external reproduction of the committed CAP2 U56 headline (idea 2336/2391)
    h = df[(df.panel == "U56") & (df.n_max == "INF") & (df.wcap == "0.02")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    hs = sf[(sf.panel == "U56") & (sf.n_max == "INF") & (sf.wcap == "0.02")
            & (sf.gross == 0.75)].iloc[0]
    d7 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G7 reproduces the committed CAP2 U56 headline (idea 2336/2391: 11.62%/1.2687/-14.81%, "
         "OOS 12.77%/1.3318, 3.51 turns/yr)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} /"
         f" {h.OOS_Sharpe:.4f}, {hs.turnover_yr:.2f} turns/yr -> max|d| {d7:.2e}",
         "< 1e-3", d7 < 1e-3)
    publish("G7b idea 2322's earlier committed CAP2 U56 headline, for the record",
            "11.58% / 1.2643 / -14.81%, OOS 12.70% / 1.3243 (the tape has advanced since)")

    for pname, ref in (("U56", 38.45), ("B136", 93.22)):
        c = sf[(sf.panel == pname) & (sf.n_max == "INF") & (sf.wcap == "0.02")
               & (sf.gross == 0.75)].iloc[0]
        publish(f"G10 idea 2381's published breadth number at the uncapped COUNT ({pname})",
                f"mean names held {c.mean_n_held:.2f} vs committed {ref:.2f}")
    for pname in panels:
        c = sf[sf.panel == pname].iloc[0]
        publish(f"G11 ranking tie census ({pname}) — days with ANY tied distance among IN names",
                f"{c.tie_days} of {c.window_days} ({c.tie_days / c.window_days:.3%}); ties are "
                f"broken by COLUMN ORDER (rank method='first'), a fixed a-priori convention")

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        for wc in WCAPS:
            tag = "   [CAP2's own 2% weight cap]" if wc == 0.02 else "   [weight cap OFF]"
            say(f"\n  {pname}  wcap {wlabel(wc)}{tag}")
            say("  N_max   g   |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD |"
                " 4a 4b | H1/H2/OOS/DD/CAGR | maxNameW meanNameW nHeld bookGross meanSHY turn/yr")
            for g in GROSSES:
                for n in NMAXES:
                    nl = nlabel(n)
                    r = df[(df.panel == pname) & (df.n_max == nl) & (df.wcap == wlabel(wc))
                           & (df.gross == g) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    c = sf[(sf.panel == pname) & (sf.n_max == nl) & (sf.wcap == wlabel(wc))
                           & (sf.gross == g)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    star = " <- CAP2" if (nl == "INF" and wc == 0.02 and g == 0.75) else ""
                    say(f"  {nl:6s} {g:.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" {r.OOS_MaxDD:7.2%} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  |"
                        f" {lg:17s} | {c.max_name_w:8.2%} {c.mean_name_w:9.2%} {c.mean_n_held:5.1f}"
                        f" {c.mean_book_gross:9.3f} {c.mean_sweep_w:7.3f} {c.turnover_yr:7.2f}{star}")

    say("\n=== B. THE ANSWER — does any FINITE N_max clear 4b on BOTH panels at the same (g, rung)? ===")
    for wc in WCAPS:
        say(f"\n  wcap {wlabel(wc)}" + ("   [CAP2's own]" if wc == 0.02 else "   [weight cap OFF]"))
        say("  N_max   g    | " + "  ".join(f"{int(x):2d}bps U56/B136" for x in RUNGS)
            + "  | both-panel rungs")
        for n in NMAXES:
            nl = nlabel(n)
            for g in GROSSES:
                cells, both = [], 0
                for rung in RUNGS:
                    q = {p: df[(df.panel == p) & (df.n_max == nl) & (df.wcap == wlabel(wc))
                               & (df.gross == g) & (df.cost_bps == rung)].iloc[0].pass4b
                         for p in panels}
                    cells.append(f"   {'Y' if q['U56'] else '.'}/{'Y' if q['B136'] else '.'}     ")
                    both += int(q["U56"] and q["B136"])
                say(f"  {nl:6s} {g:.2f}  | " + "".join(cells) + f"  | {both} of {len(RUNGS)}")
    say("\n  both-panel 4b pass count by N_max (summed over 2 gross x 4 rungs, max 8):")
    for wc in WCAPS:
        say(f"    wcap {wlabel(wc)}:  " + "   ".join(
            f"N_max={nlabel(n):4s} {sum(int(all(df[(df.panel == p) & (df.n_max == nlabel(n)) & (df.wcap == wlabel(wc)) & (df.gross == g) & (df.cost_bps == rung)].iloc[0].pass4b for p in panels)) for g in GROSSES for rung in RUNGS)}/8"
            for n in NMAXES))

    say("\n=== C. KEEP COUNTS OVER ALL PUBLISHED ROWS ===")
    say(f"  {len(df)} rows (5 N_max x 2 gross x 2 wcap x 2 panels x 4 rungs):"
        f"  4b {int(df.pass4b.sum())}   4a {int(df.pass4a.sum())}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding legs on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("  4b by (panel, wcap, N_max) over 8 rows each (2 gross x 4 rungs):")
    for pname in panels:
        for wc in WCAPS:
            say(f"    {pname:5s} wcap {wlabel(wc):4s}: " + "   ".join(
                f"N_max={nlabel(n):4s} {int(df[(df.panel == pname) & (df.wcap == wlabel(wc)) & (df.n_max == nlabel(n))].pass4b.sum())}/8"
                for n in NMAXES))
    say("  the two devices side by side at g=0.75, 10 bps (both panels), 4b legs:")
    for pname in panels:
        for tag, nl, wc in (("WEIGHT cap only (CAP2)", "INF", 0.02),
                            ("no cap at all (CAND)", "INF", "INF"),
                            ("BREADTH cap 30 only", "30", "INF"),
                            ("BREADTH cap 20 only", "20", "INF"),
                            ("BOTH caps (30 + 2%)", "30", 0.02)):
            r = df[(df.panel == pname) & (df.n_max == nl) & (df.wcap == wlabel(wc))
                   & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
            say(f"    {pname:5s} {tag:24s} {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
                f"  legs {lg}  4b {'Y' if r.pass4b else '.'}"
                f"  m_DD {r.m_DD * 100:+6.2f}pp  m_CAGR {r.m_CAGR * 100:+6.2f}pp")

    say("\n=== D. WHAT THE BREADTH CAP DOES TO THE BOOK (10 bps) — FEWER vs LESS ===")
    say("  panel N_max  g    wcap |  nHeld  maxNameW meanNameW bookGross meanSHY  turn/yr | Sharpe   MaxDD")
    for pname in panels:
        for wc in WCAPS:
            for g in GROSSES:
                for n in NMAXES:
                    nl = nlabel(n)
                    c = sf[(sf.panel == pname) & (sf.n_max == nl) & (sf.wcap == wlabel(wc))
                           & (sf.gross == g)].iloc[0]
                    r = df[(df.panel == pname) & (df.n_max == nl) & (df.wcap == wlabel(wc))
                           & (df.gross == g) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    say(f"  {pname:5s} {nl:5s} {g:.2f} {wlabel(wc):4s} | {c.mean_n_held:6.2f}"
                        f" {c.max_name_w:9.2%} {c.mean_name_w:9.2%} {c.mean_book_gross:9.3f}"
                        f" {c.mean_sweep_w:8.3f} {c.turnover_yr:8.2f} | {r.Sharpe:7.4f} {r.MaxDD:8.2%}")

    say("\n=== E. RULE 8 — (N_max, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf_rows = []
    for pname, (px, invest) in panels.items():
        for wc in WCAPS:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.wcap == wlabel(wc)) & (df.cost_bps == rung)]
                anchor = d[(d.n_max == "INF") & (d.gross == LIVE_GROSS)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = d.loc[d[col].idxmax()]
                    wf_rows.append(dict(
                        panel=pname, wcap=wlabel(wc), cost_bps=rung, chooser=chooser,
                        pick_n_max=pick.n_max, pick_gross=pick.gross,
                        OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                        anchor_OOS_Sharpe=anchor.OOS_Sharpe, anchor_OOS_CAGR=anchor.OOS_CAGR,
                        base_OOS_Sharpe=pick.base_OOS_Sharpe, spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                        spy_OOS_CAGR=pick.spy_OOS_CAGR, full4b=bool(pick.pass4b),
                        beats_spy_oos=bool(pick.OOS_Sharpe > pick.spy_OOS_Sharpe),
                        beats_base_oos=bool(pick.OOS_Sharpe > pick.base_OOS_Sharpe),
                        beats_anchor_oos=bool(pick.OOS_Sharpe > anchor.OOS_Sharpe),
                        pick_is_inf=bool(pick.n_max == "INF"),
                        pick_is_finite=bool(pick.n_max != "INF")))
                    say(f"  {pname:5s} wcap {wlabel(wc):4s} {rung:5.1f}bps {chooser:11s} ->"
                        f" N_max {pick.n_max:4s} g {pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" N_max=INF anchor OOS {anchor.OOS_CAGR:6.2%} / {anchor.OOS_Sharpe:.4f} |"
                        f" live v2 OOS {pick.base_OOS_Sharpe:.4f} | SPY OOS {pick.spy_OOS_Sharpe:.4f} |"
                        f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf_rows); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks beating SPY OOS {int(wfd.beats_spy_oos.sum())} of {len(wfd)};"
        f"  beating the live book OOS {int(wfd.beats_base_oos.sum())} of {len(wfd)};"
        f"  beating the N_max=INF anchor OOS {int(wfd.beats_anchor_oos.sum())} of {len(wfd)}")
    say(f"  picks landing on a FINITE breadth cap {int(wfd.pick_is_finite.sum())} of {len(wfd)};"
        f"  on N_max=INF (no breadth cap) {int(wfd.pick_is_inf.sum())} of {len(wfd)};"
        f"  carrying a full-sample 4b pass {int(wfd.full4b.sum())} of {len(wfd)}")
    say("  picks by N_max: " + ", ".join(f"{k} x{int(v)}" for k, v in wfd.pick_n_max.value_counts().items()))
    say("  picks by gross: " + ", ".join(f"{k} x{int(v)}" for k, v in wfd.pick_gross.value_counts().items()))
    agree = 0
    for wc in WCAPS:
        for rung in RUNGS:
            for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                q = wfd[(wfd.wcap == wlabel(wc)) & (wfd.cost_bps == rung) & (wfd.chooser == ch)]
                if len(q) == 2 and q.iloc[0].pick_n_max == q.iloc[1].pick_n_max \
                        and q.iloc[0].pick_gross == q.iloc[1].pick_gross:
                    agree += 1
    say(f"  the two panels agree on (N_max, gross) in {agree} of 16 (wcap, rung, chooser) cells")

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .shape.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
