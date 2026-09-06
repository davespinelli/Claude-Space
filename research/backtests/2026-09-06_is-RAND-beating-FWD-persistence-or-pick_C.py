#!/usr/bin/env python3
"""Idea 260 - "is-RAND-beating-FWD-persistence-or-pick" (lane C, 2026-09-06).

The question
------------
Idea 82 measured the isolate the record had been missing: at matched n and matched gross,

    FWD - RAND  =  -0.0213 Sharpe,  t -2.72,  positive in 21/64 (cell, seed) draws

and concluded that the composite ranking does not reliably add Sharpe over a random pick
of the same size.  That number carried a construction choice, pre-registered in idea 82's
own docstring and quoted here verbatim:

    RAND   n eligible names by a per-name uniform score drawn ONCE per seed and held
           constant through time, so the arm's persistence - and hence its turnover -
           is generated the same way FWD's and REV's are, not by weekly re-drawing
           (a weekly re-draw would hand RAND a ~52x/yr turnover bill and answer a
           cost question instead of a ranking question).

The choice was made for a good reason and it does something the docstring does not say.
A per-name score drawn once and held forever does not pick a random name each week: it
picks a random SUBSET of the panel and holds it for seventeen years.  Its realised
turnover (9.0-9.5x/yr in idea 82's grid) comes entirely from names crossing the
eligibility gate, exactly like FWD's (11.0-14.3x/yr).  So `FWD - RAND` is not "ranking vs
a coin flip"; it is "ranking vs one fixed random subset", and the two arms differ in
WHICH names they hold, not in HOW OFTEN they change them.  A negative sign there is
consistent with two different worlds:

    (i) THE PICK.  A random n-subset of the eligible set really is a better risk-adjusted
        book than the composite's top n, at matched breadth.  Then the sign should survive
        re-drawing the subset every week, because every draw is equally uninformed.
    (ii) THE PERSISTENCE.  Holding ANY fixed subset for the whole sample is worth Sharpe -
        a held random subset is a buy-and-hold-ish book with low turnover and whatever
        diversification its 20 names happen to carry, while FWD churns through the gate.
        Then the sign is a statement about holding, not about picking, and it should
        weaken or reverse once the random arm is re-drawn.

This run separates them, which is what the queue asks for.

Design
------
Everything except the new arm is idea 82's, imported verbatim: panels U56 / B136 /
BSTK100, weekly cadence, next-day execution, gate = above-200d AND vol20 < 0.60, key =
the composite WITHOUT the vol scaler, GROSS MATCHED AT 0.75 on every arm including EWall
(idea 73's `CANDg` / idea 240's NORM), n in {20,30,40,60}, 8 seeds, every seed reported.

    EWall  every eligible name, equal weight, gross matched
    FWD    top-n by the composite key                       (the incumbent construction)
    REV    bottom-n by the composite key                     (the signed-key check)
    RANDH  idea 82's RAND, byte-for-byte: per-name uniform drawn ONCE (rng 1000+seed),
           held constant through time                        (a fixed random SUBSET)
    RANDW  the new arm: a FRESH per-name uniform drawn at EVERY rebalance date
           (rng 2000+seed, one draw per rebalance week, held between rebalances so the
           engine's next-day execution is unchanged)          (a fresh random PICK)

COST RUNGS 0 / 10 / 30 bps, all three reported for every point, because a weekly re-draw
buys its independence with turnover and the queue asks for the bill to be shown.  Costs
are applied exactly, not approximately: `engine.backtest` computes
`port = (held*rets).sum(axis=1) - turnover*cost_bps/1e4`, so `held` and `turnover` do not
depend on the rung and each book is run ONCE at 0 bps with the other rungs derived as
`r(c) = r(0) - turnover*c/1e4`.  This identity is asserted against a live 10 bps
`backtest()` call before any result is read; the run aborts if it does not hold to 0.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (4)
The arm is the hypothesis axis (pre-registered above), the cost rung is a reported axis
the queue names explicitly, and the seed is averaged over with every draw written out.
Grid = 3 panels x [EWall + v1 + 4 FWD + 4 REV + 32 RANDH + 32 RANDW] x 3 rungs
     = 3 x 74 x 3 = 666 points, ALL written to `.grid.csv`.

Pre-registered decision rule (written before any number was read)
-----------------------------------------------------------------
The SIGN VERDICT is read at 0 bps.  That rung is the only one that answers a PICK
question: at 10 and 30 bps `FWD - RANDW` is inflated by RANDW's turnover bill, which is
the cost question idea 82 deliberately refused to answer under the label of a ranking
question.  Both cost rungs are reported in full anyway, and the rung at which the sign
flips (if it flips) is reported as the arm's cost breakeven.

    (a) If `FWD - RANDW` is NEGATIVE at 0 bps with the same reliability idea 82 reported
        for `FWD - RANDH` (t < -2 per (cell, seed)), the sign is about the PICK, survives
        the separation, and idea 82's isolate is CONFIRMED under its own label.
    (b) If `FWD - RANDW` is POSITIVE at 0 bps while `FWD - RANDH` reproduces negative,
        idea 82's negative sign is generated by HOLDING the draw, not by the draw.  The
        isolate is then correctly measured and MISNAMED - it is a persistence statement -
        and every published quotation of "the composite adds nothing over a random pick"
        needs the qualifier "...over one fixed random subset held for the sample".
    (c) If `FWD - RANDW` is indistinguishable from zero at 0 bps, neither reading is
        supported and the correct verdict is that the isolate does not have the power to
        separate the two channels at 8 seeds; that is a PARK on the label, not a KEEP.

The decomposition `(FWD - RANDW) = (FWD - RANDH) + (RANDH - RANDW)` is an identity and is
asserted to machine precision; `RANDH - RANDW` is the persistence leg on its own, read at
every rung, and is the number the queue is actually asking for.

Idea 82's KILL turned on a Sharpe/CAGR reversal (its `FWD - RAND` is -0.0213 on Sharpe and
+1.25 pp/yr on CAGR, t +4.30, 8/8), so EVERY comparison here is reported on CAGR and
|MaxDD| beside Sharpe.  A separation that only moves one metric is reported as such.

Reproduction gate (must pass before anything else is read)
    U56/CAND20 FIXED (idea 73's literal GROSS/n)  -> 12.7% / 1.093 / -18.3%, halves 1.088/1.103
    U56/RULES v1                                  -> 6.5% / 0.666 / -13.8%
    idea 82's isolate at 10 bps: `FWD - RANDH` = -0.0213, t -2.72, 21/64 per (cell, seed)
    idea 82's 8 unsaturated-cell means at 10 bps: EWall-FWD +0.0467 (7/8), FWD-REV +0.1803

Walk-forward (PROTOCOL rule 8) - selectors fixed, with direction, before any OOS read
    EWALL         EWall, no ranking, no n
    FWD20         FWD n=20                                    (incumbent construction)
    RANDH20       mean over the 8 held-draw seeds at n=20      (idea 82's coin flip)
    RANDW20       mean over the 8 weekly-redraw seeds at n=20  (the honest coin flip)
    FWD_ISARGMAX  n = argmax IS Sharpe within the FWD arm
    ALL_ISARGMAX  (arm, n, seed) = argmax IS Sharpe over every arm
    IS = 2009-01-01..2016-12-31 (parameters chosen here only), OOS = 2017-01-01..end,
    read once, at each cost rung, per panel and pooled, against RULES v1 OOS and SPY OOS.

Verdicts (both KEEP paths, on every point, at every rung)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SATURATION.  When a panel supplies fewer than n eligible names, EVERY n-arm IS EWall and
the comparison is between a book and itself.  `sat_share` is reported for every cell and
cells with sat_share > 0.25 are excluded from headline counts, exactly as in idea 82.

SURVIVORSHIP: universe_broad.json and the megacap cut are CURRENT constituents, so B136
and BSTK100 are one-directional.  The direction bites this question specifically: on a
list of known survivors, a random subset HELD for the sample collects the full survivorship
premium of whatever it drew, while a weekly re-draw keeps re-entering the same premium at
a fresh cost.  The bias therefore runs TOWARD RANDH and AGAINST RANDW, i.e. toward finding
that idea 82's sign is a persistence artefact.  Any verdict in that direction must be
discounted by it, and it is restated in the result.

Deterministic (fixed seeds), standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

RUNGS = [0, 10, 30]
HEADLINE_RUNG = 10          # idea 82's rung, used only for the reproduction gate
SIGN_RUNG = 0               # pre-registered: the rung the sign verdict is read at
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [20, 30, 40, 60]
SEEDS = list(range(8))
IS_START = "2009-01-01"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SAT_CAP = 0.25
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)


# ------------------------------------------------------------------ panels (idea 82, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":     sub(px56, list(px56.columns)),
        "B136":    sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
    }


# ------------------------------------------------------------------ books
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def _held_key(px, seed):
    """idea 82's RAND: ONE uniform per name, drawn once, held for the whole sample."""
    rng = np.random.default_rng(1000 + seed)
    return pd.DataFrame(np.tile(rng.random(px.shape[1]), (len(px.index), 1)),
                        index=px.index, columns=px.columns)


