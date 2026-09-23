#!/usr/bin/env python3
"""idea 2351 (lane cloud, run 37, 2026-09-23) — does a MINIMUM HOLDING PERIOD cut the CAPPED
candidate's 3.51x TURNOVER where the DRIFT BAND could not?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` (`CAND`: every name INSIDE the 200d +/-3%
band held at `gross / N_in` of NAV, idle NAV swept to SHY) as the record's standing 4b
KEEP-candidate; idea 2322 added a 2.0% per-name cap (`CAP2`).  TURNOVER IS THE ONLY STATED
BLOCKER ON ITS ADOPTION: CAP2 runs at 3.51 turns/yr against the live book's 1.77.

Idea 2328 KILLED the weight-drift no-trade band as the fix — at 100% held-set fidelity it
removes only 3.51 -> 3.07 turns/yr, and every deep cut sits at broken fidelity — but it
attacked the WEIGHTS while leaving the IN/OUT SET free to churn every week.  The other half
of the turnover bill is the SET: a name that crosses the 200d band twice in a fortnight is
bought and sold twice.  A HOLD FLOOR attacks exactly that half:

    a name admitted at decision day t cannot be dropped before t + m trading days, even if
    the 200d band gates it OUT.  The forced hold is carried at its capped weight
    (per-name weight = min(gross / N_eff, cap), N_eff = the effective held set) and the
    residual still sweeps to SHY at phi = 1.00.

DIAL 1 -- hold floor m {0, 10, 21, 42, 63} trading days.  m = 0 IS CAP2 exactly (gate G1),
          so one ladder spans the known book.  The ladder tops out at one quarter, beyond
          which the weekly cadence is no longer the thing being damped.
DIAL 2 -- gross g {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: book {CAP2 (cap 0.02), CAND (cap INF)}, panels {U56, B136},
4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence, band 0.03, t+1 execution, the SHY sweep.
5 x 2 x 2 x 2 = 40 books, every one published at every rung = 160 rows.
SMALL is NOT priced and the reason is stated rather than buried: ideas 2318 / 2322 / 2326 /
2343 each published SMALL's 4b pass count at 0 of 40-120, so there is no pass there to keep.

THE IDEA'S OWN PREMISE IS TESTED, NOT ASSUMED.  "A hold floor cuts SET churn" is a claim with
a cost attached: the floor forces the book to hold names the 200d band has gated OUT, i.e. it
DELIBERATELY breaks held-set fidelity (unlike 2328's band, where broken fidelity was a
defect).  Section E publishes, at every m: realised turnover, held-set fidelity against m=0,
the FORCED-HOLD SHARE (held cells the band says should be OUT), mean names held, and mean
gross — so the reader can see exactly what the turnover saving is bought with.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse)
and 4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x
SPY's).  RULE 8: (m, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only
choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_minimum-holding-period-on-the-capped-candidate_cloud.py
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
from engine import backtest, rebalance_mask                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "minimum-holding-period-on-the-capped-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
HOLDS = [0, 10, 21, 42, 63]
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": "INF"}
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
SWEEP = "SHY"
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


# ---------------------------------------------------------------- the books
def cap_weights(px, invest, cap, gross):
    """idea 2322's CAP2 / idea 2300's CAND, verbatim from the committed lane-B script."""
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


def hold_state(px, invest, m):
    """The effective held set under a hold floor of m trading days.  Decisions are taken on
    `engine.rebalance_mask` days (the days whose weights engine.backtest applies at t+1) and
    the set is carried unchanged between them, so the matrix handed to engine.backtest is
    constant inside each week exactly as the book is."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    dec = rebalance_mask(px.index, CADENCE).values.copy()
    dec[0] = True
    inbv, prv = inb.values, pr.values
    n, k = inbv.shape
    state = np.zeros((n, k), dtype=bool)
    forced_m = np.zeros((n, k), dtype=bool)
    held = np.zeros(k, dtype=bool)
    admit = np.full(k, -10**9, dtype=np.int64)
    n_forced_dec = 0
    for i in range(n):
        if dec[i]:
            tgt = inbv[i]
            forced = held & (~tgt) & ((i - admit) < m) & prv[i]
            eff = tgt | forced
            newly = eff & ~held
            admit = np.where(newly, i, admit)
            held, cur_forced = eff, forced
            n_forced_dec += int(forced.sum())
        state[i] = held
        forced_m[i] = cur_forced if dec[i] else forced_m[i - 1]
    return (pd.DataFrame(state, index=px.index, columns=q.columns),
            pd.DataFrame(forced_m, index=px.index, columns=q.columns), inb, n_forced_dec)


