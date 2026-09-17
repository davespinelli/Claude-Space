#!/usr/bin/env python3
"""
Idea 1227 (lane C, 2026-09-17) — should H_RUNNERUP replace the record's standing HEADLINE FORM?

THE PREMISE, READ FROM THE RECORD.  Idea 1223 walked a synthetic degenerate rung into the
record's four-ladder comparison set and found that H_RUNNERUP (the median-widest ladder against
the SECOND-widest) is the ONLY reading of "the widest dial" a degenerate member cannot
manufacture: it CREATED 0 headline calls at every delta <= 0.30, against 40 of 42 for
H_NARROWEST and 37 of 42 for H_ANY.  That is an argument for adopting H_RUNNERUP as the
record's standing headline form on ROBUSTNESS grounds.  But 1223 also priced it, and it ran
-0.0183 of mean OOS Sharpe against CH_ANCHOR (do nothing) on 42 picks, |t| = 1.16.  Immune to
manufacture is not the same as worth deploying, and 42 picks on ONE expanding IS window cannot
separate "H_RUNNERUP is a worse chooser than holding" from "H_RUNNERUP barely ever moves, and
the two or three times it did were unlucky".

THIS RUN GIVES EVERY HEADLINE FORM DOZENS OF PICKS AND ASKS WHETHER ANY BEATS HOLDING.

  Folds become QUARTERLY rather than annual (55 per panel, 165 (panel, fold) cells per grid
  point against 1223's 42), and the IS window becomes a DIAL rather than a fixed expanding one.
  Each (headline form, IS window) is a deployable chooser: read the comparison set's Sharpe
  spreads on the IS window, apply the record's calibrated conditional two-sided bar B_IID95 in
  that form, and either TUNE to the named ladder's IS-argmax rung or HOLD THE ANCHOR.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  HEADLINE FORM   {H_RUNNERUP, H_NARROWEST, H_ANY}  + the two controls CH_RAW and CH_ANCHOR
  IS WINDOW L     {252, 504, 756, 1260, 2520, EXPANDING} trading days, rolling, ending the day
                  before the fold opens

  30 (form, L) cells, EVERY ONE PUBLISHED, at each of 2 comparison sets and 2 fold cadences.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
COMPARISON SET {ALL4, NG} — the verdict is read off ALL4, the record's OWN standing set, and NG
(1214's degenerate-free set) is carried at every cell as a declared sensitivity, not a choice;
FOLD CADENCE {QUARTER, YEAR} — QUARTER is the primary because the queue asks for dozens of
picks, YEAR is carried because it is 1223's own grid and gate G8 replicates 1223 on it.

THE NULL, BECAUSE "BEATS HOLDING" IS A CLAIM ABOUT A CHOOSER AND NOT ABOUT A BOOK.  Idea 1227
(cloud, same day) found 14 of 32 naive "gain > 0" passes flip under a count-matched bar and
that ALL survivors flip once TIMING is randomised too.  Every gain in this run is therefore
scored against two pre-declared nulls, 2,000 reps each:

  NL_COUNT  move on m randomly chosen folds out of F (m = the chooser's own move count), each
            move going to a uniformly drawn NON-ANCHOR rung book.  Matches COUNT only.
  NL_PERM   the chooser's OWN destination multiset, re-dealt to randomly chosen folds.  Matches
            count AND destinations; only the TIMING is random.

Frozen at the record's construction, inherited from 1207/1214/1223 unchanged: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 /
CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up 260 rows, the
conditional two-sided null band and its Monte-Carlo construction (seed 12141214, so the bands
are literally 1214's and 1223's numbers).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with (form, L) chosen on the IS folds
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every stitched chooser curve and every rule-8 pick; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_should-H_RUNNERUP-replace-the-record-s-standing-HEADLINE-FORM_C.py
"""
from __future__ import annotations

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
SLUG = "should-H_RUNNERUP-replace-the-record-s-standing-HEADLINE-FORM"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
ANCHOR_KEY = ("CADENCE", "W")

LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}

# ---- DIAL 1: headline form (three readings of "the widest dial", 1223's definitions verbatim)
HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
CHOOSERS = HFORMS + ["CH_RAW", "CH_ANCHOR"]

# ---- DIAL 2: IS window length, in trading days; None = EXPANDING (1223's window)
WINDOWS = [252, 504, 756, 1260, 2520, None]
def wname(L):
    return "EXPAND" if L is None else f"L{L}"

# ---- not dials
NG4 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = {"ALL4": ALL4, "NG": NG4}
CADENCES = ["QUARTER", "YEAR"]
BAR = "B_IID95"
MIN_IS = 252
MIN_FOLD = 40

NMC = 1_500_000
MC_SEED = 12141214
NULL_REPS, NULL_SEED = 2000, 12271227
LIVE_MAXDD_COMMITTED = -0.1205

# Hartley's d2(k) = E[range of k iid N(0,1)].  Published constants, gated against Monte Carlo.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

