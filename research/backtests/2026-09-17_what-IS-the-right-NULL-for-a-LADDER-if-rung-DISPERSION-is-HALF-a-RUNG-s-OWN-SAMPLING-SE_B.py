#!/usr/bin/env python3
"""Idea 1218 (lane B, 2026-09-17)
   what-IS-the-right-NULL-for-a-LADDER-if-rung-DISPERSION-is-HALF-a-RUNG-s-OWN-SAMPLING-SE

THE QUEUE'S PREMISE, QUOTED.  Idea 1205 found that k = 8 INDEPENDENT gross-matched null
books realise only 0.4186 of the range d2(8) predicts from their own single-book sampling
SE, "because they share the market factor"; that ratio, not 1, is the achievable ceiling
for any ladder on this tape.  The queue asks for the ratio MEASURED AS A FUNCTION of
cross-book correlation (varying N, the draw pool and the panel), and for a verdict on
whether a CORRELATION-CORRECTED d2 gives a bar a real ladder could clear.

THE ARITHMETIC, DECLARED BEFORE ANY NUMBER.  For k exchangeable draws with common
sampling SD s and pairwise correlation rho, write X_i = sqrt(rho) Z0 + sqrt(1-rho) e_i.
The common term Z0 cancels out of every difference, so

    E[max X - min X]  =  sqrt(1 - rho) * d2(k) * s          (*)

i.e. the corrected constant is d2_corr(k, rho) = d2(k) * sqrt(1 - rho), and the corrected
statistic is

    R_corr  =  range / (d2(k) * sqrt(1 - rho) * s)  =  R / sqrt(1 - rho).

(*) is exact for equicorrelated normals and is checked as a standalone gate (G_LAW) and
again end-to-end on a synthetic driver whose rho is imposed (D_SYNTH).  If 1205's R =
0.4186 is pure correlation, the rho of its eight books' SHARPE ESTIMATORS must be about
1 - 0.4186^2 = 0.825 -- that is a prediction this run can falsify, not a fit.

WHICH rho.  Not the correlation of daily returns: the object d2 scales is the ladder's
STATISTIC, so the relevant rho is the cross-book correlation of the SHARPE ESTIMATOR,
measured by a PAIRED bootstrap (one resampled day index applied to all k books at once).
Both are measured and published at every rung; they are not the same number and the run
reports the gap.

TUNED DIALS (2, PROTOCOL rule 4) -- and the queue names both:

  `CORR DRIVER`  {D_N, D_POOL, D_SYNTH}
  `PANEL`        {U56, B136, SMALL}

  = 9 cells, EVERY ONE PUBLISHED in `.dialgrid.csv`.

  D_N     k independent gross-matched null books drawing N names uniformly from the
          eligible set, N on the ladder {2, 3, 5, 10, 20, 40}.  More names -> each book
          is closer to the pool average -> higher cross-book correlation.
  D_POOL  the same, N fixed at 20, but drawing from the top-q fraction of the eligible
          set by the frozen composite, q on the ladder {0.02, 0.05, 0.10, 0.25, 0.50,
          1.00}.  A narrower pool forces overlap -> higher correlation, and the narrowest
          rung is a built-in degenerate control (books become the same book).
  D_SYNTH the KNOWN-ANSWER control: k Gaussian series calibrated to the anchor book's own
          mean and vol with rho IMPOSED at {0.00, 0.20, 0.40, 0.60, 0.80, 0.95}, pushed
          through the identical measurement pipeline.  If R_corr does not read 1 there,
          the pipeline is wrong and nothing else in the run means anything.

  NOT dials, reported at every value: PANEL (rule 9) is the second dial but every panel is
  reported everywhere anyway; the rung ladders above; k {4, 8}; the SD BASIS {S_IID,
  S_BLOCK} (63-day moving block); the statistic {Sharpe headline, CAGR}; the record's four
  real ladders {N, H, GROSS, CADENCE} at their committed rungs; the 4a and 4b legs; the
  rule-8 walk-forward arm.

FROZEN at the 2026-09-04 KEEP-4b candidate's construction, exactly as 1205 and 1225 froze
it: composite = mean of the percentile ranks of (12-1, 6m, 3m), NO vol scaler, eligibility
= above own 200d MA and vol20 < 0.60, top-N equal weight at g/N of NAV, gated-out weight to
CASH at 0%, 10 bps per unit turnover (rule 2), next-day execution (LAG 1), warm-up 260
rows, IS ends 2016-12-31.  ANCHOR = N 20 / H 126 / gross 0.75 / weekly.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists; SMALL is the current
output of a sub-$2B screen (data/SMALL_PANEL_README.md) less the documented max_1d_move
>= 1.0 exclusion.  Every CAGR and drawdown LEVEL here is optimistic and every 4a/4b count
is an UPPER bound.  R, R_corr and rho are ratios of one construction against itself on one
tape, so the bias very largely cancels out of them; it does NOT cancel out of the rule-8
OOS levels or the 4b legs.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-17"
SLUG = "what-IS-the-right-NULL-for-a-LADDER-if-rung-DISPERSION-is-HALF-a-RUNG-s-OWN-SAMPLING-SE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ---------------------------------------------------------------- frozen construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

# ------------------------------------------------------------------------ dial 1
DRIVERS = ["D_N", "D_POOL", "D_SYNTH"]
N_RUNGS = [2, 3, 5, 10, 20, 40]
Q_RUNGS = [0.02, 0.05, 0.10, 0.25, 0.50, 1.00]
RHO_RUNGS = [0.00, 0.20, 0.40, 0.60, 0.80, 0.95]
K_BOOKS = 8
K_SUB = 4                                    # the k = 4 robustness column

# the record's four committed ladders, for ARM B / ARM C
N_REC = [5, 8, 10, 12, 15, 20, 25, 30, 40]
H_REC = [21, 63, 126]
G_REC = [0.30, 0.40, 0.50, 0.60, 0.70, 0.75, 0.85, 1.00]
C_REC = [1, 5, 21, 63]
REAL_LADDERS = {"N": N_REC, "H": H_REC, "GROSS": G_REC, "CADENCE": C_REC}
DEGENERATE_BY_1189 = {"GROSS"}               # the dial 1189 called degenerate, pre-declared

BASES = ["S_IID", "S_BLOCK"]
L_BLOCK, BDRAWS, CHUNK = 63, 300, 60
SEED_BASE = 12181218
USEFUL_LO, USEFUL_HI = 0.5, 2.0              # the pre-registered "useful bar" band

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<7s} {'PASS' if ok else 'FAIL'}  {what:<66s} {value:.4e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, bar, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, bar=bar, measured=str(measured),
                    supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ============================================================ d2, the control-chart constant
_QUAD: dict = {}


def _quad():
    if not _QUAD:
        from math import erf, sqrt
        xs = np.linspace(-12.0, 12.0, 400001)
        _QUAD["xs"] = xs
        _QUAD["F"] = 0.5 * (1.0 + np.vectorize(erf)(xs / sqrt(2.0)))
    return _QUAD["xs"], _QUAD["F"]


def d2(k: int) -> float:
    """E[range of k iid standard normals] = int [1 - F^k - (1-F)^k] dx (exact quadrature)."""
    if k < 2:
        return 0.0
    xs, F = _quad()
    y = 1.0 - F ** k - (1.0 - F) ** k
    trap = getattr(np, "trapezoid", None) or np.trapz
    return float(trap(y, xs))


_D2: dict = {}


def D2(k):
    if k not in _D2:
        _D2[k] = d2(k)
    return _D2[k]


_D3: dict = {}
D3_REPS = 200_000


def D3(k: int) -> float:
    """d3(k) = SD of the range of k iid standard normals (Monte Carlo, seeded).  d3/d2 is the
    coefficient of variation of a ONE-DRAW range statistic -- i.e. the sampling SD of R itself
    under R's own null, which is what says whether a single ladder's R can certify anything."""
    if k < 2:
        return 0.0
    if k not in _D3:
        rg = np.random.default_rng(seed_of("d3", k))
        X = rg.standard_normal((D3_REPS, k))
        _D3[k] = float((X.max(axis=1) - X.min(axis=1)).std(ddof=1))
    return _D3[k]


# ================================================================= the record's runner
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / vol if vol else np.nan


def legs_composite(px):
    parts = []
    for skip, look in LEGS:
        x = (px.shift(skip) / px.shift(look) - 1.0) if skip else (px / px.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    return sum(parts) / len(parts)


def mech(px):
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    sc = comp * (0.5 + 0.5 * above.astype(float))
    return sc.values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]
            young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = rank_key[t].copy()
            k[~(elig[t] & priced[t])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new_cur = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new_cur[c] = cur[c]
        for c in take:
            new_cur[c] = t
        cur = new_cur
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, sel] = gross / len(sel)
    return W


def windows_of(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, ins_m, oos_m):
    """r is ALREADY warm-up trimmed; ins_m / oos_m are masks on that trimmed series."""
    c, s, d = fmet(r)
    h = len(r) // 2
    oc, os_, od = fmet(r[oos_m])
    ic, is_, idd = fmet(r[ins_m])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[:h]), H2=fsharpe(r[h:]),
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def legs_4b(b, sb):
    return {"L_H1": bool(b["H1"] > sb["H1"]), "L_H2": bool(b["H2"] > sb["H2"]),
            "L_OOS": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "L_DD": bool(abs(b["MaxDD"]) <= DD_CAP * abs(sb["MaxDD"])),
            "L_CAGR": bool(b["CAGR"] >= CAGR_FLOOR * sb["CAGR"])}


def legs_4b_oos(b, sb):
    return {"O_S": bool(b["OOS_Sharpe"] > sb["OOS_Sharpe"]),
            "O_DD": bool(abs(b["OOS_MaxDD"]) <= DD_CAP * abs(sb["OOS_MaxDD"])),
            "O_CAGR": bool(b["OOS_CAGR"] >= CAGR_FLOOR * sb["OOS_CAGR"])}


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


# ==================================================== the paired bootstrap, the whole engine
def boot_index(T, basis, rng, ndraw):
    if basis == "S_IID":
        return rng.integers(0, T, size=(ndraw, T))
    nb = int(np.ceil(T / L_BLOCK))
    st = rng.integers(0, T, size=(ndraw, nb))
    idx = (st[:, :, None] + np.arange(L_BLOCK)[None, None, :]) % T
    return idx.reshape(ndraw, nb * L_BLOCK)[:, :T]


def paired_sharpes(R, basis, tag, B=BDRAWS):
    """R is (k, T) daily net returns.  ONE resampled day index per draw is applied to ALL k
    books (paired), so the returned (B, k) matrix carries the JOINT sampling distribution of
    the k Sharpes -- which is what d2 must be corrected for."""
    R = np.asarray(R, float)
    k, T = R.shape
    rng = np.random.default_rng(seed_of("boot", basis, tag))
    out = np.empty((B, k))
    done = 0
    while done < B:
        nd = min(CHUNK, B - done)
        idx = boot_index(T, basis, rng, nd)
        for j in range(k):
            x = R[j][idx]
            mu = x.mean(axis=1) * 252.0
            sg = x.std(axis=1, ddof=1) * np.sqrt(252.0)
            out[done:done + nd, j] = np.where(sg > 0, mu / sg, np.nan)
        done += nd
    return out


def mean_pair_corr(M):
    """Mean off-diagonal Pearson correlation of the columns of M."""
    M = np.asarray(M, float)
    if M.shape[1] < 2:
        return np.nan
    sd = M.std(axis=0, ddof=1)
    if np.any(~np.isfinite(sd)) or np.any(sd <= 0):
        return 1.0                       # identical columns -> perfectly correlated
    C = np.corrcoef(M, rowvar=False)
    k = C.shape[0]
    iu = np.triu_indices(k, 1)
    return float(np.nanmean(C[iu]))


def daily_pair_corr(R):
    R = np.asarray(R, float)
    sd = R.std(axis=1, ddof=1)
    if np.any(sd <= 0):
        return 1.0
    C = np.corrcoef(R)
    iu = np.triu_indices(C.shape[0], 1)
    return float(np.nanmean(C[iu]))


def measure(R, basis, tag, k=None):
    """The whole statistic set for one family of books.  R is (k, T)."""
    R = np.asarray(R, float)
    if k is None:
        k = R.shape[0]
    R = R[:k]
    S = np.array([fsharpe(r) for r in R])
    rng_S = float(np.nanmax(S) - np.nanmin(S))
    BS = paired_sharpes(R, basis, tag)
    sd1 = float(np.nanmean(np.nanstd(BS, axis=0, ddof=1)))
    rho_S = mean_pair_corr(BS)
    rho_r = daily_pair_corr(R)
    dk = D2(k)
    Rraw = rng_S / (dk * sd1) if sd1 > 0 else np.nan
    corr_fac = np.sqrt(max(1.0 - rho_S, 1e-12))
    Rcorr = Rraw / corr_fac if np.isfinite(Rraw) else np.nan
    Rb = (np.nanmax(BS, axis=1) - np.nanmin(BS, axis=1)) / (dk * sd1) if sd1 > 0 else np.array([np.nan])
    lo, hi = (float(np.nanpercentile(Rb, 5)), float(np.nanpercentile(Rb, 95)))
    null_sd = D3(k) / dk                       # sampling SD of R under R's OWN null
    return dict(k=k, sd_basis=basis, range_S=rng_S, sd1=sd1, rho_S=rho_S, rho_r=rho_r,
                d2k=dk, d3k=D3(k), null_sd_R=null_sd, R=Rraw, R_corr=Rcorr,
                sqrt1mrho=corr_fac, amplification=1.0 / corr_fac,
                z_corr=(Rcorr - 1.0) / null_sd if np.isfinite(Rcorr) else np.nan,
                R_lo=lo, R_hi=hi, mean_S=float(np.nanmean(S)), sd_cross=float(np.nanstd(S, ddof=1)))


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 3:
        return np.nan
    rx, ry = pd.Series(x).rank().values, pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def auc(pos, neg):
    """P(a random degenerate ladder scores BELOW a random live one); 0.5 = no separation."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[np.isfinite(pos)], neg[np.isfinite(neg)]
    if not len(pos) or not len(neg):
        return np.nan
    less = (pos[:, None] < neg[None, :]).sum()
    ties = (pos[:, None] == neg[None, :]).sum()
    return float((less + 0.5 * ties) / (len(pos) * len(neg)))


