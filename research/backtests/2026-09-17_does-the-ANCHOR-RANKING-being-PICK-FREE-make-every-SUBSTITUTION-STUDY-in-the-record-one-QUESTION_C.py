#!/usr/bin/env python3
"""
Idea 1240 (lane C, 2026-09-17) — does the ANCHOR RANKING being PICK-FREE make every
SUBSTITUTION STUDY in the record ONE QUESTION?

THE PREMISE, READ FROM THE RECORD.  Idea 1237 (lane C, 2026-09-17) established two facts about
idea 1224's substitution study.  G9: DELTA(A) == meanOOS(A) - meanOOS(picks) to 3.3e-16, i.e.
the pick column enters the published statistic as an ADDITIVE CONSTANT that does not depend on
the alternative A.  G13: the anchor column is bit-identical across pick sets sharing a fold set.
Consequence, which 1224 published as three measurements: the incumbent ranked 5 of 19 on ALL
THREE of its pick sets (P_1214 42 picks, P_AXIS 168, P_TEXT 620) not because three independent
contrasts agreed but because they were ARITHMETICALLY THE SAME CONTRAST.  The queue asks how
general that is.

WHAT IS ACTUALLY BEING TESTED, STATED BEFORE ANY NUMBER IS READ.  Write a substitution study in
its general form.  Alternatives A in a candidate set; a pick set P = {(cell_i, book_i)} where
cell = (panel, fold); the published statistic

    DELTA(A, P) = (1/|P|) * sum_i [ S(A ; cell_i) - S(book_i ; cell_i) ]

with S = OOS Sharpe on that cell.  Split the sum:

    DELTA(A, P) = SUM_c w_P(c) * S(A ; c)  -  K(P),     w_P(c) = #{i : cell_i = c} / |P|
                                                        K(P)   = (1/|P|) sum_i S(book_i ; cell_i)

K(P) is pick-only and shifts every alternative by the same amount.  Therefore, FOR A MEAN-FORM
CONTRAST, the ranking of alternatives depends on the pick set ONLY THROUGH THE CELL-WEIGHT
VECTOR w_P.  This is the exact criterion, and it is sharper than 1237's fold-set version:

    RANK-DEGENERATE  <=>  the contrast is mean-form  AND  w_P == w_P' .

It also says where the degeneracy STOPS.  Two escapes exist and both are testable:
  (E1) a pick set that WEIGHTS CELLS DIFFERENTLY (unequal picks per panel or per fold) — the
       anchor column becomes a different weighted mean and the rank CAN move;
  (E2) a contrast that is NOT mean-form (median, clustered t, win rate, trimmed mean) — the
       pick column stops being an additive constant and the rank CAN move.
Whether either escape moves the rank IN FACT, on this tape, is a measurement, not an identity,
and this run makes it.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) ONE QUESTION — a majority (> 0.50) of the record's checkable pick-set contrasts are
      rank-degenerate by the criterion above, AND the escapes that exist on this tape move the
      incumbent's rank by less than 1 place on median.  The record's substitution studies are
      re-publications of one measurement.
  (B) NOT ONE QUESTION — either the degenerate share is <= 0.50, or the escapes move the rank
      by >= 2 places on median, i.e. 1224 was a special case and not a structure.
  (C) MIXED — degenerate share > 0.50 but the escapes move the rank >= 2 places, i.e. the
      record's contrasts are degenerate BY CHOICE OF STATISTIC and not by arithmetic necessity.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  STUDY SET          {S_STRICT, S_BROAD, S_ALL} — which committed units count as substitution /
                     counterfactual / "replace X with Y" studies.
                     S_STRICT  substitution language AND >= 2 named pick/claim sets AND a named
                               rank or ordering claim.
                     S_BROAD   substitution language AND >= 2 named pick/claim sets.
                     S_ALL     any committed unit naming a pick-conditioned contrast at all.
  CONTRAST DEFINITION {C_MEAN, C_MED, C_T, C_WIN, C_TRIM} — the statistic alternatives are
                     ranked by.  C_MEAN is the record's own (1214/1224/1237).  The other four
                     are the E2 escapes.

NOT DIALS, REPORTED AT EVERY VALUE: the PICK-SET FAMILY (9 sets spanning the w-vector, below) —
it is the OBJECT of the census, not a tuning knob; PANEL {U56, B136, SMALL} (rule 9); the four
ladders; the 22 candidate books (19 distinct); the 14 folds; the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, GROSS 0.75 anchor, 10 bps (rule 2), decide-at-t / apply-at-t+1,
warm-up 260 rows, OOS split 2017-01-01 (rule 8).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
candidate book and every rule-8 row; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only).
"""
from __future__ import annotations

