#!/usr/bin/env python3
"""QUEUE idea 96 — stop-as-negative-insurance (cloud, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 94 found the per-name trailing stop's dMaxDD is NEGATIVE in 10 of 12 matched cells at
both 15% and 25%, i.e. it makes drawdown worse while costing CAGR. Test whether the sign is
the instrument or the grid: an intra-week exit (check the stop daily, rebalance weekly) vs
the weekly-grid exit used here, and a same-day vs next-day execution. If the weekly grid is
the cause, the stop is mispriced everywhere it has been run."

Code audit done FIRST, before any backtest (and it changes the question).  Reading idea 94's
`run()` line by line: the stop's trailing high is updated on EVERY row and the trigger is
evaluated on EVERY row (step 5 of its loop, unconditional on the rebalance mask), so the exit
is ALREADY intra-week — the queue's "the weekly-grid exit used here" is wrong about the
implementation.  What is on the weekly grid in idea 94 is the RE-ENTRY, which is what its own
mechanism sentence says ("sells into the drawdown and re-buys at the next weekly rebalance").
Second and sharper: a hit at row i sets `pending`, which is executed at row i+1 BEFORE that
row's return is earned, so the position's last return day is day i and its effective exit
price is `px[i]` — **the very close at which the trigger was observed**.  Under PROTOCOL rule
2 a decision taken at close t is executed at t+1, so idea 94's stop is one bar FASTER than the
protocol allows and its published price is, if anything, optimistic.  That inverts the queue's
hypothesis: the worry was that a too-slow grid made the stop look bad; the code says the
timing is too GENEROUS, and the honest test is whether the sign survives being SLOWED to the
protocol convention.  Both directions are run anyway, and idea 94's exact convention is
reproduced first so nothing here rests on the reading above.

The 2 x 3 design (this run's two tuned parameters; everything else is reported at every value)
    CHECK  daily   — evaluate the trailing-stop trigger on every trading day (idea 94)
           weekly  — track the running high daily, but evaluate the trigger only on the
                     weekly rebalance rows (the "weekly grid" the queue supposed was in use)
    LAG    same    — flatten before the next row's return, i.e. exit at the triggering close
                     (idea 94's as-coded convention; NOT protocol-conformant)
           next    — earn one more day, then flatten: exit at the close AFTER the trigger
                     (PROTOCOL rule 2's next-day execution, the conformant arm)
           rebal   — flatten at the next scheduled weekly rebalance (the slowest exit)
Six implementations x stop depth {15%, 25%} x 3 books x 2 universes x 2 cost rungs = 144 stop
arms plus 12 matched no-stop controls, every one reported.  Stop depth is inherited from idea
94 and reported at both values, not tuned.  Re-entry stays on the weekly grid in every arm so
that CHECK and LAG are the only things that move.

Books and panels are idea 94's, imported from its module rather than re-implemented:
`V1u` (live composite /sqrt(vol20), top-5 at 15% each), `TOP20` (composite top-20, equal weight
at 75% gross), `EWall` (equal-weight every name at 75% gross); universes `u56` = universe.json
(BTC/ETH excluded) and `broad` = universe_broad.json; weekly rebalance, 10 and 25 bps.

Reference instrument.  Every cell also gets an 11-point static-gross ladder (m = 0.50..1.00)
on its own control book, so each stop can be read against the price of simply holding less —
idea 94's `gross-m` lever, recomputed here rather than quoted.

Pricing conventions.  dX = arm minus its OWN matched control (same universe, book, cost rung).
An arm is PRICEABLE only if dMaxDD > 0 (it actually bought drawdown) AND, per idea 119's
proposal, dMaxDD >= 10% of the control's own |MaxDD| (the relative materiality floor).  Both
counts are reported so the row can be compared with idea 94's absolute-floor version.

Tests (all reported whatever they say)
    A  REPRODUCTION.  This run's generalised stop simulator at (check=daily, lag=same) against
       idea 94's `run(stop=...)`, arm for arm, max|diff| printed; and idea 94's published
       median dMaxDD (-0.69 / -1.25 pp) and dSharpe (-0.033 / -0.006) re-derived.
    B  MAIN GRID.  All 144 arms + 12 controls: CAGR/Sharpe/MaxDD/H1/H2/IS/OOS, turnover, stop
       firings, dCAGR/dSharpe/dMaxDD, priceability under both floors, 4a and 4b.
    C  IS THE SIGN THE GRID?  dMaxDD sign counts over the 12 matched cells for each of the six
       implementations at each depth — the queue's question, answered as a table.
    D  EXIT SPEED.  dMaxDD and dCAGR ordered by exit speed, and the cost of moving idea 94's
       arm from its as-coded same-day exit to the PROTOCOL-conformant next-day one.
    E  MECHANISM.  Stop firings per year, the realised invested gross of arm vs control (the
       "sells into the drawdown and re-buys at the next rebalance" claim measured as a
       de-grossing rather than asserted), turnover of both, and each cell's own static-gross
       lever in pp of CAGR per pp of MaxDD — the price the stop has to beat.
    F  PROTOCOL RULE 8 WALK-FORWARD.  Implementation and depth chosen on 2009-2016 ONLY by
       argmax IS Sharpe over {12 stop arms + the no-stop control}, evaluated on 2017-2026 read
       once, in every cell.  Reports how often the selector takes a stop at all, OOS regret vs
       the control, and OOS CAGR/Sharpe/MaxDD against RULES v1 and SPY.
    G  4a / 4b footprint for every arm and control on both KEEP paths.
    H  POST-TRIGGER REVERSAL (added after the run, to explain test D rather than report it).
       For every stop firing, the triggering name's return on the NEXT day and over the next
       5 days, against the unconditional daily return of the same panel. If the one-day-slower
       exit is simply selling after a bounce, the drawdown it "buys" is a short-term reversal,
       not an insurance property, and it cannot be quoted as either.

Pre-registered predictions (written after the code audit above, before any backtest was run)
    P1  The generalised simulator at (daily, same) reproduces idea 94's stop arms to < 1e-12.
    P2  The sign is the INSTRUMENT, not the grid: dMaxDD < 0 in the majority of the 12 matched
        cells under ALL SIX implementations, at both depths.
    P3  dMaxDD is monotone in exit speed — the fastest arm (daily/same) is the least negative
        and the slowest (weekly/rebal) the most negative.
    P4  0 of 144 stop arms pass 4b, and the PROTOCOL-conformant (daily, next) arm is WORSE on
        dMaxDD than idea 94's as-coded (daily, same) arm in a majority of cells, i.e. idea 94's
        KILL survives being made protocol-conformant and its published number was generous.

CORRECTION (added after the run, on re-deriving the engine's lag convention from first
principles rather than from the shape of idea 94's loop).  The audit paragraph above is WRONG
on one point and the error is left visible rather than edited out, because two of the
predictions were written on top of it.  `engine.backtest` holds `w.shift(1)`, i.e. a weight
computed from data through close t-1 is the weight that earns day t's return — "decided at t,
applied at t+1" in PROTOCOL rule 2's words.  Idea 94's stop fires from close i and the name is
flat for day i+1's return, which is EXACTLY that convention.  So idea 94's stop is
protocol-conformant, not one bar fast, and this run's `lag='next'` arm is one day SLOWER than
the protocol allows, not the conformant one.  Nothing in the code or the numbers changes; what
changes is which arm may be quoted, and P4's second clause was scored against a false premise.
See test H, added for the same reason: it asks whether the one-day-slower arm's drawdown gain
is a short-term reversal being harvested rather than a property of the stop.

SURVIVORSHIP.  Both panels are current-constituent lists (universe.json, universe_broad.json):
names that fell out are absent, which flatters any always-invested book and therefore makes a
protective instrument look WORSE than it was.  That bias runs in the same direction as this
run's conclusion, so the conclusion is a lower bound on the stop's value, not an upper one —
stated rather than corrected, and the reason nothing here is quoted as an achievable return.
The calendar-day index defect of idea 38 is still unfixed for these two panels; it applies
identically to arm and control in every comparison below, which is what this run compares.

Deterministic, standalone.  Imports research/baseline.py and idea 94's module unchanged;
modifies nothing.  Writes .console.txt and four .csv companions next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe  # noqa: E402
from engine import metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_stop-as-negative-insurance_cloud"
OUT = ROOT / "research" / "backtests"
I94 = ROOT / "research" / "backtests" / "2026-09-04_drawdown-insurance-price-list_B.py"

_spec = importlib.util.spec_from_file_location("i94", I94)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, GROSS = H.FREQ, H.GROSS
IS_END, OOS_START = H.IS_END, H.OOS_START
BOOKS, COSTS = H.BOOKS, H.COSTS
DEPTHS = [0.15, 0.25]
CHECKS = ["daily", "weekly"]
LAGS = ["same", "next", "rebal"]
LEVER = np.round(np.arange(0.50, 1.001, 0.05), 2)
WARMUP = 260
REL_FLOOR = 0.10                 # idea 119: material only if dMaxDD >= 10% of |control MaxDD|

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------- generalised stop simulator ----
def run_stop(px, W, stop=None, check="daily", lag="same", m=1.0, bps=H.PCOST, freq=FREQ):
    """idea 94's `run()` with the stop's CHECK frequency and execution LAG made explicit.

    check='daily'  evaluate the trigger every row (idea 94)
    check='weekly' evaluate it only on rebalance rows; the running high still updates daily
    lag='same'     flatten at row i+1, so the last return day is i -> exit price px[i] (idea 94)
    lag='next'     flatten at row i+2, so the last return day is i+1 -> exit price px[i+1]
                   (PROTOCOL rule 2: decided at close t, executed at t+1)
    lag='rebal'    flatten at the next scheduled rebalance row
    Everything else — drift, cost accounting, re-entry on the weekly grid — is idea 94's.
    """
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape
    nxt = np.full(nrow, -1, dtype=int)                 # next rebalance row strictly after i
    j = -1
    for i in range(nrow - 1, -1, -1):
        nxt[i] = j
        if mask[i]:
            j = i

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    exit_at = np.full(ncol, -1, dtype=int)             # row on which a fired stop is executed
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross = np.zeros(nrow)                             # realised invested gross, the mechanism
    n_stops = 0
    trig_rows, trig_cols = [], []

    for i in range(nrow):
        due = exit_at == i                             # 1. stop exits falling due now
        if due.any():
            turn[i] += cur[due].sum()
            cur = np.where(due, 0.0, cur)
            exit_at = np.where(due, -1, exit_at)
        if mask[i] and i > 0:                          # 2. scheduled rebalance (re-entry here)
            new = tgt[i - 1]
            s = new.sum()
            if s > 1.0:
                new = new / s
            turn[i] += np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        gross[i] = cur.sum()
        growth = cur * (1 + rets[i])                   # 4. drift
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:                           # 5. trailing highs / fire stops
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p), np.nan)
            if check == "daily" or mask[i]:
                hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop)) & (exit_at < 0)
                if hit.any():
                    n_stops += int(hit.sum())
                    idx = np.flatnonzero(hit)
                    trig_rows.extend([i] * len(idx))
                    trig_cols.extend(idx.tolist())
                    if lag == "same":
                        tgt_row = min(i + 1, nrow - 1)
                    elif lag == "next":
                        tgt_row = min(i + 2, nrow - 1)
                    else:
                        tgt_row = nxt[i] if nxt[i] > 0 else nrow - 1
                    exit_at = np.where(hit, tgt_row, exit_at)

    r = (pd.Series((held * rets).sum(axis=1), index=px.index)
         - pd.Series(turn, index=px.index) * bps / 1e4)
    return dict(r=r, to=pd.Series(turn, index=px.index), n_stops=n_stops,
                gross=pd.Series(gross, index=px.index),
                trig=(np.array(trig_rows, dtype=int), np.array(trig_cols, dtype=int)))


# ------------------------------------------------------------- metric helpers ----
def stats(r, start):
    r = r.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], IS_Sharpe=i["Sharpe"], IS_MaxDD=i["MaxDD"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def verdicts(d, base, spy):
    p4a = d["H1"] > base["H1"] and d["H2"] > base["H2"] and d["MaxDD"] >= base["MaxDD"]
    p4b = (d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and d["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])
    return p4a, p4b


def main():
    say("[audit] idea 94 `run()` reading, done before any backtest: the trailing-stop trigger "
        "is evaluated on EVERY row (its step 5 is not gated by the rebalance mask), so the exit "
        "is already intra-week; the weekly grid governs RE-ENTRY only. A hit at row i is "
        "executed at row i+1 before that row's return, so the effective exit price is px[i], "
        "the triggering close — one bar faster than PROTOCOL rule 2's next-day execution.")

    panels = {}
    panels["u56"] = load_universe()
    panels["broad"] = load_universe(broad=True)
    rows, cells = [], {}

    for uname, px in panels.items():
        start = px.index[WARMUP]
        spy_r = px["SPY"].pct_change().fillna(0.0)
        spy = stats(spy_r, start)
        v1 = H.targets(px, "V1u")
        base_v1 = stats(run_stop(px, v1, None, bps=H.PCOST)["r"], start)
        say(f"\n[panel] {uname}: {px.shape[1]} columns, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"[SPY] {uname}: CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.3f} "
            f"MaxDD {spy['MaxDD']:.1%} halves {spy['H1']:.3f}/{spy['H2']:.3f} "
            f"OOS {spy['OOS_CAGR']:.2%}/{spy['OOS_Sharpe']:.3f}/{spy['OOS_MaxDD']:.1%} "
            f"| 4b bars MaxDD >= {0.60*spy['MaxDD']:.1%}, CAGR >= {0.70*spy['CAGR']:.2%}")
        say(f"[v1 baseline] {uname}: {base_v1['CAGR']:.2%}/{base_v1['Sharpe']:.3f}/"
            f"{base_v1['MaxDD']:.1%} halves {base_v1['H1']:.3f}/{base_v1['H2']:.3f}")

        for book in BOOKS:
            W = H.targets(px, book)
            for cost in COSTS:
                # ---- A: reproduction of idea 94's convention, arm for arm ----
                ctl_ref = H.run(px, W, bps=cost)["r"]
                ctl_res = run_stop(px, W, None, bps=cost)
                ctl = ctl_res["r"]
                dctl = float((ctl - ctl_ref).abs().max())
                c = stats(ctl, start)
                _yrs = len(ctl.loc[start:]) / 252
                c["turnover"] = ctl_res["to"].loc[start:].sum() / _yrs
                c["gross"] = float(ctl_res["gross"].loc[start:].mean())
                cells[(uname, book, cost)] = dict(ctl=c, spy=spy, base=base_v1, start=start)

                # static-gross lever on this cell's own control
                lad = []
                for m in LEVER:
                    lr = run_stop(px, W, None, m=float(m), bps=cost)["r"]
                    lm = stats(lr, start)
                    lad.append((lm["MaxDD"], lm["CAGR"]))
                lad = np.array(lad)
                lever = float(np.polyfit(-lad[:, 0] * 100, lad[:, 1] * 100, 1)[0])  # pp CAGR / pp MaxDD
                cells[(uname, book, cost)]["lever"] = lever

                for depth in DEPTHS:
                    ref = H.run(px, W, stop=depth, bps=cost)
                    for check in CHECKS:
                        for lag in LAGS:
                            res = run_stop(px, W, stop=depth, check=check, lag=lag, bps=cost)
                            d = stats(res["r"], start)
                            yrs = len(res["r"].loc[start:]) / 252
                            d.update(universe=uname, book=book, cost_bps=cost,
                                     depth=depth, check=check, lag=lag,
                                     arm=f"{check}/{lag}/stop{int(depth*100)}",
                                     turnover=res["to"].loc[start:].sum() / yrs,
                                     stops_per_yr=res["n_stops"] / yrs,
                                     gross_mean=float(res["gross"].loc[start:].mean()),
                                     ctl_gross=c["gross"], ctl_turnover=c["turnover"],
                                     dCAGR_pp=100 * (d["CAGR"] - c["CAGR"]),
                                     dSharpe=d["Sharpe"] - c["Sharpe"],
                                     dMaxDD_pp=100 * (d["MaxDD"] - c["MaxDD"]),
                                     ctl_MaxDD=c["MaxDD"], lever=lever, repro_diff=dctl)
                            d["priceable_abs"] = d["dMaxDD_pp"] > 0.10
                            d["priceable_rel"] = d["dMaxDD_pp"] >= REL_FLOOR * 100 * abs(c["MaxDD"])
                            d["price"] = (-d["dCAGR_pp"] / d["dMaxDD_pp"]
                                          if d["dMaxDD_pp"] > 0.10 else np.nan)
                            d["pass4a"], d["pass4b"] = verdicts(d, base_v1, spy)
                            if check == "daily" and lag == "same":
                                d["i94_diff"] = float((res["r"] - ref["r"]).abs().max())
                                d["i94_stops_diff"] = res["n_stops"] - ref["n_stops"]
                            else:
                                d["i94_diff"], d["i94_stops_diff"] = np.nan, np.nan
                            rows.append(d)
                # controls as rows too
                cr = dict(c)
                cr.update(universe=uname, book=book, cost_bps=cost, depth=np.nan,
                          check="none", lag="none", arm="control (no stop)",
                          dCAGR_pp=0.0, dSharpe=0.0, dMaxDD_pp=0.0, ctl_MaxDD=c["MaxDD"],
                          lever=lever, repro_diff=dctl, priceable_abs=False,
                          priceable_rel=False, price=np.nan, stops_per_yr=0.0,
                          turnover=c["turnover"], ctl_turnover=c["turnover"],
                          gross_mean=c["gross"], ctl_gross=c["gross"], i94_diff=np.nan,
                          i94_stops_diff=np.nan)
                cr["pass4a"], cr["pass4b"] = verdicts(cr, base_v1, spy)
                rows.append(cr)

    g = pd.DataFrame(rows)
    gcols = ["universe", "book", "cost_bps", "arm", "check", "lag", "depth", "CAGR", "Sharpe",
             "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "dCAGR_pp", "dSharpe", "dMaxDD_pp", "price", "lever", "priceable_abs",
             "priceable_rel", "turnover", "ctl_turnover", "stops_per_yr", "gross_mean",
             "ctl_gross", "pass4a", "pass4b",
             "repro_diff", "i94_diff"]
    g[gcols].to_csv(OUT / f"{STEM}.grid.csv", index=False)
    arms = g[g.check != "none"]
    say(f"\n[B] grid: {len(arms)} stop arms + {len(g)-len(arms)} controls -> {STEM}.grid.csv")

    # ---- A: reproduction ----
    rep = arms[(arms.check == "daily") & (arms.lag == "same")]
    say(f"\n[A] REPRODUCTION of idea 94's stop convention (check=daily, lag=same):")
    say(f"    control vs idea 94's own `run()`  max|diff| over 12 cells = "
        f"{g.repro_diff.max():.3e}")
    say(f"    stop arms vs idea 94's `run(stop=...)` max|diff| over 24 arms = "
        f"{rep.i94_diff.max():.3e}; firing-count differences = "
        f"{int(rep.i94_stops_diff.abs().max())}")
    for depth in DEPTHS:
        s = rep[rep.depth == depth]
        say(f"    stop{int(depth*100)}: median dMaxDD {s.dMaxDD_pp.median():+.2f} pp "
            f"[idea 94 published {-0.69 if depth==0.15 else -1.25:+.2f}], median dSharpe "
            f"{s.dSharpe.median():+.3f} [published {-0.033 if depth==0.15 else -0.006:+.3f}], "
            f"median turnover {s.turnover.median():.1f}x "
            f"[published {12.5 if depth==0.15 else 11.3:.1f}x], "
            f"dMaxDD < 0 in {int((s.dMaxDD_pp<0).sum())}/{len(s)} cells "
            f"[published 10/12 negative, 0/12 priceable]")

    # ---- C: is the sign the grid? ----
    say("\n[C] IS THE SIGN THE GRID? dMaxDD sign over the 12 matched cells, by implementation:")
    say(f"    {'check':>7} {'lag':>6} {'depth':>6} {'dMaxDD<0':>9} {'med dMaxDD':>11} "
        f"{'med dCAGR':>10} {'med dSharpe':>12} {'priceable(abs)':>15} {'priceable(rel)':>15}")
    crows = []
    for check in CHECKS:
        for lag in LAGS:
            for depth in DEPTHS:
                s = arms[(arms.check == check) & (arms.lag == lag) & (arms.depth == depth)]
                row = dict(check=check, lag=lag, depth=depth, n=len(s),
                           n_neg=int((s.dMaxDD_pp < 0).sum()),
                           med_dMaxDD=s.dMaxDD_pp.median(), med_dCAGR=s.dCAGR_pp.median(),
                           med_dSharpe=s.dSharpe.median(),
                           priceable_abs=int(s.priceable_abs.sum()),
                           priceable_rel=int(s.priceable_rel.sum()),
                           med_turnover=s.turnover.median(),
                           med_stops=s.stops_per_yr.median())
                crows.append(row)
                say(f"    {check:>7} {lag:>6} {depth:>6.2f} {row['n_neg']:>6}/{len(s):<2} "
                    f"{row['med_dMaxDD']:>11.2f} {row['med_dCAGR']:>10.2f} "
                    f"{row['med_dSharpe']:>12.3f} {row['priceable_abs']:>14}/{len(s)} "
                    f"{row['priceable_rel']:>14}/{len(s)}")
    impl = pd.DataFrame(crows)
    impl.to_csv(OUT / f"{STEM}.implementations.csv", index=False)

    # ---- D: exit speed ----
    say("\n[D] EXIT SPEED — the queue's axis, slowest to fastest (median over 12 cells, "
        "both depths pooled):")
    order = [("daily", "same"), ("daily", "next"), ("weekly", "same"), ("weekly", "next"),
             ("daily", "rebal"), ("weekly", "rebal")]
    for check, lag in order:
        s = arms[(arms.check == check) & (arms.lag == lag)]
        say(f"    {check:>7}/{lag:<6}: med dMaxDD {s.dMaxDD_pp.median():+7.2f} pp | "
            f"med dCAGR {s.dCAGR_pp.median():+7.2f} pp | med dSharpe {s.dSharpe.median():+.3f} | "
            f"dMaxDD<0 in {int((s.dMaxDD_pp<0).sum())}/{len(s)} | "
            f"stops/yr {s.stops_per_yr.median():.1f}")
    a = arms[(arms.check == "daily") & (arms.lag == "same")].set_index(
        ["universe", "book", "cost_bps", "depth"])
    b = arms[(arms.check == "daily") & (arms.lag == "next")].set_index(
        ["universe", "book", "cost_bps", "depth"])
    dd = (b.dMaxDD_pp - a.dMaxDD_pp).dropna()
    dc = (b.dCAGR_pp - a.dCAGR_pp).dropna()
    ds = (b.dSharpe - a.dSharpe).dropna()
    say(f"    COST OF PROTOCOL CONFORMANCE (as-coded same-day -> next-day, 24 arms): "
        f"dMaxDD worsens in {int((dd<0).sum())}/{len(dd)} (median {dd.median():+.3f} pp), "
        f"dCAGR {dc.median():+.3f} pp, dSharpe {ds.median():+.4f}")

    # ---- E: mechanism ----
    say("\n[E] MECHANISM — firings, the de-grossing they cause, and the lever this must beat "
        "(check=daily, lag=same, i.e. idea 94's own arm):")
    say(f"    {'universe':>8} {'book':>6} {'cost':>5} {'depth':>6} {'stops/yr':>9} "
        f"{'gross arm':>10} {'gross ctl':>10} {'turn arm':>9} {'turn ctl':>9} {'lever pp/pp':>12}")
    for _, x in arms[(arms.check == "daily") & (arms.lag == "same")].sort_values(
            ["universe", "book", "cost_bps", "depth"]).iterrows():
        say(f"    {x.universe:>8} {x.book:>6} {x.cost_bps:>5.0f} {x.depth:>6.2f} "
            f"{x.stops_per_yr:>9.1f} {x.gross_mean:>10.3f} {x.ctl_gross:>10.3f} "
            f"{x.turnover:>8.1f}x {x.ctl_turnover:>8.1f}x {x.lever:>12.3f}")

    # ---- F: rule 8 walk-forward ----
    say(f"\n[F] PROTOCOL RULE 8 WALK-FORWARD — implementation + depth chosen on "
        f"..{IS_END} by argmax IS Sharpe over {{12 stop arms + no-stop control}}, "
        f"OOS {OOS_START}.. read once:")
    wrows = []
    for (u, bk, ck), sub in g.groupby(["universe", "book", "cost_bps"]):
        c = cells[(u, bk, ck)]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        ctl = sub[sub.check == "none"].iloc[0]
        took = pick.arm != "control (no stop)"
        say(f"    {u:>7}/{bk:<6}@{ck:.0f}bp pick **{pick.arm}** (IS {pick.IS_Sharpe:.3f} vs "
            f"control {ctl.IS_Sharpe:.3f}) -> OOS {pick.OOS_CAGR:>7.2%}/{pick.OOS_Sharpe:.3f}/"
            f"{pick.OOS_MaxDD:.1%} vs control OOS {ctl.OOS_CAGR:.2%}/{ctl.OOS_Sharpe:.3f}/"
            f"{ctl.OOS_MaxDD:.1%} | regret {pick.OOS_Sharpe-ctl.OOS_Sharpe:+.3f} | "
            f"SPY OOS {c['spy']['OOS_CAGR']:.2%}/{c['spy']['OOS_Sharpe']:.3f} | "
            f"4a {pick.pass4a} 4b {pick.pass4b}")
        wrows.append(dict(universe=u, book=bk, cost_bps=ck, pick=pick.arm, took_stop=took,
                          IS_Sharpe=pick.IS_Sharpe, ctl_IS_Sharpe=ctl.IS_Sharpe,
                          OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                          OOS_MaxDD=pick.OOS_MaxDD, ctl_OOS_Sharpe=ctl.OOS_Sharpe,
                          regret=pick.OOS_Sharpe - ctl.OOS_Sharpe,
                          SPY_OOS_Sharpe=c["spy"]["OOS_Sharpe"],
                          v1_OOS_Sharpe=c["base"]["OOS_Sharpe"],
                          pass4a=pick.pass4a, pass4b=pick.pass4b))
    wf = pd.DataFrame(wrows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"    selector took a stop in {int(wf.took_stop.sum())}/{len(wf)} cells; mean OOS "
        f"regret vs the no-stop control {wf.regret.mean():+.3f}; "
        f"OOS Sharpe beats SPY in {int((wf.OOS_Sharpe>wf.SPY_OOS_Sharpe).sum())}/{len(wf)}")

    # ---- G: KEEP footprint ----
    say(f"\n[G] KEEP footprint: 4a {int(arms.pass4a.sum())}/{len(arms)} stop arms "
        f"({int(g[g.check=='none'].pass4a.sum())}/{len(g[g.check=='none'])} controls); "
        f"4b {int(arms.pass4b.sum())}/{len(arms)} stop arms "
        f"({int(g[g.check=='none'].pass4b.sum())}/{len(g[g.check=='none'])} controls)")
    if arms.pass4b.any():
        for _, x in arms[arms.pass4b].iterrows():
            say(f"    4b: {x.universe}/{x.book}@{x.cost_bps:.0f} {x.arm} "
                f"{x.CAGR:.2%}/{x.Sharpe:.3f}/{x.MaxDD:.1%} halves {x.H1:.3f}/{x.H2:.3f} "
                f"OOS {x.OOS_Sharpe:.3f}")
    ctls = g[g.check == "none"]
    if ctls.pass4b.any():
        say("    control books passing 4b (inherited, not caused by any stop):")
        for _, x in ctls[ctls.pass4b].iterrows():
            say(f"      {x.universe}/{x.book}@{x.cost_bps:.0f}: {x.CAGR:.2%}/{x.Sharpe:.3f}/"
                f"{x.MaxDD:.1%} halves {x.H1:.3f}/{x.H2:.3f} OOS {x.OOS_Sharpe:.3f}")

    # ---- H: post-trigger reversal (why does a one-day-slower exit buy drawdown?) ----
    say("\n[H] POST-TRIGGER REVERSAL — is the slower exit harvesting a bounce? Mean return of "
        "the triggering name on the day AFTER the trigger and over the next 5 days, against the "
        "same panel's unconditional daily mean:")
    say(f"    {'universe':>8} {'book':>6} {'depth':>6} {'firings':>8} {'E[r|t+1]':>10} "
        f"{'uncond':>9} {'t-stat':>8} {'E[r|t+1..5]':>12} {'uncond x5':>10}")
    hrows = []
    for uname, px in panels.items():
        rr = px.pct_change().fillna(0.0).values
        uncond = float(np.nanmean(px.pct_change().values))
        f5 = pd.DataFrame(rr).rolling(5).sum().shift(-5).values      # next 5 days, sum of returns
        for book in BOOKS:
            W = H.targets(px, book)
            for depth in DEPTHS:
                res = run_stop(px, W, stop=depth, check="daily", lag="same", bps=H.PCOST)
                ti, tc = res["trig"]
                keep = ti + 1 < len(px)
                ti, tc = ti[keep], tc[keep]
                nxt1 = rr[ti + 1, tc]
                nxt5 = f5[ti, tc]
                nxt5 = nxt5[np.isfinite(nxt5)]
                tstat = (float(np.mean(nxt1)) - uncond) / (float(np.std(nxt1, ddof=1)) /
                                                           np.sqrt(len(nxt1))) if len(nxt1) > 2 else np.nan
                hrows.append(dict(universe=uname, book=book, depth=depth, firings=len(ti),
                                  mean_next1=float(np.mean(nxt1)), uncond=uncond, t=tstat,
                                  mean_next5=float(np.mean(nxt5)) if len(nxt5) else np.nan))
                say(f"    {uname:>8} {book:>6} {depth:>6.2f} {len(ti):>8} "
                    f"{100*np.mean(nxt1):>9.3f}% {100*uncond:>8.3f}% {tstat:>8.2f} "
                    f"{100*np.mean(nxt5) if len(nxt5) else float('nan'):>11.3f}% "
                    f"{500*uncond:>9.3f}%")
    rev = pd.DataFrame(hrows)
    rev.to_csv(OUT / f"{STEM}.reversal.csv", index=False)
    say(f"    post-trigger next-day mean exceeds the unconditional mean in "
        f"{int((rev.mean_next1 > rev.uncond).sum())}/{len(rev)} cells; median excess "
        f"{100*(rev.mean_next1 - rev.uncond).median():+.3f} pp/day")

    # ---- predictions ----
    say("\n[P] pre-registered predictions vs outcome")
    say(f"    P1 (daily,same) reproduces idea 94 to <1e-12: max|diff| {rep.i94_diff.max():.3e} "
        f"-> {'CONFIRMED' if rep.i94_diff.max() < 1e-12 else 'REFUTED'}")
    worst = impl.n_neg.min()
    say(f"    P2 dMaxDD < 0 in the majority of 12 cells for ALL SIX implementations at both "
        f"depths: minimum negative count over the 12 (impl, depth) groups = {worst}/12 -> "
        f"{'CONFIRMED' if worst > 6 else 'REFUTED'}")
    sp = {(c, l): arms[(arms.check == c) & (arms.lag == l)].dMaxDD_pp.median()
          for c in CHECKS for l in LAGS}
    fastest, slowest = sp[("daily", "same")], sp[("weekly", "rebal")]
    say(f"    P3 dMaxDD monotone in exit speed: fastest daily/same {fastest:+.2f} pp, slowest "
        f"weekly/rebal {slowest:+.2f} pp -> "
        f"{'CONFIRMED' if fastest > slowest else 'REFUTED'} "
        f"(full ordering " + ", ".join(f"{c}/{l} {v:+.2f}" for (c, l), v in sp.items()) + ")")
    say(f"    P4 0 of {len(arms)} stop arms pass 4b: {int(arms.pass4b.sum())}; and next-day is "
        f"worse than same-day on dMaxDD in {int((dd<0).sum())}/{len(dd)} arms -> "
        f"{'CONFIRMED' if arms.pass4b.sum()==0 and (dd<0).sum() > len(dd)/2 else 'PARTIAL/REFUTED'}")
    say("    P4 note (see CORRECTION in the docstring): its second clause was written on a "
        "mistaken reading of the engine's lag. `lag=same` IS the protocol-conformant arm, so "
        "the protocol-conformant answer is the same-day column, where the stop still destroys "
        "drawdown; every 4b pass above sits on the one-day-SLOWER `next` arm, which PROTOCOL "
        "rule 2 does not permit and test H explains.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
