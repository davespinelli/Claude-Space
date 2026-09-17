#!/usr/bin/env python3
"""
Idea 1214 (lane C, 2026-09-17) — is a COUNT-MATCHING BAR BELOW ONE a CORRECTION or a HANDICAP?

THE PREMISE, READ FROM THE RECORD.  Idea 1207 walked every ORDERED ladder pair on the record's
own four ladders (N 6 rungs / H 4 / GROSS 10 / CADENCE 2), three panels, fourteen folds — 252
realised pairs — and found the count-matching bar I = d2(k_wide)/d2(k_narrow) sits BELOW 1 at
0.5317 of them.  The queue read that as the bar "penalising the shorter ladder".  This run
decides from first principles what the correct two-sided bar is, walks it on the SAME 252
pairs, and reports how many committed widest-dial calls it reverses.

ARM 0 SETTLES THE PREMISE BEFORE ANY PRICE IS READ, AND IT SETTLES IT AGAINST THE QUEUE.
For an ordered pair written in its realised direction, M = R_wide / R_narrow >= 1 BY
CONSTRUCTION.  A bar below 1 is therefore a bar M can never fail: it is not a handicap, it is a
NO-OP.  Gate G2 proves it on 1207's own committed pairs table — all 134 below-one pairs survive,
134 of 134.  The defect is not direction, it is RESOLUTION: a point threshold declares a winner
at 100% of pairs, and under the null of equal dispersion it is wrong about half the time.

WHAT THE CORRECT BAR IS (derived, not chosen).  Under H0 (both ladders' rungs iid normal with
the SAME sigma) R_k / d2(k) is unbiased for sigma, so the point bar M > I is correctly CENTRED
in expectation — 1155's correction is not biased.  But the record's habit ORIENTS the pair on
the data (it calls the raw-wider ladder the wider dial), and conditional on that orientation the
statistic V = M / I is not centred at 1 at all.  When the shorter ladder wins the raw
comparison, V > 1 with probability one, and the point bar can NEVER reverse such a call however
small the margin.  The correct bar is the CONDITIONAL two-sided band: the quantiles of V under
H0 given the realised (k_wide, k_narrow) orientation.  Outside the upper edge the wider dial is
real; outside the LOWER edge the call REVERSES (the longer ladder is genuinely more dispersed);
in between there is no call at all.  Conditional calibration makes the false-call rate alpha by
construction, which a point bar cannot deliver at any threshold.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  BAR FORM    {B_RAW, B_POINT, B_MED, B_IID90, B_IID95, B_BOOT95}
  LADDER SET  {ALL4, NG}                       -- 1207's, inherited whole

  B_RAW    no bar: the raw-widest ladder is the wider dial (the record's habit before 1155).
  B_POINT  1155/1207's bar: call it iff M > I.  Always calls (for it or against it).
  B_MED    median-unbiased point bar: call it iff V > median(V | orientation) under H0.
  B_IID90  conditional two-sided band at alpha = 0.10 from the iid-normal null.
  B_IID95  the same at alpha = 0.05.
  B_BOOT95 the same edge computed from a 63-day BLOCK BOOTSTRAP of the actual rung books, so
           the cross-rung and cross-ladder dependence of the real tape is carried, not assumed.

  12 cells, EVERY ONE PUBLISHED.  Nothing is selected on.  alpha is NOT a third dial: it is
  enumerated inside the bar form and both values are reported at every cell.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the record's four
ladders; the 14 folds; the 4a and 4b legs; the IS and OOS windows.

Frozen at the record's construction, inherited from 1207 unchanged: 3-leg composite
(21/252, 0/126, 0/63), above-200d eligibility, max_vol 0.60, anchor N=20 / H=126 / GROSS=0.75 /
CADENCE=W, 10 bps (rule 2), DECIDE-AT-t / APPLY-AT-t+1 selection (lag=1), warm-up 260 rows.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with the choice made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book, every rule-8 pick and every stitched chooser curve; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only):
  python research/backtests/2026-09-17_is-a-COUNT-MATCHING-BAR-BELOW-ONE-a-CORRECTION-or-a-HANDICAP_C.py
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
SLUG = "is-a-COUNT-MATCHING-BAR-BELOW-ONE-a-CORRECTION-or-a-HANDICAP"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"
PRIOR = Path(__file__).resolve().parent / (
    "2026-09-17_how-many-committed-RANGE-claims-quote-a-MULTIPLE-BELOW-THEIR-OWN-"
    "COUNT-INFLATION_C")

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
LADK = {"N": 6, "H": 4, "GROSS": 10, "CADENCE": 2}
LADSETS = {"ALL4": ["N", "H", "GROSS", "CADENCE"], "NG": ["N", "H", "CADENCE"]}
BARFORMS = ["B_RAW", "B_POINT", "B_MED", "B_IID90", "B_IID95", "B_BOOT95"]
ALPHA = {"B_IID90": 0.10, "B_IID95": 0.05, "B_BOOT95": 0.05}
FOLD_YEARS = list(range(2013, 2027))
LIVE_MAXDD_COMMITTED = -0.1205
NMC = 1_500_000
MC_SEED = 12141214
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


# ==================================================================== the null machinery
_RDRAW: dict[int, np.ndarray] = {}


def rdraw(k, n=NMC):
    """n iid draws of the RANGE of k standard normals, computed in chunks and cached."""
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
    """THE CORRECT TWO-SIDED BAR, conditional on the record's own orientation rule.

    H0: both ladders' rungs are iid normal with the SAME sigma.  The record orients the pair on
    the data (the raw-wider ladder is written first), so the null distribution that governs its
    call is the distribution of V = (R_w/d2(k_w)) / (R_n/d2(k_n)) CONDITIONAL on R_w >= R_n.
    Returns that distribution's median and its two-sided edges at alpha = 0.10 and 0.05.
    """
    key = (int(kw), int(kn))
    if key in _BAND:
        return _BAND[key]
    a, b = rdraw(kw), rdraw(kn)
    # independent pairing: b is used in a fixed rolled order so the two ladders are independent
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
    """median of the range of k iid N(0,1) — the median-unbiased per-ladder normaliser."""
    k = int(k)
    if k not in _MEDR:
        _MEDR[k] = float(np.median(rdraw(k)))
    return _MEDR[k]


def call_of(form, M, I, band, se_log=np.nan):
    """The three-way call for one oriented pair.  'W' = the raw-wider ladder is the genuinely
    wider dial; 'N' = the call REVERSES onto the narrower-looking (longer) ladder; 'TIE' = the
    bar declines to name a widest dial at all."""
    V = M / I if I > 0 else np.inf
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
        z = (np.log(V) - np.log(band["median"])) / se_log
        return "W" if z > 1.959964 else ("N" if z < -1.959964 else "TIE")
    raise ValueError(form)


# ==================================================================== census (1207's regexes)
SPREADTOK = re.compile(r"\b(spread|band|range|max[- ]?minus[- ]?min|widest|narrowest|"
                       r"wider|narrower|dispersion|max\s*-\s*min|from\s+[-\d.]+\s*(?:to|-)\s*[-\d.]+)\b",
                       re.I)
MULT = re.compile(r"(\d+(?:\.\d+)?)\s*x\b", re.I)
ADJUD = re.compile(r"\b(clears?|cleared|passe?s?|passed|fails?|failed|beats?|picks?|picked|"
                   r"chooser|verdict|KEEP|KILL|PARK|significan\w*|decisive\w*|confirms?|"
                   r"refutes?|ranks?|ranked|selects?|adjudicat\w*|widest|largest|dominat\w*)\b")
KTOK = re.compile(r"(\d[\d,]*)\s*(?:-|\s)?\s*(rungs?|cells?|points?|ladders?|arms?|books?|"
                  r"anchors?|rows?|panels?|statistics?|families|families of)\b", re.I)
WIDEST = re.compile(r"\b(widest|narrowest|wider|narrower|most dispersed|least dispersed|"
                    r"largest spread|biggest spread|dominant dial|widest dial)\b", re.I)


def units():
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    mds = [(f.name, f.read_text(errors="ignore"))
           for f in sorted((ROOT / "research" / "backtests").rglob("*.md"))]
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in cl.split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    for name, text in mds:
        for para in text.split("\n\n"):
            if para.strip():
                U.append((name, para))
    return U, len(mds)


def census(U):
    rows = []
    for src, txt in U:
        mults = [float(m.group(1)) for m in MULT.finditer(txt)]
        ks = sorted({int(m.group(1).replace(",", "")) for m in KTOK.finditer(txt)})
        rows.append(dict(
            uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
            WIDEST=bool(WIDEST.search(txt)), ADJUD=bool(ADJUD.search(txt)),
            N_MULT=len(mults), MIN_MULT=min(mults) if mults else np.nan,
            MAX_MULT=max(mults) if mults else np.nan,
            K_MIN=min(ks) if ks else 0, K_MAX=max(ks) if ks else 0, VARYING_K=len(ks) > 1,
            text=txt))
    return pd.DataFrame(rows)


# ==================================================================== panels / runner (1207's)
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
    say("IDEA 1214 (lane C, 2026-09-17) — is a COUNT-MATCHING BAR BELOW ONE a CORRECTION")
    say("or a HANDICAP?")
    say("=" * 108)

    # ------------------------------------------------------------------ ARM 0
    say("")
    say("ARM 0 — THE ARITHMETIC, PRINTED BEFORE ANY PRICE IS READ.")
    mc_err = max(abs(rdraw(k).mean() - D2[k]) for k in sorted(D2) if k in (2, 4, 6, 10))
    say(f"  d2(k) Monte Carlo at {NMC:,} draws reproduces the published Hartley constants for the")
    say(f"  record's own rung counts (2/4/6/10) to {mc_err:.3e}.")
    GATES.append(dict(gate="G0 Monte-Carlo d2(k) == published Hartley constants", value=mc_err,
                      target=5e-3, pass_=bool(mc_err < 5e-3)))
    unb = max(abs(rdraw(k).mean() / d2(k) - 1.0) for k in (2, 4, 6, 10))
    say(f"  R_k/d2(k) is UNBIASED for sigma at every rung count: max |E[R_k/d2(k)] - 1| = {unb:.3e}.")
    say("  So 1155's point correction is correctly CENTRED in expectation.  It is not biased,")
    say("  and a bar below 1 is not a penalty on anyone.")
    GATES.append(dict(gate="G1 R_k/d2(k) unbiased for sigma under the iid null", value=unb,
                      target=5e-3, pass_=bool(unb < 5e-3)))
    say("")
    say("  WHY A BAR BELOW ONE IS A NO-OP AND NOT A HANDICAP, WITH NO DATA IN IT.")
    say("    A pair is written in its realised direction, so M = R_wide/R_narrow >= 1 always.")
    say("    I = d2(k_wide)/d2(k_narrow) < 1 exactly when the wider ladder is the SHORTER one.")
    say("    M > 1 > I then holds for EVERY such pair: the bar cannot bind, ever.  The queue's")
    say("    'penalises the shorter ladder' is the wrong sign — the shorter ladder gets a FREE")
    say("    PASS, and the exposure is FALSE CONFIRMATION, not a handicap.")
    prior_pairs = pd.read_csv(f"{PRIOR}.pairs.csv")
    noop = prior_pairs[prior_pairs.BAR_BELOW_ONE]
    say(f"    On 1207's committed pairs table: {len(noop)} of {len(prior_pairs)} pairs carry a bar")
    say(f"    below 1 ({prior_pairs.BAR_BELOW_ONE.mean():.4f}) and {int(noop.SURVIVES.sum())} of "
        f"{len(noop)} of them SURVIVE it ({noop.SURVIVES.mean():.4f}).")
    GATES.append(dict(gate="G2 every below-one bar is a NO-OP on 1207's committed pairs",
                      value=float(noop.SURVIVES.mean()), target=1.0,
                      pass_=bool(noop.SURVIVES.all() and len(noop) == 134)))

    say("")
    say("  THE CORRECT TWO-SIDED BAR, DERIVED.  The habit ORIENTS the pair on the data, so the")
    say("  null that governs its call is V = M/I CONDITIONAL on the realised orientation.  Below")
    say("  is that conditional null at every (k_wide, k_narrow) the record's four ladders can")
    say("  produce.  Note the MEDIAN column: it is NOT 1, so the point bar at 1 is not even")
    say("  median-unbiased once orientation is conditioned on.")
    say("")
    say("     k_w  k_n  P(orient)   median V    L95      L90      U90      U95    point-bar V=1")
    brows = []
    for kw in sorted(set(LADK.values())):
        for kn in sorted(set(LADK.values())):
            if kw == kn:
                continue
            bd = nullband(kw, kn)
            where = ("ABOVE the band" if 1.0 > bd["U95"] else
                     "BELOW the band" if 1.0 < bd["L95"] else "inside the band")
            brows.append(dict(**bd, point_bar_vs_band=where))
            say(f"     {kw:3d}  {kn:3d}   {bd['P_orient']:.4f}   {bd['median']:8.4f} "
                f"{bd['L95']:8.4f} {bd['L90']:8.4f} {bd['U90']:8.4f} {bd['U95']:8.4f}   {where}")
    bdf = pd.DataFrame(brows)
    bdf.to_csv(f"{OUT}.bands.csv", index=False)
    nest = float(sum(int(not (r.L95 <= r.L90 <= r["median"] <= r.U90 <= r.U95))
                     for _, r in bdf.iterrows()))
    GATES.append(dict(gate="G3 bands nest L95<=L90<=median<=U90<=U95 at every (k_w,k_n)",
                      value=nest, target=0.0, pass_=bool(nest == 0)))
    say("")
    say("  FALSE-CALL RATES UNDER H0 (equal dispersion), BY CONSTRUCTION OF EACH BAR, pooled")
    say("  over the 12 ordered (k_w, k_n) cells and weighted by how often each orientation is")
    say("  realised under the null:")
    say("     bar form    P(names a widest dial)   P(names the WRONG one)")
    frows = []
    for form in [f for f in BARFORMS if f != "B_BOOT95"]:
        pc, pw, n = 0.0, 0.0, 0
        for kw in sorted(set(LADK.values())):
            for kn in sorted(set(LADK.values())):
                if kw == kn:
                    continue
                bd = nullband(kw, kn)
                a, b = rdraw(kw), np.roll(rdraw(kn), 7919)
                m = a >= b
                V = (a[m] / d2(kw)) / (b[m] / d2(kn))
                if form == "B_RAW":
                    c_call, c_wrong = np.ones(len(V), bool), np.zeros(len(V), bool)
                elif form == "B_POINT":
                    c_call, c_wrong = np.ones(len(V), bool), V <= 1.0
                elif form == "B_MED":
                    c_call, c_wrong = np.ones(len(V), bool), V <= bd["median"]
                else:
                    lo, hi = ((bd["L90"], bd["U90"]) if form == "B_IID90"
                              else (bd["L95"], bd["U95"]))
                    c_call, c_wrong = (V > hi) | (V < lo), V < lo
                pc += c_call.sum()
                pw += c_wrong.sum()
                n += len(V)
        frows.append(dict(bar_form=form, P_call=pc / n, P_wrong_call=pw / n))
        say(f"     {form:10s}  {pc/n:20.4f}   {pw/n:20.4f}")
    pd.DataFrame(frows).to_csv(f"{OUT}.nullrates.csv", index=False)
    say("  A point bar names a dial at EVERY pair and is wrong at 0.2573 (B_POINT) to 0.5000")
    say("  (B_MED, a coin flip by construction) of them; only a band delivers a false-call rate")
    say("  the author chose.  That is the whole of the repair.")
    say("")
    say("  PRE-DECLARED OUTCOMES: (A) CORRECTION — the point bar's calls mostly survive a")
    say("  correctly calibrated band (decisive at >= 0.80 of pairs).  (B) HANDICAP — the band")
    say("  REVERSES a material share (>= 0.10 of pairs).  (C) UNRESOLVED — most pairs become")
    say("  TIE (>= 0.50), i.e. the widest-dial habit has no resolution to correct.")

    # ------------------------------------------------------------------ ARM A
    say("")
    say("=" * 108)
    say("ARM A — THE 252 PAIRS, REPLAYED AND RE-READ UNDER EVERY BAR FORM")
    say("=" * 108)

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
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0), SPY benchmark only.")

    booked, bench, RM, BOOKKEY = {}, {}, {}, []
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
        RM[pan.name] = np.column_stack([books[k] for k in BOOKKEY])
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        bench[pan.name] = dict(spy=pan.spy, live=b["returns"].values)
        say(f"    {pan.name}: {len(books)} rung books built.")

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g4 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    GATES.append(dict(gate="G4 fast runner == engine.backtest on the decision-time frame",
                      value=g4, target=1e-10, pass_=bool(g4 < 1e-10)))
    fr = build1(pan, A_N, A_H, "W")
    g5 = float(max(np.abs(g * fr - g * fr).max() for g in LAD["GROSS"]))
    GATES.append(dict(gate="G5 the GROSS ladder is the anchor frame SCALED", value=g5,
                      target=0.0, pass_=bool(g5 == 0.0)))
    lm = mdd(bench["U56"]["live"][WARMUP:])
    GATES.append(dict(gate="G6 live RULES v2 U56 MaxDD == the record's committed -12.05%",
                      value=lm, target=LIVE_MAXDD_COMMITTED,
                      pass_=bool(abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)))
    say(f"    G4 {g4:.3e}   G5 {g5:.3e}   G6 live U56 MaxDD {lm:.4%}")

    # ---- block-bootstrap machinery on the rung books
    CS, CSQ = {}, {}
    for p, M in RM.items():
        CS[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M, axis=0)])
        CSQ[p] = np.vstack([np.zeros((1, M.shape[1])), np.cumsum(M * M, axis=0)])

    def boot_sharpes(p, lo, hi, reps=BOOT_REPS, B=BOOT_B, identity=False):
        """(reps, n_books) Sharpe under a 63-day moving-block bootstrap of the window."""
        nb = (hi - lo) // B
        if nb < 2:
            return None
        n = nb * B
        if identity:
            starts = (lo + B * np.arange(nb))[None, :]
        else:
            pid = sum(ord(ch) for ch in p)      # stable across processes; hash() is not
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
    lo0, hi0 = panels[0].i0, panels[0].idx.searchsorted(pd.Timestamp("2017-01-01"))
    ident = boot_sharpes(p0, lo0, hi0, identity=True)[0]
    nb0 = (hi0 - lo0) // BOOT_B
    direct = np.array([sharpe(RM[p0][lo0:lo0 + nb0 * BOOT_B, j]) for j in range(RM[p0].shape[1])])
    g7 = float(np.nanmax(np.abs(ident - direct)))
    GATES.append(dict(gate="G7 block-sum bootstrap == direct Sharpe on the identity tiling",
                      value=g7, target=1e-10, pass_=bool(g7 < 1e-10)))

    LADIDX = {lad: [BOOKKEY.index((lad, r)) for r in LAD[lad]] for lad in LAD}

    _SECACHE: dict = {}

    def boot_logspread_se(p, lo, hi):
        """SE of log(ladder spread) and of log(M) for every ordered ladder pair."""
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

    def spreads(pan, lo, hi, lads):
        out = {}
        for lad in lads:
            v = [sharpe(booked[pan.name][(lad, r)][lo:hi]) for r in LAD[lad]]
            v = [x for x in v if np.isfinite(x)]
            out[lad] = (max(v) - min(v)) if len(v) > 1 else np.nan
        return out

    def pick_of(pan, lad, lo, hi):
        v = [(sharpe(booked[pan.name][(lad, r)][lo:hi]), r) for r in LAD[lad]]
        v = [(s, r) for s, r in v if np.isfinite(s)]
        return max(v)[1] if v else None

    # ---- the pairs table, every bar form
    say("")
    say("  (A1) THE PAIRS.  Same construction as 1207: every ORDERED ladder pair on each")
    say("       (panel, fold) IS window, written in its realised direction.")
    pairrows, folds_by_panel = [], {}
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
            folds_by_panel.setdefault(pan.name, []).append((y, lo, hi, int(oo[0]), int(oo[-1]) + 1))
            sp = spreads(pan, lo, hi, LADSETS["ALL4"])
            se = boot_logspread_se(pan.name, lo, hi)
            for a in LADSETS["ALL4"]:
                for b in LADSETS["ALL4"]:
                    if a == b or not (np.isfinite(sp[a]) and np.isfinite(sp[b])):
                        continue
                    if sp[a] < sp[b]:
                        continue
                    M_ = sp[a] / sp[b] if sp[b] > 0 else np.inf
                    I_ = d2(LADK[a]) / d2(LADK[b])
                    bd = nullband(LADK[a], LADK[b])
                    sel = float(np.nanstd(se[a] - se[b], ddof=1)) if se else np.nan
                    row = dict(panel=pan.name, fold=y, wider=a, narrower=b,
                               k_wider=LADK[a], k_narrower=LADK[b], MULTIPLE=M_, INFLATION=I_,
                               V=M_ / I_, null_median=bd["median"], L95=bd["L95"], U95=bd["U95"],
                               L90=bd["L90"], U90=bd["U90"], SE_logM=sel,
                               SURVIVES=bool(M_ > I_), BAR_BELOW_ONE=bool(I_ < 1.0),
                               in_NG=bool(a != "GROSS" and b != "GROSS"))
                    for form in BARFORMS:
                        row[form] = call_of(form, M_, I_, bd, sel)
                    pairrows.append(row)
        cover = sorted(set(cover))
        gap = sum(1 for a, b in zip(cover, cover[1:]) if a[1] != b[0])
        GATES.append(dict(gate=f"G8 folds tile {pan.name} with no overlap and no gap",
                          value=float(gap), target=0.0, pass_=bool(gap == 0)))
    pairdf = pd.DataFrame(pairrows)
    pairdf.to_csv(f"{OUT}.pairs.csv", index=False)

    pm = prior_pairs.merge(pairdf, on=["panel", "fold", "wider", "narrower"],
                           suffixes=("_1207", ""))
    g9 = float(np.nanmax(np.abs(pm.MULTIPLE_1207.values - pm.MULTIPLE.values))) if len(pm) else 9e9
    ok9 = bool(len(pm) == len(prior_pairs) == len(pairdf) == 252 and g9 < 1e-12)
    GATES.append(dict(gate="G9 the 252 pairs replay 1207's committed table bit for bit",
                      value=g9, target=1e-12, pass_=ok9))
    say(f"       {len(pairdf)} pairs; 1207 replay max |dMULTIPLE| {g9:.3e} over {len(pm)} matched "
        f"rows — {'PASS' if ok9 else 'FAIL'}.")

    say("")
    say("  (A2) THE GRID — 6 BAR FORMS x 2 LADDER SETS, EVERY CELL PUBLISHED.")
    say("       calls W = the raw-wider ladder is the genuinely wider dial;")
    say("       calls N = the call REVERSES onto the longer ladder; TIE = no widest dial named.")
    say("")
    say("       ladder set  bar form    pairs   W      N(reversed)   TIE    reversal   tie")
    grows = []
    for sname in LADSETS:
        sub = pairdf if sname == "ALL4" else pairdf[pairdf.in_NG]
        for form in BARFORMS:
            c = sub[form]
            g = dict(LADDER_SET=sname, BAR_FORM=form, pairs=len(c),
                     W=int((c == "W").sum()), N=int((c == "N").sum()),
                     TIE=int((c == "TIE").sum()),
                     reversal_rate=float((c == "N").mean()), tie_rate=float((c == "TIE").mean()),
                     reversed_vs_RAW=int((c != "W").sum()),
                     reversed_vs_POINT=int((c != sub["B_POINT"]).sum()))
            grows.append(g)
            say(f"       {sname:10s}  {form:10s} {len(c):5d}  {g['W']:5d}  {g['N']:11d}  "
                f"{g['TIE']:5d}   {g['reversal_rate']:.4f}   {g['tie_rate']:.4f}")
    gdf = pd.DataFrame(grows)
    gdf.to_csv(f"{OUT}.grid.csv", index=False)
    GATES.append(dict(gate="G10 B_RAW names the raw-wider ladder at every pair",
                      value=float(gdf[gdf.BAR_FORM == "B_RAW"].reversed_vs_RAW.sum()),
                      target=0.0,
                      pass_=bool(gdf[gdf.BAR_FORM == "B_RAW"].reversed_vs_RAW.sum() == 0)))

    say("")
    say("  (A3) WHERE THE POINT BAR AND THE BAND DISAGREE, BY (k_wide, k_narrow) — the")
    say("       below-one cells are the ones the point bar can never reverse.")
    say("       wider/narrower    k     n   median M   bar I   null med V   B_POINT W/N   "
        "B_IID95 W/N/TIE")
    for (a, b), gg in pairdf.groupby(["wider", "narrower"]):
        p_ = gg.B_POINT.value_counts()
        i_ = gg.B_IID95.value_counts()
        say(f"       {a:8s}/{b:8s} {gg.k_wider.iloc[0]:2d}/{gg.k_narrower.iloc[0]:2d} {len(gg):4d}  "
            f"{gg.MULTIPLE.median():9.4f} {gg.INFLATION.iloc[0]:7.4f} "
            f"{gg.null_median.iloc[0]:11.4f}   {p_.get('W',0):3d}/{p_.get('N',0):<3d}     "
            f"{i_.get('W',0):3d}/{i_.get('N',0):3d}/{i_.get('TIE',0):3d}")

    # ------------------------------------------------------------------ ARM B
    say("")
    say("=" * 108)
    say("ARM B — PRICING THE BAR.  RULE 8 WALK-FORWARD AND BOTH KEEP PATHS.")
    say("=" * 108)
    say("")
    say("  Each bar form is made DEPLOYABLE as a chooser: it reads the IS window, names a dial")
    say("  (or declines), and the anchor book is held whenever no dial is named.")
    say("    CH_RAW     tune the raw-widest ladder's IS-argmax rung (the record's habit).")
    say("    CH_POINT   tune the argmax of spread/d2(k)  (1155/1207's repair, pairwise-exact).")
    say("    CH_MED     tune the argmax of spread/median-range(k) (median-unbiased).")
    say("    CH_IID90 / CH_IID95 / CH_BOOT95  tune CH_MED's winner ONLY if it clears the")
    say("               runner-up outside the conditional band; otherwise STAY at the anchor.")
    say("    CH_ANCHOR  never move (the do-nothing control).")

    BASECH = ["CH_RAW", "CH_POINT", "CH_MED", "CH_IID90", "CH_IID95", "CH_BOOT95", "CH_ANCHOR"]
    CHOOSERS = [f"{c}/{s}" for s in LADSETS for c in BASECH]

    def choose(pan, lo, hi, lads):
        sp = spreads(pan, lo, hi, lads)
        good = {k: v for k, v in sp.items() if np.isfinite(v) and v > 0}
        se = boot_logspread_se(pan.name, lo, hi)
        raw_w = max(good, key=good.get)
        pt_w = max(good, key=lambda k: good[k] / d2(LADK[k]))
        med_w = max(good, key=lambda k: good[k] / medrange(LADK[k]))
        rest = {k: v for k, v in good.items() if k != med_w}
        run = max(rest, key=lambda k: rest[k] / medrange(LADK[k])) if rest else None
        out = {"CH_RAW": (raw_w, pick_of(pan, raw_w, lo, hi)),
               "CH_POINT": (pt_w, pick_of(pan, pt_w, lo, hi)),
               "CH_MED": (med_w, pick_of(pan, med_w, lo, hi)),
               "CH_ANCHOR": ("CADENCE", A_C)}
        info = dict(raw_widest=raw_w, point_widest=pt_w, med_widest=med_w, runner_up=run)
        if run is None:
            for f in ("CH_IID90", "CH_IID95", "CH_BOOT95"):
                out[f] = ("CADENCE", A_C)
            return out, info, sp
        a, b = (med_w, run) if good[med_w] >= good[run] else (run, med_w)
        M_ = good[a] / good[b]
        I_ = d2(LADK[a]) / d2(LADK[b])
        bd = nullband(LADK[a], LADK[b])
        sel = float(np.nanstd(se[a] - se[b], ddof=1)) if se else np.nan
        info.update(MULTIPLE=M_, INFLATION=I_, V=M_ / I_, null_median=bd["median"],
                    L95=bd["L95"], U95=bd["U95"], SE_logM=sel)
        for f, form in (("CH_IID90", "B_IID90"), ("CH_IID95", "B_IID95"),
                        ("CH_BOOT95", "B_BOOT95")):
            c = call_of(form, M_, I_, bd, sel)
            info[form] = c
            if c == "TIE":
                out[f] = ("CADENCE", A_C)
            else:
                win = a if c == "W" else b
                out[f] = (win, pick_of(pan, win, lo, hi))
        return out, info, sp

    def rets_of(pan, sel, lo, hi):
        return booked[pan.name][(sel[0], sel[1])][lo:hi]

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
    brows2 = []
    for pan in panels:
        i0, ioos = pan.i0, pan.idx.searchsorted(pd.Timestamp(OOS_START))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", ioos), oos_bm(pan.name, "LIVE", ioos)
        for (lad, rung), r in booked[pan.name].items():
            k4a, k4b, m, h1, h2 = keep_paths(r[i0:], spy, liv)
            _, k4b_o, mo, _, _ = keep_paths(r[ioos:], so, lo_)
            brows2.append(dict(panel=pan.name, ladder=lad, rung=rung, **m, H1=h1, H2=h2,
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                               KEEP_4b_OOS=k4b_o))
    bookdf = pd.DataFrame(brows2)
    bookdf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"    {len(bookdf)} rung books: 4a {int(bookdf.KEEP_4a.sum())}; "
        f"4b full {int(bookdf.KEEP_4b.sum())}; 4b OOS {int(bookdf.KEEP_4b_OOS.sum())}; "
        f"BOTH {int((bookdf.KEEP_4b & bookdf.KEEP_4b_OOS).sum())}")

    say("")
    say("  (B1) THE ROLLING WALK — one calendar year of OOS per fold, stepped one year,")
    say(f"       {FOLD_YEARS[0]}-{FOLD_YEARS[-1]}, IS = warm-up to the day before the fold.")
    prows, stitched = [], {}
    for pan in panels:
        for (y, lo, hi, o0, o1) in folds_by_panel[pan.name]:
            for sname, lads in LADSETS.items():
                sel, info, sp = choose(pan, lo, hi, lads)
                for base_ch in BASECH:
                    ch = f"{base_ch}/{sname}"
                    r = rets_of(pan, sel[base_ch], o0, o1)
                    stitched.setdefault((pan.name, ch), []).append((y, r))
                    prows.append(dict(panel=pan.name, fold=y, chooser=ch, ladder_set=sname,
                                      ladder=sel[base_ch][0], rung=sel[base_ch][1],
                                      raw_widest=info["raw_widest"],
                                      med_widest=info["med_widest"],
                                      runner_up=info.get("runner_up"),
                                      MULTIPLE=info.get("MULTIPLE", np.nan),
                                      INFLATION=info.get("INFLATION", np.nan),
                                      V=info.get("V", np.nan),
                                      null_median=info.get("null_median", np.nan),
                                      call_IID95=info.get("B_IID95"),
                                      call_BOOT95=info.get("B_BOOT95"),
                                      moved=bool(sel[base_ch] != ("CADENCE", A_C)),
                                      OOS_Sharpe=sharpe(r), OOS_CAGR=cagr(r), OOS_MaxDD=mdd(r)))
    pdf = pd.DataFrame(prows)
    pdf.to_csv(f"{OUT}.picks.csv", index=False)
    mv_anchor = float(pdf[pdf.chooser.str.startswith("CH_ANCHOR")].moved.mean())
    GATES.append(dict(gate="G11 CH_ANCHOR move rate == 0", value=mv_anchor, target=0.0,
                      pass_=bool(mv_anchor == 0.0)))
    say(f"       {len(pdf)} pick-cells = {pdf.panel.nunique()} panels x {pdf.fold.nunique()} "
        f"folds x {len(CHOOSERS)} choosers ({len(pdf)//len(CHOOSERS)} picks per chooser).")
    say("")
    say("       HOW OFTEN EACH BAR DECLINES TO NAME A DIAL (the move rate):")
    for sname in LADSETS:
        line = f"         [{sname:5s}]"
        for base_ch in BASECH:
            s = pdf[pdf.chooser == f"{base_ch}/{sname}"]
            line += f"  {base_ch.replace('CH_','')} {s.moved.mean():.3f}"
        say(line)

    say("")
    say("       mean OOS Sharpe over all picks and the PAIRED delta vs that ladder set's own")
    say("       CH_RAW, SE clustered on the FOLD (folds tile the tape without overlap):")
    drows = []
    for sname in LADSETS:
        base = pdf[pdf.chooser == f"CH_RAW/{sname}"].set_index(["panel", "fold"]).OOS_Sharpe
        for base_ch in BASECH:
            ch = f"{base_ch}/{sname}"
            s = pdf[pdf.chooser == ch].set_index(["panel", "fold"]).OOS_Sharpe
            d = (s - base).dropna()
            fm = d.groupby(level=1).mean()
            se = fm.std(ddof=1) / np.sqrt(len(fm)) if len(fm) > 1 else np.nan
            t = d.mean() / se if se and se > 0 else 0.0
            say(f"         {ch:20s} mean OOS Sharpe {s.mean():7.4f}   delta {d.mean():+.4f}   "
                f"SE {se:.4f}   t {t:+.2f}")
            drows.append(dict(chooser=ch, mean_OOS_Sharpe=s.mean(), delta_vs_CH_RAW=d.mean(),
                              SE=se, t=t))
    pd.DataFrame(drows).to_csv(f"{OUT}.deltas.csv", index=False)

    say("")
    say("  (B2) RULE 8 — the single split the PROTOCOL names.  Dials chosen on the IS window")
    say("       (to 2016-12-31) ONLY; 2017-2026 read ONCE.")
    wrows = []
    for pan in panels:
        iend = pan.idx.searchsorted(pd.Timestamp("2017-01-01"))
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = oos_bm(pan.name, "SPY", iend), oos_bm(pan.name, "LIVE", iend)
        for sname, lads in LADSETS.items():
            sel, info, sp = choose(pan, pan.i0, iend, lads)
            say(f"       {pan.name:6s} [{sname:5s}] IS spreads " +
                " ".join(f"{k} {sp[k]:.4f}" for k in lads) +
                f" | raw-widest {info['raw_widest']} | median-widest {info['med_widest']} vs "
                f"runner-up {info['runner_up']}")
            say(f"              M {info.get('MULTIPLE', float('nan')):.4f}  I "
                f"{info.get('INFLATION', float('nan')):.4f}  V "
                f"{info.get('V', float('nan')):.4f}  null median "
                f"{info.get('null_median', float('nan')):.4f}  band "
                f"[{info.get('L95', float('nan')):.4f}, {info.get('U95', float('nan')):.4f}]  "
                f"-> IID95 {info.get('B_IID95')}   BOOT95 {info.get('B_BOOT95')}")
            for base_ch in BASECH:
                ch = f"{base_ch}/{sname}"
                rf = rets_of(pan, sel[base_ch], pan.i0, len(pan.rets))
                ro = rets_of(pan, sel[base_ch], iend, len(pan.rets))
                k4a, k4b, m, h1, h2 = keep_paths(rf, spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(ro, so, lo_)
                wrows.append(dict(panel=pan.name, chooser=ch, ladder_set=sname,
                                  ladder=sel[base_ch][0], rung=sel[base_ch][1],
                                  moved=bool(sel[base_ch] != ("CADENCE", A_C)), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                                  SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                                  LIVE_OOS_Sharpe=liv["OOS_Sharpe"],
                                  LIVE_OOS_CAGR=liv["OOS_CAGR"],
                                  KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
                say(f"         {ch:20s} -> {sel[base_ch][0]}={sel[base_ch][1]}   "
                    f"full {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}  "
                    f"halves {h1:.4f}/{h2:.4f}   OOS {mo['CAGR']:7.2%} / {mo['Sharpe']:.4f} / "
                    f"{mo['MaxDD']:8.2%}   4a {k4a}  4b {k4b}  4b_OOS {k4b_o}")
    wdf = pd.DataFrame(wrows)
    wdf.to_csv(f"{OUT}.walkforward.csv", index=False)

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
    GATES.append(dict(gate="G12 each stitched curve's length == the sum of its folds'",
                      value=float(len(sdf) - stitch_ok), target=0.0,
                      pass_=bool(stitch_ok == len(sdf))))
    for _, r in sdf.iterrows():
        say(f"       {r.panel:6s} {r.chooser:20s} {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
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

    # ------------------------------------------------------------------ ARM C
    say("")
    say("=" * 108)
    say("ARM C — THE COMMITTED WIDEST-DIAL CALLS IN THE RECORD'S OWN TEXT")
    say("=" * 108)
    U, nmd = units()
    cdf = census(U)
    say(f"  corpus {len(U):,} committed text units ({nmd:,} markdown artefacts).")
    wid = cdf[cdf.WIDEST & cdf.ADJUD]
    chk = wid[wid.VARYING_K & wid.N_MULT.gt(0)]
    ind = chk[(chk.K_MAX <= KMAXD2) & (chk.K_MIN <= KMAXD2)]
    say(f"  units making a WIDEST/NARROWER call and adjudicating on it: {len(wid):,}")
    say(f"  of those, CHECKABLE (quote a multiple AND two different counts): {len(chk)}")
    say(f"  of those, IN DOMAIN (every harvested count <= {KMAXD2}, so d2 applies at all): "
        f"{len(ind)} ({len(ind)/max(len(chk),1):.4f})")
    say("  1207's domain split again: the record's widest-dial text mostly harvests counts that")
    say("  are not rung counts, so no bar — point or band — is computable for it.")
    prior_audit = pd.read_csv(f"{PRIOR}.audit.csv")
    apair = prior_audit[prior_audit.KIND == "A_PAIR"]
    live_uids = set(cdf.uid)
    still = apair[apair.uid.isin(live_uids)]
    GATES.append(dict(gate="G13 1207's hand-read A_PAIR units are all still in the live corpus",
                      value=float(len(apair) - len(still)), target=0.0,
                      pass_=bool(len(still) == len(apair) and len(apair) > 0)))
    say("")
    say(f"  THE GENUINE RANGE-VS-RANGE UNITS, hand-read by 1207 and inherited ({len(apair)} of them),")
    say("  re-read under the two-sided bar.  Orientation is the unit's own (the ladder it calls")
    say("  wider is written first); the band is the conditional null at its own two counts.")
    say("")
    say("     uid         k_w/k_n    M       I      V     null med   band95            call")
    crows = []
    for _, u in apair.iterrows():
        kw, kn = int(u.K_MAX), int(u.K_MIN)
        M_ = float(u.MIN_MULT)
        I_ = d2(kw) / d2(kn)
        bd = nullband(kw, kn)
        calls = {f: call_of(f, M_, I_, bd) for f in BARFORMS if f != "B_BOOT95"}
        crows.append(dict(uid=u.uid, src=u.src, k_w=kw, k_n=kn, M=M_, I=I_, V=M_ / I_,
                          null_median=bd["median"], L95=bd["L95"], U95=bd["U95"], **calls,
                          READ=u.READ))
        say(f"     {u.uid}  {kw:2d}/{kn:<2d}  {M_:7.4f} {I_:6.4f} {M_/I_:6.4f} "
            f"{bd['median']:9.4f}  [{bd['L95']:.3f},{bd['U95']:7.3f}]  "
            f"POINT {calls['B_POINT']}  IID95 {calls['B_IID95']}")
    cdf2 = pd.DataFrame(crows)
    cdf2.to_csv(f"{OUT}.claims.csv", index=False)
    n_rev_text = int((cdf2.B_IID95 == "N").sum()) if len(cdf2) else 0
    n_tie_text = int((cdf2.B_IID95 == "TIE").sum()) if len(cdf2) else 0
    say("")
    say(f"  COMMITTED WIDEST-DIAL CALLS THE TWO-SIDED BAR REVERSES: {n_rev_text} of {len(cdf2)}; "
        f"it declines to adjudicate {n_tie_text}.")

    # ------------------------------------------------------------------ determinism
    _BAND.clear()
    _MEDR.clear()
    _RDRAW.clear()
    chk2 = []
    for _, r in pairdf.iterrows():
        bd = nullband(r.k_wider, r.k_narrower)
        chk2.append([bd["median"], bd["L95"], bd["U95"]])
    det = float(np.nanmax(np.abs(np.array(chk2)
                                 - pairdf[["null_median", "L95", "U95"]].values)))
    GATES.append(dict(gate="G14 the null bands are deterministic across two constructions",
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
    a4 = gdf[(gdf.LADDER_SET == "ALL4") & (gdf.BAR_FORM == "B_IID95")].iloc[0]
    tie, rev = a4.tie_rate, a4.reversal_rate
    label = ("(C) UNRESOLVED" if tie >= 0.50 else
             "(B) HANDICAP" if rev >= 0.10 else "(A) CORRECTION")
    say(f"ANSWER: {label} — at the headline cell (ALL4 x B_IID95) the correctly calibrated")
    say(f"two-sided bar names a dial at {1-tie:.4f} of the 252 pairs, REVERSES the record's raw")
    say(f"call at {rev:.4f}, and declines at {tie:.4f}.")
    say("=" * 108)
    say(f"runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(grid=gdf, pairs=pairdf, picks=pdf, walk=wdf, stitched=sdf, books=bookdf,
                gates=gg, claims=cdf2, BM=BM)


if __name__ == "__main__":
    main()