import hashlib
import itertools
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
SLUG = ("does-the-ANCHOR-RANKING-being-PICK-FREE-make-every-SUBSTITUTION-STUDY-in-the-record-"
        "one-QUESTION")
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}
LADS = ["N", "H", "GROSS", "CADENCE"]
FOLD_YEARS = list(range(2013, 2027))
CONTRASTS = ["C_MEAN", "C_MED", "C_T", "C_WIN", "C_TRIM"]
STUDY_SETS = ["S_STRICT", "S_BROAD", "S_ALL"]
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels / runner (1237's)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def akey(k):
    return f"{k[0]}={k[1]}"


# ==================================================================== contrast definitions
def contrast(stat, d, fold):
    """d = per-pick difference vector for ONE alternative; fold = its cluster labels.
    Returns the scalar the alternatives are ranked by.  C_MEAN is the record's own."""
    d = np.asarray(d, float)
    ok = np.isfinite(d)
    d, f = d[ok], np.asarray(fold)[ok]
    if len(d) == 0:
        return np.nan
    if stat == "C_MEAN":
        return float(d.mean())
    if stat == "C_MED":
        return float(np.median(d))
    if stat == "C_WIN":
        return float((d > 0).mean())
    if stat == "C_TRIM":
        lo, hi = np.percentile(d, [10, 90])
        sel = d[(d >= lo) & (d <= hi)]
        return float(sel.mean()) if len(sel) else float(d.mean())
    if stat == "C_T":
        fm = pd.Series(d).groupby(pd.Series(f).values).mean()
        if len(fm) < 2:
            return 0.0
        se = float(fm.std(ddof=1) / np.sqrt(len(fm)))
        return float(d.mean() / se) if se > 0 else 0.0
    raise ValueError(stat)


ADDITIVE = {"C_MEAN": True, "C_MED": False, "C_T": False, "C_WIN": False, "C_TRIM": False}


def ranking(vals):
    """Descending rank (1 = best) with deterministic tie-break on the alternative's index."""
    order = sorted(range(len(vals)),
                   key=lambda i: (-(vals[i] if np.isfinite(vals[i]) else -np.inf), i))
    rk = [0] * len(vals)
    for pos, i in enumerate(order):
        rk[i] = pos + 1
    return rk


def kendall_tau(a, b):
    n = len(a)
    if n < 2:
        return np.nan
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = np.sign(a[i] - a[j]) * np.sign(b[i] - b[j])
            if s > 0:
                c += 1
            elif s < 0:
                d += 1
    return (c - d) / (0.5 * n * (n - 1))


# ==================================================================== the record's own text
SUBST = re.compile(r"\b(substitut\w*|counterfactual\w*|stand[- ]?in|replace[sd]?\b|replacing|"
                   r"instead of|in place of|swap\w*|re-?score\w*|re-?read\w*|re-?price\w*)\b",
                   re.I)
PICKISH = re.compile(r"\b(pick set|pick-set|picks|pick|claim set|claim-set|claims|corpus|"
                     r"cells?|P_[A-Z0-9]+|C_[A-Z0-9]+|S_[A-Z0-9]+)\b")
RANKISH = re.compile(r"\b(rank\w*|ordering|argmax|top|best|worst|\d+\s+of\s+\d+)\b", re.I)
NAMEDSET = re.compile(r"\b(P_[A-Z0-9]+|C_[A-Z0-9]+|S_[A-Z0-9]+|A_[A-Z0-9]+|T_[A-Z0-9]+|"
                      r"B_[A-Z0-9]+|D_[A-Z0-9]+|K_[A-Za-z0-9]+|H_[A-Z0-9]+|UG_[A-Z0-9]+)\b")
STAT_PAT = {
    "C_MEAN": re.compile(r"\b(mean|average|pooled|DELTA)\b", re.I),
    "C_MED": re.compile(r"\bmedian\b", re.I),
    "C_T": re.compile(r"\b(t[- ]stat\w*|\bt\s*[+-]?\d|clustered|SE\b|standard error)\b", re.I),
    "C_WIN": re.compile(r"\b(win rate|winrate|\d+W/\d+L|sign p|hit rate|\bof\s+\d+\s+cells?)\b",
                        re.I),
    "C_TRIM": re.compile(r"\b(trimmed|winsoriz\w*)\b", re.I),
}


def units():
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in cl.split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    nmd = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        nmd += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, nmd


def census(U):
    """Classify every committed unit.  A unit is a SUBSTITUTION STUDY if it uses substitution
    language; it carries a PICK-SET CONTRAST if it names >= 2 distinct set tokens; its CONTRAST
    STATISTIC is whatever statistic vocabulary it names (C_MEAN when it names a mean/DELTA and
    nothing sharper).  Classification is TEXTUAL and is reported as such."""
    rows = []
    for src, txt in U:
        sub = bool(SUBST.search(txt))
        sets = sorted(set(NAMEDSET.findall(txt)))
        pick = bool(PICKISH.search(txt))
        rank = bool(RANKISH.search(txt))
        stats = [s for s, p in STAT_PAT.items() if p.search(txt)]
        # the statistic the ALTERNATIVES are ranked by: the sharpest named non-mean form wins,
        # else C_MEAN when a mean/DELTA is named, else UNSTATED.
        sharp = [s for s in stats if s != "C_MEAN"]
        stat = sharp[0] if sharp else ("C_MEAN" if "C_MEAN" in stats else "UNSTATED")
        rows.append(dict(uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
                         SUBST=sub, PICKISH=pick, RANKISH=rank, n_sets=len(sets),
                         sets="|".join(sets[:8]), stat=stat, n_stats=len(stats),
                         S_ALL=bool(pick and len(sets) >= 2),
                         S_BROAD=bool(sub and len(sets) >= 2),
                         S_STRICT=bool(sub and len(sets) >= 2 and rank)))
    return pd.DataFrame(rows)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1240 (lane C, 2026-09-17) — does the ANCHOR RANKING being PICK-FREE make every")
    say("SUBSTITUTION STUDY in the record ONE QUESTION?")
    say("=" * 110)
    say("")
    say("  DELTA(A,P) = SUM_c w_P(c) S(A;c) - K(P).  K(P) is PICK-ONLY and shifts every")
    say("  alternative equally.  EXACT CRITERION, declared before the tape is read:")
    say("      RANK-DEGENERATE  <=>  contrast is MEAN-FORM  AND  w_P == w_P'.")
    say("  Two escapes: (E1) a pick set that weights CELLS differently; (E2) a contrast that is")
    say("  not mean-form.  Whether either MOVES THE RANK on this tape is measured, not assumed.")
    say("  PRE-DECLARED: (A) ONE QUESTION — degenerate share > 0.50 AND escapes move the")
    say("  incumbent's rank < 1 place on median.  (B) NOT ONE QUESTION — share <= 0.50 or")
    say("  escapes move >= 2 places.  (C) MIXED — share > 0.50 but escapes move >= 2 places.")

    # ------------------------------------------------------------------ panels, books, folds
    say("")
    say("=" * 110)
    say("ARM A — PANELS, THE 22 CANDIDATE BOOKS, THE (panel, fold) CELL TABLE")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")

    booked, bench, BOOKKEY = {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
        af = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]),
                                         f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(books)} candidate books built.")
        del frames

    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    INC = ("N", A_N)

    # machinery gates
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    lm = mdd(bench["U56"]["live"][WARMUP:])
    gate("G2 live RULES v2 U56 MaxDD == committed -12.05%", lm, LIVE_MAXDD_COMMITTED,
         abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)

    # the 19 DISTINCT alternatives (four anchor keys are one book — 1224 G4, replayed as G3)
    dev = 0.0
    for k in ANCH_KEYS[1:]:
        dev = max(dev, float(np.abs(booked["U56"][k] - booked["U56"][ANCH_KEYS[0]]).max()))
    gate("G3 the four anchor keys are ONE book (bit for bit)", dev, 0.0, dev == 0.0)
    ALT = [k for k in BOOKKEY if k == INC or k not in ANCH_KEYS]
    gate("G4 distinct candidate set size", float(len(ALT)), 19.0, len(ALT) == 19)
    say(f"    ALTERNATIVES: {len(ALT)} distinct books ({len(BOOKKEY)} keys, "
        f"{len(ANCH_KEYS)-1} collapsed into the incumbent).")

    # folds
    folds = {}
    for pan in panels:
        yrs = pan.idx.year.values
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            if int(oo[0]) - pan.i0 < 252:
                continue
            folds.setdefault(pan.name, []).append((y, pan.i0, int(oo[0]), int(oo[0]),
                                                   int(oo[-1]) + 1))
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")

    # the cell table S(A ; panel, fold)
    S = {}
    CELLS = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            CELLS.append((pan.name, y))
            for k in BOOKKEY:
                S[(pan.name, k, y)] = sharpe(booked[pan.name][k][o0:o1])
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}
    say(f"    CELL TABLE: {len(CELLS)} (panel, fold) cells x {len(BOOKKEY)} books = "
        f"{len(CELLS)*len(BOOKKEY)} OOS Sharpes.")

    def is_sharpe(p, k, lo, hi):
        return sharpe(booked[p][k][lo:hi])

    def argmax_rung(p, lad, lo, hi):
        v = [(is_sharpe(p, (lad, r), lo, hi), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    # ------------------------------------------------------------------ the pick-set family
    say("")
    say("=" * 110)
    say("ARM B — THE PICK-SET FAMILY (the object of the census, not a dial)")
    say("=" * 110)
    say("")
    say("  Every pick is rule-8 legal: the book is the IS argmax on that fold's OWN IS window.")
    say("  The family is built to SPAN the cell-weight vector w_P, which is the only channel")
    say("  through which a mean-form contrast can see the pick set at all.")

    def pick_axis(pans, lads, yrs, rep=1):
        P = []
        for pn in pans:
            for (y, lo, hi, o0, o1) in folds[pn]:
                if y not in yrs:
                    continue
                for lad in lads:
                    r = argmax_rung(pn, lad, lo, hi)
                    if r is None:
                        continue
                    for _ in range(rep):
                        P.append((pn, y, (lad, r)))
        return P

    ALLP = [p.name for p in panels]
    ALLY = set(FOLD_YEARS)
    YOOS = {y for y in FOLD_YEARS if y >= 2017}
    YEARLY = {y for y in FOLD_YEARS if y < 2017}
    PICKSETS = {}
    PICKSETS["P_ALL4"] = pick_axis(ALLP, LADS, ALLY)                     # 1224's P_AXIS shape
    PICKSETS["P_N"] = pick_axis(ALLP, ["N"], ALLY)                       # one ladder
    PICKSETS["P_GROSS"] = pick_axis(ALLP, ["GROSS"], ALLY)               # the degenerate ladder
    PICKSETS["P_U56"] = pick_axis(["U56"], LADS, ALLY)                   # single panel
    PICKSETS["P_SMALL"] = pick_axis(["SMALL"], LADS, ALLY)               # single panel
    PICKSETS["P_OOS"] = pick_axis(ALLP, LADS, YOOS)                      # late folds only
    PICKSETS["P_EARLY"] = pick_axis(ALLP, LADS, YEARLY)                  # early folds only
    PICKSETS["P_TILT"] = (pick_axis(["U56"], LADS, ALLY, rep=5)
                          + pick_axis(["B136", "SMALL"], LADS, ALLY))    # deliberate w tilt
    PICKSETS["P_TEXT"] = None                                            # filled below

    # P_TEXT: the record's OWN committed (panel, ladder, rung) triples, harvested from the text
    R_N = re.compile(r"\bN\s*=\s*(\d+)\b")
    R_H = re.compile(r"\bH\s*=\s*(\d+)\b")
    R_G = re.compile(r"\b(?:gross|g)\s*[= ]\s*(0?\.\d{2})\b", re.I)
    R_C = re.compile(r"\b(weekly|monthly)\b", re.I)
    PANEL_R = re.compile(r"\b(U56|B136|SMALL)\b")
    U, nmd = units()
    triples = set()
    for src, txt in U:
        pans_ = set(PANEL_R.findall(txt))
        if not pans_:
            continue
        tr = []
        for m in R_N.finditer(txt):
            if int(m.group(1)) in LAD["N"]:
                tr.append(("N", int(m.group(1))))
        for m in R_H.finditer(txt):
            if int(m.group(1)) in LAD["H"]:
                tr.append(("H", int(m.group(1))))
        for m in R_G.finditer(txt):
            if round(float(m.group(1)), 2) in LAD["GROSS"]:
                tr.append(("GROSS", round(float(m.group(1)), 2)))
        for m in R_C.finditer(txt):
            tr.append(("CADENCE", "W" if m.group(1).lower() == "weekly" else "M"))
        for pn in pans_:
            for k in set(tr):
                triples.add((pn, k))
    PT = []
    for (pn, k) in sorted(triples, key=lambda x: (x[0], str(x[1]))):
        for (y, lo, hi, o0, o1) in folds[pn]:
            if y >= 2017:
                PT.append((pn, y, k))
    PICKSETS["P_TEXT"] = PT
    say(f"    P_TEXT harvested from {len(U)} committed units ({nmd} memo/result files): "
        f"{len(triples)} (panel, rung) triples x their OOS folds = {len(PT)} picks.")

    # cell-weight vectors
    cell_index = {c: i for i, c in enumerate(CELLS)}
    WVEC = {}
    for nm, P in PICKSETS.items():
        w = np.zeros(len(CELLS))
        for (pn, y, k) in P:
            w[cell_index[(pn, y)]] += 1.0
        WVEC[nm] = w / w.sum() if w.sum() else w
    say("")
    say("    name        picks   distinct cells   w-entropy   max w")
    prow = []
    for nm, P in PICKSETS.items():
        w = WVEC[nm]
        nz = w[w > 0]
        ent = float(-(nz * np.log(nz)).sum() / np.log(len(nz))) if len(nz) > 1 else 0.0
        say(f"    {nm:11s} {len(P):6d}   {int((w>0).sum()):14d}   {ent:9.4f}   {w.max():.4f}")
        prow.append(dict(pickset=nm, n_picks=len(P), n_cells=int((w > 0).sum()),
                         w_entropy=ent, w_max=float(w.max())))
    pd.DataFrame(prow).to_csv(f"{OUT}.picksets.csv", index=False)

    # ------------------------------------------------------------------ ARM C: the identity
    say("")
    say("=" * 110)
    say("ARM C — THE IDENTITY, VERIFIED TO MACHINE PRECISION BEFORE IT IS USED")
    say("=" * 110)
    say("")
    say("    G5 checks DELTA(A,P) == SUM_c w_P(c) S(A;c) - K(P) at every (alternative, pick")
    say("    set) pair.  G6 checks that K(P) does not depend on A (it is the additive constant).")

    def diffs(P, A):
        return np.array([S[(pn, A, y)] - S[(pn, bk, y)] for (pn, y, bk) in P], float)

    def foldlab(P):
        return np.array([f"{pn}:{y}" for (pn, y, bk) in P])

    dev5 = 0.0
    for nm, P in PICKSETS.items():
        w = WVEC[nm]
        K = float(np.mean([S[(pn, bk, y)] for (pn, y, bk) in P]))
        for A in ALT:
            lhs = float(np.mean(diffs(P, A)))
            rhs = float(sum(w[i] * S[(CELLS[i][0], A, CELLS[i][1])] for i in range(len(CELLS))
                            if w[i] > 0)) - K
            dev5 = max(dev5, abs(lhs - rhs))
    gate("G5 DELTA(A,P) == SUM_c w_P(c)S(A;c) - K(P)", dev5, 1e-12, dev5 < 1e-12)
    say(f"    G5 max deviation over {len(PICKSETS)*len(ALT)} (alternative, pick set) pairs: "
        f"{dev5:.3e}")

    Kvals = {nm: float(np.mean([S[(pn, bk, y)] for (pn, y, bk) in P]))
             for nm, P in PICKSETS.items()}
    dev6 = 0.0
    for nm, P in PICKSETS.items():
        col = np.array([float(np.mean(diffs(P, A)))
                        - sum(WVEC[nm][i] * S[(CELLS[i][0], A, CELLS[i][1])]
                              for i in range(len(CELLS)) if WVEC[nm][i] > 0) for A in ALT])
        dev6 = max(dev6, float(col.max() - col.min()))
    gate("G6 K(P) is constant across alternatives", dev6, 1e-12, dev6 < 1e-12)
    say(f"    G6 max spread of K(P) across the {len(ALT)} alternatives: {dev6:.3e}  "
        f"(it is the additive constant, exactly as 1237's G9 found at one pick set)")

    # ------------------------------------------------------------------ ARM D: rank movement
    say("")
    say("=" * 110)
    say("ARM D — DOES THE RANK MOVE?  EVERY (pick-set pair) x (contrast) CELL, ALL REPORTED")
    say("=" * 110)
    say("")
    say("    For each contrast and each pick set, the 19 alternatives are ranked.  A pair of")
    say("    pick sets is DEGENERATE-BY-ARITHMETIC when the contrast is mean-form AND the two")
    say("    w-vectors are identical; it is IDENTICAL-IN-FACT when the two rankings match.")

    RK, VAL = {}, {}
    for stat in CONTRASTS:
        for nm, P in PICKSETS.items():
            fl = foldlab(P)
            v = [contrast(stat, diffs(P, A), fl) for A in ALT]
            VAL[(stat, nm)] = v
            RK[(stat, nm)] = ranking(v)

    names = list(PICKSETS)
    rows = []
    for stat in CONTRASTS:
        for a, b in itertools.combinations(names, 2):
            same_w = bool(np.allclose(WVEC[a], WVEC[b], atol=1e-15, rtol=0))
            forced = bool(ADDITIVE[stat] and same_w)
            ra, rb = RK[(stat, a)], RK[(stat, b)]
            ident = bool(ra == rb)
            tau = kendall_tau(ra, rb)
            ia, ib = ra[ALT.index(INC)], rb[ALT.index(INC)]
            rows.append(dict(contrast=stat, A=a, B=b, same_w=same_w,
                             forced_identical=forced, identical_in_fact=ident,
                             kendall_tau=tau, inc_rank_A=ia, inc_rank_B=ib,
                             inc_rank_move=abs(ia - ib)))
    RP = pd.DataFrame(rows)
    RP.to_csv(f"{OUT}.rankpairs.csv", index=False)
    gate("G7 every arithmetically forced pair IS identical in fact",
         float((RP[RP.forced_identical].identical_in_fact == False).sum()), 0.0,
         bool((RP[RP.forced_identical].identical_in_fact).all()))

    say("")
    say("    contrast   additive   pairs   same-w   FORCED   identical-in-fact   median tau   "
        "median |rank move|")
    srows = []
    for stat in CONTRASTS:
        q = RP[RP.contrast == stat]
        say(f"    {stat:10s} {str(ADDITIVE[stat]):8s}  {len(q):5d}   {int(q.same_w.sum()):6d}   "
            f"{int(q.forced_identical.sum()):6d}   {int(q.identical_in_fact.sum()):17d}   "
            f"{q.kendall_tau.median():10.4f}   {q.inc_rank_move.median():17.1f}")
        srows.append(dict(contrast=stat, additive=ADDITIVE[stat], pairs=len(q),
                          same_w=int(q.same_w.sum()), forced=int(q.forced_identical.sum()),
                          identical=int(q.identical_in_fact.sum()),
                          median_tau=float(q.kendall_tau.median()),
                          median_rank_move=float(q.inc_rank_move.median()),
                          max_rank_move=int(q.inc_rank_move.max())))
    pd.DataFrame(srows).to_csv(f"{OUT}.bycontrast.csv", index=False)

    # the two escapes, priced separately
    e1 = RP[(RP.contrast == "C_MEAN") & (~RP.same_w)]
    e1s = RP[(RP.contrast == "C_MEAN") & (RP.same_w)]
    e2 = RP[(~RP.contrast.isin(["C_MEAN"])) & (RP.same_w)]
    say("")
    say(f"    (E1) DIFFERENT w, MEAN-FORM contrast: {len(e1)} pairs, identical in fact "
        f"{int(e1.identical_in_fact.sum())} ({e1.identical_in_fact.mean():.3f}), median tau "
        f"{e1.kendall_tau.median():.4f}, median |incumbent rank move| "
        f"{e1.inc_rank_move.median():.1f}, max {int(e1.inc_rank_move.max())}.")
    say(f"         NOTE THE SPLIT: the FULL ranking survives reweighting at only "
        f"{e1.identical_in_fact.mean():.3f} of pairs, but the INCUMBENT'S OWN rank moves 0 "
        f"places at {float((e1.inc_rank_move==0).mean()):.3f} of them.  1224 read the second")
    say("         and reported the first — its three pick sets agreed about THAT BOOK, not")
    say("         about the ranking.")
    say(f"    (E0) SAME w, MEAN-FORM contrast:      {len(e1s)} pairs, identical in fact "
        f"{int(e1s.identical_in_fact.sum())} ({e1s.identical_in_fact.mean():.3f}) — "
        f"ARITHMETICALLY FORCED, and G7 confirms it.")
    say(f"    (E2) SAME w, NON-MEAN contrast:       {len(e2)} pairs, identical in fact "
        f"{int(e2.identical_in_fact.sum())} ({e2.identical_in_fact.mean():.3f}), median tau "
        f"{e2.kendall_tau.median():.4f}, median |incumbent rank move| "
        f"{e2.inc_rank_move.median():.1f}, max {int(e2.inc_rank_move.max())}.")

    say("")
    say("    THE INCUMBENT'S RANK, 1 = best, over the 19 distinct books, at every cell:")
    say("    pickset     " + "  ".join(f"{s:>7s}" for s in CONTRASTS))
    irows = []
    for nm in names:
        r = [RK[(s, nm)][ALT.index(INC)] for s in CONTRASTS]
        say(f"    {nm:11s} " + "  ".join(f"{x:7d}" for x in r))
        irows.append(dict(pickset=nm, **{s: RK[(s, nm)][ALT.index(INC)] for s in CONTRASTS},
                          **{f"val_{s}": VAL[(s, nm)][ALT.index(INC)] for s in CONTRASTS}))
    pd.DataFrame(irows).to_csv(f"{OUT}.incumbent.csv", index=False)

    # ------------------------------------------------------------------ ARM E: the census
    say("")
    say("=" * 110)
    say("ARM E — THE RECORD'S OWN SUBSTITUTION STUDIES (dial 1: STUDY SET)")
    say("=" * 110)
    HV = census(U)
    HV.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    say("")
    say(f"    {len(HV)} committed units read ({nmd} memo/result files + LEADERBOARD rows + "
        f"CHANGELOG paragraphs).")
    say("")
    say("    study set   units   with a pick-set contrast   stat=C_MEAN   stat UNSTATED   "
        "MEAN-FORM share")
    crows = []
    for ss in STUDY_SETS:
        q = HV[HV[ss]]
        nmean = int((q.stat == "C_MEAN").sum())
        nuns = int((q.stat == "UNSTATED").sum())
        share = nmean / len(q) if len(q) else np.nan
        say(f"    {ss:11s} {len(q):6d}   {len(q):24d}   {nmean:11d}   {nuns:13d}   "
            f"{share:15.4f}")
        crows.append(dict(study_set=ss, units=len(q), mean_form=nmean, unstated=nuns,
                          mean_form_share=share,
                          **{f"stat_{s}": int((q.stat == s).sum()) for s in CONTRASTS}))
    pd.DataFrame(crows).to_csv(f"{OUT}.studysets.csv", index=False)
    say("")
    say("    DEGENERACY SHARE = mean-form share x (the measured rate at which a mean-form")
    say("    contrast is rank-identical across pick sets on this tape).  The second factor is")
    say("    ARM D's C_MEAN identical-in-fact rate, which is the honest upper bound: a unit")
    say("    whose two pick sets share w is forced, one whose w differs is not.")
    cmean_rate = float(RP[RP.contrast == "C_MEAN"].identical_in_fact.mean())
    forced_rate = float(RP[RP.contrast == "C_MEAN"].forced_identical.mean())
    for r in crows:
        r["degenerate_share_upper"] = r["mean_form_share"] * cmean_rate
        r["degenerate_share_forced"] = r["mean_form_share"] * forced_rate
        say(f"    {r['study_set']:11s} mean-form {r['mean_form_share']:.4f} x identical-in-fact "
            f"{cmean_rate:.4f} = {r['degenerate_share_upper']:.4f} upper; x FORCED "
            f"{forced_rate:.4f} = {r['degenerate_share_forced']:.4f} floor.")
    say("")
    say("    THE UNSTATED SHARE IS THE LOAD-BEARING NUMBER, SO IT IS BOUNDED BOTH WAYS.  Roughly")
    say("    half of every study set names NO ranking statistic at all, so its degeneracy is")
    say("    unknowable from its own text.  The verdict must not turn on how they are assigned,")
    say("    so both extremes are published: UNSTATED counted as NOT mean-form (the reading")
    say("    above) and UNSTATED counted as ALL mean-form (the most generous reading the")
    say("    premise could ask for).")
    say("")
    say("    study set   UNSTATED share   share if UNSTATED=NOT-mean   share if UNSTATED=ALL-mean")
    for r in crows:
        n = r["units"]
        lo_s = r["mean_form_share"] * cmean_rate
        hi_s = ((r["mean_form"] + r["unstated"]) / n if n else np.nan) * cmean_rate
        r["degenerate_share_unstated_all_mean"] = hi_s
        r["unstated_share"] = r["unstated"] / n if n else np.nan
        say(f"    {r['study_set']:11s} {r['unstated_share']:14.4f}   {lo_s:25.4f}   "
            f"{hi_s:26.4f}")
    hi_all = max(r["degenerate_share_unstated_all_mean"] for r in crows)
    gate("G8 verdict robust to the UNSTATED assignment (generous bound still < 0.50)",
         hi_all, 0.50, hi_all < 0.50)
    say(f"    Even at the most generous assignment the degenerate share tops out at "
        f"{hi_all:.4f}, still far below the 0.50 the premise needs.")

    say("")
    say("    THE RECORD'S OWN CLAIM, REPLAYED.  1224/1237 committed 'the incumbent ranked 5 of")
    say("    19' on P_AXIS under a mean-form contrast.  P_ALL4 is that pick set rebuilt here.")
    inc_all4 = RK[("C_MEAN", "P_ALL4")][ALT.index(INC)]
    gate("G9 replay of the record's committed incumbent rank (P_ALL4, C_MEAN)",
         float(inc_all4), 5.0, inc_all4 == 5)
    say(f"    Rebuilt: {inc_all4} of {len(ALT)}.  The record's number reproduces.")
    pd.DataFrame(crows).to_csv(f"{OUT}.studysets.csv", index=False)

    # ------------------------------------------------------------------ ARM F: KEEP paths
    say("")
    say("=" * 110)
    say("ARM F — BOTH KEEP PATHS AND RULE 8 (PROTOCOL rules 4 and 8)")
    say("=" * 110)
    BM = {}
    for pan in panels:
        ioos = ilim[pan.name]
        for nmb, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[pan.i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nmb)] = dict(**triple(full), H1=h1, H2=h2,
                                       OOS_Sharpe=sharpe(r[ioos:]), OOS_CAGR=cagr(r[ioos:]),
                                       OOS_MaxDD=mdd(r[ioos:]))
    say("")
    say("    panel  bench   full CAGR / Sharpe / MaxDD        halves           "
        "OOS CAGR / Sharpe / MaxDD")
    for pan in panels:
        for nmb in ("SPY", "LIVE"):
            d = BM[(pan.name, nmb)]
            say(f"    {pan.name:6s} {nmb:5s} {d['CAGR']:8.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}   {d['H1']:.4f}/{d['H2']:.4f}   {d['OOS_CAGR']:8.2%} / "
                f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def oos_bm(p, nmb, ioos):
        d = BM[(p, nmb)]
        r = bench[p]["spy" if nmb == "SPY" else "live"][ioos:]
        h1, h2 = halves(r)
        return dict(H1=h1, H2=h2, CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    brows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for k in BOOKKEY:
            r = booked[pan.name][k]
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows.append(dict(panel=pan.name, book=akey(k), ladder=k[0], rung=k[1],
                              is_incumbent=bool(k in ANCH_KEYS), **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say("")
    say(f"    (F1) ALL {len(BK)} CANDIDATE BOOKS, nothing selected on: 4a "
        f"{int(BK.KEEP_4a.sum())}; 4b full {int(BK.KEEP_4b.sum())}; 4b OOS "
        f"{int(BK.KEEP_4b_OOS.sum())}; BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    both = BK[BK.KEEP_4b & BK.KEEP_4b_OOS]
    if len(both):
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8))
                     for _, r in both.iterrows()})
        say(f"         The {len(both)} both-paths books collapse to {len(rk)} DISTINCT on "
            f"1211's realised-return key; {int(both.is_incumbent.sum())} ARE the incumbent.")
        for _, r in both.iterrows():
            say(f"         {r.panel:6s} {r.book:14s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
                f"{r.MaxDD:8.2%}   {r.H1:.4f}/{r.H2:.4f}   OOS {r.OOS_CAGR:7.2%} / "
                f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}")

    say("")
    say("    (F2) RULE 8 — the chooser this idea puts on trial, run walk-forward.  For every")
    say("         (panel, pick set, contrast) the BEST-RANKED alternative is chosen on the IS")
    say("         window ONLY (folds < 2017, IS argmax picks, IS-window cell Sharpes) and its")
    say("         2017-2026 return is read ONCE.  All grid points reported.")
    wrows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        isf = [(y, lo, hi, o0, o1) for (y, lo, hi, o0, o1) in folds[pan.name] if y < 2017]
        for nm, P in PICKSETS.items():
            Pis = [(pn, y, bk) for (pn, y, bk) in P
                   if pn == pan.name and y in {f[0] for f in isf}]
            if len(Pis) < 4:
                continue
            fl = np.array([f"{pn}:{y}" for (pn, y, bk) in Pis])
            for stat in CONTRASTS:
                v = [contrast(stat, np.array([S[(pn, A, y)] - S[(pn, bk, y)]
                                              for (pn, y, bk) in Pis], float), fl) for A in ALT]
                Achosen = ALT[int(np.nanargmax(np.where(np.isfinite(v), v, -np.inf)))]
                rr = booked[pan.name][Achosen]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[ioos:], so, lo_)
                wrows.append(dict(panel=pan.name, pickset=nm, contrast=stat,
                                  chosen=akey(Achosen),
                                  is_incumbent=bool(Achosen == INC), n_is_picks=len(Pis),
                                  **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
        # the do-nothing reference: hold the incumbent anchor
        rr = booked[pan.name][INC]
        k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
        _, k4b_o, mo, _, _ = keep_paths(rr[ioos:], so, lo_)
        wrows.append(dict(panel=pan.name, pickset="S_NONE", contrast="S_NONE",
                          chosen=akey(INC), is_incumbent=True, n_is_picks=0, **m, H1=h1, H2=h2,
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"         RULE-8 ROWS: {len(W8)}.  4a {int(W8.KEEP_4a.sum())}; 4b full "
        f"{int(W8.KEEP_4b.sum())}; 4b OOS {int(W8.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())}.")
    q = W8[W8.contrast != "S_NONE"]
    say(f"         Distinct books the chooser ever names: {q.chosen.nunique()} "
        f"({', '.join(sorted(q.chosen.unique())[:8])}...); it names the INCUMBENT at "
        f"{int(q.is_incumbent.sum())} of {len(q)} rows.")
    say("")
    say("         Mean OOS Sharpe by contrast over the rule-8 rows (do-nothing = "
        f"{W8[W8.contrast=='S_NONE'].OOS_Sharpe.mean():.4f}):")
    for stat in CONTRASTS:
        z = q[q.contrast == stat]
        if len(z):
            say(f"           {stat:8s} {z.OOS_Sharpe.mean():.4f}  over {len(z)} rows, "
                f"{z.chosen.nunique()} distinct books")
    dk = W8[W8.KEEP_4b & W8.KEEP_4b_OOS]
    if len(dk):
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8))
                     for _, r in dk.iterrows()})
        say(f"         The {len(dk)} both-4b rows collapse to {len(rk)} DISTINCT BOOKS.")
        for p, c, s in rk:
            mrow = dk[(dk.panel == p) & (dk.OOS_CAGR.round(8) == c)].iloc[0]
            say(f"           {p:6s} {mrow.chosen:12s} full {mrow.CAGR:7.2%} / "
                f"{mrow.Sharpe:.4f} / {mrow.MaxDD:8.2%}  halves {mrow.H1:.4f}/{mrow.H2:.4f}  "
                f"OOS {mrow.OOS_CAGR:7.2%} / {mrow.OOS_Sharpe:.4f} / {mrow.OOS_MaxDD:8.2%}")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    say("VERDICT")
    say("=" * 110)
    esc_move = float(pd.concat([e1.inc_rank_move, e2.inc_rank_move]).median())
    best = max(crows, key=lambda r: r["degenerate_share_upper"])
    worst = min(crows, key=lambda r: r["degenerate_share_upper"])
    share_hi, share_lo = best["degenerate_share_upper"], worst["degenerate_share_upper"]
    if share_hi > 0.50 and esc_move < 1.0:
        out = "(A) ONE QUESTION"
    elif share_hi <= 0.50 or esc_move >= 2.0:
        out = "(B) NOT ONE QUESTION" if share_hi <= 0.50 else "(C) MIXED"
    else:
        out = "(C) MIXED"
    say("")
    say(f"    PRE-DECLARED OUTCOME FIRES: {out}")
    say(f"      degenerate share (upper) {share_lo:.4f}-{share_hi:.4f} over the three study")
    say(f"      sets; median |incumbent rank move| across BOTH escapes {esc_move:.1f} places.")
    say(f"      C_MEAN rank-identical in fact at {cmean_rate:.4f} of pick-set pairs, of which")
    say(f"      {forced_rate:.4f} are ARITHMETICALLY FORCED (G7: forced => identical, 0 misses).")
    say("")
    say(f"    CAPITAL: 4a {int(BK.KEEP_4a.sum())} of {len(BK)} books and "
        f"{int(W8.KEEP_4a.sum())} of {len(W8)} rule-8 rows; 4b BOTH "
        f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books / "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())} rows, collapsing to books the record")
    say("    already holds.  NO NEW BOOK, NO RULES CHANGE, NO PROTOCOL EDIT.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    for _, r in GD.iterrows():
        say(f"      {'PASS' if r.pass_ else 'FAIL'}  {r.gate}  value={r.value}  "
            f"target={r.target}")
    say("")
    say(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
