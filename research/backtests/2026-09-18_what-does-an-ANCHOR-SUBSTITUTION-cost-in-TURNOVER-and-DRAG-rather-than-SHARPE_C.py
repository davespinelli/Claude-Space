#!/usr/bin/env python3
"""
Idea 1236 (lane C, 2026-09-18) — what does an ANCHOR SUBSTITUTION cost in TURNOVER and DRAG
rather than SHARPE?

THE PREMISE, READ FROM THE RECORD.  Idea 1224 (lane C, 2026-09-17) priced the record's
anchor substitution at +0.0204 of OOS Sharpe (SE 0.0105, t +1.94) over 620 committed
pick-cells and +0.0211 (SE 0.0283, t +0.75) over the 168 rebuildable P_AXIS picks.  It
priced it ONLY in Sharpe, at ONE cost rung (10 bps).  Idea 931 established that a
W->M cadence improvement is a TURNOVER REBATE every book collects, with the null's own
median gain running +0.0466 / +0.3334 / +0.7624 / +1.4501 of Sharpe at 0 / 10 / 25 / 50 bps.
The anchor rung (N=20 / H=126 / GROSS=0.75 / CADENCE=W) is a SLOW book; an IS argmax is free
to land on N=5 or H=21 or CADENCE=M, which are FAST books.  So part of 1224's +0.0211 may be
nothing but the anchor paying less cost, and a further part may be a re-booking cost the
sliced-fold accounting never charged the moving pick at all.  This run separates the three.

WHAT IS BEING MEASURED, STATED BEFORE ANY NUMBER IS READ.

  DELTA(c) = mean over picks of [ OOS Sharpe(anchor book at cost c)
                                - OOS Sharpe(the book the record picked, at cost c) ]

  the same object 1224 published, now as a function of the cost rung c.  Decompose it:

  GROSS PART = DELTA(0)             the part that survives with costs switched off
  REBATE(c)  = DELTA(c) - DELTA(0)  the part that is only differential cost drag
  SHARE(c)   = REBATE(c) / DELTA(c) the fraction of the published gain that is the rebate

  PRE-DECLARED ANSWER TO THE QUEUE'S QUESTION ("report the rung at which the Sharpe gain is
  entirely the rebate"): the gain is ENTIRELY THE REBATE at rung c iff SHARE(c) >= 1.0,
  which happens iff DELTA(0) <= 0 < DELTA(c).  If DELTA(0) > 0 then NO finite rung makes the
  gain entirely the rebate and the honest report is SHARE(c) at each rung plus the statement
  that a positive cost-free part exists.  Both outcomes are reported; neither is selected on.

  PRE-DECLARED OUTCOMES.  (A) ENTIRELY REBATE — DELTA(0) <= 0 and DELTA(10) > 0.
  (B) MOSTLY REBATE — DELTA(0) > 0 and SHARE(10) >= 0.50.  (C) MOSTLY GROSS — DELTA(0) > 0
  and SHARE(10) < 0.50.  (D) NO GAIN AT ANY RUNG — DELTA(c) <= 0 at all four rungs.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  COST RUNG   {0, 10, 25, 50} bps       (931's ladder, the queue's ladder)
  PICK SET    {P_1214, P_AXIS, P_TEXT}  (1224's three, so the headline is re-priced, not a
                                         new object)

  12 cells, every one published in `.grid.csv`.  The SUBSTITUTION RULE is FROZEN at S_ALL —
  1224 proved S_ALL, S_SE1, S_SE2 and S_ANC95 are decision-identical on the record's own
  committed picks (0 of 620 differing cells), so it is not a live dial and spending one of
  the two on it would buy nothing.  THE PICKS THEMSELVES ARE FROZEN AT THE RECORD'S OWN 10
  bps RUNG, because the queue says "re-price the SAME 168 picks"; an arm in which the chooser
  ALSO sees cost c is reported separately as a robustness reading, not as a third dial.

THE THREE THINGS BEING SEPARATED, all published:
  (1) TURNOVER.  Annualised one-way turnover of the anchor book and of the picked book over
      each fold's OOS window.  A pure mechanical fact, independent of c.
  (2) DRAG.  CAGR(0 bps) - CAGR(c bps) for each book, in pp/yr.  Turnover x c, realised.
  (3) THE RE-BOOKING COST the sliced accounting omits.  1224 read each fold's OOS Sharpe off
      a book run continuously over the whole tape, so a pick that CHANGES between folds was
      never charged for the switch.  ARM D builds the REALISED STITCHED book — hold fold f's
      pick during fold f, pay the true turnover on the switch day — and prices it against the
      anchor, which by construction never switches.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the record's four
ladders N/H/GROSS/CADENCE; the 14 folds; the 4a and 4b legs; the IS and OOS windows.

Frozen at the record's construction: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 / CADENCE=W, decide-at-t /
apply-at-t+1 (rule 2), warm-up 260 rows.  PROTOCOL rule 2's 10 bps is the REFERENCE rung and
is one of the four; the other three are the sensitivity the queue asks for and no verdict is
taken at a rung other than 10 bps.

PROTOCOL: rule 2 execution; rule 8 walk-forward with every rung chosen on
warm-up..2016-12-31 ONLY and 2017-2026 read once, re-run at each cost rung; BOTH KEEP paths
(4a vs live RULES v2, 4b vs SPY) on every rule-8 row and every stitched curve; rule 9
survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT
modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-18_what-does-an-ANCHOR-SUBSTITUTION-cost-in-TURNOVER-and-DRAG-rather-than-SHARPE_C.py
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

DATE = "2026-09-18"
SLUG = "what-does-an-ANCHOR-SUBSTITUTION-cost-in-TURNOVER-and-DRAG-rather-than-SHARPE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

WARMUP, MAXVOL = 260, 0.60
REF_COST = 10.0                      # PROTOCOL rule 2's rung; the only rung a verdict is read at
COSTS = [0.0, 10.0, 25.0, 50.0]      # DIAL 1
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
PICKSETS = ["P_1214", "P_AXIS", "P_TEXT"]                       # DIAL 2
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
# 1224's committed price legs at 10 bps, replayed by gates G11/G12.
C1224_AXIS = dict(mean_OOS=1.0151, anc_OOS=1.0362, delta=0.0211, SE=0.0283)
C1224_1214 = dict(mean_OOS=0.9677, anc_OOS=1.0362, delta=0.0685, SE=0.0514)
REPLAY_END = "2026-09-16"          # the last day of the tape idea 1224 read

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


def nrun(pan, Wt, reb):
    """1224's fast runner, generalised: `reb` is an arbitrary sorted array of application-time
    rebalance rows.  Returns (GROSS daily returns, one-way turnover at each row).  Costs are
    applied afterwards as r(c) = gross - turn * c / 1e4, which is exactly what 1224's nrun did
    at its single hard-wired rung (gate G1)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    reb = np.asarray(reb, dtype=np.int64)
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
    return (held * rets).sum(axis=1), turn


