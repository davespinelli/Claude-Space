#!/usr/bin/env python3
"""Idea 551 - "restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain" (lane C, 2026-09-09).

The question
------------
Idea 298 (2026-09-06, cloud) killed the `share ~ c_bar` discount curve and put a ZERO-PARAMETER
prescription in its place:

    "subtract the gate's own timing residual (~0.0 pp/yr for a pure-exposure gate,
     0.3-0.6 pp/yr for an MA gate), INDEPENDENT of c_bar."

Idea 300 turned that prose into a hard number: `BAR_MA_RESID = (-0.70, -0.20)` pp/yr, a
pre-registered band that a matched MA arm's mean resid0 has to sit inside before the rest of
that script is allowed to speak.  The band has since been quoted forward as a prior.

Idea 307 (lane B, today) found the band is CADENCE-BOUND.  On SMALL439 the MA gate's mean
resid0 reads -0.0904 at DAILY and -0.1078 at ANNUAL - both OUTSIDE [-0.70, -0.20] - against
-0.6871 at QUARTERLY.  The "level-independent lump" is largest in the middle of the cadence dial
and collapses at both ends.  Idea 298 and idea 300 both ran CADENCES = ["W", "M", "Q"]: the band
was fitted on the interior of a dial and published without the dial's name on it.

Two things follow, and only one of them is bookkeeping:

  (a) THE AUDIT.  Every committed result that used the band as a BAR or as a PRIOR inherits a
      cadence restriction that was never stated.  How many of those uses CHANGE VERDICT once the
      band is quoted with its domain?  If they all ran inside W/M/Q the answer is zero and the
      correction is a stamp, not a retraction.  That has to be measured, not assumed.

  (b) THE DOMAIN ITSELF.  Idea 307 measured the cadence profile on SMALL439 ONLY.  Idea 298
      fitted the band on THREE panels (per-panel intercepts -0.619 / -0.267 / -0.352 pp,
      t -5.43 / -3.16 / -3.96).  So the queue's premise - "the band is a W/M/Q fact" - is itself
      a one-panel fact until D and A are read on U56 and B136.  Ten of the fifteen
      (panel x cadence) cells this question needs have never been run.

This script runs all fifteen, on both constructions and both gate families, and then re-scores
the census.

Pre-registered hypotheses and bars (written before any U56 or B136 extreme-cadence number was read)
---------------------------------------------------------------------------------------------------
H_DOMAIN (the queue's premise, stated as a testable claim).  The published band [-0.70, -0.20]
    is exactly the W/M/Q interior of the cadence dial, on EVERY panel.
    BAR, both clauses:
      (1) the MA-THRESH mean resid0 is INSIDE the band in all 9 interior cells
          (3 panels x {W, M, Q});
      (2) it is OUTSIDE the band in all 6 extreme cells (3 panels x {D, A}).
    H_DOMAIN holds only if both clauses hold.

H_ONE_PANEL (the rival).  The collapse at the extremes is a SMALL439 fact that idea 307
    generalised without a second panel.
    BAR: at least one LARGE panel (U56 or B136) has its D mean OR its A mean INSIDE the band.
    H_DOMAIN and H_ONE_PANEL are mutually exclusive on clause (2) and jointly exhaustive there;
    clause (1) can fail on its own, which would mean the band is not even an interior fact and
    idea 300's gate passed on a pooled mean that hides panel-level failures.

H_AUDIT (the deliverable the queue asked for).  No committed use of the band changes verdict
    once the band is quoted with its cadence domain, because every use ran inside W/M/Q.
    BAR: flip count == 0 over the census, where a use FLIPS if
      (i)  it was evaluated at a cadence outside the measured domain (its clause becomes
           UNDEFINED rather than PASS), or
      (ii) its published POOLED-across-cadence reading passes the band while the same clause
           read PER-CADENCE fails at one or more of its own cadences (or vice versa).
    H_AUDIT fails if any use flips on either limb.

The census rule (fixed before running it, so the denominator is not chosen after the fact)
-------------------------------------------------------------------------------------------
Scan every .py and .md under research/ EXCEPT the four ledgers (QUEUE.md, LEADERBOARD.md,
CHANGELOG.md, PROTOCOL.md - they restate, they do not use) and except this file.  A stem is a
USE if it matches
    BAR    : the literal band pair -0.70 / -0.20 within 20 characters of each other in a .py
             (i.e. a constant or a comparison), or
    PRIOR  : the prescription in prose - "0.3-0.6 pp/yr" / "0.3..0.6 pp/yr" / "-0.3..-0.6" /
             "level-independent lump" / "lump of -0.38"
and is classified BAR if any of its files matches the BAR pattern, else PRIOR.  Ledgers and
console logs are counted separately and never scored (a console is an artefact of a script that
is already in the census).  Each use's CADENCE DOMAIN is read from its own source:
`CADENCES = [...]` in the .py.  Uses with no recoverable cadence list are reported as UNKNOWN
and counted against H_AUDIT, not silently dropped.

G0 - reproduction / validity gates, asserted and printed BEFORE any headline number
-----------------------------------------------------------------------------------
G0.1  The local cadence-extended runner must equal `engine.backtest` EXACTLY at the four
      cadences the engine supports (D, W, M, Q), on every panel: max |dr_t| < 1e-15 and zero
      mask-disagreement bars.  `engine.rebalance_mask` has no "A" and PROTOCOL forbids editing
      the engine, so the annual arm runs through a local copy of the engine's own loop with one
      extra period key.  Without this gate the A column is a different backtester.
G0.2  Idea 298's committed `.decomp.csv` MA-THRESH cells must reproduce on ALL THREE panels at
      W/M/Q: max |d resid0| < 1e-6 pp/yr over the 81 shared cells
      (3 panels x 9 thetas x 3 cadences).  This is the band's own source table.
G0.3  Idea 307's committed `.decomp.csv` MA-THRESH cells must reproduce on SMALL439 at ALL FIVE
      cadences: max |d resid0| < 1e-6 pp/yr over 45 shared cells.  This is the cadence profile
      the queue is quoting.
G0.4  The identity r_dg,t == c_t * r_rs,t at 0 bps (idea 290), max |error| < 1e-12, at every
      cadence on every panel.
G0.5  Matching quality: |mask fraction(QUANTILE-M) - mask fraction(MA-THRESH)| < 0.01 at all 9
      thetas on all 3 panels, so "at matched c_bar" is true where it is claimed.
G0.6  LIVE RULES v2 on U56, weekly, 10 bps: 8.66% / 1.2056 / -12.05%.

Design
------
PANELS (a REPORTED contrast, 3 values - the whole point is that idea 307 had one):
  U56       research/universe.json (ETFs + mega caps), SPY held out as benchmark.
  B136      research/universe_broad.json (~100 large caps + 36 ETFs), SPY held out.
  SMALL439  data/prices_small.csv.gz sub-$2B names less the 44 with max_1d_move >= 1.0.

FAMILIES (a REPORTED contrast, not a dial):
  MA-THRESH   IN where px > ma200*(1+theta).  The band's own gate.
  QUANTILE-M  IN the top ceil(x*n_t) live names by px/ma200-1, x set to the MA arm's OWN mean
              mask fraction at that theta on that panel.  Same ranking, same mean exposure,
              CONSTANT depth.  Carried as the control that separates "the MA gate's residual
              collapses at the extremes" from "the decomposition collapses at the extremes".

CONSTRUCTIONS (both reported): RESPREAD (w = GROSS/k_t, exposure pinned) and DEGROSS
  (w = GROSS/n_t, gated weight to cash).  resid0 is defined on the pair:
      resid0 = [CAGR0(DEGROSS) - CAGR0(RESPREAD)] - [CAGR0(c_bar * r_RESPREAD) - CAGR0(r_RESPREAD)]

Tuned parameters (PROTOCOL rule 4: at most two)
    1. cadence   5 values: D, W, M, Q, A          <- the dial the band forgot to name
    2. bar       5 band widths: half-width multiples m in {0.5, 0.75, 1.0, 1.5, 2.0} around the
                 published centre -0.45 (m = 1.0 IS the published [-0.70, -0.20])
Theta is idea 298/300/307's grid VERBATIM (9 values, not chosen here) and is reported in full;
x is a deterministic function of theta (the matching), not a dial; panel, family and
construction are reported contrasts.  ALL grid points are reported.

Grid: 9 theta x 5 cadence x 2 family x 2 construction x 3 panels = 540 books, 135 decomposition
cells.  Gross 0.75, 10 bps, next-day execution, no shorting, no leverage.  The 0-bps rung every
residual uses is DERIVED exactly (r0 = r10 + turnover*bps/1e4) from the same book, not re-run.

Rule 8 walk-forward (required; directions fixed before any OOS number was read)
  WF-A (the book).  Within each panel x family x construction, (theta, cadence) is chosen on
        2010..2016-12-31 by IS Sharpe and 2017-01-01..2026 is read ONCE.  OOS CAGR / Sharpe /
        MaxDD against RULES v2 (live), SPY and the cadence-matched no-gate EWall control.
  WF-B (the band as a predictor - the headline).  Fit the band on IS ONLY, two ways:
        UNQUALIFIED  one band for the whole dial: IS mean +/- 2 sd over all cadences pooled;
        QUALIFIED    one band per cadence: that cadence's IS mean +/- 2 sd.
        Score both on the untouched OOS window: coverage (share of OOS per-(panel, theta) resid0
        inside the band) and MAE of the band CENTRE against the OOS resid0, per cadence, with a
        hard ZERO carried as the third predictor.  If the qualified band does not beat the
        unqualified one out of sample, the cadence stamp is cosmetic and should be reported as
        such.
  WF-C (the domain).  Re-run H_DOMAIN's two clauses on the IS window alone and on the OOS window
        alone.  A domain that only exists in one window is not a domain.

Verdicts (both KEEP paths, on every one of the 540 books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: data/prices_small.csv.gz and research/universe_broad.json are CURRENT constituents
- no delistings - so every CAGR LEVEL is inflated and the 4a/4b columns inherit the bias whole.
The headline is an arm-minus-arm contrast on the SAME names, SAME ranking and SAME days, so the
bias very largely cancels out of resid0; it does NOT cancel out of the KEEP columns.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .decomp.csv .band.csv .census.csv .walkforward.csv .console.txt
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest as engine_backtest, rebalance_mask as engine_mask, metrics

COST_BPS = 10
GROSS = 0.75
CADENCES = ["D", "W", "M", "Q", "A"]
INTERIOR = ["W", "M", "Q"]                 # idea 298/300's published cadences
EXTREMES = ["D", "A"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
FAMILIES = ["MA-THRESH", "QUANTILE-M"]
PANELS = ["U56", "B136", "SMALL439"]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

# ---- the object under test: idea 300's pre-registered band, and the bar dial around it
BAND_PUB = (-0.70, -0.20)                  # idea 300 BAR_MA_RESID, pp/yr
BAND_CENTRE = 0.5 * (BAND_PUB[0] + BAND_PUB[1])       # -0.45
BAND_HALF = 0.5 * (BAND_PUB[1] - BAND_PUB[0])         # 0.25
BAR_M = [0.5, 0.75, 1.0, 1.5, 2.0]         # tuned dial 2: half-width multiples

# ---- gate tolerances
BAR_ENGINE = 1e-15
BAR_REPRO = 1e-6
BAR_IDENT = 1e-12
BAR_MASK_TOL = 0.01
LIVE_PUB = (0.0866, 1.2056, -0.1205)
BAR_LIVE = 5e-4

PRIOR298 = REPO / "research" / "backtests" / \
    "2026-09-06_does-the-cash-drag-share-depend-on-the-panel-or-on-the-gate-level_cloud.decomp.csv"
PRIOR307 = REPO / "research" / "backtests" / \
    "2026-09-09_does-the-QUANTILE-zero-residual-hold-at-DAILY-and-ANNUAL-cadence_B.decomp.csv"

OUT = Path(__file__).with_suffix("")
SELF = Path(__file__).name
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 800)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- cadence + local engine
def cad_mask(idx, cad):
    """True on the last trading bar of each cadence block.  Identical to
    engine.rebalance_mask for D/W/M/Q; adds A (calendar year)."""
    if cad == "D":
        return pd.Series(True, index=idx)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"),
           "Q": idx.to_period("Q"), "A": idx.to_period("Y")}[cad]
    s = pd.Series(key, index=idx)
    return s != s.shift(-1)


def bt(prices, weights, cost_bps=COST_BPS, cad="W"):
    """Copy of engine.backtest's loop with the cadence mask swapped for one that also knows
    "A".  G0.1 asserts it equals engine.backtest at D/W/M/Q on every panel."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = cad_mask(prices.index, cad).shift(1, fill_value=False)
    cur = np.zeros(len(prices.columns))
    wv, rv, mv = w_target.values, rets.values, mask.values
    hv = np.zeros_like(wv)
    tv = np.zeros(len(prices.index))
    for i in range(len(prices.index)):
        if mv[i] or i == 0:
            new = wv[i]
            tv[i] = np.abs(new - cur).sum()
            cur = new
        hv[i] = cur
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    held = pd.DataFrame(hv, index=prices.index, columns=prices.columns)
    turnover = pd.Series(tv, index=prices.index)
    port = (held * rets).sum(axis=1) - turnover * cost_bps / 1e4
    return {"returns": port, "weights": held, "turnover": turnover}


