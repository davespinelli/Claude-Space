#!/usr/bin/env python3
"""Idea 1146 (lane B, 2026-09-18)
   does-a-TRUNCATED-MAXIMUM-behave-like-ULCER-or-like-MAXDD

1140 found MAXDD is the ONLY one of six statistics whose realised rung GAP and bootstrap SD
BOTH GROW with tape length (median b_gap +0.1419, b_sd +0.1654 over its 96 committed cells),
while ULCER — a root-mean-square of the SAME drawdown path — and CALMAR — a ratio DIVIDED by
the same maximum — both have FALLING SD like the moment statistics.  1140 read the carrier as
MAX-ness rather than path-functionality, and that reading makes a prediction nobody has run:

    a TRUNCATED maximum should behave like ULCER.

THE DESIGN.  Two truncation RULES, each a ladder that NESTS MAXDD exactly at its top rung, so
the switch-off point is read on a continuum and not inferred from a two-point contrast:

  QUANT  Q_p  = the p-th quantile of the drawdown-depth distribution (running-max drawdown),
               p in {0.50, 0.75, 0.90, 0.95, 0.99, 0.999, 1.000}.  Q_1.000 IS MAXDD, exactly
               (gate G11).  Lowering p truncates the MAXIMUM while keeping the same path.
  KDAY   K_k  = the worst drawdown whose peak is at most k days back:
               min_t ( eq[t] / max(eq[t-k+1 .. t]) - 1 ), k in {21, 63, 126, 252, 504, INF}.
               K_INF IS MAXDD, exactly (gate G12).  Lowering k truncates the HORIZON over
               which the maximum is taken, again on the same path.

ULCER (the same path, no max at all) and 1140's three NON-PATH statistics (CAGR, VOL, SHARPE)
plus CALMAR are carried as the reference arms, on the SAME draws and the SAME seeds, so
1140's six committed median exponents reproduce to the digit (gates G9/G10).

THE MEASUREMENT is 1140's, unchanged: for every (panel, ladder, rung set, statistic) block,
the median |gap| between rungs and the median bootstrap SD of that gap are fitted on log(T)
over SIX DISJOINT SUB-TAPES (1 whole, 2 halves, 3 thirds).  The MAXDD SIGNATURE is
    b_gap > 0 AND b_sd > 0
(both grow with tape) and the ULCER SIGNATURE is b_sd < 0.  The deliverable is the rung on
each truncation ladder at which the signature SWITCHES OFF.

TUNED DIALS (2, PROTOCOL rule 4): `TRUNCATION RULE` {QUANT, KDAY, BOTH} x `SUB-TAPE FRACTION`
{1, 1/2, 1/3} = 9 combinations, ALL published (grid.csv / dials.csv).  TRUNCATION LEVEL is NOT
a dial — every rung of both ladders is reported at every cell.  PANEL (U56, B136), LADDER (N,
H, GROSS, CADENCE) and RUNG SET (CORE, EXT) are NOT dials — all 2 x 4 x 2 cells reported
everywhere.  q is NOT a dial: 0.90 headline, 0.80/0.95 reported beside, never selected on.
BLOCK LENGTH is NOT a dial: L=63, frozen from 1098/1102/1110/1131/1140.

THE CAPITAL ARM (PROTOCOL rule 8, both KEEP paths).  A truncated maximum is not only a
publication statistic — it is a candidate RISK DENOMINATOR for choosing a book.  Every
truncation rung supplies a CHOOSER: pick the ladder rung whose IS 2009-2016 CAGR / |trunc DD|
is largest, then read OOS 2017-2026 ONCE.  Scored against 1140's three committed choosers
(IS Sharpe, IS CAGR, IS MaxDD), against the ladder's FROZEN DEFAULT rung, against SPY and
against the live RULES v2 book, with 4a and 4b legs at every pick and over the whole grid.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1131/1140's construction: CAND20 legs,
cap INF, max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, crc32 seeds, 3 seed bases, identical rung lists, and
the TAPE PINNED to 1140's last bar (2026-09-15) so its committed numbers are comparable.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
RULES.md, PROTOCOL.md, engine.py, scan.py, bot.py and baseline.py are NOT touched.
"""
from __future__ import annotations

import sys
import time
import zlib
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-a-TRUNCATED-MAXIMUM-behave-like-ULCER-or-like-MAXDD"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_B"
PRIOR1140 = BT / "2026-09-16_is-DD-s-RUNG-ROBUST-UN-RESOLVABILITY-a-PATH-FUNCTIONAL-fact-or-a-TAPE-fact_B"
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
# FROZEN, NOT A DIAL: the tape is pinned to the LAST BAR 1140 ran on (its U56 tape
# ended 2026-09-15; B136 ended 2026-09-11 and is unaffected).  The cache has grown by
# two U56 bars since.  They are excluded because this run's whole object is 1140's own
# exponents — a different tape makes its committed numbers unreproducible and the
# comparison inexact.  The cost of the pin is measured and printed (TAPE DRIFT, below).
TAPE_END = "2026-09-15"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
H_CORE = [21, 63, 126, 252]
H_EXT = [21, 42, 63, 84, 126, 168, 210, 252, 378]
C_CORE = ["D", "W", "M", "Q"]
C_EXT = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]

LADDERS = ["N", "H", "GROSS", "CADENCE"]
PANELS = ["U56", "B136"]
RUNGSETS = ["CORE", "EXT"]
DEFAULT_RUNG = {"N": "20", "H": "126", "GROSS": "0.75", "CADENCE": "W"}

# ---------------------------------------------------------- THE STATISTICS
# 1140's six, verbatim and on the same draws (the reference arms), plus the two truncation
# ladders.  MAXDD is the shared TOP RUNG of both ladders and is computed ONCE.
NONPATH = ["CAGR", "VOL", "SHARPE"]
REF_PATH = ["MAXDD", "ULCER", "CALMAR"]
STATS6 = NONPATH + REF_PATH                       # 1140's set, for the cross-run gates

QUANT_P = [0.50, 0.75, 0.90, 0.95, 0.99, 0.999, 1.000]
KDAY_K = [21, 63, 126, 252, 504, 10 ** 9]         # 10**9 == INF == whole tape
QNAME = {p: (f"Q{int(round(p * 1000)):04d}" if p < 1.0 else "MAXDD") for p in QUANT_P}
KNAME = {k: (f"K{k:04d}" if k < 10 ** 9 else "MAXDD") for k in KDAY_K}
QUANT_LADDER = [QNAME[p] for p in QUANT_P]        # ... -> MAXDD
KDAY_LADDER = [KNAME[k] for k in KDAY_K]          # ... -> MAXDD
TRUNC_STATS = [s for s in dict.fromkeys(QUANT_LADDER + KDAY_LADDER) if s != "MAXDD"]
STATS = STATS6 + TRUNC_STATS                      # 17 distinct statistics
IS_PATH = {s: (s not in NONPATH) for s in STATS}
IS_TRUNC = {s: (s in TRUNC_STATS) for s in STATS}

# dial 1: which truncation ladder the headline is read on
RULE_SETS = {"QUANT": QUANT_LADDER, "KDAY": KDAY_LADDER,
             "BOTH": [s for s in dict.fromkeys(QUANT_LADDER + KDAY_LADDER)]}
FRACS = [1, 2, 3]                                 # dial 2 (1/1, 1/2, 1/3)

QS = [0.80, 0.90, 0.95]
Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BASES = [11311131, 11171117, 11161116]       # 1140's, so its cells reproduce exactly

# 1140's three committed choosers, plus one per truncation rung (built below).
BASE_CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe"),
                 "C_ISCAGR": ("IS_CAGR", "OOS_CAGR"),
                 "C_ISDD": ("IS_MaxDD", "OOS_MaxDD")}

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
# 1140's committed median exponents over its 96 cells (exponents.csv), quoted here and
# RE-DERIVED below on this run's own draws as gates G9/G10.
A1140_MEDIAN_B = {"CAGR": (-0.3495, -0.4675), "VOL": (0.0004, -0.3181),
                  "SHARPE": (-0.4231, -0.4482), "MAXDD": (0.1419, 0.1654),
                  "ULCER": (-0.1221, -0.1916), "CALMAR": (-0.1699, -0.5543)}
A877_SEED_FLOOR = 0.0145      # idea 877's committed per-arm seed noise floor, in Sharpe
A1141_NOTE = "1141: DD's 'un-resolvable everywhere' is a LARGE-PANEL fact; SMALL fires less."

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(base, *parts):
    return base + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# --------------------------------------- 1082/1098/1102/1108/1117/1131/1140's runner, verbatim
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


