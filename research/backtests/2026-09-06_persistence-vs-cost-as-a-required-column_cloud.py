#!/usr/bin/env python3
"""IDEA 263  persistence-vs-cost-as-a-required-column   (cloud, 2026-09-06)

THE QUESTION
------------
Ideas 260 and 262 both ended on the same observation: a Sharpe difference quoted at ONE
cost rung is not a verdict when the two arms churn at different rates.  Idea 262 proved
the mechanism exactly --

    c* = dSharpe(0) * 1e4 / (T_x/vol_x - T_y/vol_y)          (R^2 0.9989 over 337 points)

-- on NULL arms.  The queue's proposal (idea 263) turns that into a reporting clause:

    any comparison between two arms whose TURNOVERS DIFFER BY MORE THAN 2x must publish
    (i) both turnovers and (ii) the difference at 0 bps beside the quoted rung,
    and the column is back-filled over the leaderboard's turnover-mismatched rows.

A clause is only worth adding to PROTOCOL if it FIRES where verdicts are actually at risk
and STAYS QUIET where they are not.  So this run does not ask "is the ratio big sometimes";
it asks whether `ratio > 2x` is a good TRIGGER.  Three things have to be measured:

  Q2  COVERAGE.  How often is the record's own dial machinery turnover-mismatched at all?
      Census every within-family pair of the record's REAL (non-null) dials -- cadence, n,
      gross, the vol scaler, the eligibility gate, the hysteresis band, ranked-vs-EWall --
      on three panels, and report the whole distribution of turnover ratios.
  Q3  CONSEQUENCE.  For every pair, the EXACT cost rung at which its Sharpe difference
      changes sign (bisection on the derived net series, not an interpolation), and whether
      that rung lands inside the 0-25 bps range the record actually quotes.  A pair whose
      breakeven is inside that range is a pair whose published verdict is a statement about
      the rung, not about the arms.
  Q4  IS 2x THE RIGHT TRIGGER?  Score `ratio > x` as a binary classifier of "breakeven in
      (0, 25] bps" at x in {1.2, 1.4, 2.0, 3.0} (1.2/1.4 are idea 267's pre-registered
      band), against the alternative trigger the law itself implies -- the VOL-NORMALISED
      turnover GAP |T_x/vol_x - T_y/vol_y|, which is the denominator of c* and therefore
      the quantity a rung-sensitivity screen should actually key on.  Full confusion counts
      for every threshold, both triggers, all pairs.

PRE-REGISTERED DECISION RULE  (written before any number of this run was read)
-----------------------------------------------------------------------------
  (a) KEEP AS PROPOSED  -- if `ratio > 2x` fires on a large majority of the pairs whose
      breakeven is inside 0-25 bps AND stays quiet on a large majority of those whose
      breakeven is outside it, the clause is a good screen exactly as the queue wrote it.
  (b) KEEP AMENDED      -- if the ratio is a poor screen but the vol-normalised turnover
      GAP separates the same two sets cleanly, then the clause is right in intent and wrong
      in coordinate: the required column is the gap (or c* itself), not the ratio.
  (c) KILL              -- if turnover-mismatched pairs essentially never flip inside
      0-25 bps, the clause is a column nobody would ever read and PROTOCOL should not
      carry it.
  Any of (a)/(b) is a REPORTING clause only.  This run proposes no book and no RULES
  change; PROTOCOL is not edited by this script (rule 6 -- Sunday review).

DESIGN
------
Idea 78's construction is IMPORTED, not re-implemented: `build_panels`, `eligible_mask`,
`weights_cand` (top-n by the composite key WITHOUT the vol scaler, gross/n each),
`weights_ewall`, `fail_4a`, `fail_4b`; idea 171's vectorised `fast_backtest` is asserted
identical to `engine.backtest` on this run's own weight matrices before it is used.

  PANELS        U56, B136, SMALL439 (the 483-name sub-$2B panel with the 44
                `max_1d_move >= 1.0` tickers dropped -- SURVIVORSHIP: current constituents
                of the screen only, no delistings; never pooled with the large caps).
  BOOKS/panel   24, all at t+1 execution, gate = above-200d AND vol20 < 0.60 unless the
                book IS the gate arm, gross 0.75 unless the book IS the gross arm:
                  FWD{5,10,20,40,60} weekly                       (the n family)
                  FWD{10,20,40} at D / M / Q                      (the cadence family)
                  FWD20 weekly at gross {0.25, 0.50, 1.00}        (the gross family)
                  FWD20 weekly WITH the vol scaler                (the scaler family)
                  FWD20 weekly, gate = none / above-200d only     (the gate family)
                  FWD20 weekly with hysteresis band b = 10 / 20   (the band family)
                  EWALL weekly, gross matched                     (the selection family)
                  RULES v1 (the live book)                        (baseline, not a pair arm)
  PAIRS         46 per panel = 138 total, every one written to `.pairs.csv`.
  COST          `fast_backtest` returns (gross return series, turnover series) and neither
                depends on the rung, so every book is simulated ONCE at 0 bps and any rung
                is derived EXACTLY as r(c) = r(0) - turnover*c/1e4.  The identity is
                asserted against a live `engine.backtest(cost_bps=...)` call in Q1 before
                any result is read.  Reported rungs 0/1/2/5/10/15/25 bps, every book at
                every rung, in `.grid.csv` (504 points).
  BREAKEVEN     dSharpe(c) is scanned on a 0.05-bps ladder over [0, 200] and then bisected
                to 1e-4 bps.  This is EXACT (the derived series is exact), not the law's
                approximation; the law is then scored against it as a by-product.
  WINDOWS       full sample from bar 260, first/second half, IS <= 2016-12-31 chooses,
                OOS >= 2017-01-01 read ONCE (rule 8).

TUNED PARAMETERS (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (5 values, ALL reported)
The dial FAMILY is the hypothesis axis, the cost rung is the reported axis -- the whole
point of the run -- and the trigger threshold is scored over its whole range rather than
picked.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .pairs.csv, .trigger.csv,
.walkforward.csv, .keep.csv
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_persistence-vs-cost-as-a-required-column_cloud"
OUT = ROOT / "research" / "backtests"
P78_STEM = "2026-09-05_candidate-count-vs-dispersion_B"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"

RUNGS = [0, 1, 2, 5, 10, 15, 25]
BASE_RUNG = 10
QUOTED_MAX = 25.0          # the range of rungs the record actually quotes
GROSS = 0.75
FREQ = "W"
NS = [5, 10, 20, 40, 60]
CADENCES = ["D", "W", "M", "Q"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PANELS = ["U56", "B136", "SMALL439"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p78 = _load(P78_STEM, "p78")
p171 = _load(P171_STEM, "p171")
p78.P = P
p171.P = P
fast_backtest = p171.fast_backtest


def fb(px, w, freq):
    """(gross return series at 0 bps, turnover series) -- rung-independent, both of them."""
    z = fast_backtest(px, w, 0.0, freq)
    return z["returns"], z["turnover"]


eligible_mask = p78.eligible_mask
weights_cand = p78.weights_cand
weights_ewall = p78.weights_ewall
fail_4a, fail_4b = p78.fail_4a, p78.fail_4b


# ------------------------------------------------------------------ the books
def gate_mask(px, tradable, kind):
    """kind: 'full' = idea 78's gate; 'ma' = 200d only; 'none' = tradable only."""
    _, above, vol20 = score(px)
    if kind == "full":
        m = (above & (vol20 < 0.60)).copy()
    elif kind == "ma":
        m = above.copy()
    else:
        m = pd.DataFrame(True, index=px.index, columns=px.columns)
        m = m.where(px.notna(), False)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def weights_fwd(px, tradable, n, gross=GROSS, gate="full", vol_scale=False):
    elig = gate_mask(px, tradable, gate)
    s = score(px, vol_scale=vol_scale)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def weights_band(px, tradable, n, band, gross=GROSS, freq=FREQ):
    """Hysteresis: a held name is kept while its rank <= n+band and it is still eligible;
    empty slots are filled by the best-ranked names not already held.  Path-dependent, so
    it is stepped over the SIGNAL days (the last trading day of each period) only."""
    elig = gate_mask(px, tradable, "full")
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    sig = rebalance_mask(px.index, freq)
    cols = list(px.columns)
    W = np.zeros((len(px.index), len(cols)))
    rk = rank.values
    held: list[int] = []
    for i in np.flatnonzero(sig.values):
        r = rk[i]
        # the fresh top-n is EXACTLY idea 78's `rank <= n` selection (ties included), so
        # band = 0 reduces to `weights_cand` by construction rather than by coincidence
        fresh = [int(j) for j in np.argsort(np.where(np.isfinite(r), r, np.inf))
                 if np.isfinite(r[j]) and r[j] <= n]
        keep = [j for j in held if np.isfinite(r[j]) and r[j] <= n + band]
        for j in fresh:
            if len(keep) >= max(n, len(fresh)):
                break
            if j not in keep:
                keep.append(j)
        held = keep
        if held:
            W[i, held] = gross / n
    out = pd.DataFrame(W, index=px.index, columns=cols)
    out.loc[~sig.values, :] = np.nan          # only the signal days carry a decision
    return out.ffill().fillna(0.0)