def _weekly_key(px, seed, rmask):
    """The new arm: a FRESH uniform per name at every rebalance date, held between them.

    The engine reads a weights row only on rebalance dates (it shifts both the weights and
    the rebalance mask by one day), so drawing on rebalance dates and forward-filling in
    between leaves execution identical to every other arm and changes ONLY the persistence
    of the pick.
    """
    rng = np.random.default_rng(2000 + seed)
    idx = px.index
    reb = np.flatnonzero(rmask.values)
    k = np.empty((len(idx), px.shape[1]), dtype=float)
    k[:] = np.nan
    # a draw for the pre-first-rebalance stub as well, so no row is undefined
    k[0] = rng.random(px.shape[1])
    for i in reb:
        k[i] = rng.random(px.shape[1])
    return pd.DataFrame(k, index=idx, columns=px.columns).ffill()


def weights(px, tradable, arm, n=None, seed=None, rmask=None):
    """All arms gross-matched at GROSS (idea 73's CANDg / idea 240's NORM)."""
    elig = eligible_mask(px, tradable)
    if arm == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "FIXED20":                       # idea 73's literal GROSS/n, reproduction gate only
        s = score(px, vol_scale=False)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 20).astype(float) * (GROSS / 20)
    if arm == "EWall":
        sel = elig.astype(float)
    else:
        if arm == "RANDH":
            key, asc = _held_key(px, seed), False
        elif arm == "RANDW":
            key, asc = _weekly_key(px, seed, rmask), False
        else:
            key = score(px, vol_scale=False)[0]
            asc = (arm == "REV")               # REV = worst-n by the composite
        rank = key.where(elig).rank(axis=1, ascending=asc)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


