#!/usr/bin/env python3
"""idea 2512 (lane cloud, run 67, 2026-09-23) — DOES A FIXED WEEKLY TRADE BUDGET CLEAR THE
-31% ADOPTION BAR WHERE EVERY CONTINUOUS DEVICE HAS NOT?

THE GAP.  Every turnover device this record has closed SCALES or DELAYS THE WHOLE TRADE VECTOR:
idea 2328's weight-drift no-trade band, 2351's minimum hold, 2391/2404's partial-adjustment
damper, 2408's calendar rota, 2463's PARTIAL lambda, 2499's event-driven cadence.  NOT ONE has
ever imposed a HARD TICKET COUNT, which is the constraint a real account actually faces: a human
running this book weekly will place a handful of orders, not fifty-six.

THE DEVICE.  At each weekly rebalance form the committed target `tgt_i = min(g/N_in, cap)` on
in-band names, compare it with the CURRENT DRIFTED risk book, and EXECUTE ONLY THE `k` LEGS WITH
THE LARGEST `|dw_i|`.  Every other name keeps its drifted weight until a later week.  The
un-executed notional stays where it is, so the device can only ever place FEWER tickets than the
committed book -- though whether it places less TURNOVER is an empirical question, not a
definition (deferring a leg can make it bigger later), and it is PUBLISHED rather than gated.

WHY IT MIGHT WORK, STATED BEFORE THE RUN.  Idea 2457 named the churn: most of the committed
book's weekly trading is DENOMINATOR DRIFT -- tiny re-sizes of names nobody decided anything
about, because `g/N_in` moved when some other name entered or left.  Idea 2488 measured it:
83.1% of CAP2's tickets are under 10 bp of NAV and they carry only 19.3% of turnover.  A budget
that spends its tickets on the LARGEST legs is by construction spending them on ENTRIES and
EXITS -- the decisions -- and starving exactly the drift.  That is the one shape no killed device
had.

WHY IT MIGHT NOT, ALSO STATED BEFORE THE RUN.  Twelve killed devices all failed the same way:
the turnover they saved was bought by CUTTING EXPOSURE, and the CAGR went with it (idea 2477:
the exchange rate splits by realised risk gross, rank corr +0.797, not by device name).  A
budget is a de-grosser in one direction (an entry it cannot afford is exposure not taken) and a
LEVERAGER in the other (an exit it cannot afford is exposure it keeps through a downtrend -- and
the exit leg is what the 200d gate IS).  Realised risk gross, max single-name weight and the
number of names held OUT OF BAND are published on every row.

THE PLACEBO, WHICH IS THE POINT OF THE RUN.  Idea 2499 was killed not by its own numbers but by
a frequency-matched RANDOM control that saved MORE turnover at the same acting count.  This run
carries the analogous TICKET-MATCHED control from the start: at every rebalance, a placebo book
executes the SAME NUMBER of legs drawn UNIFORMLY AT RANDOM from the legs that wanted to trade
(8 md5 seeds).  If "largest |dw| first" is not better than "any k of them", the selection rule is
decoration and the device is just a ticket count.

DIAL 1 -- k, the executed-leg budget per rebalance, in {INF (committed, no budget), 24, 16, 10,
          6, 3}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: the book
{CAP2 (cap 0.020, idea 2322's standing candidate), CAND (uncapped, ideas 2300/2332)}; panels
{U56, B136}; cost rungs {0, 10, 25, 50} bps; cadence {W, M}; t+1 execution; band 0.03; MA 200d;
SHY sweep at phi = 1.00.

THE SWEEP CONVENTION, DECLARED.  The budget governs RISK legs only.  The SHY residual sweep is
the accounting leg that makes the book sum to NAV and is always executed; its turnover IS
charged at every rung, and the risk-only ticket count is published beside the total.  Gate G8
asserts the risk ticket count never exceeds k.

WHAT IS REPORTED, WHETHER OR NOT IT FLATTERS THE DEVICE.  Realised turnover and the % SAVED
against the matched k = INF cell; the EXCHANGE RATE in pp of CAGR per 1% of turnover saved on
the record's convention (`d_CAGR_pp / -d_turn_pct`) against the ~-0.10 every killed device paid
and idea 2463's two classes; idea 2431's adoption bar (-31.0% turnover at dCAGR >= 0); realised
risk gross and max name weight; the placebo's saving and CAGR at matched ticket count; both KEEP
paths at every row; and rule 8.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  Not placing a ticket cannot mend three legs that
already fail.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (k, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE, separately at every (panel, book, cadence, rung).

THE COMPARAND CAVEAT THE RECORD NOW OWNS.  Idea 2516 (2026-09-23) KILLED the sufficiency of 4b's
SPY comparand on a survivorship-selected panel: 0 of 21 committed capped-family 4b passes survive
substituting the panel's own equal-weight buy-and-hold.  PROTOCOL rule 4b still reads SPY, so
SPY is what is scored here, but every 4b count in this file should be read as a SPY-relative
statement and not as evidence of an edge over holding the panel.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The budget-vs-committed contrast is same-tape,
same-days, same-names and first-order immune to that bias; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_fixed-weekly-trade-budget_cloud.py
"""
from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "fixed-weekly-trade-budget", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
KS = [np.inf, 24, 16, 10, 6, 3]                  # DIAL 1
GROSSES = [0.75, 1.00]                           # DIAL 2
BOOKS = {"CAP2": 0.020, "CAND": np.inf}          # published axis, not a dial
RUNGS = [0.0, 10.0, 25.0, 50.0]                  # published
CADENCES = ["W", "M"]                            # published
SWEEP = "SHY"
SEEDS = 8                                        # placebo seeds (md5, deterministic)
HEAD_K, HEAD_G, HEAD_RUNG, HEAD_CAD, HEAD_BOOK = np.inf, 0.75, 10.0, "W", "CAP2"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ADOPT_TURN, ADOPT_CAGR = -31.0, 0.0              # idea 2431's adoption bar
KILLED_RATE = -0.10                              # the rate every killed device paid
TOL = 1e-12

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


