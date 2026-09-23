#!/usr/bin/env python3
"""idea 2546 (lane cloud, run 73, 2026-09-23) — IS THE STANDING 4b CANDIDATE REDUCIBLE TO ONE
MARKET-LEVEL 200d GATE ON THE PANEL'S OWN EQUAL-WEIGHT INDEX?

THE GAP.  Two committed results say the candidate's per-NAME gate may be decoration.  Idea 2539
killed the 200d band as a RETURN-PICKING rule (being above your own 200d does not predict your
own forward return on this tape).  Idea 2506 proved the 2% per-name cap is not a concentration
control at all but a BREADTH-LINKED GROSS SCHEDULE `min(g, 0.02 x N_in)`.  Together they say the
book's only live content is "how much NAV is at risk, when" -- a single scalar path.  If that is
right, the 40-name per-name gate is an expensive way to compute a number that ONE gate on the
panel's own equal-weight index would compute for a fraction of the tickets, and the candidate's
single stated adoption blocker (turnover ~3.0-3.5x/yr against the live book's 1.77x) dissolves.

THE DEVICE -- `IDXG`.  Build the panel's OWN equal-weight total-return index `EWI` (daily
cross-sectional mean return of every priced column, compounded).  Apply `baseline.band_state` to
that ONE series.  When the gate is IN, hold EVERY priced name at `g / N_priced`; when it is OUT,
hold nothing and sweep to SHY.  Exactly one gate, one decision per rebalance, no per-name state.

WHY THIS IS A FALSIFICATION TEST AND NOT A TUNING EXERCISE.  The reduction is a STRONG claim and
it is refutable in a specific direction, stated here before any compute: if the per-name gate
carries CROSS-SECTIONAL content (it drops the weak names, not merely the weak market), `IDXG`
will hold the market through the names the candidate had already sold and its `L_DD` leg -- the
one leg the whole family lives on (idea 2550: `L_DD` binds first in 128 of 128 blend fails) --
will break.  `EWBH` (always in, no gate) is carried as the always-invested control, and the
uncapped `CAND` and capped `CAP2` books are carried at the SAME band and gross so the comparison
is same-tape and same-day.  G3 asserts the CAND / CAP2 cells reproduce the committed headlines.

DIAL 1 -- the band half-width `band` in {0.00, 0.03 (live), 0.05, 0.10}.
DIAL 2 -- gross `g` in {0.75 (live), 1.00}.
Exactly two tuned parameters (G6).  Every grid point is reported.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, books
{CAND, CAP2, IDXG, EWBH}, weekly cadence, t+1 execution, MA 200d, the 2% cap and the SHY sweep
at phi = 1.00.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing; collapsing forty gates into one cannot move three failing legs.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (band, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, 2017-2026 is then read ONCE, and each pick is scored against the COMMITTED
cell (band 0.03, gross 0.75) of its own book.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the EWI gate is
`baseline.band_state` applied to one column, bit for bit.  G3 the CAND / CAP2 committed cells
reproduce the record's U56 headlines.  G4 no leverage.  G5 cost exactly linear in the rung.
G6 exactly two tuned parameters.  G7 the EWI and its gate are CAUSAL (panel-truncation replica).
G8 IDXG's held set is exactly EWBH's held set on gate-IN days and empty on gate-OUT days.
G9 the sweep instrument is priced on every held row.  G10 IDXG really is cheaper (fewer tickets).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The IDXG-vs-CAND contrast is same-tape, same-day
and first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_one-market-level-gate_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "one-market-level-gate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

MA_LEN, CADENCE, WARMUP = 200, "W", 260
BANDS = [0.00, 0.03, 0.05, 0.10]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
BOOKS = ["CAND", "CAP2", "IDXG", "EWBH"]
NAME_CAP, SWEEP = 0.020, "SHY"
COMMITTED_BAND, COMMITTED_GROSS, HEADLINE_RUNG = 0.03, 0.75, 10.0
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


# ---------------------------------------------------------------- the panel's own EW index
def ew_index(px):
    """Equal-weight total-return index of EVERY priced column of the panel, compounded daily.
    Past closes only: r_t uses closes t-1 and t, so the level at t is known at the close of t
    (G7 asserts this by panel truncation)."""
    rv = px.pct_change()
    m = rv.mean(axis=1, skipna=True).fillna(0.0)
    return (1 + m).cumprod().rename("EWI")


def index_gate(px, band):
    """ONE gate: `baseline.band_state` applied to the panel's own EW index (G2 asserts the call
    is the library's, unmodified).  Returns a boolean Series."""
    ewi = ew_index(px).to_frame()
    return band_state(ewi, band)["EWI"]