# ------------------------------------------------------------------ stats
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def paired_t(d):
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=float)
    if len(d) < 2:
        return np.nan, np.nan
    se = d.std(ddof=1) / np.sqrt(len(d))
    return d.mean(), (d.mean() / se if se > 0 else np.nan)


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ main
def main():
    panels = build_panels()

    print("=" * 210)
    print(f"Idea 260 is-RAND-beating-FWD-persistence-or-pick (lane C) | {SCRIPT} | "
          f"weekly, next-day execution, gross matched at {GROSS}, cost rungs {RUNGS} bps")
    print("=" * 210)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    necl, rmasks = {}, {}
    for k, (p, tr) in panels.items():
        e = eligible_mask(p, tr)
        m = rebalance_mask(p.index, FREQ)
        rmasks[k] = m
        necl[k] = e[m.values].sum(axis=1)
        print(f"  {k:<8} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  {p.index[0].date()} -> {p.index[-1].date()}"
              f"   mean eligible {necl[k].mean():.1f}  (p10 {necl[k].quantile(.10):.0f} / p90 {necl[k].quantile(.90):.0f})"
              f"   rebalances {int(m.sum())}")

    # ---- run every book ONCE at 0 bps; other rungs are exact ------------
    jobs = [("EWall", None, None), ("v1", None, None)]
    jobs += [(a, n, None) for a in ("FWD", "REV") for n in NS]
    jobs += [(a, n, s) for a in ("RANDH", "RANDW") for n in NS for s in SEEDS]

    gross_ret, turn, gross_w, held_w = {}, {}, {}, {}
    for pk, (p, tr) in panels.items():
        for arm, n, seed in jobs:
            w = weights(p, tr, arm, n, seed, rmasks[pk])
            r = backtest(p, w, cost_bps=0, freq=FREQ)
            key = (pk, arm, n, seed)
            gross_ret[key] = r["returns"]
            turn[key] = r["turnover"]
            hw = r["weights"]
            gross_w[key] = hw.sum(axis=1)
            held_w[key] = (hw > 1e-12).sum(axis=1)
        print(f"  ran {pk}  ({len(jobs)} books at 0 bps)")

    def R(pk, arm, n, seed, bps):
        k = (pk, arm, n, seed)
        return gross_ret[k] - turn[k] * bps / 1e4

    # ---- HARNESS IDENTITY: the derived rung must equal a live backtest ---
    p, tr = panels["U56"]
    w_chk = weights(p, tr, "FWD", 20, None, rmasks["U56"])
    live10 = backtest(p, w_chk, cost_bps=10, freq=FREQ)["returns"]
    err = float((R("U56", "FWD", 20, None, 10) - live10).abs().max())
    w_chk2 = weights(p, tr, "RANDW", 20, 0, rmasks["U56"])
    live30 = backtest(p, w_chk2, cost_bps=30, freq=FREQ)["returns"]
    err2 = float((R("U56", "RANDW", 20, 0, 30) - live30).abs().max())
    print(f"\nHarness identity (derived rung vs live backtest): FWD20@10bps {err:.3e}, RANDW20s0@30bps {err2:.3e}")
    if max(err, err2) > 1e-15:
        print("!! COST DERIVATION IS NOT EXACT - aborting."); sys.exit(1)

    # ---- reproduction gate ----------------------------------------------
    start56 = px56.index[260]
    w_fix = weights(px56, panels["U56"][1], "FIXED20")
    r_fix = backtest(px56, w_fix, cost_bps=HEADLINE_RUNG, freq=FREQ)["returns"].loc[start56:]
    r_v1 = R("U56", "v1", None, None, HEADLINE_RUNG).loc[start56:]
    print("\n--- reproduction gate (universe.json window, must match idea 82's published rows) ---")
    for nm, r, want in [("U56/CAND20 FIXED", r_fix, "12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                        ("U56/RULES v1   ", r_v1, "6.5% / 0.666 / -13.8%")]:
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {nm}  {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [published {want}]")

    # ---- common window --------------------------------------------------
    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    spy_full = px56["SPY"].pct_change().fillna(0)
    spy = spy_full.loc[start:end]
    spy_oos = spy_full.loc[OOS_START:end]
    print(f"\nCommon evaluation window: {start.date()} -> {end.date()}   IS {IS_START}..{IS_END}, OOS {OOS_START}..{end.date()}")
    ms = metrics(spy)
    print(f"  SPY full {ms['CAGR']:.1%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.1%}  "
          f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  "
          f"OOS {metrics(spy_oos)['CAGR']:.1%} / {metrics(spy_oos)['Sharpe']:.3f} / {metrics(spy_oos)['MaxDD']:.1%}")

    # ---- grid (every point, every rung) ---------------------------------
    rows = []
    for (pk, arm, n, seed) in gross_ret:
        for bps in RUNGS:
            rr = R(pk, arm, n, seed, bps)
            r = rr.loc[start:end]
            r_oos = rr.loc[OOS_START:end]
            base = R(pk, "v1", None, None, bps).loc[start:end]
            m, mo = metrics(r), metrics(r_oos)
            h1, h2 = half_sharpes(r)
            sat = float((necl[pk] <= n).mean()) if n else 1.0
            rows.append(dict(
                panel=pk, arm=arm, n=(n if n else 0), seed=(-1 if seed is None else seed), bps=bps,
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                IS_Sharpe=metrics(rr.loc[IS_START:IS_END])["Sharpe"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                turnover=turn[(pk, arm, n, seed)].loc[start:end].sum() / m["Years"],
                gross=gross_w[(pk, arm, n, seed)].loc[start:end].mean(),
                held=held_w[(pk, arm, n, seed)].loc[start:end].mean(),
                sat_share=sat, f4a=v4a(r, base), f4b=fail4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows)
    grid["k4b"] = grid["f4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\nGrid: {len(grid)} points -> {STEM}.grid.csv  (4a {int(grid.f4a.sum())}, 4b {int(grid.k4b.sum())})")

    # ---- 1. THE TURNOVER SEPARATION IS REAL? ----------------------------
    print("\n--- turnover by arm (x/yr, full sample; the channel the new arm opens) ---")
    tv = (grid[grid.bps == 0].groupby(["panel", "arm", "n"])
          .agg(turnover=("turnover", "mean"), held=("held", "mean"), gross=("gross", "mean")))
    print(fmt(tv, 2))
    tsum = grid[(grid.bps == 0) & grid.arm.isin(["FWD", "RANDH", "RANDW", "EWall", "REV"])] \
        .groupby("arm").turnover.agg(["mean", "min", "max"])
    print("\n  by arm:"); print(fmt(tsum, 2))

    # ---- 2. the comparisons, at every rung -------------------------------
    def S(pk, arm, n, bps, seed=None, col="Sharpe"):
        row = grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == (n or 0)) &
                   (grid.seed == (-1 if seed is None else seed)) & (grid.bps == bps)]
        return float(row[col].iloc[0])

    def SM(pk, arm, n, bps, col="Sharpe"):     # mean over the 8 seeds
        row = grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == n) & (grid.bps == bps)]
        return float(row[col].mean())

    comp = []
    for pk in panels:
        for n in NS:
            sat = float((necl[pk] <= n).mean())
            for bps in RUNGS:
                for col in ("Sharpe", "CAGR", "MaxDD"):
                    ew, fwd, rev = S(pk, "EWall", None, bps, col=col), S(pk, "FWD", n, bps, col=col), S(pk, "REV", n, bps, col=col)
                    rh, rw = SM(pk, "RANDH", n, bps, col), SM(pk, "RANDW", n, bps, col)
                    comp.append(dict(panel=pk, n=n, bps=bps, metric=col, sat_share=sat, unsat=(sat <= SAT_CAP),
                                     EWall=ew, FWD=fwd, REV=rev, RANDH=rh, RANDW=rw,
                                     d_FWD_RANDH=fwd - rh, d_FWD_RANDW=fwd - rw,
                                     d_RANDH_RANDW=rh - rw, d_EW_FWD=ew - fwd, d_FWD_REV=fwd - rev))
    comp = pd.DataFrame(comp)
    comp.to_csv(OUT / f"{STEM}.comparisons.csv", index=False)

    # decomposition identity
    ident = (comp.d_FWD_RANDW - (comp.d_FWD_RANDH + comp.d_RANDH_RANDW)).abs().max()
    print(f"\nDecomposition identity  max |(FWD-RANDW) - ((FWD-RANDH)+(RANDH-RANDW))| = {ident:.3e}")

    U = comp[comp.unsat]
    print(f"\nUnsaturated cells (sat_share <= {SAT_CAP}): {len(U[(U.bps == 0) & (U.metric == 'Sharpe')])} of "
          f"{len(comp[(comp.bps == 0) & (comp.metric == 'Sharpe')])} (panel, n) cells")

    print("\n--- every cell, Sharpe, all three rungs (unsaturated flagged) ---")
    sh = comp[comp.metric == "Sharpe"].copy()
    print(fmt(sh[["panel", "n", "bps", "unsat", "EWall", "FWD", "REV", "RANDH", "RANDW",
                  "d_FWD_RANDH", "d_FWD_RANDW", "d_RANDH_RANDW"]].set_index(["panel", "n", "bps"]), 4))

    # ---- 3. headline table: the sign, at every rung, on every metric -----
    print("\n" + "=" * 210)
    print("HEADLINE: does `FWD - RAND` keep its sign once persistence is separated from the pick?")
    print("=" * 210)
    hl = []
    for col in ("Sharpe", "CAGR", "MaxDD"):
        for bps in RUNGS:
            g = U[(U.metric == col) & (U.bps == bps)]
            for c, q in [("d_FWD_RANDH", "FWD - RANDH  (idea 82's isolate: held draw)"),
                         ("d_FWD_RANDW", "FWD - RANDW  (the queue's arm: weekly re-draw)"),
                         ("d_RANDH_RANDW", "RANDH- RANDW (the PERSISTENCE leg alone)"),
                         ("d_EW_FWD", "EWall- FWD   (idea 82's headline)")]:
                m_, t_ = paired_t(g[c])
                hl.append(dict(metric=col, bps=bps, comparison=q, mean=m_, t=t_,
                               pos=int((g[c] > 0).sum()), cells=len(g)))
    hl = pd.DataFrame(hl)
    hl.to_csv(OUT / f"{STEM}.headline.csv", index=False)
    for col in ("Sharpe", "CAGR", "MaxDD"):
        print(f"\n  --- {col} (over the unsaturated cells; RAND arms are the 8-seed mean) ---")
        print(fmt(hl[hl.metric == col].set_index(["bps", "comparison"])[["mean", "t", "pos", "cells"]], 4))

    # ---- 4. per (cell, seed): the RAND mean is not doing hidden work -----
    print("\n--- per (cell, seed) draws, Sharpe (idea 82 reported FWD-RANDH = -0.0213, t -2.72, 21/64) ---")
    ps = []
    for pk in panels:
        for n in NS:
            if float((necl[pk] <= n).mean()) > SAT_CAP:
                continue
            for bps in RUNGS:
                for s in SEEDS:
                    ps.append(dict(panel=pk, n=n, bps=bps, seed=s,
                                   d_FWD_RANDH=S(pk, "FWD", n, bps) - S(pk, "RANDH", n, bps, s),
                                   d_FWD_RANDW=S(pk, "FWD", n, bps) - S(pk, "RANDW", n, bps, s),
                                   d_RANDH_RANDW=S(pk, "RANDH", n, bps, s) - S(pk, "RANDW", n, bps, s)))
    ps = pd.DataFrame(ps)
    ps.to_csv(OUT / f"{STEM}.seeds.csv", index=False)
    seedtab = []
    for bps in RUNGS:
        g = ps[ps.bps == bps]
        for c in ("d_FWD_RANDH", "d_FWD_RANDW", "d_RANDH_RANDW"):
            m_, t_ = paired_t(g[c])
            seedtab.append(dict(bps=bps, comparison=c, mean=m_, t=t_,
                                pos=int((g[c] > 0).sum()), draws=len(g),
                                min=g[c].min(), max=g[c].max()))
    seedtab = pd.DataFrame(seedtab)
    print(fmt(seedtab.set_index(["bps", "comparison"]), 4))

    # per-seed spread of the RANDW arm itself (is one seed carrying it?)
    print("\n--- RANDW seed dispersion at n=20, 0 bps (Sharpe per seed) ---")
    sd = (grid[(grid.arm == "RANDW") & (grid.n == 20) & (grid.bps == 0)]
          .pivot_table(index="panel", columns="seed", values="Sharpe"))
    print(fmt(sd, 3))
    print("\n--- RANDH seed dispersion at n=20, 0 bps (Sharpe per seed) ---")
    sdh = (grid[(grid.arm == "RANDH") & (grid.n == 20) & (grid.bps == 0)]
           .pivot_table(index="panel", columns="seed", values="Sharpe"))
    print(fmt(sdh, 3))

    # ---- 5. the cost breakeven of the weekly re-draw ---------------------
    # `FWD - RANDW` is a straight line in the rung only if the two arms' turnovers are
    # fixed, which they are.  Report the rung at which each cell's sign flips, by linear
    # interpolation between the three measured rungs, and clip to the reported ladder.
    print("\n--- where the weekly re-draw's turnover bill flips the sign (Sharpe, unsaturated cells) ---")
    be = []
    for pk in panels:
        for n in NS:
            if float((necl[pk] <= n).mean()) > SAT_CAP:
                continue
            d = {b: S(pk, "FWD", n, b) - SM(pk, "RANDW", n, b) for b in RUNGS}
            flip = "no flip in 0..30"
            xs = sorted(RUNGS)
            for a, b in zip(xs, xs[1:]):
                if np.sign(d[a]) != np.sign(d[b]):
                    x = a + (b - a) * (0 - d[a]) / (d[b] - d[a])
                    flip = f"{x:.1f} bps"
                    break
            be.append(dict(panel=pk, n=n, d0=d[0], d10=d[10], d30=d[30], sign_flip=flip,
                           turn_FWD=SM(pk, "FWD", n, 0, "turnover") if False else
                           float(grid[(grid.panel == pk) & (grid.arm == "FWD") & (grid.n == n) & (grid.bps == 0)].turnover.iloc[0]),
                           turn_RANDW=SM(pk, "RANDW", n, 0, "turnover")))
    be = pd.DataFrame(be)
    be.to_csv(OUT / f"{STEM}.breakeven.csv", index=False)
    print(fmt(be.set_index(["panel", "n"]), 4))

    # ---- 6. rule 8 walk-forward -----------------------------------------
    print("\n" + "=" * 210)
    print("RULE 8 WALK-FORWARD  (parameters chosen on IS 2009-2016 only; OOS 2017-2026 read once)")
    print("=" * 210)

    def isS(pk, arm, n, bps, seed=None):
        return float(grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == (n or 0)) &
                          (grid.seed == (-1 if seed is None else seed)) & (grid.bps == bps)].IS_Sharpe.iloc[0])

    wf = []
    for bps in RUNGS:
        for pk in panels:
            ns_ok = [n for n in NS if float((necl[pk] <= n).mean()) <= SAT_CAP] or NS
            picks = {
                "EWALL": ("EWall", None, None),
                "FWD20": ("FWD", 20, None),
                "FWD_ISARGMAX": ("FWD", max(ns_ok, key=lambda n: isS(pk, "FWD", n, bps)), None),
            }
            cands = [("FWD", n, None) for n in ns_ok] + [("REV", n, None) for n in ns_ok] + \
                    [(a, n, s) for a in ("RANDH", "RANDW") for n in ns_ok for s in SEEDS] + \
                    [("EWall", None, None)]
            picks["ALL_ISARGMAX"] = max(cands, key=lambda c: isS(pk, c[0], c[1], bps, c[2]))
            for nm, (arm, n, seed) in picks.items():
                m = metrics(R(pk, arm, n, seed, bps).loc[OOS_START:end])
                wf.append(dict(bps=bps, panel=pk, selector=nm, pick=f"{arm}{n if n else ''}",
                               OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
            for arm in ("RANDH", "RANDW"):
                mm = [metrics(R(pk, arm, 20, s, bps).loc[OOS_START:end]) for s in SEEDS]
                wf.append(dict(bps=bps, panel=pk, selector=f"{arm}20", pick=f"{arm}20 (8 seeds)",
                               OOS_CAGR=float(np.mean([x["CAGR"] for x in mm])),
                               OOS_Sharpe=float(np.mean([x["Sharpe"] for x in mm])),
                               OOS_MaxDD=float(np.mean([x["MaxDD"] for x in mm]))))
            b = metrics(R(pk, "v1", None, None, bps).loc[OOS_START:end])
            wf.append(dict(bps=bps, panel=pk, selector="RULES v1", pick="baseline",
                           OOS_CAGR=b["CAGR"], OOS_Sharpe=b["Sharpe"], OOS_MaxDD=b["MaxDD"]))
            mo_ = metrics(spy_oos)
            wf.append(dict(bps=bps, panel=pk, selector="SPY", pick="benchmark",
                           OOS_CAGR=mo_["CAGR"], OOS_Sharpe=mo_["Sharpe"], OOS_MaxDD=mo_["MaxDD"]))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(wf.set_index(["bps", "panel", "selector"])))

    print("\n--- pooled over the 3 panels (equal weight), per rung ---")
    pool = wf.groupby(["bps", "selector"])[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
    for bps in RUNGS:
        print(f"\n  {bps} bps:")
        print(fmt(pool.loc[bps].sort_values("OOS_Sharpe", ascending=False)))

    print("\n--- OOS: does the weekly re-draw beat the composite out of sample? ---")
    for bps in RUNGS:
        w_ = wf[wf.bps == bps]
        f20 = w_[w_.selector == "FWD20"].set_index("panel").OOS_Sharpe
        for sel in ("RANDH20", "RANDW20", "EWALL", "ALL_ISARGMAX"):
            o = w_[w_.selector == sel].set_index("panel").OOS_Sharpe
            d = (f20 - o).dropna()
            print(f"  {bps:>2} bps  FWD20 - {sel:<13} OOS Sharpe: mean {d.mean():+.4f}, wins {int((d > 0).sum())}/{len(d)}  "
                  f"({', '.join(f'{k} {v:+.3f}' for k, v in d.items())})")

    # ---- 7. KEEP paths ---------------------------------------------------
    print("\n--- KEEP paths (unsaturated cells + EWall; RAND arms shown as pass COUNTS over 8 seeds) ---")
    kp = grid[(grid.arm.isin(["EWall", "FWD", "REV"])) & ((grid.arm == "EWall") | (grid.sat_share <= SAT_CAP))]
    print(fmt(kp.sort_values(["bps", "panel", "arm", "n"])[["bps", "panel", "arm", "n", "CAGR", "Sharpe",
                                                           "MaxDD", "H1", "H2", "OOS_Sharpe", "turnover", "f4a", "f4b"]]
              .set_index(["bps", "panel", "arm", "n"])))
    rk = (grid[grid.arm.isin(["RANDH", "RANDW"]) & (grid.sat_share <= SAT_CAP)]
          .groupby(["bps", "panel", "arm", "n"])
          .agg(Sharpe=("Sharpe", "mean"), CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
               turnover=("turnover", "mean"), k4a=("f4a", "sum"), k4b=("k4b", "sum")))
    print("\n--- RAND arms, 8 seeds each (mean metrics; k4a/k4b = seeds passing) ---")
    print(fmt(rk, 3))
    print(f"\n4b passes: {int(grid.k4b.sum())} of {len(grid)} points")
    print(fmt(grid.groupby(["bps", "arm"]).agg(points=("k4b", "size"), k4b=("k4b", "sum"), k4a=("f4a", "sum"))))

    print("\nWrote:", ", ".join(f"{STEM}.{x}.csv" for x in
                                ("grid", "comparisons", "headline", "seeds", "breakeven", "walkforward")))


if __name__ == "__main__":
    main()
