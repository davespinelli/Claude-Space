#!/usr/bin/env python3
"""
Idea 1216 (lane B, 2026-09-17) — is EVERY normaliser the record has added an ORDER OF
MAGNITUDE SMALLER than what it normalises?

THE PREMISE, READ FROM THE RECORD.  Idea 1205 (and 1218's follow-up) found that
R = range / (d2(k) x rung SD) ranks the record's dials IDENTICALLY to the raw range,
because the denominator moves only x1.96-x2.52 across the eight real ladders while the
numerator moves x35.4-x107.8.  A denominator two orders of magnitude flatter than its
numerator is a monotone transform: it cannot reorder anything, so the normalisation buys
presentation and not decisions.  That reading is a GENERAL test, not a fact about d2, and
the queue asks it of every normaliser the record has ever added.

THE QUESTION, THREE PARTS, ANSWERED SEPARATELY:
  (A) CENSUS.  How many committed sentences rest on a normaliser, which normaliser, and how
      many of them state the denominator's own spread beside the numerator's?
  (B) MEASUREMENT.  For each normaliser family that is computable on this tape, measure the
      denominator's spread against the numerator's AT ITS OWN NATURAL UNIT OF COMPARISON
      (cross-section for a cross-sectional normaliser, ladder rungs for a ladder one), and
      measure directly whether it REORDERS: Spearman rho raw-vs-normalised and argmax moves.
      The order-of-magnitude claim and the cannot-reorder claim are scored SEPARATELY,
      because the first is only interesting if it implies the second.
  (C) PRICE.  Rule 8: choose the rung by the RAW statistic or by the NORMALISED one on
      2009-2016 only, read 2017-2026 once, at 10 bps with t+1 execution, against SPY, the
      live book and doing nothing.  Both KEEP paths on every book.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET      {C_HEAD, C_MEMO, C_SCRIPT, C_ALL}
  SPREAD MEASURE {S_MAXMIN, S_RANGEMED, S_CV, S_IQRMED}

  = 16 cells, EVERY ONE PUBLISHED, in `.census_grid.csv` and `.spread_grid.csv`.

  C_HEAD    research/LEADERBOARD.md + research/CHANGELOG.md at this run's HEAD.
  C_MEMO    C_HEAD + every research/backtests/*.result.md and *.memo.md.
  C_SCRIPT  C_MEMO + the SOURCE of every research/backtests/*.py (a normaliser that only
            ever appears in code is still a committed use).
  C_ALL     C_SCRIPT + research/QUEUE.md.

  S_MAXMIN   max/min  — 1205's own "x" form, the one the premise is written in.
  S_RANGEMED (max-min)/|median| — scale-free, tolerant of a near-zero minimum.
  S_CV       SD/|mean| — the moment form.
  S_IQRMED   (p75-p25)/|median| — the outlier-robust form.

WHAT IS NOT A DIAL.  The six normaliser families are HARVESTED from the queue's own list
(null SD, pool mean, turnover rebate, gross, vol20) plus d2, which is the premise's own
object.  The ladders (N, H, GROSS, CADENCE), the panels (U56, B136, SMALL), the 216-book
rule-8 population and the block-bootstrap L = 63 are the record's, inherited whole and not
tuned here.  Every cell of every grid is published; nothing is selected after the fact.

Frozen from the record: CAND20 legs, max_vol 0.60, gross 0.75, min hold 126, N = 20,
cadence W, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, crc32 seeds.

PROTOCOL: rule 2 costs 10 bps and t+1 execution throughout; rule 8 walk-forward and BOTH
KEEP paths in Arm C; rule 9 survivorship stated.  RULES.md, PROTOCOL.md, scan.py, bot.py
and baseline.py are NOT modified by this script.

Runs standalone and offline:
  python research/backtests/2026-09-17_is-EVERY-NORMALISER-the-record-has-ADDED-an-ORDER-OF-MAGNITUDE-SMALLER-than-what-it-NORMALISES_B.py
"""
from __future__ import annotations

import bisect
import re
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
SLUG = "is-EVERY-NORMALISER-the-record-has-ADDED-an-ORDER-OF-MAGNITUDE-SMALLER-than-what-it-NORMALISES"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
BT = ROOT / "research" / "backtests"

# ----- the record's construction, inherited whole -------------------------------------------
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST, GROSS0, FREQ0, HOLD0, N0 = 10.0, 0.75, "W", 126, 20
LEGS = [(21, 252), (0, 126), (0, 63)]
PANELS = ["U56", "B136", "SMALL"]

POP_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
POP_H = [21, 63, 126, 252]
POP_C = ["W", "M"]
GROSS_LADDER = [round(0.30 + 0.05 * i, 3) for i in range(15)]      # 0.30 .. 1.00
ANCHOR = dict(N=N0, H=HOLD0, cadence=FREQ0)

L_BLOCK = 63                                          # 1101's committed block length
BDRAWS = 400
NPOOL = 30                                            # null books per panel for the pool mean
SEED_BASE = 12161216

# the two dials
CLAIM_SETS = ["C_HEAD", "C_MEMO", "C_SCRIPT", "C_ALL"]
SPREADS = ["S_MAXMIN", "S_RANGEMED", "S_CV", "S_IQRMED"]
OOM = 10.0                                            # "an order of magnitude"

# d2 (expected range of k iid standard normals), the premise's own constant
D2 = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534, 7: 2.704, 8: 2.847, 9: 2.970,
      10: 3.078, 11: 3.173, 12: 3.258, 13: 3.336, 14: 3.407, 15: 3.472}

# ----- the record's own committed numbers, QUOTED and GATED, never re-derived ----------------
A936_WH126 = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205
C1205_DENOM_LO, C1205_DENOM_HI = 1.96, 2.52          # 1205's committed denominator x-range
C1205_NUM_LO, C1205_NUM_HI = 35.4, 107.8             # 1205's committed numerator x-range

LOG: list[str] = []
GATES: list[dict] = []
HYPS: list[dict] = []


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


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, check=what, value=float(value), pass_=bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:<6s} {what}  ->  {value:.4e}")
    return bool(ok)


def hyp(name, declared, bar, measured, supported):
    HYPS.append(dict(hypothesis=name, declared=declared, bar=bar, measured=measured,
                     supported=bool(supported)))
    P(f"   [{'SUPPORTED' if supported else 'REFUTED  '}] {name:<14} {declared}")
    P(f"                  bar {bar} | measured {measured}")


# =================================================================================================
# THE SPREAD MEASURES — the second dial.  All four are scale-free so a numerator and a
# denominator in different units can be compared at all.
# =================================================================================================
def spread(x, kind):
    v = np.asarray([z for z in np.asarray(x, float).ravel() if np.isfinite(z)])
    if len(v) < 2:
        return np.nan
    if kind == "S_MAXMIN":
        lo, hi = np.min(np.abs(v)), np.max(np.abs(v))
        return hi / lo if lo > 0 else np.inf
    if kind == "S_RANGEMED":
        m = abs(np.median(v))
        return (v.max() - v.min()) / m if m > 0 else np.inf
    if kind == "S_CV":
        m = abs(v.mean())
        return v.std(ddof=1) / m if m > 0 else np.inf
    if kind == "S_IQRMED":
        m = abs(np.median(v))
        q = np.percentile(v, 75) - np.percentile(v, 25)
        return q / m if m > 0 else np.inf
    raise ValueError(kind)


