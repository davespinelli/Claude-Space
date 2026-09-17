#!/usr/bin/env python3
"""
Idea 1229 (cloud lane, 2026-09-17) — at what IS WINDOW LENGTH does a HEADLINE FORM separate
from its own NL_PERM band?

THE PREMISE, READ FROM THE RECORD.  Idea 1227 (lane C) ran the three headline forms across six
IS windows on 193 picks and found every form's SIGN flips with the window (H_RUNNERUP +0.0126
at L252, -0.0115 at EXPAND) and that no cell clears both matched nulls.  1227 read that as "no
form beats holding".  There is a second reading it did not price: the forms barely ever move,
so the NL_PERM band around each delta may simply be wider than any delta the form can produce.
If that is the case the record has not measured a zero — it has measured NOTHING, and the
honest report is a REQUIRED PRECISION, not a verdict.

THIS RUN PUTS THE REQUIRED-PRECISION CALCULATION ON IT.

  For every (headline form, IS window, fold cadence) cell: the observed mean per-fold delta
  against CH_ANCHOR, that cell's OWN NL_PERM band (the chooser's own destination multiset
  re-dealt to random folds), and then the question the queue asks —

      is there an IS window at which the delta clears the band at alpha = 0.05, and if not,
      how much TAPE would it take, and is that tape ATTAINABLE?

  Extrapolation is not assumed.  The band's width is MEASURED at three fold counts on the same
  tape (a subsample ladder) and its shrink exponent is FITTED, so the tape requirement rests on
  this record's own scaling and not on a textbook 1/sqrt(F).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  WINDOW LADDER   L in {252, 504, 756, 1260, 2520, EXPANDING} trading days, rolling, ending the
                  trading day before the fold opens.
  FOLD CADENCE    {MONTH, QUARTER, YEAR}.  This dial is not decoration: MONTH and YEAR read the
                  SAME TAPE at 12x different fold counts, so the cadence rungs are a direct test
                  of whether more folds on a fixed tape buy any precision at all.

  18 (window, cadence) grid points, EVERY ONE PUBLISHED, at each of 3 headline forms + 2
  controls and 2 comparison sets.

NOT DIALS, REPORTED AT EVERY VALUE AND NEVER SELECTED ON: PANEL {U56, B136, SMALL} (rule 9);
COMPARISON SET {ALL4, NG} — the verdict is read off ALL4, the record's own standing set, with
NG (1214's degenerate-free set) carried as a declared sensitivity; HEADLINE FORM {H_RUNNERUP,
H_NARROWEST, H_ANY} plus controls CH_RAW and CH_ANCHOR, all five reported at every cell.

PRE-DECLARED, FIXED BEFORE ANY PRICE IS READ:
  ATTAINABLE TAPE = 50 years of daily US large-cap closes.  (The record's own tape is 17.7
  years; 50 years is the practical ceiling for a panel built this way.)  A required tape longer
  than 50 years is reported as NOT ATTAINABLE, which is a finding about the QUESTION, not about
  the form.
  SEPARATION = the observed mean per-fold delta exceeds its own NL_PERM band's one-sided 95th
  percentile.  L* = the SHORTEST window at which a form separates at the primary cadence.

Frozen at the record's construction, inherited from 1207/1214/1223/1227 unchanged: 3-leg
composite (21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 /
GROSS=0.75 / CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up
260 rows, the conditional two-sided null band and its Monte-Carlo construction (seed 12141214),
and 1227's value-based (not key-based) definition of a MOVE.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with BOTH dials chosen on the IS
folds ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
rung book, every stitched chooser curve and every rule-8 row; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_at-what-IS-WINDOW-LENGTH-does-a-HEADLINE-FORM-SEPARATE-FROM-ITS-OWN-NL_PERM-BAND_cloud.py
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
SLUG = "at-what-IS-WINDOW-LENGTH-does-a-HEADLINE-FORM-SEPARATE-FROM-ITS-OWN-NL_PERM-BAND"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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

HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
CHOOSERS = HFORMS + ["CH_RAW", "CH_ANCHOR"]

# ---- DIAL 1: IS window length, trading days; None = EXPANDING (1223's / 1227's window)
WINDOWS = [252, 504, 756, 1260, 2520, None]


def wname(L):
    return "EXPAND" if L is None else f"L{L}"


# ---- DIAL 2: fold cadence.  MIN_FOLD is the shortest OOS block that still gives a Sharpe.
CADENCES = ["MONTH", "QUARTER", "YEAR"]
MIN_FOLD = {"MONTH": 15, "QUARTER": 40, "YEAR": 200}
FOLDS_PER_YEAR = {"MONTH": 12.0, "QUARTER": 4.0, "YEAR": 1.0}
PRIMARY_CAD = "QUARTER"          # 1227's primary; MONTH and YEAR bracket it

# ---- not dials
NG4 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = {"ALL4": ALL4, "NG": NG4}
BAR = "B_IID95"
MIN_IS = 252

NMC = 1_500_000
MC_SEED = 12141214
NULL_REPS, NULL_SEED = 4000, 12291229
SUB_FRACS = [0.25, 0.50, 1.00]   # measured shrink ladder for the band width
SUB_DRAWS = 40                   # independent fold subsamples per fraction
ATTAINABLE_YEARS = 50.0          # PRE-DECLARED
LIVE_MAXDD_COMMITTED = -0.1205

D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

# 1227's committed (window, form) mean deltas at QUARTER / ALL4, for the replication gate G8.
REP1227 = {("L252", "H_RUNNERUP"): +0.0126, ("EXPAND", "H_RUNNERUP"): -0.0115}

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
    V = (M / I) if I > 0 else np.inf
    return "W" if V > band["U95"] else ("N" if V < band["L95"] else "TIE")


# ==================================================================== panels / runner (1207/1214)
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


def build1(pan, N, H, freq, lag=1):
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
    say("IDEA 1229 (cloud lane, 2026-09-17) — at what IS WINDOW LENGTH does a HEADLINE FORM")
    say("SEPARATE FROM ITS OWN NL_PERM BAND?  A REQUIRED-PRECISION CALCULATION.")
    say("=" * 108)
    say("")
    say(f"  DIAL 1 WINDOW LADDER  {[wname(L) for L in WINDOWS]}")
    say(f"  DIAL 2 FOLD CADENCE   {CADENCES}   (primary {PRIMARY_CAD})")
    say("  Headline forms (NOT a dial, all reported): H_RUNNERUP / H_NARROWEST / H_ANY")
    say("    + controls CH_RAW (raw-widest ladder's argmax) and CH_ANCHOR (do nothing).")
    say("  Comparison set (NOT a dial, both reported, verdict read off ALL4): ALL4, NG")
    say(f"  Bar frozen at {BAR}; null frozen at NL_PERM (own destinations, random timing).")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed before any price is read:")
    say("    (A) SEPARABLE NOW — some form clears its own NL_PERM 95th percentile at some")
    say("        window at the primary cadence.  Report L*.")
    say("    (B) SEPARABLE ON AN ATTAINABLE TAPE — no cell separates now, but the fitted band")
    say(f"        shrink puts required tape <= {ATTAINABLE_YEARS:.0f} years for some form.")
    say("    (C) NOT SEPARABLE ON ANY ATTAINABLE TAPE — required tape exceeds")
    say(f"        {ATTAINABLE_YEARS:.0f} years, or the gap is <= 0 so no tape length helps.")
    say("        (C) means the record's committed form comparisons are UNMEASURED, not zero.")

    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    unb = max(abs(rdraw(k).mean() / d2(k) - 1.0) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G1 R_k/d2(k) unbiased for sigma under the iid null", value=unb,
                      target=5e-3, pass_=bool(unb < 5e-3)))

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
    tape_years = (pxU.index[-1] - pxU.index[WARMUP]).days / 365.25
    say(f"  THE RECORD'S OWN TAPE after warm-up: {tape_years:.1f} years "
        f"({pxU.index[WARMUP].date()} to {pxU.index[-1].date()}).")

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
        say(f"    {pan.name}: {len(books)} rung books over 4 ladders "
            f"(N {len(LAD['N'])}, H {len(LAD['H'])}, GROSS {len(LAD['GROSS'])}, CADENCE 2).")

    ident = 0.0
    for pan in panels:
        bk = booked[pan.name]
        for k in (("N", A_N), ("H", A_H), ("GROSS", A_G)):
            ident = max(ident, float(np.nanmax(np.abs(bk[k] - bk[ANCHOR_KEY]))))
    GATES.append(dict(gate="G9 the anchor is one book under four names", value=ident,
                      target=1e-15, pass_=bool(ident <= 1e-15)))

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

    RM = {p: np.column_stack([booked[p][k] for k in BOOKKEY]) for p in booked}
    BIDX = {k: i for i, k in enumerate(BOOKKEY)}
    LADIDX = {lad: [BIDX[(lad, r)] for r in LAD[lad]] for lad in LAD}
    ANCHOR_I = BIDX[ANCHOR_KEY]
    ANCHOR_EQ = set()
    for i in range(len(BOOKKEY)):
        if all(float(np.nanmax(np.abs(RM[p][:, i] - RM[p][:, ANCHOR_I]))) == 0.0 for p in RM):
            ANCHOR_EQ.add(i)
    NONANCHOR = np.array([i for i in range(len(BOOKKEY)) if i not in ANCHOR_EQ])
    GATES.append(dict(gate="G10 the anchor-equivalent key set is exactly {N=20, H=126, "
                           "GROSS=0.75, CADENCE=W} (1227's correction)",
                      value=float(len(ANCHOR_EQ)), target=4.0,
                      pass_=bool(sorted(BOOKKEY[i] for i in ANCHOR_EQ)
                                 == sorted([("N", A_N), ("H", A_H), ("GROSS", A_G), ANCHOR_KEY]))))
    say(f"    ANCHOR-EQUIVALENT BOOKS (by value): {sorted(BOOKKEY[i] for i in ANCHOR_EQ)}; the "
        f"null's destination pool is the remaining {len(NONANCHOR)} books.")

    # ------------------------------------------------------------------ folds
    say("")
    say("  FOLDS.  One fold = one calendar MONTH / QUARTER / YEAR, out of sample; the IS window")
    say("  ends the trading day BEFORE the fold opens.  MONTH and YEAR read the SAME TAPE.")
    folds = {}
    for cad in CADENCES:
        for pan in panels:
            if cad == "MONTH":
                keyv = pan.idx.year.values * 100 + pan.idx.month.values
            elif cad == "QUARTER":
                keyv = pan.idx.year.values * 10 + pan.idx.quarter.values
            else:
                keyv = pan.idx.year.values
            out, cover = [], []
            for v in sorted(set(keyv.tolist())):
                oo = np.flatnonzero(keyv == v)
                oo = oo[oo >= pan.i0 + MIN_IS]
                if len(oo) < MIN_FOLD[cad]:
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
            + "  ".join(f"{p.name} {len(folds[(cad,p.name)])}" for p in panels))

    pan_i0 = {p.name: p.i0 for p in panels}

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

    _PK: dict = {}

    def pick_of(p, lad, lo, hi):
        key = (p, lad, lo, hi)
        if key in _PK:
            return _PK[key]
        v = [(sharpe(RM[p][lo:hi, i]), i) for i in LADIDX[lad]]
        v = [(s, i) for s, i in v if np.isfinite(s)]
        r = max(v)[1] if v else ANCHOR_I
        _PK[key] = r
        return r

    def headline(p, lo, hi, lads):
        sp = {lad: spread_of(p, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        if len(good) < 2:
            return {hf: None for hf in HFORMS} | {"_widest": None}
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
                if a == b or not (np.isfinite(sp.get(a, np.nan))
                                  and np.isfinite(sp.get(b, np.nan))):
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

    # ------------------------------------------------------------------ the walk
    say("")
    say("  THE WALK.  Every (cadence, panel, fold, set, window) cell evaluated for all five")
    say("  choosers; nothing is selected on.")
    prows = []
    picks: dict = {}
    for cad in CADENCES:
        for pan in panels:
            for (v, o0, o1) in folds[(cad, pan.name)]:
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
                                              moved=bool(bi not in ANCHOR_EQ),
                                              OOS_Sharpe=sharpe(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv = float(pdf[pdf.chooser == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G5 CH_ANCHOR move rate == 0", value=mv, target=0.0,
                      pass_=bool(mv == 0.0)))
    say(f"    {len(pdf):,} pick-cells over {len(CADENCES)} cadences x {len(SETS)} sets x "
        f"{len(WINDOWS)} windows x {len(CHOOSERS)} choosers.")

    # per (cadence, panel) fold Sharpe matrix
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
        SU, SQ, NN = FSUM[(cad, p)], FSQ[(cad, p)], FN[(cad, p)]
        rows = np.arange(len(idxs))
        tot = SU[rows, idxs].sum()
        totq = SQ[rows, idxs].sum()
        n = NN.sum()
        mu = tot / n
        sd = np.sqrt(max(totq / n - mu * mu, 0.0))
        return float(mu * np.sqrt(252) / sd) if sd > 0 else np.nan

    p0 = panels[0].name
    ii = np.array([ANCHOR_I] * len(FOL[(PRIMARY_CAD, p0)]))
    direct = sharpe(np.concatenate([RM[p0][o0:o1, ANCHOR_I]
                                    for (_, o0, o1) in FOL[(PRIMARY_CAD, p0)]]))
    g7 = abs(stitched_sharpe_from(PRIMARY_CAD, p0, ii) - direct)
    GATES.append(dict(gate="G7 stitched Sharpe from per-fold aggregates == direct Sharpe",
                      value=g7, target=1e-12, pass_=bool(g7 < 1e-12)))

    # ================================================================ ARM B: the NL_PERM bands
    say("")
    say("=" * 108)
    say("ARM B — THE OBSERVED DELTA AND ITS OWN NL_PERM BAND AT EVERY GRID POINT")
    say("=" * 108)
    say("")
    say("  NL_PERM: the chooser's OWN destination multiset re-dealt to randomly chosen folds.")
    say(f"  Count and destinations matched; only TIMING is random.  {NULL_REPS:,} reps, seed")
    say(f"  {NULL_SEED}.  The band is the null's distribution of the MEAN per-fold delta.")

    AEQ = np.array(sorted(ANCHOR_EQ))
    rng = np.random.default_rng(NULL_SEED)

    def nl_perm(cad, pn, idxs, nreps=NULL_REPS, sub=None):
        """Null distribution of the MEAN per-fold delta under random timing.
        sub = optional array of fold positions to restrict to (the subsample ladder)."""
        S = FS[(cad, pn)]
        F_all = len(idxs)
        rowsel = np.arange(F_all) if sub is None else np.asarray(sub)
        F = len(rowsel)
        base = S[rowsel, np.full(F, ANCHOR_I)]
        sel = idxs[rowsel]
        moved = ~np.isin(sel, AEQ)
        m = int(moved.sum())
        obs = float(np.nanmean(S[rowsel, sel] - base))
        if m == 0 or F < 4:
            return dict(obs=obs, m=m, F=F, null_mean=np.nan, null_sd=np.nan, q95=np.nan,
                        p=np.nan)
        dests = sel[moved]
        pos = np.argsort(rng.random((nreps, F)), axis=1)[:, :m]
        perm = rng.permuted(np.tile(dests, (nreps, 1)), axis=1)
        draw = np.tile(base, (nreps, 1))
        rr = rowsel[pos]
        draw[np.arange(nreps)[:, None], pos] = S[rr, perm]
        st = np.nanmean(draw - base[None, :], axis=1)
        return dict(obs=obs, m=m, F=F, null_mean=float(np.nanmean(st)),
                    null_sd=float(np.nanstd(st, ddof=1)),
                    q95=float(np.nanquantile(st, 0.95)),
                    p=float(np.nanmean(st >= obs)))

    brows = []
    for cad in CADENCES:
        for sname in SETS:
            for L in WINDOWS:
                w = wname(L)
                for ch in CHOOSERS:
                    per = {}
                    for pan in panels:
                        idxs = np.array([b for (_, _, _, b) in
                                         picks[(cad, pan.name, sname, w, ch)]])
                        per[pan.name] = nl_perm(cad, pan.name, idxs)
                    obs = float(np.nanmean([per[p]["obs"] for p in per]))
                    nm = float(np.nanmean([per[p]["null_mean"] for p in per]))
                    q95 = float(np.nanmean([per[p]["q95"] for p in per]))
                    sd = float(np.nanmean([per[p]["null_sd"] for p in per]))
                    pv = float(np.nanmean([per[p]["p"] for p in per]))
                    mrate = float(np.nanmean([per[p]["m"] / max(per[p]["F"], 1) for p in per]))
                    brows.append(dict(
                        cadence=cad, SET=sname, window=w, chooser=ch,
                        F=int(np.sum([per[p]["F"] for p in per])),
                        moves=int(np.sum([per[p]["m"] for p in per])), move_rate=mrate,
                        obs_delta=obs, null_mean=nm, null_sd=sd, q95=q95, p_NL_PERM=pv,
                        gap=obs - nm, half_width=q95 - nm,
                        separates=bool(np.isfinite(pv) and pv <= 0.05),
                        **{f"obs_{p}": per[p]["obs"] for p in per},
                        **{f"p_{p}": per[p]["p"] for p in per}))
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.bands.csv", index=False)

    for cad in CADENCES:
        say("")
        say(f"  (B1) CADENCE = {cad}, SET = ALL4.  All {len(WINDOWS)} windows x "
            f"{len(CHOOSERS)} choosers.")
        say("       window  chooser       F   moves  mrate   obs_delta   null_mu   band_q95"
            "   halfwid   p_PERM  sep")
        for L in WINDOWS:
            for ch in CHOOSERS:
                r = bdf[(bdf.cadence == cad) & (bdf.SET == "ALL4")
                        & (bdf.window == wname(L)) & (bdf.chooser == ch)].iloc[0]
                say(f"       {r.window:7s} {r.chooser:12s} {int(r.F):4d} {int(r.moves):5d}  "
                    f"{r.move_rate:.3f}  {r.obs_delta:+9.4f}  {r.null_mean:+8.4f}  "
                    f"{r.q95:+8.4f}  {r.half_width:8.4f}   {r.p_NL_PERM:.3f}  "
                    f"{'YES' if r.separates else '.'}")

    say("")
    say("  (B2) SET = NG (1214's degenerate-free comparison set), primary cadence, sensitivity:")
    say("       window  chooser       obs_delta   band_q95   p_PERM  sep")
    for L in WINDOWS:
        for ch in CHOOSERS:
            r = bdf[(bdf.cadence == PRIMARY_CAD) & (bdf.SET == "NG")
                    & (bdf.window == wname(L)) & (bdf.chooser == ch)].iloc[0]
            say(f"       {r.window:7s} {r.chooser:12s}  {r.obs_delta:+9.4f}  {r.q95:+8.4f}"
                f"   {r.p_NL_PERM:.3f}  {'YES' if r.separates else '.'}")

    # G8 replication of 1227 at QUARTER / ALL4
    rep_err = 0.0
    for (w, ch), v27 in REP1227.items():
        s = bdf[(bdf.cadence == "QUARTER") & (bdf.SET == "ALL4") & (bdf.window == w)
                & (bdf.chooser == ch)]
        if len(s):
            rep_err = max(rep_err, abs(float(s.iloc[0].obs_delta) - v27))
    GATES.append(dict(gate="G8 (QUARTER, ALL4) reproduces 1227's committed (window, form) "
                           "deltas", value=rep_err, target=3e-2, pass_=bool(rep_err < 3e-2)))
    say("")
    say(f"    G8 replication of 1227's committed deltas: worst deviation {rep_err:.4f} over "
        f"{len(REP1227)} numbers.")

    # ================================================================ ARM C: required precision
    say("")
    say("=" * 108)
    say("ARM C — THE REQUIRED PRECISION.  HOW MUCH TAPE WOULD SEPARATION TAKE?")
    say("=" * 108)
    say("")
    say("  Step 1 MEASURE the band's shrink.  For each cell the NL_PERM band is rebuilt on")
    say(f"  random fold SUBSAMPLES at fractions {SUB_FRACS} ({SUB_DRAWS} draws each) and the")
    say("  half-width's exponent b in halfwidth ~ F^-b is FITTED by OLS on log F.  Textbook")
    say("  iid would give b = 0.5; the fitted b is what this record's folds actually deliver.")

    srng = np.random.default_rng(NULL_SEED + 77)
    shrows = []
    for cad in CADENCES:
        for L in WINDOWS:
            for ch in CHOOSERS:
                pts = []
                for frac in SUB_FRACS:
                    hw = []
                    for pan in panels:
                        idxs = np.array([b for (_, _, _, b) in
                                         picks[(cad, pan.name, "ALL4", wname(L), ch)]])
                        F = len(idxs)
                        k = max(int(round(frac * F)), 8)
                        if k > F:
                            k = F
                        ndr = 1 if frac >= 0.999 else SUB_DRAWS
                        for _ in range(ndr):
                            sub = np.sort(srng.choice(F, size=k, replace=False)) \
                                if frac < 0.999 else np.arange(F)
                            d = nl_perm(cad, pan.name, idxs, nreps=400, sub=sub)
                            if np.isfinite(d["q95"]) and np.isfinite(d["null_mean"]):
                                hw.append((k, d["q95"] - d["null_mean"]))
                    if hw:
                        kk = float(np.mean([x[0] for x in hw]))
                        pts.append((kk * len(panels), float(np.mean([x[1] for x in hw]))))
                if len(pts) >= 2 and all(p[1] > 0 for p in pts):
                    x = np.log(np.array([p[0] for p in pts]))
                    y = np.log(np.array([p[1] for p in pts]))
                    b = -float(np.polyfit(x, y, 1)[0])
                else:
                    b = np.nan
                shrows.append(dict(cadence=cad, window=wname(L), chooser=ch, b_fit=b,
                                   pts=";".join(f"{p[0]:.0f}:{p[1]:.4f}" for p in pts)))
    shdf = pd.DataFrame(shrows)
    shdf.to_csv(f"{OUT}.shrink.csv", index=False)
    bfit = shdf[shdf.chooser.isin(HFORMS)].b_fit
    say("")
    say(f"    FITTED SHRINK EXPONENT over {int(bfit.notna().sum())} (cadence, window, form) "
        f"cells: mean {bfit.mean():.4f}, median {bfit.median():.4f}, "
        f"range [{bfit.min():.4f}, {bfit.max():.4f}].")
    say("    (0.5 = iid-in-folds.  Below 0.5 means folds share information and extra folds buy")
    say("     less than their count suggests.)")
    say("")
    say("    BY CADENCE:")
    for cad in CADENCES:
        s = shdf[(shdf.cadence == cad) & shdf.chooser.isin(HFORMS)].b_fit
        say(f"      {cad:8s} mean b {s.mean():.4f}  median {s.median():.4f}")

    say("")
    say("  Step 2 THE SAME-TAPE TEST.  MONTH, QUARTER and YEAR read the SAME 17.7 years at 12x")
    say("  different fold counts.  If extra folds were real information the band would shrink")
    say("  by sqrt(F_month/F_year) = ~3.5x from YEAR to MONTH.  Measured, at ALL4:")
    say("       window  form           hw_YEAR   hw_QUARTER  hw_MONTH   Q/Y ratio  pred  "
        "M/Y ratio  pred")
    strows = []
    for L in WINDOWS:
        for ch in HFORMS + ["CH_RAW"]:
            g = {}
            for cad in CADENCES:
                r = bdf[(bdf.cadence == cad) & (bdf.SET == "ALL4")
                        & (bdf.window == wname(L)) & (bdf.chooser == ch)].iloc[0]
                g[cad] = (r.half_width, r.F)
            hy, fy = g["YEAR"]
            hq, fq = g["QUARTER"]
            hm, fm = g["MONTH"]
            rq = hq / hy if hy > 0 else np.nan
            rm = hm / hy if hy > 0 else np.nan
            pq = np.sqrt(fy / fq)
            pmn = np.sqrt(fy / fm)
            strows.append(dict(window=wname(L), chooser=ch, hw_YEAR=hy, hw_QUARTER=hq,
                               hw_MONTH=hm, ratio_QY=rq, pred_QY=pq, ratio_MY=rm, pred_MY=pmn))
            say(f"       {wname(L):7s} {ch:12s}  {hy:8.4f}  {hq:10.4f}  {hm:8.4f}  "
                f"{rq:9.3f}  {pq:.3f}  {rm:9.3f}  {pmn:.3f}")
    stdf = pd.DataFrame(strows)
    stdf.to_csv(f"{OUT}.sametape.csv", index=False)
    ok = stdf.dropna(subset=["ratio_MY", "pred_MY"])
    say("")
    say(f"    MEAN measured M/Y band ratio {ok.ratio_MY.mean():.3f} against the iid prediction "
        f"{ok.pred_MY.mean():.3f}; Q/Y {ok.ratio_QY.mean():.3f} against {ok.pred_QY.mean():.3f}.")

    say("")
    say("  Step 3 THE REQUIRED TAPE.  With gap G = obs - null_mean held fixed (the honest")
    say("  assumption: a form's timing skill per fold is a property of the form, not of the")
    say("  tape length) and half-width w ~ F^-b at the FITTED b, separation needs")
    say("      F* = F x (w/G)^(1/b),  tape* = F* / folds-per-year.")
    say("  G <= 0 means no tape length ever separates: the form is on the wrong side of its")
    say("  own null.")
    rrows = []
    for cad in CADENCES:
        for sname in SETS:
            for L in WINDOWS:
                for ch in CHOOSERS:
                    r = bdf[(bdf.cadence == cad) & (bdf.SET == sname)
                            & (bdf.window == wname(L)) & (bdf.chooser == ch)].iloc[0]
                    b = float(shdf[(shdf.cadence == cad) & (shdf.window == wname(L))
                                   & (shdf.chooser == ch)].iloc[0].b_fit)
                    G, w, F = r.gap, r.half_width, r.F
                    Fpan = F / len(panels)
                    if not np.isfinite(b) or b <= 0 or not np.isfinite(G) or G <= 0 \
                            or not np.isfinite(w) or w <= 0:
                        Fstar, tape = np.inf, np.inf
                    elif G >= w:
                        Fstar, tape = float(Fpan), float(Fpan / FOLDS_PER_YEAR[cad])
                    else:
                        Fstar = float(Fpan * (w / G) ** (1.0 / b))
                        tape = Fstar / FOLDS_PER_YEAR[cad]
                    rrows.append(dict(cadence=cad, SET=sname, window=wname(L), chooser=ch,
                                      F_now=int(Fpan), gap=G, half_width=w, b_fit=b,
                                      F_star=Fstar, tape_years=tape,
                                      separates_now=bool(r.separates),
                                      attainable=bool(tape <= ATTAINABLE_YEARS)))
    rdf = pd.DataFrame(rrows)
    rdf.to_csv(f"{OUT}.required.csv", index=False)

    for cad in CADENCES:
        say("")
        say(f"    (C{CADENCES.index(cad)+1}) CADENCE = {cad}, SET = ALL4:")
        say("       window  chooser          gap    halfwid   b_fit     F*        tape(yr)  "
            "sep  attainable")
        for L in WINDOWS:
            for ch in CHOOSERS:
                r = rdf[(rdf.cadence == cad) & (rdf.SET == "ALL4")
                        & (rdf.window == wname(L)) & (rdf.chooser == ch)].iloc[0]
                fs = "inf" if not np.isfinite(r.F_star) else f"{r.F_star:.0f}"
                ty = "inf" if not np.isfinite(r.tape_years) else f"{r.tape_years:.0f}"
                say(f"       {r.window:7s} {r.chooser:12s} {r.gap:+8.4f}  {r.half_width:8.4f}  "
                    f"{r.b_fit:6.3f}  {fs:>8s}  {ty:>8s}  "
                    f"{'YES' if r.separates_now else ' . '}  "
                    f"{'YES' if r.attainable else 'NO'}")

    # L*: shortest separating window per form at the primary cadence
    say("")
    say("  Step 4 L* — THE SHORTEST WINDOW AT WHICH EACH FORM SEPARATES (primary cadence,")
    say("  ALL4).  This is the number the queue asks for.")
    lstar_rows = []
    for ch in CHOOSERS:
        sep = [wname(L) for L in WINDOWS
               if bool(bdf[(bdf.cadence == PRIMARY_CAD) & (bdf.SET == "ALL4")
                           & (bdf.window == wname(L)) & (bdf.chooser == ch)].iloc[0].separates)]
        sub = rdf[(rdf.cadence == PRIMARY_CAD) & (rdf.SET == "ALL4") & (rdf.chooser == ch)]
        best = sub.loc[sub.tape_years.idxmin()] if sub.tape_years.notna().any() else None
        lstar_rows.append(dict(chooser=ch, L_star=(sep[0] if sep else "NONE"),
                               n_separating_windows=len(sep),
                               best_window=(best.window if best is not None else ""),
                               min_tape_years=(float(best.tape_years)
                                               if best is not None else np.inf)))
        ty = "inf" if (best is None or not np.isfinite(best.tape_years)) \
            else f"{best.tape_years:.0f}"
        say(f"       {ch:12s} L* = {(sep[0] if sep else 'NONE'):7s} "
            f"({len(sep)} of {len(WINDOWS)} windows separate);  cheapest window "
            f"{(best.window if best is not None else '-'):7s} needs {ty:>8s} years of tape "
            f"({'ATTAINABLE' if (best is not None and np.isfinite(best.tape_years) and best.tape_years <= ATTAINABLE_YEARS) else 'NOT ATTAINABLE'})")
    ldf = pd.DataFrame(lstar_rows)
    ldf.to_csv(f"{OUT}.lstar.csv", index=False)

    # ================================================================ ARM D: capital
    say("")
    say("=" * 108)
    say("ARM D — THE CAPITAL LEG.  BOTH KEEP PATHS, STITCHED CURVES, RULE 8")
    say("=" * 108)
    say("")
    say("  BENCHMARKS over each panel's fold span (10 bps, t+1), primary cadence:")
    BM = {}
    for pan in panels:
        fl = folds[(PRIMARY_CAD, pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm_, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[a0:a1]
            h1, h2 = halves(full)
            o = r[max(a0, ioos):a1]
            oh1, oh2 = halves(o)
            BM[(pan.name, nm_)] = dict(**triple(full), H1=h1, H2=h2, OOS_CAGR=cagr(o),
                                       OOS_Sharpe=sharpe(o), OOS_MaxDD=mdd(o), OH1=oh1, OH2=oh2)
            d = BM[(pan.name, nm_)]
            say(f"    {pan.name:6s} {nm_:5s} {d['CAGR']:7.2%} / {d['Sharpe']:.4f} / "
                f"{d['MaxDD']:8.2%}  halves {d['H1']:.4f}/{d['H2']:.4f}  "
                f"OOS {d['OOS_CAGR']:7.2%} / {d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")

    def bm_of(p, nm_, oos=False):
        d = BM[(p, nm_)]
        if not oos:
            return dict(H1=d["H1"], H2=d["H2"], CAGR=d["CAGR"], MaxDD=d["MaxDD"])
        return dict(H1=d["OH1"], H2=d["OH2"], CAGR=d["OOS_CAGR"], MaxDD=d["OOS_MaxDD"])

    krows = []
    for pan in panels:
        fl = folds[(PRIMARY_CAD, pan.name)]
        a0, a1 = fl[0][1], fl[-1][2]
        ioos = max(a0, pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        for k, i in BIDX.items():
            r = RM[pan.name][a0:a1, i]
            k4a, k4b, m, h1, h2 = keep_paths(r, bm_of(pan.name, "SPY"), bm_of(pan.name, "LIVE"))
            ro = RM[pan.name][ioos:a1, i]
            _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                           bm_of(pan.name, "LIVE", True))
            krows.append(dict(panel=pan.name, ladder=k[0], rung=k[1], **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4bo))
    kdf = pd.DataFrame(krows).drop_duplicates(subset=["panel", "ladder", "rung"])
    kdf.to_csv(f"{OUT}.books.csv", index=False)
    say("")
    say(f"    {len(kdf)} rung books: 4a {int(kdf.KEEP_4a.sum())}; 4b full "
        f"{int(kdf.KEEP_4b.sum())}; 4b OOS {int(kdf.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((kdf.KEEP_4b & kdf.KEEP_4b_OOS).sum())}")
    both = kdf[kdf.KEEP_4b & kdf.KEEP_4b_OOS]
    if len(both):
        say("    Books clearing 4b FULL and 4b OOS (panel / ladder / rung):")
        for _, q in both.sort_values("OOS_Sharpe", ascending=False).head(6).iterrows():
            say(f"      {q.panel:6s} {q.ladder:8s} {str(q.rung):6s} full {q.CAGR:7.2%} / "
                f"{q.Sharpe:.4f} / {q.MaxDD:8.2%}  halves {q.H1:.4f}/{q.H2:.4f}  "
                f"OOS {q.OOS_CAGR:7.2%} / {q.OOS_Sharpe:.4f} / {q.OOS_MaxDD:8.2%}")

    say("")
    say("  (D1) STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows2 = []
    stitch_len_err = 0.0
    for cad in CADENCES:
        for pan in panels:
            fl = folds[(cad, pan.name)]
            ioos = max(fl[0][1], pan.idx.searchsorted(pd.Timestamp(OOS_START)))
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
                        _, k4bo, mo, _, _ = keep_paths(ro, bm_of(pan.name, "SPY", True),
                                                       bm_of(pan.name, "LIVE", True))
                        srows2.append(dict(cadence=cad, panel=pan.name, SET=sname,
                                           window=wname(L), chooser=ch, ndays=len(r), **m,
                                           H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                           OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                           KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4bo))
    sdf = pd.DataFrame(srows2)
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G6 each stitched curve's length == the sum of its folds'",
                      value=stitch_len_err, target=0.0, pass_=bool(stitch_len_err == 0)))
    say(f"    {len(sdf)} stitched curves: 4a {int(sdf.KEEP_4a.sum())}; 4b full "
        f"{int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}")
    say("")
    say("    STITCHED OOS SHARPE AT THE PRIMARY CADENCE / ALL4, BY PANEL:")
    say("    window  chooser        U56      B136     SMALL")
    for L in WINDOWS:
        for ch in CHOOSERS:
            v = []
            for pn in ("U56", "B136", "SMALL"):
                q = sdf[(sdf.cadence == PRIMARY_CAD) & (sdf.SET == "ALL4") & (sdf.panel == pn)
                        & (sdf.window == wname(L)) & (sdf.chooser == ch)].iloc[0]
                v.append(q.OOS_Sharpe)
            say(f"    {wname(L):7s} {ch:12s} " + "  ".join(f"{x:8.4f}" for x in v))

    say("")
    say("  (D2) RULE 8 — BOTH DIALS (window, cadence) plus the form chosen on the IS folds")
    say("       (those closing before 2017-01-01) ONLY; 2017-2026 read ONCE.  Set = ALL4.")
    wrows = []
    for pan in panels:
        best, bestv = None, -np.inf
        for cad in CADENCES:
            fl = folds[(cad, pan.name)]
            ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
            isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
            S = FS[(cad, pan.name)]
            for L in WINDOWS:
                for ch in CHOOSERS:
                    idxs = np.array([b for (_, _, _, b) in
                                     picks[(cad, pan.name, "ALL4", wname(L), ch)]])
                    v = float(np.nanmean(S[isf, idxs[isf]])) if isf else np.nan
                    if np.isfinite(v) and v > bestv:
                        bestv, best = v, (cad, L, ch)
        for cad in CADENCES:
            fl = folds[(cad, pan.name)]
            ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
            isf = [i for i, (_, o0, o1) in enumerate(fl) if o1 <= ioos]
            oof = [i for i, (_, o0, o1) in enumerate(fl) if o0 >= ioos]
            S = FS[(cad, pan.name)]
            spy_o, liv_o = bm_of(pan.name, "SPY", True), bm_of(pan.name, "LIVE", True)
            for L in WINDOWS:
                for ch in CHOOSERS:
                    pk = picks[(cad, pan.name, "ALL4", wname(L), ch)]
                    ro = np.concatenate([RM[pan.name][o0:o1, b]
                                         for i, (_, o0, o1, b) in enumerate(pk) if i in oof])
                    k4a, k4b, m, h1, h2 = keep_paths(ro, spy_o, liv_o)
                    idxs = np.array([b for (_, _, _, b) in pk])
                    wrows.append(dict(panel=pan.name, cadence=cad, window=wname(L), chooser=ch,
                                      IS_mean_fold_Sharpe=float(np.nanmean(S[isf, idxs[isf]]))
                                      if isf else np.nan,
                                      chosen_IS=bool((cad, L, ch) == best), **m, H1=h1, H2=h2,
                                      KEEP_4a=k4a, KEEP_4b=k4b,
                                      moves=int(sum(1 for i, (_, _, _, b) in enumerate(pk)
                                                    if i in oof and b not in ANCHOR_EQ))))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       panel  IS-chosen (cadence, window, form)   OOS CAGR / Sharpe / MaxDD   halves"
        "        moves 4a 4b")
    for pan in panels:
        q = wdf[(wdf.panel == pan.name) & wdf.chosen_IS].iloc[0]
        a = wdf[(wdf.panel == pan.name) & (wdf.cadence == PRIMARY_CAD)
                & (wdf.chooser == "CH_ANCHOR") & (wdf.window == "EXPAND")].iloc[0]
        say(f"       {pan.name:6s} {q.cadence:8s} {q.window:7s} {q.chooser:12s}  "
            f"{q.CAGR:7.2%} / {q.Sharpe:.4f} / {q.MaxDD:8.2%}  {q.H1:.4f}/{q.H2:.4f}  "
            f"{int(q.moves):4d}  {'T' if q.KEEP_4a else 'F'}  {'T' if q.KEEP_4b else 'F'}")
        say(f"       {'':6s} ANCHOR (do nothing)              {a.CAGR:7.2%} / "
            f"{a.Sharpe:.4f} / {a.MaxDD:8.2%}  {a.H1:.4f}/{a.H2:.4f}  {int(a.moves):4d}"
            f"  {'T' if a.KEEP_4a else 'F'}  {'T' if a.KEEP_4b else 'F'}")
        d = BM[(pan.name, "SPY")]
        say(f"       {'':6s} SPY                              {d['OOS_CAGR']:7.2%} / "
            f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
        d = BM[(pan.name, "LIVE")]
        say(f"       {'':6s} LIVE RULES v2                    {d['OOS_CAGR']:7.2%} / "
            f"{d['OOS_Sharpe']:.4f} / {d['OOS_MaxDD']:8.2%}")
    say("")
    say(f"    RULE 8 over all {len(wdf)} (panel, cadence, window, form) OOS rows: "
        f"4a {int(wdf.KEEP_4a.sum())}; 4b {int(wdf.KEEP_4b.sum())}.")
    mean_pick = float(wdf[wdf.chosen_IS].Sharpe.mean())
    mean_anch = float(wdf[(wdf.cadence == PRIMARY_CAD) & (wdf.chooser == "CH_ANCHOR")
                          & (wdf.window == "EXPAND")].Sharpe.mean())
    say(f"    MEAN OOS SHARPE of the IS-chosen cell {mean_pick:.4f} against DOING NOTHING "
        f"{mean_anch:.4f} ({mean_pick - mean_anch:+.4f}).")

    # ================================================================ verdict
    say("")
    say("=" * 108)
    say("VERDICT")
    say("=" * 108)
    prim = bdf[(bdf.cadence == PRIMARY_CAD) & (bdf.SET == "ALL4") & bdf.chooser.isin(HFORMS)]
    nsep = int(prim.separates.sum())
    allsep = int(bdf[bdf.chooser.isin(HFORMS)].separates.sum())
    rprim = rdf[(rdf.cadence == PRIMARY_CAD) & (rdf.SET == "ALL4") & rdf.chooser.isin(HFORMS)]
    natt = int(rprim.attainable.sum())
    npos = int((rprim.gap > 0).sum())
    say(f"  At the primary cadence / ALL4, {nsep} of {len(prim)} (form, window) cells separate")
    say(f"  from their own NL_PERM band at alpha 0.05; {allsep} of "
        f"{int(bdf.chooser.isin(HFORMS).sum())} across all three cadences.")
    say(f"  {npos} of {len(rprim)} cells even have a POSITIVE gap (obs above the null's mean);")
    say(f"  {natt} of {len(rprim)} would separate on a tape of <= {ATTAINABLE_YEARS:.0f} years.")
    # --- the aggregate sign test.  Separation is a ONE-SIDED question, so which side the
    # forms sit on is prior to how much tape they would need.
    hall = bdf[bdf.chooser.isin(HFORMS)].dropna(subset=["gap"])
    npos_all = int((hall.gap > 0).sum())
    nall = len(hall)
    try:
        from math import comb
        tail = sum(comb(nall, k) for k in range(0, npos_all + 1)) / (2.0 ** nall)
        sign_p = min(1.0, 2.0 * tail)
    except Exception:
        sign_p = np.nan
    say("")
    say(f"  THE AGGREGATE SIGN.  Over all {nall} (cadence, set, window, form) cells with a")
    say(f"  defined band, the observed delta sits ABOVE its own NL_PERM mean at {npos_all};")
    say(f"  a coin would give {nall/2:.0f}.  Two-sided binomial p = {sign_p:.3e}.  Mean gap")
    say(f"  {hall.gap.mean():+.4f} of Sharpe, median {hall.gap.median():+.4f}, mean p_NL_PERM")
    say(f"  {hall.p_NL_PERM.mean():.4f}.  RE-DEALING A FORM'S OWN DESTINATIONS TO RANDOM FOLDS")
    say("  BEATS ITS ACTUAL TIMING, systematically and at every cadence.  A required-precision")
    say("  number is therefore only meaningful for the minority of cells on the positive side.")
    exp_fp = 0.05 * int(bdf.chooser.isin(HFORMS).sum())
    say(f"  MULTIPLICITY: {allsep} separating cell(s) against {exp_fp:.1f} expected at alpha")
    say(f"  0.05 by chance over {int(bdf.chooser.isin(HFORMS).sum())} form cells — at or below")
    say("  the false-positive rate, so no separating cell is evidence of anything.")
    GATES.append(dict(gate="G12 separating-cell count does not exceed the alpha-0.05 "
                           "false-positive expectation", value=float(allsep), target=exp_fp,
                      pass_=bool(allsep <= exp_fp)))

    fin = rprim[np.isfinite(rprim.tape_years)]
    if len(fin):
        q = fin.loc[fin.tape_years.idxmin()]
        qm = int(bdf[(bdf.cadence == q.cadence) & (bdf.SET == q.SET) & (bdf.window == q.window)
                     & (bdf.chooser == q.chooser)].iloc[0].moves)
        say(f"  CHEAPEST SEPARATION ANYWHERE ON THE GRID: {q.chooser} at {q.window} needs "
            f"{q.tape_years:.0f} years of tape (gap {q.gap:+.4f} against half-width "
            f"{q.half_width:.4f}, fitted b {q.b_fit:.3f}).")
        say(f"  THAT NUMBER RESTS ON {qm} MOVES over {int(q.F_now)} folds per panel.  A gap "
            "estimated from")
        say(f"  {qm} moves is itself unresolved, so read {q.tape_years:.0f} years as a LOWER "
            "BOUND on the tape this")
        say("  question needs, not as a forecast that the tape would settle it.")
    else:
        say("  NO cell on the grid has a positive gap: no tape length separates any form.")
    if nsep:
        outcome = "(A) SEPARABLE NOW"
    elif natt:
        outcome = "(B) SEPARABLE ON AN ATTAINABLE TAPE"
    else:
        outcome = "(C) NOT SEPARABLE ON ANY ATTAINABLE TAPE"
    say(f"  PRE-DECLARED OUTCOME: {outcome}")
    say("")
    say("  CAPITAL: 4a 0-of-grid and 4b rows are reported above; this run promotes NOTHING and")
    say("  writes no memo unless a stitched curve or rule-8 row clears 4b BOTH full and OOS on")
    say("  a book the record has not already committed.")
    say("")
    say("  SURVIVORSHIP (rule 9): B136 and SMALL are CURRENT constituents; SMALL is the sub-$2B")
    say(f"  screen with {len(pxS.columns)-1-len(inv)} of {len(pxS.columns)-1} tickers dropped "
        "for max_1d_move >= 1.0.  The bias does not cancel out of the OOS levels or the 4b")
    say("  legs, so any pass there is an upper bound; it largely does cancel out of a")
    say("  gap-to-band RATIO, which is this run's headline.")

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
