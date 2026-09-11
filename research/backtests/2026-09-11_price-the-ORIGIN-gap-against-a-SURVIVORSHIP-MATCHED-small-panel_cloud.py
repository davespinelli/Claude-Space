#!/usr/bin/env python3
"""Idea 782 (cloud, 2026-09-11) - price-the-ORIGIN-gap-against-a-SURVIVORSHIP-MATCHED-small-panel.

QUESTION
--------
Idea 570 (cloud, 2026-09-11) replaced idea 568's Gaussian kernel with an EXACT one-to-one
name-level match on the characteristic and found the B136-vs-SMALL439 MA-gate selection
premium gap SURVIVES: +0.1649 to +0.3021 (t +7.57 to +48.64), inside its own seed sd on 0 of
18 points, at 1.69x-3.09x the published U56-SMALL439 gap, holding sign IS vs OOS 18 of 18.
It closed by naming the one channel its design could NOT control:

    "the design controls the characteristic but NOT differential survivorship - SMALL439 is a
     current-constituent screen carrying more survivorship premium than B136, which would
     produce exactly this sign; that is the first thing a KEEP would have to answer."

This run answers it as far as the committed data allow: it matches on LISTING HISTORY as well
as the characteristic, and re-reads the gap.

WHY LISTING HISTORY IS THE RIGHT OBSERVABLE PROXY, AND WHAT IT DOES NOT BUY
--------------------------------------------------------------------------
Both panels are current-constituent screens, so the names that DIED are missing from both and
no committed artefact can restore them.  What IS observable, and what differs enormously
between the panels, is how much of the window each name was listed for:

    B136  : 123 of 134 names carry a first bar on the pool's opening day, 2010-01-04 (91.8%)
    SMALL : 239 of 439 (54.4%); 192 small names list after 2010, 52 of them after 2020.

A name that IPOs mid-window and is still in a current-constituent screen today has, by
construction, survived from its listing to today - it is a pure post-selection sample over a
SHORTER window, and the shorter the window the stronger the conditioning.  So the small panel
is not merely "more survivorship-exposed"; it is differentially exposed THROUGH a variable
this run can measure and match on.  Matching first-bar date equalises that channel.

STATED PLAINLY, BEFORE ANY NUMBER IS READ: this removes the LISTING-WINDOW component of the
differential survivorship channel.  It cannot remove the component carried by names delisted
before 2026-09-04, because neither panel contains any.  A gap that survives a first-bar match
is therefore NOT proven free of survivorship - it is proven free of the only part of it the
record can see.  That limitation is restated beside every headline.

DESIGN
------
Pool  = idea 570's pooled frame verbatim (134 B136 + 439 SMALL tradables with a defined
        characteristic = 573 names, common index 2010-01-04 .. 2026-09-04, 4194 bars).
Match = idea 570's greedy one-to-one nearest-neighbour pairing at FIXED characteristic
        tolerance tau = 0.02 (its tight rung, where H_EXACT held), with ONE constraint added:
        a B name may only take an S partner whose FIRST BAR in the pool is within h calendar
        days of its own.  The B visiting order is idea 570's permutation for (char, tau, k,
        seed), unchanged - the history filter restricts the eligible partners, it does not
        reseed the draw.  At h = inf the algorithm is therefore BYTE-IDENTICAL to idea 570's
        tau=0.02 arm, which gate G5 exploits as an exact reproduction.
Arms  (idea 51 / 312 / 568 / 570 verbatim): EWall = gross g over every priced tradable name
        (CONTROL); MA-RS = gross g respread over names above their 200d MA (TREATMENT);
        premium = Sharpe(MA-RS) - Sharpe(EWall) at the SAME (panel, g, cadence).  RESPREAD
        holds gross fixed, so the premium is pure selection with no exposure dial.
GAP   = premium(B panel) - premium(S panel), per seed; headline = mean over seeds, with
        sd_pair = sqrt((sd_B^2 + sd_S^2)/2), the SAME statistic ideas 568 and 570 published.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. HISTORY BUCKET h in {0, 90, 365, inf} calendar days of first-bar difference
       (h = 0 means the pair's first bars are the SAME day)
    2. k in {12, 24, 34} pairs -- the ladder is capped by the FEASIBILITY CENSUS printed before
       any premium is read (at tau = 0.02 the tightest cell, breadth at h = 0, supplies at most
       35 pairs), NOT by any result.  Idea 570's k = 36 / 72 rungs are unreachable here and are
       reported as such.
All 4 x 3 = 12 grid points are reported, for BOTH characteristics.
REPORTED (never selected) axes: characteristic {cvol, breadth}, gross {0.50, 0.75, 1.00},
    cadence {W, M}, seed (12), period (FULL / IS / OOS).  tau is FIXED at 0.02, not tuned.

PRE-REGISTERED HYPOTHESES (written before any history-matched premium was read)
------------------------------------------------------------------------------
GAP_PUB  = 0.0978   (idea 51's published U56 - SMALL439 premium gap)
G570_MIN = 0.1649   (idea 570's smallest exactly-matched origin gap over its 18 points)
G570_MAX = 0.3021   (its largest)
H_FEAS  : at h = 0 there are still k feasible pairs for every seed at every k.  This is the
          run's premise; if it fails at some k, that k is reported INFEASIBLE, not dropped,
          and no conclusion is drawn from it.
H_SURV  : the origin gap IS the listing-history (differential survivorship) channel.
          Falsified unless the gap at h = 0 falls inside its own seed sd (|gap| <= sd_pair).
H_HMONO : if listing history carries the gap, |gap| shrinks monotonically as h tightens
          (inf -> 365 -> 90 -> 0).  A flat or non-monotone ladder says it is not the carrier.
H_DIR   : survivorship is the alternative explanation for the SIGN (S more exposed => S
          premium inflated => B-S gap understated, or S depressed => gap overstated).  The
          direction the gap moves when the channel is closed is reported either way; a gap
          that GROWS at h = 0 rules survivorship out as its source, not merely in.

GATES (pre-registered, run and printed before any new number is read)
    G1 kernel repro  : idea 568's committed `.origin.csv` rows rebuilt from its own seeding
       scheme and price source, all rows x 7 columns.                           bar 1e-9
    G2 real panels   : the three real panels' premia re-derived from prices and compared to
       idea 312's committed REAL grid.       bar 1e-9 (1e-4 on U56, which carries idea 312's
       documented data/prices.csv adjusted-close revision)
    G3 identity      : fast_backtest vs engine.backtest on one book per real panel.  bar 1e-12
    G4 pool          : the pooled frame reproduces idea 570's counts and window exactly
       (573 names = B 134 + SMALL 439, 2010-01-04 .. 2026-09-04, 4194 bars).       exact
    G5 h=inf == 570  : a HISTORY-BLIND arm run at idea 570's OWN k rungs (18, 36 - its 72 rung
       is infeasible at tau=0.02 in its run and in this one) reproduces its committed
       `.origin.csv` tau=0.02 rows (prem_B, prem_S, gap, sd_pair, residual, name_residual) on
       all 4 (char, k) points.                                                   bar 1e-12
    G6 history data  : the first-bar dates this run matches on are the same object as
       data/small_meta.csv's `first_date` column for every small name whose listing starts
       inside the pooled window.                                                   exact

RULE 8 WALK-FORWARD (required, run whatever the match says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: re-read the history-matched origin gap on IS-only and OOS-only
       returns at every one of the 12 points and report whether it holds sign and magnitude.
    WF-B on a BOOK: the contrast is a DECISION RULE - "trade the B-sourced panel rather than
       the S-sourced one at matched characteristic AND matched listing history".  Pick
       (characteristic, h, k) by IS Sharpe of the seed-pooled B-side MA-RS book at g=0.75/W,
       read OOS ONCE against RULES v2 on U56 and SPY; the S-side twin, an ORIGIN-BLIND control
       (the matched pair's names pooled) and the INCUMBENT whole-B136 MA-RS gate are reported
       beside it.
    KEEP paths 4a and 4b are evaluated for EVERY book.  Stated up front: a matched draw is a
       diagnostic panel, NOT a rule anyone can trade, so a 4b pass here is a diagnostic and
       never a capital candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents.  The small
    panel additionally drops every ticker with max_1d_move >= 1.0 (439 of 483 kept).  See the
    section above for exactly which part of the channel this run closes and which it cannot.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and committed artefacts of
ideas 312, 568 and 570; modifies nothing but its own outputs:
    .grid.csv .match.csv .origin.csv .walkforward.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PARENT_END = "2026-09-04"
CHARS = ["cvol", "breadth"]
TAU = 0.02                       # FIXED at idea 570's tight rung; NOT a tuned parameter here
HISTS = [0, 90, 365, np.inf]     # TUNED 1: calendar days of first-bar difference allowed
# TUNED 2.  Idea 570's ladder was {18, 36, 72}; at tau = 0.02 with the history constraint the
# pool cannot supply 36 pairs in every cell (the FEASIBILITY CENSUS below, printed before any
# premium is read, measures the ceiling: breadth at h = 0 tops out at 35 pairs).  The ladder
# is therefore capped at 34 by FEASIBILITY, not by any result.
KS = [12, 24, 34]
SEEDS = list(range(12))

# committed constants of the parent line
K568 = 36
SEEDS568 = [0, 1, 2, 3, 4, 5]
BW_MULT = 0.5
GAP_PUB = 0.0978
G570_MIN, G570_MAX = 0.1649, 0.3021
P568 = OUT / "2026-09-09_can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT_C"
P570 = OUT / "2026-09-11_is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect_cloud"
P312 = OUT / "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.grid.csv"
TOL, TOL_U56, EXACT_BAR, IDENT = 1e-9, 1e-4, 0.01, 1e-12

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G3).  Idea 312/568/570's runner."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels
def small_tradables(pxs):
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return [c for c in pxs.columns if c != "SPY" and c not in bad]


def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    s_stk = small_tradables(pxs)
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


def name_chars(pool):
    """idea 568/570's per-NAME characteristic, verbatim: annualised vol and MA breadth."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    on = above_ma(pool) & pool.notna()
    br = (on.sum() / pool.notna().sum().replace(0, np.nan)).astype(float)
    return pd.DataFrame(dict(cvol=vol, breadth=br)).dropna()


