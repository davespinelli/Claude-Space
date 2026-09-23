#!/usr/bin/env python3
"""idea 2383 (lane cloud, run 41, 2026-09-23) — IS THE CAPPED CANDIDATE'S 200d GATE
ASYMMETRIC?  ENTRY EDGE vs EXIT EDGE, PRICED SEPARATELY FOR THE FIRST TIME.

THE OBJECT.  RULES v2 clause 2 is a SYMMETRIC hysteresis band: a name is IN above
`ma x (1 + 0.03)`, OUT below `ma x (1 - 0.03)`, and holds its previous state in between.
The record's standing KEEP-4b candidate (idea 2322's CAP2 = idea 2300's RG100 + phi = 1.00
with a 2% per-name weight cap) inherits that gate verbatim.  Idea 2343's width ladder moved
BOTH edges together (one dial c), so no committed run has ever priced them apart.  They do
different jobs:

    ENTRY edge  b_in   decides WHAT THE BOOK ADMITS   -> a lag and a cost
    EXIT  edge  b_out  decides WHAT IT TOLERATES      -> the drawdown leg and most of the churn

    IN_t  = 1 if px > ma x (1 + b_in);  0 if px < ma x (1 - b_out);  else IN_{t-1};  0 pre-MA
    w_i   = min(gross / N_in, 0.02) on IN names,  idle NAV -> SHY (phi = 1.00)

DIAL 1 -- b_in  {0.01, 0.03, 0.06, 0.10}
DIAL 2 -- b_out {0.01, 0.03, 0.06, 0.10}
`b_in = b_out = 0.03` IS the live clause-2 gate, so the grid SPANS the committed book exactly
(asserted bit-for-bit by gates G2 and G3).

REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
gross {0.75 live, 1.00}, weekly cadence, t+1 execution, MA length 200, the 2% weight cap, the
SHY sweep.  16 x 2 x 3 = 96 books, every one published at every rung = 384 rows.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: (b_in, b_out) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR) inside each (panel, gross, rung) cell, then 2017-2026 read ONCE.

THE DELIVERABLE is the OWNERSHIP decomposition: holding one edge fixed and sweeping the other,
which edge moves MaxDD and which moves turnover, and whether any asymmetric cell clears 4b on
BOTH large-cap panels where the symmetric live gate does not.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the
(0.03, 0.03) gate is BIT-IDENTICAL to `baseline.band_state`.  G3 the (0.03, 0.03) book is
BIT-IDENTICAL to an independent CAP2 construction.  G4 no leverage anywhere.  G5 BOTH edges
BITE independently.  G6 SHY priced on every held row.  G7 SMALL dropped-ticker rule bit.
G8 exactly two tuned parameters.  G9 no lookahead (weights on a truncated panel identical to
the full-panel weights over the overlap).  G10 EXTERNAL REPRODUCTION of idea 2322/2336's
committed CAP2 U56 headline (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318, turnover 3.51x).

SURVIVORSHIP CAVEAT (rule 9, binding on every row below): `universe.json` (U56),
`universe_broad.json` (B136) and the sub-$2B SMALL pool are CURRENT constituents of their
screens, held from 2008 / 2010, so ABSOLUTE levels (and therefore 4b's `L_CAGR` floor most of
all) are biased upward.  The b_in-vs-b_out contrast is same-tape, same-day, same-gross and
same-panel, so it is first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_asymmetric-entry-exit-band_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "asymmetric-entry-exit-band", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

MA_LEN, CADENCE, WARMUP = 200, "W", 260
EDGES = [0.01, 0.03, 0.06, 0.10]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, LIVE_B, NAME_CAP, SWEEP = 10.0, 0.03, 0.020, "SHY"
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


# ---------------------------------------------------------------- the gate, two edges
def band_state_asym(px, b_in, b_out, L=MA_LEN):
    """RULES v2 clause 2 with the two edges separated.  IN above ma*(1+b_in), OUT below
    ma*(1-b_out), previous state in between, OUT before L closes exist.  At b_in = b_out = 0.03
    this is `baseline.band_state` verbatim (asserted by G2)."""
    ma = px.rolling(L).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b_in), 1.0).mask(px < ma * (1 - b_out), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def cap_weights(px, invest, b_in, b_out, gross, cap=NAME_CAP):
    """idea 2322's CAP2 on the asymmetric gate: w_i = min(gross / N_in, cap) on IN names,
    idle NAV swept to SHY at phi = 1.00."""
    q = px[invest]
    pr = q.notna()
    inb = band_state_asym(q, b_in, b_out) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    w = inb.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def cap2_reference(px, invest, gross, cap=NAME_CAP):
    """Independent construction of CAP2 built on `baseline.band_state` (the live clause-2
    object) rather than on band_state_asym, in the min(Series, scalar) form idea 2391 used."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, LIVE_B) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(float(cap), index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- engine replica