def book_specs():
    """(name, family, dial-value, weights-builder, cadence).  24 books per panel."""
    B = []
    for n in NS:
        B.append((f"FWD{n}", "N", float(n), lambda px, tr, n=n: weights_fwd(px, tr, n), "W"))
    for n in [10, 20, 40]:
        for f in CADENCES:
            if f == "W":
                continue
            B.append((f"FWD{n}@{f}", f"CADENCE_n{n}", {"D": 1.0, "W": 5.0, "M": 21.0, "Q": 63.0}[f],
                      lambda px, tr, n=n: weights_fwd(px, tr, n), f))
    for g in [0.25, 0.50, 1.00]:
        B.append((f"FWD20g{g:.2f}", "GROSS", g,
                  lambda px, tr, g=g: weights_fwd(px, tr, 20, gross=g), "W"))
    B.append(("FWD20vs", "SCALER", 1.0, lambda px, tr: weights_fwd(px, tr, 20, vol_scale=True), "W"))
    B.append(("FWD20gate-none", "GATE", 0.0, lambda px, tr: weights_fwd(px, tr, 20, gate="none"), "W"))
    B.append(("FWD20gate-ma", "GATE", 1.0, lambda px, tr: weights_fwd(px, tr, 20, gate="ma"), "W"))
    for b in [10, 20]:
        B.append((f"FWD20b{b}", "BAND", float(b),
                  lambda px, tr, b=b: weights_band(px, tr, 20, b), "W"))
    B.append(("EWALL", "SELECTION", 0.0, lambda px, tr: weights_ewall(px, tr), "W"))
    B.append(("RULESv1", "BASELINE", np.nan, lambda px, tr: rules_v1_weights(px), "W"))
    return B


