#!/usr/bin/env python3
"""idea 2431 (lane B, 2026-09-23) — the CAPPED CANDIDATE's COST BREAKEVEN, published as its
own object: at exactly which cost rung does each 4b leg fail, and what turnover would the
book have to reach to clear 50 bps AT ITS CURRENT RETURNS?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  CAP2 runs at 3.51 turns/yr
against the live book's 1.77.  Every device filed against that turnover is now dead — no-trade
band (2328), minimum hold (2351), partial-adjustment damper (2391 / 2404), calendar rota
(2408) — and idea 2395 established that the death at 50 bps is a statement about the cost
LEVEL, not the cost convention.  What the record has never published is the BREAKEVEN itself.

WHY IT IS WORTH ONE RUN.  Every future turnover device has to clear an adoption bar, and
right now that bar is re-derived by re-running the whole family each time one is filed.  The
bar is a NUMBER.  Cost enters `engine.backtest` exactly linearly:

    r(c) = r0 - turnover * c / 1e4          (engine.py:50, verified as gate G1)

so ONE zero-cost pass per book prices the entire ladder, and — the identity this run turns
into the deliverable — scaling TURNOVER by `lam` at rung `c` is arithmetically identical to
leaving turnover alone and moving to rung `lam * c`:

    r0 - (lam * turnover) * c / 1e4  ==  r0 - turnover * (lam * c) / 1e4

Therefore the breakeven RUNG and the breakeven TURNOVER are the same measurement in two
units, and `T* = T_now * c*_4b / 50` is the exact turnover a device must deliver to make this
book survive 50 bps at unchanged returns.  Gate G8 checks that identity numerically against
an independently computed lam-ladder rather than asserting it.

DIAL 1 -- cost rung `c`, a FINE ladder: 0..100 bps in 1 bps steps (101 rungs).
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
weekly cadence, band 0.03, t+1 execution, SHY sweep at phi = 1.00.
2 panels x 2 books x 2 gross x 101 rungs = 808 rows, every one published.
SMALL is NOT priced, and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there whose
breakeven could be measured.

THE COST CONVENTION IS MADE EXPLICIT, NOT ASSUMED.  SPY buy-and-hold has NO turnover in this
construction, so the 4b comparand is cost-free at every rung by construction; the live RULES
v2 baseline DOES turn over, so 4a is judged with the baseline priced at the SAME rung as the
candidate (primary) and, published beside it, with the baseline pinned at the protocol's
10 bps (`pass4a_b10`).  Section D reports how much of the 4b breakeven is an artifact of the
benchmark being free.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: `gross` chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR) at every rung, then 2017-2026 read ONCE; and, because the
deliverable IS a breakeven, the breakeven is ITSELF walked forward (section F) — computed on
IS only and re-read on OOS only, so the record learns whether the adoption bar is stable.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_cost-rung-breakeven-of-the-capped-candidate_B.py
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

DATE, SLUG, LANE = "2026-09-23", "cost-rung-breakeven-of-the-capped-candidate", "B"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
RUNGS = [float(c) for c in range(0, 101)]          # DIAL 1: 1 bps steps, 0..100
GROSSES = [0.75, 1.00]                             # DIAL 2
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
PROTOCOL_RUNG, TARGET_RUNG = 10.0, 50.0
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
    """idea 2322's CAP2 / idea 2300's CAND: w_i = min(gross / N_in, cap) on names INSIDE the
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
    """One pass at cost_bps = 0; every rung is then arithmetic (engine.py:50)."""
    res = backtest(px, w, cost_bps=0.0, freq=CADENCE)
    return dict(r0=res["returns"], turnover=res["turnover"],
                gross=res["weights"].sum(axis=1))


def priced(z, bps):
    return z["r0"] - z["turnover"] * bps / 1e4


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
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR))


def window_legs(r, spy):
    """4b's window-local analogue (no OOS leg): used ONLY by section F's IS-vs-OOS
    breakeven stability read, never by the headline verdict."""
    h1, h2 = halves(r)
    s1, s2 = halves(spy)
    return bool(h1 > s1 and h2 > s2 and maxdd(r) >= DD_CAP * maxdd(spy)
                and cagr(r) >= CAGR_FLOOR * cagr(spy))


