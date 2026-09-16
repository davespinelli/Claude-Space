#!/usr/bin/env python3
"""Idea 1060 (lane C, 2026-09-16) — does EVERY redrawn NULL in the record need a
TURNOVER-MATCHED twin?

QUESTION (QUEUE idea 1060, verbatim)
    idea 968's C2 found a uniformly redrawn 20-name null fails four of five 4b legs at 1.000 at
    10 bps and at 0.000-0.050 at 0 bps, because it turns over 239x/yr (U56) to 321x/yr (B136) at
    daily cadence.  Census the record's committed redrawn-null claims for realised turnover
    against the books they price, and re-run the worst offenders against a turnover-matched
    null.  Max 2 params (claim set, matching rule).

THE OBJECT.  A "null" in this record is a COIN FLIP: NTOP=20 names drawn uniformly from those
    priced that day, equal weighted, same gross, same decision grid as the book it prices.  It
    is used to answer "would a monkey have done this too?".  The defect 968 exposed is that the
    coin flip does not only destroy SELECTION — it also destroys PERSISTENCE.  A book holds its
    names; the null redraws them.  Under PROTOCOL rule 2's 10 bps that difference is a CHARGE,
    not a control, and the charge is enormous at fast cadences.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER (a prediction, not a post-hoc story).
    A 20-name book that redraws uniformly from N priced names keeps, in expectation, 20*20/N of
    its names, so it trades ~2*gross*(1 - 20/N) of NAV per decision day.  On U56 (N~56) that is
    ~0.98 of the book per rebalance; at daily cadence, ~250 rebalances/yr, i.e. ~240x/yr of
    turnover against a book's 22x/yr.  At 10 bps that is ~2,400 bp/yr of drag the book never
    pays.  CONSEQUENCE, stated ahead of the numbers: on every RETURN-scaled leg (L_H1, L_H2,
    L_OOS, L_CAGR) the comparand is not a coin flip, it is a coin flip carrying a 24%/yr tax,
    and "the book beats the coin flip" on those legs is bought, not earned.  On L_DD the sign is
    not obvious a priori (churn both adds cost and de-concentrates risk), so that leg is the one
    this run cannot predict and must measure.

WHAT IS MEASURED
    (A) THE CORPUS CENSUS.  Every committed research file is parsed.  Scripts carrying a random
        name draw are classified ROTATING (the draw sits inside a per-row / per-decision loop or
        is a full (T x N) random matrix) vs FIXED (drawn once) vs AMBIG, by AST, not by grep.
        Every committed CLAIM line that cites a null is harvested and tested for whether it
        states the null's REALISED TURNOVER.  Three claim sets are reported (dial 1).
    (B) THE HANDICAP.  For the canonical redrawn null this run rebuilds bit-for-bit from 968's
        own seeds: realised annual turnover, and the ratio to the book it prices (CAND20 at the
        same cadence, gross and panel), at D / W / M / Q on both panels.
    (C) THE MATCHED TWIN (the re-run).  Four matching rules (dial 2), all reported:
          UNIF   f = 1, the record's own kind: redraw all 20 names every decision day.
          SWAP   each held name is replaced with probability f, f solved by bisection so the
                 null's realised turnover equals the book's it prices.
          HOLD   full redraw every k-th decision day, k chosen from a ladder to match the same
                 target (a SECOND mechanism for the same match, so the result is not an artifact
                 of how the match is made).
          FIXED  f = 0: draw once, hold, rebalance to equal weight on the decision grid.
        UNIF and FIXED are the f = 1 and f = 0 endpoints of the SWAP family, so the ladder is
        one continuous object and the record's kind is on it.
        The five 4b legs are then re-scored against each twin, at 10 bps and at 0 bps.
    (D) RULE 8 WALK-FORWARD at PROTOCOL's split 2016-12-31.  The matching parameter is solved on
        IS (2009-2016) turnover ALONE and the OOS window is read ONCE: OOS CAGR / Sharpe / MaxDD
        for the book against RULES v2 and SPY, BOTH KEEP paths, and the book's OOS percentile
        against each null kind — the adjudication the null choice actually moves.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported.
    (1) CLAIM SET      CS_ALL (every committed file), CS_MD (the committed prose record only),
                       CS_WORST (claims whose own script rotates AND prices at D or W cadence).
    (2) MATCHING RULE  UNIF / SWAP / HOLD / FIXED as above.

    NOT dials: the cadence ladder D/W/M/Q, the panels U56/B136, NTOP = 20, gross 0.75 and
    NSEED = 20 are 968's census POPULATION, carried over verbatim so its published null numbers
    reproduce exactly (gates G5, G6).  The 0 bps column is a DIAGNOSTIC on the comparand (968's
    C2 precedent), not a third dial: 10 bps stays the headline everywhere.

PRE-REGISTERED HYPOTHESES AND BARS (declared before any number below the gates was read)
    H_CENSUS  the record does not state the handicap: < 10% of committed null-citing claims
              state the null's realised turnover, in every claim set.
    H_GAP     the handicap is large: the redrawn null turns over >= 5x the book it prices at D
              and W, on both panels.
    H_MOVE    DECISIVE.  Turnover-matching moves the null's per-leg base rate by >= 0.25 in at
              least half of the (leg x cadence x panel) cells at 10 bps.  PASS => the record's
              null-based adjudications are turnover artifacts wherever they were read at a fast
              cadence, and every redrawn null needs a matched twin.  FAIL => the handicap is
              real but does not move the verdicts, and the record's nulls stand.
    H_ZERO    and the move is COST, not selection: at 0 bps the UNIF -> SWAP base-rate move on
              the four return-scaled legs is < 0.10 in at least 75% of cells.
    H_DD      L_DD is the exception (968's C2, idea 1061's object): the null's L_DD failure
              share stays >= 0.85 under matching in every cell at 10 bps.
    H_TWIN    the result is not an artifact of HOW the match is made: SWAP and HOLD per-leg base
              rates differ by <= 0.15 in at least 80% of cells.
    H_RULE8   with the matching parameter solved on IS alone, the book's OOS percentile against
              the null moves by >= 0.25 between UNIF and SWAP in a majority of (panel, cadence)
              cells.

REPRODUCTION GATES (printed before any hypothesis number is read)
    G1  this run's fast runner == engine.backtest on live books, returns AND turnover, at all
        four cadences.
    G2  BAND03's gross-1 weights == baseline.rules_v2_weights(px, 0.03, g)/g exactly.
    G3  CROSS-RUN: CAND20 weekly at gross 0.75 reproduces the committed KEEP-4b triple
        12.66% / 1.0921 / -18.31% inside the record's own published tolerance.
    G4  CROSS-RUN: SPY's OOS triple at 2016-12-31 == the committed 15.21% / 0.8713 / -33.72%.
    G5  CROSS-RUN: 968's published redrawn-null TURNOVER reproduces exactly (U56 D/W/M/Q
        239.004 / 49.804 / 11.501 / 3.891 x/yr; B136 D 320.780).
    G6  CROSS-RUN: 968's published redrawn-null LEG FAILURE SHARES reproduce exactly at its own
        cell (gross 0.75, 20 seeds, both panels, all four cadences).
    G7  the twins are turnover-matched: |null turnover / book turnover - 1| <= 0.05 in every
        cell, or the cell is flagged CLIPPED (the match is unreachable at f = 0) and reported.
    G8  every null kind is gross-matched: invested weight == gross on the decision grid to 1e-12.
    G9  determinism: every null rebuilds bit-for-bit off process-stable md5 seeds.
    G10 the family is continuous and contains the record's kind: SWAP at f = 1 reproduces UNIF's
        turnover to within 2%, and SWAP at f = 0 is FIXED by construction.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and
    drawdown LEVEL below is optimistic.  The measured object is a DIFFERENCE between two nulls
    drawn from the SAME survivorship-inflated panel on the SAME days, so the bias is common to
    both sides of the comparison that decides this run.  Where it does not cancel it inflates
    CAGR, which makes the MATCHED null look BETTER and therefore makes H_MOVE easier to pass —
    reported, not asserted.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import ast
import hashlib
import re
import subprocess
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-16"
SLUG = "does-EVERY-redrawn-NULL-in-the-record-need-a-TURNOVER-MATCHED-twin"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST = 10.0
LAG = 1
WARMUP = 260
NTOP = 20
MAXVOL = 0.60
BAND = 0.03
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GROSS = 0.75                      # 968's / the record's headline gross (NOT a dial here)
PANELS = ["U56", "B136"]
CADENCES = ["D", "W", "M", "Q"]
LEGS = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
RETLEGS = ["L_H1", "L_H2", "L_OOS", "L_CAGR"]
NSEED = 20

# ---- dial 2: the matching rules ---------------------------------------------------------------
RULES = ["UNIF", "SWAP", "HOLD", "FIXED"]
HOLD_LADDER = [1, 2, 3, 4, 5, 6, 8, 10, 13, 17, 21, 26, 34, 42, 55, 70, 89, 110, 144, 180, 233]

# ---- committed values this run is gated against ------------------------------------------------
CAND20_PUB = (0.1266, 1.0921, -0.1831)
G3_TOL = (5e-3, 3.3e-2, 5e-3)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
PUB_968_TURN = {("U56", "D"): 239.004162, ("U56", "W"): 49.803758, ("U56", "M"): 11.500988,
                ("U56", "Q"): 3.890670, ("B136", "D"): 320.779528, ("B136", "W"): 66.620774,
                ("B136", "M"): 15.341028, ("B136", "Q"): 5.126620}
PUB_968_NULL_LEGS = {   # 968's profile.csv, kind NULL, gross 0.75  (failure shares)
    ("U56", "D"): dict(L_H1=1.00, L_H2=1.00, L_OOS=1.00, L_DD=1.00, L_CAGR=1.00),
    ("U56", "W"): dict(L_H1=1.00, L_H2=1.00, L_OOS=1.00, L_DD=1.00, L_CAGR=1.00),
    ("U56", "M"): dict(L_H1=0.15, L_H2=0.10, L_OOS=0.05, L_DD=0.95, L_CAGR=0.10),
    ("U56", "Q"): dict(L_H1=0.00, L_H2=0.05, L_OOS=0.00, L_DD=0.85, L_CAGR=0.00),
    ("B136", "D"): dict(L_H1=1.00, L_H2=1.00, L_OOS=1.00, L_DD=1.00, L_CAGR=1.00),
    ("B136", "W"): dict(L_H1=1.00, L_H2=1.00, L_OOS=1.00, L_DD=1.00, L_CAGR=1.00),
    ("B136", "M"): dict(L_H1=0.05, L_H2=0.60, L_OOS=0.50, L_DD=1.00, L_CAGR=0.05),
    ("B136", "Q"): dict(L_H1=0.00, L_H2=0.10, L_OOS=0.10, L_DD=1.00, L_CAGR=0.00)}

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


# ====================================================================== runner (gated at G1)
def nrun(rets, wt, mk, cost=0.0):
    """Hold target weights `wt` (already lagged), rebalancing only where `mk` (already lagged) is
    True; drift in between.  Same semantics as engine.backtest — gated bit-for-bit at G1.
    Returns (returns at `cost`, turnover).  Cost is linear in turnover, so a run at cost=0 can be
    re-priced at any rung as r - turn*bps/1e4 (used throughout; identical by construction)."""
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
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
    return (held * rets).sum(axis=1) - turn * cost / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def lag(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def lagmask(m):
    out = np.zeros_like(m)
    out[LAG:] = m[:-LAG]
    return out


def blocks(r, warm, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ii = r[warm & ~oos]
    ic, is_, idd = fmet(ii)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


# ====================================================================== the books
def legs_composite(px, legs):
    parts = []
    for skip, look in legs:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech_w1(px, mech):
    """Gross-1.0 target weights.  CAND20 is the record's standing KEEP-4b construction (top-20
    equal weight, no vol scaler); BAND03 is the live RULES v2 membership book."""
    if mech == "BAND03":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, BAND), 0.0).values
    comp = legs_composite(px, [(21, 252), (0, 126), (0, 63)])
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    elig = sc.where(above & (vol20 < MAXVOL))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= NTOP).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0).values


# ====================================================================== the nulls (dial 2)
def null_unif(px, seed):
    """968's own construction, verbatim and seeded identically so its numbers reproduce: NTOP
    names drawn uniformly from those priced that day, equal weighted, redrawn EVERY row."""
    ok = px.notna().values
    T, N = ok.shape
    rng = np.random.default_rng(mdseed("NULL", seed, T, N))
    W = np.zeros((T, N))
    for i in range(T):
        idx = np.flatnonzero(ok[i])
        if len(idx) == 0:
            continue
        k = min(NTOP, len(idx))
        pick = rng.choice(idx, size=k, replace=False)
        W[i, pick] = 1.0 / k
    return W


def null_swap(px, seed, f, mask):
    """SWAP-f: on each DECISION day each held name is replaced with probability f; names that
    stop being priced are replaced regardless; the basket is refilled to NTOP and equal weighted.
    f = 1 is the record's uniform redraw, f = 0 is a fixed basket (FIXED)."""
    ok = px.notna().values
    T, N = ok.shape
    rng = np.random.default_rng(mdseed("SWAP", seed, f"{f:.8f}", T, N))
    W = np.zeros((T, N))
    held = np.zeros(N, bool)
    started = False
    for i in range(T):
        okr = ok[i]
        if not okr.any():
            continue
        if not started:
            pool = np.flatnonzero(okr)
            k = min(NTOP, len(pool))
            held[:] = False
            held[rng.choice(pool, size=k, replace=False)] = True
            started = True
        elif mask[i]:
            keep = held & okr
            if f > 0:
                kidx = np.flatnonzero(keep)
                if len(kidx):
                    keep[kidx[rng.random(len(kidx)) < f]] = False
            pool = np.flatnonzero(okr & ~keep)
            need = min(NTOP, int(okr.sum())) - int(keep.sum())
            held = keep
            if need > 0 and len(pool):
                held = keep.copy()
                held[rng.choice(pool, size=min(need, len(pool)), replace=False)] = True
        else:
            keep = held & okr
            if keep.sum() == 0:                      # every name de-listed: forced redraw
                pool = np.flatnonzero(okr)
                keep = np.zeros(N, bool)
                keep[rng.choice(pool, size=min(NTOP, len(pool)), replace=False)] = True
            held = keep
        k = int(held.sum())
        if k:
            W[i, held] = 1.0 / k
    return W


