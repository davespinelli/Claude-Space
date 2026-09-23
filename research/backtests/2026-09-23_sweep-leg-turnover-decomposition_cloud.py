#!/usr/bin/env python3
"""idea 2449 (lane cloud, run 52, 2026-09-23) — HOW MUCH OF THE CANDIDATE'S 3.51x TURNOVER
BLOCKER IS THE SWEEP LEG'S OWN CHURN RATHER THAN THE RISK BOOK'S?

THE GAP.  The standing 4b candidate has exactly ONE stated adoption blocker: realised turnover of
3.51x/yr against the live book's 1.77x.  Run 49 found the ZERO-sweep construction is 22.4%
cheaper (2.72x vs 3.51x on U56/CAP2) while still passing 4b, i.e. roughly a fifth of the blocker
is the SHY leg trading against itself as the risk book's gross breathes.  But `sum |new - cur|`
is reported as ONE number at every published cell in this record, so nobody has ever billed the
two legs separately.  A blocker that is mostly sweep churn is an EXECUTION-CONVENTION question
(sweep monthly, or hold the T-bill through the drift), not a signal question.

THE DECOMPOSITION.  The runner carries the risk book `cur_risk` (an m-vector, SHY-as-a-band-name
included) and the sweep position `cur_sweep` (a scalar in the sweep instrument) as SEPARATE
state, drifting both on the same daily returns and the same portfolio total.  Then
    turn_risk  = sum_j |new_risk_j - cur_risk_j|              (the signal leg's own bill)
    turn_sweep = |new_sweep - cur_sweep|                       (the idle-cash leg's own bill)
    turn_net   = sum_{j != si} |dj| + |d_si + d_sweep|         (THE COMMITTED CONVENTION)
`turn_net` is what `engine.backtest` charges and is what every published 3.51x is: the two legs
NET at the sweep column, because a risk-book sale of SHY and a sweep purchase of SHY are the same
trade.  This run publishes all three and the netting benefit `turn_risk + turn_sweep - turn_net`,
which is itself a number the record has never seen.  G2 asserts the split runner is BIT-IDENTICAL
to the committed one at (SHY, weekly).

DIAL 1 -- the sweep instrument in {SHY (committed), IEF, LQD, ZERO}.  ZERO holds idle NAV at 0%
          and has NO sweep leg at all, so it is the lower bound on the sweep bill by construction.
DIAL 2 -- the sweep cadence in {W (committed, in lockstep with the core), M, Q, NEVER}.  A lazy
          sweep is re-set to `1 - gross_risk` only on its own dates; in between it DRIFTS, and is
          only ever clipped DOWNWARDS to keep total weight <= 1 (no leverage, ever).  The clip is
          a forced trade and is billed to the sweep leg; G7 publishes how often it binds.

EXACTLY TWO TUNED PARAMETERS (sweep instrument, sweep cadence).  Gross, panel, book, cost rung
and core cadence are REPORTED AT EVERY GRID POINT AND NEVER SELECTED ON.

BOOKS.  CAP2 (idea 2322's 2%-per-name capped candidate) and CAND (idea 2300/2332's uncapped
`gross / N_in` book), plus the LIVE RULES v2 book as the 4a baseline.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials are chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers,
2017-2026 is then read ONCE, and the picks are scored against the COMMITTED (SHY, W) cell.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and 2383 read it at 0 of 128 with L_DD, L_H2 and
L_OOS all failing at every cell.  A sweep-leg convention cannot move three failing legs at once.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest` on the live book.
G2 the split runner is BIT-IDENTICAL to the committed combined runner at (SHY, W).  G3 the
committed cell reproduces the published CAP2 / CAND U56 headlines.  G4 no leverage anywhere.
G5 cost exactly linear in the rung.  G6 exactly two tuned parameters.  G7 the no-leverage clip
(published, not asserted).  G8 ZERO's sweep bill is identically 0.  G9 ZERO is cadence-invariant.
G10 turn_net <= turn_risk + turn_sweep at every cell (the netting inequality).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The leg-vs-leg turnover split is a same-tape,
same-day accounting identity and is first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_sweep-leg-turnover-decomposition_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "sweep-leg-turnover-decomposition", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
INSTRUMENTS = ["SHY", "IEF", "LQD", "ZERO"]          # DIAL 1; SHY is committed, ZERO has no leg
SWEEP_CADENCES = ["W", "M", "Q", "NEVER"]            # DIAL 2; W is committed
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
NAME_CAP = 0.020
BOOKS = {"CAP2": NAME_CAP, "CAND": np.inf}
HEADLINE_RUNG, HEADLINE_INST, HEADLINE_CAD = 10.0, "SHY", "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LIVE_TURNOVER = 1.77                                  # the live RULES v2 book, for scale

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


# ---------------------------------------------------------------- the risk book
def risk_weights(px, gross, cap):
    """The committed candidate's risk leg: every name inside the 200d +/-band at gross/N_in,
    clipped to `cap` per name.  cap = INF is CAND, cap = 0.02 is CAP2."""
    el = band_state(px, BAND) & px.notna()
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_split(prices, w_risk, inst, sweep_cad, freq=CADENCE):
    """`engine.backtest` semantics, with the RISK book and the SWEEP position carried as separate
    state so their bills can be split.  Weights decided at t-1, applied at t; both legs drift
    between rebalances; the sweep is re-set only on its own cadence and is only ever clipped
    DOWNWARDS in between (no leverage).  `turn_net` is the committed convention."""
    cols = list(prices.columns)
    has_sweep = inst != "ZERO"
    si = cols.index(inst) if has_sweep else -1
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[inst].notna().values.astype(float) if has_sweep else np.zeros(len(prices))
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values

    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    core = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    if not has_sweep or sweep_cad == "NEVER":
        smask = np.zeros(len(prices), dtype=bool)
    else:
        k2 = pd.Series(prices.index.to_period(sweep_cad), index=prices.index)
        smask = (k2 != k2.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m); cs = 0.0
    t_net = np.zeros(n); t_risk = np.zeros(n); t_swp = np.zeros(n)
    r0 = np.zeros(n); gr = np.zeros(n); grisk = np.zeros(n); swp = np.zeros(n)
    nheld = np.zeros(n); mx = np.zeros(n); clip = np.zeros(n)
    for i in range(n):
        if core[i] or smask[i] or i == 0:
            new = wt[i].copy() if (core[i] or i == 0) else cur.copy()
            room = max(0.0, 1.0 - new.sum())
            if not has_sweep:
                ns = 0.0
            elif smask[i] or i == 0:
                ns = room * s_ok[i]                       # re-set to the target sweep
            else:
                ns = min(cs, room)                        # lazy: drift, clipped DOWN only
                clip[i] = 1.0 if ns < cs - 1e-15 else 0.0
            d = new - cur
            t_risk[i] = float(np.abs(d).sum())
            t_swp[i] = float(abs(ns - cs))
            if has_sweep:
                t_net[i] = float(np.abs(np.delete(d, si)).sum() + abs(d[si] + (ns - cs)))
            else:
                t_net[i] = t_risk[i]
            cur = new; cs = ns
        tot_w = cur.sum() + cs
        gr[i] = tot_w; grisk[i] = cur.sum(); swp[i] = cs
        nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum() + (cs * rv[i][si] if has_sweep else 0.0))
        g = cur * (1 + rv[i]); gs = cs * (1 + rv[i][si]) if has_sweep else 0.0
        tot = g.sum() + gs + (1 - tot_w)
        if tot > 0:
            cur = g / tot; cs = gs / tot
    idx = prices.index
    S = lambda a: pd.Series(a, index=idx)
    return dict(r0=S(r0), turn=S(t_net), turn_risk=S(t_risk), turn_sweep=S(t_swp),
                gross=S(gr), gross_risk=S(grisk), sweep_w=S(swp), names=S(nheld),
                maxw=S(mx), clip=S(clip))


def run_committed(prices, w_risk, inst=HEADLINE_INST, freq=CADENCE):
    """The committed combined runner (run 49's, verbatim) — the G2 comparand."""
    cols = list(prices.columns); si = cols.index(inst)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[inst].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    s_key = pd.Series(prices.index.to_period(freq), index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    n, m = len(prices.index), len(cols)
    cur = np.zeros(m); turn = np.zeros(n); r0 = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum()); cur = new
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    return dict(r0=pd.Series(r0, index=prices.index), turn=pd.Series(turn, index=prices.index))


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


def cells():
    """The (instrument, cadence) grid.  ZERO has no sweep leg, so it is priced ONCE and G9
    asserts cadence-invariance rather than publishing four identical rows."""
    out = []
    for inst in INSTRUMENTS:
        for cad in (SWEEP_CADENCES if inst != "ZERO" else ["n/a"]):
            out.append((inst, cad))
    return out


def main():
    t0 = time.time()
    say("=== idea 2449 — HOW MUCH OF THE 3.51x TURNOVER BLOCKER IS THE SWEEP LEG'S OWN CHURN? ===")
    say(f"    {DATE}  lane {LANE} run 52   band {BAND}  MA {MA_LEN}d  core cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}")
    say(f"    DIAL 1 sweep instrument {INSTRUMENTS}     DIAL 2 sweep cadence {SWEEP_CADENCES}")
    say("    The runner carries the RISK book and the SWEEP position as SEPARATE state and bills")
    say("    turn_risk, turn_sweep and turn_net (the committed netted convention) at every cell.")
    say("    PRIOR, STATED BEFORE COMPUTE: run 49's ZERO-sweep cell is 22.4% cheaper than the")
    say("    committed one, so the sweep leg's GROSS bill should be ~0.8x/yr of the 3.51x — but the")
    say("    two legs NET at the sweep column, so the netting benefit may be most of that gap.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383) and 0 of 40-120 (2318/2322/2326/2343).")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The leg split is an accounting identity on one tape and immune.")
    gate("G6 exactly two tuned parameters", "sweep instrument, sweep cadence", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)
        miss = [i for i in INSTRUMENTS if i != "ZERO" and i not in px.columns]
        gate(f"G0b every sweep instrument priced on {nm}",
             f"missing {miss or 'none'}; non-null on scored rows: "
             + " ".join(f"{i}:{bool(px[i].loc[px.index[WARMUP]:].notna().all())}"
                        for i in INSTRUMENTS if i != "ZERO"), "none missing", not miss)

    px_u = panels["U56"]

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_split(px_u, w_live, "ZERO", "n/a")
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, no sweep)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)
    lv_start = px_u.index[WARMUP]
    lv_r = (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4).loc[lv_start:]
    lv_turn = float(lv["turn"].loc[lv_start:].sum() / (len(lv_r) / 252))
    gate("G1b the 4a comparand IS the live book as live (RULES v2 de-grosses to CASH, never"
         " sweeps): its published turnover and Sharpe reproduce",
         f"turnover {lv_turn:.3f}x/yr (record: 1.77x)  Sharpe {sharpe(lv_r):.4f}"
         f" halves {halves(lv_r)[0]:.4f}/{halves(lv_r)[1]:.4f} (record: 1.2052, 1.2262/1.1897)"
         f"  MaxDD {maxdd(lv_r):.2%} (record: -12.05%)",
         "turnover within 0.05x and Sharpe within 1e-3 of the record",
         abs(lv_turn - 1.77) < 0.05 and abs(sharpe(lv_r) - 1.2052) < 1e-3)

    # G2 the SPLIT runner is bit-identical to the COMMITTED combined runner at (SHY, W)
    d2r, d2t = 0.0, 0.0
    for pn, px in panels.items():
        for bn, cap in BOOKS.items():
            wr = risk_weights(px, 0.75, cap)
            a = run_split(px, wr, "SHY", "W"); b = run_committed(px, wr, "SHY")
            d2r = max(d2r, float((a["r0"] - b["r0"]).abs().max()))
            d2t = max(d2t, float((a["turn"] - b["turn"]).abs().max()))
    gate("G2 the SPLIT runner == the COMMITTED combined runner at (SHY, W), 4 books",
         f"max|d returns| {d2r:.3e}   max|d netted turnover| {d2t:.3e}", "< 1e-12",
         max(d2r, d2t) < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        # THE 4a COMPARAND IS THE LIVE BOOK AS LIVE: RULES v2 clause 2 de-grosses to CASH and
        # never sweeps, so the baseline is run with NO sweep leg (inst = ZERO), which is
        # `engine.backtest(px, rules_v2_weights(px))` exactly — G1b asserts it.
        base = run_split(px, rules_v2_weights(px, band=BAND, gross=0.75), "ZERO", "n/a")
        base_r = (base["r0"] - base["turn"] * HEADLINE_RUNG / 1e4).loc[start:]
        base_turn = float(base["turn"].loc[start:].sum() / (len(base_r) / 252))
        for bname, cap in BOOKS.items():
            for gross in GROSSES:
                wr = risk_weights(px, gross, cap)
                for inst, cad in cells():
                    bk = run_split(px, wr, inst, cad)
                    sl = slice(start, None)
                    r0 = bk["r0"].loc[sl]; tn = bk["turn"].loc[sl]
                    tr = bk["turn_risk"].loc[sl]; ts = bk["turn_sweep"].loc[sl]
                    yrs = len(r0) / 252
                    book_facts.append(dict(
                        panel=pname, book=bname, gross=gross, inst=inst, cad=cad,
                        turn_net_yr=float(tn.sum() / yrs), turn_risk_yr=float(tr.sum() / yrs),
                        turn_sweep_yr=float(ts.sum() / yrs),
                        netting_yr=float((tr.sum() + ts.sum() - tn.sum()) / yrs),
                        sweep_share=float(ts.sum() / (tr.sum() + ts.sum())) if (tr.sum() + ts.sum()) > 0 else 0.0,
                        mean_sweep_w=float(bk["sweep_w"].loc[sl].mean()),
                        mean_gross=float(bk["gross"].loc[sl].mean()),
                        max_gross=float(bk["gross"].loc[sl].max()),
                        mean_gross_risk=float(bk["gross_risk"].loc[sl].mean()),
                        mean_names=float(bk["names"].loc[sl].mean()),
                        max_name_w=float(bk["maxw"].loc[sl].max()),
                        clip_days=float(bk["clip"].loc[sl].sum()),
                        n_rebal=float((tn > 0).sum())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, book=bname, gross=gross, inst=inst, cad=cad,
                            cost_bps=rung,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / yrs),
                            turn_risk_yr=float(tr.sum() / yrs), turn_sweep_yr=float(ts.sum() / yrs),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                            base_CAGR=cagr(base_r), base_turn=base_turn,
                            base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_OOS_MaxDD=maxdd(spy_oos), spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x 2 books x {len(GROSSES)} gross x {len(cells())}"
        f" (instrument, cadence) cells x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max total weight <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.12f} total, "
         f"{bf.max_name_w.max():.4f} max single risk name", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))
    gate("G10 the netting inequality turn_net <= turn_risk + turn_sweep at EVERY path",
         f"violations {int((bf.turn_net_yr > bf.turn_risk_yr + bf.turn_sweep_yr + 1e-12).sum())}"
         f" of {len(bf)}; max netting benefit {bf.netting_yr.max():.4f} turns/yr",
         "0", int((bf.turn_net_yr > bf.turn_risk_yr + bf.turn_sweep_yr + 1e-12).sum()) == 0)
    z = bf[bf.inst == "ZERO"]
    gate("G8 the ZERO sweep has NO sweep leg (turn_sweep identically 0)",
         f"max {z.turn_sweep_yr.max():.3e} over {len(z)} paths", "0.0", float(z.turn_sweep_yr.max()) == 0.0)
    zc = run_split(px_u, risk_weights(px_u, 0.75, NAME_CAP), "ZERO", "NEVER")
    zw = run_split(px_u, risk_weights(px_u, 0.75, NAME_CAP), "ZERO", "Q")
    d9 = float((zc["r0"] - zw["r0"]).abs().max() + (zc["turn"] - zw["turn"]).abs().max())
    gate("G9 the ZERO sweep is CADENCE-INVARIANT (so it is priced once, not four times)",
         f"max|d| {d9:.3e}", "0.0", d9 == 0.0)

    pz = panels["U56"]; bz = run_split(pz, risk_weights(pz, 0.75, NAME_CAP), "SHY", "W")
    st = pz.index[WARMUP]
    r25 = (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]; r50 = (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:]
    r00 = bz["r0"].loc[st:]
    d5 = float(((r00 - r25) * 2 - (r00 - r50)).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    cl = bf[(bf.inst != "ZERO")]
    publish("G7 the no-leverage clip on lazy sweeps (days the drifted sweep had to be cut)",
            "  ".join(f"{c}:{cl[cl.cad == c].clip_days.mean():.1f}d mean" for c in SWEEP_CADENCES)
            + f"  (of {len(pz) - WARMUP} scored rows)")

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.inst == "SHY") & (df.cad == "W")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.inst == "SHY") & (df.cad == "W")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10, abs(a.turnover_yr - 3.51) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 (SHY, W) reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318,"
         " 3.51x) AND CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f}"
         f" turn {a.turnover_yr:.2f}x; CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%}"
         f" OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f} -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. THE DECOMPOSITION
    say("\n=== A. THE ANSWER: THE COMMITTED 3.51x SPLIT INTO ITS TWO LEGS (instrument SHY, cadence W) ===")
    say("  panel book  g   | turn_net | turn_risk | turn_sweep | risk+sweep | netting | sweep share | vs live 1.77x")
    for pname in panels:
        for bn in BOOKS:
            for g in GROSSES:
                e = bf[(bf.panel == pname) & (bf.book == bn) & (bf.gross == g)
                       & (bf.inst == "SHY") & (bf.cad == "W")].iloc[0]
                say(f"  {pname:5s} {bn:4s} {g:.2f} | {e.turn_net_yr:8.3f} | {e.turn_risk_yr:9.3f} |"
                    f" {e.turn_sweep_yr:10.3f} | {e.turn_risk_yr + e.turn_sweep_yr:10.3f} |"
                    f" {e.netting_yr:7.3f} | {e.sweep_share:11.1%} |"
                    f" {e.turn_net_yr / LIVE_TURNOVER:8.2f}x")
    hs = bf[(bf.panel == "U56") & (bf.book == "CAP2") & (bf.gross == 0.75)
            & (bf.inst == "SHY") & (bf.cad == "W")].iloc[0]
    zr = bf[(bf.panel == "U56") & (bf.book == "CAP2") & (bf.gross == 0.75) & (bf.inst == "ZERO")].iloc[0]
    say(f"\n  THE HEADLINE CELL (U56 / CAP2 / g0.75).  Committed netted bill {hs.turn_net_yr:.3f}x/yr.")
    say(f"   The sweep leg's OWN gross bill is {hs.turn_sweep_yr:.3f}x/yr"
        f" = {hs.turn_sweep_yr / (hs.turn_risk_yr + hs.turn_sweep_yr):.1%} of the gross-of-netting total,")
    say(f"   but {hs.netting_yr:.3f}x/yr of it NETS against the risk book's own SHY trades, so the")
    say(f"   sweep leg's MARGINAL contribution to the committed number is"
        f" {hs.turn_net_yr - zr.turn_net_yr:+.3f}x/yr"
        f" ({(hs.turn_net_yr - zr.turn_net_yr) / hs.turn_net_yr:+.1%} of 3.51x),")
    say(f"   i.e. the ZERO-sweep book pays {zr.turn_net_yr:.3f}x/yr.  Adoption bar: the live book is"
        f" {LIVE_TURNOVER:.2f}x.")
    say(f"   EVEN AT ZERO SWEEP COST the risk leg alone is {zr.turn_net_yr / LIVE_TURNOVER:.2f}x the live book.")

    # ------------------------------------------------------------ B. every grid point
    say("\n=== B. THE FULL (instrument x cadence) LADDER, g 0.75 — EVERY GRID POINT ===")
    say("  panel book inst cad   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | net  risk  sweep | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bn in BOOKS:
            for inst, cad in cells():
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bn) & (df.inst == inst)
                           & (df.cad == cad) & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    tag = "   <= COMMITTED" if (inst == "SHY" and cad == "W") else ""
                    say(f"  {pname:5s} {bn:4s} {inst:4s} {cad:5s} {rung:5.1f} | {r.CAGR:6.2%}"
                        f" {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                        f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:4.2f} "
                        f"{r.turn_risk_yr:5.2f} {r.turn_sweep_yr:6.2f} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}{tag}")
    say("\n  (gross 1.00 rows are in the CSV; the headline conclusions are quoted at the live 0.75.)")

    # ------------------------------------------------------------ C. what the convention buys
    say("\n=== C. WHAT EACH CONVENTION BUYS AGAINST THE COMMITTED (SHY, W) CELL ===")
    say("  panel book  g   inst cad   | dTurnover_net | dCAGR@10 | dSharpe  | dOOS Sh  | 4b W -> 4b cell")
    dec = []
    for pname in panels:
        for bn in BOOKS:
            for g in GROSSES:
                z0 = df[(df.panel == pname) & (df.book == bn) & (df.gross == g) & (df.inst == "SHY")
                        & (df.cad == "W") & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                for inst, cad in cells():
                    if inst == "SHY" and cad == "W":
                        continue
                    r = df[(df.panel == pname) & (df.book == bn) & (df.gross == g)
                           & (df.inst == inst) & (df.cad == cad)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    dec.append(dict(panel=pname, book=bn, gross=g, inst=inst, cad=cad,
                                    dTurn=r.turnover_yr / z0.turnover_yr - 1,
                                    dTurn_abs=r.turnover_yr - z0.turnover_yr,
                                    dCAGR=r.CAGR - z0.CAGR, dSharpe=r.Sharpe - z0.Sharpe,
                                    dMaxDD=r.MaxDD - z0.MaxDD,
                                    dOOS_Sharpe=r.OOS_Sharpe - z0.OOS_Sharpe,
                                    w4b=bool(z0.pass4b), c4b=bool(r.pass4b)))
                    if g == 0.75:
                        say(f"  {pname:5s} {bn:4s} {g:.2f} {inst:4s} {cad:5s} |"
                            f" {r.turnover_yr / z0.turnover_yr - 1:+13.1%} | {r.CAGR - z0.CAGR:+8.2%} |"
                            f" {r.Sharpe - z0.Sharpe:+8.4f} | {r.OOS_Sharpe - z0.OOS_Sharpe:+8.4f} |"
                            f" {'PASS' if z0.pass4b else 'fail'} -> {'PASS' if r.pass4b else 'fail'}")
    dd_ = pd.DataFrame(dec); dd_.to_csv(f"{OUT}.decomposition.csv", index=False)
    say(f"\n  Over all {len(dd_)} (cell vs its own (SHY,W)) pairs at 10 bps:")
    say(f"   dTurnover < 0 in {int((dd_.dTurn < 0).sum())} of {len(dd_)}"
        f"   dCAGR > 0 in {int((dd_.dCAGR > 0).sum())}"
        f"   dSharpe > 0 in {int((dd_.dSharpe > 0).sum())}"
        f"   dOOS Sharpe > 0 in {int((dd_.dOOS_Sharpe > 0).sum())}"
        f"   4b kept in {int((dd_.w4b & dd_.c4b).sum())} of {int(dd_.w4b.sum())}")
    say("   by cadence (mean over instruments, panels, books, gross):")
    for cad in SWEEP_CADENCES:
        q = dd_[dd_.cad == cad]
        if len(q):
            say(f"    cad {cad:5s}  mean dTurn {q.dTurn.mean():+7.1%} ({q.dTurn_abs.mean():+.3f}x/yr)"
                f"  dCAGR {q.dCAGR.mean():+.2%}  dSharpe {q.dSharpe.mean():+.4f}"
                f"  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}   4b {int(q.c4b.sum())}/{len(q)}")
    say("   by instrument:")
    for inst in INSTRUMENTS:
        q = dd_[dd_.inst == inst]
        if len(q):
            say(f"    {inst:5s}      mean dTurn {q.dTurn.mean():+7.1%} ({q.dTurn_abs.mean():+.3f}x/yr)"
                f"  dCAGR {q.dCAGR.mean():+.2%}  dSharpe {q.dSharpe.mean():+.4f}"
                f"  dOOS Sh {q.dOOS_Sharpe.mean():+.4f}   4b {int(q.c4b.sum())}/{len(q)}")

    say("\n  THE ADOPTION QUESTION: does ANY (instrument, cadence) get the netted bill under the")
    say("  live book's 1.77x while KEEPING a 4b pass at 10 bps?")
    cand = df[(df.cost_bps == HEADLINE_RUNG) & (df.turnover_yr <= LIVE_TURNOVER) & df.pass4b]
    say(f"   rows with turnover <= {LIVE_TURNOVER:.2f}x AND 4b at 10 bps: {len(cand)} of"
        f" {len(df[df.cost_bps == HEADLINE_RUNG])}")
    cheap = df[(df.cost_bps == HEADLINE_RUNG) & df.pass4b].sort_values("turnover_yr")
    say(f"   the CHEAPEST 4b-passing cells at 10 bps ({len(cheap)} pass):")
    for _, r in cheap.head(8).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} {r.inst:4s} {r.cad:5s} g{r.gross:.2f}"
            f"  turn {r.turnover_yr:.3f}x (risk {r.turn_risk_yr:.3f} + sweep {r.turn_sweep_yr:.3f})"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}")

    # ------------------------------------------------------------ D. KEEP counts
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for inst in INSTRUMENTS:
        d = df[df.inst == inst]
        say(f"   inst {inst:5s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~d[x][~d.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for cad in SWEEP_CADENCES + ["n/a"]:
        d = df[df.cad == cad]
        if len(d):
            say(f"   cad {cad:5s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    jt = []
    for bn in BOOKS:
        for g in GROSSES:
            for inst, cad in cells():
                for rung in RUNGS:
                    q = df[(df.book == bn) & (df.gross == g) & (df.inst == inst)
                           & (df.cad == cad) & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                    jt.append(dict(book=bn, gross=g, inst=inst, cad=cad, cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"\n  JOINT both-panel 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by instrument: "
        + "  ".join(f"{i}:{int(jf[jf.inst == i].joint.sum())}/{len(jf[jf.inst == i])}" for i in INSTRUMENTS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.head(12).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} {r.inst:4s} {r.cad:5s} g{r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  turn {r.turnover_yr:.2f}x"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 — the two dials (sweep instrument, sweep cadence) chosen on")
    say("    warm-up..2016-12-31 ONLY, 2017-2026 read ONCE, scored against the COMMITTED (SHY, W). ===")
    wf = []
    for pname in panels:
        for bn in BOOKS:
            for g in GROSSES:
                for rung in RUNGS:
                    d = df[(df.panel == pname) & (df.book == bn) & (df.gross == g)
                           & (df.cost_bps == rung)]
                    cm = d[(d.inst == "SHY") & (d.cad == "W")].iloc[0]
                    for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        pk = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=pname, book=bn, gross=g, cost_bps=rung, chooser=chooser,
                                       pick=f"{pk.inst}/{pk.cad}", full4b=bool(pk.pass4b),
                                       OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                       OOS_MaxDD=pk.OOS_MaxDD, pick_turn=pk.turnover_yr,
                                       committed_turn=cm.turnover_yr,
                                       committed_OOS_Sharpe=cm.OOS_Sharpe,
                                       committed_OOS_CAGR=cm.OOS_CAGR,
                                       base_OOS_Sharpe=pk.base_OOS_Sharpe,
                                       base_OOS_CAGR=pk.base_OOS_CAGR,
                                       spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR,
                                       spy_OOS_MaxDD=pk.spy_OOS_MaxDD))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 books x {len(GROSSES)} gross x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                        {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:              {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED (SHY,W) cell's OOS Sharpe: {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                  {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution: " + "  ".join(
        f"{p}:{int((wfd.pick == p).sum())}" for p in sorted(wfd.pick.unique())))
    say(f"   mean OOS CAGR / Sharpe / MaxDD of the IS-only picks:"
        f" {wfd.OOS_CAGR.mean():.2%} / {wfd.OOS_Sharpe.mean():.4f} / {wfd.OOS_MaxDD.mean():.2%}")
    say(f"   the COMMITTED cell's:                                 "
        f" {wfd.committed_OOS_CAGR.mean():.2%} / {wfd.committed_OOS_Sharpe.mean():.4f}"
        f"  ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f} Sharpe)")
    say(f"   the LIVE RULES v2 baseline's:                         "
        f" {wfd.base_OOS_CAGR.mean():.2%} / {wfd.base_OOS_Sharpe.mean():.4f}")
    say(f"   SPY's:                                                "
        f" {wfd.spy_OOS_CAGR.mean():.2%} / {wfd.spy_OOS_Sharpe.mean():.4f} / {wfd.spy_OOS_MaxDD.mean():.2%}")
    say(f"   mean turnover of the picks {wfd.pick_turn.mean():.3f}x vs the committed {wfd.committed_turn.mean():.3f}x")
    say("\n   panel book  g    bps chooser     | pick       OOS CAGR  OOS Sh  turn/yr | committed OOS Sh / turn")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.book:4s} {r.gross:.2f} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r['pick']:10s} {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f} {r.pick_turn:7.3f} |"
            f" {r.committed_OOS_Sharpe:12.4f} / {r.committed_turn:.3f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