def at_cost(gr, tu, c):
    return gr - tu * c / 1e4


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


def annturn(tu, lo, hi):
    n = hi - lo
    return float(np.sum(tu[lo:hi]) * 252.0 / n) if n > 0 else np.nan


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def bmpack(r):
    h1, h2 = halves(r)
    m = triple(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2)


def clustered(d, fold):
    """Mean of d, SE clustered on fold (1214/1224's estimator: SD of the fold means / sqrt(G))."""
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


# ==================================================================== world construction
def make_panels(end=None):
    """The record's three panels.  `end` truncates every panel to that date, which is the only
    way to replay a committed number after data/prices.csv has been rewritten by a later
    nightly close."""
    pxU = load_universe()
    pxB = load_universe(broad=True)
    pxS = load_universe(small=True)
    if end is not None:
        e = pd.Timestamp(end)
        pxU, pxB, pxS = pxU.loc[:e], pxB.loc[:e], pxS.loc[:e]
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels = [Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]),
              Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]),
              Panel("SMALL", pxS, inv)]
    return panels, inv, pxU, pxB, pxS


def build_books(pan):
    """Every rung book of every ladder as (gross returns, turnover), plus the frames and the
    (freq, frame key, gross) recipe each rung was built from."""
    frames = {}
    for N in LAD["N"]:
        frames[(N, A_H, "W")] = None
    for H in LAD["H"]:
        frames[(A_N, H, "W")] = None
    frames[(A_N, A_H, "M")] = None
    for key in list(frames):
        frames[key] = build1(pan, key[0], key[1], key[2])
    af = frames[(A_N, A_H, "W")]
    gb, tb, rb = {}, {}, {}
    for N in LAD["N"]:
        gb[("N", N)], tb[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], pan.seg["W"])
        rb[("N", N)] = ("W", (N, A_H, "W"), A_G)
    for H in LAD["H"]:
        gb[("H", H)], tb[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], pan.seg["W"])
        rb[("H", H)] = ("W", (A_N, H, "W"), A_G)
    for f in LAD["CADENCE"]:
        fr = af if f == "W" else frames[(A_N, A_H, "M")]
        gb[("CADENCE", f)], tb[("CADENCE", f)] = nrun(pan, A_G * fr, pan.seg[f])
        rb[("CADENCE", f)] = (f, (A_N, A_H, f), A_G)
    for g in LAD["GROSS"]:
        gb[("GROSS", g)], tb[("GROSS", g)] = nrun(pan, g * af, pan.seg["W"])
        rb[("GROSS", g)] = ("W", (A_N, A_H, "W"), g)
    return frames, gb, tb, rb


def make_folds(pan):
    yrs = pan.idx.year.values
    out = []
    for y in FOLD_YEARS:
        oo = np.flatnonzero(yrs == y)
        oo = oo[oo >= pan.i0]
        if len(oo) < 60:
            continue
        lo, hi = pan.i0, int(oo[0])
        if hi - lo < 252:
            continue
        out.append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
    return out