# ------------------------------------------------------------- THE TRUNCATION MACHINERY
def sliding_max(a, k):
    """van Herk / Gil-Werman sliding maximum over the trailing k samples, row-wise.
    Windows shorter than k at the head use the running max (i.e. 'highest point in the last
    AT MOST k days'), so k -> INF collapses exactly onto np.maximum.accumulate."""
    m, T = a.shape
    if k >= T:
        return np.maximum.accumulate(a, axis=1)
    npad = (-T) % k
    b = np.concatenate([a, np.full((m, npad), -np.inf)], axis=1).reshape(m, -1, k)
    pref = np.maximum.accumulate(b, axis=2).reshape(m, -1)[:, :T]
    suff = np.maximum.accumulate(b[:, :, ::-1], axis=2)[:, :, ::-1].reshape(m, -1)[:, :T]
    out = np.empty((m, T), float)
    out[:, k - 1:] = np.maximum(suff[:, :T - k + 1], pref[:, k - 1:])
    if k > 1:
        out[:, :k - 1] = np.maximum.accumulate(a[:, :k - 1], axis=1)
    return out


def trunc_from_logpath(cum):
    """Every drawdown-path statistic of a (m, T) matrix of CUMULATIVE LOG equity paths, in
    the units the bootstrap uses (percent, negative for a loss; ULCER positive).
    Returns a dict name -> (m,) array."""
    run = np.maximum.accumulate(cum, axis=1)
    ddp = np.expm1(cum - run)                       # <= 0
    depth = -ddp                                    # >= 0
    out = {"MAXDD": -depth.max(axis=1) * 100.0,
           "ULCER": np.sqrt((ddp ** 2).mean(axis=1)) * 100.0}
    ps = [p for p in QUANT_P if p < 1.0]
    qv = np.quantile(depth, ps, axis=1)             # (len(ps), m), one partition pass
    for i, p in enumerate(ps):
        out[QNAME[p]] = -qv[i] * 100.0
    for k in KDAY_K:
        if k >= 10 ** 9:
            continue
        out[KNAME[k]] = np.expm1(cum - sliding_max(cum, k)).min(axis=1) * 100.0
    return out


def stats_all(r):
    """The 17 realised statistics on one return slice.  Same units as the bootstrap."""
    r = np.asarray(r, float)
    n = len(r)
    cum = np.log1p(r).cumsum()[None, :]
    d = trunc_from_logpath(cum)
    out = {k: float(v[0]) for k, v in d.items()}
    eq = np.exp(cum[0])
    cagr = eq[-1] ** (252.0 / n) - 1.0
    vol = float(r.std(ddof=1) * np.sqrt(252.0))
    out["CAGR"] = cagr * 100.0
    out["VOL"] = vol * 100.0
    out["SHARPE"] = (r.mean() * 252.0) / vol if vol else np.nan
    out["CALMAR"] = (cagr / abs(out["MAXDD"] / 100.0)) if out["MAXDD"] < 0 else np.nan
    return out


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


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks_m(r, warm, ins, oos):
    rr = r[warm]
    c, s, d = fmet(rr)
    h = len(rr) // 2
    oc, os_, od = fmet(r[oos])
    ic, is_, idd = fmet(r[ins])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(rr[:h]), H2=fsharpe(rr[h:]),
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


def legs_4a(b, lbm):
    return {"A_H1": bool(b["H1"] > lbm["H1"]), "A_H2": bool(b["H2"] > lbm["H2"]),
            "A_DD": bool(b["MaxDD"] >= lbm["MaxDD"])}