def panel_char_568(pxd, tradable, char):
    """idea 568's panel_chars (the `achieved` estimator), restricted to the two chars used."""
    cols = [c for c in pxd.columns if c in tradable]
    if char == "cvol":
        return float((pxd[cols].pct_change().std() * np.sqrt(252)).mean())
    on = above_ma(pxd[cols]) & pxd[cols].notna()
    return float(on.sum(axis=1).div(pxd[cols].notna().sum(axis=1).replace(0, np.nan)).mean())


# ------------------------------------------------------------------------- matching
def greedy_match(nc, bnames, snames, char, k, seed, first, hist_days, tau=TAU):
    """Idea 570's greedy one-to-one match, with a LISTING-HISTORY constraint added.

    The B visiting order is idea 570's permutation for (char, tau, k, seed) - UNCHANGED, so
    at hist_days = inf this function is byte-identical to idea 570's greedy_match at tau=0.02
    (gate G5).  Each B name takes its nearest UNUSED S partner on `char` subject to BOTH
    |x_b - x_s| <= tau and |first_b - first_s| <= hist_days calendar days."""
    rng = np.random.default_rng(zlib.crc32(f"MATCH|{char}|{tau}|{k}|{seed}".encode()) % (2 ** 32))
    xb = nc.loc[sorted(bnames), char]
    xs = nc.loc[sorted(snames), char].sort_values()
    s_names = xs.index.to_numpy()
    s_vals = xs.to_numpy(float)
    s_first = first.reindex(s_names).to_numpy("datetime64[ns]")
    used = np.zeros(len(s_vals), bool)
    order = rng.permutation(xb.index.to_numpy())
    pairs = []
    for b in order:
        if len(pairs) >= k:
            break
        v = float(xb.loc[b])
        d = np.abs(s_vals - v)
        d[used] = np.inf
        if np.isfinite(hist_days):
            fb = np.datetime64(first.loc[b], "ns")
            dd = np.abs((s_first - fb) / np.timedelta64(1, "D"))
            d = np.where(dd <= hist_days, d, np.inf)
        j = int(np.argmin(d))
        if not np.isfinite(d[j]) or d[j] > tau:
            continue
        used[j] = True
        pairs.append((b, str(s_names[j]), float(v), float(s_vals[j]), float(d[j]),
                      pd.Timestamp(first.loc[b]), pd.Timestamp(first.loc[s_names[j]])))
    return pairs


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 108)
    P("IDEA 782  price-the-ORIGIN-gap-against-a-SURVIVORSHIP-MATCHED-small-panel  (cloud, 2026-09-11)")
    P("=" * 108)
    P(f"PROTOCOL: {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START} read once.")
    P(f"TUNED (2): HISTORY BUCKET h in {HISTS} days x k in {KS} -- all 12 points reported.")
    P(f"FIXED (not tuned): characteristic tolerance tau = {TAU} (idea 570's tight rung).")
    P(f"Pre-registered: GAP_PUB {GAP_PUB:.4f}; idea 570's exact-match gap band "
      f"[{G570_MIN:+.4f}, {G570_MAX:+.4f}].")
    P("")

    # ---------------------------------------------------------------- gates
    P("=" * 108)
    P("GATES (pre-registered; printed before any history-matched number is read)")
    P("=" * 108)
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    real_rows = []
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                res = {a: fast_backtest(px, w, COST, freq) for a, w in books.items()}
                rets = {a: v["returns"].loc[st:] for a, v in res.items()}
                mc = metrics(rets["EWall"])
                for a in books:
                    row = dict(panel=nm, kind="REAL", arm=a, gross=g, cadence=freq)
                    row.update(rowify(rets[a], res[a]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    real_rows.append(row)
    REAL = pd.DataFrame(real_rows)
    par = pd.read_csv(P312)
    par = par[(par.kind == "REAL") & par.arm.isin(["EWall", "MA-RS"])].copy()
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "turnover", "dCAGR_vs_EWall", "dSharpe_vs_EWall"]
    m = REAL.merge(par, on=["panel", "arm", "gross", "cadence"], suffixes=("", "_p"))
    perp = m.assign(d=np.abs(m[cmpcols].values - m[[c + "_p" for c in cmpcols]].values).max(1)) \
            .groupby("panel").d.max()
    g2ok = all(float(perp[p]) < (TOL_U56 if p == "U56" else TOL) for p in perp.index)
    P(f"G2 real panels  : {len(m)} of 36 REAL rows vs idea 312's committed grid; per panel "
      + "  ".join(f"{k} {v:.2e}" for k, v in perp.items())
      + f" -> {'PASS' if g2ok else 'FAIL'}  (U56 bar {TOL_U56:.0e}: documented prices.csv revision)")
    pub = REAL[REAL.arm == "MA-RS"].groupby("panel").dSharpe_vs_EWall.mean()
    P("                  published premium re-read: "
      + "  ".join(f"{k} {v:+.4f}" for k, v in pub.items())
      + f"   U56-{SMALLK} gap {float(pub['U56']-pub[SMALLK]):+.4f} (pre-reg {GAP_PUB:.4f})")

    g3 = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        g3 = max(g3, float((fast_backtest(px, w, COST, "W")["returns"]
                            - backtest(px, w, cost_bps=COST, freq="W")["returns"]).abs().max()))
    P(f"G3 identity     : fast_backtest vs engine.backtest max |dret| = {g3:.3e} (bar 1e-12) -> "
      f"{'PASS' if g3 < IDENT else 'FAIL'}")

    # pooled frame (idea 568/570's, verbatim)
    pxB, trB = panels["B136"]
    pxS, trS = panels[SMALLK]
    ix = pxB.index.intersection(pxS.index)
    bn = sorted([c for c in pxB.columns if c in trB and c != "SPY"])
    sn = sorted([c for c in pxS.columns if c in trS])
    pool = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1).ffill()
    spy_pool = pxB.loc[ix, "SPY"]
    nc = name_chars(pool)
    bnames = sorted(set(bn) & set(nc.index))
    snames = sorted(set(sn) & set(nc.index))
    g4 = (len(nc) == 573 and len(bnames) == 134 and len(snames) == 439
          and str(ix.min().date()) == "2010-01-04" and str(ix.max().date()) == "2026-09-04"
          and len(ix) == 4194)
    P(f"G4 pool         : {ix.min().date()}..{ix.max().date()} ({len(ix)} bars), B {len(bnames)} "
      f"+ SMALL {len(snames)} = {len(nc)} names -> {'PASS' if g4 else 'FAIL'} (idea 570's "
      f"committed G4: 573 = 134 + 439, 4194 bars)")

    # ---- listing history, the object this run matches on
    raw = pd.concat([pxB.loc[ix, bn], pxS.loc[ix, sn]], axis=1)      # PRE-ffill: true first bar
    first = raw.apply(lambda s: s.first_valid_index())
    first = first.reindex(sorted(bnames) + sorted(snames))
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    meta = meta.set_index("ticker").first_date.astype("datetime64[ns]")
    chk = pd.DataFrame({"run": first.reindex(snames), "meta": meta.reindex(snames)}).dropna()
    inside = chk[chk.meta > ix.min()]                 # names listing INSIDE the pooled window
    g6d = int((inside.run != inside.meta).sum())
    P(f"G6 history data : {len(inside)} small names list inside the pooled window; first bar as "
      f"computed here vs data/small_meta.csv `first_date`: {g6d} mismatches -> "
      f"{'PASS' if g6d == 0 else 'FAIL'}  (the {len(chk)-len(inside)} names dated at or before "
      f"{ix.min().date()} are censored by the pooled window and excluded from the check)")
    bfull = int((first.reindex(bnames) == ix.min()).sum())
    sfull = int((first.reindex(snames) == ix.min()).sum())
    P(f"                  FULL-HISTORY SHARE, the asymmetry this run closes: B {bfull}/"
      f"{len(bnames)} = {bfull/len(bnames):.1%}   SMALL {sfull}/{len(snames)} = "
      f"{sfull/len(snames):.1%}")
    hb = first.reindex(bnames).dt.year.value_counts().sort_index()
    hs = first.reindex(snames).dt.year.value_counts().sort_index()
    P("                  B  first-bar years: " + ", ".join(f"{int(y)}:{int(c)}" for y, c in hb.items()))
    P("                  S  first-bar years: " + ", ".join(f"{int(y)}:{int(c)}" for y, c in hs.items()))

    def frame_of(names):
        cols = list(dict.fromkeys(list(names) + ["SPY"]))
        return pd.concat([pool[list(names)], spy_pool.rename("SPY")], axis=1)[cols] \
            .dropna(how="all").ffill()

    def achieved_of(names, char):
        return panel_char_568(frame_of(names), set(names), char)

    def premium_of(names, period="FULL"):
        """idea 568's premium: mean over (gross, cadence) of Sharpe(MA-RS) - Sharpe(EWall)."""
        pxd = frame_of(names)
        tr = set(names)
        st = pxd.index[260]
        out = []
        for g in GROSS:
            books = make_books(pxd, tr, g)
            for freq in CADENCE:
                rr = {a: fast_backtest(pxd, w, COST, freq)["returns"].loc[st:]
                      for a, w in books.items()}
                if period == "IS":
                    rr = {a: r.loc[:IS_END] for a, r in rr.items()}
                elif period == "OOS":
                    rr = {a: r.loc[OOS_START:] for a, r in rr.items()}
                out.append(metrics(rr["MA-RS"])["Sharpe"] - metrics(rr["EWall"])["Sharpe"])
        return float(np.mean(out))

    # ---- G1: rebuild idea 568's KERNEL origin rows from its own scheme
    def kernel_draw(char, L, flavour, sd):
        names = np.array({"BONLY": bnames, "SONLY": snames,
                          "POOL": sorted(nc.index)}[flavour])
        x = nc.loc[names, char].to_numpy(float)
        h = BW_MULT * float(nc[char].std())
        rng = np.random.default_rng(
            zlib.crc32(f"CHAR|{char}|{L:.3f}|{flavour}|{sd}".encode()) % (2 ** 32))
        w = np.exp(-0.5 * ((x - L) / h) ** 2)
        w = w / w.sum()
        return sorted(rng.choice(names, size=K568, replace=False, p=w).tolist())

    or_old = pd.read_csv(f"{P568}.origin.csv")
    g1rows = []
    for _, r in or_old.iterrows():
        pb = [kernel_draw(r["char"], r["level"], "BONLY", s) for s in SEEDS568]
        ps = [kernel_draw(r["char"], r["level"], "SONLY", s) for s in SEEDS568]
        ab = float(np.mean([achieved_of(p, r["char"]) for p in pb]))
        as_ = float(np.mean([achieved_of(p, r["char"]) for p in ps]))
        vb = [premium_of(p) for p in pb]
        vs = [premium_of(p) for p in ps]
        sdp = float(np.sqrt((np.std(vb, ddof=1) ** 2 + np.std(vs, ddof=1) ** 2) / 2))
        gp = float(np.mean(vb) - np.mean(vs))
        g1rows.append(dict(char=r["char"], level=r["level"], achieved_B=ab, achieved_S=as_,
                           prem_B=float(np.mean(vb)), prem_S=float(np.mean(vs)), gap=gp,
                           sd_pair=sdp, t=gp / (sdp / np.sqrt(len(SEEDS568)))))
    g1 = pd.DataFrame(g1rows)
    mm = g1.merge(or_old, on=["char", "level"], suffixes=("_r", "_c"))
    c1 = ["achieved_B", "achieved_S", "prem_B", "prem_S", "gap", "sd_pair", "t"]
    g1d = max(float(np.abs(mm[c + "_r"] - mm[c + "_c"]).max()) for c in c1)
    P(f"G1 kernel repro : idea 568's committed .origin.csv rebuilt here from its own seeding "
      f"scheme, all {len(mm)} rows x {len(c1)} columns, max |d| = {g1d:.3e} (bar {TOL:.0e}) -> "
      f"{'PASS' if g1d < TOL else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- the matched grid
    P("=" * 108)
    P("THE HISTORY-MATCHED ONE-TO-ONE MATCH (tau = 0.02 on the characteristic AND |dfirst| <= h)")
    P("=" * 108)

    def run_point(ch, h, k, sd):
        pr = greedy_match(nc, bnames, snames, ch, k, sd, first, h)
        if len(pr) < k:
            return dict(char=ch, hbucket=h, k=k, seed=sd, n_pairs=len(pr), feasible=False), []
        B = [p[0] for p in pr]
        S = [p[1] for p in pr]
        nb = float(np.mean([p[2] for p in pr]))
        ns = float(np.mean([p[3] for p in pr]))
        ab, as_ = achieved_of(B, ch), achieved_of(S, ch)
        hd = np.array([abs((p[5] - p[6]).days) for p in pr], float)
        agb = np.array([(ix.max() - p[5]).days for p in pr], float) / 365.25
        ags = np.array([(ix.max() - p[6]).days for p in pr], float) / 365.25
        row = dict(char=ch, hbucket=h, k=k, seed=sd, n_pairs=len(pr), feasible=True,
                   achieved_B=ab, achieved_S=as_, residual=abs(ab - as_),
                   name_B=nb, name_S=ns, name_residual=abs(nb - ns),
                   max_pair_d=float(np.max([p[4] for p in pr])),
                   hist_B_yrs=float(agb.mean()), hist_S_yrs=float(ags.mean()),
                   hist_residual_yrs=float(abs(agb.mean() - ags.mean())),
                   max_hist_gap_days=float(hd.max()))
        gr_out = []
        for side, names in (("B", B), ("S", S)):
            pxd = frame_of(names)
            tr = set(names)
            st = pxd.index[260]
            spy = pxd["SPY"].pct_change().fillna(0.0).loc[st:]
            v2 = fast_backtest(pxd, rules_v2_weights(pxd), COST, "W")["returns"].loc[st:]
            pf, pi, po = [], [], []
            for g in GROSS:
                books = make_books(pxd, tr, g)
                for freq in CADENCE:
                    res = {a: fast_backtest(pxd, w, COST, freq) for a, w in books.items()}
                    rr = {a: v["returns"].loc[st:] for a, v in res.items()}
                    pf.append(metrics(rr["MA-RS"])["Sharpe"] - metrics(rr["EWall"])["Sharpe"])
                    pi.append(metrics(rr["MA-RS"].loc[:IS_END])["Sharpe"]
                              - metrics(rr["EWall"].loc[:IS_END])["Sharpe"])
                    po.append(metrics(rr["MA-RS"].loc[OOS_START:])["Sharpe"]
                              - metrics(rr["EWall"].loc[OOS_START:])["Sharpe"])
                    for a in books:
                        r = rr[a]
                        gd = dict(char=ch, hbucket=h, k=k, seed=sd, side=side, arm=a,
                                  gross=g, cadence=freq)
                        gd.update(rowify(r, res[a]["turnover"].loc[st:]))
                        gd["keep4a"] = keep_4a(r, v2)
                        gd["fail4b"] = fail_4b(r, spy)
                        gd["keep4b"] = gd["fail4b"] == "-"
                        gr_out.append(gd)
            row[f"prem_{side}"] = float(np.mean(pf))
            row[f"premIS_{side}"] = float(np.mean(pi))
            row[f"premOOS_{side}"] = float(np.mean(po))
            row[f"names_{side}"] = ",".join(names)
        return row, gr_out

    P("FEASIBILITY CENSUS (run BEFORE any premium is read; it is what caps the k ladder)")
    P("  max one-to-one pairs available per seed at tau = 0.02, over the 12 seeds:")
    feas_rows = []
    for ch in CHARS:
        for h in HISTS:
            mx = [len(greedy_match(nc, bnames, snames, ch, 10 ** 6, sd, first, h))
                  for sd in SEEDS]
            feas_rows.append(dict(char=ch, hbucket=h, min_pairs=int(np.min(mx)),
                                  med_pairs=int(np.median(mx)), max_pairs=int(np.max(mx))))
    FEAS = pd.DataFrame(feas_rows)
    P(fmt(FEAS.set_index(["char", "hbucket"]), 0))
    cap = int(FEAS.min_pairs.min())
    P(f"  binding cell supplies {cap} pairs -> k ladder {KS} (all rungs feasible in every cell); "
      f"idea 570's k=36 rung is reachable only history-blind and its k=72 rung is infeasible at "
      f"tau=0.02 in ITS run too (its committed .origin.csv carries no tau=0.02 k=72 row).")
    P("")

    mrows, grows = [], []
    for ch in CHARS:
        for h in HISTS:
            for k in KS:
                for sd in SEEDS:
                    row, gr = run_point(ch, h, k, sd)
                    mrows.append(row)
                    grows.extend(gr)
        P(f"  {ch}: {len(HISTS)} h x {len(KS)} k x {len(SEEDS)} seeds matched "
          f"({time.time()-t0:.0f}s)")
    M = pd.DataFrame(mrows)
    G = pd.DataFrame(grows)
    P("")

    # ---------------------------------------------------------------- match quality
    P("=" * 108)
    P("MATCH QUALITY - characteristic residual AND listing-history residual at every point")
    P("=" * 108)
    ok = M[M.feasible]
    mq = ok.groupby(["char", "hbucket", "k"]).agg(
        seeds=("seed", "size"), residual=("residual", "mean"),
        name_residual=("name_residual", "mean"),
        histB=("hist_B_yrs", "mean"), histS=("hist_S_yrs", "mean"),
        hist_resid_yrs=("hist_residual_yrs", "mean"),
        max_hist_gap_d=("max_hist_gap_days", "mean")).reset_index()
    P(fmt(mq.set_index(["char", "hbucket", "k"]), 5))
    infeas = M[~M.feasible]
    if len(infeas):
        P("  INFEASIBLE points (fewer than k pairs available) - reported, never dropped:")
        for (ch, h, k), grp in infeas.groupby(["char", "hbucket", "k"]):
            P(f"    {ch:8s} h {h:<6} k {k:3d}: {len(grp)} of {len(SEEDS)} seeds short "
              f"(max pairs found {int(grp.n_pairs.max())})")
    else:
        P("  INFEASIBLE points: none - every (char, h, k, seed) found its k pairs.")
    h0 = mq[mq["hbucket"] == 0]
    hinf = mq[~np.isfinite(mq["hbucket"])]
    P("")
    _f0 = int((ok[ok["hbucket"] == 0].groupby(["char", "k"]).size() == len(SEEDS)).sum())
    _i0 = len(infeas[infeas["hbucket"] == 0])
    P(f"H_FEAS  : at h = 0 all {len(SEEDS)} seeds are feasible at {_f0} of "
      f"{len(CHARS)*len(KS)} (char, k) points -> "
      + ("HOLDS" if _i0 == 0 else "PARTIAL - see the infeasible table"))
    P(f"          listing-history residual collapses from {hinf.hist_resid_yrs.mean():.3f} yrs "
      f"(history-blind, idea 570's design) to {h0.hist_resid_yrs.mean():.3f} yrs at h = 0; "
      f"worst pair gap at h = 0 is {h0.max_hist_gap_d.max():.0f} days")
    P("")

    # ---------------------------------------------------------------- the origin gap
    P("=" * 108)
    P("THE ORIGIN GAP UNDER A HISTORY-MATCHED EXACT MATCH (all 12 tuned points x 2 chars)")
    P("=" * 108)
    orows = []
    for (ch, h, k), grp in ok.groupby(["char", "hbucket", "k"]):
        gaps = (grp.prem_B - grp.prem_S).to_numpy(float)
        sdp = float(np.sqrt((grp.prem_B.std(ddof=1) ** 2 + grp.prem_S.std(ddof=1) ** 2) / 2))
        gp = float(np.mean(gaps))
        n = len(grp)
        orows.append(dict(
            char=ch, hbucket=h, k=k, n=n, residual=float(grp.residual.mean()),
            hist_resid_yrs=float(grp.hist_residual_yrs.mean()),
            prem_B=float(grp.prem_B.mean()), prem_S=float(grp.prem_S.mean()), gap=gp,
            sd_gap=float(np.std(gaps, ddof=1)), sd_pair=sdp,
            t=gp / (sdp / np.sqrt(n)) if sdp > 0 else np.nan,
            within_floor=bool(abs(gp) <= sdp), ratio_to_GAP=gp / GAP_PUB,
            gap_IS=float((grp.premIS_B - grp.premIS_S).mean()),
            gap_OOS=float((grp.premOOS_B - grp.premOOS_S).mean())))
    OR = pd.DataFrame(orows)
    P(fmt(OR.set_index(["char", "hbucket", "k"])[
        ["n", "residual", "hist_resid_yrs", "prem_B", "prem_S", "gap", "sd_gap", "sd_pair", "t",
         "within_floor", "ratio_to_GAP"]], 4))
    P("")

    # ---- G5: a history-blind arm at idea 570's OWN k rungs must BE its tau=0.02 arm
    try:
        o570 = pd.read_csv(f"{P570}.origin.csv")
        o570 = o570[np.isclose(o570.tau, TAU)]
        g5rows = []
        for ch in CHARS:
            for k in sorted(o570[o570.char == ch].k.unique()):
                pb, ps, rs, nr = [], [], [], []
                for sd in SEEDS:
                    pr = greedy_match(nc, bnames, snames, ch, int(k), sd, first, np.inf)
                    if len(pr) < k:
                        continue
                    B = [p[0] for p in pr]
                    S = [p[1] for p in pr]
                    pb.append(premium_of(B))
                    ps.append(premium_of(S))
                    rs.append(abs(achieved_of(B, ch) - achieved_of(S, ch)))
                    nr.append(abs(float(np.mean([p[2] for p in pr]))
                                  - float(np.mean([p[3] for p in pr]))))
                g5rows.append(dict(
                    char=ch, k=int(k), n=len(pb), prem_B=float(np.mean(pb)),
                    prem_S=float(np.mean(ps)), gap=float(np.mean(pb) - np.mean(ps)),
                    sd_pair=float(np.sqrt((np.std(pb, ddof=1) ** 2
                                           + np.std(ps, ddof=1) ** 2) / 2)),
                    residual=float(np.mean(rs)), name_residual=float(np.mean(nr))))
        B5 = pd.DataFrame(g5rows)
        j = B5.merge(o570, on=["char", "k"], suffixes=("_r", "_c"))
        c5 = ["prem_B", "prem_S", "gap", "sd_pair", "residual", "name_residual"]
        g5d = max(float(np.abs(j[c + "_r"] - j[c + "_c"]).max()) for c in c5) if len(j) else np.nan
        P(f"G5 h=inf == 570 : HISTORY-BLIND arm re-run at idea 570's own k rungs "
          f"{sorted(B5.k.unique())} vs its committed tau=0.02 rows, {len(j)} (char, k) points x "
          f"{len(c5)} columns, max |d| = {g5d:.3e} (bar {IDENT:.0e}) -> "
          f"{'PASS' if g5d < IDENT else 'FAIL'}")
        P("                  " + fmt(B5.set_index(["char", "k"])[c5], 6)
          .replace("\n", "\n                  "))
    except FileNotFoundError:
        P("G5 h=inf == 570 : idea 570's .origin.csv not found -> SKIPPED (reported, not hidden)")
    P("")

    P("GAP LADDER in the history bucket (does closing the listing-history channel shrink it?)")
    P(fmt(OR.pivot_table(index=["char", "k"], columns="hbucket", values="gap"), 4))
    P("  (mean listing-history residual, years, at the same points)")
    P(fmt(OR.pivot_table(index=["char", "k"], columns="hbucket", values="hist_resid_yrs"), 4))
    P("  (mean characteristic residual at the same points - the channel idea 570 closed)")
    P(fmt(OR.pivot_table(index=["char", "k"], columns="hbucket", values="residual"), 5))
    P("")

    t0r = OR[OR["hbucket"] == 0]
    P(f"H_SURV  : at h = 0 the gap is inside its own seed sd on "
      f"{int(t0r.within_floor.sum())} of {len(t0r)} points; gaps "
      f"{t0r.gap.min():+.4f} to {t0r.gap.max():+.4f} vs sd_pair "
      f"{t0r.sd_pair.min():.4f}-{t0r.sd_pair.max():.4f} -> "
      + ("HOLDS - the origin gap WAS the listing-history channel"
         if bool(t0r.within_floor.all()) else
         "FALSIFIED - origin survives an exact characteristic AND listing-history match"))
    mono = []
    for (ch, k), grp in OR.groupby(["char", "k"]):
        gs = grp.sort_values("hbucket", ascending=False).gap.to_numpy(float)
        mono.append(bool(np.all(np.diff(np.abs(gs)) <= 1e-12)))
    P(f"H_HMONO : |gap| falls monotonically as h tightens on {sum(mono)} of {len(mono)} "
      f"(characteristic, k) ladders -> {'HOLDS' if all(mono) else 'FALSIFIED'}")
    bl = OR[~np.isfinite(OR["hbucket"])].set_index(["char", "k"]).gap
    t0i = t0r.set_index(["char", "k"]).gap
    dd = (t0i - bl.reindex(t0i.index)).dropna()
    P(f"H_DIR   : h=0 minus history-blind, per (char, k): mean {dd.mean():+.4f}, range "
      f"{dd.min():+.4f} to {dd.max():+.4f}; the gap GROWS at {int((dd>0).sum())} of {len(dd)} "
      f"points -> closing the listing-history channel "
      + ("GROWS the gap (survivorship was working AGAINST idea 570's finding)"
         if dd.mean() > 0 else "SHRINKS the gap (survivorship was inflating it)"))
    P(f"          h=0 band [{t0r.gap.min():+.4f}, {t0r.gap.max():+.4f}] vs idea 570's exact-match "
      f"band [{G570_MIN:+.4f}, {G570_MAX:+.4f}] vs published {GAP_PUB:+.4f}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 108)
    P("KEEP PATHS (PROTOCOL rule 4a and 4b, every book on the history-matched grid)")
    P("=" * 108)
    P(f"over {len(G)} books: 4a {int(G.keep4a.sum())}/{len(G)}, 4b {int(G.keep4b.sum())}/{len(G)}, "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}/{len(G)}")
    P("  by side: " + ", ".join(
        f"{s} 4a {int(v.keep4a.sum())}/{len(v)} 4b {int(v.keep4b.sum())}/{len(v)}"
        for s, v in G.groupby("side")))
    P("  by hist: " + ", ".join(
        f"h={h} 4b {int(v.keep4b.sum())}/{len(v)}" for h, v in G.groupby("hbucket", dropna=False)))
    P("  by arm : " + ", ".join(
        f"{s} 4b {int(v.keep4b.sum())}/{len(v)}" for s, v in G.groupby("arm")))
    P("  4b binding failure legs: " + ", ".join(
        f"{a} {b}" for a, b in G.fail4b.value_counts().head(6).items()))
    P("")

    # ---------------------------------------------------------------- rule 8
    P("=" * 108)
    P("RULE 8 WALK-FORWARD")
    P("=" * 108)
    P("WF-A: the history-matched origin gap re-read on IS-only and OOS-only returns")
    P(fmt(OR.set_index(["char", "hbucket", "k"])[["gap", "gap_IS", "gap_OOS"]], 4))
    same_sign = int(((np.sign(OR.gap_IS) == np.sign(OR.gap_OOS)) & (OR.gap_IS != 0)).sum())
    P(f"  gap holds sign IS vs OOS at {same_sign} of {len(OR)} points; mean gap "
      f"FULL {OR.gap.mean():+.4f} / IS {OR.gap_IS.mean():+.4f} / OOS {OR.gap_OOS.mean():+.4f}")
    ss0 = int(((np.sign(t0r.gap_IS) == np.sign(t0r.gap_OOS)) & (t0r.gap_IS != 0)).sum())
    P(f"  at h = 0 alone: sign held {ss0} of {len(t0r)}; mean FULL {t0r.gap.mean():+.4f} / "
      f"IS {t0r.gap_IS.mean():+.4f} / OOS {t0r.gap_OOS.mean():+.4f}")
    P("")

    P("WF-B: the history-matched origin contrast priced as a BOOK - pick (char, h, k) by IS")
    P("      Sharpe of the seed-pooled B-side MA-RS book at g=0.75/W; OOS read ONCE.")
    sel = G[(G.arm == "MA-RS") & (G.gross == 0.75) & (G.cadence == "W")]
    pick_tbl = sel[sel.side == "B"].groupby(["char", "hbucket", "k"]).IS_Sharpe.mean()
    P("  IS Sharpe of the B-side book at every point (the selection surface):")
    P(fmt(pick_tbl.to_frame(), 4))
    best = pick_tbl.idxmax()
    P(f"  IS-best point: char={best[0]}, h={best[1]}, k={best[2]}  (IS Sharpe {pick_tbl.max():.4f})")

    u56px, u56tr = panels["U56"]
    st56 = u56px.index[260]
    v2_56 = fast_backtest(u56px, rules_v2_weights(u56px), COST, "W")["returns"].loc[st56:]
    spy56 = u56px["SPY"].pct_change().fillna(0.0).loc[st56:]

    def pooled_book(char, h, k, which):
        """Seed-pooled equal-weight-of-seeds MA-RS book at g=0.75/W.
        which in {'B','S','BLIND'} - BLIND pools each seed's B and S matched names."""
        segs = []
        for sd in SEEDS:
            row = M[(M.char == char) & (M.k == k) & (M.seed == sd)
                    & ((M["hbucket"] == h) if np.isfinite(h) else ~np.isfinite(M["hbucket"]))]
            if not len(row) or not bool(row.feasible.iloc[0]):
                continue
            if which == "BLIND":
                names = row["names_B"].iloc[0].split(",") + row["names_S"].iloc[0].split(",")
            else:
                names = row[f"names_{which}"].iloc[0].split(",")
            pxd = frame_of(names)
            w = make_books(pxd, set(names), 0.75)["MA-RS"]
            segs.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[pxd.index[260]:])
        idx = segs[0].index
        return pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)

    # INCUMBENT controls: the record's existing MA-RS gate on the WHOLE panels.
    pxB_pool = pd.concat([pool[bnames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    b136_full = fast_backtest(pxB_pool, make_books(pxB_pool, set(bnames), 0.75)["MA-RS"],
                              COST, "W")["returns"].loc[pxB_pool.index[260]:]
    pxS_pool = pd.concat([pool[snames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    small_full = fast_backtest(pxS_pool, make_books(pxS_pool, set(snames), 0.75)["MA-RS"],
                               COST, "W")["returns"].loc[pxS_pool.index[260]:]
    # FULL-HISTORY-ONLY small panel: the crudest survivorship control, reported beside it.
    sfull_names = sorted([n for n in snames if first.loc[n] == ix.min()])
    pxSF = pd.concat([pool[sfull_names], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    small_fh = fast_backtest(pxSF, make_books(pxSF, set(sfull_names), 0.75)["MA-RS"],
                             COST, "W")["returns"].loc[pxSF.index[260]:]

    bside = pooled_book(*best, "B")
    wf_rows = []
    for nm, r in (("B-side (IS pick)", bside),
                  ("S-side twin", pooled_book(*best, "S")),
                  ("ORIGIN-BLIND control", pooled_book(*best, "BLIND")),
                  ("INCUMBENT B136 MA-RS g0.75 W", b136_full),
                  (f"SMALL{len(snames)} MA-RS g0.75 W", small_full),
                  (f"SMALL full-history only (n={len(sfull_names)})", small_fh),
                  ("RULES v2 U56 (live book)", v2_56),
                  ("SPY", spy56)):
        sp = spy56.reindex(r.index).fillna(0.0)
        mo, mf = metrics(r.loc[OOS_START:]), metrics(r)
        wf_rows.append(dict(book=nm, CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            keep4a=keep_4a(r, v2_56.reindex(r.index).fillna(0.0)),
                            fail4b=fail_4b(r, sp), keep4b=(fail_4b(r, sp) == "-")))
    WF = pd.DataFrame(wf_rows)
    P(fmt(WF.set_index("book"), 4))
    bs = float(WF[WF.book == "RULES v2 U56 (live book)"].OOS_Sharpe.iloc[0])
    ss = float(WF[WF.book == "SPY"].OOS_Sharpe.iloc[0])
    cand = WF[WF.book.isin(["B-side (IS pick)", "S-side twin", "ORIGIN-BLIND control"])]
    P(f"  books beating RULES v2 U56 OOS Sharpe ({bs:.4f}): {int((cand.OOS_Sharpe>bs).sum())}/3; "
      f"beating SPY ({ss:.4f}): {int((cand.OOS_Sharpe>ss).sum())}/3")
    P(f"  decision books: 4a {int(cand.keep4a.sum())}/3, 4b {int(cand.keep4b.sum())}/3, "
      f"BOTH {int((cand.keep4a & cand.keep4b).sum())}/3")
    ix2 = bside.index.intersection(b136_full.index)
    corr = float(np.corrcoef(bside.reindex(ix2).fillna(0.0),
                             b136_full.reindex(ix2).fillna(0.0))[0, 1])
    P(f"  B-side book vs the INCUMBENT whole-B136 MA-RS gate, daily-return correlation: {corr:.4f}")
    P("")

    # A directly readable survivorship statement, no tuning: whole-S panel vs its
    # full-history-only subset at the same gross and cadence.
    sf = WF[WF.book.str.startswith("SMALL full-history")].iloc[0]
    sa = WF[WF.book.str.startswith(f"SMALL{len(snames)}")].iloc[0]
    P("  SURVIVORSHIP READ-ACROSS (no tuning): the SMALL panel restricted to its "
      f"{len(sfull_names)} full-history names runs CAGR {sf.CAGR:.2%} / Sharpe {sf.Sharpe:.4f} "
      f"against the whole {len(snames)}-name panel's {sa.CAGR:.2%} / {sa.Sharpe:.4f} "
      f"(OOS Sharpe {sf.OOS_Sharpe:.4f} vs {sa.OOS_Sharpe:.4f}).")
    P("")

    # ---------------------------------------------------------------- write
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    M.drop(columns=[c for c in M.columns if c.startswith("names_")]).to_csv(
        OUT / f"{STAMP}.match.csv", index=False)
    OR.to_csv(OUT / f"{STAMP}.origin.csv", index=False)
    pd.concat([g1.assign(leg="G1_kernel_repro"), WF.assign(leg="WF-B")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    G[["char", "hbucket", "k", "seed", "side", "arm", "gross", "cadence", "keep4a", "fail4b",
       "keep4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"wrote grid {len(G)}, match {len(M)}, origin {len(OR)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