def null_hold(px, seed, k, mask):
    """HOLD-k: a FULL redraw every k-th decision day, held (and equal-weighted on the decision
    grid) in between.  A second mechanism for the same turnover match."""
    ok = px.notna().values
    T, N = ok.shape
    rng = np.random.default_rng(mdseed("HOLD", seed, k, T, N))
    W = np.zeros((T, N))
    held = np.zeros(N, bool)
    started = False
    j = 0
    for i in range(T):
        okr = ok[i]
        if not okr.any():
            continue
        redraw = not started
        if started and mask[i]:
            j += 1
            redraw = (j % k) == 0
        if redraw:
            pool = np.flatnonzero(okr)
            held = np.zeros(N, bool)
            held[rng.choice(pool, size=min(NTOP, len(pool)), replace=False)] = True
            started = True
        else:
            keep = held & okr
            if keep.sum() < min(NTOP, int(okr.sum())) and mask[i]:
                pool = np.flatnonzero(okr & ~keep)
                need = min(NTOP, int(okr.sum())) - int(keep.sum())
                if need > 0 and len(pool):
                    keep = keep.copy()
                    keep[rng.choice(pool, size=min(need, len(pool)), replace=False)] = True
            held = keep
        n = int(held.sum())
        if n:
            W[i, held] = 1.0 / n
    return W


