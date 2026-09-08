#!/usr/bin/env python3
"""Idea 232 - "does-the-vol-gate-corner-survive-being-pre-registered" (lane B, 2026-09-08).

The question
------------
Idea 228 ran a rule-8 walk-forward over four dials and found a POSITIVE selector premium
(+0.0177 mean OOS Sharpe over do-nothing, 59.5% wins).  All of it came from one dial: the
vol-cap V (+0.1049 mean, 85.7% wins, +0.213..+0.376 on SMALL484); excluding V the premium
is -0.0113 over 63 cells.  What the chooser "discovered" was one corner of one ladder -
switch the vol20 gate OFF - i.e. ideas 38/49's standing result, re-found by a selector.

A corner an IS chooser reaches for is exactly the shape that a selector-artefact takes
(idea 173: three of the project's dials are monotone, so the argmax is a statement about
where the grid was stopped).  So the corner has to be priced WITHOUT a selector.  This run
pre-registers the two arms and reads both:

    GATE_ON   eligible = (px > 200d MA) AND (vol20 < 0.60)     the live/default screen
    GATE_OFF  eligible = (px > 200d MA)                        no vol gate at all

The 200d gate is held FIXED at g = 0.00 in both arms (the queue's condition), so the only
thing that changes between the two books is the vol20 < 0.60 clause.  Neither arm is
chosen: both are reported at every panel, every count and every rung.

Construction (idea 228's standing shape, verbatim)
--------------------------------------------------
    rank    = RULES v1 composite (12-1 / 6m / 3m rank average), NO vol scaler
    eligible= 200d trend gate (g = 0.00), optionally AND vol20 < 0.60
    hold    = top n eligible, 1/n each, weekly (freq = "W"), t+1 execution
    default = n = 20 (idea 228's do-nothing point of the N dial) - the headline row

Tuned parameters (PROTOCOL rule 4: at most two)
    1. n in {5, 10, 20, 30, 40}      position count
    2. c in {0, 5, 10, 15, 20, 25, 30} bps   idea 82's cost ladder
The GATE ARM and the PANEL are the treatment axes of the idea itself, not dials: both are
pre-registered and both are reported at every grid point, neither is selected.

GROSS and the RANKING KEY are not dials here either.  Each is pinned at the TWO published
levels this same corner has already been quoted at in the record, both reported in full,
neither chosen.  The record turns out to carry the corner in two different books:

    gross  g = 1.00   idea 228's own book, the shape the +0.1049 premium was measured on;
           g = 0.75   the record's standing gross, and idea 256's level.
    key    COMP       the composite WITHOUT the vol scaler - idea 228's ranking;
           V1KEY      score(vol_scale=True), the LIVE RULES v1 key - idea 256's ranking.

That second axis is forced, not chosen: idea 228's "u56 n=20 max_vol=off" and idea 256's
"u56 n=20 max_vol=off g=0.75" are quoted as the same cell and are NOT the same book (10 bps:
Sharpe 1.147 vs 0.993, turnover 12.22 vs 11.59/yr) because idea 256 ranks with the vol
scaler and idea 228 does not.  Both are reproduced in pre-check [b] and both are carried.
The distinction is on-question: a vol GATE and a 1/sqrt(vol) RANK TILT are two ways to spend
the same information, so a corner that only pays on the un-tilted key is not a vol result.

Grid = 3 panels x 2 keys x 2 gross x 2 arms x 5 n x 7 rungs = 840 points, all in .grid.csv.
The cost ladder is exact, not re-simulated: net(c) = gross - turnover*c/1e4 is an identity
of the engine (pre-check [c]).

Pre-checks run BEFORE any new number is read
    [a] harness: the live RULES v1 row on U56 and idea 2's U56/CAND20 row.
    [b] premise, TWO reproductions of committed CSVs:
        - idea 228's own .grid.csv, the whole V dial: 3 panels x 8 vol thresholds x 7 rungs
          = 168 rows on CAGR/Sharpe/MaxDD/H1/H2/OOS.  Its V=0.60 and V=5.00 columns ARE
          this run's GATE_ON and GATE_OFF arms at n=20, g=1.00, so this is the premise
          itself, not a proxy;
        - idea 256's committed 4b row at g=0.75, which needs ITS key (V1KEY) to reproduce.
        If either fails to reproduce the run has no premise and aborts.  Idea 228 hand-rolled
        its own rebalance loop; this run uses engine.backtest, so the [b1] tolerance is 1e-3
        of Sharpe and the residual is published cell by cell (worst U56 V=0.3: 1.4e-4).
    [c] the cost identity.
    [d] non-degeneracy: the vol gate must actually bind - report the share of trend-eligible
        names it removes and the share of REBALANCE WEEKS in which the two arms' top-n sets
        differ.  If the gate never binds the comparison is empty.

Walk-forward (PROTOCOL rule 8) - every selector fixed before any OOS number was read
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.
    A0  GATE_ON  at the pre-registered n = 20               (the do-nothing / live screen)
    A1  GATE_OFF at the pre-registered n = 20               (THE PRE-REGISTERED CORNER)
    S1  IS-argmax over (arm, n) at each rung                (idea 228's chooser, rebuilt)
    S2  IS-argmax over n only, arm pinned to GATE_ON        (a chooser denied the corner)
    S3  random (arm, n), seed fixed in advance              (the size-matched null)
    Run independently inside every (key, gross, panel, rung) cell; nothing pools across keys.
    If A1 - A0 out of sample is of the same size as idea 228's +0.1049 chooser premium,
    the corner is real and needed no selector.  If A1 - A0 is ~0 or negative while S1 - A0
    is positive, the premium was the SELECTION, not the corner.

Significance of the headline difference
    Stationary block bootstrap (mean block 21 trading days, 2,000 draws, seed 232001) on
    the PAIRED daily net-return difference GATE_OFF - GATE_ON at n = 20, 10 bps, per
    (key, gross, panel):
    reports the Sharpe-difference CI and P(diff <= 0).  A corner worth a rules change has
    to clear its own noise band, not just have a positive sign.

Verdicts (both KEEP paths, all 840 points)
    4a  Sharpe > RULES v2 (the LIVE book since 2026-09-06) in BOTH halves AND MaxDD no
        worse than RULES v2.  The RULES v1 verdict is carried alongside for continuity.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: universe.json, universe_broad.json and the small panel are CURRENT
constituents, one-directional; every arm inherits that in full and nothing here corrects
it.  A vol gate is exactly the clause a survivorship-biased panel flatters (the names that
blew up on high vol are not in the list), so GATE_OFF's edge here is an UPPER bound.

Deterministic, standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import sys, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask                          # noqa: E402

FREQ = "W"
GROSSES = [1.00, 0.75]           # idea 228's book and idea 256's; both PUBLISHED, neither chosen
GROSS_HEAD = 1.00                # the level the premise (+0.1049) was measured on
MAX_VOL = 0.60
NS = [5, 10, 20, 30, 40]
N_HEAD = 20                      # idea 228's do-nothing count; the headline row
RUNGS = [0, 5, 10, 15, 20, 25, 30]
COST_MAIN = 10
WARMUP = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOT_DRAWS = 2000
BOOT_BLOCK = 21
SEED_BOOT = 232_001
SEED_S3 = 232_999
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 800)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)

def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")

def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def stats(r):
    m = metrics(r)
    h1, h2 = half_sharpes(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)

def fail_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"

def fail_4b(s, oos_sharpe, spy, spy_oos):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_sharpe > spy_oos: f.append("OOS")
    if not abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]): f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"

def net(r0, tno, c):
    return r0 - tno * c / 1e4


# ---------------------------------------------------------------- panels (idea 228's)
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    def sub(px, tradable):
        p = px.dropna(how="all").ffill()
        return p, set(tradable)

    s_stk = [c for c in pxs.columns if c != "SPY"]
    return {
        "U56":      sub(px56, [c for c in px56.columns]),
        "B136":     sub(px136, [c for c in px136.columns]),
        "SMALL484": sub(pxs, s_stk),
    }


def ingredients(px, tradable):
    """Idea 228's exact recovery of the composite without the vol scaler, the LIVE RULES v1
    vol-scaled key (idea 256's), and the two eligibility masks.  Higher key = preferred."""
    s_ns, above, vol20 = score(px, vol_scale=False)
    comp = s_ns / (0.5 + 0.5 * above.astype(float))      # exact: undo the soft 200d tilt
    s_v1, _, _ = score(px, vol_scale=True)               # the live key: comp * tilt / sqrt(vol20)
    trend = above.copy()                                  # g = 0.00, held fixed in both arms
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        trend[drop] = False
    elig_on = trend & (vol20 < MAX_VOL)
    elig_off = trend.copy()
    return comp, elig_on, elig_off, vol20, s_v1


def topn_weights(comp, elig, n, gross=GROSS_HEAD):
    """Top-n equal weight over the eligible set (idea 228's book_weights at gross=1.00)."""
    e = comp.where(elig)
    rank = e.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def run_book(px, w, start):
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def block_boot_sharpe_diff(d, draws, block, seed):
    """Stationary block bootstrap on a PAIRED daily difference series.  Returns
    (mean, lo, hi, P(diff<=0)) for the annualised Sharpe of the difference stream."""
    x = np.asarray(d.dropna(), dtype=float)
    nobs = len(x)
    rng = np.random.default_rng(seed)
    nblk = int(np.ceil(nobs / block))
    out = np.empty(draws)
    for i in range(draws):
        starts = rng.integers(0, nobs, size=nblk)
        idx = (starts[:, None] + np.arange(block)[None, :]).ravel()[:nobs] % nobs
        s = x[idx]
        sd = s.std(ddof=1)
        out[i] = (s.mean() * 252) / (sd * np.sqrt(252)) if sd > 0 else np.nan
    out = out[~np.isnan(out)]
    obs_sd = x.std(ddof=1)
    obs = (x.mean() * 252) / (obs_sd * np.sqrt(252)) if obs_sd > 0 else np.nan
    return obs, float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)), float((out <= 0).mean())