def replay_levels(end):
    """Rebuild 1224's P_AXIS and P_1214 legs at 10 bps on a tape truncated to `end`.  Used only
    by the replay gate; nothing downstream reads it."""
    panels, _inv, _a, _b, _c = make_panels(end)
    bk, tn = {}, {}
    for pan in panels:
        _fr, gb, tb, _rb = build_books(pan)
        bk[pan.name], tn[pan.name] = gb, tb

    def iss(p, lad, r, lo, hi):
        return sharpe(at_cost(bk[p][(lad, r)], tn[p][(lad, r)], REF_COST)[lo:hi])

    def amax(p, lad, lo, hi):
        v = [(iss(p, lad, r, lo, hi), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    rows = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in make_folds(pan):
            def px_(lad, r):
                return sharpe(at_cost(bk[pan.name][(lad, r)],
                                      tn[pan.name][(lad, r)], REF_COST)[o0:o1])
            for lad in LADS:
                r = amax(pan.name, lad, lo, hi)
                rows.append(dict(ps="P_AXIS", fold=y, pick=px_(lad, r),
                                 anc=px_(lad, ANCHOR_RUNG[lad])))
            spr = {}
            for lad in LADS:
                v = [iss(pan.name, lad, r, lo, hi) for r in LAD[lad]]
                v = [x for x in v if np.isfinite(x)]
                spr[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
            wid = max(spr, key=lambda k: (spr[k] if np.isfinite(spr[k]) else -np.inf))
            r = amax(pan.name, wid, lo, hi)
            rows.append(dict(ps="P_1214", fold=y, pick=px_(wid, r),
                             anc=px_(wid, ANCHOR_RUNG[wid])))
    R = pd.DataFrame(rows)
    out = {}
    for ps in ("P_AXIS", "P_1214"):
        s = R[R.ps == ps]
        m, se, t, n, _ = clustered((s.anc - s.pick).values, s.fold.values)
        out[ps] = dict(mean_OOS=float(s.pick.mean()), anc_OOS=float(s.anc.mean()),
                       delta=m, SE=se, t=t, n=n)
    return out


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1236 (lane C, 2026-09-18) — what does an ANCHOR SUBSTITUTION cost in TURNOVER")
    say("and DRAG rather than SHARPE?")
    say("=" * 108)
    say("")
    say("  DELTA(c) = OOS Sharpe(anchor book @ c) - OOS Sharpe(the book the record picked @ c).")
    say("  GROSS PART = DELTA(0); REBATE(c) = DELTA(c) - DELTA(0); SHARE(c) = REBATE/DELTA.")
    say("  ENTIRELY THE REBATE at rung c  <=>  SHARE(c) >= 1.0  <=>  DELTA(0) <= 0 < DELTA(c).")
    say("  OUTCOMES: (A) ENTIRELY REBATE  (B) MOSTLY REBATE, SHARE(10) >= 0.50")
    say("            (C) MOSTLY GROSS, SHARE(10) < 0.50  (D) NO GAIN AT ANY RUNG.")

    # ------------------------------------------------------------------ panels and rung books
    say("")
    say("=" * 108)
    say("ARM A — PANELS, RUNG BOOKS, TURNOVER")
    say("=" * 108)
    panels, inv, pxU, pxB, pxS = make_panels()
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")
    say(f"  TAPE: U56 ends {pxU.index[-1].date()}, B136 {pxB.index[-1].date()}, "
        f"SMALL {pxS.index[-1].date()}.")

    booked, turned, rebs, bench, frames_all = {}, {}, {}, {}, {}
    for pan in panels:
        frames, gb, tb, rb = build_books(pan)
        frames_all[pan.name] = frames
        booked[pan.name], turned[pan.name], rebs[pan.name] = gb, tb, rb
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=REF_COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name:6s} {len(gb)} rung books built "
            f"({' '.join(f'{k} {len(v)}' for k, v in LAD.items())}).")

    BOOKKEY = list(booked["U56"].keys())

    # ---- machinery gates
    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=REF_COST, freq="W")["returns"].values
    gr, tu = nrun(pan, Wt, pan.seg["W"])
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - at_cost(gr, tu, REF_COST)[WARMUP:])))
    gate("G1 fast runner @10bps == engine.backtest on the decision-time frame", g1, 1e-10,
         g1 < 1e-10)
    g1b = max(float(np.nanmax(np.abs(
        backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=c, freq="W")["returns"].values[WARMUP:]
        - at_cost(gr, tu, c)[WARMUP:]))) for c in COSTS)
    gate("G2 r(c) = gross - turn*c/1e4 == engine.backtest at EVERY cost rung", g1b, 1e-10,
         g1b < 1e-10)
    lm = mdd(at_cost(*nrun(pan, A_G * frames_all["U56"][(A_N, A_H, "W")], pan.seg["W"]),
                     REF_COST)[WARMUP:])
    lmv = mdd(bench["U56"]["live"][WARMUP:])
    gate("G3 live RULES v2 U56 MaxDD == the record's committed -12.05%", lmv,
         LIVE_MAXDD_COMMITTED, abs(lmv - LIVE_MAXDD_COMMITTED) < 5e-4)
    anc = [booked["U56"][(l, ANCHOR_RUNG[l])] for l in LADS]
    g4 = float(max(np.abs(a - anc[0]).max() for a in anc))
    anct = [turned["U56"][(l, ANCHOR_RUNG[l])] for l in LADS]
    g4t = float(max(np.abs(a - anct[0]).max() for a in anct))
    gate("G4 the anchor rung of all four ladders is ONE book, returns AND turnover",
         max(g4, g4t), 0.0, max(g4, g4t) == 0.0)
    gz = float(max(np.abs(at_cost(booked["U56"][k], turned["U56"][k], 0.0)
                          - booked["U56"][k]).max() for k in BOOKKEY))
    gate("G5 the 0 bps rung is the gross book exactly", gz, 0.0, gz == 0.0)
    say(f"    G1 {g1:.3e}   G2 {g1b:.3e}   G3 live U56 MaxDD {lmv:.4%}  (anchor book "
        f"{lm:.4%})   G4 {max(g4,g4t):.3e}   G5 {gz:.3e}")

    # ---- TURNOVER TABLE: the mechanical fact, independent of c
    say("")
    say("  (A1) ANNUALISED ONE-WAY TURNOVER of every rung book, post-warm-up, and the DRAG in")
    say("       pp/yr of CAGR that each cost rung takes out of it.  This is dial-free.")
    trow = []
    for pan in panels:
        for k in BOOKKEY:
            lad, rung = k
            gr, tu = booked[pan.name][k], turned[pan.name][k]
            lo, hi = pan.i0, len(gr)
            a = annturn(tu, lo, hi)
            base = cagr(at_cost(gr, tu, 0.0)[lo:hi])
            d = dict(panel=pan.name, ladder=lad, rung=rung,
                     is_anchor=bool(rung == ANCHOR_RUNG[lad]), ann_turnover=a, CAGR_0bps=base)
            for c in COSTS:
                r = at_cost(gr, tu, c)[lo:hi]
                d[f"CAGR_{int(c)}"] = cagr(r)
                d[f"Sharpe_{int(c)}"] = sharpe(r)
                d[f"drag_pp_{int(c)}"] = 100.0 * (base - cagr(r))
            trow.append(d)
    TT = pd.DataFrame(trow)
    TT.to_csv(f"{OUT}.turnover.csv", index=False)
    say("")
    say("       panel   ladder    rung     ann turnover   drag pp/yr @10 / @25 / @50   "
        "Sharpe @0 / @10 / @50")
    for pan in panels:
        for lad in LADS:
            s = TT[(TT.panel == pan.name) & (TT.ladder == lad)]
            for _, r in s.iterrows():
                mark = " <- ANCHOR" if r.is_anchor else ""
                say(f"       {r.panel:6s}  {r.ladder:8s} {str(r.rung):6s}   {r.ann_turnover:9.3f}"
                    f"      {r.drag_pp_10:5.2f} / {r.drag_pp_25:5.2f} / {r.drag_pp_50:5.2f}    "
                    f"   {r.Sharpe_0:6.4f} / {r.Sharpe_10:6.4f} / {r.Sharpe_50:6.4f}{mark}")
        say("")

    # ---- the anchor's turnover rank inside its own ladder
    say("  (A2) WHERE THE ANCHOR SITS IN ITS OWN LADDER'S TURNOVER ORDER (1 = slowest):")
    ranks = []
    for pan in panels:
        for lad in LADS:
            s = TT[(TT.panel == pan.name) & (TT.ladder == lad)].copy()
            s["rk"] = s.ann_turnover.rank(method="min")
            a = s[s.is_anchor].iloc[0]
            ranks.append(dict(panel=pan.name, ladder=lad, n_rungs=len(s), anchor_rank=int(a.rk),
                              anchor_turnover=float(a.ann_turnover),
                              slowest=float(s.ann_turnover.min()),
                              fastest=float(s.ann_turnover.max())))
            say(f"       {pan.name:6s} {lad:8s} anchor rank {int(a.rk)} of {len(s)}  "
                f"(anchor {a.ann_turnover:.3f}, ladder range "
                f"{s.ann_turnover.min():.3f}..{s.ann_turnover.max():.3f})")
    pd.DataFrame(ranks).to_csv(f"{OUT}.anchorrank.csv", index=False)

    # ---- folds
    folds = {}
    for pan in panels:
        folds[pan.name] = make_folds(pan)
        cover = sorted(set((o0, o1) for (_y, _lo, _hi, o0, o1) in folds[pan.name]))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        gate(f"G6 folds tile {pan.name} with no overlap and no gap", float(gap), 0.0, gap == 0)
    say("")
    say(f"    FOLDS: {len(folds['U56'])} per panel, {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}; "
        f"IS = warm-up to the day before the fold, OOS = the fold year.")

    # ------------------------------------------------------------------ pick sets (1224's)
    say("")
    say("=" * 108)
    say("ARM B — THE PICK SETS (1224's three, rebuilt; picks FROZEN at the record's 10 bps)")
    say("=" * 108)

    def is_sharpe(p, lad, rung, lo, hi, c):
        return sharpe(at_cost(booked[p][(lad, rung)], turned[p][(lad, rung)], c)[lo:hi])

    def argmax_rung(p, lad, lo, hi, c):
        v = [(is_sharpe(p, lad, r, lo, hi, c), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    picks = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds[pan.name]:
            for lad in LADS:
                r = argmax_rung(pan.name, lad, lo, hi, REF_COST)
                picks.append(dict(pickset="P_AXIS", panel=pan.name, fold=y, ladder=lad, rung=r,
                                  lo=lo, hi=hi, o0=o0, o1=o1))
            spr = {}
            for lad in LADS:
                v = [is_sharpe(pan.name, lad, r, lo, hi, REF_COST) for r in LAD[lad]]
                v = [x for x in v if np.isfinite(x)]
                spr[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
            wid = max(spr, key=lambda k: (spr[k] if np.isfinite(spr[k]) else -np.inf))
            picks.append(dict(pickset="P_1214", panel=pan.name, fold=y, ladder=wid,
                              rung=argmax_rung(pan.name, wid, lo, hi, REF_COST),
                              lo=lo, hi=hi, o0=o0, o1=o1))

    say("")
    say("  (B1) P_TEXT — the record's OWN committed rule-8 picks, harvested exactly as 1224.")
    U, nmd = units()
    HV = harvest(U)
    HV.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    say(f"       {len(HV):,} committed units over {nmd:,} .md files + LEADERBOARD + CHANGELOG "
        f"(1224 read 33,861 over 1,160 — the tree has grown since; the DRIFT is reported,")
    say("       not corrected for, and P_AXIS carries the replay gate precisely because it is")
    say("       text-independent).")
    say(f"       rule-8 context {int(HV.RULE8.sum()):,} ({HV.RULE8.mean():.4f}); "
        f"AND a pick verb {int((HV.RULE8 & HV.PICK).sum()):,}; "
        f"CHECKABLE {int(HV.CHECKABLE.sum()):,} ({HV.CHECKABLE.mean():.4f}).")
    trips = {}
    for _, r in HV[HV.CHECKABLE].iterrows():
        for pn in r.panels.split("|"):
            for tk in r.triples.split("|"):
                lad, rv = tk.split("=")
                rung = (rv if lad == "CADENCE" else
                        (float(rv) if lad == "GROSS" else int(rv)))
                trips.setdefault((pn, lad, rung), 0)
                trips[(pn, lad, rung)] += 1
    say(f"       {len(trips)} DISTINCT committed (panel, ladder, rung) picks over "
        f"{sum(trips.values()):,} unit-mentions.")
    bad = [k for k in trips if k[2] not in LAD[k[1]]]
    gate("G7 every harvested rung is a rung of the record's committed ladder", float(len(bad)),
         0.0, len(bad) == 0)
    ilim = {pan.name: pan.idx.searchsorted(pd.Timestamp(OOS_START)) for pan in panels}
    for (pn, lad, rung), _n in sorted(trips.items(), key=lambda kv: (kv[0][0], kv[0][1],
                                                                    str(kv[0][2]))):
        pobj = [p for p in panels if p.name == pn][0]
        for (y, _lo, _hi, o0, o1) in folds[pn]:
            if y < 2017:
                continue
            picks.append(dict(pickset="P_TEXT", panel=pn, fold=y, ladder=lad, rung=rung,
                              lo=pobj.i0, hi=ilim[pn], o0=o0, o1=o1))
    P = pd.DataFrame(picks)
    say(f"       PICK SETS: P_1214 {int((P.pickset=='P_1214').sum())} cells, "
        f"P_AXIS {int((P.pickset=='P_AXIS').sum())}, "
        f"P_TEXT {int((P.pickset=='P_TEXT').sum())}.")
    gate("G8 P_AXIS is 1224's 168 cells (3 panels x 4 ladders x 14 folds)",
         float((P.pickset == "P_AXIS").sum()), 168.0, int((P.pickset == "P_AXIS").sum()) == 168)

    # ------------------------------------------------------------------ price every cell
    say("")
    say("  (B2) THE PRICE AT EVERY COST RUNG.  All 12 cells published.  For each pick the")
    say("       anchor book and the picked book are read on the SAME fold window at the SAME")
    say("       rung, and their annualised turnovers are recorded alongside.")
    rows = []
    for _, q in P.iterrows():
        k_pick = (q.ladder, q.rung)
        k_anc = (q.ladder, ANCHOR_RUNG[q.ladder])
        gp, tp = booked[q.panel][k_pick], turned[q.panel][k_pick]
        ga, ta = booked[q.panel][k_anc], turned[q.panel][k_anc]
        tp_a, ta_a = annturn(tp, q.o0, q.o1), annturn(ta, q.o0, q.o1)
        d = dict(pickset=q.pickset, panel=q.panel, fold=q.fold, ladder=q.ladder, rung=q.rung,
                 at_anchor=bool(q.rung == ANCHOR_RUNG[q.ladder]),
                 turn_pick=tp_a, turn_anchor=ta_a, turn_delta=ta_a - tp_a)
        for c in COSTS:
            sp = sharpe(at_cost(gp, tp, c)[q.o0:q.o1])
            sa = sharpe(at_cost(ga, ta, c)[q.o0:q.o1])
            d[f"S_pick_{int(c)}"] = sp
            d[f"S_anc_{int(c)}"] = sa
            d[f"delta_{int(c)}"] = sa - sp
            d[f"drag_pick_{int(c)}"] = 100.0 * (cagr(at_cost(gp, tp, 0.0)[q.o0:q.o1])
                                                - cagr(at_cost(gp, tp, c)[q.o0:q.o1]))
            d[f"drag_anc_{int(c)}"] = 100.0 * (cagr(at_cost(ga, ta, 0.0)[q.o0:q.o1])
                                               - cagr(at_cost(ga, ta, c)[q.o0:q.o1]))
        rows.append(d)
    D = pd.DataFrame(rows)
    D.to_csv(f"{OUT}.picks.csv.gz", index=False, compression="gzip")

    za = D[D.at_anchor][[f"delta_{int(c)}" for c in COSTS]].abs().values
    za = float(np.nanmax(za)) if za.size else 0.0
    gate("G9 a pick already AT the anchor has delta 0 at every cost rung", za, 0.0, za == 0.0)

    say("")
    say("       pick set   rung   picks  move   mean turnover pick/anchor   DELTA      SE      t"
        "     SHARE")
    grid = []
    for ps in PICKSETS:
        s = D[D.pickset == ps]
        d0, _, _, _, _ = clustered(s["delta_0"].values, s.fold.values)
        for c in COSTS:
            m, se, t, n, G = clustered(s[f"delta_{int(c)}"].values, s.fold.values)
            reb = m - d0
            share = (reb / m) if (np.isfinite(m) and m != 0) else np.nan
            grid.append(dict(PICK_SET=ps, COST_BPS=c, picks=n, folds=G,
                             move_rate=float((~s.at_anchor).mean()),
                             turn_pick=float(s.turn_pick.mean()),
                             turn_anchor=float(s.turn_anchor.mean()),
                             drag_pick_pp=float(s[f"drag_pick_{int(c)}"].mean()),
                             drag_anc_pp=float(s[f"drag_anc_{int(c)}"].mean()),
                             mean_S_pick=float(s[f"S_pick_{int(c)}"].mean()),
                             mean_S_anchor=float(s[f"S_anc_{int(c)}"].mean()),
                             DELTA=m, SE=se, t=t, GROSS_PART=d0, REBATE=reb, SHARE=share))
            say(f"       {ps:9s} {int(c):4d}  {n:6d}  {(~s.at_anchor).mean():.3f}  "
                f"{s.turn_pick.mean():8.3f} /{s.turn_anchor.mean():8.3f}      "
                f"{m:+.4f}  {se if np.isfinite(se) else 0:.4f} {t:+6.2f}   "
                f"{share if np.isfinite(share) else float('nan'):+7.3f}")
    GR = pd.DataFrame(grid)
    GR.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- replay gates against 1224's committed 10 bps numbers.
    # data/prices.csv is rewritten by the nightly close, so the tape this run reads is NOT the
    # tape 1224 read (it ends 2026-09-17, 1224's ended 2026-09-16).  The gate is therefore
    # SPLIT, and the drift is MEASURED rather than tolerated: G10 replays 1224's DELTA and SE
    # on the LIVE tape (the object this run re-prices), G11 replays its LEVELS on 1224's own
    # truncated tape.  Neither bar was widened to make a number pass.
    say("")
    say("       REPLAY.  This tree's prices.csv ends "
        f"{panels[0].idx[-1].date()}; 1224 ran on the tape ending {REPLAY_END}.  The levels")
    say("       are therefore NOT expected to match to 1e-4 on the live tape and the gate does")
    say("       not pretend otherwise: G10 is the DELTA/SE on the live tape, G11 is the FULL")
    say("       leg re-run on 1224's truncated tape.")
    for ps, C in (("P_AXIS", C1224_AXIS), ("P_1214", C1224_1214)):
        s = D[D.pickset == ps]
        mp, ma = float(s["S_pick_10"].mean()), float(s["S_anc_10"].mean())
        dm, dse, _, _, _ = clustered(s["delta_10"].values, s.fold.values)
        err = max(abs(dm - C["delta"]), abs(dse - C["SE"]))
        lev = max(abs(mp - C["mean_OOS"]), abs(ma - C["anc_OOS"]))
        gate(f"G10 {ps} @10bps replays 1224's committed DELTA and SE on the LIVE tape",
             float(err), 5e-4, err < 5e-4)
        say("")
        say(f"       G10 {ps} @ 10 bps, live tape: pick {mp:.4f} (1224 {C['mean_OOS']}), "
            f"anchor {ma:.4f} ({C['anc_OOS']}), delta {dm:+.4f} ({C['delta']:+.4f}), "
            f"SE {dse:.4f} ({C['SE']:.4f}) — delta/SE dev {err:.2e}, LEVEL drift {lev:.2e}.")
    say("")
    say(f"       G11 — the same two legs re-run on the tape truncated to {REPLAY_END}:")
    RP = replay_levels(REPLAY_END)
    rprows = []
    for ps, C in (("P_AXIS", C1224_AXIS), ("P_1214", C1224_1214)):
        r = RP[ps]
        err = max(abs(r["mean_OOS"] - C["mean_OOS"]), abs(r["anc_OOS"] - C["anc_OOS"]),
                  abs(r["delta"] - C["delta"]), abs(r["SE"] - C["SE"]))
        gate(f"G11 {ps} @10bps replays 1224's committed LEVELS on 1224's own tape", float(err),
             1e-4, err < 1e-4)
        rprows.append(dict(pickset=ps, tape=REPLAY_END, picks=r["n"], pick=r["mean_OOS"],
                           anchor=r["anc_OOS"], delta=r["delta"], SE=r["SE"],
                           committed_pick=C["mean_OOS"], committed_anchor=C["anc_OOS"],
                           committed_delta=C["delta"], committed_SE=C["SE"], max_dev=err))
        say(f"             {ps:7s} pick {r['mean_OOS']:.4f} ({C['mean_OOS']}), anchor "
            f"{r['anc_OOS']:.4f} ({C['anc_OOS']}), delta {r['delta']:+.4f} "
            f"({C['delta']:+.4f}), SE {r['SE']:.4f} ({C['SE']:.4f}) — max dev {err:.2e}.")
    pd.DataFrame(rprows).to_csv(f"{OUT}.replay.csv", index=False)

    # ---- by ladder and panel, at every rung (S_ALL is frozen; this is where the sign lives)
    say("")
    say("  (B3) DELTA BY LADDER AND PANEL AT EVERY COST RUNG (P_AXIS — the queue's 168):")
    cut = []
    s0 = D[D.pickset == "P_AXIS"]
    for col in ("ladder", "panel"):
        for v, g in s0.groupby(col):
            d0, _, _, _, _ = clustered(g["delta_0"].values, g.fold.values)
            line = f"       {col:7s} {str(v):9s} turn {g.turn_pick.mean():7.3f}/" \
                   f"{g.turn_anchor.mean():7.3f}  "
            for c in COSTS:
                m, se, t, n, _ = clustered(g[f"delta_{int(c)}"].values, g.fold.values)
                cut.append(dict(cut=col, value=v, COST_BPS=c, picks=n, DELTA=m, SE=se, t=t,
                                GROSS_PART=d0, REBATE=m - d0,
                                SHARE=(m - d0) / m if m else np.nan,
                                turn_pick=float(g.turn_pick.mean()),
                                turn_anchor=float(g.turn_anchor.mean())))
                line += f"  @{int(c):2d} {m:+.4f}(t{t:+5.2f})"
            say(line)
    pd.DataFrame(cut).to_csv(f"{OUT}.bycut.csv", index=False)

    # ---- robustness: the chooser ALSO sees cost c (NOT a dial; reported, not verdicted on)
    say("")
    say("  (B4) ROBUSTNESS (not a dial): if the CHOOSER also pays c, does it pick slower rungs")
    say("       and does the delta shrink on its own?")
    rob = []
    for c in COSTS:
        drow, frow, mv = [], [], []
        for pan in panels:
            for (y, lo, hi, o0, o1) in folds[pan.name]:
                for lad in LADS:
                    r = argmax_rung(pan.name, lad, lo, hi, c)
                    a = ANCHOR_RUNG[lad]
                    sp = sharpe(at_cost(booked[pan.name][(lad, r)],
                                        turned[pan.name][(lad, r)], c)[o0:o1])
                    sa = sharpe(at_cost(booked[pan.name][(lad, a)],
                                        turned[pan.name][(lad, a)], c)[o0:o1])
                    drow.append(sa - sp)
                    frow.append(y)
                    mv.append(r != a)
        m, se, t, n, _ = clustered(drow, frow)
        rob.append(dict(COST_BPS=c, picks=n, move_rate=float(np.mean(mv)), DELTA=m, SE=se, t=t))
        say(f"       chooser @ {int(c):2d} bps: move rate {np.mean(mv):.4f}  "
            f"DELTA {m:+.4f}  SE {se if np.isfinite(se) else 0:.4f}  t {t:+.2f}")
    pd.DataFrame(rob).to_csv(f"{OUT}.robust.csv", index=False)

    # ------------------------------------------------------------------ ARM D — the omitted switch
    say("")
    say("=" * 108)
    say("ARM D — THE RE-BOOKING COST 1224's SLICED ACCOUNTING NEVER CHARGED")
    say("=" * 108)
    say("")
    say("  1224 read each fold's OOS Sharpe off a book run CONTINUOUSLY over the whole tape, so")
    say("  a pick that CHANGES between folds paid nothing for the switch.  Here the REALISED")
    say("  STITCHED book holds fold f's pick during fold f and pays the true turnover on the")
    say("  switch day.  The anchor, by construction, never switches — that is the queue's")
    say("  'the anchor holds ONE book across the whole tape'.")

    def stitched(pan, lad, cost_for_choice):
        """Realised moving-pick book: fold f's IS argmax held through fold f, re-booked (and
        charged) on the switch day.  Returns (gross, turn, span, n_switch, seq)."""
        fl = folds[pan.name]
        span = (fl[0][3], fl[-1][4])
        W = np.zeros_like(pan.rets)
        reb, prev, nsw, seq = [], None, 0, []
        for (y, lo, hi, o0, o1) in fl:
            r = argmax_rung(pan.name, lad, lo, hi, cost_for_choice)
            seq.append((y, r))
            freq, fkey, g = rebs[pan.name][(lad, r)]
            fr = g * frames_all[pan.name][fkey]
            W[o0:o1] = fr[o0:o1]
            days = [d for d in pan.seg[freq] if o0 <= d < o1]
            if prev is not None and r != prev:
                nsw += 1
                if o0 not in days:
                    days = [o0] + days
            elif prev is None and o0 not in days:
                days = [o0] + days
            reb.extend(days)
            prev = r
        reb = np.array(sorted(set(reb)), dtype=np.int64)
        reb = reb[(reb >= span[0]) & (reb < span[1])]
        gr, tu = nrun(pan, W, reb)
        return gr, tu, span, nsw, seq

    strows = []
    for pan in panels:
        spy_full = pan.spy
        for lad in LADS:
            gs, ts, span, nsw, seq = stitched(pan, lad, REF_COST)
            lo, hi = span
            ka = (lad, ANCHOR_RUNG[lad])
            ga, ta = booked[pan.name][ka], turned[pan.name][ka]
            bm = bmpack(spy_full[lo:hi])
            lv = bmpack(bench[pan.name]["live"][lo:hi])
            for c in COSTS:
                rs = at_cost(gs, ts, c)[lo:hi]
                ra = at_cost(ga, ta, c)[lo:hi]
                k4a_s, k4b_s, ms, h1s, h2s = keep_paths(rs, bm, lv)
                k4a_a, k4b_a, ma, h1a, h2a = keep_paths(ra, bm, lv)
                strows.append(dict(
                    panel=pan.name, ladder=lad, COST_BPS=c, n_switch=nsw,
                    seq="|".join(f"{y}:{r}" for y, r in seq),
                    turn_stitched=annturn(ts, lo, hi), turn_anchor=annturn(ta, lo, hi),
                    CAGR_stitched=ms["CAGR"], Sharpe_stitched=ms["Sharpe"],
                    MaxDD_stitched=ms["MaxDD"], H1_stitched=h1s, H2_stitched=h2s,
                    CAGR_anchor=ma["CAGR"], Sharpe_anchor=ma["Sharpe"],
                    MaxDD_anchor=ma["MaxDD"], H1_anchor=h1a, H2_anchor=h2a,
                    d_Sharpe=ma["Sharpe"] - ms["Sharpe"],
                    SPY_CAGR=bm["CAGR"], SPY_Sharpe=bm["Sharpe"], SPY_MaxDD=bm["MaxDD"],
                    LIVE_CAGR=lv["CAGR"], LIVE_Sharpe=lv["Sharpe"], LIVE_MaxDD=lv["MaxDD"],
                    k4a_stitched=k4a_s, k4b_stitched=k4b_s,
                    k4a_anchor=k4a_a, k4b_anchor=k4b_a))
    ST = pd.DataFrame(strows)
    ST.to_csv(f"{OUT}.stitched.csv", index=False)
    say("")
    say("       panel   ladder   switches  ann turnover stitched/anchor   "
        "d_Sharpe(anchor-stitched) @0/@10/@25/@50")
    for pan in panels:
        for lad in LADS:
            s = ST[(ST.panel == pan.name) & (ST.ladder == lad)].set_index("COST_BPS")
            r0 = s.loc[0.0]
            say(f"       {pan.name:6s}  {lad:8s} {int(r0.n_switch):6d}    "
                f"{r0.turn_stitched:8.3f} /{r0.turn_anchor:8.3f}         "
                + "  ".join(f"{s.loc[c].d_Sharpe:+.4f}" for c in COSTS))
    nsc = int(ST[ST.COST_BPS == 0.0].n_switch.sum())
    gate("G12 the stitched books actually switch (the re-booking cost is non-trivial)",
         float(nsc), 1.0, nsc >= 1)
    sam = ST[(ST.COST_BPS == 0.0) & (ST.ladder == "GROSS")]
    say("")
    say(f"       Total fold-boundary switches across 12 (panel, ladder) stitched books: {nsc}.")
    say("       4a / 4b on the stitched books at 10 bps: "
        f"{int(ST[(ST.COST_BPS==REF_COST)].k4a_stitched.sum())} / "
        f"{int(ST[(ST.COST_BPS==REF_COST)].k4b_stitched.sum())} of "
        f"{int((ST.COST_BPS==REF_COST).sum())}; anchor books "
        f"{int(ST[(ST.COST_BPS==REF_COST)].k4a_anchor.sum())} / "
        f"{int(ST[(ST.COST_BPS==REF_COST)].k4b_anchor.sum())}.")

    # ------------------------------------------------------------------ ARM E — rule 8 proper
    say("")
    say("=" * 108)
    say("ARM E — PROTOCOL RULE 8 (rungs chosen on warm-up..2016-12-31 ONLY; 2017-2026 read once)")
    say("=" * 108)
    wf = []
    for pan in panels:
        i1 = int(pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        lo, hi = pan.i0, len(pan.rets)
        bm = bmpack(pan.spy[i1:hi])
        lv = bmpack(bench[pan.name]["live"][i1:hi])
        for lad in LADS:
            a = ANCHOR_RUNG[lad]
            for c in COSTS:
                r = argmax_rung(pan.name, lad, lo, i1, c)
                for arm, rung in (("IS_ARGMAX", r), ("ANCHOR", a)):
                    gb, tb = booked[pan.name][(lad, rung)], turned[pan.name][(lad, rung)]
                    full = at_cost(gb, tb, c)[lo:hi]
                    oos = at_cost(gb, tb, c)[i1:hi]
                    k4a, k4b, m, h1, h2 = keep_paths(oos, bm, lv)
                    k4aF, k4bF, mF, h1F, h2F = keep_paths(
                        full, bmpack(pan.spy[lo:hi]), bmpack(bench[pan.name]["live"][lo:hi]))
                    wf.append(dict(
                        panel=pan.name, ladder=lad, COST_BPS=c, arm=arm, rung=rung,
                        IS_argmax=r, ann_turnover=annturn(tb, i1, hi),
                        full_CAGR=mF["CAGR"], full_Sharpe=mF["Sharpe"], full_MaxDD=mF["MaxDD"],
                        full_H1=h1F, full_H2=h2F,
                        OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"],
                        OOS_H1=h1, OOS_H2=h2,
                        SPY_OOS_CAGR=bm["CAGR"], SPY_OOS_Sharpe=bm["Sharpe"],
                        SPY_OOS_MaxDD=bm["MaxDD"],
                        LIVE_OOS_CAGR=lv["CAGR"], LIVE_OOS_Sharpe=lv["Sharpe"],
                        LIVE_OOS_MaxDD=lv["MaxDD"],
                        k4a_full=k4aF, k4b_full=k4bF, k4a_OOS=k4a, k4b_OOS=k4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       panel   ladder  cost  arm        rung   turnover  OOS CAGR / Sharpe / MaxDD"
        "   4a  4b")
    for _, r in WF.iterrows():
        say(f"       {r.panel:6s}  {r.ladder:7s} {int(r.COST_BPS):4d}  {r.arm:9s} "
            f"{str(r.rung):6s} {r.ann_turnover:8.3f}  {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} /"
            f" {r.OOS_MaxDD:7.2%}   {'T' if r.k4a_OOS else 'F'}   {'T' if r.k4b_OOS else 'F'}")
    say("")
    for pan in panels:
        i1 = int(pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        b = bmpack(pan.spy[i1:])
        l = bmpack(bench[pan.name]["live"][i1:])
        say(f"       BENCHMARKS {pan.name:6s} OOS: SPY {b['CAGR']:.2%} / {b['Sharpe']:.4f} / "
            f"{b['MaxDD']:.2%} (H {b['H1']:.4f}/{b['H2']:.4f});  LIVE RULES v2 "
            f"{l['CAGR']:.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:.2%} "
            f"(H {l['H1']:.4f}/{l['H2']:.4f}).")
    say("")
    say(f"       RULE-8 ROWS: {len(WF)}.  4a full {int(WF.k4a_full.sum())} of {len(WF)}; "
        f"4a OOS {int(WF.k4a_OOS.sum())}; 4b full {int(WF.k4b_full.sum())}; "
        f"4b OOS {int(WF.k4b_OOS.sum())}; BOTH 4b legs "
        f"{int((WF.k4b_full & WF.k4b_OOS).sum())}.")
    dd = WF[WF.arm == "ANCHOR"].set_index(["panel", "ladder", "COST_BPS"]).OOS_Sharpe - \
        WF[WF.arm == "IS_ARGMAX"].set_index(["panel", "ladder", "COST_BPS"]).OOS_Sharpe
    say("       CHOOSER-MINUS-ANCHOR on the rule-8 split, by cost rung: " +
        "  ".join(f"@{int(c)} {dd.xs(c, level='COST_BPS').mean():+.4f}" for c in COSTS))
    r8 = pd.DataFrame(dict(COST_BPS=COSTS,
                           anchor_minus_argmax=[float(dd.xs(c, level="COST_BPS").mean())
                                                for c in COSTS]))
    r8.to_csv(f"{OUT}.rule8_by_cost.csv", index=False)

    # ------------------------------------------------------------------ the verdict
    say("")
    say("=" * 108)
    say("THE ANSWER")
    say("=" * 108)
    ver = []
    for ps in PICKSETS:
        s = GR[GR.PICK_SET == ps].set_index("COST_BPS")
        d0 = float(s.loc[0.0, "DELTA"])
        dref = float(s.loc[REF_COST, "DELTA"])
        share_ref = float(s.loc[REF_COST, "SHARE"])
        entirely = [c for c in COSTS if c > 0
                    and np.isfinite(s.loc[c, "SHARE"]) and s.loc[c, "SHARE"] >= 1.0]
        if all(float(s.loc[c, "DELTA"]) <= 0 for c in COSTS):
            out = "D_NO_GAIN_AT_ANY_RUNG"
        elif d0 <= 0 < dref:
            out = "A_ENTIRELY_REBATE"
        elif share_ref >= 0.50:
            out = "B_MOSTLY_REBATE"
        else:
            out = "C_MOSTLY_GROSS"
        ver.append(dict(PICK_SET=ps, DELTA_0=d0, DELTA_10=dref, SHARE_10=share_ref,
                        entirely_rebate_rungs="|".join(str(int(c)) for c in entirely)
                        if entirely else "NONE",
                        turn_pick=float(s.loc[REF_COST, "turn_pick"]),
                        turn_anchor=float(s.loc[REF_COST, "turn_anchor"]),
                        OUTCOME=out))
        say(f"  {ps:9s} DELTA(0) {d0:+.4f}   DELTA(10) {dref:+.4f}   SHARE(10) "
            f"{share_ref:+.3f}   entirely-rebate rungs: "
            f"{'|'.join(str(int(c)) for c in entirely) if entirely else 'NONE'}   -> {out}")
    VD = pd.DataFrame(ver)
    VD.to_csv(f"{OUT}.verdict.csv", index=False)

    GT = pd.DataFrame(GATES)
    GT.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say("=" * 108)
    say(f"GATES {int(GT.pass_.sum())} of {len(GT)}")
    for _, g in GT.iterrows():
        say(f"  [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value {g.value}  target {g.target}")
    say("")
    say(f"Runtime {time.time()-t0:.1f}s.  Offline, deterministic.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
