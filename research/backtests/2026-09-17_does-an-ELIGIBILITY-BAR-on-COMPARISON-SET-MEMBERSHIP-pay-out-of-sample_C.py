#!/usr/bin/env python3
"""
Idea 1226 (lane C, 2026-09-17) — does an ELIGIBILITY BAR on COMPARISON-SET MEMBERSHIP pay
out of sample?

THE PREMISE, READ FROM THE RECORD.  Idea 1223 walked a synthetic ladder whose degeneracy is a
dial into and out of the record's comparison set and found that admitting ONE perfectly
degenerate rung makes the widest-dial chooser move at 0.881 of cells instead of 0.024, and that
this costs -0.0487 of mean OOS fold Sharpe.  The obvious repair, which the queue names, is an
ELIGIBILITY BAR: admit a ladder to the comparison set only if its OWN Sharpe spread clears its
OWN null band, then re-price every chooser.  1223 proposed it; nobody has priced it.

THIS RUN PRICES IT, and asks the only question that decides whether the clause is worth writing
into PROTOCOL: does the bar pay OUT OF SAMPLE, and does it pay for a reason other than MOVING
LESS?  The record has found five times (1206, 1221, 1226, 1227, 1230) that doing nothing beats
every chooser it has built, so any rule that merely holds the anchor more often will LOOK like
it pays.  ARM D separates the two with a move-rate-matched null.

THE ADMISSION TEST.  For a ladder of k rungs on an IS window, the observed statistic is its
realised Sharpe spread R_obs = max_j S_j - min_j S_j.  Its OWN null band is built by block
bootstrap (B = 63 rows, 800 reps, block starts SHARED across every book so the cross-rung market
factor survives — 1218's finding that k independent books realise only 0.42 of the range d2(k)
predicts is exactly this dependence) and then RECENTRED: each rung's bootstrap column has its own
bootstrap mean removed, so under the null every rung has the same true Sharpe and nothing but
sampling noise separates them.  The range of the recentred draws is the null distribution of
R.  A ladder is ADMITTED iff R_obs clears the bar's quantile of that distribution.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  ADMISSION BAR    {A_NONE, A_POS, A_MED, A_90, A_95, A_99}
                   A_NONE admits everything (the record's current habit, the control).
                   A_POS admits iff R_obs > 0 (the cheapest bar that exists).
                   A_MED / A_90 / A_95 / A_99 admit iff R_obs clears the 50th / 90th / 95th /
                   99th percentile of the ladder's own recentred null range.
  COMPARISON SET   {NG, NG_D, ALL4, ALL4_D}
                   NG     = {N, H, CADENCE}           1223's degenerate-free set
                   ALL4   = NG + GROSS                the record's own set (GROSS is degenerate
                                                      for the reason 1189 gives: Sharpe is
                                                      invariant to gross at a 0% cash rate)
                   NG_D   = NG   + DEG                NG plus a PERFECTLY degenerate rung
                   ALL4_D = ALL4 + DEG                both degenerate ladders present

  24 cells, EVERY ONE PUBLISHED.  DEG is 1223's synthetic ladder at delta = 0.00 — six rungs that
  are the ANCHOR weight frame bit for bit, so its spread is EXACTLY 0 by construction (gate G2).

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the 14 folds; the three
HEADLINE FORMS {H_RUNNERUP, H_NARROWEST, H_ANY} inherited whole from 1223; the two controls
{CH_RAW, CH_ANCHOR}; the 4a and 4b legs; the IS and OOS windows.

Frozen at the record's construction, inherited from 1207/1214/1223 unchanged: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 /
CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up 260 rows, the
conditional two-sided null band B_IID95 and its Monte-Carlo construction, the 14 calendar folds.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every rule-8 pick and every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_does-an-ELIGIBILITY-BAR-on-COMPARISON-SET-MEMBERSHIP-pay-out-of-sample_C.py
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
SLUG = "does-an-ELIGIBILITY-BAR-on-COMPARISON-SET-MEMBERSHIP-pay-out-of-sample"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
PRIOR1223 = Path(__file__).resolve().parent / (
    "2026-09-17_does-a-DEGENERATE-LADDER-in-the-COMPARISON-SET-MANUFACTURE-decisive-"
    "WIDEST-DIAL-calls_C")

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"

NRUNGS = [5, 10, 15, 20, 30, 40]
DEG = "DEG@0.00"
LAD = {
    "N": NRUNGS,
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
    DEG: list(NRUNGS),
}
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2, DEG: 6}

# ---- DIAL 1: the admission bar
BARS = ["A_NONE", "A_POS", "A_MED", "A_90", "A_95", "A_99"]
BARQ = {"A_MED": 0.50, "A_90": 0.90, "A_95": 0.95, "A_99": 0.99}

# ---- DIAL 2: the comparison set
NG3 = ["N", "H", "CADENCE"]
ALL4 = ["N", "H", "GROSS", "CADENCE"]
SETS = ["NG", "NG_D", "ALL4", "ALL4_D"]
SETLAD = {"NG": NG3, "NG_D": NG3 + [DEG], "ALL4": ALL4, "ALL4_D": ALL4 + [DEG]}

BARFORMS = ["B_RAW", "B_POINT", "B_MED", "B_IID95", "B_BOOT95"]
HFORMS = ["H_RUNNERUP", "H_NARROWEST", "H_ANY"]
BASECH = HFORMS + ["CH_RAW", "CH_ANCHOR"]
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
NMC = 1_500_000
MC_SEED = 12141214            # 1214's / 1223's, so the bands are literally the same numbers
BOOT_B, BOOT_REPS, BOOT_SEED = 63, 800, 214214
NL_REPS, NL_SEED = 4000, 12261226

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


# ==================================================================== the pair null (1214/1223)
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
    V = (M / I) if I > 0 else np.inf
    if form == "B_RAW":
        return "W"
    if form == "B_POINT":
        return "W" if M > I else "N"
    if form == "B_MED":
        return "W" if V > band["median"] else "N"
    if form == "B_IID95":
        return "W" if V > band["U95"] else ("N" if V < band["L95"] else "TIE")
    if form == "B_BOOT95":
        if not np.isfinite(se_log) or se_log <= 0:
            return "TIE"
        lv = np.log(V) if V > 0 else -np.inf
        z = (lv - np.log(band["median"])) / se_log
        return "W" if z > 1.959964 else ("N" if z < -1.959964 else "TIE")
    raise ValueError(form)


# ==================================================================== panels / runner (1207/1223)
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
    say("IDEA 1226 (lane C, 2026-09-17) — does an ELIGIBILITY BAR on COMPARISON-SET MEMBERSHIP")
    say("pay out of sample?")
    say("=" * 108)

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("=" * 108)
    say("ARM 0 — WHAT THE BAR DOES BEFORE ANY PRICE IS READ")
    say("=" * 108)
    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in (2, 4, 6, 10))
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    say(f"  d2(k) MC at {NMC:,} draws reproduces Hartley to {mc_err:.3e}.")
    say("")
    say("  (0a) A PERFECTLY DEGENERATE LADDER FAILS THE CHEAPEST BAR THAT EXISTS.  Its rungs are")
    say("       the same book, so every bootstrap draw gives the same Sharpe at every rung: the")
    say("       recentred null range is 0 in EVERY rep AND the observed spread is 0.  R_obs > 0")
    say("       is FALSE, so A_POS already excludes it — and A_MED / A_90 / A_95 / A_99, which")
    say("       are strictly stronger, exclude it too.  THE EXPENSIVE BAR IS NOT NEEDED FOR THE")
    say("       CASE 1223 BUILT.  What the expensive bars can still do is exclude ladders whose")
    say("       spread is real but not distinguishable from their own sampling noise — GROSS,")
    say("       whose spread 1214 measured at 0.0011-0.0034, is the live candidate.")
    say("")
    say("  (0b) THE BAR IS ALSO A DO-NOTHING DIAL, AND THAT IS THE WHOLE DIFFICULTY.  Excluding")
    say("       ladders shrinks the comparison set; a set of 0 or 1 ladder has no pair, so every")
    say("       headline form returns TIE and the chooser HOLDS THE ANCHOR.  The record has found")
    say("       five times that holding the anchor beats every chooser out of sample, so a bar")
    say("       that merely holds more often WILL look like it pays.  ARM D prices the bar")
    say("       against a null that moves exactly as often as it does (1227's NL_PERM).")

    # ------------------------------------------------------------------ panels and books
    say("")
    say("=" * 108)
    say("ARM A — THE LADDERS AND THE ADMISSION TEST")
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
    deg_err = 0.0
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
        # ---- the PERFECTLY degenerate ladder: six rungs that are the anchor book bit for bit
        anchor_book = nrun(pan, A_G * anchor_frame, "W")
        for N in NRUNGS:
            books[(DEG, N)] = nrun(pan, A_G * anchor_frame, "W")
            deg_err = max(deg_err, float(np.nanmax(np.abs(books[(DEG, N)] - anchor_book))))
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        RM[pan.name] = np.column_stack([books[k] for k in BOOKKEY])
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built ({len(NRUNGS)} of them the DEG rung).")

    GATES.append(dict(gate="G2 every DEG rung == the anchor book, bit for bit", value=deg_err,
                      target=1e-15, pass_=bool(deg_err <= 1e-15)))

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
    say(f"    G2 {deg_err:.3e}  G4 {g4:.3e}  G5 live U56 MaxDD {lm:.4%}")

    # ---- block-bootstrap machinery (shared block starts across books: dependence survives)
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

    # ---- THE ADMISSION TEST: observed spread vs the ladder's OWN recentred null range
    _ADMCACHE: dict = {}

    def admit_of(p, lo, hi):
        """{ladder: dict(R_obs, q50, q90, q95, q99, admitted-by-bar...)} on the window [lo,hi)."""
        key = (p, lo, hi)
        if key in _ADMCACHE:
            return _ADMCACHE[key]
        S = boot_sharpes(p, lo, hi)
        out = {}
        for lad, ii in LADIDX.items():
            v = [sharpe(RM[p][lo:hi, j]) for j in ii]
            v = [x for x in v if np.isfinite(x)]
            R = (max(v) - min(v)) if len(v) > 1 else np.nan
            d = dict(R_obs=R, q50=np.nan, q90=np.nan, q95=np.nan, q99=np.nan, nrep=0)
            if S is not None:
                Vb = S[:, ii]
                V0 = Vb - np.nanmean(Vb, axis=0)[None, :]      # recentre: equal true Sharpe
                rng_ = np.nanmax(V0, axis=1) - np.nanmin(V0, axis=1)
                rng_ = rng_[np.isfinite(rng_)]
                if len(rng_) > 10:
                    d.update(q50=float(np.quantile(rng_, 0.50)),
                             q90=float(np.quantile(rng_, 0.90)),
                             q95=float(np.quantile(rng_, 0.95)),
                             q99=float(np.quantile(rng_, 0.99)), nrep=len(rng_))
            for bar in BARS:
                if bar == "A_NONE":
                    ok = bool(np.isfinite(R))
                elif bar == "A_POS":
                    ok = bool(np.isfinite(R) and R > 0)
                else:
                    q = d[{"A_MED": "q50", "A_90": "q90", "A_95": "q95", "A_99": "q99"}[bar]]
                    ok = bool(np.isfinite(R) and np.isfinite(q) and R > q)
                d[bar] = ok
            out[lad] = d
        _ADMCACHE[key] = out
        return out

    _SPCACHE: dict = {}

    def spread_of(pan, lad, lo, hi):
        key = (pan.name, lad, lo, hi)
        if key not in _SPCACHE:
            v = [sharpe(booked[pan.name][(lad, r)][lo:hi]) for r in LAD[lad]]
            v = [x for x in v if np.isfinite(x)]
            _SPCACHE[key] = (max(v) - min(v)) if len(v) > 1 else np.nan
        return _SPCACHE[key]

    def pick_of(pan, lad, lo, hi):
        v = [(sharpe(booked[pan.name][(lad, r)][lo:hi]), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

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
    say("")
    say(f"    {nfold} (panel, fold) cells = 3 panels x "
        f"{len(folds_by_panel['U56'])} folds ({FOLD_YEARS[0]}-{FOLD_YEARS[-1]}).")

    # ---- G3: the DEG ladder's observed spread is exactly 0 at every cell
    zerr = 0.0
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            zerr = max(zerr, abs(spread_of(pan, DEG, lo, hi)))
    GATES.append(dict(gate="G3 the DEG ladder's IS spread is exactly 0 at every cell",
                      value=zerr, target=0.0, pass_=bool(zerr == 0.0)))

    # ---- ADMISSION TABLE
    say("")
    say("  (A1) THE ADMISSION TEST AT EVERY (panel, fold, ladder).  R_obs is the ladder's realised")
    say("       IS Sharpe spread; q50/q90/q95/q99 are quantiles of its OWN recentred null range")
    say(f"       ({BOOT_REPS} block-bootstrap reps, B = {BOOT_B} rows, starts SHARED across books).")
    admrows = []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            A = admit_of(pan.name, lo, hi)
            for lad in LAD:
                d = A[lad]
                admrows.append(dict(panel=pan.name, fold=y, ladder=lad, k=LADK[lad],
                                    R_obs=d["R_obs"], q50=d["q50"], q90=d["q90"],
                                    q95=d["q95"], q99=d["q99"],
                                    ratio_R_over_q95=(d["R_obs"] / d["q95"])
                                    if np.isfinite(d["q95"]) and d["q95"] > 0 else np.nan,
                                    **{b: d[b] for b in BARS}))
    admdf = pd.DataFrame(admrows)
    admdf.to_csv(f"{OUT}.admission.csv", index=False)
    say("")
    say("       ADMISSION RATE BY LADDER AND BAR (over the 42 (panel, fold) cells):")
    say("")
    say("       ladder    k   med R_obs   med q95    med R/q95   " + "  ".join(f"{b:>7s}" for b in BARS))
    for lad in LAD:
        s = admdf[admdf.ladder == lad]
        say(f"       {lad:9s} {LADK[lad]:2d}   {np.nanmedian(s.R_obs):9.4f}  "
            f"{np.nanmedian(s.q95):9.4f}  {np.nanmedian(s.ratio_R_over_q95):10.4f}   "
            + "  ".join(f"{s[b].mean():7.3f}" for b in BARS))
    degadm = int(admdf[(admdf.ladder == DEG)][BARS[1:]].values.sum())
    GATES.append(dict(gate="G8 the DEG ladder is admitted by NO bar above A_NONE",
                      value=float(degadm), target=0.0, pass_=bool(degadm == 0)))
    nadm = admdf[admdf.ladder == "A_NONE"] if False else None
    del nadm

    say("")
    say("       ADMITTED SET SIZE BY (set, bar), mean over the 42 cells:")
    say("")
    say("       set      " + "  ".join(f"{b:>8s}" for b in BARS))
    szrows = []
    for sname in SETS:
        sz = []
        for bar in BARS:
            vals = []
            for pan in panels:
                for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
                    A = admit_of(pan.name, lo, hi)
                    vals.append(sum(1 for lad in SETLAD[sname] if A[lad][bar]))
            sz.append(float(np.mean(vals)))
            szrows.append(dict(SET=sname, BAR=bar, mean_size=float(np.mean(vals)),
                               min_size=int(np.min(vals)), max_size=int(np.max(vals)),
                               frac_lt2=float(np.mean(np.array(vals) < 2))))
        say(f"       {sname:7s}  " + "  ".join(f"{x:8.3f}" for x in sz))
    pd.DataFrame(szrows).to_csv(f"{OUT}.setsize.csv", index=False)

    # ------------------------------------------------------------------ ARM B
    say("")
    say("=" * 108)
    say("ARM B — THE 24-CELL GRID: WHAT THE BAR DOES TO THE HEADLINE CALL")
    say("=" * 108)

    def pairs_of(pan, lo, hi, lads, se):
        sp = {lad: spread_of(pan, lad, lo, hi) for lad in lads}
        rows = []
        for a in lads:
            for b in lads:
                if a == b or not (np.isfinite(sp[a]) and np.isfinite(sp[b])):
                    continue
                if sp[a] < sp[b]:
                    continue
                if sp[a] == sp[b] and a > b:
                    continue
                M_ = (sp[a] / sp[b]) if sp[b] > 0 else (np.inf if sp[a] > 0 else 1.0)
                I_ = d2(LADK[a]) / d2(LADK[b])
                bd = nullband(LADK[a], LADK[b])
                sel = float(np.nanstd(se[a] - se[b], ddof=1)) if se else np.nan
                row = dict(wider=a, narrower=b, sp_w=sp[a], sp_n=sp[b], MULTIPLE=M_,
                           INFLATION=I_, V=M_ / I_, null_median=bd["median"],
                           L95=bd["L95"], U95=bd["U95"], SE_logM=sel,
                           involves_DEG=bool(a == DEG or b == DEG),
                           involves_GROSS=bool(a == "GROSS" or b == "GROSS"))
                for form in BARFORMS:
                    row[form] = call_of(form, M_, I_, bd, sel)
                rows.append(row)
        return sp, rows

    def headline(pan, lo, hi, lads, se, form="B_IID95"):
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
        return out

    def admitted(pan, lo, hi, sname, bar):
        A = admit_of(pan.name, lo, hi)
        return [lad for lad in SETLAD[sname] if A[lad][bar]]

    headrows, pairrows = [], []
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            se = boot_logspread_se(pan.name, lo, hi)
            for sname in SETS:
                for bar in BARS:
                    lads = admitted(pan, lo, hi, sname, bar)
                    hd = headline(pan, lo, hi, lads, se) if len(lads) >= 2 else None
                    _, prs = pairs_of(pan, lo, hi, lads, se) if len(lads) >= 2 else ({}, [])
                    for r in prs:
                        pairrows.append(dict(panel=pan.name, fold=y, SET=sname, BAR=bar, **r))
                    for hf in HFORMS:
                        if hd is None:
                            c, named, V = "TIE", None, np.nan
                        else:
                            c, named, V = hd[hf]
                        headrows.append(dict(panel=pan.name, fold=y, SET=sname, BAR=bar,
                                             HFORM=hf, call=c, named=named, V=V,
                                             n_admitted=len(lads)))
    pairdf = pd.DataFrame(pairrows)
    headdf = pd.DataFrame(headrows)
    pairdf.to_csv(f"{OUT}.pairs.csv", index=False)
    headdf.to_csv(f"{OUT}.headline.csv", index=False)
    say(f"  {len(pairdf):,} pair rows and {len(headdf):,} headline rows over "
        f"{len(SETS)} sets x {len(BARS)} bars x {nfold} (panel, fold) cells.")

    # ---- G9: replay 1223's A_NONE pairs (the control must reproduce the record)
    try:
        pr = pd.read_csv(f"{PRIOR1223}.pairs.csv")
        pr = pr[(pr.SET == "ALL4") & (pr.DELTA == 0.00)]
        mine = pairdf[(pairdf.SET == "ALL4") & (pairdf.BAR == "A_NONE")]
        mg = pr.merge(mine, on=["panel", "fold", "wider", "narrower"], suffixes=("_23", ""))
        g9 = float(np.nanmax(np.abs(mg.MULTIPLE_23.values - mg.MULTIPLE.values)))
        ok9 = bool(len(mg) == len(pr) == len(mine) and g9 < 1e-12)
        say(f"  1223 ALL4 replay: {len(mg)} rows, max |dMULTIPLE| {g9:.3e} — "
            f"{'PASS' if ok9 else 'FAIL'}.")
    except Exception as e:                                        # pragma: no cover
        g9, ok9 = 9e9, False
        say(f"  (1223 replay unavailable: {e})")
    GATES.append(dict(gate="G9 the A_NONE / ALL4 pairs replay 1223's committed table",
                      value=g9, target=1e-12, pass_=ok9))

    say("")
    say("  (B1) DECISIVE RATE AND HEADLINE CALLS AT EVERY GRID POINT.  decisive = the bar names")
    say("       a widest dial (W or N) at B_IID95; TIE = it declines or no pair exists.")
    say("")
    say("       set      bar       pairs  decisive   rate    H_RUNNERUP  H_NARROWEST   H_ANY   "
        "names DEG  names GROSS")
    grows = []
    for sname in SETS:
        for bar in BARS:
            sub = pairdf[(pairdf.SET == sname) & (pairdf.BAR == bar)]
            hh = headdf[(headdf.SET == sname) & (headdf.BAR == bar)]
            dec = (sub.B_IID95 != "TIE") if len(sub) else pd.Series(dtype=bool)
            g = dict(SET=sname, BAR=bar, pairs=len(sub),
                     decisive=int(dec.sum()) if len(sub) else 0,
                     decisive_rate=float(dec.mean()) if len(sub) else np.nan,
                     names_DEG=int(hh.named.astype(str).eq(DEG).sum()),
                     names_GROSS=int(hh.named.astype(str).eq("GROSS").sum()),
                     mean_admitted=float(hh.n_admitted.mean()))
            for f in BARFORMS:
                g[f"rate_{f}"] = float((sub[f] != "TIE").mean()) if len(sub) else np.nan
            for hf in HFORMS:
                hs = hh[hh.HFORM == hf]
                g[f"head_{hf}_rate"] = float((hs.call != "TIE").mean())
            grows.append(g)
            say(f"       {sname:7s}  {bar:8s} {len(sub):6d} {g['decisive']:9d}  "
                f"{(g['decisive_rate'] if np.isfinite(g['decisive_rate'] or np.nan) else float('nan')):.4f}"
                f"     {g['head_H_RUNNERUP_rate']:.4f}      {g['head_H_NARROWEST_rate']:.4f}"
                f"     {g['head_H_ANY_rate']:.4f}   {g['names_DEG']:7d}  {g['names_GROSS']:9d}")
    gdf = pd.DataFrame(grows)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)

    say("")
    say("  (B2) THE SAME GRID THROUGH ALL FIVE BAR FORMS (pairwise decisive rate):")
    say("")
    say("       set      bar        B_RAW   B_POINT   B_MED   B_IID95  B_BOOT95")
    for _, g in gdf.iterrows():
        say(f"       {g.SET:7s}  {g.BAR:8s}  {g.rate_B_RAW:.4f}  {g.rate_B_POINT:.4f}   "
            f"{g.rate_B_MED:.4f}  {g.rate_B_IID95:.4f}   {g.rate_B_BOOT95:.4f}")

    # ------------------------------------------------------------------ ARM C
    say("")
    say("=" * 108)
    say("ARM C — PRICING THE BAR.  RULE 8 WALK-FORWARD AND BOTH KEEP PATHS.")
    say("=" * 108)

    def choose(pan, lo, hi, sname, bar):
        lads = admitted(pan, lo, hi, sname, bar)
        se = boot_logspread_se(pan.name, lo, hi)
        hd = headline(pan, lo, hi, lads, se) if len(lads) >= 2 else None
        sp = {lad: spread_of(pan, lad, lo, hi) for lad in lads}
        good = {k: v for k, v in sp.items() if np.isfinite(v)}
        raw_w = max(good, key=good.get) if good else None
        out = {"CH_RAW": (raw_w, pick_of(pan, raw_w, lo, hi)) if raw_w else ("CADENCE", A_C),
               "CH_ANCHOR": ("CADENCE", A_C)}
        for hf in HFORMS:
            if hd is None:
                out[hf] = ("CADENCE", A_C)
                continue
            c, named, _ = hd[hf]
            out[hf] = ("CADENCE", A_C) if (c == "TIE" or named is None) \
                else (named, pick_of(pan, named, lo, hi))
        return out

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
            brows.append(dict(panel=pan.name, ladder=lad, rung=rung, **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4b_o))
    bookdf = pd.DataFrame(brows)
    bookdf.to_csv(f"{OUT}.books.csv", index=False)
    uniq_books = bookdf.drop_duplicates(subset=["panel", "CAGR", "Sharpe", "MaxDD"])
    say(f"    {len(bookdf)} rung books ({len(uniq_books)} DISTINCT by (panel, CAGR, Sharpe, "
        f"MaxDD) — 1194's key): 4a {int(bookdf.KEEP_4a.sum())}; "
        f"4b full {int(bookdf.KEEP_4b.sum())}; 4b OOS {int(bookdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bookdf.KEEP_4b & bookdf.KEEP_4b_OOS).sum())}")
    say(f"    on DISTINCT books: 4a {int(uniq_books.KEEP_4a.sum())}; "
        f"4b full {int(uniq_books.KEEP_4b.sum())}; 4b OOS {int(uniq_books.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((uniq_books.KEEP_4b & uniq_books.KEEP_4b_OOS).sum())}")

    say("")
    say("  (C1) THE ROLLING WALK — one calendar year of OOS per fold, IS = warm-up to the day")
    say("       before the fold.  Every choice made on the IS window ONLY.")
    prows, stitched = [], {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for sname in SETS:
                for bar in BARS:
                    sel = choose(pan, lo, hi, sname, bar)
                    for bc in BASECH:
                        ch = f"{bc}|{sname}|{bar}"
                        r = booked[pan.name][(sel[bc][0], sel[bc][1])][o0:o1]
                        stitched.setdefault((pan.name, ch), []).append((y, r))
                        prows.append(dict(panel=pan.name, fold=y, SET=sname, BAR=bar,
                                          base_chooser=bc, chooser=ch, ladder=sel[bc][0],
                                          rung=sel[bc][1],
                                          moved=bool(sel[bc] != ("CADENCE", A_C)),
                                          OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r),
                                          OOS_MaxDD=mdd(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv_anchor = float(pdf[pdf.base_chooser == "CH_ANCHOR"].moved.mean())
    GATES.append(dict(gate="G10 CH_ANCHOR move rate == 0 (inert to both dials)",
                      value=mv_anchor, target=0.0, pass_=bool(mv_anchor == 0.0)))
    say(f"       {len(pdf):,} pick-cells = {nfold} (panel, fold) x {len(SETS)} sets x "
        f"{len(BARS)} bars x {len(BASECH)} choosers.")

    # ---- G11: a MOVE onto a book equivalent to the anchor is not a move (1230's correction)
    anchor_ret = {p: booked[p][("CADENCE", A_C)] for p in booked}
    eqkeys = {}
    for p in booked:
        eqkeys[p] = {k for k, v in booked[p].items()
                     if float(np.nanmax(np.abs(v - anchor_ret[p]))) <= 1e-15}
    pdf["moved_KEY"] = pdf.moved
    pdf["moved_VALUE"] = [not ((r.ladder, r.rung) in eqkeys[r.panel])
                          for r in pdf.itertuples()]
    say(f"       1230's correction applied: {len(eqkeys['U56'])} of {len(BOOKKEY)} U56 book keys "
        f"are the ANCHOR bit for bit, so a 'move' onto one is a NO-OP.")
    say(f"       move rate on KEYS {pdf.moved_KEY.mean():.4f} vs on VALUES "
        f"{pdf.moved_VALUE.mean():.4f} (overstatement "
        f"{pdf.moved_KEY.mean() - pdf.moved_VALUE.mean():+.4f} of pick-cells).")
    GATES.append(dict(gate="G11 the VALUE move rate never exceeds the KEY move rate",
                      value=float(pdf.moved_VALUE.mean() - pdf.moved_KEY.mean()), target=0.0,
                      pass_=bool(pdf.moved_VALUE.mean() <= pdf.moved_KEY.mean() + 1e-12)))
    pdf.to_csv(f"{OUT}.picks.csv", index=False)

    say("")
    say("       MOVE RATE AND MEAN OOS SHARPE AT EVERY GRID POINT, PAIRED vs CH_ANCHOR")
    say("       (SE clustered on the 14 folds, which tile the tape without overlap):")
    say("")
    say("       set      bar       chooser       move(KEY/VALUE)   mean OOS Sharpe   "
        "d vs ANCHOR    SE      t")
    anch = pdf[pdf.base_chooser == "CH_ANCHOR"].groupby(["panel", "fold"]).OOS_Sharpe.first()
    drows = []
    for sname in SETS:
        for bar in BARS:
            for bc in BASECH:
                s = pdf[(pdf.SET == sname) & (pdf.BAR == bar) & (pdf.base_chooser == bc)]
                ss = s.set_index(["panel", "fold"]).OOS_Sharpe
                d = (ss - anch).dropna()
                fm = d.groupby(level=1).mean()
                se_ = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
                t = d.mean() / se_ if se_ and se_ > 0 else 0.0
                drows.append(dict(SET=sname, BAR=bar, base_chooser=bc,
                                  move_rate_KEY=float(s.moved_KEY.mean()),
                                  move_rate_VALUE=float(s.moved_VALUE.mean()),
                                  mean_OOS_Sharpe=float(ss.mean()),
                                  delta_vs_ANCHOR=float(d.mean()), SE=se_, t=t))
                say(f"       {sname:7s}  {bar:8s}  {bc:12s} {s.moved_KEY.mean():.3f}/"
                    f"{s.moved_VALUE.mean():.3f}     {ss.mean():13.4f}   {d.mean():+10.4f}   "
                    f"{se_:.4f} {t:+.2f}")
    ddf = pd.DataFrame(drows)
    ddf.to_csv(f"{OUT}.deltas.csv", index=False)

    # ------------------------------------------------------------------ ARM D
    say("")
    say("=" * 108)
    say("ARM D — DOES THE BAR PAY FOR A REASON OTHER THAN MOVING LESS?")
    say("=" * 108)
    say("")
    say("  THE NULL (1227's NL_PERM, count-matched).  For each (set, bar, form) the chooser makes")
    say("  a decision at each of the 42 cells: MOVE to some book, or HOLD the anchor.  The null")
    say("  keeps the chooser's OWN destination multiset and its OWN move COUNT and re-deals the")
    say("  destinations to RANDOMLY chosen cells.  If the observed mean OOS Sharpe sits inside")
    say("  that band, the bar buys nothing beyond the number of times it declines to move.")
    say("")
    cells = [(p, y) for p in folds_by_panel for (y, *_x) in folds_by_panel[p]]
    cellidx = {c: i for i, c in enumerate(cells)}
    oos_of = {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for k in BOOKKEY:
                oos_of[(pan.name, y, k)] = sharpe(booked[pan.name][k][o0:o1])
    rng = np.random.default_rng(NL_SEED)
    nlrows = []
    say("       set      bar       form           moves  obs mean   null mean   null SD   "
        "gap      p")
    for sname in SETS:
        for bar in BARS:
            for bc in BASECH:
                s = pdf[(pdf.SET == sname) & (pdf.BAR == bar) & (pdf.base_chooser == bc)]
                obs = float(s.OOS_Sharpe.mean())
                dest = [(r.ladder, r.rung) for r in s.itertuples() if r.moved_VALUE]
                nmv = len(dest)
                base = np.array([oos_of[(r.panel, r.fold, ("CADENCE", A_C))]
                                 for r in s.itertuples()], float)
                if nmv == 0:
                    nlrows.append(dict(SET=sname, BAR=bar, base_chooser=bc, n_moves=0,
                                       obs=obs, null_mean=obs, null_sd=0.0, gap=0.0, p=np.nan))
                    say(f"       {sname:7s}  {bar:8s}  {bc:12s} {0:6d}  {obs:8.4f}  "
                        f"{obs:10.4f}  {0.0:8.4f}  {0.0:+7.4f}   n/a")
                    continue
                cellkeys = [(r.panel, r.fold) for r in s.itertuples()]
                dvals = np.array([[oos_of[(p_, y_, dk)] for dk in dest]
                                  for (p_, y_) in cellkeys], float)      # cells x destinations
                nc = len(cellkeys)
                draws = np.empty(NL_REPS)
                for rep in range(NL_REPS):
                    perm = rng.permutation(nc)[:nmv]
                    dperm = rng.permutation(nmv)
                    v = base.copy()
                    v[perm] = dvals[perm, dperm]
                    draws[rep] = v.mean()
                nm_, nsd = float(draws.mean()), float(draws.std(ddof=1))
                p_ = float((draws >= obs).mean())
                nlrows.append(dict(SET=sname, BAR=bar, base_chooser=bc, n_moves=nmv, obs=obs,
                                   null_mean=nm_, null_sd=nsd, gap=obs - nm_, p=p_))
                say(f"       {sname:7s}  {bar:8s}  {bc:12s} {nmv:6d}  {obs:8.4f}  "
                    f"{nm_:10.4f}  {nsd:8.4f}  {obs-nm_:+7.4f}  {p_:.4f}")
    nldf = pd.DataFrame(nlrows)
    nldf.to_csv(f"{OUT}.null.csv", index=False)
    live = nldf[nldf.n_moves > 0]
    say("")
    say(f"       Over the {len(live)} (set, bar, chooser) cells that move at all: the observed")
    say(f"       mean sits ABOVE its own count-matched null at {int((live.gap > 0).sum())} of "
        f"{len(live)}; mean gap {live.gap.mean():+.4f}; p < 0.05 at "
        f"{int((live.p < 0.05).sum())}; p < 0.05 expected by chance "
        f"{0.05*len(live):.1f}.")
    GATES.append(dict(gate="G12 the count-matched null is computed at every moving cell",
                      value=float(live.p.notna().mean()), target=1.0,
                      pass_=bool(live.p.notna().all())))

    # ------------------------------------------------------------------ ARM E: rule 8
    say("")
    say("=" * 108)
    say("ARM E — RULE 8: THE SINGLE SPLIT THE PROTOCOL NAMES")
    say("=" * 108)
    say("  Both dials AND the chooser chosen on the IS window (to 2016-12-31) ONLY;")
    say("  2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        iend = pan.idx.searchsorted(pd.Timestamp("2017-01-01"))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", iend), oos_bm(pan.name, "LIVE", iend)
        for sname in SETS:
            for bar in BARS:
                sel = choose(pan, pan.i0, iend, sname, bar)
                for bc in BASECH:
                    ch = f"{bc}|{sname}|{bar}"
                    key = (sel[bc][0], sel[bc][1])
                    rf = booked[pan.name][key][pan.i0:]
                    ro = booked[pan.name][key][iend:]
                    k4a, k4b, m, h1, h2 = keep_paths(rf, spy, liv)
                    _, k4b_o, mo, _, _ = keep_paths(ro, so, lo_)
                    wrows.append(dict(panel=pan.name, SET=sname, BAR=bar, base_chooser=bc,
                                      chooser=ch, ladder=key[0], rung=key[1],
                                      moved_KEY=bool(key != ("CADENCE", A_C)),
                                      moved_VALUE=bool(key not in eqkeys[pan.name]),
                                      **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                      OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                      SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                                      SPY_OOS_CAGR=spy["OOS_CAGR"],
                                      SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                                      LIVE_OOS_Sharpe=liv["OOS_Sharpe"],
                                      KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

    say("")
    say("  EVERY DISTINCT RULE-8 OUTCOME (rows collapse where the pick is the same book):")
    say("  panel  pick            full CAGR/Sharpe/MaxDD       halves         "
        "OOS CAGR/Sharpe/MaxDD      4a   4b   4bOOS")
    seen = set()
    for _, r in wdf.sort_values(["panel", "ladder", "rung"]).iterrows():
        key = (r.panel, r.ladder, r.rung)
        if key in seen:
            continue
        seen.add(key)
        say(f"  {r.panel:6s} {str(r.ladder)+'='+str(r.rung):15s} "
            f"{r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:8.2%}  {r.H1:.4f}/{r.H2:.4f}  "
            f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:8.2%}   "
            f"{str(r.KEEP_4a):5s} {str(r.KEEP_4b):5s} {str(r.KEEP_4b_OOS):5s}")

    say("")
    say("  RULE-8 ROWS BY GRID CELL (all 24 cells x 5 choosers x 3 panels):")
    say("       set      bar       moved(K/V)   mean OOS Sharpe   4a   4b   4bOOS")
    for sname in SETS:
        for bar in BARS:
            s = wdf[(wdf.SET == sname) & (wdf.BAR == bar)]
            say(f"       {sname:7s}  {bar:8s}  {s.moved_KEY.mean():.3f}/"
                f"{s.moved_VALUE.mean():.3f}      {s.OOS_Sharpe.mean():13.4f}  "
                f"{int(s.KEEP_4a.sum()):4d} {int(s.KEEP_4b.sum()):4d} "
                f"{int(s.KEEP_4b_OOS.sum()):6d}")

    say("")
    say("  (E1) THE STITCHED DEPLOYABLE CURVES — each chooser's own fold picks, concatenated.")
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
    GATES.append(dict(gate="G13 each stitched curve's length == the sum of its folds'",
                      value=float(len(sdf) - stitch_ok), target=0.0,
                      pass_=bool(stitch_ok == len(sdf))))
    uni = sdf.drop_duplicates(subset=["panel", "CAGR", "Sharpe", "MaxDD"])
    say(f"       {len(sdf)} stitched curves, {len(uni)} DISTINCT outcomes:")
    for _, r in uni.iterrows():
        say(f"       {r.panel:6s} {r.chooser:24s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
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
            r0 = gg.iloc[0]
            say(f"       {k}  x{len(gg)} rows  full {r0.CAGR:7.2%} / {r0.Sharpe:.4f} / "
                f"{r0.MaxDD:8.2%}  OOS {r0.OOS_CAGR:7.2%} / {r0.OOS_Sharpe:.4f} / "
                f"{r0.OOS_MaxDD:8.2%}")

    # ---- the headline number: does the bar buy OOS Sharpe?
    say("")
    say("  (E2) THE HEADLINE — MEAN OOS SHARPE BY BAR, POOLED OVER SETS AND HEADLINE FORMS")
    say("       (the 3 headline forms only; CH_RAW and CH_ANCHOR reported beside them).")
    say("")
    say("       bar       rolling folds (42 cells x 4 sets x 3 forms)     rule 8 (3 panels)")
    say("                 mean OOS Sh   d vs A_NONE   move(V)             mean OOS Sh   d vs A_NONE")
    hrows = []
    for bar in BARS:
        a = pdf[(pdf.BAR == bar) & (pdf.base_chooser.isin(HFORMS))]
        b = wdf[(wdf.BAR == bar) & (wdf.base_chooser.isin(HFORMS))]
        a0 = pdf[(pdf.BAR == "A_NONE") & (pdf.base_chooser.isin(HFORMS))]
        b0 = wdf[(wdf.BAR == "A_NONE") & (wdf.base_chooser.isin(HFORMS))]
        hrows.append(dict(BAR=bar, roll_mean=float(a.OOS_Sharpe.mean()),
                          roll_delta=float(a.OOS_Sharpe.mean() - a0.OOS_Sharpe.mean()),
                          roll_move_VALUE=float(a.moved_VALUE.mean()),
                          w8_mean=float(b.OOS_Sharpe.mean()),
                          w8_delta=float(b.OOS_Sharpe.mean() - b0.OOS_Sharpe.mean())))
        h = hrows[-1]
        say(f"       {bar:8s}  {h['roll_mean']:11.4f}   {h['roll_delta']:+11.4f}   "
            f"{h['roll_move_VALUE']:.3f}               {h['w8_mean']:11.4f}   "
            f"{h['w8_delta']:+11.4f}")
    anch_roll = float(pdf[pdf.base_chooser == "CH_ANCHOR"].OOS_Sharpe.mean())
    anch_w8 = float(wdf[wdf.base_chooser == "CH_ANCHOR"].OOS_Sharpe.mean())
    say(f"       {'ANCHOR':8s}  {anch_roll:11.4f}   (do nothing)              "
        f"      {anch_w8:11.4f}   (do nothing)")
    hdf = pd.DataFrame(hrows)
    hdf.to_csv(f"{OUT}.headline_bar.csv", index=False)
    best = hdf.iloc[int(np.argmax(hdf.roll_mean.values))]
    say("")
    say(f"       BEST BAR ON THE ROLLING WALK: {best.BAR} at {best.roll_mean:.4f} "
        f"({best.roll_delta:+.4f} vs the record's habit A_NONE), still "
        f"{best.roll_mean - anch_roll:+.4f} against DOING NOTHING ({anch_roll:.4f}).")

    # ------------------------------------------------------------------ determinism
    _BAND.clear()
    _MEDR.clear()
    _RDRAW.clear()
    chk = []
    smp = pairdf.drop_duplicates(subset=["wider", "narrower"]).head(12)
    for _, r in smp.iterrows():
        bd = nullband(LADK[r.wider], LADK[r.narrower])
        chk.append([bd["median"], bd["L95"], bd["U95"]])
    det = float(np.nanmax(np.abs(np.array(chk) - smp[["null_median", "L95", "U95"]].values)))
    GATES.append(dict(gate="G14 the null bands are deterministic across two constructions",
                      value=det, target=0.0, pass_=bool(det == 0.0)))
    a1 = admit_of("U56", panels[0].i0, panels[0].idx.searchsorted(pd.Timestamp(OOS_START)))
    _ADMCACHE.clear()
    a2 = admit_of("U56", panels[0].i0, panels[0].idx.searchsorted(pd.Timestamp(OOS_START)))
    adet = max(abs(a1[l]["q95"] - a2[l]["q95"]) for l in LAD if np.isfinite(a1[l]["q95"]))
    GATES.append(dict(gate="G15 the admission bands are deterministic across two constructions",
                      value=adet, target=0.0, pass_=bool(adet == 0.0)))

    # ------------------------------------------------------------------ gates
    say("")
    say("=" * 108)
    say("GATES")
    say("=" * 108)
    gg = pd.DataFrame(GATES)
    gg.to_csv(f"{OUT}.gates.csv", index=False)
    for _, g in gg.iterrows():
        say(f"  {'PASS' if g.pass_ else 'FAIL'}  {g.gate:64s} {g.value:>14.6g} "
            f"(target {g.target:g})")
    say(f"  {int(gg.pass_.sum())} of {len(gg)} gates pass.")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 108)
    pays_vs_none = float(best.roll_delta) > 0
    pays_vs_nothing = float(best.roll_mean - anch_roll) > 0
    beats_null = int((live.p < 0.05).sum())
    label = ("(A) THE BAR PAYS ON ITS OWN" if (pays_vs_nothing and beats_null > 0.05 * len(live))
             else "(B) THE BAR REPAIRS THE DAMAGE BUT DOES NOT BEAT DOING NOTHING"
             if pays_vs_none else "(C) THE BAR DOES NOT PAY")
    say(f"ANSWER: {label}")
    say(f"  the best bar buys {best.roll_delta:+.4f} of mean OOS fold Sharpe over the record's")
    say(f"  habit of admitting everything, and still gives up "
        f"{best.roll_mean - anch_roll:+.4f} against doing nothing;")
    say(f"  {int((live.gap > 0).sum())} of {len(live)} moving cells sit above their own "
        f"count-matched null, {int((live.p < 0.05).sum())} at p < 0.05 against "
        f"{0.05*len(live):.1f} expected.")
    say("=" * 108)
    say(f"runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(adm=admdf, grid=gdf, picks=pdf, deltas=ddf, null=nldf, walk=wdf,
                stitched=sdf, books=bookdf, gates=gg, headline=hdf)


if __name__ == "__main__":
    main()