def main():
    t0 = time.time()
    P("=" * 200)
    P(f"Idea 232 does-the-vol-gate-corner-survive-being-pre-registered (lane B) | {SCRIPT}")
    P(f"weekly, t+1 execution, gross {GROSSES} (both published levels), 200d gate held FIXED at g=0.00, "
      f"only the vol20<{MAX_VOL} clause moves")
    P("=" * 200)

    panels = build_panels()
    px56, tr56 = panels["U56"]

    yrs = px56.index.to_series().groupby(px56.index.year).count()
    P(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    start56 = px56.index[WARMUP]
    comp56, on56, off56, vol56, v1key56 = ingredients(px56, tr56)

    # ------------------------------------------------ pre-check [a] harness
    P("\n--- pre-check [a] harness on universe.json's own window (must match published rows) ---")
    for lbl, w, want in [("U56/v1", rules_v1_weights(px56), "live v1: 6.5% / 0.666 / -13.8% h 0.64/0.69"),
                         ("U56/CAND20", topn_weights(comp56, on56, 20) * 0.75,
                          "idea 2 KEEP shape (0.75 gross): 12.7% / 1.093 / -18.3%")]:
        r = backtest(px56, w, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        P(f"  {lbl:<11} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    # ------------------------------------------------ pre-check [b] the premise, exactly
    P("\n--- pre-check [b1] EXACT reproduction of idea 228's committed .grid.csv, the whole V dial ---")
    p228 = REPO / "research" / "backtests" / "2026-09-06_does-any-dial-argmax-move-with-cost_C.grid.csv"
    g228 = pd.read_csv(p228)
    g228 = g228[g228.dial == "V"].copy()
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turn_yr"]
    # idea 228's construction VERBATIM: it ranks every column of the panel, which on
    # SMALL484 lets SPY itself into the book.  Reproduced here as published; the idea-232
    # arms below exclude the benchmark from the tradable set (see pre-check [d2]).
    rep = []
    for pk, (px, tr) in panels.items():
        s_ns, above_raw, v20 = score(px, vol_scale=False)
        comp_raw = s_ns / (0.5 + 0.5 * above_raw.astype(float))
        start = px.index[WARMUP]
        yrs_n = len(px.loc[start:]) / 252
        for v in sorted(g228[g228.panel == pk].value.unique()):
            r0, tno = run_book(px, topn_weights(comp_raw, above_raw & (v20 < v), N_HEAD, 1.00), start)
            for c in RUNGS:
                r = net(r0, tno, c); s = stats(r); o = metrics(r.loc[OOS_START:])
                rep.append(dict(panel=pk, value=v, bps=c, turn_yr=float(tno.sum() / yrs_n),
                                OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"], **s))
    rep = pd.DataFrame(rep)
    mg = g228.merge(rep, on=["panel", "value", "bps"], suffixes=("_pub", "_new"))
    if len(mg) != len(g228):
        P(f"!! only {len(mg)} of {len(g228)} published V-dial rows matched on keys - aborting."); sys.exit(1)
    worst = {c: float((mg[f"{c}_pub"] - mg[f"{c}_new"]).abs().max()) for c in cols}
    P(f"  {len(mg)} rows (3 panels x 8 vol thresholds x 7 rungs); max |published - reproduced| per column:")
    P("   ", {k: f"{v:.2e}" for k, v in worst.items()})
    mg["_dS"] = (mg.Sharpe_pub - mg.Sharpe_new).abs()
    P(f"  by panel, max |dSharpe|: " + ", ".join(f"{p} {v:.2e}" for p, v in mg.groupby('panel')._dS.max().items()))
    wc = mg.loc[mg._dS.idxmax()]
    P(f"  worst cell {wc.panel} V={wc.value} @{int(wc.bps)} bps: published {wc.Sharpe_pub:.6f} vs {wc.Sharpe_new:.6f} "
      f"(turnover {wc.turn_yr_pub:.4f} vs {wc.turn_yr_new:.4f}) - idea 228 hand-rolled its own rebalance loop, this run")
    P(f"  uses engine.backtest; the two differ only in first-bar handling.  Tolerance for the premise: 1e-3 on Sharpe.")
    if max(worst[c] for c in cols if c != "turn_yr") > 1e-3 or worst["turn_yr"] > 2e-2:
        P("!! idea 228's committed V dial does not reproduce - aborting (idea 232 has no premise)."); sys.exit(1)
    v_on = mg[(mg.panel == "U56") & (mg.value == 0.6) & (mg.bps == COST_MAIN)].iloc[0]
    v_off = mg[(mg.panel == "U56") & (mg.value == 5.0) & (mg.bps == COST_MAIN)].iloc[0]
    P(f"  the two arms ARE two of those rows: U56 @10 bps V=0.60 Sharpe {v_on.Sharpe_pub:.4f} vs "
      f"V=5.00 {v_off.Sharpe_pub:.4f} (d {v_off.Sharpe_pub - v_on.Sharpe_pub:+.4f})")

    P("\n--- pre-check [b2] idea 256's committed 4b row: U56 n=20 max_vol=OFF g=0.75 @10 bps -> 10.7157% / 0.9934 / -19.4934% h 1.0393/0.9655 OOS 1.0334 ---")
    P("  The record quotes this and idea 228's V=5.00 point as the SAME corner.  They are three")
    P("  construction changes apart, so both are rebuilt here and the gap is priced, not assumed:")
    P("    (1) ranking key  - idea 256 ranks with score(vol_scale=True), idea 228 without the scaler;")
    P("    (2) gross channel- idea 256 NORMALISES (gross spread over the names actually held),")
    P("                       idea 228 uses the RAW gross/n and holds the shortfall as cash;")
    P("    (3) gross level  - 0.75 vs 1.00.")
    s_v1, _, _ = score(px56, vol_scale=True)

    def w256(key, elig, n, gross):
        """idea 256's book_weights: constant-gross NORM channel."""
        sel = ((key.where(elig).rank(axis=1, ascending=False)) <= n).astype(float)
        cnt = sel.sum(axis=1).replace(0.0, np.nan)
        return (sel.div(cnt, axis=0) * gross).fillna(0.0)

    off99 = off56 & (vol56 < 99.0)      # idea 256 spells "off" as max_vol=99, not as no clause
    raw_w = lambda k, e, n, g: topn_weights(k, e, n, g)
    b2 = []
    for lbl, key, wf_, el in [("idea 256 verbatim  (V1KEY, NORM, g=0.75)", s_v1, w256, off99),
                              ("            same but RAW gross/n        ", s_v1, raw_w, off99),
                              ("            same but COMP key, NORM     ", comp56, w256, off99),
                              ("idea 228 shape     (COMP, RAW, g=0.75)  ", comp56, raw_w, off99),
                              ("this run's GATE_OFF (COMP, RAW, no clause)", comp56, raw_w, off56)]:
        r_off, t_off = run_book(px56, wf_(key, el, N_HEAD, 0.75), start56)
        rn2 = net(r_off, t_off, COST_MAIN)
        m = metrics(rn2); h1, h2 = half_sharpes(rn2); o = metrics(rn2.loc[OOS_START:])
        P(f"    {lbl}  {m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%}  halves {h1:.4f}/{h2:.4f}  "
          f"OOS {o['Sharpe']:.4f}  turn {t_off.sum()/(len(rn2)/252):.4f}/yr")
        b2.append((lbl, m["Sharpe"], o["Sharpe"]))
    res = dict(Sharpe=abs(b2[0][1] - 0.993389), OOS_Sharpe=abs(b2[0][2] - 1.033379))
    P(f"  residual vs idea 256's committed row: |dSharpe| {res['Sharpe']:.2e}, |dOOS| {res['OOS_Sharpe']:.2e}; "
      f"MaxDD and H1 agree to 4 dp.  Same engine-vs-hand-rolled-loop first-bar residual as [b1];")
    P(f"  tolerance 5e-3, which is 20x smaller than the smallest of the three construction gaps below "
      f"({min(abs(b2[0][1]-b2[i][1]) for i in (1, 2, 3)):.4f}).")
    if max(res.values()) > 5e-3:
        P("!! idea 256's committed point does not reproduce under its own construction - aborting."); sys.exit(1)
    P(f"  idea 256's row reproduces on its own construction (Sharpe {b2[0][1]:.4f} vs published 0.9934, "
      f"OOS {b2[0][2]:.4f} vs 1.0334).")
    P(f"  What the record calls one corner is worth Sharpe {b2[0][1]:.4f} (idea 256's book) or "
      f"{b2[3][1]:.4f} (idea 228's) - a {b2[3][1]-b2[0][1]:+.4f} spread from construction alone,")
    P(f"  which is {abs(b2[3][1]-b2[0][1])/0.1049:.1f}x idea 228's whole +0.1049 chooser premium.")
    P("  The grid below carries idea 228's RAW gross channel (the premise) and BOTH ranking keys at BOTH gross levels.")
    P("  The NORM channel is idea 244's, already priced there, and is NOT a further axis of this run.")

    # ------------------------------------------------ pre-check [c] cost identity + arm identity
    P("\n--- pre-check [c] cost identity  net(c) = gross - turnover*c/1e4  (must be < 1e-12) ---")
    r_id, t_id = run_book(px56, topn_weights(comp56, off56, N_HEAD, 0.75), start56)
    direct = backtest(px56, topn_weights(comp56, off56, N_HEAD, 0.75), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start56:]
    dmax = float((net(r_id, t_id, COST_MAIN) - direct).abs().max())
    P(f"  U56 GATE_OFF n=20 g=0.75 at 10 bps: max|identity - direct| = {dmax:.3e}")
    if not dmax < 1e-12:
        P("!! cost identity broken - aborting."); sys.exit(1)
    # the GATE_OFF arm (no vol clause at all) must be byte-identical to idea 228's V=5.00 arm
    r_a, _ = run_book(px56, topn_weights(comp56, off56, N_HEAD, 1.00), start56)
    r_b, _ = run_book(px56, topn_weights(comp56, off56 & (vol56 < 5.00), N_HEAD, 1.00), start56)
    dv = float((r_a - r_b).abs().max())
    P(f"  GATE_OFF (no vol clause) vs idea 228's V=5.00 arm on U56: max|d| returns = {dv:.3e}")
    if not dv < 1e-15:
        P("!! GATE_OFF is not idea 228's V=5.00 corner - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [d] does the gate bind?
    P("\n--- pre-check [d] non-degeneracy: does the vol20 gate actually bind? ---")
    bind_rows = []
    for pk, (px, tr) in panels.items():
        comp, on, off, vol20, v1key = ingredients(px, tr)
        start = px.index[WARMUP]
        mask = rebalance_mask(px.index, FREQ)
        reb = px.index[mask.values]
        reb = reb[reb >= start]
        n_tr = off.loc[reb].sum(axis=1)
        n_on = on.loc[reb].sum(axis=1)
        cut_share = float(((n_tr - n_on) / n_tr.replace(0, np.nan)).mean())
        # do the top-20 SETS differ?
        sel_on = (comp.where(on).rank(axis=1, ascending=False) <= N_HEAD).loc[reb]
        sel_off = (comp.where(off).rank(axis=1, ascending=False) <= N_HEAD).loc[reb]
        diff_wk = float((sel_on != sel_off).any(axis=1).mean())
        n_diff = float((sel_on != sel_off).sum(axis=1).mean() / 2)
        bind_rows.append(dict(panel=pk, mean_trend_eligible=float(n_tr.mean()),
                              mean_vol_gated=float(n_on.mean()), share_cut_by_gate=cut_share,
                              weeks_top20_differs=diff_wk, mean_names_swapped=n_diff))
    bind = pd.DataFrame(bind_rows).set_index("panel")
    P(fmt(bind))
    if bind["weeks_top20_differs"].min() < 0.01:
        P("!! the gate does not bind on some panel - the comparison would be empty; aborting."); sys.exit(1)
    P("  the gate binds on all three panels")

    P("\n--- pre-check [d2] the ONE deviation from idea 228's construction, priced ---")
    P("  idea 228 ranks every column of the panel, so on SMALL484 the SPY benchmark is itself")
    P("  a holdable name.  Idea 232's arms exclude it.  Cost of the correction, n=20 g=1.00 @10 bps:")
    pxs, trs = panels["SMALL484"]
    s_ns, above_raw, v20s = score(pxs, vol_scale=False)
    comp_raw = s_ns / (0.5 + 0.5 * above_raw.astype(float))
    comp_s, on_s, off_s, _, _ = ingredients(pxs, trs)
    st = pxs.index[WARMUP]
    for lbl, cmp_, el in [("idea 228 (SPY holdable)", comp_raw, above_raw),
                          ("idea 232 (SPY excluded)", comp_s, off_s)]:
        r0, tno = run_book(pxs, topn_weights(cmp_, el, N_HEAD, 1.00), st)
        r = net(r0, tno, COST_MAIN); m = metrics(r); h1, h2 = half_sharpes(r)
        P(f"    GATE_OFF {lbl:<24} {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}  halves {h1:.4f}/{h2:.4f}")

    # ------------------------------------------------ the pre-registered grid
    P("\n" + "=" * 200)
    P(f"THE GRID - {len(panels)} panels x 2 arms x {len(NS)} n x {len(RUNGS)} rungs x {len(GROSSES)} gross = "
      f"{len(panels)*2*len(NS)*len(RUNGS)*len(GROSSES)} points, all written to {STEM}.grid.csv")
    P("=" * 200)

    rows, books, refs = [], {}, {}
    for pk, (px, tr) in panels.items():
        start = px.index[WARMUP]
        comp, on, off, vol20, v1key = ingredients(px, tr)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy); spy_oos = metrics(spy.loc[OOS_START:])
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start:]
        refs[pk] = dict(spy=spy_s, spy_oos=spy_oos, v2=stats(v2), v2_oos=metrics(v2.loc[OOS_START:]),
                        v1=stats(v1), v1_oos=metrics(v1.loc[OOS_START:]))
        yrs_n = len(spy) / 252

        for kname, key in [("COMP", comp), ("V1KEY", v1key)]:
          for g in GROSSES:
            for arm, elig in [("GATE_ON", on), ("GATE_OFF", off)]:
                for n in NS:
                    if n > len(tr):
                        continue
                    r0, tno = run_book(px, topn_weights(key, elig, n, g), start)
                    books[(pk, kname, g, arm, n)] = (r0, tno)
                    for c in RUNGS:
                        r = net(r0, tno, c)
                        s = stats(r)
                        o = metrics(r.loc[OOS_START:])
                        rows.append(dict(panel=pk, key=kname, gross=g, arm=arm, n=n, bps=c,
                                         turn_yr=float(tno.sum() / yrs_n), **s,
                                         OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                         IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                         fail4a=fail_4a(s, refs[pk]["v2"]),
                                         fail4a_v1=fail_4a(s, refs[pk]["v1"]),
                                         fail4b=fail_4b(s, o["Sharpe"], spy_s, spy_oos["Sharpe"])))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P("\n--- reference rows per panel (10 bps, full sample; OOS = 2017-2026) ---")
    ref_tbl = pd.DataFrame([dict(panel=pk, who=w, CAGR=d[w]["CAGR"], Sharpe=d[w]["Sharpe"],
                                 MaxDD=d[w]["MaxDD"], H1=d[w]["H1"], H2=d[w]["H2"],
                                 OOS_Sharpe=d[f"{w}_oos"]["Sharpe"], OOS_CAGR=d[f"{w}_oos"]["CAGR"],
                                 OOS_MaxDD=d[f"{w}_oos"]["MaxDD"])
                            for pk, d in refs.items() for w in ("spy", "v2", "v1")]).set_index(["panel", "who"])
    P(fmt(ref_tbl))

    # ------------------------------------------------ headline: the pre-registered pair
    P("\n" + "=" * 200)
    P(f"HEADLINE - the PRE-REGISTERED pair at n = {N_HEAD}, g = {GROSS_HEAD:.2f}, key = COMP (idea 228's own book):")
    P("           GATE_OFF minus GATE_ON, every panel x every rung.  Nothing is selected.")
    P("=" * 200)
    head = grid[(grid["n"] == N_HEAD) & (grid["gross"] == GROSS_HEAD) & (grid["key"] == "COMP")]
    d_rows = []
    for pk in panels:
        for c in RUNGS:
            a = head[(head.panel == pk) & (head.bps == c) & (head.arm == "GATE_OFF")].iloc[0]
            b = head[(head.panel == pk) & (head.bps == c) & (head.arm == "GATE_ON")].iloc[0]
            d_rows.append(dict(panel=pk, bps=c,
                               ON_Sharpe=b.Sharpe, OFF_Sharpe=a.Sharpe, dSharpe=a.Sharpe - b.Sharpe,
                               ON_CAGR=b.CAGR, OFF_CAGR=a.CAGR, dCAGR=a.CAGR - b.CAGR,
                               ON_MaxDD=b.MaxDD, OFF_MaxDD=a.MaxDD, dMaxDD=a.MaxDD - b.MaxDD,
                               ON_OOS=b.OOS_Sharpe, OFF_OOS=a.OOS_Sharpe, dOOS=a.OOS_Sharpe - b.OOS_Sharpe,
                               dH1=a.H1 - b.H1, dH2=a.H2 - b.H2,
                               ON_turn=b.turn_yr, OFF_turn=a.turn_yr))
    dhead = pd.DataFrame(d_rows)
    dhead.to_csv(OUT / f"{STEM}.headline.csv", index=False)
    P(fmt(dhead.set_index(["panel", "bps"])[["ON_Sharpe", "OFF_Sharpe", "dSharpe", "dH1", "dH2",
                                             "ON_OOS", "OFF_OOS", "dOOS", "dCAGR", "dMaxDD"]]))
    P(f"\n  dSharpe > 0 in {int((dhead.dSharpe > 0).sum())} of {len(dhead)} (panel x rung) cells at n={N_HEAD}; "
      f"mean {dhead.dSharpe.mean():+.4f}")
    P(f"  dOOS    > 0 in {int((dhead.dOOS > 0).sum())} of {len(dhead)}; mean {dhead.dOOS.mean():+.4f}"
      f"   [idea 228's V-dial CHOOSER premium was +0.1049]")
    P(f"  BOTH halves improved in {int(((dhead.dH1 > 0) & (dhead.dH2 > 0)).sum())} of {len(dhead)}")
    P(f"  dMaxDD (negative = the corner DEEPENS the drawdown): mean {dhead.dMaxDD.mean():+.2%}, "
      f"worse in {int((dhead.dMaxDD < 0).sum())} of {len(dhead)}")

    # full n x arm surface at the protocol rung
    IDX = ["key", "gross", "panel", "n"]
    P(f"\n--- the whole (key x gross x arm x n) surface at PROTOCOL's own {COST_MAIN} bps ---")
    at10 = grid[grid.bps == COST_MAIN].pivot_table(index=IDX, columns="arm",
                                                   values=["Sharpe", "OOS_Sharpe", "CAGR", "MaxDD"])
    P(fmt(at10))
    surf = grid[grid.bps == COST_MAIN].pivot_table(index=IDX, columns="arm", values="Sharpe")
    surf["dSharpe"] = surf["GATE_OFF"] - surf["GATE_ON"]
    P(f"\n  at 10 bps, dSharpe > 0 in {int((surf.dSharpe > 0).sum())} of {len(surf)} (key x gross x panel x n) cells; "
      f"mean {surf.dSharpe.mean():+.4f}, min {surf.dSharpe.min():+.4f}, max {surf.dSharpe.max():+.4f}")
    IDXB = IDX + ["bps"]
    allc = grid.pivot_table(index=IDXB, columns="arm", values="Sharpe")
    allc["d"] = allc["GATE_OFF"] - allc["GATE_ON"]
    allo = grid.pivot_table(index=IDXB, columns="arm", values="OOS_Sharpe")
    allo["d"] = allo["GATE_OFF"] - allo["GATE_ON"]
    alld = grid.pivot_table(index=IDXB, columns="arm", values="MaxDD")
    alld["d"] = alld["GATE_OFF"] - alld["GATE_ON"]
    P(f"  over ALL {len(allc)} (key x gross x panel x n x rung) cells:")
    P(f"    full-sample dSharpe > 0 in {int((allc.d > 0).sum())}/{len(allc)}, mean {allc.d.mean():+.4f}, sd {allc.d.std():.4f}")
    P(f"    OOS         dSharpe > 0 in {int((allo.d > 0).sum())}/{len(allo)}, mean {allo.d.mean():+.4f}, sd {allo.d.std():.4f}")
    P(f"    dMaxDD < 0 (corner deepens the drawdown) in {int((alld.d < 0).sum())}/{len(alld)}, mean {alld.d.mean():+.2%}")
    P("\n  THE CORNER BY RANKING KEY - does the gate still pay once the ranking already carries vol?")
    bk = allc.reset_index().groupby("key").d.agg(["mean", "std", "min", "max", lambda s: (s > 0).mean()])
    bk.columns = ["mean_dSharpe", "sd", "min", "max", "share>0"]
    P(fmt(bk))
    bko = allo.reset_index().groupby("key").d.agg(["mean", "std", lambda s: (s > 0).mean()])
    bko.columns = ["mean_dOOS_Sharpe", "sd", "share>0"]
    P(fmt(bko))
    P("\n  ... and by panel x key (full-sample dSharpe, 10 bps):")
    P(fmt(surf.reset_index().pivot_table(index=["panel", "key"], columns="gross", values="dSharpe")))

    # ------------------------------------------------ significance of the headline
    P("\n" + "=" * 200)
    P(f"IS THE DIFFERENCE BIGGER THAN ITS OWN NOISE? stationary block bootstrap on the PAIRED daily")
    P(f"difference GATE_OFF - GATE_ON at n={N_HEAD}, {COST_MAIN} bps ({BOOT_DRAWS} draws, mean block {BOOT_BLOCK}d, seed {SEED_BOOT})")
    P("=" * 200)
    boot_rows = []
    for kname in ("COMP", "V1KEY"):
      for g in GROSSES:
        for pk in panels:
            ra, ta = books[(pk, kname, g, "GATE_OFF", N_HEAD)]
            rb, tb = books[(pk, kname, g, "GATE_ON", N_HEAD)]
            d = net(ra, ta, COST_MAIN) - net(rb, tb, COST_MAIN)
            obs, lo, hi, p0 = block_boot_sharpe_diff(d, BOOT_DRAWS, BOOT_BLOCK, SEED_BOOT)
            d_oos = d.loc[OOS_START:]
            obs_o, lo_o, hi_o, p0_o = block_boot_sharpe_diff(d_oos, BOOT_DRAWS, BOOT_BLOCK, SEED_BOOT + 1)
            boot_rows.append(dict(key=kname, gross=g, panel=pk, diff_ann_ret=float(d.mean() * 252), diff_Sharpe=obs,
                                  ci_lo=lo, ci_hi=hi, P_le_0=p0,
                                  oos_diff_Sharpe=obs_o, oos_ci_lo=lo_o, oos_ci_hi=hi_o, oos_P_le_0=p0_o))
    boot = pd.DataFrame(boot_rows).set_index(["key", "gross", "panel"])
    boot.to_csv(OUT / f"{STEM}.bootstrap.csv")
    P(fmt(boot))

    # ------------------------------------------------ rule 8 walk-forward
    P("\n" + "=" * 200)
    P("RULE 8 WALK-FORWARD - every selector fixed before any OOS number was read; params on 2009-2016, 2017-2026 read ONCE")
    P("  A0 GATE_ON n=20 (do-nothing) | A1 GATE_OFF n=20 (THE PRE-REGISTERED CORNER)")
    P("  S1 IS-argmax over (arm, n)   | S2 IS-argmax over n with the arm pinned ON | S3 random (arm, n), fixed seed")
    P("=" * 200)
    rng = np.random.default_rng(SEED_S3)
    wf = []
    for kname in ("COMP", "V1KEY"):
     for g in GROSSES:
      for pk in panels:
        cells = [(a, n) for a in ("GATE_ON", "GATE_OFF") for n in NS if (pk, kname, g, a, n) in books]
        for c in RUNGS:
            def IS(a, n):
                r0, tno = books[(pk, kname, g, a, n)]
                return metrics(net(r0, tno, c).loc[:IS_END])["Sharpe"]
            def OOS(a, n):
                r0, tno = books[(pk, kname, g, a, n)]
                m = metrics(net(r0, tno, c).loc[OOS_START:])
                return m["Sharpe"], m["CAGR"], m["MaxDD"]
            s1 = max(cells, key=lambda k: IS(*k))
            s2 = max([k for k in cells if k[0] == "GATE_ON"], key=lambda k: IS(*k))
            s3 = cells[int(rng.integers(0, len(cells)))]
            orc = max(cells, key=lambda k: OOS(*k)[0])
            a0, a1 = ("GATE_ON", N_HEAD), ("GATE_OFF", N_HEAD)
            row = dict(key=kname, gross=g, panel=pk, bps=c)
            for tag, k in [("A0", a0), ("A1", a1), ("S1", s1), ("S2", s2), ("S3", s3), ("ORACLE", orc)]:
                sh, cg, dd = OOS(*k)
                row[f"{tag}_pick"] = f"{k[0]}/n{k[1]}"
                row[f"{tag}_OOS_Sharpe"] = sh
                row[f"{tag}_OOS_CAGR"] = cg
                row[f"{tag}_OOS_MaxDD"] = dd
            row["A1_minus_A0"] = row["A1_OOS_Sharpe"] - row["A0_OOS_Sharpe"]
            row["S1_minus_A0"] = row["S1_OOS_Sharpe"] - row["A0_OOS_Sharpe"]
            row["S2_minus_A0"] = row["S2_OOS_Sharpe"] - row["A0_OOS_Sharpe"]
            row["S3_minus_A0"] = row["S3_OOS_Sharpe"] - row["A0_OOS_Sharpe"]
            row["S1_regret"] = row["ORACLE_OOS_Sharpe"] - row["S1_OOS_Sharpe"]
            row["SPY_OOS_Sharpe"] = refs[pk]["spy_oos"]["Sharpe"]
            row["v2_OOS_Sharpe"] = refs[pk]["v2_oos"]["Sharpe"]
            wf.append(row)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(fmt(W.set_index(["key", "gross", "panel", "bps"])[["A0_OOS_Sharpe", "A1_OOS_Sharpe", "A1_minus_A0",
                                                         "S1_pick", "S1_OOS_Sharpe", "S1_minus_A0",
                                                         "S2_minus_A0", "S3_minus_A0", "SPY_OOS_Sharpe", "v2_OOS_Sharpe"]]))
    P("")
    P(f"  A1 - A0 (THE PRE-REGISTERED CORNER, no selector): mean {W.A1_minus_A0.mean():+.4f}, "
      f"wins {int((W.A1_minus_A0 > 0).sum())}/{len(W)} ({(W.A1_minus_A0 > 0).mean():.1%})")
    P(f"  S1 - A0 (idea 228's chooser, rebuilt)           : mean {W.S1_minus_A0.mean():+.4f}, "
      f"wins {int((W.S1_minus_A0 > 0).sum())}/{len(W)} ({(W.S1_minus_A0 > 0).mean():.1%})   "
      f"[idea 228 published +0.1049 / 85.7% on the V dial]")
    P(f"  S2 - A0 (chooser DENIED the corner)             : mean {W.S2_minus_A0.mean():+.4f}, "
      f"wins {int((W.S2_minus_A0 > 0).sum())}/{len(W)}")
    P(f"  S3 - A0 (random pick, the size-matched null)    : mean {W.S3_minus_A0.mean():+.4f}, "
      f"wins {int((W.S3_minus_A0 > 0).sum())}/{len(W)}")
    P(f"  S1 mean regret vs the OOS oracle: {W.S1_regret.mean():+.4f}")
    picks = W.S1_pick.str.split("/").str[0].value_counts()
    P(f"  what S1 actually picks: {dict(picks)}   (n: {dict(W.S1_pick.str.split('/n').str[1].value_counts())})")
    P(f"  A1 beats SPY OOS in {int((W.A1_OOS_Sharpe > W.SPY_OOS_Sharpe).sum())}/{len(W)}, "
      f"RULES v2 OOS in {int((W.A1_OOS_Sharpe > W.v2_OOS_Sharpe).sum())}/{len(W)}")
    P(f"  A0 beats SPY OOS in {int((W.A0_OOS_Sharpe > W.SPY_OOS_Sharpe).sum())}/{len(W)}, "
      f"RULES v2 OOS in {int((W.A0_OOS_Sharpe > W.v2_OOS_Sharpe).sum())}/{len(W)}")

    # ------------------------------------------------ KEEP paths
    P("\n" + "=" * 200)
    P(f"BOTH KEEP PATHS on all {len(grid)} grid points (4a vs the LIVE RULES v2; 4b vs SPY)")
    P("=" * 200)
    keep = grid.assign(pass4a=grid.fail4a == "-", pass4a_v1=grid.fail4a_v1 == "-", pass4b=grid.fail4b == "-")
    kt = keep.groupby(["key", "gross", "panel", "arm", "bps"])[["pass4a", "pass4a_v1", "pass4b"]].sum()
    kt.to_csv(OUT / f"{STEM}.keep.csv")
    P(fmt(kt.unstack("bps"), p=0))
    P(f"\n  4a passes {int(keep.pass4a.sum())}/{len(keep)} (vs RULES v1: {int(keep.pass4a_v1.sum())}/{len(keep)}); "
      f"4b passes {int(keep.pass4b.sum())}/{len(keep)}")
    for arm in ("GATE_ON", "GATE_OFF"):
        k = keep[keep.arm == arm]
        P(f"    {arm:<9} 4a {int(k.pass4a.sum()):>3}/{len(k)}   4b {int(k.pass4b.sum()):>3}/{len(k)}")
    b4 = keep[keep.pass4b]
    if len(b4):
        P("\n  every 4b passer (all rungs):")
        P(fmt(b4[["key", "gross", "panel", "arm", "n", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "turn_yr"]]
              .sort_values(["key", "gross", "panel", "arm", "n", "bps"]).set_index(["key", "gross", "panel", "arm", "n", "bps"])))
        at_p = b4[b4.bps == COST_MAIN]
        P(f"\n  at PROTOCOL's own {COST_MAIN} bps: {len(at_p)} of {len(keep[keep.bps == COST_MAIN])} points pass 4b "
          f"(GATE_OFF {int((at_p.arm == 'GATE_OFF').sum())}, GATE_ON {int((at_p.arm == 'GATE_ON').sum())})")
    P("\n  binding 4b bar counts at 10 bps (which bar kills each point):")
    fb = keep[keep.bps == COST_MAIN].fail4b.str.split(",").explode().value_counts()
    P("   ", dict(fb))

    # ------------------------------------------------ verdict
    P("\n" + "=" * 200)
    P("VERDICT")
    P("=" * 200)
    d10 = dhead[dhead.bps == COST_MAIN]
    P(f"  The corner at PROTOCOL's own rung ({COST_MAIN} bps), n={N_HEAD}:")
    for _, r in d10.iterrows():
        P(f"    {r.panel:<9} ON {r.ON_Sharpe:.4f} -> OFF {r.OFF_Sharpe:.4f}  (d {r.dSharpe:+.4f}); "
          f"OOS {r.ON_OOS:.4f} -> {r.OFF_OOS:.4f} (d {r.dOOS:+.4f}); dCAGR {r.dCAGR:+.2%}; dMaxDD {r.dMaxDD:+.2%}")
    P(f"  Pre-registered A1-A0 OOS mean {W.A1_minus_A0.mean():+.4f} vs the SELECTED S1-A0 {W.S1_minus_A0.mean():+.4f}.")
    P(f"  Bootstrap P(paired Sharpe diff <= 0) at g={GROSS_HEAD:.2f}: " +
      ", ".join(f"{pk} {boot.loc[('COMP', GROSS_HEAD, pk), 'P_le_0']:.3f} (OOS {boot.loc[('COMP', GROSS_HEAD, pk), 'oos_P_le_0']:.3f})"
                for pk in panels))
    P(f"  4a {int(keep.pass4a.sum())}/{len(keep)}; 4b {int(keep.pass4b.sum())}/{len(keep)}.")
    P(f"\n  runtime {time.time()-t0:.1f}s")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
