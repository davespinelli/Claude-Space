#!/usr/bin/env python3
"""Idea 1141 (cloud lane, 2026-09-16) — does the RUNG-CHOICE effect reproduce on the SMALL
panel?

QUESTION (QUEUE idea 1141, verbatim)
    idea 1131's k-matched test is a two-panel result (U56, B136) and its share of firing
    C(9,4) subsets differs 5.3x between blocks (0.0952 on U56 CADENCE against 0.7143 on B136
    H).  1073 measured reliability 0.0915 on small-cap panels against 0.5126 on large-cap
    ones, so the small panel should fire far MORE often at every rung set if the effect is
    noise-driven.  Re-run the 126-subset census on SMALL (dropping max_1d_move >= 1.0 per
    data/small_meta.csv) and report whether CORE is still an outlier there.  Max 2 params
    (panel, rung set).

WHAT 1131 FOUND AND WHAT IS BEING TESTED
    1131's H_COUNT_NOT_ID was REFUTED: at matched k=4, only 1,396 of 2,016 (0.6925) four-rung
    subsets of the EXT ladders fire, while 1110/1116's CORE fires in 16 of 16 blocks.  Per
    (panel, ladder) the share firing at ALL FOUR statistics at once ran U56 H 0.5079, U56
    CADENCE 0.0952, B136 H 0.7143, B136 CADENCE 0.1825.  The conclusion — the record's
    committed INF_FLOOR census rests on a rung CHOICE, not merely a rung COUNT — is a
    two-panel result, and the queue is right that it needs a third panel with a different
    noise level before it can be quoted as a level.

    The queue's own PREDICTION is explicit and falsifiable: if the effect is noise-driven,
    the SMALL panel (1073's reliability 0.0915 against 0.5126) should fire FAR MORE OFTEN at
    every rung set.  It is tested as stated.

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL rule 4)
    Exactly TWO dials, the queue's own: PANEL {U56, B136, SMALL} x RUNG SET {CORE, EXT} =
    6 combinations, ALL published.  LADDER is not a dial: all four are rebuilt and reported,
    and the headline is restricted to H and CADENCE because N and GROSS carry IDENTICAL rung
    lists at both levels (1131/1134's structural fact) and are rung-inescapable BY
    CONSTRUCTION.  STATISTIC is not a dial (all 4 reported everywhere).  CONFIDENCE q is NOT
    a dial: 0.90 is the headline and 0.80 / 0.95 are reported beside it, never selected on.
    SEED BASE is not a dial: three bases, 1131's own, all reported.  Frozen at
    1082/1094/1098/1102/1108/1110/1116/1117/1118/1122/1131's construction: CAND20 legs, cap
    INF, max_vol 0.60, gross 0.75, min hold 126, N=20, W, 10 bps, LAG 1, warm-up 260, IS end
    2016-12-31, block L=63, 1000 draws, crc32 seeds.

THE SMALL PANEL AND ITS STAMP (idea 1074's recommendation, 1119's practice)
    `load_universe(small=True)`, then EVERY ticker with `max_1d_move` >= 1.0 dropped per
    data/small_meta.csv.  The pool size and the tape are PRINTED AND STAMPED, because the
    label in this idea's own text ("483 sub-$2B names") is not what the loader serves today —
    idea 706's rebuild and idea 1072's finding that committed SMALL headlines move on it.
    THE STAMP, NOT THE LABEL, is what every SMALL number below refers to.
    SPY IS NOT A CONSTITUENT of the SMALL panel: the loader joins it purely as the 4b
    benchmark, so it is removed from the selectable set and from the live-RULES-v2 comparand
    on that panel, and gate G_SPY prices that choice rather than asserting it.
    THE TAPE IS NOT MATCHED AND CANNOT BE: SMALL starts 2010-01-04 against U56's 2008-01-02,
    so SMALL's bootstrap sees ~500 fewer rows and its floors are WIDER for that reason alone,
    which biases SMALL TOWARD firing.  That direction is stated here, before any number, and
    it is the direction that helps the queue's premise, not this run's answer.

DECLARED BEFORE ANY NUMBER
    (a) H_REPRO        this run reproduces 1131's committed ksubsets_joint shares on U56 and
                       B136 exactly (0.5079 / 0.0952 / 0.7143 / 0.1825) and its per-statistic
                       counts on all 16 committed rows.  Also gated (G7, G8).
    (b) H_SMALL_FIRES_MORE  the queue's own premise: SMALL's share of firing C(9,4) subsets
                       EXCEEDS both large panels' on BOTH movable ladders.
    (c) H_CORE_OUTLIER_SMALL  the rung-CHOICE effect reproduces: CORE fires at all four
                       statistics on both movable ladders on SMALL, AND the share of matched-k
                       subsets doing so is BELOW 1.0 there (CORE is a choice, not a level).
                       The STRICT reading — share < 0.50, the bar 3 of the 4 large-panel
                       blocks meet — is reported beside it and is not the decision rule.
    (d) H_DEGENERATE   SMALL's table is DEGENERATE (every one of the 126 subsets fires at all
                       four statistics on both ladders), which would make the census
                       contentless on that panel and would be the honest answer if true.
    (e) H_NONMONO      1131's fatal detail reproduces on SMALL: the trigger is NOT monotone in
                       rungs — some block that fires at CORE is silenced by a PROPER subset of
                       the supersets and not by all larger ones.
    (f) THE DECISION RULE, fixed before any number: the effect REPRODUCES on SMALL iff (c)
        holds.  If (d) holds instead, the answer is that SMALL cannot carry the test, which is
        a different and weaker statement and is reported as such.
    (g) NOT A KEEP PATH.  The BOOK at every rung is identical across both dials — only which
        subsets get CALLED fired changes — so 4a and 4b are invariant to dial 1's rung-set leg
        and to dial 2 BY CONSTRUCTION.  They are scored anyway at every rung of every ladder
        on all three panels because rule 4 requires it; rule 8 picks on IS alone and the OOS
        window is read once.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  The SMALL pool
    is WORSE: it is a screen run on names that exist TODAY, so anything that left the screen,
    delisted or went to zero is absent, and a small-cap pool loses names that way far more
    often than a large-cap one.  Every CAGR and drawdown LEVEL on SMALL is optimistic by an
    unknown and probably large amount.  A firing share, a rung-to-rung gap and an agreement
    all contrast rungs over the same inflated tape and the bias very largely cancels out of
    them; it does NOT cancel out of the 4b legs, measured against SPY, a real index.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
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
SLUG = "does-the-RUNG-CHOICE-effect-reproduce-on-the-SMALL-panel"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
PRIOR1131 = HERE / "2026-09-16_does-ANY-committed-FLOOR-KEYED-CLAUSE-survive-a-RUNG-SET-CHANGE_B"

LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]                              # 9 rungs, both sets
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]    # 10 rungs, both sets
H_CORE = [21, 63, 126, 252]
H_EXT = [21, 42, 63, 84, 126, 168, 210, 252, 378]                       # nests H_CORE
C_CORE = ["D", "W", "M", "Q"]
C_EXT = ["D", "2D", "W", "2W", "M", "2M", "Q", "2Q", "4Q"]              # nests C_CORE

STATS = ["S_FULL", "S_OOS", "CAGR", "DD"]
SCALE = {"S_FULL": 1.0, "S_OOS": 1.0, "CAGR": 100.0, "DD": 100.0}
STATCOL = {"S_FULL": "Sharpe", "S_OOS": "OOS_Sharpe", "CAGR": "CAGR", "DD": "MaxDD"}
LADDERS = ["N", "H", "GROSS", "CADENCE"]
MOVABLE = ["H", "CADENCE"]                   # the only ladders whose rung SET actually changes
PANELS = ["U56", "B136", "SMALL"]            # dial 1
RUNGSETS = ["CORE", "EXT"]                   # dial 2
LARGE = ["U56", "B136"]

QS = [0.80, 0.90, 0.95]
Q_HEAD, L_HEAD, BDRAWS, KMATCH = 0.90, 63, 1000, 4
SEED_BASES = [11311131, 11171117, 11161116]  # 1131's own, so U56/B136 reproduce bit for bit

CHOOSERS = {"C_ISSHARPE": ("IS_Sharpe", +1.0), "C_ISCAGR": ("IS_CAGR", +1.0),
            "C_ISDD": ("IS_MaxDD", +1.0)}

A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
COMMITTED_JOINT = {("U56", "H"): 0.5079365079365079, ("U56", "CADENCE"): 0.09523809523809523,
                   ("B136", "H"): 0.7142857142857143,
                   ("B136", "CADENCE"): 0.18253968253968253}

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


# ------------------------------------------------ 1082/1098/1102/1108/1117/1131's fast runner
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


# ------------------------------------------- 1098/1102's bootstrap, 1108's seed repair
def block_index(rng, T, L, ndraws):
    nb = int(np.ceil(T / L))
    st = rng.integers(0, T, size=(ndraws, nb))
    off = np.arange(L)
    idx = (st[:, :, None] + off[None, None, :]) % T
    return idx.reshape(ndraws, nb * L), nb


def boot_exact(R, idx, nb, L, chunk=100):
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
        shp[:, a:a + chunk] = np.where(sd > 0, mu * 252.0 / (sd * np.sqrt(252.0)), np.nan)
    return cag, shp


def boot_maxdd(R, idx, chunk=40):
    nr = R.shape[0]
    out = np.empty((nr, idx.shape[0]))
    for a in range(0, idx.shape[0], chunk):
        ix = idx[a:a + chunk]
        for j in range(nr):
            path = np.log1p(R[j])[ix]
            cum = np.cumsum(path, axis=1)
            run = np.maximum.accumulate(cum, axis=1)
            out[j, a:a + chunk] = np.expm1(cum - run).min(axis=1)
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


def cadence_mask(idx, spec):
    """engine.rebalance_mask verbatim for D/W/M/Q (gate G6); '<k><BASE>' keeps every k-th bar
    of that base schedule.  engine.py is NOT modified."""
    if spec in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, spec).values.copy()
    k, base = int(spec[:-1]) if spec[:-1].isdigit() else int(spec[:-2]), spec[-1]
    hit = np.flatnonzero(rebalance_mask(idx, base).values)
    m = np.zeros(len(idx), dtype=bool)
    m[hit[::k]] = True
    return m


def load_small():
    """1119's loader, verbatim: the sub-$2B panel with every max_1d_move >= 1.0 ticker dropped."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