# ====================================================================== (A) the corpus census
DRAW_FNS = {"choice", "permutation", "shuffle", "integers", "randint", "random_sample",
            "standard_normal", "normal", "sample"}
TIME_TOK = re.compile(r"\b(T|nT|len\(px|len\(idx|len\(rets|idx|index|dates?|days?|rows?|"
                      r"decision|reb|mask|mk)\b", re.I)
NULL_TOK = re.compile(r"(\bnull\b|\bnulls\b|coin[ -]?flip|random book|randomly drawn|"
                      r"\bredrawn\b|re-?drawn|\bplacebo\b|base rate|monkey)", re.I)
TURN_TOK = re.compile(r"(turnover|turn_yr|\bturns? over\b|x/ ?yr|×/ ?yr)", re.I)
NUM_TOK = re.compile(r"\d")
FAST_TOK = re.compile(r"(daily|weekly|freq\s*=\s*[\"']([DW])[\"']|cadence.*\b[DW]\b|\"D\"|'D'|"
                      r"\"W\"|'W')")


def classify_script(path):
    """AST classification of a script's random NAME DRAW: ROTATING (draw inside a per-row/
    per-decision loop, or a full (T x N) random matrix), FIXED (drawn once), AMBIG."""
    try:
        src = path.read_text(errors="replace")
    except Exception:
        return None
    if not NUM_TOK.search(src):
        return None
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    draws = []

    def walk(node, loops):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.For, ast.While)):
                try:
                    it = ast.unparse(ch.iter) if isinstance(ch, ast.For) else ast.unparse(ch.test)
                except Exception:
                    it = ""
                walk(ch, loops + [it])
                continue
            if isinstance(ch, ast.Call) and isinstance(ch.func, ast.Attribute) \
                    and ch.func.attr in DRAW_FNS:
                try:
                    txt = ast.unparse(ch)
                except Exception:
                    txt = ""
                draws.append((ch.lineno, list(loops), txt))
            walk(ch, loops)

    walk(tree, [])
    if not draws:
        return None
    rotating = False
    for _, loops, txt in draws:
        if any(TIME_TOK.search(it or "") for it in loops):
            rotating = True
        if re.search(r"(size|shape)\s*=\s*\(?\s*[A-Za-z_]*T\b", txt) or \
           re.search(r"\((\s*T\s*,\s*N\s*)\)", txt) or "px.shape" in txt:
            rotating = True
    anyloop = any(loops for _, loops, _ in draws)
    kind = "ROTATING" if rotating else ("AMBIG" if anyloop else "FIXED")
    return dict(file=str(path.relative_to(ROOT)), ndraw=len(draws), kind=kind,
                null_tok=bool(NULL_TOK.search(src)), fast=bool(FAST_TOK.search(src)),
                turn_tok=bool(TURN_TOK.search(src)), lines=src.count("\n") + 1)


def harvest_claims(files):
    """A CLAIM is a committed line that cites a null AND carries a number.  It STATES ITS
    TURNOVER if the same line, or either neighbour, also carries a turnover token with a
    number."""
    rows = []
    for p in files:
        try:
            L = p.read_text(errors="replace").split("\n")
        except Exception:
            continue
        for i, line in enumerate(L):
            if not NULL_TOK.search(line) or not re.search(r"\d+\.\d+|\d+\s?%|\bx/ ?yr", line):
                continue
            win = " ".join(L[max(0, i - 1):i + 2])
            rows.append(dict(file=str(p.relative_to(ROOT)), line=i + 1,
                             stated_turnover=bool(TURN_TOK.search(win)
                                                  and NUM_TOK.search(win)),
                             stated_same_line=bool(TURN_TOK.search(line)),
                             text=line.strip()[:240]))
    return pd.DataFrame(rows)


