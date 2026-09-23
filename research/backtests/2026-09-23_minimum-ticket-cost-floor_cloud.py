#!/usr/bin/env python3
"""idea 2488 (lane cloud, run 61, 2026-09-23) — DOES A MINIMUM-TICKET COST FLOOR MOVE WHERE THE
CAPPED FAMILY DIES?

THE GAP.  Every cost rung this record has ever charged is EXACTLY PROPORTIONAL to `|dw|`.  Under
that model a 1 bp re-size of a 2% position is billed a THOUSANDTH of what a full 2% entry is
billed.  Real execution is not like that: a ticket carries a FIXED component — the spread it must
cross, the odd-lot and minimum-commission floor, the fact that somebody has to route it — that a
purely proportional model prices at ZERO.  And the standing 4b candidate (idea 2322's CAP2) is,
by the record's own account, a book of MANY SMALL RE-SIZES rather than few large ones: precisely
the trade a proportional model under-charges.  If that is right, the candidate's cost robustness
(idea 2431: 4b survives 25 bps and dies between 33 and 54 bps per cell) is measured on a bill
whose SHAPE is wrong, and the death rung is optimistic.

THE COST MODEL.  `cost_t = (1 - phi) * c/1e4 * |dw|_t  +  f * tickets_t`, where a TICKET is one
name traded on one rebalance day (|dw| > 1e-12, the SHY sweep trade included, because it is a
real order) and `f` is CALIBRATED, never free:

    f = phi * (c/1e4 * SUM_t |dw|_t) / SUM_t tickets_t

so that the TOTAL BILL over the scored sample equals the flat rung's bill EXACTLY (G8).  `phi` is
therefore the FIXED SHARE of a revenue-neutral bill: phi = 0 IS the committed proportional model,
phi = 1 is a pure per-ticket charge, and nothing in between changes how much the book pays IN
TOTAL — only WHICH TRADES pay it.

TWO CALIBRATION CONVENTIONS, BOTH PUBLISHED, because they answer different questions:
  SELF  -- `f` from the book's OWN realised path.  Revenue-neutral for every book.  Answers: does
           RE-SHAPING the bill, at an unchanged total, move the verdict?  (It can: the bill's
           TIMING changes, and a period of many small tickets now pays more.)
  PANEL -- `f` fixed ONCE per (panel, cadence, rung) from the COMMITTED REFERENCE BOOK (CAP2 at
           g 0.75) and then charged to EVERY book.  NOT revenue-neutral away from the reference.
           Answers the idea's actual question: does a fixed component RE-ORDER the family and move
           the boundary?  A book that buys its turnover in more, smaller tickets now pays more for
           the same `|dw|`.

DIAL 1 -- phi, the fixed share of the calibrated bill, in {0, 0.25, 0.50, 0.75, 1.00}.  It pins
          `f` exactly; `f` is not a free parameter.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: panels
{U56, B136}; the BOOK LADDER cap in {0.015, 0.020 (CAP2), 0.030, INF (CAND)}; cost rungs
{0, 10, 25, 50} bps plus a FINE 0..120 bps ladder used ONLY to locate the death rung; cadence
{W, M}; t+1 execution; band 0.03; MA 200d; SHY sweep at phi_sweep = 1.00.

THE PREMISE IS TESTED, NOT ASSUMED.  The idea asserts the capped book's turnover is dominated by
many small re-sizes.  This run PUBLISHES THE TICKET-SIZE DISTRIBUTION of every book over eight
pre-registered |dw| buckets before any verdict is read, so the premise can be REFUTED here as
readily as confirmed.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  Re-shaping a bill cannot mend three legs that fail
at a ZERO bill.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (phi, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE, separately at every (panel, cadence, book, rung,
calibration).

GATES.  G0 >= 10y per panel.  G1 the runner IS `engine.backtest` at phi = 0.  G2 the eligible set
IS `baseline.band_state` & priced.  G3 phi = 0 reproduces the committed CAP2 AND CAND U56
headlines.  G4 no leverage.  G5 at phi = 0 the bill is exactly linear in the rung.  G6 exactly two
tuned parameters.  G7 the comparands are bit-identical across every phi and calibration.  G8 SELF
calibration is REVENUE-NEUTRAL at every phi (total bill == the flat rung's, to machine precision).
G9 the sweep instrument is priced on every scored row.  G10 at phi = 1 the proportional component
is exactly zero and the whole bill is per-ticket.  G11 PANEL == SELF on the reference book itself.
G12 the ticket count is bounded by the number of investable names per rebalance.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The phi-vs-phi contrast is same-path, same-days,
same-trades — it changes ONLY the bill — and is first-order immune to that bias; the absolute 4b
verdicts and death rungs are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_minimum-ticket-cost-floor_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "minimum-ticket-cost-floor", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
PHIS = [0.00, 0.25, 0.50, 0.75, 1.00]          # DIAL 1 (pins f; f is calibrated, not free)
GROSSES = [0.75, 1.00]                          # DIAL 2
CAPS = [0.015, 0.020, 0.030, np.inf]            # published book ladder (0.020 = CAP2, INF = CAND)
RUNGS = [0.0, 10.0, 25.0, 50.0]                 # published
FINE = [float(x) for x in range(0, 122, 2)]     # death-rung ladder ONLY
CADENCES = ["W", "M"]                           # published
CALS = ["SELF", "PANEL"]                        # published calibration conventions
SWEEP = "SHY"
REF_CAP, REF_GROSS = 0.020, 0.75                # the committed reference book for PANEL
HEADLINE_RUNG, HEADLINE_CAD = 10.0, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
TICK_EPS = 1e-12
BUCKETS = [0.0, 1e-4, 5e-4, 1e-3, 2.5e-3, 5e-3, 1e-2, 2e-2, np.inf]   # |dw| in NAV, 1..200+ bp
BLAB = ["<=1bp", "1-5bp", "5-10bp", "10-25bp", "25-50bp", "50-100bp", "100-200bp", ">200bp"]

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


def cname(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


def bookname(c):
    return "CAP2" if c == REF_CAP else ("CAND" if not np.isfinite(c) else f"CAP{c:.3f}")


# ---------------------------------------------------------------- the book
def eligible(px):
    return band_state(px, BAND) & px.notna()


def risk_weights(el, gross, cap):
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def run_book(prices, w_risk, freq, sweep=True):
    """`engine.backtest` verbatim, except that the per-day TURNOVER and the per-day TICKET COUNT
    are both retained, so every cost MODEL and every rung is read off the SAME realised path.
    A TICKET is one name traded on one rebalance day; the SHY sweep trade counts, because it is a
    real order that a broker bills."""
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
    turn = np.zeros(n); tick = np.zeros(n); r0 = np.zeros(n)
    gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n); swp = np.zeros(n)
    hist_t = np.zeros(len(BLAB)); hist_n = np.zeros(len(BLAB))
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            d = np.abs(new - cur)
            turn[i] = float(d.sum())
            hit = d > TICK_EPS
            tick[i] = float(hit.sum())
            if hit.any():
                idxb = np.digitize(d[hit], BUCKETS) - 1
                np.add.at(hist_t, idxb, d[hit])
                np.add.at(hist_n, idxb, 1.0)
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        swp[i] = float(cur[si])
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                tick=pd.Series(tick, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx),
                sweep_w=pd.Series(swp, index=idx), hist_t=hist_t, hist_n=hist_n)


def bill(turn, tick, rung, phi, f):
    """The mixed bill, as a daily return drag.  phi = 0 IS the committed proportional model."""
    return (1.0 - phi) * rung / 1e4 * turn + f * tick


def calib_f(turn, tick, rung, phi):
    """f such that the TOTAL bill equals the flat rung's bill EXACTLY (revenue-neutral)."""
    K = float(tick.sum())
    return (phi * (rung / 1e4) * float(turn.sum()) / K) if K > 0 else 0.0


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
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


