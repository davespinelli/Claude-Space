#!/usr/bin/env python3
"""
Idea 1238 (lane cloud, 2026-09-17) — must every committed TUNING COST in the record NAME ITS
ANCHOR?

THE PREMISE, READ FROM THE RECORD.  Idea 1224 priced the record's tuning cost as
DELTA = OOS Sharpe(substituted book) - OOS Sharpe(the book the record picked) and published
+0.0204 over 620 committed pick-cells.  Idea 1237 then walked the ANCHOR itself over the
record's own 22 rung books (19 distinct, its gate G5) and found the SAME 620 cells price
anywhere from -0.3292 to +0.1105 of OOS Sharpe depending only on which book stands in as the
anchor, with the SIGN flipping at 4 of the 19.  Every committed "tuning costs X" /
"the substitution is worth X" figure in the record was therefore measured against ONE
counterfactual that the sentence carrying the figure may never have named.

THE QUESTION, IN TWO ARMS, BOTH PRE-DECLARED:

  ARM 1  THE CENSUS.  Harvest every committed unit in the record (LEADERBOARD.md,
         CHANGELOG.md, every research/backtests/*.md) that states a SIGNED PRICE in
         substitution / tuning-cost language, and classify each by how completely it names its
         anchor:  A_FULL   the unit states a rung for all four ladders (N, H, GROSS, CADENCE) —
                           the comparand book is fully identified from the sentence alone;
                  A_PARTIAL the unit uses a comparand word (anchor / against / vs / incumbent /
                           baseline / comparand / substitut*) and names >= 1 ladder rung;
                  A_NONE    neither — the figure stands with no comparand recoverable from it.

  ARM 2  THE RE-PRICE.  For every CHECKABLE claim (one that names a panel AND a rebuildable
         ladder rung AND carries rule-8 / pick language — 1224's checkability test), re-price
         its own cells against each candidate anchor A:

             DELTA_c(A) = mean over c's cells [ OOS Sharpe(A) - OOS Sharpe(the book c names) ]

         over the 10 OOS fold-years, SE clustered on fold (1214's estimator), and report how
         many claims KEEP THE SIGN of their committed figure across the candidate set.
         COMMITTED SIGN is the sign of the largest-|.| signed figure in the unit (declared
         here, before any number is read; ties broken by first occurrence).

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) THE ANCHOR MUST BE NAMED — a majority of committed tuning-cost figures are A_NONE AND
      the median checkable claim keeps its sign at <= 0.75 of the candidate set.  The schema
      clause is earned: no tuning-cost figure without its anchor.
  (B) THE ANCHOR IS INERT — >= 0.75 of checkable claims keep their sign at EVERY candidate.
      Naming the anchor would be book-keeping, not information.
  (C) NEITHER — the census and the re-price disagree, or both land inside the bands above.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET      {C_STRICT, C_LOOSE, C_ALL}
                 C_STRICT  substitution/tuning language AND a signed figure AND the word Sharpe
                 C_LOOSE   substitution/tuning/cost/worth language AND a signed figure
                 C_ALL     any committed unit carrying a signed figure at all
  CANDIDATE SET  {A19, A_REAL9, A_RULE8}
                 A19     the record's 19 distinct rung books (1237 G5)
                 A_REAL9 A19 minus the 9 GROSS rungs, which 1237's G12 shows are the incumbent
                         RE-LEVERED (Sharpe gap < 0.005) — the genuinely different stand-ins
                 A_RULE8 only candidates an IS-argmax chooser could have named on
                         warm-up..2016-12-31 (rule 8 legal), one per panel, plus the incumbent

FROZEN, NOT DIALLED: the substitution rule at S_ALL (1224: the resolution qualifiers S_SE1 /
S_SE2 / S_ANC95 are decision-identical at 0 of 620 cells, so carrying one spends a dial on a
no-op).  The record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, 10 bps (rule 2), decide-at-t / apply-at-t+1, warm-up 260 rows.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the four ladders; the
14 folds; the 4a and 4b legs; the IS and OOS windows.

THE TRADABLE ARM (rule 8).  A census is not a book, so the run also prices the POLICY the
census implies, made decidable on IS data only:

  S_NONE   at each fold, hold the ladder's IS-argmax rung (the record's habit: tune).
  S_ALL    at each fold, hold the frozen anchor instead (1224's substitution).
  S_SIGN   at each fold, compute on the IS WINDOW ONLY the sign of (anchor - IS-argmax) against
           every candidate in the candidate set; hold the anchor iff a strict majority of the
           candidates agree on a POSITIVE sign, else hold the IS-argmax rung.  This is
           "require the claim to keep its sign across the candidate set before acting on it",
           made rule-8 legal.

Each policy's fold-year OOS segments are concatenated into ONE tradable daily curve per
(panel, ladder, policy) and scored on BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY),
full sample / halves / OOS.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths on every rung book, every rule-8 row and
every stitched curve; rule 9 survivorship stated (SMALL and B136 are CURRENT constituents).
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_must-every-committed-TUNING-COST-in-the-record-NAME-ITS-ANCHOR_cloud.py
"""
from __future__ import annotations