# the within-family pairs.  Cross-family pairs are NOT formed: a pair must differ in one
# dial for "the difference at 0 bps" to mean anything.
def pair_specs():
    pr = []
    for i in range(len(NS)):
        for j in range(i + 1, len(NS)):
            pr.append(("N", f"FWD{NS[i]}", f"FWD{NS[j]}"))
    for n in [10, 20, 40]:
        nm = {f: (f"FWD{n}" if f == "W" else f"FWD{n}@{f}") for f in CADENCES}
        for i in range(len(CADENCES)):
            for j in range(i + 1, len(CADENCES)):
                pr.append((f"CADENCE_n{n}", nm[CADENCES[i]], nm[CADENCES[j]]))
    gs = ["FWD20g0.25", "FWD20g0.50", "FWD20", "FWD20g1.00"]
    for i in range(len(gs)):
        for j in range(i + 1, len(gs)):
            pr.append(("GROSS", gs[i], gs[j]))
    pr.append(("SCALER", "FWD20", "FWD20vs"))
    gt = ["FWD20gate-none", "FWD20gate-ma", "FWD20"]
    for i in range(len(gt)):
        for j in range(i + 1, len(gt)):
            pr.append(("GATE", gt[i], gt[j]))
    bd = ["FWD20", "FWD20b10", "FWD20b20"]
    for i in range(len(bd)):
        for j in range(i + 1, len(bd)):
            pr.append(("BAND", bd[i], bd[j]))
    for n in NS:
        pr.append(("SELECTION", "EWALL", f"FWD{n}"))
    return pr