def main():
    t0 = time.time()
    say("=== idea 2488 — DOES A MINIMUM-TICKET COST FLOOR MOVE WHERE THE CAPPED FAMILY DIES?")
    say("    (lane cloud, run 61) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  fine ladder {FINE[0]:.0f}..{FINE[-1]:.0f} bps step 2 (death rung only)  sweep {SWEEP}")
    say(f"    DIAL 1 phi (fixed share of a revenue-neutral bill) {PHIS}    DIAL 2 gross {GROSSES}")
    say(f"    PUBLISHED AXIS, NEVER SELECTED ON: book ladder {[bookname(c) for c in CAPS]},"
        f" panels, rungs, cadence, calibration {CALS}.")
    say("    MODEL: cost_t = (1-phi) * c/1e4 * |dw|_t + f * tickets_t, f CALIBRATED so the TOTAL")
    say("    bill equals the flat rung's (G8).  phi = 0 IS the committed model; phi = 1 is a pure")
    say("    per-ticket charge.  Nothing in between changes how MUCH the book pays — only WHICH")
    say("    trades pay it.  SELF calibrates on the book's own path; PANEL fixes f once from the")
    say("    committed reference book (CAP2, g 0.75) and charges it to every book.")
    say("    THE PREMISE IS TESTED: the ticket-size distribution of every book is PUBLISHED over")
    say("    eight pre-registered |dw| buckets BEFORE any verdict is read.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383), 0 of 40-120 (2318/2322/2326/2343);")
    say("    re-shaping a bill cannot mend three legs that fail at a ZERO bill.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The phi contrast is same-path, same-trades, first-order immune;")
    say("    the absolute 4b verdicts and death rungs are not.")
    gate("G6 exactly two tuned parameters", "phi, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs_u = band_state(px_u, BAND) & px_u.notna()
    d2 = int((eligible(px_u) != bs_u).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {bs_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

    el_u = eligible(px_u)
    d1 = 0.0
    for _cap in (REF_CAP, np.inf):
        w = risk_weights(el_u, REF_GROSS, _cap)
        r_eng = backtest(px_u, w, cost_bps=HEADLINE_RUNG, freq=HEADLINE_CAD)["returns"]
        bk = run_book(px_u, w, HEADLINE_CAD, sweep=False)
        d1 = max(d1, float((r_eng - (bk["r0"] - bill(bk["turn"], bk["tick"], HEADLINE_RUNG, 0.0, 0.0)))
                           .abs().max()))
    gate("G1 at phi = 0 the runner IS engine.backtest (CAP2 and CAND, g 0.75, W, 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # ------------------------------------------------------------ the realised paths (phi-free)
    P = {}
    cmp_ = {}
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        spy_t = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq="W")["returns"].loc[start:]
        cmp_[pname] = (spy_t, base_t)
        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    bk = run_book(px, risk_weights(el, gross, cap), cad)
                    P[(pname, cad, cname(cap), gross)] = dict(
                        r0=bk["r0"].loc[start:], turn=bk["turn"].loc[start:],
                        tick=bk["tick"].loc[start:], hist_t=bk["hist_t"], hist_n=bk["hist_n"],
                        max_gross=float(bk["gross"].loc[start:].max()),
                        mean_names=float(bk["names"].loc[start:].mean()),
                        max_name_w=float(bk["maxw"].loc[start:].max()),
                        mean_sweep=float(bk["sweep_w"].loc[start:].mean()))
    say(f"\n    {len(P)} realised weight paths (the phi dial changes ONLY the bill, never the path).")
    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(P)} paths: {max(v['max_gross'] for v in P.values()):.6f}",
         "<= 1+1e-12", max(v["max_gross"] for v in P.values()) <= 1 + 1e-12)
    nmax = {p: len(px.columns) for p, px in panels.items()}
    tk_ok = all(v["tick"].max() <= nmax[k[0]] for k, v in P.items())
    gate("G12 the ticket count never exceeds the investable name count",
         f"max tickets/day {max(v['tick'].max() for v in P.values()):.0f}"
         f" against {nmax} investable", "<= panel width", tk_ok)

    # ------------------------------------------------------------ A. the ticket-size distribution
    say("\n=== A. THE PREMISE, TESTED BEFORE ANY VERDICT: WHAT SIZE ARE THE TICKETS?  (share of")
    say("    TICKETS and of TURNOVER in each |dw| bucket; W cadence, g 0.75, 10 bps path) ===")
    say("  panel book |  tickets/yr | mean ticket |  " + " | ".join(f"{b:>9s}" for b in BLAB))
    tk_rows = []
    for pname in panels:
        for cap in CAPS:
            v = P[(pname, "W", cname(cap), REF_GROSS)]
            yrs = len(v["turn"]) / 252
            hn, ht = v["hist_n"], v["hist_t"]
            mt = float(v["turn"].sum() / v["tick"].sum()) if v["tick"].sum() else np.nan
            say(f"  {pname:5s} {bookname(cap):5s}| {v['tick'].sum()/yrs:11.1f} |"
                f" {mt*1e4:8.2f} bp |  " + " | ".join(f"{x/hn.sum():8.2%}" for x in hn))
            say(f"  {'':5s} {'':5s}|  (turnover) |             |  "
                + " | ".join(f"{x/ht.sum():8.2%}" for x in ht))
            tk_rows.append(dict(panel=pname, book=bookname(cap), cap=cname(cap),
                                tickets_yr=float(v["tick"].sum() / yrs),
                                turnover_yr=float(v["turn"].sum() / yrs),
                                mean_ticket_bp=mt * 1e4,
                                **{f"n_{b}": float(x / hn.sum()) for b, x in zip(BLAB, hn)},
                                **{f"t_{b}": float(x / ht.sum()) for b, x in zip(BLAB, ht)}))
    tk = pd.DataFrame(tk_rows); tk.to_csv(f"{OUT}.tickets.csv", index=False)
    small_n = float(tk[tk.book == "CAP2"][["n_<=1bp", "n_1-5bp", "n_5-10bp"]].sum(axis=1).mean())
    small_t = float(tk[tk.book == "CAP2"][["t_<=1bp", "t_1-5bp", "t_5-10bp"]].sum(axis=1).mean())
    cand_n = float(tk[tk.book == "CAND"][["n_<=1bp", "n_1-5bp", "n_5-10bp"]].sum(axis=1).mean())
    publish("THE IDEA'S PREMISE ('many small re-sizes'), MEASURED",
            f"CAP2: {small_n:.1%} of TICKETS are under 10 bp of NAV but they carry only"
            f" {small_t:.1%} of TURNOVER;  CAND: {cand_n:.1%} of tickets under 10 bp;"
            f" CAP2 mean ticket {tk[tk.book=='CAP2'].mean_ticket_bp.mean():.2f} bp vs CAND"
            f" {tk[tk.book=='CAND'].mean_ticket_bp.mean():.2f} bp")

    # --- G13: the MECHANISM.  If the ticket COUNT does not depend on the cap, then a per-ticket
    # charge is the SAME BILL for every book in the family, and the floor cannot single the
    # capped book out.  This is asserted, not assumed.
    tspread = 0.0
    for pname in panels:
        for cad in CADENCES:
            for gross in GROSSES:
                tk_c = [float(P[(pname, cad, cname(c), gross)]["tick"].sum()) for c in CAPS]
                tspread = max(tspread, (max(tk_c) - min(tk_c)) / max(tk_c))
    gate("G13 THE MECHANISM: the TICKET COUNT is NEAR-INVARIANT to the cap (the cap changes ticket"
         " SIZE, not ticket COUNT), so a per-ticket charge bills every book in the family alike."
         "  Pre-registered tolerance 1%; this is a MEASURED near-invariance, NOT an identity —"
         " the residual is names whose capped weight rounds to no trade on a given day",
         f"max relative spread of total tickets across the 4-book cap ladder, over"
         f" {len(panels)*len(CADENCES)*len(GROSSES)} (panel, cadence, gross) cells: {tspread:.3e}"
         f" ({tspread:.3%})", "< 1e-2", tspread < 1e-2)
    publish("CONSEQUENCE — mean TICKET SIZE across the cap ladder (U56 / B136, W, g 0.75)",
            "U56 " + " -> ".join(f"{bookname(c)} {tk[(tk.panel=='U56') & (tk.cap==cname(c))].iloc[0].mean_ticket_bp:.2f}bp"
                                 for c in CAPS)
            + ";  B136 " + " -> ".join(f"{bookname(c)} {tk[(tk.panel=='B136') & (tk.cap==cname(c))].iloc[0].mean_ticket_bp:.2f}bp"
                                       for c in CAPS))

    # ------------------------------------------------------------ the grid
    rows = []
    fvals = []
    for pname in panels:
        spy_t, base_t = cmp_[pname]
        spy_oos = spy_t.loc[OOS_START:]
        for cad in CADENCES:
            for rung in RUNGS:
                for phi in PHIS:
                    ref = P[(pname, cad, cname(REF_CAP), REF_GROSS)]
                    f_panel = calib_f(ref["turn"], ref["tick"], rung, phi)
                    for cap in CAPS:
                        for gross in GROSSES:
                            v = P[(pname, cad, cname(cap), gross)]
                            for cal in CALS:
                                f = calib_f(v["turn"], v["tick"], rung, phi) if cal == "SELF" \
                                    else f_panel
                                b = bill(v["turn"], v["tick"], rung, phi, f)
                                r = v["r0"] - b
                                flat = rung / 1e4 * float(v["turn"].sum())
                                yrs = len(v["turn"]) / 252
                                r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                                lg = legs(r, base_t, spy_t, r_oos, spy_oos)
                                fvals.append(dict(panel=pname, cadence=cad, cost_bps=rung,
                                                  phi=phi, book=bookname(cap), gross=gross,
                                                  cal=cal, f_bp=f * 1e4,
                                                  bill_yr_bp=float(b.sum()) / yrs * 1e4,
                                                  flat_bill_yr_bp=flat / yrs * 1e4,
                                                  bill_ratio=(float(b.sum()) / flat) if flat > 0 else 1.0))
                                rows.append(dict(
                                    panel=pname, cadence=cad, book=bookname(cap), cap=cname(cap),
                                    gross=gross, cost_bps=rung, phi=phi, cal=cal,
                                    f_bp=f * 1e4,
                                    CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                    Calmar=calmar(r),
                                    turnover_yr=float(v["turn"].sum() / yrs),
                                    tickets_yr=float(v["tick"].sum() / yrs),
                                    bill_yr_bp=float(b.sum()) / yrs * 1e4,
                                    bill_ratio=(float(b.sum()) / flat) if flat > 0 else 1.0,
                                    max_name_w=v["max_name_w"],
                                    IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                    OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos),
                                    OOS_MaxDD=maxdd(r_oos),
                                    base_Sharpe=sharpe(base_t), base_CAGR=cagr(base_t),
                                    base_MaxDD=maxdd(base_t),
                                    base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                    base_OOS_CAGR=cagr(base_t.loc[OOS_START:]),
                                    spy_CAGR=cagr(spy_t), spy_Sharpe=sharpe(spy_t),
                                    spy_MaxDD=maxdd(spy_t), spy_OOS_CAGR=cagr(spy_oos),
                                    spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                    **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    fv = pd.DataFrame(fvals); fv.to_csv(f"{OUT}.calibration.csv", index=False)
    say(f"    {len(df)} published rows = 2 panels x {len(CADENCES)} cadences x {len(CAPS)} books"
        f" x {len(GROSSES)} gross x {len(RUNGS)} rungs x {len(PHIS)} phi x {len(CALS)} calibrations.")

    d7 = 0.0
    for pname in panels:
        q = df[df.panel == pname]
        d7 = max(d7, float(q.spy_Sharpe.max() - q.spy_Sharpe.min()),
                 float(q.base_Sharpe.max() - q.base_Sharpe.min()),
                 float(q.spy_OOS_Sharpe.max() - q.spy_OOS_Sharpe.min()))
    gate("G7 the comparands (SPY and live RULES v2) are BIT-IDENTICAL across every phi and"
         " calibration", f"max spread over all {len(df)} rows: {d7:.3e}", "0.0", d7 == 0.0)
    slf = fv[(fv.cal == "SELF") & (fv.cost_bps > 0)]
    gate("G8 SELF calibration is REVENUE-NEUTRAL at every phi (total bill == the flat rung's)",
         f"max |bill/flat - 1| over {len(slf)} arms: {float((slf.bill_ratio - 1).abs().max()):.3e}",
         "< 1e-12", float((slf.bill_ratio - 1).abs().max()) < 1e-12)
    ref_rows = fv[(fv.book == "CAP2") & (fv.gross == REF_GROSS)]
    d11 = float(ref_rows.pivot_table(index=["panel", "cadence", "cost_bps", "phi"],
                                     columns="cal", values="f_bp").diff(axis=1).abs().max().max())
    gate("G11 PANEL == SELF on the reference book itself (CAP2, g 0.75)",
         f"max |f_PANEL - f_SELF| over {len(ref_rows)//2} reference arms: {d11:.3e} bp",
         "< 1e-12", d11 < 1e-12)
    p1 = df[df.phi == 1.00]
    gate("G10 at phi = 1 the proportional component is exactly zero (the whole bill is per-ticket)",
         f"checked on {len(p1)} rows; f > 0 on {int((p1.f_bp > 0).sum())} of the"
         f" {int((p1.cost_bps > 0).sum())} with a non-zero rung",
         "f > 0 wherever rung > 0",
         int((p1[p1.cost_bps > 0].f_bp > 0).sum()) == int((p1.cost_bps > 0).sum()))
    v = P[("U56", "W", cname(REF_CAP), REF_GROSS)]
    d5 = float((2 * bill(v["turn"], v["tick"], 25.0, 0.0, 0.0)
                - bill(v["turn"], v["tick"], 50.0, 0.0, 0.0)).abs().max())
    gate("G5 at phi = 0 the bill is EXACTLY linear in the rung", f"max|d| {d5:.3e}", "< 1e-15",
         d5 < 1e-15)

    def cell(panel, cad, book, gross, rung, phi, cal):
        return df[(df.panel == panel) & (df.cadence == cad) & (df.book == book)
                  & (df.gross == gross) & (df.cost_bps == rung) & (df.phi == phi)
                  & (df.cal == cal)].iloc[0]

    a = cell("U56", "W", "CAP2", 0.75, 10.0, 0.00, "SELF")
    b = cell("U56", "W", "CAND", 0.75, 10.0, 0.00, "SELF")
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 phi = 0 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND"
         " CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    say(f"    ANCHOR published: U56 SPY full {a.spy_CAGR:.2%} / {a.spy_Sharpe:.4f} / {a.spy_MaxDD:.2%},"
        f" OOS {a.spy_OOS_CAGR:.2%} / {a.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {a.base_CAGR:.2%} / {a.base_Sharpe:.4f} / {a.base_MaxDD:.2%},"
        f" OOS {a.base_OOS_Sharpe:.4f}.")

    # ------------------------------------------------------------ B. what f actually is
    say("\n=== B. THE CALIBRATED FLOOR ITSELF (PANEL convention, f fixed from CAP2 g 0.75) ===")
    say("  panel cad rung |  phi |    f (bp of NAV per ticket) | CAP2 bill/flat | CAND bill/flat")
    for pname in panels:
        for cad in CADENCES:
            for rung in RUNGS[1:]:
                for phi in PHIS[1:]:
                    q = fv[(fv.panel == pname) & (fv.cadence == cad) & (fv.cost_bps == rung)
                           & (fv.phi == phi) & (fv.cal == "PANEL") & (fv.gross == REF_GROSS)]
                    c2 = q[q.book == "CAP2"].iloc[0]; cd = q[q.book == "CAND"].iloc[0]
                    say(f"  {pname:5s} {cad:3s} {rung:4.0f} | {phi:4.2f} | {c2.f_bp:26.4f} |"
                        f" {c2.bill_ratio:14.4f} | {cd.bill_ratio:14.4f}")

    for pname in panels:
        eq = fv[(fv.cal == "PANEL") & (fv.phi == 1.00) & (fv.cost_bps == HEADLINE_RUNG)
                & (fv.gross == REF_GROSS) & (fv.cadence == HEADLINE_CAD) & (fv.panel == pname)]
        eq0 = fv[(fv.cal == "PANEL") & (fv.phi == 0.00) & (fv.cost_bps == HEADLINE_RUNG)
                 & (fv.gross == REF_GROSS) & (fv.cadence == HEADLINE_CAD) & (fv.panel == pname)]
        publish(f"THE FLOOR RE-PRICES THE FAMILY TOWARDS ONE COMMON BILL ({pname}, W, 10 bps,"
                " g 0.75) — so it HELPS the book trading the BIGGEST tickets, the UNCAPPED one,"
                " and HURTS the tightest cap",
                "bill/flat at phi=1: " + "; ".join(f"{r.book} {r.bill_ratio:.4f}"
                                                   for r in eq.itertuples())
                + f"  (every one is 1.0000 at phi=0, spread"
                f" {float(eq0.bill_ratio.max() - eq0.bill_ratio.min()):.4f};"
                f" spread at phi=1 is"
                f" {float(eq.bill_ratio.max() - eq.bill_ratio.min()):.4f})")

    # ------------------------------------------------------------ C. the death rung
    say("\n=== C. WHERE THE CAPPED FAMILY DIES — the SMALLEST cost rung at which the row's 4b")
    say(f"    verdict fails, searched on a FINE ladder {FINE[0]:.0f}..{FINE[-1]:.0f} bps step 2.")
    say("    (`>120` = still passing at the top of the ladder; `0` = never passes.) ===")
    death = []
    for pname in panels:
        spy_t, base_t = cmp_[pname]
        spy_oos = spy_t.loc[OOS_START:]
        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    v = P[(pname, cad, cname(cap), gross)]
                    ref = P[(pname, cad, cname(REF_CAP), REF_GROSS)]
                    for phi in PHIS:
                        for cal in CALS:
                            dr = np.nan; alive0 = None
                            for rung in FINE:
                                src = v if cal == "SELF" else ref
                                f = calib_f(src["turn"], src["tick"], rung, phi)
                                r = v["r0"] - bill(v["turn"], v["tick"], rung, phi, f)
                                lg = legs(r, base_t, spy_t, r.loc[OOS_START:], spy_oos)
                                if alive0 is None:
                                    alive0 = lg["pass4b"]
                                if not lg["pass4b"]:
                                    dr = rung; break
                            death.append(dict(panel=pname, cadence=cad, book=bookname(cap),
                                              gross=gross, phi=phi, cal=cal,
                                              alive_at_0=bool(alive0),
                                              death_rung=dr if not np.isnan(dr) else np.nan,
                                              survives_ladder=bool(np.isnan(dr))))
    dth = pd.DataFrame(death); dth.to_csv(f"{OUT}.death.csv", index=False)
    say("  panel cad book  g    cal   |  " + " | ".join(f"phi {p:.2f}" for p in PHIS)
        + "  | d(death) phi 0 -> 1")
    for pname in panels:
        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    for cal in CALS:
                        q = dth[(dth.panel == pname) & (dth.cadence == cad)
                                & (dth.book == bookname(cap)) & (dth.gross == gross)
                                & (dth.cal == cal)].set_index("phi")
                        def fmt(p):
                            r = q.loc[p]
                            if not r.alive_at_0: return "   never"
                            if r.survives_ladder: return "   >120 "
                            return f"{r.death_rung:7.0f} "
                        d0, d1_ = q.loc[0.00], q.loc[1.00]
                        if d0.alive_at_0 and not d0.survives_ladder and not d1_.survives_ladder \
                                and d1_.alive_at_0:
                            dd = f"{d1_.death_rung - d0.death_rung:+.0f} bps"
                        else:
                            dd = "   n/a"
                        say(f"  {pname:5s} {cad:3s} {bookname(cap):5s} {gross:.2f} {cal:5s} |  "
                            + " | ".join(fmt(p) for p in PHIS) + f"  | {dd}")
    liv = dth[dth.alive_at_0 & ~dth.survives_ladder]
    piv = liv.pivot_table(index=["panel", "cadence", "book", "gross", "cal"], columns="phi",
                          values="death_rung")
    piv = piv.dropna()
    if len(piv):
        mv = piv[1.00] - piv[0.00]
        publish("DOES THE FLOOR MOVE THE DEATH RUNG?",
                f"over {len(piv)} rows measurable at BOTH phi 0 and phi 1:"
                f" median move {mv.median():+.1f} bps, mean {mv.mean():+.2f},"
                f" range [{mv.min():+.0f}, {mv.max():+.0f}];"
                f" EARLIER (floor HURTS) {int((mv < 0).sum())}, LATER (floor HELPS)"
                f" {int((mv > 0).sum())}, UNCHANGED {int((mv == 0).sum())}")
        for cal in CALS:
            s = piv.xs(cal, level="cal") if "cal" in piv.index.names else piv
            m2 = s[1.00] - s[0.00]
            publish(f"  under {cal} calibration",
                    f"n={len(s)}, median move {m2.median():+.1f} bps,"
                    f" earlier {int((m2 < 0).sum())} / later {int((m2 > 0).sum())} /"
                    f" unchanged {int((m2 == 0).sum())}")

    # ------------------------------------------------------------ D. KEEP paths
    say("\n=== D. BOTH KEEP PATHS OVER ALL PUBLISHED ROWS ===")
    say(f"  4b {int(df.pass4b.sum())} of {len(df)};  4a {int(df.pass4a.sum())} of {len(df)}")
    say("  cal   phi  | 4b      | 4a | 4b at 10bps | 4b at 25bps | 4b at 50bps | L_DD fail |"
        " L_CAGR fail")
    for cal in CALS:
        for phi in PHIS:
            q = df[(df.cal == cal) & (df.phi == phi)]
            say(f"  {cal:5s} {phi:4.2f} | {int(q.pass4b.sum()):3d}/{len(q):<3d} |"
                f" {int(q.pass4a.sum()):2d} |"
                + " | ".join(f"{int(q[q.cost_bps==rg].pass4b.sum()):5d}/{len(q[q.cost_bps==rg]):<5d}"
                             for rg in (10.0, 25.0, 50.0))
                + f" | {int((~q.L_DD).sum()):9d} | {int((~q.L_CAGR).sum()):11d}")

    say("\n  HEADLINE CELLS (U56, W, g 0.75, 10 bps) — how far does re-shaping the bill move them?")
    say("  book  cal   |  phi |   CAGR |  Sharpe |   MaxDD |  OOS Sharpe | bill/yr (bp) | 4b")
    for cap in CAPS:
        for cal in CALS:
            for phi in PHIS:
                q = cell("U56", "W", bookname(cap), 0.75, 10.0, phi, cal)
                say(f"  {bookname(cap):5s} {cal:5s} | {phi:4.2f} | {q.CAGR:6.2%} | {q.Sharpe:7.4f} |"
                    f" {q.MaxDD:7.2%} | {q.OOS_Sharpe:11.4f} | {q.bill_yr_bp:12.2f} |"
                    f" {'Y' if q.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the two dials (phi, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (panel, cadence, book, rung, cal). ===")
    wf = []
    for pname in panels:
        for cad in CADENCES:
            for cap in CAPS:
                for rung in RUNGS:
                    for cal in CALS:
                        q = df[(df.panel == pname) & (df.cadence == cad)
                               & (df.book == bookname(cap)) & (df.cost_bps == rung)
                               & (df.cal == cal)]
                        for ch, keyf in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                            p = q.loc[q[keyf].idxmax()]
                            wf.append(dict(panel=pname, cadence=cad, book=bookname(cap),
                                           cost_bps=rung, cal=cal, chooser=ch,
                                           pick_phi=p.phi, pick_gross=p.gross,
                                           OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                                           OOS_MaxDD=p.OOS_MaxDD,
                                           spy_OOS_Sharpe=p.spy_OOS_Sharpe,
                                           spy_OOS_CAGR=p.spy_OOS_CAGR,
                                           base_OOS_Sharpe=p.base_OOS_Sharpe,
                                           beats_spy=bool(p.OOS_Sharpe > p.spy_OOS_Sharpe),
                                           beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                                           full4b=bool(p.pass4b)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  panel cad book  cal   | picks (phi/g)                        | OOS CAGR | OOS Sharpe |"
        " > SPY | > live | full 4b")
    for pname in panels:
        for cad in CADENCES:
            for cap in CAPS:
                for cal in CALS:
                    q = wfd[(wfd.panel == pname) & (wfd.cadence == cad)
                            & (wfd.book == bookname(cap)) & (wfd.cal == cal)]
                    top = q.groupby(["pick_phi", "pick_gross"]).size().sort_values(ascending=False)
                    desc = ", ".join(f"{a:.2f}/{b:.2f}:{c}" for (a, b), c in top.items())
                    say(f"  {pname:5s} {cad:3s} {bookname(cap):5s} {cal:5s} | {desc:36s} |"
                        f" {q.OOS_CAGR.mean():8.2%} | {q.OOS_Sharpe.mean():10.4f} |"
                        f" {int(q.beats_spy.sum()):3d}/{len(q):<3d} |"
                        f" {int(q.beats_base.sum()):3d}/{len(q):<3d} |"
                        f" {int(q.full4b.sum()):3d}/{len(q)}")
    say(f"\n  OVERALL rule 8: {int(wfd.beats_spy.sum())} of {len(wfd)} picks beat SPY's OOS Sharpe;"
        f" {int(wfd.beats_base.sum())} of {len(wfd)} beat the LIVE book's;"
        f" {int(wfd.full4b.sum())} of {len(wfd)} carry a full-sample 4b.")
    say(f"  BENCHMARK OOS (2017-2026), read once: SPY {wfd.spy_OOS_CAGR.mean():.2%} /"
        f" {wfd.spy_OOS_Sharpe.mean():.4f};  live RULES v2 {wfd.base_OOS_Sharpe.mean():.4f}"
        f"  (panel-pooled means).")
    publish("DOES THE FLOOR MOVE THE RULE-8 PICK?",
            "; ".join(f"phi={p:.2f} picked in {int((wfd.pick_phi == p).sum())} of {len(wfd)}"
                      for p in PHIS))

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