import hashlib
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
SLUG = "must-every-committed-TUNING-COST-in-the-record-NAME-ITS-ANCHOR"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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
CLAIM_SETS = ["C_STRICT", "C_LOOSE", "C_ALL"]
CAND_SETS = ["A19", "A_REAL9", "A_RULE8"]
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


# ==================================================================== panels / runner (1224's)
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


def clustered(d, fold):
    s = pd.Series(np.asarray(d, float))
    f = pd.Series(np.asarray(fold))
    ok = s.notna()
    s, f = s[ok], f[ok]
    if len(s) == 0:
        return np.nan, np.nan, np.nan, 0, 0
    fm = s.groupby(f.values).mean()
    se = float(fm.std(ddof=1) / np.sqrt(len(fm))) if len(fm) > 1 else np.nan
    m = float(s.mean())
    t = m / se if se and se > 0 else 0.0
    return m, se, float(t), len(s), len(fm)


def akey(k):
    return f"{k[0]}={k[1]}"


# ==================================================================== the record's own text
UNIT_R8 = re.compile(r"\b(rule[- ]?8|walk[- ]?forward|out[- ]of[- ]sample|OOS)\b", re.I)
UNIT_PICK = re.compile(r"\b(pick|picks|picked|chose|chosen|choose|argmax|select|selects|"
                       r"selected|chooser)\b", re.I)
PANEL_R = re.compile(r"\b(U56|B136|SMALL)\b")
R_N = re.compile(r"\bN\s*=\s*(\d+)\b")
R_H = re.compile(r"\bH\s*=\s*(\d+)\b")
R_G = re.compile(r"\b(?:gross|g)\s*[= ]\s*(0?\.\d{2})\b", re.I)
R_C = re.compile(r"\b(weekly|monthly)\b", re.I)

# ARM 1's three language screens and the signed-figure form the record actually writes.
FIG = re.compile(r"(?<![\w.])([+-]\d\.\d{3,4})(?![\d])")
SUBST = re.compile(r"\b(tuning cost|substitut\w*|counterfactual|stand[- ]in|replace\w*|"
                   r"stop tuning|instead of the|in place of|anchor\w*)\b", re.I)
PRICE = re.compile(r"\b(cost\w*|worth|pays?|paid|price[ds]?|prices|rebate|gain\w*|buys?|"
                   r"penalt\w*|charge\w*)\b", re.I)
SHARPE = re.compile(r"\bSharpe\b", re.I)
COMPARAND = re.compile(r"\b(anchor\w*|against|versus|vs\.?|incumbent|baseline|comparand|"
                       r"substitut\w*|relative to|compared (?:to|with))\b", re.I)


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