# 1223's committed numbers at (YEAR folds, EXPANDING window), for the replication gate G8.
REP1223 = {("ALL4", "CH_ANCHOR"): (0.000, 1.0362), ("ALL4", "H_RUNNERUP"): (0.048, 1.0179),
           ("ALL4", "H_NARROWEST"): (0.881, 0.9875), ("ALL4", "H_ANY"): (0.881, 0.9875),
           ("ALL4", "CH_RAW"): (1.000, 0.9677), ("NG", "H_NARROWEST"): (0.024, 1.0368),
           ("NG", "H_ANY"): (0.095, 1.0394), ("NG", "H_RUNNERUP"): (0.048, 1.0179)}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def d2(k):
    return D2[min(max(int(k), 2), KMAXD2)]


# ==================================================================== the null machinery (1214)
_RDRAW: dict[int, np.ndarray] = {}


def rdraw(k, n=NMC):
    k = int(k)
    if k in _RDRAW:
        return _RDRAW[k]
    rng = np.random.default_rng(MC_SEED + 1000 * k)
    out = np.empty(n, dtype=np.float64)
    step = 250_000
    for i in range(0, n, step):
        m = min(step, n - i)
        x = rng.standard_normal((m, k))
        out[i:i + m] = x.max(1) - x.min(1)
    _RDRAW[k] = out
    return out


_BAND: dict[tuple, dict] = {}


def nullband(kw, kn):
    """1214's conditional two-sided bar.  V = (R_w/d2(k_w))/(R_n/d2(k_n)) CONDITIONAL on the
    realised orientation R_w >= R_n, which is how the record writes every pair."""
    key = (int(kw), int(kn))
    if key in _BAND:
        return _BAND[key]
    a, b = rdraw(kw), rdraw(kn)
    b = np.roll(b, 7919)
    m = a >= b
    va = (a[m] / d2(kw)) / (b[m] / d2(kn))
    out = dict(k_w=int(kw), k_n=int(kn), median=float(np.median(va)),
               L95=float(np.quantile(va, 0.025)), U95=float(np.quantile(va, 0.975)))
    _BAND[key] = out
    return out


_MEDR: dict[int, float] = {}


def medrange(k):
    k = int(k)
    if k not in _MEDR:
        _MEDR[k] = float(np.median(rdraw(k)))
    return _MEDR[k]


def call_iid95(M, I, band):
    """'W' = the raw-wider ladder is the genuinely wider dial; 'N' = the call REVERSES onto the
    narrower-looking ladder; 'TIE' = the bar declines to name a widest dial at all."""
    V = (M / I) if I > 0 else np.inf
    return "W" if V > band["U95"] else ("N" if V < band["L95"] else "TIE")


