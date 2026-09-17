#!/usr/bin/env python3
"""Idea 1174 (lane C, 2026-09-17) — how many committed H-AXIS claims rest on the THREE-POINT
LADDER {21, 63, 126}?

QUESTION (QUEUE idea 1174, verbatim)
    idea 1093 overturned two of 1086's headlines (the B136 hump, and 'monotone is a B136
    property') purely by putting four more rungs on the hold axis, and recovered a smooth argmax
    path the 3-point ladder read as non-monotone.  Census the record's committed H-axis claims
    for how many were measured at exactly {21, 63, 126} and re-price the cheapest of them on a
    finer ladder.  Max 2 params (claim set, ladder spacing).

THE TWO TUNED DIALS (PROTOCOL rule 4, no more than two — and the queue names both)
    1. CLAIM SET   {C_STRICT, C_PROX, C_ALL}
       C_STRICT — the unit carries an H-AXIS token AND a LADDER-SHAPE verb AND names >= 2
                  distinct H rungs: a ladder claim proper, the population the queue means.
       C_PROX   — H-AXIS token and shape verb within a +/-240-character window of each other,
                  >= 1 rung named.  The loose-attachment reading (1098/1149's PROX convention).
       C_ALL    — any unit carrying an H-AXIS token and >= 1 rung, shape verb or not.  The
                  widest reading; an upper bound on the population.
    2. LADDER SPACING  {L3, L7, LFINE}, STRICTLY NESTED L3 < L7 < LFINE, SAME RANGE [21, 126]
       L3    = [21, 63, 126]                                 — the record's three-point ladder
       L7    = [21, 42, 52, 63, 76, 90, 126]                 — 1093's ladder, UNCHANGED
       LFINE = L7 + [26, 32, 37, 47, 57, 69, 83, 105, 115]   — 16 rungs
       The range is held FIXED at [21, 126] on purpose.  Extending the axis past 126 would
       confound SPACING with RANGE, and then a moved argmax would say nothing about resolution.
    3 x 3 = 9 cells, EVERY ONE PUBLISHED in `.census.csv` and `.ladder.csv`.

NOT DIALS, reported at every value: PANEL {U56, B136}; N in {5, 8, 10, 12, 15, 20, 25, 30, 40}
    (1082/1086/1093's committed N ladder); the four claim statistics {Sharpe, CAGR, MaxDD,
    turnover}; the 4a/4b legs; the five rule-8 choosers.  2 x 9 x 16 = 288 books, all published.
    Everything else is FROZEN at 936/1071/1082/1086/1093's construction: cap INF, CAND20 legs
    (21/252, 0/126, 0/63), max_vol 0.60, gross 0.75, W cadence, 10 bps, LAG 1, warm-up 260.

WHY THIS IS THE CHEAPEST CLAIM TO RE-PRICE, SAID BEFORE THE CENSUS RUNS
    The queue says "re-price the cheapest of them".  CHEAPEST is defined here as a re-pricing
    COST CLASS assigned to every harvested claim from its own text, and published as a census
    column, so the choice is a MEASUREMENT and not a convenience:
        P_BOOK — the claim's statistic is a BOOK metric on the H axis (Sharpe, CAGR, MaxDD,
                 turnover).  Re-pricing costs one book build per rung.  CHEAPEST.
        P_NULL — the statistic is an EDGE / null-median object: 40 seeded null books per rung.
        P_BOOT — the statistic carries a bootstrap / resample band.
        P_TAPE — the statistic needs a synthetic (IID / block / factor) tape.
    Arm B re-prices the P_BOOK family and ONLY the P_BOOK family, at every (panel, N).

A DEFECT THIS RUN FOUND IN ITSELF AND DID NOT HIDE
    The first cut matched the bare-letter H forms (`H=63`, `H in {...}`) CASE-INSENSITIVELY and
    swept in `h=1` — idea 125's event-study forward horizon — and `h=8%/yr` — idea 54's delisting
    HAZARD — as if they were hold rungs.  They are different objects that share a letter.  The
    bare-letter forms are now case-SENSITIVE; the WORD forms ("hold", "min hold", "holding
    period") stay case-insensitive.  G11 proves the repair only ever REMOVES units, and the
    console prints how many, so the pre-repair population is recoverable from this file.

DECLARED BEFORE ANY NUMBER — the four outcomes, so none can be read off the numbers afterwards.
    Scored on the HEADLINE statistic (Sharpe), over the 18 (panel, N) families, comparing each
    family's L3 READING to its LFINE reading.  A READING is the pair (argmax rung, monotone
    verdict); it is OVERTURNED when either component changes.
    (A) THE 3-POINT LADDER IS LOAD-BEARING : overturned at >= 9 of 18 families.
    (B) THE 3-POINT LADDER IS INNOCUOUS    : overturned at <= 4 of 18.
    (C) MIXED                              : 5..8 of 18.
    (D) NOT RESOLVABLE                     : LFINE's own argmax is not stable between L7 and
        LFINE at >= 12 of 18, i.e. the finer ladder has not converged either and neither
        reading is a measurement.  (D) is checked FIRST and overrides (A)/(B)/(C).
    A LADDER READING IS NOT A KEEP PATH.  4a and 4b are scored at all 288 cells and rule 8
    picks (N, H) on 2009-2016 alone, reading 2017-2026 ONCE, with the LADDER ITSELF as the
    chooser's constraint: C_L3 may only pick rungs in L3, C_LFINE may pick any.  That is the
    capital question this idea actually poses — does buying resolution on the hold axis buy
    out-of-sample Sharpe, or only a tidier chart?

SURVIVORSHIP (PROTOCOL rule 9).  U56 (research/universe.json) and B136
    (research/universe_broad.json) are CURRENT-CONSTITUENT lists.  Every CAGR and drawdown LEVEL
    below is optimistic and every 4a/4b count is an UPPER bound.  The census arm is a scan of
    committed text and carries no market bias at all.  The bias very largely cancels out of a
    ladder READING, which ranks one construction against itself on one tape — but it does NOT
    cancel out of the rule-8 OOS levels, and those are stated as upper bounds.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "how-many-committed-H-AXIS-claims-rest-on-the-THREE-POINT-LADDER-21-63-126"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
BT = ROOT / "research" / "backtests"

# ---- frozen construction (NOT dials) -------------------------------------------------------
LAG = 1
WARMUP = 260
MAXVOL = 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
GROSS0 = 0.75
FREQ = "W"
LEGS = [(21, 252), (0, 126), (0, 63)]
CAPNAME = "INF"
NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
PANELS = ["U56", "B136"]

# ---- dial 2: the ladder spacings, strictly nested, same range ------------------------------
L3 = [21, 63, 126]
L7 = [21, 42, 52, 63, 76, 90, 126]
LFINE = sorted(set(L7) | {26, 32, 37, 47, 57, 69, 83, 105, 115})
LADDERS = {"L3": L3, "L7": L7, "LFINE": LFINE}
HS = LFINE                                        # the grid is built once, on the finest rung set
STATS = ["Sharpe", "CAGR", "MaxDD", "turnover"]

# ---- dial 1: the claim sets ----------------------------------------------------------------
CLAIM_SETS = ["C_STRICT", "C_PROX", "C_ALL"]
PROX_W = 240                                      # the PROX attachment window, in characters

# committed cross-run anchors (ideas 936 / 1071 / 1082 / 1086 / 1093 / 1018+1023)
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
G1093 = BT / ("2026-09-17_is-the-B136-H63-MONOTONE-LADDER-a-GENUINE-SLOPE-or-the-"
              "MIDDLE-RUNG-of-a-NON-MONOTONE-H-DIAL_C.grid.csv")
B1093 = BT / ("2026-09-17_is-the-B136-H63-MONOTONE-LADDER-a-GENUINE-SLOPE-or-the-"
              "MIDDLE-RUNG-of-a-NON-MONOTONE-H-DIAL_C.benchmarks.csv")

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ============================================================================ ARM A: the census
# An H-AXIS token: the record writes the hold axis as `H=63`, `H 63`, "min hold", "hold ladder",
# "holding period", "the H dial", "H-axis".  `N=` and `n=` are deliberately NOT H tokens.
#
# THE BARE-LETTER FORMS ARE CASE-SENSITIVE, AND THIS IS A CORRECTION THIS RUN FOUND IN ITSELF.
# The first cut matched them case-insensitively and swept in `h=1` (idea 125's event-study
# forward horizon) and `h=8%/yr` (idea 54's delisting HAZARD) — different objects that happen to
# share a letter.  Capital `H` is the record's min-hold axis; lower-case `h` is not, so the bare
# forms below carry no re.I while the WORD forms ("hold", "min hold", "holding period") keep it.
HTOK_CS = re.compile(r"\bH\s*=\s*\d+|\bH\s+in\b|\bH-?\s*(?:axis|dial|ladder|rung|rungs)\b")
HTOK_CI = re.compile(
    r"\bmin(?:imum)?[- ]hold\b|\bhold(?:ing)?[- ](?:period|length|ladder|axis|rung|rungs)\b"
    r"|\bhold\s*=\s*\d+", re.I)


class _HTok:
    """H-axis token: case-SENSITIVE bare-letter forms, case-insensitive word forms."""

    @staticmethod
    def search(t):
        return HTOK_CS.search(t) or HTOK_CI.search(t)

    @staticmethod
    def finditer(t):
        return sorted(list(HTOK_CS.finditer(t)) + list(HTOK_CI.finditer(t)),
                      key=lambda m: m.start())


HTOK_RX = _HTok
# a LADDER-SHAPE verb: the claim asserts something about the SHAPE of the H curve
SHAPE_RX = re.compile(
    r"\bmonoton\w*\b|\bnon-?monoton\w*\b|\bargmax\b|\bpeak\w*\b|\bhump\w*\b|\binterior\b"
    r"|\bboundary\b|\brises?\b|\brising\b|\bfalls?\b|\bfalling\b|\bdecreas\w*\b|\bincreas\w*\b"
    r"|\bbest\b|\boptim\w*\b|\bbetween\b|\bflat\b|\bslope\b|\bladder\b|\bU-?shape\w*\b"
    r"|\bmiddle\s+rung\b|\bleft\s+end\b|\bright\s+end\b", re.I)
# an H RUNG: a number ATTACHED to an H token, never a bare integer anywhere in the sentence.
# Case-sensitive on the bare `H` forms for the reason given above; the `hold = n` form keeps re.I.
RUNG_CS = re.compile(r"(?:\bH\s*=\s*|\bH\s+)(\d{1,3})\b|\bH\s+in\s*\{([0-9,\s]+)\}")
RUNG_CI = re.compile(r"\bhold\s*=\s*(\d{1,3})\b|\bhold(?:s)?\s+(?:in\s*)?\{([0-9,\s]+)\}", re.I)
# the PRE-REPAIR reading, kept so the repair can be PRICED (gate G11) instead of just asserted
RUNG_LOOSE = re.compile(RUNG_CS.pattern, re.I)
HTOK_LOOSE = re.compile(HTOK_CS.pattern, re.I)
# re-pricing COST CLASS, read off the claim's own text (cheapest wins ties downward)
TAPE_RX = re.compile(r"\bsynthetic\s+tape\b|\bT_IID\b|\bT_BLOCK\b|\bT_FACTOR\b|\bcontrolled\s+tape\b", re.I)
BOOT_RX = re.compile(r"\bbootstrap\w*\b|\bresampl\w*\b|\bP_boot\b|\b90%\s+band\b|\bdraws\b", re.I)
NULL_RX = re.compile(r"\bEDGE\b|\bnull\b|\bnulls\b|\bDD-?matched\b|\bseed(?:s|ed)?\b", re.I)
BOOKSTAT_RX = re.compile(r"\bSharpe\b|\bCAGR\b|\bMaxDD\b|\bdrawdown\b|\bturnover\b", re.I)

RUNGS_3 = frozenset(L3)


def corpus():
    """Every COMMITTED text unit in the record: LEADERBOARD rows, CHANGELOG paragraphs, and the
    paragraphs of every research/backtests/*.result.md.  Read verbatim off HEAD."""
    units = []
    lb = [l for l in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n")
          if l.startswith("|") and not l.startswith("|---")]
    units += [("LEADERBOARD", str(i), t) for i, t in enumerate(lb[1:])]
    cl = [p for p in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n")
          if p.strip()]
    units += [("CHANGELOG", str(i), t) for i, t in enumerate(cl)]
    nfiles = 0
    for f in sorted(BT.glob("*.result.md")):
        nfiles += 1
        ps = [p for p in f.read_text(errors="ignore").split("\n\n") if p.strip()]
        units += [("RESULTMD", f"{f.stem}#{i}", t) for i, t in enumerate(ps)]
    return units, nfiles


def rungs_in(t):
    """The set of H rungs a unit NAMES, only ever through an H token — never a bare integer."""
    out = set()
    for rx in (RUNG_CS, RUNG_CI):
        for m in rx.finditer(t):
            if m.group(1):
                out.add(int(m.group(1)))
            if m.group(2):
                for x in re.findall(r"\d{1,3}", m.group(2)):
                    out.add(int(x))
    return {r for r in out if 1 <= r <= 512}


def cost_class(t):
    if TAPE_RX.search(t):
        return "P_TAPE"
    if BOOT_RX.search(t):
        return "P_BOOT"
    if NULL_RX.search(t):
        return "P_NULL"
    if BOOKSTAT_RX.search(t):
        return "P_BOOK"
    return "P_OTHER"


def prox_hit(t):
    """H token and shape verb within PROX_W characters of each other."""
    hs = [m.start() for m in HTOK_RX.finditer(t)]
    ss = [m.start() for m in SHAPE_RX.finditer(t)]
    if not hs or not ss:
        return False
    return min(abs(a - b) for a in hs for b in ss) <= PROX_W


def harvest_loose(units):
    """The PRE-REPAIR population: bare-letter H forms matched case-INSENSITIVELY, so `h=1` and
    `h=8%/yr` count as hold rungs.  Kept only so G11 can price what the repair removes."""
    out = set()
    for src, uid, t in units:
        if not (HTOK_LOOSE.search(t) or HTOK_CI.search(t)):
            continue
        rg = set()
        for rx in (RUNG_LOOSE, RUNG_CI):
            for m in rx.finditer(t):
                if m.group(1):
                    rg.add(int(m.group(1)))
                if m.group(2):
                    for x in re.findall(r"\d{1,3}", m.group(2)):
                        rg.add(int(x))
        if {r for r in rg if 1 <= r <= 512}:
            out.add((src, uid))
    return out


def harvest(units):
    rows = []
    for src, uid, t in units:
        if not HTOK_RX.search(t):
            continue
        rg = rungs_in(t)
        if not rg:
            continue
        shape = bool(SHAPE_RX.search(t))
        sets = []
        if shape and len(rg) >= 2:
            sets.append("C_STRICT")
        if prox_hit(t):
            sets.append("C_PROX")
        sets.append("C_ALL")
        named3 = rg & RUNGS_3
        if rg == RUNGS_3:
            lad = "LAD_3POINT"          # measured at EXACTLY {21, 63, 126}
        elif rg < RUNGS_3:
            lad = "LAD_SUBSET"          # inside the 3-point ladder, but fewer than 3 rungs
        elif rg > RUNGS_3:
            lad = "LAD_SUPERSET"        # covers the 3-point ladder AND carries finer rungs
        else:
            lad = "LAD_OFF"             # names a rung outside it and does not cover it
        rows.append(dict(
            source=src, unit=uid, in_C_STRICT="C_STRICT" in sets, in_C_PROX="C_PROX" in sets,
            in_C_ALL=True, shape_verb=shape, n_rungs=len(rg),
            rungs="|".join(str(x) for x in sorted(rg)),
            ladder_class=lad, on_3point_exactly=(rg == RUNGS_3),
            confined_to_3point=(rg <= RUNGS_3), covers_3point=(RUNGS_3 <= rg),
            n_of_3_named=len(named3),
            cost_class=cost_class(t), unit_len=len(t)))
    return pd.DataFrame(rows)


# ================================================================== ARM B: the books (frozen)
def nrun(rets, wt, mk):
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
    return (held * rets).sum(axis=1), turn


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


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
    return out


def mech(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    """1082's build(), unmodified: MIN HOLD H, N slots, cap INF, equal weight gross/len(sel)."""
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb = []
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        nsel_by_reb.append(len(sel))
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W, np.array(nsel_by_reb)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def blocks(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ------------------------------------------------------------------- the ladder READING itself
def reading(hs, vals, higher_is_better=True):
    """A READING of an H ladder: (argmax rung, monotone verdict, interior flag, end-to-end sign).
    MaxDD is passed as |MaxDD| with higher_is_better=False so 'best' always means the same thing.
    """
    v = np.asarray(vals, float)
    if not higher_is_better:
        v = -v
    am = int(hs[int(np.argmax(v))])
    d = np.diff(v)
    if np.all(d > 0):
        mono = "UP"
    elif np.all(d < 0):
        mono = "DOWN"
    else:
        mono = "NONMONO"
    interior = am not in (hs[0], hs[-1])
    e2e = float(v[-1] - v[0])
    return dict(argmax=am, monotone=mono, interior=bool(interior), end_to_end=e2e,
                best=float(v.max()), worst=float(v.min()), spread=float(v.max() - v.min()))


def main():
    t0 = time.time()
    P(f"# Idea 1174 (lane C, {DATE}) — how many committed H-AXIS claims rest on the THREE-POINT")
    P("#   LADDER {21, 63, 126}, and what happens to the cheapest of them on a finer one?")
    P(f"# 2 tuned dials: CLAIM SET {CLAIM_SETS} x LADDER SPACING {list(LADDERS)} = 9 cells,")
    P("#   every one published.  NOT dials: panel {U56, B136}, N " + str(NS) + ", the four")
    P(f"#   statistics {STATS}, the 4a/4b legs, the five rule-8 choosers.")
    P(f"# LADDERS (strictly nested, SAME range [21,126] so spacing is not confounded with range):")
    for k, v in LADDERS.items():
        P(f"#   {k:5s} ({len(v):2d} rungs): {v}")
    P(f"# FROZEN (not dials): cap {CAPNAME}, CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0},")
    P(f"#   cost {COST:.0f} bps, LAG {LAG}, cadence {FREQ}, warm-up {WARMUP}, IS ends {IS_END}.")
    P("# DECLARED BEFORE ANY NUMBER — scored on Sharpe over the 18 (panel, N) families:")
    P("#   (D) NOT RESOLVABLE           : L7-vs-LFINE argmax differs at >= 12 of 18  [checked FIRST]")
    P("#   (A) 3-POINT LADDER LOAD-BEARING: L3 reading overturned by LFINE at >= 9 of 18")
    P("#   (B) 3-POINT LADDER INNOCUOUS   : overturned at <= 4 of 18")
    P("#   (C) MIXED                      : 5..8 of 18")
    P("# CHEAPEST = cost class P_BOOK, assigned to every claim from its own text and published.")
    P("")

    # ---------------------------------------------------------------- ARM A: harvest the record
    units, nfiles = corpus()
    P(f"## ARM A — THE CENSUS.  Corpus = {len(units):,} committed text units "
      f"(LEADERBOARD rows + CHANGELOG paragraphs + {nfiles} *.result.md files).")
    cl = harvest(units)
    loose = harvest_loose(units)
    strict_ids = set(zip(cl.source, cl.unit))
    P(f"   {len(cl):,} units carry an H-AXIS token AND name at least one H rung.")
    P(f"   THE REPAIR, PRICED (see G11): the PRE-REPAIR case-insensitive reading gives "
      f"{len(loose):,} units; making the bare-letter `H` forms CASE-SENSITIVE removes "
      f"{len(loose) - len(strict_ids):,} of them (idea 125's `h=1` event horizon, idea 54's "
      f"`h=8%/yr` hazard and their kin) and adds none.")
    dump(cl, "claims")

    census = []
    for cs in CLAIM_SETS:
        sub = cl[cl[f"in_{cs}"]]
        n = len(sub)
        for lad in ["LAD_3POINT", "LAD_SUBSET", "LAD_SUPERSET", "LAD_OFF"]:
            k = int((sub.ladder_class == lad).sum())
            census.append(dict(claim_set=cs, n_claims=n, ladder_class=lad, n=k,
                               share=(k / n if n else np.nan)))
    cen = pd.DataFrame(census)
    dump(cen, "census")

    P("")
    P("   THE QUEUE'S QUESTION, AT EVERY CLAIM SET.  TWO READINGS ARE PUBLISHED AND NEVER MERGED:")
    P("     EXACT    — the unit names exactly {21, 63, 126} and nothing else.")
    P("     CONFINED — the unit names only rungs drawn FROM {21, 63, 126} (1, 2 or all 3), i.e.")
    P("                it has never been off the three-point ladder.  This is the wider and, for")
    P("                the queue's worry, the RELEVANT reading: a claim measured at H=63 alone is")
    P("                as unable to see a finer rung as one measured at all three.")
    P("     claim set   claims     EXACT   share    CONFINED   share    SUPERSET     OFF")
    head = {}
    for cs in CLAIM_SETS:
        sub = cl[cl[f"in_{cs}"]]
        n = len(sub)
        ex = int(sub.on_3point_exactly.sum())
        conf = int(sub.confined_to_3point.sum())
        sup = int((sub.ladder_class == "LAD_SUPERSET").sum())
        off = int((sub.ladder_class == "LAD_OFF").sum())
        head[cs] = (n, ex, conf, sup, off)
        P(f"     {cs:10s} {n:6d}   {ex:7d}   {(ex/n if n else np.nan):5.3f}   "
          f"{conf:8d}   {(conf/n if n else np.nan):5.3f}   {sup:8d}   {off:5d}")
    P("")
    P("   RE-PRICING COST CLASS (the queue's 'cheapest'), at every claim set:")
    P("     claim set   " + "".join(f"{c:>10s}" for c in
                                    ["P_BOOK", "P_NULL", "P_BOOT", "P_TAPE", "P_OTHER"]))
    for cs in CLAIM_SETS:
        sub = cl[cl[f"in_{cs}"]]
        P(f"     {cs:10s}   " + "".join(
            f"{int((sub.cost_class == c).sum()):>10d}"
            for c in ["P_BOOK", "P_NULL", "P_BOOT", "P_TAPE", "P_OTHER"]))
    P("")
    P("   THE RUNG HISTOGRAM — which H rungs the record has actually measured (C_ALL):")
    hist = {}
    for s in cl.rungs:
        for x in str(s).split("|"):
            if x:
                hist[int(x)] = hist.get(int(x), 0) + 1
    for r_, c_ in sorted(hist.items(), key=lambda kv: -kv[1])[:14]:
        P(f"     H={r_:<4d} {c_:5d} units" + ("   <- 3-point ladder" if r_ in RUNGS_3 else ""))
    dump(pd.DataFrame([dict(rung=k, units=v, in_3point=k in RUNGS_3)
                       for k, v in sorted(hist.items())]), "runghist")

    # ---------------------------------------------------------------- ARM B: build the 288 books
    P("")
    P(f"## ARM B — RE-PRICING THE P_BOOK FAMILY.  {len(PANELS)} panels x {len(NS)} N x "
      f"{len(HS)} H = {len(PANELS)*len(NS)*len(HS)} books, ALL published.")
    rows, benchrows, gaterows, picks = [], [], [], []
    gates = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        K = len(px.columns)
        T = len(idx)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        P(f"   --- {panel}: {K} columns, {T} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates")
        P(f"       SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"       RULES v2 full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  "
          f"halves {lb['H1']:.4f}/{lb['H2']:.4f}  OOS {lb['OOS_CAGR']:.2%} / "
          f"{lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")
        benchrows += [dict(panel=panel, series="SPY", **sb),
                      dict(panel=panel, series="RULESv2_live", **lb)]

        if panel == "U56":
            W20, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            g, tn = nrun(rets, lagmat(W20), mkl)
            fast = g - tn * COST / 1e4
            d1 = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1 fast runner == engine.backtest (U56, N=20, H=126, cap INF)"] = (d1, d1 < 1e-12)
            m = fmet(fast[warm])
            d2 = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2 CROSS-RUN vs 936/1071/1082/1086/1093's committed W/H126 N=20 triple"] = (
                d2, d2 < 5e-3)
            d3 = max(abs(sb["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
                     abs(sb["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
                     abs(sb["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
            gates["G3 CROSS-RUN SPY OOS triple"] = (d3, d3 < 5e-4)
            d4 = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED)
            gates["G4 live RULES v2 MaxDD == committed -12.05%"] = (d4, d4 < 5e-4)
            Wa, _ = build(rank_key, elig, priced, reb, 20, 126, T, K, GROSS0)
            gates["G6 build() is deterministic"] = (float(np.abs(Wa - W20).max()),
                                                    float(np.abs(Wa - W20).max()) == 0.0)

        for N in NS:
            for H in HS:
                W, nsel = build(rank_key, elig, priced, reb, N, H, T, K, GROSS0)
                g, tn = nrun(rets, lagmat(W), mkl)
                r = g - tn * COST / 1e4
                b = blocks(r, warm, ins, oos)
                l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                rw = dict(panel=panel, N=N, H=H, cap=CAPNAME,
                          mean_nsel=float(nsel.mean()),
                          turnover=float(tn[warm].sum() / (warm.sum() / 252.0)),
                          IS_turnover=float(tn[ins].sum() / (ins.sum() / 252.0)),
                          **b, **l4b, **l4a, **l4bo,
                          pass4b=all(l4b.values()), pass4a=all(l4a.values()),
                          pass4b_oos=all(l4bo.values()),
                          in_L3=H in L3, in_L7=H in L7)
                rw["pass4b_full_and_oos"] = rw["pass4b"] and rw["pass4b_oos"]
                rows.append(rw)
            P(f"       N={N:2d} done ({len(HS)} rungs)  ({time.time()-t0:.0f}s)")

        gp = pd.DataFrame([r for r in rows if r["panel"] == panel])
        # ---- RULE 8: IS-only choosers pick (N, H); OOS read ONCE.  The LADDER is the constraint.
        chs = [("C_L3", "IS_Sharpe", L3), ("C_L7", "IS_Sharpe", L7),
               ("C_LFINE", "IS_Sharpe", LFINE), ("C_LFINE_CAGR", "IS_CAGR", LFINE),
               ("C_LFINE_DD", "IS_MaxDD", LFINE)]
        for cname, key, lad in chs:
            cand = gp[gp.H.isin(lad)]
            pick = cand.sort_values([key, "N", "H"], ascending=[False, True, True]).iloc[0]
            picks.append(dict(panel=panel, chooser=cname, ladder=("L3" if lad is L3 else
                                                                 "L7" if lad is L7 else "LFINE"),
                              key=key, N=int(pick["N"]), H=int(pick["H"]),
                              IS_Sharpe=pick["IS_Sharpe"], IS_CAGR=pick["IS_CAGR"],
                              IS_MaxDD=pick["IS_MaxDD"],
                              OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                              OOS_MaxDD=pick["OOS_MaxDD"],
                              full_CAGR=pick["CAGR"], full_Sharpe=pick["Sharpe"],
                              full_MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                              turnover=pick["turnover"],
                              spy_OOS_CAGR=sb["OOS_CAGR"], spy_OOS_Sharpe=sb["OOS_Sharpe"],
                              spy_OOS_MaxDD=sb["OOS_MaxDD"],
                              live_OOS_Sharpe=lb["OOS_Sharpe"], live_OOS_MaxDD=lb["OOS_MaxDD"],
                              pass4b_full=bool(pick["pass4b"]),
                              pass4b_oos=bool(pick["pass4b_oos"]),
                              pass4a=bool(pick["pass4a"])))

    grid = pd.DataFrame(rows)
    bn = pd.DataFrame(benchrows)
    pk = pd.DataFrame(picks)

    # ------------------------------------------------------------------ cross-run gate vs 1093
    if G1093.exists():
        g93 = pd.read_csv(G1093)
        j = grid.merge(g93, on=["panel", "N", "H"], suffixes=("", "_93"))
        d5 = max(float(np.abs(j.CAGR - j.CAGR_93).max()),
                 float(np.abs(j.Sharpe - j.Sharpe_93).max()),
                 float(np.abs(j.MaxDD - j.MaxDD_93).max()),
                 float(np.abs(j.turnover - j.turnover_93).max()))
        gates[f"G5 CROSS-RUN 1093's committed grid reproduced cell-for-cell ({len(j)} shared "
              "(panel, N, H) cells, 4 statistics each)"] = (d5, d5 < 5e-3)
        gates["G5b the shared-cell count is 1093's WHOLE committed grid"] = (
            float(len(j)), len(j) == len(g93))
    else:
        gates["G5 CROSS-RUN 1093's committed grid (FILE MISSING — gate cannot run)"] = (
            float("nan"), False)

    # G3b DIAGNOSES G3 rather than absorbing it: if the SAME-DAY committed benchmarks reproduce
    # exactly while the OLDER anchor drifts, the drift is a TAPE VINTAGE effect (idea 1163's
    # finding, arriving from the benchmark side) and not a construction error in this run.
    if B1093.exists():
        b93 = pd.read_csv(B1093)
        bn2 = bn.copy()
        bn2["series"] = bn2.series.str.replace("RULESv2_live", "RULESv2", regex=False)
        j = bn2.merge(b93, on=["panel", "series"], suffixes=("", "_93"))
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe", "IS_MaxDD",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
        d3b = max(float(np.abs(j[c] - j[f"{c}_93"]).max()) for c in cols)
        gates[f"G3b CROSS-RUN 1093's SAME-DAY committed benchmarks reproduced ({len(j)} series x "
              f"{len(cols)} statistics) — the diagnosis of G3"] = (d3b, d3b < 1e-6)

    nest = (set(L3) <= set(L7) <= set(LFINE))
    gates["G7 the ladders are STRICTLY NESTED L3 < L7 < LFINE"] = (
        float(len(LFINE) - len(L7)), bool(nest and len(L3) < len(L7) < len(LFINE)))
    gates["G8 all three ladders span the SAME range [21, 126] (spacing is not range)"] = (
        0.0, min(L3) == min(L7) == min(LFINE) == 21 and max(L3) == max(L7) == max(LFINE) == 126)
    tsp = float(grid[grid.panel == "B136"].turnover.max() - grid[grid.panel == "B136"].turnover.min())
    gates["G9 the H dial is LIVE (B136 turnover spread >= 1.0x/yr across the ladder)"] = (
        tsp, tsp >= 1.0)
    gates["G10 the census population partitions by ladder class"] = (
        float(len(cl)), int(cen[cen.claim_set == "C_ALL"].n.sum()) == len(cl))
    gates["G11 the case-sensitivity REPAIR only ever REMOVES units (strict population is a "
          "strict subset of the pre-repair one)"] = (
        float(len(strict_ids - loose)), len(strict_ids - loose) == 0)

    P("")
    P("## GATES (printed before any result number)")
    for k, (v, ok) in gates.items():
        P(f"   {'PASS' if ok else 'FAIL'}  {k}: |d| = {v:.3e}")
        gaterows.append(dict(gate=k, value=v, passed=bool(ok)))

    # ------------------------------------------------------------------ the ladder readings
    P("")
    P("## THE READINGS — every (panel, N) family read on each of the three ladders, 4 statistics")
    lad_rows = []
    for panel in PANELS:
        for N in NS:
            s = grid[(grid.panel == panel) & (grid.N == N)].set_index("H")
            for stat in STATS:
                hib = stat not in ("MaxDD", "turnover")
                for lname, lad in LADDERS.items():
                    v = [(-abs(s.loc[h, "MaxDD"]) if stat == "MaxDD" else float(s.loc[h, stat]))
                         for h in lad]
                    rd = reading(lad, v, higher_is_better=(True if stat == "MaxDD" else hib))
                    lad_rows.append(dict(panel=panel, N=N, stat=stat, ladder=lname,
                                         n_rungs=len(lad), **rd))
    ld = pd.DataFrame(lad_rows)
    dump(ld, "ladder")

    piv = ld.pivot_table(index=["panel", "N", "stat"], columns="ladder",
                         values=["argmax", "monotone", "interior"], aggfunc="first")
    ov_rows = []
    for (panel, N, stat), r_ in piv.iterrows():
        a3, a7, af = r_[("argmax", "L3")], r_[("argmax", "L7")], r_[("argmax", "LFINE")]
        m3, m7, mf = r_[("monotone", "L3")], r_[("monotone", "L7")], r_[("monotone", "LFINE")]
        ov_rows.append(dict(panel=panel, N=N, stat=stat,
                            argmax_L3=a3, argmax_L7=a7, argmax_LFINE=af,
                            mono_L3=m3, mono_L7=m7, mono_LFINE=mf,
                            interior_L3=bool(r_[("interior", "L3")]),
                            interior_LFINE=bool(r_[("interior", "LFINE")]),
                            argmax_moved=(a3 != af), mono_flipped=(m3 != mf),
                            overturned=((a3 != af) or (m3 != mf)),
                            unconverged=(a7 != af)))
    ov = pd.DataFrame(ov_rows)
    dump(ov, "overturn")

    P("")
    P("   PER-FAMILY, HEADLINE STATISTIC = Sharpe  (18 families)")
    P("     panel   N   argmax L3 / L7 / LFINE    monotone L3 / L7 / LFINE      overturned  unconv")
    hs_ = ov[ov.stat == "Sharpe"]
    for _, r_ in hs_.iterrows():
        P(f"     {r_.panel:6s} {int(r_.N):3d}   {int(r_.argmax_L3):4d} /{int(r_.argmax_L7):4d} /"
          f"{int(r_.argmax_LFINE):5d}       {r_.mono_L3:8s}/{r_.mono_L7:9s}/{r_.mono_LFINE:9s}"
          f"    {str(bool(r_.overturned)):5s}      {str(bool(r_.unconverged)):5s}")
    n_ov = int(hs_.overturned.sum())
    n_unc = int(hs_.unconverged.sum())
    n_am = int(hs_.argmax_moved.sum())
    n_mf = int(hs_.mono_flipped.sum())
    P(f"     Sharpe: OVERTURNED {n_ov} of {len(hs_)}   (argmax moved {n_am}, monotone flipped "
      f"{n_mf})   L7-vs-LFINE unconverged {n_unc} of {len(hs_)}")

    P("")
    P("   ALL FOUR STATISTICS (the 3 non-headline ones are CONTROLS, not the pre-declared scoring)")
    P("     stat        families   overturned   argmax moved   monotone flipped   unconverged")
    for stat in STATS:
        s = ov[ov.stat == stat]
        P(f"     {stat:10s} {len(s):9d}   {int(s.overturned.sum()):10d}   "
          f"{int(s.argmax_moved.sum()):12d}   {int(s.mono_flipped.sum()):16d}   "
          f"{int(s.unconverged.sum()):11d}")

    P("")
    P("   THE INTERIOR-PEAK QUESTION — on L3 the ONLY interior rung is 63, so an 'interior peak'")
    P("   read off the 3-point ladder is always the claim 'H=63 is best'.  Does it survive?")
    for stat in STATS:
        s = ov[ov.stat == stat]
        i3 = s[s.interior_L3]
        keep = int((i3.argmax_LFINE == 63).sum())
        P(f"     {stat:10s}  interior on L3 at {len(i3):2d} of {len(s)} families; "
          f"LFINE keeps the peak AT 63 at {keep} of those {len(i3)}"
          + (f"; LFINE argmax there: {sorted(set(int(x) for x in i3.argmax_LFINE))}"
             if len(i3) else ""))

    # ---------------------------------------------------------- the pre-declared verdict
    P("")
    if n_unc >= 12:
        outcome = "(D) NOT RESOLVABLE"
    elif n_ov >= 9:
        outcome = "(A) THE 3-POINT LADDER IS LOAD-BEARING"
    elif n_ov <= 4:
        outcome = "(B) THE 3-POINT LADDER IS INNOCUOUS"
    else:
        outcome = "(C) MIXED"
    P(f"## PRE-DECLARED OUTCOME: {outcome}   "
      f"(Sharpe: overturned {n_ov}/18, L7-vs-LFINE unconverged {n_unc}/18)")

    # ------------------------------------------------------------------ KEEP paths + rule 8
    P("")
    P("## BOTH KEEP PATHS at all 288 cells (PROTOCOL rule 4)")
    for panel in PANELS:
        s = grid[grid.panel == panel]
        P(f"   {panel}: 4b full {int(s.pass4b.sum())}/{len(s)}   "
          f"4b OOS {int(s.pass4b_oos.sum())}/{len(s)}   "
          f"4b full AND OOS {int(s.pass4b_full_and_oos.sum())}/{len(s)}   "
          f"4a {int(s.pass4a.sum())}/{len(s)}")
    P(f"   TOTAL: 4b full {int(grid.pass4b.sum())}/{len(grid)}   "
      f"4b OOS {int(grid.pass4b_oos.sum())}/{len(grid)}   "
      f"4b full AND OOS {int(grid.pass4b_full_and_oos.sum())}/{len(grid)}   "
      f"4a {int(grid.pass4a.sum())}/{len(grid)}")
    both = grid[grid.pass4b_full_and_oos]
    if len(both):
        P("   books clearing 4b FULL and OOS at 10 bps:")
        for _, r_ in both.sort_values("Sharpe", ascending=False).iterrows():
            P(f"      {r_.panel} N={int(r_.N):2d} H={int(r_.H):3d}  {r_.CAGR:7.2%} / "
              f"{r_.Sharpe:.4f} / {r_.MaxDD:7.2%}  halves {r_.H1:.3f}/{r_.H2:.3f}  "
              f"OOS {r_.OOS_CAGR:6.2%}/{r_.OOS_Sharpe:.4f}/{r_.OOS_MaxDD:7.2%}  "
              f"turn {r_.turnover:.2f}x   on L3: {bool(r_.in_L3)}")
    P("   4b pass rate BY LADDER MEMBERSHIP (is a 4b winner reachable from the coarse ladder?):")
    for lname, lad in LADDERS.items():
        s = grid[grid.H.isin(lad)]
        P(f"      {lname:5s} {len(s):4d} cells   4b full {int(s.pass4b.sum()):3d}   "
          f"4b full+OOS {int(s.pass4b_full_and_oos.sum()):3d}   4a {int(s.pass4a.sum()):3d}")

    P("")
    P("## RULE 8 WALK-FORWARD — (N, H) chosen on 2009-2016 ONLY, 2017-2026 read ONCE.")
    P("   The LADDER is the chooser's constraint: C_L3 may only pick rungs in {21,63,126}.")
    P("     panel  chooser        N   H     IS_Sharpe    OOS CAGR / Sharpe / MaxDD   "
      "SPY OOS S   beats SPY  4b  4bOOS  4a")
    for _, r_ in pk.iterrows():
        P(f"     {r_.panel:6s} {r_.chooser:13s} {int(r_.N):3d} {int(r_.H):3d}   "
          f"{r_.IS_Sharpe:9.4f}    {r_.OOS_CAGR:7.2%} / {r_.OOS_Sharpe:.4f} / "
          f"{r_.OOS_MaxDD:7.2%}   {r_.spy_OOS_Sharpe:.4f}   "
          f"{str(bool(r_.OOS_Sharpe > r_.spy_OOS_Sharpe)):5s}      {int(r_.pass4b_full)}  "
          f"{int(r_.pass4b_oos)}     {int(r_.pass4a)}")
    P("")
    P("   DOES RESOLUTION ON THE HOLD AXIS BUY OOS SHARPE?  (the capital question)")
    for lname in ["L3", "L7", "LFINE"]:
        s = pk[(pk.ladder == lname) & (pk.key == "IS_Sharpe")]
        P(f"     {lname:5s} IS-Sharpe chooser: mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}  "
          f"mean OOS CAGR {s.OOS_CAGR.mean():.2%}  beats SPY "
          f"{int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum())} of {len(s)}  "
          f"4b full {int(s.pass4b_full.sum())} of {len(s)}  picks "
          f"{[(p, int(n), int(h)) for p, n, h in zip(s.panel, s.N, s.H)]}")
    d_fine = float(pk[(pk.ladder == "LFINE") & (pk.key == "IS_Sharpe")].OOS_Sharpe.mean()
                   - pk[(pk.ladder == "L3") & (pk.key == "IS_Sharpe")].OOS_Sharpe.mean())
    P(f"     LFINE - L3 on mean OOS Sharpe: {d_fine:+.4f}")

    dump(grid, "grid")
    dump(pk, "rule8")
    dump(bn, "benchmarks")
    dump(pd.DataFrame(gaterows), "gates")

    # ------------------------------------------------------------------ LEADERBOARD rows
    P("")
    P("## LEADERBOARD rows")
    lbrows = []
    for panel in PANELS:
        s = pk[(pk.panel == panel) & (pk.chooser == "C_LFINE")].iloc[0]
        g3 = pk[(pk.panel == panel) & (pk.chooser == "C_L3")].iloc[0]
        b0 = bn[(bn.panel == panel) & (bn.series == "RULESv2_live")].iloc[0]
        nm = f"1174 {panel} C_LFINE rule-8 pick N={int(s.N)} H={int(s.H)} (vs C_L3 H={int(g3.H)})"
        v = "KEEP-candidate" if (s.pass4b_full and s.pass4b_oos) else "KILL"
        lbrows.append(f"| {DATE} | {nm} | {s.full_CAGR:.1%} | {s.full_Sharpe:.2f} | "
                      f"{s.full_MaxDD:.1%} | {s.H1:.2f} / {s.H2:.2f} | "
                      f"{b0.Sharpe:.2f} ({b0.H1:.2f}/{b0.H2:.2f}) | {v} | "
                      f"{DATE}_{SLUG}_C.py |")
    nm = (f"1174 census: H-axis claims EXACTLY on {{21,63,126}} = {head['C_STRICT'][1]}/"
          f"{head['C_STRICT'][0]} C_STRICT and {head['C_ALL'][1]}/{head['C_ALL'][0]} C_ALL, "
          f"CONFINED to it {head['C_STRICT'][2]}/{head['C_STRICT'][0]} and "
          f"{head['C_ALL'][2]}/{head['C_ALL'][0]}; Sharpe reading overturned {n_ov}/18 on LFINE")
    lbrows.append(f"| {DATE} | {nm} | n/a | n/a | n/a | n/a | n/a | KILL as a capital finding | "
                  f"{DATE}_{SLUG}_C.py |")
    for l in lbrows:
        P("   " + l)

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    Path(f"{OUT}.leaderboard.txt").write_text("\n".join(lbrows) + "\n")
    P(f"\n# done in {time.time()-t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
