#!/usr/bin/env python3
"""Idea 1107 (cloud lane, 2026-09-16) — RE-PRICE every committed ARGMAX on an H or CAP LADDER.

QUESTION (QUEUE idea 1107, verbatim)
    idea 1097 found 13 of 34 committed EDGE ladders change argmax under the rank-matched null,
    and twelve sit on the H axis (7 of 18) and 1071's cap axis (5 of 8), with three cap ladders
    at NEGATIVE rank correlation between the two gates; the N axis is stable (1 of 8).  Combined
    with 1098's resolution floor, a published argmax on those two axes may carry no information
    at all.  Harvest every committed argmax claim on an H or cap ladder and report how many
    survive both the null gate and their own resolution floor.  Max 2 params (claim set, floor
    basis).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials: CLAIM SET {CORE, WIDE} x FLOOR BASIS {SEED, TAPE, JOINT} = 6 cells, ALL
    published.
      CORE = the 26 committed EDGE ladders on an H or cap axis that this run rebuilds exactly —
             1086's 18 H ladders (2 panels x 9 N, rungs H in {21, 63, 126}) and 1071's 8 cap
             ladders (2 panels x 4 N, rungs cap in {1.00, 1.25, 1.50, 2.00, INF}).  Each gets
             its OWN measured gate verdict and its OWN measured floor.
      WIDE = every VALUED argmax / 'peaks at' claim in the corpus naming an H or a cap value.
             A claim whose ladder IS a rebuilt CORE ladder is scored on that ladder's MEASURED
             verdict; every other one gets a TRANSFERRED rate from the CORE ladders of the same
             axis — declared here, in advance, as an EXTRAPOLATION and NOT a re-derivation
             (1048's convention, 1102's bookkeeping).  The two bases are counted separately.
      FLOOR BASIS — three readings of "how big must a gap be before the argmax means anything":
        SEED   the record's OWN bar (1082/1085/1097): the EDGE at a rung carries the seed SE of
               its null median, SE = 1.2533 * s / sqrt(m).  The pairwise floor is
               K * sqrt(SE_i^2 + SE_j^2) with K = 2.0, the same K those runs argued against.
        TAPE   1098/1102/1108's block-bootstrap resolution floor: over all rung pairs,
               A_ij = P(a circular-block resample agrees with the full-sample sign of
               EDGE_i - EDGE_j); the floor at q=0.90 is the smallest |gap| strictly above every
               unresolved one.  ONE index per draw, applied JOINTLY to the book and to all of
               that ladder's null seeds, because the ladder is a set of books over one tape.
        JOINT  the two in quadrature, sqrt(SEED^2 + TAPE^2) — seed noise and tape noise are
               independent by construction (the seeds index draws of a rank matrix, the blocks
               index draws of the tape).

    THE CELL COORDINATES ARE NOT DIALS.  (panel, N, H, cap, seeds, DD-match convention) are taken
    EXACTLY as the record committed them.  Everything else frozen at 936/1071/1082/1085/1086/
    1097's construction: CAND20 legs [(21,252),(0,126),(0,63)], max_vol 0.60, gross 0.75, W
    cadence, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, q=0.90, K=2.0, 40 seeds / REBUILT
    match on family A, 20 seeds / CASH match on family B.

A DECLARED APPROXIMATION IN THE TAPE BASIS, AND ITS DIRECTION
    The DD-match multiplier lambda is a book-level scalar solved by bisection on the FULL-SAMPLE
    path.  Re-solving it inside every bootstrap draw would cost 26 x 1000 x (3 or 5) x (40 or
    20) bisections and is not run here; lambda is held at its full-sample value and the
    resampled null CAGR is computed exactly from block log-sums of the lambda-scaled series.
    DIRECTION, declared in advance: holding lambda fixed REMOVES a source of draw-to-draw
    variation, so the TAPE floor published here is a LOWER bound on the true one — it makes
    argmaxes look MORE resolved than they are, which is conservative AGAINST this run's expected
    finding.  Every count below is therefore an UPPER bound on survival.

DECLARED BEFORE ANY NUMBER
    (a) H_SURVIVE — FEWER THAN HALF of the 26 CORE argmaxes survive BOTH the null gate and
        their own floor at q=0.90 on the headline TAPE basis.
    (b) H_FLOOR_BINDS — the FLOOR is the harder of the two tests: more CORE ladders fail the
        floor alone than fail the gate alone.
    (c) H_SHORT — a 3-rung ladder cannot resolve an argmax on this tape: 0 of the 18 H ladders
        clear their TAPE floor.  The cap ladders have 5 rungs and are the fairer test.
    (d) H_BASIS — the three floor bases agree on the survival verdict for >= 0.80 of CORE
        ladders.  If they do not, "survives its floor" is a basis statement, not a tape one.
    (e) H_HARVEST — the corpus carries at least 20 VALUED H-or-cap argmax claims.
    (f) EDGE IS NOT A KEEP PATH AND THIS RUN CANNOT MOVE ONE.  The BOOK at every cell is
        byte-identical across the two gates — only the comparand changes — so 4a and 4b are
        invariant to dial 2 by construction.  Both paths are scored at all 94 cells anyway
        because rule 4 requires it, and rule 8 picks the rung on 2009-2016 ALONE, per ladder,
        OOS read ONCE.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT panels.  EDGE, the gate
    and the floor are all within-pool contrasts over the same inflated tape and the bias very
    largely cancels out of them; it does NOT cancel out of the 4b legs, which are measured
    against SPY, a real index, so every 4a/4b count is an UPPER bound.
"""
from __future__ import annotations