# --------------------------------------------------------------------- metrics
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def sharpe(r):
    return metrics(r)["Sharpe"]


def moments(g, t):
    """Everything Sharpe(c) needs, for r(c) = g - t*c/1e4.  Exact, closed form:
        mean(r) = mg - mt*k,  var(r) = vg - 2*k*cgt + k^2*vt,   k = c/1e4
    so the whole cost ladder is an algebraic function of five numbers.  ddof = 1 to match
    pandas' `std`, which is what `engine.metrics` uses.  Asserted against `metrics` in Q1."""
    gv, tv = np.asarray(g, float), np.asarray(t, float)
    n = len(gv)
    mg, mt = gv.mean(), tv.mean()
    dg, dt = gv - mg, tv - mt
    return (mg, mt, dg @ dg / (n - 1), dg @ dt / (n - 1), dt @ dt / (n - 1))


def sharpe_at(mo, c):
    mg, mt, vg, cgt, vt = mo
    k = c / 1e4
    var = vg - 2 * k * cgt + k * k * vt
    if var <= 0:
        return np.nan
    return np.sqrt(252.0) * (mg - mt * k) / np.sqrt(var)


def dsharpe(mx, my, c):
    return sharpe_at(mx, c) - sharpe_at(my, c)


def exact_breakeven(mx, my, hi=200.0, step=0.05):
    """Smallest c >= 0 at which dSharpe changes sign.  Ladder then bisection to 1e-6 bps.
    Returns (c*, d0) with c* = nan when the sign never changes on [0, hi]."""
    d0 = dsharpe(mx, my, 0.0)
    prev_c, prev_d = 0.0, d0
    for c in np.arange(step, hi + step, step):
        d = dsharpe(mx, my, float(c))
        if np.isfinite(d) and np.isfinite(prev_d) and (d == 0.0 or np.sign(d) != np.sign(prev_d)):
            lo, hi_, dlo = prev_c, float(c), prev_d
            for _ in range(80):
                mid = 0.5 * (lo + hi_)
                dm = dsharpe(mx, my, mid)
                if np.sign(dm) == np.sign(dlo):
                    lo, dlo = mid, dm
                else:
                    hi_ = mid
                if hi_ - lo < 1e-6:
                    break
            return 0.5 * (lo + hi_), d0
        prev_c, prev_d = float(c), d
    return np.nan, d0


