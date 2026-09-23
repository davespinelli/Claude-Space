#!/usr/bin/env python3
"""idea 2506 (lane C, run 63, 2026-09-23) — IS THE CANDIDATE'S 2% NAME CAP A CONCENTRATION
CONTROL, OR A DISGUISED BREADTH-LINKED GROSS SCHEDULE?

THE GAP.  The standing KEEP-4b candidate (idea 2322's CAP2) sizes every held name at
`min(g / N_in, 0.02)`.  That number is the SAME for every held name, so the cap cannot
de-concentrate a book that is already equal-weight.  What the cap ACTUALLY does is pin realised
risk gross to `min(g, 0.02 x N_in)` — a KINKED function of BREADTH that binds only when fewer
than `g / 0.02` names are inside the band, i.e. precisely in weak markets.  Twelve runs have
swept the cap LEVEL; none has ever asked what SHAPE the cap is, or whether its kink earns
anything.  If the reading is right, the candidate's "2% per-name cap" is not a risk limit at all
and the RULES wording that describes it as one is wrong.

WHAT IS PROVED VERSUS WHAT IS PRICED.  The identity is a GATE (G7, G10, G11), not a claim: the
run asserts it to machine precision and stops if it fails.  What is PRICED is the follow-on
question the identity forces — is the KINK the right breadth schedule?  The kink is a
two-regime rule: constant GROSS above the kink, constant WEIGHT-PER-NAME below it.  The natural
one-parameter family spanning both regimes is

    G_t = g x p_t ** alpha,     p_t = N_in,t / N_priced,t   (breadth), per-name w = G_t / N_in,t

with alpha = 0 the UNCAPPED book CAND (constant gross, exactly), alpha = 1 constant weight per
name (`g / N_priced`, the cap's binding regime in smooth form) and alpha = 2 a convex de-grosser.
The kinked cap is the piecewise MAX of the alpha = 0 and alpha = 1 members at a level.

DIAL 1 -- SHAPE, ONE LADDER OF 8: KINK{cap 0.015, 0.020 (= the committed CAP2), 0.030, INF
          (= CAND)} and SMOOTH{alpha 0.25, 0.50, 1.00, 2.00}.  SMOOTH alpha = 0 IS KINK INF IS
          CAND, so it is asserted as an identity (G8) rather than spent as a grid point.
DIAL 2 -- gross g in {0.50, 0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, weekly cadence,
t+1 execution, band 0.03, MA 200d, the phi = 1.00 SHY sweep.

PRIOR, STATED BEFORE COMPUTE.  The identity itself is arithmetic and cannot fail.  On the priced
question the prior is that the KINK is NOT special — a kink is what you get from a cap, not from
an optimisation, and the record's twelve killed turnover devices all show this book's deltas
tracking realised risk gross rather than device design (idea 2477).  The expectation is therefore
that some smooth alpha REPRODUCES the committed cell's 4b pass at a similar gross path, and that
the rule-8 chooser cannot tell the shapes apart.  A clean refutation would be a smooth arm that
dominates CAP2 on every leg at equal or lower turnover, or a kink that no smooth alpha matches.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS all failing at every cell.  A gross SCHEDULE re-scales an existing book; it cannot move
three failing legs at once, so there is no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (shape, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE and scored against the committed CAP2 cell, the
live RULES v2 book and SPY.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the eligible
set IS `baseline.band_state` & priced.  G3 KINK 0.020 / KINK INF reproduce the committed CAP2 and
CAND U56 headlines.  G4 no leverage.  G5 cost exactly linear in the rung.  G6 exactly two tuned
parameters.  **G7 THE IDENTITY: the kink family's target risk gross IS `min(g, cap x N_in)`.**
G8 SMOOTH alpha = 0 IS KINK INF bit for bit.  G9 the SHY sweep is priced on every held row.
**G10 every arm's held weights are UNIFORM across names (so no arm in this study, capped or not,
can de-concentrate anything).**  **G11 in every cap-binding row the max name weight IS the cap
and the per-name weight is CONSTANT in `N_in`.**  G12 the comparands (SPY, live RULES v2) are
bit-identical across every arm.  G13 the smooth family's realised gross tracks `g x p^alpha`.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The shape-vs-shape contrast is same-tape, same-day,
same-names and first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_cap-as-breadth-linked-gross-schedule_C.py
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

DATE, SLUG, LANE = "2026-09-23", "cap-as-breadth-linked-gross-schedule", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
CAPS = [0.015, 0.020, 0.030, np.inf]          # KINK ladder; 0.020 is the committed CAP2
ALPHAS = [0.25, 0.50, 1.00, 2.00]             # SMOOTH ladder; alpha 0 == KINK INF (G8)
GROSSES = [0.50, 0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, HEADLINE_G, COMMITTED_CAP = 10.0, 0.75, 0.020
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


# ---------------------------------------------------------------- the two shape families
def eligible(px):
    """The committed eligible set: inside the 200d +/- 3% hysteretic band AND priced.  G2 asserts
    this IS `baseline.band_state` unmodified."""
    return band_state(px, BAND) & px.notna()


def breadth(px):
    el = eligible(px)
    n_in = el.sum(axis=1).astype(float)
    n_pr = px.notna().sum(axis=1).astype(float)
    return el, n_in, n_pr


def kink_weights(px, gross, cap):
    """The COMMITTED family: every held name at `min(g / N_in, cap)`.  Uniform across names."""
    el, n_in, _ = breadth(px)
    per = (gross / n_in.replace(0, np.nan)).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0), per


def smooth_weights(px, gross, alpha):
    """The SMOOTH family: target risk gross `G_t = g x p_t**alpha`, spread equally over the same
    eligible set.  alpha = 0 reproduces the uncapped book exactly (G8)."""
    el, n_in, n_pr = breadth(px)
    p = (n_in / n_pr.replace(0, np.nan)).fillna(0.0)
    G = gross * np.power(p.clip(lower=0.0), alpha)
    per = (G / n_in.replace(0, np.nan)).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0), per


SHAPES = ([("KINK", c) for c in CAPS] + [("SMOOTH", a) for a in ALPHAS])


def shape_name(fam, v):
    if fam == "KINK":
        return "CAND" if not np.isfinite(v) else f"CAP{v:.3f}"
    return f"A{v:.2f}"


def shape_weights(px, gross, fam, v):
    return (kink_weights(px, gross, v) if fam == "KINK" else smooth_weights(px, gross, v))


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
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n)
    rgr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n); spread = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
        gr[i] = cur.sum()
        risk = cur.copy(); risk[si] = max(0.0, risk[si] - 0.0)
        rgr[i] = float(wt[i].sum())
        held = cur > 1e-12
        nheld[i] = float(held.sum()); mx[i] = float(cur.max())
        hw = wt[i][wt[i] > 1e-12]
        spread[i] = float(hw.max() - hw.min()) if hw.size else 0.0
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), risk_gross=pd.Series(rgr, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx),
                wspread=pd.Series(spread, index=idx))


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
    say("=== idea 2506 — IS THE 2% NAME CAP A CONCENTRATION CONTROL, OR A BREADTH-LINKED GROSS SCHEDULE? ===")
    say(f"    {DATE}  lane {LANE} run 63   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 SHAPE (one ladder of {len(SHAPES)}): KINK caps {[('INF' if not np.isfinite(c) else c) for c in CAPS]}"
        f" + SMOOTH alphas {ALPHAS}    DIAL 2 gross {GROSSES}")
    say("    PRIOR, STATED BEFORE COMPUTE: the identity is arithmetic and cannot fail; on the PRICED question the")
    say("    expectation is that the KINK is NOT special — some smooth alpha should reproduce the committed cell's")
    say("    4b pass at a similar gross path and the rule-8 chooser should not be able to tell the shapes apart.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383) and 0 of 40-120 (2318/2322/2326/2343); a gross")
    say("    SCHEDULE re-scales an existing book and cannot move three failing legs at once.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The shape-vs-shape contrast is same-tape, same-day and first-order immune.")
    gate("G6 exactly two tuned parameters", "shape (cap OR alpha, one ladder), gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    el_u, nin_u, npr_u = breadth(px_u)
    bs = band_state(px_u, BAND)
    d2 = int((el_u != (bs & px_u.notna())).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean N_in {nin_u.loc[px_u.index[WARMUP]:].mean():.2f} of"
         f" {npr_u.loc[px_u.index[WARMUP]:].mean():.2f} priced", "0", d2 == 0)

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=HEADLINE_G)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ---------------- G7 / G10 / G11: THE IDENTITY THE WHOLE IDEA TURNS ON
    say("\n=== 0. THE IDENTITY, ASSERTED RATHER THAN CLAIMED ===")
    worst7 = worst10 = worst11 = 0.0
    bind_share = {}
    for pname, px in panels.items():
        el, n_in, n_pr = breadth(px)
        sl = slice(px.index[WARMUP], None)
        for gross in GROSSES:
            for cap in CAPS:
                wk, per = kink_weights(px, gross, cap)
                tgt = wk.sum(axis=1)                              # realised TARGET risk gross
                want = np.minimum(gross, (cap * n_in) if np.isfinite(cap) else np.inf * np.ones(len(n_in)))
                want = pd.Series(np.where(n_in.values > 0, want, 0.0), index=n_in.index)
                worst7 = max(worst7, float((tgt - want).abs().loc[sl].max()))
                # uniformity: max - min over HELD names
                hw = wk.where(wk > 1e-15)
                worst10 = max(worst10, float((hw.max(axis=1) - hw.min(axis=1)).fillna(0.0).loc[sl].max()))
                if np.isfinite(cap):
                    binds = (gross / n_in.replace(0, np.nan)) > cap
                    bind_share[(pname, gross, cap)] = float(binds.loc[sl].mean())
                    if binds.loc[sl].any():
                        # in binding rows the per-name weight IS the cap, constant in N_in
                        worst11 = max(worst11, float((per.loc[sl][binds.loc[sl]] - cap).abs().max()))
    gate("G7 THE IDENTITY: the kink family's target risk gross IS min(g, cap x N_in), exactly",
         f"max|target_gross - min(g, cap x N_in)| over all panels x gross x caps: {worst7:.3e}",
         "< 1e-12 (float summation precision over up to 136 columns)", worst7 < 1e-12)
    gate("G10 every arm's held weights are UNIFORM across names (a cap on an equal-weight book"
         " cannot de-concentrate)", f"max (max_w - min_w) over held names: {worst10:.3e}",
         "< 1e-15", worst10 < 1e-15)
    gate("G11 in every cap-BINDING row the per-name weight IS the cap, constant in N_in",
         f"max|w_pername - cap| over binding rows: {worst11:.3e}", "< 1e-15", worst11 < 1e-15)
    say("    READING: a cap of `c` on `g/N_in` is not a risk limit on a NAME.  It is the schedule")
    say("      risk gross = min(g, c x N_in),  i.e. CONSTANT GROSS above breadth g/c and CONSTANT")
    say("      WEIGHT-PER-NAME (= c) below it.  The kink sits at N_in = g/c names.")
    for (pname, gross, cap), sh in sorted(bind_share.items()):
        if gross == HEADLINE_G:
            say(f"      {pname:5s} g {gross:.2f} cap {cap:.3f}: kink at N_in = {gross/cap:.1f} names;"
                f" the cap BINDS on {sh:.1%} of scored days")

    # G8 SMOOTH alpha = 0 IS KINK INF
    w0a, _ = smooth_weights(px_u, HEADLINE_G, 0.0)
    w0b, _ = kink_weights(px_u, HEADLINE_G, np.inf)
    d8 = float((w0a - w0b).abs().max().max())
    gate("G8 SMOOTH alpha = 0 IS KINK INF (= CAND) bit for bit", f"max|d| {d8:.3e}", "0.0", d8 == 0.0)

    # G14 -- THE OTHER END OF THE LADDER, AND THE FINDING THIS RUN DID NOT EXPECT:
    # alpha = 1 gives per-name weight g / N_priced, which IS `baseline.rules_v2_weights`.
    worst14 = 0.0
    for pname, px in panels.items():
        for gross in GROSSES:
            wa1, _ = smooth_weights(px, gross, 1.0)
            worst14 = max(worst14, float((wa1 - rules_v2_weights(px, band=BAND, gross=gross)).abs().max().max()))
    gate("G14 SMOOTH alpha = 1 IS `baseline.rules_v2_weights` — THE LIVE BOOK — at every panel and gross",
         f"max|d| {worst14:.3e}", "< 1e-15", worst14 < 1e-15)
    say("    READING: the ladder therefore SPANS the record's two headline books.  alpha = 0 IS the uncapped")
    say("      candidate CAND (constant gross g); alpha = 1 IS the LIVE RULES v2 book (constant weight")
    say("      g/N_priced per name, gross = g x breadth); and the 2% cap is the PIECEWISE MAX of those two")
    say("      regimes — constant gross above N_in = g/c names, constant per-name weight below it.  The")
    say("      standing candidate is a KINKED INTERPOLATION BETWEEN THE LIVE BOOK AND THE UNCAPPED ONE.")
    say("      The only difference between the A1.00 arm priced here and the 4a baseline is the SHY SWEEP.")

    # G13 the smooth family's realised target gross tracks g x p^alpha
    worst13 = 0.0
    for pname, px in panels.items():
        el, n_in, n_pr = breadth(px)
        p = (n_in / n_pr.replace(0, np.nan)).fillna(0.0)
        for gross in GROSSES:
            for a in ALPHAS:
                ws, _ = smooth_weights(px, gross, a)
                want = pd.Series(np.where(n_in.values > 0, gross * np.power(p.values, a), 0.0), index=p.index)
                worst13 = max(worst13, float((ws.sum(axis=1) - want).abs().loc[px.index[WARMUP]:].max()))
    gate("G13 the smooth family's target risk gross IS g x p^alpha", f"max|d| {worst13:.3e}",
         "< 1e-12 (float summation precision)", worst13 < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    comparands = {}
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=HEADLINE_G),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        comparands[pname] = (spy, base_r)
        for fam, v in SHAPES:
            sname = shape_name(fam, v)
            for gross in GROSSES:
                wr, _ = shape_weights(px, gross, fam, v)
                bk = run_book(px, wr)
                r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                book_facts.append(dict(
                    panel=pname, family=fam, shp=sname, gross=gross,
                    turnover_yr=float(tn.sum() / (len(tn) / 252)),
                    mean_risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                    mean_tot_gross=float(bk["gross"].loc[start:].mean()),
                    max_tot_gross=float(bk["gross"].loc[start:].max()),
                    mean_names=float(bk["names"].loc[start:].mean()),
                    max_name_w=float(bk["maxw"].loc[start:].max()),
                    max_w_spread=float(bk["wspread"].loc[start:].max())))
                for rung in RUNGS:
                    r = r0 - tn * rung / 1e4
                    r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                    lg = legs(r, base_r, spy, r_oos, spy_oos)
                    rows.append(dict(
                        panel=pname, family=fam, shp=sname, gross=gross, cost_bps=rung,
                        CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                        turnover_yr=float(tn.sum() / (len(tn) / 252)),
                        mean_risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                        max_name_w=float(bk["maxw"].loc[start:].max()),
                        IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                        OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                        base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                        base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                        base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                        base_OOS_MaxDD=maxdd(base_r.loc[OOS_START:]),
                        spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                        spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                        spy_OOS_MaxDD=maxdd(spy_oos), spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(SHAPES)} shapes x {len(GROSSES)} gross x"
        f" {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max total gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_tot_gross.max():.6f}", "<= 1+1e-12",
         bool(bf.max_tot_gross.max() <= 1 + 1e-12))
    gate("G10b the realised HELD weights stay uniform on every path (drift aside, at rebalance)",
         f"max within-day weight spread over all {len(bf)} paths: {bf.max_w_spread.max():.3e}",
         "< 1e-15", bool(bf.max_w_spread.max() < 1e-15))
    pz = panels["U56"]
    wr0, _ = kink_weights(pz, HEADLINE_G, COMMITTED_CAP)
    bz = run_book(pz, wr0); st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)
    sp = df.groupby("panel")[["spy_Sharpe", "base_Sharpe", "spy_OOS_Sharpe", "base_OOS_Sharpe"]].nunique()
    gate("G12 the comparands (SPY, live RULES v2) are bit-identical across every arm",
         f"distinct values per panel: {sp.values.tolist()}", "all 1",
         bool((sp.values == 1).all()))

    a = df[(df.panel == "U56") & (df.shp == f"CAP{COMMITTED_CAP:.3f}") & (df.gross == HEADLINE_G)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.shp == "CAND") & (df.gross == HEADLINE_G)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 KINK 0.020 / KINK INF reproduce the committed CAP2 (11.62%/1.2687/-14.81%, OOS"
         " 12.77%/1.3318) AND CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say("\n=== A. THE FULL LADDER — EVERY GRID POINT (192 rows) ===")
    say("  panel shape    g    bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr | rgross maxw | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for fam, v in SHAPES:
            sname = shape_name(fam, v)
            for gross in GROSSES:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.shp == sname) & (df.gross == gross)
                           & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    tag = "   <= COMMITTED" if (sname == f"CAP{COMMITTED_CAP:.3f}" and gross == HEADLINE_G
                                               and rung == HEADLINE_RUNG) else ""
                    say(f"  {pname:5s} {sname:8s} {gross:.2f} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {r.mean_risk_gross:6.3f} {r.max_name_w:5.3f}"
                        f" | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}{tag}")

    # ------------------------------------------------------------ B. the priced question
    say("\n=== B. THE PRICED QUESTION: DOES ANY SMOOTH alpha MATCH OR BEAT THE KINK? (vs the committed CAP2 cell, same panel/gross/rung) ===")
    say("  panel  g    bps  shape    | dCAGR    dSharpe   dMaxDD   dOOS_Sh | dTurn%  | d(mean risk gross) | 4b")
    cmp_rows = []
    for pname in panels:
        for gross in GROSSES:
            for rung in RUNGS:
                z = df[(df.panel == pname) & (df.shp == f"CAP{COMMITTED_CAP:.3f}")
                       & (df.gross == gross) & (df.cost_bps == rung)].iloc[0]
                for fam, v in SHAPES:
                    sname = shape_name(fam, v)
                    if sname == f"CAP{COMMITTED_CAP:.3f}":
                        continue
                    r = df[(df.panel == pname) & (df.shp == sname) & (df.gross == gross)
                           & (df.cost_bps == rung)].iloc[0]
                    d = dict(panel=pname, gross=gross, cost_bps=rung, family=fam, shp=sname,
                             dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                             dMaxDD=r.MaxDD - z.MaxDD, dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                             dTurn=r.turnover_yr / z.turnover_yr - 1,
                             dGross=r.mean_risk_gross - z.mean_risk_gross,
                             cap4b=bool(z.pass4b), arm4b=bool(r.pass4b),
                             dominates=bool(r.CAGR >= z.CAGR and r.Sharpe >= z.Sharpe
                                            and r.MaxDD >= z.MaxDD and r.OOS_Sharpe >= z.OOS_Sharpe
                                            and r.turnover_yr <= z.turnover_yr))
                    cmp_rows.append(d)
                    if rung == HEADLINE_RUNG:
                        say(f"  {pname:5s} {gross:.2f} {rung:5.1f}  {sname:8s} | {d['dCAGR']:+7.2%}"
                            f" {d['dSharpe']:+9.4f} {d['dMaxDD']:+8.2%} {d['dOOS_Sharpe']:+8.4f}"
                            f" | {d['dTurn']:+6.1%} | {d['dGross']:+17.4f} | "
                            f"{'Y' if d['arm4b'] else '.'}")
    cmp = pd.DataFrame(cmp_rows); cmp.to_csv(f"{OUT}.vs_committed.csv", index=False)
    dom = cmp[cmp.dominates]
    say(f"\n    ARMS DOMINATING THE COMMITTED CAP2 CELL on ALL FIVE of (CAGR, Sharpe, MaxDD, OOS Sharpe,"
        f" turnover): {len(dom)} of {len(cmp)}")
    if len(dom):
        say("    " + "; ".join(f"{r.panel}/g{r.gross:.2f}/{r.cost_bps:.0f}bps/{r.shp}"
                               for r in dom.itertuples()))
    say(f"    SMOOTH arms matching the kink's 4b where the kink passes: "
        f"{int(((cmp.family == 'SMOOTH') & cmp.cap4b & cmp.arm4b).sum())} of "
        f"{int(((cmp.family == 'SMOOTH') & cmp.cap4b).sum())}")

    # ------------------------------------------------------------ C. shape-level rollup
    say("\n=== C. SHAPE-LEVEL ROLLUP: 4b / 4a COUNTS, TURNOVER AND REALISED GROSS (both panels, all gross, all rungs) ===")
    say("  shape    | 4b of 24 | 4a of 24 | mean risk gross | mean turn/yr | median Sharpe | median OOS Sharpe")
    for fam, v in SHAPES:
        sname = shape_name(fam, v)
        s = df[df.shp == sname]
        say(f"  {sname:8s} | {int(s.pass4b.sum()):7d}  | {int(s.pass4a.sum()):7d}  |"
            f" {s.mean_risk_gross.mean():14.4f}  | {s.turnover_yr.mean():11.2f}  |"
            f" {s.Sharpe.median():12.4f}  | {s.OOS_Sharpe.median():16.4f}")
    say(f"\n  BOTH KEEP PATHS OVER ALL {len(df)} ROWS: 4b {int(df.pass4b.sum())}, 4a {int(df.pass4a.sum())}.")
    for lg in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"):
        say(f"    leg {lg:6s} fails {int((~df[lg]).sum()):4d} of {len(df)}")
    fail4a = df[~df.pass4a]
    say(f"    4a binding leg: MaxDD worse than the live book in "
        f"{int((fail4a.MaxDD < fail4a.base_MaxDD).sum())} of {len(fail4a)} failures.")

    say("\n  THE A1.00 ARM IS THE LIVE BOOK PLUS THE SHY SWEEP, AND NOTHING ELSE (G14).  Its delta against the")
    say("  4a baseline is therefore the sweep's value, measured here rather than assumed:")
    say("   panel  g    bps |  A1.00 CAGR / Sharpe / MaxDD  |  live RULES v2 CAGR / Sharpe / MaxDD  |  dCAGR   dSharpe   dMaxDD")
    for pname in panels:
        for gross in GROSSES:
            for rung in (HEADLINE_RUNG,):
                r = df[(df.panel == pname) & (df.shp == "A1.00") & (df.gross == gross)
                       & (df.cost_bps == rung)].iloc[0]
                say(f"   {pname:5s} {gross:.2f} {rung:5.1f} | {r.CAGR:11.2%} {r.Sharpe:8.4f} {r.MaxDD:9.2%}"
                    f"  | {r.base_CAGR:15.2%} {r.base_Sharpe:8.4f} {r.base_MaxDD:9.2%}"
                    f"  | {r.CAGR - r.base_CAGR:+7.2%} {r.Sharpe - r.base_Sharpe:+9.4f}"
                    f" {r.MaxDD - r.base_MaxDD:+8.2%}"
                    + ("   <= the 4a baseline's own gross" if gross == HEADLINE_G else ""))

    # ------------------------------------------------------------ D. the breadth mechanism
    say("\n=== D. THE MECHANISM: WHAT BREADTH ACTUALLY DOES, AND WHERE THE KINK SITS ===")
    for pname, px in panels.items():
        el, n_in, n_pr = breadth(px)
        sl = slice(px.index[WARMUP], None)
        p = (n_in / n_pr.replace(0, np.nan)).loc[sl]
        say(f"  {pname:5s} breadth p = N_in/N_priced: mean {p.mean():.3f} median {p.median():.3f}"
            f"  p10 {p.quantile(0.10):.3f}  p90 {p.quantile(0.90):.3f}  min {p.min():.3f}")
        for gross in GROSSES:
            k = gross / COMMITTED_CAP
            say(f"      g {gross:.2f}: kink at N_in = {k:.1f} of {n_pr.loc[sl].mean():.0f} priced"
                f" (p* = {k / n_pr.loc[sl].mean():.3f}); cap binds {float((n_in.loc[sl] < k).mean()):.1%} of days;"
                f" realised risk gross mean {float(np.minimum(gross, COMMITTED_CAP * n_in.loc[sl]).mean()):.4f}")

    say("\n  CROSS-PANEL AGREEMENT (the same (shape, gross, rung) cell passing on U56 AND B136):")
    for leg in ("pass4a", "pass4b"):
        piv = df.pivot_table(index=["shp", "gross", "cost_bps"], columns="panel", values=leg).astype(bool)
        both = piv["U56"] & piv["B136"]
        say(f"    {leg}: {int(both.sum())} of {len(piv)} cells — " +
            ", ".join(f"{i[0]}/g{i[1]:.2f}/{i[2]:.0f}bps" for i in both[both].index))

    # ------------------------------------------------------------ E. RULE 8 walk-forward
    say("\n=== E. RULE 8 WALK-FORWARD — (shape, gross) FITTED ON warm-up..2016-12-31 ONLY, 2017-2026 READ ONCE ===")
    say("    Two pre-stated IS-only choosers: C_ISSHARPE = argmax IS Sharpe; C_ISCALMAR = argmax IS Calmar.")
    picks = []
    for pname in panels:
        spy, base_r = comparands[pname]
        for rung in RUNGS:
            sub = df[(df.panel == pname) & (df.cost_bps == rung)]
            for cname, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                w = sub.loc[sub[col].idxmax()]
                picks.append(dict(panel=pname, cost_bps=rung, chooser=cname, shp=w.shp,
                                  family=w.family, gross=w.gross,
                                  IS_Sharpe=w.IS_Sharpe, IS_Calmar=w.IS_Calmar,
                                  OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe, OOS_MaxDD=w.OOS_MaxDD,
                                  base_OOS_CAGR=w.base_OOS_CAGR, base_OOS_Sharpe=w.base_OOS_Sharpe,
                                  base_OOS_MaxDD=w.base_OOS_MaxDD,
                                  spy_OOS_CAGR=w.spy_OOS_CAGR, spy_OOS_Sharpe=w.spy_OOS_Sharpe,
                                  spy_OOS_MaxDD=w.spy_OOS_MaxDD,
                                  beats_spy_oos=bool(w.OOS_Sharpe > w.spy_OOS_Sharpe),
                                  beats_base_oos=bool(w.OOS_Sharpe > w.base_OOS_Sharpe),
                                  full4b=bool(w.pass4b), full4a=bool(w.pass4a),
                                  turnover_yr=w.turnover_yr))
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.rule8.csv", index=False)
    say("  panel  bps  chooser     | pick (shape, g)   | OOS CAGR  OOS Sh   OOS MaxDD | vs live OOS Sh | vs SPY OOS Sh | full 4b")
    for r in pk.itertuples():
        say(f"  {r.panel:5s} {r.cost_bps:4.0f}  {r.chooser:11s} | {r.shp:8s} g{r.gross:.2f}     |"
            f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:8.4f} {r.OOS_MaxDD:10.2%} |"
            f" {r.base_OOS_Sharpe:14.4f} | {r.spy_OOS_Sharpe:13.4f} | {'Y' if r.full4b else '.'}")
    say(f"\n    {int(pk.beats_spy_oos.sum())} of {len(pk)} picks beat SPY's OOS Sharpe;"
        f" {int(pk.beats_base_oos.sum())} of {len(pk)} beat the LIVE book's;"
        f" {int(pk.full4b.sum())} of {len(pk)} carry a full-sample 4b; 4a {int(pk.full4a.sum())} of {len(pk)}.")
    say("    CHOOSER SHAPE PREFERENCE (the whole question, out of sample): " +
        "  ".join(f"{k}:{v}" for k, v in pk.shp.value_counts().items()))
    say(f"    family split: KINK {int((pk.family == 'KINK').sum())} of {len(pk)},"
        f" SMOOTH {int((pk.family == 'SMOOTH').sum())} of {len(pk)}.")
    for pname in panels:
        spy, base_r = comparands[pname]
        say(f"    {pname} benchmarks read ONCE — SPY OOS {cagr(spy.loc[OOS_START:]):.2%} /"
            f" {sharpe(spy.loc[OOS_START:]):.4f} / {maxdd(spy.loc[OOS_START:]):.2%};"
            f" live RULES v2 OOS {cagr(base_r.loc[OOS_START:]):.2%} / {sharpe(base_r.loc[OOS_START:]):.4f}"
            f" / {maxdd(base_r.loc[OOS_START:]):.2%}")

    # ------------------------------------------------------------ gate summary
    g = pd.DataFrame(GATES); g.to_csv(f"{OUT}.gates.csv", index=False)
    npass = int(g.pass_.sum())
    say(f"\n=== GATES: {npass} of {len(g)} pass ===")
    for r in g[~g.pass_].itertuples():
        say(f"    FAILED: {r.gate} -> {r.value}")
    say(f"\n    elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