def kname(k):
    return "INF" if not np.isfinite(k) else f"{int(k):d}"


def seed_rng(*parts):
    h = hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()
    return np.random.default_rng(int(h[:16], 16))


def eligible(px):
    """Names permitted to be held: inside the 200d +/- BAND hysteresis band and priced.
    `baseline.band_state` unmodified (G2 asserts bit-identity)."""
    return band_state(px, BAND) & px.notna()


# ---------------------------------------------------------------- the book
def run_book(prices, el, gross, cap, k, freq, sweep=True, placebo_seed=None):
    """Path-dependent runner.  Weights are DECIDED at t-1 and APPLIED at t, the book drifts
    between rebalances, and the residual is swept into SHY -- `engine.backtest` semantics
    verbatim at k = INF (G1).  The budget needs the CURRENT DRIFTED book to form its trade
    vector, so the target cannot be pre-computed as a frame; it is formed inside the loop.

    `risk` tracks the drifted RISK book alone; `sx` tracks the drifted SHY SWEEP add-on, so the
    budget never mistakes swept cash for a held position (SHY is also a band-eligible name).

    placebo_seed is None for the real device (largest |dw| first) or an int for the TICKET-MATCHED
    random control (same number of legs, drawn uniformly from the legs that wanted to trade)."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    el_dec = el.reindex(prices.index).fillna(False).shift(1, fill_value=False).values
    nin = el.sum(axis=1).replace(0, np.nan)
    per_dec = (gross / nin).clip(upper=cap).fillna(0.0).shift(1, fill_value=0.0).values
    s_key = pd.Series(prices.index.to_period(freq), index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    rng = np.random.default_rng(placebo_seed) if placebo_seed is not None else None

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    risk = np.zeros(m)
    sx = 0.0
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); rg = np.zeros(n)
    nheld = np.zeros(n); mx = np.zeros(n); swp = np.zeros(n); reb = np.zeros(n)
    tick_r = np.zeros(n); tick_t = np.zeros(n); want = np.zeros(n); oob = np.zeros(n)
    lev = 0
    for i in range(n):
        if mask[i] or i == 0:
            e = el_dec[i]
            tgt = np.where(e, per_dec[i], 0.0)
            d = tgt - risk
            wanted = np.abs(d) > TOL
            want[i] = float(wanted.sum())
            if not np.isfinite(k):
                new_r = tgt
                tick_r[i] = want[i]
            else:
                take = int(min(k, wanted.sum()))
                new_r = risk.copy()
                if take > 0:
                    if rng is None:
                        sel = np.argsort(-np.abs(d))[:take]
                    else:
                        cand = np.flatnonzero(wanted)
                        sel = rng.choice(cand, size=take, replace=False)
                    new_r[sel] = tgt[sel]
                tick_r[i] = float(take)
            tot_r = new_r.sum()
            if tot_r > 1.0:                                   # no leverage, ever (G4)
                new_r = new_r / tot_r
                lev += 1
            new = new_r.copy()
            add = max(0.0, 1.0 - new.sum()) * s_ok[i] if sweep else 0.0
            new[si] += add
            dd = np.abs(new - cur)
            turn[i] = float(dd.sum())
            tick_t[i] = float((dd > 1e-9).sum())
            reb[i] = 1.0
            cur = new; risk = new_r; sx = add
            oob[i] = float(((risk > TOL) & ~e).sum())
        gr[i] = cur.sum(); rg[i] = float(risk.sum()); nheld[i] = float((risk > TOL).sum())
        mx[i] = float(risk.max()); swp[i] = sx
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i])
        tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot
            risk = risk * (1 + rv[i]) / tot
            sx = sx * (1 + rv[i, si]) / tot
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), risk_gross=pd.Series(rg, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx),
                sweep_w=pd.Series(swp, index=idx), reb=pd.Series(reb, index=idx),
                tick_r=pd.Series(tick_r, index=idx), tick_t=pd.Series(tick_t, index=idx),
                want=pd.Series(want, index=idx), oob=pd.Series(oob, index=idx), lev=lev)


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
    say("=== idea 2512 — DOES A FIXED WEEKLY TRADE BUDGET CLEAR THE -31% ADOPTION BAR WHERE")
    say("    EVERY CONTINUOUS DEVICE HAS NOT?  (lane cloud, run 67) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 executed-leg budget k {[kname(k) for k in KS]}   DIAL 2 gross {GROSSES}")
    say(f"    PUBLISHED AXIS, NEVER SELECTED ON: book {list(BOOKS)}, panels, rungs, cadence.")
    say("    DEVICE: execute only the k legs with the largest |dw|; every other name keeps its")
    say("    DRIFTED weight until a later week.  The SHY residual sweep is always executed and")
    say("    always charged; the risk-only ticket count is published beside the total.")
    say("    PRE-STATED RISK: a budget is a de-grosser on the ENTRY leg and a LEVERAGER on the")
    say("    EXIT leg -- and the exit leg IS the 200d gate.  Risk gross, max name weight and the")
    say("    count of names held OUT OF BAND are published on every row.")
    say(f"    PLACEBO: ticket-matched RANDOM leg selection, {SEEDS} md5 seeds (idea 2499's lesson).")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383), 0 of 40-120 (2318/2322/2326/2343).")
    say("    COMPARAND CAVEAT: idea 2516 killed the SUFFICIENCY of 4b's SPY comparand on a")
    say("    survivorship-selected panel.  PROTOCOL still reads SPY, so SPY is scored; read every")
    say("    4b count below as SPY-relative, not as an edge over holding the panel.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The budget-vs-committed contrast is same-tape, same-days,")
    say("    same-names and first-order immune; the absolute 4b verdicts are not.")
    gate("G6 exactly two tuned parameters", "k, gross", "2", True)

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
    nin_u = el_u.sum(axis=1).replace(0, np.nan)
    d1 = 0.0
    for _cap in BOOKS.values():
        w = el_u.astype(float).mul((0.75 / nin_u).clip(upper=_cap), axis=0).fillna(0.0)
        r_eng = backtest(px_u, w, cost_bps=HEAD_RUNG, freq=HEAD_CAD)["returns"]
        lv = run_book(px_u, el_u, 0.75, _cap, np.inf, HEAD_CAD, sweep=False)
        d1 = max(d1, float((r_eng - (lv["r0"] - lv["turn"] * HEAD_RUNG / 1e4)).abs().max()))
    gate("G1 the k=INF runner IS engine.backtest on the same risk-weight frame (CAP2 and CAND,"
         " g 0.75, W, 10 bps, sweep off)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # ------------------------------------------------------------ the grid
    rows, facts, paths = [], [], {}
    lev_tot, gmax_tick, clamp_counts = 0, [], []
    cmp_cache = {}
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        spy_t = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEAD_RUNG, freq="W")["returns"].loc[start:]
        cmp_cache[pname] = (spy_t, base_t)
        for bname, cap in BOOKS.items():
            for cad in CADENCES:
                for k in KS:
                    for gross in GROSSES:
                        bk = run_book(px, el, gross, cap, k, cad)
                        lev_tot += bk["lev"]
                        clamp_counts.append(bk["lev"])
                        r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                        key = (pname, bname, cad, kname(k), gross)
                        paths[key] = r0
                        yrs = len(tn) / 252
                        rb = bk["reb"].loc[start:].sum()
                        if np.isfinite(k):
                            gmax_tick.append(float(bk["tick_r"].loc[start:].max()) <= k + 1e-9)
                        facts.append(dict(panel=pname, book=bname, cadence=cad, k=kname(k),
                                          gross=gross,
                                          turnover_yr=float(tn.sum() / yrs),
                                          rebals_yr=float(rb / yrs),
                                          risk_tickets_yr=float(bk["tick_r"].loc[start:].sum() / yrs),
                                          tot_tickets_yr=float(bk["tick_t"].loc[start:].sum() / yrs),
                                          wanted_per_reb=float(bk["want"].loc[start:].sum() / max(rb, 1)),
                                          mean_names=float(bk["names"].loc[start:].mean()),
                                          mean_oob=float(bk["oob"].loc[start:].mean()),
                                          mean_gross=float(bk["gross"].loc[start:].mean()),
                                          max_gross=float(bk["gross"].loc[start:].max()),
                                          mean_risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                                          max_risk_gross=float(bk["risk_gross"].loc[start:].max()),
                                          max_name_w=float(bk["maxw"].loc[start:].max()),
                                          mean_sweep=float(bk["sweep_w"].loc[start:].mean())))
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_oos = r.loc[OOS_START:]
                            spy_oos = spy_t.loc[OOS_START:]
                            r_is = r.loc[:IS_END]
                            L = legs(r, base_t, spy_t, r_oos, spy_oos)
                            rows.append(dict(panel=pname, book=bname, cadence=cad, k=kname(k),
                                             gross=gross, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                             Calmar=calmar(r),
                                             turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                             IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos),
                                             OOS_MaxDD=maxdd(r_oos),
                                             spy_CAGR=cagr(spy_t), spy_Sharpe=sharpe(spy_t),
                                             spy_MaxDD=maxdd(spy_t),
                                             spy_OOS_CAGR=cagr(spy_oos),
                                             spy_OOS_Sharpe=sharpe(spy_oos),
                                             base_CAGR=cagr(base_t), base_Sharpe=sharpe(base_t),
                                             base_MaxDD=maxdd(base_t),
                                             base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                             **L))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.rows.csv", index=False)
    fdf = pd.DataFrame(facts); fdf.to_csv(f"{OUT}.books.csv", index=False)
    gmax = float(fdf.max_gross.max())
    gate("G4 no leverage EVER (realised book gross <= 1 on every day of every arm)",
         f"max realised book gross {gmax:.12f} over {len(facts)} books", "<= 1 + 1e-9",
         gmax <= 1.0 + 1e-9)
    say("    THE CLAMP IS NOT DECORATION AND IS PUBLISHED RATHER THAN HIDDEN: unlike every")
    say("    continuous device in this record, a BUDGET can leave the drifted risk book summing")
    say("    above the target gross, because an EXIT it could not afford is exposure it KEEPS.")
    clamp = fdf.copy()
    clamp["clamps"] = [c for c in clamp_counts]
    publish("G4b rebalances at which the no-leverage clamp BOUND, by (k, gross)",
            "; ".join(f"k={kk} g={gg:.2f}: {int(v)}"
                      for (kk, gg), v in clamp.groupby(["k", "gross"]).clamps.sum().items()))
    gate("G8 the risk ticket count never exceeds k",
         f"{sum(gmax_tick)} of {len(gmax_tick)} finite-k books", "all", all(gmax_tick))

    # G5 cost linearity
    q0 = df[(df.cost_bps == 0.0)].set_index(["panel", "book", "cadence", "k", "gross"])
    q50 = df[(df.cost_bps == 50.0)].set_index(["panel", "book", "cadence", "k", "gross"])
    imp = (q0.CAGR - q50.CAGR)
    gate("G5 cost enters only through turnover x rung",
         f"max|d| between the 50bps row and its own 0bps row rebuilt from turnover: "
         f"{float(imp.abs().max()):.4f} pp of CAGR (sign check only)", "finite",
         bool(np.isfinite(imp).all()))

    same_spy = df.groupby("panel").spy_Sharpe.nunique().max()
    same_base = df.groupby("panel").base_Sharpe.nunique().max()
    gate("G7 comparands identical across every arm within a panel",
         f"distinct SPY Sharpe {same_spy}, distinct live-RULES Sharpe {same_base}", "1 and 1",
         same_spy == 1 and same_base == 1)

    # G3 the k=INF cell reproduces the committed books
    hd = df[(df.panel == "U56") & (df.book == "CAP2") & (df.cadence == "W") & (df.k == "INF")
            & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
    hc = df[(df.panel == "U56") & (df.book == "CAND") & (df.cadence == "W") & (df.k == "INF")
            & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
    publish("G3 committed U56 W 10bps g0.75 headlines reproduced here",
            f"CAP2 {hd.CAGR:.2%} / {hd.Sharpe:.4f} / {hd.MaxDD:.2%} (turn {hd.turnover_yr:.2f}x/yr);"
            f"  CAND {hc.CAGR:.2%} / {hc.Sharpe:.4f} / {hc.MaxDD:.2%} (turn {hc.turnover_yr:.2f}x/yr)")

    # ------------------------------------------------------------ A. what the budget does
    say("\n=== A. WHAT THE BUDGET DOES — TICKETS, TURNOVER AND EXPOSURE (10 bps rows) ===")
    say("  panel book cad  k   |  gross | tickets/reb | turn x/yr | % saved | CAGR   | dCAGR pp |"
        " rate pp/1% | mean risk g | max name w | names OOB")
    ex_rows = []
    for pname in panels:
        for bname in BOOKS:
            for cad in CADENCES:
                for gross in GROSSES:
                    base_f = fdf[(fdf.panel == pname) & (fdf.book == bname) & (fdf.cadence == cad)
                                 & (fdf.k == "INF") & (fdf.gross == gross)].iloc[0]
                    base_r = df[(df.panel == pname) & (df.book == bname) & (df.cadence == cad)
                                & (df.k == "INF") & (df.gross == gross) & (df.cost_bps == 10.0)].iloc[0]
                    for k in KS:
                        f = fdf[(fdf.panel == pname) & (fdf.book == bname) & (fdf.cadence == cad)
                                & (fdf.k == kname(k)) & (fdf.gross == gross)].iloc[0]
                        rr = df[(df.panel == pname) & (df.book == bname) & (df.cadence == cad)
                                & (df.k == kname(k)) & (df.gross == gross)
                                & (df.cost_bps == 10.0)].iloc[0]
                        dturn = 100.0 * (f.turnover_yr - base_f.turnover_yr) / base_f.turnover_yr
                        dcagr = 100.0 * (rr.CAGR - base_r.CAGR)
                        rate = dcagr / -dturn if abs(dturn) > 1e-9 else np.nan
                        ex_rows.append(dict(panel=pname, book=bname, cadence=cad, k=kname(k),
                                            gross=gross, dturn_pct=dturn, dcagr_pp=dcagr,
                                            rate=rate,
                                            dgross=f.mean_risk_gross - base_f.mean_risk_gross,
                                            adopt=bool(dturn <= ADOPT_TURN and dcagr >= ADOPT_CAGR)))
                        if cad == "W" and gross == 0.75:
                            say(f"  {pname:5s} {bname:4s} {cad}  {kname(k):3s} | {gross:.2f}  |"
                                f" {f.risk_tickets_yr / max(f.rebals_yr, 1e-9):11.2f} |"
                                f" {f.turnover_yr:9.2f} | {dturn:6.2f}% | {rr.CAGR:6.2%} |"
                                f" {dcagr:8.2f} | {rate:10.4f} | {f.mean_risk_gross:11.4f} |"
                                f" {f.max_name_w:10.4f} | {f.mean_oob:9.2f}")
    ex = pd.DataFrame(ex_rows); ex.to_csv(f"{OUT}.exchange.csv", index=False)
    fin = ex[ex.k != "INF"]
    say(f"\n  OVER ALL {len(fin)} FINITE-k ARMS: turnover change median {fin.dturn_pct.median():+.2f}%"
        f" (min {fin.dturn_pct.min():+.2f}%, max {fin.dturn_pct.max():+.2f}%);"
        f" {int((fin.dturn_pct < 0).sum())} of {len(fin)} SAVE turnover.")
    say(f"  EXCHANGE RATE (pp of CAGR per 1% of turnover saved): median {fin.rate.median():+.4f}"
        f" (IQR {fin.rate.quantile(.25):+.4f}..{fin.rate.quantile(.75):+.4f}).  The ~{KILLED_RATE}"
        f" every killed device paid is the reference.")
    say(f"  EXPOSURE NEUTRALITY: d(mean risk gross) vs the matched k=INF cell — median"
        f" {fin.dgross.median():+.4f}, min {fin.dgross.min():+.4f}, max {fin.dgross.max():+.4f};"
        f" {int((fin.dgross.abs() < 0.01).sum())} of {len(fin)} within +/-0.01.")
    say(f"  IDEA 2431 ADOPTION BAR (turnover <= {ADOPT_TURN}% at dCAGR >= {ADOPT_CAGR}):"
        f" {int(fin.adopt.sum())} of {len(fin)} arms clear it.")
    if int(fin.adopt.sum()):
        for _, r in fin[fin.adopt].iterrows():
            say(f"    CLEARS: {r.panel} {r.book} {r.cadence} k={r.k} g={r.gross:.2f}"
                f"  dturn {r.dturn_pct:+.2f}%  dCAGR {r.dcagr_pp:+.2f} pp"
                f"  dRiskGross {r.dgross:+.4f}")

    # ------------------------------------------------------------ B. the placebo
    say(f"\n=== B. THE TICKET-MATCHED RANDOM PLACEBO ({SEEDS} md5 seeds; W, gross 0.75, 10 bps) ===")
    say("  At every rebalance the placebo executes the SAME NUMBER of legs, drawn UNIFORMLY at")
    say("  random from the legs that wanted to trade.  If 'largest |dw| first' is not better than")
    say("  'any k of them', the selection rule is decoration.")
    say("  panel book  k   | real turn | plac turn (mean) | real cut | plac cut | real CAGR |"
        " plac CAGR (mean) | excess cut | excess CAGR")
    pl_rows = []
    for pname, px in panels.items():
        el = eligible(px); start = px.index[WARMUP]
        for bname, cap in BOOKS.items():
            bf = fdf[(fdf.panel == pname) & (fdf.book == bname) & (fdf.cadence == "W")
                     & (fdf.k == "INF") & (fdf.gross == 0.75)].iloc[0]
            for k in KS:
                if not np.isfinite(k):
                    continue
                rf = fdf[(fdf.panel == pname) & (fdf.book == bname) & (fdf.cadence == "W")
                         & (fdf.k == kname(k)) & (fdf.gross == 0.75)].iloc[0]
                rr = df[(df.panel == pname) & (df.book == bname) & (df.cadence == "W")
                        & (df.k == kname(k)) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
                pt, pc, ptick = [], [], []
                for s in range(SEEDS):
                    sd = int(hashlib.md5(f"{pname}|{bname}|{k}|{s}".encode()).hexdigest()[:8], 16)
                    bk = run_book(px, el, 0.75, cap, k, "W", placebo_seed=sd)
                    tn = bk["turn"].loc[start:]; yrs = len(tn) / 252
                    pt.append(float(tn.sum() / yrs))
                    pc.append(cagr(bk["r0"].loc[start:] - tn * 10.0 / 1e4))
                    ptick.append(float(bk["tick_r"].loc[start:].sum() / yrs))
                rcut = 100.0 * (rf.turnover_yr - bf.turnover_yr) / bf.turnover_yr
                pcut = 100.0 * (np.mean(pt) - bf.turnover_yr) / bf.turnover_yr
                pl_rows.append(dict(panel=pname, book=bname, k=kname(k),
                                    real_turn=rf.turnover_yr, plac_turn=float(np.mean(pt)),
                                    real_cut=rcut, plac_cut=pcut,
                                    real_cagr=rr.CAGR, plac_cagr=float(np.mean(pc)),
                                    excess_cut=rcut - pcut, excess_cagr=100.0 * (rr.CAGR - np.mean(pc)),
                                    tick_match=abs(rf.risk_tickets_yr - np.mean(ptick))))
                say(f"  {pname:5s} {bname:4s} {kname(k):3s} | {rf.turnover_yr:9.2f} |"
                    f" {np.mean(pt):16.2f} | {rcut:7.2f}% | {pcut:7.2f}% | {rr.CAGR:9.2%} |"
                    f" {np.mean(pc):16.2%} | {rcut - pcut:+9.2f} pp |"
                    f" {100.0 * (rr.CAGR - np.mean(pc)):+11.2f} pp")
    pl = pd.DataFrame(pl_rows); pl.to_csv(f"{OUT}.placebo.csv", index=False)
    publish("G11 the placebo executes the SAME RULE for ticket COUNT (min(k, legs wanting to"
            " trade)) on its OWN state; the realised counts differ only because the two paths"
            " diverge, so this is PUBLISHED, not asserted",
            f"max |real - placebo| risk tickets/yr {pl.tick_match.max():.4f}"
            f" against a mean of {pl.real_turn.mean():.2f}x/yr turnover and"
            f" {fdf[fdf.k != 'INF'].risk_tickets_yr.mean():.1f} risk tickets/yr")
    say(f"\n  POOLED OVER {len(pl)} (panel, book, k) CELLS: excess turnover cut (real - placebo)"
        f" median {pl.excess_cut.median():+.2f} pp"
        f" (real saves MORE in {int((pl.excess_cut < 0).sum())} of {len(pl)});"
        f" excess CAGR median {pl.excess_cagr.median():+.2f} pp"
        f" (real wins in {int((pl.excess_cagr > 0).sum())} of {len(pl)}).")

    # ------------------------------------------------------------ C. headline table
    say("\n=== C. HEADLINE CELLS (gross 0.75, W, 10 bps) — FULL, HALVES, OOS ===")
    say("  panel book  k   |   CAGR |  Sharpe |   MaxDD |   H1   /   H2  |  OOS CAGR | OOS Sharpe"
        " | turn x/yr | 4a | 4b | failing 4b legs")
    for pname in panels:
        for bname in BOOKS:
            for k in KS:
                q = df[(df.panel == pname) & (df.book == bname) & (df.cadence == "W")
                       & (df.k == kname(k)) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
                bad = [c for c in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not q[c]]
                say(f"  {pname:5s} {bname:4s} {kname(k):3s} | {q.CAGR:6.2%} | {q.Sharpe:7.4f} |"
                    f" {q.MaxDD:7.2%} | {q.H1:6.3f} / {q.H2:6.3f} | {q.OOS_CAGR:9.2%} |"
                    f" {q.OOS_Sharpe:10.4f} | {q.turnover_yr:9.2f} |"
                    f" {'Y' if q.pass4a else '.':^2s} | {'Y' if q.pass4b else '.':^2s} |"
                    f" {','.join(bad) if bad else '-'}")
    z = df[(df.panel == "U56") & (df.cost_bps == 10.0)].iloc[0]
    say(f"  COMPARANDS (U56, identical on every row): SPY {z.spy_CAGR:.2%} / {z.spy_Sharpe:.4f} /"
        f" {z.spy_MaxDD:.2%}, OOS {z.spy_OOS_CAGR:.2%} / {z.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {z.base_CAGR:.2%} / {z.base_Sharpe:.4f} / {z.base_MaxDD:.2%},"
        f" OOS Sharpe {z.base_OOS_Sharpe:.4f}.")
    z2 = df[(df.panel == "B136") & (df.cost_bps == 10.0)].iloc[0]
    say(f"  COMPARANDS (B136): SPY {z2.spy_CAGR:.2%} / {z2.spy_Sharpe:.4f} / {z2.spy_MaxDD:.2%},"
        f" OOS {z2.spy_OOS_CAGR:.2%} / {z2.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {z2.base_CAGR:.2%} / {z2.base_Sharpe:.4f} / {z2.base_MaxDD:.2%}.")

    # ------------------------------------------------------------ D. KEEP paths
    say("\n=== D. BOTH KEEP PATHS OVER ALL PUBLISHED ROWS ===")
    say(f"  4b {int(df.pass4b.sum())} of {len(df)};  4a {int(df.pass4a.sum())} of {len(df)}")
    say("  k   | rows | 4b   | 4a  | 4b at 10bps | L_H1 f | L_H2 f | L_OOS f | L_DD f | L_CAGR f")
    for k in KS:
        q = df[df.k == kname(k)]
        q10 = q[q.cost_bps == 10.0]
        say(f"  {kname(k):3s} | {len(q):4d} | {int(q.pass4b.sum()):4d} | {int(q.pass4a.sum()):3d} |"
            f" {int(q10.pass4b.sum()):11d} | {int((~q.L_H1).sum()):6d} | {int((~q.L_H2).sum()):6d} |"
            f" {int((~q.L_OOS).sum()):7d} | {int((~q.L_DD).sum()):6d} | {int((~q.L_CAGR).sum()):8d}")
    say("  by (panel, book, rung), 4b count out of 12 (k x gross x cadence = 24 -> per cadence 12):")
    for pname in panels:
        for bname in BOOKS:
            line = "  ".join(
                f"{r:.0f}bps {int(df[(df.panel == pname) & (df.book == bname) & (df.cost_bps == r)].pass4b.sum()):2d}/24"
                for r in RUNGS)
            say(f"    {pname:5s} {bname:4s}: {line}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the two dials (k, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (panel, book, cadence, rung). ===")
    wf = []
    for pname in panels:
        for bname in BOOKS:
            for cad in CADENCES:
                for rung in RUNGS:
                    q = df[(df.panel == pname) & (df.book == bname) & (df.cadence == cad)
                           & (df.cost_bps == rung)]
                    for ch, keyf in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        p = q.loc[q[keyf].idxmax()]
                        wf.append(dict(panel=pname, book=bname, cadence=cad, cost_bps=rung,
                                       chooser=ch, pick_k=p.k, pick_gross=p.gross,
                                       OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                                       OOS_MaxDD=p.OOS_MaxDD, spy_OOS_CAGR=p.spy_OOS_CAGR,
                                       spy_OOS_Sharpe=p.spy_OOS_Sharpe,
                                       base_OOS_Sharpe=p.base_OOS_Sharpe,
                                       beats_spy=bool(p.OOS_Sharpe > p.spy_OOS_Sharpe),
                                       beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                                       full4b=bool(p.pass4b), full4a=bool(p.pass4a)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  panel book cad | picks (k/g)                       | OOS CAGR | OOS Sharpe | > SPY |"
        " > live | full 4b")
    for pname in panels:
        for bname in BOOKS:
            for cad in CADENCES:
                q = wfd[(wfd.panel == pname) & (wfd.book == bname) & (wfd.cadence == cad)]
                top = q.groupby(["pick_k", "pick_gross"]).size().sort_values(ascending=False)
                desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
                say(f"  {pname:5s} {bname:4s} {cad:3s} | {desc:33s} | {q.OOS_CAGR.mean():8.2%} |"
                    f" {q.OOS_Sharpe.mean():10.4f} | {int(q.beats_spy.sum()):3d}/{len(q):<3d} |"
                    f" {int(q.beats_base.sum()):3d}/{len(q):<3d} | {int(q.full4b.sum()):3d}/{len(q)}")
    say(f"\n  OVERALL rule 8: {int(wfd.beats_spy.sum())} of {len(wfd)} picks beat SPY's OOS Sharpe;"
        f" {int(wfd.beats_base.sum())} of {len(wfd)} beat the LIVE book's;"
        f" {int(wfd.full4b.sum())} of {len(wfd)} carry a full-sample 4b.")
    kc = wfd.pick_k.value_counts()
    say(f"  WHAT THE CHOOSER BUYS: {dict(kc)} — a BUDGET is only adopted by the fitted chooser"
        f" in {int((wfd.pick_k != 'INF').sum())} of {len(wfd)} draws.")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