# ==================================================================== panels / runner (1207/1214)
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
    """1098/1159's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1 (1209's correction).  Row t is the APPLICATION-time weight."""
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


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 108)
    say("IDEA 1227 (lane C, 2026-09-17) — should H_RUNNERUP replace the record's standing")
    say("HEADLINE FORM?")
    say("=" * 108)
    say("")
    say("  DIAL 1 HEADLINE FORM  H_RUNNERUP / H_NARROWEST / H_ANY  (+ controls CH_RAW, CH_ANCHOR)")
    say(f"  DIAL 2 IS WINDOW      {[wname(L) for L in WINDOWS]}")
    say("  Comparison set (NOT a dial, both reported, verdict read off ALL4): ALL4, NG")
    say("  Fold cadence (NOT a dial, both reported, primary QUARTER): QUARTER, YEAR")
    say("  Bar frozen at B_IID95, the record's calibrated conditional two-sided band.")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any price is read:")
    say("    (A) REPLACE — some headline form beats CH_ANCHOR on mean OOS Sharpe at ALL4 with")
    say("        a fold-clustered |t| >= 2 AND clears BOTH nulls at p <= 0.05, and H_RUNNERUP")
    say("        is that form or is within 1 SE of it.")
    say("    (B) NO STANDING FORM BEATS HOLDING — no form clears (A) at any window.")
    say("    (C) PARTIAL — a form clears the raw bar but not the nulls, or only at one window.")

    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    unb = max(abs(rdraw(k).mean() / d2(k) - 1.0) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G1 R_k/d2(k) unbiased for sigma under the iid null", value=unb,
                      target=5e-3, pass_=bool(unb < 5e-3)))
    say("")
    say(f"  d2(k) MC at {NMC:,} draws reproduces Hartley to {mc_err:.3e}; R_k/d2(k) unbiased to "
        f"{unb:.3e}.")

    # ------------------------------------------------------------------ panels and books
    say("")
    say("=" * 108)
    say("ARM A — THE BOOKS, THE FOLDS, AND THE CHOOSERS")
    say("=" * 108)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mvv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mvv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")

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
        anchor_frame = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            fr = anchor_frame if f == "W" else frames[(A_N, A_H, "M")]
            books[("CADENCE", f)] = nrun(pan, A_G * fr, f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * anchor_frame, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built over 4 ladders "
            f"(N {len(LAD['N'])}, H {len(LAD['H'])}, GROSS {len(LAD['GROSS'])}, CADENCE 2).")

    # ---- identity gates on the anchor
    ident = 0.0
    for pan in panels:
        bk = booked[pan.name]
        for k in (("N", A_N), ("H", A_H), ("GROSS", A_G)):
            ident = max(ident, float(np.nanmax(np.abs(bk[k] - bk[ANCHOR_KEY]))))
    GATES.append(dict(gate="G9 the anchor is one book under four names (N=20 == H=126 == "
                           "GROSS=0.75 == CADENCE=W)", value=ident, target=1e-15,
                      pass_=bool(ident <= 1e-15)))

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g2 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G2 fast runner == engine.backtest on the decision-time frame",
                      value=g2, target=1e-10, pass_=bool(g2 < 1e-10)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G3 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    say(f"    G9 anchor identity {ident:.3e}  G2 runner {g2:.3e}  G3 live U56 MaxDD {lm:.4%}")

    # ---- per-book return matrix, for fast slicing
    RM = {p: np.column_stack([booked[p][k] for k in BOOKKEY]) for p in booked}
    BIDX = {k: i for i, k in enumerate(BOOKKEY)}
    LADIDX = {lad: [BIDX[(lad, r)] for r in LAD[lad]] for lad in LAD}
    ANCHOR_I = BIDX[ANCHOR_KEY]
    # THE ANCHOR IS ONE BOOK UNDER FOUR NAMES (G9): N=20, H=126, GROSS=0.75 and CADENCE=W are
    # the SAME return series.  A chooser that "moves" onto one of them has not moved, and a null
    # that draws one of them as a destination has drawn a no-op.  Both are defined by VALUE.
    ANCHOR_EQ = set()
    for i in range(len(BOOKKEY)):
        if all(float(np.nanmax(np.abs(RM[p][:, i] - RM[p][:, ANCHOR_I]))) == 0.0 for p in RM):
            ANCHOR_EQ.add(i)
    NONANCHOR = np.array([i for i in range(len(BOOKKEY)) if i not in ANCHOR_EQ])
    GATES.append(dict(gate="G10 the anchor-equivalent key set is exactly {N=20, H=126, "
                           "GROSS=0.75, CADENCE=W}", value=float(len(ANCHOR_EQ)), target=4.0,
                      pass_=bool(sorted(BOOKKEY[i] for i in ANCHOR_EQ)
                                 == sorted([("N", A_N), ("H", A_H), ("GROSS", A_G), ANCHOR_KEY]))))
    say(f"    ANCHOR-EQUIVALENT BOOKS (by value, not by name): "
        f"{sorted(BOOKKEY[i] for i in ANCHOR_EQ)} — a pick landing on any of these is NOT a move,")
    say(f"    and the null's destination pool is the remaining {len(NONANCHOR)} books.")

    # ------------------------------------------------------------------ folds
    say("")
    say("  FOLDS.  A fold is one calendar QUARTER (primary) or one calendar YEAR (1223's grid),")
    say("  out of sample; the IS window ends the trading day BEFORE the fold opens.")
    folds = {}
    for cad in CADENCES:
        for pan in panels:
            keyv = (pan.idx.year.values * 10 + pan.idx.quarter.values) if cad == "QUARTER" \
                else pan.idx.year.values
            out = []
            cover = []
            for v in sorted(set(keyv.tolist())):
                oo = np.flatnonzero(keyv == v)
                oo = oo[oo >= pan.i0 + MIN_IS]
                if len(oo) < MIN_FOLD:
                    continue
                o0, o1 = int(oo[0]), int(oo[-1]) + 1
                if o0 - pan.i0 < MIN_IS:
                    continue
                out.append((v, o0, o1))
                cover.append((o0, o1))
            cover = sorted(set(cover))
            gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
            GATES.append(dict(gate=f"G4 {cad} folds tile {pan.name} with no overlap and no gap",
                              value=float(gap), target=0.0, pass_=bool(gap == 0)))
            folds[(cad, pan.name)] = out
    for cad in CADENCES:
        n = sum(len(folds[(cad, p.name)]) for p in panels)
        say(f"    {cad:8s}: {n:4d} (panel, fold) cells  "
            + "  ".join(f"{p.name} {len(folds[(cad, p.name)])} "
                        f"({folds[(cad,p.name)][0][0]}-{folds[(cad,p.name)][-1][0]})"
                        for p in panels))

    # ------------------------------------------------------------------ chooser machinery
    _SP: dict = {}

    def spread_of(p, lad, lo, hi):
        key = (p, lad, lo, hi)
        if key in _SP:
            return _SP[key]
        v = [sharpe(RM[p][lo:hi, i]) for i in LADIDX[lad]]
        v = [x for x in v if np.isfinite(x)]
        s = (max(v) - min(v)) if len(v) > 1 else np.nan
        _SP[key] = s
        return s

    def pick_of(p, lad, lo, hi):
        v = [(sharpe(RM[p][lo:hi, i]), i) for i in LADIDX[lad]]
        v = [(s, i) for s, i in v if np.isfinite(s)]
        return max(v)[1] if v else ANCHOR_I

    def headline(p, lo, hi, lads):
        """1223's three readings of 'the widest dial', all at B_IID95."""
        sp = {lad: spread_of(p, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        if len(good) < 2:
            return {hf: (None) for hf in HFORMS} | {"_widest": None}
        order = sorted(good, key=lambda k: good[k] / medrange(LADK[k]), reverse=True)
        w = order[0]
        out = {}
        for hf, comparand in (("H_RUNNERUP", order[1]), ("H_NARROWEST", order[-1])):
            if comparand == w:
                out[hf] = None
                continue
            a, b = (w, comparand) if good[w] >= good[comparand] else (comparand, w)
            M_ = (good[a] / good[b]) if good[b] > 0 else (np.inf if good[a] > 0 else 1.0)
            I_ = d2(LADK[a]) / d2(LADK[b])
            c = call_iid95(M_, I_, nullband(LADK[a], LADK[b]))
            out[hf] = None if c == "TIE" else (a if c == "W" else b)
        anyd = False
        for a in lads:
            for b in lads:
                if a == b or not (np.isfinite(sp.get(a, np.nan)) and np.isfinite(sp.get(b, np.nan))):
                    continue
                if sp[a] < sp[b] or (sp[a] == sp[b] and a > b):
                    continue
                M_ = (sp[a] / sp[b]) if sp[b] > 0 else (np.inf if sp[a] > 0 else 1.0)
                I_ = d2(LADK[a]) / d2(LADK[b])
                if call_iid95(M_, I_, nullband(LADK[a], LADK[b])) != "TIE":
                    anyd = True
        out["H_ANY"] = w if anyd else None
        out["_widest"] = w
        return out

    def choose(p, o0, L, sname):
        """Returns {chooser: book index} for one (panel, fold, window, set) cell."""
        lads = SETS[sname]
        lo = pan_i0[p] if L is None else max(pan_i0[p], o0 - L)
        hi = o0
        hd = headline(p, lo, hi, lads)
        sp = {lad: spread_of(p, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        raw_w = max(good, key=good.get) if good else None
        out = {"CH_ANCHOR": ANCHOR_I,
               "CH_RAW": ANCHOR_I if raw_w is None else pick_of(p, raw_w, lo, hi)}
        for hf in HFORMS:
            named = hd[hf]
            out[hf] = ANCHOR_I if named is None else pick_of(p, named, lo, hi)
        return out, (hi - lo)

    pan_i0 = {p.name: p.i0 for p in panels}
    PAN = {p.name: p for p in panels}

    # ------------------------------------------------------------------ the walk
    say("")
    say("  THE WALK.  Every (cadence, panel, fold, set, window) cell is evaluated for all five")
    say("  choosers; nothing is selected on.")
    prows = []
    picks: dict = {}
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            for (v, o0, o1) in fl:
                for sname in SETS:
                    for L in WINDOWS:
                        sel, islen = choose(pan.name, o0, L, sname)
                        for ch in CHOOSERS:
                            bi = sel[ch]
                            r = RM[pan.name][o0:o1, bi]
                            picks.setdefault((cad, pan.name, sname, wname(L), ch), []).append(
                                (v, o0, o1, bi))
                            prows.append(dict(cadence=cad, panel=pan.name, fold=v, SET=sname,
                                              window=wname(L), IS_len=islen, chooser=ch,
                                              ladder=BOOKKEY[bi][0], rung=BOOKKEY[bi][1],
                                              moved=bool(bi not in ANCHOR_EQ), moved_key=bool(bi != ANCHOR_I),
                                              OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r),
                                              OOS_MaxDD=mdd(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv = float(pdf[pdf.chooser == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G5 CH_ANCHOR move rate == 0", value=mv, target=0.0,
                      pass_=bool(mv == 0.0)))
    dk = float(pdf.moved_key.mean() - pdf.moved.mean())
    GATES.append(dict(gate="G11 a value-based move rate never exceeds 1223's key-based one",
                      value=dk, target=0.0, pass_=bool(dk >= 0.0)))
    say(f"    MOVE RATE, 1223's KEY DEFINITION {pdf.moved_key.mean():.4f} vs THIS RUN'S VALUE "
        f"DEFINITION {pdf.moved.mean():.4f}: {dk:.4f} of all pick-cells are 'moves' onto a book")
    say("    that IS the anchor.  Every delta and every Sharpe below is unaffected (the books are")
    say("    identical); the MOVE RATE and the null's destination pool are.")
    nq = len(pdf[pdf.cadence == "QUARTER"])
    say(f"    {len(pdf):,} pick-cells ({nq:,} at QUARTER): "
        f"{sum(len(folds[('QUARTER', p.name)]) for p in panels)} (panel, fold) x {len(SETS)} sets "
        f"x {len(WINDOWS)} windows x {len(CHOOSERS)} choosers.")

    # ---- G8: replicate 1223 at (YEAR, EXPAND)
    rep_err = 0.0
    for (sname, ch), (mv23, ms23) in REP1223.items():
        s = pdf[(pdf.cadence == "YEAR") & (pdf.window == "EXPAND") & (pdf.SET == sname)
                & (pdf.chooser == ch) & (pdf.fold >= 2013)]
        if not len(s):
            continue
        rep_err = max(rep_err, abs(float(s.moved_key.mean()) - mv23),
                      abs(float(s.OOS_Sharpe.mean()) - ms23))
    GATES.append(dict(gate="G8 (YEAR, EXPAND) replicates 1223's committed move rates and mean "
                           "OOS Sharpes", value=rep_err, target=2e-2, pass_=bool(rep_err < 2e-2)))
    say(f"    G8 replication of 1223 at (YEAR, EXPAND): worst deviation {rep_err:.4f} over "
        f"{len(REP1223)} committed (set, chooser) numbers.")

    # ------------------------------------------------------------------ ARM B: does any beat holding
    say("")
    say("=" * 108)
    say("ARM B — DOES ANY HEADLINE FORM BEAT HOLDING?  PAIRED DELTAS AND TWO MATCHED NULLS")
    say("=" * 108)

    # per (cadence, panel) fold Sharpe matrix + aggregates, for exact null statistics
    FS, FSUM, FSQ, FN, FOL = {}, {}, {}, {}, {}
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            M = RM[pan.name]
            S = np.empty((len(fl), M.shape[1]))
            SU = np.empty_like(S)
            SQ = np.empty_like(S)
            NN = np.empty(len(fl))
            for i, (v, o0, o1) in enumerate(fl):
                sl = M[o0:o1]
                SU[i] = sl.sum(0)
                SQ[i] = (sl * sl).sum(0)
                NN[i] = o1 - o0
                mu = SU[i] / NN[i]
                sd = np.sqrt(np.maximum(SQ[i] / NN[i] - mu * mu, 0.0))
                S[i] = np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)
            FS[(cad, pan.name)] = S
            FSUM[(cad, pan.name)] = SU
            FSQ[(cad, pan.name)] = SQ
            FN[(cad, pan.name)] = NN
            FOL[(cad, pan.name)] = fl

    def stitched_sharpe_from(cad, p, idxs):
        """Exact Sharpe of the concatenated fold returns, from per-fold aggregates."""
        SU, SQ, NN = FSUM[(cad, p)], FSQ[(cad, p)], FN[(cad, p)]
        rows = np.arange(len(idxs))
        tot = SU[rows, idxs].sum()
        totq = SQ[rows, idxs].sum()
        n = NN.sum()
        mu = tot / n
        sd = np.sqrt(max(totq / n - mu * mu, 0.0))
        return float(mu * np.sqrt(252) / sd) if sd > 0 else np.nan

    # gate: aggregate identity == direct
    cad0, p0 = "QUARTER", panels[0].name
    ii = np.array([ANCHOR_I] * len(FOL[(cad0, p0)]))
    direct = sharpe(np.concatenate([RM[p0][o0:o1, ANCHOR_I] for (_, o0, o1) in FOL[(cad0, p0)]]))
    g7 = abs(stitched_sharpe_from(cad0, p0, ii) - direct)
    GATES.append(dict(gate="G7 stitched Sharpe from per-fold aggregates == direct Sharpe",
                      value=g7, target=1e-12, pass_=bool(g7 < 1e-12)))

    def _m(v):
        v = [x for x in v if np.isfinite(x)]
        return float(np.mean(v)) if v else np.nan

    rng = np.random.default_rng(NULL_SEED)
    AEQ = np.array(sorted(ANCHOR_EQ))
    drows = []
    for cad in CADENCES:
        for sname in SETS:
            for L in WINDOWS:
                w = wname(L)
                # paired fold deltas pooled over panels, clustered on folds
                for ch in CHOOSERS:
                    dels, ms, mvr, nfold = [], [], [], 0
                    per_panel = {}
                    for pan in panels:
                        key = (cad, pan.name, sname, w, ch)
                        akey = (cad, pan.name, sname, w, "CH_ANCHOR")
                        idxs = np.array([b for (_, _, _, b) in picks[key]])
                        aidx = np.array([b for (_, _, _, b) in picks[akey]])
                        S = FS[(cad, pan.name)]
                        rows = np.arange(len(idxs))
                        so = S[rows, idxs]
                        sa = S[rows, aidx]
                        dels.append(so - sa)
                        ms.append(so)
                        mvr.append(~np.isin(idxs, AEQ))
                        nfold = max(nfold, len(idxs))
                        per_panel[pan.name] = (idxs, so, sa)
                    d = np.concatenate(dels)
                    sall = np.concatenate(ms)
                    mall = np.concatenate(mvr)
                    # cluster on fold position (the folds tile the tape; panels share the tape)
                    maxf = max(len(x) for x in dels)
                    byf = np.full((len(dels), maxf), np.nan)
                    for i, x in enumerate(dels):
                        byf[i, -len(x):] = x
                    fm = np.nanmean(byf, axis=0)
                    fm = fm[np.isfinite(fm)]
                    se = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                    t = (np.nanmean(d) / se) if (se and se > 0) else 0.0
                    # stitched Sharpe of the chooser, pooled per panel
                    st = {pn: stitched_sharpe_from(cad, pn, per_panel[pn][0]) for pn in per_panel}
                    sta = {pn: stitched_sharpe_from(
                        cad, pn, np.array([b for (_, _, _, b) in
                                           picks[(cad, pn, sname, w, "CH_ANCHOR")]]))
                        for pn in per_panel}
                    # ---- nulls, per panel then pooled
                    p_count, p_perm = [], []
                    for pn in per_panel:
                        idxs, so, sa = per_panel[pn]
                        F = len(idxs)
                        m = int((~np.isin(idxs, AEQ)).sum())
                        S = FS[(cad, pn)]
                        obs = float(np.nanmean(so - sa))
                        if m == 0:
                            p_count.append(np.nan)
                            p_perm.append(np.nan)
                            continue
                        base = S[np.arange(F), np.full(F, ANCHOR_I)]
                        dests = idxs[~np.isin(idxs, AEQ)]
                        # NL_COUNT
                        pos = np.argsort(rng.random((NULL_REPS, F)), axis=1)[:, :m]
                        dd = rng.choice(NONANCHOR, size=(NULL_REPS, m))
                        draw = np.tile(base, (NULL_REPS, 1))
                        draw[np.arange(NULL_REPS)[:, None], pos] = S[pos, dd]
                        st_null = np.nanmean(draw - base[None, :], axis=1)
                        p_count.append(float((st_null >= obs).mean()))
                        # NL_PERM: same destinations, random timing
                        perm = rng.permuted(np.tile(dests, (NULL_REPS, 1)), axis=1)
                        draw2 = np.tile(base, (NULL_REPS, 1))
                        draw2[np.arange(NULL_REPS)[:, None], pos] = S[pos, perm]
                        st_null2 = np.nanmean(draw2 - base[None, :], axis=1)
                        p_perm.append(float((st_null2 >= obs).mean()))
                    drows.append(dict(cadence=cad, SET=sname, window=w, chooser=ch,
                                      npicks=len(d), move_rate=float(mall.mean()),
                                      mean_OOS_Sharpe=float(np.nanmean(sall)),
                                      delta_vs_ANCHOR=float(np.nanmean(d)), SE=se, t=t,
                                      p_NL_COUNT=_m(p_count), p_NL_PERM=_m(p_perm),
                                      **{f"stitch_{pn}": st[pn] for pn in st},
                                      **{f"stitchA_{pn}": sta[pn] for pn in sta}))
    ddf = pd.DataFrame(drows)
    ddf.to_csv(f"{OUT}.deltas.csv", index=False)

    say("")
    say("  (B1) EVERY GRID POINT AT THE PRIMARY CADENCE (QUARTER).  Paired vs CH_ANCHOR, SE")
    say("       clustered on folds; p is the one-sided fraction of matched null draws at or")
    say("       above the observed gain (2,000 reps each, averaged over the three panels).")
    for sname in SETS:
        say("")
        say(f"       SET = {sname}")
        say("       window  chooser       npick  move   meanOOS   delta      SE       t     "
            "p_COUNT  p_PERM")
        for L in WINDOWS:
            for ch in CHOOSERS:
                r = ddf[(ddf.cadence == "QUARTER") & (ddf.SET == sname)
                        & (ddf.window == wname(L)) & (ddf.chooser == ch)].iloc[0]
                say(f"       {wname(L):7s} {ch:12s} {int(r.npicks):5d}  {r.move_rate:.3f}  "
                    f"{r.mean_OOS_Sharpe:7.4f}  {r.delta_vs_ANCHOR:+8.4f}  {r.SE:.4f} "
                    f"{r.t:+6.2f}   {r.p_NL_COUNT:.3f}   {r.p_NL_PERM:.3f}")

    say("")
    say("  (B2) THE SAME GRID AT YEAR FOLDS (1223's cadence), for continuity:")
    say("       window  chooser       npick  move   meanOOS   delta      SE       t")
    for L in WINDOWS:
        for ch in CHOOSERS:
            r = ddf[(ddf.cadence == "YEAR") & (ddf.SET == "ALL4")
                    & (ddf.window == wname(L)) & (ddf.chooser == ch)].iloc[0]
            say(f"       {wname(L):7s} {ch:12s} {int(r.npicks):5d}  {r.move_rate:.3f}  "
                f"{r.mean_OOS_Sharpe:7.4f}  {r.delta_vs_ANCHOR:+8.4f}  {r.SE:.4f} {r.t:+6.2f}")

    # ------------------------------------------------------------------ ARM C: capital
    say("")
    say("=" * 108)
    say("ARM C — THE CAPITAL LEG.  STITCHED CURVES, RULE 8, BOTH KEEP PATHS")
    say("=" * 108)

    say("")
    say("  BENCHMARKS over each panel's FOLD SPAN (10 bps, t+1), QUARTER cadence:")
    BM = {}
    for pan in panels:
        fl = folds[("QUARTER", pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[a0:a1]
            h1, h2 = halves(full)
            o = r[max(a0, ioos):a1]
            oh1, oh2 = halves(o)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2, OOS_CAGR=cagr(o),
                                      OOS_Sharpe=sharpe(o), OOS_MaxDD=mdd(o), OH1=oh1, OH2=oh2)
            d = BM[(pan.name, nm)]
            say(f"    {pan.name:6s} {nm:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def bm_of(p, nm, oos=False):
        d = BM[(p, nm)]
        if not oos:
            return dict(H1=d["H1"], H2=d["H2"], CAGR=d["CAGR"], MaxDD=d["MaxDD"])
        return dict(H1=d["OH1"], H2=d["OH2"], CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    say("")
    say("  BOTH KEEP PATHS ON EVERY RUNG BOOK (nothing selected on):")
    brows = []
    for pan in panels:
        fl = folds[("QUARTER", pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        for k, i in BIDX.items():
            r = RM[pan.name][a0:a1, i]
            k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"), bm_of(pan.name, "LIVE"))
            ro = RM[pan.name][ioos:a1, i]
            _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                           bm_of(pan.name, "LIVE", True))
            brows.append(dict(panel=pan.name, ladder=k[0], rung=k[1], **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    bdf = pd.DataFrame(brows).drop_duplicates(subset=["panel", "ladder", "rung"])
    bdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bdf)} rung books: 4a {int(bdf.KEEP_4a.sum())}; 4b full "
        f"{int(bdf.KEEP_4b.sum())}; 4b OOS {int(bdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bdf.KEEP_4b & bdf.KEEP_4b_OOS).sum())}")

    say("")
    say("  (C1) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows = []
    stitch_len_err = 0.0
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            a0, a1 = fl[0][1], fl[-1][2]
            ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
            for sname in SETS:
                for L in WINDOWS:
                    for ch in CHOOSERS:
                        pk = picks[(cad, pan.name, sname, wname(L), ch)]
                        r = np.concatenate([RM[pan.name][o0:o1, b] for (_, o0, o1, b) in pk])
                        ro = np.concatenate([RM[pan.name][max(o0, ioos):o1, b]
                                             for (_, o0, o1, b) in pk if o1 > ioos])
                        stitch_len_err = max(stitch_len_err,
                                             abs(len(r) - sum(o1 - o0 for (_, o0, o1, _) in pk)))
                        k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"),
                                                         bm_of(pan.name, "LIVE"))
                        _, k4bo, mo, oh1, oh2 = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                                           bm_of(pan.name, "LIVE", True))
                        srows.append(dict(cadence=cad, panel=pan.name, SET=sname, window=wname(L),
                                          chooser=ch, ndays=len(r), **m, H1=h1, H2=h2,
                                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                          OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                          KEEP_4b_OOS=k4bo))
    sdf = pd.DataFrame(srows)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G6 each stitched curve's length == the sum of its folds'",
                      value=stitch_len_err, target=0.0, pass_=bool(stitch_len_err == 0)))
    say(f"    {len(sdf)} stitched curves: 4a {int(sdf.KEEP_4a.sum())}; 4b full "
        f"{int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((sdf.KEEP_4b & sdf.KEEP_4b_OOS).sum())}")
    say("")
    say("    STITCHED OOS SHARPE AT QUARTER / ALL4, BY PANEL (anchor row is the do-nothing book):")
    say("    window  chooser        U56      B136     SMALL")
    for L in WINDOWS:
        for ch in CHOOSERS:
            v = []
            for pn in ("U56", "B136", "SMALL"):
                q = sdf[(sdf.cadence == "QUARTER") & (sdf.SET == "ALL4") & (sdf.panel == pn)
                        & (sdf.window == wname(L)) & (sdf.chooser == ch)].iloc[0]
                v.append(q.OOS_Sharpe)
            say(f"    {wname(L):7s} {ch:12s} " + "  ".join(f"{x:8.4f}" for x in v))

    say("")
    say("  (C2) RULE 8 — the split PROTOCOL names.  The TWO DIALS (headline form, IS window) are")
    say("       chosen on the IS folds (those closing before 2017-01-01) ONLY, on mean fold OOS")
    say("       Sharpe; the 2017-2026 folds are then read ONCE.  Set frozen at ALL4.")
    wrows = []
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
            isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
            oof = [i for i, (_, o0, o1) in enumerate(fl) if o0 >= ioos]
            S = FS[(cad, pan.name)]
            best, bestv = None, -np.inf
            for L in WINDOWS:
                for ch in CHOOSERS:
                    idxs = np.array([b for (_, _, _, b) in
                                     picks[(cad, pan.name, "ALL4", wname(L), ch)]])
                    v = float(np.nanmean(S[isf, idxs[isf]])) if isf else np.nan
                    if np.isfinite(v) and v > bestv:
                        bestv, best = v, (L, ch)
            a0 = fl[oof[0]][1]
            a1 = fl[-1][2]
            spy_o, liv_o = bm_of(pan.name, "SPY", True), bm_of(pan.name, "LIVE", True)
            for L in WINDOWS:
                for ch in CHOOSERS:
                    pk = picks[(cad, pan.name, "ALL4", wname(L), ch)]
                    ro = np.concatenate([RM[pan.name][o0:o1, b]
                                         for i, (_, o0, o1, b) in enumerate(pk) if i in oof])
                    k4a, k4b, m, h1, h2 = keep_paths(ro, spy_o, liv_o)
                    wrows.append(dict(cadence=cad, panel=pan.name, window=wname(L), chooser=ch,
                                      IS_mean_fold_Sharpe=float(np.nanmean(
                                          S[isf, np.array([b for (_, _, _, b) in pk])[isf]]))
                                      if isf else np.nan,
                                      chosen_IS=bool((L, ch) == best), **m, H1=h1, H2=h2,
                                      KEEP_4a=k4a, KEEP_4b=k4b,
                                      moves=int(sum(1 for i, (_, _, _, b) in enumerate(pk)
                                                    if i in oof and b not in ANCHOR_EQ))))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       panel  IS-chosen (window, form)   OOS CAGR / Sharpe / MaxDD   halves      "
        "moves  4a 4b")
    for cad in ["QUARTER", "YEAR"]:
        say(f"       --- {cad} folds ---")
        for pan in panels:
            q = wdf[(wdf.cadence == cad) & (wdf.panel == pan.name) & wdf.chosen_IS].iloc[0]
            a = wdf[(wdf.cadence == cad) & (wdf.panel == pan.name)
                    & (wdf.chooser == "CH_ANCHOR") & (wdf.window == "EXPAND")].iloc[0]
            say(f"       {pan.name:6s} {q.window:7s} {q.chooser:12s}  {q.CAGR:7.2%} / "
                f"{q.Sharpe:.4f} / {q.MaxDD:8.2%}  {q.H1:.4f}/{q.H2:.4f}  {int(q.moves):4d}"
                f"   {'T' if q.KEEP_4a else 'F'}  {'T' if q.KEEP_4b else 'F'}")
            say(f"       {'':6s} ANCHOR (do nothing)    {a.CAGR:7.2%} / "
                f"{a.Sharpe:.4f} / {a.MaxDD:8.2%}  {a.H1:.4f}/{a.H2:.4f}  {int(a.moves):4d}"
                f"   {'T' if a.KEEP_4a else 'F'}  {'T' if a.KEEP_4b else 'F'}")
            d = BM[(pan.name, "SPY")]
            say(f"       {'':6s} SPY                    {d['OOS_CAGR']:7.2%} / "
                f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
            d = BM[(pan.name, "LIVE")]
            say(f"       {'':6s} LIVE RULES v2          {d['OOS_CAGR']:7.2%} / "
                f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    q = ddf[(ddf.cadence == "QUARTER") & (ddf.SET == "ALL4") & (ddf.chooser.isin(HFORMS))]
    winners = q[(q.delta_vs_ANCHOR > 0) & (q.t >= 2.0) & (q.p_NL_COUNT <= 0.05)
                & (q.p_NL_PERM <= 0.05)]
    naive = q[q.delta_vs_ANCHOR > 0]
    say(f"  At ALL4 / QUARTER, {len(naive)} of {len(q)} (form, window) cells post a POSITIVE raw")
    say(f"  gain over holding; {len(winners)} of {len(q)} survive |t| >= 2 AND both matched nulls.")
    ru = ddf[(ddf.cadence == "QUARTER") & (ddf.SET == "ALL4") & (ddf.chooser == "H_RUNNERUP")]
    say(f"  H_RUNNERUP specifically: mean delta over {len(ru)} windows "
        f"{ru.delta_vs_ANCHOR.mean():+.4f}, best window {ru.loc[ru.delta_vs_ANCHOR.idxmax()].window}"
        f" at {ru.delta_vs_ANCHOR.max():+.4f} (t {ru.loc[ru.delta_vs_ANCHOR.idxmax()].t:+.2f}), "
        f"move rate {ru.move_rate.mean():.3f}.")
    outcome = "(A) REPLACE" if len(winners) else ("(B) NO STANDING FORM BEATS HOLDING"
                                                 if not len(naive) else "(C) PARTIAL")
    say(f"  PRE-DECLARED OUTCOME: {outcome}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"  GATES {int(gdf.pass_.sum())} of {len(gdf)}:")
    for _, g in gdf.iterrows():
        say(f"    [{'PASS' if g.pass_ else 'FAIL'}] {g.gate}  value={g.value:.3e} "
            f"target={g.target:.3e}")
    say("")
    say(f"  Runtime {time.time()-t0:.0f}s, offline, deterministic.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