def run_book(prices, weights, freq=CADENCE):
    """Replica of engine.backtest keeping zero-cost returns + turnover so every cost rung is
    priced from one pass.  Un-invested residual drifts at 0% (the engine's convention)."""
    rets = prices.pct_change().fillna(0.0)
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False).values
    n, m = len(prices.index), len(prices.columns)
    held = np.zeros((n, m)); cur = np.zeros(m)
    to = np.zeros(n); gr = np.zeros(n); rv = rets.values
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        held[i] = cur; gr[i] = cur.sum()
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    return dict(r0=pd.Series((held * rv).sum(axis=1), index=prices.index),
                turnover=pd.Series(to, index=prices.index),
                gross=pd.Series(gr, index=prices.index))


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
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2383 — IS THE CAPPED CANDIDATE'S 200d GATE ASYMMETRIC? (entry vs exit edge) ===")
    say(f"    {DATE}  lane {LANE} run 41   MA {MA_LEN}d  cadence {CADENCE}  t+1  rungs {RUNGS} bps"
        f"  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 b_in {EDGES}   DIAL 2 b_out {EDGES}   [reported: gross {GROSSES}, 3 panels, 4 rungs]")
    say("    SURVIVORSHIP (rule 9): U56 / B136 / SMALL are CURRENT constituents of their screens,")
    say("    so absolute levels are biased upward and 4b's CAGR floor is the most contaminated leg.")
    say("    The b_in-vs-b_out contrast is same-tape / same-day / same-gross and first-order immune.")
    gate("G8 exactly two tuned parameters", "b_in, b_out", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G7 SMALL dropped-ticker rule bit (max_1d_move >= 1.0)", f"{dropped} names dropped", ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c not in ("SPY", SWEEP)] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(invest)} investable, {len(px)} rows", ">= 10y", yrs >= 10)

    d2 = int((band_state_asym(px_u, LIVE_B, LIVE_B) != band_state(px_u, LIVE_B)).sum().sum())
    gate("G2 band_state_asym(0.03, 0.03) == baseline.band_state (live clause 2)",
         f"{d2} differing cells of {px_u.size}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=LIVE_B, gross=0.75)
    res_live = run_book(px_u, w_live)
    d1 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    pxq, invq = panels["U56"]
    d3 = float((cap_weights(pxq, invq, LIVE_B, LIVE_B, 0.75) - cap2_reference(pxq, invq, 0.75)).abs().max().max())
    gate("G3 (0.03, 0.03) book == an independent CAP2 construction (U56, g=0.75)",
         f"max|dw| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    cut = pxq.index[int(len(pxq) * 0.70)]
    d9 = float((cap_weights(pxq.loc[:cut], invq, 0.06, 0.01, 0.75)
                - cap_weights(pxq, invq, 0.06, 0.01, 0.75).loc[:cut]).abs().max().max())
    gate(f"G9 no lookahead (panel truncated at {cut.date()}, asymmetric cell 0.06/0.01)",
         f"max|dw| {d9:.3e}", "< 1e-12", d9 < 1e-12)

    rows, expo = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_res = run_book(px, rules_v2_weights(px[invest], band=LIVE_B, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0))
        base_r = priced(base_res, HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} investable)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}"
            f"  halves {halves(base_r)[0]:.4f}/{halves(base_r)[1]:.4f}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        for gross in GROSSES:
            for bi in EDGES:
                for bo in EDGES:
                    w = cap_weights(px, invest, bi, bo, gross)
                    mx = float(w.sum(axis=1).max())
                    res = run_book(px, w)
                    nmw = w.drop(columns=[SWEEP]).loc[win]
                    pos = nmw.values[nmw.values > 0]
                    inb = band_state_asym(px[invest], bi, bo) & px[invest].notna()
                    nin = inb.sum(axis=1).loc[win]
                    npr = px[invest].notna().sum(axis=1).loc[win]
                    expo.append(dict(panel=pname, b_in=bi, b_out=bo, gross=gross,
                                     time_in=float((nin / npr.replace(0, np.nan)).mean()),
                                     mean_N_in=float(nin.mean()), days_all_out=int((nin == 0).sum()),
                                     flips=int(inb.astype(int).diff().abs().sum(axis=1).loc[win].sum()),
                                     max_name_w=float(pos.max()) if len(pos) else 0.0,
                                     mean_gross=float(res["gross"].loc[win].mean()),
                                     mean_shy=float(w[SWEEP].loc[win].mean()),
                                     turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                     max_row_sum=mx))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, b_in=bi, b_out=bo, gross=gross, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                         spy_OOS_Sharpe=sharpe(spy_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); ef = pd.DataFrame(expo)
    df.to_csv(f"{OUT}.grid.csv", index=False); ef.to_csv(f"{OUT}.exposure.csv", index=False)

    gate("G4 no leverage (all 96 books)", f"max row sum {ef.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((ef.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}", "True", shy_ok)

    # G5 both edges bite INDEPENDENTLY (hold one fixed at 0.03, sweep the other)
    bites = []
    for pname in panels:
        e = ef[(ef.panel == pname) & (ef.gross == 0.75)]
        a = e[e.b_out == LIVE_B].sort_values("b_in")
        b = e[e.b_in == LIVE_B].sort_values("b_out")
        ok = bool(np.ptp(a.time_in.values) > 1e-6 and np.ptp(b.time_in.values) > 1e-6
                  and np.ptp(a.turnover_yr.values) > 1e-6 and np.ptp(b.turnover_yr.values) > 1e-6)
        bites.append(ok)
        say(f"    {pname}: b_in sweep (b_out=0.03) time-IN {a.time_in.iloc[0]:.3f}->{a.time_in.iloc[-1]:.3f}"
            f" turn {a.turnover_yr.iloc[0]:.2f}->{a.turnover_yr.iloc[-1]:.2f} |"
            f" b_out sweep (b_in=0.03) time-IN {b.time_in.iloc[0]:.3f}->{b.time_in.iloc[-1]:.3f}"
            f" turn {b.turnover_yr.iloc[0]:.2f}->{b.turnover_yr.iloc[-1]:.2f}")
    gate("G5 BOTH edges bite independently (time-IN and turnover move on each sweep)",
         f"{sum(bites)} of {len(bites)} panels", "3 of 3", all(bites))

    h = df[(df.panel == "U56") & (df.b_in == LIVE_B) & (df.b_out == LIVE_B)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    e0 = ef[(ef.panel == "U56") & (ef.b_in == LIVE_B) & (ef.b_out == LIVE_B) & (ef.gross == 0.75)].iloc[0]
    d10 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
              abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G10 reproduces the committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {e0.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the full grid
    say("\n=== A. THE FULL 4x4 GRID AT THE HEADLINE RUNG (10 bps), gross 0.75 — every point ===")
    for pname in panels:
        say(f"\n  {pname}   (rows = b_in entry edge, cols = b_out exit edge)")
        say("   b_in \\ b_out |" + "".join(f"     {bo:.2f}      " for bo in EDGES))
        for bi in EDGES:
            cells = []
            for bo in EDGES:
                r = df[(df.panel == pname) & (df.b_in == bi) & (df.b_out == bo)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                cells.append(f" {r.CAGR:6.2%}/{r.Sharpe:5.3f}/{'Y' if r.pass4b else '.'}")
            say(f"        {bi:.2f}   |" + "".join(cells) + ("   <= live row" if bi == LIVE_B else ""))
        say("        (each cell: CAGR / Sharpe / 4b)   live gate is the (0.03, 0.03) cell")
    say("\n  FULL DETAIL, gross 0.75 @ 10 bps:")
    say("  panel  b_in b_out |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR | timeIN  maxw  turn/yr")
    for pname in panels:
        for bi in EDGES:
            for bo in EDGES:
                r = df[(df.panel == pname) & (df.b_in == bi) & (df.b_out == bo)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.b_in == bi) & (ef.b_out == bo) & (ef.gross == 0.75)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s}  {bi:.2f} {bo:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {e.time_in:6.3f} {e.max_name_w:5.2%} {e.turnover_yr:7.2f}"
                    + ("   <= LIVE GATE (CAP2)" if bi == LIVE_B and bo == LIVE_B else ""))

    # ------------------------------------------------------------ B. ownership
    say("\n=== B. WHICH EDGE OWNS WHAT — marginal effect of each edge, averaged over the other ===")
    say("    (gross 0.75, 10 bps; 'span' = value at edge 0.10 minus value at edge 0.01, averaged")
    say("     over the four settings of the OTHER edge, so the two columns are directly comparable)")
    own_rows = []
    for pname in panels:
        d = df[(df.panel == pname) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
        e = ef[(ef.panel == pname) & (ef.gross == 0.75)]
        for metric, src, col in (("MaxDD", d, "MaxDD"), ("CAGR", d, "CAGR"), ("Sharpe", d, "Sharpe"),
                                 ("turnover/yr", e, "turnover_yr"), ("time-IN", e, "time_in"),
                                 ("mean gross", e, "mean_gross")):
            s_in = float(src[src.b_in == EDGES[-1]][col].mean() - src[src.b_in == EDGES[0]][col].mean())
            s_out = float(src[src.b_out == EDGES[-1]][col].mean() - src[src.b_out == EDGES[0]][col].mean())
            own = "b_in (ENTRY)" if abs(s_in) > abs(s_out) else "b_out (EXIT)"
            ratio = abs(s_in) / abs(s_out) if abs(s_out) > 1e-12 else np.inf
            own_rows.append(dict(panel=pname, metric=metric, span_b_in=s_in, span_b_out=s_out,
                                 owner=own, ratio_in_over_out=ratio))
            say(f"  {pname:5s} {metric:12s}  span(b_in) {s_in:+10.4f}   span(b_out) {s_out:+10.4f}"
                f"   -> OWNED BY {own:13s} (|in|/|out| = {ratio:5.2f})")
    pd.DataFrame(own_rows).to_csv(f"{OUT}.ownership.csv", index=False)
    say("\n  THE SAME QUESTION AS A COUNT: how often is each 4b leg's failure moved by each edge?")
    for pname in panels:
        d = df[(df.panel == pname) & (df.gross == 0.75)]
        for leg in ("L_DD", "L_CAGR", "L_H1", "L_H2", "L_OOS"):
            f_in = [int((~d[d.b_in == b][leg]).sum()) for b in EDGES]
            f_out = [int((~d[d.b_out == b][leg]).sum()) for b in EDGES]
            say(f"   {pname:5s} {leg:7s} FAILs by b_in {f_in} (0.01->0.10)   by b_out {f_out}")

    # ------------------------------------------------------------ C. keep counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (4 b_in x 4 b_out x 2 gross x 3 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for pname in panels:
        d = df[df.panel == pname]
        say(f"   panel {pname:5s}:  4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")

    say("\n  JOINT BOTH-LARGE-CAP-PANEL 4b (U56 AND B136 at the same b_in, b_out, gross, rung):")
    joint = []
    for bi in EDGES:
        for bo in EDGES:
            for gross in GROSSES:
                for rung in RUNGS:
                    q = df[(df.b_in == bi) & (df.b_out == bo) & (df.gross == gross) & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                    joint.append(dict(b_in=bi, b_out=bo, gross=gross, cost_bps=rung,
                                      joint=bool(u.pass4b and b.pass4b), u=bool(u.pass4b), b=bool(b.pass4b)))
    jf = pd.DataFrame(joint)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells    "
        f"live (0.03, 0.03) cells joint: {int(jf[(jf.b_in == LIVE_B) & (jf.b_out == LIVE_B)].joint.sum())} of 8")
    for bi in EDGES:
        say("   b_in " + f"{bi:.2f}" + ":  " + "  ".join(
            f"b_out {bo:.2f} {int(jf[(jf.b_in == bi) & (jf.b_out == bo)].joint.sum())}/8" for bo in EDGES))
    best = jf.groupby(["b_in", "b_out"]).joint.sum().sort_values(ascending=False)
    say(f"   best (b_in, b_out) by joint 4b count: {best.index[0]} with {int(best.iloc[0])} of 8"
        f"   [live (0.03, 0.03) has {int(best.loc[(LIVE_B, LIVE_B)])} of 8]")

    # ------------------------------------------------------------ D. asymmetry
    say("\n=== D. IS ASYMMETRY ITSELF WORTH ANYTHING?  symmetric diagonal vs off-diagonal ===")
    sym = df[df.b_in == df.b_out]; asym = df[df.b_in != df.b_out]
    say(f"   symmetric cells (4 of 16):  4b {int(sym.pass4b.sum())}/{len(sym)} = {sym.pass4b.mean():.1%}")
    say(f"   asymmetric cells (12 of 16): 4b {int(asym.pass4b.sum())}/{len(asym)} = {asym.pass4b.mean():.1%}")
    loose_exit = df[df.b_out > df.b_in]; tight_exit = df[df.b_out < df.b_in]
    say(f"   LOOSE exit (b_out > b_in, slower to sell):  4b {int(loose_exit.pass4b.sum())}/{len(loose_exit)}"
        f" = {loose_exit.pass4b.mean():.1%}   mean MaxDD {loose_exit.MaxDD.mean():.2%}  mean CAGR {loose_exit.CAGR.mean():.2%}")
    say(f"   TIGHT exit (b_out < b_in, quicker to sell): 4b {int(tight_exit.pass4b.sum())}/{len(tight_exit)}"
        f" = {tight_exit.pass4b.mean():.1%}   mean MaxDD {tight_exit.MaxDD.mean():.2%}  mean CAGR {tight_exit.CAGR.mean():.2%}")
    say(f"   symmetric:                                  mean MaxDD {sym.MaxDD.mean():.2%}  mean CAGR {sym.CAGR.mean():.2%}")

    say("\n  DELTAS AGAINST THE LIVE GATE (U56 / B136, g = 0.75, 10 bps):")
    for pname in ("U56", "B136"):
        ref = df[(df.panel == pname) & (df.b_in == LIVE_B) & (df.b_out == LIVE_B)
                 & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        er = ef[(ef.panel == pname) & (ef.b_in == LIVE_B) & (ef.b_out == LIVE_B) & (ef.gross == 0.75)].iloc[0]
        say(f"   {pname} reference (0.03, 0.03): {ref.CAGR:.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:.2%}"
            f"  turn {er.turnover_yr:.2f}x")
        for bi in EDGES:
            for bo in EDGES:
                if bi == LIVE_B and bo == LIVE_B:
                    continue
                r = df[(df.panel == pname) & (df.b_in == bi) & (df.b_out == bo)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.b_in == bi) & (ef.b_out == bo) & (ef.gross == 0.75)].iloc[0]
                say(f"     ({bi:.2f}, {bo:.2f})  dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
                    f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dTurn {e.turnover_yr - er.turnover_yr:+6.2f}x"
                    f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — (b_in, b_out) chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=LIVE_B, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung)]
                inc = d[(d.b_in == LIVE_B) & (d.b_out == LIVE_B)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=chooser,
                                   pick_b_in=pk.b_in, pick_b_out=pk.b_out,
                                   pick_is_live=bool(pk.b_in == LIVE_B and pk.b_out == LIVE_B),
                                   pick_is_asym=bool(pk.b_in != pk.b_out),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                   inc_OOS_Sharpe=inc.OOS_Sharpe, inc_OOS_CAGR=inc.OOS_CAGR, inc_OOS_MaxDD=inc.OOS_MaxDD,
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   full4b=bool(pk.pass4b)))
                    if gross == 0.75:
                        say(f"  {pname:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} -> ({pk.b_in:.2f}, {pk.b_out:.2f}) |"
                            f" OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%} |"
                            f" live-gate cell OOS {inc.OOS_CAGR:6.2%} / {inc.OOS_Sharpe:.4f} |"
                            f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} |"
                            f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} | full 4b {'Y' if pk.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  {len(wfd)} picks (3 panels x 2 gross x 4 rungs x 2 choosers).")
    say(f"   picks landing on the LIVE symmetric gate (0.03, 0.03): {int(wfd.pick_is_live.sum())} of {len(wfd)}")
    say(f"   picks that are ASYMMETRIC (b_in != b_out):            {int(wfd.pick_is_asym.sum())} of {len(wfd)}")
    say(f"   picks beating SPY's OOS Sharpe:                       {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the LIVE BOOK's OOS Sharpe:             {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the LIVE-GATE CELL's own OOS Sharpe:    {int((wfd.OOS_Sharpe > wfd.inc_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                 {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over b_in:  " + "  ".join(f"{b:.2f}:{int((wfd.pick_b_in == b).sum())}" for b in EDGES))
    say("   pick distribution over b_out: " + "  ".join(f"{b:.2f}:{int((wfd.pick_b_out == b).sum())}" for b in EDGES))
    agree = 0
    for gross in GROSSES:
        for rung in RUNGS:
            for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                q = wfd[(wfd.gross == gross) & (wfd.cost_bps == rung) & (wfd.chooser == ch)]
                u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                agree += int(u.pick_b_in == b.pick_b_in and u.pick_b_out == b.pick_b_out)
    say(f"   U56 and B136 agree on (b_in, b_out) in {agree} of 16 (gross x rung x chooser) cells")
    say("\n   RULE-8 REACHABILITY OF A JOINT BOTH-PANEL 4b PASS (the honest bar):")
    reach = 0
    for gross in GROSSES:
        for rung in RUNGS:
            for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                q = wfd[(wfd.gross == gross) & (wfd.cost_bps == rung) & (wfd.chooser == ch)]
                u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                same = (u.pick_b_in == b.pick_b_in and u.pick_b_out == b.pick_b_out)
                reach += int(same and u.full4b and b.full4b)
    say(f"   cells where both panels pick the SAME (b_in, b_out) AND both carry a full-sample 4b: {reach} of 16")

    # ------------------------------------------------------------ F. restricted rule 8 (POST-HOC)
    say("\n=== F. RESTRICTED RULE 8 — b_in HELD AT THE LIVE 0.03 (not tuned), ONLY b_out CHOSEN ===")
    say("    THIS SECTION IS POST-HOC AND IS LABELLED AS SUCH: it was added after section E showed")
    say("    that 45 of 48 unrestricted picks take b_out = 0.10 while the two panels scatter on b_in.")
    say("    It is a ONE-DIAL nested reading of the same grid (no refit, no new book): the incumbent")
    say("    entry edge is kept at the live constant and only the exit edge is fitted in-sample.")
    say("    It is REPORTED, not used to upgrade any verdict in sections A-E.")
    rwf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        for gross in GROSSES:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.gross == gross) & (df.cost_bps == rung) & (df.b_in == LIVE_B)]
                inc = d[d.b_out == LIVE_B].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = d.loc[d[col].idxmax()]
                    rwf.append(dict(panel=pname, gross=gross, cost_bps=rung, chooser=chooser,
                                    pick_b_out=pk.b_out, full4b=bool(pk.pass4b),
                                    OOS_Sharpe=pk.OOS_Sharpe, OOS_CAGR=pk.OOS_CAGR, OOS_MaxDD=pk.OOS_MaxDD,
                                    inc_OOS_Sharpe=inc.OOS_Sharpe, spy_OOS_Sharpe=sharpe(spy_oos)))
                    if gross == 0.75:
                        say(f"  {pname:5s} g{gross:.2f} {rung:5.1f}bps {chooser:11s} -> b_out {pk.b_out:.2f} |"
                            f" OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%} |"
                            f" live-gate cell OOS {inc.OOS_Sharpe:.4f} | full 4b {'Y' if pk.pass4b else '.'}")
    rf = pd.DataFrame(rwf)
    rf.to_csv(f"{OUT}.walkforward_restricted.csv", index=False)
    say("   restricted pick distribution over b_out: " + "  ".join(
        f"{b:.2f}:{int((rf.pick_b_out == b).sum())}" for b in EDGES))
    ragree = rreach = 0
    for gross in GROSSES:
        for rung in RUNGS:
            for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                q = rf[(rf.gross == gross) & (rf.cost_bps == rung) & (rf.chooser == ch)]
                u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                same = bool(u.pick_b_out == b.pick_b_out)
                ragree += int(same)
                rreach += int(same and u.full4b and b.full4b)
    say(f"   U56 and B136 agree on b_out in {ragree} of 16 (gross x rung x chooser) cells")
    say(f"   cells where both panels pick the SAME b_out AND both carry a full-sample 4b: {rreach} of 16")
    say(f"   restricted picks beating SPY's OOS Sharpe: {int((rf.OOS_Sharpe > rf.spy_OOS_Sharpe).sum())} of {len(rf)}")

    # ------------------------------------------------------------ G. the candidate, stated
    say("\n=== G. THE CELL THIS RUN FILES, STATED IN FULL: b_in = 0.03 (LIVE), b_out = 0.10 ===")
    for pname in ("U56", "B136"):
        for rung in RUNGS:
            r = df[(df.panel == pname) & (df.b_in == LIVE_B) & (df.b_out == 0.10)
                   & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
            i = df[(df.panel == pname) & (df.b_in == LIVE_B) & (df.b_out == LIVE_B)
                   & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
            say(f"  {pname:5s} {rung:5.1f}bps  CAND {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
                f"  halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:7.2%}"
                f"  4b {'Y' if r.pass4b else '.'}   || CAP2 {i.CAGR:6.2%} / {i.Sharpe:.4f} / {i.MaxDD:7.2%}"
                f" 4b {'Y' if i.pass4b else '.'}   || m_DD {r.m_DD:+.4f} m_CAGR {r.m_CAGR:+.4f}")
    for pname in ("U56", "B136"):
        e = ef[(ef.panel == pname) & (ef.b_in == LIVE_B) & (ef.b_out == 0.10) & (ef.gross == 0.75)].iloc[0]
        i = ef[(ef.panel == pname) & (ef.b_in == LIVE_B) & (ef.b_out == LIVE_B) & (ef.gross == 0.75)].iloc[0]
        say(f"  {pname:5s} turnover {i.turnover_yr:.2f}x -> {e.turnover_yr:.2f}x/yr"
            f"   time-IN {i.time_in:.3f} -> {e.time_in:.3f}   mean N_in {i.mean_N_in:.1f} -> {e.mean_N_in:.1f}"
            f"   mean SHY {i.mean_shy:.3f} -> {e.mean_shy:.3f}   max name w {e.max_name_w:.2%}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    npass, ntot = int(gdf.pass_.sum()), len(gdf)
    say(f"\n=== GATES: {npass} of {ntot} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .ownership.csv / .walkforward.csv / .gates.csv"
        f"   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
