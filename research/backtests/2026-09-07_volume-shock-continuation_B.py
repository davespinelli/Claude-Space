#!/usr/bin/env python3
"""Idea 34 - "volume-shock-continuation": does the Gervais-Kaniel-Mingelgrin (2001)
high-volume return premium exist in the sub-$2B small-cap panel, and does the VOLUME leg
add anything at all to the RETURN leg it is bundled with?

The question
------------
GKM's claim is that a stock whose trading volume is abnormally HIGH becomes more visible,
and that visibility is worth a positive return over the following weeks - the effect being
larger in small caps.  The queue's wording is the standard modern form: abnormal volume
(20d mean vs 120d mean) combined with the sign of the accompanying return, held 1 week /
1 month / 3 months, continuation vs reversal.

The trap this script is built to avoid
--------------------------------------
"High volume AND positive return" is TWO signals stapled together, and the second one is
just 20-day price momentum, which this record has already priced many times.  A book built
on the pair can beat the panel while the volume leg contributes nothing (or less than
nothing).  So the grid is always run beside two structural controls that hold everything
else fixed and delete one leg each:

    RET-ONLY(h)     positive 20d return, NO volume condition, same holding period
    VOL-ONLY(s,h)   volume shock at threshold s, EITHER return sign, same holding period

The reportable quantity is not the book's Sharpe.  It is
    volume increment  = Sharpe(UP arm) - Sharpe(RET-ONLY) at matched h
    return increment  = Sharpe(UP arm) - Sharpe(VOL-ONLY) at matched (s, h)
Idea 34 is a VOLUME idea, so it only survives if the volume increment is positive.

The rule family
---------------
    AV_t   = mean(volume, 20d) / mean(volume, 120d)          (per name, causal)
    R_t    = px_t / px_{t-20} - 1                            (same 20d window)
    trigger(UP)   : AV_t >= s  and  R_t > 0
    trigger(DOWN) : AV_t >= s  and  R_t < 0                  (the reversal arm)
    held on day t : a trigger fired on any of the last h trading days
    weights       : equal weight over held names, renormalised to a CONSTANT 75% gross
                    (idea 81: the gross convention, not the signal, drives most cross-book
                    spreads, so it is pinned); no names held -> cash.

Tuned parameters (PROTOCOL rule 4: at most two) - s and h.  ALL 12 (s, h) points reported,
for BOTH sign arms (24 cells), plus 7 controls.  Nothing else is searched: the 20d/120d
volume windows, the 20d return window, 75% gross, weekly rebalance, 10 bps, next-day
execution and the panel are all fixed in advance.

Cost rungs
----------
Idea 47 found every 4b pass in this record sits at or below PROTOCOL's own 10 bps anchor,
and a 1-week holding period churns hard, so 0 / 10 / 25 bps are all reported.  Costs are
derived analytically from one zero-cost run per book (engine.backtest's drift path does not
depend on cost_bps), and that identity is CHECKED against engine.backtest at 10 bps to
max|diff| < 1e-12 before any result is read.

Verdicts (both KEEP paths, every cell, at the 10 bps anchor)
    4a: Sharpe > the LIVE book (RULES v2 on this panel) in BOTH halves AND MaxDD no worse.
    4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Rule 8 walk-forward (required): (s, h) chosen by IS Sharpe on 2010-2016 alone, then
2017-2026 read once, per sign arm and per cost rung.  Reported against the OOS-best cell of
the same pool (the chooser's regret) and against the pool mean (is the chooser a coin?).

Data
----
data/prices_small.csv.gz + data/volume_small.csv.gz via baseline.load_universe(small=True)
and baseline.load_volume(small=True).  The 44 tickers flagged with max_1d_move >= 1.0 in
data/small_meta.csv are DROPPED before anything is computed (the README's own instruction:
an unfiltered momentum/reversal test is otherwise dominated by unadjusted level steps) ->
SMALL439.  SPY is a benchmark column only and is never held.

SURVIVORSHIP: the panel is the CURRENT constituent list of a sub-$2B screen, so every name
survived the whole sample by construction.  Absolute returns here are biased upward, and
the bias is worst exactly for a signal that fires on distressed high-volume names.  Only
the increments (UP vs RET-ONLY vs VOL-ONLY on the same panel) are trustworthy.

Deterministic, standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, load_volume, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics

FREQ = "W"
GROSS = 0.75
COST_RUNGS = [0, 10, 25]
ANCHOR = 10                 # PROTOCOL's cost anchor; verdicts are read here
BAD_MOVE = 1.0              # data/SMALL_PANEL_README.md's own exclusion threshold
VOL_SHORT, VOL_LONG = 20, 120
RET_WIN = 20
SS = [1.25, 1.50, 2.00, 3.00]       # tuned parameter 1: volume-shock threshold
HS = [5, 21, 63]                    # tuned parameter 2: holding period (1w / 1m / 3m)
S_CTRL = 1.50                       # threshold used by the VOL-ONLY control (mid-grid, fixed)
SEEDS = [1, 2, 3, 4, 5]             # count-matched random control (fixed in advance)
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SCRIPT = Path(__file__).name

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- data ----
def panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = sorted(set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"]))
    px = px[[c for c in px.columns if c not in bad]]
    sel = px.drop(columns=["SPY"])                       # SPY is benchmark only, never held
    vol = load_volume(small=True).reindex(index=px.index, columns=sel.columns)
    vol = vol.mask(vol <= 0)                             # zero bars are missing, not real
    return px, sel, vol, bad


def signals(sel, vol):
    """AV_t (abnormal volume) and R_t (20d return), both causal and both NaN until their
    full windows exist.  A name with a NaN price or a NaN AV can never trigger."""
    v_s = vol.rolling(VOL_SHORT, min_periods=VOL_SHORT).mean()
    v_l = vol.rolling(VOL_LONG, min_periods=VOL_LONG).mean()
    av = v_s / v_l.where(v_l > 0)
    r = sel / sel.shift(RET_WIN) - 1
    live = sel.notna() & sel.shift(RET_WIN).notna()
    return av.where(live), r.where(live)


# ------------------------------------------------------------- weights ----
def hold_from_trigger(trig, h):
    """A name is held on day t if it triggered on any of the last h trading days
    (t included).  Rolling max of a 0/1 frame - strictly backward looking."""
    return trig.astype(float).rolling(h, min_periods=1).max() > 0


def eqw(held, index, columns):
    """Equal weight over held names at a CONSTANT 75% gross; cash when nothing is held."""
    n = held.sum(axis=1)
    w = held.astype(float).div(n.replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    return w.reindex(index=index, columns=columns).fillna(0.0)


def trigger(sel, av, r, kind, s=None):
    if kind == "UP":
        t = (av >= s) & (r > 0)
    elif kind == "DOWN":
        t = (av >= s) & (r < 0)
    elif kind == "RET":                      # return leg alone
        t = r > 0
    elif kind == "VOL":                      # volume leg alone, either sign
        t = (av >= s) & r.notna()
    else:
        raise ValueError(kind)
    return t.where(av.notna() & r.notna(), False)


def book(sel, av, r, kind, s=None, h=None, index=None, columns=None):
    if kind == "EWALL":                      # the panel itself
        return eqw(sel.notna(), index, columns)
    return eqw(hold_from_trigger(trigger(sel, av, r, kind, s), h), index, columns)


def rand_count(w_ref, valid, seed, index, columns):
    """COUNT-MATCHED RANDOM CONTROL.  On every day, hold the SAME NUMBER of names the
    reference book holds, drawn uniformly and INDEPENDENTLY from the names that are
    investable that day.  Separates a volume premium from the mechanical effect of holding
    a smaller, more concentrated book.  It does NOT match turnover - an independent daily
    draw rotates the whole book every rebalance - so it is only readable at 0 bps."""
    n = (w_ref.reindex(columns=valid.columns).fillna(0.0) > 1e-12).sum(axis=1)
    rng = np.random.default_rng(seed)
    u = pd.DataFrame(rng.random(valid.shape), index=valid.index, columns=valid.columns)
    rank = u.where(valid).rank(axis=1, ascending=False)
    held = rank.le(n.reindex(valid.index).fillna(0.0).clip(lower=0), axis=0)
    return eqw(held.fillna(False) & (n.values[:, None] > 0), index, columns)


def rand_rate(trig, valid, h, seed, index, columns):
    """TURNOVER-MATCHED RANDOM CONTROL (the null that can be read at any cost rung).
    Replace the real trigger with a Bernoulli trigger of the SAME unconditional rate p,
    then hold it for the SAME h days.  Matching the trigger rate and the holding period
    matches BOTH the book's size and its churn in expectation, so what is left is the
    only thing the signal claims: that the names it picks are better than random names
    picked at the same rate and held the same way."""
    p = float(trig.where(valid).sum().sum() / valid.sum().sum())
    rng = np.random.default_rng(10_000 + seed)
    u = pd.DataFrame(rng.random(valid.shape), index=valid.index, columns=valid.columns)
    return eqw(hold_from_trigger((u < p) & valid, h), index, columns)


# ----------------------------------------------------------- simulation ----
def run_zero(px, w):
    """One zero-cost run; costs at any rung are returns0 - turnover * bps / 1e4."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"], res["turnover"], res["weights"]