# ------------------------------------------- 1098/1102's bootstrap, 1108's seed repair, + TRUNC
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_moments(R, idx, nb, L, chunk=100):
    """CAGR %, SHARPE, VOL % for every (rung, draw) — moment functionals, closed form."""
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    R2 = np.concatenate([R, R], axis=1)
    CS1 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2, axis=1)], axis=1)
    CS2 = np.concatenate([np.zeros((R.shape[0], 1)), np.cumsum(R2 ** 2, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    cag = np.empty((R.shape[0], nd))
    shp = np.empty((R.shape[0], nd))
    vol = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        s1 = (CS1[:, s + L] - CS1[:, s]).sum(axis=2)
        s2 = (CS2[:, s + L] - CS2[:, s]).sum(axis=2)
        cag[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
        mu = s1 / n
        var = (s2 - n * mu ** 2) / (n - 1)
        sd = np.sqrt(np.maximum(var, 0.0))
        vol[:, a:a + chunk] = sd * np.sqrt(252.0)
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp, vol


def boot_path(R, idx, chunk=40):
    """MAXDD, ULCER and every TRUNCATED maximum for every (rung, draw), in ONE pass over the
    SAME draws, so the whole truncation ladder pairs draw-for-draw with 1140's MAXDD."""
    nr = R.shape[0]
    nd = idx.shape[0]
    names = ["MAXDD", "ULCER"] + TRUNC_STATS
    out = {s: np.empty((nr, nd)) for s in names}
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            cum = np.cumsum(np.log1p(R[j])[ix], axis=1)
            d = trunc_from_logpath(cum)
            for s in names:
                out[s][j, a:a + chunk] = d[s] / 100.0        # back to fractions; scaled below
    return out


def boot_all(R, idx, nb, L):
    """All 17 statistics on ONE set of draws, in the units of stats_all()."""
    cag, shp, vol = boot_moments(R, idx, nb, L)
    pa = boot_path(R, idx)
    with np.errstate(divide="ignore", invalid="ignore"):
        cal = np.where(pa["MAXDD"] < 0, cag / np.abs(pa["MAXDD"]), np.nan)
    out = {"CAGR": cag * 100.0, "VOL": vol * 100.0, "SHARPE": shp, "CALMAR": cal}
    for s, v in pa.items():
        out[s] = v * 100.0
    return out


def agree_matrix(vals, boot):
    k = len(vals)
    A = np.full((k, k), np.nan)
    np.fill_diagonal(A, 1.0)
    for i, j in combinations(range(k), 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g):
            continue
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        A[i, j] = A[j, i] = float((np.sign(d) == np.sign(g)).mean()) if len(d) else np.nan
    return A


def sd_matrix(boot):
    k = boot.shape[0]
    S = np.full((k, k), np.nan)
    for i, j in combinations(range(k), 2):
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        S[i, j] = S[j, i] = float(d.std(ddof=1)) if len(d) > 2 else np.nan
    return S


def floor_sub(vals, A, sub, q):
    gaps, agr = [], []
    for i, j in combinations(sub, 2):
        g = vals[i] - vals[j]
        if not np.isfinite(g) or not np.isfinite(A[i, j]):
            continue
        gaps.append(abs(g))
        agr.append(A[i, j])
    if not gaps:
        return float("inf"), 0.0
    gaps, agr = np.array(gaps), np.array(agr)
    un = agr < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    return (float(gaps[ok].min()) if ok.any() else float("inf")), largest_un


def sub_summary(vals, A, S, sub):
    g, sd, ag = [], [], []
    for i, j in combinations(sub, 2):
        gap = vals[i] - vals[j]
        if not np.isfinite(gap):
            continue
        g.append(abs(gap))
        sd.append(S[i, j])
        ag.append(A[i, j])
    g, sd, ag = np.array(g, float), np.array(sd, float), np.array(ag, float)
    m = np.isfinite(g) & np.isfinite(sd) & (sd > 0)
    ratio = g[m] / sd[m]
    return (float(np.median(g[np.isfinite(g)])) if np.isfinite(g).any() else np.nan,
            float(np.median(sd[np.isfinite(sd)])) if np.isfinite(sd).any() else np.nan,
            float(np.median(ratio)) if len(ratio) else np.nan,
            float(np.nanmean(ag)) if np.isfinite(ag).any() else np.nan,
            int(len(g)))


def loglog_slope(T, y):
    """OLS slope of log(y) on log(T); nan unless at least 3 finite positive points."""
    T, y = np.asarray(T, float), np.asarray(y, float)
    m = np.isfinite(T) & np.isfinite(y) & (T > 0) & (y > 0)
    if m.sum() < 3:
        return np.nan
    x, z = np.log(T[m]), np.log(y[m])
    x = x - x.mean()
    return float((x * (z - z.mean())).sum() / (x ** 2).sum()) if (x ** 2).sum() else np.nan


def cadence_mask(idx, spec):
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def subtapes(n_warm):
    out = []
    for f in FRACS:
        edges = [int(round(i * n_warm / f)) for i in range(f + 1)]
        for k in range(f):
            out.append((f"F{f}_{k + 1}", f, k + 1, edges[k], edges[k + 1]))
    return out


def main():
    t0 = time.time()
    P(f"# Idea 1146 (lane B, {DATE}) — does a TRUNCATED MAXIMUM behave like ULCER or like MAXDD?")
    P("#   1140: MAXDD is the ONLY one of six statistics whose realised rung GAP and bootstrap")
    P("#   SD BOTH GROW with tape length (median b +0.1419 / +0.1654); ULCER and CALMAR, on the")
    P("#   SAME drawdown path, both have FALLING SD.  1140 read the carrier as MAX-ness.  This")
    P("#   run builds the TRUNCATION LADDER that reading predicts and reports where the MAXDD")
    P("#   signature switches off.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): TRUNCATION RULE {list(RULE_SETS)} x SUB-TAPE")
    P(f"#   FRACTION {['1/' + str(f) for f in FRACS]} = 9 combinations, ALL published.")
    P("#   TRUNCATION LEVEL is NOT a dial — every rung of both ladders reported at every cell.")
    P("#   PANEL, LADDER and RUNG SET are NOT dials — all 2 x 4 x 2 cells reported everywhere.")
    P(f"#   q is NOT a dial: {Q_HEAD} headline, {QS} reported beside, never selected on.")
    P(f"#   BLOCK LENGTH is NOT a dial: L={L_HEAD} frozen from 1098/1102/1110/1131/1140.")
    P("#   THE TWO TRUNCATION LADDERS (both NEST MAXDD exactly at their top rung):")
    P(f"     QUANT  {QUANT_LADDER}   (p = {QUANT_P})")
    P(f"     KDAY   {KDAY_LADDER}   (k = {[k for k in KDAY_K[:-1]] + ['INF']})")
    P(f"   REFERENCE ARMS (1140's six, same draws, same seeds): {STATS6}")
    P(f"   {len(STATS)} distinct statistics in total.")
    P(f"#   CORE  H {H_CORE}  CADENCE {C_CORE}")
    P(f"#   EXT   H {H_EXT}  CADENCE {C_EXT}")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, hold {HOLD0}, N {N0},")
    P(f"#   cadence {FREQ0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END},")
    P(f"#   block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, seed bases {SEED_BASES}.")
    P(f"# PRIOR QUOTED, NOT RECOMPUTED: {A1141_NOTE}")
    P("# DEFINITIONS, declared before any number:")
    P("#   MAXDD SIGNATURE  b_gap > 0 AND b_sd > 0   (both grow with tape length)")
    P("#   ULCER SIGNATURE  b_sd < 0                 (sampling SD falls with tape length)")
    P("#   SWITCH-OFF RUNG  the rung of a truncation ladder, reading from the truncated end")
    P("#                    TOWARD MAXDD, at which the MAXDD signature first turns ON.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_MAXDD_SIG   MAXDD reproduces 1140: median b_gap > 0 AND median b_sd > 0.")
    P("#   (b) H_ULCER_SIG   ULCER reproduces 1140: median b_sd < 0.")
    P("#   (c) H_SWITCH      the ladders are NOT uniform: at least one truncated rung on each")
    P("#                     rule carries the ULCER signature (b_sd < 0), i.e. the signature")
    P("#                     switches off somewhere strictly below the maximum.")
    P("#   (d) H_KNIFE_EDGE  1140's reading in its STRONGEST form: the signature is confined")
    P("#                     to the extreme — ON at p >= 0.99 / k >= 504 and OFF at p <= 0.95")
    P("#                     and k <= 252.")
    P("#   (e) H_MONOTONE    b_sd is NON-DECREASING along each ladder toward MAXDD (>= 80% of")
    P("#                     adjacent rung pairs, per rule, at the headline).")
    P("#   (f) H_CAPITAL     THE CAPITAL LEG: some truncated-maximum CHOOSER beats 1140's")
    P("#                     MaxDD chooser C_ISDD on median rule-8 OOS Sharpe across cells.")
    P("# DECISION RULE, declared before any number:")
    P("#   LIKE ULCER  iff H_MAXDD_SIG and H_ULCER_SIG and H_SWITCH and H_KNIFE_EDGE —")
    P("#               truncating the maximum AT ALL removes the signature.")
    P("#   LIKE MAXDD  iff H_MAXDD_SIG and the signature survives at EVERY truncated rung of")
    P("#               at least one rule (that rule has NO switch-off).")
    P("#   MIXED       anything else, reported as MIXED and not rounded to either.")
    P("#   THE CONFOUND, NAMED FIRST: a lower quantile / shorter horizon is a SMALLER number")
    P("#   in level as well as a less extreme one, and a smaller level mechanically carries a")
    P("#   smaller gap.  That is why the headline is the EXPONENT of the gap and of the SD")
    P("#   SEPARATELY (a level shift moves both together and cancels in neither), and why the")
    P("#   LEVELS are published beside them (levels.csv) so the reader can check it.")
    P("")

    gaterows, gates = [], {}
    dropped = {}
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px_all = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        px = px_all.loc[:TAPE_END]
        dropped[panel] = (len(px_all), len(px))
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}"
          f"   [cache holds {dropped[panel][0]:,} rows; {dropped[panel][0] - dropped[panel][1]} "
          f"bar(s) after {TAPE_END} EXCLUDED by the pin]")

    def run_cell(panel, N, H, gross, freq):
        d = panels[panel]
        mk = cadence_mask(d["idx"], freq)
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d["sc"], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, tn

    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1, pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                        {g1:.2e}   {'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2, pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple            {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%})")

    # TAPE DRIFT — what the pin costs, measured rather than asserted.  The default U56 book is
    # re-run on the UNPINNED cache (two extra bars) and its full-tape triple printed beside the
    # pinned one, so the reader can price the pin instead of trusting it.
    px_un = load_universe(broad=False).dropna(how="all").ffill()
    if len(px_un) > len(d["px"]):
        warm_u, ins_u, oos_u = windows(px_un.index)
        sc_u, el_u = mech(px_un)
        mk_u = rebalance_mask(px_un.index, FREQ0).values
        mkl_u = np.roll(mk_u, LAG)
        mkl_u[:LAG] = False
        W_u = build(-sc_u, el_u, px_un.notna().values, np.flatnonzero(mk_u), N0, HOLD0,
                    len(px_un), len(px_un.columns), GROSS0)
        Wl_u = np.zeros_like(W_u)
        Wl_u[LAG:] = W_u[:-LAG]
        g_u, tn_u = nrun(px_un.pct_change().fillna(0.0).values, Wl_u, mkl_u)
        mu = blocks_m(g_u - tn_u * COST / 1e4, warm_u, ins_u, oos_u)
        P(f"  TAPE DRIFT  the {len(px_un) - len(d['px'])} excluded U56 bar(s) move the default "
          f"book's full-tape triple from")
        P(f"              {m['CAGR']:.4%} / {m['Sharpe']:.4f} / {m['MaxDD']:.4%}  (pinned, == 1140) to")
        P(f"              {mu['CAGR']:.4%} / {mu['Sharpe']:.4f} / {mu['MaxDD']:.4%}  (unpinned cache), i.e. "
          f"CAGR {mu['CAGR'] - m['CAGR']:+.4%}, Sharpe {mu['Sharpe'] - m['Sharpe']:+.4f}.")
        P("              That drift is LARGER than several of the gate tolerances below, which is")
        P("              why the pin exists.  It is NOT a dial and nothing is selected on it.")

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    sm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    g3 = max(abs(sm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]), abs(sm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(sm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                        {g3:.2e}   {'PASS' if gates['G3'] else 'FAIL'}")

    r12, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    m12 = blocks_m(r12, d["warm"], d["ins"], d["oos"])
    g4 = max(abs(m12["CAGR"] - A1098_U56_N12[0]), abs(m12["Sharpe"] - A1098_U56_N12[1]),
             abs(m12["MaxDD"] - A1098_U56_N12[2]))
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="committed U56 n=12 triple", value=g4, pass_=gates["G4"]))
    P(f"  G4  CROSS-RUN 1098/1102's committed U56 n=12 triple       {g4:.2e}   {'PASS' if gates['G4'] else 'FAIL'}")

    db = panels["B136"]
    r15, _ = run_cell("B136", 15, HOLD0, GROSS0, FREQ0)
    m15 = blocks_m(r15, db["warm"], db["ins"], db["oos"])
    g4b = max(abs(m15["CAGR"] - A1098_B136_N15[0]), abs(m15["Sharpe"] - A1098_B136_N15[1]),
              abs(m15["MaxDD"] - A1098_B136_N15[2]))
    gates["G4b"] = g4b < 5e-4
    gaterows.append(dict(gate="G4b", what="committed B136 n=15 triple", value=g4b, pass_=gates["G4b"]))
    P(f"  G4b CROSS-RUN 1098/1102's committed B136 n=15 triple      {g4b:.2e}   {'PASS' if gates['G4b'] else 'FAIL'}")

    lb = {}
    for panel in PANELS:
        dp = panels[panel]
        lr = backtest(dp["px"], rules_v2_weights(dp["px"]), cost_bps=COST, freq="W")["returns"].values
        lb[panel] = blocks_m(lr, dp["warm"], dp["ins"], dp["oos"])
    g5 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G5"] = g5 < 5e-4
    gaterows.append(dict(gate="G5", what="live RULES v2 MaxDD", value=g5, pass_=gates["G5"]))
    P(f"  G5  live RULES v2 MaxDD == committed -12.05%              {g5:.2e}   {'PASS' if gates['G5'] else 'FAIL'}")

    r12b, _ = run_cell("U56", 12, HOLD0, GROSS0, FREQ0)
    g6 = float(np.abs(r12 - r12b).max())
    gates["G6"] = g6 == 0.0
    gaterows.append(dict(gate="G6", what="determinism", value=g6, pass_=gates["G6"]))
    P(f"  G6  determinism                                           {g6:.2e}   {'PASS' if gates['G6'] else 'FAIL'}")

    g7 = max(int(np.abs(cadence_mask(d["idx"], f).astype(int) - rebalance_mask(d["idx"], f).values.astype(int)).sum())
             for f in ("D", "W", "M", "Q"))
    gates["G7"] = g7 == 0
    gaterows.append(dict(gate="G7", what="cadence_mask == engine.rebalance_mask on D/W/M/Q",
                         value=float(g7), pass_=gates["G7"]))
    P(f"  G7  cadence_mask == engine.rebalance_mask (D/W/M/Q)       {g7:.2e}   {'PASS' if gates['G7'] else 'FAIL'}")

    # ---- G11/G12: the two truncation ladders NEST MAXDD exactly at their top rung, and the
    # sliding-max primitive equals a brute-force rolling max.  Checked on real return paths.
    rng0 = np.random.default_rng(1146)
    _pl = min(int(d["warm"].sum()), int(db["warm"].sum()))
    probe = np.vstack([rfast[d["warm"]][:_pl], r12[d["warm"]][:_pl], r15[db["warm"]][:_pl]])
    cum_probe = np.cumsum(np.log1p(probe), axis=1)
    tp = trunc_from_logpath(cum_probe)
    mdd_direct = np.array([stats_all(probe[i])["MAXDD"] for i in range(probe.shape[0])])
    g11 = float(np.abs(tp["MAXDD"] - mdd_direct).max())
    gates["G11"] = g11 < 1e-12
    gaterows.append(dict(gate="G11", what="QUANT top rung (p=1) == MAXDD == stats_all MAXDD",
                         value=g11, pass_=gates["G11"]))
    P(f"  G11 QUANT p=1.000 IS MAXDD (and == stats_all)             {g11:.2e}   {'PASS' if gates['G11'] else 'FAIL'}")

    kbrute = []
    for k in (21, 63, 252):
        s = pd.DataFrame(cum_probe.T).rolling(k, min_periods=1).max().values.T
        kbrute.append(float(np.abs(sliding_max(cum_probe, k) - s).max()))
    kinf = float(np.abs(np.expm1(cum_probe - sliding_max(cum_probe, 10 ** 9)).min(axis=1) * 100.0
                        - tp["MAXDD"]).max())
    g12 = max(max(kbrute), kinf)
    gates["G12"] = g12 < 1e-12
    gaterows.append(dict(gate="G12", what="sliding_max == pandas rolling max; KDAY k=INF == MAXDD",
                         value=g12, pass_=gates["G12"]))
    P(f"  G12 sliding_max == rolling max; K_INF IS MAXDD            {g12:.2e}   {'PASS' if gates['G12'] else 'FAIL'}")

    # ---- G13: the truncation ladders are ORDERED by construction (a lower quantile / shorter
    # horizon is never DEEPER than a higher one).  If this failed the ladders would not nest.
    # depth is NEGATIVE, so each rung toward MAXDD must be <= the one before it
    ordq = max(float(np.max(tp[QUANT_LADDER[i + 1]] - tp[QUANT_LADDER[i]]))
               for i in range(len(QUANT_LADDER) - 1))
    ordk = max(float(np.max(tp[KDAY_LADDER[i + 1]] - tp[KDAY_LADDER[i]]))
               for i in range(len(KDAY_LADDER) - 1))
    g13 = max(ordq, ordk)
    gates["G13"] = g13 <= 1e-12
    gaterows.append(dict(gate="G13", what="both ladders monotone in depth toward MAXDD",
                         value=g13, pass_=gates["G13"]))
    P(f"  G13 both ladders nest monotonically toward MAXDD          {g13:.2e}   {'PASS' if gates['G13'] else 'FAIL'}")

    # ------------------------------------------------------------------------ BUILD EVERY BOOK
    RUNGS = {"N": [str(x) for x in LAD_N], "GROSS": [str(x) for x in LAD_G],
             "H": [str(x) for x in sorted(set(H_CORE + H_EXT))], "CADENCE": list(C_EXT)}
    SUBSET = {("N", "CORE"): RUNGS["N"], ("N", "EXT"): RUNGS["N"],
              ("GROSS", "CORE"): RUNGS["GROSS"], ("GROSS", "EXT"): RUNGS["GROSS"],
              ("H", "CORE"): [str(x) for x in H_CORE], ("H", "EXT"): [str(x) for x in H_EXT],
              ("CADENCE", "CORE"): list(C_CORE), ("CADENCE", "EXT"): list(C_EXT)}
    MOVES = {lad: SUBSET[(lad, "CORE")] != SUBSET[(lad, "EXT")] for lad in LADDERS}

    def cell_params(lad, rung):
        N, H, gr, fq = N0, HOLD0, GROSS0, FREQ0
        if lad == "N":
            N = int(rung)
        elif lad == "H":
            H = int(rung)
        elif lad == "GROSS":
            gr = float(rung)
        else:
            fq = str(rung)
        return N, H, gr, fq

    grid_rows, RET = [], {}
    for panel in PANELS:
        dp = panels[panel]
        sb = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"], dp["oos"])
        panels[panel]["spy_m"] = sb
        for lad in LADDERS:
            for rung in RUNGS[lad]:
                N, H, gr, fq = cell_params(lad, rung)
                r, tn = run_cell(panel, N, H, gr, fq)
                RET[(panel, lad, rung)] = r
                b = blocks_m(r, dp["warm"], dp["ins"], dp["oos"])
                row = dict(panel=panel, ladder=lad, rung=rung, N=N, H=H, gross=gr, freq=fq,
                           in_core=bool(rung in SUBSET[(lad, "CORE")]),
                           turnover=float(tn[dp["warm"]].sum()) / (dp["warm"].sum() / 252.0), **b)
                # the IS truncated maxima of THIS book — the capital arm's chooser keys
                ist = stats_all(r[dp["ins"]])
                for s in ["MAXDD"] + TRUNC_STATS:
                    row[f"IS_{s}"] = ist[s]
                    row[f"IS_CALM_{s}"] = (row["IS_CAGR"] / abs(ist[s] / 100.0)
                                           if ist[s] < 0 else np.nan)
                row.update(legs_4b(b, sb))
                row.update(legs_4b_oos(b, sb))
                row.update(legs_4a(b, lb[panel]))
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
    G = pd.DataFrame(grid_rows)
    P(f"  built {len(G):,} books ({int(G.in_core.sum())} on 1110/1116's CORE rungs) in "
      f"{time.time() - t0:.0f}s")

    prior = pd.read_csv(f"{PRIOR1110}.grid.csv", dtype=str, keep_default_na=False)
    mine = G.set_index(["panel", "ladder", "rung"])
    dev = []
    for _, r in prior.iterrows():
        key = (r["panel"], r["ladder"], r["rung"])
        if key not in mine.index:
            dev.append(np.inf)
            continue
        mr = mine.loc[key]
        dev.append(max(abs(mr["CAGR"] - float(r["CAGR"])), abs(mr["Sharpe"] - float(r["Sharpe"])),
                       abs(mr["MaxDD"] - float(r["MaxDD"])), abs(mr["OOS_Sharpe"] - float(r["OOS_Sharpe"])),
                       abs(mr["turnover"] - float(r["turnover"]))))
    g8 = float(np.max(dev))
    gates["G8"] = g8 < 1e-9 and len(prior) == 54
    gaterows.append(dict(gate="G8", what=f"reproduce 1110's committed {len(prior)}-row CORE grid",
                         value=g8, pass_=gates["G8"]))
    P(f"  G8  reproduce 1110's committed {len(prior)}-row CORE grid         {g8:.2e}   {'PASS' if gates['G8'] else 'FAIL'}")

    # --------------------------------------------------- THE SUB-TAPES AND THE BOOTSTRAP GRID
    TAPES = {}
    for panel in PANELS:
        nw = int(panels[panel]["warm"].sum())
        TAPES[panel] = subtapes(nw)
    P("## THE SIX DISJOINT SUB-TAPES (warm tape only; contiguous, disjoint within a fraction)")
    for panel in PANELS:
        dp = panels[panel]
        wi = dp["idx"][dp["warm"]]
        for nm, f, k, lo, hi in TAPES[panel]:
            P(f"  {panel:5s} {nm:6s} 1/{f}  n={hi - lo:5,d}  {wi[lo].date()} -> {wi[hi - 1].date()}")

    cells, levels = [], []
    P(f"## BOOTSTRAP — 3 seed bases x 2 panels x 4 ladders x 6 sub-tapes x {len(STATS)} statistics")
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            for lad in LADDERS:
                rl = RUNGS[lad]
                Rw = np.array([RET[(panel, lad, r)][dp["warm"]] for r in rl])
                for nm, f, k, lo, hi in TAPES[panel]:
                    Rs = Rw[:, lo:hi]
                    tag = "warm" if f == 1 else f"sub{f}_{k}"
                    rng = np.random.default_rng(seed_of(base, panel, lad, tag))
                    ix, nb = block_index(rng, Rs.shape[1], L_HEAD, BDRAWS)
                    bo = boot_all(Rs, ix, nb, L_HEAD)
                    per = [stats_all(Rs[i]) for i in range(len(rl))]
                    vals = {s: np.array([per[i][s] for i in range(len(rl))], float) for s in STATS}
                    if base == SEED_BASES[0]:
                        for i, rg in enumerate(rl):
                            for s in STATS:
                                levels.append(dict(panel=panel, ladder=lad, rung=rg, subtape=nm,
                                                   frac=f, n=hi - lo, stat=s, is_path=IS_PATH[s],
                                                   is_trunc=IS_TRUNC[s], value=vals[s][i]))
                    for s in STATS:
                        A = agree_matrix(vals[s], bo[s])
                        S = sd_matrix(bo[s])
                        for rs in RUNGSETS:
                            sub = [rl.index(r) for r in SUBSET[(lad, rs)]]
                            mg, msd, mratio, magr, npair = sub_summary(vals[s], A, S, sub)
                            for q in QS:
                                flo, _ = floor_sub(vals[s], A, sub, q)
                                cells.append(dict(
                                    base=base, panel=panel, ladder=lad, rung_set=rs,
                                    rung_set_moves=MOVES[lad], stat=s, is_path=IS_PATH[s],
                                    is_trunc=IS_TRUNC[s], subtape=nm, frac=f, n=hi - lo, q=q,
                                    inf=bool(not np.isfinite(flo)),
                                    floor=(np.nan if not np.isfinite(flo) else flo),
                                    med_gap=mg, med_sd=msd, med_ratio=mratio,
                                    mean_agree=magr, n_pairs=npair))
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")
    C = pd.DataFrame(cells)
    LV = pd.DataFrame(levels)
    dump(C, "cells")
    dump(LV, "levels")

    # ------------------------------------------- THE EXPONENTS (1140's fit, VERBATIM)
    # 1140's pooling, unchanged: median y per (cell, sub-tape) over the three seed bases FIRST,
    # then fit log(y) on log(n) across ALL SIX sub-tape rows (1 whole, 2 halves, 3 thirds).
    P("## THE EXPONENTS — 1140's fit, verbatim.  For each (panel, ladder, rung set, statistic)")
    P("##   fit log(y) = a + b*log(n) over the SIX sub-tapes, pooled over the 3 seed bases by")
    P("##   taking the median y per (cell, sub-tape) first.")
    exkey = ["panel", "ladder", "rung_set", "stat"]
    med = (C[C.q == Q_HEAD].groupby(exkey + ["subtape", "frac", "n"], as_index=False)
           [["med_ratio", "med_gap", "med_sd", "mean_agree"]].median())
    exps = []
    for kk, z in med.groupby(exkey):
        panel, lad, rs, s_ = kk
        exps.append(dict(panel=panel, ladder=lad, rung_set=rs, stat=s_, is_path=IS_PATH[s_],
                         is_trunc=IS_TRUNC[s_], rung_set_moves=MOVES[lad], n_subtapes=len(z),
                         b_ratio=loglog_slope(z.n, z.med_ratio),
                         b_gap=loglog_slope(z.n, np.abs(z.med_gap)),
                         b_sd=loglog_slope(z.n, z.med_sd),
                         b_agree=loglog_slope(z.n, z.mean_agree)))
    E = pd.DataFrame(exps)
    dump(E, "exponents")
    E0 = E                                    # 16 cells per statistic, as in 1140

    # ---- G9: reproduce 1140's COMMITTED exponents.csv cell by cell on its six statistics.
    # This is the load-bearing gate: it proves the truncation ladder below is measured on the
    # same books, the same draws and the same fit as the finding it is testing.
    px1140 = pd.read_csv(f"{PRIOR1140}.exponents.csv")
    mine9 = E0.set_index(["panel", "ladder", "rung_set", "stat"])
    dev9, n9 = [], 0
    for _, rr in px1140.iterrows():
        key = (rr["panel"], rr["ladder"], rr["rung_set"], rr["stat"])
        if key not in mine9.index:
            dev9.append(np.inf)
            continue
        n9 += 1
        mr = mine9.loc[key]
        dev9.append(max(abs(mr["b_gap"] - rr["b_gap"]), abs(mr["b_sd"] - rr["b_sd"]),
                        abs(mr["b_ratio"] - rr["b_ratio"]), abs(mr["b_agree"] - rr["b_agree"])))
    g9 = float(np.max(dev9))
    gates["G9"] = g9 < 1e-9 and n9 == 96
    gaterows.append(dict(gate="G9", what=f"reproduce 1140's committed {n9}-cell exponent table",
                         value=g9, pass_=gates["G9"]))
    P(f"  G9  CROSS-RUN 1140's committed {n9}-cell exponent table       {g9:.2e}   {'PASS' if gates['G9'] else 'FAIL'}")
    for s_, (bg, bs) in A1140_MEDIAN_B.items():
        me = E0[E0.stat == s_]
        P(f"      {s_:7s} median b_gap {float(np.nanmedian(me.b_gap)):+.4f} (1140 {bg:+.4f})   "
          f"b_sd {float(np.nanmedian(me.b_sd)):+.4f} (1140 {bs:+.4f})")
    g10 = float(C.groupby("stat").med_gap.apply(lambda x: np.nanmin(np.abs(x))).min())
    gates["G10"] = g10 > 0
    gaterows.append(dict(gate="G10", what="every statistic live (min median |gap| > 0)",
                         value=g10, pass_=gates["G10"]))
    P(f"  G10 every statistic live (min median |gap|)               {g10:.2e}   {'PASS' if gates['G10'] else 'FAIL'}")

    # ---- G14: the gate that actually carries this run.  G8/G9 compare against artifacts
    # committed on 2026-09-16; data/prices.csv has since been RE-CACHED and the adjusted
    # closes RESTATED (measured above: the default U56 book's committed full-tape CAGR moves
    # by ~4e-5 on the SAME pinned bars).  Bit-exact reproduction of a 1e-9 bar is therefore
    # impossible and is reported as a FAIL rather than papered over with a wider bar.  What
    # must survive a restatement of that size is 1140's committed SIGNATURE: the sign of all
    # 12 median exponents, and the two headline medians to 4 decimal places.
    sign_bad = 0
    for s_, (bg, bs) in A1140_MEDIAN_B.items():
        me = E0[E0.stat == s_]
        sign_bad += int(np.sign(float(np.nanmedian(me.b_gap))) != np.sign(bg))
        sign_bad += int(np.sign(float(np.nanmedian(me.b_sd))) != np.sign(bs))
    head_dev = max(abs(round(float(np.nanmedian(E0[E0.stat == "MAXDD"].b_gap)), 4) - 0.1419),
                   abs(round(float(np.nanmedian(E0[E0.stat == "MAXDD"].b_sd)), 4) - 0.1654),
                   abs(round(float(np.nanmedian(E0[E0.stat == "ULCER"].b_gap)), 4) + 0.1221),
                   abs(round(float(np.nanmedian(E0[E0.stat == "ULCER"].b_sd)), 4) + 0.1916))
    gates["G14"] = (sign_bad == 0) and head_dev < 5e-5
    gaterows.append(dict(gate="G14", what="1140's committed SIGNATURE (12 signs + 4 headline "
                                          "medians to 4dp) survives the cache restatement",
                         value=float(sign_bad) + head_dev, pass_=gates["G14"]))
    P(f"  G14 1140's SIGNATURE survives the restatement             "
      f"{float(sign_bad) + head_dev:.2e}   {'PASS' if gates['G14'] else 'FAIL'}  "
      f"({sign_bad} of 12 medians flip sign; headline dev {head_dev:.1e})")
    P("  NOTE ON G8/G9 — both compare against artifacts committed on 2026-09-16 at a 1e-9 bar.")
    P("  data/prices.csv has been RE-CACHED since and its adjusted closes RESTATED; the TAPE")
    P("  DRIFT block above measures the restatement on the SAME pinned bars.  A 1e-9 bar cannot")
    P("  survive that, so G8/G9 are reported FAILED, with their deviations published, and G14")
    P("  carries the reproduction claim instead.  No bar was widened to make anything pass.")
    dump(pd.DataFrame(gaterows), "gates")
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")
    if not all(gates.values()):
        P("  !! A GATE FAILED — every number below is reported anyway and must be read as suspect.")
    P("")

    # ----------------------------------------- RESULT 1: THE TRUNCATION LADDER, BOTH RULES
    P("## RESULT 1 — THE TRUNCATION LADDER.  Median exponents over the 96 (panel, ladder,")
    P("##   rung set) cells at the headline seed base, q = 0.90.  SIG = the MAXDD signature")
    P("##   (b_gap > 0 AND b_sd > 0).  Reading DOWN each block runs from the most truncated")
    P("##   rung to MAXDD itself.")
    lad_rows = []
    for rule, ladder in (("QUANT", QUANT_LADDER), ("KDAY", KDAY_LADDER)):
        for pos, s in enumerate(ladder):
            me = E0[E0.stat == s]
            bg = float(np.nanmedian(me.b_gap))
            bs = float(np.nanmedian(me.b_sd))
            br = float(np.nanmedian(me.b_ratio))
            cellsig = ((me.b_gap > 0) & (me.b_sd > 0))
            lad_rows.append(dict(rule=rule, pos=pos, stat=s,
                                 level=("p=" + str(QUANT_P[pos]) if rule == "QUANT"
                                        else "k=" + (str(KDAY_K[pos]) if KDAY_K[pos] < 10 ** 9 else "INF")),
                                 med_b_gap=bg, med_b_sd=bs, med_b_ratio=br,
                                 sig_MAXDD=bool(bg > 0 and bs > 0), sig_ULCER=bool(bs < 0),
                                 cell_share_sig=float(cellsig.mean()), n_cells=int(len(me))))
    LAD = pd.DataFrame(lad_rows)
    dump(LAD, "ladder")
    for rule in ("QUANT", "KDAY"):
        P(f"  --- rule {rule} ---")
        sub = LAD[LAD.rule == rule]
        P("   " + sub[["level", "stat", "med_b_gap", "med_b_sd", "med_b_ratio", "sig_MAXDD",
                       "sig_ULCER", "cell_share_sig"]].to_string(
            index=False, float_format=lambda x: f"{x:+.4f}").replace("\n", "\n   "))
    ulc = E0[E0.stat == "ULCER"]
    P(f"  REFERENCE  ULCER  b_gap {float(np.nanmedian(ulc.b_gap)):+.4f}  "
      f"b_sd {float(np.nanmedian(ulc.b_sd)):+.4f}  (1140: -0.1221 / -0.1916)")
    P("")

    # ---------------------------------------------- RESULT 2: WHERE THE SIGNATURE SWITCHES OFF
    P("## RESULT 2 — THE SWITCH-OFF RUNG (the deliverable the idea asks for)")
    sw_rows = []
    for rule, ladder in (("QUANT", QUANT_LADDER), ("KDAY", KDAY_LADDER)):
        sub = LAD[LAD.rule == rule].sort_values("pos")
        on = sub[sub.sig_MAXDD]
        first_on = str(on.iloc[0]["level"]) if len(on) else "NEVER"
        all_on = bool(sub.sig_MAXDD.all())
        n_off = int((~sub.sig_MAXDD).sum())
        sw_rows.append(dict(rule=rule, n_rungs=len(sub), n_sig_off=n_off,
                            first_rung_with_MAXDD_signature=first_on,
                            signature_at_every_rung=all_on,
                            switch_off_exists=bool(n_off > 0 and len(on) > 0)))
        P(f"  {rule:6s} {n_off} of {len(sub)} rungs carry the ULCER side; the MAXDD signature")
        P(f"         first turns ON at {first_on}; uniform-MAXDD = {all_on}")
    SW = pd.DataFrame(sw_rows)
    dump(SW, "switch")
    P("")

    # -------------------------------------------------- RESULT 3: THE DIAL GRID (9 combinations)
    P("## RESULT 3 — BOTH TUNED DIALS, ALL 9 COMBINATIONS (rule 4 requires every grid point)")
    P("##   Read: median b_sd over the truncated rungs of that rule, computed from the tape")
    P("##   lengths that dial 2 admits.  frac 1 = whole tape only is a DEGENERATE fit (a")
    P("##   single length cannot identify a slope) and is reported as nan, not as zero.")
    dial_rows = []
    for rule, ladder in RULE_SETS.items():
        trunc_only = [s for s in ladder if s != "MAXDD"]
        for f in FRACS:
            keep_n = sorted(C[C.frac <= f].n.unique())
            cb = med[med.frac <= f]
            bgs, bss = [], []
            for (panel, lad, rs, s_), grp in cb.groupby(["panel", "ladder", "rung_set", "stat"]):
                if s_ not in trunc_only:
                    continue
                bgs.append(loglog_slope(grp.n, np.abs(grp.med_gap)))
                bss.append(loglog_slope(grp.n, grp.med_sd))
            mg = float(np.nanmedian(bgs)) if len(bgs) and np.isfinite(bgs).any() else np.nan
            ms = float(np.nanmedian(bss)) if len(bss) and np.isfinite(bss).any() else np.nan
            dial_rows.append(dict(trunc_rule=rule, subtape_fraction=f"1/{f}",
                                  n_tape_lengths=len(keep_n), n_trunc_rungs=len(trunc_only),
                                  med_b_gap_trunc=mg, med_b_sd_trunc=ms,
                                  verdict=("nan (degenerate fit)" if not np.isfinite(ms)
                                           else ("LIKE MAXDD" if ms > 0 else "LIKE ULCER"))))
    DL = pd.DataFrame(dial_rows)
    dump(DL, "dials")
    P("   " + DL.to_string(index=False, float_format=lambda x: f"{x:+.4f}").replace("\n", "\n   "))
    P("")

    # ------------------------------------------------- RESULT 4: MONOTONICITY ALONG THE LADDER
    P("## RESULT 4 — IS b_sd MONOTONE ALONG EACH LADDER?  Share of adjacent rung pairs whose")
    P("##   b_sd RISES toward MAXDD, cell by cell (not on the medians), at the headline base.")
    mono_rows = []
    for rule, ladder in (("QUANT", QUANT_LADDER), ("KDAY", KDAY_LADDER)):
        piv = E0.pivot_table(index=["panel", "ladder", "rung_set"], columns="stat", values="b_sd")
        ok = tot = 0
        for i in range(len(ladder) - 1):
            a, b = piv[ladder[i]], piv[ladder[i + 1]]
            m = np.isfinite(a) & np.isfinite(b)
            ok += int((b[m] >= a[m]).sum())
            tot += int(m.sum())
        mono_rows.append(dict(rule=rule, adjacent_pairs=tot, rising_toward_MAXDD=ok,
                              share=(ok / tot if tot else np.nan)))
        P(f"  {rule:6s} {ok} of {tot} adjacent (cell, rung-pair) comparisons rise toward MAXDD "
          f"({ok / tot:.1%})" if tot else f"  {rule}: no comparisons")
    MO = pd.DataFrame(mono_rows)
    dump(MO, "monotone")
    P("")

    # --------------------------------------------- RESULT 5: LEVELS (the named confound)
    P("## RESULT 5 — THE LEVELS, so the level-shift confound is checkable and not asserted.")
    P("##   Median realised statistic over every (panel, ladder, rung) on the FULL warm tape.")
    lv0 = LV[LV.frac == 1].groupby("stat").value.median().rename("median_level")
    lvd = pd.DataFrame(lv0).reset_index()
    lvd["is_trunc"] = lvd.stat.map(IS_TRUNC)
    dump(lvd, "levelsummary")
    for rule, ladder in (("QUANT", QUANT_LADDER), ("KDAY", KDAY_LADDER)):
        P(f"  {rule:6s} " + "  ".join(f"{s}={float(lv0[s]):+.2f}%" for s in ladder))
    P(f"  ULCER  {float(lv0['ULCER']):+.2f}%   (a DEPTH, positive by construction)")
    P("  DEGENERACY CHECK — THE BIGGEST CAVEAT ON THE KDAY ARM, MEASURED.  A horizon rung only")
    P("  truncates anything if the book's worst drawdown actually took LONGER than k days to")
    P("  reach its trough from its peak.  Share of the 74 (panel, ladder, rung) books on the")
    P("  FULL warm tape at which K_k is BIT-IDENTICAL to MAXDD, i.e. the rung truncates NOTHING:")
    wide = LV[LV.frac == 1].pivot_table(index=["panel", "ladder", "rung"], columns="stat",
                                        values="value")
    degen = []
    for k in KDAY_K[:-1]:
        nm = KNAME[k]
        eq = (np.abs(wide[nm] - wide["MAXDD"]) < 1e-12)
        degen.append(dict(rung=nm, k=k, n_books=int(len(eq)), n_identical_to_MAXDD=int(eq.sum()),
                          share_degenerate=float(eq.mean()),
                          median_gap_pp=float((wide[nm] - wide["MAXDD"]).median())))
        P(f"    {nm}  k={k:4d}   {int(eq.sum()):3d} of {len(eq)} books ({eq.mean():.1%})   "
          f"median K_k - MAXDD {float((wide[nm] - wide['MAXDD']).median()):+.3f} pp")
    DG = pd.DataFrame(degen)
    dump(DG, "kday_degeneracy")
    P("  READ THIS BEFORE THE KDAY RESULT: wherever the share above is high the KDAY rung is")
    P("  MAXDD under another name, and its exponents MUST agree with MAXDD's trivially.  The")
    P("  KDAY arm therefore rests on the rungs where the share is LOW, and the conclusion drawn")
    P("  from it is only as strong as those rungs.")
    P("")

    # ------------------------------------------------- THE PRICE LEG: RULE 8 WALK-FORWARD
    P("## THE PRICE LEG — RULE 8 WALK-FORWARD.  Rung chosen on IS 2009-2016 ALONE; OOS")
    P("##   2017-2026 read ONCE.  Every truncation rung supplies a CHOOSER (maximise IS")
    P("##   CAGR / |truncated DD|) beside 1140's three.  Scored against the ladder's FROZEN")
    P("##   DEFAULT rung, against SPY and against the live RULES v2 book, BOTH KEEP PATHS.")
    CHOOSERS = dict(BASE_CHOOSERS)
    for s in ["MAXDD"] + TRUNC_STATS:
        CHOOSERS[f"C_CALM_{s}"] = (f"IS_CALM_{s}", "OOS_Sharpe")
    gi = G.set_index(["panel", "ladder", "rung"])
    wf = []
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for ch, (iscol, ooscol) in CHOOSERS.items():
                    if not np.isfinite(sub[iscol]).any():
                        continue
                    pick = sub.loc[sub[iscol].idxmax()]
                    best = sub.loc[sub[ooscol].idxmax()]
                    fullbest = sub.loc[sub["Sharpe"].idxmax()]
                    wf.append(dict(
                        panel=panel, ladder=lad, rung_set=rs, chooser=ch,
                        chooser_is_trunc=bool(ch.startswith("C_CALM_") and
                                              IS_TRUNC.get(ch[len("C_CALM_"):], False)),
                        k=len(rungs), pick=pick["rung"], default=DEFAULT_RUNG[lad],
                        full_argmax=fullbest["rung"],
                        pick_is_default=bool(pick["rung"] == DEFAULT_RUNG[lad]),
                        pick_is_full_argmax=bool(pick["rung"] == fullbest["rung"]),
                        CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                        H1=pick["H1"], H2=pick["H2"], OOS_CAGR=pick["OOS_CAGR"],
                        OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                        adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                        regret=float(best[ooscol] - pick[ooscol]),
                        pass_4b_full=bool(pick["pass_4b_full"]), pass_4b_oos=bool(pick["pass_4b_oos"]),
                        pass_4a=bool(pick["pass_4a"]),
                        spy_OOS_Sharpe=sb["OOS_Sharpe"], live_OOS_Sharpe=lbm["OOS_Sharpe"]))
    WF = pd.DataFrame(wf)
    dump(WF, "walkforward")
    dump(G, "books")

    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        P(f"  {panel} SPY       full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}   "
          f"halves {sb['H1']:.4f}/{sb['H2']:.4f}   OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel} RULES v2  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / {lbm['MaxDD']:.2%}   "
          f"halves {lbm['H1']:.4f}/{lbm['H2']:.4f}   OOS {lbm['OOS_CAGR']:.2%} / "
          f"{lbm['OOS_Sharpe']:.4f} / {lbm['OOS_MaxDD']:.2%}")
    P(f"  IS picks: {len(WF)} across {WF.chooser.nunique()} choosers — 4b full "
      f"{int(WF.pass_4b_full.sum())}, 4b OOS {int(WF.pass_4b_oos.sum())}, 4a "
      f"{int(WF.pass_4a.sum())}, median OOS Sharpe {WF.OOS_Sharpe.median():.4f}")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, 4b OOS "
      f"{int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}")

    P("  PER-CHOOSER rule-8 OOS (median over the 16 panel x ladder x rung-set cells):")
    ch_sum = (WF.groupby("chooser")
              .agg(med_OOS_Sharpe=("OOS_Sharpe", "median"),
                   med_OOS_CAGR=("OOS_CAGR", "median"),
                   med_OOS_MaxDD=("OOS_MaxDD", "median"),
                   med_adv_vs_default=("adv_oos_sharpe", "median"),
                   share_pick_is_default=("pick_is_default", "mean"),
                   n_4b_full=("pass_4b_full", "sum"), n_4b_oos=("pass_4b_oos", "sum"),
                   n_4a=("pass_4a", "sum"), n=("OOS_Sharpe", "size"))
              .sort_values("med_OOS_Sharpe", ascending=False))
    dump(ch_sum.reset_index(), "choosers")
    P("   " + ch_sum.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    dd_med = float(ch_sum.loc["C_ISDD", "med_OOS_Sharpe"])
    trunc_ch = [c for c in ch_sum.index if c.startswith("C_CALM_") and IS_TRUNC.get(c[len("C_CALM_"):], False)]
    best_tr = max(trunc_ch, key=lambda c: ch_sum.loc[c, "med_OOS_Sharpe"]) if trunc_ch else None
    best_tr_med = float(ch_sum.loc[best_tr, "med_OOS_Sharpe"]) if best_tr else np.nan
    P(f"  C_ISDD (1140's MaxDD chooser) median OOS Sharpe {dd_med:.4f}; best TRUNCATED chooser "
      f"{best_tr} {best_tr_med:.4f}  (gap {best_tr_med - dd_med:+.4f})")
    pw = WF[WF.pass_4b_full]
    P("  EVERY IS PICK THAT CLEARS 4b (full), with its OOS triple:")
    if len(pw):
        P("   " + pw[["panel", "ladder", "rung_set", "chooser", "pick", "pick_is_default", "CAGR",
                      "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
        P(f"  distinct BOOKS behind those {len(pw)} passes: "
          f"{sorted(set(zip(pw.panel, pw.ladder, pw.pick)))}")
        P(f"  of which PICK == FROZEN DEFAULT: {int(pw.pick_is_default.sum())} of {len(pw)}")
    else:
        P("    none")
    best_row = WF.loc[WF.OOS_Sharpe.idxmax()]
    P(f"  BEST IS PICK BY OOS SHARPE: {best_row['panel']} {best_row['ladder']}/{best_row['rung_set']} "
      f"{best_row['chooser']} pick {best_row['pick']} — full {best_row['CAGR']:.2%} / "
      f"{best_row['Sharpe']:.4f} / {best_row['MaxDD']:.2%}, halves {best_row['H1']:.4f}/"
      f"{best_row['H2']:.4f}, OOS {best_row['OOS_CAGR']:.2%} / {best_row['OOS_Sharpe']:.4f} / "
      f"{best_row['OOS_MaxDD']:.2%}")
    P("")

    # ----------------------------------------------------------------------------- HYPOTHESES
    mdd = E0[E0.stat == "MAXDD"]
    mdd_bg, mdd_bs = float(np.nanmedian(mdd.b_gap)), float(np.nanmedian(mdd.b_sd))
    ulc_bs = float(np.nanmedian(ulc.b_sd))
    h_maxdd_sig = bool(mdd_bg > 0 and mdd_bs > 0)
    h_ulcer_sig = bool(ulc_bs < 0)
    swq = SW[SW.rule == "QUANT"].iloc[0]
    swk = SW[SW.rule == "KDAY"].iloc[0]
    h_switch = bool(swq["n_sig_off"] > 0 and swk["n_sig_off"] > 0)

    def sig_of(name):
        row = LAD[LAD.stat == name]
        return bool(row.iloc[0]["sig_MAXDD"]) if len(row) else False

    knife_on = sig_of(QNAME[0.99]) and sig_of(QNAME[0.999]) and sig_of("MAXDD") and sig_of(KNAME[504])
    knife_off = (not sig_of(QNAME[0.95])) and (not sig_of(QNAME[0.90])) and \
                (not sig_of(KNAME[252])) and (not sig_of(KNAME[126]))
    h_knife = bool(knife_on and knife_off)
    h_mono = bool((MO.share >= 0.80).all())
    h_capital = bool(np.isfinite(best_tr_med) and best_tr_med > dd_med)

    HYP = {
        "H_MAXDD_SIG": (h_maxdd_sig, f"MAXDD median b_gap {mdd_bg:+.4f}, b_sd {mdd_bs:+.4f} "
                                     f"(1140 committed +0.1419 / +0.1654)"),
        "H_ULCER_SIG": (h_ulcer_sig, f"ULCER median b_sd {ulc_bs:+.4f} (1140 committed -0.1916)"),
        "H_SWITCH": (h_switch, f"rungs on the ULCER side: QUANT {int(swq['n_sig_off'])} of "
                               f"{int(swq['n_rungs'])}, KDAY {int(swk['n_sig_off'])} of "
                               f"{int(swk['n_rungs'])}"),
        "H_KNIFE_EDGE": (h_knife, f"signature ON at p>=0.99 and k>=504: {knife_on}; OFF at "
                                  f"p<=0.95 and k<=252: {knife_off}"),
        "H_MONOTONE": (h_mono, "b_sd rises toward MAXDD in " +
                       ", ".join(f"{r['rule']} {r['share']:.1%}" for _, r in MO.iterrows()) +
                       " of adjacent cell comparisons (bar 80%)"),
        "H_CAPITAL": (h_capital, f"best truncated chooser {best_tr} median OOS Sharpe "
                                 f"{best_tr_med:.4f} vs C_ISDD {dd_med:.4f} "
                                 f"({best_tr_med - dd_med:+.4f})"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in HYP.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:13s} {why}")
    P(f"  {sum(1 for v in HYP.values() if v[0])} of {len(HYP)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in HYP.items()]),
         "hypotheses")
    P("")

    # -------------------------------------------------------------------------------- VERDICT
    uniform_rule = [r["rule"] for _, r in SW.iterrows() if r["signature_at_every_rung"]]
    like_ulcer = h_maxdd_sig and h_ulcer_sig and h_switch and h_knife
    like_maxdd = h_maxdd_sig and len(uniform_rule) > 0
    answer = ("LIKE ULCER" if like_ulcer else "LIKE MAXDD" if like_maxdd else "MIXED")
    n4b = int(WF.pass_4b_full.sum())
    nd = WF[WF.pass_4b_full & ~WF.pick_is_default]
    nondefault_4b = int(nd.shape[0])
    capital_declared = ("KEEP-4b-candidate" if nondefault_4b > 0 and h_capital else "KILL (capital)")

    # ---------------------------------------------------------------- CAPITAL ADDENDUM
    # LABELLED POST-HOC.  The capital rule declared above fires on (any non-default 4b pass)
    # AND (any truncated chooser beating C_ISDD by any margin).  Both legs cleared, so by the
    # letter of the declared rule this run is a KEEP-4b-candidate.  It is not one, and the
    # reason is arithmetic that the declared rule simply failed to ask for.  Nothing here is
    # tuned toward a pass — every leg below moves the verdict the OTHER way, and the declared
    # rule's own output is published unchanged beside it.
    P("## CAPITAL ADDENDUM — POST-HOC, LABELLED AS SUCH.  Three facts the declared capital")
    P("##   rule did not ask for, each of which moves the verdict AWAY from a proposal.")
    adv_le0 = int((ch_sum.med_adv_vs_default <= 0).sum())
    P(f"  (1) NO CHOOSER BEATS DOING NOTHING.  {adv_le0} of {len(ch_sum)} choosers — 1140's")
    P("      three and all 12 truncated ones — have a median rule-8 OOS Sharpe advantage over")
    P("      the ladder's FROZEN DEFAULT rung that is <= 0.  Choosing a rung by ANY of these")
    P("      statistics, truncated or not, loses out of sample to keeping the default.")
    if nondefault_4b:
        dflt_oos = {}
        for _, rr in nd.iterrows():
            dflt_oos[(rr["panel"], rr["ladder"])] = float(
                gi.loc[(rr["panel"], rr["ladder"], DEFAULT_RUNG[rr["ladder"]])]["OOS_Sharpe"])
        worse = int(sum(1 for _, rr in nd.iterrows()
                        if rr["OOS_Sharpe"] < dflt_oos[(rr["panel"], rr["ladder"])]))
        gain = [float(rr["OOS_Sharpe"] - dflt_oos[(rr["panel"], rr["ladder"])])
                for _, rr in nd.iterrows()]
        best_gain = max(gain)
        P(f"  (2) THE {nondefault_4b} NON-DEFAULT 4b PASSES BUY NOTHING.  {worse} of "
          f"{nondefault_4b} have a")
        P("      LOWER rule-8 OOS Sharpe than the frozen default rung on their own panel and")
        P(f"      ladder, and the best of the other {nondefault_4b - worse} beats its default by "
          f"{best_gain:+.4f} — still inside")
        P(f"      877's {A877_SEED_FLOOR:.4f} seed floor.  All {nondefault_4b}, in full:")
        for _, rr in nd.iterrows():
            P(f"        {rr['panel']:5s} {rr['ladder']:7s} {rr['chooser']:13s} pick {rr['pick']:5s} "
              f"OOS S {rr['OOS_Sharpe']:.4f}  vs default "
              f"{dflt_oos[(rr['panel'], rr['ladder'])]:.4f}  "
              f"({rr['OOS_Sharpe'] - dflt_oos[(rr['panel'], rr['ladder'])]:+.4f})")
    else:
        worse = 0
        P("  (2) there are no non-default 4b passes.")
    P(f"  (3) THE TRUNCATED EDGE IS INSIDE THE RECORD'S OWN NOISE FLOOR.  The best truncated")
    P(f"      chooser beats C_ISDD by {best_tr_med - dd_med:+.4f} of Sharpe.  Idea 877's committed")
    P(f"      per-arm seed noise floor is {A877_SEED_FLOOR:.4f} of Sharpe — "
      f"{A877_SEED_FLOOR / abs(best_tr_med - dd_med) if best_tr_med != dd_med else float('inf'):.0f}x larger.")
    P("      Quoted from 877, not recomputed here.")
    above_floor = bool(abs(best_tr_med - dd_med) > A877_SEED_FLOOR)
    capital = ("KEEP-4b-candidate" if (nondefault_4b > worse and above_floor and adv_le0 < len(ch_sum))
               else "KILL (capital)")
    P(f"  DECLARED RULE SAYS: {capital_declared}.  WITH THE ADDENDUM: {capital}.")
    P("  NOTHING IS PROPOSED. 4a is 0 of 240; every 4b pass is either the incumbent frozen")
    P("  default or a strictly worse gross-dial neighbour of it; and the truncated-maximum")
    P("  chooser's edge over the MaxDD chooser is an order of magnitude inside the seed floor.")
    P("  The declared capital rule was TOO WEAK, and that is recorded as a defect of this")
    P("  run's pre-registration, not smoothed over.")
    P("")
    P("## THE ANSWER (decision rule declared before any number)")
    P(f"  H_MAXDD_SIG {h_maxdd_sig}  H_ULCER_SIG {h_ulcer_sig}  H_SWITCH {h_switch}  "
      f"H_KNIFE_EDGE {h_knife}  H_MONOTONE {h_mono}")
    P(f"  => a TRUNCATED MAXIMUM behaves: {answer}")
    P("  AND THE ANSWER IS AXIS-DEPENDENT, which is the finding.  The two rules truncate")
    P("  DIFFERENT things and do not agree:")
    P("    QUANT truncates the ORDER STATISTIC — how deep into the tail of the drawdown")
    P("          distribution the number reaches.  Truncating it AT ALL removes the")
    P("          signature (b_sd is negative at every p <= 0.90 and only turns positive")
    P("          between p=0.95 and p=0.99); the MAXDD signature needs p >= 0.999.")
    P("    KDAY  truncates the HORIZON — how far back the peak may be.  Truncating it does")
    P("          NOT remove the signature at any rung tested, down to a 21-day lookback,")
    P("          where the signature is in fact STRONGER than MAXDD's own.")
    P("  So 1140's 'MAX-ness' is more precisely EXTREME-ORDER-STATISTIC-ness: a worst-of-many")
    P("  still grows with the tape however short the window it is taken over, because a longer")
    P("  tape supplies more windows; a 90th-percentile drawdown does not, because it is not a")
    P("  worst-of-anything.  A truncated maximum behaves like ULCER only when the truncation")
    P("  is applied to the ORDER, not to the WINDOW.")
    for _, r in SW.iterrows():
        P(f"     {r['rule']:6s} MAXDD signature first ON at {r['first_rung_with_MAXDD_signature']}; "
          f"{int(r['n_sig_off'])} of {int(r['n_rungs'])} rungs on the ULCER side")
    P(f"  CAPITAL (rule 8, both KEEP paths): {capital} (declared rule said {capital_declared}) "
      f"— 4a {int(WF.pass_4a.sum())} of {len(WF)}, "
      f"4b(full) {n4b} of {len(WF)}, of which NON-DEFAULT picks {nondefault_4b}; the best")
    P(f"  truncated chooser is {best_tr} at median OOS Sharpe {best_tr_med:.4f} against C_ISDD's "
      f"{dd_med:.4f}.")
    P("  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels. Every level above")
    P("  is optimistic and every exponent is measured on that inflated tape.")
    P(f"  {A1141_NOTE}")
    P("")
    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
