#!/usr/bin/env python3
"""Idea 570 (cloud, 2026-09-11) - is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect.

QUESTION
--------
Idea 568 (lane C, 2026-09-09) matched B136-sourced and SMALL439-sourced k=36 draws on a
characteristic with a Gaussian KERNEL and found the panel of ORIGIN still separates the
MA-gate selection premium by +0.2537 / +0.1997 / +0.1348 (t +8.04 / +7.11 / +5.55), i.e. at
2.00x the whole published U56-SMALL439 gap.  But the kernel never matched exactly: at the
cvol L=0.32 rung the B draws land at 0.2732 and the S draws at 0.4022 - a 0.1290 residual.
This run replaces the kernel with an EXACT one-to-one NAME-LEVEL match (greedy
nearest-neighbour pairing of one B name to one S name on the characteristic, k pairs) and
re-reads the B-S premium gap and its seed sd under that match.

WHY THE RESIDUAL MATTERS AND WHICH WAY IT CUTS
----------------------------------------------
If the characteristic carried the premium, the un-matched residual would have to explain the
gap.  Idea 568 argued the residual works AGAINST its own finding (the B draws sit at lower
cvol, and the pooled cvol slope it measured runs the WRONG way), so its +0.2537 is a lower
bound.  That argument is an inference from a slope it also called noise.  An exact match
removes the argument entirely: under one-to-one pairing the two panels carry the SAME
characteristic distribution by construction, so whatever gap remains cannot be a matching
residual.  The direction the gap moves when the residual is driven to zero is the answer.

DESIGN
------
Pool  = 135 B136 tradables + 439 SMALL439 tradables on the COMMON index (2010-01-04 ..
        2026-09-04), idea 568's pooled frame verbatim; SPY joined as benchmark only.
Match = for each seed, shuffle the B names, and give each in turn its NEAREST unused S
        partner on the characteristic, accepting the pair only if |x_b - x_s| <= tau.
        Take the first k accepted pairs.  The B panel is those k B names; the S panel is
        their k matched S partners.  One-to-one, no name reused, panels equally wide.
Arms  (idea 51 / 312 / 568 verbatim): EWall = gross g over every priced tradable name
        (CONTROL); MA-RS = gross g respread over names above their 200d MA (TREATMENT);
        premium = Sharpe(MA-RS) - Sharpe(EWall) at the SAME (panel, g, cadence).  RESPREAD
        holds gross fixed, so the premium is pure selection with no exposure dial.
GAP   = premium(B panel) - premium(S panel), per seed; headline = mean over seeds, sd =
        sd over seeds, and sd_pair = sqrt((sd_B^2 + sd_S^2)/2) so it is the SAME statistic
        idea 568 published.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. MATCH TOLERANCE tau in {0.01, 0.02, 0.05, inf}   (inf = nearest available, no cap)
    2. k in {18, 36, 72} pairs
All 4 x 3 = 12 grid points are reported, for BOTH characteristics.
REPORTED (never selected) axes: characteristic {cvol, breadth}, gross {0.50, 0.75, 1.00},
    cadence {W, M}, seed (12), period (FULL / IS / OOS).

PRE-REGISTERED HYPOTHESES (written before any exactly-matched premium was read)
------------------------------------------------------------------------------
GAP_PUB   = 0.0978  (idea 51's published U56 - SMALL439 premium gap)
KERNEL    = 0.2537  (idea 568's origin gap at its cvol L=0.32 rung)
RESID_568 = 0.1290  (its B/S achieved-characteristic residual at that rung)
H_EXACT  : the one-to-one match drives the B-vs-S characteristic residual below 0.01 at
           tau <= 0.02 - two orders below idea 568's 0.1290.  This is the run's premise; if
           it fails, an exact match is not available and the question cannot be answered.
H_RESID  : the origin gap IS the matching residual.  Falsified unless the gap at the exact
           match falls inside its own seed sd (|gap| <= sd_pair) at tau <= 0.02.
H_MONO   : if the residual carries the gap, the gap shrinks monotonically as tau tightens
           (inf -> 0.05 -> 0.02 -> 0.01).  A flat or non-monotone ladder says the residual
           is not the carrier.

GATES (pre-registered, run and printed before any new number is read)
    G1 kernel reproduction : idea 568's committed `.origin.csv` rows (achieved_B, achieved_S,
       prem_B, prem_S, gap, sd_pair, t) rebuilt HERE from its own seeding scheme and price
       source, all 3 rows x 7 columns.                                          bar 1e-9
    G2 real panels         : the three real panels' published premia re-derived from prices
       and compared to idea 568's committed REAL grid rows.       bar 1e-9 (1e-4 on U56,
       which carries idea 312's documented data/prices.csv adjusted-close revision)
    G3 identity            : fast_backtest vs engine.backtest on one book per real panel.
                                                                                 bar 1e-12
    G4 pool                : the pooled frame reproduces idea 568's name counts and window
       (574 names, 2010-01-04 .. 2026-09-04) exactly.                              exact

RULE 8 WALK-FORWARD (required, run whatever the match says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: re-read the exactly-matched origin gap on IS-only and on OOS-only
       returns at every one of the 12 points and report whether it holds sign and magnitude.
    WF-B on a BOOK: the origin contrast is a DECISION RULE - "trade the B-sourced panel
       rather than the S-sourced one at matched characteristic".  Pick (characteristic, tau,
       k) by IS Sharpe of the seed-pooled B-side MA-RS book at g=0.75/W, read OOS ONCE
       against RULES v2 on U56 and SPY; the S-side twin and an ORIGIN-BLIND control (the
       matched pair's names pooled) are reported beside it.
    KEEP paths 4a and 4b are evaluated for EVERY book.  Stated up front: a matched draw is a
       diagnostic panel, NOT a rule anyone can trade, so a 4b pass here is a diagnostic and
       never a capital candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, so every
    draw carries a survivorship premium and the small end carries more of it.  The premium is
    an arm-minus-arm difference on the SAME panel, so the level bias largely cancels, but the
    B-minus-S ORIGIN gap does NOT cancel it - a differential survivorship premium between the
    two panels is an alternative explanation this design cannot exclude, and it is restated
    beside the headline.  The small panel additionally drops every ticker with
    max_1d_move >= 1.0 (439 of 483 kept).

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and committed artefacts of
idea 568; modifies nothing but its own outputs:
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
TAUS = [0.01, 0.02, 0.05, np.inf]
KS = [18, 36, 72]
SEEDS = list(range(12))

# idea 568's own constants and published numbers
K568 = 36
SEEDS568 = [0, 1, 2, 3, 4, 5]
LEVELS568 = {"cvol": [0.25, 0.32, 0.39, 0.46, 0.53, 0.60],
             "breadth": [0.46, 0.52, 0.58, 0.64, 0.70]}
BW_MULT = 0.5
GAP_PUB = 0.0978
KERNEL = 0.2537
RESID_568 = 0.1290
P568 = OUT / "2026-09-09_can-any-B136-recomposition-reach-SMALL439-s-CHARACTERISTIC-SUPPORT_C"
P312 = OUT / "2026-09-09_is-the-panel-ordering-an-ETF-SHARE-effect_B.grid.csv"
TOL, TOL_U56, EXACT_BAR = 1e-9, 1e-4, 0.01

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G3).  Idea 312/568's runner."""
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
    """idea 568's per-NAME characteristic, verbatim: annualised vol and MA breadth."""
    r = pool.pct_change()
    vol = (r.std() * np.sqrt(252)).astype(float)
    on = above_ma(pool) & pool.notna()
    br = (on.sum() / pool.notna().sum().replace(0, np.nan)).astype(float)
    return pd.DataFrame(dict(cvol=vol, breadth=br)).dropna()


