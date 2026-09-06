#!/usr/bin/env python3
"""Idea 82 - "ranking-subtracts-value" (lane B, 2026-09-06).

The question
------------
Idea 73's blunt finding: the GROSS-MATCHED ranking premium is negative in 16 of 21
(panel, n) cells and in 132 of 150 random sub-panels -- on large-cap panels the composite
ranking appears to DESTROY value against equal-weighting the same eligible set, and only
the eligibility GATE earns anything.  The queue asks for the strong version, directly:

    EWall vs CANDg-n at n in {20,30,40,60} on both large-cap lists, with the ranking
    REVERSED as a sign check; if it holds, recommend dropping ranking from the candidate
    book entirely (which is what `B136/EWall` (idea 10) and `ew-band3` (idea 57) already are).

The confound the queue's design does not close (stated BEFORE any number was read)
---------------------------------------------------------------------------------
`EWall` holds EVERY eligible name; `CANDg-n` holds n of them at matched gross.  Their
difference is therefore TWO things at once:

    (i) CONCENTRATION  -- holding n names instead of ~35 (U56) / ~86 (B136), and
    (ii) RANKING       -- WHICH n, chosen by the composite key.

"EWall > CANDg-n" is consistent with a ranking that is worthless (or harmful) AND with a
ranking that is fine while concentration is expensive.  Idea 73's number cannot tell them
apart, and neither can the queue's wording.  So this run adds the one arm that separates
them - a RANDOM pick of n eligible names at the same gross and the same persistence:

    FWD    top-n by the composite key           (the incumbent construction)
    REV    BOTTOM-n by the composite key        (the queue's sign check)
    RAND   n eligible names by a per-name uniform score drawn ONCE per seed and held
           constant through time, so the arm's persistence - and hence its turnover -
           is generated the same way FWD's and REV's are, not by weekly re-drawing
           (a weekly re-draw would hand RAND a ~52x/yr turnover bill and answer a
           cost question instead of a ranking question).  8 seeds, EVERY seed reported.
    EWall  every eligible name, equal weight    (the no-ranking book under test)

That gives the three comparisons the recommendation actually needs:

    EWall - FWD  : the queue's statistic (concentration + ranking)
    FWD   - RAND : what the RANKING adds, at matched n and matched gross (the isolate)
    FWD   - REV  : whether the key carries signed information at all (the sign check)

Pre-registered decision rule (written before any result was read)
-----------------------------------------------------------------
    Idea 82's recommendation ("drop ranking from the candidate book") is UPHELD only if
      (a) EWall >= FWD on Sharpe in a majority of unsaturated cells, AND
      (b) FWD - RAND is NOT reliably positive (i.e. the composite adds nothing over a
          random pick of the same size), AND
      (c) rule 8 agrees: the EWALL selector is not beaten OOS by the FWD selectors.
    If (a) holds but (b) fails - FWD beats RAND - then the EWall gap is CONCENTRATION,
    idea 73's headline is real but MISNAMED, and the correct recommendation is about
    breadth, not about ranking.  That outcome is a KILL of the queue's inference, not of
    its measurement, and it will be reported as such.
    If FWD < REV reliably, the key is actively perverse and that is a separate finding.

Design
------
Panels (the two large-cap lists the queue names, plus one stocks-only cut as a reported
extra):  U56 (research/universe.json), B136 (research/universe_broad.json),
         BSTK100 (B136 minus the 36 ETFs).
Gate, cadence, cost, execution and the ranking key are idea 73/240's, imported verbatim:
weekly, next-day execution, 10 bps, gate = above-200d AND vol20 < 0.60, key = the
composite WITHOUT the vol scaler.

GROSS IS MATCHED EVERYWHERE.  Every arm, including EWall, invests GROSS=0.75 whenever
anything is eligible (idea 73's `CANDg` / idea 240's NORM convention).  Idea 73's literal
`GROSS/n` FIXED convention is a gross ladder in disguise (idea 240/244) and is NOT used
for any comparison here; it is run at n=20 on U56 only, as the reproduction gate.
Realised mean gross is reported for every cell to show the channel is closed.

SATURATION.  When a panel supplies fewer than n eligible names the CANDg book IS EWall.
`sat_share` (share of rebalance dates with n_elig <= n) is reported for every cell and
cells with sat_share > 0.25 are excluded from the headline counts, because a comparison
between a book and itself is not evidence about ranking.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (4)
The arm (EWall/FWD/REV/RAND) is the hypothesis axis, pre-registered above, not a tuned
dial; the seed is averaged over and every draw is reported.
Grid = 3 panels x 4 n x (FWD + REV + 8 RAND seeds) = 120 points, + 3 EWall + 3 v1
references + 1 reproduction row = 127, ALL written to `.grid.csv`.

Walk-forward (PROTOCOL rule 8) - selectors fixed, with direction, before any OOS read
    EWALL        EWall, no ranking, no n                       (the recommendation)
    FWD20        FWD n=20                                      (incumbent construction)
    FWD_ISARGMAX n = argmax IS Sharpe within the FWD arm        (the n dial, read IS)
    ALL_ISARGMAX (arm, n) = argmax IS Sharpe over all 12 arms   (the full dial reading)
    RAND20       mean over the 8 RAND seeds at n=20             (a coin flip on the pick)
    IS = 2009-01-01..2016-12-31 (parameters chosen here only), OOS = 2017-01-01..end,
    read once.  Reported per panel and pooled, against RULES v1 OOS and SPY OOS.

Verdicts (both KEEP paths, on every point)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe_broad.json and the megacap list are CURRENT constituents, so
B136/BSTK100 are one-directional.  This bites the present question in a specific,
statable direction: on a list of known survivors, holding EVERYTHING (EWall) inherits the
full survivorship premium, while any selection rule can only redistribute it.  A result
that says "do not select" is therefore the result this bias manufactures, and any KEEP
resting on it must be discounted.  Restated in the memo.

A DIAGNOSTIC (not an arm, not selected on) reports 5 disjoint 20-name rank BANDS of the
key per panel, because FWD > REV together with FWD < RAND can only hold if the key is
non-monotone in future Sharpe, and that is the claim the bands test directly.

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

COST_BPS = 10
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
pd.set_option("display.max_rows", 400)


# ------------------------------------------------------------------ panels (idea 73/240, verbatim)
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


def weights(px, tradable, arm, n=None, seed=None):
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
        if arm == "RAND":
            rng = np.random.default_rng(1000 + seed)
            key = pd.DataFrame(np.tile(rng.random(px.shape[1]), (len(px.index), 1)),
                               index=px.index, columns=px.columns)
            asc = False
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

    print("=" * 200)
    print(f"Idea 82 ranking-subtracts-value (lane B) | {SCRIPT} | {COST_BPS} bps, weekly, next-day execution, gross matched at {GROSS}")
    print("=" * 200)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    mask56 = rebalance_mask(px56.index, FREQ)
    print("\nPanels:")
    necl = {}
    for k, (p, tr) in panels.items():
        e = eligible_mask(p, tr)
        m = rebalance_mask(p.index, FREQ)
        necl[k] = e[m.values].sum(axis=1)
        print(f"  {k:<8} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  {p.index[0].date()} -> {p.index[-1].date()}"
              f"   mean eligible {necl[k].mean():.1f}  (p10 {necl[k].quantile(.10):.0f} / p90 {necl[k].quantile(.90):.0f})")

    # ---- run every book -------------------------------------------------
    jobs = [("EWall", None, None), ("v1", None, None)]
    jobs += [(a, n, None) for a in ("FWD", "REV") for n in NS]
    jobs += [("RAND", n, s) for n in NS for s in SEEDS]

    res, turn, gross_r, held_r = {}, {}, {}, {}
    for pk, (p, tr) in panels.items():
        for arm, n, seed in jobs:
            w = weights(p, tr, arm, n, seed)
            r = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            key = (pk, arm, n, seed)
            res[key] = r["returns"]
            turn[key] = r["turnover"]
            hw = r["weights"]
            gross_r[key] = hw.sum(axis=1)
            held_r[key] = (hw > 1e-12).sum(axis=1)
        print(f"  ran {pk}  ({len(jobs)} books)")

    # ---- reproduction gate ----------------------------------------------
    start56 = px56.index[260]
    w_fix = weights(px56, panels["U56"][1], "FIXED20")
    r_fix = backtest(px56, w_fix, cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start56:]
    r_v1 = res[("U56", "v1", None, None)].loc[start56:]
    print("\n--- reproduction gate (universe.json window, must match published rows) ---")
    for nm, r, want in [("U56/CAND20 FIXED", r_fix, "idea 2/73 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                        ("U56/RULES v1   ", r_v1, "live v1: 6.5% / 0.666 / -13.8%")]:
        m = metrics(r); h1, h2 = half_sharpes(r)
        print(f"  {nm}  {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    # ---- common window --------------------------------------------------
    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    spy_full = px56["SPY"].pct_change().fillna(0)
    spy = spy_full.loc[start:end]
    spy_oos = spy_full.loc[OOS_START:end]
    print(f"\nCommon evaluation window: {start.date()} -> {end.date()}   "
          f"IS {IS_START}..{IS_END}, OOS {OOS_START}..{end.date()}")
    ms = metrics(spy); print(f"  SPY full {ms['CAGR']:.1%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.1%}  "
                             f"halves {half_sharpes(spy)[0]:.3f}/{half_sharpes(spy)[1]:.3f}  "
                             f"OOS {metrics(spy_oos)['CAGR']:.1%} / {metrics(spy_oos)['Sharpe']:.3f} / {metrics(spy_oos)['MaxDD']:.1%}")

    # ---- grid -----------------------------------------------------------
    rows = []
    for (pk, arm, n, seed), rr in res.items():
        r = rr.loc[start:end]
        r_is = rr.loc[IS_START:IS_END]
        r_oos = rr.loc[OOS_START:end]
        base = res[(pk, "v1", None, None)].loc[start:end]
        m, mo = metrics(r), metrics(r_oos)
        h1, h2 = half_sharpes(r)
        ne = necl[pk]
        sat = float((ne <= n).mean()) if n else 1.0
        rows.append(dict(
            panel=pk, arm=arm, n=(n if n else 0), seed=(-1 if seed is None else seed),
            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
            IS_Sharpe=metrics(r_is)["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
            turnover=turn[(pk, arm, n, seed)].loc[start:end].sum() / m["Years"],
            gross=gross_r[(pk, arm, n, seed)].loc[start:end].mean(),
            held=held_r[(pk, arm, n, seed)].loc[start:end].mean(),
            sat_share=sat,
            f4a=v4a(r, base), f4b=fail4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows)
    grid["k4b"] = grid["f4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\nGrid: {len(grid)} points -> {STEM}.grid.csv  (4a {grid.f4a.sum()}/{len(grid)}, 4b {grid.k4b.sum()}/{len(grid)})")

    show = grid[grid.arm != "RAND"].sort_values(["panel", "arm", "n"])
    print("\n--- every non-RAND point (full sample, common window) ---")
    print(fmt(show[["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                    "turnover", "gross", "held", "sat_share", "f4a", "f4b"]].set_index(["panel", "arm", "n"])))

    rag = (grid[grid.arm == "RAND"].groupby(["panel", "n"])
           .agg(Sharpe=("Sharpe", "mean"), Sharpe_sd=("Sharpe", "std"), Sharpe_min=("Sharpe", "min"),
                Sharpe_max=("Sharpe", "max"), CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                OOS_Sharpe=("OOS_Sharpe", "mean"), turnover=("turnover", "mean"),
                gross=("gross", "mean"), held=("held", "mean"), k4b=("k4b", "sum")))
    print("\n--- RAND arm, 8 seeds each (mean / sd / min / max) ---")
    print(fmt(rag))

    # ---- the three comparisons ------------------------------------------
    def S(pk, arm, n, seed=None):
        row = grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == (n or 0)) & (grid.seed == (-1 if seed is None else seed))]
        return float(row.Sharpe.iloc[0])

    comp = []
    for pk in panels:
        ew = S(pk, "EWall", None)
        for n in NS:
            fwd, rev = S(pk, "FWD", n), S(pk, "REV", n)
            rmean = float(rag.loc[(pk, n), "Sharpe"])
            sat = float((necl[pk] <= n).mean())
            comp.append(dict(panel=pk, n=n, sat_share=sat, unsat=(sat <= SAT_CAP),
                             EWall=ew, FWD=fwd, REV=rev, RAND=rmean,
                             d_EW_FWD=ew - fwd, d_FWD_RAND=fwd - rmean, d_FWD_REV=fwd - rev,
                             d_EW_RAND=ew - rmean))
    comp = pd.DataFrame(comp)
    comp.to_csv(OUT / f"{STEM}.comparisons.csv", index=False)
    print("\n--- the three comparisons (Sharpe, full sample; gross matched) ---")
    print(fmt(comp.set_index(["panel", "n"])))

    U = comp[comp.unsat]
    print(f"\nUnsaturated cells (sat_share <= {SAT_CAP}): {len(U)} of {len(comp)}")
    print("\n--- headline counts and paired t (over unsaturated cells) ---")
    hl = []
    for col, q in [("d_EW_FWD", "EWall - FWD   (the queue's statistic: concentration + ranking)"),
                   ("d_FWD_RAND", "FWD  - RAND   (what the RANKING adds, matched n and gross)"),
                   ("d_FWD_REV", "FWD  - REV    (does the key carry signed information)"),
                   ("d_EW_RAND", "EWall- RAND   (concentration alone, ranking removed)")]:
        mean, t = paired_t(U[col])
        hl.append(dict(comparison=q, mean=mean, t=t, pos=int((U[col] > 0).sum()), n_cells=len(U),
                       min=U[col].min(), max=U[col].max()))
    hl = pd.DataFrame(hl)
    print(fmt(hl.set_index("comparison"), 4))

    # per-seed version of FWD-RAND so the RAND mean is not doing hidden work
    ps = []
    for pk in panels:
        for n in NS:
            if float((necl[pk] <= n).mean()) > SAT_CAP:
                continue
            for s in SEEDS:
                ps.append(dict(panel=pk, n=n, seed=s, d=S(pk, "FWD", n) - S(pk, "RAND", n, s)))
    ps = pd.DataFrame(ps)
    mean, t = paired_t(ps.d)
    print(f"\nFWD - RAND over all {len(ps)} (cell, seed) draws: mean {mean:+.4f}, t {t:+.2f}, "
          f"positive in {int((ps.d > 0).sum())}/{len(ps)}  (min {ps.d.min():+.4f}, max {ps.d.max():+.4f})")
    ps.to_csv(OUT / f"{STEM}.fwd_vs_rand_seeds.csv", index=False)

    # ---- diagnostic: is the key MONOTONE? --------------------------------
    # FWD > REV (the key is signed) and FWD < RAND (the top tail loses to a middle draw)
    # can only both hold if the key's relation to future Sharpe is NON-MONOTONE.  Read it
    # directly: 5 disjoint rank BANDS of 20 names each (1-20, 21-40, ... 81-100 by the
    # composite), gross-matched, on every panel.  This is the same n dial re-expressed as
    # a position, not a third tuned parameter, and no arm below is selected on.
    print("\n--- diagnostic: disjoint rank bands of 20 by the composite key (gross matched) ---")
    diag = []
    for pk, (p, tr) in panels.items():
        elig = eligible_mask(p, tr)
        key = score(p, vol_scale=False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        for j in range(1, 6):
            sel = ((rank > (j - 1) * 20) & (rank <= j * 20)).astype(float)
            held = sel.sum(axis=1).replace(0, np.nan)
            w = sel.div(held, axis=0).mul(GROSS).fillna(0.0)
            rr = backtest(p, w, cost_bps=COST_BPS, freq=FREQ)
            r = rr["returns"].loc[start:end]
            m = metrics(r); h1, h2 = half_sharpes(r)
            diag.append(dict(panel=pk, band=f"{(j-1)*20+1}-{j*20}", CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                             MaxDD=m["MaxDD"], H1=h1, H2=h2,
                             OOS_Sharpe=metrics(rr["returns"].loc[OOS_START:end])["Sharpe"],
                             turnover=rr["turnover"].loc[start:end].sum() / m["Years"],
                             held=(rr["weights"].loc[start:end] > 1e-12).sum(axis=1).mean()))
    diag = pd.DataFrame(diag)
    diag.to_csv(OUT / f"{STEM}.bands.csv", index=False)
    print(fmt(diag.set_index(["panel", "band"])))
    for pk, g in diag.groupby("panel"):
        best = g.loc[g.Sharpe.idxmax(), "band"]
        print(f"  {pk:<8} argmax band = {best}   (band1 {g.Sharpe.iloc[0]:.3f} -> band5 {g.Sharpe.iloc[-1]:.3f}; "
              f"interior best: {'YES' if best not in ('1-20', '81-100') else 'no'})")

    # ---- the same three comparisons on CAGR and on risk ------------------
    # If the key is monotone (bands, above) but FWD still loses to RAND on SHARPE, the
    # ranking must be buying return with risk.  Read the same cells on CAGR and MaxDD.
    print("\n--- the three comparisons re-read on CAGR and MaxDD (unsaturated cells) ---")
    def G(pk, arm, n, col, seed=None):
        row = grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == (n or 0)) &
                   (grid.seed == (-1 if seed is None else seed))]
        return float(row[col].iloc[0])

    rr_rows = []
    for _, c in comp[comp.unsat].iterrows():
        pk, n = c.panel, int(c.n)
        rmean_c = float(rag.loc[(pk, n), "CAGR"]); rmean_d = float(rag.loc[(pk, n), "MaxDD"])
        rr_rows.append(dict(panel=pk, n=n,
                            CAGR_EWall=G(pk, "EWall", None, "CAGR"), CAGR_FWD=G(pk, "FWD", n, "CAGR"),
                            CAGR_RAND=rmean_c, CAGR_REV=G(pk, "REV", n, "CAGR"),
                            dC_FWD_EW=G(pk, "FWD", n, "CAGR") - G(pk, "EWall", None, "CAGR"),
                            dC_FWD_RAND=G(pk, "FWD", n, "CAGR") - rmean_c,
                            dDD_FWD_EW=abs(G(pk, "FWD", n, "MaxDD")) - abs(G(pk, "EWall", None, "MaxDD")),
                            dDD_FWD_RAND=abs(G(pk, "FWD", n, "MaxDD")) - abs(rmean_d)))
    rr_df = pd.DataFrame(rr_rows)
    rr_df.to_csv(OUT / f"{STEM}.cagr.csv", index=False)
    print(fmt(rr_df.set_index(["panel", "n"]), 4))
    for col, q in [("dC_FWD_EW", "CAGR: FWD - EWall"), ("dC_FWD_RAND", "CAGR: FWD - RAND"),
                   ("dDD_FWD_EW", "|MaxDD|: FWD - EWall"), ("dDD_FWD_RAND", "|MaxDD|: FWD - RAND")]:
        m_, t_ = paired_t(rr_df[col])
        print(f"  {q:<22} mean {m_:+.4f}, t {t_:+.2f}, positive in {int((rr_df[col] > 0).sum())}/{len(rr_df)}")

    # ---- where does the ranking cost land: halves ------------------------
    print("\n--- EWall - FWD by half (unsaturated cells) ---")
    hv = []
    for _, c in comp[comp.unsat].iterrows():
        pk, n = c.panel, int(c.n)
        e = grid[(grid.panel == pk) & (grid.arm == "EWall")].iloc[0]
        f = grid[(grid.panel == pk) & (grid.arm == "FWD") & (grid.n == n)].iloc[0]
        hv.append(dict(panel=pk, n=n, dH1=e.H1 - f.H1, dH2=e.H2 - f.H2, dOOS=e.OOS_Sharpe - f.OOS_Sharpe))
    hv = pd.DataFrame(hv)
    print(fmt(hv.set_index(["panel", "n"]), 4))
    for col in ("dH1", "dH2", "dOOS"):
        m_, t_ = paired_t(hv[col])
        print(f"  {col}: mean {m_:+.4f}, t {t_:+.2f}, positive in {int((hv[col] > 0).sum())}/{len(hv)}")

    # ---- rule 8 walk-forward -------------------------------------------
    print("\n" + "=" * 200)
    print("RULE 8 WALK-FORWARD  (parameters chosen on IS 2009-2016 only; OOS 2017-2026 read once)")
    print("=" * 200)

    def isS(pk, arm, n, seed=None):
        return float(grid[(grid.panel == pk) & (grid.arm == arm) & (grid.n == (n or 0)) &
                          (grid.seed == (-1 if seed is None else seed))].IS_Sharpe.iloc[0])

    wf = []
    for pk in panels:
        ns_ok = [n for n in NS if float((necl[pk] <= n).mean()) <= SAT_CAP] or NS
        picks = {
            "EWALL": ("EWall", None, None),
            "FWD20": ("FWD", 20, None),
            "FWD_ISARGMAX": ("FWD", max(ns_ok, key=lambda n: isS(pk, "FWD", n)), None),
        }
        cands = [("FWD", n, None) for n in ns_ok] + [("REV", n, None) for n in ns_ok] + \
                [("RAND", n, s) for n in ns_ok for s in SEEDS] + [("EWall", None, None)]
        picks["ALL_ISARGMAX"] = max(cands, key=lambda c: isS(pk, c[0], c[1], c[2]))
        for nm, (arm, n, seed) in picks.items():
            r = res[(pk, arm, n, seed)].loc[OOS_START:end]
            m = metrics(r)
            wf.append(dict(panel=pk, selector=nm, pick=f"{arm}{n if n else ''}", OOS_CAGR=m["CAGR"],
                           OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
        rs = [metrics(res[(pk, "RAND", 20, s)].loc[OOS_START:end]) for s in SEEDS]
        wf.append(dict(panel=pk, selector="RAND20", pick="RAND20 (8 seeds)",
                       OOS_CAGR=float(np.mean([x["CAGR"] for x in rs])),
                       OOS_Sharpe=float(np.mean([x["Sharpe"] for x in rs])),
                       OOS_MaxDD=float(np.mean([x["MaxDD"] for x in rs]))))
        b = metrics(res[(pk, "v1", None, None)].loc[OOS_START:end])
        wf.append(dict(panel=pk, selector="RULES v1", pick="baseline",
                       OOS_CAGR=b["CAGR"], OOS_Sharpe=b["Sharpe"], OOS_MaxDD=b["MaxDD"]))
    mo = metrics(spy_oos)
    for pk in panels:
        wf.append(dict(panel=pk, selector="SPY", pick="benchmark", OOS_CAGR=mo["CAGR"],
                       OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(wf.set_index(["panel", "selector"])))

    pool = wf.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
    print("\n--- pooled over the 3 panels (equal weight) ---")
    print(fmt(pool.sort_values("OOS_Sharpe", ascending=False)))

    ewall_oos = wf[wf.selector == "EWALL"].set_index("panel").OOS_Sharpe
    for sel in ("FWD20", "FWD_ISARGMAX", "ALL_ISARGMAX", "RAND20"):
        o = wf[wf.selector == sel].set_index("panel").OOS_Sharpe
        d = (ewall_oos - o).dropna()
        print(f"  EWALL - {sel:<13} OOS Sharpe: mean {d.mean():+.4f}, wins {int((d > 0).sum())}/{len(d)}  "
              f"({', '.join(f'{k} {v:+.3f}' for k, v in d.items())})")

    # ---- KEEP-path summary ---------------------------------------------
    print("\n--- KEEP paths, unsaturated cells + EWall (4b failing-bar detail) ---")
    kp = grid[(grid.arm.isin(["EWall", "FWD", "REV"])) &
              ((grid.arm == "EWall") | (grid.sat_share <= SAT_CAP))]
    print(fmt(kp.sort_values(["panel", "arm", "n"])[["panel", "arm", "n", "CAGR", "Sharpe", "MaxDD",
                                                     "H1", "H2", "OOS_Sharpe", "f4a", "f4b"]]
              .set_index(["panel", "arm", "n"])))
    print(f"\n4b passes: {int(grid.k4b.sum())} of {len(grid)} points "
          f"({', '.join(f'{a} {int(g.k4b.sum())}/{len(g)}' for a, g in grid.groupby('arm'))})")

    print("\nWrote:", ", ".join(f"{STEM}.{x}.csv" for x in ("grid", "comparisons", "fwd_vs_rand_seeds", "walkforward")))


if __name__ == "__main__":
    main()