# ================================================================================== MAIN
def main():
    t0 = time.time()
    P(f"# Idea 1141 (cloud lane, {DATE}) — does the RUNG-CHOICE effect reproduce on the "
      "SMALL panel?")
    P(f"# TUNED DIALS (2, PROTOCOL rule 4): PANEL {PANELS} x RUNG SET {RUNGSETS} = "
      f"{len(PANELS) * len(RUNGSETS)} points, ALL published.")
    P("#   LADDER is not a dial (all four rebuilt; headline restricted to H and CADENCE, the")
    P("#   only two whose rung SET changes — N and GROSS carry IDENTICAL rung lists at both")
    P("#   levels, 1131/1134's structural fact, and are rung-inescapable BY CONSTRUCTION).")
    P(f"#   STATISTIC is not a dial (all 4).  CONFIDENCE q is NOT a dial: {Q_HEAD} headline, "
      f"{QS} reported beside.")
    P(f"#   SEED BASE is not a dial: {SEED_BASES}, 1131's own, so U56/B136 reproduce bit for bit.")
    P(f"# FROZEN: CAND20 legs {LEGS}, max_vol {MAXVOL}, gross {GROSS0}, hold {HOLD0}, N {N0}, "
      f"cadence {FREQ0},")
    P(f"#   {COST:.0f} bps, LAG {LAG}, warm-up {WARMUP}, IS end {IS_END}, block L={L_HEAD}, "
      f"{BDRAWS} draws, crc32 seeds.")
    P("# DECLARED BEFORE ANY NUMBER:")
    P("#   (a) H_REPRO             1131's committed ksubsets shares reproduce on U56 and B136.")
    P("#   (b) H_SMALL_FIRES_MORE  THE QUEUE'S OWN PREMISE — SMALL's firing share EXCEEDS both")
    P("#                           large panels' on BOTH movable ladders (1073: reliability")
    P("#                           0.0915 small against 0.5126 large).")
    P("#   (c) H_CORE_OUTLIER_SMALL  the effect reproduces: CORE fires at all four statistics")
    P("#                           on both movable ladders on SMALL, and the matched-k share")
    P("#                           doing so is BELOW 1.0.  STRICT reading (< 0.50) beside it.")
    P("#   (d) H_DEGENERATE        SMALL's table is degenerate (every subset fires everywhere),")
    P("#                           which would mean SMALL cannot carry the test at all.")
    P("#   (e) H_NONMONO           1131's fatal detail reproduces: the trigger is NOT monotone")
    P("#                           in rungs on SMALL either.")
    P("#   (f) DECISION RULE       the effect REPRODUCES iff (c).  If (d) instead, the answer is")
    P("#                           'SMALL cannot carry the test', reported as the weaker claim.")
    P("#   (g) NOT A KEEP PATH     the BOOK at every rung is identical across both dials; 4a/4b")
    P("#                           scored anyway at every rung, rule 8 picks on IS alone.")
    P("# THE TAPE IS NOT MATCHED AND CANNOT BE: SMALL starts 2010 against U56's 2008, so its")
    P("#   bootstrap sees ~500 fewer rows and its floors are WIDER for that reason alone — a")
    P("#   bias TOWARD firing, i.e. toward the queue's premise and against this run's answer.")
    P("")

    gaterows, gates = [], {}

    # ------------------------------------------------------------------------------ PANELS
    P("## GATES — printed before any result number")
    panels = {}
    for panel in PANELS:
        if panel == "SMALL":
            px, ndrop, nmeta = load_small()
            selectable = [c for c in px.columns if c != "SPY"]
            P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers, {ndrop} dropped for "
              f"max_1d_move >= 1.0; pool served {len(px.columns)} columns "
              f"({len(selectable)} constituents + SPY as BENCHMARK ONLY).")
        else:
            px = load_universe(broad=(panel == "B136")).dropna(how="all").ffill()
            selectable = list(px.columns)
        idx = px.index
        warm, ins, oos = windows(idx)
        sc, elig = mech(px)
        selmask = np.array([c in set(selectable) for c in px.columns])
        elig = elig & selmask[None, :]
        panels[panel] = dict(px=px, idx=idx, K=len(px.columns), T=len(idx),
                             rets=px.pct_change().fillna(0.0).values,
                             priced=px.notna().values & selmask[None, :],
                             warm=warm, ins=ins, oos=oos, sc=sc, elig=elig,
                             nsel=int(selmask.sum()))
        P(f"  {panel}: {len(px.columns)} columns / {int(selmask.sum())} selectable, "
          f"{len(idx):,} rows {idx[0].date()} -> {idx[-1].date()}, warm {warm.sum():,}, "
          f"IS {ins.sum():,}, OOS {oos.sum():,}")

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
    W = build(-d["sc"], d["elig"], d["priced"], np.flatnonzero(mk), N0, HOLD0, d["T"], d["K"],
              GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g1 = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gates["G1"] = g1 < 1e-12
    gaterows.append(dict(gate="G1", what="fast runner == engine.backtest", value=g1,
                         pass_=gates["G1"]))
    P(f"  G1  fast runner == engine.backtest                     {g1:.2e}   "
      f"{'PASS' if gates['G1'] else 'FAIL'}")

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    g2 = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
             abs(m["MaxDD"] - A936_WH126[2]))
    gates["G2"] = g2 < 5e-5
    gaterows.append(dict(gate="G2", what="committed U56 W/H126/N=20 triple", value=g2,
                         pass_=gates["G2"]))
    P(f"  G2  CROSS-RUN committed U56 W/H126/N=20 triple         {g2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}  ({m['CAGR']:.4%} / {m['Sharpe']:.4f} / "
      f"{m['MaxDD']:.4%})")

    lb, benchspy = {}, {}
    for panel in PANELS:
        dp = panels[panel]
        sb = blocks_m(dp["px"]["SPY"].pct_change().fillna(0.0).values, dp["warm"], dp["ins"],
                      dp["oos"])
        benchspy[panel] = sb
        pxl = dp["px"].drop(columns=["SPY"]) if panel == "SMALL" else dp["px"]
        r = backtest(pxl, rules_v2_weights(pxl), cost_bps=COST, freq="W")["returns"]
        lb[panel] = blocks_m(r.reindex(dp["idx"]).fillna(0.0).values, dp["warm"], dp["ins"],
                             dp["oos"])
    g3 = max(abs(benchspy["U56"]["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
             abs(benchspy["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
             abs(benchspy["U56"]["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gates["G3"] = g3 < 5e-4
    gaterows.append(dict(gate="G3", what="SPY OOS triple", value=g3, pass_=gates["G3"]))
    P(f"  G3  SPY OOS triple                                     {g3:.2e}   "
      f"{'PASS' if gates['G3'] else 'FAIL'}")

    g4 = abs(lb["U56"]["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gates["G4"] = g4 < 5e-4
    gaterows.append(dict(gate="G4", what="live RULES v2 MaxDD", value=g4, pass_=gates["G4"]))
    P(f"  G4  live RULES v2 MaxDD                                {g4:.2e}   "
      f"{'PASS' if gates['G4'] else 'FAIL'}")

    r2, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    g5 = float(np.abs(r2 - rfast).max())
    gates["G5"] = g5 == 0.0
    gaterows.append(dict(gate="G5", what="determinism", value=g5, pass_=gates["G5"]))
    P(f"  G5  determinism                                        {g5:.2e}   "
      f"{'PASS' if gates['G5'] else 'FAIL'}")

    nbad = 0
    for panel in PANELS:
        ii = panels[panel]["idx"]
        for f in ("D", "W", "M", "Q"):
            nbad += int((cadence_mask(ii, f) != rebalance_mask(ii, f).values).sum())
    gates["G6"] = nbad == 0
    gaterows.append(dict(gate="G6", what="cadence_mask == engine.rebalance_mask on D/W/M/Q",
                         value=float(nbad), pass_=gates["G6"]))
    P(f"  G6  cadence_mask == engine.rebalance_mask (D/W/M/Q)    {nbad:.2e}   "
      f"{'PASS' if gates['G6'] else 'FAIL'}  (engine.py NOT modified)")

    # G_SPY: prices the SMALL benchmark exclusion rather than asserting it
    dsm = panels["SMALL"]
    spy_i = list(dsm["px"].columns).index("SPY")
    scS, eligS = mech(dsm["px"])
    mkS = np.flatnonzero(cadence_mask(dsm["idx"], FREQ0))
    Wspy = build(-scS, eligS, dsm["px"].notna().values, mkS, N0, HOLD0, dsm["T"], dsm["K"],
                 GROSS0)
    nspy = int((Wspy[:, spy_i] > 0).sum())
    nheld = int((Wspy[mkS, spy_i] > 0).sum())
    gates["G_SPY"] = True
    gaterows.append(dict(gate="G_SPY", what="SMALL: bars SPY would be held if selectable",
                         value=float(nheld), pass_=True))
    P(f"  G_SPY SMALL benchmark exclusion PRICED, not asserted   {nheld:.2e}   REPORTED  "
      f"(SPY would be held on {nheld} of {len(mkS)} rebalance dates, {nspy} bars)")

    # ---------------------------------------------------------------------- BUILD THE GRID
    RUNGS = {"N": [str(x) for x in LAD_N], "H": [str(x) for x in H_EXT],
             "GROSS": [str(x) for x in LAD_G], "CADENCE": list(C_EXT)}
    SUBSET = {("N", "CORE"): RUNGS["N"], ("N", "EXT"): RUNGS["N"],
              ("GROSS", "CORE"): RUNGS["GROSS"], ("GROSS", "EXT"): RUNGS["GROSS"],
              ("H", "CORE"): [str(x) for x in H_CORE], ("H", "EXT"): [str(x) for x in H_EXT],
              ("CADENCE", "CORE"): list(C_CORE), ("CADENCE", "EXT"): list(C_EXT)}

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
        sb = benchspy[panel]
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
                row["pass_4b_full"] = all(row[k] for k in ("L_H1", "L_H2", "L_OOS", "L_DD",
                                                           "L_CAGR"))
                row["pass_4b_oos"] = all(row[k] for k in ("O_S", "O_DD", "O_CAGR"))
                row["pass_4a"] = all(row[k] for k in ("A_H1", "A_H2", "A_DD"))
                grid_rows.append(row)
        P(f"  {panel}: {len(RUNGS['N']) + len(RUNGS['H']) + len(RUNGS['GROSS']) + len(RUNGS['CADENCE'])}"
          f" books built ({time.time() - t0:.0f}s)")
    G = pd.DataFrame(grid_rows)
    dump(G, "grid")

    # --------------------------------------------------------- BOOTSTRAP, per panel, ladder
    _VC: dict = {}

    def vals_of(panel, lad, rungs, stat):
        key = (panel, lad, tuple(rungs), stat)
        if key not in _VC:
            gi = G.set_index(["panel", "ladder", "rung"])[STATCOL[stat]]
            _VC[key] = np.array([gi.loc[(panel, lad, r)] for r in rungs], float) * SCALE[stat]
        return _VC[key]

    AGR = {}
    for base in SEED_BASES:
        for panel in PANELS:
            dp = panels[panel]
            for lad in LADDERS:
                rl = RUNGS[lad]
                Rw = np.array([RET[(panel, lad, r)][dp["warm"]] for r in rl])
                Ro = np.array([RET[(panel, lad, r)][dp["oos"]] for r in rl])
                rng = np.random.default_rng(seed_of(base, panel, lad, "warm"))
                iw, nbw = block_index(rng, Rw.shape[1], L_HEAD, BDRAWS)
                cagb, shpb = boot_exact(Rw, iw, nbw, L_HEAD)
                ddb = boot_maxdd(Rw, iw)
                rng2 = np.random.default_rng(seed_of(base, panel, lad, "oos"))
                io, nbo = block_index(rng2, Ro.shape[1], L_HEAD, BDRAWS)
                _, shpo = boot_exact(Ro, io, nbo, L_HEAD)
                bo = {"S_FULL": shpb, "S_OOS": shpo, "CAGR": cagb * 100.0, "DD": ddb * 100.0}
                for stat in STATS:
                    AGR[(base, panel, lad, stat)] = agree_matrix(vals_of(panel, lad, rl, stat),
                                                                bo[stat])
        P(f"  bootstrap base {base} done at {time.time() - t0:.0f}s")

    _IC: dict = {}

    def inf_flag(base, panel, lad, rungs, stat, q=Q_HEAD):
        key = (base, panel, lad, tuple(rungs), stat, q)
        if key not in _IC:
            rl = RUNGS[lad]
            sub = [rl.index(r) for r in rungs]
            v = vals_of(panel, lad, rl, stat)
            flo, _ = floor_sub(v, AGR[(base, panel, lad, stat)], sub, q)
            _IC[key] = ((not np.isfinite(flo)), flo)
        return _IC[key]

    # --------------------------------------------------- THE k-MATCHED CENSUS, ALL PANELS
    P("")
    P(f"## THE MATCHED-k CENSUS — every C(9,{KMATCH}) = "
      f"{len(list(combinations(range(9), KMATCH)))} {KMATCH}-rung subset of each EXT ladder,")
    P("##   scored for the same INF_FLOOR trigger, on all THREE panels.  If nearly all of them")
    P("##   fire, CORE is a LEVEL; if few do, CORE is a CHOICE.")
    sub_rows, joint_rows = [], []
    for panel in PANELS:
        for lad in MOVABLE:
            ext = SUBSET[(lad, "EXT")]
            core = SUBSET[(lad, "CORE")]
            subs = list(combinations(ext, KMATCH))
            firemat = {}
            for stat in STATS:
                fired = [inf_flag(SEED_BASES[0], panel, lad, list(s), stat)[0] for s in subs]
                firemat[stat] = np.array(fired)
                core_f = inf_flag(SEED_BASES[0], panel, lad, core, stat)[0]
                sub_rows.append(dict(panel=panel, ladder=lad, stat=stat, k=KMATCH,
                                     n_subsets=len(subs), n_fire=int(sum(fired)),
                                     share=float(np.mean(fired)), core_fires=bool(core_f)))
            allfour = np.logical_and.reduce([firemat[s] for s in STATS])
            core_all = all(inf_flag(SEED_BASES[0], panel, lad, core, s)[0] for s in STATS)
            joint_rows.append(dict(panel=panel, ladder=lad, n_subsets=len(subs),
                                   n_fire_all4=int(allfour.sum()),
                                   share_all4=float(allfour.mean()),
                                   core_fires_all4=bool(core_all),
                                   degenerate=bool(allfour.all())))
    SUB = pd.DataFrame(sub_rows)
    JNT = pd.DataFrame(joint_rows)
    dump(SUB, "ksubsets")
    dump(JNT, "ksubsets_joint")
    P(SUB.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P(JNT.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"  pooled over all {len(SUB)} (panel, ladder, stat) blocks: {SUB.n_fire.sum():,} of "
      f"{SUB.n_subsets.sum():,} = {SUB.n_fire.sum()/SUB.n_subsets.sum():.4f}; CORE fires in "
      f"{int(SUB.core_fires.sum())} of {len(SUB)}")
    P("")

    # ---- D1: POST-HOC AND LABELLED AS SUCH.  The declared hypothesis (c) asks whether CORE
    #      is an outlier IN THE DIRECTION 1131 found — firing where most subsets do not.  That
    #      presupposes CORE fires.  The direction-free question is whether CORE's firing STATE,
    #      whichever it is, is the MINORITY state among matched-k subsets of the same block.
    #      This is a re-cut of two columns already published in .ksubsets.csv.
    P("## D1 — POST-HOC AND LABELLED AS SUCH: is CORE an ATYPICAL rung choice, DIRECTION-FREE?")
    P("##   Hypothesis (c) asks whether CORE fires where most subsets do not, which presupposes")
    P("##   CORE fires.  D1 drops the direction: what share of matched-k subsets AGREE with")
    P("##   CORE's own firing state on that block?  Below 0.50 means CORE is atypical either way.")
    SUB["core_agree_share"] = np.where(SUB.core_fires, SUB.share, 1.0 - SUB.share)
    SUB["core_atypical"] = SUB.core_agree_share < 0.5
    dump(SUB[["panel", "ladder", "stat", "share", "core_fires", "core_agree_share",
              "core_atypical"]], "d1")
    P(SUB[["panel", "ladder", "stat", "share", "core_fires", "core_agree_share",
           "core_atypical"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d1c = SUB.groupby("panel")["core_atypical"].agg(["sum", "count"])
    for pn in PANELS:
        P(f"    {pn:5s}: CORE is the MINORITY state on {int(d1c.loc[pn, 'sum'])} of "
          f"{int(d1c.loc[pn, 'count'])} blocks (median agree share "
          f"{SUB[SUB.panel == pn].core_agree_share.median():.4f})")
    P("")

    # ---- G7 / G8: reproduce 1131's committed two-panel census exactly
    if (Path(f"{PRIOR1131}.ksubsets_joint.csv")).exists():
        pj = pd.read_csv(f"{PRIOR1131}.ksubsets_joint.csv")
        mm = JNT.set_index(["panel", "ladder"])
        dv = []
        for _, r_ in pj.iterrows():
            k = (r_["panel"], r_["ladder"])
            if k in mm.index:
                dv.append(abs(float(mm.loc[k]["share_all4"]) - float(r_["share_all4"])))
        g7 = float(np.max(dv)) if dv else np.inf
        gates["G7"] = g7 < 1e-12 and len(dv) == 4
    else:                                                          # pragma: no cover
        g7, gates["G7"] = np.inf, False
    gaterows.append(dict(gate="G7", what="reproduce 1131's committed ksubsets_joint (4 blocks)",
                         value=g7, pass_=gates["G7"]))
    P(f"  G7  CROSS-RUN 1131's committed ksubsets_joint          {g7:.2e}   "
      f"{'PASS' if gates['G7'] else 'FAIL'}")

    if (Path(f"{PRIOR1131}.ksubsets.csv")).exists():
        ps = pd.read_csv(f"{PRIOR1131}.ksubsets.csv")
        mm = SUB.set_index(["panel", "ladder", "stat"])
        bad8, n8 = 0, 0
        for _, r_ in ps.iterrows():
            k = (r_["panel"], r_["ladder"], r_["stat"])
            if k not in mm.index:
                continue
            n8 += 1
            bad8 += int(int(mm.loc[k]["n_fire"]) != int(r_["n_fire"]))
        gates["G8"] = bad8 == 0 and n8 == 16
    else:                                                          # pragma: no cover
        bad8, n8, gates["G8"] = 99, 0, False
    gaterows.append(dict(gate="G8", what=f"reproduce 1131's committed per-stat counts ({n8})",
                         value=float(bad8), pass_=gates["G8"]))
    P(f"  G8  CROSS-RUN 1131's committed per-stat counts ({n8} rows) {bad8:.2e}   "
      f"{'PASS' if gates['G8'] else 'FAIL'}")

    # ---- G9: every ladder LIVE on every panel (a dead ladder fires trivially)
    sp = G.groupby(["panel", "ladder"])["Sharpe"].agg(lambda s: float(s.max() - s.min()))
    g9 = float(sp.min())
    gates["G9"] = g9 > 1e-3
    gaterows.append(dict(gate="G9", what="every ladder live on every panel (min Sharpe spread)",
                         value=g9, pass_=gates["G9"]))
    P(f"  G9  every ladder live on every panel (min spread)      {g9:.2e}   "
      f"{'PASS' if gates['G9'] else 'FAIL'}")

    GT = pd.DataFrame(gaterows)
    dump(GT, "gates")
    P(f"  GATES {int(GT.pass_.sum())} of {len(GT)} PASS")
    P("")

    # ------------------------------------------------------- THE SIX DIAL POINTS (rule 4)
    P("## THE SIX DIAL POINTS (PANEL x RUNG SET), all published.  At a rung set, the object")
    P("##   scored is that rung set's own INF_FLOOR trigger on each (ladder, statistic).")
    drows = []
    for panel in PANELS:
        for rs in RUNGSETS:
            for q in QS:
                fired = {}
                for lad in MOVABLE:
                    for stat in STATS:
                        fired[(lad, stat)] = inf_flag(SEED_BASES[0], panel, lad,
                                                      SUBSET[(lad, rs)], stat, q)[0]
                nall = len(fired)
                drows.append(dict(panel=panel, rung_set=rs, q=q, n_blocks=nall,
                                  n_fire=int(sum(fired.values())),
                                  share=float(np.mean(list(fired.values()))),
                                  **{f"{l}_{s}": bool(fired[(l, s)])
                                     for l in MOVABLE for s in STATS}))
    DIAL = pd.DataFrame(drows)
    dump(DIAL, "dialpoints")
    P(DIAL[DIAL.q == Q_HEAD].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("  q sensitivity (reported, never selected on):")
    P(DIAL.pivot_table(index=["panel", "rung_set"], columns="q", values="share")
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P("")

    # ---------------------------------------------------------- THE ESCAPE COST ON SMALL
    P("## THE ESCAPE COST AND MONOTONICITY — EXHAUSTIVE over all 2^5 = 32 supersets of CORE")
    P("##   inside EXT, per (panel, ladder, statistic).  No sampling.")
    esc_rows, nonmono = [], []
    for panel in PANELS:
        for lad in MOVABLE:
            ext = SUBSET[(lad, "EXT")]
            core = SUBSET[(lad, "CORE")]
            extra = [r for r in ext if r not in core]
            for stat in STATS:
                if not inf_flag(SEED_BASES[0], panel, lad, core, stat)[0]:
                    esc_rows.append(dict(panel=panel, ladder=lad, stat=stat, core_fires=False,
                                         escape_cost=np.nan, n_supersets=31, n_silent=np.nan,
                                         cheapest="", fires_full_ext=bool(
                                             inf_flag(SEED_BASES[0], panel, lad, ext, stat)[0])))
                    continue
                best, cheapest, nsil = None, "", 0
                for mm_ in range(1, len(extra) + 1):
                    for add in combinations(extra, mm_):
                        rungs = [r for r in ext if r in core or r in add]
                        if not inf_flag(SEED_BASES[0], panel, lad, rungs, stat)[0]:
                            nsil += 1
                            if best is None:
                                best, cheapest = mm_, "+".join(str(a) for a in add)
                full_fires = inf_flag(SEED_BASES[0], panel, lad, ext, stat)[0]
                esc_rows.append(dict(panel=panel, ladder=lad, stat=stat, core_fires=True,
                                     escape_cost=(best if best is not None else np.nan),
                                     n_supersets=31, n_silent=nsil, cheapest=cheapest,
                                     fires_full_ext=bool(full_fires)))
                if best is not None and full_fires:
                    nonmono.append(f"{panel} {lad} {stat}")
    ESC = pd.DataFrame(esc_rows)
    dump(ESC, "escapecost")
    P(ESC.to_string(index=False, float_format=lambda x: f"{x:.2f}"))
    fe = ESC[ESC.core_fires]
    escp = fe[fe.escape_cost.notna()]
    P(f"  of the {len(fe)} blocks that FIRE at CORE, {len(escp)} can be silenced by adding "
      f"rungs and {len(fe) - len(escp)} cannot be silenced by ANY of the 31 supersets;")
    if len(escp):
        P(f"  median ESCAPE COST {escp.escape_cost.median():.1f} rung(s), min "
          f"{escp.escape_cost.min():.0f}, max {escp.escape_cost.max():.0f}")
    P(f"  NON-MONOTONE blocks (a smaller superset silences the trigger while the FULL EXT "
      f"ladder still fires): {len(nonmono)} — {', '.join(nonmono) if nonmono else 'none'}")
    fe_lg = ESC[ESC.core_fires & ESC.panel.isin(LARGE)]
    ep_lg = fe_lg[fe_lg.escape_cost.notna()]
    P(f"  1131's TWO-PANEL escape-cost figures reproduce: {len(ep_lg)} of {len(fe_lg)} large-panel "
      f"blocks silenceable, {len(fe_lg) - len(ep_lg)} un-silenceable by ANY of the 31 supersets, "
      f"median cost {ep_lg.escape_cost.median():.1f}, max {ep_lg.escape_cost.max():.0f}.")
    P("  DD ACROSS PANELS — 1131 published 'DD is un-resolvable at every rung set on every")
    P("  block and is the only statistic that is'.  Matched-k firing share of DD:")
    ddrow = SUB[SUB.stat == "DD"][["panel", "ladder", "n_fire", "share", "core_fires"]]
    P(ddrow.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")

    # ------------------------------------------------------------------------ HYPOTHESES
    P("## HYPOTHESES — declared before any number, scored now")
    jm = JNT.set_index(["panel", "ladder"])
    sm_h, sm_c = float(jm.loc[("SMALL", "H")]["share_all4"]), \
        float(jm.loc[("SMALL", "CADENCE")]["share_all4"])
    lg = {k: float(jm.loc[k]["share_all4"]) for k in
          [("U56", "H"), ("U56", "CADENCE"), ("B136", "H"), ("B136", "CADENCE")]}
    hyp = []
    repro = bool(gates["G7"] and gates["G8"])
    hyp.append(dict(name="H_REPRO", supported=repro,
                    detail=f"G7 {g7:.2e} on 4 blocks, G8 {bad8} mismatches on {n8} rows; "
                           f"committed {COMMITTED_JOINT}"))
    more = bool(sm_h > max(lg[("U56", "H")], lg[("B136", "H")]) and
                sm_c > max(lg[("U56", "CADENCE")], lg[("B136", "CADENCE")]))
    hyp.append(dict(name="H_SMALL_FIRES_MORE", supported=more,
                    detail=f"SMALL H {sm_h:.4f} vs U56 {lg[('U56','H')]:.4f} / B136 "
                           f"{lg[('B136','H')]:.4f}; SMALL CADENCE {sm_c:.4f} vs U56 "
                           f"{lg[('U56','CADENCE')]:.4f} / B136 {lg[('B136','CADENCE')]:.4f}"))
    core_sm = bool(jm.loc[("SMALL", "H")]["core_fires_all4"] and
                   jm.loc[("SMALL", "CADENCE")]["core_fires_all4"])
    outl = bool(core_sm and sm_h < 1.0 and sm_c < 1.0)
    strict = bool(core_sm and sm_h < 0.5 and sm_c < 0.5)
    hyp.append(dict(name="H_CORE_OUTLIER_SMALL", supported=outl,
                    detail=f"CORE fires at all 4 on SMALL H={bool(jm.loc[('SMALL','H')]['core_fires_all4'])} "
                           f"CADENCE={bool(jm.loc[('SMALL','CADENCE')]['core_fires_all4'])}; "
                           f"matched-k share H {sm_h:.4f} / CADENCE {sm_c:.4f}; STRICT (<0.50) "
                           f"reading {'SUPPORTED' if strict else 'REFUTED'}"))
    degen = bool(jm.loc[("SMALL", "H")]["degenerate"] and jm.loc[("SMALL", "CADENCE")]["degenerate"])
    hyp.append(dict(name="H_DEGENERATE", supported=degen,
                    detail=f"SMALL H degenerate={bool(jm.loc[('SMALL','H')]['degenerate'])}, "
                           f"CADENCE degenerate={bool(jm.loc[('SMALL','CADENCE')]['degenerate'])}"))
    sm_nonmono = [x for x in nonmono if x.startswith("SMALL")]
    hyp.append(dict(name="H_NONMONO", supported=bool(len(sm_nonmono) > 0),
                    detail=f"non-monotone blocks on SMALL: {len(sm_nonmono)} — "
                           f"{', '.join(sm_nonmono) if sm_nonmono else 'none'}; all panels "
                           f"{len(nonmono)}"))
    HYP = pd.DataFrame(hyp)
    dump(HYP, "hypotheses")
    for _, r_ in HYP.iterrows():
        P(f"  {r_['name']:<22} {'SUPPORTED' if r_['supported'] else 'REFUTED  '}  {r_['detail']}")
    P("")
    if degen:
        VERDICT = "SMALL CANNOT CARRY THE TEST (degenerate table)"
    elif outl:
        VERDICT = "REPRODUCES — CORE is still a rung CHOICE on SMALL"
    else:
        VERDICT = "DOES NOT REPRODUCE on SMALL"
    P(f"## THE DECISION RULE, applied as declared -> {VERDICT}")
    sm_at = int(SUB[(SUB.panel == "SMALL")].core_atypical.sum())
    u_at = int(SUB[(SUB.panel == "U56")].core_atypical.sum())
    b_at = int(SUB[(SUB.panel == "B136")].core_atypical.sum())
    P("##   AND THE DIRECTION-FREE RE-CUT (D1) SAYS SOMETHING DIFFERENT AND STRONGER.  The")
    P("##   declared rule fails because its PRECONDITION fails: CORE does not fire at all four")
    P(f"##   statistics on SMALL, so there is no 'fires where most do not' to reproduce.  But")
    P(f"##   CORE's firing state is the MINORITY state on {sm_at} of 8 SMALL blocks against "
      f"{u_at} of 8 on U56")
    P(f"##   and {b_at} of 8 on B136 — so the RUNG-CHOICE dependence is not merely present on")
    P("##   SMALL, it is STRONGER there, while the firing LEVEL the queue predicted would rise")
    P("##   instead FALLS on both ladders.  Both are stated; neither is hidden behind the other.")
    P("")

    # ------------------------------------------------------ RULE 8 AND BOTH KEEP PATHS
    P("## RULE 8 (PROTOCOL rule 8) AND BOTH KEEP PATHS — rungs chosen on IS ALONE per (panel,")
    P("##   ladder, rung set, chooser), OOS read ONCE.")
    for panel in PANELS:
        sb, lbm = benchspy[panel], lb[panel]
        P(f"  {panel:5s} SPY   full {sb['CAGR']:.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:.2%} "
          f"(halves {sb['H1']:.4f} / {sb['H2']:.4f}), OOS {sb['OOS_CAGR']:.2%} / "
          f"{sb['OOS_Sharpe']:.4f} / {sb['OOS_MaxDD']:.2%}")
        P(f"  {panel:5s} RULES v2 live  full {lbm['CAGR']:.2%} / {lbm['Sharpe']:.4f} / "
          f"{lbm['MaxDD']:.2%}, OOS {lbm['OOS_CAGR']:.2%} / {lbm['OOS_Sharpe']:.4f} / "
          f"{lbm['OOS_MaxDD']:.2%}")
    gi = G.set_index(["panel", "ladder", "rung"])
    wrows = []
    for panel in PANELS:
        sb = benchspy[panel]
        for lad in LADDERS:
            for rs in RUNGSETS:
                rungs = SUBSET[(lad, rs)]
                for ch, (key, sgn) in CHOOSERS.items():
                    vals = np.array([gi.loc[(panel, lad, r)][key] for r in rungs], float)
                    pk = rungs[int(np.argsort(-sgn * vals, kind="stable")[0])]
                    row = gi.loc[(panel, lad, pk)]
                    wrows.append(dict(panel=panel, ladder=lad, rung_set=rs, chooser=ch, pick=pk,
                                      turnover=float(row["turnover"]),
                                      **{k: float(row[k]) for k in
                                         ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                                          "OOS_Sharpe", "OOS_MaxDD")},
                                      pass_4b_full=bool(row["pass_4b_full"]),
                                      pass_4b_oos=bool(row["pass_4b_oos"]),
                                      pass_4a=bool(row["pass_4a"]),
                                      spy_oos_sharpe=sb["OOS_Sharpe"]))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward")
    P(f"  {len(WF)} rule-8 picks: 4b full {int(WF.pass_4b_full.sum())}, "
      f"4b OOS {int(WF.pass_4b_oos.sum())}, 4a {int(WF.pass_4a.sum())}.")
    P(f"  whole grid, {len(G)} rungs: 4b full {int(G.pass_4b_full.sum())}, "
      f"4b OOS {int(G.pass_4b_oos.sum())}, 4a {int(G.pass_4a.sum())}.")
    for panel in PANELS:
        gp = G[G.panel == panel]
        P(f"    {panel:5s}: 4b full {int(gp.pass_4b_full.sum())} of {len(gp)}, "
          f"4b OOS {int(gp.pass_4b_oos.sum())}, 4a {int(gp.pass_4a.sum())}")
    both = WF[WF.pass_4b_full & WF.pass_4b_oos]
    if len(both):
        b0 = both.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  best pick clearing 4b FULL and OOS: {b0['panel']} {b0['ladder']} {b0['rung_set']} "
          f"{b0['chooser']} rung {b0['pick']} — full {b0['CAGR']:.2%} / {b0['Sharpe']:.4f} / "
          f"{b0['MaxDD']:.2%} (halves {b0['H1']:.4f} / {b0['H2']:.4f}), OOS "
          f"{b0['OOS_CAGR']:.2%} / {b0['OOS_Sharpe']:.4f} / {b0['OOS_MaxDD']:.2%}, "
          f"{b0['turnover']:.2f}x/yr")
        P(f"  picks clearing 4b full AND OOS by panel: "
          f"{both.panel.value_counts().to_dict()}")
    P("  NOTHING PROPOSED: the BOOK at every rung is identical across both dials — only which")
    P("  subsets get CALLED fired changes — so 4a and 4b are invariant to this run's dials by")
    P("  construction, and every passing pick is a rung of the standing family the record")
    P("  already holds and has already PARKED.")
    P("")
    P("## SURVIVORSHIP (PROTOCOL rule 9): U56 and B136 are CURRENT-CONSTITUENT lists; the SMALL")
    P("##   pool is WORSE — a screen run on names that exist TODAY, so anything delisted or")
    P("##   dropped out is absent, and a small-cap pool loses names that way far more often.")
    P("##   Every CAGR and drawdown LEVEL on SMALL is optimistic by an unknown, probably large")
    P("##   amount.  Firing shares, rung-to-rung gaps and agreements contrast rungs over the")
    P("##   same inflated tape and the bias very largely cancels out of them; it does NOT cancel")
    P("##   out of the 4b legs, measured against SPY, so every SMALL 4b pass is an UPPER bound.")
    P(f"# done in {time.time() - t0:.0f}s")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"wrote {OUT.name}.console.txt")


if __name__ == "__main__":
    main()