def feasible_band(x, k=K568):
    v = np.sort(np.asarray(x, float))
    return float(v[:k].mean()), float(v[-k:].mean())


def panel_char_568(pxd, tradable, char):
    """idea 568's panel_chars, restricted to the two characteristics this run uses.

    NOTE this is NOT the mean of the per-name characteristic: `breadth` is the mean over DAYS
    of the cross-sectional share above the 200d MA, which differs from the mean over NAMES
    whenever names have different histories.  Idea 568's `achieved` column is this object, so
    every residual quoted against its 0.1290 is computed the same way."""
    cols = [c for c in pxd.columns if c in tradable]
    if char == "cvol":
        return float((pxd[cols].pct_change().std() * np.sqrt(252)).mean())
    on = above_ma(pxd[cols]) & pxd[cols].notna()
    return float(on.sum(axis=1).div(pxd[cols].notna().sum(axis=1).replace(0, np.nan)).mean())


# ------------------------------------------------------------------------- matching
def greedy_match(nc, bnames, snames, char, tau, k, seed):
    """One-to-one greedy nearest-neighbour pairing of a B name to an S name on `char`.

    The B names are visited in a seeded random order; each takes its nearest UNUSED S
    partner, and the pair is kept only if |x_b - x_s| <= tau.  The first k accepted pairs
    are returned.  No name is ever reused on either side, so the two panels are equally wide
    and carry the same characteristic distribution up to tau."""
    rng = np.random.default_rng(zlib.crc32(f"MATCH|{char}|{tau}|{k}|{seed}".encode()) % (2 ** 32))
    xb = nc.loc[sorted(bnames), char]
    xs = nc.loc[sorted(snames), char].sort_values()
    s_names = xs.index.to_numpy()
    s_vals = xs.to_numpy(float)
    used = np.zeros(len(s_vals), bool)
    order = rng.permutation(xb.index.to_numpy())
    pairs = []
    for b in order:
        if len(pairs) >= k:
            break
        v = float(xb.loc[b])
        d = np.abs(s_vals - v)
        d[used] = np.inf
        j = int(np.argmin(d))
        if not np.isfinite(d[j]) or d[j] > tau:
            continue
        used[j] = True
        pairs.append((b, str(s_names[j]), float(v), float(s_vals[j]), float(d[j])))
    return pairs


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P("=" * 108)
    P(f"IDEA 570  is-the-ORIGIN-gap-a-MATCHING-RESIDUAL-or-a-real-panel-effect  (cloud, 2026-09-11)")
    P("=" * 108)
    P(f"PROTOCOL: {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START} read once.")
    P(f"TUNED (2): MATCH TOLERANCE tau in {TAUS} x k in {KS} -- all 12 points reported.")
    P(f"Pre-registered: GAP_PUB {GAP_PUB:.4f}, idea 568 KERNEL gap {KERNEL:.4f}, "
      f"its residual {RESID_568:.4f}.")
    P("")

    # ---------------------------------------------------------------- gates
    P("=" * 108)
    P("GATES (pre-registered; printed before any exactly-matched number is read)")
    P("=" * 108)
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, real_rows = {}, []
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = fast_backtest(px, rules_v2_weights(px), COST, "W")["returns"].loc[st:]
        ref[nm] = dict(start=st, spy=spy, v2=v2)
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
    P(f"G2 real panels  : {len(m)} of 36 REAL rows vs idea 312/568's committed grid; per panel "
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
      f"{'PASS' if g3 < 1e-12 else 'FAIL'}")

    # pooled frame (idea 568's, verbatim)
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
          and str(ix.min().date()) == "2010-01-04" and str(ix.max().date()) == "2026-09-04")
    P(f"G4 pool         : {ix.min().date()}..{ix.max().date()}, B {len(bnames)} + SMALL "
      f"{len(snames)} = {len(nc)} names -> {'PASS' if g4 else 'FAIL'} (idea 568's COMMITTED "
      f"CONSOLE: 'pooled index 2010-01-04 .. 2026-09-04 (4194 bars)', 'names: B 134 SMALL 439 "
      f"total 573'; bars here {len(ix)})")
    P("                  DEFECT FOUND, minor: idea 568's committed docstring states "
      "'Pool = 135 B136 tradables + 439 SMALL tradables = 574 names'. Its own console, and "
      "this reproduction, say 134 + 439 = 573 - one B136 name carries no characteristic and "
      "is dropped by `name_chars`. The prose was never reconciled with the run; the NUMBERS "
      "are unaffected (every published rung used the 573-name pool).")

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
    P("                  " + fmt(g1.set_index(["char", "level"])[c1], 4).replace("\n", "\n                  "))
    resid_reread = float(np.abs(g1.achieved_B - g1.achieved_S).max())
    P(f"                  idea 568's worst B/S characteristic residual re-read: "
      f"{resid_reread:.4f} (queue quotes {RESID_568:.4f} at cvol L=0.32)")
    P("")

    # ---------------------------------------------------------------- the exact match
    P("=" * 108)
    P("THE EXACT ONE-TO-ONE MATCH (greedy nearest-neighbour, k pairs, no name reused)")
    P("=" * 108)
    for ch in CHARS:
        blo, bhi = feasible_band(nc.loc[bnames, ch])
        slo, shi = feasible_band(nc.loc[snames, ch])
        P(f"  {ch:8s} B range [{nc.loc[bnames,ch].min():.4f}, {nc.loc[bnames,ch].max():.4f}] "
          f"mean {nc.loc[bnames,ch].mean():.4f}   S range "
          f"[{nc.loc[snames,ch].min():.4f}, {nc.loc[snames,ch].max():.4f}] "
          f"mean {nc.loc[snames,ch].mean():.4f}   k=36 reach B [{blo:.3f},{bhi:.3f}] "
          f"S [{slo:.3f},{shi:.3f}]")
    P("")

    mrows, grows = [], []
    for ch in CHARS:
        for tau in TAUS:
            for k in KS:
                for sd in SEEDS:
                    pr = greedy_match(nc, bnames, snames, ch, tau, k, sd)
                    if len(pr) < k:
                        mrows.append(dict(char=ch, tau=tau, k=k, seed=sd, n_pairs=len(pr),
                                          feasible=False, achieved_B=np.nan, achieved_S=np.nan,
                                          residual=np.nan, max_pair_d=np.nan,
                                          prem_B=np.nan, prem_S=np.nan))
                        continue
                    B = [p[0] for p in pr]
                    S = [p[1] for p in pr]
                    nb = float(np.mean([p[2] for p in pr]))
                    ns = float(np.mean([p[3] for p in pr]))
                    ab = achieved_of(B, ch)          # idea 568's `achieved`, same estimator
                    as_ = achieved_of(S, ch)
                    mxd = float(np.max([p[4] for p in pr]))
                    row = dict(char=ch, tau=tau, k=k, seed=sd, n_pairs=len(pr), feasible=True,
                               achieved_B=ab, achieved_S=as_, residual=abs(ab - as_),
                               name_B=nb, name_S=ns, name_residual=abs(nb - ns),
                               max_pair_d=mxd)
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
                                    gr = dict(char=ch, tau=tau, k=k, seed=sd, side=side, arm=a,
                                              gross=g, cadence=freq)
                                    gr.update(rowify(r, res[a]["turnover"].loc[st:]))
                                    gr["keep4a"] = keep_4a(r, v2)
                                    gr["fail4b"] = fail_4b(r, spy)
                                    gr["keep4b"] = gr["fail4b"] == "-"
                                    grows.append(gr)
                        row[f"prem_{side}"] = float(np.mean(pf))
                        row[f"premIS_{side}"] = float(np.mean(pi))
                        row[f"premOOS_{side}"] = float(np.mean(po))
                        row[f"names_{side}"] = ",".join(names)
                    mrows.append(row)
        P(f"  {ch}: {len(TAUS)} tau x {len(KS)} k x {len(SEEDS)} seeds matched "
          f"({time.time()-t0:.0f}s)")
    M = pd.DataFrame(mrows)
    G = pd.DataFrame(grows)
    P("")

    # ---------------------------------------------------------------- match quality
    P("=" * 108)
    P("MATCH QUALITY - the residual idea 568 could not remove (bar for H_EXACT: 0.01)")
    P("=" * 108)
    ok = M[M.feasible]
    mq = ok.groupby(["char", "tau", "k"]).agg(
        seeds=("seed", "size"), achieved_B=("achieved_B", "mean"),
        achieved_S=("achieved_S", "mean"), residual=("residual", "mean"),
        name_residual=("name_residual", "mean"),
        max_pair_d=("max_pair_d", "mean")).reset_index()
    P(fmt(mq.set_index(["char", "tau", "k"]), 5))
    infeas = M[~M.feasible]
    if len(infeas):
        P("  INFEASIBLE points (fewer than k pairs available within tau) - reported, not dropped:")
        for (ch, tau, k), grp in infeas.groupby(["char", "tau", "k"]):
            P(f"    {ch:8s} tau {tau:<5} k {k:3d}: {len(grp)} of {len(SEEDS)} seeds short "
              f"(max pairs found {int(M[(M.char==ch)&(M.tau==tau)&(M.k==k)].n_pairs.max())})")
    tt = mq[mq.tau <= 0.02]
    worst_tight = float(tt.residual.max()) if len(tt) else np.nan
    worst_name = float(tt.name_residual.max()) if len(tt) else np.nan
    P("")
    P(f"H_EXACT : at tau <= 0.02 the worst mean NAME-level residual (what the match controls) "
      f"is {worst_name:.6f}; the worst PANEL-level residual, idea 568's own estimator, is "
      f"{worst_tight:.5f} against its {RESID_568:.4f} (bar {EXACT_BAR}) -> "
      f"{'HOLDS - the match IS exact' if worst_tight < EXACT_BAR else 'FALSIFIED at the panel level'}")
    P("")

    # ---------------------------------------------------------------- the origin gap
    P("=" * 108)
    P("THE ORIGIN GAP UNDER AN EXACT MATCH (all 12 tuned points x 2 characteristics)")
    P("=" * 108)
    orows = []
    for (ch, tau, k), grp in ok.groupby(["char", "tau", "k"]):
        gaps = (grp.prem_B - grp.prem_S).to_numpy(float)
        sdp = float(np.sqrt((grp.prem_B.std(ddof=1) ** 2 + grp.prem_S.std(ddof=1) ** 2) / 2))
        gp = float(np.mean(gaps))
        n = len(grp)
        orows.append(dict(
            char=ch, tau=tau, k=k, n=n, residual=float(grp.residual.mean()),
            name_residual=float(grp.name_residual.mean()),
            prem_B=float(grp.prem_B.mean()), prem_S=float(grp.prem_S.mean()), gap=gp,
            sd_gap=float(np.std(gaps, ddof=1)), sd_pair=sdp,
            t=gp / (sdp / np.sqrt(n)) if sdp > 0 else np.nan,
            within_floor=bool(abs(gp) <= sdp), ratio_to_GAP=gp / GAP_PUB,
            ratio_to_KERNEL=gp / KERNEL,
            gap_IS=float((grp.premIS_B - grp.premIS_S).mean()),
            gap_OOS=float((grp.premOOS_B - grp.premOOS_S).mean())))
    OR = pd.DataFrame(orows)
    P(fmt(OR.set_index(["char", "tau", "k"])[
        ["n", "name_residual", "residual", "prem_B", "prem_S", "gap", "sd_gap", "sd_pair", "t",
         "within_floor", "ratio_to_GAP", "ratio_to_KERNEL"]], 4))
    P("")
    P("GAP LADDER in the match tolerance (does tightening the match shrink the gap?)")
    P(fmt(OR.pivot_table(index=["char", "k"], columns="tau", values="gap"), 4))
    P("  (mean |residual| at the same points)")
    P(fmt(OR.pivot_table(index=["char", "k"], columns="tau", values="residual"), 5))
    P("")

    tight = OR[OR.tau <= 0.02]
    P(f"H_RESID : at tau <= 0.02 the gap is inside its own seed sd on "
      f"{int(tight.within_floor.sum())} of {len(tight)} points; gaps "
      f"{tight.gap.min():+.4f} to {tight.gap.max():+.4f} vs sd_pair "
      f"{tight.sd_pair.min():.4f}-{tight.sd_pair.max():.4f} -> "
      f"{'HOLDS - the origin gap WAS the matching residual' if bool(tight.within_floor.all()) else 'FALSIFIED - origin survives an EXACT match'}")
    mono = []
    for (ch, k), grp in OR.groupby(["char", "k"]):
        gs = grp.sort_values("tau", ascending=False).gap.to_numpy(float)
        mono.append(bool(np.all(np.diff(np.abs(gs)) <= 1e-12)))
    P(f"H_MONO  : |gap| falls monotonically as tau tightens on {sum(mono)} of {len(mono)} "
      f"(characteristic, k) ladders -> {'HOLDS' if all(mono) else 'FALSIFIED'}")
    P("")

    # ---------------------------------------------------------------- KEEP paths
    P("=" * 108)
    P("KEEP PATHS (PROTOCOL rule 4a and 4b, every book on the matched grid)")
    P("=" * 108)
    P(f"over {len(G)} books: 4a {int(G.keep4a.sum())}/{len(G)}, 4b {int(G.keep4b.sum())}/{len(G)}, "
      f"BOTH {int((G.keep4a & G.keep4b).sum())}/{len(G)}")
    P("  by side: " + ", ".join(
        f"{s} 4a {int(v.keep4a.sum())}/{len(v)} 4b {int(v.keep4b.sum())}/{len(v)}"
        for s, v in G.groupby("side")))
    P("  by arm : " + ", ".join(
        f"{s} 4b {int(v.keep4b.sum())}/{len(v)}" for s, v in G.groupby("arm")))
    P("  4b binding failure legs: " + ", ".join(
        f"{a} {b}" for a, b in G.fail4b.value_counts().head(6).items()))
    P("")

    # ---------------------------------------------------------------- rule 8
    P("=" * 108)
    P("RULE 8 WALK-FORWARD")
    P("=" * 108)
    P("WF-A: the exactly-matched origin gap re-read on IS-only and OOS-only returns")
    wfa = OR.set_index(["char", "tau", "k"])[["gap", "gap_IS", "gap_OOS"]]
    P(fmt(wfa, 4))
    same_sign = int(((np.sign(OR.gap_IS) == np.sign(OR.gap_OOS)) & (OR.gap_IS != 0)).sum())
    P(f"  gap holds sign IS vs OOS at {same_sign} of {len(OR)} points; mean gap "
      f"FULL {OR.gap.mean():+.4f} / IS {OR.gap_IS.mean():+.4f} / OOS {OR.gap_OOS.mean():+.4f}")
    P("")

    P("WF-B: the origin contrast priced as a BOOK - pick (char, tau, k) by IS Sharpe of the")
    P("      seed-pooled B-side MA-RS book at g=0.75/W; OOS read ONCE.")
    sel = G[(G.arm == "MA-RS") & (G.gross == 0.75) & (G.cadence == "W")]
    pick_tbl = sel[sel.side == "B"].groupby(["char", "tau", "k"]).IS_Sharpe.mean()
    P("  IS Sharpe of the B-side book at every point (the selection surface):")
    P(fmt(pick_tbl.to_frame(), 4))
    best = pick_tbl.idxmax()
    P(f"  IS-best point: char={best[0]}, tau={best[1]}, k={best[2]}  "
      f"(IS Sharpe {pick_tbl.max():.4f})")
    u56px, u56tr = panels["U56"]
    st56 = u56px.index[260]
    v2_56 = fast_backtest(u56px, rules_v2_weights(u56px), COST, "W")["returns"].loc[st56:]
    spy56 = u56px["SPY"].pct_change().fillna(0.0).loc[st56:]

    def book_of(char, tau, k, side):
        """Seed-pooled equal-weight-of-seeds MA-RS book at g=0.75/W on that side's panels."""
        segs = []
        for sd in SEEDS:
            row = M[(M.char == char) & (M.tau == tau) & (M.k == k) & (M.seed == sd)]
            if not len(row) or not bool(row.feasible.iloc[0]):
                continue
            names = row[f"names_{side}"].iloc[0].split(",")
            cols = list(dict.fromkeys(names + ["SPY"]))
            pxd = pd.concat([pool[names], spy_pool.rename("SPY")], axis=1)[cols] \
                .dropna(how="all").ffill()
            w = make_books(pxd, set(names), 0.75)["MA-RS"]
            segs.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[pxd.index[260]:])
        idx = segs[0].index
        return pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)

    def blind_of(char, tau, k):
        """ORIGIN-BLIND control: each seed's B and S matched names POOLED into one panel."""
        segs = []
        for sd in SEEDS:
            row = M[(M.char == char) & (M.tau == tau) & (M.k == k) & (M.seed == sd)]
            if not len(row) or not bool(row.feasible.iloc[0]):
                continue
            names = row["names_B"].iloc[0].split(",") + row["names_S"].iloc[0].split(",")
            cols = list(dict.fromkeys(names + ["SPY"]))
            pxd = pd.concat([pool[names], spy_pool.rename("SPY")], axis=1)[cols] \
                .dropna(how="all").ffill()
            w = make_books(pxd, set(names), 0.75)["MA-RS"]
            segs.append(fast_backtest(pxd, w, COST, "W")["returns"].loc[pxd.index[260]:])
        idx = segs[0].index
        return pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)

    # INCUMBENT control: the record's existing MA-RS gate on the WHOLE B136 panel, same
    # window, same gross and cadence.  If the B-side book's numbers are this book's numbers,
    # any KEEP path it clears belongs to a book the record already has.
    pxB_pool = pd.concat([pool[bnames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    b136_full = fast_backtest(pxB_pool, make_books(pxB_pool, set(bnames), 0.75)["MA-RS"],
                              COST, "W")["returns"].loc[pxB_pool.index[260]:]
    pxS_pool = pd.concat([pool[snames], spy_pool.rename("SPY")], axis=1).dropna(how="all").ffill()
    small_full = fast_backtest(pxS_pool, make_books(pxS_pool, set(snames), 0.75)["MA-RS"],
                               COST, "W")["returns"].loc[pxS_pool.index[260]:]

    bside = book_of(*best, "B")
    wf_rows = []
    for nm, r in (("B-side (IS pick)", bside),
                  ("S-side twin", book_of(*best, "S")),
                  ("ORIGIN-BLIND control", blind_of(*best)),
                  ("INCUMBENT B136 MA-RS g0.75 W", b136_full),
                  ("SMALL439 MA-RS g0.75 W", small_full),
                  ("RULES v2 U56 (live book)", v2_56),
                  ("SPY", spy56)):
        sp = spy56.reindex(r.index).fillna(0.0)
        mo = metrics(r.loc[OOS_START:])
        mf = metrics(r)
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
    corr = float(np.corrcoef(bside.reindex(ix2).fillna(0.0), b136_full.reindex(ix2).fillna(0.0))[0, 1])
    inc = WF[WF.book == "INCUMBENT B136 MA-RS g0.75 W"].iloc[0]
    bs_row = WF[WF.book == "B-side (IS pick)"].iloc[0]
    P("")
    P("  IS THE B-SIDE BOOK ANYTHING BUT THE INCUMBENT? daily-return correlation with the "
      f"whole-B136 MA-RS gate at the same gross/cadence: {corr:.4f}")
    P(f"    B-side   CAGR {bs_row.CAGR:.2%} Sharpe {bs_row.Sharpe:.4f} MaxDD {bs_row.MaxDD:.2%} "
      f"| OOS {bs_row.OOS_CAGR:.2%} / {bs_row.OOS_Sharpe:.4f} / {bs_row.OOS_MaxDD:.2%} "
      f"| 4b {'PASS' if bs_row.keep4b else bs_row.fail4b}")
    P(f"    B136 all CAGR {inc.CAGR:.2%} Sharpe {inc.Sharpe:.4f} MaxDD {inc.MaxDD:.2%} "
      f"| OOS {inc.OOS_CAGR:.2%} / {inc.OOS_Sharpe:.4f} / {inc.OOS_MaxDD:.2%} "
      f"| 4b {'PASS' if inc.keep4b else inc.fail4b}")
    P("")

    # ---------------------------------------------------------------- write
    G.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    M.drop(columns=[c for c in M.columns if c.startswith("names_")]).to_csv(
        OUT / f"{STAMP}.match.csv", index=False)
    OR.to_csv(OUT / f"{STAMP}.origin.csv", index=False)
    pd.concat([g1.assign(leg="G1_kernel_repro"), WF.assign(leg="WF-B")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    G[["char", "tau", "k", "seed", "side", "arm", "gross", "cadence", "keep4a", "fail4b",
       "keep4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"wrote grid {len(G)}, match {len(M)}, origin {len(OR)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