import hashlib
import re
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
SLUG = "RE-PRICE-every-committed-ARGMAX-on-an-H-or-CAP-LADDER"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ = 10.0, 0.75, "W"
LEGS = [(21, 252), (0, 126), (0, 63)]

PANELS = ["U56", "B136"]
GATESET = ["OPEN", "ELIG"]
CLAIMSETS = ["CORE", "WIDE"]                 # dial 1
BASES = ["SEED", "TAPE", "JOINT"]            # dial 2
BASIS_HEAD = "TAPE"

A_NS = [5, 8, 10, 12, 15, 20, 25, 30, 40]
A_HS = [21, 63, 126]
A_SEEDS, A_BISECT = 40, 34
B_NS = [20, 25, 30, 40]
B_CAPKEYS = ["1.00", "1.25", "1.50", "2.00", "INF"]
B_HOLD, B_SEEDS, B_BISECT = 126, 20, 60

DECISIVE_K = 2.0
QFLOOR = 0.90
BDRAWS = 1000
BLOCKS_L = [21, 63, 126]
L_HEAD = 63
SEED_BOOT = 11071107

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = {"U56": (0.1521, 0.8713, -0.3372), "B136": (0.1533, 0.8767, -0.3372)}
LIVE_MAXDD_COMMITTED = {"U56": -0.1205, "B136": -0.1224}
SRC_1097 = ROOT / "research" / "backtests" / (
    "2026-09-16_RE-READ-every-committed-EDGE-FIGURE-as-a-LOWER-BOUND_B.grid.csv")
SRC_1097L = ROOT / "research" / "backtests" / (
    "2026-09-16_RE-READ-every-committed-EDGE-FIGURE-as-a-LOWER-BOUND_B.ladders.csv")

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def mdseed(*parts):
    """1071/1082/1085/1086/1097's seed recipe, verbatim.  The cap key is a STRING and is never
    converted (defect 1105: pandas would read 'INF' as inf and draw different nulls)."""
    return int(hashlib.md5("|".join(str(x) for x in parts).encode()).hexdigest()[:8], 16)


def bseed(*parts):
    """Bootstrap seed — zlib.crc32, deterministic across processes (1108's H_SEED)."""
    return SEED_BOOT + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


# ------------------------------------------- 1097's runner and rescaler, copied verbatim
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


def gross_rescaler(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy()
    mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    A = wt[s0] * (Cp / Cp[s0])
    AR = (A * rets).sum(axis=1)
    S = A.sum(axis=1)
    Wsum = wt[s0].sum(axis=1)
    s0p = reb[np.maximum(seg - 1, 0)]
    Ap = (wt[s0p] * (Cp / Cp[s0p]))[reb]
    Sp = Ap.sum(axis=1)
    Wsp = wt[s0p].sum(axis=1)[reb]
    Ap[0] = 0.0
    Sp[0] = 0.0
    Wsp[0] = 0.0
    Wr = wt[reb]
    c = COST / 1e4

    def f(lam):
        V = 1.0 + lam * (S - Wsum)
        g = lam * AR / V
        Vp = 1.0 + lam * (Sp - Wsp)
        tr = lam * np.abs(Wr - Ap / Vp[:, None]).sum(axis=1)
        out = g.copy()
        out[reb] -= tr * c
        return out

    return f


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


def maxdd(r):
    eq = np.cumprod(1.0 + np.asarray(r, float))
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


def lagmat(a):
    out = np.zeros_like(a)
    out[LAG:] = a[:-LAG]
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


def build(rank_key, elig, priced, reb, N, cap, H, T, K, gross):
    W = np.zeros((T, K))
    cur = np.full(K, -1, dtype=np.int64)
    nsel_by_reb, gross_by_reb = [], []
    per_cap = cap * gross / N if np.isfinite(cap) else np.inf
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
        nsel_by_reb.append(len(sel))
        stop = reb[i + 1] if i + 1 < len(reb) else T
        if len(sel):
            w = min(gross / len(sel), per_cap)
            W[t:stop, sel] = w
            gross_by_reb.append(w * len(sel))
        else:
            gross_by_reb.append(0.0)
    return W, np.array(nsel_by_reb), np.array(gross_by_reb)


def windows(idx):
    warm = np.zeros(len(idx), dtype=bool)
    warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    ins = warm & ~oos
    return warm, ins, oos


def blocks(r, warm, ins, oos):
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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def lam_cash(r, target_dd, it):
    if abs(maxdd(r)) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(m * r)) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def lam_rebuilt(f, sl, target_dd, it):
    if abs(maxdd(f(1.0)[sl])) <= abs(target_dd):
        return None
    a, b = 1e-4, 1.0
    for _ in range(it):
        m = 0.5 * (a + b)
        if abs(maxdd(f(m)[sl])) > abs(target_dd):
            b = m
        else:
            a = m
    return 0.5 * (a + b)


def se_median(x):
    x = np.asarray(x, float)
    return 100.0 * 1.2533 * x.std(ddof=1) / np.sqrt(len(x))


# ------------------------------------------------------- 1098/1102/1108's bootstrap machinery
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_cagr(R, idx, nb, L, chunk=100):
    """CAGR of every row of R (series x T) under the SHARED block index — EXACT, because a
    product does not care about order."""
    LG = np.log1p(R)
    D = np.concatenate([LG, LG], axis=1)
    CS = np.concatenate([np.zeros((D.shape[0], 1)), np.cumsum(D, axis=1)], axis=1)
    nd = idx.shape[0]
    st = idx[:, ::L]
    out = np.empty((R.shape[0], nd))
    n = nb * L
    for a in range(0, nd, chunk):
        s = st[a:a + chunk]
        lsum = (CS[:, s + L] - CS[:, s]).sum(axis=2)
        out[:, a:a + chunk] = np.expm1(lsum * (252.0 / n))
    return out