def at_cost(r0, turn, bps):
    return r0 - turn * bps / 1e4


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def tests_4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    mo, mso = metrics(r.loc[OOS_START:]), metrics(spy.loc[OOS_START:])
    return {"H1": h1 > s1, "H2": h2 > s2, "OOS": mo["Sharpe"] > mso["Sharpe"],
            "DD": abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
            "CAGR": m["CAGR"] >= 0.70 * ms["CAGR"]}


def fail_4b(r, spy):
    f = [k for k, v in tests_4b(r, spy).items() if not v]
    return ",".join(f) if f else "-"


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def summarise(name, r, turn, held, spy, base):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(book=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
             OOS_MaxDD=mo["MaxDD"],
             p4a=verdict_4a(r, base), p4b=all(tests_4b(r, spy).values()),
             fail4b=fail_4b(r, spy))
    if held is not None:
        d["names"] = float((held > 1e-12).sum(axis=1).mean())
        d["turn"] = float(turn.sum() / m["Years"])
    return d


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- main ----
def main():
    px, sel, vol, bad = panel()
    av, r20 = signals(sel, vol)
    idx, cols = px.index, px.columns
    start = px.index[260]                                # warm-up skip, as baseline.compare
    yrs = px.index.to_series().groupby(px.index.year).count()

    print("=" * 170)
    print(f"Idea 34 volume-shock-continuation (lane B) | {SCRIPT}")
    print("=" * 170)
    print(f"Panel SMALL439: {sel.shape[1]} names + SPY benchmark, "
          f"{px.index[0].date()} -> {px.index[-1].date()}; {len(bad)} names dropped for "
          f"max_1d_move >= {BAD_MOVE:.0%}")
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
    if yrs.loc[2013:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting.")
        sys.exit(1)
    print(f"Eval sample {start.date()} -> {px.index[-1].date()} | IS <= {IS_END}, "
          f"OOS >= {OOS_START}")
    print(f"Fixed, not searched: vol windows {VOL_SHORT}d/{VOL_LONG}d, return window "
          f"{RET_WIN}d, gross {GROSS:.0%}, weekly, next-day fill, panel.")
    print(f"Tuned (2): s in {SS} x h in {HS} = {len(SS)*len(HS)} points, BOTH sign arms, "
          f"ALL reported. Cost rungs {COST_RUNGS} bps; verdicts read at {ANCHOR} bps.")
    print("SURVIVORSHIP: current-constituent sub-$2B screen. Absolute returns biased UP; "
          "only the leg increments are durable.\n")

    # ---- premise: does an abnormal-volume shock happen often enough to build a book?
    avv = av.loc[start:]
    print("=" * 170)
    print("PREMISE - the signal's own frequency.  If the shock is too rare the book is a "
          "handful of names and the test is about idiosyncratic noise, not a premium.")
    prem = pd.DataFrame({
        "AV>=s share of name-days": [float((avv >= s).sum().sum() / avv.notna().sum().sum())
                                     for s in SS],
        "mean names triggering/day": [float((avv >= s).sum(axis=1).mean()) for s in SS],
    }, index=[f"s={s:.2f}" for s in SS])
    print(fmt(prem))
    print(f"  AV_t distribution over all name-days: median {float(avv.stack().median()):.3f}, "
          f"p90 {float(avv.stack().quantile(0.90)):.3f}, "
          f"p99 {float(avv.stack().quantile(0.99)):.3f}")
    up_share = float(((r20.loc[start:] > 0) & (avv >= S_CTRL)).sum().sum() /
                     (avv >= S_CTRL).sum().sum())
    print(f"  conditional on AV>={S_CTRL:.2f}, the 20d return is POSITIVE on "
          f"{up_share:.1%} of triggering name-days (unconditional base rate "
          f"{float((r20.loc[start:] > 0).sum().sum() / r20.loc[start:].notna().sum().sum()):.1%})")
    print()

    # ---- benchmarks
    spy_r = px["SPY"].pct_change().fillna(0.0)
    base0, base_t, _ = run_zero(px, rules_v2_weights(px))
    v1_0, v1_t, _ = run_zero(px, rules_v1_weights(px))

    # ---- identity check: analytic costs vs engine.backtest at the anchor
    probe_w = book(sel, av, r20, "UP", s=1.50, h=21, index=idx, columns=cols)
    p0, pt, _ = run_zero(px, probe_w)
    p_engine = backtest(px, probe_w, cost_bps=ANCHOR, freq=FREQ)["returns"]
    dmax = float((at_cost(p0, pt, ANCHOR) - p_engine).abs().max())
    print(f"COST IDENTITY CHECK (UP s=1.50 h=21 @ {ANCHOR} bps): "
          f"max|analytic - engine| = {dmax:.3e}")
    if dmax > 1e-12:
        print("!! cost identity failed - aborting.")
        sys.exit(1)
    print()

    # ---- build every book once, at zero cost
    books = {}
    for s in SS:
        for h in HS:
            for kind in ("UP", "DOWN"):
                books[(kind, s, h)] = book(sel, av, r20, kind, s=s, h=h,
                                           index=idx, columns=cols)
    for h in HS:
        books[("RET", np.nan, h)] = book(sel, av, r20, "RET", h=h, index=idx, columns=cols)
        books[("VOL", S_CTRL, h)] = book(sel, av, r20, "VOL", s=S_CTRL, h=h,
                                         index=idx, columns=cols)
    books[("EWALL", np.nan, np.nan)] = book(sel, av, r20, "EWALL", index=idx, columns=cols)

    # count-matched random controls for the three books the discussion turns on
    valid = av.notna() & r20.notna() & sel.notna()
    rand_refs = [("UP", 1.50, 21), ("UP", 2.00, 21), ("VOL", S_CTRL, 21)]
    for ref in rand_refs:
        tr = trigger(sel, av, r20, ref[0], ref[1])
        for seed in SEEDS:
            books[("RANDC", ref, seed)] = rand_count(books[ref], valid, seed, idx, cols)
            books[("RANDT", ref, seed)] = rand_rate(tr, valid, ref[2], seed, idx, cols)

    raw = {}
    for key, w in books.items():
        r0, t0, held = run_zero(px, w)
        raw[key] = (r0.loc[start:], t0.loc[start:], held.loc[start:])

    # ---- the full grid, at every cost rung
    rows, rand_rows = [], []
    series = {}
    for bps in COST_RUNGS:
        spy = spy_r.loc[start:]
        base = at_cost(base0, base_t, bps).loc[start:]
        v1 = at_cost(v1_0, v1_t, bps).loc[start:]
        for key, (r0, t0, held) in raw.items():
            kind, s, h = key
            rr = at_cost(r0, t0, bps)
            series[(bps,) + key] = rr
            if kind in ("RANDC", "RANDT"):
                ref, seed = s, h
                nm = f"{kind}[{ref[0]} s{ref[1]:.2f} h{ref[2]:g}] seed{seed}"
                rand_rows.append(dict(bps=bps, null=kind,
                                      ref=f"{ref[0]} s{ref[1]:.2f} h{ref[2]:g}", seed=seed,
                                      **summarise(nm, rr, t0, held, spy, base)))
                continue
            nm = (f"{kind} s{s:.2f} h{h:g}" if kind in ("UP", "DOWN", "VOL")
                  else (f"{kind} h{h:g}" if kind == "RET" else kind))
            rows.append(dict(bps=bps, kind=kind, s=s, h=h,
                             **summarise(nm, rr, t0, held, spy, base)))
        for nm, rr in (("RULES v2 (live)", base), ("RULES v1", v1), ("SPY", spy)):
            rows.append(dict(bps=bps, kind="bench", s=np.nan, h=np.nan,
                             **summarise(nm, rr, pd.Series(0.0, index=rr.index), None,
                                         spy, base)))
    grid = pd.DataFrame(rows)

    cols_show = ["book", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_CAGR",
                 "OOS_Sharpe", "OOS_MaxDD", "names", "turn", "p4a", "p4b", "fail4b"]
    for bps in COST_RUNGS:
        g = grid[grid.bps == bps]
        print("=" * 170)
        print(f"FULL GRID at {bps} bps - all {int((g.kind.isin(['UP','DOWN'])).sum())} tuned "
              f"cells + controls + benchmarks (verdicts are only meaningful at {ANCHOR} bps)")
        print("=" * 170)
        print(fmt(g[cols_show].set_index("book")))
        print(f"  4a passes {int(g[g.kind.isin(['UP','DOWN'])].p4a.sum())}/"
              f"{int(g.kind.isin(['UP','DOWN']).sum())}   4b passes "
              f"{int(g[g.kind.isin(['UP','DOWN'])].p4b.sum())}/"
              f"{int(g.kind.isin(['UP','DOWN']).sum())}")
        print()

    # ---- THE test: does the volume leg add anything?
    print("=" * 170)
    print("LEG ATTRIBUTION - the reportable quantity.  volume increment = Sharpe(UP s,h) - "
          "Sharpe(RET-ONLY h); return increment = Sharpe(UP s,h) - Sharpe(VOL-ONLY 1.50,h).")
    print("Idea 34 is a VOLUME claim, so it lives or dies on the FIRST column's sign.")
    print("=" * 170)
    att = []
    for bps in COST_RUNGS:
        for s in SS:
            for h in HS:
                up = metrics(series[(bps, "UP", s, h)])
                ret = metrics(series[(bps, "RET", np.nan, h)])
                volo = metrics(series[(bps, "VOL", S_CTRL, h)])
                ew = metrics(series[(bps, "EWALL", np.nan, np.nan)])
                att.append(dict(bps=bps, s=s, h=h,
                                dS_vs_RETONLY=up["Sharpe"] - ret["Sharpe"],
                                dCAGR_vs_RETONLY=up["CAGR"] - ret["CAGR"],
                                dS_vs_VOLONLY=up["Sharpe"] - volo["Sharpe"],
                                dS_vs_EWALL=up["Sharpe"] - ew["Sharpe"]))
    A = pd.DataFrame(att)
    print(fmt(A.set_index(["bps", "s", "h"])))
    for bps in COST_RUNGS:
        a = A[A.bps == bps]
        print(f"  {bps:>2} bps: volume increment positive in {int((a.dS_vs_RETONLY > 0).sum())}"
              f"/{len(a)} cells, mean {a.dS_vs_RETONLY.mean():+.4f}, "
              f"median {a.dS_vs_RETONLY.median():+.4f}, "
              f"range [{a.dS_vs_RETONLY.min():+.4f}, {a.dS_vs_RETONLY.max():+.4f}]  |  "
              f"return increment positive in {int((a.dS_vs_VOLONLY > 0).sum())}/{len(a)}, "
              f"mean {a.dS_vs_VOLONLY.mean():+.4f}")
    print()

    # ---- count-matched random control: premium, or just a smaller book?
    print("=" * 170)
    print("RANDOM NULLS - two of them, 5 seeds each.  RANDC holds the same NUMBER of names,")
    print("drawn independently each day (matches size, NOT churn -> only readable at 0 bps).")
    print("RANDT fires a Bernoulli trigger at the SAME RATE and holds it h days (matches size")
    print("AND churn -> readable at every rung).  This is what separates a volume PREMIUM from")
    print("the mechanical effect of holding a smaller or a slower book.")
    print("=" * 170)
    R = pd.DataFrame(rand_rows)
    print(fmt(R.groupby(["null", "bps", "ref"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                                 "OOS_Sharpe", "names", "turn"]]
              .agg(["mean", "std"])))
    comp = []
    for null in ("RANDC", "RANDT"):
        for bps in COST_RUNGS:
            for ref in rand_refs:
                nm = f"{ref[0]} s{ref[1]:.2f} h{ref[2]:g}"
                sig = metrics(series[(bps,) + ref])
                sig_t = float(raw[ref][1].sum() / sig["Years"])
                pool = R[(R.null == null) & (R.bps == bps) & (R.ref == nm)]
                comp.append(dict(null=null, bps=bps, book=nm, sig_Sharpe=sig["Sharpe"],
                                 null_mean=pool.Sharpe.mean(), null_sd=pool.Sharpe.std(),
                                 null_max=pool.Sharpe.max(),
                                 dSharpe=sig["Sharpe"] - pool.Sharpe.mean(),
                                 z=((sig["Sharpe"] - pool.Sharpe.mean()) / pool.Sharpe.std()
                                    if pool.Sharpe.std() > 0 else np.nan),
                                 beats_all=bool(sig["Sharpe"] > pool.Sharpe.max()),
                                 sig_turn=sig_t, null_turn=pool.turn.mean(),
                                 turn_ratio=pool.turn.mean() / sig_t if sig_t else np.nan))
    CMP = pd.DataFrame(comp)
    print()
    print(fmt(CMP.set_index(["null", "bps", "book"])))
    print("  TURNOVER FIDELITY is the column that licenses the reading: RANDC's turn_ratio is "
          "far from 1 (an independent daily draw rotates the whole book), RANDT's is near 1.")
    print()

    # ---- continuation vs reversal, the queue's literal question
    print("=" * 170)
    print("CONTINUATION vs REVERSAL (the queue's literal question): UP minus DOWN at matched "
          "(s, h).  A positive number is GKM continuation; a negative one is reversal.")
    print("=" * 170)
    cr = []
    for bps in COST_RUNGS:
        for s in SS:
            for h in HS:
                u, d = metrics(series[(bps, "UP", s, h)]), metrics(series[(bps, "DOWN", s, h)])
                cr.append(dict(bps=bps, s=s, h=h, UP_Sharpe=u["Sharpe"], DOWN_Sharpe=d["Sharpe"],
                               dSharpe=u["Sharpe"] - d["Sharpe"],
                               UP_CAGR=u["CAGR"], DOWN_CAGR=d["CAGR"],
                               dCAGR=u["CAGR"] - d["CAGR"]))
    C = pd.DataFrame(cr)
    print(fmt(C.set_index(["bps", "s", "h"])))
    for bps in COST_RUNGS:
        c = C[C.bps == bps]
        print(f"  {bps:>2} bps: UP beats DOWN on Sharpe in {int((c.dSharpe > 0).sum())}/{len(c)}"
              f" cells, mean dSharpe {c.dSharpe.mean():+.4f}, mean dCAGR "
              f"{c.dCAGR.mean():+.2%}")
    print()

    # ---- horizon shape (the 1w / 1m / 3m question), pooled over s
    print("=" * 170)
    print("HOLDING-HORIZON SHAPE at the anchor - mean over the four thresholds")
    print("=" * 170)
    g10 = grid[(grid.bps == ANCHOR) & grid.kind.isin(["UP", "DOWN"])]
    print(fmt(g10.groupby(["kind", "h"])[["CAGR", "Sharpe", "MaxDD", "names", "turn"]].mean()))
    print()

    # ---- rule 8 walk-forward
    print("=" * 170)
    print("RULE 8 WALK-FORWARD - (s, h) chosen by IS Sharpe on 2010..2016 alone, 2017-2026 "
          "read once.  Reported against the pool's OOS best (regret) and pool mean (coin).")
    print("=" * 170)
    wf = []
    for bps in COST_RUNGS:
        spy = spy_r.loc[start:]
        base = at_cost(base0, base_t, bps).loc[start:]
        spy_o, base_o = spy.loc[OOS_START:], base.loc[OOS_START:]
        for kind in ("UP", "DOWN"):
            pool = {(s, h): series[(bps, kind, s, h)] for s in SS for h in HS}
            is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in pool.items()}
            oo = {k: metrics(v.loc[OOS_START:]) for k, v in pool.items()}
            pick = max(is_s, key=is_s.get)
            best = max(oo, key=lambda k: oo[k]["Sharpe"])
            wf.append(dict(
                bps=bps, arm=kind, pick=f"s{pick[0]:.2f} h{pick[1]:g}",
                IS_Sharpe=is_s[pick], OOS_CAGR=oo[pick]["CAGR"], OOS_Sharpe=oo[pick]["Sharpe"],
                OOS_MaxDD=oo[pick]["MaxDD"],
                pool_mean_OOS_S=float(np.mean([m["Sharpe"] for m in oo.values()])),
                best=f"s{best[0]:.2f} h{best[1]:g}", best_OOS_S=oo[best]["Sharpe"],
                regret=oo[best]["Sharpe"] - oo[pick]["Sharpe"],
                picked_best=pick == best,
                base_OOS_S=metrics(base_o)["Sharpe"], spy_OOS_S=metrics(spy_o)["Sharpe"],
                base_OOS_CAGR=metrics(base_o)["CAGR"], spy_OOS_CAGR=metrics(spy_o)["CAGR"],
                spy_OOS_MaxDD=metrics(spy_o)["MaxDD"], base_OOS_MaxDD=metrics(base_o)["MaxDD"]))
    W = pd.DataFrame(wf)
    print(fmt(W.set_index(["bps", "arm"])))
    print(f"  IS chooser picked the OOS-best cell in {int(W.picked_best.sum())}/{len(W)} "
          f"(chance = {len(W)/12:.1f}); beat its own pool mean in "
          f"{int((W.OOS_Sharpe > W.pool_mean_OOS_S).sum())}/{len(W)}")
    print()

    # ---- capacity, so the number is not a paper number (idea 121's criterion)
    print("=" * 170)
    print("CAPACITY (idea 121's criterion): p25 of the held names' 20d median DOLLAR volume, "
          "and what a $10M trade would be as a share of it.")
    print("=" * 170)
    dv20 = (sel * vol).rolling(20).median()
    cap = []
    for s in (1.50, 3.00):
        for h in HS:
            held = raw[("UP", s, h)][2].reindex(columns=sel.columns).fillna(0.0)
            mask = held > 1e-12
            d = dv20.loc[start:].where(mask.loc[start:])
            p25 = float(np.nanquantile(d.values[np.isfinite(d.values)], 0.25))
            cap.append(dict(book=f"UP s{s:.2f} h{h:g}", p25_dollar_ADV=p25,
                            share_of_p25_for_10M=1e7 / p25 if p25 > 0 else np.nan))
    print(pd.DataFrame(cap).set_index("book").to_string(
        float_format=lambda x: f"{x:,.3f}"))
    print()

    # ---- leaderboard rows
    print("=" * 170)
    print("LEADERBOARD ROWS")
    print("=" * 170)
    g = grid[grid.bps == ANCHOR].set_index("book")
    b = g.loc["RULES v2 (live)"]
    sp = g.loc["SPY"]
    def row(label, key, note):
        d = g.loc[key]
        return (f"| 2026-09-07 | 34 {label} | {d.CAGR:.1%} | {d.Sharpe:.2f} | {d.MaxDD:.1%} | "
                f"{d.H1:.2f} / {d.H2:.2f} | RULES v2 {b.Sharpe:.2f} ({b.H1:.2f}/{b.H2:.2f}), "
                f"SPY {sp.Sharpe:.2f} ({sp.H1:.2f}/{sp.H2:.2f}) | {note} | {SCRIPT} |")
    wf10 = W[(W.bps == ANCHOR)]
    print(row("UP s1.50 h21 (mid-grid continuation book), SMALL439 @10bps", "UP s1.50 h21",
              "KILL — see script"))
    print(row("RET-ONLY h21 control (return leg alone, no volume condition)", "RET h21",
              "control"))
    print(row("VOL-ONLY s1.50 h21 control (volume leg alone, either return sign)",
              "VOL s1.50 h21", "control"))
    print(row("EWALL control (all 439 names, 75% gross)", "EWALL", "control"))
    print(wf10.set_index("arm")[["pick", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                 "best", "best_OOS_S", "regret", "picked_best"]].to_string())

    # ---- verdict summary
    print()
    print("=" * 170)
    a10 = A[A.bps == ANCHOR]
    c10 = C[C.bps == ANCHOR]
    n_t = int(grid[(grid.bps == ANCHOR) & grid.kind.isin(["UP", "DOWN"])].shape[0])
    print(f"SUMMARY @ {ANCHOR} bps: 4a "
          f"{int(grid[(grid.bps == ANCHOR) & grid.kind.isin(['UP','DOWN'])].p4a.sum())}/{n_t}, "
          f"4b {int(grid[(grid.bps == ANCHOR) & grid.kind.isin(['UP','DOWN'])].p4b.sum())}/{n_t}")
    print(f"  volume increment vs RET-ONLY: {int((a10.dS_vs_RETONLY > 0).sum())}/{len(a10)} "
          f"positive, mean {a10.dS_vs_RETONLY.mean():+.4f} Sharpe, "
          f"{a10.dCAGR_vs_RETONLY.mean():+.2%} CAGR")
    print(f"  continuation vs reversal: UP > DOWN in {int((c10.dSharpe > 0).sum())}/{len(c10)}, "
          f"mean {c10.dSharpe.mean():+.4f} Sharpe")
    k10 = CMP[(CMP.bps == ANCHOR) & (CMP.null == "RANDT")]
    k0 = CMP[(CMP.bps == 0) & (CMP.null == "RANDC")]
    print(f"  vs TURNOVER-matched null (RANDT @ {ANCHOR} bps): signal beats the null mean in "
          f"{int((k10.dSharpe > 0).sum())}/{len(k10)} books, mean dSharpe "
          f"{k10.dSharpe.mean():+.4f}, beats ALL 5 seeds in {int(k10.beats_all.sum())}/{len(k10)}"
          f" (turnover ratio {k10.turn_ratio.mean():.2f}x)")
    print(f"  vs COUNT-matched null (RANDC @ 0 bps): beats the null mean in "
          f"{int((k0.dSharpe > 0).sum())}/{len(k0)}, mean dSharpe {k0.dSharpe.mean():+.4f}, "
          f"beats ALL 5 seeds in {int(k0.beats_all.sum())}/{len(k0)}")
    print(f"  4b failure reasons @ {ANCHOR} bps: "
          f"{grid[(grid.bps == ANCHOR) & grid.kind.isin(['UP','DOWN'])].fail4b.value_counts().to_dict()}")
    print("=" * 170)


if __name__ == "__main__":
    main()