def hold_weights(px, invest, cap, gross, m):
    st, fc, inb, nfd = hold_state(px, invest, m)
    neff = st.sum(axis=1).replace(0, np.nan)
    per = gross / neff
    c = pd.Series(np.inf if cap == "INF" else float(cap), index=px.index)
    per = pd.concat([per, c], axis=1).min(axis=1)
    w = st.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w, st, fc, inb, nfd


def run(px, w, freq=CADENCE):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return dict(r0=res["returns"], turnover=res["turnover"], held=res["weights"])


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


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
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


def main():
    t0 = time.time()
    say("=== idea 2351 (lane cloud, run 37) — does a MINIMUM HOLDING PERIOD cut the CAPPED candidate's 3.51x turnover? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 hold floor m {HOLDS} trading days   DIAL 2 gross {GROSSES}")
    say(f"    REPORTED not selected: book {list(BOOKS)}  panels U56/B136  rungs {RUNGS}")
    gate("G8 exactly two tuned parameters", "hold floor m, gross g", "2", True)

    panels = {}
    px_u = load_universe()
    px_b = load_universe(broad=True)
    for nm, px in (("U56", px_u), ("B136", px_b)):
        invest = list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} columns, {len(px)} rows", ">= 10y", yrs >= 10)
        win = px.index[WARMUP:]
        dead = [c for c in px.columns if px[c].loc[win].notna().sum() == 0]
        publish(f"G9 all-NaN columns in {nm} (idea 2332's MMC defect, carried forward)",
                f"{len(dead)} dead: {dead} -> {len(invest) - len(dead)} priced names")
        gate(f"G6 sweep {SWEEP} priced on every in-window row ({nm})",
             f"non-null {int(px[SWEEP].loc[win].notna().sum())} of {len(win)}", "all",
             bool(px[SWEEP].loc[win].notna().all()))

    # ---- G1: m = 0 IS the committed book, bit-for-bit
    # The held set is carried between decision days, so the two weight matrices agree on the
    # DECISION rows (the only rows engine.backtest reads through its shifted mask) and are
    # free to differ on the rows in between.  Both the decision-row weights AND the priced
    # return series are therefore checked; the second is the binding test.
    dec_u = rebalance_mask(px_u.index, CADENCE)
    for bk, cap in BOOKS.items():
        for g in GROSSES:
            w0, st, fc, inb, nfd = hold_weights(px_u, panels["U56"][1], cap, g, 0)
            wc = cap_weights(px_u, panels["U56"][1], cap, g)
            d1 = float((w0[dec_u.values] - wc[dec_u.values]).abs().max().max())
            r_eng = backtest(px_u, wc, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
            d1b = float((r_eng - priced(run(px_u, w0), HEADLINE_RUNG)).abs().max())
            gate(f"G1 m=0 reproduces the committed book ({bk}, U56, g={g:.2f})",
                 f"max|dw| on decision rows {d1:.3e}; max|dr| vs engine.backtest {d1b:.3e};"
                 f" forced holds {nfd}", "< 1e-12 and 0 forced", d1 < 1e-12 and d1b < 1e-12 and nfd == 0)
            publish(f"G1b off-decision-row weight gap is carried state, not a book difference ({bk}, U56, g={g:.2f})",
                    f"max|dw| over ALL rows {float((w0 - wc).abs().max().max()):.3e}"
                    f" (the hold book carries last week's set; engine reads decision rows only)")

    # ---- G10: no lookahead — the held set up to a cut date is invariant to the future tape
    cut = "2018-06-29"
    px2 = px_u.copy()
    px2.loc[px2.index > cut] = px2.loc[px2.index > cut] * 1.5
    wa, _, _, _, _ = hold_weights(px_u, panels["U56"][1], 0.020, 0.75, 42)
    wb, _, _, _, _ = hold_weights(px2, panels["U56"][1], 0.020, 0.75, 42)
    dlk = float((wa.loc[:cut] - wb.loc[:cut]).abs().max().max())
    gate("G10 no lookahead (future tape x1.5 after 2018-06-29 leaves every earlier weight identical)",
         f"max|dw| on rows <= {cut}: {dlk:.3e}", "< 1e-15", dlk < 1e-15)

    # ---- G12: the floor really is a FLOOR — no held spell shorter than m after admission
    st, fc, inb, nfd = hold_state(px_u, panels["U56"][1], 42)
    dec_idx = np.flatnonzero(rebalance_mask(px_u.index, CADENCE).values)
    sv = st.values
    viol = 0
    for j in range(sv.shape[1]):
        col = sv[:, j]
        starts = np.flatnonzero(col[1:] & ~col[:-1]) + 1
        for s0 in starts:
            e = np.flatnonzero(~col[s0:])
            if len(e):
                spell = e[0]
                if spell < 42 and (s0 + spell) < len(col) - 1:
                    viol += 1
    gate("G12 the floor binds (no held spell shorter than m=42 trading days on U56)",
         f"{viol} spells shorter than 42 days", "0", viol == 0)

    # ---------------------------------------------------------------- the grid
    rows, tr_rows = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname}  ({len(invest)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        for bk, cap in BOOKS.items():
            for gross in GROSSES:
                ref_state = None
                for m in HOLDS:
                    w, st, fc, inb, nfd = hold_weights(px, invest, cap, gross, m)
                    res = run(px, w)
                    hw = res["held"].drop(columns=[SWEEP]).loc[win]
                    state = (hw.values > 1e-12)
                    if m == 0:
                        ref_state = state
                    stv = st.loc[win].values
                    fcv = fc.loc[win].values
                    pos = hw.values[hw.values > 1e-12]
                    tr_rows.append(dict(panel=pname, book=bk, gross=gross, hold=m,
                                        turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                        heldset_fidelity=float((state == ref_state).mean()),
                                        forced_share=float(fcv.sum() / max(1, stv.sum())),
                                        forced_decisions=nfd,
                                        mean_names_in=float(stv.sum(axis=1).mean()),
                                        mean_band_in=float(inb.loc[win].values.sum(axis=1).mean()),
                                        max_name_w=float(pos.max()) if len(pos) else 0.0,
                                        med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                                        mean_gross=float(res["held"].loc[win].sum(axis=1).mean()),
                                        mean_risk_gross=float(hw.values.sum(axis=1).mean()),
                                        mean_sweep_w=float(res["held"][SWEEP].loc[win].mean()),
                                        max_row_sum=float(res["held"].sum(axis=1).max())))
                    for rung in RUNGS:
                        r = priced(res, rung).loc[win]
                        r_oos = r.loc[OOS_START:]
                        h1, h2 = halves(r)
                        rows.append(dict(panel=pname, book=bk, gross=gross, hold=m, cost_bps=rung,
                                         CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                         H1=h1, H2=h2,
                                         IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                         OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                         **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); tf = pd.DataFrame(tr_rows)
    df.to_csv(f"{OUT}.grid.csv", index=False); tf.to_csv(f"{OUT}.turnover.csv", index=False)

    # ---- G2 / G3: external reproduction of the two committed headlines at m = 0
    h = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75) & (df.hold == 0)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    t2 = tf[(tf.panel == "U56") & (tf.book == "CAP2") & (tf.gross == 0.75) & (tf.hold == 0)].iloc[0]
    d2 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10, abs(t2.turnover_yr - 3.51) / 100)
    gate("G2 reproduces idea 2336's committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318, 3.51x)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {t2.turnover_yr:.2f}x -> max|d| {d2:.2e}", "< 1e-3", d2 < 1e-3)
    h3 = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == 0.75) & (df.hold == 0)
            & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(h3.CAGR - 0.125950), abs(h3.Sharpe - 1.1934) / 10, abs(h3.MaxDD + 0.173923),
             abs(h3.OOS_CAGR - 0.138525), abs(h3.OOS_Sharpe - 1.2397) / 10)
    gate("G3 reproduces idea 2300/2332's committed CAND U56 headline (12.5950%/1.1934/-17.3923%, OOS 13.8525%/1.2397)",
         f"read {h3.CAGR:.4%} / {h3.Sharpe:.4f} / {h3.MaxDD:.4%}, OOS {h3.OOS_CAGR:.4%} / {h3.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G4 no leverage anywhere (40 books)", f"max row gross {tf.max_row_sum.max():.9f}",
         "<= 1+1e-9", tf.max_row_sum.max() <= 1 + 1e-9)

    # ---- G5: the dial BITES on turnover, and monotonicity is published not assumed
    bites, mono = [], []
    for (pn, bk, g), grp in tf.groupby(["panel", "book", "gross"]):
        v = grp.sort_values("hold").turnover_yr.values
        bites.append(v[-1] < v[0] - 1e-9)
        mono.append(bool(np.all(np.diff(v) <= 1e-9)))
    gate("G5 the hold dial BITES (turnover at m=63 strictly below m=0)",
         f"{sum(bites)} of {len(bites)} (panel, book, gross) cells", f"{len(bites)} of {len(bites)}", all(bites))
    publish("G5b turnover MONOTONE non-increasing along the whole m ladder",
            f"{sum(mono)} of {len(mono)} cells")
    publish("G11 held-set fidelity is DELIBERATELY broken by this device (unlike idea 2328's band)",
            "min fidelity over all 40 books "
            f"{tf.heldset_fidelity.min():.4%}, max forced-hold share {tf.forced_share.max():.4%}")

    # ---------------------------------------------------------------- A. full grid
    say(f"\n=== A. THE FULL GRID AT THE HEADLINE RUNG ({HEADLINE_RUNG:.0f} bps) — every point, nothing dropped ===")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk}")
            say("    m  gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
                " legs H1/H2/OOS/DD/CAGR | turn/yr  dturn%  fidelity  forced%  N_held")
            for gross in GROSSES:
                for m in HOLDS:
                    r = df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.hold == m)
                           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                    c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross) & (tf.hold == m)].iloc[0]
                    c0 = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross) & (tf.hold == 0)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {m:3d}  {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                        f" {c.turnover_yr:7.2f} {c.turnover_yr / c0.turnover_yr - 1:+7.1%} {c.heldset_fidelity:9.4%}"
                        f" {c.forced_share:8.2%} {c.mean_names_in:7.2f}")

    # ---------------------------------------------------------------- B. keep counts
    say(f"\n=== B. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS (5 m x 2 gross x 2 books x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        dd = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass counts by (book, panel, m) over 4 rungs x 2 gross:")
    for bk in BOOKS:
        for pname in panels:
            line = "  ".join(f"m{m:<2d} {int(df[(df.book == bk) & (df.panel == pname) & (df.hold == m)].pass4b.sum()):2d}/8"
                             for m in HOLDS)
            say(f"    {bk:5s} {pname:5s}  {line}")

    # ---------------------------------------------------------------- C. the adoption question
    say("\n=== C. THE ADOPTION QUESTION: what does each turn of turnover COST? (each m minus m=0) ===")
    for pname in panels:
        for bk in BOOKS:
            for gross in GROSSES:
                say(f"\n  {pname} / {bk} / gross {gross:.2f}")
                say("    m   turn/yr  dturn%  | dCAGR @0bps  @10bps  @25bps  @50bps | dSharpe@10  dOOS_Sh@10  dMaxDD@10 |"
                    " CAGR pp per turn saved @10bps | fidelity forced%")
                ref = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.hold == 0)
                              & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                t0r = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross) & (tf.hold == 0)].iloc[0]
                for m in HOLDS:
                    c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == gross) & (tf.hold == m)].iloc[0]
                    r = {rg: df[(df.panel == pname) & (df.book == bk) & (df.gross == gross) & (df.hold == m)
                                & (df.cost_bps == rg)].iloc[0] for rg in RUNGS}
                    saved = t0r.turnover_yr - c.turnover_yr
                    rate = (ref[10.0].CAGR - r[10.0].CAGR) * 100 / saved if saved > 1e-9 else np.nan
                    say(f"  {m:3d} {c.turnover_yr:8.2f} {c.turnover_yr / t0r.turnover_yr - 1:+7.1%}  |" +
                        "".join(f" {r[rg].CAGR - ref[rg].CAGR:+11.2%}" for rg in RUNGS) +
                        f" | {r[10.0].Sharpe - ref[10.0].Sharpe:+10.4f} {r[10.0].OOS_Sharpe - ref[10.0].OOS_Sharpe:+11.4f}"
                        f" {r[10.0].MaxDD - ref[10.0].MaxDD:+10.2%} | {rate:29.3f} | {c.heldset_fidelity:8.4%} {c.forced_share:7.2%}")

    say("\n  IS THERE ANY m THAT CUTS TURNOVER AND KEEPS THE 4b PASS? (m > 0, same panel/book/gross/rung)")
    for rung in RUNGS:
        keep = []
        for (pn, bk, g), grp in df[df.cost_bps == rung].groupby(["panel", "book", "gross"]):
            z = grp[grp.hold == 0].iloc[0]
            if not z.pass4b:
                continue
            tg = tf[(tf.panel == pn) & (tf.book == bk) & (tf.gross == g)].set_index("hold")
            for _, r in grp[grp.hold > 0].iterrows():
                if r.pass4b and tg.loc[r.hold].turnover_yr < tg.loc[0].turnover_yr - 1e-9:
                    keep.append(f"{pn}/{bk}/g{g:.2f}/m{int(r.hold)} (turn {tg.loc[r.hold].turnover_yr:.2f} vs"
                                f" {tg.loc[0].turnover_yr:.2f}, CAGR {r.CAGR:.2%} vs {z.CAGR:.2%})")
        say(f"   {rung:5.1f} bps: {len(keep)} such cells" + ("  ->  " + "; ".join(keep) if keep else ""))

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 — (m, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                            .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for bk in BOOKS:
            for rung in RUNGS:
                dd = df[(df.panel == pname) & (df.book == bk) & (df.cost_bps == rung)]
                und = dd[(dd.hold == 0) & (dd.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pick = dd.loc[dd[col].idxmax()]
                    tg = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == pick.gross)].set_index("hold")
                    wf.append(dict(panel=pname, book=bk, cost_bps=rung, chooser=chooser,
                                   pick_hold=pick.hold, pick_gross=pick.gross,
                                   pick_turnover=float(tg.loc[pick.hold].turnover_yr),
                                   OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                   pick_pass4b=bool(pick.pass4b), pick_is_m0=bool(pick.hold == 0),
                                   und_OOS_CAGR=und.OOS_CAGR, und_OOS_Sharpe=und.OOS_Sharpe,
                                   beats_undamped_OOS_Sharpe=bool(pick.OOS_Sharpe > und.OOS_Sharpe),
                                   base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos), base_OOS_MaxDD=maxdd(b_oos),
                                   spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                   beats_SPY_OOS_Sharpe=bool(pick.OOS_Sharpe > sharpe(spy_oos))))
                    say(f"  {pname:5s} {bk:5s} {rung:5.1f}bps {chooser:11s} -> m {int(pick.hold):2d} g {pick.gross:.2f} |"
                        f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                        f" turn {tg.loc[pick.hold].turnover_yr:5.2f} | m=0 g0.75 OOS {und.OOS_CAGR:6.2%} /"
                        f" {und.OOS_Sharpe:.4f} | live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} |"
                        f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} | full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on m = 0 (NO hold floor, i.e. the committed book): {int(wfd.pick_is_m0.sum())} of {len(wfd)}")
    say(f"  picks beating the m=0 g=0.75 book's OOS Sharpe: {int(wfd.beats_undamped_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks beating SPY's OOS Sharpe:                 {int(wfd.beats_SPY_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  picks whose full-sample row also passes 4b:     {int(wfd.pick_pass4b.sum())} of {len(wfd)}")
    say("  pick distribution over m: " + "  ".join(f"m{m} {int((wfd.pick_hold == m).sum())}" for m in HOLDS))

    # ---------------------------------------------------------------- E. the premise
    say("\n=== E. THE IDEA'S OWN PREMISE — what is the turnover saving bought WITH? ===")
    say("  (forced% = held (day,name) cells the 200d band says should be OUT; N_band = mean names the band admits)")
    for pname in panels:
        for bk in BOOKS:
            say(f"\n  {pname} / {bk} / gross 0.75")
            say("    m   turn/yr  fidelity  forced%  forced decisions  N_held  N_band  mean risk gross  mean SHY  max w")
            for m in HOLDS:
                c = tf[(tf.panel == pname) & (tf.book == bk) & (tf.gross == 0.75) & (tf.hold == m)].iloc[0]
                say(f"  {m:3d} {c.turnover_yr:8.2f} {c.heldset_fidelity:9.4%} {c.forced_share:8.2%}"
                    f" {int(c.forced_decisions):17d} {c.mean_names_in:7.2f} {c.mean_band_in:7.2f}"
                    f" {c.mean_risk_gross:15.4f} {c.mean_sweep_w:9.2%} {c.max_name_w:6.2%}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .turnover.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