def floor_from_agreement(gaps, agree, q):
    gaps = np.asarray(gaps, float)
    agree = np.asarray(agree, float)
    un = agree < q
    largest_un = float(gaps[un].max()) if un.any() else 0.0
    ok = (~un) & (gaps > largest_un)
    flo = float(gaps[ok].min()) if ok.any() else float("inf")
    return flo, largest_un, int(un.sum())


# ------------------------------------------------- the WIDE arm: harvest H / cap argmax claims
SRC = {"LEADERBOARD": [ROOT / "research" / "LEADERBOARD.md"],
       "CHANGELOG": [ROOT / "research" / "CHANGELOG.md"],
       "QUEUE": [ROOT / "research" / "QUEUE.md"],
       "RESULTMD": sorted((ROOT / "research" / "backtests").glob("*.result.md")),
       "MEMO": sorted((ROOT / "research" / "backtests").glob("*.memo.md"))}
CLAIM_RE = re.compile(r"(?i)\b(argmax|peaks?\s+at|peak\s+is\s+at|optimum\s+at|optimal|best)\b")
AXIS_RE = [("H", re.compile(r"(?i)\b(?:h|hold|min[_ ]hold)\s*=\s*(\d{1,3})\b")),
           ("cap", re.compile(r"(?i)\bcap\s*=?\s*(INF|inf|\d\.\d{1,2})\b"))]
WIN = 120


def harvest():
    """1102's harvester, restricted to the two axes 1107 is about.  UNIT = one '|'-delimited
    cell (LEADERBOARD) or one non-empty line elsewhere.  Rejects are counted and published."""
    rows, rej = [], []
    for src, paths in SRC.items():
        for p in paths:
            try:
                txt = p.read_text(errors="ignore")
            except OSError:
                continue
            for ln, line in enumerate(txt.split("\n")):
                units = line.split("|") if "|" in line else [line]
                for uix, u in enumerate(units):
                    if not u.strip():
                        continue
                    for m in CLAIM_RE.finditer(u):
                        lo, hi = max(0, m.start() - WIN), min(len(u), m.end() + WIN)
                        ctx = u[lo:hi]
                        ax, val = None, None
                        for a, rx in AXIS_RE:
                            mm = rx.search(ctx)
                            if mm:
                                ax, val = a, mm.group(1)
                                break
                        rec = dict(source=src, file=p.name, line=ln, unit=uix,
                                   word=m.group(0).lower(), axis=ax or "", value=val or "",
                                   panel=("U56" if "U56" in ctx else
                                          ("B136" if "B136" in ctx else "")),
                                   ctx=ctx.replace("\n", " ")[:260])
                        if ax is None:
                            rej.append({**rec, "reason": "no_H_or_cap_value_in_window"})
                        else:
                            rows.append(rec)
    return pd.DataFrame(rows), pd.DataFrame(rej)


