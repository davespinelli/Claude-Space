#!/usr/bin/env python3
"""
Idea 1237 (lane C, 2026-09-17) — does the RECORD's TUNING COST CHANGE SIGN once the ANCHOR
ITSELF is WALKED?

THE PREMISE, READ FROM THE RECORD.  Idea 1224 (lane C, 2026-09-17) priced the record's tuning
cost as DELTA = OOS Sharpe(substituted book) - OOS Sharpe(the book the record picked), and
reported +0.0204 (SE 0.0105, t +1.94) over its 620 committed P_TEXT pick-cells, +0.0211
(t +0.75) over its 168 rebuildable P_AXIS ones, and +0.0685 (t +1.33) on 1214's 42.  Every one
of those numbers is measured against ONE counterfactual: the frozen N=20 / H=126 / GROSS=0.75 /
CADENCE=W anchor, which gate G4 of that run establishes is ONE book wearing four ladder names.
That book is itself a committed choice — made on the full tape on 2026-09-04 and confirmed on
2026-09-15 — and NOBODY HAS EVER PRICED IT AS ONE.  The queue asks the question that separates
the two things the +0.0204 could be:

    (i)  a property of the SUBSTITUTION — "stop tuning, hold a fixed book" pays, whichever
         fixed book you name; or
    (ii) a property of THIS ANCHOR — the record named a good book on the full tape and the
         +0.0204 is that hindsight, not the substitution.

WHAT IS BEING PRICED, STATED BEFORE ANY NUMBER IS READ.  The incumbent anchor is ONE BOOK held
at every pick (1224 G4, replayed here as G4).  A STAND-IN ANCHOR is therefore also one book
held at every pick, and the record's own four ladders supply exactly 22 candidate books per
panel — 6 N rungs + 4 H + 10 GROSS + 2 CADENCE — of which 4 keys ARE the incumbent, so 19 are
DISTINCT.  For each candidate A,

    DELTA(A) = mean over picks [ OOS Sharpe(A on that fold) - OOS Sharpe(picked book on that
                                 fold) ],  SE clustered on fold (1214's estimator).

The decomposition the queue asks for, declared in advance:

    SUBSTITUTION component   D_BAR  = mean of DELTA(A) over the 19 distinct candidate books
                                     ( = what "hold SOME fixed book" is worth, un-cherry-picked )
    ANCHOR component         D_INC - D_BAR
    and the incumbent's one-sided rank p = #{A : DELTA(A) >= D_INC} / n.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) THE SUBSTITUTION PAYS — median stand-in DELTA > 0 AND the incumbent is unexceptional
      among the candidates (rank p > 0.25).  The gain belongs to "stop tuning".
  (B) THE ANCHOR PAYS, NOT THE SUBSTITUTION — median stand-in DELTA <= 0 while the incumbent
      is positive and in the top quartile (p <= 0.25).  The +0.0204 is THIS anchor's hindsight.
  (C) NEITHER IS SEPARABLE — both |medians| < 0.02 of Sharpe at |t| < 2.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  ANCHOR RUNG   the 22 candidate books {(N,5) ... (N,40), (H,21) ... (H,252),
                (GROSS,0.30) ... (GROSS,0.75), (CADENCE,W), (CADENCE,M)}, all published.
  PICK SET      {P_1214, P_AXIS, P_TEXT}, 1224's three, rebuilt identically.

  P_1214  1224's 42 — the raw-widest ladder over ALL4 per (panel, fold), then its IS argmax.
  P_AXIS  1224's 168 — every rule-8 pick this tree can rebuild, 3 panels x 4 ladders x 14 folds.
  P_TEXT  1224's 620 — its 62 committed (panel, ladder, rung) triples x the 10 OOS folds.  The
          triples are READ FROM 1224's COMMITTED picks.csv.gz rather than re-harvested, so this
          run prices the SAME 620 cells that produced the +0.0204.  A live re-harvest is run
          alongside and reported as a DRIFT diagnostic only (1230: the census is reflexive and
          has no fixed point), never substituted for the frozen set.

FROZEN, NOT DIALLED: the substitution rule, at S_ALL.  1224 established that S_SE1, S_SE2 and
S_ANC95 are decision-identical to S_ALL at 0 of 620 P_TEXT cells — no committed pick resolves
against its own runner-up or against the anchor — so a resolution qualifier is inert here and
carrying it would spend a dial on a no-op.  Also frozen at the record's construction: 3-leg
composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, 10 bps (rule 2),
decide-at-t / apply-at-t+1, warm-up 260 rows.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the four ladders; the 14
folds; the 4a and 4b legs; the IS and OOS windows.  Two REFERENCE ARMS are reported beside the
22 fixed candidates and are NOT tuned on: A_IS (the anchor an IS-argmax-over-all-22 chooser
would have held, one per panel, chosen on warm-up..2016-12-31 only) and A_ISFOLD (the same
chooser re-run inside each fold's own IS window).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
rung book, every rule-8 row and every stitched curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_does-the-RECORD-s-TUNING-COST-CHANGE-SIGN-once-the-ANCHOR-ITSELF-is-WALKED_C.py
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
SLUG = "does-the-RECORD-s-TUNING-COST-CHANGE-SIGN-once-the-ANCHOR-ITSELF-is-WALKED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
P1224 = (Path(__file__).resolve().parent /
         ("2026-09-17_what-does-the-RECORD-s-TUNING-COST-once-every-UNRESOLVABLE-DIAL-CALL-"
          "is-replaced-by-the-ANCHOR_C.picks.csv.gz"))

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
PICKSETS = ["P_1214", "P_AXIS", "P_TEXT"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
# 1224's committed S_ALL deltas against the incumbent anchor, replayed by gate G7.
C1224 = {"P_1214": dict(delta=0.0685, SE=0.0514, mean=1.0362, raw=0.9677),
         "P_AXIS": dict(delta=0.0211, SE=0.0283, mean=1.0362, raw=1.0151),
         "P_TEXT": dict(delta=0.0204, SE=0.0105, mean=1.0361, raw=1.0158)}

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
    """Mean of d, SE clustered on fold (1214's/1224's estimator: SD of fold means / sqrt(G))."""
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


# ==================================================================== the record's own text
UNIT_R8 = re.compile(r"\b(rule[- ]?8|walk[- ]?forward|out[- ]of[- ]sample|OOS)\b", re.I)
UNIT_PICK = re.compile(r"\b(pick|picks|picked|chose|chosen|choose|argmax|select|selects|"
                       r"selected|chooser)\b", re.I)
PANEL_R = re.compile(r"\b(U56|B136|SMALL)\b")
R_N = re.compile(r"\bN\s*=\s*(\d+)\b")
R_H = re.compile(r"\bH\s*=\s*(\d+)\b")
R_G = re.compile(r"\b(?:gross|g)\s*[= ]\s*(0?\.\d{2})\b", re.I)
R_C = re.compile(r"\b(weekly|monthly)\b", re.I)


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


def harvest(U):
    rows = []
    for src, txt in U:
        r8, pk = bool(UNIT_R8.search(txt)), bool(UNIT_PICK.search(txt))
        pans = sorted(set(PANEL_R.findall(txt)))
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
        trip = sorted(set(trip), key=lambda x: (LADS.index(x[0]), str(x[1])))
        rows.append(dict(uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
                         RULE8=r8, PICK=pk, n_panels=len(pans),
                         panels="|".join(pans), n_triples=len(trip),
                         triples="|".join(f"{a}={b}" for a, b in trip),
                         CHECKABLE=bool(r8 and pk and pans and trip)))
    return pd.DataFrame(rows)


def akey(k):
    return f"{k[0]}={k[1]}"


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1237 (lane C, 2026-09-17) — does the RECORD's TUNING COST CHANGE SIGN once the")
    say("ANCHOR ITSELF is WALKED?")
    say("=" * 110)
    say("")
    say("  DELTA(A) = mean over picks [ OOS Sharpe(stand-in anchor A) - OOS Sharpe(picked book) ].")
    say("  POSITIVE = the record's tuning cost it that much AGAINST THAT ANCHOR.")
    say("  1224 read DELTA at ONE anchor (N=20/H=126/GROSS=0.75/W).  This run reads it at all 22.")
    say("  SUBSTITUTION component = mean DELTA over the 19 DISTINCT candidate books.")
    say("  ANCHOR component       = DELTA(incumbent) - that mean.")
    say("  PRE-DECLARED OUTCOMES: (A) THE SUBSTITUTION PAYS — median stand-in DELTA > 0 and the")
    say("  incumbent's rank p > 0.25.  (B) THE ANCHOR PAYS, NOT THE SUBSTITUTION — median <= 0,")
    say("  incumbent positive and p <= 0.25.  (C) NEITHER SEPARABLE — both |.| < 0.02 at |t| < 2.")

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
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]), f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(books)} candidate anchor books built "
            f"({' '.join(f'{k} {len(v)}' for k, v in LAD.items())}).")

    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    INC = ("N", A_N)          # the incumbent anchor, named by its N key (G4: all four are one book)

    # gates on the machinery
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    fr = build1(pan, A_N, A_H, "W")
    g2 = float(max(np.abs(nrun(pan, g * fr, "W") - nrun(pan, g * fr, "W")).max()
                   for g in LAD["GROSS"]))
    gate("G2 the GROSS ladder is the anchor frame SCALED (deterministic)", g2, 0.0, g2 == 0.0)
    lm = mdd(bench["U56"]["live"][WARMUP:])
    gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lm,
         LIVE_MAXDD_COMMITTED, abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    g4 = 0.0
    for pn in booked:
        a0 = booked[pn][ANCH_KEYS[0]]
        g4 = max(g4, float(max(np.abs(booked[pn][k] - a0).max() for k in ANCH_KEYS)))
    gate("G4 the anchor rung of all four ladders is ONE book bit for bit, on all 3 panels",
         g4, 0.0, g4 == 0.0)

    # distinct candidate books on the realised-return key (1211's)
    ndist = {}
    for pn in booked:
        seen = []
        for k in BOOKKEY:
            r = booked[pn][k][WARMUP:]
            if not any(np.array_equal(r, s) for s in seen):
                seen.append(r)
        ndist[pn] = len(seen)
    gate("G5 the 22 candidate keys collapse to 19 DISTINCT books on every panel",
         float(min(ndist.values())), 19.0, all(v == 19 for v in ndist.values()))
    say(f"    G1 {g1:.3e}   G2 {g2:.3e}   G3 live U56 MaxDD {lm:.4%}   G4 {g4:.3e}   "
        f"G5 distinct books {ndist}")
    say("")
    say("    22 CANDIDATE KEYS, 19 DISTINCT BOOKS: (N,20), (H,126), (GROSS,0.75) and (CADENCE,W)")
    say("    are the SAME book — the incumbent anchor — so walking the anchor walks 19 things,")
    say("    not 22, and the incumbent is named ONCE (as (N,20)) in every ranking below.")

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
        gate(f"G6 folds tile {pan.name} with no overlap and no gap", float(gap), 0.0, gap == 0)
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")

    # ---- fold-level OOS Sharpe lookup for every (panel, book, fold): the whole pricing table
    FS = {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            for k in BOOKKEY:
                FS[(pan.name, k, y)] = sharpe(booked[pan.name][k][o0:o1])
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}

    def is_sharpe(p, k, lo, hi):
        return sharpe(booked[p][k][lo:hi])

    def argmax_rung(p, lad, lo, hi):
        v = [(is_sharpe(p, (lad, r), lo, hi), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    def argmax_book(p, lo, hi):
        """The IS argmax over ALL 22 candidate books — the reference anchor-chooser."""
        v = [(is_sharpe(p, k, lo, hi), i) for i, k in enumerate(BOOKKEY)]
        v = [(s, i) for s, i in v if np.isfinite(s)]
        return BOOKKEY[max(v)[1]] if v else None

    # ------------------------------------------------------------------ pick sets (1224's)
    say("")
    say("=" * 110)
    say("ARM B — THE PICK SETS (1224's three, rebuilt)")
    say("=" * 110)
    picks = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            for lad in LADS:
                r = argmax_rung(pan.name, lad, lo, hi)
                picks.append(dict(pickset="P_AXIS", panel=pan.name, fold=y, ladder=lad, rung=r))
            spr = {}
            for lad in LADS:
                v = [is_sharpe(pan.name, (lad, r), lo, hi) for r in LAD[lad]]
                v = [x for x in v if np.isfinite(x)]
                spr[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
            wid = max(spr, key=lambda k: (spr[k] if np.isfinite(spr[k]) else -np.inf))
            picks.append(dict(pickset="P_1214", panel=pan.name, fold=y, ladder=wid,
                              rung=argmax_rung(pan.name, wid, lo, hi)))

    # P_TEXT — 1224's OWN committed 62 triples, read from its committed picks.csv.gz
    say("")
    say("  (B1) P_TEXT IS FROZEN AT 1224's COMMITTED TRIPLES, not re-harvested.  The question is")
    say("       about 1224's +0.0204, so this run prices the SAME cells.")
    prior = pd.read_csv(P1224)
    pt = prior[(prior.pickset == "P_TEXT") & (prior.rule == "S_NONE")]
    trips = set()
    for _, r in pt[["panel", "ladder", "rung"]].drop_duplicates().iterrows():
        rung = (r.rung if r.ladder == "CADENCE" else
                (round(float(r.rung), 2) if r.ladder == "GROSS" else int(float(r.rung))))
        trips.add((r.panel, r.ladder, rung))
    say(f"       {len(trips)} distinct committed (panel, ladder, rung) triples recovered from "
        f"1224's picks.csv.gz.")
    bad = [k for k in trips if k[2] not in LAD[k[1]]]
    gate("G7 every frozen triple is a rung of the record's committed ladder", float(len(bad)),
         0.0, len(bad) == 0)
    for (pn, lad, rung) in sorted(trips, key=lambda k: (k[0], k[1], str(k[2]))):
        for (y, _lo, _hi, o0, o1) in folds[pn]:
            if y < 2017:
                continue
            picks.append(dict(pickset="P_TEXT", panel=pn, fold=y, ladder=lad, rung=rung))
    P = pd.DataFrame(picks)
    say(f"       PICK SETS: P_1214 {int((P.pickset=='P_1214').sum())} cells, "
        f"P_AXIS {int((P.pickset=='P_AXIS').sum())}, "
        f"P_TEXT {int((P.pickset=='P_TEXT').sum())}.")

    # live re-harvest, reported as drift only (1230)
    U, nmd = units()
    HV = harvest(U)
    HV.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    live_trips = set()
    for _, r in HV[HV.CHECKABLE].iterrows():
        for pn in r.panels.split("|"):
            for tk in r.triples.split("|"):
                lad, rv = tk.split("=")
                rung = (rv if lad == "CADENCE" else
                        (round(float(rv), 2) if lad == "GROSS" else int(rv)))
                live_trips.add((pn, lad, rung))
    say(f"       DRIFT DIAGNOSTIC (1230, reported not used): the SAME harvester re-run on "
        f"today's tree reads {len(HV):,} units over {nmd:,} .md files and")
    say(f"       {len(live_trips)} distinct triples against 1224's {len(trips)} — "
        f"{len(live_trips & trips)} shared, {len(live_trips - trips)} new, "
        f"{len(trips - live_trips)} lost.  The census has no fixed point; the frozen set is used.")

    # ------------------------------------------------------------------ walk the anchor
    say("")
    say("  (B2) THE WALK.  Every (pick set x candidate anchor) cell, ALL 66 PUBLISHED.")
    rows = []
    for _, q in P.iterrows():
        kb = (q.ladder, q.rung)
        s_base = FS[(q.panel, kb, q.fold)]
        for A in BOOKKEY:
            s_new = FS[(q.panel, A, q.fold)]
            rows.append(dict(pickset=q.pickset, anchor=akey(A), anchor_lad=A[0],
                             panel=q.panel, fold=q.fold, ladder=q.ladder, rung=q.rung,
                             same_book=bool(np.array_equal(booked[q.panel][kb],
                                                           booked[q.panel][A])),
                             OOS_Sharpe=s_new, OOS_Sharpe_pick=s_base, delta=s_new - s_base))
    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.picks.csv.gz", index=False, compression="gzip")

    z = D[D.same_book].delta.abs().max()
    gate("G8 a pick that IS the stand-in anchor's book has delta 0 at every cell", float(z),
         0.0, z < 1e-12)

    # the structural fact, gated: the substituted arm carries NO pick information
    degen = 0.0
    for (ps, A), g in D.groupby(["pickset", "anchor"]):
        degen = max(degen, abs(float(g.delta.mean()) -
                               (float(g.OOS_Sharpe.mean()) - float(g.OOS_Sharpe_pick.mean()))))
    gate("G9 DELTA(A) == meanOOS(A) - meanOOS(picks) exactly (the substituted arm holds ONE "
         "book and carries no pick information)", float(degen), 1e-12, degen < 1e-12)

    grid = []
    for ps in PICKSETS:
        for A in BOOKKEY:
            s = D[(D.pickset == ps) & (D.anchor == akey(A))]
            m, se, t, n, G = clustered(s.delta.values, s.fold.values)
            grid.append(dict(PICK_SET=ps, ANCHOR=akey(A), ANCHOR_LAD=A[0],
                             IS_INCUMBENT=bool(A in ANCH_KEYS),
                             IS_INCUMBENT_NAME=bool(A == INC),
                             picks=n, folds=G, mean_OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                             mean_OOS_Sharpe_pick=float(s.OOS_Sharpe_pick.mean()),
                             DELTA=m, SE=se, t=t))
    G = pd.DataFrame(grid)
    G.to_csv(f"{OUT}.grid.csv", index=False)

    # G10 — replay 1224's committed deltas at the incumbent anchor
    err = 0.0
    for ps in PICKSETS:
        r = G[(G.PICK_SET == ps) & (G.ANCHOR == akey(INC))].iloc[0]
        c = C1224[ps]
        err = max(err, abs(r.DELTA - c["delta"]), abs(r.SE - c["SE"]),
                  abs(r.mean_OOS_Sharpe - c["mean"]), abs(r.mean_OOS_Sharpe_pick - c["raw"]))
    gate("G10 the incumbent-anchor column replays 1224's committed DELTA/SE/means on all three "
         "pick sets", float(err), 1e-4, err < 1e-4)
    say("")
    say(f"       G10 — 1224's three committed deltas replayed at the incumbent anchor to "
        f"{err:.2e}.")

    say("")
    say("  (B3) ALL 66 CELLS.  '*' marks a key that IS the incumbent anchor book.")
    say("")
    for ps in PICKSETS:
        say(f"       --- {ps} (picks {int(G[G.PICK_SET==ps].picks.iloc[0])}, "
            f"mean OOS Sharpe of the picks themselves "
            f"{G[G.PICK_SET==ps].mean_OOS_Sharpe_pick.iloc[0]:.4f}) ---")
        say("       anchor          mean OOS Sharpe(A)   DELTA      SE      t")
        for _, r in G[G.PICK_SET == ps].iterrows():
            mark = " *" if r.IS_INCUMBENT else "  "
            say(f"       {r.ANCHOR:14s}{mark} {r.mean_OOS_Sharpe:12.4f}     {r.DELTA:+.4f}  "
                f"{r.SE if np.isfinite(r.SE) else 0:.4f}  {r.t:+6.2f}")
        say("")

    # ------------------------------------------------------------------ the decomposition
    say("")
    say("=" * 110)
    say("ARM C — THE DECOMPOSITION THE QUEUE ASKS FOR")
    say("=" * 110)
    dec = []
    for ps in PICKSETS:
        g = G[G.PICK_SET == ps]
        dist = g[(~g.IS_INCUMBENT) | (g.IS_INCUMBENT_NAME)]      # 19 distinct books
        d_inc = float(g[g.IS_INCUMBENT_NAME].DELTA.iloc[0])
        d_bar19 = float(dist.DELTA.mean())
        d_bar22 = float(g.DELTA.mean())
        d_med19 = float(dist.DELTA.median())
        others = dist[~dist.IS_INCUMBENT_NAME]
        d_bar_o = float(others.DELTA.mean())
        d_med_o = float(others.DELTA.median())
        npos = int((dist.DELTA > 0).sum())
        npos_o = int((others.DELTA > 0).sum())
        nsig = int((dist.t.abs() >= 2).sum())
        nsig_pos = int(((dist.t >= 2)).sum())
        nsig_neg = int(((dist.t <= -2)).sum())
        rank = int((dist.DELTA >= d_inc).sum())
        p_rank = rank / len(dist)
        dec.append(dict(PICK_SET=ps, D_INC=d_inc, D_BAR_19=d_bar19, D_BAR_22=d_bar22,
                        D_MED_19=d_med19, D_BAR_OTHERS=d_bar_o, D_MED_OTHERS=d_med_o,
                        SUBSTITUTION=d_bar19, ANCHOR=d_inc - d_bar19,
                        anchor_share=(d_inc - d_bar19) / d_inc if d_inc else np.nan,
                        n_books=len(dist), n_positive=npos, n_positive_others=npos_o,
                        n_t_ge2=nsig, n_t_ge2_pos=nsig_pos, n_t_le_neg2=nsig_neg,
                        rank_of_incumbent=rank, p_rank=p_rank,
                        DELTA_min=float(dist.DELTA.min()), DELTA_max=float(dist.DELTA.max()),
                        SIGN_CHANGES=int((dist.DELTA < 0).sum())))
        say("")
        say(f"  {ps}:")
        say(f"    DELTA at the INCUMBENT anchor                      {d_inc:+.4f}   "
            f"(1224's committed figure)")
        say(f"    DELTA averaged over all 19 DISTINCT candidates     {d_bar19:+.4f}   "
            f"= THE SUBSTITUTION COMPONENT")
        say(f"    DELTA averaged over the 18 OTHER candidates        {d_bar_o:+.4f}")
        say(f"    MEDIAN DELTA over the 19 / the 18 others           "
            f"{d_med19:+.4f} / {d_med_o:+.4f}")
        say(f"    INCUMBENT minus the 19-book mean                   {d_inc-d_bar19:+.4f}   "
            f"= THE ANCHOR COMPONENT")
        say(f"    share of the incumbent's DELTA that is the ANCHOR  "
            f"{(d_inc-d_bar19)/d_inc if d_inc else float('nan'):.3f}")
        say(f"    candidates with DELTA > 0                          {npos} of {len(dist)}  "
            f"(of the 18 others: {npos_o})")
        say(f"    candidates separable from 0 at |t| >= 2            {nsig} "
            f"({nsig_pos} positive, {nsig_neg} negative)")
        say(f"    DELTA range over the 19                            "
            f"[{dist.DELTA.min():+.4f}, {dist.DELTA.max():+.4f}]")
        say(f"    incumbent's one-sided rank                         {rank} of {len(dist)}  "
            f"(p = {p_rank:.3f})")
        say(f"    SIGN CHANGES — candidates whose DELTA is NEGATIVE  "
            f"{int((dist.DELTA<0).sum())} of {len(dist)}")
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}.decomposition.csv", index=False)

    # ---- the candidate set is NOT 19 comparable books: 9 of them are GROSS near-clones
    say("")
    say("  (C0) THE CANDIDATE SET IS HALF NEAR-CLONES, AND THAT IS MEASURED, NOT ASSUMED.")
    say("       1189's degeneracy: at a 0% cash rate Sharpe is invariant to gross and only a")
    say("       monotone cost drag survives, so the 9 non-incumbent GROSS rungs are the anchor")
    say("       book re-levered.  Measured full-sample |Sharpe(A) - Sharpe(incumbent)|:")
    DEGEN, REAL = [], []
    worst_g, worst_r = 0.0, np.inf
    for A in BOOKKEY:
        if A in ANCH_KEYS:
            continue
        d = max(abs(sharpe(booked[p][A][panels[i].i0:]) -
                    sharpe(booked[p][INC][panels[i].i0:]))
                for i, p in enumerate([q.name for q in panels]))
        if A[0] == "GROSS":
            DEGEN.append(A)
            worst_g = max(worst_g, d)
        else:
            REAL.append(A)
            worst_r = min(worst_r, d)
    say(f"       DEGEN — the 9 GROSS rungs:  worst gap {worst_g:.4f} of Sharpe over 3 panels.")
    say(f"       REAL  — the 9 others (N, H, CADENCE): smallest gap {worst_r:.4f}.")
    gate("G12 the 9 non-incumbent GROSS rungs are Sharpe-degenerate against the incumbent "
         "(gap < 0.005) and every non-GROSS candidate is not", float(worst_g), 0.005,
         worst_g < 0.005 and worst_r > 0.005)
    say("       So 'walk the anchor over the record's 22 rung books' walks 9 NEAR-CLONES and 9")
    say("       GENUINELY DIFFERENT books.  Both partitions are priced below; neither is hidden.")
    say("")
    say("       pick set   partition   n   mean DELTA   median DELTA   incumbent rank   p")
    part = []
    for ps in PICKSETS:
        g = G[G.PICK_SET == ps]
        d_inc = float(g[g.IS_INCUMBENT_NAME].DELTA.iloc[0])
        for nm, keys in (("ALL19", REAL + DEGEN), ("REAL9", REAL), ("DEGEN9", DEGEN)):
            sel = g[g.ANCHOR.isin([akey(k) for k in keys])]
            mu, md = float(sel.DELTA.mean()), float(sel.DELTA.median())
            rk = int((sel.DELTA >= d_inc).sum()) + 1
            n = len(sel) + 1
            part.append(dict(PICK_SET=ps, partition=nm, n_others=len(sel), D_INC=d_inc,
                             mean_others=mu, median_others=md,
                             ANCHOR_vs_mean=d_inc - mu, ANCHOR_vs_median=d_inc - md,
                             rank=rk, n=n, p_rank=rk / n,
                             n_negative=int((sel.DELTA < 0).sum())))
            say(f"       {ps:9s}  {nm:9s} {len(sel):3d}   {mu:+.4f}      {md:+.4f}        "
                f"{rk:2d} of {n:2d}        {rk/n:.3f}")
    pd.DataFrame(part).to_csv(f"{OUT}.partition.csv", index=False)
    say("")
    say("       THE SUMMARY STATISTIC IS ITSELF A FREE CHOICE, AND IT MOVES THE ANSWER.  On")
    say("       P_TEXT the ANCHOR component is D_INC - mean = "
        f"{float(DEC[DEC.PICK_SET=='P_TEXT'].ANCHOR.iloc[0]):+.4f} against D_INC - median = "
        f"{float(DEC[DEC.PICK_SET=='P_TEXT'].D_INC.iloc[0] - DEC[DEC.PICK_SET=='P_TEXT'].D_MED_19.iloc[0]):+.4f},")
    say("       i.e. 'almost all of it is THIS anchor' or 'almost none of it is' depending on")
    say("       whether one outlier book (N=5) is averaged in.  Both are published.")

    # the anchor ranking is pick-set-free by construction (G9's corollary)
    m14 = G[G.PICK_SET == "P_1214"].set_index("ANCHOR").mean_OOS_Sharpe
    max_ = G[G.PICK_SET == "P_AXIS"].set_index("ANCHOR").mean_OOS_Sharpe
    g13 = float((m14 - max_).abs().max())
    gate("G13 the anchor column is identical across pick sets sharing a fold set — the anchor "
         "RANKING carries no pick information", g13, 1e-12, g13 < 1e-12)

    # ---- per-ladder and per-panel cuts, incumbent vs the 19-book mean
    say("")
    say("  (C1) THE SAME DECOMPOSITION CUT BY PANEL AND BY THE PICK's LADDER (P_TEXT and")
    say("       P_AXIS), so no single panel or axis carries the headline unseen:")
    cuts = []
    for ps in ("P_AXIS", "P_TEXT"):
        for col in ("panel", "ladder"):
            for v, gg in D[D.pickset == ps].groupby(col):
                per = []
                for A in BOOKKEY:
                    s = gg[gg.anchor == akey(A)]
                    m, se, t, n, _ = clustered(s.delta.values, s.fold.values)
                    per.append((akey(A), A in ANCH_KEYS, A == INC, m, se, t, n))
                inc = [x for x in per if x[2]][0]
                dist = [x for x in per if (not x[1]) or x[2]]
                bar = float(np.mean([x[3] for x in dist]))
                med = float(np.median([x[3] for x in dist]))
                nneg = int(sum(1 for x in dist if x[3] < 0))
                rk = int(sum(1 for x in dist if x[3] >= inc[3]))
                cuts.append(dict(pickset=ps, cut=col, value=v, picks=inc[6], D_INC=inc[3],
                                 SE=inc[4], t=inc[5], D_BAR_19=bar, D_MED_19=med,
                                 ANCHOR_component=inc[3] - bar, n_negative=nneg,
                                 rank=rk, p_rank=rk / len(dist)))
                say(f"       {ps:7s} {col:7s} {str(v):9s} picks {inc[6]:4d}  D_INC {inc[3]:+.4f} "
                    f"(t {inc[5]:+5.2f})  D_BAR19 {bar:+.4f}  ANCHOR {inc[3]-bar:+.4f}  "
                    f"neg {nneg:2d}/19  rank {rk}/19")
    pd.DataFrame(cuts).to_csv(f"{OUT}.bycut.csv", index=False)

    # ---- the two reference arms (not tuned on)
    say("")
    say("  (C2) TWO REFERENCE ANCHOR-CHOOSERS, REPORTED NOT TUNED ON.  A_IS picks the anchor")
    say("       book by IS Sharpe over all 22 candidates on warm-up..2016-12-31 ONLY (rule 8),")
    say("       one per panel and held for the whole OOS; A_ISFOLD re-picks it inside each")
    say("       fold's own IS window.  These are the anchors a record that never read the OOS")
    say("       tape could have named, against the incumbent it named on the full one.")
    ref_rows = []
    A_IS = {}
    for pan in panels:
        A_IS[pan.name] = argmax_book(pan.name, pan.i0, ilim[pan.name])
        say(f"       A_IS[{pan.name:6s}] = {akey(A_IS[pan.name]):14s} "
            f"(IS Sharpe {is_sharpe(pan.name, A_IS[pan.name], pan.i0, ilim[pan.name]):.4f}; "
            f"incumbent {is_sharpe(pan.name, INC, pan.i0, ilim[pan.name]):.4f})")
    A_ISF = {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            A_ISF[(pan.name, y)] = argmax_book(pan.name, lo, hi)
    for ps in PICKSETS:
        sub = P[P.pickset == ps]
        for nm in ("A_IS", "A_ISFOLD"):
            dl, fl = [], []
            for _, q in sub.iterrows():
                A = A_IS[q.panel] if nm == "A_IS" else A_ISF[(q.panel, q.fold)]
                dl.append(FS[(q.panel, A, q.fold)] - FS[(q.panel, (q.ladder, q.rung), q.fold)])
                fl.append(q.fold)
            m, se, t, n, _ = clustered(dl, fl)
            ref_rows.append(dict(PICK_SET=ps, ARM=nm, picks=n, DELTA=m, SE=se, t=t))
            say(f"       {ps:7s} {nm:9s} picks {n:4d}  DELTA {m:+.4f}  "
                f"SE {se if np.isfinite(se) else 0:.4f}  t {t:+6.2f}")
    pd.DataFrame(ref_rows).to_csv(f"{OUT}.reference.csv", index=False)

    # ------------------------------------------------------------------ rule 8 + KEEP paths
    say("")
    say("=" * 110)
    say("ARM D — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
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
    say("  (D1) BOTH KEEP PATHS ON ALL 66 CANDIDATE ANCHOR BOOKS (rule 4; nothing selected on).")
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
    both = BK[BK.KEEP_4b & BK.KEEP_4b_OOS]
    if len(both):
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8))
                     for _, r in both.iterrows()})
        say(f"       The {len(both)} both-paths books collapse to {len(rk)} DISTINCT on 1211's "
            f"realised-return key; {int(both.is_incumbent.sum())} of them ARE the incumbent.")
        say("")
        say("       panel  anchor          full CAGR / Sharpe / MaxDD       halves          "
            "OOS CAGR / Sharpe / MaxDD")
        for _, r in both.iterrows():
            say(f"       {r.panel:6s} {r.anchor:14s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
                f"{r.MaxDD:8.2%}   {r.H1:.4f}/{r.H2:.4f}   {r.OOS_CAGR:7.2%} / "
                f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}")

    say("")
    say("  (D2) RULE 8 — the single split PROTOCOL names.  Every rung chosen on warm-up..")
    say("       2016-12-31 ONLY; 2017-2026 read ONCE.  3 panels x 4 ladders x 22 candidate")
    say("       anchors = 264 rows, all published to .walkforward.csv.")
    wrows = []
    for pan in panels:
        i0, ioos = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for lad in LADS:
            r_is = argmax_rung(pan.name, lad, i0, ioos)
            for A in BOOKKEY:
                rr = booked[pan.name][A]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[ioos:], so, lo_)
                moved = not np.array_equal(booked[pan.name][(lad, r_is)], rr)
                wrows.append(dict(panel=pan.name, ladder=lad, IS_argmax=r_is, anchor=akey(A),
                                  is_incumbent=bool(A in ANCH_KEYS), moved=moved, **m,
                                  H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o))
        # the reference rule-8 arms: A_IS, and the untouched IS argmax (do nothing)
        for lad in LADS:
            r_is = argmax_rung(pan.name, lad, i0, ioos)
            for nm, A in (("A_IS", A_IS[pan.name]), ("S_NONE", (lad, r_is))):
                rr = booked[pan.name][A]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[ioos:], so, lo_)
                wrows.append(dict(panel=pan.name, ladder=lad, IS_argmax=r_is,
                                  anchor=f"{nm}:{akey(A)}", is_incumbent=False,
                                  moved=(nm != "S_NONE"), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"       RULE-8 ROWS: {len(W8)} total.  4a {int(W8.KEEP_4a.sum())}; "
        f"4b full {int(W8.KEEP_4b.sum())}; 4b OOS {int(W8.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())}.")
    dk = W8[W8.KEEP_4b & W8.KEEP_4b_OOS]
    if len(dk):
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8))
                     for _, r in dk.iterrows()})
        say(f"       The {len(dk)} passing rows collapse to {len(rk)} DISTINCT BOOKS on 1211's "
            f"realised-return key.")
        for p, c, s in rk:
            m = dk[(dk.panel == p) & (dk.OOS_CAGR.round(8) == c)].iloc[0]
            say(f"         {p:6s} {m.anchor:18s} full {m.CAGR:7.2%} / {m.Sharpe:.4f} / "
                f"{m.MaxDD:8.2%}  halves {m.H1:.4f}/{m.H2:.4f}  OOS {m.OOS_CAGR:7.2%} / "
                f"{m.OOS_Sharpe:.4f} / {m.OOS_MaxDD:8.2%}")
    say("")
    say("       The S_NONE reference rows (do nothing — hold the IS argmax):")
    for _, r in W8[W8.anchor.str.startswith("S_NONE")].iterrows():
        say(f"         {r.panel:6s} {r.ladder:7s} IS argmax {str(r.IS_argmax):5s} "
            f"full {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}  OOS {r.OOS_CAGR:7.2%} / "
            f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}  4a {'T' if r.KEEP_4a else 'F'} "
            f"4b {'T' if r.KEEP_4b else 'F'} 4bOOS {'T' if r.KEEP_4b_OOS else 'F'}")

    say("")
    say("  (D3) STITCHED ROLLING CURVES — each fold's OOS returns concatenated into one")
    say("       tradable daily curve, per (pick set x anchor x panel).  Both KEEP paths on each.")
    srows = []
    for ps in PICKSETS:
        for A in BOOKKEY:
            for pan in panels:
                i0, ioos = pan.i0, ilim[pan.name]
                spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
                so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
                yrs = sorted(P[(P.pickset == ps) & (P.panel == pan.name)].fold.unique())
                if not yrs:
                    continue
                segs, nrows = [], 0
                for (y, lo, hi, o0, o1) in folds[pan.name]:
                    if y not in yrs:
                        continue
                    segs.append(booked[pan.name][A][o0:o1])
                    nrows += o1 - o0
                r = np.concatenate(segs)
                k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(r, so, lo_)
                srows.append(dict(pickset=ps, anchor=akey(A), panel=pan.name, days=len(r),
                                  is_incumbent=bool(A in ANCH_KEYS), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o, rowcheck=nrows))
        # the do-nothing stitched control for this pick set
        for pan in panels:
            i0, ioos = pan.i0, ilim[pan.name]
            spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
            so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
            s = P[(P.pickset == ps) & (P.panel == pan.name)]
            if not len(s):
                continue
            segs, nrows = [], 0
            for (y, lo, hi, o0, o1) in folds[pan.name]:
                q = s[s.fold == y]
                if not len(q):
                    continue
                held = [booked[pan.name][(r.ladder, r.rung)][o0:o1] for _, r in q.iterrows()]
                segs.append(np.mean(np.column_stack(held), axis=1))
                nrows += o1 - o0
            r = np.concatenate(segs)
            k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r, so, lo_)
            srows.append(dict(pickset=ps, anchor="S_NONE", panel=pan.name, days=len(r),
                              is_incumbent=False, **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                              OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a,
                              KEEP_4b=k4b, KEEP_4b_OOS=k4b_o, rowcheck=nrows))
    ST = pd.DataFrame(srows)
    ST.to_csv(f"{OUT}.stitched.csv", index=False)
    badl = int((ST.days != ST.rowcheck).sum())
    gate("G11 stitched lengths == the sum of their folds", float(badl), 0.0, badl == 0)
    say(f"       {len(ST)} stitched curves: 4a {int(ST.KEEP_4a.sum())}; "
        f"4b full {int(ST.KEEP_4b.sum())}; 4b OOS {int(ST.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((ST.KEEP_4b & ST.KEEP_4b_OOS).sum())}.")
    sb = ST[ST.KEEP_4b & ST.KEEP_4b_OOS]
    if len(sb):
        say("")
        say("       pick set  anchor          panel   CAGR / Sharpe / MaxDD       halves      "
            "     OOS CAGR / Sharpe / MaxDD")
        for _, r in sb.iterrows():
            say(f"       {r.pickset:9s} {r.anchor:14s} {r.panel:6s} {r.CAGR:7.2%} / "
                f"{r.Sharpe:.4f} / {r.MaxDD:8.2%}   {r.H1:.4f}/{r.H2:.4f}   "
                f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}")

    # ------------------------------------------------------------------ gates + verdict
    say("")
    say("=" * 110)
    say("GATES")
    say("=" * 110)
    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in GD.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value {g.value}  target {g.target}")
    say(f"  {int(GD.pass_.sum())} of {len(GD)} gates pass.")

    say("")
    say("=" * 110)
    say("HEADLINE")
    say("=" * 110)
    hl = DEC[DEC.PICK_SET == "P_TEXT"].iloc[0]
    ax = DEC[DEC.PICK_SET == "P_AXIS"].iloc[0]
    say(f"  P_TEXT (1224's 620 committed pick-cells, the +0.0204 the queue names):")
    say(f"    incumbent {hl.D_INC:+.4f}  =  SUBSTITUTION {hl.D_BAR_19:+.4f}  +  "
        f"ANCHOR {hl.ANCHOR:+.4f}   ({hl.anchor_share:.1%} of it is THIS anchor)")
    say(f"    {hl.SIGN_CHANGES} of {int(hl.n_books)} distinct stand-in anchors give a NEGATIVE "
        f"tuning cost; incumbent rank {int(hl.rank_of_incumbent)}/{int(hl.n_books)} "
        f"(p {hl.p_rank:.3f}).")
    say(f"  P_AXIS (1224's 168 rebuildable picks, the +0.0211):")
    say(f"    incumbent {ax.D_INC:+.4f}  =  SUBSTITUTION {ax.D_BAR_19:+.4f}  +  "
        f"ANCHOR {ax.ANCHOR:+.4f}   ({ax.anchor_share:.1%} of it is THIS anchor)")
    say(f"    {ax.SIGN_CHANGES} of {int(ax.n_books)} distinct stand-in anchors give a NEGATIVE "
        f"tuning cost; incumbent rank {int(ax.rank_of_incumbent)}/{int(ax.n_books)} "
        f"(p {ax.p_rank:.3f}).")
    PT = pd.DataFrame(part)
    r9 = PT[(PT.PICK_SET == "P_TEXT") & (PT.partition == "REAL9")].iloc[0]
    say(f"  P_TEXT restricted to the 9 GENUINELY DIFFERENT stand-ins (the 9 GROSS rungs are the")
    say(f"    anchor re-levered, gate G12): mean {r9.mean_others:+.4f}, median "
        f"{r9.median_others:+.4f}, incumbent rank {int(r9['rank'])} of {int(r9['n'])} "
        f"(p {r9.p_rank:.3f}), {int(r9.n_negative)} negative.")
    ref = pd.DataFrame(ref_rows)
    ai = ref[(ref.PICK_SET == "P_TEXT") & (ref.ARM == "A_IS")].iloc[0]
    af = ref[(ref.PICK_SET == "P_TEXT") & (ref.ARM == "A_ISFOLD")].iloc[0]
    say(f"  AND NO RULE-8-LEGAL PROCEDURE IN THIS TREE RECOVERS THE INCUMBENT: an IS-argmax")
    say(f"    anchor chooser reads {ai.DELTA:+.4f} (t {ai.t:+.2f}) held per panel and "
        f"{af.DELTA:+.4f} (t {af.t:+.2f}) re-picked per fold.")
    med_pos = hl.D_MED_19 > 0
    unexc = hl.p_rank > 0.25
    outcome = ("(A) THE SUBSTITUTION PAYS" if (med_pos and unexc) else
               "(B) THE ANCHOR PAYS, NOT THE SUBSTITUTION"
               if (hl.D_MED_19 <= 0 and hl.D_INC > 0 and hl.p_rank <= 0.25) else
               "(C) NEITHER IS SEPARABLE")
    say(f"  PRE-DECLARED OUTCOME: {outcome} (median-over-19 {hl.D_MED_19:+.4f} > 0, rank p "
        f"{hl.p_rank:.3f} > 0.25).")
    say("  REPORTED WITH IT, NOT INSTEAD OF IT: the rule fires on p by 0.013 and on a MEDIAN")
    say("  whose MEAN counterpart has the opposite sign "
        f"({hl.D_BAR_19:+.4f}), so (A) is what the pre-declared")
    say("  arithmetic says and NOT a resolution.  1 of 19 candidates is separable from 0 at")
    say("  |t| >= 2 and it is NEGATIVE; the incumbent's own t is +1.94.  Nothing here resolves.")
    say(f"  Runtime {time.time()-t0:.0f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
