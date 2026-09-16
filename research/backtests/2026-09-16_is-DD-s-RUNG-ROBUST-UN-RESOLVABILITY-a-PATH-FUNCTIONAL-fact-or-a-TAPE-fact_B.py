#!/usr/bin/env python3
"""Idea 1140 (lane B, 2026-09-16)
   is-DD-s-RUNG-ROBUST-UN-RESOLVABILITY-a-PATH-FUNCTIONAL-fact-or-a-TAPE-fact

1131 found DD is the ONLY statistic un-resolvable at every rung set on every block (4 of 4
ROBUST on the two ladders whose rung set moves, and silenced by NONE of the 31 supersets of
CORE inside EXT), while S_FULL, S_OOS and CAGR all escape somewhere.  1110 had already noted
DD's floor runs the OTHER way in the tape-length fit (+0.2093 against -0.4540).  1141 (cloud,
same day) then CORRECTED 1131's wording: DD's "un-resolvable everywhere" is a LARGE-PANEL
fact — it fires less on SMALL — which is already evidence the reading is not a pure property
of the functional.

Two readings are on the table and this run separates them:

  PATH  — MaxDD is a PATH FUNCTIONAL.  Its own level grows with the length of the tape it is
          measured on, so both the GAP between two rungs and the bootstrap DISPERSION of that
          gap grow together and the ratio between them never improves.  If that is the
          carrier, EVERY path functional must behave the same way and every moment functional
          must not.
  TAPE  — the un-resolvability is a property of THIS tape (one 2008-2026 record with two
          crashes in it) and would not survive being measured on a different stretch of it.

THE DESIGN.  Six statistics in THREE MATCHED PAIRS, where the only thing that differs inside
a pair is whether the statistic reads the PATH or only the MOMENTS of the same return stream:

      role          NON-PATH (moments)        PATH (order-dependent)
      level         CAGR                      MAXDD
      dispersion    VOL                       ULCER
      ratio         SHARPE                    CALMAR

and SIX DISJOINT SUB-TAPES of the warm record (1 whole, 2 halves, 3 thirds), so the same 16
(panel, ladder, statistic) blocks 1131 published are re-run at three tape lengths.

THE DECISIVE TEST is not the firing count — shortening a tape makes EVERYTHING noisier and
therefore more un-resolvable, which is a confound running in the PATH reading's favour.  It
is the RESOLUTION EXPONENT.  For a moment functional the pairwise gap is level-stable in T
while its sampling SD falls as T^-0.5, so the resolution ratio |gap| / SD(gap) must grow as
T^+0.5.  For a path functional whose own level grows with T, the gap grows too and the ratio
must stay FLAT.  Fitting log(median ratio) on log(T) over the three tape lengths gives an
exponent per block whose predicted value is +0.5 for the non-path arm and 0 for the path arm,
and the GAP and SD exponents are published separately so the mechanism is checkable, not
inferred.

TUNED DIALS (2, PROTOCOL rule 4): `STAT SET` {S_NONPATH, S_PATH, S_ALL} x `SUB-TAPE FRACTION`
{1, 1/2, 1/3} = 9 combinations, ALL published.  PANEL (U56, B136), LADDER (N, H, GROSS,
CADENCE) and RUNG SET (CORE, EXT) are NOT dials — every one of the 2 x 4 x 2 x 6 = 96 cells is
reported everywhere.  CONFIDENCE q is NOT a dial: 0.90 is the headline, 0.80 and 0.95 are
reported beside it at every point and nothing is selected on them.  BLOCK LENGTH is NOT a
dial: L=63 is the headline, frozen from 1098/1102/1110/1131.

FROZEN at 1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131's construction: CAND20 legs,
cap INF, max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
2016-12-31, block L=63, 1000 draws, crc32 seeds, 3 seed bases, identical rung lists.

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

DATE = "2026-09-16"
SLUG = "is-DD-s-RUNG-ROBUST-UN-RESOLVABILITY-a-PATH-FUNCTIONAL-fact-or-a-TAPE-fact"
BT = Path(__file__).resolve().parent
OUT = BT / f"{DATE}_{SLUG}_B"
PRIOR1131 = BT / "2026-09-16_does-ANY-committed-FLOOR-KEYED-CLAUSE-survive-a-RUNG-SET-CHANGE_B"
PRIOR1110 = BT / "2026-09-16_what-does-the-RECORD-LOSE-if-the-FLOOR-CLAUSE-is-ENACTED-AS-WRITTEN_C"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
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

# ------------------------------------------------------- THE SIX STATISTICS, IN MATCHED PAIRS
NONPATH = ["CAGR", "VOL", "SHARPE"]
PATH = ["MAXDD", "ULCER", "CALMAR"]
STATS6 = NONPATH + PATH
PAIRS = [("level", "CAGR", "MAXDD"), ("dispersion", "VOL", "ULCER"), ("ratio", "SHARPE", "CALMAR")]
IS_PATH = {s: (s in PATH) for s in STATS6}
STAT_SETS = {"S_NONPATH": NONPATH, "S_PATH": PATH, "S_ALL": STATS6}    # dial 1
FRACS = [1, 2, 3]                                                      # dial 2 (1/1, 1/2, 1/3)

QS = [0.80, 0.90, 0.95]
Q_HEAD, L_HEAD, BDRAWS = 0.90, 63, 1000
SEED_BASES = [11311131, 11171117, 11161116]        # 1131's, so the full-tape cells reproduce

CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", "OOS_Sharpe", +1.0),
            "C_ISCAGR": ("IS_CAGR", "OOS_CAGR", +1.0),
            "C_ISDD": ("IS_MaxDD", "OOS_MaxDD", +1.0)}

A936_WH126 = (0.155787, 1.139701, -0.191276)
A1098_U56_N12 = (0.1771, 1.1692, -0.2017)
A1098_B136_N15 = (0.1678, 1.0682, -0.1966)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
# 1141 (cloud, committed 2026-09-16) — DD's matched-k firing share on the SMALL panel, quoted
# not recomputed (this run rebuilds U56 and B136 only; SMALL is 1141's leg).
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


# --------------------------------------- 1082/1098/1102/1108/1117/1131's fast runner, verbatim
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


def stats6(r):
    """The six realised statistics on one return slice, in the units the bootstrap uses:
    CAGR %, VOL %, SHARPE, MAXDD % (negative), ULCER % (positive), CALMAR (CAGR/|MaxDD|)."""
    r = np.asarray(r, float)
    n = len(r)
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / n) - 1.0
    ddp = eq / np.maximum.accumulate(eq) - 1.0
    mdd = float(ddp.min())
    ulcer = float(np.sqrt((ddp ** 2).mean()))
    vol = float(r.std(ddof=1) * np.sqrt(252.0))
    shp = (r.mean() * 252.0) / vol if vol else np.nan
    calmar = cagr / abs(mdd) if mdd < 0 else np.nan
    return {"CAGR": cagr * 100.0, "VOL": vol * 100.0, "SHARPE": shp,
            "MAXDD": mdd * 100.0, "ULCER": ulcer * 100.0, "CALMAR": calmar}


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


# ------------------------------------------- 1098/1102's bootstrap, 1108's seed repair, + PATH
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
    """MAXDD and ULCER for every (rung, draw) — 1131's boot_maxdd, extended to the second
    path functional in the SAME pass over the SAME draws, so CALMAR pairs draw-for-draw."""
    nr, _ = R.shape
    nd = idx.shape[0]
    dd = np.empty((nr, nd))
    ulc = np.empty((nr, nd))
    for a in range(0, nd, chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            ddp = np.expm1(cum - run)
            dd[j, a:a + chunk] = ddp.min(axis=1)
            ulc[j, a:a + chunk] = np.sqrt((ddp ** 2).mean(axis=1))
    return dd, ulc


def boot_six(R, idx, nb, L):
    """All six statistics on ONE set of draws, in the units of stats6()."""
    cag, shp, vol = boot_moments(R, idx, nb, L)
    dd, ulc = boot_path(R, idx)
    with np.errstate(divide="ignore", invalid="ignore"):
        cal = np.where(dd < 0, cag / np.abs(dd), np.nan)
    return {"CAGR": cag * 100.0, "VOL": vol * 100.0, "SHARPE": shp,
            "MAXDD": dd * 100.0, "ULCER": ulc * 100.0, "CALMAR": cal}


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
    """SD of the bootstrap GAP for every rung pair — the denominator of the resolution ratio."""
    k = boot.shape[0]
    S = np.full((k, k), np.nan)
    for i, j in combinations(range(k), 2):
        d = boot[i] - boot[j]
        d = d[np.isfinite(d)]
        S[i, j] = S[j, i] = float(d.std(ddof=1)) if len(d) > 2 else np.nan
    return S


def floor_sub(vals, A, sub, q):
    """1098's floor restricted to rung subset `sub`: the smallest gap above which EVERY pair
    is resolved at q; INFINITE when the LARGEST gap in the subset is itself un-resolved."""
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
    """median |gap|, median SD(gap), median resolution ratio and mean agreement over the
    rung pairs inside subset `sub`."""
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
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G7); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def subtapes(n_warm):
    """The SIX disjoint sub-tapes: 1 whole, 2 halves, 3 thirds, as (name, frac, k, lo, hi)
    index ranges into the WARM return vector.  Contiguous, disjoint within a fraction, and
    exhaustive of the warm tape at every fraction."""
    out = []
    for f in FRACS:
        edges = [int(round(i * n_warm / f)) for i in range(f + 1)]
        for k in range(f):
            out.append((f"F{f}_{k + 1}", f, k + 1, edges[k], edges[k + 1]))
    return out


def main():
    t0 = time.time()
    P(f"# Idea 1140 (lane B, {DATE}) — is DD's RUNG-ROBUST UN-RESOLVABILITY a PATH-FUNCTIONAL")
    P("#   fact or a TAPE fact?  1131's 16 blocks re-run with THREE MATCHED PAIRS of")
    P("#   statistics (moment vs path) over SIX DISJOINT SUB-TAPES.")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): STAT SET {list(STAT_SETS)} x SUB-TAPE FRACTION")
    P(f"#   {['1/' + str(f) for f in FRACS]} = 9 combinations, ALL published.")
    P("#   PANEL, LADDER and RUNG SET are NOT dials — all 2 x 4 x 2 cells reported everywhere.")
    P(f"#   q is NOT a dial: {Q_HEAD} headline, {QS} reported beside, never selected on.")
    P(f"#   BLOCK LENGTH is NOT a dial: L={L_HEAD} frozen from 1098/1102/1110/1131.")
    P("#   THE MATCHED PAIRS (the only thing that differs inside a pair is PATH-vs-MOMENT):")
    for role, np_, p_ in PAIRS:
        P(f"     {role:11s}  NON-PATH {np_:7s}  PATH {p_}")
    P(f"#   CORE  H {H_CORE}  CADENCE {C_CORE}")
    P(f"#   EXT   H {H_EXT}  CADENCE {C_EXT}")
    P(f"#   N {LAD_N} and GROSS {LAD_G} are IDENTICAL at both levels (1134's finding), so only")
    P("#   H and CADENCE are 'movers'; N and GROSS are reported and excluded from mover counts.")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, hold {HOLD0}, N {N0},")
    P(f"#   cadence {FREQ0}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END},")
    P(f"#   block L={L_HEAD}, {BDRAWS} draws, crc32 seeds, seed bases {SEED_BASES}.")
    P(f"# PRIOR QUOTED, NOT RECOMPUTED: {A1141_NOTE}")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_PATH_FIRES    at the FULL tape every PATH statistic (MAXDD, ULCER, CALMAR) is")
    P("#                       INF at BOTH rung sets on all 4 mover blocks — 12 of 12 — i.e.")
    P("#                       DD's robustness is shared by its matched path partners.")
    P("#   (b) H_NONPATH_ESC   at the FULL tape at least one NON-PATH statistic ESCAPES (fires")
    P("#                       at CORE, silent at EXT) on at least one mover block.")
    P("#   (c) H_EXPONENT      THE DECISIVE TEST.  Median resolution-ratio exponent over the")
    P("#                       three tape lengths is >= +0.35 for the NON-PATH arm and")
    P("#                       <= +0.20 for the PATH arm.  (Moment functionals: gap flat in T,")
    P("#                       SD ~ T^-0.5, so ratio ~ T^+0.5.  Path functionals: gap grows")
    P("#                       with T too, so the ratio is flat.)")
    P("#   (d) H_GAP_GROWS     the MECHANISM leg: median |gap| exponent is > +0.10 for the")
    P("#                       PATH arm and within +/-0.10 of zero for the NON-PATH arm.")
    P("#   (e) H_TAPE_ESCAPE   the TAPE reading's own prediction: MAXDD becomes RESOLVABLE on")
    P("#                       at least one of the five shortened disjoint sub-tapes at EXT.")
    P("#   (f) NOT A KEEP PATH no book is proposed.  The 74 books are byte-identical to")
    P("#                       1131's by construction, so 4a/4b and rule 8 are INVARIANT to")
    P("#                       both dials; they are scored at every rung because rule 4")
    P("#                       requires it, not because anything here is a candidate.")
    P("# DECISION RULE, declared before any number:")
    P("#   PATH-FUNCTIONAL  iff H_PATH_FIRES and H_NONPATH_ESC and H_EXPONENT.")
    P("#   TAPE             iff H_TAPE_ESCAPE and the PATH arm's exponent is NOT below the")
    P("#                    NON-PATH arm's.")
    P("#   MIXED            anything else, and it is reported as MIXED, not rounded to either.")
    P("#   THE CONFOUND, NAMED FIRST: a SHORTER tape is noisier, so firing counts must RISE at")
    P("#   1/2 and 1/3 for EVERY statistic.  That is why the headline is the EXPONENT (a")
    P("#   ratio of two things that both move) and not the firing count.  A sub-tape firing")
    P("#   count is reported but is NOT evidence for the PATH reading.")
    P("")

    gaterows, gates = [], {}
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig)
        P(f"  {panel}: {len(px.columns)} names, {len(idx):,} rows {idx[0].date()} -> "
          f"{idx[-1].date()}, warm {warm.sum():,}, IS {ins.sum():,}, OOS {oos.sum():,}")

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

    cells = []          # one row per (base, panel, ladder, rung_set, stat, subtape, q)
    levels = []         # one row per (panel, ladder, rung, subtape, stat): the realised level
    P("## BOOTSTRAP — 2 panels x 4 ladders x 6 sub-tapes x 3 seed bases")
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
                    bo = boot_six(Rs, ix, nb, L_HEAD)
                    vals = {s: np.array([stats6(Rs[i])[s] for i in range(len(rl))], float)
                            for s in STATS6}
                    if base == SEED_BASES[0]:
                        for i, rg in enumerate(rl):
                            for s in STATS6:
                                levels.append(dict(panel=panel, ladder=lad, rung=rg, subtape=nm,
                                                   frac=f, n=hi - lo, stat=s, is_path=IS_PATH[s],
                                                   value=vals[s][i]))
                    for s in STATS6:
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
                                    subtape=nm, frac=f, n=hi - lo, q=q,
                                    inf=bool(not np.isfinite(flo)),
                                    floor=(np.nan if not np.isfinite(flo) else flo),
                                    med_gap=mg, med_sd=msd, med_ratio=mratio,
                                    mean_agree=magr, n_pairs=npair))
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")
    C = pd.DataFrame(cells)
    LV = pd.DataFrame(levels)
    dump(C, "cells")
    dump(LV, "levels")

    # ---- G9: reproduce 1131's committed 16-block table on the three SHARED statistics
    # 1131's S_FULL == this run's SHARPE, its CAGR == CAGR, its DD == MAXDD, all on the FULL
    # warm tape at q=0.90, seed base 11311131, identical rung lists and identical draws.
    MAP1131 = {"S_FULL": "SHARPE", "CAGR": "CAGR", "DD": "MAXDD"}
    blk = pd.read_csv(f"{PRIOR1131}.blocks.csv")
    head0 = C[(C.base == SEED_BASES[0]) & (C.q == Q_HEAD) & (C.frac == 1)]
    hi_ = head0.set_index(["panel", "ladder", "stat", "rung_set"])["inf"]
    bad9 = n9 = 0
    for _, r in blk.iterrows():
        if r["stat"] not in MAP1131:
            continue
        s = MAP1131[r["stat"]]
        n9 += 1
        mine_core = bool(hi_.loc[(r["panel"], r["ladder"], s, "CORE")])
        mine_ext = bool(hi_.loc[(r["panel"], r["ladder"], s, "EXT")])
        bad9 += int(mine_core != bool(r["fires_CORE"])) + int(mine_ext != bool(r["fires_EXT"]))
    gates["G9"] = bad9 == 0 and n9 == 12
    gaterows.append(dict(gate="G9", what=f"reproduce 1131's committed block table ({n9} shared blocks)",
                         value=float(bad9), pass_=gates["G9"]))
    P(f"  G9  CROSS-RUN 1131's committed 16-block table, {n9} shared blocks  {bad9:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}")

    g10 = float(C.groupby("stat").med_gap.apply(lambda x: np.nanmin(np.abs(x))).min())
    gates["G10"] = g10 > 0
    gaterows.append(dict(gate="G10", what="every statistic live (min median |gap| > 0)",
                         value=g10, pass_=gates["G10"]))
    P(f"  G10 every statistic live (min median |gap|)               {g10:.2e}   {'PASS' if gates['G10'] else 'FAIL'}")
    dump(pd.DataFrame(gaterows), "gates")
    P(f"  GATES {sum(gates.values())} of {len(gates)} PASS")
    if not all(gates.values()):
        P("  !! A GATE FAILED — every number below is reported anyway and must be read as suspect.")
    P("")

    # ------------------------------------------------ RESULT 1: THE FULL-TAPE BLOCK TABLE, x6
    P("## RESULT 1 — 1131's 16-block table, re-run with all SIX statistics on the FULL tape")
    P("##   (q = 0.90, seed base 11311131; ROBUST = fires at BOTH rung sets, ESCAPABLE = fires")
    P("##   at CORE and is silent at EXT, INDUCED = the reverse, DEAD = fires at neither)")
    brows = []
    for base in SEED_BASES:
        h = C[(C.base == base) & (C.q == Q_HEAD) & (C.frac == 1)]
        hh = h.set_index(["panel", "ladder", "stat", "rung_set"])["inf"]
        for panel in PANELS:
            for lad in LADDERS:
                for s in STATS6:
                    fc = bool(hh.loc[(panel, lad, s, "CORE")])
                    fe = bool(hh.loc[(panel, lad, s, "EXT")])
                    cls = ("ROBUST" if fc and fe else "ESCAPABLE" if fc else
                           "INDUCED" if fe else "DEAD")
                    brows.append(dict(base=base, panel=panel, ladder=lad, stat=s,
                                      is_path=IS_PATH[s], rung_set_moves=MOVES[lad],
                                      fires_CORE=fc, fires_EXT=fe, cls=cls))
    B = pd.DataFrame(brows)
    dump(B, "blocks")
    b0 = B[(B.base == SEED_BASES[0]) & B.rung_set_moves]
    P(b0.pivot_table(index=["panel", "ladder"], columns="stat", values="cls",
                     aggfunc="first").reindex(columns=STATS6).to_string())
    P("")
    P("  by ARM over the 4 mover blocks (H and CADENCE on both panels), headline seed base:")
    for s in STATS6:
        z = b0[b0.stat == s]
        P(f"    {'PATH    ' if IS_PATH[s] else 'NON-PATH'} {s:7s}  ROBUST {int((z.cls == 'ROBUST').sum())}/4"
          f"   ESCAPABLE {int((z.cls == 'ESCAPABLE').sum())}/4"
          f"   INDUCED {int((z.cls == 'INDUCED').sum())}/4"
          f"   DEAD {int((z.cls == 'DEAD').sum())}/4")
    P("  ACROSS ALL THREE SEED BASES (12 mover cells per statistic):")
    for s in STATS6:
        z = B[B.rung_set_moves & (B.stat == s)]
        P(f"    {s:7s}  ROBUST {int((z.cls == 'ROBUST').sum())}/12   ESCAPABLE "
          f"{int((z.cls == 'ESCAPABLE').sum())}/12   INDUCED {int((z.cls == 'INDUCED').sum())}/12"
          f"   DEAD {int((z.cls == 'DEAD').sum())}/12")
    P("  N and GROSS (rung lists IDENTICAL at both levels — inescapable BY CONSTRUCTION, shown")
    P("  for completeness and excluded from every mover count above):")
    bn = B[(B.base == SEED_BASES[0]) & ~B.rung_set_moves]
    P("   " + bn.pivot_table(index=["panel", "ladder"], columns="stat", values="cls",
                             aggfunc="first").reindex(columns=STATS6).to_string().replace("\n", "\n   "))
    P("")
    P("  THE MATCHED-PAIR READING (same role, the ONLY difference is path-vs-moment):")
    for role, npn, pn in PAIRS:
        zn = B[B.rung_set_moves & (B.stat == npn)]
        zp = B[B.rung_set_moves & (B.stat == pn)]
        P(f"    {role:11s}  {npn:7s} ROBUST {int((zn.cls == 'ROBUST').sum()):2d}/12   vs   "
          f"{pn:7s} ROBUST {int((zp.cls == 'ROBUST').sum()):2d}/12")
    P("")

    # ---------------------------------------- RESULT 2: THE SUB-TAPE FIRING COUNTS (CONFOUNDED)
    P("## RESULT 2 — the SUB-TAPE firing counts, 9 DIAL COMBINATIONS, ALL PUBLISHED")
    P("##   (STAT SET x SUB-TAPE FRACTION; share of mover cells that read INF at EXT, q=0.90,")
    P("##   pooled over 3 seed bases, 2 panels, 2 mover ladders and the sub-tapes of that")
    P("##   fraction).  READ WITH THE CONFOUND: a shorter tape is noisier, so this share MUST")
    P("##   rise at 1/2 and 1/3 for every arm.  It is NOT the test.")
    grid = []
    hq = C[(C.q == Q_HEAD) & (C.rung_set == "EXT") & C.rung_set_moves]
    for setname, slist in STAT_SETS.items():
        for f in FRACS:
            z = hq[hq.stat.isin(slist) & (hq.frac == f)]
            grid.append(dict(stat_set=setname, frac=f"1/{f}", n_cells=len(z),
                             inf_share=float(z.inf.mean()) if len(z) else np.nan,
                             med_ratio=float(np.nanmedian(z.med_ratio)),
                             med_gap=float(np.nanmedian(np.abs(z.med_gap))),
                             med_sd=float(np.nanmedian(z.med_sd)),
                             mean_agree=float(np.nanmean(z.mean_agree))))
    GR = pd.DataFrame(grid)
    dump(GR, "grid")
    P(GR.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  the same 9 cells at q = 0.80 and q = 0.95 (reported beside, never selected on):")
    for q in (0.80, 0.95):
        zq = C[(C.q == q) & (C.rung_set == "EXT") & C.rung_set_moves]
        line = [f"    q={q:.2f}  "]
        for setname, slist in STAT_SETS.items():
            for f in FRACS:
                z = zq[zq.stat.isin(slist) & (zq.frac == f)]
                line.append(f"{setname}/1/{f} {z.inf.mean():.3f}  ")
        P("".join(line))
    P("")
    P("  per-statistic INF share at EXT by fraction (all 6 statistics, all 3 fractions):")
    pv = hq.pivot_table(index="stat", columns="frac", values="inf", aggfunc="mean")
    pv = pv.reindex(STATS6)
    pv.columns = [f"1/{c}" for c in pv.columns]
    P("   " + pv.to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P("")

    # -------------------------------------------- RESULT 3: THE DECISIVE TEST — THE EXPONENTS
    P("## RESULT 3 — THE DECISIVE TEST: the RESOLUTION EXPONENT")
    P("##   For each (panel, ladder, statistic, rung set) fit log(y) = a + b*log(n) over the")
    P("##   SIX sub-tapes (n = 1, 1/2, 1/2, 1/3, 1/3, 1/3 of the warm tape), for")
    P("##     y = median resolution ratio |gap| / SD(gap)   -> PREDICTED b = +0.5 non-path, 0 path")
    P("##     y = median |gap|                              -> PREDICTED b = 0 non-path, > 0 path")
    P("##     y = median SD(gap)                            -> PREDICTED b = -0.5 non-path")
    P("##   Pooled over the 3 seed bases by taking the median y per (cell, sub-tape) first.")
    ex = []
    key = ["panel", "ladder", "rung_set", "stat"]
    med = (C[C.q == Q_HEAD].groupby(key + ["subtape", "frac", "n"], as_index=False)
           [["med_ratio", "med_gap", "med_sd", "mean_agree"]].median())
    for k, z in med.groupby(key):
        panel, lad, rs, s = k
        ex.append(dict(panel=panel, ladder=lad, rung_set=rs, stat=s, is_path=IS_PATH[s],
                       rung_set_moves=MOVES[lad], n_subtapes=len(z),
                       b_ratio=loglog_slope(z.n, z.med_ratio),
                       b_gap=loglog_slope(z.n, np.abs(z.med_gap)),
                       b_sd=loglog_slope(z.n, z.med_sd),
                       b_agree=loglog_slope(z.n, z.mean_agree)))
    EX = pd.DataFrame(ex)
    dump(EX, "exponents")
    P("  MEDIAN EXPONENT by statistic, over all 2 panels x 4 ladders x 2 rung sets = 16 cells:")
    P(f"    {'statistic':9s} {'arm':9s} {'b(ratio)':>9s} {'b(gap)':>9s} {'b(SD)':>9s} {'b(agree)':>9s}")
    for s in STATS6:
        z = EX[EX.stat == s]
        P(f"    {s:9s} {'PATH' if IS_PATH[s] else 'NON-PATH':9s} "
          f"{np.nanmedian(z.b_ratio):9.4f} {np.nanmedian(z.b_gap):9.4f} "
          f"{np.nanmedian(z.b_sd):9.4f} {np.nanmedian(z.b_agree):9.4f}")
    bnp = float(np.nanmedian(EX[~EX.is_path].b_ratio))
    bp = float(np.nanmedian(EX[EX.is_path].b_ratio))
    gnp = float(np.nanmedian(EX[~EX.is_path].b_gap))
    gp = float(np.nanmedian(EX[EX.is_path].b_gap))
    snp = float(np.nanmedian(EX[~EX.is_path].b_sd))
    sp = float(np.nanmedian(EX[EX.is_path].b_sd))
    P(f"  ARM MEDIANS       NON-PATH b(ratio) {bnp:+.4f}   PATH b(ratio) {bp:+.4f}   "
      f"separation {bnp - bp:+.4f}")
    P(f"  MECHANISM         NON-PATH b(gap)   {gnp:+.4f}   PATH b(gap)   {gp:+.4f}")
    P(f"                    NON-PATH b(SD)    {snp:+.4f}   PATH b(SD)    {sp:+.4f}")
    P("  MATCHED PAIRS (b(ratio), median over the 16 cells):")
    for role, npn, pn in PAIRS:
        a_ = float(np.nanmedian(EX[EX.stat == npn].b_ratio))
        b_ = float(np.nanmedian(EX[EX.stat == pn].b_ratio))
        P(f"    {role:11s} {npn:7s} {a_:+.4f}   vs   {pn:7s} {b_:+.4f}   gap {a_ - b_:+.4f}")
    P("  MOVER LADDERS ONLY (H and CADENCE, the 8 cells 1131's headline lives on):")
    mvx = EX[EX.rung_set_moves]
    for s in STATS6:
        z = mvx[mvx.stat == s]
        P(f"    {s:9s} b(ratio) {np.nanmedian(z.b_ratio):+.4f}   b(gap) {np.nanmedian(z.b_gap):+.4f}"
          f"   b(SD) {np.nanmedian(z.b_sd):+.4f}")
    P("")

    # --------------------------------- RESULT 4: DOES MAXDD EVER ESCAPE ON A SHORTENED TAPE?
    P("## RESULT 4 — the TAPE reading's own prediction: does MAXDD become RESOLVABLE on any")
    P("##   SHORTENED disjoint sub-tape at EXT?  (all 3 seed bases, both panels, both mover")
    P("##   ladders, the 5 shortened sub-tapes, q=0.90)")
    dsub = C[(C.q == Q_HEAD) & (C.rung_set == "EXT") & C.rung_set_moves & (C.stat == "MAXDD")]
    dshort = dsub[dsub.frac > 1]
    res = dshort[~dshort.inf]
    P(f"  MAXDD cells on shortened tapes: {len(dshort)};  RESOLVABLE (not INF): {len(res)}")
    if len(res):
        P("   " + res[["base", "panel", "ladder", "subtape", "floor", "med_ratio",
                       "mean_agree"]].to_string(index=False,
                                                float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P(f"  and on the FULL tape: {int((~dsub[dsub.frac == 1].inf).sum())} of "
      f"{int((dsub.frac == 1).sum())} resolvable")
    P("  the same question for every statistic (share RESOLVABLE at EXT on shortened tapes):")
    for s in STATS6:
        z = C[(C.q == Q_HEAD) & (C.rung_set == "EXT") & C.rung_set_moves & (C.stat == s) & (C.frac > 1)]
        zf = C[(C.q == Q_HEAD) & (C.rung_set == "EXT") & C.rung_set_moves & (C.stat == s) & (C.frac == 1)]
        P(f"    {s:9s} shortened {int((~z.inf).sum()):3d}/{len(z):3d}   full tape "
          f"{int((~zf.inf).sum()):2d}/{len(zf):2d}")
    P("")
    P("## RESULT 5 — the LEVEL leg 1110 flagged: does each statistic's own LEVEL grow with the")
    P("##   tape it is measured on?  (median over rungs of |value|, by fraction, headline seed)")
    lv = LV.groupby(["stat", "frac"]).value.apply(lambda x: float(np.nanmedian(np.abs(x)))).unstack()
    lv.columns = [f"1/{c}" for c in lv.columns]
    lv["b(level)"] = [loglog_slope(
        LV[LV.stat == s].groupby("frac").n.median().values,
        LV[LV.stat == s].groupby("frac").value.apply(lambda x: float(np.nanmedian(np.abs(x)))).values)
        for s in lv.index]
    P("   " + lv.reindex(STATS6).to_string(float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P("")

    # ------------------------------------ RESULT 6: POST-HOC AND LABELLED AS SUCH
    P("## RESULT 6 — POST-HOC, LABELLED.  A DEFECT IN THIS RUN'S OWN PRE-REGISTERED ARM")
    P("##   MEDIAN, found after the numbers were printed and reported rather than fixed.")
    P("##   H_EXPONENT's arm medians pool ALL 16 (panel, ladder, rung set) cells per statistic,")
    P("##   including the N and GROSS ladders whose rung set CANNOT move and on which 1131's")
    P("##   claim does not live.  The question is about H and CADENCE.  Restricting to those")
    P("##   8 cells is a RE-CUT OF ALREADY-PUBLISHED COLUMNS, not a third dial — and it moves")
    P("##   the exponent comparison, so it is published beside the pre-registered one and the")
    P("##   pre-registered verdict is NOT rewritten.")
    h_exponent = bool(np.isfinite(bnp) and np.isfinite(bp) and bnp >= 0.35 and bp <= 0.20)
    mvnp = float(np.nanmedian(mvx[~mvx.is_path].b_ratio))
    mvp = float(np.nanmedian(mvx[mvx.is_path].b_ratio))
    mvgnp = float(np.nanmedian(mvx[~mvx.is_path].b_gap))
    mvgp = float(np.nanmedian(mvx[mvx.is_path].b_gap))
    mvsnp = float(np.nanmedian(mvx[~mvx.is_path].b_sd))
    mvsp = float(np.nanmedian(mvx[mvx.is_path].b_sd))
    P(f"  PRE-REGISTERED (all 16 cells)  NON-PATH b(ratio) {bnp:+.4f}   PATH {bp:+.4f}   "
      f"separation {bnp - bp:+.4f}   => H_EXPONENT {h_exponent}")
    P(f"  POST-HOC (mover ladders only)  NON-PATH b(ratio) {mvnp:+.4f}   PATH {mvp:+.4f}   "
      f"separation {mvnp - mvp:+.4f}")
    P(f"  POST-HOC mechanism             NON-PATH b(gap) {mvgnp:+.4f} / b(SD) {mvsnp:+.4f}   "
      f"PATH b(gap) {mvgp:+.4f} / b(SD) {mvsp:+.4f}")
    P("  THE SIGN THAT MATTERS, and it is NOT the one either reading predicted: on the mover")
    P("  ladders the NON-PATH arm's resolution ratio gets WORSE with a LONGER tape, because")
    P("  its realised rung GAP shrinks FASTER than its sampling SD does.  SD falls at about")
    P(f"  n^{mvsnp:+.2f} (textbook is -0.50); the gap falls at n^{mvgnp:+.2f}.  A gap that")
    P("  converges to ~0 is a rung effect that IS ~0: more tape will never resolve it.")
    P("  MAXDD alone has BOTH exponents POSITIVE — its gap AND its dispersion GROW with the")
    P("  tape.  That is the EXTREME-VALUE signature (a maximum over a longer path is larger")
    P("  and more dispersed), and it is NOT shared by the two path functionals that AVERAGE")
    P("  (ULCER, a root-mean-square of the same drawdown path) or that DIVIDE BY the maximum")
    P("  (CALMAR).  So the carrier is MAX-ness, a strict SUBSET of path-functionality.")
    ph = []
    for s in STATS6:
        z = mvx[mvx.stat == s]
        zz = EX[EX.stat == s]
        ph.append(dict(stat=s, is_path=IS_PATH[s],
                       b_ratio_movers=float(np.nanmedian(z.b_ratio)),
                       b_gap_movers=float(np.nanmedian(z.b_gap)),
                       b_sd_movers=float(np.nanmedian(z.b_sd)),
                       b_ratio_all=float(np.nanmedian(zz.b_ratio)),
                       b_gap_all=float(np.nanmedian(zz.b_gap)),
                       b_sd_all=float(np.nanmedian(zz.b_sd)),
                       both_exponents_positive=bool(np.nanmedian(z.b_gap) > 0 and
                                                    np.nanmedian(z.b_sd) > 0)))
    PH = pd.DataFrame(ph)
    dump(PH, "posthoc")
    P("   " + PH.to_string(index=False, float_format=lambda x: f"{x:+.4f}").replace("\n", "\n   "))
    P("")

    P("## RESULT 7 — THE SECOND CONFOUND, NAMED: a sub-tape differs from the full tape in")
    P("##   LENGTH *and* in REGIME.  Size of each, measured on the SAME published column")
    P("##   (median resolution ratio at EXT on the mover ladders, headline q):")
    zz = C[(C.q == Q_HEAD) & (C.rung_set == "EXT") & C.rung_set_moves]
    reg = []
    for s in STATS6:
        z = zz[zz.stat == s]
        within = z[z.frac > 1].groupby(["panel", "ladder", "frac", "base"]).med_ratio.apply(
            lambda x: float(np.nanmax(x) - np.nanmin(x)))
        between = abs(float(np.nanmedian(z[z.frac == 1].med_ratio)) -
                      float(np.nanmedian(z[z.frac == 3].med_ratio)))
        reg.append(dict(stat=s, is_path=IS_PATH[s],
                        within_fraction_spread=float(np.nanmedian(within)),
                        between_fraction_move=between,
                        regime_over_length=(float(np.nanmedian(within)) / between
                                            if between > 0 else np.nan)))
    RG = pd.DataFrame(reg)
    dump(RG, "regime")
    P("   " + RG.to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
    P("  WITHIN-fraction spread is pure REGIME (same length, different stretch of tape);")
    P("  BETWEEN-fraction move is length plus regime.  Where the ratio above exceeds 1 the")
    P("  length effect this run fits is SMALLER than the regime noise it is fitted through,")
    P("  and the exponent for that statistic should be read as an upper bound on precision,")
    P("  not as a measurement.  This is a LIMIT of the design, stated, not a result.")
    P("")

    P("## RESULT 8 — WHERE MAXDD DOES ESCAPE: the structure of the 13 resolvable cells")
    esc_struct = (dshort[~dshort.inf].groupby(["panel", "ladder", "subtape"]).size()
                  .rename("n_seed_bases").reset_index())
    dump(esc_struct, "ddescapes")
    P("   " + esc_struct.to_string(index=False).replace("\n", "\n   ")
      if len(esc_struct) else "   none")
    P(f"  {len(esc_struct)} distinct (panel, ladder, sub-tape) combinations out of "
      f"{dshort.groupby(['panel', 'ladder', 'subtape']).ngroups}; the rest are INF at every")
    P("  seed base.  So MAXDD's un-resolvability is not absolute — there ARE stretches of")
    P("  this record on which its rung gaps resolve — but it is the most robust of the six")
    P("  statistics at EVERY fraction, which is why neither reading of the idea survives whole.")
    P("")

    # ------------------------------------------------- THE PRICE LEG: RULE 8 WALK-FORWARD
    P("## THE PRICE LEG — RULE 8 WALK-FORWARD.  Rung chosen on IS 2009-2016 ALONE; OOS")
    P("##   2017-2026 read ONCE.  Scored against that ladder's FROZEN DEFAULT rung, against")
    P("##   SPY and against the live RULES v2 book.  BOTH KEEP PATHS scored at every rung.")
    P("##   The books are byte-identical to 1131's, so this leg is INVARIANT to both dials.")
    gi = G.set_index(["panel", "ladder", "rung"])
    wf = []
    for panel in PANELS:
        sb, lbm = panels[panel]["spy_m"], lb[panel]
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                sub = G[(G.panel == panel) & (G.ladder == lad) & (G.rung.isin(rungs))]
                dref = gi.loc[(panel, lad, DEFAULT_RUNG[lad])]
                for ch, (iscol, ooscol, sign) in CHOOSERS.items():
                    pick = sub.loc[sub[iscol].idxmax()]
                    best = sub.loc[sub[ooscol].idxmax()]
                    fullbest = sub.loc[sub["Sharpe"].idxmax()]
                    wf.append(dict(
                        panel=panel, ladder=lad, rung_set=rs, chooser=ch, k=len(rungs),
                        pick=pick["rung"], default=DEFAULT_RUNG[lad], full_argmax=fullbest["rung"],
                        pick_is_default=bool(pick["rung"] == DEFAULT_RUNG[lad]),
                        pick_is_full_argmax=bool(pick["rung"] == fullbest["rung"]),
                        CAGR=pick["CAGR"], Sharpe=pick["Sharpe"], MaxDD=pick["MaxDD"],
                        H1=pick["H1"], H2=pick["H2"], OOS_CAGR=pick["OOS_CAGR"],
                        OOS_Sharpe=pick["OOS_Sharpe"], OOS_MaxDD=pick["OOS_MaxDD"],
                        adv_matched=sign * float(pick[ooscol] - dref[ooscol]),
                        adv_oos_sharpe=float(pick["OOS_Sharpe"] - dref["OOS_Sharpe"]),
                        regret=float(sign * (best[ooscol] - pick[ooscol])),
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
    P(f"  IS picks: {len(WF)} — 4b full {int(WF.pass_4b_full.sum())}, 4b OOS "
      f"{int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}, median OOS Sharpe "
      f"{WF.OOS_Sharpe.median():.4f}, median regret {WF.regret.median():+.4f}")
    P(f"  whole grid {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, 4b OOS "
      f"{int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}")
    pw = WF[WF.pass_4b_full]
    P("  EVERY IS PICK THAT CLEARS 4b (full), with its OOS triple:")
    if len(pw):
        P("   " + pw[["panel", "ladder", "rung_set", "chooser", "pick", "pick_is_default", "CAGR",
                      "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n   "))
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
    mv12 = B[B.rung_set_moves]
    path_rob = int((mv12[mv12.stat.isin(PATH)].cls == "ROBUST").sum())
    path_tot = int(len(mv12[mv12.stat.isin(PATH)]))
    path_rob_hd = int((b0[b0.stat.isin(PATH)].cls == "ROBUST").sum())
    nonpath_esc = int((mv12[mv12.stat.isin(NONPATH)].cls == "ESCAPABLE").sum())
    dd_escapes = int((~dshort.inf).sum())

    h_path_fires = bool(path_rob_hd == 12)
    h_nonpath_esc = bool(nonpath_esc > 0)
    h_exponent = bool(np.isfinite(bnp) and np.isfinite(bp) and bnp >= 0.35 and bp <= 0.20)
    h_gap_grows = bool(np.isfinite(gp) and np.isfinite(gnp) and gp > 0.10 and abs(gnp) <= 0.10)
    h_tape_escape = bool(dd_escapes > 0)

    HYP = {
        "H_PATH_FIRES": (h_path_fires, f"PATH arm ROBUST on the 4 mover blocks x 3 statistics: "
                                       f"{path_rob_hd} of 12 at the headline seed base "
                                       f"({path_rob} of {path_tot} over all 3 bases)"),
        "H_NONPATH_ESC": (h_nonpath_esc, f"NON-PATH ESCAPABLE cells over all 3 bases: "
                                         f"{nonpath_esc} of {len(mv12[mv12.stat.isin(NONPATH)])}"),
        "H_EXPONENT": (h_exponent, f"median b(ratio) NON-PATH {bnp:+.4f} (bar >= +0.35), PATH "
                                   f"{bp:+.4f} (bar <= +0.20), separation {bnp - bp:+.4f}"),
        "H_GAP_GROWS": (h_gap_grows, f"median b(gap) PATH {gp:+.4f} (bar > +0.10), NON-PATH "
                                     f"{gnp:+.4f} (bar |.| <= 0.10)"),
        "H_TAPE_ESCAPE": (h_tape_escape, f"MAXDD RESOLVABLE on {dd_escapes} of {len(dshort)} "
                                         f"shortened-sub-tape mover cells at EXT"),
    }
    P("## HYPOTHESES, declared before any number")
    for k, (ok, why) in HYP.items():
        P(f"  {'SUPPORTED' if ok else 'REFUTED  '}  {k:15s} {why}")
    P(f"  {sum(1 for v in HYP.values() if v[0])} of {len(HYP)} SUPPORTED")
    dump(pd.DataFrame([dict(hypothesis=k, supported=v[0], evidence=v[1]) for k, v in HYP.items()]),
         "hypotheses")
    P("")

    # -------------------------------------------------------------------------------- VERDICT
    is_path_verdict = h_path_fires and h_nonpath_esc and h_exponent
    is_tape_verdict = h_tape_escape and np.isfinite(bp) and np.isfinite(bnp) and bp >= bnp
    verdict = ("PATH-FUNCTIONAL" if is_path_verdict else
               "TAPE" if is_tape_verdict else "MIXED")
    P("## THE ANSWER (decision rule declared before any number)")
    P(f"  H_PATH_FIRES {h_path_fires}   H_NONPATH_ESC {h_nonpath_esc}   H_EXPONENT {h_exponent}")
    P(f"  H_TAPE_ESCAPE {h_tape_escape}   PATH b(ratio) {bp:+.4f} vs NON-PATH {bnp:+.4f}")
    P(f"  => the idea is answered: {verdict}")
    P(f"  SURVIVORSHIP (rule 9): U56 and B136 are CURRENT-CONSTITUENT panels.  Every level")
    P(f"  above is optimistic and the exponents are measured on that inflated tape.")
    P(f"  {A1141_NOTE}")
    P("")
    P(f"\n# done in {time.time() - t0:.0f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