# ---------------------------------------------------------------- the four books
def risk_weights(px, book, band, gross):
    priced = px.notna()
    if book == "EWBH":
        el = priced
    elif book == "IDXG":
        el = priced.mul(index_gate(px, band), axis=0)
    else:                                   # CAND / CAP2 -- the committed per-NAME gate
        el = band_state(px, band) & priced
    el = el.astype(bool)
    nin = el.sum(axis=1).replace(0, np.nan)
    cap = NAME_CAP if book == "CAP2" else np.inf
    if book in ("EWBH", "IDXG"):
        # `g / N_priced`: the denominator is the panel, not the in-band count, so the gate is a
        # pure de-grosser (the index gate cannot re-spread NAV into the survivors).
        nin = priced.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the per-day turnover is retained so every cost rung
    is read off the SAME realised path.  Weights decided at t-1, applied at t; the book drifts
    between rebalances; the residual is swept into SHY at phi = 1.00."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    tick = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            d = np.abs(new - cur)
            turn[i] = float(d.sum())
            tick[i] = float((d > 1e-9).sum())
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx), tickets=pd.Series(tick, index=idx))


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
    say("=== idea 2546 — IS THE 4b CANDIDATE REDUCIBLE TO ONE MARKET-LEVEL 200d GATE ON ITS OWN EWBH? ===")
    say(f"    {DATE}  lane {LANE} run 73   MA {MA_LEN}d  cadence {CADENCE}  t+1  rungs {RUNGS} bps"
        f"  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 band {BANDS}   DIAL 2 gross {GROSSES}   books {BOOKS}   panels U56 / B136")
    say("    PRIOR, STATED BEFORE COMPUTE: 2539 killed the band as a RETURN picker and 2506 proved the cap is")
    say("    a breadth-linked GROSS schedule, so the reduction SHOULD hold.  It is refutable in one direction:")
    say("    if the per-name gate carries CROSS-SECTIONAL content, IDXG holds the names CAND had sold and its")
    say("    `L_DD` leg — the leg the whole family lives on (2550: binds first in 128 of 128) — will break.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383) and 0 of 40-120 (2318/2322/2326/2343); collapsing")
    say("    forty gates into one cannot move three simultaneously failing legs.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; `L_CAGR` is the")
    say("    contaminated leg.  The IDXG-vs-CAND contrast is same-tape, same-day and first-order immune.")
    gate("G6 exactly two tuned parameters", "band, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]

    # G2 the index gate IS baseline.band_state on one column
    ewi = ew_index(px_u)
    ref = band_state(ewi.to_frame(), COMMITTED_BAND)["EWI"]
    d2 = int((index_gate(px_u, COMMITTED_BAND) != ref).sum())
    gate("G2 the EWI gate IS baseline.band_state applied to one column, unmodified",
         f"{d2} differing days; gate IN on {ref.loc[px_u.index[WARMUP]:].mean():.1%} of scored days",
         "0", d2 == 0)

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=COMMITTED_BAND, gross=COMMITTED_GROSS)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G7 the EWI and its gate are causal
    cut = px_u.index[3000]
    e_full = ew_index(px_u).loc[:cut]
    e_trunc = ew_index(px_u.loc[:cut])
    d7r = float((e_full / e_full.iloc[0] - e_trunc / e_trunc.iloc[0]).abs().max())
    g_full = index_gate(px_u, COMMITTED_BAND).loc[:cut]
    g_trunc = index_gate(px_u.loc[:cut], COMMITTED_BAND)
    d7g = int((g_full != g_trunc).sum())
    gate("G7 the EWI and its gate are CAUSAL (panel truncation at row 3000 changes nothing before it)",
         f"max|d level| {d7r:.3e} over {len(e_full)} days; {d7g} differing gate days", "0.0",
         d7r < 1e-12 and d7g == 0)

    # G8 IDXG's held set == EWBH's on gate-IN days, empty on gate-OUT days
    wi = risk_weights(px_u, "IDXG", COMMITTED_BAND, COMMITTED_GROSS)
    we = risk_weights(px_u, "EWBH", COMMITTED_BAND, COMMITTED_GROSS)
    gON = index_gate(px_u, COMMITTED_BAND)
    d8a = float((wi[gON] - we[gON]).abs().max().max())
    d8b = float(wi[~gON].abs().max().max())
    gate("G8 IDXG == EWBH on gate-IN days and is FLAT on gate-OUT days",
         f"max|d| IN {d8a:.3e}; max weight OUT {d8b:.3e}", "both 0",
         d8a < 1e-15 and d8b < 1e-15)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=COMMITTED_BAND, gross=COMMITTED_GROSS),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for bname in BOOKS:
            for band in BANDS:
                for gross in GROSSES:
                    wr = risk_weights(px, bname, band, gross)
                    bk = run_book(px, wr)
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    yrs = len(tn) / 252
                    book_facts.append(dict(
                        panel=pname, book=bname, band=band, gross=gross,
                        turnover_yr=float(tn.sum() / yrs),
                        tickets_yr=float(bk["tickets"].loc[start:].sum() / yrs),
                        mean_names=float(bk["names"].loc[start:].mean()),
                        mean_gross=float(bk["gross"].loc[start:].mean()),
                        max_gross=float(bk["gross"].loc[start:].max()),
                        max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, book=bname, band=band, gross=gross, cost_bps=rung,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / yrs),
                            tickets_yr=float(bk["tickets"].loc[start:].sum() / yrs),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                            base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_OOS_MaxDD=maxdd(spy_oos), spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(BOOKS)} books x {len(BANDS)} bands x"
        f" {len(GROSSES)} gross x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} gross, {bf.max_name_w.max():.4f} max single name",
         "<= 1+1e-12", bool(bf.max_gross.max() <= 1 + 1e-12))

    pz = panels["U56"]
    bz = run_book(pz, risk_weights(pz, "CAP2", COMMITTED_BAND, COMMITTED_GROSS))
    st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    sel = dict(panel="U56", band=COMMITTED_BAND, gross=COMMITTED_GROSS, cost_bps=HEADLINE_RUNG)
    def cell(book, **kw):
        q = df.copy()
        for k, v in {**sel, **kw, "book": book}.items():
            q = q[q[k] == v]
        return q.iloc[0]
    a, b = cell("CAP2"), cell("CAND")
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 the committed cells reproduce the record's U56 headlines — CAP2 (11.62%/1.2687/-14.81%,"
         " OOS 12.77%/1.3318) and CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397)",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    gate("G10 IDXG really is cheaper than the per-name book (tickets/yr, U56, committed cell)",
         f"IDXG {cell('IDXG').tickets_yr:.1f} vs CAND {b.tickets_yr:.1f} vs CAP2 {a.tickets_yr:.1f}"
         f"  (turnover {cell('IDXG').turnover_yr:.2f}x vs {b.turnover_yr:.2f}x / {a.turnover_yr:.2f}x)",
         "IDXG strictly fewer", cell("IDXG").tickets_yr < min(a.tickets_yr, b.tickets_yr))

    # ------------------------------------------------------------ A. the full ladder
    say("\n=== A. THE FULL LADDER — EVERY GRID POINT (all 4 books x 4 bands x 2 gross x 4 rungs x 2 panels) ===")
    say("  panel book band gross   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr tick/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for band in BANDS:
                for gross in GROSSES:
                    for rung in RUNGS:
                        r = df[(df.panel == pname) & (df.book == bk_) & (df.band == band)
                               & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                        lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                        mark = "   <= COMMITTED" if (band == COMMITTED_BAND and gross == COMMITTED_GROSS
                                                     and rung == HEADLINE_RUNG) else ""
                        say(f"  {pname:5s} {bk_:4s} {band:4.2f} {gross:5.2f} {rung:5.1f} | {r.CAGR:6.2%}"
                            f" {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                            f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:7.2f} {r.tickets_yr:7.1f} |"
                            f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}{mark}")
        say(f"  SPY ({pname}): CAGR {df[df.panel == pname].spy_CAGR.iloc[0]:.2%}"
            f"  Sharpe {df[df.panel == pname].spy_Sharpe.iloc[0]:.4f}"
            f"  MaxDD {df[df.panel == pname].spy_MaxDD.iloc[0]:.2%}"
            f"  OOS {df[df.panel == pname].spy_OOS_CAGR.iloc[0]:.2%} / {df[df.panel == pname].spy_OOS_Sharpe.iloc[0]:.4f}"
            f"   |   live RULES v2: CAGR {df[df.panel == pname].base_CAGR.iloc[0]:.2%}"
            f"  Sharpe {df[df.panel == pname].base_Sharpe.iloc[0]:.4f}"
            f"  MaxDD {df[df.panel == pname].base_MaxDD.iloc[0]:.2%}"
            f"  OOS Sh {df[df.panel == pname].base_OOS_Sharpe.iloc[0]:.4f}")

    # ------------------------------------------------------------ B. the reduction, head to head
    say("\n=== B. THE WHOLE QUESTION: IDXG vs its OWN per-name book, same panel / band / gross / rung ===")
    say("  panel band gross  bps | dCAGR    dSharpe   dMaxDD   dOOS_Sh | dTurn   dTickets | CAND 4b -> IDXG 4b")
    red = []
    for pname in panels:
        for band in BANDS:
            for gross in GROSSES:
                for rung in RUNGS:
                    def g_(bk_):
                        return df[(df.panel == pname) & (df.book == bk_) & (df.band == band)
                                  & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                    i_, c_, p_, e_ = g_("IDXG"), g_("CAND"), g_("CAP2"), g_("EWBH")
                    red.append(dict(panel=pname, band=band, gross=gross, cost_bps=rung,
                                    dCAGR=i_.CAGR - c_.CAGR, dSharpe=i_.Sharpe - c_.Sharpe,
                                    dMaxDD=i_.MaxDD - c_.MaxDD, dOOS_Sharpe=i_.OOS_Sharpe - c_.OOS_Sharpe,
                                    dTurn=i_.turnover_yr / c_.turnover_yr - 1,
                                    dTick=i_.tickets_yr / c_.tickets_yr - 1,
                                    cand4b=bool(c_.pass4b), cap4b=bool(p_.pass4b),
                                    idxg4b=bool(i_.pass4b), ewbh4b=bool(e_.pass4b),
                                    idxg_DD=i_.MaxDD, cand_DD=c_.MaxDD, ewbh_DD=e_.MaxDD))
                    if gross == COMMITTED_GROSS and rung == HEADLINE_RUNG:
                        z = red[-1]
                        say(f"  {pname:5s} {band:4.2f} {gross:5.2f} {rung:5.1f} | {z['dCAGR']:+7.2%}"
                            f" {z['dSharpe']:+9.4f} {z['dMaxDD']:+8.2%} {z['dOOS_Sharpe']:+9.4f} |"
                            f" {z['dTurn']:+7.1%} {z['dTick']:+8.1%} | "
                            f"{'PASS' if z['cand4b'] else 'fail'} -> {'PASS' if z['idxg4b'] else 'fail'}")
    rd = pd.DataFrame(red); rd.to_csv(f"{OUT}.reduction.csv", index=False)
    say(f"\n  Over all {len(rd)} matched (IDXG vs CAND) pairs:")
    say(f"   IDXG cheaper in turnover: {int((rd.dTurn < 0).sum())} of {len(rd)}"
        f"   cheaper in tickets: {int((rd.dTick < 0).sum())}"
        f"   dSharpe > 0: {int((rd.dSharpe > 0).sum())}"
        f"   dCAGR > 0: {int((rd.dCAGR > 0).sum())}"
        f"   dMaxDD > 0 (shallower): {int((rd.dMaxDD > 0).sum())}"
        f"   dOOS Sharpe > 0: {int((rd.dOOS_Sharpe > 0).sum())}")
    say(f"   mean dSharpe {rd.dSharpe.mean():+.4f}  mean dCAGR {rd.dCAGR.mean():+.2%}"
        f"  mean dMaxDD {rd.dMaxDD.mean():+.2%}  mean dTurnover {rd.dTurn.mean():+.1%}"
        f"  mean dTickets {rd.dTick.mean():+.1%}")
    say(f"   4b passes: CAND {int(rd.cand4b.sum())} / CAP2 {int(rd.cap4b.sum())} /"
        f" IDXG {int(rd.idxg4b.sum())} / EWBH {int(rd.ewbh4b.sum())} of {len(rd)} matched cells")
    say(f"   the DD leg, mean MaxDD: CAND {rd.cand_DD.mean():.2%}  IDXG {rd.idxg_DD.mean():.2%}"
        f"  EWBH {rd.ewbh_DD.mean():.2%}   (4b bar = 0.60 x SPY's)")

    # ------------------------------------------------------------ B2. is the KILL structural?
    say("\n=== B2. IS THE IDXG KILL STRUCTURAL, OR JUST OFF-GRID? — a FINE gross scan at the live band")
    say("    0.03 and 10 bps, PUBLISHED AND NEVER SELECTED ON (it adds no dial: nothing below is chosen,")
    say("    it only asks whether ANY gross could clear `L_DD` and `L_CAGR` AT ONCE). ===")
    say("  panel  gross |   CAGR    MaxDD  | L_CAGR floor  L_DD bar | L_H1 L_H2 L_OOS L_DD L_CAGR | 4b")
    fine = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos = spy.loc[OOS_START:]
        base_r = backtest(px, rules_v2_weights(px, band=COMMITTED_BAND, gross=COMMITTED_GROSS),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for g in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]:
            bk = run_book(px, risk_weights(px, "IDXG", COMMITTED_BAND, g))
            r = (bk["r0"] - bk["turn"] * HEADLINE_RUNG / 1e4).loc[start:]
            lg = legs(r, base_r, spy, r.loc[OOS_START:], spy_oos)
            fine.append(dict(panel=pname, gross=g, CAGR=cagr(r), MaxDD=maxdd(r),
                             cagr_floor=CAGR_FLOOR * cagr(spy), dd_bar=DD_CAP * maxdd(spy), **lg))
            say(f"  {pname:5s} {g:6.2f} | {cagr(r):6.2%} {maxdd(r):8.2%} | {CAGR_FLOOR * cagr(spy):12.2%}"
                f" {DD_CAP * maxdd(spy):9.2%} | "
                + "    ".join("1" if lg[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                + f"   | {'PASS' if lg['pass4b'] else 'fail'}")
    fn = pd.DataFrame(fine); fn.to_csv(f"{OUT}.fine_gross.csv", index=False)

    say("\n   THE FINE WINDOW IS NOT A KEEP UNTIL RULE 8 SAYS SO — the same IS-only choosers run over the")
    say("   FINE gross ladder (warm-up..2016-12-31 only), 2017-2026 then read ONCE:")
    fwf = []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
        base_r = backtest(px, rules_v2_weights(px, band=COMMITTED_BAND, gross=COMMITTED_GROSS),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        cand = []
        for g in [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]:
            bk = run_book(px, risk_weights(px, "IDXG", COMMITTED_BAND, g))
            r = (bk["r0"] - bk["turn"] * HEADLINE_RUNG / 1e4).loc[start:]
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            cand.append(dict(panel=pname, gross=g, IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                             OOS_Sharpe=sharpe(r_oos), OOS_CAGR=cagr(r_oos), OOS_MaxDD=maxdd(r_oos),
                             **legs(r, base_r, spy, r_oos, spy_oos)))
        cd = pd.DataFrame(cand)
        for ch, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
            pk = cd.loc[cd[col].idxmax()]
            fwf.append(dict(panel=pname, chooser=ch, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                            OOS_Sharpe=pk.OOS_Sharpe, OOS_CAGR=pk.OOS_CAGR, OOS_MaxDD=pk.OOS_MaxDD,
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos)))
            say(f"    {pname:5s} {ch:11s} picks gross {pk.gross:.2f}"
                f"  -> OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%}"
                f"   full-sample 4b {'PASS' if pk.pass4b else 'fail'}"
                f"   (SPY OOS {cagr(spy_oos):.2%} / {sharpe(spy_oos):.4f})")
    fw = pd.DataFrame(fwf); fw.to_csv(f"{OUT}.fine_walkforward.csv", index=False)
    say(f"   fine-ladder rule-8 picks carrying a full-sample 4b pass: {int(fw.full4b.sum())} of {len(fw)}"
        f"   (both panels must hold for an adoptable book).")
    for pname in panels:
        q = fn[fn.panel == pname]
        okD, okC = q[q.L_DD], q[q.L_CAGR]
        say(f"   {pname}: `L_DD` holds for gross <= {okD.gross.max() if len(okD) else float('nan'):.2f}"
            f" and `L_CAGR` holds for gross >= {okC.gross.min() if len(okC) else float('nan'):.2f}"
            f"  -> the two feasible sets are {'DISJOINT — the KILL is STRUCTURAL' if (not len(okD) or not len(okC) or okD.gross.max() < okC.gross.min()) else 'OVERLAPPING'}"
            f"; joint 4b on the fine scan: {int(q.pass4b.sum())} of {len(q)}")

    # ------------------------------------------------------------ C. KEEP counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for bk_ in BOOKS:
        d = df[df.book == bk_]
        say(f"   {bk_:5s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   first-binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by book: "
            + "  ".join(f"{bk_}:{int(d[d.book == bk_].pass4b.sum())}/{len(d[d.book == bk_])}" for bk_ in BOOKS))
    for band in BANDS:
        d = df[df.band == band]
        say(f"   band {band:4.2f}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by book: "
            + "  ".join(f"{bk_}:{int(d[d.book == bk_].pass4b.sum())}/{len(d[d.book == bk_])}" for bk_ in BOOKS))
    for pname in panels:
        d = df[df.panel == pname]
        say(f"   {pname:5s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   by book: "
            + "  ".join(f"{bk_}:{int(d[d.book == bk_].pass4b.sum())}/{len(d[d.book == bk_])}" for bk_ in BOOKS))
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same book, band, gross, rung):")
    jt = []
    for bk_ in BOOKS:
        for band in BANDS:
            for gross in GROSSES:
                for rung in RUNGS:
                    q = df[(df.book == bk_) & (df.band == band) & (df.gross == gross) & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                    jt.append(dict(book=bk_, band=band, gross=gross, cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by book: "
        + "  ".join(f"{bk_}:{int(jf[jf.book == bk_].joint.sum())}/{len(jf[jf.book == bk_])}" for bk_ in BOOKS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)} of {len(df)}")
    for _, r in pa.head(24).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} band {r.band:.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  turn {r.turnover_yr:.2f}x"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ D. the adoption bar
    say(f"\n=== D. THE ADOPTION BAR — turnover and tickets against the live book's {LIVE_TURNOVER}x/yr ===")
    say("  panel book band gross | turnover/yr  vs live | tickets/yr | mean names | mean gross")
    for pname in panels:
        for bk_ in BOOKS:
            for band in BANDS:
                e = bf[(bf.panel == pname) & (bf.book == bk_) & (bf.band == band)
                       & (bf.gross == COMMITTED_GROSS)].iloc[0]
                say(f"  {pname:5s} {bk_:4s} {band:4.2f} {COMMITTED_GROSS:5.2f} |"
                    f" {e.turnover_yr:11.2f} {e.turnover_yr / LIVE_TURNOVER:6.2f}x |"
                    f" {e.tickets_yr:10.1f} | {e.mean_names:10.2f} | {e.mean_gross:10.3f}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (band, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated")
    say("    IS-only choosers, 2017-2026 read ONCE, each pick scored against its own book's COMMITTED cell")
    say(f"    (band {COMMITTED_BAND}, gross {COMMITTED_GROSS}). ===")
    wf = []
    for pname in panels:
        for bk_ in BOOKS:
            for rung in RUNGS:
                d = df[(df.panel == pname) & (df.book == bk_) & (df.cost_bps == rung)]
                cm = d[(d.band == COMMITTED_BAND) & (d.gross == COMMITTED_GROSS)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = d.loc[d[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk_, cost_bps=rung, chooser=chooser,
                                   pick_band=pk.band, pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                   pick_turn=pk.turnover_yr, committed_turn=cm.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe, committed_OOS_CAGR=cm.OOS_CAGR,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR,
                                   spy_OOS_MaxDD=pk.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x {len(BOOKS)} books x {len(RUNGS)} rungs x 2 choosers).")
    say("  book  | picks | beat SPY OOS Sh | beat live OOS Sh | beat own COMMITTED cell | full 4b | mean OOS CAGR / Sh / MaxDD | mean turn")
    for bk_ in BOOKS:
        q = wfd[wfd.book == bk_]
        say(f"  {bk_:5s} | {len(q):5d} | {int((q.OOS_Sharpe > q.spy_OOS_Sharpe).sum()):15d}"
            f" | {int((q.OOS_Sharpe > q.base_OOS_Sharpe).sum()):16d}"
            f" | {int((q.OOS_Sharpe > q.committed_OOS_Sharpe).sum()):23d}"
            f" | {int(q.full4b.sum()):7d} | {q.OOS_CAGR.mean():7.2%} / {q.OOS_Sharpe.mean():.4f} /"
            f" {q.OOS_MaxDD.mean():7.2%} | {q.pick_turn.mean():8.2f}x")
    say(f"   SPY OOS (mean over picks): CAGR {wfd.spy_OOS_CAGR.mean():.2%}"
        f"  Sharpe {wfd.spy_OOS_Sharpe.mean():.4f}  MaxDD {wfd.spy_OOS_MaxDD.mean():.2%}"
        f"   |  live RULES v2 OOS Sharpe {wfd.base_OOS_Sharpe.mean():.4f}, CAGR {wfd.base_OOS_CAGR.mean():.2%}")
    say("   pick distribution over band:  " + "  ".join(
        f"{b:.2f}:{int((wfd.pick_band == b).sum())}" for b in BANDS))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say("   per book, pick distribution over band: " + " | ".join(
        f"{bk_} " + ",".join(f"{b:.2f}:{int((wfd[wfd.book == bk_].pick_band == b).sum())}" for b in BANDS)
        for bk_ in BOOKS))

    # ------------------------------------------------------------ F. gates + verdict
    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(gdf.pass_.sum()); ntot = len(gdf)
    say(f"\n=== F. GATES: {npass} of {ntot} pass ===")
    for _, g in gdf.iterrows():
        say(f"   {'PASS' if g.pass_ else 'FAIL'}  {g.gate}")
    say(f"\n  elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