# ---------------------------------------------------------------- panels (idea 298's, verbatim)
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0)")
    for nm, (p, _) in out.items():
        P(f"  {nm}: {p.index[0].date()} .. {p.index[-1].date()}  ({len(p)} days)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def ma_gate(px, theta):
    return (px > px.rolling(200).mean() * (1 + theta)) & live_mask(px)


def quantile_gate(px, x):
    live = live_mask(px)
    dist = (px / px.rolling(200).mean() - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * GROSS
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * GROSS


def control_book(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0) * GROSS


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


def in_band(v, lo, hi):
    return bool(lo <= v <= hi)


# ---------------------------------------------------------------- the census
CENSUS_BAR = re.compile(r"-0\.70(?![0-9]).{0,20}?-0\.20(?![0-9])"
                        r"|-0\.20(?![0-9]).{0,20}?-0\.70(?![0-9])", re.S)
CENSUS_DOMAIN = re.compile(r"cadence-bound|W/M/Q fact|stated bound|cadence domain", re.I)
CENSUS_PRIOR = re.compile(
    r"0\.3\s*[-–.]{1,3}\s*0\.6\s*pp|-0\.3\s*\.\.\s*-0\.6|level-independent lump|lump of -0\.38",
    re.I)
LEDGERS = {"QUEUE.md", "LEADERBOARD.md", "CHANGELOG.md", "PROTOCOL.md"}


def census():
    """Every committed file that USES the band as a bar or a prior, by the rule in the
    docstring.  Ledgers and console/artefact files are counted but never scored."""
    root = REPO / "research"
    rows = {}
    ledger_hits, console_hits = [], []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in (".py", ".md", ".txt"):
            continue
        if p.name == SELF or p.name.startswith(OUT.name):
            continue
        try:
            t = p.read_text(errors="ignore")
        except Exception:
            continue
        is_bar = bool(CENSUS_BAR.search(t)) and p.suffix == ".py"
        is_prior = bool(CENSUS_PRIOR.search(t)) or bool(CENSUS_BAR.search(t))
        if not (is_bar or is_prior):
            continue
        if p.name in LEDGERS:
            ledger_hits.append(p.name)
            continue
        if p.suffix == ".txt":
            console_hits.append(p.name)
            continue
        stem = p.name.split(".")[0]
        r = rows.setdefault(stem, dict(stem=stem, role="PRIOR", files=[]))
        r["files"].append(p.name)
        if is_bar:
            r["role"] = "BAR"
    # cadence domain of each use, read from its own source
    for stem, r in rows.items():
        src = root / "backtests" / f"{stem}.py"
        cads, pans = "UNKNOWN", "UNKNOWN"
        if src.exists():
            t = src.read_text(errors="ignore")
            m = re.search(r"^CADENCES\s*=\s*\[([^\]]*)\]", t, re.M)
            if m:
                found = [a or b for a, b in
                         re.findall(r'"([A-Z])"|\'([A-Z])\'', m.group(1))]
                cads = ",".join(sorted(found, key=lambda c: CADENCES.index(c)
                                       if c in CADENCES else 99)) or "LIST-EMPTY"
            elif "CADENCES" in t:
                cads = "LIST-NOT-PARSED"
            mp = re.search(r"^PANELS\s*=\s*\[([^\]]*)\]", t, re.M)
            if mp:
                pans = ",".join(re.findall(r'"([A-Za-z0-9]+)"', mp.group(1)))
            elif "SMALL439" in t and "U56" not in t:
                pans = "SMALL439"
            elif "SMALL439" in t:
                pans = "SMALL439(+)"
        else:
            cads = "NO-SCRIPT"
        res = root / "backtests" / f"{stem}.result.md"
        r["states_domain"] = bool(res.exists() and
                                  CENSUS_DOMAIN.search(res.read_text(errors="ignore")))
        r["cadences"] = cads
        r["panels"] = pans
        r["files"] = ";".join(sorted(r["files"]))
    return pd.DataFrame(rows.values()), ledger_hits, console_hits


# ---------------------------------------------------------------- main
def main():
    P("=" * 178)
    P("Idea 551 restate-idea-298s-MA-RESIDUAL-BAND-with-its-cadence-domain (lane C) | " + SELF)
    P("=" * 178)
    P(f"THE OBJECT UNDER TEST: idea 300's BAR_MA_RESID = {BAND_PUB} pp/yr, idea 298's "
      f"'0.3-0.6 pp/yr for an MA gate, independent of c_bar'.")
    P(f"costs {COST_BPS} bps (0-bps rung DERIVED exactly as r0 = r10 + turnover*bps/1e4), "
      f"gross {GROSS}, next-day execution, no shorting, no leverage.")
    P(f"tuned dials (2): cadence {CADENCES} x bar half-width multiple {BAR_M} around centre "
      f"{BAND_CENTRE:+.2f} (m=1.0 IS the published band).  ALL grid points reported.")
    P(f"reported contrasts: panel {PANELS} x family {FAMILIES} x construction {CONSTRUCTIONS} "
      f"x theta {MA_THETA}  ->  540 books, 135 decomposition cells.")
    P("pre-registered bars (written before any U56/B136 extreme-cadence number was read):")
    P(f"  H_DOMAIN   : MA mean resid0 INSIDE {BAND_PUB} in all 9 interior (panel x W/M/Q) cells "
      f"AND OUTSIDE it in all 6 extreme (panel x D/A) cells")
    P("  H_ONE_PANEL: at least one of U56/B136 has its D or A mean INSIDE the band")
    P("  H_AUDIT    : flip count == 0 over the census (out-of-domain use, or pooled-vs-per-cadence "
      "reading disagreeing)")
    P(f"  G0.1 local runner == engine.backtest at D/W/M/Q on every panel, < {BAR_ENGINE:.0e}")
    P(f"  G0.2 idea 298 .decomp.csv MA resid0 reproduces, 3 panels x W/M/Q, < {BAR_REPRO:.0e} pp/yr")
    P(f"  G0.3 idea 307 .decomp.csv MA resid0 reproduces, SMALL439 x 5 cadences, < {BAR_REPRO:.0e}")
    P(f"  G0.4 identity |r_dg - c_t*r_rs| < {BAR_IDENT:.0e} at every cadence on every panel")
    P(f"  G0.5 |d mask fraction(Q - MA)| < {BAR_MASK_TOL} at all 9 thetas on all 3 panels")
    P(f"  G0.6 LIVE RULES v2 U56 = {LIVE_PUB[0]:.2%} / {LIVE_PUB[1]:.4f} / {LIVE_PUB[2]:.2%}")
    P("SURVIVORSHIP: SMALL439 and B136 are current constituents of their screens; CAGR LEVELS "
      "inflated, arm-minus-arm residuals very largely immune, the 4a/4b columns are NOT.")
    flush_log()

    PX = panels()

    # --------------------------------------------- G0.6 live book
    px_u = load_universe()
    live_full = engine_backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS,
                                freq="W")["returns"]
    lv = metrics(live_full.loc[px_u.index[260]:])
    ok_g06 = (abs(lv["CAGR"] - LIVE_PUB[0]) < BAR_LIVE and abs(lv["Sharpe"] - LIVE_PUB[1]) < BAR_LIVE
              and abs(lv["MaxDD"] - LIVE_PUB[2]) < BAR_LIVE)
    P("\n" + "=" * 178)
    P("G0 GATES")
    P("=" * 178)
    P(f"G0.6 {'PASS' if ok_g06 else 'FAIL'}  LIVE RULES v2 U56 {lv['CAGR']:.2%} / "
      f"{lv['Sharpe']:.4f} / {lv['MaxDD']:.2%}  (published "
      f"{LIVE_PUB[0]:.2%} / {LIVE_PUB[1]:.4f} / {LIVE_PUB[2]:.2%})")

    # --------------------------------------------- G0.1 engine equivalence, every panel
    g01 = []
    for pname in PANELS:
        px = PX[pname][0]
        probe = book(px, ma_gate(px, 0.00), "DEGROSS")
        for cad in ["D", "W", "M", "Q"]:
            a = engine_backtest(px, probe, cost_bps=COST_BPS, freq=cad)["returns"]
            b = bt(px, probe, cost_bps=COST_BPS, cad=cad)["returns"]
            mk = int((cad_mask(px.index, cad).values != engine_mask(px.index, cad).values).sum())
            g01.append(dict(panel=pname, cad=cad, max_abs_dr=float((a - b).abs().max()),
                            mask_diff_bars=mk))
    G01 = pd.DataFrame(g01)
    ok_g01 = bool(G01.max_abs_dr.max() < BAR_ENGINE and G01.mask_diff_bars.max() == 0)
    P(f"G0.1 {'PASS' if ok_g01 else 'FAIL'}  worst |dr_t| = {G01.max_abs_dr.max():.3e} over "
      f"{len(G01)} (panel x cadence) probes, mask-disagreement bars "
      f"{int(G01.mask_diff_bars.max())}")
    flush_log()

    # --------------------------------------------- matching (G0.5)
    gates, match = {}, []
    for pname in PANELS:
        px = PX[pname][0]
        start = px.index[260]
        gates[pname] = {}
        for th in MA_THETA:
            gma = ma_gate(px, th)
            live = live_mask(px)
            frac_ma = float((gma.sum(axis=1) / live.sum(axis=1).clip(lower=1)).loc[start:].mean())
            gq = quantile_gate(px, frac_ma)
            frac_q = float((gq.sum(axis=1) / live.sum(axis=1).clip(lower=1)).loc[start:].mean())
            gates[pname][th] = {"MA-THRESH": gma, "QUANTILE-M": gq}
            match.append(dict(panel=pname, theta=th, x=frac_ma, frac_ma=frac_ma, frac_q=frac_q,
                              d_frac=frac_q - frac_ma))
    M = pd.DataFrame(match)
    ok_g05 = bool(M.d_frac.abs().max() < BAR_MASK_TOL)
    P(f"G0.5 {'PASS' if ok_g05 else 'FAIL'}  worst |d mask fraction| = "
      f"{M.d_frac.abs().max():.5f} at {BAR_MASK_TOL} over {len(M)} (panel x theta) cells")
    flush_log()

    # --------------------------------------------- the 540-book grid
    P("\n" + "=" * 178)
    P("RUNNING THE 540-BOOK GRID (3 panel x 9 theta x 5 cadence x 2 family x 2 construction)")
    P("=" * 178)
    rows, decomp = [], []
    ident_worst = 0.0
    for pname in PANELS:
        px, spy_px = PX[pname]
        start = px.index[260]
        years = len(px.loc[start:]) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.loc[start:])
        ctrl = {}
        for cad in CADENCES:
            rc = bt(px, control_book(px), cost_bps=COST_BPS, cad=cad)["returns"].loc[start:]
            ctrl[cad] = stat(rc)
        P(f"\nPANEL {pname}: from {start.date()} ({years:.2f} yrs) | "
          f"SPY {spy_s['CAGR']:.2%}/{spy_s['Sharpe']:.4f}/{spy_s['MaxDD']:.2%} | "
          f"LIVE v2 {live_s['CAGR']:.2%}/{live_s['Sharpe']:.4f}/{live_s['MaxDD']:.2%} | "
          f"EWall-W {ctrl['W']['CAGR']:.2%}/{ctrl['W']['Sharpe']:.4f}/{ctrl['W']['MaxDD']:.2%}")
        flush_log()
        for th in MA_THETA:
            for cad in CADENCES:
                for fam in FAMILIES:
                    g = gates[pname][th][fam]
                    arms = {}
                    for con in CONSTRUCTIONS:
                        res = bt(px, book(px, g, con), cost_bps=COST_BPS, cad=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        r0 = r10 + turn * COST_BPS / 1e4
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        arms[con] = dict(r0=r0, gross=grs, s=s)
                        rows.append(dict(panel=pname, theta=th,
                                         x=float(M[(M.panel == pname) & (M.theta == th)].x.iloc[0]),
                                         cad=cad, family=fam, con=con, **s, CAGR0=cagr(r0),
                                         gross_mean=float(grs.mean()),
                                         turn_yr=float(turn.sum() / years),
                                         dSharpe_ctrl=s["Sharpe"] - ctrl[cad]["Sharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = arms["DEGROSS"], arms["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    ident = float((dg["r0"] - c_t * rs["r0"]).abs().max())
                    ident_worst = max(ident_worst, ident)

                    def dec(lo, hi, tag, rs=rs, dg=dg, c_t=c_t):
                        sl = slice(lo, hi)
                        rr, rd = rs["r0"].loc[sl], dg["r0"].loc[sl]
                        cb = float(c_t.loc[sl].mean())
                        g0 = 100 * (cagr(rd) - cagr(rr))
                        p0 = 100 * (cagr(cb * rr) - cagr(rr))
                        return dict(window=tag, c_bar=cb, c_sd=float(c_t.loc[sl].std()),
                                    gap0_pp=g0, pred0_pp=p0, resid0_pp=g0 - p0,
                                    share=(p0 / g0 if abs(g0) > 1e-9 else np.nan),
                                    CAGR_rs0=cagr(rr), CAGR_dg0=cagr(rd))

                    base = dict(panel=pname, theta=th, cad=cad, family=fam, ident_max_err=ident)
                    for tag, lo, hi in (("FULL", None, None), ("IS", None, IS_END),
                                        ("OOS", OOS_START, None)):
                        decomp.append({**base, **dec(lo, hi, tag)})
        P(f"  {pname} done ({len(rows)} book rows so far)")
        flush_log()

    G = pd.DataFrame(rows)
    D = pd.DataFrame(decomp)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    D.to_csv(f"{OUT}.decomp.csv", index=False)
    ok_g04 = bool(ident_worst < BAR_IDENT)
    P(f"\nG0.4 {'PASS' if ok_g04 else 'FAIL'}  worst identity error = {ident_worst:.3e} "
      f"at {BAR_IDENT:.0e}")

    # --------------------------------------------- G0.2 / G0.3 reproduction
    F = D[D.window == "FULL"]
    p298 = pd.read_csv(PRIOR298)
    p298 = p298[(p298.family == "MA-THRESH") & (p298.window == "FULL")]
    j2 = p298[["panel", "level", "cad", "resid0_pp", "c_bar"]].merge(
        F[F.family == "MA-THRESH"][["panel", "theta", "cad", "resid0_pp", "c_bar"]],
        left_on=["panel", "level", "cad"], right_on=["panel", "theta", "cad"],
        suffixes=("_298", "_me"))
    d2 = (j2.resid0_pp_298 - j2.resid0_pp_me).abs()
    ok_g02 = bool(len(j2) == 81 and d2.max() < BAR_REPRO)
    P(f"G0.2 {'PASS' if ok_g02 else 'FAIL'}  idea 298 MA resid0: matched {len(j2)}/81 cells, "
      f"worst |d resid0| = {d2.max():.3e} pp/yr, worst |d c_bar| = "
      f"{(j2.c_bar_298 - j2.c_bar_me).abs().max():.3e}")

    p307 = pd.read_csv(PRIOR307)
    p307 = p307[(p307.family == "MA-THRESH") & (p307.window == "FULL")]
    j3 = p307[["theta", "cad", "resid0_pp"]].merge(
        F[(F.family == "MA-THRESH") & (F.panel == "SMALL439")][["theta", "cad", "resid0_pp"]],
        on=["theta", "cad"], suffixes=("_307", "_me"))
    d3 = (j3.resid0_pp_307 - j3.resid0_pp_me).abs()
    ok_g03 = bool(len(j3) == 45 and d3.max() < BAR_REPRO)
    P(f"G0.3 {'PASS' if ok_g03 else 'FAIL'}  idea 307 MA resid0 (SMALL439, 5 cadences): matched "
      f"{len(j3)}/45 cells, worst |d resid0| = {d3.max():.3e} pp/yr")
    P(f"\nALL GATES: G0.1 {ok_g01} G0.2 {ok_g02} G0.3 {ok_g03} G0.4 {ok_g04} G0.5 {ok_g05} "
      f"G0.6 {ok_g06}")
    flush_log()

    # --------------------------------------------- THE HEADLINE: the band by panel x cadence
    P("\n" + "=" * 178)
    P("THE HEADLINE - MA-THRESH mean resid0 (pp/yr) BY PANEL x CADENCE, and the published band")
    P("=" * 178)
    band_rows = []
    for pname in PANELS:
        for fam in FAMILIES:
            for cad in CADENCES:
                for win in ("FULL", "IS", "OOS"):
                    v = D[(D.panel == pname) & (D.family == fam) & (D.cad == cad) &
                          (D.window == win)]
                    band_rows.append(dict(
                        panel=pname, family=fam, cad=cad, window=win, n=len(v),
                        mean_resid0=v.resid0_pp.mean(), sd_resid0=v.resid0_pp.std(),
                        min_resid0=v.resid0_pp.min(), max_resid0=v.resid0_pp.max(),
                        max_abs=v.resid0_pp.abs().max(), n_neg=int((v.resid0_pp < 0).sum()),
                        mean_c_bar=v.c_bar.mean(), mean_c_sd=v.c_sd.mean(),
                        in_pub_band=in_band(v.resid0_pp.mean(), *BAND_PUB),
                        theta_in_band=int(sum(in_band(z, *BAND_PUB) for z in v.resid0_pp))))
    B = pd.DataFrame(band_rows)
    B.to_csv(f"{OUT}.band.csv", index=False)
    MAF = B[(B.family == "MA-THRESH") & (B.window == "FULL")]
    P("\nMA-THRESH, FULL sample (the band's own gate family).  in_band is against the published "
      f"{BAND_PUB}; theta_in_band counts how many of the 9 thetas sit inside.")
    P(fmt(MAF.set_index(["panel", "cad"])[["mean_resid0", "sd_resid0", "min_resid0",
                                           "max_resid0", "mean_c_bar", "mean_c_sd",
                                           "in_pub_band", "theta_in_band"]]))
    P("\nQUANTILE-M, FULL sample (the matched pure-exposure control - if IT also collapses at "
      "the extremes the effect is the decomposition's, not the MA gate's):")
    QF = B[(B.family == "QUANTILE-M") & (B.window == "FULL")]
    P(fmt(QF.set_index(["panel", "cad"])[["mean_resid0", "sd_resid0", "max_abs", "mean_c_bar",
                                          "mean_c_sd"]]))
    P("\nSEPARATION (MA - QUANTILE mean resid0, pp/yr) by panel x cadence:")
    sep = MAF.set_index(["panel", "cad"]).mean_resid0 - QF.set_index(["panel", "cad"]).mean_resid0
    P(fmt(sep.unstack().reindex(columns=CADENCES)))
    flush_log()

    # --------------------------------------------- H_DOMAIN / H_ONE_PANEL
    P("\n" + "=" * 178)
    P("H_DOMAIN  /  H_ONE_PANEL")
    P("=" * 178)
    cl1, cl2 = [], []
    for pname in PANELS:
        for cad in CADENCES:
            v = float(MAF[(MAF.panel == pname) & (MAF.cad == cad)].mean_resid0.iloc[0])
            inb = in_band(v, *BAND_PUB)
            (cl1 if cad in INTERIOR else cl2).append(
                dict(panel=pname, cad=cad, mean_resid0=v, inside=inb))
    C1, C2 = pd.DataFrame(cl1), pd.DataFrame(cl2)
    ok_c1 = bool(C1.inside.all())
    ok_c2 = bool((~C2.inside).all())
    P(f"clause (1) all 9 INTERIOR (W/M/Q) cells inside {BAND_PUB}: "
      f"{int(C1.inside.sum())}/9  {'PASS' if ok_c1 else 'FAIL'}")
    P(fmt(C1.set_index(["panel", "cad"])))
    P(f"clause (2) all 6 EXTREME (D/A) cells outside {BAND_PUB}: "
      f"{int((~C2.inside).sum())}/6  {'PASS' if ok_c2 else 'FAIL'}")
    P(fmt(C2.set_index(["panel", "cad"])))
    H_DOMAIN = ok_c1 and ok_c2
    large_ext = C2[C2.panel != "SMALL439"]
    H_ONE_PANEL = bool(large_ext.inside.any())
    P(f"\nH_DOMAIN    {'HOLDS' if H_DOMAIN else 'FAILS'}  (clause1 {ok_c1}, clause2 {ok_c2})")
    P(f"H_ONE_PANEL {'HOLDS' if H_ONE_PANEL else 'FAILS'}  (a large panel's D or A mean inside "
      f"the band: {int(large_ext.inside.sum())}/4)")

    # --------------------------------------------- the bar dial
    P("\n" + "=" * 178)
    P("THE BAR DIAL - in-band share of the 9 thetas, by cadence, at every band width "
      "(m=1.0 IS the published band).  Pooled over the 3 panels then broken out.")
    P("=" * 178)
    bar_rows = []
    for m in BAR_M:
        lo, hi = BAND_CENTRE - BAND_HALF * m, BAND_CENTRE + BAND_HALF * m
        for cad in CADENCES:
            v = F[(F.family == "MA-THRESH") & (F.cad == cad)]
            row = dict(m=m, band=f"[{lo:+.3f},{hi:+.3f}]", cad=cad,
                       pooled=float(np.mean([in_band(z, lo, hi) for z in v.resid0_pp])))
            for pname in PANELS:
                vv = v[v.panel == pname]
                row[pname] = float(np.mean([in_band(z, lo, hi) for z in vv.resid0_pp]))
                row[pname + "_mean_in"] = in_band(float(vv.resid0_pp.mean()), lo, hi)
            bar_rows.append(row)
    BAR = pd.DataFrame(bar_rows)
    P(fmt(BAR.set_index(["m", "band", "cad"]), 3))
    flush_log()

    # --------------------------------------------- THE AUDIT
    P("\n" + "=" * 178)
    P("THE AUDIT - every committed use of the band as a BAR or a PRIOR, re-scored with the "
      "band's cadence domain")
    P("=" * 178)
    CEN, ledger_hits, console_hits = census()
    P(f"census rule (pre-registered): BAR = literal -0.70/-0.20 pair inside a .py; "
      f"PRIOR = the prescription in prose.  Ledgers excluded: {sorted(set(ledger_hits))}.  "
      f"Console/artefact files matching (not scored, they are outputs of scripts already in the "
      f"census): {len(console_hits)}.")
    if CEN.empty:
        P("census EMPTY - the rule found nothing, which cannot be right; aborting the audit.")
        H_AUDIT = False
        CEN = pd.DataFrame(columns=["stem", "role", "cadences", "panels"])
    else:
        # the measured domain: the cadences at which the band actually contains the mean, on
        # every panel
        dom = sorted({c for c in CADENCES
                      if all(in_band(float(MAF[(MAF.panel == p) & (MAF.cad == c)]
                                           .mean_resid0.iloc[0]), *BAND_PUB) for p in PANELS)},
                     key=CADENCES.index)
        P(f"MEASURED DOMAIN of {BAND_PUB} (cadences where the MA mean is inside on ALL THREE "
          f"panels): {dom}")
        aud = []
        for _, r in CEN.iterrows():
            cads = [c for c in str(r.cadences).split(",") if c in CADENCES]
            unknown = len(cads) == 0
            out_of_dom = [c for c in cads if c not in dom]
            # pooled reading (as published) vs per-cadence reading, on this use's own cadences
            if cads:
                v = F[(F.family == "MA-THRESH") & (F.cad.isin(cads))]
                pooled = float(v.resid0_pp.mean())
                pooled_pass = in_band(pooled, *BAND_PUB)
                per = {c: float(F[(F.family == "MA-THRESH") & (F.cad == c)].resid0_pp.mean())
                       for c in cads}
                per_pass = all(in_band(x, *BAND_PUB) for x in per.values())
            else:
                pooled, pooled_pass, per, per_pass = np.nan, None, {}, None
            flip_i = bool(out_of_dom) or unknown
            flip_ii = bool(pooled_pass is not None and pooled_pass != per_pass)
            aud.append(dict(stem=r.stem, role=r.role, cadences=r.cadences, panels=r.panels,
                            states_domain=bool(r.states_domain),
                            pooled_resid0=pooled, pooled_pass=pooled_pass,
                            per_cadence_pass=per_pass,
                            out_of_domain=",".join(out_of_dom) if out_of_dom else "-",
                            flip_out_of_domain=flip_i, flip_reading=flip_ii,
                            FLIPS=bool(flip_i or flip_ii)))
        A = pd.DataFrame(aud)
        A.to_csv(f"{OUT}.census.csv", index=False)
        P(fmt(A.drop(columns=["panels"]).set_index(["stem"])))
        P(f"\nuses found: {len(A)}  ({int((A.role == 'BAR').sum())} BAR, "
          f"{int((A.role == 'PRIOR').sum())} PRIOR)")
        P(f"flips: {int(A.FLIPS.sum())} of {len(A)}  "
          f"(out-of-domain {int(A.flip_out_of_domain.sum())}, "
          f"pooled-vs-per-cadence reading {int(A.flip_reading.sum())})")
        P(f"  of which already state the cadence restriction in their own committed result "
          f"(self-corrected, not an outstanding erratum): "
          f"{int((A.FLIPS & A.states_domain).sum())}; "
          f"UNCORRECTED flips: {int((A.FLIPS & ~A.states_domain).sum())}")
        H_AUDIT = bool(A.FLIPS.sum() == 0)
    P(f"H_AUDIT {'HOLDS' if H_AUDIT else 'FAILS'}")
    flush_log()

    # --------------------------------------------- rule 8 walk-forward
    P("\n" + "=" * 178)
    P("RULE 8 WALK-FORWARD")
    P("=" * 178)
    wf = []
    P("\nWF-A  (theta, cadence) chosen on IS Sharpe within panel x family x construction; "
      "OOS read once.")
    for pname in PANELS:
        px, spy_px = PX[pname]
        start = px.index[260]
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.loc[start:])
        ctrl_o = {}
        for cad in CADENCES:
            ctrl_o[cad] = stat(bt(px, control_book(px), cost_bps=COST_BPS,
                                  cad=cad)["returns"].loc[start:])
        for fam in FAMILIES:
            for con in CONSTRUCTIONS:
                sub = G[(G.panel == pname) & (G.family == fam) & (G.con == con)]
                pick = sub.loc[sub.isSharpe.idxmax()]
                wf.append(dict(test="WF-A", panel=pname, family=fam, con=con,
                               pick=f"theta={pick.theta:+.2f},cad={pick.cad}",
                               oCAGR=pick.oCAGR, oSharpe=pick.oSharpe, oMaxDD=pick.oMaxDD,
                               spy_oSharpe=spy_s["oSharpe"], live_oSharpe=live_s["oSharpe"],
                               ctrl_oSharpe=ctrl_o[pick.cad]["oSharpe"],
                               beats_spy=bool(pick.oSharpe > spy_s["oSharpe"]),
                               beats_live=bool(pick.oSharpe > live_s["oSharpe"]),
                               beats_ctrl=bool(pick.oSharpe > ctrl_o[pick.cad]["oSharpe"])))
    WFA = pd.DataFrame([w for w in wf if w["test"] == "WF-A"])
    P(fmt(WFA.drop(columns=["test"]).set_index(["panel", "family", "con"])))
    P(f"WF-A: beats SPY {int(WFA.beats_spy.sum())}/{len(WFA)}, "
      f"beats LIVE v2 {int(WFA.beats_live.sum())}/{len(WFA)}, "
      f"beats its own no-gate control {int(WFA.beats_ctrl.sum())}/{len(WFA)}")

    P("\nWF-B  the band as an OOS predictor.  UNQUALIFIED = one IS band for the whole dial; "
      "QUALIFIED = one IS band per cadence; ZERO carried as the third predictor.")
    IS_ = D[(D.window == "IS") & (D.family == "MA-THRESH")]
    OO_ = D[(D.window == "OOS") & (D.family == "MA-THRESH")]
    u_mu, u_sd = IS_.resid0_pp.mean(), IS_.resid0_pp.std()
    u_lo, u_hi = u_mu - 2 * u_sd, u_mu + 2 * u_sd
    P(f"  UNQUALIFIED IS band = [{u_lo:+.4f}, {u_hi:+.4f}] (IS mean {u_mu:+.4f} +/- 2 sd "
      f"{u_sd:.4f}) over {len(IS_)} IS cells")
    wfb = []
    for cad in CADENCES:
        i = IS_[IS_.cad == cad].resid0_pp
        o = OO_[OO_.cad == cad].resid0_pp
        q_mu, q_sd = i.mean(), i.std()
        q_lo, q_hi = q_mu - 2 * q_sd, q_mu + 2 * q_sd
        wfb.append(dict(cad=cad, n_oos=len(o),
                        IS_mean=q_mu, qual_band=f"[{q_lo:+.3f},{q_hi:+.3f}]",
                        cov_unqual=float(np.mean([in_band(z, u_lo, u_hi) for z in o])),
                        cov_qual=float(np.mean([in_band(z, q_lo, q_hi) for z in o])),
                        cov_pub=float(np.mean([in_band(z, *BAND_PUB) for z in o])),
                        MAE_unqual=float((o - u_mu).abs().mean()),
                        MAE_qual=float((o - q_mu).abs().mean()),
                        MAE_pub=float((o - BAND_CENTRE).abs().mean()),
                        MAE_zero=float(o.abs().mean())))
    WFB = pd.DataFrame(wfb)
    P(fmt(WFB.set_index("cad")))
    q_wins = int((WFB.MAE_qual < WFB.MAE_unqual).sum())
    z_wins = int((WFB.MAE_zero < WFB.MAE_qual).sum())
    P(f"  QUALIFIED centre beats UNQUALIFIED centre on OOS MAE in {q_wins}/5 cadences; "
      f"a hard ZERO beats the QUALIFIED centre in {z_wins}/5.")

    P("\nWF-C  H_DOMAIN's two clauses re-read on the IS window alone and the OOS window alone.")
    wfc = []
    for win in ("IS", "OOS"):
        sub = B[(B.family == "MA-THRESH") & (B.window == win)]
        c1 = sum(bool(sub[(sub.panel == p) & (sub.cad == c)].in_pub_band.iloc[0])
                 for p in PANELS for c in INTERIOR)
        c2 = sum(not bool(sub[(sub.panel == p) & (sub.cad == c)].in_pub_band.iloc[0])
                 for p in PANELS for c in EXTREMES)
        wfc.append(dict(window=win, interior_inside=f"{c1}/9", extreme_outside=f"{c2}/6",
                        H_DOMAIN=bool(c1 == 9 and c2 == 6)))
    WFC = pd.DataFrame(wfc)
    P(fmt(WFC.set_index("window")))
    pd.concat([WFA, WFB.assign(test="WF-B"), WFC.assign(test="WF-C")],
              ignore_index=True).to_csv(f"{OUT}.walkforward.csv", index=False)
    flush_log()

    # --------------------------------------------- KEEP paths
    P("\n" + "=" * 178)
    P("BOTH KEEP PATHS over all 540 books")
    P("=" * 178)
    G["pass4b"] = G.f4b == "-"
    P(f"4a (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse): {int(G.p4a.sum())}/{len(G)}")
    P(f"4b (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
      f"{int(G.pass4b.sum())}/{len(G)}")
    P(f"BOTH: {int((G.p4a & G.pass4b).sum())}/{len(G)}")
    P("\nby panel:")
    P(fmt(G.groupby("panel")[["p4a", "pass4b"]].sum().astype(int), 0))
    P("\nby cadence:")
    P(fmt(G.groupby("cad")[["p4a", "pass4b"]].sum().astype(int).reindex(CADENCES), 0))
    fails = pd.Series([t for s in G.f4b for t in s.split(",") if t != "-"]).value_counts()
    P("\n4b failing legs (a book can fail several):")
    P(fails.to_string())
    if int(G.pass4b.sum()):
        P("\n4b passers:")
        P(fmt(G[G.pass4b][["panel", "family", "con", "theta", "cad", "CAGR", "Sharpe", "MaxDD",
                           "H1", "H2", "oSharpe"]].set_index(["panel", "family", "con"])))
    if int(G.p4a.sum()):
        P("\n4a passers:")
        P(fmt(G[G.p4a][["panel", "family", "con", "theta", "cad", "CAGR", "Sharpe", "MaxDD",
                        "H1", "H2", "oSharpe"]].set_index(["panel", "family", "con"])))

    # --------------------------------------------- summary
    P("\n" + "=" * 178)
    P("SUMMARY")
    P("=" * 178)
    for pname in PANELS:
        P(f"MA-THRESH mean resid0 (FULL, pp/yr) {pname:9s}: " +
          ", ".join(f"{c}={float(MAF[(MAF.panel == pname) & (MAF.cad == c)].mean_resid0.iloc[0]):+.4f}"
                    for c in CADENCES))
    for pname in PANELS:
        P(f"QUANTILE-M mean resid0 (FULL, pp/yr) {pname:9s}: " +
          ", ".join(f"{c}={float(QF[(QF.panel == pname) & (QF.cad == c)].mean_resid0.iloc[0]):+.4f}"
                    for c in CADENCES))
    P(f"H_DOMAIN {'HOLDS' if H_DOMAIN else 'FAILS'} | H_ONE_PANEL "
      f"{'HOLDS' if H_ONE_PANEL else 'FAILS'} | H_AUDIT {'HOLDS' if H_AUDIT else 'FAILS'}")
    P(f"gates: G0.1 {ok_g01} G0.2 {ok_g02} G0.3 {ok_g03} G0.4 {ok_g04} G0.5 {ok_g05} "
      f"G0.6 {ok_g06}")
    P(f"KEEP: 4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.pass4b.sum())}/{len(G)}, "
      f"BOTH {int((G.p4a & G.pass4b).sum())}/{len(G)}")
    P("SURVIVORSHIP: current constituents on SMALL439 and B136; CAGR levels and the 4a/4b "
      "columns are inflated; the resid0 contrasts are arm-minus-arm on the same names and days.")
    flush_log()


if __name__ == "__main__":
    main()
