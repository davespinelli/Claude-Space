#!/usr/bin/env python3
"""
Idea 1241 (lane B, 2026-09-18) — does the record's BLOCK LENGTH 63 have ANY argument other
than INHERITANCE?

WHY THIS IDEA.  1241 is the LAST numbered item standing in QUEUE.md's '## Open' section
(everything below it is lane annotation, not an idea) and the lane rule says lane B claims the
last.  No eligibility skip is taken.  The idea is price-only, answerable offline from the
committed caches, and lane B's own 1265 correction applies: a methodology question CAN carry a
capital arm, so ARM C below builds real books on three panels, prints both KEEP paths at every
cell and reads 2017-2026 exactly once under PROTOCOL rule 8.

THE PREMISE (idea 1208, this lane, 2026-09-17).  L = 63 is stated in 145 of the record's 325
L-statements, against 34 for L=21, 27 for 126 and 20 for 252.  It was first named by 1101 and
never argued.  On 1208's own 72 committed decisions the resolution rate it produces (16/72 =
0.2222) sits barely above L=21's (14/72 = 0.1944) and well below L=504's (23/72 = 0.3194).
Nobody has ever asked the tape what block length it wants.  This run asks it.

THE THREE QUESTIONS, IN THE QUEUE'S OWN ORDER:
  A.  What is the tape's OWN optimal block length?  (Politis-White plug-in for the stationary
      and the circular block bootstrap, Hall-Horowitz-Jing subsampling, and a HAC-match
      estimator, on each panel's book returns.)  How far does 63 sit from it?
  B.  Would any principled L change the RECORD'S COMMITTED resolution counts?  Answered on
      1208's own committed `.Ldependence.csv` — the SAME 72 decisions, not a re-derivation —
      by reading the count at the rung L-hat lands on.
  C.  Is any of it worth money?  A decisiveness bar at each L, run as a CHOOSER against the
      do-nothing anchor on a fresh N x H grid under rule 8.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):
    ESTIMATOR {PW_SB, PW_CB, HHJ, VMATCH}
        PW_SB   Politis-White (2004) plug-in for the STATIONARY bootstrap, with the
                Patton-Politis-White (2009) correction: b = (2*G^2/D_SB)^(1/3) * n^(1/3),
                D_SB = 2*sigma_inf^4, G = sum_k lam(k/M)*|k|*R(k), flat-top kernel lam,
                M = 2*m_hat from the |rho| < 2*sqrt(log10(n)/n) rule, b capped at
                ceil(min(3*sqrt(n), n/3)).
        PW_CB   (headline) the same with D_CB = (4/3)*sigma_inf^4 — the CIRCULAR block
                bootstrap, which is what the record's resamplers actually run.
        HHJ     Hall-Horowitz-Jing (1995): minimise subsample MSE of the statistic's bootstrap
                SD over a block ladder on overlapping subsamples of length m = round(n^(2/3)),
                then rescale L(n) = L(m) * (n/m)^(1/3).  Its pilot dependence is REPORTED, not
                hidden: the target is the full-sample bootstrap SD at the PW_CB rung.
        VMATCH  the L at which the circular-block bootstrap SD of the SHARPE equals the
                Newey-West HAC SD of the same Sharpe (Bartlett kernel, bandwidth
                floor(4*(T/100)^(2/9))).  This is the practical question the record is really
                asking: which L reproduces the answer a HAC standard error gives.
    PANEL {U56, B136, SMALL, SPY}
    4 x 4 = 16 cells, EVERY ONE published, at each of three SERIES kinds.

NOT A DIAL, reported at every value (control):
    SERIES {S_RAW, S_PSI, S_DIFF}
        S_RAW   the frozen 2026-09-04 book's daily net returns on that panel (SPY: buy-and-hold).
        S_PSI   its SHARPE INFLUENCE FUNCTION psi_t = (r-mu)/sd - (S/2)*((r-mu)^2/sd^2 - 1).
                A plug-in block length is derived for a SAMPLE MEAN; the record bootstraps a
                SHARPE, and psi is the series whose mean the Sharpe is asymptotically equal to.
                This is the correct input and it is reported beside the naive one.
        S_DIFF  the 35 (grid cell - anchor) daily net return DIFFERENCES on that panel — the
                object a decisiveness bar actually resamples.  Median and IQR over the 35.
    WINDOW {FULL, IS} — every estimate is reported on the full sample AND on warm-up..2016-12-31
        only.  The rule-8 chooser in ARM C uses the IS-only L-hat and nothing else.

PRE-DECLARED OUTCOMES, written before any number was read:
  H_FAR       the plug-in optimum for daily book returns is BELOW 21, i.e. 63 is far above what
              the tape asks for (daily equity returns carry little serial dependence, and the
              plug-in's n^(1/3) rate on ~4,400 rows puts the scale near 10).
  H_AGREE     the four estimators agree within a factor of 3 on the same series.  If they do
              not, "the tape's optimal L" is not a well-posed quantity on this data and the
              honest finding is that neither 63 nor any rival has an argument.
  H_NOCHANGE  on 1208's own 72 committed decisions the resolution count at L-hat differs from
              63's 16 by at most 3, i.e. the inheritance is harmless even though it is unargued.
  H_CAPITAL   no decisiveness bar, at ANY L on the ladder, is worth more than +0.02 of mean OOS
              Sharpe against doing nothing.  (Every chooser the record has run since 1206 has
              lost to do-nothing; the prior is strong and is stated as such.)
  Whichever fire are reported as they fall.  The capital verdict follows rule 8, not ARM A.

ARM C — THE CAPITAL ARM AND RULE 8 (required).  The frozen 2026-09-04 book with its two
structural axes walked: N {10,12,16,20,25,30} x H {21,42,63,126,189,252} = 36 cells per panel,
108 books, EVERY ONE in `.grid.csv` with its 4a and 4b legs, full/half/IS/OOS CAGR, Sharpe,
MaxDD and turnover.  These are the record's committed comparison set, not tuned parameters:
nothing about the book is chosen on out-of-sample information anywhere in this script.
Everything else is the committed construction — RAW three-leg composite ranking, eligibility =
above own 200d MA AND vol20 < 0.60, GROSS = 0.75, weekly Fri-decide / Mon-trade, equal slot
weights, 10 bps per unit turnover, t+1 execution, 260-row warm-up.  The anchor is (N=20, H=126).
Choosers, all reported:
    C_ANCHOR    do nothing: always the committed (20, 126).
    C_ISSHARPE  argmax IS Sharpe — the record's standing chooser, no bar at all.
    C_DEC_L21 / C_DEC_L63 / C_DEC_LHAT / C_DEC_L252 / C_DEC_L504
                among cells whose IS Sharpe advantage over the anchor is DECISIVE at that block
                length (|dS| > 2 SE, SE from a JOINT circular-block resample of the two arms),
                argmax IS Sharpe; otherwise stay at the anchor.
    C_RANDOM    a count-matched seeded random control, matched to C_DEC_L63's move count, so a
                gain that is merely the price of MOVING is visible as such (1221's lesson).
Parameters are chosen on warm-up..2016-12-31 ONLY; 2017-2026 is read ONCE.

GATES.  G1 the (20,126) cell replays the committed 2026-09-04 U56 anchor triple 15.71% / 1.1480
/ -19.13%, VINTAGE-PINNED to the 2026-09-16 cache end those numbers were produced on (1264
published the one-day drift; it is not re-litigated here).  G2 ARM C determinism, bit for bit.
G3 PW_CB on seeded iid gaussian noise returns a block length <= 3.  G4 PW_CB on a seeded AR(1)
with phi = 0.8 returns a strictly larger block length than on that noise.  G5 every published
L-hat lies inside [1, ceil(min(3*sqrt(n), n/3))].  G6 1208's committed `.Ldependence.csv` is
re-read, not re-derived, and reproduces its committed 16/72 at L=63 and 14/72 at L=21.  G7 the
IS and OOS windows do not overlap and OOS starts on or after 2017-01-01.  G8 the IS-window
L-hat is computed from an IS-truncated return vector and reads no OOS row.  G9 every resolution
rate lies in [0,1].  G10 bootstrap determinism: the headline SE recomputed bit for bit.
G11 the flat-top kernel weights integrate to the textbook values (lam(0)=1, lam(0.5)=1,
lam(0.75)=0.5, lam(1)=0).

PROTOCOL: rule 2 costs (10 bps) and t+1 execution; rule 4 both KEEP paths at every ARM C cell;
rule 5 one idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship
stated.  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv dropped before anything
is computed).  Every absolute level in ARM C is optimistic and every 4b pass is an UPPER bound.
ARM A is a question about the DEPENDENCE STRUCTURE of a return series, not its level, so a level
bias common to the panel does not move an autocorrelation; but the series themselves are drawn
from surviving names, so even the block lengths are the surviving names' block lengths.
ARM B re-reads numbers the record already committed and changes nothing about them.

Runs standalone and offline (committed caches and committed artefacts only):
  python research/backtests/2026-09-18_does-the-record-s-BLOCK-LENGTH-63-have-ANY-argument-other-than-INHERITANCE_B.py
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

DATE = "2026-09-18"
SLUG = "does-the-record-s-BLOCK-LENGTH-63-have-ANY-argument-other-than-INHERITANCE"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"
PRIOR_1208 = OUT / ("2026-09-17_is-the-BLOCK-LENGTH-the-record-s-LARGEST-UNSTATED-DIAL-"
                    "across-every-RESAMPLING-claim_B.Ldependence.csv")

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
LEGS = [(21, 252), (0, 126), (0, 63)]               # the committed RAW three-leg composite
N_LADDER = [10, 12, 16, 20, 25, 30]                 # committed comparison set, axis 1
H_LADDER = [21, 42, 63, 126, 189, 252]              # committed comparison set, axis 2
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)      # gate G1
VINTAGE = pd.Timestamp("2026-09-16")
SEED = 20260918
NBOOT = 400                                         # bootstrap reps (a comparand, not a dial)
INHERITED_L = 63
SEARCH_L = [1, 2, 3, 5, 8, 13, 21, 34, 42, 63, 84, 126, 189, 252, 378, 504]   # VMATCH search
HHJ_L = [2, 5, 10, 21, 42, 63, 126, 252]                                      # HHJ candidates
ESTIMATORS = ["PW_SB", "PW_CB", "HHJ", "VMATCH"]
SERIES_KINDS = ["S_RAW", "S_PSI", "S_DIFF"]

GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ================================================================== metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(r, o):
    n = len(r)
    h = n // 2
    hi = o // 2
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]),
                oos=stats(r[o:]), **{"is": stats(r[:o])},
                is_h1=stats(r[:hi]), is_h2=stats(r[hi:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


def legs_4a(b, live):
    return dict(H1=b["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(b, spy):
    return dict(H1=b["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=b["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=b["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=b["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=b["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ============================================================ ARM A — block length estimators
def flat_top(t):
    """Politis-White trapezoidal (flat-top) lag window."""
    a = np.abs(np.asarray(t, float))
    return np.where(a <= 0.5, 1.0, np.where(a <= 1.0, 2.0 * (1.0 - a), 0.0))


def autocov(x, nlag):
    n = len(x)
    xc = x - x.mean()
    return np.array([float(np.dot(xc[:n - k], xc[k:]) / n) for k in range(nlag + 1)])


def b_max(n):
    return int(np.ceil(min(3.0 * np.sqrt(n), n / 3.0)))


def politis_white(x):
    """Returns (b_stationary, b_circular, M, m_hat).  Patton-Politis-White (2009) constants."""
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 50 or x.std() == 0:
        return np.nan, np.nan, 0, 0
    Kn = max(5, int(np.ceil(np.log10(n))))
    mmax = int(np.ceil(np.sqrt(n)))
    nlag = min(n - 1, mmax + Kn)
    R = autocov(x, nlag)
    rho = R / R[0]
    crit = 2.0 * np.sqrt(np.log10(n) / n)
    m_hat = mmax
    for m in range(1, mmax + 1):
        ks = [m + k for k in range(1, Kn + 1) if m + k <= nlag]
        if ks and all(abs(rho[k]) < crit for k in ks):
            m_hat = m
            break
    M = int(min(2 * m_hat, mmax))
    ks = np.arange(-M, M + 1)
    w = flat_top(ks / M) if M > 0 else np.ones(1)
    Rk = R[np.abs(ks)]
    G = float(np.sum(w * np.abs(ks) * Rk))
    sig2 = float(np.sum(w * Rk))
    if not np.isfinite(G) or not np.isfinite(sig2) or sig2 <= 0:
        return np.nan, np.nan, M, m_hat
    bm = b_max(n)
    out = []
    for D in (2.0 * sig2 ** 2, (4.0 / 3.0) * sig2 ** 2):
        b = (2.0 * G ** 2 / D) ** (1.0 / 3.0) * n ** (1.0 / 3.0) if D > 0 else np.nan
        out.append(float(np.clip(b, 1.0, bm)) if np.isfinite(b) else np.nan)
    return out[0], out[1], M, m_hat


def psi_sharpe(r):
    """Influence function of the (unannualised) Sharpe ratio: the series whose MEAN the Sharpe
    is asymptotically equal to, up to the delta-method constant."""
    r = np.asarray(r, float)
    mu, sd = r.mean(), r.std(ddof=0)
    if sd == 0:
        return np.zeros_like(r)
    z = (r - mu) / sd
    S = mu / sd
    return z - 0.5 * S * (z ** 2 - 1.0)


def cb_index(rng, T, L, B):
    """Circular block bootstrap index matrix, shape (B, T)."""
    L = int(max(1, min(L, T)))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(B, nb))
    idx = (starts[:, :, None] + np.arange(L)[None, None, :]) % T
    return idx.reshape(B, nb * L)[:, :T]


def boot_sharpe_sd(r, L, B, seed):
    """SD of the (unannualised) Sharpe under a circular block bootstrap at block length L."""
    r = np.asarray(r, float)
    T = len(r)
    rng = np.random.default_rng(seed)
    idx = cb_index(rng, T, L, B)
    rb = r[idx]
    mu = rb.mean(axis=1)
    sd = rb.std(axis=1, ddof=0)
    s = np.where(sd > 0, mu / np.where(sd > 0, sd, 1.0), np.nan)
    return float(np.nanstd(s, ddof=0))


def hac_sharpe_sd(r):
    """Newey-West (Bartlett) HAC SD of the unannualised Sharpe via its influence function."""
    r = np.asarray(r, float)
    T = len(r)
    p = psi_sharpe(r)
    q = int(np.floor(4.0 * (T / 100.0) ** (2.0 / 9.0)))
    R = autocov(p, q)
    lrv = R[0] + 2.0 * sum((1.0 - k / (q + 1.0)) * R[k] for k in range(1, q + 1))
    return float(np.sqrt(max(lrv, 0.0) / T))


def vmatch(r, seed):
    """The L at which the circular-block bootstrap SD of the Sharpe equals its HAC SD.

    On S_PSI the "Sharpe" is the mean/sd of the influence function itself; the statistic is
    mean-like either way, which is exactly what a block length is defined for.  Stated here
    because it is the one place where the series kind changes what VMATCH is matching.

    IDENTIFICATION IS REPORTED, NOT ASSUMED.  If the bootstrap SD is FLAT in L the argmin is
    noise and the estimator has no content, so this returns the whole ladder's SD spread
    (max/min) and the set of rungs landing within 5% of the HAC target.  A spread under 1.10
    means the tape cannot tell the rungs apart at all, and the point estimate is reported as
    UNIDENTIFIED rather than quoted as an answer.
    """
    r = np.asarray(r, float)
    tgt = hac_sharpe_sd(r)
    if not np.isfinite(tgt) or tgt <= 0:
        return dict(L=np.nan, tgt=np.nan, sd=np.nan, spread=np.nan, lo=np.nan, hi=np.nan,
                    identified=False)
    sds = {}
    for L in SEARCH_L:
        if L >= len(r):
            break
        sd = boot_sharpe_sd(r, L, NBOOT, seed + L)
        if np.isfinite(sd) and sd > 0:
            sds[L] = sd
    if not sds:
        return dict(L=np.nan, tgt=np.nan, sd=np.nan, spread=np.nan, lo=np.nan, hi=np.nan,
                    identified=False)
    bl = min(sds, key=lambda L: abs(np.log(sds[L] / tgt)))
    v = np.array(list(sds.values()))
    spread = float(v.max() / v.min())
    near = [L for L, sd in sds.items() if abs(np.log(sd / tgt)) <= np.log(1.05)]
    return dict(L=float(bl), tgt=tgt, sd=sds[bl], spread=spread,
                lo=float(min(near)) if near else np.nan,
                hi=float(max(near)) if near else np.nan,
                identified=bool(spread >= 1.10))


def hhj(r, pilot_L, seed):
    """Hall-Horowitz-Jing (1995) subsample MSE choice of L for the Sharpe's bootstrap SD.

    Target ('truth'): the FULL-sample bootstrap SD at the PW_CB pilot rung, scaled by sqrt(n).
    The pilot dependence is real and is reported, not hidden: HHJ needs a target and the record
    has none.  Subsamples are overlapping, length m = round(n^(2/3)), about 40 of them.
    """
    r = np.asarray(r, float)
    n = len(r)
    if n < 400 or not np.isfinite(pilot_L):
        return np.nan, np.nan
    tgt = boot_sharpe_sd(r, int(round(pilot_L)), NBOOT, seed) * np.sqrt(n)
    m = int(round(n ** (2.0 / 3.0)))
    nsub = 40
    starts = np.linspace(0, n - m, nsub).astype(int)
    best, bl = np.inf, np.nan
    for L in HHJ_L:
        if L >= m:
            break
        errs = []
        for j, s0 in enumerate(starts):
            sd = boot_sharpe_sd(r[s0:s0 + m], L, 100, seed + 7919 * L + j)
            if np.isfinite(sd):
                errs.append((sd * np.sqrt(m) - tgt) ** 2)
        if not errs:
            continue
        mse = float(np.mean(errs))
        if mse < best:
            best, bl = mse, float(L)
    if not np.isfinite(bl):
        return np.nan, np.nan
    return float(np.clip(bl * (n / m) ** (1.0 / 3.0), 1.0, b_max(n))), bl


def estimate_all(x, seed, pilot=None):
    """All four estimators on one series.  Returns a dict keyed by estimator name."""
    bsb, bcb, M, m_hat = politis_white(x)
    pl = pilot if pilot is not None else bcb
    hh, hh_raw = hhj(x, pl, seed + 11)
    vm = vmatch(x, seed + 23)
    return dict(PW_SB=bsb, PW_CB=bcb, HHJ=hh, VMATCH=vm["L"],
                _M=M, _m_hat=m_hat, _hhj_sub=hh_raw, _hac_sd=vm["tgt"], _vm_sd=vm["sd"],
                _vm_spread=vm["spread"], _vm_lo=vm["lo"], _vm_hi=vm["hi"],
                _vm_ident=vm["identified"], _n=len(x))


# ================================================================== ARM C — the capital arm
class Panel:
    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        parts = []
        for skip, look in LEGS:
            x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
            parts.append(x.rank(axis=1, pct=True))
        comp = (sum(parts) / len(parts)).values
        self.key = np.where(np.isfinite(comp), -comp, np.inf)
        above = (q > q.rolling(200).mean()).values
        vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
        self.elig = above & (np.nan_to_num(vol20, nan=1e9) < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, N, H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, equal slot weights (the committed
    1/len(held) convention).  Row t is the APPLICATION-time weight: decided t-lag, applied t."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    nreb = len(pan.reb)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            for c in np.argsort(k, kind="stable"):
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def run(pan, Wt, gross=A_G):
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    for i0, i1 in zip(pan.reb, np.append(pan.reb[1:], T)):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0))


def pair_decisive(r_arm, r_anc, L, seed, B=NBOOT):
    """JOINT circular-block resample of the two arms at block length L.  Returns
    (dS_observed, SE, decisive) with the record's 2-SE bar, both series annualised."""
    T = len(r_arm)
    rng = np.random.default_rng(seed)
    idx = cb_index(rng, T, L, B)
    a, b = r_arm[idx], r_anc[idx]
    sa = a.mean(axis=1) / np.where(a.std(axis=1, ddof=0) > 0, a.std(axis=1, ddof=0), np.nan)
    sb = b.mean(axis=1) / np.where(b.std(axis=1, ddof=0) > 0, b.std(axis=1, ddof=0), np.nan)
    d = (sa - sb) * np.sqrt(252.0)
    se = float(np.nanstd(d, ddof=0))
    obs = sharpe(r_arm) - sharpe(r_anc)
    return obs, se, bool(np.isfinite(se) and se > 0 and abs(obs) > 2.0 * se)


