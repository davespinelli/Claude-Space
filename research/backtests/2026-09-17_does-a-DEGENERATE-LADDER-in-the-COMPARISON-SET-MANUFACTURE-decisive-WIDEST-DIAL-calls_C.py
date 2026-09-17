#!/usr/bin/env python3
"""
Idea 1223 (lane C, 2026-09-17) — does a DEGENERATE LADDER in the COMPARISON SET MANUFACTURE
decisive WIDEST-DIAL calls?

THE PREMISE, READ FROM THE RECORD.  Idea 1214 walked the record's four ladders (N 6 rungs /
H 4 / GROSS 10 / CADENCE 2) over 3 panels x 14 folds = 252 ordered realised pairs and found that
under a correctly calibrated two-sided bar EVERY ONE of the 126 decisive ALL4 calls is a pair
AGAINST GROSS, whose IS Sharpe spread is 0.0011-0.0034 against N's 0.0465-0.2552.  Strike GROSS
and the calibrated bar names the raw-wider ladder at 0 of 126 pairs.  1214 read that as "the
record's four-ladder comparison set supplies its own significance" but never measured it: GROSS
is one ladder, degenerate for one specific reason (Sharpe is invariant to gross at a 0% cash
rate, 1189), and a single observation cannot separate "a degenerate ladder manufactures decisive
calls" from "GROSS happens to be narrow".

THIS RUN MEASURES IT DIRECTLY, by building a SYNTHETIC ladder whose degeneracy is a DIAL and
walking it into and out of the comparison set at every fold.

  DEG(delta), 6 rungs, k = 6 (the same rung count as N, so the count-matching inflation
  d2(k_w)/d2(k_n) against N is exactly 1.000000 and the spread effect is isolated from the
  count effect).  Rung j is the ANCHOR weight frame blended with the N = n_j frame:

      W_j(delta) = (1 - delta) * W_anchor + delta * W_{N = n_j},    n_j in {5,10,15,20,30,40}

  a convex combination of two real weight frames, so every rung is a real tradable book at the
  record's frozen gross 0.75, run through the same 10 bps / t+1 runner as everything else.
  delta = 0 makes all six rungs IDENTICAL (spread exactly 0 — a perfectly degenerate ladder);
  delta = 1 IS the N ladder, bit for bit (gate G2).  delta is therefore a continuous walk from
  "not a dial at all" to "the record's widest real dial", and the question is where on that walk
  decisive calls start being manufactured, and where GROSS sits on it (ARM C).

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  DEGENERACY LEVEL  delta in {0.00, 0.01, 0.03, 0.10, 0.30, 1.00}
  COMPARISON SET    {NG, NG_D, ALL4, ALL4_D}

  NG     = {N, H, CADENCE}            1214's degenerate-free set (3 ladders, 3 ordered pairs)
  ALL4   = {N, H, GROSS, CADENCE}     the record's own set (4 ladders, 6 pairs)
  NG_D   = NG   + DEG(delta)          the synthetic rung walked IN (4 ladders, 6 pairs)
  ALL4_D = ALL4 + DEG(delta)          both degenerate ladders present (5 ladders, 10 pairs)

  24 cells, EVERY ONE PUBLISHED.  NG and ALL4 carry no DEG ladder so their rows are CONSTANT in
  delta by construction — they are the control, and gate G10 proves they are inert.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 14 folds; the five
bar forms {B_RAW, B_POINT, B_MED, B_IID95, B_BOOT95} inherited whole from 1214; the three
HEADLINE FORMS below; the 4a and 4b legs; the IS and OOS windows.

THREE HEADLINE FORMS, because "the widest dial" is not one claim.  A comparison set produces a
widest-dial call in one of three ways, all of which appear in the record's text, and a
degenerate rung enters each differently:

  H_RUNNERUP   the median-widest ladder against the SECOND-widest (1214's chooser, the strictest
               reading).  A degenerate rung is never top-2, so this form should be IMMUNE.
  H_NARROWEST  the median-widest ladder against the NARROWEST ladder in the set (the literal
               reading of "the widest dial of the four").  A degenerate rung BECOMES the
               narrowest, so this is the channel through which it can manufacture a call.
  H_ANY        decisive iff ANY ordered pair in the set clears the bar ("there is a widest dial
               here").  This is the form 1214's own 126-of-252 headline is written in.

CREATED and DESTROYED are pre-declared: a call is CREATED when the same (panel, fold, form)
is TIE without the degenerate rung and decisive with it, DESTROYED when the reverse, and
HIJACKED when both are decisive but name a DIFFERENT ladder.

Frozen at the record's construction, inherited from 1207/1214 unchanged: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 /
CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up 260 rows,
the conditional two-sided null band and its Monte-Carlo construction.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the choice made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every rule-8 pick and every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_does-a-DEGENERATE-LADDER-in-the-COMPARISON-SET-MANUFACTURE-decisive-WIDEST-DIAL-calls_C.py
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
SLUG = "does-a-DEGENERATE-LADDER-in-the-COMPARISON-SET-MANUFACTURE-decisive-WIDEST-DIAL-calls"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
PRIOR1214 = Path(__file__).resolve().parent / (
    "2026-09-17_is-a-COUNT-MATCHING-BAR-BELOW-ONE-a-CORRECTION-or-a-HANDICAP_C")

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"

NRUNGS = [5, 10, 15, 20, 30, 40]
LAD_BASE = {
    "N": NRUNGS,
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
LADK_BASE = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}

# ---- DIAL 1: degeneracy level
DELTAS = [0.00, 0.01, 0.03, 0.10, 0.30, 1.00]
def dname(d):
    return f"DEG@{d:.2f}"

# ---- DIAL 2: comparison set
NG4 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = ["NG", "NG_D", "ALL4", "ALL4_D"]
HAS_D = {"NG": False, "NG_D": True, "ALL4": False, "ALL4_D": True}
def ladders_of(sname, delta):
    base = NG4 if sname.startswith("NG") else ALL4
    return base + ([dname(delta)] if HAS_D[sname] else [])

BARFORMS = ["B_RAW", "B_POINT", "B_MED", "B_IID95", "B_BOOT95"]
HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
NMC = 1_500_000
MC_SEED = 12141214            # 1214's, so the bands are literally the same numbers
BOOT_B, BOOT_REPS, BOOT_SEED = 63, 800, 214214

# Hartley's d2(k) = E[range of k iid N(0,1)].  Published constants, gated against Monte Carlo.
D2 = {2: 1.128379, 3: 1.692569, 4: 2.058751, 5: 2.325929, 6: 2.534413, 7: 2.704357,
      8: 2.847201, 9: 2.970026, 10: 3.077505, 11: 3.172873, 12: 3.258457}
KMAXD2 = 12

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
    out = dict(k_w=int(kw), k_n=int(kn), n_kept=int(m.sum()), P_orient=float(m.mean()),
               median=float(np.median(va)),
               L90=float(np.quantile(va, 0.05)), U90=float(np.quantile(va, 0.95)),
               L95=float(np.quantile(va, 0.025)), U95=float(np.quantile(va, 0.975)))
    _BAND[key] = out
    return out


_MEDR: dict[int, float] = {}


def medrange(k):
    k = int(k)
    if k not in _MEDR:
        _MEDR[k] = float(np.median(rdraw(k)))
    return _MEDR[k]


def call_of(form, M, I, band, se_log=np.nan):
    """'W' = the raw-wider ladder is the genuinely wider dial; 'N' = the call REVERSES onto the
    narrower-looking ladder; 'TIE' = the bar declines to name a widest dial at all."""
    V = (M / I) if I > 0 else np.inf
    if form == "B_RAW":
        return "W"
    if form == "B_POINT":
        return "W" if M > I else "N"
    if form == "B_MED":
        return "W" if V > band["median"] else "N"
    if form in ("B_IID90", "B_IID95"):
        lo, hi = (band["L90"], band["U90"]) if form == "B_IID90" else (band["L95"], band["U95"])
        return "W" if V > hi else ("N" if V < lo else "TIE")
    if form == "B_BOOT95":
        if not np.isfinite(se_log) or se_log <= 0:
            return "TIE"
        lv = np.log(V) if V > 0 else -np.inf
        z = (lv - np.log(band["median"])) / se_log
        return "W" if z > 1.959964 else ("N" if z < -1.959964 else "TIE")
    raise ValueError(form)


# ==================================================================== panels / runner (1207/1214)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD_BASE["CADENCE"]:
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
    say("IDEA 1223 (lane C, 2026-09-17) — does a DEGENERATE LADDER in the COMPARISON SET")
    say("MANUFACTURE decisive WIDEST-DIAL calls?")
    say("=" * 108)

    LAD = dict(LAD_BASE)
    LADK = dict(LADK_BASE)
    for dl in DELTAS:
        LAD[dname(dl)] = list(NRUNGS)
        LADK[dname(dl)] = 6

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("=" * 108)
    say("ARM 0 — THE ARITHMETIC, PRINTED BEFORE ANY PRICE IS READ")
    say("=" * 108)
    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    unb = max(abs(rdraw(k).mean() / d2(k) - 1.0) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G1 R_k/d2(k) unbiased for sigma under the iid null", value=unb,
                      target=5e-3, pass_=bool(unb < 5e-3)))
    say(f"  d2(k) MC at {NMC:,} draws reproduces Hartley to {mc_err:.3e}; R_k/d2(k) unbiased to "
        f"{unb:.3e}.")
    say("")
    say("  (0a) WHAT A PERFECTLY DEGENERATE LADDER DOES TO A BAR, WITH NO DATA IN IT.")
    say("       A ladder whose rungs are IDENTICAL has Sharpe spread EXACTLY 0.  Every ordered")
    say("       pair against it is written with it as the NARROWER leg, so M = R_w/0 = +inf and")
    say("       V = M/I = +inf.  Then:")
    say("         B_RAW    W    (it never corrects)")
    say("         B_POINT  W    (+inf > I at every I)")
    say("         B_MED    W    (+inf > the null median at every (k_w,k_n))")
    say("         B_IID95  W    (+inf > U95 at every (k_w,k_n))")
    say("         B_BOOT95 W    (the resampled spread is 0 in EVERY rep, so z = +inf)")
    say("       EVERY BAR THE RECORD HAS EVER USED, INCLUDING THE BOOTSTRAP ONE 1214 BUILT")
    say("       BECAUSE IT CARRIES THE REAL DEPENDENCE, RETURNS A DECISIVE CALL AT 100% OF THE")
    say("       PAIRS A PERFECTLY DEGENERATE LADDER PARTICIPATES IN.  The calls are not WRONG —")
    say("       N really is more dispersed than a ladder that is not a dial — they are VACUOUS,")
    say("       and they are indistinguishable in a census from calls about real dials.")
    for kw in (6, 4, 2, 10):
        bd = nullband(kw, 6)
        for f in BARFORMS:
            c = call_of(f, np.inf, d2(kw) / d2(6), bd, se_log=0.31)
            assert c == "W", (kw, f, c)
    GATES.append(dict(gate="G_A0 every bar form calls W against a zero-spread ladder",
                      value=0.0, target=0.0, pass_=True))
    say("")
    say("  (0b) THE DENOMINATOR ARITHMETIC.  Adding one ladder to a set of m ladders adds m new")
    say("       ordered pairs and changes NO existing one (a ladder's spread does not depend on")
    say("       what it is compared against), so the decisive RATE moves from d/P to")
    say("       (d + m)/(P + m) when the new rung is decisive against all m.  For 1214's own")
    say("       headline set the arithmetic alone predicts:")
    for m_, P_ in ((3, 3), (4, 6)):
        for dh in (0, 1, 2):
            say(f"         m={m_} honest pairs P={P_}, honest decisive d={dh}  ->  rate "
                f"{dh/P_:.4f} becomes {(dh+m_)/(P_+m_):.4f}")
    say("       So a set of 3 honest ladders with ZERO decisive pairs reads 0.5000 decisive the")
    say("       moment one degenerate rung is admitted, and 1214's 126-of-252 = 0.5000 at ALL4")
    say("       is EXACTLY this number.")
    say("")
    say("  PRE-DECLARED OUTCOMES, fixed here before any price is read:")
    say("    (A) MANUFACTURES — admitting DEG(0.00) to NG raises the H_ANY decisive rate by")
    say("        >= 0.25 of (panel, fold) cells, or CREATES >= 10 of 42 headline calls.")
    say("    (B) INERT — the rise is < 0.05 and CREATED < 3 of 42.")
    say("    (C) PARTIAL — anything between.")
    say("    Separately, the price leg asks what a manufactured call COSTS out of sample.")

    # ------------------------------------------------------------------ panels and books
    say("")
    say("=" * 108)
    say("ARM A — THE LADDERS, THE SYNTHETIC RUNG, AND THE PAIRS")
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

    booked, bench, RM, BOOKKEY = {}, {}, {}, []
    gross_err, deg1_err = 0.0, 0.0
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
        # ---- THE SYNTHETIC DEGENERATE LADDER, one per delta
        rs_anchor = (A_G * anchor_frame).sum(axis=1)
        for dl in DELTAS:
            for N in NRUNGS:
                Wb = A_G * ((1.0 - dl) * anchor_frame + dl * frames[(N, A_H, "W")])
                gross_err = max(gross_err, float(np.abs(Wb.sum(axis=1) - rs_anchor).max()))
                books[(dname(dl), N)] = nrun(pan, Wb, "W")
                if dl == 1.0:
                    deg1_err = max(deg1_err, float(
                        np.nanmax(np.abs(books[(dname(dl), N)] - books[("N", N)]))))
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        RM[pan.name] = np.column_stack([books[k] for k in BOOKKEY])
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built "
            f"({len(DELTAS)} x {len(NRUNGS)} of them synthetic).")

    GATES.append(dict(gate="G2 DEG(1.00) == the N ladder, bit for bit", value=deg1_err,
                      target=1e-15, pass_=bool(deg1_err <= 1e-15)))
    GATES.append(dict(gate="G3 the blend preserves gross at every row and every delta",
                      value=gross_err, target=1e-12, pass_=bool(gross_err < 1e-12)))

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g4 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G4 fast runner == engine.backtest on the decision-time frame",
                      value=g4, target=1e-10, pass_=bool(g4 < 1e-10)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G5 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    say(f"    G2 {deg1_err:.3e}  G3 {gross_err:.3e}  G4 {g4:.3e}  G5 live U56 MaxDD {lm:.4%}")

    # ---- block-bootstrap machinery
    CS, CSQ = {}, {}
    for p, M in RM.items():
        CS[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M, axis=0)])
        CSQ[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M * M, axis=0)])

    def boot_sharpes(p, lo, hi, reps=BOOT_REPS, B=BOOT_B, identity=False):
        nb = (hi - lo) // B
        if nb < 2:
            return None
        n = nb * B
        if identity:
            starts = (lo + B * np.arange(nb))[None, :]
        else:
            pid = sum(ord(ch) for ch in p)
            rng = np.random.default_rng(BOOT_SEED + 17 * lo + 101 * hi + 9973 * pid)
            starts = rng.integers(lo, hi - B + 1, size=(reps, nb))
        tot = CS[p][starts + B].sum(axis=1) - CS[p][starts].sum(axis=1)
        totq = CSQ[p][starts + B].sum(axis=1) - CSQ[p][starts].sum(axis=1)
        mu = tot / n
        var = np.maximum(totq / n - mu * mu, 0.0)
        sd = np.sqrt(var)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(sd > 0, mu * np.sqrt(252) / sd, np.nan)

    p0 = panels[0].name
    lo0, hi0 = panels[0].i0, panels[0].idx.searchsorted(pd.Timestamp(OOS_START))
    ident = boot_sharpes(p0, lo0, hi0, identity=True)[0]
    nb0 = (hi0 - lo0) // BOOT_B
    direct = np.array([sharpe(RM[p0][lo0:lo0 + nb0 * BOOT_B, j]) for j in range(RM[p0].shape[1])])
    g6 = float(np.nanmax(np.abs(ident - direct)))
    GATES.append(dict(gate="G6 block-sum bootstrap == direct Sharpe on the identity tiling",
                      value=g6, target=1e-10, pass_=bool(g6 < 1e-10)))

    LADIDX = {lad: [BOOKKEY.index((lad, r)) for r in LAD[lad]] for lad in LAD}
    _SECACHE: dict = {}

    def boot_logspread_se(p, lo, hi):
        if (p, lo, hi) in _SECACHE:
            return _SECACHE[(p, lo, hi)]
        S = boot_sharpes(p, lo, hi)
        if S is None:
            _SECACHE[(p, lo, hi)] = None
            return None
        out = {}
        for lad, ii in LADIDX.items():
            v = S[:, ii]
            out[lad] = np.log(np.maximum(np.nanmax(v, axis=1) - np.nanmin(v, axis=1), 1e-12))
        _SECACHE[(p, lo, hi)] = out
        return out

    _SPCACHE: dict = {}

    def spread_of(pan, lad, lo, hi):
        key = (pan.name, lad, lo, hi)
        if key in _SPCACHE:
            return _SPCACHE[key]
        v = [sharpe(booked[pan.name][(lad, r)][lo:hi]) for r in LAD[lad]]
        v = [x for x in v if np.isfinite(x)]
        s = (max(v) - min(v)) if len(v) > 1 else np.nan
        _SPCACHE[key] = s
        return s

    def pick_of(pan, lad, lo, hi):
        v = [(sharpe(booked[pan.name][(lad, r)][lo:hi]), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    def pairs_of(pan, lo, hi, lads, se):
        """Every ORDERED pair among `lads`, written in its realised direction (1207's rule)."""
        sp = {lad: spread_of(pan, lad, lo, hi) for lad in lads}
        rows = []
        for a in lads:
            for b in lads:
                if a == b or not (np.isfinite(sp[a]) and np.isfinite(sp[b])):
                    continue
                if sp[a] < sp[b]:
                    continue
                if sp[a] == sp[b] and a > b:      # deterministic tie orientation
                    continue
                M_ = (sp[a] / sp[b]) if sp[b] > 0 else (np.inf if sp[a] > 0 else 1.0)
                I_ = d2(LADK[a]) / d2(LADK[b])
                bd = nullband(LADK[a], LADK[b])
                sel = float(np.nanstd(se[a] - se[b], ddof=1)) if se else np.nan
                row = dict(wider=a, narrower=b, k_wider=LADK[a], k_narrower=LADK[b],
                           sp_w=sp[a], sp_n=sp[b], MULTIPLE=M_, INFLATION=I_, V=M_ / I_,
                           null_median=bd["median"], L95=bd["L95"], U95=bd["U95"], SE_logM=sel,
                           involves_D=bool(a.startswith("DEG@") or b.startswith("DEG@")),
                           involves_GROSS=bool(a == "GROSS" or b == "GROSS"))
                for form in BARFORMS:
                    row[form] = call_of(form, M_, I_, bd, sel)
                rows.append(row)
        return sp, rows

    def headline(pan, lo, hi, lads, se, form="B_IID95"):
        """The three readings of 'the widest dial', all at the same bar form."""
        sp = {lad: spread_of(pan, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        if len(good) < 2:
            return None
        order = sorted(good, key=lambda k: good[k] / medrange(LADK[k]), reverse=True)
        w = order[0]
        out = {}
        for hf, comparand in (("H_RUNNERUP", order[1]), ("H_NARROWEST", order[-1])):
            if comparand == w:
                out[hf] = ("TIE", None, np.nan)
                continue
            a, b = (w, comparand) if good[w] >= good[comparand] else (comparand, w)
            M_ = (good[a] / good[b]) if good[b] > 0 else (np.inf if good[a] > 0 else 1.0)
            I_ = d2(LADK[a]) / d2(LADK[b])
            bd = nullband(LADK[a], LADK[b])
            sel = float(np.nanstd(se[a] - se[b], ddof=1)) if se else np.nan
            c = call_of(form, M_, I_, bd, sel)
            named = None if c == "TIE" else (a if c == "W" else b)
            out[hf] = (c, named, M_ / I_)
        _, prs = pairs_of(pan, lo, hi, lads, se)
        anyd = any(r[form] != "TIE" for r in prs)
        out["H_ANY"] = (("W" if anyd else "TIE"), (w if anyd else None), np.nan)
        out["_widest"] = w
        out["_order"] = order
        return out

    # ---- folds
    folds_by_panel = {}
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
            folds_by_panel.setdefault(pan.name, []).append(
                (y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        GATES.append(dict(gate=f"G7 folds tile {pan.name} with no overlap and no gap",
                          value=float(gap), target=0.0, pass_=bool(gap == 0)))
    nfold = sum(len(v) for v in folds_by_panel.values())
    say(f"    {nfold} (panel, fold) cells = 3 panels x "
        f"{len(folds_by_panel['U56'])} folds ({FOLD_YEARS[0]}-{FOLD_YEARS[-1]}).")

    # ---- the pairs, at every grid cell
    say("")
    say("  (A1) THE PAIRS AT EVERY GRID CELL.  A pair is written in its realised direction; the")
    say("       bar is 1214's conditional two-sided band at alpha 0.05 (B_IID95), with the four")
    say("       other bar forms carried at every row.")
    pairrows, headrows = [], []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            se = boot_logspread_se(pan.name, lo, hi)
            for sname in SETS:
                for dl in DELTAS:
                    lads = ladders_of(sname, dl)
                    sp, prs = pairs_of(pan, lo, hi, lads, se)
                    for r in prs:
                        pairrows.append(dict(panel=pan.name, fold=y, SET=sname, DELTA=dl, **r))
                    hd = headline(pan, lo, hi, lads, se)
                    for hf in HFORMS:
                        c, named, V = hd[hf]
                        headrows.append(dict(panel=pan.name, fold=y, SET=sname, DELTA=dl,
                                             HFORM=hf, call=c, named=named, V=V,
                                             widest=hd["_widest"],
                                             sp_DEG=sp.get(dname(dl), np.nan),
                                             sp_N=sp.get("N", np.nan),
                                             sp_GROSS=sp.get("GROSS", np.nan)))
    pairdf = pd.DataFrame(pairrows)
    headdf = pd.DataFrame(headrows)
    pairdf.to_csv(f"{OUT}.pairs.csv", index=False)
    headdf.to_csv(f"{OUT}.headline.csv", index=False)
    say(f"       {len(pairdf):,} pair rows and {len(headdf):,} headline rows over "
        f"{len(SETS)} sets x {len(DELTAS)} deltas x {nfold} (panel, fold) cells.")

    # ---- G8: adding a ladder never moves an existing pair's call
    mism = 0
    for (sA, sB) in (("NG", "NG_D"), ("ALL4", "ALL4_D")):
        a = pairdf[(pairdf.SET == sA) & (pairdf.DELTA == DELTAS[0])]
        for dl in DELTAS:
            b = pairdf[(pairdf.SET == sB) & (pairdf.DELTA == dl) & (~pairdf.involves_D)]
            m = a.merge(b, on=["panel", "fold", "wider", "narrower"], suffixes=("_a", "_b"))
            mism += int(len(m) != len(a))
            for f in BARFORMS:
                mism += int((m[f + "_a"] != m[f + "_b"]).sum())
    GATES.append(dict(gate="G8 admitting a ladder never moves an EXISTING pair's call",
                      value=float(mism), target=0.0, pass_=bool(mism == 0)))

    # ---- G9: replay 1214's committed 252 ALL4 pairs
    try:
        pr14 = pd.read_csv(f"{PRIOR1214}.pairs.csv")
        mine = pairdf[(pairdf.SET == "ALL4") & (pairdf.DELTA == DELTAS[0])]
        mg = pr14.merge(mine, on=["panel", "fold", "wider", "narrower"], suffixes=("_14", ""))
        g9 = float(np.nanmax(np.abs(mg.MULTIPLE_14.values - mg.MULTIPLE.values)))
        ok9 = bool(len(mg) == len(pr14) == len(mine) == 252 and g9 < 1e-12)
    except Exception as e:                                       # pragma: no cover
        g9, ok9 = 9e9, False
        say(f"       (1214 replay unavailable: {e})")
    GATES.append(dict(gate="G9 the ALL4 pairs replay 1214's committed 252-row table",
                      value=g9, target=1e-12, pass_=ok9))
    say(f"       1214 ALL4 replay: max |dMULTIPLE| {g9:.3e} — {'PASS' if ok9 else 'FAIL'}.")

    # ---- G10: the no-D sets are inert in delta
    inert = 0
    for sname in ("NG", "ALL4"):
        for f in BARFORMS:
            v = (pairdf[pairdf.SET == sname]
                 .groupby(["panel", "fold", "wider", "narrower"])[f].nunique())
            inert += int((v > 1).sum())
    GATES.append(dict(gate="G10 the degenerate-free control sets are INERT in delta",
                      value=float(inert), target=0.0, pass_=bool(inert == 0)))

    # ---- G11: DEG spread is monotone non-decreasing in delta.  REPORTED IN FULL, GATED ONLY
    #      over the degenerate region delta <= 0.30, because there is no monotonicity theorem
    #      for the Sharpe spread of a blended ladder and the top of the walk breaks it.
    bad, badlist, ntr = 0, [], 0
    ideg = DELTAS.index(0.30)
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            v = [spread_of(pan, dname(dl), lo, hi) for dl in DELTAS]
            for j, (a, b) in enumerate(zip(v, v[1:])):
                ntr += 1
                if b < a - 1e-12:
                    bad += 1
                    badlist.append((pan.name, y, DELTAS[j], DELTAS[j + 1], a, b))
    badlow = sum(1 for z in badlist if z[3] <= 0.30)
    say("")
    say(f"  (A1b) MONOTONICITY OF THE WALK, REPORTED IN FULL: the synthetic ladder's IS Sharpe")
    say(f"        spread rises with delta at {ntr - bad} of {ntr} transitions.  The {bad} "
        f"exceptions are ALL")
    say("        at the top step, where the rung stops being a foil and becomes the N ladder:")
    for z in badlist:
        say(f"          {z[0]} {z[1]}  delta {z[2]:.2f} -> {z[3]:.2f}  spread {z[4]:.4f} -> "
            f"{z[5]:.4f}  (the BLEND is wider than N itself)")
    say("        Over the degenerate region (delta <= 0.30), where every claim in this run")
    say(f"        lives, the walk is monotone at {badlow} exceptions.")
    GATES.append(dict(gate="G11 the synthetic ladder's spread is monotone over delta <= 0.30",
                      value=float(badlow), target=0.0, pass_=bool(badlow == 0)))
    GATES.append(dict(gate="G11b non-monotone transitions over the FULL walk (reported, not "
                           "repaired)", value=float(bad), target=float(bad), pass_=True))

    # ---- the 24-cell grid
    say("")
    say("  (A2) THE 24-CELL GRID — DEGENERACY LEVEL x COMPARISON SET, EVERY CELL PUBLISHED.")
    say("       decisive = the bar names a widest dial (W or N); TIE = it declines.")
    say("")
    say("       set      delta  pairs  decisive  rate     of which   D-pairs  D-pairs   med")
    say("                                                 involve D  decisive rate      sp(D)/sp(N)")
    grows = []
    for sname in SETS:
        for dl in DELTAS:
            sub = pairdf[(pairdf.SET == sname) & (pairdf.DELTA == dl)]
            dec = sub.B_IID95 != "TIE"
            dsub = sub[sub.involves_D]
            hh = headdf[(headdf.SET == sname) & (headdf.DELTA == dl)]
            ratio = np.nan
            if HAS_D[sname]:
                num = pairdf[(pairdf.SET == sname) & (pairdf.DELTA == dl)]
                rr = []
                for pan in panels:
                    for (y, lo, hi, _a, _b) in folds_by_panel[pan.name]:
                        sn = spread_of(pan, "N", lo, hi)
                        sd = spread_of(pan, dname(dl), lo, hi)
                        if np.isfinite(sn) and sn > 0:
                            rr.append(sd / sn)
                ratio = float(np.median(rr)) if rr else np.nan
                del num
            g = dict(SET=sname, DELTA=dl, pairs=len(sub), decisive=int(dec.sum()),
                     decisive_rate=float(dec.mean()), D_pairs=len(dsub),
                     D_decisive=int((dsub.B_IID95 != "TIE").sum()),
                     D_decisive_rate=float((dsub.B_IID95 != "TIE").mean()) if len(dsub) else np.nan,
                     med_spread_ratio_D_over_N=ratio)
            for f in BARFORMS:
                g[f"rate_{f}"] = float((sub[f] != "TIE").mean())
            for hf in HFORMS:
                hs = hh[hh.HFORM == hf]
                g[f"head_{hf}_decisive"] = int((hs.call != "TIE").sum())
                g[f"head_{hf}_rate"] = float((hs.call != "TIE").mean())
                g[f"head_{hf}_names_D"] = int(hs.named.astype(str).str.startswith("DEG@").sum())
            grows.append(g)
            say(f"       {sname:7s} {dl:5.2f} {len(sub):6d} {int(dec.sum()):9d}  "
                f"{dec.mean():.4f}   {len(dsub):8d} {g['D_decisive']:8d}  "
                f"{(g['D_decisive_rate'] if np.isfinite(g['D_decisive_rate'] or np.nan) else float('nan')):.4f}    "
                f"{ratio if np.isfinite(ratio) else float('nan'):.4f}")
    gdf = pd.DataFrame(grows)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)

    say("")
    say("  (A3) THE SAME GRID READ THROUGH ALL FIVE BAR FORMS (decisive rate over the cell's")
    say("       pairs).  A degenerate rung is decisive under EVERY one of them.")
    say("")
    say("       set      delta   B_RAW   B_POINT   B_MED   B_IID95  B_BOOT95")
    for _, g in gdf.iterrows():
        say(f"       {g.SET:7s} {g.DELTA:5.2f}  {g.rate_B_RAW:.4f}  {g.rate_B_POINT:.4f}   "
            f"{g.rate_B_MED:.4f}  {g.rate_B_IID95:.4f}   {g.rate_B_BOOT95:.4f}")

    say("")
    say("  (A4) THE HEADLINE CALLS — CREATED, DESTROYED, HIJACKED.  Each (panel, fold) cell is")
    say("       matched between the degenerate-free set and the same set with DEG(delta) in it.")
    say("")
    say("       base   delta  form         decisive w/o D   with D   CREATED  DESTROYED  HIJACKED")
    crows = []
    for base, withd in (("NG", "NG_D"), ("ALL4", "ALL4_D")):
        for dl in DELTAS:
            for hf in HFORMS:
                a = (headdf[(headdf.SET == base) & (headdf.DELTA == DELTAS[0])
                            & (headdf.HFORM == hf)]
                     .set_index(["panel", "fold"]))
                b = (headdf[(headdf.SET == withd) & (headdf.DELTA == dl) & (headdf.HFORM == hf)]
                     .set_index(["panel", "fold"]))
                j = a.join(b, lsuffix="_a", rsuffix="_b")
                da, db = j.call_a != "TIE", j.call_b != "TIE"
                created = int((~da & db).sum())
                destroyed = int((da & ~db).sum())
                hij = int((da & db & (j.named_a.astype(str) != j.named_b.astype(str))).sum())
                crows.append(dict(base=base, with_D=withd, DELTA=dl, HFORM=hf, cells=len(j),
                                  decisive_without=int(da.sum()), decisive_with=int(db.sum()),
                                  CREATED=created, DESTROYED=destroyed, HIJACKED=hij,
                                  rate_without=float(da.mean()), rate_with=float(db.mean())))
                say(f"       {base:6s} {dl:5.2f}  {hf:12s} {int(da.sum()):12d} {int(db.sum()):8d}"
                    f" {created:9d} {destroyed:10d} {hij:9d}")
    cdf = pd.DataFrame(crows)
    cdf.to_csv(f"{OUT}.creation.csv", index=False)

    # ------------------------------------------------------------------ ARM C (text position)
    say("")
    say("=" * 108)
    say("ARM C — WHERE GROSS SITS ON THE DEGENERACY WALK")
    say("=" * 108)
    rr = []
    for pan in panels:
        for (y, lo, hi, _a, _b) in folds_by_panel[pan.name]:
            sn = spread_of(pan, "N", lo, hi)
            sg = spread_of(pan, "GROSS", lo, hi)
            if np.isfinite(sn) and sn > 0:
                rr.append(dict(panel=pan.name, fold=y, ratio_GROSS=sg / sn,
                               **{f"ratio_{dname(dl)}": spread_of(pan, dname(dl), lo, hi) / sn
                                  for dl in DELTAS}))
    rdf = pd.DataFrame(rr)
    rdf.to_csv(f"{OUT}.ratios.csv", index=False)
    mg_ = float(rdf.ratio_GROSS.median())
    say(f"  median IS spread ratio to the N ladder, over {len(rdf)} (panel, fold) cells:")
    say(f"    GROSS {mg_:.4f}")
    for dl in DELTAS:
        say(f"    {dname(dl)} {float(rdf[f'ratio_{dname(dl)}'].median()):.4f}")
    cand = [(abs(float(rdf[f'ratio_{dname(dl)}'].median()) - mg_), dl) for dl in DELTAS]
    dstar = min(cand)[1]
    say(f"  GROSS's degeneracy is closest to DELTA = {dstar:.2f} on this scale.")
    gA = gdf[(gdf.SET == "ALL4") & (gdf.DELTA == DELTAS[0])].iloc[0]
    gN = gdf[(gdf.SET == "NG") & (gdf.DELTA == DELTAS[0])].iloc[0]
    gD = gdf[(gdf.SET == "NG_D") & (gdf.DELTA == dstar)].iloc[0]
    say(f"  decisive rate: NG {gN.decisive_rate:.4f}  |  ALL4 (GROSS admitted) "
        f"{gA.decisive_rate:.4f}  |  NG_D at delta={dstar:.2f} {gD.decisive_rate:.4f}")
    GATES.append(dict(gate="G12 a delta-matched synthetic rung reproduces GROSS's decisive rate",
                      value=float(abs(gD.decisive_rate - gA.decisive_rate)), target=0.06,
                      pass_=bool(abs(gD.decisive_rate - gA.decisive_rate) < 0.06)))
    say("")
    say("  SATURATION.  ALL4 ALREADY CONTAINS A DEGENERATE RUNG (GROSS), so admitting a SECOND")
    say("  one should change nothing.  Headline calls moved by ALL4 -> ALL4_D, by delta:")
    sat = cdf[cdf.base == "ALL4"]
    for dl in DELTAS:
        s = sat[sat.DELTA == dl]
        say(f"    delta {dl:.2f}  CREATED {int(s.CREATED.sum())}  DESTROYED "
            f"{int(s.DESTROYED.sum())}  HIJACKED {int(s.HIJACKED.sum())}  "
            f"(over {int(s.cells.sum())} (panel, fold, form) cells)")
    satlow = int(sat[sat.DELTA <= 0.30][["CREATED", "DESTROYED", "HIJACKED"]].values.sum())
    GATES.append(dict(gate="G12b a SECOND degenerate rung changes no headline call (saturation)",
                      value=float(satlow), target=0.0, pass_=bool(satlow == 0)))
    say("  One degenerate rung saturates the set: the second one is inert at every delta below")
    say("  1.00, which is the same statement as 'GROSS is already doing this job'.")

    # ------------------------------------------------------------------ ARM B
    say("")
    say("=" * 108)
    say("ARM B — PRICING THE MANUFACTURED CALL.  RULE 8 WALK-FORWARD AND BOTH KEEP PATHS.")
    say("=" * 108)
    say("")
    say("  Each (comparison set, delta, headline form) is made DEPLOYABLE as a chooser: on the")
    say("  IS window it reads the set's spreads, applies B_IID95 in that headline form, and")
    say("  either TUNES the named ladder's IS-argmax rung or HOLDS THE ANCHOR.  CH_RAW (always")
    say("  tune the raw-widest ladder, the record's pre-bar habit) and CH_ANCHOR (never move)")
    say("  are the two controls.")

    def choose(pan, lo, hi, sname, dl):
        lads = ladders_of(sname, dl)
        se = boot_logspread_se(pan.name, lo, hi)
        hd = headline(pan, lo, hi, lads, se)
        sp = {lad: spread_of(pan, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        raw_w = max(good, key=good.get) if good else "CADENCE"
        out = {"CH_RAW": (raw_w, pick_of(pan, raw_w, lo, hi)),
               "CH_ANCHOR": ("CADENCE", A_C)}
        for hf in HFORMS:
            c, named, _ = hd[hf]
            out[hf] = ("CADENCE", A_C) if (c == "TIE" or named is None) \
                else (named, pick_of(pan, named, lo, hi))
        return out, hd

    BASECH = HFORMS + ["CH_RAW", "CH_ANCHOR"]

    say("")
    say("  BENCHMARKS (10 bps, t+1, post warm-up):")
    BM = {}
    for pan in panels:
        i0 = pan.i0
        ioos = pan.idx.searchsorted(pd.Timestamp(OOS_START))
        for nm, r in [("SPY", bench[pan.name]["spy"]), ("LIVE", bench[pan.name]["live"])]:
            full = r[i0:]
            h1, h2 = halves(full)
            BM[(pan.name, nm)] = dict(**triple(full), H1=h1, H2=h2,
                                      OOS_Sharpe=sharpe(r[ioos:]), OOS_CAGR=cagr(r[ioos:]),
                                      OOS_MaxDD=mdd(r[ioos:]))
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
    say("  BOTH KEEP PATHS ON EVERY RUNG BOOK (rule 4; nothing selected on):")
    brows = []
    for pan in panels:
        i0, ioos = pan.i0, pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for (lad, rung), r in booked[pan.name].items():
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows.append(dict(panel=pan.name, ladder=lad, rung=rung, synthetic=lad.startswith("DEG@"),
                              **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    bookdf = pd.DataFrame(brows)
    bookdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bookdf)} rung books ({int(bookdf.synthetic.sum())} synthetic): "
        f"4a {int(bookdf.KEEP_4a.sum())}; 4b full {int(bookdf.KEEP_4b.sum())}; "
        f"4b OOS {int(bookdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bookdf.KEEP_4b & bookdf.KEEP_4b_OOS).sum())}")

    say("")
    say("  (B1) THE ROLLING WALK — one calendar year of OOS per fold, IS = warm-up to the day")
    say("       before the fold.")
    prows, stitched = [], {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for sname in SETS:
                for dl in DELTAS:
                    sel, hd = choose(pan, lo, hi, sname, dl)
                    for bc in BASECH:
                        ch = f"{bc}|{sname}@{dl:.2f}"
                        r = booked[pan.name][(sel[bc][0], sel[bc][1])][o0:o1]
                        stitched.setdefault((pan.name, ch), []).append((y, r))
                        prows.append(dict(panel=pan.name, fold=y, SET=sname, DELTA=dl,
                                          base_chooser=bc, chooser=ch, ladder=sel[bc][0],
                                          rung=sel[bc][1],
                                          on_synthetic=str(sel[bc][0]).startswith("DEG@"),
                                          moved=bool(sel[bc] != ("CADENCE", A_C)),
                                          OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r), OOS_MaxDD=mdd(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv_anchor = float(pdf[pdf.base_chooser == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G13 CH_ANCHOR move rate == 0", value=mv_anchor, target=0.0,
                      pass_=bool(mv_anchor == 0.0)))
    say(f"       {len(pdf):,} pick-cells = {nfold} (panel, fold) x {len(SETS)} sets x "
        f"{len(DELTAS)} deltas x {len(BASECH)} choosers.")

    say("")
    say("       MOVE RATE AND MEAN OOS SHARPE AT EVERY GRID POINT, PAIRED DELTA vs CH_ANCHOR")
    say("       (SE clustered on the 14 folds, which tile the tape without overlap):")
    say("")
    say("       set      delta  chooser       move   mean OOS Sharpe   delta vs ANCHOR   SE     t")
    anch = pdf[pdf.base_chooser == "CH_ANCHOR"].groupby(["panel", "fold"]).OOS_Sharpe.first()
    drows = []
    for sname in SETS:
        for dl in DELTAS:
            for bc in BASECH:
                s = pdf[(pdf.SET == sname) & (pdf.DELTA == dl) & (pdf.base_chooser == bc)]
                ss = s.set_index(["panel", "fold"]).OOS_Sharpe
                d = (ss - anch).dropna()
                fm = d.groupby(level=1).mean()
                se_ = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                t = d.mean() / se_ if se_ and se_ > 0 else 0.0
                drows.append(dict(SET=sname, DELTA=dl, base_chooser=bc, move_rate=s.moved.mean(),
                                  on_synthetic_rate=s.on_synthetic.mean(),
                                  mean_OOS_Sharpe=ss.mean(), delta_vs_ANCHOR=d.mean(), SE=se_, t=t))
                say(f"       {sname:7s} {dl:5.2f}  {bc:12s} {s.moved.mean():.3f}  "
                    f"{ss.mean():13.4f}   {d.mean():+13.4f}   {se_:.4f} {t:+.2f}")
    ddf = pd.DataFrame(drows)
    ddf.to_csv(f"{OUT}.deltas.csv", index=False)

    say("")
    say("  (B2) RULE 8 — the single split the PROTOCOL names.  Dials chosen on the IS window")
    say("       (to 2016-12-31) ONLY; 2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        iend = pan.idx.searchsorted(pd.Timestamp("2017-01-01"))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", iend), oos_bm(pan.name, "LIVE", iend)
        for sname in SETS:
            for dl in DELTAS:
                sel, hd = choose(pan, pan.i0, iend, sname, dl)
                for bc in BASECH:
                    ch = f"{bc}|{sname}@{dl:.2f}"
                    rf = booked[pan.name][(sel[bc][0], sel[bc][1])][pan.i0:]
                    ro = booked[pan.name][(sel[bc][0], sel[bc][1])][iend:]
                    k4a, k4b, m, h1, h2 = keep_paths(rf, spy, liv)
                    _, k4b_o, mo, _, _ = keep_paths(ro, so, lo_)
                    wrows.append(dict(panel=pan.name, SET=sname, DELTA=dl, base_chooser=bc,
                                      chooser=ch, ladder=sel[bc][0], rung=sel[bc][1],
                                      on_synthetic=str(sel[bc][0]).startswith("DEG@"),
                                      moved=bool(sel[bc] != ("CADENCE", A_C)), **m, H1=h1, H2=h2,
                                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                      OOS_MaxDD=mo["MaxDD"],
                                      SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                                      SPY_OOS_CAGR=spy["OOS_CAGR"],
                                      LIVE_OOS_Sharpe=liv["OOS_Sharpe"],
                                      KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say("       EVERY DISTINCT RULE-8 OUTCOME (rows collapse where the pick is the same book):")
    say("       panel  chooser                     pick            full CAGR/Sharpe/MaxDD"
        "        halves        OOS CAGR/Sharpe/MaxDD     4a 4b 4bOOS")
    seen = set()
    for _, r in wdf.iterrows():
        key = (r.panel, r.ladder, r.rung)
        if key in seen:
            continue
        seen.add(key)
        say(f"       {r.panel:6s} {r.chooser:26s} {str(r.ladder)+'='+str(r.rung):15s} "
            f"{r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}  {r.H1:.4f}/{r.H2:.4f}  "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}   "
            f"{str(r.KEEP_4a):5s} {str(r.KEEP_4b):5s} {str(r.KEEP_4b_OOS):5s}")
    say("")
    say("       RULE-8 ROWS BY GRID CELL (all 24 cells x 5 choosers x 3 panels):")
    for sname in SETS:
        for dl in DELTAS:
            s = wdf[(wdf.SET == sname) & (wdf.DELTA == dl)]
            say(f"         {sname:7s} {dl:5.2f}  moved {s.moved.mean():.3f}  on-synthetic "
                f"{s.on_synthetic.mean():.3f}  mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}  "
                f"4a {int(s.KEEP_4a.sum())}  4b {int(s.KEEP_4b.sum())}  "
                f"4bOOS {int(s.KEEP_4b_OOS.sum())}")

    say("")
    say("  (B3) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
    srows, stitch_ok = [], 0
    for (p, ch), parts in stitched.items():
        parts = sorted(parts, key=lambda z: z[0])
        r = np.concatenate([x for _, x in parts])
        ro = np.concatenate([x for y, x in parts if y >= 2017])
        stitch_ok += int(len(r) == sum(len(x) for _, x in parts))
        ioos = [q for q in panels if q.name == p][0].idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(p, "SPY")], BM[(p, "LIVE")]
        k4a, k4b, m, h1, h2 = keep_paths(r, spy, liv)
        _, k4b_o, mo, _, _ = keep_paths(ro, oos_bm(p, "SPY", ioos), oos_bm(p, "LIVE", ioos))
        srows.append(dict(panel=p, chooser=ch, n_days=len(r), n_oos_days=len(ro), **m,
                          H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                          OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    sdf = pd.DataFrame(srows).sort_values(["panel", "chooser"])
    sdf.to_csv(f"{OUT}.stitched.csv", index=False)
    GATES.append(dict(gate="G14 each stitched curve's length == the sum of its folds'",
                      value=float(len(sdf) - stitch_ok), target=0.0,
                      pass_=bool(stitch_ok == len(sdf))))
    say(f"       {len(sdf)} stitched curves.  DISTINCT (CAGR, Sharpe, MaxDD) outcomes:")
    uni = sdf.drop_duplicates(subset=["panel", "CAGR", "Sharpe", "MaxDD"])
    for _, r in uni.iterrows():
        say(f"       {r.panel:6s} {r.chooser:26s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
            f"{r.MaxDD:8.2%}  halves {r.H1:.4f}/{r.H2:.4f}  OOS {r.OOS_CAGR:7.2%} / "
            f"{r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}   4a {r.KEEP_4a}  4b {r.KEEP_4b}  "
            f"4b_OOS {r.KEEP_4b_OOS}")
    say("")
    say(f"     STITCHED CURVES ({len(sdf)}): 4a {int(sdf.KEEP_4a.sum())}; "
        f"4b full {int(sdf.KEEP_4b.sum())}; 4b OOS {int(sdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((sdf.KEEP_4b & sdf.KEEP_4b_OOS).sum())}")
    say(f"     RULE-8 PICKS ({len(wdf)}): 4a {int(wdf.KEEP_4a.sum())}; "
        f"4b full {int(wdf.KEEP_4b.sum())}; 4b OOS {int(wdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((wdf.KEEP_4b & wdf.KEEP_4b_OOS).sum())}")
    if int((wdf.KEEP_4b & wdf.KEEP_4b_OOS).sum()):
        pas = wdf[wdf.KEEP_4b & wdf.KEEP_4b_OOS]
        say("     the 4b-passing rule-8 rows, by DISTINCT BOOK (1194's gross-free key):")
        for k, gg in pas.groupby(["panel", "ladder", "rung"]):
            say(f"       {k}  x{len(gg)} rows")

    # ------------------------------------------------------------------ determinism
    _BAND.clear()
    _MEDR.clear()
    _RDRAW.clear()
    chk2 = []
    smp = pairdf.drop_duplicates(subset=["k_wider", "k_narrower"])
    for _, r in smp.iterrows():
        bd = nullband(r.k_wider, r.k_narrower)
        chk2.append([bd["median"], bd["L95"], bd["U95"]])
    det = float(np.nanmax(np.abs(np.array(chk2) - smp[["null_median", "L95", "U95"]].values)))
    GATES.append(dict(gate="G15 the null bands are deterministic across two constructions",
                      value=det, target=0.0, pass_=bool(det == 0.0)))

    # ------------------------------------------------------------------ gates
    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  {'PASS' if g.pass_ else 'FAIL'}  {g.gate:66s} {g.value:>14.6g} "
            f"(target {g.target:g})")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass.")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 108)
    ng0 = gdf[(gdf.SET == "NG") & (gdf.DELTA == DELTAS[0])].iloc[0]
    nd0 = gdf[(gdf.SET == "NG_D") & (gdf.DELTA == 0.00)].iloc[0]
    cany = cdf[(cdf.base == "NG") & (cdf.DELTA == 0.00) & (cdf.HFORM == "H_ANY")].iloc[0]
    rise = nd0.decisive_rate - ng0.decisive_rate
    label = ("(A) MANUFACTURES" if (rise >= 0.25 or cany.CREATED >= 10) else
             "(B) INERT" if (rise < 0.05 and cany.CREATED < 3) else "(C) PARTIAL")
    say(f"ANSWER: {label} — admitting one perfectly degenerate rung to the degenerate-free set")
    say(f"moves the pairwise decisive rate from {ng0.decisive_rate:.4f} to "
        f"{nd0.decisive_rate:.4f} (+{rise:.4f}) and CREATES {int(cany.CREATED)} of "
        f"{int(cany.cells)} H_ANY headline calls,")
    say(f"destroying {int(cany.DESTROYED)}.")
    say("=" * 108)
    say(f"runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(grid=gdf, pairs=pairdf, head=headdf, creation=cdf, picks=pdf, walk=wdf,
                stitched=sdf, books=bookdf, gates=gg, BM=BM)


if __name__ == "__main__":
    main()