# =================================================================================================
def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def stride_mask(T, k):
    m = np.zeros(T, dtype=bool)
    m[np.arange(k - 1, T, k)] = True
    return m


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1218 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P("")

    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    small, ndrop, nmeta = load_small()
    raw["SMALL"] = small
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        panels[panel] = dict(px=px, idx=idx, K=K, T=T, spy_i=spy_i,
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values, warm=warm,
                             ins_m=ins[warm], oos_m=oos[warm],
                             sc=sc, elig=elig)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    # ---------------------------------------------------------------- the book constructor
    def run_W(panel, W, mk):
        d = panels[panel]
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return (g - tn * COST / 1e4)[d["warm"]]

    _SEL: dict = {}

    def selection(panel, N, H, cadence):
        key = (panel, N, H, cadence)
        anchor = (N, H, cadence) == (N0, HOLD0, "W")
        if anchor and key in _SEL:
            return _SEL[key]
        d = panels[panel]
        mk = (rebalance_mask(d["idx"], FREQ0).values if cadence == "W"
              else stride_mask(d["T"], int(cadence)))
        W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk),
                  N, H, d["T"], d["K"], 1.0)
        if anchor:
            _SEL.clear()
            _SEL[key] = (W, mk)
        return W, mk

    def book(panel, N=N0, H=HOLD0, gross=GROSS0, cadence="W"):
        W, mk = selection(panel, N, H, cadence)
        return run_W(panel, W * gross, mk)

    def null_book(panel, seed, N=N0, q=1.00, gross=GROSS0):
        """A gross-matched RANDOM book: at each weekly rebalance draw N names uniformly from
        the top-q fraction (by the frozen composite) of those priced AND eligible that day,
        at gross/N.  Independent across seeds; q = 1.00 is 1205's CTRL_LIVE."""
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("null", panel, seed, N, q))
        W = np.zeros((d["T"], d["K"]))
        ok = d["elig"] & d["priced"]
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if not len(cand):
                continue
            if q < 1.0:
                m = max(1, int(np.ceil(q * len(cand))))
                order = np.argsort(-d["sc"][t, cand], kind="stable")
                cand = cand[order[:m]]
            sel = rng.choice(cand, size=min(N, len(cand)), replace=False)
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            W[t:stop, sel] = gross / len(sel)
        return run_W(panel, W, mk)

    # ------------------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    v = abs(D2(2) - 2.0 / np.sqrt(np.pi))
    gate("G_D2", "d2(2) == 2/sqrt(pi) (quadrature vs closed form)", v, v < 1e-6)
    v = abs(D2(8) - 2.847)
    gate("G_D2b", "d2(8) == 2.847 (published control-chart table)", v, v < 5e-4)
    # G_LAW: the correction identity itself, on pure equicorrelated normals
    rngL = np.random.default_rng(seed_of("law"))
    worst = 0.0
    for rho in RHO_RUNGS:
        Z0 = rngL.standard_normal((20000, 1))
        E = rngL.standard_normal((20000, K_BOOKS))
        X = np.sqrt(rho) * Z0 + np.sqrt(1 - rho) * E
        got = (X.max(axis=1) - X.min(axis=1)).mean() / D2(K_BOOKS)
        worst = max(worst, abs(got - np.sqrt(1 - rho)))
    gate("G_LAW", "E[range]/d2(k) == sqrt(1-rho) on equicorrelated normals (worst rho)",
         worst, worst < 0.02)
    v = abs(D3(2) - 0.8525)
    gate("G_D3", "d3(2) == 0.8525 (published control-chart table; Monte Carlo)", v, v < 5e-3)
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0,
              d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast = run_W("U56", W, mk)
    v = float(np.abs(eng[d["warm"]] - rfast).max())
    gate("G1", "fast runner == engine.backtest (U56 anchor, post warm-up)", v, v < 1e-12)
    a = book("U56")
    gate("G2", "book() == the gate's own anchor path", float(np.abs(a - rfast).max()),
         float(np.abs(a - rfast).max()) < 1e-14)
    b1, b2 = book("U56", N=12), book("U56", N=12)
    gate("G3", "determinism: same book twice", float(np.abs(b1 - b2).max()),
         float(np.abs(b1 - b2).max()) == 0.0)
    n1, n2 = null_book("U56", 0), null_book("U56", 1)
    v = float(abs(np.corrcoef(n1, n2)[0, 1]))
    gate("G4", "two null books are NOT the same path (|corr| < 0.99)", v, v < 0.99)
    # G5: a paired bootstrap of ONE book against ITSELF must read rho_S = 1 exactly
    m_self = measure(np.vstack([n1, n1]), "S_IID", "selfpair")
    gate("G5", "paired bootstrap of a book against itself reads rho_S == 1",
         abs(m_self["rho_S"] - 1.0), abs(m_self["rho_S"] - 1.0) < 1e-9)
    P("")

    # ------------------------------------------------------- benchmarks, once per panel
    P("## BENCHMARKS (per panel, 10 bps, next-day execution, post warm-up)")
    bench = {}
    for panel in PANELS:
        dd = panels[panel]
        spy = dd["px"]["SPY"].pct_change().fillna(0.0).values[dd["warm"]]
        live = run_W(panel, rules_v2_weights(dd["px"]).values,
                     rebalance_mask(dd["idx"], FREQ0).values)
        anc = book(panel)
        bench[panel] = dict(SPY=blocks_m(spy, dd["ins_m"], dd["oos_m"]),
                            LIVE=blocks_m(live, dd["ins_m"], dd["oos_m"]),
                            ANCHOR=blocks_m(anc, dd["ins_m"], dd["oos_m"]))
        for kk in ("SPY", "LIVE", "ANCHOR"):
            m = bench[panel][kk]
            P(f"  {panel:<6s} {kk:<7s} {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:8.2%}"
              f"  halves {m['H1']:.4f}/{m['H2']:.4f}  OOS {m['OOS_CAGR']:7.2%} / "
              f"{m['OOS_Sharpe']:.4f} / {m['OOS_MaxDD']:8.2%}")
    P("")

    # ============================== ARM 1: R as a function of cross-book correlation
    P("## ARM 1 — R and R_corr along every CORR DRIVER ladder, every panel, every SD basis")
    P("##         (k = 8 books per rung; the k = 4 column is the same books' first four)")
    rows = []
    for panel in PANELS:
        dd = panels[panel]
        anc = book(panel)
        for driver in DRIVERS:
            rungs = {"D_N": N_RUNGS, "D_POOL": Q_RUNGS, "D_SYNTH": RHO_RUNGS}[driver]
            for rung in rungs:
                if driver == "D_N":
                    R = np.vstack([null_book(panel, s, N=rung) for s in range(K_BOOKS)])
                elif driver == "D_POOL":
                    R = np.vstack([null_book(panel, 100 + s, N=N0, q=rung)
                                   for s in range(K_BOOKS)])
                else:
                    rg = np.random.default_rng(seed_of("synth", panel, rung))
                    T = len(anc)
                    mu, sg = anc.mean(), anc.std(ddof=1)
                    Z0 = rg.standard_normal((T, 1))
                    E = rg.standard_normal((T, K_BOOKS))
                    R = (mu + sg * (np.sqrt(rung) * Z0 + np.sqrt(1 - rung) * E)).T
                for basis in BASES:
                    for k in (K_BOOKS, K_SUB):
                        m = measure(R, basis, f"{panel}|{driver}|{rung}|{k}", k=k)
                        rows.append(dict(panel=panel, driver=driver, rung=rung, **m))
                mm = [r for r in rows[-4:] if r["k"] == K_BOOKS and r["sd_basis"] == "S_IID"][0]
                P(f"  {panel:<6s} {driver:<8s} rung={str(rung):<5s} rho_r {mm['rho_r']:.4f} "
                  f"rho_S {mm['rho_S']:.4f}  range {mm['range_S']:.4f}  sd1 {mm['sd1']:.4f}  "
                  f"R {mm['R']:.4f} [{mm['R_lo']:.3f},{mm['R_hi']:.3f}]  "
                  f"R_corr {mm['R_corr']:.4f}")
    arm1 = pd.DataFrame(rows)
    dump(arm1, "corrladder")
    P("")

    # ------------------------------------------------- the 9-cell dial grid, all published
    P("## THE 9-CELL DIAL GRID (CORR DRIVER x PANEL), headline basis S_IID, k = 8")
    g = arm1[(arm1.sd_basis == "S_IID") & (arm1.k == K_BOOKS)]
    cells = []
    for panel in PANELS:
        for driver in DRIVERS:
            s = g[(g.panel == panel) & (g.driver == driver)]
            cells.append(dict(
                panel=panel, driver=driver, n_rungs=len(s),
                rho_S_min=s.rho_S.min(), rho_S_max=s.rho_S.max(),
                rho_r_min=s.rho_r.min(), rho_r_max=s.rho_r.max(),
                R_min=s.R.min(), R_max=s.R.max(), R_mean=s.R.mean(),
                Rcorr_min=s.R_corr.min(), Rcorr_max=s.R_corr.max(), Rcorr_mean=s.R_corr.mean(),
                rho_span=s.rho_S.max() - s.rho_S.min(),
                spearman_R_rho=spearman(s.rho_S.values, s.R.values),
                n_Rcorr_in_band=int(((s.R_corr >= USEFUL_LO) & (s.R_corr <= USEFUL_HI)).sum()),
                max_abs_Rcorr_dev=float(np.nanmax(np.abs(s.R_corr.values - 1.0)))))
    cellsdf = pd.DataFrame(cells)
    dump(cellsdf, "dialgrid")
    for _, c in cellsdf.iterrows():
        P(f"  {c.panel:<6s} {c.driver:<8s} rho_S {c.rho_S_min:.4f}->{c.rho_S_max:.4f} "
          f"(span {c.rho_span:.4f})  R {c.R_min:.4f}->{c.R_max:.4f}  "
          f"R_corr mean {c.Rcorr_mean:.4f} (worst dev from 1: {c.max_abs_Rcorr_dev:.4f})  "
          f"spearman(R, rho_S) {c.spearman_R_rho:+.4f}")
    P("")

    # ------------------------------------------------------------- pre-registered hypotheses
    P("## PRE-REGISTERED HYPOTHESES (declared in the header before any number was read)")
    syn = g[g.driver == "D_SYNTH"]
    worst_syn = float(np.nanmax(np.abs(syn.R_corr.values - 1.0)))
    hyp("H_LAW", "R_corr in [0.85, 1.15] at every imposed rho on D_SYNTH", "0.15",
        f"worst |R_corr - 1| = {worst_syn:.4f} over {len(syn)} synthetic rungs",
        worst_syn <= 0.15)
    real = g[g.driver != "D_SYNTH"]
    sps = [spearman(real[(real.panel == p) & (real.driver == dv)].rho_S.values,
                    real[(real.panel == p) & (real.driver == dv)].R.values)
           for p in PANELS for dv in ("D_N", "D_POOL")]
    hyp("H_MONO", "R falls with rho_S on every real driver ladder (spearman <= -0.8)", "-0.80",
        f"spearman per cell {['%.3f' % x for x in sps]}",
        all(np.isfinite(x) and x <= -0.8 for x in sps))
    spans = [float(real[(real.panel == p) & (real.driver == dv)].rho_S.max()
                   - real[(real.panel == p) & (real.driver == dv)].rho_S.min())
             for p in PANELS for dv in ("D_N", "D_POOL")]
    hyp("H_DRIVER", "each real driver moves rho_S by >= 0.20 on each panel", "0.20",
        f"spans {['%.3f' % x for x in spans]}", all(x >= 0.20 for x in spans))
    # the 1205 reading, re-measured: CTRL_LIVE is D_POOL q=1.00 == D_N N=20
    live_rows = g[(g.driver == "D_POOL") & (g.rung == 1.00)]
    pred_rho = 1.0 - 0.4186 ** 2
    hyp("H_1205", "if 1205's R=0.4186 is pure correlation, rho_S ~ 0.825 on CTRL_LIVE", "0.825",
        f"measured rho_S {['%.4f' % x for x in live_rows.rho_S.values]} "
        f"(R {['%.4f' % x for x in live_rows.R.values]}), predicted {pred_rho:.4f}",
        bool(np.all(np.abs(live_rows.rho_S.values - pred_rho) < 0.15)))
    P("")

    # -------------------------- ARM 1c — POST-HOC (declared as such): the POWER of one R
    P("## ARM 1c — POST-HOC, NOT PRE-REGISTERED.  H_LAW was declared at +-0.15 on a SINGLE")
    P("##          rung.  R is a ONE-DRAW range statistic, so its own null SD is d3(k)/d2(k).")
    P("##          This arm prices that, and re-reads the law where it CAN be read: pooled.")
    pw = pd.DataFrame([dict(k=k, d2=D2(k), d3=D3(k), null_sd_R=D3(k) / D2(k),
                            band_95=f"[{1 - 1.96 * D3(k) / D2(k):.3f}, {1 + 1.96 * D3(k) / D2(k):.3f}]")
                       for k in (2, 3, 4, 8, 9, 12)])
    dump(pw, "power")
    for _, r in pw.iterrows():
        P(f"    k={int(r.k):<3d} d2 {r.d2:.4f}  d3 {r.d3:.4f}  null SD of R {r.null_sd_R:.4f}  "
          f"95% band for a single TRUE-null R_corr {r.band_95}")
    pool = []
    for driver in DRIVERS + ["D_POOL_nondegen"]:
        # D_POOL_nondegen drops the rungs whose pool is smaller than N, where all k books are
        # literally the SAME book (range exactly 0, rho exactly 1) and R_corr is 0/0 -> 0.
        s = (g[(g.driver == "D_POOL") & (g.range_S > 0)] if driver == "D_POOL_nondegen"
             else g[g.driver == driver])
        sd_one = float(np.nanmean(s.null_sd_R))
        m = float(np.nanmean(s.R_corr))
        se = sd_one / np.sqrt(len(s))
        pool.append(dict(driver=driver, n_rungs=len(s), mean_R_corr=m, se=se,
                         z=(m - 1.0) / se, mean_R=float(np.nanmean(s.R))))
    pooldf = pd.DataFrame(pool)
    dump(pooldf, "pooledlaw")
    for _, r in pooldf.iterrows():
        P(f"    {r.driver:<8s} mean R_corr over {int(r.n_rungs)} rungs = {r.mean_R_corr:.4f} "
          f"(SE {r.se:.4f}, z vs 1 = {r.z:+.2f}), mean RAW R = {r.mean_R:.4f}")
    P("")

    # ============================== ARM 2: the record's four real ladders under both bars
    P("## ARM 2 — the record's four committed ladders: R, rho_S, R_corr (full sample)")
    ladder_books: dict = {}
    lrows = []
    for panel in PANELS:
        dd = panels[panel]
        for lad, rungs in REAL_LADDERS.items():
            Rs, mets = [], []
            for rung in rungs:
                if lad == "N":
                    r = book(panel, N=rung)
                elif lad == "H":
                    r = book(panel, H=rung)
                elif lad == "GROSS":
                    r = book(panel, gross=rung)
                else:
                    r = book(panel, cadence=("W" if rung == 5 else rung))
                Rs.append(r)
                mets.append(blocks_m(r, dd["ins_m"], dd["oos_m"]))
            Rs = np.vstack(Rs)
            ladder_books[(panel, lad)] = (Rs, mets, rungs)
            for basis in BASES:
                m = measure(Rs, basis, f"real|{panel}|{lad}")
                # the same statistics on the IS window only (what a rule-8 chooser may see)
                mi = measure(Rs[:, dd["ins_m"]], basis, f"realIS|{panel}|{lad}")
                lrows.append(dict(panel=panel, ladder=lad,
                                  degenerate_by_1189=lad in DEGENERATE_BY_1189, **m,
                                  IS_rho_S=mi["rho_S"], IS_R=mi["R"], IS_R_corr=mi["R_corr"],
                                  IS_range=mi["range_S"], IS_sd1=mi["sd1"]))
            mm = lrows[-2]
            P(f"  {panel:<6s} {mm['ladder']:<8s} k={mm['k']:<2d} rho_r {mm['rho_r']:.4f} "
              f"rho_S {mm['rho_S']:.4f}  range {mm['range_S']:.4f}  sd1 {mm['sd1']:.4f}  "
              f"R {mm['R']:.4f} [{mm['R_lo']:.3f},{mm['R_hi']:.3f}]  R_corr {mm['R_corr']:.4f}"
              f"  (x{mm['amplification']:.1f}, z {mm['z_corr']:+.2f})")
    arm2 = pd.DataFrame(lrows)
    dump(arm2, "realladders")

    a2 = arm2[arm2.sd_basis == "S_IID"]
    n_raw_clear = int((a2.R >= 1.0).sum())
    n_corr_clear = int((a2.R_corr >= 1.0).sum())
    n_band = int(((a2.R_corr >= USEFUL_LO) & (a2.R_corr <= USEFUL_HI)).sum())
    P(f"  RAW bar R >= 1 cleared by {n_raw_clear} of {len(a2)} real ladders; "
      f"CORRECTED bar R_corr >= 1 cleared by {n_corr_clear} of {len(a2)}; "
      f"R_corr inside the pre-registered useful band [{USEFUL_LO}, {USEFUL_HI}] at {n_band}.")
    nz = int((np.abs(a2.z_corr.values) > 1.96).sum())
    P(f"  POWER: |z| > 1.96 against the CORRECTED null at {nz} of {len(a2)} real ladders "
      f"(worst |z| {np.nanmax(np.abs(a2.z_corr.values)):.2f}); the same count on the "
      f"{len(g)} driver rungs is {int((np.abs(g.z_corr.values) > 1.96).sum())}.")
    hyp("H_REAL", "a correlation-corrected d2 gives a bar a REAL ladder can clear "
        "(R_corr >= 1 at >= 1 of 12 real ladders)", "1 of 12",
        f"{n_corr_clear} of {len(a2)} clear; raw bar cleared by {n_raw_clear}",
        n_corr_clear >= 1)
    hyp("H_USEFUL", "the corrected bar is a BAR, not a formality: it separates, i.e. "
        "not all 12 real ladders sit above it and not all sit below", "1..11 of 12",
        f"{n_corr_clear} of {len(a2)} above", 1 <= n_corr_clear <= len(a2) - 1)
    deg = a2[a2.degenerate_by_1189]
    liv = a2[~a2.degenerate_by_1189]
    sep = pd.DataFrame([dict(statistic=s,
                             auc_degenerate_below_live=auc(deg[s].values, liv[s].values),
                             degen_mean=float(deg[s].mean()), live_mean=float(liv[s].mean()))
                        for s in ("range_S", "R", "R_corr", "rho_S")])
    dump(sep, "separation")
    for _, s in sep.iterrows():
        P(f"  separation {s.statistic:<9s} AUC {s.auc_degenerate_below_live:.4f}  "
          f"(GROSS mean {s.degen_mean:.4f} vs live dials {s.live_mean:.4f})")
    P("  AMPLIFICATION — the correction multiplies the raw R by 1/sqrt(1-rho_S); at rho_S -> 1")
    P("  that factor and its own estimation error both diverge, so R_corr on a degenerate")
    P("  ladder is a ratio of two numbers that are both ~0:")
    for _, r in a2.sort_values("amplification", ascending=False).iterrows():
        drho = (1.0 - r.rho_S) * 0.75          # the rho error that doubles R_corr (1/sqrt(1-rho))
        P(f"    {r.panel:<6s} {r.ladder:<8s} rho_S {r.rho_S:.6f}  x{r.amplification:8.1f}  "
          f"a rho error of {drho:.2e} doubles R_corr")
    P("")

    # ============================== ARM 3: RULE 8 WALK-FORWARD + both KEEP paths
    P("## ARM 3 — RULE 8 WALK-FORWARD.  Every chooser reads the IS window (warm-up..2016-12-31)")
    P("##         ONLY; 2017-2026 is read ONCE.  Five move-or-stay rules, 12 decisions each.")
    # IS-only bars, so the rules are honest:
    isb = arm2[arm2.sd_basis == "S_IID"].set_index(["panel", "ladder"])
    raw_bar = {p: float(isb.loc[p].IS_R.median()) for p in PANELS}
    P(f"  IS-only RAW bar per panel (median IS_R over that panel's four ladders): "
      + ", ".join(f"{p} {raw_bar[p]:.4f}" for p in PANELS))
    picks = []
    for panel in PANELS:
        sb, lb, an = bench[panel]["SPY"], bench[panel]["LIVE"], bench[panel]["ANCHOR"]
        for lad, rungs in REAL_LADDERS.items():
            Rs, mets, rl = ladder_books[(panel, lad)]
            iss = np.array([m["IS_Sharpe"] for m in mets])
            j = int(np.nanargmax(iss))
            row = isb.loc[(panel, lad)]
            anchor_rung = {"N": N0, "H": HOLD0, "GROSS": GROSS0, "CADENCE": 5}[lad]
            ja = rl.index(anchor_rung)
            rules = {
                "C_STAY": False,
                "C_ALWAYS": True,
                "C_RAW": bool(row.IS_R >= raw_bar[panel]),
                "C_CORR": bool(row.IS_R_corr >= 1.0),
                "C_CORRBAND": bool(row.IS_R_corr >= 1.0 and row.IS_rho_S <= 0.99),
            }
            for rule, move in rules.items():
                jj = j if move else ja
                ch, m = rl[jj], mets[jj]
                l4b, l4o, l4a = legs_4b(m, sb), legs_4b_oos(m, sb), legs_4a(m, lb)
                picks.append(dict(
                    panel=panel, ladder=lad, rule=rule, moved=bool(jj != ja),
                    chosen_rung=ch, anchor_rung=anchor_rung, k=len(rl),
                    IS_R=float(row.IS_R), IS_R_corr=float(row.IS_R_corr),
                    IS_rho_S=float(row.IS_rho_S), IS_Sharpe=m["IS_Sharpe"],
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                    H1=m["H1"], H2=m["H2"],
                    OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"], OOS_MaxDD=m["OOS_MaxDD"],
                    anchor_OOS_Sharpe=an["OOS_Sharpe"], SPY_OOS_Sharpe=sb["OOS_Sharpe"],
                    LIVE_OOS_Sharpe=lb["OOS_Sharpe"],
                    SPY_OOS_CAGR=sb["OOS_CAGR"], SPY_OOS_MaxDD=sb["OOS_MaxDD"],
                    **l4b, **l4o, **l4a,
                    pass_4b_full=all(l4b.values()), pass_4b_oos=all(l4o.values()),
                    pass_4a=all(l4a.values())))
    picks = pd.DataFrame(picks)
    dump(picks, "walkforward")
    P("  per-rule summary (12 decisions each):")
    for rule in ("C_STAY", "C_ALWAYS", "C_RAW", "C_CORR", "C_CORRBAND"):
        s = picks[picks.rule == rule]
        P(f"    {rule:<11s} move rate {s.moved.mean():.4f}  mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}"
          f"  mean OOS CAGR {s.OOS_CAGR.mean():7.2%}  mean OOS MaxDD {s.OOS_MaxDD.mean():8.2%}"
          f"  4a {int(s.pass_4a.sum())}/12  4b full {int(s.pass_4b_full.sum())}/12"
          f"  4b OOS {int(s.pass_4b_oos.sum())}/12")
    P(f"  reference: mean anchor OOS Sharpe {picks[picks.rule=='C_STAY'].OOS_Sharpe.mean():.4f}; "
      f"SPY OOS Sharpe per panel " + ", ".join(
          f"{p} {bench[p]['SPY']['OOS_Sharpe']:.4f}" for p in PANELS) + "; live RULES v2 " +
      ", ".join(f"{p} {bench[p]['LIVE']['OOS_Sharpe']:.4f}" for p in PANELS))
    for _, p_ in picks[picks.rule != "C_STAY"].iterrows():
        if p_.moved:
            P(f"    MOVE {p_.panel:<6s} {p_.ladder:<8s} {p_.rule:<11s} "
              f"{p_.anchor_rung} -> {p_.chosen_rung}  OOS {p_.OOS_CAGR:7.2%} / "
              f"{p_.OOS_Sharpe:.4f} / {p_.OOS_MaxDD:8.2%}  (anchor {p_.anchor_OOS_Sharpe:.4f})")
    P(f"  4a passes {int(picks.pass_4a.sum())} of {len(picks)}; "
      f"4b full {int(picks.pass_4b_full.sum())}; 4b OOS {int(picks.pass_4b_oos.sum())}; "
      f"BOTH {int((picks.pass_4b_full & picks.pass_4b_oos).sum())}")
    # idea 1211's lesson: count BOOKS, not decision rows.  A do-nothing rule reselects the
    # SAME anchor book at every ladder, so 4b row counts inflate by up to 4x here.
    pb = picks[picks.pass_4b_full]
    pb_books = sorted({(r.panel, r.ladder if r.moved else "ANCHOR", r.chosen_rung)
                       for _, r in pb.iterrows()})
    P(f"  BOOK IDENTITY (rule 1211): the {len(pb)} 4b-passing decision rows collapse to "
      f"{len(pb_books)} DISTINCT books: {pb_books}")
    P(f"  of those, books that are the FROZEN ANCHOR (already in the record, not new): "
      f"{sum(1 for b in pb_books if b[1] == 'ANCHOR')}")
    best = picks.sort_values("OOS_Sharpe", ascending=False).iloc[0]
    P(f"  BEST rule-8 book anywhere in the run: {best.panel} {best.ladder} rung {best.chosen_rung}"
      f" — full {best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%} "
      f"(halves {best.H1:.4f}/{best.H2:.4f}), OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / "
      f"{best.OOS_MaxDD:.2%}")
    P("")

    # ------------------------------------------- does R_corr predict what a move is worth?
    P("## ARM 3b — does R (or R_corr) predict the OOS value of moving on that ladder?")
    al = picks[picks.rule == "C_ALWAYS"].set_index(["panel", "ladder"])
    st = picks[picks.rule == "C_STAY"].set_index(["panel", "ladder"])
    delta = (al.OOS_Sharpe - st.OOS_Sharpe).rename("move_value").reset_index()
    delta = delta.merge(a2.reset_index()[["panel", "ladder", "R", "R_corr", "rho_S", "range_S"]],
                        on=["panel", "ladder"])
    delta["IS_R"] = [float(isb.loc[(r.panel, r.ladder)].IS_R) for _, r in delta.iterrows()]
    delta["IS_R_corr"] = [float(isb.loc[(r.panel, r.ladder)].IS_R_corr) for _, r in delta.iterrows()]
    dump(delta, "movevalue")
    for s in ("IS_R", "IS_R_corr", "R", "R_corr", "range_S", "rho_S"):
        P(f"    spearman(move_value, {s:<9s}) = {spearman(delta[s].values, delta.move_value.values):+.4f}")
    P(f"    mean move_value (C_ALWAYS - C_STAY) = {delta.move_value.mean():+.4f} Sharpe over "
      f"{len(delta)} ladders; positive at {int((delta.move_value > 0).sum())} of {len(delta)}")
    P("")

    dump(pd.DataFrame(GATES), "gates")
    dump(pd.DataFrame(HYP), "hypotheses")
    P(f"## GATES {sum(x['pass_'] for x in GATES)} of {len(GATES)} PASS")
    P(f"## RUNTIME {time.time() - t0:.0f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))
    return arm1, cellsdf, arm2, picks, delta


if __name__ == "__main__":
    main()