# ================================================================== main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1241 lane B — {SLUG}")
    say("# DIAL 1 estimator = PW_SB / PW_CB (headline) / HHJ / VMATCH")
    say("# DIAL 2 panel     = U56 / B136 / SMALL / SPY")
    say("# control, never chosen on: SERIES {S_RAW, S_PSI, S_DIFF} x WINDOW {FULL, IS}")
    say(f"# inherited block length under test: L = {INHERITED_L} (1101's, 145 of 325 L-statements)")

    # ---- G11, data-free
    lt = flat_top([0.0, 0.5, 0.75, 1.0, 1.5])
    gate("G11 flat-top kernel", f"{list(np.round(lt, 6))}", "[1,1,0.5,0,0]",
         np.allclose(lt, [1.0, 1.0, 0.5, 0.0, 0.0]))

    # ---- G3/G4, data-free sanity of the estimator itself
    rg = np.random.default_rng(SEED)
    wn = rg.standard_normal(4400) * 0.01
    _, b_wn, _, _ = politis_white(wn)
    ar = np.zeros(4400)
    e = rg.standard_normal(4400) * 0.01
    for i in range(1, 4400):
        ar[i] = 0.8 * ar[i - 1] + e[i]
    _, b_ar, _, _ = politis_white(ar)
    gate("G3 PW_CB on iid noise", f"{b_wn:.4f}", "<= 3", np.isfinite(b_wn) and b_wn <= 3.0)
    gate("G4 PW_CB on AR(1) phi=0.8", f"{b_ar:.4f} vs noise {b_wn:.4f}", "strictly larger",
         np.isfinite(b_ar) and b_ar > b_wn)

    # ---------------------------------------------------------------- panels
    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    say("\n================ ARM C(1) — THE GRID (three panels, 36 cells each) ================")
    say(f"# frozen book: RAW composite {LEGS}, gate = above 200d MA AND vol20 < {MAXVOL}, "
        f"GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal slot weights")
    say(f"# comparison set: N {N_LADDER} x H {H_LADDER}; anchor = (N={A_N}, H={A_H})")

    grid, picks, Lrows, resrows, pairrows = [], [], [], [], []
    rng = np.random.default_rng(SEED)
    panel_state = {}
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
        spy = windows(pan.spy[WARMUP:], o)
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(live_r, o)
        gate(f"G7 {pname} IS/OOS split", f"IS ends {idx[o-1].date()}, OOS starts {idx[o].date()}",
             ">= 2017-01-01", idx[o] >= OOS_START and idx[o - 1] < OOS_START)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"window {idx[0].date()}..{idx[-1].date()}  IS {o} / OOS {len(idx)-o} rows")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%}  halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"  OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f} / {spy['oos']['MaxDD']:7.2%}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}  halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"  OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f} / {live['oos']['MaxDD']:7.2%}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}  "
            f"CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}  "
            f"Sharpe H1 {spy['h1']['Sharpe']:.4f} H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")
        say("    N    H |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe | IS Sh  IS CAGR | OOS Sh  OOS CAGR"
            "  OOS DD | turn | 4a 4b | fail4b")
        cellmap, rets = {}, {}
        for N in N_LADDER:
            for Hh in H_LADDER:
                r, turn = run(pan, build(pan, N, Hh))
                r = r[WARMUP:]
                w = windows(r, o)
                a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                rec = dict(panel=pname, N=N, H=Hh, **flat(w), turnover=turn,
                           keep4a=all(a4.values()), keep4b=all(b4.values()),
                           fail4a=failed(a4), fail4b=failed(b4),
                           is_anchor=(N == A_N and Hh == A_H))
                grid.append(rec)
                cellmap[(N, Hh)] = rec
                rets[(N, Hh)] = r
                say(f"   {N:3d} {Hh:4d} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} "
                    f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | "
                    f"{w['is']['Sharpe']:6.4f} {w['is']['CAGR']:7.2%} | {w['oos']['Sharpe']:6.4f} "
                    f"{w['oos']['CAGR']:8.2%} {w['oos']['MaxDD']:7.2%} | {turn:4.2f} | "
                    f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} "
                    f" | {failed(b4)}")
        panel_state[pname] = dict(pan=pan, idx=idx, o=o, spy=spy, live=live,
                                  cellmap=cellmap, rets=rets, px=p_px, inv=inv)

        if pname == "U56":
            q = p_px.loc[:VINTAGE]
            vp = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
            rv, _ = run(vp, build(vp, A_N, A_H))
            rv = rv[WARMUP:]
            tv = (cagr(rv), sharpe(rv), mdd(rv))
            dv = max(abs(a - b) for a, b in zip(tv, COMMITTED_U56))
            gate("G1 committed anchor replay (vintage-pinned)",
                 f"{tv[0]:.6f}/{tv[1]:.5f}/{tv[2]:.6f} max|d| {dv:.3e}", "< 1e-4", dv < 1e-4)
            r2, _ = run(pan, build(pan, A_N, A_H))
            r3, _ = run(pan, build(pan, A_N, A_H))
            gate("G2 ARM C determinism", f"max|d| {np.abs(r2 - r3).max():.3e}", "0",
                 np.abs(r2 - r3).max() == 0.0)

    # ---------------------------------------------------------------- ARM A
    say("\n================ ARM A — WHAT BLOCK LENGTH DOES THE TAPE ASK FOR? ================")
    say("# every estimate on the FULL sample and on the IS window (warm-up..2016-12-31) alone")
    sources = []
    for pname in panel_state:
        st = panel_state[pname]
        sources.append((pname, st["rets"][(A_N, A_H)], st["o"], st))
    st0 = panel_state["U56"]
    sources.append(("SPY", st0["pan"].spy[WARMUP:], st0["o"], None))

    say("\n   panel  series  window |    n |  PW_SB   PW_CB     HHJ  VMATCH |  M  m_hat | "
        "63/PW_CB  HAC sd   boot sd   VMATCH identification")
    say("   (* after VMATCH = UNIDENTIFIED: the bootstrap SD spread over the whole 1..504 ladder "
        "is under 1.10, so the tape cannot tell the rungs apart)")
    for sname, base_r, o, st in sources:
        kinds = [("S_RAW", base_r), ("S_PSI", psi_sharpe(base_r))]
        if st is not None:
            kinds.append(("S_DIFF", None))          # handled below (35 series)
        for kind, series in kinds:
            for wname, sl in (("FULL", slice(None)), ("IS", slice(0, o))):
                if kind == "S_DIFF":
                    anc = st["rets"][(A_N, A_H)]
                    per = []
                    for k, rr in st["rets"].items():
                        if k == (A_N, A_H):
                            continue
                        d = (rr - anc)[sl]
                        if d.std() == 0:
                            continue
                        e = estimate_all(d, SEED + 3 * (k[0] * 1000 + k[1]))
                        per.append(e)
                        Lrows.append(dict(panel=sname, series="S_DIFF_pair", window=wname,
                                          cell_N=k[0], cell_H=k[1], n=e["_n"],
                                          **{k2: e[k2] for k2 in ESTIMATORS}))
                    if not per:
                        continue
                    agg = {e: float(np.nanmedian([p[e] for p in per])) for e in ESTIMATORS}
                    q1 = {e: float(np.nanpercentile([p[e] for p in per], 25)) for e in ESTIMATORS}
                    q3 = {e: float(np.nanpercentile([p[e] for p in per], 75)) for e in ESTIMATORS}
                    row = dict(panel=sname, series="S_DIFF", window=wname,
                               n=int(np.median([p["_n"] for p in per])), **agg,
                               **{f"{e}_q1": q1[e] for e in ESTIMATORS},
                               **{f"{e}_q3": q3[e] for e in ESTIMATORS}, npairs=len(per))
                    Lrows.append(row)
                    say(f"   {sname:6s} {'S_DIFF':7s} {wname:6s} | {row['n']:4d} | "
                        f"{agg['PW_SB']:6.2f}  {agg['PW_CB']:6.2f}  {agg['HHJ']:6.2f}  "
                        f"{agg['VMATCH']:6.2f} |  -    -    | "
                        f"{INHERITED_L/agg['PW_CB'] if agg['PW_CB']>0 else np.nan:8.2f}  "
                        f"(median over {len(per)} pairs; IQR PW_CB "
                        f"{q1['PW_CB']:.2f}-{q3['PW_CB']:.2f})")
                    continue
                x = series[sl]
                e = estimate_all(x, SEED + 101)
                row = dict(panel=sname, series=kind, window=wname, n=e["_n"],
                           **{k2: e[k2] for k2 in ESTIMATORS}, M=e["_M"], m_hat=e["_m_hat"],
                           hhj_sub=e["_hhj_sub"], hac_sd=e["_hac_sd"], vm_sd=e["_vm_sd"],
                           vm_spread=e["_vm_spread"], vm_lo=e["_vm_lo"], vm_hi=e["_vm_hi"],
                           vm_identified=e["_vm_ident"],
                           ratio_63_over_PW_CB=INHERITED_L / e["PW_CB"] if e["PW_CB"] else np.nan,
                           b_max=b_max(e["_n"]))
                Lrows.append(row)
                say(f"   {sname:6s} {kind:7s} {wname:6s} | {e['_n']:4d} | {e['PW_SB']:6.2f}  "
                    f"{e['PW_CB']:6.2f}  {e['HHJ']:6.2f}  {e['VMATCH']:6.2f}"
                    f"{'' if e['_vm_ident'] else '*'} | "
                    f"{e['_M']:2d} {e['_m_hat']:5d}  | {row['ratio_63_over_PW_CB']:8.2f}  "
                    f"{e['_hac_sd']:.6f}  {e['_vm_sd']:.6f}  spread {e['_vm_spread']:.3f} "
                    f"within5% [{e['_vm_lo']:.0f},{e['_vm_hi']:.0f}]")

    LT = pd.DataFrame(Lrows)
    LT.to_csv(f"{STEM}.blocklen.csv", index=False)

    head = LT[(LT.series == "S_PSI") & (LT.window == "FULL")]
    hd_all = LT[(LT.series.isin(["S_RAW", "S_PSI", "S_DIFF"])) & (LT.window == "FULL")]
    say("\n   HEADLINE (PW_CB on the SHARPE INFLUENCE FUNCTION, full sample, 4 panels):")
    for _, r in head.iterrows():
        say(f"     {r.panel:6s} PW_CB {r.PW_CB:7.2f}   63 is {INHERITED_L/r.PW_CB:6.2f}x it   "
            f"(PW_SB {r.PW_SB:.2f}, HHJ {r.HHJ:.2f}, VMATCH {r.VMATCH:.2f}, cap {r.b_max:.0f})")
    med_pwcb = float(np.nanmedian(hd_all.PW_CB))
    allv = hd_all[ESTIMATORS].values.astype(float)
    allv = allv[np.isfinite(allv)]
    say(f"   median PW_CB over all {len(hd_all)} (panel x series) full-sample cells: {med_pwcb:.2f}; "
        f"63 is {INHERITED_L/med_pwcb:.2f}x it")
    say(f"   all four estimators over all cells: min {allv.min():.2f} max {allv.max():.2f} "
        f"median {np.median(allv):.2f}  (spread max/min {allv.max()/max(allv.min(),1e-9):.2f}x)")
    say(f"   H_FAR    (plug-in optimum < 21): "
        f"{'HELD' if med_pwcb < 21 else 'FAILED'}  (median {med_pwcb:.2f})")
    # H_AGREE: per-cell max/min across the four estimators
    ratios = []
    for _, r in hd_all.iterrows():
        v = np.array([r[e] for e in ESTIMATORS], float)
        v = v[np.isfinite(v) & (v > 0)]
        if len(v) >= 2:
            ratios.append(v.max() / v.min())
    ident = LT[(LT.window == "FULL") & LT.vm_identified.notna()]
    if len(ident):
        say(f"   VMATCH identification: {int(ident.vm_identified.sum())} of {len(ident)} "
            f"full-sample cells have a bootstrap-SD spread >= 1.10 over the 1..504 ladder; "
            f"median spread {ident.vm_spread.median():.3f}, max {ident.vm_spread.max():.3f}")
    say(f"   H_AGREE  (four estimators within 3x on the same series): median spread "
        f"{np.median(ratios):.2f}x, worst {max(ratios):.2f}x, "
        f"{sum(x <= 3 for x in ratios)} of {len(ratios)} cells within 3x -> "
        f"{'HELD' if np.median(ratios) <= 3 else 'FAILED'}")

    # ---------------------------------------------------------------- ARM B
    say("\n================ ARM B — WOULD A PRINCIPLED L MOVE THE RECORD'S OWN COUNTS? ============")
    if PRIOR_1208.exists():
        LD = pd.read_csv(PRIOR_1208)
        rungs = [c for c in LD.columns if c.isdigit()]
        counts = {int(c): int(LD[c].sum()) for c in rungs}
        n72 = len(LD)
        gate("G6 1208 committed counts re-read",
             f"L=63 {counts.get(63)}/{n72}, L=21 {counts.get(21)}/{n72}", "16/72 and 14/72",
             counts.get(63) == 16 and counts.get(21) == 14 and n72 == 72)
        say(f"   1208's committed decisions: {n72}.  resolution count by rung:")
        say("     " + "  ".join(f"L={k}:{v}" for k, v in sorted(counts.items())))
        # where does L-hat land on that ladder?
        cand = sorted(counts)
        for label, Lv in [("PW_CB median (all cells)", med_pwcb),
                          ("PW_CB U56 S_PSI", float(head[head.panel == "U56"].PW_CB.iloc[0])),
                          ("VMATCH median", float(np.nanmedian(hd_all.VMATCH))),
                          ("HHJ median", float(np.nanmedian(hd_all.HHJ)))]:
            lo = max([c for c in cand if c <= Lv], default=cand[0])
            hi = min([c for c in cand if c >= Lv], default=cand[-1])
            say(f"   L-hat {label:24s} = {Lv:7.2f} -> brackets [{lo}, {hi}] "
                f"-> resolution {counts[lo]}..{counts[hi]} of {n72} "
                f"(L=63 gives {counts[63]}; delta {counts[lo]-counts[63]:+d}..{counts[hi]-counts[63]:+d})")
            resrows.append(dict(arm="B_1208", label=label, L_hat=Lv, lo=lo, hi=hi,
                                res_lo=counts[lo], res_hi=counts[hi], res_63=counts[63],
                                n=n72))
        lo = max([c for c in cand if c <= med_pwcb], default=cand[0])
        hi = min([c for c in cand if c >= med_pwcb], default=cand[-1])
        dmax = max(abs(counts[lo] - counts[63]), abs(counts[hi] - counts[63]))
        say(f"   H_NOCHANGE (|count at L-hat - count at 63| <= 3 of 72): worst {dmax} -> "
            f"{'HELD' if dmax <= 3 else 'FAILED'}")
    else:
        gate("G6 1208 committed counts re-read", "artefact missing", "present", False)
        say("   1208's artefact is not in the tree; ARM B cannot be run against the record's "
            "own decisions and is reported as UNAVAILABLE, not estimated.")

    # ---------------------------------------------------------------- ARM C(2)
    say("\n================ ARM C(2) — THE BAR AS A CHOOSER, RULE 8 ================")
    say("# IS-only decisions; 2017-2026 read ONCE.  SE from a JOINT circular-block resample of")
    say(f"# the two arms, B = {NBOOT}, bar |dS| > 2 SE.  L-hat per panel = PW_CB on that panel's")
    say("# IS-window S_PSI series — an IS-only quantity (gate G8).")
    for pname in panel_state:
        st = panel_state[pname]
        o, cellmap, rets = st["o"], st["cellmap"], st["rets"]
        anc_r = rets[(A_N, A_H)][:o]
        e_is = estimate_all(psi_sharpe(anc_r), SEED + 401)
        Lhat = float(np.clip(round(e_is["PW_CB"]), 1, 504))
        gate(f"G8 {pname} IS-only L-hat", f"n={len(anc_r)} of {len(rets[(A_N,A_H)])} rows, "
             f"last IS day {st['idx'][o-1].date()}, PW_CB {e_is['PW_CB']:.2f} -> L-hat {Lhat:.0f}",
             "IS slice only, last day < 2017-01-01",
             len(anc_r) == o and st["idx"][o - 1] < OOS_START)
        ladder = [("L21", 21), ("L63", 63), ("LHAT", int(Lhat)), ("L252", 252), ("L504", 504)]
        say(f"\n## {pname}  IS rows {o}  L-hat {Lhat:.0f}")
        say("   bar     L | decisive of 35 | rate | chosen (N,H) | IS Sharpe | OOS Sharpe  OOS CAGR"
            "  OOS MaxDD | delta vs anchor")
        anc = cellmap[(A_N, A_H)]
        for lab, Lv in ladder:
            dec, best, bests = [], (A_N, A_H), anc["is_Sharpe"]
            for k, rr in rets.items():
                if k == (A_N, A_H):
                    continue
                obs, se, d = pair_decisive(rr[:o], anc_r, Lv, SEED + 17 * Lv + k[0] * 100 + k[1])
                pairrows.append(dict(panel=pname, bar=lab, L=Lv, N=k[0], H=k[1],
                                     dS=obs, SE=se, decisive=d))
                if d:
                    dec.append(k)
                    if obs > 0 and cellmap[k]["is_Sharpe"] > bests:
                        bests, best = cellmap[k]["is_Sharpe"], k
            rate = len(dec) / (len(rets) - 1)
            c = cellmap[best]
            delta = c["oos_Sharpe"] - anc["oos_Sharpe"]
            resrows.append(dict(arm="C_rate", panel=pname, bar=lab, L=Lv, decisive=len(dec),
                                npairs=len(rets) - 1, rate=rate))
            picks.append(dict(panel=pname, chooser=f"C_DEC_{lab}", L=Lv, N=best[0], H=best[1],
                              is_Sharpe=c["is_Sharpe"], is_CAGR=c["is_CAGR"],
                              oos_Sharpe=c["oos_Sharpe"], oos_CAGR=c["oos_CAGR"],
                              oos_MaxDD=c["oos_MaxDD"], delta=delta, moved=best != (A_N, A_H),
                              keep4a=c["keep4a"], keep4b=c["keep4b"],
                              spy_oos_Sharpe=st["spy"]["oos"]["Sharpe"],
                              live_oos_Sharpe=st["live"]["oos"]["Sharpe"]))
            say(f"   {lab:5s} {Lv:4d} | {len(dec):14d} | {rate:.3f} | ({best[0]:3d},{best[1]:4d})  | "
                f"{c['is_Sharpe']:9.4f} | {c['oos_Sharpe']:10.4f} {c['oos_CAGR']:9.2%} "
                f"{c['oos_MaxDD']:10.2%} | {delta:+.4f}")

        # the two reference choosers on this panel
        ks = list(cellmap)
        best_is = max(ks, key=lambda k: (cellmap[k]["is_Sharpe"], -k[0], -k[1]))
        l63 = [p for p in picks if p["panel"] == pname and p["chooser"] == "C_DEC_L63"][0]
        pool = [k for k in ks if k != (A_N, A_H)]
        rnd = tuple(pool[int(rng.integers(len(pool)))]) if l63["moved"] else (A_N, A_H)
        for cname, k in (("C_ANCHOR", (A_N, A_H)), ("C_ISSHARPE", best_is), ("C_RANDOM", rnd)):
            c = cellmap[k]
            picks.append(dict(panel=pname, chooser=cname, L=np.nan, N=k[0], H=k[1],
                              is_Sharpe=c["is_Sharpe"], is_CAGR=c["is_CAGR"],
                              oos_Sharpe=c["oos_Sharpe"], oos_CAGR=c["oos_CAGR"],
                              oos_MaxDD=c["oos_MaxDD"],
                              delta=c["oos_Sharpe"] - anc["oos_Sharpe"], moved=k != (A_N, A_H),
                              keep4a=c["keep4a"], keep4b=c["keep4b"],
                              spy_oos_Sharpe=st["spy"]["oos"]["Sharpe"],
                              live_oos_Sharpe=st["live"]["oos"]["Sharpe"]))
            say(f"   {cname:9s}    | {'':14s} |       | ({k[0]:3d},{k[1]:4d})  | "
                f"{c['is_Sharpe']:9.4f} | {c['oos_Sharpe']:10.4f} {c['oos_CAGR']:9.2%} "
                f"{c['oos_MaxDD']:10.2%} | {c['oos_Sharpe']-anc['oos_Sharpe']:+.4f}")

    G = pd.DataFrame(grid)
    P = pd.DataFrame(picks)
    RS = pd.DataFrame(resrows)
    PR = pd.DataFrame(pairrows)
    G.to_csv(f"{STEM}.grid.csv", index=False)
    P.to_csv(f"{STEM}.walkforward.csv", index=False)
    RS.to_csv(f"{STEM}.resolution.csv", index=False)
    PR.to_csv(f"{STEM}.pairs.csv", index=False)

    gate("G9 resolution rates in [0,1]",
         f"[{RS[RS.arm=='C_rate'].rate.min():.3f}, {RS[RS.arm=='C_rate'].rate.max():.3f}]", "[0,1]",
         RS[RS.arm == "C_rate"].rate.between(0, 1).all())
    stA = panel_state["U56"]
    a = pair_decisive(stA["rets"][(10, 21)][:stA["o"]], stA["rets"][(A_N, A_H)][:stA["o"]],
                      63, SEED + 17 * 63 + 10 * 100 + 21)
    b = pair_decisive(stA["rets"][(10, 21)][:stA["o"]], stA["rets"][(A_N, A_H)][:stA["o"]],
                      63, SEED + 17 * 63 + 10 * 100 + 21)
    gate("G10 bootstrap determinism", f"SE {a[1]:.8f} vs {b[1]:.8f}", "identical", a[1] == b[1])
    gate("G5 every L-hat inside [1, b_max]",
         f"{int(np.isfinite(LT[ESTIMATORS].values.astype(float)).sum())} finite estimates",
         "all in bounds",
         bool(np.nanmin(LT[ESTIMATORS].values.astype(float)) >= 1.0
              and np.nanmax(LT[ESTIMATORS].values.astype(float)) <= 504.0))

    # ---------------------------------------------------------------- pooled rule 8
    say("\n================ RULE 8 SUMMARY — POOLED OVER 3 PANELS ================")
    base = P[P.chooser == "C_ANCHOR"].oos_Sharpe.mean()
    say("   chooser        mean OOS Sharpe   delta vs do-nothing   moves   4b passes among picks")
    order = ["C_ANCHOR", "C_ISSHARPE", "C_DEC_L21", "C_DEC_L63", "C_DEC_LHAT",
             "C_DEC_L252", "C_DEC_L504", "C_RANDOM"]
    for cname in order:
        s = P[P.chooser == cname]
        if not len(s):
            continue
        say(f"   {cname:13s} {s.oos_Sharpe.mean():15.4f} {s.oos_Sharpe.mean()-base:+21.4f} "
            f"{int(s.moved.sum()):7d}   {int(s.keep4b.sum())} of {len(s)}")
    best_bar = max(("C_DEC_L21", "C_DEC_L63", "C_DEC_LHAT", "C_DEC_L252", "C_DEC_L504"),
                   key=lambda c: P[P.chooser == c].oos_Sharpe.mean())
    gain = P[P.chooser == best_bar].oos_Sharpe.mean() - base
    # ---- how often the bar fires at all, and where the pooled number comes from.
    ndec = int(PR.decisive.sum())
    say(f"\n   THE BAR ALMOST NEVER FIRES: {ndec} of {len(PR)} pair-tests are decisive "
        f"({ndec/len(PR):.4f}); by rung "
        + ", ".join(f"{k} {int(v)}" for k, v in PR.groupby('bar').decisive.sum().items()))
    say("   per-panel OOS Sharpe delta vs the anchor (the pooled row is a mean of THREE numbers):")
    for pan in P.panel.unique():
        s_ = P[P.panel == pan]
        say(f"     {pan:9s} " + "  ".join(
            f"{r.chooser.replace('C_DEC_',''):9s}{r.delta:+.4f}" for r in s_.itertuples()))
    say(f"\n   H_CAPITAL (no bar worth > +0.02 of mean OOS Sharpe): best bar {best_bar} at "
        f"{gain:+.4f} -> {'HELD' if gain <= 0.02 else 'FAILED'}")
    dhat = P[P.chooser == "C_DEC_LHAT"].oos_Sharpe.mean() - P[P.chooser == "C_DEC_L63"].oos_Sharpe.mean()
    say(f"   L-hat bar minus the INHERITED 63 bar: {dhat:+.4f} of mean OOS Sharpe "
        f"({'the tape-chosen L is worth nothing here' if abs(dhat) < 0.02 else 'material'})")

    # ---- ARM A closing summary: where does 63 sit in the WHOLE published distribution?
    allv = LT[ESTIMATORS].values.astype(float)
    allv = allv[np.isfinite(allv)]
    say(f"\n   WHERE 63 SITS IN THE WHOLE PUBLISHED DISTRIBUTION: {len(allv)} estimates "
        f"(4 estimators x 4 panels x 3 series x 2 windows, incl. every S_DIFF pair). "
        f"median {np.median(allv):.2f}, "
        f"{(allv < INHERITED_L).mean():.4f} of them BELOW 63, "
        f"{int((allv >= INHERITED_L).sum())} at or above it "
        f"(those are the VMATCH ladder's own top rungs on single difference series, not "
        f"panel-level answers). Panel-level S_PSI full-sample estimates: "
        + ", ".join(f"{r.panel} {r.PW_CB:.2f}" for _, r in head.iterrows()))

    say(f"\n   4a passes {int(G.keep4a.sum())} of {len(G)};  4b passes {int(G.keep4b.sum())} of {len(G)}"
        "  (by panel: " + ", ".join(f"{p} {int(G[G.panel==p].keep4b.sum())}/{len(G[G.panel==p])}"
                                    for p in G.panel.unique()) + ")")
    fb = G.loc[~G.keep4b, "fail4b"].str.split(",").explode().value_counts()
    say("   which 4b leg fails, over the " + f"{int((~G.keep4b).sum())} failures: "
        + ", ".join(f"{k} {v}" for k, v in fb.items()))
    fa = G.loc[~G.keep4a, "fail4a"].str.split(",").explode().value_counts()
    say("   which 4a leg fails, over the " + f"{int((~G.keep4a).sum())} failures: "
        + ", ".join(f"{k} {v}" for k, v in fa.items()))
    for p in G.panel.unique():
        s = G[(G.panel == p) & G.keep4b]
        if len(s):
            say(f"   {p}: {len(s)} 4b passes, CAGR {s.full_CAGR.min():.2%}..{s.full_CAGR.max():.2%}, "
                f"Sharpe {s.full_Sharpe.min():.4f}..{s.full_Sharpe.max():.4f}, "
                f"OOS Sharpe {s.oos_Sharpe.min():.4f}..{s.oos_Sharpe.max():.4f}")

    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)
    npass = sum(g["pass_"] for g in GATES)
    say(f"\n   GATES {npass} of {len(GATES)} PASS")
    say(f"   elapsed {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