def confusion(flag, truth):
    flag, truth = np.asarray(flag, bool), np.asarray(truth, bool)
    tp = int((flag & truth).sum()); fp = int((flag & ~truth).sum())
    fn = int((~flag & truth).sum()); tn = int((~flag & ~truth).sum())
    prec = tp / (tp + fp) if tp + fp else np.nan
    rec = tp / (tp + fn) if tp + fn else np.nan
    return dict(TP=tp, FP=fp, FN=fn, TN=tn, precision=prec, recall=rec,
                accuracy=(tp + tn) / len(flag) if len(flag) else np.nan,
                fires=int(flag.sum()))


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 263  persistence-vs-cost-as-a-required-column   (cloud, 2026-09-06)")
    P("=" * 118)

    P("\nbuilding idea 78's panels (its own build_panels, imported) ...")
    panels = p78.build_panels()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL439: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} "
      "tradable (SURVIVORSHIP: current constituents of the screen only, no delistings)")
    panels["SMALL439"] = (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk))
    for nm in PANELS:
        px, tr = panels[nm]
        P(f"  {nm:9s} {px.shape[1]:4d} columns, {len(tr):4d} tradable, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")

    # ------------------------------------------------------------------ Q1 controls
    P("\n" + "=" * 118)
    P("Q1  REPRODUCTION CONTROLS, asserted before any result is read")
    P("=" * 118)
    px, tr = panels["U56"]
    w = weights_fwd(px, tr, 20)
    P("\n  [a] weights_fwd(n=20) == idea 78's weights_cand(n=20), element-wise")
    d = float((w - weights_cand(px, tr, 20)).abs().max().max())
    P(f"      max |dw| over the whole U56 matrix = {d:.3e}")
    assert d == 0.0

    P("\n  [b] fast_backtest == engine.backtest  (same weights, same rung, same freq)")
    z = backtest(px, w, cost_bps=10.0, freq=FREQ)
    fz = fast_backtest(px, w, 10.0, FREQ)
    d = float((fz["returns"] - z["returns"]).abs().max())
    dt = float((fz["turnover"] - z["turnover"]).abs().max())
    P(f"      max |dreturn| = {d:.3e}   max |dturnover| = {dt:.3e}")
    assert d < 1e-12 and dt < 1e-12

    P("\n  [c] cost identity: net(c) == gross - turnover*c/1e4, direct vs derived")
    g0, tn0 = fb(px, w, FREQ)
    dmax = 0.0
    for cb in RUNGS:
        direct = backtest(px, w, cost_bps=float(cb), freq=FREQ)["returns"]
        dmax = max(dmax, float((direct - (g0 - tn0 * cb / 1e4)).abs().max()))
    P(f"      max |direct - derived| over rungs {RUNGS} = {dmax:.3e}")
    assert dmax < 1e-12

    P("\n  [d] the closed-form Sharpe(c) used for every breakeven == engine.metrics(net(c))")
    mo = moments(g0, tn0)
    dmax = 0.0
    for cb in [0, 1, 2, 5, 10, 15, 25, 50, 100]:
        dmax = max(dmax, abs(sharpe_at(mo, float(cb)) - sharpe(g0 - tn0 * cb / 1e4)))
    P(f"      max |closed-form - metrics| over 0..100 bps = {dmax:.3e}")
    assert dmax < 1e-10

    P("\n  [e] the hysteresis band at b = 0 is the plain top-n book, on every signal day")
    sig = rebalance_mask(px.index, FREQ)
    d = float((weights_band(px, tr, 20, 0)[sig.values]
               - weights_fwd(px, tr, 20)[sig.values]).abs().max().max())
    P(f"      max |dw| over the {int(sig.sum())} weekly signal days = {d:.3e}")
    assert d < 1e-12

    # ------------------------------------------------------------------ simulate
    P("\n" + "=" * 118)
    P("Q2  THE CORPUS -- 24 books x 3 panels, each simulated ONCE at 0 bps")
    P("=" * 118)
    specs = book_specs()
    sims, grid_rows = {}, []
    for pn in PANELS:
        px, tr = panels[pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = {}
        for nm, fam, dial, fn, freq in specs:
            g, tn = fb(px, fn(px, tr), freq)
            g, tn = g.loc[start:], tn.loc[start:]
            sims[(pn, nm)] = (g, tn, fam, dial, freq)
            if nm == "RULESv1":
                for cb in RUNGS:
                    base[cb] = g - tn * cb / 1e4
        for nm, fam, dial, fn, freq in specs:
            g, tn, fam, dial, freq = sims[(pn, nm)]
            yrs = metrics(g)["Years"]
            for cb in RUNGS:
                r = g - tn * cb / 1e4
                m, mo = metrics(r), metrics(r.loc[OOS_START:])
                h1, h2 = halves(r)
                grid_rows.append(dict(
                    panel=pn, book=nm, family=fam, dial=dial, freq=freq, cost_bps=cb,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    vol=m["Vol"], turnover=float(tn.sum() / yrs),
                    IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                    OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                    fail4a=fail_4a(r, base[cb]),
                    fail4b=fail_4b(r, spy, r.loc[OOS_START:], spy.loc[OOS_START:])))
        P(f"  {pn}: {len(specs)} books simulated   ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(grid_rows)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"\n  .grid.csv = {len(grid)} points (24 books x 3 panels x {len(RUNGS)} rungs), ALL printed below")

    P("\n  annualised turnover by book and panel (the column the clause would require):")
    tt = grid[grid.cost_bps == 0].pivot(index="book", columns="panel", values="turnover")
    P(tt.reindex([s[0] for s in specs]).to_string(float_format=lambda x: f"{x:8.2f}"))

    P("\n  the full grid, every point:")
    P(grid.to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ Q3 pairs
    P("\n" + "=" * 118)
    P("Q3  EVERY WITHIN-FAMILY PAIR: turnover ratio, dSharpe(0), and the EXACT breakeven")
    P("=" * 118)
    prs = pair_specs()
    rows = []
    for pn in PANELS:
        for fam, a, b in prs:
            ga, ta = sims[(pn, a)][0], sims[(pn, a)][1]
            gb, tb = sims[(pn, b)][0], sims[(pn, b)][1]
            ya = metrics(ga)["Years"]
            Ta, Tb = float(ta.sum() / ya), float(tb.sum() / ya)
            va, vb = metrics(ga)["Vol"], metrics(gb)["Vol"]
            mx, my = moments(ga, ta), moments(gb, tb)
            cstar, d0 = exact_breakeven(mx, my)
            d10 = dsharpe(mx, my, 10.0)
            law_den = Ta / va - Tb / vb
            law = d0 * 1e4 / law_den if law_den != 0 else np.inf
            rows.append(dict(
                panel=pn, family=fam, x=a, y=b, T_x=Ta, T_y=Tb,
                ratio=max(Ta, Tb) / min(Ta, Tb) if min(Ta, Tb) > 0 else np.inf,
                vol_x=va, vol_y=vb, gap=Ta / va - Tb / vb, abs_gap=abs(Ta / va - Tb / vb),
                dSharpe_0=d0, dSharpe_10=d10, dSharpe_25=dsharpe(mx, my, 25.0),
                c_star=cstar, c_star_law=law,
                flips_in_quoted=bool(np.isfinite(cstar) and 0.0 < cstar <= QUOTED_MAX),
                sign_flips_0_to_10=bool(np.sign(d0) != np.sign(d10))))
    pairs = pd.DataFrame(rows)
    pairs.to_csv(OUT / f"{STEM}.pairs.csv", index=False)
    P(f"\n  {len(pairs)} pairs ({len(prs)} per panel x 3), ALL printed:")
    P(pairs.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  turnover-ratio distribution by family (max/min of the two annualised turnovers):")
    P(pairs.groupby("family")["ratio"].describe()[["count", "min", "50%", "max"]]
      .to_string(float_format=lambda x: f"{x:.3f}"))
    for thr in (1.2, 1.4, 2.0, 3.0):
        P(f"  pairs with ratio > {thr:.1f}x : {int((pairs.ratio > thr).sum()):3d} / {len(pairs)}")
    P(f"  pairs whose breakeven lands in (0, {QUOTED_MAX:.0f}] bps : "
      f"{int(pairs.flips_in_quoted.sum()):3d} / {len(pairs)}")
    P(f"  pairs whose sign at 0 bps differs from its sign at {BASE_RUNG} bps : "
      f"{int(pairs.sign_flips_0_to_10.sum()):3d} / {len(pairs)}")
    P("\n  by family -- mismatched (>2x) vs rung-sensitive (breakeven in 0-25):")
    fam = pairs.groupby("family").agg(n=("ratio", "size"), gt2x=("ratio", lambda s: int((s > 2).sum())),
                                      flips=("flips_in_quoted", "sum"),
                                      med_ratio=("ratio", "median"),
                                      med_absgap=("abs_gap", "median"))
    P(fam.to_string(float_format=lambda x: f"{x:.3f}"))

    ok = pairs[np.isfinite(pairs.c_star) & np.isfinite(pairs.c_star_law)]
    if len(ok) > 2:
        err = (ok.c_star_law - ok.c_star).abs()
        ss = 1 - ((ok.c_star_law - ok.c_star) ** 2).sum() / ((ok.c_star - ok.c_star.mean()) ** 2).sum()
        P(f"\n  idea 262's law re-scored on THIS run's non-null pairs ({len(ok)} flipping): "
          f"R^2 {ss:.4f}, median |err| {err.median():.3f} bps, 90th pct {err.quantile(0.9):.3f} bps")

    # ------------------------------------------------------------------ Q4 trigger
    P("\n" + "=" * 118)
    P("Q4  IS `ratio > 2x` THE RIGHT TRIGGER?  both candidate triggers scored on the same pairs")
    P("=" * 118)
    truth = pairs.flips_in_quoted.values
    trows = []
    for thr in (1.1, 1.2, 1.4, 1.5, 2.0, 2.5, 3.0, 4.0):
        trows.append(dict(trigger="ratio", threshold=thr, **confusion(pairs.ratio.values > thr, truth)))
    for thr in (0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0):
        trows.append(dict(trigger="abs_gap", threshold=thr, **confusion(pairs.abs_gap.values > thr, truth)))
    # the third candidate: the clause's OWN four numbers, combined the way idea 262's law says.
    # This is not a new measurement -- it is exactly what a reader of the proposed column can
    # compute with a calculator, and it is scored against the same measured truth.
    law_flag = (pairs.c_star_law.values > 0) & (pairs.c_star_law.values <= QUOTED_MAX)
    trows.append(dict(trigger="law_c_star_in_0_25", threshold=QUOTED_MAX, **confusion(law_flag, truth)))
    trig = pd.DataFrame(trows)
    trig.to_csv(OUT / f"{STEM}.trigger.csv", index=False)
    P(f"\n  truth = breakeven in (0, {QUOTED_MAX:.0f}] bps; {int(truth.sum())} of {len(truth)} pairs")
    P(trig.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n  the three triggers head to head at the queue's own threshold and at the best abs_gap cut:")
    for lab, flag in (("ratio > 2.0x", pairs.ratio.values > 2.0),
                      ("abs_gap > 2.0", pairs.abs_gap.values > 2.0),
                      ("abs_gap > 5.0", pairs.abs_gap.values > 5.0),
                      ("law c* in 0-25", law_flag)):
        c = confusion(flag, truth)
        P(f"    {lab:14s} fires {c['fires']:3d}  TP {c['TP']:3d}  FP {c['FP']:3d}  FN {c['FN']:3d}  "
          f"TN {c['TN']:3d}  precision {c['precision']:.3f}  recall {c['recall']:.3f}")

    P("\n  the pairs the ratio MISSES (breakeven in range, ratio <= 2x) -- the clause's blind spot:")
    miss = pairs[(pairs.ratio <= 2.0) & pairs.flips_in_quoted]
    P(miss[["panel", "family", "x", "y", "T_x", "T_y", "ratio", "abs_gap", "dSharpe_0", "c_star"]]
      .to_string(float_format=lambda x: f"{x:.4f}") if len(miss) else "    (none)")
    P("\n  the pairs the ratio FALSELY flags (ratio > 2x, breakeven outside 0-25) -- the noise:")
    fp = pairs[(pairs.ratio > 2.0) & ~pairs.flips_in_quoted]
    P(f"    {len(fp)} pairs; by family: "
      + ", ".join(f"{k} {v}" for k, v in fp.family.value_counts().items()))

    P("\n  WHY the ratio mis-fires -- the GROSS family is the clean counter-example.  Scaling")
    P("  gross scales turnover AND vol together, so T/vol (the denominator of c*) barely")
    P("  moves however large the turnover ratio gets:")
    gr = pairs[pairs.family == "GROSS"][["panel", "x", "y", "T_x", "T_y", "ratio",
                                         "vol_x", "vol_y", "gap", "abs_gap", "c_star"]]
    P(gr.to_string(float_format=lambda x: f"{x:.4f}"))
    P(f"    GROSS pairs: median ratio {gr.ratio.median():.3f}, median |gap| {gr.abs_gap.median():.3f}, "
      f"{int(pairs[(pairs.family == 'GROSS')].flips_in_quoted.sum())} of {len(gr)} flip inside 0-25 bps")

    # ------------------------------------------------------------------ Q5 rule 8
    P("\n" + "=" * 118)
    P("Q5  RULE 8 -- IS <= 2016-12-31 chooses, OOS >= 2017-01-01 read ONCE")
    P("=" * 118)
    P("\n  the selector question the column implies: the record quotes SOME comparisons at")
    P("  0 bps and some at 10 bps.  Does the rung the chooser reads change what it picks,")
    P("  and does that change survive out of sample?")
    wf = []
    for pn in PANELS:
        px, tr = panels[pn]
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        arms = [s[0] for s in specs if s[1] != "BASELINE"]
        for chooser in (0, 10, 25):
            isb = {a: sharpe((sims[(pn, a)][0] - sims[(pn, a)][1] * chooser / 1e4).loc[:IS_END])
                   for a in arms}
            pick = max(isb, key=isb.get)
            g, tn = sims[(pn, pick)][0], sims[(pn, pick)][1]
            r = (g - tn * BASE_RUNG / 1e4).loc[OOS_START:]
            m = metrics(r)
            wf.append(dict(panel=pn, chooser_rung=chooser, pick=pick, IS_Sharpe=isb[pick],
                           OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"],
                           turnover=float(tn.loc[OOS_START:].sum() / m["Years"])))
        for lab, nm in (("ANCHOR FWD20", "FWD20"), ("EWALL", "EWALL"), ("RULESv1", "RULESv1")):
            g, tn = sims[(pn, nm)][0], sims[(pn, nm)][1]
            r = (g - tn * BASE_RUNG / 1e4).loc[OOS_START:]
            m = metrics(r)
            wf.append(dict(panel=pn, chooser_rung=np.nan, pick=lab, IS_Sharpe=np.nan,
                           OOS_Sharpe=m["Sharpe"], OOS_CAGR=m["CAGR"], OOS_MaxDD=m["MaxDD"],
                           turnover=float(tn.loc[OOS_START:].sum() / m["Years"])))
        ms = metrics(spy.loc[OOS_START:])
        wf.append(dict(panel=pn, chooser_rung=np.nan, pick="SPY", IS_Sharpe=np.nan,
                       OOS_Sharpe=ms["Sharpe"], OOS_CAGR=ms["CAGR"], OOS_MaxDD=ms["MaxDD"],
                       turnover=0.0))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  (OOS read at 10 bps in every row; the chooser_rung is what the SELECTOR saw)")
    P(wfd.to_string(float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ Q6 keep paths
    P("\n" + "=" * 118)
    P("Q6  BOTH KEEP PATHS on every (panel, book, rung)")
    P("=" * 118)
    keep = grid[["panel", "book", "family", "cost_bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "OOS_Sharpe", "turnover", "fail4a", "fail4b"]].copy()
    keep["pass4a"] = keep.fail4a == "-"
    keep["pass4b"] = keep.fail4b == "-"
    keep.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  4a passes {int(keep.pass4a.sum())} / {len(keep)}    "
      f"4b passes {int(keep.pass4b.sum())} / {len(keep)}")
    P("\n  4b passes at 10 bps, by panel and book:")
    k10 = keep[(keep.cost_bps == BASE_RUNG) & keep.pass4b]
    P(k10.to_string(float_format=lambda x: f"{x:.4f}") if len(k10) else "    (none)")
    P("\n  binding 4b bar across the 10-bps grid (which clause fails, counted):")
    fails = keep[keep.cost_bps == BASE_RUNG].fail4b.str.split(",").explode()
    P(fails[fails != "-"].value_counts().to_string())

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