def breakeven(flags, rungs=RUNGS):
    """The LAST rung at which `flags` holds at that rung AND at every cheaper rung.
    -1.0 -> already failing at 0 bps.  np.inf -> still passing at the top of the ladder."""
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
    say("=== idea 2431 (lane B, run 47) — the CAPPED CANDIDATE's COST BREAKEVEN as its own object ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 cost rung c: {RUNGS[0]:.0f}..{RUNGS[-1]:.0f} bps in 1 bps steps ({len(RUNGS)} rungs)"
        f"   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  cap 0.02  band {BAND}")
    gate("G7 exactly two tuned parameters", "cost rung c, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: the linear cost identity IS engine.backtest, not an approximation
    px_u = panels["U56"][0]
    for bk, cap in BOOKS.items():
        w0 = cap_weights(px_u, panels["U56"][1], cap, 0.75)
        z = zero_cost(px_u, w0)
        d1 = max(float((backtest(px_u, w0, cost_bps=rg, freq=CADENCE)["returns"] - priced(z, rg)).abs().max())
                 for rg in (10.0, 25.0, 50.0, 100.0))
        gate(f"G1 r0 - turnover*c/1e4 == engine.backtest(cost_bps=c) at 10/25/50/100 ({bk}, U56, g=0.75)",
             f"max|d| {d1:.3e}", "< 1e-15", d1 < 1e-15)

    # ---------------------------------------------------------------- the grid
    rows, cells, lam_rows = [], [], []
    LAMS = [round(x, 4) for x in np.arange(0.0, 2.0001, 0.005)]
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        spy_is = spy.loc[:IS_END]
        zbase = zero_cost(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                          .reindex(columns=px.columns).fillna(0.0))
        base_turn = float(zbase["turnover"].loc[win].sum() / yrs)
        base10 = priced(zbase, PROTOCOL_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} cols)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"  (turnover 0.00x -> cost-free at every rung)   live RULES v2 @10bps {cagr(base10):.2%} /"
            f" {sharpe(base10):.4f} / {maxdd(base10):.2%}, turnover {base_turn:.2f}x")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                z = zero_cost(px, cap_weights(px, invest, cap, gross))
                turn = float(z["turnover"].loc[win].sum() / yrs)
                cell = dict(panel=pname, book=bk, gross=gross, turnover_yr=turn,
                            base_turnover_yr=base_turn, max_row_gross=float(z["gross"].max()))
                for rung in RUNGS:
                    r = priced(z, rung).loc[win]
                    b = priced(zbase, rung).loc[win]
                    r_oos, r_is = r.loc[OOS_START:], r.loc[:IS_END]
                    lg = legs(r, b, spy, r_oos, spy_oos)
                    h1, h2 = halves(r)
                    p4a_b10 = (h1 > halves(base10)[0]) and (h2 > halves(base10)[1]) and (maxdd(r) >= maxdd(base10))
                    rows.append(dict(panel=pname, book=bk, gross=gross, cost_bps=rung, turnover_yr=turn,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2, IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     base_Sharpe=sharpe(b), base_MaxDD=maxdd(b),
                                     pass4a_b10=bool(p4a_b10),
                                     IS_win_4b=window_legs(r_is, spy_is),
                                     OOS_win_4b=window_legs(r_oos, spy_oos), **lg))
                # --- independent lam-ladder at the 50 bps target rung (G8's comparand)
                lam_pass = []
                for lam in LAMS:
                    r = (z["r0"] - lam * z["turnover"] * TARGET_RUNG / 1e4).loc[win]
                    b = priced(zbase, TARGET_RUNG).loc[win]
                    lam_pass.append(legs(r, b, spy, r.loc[OOS_START:], spy_oos)["pass4b"])
                lam_star = breakeven(lam_pass, LAMS)
                cell["lam_star_at50"] = lam_star
                cells.append(cell)
                lam_rows.append(dict(panel=pname, book=bk, gross=gross, turnover_yr=turn,
                                     lam_star_at50=lam_star,
                                     T_star=(lam_star * turn if np.isfinite(lam_star) and lam_star >= 0 else np.nan)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); cf = pd.DataFrame(cells)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- G2 / G3: external reproduction of the two committed headlines at the protocol rung
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75) & (df.cost_bps == PROTOCOL_RUNG)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10, abs(h.turnover_yr - 3.51) / 100)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318, 3.51x)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {h.turnover_yr:.2f}x -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == 0.75) & (df.cost_bps == PROTOCOL_RUNG)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (8 books)", f"max row gross {cf.max_row_gross.max():.9f}", "<= 1+1e-12",
         cf.max_row_gross.max() <= 1 + 1e-12)

    # ---- G5: every leg is a DOWN-SET in c (once failed, never passes again) -> a breakeven exists
    bad, mono = [], []
    for (p, b, g), grp in df.groupby(["panel", "book", "gross"]):
        grp = grp.sort_values("cost_bps")
        for k in LEGS + ("pass4a", "pass4b"):
            v = grp[k].values.astype(bool)
            if v.any() and not np.all(v[:int(v.sum())]):
                bad.append((p, b, g, k))
        mono.append(bool(np.all(np.diff(grp.Sharpe.values) < 1e-12) and np.all(np.diff(grp.CAGR.values) < 1e-12)))
    gate("G5 every 4a/4b leg is a DOWN-SET along the cost ladder (a breakeven rung is well defined)",
         f"{len(bad)} violations over {len(cf)} cells x {len(LEGS) + 2} legs: {bad[:4]}", "0", not bad)
    gate("G5b Sharpe and CAGR strictly decreasing in c in every cell", f"{sum(mono)} of {len(mono)}",
         f"{len(mono)} of {len(mono)}", all(mono))
    publish("G9 the 4b comparand's own cost", "SPY buy-and-hold turnover 0.00x -> cost-free at every rung"
            " by construction; the live RULES v2 comparand for 4a IS priced at the same rung (pass4a),"
            " with the 10 bps-pinned variant published beside it (pass4a_b10)")

    # ---------------------------------------------------------------- A. the breakeven table
    say("\n=== A. THE DELIVERABLE — the exact 1-bp rung at which each leg LAST holds (bps) ===")
    say("  (`never` = already failing at 0 bps; `>100` = still passing at the top of the ladder)")
    say("  panel book  gross | turn/yr |    4b |    4a  4a@b10 |   L_H1   L_H2  L_OOS   L_DD  L_CAGR | binding leg")
    be_rows = []
    for _, c in cf.iterrows():
        grp = df[(df.panel == c.panel) & (df.book == c.book) & (df.gross == c.gross)].sort_values("cost_bps")
        be = {k: breakeven(grp[k].values.astype(bool)) for k in LEGS + ("pass4a", "pass4b", "pass4a_b10")}
        finite = {k: be[k] for k in LEGS}
        binding = min(finite, key=lambda k: (np.inf if not np.isfinite(finite[k]) else finite[k]))
        be_rows.append(dict(panel=c.panel, book=c.book, gross=c.gross, turnover_yr=c.turnover_yr,
                            lam_star_at50=c.lam_star_at50,
                            T_star_at50=(c.lam_star_at50 * c.turnover_yr
                                         if np.isfinite(c.lam_star_at50) and c.lam_star_at50 >= 0 else np.nan),
                            binding_leg=binding, **{f"be_{k}": be[k] for k in be}))
        say(f"  {c.panel:5s} {c.book:5s} {c.gross:.2f} | {c.turnover_yr:7.2f} | {fmt_be(be['pass4b']):>5s} |"
            f" {fmt_be(be['pass4a']):>5s} {fmt_be(be['pass4a_b10']):>6s} |" +
            "".join(f" {fmt_be(be[k]):>6s}" for k in LEGS) + f" | {binding}")
    bf = pd.DataFrame(be_rows)
    bf.to_csv(f"{OUT}.breakeven.csv", index=False)

    # ---- G8: the rung/turnover identity, checked numerically not asserted
    dd8 = []
    for _, r in bf.iterrows():
        if np.isfinite(r.be_pass4b) and r.be_pass4b >= 0 and np.isfinite(r.lam_star_at50) and r.lam_star_at50 >= 0:
            dd8.append(abs(r.lam_star_at50 * TARGET_RUNG - r.be_pass4b))
    gate("G8 lam* x 50 == the 4b breakeven rung (turnover and cost are the same measurement)",
         f"max|d| {max(dd8):.4f} bps over {len(dd8)} finite cells (ladder steps: 1 bps, lam 0.005 = 0.25 bps)",
         "<= 1.25 bps", (max(dd8) if dd8 else 0.0) <= 1.25)

    # ---------------------------------------------------------------- B. the full ladder
    say("\n=== B. THE FULL COST LADDER — every rung, nothing dropped (printed every 5 bps; all 101 in .grid.csv) ===")
    for pname in panels:
        for bk in BOOKS:
            for gross in GROSSES:
                say(f"\n  {pname} / {bk} / gross {gross:.2f}"
                    f"  (turnover {cf[(cf.panel == pname) & (cf.book == bk) & (cf.gross == gross)].turnover_yr.iloc[0]:.2f}x)")
                say("    c |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | H1/H2/OOS/DD/CAGR")
                grp = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross)].set_index("cost_bps")
                for rung in RUNGS:
                    if rung % 5 and rung not in (PROTOCOL_RUNG, 25.0, TARGET_RUNG):
                        continue
                    r = grp.loc[rung]
                    lg = "".join("1" if r[k] else "0" for k in LEGS)
                    say(f"  {rung:3.0f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                        f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}")

    # ---------------------------------------------------------------- C. keep counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (2 panels x 2 books x 2 gross x {len(RUNGS)} rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}"
        f"      4a@b10 passes: {int(df.pass4a_b10.sum())} of {len(df)}")
    for rung in (0.0, PROTOCOL_RUNG, 25.0, TARGET_RUNG, 100.0):
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):2d}/{len(dd)}   4a {int(dd.pass4a.sum()):2d}/{len(dd)}"
            f"   4b FAILs by leg: " + "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in LEGS))

    # ---------------------------------------------------------------- D. what the free benchmark buys
    say("\n=== D. HOW MUCH OF THE BREAKEVEN IS THE BENCHMARK BEING FREE? ===")
    say("  4a is the same book judged against a comparand that ALSO pays the rung.  If 4a's breakeven")
    say("  sits far above 4b's, the candidate's cost problem is a problem with SPY, not with trading.")
    say("  panel book  gross | 4b be | 4a be (same rung) | 4a be (base pinned @10) | gap 4a-4b")
    for _, r in bf.iterrows():
        a, b = r.be_pass4a, r.be_pass4b
        gap = "n/a" if not (np.isfinite(a) and np.isfinite(b) and a >= 0 and b >= 0) else f"{a - b:+.0f}"
        say(f"  {r.panel:5s} {r.book:5s} {r.gross:.2f} | {fmt_be(b):>5s} | {fmt_be(a):>17s} |"
            f" {fmt_be(r.be_pass4a_b10):>23s} | {gap:>9s}")

    # ---------------------------------------------------------------- E. rule 8
    say("\n=== E. RULE 8 — gross chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        zbase = zero_cost(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                          .reindex(columns=px.columns).fillna(0.0))
        for bk in BOOKS:
            for rung in (0.0, PROTOCOL_RUNG, 25.0, TARGET_RUNG):
                b_oos = priced(zbase, rung).loc[win].loc[OOS_START:]
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung)]
                live = dd[dd.gross == 0.75].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = dd.loc[dd[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser, pick_gross=pick.gross,
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   pick_pass4b=bool(pick.pass4b), pick_L_OOS=bool(pick.L_OOS),
                                   live_gross_OOS_Sharpe=live.OOS_Sharpe,
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_base_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(b_oos)),
                                   beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos))))
                    say(f"  {pname:5s} {bk:5s} {rung:5.1f}bps {chooser:11s} -> gross {pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                        f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                        f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks beating the LIVE baseline's OOS Sharpe: {int(wfd.beats_base_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  rule-8 picks beating SPY's OOS Sharpe:                {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  rule-8 picks whose full-sample row passes 4b:         {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over gross: " + "  ".join(f"g{g:.2f} {int((wfd.pick_gross == g).sum())}" for g in GROSSES))

    # ---------------------------------------------------------------- F. the breakeven itself, walked forward
    say("\n=== F. THE BREAKEVEN WALKED FORWARD — fitted on IS (<=2016) ONLY, re-read on OOS (2017-) ONLY ===")
    say("  (window-local 4b: Sharpe > SPY in both halves OF THAT WINDOW, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's)")
    say("  panel book  gross |  IS breakeven | OOS breakeven |  drift | full-sample 4b breakeven")
    st = []
    for _, c in cf.iterrows():
        grp = df[(df.panel == c.panel) & (df.book == c.book) & (df.gross == c.gross)].sort_values("cost_bps")
        b_is = breakeven(grp.IS_win_4b.values.astype(bool))
        b_oo = breakeven(grp.OOS_win_4b.values.astype(bool))
        b_full = breakeven(grp.pass4b.values.astype(bool))
        dr = "n/a" if not (np.isfinite(b_is) and np.isfinite(b_oo) and b_is >= 0 and b_oo >= 0) else f"{b_oo - b_is:+.0f}"
        st.append(dict(panel=c.panel, book=c.book, gross=c.gross, be_IS=b_is, be_OOS=b_oo, be_full=b_full))
        say(f"  {c.panel:5s} {c.book:5s} {c.gross:.2f} | {fmt_be(b_is):>13s} | {fmt_be(b_oo):>13s} |"
            f" {dr:>6s} | {fmt_be(b_full):>24s}")
    pd.DataFrame(st).to_csv(f"{OUT}.stability.csv", index=False)

    # ---------------------------------------------------------------- G. the adoption bar
    say(f"\n=== G. THE ADOPTION BAR — what turnover must a device deliver to clear {TARGET_RUNG:.0f} bps at CURRENT returns? ===")
    say("  lam* = the largest turnover multiplier at which 4b still passes at 50 bps (independent ladder);")
    say("  T* = lam* x the book's current turnover.  `impossible` = the book fails 4b at 50 bps even at zero turnover cost.")
    say("  panel book  gross | turn/yr now |    lam* |     T* (turns/yr) | required cut")
    for _, r in bf.iterrows():
        if not np.isfinite(r.lam_star_at50) or r.lam_star_at50 < 0:
            say(f"  {r.panel:5s} {r.book:5s} {r.gross:.2f} | {r.turnover_yr:11.2f} |"
                f" {'impossible' if r.lam_star_at50 < 0 else 'unbounded':>7s} | {'-':>17s} | -")
        else:
            say(f"  {r.panel:5s} {r.book:5s} {r.gross:.2f} | {r.turnover_yr:11.2f} | {r.lam_star_at50:7.3f} |"
                f" {r.T_star_at50:17.2f} | {r.T_star_at50 / r.turnover_yr - 1:+12.1%}")
    say(f"\n  live RULES v2 turnover for scale: "
        + "  ".join(f"{p} {cf[cf.panel == p].base_turnover_yr.iloc[0]:.2f}x" for p in panels))

    # ---------------------------------------------------------------- verdict
    say("\n=== VERDICT ===")
    n4b_50 = int(df[df.cost_bps == TARGET_RUNG].pass4b.sum())
    n4b_10 = int(df[df.cost_bps == PROTOCOL_RUNG].pass4b.sum())
    say(f"  4b at the protocol's 10 bps: {n4b_10} of {len(cf)} cells.  4b at 50 bps: {n4b_50} of {len(cf)} cells.")
    say(f"  ANSWERED = {'NO' if n4b_50 == 0 else 'PARTLY'}: the question 'does the 4b pass survive 25 and 50 bps' is")
    say("  answered by the breakeven table in section A, and the adoption bar every future turnover device")
    say("  must clear is published in section G.  This run tunes nothing and proposes no new book: it is a")
    say("  MEASUREMENT of the standing candidate, so its own verdict is neither KEEP nor KILL of a new idea.")
    gp = [g for g in GATES if g["target"] != "published, not asserted"]
    say(f"\n  gates: {sum(g['pass_'] for g in gp)} of {len(gp)} PASS")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    say(f"  wrote {OUT.name}.grid.csv / .breakeven.csv / .walkforward.csv / .stability.csv / .gates.csv / .log.txt")
    say(f"  total {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
