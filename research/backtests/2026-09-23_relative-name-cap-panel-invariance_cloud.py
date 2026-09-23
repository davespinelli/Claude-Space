#!/usr/bin/env python3
"""idea 2381 (lane cloud, 2026-09-23) — is the 2% NAME CAP PANEL-INVARIANT, or should it SCALE
with 1/N?

THE OBJECT.  Idea 2322's standing KEEP-4b candidate (CAP2) holds each name inside the 200d
+/-3% band at `min(gross / N_in, 0.02)` and sweeps idle NAV to SHY.  That 0.02 is an ABSOLUTE
constant, so it binds only when `gross / N_in > 0.02`, i.e. at gross 0.75 when N_in < 37.5
names.  On U56 that is 67% of the panel's breadth; on B136 only 28%.  The record's own two-panel
gap (U56 passes every leg, B136 fails `L_DD` at gross 1.00) may be nothing but that asymmetry.

THE DEVICE.  Price the cap in RELATIVE units instead — one cap multiple `a` that means the same
thing on a 56-name panel and a 136-name panel:

    per-name weight  w_i = min( gross / N_in,t ,  c_t )      on IN names, idle -> SHY at phi=1
    CONVENTION G (HEADLINE, pre-stated in the claim):  c_t = a x gross / N_priced,t
    CONVENTION A (the idea's literal text):            c_t = a / N_priced,t

Under G, `a = 1.0` IS the live de-grossed book EXACTLY (w_i = gross/N_priced on IN names) at
BOTH gross settings and `a = INF` IS the uncapped candidate, so ONE ladder spans both known
books -- the two anchor claims the idea itself makes.  The literal convention A honours those
anchors only at gross 1.00, where the two conventions coincide (gate G1c).  BOTH are published;
the headline convention was fixed in the pushed claim BEFORE any compute.

DIAL 1 -- cap multiple a {1.0, 1.25, 1.5, 2.0, INF}.
DIAL 2 -- gross g {0.75 (live), 1.00}.
The ABSOLUTE 2% cap (CAP2) is priced alongside as a FIXED REFERENCE, never as a dial: it is the
comparand the idea exists to beat, not a third tuned parameter.

REPORTED, NEVER SELECTED ON: 2 panels (U56, B136), 2 conventions, 4 cost rungs (0/10/25/50 bps),
weekly cadence, t+1 execution, band 0.03, sweep SHY phi=1.00.
5 x 2 x 2 x 2 x 4 = 160 published ladder rows + 16 CAP2 reference rows; every grid point printed.

THE QUESTION, stated so it can be answered NO: does ONE value of a clear 4b on BOTH panels, at
the same gross and the same rung, where one value of the ABSOLUTE cap cannot?

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (a, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1a convention G at a=1.0 is BIT-IDENTICAL to `rules_v2_weights`
on the risk book.  G1b a=INF is bit-identical to an independent uncapped-candidate construction.
G1c conventions G and A coincide at gross 1.00.  G2 the per-column replica equals
`engine.backtest`.  G3 no leverage anywhere.  G4 NO LOOKAHEAD.  G5 SHY priced on every held row.
G6 exactly two tuned parameters.  G7 EXTERNAL REPRODUCTION of idea 2322's committed U56 CAP2
headline (11.58% / 1.2643 / -14.81%, OOS 12.70% / 1.3243) off the reference rows.  G8 the cap
BITES: max per-name weight is non-decreasing in a and never exceeds c_t.  G9 the filed premise
is MEASURED, not assumed: the days each cap binds on each panel are published.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so absolute 4b
levels are optimistic.  The cap-unit contrast is same-tape, same-day, same-gross and first-order
immune; the CAGR floor leg is an ABSOLUTE bar and is the most contaminated reading.  SMALL is
NOT priced: ideas 2318 / 2322 / 2326 / 2343 each published SMALL's 4b pass count at 0 of 40-120,
so there is no pass on that panel for a cap unit to keep or break.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_relative-name-cap-panel-invariance_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "relative-name-cap-panel-invariance", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
ABS_CAP = 0.02                       # idea 2322's filed CAP2 constant -- REFERENCE, not a dial
SWEEP, PHI = "SHY", 1.00
ALPHAS = [1.0, 1.25, 1.5, 2.0, "INF"]
CONVS = ["G", "A"]                   # G = a*gross/N_priced (HEADLINE), A = a/N_priced (literal)
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, HEADLINE_CONV = 10.0, "G"
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


def alabel(a):
    return a if isinstance(a, str) else f"{a:.2f}"


# ---------------------------------------------------------------- the books
def _in_and_counts(px, invest):
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    n_in = inb.sum(axis=1)
    n_pr = pr.sum(axis=1)
    return q, inb, n_in, n_pr


def cap_series(px, invest, a, conv, gross):
    """The per-name cap c_t for this (a, convention, gross).  INF -> no cap."""
    _, _, _, n_pr = _in_and_counts(px, invest)
    if a == "INF":
        return pd.Series(np.inf, index=px.index)
    unit = gross if conv == "G" else 1.0
    return float(a) * unit / n_pr.replace(0, np.nan)


def relcap_weights(px, invest, a, conv, gross, sweep=True):
    """w_i = min(gross/N_in, c_t) on IN names; idle NAV -> SHY at phi = 1 when sweep."""
    q, inb, n_in, _ = _in_and_counts(px, invest)
    base = gross / n_in.replace(0, np.nan)
    c = cap_series(px, invest, a, conv, gross)
    per = pd.concat([base, c], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    if not sweep:
        return w
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def abscap_weights(px, invest, gross, sweep=True):
    """idea 2322's filed CAP2 REFERENCE: w_i = min(gross/N_in, 0.02)."""
    q, inb, n_in, _ = _in_and_counts(px, invest)
    per = pd.concat([gross / n_in.replace(0, np.nan),
                     pd.Series(ABS_CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    if not sweep:
        return w
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w


def uncapped_reference(px, invest, gross):
    """Independent construction of the UNCAPPED candidate: gross spread over the IN set."""
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
                m_CAGR=float(cagr(r) - CAGR_FLOOR * cagr(spy)))


def main():
    t0 = time.time()
    say("=== idea 2381 — is the 2% NAME CAP PANEL-INVARIANT, or should it SCALE with 1/N? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  "
        f"sweep {SWEEP} phi={PHI:.2f}   absolute reference cap {ABS_CAP:.2%} (idea 2322, FIXED)")
    say(f"    DIAL 1 cap multiple a {[alabel(a) for a in ALPHAS]}   DIAL 2 gross g {GROSSES}")
    say(f"    CONVENTION G (HEADLINE, pre-stated in the pushed claim): c_t = a x gross / N_priced,t")
    say(f"    CONVENTION A (the idea's literal text):                  c_t = a / N_priced,t")
    gate("G6 exactly two tuned parameters", "cap multiple a, gross g "
         "(the absolute 2% cap is a fixed REFERENCE, the convention is REPORTED not selected)",
         "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u, inv_u = panels["U56"]

    # ---- G2 replica fidelity
    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)

    # ---- G1a/b/c the ladder's two anchors
    for g in GROSSES:
        d1a = float((relcap_weights(px_u, inv_u, 1.0, "G", g, sweep=False)
                     - rules_v2_weights(px_u, band=BAND, gross=g)).abs().max().max())
        gate(f"G1a convention G at a=1.00 == rules_v2_weights (the live de-grossed book), g={g}",
             f"max|dw| {d1a:.3e}", "< 1e-12", d1a < 1e-12)
    d1b = float((relcap_weights(px_u, inv_u, "INF", "G", 0.75, sweep=False)
                 - uncapped_reference(px_u, inv_u, 0.75)).abs().max().max())
    gate("G1b a=INF == independent uncapped-candidate construction (U56, g=0.75)",
         f"max|dw| {d1b:.3e}", "< 1e-12", d1b < 1e-12)
    d1c = max(float((relcap_weights(px_u, inv_u, a, "G", 1.00, sweep=False)
                     - relcap_weights(px_u, inv_u, a, "A", 1.00, sweep=False)).abs().max().max())
              for a in ALPHAS)
    gate("G1c conventions G and A coincide at gross 1.00 (they differ only by the gross factor)",
         f"max|dw| over all a {d1c:.3e}", "< 1e-12", d1c < 1e-12)

    # ---- G4 no lookahead
    D = px_u.index[int(len(px_u) * 0.7)]
    wf = relcap_weights(px_u, inv_u, 1.5, "G", 0.75).loc[:D]
    pxt = px_u.loc[:D]
    wt = relcap_weights(pxt, [c for c in inv_u if c in pxt.columns], 1.5, "G", 0.75)
    d4 = float((wf - wt.reindex(columns=wf.columns).fillna(0.0)).abs().max().max())
    gate(f"G4 NO LOOKAHEAD: weights truncated at {D.date()} == full-panel weights up to {D.date()}",
         f"max|dw| {d4:.3e}", "< 1e-12", d4 < 1e-12)

    # ---------------------------------------------------------------- the grid
    rows, shape = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS)
                            .reindex(columns=px.columns).fillna(0.0))
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        _, inb, n_in, n_pr = _in_and_counts(px, invest)
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} /"
            f" {maxdd(base_r):.2%}   median N_in {int(n_in.loc[win].median())} of median"
            f" N_priced {int(n_pr.loc[win].median())}")

        books = []
        for g in GROSSES:
            books.append(("CAP2abs", "-", g, abscap_weights(px, invest, g),
                          abscap_weights(px, invest, g, sweep=False),
                          pd.Series(ABS_CAP, index=px.index)))
            for conv in CONVS:
                for a in ALPHAS:
                    books.append((alabel(a), conv, g, relcap_weights(px, invest, a, conv, g),
                                  relcap_weights(px, invest, a, conv, g, sweep=False),
                                  cap_series(px, invest, a, conv, g)))
        for alab, conv, g, w, w_book, c in books:
            res = run_book(px, w)
            # RISK BOOK = weights BEFORE the cash sweep; the SHY sweep is cash, not a position
            book_only = w_book.loc[win]
            pos = book_only.values[book_only.values > 0]
            binds = ((g / n_in.replace(0, np.nan)) > c).loc[win]
            base_pn = (g / n_in.replace(0, np.nan)).loc[win]
            shape.append(dict(panel=pname, a=alab, conv=conv, gross=g,
                              bind_days=int(binds.fillna(False).sum()),
                              bind_frac=float(binds.fillna(False).mean()),
                              max_name_w=float(pos.max()) if len(pos) else 0.0,
                              mean_name_w=float(pos.mean()) if len(pos) else 0.0,
                              mean_book_gross=float(book_only.sum(axis=1).mean()),
                              mean_gross=float(res["gross"].loc[win].mean()),
                              mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                              mean_n_held=float((book_only > 0).sum(axis=1).mean()),
                              turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                              max_row_sum=float(w.sum(axis=1).max()),
                              median_uncapped_w=float(base_pn.median())))
            for rung in RUNGS:
                r = priced(res, rung).loc[win]
                b = priced(base_res, rung).loc[win]
                r_oos = r.loc[OOS_START:]
                h1, h2 = halves(r)
                rows.append(dict(panel=pname, a=alab, conv=conv, gross=g, cost_bps=rung,
                                 CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                 H1=h1, H2=h2,
                                 IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                 OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                 base_OOS_Sharpe=sharpe(b.loc[OOS_START:]),
                                 base_OOS_CAGR=cagr(b.loc[OOS_START:]),
                                 spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                 spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                 **legs(r, b, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); sf = pd.DataFrame(shape)
    df.to_csv(f"{OUT}.grid.csv", index=False); sf.to_csv(f"{OUT}.shape.csv", index=False)
    lad = df[df.a != "CAP2abs"]; ref = df[df.a == "CAP2abs"]

    gate("G3 no leverage (all books)", f"max row sum {sf.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((sf.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px, _ in panels.values())
    gate("G5 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    mono = []
    for (pn, cv, g), grp in sf[sf.a != "CAP2abs"].groupby(["panel", "conv", "gross"]):
        v = grp.set_index("a").reindex([alabel(a) for a in ALPHAS]).max_name_w.values
        mono.append(bool(np.all(np.diff(v) >= -1e-12)))
    gate("G8 max per-name weight is non-decreasing along the a ladder",
         f"{sum(mono)} of {len(mono)} (panel, conv, gross) cells", f"{len(mono)} of {len(mono)}",
         all(mono))
    h = ref[(ref.panel == "U56") & (ref.gross == 0.75) & (ref.cost_bps == HEADLINE_RUNG)].iloc[0]
    d7 = max(abs(h.CAGR - 0.1158), abs(h.Sharpe - 1.2643) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1270), abs(h.OOS_Sharpe - 1.3243) / 10)
    gate("G7 reproduces idea 2322's committed U56 CAP2 headline (11.58%/1.2643/-14.81%, OOS 12.70%/1.3243)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d7:.2e}", "< 1e-3", d7 < 1e-3)
    # G10 -- unplanned cross-check: a=1.00 under convention G IS the live de-grossed book plus
    # the SHY sweep, i.e. idea 2294's committed idle-cash sleeve.  Published, not asserted: the
    # U56 cache has advanced since 2294 ran (its window now ends 2026-09-22, B136's 2026-09-18),
    # so only B136 can be expected to match to the published precision.
    for pname, ref_txt in (("U56", "9.1201% / 1.2675 / -11.4824% (halves 1.2774 / 1.2635)"),
                           ("B136", "8.4751% / 1.1669 / -11.6473% (halves 1.2772 / 1.0605)")):
        q = df[(df.panel == pname) & (df.a == "1.00") & (df.conv == "G") & (df.gross == 0.75)
               & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        publish(f"G10 a=1.00 (convention G) reproduces idea 2294's committed idle-cash sleeve ({pname})",
                f"read {q.CAGR:.4%} / {q.Sharpe:.4f} / {q.MaxDD:.4%} (halves {q.H1:.4f} / {q.H2:.4f})"
                f"  vs committed {ref_txt}")

    for pname in panels:
        c = sf[(sf.panel == pname) & (sf.a == "CAP2abs") & (sf.gross == 0.75)].iloc[0]
        publish(f"G9 the filed premise, MEASURED ({pname}, absolute 2% cap at g=0.75)",
                f"the 2% cap binds on {c.bind_days} of the window's days ({c.bind_frac:.1%}); "
                f"median uncapped per-name weight {c.median_uncapped_w:.3%}; "
                f"mean names held {c.mean_n_held:.2f}; mean book gross {c.mean_book_gross:.3f}")

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL LADDER AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        for conv in CONVS:
            say(f"\n  {pname}  convention {conv}"
                + ("   [HEADLINE]" if conv == HEADLINE_CONV else "   [published, not headline]"))
            say("  a      g    |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD |"
                " 4a 4b | H1/H2/OOS/DD/CAGR | maxNameW meanNameW nHeld bookGross bind%  turn/yr")
            for g in GROSSES:
                for a in ALPHAS + ["CAP2abs"]:
                    al = alabel(a) if a != "CAP2abs" else "CAP2abs"
                    cv = conv if a != "CAP2abs" else "-"
                    r = df[(df.panel == pname) & (df.a == al) & (df.conv == cv) & (df.gross == g)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    c = sf[(sf.panel == pname) & (sf.a == al) & (sf.conv == cv) & (sf.gross == g)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {al:6s} {g:.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                        f" {c.max_name_w:8.2%} {c.mean_name_w:9.2%} {c.mean_n_held:5.1f}"
                        f" {c.mean_book_gross:9.3f} {c.bind_frac:6.1%} {c.turnover_yr:7.2f}")

    say("\n=== B. THE ANSWER — does ONE value of a clear 4b on BOTH panels at the same (g, rung)? ===")
    say("  (the absolute 2% cap is shown on the same footing as the comparand it has to beat)")
    for conv in CONVS:
        say(f"\n  convention {conv}" + ("   [HEADLINE]" if conv == HEADLINE_CONV else ""))
        say("  a      g     | " + "  ".join(f"{int(x):2d}bps U56/B136" for x in RUNGS) + "  | both-panel rungs")
        for a in ALPHAS + ["CAP2abs"]:
            al = alabel(a) if a != "CAP2abs" else "CAP2abs"
            cv = conv if a != "CAP2abs" else "-"
            for g in GROSSES:
                cells, both = [], 0
                for rung in RUNGS:
                    q = {p: df[(df.panel == p) & (df.a == al) & (df.conv == cv) & (df.gross == g)
                               & (df.cost_bps == rung)].iloc[0].pass4b for p in panels}
                    cells.append(f"   {'Y' if q['U56'] else '.'}/{'Y' if q['B136'] else '.'}     ")
                    both += int(q["U56"] and q["B136"])
                say(f"  {al:6s} {g:.2f}  | " + "".join(cells) + f"  | {both} of {len(RUNGS)}")
    say("\n  both-panel 4b pass count by a (summed over 2 gross x 4 rungs, max 8), headline convention G:")
    for a in ALPHAS + ["CAP2abs"]:
        al = alabel(a) if a != "CAP2abs" else "CAP2abs"
        cv = "G" if a != "CAP2abs" else "-"
        n = sum(int(all(df[(df.panel == p) & (df.a == al) & (df.conv == cv) & (df.gross == g)
                           & (df.cost_bps == rung)].iloc[0].pass4b for p in panels))
                for g in GROSSES for rung in RUNGS)
        say(f"    a = {al:8s} -> {n} of 8")

    say("\n=== C. KEEP COUNTS OVER ALL PUBLISHED ROWS ===")
    say(f"  ladder rows (5 a x 2 conv x 2 gross x 2 panels x 4 rungs = {len(lad)}):"
        f"  4b {int(lad.pass4b.sum())}   4a {int(lad.pass4a.sum())}")
    say(f"  CAP2 absolute reference rows ({len(ref)}):  4b {int(ref.pass4b.sum())}   4a {int(ref.pass4a.sum())}")
    for rung in RUNGS:
        d = lad[lad.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("  4b by (panel, convention, a) over 8 rows each (2 gross x 4 rungs):")
    for pname in panels:
        for conv in CONVS:
            say(f"    {pname:5s} {conv}: " + "   ".join(
                f"a={alabel(a):5s} {int(df[(df.panel == pname) & (df.conv == conv) & (df.a == alabel(a))].pass4b.sum())}/8"
                for a in ALPHAS))

    say("\n=== D. WHAT THE RELATIVE CAP DOES TO THE BOOK (g=0.75, convention G, 10 bps) ===")
    say("  panel a      | cap c_t at median N | max name  mean name  nHeld  bookGross  meanSHY  bind%  turn/yr")
    for pname in panels:
        px, invest = panels[pname]
        _, _, _, n_pr = _in_and_counts(px, invest)
        npm = float(n_pr.loc[px.index[WARMUP:]].median())
        for a in ALPHAS + ["CAP2abs"]:
            al = alabel(a) if a != "CAP2abs" else "CAP2abs"
            cv = "G" if a != "CAP2abs" else "-"
            c = sf[(sf.panel == pname) & (sf.a == al) & (sf.conv == cv) & (sf.gross == 0.75)].iloc[0]
            ct = "  n/a  " if al == "INF" else (f"{ABS_CAP:7.3%}" if al == "CAP2abs"
                                                else f"{float(al) * 0.75 / npm:7.3%}")
            say(f"  {pname:5s} {al:6s} | {ct}              | {c.max_name_w:7.2%} {c.mean_name_w:9.2%}"
                f" {c.mean_n_held:6.1f} {c.mean_book_gross:9.3f} {c.mean_sweep_w:8.3f}"
                f" {c.bind_frac:6.1%} {c.turnover_yr:7.2f}")

    say("\n=== E. RULE 8 — (a, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        spy_oos = px["SPY"].pct_change().fillna(0.0).loc[OOS_START:]
        for conv in CONVS:
            for rung in RUNGS:
                d = lad[(lad.panel == pname) & (lad.conv == conv) & (lad.cost_bps == rung)]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = d.loc[d[col].idxmax()]
                    rr = ref[(ref.panel == pname) & (ref.gross == pick.gross)
                             & (ref.cost_bps == rung)].iloc[0]
                    wf.append(dict(panel=pname, conv=conv, cost_bps=rung, chooser=chooser,
                                   pick_a=pick.a, pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                   OOS_MaxDD=pick.OOS_MaxDD,
                                   abs_OOS_Sharpe=rr.OOS_Sharpe, abs_OOS_CAGR=rr.OOS_CAGR,
                                   base_OOS_Sharpe=pick.base_OOS_Sharpe,
                                   spy_OOS_Sharpe=pick.spy_OOS_Sharpe, spy_OOS_CAGR=pick.spy_OOS_CAGR,
                                   full4b=bool(pick.pass4b),
                                   beats_spy_oos=bool(pick.OOS_Sharpe > pick.spy_OOS_Sharpe),
                                   beats_base_oos=bool(pick.OOS_Sharpe > pick.base_OOS_Sharpe),
                                   beats_abs_oos=bool(pick.OOS_Sharpe > rr.OOS_Sharpe),
                                   pick_is_live=bool(pick.a == "1.00"),
                                   pick_is_inf=bool(pick.a == "INF")))
                    say(f"  {pname:5s} {conv} {rung:5.1f}bps {chooser:11s} -> a {pick.a:6s} g {pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" abs-2% OOS {rr.OOS_CAGR:6.2%} / {rr.OOS_Sharpe:.4f} |"
                        f" live v2 OOS {pick.base_OOS_Sharpe:.4f} | SPY OOS {pick.spy_OOS_Sharpe:.4f} |"
                        f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks beating SPY OOS {int(wfd.beats_spy_oos.sum())} of {len(wfd)};"
        f"  beating the live book OOS {int(wfd.beats_base_oos.sum())} of {len(wfd)};"
        f"  beating the ABSOLUTE 2% cap OOS {int(wfd.beats_abs_oos.sum())} of {len(wfd)}")
    say(f"  picks landing on a=1.00 (the live de-grossed book) {int(wfd.pick_is_live.sum())}"
        f" of {len(wfd)};  on a=INF (the uncapped candidate) {int(wfd.pick_is_inf.sum())} of {len(wfd)}")
    say("  picks by a: " + ", ".join(f"{k} x{int(v)}" for k, v in wfd.pick_a.value_counts().items()))

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .shape.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