def rungs_in(txt):
    trip = []
    for m in R_N.finditer(txt):
        v = int(m.group(1))
        if v in LAD["N"]:
            trip.append(("N", v))
    for m in R_H.finditer(txt):
        v = int(m.group(1))
        if v in LAD["H"]:
            trip.append(("H", v))
    for m in R_G.finditer(txt):
        v = round(float(m.group(1)), 2)
        if v in LAD["GROSS"]:
            trip.append(("GROSS", v))
    for m in R_C.finditer(txt):
        trip.append(("CADENCE", "W" if m.group(1).lower() == "weekly" else "M"))
    return sorted(set(trip), key=lambda x: (LADS.index(x[0]), str(x[1])))


def harvest(U):
    """One row per committed unit: the census fields (ARM 1) and the checkability fields
    (ARM 2, 1224's test) computed once, together."""
    rows = []
    for src, txt in U:
        figs = [float(x) for x in FIG.findall(txt)]
        has_fig = len(figs) > 0
        s_sub, s_pri, s_shp = bool(SUBST.search(txt)), bool(PRICE.search(txt)), bool(SHARPE.search(txt))
        c_strict = has_fig and s_sub and s_pri and s_shp
        c_loose = has_fig and (s_sub or s_pri)
        c_all = has_fig
        trip = rungs_in(txt)
        lads_named = sorted({a for a, _ in trip})
        a_full = len(lads_named) == 4
        a_part = (not a_full) and bool(COMPARAND.search(txt)) and len(trip) > 0
        anchor = "A_FULL" if a_full else ("A_PARTIAL" if a_part else "A_NONE")
        r8, pk = bool(UNIT_R8.search(txt)), bool(UNIT_PICK.search(txt))
        pans = sorted(set(PANEL_R.findall(txt)))
        big = max(figs, key=abs) if figs else np.nan
        rows.append(dict(
            uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
            n_fig=len(figs), committed_figure=big,
            committed_sign=(0 if not figs else (1 if big > 0 else -1)),
            LANG_SUBST=s_sub, LANG_PRICE=s_pri, LANG_SHARPE=s_shp,
            C_STRICT=c_strict, C_LOOSE=c_loose, C_ALL=c_all,
            ANCHOR_CLASS=anchor, n_ladders_named=len(lads_named),
            RULE8=r8, PICK=pk, n_panels=len(pans), panels="|".join(pans),
            n_triples=len(trip), triples="|".join(f"{a}={b}" for a, b in trip),
            CHECKABLE=bool(r8 and pk and pans and trip)))
    return pd.DataFrame(rows)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1238 (lane cloud, 2026-09-17) — must every committed TUNING COST in the record")
    say("NAME ITS ANCHOR?")
    say("=" * 110)
    say("")
    say("  ARM 1 CENSUS: of the record's committed signed prices in substitution language, how")
    say("        many name the comparand book they were measured against?")
    say("  ARM 2 RE-PRICE: DELTA_c(A) = mean over c's own cells [OOS Sharpe(A) - OOS Sharpe(the")
    say("        book c names)]; how many claims KEEP THE SIGN of their committed figure across")
    say("        the candidate set?")
    say("  PRE-DECLARED: (A) THE ANCHOR MUST BE NAMED — majority A_NONE and median sign-keep")
    say("        <= 0.75.  (B) THE ANCHOR IS INERT — >= 0.75 of claims keep their sign at EVERY")
    say("        candidate.  (C) NEITHER.")

    # ------------------------------------------------------------------ panels and rung books
    say("")
    say("=" * 110)
    say("ARM A — PANELS, THE 22 CANDIDATE ANCHOR BOOKS, FOLDS")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv").set_index("ticker")
    bad = set(meta.index[meta.max_1d_move >= 1.0])
    inv = [c for c in pxS.columns if c != "SPY" and c not in bad]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped on data/small_meta.csv max_1d_move >= 1.0); "
        f"SPY benchmark only.")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents of their screens — "
        "names that")
    say("  delisted or were acquired are absent, so every level on those two panels is biased "
        "high.  This")
    say("  run's headline is a WITHIN-panel sign comparison, which the bias does not move, but "
        "the levels are not tradable as printed.")

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
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]), f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(books)} candidate anchor books built.")

    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    INC = ("N", A_N)

    # ---- machinery gates (1237's G1-G5, replayed)
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    lm = mdd(bench["U56"]["live"][WARMUP:])
    gate("G2 live RULES v2 U56 MaxDD == the record's committed -12.05%", lm,
         LIVE_MAXDD_COMMITTED, abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    g3 = 0.0
    for pn in booked:
        a0 = booked[pn][ANCH_KEYS[0]]
        g3 = max(g3, float(max(np.abs(booked[pn][k] - a0).max() for k in ANCH_KEYS)))
    gate("G3 the anchor rung of all four ladders is ONE book bit for bit, on all 3 panels",
         g3, 0.0, g3 == 0.0)
    ndist = {}
    for pn in booked:
        seen = []
        for k in BOOKKEY:
            r = booked[pn][k][WARMUP:]
            if not any(np.array_equal(r, s) for s in seen):
                seen.append(r)
        ndist[pn] = len(seen)
    gate("G4 the 22 candidate keys collapse to 19 DISTINCT books on every panel",
         float(min(ndist.values())), 19.0, all(v == 19 for v in ndist.values()))
    say(f"    G1 {g1:.3e}   G2 live U56 MaxDD {lm:.4%}   G3 {g3:.3e}   G4 distinct {ndist}")

    # ---- folds
    folds = {}
    for pan in panels:
        yrs = pan.idx.year.values
        cover = []
        for y in FOLD_YEARS:
            oo = np.flatnonzero(yrs == y)
            oo = oo[oo >= pan.i0]
            if len(oo) < 60:
                continue
            lo, hi = pan.i0, int(oo[0])
            if hi - lo < 252:
                continue
            cover.append((int(oo[0]), int(oo[-1]) + 1))
            folds.setdefault(pan.name, []).append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        gate(f"G5 folds tile {pan.name} with no overlap and no gap", float(gap), 0.0, gap == 0)
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")

    FS, FSEG = {}, {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            for k in BOOKKEY:
                FS[(pan.name, k, y)] = sharpe(booked[pan.name][k][o0:o1])
                FSEG[(pan.name, k, y)] = booked[pan.name][k][o0:o1]
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}

    def is_sharpe(p, k, lo, hi):
        return sharpe(booked[p][k][lo:hi])

    def argmax_rung(p, lad, lo, hi):
        v = [(is_sharpe(p, (lad, r), lo, hi), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    def argmax_book(p, lo, hi):
        v = [(is_sharpe(p, k, lo, hi), i) for i, k in enumerate(BOOKKEY)]
        v = [(s, i) for s, i in v if np.isfinite(s)]
        return BOOKKEY[max(v)[1]] if v else None

    # ---- the three CANDIDATE SETS (dial 2)
    DISTINCT = [k for k in BOOKKEY if k == INC or k not in ANCH_KEYS]   # 19 distinct keys
    GROSS_OTHERS = [k for k in DISTINCT if k[0] == "GROSS" and k != INC]
    A_IS = {pan.name: argmax_book(pan.name, pan.i0, ilim[pan.name]) for pan in panels}
    CAND = {
        "A19": DISTINCT,
        "A_REAL9": [k for k in DISTINCT if k not in GROSS_OTHERS],
        "A_RULE8": sorted({INC, *A_IS.values()}, key=lambda k: (LADS.index(k[0]), str(k[1]))),
    }
    say("")
    say("  CANDIDATE SETS (dial 2): "
        + "; ".join(f"{n} n={len(v)}" for n, v in CAND.items()))
    say(f"    A_RULE8 = the incumbent plus the IS-argmax-over-22 book per panel: "
        + ", ".join(f"{p}->{akey(A_IS[p])}" for p in A_IS))
    gate("G6 A_REAL9 drops exactly the 9 non-incumbent GROSS rungs",
         float(len(CAND["A19"]) - len(CAND["A_REAL9"])), 9.0,
         len(CAND["A19"]) - len(CAND["A_REAL9"]) == 9)

    # ------------------------------------------------------------------ ARM 1: the census
    say("")
    say("=" * 110)
    say("ARM 1 — THE CENSUS: DOES A COMMITTED TUNING-COST FIGURE NAME ITS ANCHOR?")
    say("=" * 110)
    U, nmd = units()
    HV = harvest(U)
    HV.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    say("")
    say(f"  {len(HV):,} committed units harvested (LEADERBOARD.md rows + CHANGELOG.md "
        f"paragraphs + {nmd:,} research/backtests/*.md paragraphs).")
    say(f"  {int(HV.C_ALL.sum()):,} carry at least one signed figure of the record's own "
        f"[+-]d.dddd form.")
    say("")
    say("  claim set   n claims   A_FULL           A_PARTIAL        A_NONE          "
        "names the anchor")
    cen = []
    for cs in CLAIM_SETS:
        g = HV[HV[cs]]
        n = len(g)
        cnt = {k: int((g.ANCHOR_CLASS == k).sum()) for k in ("A_FULL", "A_PARTIAL", "A_NONE")}
        named = cnt["A_FULL"]
        cen.append(dict(claim_set=cs, n=n, **cnt,
                        share_FULL=cnt["A_FULL"] / n if n else np.nan,
                        share_PARTIAL=cnt["A_PARTIAL"] / n if n else np.nan,
                        share_NONE=cnt["A_NONE"] / n if n else np.nan,
                        n_checkable=int(g.CHECKABLE.sum())))
        say(f"  {cs:10s} {n:8,d}   {cnt['A_FULL']:6,d} ({cnt['A_FULL']/max(n,1):.3f})  "
            f"{cnt['A_PARTIAL']:6,d} ({cnt['A_PARTIAL']/max(n,1):.3f})  "
            f"{cnt['A_NONE']:6,d} ({cnt['A_NONE']/max(n,1):.3f})   {named/max(n,1):.3f}")
    CEN = pd.DataFrame(cen)
    CEN.to_csv(f"{OUT}.census_summary.csv", index=False)
    say("")
    say("  A_FULL requires all four ladder rungs in the SAME unit — the strictest reading of")
    say("  'names its anchor', and the only one from which the comparand book is rebuildable")
    say("  without reading another document.  A_PARTIAL units use a comparand word and name at")
    say("  least one rung; their anchor is recoverable only by convention.")

    # ------------------------------------------------------------------ ARM 2: the re-price
    say("")
    say("=" * 110)
    say("ARM 2 — THE RE-PRICE: HOW MANY COMMITTED FIGURES KEEP THEIR SIGN?")
    say("=" * 110)
    OOS_FOLDS = {p: [f for f in folds[p] if f[0] >= 2017] for p in folds}
    say("")
    say(f"  Each checkable claim is priced on its OWN cells: its panels x its named rungs x the "
        f"{len(OOS_FOLDS['U56'])} OOS fold-years.")
    say("  DELTA_c(A) = mean over those cells [OOS Sharpe(A) - OOS Sharpe(the book c names)].")

    rows, cells = [], []
    for cs in CLAIM_SETS:
        sub = HV[HV[cs] & HV.CHECKABLE & (HV.committed_sign != 0)]
        for _, c in sub.iterrows():
            cpans = [p for p in c.panels.split("|") if p in folds]
            ctrip = []
            for tk in c.triples.split("|"):
                lad, rv = tk.split("=")
                rung = (rv if lad == "CADENCE"
                        else (round(float(rv), 2) if lad == "GROSS" else int(rv)))
                ctrip.append((lad, rung))
            base, fold_of = [], []
            for p in cpans:
                for (lad, rung) in ctrip:
                    for (y, _lo, _hi, _o0, _o1) in OOS_FOLDS[p]:
                        base.append((p, (lad, rung), y))
                        fold_of.append(y)
            if not base:
                continue
            picked = np.array([FS[b] for b in base], float)
            for csname, keys in CAND.items():
                dl = []
                for A in keys:
                    d = np.array([FS[(p, A, y)] for (p, _k, y) in base], float) - picked
                    m, se, t, n, ng = clustered(d, fold_of)
                    dl.append((akey(A), m, se, t))
                    if csname == "A19" and cs == "C_STRICT":
                        cells.append(dict(uid=c.uid, src=c.src, anchor=akey(A), DELTA=m,
                                          SE=se, t=t, n_cells=n))
                sgn = int(c.committed_sign)
                keep = [x for x in dl if (np.isfinite(x[1]) and (1 if x[1] > 0 else -1) == sgn)]
                rows.append(dict(claim_set=cs, cand_set=csname, uid=c.uid, src=c.src,
                                 committed=c.committed_figure, sign=sgn,
                                 n_cells=len(base), n_cand=len(dl),
                                 n_keep=len(keep), share_keep=len(keep) / len(dl),
                                 all_keep=len(keep) == len(dl), none_keep=len(keep) == 0,
                                 D_min=float(np.nanmin([x[1] for x in dl])),
                                 D_max=float(np.nanmax([x[1] for x in dl])),
                                 D_med=float(np.nanmedian([x[1] for x in dl]))))
    R = pd.DataFrame(rows)
    R.to_csv(f"{OUT}.reprice.csv.gz", index=False, compression="gzip")
    pd.DataFrame(cells).to_csv(f"{OUT}.cells.csv.gz", index=False, compression="gzip")

    say("")
    say("  claim set  cand set   claims   median share keeping sign   ALL keep   NONE keep   "
        "median spread D_max-D_min")
    grid = []
    for cs in CLAIM_SETS:
        for csn in CAND_SETS:
            g = R[(R.claim_set == cs) & (R.cand_set == csn)]
            if not len(g):
                continue
            spread = float((g.D_max - g.D_min).median())
            grid.append(dict(claim_set=cs, cand_set=csn, n_claims=len(g),
                             median_share_keep=float(g.share_keep.median()),
                             mean_share_keep=float(g.share_keep.mean()),
                             share_all_keep=float(g.all_keep.mean()),
                             share_none_keep=float(g.none_keep.mean()),
                             median_spread=spread,
                             median_D_med=float(g.D_med.median())))
            say(f"  {cs:10s} {csn:9s} {len(g):7,d}   {g.share_keep.median():.4f}"
                f"                    {g.all_keep.mean():.4f}     {g.none_keep.mean():.4f}"
                f"     {spread:.4f}")
    GR = pd.DataFrame(grid)
    GR.to_csv(f"{OUT}.grid.csv", index=False)
    say("")
    say("  ALL NINE (claim set x candidate set) CELLS ARE PUBLISHED ABOVE — no cell is chosen.")

    # the additivity identity (1237 G9): the anchor column carries no claim information
    if len(cells):
        CC = pd.DataFrame(cells)
        piv = CC.pivot_table(index="uid", columns="anchor", values="DELTA")
        rng = (piv.max(axis=1) - piv.min(axis=1))
        say("")
        say(f"  MECHANICAL NOTE (1237 G9 replayed): DELTA_c(A) = meanOOS(A over c's cells) - "
            f"meanOOS(c's own book),")
        say(f"  so the whole candidate spread at a claim is the ANCHOR column's spread, not the "
            f"claim's.  Median spread over")
        say(f"  the {len(piv)} C_STRICT checkable claims is {rng.median():.4f} of OOS Sharpe "
            f"against the record's typical committed figure of "
            f"{HV[HV.C_STRICT].committed_figure.abs().median():.4f}.")
        g7 = float(rng.median() / max(HV[HV.C_STRICT].committed_figure.abs().median(), 1e-9))
        gate("G7 the candidate-set spread is at least as large as the typical committed figure",
             g7, 1.0, g7 >= 1.0)

    # ------------------------------------------------------------------ rule 8 + KEEP paths
    say("")
    say("=" * 110)
    say("ARM 3 — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    say("=" * 110)
    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        ioos = ilim[pan.name]
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[pan.i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2, OOS_Sharpe=sharpe(r[ioos:]),
                                      OOS_CAGR=cagr(r[ioos:]), OOS_MaxDD=mdd(r[ioos:]))
            d = BM[(pan.name, nm)]
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def oos_bm(p, nm, ioos):
        d = BM[(p, nm)]
        r = bench[p]["spy" if nm == "SPY" else "live"][ioos:]
        h1, h2 = halves(r)
        return dict(H1=h1, H2=h2, CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  (3a) BOTH KEEP PATHS ON ALL 66 CANDIDATE ANCHOR BOOKS (rule 4; nothing selected on).")
    brows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for k in BOOKKEY:
            r = booked[pan.name][k]
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows.append(dict(panel=pan.name, anchor=akey(k), ladder=k[0], rung=k[1],
                              is_incumbent=bool(k in ANCH_KEYS), **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say(f"       {len(BK)} candidate books: 4a {int(BK.KEEP_4a.sum())}; "
        f"4b full {int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")

    say("")
    say("  (3b) THE SIGN-MAJORITY POLICY, MADE RULE-8 LEGAL.  At each fold the sign test is run")
    say("       on that fold's IS WINDOW ONLY; the fold year is read once.  Three policies per")
    say("       (panel, ladder, candidate set): S_NONE (tune), S_ALL (anchor), S_SIGN (anchor")
    say("       iff a strict majority of candidates agree the substitution is POSITIVE in IS).")
    prow, stitched = [], []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for lad in LADS:
            for csn in CAND_SETS:
                keys = CAND[csn]
                segs = {p: [] for p in ("S_NONE", "S_ALL", "S_SIGN")}
                nfire = 0
                for (y, lo, hi, o0, o1) in OOS_FOLDS[pan.name]:
                    pick = (lad, argmax_rung(pan.name, lad, lo, hi))
                    s_pick = is_sharpe(pan.name, pick, lo, hi)
                    pos = sum(1 for A in keys
                              if np.isfinite(is_sharpe(pan.name, A, lo, hi))
                              and is_sharpe(pan.name, A, lo, hi) - s_pick > 0)
                    fire = pos * 2 > len(keys)
                    nfire += int(fire)
                    segs["S_NONE"].append(booked[pan.name][pick][o0:o1])
                    segs["S_ALL"].append(booked[pan.name][INC][o0:o1])
                    segs["S_SIGN"].append(booked[pan.name][INC if fire else pick][o0:o1])
                for pname, sg in segs.items():
                    r = np.concatenate(sg)
                    k4a, k4b, m, h1, h2 = keep_paths(r, so, lo_)
                    prow.append(dict(panel=pan.name, ladder=lad, cand_set=csn, policy=pname,
                                     n_folds=len(sg), n_days=len(r), n_fire=nfire,
                                     fire_rate=nfire / max(len(sg), 1), **m, H1=h1, H2=h2,
                                     KEEP_4a_OOS=k4a, KEEP_4b_OOS=k4b))
                    stitched.append(dict(panel=pan.name, ladder=lad, cand_set=csn,
                                         policy=pname, n_days=len(r),
                                         Sharpe=m["Sharpe"], CAGR=m["CAGR"], MaxDD=m["MaxDD"]))
    PL = pd.DataFrame(prow)
    PL.to_csv(f"{OUT}.walkforward.csv", index=False)
    pd.DataFrame(stitched).to_csv(f"{OUT}.stitched.csv", index=False)
    ndays = PL.n_days.unique()
    gate("G8 every stitched policy curve covers the same OOS days", float(len(ndays)), 3.0,
         len(ndays) <= 3)
    say("")
    say("       panel  ladder  cand set   policy   fire   CAGR / Sharpe / MaxDD (OOS stitched)"
        "   halves        4a  4b")
    for _, r in PL.sort_values(["panel", "ladder", "cand_set", "policy"]).iterrows():
        say(f"       {r.panel:6s} {r.ladder:7s} {r.cand_set:9s} {r.policy:8s} "
            f"{r.fire_rate:.2f}  {r.CAGR:7.2%} / {r.Sharpe:7.4f} / {r.MaxDD:8.2%}      "
            f"{r.H1:7.4f}/{r.H2:7.4f}  {int(r.KEEP_4a_OOS)}   {int(r.KEEP_4b_OOS)}")
    say("")
    sm = PL.groupby("policy").Sharpe.mean()
    say("       MEAN STITCHED OOS SHARPE BY POLICY: "
        + "  ".join(f"{k} {v:+.4f}" for k, v in sm.items()))
    say(f"       S_SIGN - S_NONE {sm.get('S_SIGN', np.nan) - sm.get('S_NONE', np.nan):+.4f}; "
        f"S_SIGN - S_ALL {sm.get('S_SIGN', np.nan) - sm.get('S_ALL', np.nan):+.4f}.")
    say(f"       4b OOS PASSES: " + "  ".join(
        f"{p} {int(PL[PL.policy==p].KEEP_4b_OOS.sum())}/{len(PL[PL.policy==p])}"
        for p in ("S_NONE", "S_ALL", "S_SIGN")))

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    for _, r in G.iterrows():
        say(f"  [{'PASS' if r.pass_ else 'FAIL'}] {r.gate}  value {r.value}  target {r.target}")
    say(f"  {int(G.pass_.sum())} of {len(G)} gates pass.")

    say("")
    say("=" * 110)
    say("HEADLINE")
    say("=" * 110)
    hs = CEN[CEN.claim_set == "C_STRICT"].iloc[0]
    g19 = GR[(GR.claim_set == "C_STRICT") & (GR.cand_set == "A19")]
    med_keep = float(g19.median_share_keep.iloc[0]) if len(g19) else np.nan
    all_keep = float(g19.share_all_keep.iloc[0]) if len(g19) else np.nan
    say(f"  ARM 1: of {int(hs.n):,} committed C_STRICT tuning-cost figures, "
        f"{hs.share_FULL:.3f} name their anchor in full (A_FULL), "
        f"{hs.share_PARTIAL:.3f} partially, {hs.share_NONE:.3f} not at all.")
    say(f"  ARM 2: the median checkable C_STRICT claim keeps its committed SIGN at "
        f"{med_keep:.3f} of the record's 19 distinct anchors;")
    say(f"         {all_keep:.3f} of claims keep it at EVERY candidate.")
    if hs.share_NONE > 0.5 and med_keep <= 0.75:
        outcome = "(A) THE ANCHOR MUST BE NAMED"
    elif all_keep >= 0.75:
        outcome = "(B) THE ANCHOR IS INERT"
    else:
        outcome = "(C) NEITHER"
    say(f"  PRE-DECLARED OUTCOME: {outcome}")
    say(f"  TRADABLE ARM: S_SIGN mean stitched OOS Sharpe {sm.get('S_SIGN', np.nan):+.4f} "
        f"against S_NONE {sm.get('S_NONE', np.nan):+.4f} and S_ALL {sm.get('S_ALL', np.nan):+.4f}; "
        f"4b OOS passes "
        f"{int(PL[PL.policy=='S_SIGN'].KEEP_4b_OOS.sum())}/{len(PL[PL.policy=='S_SIGN'])}.")
    say(f"  Runtime {time.time()-t0:.0f}s.")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(CEN=CEN, GR=GR, PL=PL, BK=BK, outcome=outcome, sm=sm)


if __name__ == "__main__":
    main()