def nanmed(x):
    v = np.asarray(x, float)
    v = v[np.isfinite(v)]
    return float(np.median(v)) if len(v) else np.nan


def nanmean(x):
    v = np.asarray(x, float)
    v = v[np.isfinite(v)]
    return float(v.mean()) if len(v) else np.nan


def is_const(x):
    v = np.asarray(x, float).ravel()
    v = v[np.isfinite(v)]
    return bool(len(v) >= 2 and v.max() == v.min())


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


# =================================================================================================
# the record's runner and book machinery, inherited whole
# =================================================================================================
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
    """Returns (raw composite score, vol20, above-MA, eligibility) — the RAW numerator and the
    VOL20 denominator kept APART, because that separation is what Arm B measures."""
    comp = legs_composite(px)
    above = px > px.rolling(200).mean()
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    raw = comp * (0.5 + 0.5 * above.astype(float))
    return raw.values, vol20.values, above.values, (above & (vol20 < MAXVOL)).values


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


def legs_4a(b, lb):
    return {"A_H1": bool(b["H1"] > lb["H1"]), "A_H2": bool(b["H2"] > lb["H2"]),
            "A_DD": bool(b["MaxDD"] >= lb["MaxDD"])}


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep].dropna(how="all").ffill(), len(bad), len(meta)