def main():
    t0 = time.time()
    P(f"# Idea 1060 (lane C, {DATE}) — does EVERY redrawn NULL in the record need a "
      f"TURNOVER-MATCHED twin?")
    P(f"# 2 tuned dials: CLAIM SET (CS_ALL / CS_MD / CS_WORST) x MATCHING RULE {RULES}. "
      f"ALL points reported, none selected.")
    P("# DECLARED BEFORE ANY NUMBER: a 20-name basket redrawn uniformly from N~56 priced names")
    P("#   keeps ~20*20/N of itself, so it trades ~2*gross per rebalance — ~240x/yr at daily")
    P("#   cadence against a book's ~22x/yr, i.e. ~2,400 bp/yr of drag the book never pays.  So")
    P("#   on the four RETURN-scaled legs the comparand is a coin flip carrying a 24%/yr tax.")
    P("#   On L_DD the sign is NOT predictable a priori and must be measured.")
    P(f"# Population carried over from idea 968 verbatim (NOT dials): panels {PANELS}, cadences "
      f"{CADENCES}, NTOP {NTOP}, gross {GROSS}, {NSEED} seeds/cell.")
    P("")

    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                             text=True).stdout.strip()[:12]
    except Exception:
        sha = "unknown"

    PXD = {"U56": load_universe(), "B136": load_universe(broad=True)}
    PAN = {}
    for p, px in PXD.items():
        idx = px.index
        rets = px.pct_change().fillna(0.0).values
        warm = np.arange(len(idx)) >= WARMUP
        oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
        spyr = px["SPY"].pct_change().fillna(0.0).values
        PAN[p] = dict(px=px, idx=idx, rets=rets, warm=warm, oos=oos, T=len(idx),
                      yrs=warm.sum() / 252.0,
                      isyrs=(warm & ~oos).sum() / 252.0,
                      spy=blocks(spyr, warm, oos))
        P(f"  {p}: {px.shape[1]} cols x {len(idx)} days, {idx[0].date()} -> {idx[-1].date()}; "
          f"SPY full {PAN[p]['spy']['CAGR']:.2%} / {PAN[p]['spy']['Sharpe']:.4f} / "
          f"{PAN[p]['spy']['MaxDD']:.2%}")

    W1 = {(p, m): mech_w1(PXD[p], m) for p in PANELS for m in ("CAND20", "BAND03")}
    MASK = {(p, c): rebalance_mask(PAN[p]["idx"], c).values for p in PANELS for c in CADENCES}

    def run_book(p, m, cad):
        return nrun(PAN[p]["rets"], lag(GROSS * W1[(p, m)]), lagmask(MASK[(p, cad)]))

    BOOK = {}
    for p, m, cad in product(PANELS, ("CAND20", "BAND03"), CADENCES):
        r, t = run_book(p, m, cad)
        pan = PAN[p]
        BOOK[(p, m, cad)] = dict(r=r, turn=t,
                                 turn_yr=float(t[pan["warm"]].sum() / pan["yrs"]),
                                 turn_yr_is=float(t[pan["warm"] & ~pan["oos"]].sum()
                                                  / pan["isyrs"]))

    # ================================================================== GATES
    P("=" * 100)
    P("REPRODUCTION GATES")
    P("=" * 100)
    gates = {}

    d1r = d1t = 0.0
    for m, cad in product(["CAND20", "BAND03"], CADENCES):
        px = PXD["U56"]
        w = GROSS * W1[("U56", m)]
        mine, mt = run_book("U56", m, cad)
        eng = backtest(px, pd.DataFrame(w, index=px.index, columns=px.columns),
                       cost_bps=0.0, freq=cad)
        d1r = max(d1r, float(np.abs(mine[WARMUP:] - eng["returns"].values[WARMUP:]).max()))
        d1t = max(d1t, float(np.abs(mt[WARMUP:] - eng["turnover"].values[WARMUP:]).max()))
    gates["G1"] = (d1r < 1e-12 and d1t < 1e-12,
                   f"fast runner == engine.backtest, 2 books x {len(CADENCES)} cadences: "
                   f"max|dret| {d1r:.2e}, max|dturn| {d1t:.2e}")

    d2 = float(np.abs(W1[("U56", "BAND03")]
                      - rules_v2_weights(PXD["U56"], BAND, GROSS).values / GROSS).max())
    gates["G2"] = (d2 == 0.0, f"BAND03 == rules_v2_weights/gross exactly: max|d| {d2:.2e}")

    rc = BOOK[("U56", "CAND20", "W")]["r"] - BOOK[("U56", "CAND20", "W")]["turn"] * COST / 1e4
    trip = fmet(rc[PAN["U56"]["warm"]])
    dl = [abs(trip[i] - CAND20_PUB[i]) for i in range(3)]
    gates["G3"] = (all(d <= t for d, t in zip(dl, G3_TOL)),
                   f"CROSS-RUN CAND20 weekly @{GROSS}: {trip[0]:.4%} / {trip[1]:.4f} / "
                   f"{trip[2]:.2%} vs committed 12.66% / 1.0921 / -18.31% "
                   f"(|d| {dl[0]:.4f}/{dl[1]:.4f}/{dl[2]:.4f})")

    sp = PAN["U56"]["spy"]
    d4 = max(abs(sp["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(sp["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sp["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G4"] = (d4 < 5e-4, f"CROSS-RUN SPY OOS at {IS_END}: {sp['OOS_CAGR']:.4f} / "
                              f"{sp['OOS_Sharpe']:.4f} / {sp['OOS_MaxDD']:.4f} vs committed "
                              f"{SPY_OOS_COMMITTED} (max|d| {d4:.2e})")

    # 968's null, rebuilt bit-for-bit from its own seeds (gates G5 and G6)
    NW_UNIF = {(p, s): null_unif(PXD[p], s) for p in PANELS for s in range(NSEED)}
    unif_rows = []
    for p, cad, s in product(PANELS, CADENCES, range(NSEED)):
        pan = PAN[p]
        r0, t = nrun(pan["rets"], lag(GROSS * NW_UNIF[(p, s)]), lagmask(MASK[(p, cad)]))
        unif_rows.append(dict(panel=p, cadence=cad, seed=s,
                              turn_yr=float(t[pan["warm"]].sum() / pan["yrs"]),
                              **{k: v for k, v in legs_4b(
                                  blocks(r0 - t * COST / 1e4, pan["warm"], pan["oos"]),
                                  pan["spy"]).items()}))
    UNIF = pd.DataFrame(unif_rows)
    d5 = max(abs(float(UNIF[(UNIF.panel == p) & (UNIF.cadence == c)].turn_yr.mean()) - v)
             for (p, c), v in PUB_968_TURN.items())
    gates["G5"] = (d5 < 1e-3, f"CROSS-RUN 968's redrawn-null TURNOVER at all 8 (panel, cadence) "
                              f"cells, {NSEED} seeds: max|d| {d5:.2e} x/yr (e.g. U56 D "
                              f"{float(UNIF[(UNIF.panel=='U56')&(UNIF.cadence=='D')].turn_yr.mean()):.3f}"
                              f" vs 239.004)")
    d6 = 0.0
    for (p, c), pub in PUB_968_NULL_LEGS.items():
        s = UNIF[(UNIF.panel == p) & (UNIF.cadence == c)]
        for lg, v in pub.items():
            d6 = max(d6, abs(float((~s[lg]).mean()) - v))
    gates["G6"] = (d6 < 1e-9, f"CROSS-RUN 968's redrawn-null LEG FAILURE SHARES, 8 cells x 5 "
                              f"legs: max|d share| {d6:.2e}")

    a = null_swap(PXD["U56"], 0, 0.37, MASK[("U56", "W")])
    b = null_swap(PXD["U56"], 0, 0.37, MASK[("U56", "W")])
    c_ = null_hold(PXD["U56"], 0, 5, MASK[("U56", "W")])
    d_ = null_hold(PXD["U56"], 0, 5, MASK[("U56", "W")])
    gates["G9"] = (float(np.abs(a - b).max()) == 0.0 and float(np.abs(c_ - d_).max()) == 0.0,
                   "determinism: SWAP and HOLD nulls rebuild bit-for-bit off process-stable md5 "
                   f"seeds (ref {mdseed('SWAP', 0, '0.37000000', PAN['U56']['T'], 56)})")

    # G10: the family contains the record's kind at f = 1
    g10 = []
    for p, cad in product(PANELS, CADENCES):
        pan = PAN[p]
        w1 = null_swap(PXD[p], 0, 1.0, MASK[(p, cad)])
        t1 = nrun(pan["rets"], lag(GROSS * w1), lagmask(MASK[(p, cad)]))[1]
        got = float(t1[pan["warm"]].sum() / pan["yrs"])
        ref = float(UNIF[(UNIF.panel == p) & (UNIF.cadence == cad)].turn_yr.mean())
        g10.append(abs(got / ref - 1.0))
    gates["G10"] = (max(g10) < 0.02, f"SWAP at f=1 reproduces the record's UNIF turnover in all "
                                     f"8 cells: max|ratio-1| {max(g10):.4f}; SWAP at f=0 IS "
                                     f"FIXED by construction (same code path)")

    # ================================================================== (A) THE CORPUS CENSUS
    P("=" * 100)
    P("(A) THE CORPUS CENSUS — dial 1 (CLAIM SET), all three values reported")
    P("=" * 100)
    pyfiles = sorted((ROOT / "research").rglob("*.py"))
    mdfiles = sorted((ROOT / "research").rglob("*.md"))
    P(f"  corpus at git {sha}: {len(pyfiles):,} committed .py and {len(mdfiles):,} .md files "
      f"under research/.")
    cen = [c for c in (classify_script(p) for p in pyfiles) if c]
    CEN = pd.DataFrame(cen)
    dump(CEN, "census")
    nullscripts = CEN[CEN.null_tok]
    P(f"  {len(CEN):,} scripts carry a random draw; {len(nullscripts):,} of them also use null / "
      f"coin-flip language (the record's NULL SCRIPTS).")
    kc = nullscripts.kind.value_counts().to_dict()
    P(f"  null-script kind (AST, not grep): " + ", ".join(f"{k} {v}" for k, v in
                                                          sorted(kc.items())))
    rot = nullscripts[nullscripts.kind == "ROTATING"]
    P(f"  ROTATING null scripts: {len(rot):,}; of those {int(rot.fast.sum()):,} also price at a "
      f"D or W cadence (the WORST OFFENDERS by the arithmetic declared above).")
    P(f"  ROTATING null scripts that mention turnover ANYWHERE in the file at all: "
      f"{int(rot.turn_tok.sum()):,} of {len(rot):,} ({rot.turn_tok.mean():.1%}) — a LOOSE upper "
      f"bound on how many price their own null's churn.")

    CLAIMS = harvest_claims(mdfiles + pyfiles)
    CLAIMS["is_md"] = CLAIMS.file.str.endswith(".md")
    rotstems = {Path(f).stem.replace("_C", "").replace("_B", "").replace("_cloud", "")
                for f in rot[rot.fast].file}
    CLAIMS["worst"] = [Path(f).stem.replace(".result", "").replace(".memo", "")
                       .replace("_C", "").replace("_B", "").replace("_cloud", "") in rotstems
                       for f in CLAIMS.file]
    dump(CLAIMS, "claims")
    sets = {"CS_ALL": CLAIMS, "CS_MD": CLAIMS[CLAIMS.is_md], "CS_WORST": CLAIMS[CLAIMS.worst]}
    crows = []
    for name, s in sets.items():
        crows.append(dict(claim_set=name, n=len(s),
                          stated_turnover=float(s.stated_turnover.mean()) if len(s) else np.nan,
                          stated_same_line=float(s.stated_same_line.mean()) if len(s) else np.nan,
                          n_files=int(s.file.nunique())))
        P(f"  {name}: {len(s):,} committed null-citing claims in {s.file.nunique():,} files; "
          f"{s.stated_turnover.mean():.1%} state the null's realised turnover within +/-1 line "
          f"({s.stated_same_line.mean():.1%} on the claim line itself).")
    CSET = pd.DataFrame(crows)
    dump(CSET, "claimsets")
    P("")

    # ================================================================== (B) THE HANDICAP
    P("=" * 100)
    P("(B) THE HANDICAP — the record's redrawn null against the book it prices")
    P("=" * 100)
    hrows = []
    for p, cad in product(PANELS, CADENCES):
        nt = float(UNIF[(UNIF.panel == p) & (UNIF.cadence == cad)].turn_yr.mean())
        bt = BOOK[(p, "CAND20", cad)]["turn_yr"]
        lt = BOOK[(p, "BAND03", cad)]["turn_yr"]
        hrows.append(dict(panel=p, cadence=cad, null_turn_yr=nt, book_turn_yr=bt,
                          live_turn_yr=lt, ratio=nt / bt,
                          excess_drag_bp=(nt - bt) * COST))
    HAND = pd.DataFrame(hrows)
    dump(HAND, "handicap")
    for line in HAND.to_string(index=False, float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)
    P("")

    # ================================================================== (C) THE MATCHED TWINS
    P("=" * 100)
    P("(C) THE MATCHED TWINS — dial 2 (MATCHING RULE), all four values reported")
    P("=" * 100)

    def turn_of(W, p, cad, window=None):
        pan = PAN[p]
        t = nrun(pan["rets"], lag(GROSS * W), lagmask(MASK[(p, cad)]))[1]
        w = pan["warm"] if window is None else window
        yrs = w.sum() / 252.0
        return float(t[w].sum() / yrs)

    def solve_f(p, cad, target, window=None, seed=0):
        """Bisection on f in [0,1]; turnover is monotone increasing in f."""
        lo, hi = 0.0, 1.0
        tlo = turn_of(null_swap(PXD[p], seed, lo, MASK[(p, cad)]), p, cad, window)
        thi = turn_of(null_swap(PXD[p], seed, hi, MASK[(p, cad)]), p, cad, window)
        if target <= tlo:
            return 0.0, tlo, True
        if target >= thi:
            return 1.0, thi, True
        for _ in range(16):
            mid = 0.5 * (lo + hi)
            tm = turn_of(null_swap(PXD[p], seed, mid, MASK[(p, cad)]), p, cad, window)
            if tm < target:
                lo, tlo = mid, tm
            else:
                hi, thi = mid, tm
        f = 0.5 * (lo + hi)
        return f, turn_of(null_swap(PXD[p], seed, f, MASK[(p, cad)]), p, cad, window), False

    def solve_k(p, cad, target, window=None, seed=0):
        best = None
        for k in HOLD_LADDER:
            t = turn_of(null_hold(PXD[p], seed, k, MASK[(p, cad)]), p, cad, window)
            if best is None or abs(t - target) < abs(best[1] - target):
                best = (k, t)
            if t < target:
                break
        return best[0], best[1], abs(best[1] / target - 1.0) > 0.05

    MATCH = {}
    mrows = []
    for p, cad in product(PANELS, CADENCES):
        tgt = BOOK[(p, "CAND20", cad)]["turn_yr"]
        f, tf, fclip = solve_f(p, cad, tgt)
        k, tk, kclip = solve_k(p, cad, tgt)
        tgt_is = BOOK[(p, "CAND20", cad)]["turn_yr_is"]
        iswin = PAN[p]["warm"] & ~PAN[p]["oos"]
        f_is, tf_is, _ = solve_f(p, cad, tgt_is, window=iswin)
        k_is, tk_is, _ = solve_k(p, cad, tgt_is, window=iswin)
        MATCH[(p, cad)] = dict(f=f, k=k, f_is=f_is, k_is=k_is)
        mrows.append(dict(panel=p, cadence=cad, target_turn_yr=tgt, swap_f=f, swap_turn_yr=tf,
                          swap_err=tf / tgt - 1.0, swap_clipped=fclip, hold_k=k,
                          hold_turn_yr=tk, hold_err=tk / tgt - 1.0, hold_clipped=kclip,
                          IS_target=tgt_is, IS_swap_f=f_is, IS_hold_k=k_is))
        P(f"    {p:5s} {cad}  book {tgt:8.3f} x/yr -> SWAP f={f:.4f} ({tf:8.3f}, "
          f"{tf/tgt-1:+.1%}){' CLIPPED' if fclip else ''}   HOLD k={k:3d} ({tk:8.3f}, "
          f"{tk/tgt-1:+.1%}){' CLIPPED' if kclip else ''}   [IS-only: f={f_is:.4f}, k={k_is}]")
    MT = pd.DataFrame(mrows)
    dump(MT, "match")
    worst_err = float(np.nanmax(np.abs(MT[["swap_err", "hold_err"]].values)))
    nclip = int(MT.swap_clipped.sum() + MT.hold_clipped.sum())
    gates["G7"] = (worst_err <= 0.05 or nclip > 0,
                   f"turnover match: max|null/book - 1| {worst_err:.3f} over "
                   f"{len(MT)*2} matched cells; {nclip} cell(s) CLIPPED (match unreachable) and "
                   f"flagged in the table")
    P("")

    # ---- build every null kind and score the five legs -------------------------------------
    NRUN = []
    for p, cad, rule, s in product(PANELS, CADENCES, RULES, range(NSEED)):
        pan = PAN[p]
        m = MATCH[(p, cad)]
        if rule == "UNIF":
            W = NW_UNIF[(p, s)]
        elif rule == "SWAP":
            W = null_swap(PXD[p], s, m["f"], MASK[(p, cad)])
        elif rule == "HOLD":
            W = null_hold(PXD[p], s, m["k"], MASK[(p, cad)])
        else:
            W = null_swap(PXD[p], s, 0.0, MASK[(p, cad)])
        r0, t = nrun(pan["rets"], lag(GROSS * W), lagmask(MASK[(p, cad)]))
        row = dict(panel=p, cadence=cad, rule=rule, seed=s,
                   turn_yr=float(t[pan["warm"]].sum() / pan["yrs"]))
        for cost in (0.0, COST):
            b = blocks(r0 - t * cost / 1e4, pan["warm"], pan["oos"])
            lg = legs_4b(b, pan["spy"])
            tag = "c0" if cost == 0 else "c10"
            row.update({f"{tag}_{k}": v for k, v in lg.items()})
            row[f"{tag}_pass4b"] = all(lg.values())
            row[f"{tag}_CAGR"] = b["CAGR"]
            row[f"{tag}_Sharpe"] = b["Sharpe"]
            row[f"{tag}_MaxDD"] = b["MaxDD"]
            row[f"{tag}_OOS_Sharpe"] = b["OOS_Sharpe"]
        NRUN.append(row)
    NR = pd.DataFrame(NRUN)
    dump(NR, "nulls")

    # G8 gross match
    d8 = 0.0
    for p, cad, rule in product(PANELS, CADENCES, RULES):
        m = MATCH[(p, cad)]
        W = (NW_UNIF[(p, 0)] if rule == "UNIF" else
             null_swap(PXD[p], 0, m["f"] if rule == "SWAP" else 0.0, MASK[(p, cad)])
             if rule in ("SWAP", "FIXED") else null_hold(PXD[p], 0, m["k"], MASK[(p, cad)]))
        inv = (GROSS * W)[MASK[(p, cad)] & PAN[p]["warm"]].sum(axis=1)
        d8 = max(d8, float(np.abs(inv - GROSS).max()))
    gates["G8"] = (d8 < 1e-12, f"every null kind is gross-matched on the decision grid: "
                               f"max|invested - {GROSS}| = {d8:.2e}")

    for k in sorted(gates, key=lambda s: int(s[1:])):
        ok, msg = gates[k]
        P(f"  {k} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"GATES: {sum(1 for v in gates.values() if v[0])} of {len(gates)} pass.")
    P("")

    prof = []
    for p, cad, rule in product(PANELS, CADENCES, RULES):
        s = NR[(NR.panel == p) & (NR.cadence == cad) & (NR.rule == rule)]
        row = dict(panel=p, cadence=cad, rule=rule, n=len(s), turn_yr=float(s.turn_yr.mean()))
        for tag in ("c0", "c10"):
            for lg in LEGS:
                row[f"{tag}_{lg}"] = float((~s[f"{tag}_{lg}"]).mean())   # FAILURE share
            row[f"{tag}_pass4b"] = float(s[f"{tag}_pass4b"].mean())
            row[f"{tag}_CAGR"] = float(s[f"{tag}_CAGR"].mean())
            row[f"{tag}_MaxDD"] = float(s[f"{tag}_MaxDD"].mean())
        prof.append(row)
    PR = pd.DataFrame(prof)
    dump(PR, "profile")
    P("  NULL LEG FAILURE SHARES at PROTOCOL's 10 bps (the share of coin flips that FAIL each")
    P("  4b leg; 1.000 means the leg is free for any book):")
    cols = ["panel", "cadence", "rule", "turn_yr"] + [f"c10_{lg}" for lg in LEGS] + ["c10_pass4b"]
    for line in PR[cols].to_string(index=False,
                                   float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)
    P("")
    P("  the same cells at 0 bps (the DIAGNOSTIC — what is left when the tax is removed):")
    cols0 = ["panel", "cadence", "rule"] + [f"c0_{lg}" for lg in LEGS] + ["c0_pass4b"]
    for line in PR[cols0].to_string(index=False,
                                    float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)
    P("")

    # ---- the move: UNIF -> matched, leg by leg ---------------------------------------------
    mv = []
    for p, cad, lg, tag in product(PANELS, CADENCES, LEGS, ("c0", "c10")):
        u = float(PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == "UNIF")]
                  [f"{tag}_{lg}"].iloc[0])
        for rule in ("SWAP", "HOLD", "FIXED"):
            v = float(PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == rule)]
                      [f"{tag}_{lg}"].iloc[0])
            mv.append(dict(panel=p, cadence=cad, leg=lg, cost=tag, rule=rule, unif=u, matched=v,
                           move=v - u, big=abs(v - u) >= 0.25))
    MV = pd.DataFrame(mv)
    dump(MV, "moves")
    m10 = MV[(MV.cost == "c10") & (MV.rule == "SWAP")]
    P(f"  UNIF -> SWAP (turnover-matched) at 10 bps: {int(m10.big.sum())} of {len(m10)} "
      f"(leg x cadence x panel) cells move by >= 0.25; mean |move| {m10.move.abs().mean():.3f}, "
      f"max {m10.move.abs().max():.3f}.")
    for line in m10.pivot_table(index=["panel", "cadence"], columns="leg",
                                values="move")[LEGS].to_string(
            float_format=lambda x: f"{x:+.3f}").split("\n"):
        P("    " + line)
    P("")

    # ================================================================== (D) RULE 8
    P("=" * 100)
    P("(D) RULE 8 WALK-FORWARD — matching parameter solved on IS (2009-2016) ALONE, OOS read ONCE")
    P("=" * 100)
    r8 = []
    for p, cad in product(PANELS, CADENCES):
        pan = PAN[p]
        m = MATCH[(p, cad)]
        bk = BOOK[(p, "CAND20", cad)]
        br = bk["r"] - bk["turn"] * COST / 1e4
        bb = blocks(br, pan["warm"], pan["oos"])
        lv = BOOK[(p, "BAND03", cad)]
        lvb = blocks(lv["r"] - lv["turn"] * COST / 1e4, pan["warm"], pan["oos"])
        lvW = BOOK[(p, "BAND03", "W")]
        lvWb = blocks(lvW["r"] - lvW["turn"] * COST / 1e4, pan["warm"], pan["oos"])
        spy = pan["spy"]
        lg = legs_4b(bb, spy)
        keep4b = all(lg.values())
        keep4a = (bb["H1"] > lvWb["H1"] and bb["H2"] > lvWb["H2"]
                  and bb["MaxDD"] >= lvWb["MaxDD"])
        row = dict(panel=p, cadence=cad, book="CAND20",
                   CAGR=bb["CAGR"], Sharpe=bb["Sharpe"], MaxDD=bb["MaxDD"],
                   H1=bb["H1"], H2=bb["H2"],
                   OOS_CAGR=bb["OOS_CAGR"], OOS_Sharpe=bb["OOS_Sharpe"], OOS_MaxDD=bb["OOS_MaxDD"],
                   SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                   SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                   V2_OOS_CAGR=lvWb["OOS_CAGR"], V2_OOS_Sharpe=lvWb["OOS_Sharpe"],
                   V2_OOS_MaxDD=lvWb["OOS_MaxDD"],
                   keep4a=keep4a, keep4b=keep4b, **lg)
        for rule in RULES:
            os_ = []
            for s in range(NSEED):
                if rule == "UNIF":
                    W = NW_UNIF[(p, s)]
                elif rule == "SWAP":
                    W = null_swap(PXD[p], s, m["f_is"], MASK[(p, cad)])
                elif rule == "HOLD":
                    W = null_hold(PXD[p], s, m["k_is"], MASK[(p, cad)])
                else:
                    W = null_swap(PXD[p], s, 0.0, MASK[(p, cad)])
                r0, t = nrun(pan["rets"], lag(GROSS * W), lagmask(MASK[(p, cad)]))
                os_.append(blocks(r0 - t * COST / 1e4, pan["warm"], pan["oos"])["OOS_Sharpe"])
            os_ = np.array(os_, float)
            row[f"pct_{rule}"] = float((os_ < bb["OOS_Sharpe"]).mean())
            row[f"nullOOS_{rule}"] = float(np.median(os_))
        r8.append(row)
    R8 = pd.DataFrame(r8)
    dump(R8, "rule8")
    P("  the BOOK (CAND20 top-20 equal weight, gross 0.75), OOS 2017- read once, vs RULES v2 "
      "(live, weekly) and SPY:")
    show = ["panel", "cadence", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "V2_OOS_Sharpe", "SPY_OOS_Sharpe", "keep4a", "keep4b"]
    for line in R8[show].to_string(index=False, float_format=lambda x: f"{x:.4f}").split("\n"):
        P("    " + line)
    P("")
    P("  the ADJUDICATION the null choice moves — the book's OOS percentile against its null:")
    pcols = ["panel", "cadence"] + [f"pct_{r}" for r in RULES] + [f"nullOOS_{r}" for r in RULES]
    for line in R8[pcols].to_string(index=False, float_format=lambda x: f"{x:.3f}").split("\n"):
        P("    " + line)
    R8["pct_move"] = (R8.pct_SWAP - R8.pct_UNIF).abs()
    P(f"  |percentile(SWAP) - percentile(UNIF)| >= 0.25 in {int((R8.pct_move>=0.25).sum())} of "
      f"{len(R8)} (panel x cadence) cells; mean move {R8.pct_move.mean():.3f}.")
    P("")

    # ================================================================== HYPOTHESES
    P("=" * 100)
    P("PRE-REGISTERED HYPOTHESES (bars fixed before any number above the gates was read)")
    P("=" * 100)
    H = {}
    worst_share = float(CSET.stated_turnover.max())
    H["H_CENSUS"] = (worst_share < 0.10,
                     "stated-turnover share by claim set: " + ", ".join(
                         f"{r.claim_set} {r.stated_turnover:.1%} (n={r.n:,})"
                         for r in CSET.itertuples()) + "  < 10% in every set?")
    fast = HAND[HAND.cadence.isin(["D", "W"])]
    H["H_GAP"] = (bool((fast.ratio >= 5).all()),
                  "null/book turnover ratio at D and W: " + ", ".join(
                      f"{r.panel}/{r.cadence} {r.ratio:.1f}x" for r in fast.itertuples())
                  + "  >= 5x everywhere?  (M/Q: " + ", ".join(
                      f"{r.panel}/{r.cadence} {r.ratio:.1f}x"
                      for r in HAND[HAND.cadence.isin(['M', 'Q'])].itertuples()) + ")")
    share_big = float(m10.big.mean())
    H["H_MOVE"] = (share_big >= 0.50,
                   f"DECISIVE: UNIF -> turnover-matched moves the null's leg base rate by "
                   f">= 0.25 in {int(m10.big.sum())} of {len(m10)} cells ({share_big:.1%}) at "
                   f"10 bps; bar 50%")
    z = MV[(MV.cost == "c0") & (MV.rule == "SWAP") & (MV.leg.isin(RETLEGS))]
    small0 = float((z.move.abs() < 0.10).mean())
    H["H_ZERO"] = (small0 >= 0.75,
                   f"at 0 bps the same move on the four return-scaled legs is < 0.10 in "
                   f"{int((z.move.abs()<0.10).sum())} of {len(z)} cells ({small0:.1%}); bar 75% "
                   f"— i.e. the move is COST, not selection")
    dd10 = PR[PR.rule.isin(["SWAP", "HOLD", "FIXED"])].c10_L_DD
    H["H_DD"] = (bool((dd10 >= 0.85).all()),
                 f"L_DD failure share under matching stays >= 0.85 in every cell: range "
                 f"{dd10.min():.3f}..{dd10.max():.3f}")
    tw = []
    for p, cad, lg in product(PANELS, CADENCES, LEGS):
        a_ = float(PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == "SWAP")]
                   [f"c10_{lg}"].iloc[0])
        b_ = float(PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == "HOLD")]
                   [f"c10_{lg}"].iloc[0])
        tw.append(abs(a_ - b_))
    tw = np.array(tw)
    H["H_TWIN"] = (float((tw <= 0.15).mean()) >= 0.80,
                   f"SWAP vs HOLD (two mechanisms, same target) agree within 0.15 in "
                   f"{int((tw<=0.15).sum())} of {len(tw)} cells ({(tw<=0.15).mean():.1%}); "
                   f"max gap {tw.max():.3f}; bar 80%")
    H["H_RULE8"] = (bool((R8.pct_move >= 0.25).mean() > 0.5),
                    f"IS-chosen matching moves the book's OOS percentile by >= 0.25 in "
                    f"{int((R8.pct_move>=0.25).sum())} of {len(R8)} cells; mean move "
                    f"{R8.pct_move.mean():.3f}")
    for k, (ok, msg) in H.items():
        P(f"  {k:9s} {'PASS' if ok else 'FAIL'}  {msg}")
    P(f"HYPOTHESES: {sum(1 for v in H.values() if v[0])} of {len(H)} pass.")
    P("")

    P("=" * 100)
    P("THE ANSWER TO THE QUEUE'S QUESTION")
    P("=" * 100)
    for p in PANELS:
        for cad in CADENCES:
            u = PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == "UNIF")]
            s = PR[(PR.panel == p) & (PR.cadence == cad) & (PR.rule == "SWAP")]
            P(f"  {p:5s} {cad}: null turnover {float(u.turn_yr.iloc[0]):8.2f} -> "
              f"{float(s.turn_yr.iloc[0]):7.2f} x/yr (book "
              f"{float(HAND[(HAND.panel==p)&(HAND.cadence==cad)].book_turn_yr.iloc[0]):6.2f});  "
              f"leg failure share UNIF " + "/".join(f"{float(u[f'c10_{lg}'].iloc[0]):.2f}"
                                                    for lg in LEGS)
              + "  ->  MATCHED " + "/".join(f"{float(s[f'c10_{lg}'].iloc[0]):.2f}" for lg in LEGS)
              + f"   (legs {'/'.join(l.replace('L_','') for l in LEGS)})")
    P(f"  Runtime {time.time()-t0:.1f}s.")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return dict(gates=gates, H=H, PR=PR, HAND=HAND, CSET=CSET, R8=R8, MT=MT, MV=MV)


if __name__ == "__main__":
    main()
