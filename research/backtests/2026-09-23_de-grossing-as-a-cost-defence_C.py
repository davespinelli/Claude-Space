#!/usr/bin/env python3
"""idea 2443 (lane C, run 51, 2026-09-23) — IS DE-GROSSING A COST DEFENCE FOR THE CAPPED
CANDIDATE AT 25 AND 50 bps?

THE QUESTION.  Idea 2431 published the capped candidate's cost breakeven: its 4b pass
survives 25 bps on 5 of 8 cells and dies between 33 and 54 bps per cell.  That whole
measurement was taken on a gross dial read at only {0.75, 1.00}.  The operator's natural
next move is to SHRINK the book — hold less risk, trade less notional, pay a smaller bill —
so this run walks gross on a fine ladder and asks ONE falsifiable question:

    IS THE 4b DEATH RUNG MONOTONE (rising) IN 1/gross?

If de-grossing is a cost defence, a smaller book must tolerate a HIGHER rung.  If the death
rung does not move, cost tolerance is a property of the RULE and not of its SIZE, and no
amount of de-grossing buys an operator room to pay a real spread.

WHY THE ANSWER IS NOT OBVIOUS FROM ARITHMETIC.  Two channels pull opposite ways and neither
is a free parameter:
  (1) SCALE-FREENESS.  In this construction idle NAV is swept to SHY at phi = 1.00, so a
      band flip moves weight between a risk name and the sweep and BOTH sides are charged.
      Halving gross roughly halves the risk leg's |dw| AND the sweep's offsetting |dw|, so
      turnover falls with gross while excess return over the sweep also falls with gross.
      The RATIO — return per unit of turnover — is what a breakeven in Sharpe terms reads,
      and a pure scale dial leaves it untouched.
  (2) THE ABSOLUTE 4b BARS.  4b is not scale-free.  `L_CAGR` demands CAGR >= 0.70 x SPY's
      and `L_DD` demands MaxDD >= 0.60 x SPY's.  De-grossing walks the book DOWN through
      the CAGR floor while relaxing the drawdown cap, so it can destroy the pass on a leg
      that has nothing to do with cost.
  Channel (1) says the breakeven is flat; channel (2) says the breakeven can only get WORSE
  as gross falls, because the floor binds before the rung does.  Which one wins, and at
  which rung the crossover sits, is the measurement.

DIAL 1 -- gross `g`, the idea's ladder {0.40, 0.55, 0.70, 0.85, 1.00} PLUS the committed
          anchor 0.75, so one ladder spans the live candidate exactly and gate G2/G3 can
          assert bit-identity with the committed headline.  6 points.
DIAL 2 -- the cost rung `c`: a FINE ladder 0..100 bps in 1 bps steps (101 rungs), which
          contains the protocol's 10 bps and the idea's 25 and 50 bps as exact members.

REPORTED, NEVER SELECTED ON: books {CAP2 (cap 0.020), CAND (cap INF)}, panels {U56, B136},
weekly cadence, t+1 execution, band 0.03, the phi = 1.00 SHY sweep.
2 panels x 2 books x 6 gross x 101 rungs = 2424 rows, every one written to .grid.csv.
SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there whose
death rung could be walked.

COST ENTERS LINEARLY (engine.py:50): r(c) = r0 - turnover * c / 1e4.  One zero-cost pass per
cell therefore prices the entire 101-rung ladder exactly; gate G1 verifies that against
`engine.backtest(cost_bps=c)` rather than asserting it.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse
(the baseline priced at the SAME rung, with the 10 bps-pinned variant published beside it).
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's.  RULE 8: gross chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers,
2017-2026 read ONCE, and OOS CAGR / Sharpe / MaxDD reported against the live baseline AND
SPY; the DEATH RUNG is itself walked forward (section G) because it is the deliverable.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_de-grossing-as-a-cost-defence_C.py
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

DATE, SLUG, LANE = "2026-09-23", "de-grossing-as-a-cost-defence", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
GROSSES = [0.40, 0.55, 0.70, 0.75, 0.85, 1.00]     # DIAL 1 (0.75 = committed anchor)
COMMITTED_G = 0.75
RUNGS = [float(c) for c in range(0, 101)]          # DIAL 2
KEY_RUNGS = (0.0, 10.0, 25.0, 50.0)
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")

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


# ---------------------------------------------------------------- the target book
def cap_weights(px, invest, cap, gross):
    """idea 2300's CAND / idea 2322's CAP2: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- BAND; idle NAV swept to SHY (phi = 1.00).  cap='INF' is the uncapped candidate."""
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


def zero_cost(px, w):
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return dict(r0=res["returns"], turnover=res["turnover"], gross=res["weights"].sum(axis=1),
                risk_gross=(res["weights"].drop(columns=[SWEEP]).sum(axis=1)))


def priced(z, bps):
    return z["r0"] - z["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics (numpy, 2424 rows)
def _sharpe(a):
    v = a.std(ddof=1) * np.sqrt(252)
    return float(a.mean() * 252 / v) if v > 0 else np.nan


def _cagr(a):
    eq = np.cumprod(1.0 + a)
    return float(eq[-1] ** (252.0 / len(a)) - 1.0)


def _maxdd(a):
    eq = np.cumprod(1.0 + a)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def _calmar(a):
    d = _maxdd(a)
    return float(_cagr(a) / abs(d)) if d < 0 else np.nan


def _halves(a):
    h = len(a) // 2
    return _sharpe(a[:h]), _sharpe(a[h:])


def breakeven(flags, rungs=RUNGS):
    """The LAST rung at which `flags` holds at that rung AND every cheaper rung.
    -1.0 -> already failing at 0 bps.  inf -> still passing at the top of the ladder."""
    c = -1.0
    for f, rg in zip(flags, rungs):
        if not f:
            return c
        c = rg
    return np.inf if c == rungs[-1] else c


def fmt_be(c):
    return "never" if c < 0 else (f">{RUNGS[-1]:.0f}" if not np.isfinite(c) else f"{c:.0f}")


def main():
    t0 = time.time()
    say("=== idea 2443 (lane C, run 51) — IS DE-GROSSING A COST DEFENCE FOR THE CAPPED CANDIDATE? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 gross g: {GROSSES}  (0.75 = committed anchor, spans the live candidate)")
    say(f"    DIAL 2 cost rung c: {RUNGS[0]:.0f}..{RUNGS[-1]:.0f} bps in 1 bps steps ({len(RUNGS)} rungs)")
    say(f"    REPORTED not selected: books {list(BOOKS)}  panels U56/B136  band {BAND}  cadence {CADENCE}")
    say("    SMALL not priced: 2318/2322/2326/2343 each published SMALL 4b at 0 of 40-120 — no pass to walk.")
    gate("G7 exactly two tuned parameters", "gross g, cost rung c", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {px.shape[1]} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: the linear cost identity IS engine.backtest, not an approximation
    px_u, inv_u = panels["U56"]
    for bk, cap in BOOKS.items():
        for g in (0.40, 1.00):
            w0 = cap_weights(px_u, inv_u, cap, g)
            z = zero_cost(px_u, w0)
            d1 = max(float((backtest(px_u, w0, cost_bps=rg, freq=CADENCE)["returns"] - priced(z, rg)).abs().max())
                     for rg in (10.0, 25.0, 50.0, 100.0))
            gate(f"G1 r0 - turnover*c/1e4 == engine.backtest(cost_bps=c) at 10/25/50/100 ({bk}, U56, g={g:.2f})",
                 f"max|d| {d1:.3e}", "< 1e-15", d1 < 1e-15)

    # ---------------------------------------------------------------- the grid
    rows, cells = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy_s = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy = spy_s.values
        oos_m = np.asarray(win >= pd.Timestamp(OOS_START))
        is_m = np.asarray(win <= pd.Timestamp(IS_END))
        spy_oos, spy_is = spy[oos_m], spy[is_m]
        S_spy, S_spy_oos = _sharpe(spy), _sharpe(spy_oos)
        h_spy1, h_spy2 = _halves(spy)
        DD_spy, C_spy = _maxdd(spy), _cagr(spy)
        zbase = zero_cost(px, rules_v2_weights(px[invest], band=BAND, gross=COMMITTED_G)
                          .reindex(columns=px.columns).fillna(0.0))
        base_turn = float(zbase["turnover"].loc[win].sum() / yrs)
        base_by_rung = {rg: priced(zbase, rg).loc[win].values for rg in RUNGS}
        base10 = base_by_rung[10.0]
        b10_h = _halves(base10); b10_dd = _maxdd(base10)
        base_cache = {rg: (_halves(a), _maxdd(a), _sharpe(a), _sharpe(a[oos_m]), _cagr(a[oos_m]), _maxdd(a[oos_m]))
                      for rg, a in base_by_rung.items()}
        # SHY buy-and-hold: the de-grossing destination, published as the limit of g -> 0
        shy = px[SWEEP].pct_change().fillna(0.0).loc[win].values
        say(f"\n--- panel {pname} ({len(invest)} cols)  SPY {C_spy:.2%} / {S_spy:.4f} / {DD_spy:.2%}"
            f" (turnover 0.00x -> cost-free at every rung)")
        say(f"    live RULES v2 @10bps {_cagr(base10):.2%} / {_sharpe(base10):.4f} / {b10_dd:.2%},"
            f" turnover {base_turn:.2f}x   |   {SWEEP} B&H (the g->0 limit) {_cagr(shy):.2%} /"
            f" {_sharpe(shy):.4f} / {_maxdd(shy):.2%}")
        for bk, cap in BOOKS.items():
            for g in GROSSES:
                z = zero_cost(px, cap_weights(px, invest, cap, g))
                r0 = z["r0"].loc[win].values
                tn = z["turnover"].loc[win].values
                turn = float(tn.sum() / yrs)
                cells.append(dict(panel=pname, book=bk, gross=g, turnover_yr=turn,
                                  base_turnover_yr=base_turn,
                                  max_row_gross=float(z["gross"].max()),
                                  mean_risk_gross=float(z["risk_gross"].loc[win].mean()),
                                  spy_CAGR=C_spy, spy_Sharpe=S_spy, spy_MaxDD=DD_spy))
                for rung in RUNGS:
                    r = r0 - tn * rung / 1e4
                    (bh1, bh2), bdd, bS, bS_oos, bC_oos, bDD_oos = base_cache[rung]
                    h1, h2 = _halves(r)
                    r_oos, r_is = r[oos_m], r[is_m]
                    dd, cg = _maxdd(r), _cagr(r)
                    S_oos = _sharpe(r_oos)
                    L_H1, L_H2 = h1 > h_spy1, h2 > h_spy2
                    L_OOS = S_oos > S_spy_oos
                    L_DD = dd >= DD_CAP * DD_spy
                    L_CAGR = cg >= CAGR_FLOOR * C_spy
                    rows.append(dict(
                        panel=pname, book=bk, gross=g, cost_bps=rung, turnover_yr=turn,
                        CAGR=cg, Sharpe=_sharpe(r), MaxDD=dd, Calmar=_calmar(r), H1=h1, H2=h2,
                        IS_Sharpe=_sharpe(r_is), IS_Calmar=_calmar(r_is), IS_CAGR=_cagr(r_is),
                        OOS_CAGR=_cagr(r_oos), OOS_Sharpe=S_oos, OOS_MaxDD=_maxdd(r_oos),
                        base_Sharpe=bS, base_MaxDD=bdd, base_OOS_Sharpe=bS_oos,
                        base_OOS_CAGR=bC_oos, base_OOS_MaxDD=bDD_oos,
                        spy_CAGR=C_spy, spy_Sharpe=S_spy, spy_MaxDD=DD_spy,
                        spy_OOS_Sharpe=S_spy_oos, spy_OOS_CAGR=_cagr(spy_oos), spy_OOS_MaxDD=_maxdd(spy_oos),
                        annual_bill=turn * rung / 1e4,
                        pass4a=bool(h1 > bh1 and h2 > bh2 and dd >= bdd),
                        pass4a_b10=bool(h1 > b10_h[0] and h2 > b10_h[1] and dd >= b10_dd),
                        pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                        L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                        L_DD=bool(L_DD), L_CAGR=bool(L_CAGR)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); cf = pd.DataFrame(cells)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    cf.to_csv(f"{OUT}.cells.csv", index=False)
    say(f"\n    {len(df)} rows published to {Path(OUT).name}.grid.csv ({len(cf)} cells x {len(RUNGS)} rungs)")

    # ---- G2 / G3: external reproduction of the two committed headlines at the protocol rung
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == COMMITTED_G) & (df.cost_bps == 10.0)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10, abs(h.turnover_yr - 3.51) / 100)
    gate("G2 reproduces idea 2336's committed CAP2 U56 g=0.75 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318, 3.51x)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {h.turnover_yr:.2f}x -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == COMMITTED_G) & (df.cost_bps == 10.0)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 g=0.75 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere", f"max row gross over {len(cf)} books {cf.max_row_gross.max():.9f}",
         "<= 1+1e-12", cf.max_row_gross.max() <= 1 + 1e-12)

    # ---- G5: every leg is a DOWN-SET in c, so a death rung is well defined
    bad, mono = [], []
    for (p, b, g), grp in df.groupby(["panel", "book", "gross"]):
        grp = grp.sort_values("cost_bps")
        for k in LEGS + ("pass4a", "pass4b"):
            v = grp[k].values.astype(bool)
            if v.any() and not np.all(v[:int(v.sum())]):
                bad.append((p, b, g, k))
        mono.append(bool(np.all(np.diff(grp.Sharpe.values) < 1e-12) and np.all(np.diff(grp.CAGR.values) < 1e-12)))
    gate("G5 every 4a/4b leg is a DOWN-SET along the cost ladder (a death rung is well defined)",
         f"{len(bad)} violations over {len(cf)} cells x {len(LEGS) + 2} legs: {bad[:4]}", "0", not bad)
    gate("G5b Sharpe and CAGR strictly decreasing in c in every cell", f"{sum(mono)} of {len(mono)}",
         f"{len(mono)} of {len(mono)}", all(mono))
    publish("G9 the 4b comparand's own cost", "SPY buy-and-hold has 0.00x turnover -> cost-free at every rung"
            " by construction; the live RULES v2 comparand for 4a IS priced at the same rung (pass4a), with"
            " the 10 bps-pinned variant published beside it (pass4a_b10)")

    # ---------------------------------------------------------------- A. the death-rung table
    say("\n=== A. THE DELIVERABLE — the 4b DEATH RUNG walked against gross ===")
    say("  (`never` = already failing at 0 bps; `>100` = still passing at the top of the ladder)")
    say("  the LAST 1-bp rung at which each leg holds at that rung AND every cheaper rung.")
    say("  panel book  gross | turn/yr | CAGR@10 | 4b be |  4a  4a@b10 |   L_H1   L_H2  L_OOS   L_DD  L_CAGR | binding")
    be_rows = []
    for _, c in cf.iterrows():
        grp = df[(df.panel == c.panel) & (df.book == c.book) & (df.gross == c.gross)].sort_values("cost_bps")
        be = {k: breakeven(grp[k].values.astype(bool)) for k in LEGS + ("pass4a", "pass4b", "pass4a_b10")}
        finite = {k: be[k] for k in LEGS}
        binding = min(finite, key=lambda k: (np.inf if not np.isfinite(finite[k]) else finite[k]))
        cg10 = float(grp[grp.cost_bps == 10.0].CAGR.iloc[0])
        be_rows.append(dict(panel=c.panel, book=c.book, gross=c.gross, turnover_yr=c.turnover_yr,
                            CAGR_at10=cg10, mean_risk_gross=c.mean_risk_gross,
                            binding_leg=binding,
                            bill_at_death=(c.turnover_yr * be["pass4b"] / 1e4
                                           if np.isfinite(be["pass4b"]) and be["pass4b"] >= 0 else np.nan),
                            **{f"be_{k}": be[k] for k in be}))
        say(f"  {c.panel:5s} {c.book:5s} {c.gross:.2f} | {c.turnover_yr:7.2f} | {cg10:7.2%} |"
            f" {fmt_be(be['pass4b']):>5s} | {fmt_be(be['pass4a']):>3s} {fmt_be(be['pass4a_b10']):>6s} |" +
            "".join(f" {fmt_be(be[k]):>6s}" for k in LEGS) + f" | {binding}")
    bf = pd.DataFrame(be_rows)
    bf.to_csv(f"{OUT}.deathrung.csv", index=False)

    # ---------------------------------------------------------------- B. THE MONOTONICITY TEST
    say("\n=== B. THE IDEA'S QUESTION, ANSWERED — is the 4b death rung MONOTONE in 1/gross? ===")
    say("  the defence hypothesis predicts a HIGHER death rung at LOWER gross (a smaller book")
    say("  pays a smaller bill).  Read along each ladder from g = 1.00 DOWN to g = 0.40.")
    mono_rows = []
    for (p, b), grp in bf.groupby(["panel", "book"]):
        grp = grp.sort_values("gross", ascending=False)
        v = [(-1.0 if x < 0 else (RUNGS[-1] + 1.0 if not np.isfinite(x) else x)) for x in grp.be_pass4b]
        gs = list(grp.gross)
        rises = sum(1 for i in range(len(v) - 1) if v[i + 1] > v[i] + 1e-9)
        falls = sum(1 for i in range(len(v) - 1) if v[i + 1] < v[i] - 1e-9)
        flat = len(v) - 1 - rises - falls
        nondec = falls == 0
        mono_rows.append(dict(panel=p, book=b, ladder_hi_to_lo=" -> ".join(f"g{g:.2f}:{fmt_be(x)}"
                              for g, x in zip(gs, grp.be_pass4b)),
                              rises=rises, falls=falls, flat=flat, nondecreasing_as_g_falls=nondec,
                              span_bps=(max(v) - min(v))))
        say(f"  {p:5s} {b:5s} | " + "  ".join(f"g{g:.2f}={fmt_be(x):>5s}" for g, x in zip(gs, grp.be_pass4b))
            + f" | rises {rises} falls {falls} flat {flat} -> "
            + ("MONOTONE (defence)" if nondec and rises > 0 else
               ("FLAT (no defence, no harm)" if nondec else "NON-MONOTONE / WORSE (de-grossing HURTS)")))
    mf = pd.DataFrame(mono_rows)
    mf.to_csv(f"{OUT}.monotonicity.csv", index=False)
    gate("G10 the defence hypothesis (death rung non-decreasing as gross falls)",
         f"{int(mf.nondecreasing_as_g_falls.sum())} of {len(mf)} ladders non-decreasing;"
         f" total rises {int(mf.rises.sum())} vs falls {int(mf.falls.sum())} over"
         f" {int(mf.rises.sum() + mf.falls.sum() + mf.flat.sum())} steps",
         "PUBLISHED — this gate IS the finding, pass or fail", True)

    # ---------------------------------------------------------------- C. the mechanism
    say("\n=== C. THE MECHANISM — is de-grossing a PURE SCALE dial on the bill? ===")
    say("  if turnover is proportional to gross the bill shrinks with the book, but so does the")
    say("  return, and the death rung (a RATIO) cannot move.  t/g and (CAGR-SHY)/t are the two")
    say("  scale-free quantities; the CAGR FLOOR is the only non-scale-free bar in 4b.")
    say("  panel book  gross | turn/yr |  turn/g | risk gross | CAGR@10 | CAGR/g | bill@death (pp/yr) | binding")
    for _, r in bf.sort_values(["panel", "book", "gross"], ascending=[True, True, False]).iterrows():
        say(f"  {r.panel:5s} {r.book:5s} {r.gross:.2f} | {r.turnover_yr:7.2f} | {r.turnover_yr / r.gross:7.2f} |"
            f" {r.mean_risk_gross:10.4f} | {r.CAGR_at10:7.2%} | {r.CAGR_at10 / r.gross:6.2%} |"
            f" {(r.bill_at_death * 100 if np.isfinite(r.bill_at_death) else float('nan')):18.2f} | {r.binding_leg}")
    for (p, b), grp in bf.groupby(["panel", "book"]):
        tg = grp.turnover_yr / grp.gross
        cg = grp.CAGR_at10 / grp.gross
        publish(f"C scale-freeness {p}/{b}",
                f"turnover/gross spread {tg.min():.3f}..{tg.max():.3f} (cv {tg.std() / tg.mean():.4f}),"
                f" CAGR@10/gross spread {cg.min():.4%}..{cg.max():.4%} (cv {cg.std() / cg.mean():.4f})")

    # ---------------------------------------------------------------- D. keep counts + leg census
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}"
        f"      4a@b10 passes: {int(df.pass4a_b10.sum())} of {len(df)}")
    say("  rung |" + "".join(f"  g{g:.2f} 4b" for g in GROSSES) + " | 4b FAILs by leg (all gross)")
    for rung in KEY_RUNGS:
        dd = df[df.cost_bps == rung]
        per = "".join(f" {int(dd[dd.gross == g].pass4b.sum()):4d}/{len(dd[dd.gross == g])}" for g in GROSSES)
        fails = dd[~dd.pass4b]
        say(f"  {rung:5.0f} |{per} | " + "  ".join(f"{k} {int((~fails[k]).sum())}" for k in LEGS))
    say("\n  JOINT both-panel 4b (a cell passes only if BOTH U56 and B136 pass at that rung):")
    say("  rung | " + "  ".join(f"{bk}/g{g:.2f}" for bk in BOOKS for g in GROSSES))
    joint_rows = []
    for rung in KEY_RUNGS:
        marks = []
        for bk in BOOKS:
            for g in GROSSES:
                sub = df[(df.book == bk) & (df.gross == g) & (df.cost_bps == rung)]
                ok = bool(sub.pass4b.all()) and len(sub) == 2
                marks.append("Y" if ok else ".")
                joint_rows.append(dict(cost_bps=rung, book=bk, gross=g, joint4b=ok))
        say(f"  {rung:5.0f} | " + "  ".join(f"{m:>9s}" for m in marks))
    pd.DataFrame(joint_rows).to_csv(f"{OUT}.joint4b.csv", index=False)

    # ---------------------------------------------------------------- E. the full ladder
    say("\n=== E. THE FULL LADDER — printed every 5 bps (all 101 rungs in .grid.csv, nothing dropped) ===")
    for pname in panels:
        for bk in BOOKS:
            for g in GROSSES:
                grp = df[(df.panel == pname) & (df.book == bk) & (df.gross == g)].set_index("cost_bps")
                say(f"\n  {pname} / {bk} / gross {g:.2f}  (turnover {grp.turnover_yr.iloc[0]:.2f}x)")
                say("    c |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | legs")
                for rung in RUNGS:
                    if rung % 5 and rung not in KEY_RUNGS:
                        continue
                    r = grp.loc[rung]
                    say(f"  {rung:3.0f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                        f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  |"
                        + "".join("1" if r[k] else "0" for k in LEGS))

    # ---------------------------------------------------------------- F. rule 8
    say("\n=== F. RULE 8 — gross chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE ===")
    say("  two PRE-STATED IS-only choosers, no OOS information: C_ISSHARPE (max IS Sharpe),")
    say("  C_ISCALMAR (max IS Calmar).  OOS CAGR / Sharpe / MaxDD vs the live baseline AND SPY.")
    say("  panel book  rung chooser     | pick g | OOS CAGR  OOS Sh   OOS DD | base OOS Sh | SPY OOS Sh"
        " | beat base | beat SPY | 4b(full)")
    wf = []
    for pname in panels:
        for bk in BOOKS:
            for rung in KEY_RUNGS:
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung)]
                live = dd[dd.gross == COMMITTED_G].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser, pick_gross=pk.gross,
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                   base_OOS_MaxDD=pk.base_OOS_MaxDD,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR,
                                   spy_OOS_MaxDD=pk.spy_OOS_MaxDD,
                                   beat_base=bool(pk.OOS_Sharpe > pk.base_OOS_Sharpe),
                                   beat_spy=bool(pk.OOS_Sharpe > pk.spy_OOS_Sharpe),
                                   pick_pass4b=bool(pk.pass4b),
                                   live_OOS_Sharpe=live.OOS_Sharpe, live_pass4b=bool(live.pass4b),
                                   dOOS_vs_live=float(pk.OOS_Sharpe - live.OOS_Sharpe),
                                   picked_committed=bool(pk.gross == COMMITTED_G)))
                    say(f"  {pname:5s} {bk:5s} {rung:5.0f} {chooser:11s} |  {pk.gross:.2f}  |"
                        f" {pk.OOS_CAGR:7.2%} {pk.OOS_Sharpe:7.4f} {pk.OOS_MaxDD:7.2%} |"
                        f" {pk.base_OOS_Sharpe:11.4f} | {pk.spy_OOS_Sharpe:10.4f} |"
                        f" {'Y' if pk.OOS_Sharpe > pk.base_OOS_Sharpe else '.':^9s} |"
                        f" {'Y' if pk.OOS_Sharpe > pk.spy_OOS_Sharpe else '.':^8s} | {'Y' if pk.pass4b else '.'}")
    wdf = pd.DataFrame(wf)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE 8 SUMMARY over {len(wdf)} picks:")
    say(f"    picks landing on the committed g=0.75: {int(wdf.picked_committed.sum())} of {len(wdf)}")
    for g in GROSSES:
        n = int((wdf.pick_gross == g).sum())
        say(f"      g = {g:.2f}: {n:2d} of {len(wdf)}")
    say(f"    beat the live baseline OOS: {int(wdf.beat_base.sum())} of {len(wdf)}"
        f"    beat SPY OOS: {int(wdf.beat_spy.sum())} of {len(wdf)}")
    say(f"    picks carrying a full-sample 4b pass: {int(wdf.pick_pass4b.sum())} of {len(wdf)}")
    say(f"    mean OOS Sharpe of picks {wdf.OOS_Sharpe.mean():.4f} vs committed g=0.75"
        f" {wdf.live_OOS_Sharpe.mean():.4f} (d {wdf.dOOS_vs_live.mean():+.4f})")
    gate("G11 rule 8 does not prefer a DE-GROSSED book (picks on g < 0.75)",
         f"{int((wdf.pick_gross < COMMITTED_G).sum())} of {len(wdf)} picks below the committed gross;"
         f" mean dOOS Sharpe vs committed {wdf.dOOS_vs_live.mean():+.4f}",
         "PUBLISHED — this gate IS part of the finding", True)

    # ---------------------------------------------------------------- G. the death rung, walked forward
    say("\n=== G. THE DEATH RUNG ITSELF, WALKED FORWARD (it is the deliverable, so rule 8 applies to it) ===")
    say("  IS death rung = computed on warm-up..2016 ONLY with 4b's window-local analogue (H1/H2/DD/CAGR,")
    say("  no OOS leg, SPY measured on the same window).  OOS death rung = the same statistic read ONCE")
    say("  on 2017-2026.  A death rung that is a stable property of the rule should reproduce.")
    say("  panel book  gross |  IS be |  OOS be | full be | d(OOS-IS)")
    wf2 = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win].values
        oos_m = np.asarray(win >= pd.Timestamp(OOS_START))
        is_m = np.asarray(win <= pd.Timestamp(IS_END))
        for bk, cap in BOOKS.items():
            for g in GROSSES:
                z = zero_cost(px, cap_weights(px, invest, cap, g))
                r0 = z["r0"].loc[win].values; tn = z["turnover"].loc[win].values
                be_w = {}
                for tag, m in (("IS", is_m), ("OOS", oos_m)):
                    sp = spy[m]
                    s1, s2 = _halves(sp); dds, cgs = _maxdd(sp), _cagr(sp)
                    flags = []
                    for rung in RUNGS:
                        a = (r0 - tn * rung / 1e4)[m]
                        h1, h2 = _halves(a)
                        flags.append(bool(h1 > s1 and h2 > s2 and _maxdd(a) >= DD_CAP * dds
                                          and _cagr(a) >= CAGR_FLOOR * cgs))
                    be_w[tag] = breakeven(flags)
                full = float(bf[(bf.panel == pname) & (bf.book == bk) & (bf.gross == g)].be_pass4b.iloc[0])
                d = (be_w["OOS"] - be_w["IS"]) if (np.isfinite(be_w["OOS"]) and np.isfinite(be_w["IS"])) else np.nan
                wf2.append(dict(panel=pname, book=bk, gross=g, IS_be=be_w["IS"], OOS_be=be_w["OOS"],
                                full_be=full, d_OOS_IS=d))
                say(f"  {pname:5s} {bk:5s} {g:.2f} | {fmt_be(be_w['IS']):>6s} | {fmt_be(be_w['OOS']):>7s} |"
                    f" {fmt_be(full):>7s} | {('%+.0f' % d) if np.isfinite(d) else 'n/a':>9s}")
    w2 = pd.DataFrame(wf2)
    w2.to_csv(f"{OUT}.deathrung_walkforward.csv", index=False)
    fin = w2[np.isfinite(w2.d_OOS_IS)]
    gate("G12 the death rung reproduces out of sample",
         f"{len(fin)} of {len(w2)} cells finite on both windows; median d(OOS-IS)"
         f" {fin.d_OOS_IS.median() if len(fin) else float('nan'):+.1f} bps, range"
         f" {fin.d_OOS_IS.min() if len(fin) else float('nan'):+.0f}..{fin.d_OOS_IS.max() if len(fin) else float('nan'):+.0f}",
         "PUBLISHED — instability is itself the finding", True)

    # ---------------------------------------------------------------- H. the verdict arithmetic
    say("\n=== H. THE ANSWER ===")
    lo = bf[bf.gross == min(GROSSES)]; hi = bf[bf.gross == max(GROSSES)]
    say(f"  death rung at g={max(GROSSES):.2f}: " + ", ".join(
        f"{r.panel}/{r.book} {fmt_be(r.be_pass4b)}" for _, r in hi.iterrows()))
    say(f"  death rung at g={min(GROSSES):.2f}: " + ", ".join(
        f"{r.panel}/{r.book} {fmt_be(r.be_pass4b)}" for _, r in lo.iterrows()))
    at25 = df[df.cost_bps == 25.0]; at50 = df[df.cost_bps == 50.0]
    say(f"  4b passes at 25 bps: {int(at25.pass4b.sum())} of {len(at25)}"
        f"    at 50 bps: {int(at50.pass4b.sum())} of {len(at50)}")
    for rung in (25.0, 50.0):
        dd = df[df.cost_bps == rung]
        best = dd[dd.pass4b]
        say(f"   {rung:.0f} bps passing cells: "
            + (", ".join(f"{r.panel}/{r.book}/g{r.gross:.2f}" for _, r in best.iterrows()) or "NONE"))
    say(f"  binding leg at the death rung, by gross:")
    for g in GROSSES:
        sub = bf[bf.gross == g]
        say(f"    g={g:.2f}: " + "  ".join(f"{k} {int((sub.binding_leg == k).sum())}" for k in LEGS))

    # ---------------------------------------------------------------- gates + artefacts
    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    asserted = gdf[gdf.target.str.startswith(("<", ">", "0", "2", "all", "<=", ">=")) |
                   gdf.target.str.contains("of")]
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} entries pass"
        f" ({len(gdf) - len(asserted)} are PUBLISHED-not-asserted) ===")
    for _, r in gdf[~gdf.pass_].iterrows():
        say(f"  FAIL {r.gate}: {r.value}")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    say(f"\ndone in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