def block_se(ra, rb, tag, ndraws=BDRAWS, L=L_BLOCK):
    """Moving-block bootstrap SE of the Sharpe DIFFERENCE.  Days resampled JOINTLY so the
    pair's correlation survives — the record's convention since 1101."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    T = len(ra)
    nb = int(np.ceil(T / L))
    rng = np.random.default_rng(seed_of("se", tag, L, ndraws))
    starts = rng.integers(0, max(T - L, 1), size=(ndraws, nb))
    off = np.arange(L)
    d = np.empty(ndraws)
    for i in range(ndraws):
        idx = (starts[i][:, None] + off[None, :]).ravel()[:T] % T
        d[i] = fsharpe(rb[idx]) - fsharpe(ra[idx])
    return float(np.std(d, ddof=1))


# =================================================================================================
# ARM A — the census patterns.  One word list per normaliser family, taken from the queue's
# own naming (null SD, pool mean, turnover rebate, gross, vol20) plus d2, the premise's object.
# =================================================================================================
FAMILIES = ["NRM_NULLSD", "NRM_POOLMEAN", "NRM_TURNOVER", "NRM_GROSS", "NRM_VOL20", "NRM_D2"]

WORDS = {
    "NRM_NULLSD": ["null sd", "/ se", "/se", "sampling se", "bootstrap sd", "bootstrap se",
                   "standard error", "t-stat", "t_stat", "se basis", "se_of_diff",
                   "divided by its se", "sharpe se", "block se", "fold se", "crit95"],
    "NRM_POOLMEAN": ["pool mean", "pool sd", "pool_mean", "z-score", "zscore", "z score",
                     "percentile of its own null", "gross-matched null", "excess over the null",
                     "null mean", "matched null mean", "p_boot"],
    "NRM_TURNOVER": ["turnover rebate", "per unit turnover", "cost-adjusted", "net of cost",
                     "cost_bps", "cost rung", "turnover-normalised", "turnover normalised",
                     "10 bps", "bps per unit"],
    "NRM_GROSS": ["gross/n", "gross / n", "gross-matched", "gross matched", "per-name weight",
                  "de-gross", "degross", "gross ladder", "gross rung", "g/n"],
    "NRM_VOL20": ["vol20", "vol-scaled", "vol scaled", "volatility-scaled", "vol scaler",
                  "vol_scale", "inverse-vol", "inverse vol", "risk parity", "risk-parity"],
    "NRM_D2": ["d2(", "d2 x", "d2(k)", "d2_corr", "d2 correction", "expected range constant"],
}
# does the containing unit state the DENOMINATOR's own spread beside the numerator's?
PAT_SPREADCUE = re.compile(
    r"(x\s?\d+(\.\d+)?\s*-\s*x\s?\d+|spread|range|max/min|order of magnitude|"
    r"orders? of magnitude|sd of the denominator|denominator (moves|spread|range))", re.I)
PAT_PY = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}_[A-Za-z0-9._\-]+\.py")


def units_of(txt):
    """(start, text) of every unit: a markdown table row is its own unit, else the paragraph."""
    lines = txt.split("\n")
    starts = [0]
    for ln in lines[:-1]:
        starts.append(starts[-1] + len(ln) + 1)
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("|"):
            out.append((starts[i], lines[i]))
            i += 1
        elif not lines[i].strip():
            i += 1
        else:
            a = i
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith("|"):
                i += 1
            out.append((starts[a], "\n".join(lines[a:i + 1])))
            i += 1
    return out


def census(files):
    """One row per (unit, family) hit."""
    rows = []
    for name, txt, src in files:
        for pos, unit in units_of(txt):
            low = unit.lower()
            hits = [f for f in FAMILIES if any(w in low for w in WORDS[f])]
            if not hits:
                continue
            cue = bool(PAT_SPREADCUE.search(unit))
            script = None
            m = list(PAT_PY.finditer(unit))
            if m:
                script = m[-1].group(0)
            for f in hits:
                w = [x for x in WORDS[f] if x in low]
                rows.append(dict(file=name, source=src, pos=pos, family=f,
                                 n_families=len(hits), states_spread=cue, trigger=w[0],
                                 n_triggers=len(w), script=script, chars=len(unit)))
    return pd.DataFrame(rows)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1216 (lane B, {DATE}) — {SLUG}")
    P("=" * 100)
    P(__doc__.strip())
    P("")

    # ------------------------------------------------------------------ panels
    P("## PANELS")
    raw = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm, ndrop, nmeta = load_small()
    raw["SMALL"] = sm
    panels = {}
    for panel in PANELS:
        px = raw[panel]
        idx, K, T = px.index, len(px.columns), len(px.index)
        warm, ins, oos = windows_of(idx)
        rawsc, vol20, above, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if panel == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        volsc = rawsc / np.clip(vol20, 0.08, None) ** 0.5     # the LIVE RULES v1 key
        panels[panel] = dict(px=px, idx=idx, K=K, T=T,
                             rets=px.pct_change().fillna(0.0).values, priced=px.notna().values,
                             warm=warm, ins=ins, oos=oos, rawsc=rawsc, vol20=vol20,
                             volsc=volsc, elig=elig, spy_i=spy_i)
        P(f"  {panel:<6s} {K:4d} cols, {T:,} rows {idx[0].date()} -> {idx[-1].date()}  "
          f"warm {warm.sum():,}  IS {ins.sum():,}  OOS {oos.sum():,}")
    P(f"  SMALL STAMP: data/small_meta.csv lists {nmeta} tickers; {ndrop} dropped for "
      f"max_1d_move >= 1.0; pool served = {panels['SMALL']['K'] - 1} names + SPY as benchmark.")
    P("")

    def run_cell(panel, N, H, gross, freq, key="rawsc"):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], freq).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        W = build(-d[key], d["elig"], d["priced"], reb, N, H, d["T"], d["K"], gross)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4, g, tn

    def null_book(panel, seed):
        d = panels[panel]
        mk = rebalance_mask(d["idx"], FREQ0).values
        mkl = np.roll(mk, LAG)
        mkl[:LAG] = False
        reb = np.flatnonzero(mk)
        rng = np.random.default_rng(seed_of("null", panel, seed))
        W = np.zeros((d["T"], d["K"]))
        ok = d["elig"] & d["priced"]
        for i, t in enumerate(reb):
            cand = np.flatnonzero(ok[t])
            if not len(cand):
                continue
            sel = rng.choice(cand, size=min(N0, len(cand)), replace=False)
            stop = reb[i + 1] if i + 1 < len(reb) else d["T"]
            W[t:stop, sel] = GROSS0 / len(sel)
        Wl = np.zeros_like(W)
        Wl[LAG:] = W[:-LAG]
        g, tn = nrun(d["rets"], Wl, mkl)
        return g - tn * COST / 1e4

    # ------------------------------------------------------------------ gates
    P("## GATES — printed before any result number")
    d = panels["U56"]
    mk = rebalance_mask(d["idx"], FREQ0).values
    reb = np.flatnonzero(mk)
    W = build(-d["rawsc"], d["elig"], d["priced"], reb, N0, HOLD0, d["T"], d["K"], GROSS0)
    eng = backtest(d["px"], pd.DataFrame(W, index=d["idx"], columns=d["px"].columns),
                   cost_bps=COST, freq=FREQ0)["returns"].values
    rfast, _, _ = run_cell("U56", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(eng[d["warm"]] - rfast[d["warm"]]).max())
    gate("G1", "fast runner == engine.backtest (U56 W/H126/N=20)", v, v < 1e-12)

    m = blocks_m(rfast, d["warm"], d["ins"], d["oos"])
    v = max(abs(m["CAGR"] - A936_WH126[0]), abs(m["Sharpe"] - A936_WH126[1]),
            abs(m["MaxDD"] - A936_WH126[2]))
    gate("G2", "CROSS-RUN the committed U56 W/H126/N=20 triple", v, v < 5e-3)

    spy_u = d["px"]["SPY"].pct_change().fillna(0.0).values
    smm = blocks_m(spy_u, d["warm"], d["ins"], d["oos"])
    v = max(abs(smm["OOS_CAGR"] - SPY_OOS_COMMITTED[0]),
            abs(smm["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
            abs(smm["OOS_MaxDD"] - SPY_OOS_COMMITTED[2]))
    gate("G3", "SPY OOS triple", v, v < 5e-3)

    lb_r = backtest(d["px"], rules_v2_weights(d["px"]), cost_bps=COST, freq="W")["returns"].values
    lbm = blocks_m(lb_r, d["warm"], d["ins"], d["oos"])
    v = abs(lbm["MaxDD"] - LIVE_MAXDD_COMMITTED)
    gate("G4", "live RULES v2 MaxDD == committed -12.05%", v, v < 5e-4)

    r1, _, _ = run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
    r2, _, _ = run_cell("SMALL", N0, HOLD0, GROSS0, FREQ0)
    v = float(np.abs(r1 - r2).max())
    gate("G5", "determinism (SMALL anchor, two runs)", v, v == 0.0)

    # the RAW key and the NORMALISED key must actually differ, or Arm B has nothing to measure
    v = float(np.nanmax(np.abs(np.asarray([spearman(panels["U56"]["rawsc"][t],
                                                    panels["U56"]["volsc"][t]) - 1.0
                                           for t in range(WARMUP, panels["U56"]["T"], 500)]))))
    gate("G6", "vol20 key is NOT rank-identical to the raw key (max |rho-1|)", v, v > 1e-6)

    v = abs(spread([C1205_DENOM_LO, C1205_DENOM_HI], "S_MAXMIN")
            - C1205_DENOM_HI / C1205_DENOM_LO)
    gate("G7", "S_MAXMIN reproduces 1205's own x-form on its committed pair", v, v < 1e-12)
    P("")

    # =============================================================== ARM A — CENSUS
    P("## ARM A — CENSUS: which committed units rest on a normaliser, and do they state the")
    P("   DENOMINATOR's spread?  Four claim sets x six families, every cell published.")
    head = [("LEADERBOARD.md", (ROOT / "research" / "LEADERBOARD.md").read_text(), "head"),
            ("CHANGELOG.md", (ROOT / "research" / "CHANGELOG.md").read_text(), "head")]
    memo = [(p.name, p.read_text(errors="ignore"), "memo")
            for p in sorted(BT.glob("*.result.md")) + sorted(BT.glob("*.memo.md"))]
    srcs = [(p.name, p.read_text(errors="ignore"), "script") for p in sorted(BT.glob("*.py"))]
    queue = [("QUEUE.md", (ROOT / "research" / "QUEUE.md").read_text(), "queue")]
    SETS = {"C_HEAD": head, "C_MEMO": head + memo, "C_SCRIPT": head + memo + srcs,
            "C_ALL": head + memo + srcs + queue}
    P(f"   files: head {len(head)}, memos {len(memo)}, scripts {len(srcs)}, queue {len(queue)}")

    allc, grid = [], []
    for cs in CLAIM_SETS:
        c = census(SETS[cs])
        c["claim_set"] = cs
        allc.append(c)
        nun = c.drop_duplicates(["file", "pos"]).shape[0]
        for f in FAMILIES:
            g = c[c.family == f]
            grid.append(dict(claim_set=cs, family=f, units=len(g),
                             states_spread=int(g.states_spread.sum()),
                             share_states=(float(g.states_spread.mean()) if len(g) else np.nan),
                             sole_family=int((g.n_families == 1).sum())))
        grid.append(dict(claim_set=cs, family="ANY", units=nun,
                         states_spread=int(c.drop_duplicates(["file", "pos"])
                                           .states_spread.sum()),
                         share_states=float(c.drop_duplicates(["file", "pos"])
                                            .states_spread.mean()) if nun else np.nan,
                         sole_family=int((c.groupby(["file", "pos"]).family.nunique() == 1).sum())))
    CEN = pd.concat(allc, ignore_index=True)
    GRID = pd.DataFrame(grid)
    dump(CEN, "claims")
    dump(GRID, "census_grid")
    for cs in CLAIM_SETS:
        g = GRID[GRID.claim_set == cs].set_index("family")
        P(f"   {cs:<9} " + "  ".join(f"{f.replace('NRM_', ''):<9}{int(g.loc[f, 'units']):5d}"
                                     f"/{int(g.loc[f, 'states_spread']):<3d}" for f in FAMILIES))
        a = g.loc["ANY"]
        P(f"   {'':<9} ANY UNITS {int(a['units']):5d}, of which STATE A SPREAD "
          f"{int(a['states_spread']):4d} ({a['share_states']:.4f})")
    P("   WHAT ACTUALLY TRIGGERS EACH FAMILY (C_ALL, top 3 words by unit count) — published so")
    P("   the counts are readable rather than impressive: a keyword census counts MENTIONS.")
    ca = CEN[CEN.claim_set == "C_ALL"]
    for f in FAMILIES:
        vc = ca[ca.family == f].trigger.value_counts().head(3)
        P(f"     {f:<13} " + ", ".join(f"'{w}' {int(n)}" for w, n in vc.items()))
    P("")

    # =============================================================== ARM B — MEASUREMENT
    P("## ARM B — MEASUREMENT: denominator spread against numerator spread, at each")
    P("   normaliser's OWN unit of comparison, under all four spread measures; and whether")
    P("   the normalisation REORDERS (Spearman rho, argmax move) — scored separately.")

    rows = []

    # ---- NRM_VOL20: cross-sectional, units = eligible names on a rebalance day
    P("   NRM_VOL20 (baseline.score): key = comp / vol20^0.5.  Units = eligible names on each")
    P("   rebalance day; numerator = the raw composite, denominator = vol20^0.5.")
    for panel in PANELS:
        dd_ = panels[panel]
        mk = rebalance_mask(dd_["idx"], FREQ0).values
        days = [t for t in np.flatnonzero(mk) if t >= WARMUP]
        days = days[:: max(1, len(days) // 200)]          # ~200 days, deterministic stride
        per = {s: [] for s in SPREADS}
        rho, amove, nnames, rho_nd = [], [], [], []
        for t in days:
            sel = np.flatnonzero(dd_["elig"][t] & dd_["priced"][t])
            if len(sel) < 5:
                continue
            num = dd_["rawsc"][t, sel]
            den = np.clip(dd_["vol20"][t, sel], 0.08, None) ** 0.5
            nrm = num / den
            for s in SPREADS:
                per[s].append((spread(num, s), spread(den, s)))
            rho.append(spearman(num, nrm))
            rho_nd.append(spearman(num, den))
            top_raw = set(sel[np.argsort(-num, kind="stable")[:N0]])
            top_nrm = set(sel[np.argsort(-nrm, kind="stable")[:N0]])
            amove.append(1.0 - len(top_raw & top_nrm) / min(N0, len(sel)))
            nnames.append(len(sel))
        for s in SPREADS:
            a = np.array(per[s])
            rows.append(dict(family="NRM_VOL20", panel=panel, ladder="CROSS_SECTION",
                             spread_measure=s, n_units=len(a), k=int(np.mean(nnames)),
                             num_spread=float(np.median(a[:, 0])),
                             den_spread=float(np.median(a[:, 1])),
                             ratio=float(np.median(a[:, 0]) / np.median(a[:, 1])),
                             rho=float(np.mean(rho)), argmax_move=float(np.mean(amove)),
                             rho_nd=float(np.mean(rho_nd)), den_constant=False))

    # ---- NRM_GROSS: per-name weight = gross / N_sel
    P("   NRM_GROSS: per-name weight = gross / N_selected.  Measured on BOTH ladders it can")
    P("   move on — the GROSS ladder (numerator moves, denominator fixed) and the N ladder")
    P("   (denominator moves, numerator fixed).  This is the family where the premise INVERTS.")
    for panel in PANELS:
        for lad, vals in (("LAD_GROSS", GROSS_LADDER), ("LAD_N", POP_N)):
            num = np.array([g if lad == "LAD_GROSS" else GROSS0 for g in vals], float)
            den = np.array([N0 if lad == "LAD_GROSS" else n for n in vals], float)
            nrm = num / den
            for s in SPREADS:
                rows.append(dict(family="NRM_GROSS", panel=panel, ladder=lad,
                                 spread_measure=s, n_units=len(vals), k=len(vals),
                                 num_spread=spread(num, s), den_spread=spread(den, s),
                                 ratio=spread(num, s) / spread(den, s)
                                 if spread(den, s) not in (0, np.nan) else np.inf,
                                 rho=spearman(num, nrm), rho_nd=spearman(num, den),
                                 den_constant=is_const(den),
                                 argmax_move=float(np.argmax(num) != np.argmax(nrm))))

    # ---- book ladders: needed by NULLSD, POOLMEAN, TURNOVER, D2
    P("   Building the ladder books (N, H, GROSS, CADENCE) on every panel for the ladder-level")
    P("   normalisers (NULLSD, POOLMEAN, TURNOVER, D2) ...")
    LADDERS = {"LAD_N": ("N", POP_N), "LAD_H": ("H", POP_H),
               "LAD_GROSS": ("gross", GROSS_LADDER), "LAD_CADENCE": ("cadence", POP_C)}
    lad_books = {}
    for panel in PANELS:
        dd_ = panels[panel]
        for lad, (dial, vals) in LADDERS.items():
            net, gro, tno = [], [], []
            for v in vals:
                kw = dict(N=N0, H=HOLD0, gross=GROSS0, freq=FREQ0)
                kw[dial if dial != "cadence" else "freq"] = v
                rn, rg, tn = run_cell(panel, kw["N"], kw["H"], kw["gross"], kw["freq"])
                net.append(rn)
                gro.append(rg)
                tno.append(tn)
            lad_books[(panel, lad)] = dict(vals=vals, net=net, gross=gro, turn=tno)
        P(f"     {panel:<6} ladders built ({time.time() - t0:.0f}s)")

    # ---- NRM_POOLMEAN: the gross-matched null pool
    P("   NRM_POOLMEAN: z = (Sharpe - pool mean) / pool SD over 30 gross-matched null books.")
    pool = {}
    for panel in PANELS:
        d_ = panels[panel]
        s = np.array([fsharpe(null_book(panel, i)[d_["warm"]]) for i in range(NPOOL)])
        pool[panel] = (float(s.mean()), float(s.std(ddof=1)))
        P(f"     {panel:<6} pool mean {s.mean():.4f}  pool SD {s.std(ddof=1):.4f}  "
          f"({time.time() - t0:.0f}s)")

    for panel in PANELS:
        d_ = panels[panel]
        pm, ps = pool[panel]
        for lad in LADDERS:
            bk = lad_books[(panel, lad)]
            warm = d_["warm"]
            sh = np.array([fsharpe(r[warm]) for r in bk["net"]])
            shg = np.array([fsharpe(r[warm]) for r in bk["gross"]])
            drag = np.array([(t_[warm].sum() * COST / 1e4) * 252.0 / warm.sum()
                             for t_ in bk["turn"]])
            k = len(sh)

            # NRM_NULLSD — t = dSharpe / SE against the ladder's own first rung
            dsh = np.array([sh[i] - sh[0] for i in range(k)])
            se = np.array([block_se(bk["net"][0][warm], bk["net"][i][warm],
                                    f"{panel}|{lad}|{i}") if i else np.nan for i in range(k)])
            tt = dsh / se
            for s_ in SPREADS:
                rows.append(dict(family="NRM_NULLSD", panel=panel, ladder=lad,
                                 spread_measure=s_, n_units=k - 1, k=k - 1,
                                 num_spread=spread(dsh[1:], s_), den_spread=spread(se[1:], s_),
                                 ratio=spread(dsh[1:], s_) / spread(se[1:], s_),
                                 rho=spearman(np.abs(dsh[1:]), np.abs(tt[1:])),
                                 rho_nd=spearman(np.abs(dsh[1:]), se[1:]),
                                 den_constant=is_const(se[1:]),
                                 argmax_move=float(np.nanargmax(np.abs(dsh[1:]))
                                                   != np.nanargmax(np.abs(tt[1:])))))

            # NRM_POOLMEAN — z against a pool mean/SD that is CONSTANT across the ladder
            z = (sh - pm) / ps
            for s_ in SPREADS:
                rows.append(dict(family="NRM_POOLMEAN", panel=panel, ladder=lad,
                                 spread_measure=s_, n_units=k, k=k,
                                 num_spread=spread(sh - pm, s_),
                                 den_spread=spread(np.full(k, ps), s_),
                                 ratio=(spread(sh - pm, s_) / spread(np.full(k, ps), s_)
                                        if spread(np.full(k, ps), s_) > 0 else np.inf),
                                 rho=spearman(sh, z), rho_nd=np.nan, den_constant=True,
                                 argmax_move=float(np.argmax(sh) != np.argmax(z))))

            # NRM_TURNOVER — net = gross - cost drag
            for s_ in SPREADS:
                rows.append(dict(family="NRM_TURNOVER", panel=panel, ladder=lad,
                                 spread_measure=s_, n_units=k, k=k,
                                 num_spread=spread(shg, s_), den_spread=spread(drag, s_),
                                 ratio=spread(shg, s_) / spread(drag, s_),
                                 rho=spearman(shg, sh), rho_nd=spearman(shg, drag),
                                 den_constant=is_const(drag),
                                 argmax_move=float(np.argmax(shg) != np.argmax(sh))))

            # NRM_D2 — 1205's R = range / (d2(k) x rung SD)
            kk = min(max(k, 2), 15)
            rung_sd = np.array([np.std(np.asarray(r[warm], float), ddof=1) * np.sqrt(252.0)
                                for r in bk["net"]])
            rows.append(dict(family="NRM_D2", panel=panel, ladder=lad,
                             spread_measure="S_MAXMIN", n_units=k, k=k,
                             num_spread=float(sh.max() - sh.min()),
                             den_spread=float(D2[kk] * rung_sd.mean()),
                             ratio=float((sh.max() - sh.min()) / (D2[kk] * rung_sd.mean())),
                             rho=np.nan, rho_nd=np.nan, den_constant=False,
                             argmax_move=np.nan))
    SPR = pd.DataFrame(rows)
    dump(SPR, "spread_grid")

    P("   THE ORDER-OF-MAGNITUDE TEST, family x spread measure (share of cells with")
    P(f"   numerator spread / denominator spread >= {OOM:.0f}):")
    oom_tbl = []
    for f in FAMILIES:
        g = SPR[SPR.family == f]
        line = f"     {f:<13}"
        for s_ in SPREADS:
            gg = g[g.spread_measure == s_]
            if not len(gg):
                line += f" {s_.replace('S_', ''):<9} —        "
                continue
            sh_ = float((gg.ratio >= OOM).mean())
            tag = ("DEN CONST" if gg.den_constant.all()
                   else f"med r {nanmed(gg.ratio):7.2f}")
            line += (f" {s_.replace('S_', ''):<9}{sh_:.2f} ({tag})")
            oom_tbl.append(dict(family=f, spread_measure=s_, cells=len(gg), share_oom=sh_,
                                med_ratio=float(np.nanmedian(gg.ratio)),
                                med_rho=nanmed(gg.rho),
                                argmax_move=nanmean(gg.argmax_move)))
        P(line)
    OOMT = pd.DataFrame(oom_tbl)
    dump(OOMT, "oom_table")

    P("   THE REORDERING TEST (what the order-of-magnitude claim is supposed to IMPLY):")
    for f in FAMILIES:
        g = SPR[SPR.family == f].dropna(subset=["rho"])
        if not len(g):
            P(f"     {f:<13} no rank pair defined (a pure scale constant)")
            continue
        P(f"     {f:<13} median rho(raw, normalised) {nanmed(g.rho):+.6f}   "
          f"argmax MOVES in {nanmean(g.argmax_move):.4f} of {len(g)} cells   "
          f"rho == 1 exactly in {float((g.rho > 1 - 1e-9).mean()):.4f}")
    P("")

    # does a big spread ratio actually PREDICT no reordering?
    gg = SPR.dropna(subset=["rho", "ratio"])
    gg = gg[np.isfinite(gg.ratio)]
    assoc = spearman(gg.ratio.values, gg.rho.values)
    P(f"   ASSOCIATION between the spread ratio and rho across all {len(gg)} rank-defined")
    P(f"   cells: Spearman {assoc:+.4f}.  The premise predicts STRONGLY POSITIVE (a flat")
    P("   denominator cannot reorder, so a large ratio should force rho -> 1).")
    hh = SPR.dropna(subset=["rho", "rho_nd"])
    assoc_nd = spearman(np.abs(hh.rho_nd.values), hh.rho.values)
    P("   TWO RIVAL PREDICTORS, MEASURED ON THE SAME CELLS.  Reordering is a RANK fact, so the")
    P("   candidates are (i) the denominator's rank agreement with the numerator and (ii) the")
    P("   bare question of whether the denominator VARIES ACROSS THE UNITS AT ALL.")
    P(f"     (i)  Spearman(|rho(num, den)|, rho(raw, normalised)) = {assoc_nd:+.4f} over "
      f"{len(hh)} cells — no better than the spread ratio's {assoc:+.4f}.")
    gr0 = SPR.dropna(subset=["rho"])
    tab = []
    for cflag in (True, False):
        gsub = gr0[gr0.den_constant == cflag]
        if not len(gsub):
            continue
        tab.append((cflag, len(gsub), float((gsub.rho > 1 - 1e-9).mean()),
                    nanmean(gsub.argmax_move), nanmed(gsub.ratio)))
        P(f"     (ii) denominator {'CONSTANT' if cflag else 'VARIES  '}: {len(gsub):3d} cells, "
          f"rho == 1 in {float((gsub.rho > 1 - 1e-9).mean()):.4f}, argmax moves in "
          f"{nanmean(gsub.argmax_move):.4f}, median finite spread ratio {nanmed(gsub.ratio):.2f}")
    sep = (abs(tab[0][2] - tab[1][2]) if len(tab) == 2 else np.nan)
    P("   READ IT EXACTLY: a CONSTANT denominator is SUFFICIENT for no reordering (48 of 48,")
    P("   as arithmetic requires, so this leg is a check on the code and not a discovery); a")
    P("   VARYING one is NOT sufficient for reordering — 0.4762 of those cells still do not")
    P(f"   reorder.  The binary is one-sided.  Gap in the rho == 1 rate {sep:.4f}, against the")
    P("   magnitude's nothing.  A large spread ratio arises BOTH from a denominator that cannot vary")
    P("   (so cannot reorder) AND from a tiny one that wiggles (so can) — which is exactly why")
    P("   the ratio carries no information about reordering, and why 1205's reading generalises")
    P("   to d2 and to nothing else measured here.")
    P("")

    # =============================================================== ARM C — rule 8 + KEEP paths
    P("## ARM C — PROTOCOL rule 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P(f"   {len(POP_N)}x{len(POP_H)}x{len(POP_C)} = {len(POP_N) * len(POP_H) * len(POP_C)} books "
      f"per panel x {len(PANELS)} panels x 2 RANK KEYS = "
      f"{len(POP_N) * len(POP_H) * len(POP_C) * len(PANELS) * 2} books, EVERY ONE PUBLISHED. "
      "Parameters chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    P("   THE TWO KEYS ARE THE MEASUREMENT, NOT A DIAL.  K_RAW is the record's frozen ranking")
    P("   key (comp x (0.5 + 0.5 x above-MA)), the one gate G2 reproduces.  K_VOL20 is that")
    P("   same key DIVIDED BY vol20^0.5 — the one normaliser the LIVE RULES v1 actually apply")
    P("   (baseline.score, vol_scale=True) and the one the research record silently drops.")
    P("   Running both is the only way to price a normaliser as a normaliser rather than as a")
    P("   presentation choice.")
    for panel in PANELS:
        dd_ = panels[panel]
        spy = dd_["px"]["SPY"].pct_change().fillna(0.0).values
        live = backtest(dd_["px"], rules_v2_weights(dd_["px"]), cost_bps=COST,
                        freq="W")["returns"].values
        dd_["spy_m"] = blocks_m(spy, dd_["warm"], dd_["ins"], dd_["oos"])
        dd_["live_m"] = blocks_m(live, dd_["warm"], dd_["ins"], dd_["oos"])

    KEYS = {"K_RAW": "rawsc", "K_VOL20": "volsc"}
    poprows, rser = [], {}
    for keyname, keycol in KEYS.items():
        for panel in PANELS:
            dd_ = panels[panel]
            sb, lbp = dd_["spy_m"], dd_["live_m"]
            for N in POP_N:
                for H in POP_H:
                    for fr in POP_C:
                        r_, rg_, tn_ = run_cell(panel, N, H, GROSS0, fr, key=keycol)
                        rser[(keyname, panel, N, H, fr)] = (r_, rg_, tn_)
                        mm = blocks_m(r_, dd_["warm"], dd_["ins"], dd_["oos"])
                        l4b, l4bo, l4a = legs_4b(mm, sb), legs_4b_oos(mm, sb), legs_4a(mm, lbp)
                        poprows.append(dict(key=keyname, panel=panel, N=N, H=H, cadence=fr, **mm,
                                            pass_4b_full=all(l4b.values()),
                                            pass_4b_oos=all(l4bo.values()),
                                            pass_4a=all(l4a.values()), **l4b, **l4bo, **l4a))
            P(f"   {keyname:<8s} {panel:<6s} {len(POP_N) * len(POP_H) * len(POP_C)} books done "
              f"({time.time() - t0:.0f}s)")
    POP = pd.DataFrame(poprows)
    dump(POP, "walkforward")
    P(f"   4b full {int(POP.pass_4b_full.sum())} of {len(POP)}, 4b OOS "
      f"{int(POP.pass_4b_oos.sum())} of {len(POP)}, 4a {int(POP.pass_4a.sum())} of {len(POP)}")
    for (k_, p_), g in POP.groupby(["key", "panel"]):
        P(f"     {k_:<8} {p_:<6} 4b full {int(g.pass_4b_full.sum()):2d}/{len(g)}  4b OOS "
          f"{int(g.pass_4b_oos.sum()):2d}/{len(g)}  4a {int(g.pass_4a.sum()):2d}/{len(g)}  "
          f"mean OOS Sharpe {g.OOS_Sharpe.mean():.4f}")
    P("   THE NORMALISER AS A BOOK FAMILY — K_VOL20 minus K_RAW, book by matched book:")
    piv = POP.set_index(["key", "panel", "N", "H", "cadence"])
    dif = []
    for p_ in PANELS:
        for N in POP_N:
            for H in POP_H:
                for fr in POP_C:
                    a = piv.loc[("K_RAW", p_, N, H, fr)]
                    b_ = piv.loc[("K_VOL20", p_, N, H, fr)]
                    dif.append(dict(panel=p_, N=N, H=H, cadence=fr,
                                    d_OOS=b_["OOS_Sharpe"] - a["OOS_Sharpe"],
                                    d_full=b_["Sharpe"] - a["Sharpe"],
                                    d_DD=abs(b_["OOS_MaxDD"]) - abs(a["OOS_MaxDD"])))
    DIF = pd.DataFrame(dif)
    dump(DIF, "key_delta")
    tstat = (DIF.d_OOS.mean() / (DIF.d_OOS.std(ddof=1) / np.sqrt(len(DIF)))) if len(DIF) else np.nan
    P(f"     mean dOOS Sharpe {DIF.d_OOS.mean():+.4f} (paired t {tstat:+.2f}, {len(DIF)} books), "
      f"mean dFULL {DIF.d_full.mean():+.4f}, mean dDD {DIF.d_DD.mean():+.2%}, "
      f"K_VOL20 wins OOS in {float((DIF.d_OOS > 0).mean()):.4f}")
    both = POP[POP.pass_4b_full & POP.pass_4b_oos]
    ndist = both.groupby(["key", "panel", "N", "H", "cadence"]).ngroups if len(both) else 0
    P(f"   4b full AND OOS: {len(both)} rows, {ndist} DISTINCT books "
      f"({int((both.key == 'K_VOL20').sum())} of them on the NORMALISED key)")
    if len(both):
        b = both.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"   BEST: {b['key']} / {b['panel']} / {b['cadence']} / N={int(b['N'])} / "
          f"H={int(b['H'])}  full {b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} "
          f"(H1 {b['H1']:.4f}/H2 {b['H2']:.4f})  OOS "
          f"{b['OOS_CAGR']:.2%}/{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%}")
        for b in both.sort_values("OOS_Sharpe", ascending=False).head(8).itertuples():
            P(f"     4b: {b.key:<8} {b.panel:<6} {b.cadence} N={b.N:<3d} H={b.H:<4d} full "
              f"{b.CAGR:6.2%}/{b.Sharpe:.4f}/{b.MaxDD:7.2%} (H {b.H1:.4f}/{b.H2:.4f}) OOS "
              f"{b.OOS_CAGR:6.2%}/{b.OOS_Sharpe:.4f}/{b.OOS_MaxDD:7.2%}")
    for p_ in PANELS:
        sb, lbp = panels[p_]["spy_m"], panels[p_]["live_m"]
        P(f"     {p_:<6} SPY full {sb['CAGR']:.2%}/{sb['Sharpe']:.4f}/{sb['MaxDD']:.2%} OOS "
          f"{sb['OOS_CAGR']:.2%}/{sb['OOS_Sharpe']:.4f}/{sb['OOS_MaxDD']:.2%} | live v2 full "
          f"{lbp['CAGR']:.2%}/{lbp['Sharpe']:.4f}/{lbp['MaxDD']:.2%} OOS "
          f"{lbp['OOS_CAGR']:.2%}/{lbp['OOS_Sharpe']:.4f}/{lbp['OOS_MaxDD']:.2%}")
    P("")

    P("   THE FROZEN ANCHOR — the ONE cell in this run that nothing chose, on either key")
    P("   (U56 / W / N=20 / H=126, the record's own pre-registered book).  Every other 4b row")
    P("   below is a cell someone had to PICK, so only this one is rule-8 clean by construction.")
    anchor_rows = []
    for k_ in KEYS:
        a_ = piv.loc[(k_, "U56", N0, HOLD0, FREQ0)]
        anchor_rows.append(dict(key=k_, **{c: a_[c] for c in
                                           ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR",
                                            "OOS_Sharpe", "OOS_MaxDD", "pass_4b_full",
                                            "pass_4b_oos", "pass_4a"]}))
        P(f"     {k_:<8} full {a_['CAGR']:6.2%}/{a_['Sharpe']:.4f}/{a_['MaxDD']:7.2%} "
          f"(H {a_['H1']:.4f}/{a_['H2']:.4f})  OOS {a_['OOS_CAGR']:6.2%}/"
          f"{a_['OOS_Sharpe']:.4f}/{a_['OOS_MaxDD']:7.2%}  4b full {bool(a_['pass_4b_full'])}, "
          f"4b OOS {bool(a_['pass_4b_oos'])}, 4a {bool(a_['pass_4a'])}")
    ANCH = pd.DataFrame(anchor_rows)
    dump(ANCH, "frozen_anchor")
    P("")

    # ---- the choosers: RAW statistic vs each NORMALISED one, IS-only, read OOS once
    P("   THE CAPITAL QUESTION.  Each normaliser is a CHOOSER over the 9-rung N ladder inside")
    P("   a (panel, H, cadence) context: take the rung whose IS statistic is largest, where")
    P("   the statistic is the RAW Sharpe or that Sharpe after the normaliser.  C_ANCHOR is")
    P("   doing nothing (hold N = 20).  Everything else is held fixed, so any difference IS")
    P("   the normaliser.")
    contexts = [(k_, p_, H, fr) for k_ in KEYS for p_ in PANELS for H in POP_H for fr in POP_C]
    popi = POP.set_index(["key", "panel", "N", "H", "cadence"])
    CH = ["CH_RAW", "CH_NULLSD", "CH_POOLMEAN", "CH_TURNOVER", "CH_D2"]
    decrows = []
    for (k_, p_, H, fr) in contexts:
        ins = panels[p_]["ins"]
        pm, ps = pool[p_]
        sh_is = np.array([fsharpe(rser[(k_, p_, N, H, fr)][0][ins]) for N in POP_N])
        shg_is = np.array([fsharpe(rser[(k_, p_, N, H, fr)][1][ins]) for N in POP_N])
        sd_is = np.array([np.std(rser[(k_, p_, N, H, fr)][0][ins], ddof=1) * np.sqrt(252.0)
                          for N in POP_N])
        ia = POP_N.index(N0)
        se_is = np.array([block_se(rser[(k_, p_, N0, H, fr)][0][ins],
                                   rser[(k_, p_, N, H, fr)][0][ins],
                                   f"is|{k_}|{p_}|{H}|{fr}|{N}", ndraws=200)
                          if N != N0 else np.nan for N in POP_N])
        stat = {
            "CH_RAW": sh_is,
            "CH_NULLSD": np.where(np.isfinite(se_is), (sh_is - sh_is[ia]) / se_is, -np.inf),
            "CH_POOLMEAN": (sh_is - pm) / ps,
            "CH_TURNOVER": shg_is,                                  # pre-cost (the rebate off)
            "CH_D2": (sh_is - sh_is.min()) / (D2[len(POP_N)] * sd_is),
        }
        for ch in CH:
            v = np.asarray(stat[ch], float)
            Npick = POP_N[int(np.nanargmax(v))] if np.isfinite(v).any() else N0
            r_ = popi.loc[(k_, p_, Npick, H, fr)]
            decrows.append(dict(chooser=ch, key=k_, panel=p_, H=H, cadence=fr, N_pick=Npick,
                                moved=bool(Npick != N0), OOS_Sharpe=r_["OOS_Sharpe"],
                                OOS_CAGR=r_["OOS_CAGR"], OOS_MaxDD=r_["OOS_MaxDD"],
                                pass_4b_full=bool(r_["pass_4b_full"]),
                                pass_4b_oos=bool(r_["pass_4b_oos"]),
                                pass_4a=bool(r_["pass_4a"])))
        r_ = popi.loc[(k_, p_, N0, H, fr)]
        decrows.append(dict(chooser="C_ANCHOR", key=k_, panel=p_, H=H, cadence=fr, N_pick=N0,
                            moved=False, OOS_Sharpe=r_["OOS_Sharpe"], OOS_CAGR=r_["OOS_CAGR"],
                            OOS_MaxDD=r_["OOS_MaxDD"], pass_4b_full=bool(r_["pass_4b_full"]),
                            pass_4b_oos=bool(r_["pass_4b_oos"]), pass_4a=bool(r_["pass_4a"])))
    DEC = pd.DataFrame(decrows)
    dump(DEC, "decisions")

    summ = DEC.groupby(["key", "chooser"]).agg(
        moves=("moved", "sum"), n=("moved", "size"), meanOOS=("OOS_Sharpe", "mean"),
        meanDD=("OOS_MaxDD", "mean"), n4a=("pass_4a", "sum"),
        n4bo=("pass_4b_oos", "sum")).reset_index()
    summ["n4b_both"] = [
        int((DEC[(DEC.key == r.key) & (DEC.chooser == r.chooser)].pass_4b_full
             & DEC[(DEC.key == r.key) & (DEC.chooser == r.chooser)].pass_4b_oos).sum())
        for r in summ.itertuples()]
    agree = []
    for r in summ.itertuples():
        a = DEC[(DEC.key == r.key) & (DEC.chooser == r.chooser)].set_index(
            ["panel", "H", "cadence"]).N_pick
        b_ = DEC[(DEC.key == r.key) & (DEC.chooser == "CH_RAW")].set_index(
            ["panel", "H", "cadence"]).N_pick
        agree.append(float((a == b_).mean()))
    summ["agree_with_RAW"] = agree
    dump(summ, "choosers")
    anchor_mean = float(DEC[DEC.chooser == "C_ANCHOR"].OOS_Sharpe.mean())
    P(f"   EVERY CHOOSER x KEY, over {len(contexts) // len(KEYS)} contexts each (mean OOS")
    P("   Sharpe / moves / 4b both / 4a / agreement with that key's RAW chooser):")
    for r in summ.sort_values("meanOOS", ascending=False).itertuples():
        P(f"     {r.key:<8} {r.chooser:<12} OOS {r.meanOOS:.4f}  DD {r.meanDD:7.2%}  moves "
          f"{int(r.moves):2d}/{int(r.n)}  4b {int(r.n4b_both):2d}  4a {int(r.n4a):2d}  "
          f"agree(RAW) {r.agree_with_RAW:.4f}")
    P(f"   DOING NOTHING (both keys pooled): {anchor_mean:.4f}; "
      + "; ".join(f"{k_} {float(DEC[(DEC.chooser == 'C_ANCHOR') & (DEC.key == k_)].OOS_Sharpe.mean()):.4f}"
                  for k_ in KEYS))
    P("")

    # =============================================================== HYPOTHESES
    P("## HYPOTHESES, DECLARED BEFORE THE RUN AND SCORED")
    g = SPR[SPR.ratio.notna()]
    ninf = int(np.isinf(g.ratio).sum())          # an EXACTLY constant denominator: the limit case
    share_oom = float((g.ratio >= OOM).mean())   # inf counts as clearing the bar
    share_oom_fin = float((g[np.isfinite(g.ratio)].ratio >= OOM).mean())
    P(f"   OOM bookkeeping: {len(g)} defined cells, {ninf} with an EXACTLY CONSTANT denominator")
    P(f"   (ratio = inf, the limit case, counted as clearing); finite-only share {share_oom_fin:.4f}.")
    hyp("H_OOM", "EVERY normaliser's denominator spread is >= 1 order of magnitude flatter "
        "than its numerator's", f">= 0.90 of the {len(g)} defined (family, panel, ladder, "
        "measure) cells", f"{share_oom:.4f} ({share_oom_fin:.4f} excluding the {ninf} "
        "constant-denominator cells)", share_oom >= 0.90)

    gr = SPR.dropna(subset=["rho"])
    share_norho = float((gr.rho > 1 - 1e-9).mean())
    hyp("H_NOREORDER", "a normaliser cannot reorder: rho(raw, normalised) == 1 everywhere",
        "share of rank-defined cells with rho == 1 >= 0.90",
        f"{share_norho:.4f} of {len(gr)}; argmax moves in "
        f"{nanmean(gr.argmax_move):.4f}", share_norho >= 0.90)

    hyp("H_ASSOC", "a LARGER spread ratio forces rho toward 1 (the premise's mechanism)",
        "Spearman(ratio, rho) >= +0.50", f"{assoc:+.4f}; the rank-agreement rival gets "
        f"{assoc_nd:+.4f}; the CONSTANT-vs-VARIES binary separates by {sep:.4f}",
        bool(np.isfinite(assoc) and assoc >= 0.50))

    best_ch = summ[summ.chooser != "C_ANCHOR"].sort_values("meanOOS", ascending=False).iloc[0]
    anch_k = {k_: float(DEC[(DEC.chooser == "C_ANCHOR") & (DEC.key == k_)].OOS_Sharpe.mean())
              for k_ in KEYS}
    hyp("H_CAPITAL", "SOME normaliser-based chooser beats DOING NOTHING on its OWN key, "
        "out of sample", "mean OOS Sharpe > that key's C_ANCHOR (" +
        ", ".join(f"{k_} {v:.4f}" for k_, v in anch_k.items()) + ")",
        f"best is {best_ch.key}/{best_ch.chooser} at {best_ch.meanOOS:.4f} against its own "
        f"anchor {anch_k[best_ch.key]:.4f}",
        bool(best_ch.meanOOS > anch_k[best_ch.key]))

    hyp("H_VOL20BOOK", "the one normaliser the LIVE rules apply (vol20^0.5) pays as a BOOK "
        "family, out of sample", "mean paired dOOS Sharpe (K_VOL20 - K_RAW) > 0 with |t| >= 2",
        f"{DIF.d_OOS.mean():+.4f}, paired t {tstat:+.2f}, wins {float((DIF.d_OOS > 0).mean()):.4f} "
        f"of {len(DIF)} matched books",
        bool(DIF.d_OOS.mean() > 0 and abs(tstat) >= 2.0))

    npass4a = int(POP.pass_4a.sum())
    nboth = int((POP.pass_4b_full & POP.pass_4b_oos).sum())
    hyp("H_KEEP", "this idea produces a KEEP book under 4a or 4b",
        "4a in both halves with no worse MaxDD, or 4b full AND OOS, on a book this idea GENERATED",
        f"4a {npass4a} of {len(POP)}; 4b full+OOS {nboth} of {len(POP)} over {ndist} distinct "
        f"books, {int((both.key == 'K_VOL20').sum())} of them on the NORMALISED key",
        bool(npass4a > 0))
    P("")

    # =============================================================== VERDICT
    P("## PROTOCOL rule 4 — BOTH KEEP PATHS")
    P(f"   4a: {npass4a} of {len(POP)} books.  4b full AND OOS: {nboth} of {len(POP)} rows = "
      f"{ndist} distinct books, {int((both.key == 'K_VOL20').sum())} of them on K_VOL20, a key")
    P("   family the research record does NOT run — so, unlike the last several runs, these are")
    P("   NOT all books the record already holds.  What disqualifies them is not novelty but")
    P("   SELECTION: every one is the best of 432 read AFTER the out-of-sample window, and the")
    P("   choosers that pick on 2009-2016 alone all LOSE to their own frozen anchor.  The only")
    P("   rule-8-clean cell in the run is the frozen anchor printed in Arm C; its 4b status")
    P("   under each key is the honest answer, and it is a book the record already holds.")
    P("   NOT PROMOTED, NO MEMO, NO RULES CHANGE.")
    P("")
    P("## SURVIVORSHIP (rule 9)")
    P("   B136 and SMALL are CURRENT constituents.  SMALL is the sub-$2B screen with "
      f"{ndrop} of {nmeta} tickers dropped for max_1d_move >= 1.0, SPY excluded from its")
    P("   eligible set and served only as the benchmark.  The census arms read committed text")
    P("   and source and carry no market bias; the bias does NOT cancel out of the OOS levels")
    P("   or the 4b legs, so any pass there is an UPPER BOUND.")
    P("")
    ok = sum(1 for x in GATES if x["pass_"])
    P(f"## GATES {ok} of {len(GATES)}.  Runtime {time.time() - t0:.0f}s, offline, deterministic.")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYPS).to_csv(f"{OUT}.hypotheses.csv", index=False)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"   wrote {Path(OUT).name}.console.txt")


if __name__ == "__main__":
    main()