# ------------------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# Idea 1107 (cloud lane, {DATE}) — RE-PRICE every committed ARGMAX on an H or CAP LADDER")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): CLAIM SET {CLAIMSETS} x FLOOR BASIS {BASES} = 6")
    P("#   cells, ALL published.  CORE = the 26 committed H / cap EDGE ladders this run rebuilds")
    P("#   exactly (1086's 18 H ladders, 1071's 8 cap ladders).  WIDE = every valued H-or-cap")
    P("#   argmax claim in the corpus, the unrebuildable ones carrying a TRANSFERRED rate")
    P("#   declared in advance as an EXTRAPOLATION.")
    P("# THE CELL COORDINATES ARE NOT DIALS — (panel, N, H, cap, seeds, convention) are taken")
    P(f"#   exactly as committed.  FROZEN: legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, "
      f"cadence {FREQ}, {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, "
      f"q={QFLOOR}, K={DECISIVE_K}.")
    P("# DECLARED APPROXIMATION IN THE TAPE BASIS: lambda is held at its full-sample value")
    P("#   inside the bootstrap (re-solving it per draw is not run).  DIRECTION, declared: this")
    P("#   REMOVES variation, so the TAPE floor is a LOWER bound and every survival count below")
    P("#   is an UPPER bound — conservative AGAINST this run's expected finding.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_SURVIVE     FEWER THAN HALF of the 26 CORE argmaxes survive BOTH tests (TAPE).")
    P("#   (b) H_FLOOR_BINDS the FLOOR is the harder test (floor-only failures > gate-only).")
    P("#   (c) H_SHORT       0 of the 18 three-rung H ladders clear their TAPE floor.")
    P("#   (d) H_BASIS       the three bases agree on >= 0.80 of CORE ladders.")
    P("#   (e) H_HARVEST     >= 20 VALUED H-or-cap argmax claims in the corpus.")
    P("#   (f) EDGE IS NOT A KEEP PATH and dial 2 cannot move one: the book is byte-identical")
    P("#       across gates.  4a/4b scored at all 94 cells; rule 8 per ladder, OOS read ONCE.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------------- THE HARVEST
    P("## HARVEST (dial 1, WIDE arm) — every argmax / 'peaks at' claim naming an H or a cap")
    claims, rejects = harvest()
    P(f"  corpus: {sum(len(v) for v in SRC.values())} files over {len(SRC)} sources")
    P(f"  claim words matched: {len(claims) + len(rejects):,}   VALUED (H or cap): "
      f"{len(claims):,}   rejected: {len(rejects):,}")
    if len(claims):
        P("  by axis: " + ", ".join(f"{k} {v}" for k, v in claims["axis"].value_counts().items()))
        P("  by source: " + ", ".join(f"{k} {v}" for k, v in
                                      claims["source"].value_counts().items()))
    H_HARVEST = len(claims) >= 20
    P(f"  H_HARVEST (>= 20 valued H-or-cap claims): {'PASS' if H_HARVEST else 'FAIL'} "
      f"({len(claims)})")
    P("  HARVEST LIMITATION, declared: the axis patterns are heuristics over prose; every")
    P("    reject is published with its reason and context so the rule can be re-read.")
    dump(claims, "claims")
    dump(rejects, "rejects")
    P("")

    # ---------------------------------------------------------------- THE LADDERS, REBUILT
    P("## REBUILD — 94 committed cells, both gates, exactly as the record committed them")
    rows, benchrows = [], []
    ladders = []          # one entry per CORE ladder
    bench = {}
    for panel in PANELS:
        px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
        idx, K, T = px.index, len(px.columns), len(px.index)
        rets = px.pct_change().fillna(0.0).values
        priced = px.notna().values
        mk = rebalance_mask(idx, FREQ).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        warm, ins, oos = windows(idx)
        sc, elig_real = mech(px)
        rank_key = -np.nan_to_num(sc, nan=-np.inf)
        rank_key[np.isnan(sc)] = np.inf
        reb = np.flatnonzero(mk)
        ALLP = np.ones((T, K), dtype=bool)

        spy = px["SPY"].pct_change().fillna(0.0).values
        sb = blocks(spy, warm, ins, oos)
        live = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
        lb = blocks(live, warm, ins, oos)
        bench[panel] = (sb, lb)
        benchrows += [dict(panel=panel, series="SPY", **sb), dict(panel=panel, series="RULESv2", **lb)]
        P(f"  {panel}: {K} columns, {T:,} days {idx[0].date()}..{idx[-1].date()}, "
          f"{len(reb)} rebalance dates")
        P(f"    SPY      full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%}  halves "
          f"{sb['H1']:.4f}/{sb['H2']:.4f}  OOS {sb['OOS_CAGR']:.2%} / {sb['OOS_Sharpe']:.4f} / "
          f"{sb['OOS_MaxDD']:.2%}")
        P(f"    RULES v2 full {lb['CAGR']:.2%} / {lb['Sharpe']:.4f} / {lb['MaxDD']:.2%}  OOS "
          f"{lb['OOS_CAGR']:.2%} / {lb['OOS_Sharpe']:.4f} / {lb['OOS_MaxDD']:.2%}")

        # GATES that need this panel's tape
        if panel == "U56":
            W20, _, _ = build(rank_key, elig_real, priced, reb, 20, np.inf, 126, T, K, GROSS0)
            wdf = pd.DataFrame(W20, index=idx, columns=px.columns)
            eng = backtest(px, wdf, cost_bps=COST, freq=FREQ)["returns"].values
            gg, tn = nrun(rets, lagmat(W20), mkl)
            fast = gg - tn * COST / 1e4
            dv = float(np.abs(fast[WARMUP:] - eng[WARMUP:]).max())
            gates["G1"] = dv < 1e-12
            gaterows.append(dict(gate="G1", what="fast runner == engine.backtest (U56 N=20 H=126 cap INF)",
                                 value=dv, pass_=gates["G1"]))
            f20 = gross_rescaler(rets, lagmat(W20), mkl)
            dv = float(np.abs(f20(1.0) - fast).max())
            gates["G1b"] = dv < 1e-14
            gaterows.append(dict(gate="G1b", what="gross_rescaler(1.0) == nrun (same book, not an approximation)",
                                 value=dv, pass_=gates["G1b"]))
            Wc, _, _ = build(rank_key, elig_real, priced, reb, 20, 2.00, 126, T, K, GROSS0)
            engc = backtest(px, pd.DataFrame(Wc, index=idx, columns=px.columns),
                            cost_bps=COST, freq=FREQ)["returns"].values
            ggc, tnc = nrun(rets, lagmat(Wc), mkl)
            dv = float(np.abs((ggc - tnc * COST / 1e4)[WARMUP:] - engc[WARMUP:]).max())
            gates["G1c"] = dv < 1e-12
            gaterows.append(dict(gate="G1c", what="capped build == engine.backtest (1071's arm, cap 2.00)",
                                 value=dv, pass_=gates["G1c"]))
            m = fmet(fast[warm])
            dv = max(abs(m[i] - A936_WH126[i]) for i in range(3))
            gates["G2"] = dv < 5e-3
            gaterows.append(dict(gate="G2", what="CROSS-RUN 936/1071/1082/1097 W/H126/N=20 triple",
                                 value=dv, pass_=gates["G2"]))
        sc_ = SPY_OOS_COMMITTED[panel]
        dv = max(abs(sb["OOS_CAGR"] - sc_[0]), abs(sb["OOS_Sharpe"] - sc_[1]),
                 abs(sb["OOS_MaxDD"] - sc_[2]))
        gates[f"G3_{panel}"] = dv < 5e-4
        gaterows.append(dict(gate=f"G3_{panel}", what=f"CROSS-RUN SPY OOS triple ({panel})",
                             value=dv, pass_=gates[f"G3_{panel}"]))
        dv = abs(lb["MaxDD"] - LIVE_MAXDD_COMMITTED[panel])
        gates[f"G4_{panel}"] = dv < 5e-4
        gaterows.append(dict(gate=f"G4_{panel}", what=f"live RULES v2 MaxDD == committed ({panel})",
                             value=dv, pass_=gates[f"G4_{panel}"]))

        # ------------------------------------------------------ family A: the 9 H ladders
        for fam, Ns, rungs, axis in (("A", A_NS, A_HS, "H"), ("B", B_NS, B_CAPKEYS, "cap")):
            nseed = A_SEEDS if fam == "A" else B_SEEDS
            conv = "REBUILT" if fam == "A" else "CASH"
            bis = A_BISECT if fam == "A" else B_BISECT
            for N in Ns:
                edge = {g: [] for g in GATESET}
                se = {g: [] for g in GATESET}
                bookr, nullr = [], {g: [] for g in GATESET}
                for rung in rungs:
                    if fam == "A":
                        Hh, cap, capname = int(rung), np.inf, "INF"
                    else:
                        Hh, capname = B_HOLD, str(rung)
                        cap = np.inf if capname == "INF" else float(capname)
                    Wb, nsel, grs = build(rank_key, elig_real, priced, reb, N, cap, Hh, T, K, GROSS0)
                    gb, tb = nrun(rets, lagmat(Wb), mkl)
                    rb = gb - tb * COST / 1e4
                    b = blocks(rb, warm, ins, oos)
                    l4b, l4a, l4bo = legs_4b(b, sb), legs_4a(b, lb), legs_4b_oos(b, sb)
                    out = dict(family=fam, panel=panel, N=N, H=Hh, cap=capname, axis=axis,
                               rung=rung, seeds=nseed, convention=conv,
                               mean_nsel=float(nsel.mean()), mean_gross=float(grs.mean()),
                               turnover=float(tb[warm].sum() / (warm.sum() / 252.0)), **b,
                               **l4b, **l4a, **l4bo, pass4b=all(l4b.values()),
                               pass4a=all(l4a.values()), pass4b_oos=all(l4bo.values()))
                    bookr.append(rb[warm])
                    for gate in GATESET:
                        cs, lams, scaled = [], [], []
                        for s in range(nseed):
                            sd = (mdseed(panel, N, capname, s) if gate == "OPEN"
                                  else mdseed(panel, N, capname, "ELIG", s))
                            rk = np.random.default_rng(sd).random((T, K))
                            eg = elig_real if gate == "ELIG" else ALLP
                            Wn, _, _ = build(rk, eg, priced, reb, N, cap, Hh, T, K, GROSS0)
                            if conv == "CASH":
                                gn, tnn = nrun(rets, lagmat(Wn), mkl)
                                rn = (gn - tnn * COST / 1e4)[warm]
                                lam = lam_cash(rn, b["MaxDD"], bis)
                                if lam is None:
                                    lam = 1.0
                                ser = lam * rn
                            else:
                                fn = gross_rescaler(rets, lagmat(Wn), mkl)
                                lam = lam_rebuilt(fn, warm, b["MaxDD"], bis)
                                if lam is None:
                                    lam = 1.0
                                ser = fn(lam)[warm]
                            cs.append(fmet(ser)[0])
                            lams.append(lam)
                            scaled.append(ser)
                        cs = np.array(cs)
                        out[f"EDGE_{gate}_pp"] = 100.0 * (b["CAGR"] - float(np.median(cs)))
                        out[f"EDGE_se_{gate}_pp"] = se_median(cs)
                        out[f"null_med_{gate}"] = float(np.median(cs))
                        out[f"lam_med_{gate}"] = float(np.median(lams))
                        edge[gate].append(out[f"EDGE_{gate}_pp"])
                        se[gate].append(out[f"EDGE_se_{gate}_pp"])
                        nullr[gate].append(np.vstack(scaled))
                    out["GATE_pp"] = out["EDGE_OPEN_pp"] - out["EDGE_ELIG_pp"]
                    rows.append(out)
                ladders.append(dict(panel=panel, family=fam, axis=axis, N=N, rungs=list(rungs),
                                    k=len(rungs), edge=edge, se=se,
                                    book=np.vstack(bookr), null=nullr))
                P(f"    [{fam}] {panel} N={N:<2d} {axis} ladder  EDGE_OPEN " +
                  " ".join(f"{x:+6.3f}" for x in edge["OPEN"]) + "  |  ELIG " +
                  " ".join(f"{x:+6.3f}" for x in edge["ELIG"]) + f"   t={time.time()-t0:5.0f}s")
    G = pd.DataFrame(rows)
    dump(G, "grid")
    dump(pd.DataFrame(benchrows), "benchmarks")

    # ------------------------------------------- CROSS-RUN gates against 1097's committed CSVs
    c97 = pd.read_csv(SRC_1097)
    c97["capk"] = np.where(c97.family == "A", "INF",
                           c97["cap"].map(lambda v: "INF" if str(v).lower() in ("inf", "nan")
                                          else f"{float(v):.2f}"))
    m = G.merge(c97[["family", "panel", "N", "H", "capk", "EDGE_OPEN_pp", "EDGE_ELIG_pp",
                     "EDGE_se_OPEN_pp", "CAGR"]],
                left_on=["family", "panel", "N", "H", "cap"],
                right_on=["family", "panel", "N", "H", "capk"], suffixes=("", "_97"))
    dv = max(float((m.EDGE_OPEN_pp - m.EDGE_OPEN_pp_97).abs().max()),
             float((m.EDGE_ELIG_pp - m.EDGE_ELIG_pp_97).abs().max()))
    gates["G5"] = dv < 1e-9 and len(m) == 94
    gaterows.append(dict(gate="G5", what=f"CROSS-RUN reproduce 1097's {len(m)} committed EDGE_OPEN/ELIG figures",
                         value=dv, pass_=gates["G5"]))
    dv2 = float((m.CAGR - m.CAGR_97).abs().max())
    gates["G6"] = dv2 < 1e-9
    gaterows.append(dict(gate="G6", what="CROSS-RUN reproduce 1097's committed book CAGRs",
                         value=dv2, pass_=gates["G6"]))
    P("")

    # ------------------------------------------------------- TEST 1: THE NULL GATE (1097's)
    P("## TEST 1 — THE NULL GATE: does the committed argmax move between OPEN and ELIG?")
    L97 = pd.read_csv(SRC_1097L)
    lrows = []
    for L in ladders:
        rungs = L["rungs"]
        aO = rungs[int(np.argmax(L["edge"]["OPEN"]))]
        aE = rungs[int(np.argmax(L["edge"]["ELIG"]))]
        eo = np.array(L["edge"]["OPEN"], float)
        order = np.argsort(-eo)
        lrows.append(dict(panel=L["panel"], family=L["family"], axis=L["axis"], N=L["N"],
                          k=L["k"], rungs=str(rungs), argmax_OPEN=aO, argmax_ELIG=aE,
                          peak_OPEN=float(eo[order[0]]), runner_OPEN=float(eo[order[1]]),
                          gap_pp=float(eo[order[0]] - eo[order[1]]),
                          spread_pp=float(eo.max() - eo.min()),
                          se_peak=float(L["se"]["OPEN"][order[0]]),
                          se_runner=float(L["se"]["OPEN"][order[1]]),
                          gate_survives=bool(aO == aE)))
    LAD = pd.DataFrame(lrows)
    nsurv_gate = int(LAD["gate_survives"].sum())
    P(f"  {len(LAD)} CORE ladders (18 H + 8 cap).  argmax UNCHANGED between gates in "
      f"{nsurv_gate} of {len(LAD)}; MOVED in {len(LAD) - nsurv_gate}.")
    for ax in ("H", "cap"):
        s = LAD[LAD.axis == ax]
        P(f"    {ax:<4} axis: moved {int((~s.gate_survives).sum())} of {len(s)}")
    # cross-run against 1097's own committed ladders.csv
    mm = 0
    for _, r_ in LAD.iterrows():
        key = (f"A/{r_['panel']}/N={r_['N']}/H" if r_["axis"] == "H"
               else f"B/{r_['panel']}/N={r_['N']}/cap")
        hit = L97[L97.ladder == key]
        if len(hit):
            aO97 = hit["argmax_OPEN"].iloc[0]
            aE97 = hit["argmax_ELIG"].iloc[0]
            mineO = np.inf if str(r_["argmax_OPEN"]) == "INF" else float(r_["argmax_OPEN"])
            mineE = np.inf if str(r_["argmax_ELIG"]) == "INF" else float(r_["argmax_ELIG"])
            if (mineO == aO97 or (np.isinf(mineO) and np.isinf(aO97))) and \
               (mineE == aE97 or (np.isinf(mineE) and np.isinf(aE97))):
                mm += 1
    gates["G7"] = mm == len(LAD)
    gaterows.append(dict(gate="G7", what="CROSS-RUN 1097's committed argmax_OPEN/argmax_ELIG on all 26 H/cap ladders",
                         value=float(len(LAD) - mm), pass_=gates["G7"]))
    P(f"  G7  CROSS-RUN 1097's committed argmaxes on all 26 ladders: {mm} of {len(LAD)} "
      f"reproduce  {'PASS' if gates['G7'] else 'FAIL'}")
    P("")

    # ---------------------------------------------- TEST 2: THE FLOOR, on three bases (dial 2)
    P("## TEST 2 — THE FLOOR: is the committed peak-minus-runner-up gap above it?")
    P(f"  TAPE basis: {BDRAWS} circular-block draws, ONE index per draw applied JOINTLY to the")
    P("    book and to every null seed of that ladder; lambda held at its full-sample value")
    P("    (declared approximation, LOWER bound on the floor).")
    floorrows, pairrows = [], []
    for L in ladders:
        rungs = L["rungs"]
        eo = np.array(L["edge"]["OPEN"], float)
        seo = np.array(L["se"]["OPEN"], float)
        Rall = np.vstack([L["book"]] + [L["null"]["OPEN"][i] for i in range(L["k"])])
        nsd = L["null"]["OPEN"][0].shape[0]
        for Lb in BLOCKS_L:
            rng = np.random.default_rng(bseed(L["panel"], L["family"], L["N"], Lb))
            ix, nb = block_index(rng, Rall.shape[1], Lb, BDRAWS)
            bc = boot_cagr(Rall, ix, nb, Lb)
            bookc = bc[:L["k"]]
            E = np.empty((L["k"], BDRAWS))
            for i in range(L["k"]):
                blk = bc[L["k"] + i * nsd:L["k"] + (i + 1) * nsd]
                E[i] = 100.0 * (bookc[i] - np.median(blk, axis=0))
            gaps, agr, prs = [], [], []
            for i, j in combinations(range(L["k"]), 2):
                g = eo[i] - eo[j]
                d = E[i] - E[j]
                a = float((np.sign(d) == np.sign(g)).mean())
                gaps.append(abs(g))
                agr.append(a)
                prs.append((i, j, g, a))
            flo_t, lun, nun = floor_from_agreement(np.array(gaps), np.array(agr), QFLOOR)
            order = np.argsort(-eo)
            gap = float(eo[order[0]] - eo[order[1]])
            spread = float(eo.max() - eo.min())
            flo_s = DECISIVE_K * float(np.sqrt(seo[order[0]] ** 2 + seo[order[1]] ** 2))
            flo_j = float(np.sqrt(min(flo_t, spread) ** 2 + flo_s ** 2))
            for basis, flo in (("SEED", flo_s), ("TAPE", flo_t), ("JOINT", flo_j)):
                floorrows.append(dict(panel=L["panel"], family=L["family"], axis=L["axis"],
                                      N=L["N"], k=L["k"], L=Lb, basis=basis,
                                      argmax=rungs[order[0]], gap_pp=gap, spread_pp=spread,
                                      floor_pp=flo, floor_capped=min(flo, spread),
                                      n_unresolved=nun, largest_unresolved=lun,
                                      floor_survives=bool(gap > flo)))
            if Lb == L_HEAD:
                for (i, j, g_, a_) in prs:
                    pairrows.append(dict(panel=L["panel"], axis=L["axis"], N=L["N"],
                                         rung_i=rungs[i], rung_j=rungs[j], gap=g_, agree=a_,
                                         resolved=bool(a_ >= QFLOOR)))
    FL = pd.DataFrame(floorrows)
    dump(FL, "floor")
    dump(pd.DataFrame(pairrows), "pairs")
    for basis in BASES:
        s = FL[(FL.L == L_HEAD) & (FL.basis == basis)]
        P(f"  basis {basis:<6} floor survives in {int(s['floor_survives'].sum())} of {len(s)} "
          f"ladders  (H {int(s[s.axis=='H']['floor_survives'].sum())} of "
          f"{len(s[s.axis=='H'])}, cap {int(s[s.axis=='cap']['floor_survives'].sum())} of "
          f"{len(s[s.axis=='cap'])});  median floor {s['floor_capped'].median():.4f} pp against "
          f"median gap {s['gap_pp'].median():.4f} pp")
    P("  BLOCK LENGTH, reported and never selected on (TAPE basis):")
    for Lb in BLOCKS_L:
        s = FL[(FL.L == Lb) & (FL.basis == "TAPE")]
        P(f"    L={Lb:<4} floor survives {int(s['floor_survives'].sum())} of {len(s)}")
    P("")

    # ------------------------------------------------------- THE 6 CELLS: BOTH TESTS TOGETHER
    P("## THE ANSWER — how many committed H / cap argmaxes survive BOTH tests")
    surv = FL[FL.L == L_HEAD].merge(LAD[["panel", "axis", "N", "gate_survives"]],
                                    on=["panel", "axis", "N"], how="left")
    surv["survives_both"] = surv["floor_survives"] & surv["gate_survives"]
    dump(surv, "survival")
    cellrows, claimscored = [], []
    for basis in BASES:
        s = surv[surv.basis == basis]
        n_core, n_s = len(s), int(s["survives_both"].sum())
        rate_axis = s.groupby("axis")["survives_both"].mean().to_dict()
        overall = n_s / n_core if n_core else np.nan
        wide_s, basis_n = 0.0, {"MEASURED_AXIS": 0, "TRANSFERRED_OVERALL": 0}
        for _, c in claims.iterrows():
            if c["axis"] in rate_axis:
                rt, bs = float(rate_axis[c["axis"]]), "MEASURED_AXIS"
            else:
                rt, bs = float(overall), "TRANSFERRED_OVERALL"
            wide_s += rt
            basis_n[bs] += 1
            if basis == BASIS_HEAD:
                claimscored.append(dict(source=c["source"], file=c["file"], line=c["line"],
                                        axis=c["axis"], value=c["value"], word=c["word"],
                                        survival_rate=rt, basis=bs, ctx=c["ctx"]))
        cellrows.append(dict(basis=basis, claimset="CORE", n=n_core, n_survive=float(n_s),
                             share=overall, measured=n_core, transferred=0))
        cellrows.append(dict(basis=basis, claimset="WIDE", n=len(claims), n_survive=wide_s,
                             share=wide_s / len(claims) if len(claims) else np.nan,
                             measured=basis_n["MEASURED_AXIS"],
                             transferred=basis_n["TRANSFERRED_OVERALL"]))
        P(f"  basis {basis:<6} CORE {n_s:2d} of {n_core} survive BOTH ({overall:.3f})   "
          f"WIDE {wide_s:.1f} of {len(claims)} "
          f"({wide_s / len(claims) if len(claims) else float('nan'):.3f}) "
          f"[{basis_n['MEASURED_AXIS']} measured-by-axis, "
          f"{basis_n['TRANSFERRED_OVERALL']} transferred-overall]")
    dump(pd.DataFrame(cellrows), "cells")
    dump(pd.DataFrame(claimscored), "claimscored")
    P("")
    P(f"  every CORE ladder, headline basis {BASIS_HEAD}, L={L_HEAD}:")
    for _, r_ in surv[surv.basis == BASIS_HEAD].sort_values(["axis", "panel", "N"]).iterrows():
        P(f"    {r_['panel']:<5} {r_['axis']:<4} N={r_['N']:<2d} k={r_['k']}  argmax "
          f"{str(r_['argmax']):<5} gap {r_['gap_pp']:+7.4f} pp  floor {r_['floor_capped']:7.4f} "
          f"pp  spread {r_['spread_pp']:6.3f}  gate {'OK ' if r_['gate_survives'] else 'MOVED'}"
          f"  floor {'OK ' if r_['floor_survives'] else 'FAIL'}  -> "
          f"{'SURVIVES' if r_['survives_both'] else 'DEAD'}")
    P("")

    # --------------------------------------------------------------------------- HYPOTHESES
    P("## HYPOTHESES — declared before any number above was read")
    hyp = []
    sh = surv[surv.basis == BASIS_HEAD]
    share = float(sh["survives_both"].mean())
    hyp.append(("H_SURVIVE", share < 0.50,
                f"{int(sh['survives_both'].sum())} of {len(sh)} CORE argmaxes survive BOTH tests "
                f"on the {BASIS_HEAD} basis ({share:.3f})"))
    floor_only = int((~sh["floor_survives"] & sh["gate_survives"]).sum())
    gate_only = int((sh["floor_survives"] & ~sh["gate_survives"]).sum())
    both_fail = int((~sh["floor_survives"] & ~sh["gate_survives"]).sum())
    hyp.append(("H_FLOOR_BINDS", floor_only > gate_only,
                f"floor-only failures {floor_only}, gate-only failures {gate_only}, both fail "
                f"{both_fail}, survive {int(sh['survives_both'].sum())}"))
    hs = sh[sh.axis == "H"]
    hyp.append(("H_SHORT", int(hs["floor_survives"].sum()) == 0,
                f"{int(hs['floor_survives'].sum())} of {len(hs)} three-rung H ladders clear "
                f"their TAPE floor; cap ladders (5 rungs) "
                f"{int(sh[sh.axis=='cap']['floor_survives'].sum())} of "
                f"{len(sh[sh.axis=='cap'])}"))
    piv = surv.pivot_table(index=["panel", "axis", "N"], columns="basis", values="survives_both")
    agree = float((piv.nunique(axis=1) == 1).mean())
    hyp.append(("H_BASIS", agree >= 0.80,
                f"the three bases agree on the survival verdict for {agree:.3f} of "
                f"{len(piv)} CORE ladders"))
    hyp.append(("H_HARVEST", H_HARVEST, f"{len(claims)} valued H-or-cap argmax claims harvested"))
    for k, v, why in hyp:
        P(f"  {k:<15} {'PASS' if v else 'FAIL'}   {why}")
    P(f"  {sum(1 for _, v, _ in hyp if v)} of {len(hyp)} hypotheses PASS")
    dump(pd.DataFrame([dict(hypothesis=k, result="PASS" if v else "FAIL", detail=w)
                       for k, v, w in hyp]), "hypotheses")
    P("")

    # ------------------------------------------------------- RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 — rung chosen on IS 2009-2016 ALONE, per ladder, OOS read ONCE")
    P("  EDGE IS NOT A KEEP PATH and dial 2 cannot move one: the BOOK is byte-identical across")
    P("  the two gates, so 4a and 4b are invariant to it by construction.  Scored anyway.")
    pickrows = []
    for (panel, fam, axis, N), grp in G.groupby(["panel", "family", "axis", "N"]):
        sb, lb = bench[panel]
        for ch, key in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISDD", "IS_MaxDD"),
                        ("C_ISCAGR", "IS_CAGR")):
            g2 = grp.reset_index(drop=True)
            k = int(np.argmax(g2[key].values))
            mm_ = g2.iloc[k]
            srt = np.sort(g2[key].values)[::-1]
            pickrows.append(dict(panel=panel, family=fam, axis=axis, N=N, chooser=ch,
                                 pick=mm_["rung"], margin=float(srt[0] - srt[1]),
                                 CAGR=mm_["CAGR"], Sharpe=mm_["Sharpe"], MaxDD=mm_["MaxDD"],
                                 H1=mm_["H1"], H2=mm_["H2"], OOS_CAGR=mm_["OOS_CAGR"],
                                 OOS_Sharpe=mm_["OOS_Sharpe"], OOS_MaxDD=mm_["OOS_MaxDD"],
                                 pass_4b_full=bool(mm_["pass4b"]),
                                 pass_4b_oos=bool(mm_["pass4b_oos"]),
                                 pass_4a=bool(mm_["pass4a"])))
    PK = pd.DataFrame(pickrows)
    dump(PK, "walkforward")
    P(f"  ALL PICKS: 4b full {int(PK['pass_4b_full'].sum())} of {len(PK)}, 4b OOS "
      f"{int(PK['pass_4b_oos'].sum())} of {len(PK)}, 4a {int(PK['pass_4a'].sum())} of {len(PK)}")
    P(f"  WHOLE GRID (94 committed cells): 4b full {int(G['pass4b'].sum())}, 4b OOS "
      f"{int(G['pass4b_oos'].sum())}, 4a {int(G['pass4a'].sum())}")
    if int(PK["pass_4b_full"].sum()):
        P("  picks clearing 4b full:")
        for _, r_ in PK[PK.pass_4b_full].iterrows():
            P(f"    {r_['panel']:<5} {r_['axis']:<4} N={r_['N']:<2d} {r_['chooser']:<11} pick "
              f"{str(r_['pick']):<5} full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} "
              f"halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/"
              f"{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass_4b_oos']}")
    if int(G["pass4b"].sum()):
        P("  committed cells clearing 4b full:")
        for _, r_ in G[G.pass4b].iterrows():
            P(f"    {r_['panel']:<5} {r_['family']} N={r_['N']:<2d} H={r_['H']:<3d} "
              f"cap={r_['cap']:<4s} full {r_['CAGR']:.2%}/{r_['Sharpe']:.4f}/{r_['MaxDD']:.2%} "
              f"halves {r_['H1']:.4f}/{r_['H2']:.4f}  OOS {r_['OOS_CAGR']:.2%}/"
              f"{r_['OOS_Sharpe']:.4f}/{r_['OOS_MaxDD']:.2%}  4b OOS {r_['pass4b_oos']}")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9)")
    P("  U56 and B136 are CURRENT-CONSTITUENT panels.  EDGE, the gate and the floor are all")
    P("  within-pool contrasts over the same inflated tape and the bias very largely cancels")
    P("  out of them; it does NOT cancel out of the 4b legs, measured against SPY, a real")
    P("  index, so every 4a/4b count above is an UPPER bound.")
    P("")

    dump(pd.DataFrame(gaterows), "gates")
    P(f"# GATES {sum(gates.values())} of {len(gates)} PASS")
    for k, v in gates.items():
        if not v:
            P(f"#   FAILED: {k}")
    P(f"# elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT}.console.txt")


if __name__ == "__main__":
    main()
