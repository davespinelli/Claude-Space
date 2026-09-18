#!/usr/bin/env python3
"""Idea 1251 (lane B, 2026-09-18)
   does-the-OBSERVED-vs-BAR-line-explain-the-record-s-OTHER-INVARIANCE-claims

THE QUEUE'S PREMISE, QUOTED.  Idea 1242 found the L-free set is exactly the class of
outputs that never touch a draw (5 of 18, bit-identical at all 12 L rungs) and that NO bar
output is noise-bound.  The same line should predict invariance to the record's OTHER
resample knobs (SEED, B, draw kind, recentring).  Re-run the 18-output partition against
those knobs instead of L and report whether the OBSERVED/BAR line is the whole story or
whether some bar outputs are knob-specific.

WHAT "THE WHOLE STORY" MEANS, DECLARED BEFORE MEASURING.  If the line is the whole story
the partition is a PROPERTY OF THE OUTPUT and not of the knob: every OBS output lands in
cell 1 (structurally free) on EVERY knob, and every BAR output lands in cell 3
(knob-dependent) on EVERY knob, exactly as it did on L.  It is NOT the whole story if any
BAR output is KNOB-SPECIFIC -- free of one knob and dependent on another -- because then
"bar-side" does not tell an implementer which dial their number is keyed to, and a
committed sentence naming only L is under-stated for reasons the L study could not see.

  H_LINE        every BAR output is cell 3 on every knob and every OBS output is cell 1
                on every knob  (the queue's own prediction)
  H_OBSFREE     the 5 OBS outputs are bit-identical across every knob and every setting
  H_SPECIFIC    at least one BAR output is knob-specific (cell 1 or 2 on one knob, cell 3
                on another)                                    -- the direct negation of H_LINE
  H_MONEY       an OBS-side (knob-free) gate buys at least as much rule-8 OOS Sharpe as the
                best knob-keyed BAR gate

THE THREE CELLS ARE 1242's, UNCHANGED, and the bar is declared before measuring.  A BAR
output cannot be convicted by exact inequality -- a different knob means different DRAWS, so
an output that does not depend on the knob at all still moves on Monte-Carlo noise.  Each
output's KNOB swing is therefore measured against its OWN SEED swing (same 72 decisions,
same B, frozen construction, 8 rng streams):
    (1) STRUCTURALLY FREE     exact bitwise invariance across every setting and every seed
    (2) NOISE-BOUND           moves, but no more than NOISE_MULT x its own seed swing
    (3) KNOB-DEPENDENT        knob swing > NOISE_MULT x seed swing        NOISE_MULT = 2.0

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `KNOB`        {K_SEED, K_B, K_DRAW, K_RECENTRE}   K_SEED is the yardstick knob and is
                reported as a calibration cell (its ratio is 1.0 by construction); K_B walks
                the draw count {125, 250, 500, 1000, 2000}; K_DRAW walks the resample law
                {MBB (1101/1208's own moving block, no wrap), CBB (circular, wrapped), SB
                (stationary, geometric blocks, same mean L), IID}; K_RECENTRE walks
                {RAW, RECENTRED} (each rung column shifted to the observed level).
  `OUTPUT SET`  {OS_CORE, OS_WIDE, OS_ALL}          1242's own three sets, unchanged.

  = 12 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`; every output at every setting
  of every knob is published per decision in `.outputs.csv` and per output in
  `.partition.csv`.  The headline uses KNOB = K_DRAW and OS_CORE.  Nothing is ever selected
  on a knob ladder -- the ladder is the object under measurement.

FROZEN at 1096/1101/1154/1208/1242's construction: the SAME 72 decisions (PANEL {U56, B136,
SMALL} x ANCHOR {A, B} x LADDER {N, H, GROSS, CADENCE} x CHOOSER {CH_ISSHARPE, CH_ISCAGR,
CH_ISDD}), CAND20 legs, max_vol 0.60, min hold from the H ladder, cadence from the CADENCE
ladder, 10 bps (rule 2), LAG 1, warm-up 260, IS end 2016-12-31, bar 0.90, L = 63, crc32
seeds, DD cap 0.60, CAGR floor 0.70.  The frozen cell (MBB, B = 1000, RAW, stream 0) is
1242's L = 63 cell with 1242's own seeds and chunking, so gate G4 checks it row by row
against 1242's committed `.outputs.csv` rather than asserting it.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the current
constituents of a sub-$2B screen (data/SMALL_PANEL_README.md).  Every LEVEL here -- CAGR,
MaxDD, Sharpe and every null built on them -- is optimistic, and a resample null prices
SAMPLING error on the tape it is handed and cannot correct that.  It largely cancels out of
the headline, which is a RATIO of one construction against itself on the same tape, and it
does NOT cancel out of the 4b legs, so any pass in ARM E is an upper bound.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations

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

DATE = "2026-09-18"
SLUG = "does-the-OBSERVED-vs-BAR-line-explain-the-record-s-OTHER-INVARIANCE-claims"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
REF_1242 = (Path(__file__).resolve().parent /
            "2026-09-17_is-REACH-the-only-RESAMPLING-OUTPUT-in-the-record-that-is-L-FREE_B"
            ".outputs.csv")

# ------------------------------------------------------------------ 1101/1208/1242 construction
LAG, WARMUP, MAXVOL = 1, 260, 0.60
IS_END = "2016-12-31"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COST = 10.0
LEGS = [(21, 252), (0, 126), (0, 63)]

LAD_N = [5, 8, 10, 12, 15, 20, 25, 30, 40]
LAD_H = [21, 63, 126, 252]
LAD_G = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75]
LAD_C = ["D", "W", "M", "Q"]
LADDERS = {"N": LAD_N, "H": LAD_H, "GROSS": LAD_G, "CADENCE": LAD_C}
LADNAMES = ["N", "H", "GROSS", "CADENCE"]

ANCHORS = {
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

BAR_HI = 0.90
SEED_BASE = 12081208
L_HEAD = 63                            # frozen: the knobs are walked AT the record's L
NOISE_MULT = 2.0                       # DECLARED BEFORE MEASURING (cell-3 bar)

# ------------------------------------------------------------------ dial 1: the knobs
SEED_LADDER = [0, 1, 2, 3, 4, 5, 6, 7]       # the yardstick (also the K_SEED ladder)
SEED_REPS = [0, 1, 2]                        # streams each non-seed setting is averaged over
B_LADDER = [125, 250, 500, 1000, 2000]
DRAW_LADDER = ["MBB", "CBB", "SB", "IID"]
REC_LADDER = ["RAW", "RECENTRED"]
FROZEN = dict(stream=0, B=1000, draw="MBB", rec="RAW")

KNOBS = {
    "K_SEED":     dict(field="stream", ladder=SEED_LADDER, ends=(0, 7)),
    "K_B":        dict(field="B", ladder=B_LADDER, ends=(125, 2000)),
    "K_DRAW":     dict(field="draw", ladder=DRAW_LADDER, ends=("MBB", "IID")),
    "K_RECENTRE": dict(field="rec", ladder=REC_LADDER, ends=("RAW", "RECENTRED")),
}
KNOBNAMES = list(KNOBS)
K_HEAD = "K_DRAW"

# ------------------------------------------------------------------ dial 2: output sets (1242's)
OUTPUTS = {
    "O_REACH":      ("OBS", "bool",  "IS argmax rung == anchor rung"),
    "B_PPICK":      ("BAR", "float", "P_boot that the observed argmax is the draw argmax"),
    "B_Q95":        ("BAR", "float", "95th percentile of the pick rung's null statistic"),
    "B_NULLMED":    ("BAR", "float", "median of the pick rung's null statistic"),
    "B_RECRANGE":   ("BAR", "float", "recentred null range q95-q05 of the pick rung"),
    "B_BOOT95":     ("BAR", "float", "95th percentile of the draw top-minus-second gap"),
    "B_PCTRANK":    ("BAR", "float", "percentile rank of the observed level in its own draws"),
    "B_PMAX":       ("BAR", "float", "largest P_boot over rungs"),
    "B_MODALRUNG":  ("BAR", "int",   "index of the modal draw argmax"),
    "B_MODALMATCH": ("BAR", "bool",  "observed argmax IS the modal draw argmax"),
    "B_SD":         ("BAR", "float", "bootstrap SD of the pick rung's statistic"),
    "B_GAPEXCEEDS": ("BAR", "bool",  "observed margin exceeds B_BOOT95"),
    "B_RESOLVED":   ("BAR", "bool",  "P_pick >= 0.90 (the record's decisive bar)"),
    "B_Q05":        ("BAR", "float", "5th percentile of the pick rung's null statistic"),
    "O_PICK":       ("OBS", "int",   "index of the IS argmax rung"),
    "O_MARGIN":     ("OBS", "float", "observed top-minus-second statistic gap"),
    "O_LEVEL":      ("OBS", "float", "observed statistic at the pick rung"),
    "O_GAPRATIO":   ("OBS", "float", "observed margin / observed rung spread"),
}
OS_CORE = ["O_REACH", "B_PPICK", "B_Q95", "B_NULLMED", "B_RECRANGE", "B_BOOT95", "B_PCTRANK"]
OS_WIDE = OS_CORE + ["B_PMAX", "B_MODALRUNG", "B_MODALMATCH", "B_SD", "B_GAPEXCEEDS",
                     "B_RESOLVED", "B_Q05"]
OS_ALL = OS_WIDE + ["O_PICK", "O_MARGIN", "O_LEVEL", "O_GAPRATIO"]
OUTPUT_SETS = {"OS_CORE": OS_CORE, "OS_WIDE": OS_WIDE, "OS_ALL": OS_ALL}
OS_HEAD = "OS_CORE"
BARS = [k for k, v in OUTPUTS.items() if v[0] == "BAR"]
OBSS = [k for k, v in OUTPUTS.items() if v[0] == "OBS"]

# ------------------------------------------------------------------ record's own numbers
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
A1208_REACH = 14
A1242_RATE_63 = 0.222222
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)

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
HYP: list[dict] = []


def cached(suffix, builder):
    """Reuse this script's OWN deterministic artefact if already on disk (delete to rebuild)."""
    p = Path(f"{OUT}.{suffix}.csv")
    if p.exists():
        P(f"  reused {p.name} — deterministic artefact already on disk")
        return pd.read_csv(p)
    df = builder()
    dump(df, suffix)
    return df


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<8s} {'PASS' if ok else 'FAIL'}  {what:<70s} {value:.3e}")
    return bool(ok)


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


# ================================================================== the record's runner
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


class Panel:
    def __init__(self, name, px):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if name == "SMALL":
            elig = elig.copy()
            elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG)
            m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq):
    """Decide at the rebalance close t, apply at t+1 (rule 2), 10 bps on turnover."""
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W)
    Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    return r - turn * COST / 1e4


def ladder_books(pan, anchor, lad, cache):
    a = ANCHORS[anchor]
    out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        key = (pan.name, kw["N"], kw["H"], kw["gross"], kw["freq"])
        if key not in cache:
            cache[key] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"])
        out[rung] = cache[key]
    return out


# ================================================================== the four resample laws
def idx_MBB(rng, T, L, B):
    """1101/1208/1242's own moving block: blocks with replacement, NO wrap."""
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def idx_CBB(rng, T, L, B):
    """Circular block: same block length, starts anywhere, WRAPPED (every row equally used)."""
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(B, nb))
    off = np.arange(L)[None, None, :]
    return ((starts[:, :, None] + off).reshape(B, nb * L)[:, :T]) % T


def idx_SB(rng, T, L, B):
    """Stationary bootstrap (Politis-Romano): geometric block lengths with the SAME mean L."""
    L = int(min(max(L, 1), T))
    starts = rng.integers(0, T, size=(B, T))
    jump = rng.random((B, T)) < (1.0 / L)
    jump[:, 0] = True
    bid = np.cumsum(jump, axis=1) - 1
    ar = np.arange(T)[None, :]
    bstart = np.maximum.accumulate(np.where(jump, ar, -1), axis=1)
    return (np.take_along_axis(starts, bid, axis=1) + (ar - bstart)) % T


def idx_IID(rng, T, L, B):
    """Plain IID resample of rows (the L = 1 limit, kept as its own named law)."""
    return rng.integers(0, T, size=(B, T))


DRAW_FN = {"MBB": idx_MBB, "CBB": idx_CBB, "SB": idx_SB, "IID": idx_IID}


def draw_stats(R, stat, kind, L, seed, B, chunk=100):
    """(B, k) statistic per draw.  For kind=MBB, L=63, B=1000 the rng consumption is
    IDENTICAL to 1208/1242's pboot_argmax, so the frozen cell replays bit for bit."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    fn = DRAW_FN[kind]
    parts, done = [], 0
    while done < B:
        b = min(chunk, B - done)
        X = R[fn(rng, T, L, b)]
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1)
            v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        else:
            raise ValueError(stat)
        parts.append(np.where(np.isfinite(v), v, -np.inf))
        done += b
    return np.vstack(parts)


def recentre(D, obs):
    """K_RECENTRE = RECENTRED: shift every rung column so its draw mean sits on the OBSERVED
    level (the textbook recentring the record's prose sometimes claims and sometimes not).
    -inf draws are left alone; a column with no finite draw is untouched."""
    D2 = D.copy()
    for c in range(D.shape[1]):
        f = np.isfinite(D2[:, c])
        if f.sum() > 0:
            D2[f, c] = D2[f, c] - D2[f, c].mean() + obs[c]
    return D2


def is_stat(r, ins, stat):
    x = r[ins]
    T_is = len(x)
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    if stat == "CH_ISCAGR":
        eq = np.cumprod(1.0 + x)
        return eq[-1] ** (252.0 / T_is) - 1.0
    if stat == "CH_ISDD":
        eq = np.cumprod(1.0 + x)
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def observed_outputs(obs, rungs, anchor_rung):
    """The OBSERVED-side outputs: no draw is touched, so no knob can move them."""
    j = int(np.nanargmax(obs))
    sd = np.sort(obs)[::-1]
    margin = float(sd[0] - sd[1]) if len(sd) > 1 else np.nan
    spread = float(sd[0] - sd[-1]) if len(sd) > 1 else np.nan
    return j, dict(
        O_PICK=float(j),
        O_REACH=float(rungs[j] == anchor_rung),
        O_MARGIN=margin,
        O_LEVEL=float(obs[j]),
        O_GAPRATIO=float(margin / spread) if spread and np.isfinite(spread) and spread > 0 else np.nan,
    )


def bar_outputs(D, obs, j):
    """Every BAR-side output, all from the SAME (B, k) draw matrix (1242's definitions)."""
    am = D.argmax(axis=1)
    Pv = np.bincount(am, minlength=D.shape[1]) / D.shape[0]
    col = D[:, j]
    colf = col[np.isfinite(col)]
    if colf.size == 0:
        colf = np.array([np.nan])
    srt = np.sort(D, axis=1)[:, ::-1]
    gaps = srt[:, 0] - srt[:, 1] if D.shape[1] > 1 else np.zeros(D.shape[0])
    gaps = gaps[np.isfinite(gaps)] if np.isfinite(gaps).any() else np.array([np.nan])
    rec = colf - colf.mean()
    obs_margin = float(np.sort(obs)[::-1][0] - np.sort(obs)[::-1][1]) if len(obs) > 1 else np.nan
    b95 = float(np.percentile(gaps, 95))
    return dict(
        B_PPICK=float(Pv[j]),
        B_PMAX=float(Pv.max()),
        B_MODALRUNG=float(int(Pv.argmax())),
        B_MODALMATCH=float(int(Pv.argmax()) == j),
        B_Q95=float(np.percentile(colf, 95)),
        B_Q05=float(np.percentile(colf, 5)),
        B_NULLMED=float(np.median(colf)),
        B_RECRANGE=float(np.percentile(rec, 95) - np.percentile(rec, 5)),
        B_SD=float(colf.std(ddof=1) if colf.size > 1 else np.nan),
        B_PCTRANK=float(float((colf <= obs[j]).mean())),
        B_BOOT95=b95,
        B_GAPEXCEEDS=float(obs_margin > b95),
        B_RESOLVED=float(Pv[j] >= BAR_HI),
    )


# ================================================================== ARM D: the census
OUTPUT_TOKENS = {
    "B_PPICK":      r"\bP_?boot\b|\bP_?pick\b|\bp_?boot\b",
    "B_Q95":        r"\bq95\b|\b95th percentile\b|\bq_?0?\.?95\b",
    "B_Q05":        r"\bq05\b|\b5th percentile\b",
    "B_NULLMED":    r"\bnull median\b|\bmedian of the null\b|\bnull's median\b",
    "B_RECRANGE":   r"\brecentred (?:null )?range\b|\bre-?centred null\b|\bnull range\b",
    "B_BOOT95":     r"\bB_?BOOT_?95\b|\bbootstrap 95\b|\bbootstrap band\b|\bboot(?:strap)? bar\b",
    "B_PCTRANK":    r"\bpercentile rank\b|\bpercentile of (?:its|the) own\b|\brank within .{0,20}null\b",
    "B_SD":         r"\bbootstrap SD\b|\bboot(?:strap)? standard deviation\b|\bsampling SD\b",
    "B_RESOLVED":   r"\bresolved\b|\bunresolved\b|\bdecisive\b|\bindecisive\b|\bresolution rate\b",
    "B_MODALRUNG":  r"\bmodal (?:rung|argmax|twin|order)\b|\bshare_?top\b",
    "B_MODALMATCH": r"\bargmax is the modal\b|\bis the modal (?:rung|argmax|draw)\b|"
                    r"\bmodal(?:ly)? (?:matches|agrees)\b|\bargmax_is_modal\b",
    "B_PMAX":       r"\bP_?max\b|\blargest P_?boot\b",
    "B_GAPEXCEEDS": r"\bexceeds? its (?:own )?(?:bar|band)\b|\bclears? the (?:bar|band)\b",
    "O_REACH":      r"\breach(?:es|ed)?\b|\bargmax (?:rung )?(?:==|is|equals) (?:the )?anchor\b",
    "O_PICK":       r"\bIS argmax\b|\bargmax rung\b|\bthe pick\b|\bpick(?:ed)? rung\b",
    "O_MARGIN":     r"\b(?:IS )?margin\b|\btop-?minus-?second\b|\brung gap\b",
    "O_LEVEL":      r"\bIS Sharpe\b|\bIS CAGR\b|\bIS[- ]DD\b|\bobserved (?:level|maximum)\b",
    "O_GAPRATIO":   r"\bgap ratio\b|\bspread[- ]normalis?zed\b|\bfraction of the spread\b",
}
assert set(OUTPUT_TOKENS) == set(OUTPUTS), sorted(set(OUTPUTS) ^ set(OUTPUT_TOKENS))
OUTPUT_RE = {k: re.compile(v, re.I) for k, v in OUTPUT_TOKENS.items()}

KNOB_TOKENS = {
    "K_SEED":     r"\bseeds?\b|\brng\b|\bstreams?\b|\bdefault_rng\b|\bseeded\b",
    "K_B":        r"\bB\s*=\s*\d[\d,]*\b|\b\d[\d,]*\s+draws\b|\b\d[\d,]*\s+resamples?\b|"
                  r"\bdraw count\b|\bnumber of draws\b",
    "K_DRAW":     r"\bmoving[- ]block\b|\bcircular[- ]block\b|\bstationary bootstrap\b|"
                  r"\bIID\b|\bi\.i\.d\.\b|\bblock bootstrap\b|\bdraw kind\b|\bnull kind\b|"
                  r"\bRANDROT\b|\bpermutation\b",
    "K_RECENTRE": r"\bre-?cent(?:red|ered|ring|ering)\b|\bde-?mean(?:ed|ing)?\b",
}
KNOB_RE = {k: re.compile(v, re.I) for k, v in KNOB_TOKENS.items()}
LTOK = re.compile(
    r"\b(?:L\s*=\s*(\d+)|block length(?:\s+of)?\s+(\d+)|blocks? of (\d+)|"
    r"(\d+)[- ]day blocks?|L\s*(?:of|is)\s*(\d+))\b", re.I)
VERDICTTOK = re.compile(
    r"\b(resolved|unresolved|decisive|indecisive|not distinguishable|indistinguishable|"
    r"significan\w*|reach(?:es|ed)?|fires?|fired|silent|KEEP|KILL|PARK|passes|fails?|"
    r"survives?|refuted|supported|p\s*[<>=]\s*0?\.\d+)\b", re.I)


def units():
    U = []
    for ln in (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census():
    U, n_md = units()
    rows = []
    for src, txt in U:
        hits = {k: bool(r.search(txt)) for k, r in OUTPUT_RE.items()}
        if not any(hits.values()):
            continue
        ls = [int(g) for m in LTOK.finditer(txt) for g in m.groups() if g]
        obs_h = [k for k in hits if hits[k] and OUTPUTS[k][0] == "OBS"]
        bar_h = [k for k in hits if hits[k] and OUTPUTS[k][0] == "BAR"]
        kn = {k: bool(r.search(txt)) for k, r in KNOB_RE.items()}
        rows.append(dict(src=src, n_chars=len(txt), n_outputs=sum(hits.values()),
                         n_obs=len(obs_h), n_bar=len(bar_h),
                         side=("OBS_ONLY" if not bar_h else
                               ("BAR_ONLY" if not obs_h else "MIXED")),
                         STATES_L=bool(ls), L_STATED=ls[0] if ls else 0,
                         CARRIES_VERDICT=bool(VERDICTTOK.search(txt)),
                         n_knobs_stated=sum(kn.values()),
                         **{f"k_{k}": kn[k] for k in KNOB_RE},
                         **{f"h_{k}": hits[k] for k in OUTPUT_RE}))
    return pd.DataFrame(rows), len(U), n_md


# ================================================================== 4a / 4b legs
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


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1251 (lane B, {DATE}) — does the OBSERVED/BAR line explain the record's OTHER")
    P("                             INVARIANCE claims (SEED, B, DRAW KIND, RECENTRING)?")
    P("=" * 100)
    P("  dial 1 = KNOB        {K_SEED, K_B, K_DRAW, K_RECENTRE}     (headline K_DRAW)")
    P("  dial 2 = OUTPUT SET  {OS_CORE, OS_WIDE, OS_ALL}            (headline OS_CORE)")
    P("  NOT dials: 1242's same 72 decisions (3 panels x 2 anchors x 4 ladders x 3 choosers),")
    P(f"             L frozen at {L_HEAD}, q = 0.90.  SEED is BOTH a knob and the NOISE YARDSTICK")
    P(f"             (8 streams at the frozen cell); the cell-3 bar knob/seed > {NOISE_MULT} is DECLARED HERE.")
    P("")

    # ------------------------------------------------------------ ARM 0: data-free
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What makes an output knob-free before any tape is read.")
    P("-" * 100)
    cls = pd.DataFrame([dict(output=k, declared_class=v[0], kind=v[1], definition=v[2],
                             in_OS_CORE=k in OS_CORE, in_OS_WIDE=k in OS_WIDE)
                        for k, v in OUTPUTS.items()])
    P(cls.to_string(index=False))
    dump(cls, "classes")
    P("  The OBS rows take the observed IS path and nothing else; the draws are not an argument")
    P("  of the function, so no resample knob can move them.  The BAR rows are functionals of")
    P("  the resample law, so ANY knob that changes the draws moves them even where they do not")
    P("  depend on that knob.  That is why cell 2 exists and why the yardstick is the SEED swing.")
    rng = np.random.default_rng(1251)
    Rs = rng.normal(0.0004, 0.01, size=(1200, 6))
    obs_s = np.array([fsharpe(Rs[:, i]) for i in range(6)])
    j_s, o_s = observed_outputs(obs_s, list(range(6)), 3)
    j2, o2 = observed_outputs(obs_s, list(range(6)), 3)
    obs_dev = max(abs(o_s[k] - o2[k]) for k in o_s if np.isfinite(o_s[k]))
    gate("G1", "OBS outputs are not a function of the draws at all (max dev)", obs_dev,
         obs_dev == 0.0)
    devs = {}
    base = draw_stats(Rs, "CH_ISSHARPE", "MBB", 63, 77, B=400)
    bb = bar_outputs(base, obs_s, j_s)
    for kind in ["CBB", "SB", "IID"]:
        d = draw_stats(Rs, "CH_ISSHARPE", kind, 63, 77, B=400)
        devs[kind] = max(abs(bar_outputs(d, obs_s, j_s)[k] - bb[k]) for k in bb)
    devs["B"] = max(abs(bar_outputs(draw_stats(Rs, "CH_ISSHARPE", "MBB", 63, 77, B=2000),
                                    obs_s, j_s)[k] - bb[k]) for k in bb)
    devs["RECENTRE"] = max(abs(bar_outputs(recentre(base, obs_s), obs_s, j_s)[k] - bb[k])
                           for k in bb)
    gate("G2", "BAR outputs DO move on EVERY knob on a synthetic tape (min over knobs)",
         min(devs.values()), min(devs.values()) > 0.0)
    # the three laws must be genuinely different objects
    T_s = 1200
    u_mbb = len(np.unique(idx_MBB(np.random.default_rng(3), T_s, 63, 200)[0]))
    u_cbb = len(np.unique(idx_CBB(np.random.default_rng(3), T_s, 63, 200)[0]))
    u_iid = len(np.unique(idx_IID(np.random.default_rng(3), T_s, 63, 200)[0]))
    gate("G3", "MBB / CBB / IID give materially different row-coverage on one draw",
         float(max(u_mbb, u_cbb, u_iid) - min(u_mbb, u_cbb, u_iid)),
         len({u_mbb, u_cbb, u_iid}) == 3)
    sb_first = idx_SB(np.random.default_rng(5), T_s, 63, 2000)
    runs = (np.diff(sb_first, axis=1) != 1).sum() + sb_first.shape[0]
    mean_block = sb_first.size / runs
    gate("G3b", f"stationary bootstrap mean block length is the frozen L={L_HEAD} (|dev|)",
         abs(mean_block - L_HEAD), abs(mean_block - L_HEAD) < 8.0)
    P("")

    # ------------------------------------------------------------ panels & books
    P("-" * 100)
    P("PANELS (rule 9: all three are current-constituent lists; every LEVEL is optimistic).")
    P("-" * 100)
    raw = {"U56": load_universe(), "B136": load_universe(broad=True),
           "SMALL": load_universe(small=True)}
    pans = {}
    for nm in PANELS:
        pans[nm] = Panel(nm, raw[nm])
        p = pans[nm]
        P(f"  {nm:<6s} {p.T:>5d} rows x {p.K:>4d} cols   {p.idx[0].date()} .. {p.idx[-1].date()}"
          f"   IS {int(p.ins.sum()):>4d} / OOS {int(p.oos.sum()):>4d}")
    cache: dict = {}
    LB: dict = {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                LB[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    P(f"  {len(cache)} distinct rung books built ({time.time() - t0:.0f}s)")
    ab = LB[("U56", "A", "N")][20]
    m = blocks_m(ab, pans["U56"].warm, pans["U56"].ins, pans["U56"].oos)
    gate("G4a", "U56 anchor A full Sharpe replays 1101/1208/1242's 1.139701",
         abs(m["Sharpe"] - A1101_TRIPLE[1]), abs(m["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)
    P("")

    # ------------------------------------------------------------ ARM B: every output, every knob
    P("-" * 100)
    P("ARM B — EVERY OUTPUT AT EVERY SETTING OF EVERY KNOB, ON 1242's SAME 72 DECISIONS.")
    P("-" * 100)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    pre = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        j, oout = observed_outputs(obs, rungs, ANCHORS[an][lad])
        pre[(pn, an, lad, ch)] = (R, obs, j, oout, rungs)

    # the (knob, setting, stream) cells that have to be evaluated
    CELLS = []                                             # (knob, setting, stream, B, draw, rec)
    for s in SEED_LADDER:
        CELLS.append(("K_SEED", s, s, FROZEN["B"], FROZEN["draw"], FROZEN["rec"]))
    for Bv in B_LADDER:
        for s in SEED_REPS:
            CELLS.append(("K_B", Bv, s, Bv, FROZEN["draw"], FROZEN["rec"]))
    for dk in DRAW_LADDER:
        for s in SEED_REPS:
            CELLS.append(("K_DRAW", dk, s, FROZEN["B"], dk, FROZEN["rec"]))
    for rc in REC_LADDER:
        for s in SEED_REPS:
            CELLS.append(("K_RECENTRE", rc, s, FROZEN["B"], FROZEN["draw"], rc))
    ncalls = len({(c[3], c[4], c[2]) for c in CELLS})
    P(f"  decisions {len(DEC)}  x  knob cells {len(CELLS)}  "
      f"({ncalls} distinct draw matrices per decision, memoised)")

    def sd_seed(pn, an, lad, ch, stream):
        """stream 0 reproduces 1242's L=63 seed EXACTLY so the frozen cell replays bit-for-bit."""
        return (seed_of(pn, an, lad, ch, L_HEAD) if stream == 0
                else seed_of(pn, an, lad, ch, L_HEAD, "S", stream))

    def build_outputs():
        rows = []
        for n, (pn, an, lad, ch) in enumerate(DEC):
            R, obs, j, oout, rungs = pre[(pn, an, lad, ch)]
            memo = {}
            for (kn, setting, stream, Bv, dk, rc) in CELLS:
                key = (Bv, dk, stream)
                if key not in memo:
                    memo[key] = draw_stats(R, ch, dk, L_HEAD, sd_seed(pn, an, lad, ch, stream),
                                           B=Bv)
                D = memo[key]
                if rc == "RECENTRED":
                    D = recentre(D, obs)
                rows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, k=len(rungs),
                                 knob=kn, setting=str(setting), stream=stream,
                                 B=Bv, draw=dk, rec=rc, pick=str(rungs[j]),
                                 **oout, **bar_outputs(D, obs, j)))
            if (n + 1) % 12 == 0:
                P(f"    .. {n + 1}/{len(DEC)} decisions  ({time.time() - t0:.0f}s)")
        return pd.DataFrame(rows)

    odf = cached("outputs", build_outputs)
    odf["setting"] = odf.setting.astype(str)
    P(f"  ({time.time() - t0:.0f}s)")

    # ---- replay gate against 1242's committed artefact, row by row
    froz = odf[(odf.knob == "K_SEED") & (odf.stream == 0)]
    if REF_1242.exists():
        ref = pd.read_csv(REF_1242)
        ref = ref[ref.L.astype(str) == str(L_HEAD)]
        mg = ref.merge(froz, on=["panel", "anchor", "ladder", "chooser"], suffixes=("_r", "_m"))
        cols = [c for c in OUTPUTS if f"{c}_r" in mg.columns and f"{c}_m" in mg.columns]
        dv = {c: np.abs(pd.to_numeric(mg[f"{c}_r"], errors="coerce")
                        - pd.to_numeric(mg[f"{c}_m"], errors="coerce")) for c in cols}
        # data/prices.csv (the U56 tape) gained a daily close after 1242 ran, and the
        # dividend re-adjustment moves the WHOLE history at ~1e-7.  B136 and SMALL were not
        # refreshed, so the replay there must still be BIT-EXACT: that is the real gate.
        frz = mg.panel.isin(["B136", "SMALL"]).values
        dev_frz = max(float(np.nanmax(d.values[frz])) for d in dv.values())
        gate("G4", f"frozen cell replays 1242's L=63 BIT-EXACT on the {int(frz.sum())} rows whose "
                   "tape did not move", dev_frz, dev_frz == 0.0 and len(mg) == 72)
        others = [c for c in cols if c != "B_PCTRANK"]
        dev_u56 = max(float(np.nanmax(dv[c].values[~frz])) for c in others)
        gate("G4b", "U56 rows replay to the tape's own re-adjustment drift (all but B_PCTRANK)",
             dev_u56, dev_u56 < 1e-4)
        pr = dv["B_PCTRANK"].values[~frz]
        P(f"  NOTE: B_PCTRANK moves up to {np.nanmax(pr):.3f} on {int((pr > 0).sum())} of "
          f"{len(pr)} U56 rows for a ~1e-7 shift in the observed level — the percentile rank")
        P("        of an observed MaxDD is discontinuous because many block draws reproduce the")
        P("        same worst episode exactly.  Reported, not gated: it is a property of the")
        P("        statistic, and it is the sharpest single warning in this run.")
    else:
        gate("G4", "1242's committed outputs.csv present for the row-by-row replay", 1.0, False)
    reach_by = odf.groupby(["knob", "setting", "stream"], sort=False).O_REACH.sum()
    gate("G5", f"reach = {A1208_REACH} of 72 at EVERY (knob, setting, stream) (max |dev|)",
         float(np.abs(reach_by - A1208_REACH).max()), bool((reach_by == A1208_REACH).all()))
    r63 = float(froz.B_RESOLVED.mean())
    gate("G6", f"frozen-cell resolution rate replays 1242's L=63 rate ({A1242_RATE_63:.4f})",
         abs(r63 - A1242_RATE_63), abs(r63 - A1242_RATE_63) < 1e-6)
    P("")
    P("  the knob ladders, side by side, over the SAME 72 decisions (mean over streams):")
    side = (odf.groupby(["knob", "setting"], sort=False)
            .agg(resolution_rate=("B_RESOLVED", "mean"), mean_P_pick=("B_PPICK", "mean"),
                 mean_B_BOOT95=("B_BOOT95", "mean"), mean_B_PCTRANK=("B_PCTRANK", "mean"),
                 mean_B_RECRANGE=("B_RECRANGE", "mean"),
                 mean_B_MODALMATCH=("B_MODALMATCH", "mean"),
                 mean_O_REACH=("O_REACH", "mean")).reset_index())
    P(side.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(side, "ends")
    P("")

    # ------------------------------------------------------------ ARM C: the partition
    P("-" * 100)
    P(f"ARM C — THE PARTITION.  Each output's KNOB swing against its OWN SEED swing "
      f"({len(SEED_LADDER)} streams).")
    P("-" * 100)
    names = list(OUTPUTS)
    seed_cell = odf[odf.knob == "K_SEED"]
    key = ["panel", "anchor", "ladder", "chooser"]

    def per_dec_range(df, col):
        g = df.groupby(key)[col]
        return (g.max() - g.min()).astype(float)

    seed_swing = {c: per_dec_range(seed_cell, c) for c in names}
    seed_mean = {c: float(np.nanmean(np.abs(seed_swing[c]))) for c in names}

    prows = []
    for kn, spec in KNOBS.items():
        sub = odf[odf.knob == kn]
        lo, hi = str(spec["ends"][0]), str(spec["ends"][1])
        for c in names:
            # endpoint swing, averaged over streams to take the seed out
            a = sub[sub.setting == lo].groupby(key)[c].mean()
            b = sub[sub.setting == hi].groupby(key)[c].mean()
            ends_sw = (b - a).abs().astype(float)
            # full-ladder range, per decision, averaged over streams
            mstream = sub.groupby(key + ["setting"])[c].mean()
            full_sw = (mstream.groupby(key).max() - mstream.groupby(key).min()).astype(float)
            exact_zero = bool(np.nanmax(np.abs(sub.groupby(key)[c].max()
                                               - sub.groupby(key)[c].min())) == 0.0)
            ss = seed_mean[c]
            em, fm = float(np.nanmean(ends_sw)), float(np.nanmean(full_sw))
            ratio = (fm / ss) if ss and np.isfinite(ss) and ss > 0 else np.nan
            if exact_zero:
                cellname = "1_STRUCTURALLY_FREE"
            elif not np.isfinite(ratio):
                cellname = "3_KNOB_DEPENDENT" if fm > 0 else "1_STRUCTURALLY_FREE"
            elif ratio > NOISE_MULT:
                cellname = "3_KNOB_DEPENDENT"
            else:
                cellname = "2_NOISE_BOUND"
            prows.append(dict(knob=kn, output=c, declared_class=OUTPUTS[c][0],
                              mean_ends_swing=em, max_ends_swing=float(np.nanmax(ends_sw)),
                              mean_full_swing=fm, max_full_swing=float(np.nanmax(full_sw)),
                              n_decisions_moving=int((full_sw > 0).sum()),
                              seed_swing=ss, ratio_knob_over_seed=ratio,
                              exact_bitwise_invariant=exact_zero, cell=cellname))
    pdf = pd.DataFrame(prows)
    dump(pdf, "partition")

    P("  headline view: KNOB = K_DRAW, OUTPUT SET = OS_CORE")
    hv = pdf[(pdf.knob == K_HEAD) & (pdf.output.isin(OS_CORE))]
    P(hv[["output", "declared_class", "mean_full_swing", "seed_swing",
          "ratio_knob_over_seed", "n_decisions_moving", "cell"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("  the full 4 x 18 cell map (rows = output, cols = knob):")
    cmap = pdf.pivot(index="output", columns="knob", values="cell").loc[names]
    cmap.insert(0, "class", [OUTPUTS[c][0] for c in names])
    P(cmap.to_string())
    dump(cmap.reset_index(), "cellmap")
    P("")
    rmap = pdf.pivot(index="output", columns="knob", values="ratio_knob_over_seed").loc[names]
    P("  the same map as RATIOS (knob swing / own seed swing; bar = "
      f"{NOISE_MULT}):")
    P(rmap.to_string(float_format=lambda x: f"{x:.3f}"))
    dump(rmap.reset_index(), "ratios")
    P("")

    # ---- the hypotheses, as declared
    obs_all_free = bool((pdf[pdf.declared_class == "OBS"].cell == "1_STRUCTURALLY_FREE").all())
    hyp("H_OBSFREE", "the 5 OBS outputs are bit-identical across every knob and setting",
        f"{int((pdf[pdf.declared_class == 'OBS'].cell == '1_STRUCTURALLY_FREE').sum())} of "
        f"{len(pdf[pdf.declared_class == 'OBS'])} OBS (knob, output) cells structurally free",
        obs_all_free)
    bar_cells = pdf[pdf.declared_class == "BAR"]
    n_bar_dep = int((bar_cells.cell == "3_KNOB_DEPENDENT").sum())
    line_whole = obs_all_free and n_bar_dep == len(bar_cells)
    hyp("H_LINE", "every BAR output is cell 3 on EVERY knob and every OBS output cell 1 "
                  "(the queue's prediction)",
        f"{n_bar_dep} of {len(bar_cells)} BAR (knob, output) cells are knob-dependent; "
        f"OBS all free = {obs_all_free}", line_whole)
    spec_tbl = (bar_cells.assign(dep=bar_cells.cell == "3_KNOB_DEPENDENT")
                .groupby("output").dep.agg(["sum", "size"]).reset_index())
    spec_tbl["knob_specific"] = (spec_tbl["sum"] > 0) & (spec_tbl["sum"] < spec_tbl["size"])
    specific = spec_tbl[spec_tbl.knob_specific].output.tolist()
    hyp("H_SPECIFIC", "at least one BAR output is KNOB-SPECIFIC (free of one knob, dependent "
                      "on another) — the direct negation of H_LINE",
        f"{len(specific)} of {len(spec_tbl)} BAR outputs are knob-specific: "
        f"{specific if specific else '(none)'}", len(specific) > 0)
    dump(spec_tbl.rename(columns={"sum": "n_knobs_dependent", "size": "n_knobs"}), "specificity")
    P("")

    # ---- dial grid: both dials, all 12 combinations
    P("  DIAL GRID — every (KNOB x OUTPUT SET) combination, the verdict read off each:")
    grows = []
    for kn in KNOBNAMES:
        for osn, oset in OUTPUT_SETS.items():
            sub = pdf[(pdf.knob == kn) & (pdf.output.isin(oset))]
            bar = sub[sub.declared_class == "BAR"]
            obs = sub[sub.declared_class == "OBS"]
            grows.append(dict(
                knob=kn, output_set=osn, n_outputs=len(sub),
                n_obs_free=int((obs.cell == "1_STRUCTURALLY_FREE").sum()), n_obs=len(obs),
                n_bar_free=int((bar.cell == "1_STRUCTURALLY_FREE").sum()),
                n_bar_noise_bound=int((bar.cell == "2_NOISE_BOUND").sum()),
                n_bar_dependent=int((bar.cell == "3_KNOB_DEPENDENT").sum()), n_bar=len(bar),
                median_ratio=float(np.nanmedian(bar.ratio_knob_over_seed)),
                LINE_HOLDS=bool((obs.cell == "1_STRUCTURALLY_FREE").all()
                                and (bar.cell == "3_KNOB_DEPENDENT").all())))
    gdf = pd.DataFrame(grows)
    P(gdf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(gdf, "dialgrid")
    P(f"  the line holds in {int(gdf.LINE_HOLDS.sum())} of {len(gdf)} dial combinations.")
    P("")

    # ------------------------------------------------------------ ARM D: the census
    P("-" * 100)
    P("ARM D — CENSUS.  Does the record's committed prose STATE the knob its number is keyed to?")
    P("-" * 100)
    cdf, n_units, n_md = census()
    dump(cdf, "census")
    P(f"  {n_units:,} text units scanned ({n_md} .md files + LEADERBOARD rows + CHANGELOG paras); "
      f"{len(cdf):,} mention at least one of the 18 outputs.")
    bar_units = cdf[cdf.side.isin(["BAR_ONLY", "MIXED"])]
    verd = bar_units[bar_units.CARRIES_VERDICT]
    P(f"  {len(bar_units):,} touch a BAR output; {len(verd):,} of those carry a VERDICT word.")
    krows = []
    for kn in KNOBNAMES:
        col = f"k_{kn}"
        krows.append(dict(knob=kn, n_bar_units=len(bar_units),
                          n_stating=int(bar_units[col].sum()),
                          share_stating=float(bar_units[col].mean()),
                          n_verdict_units=len(verd), n_verdict_stating=int(verd[col].sum()),
                          share_verdict_stating=float(verd[col].mean())))
    kdf = pd.DataFrame(krows)
    P(kdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(kdf, "knobcensus")
    stated_any = verd[[f"k_{k}" for k in KNOBNAMES]].any(axis=1)
    P(f"  of the {len(verd):,} BAR-touching verdict units, {int(stated_any.sum()):,} state ANY "
      f"knob and {int((~stated_any).sum()):,} state NONE.")
    P(f"  L is stated in {int(verd.STATES_L.sum()):,} of them — i.e. the record's habit is to "
      "name L (or nothing) and")
    P("  leave the other three knobs implicit, which is only safe where the line IS the whole story.")
    P("")

    # ------------------------------------------------------------ ARM E: rule 8 + KEEP paths
    P("-" * 100)
    P("ARM E — RULE 8 WALK-FORWARD + BOTH KEEP PATHS.  Every pick made on warm-up..2016-12-31")
    P("        ONLY; 2017-2026 read once.  10 bps, next-day execution, 260-row warm-up.")
    P("-" * 100)
    live, spyb = {}, {}
    for pn in PANELS:
        pan = pans[pn]
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        lr = b["returns"].values
        live[pn] = blocks_m(lr, pan.warm, pan.ins, pan.oos)
        spyb[pn] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        P(f"  {pn:<6s} LIVE v2  full {live[pn]['CAGR']:>7.2%} / {live[pn]['Sharpe']:>6.4f} / "
          f"{live[pn]['MaxDD']:>7.2%}   OOS {live[pn]['OOS_CAGR']:>7.2%} / "
          f"{live[pn]['OOS_Sharpe']:>6.4f} / {live[pn]['OOS_MaxDD']:>7.2%}")
        P(f"  {pn:<6s} SPY      full {spyb[pn]['CAGR']:>7.2%} / {spyb[pn]['Sharpe']:>6.4f} / "
          f"{spyb[pn]['MaxDD']:>7.2%}   OOS {spyb[pn]['OOS_CAGR']:>7.2%} / "
          f"{spyb[pn]['OOS_Sharpe']:>6.4f} / {spyb[pn]['OOS_MaxDD']:>7.2%}")
    gate("G7", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]) < 0.05)

    wrows = []
    for pn in PANELS:
        pan = pans[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                for rg, r in LB[(pn, an, lad)].items():
                    m = blocks_m(r, pan.warm, pan.ins, pan.oos)
                    l4a, l4b = legs_4a(m, live[pn]), legs_4b(m, spyb[pn])
                    l4o = legs_4b_oos(m, spyb[pn])
                    wrows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rg),
                                      selector="RUNG_BOOK", knob="-", setting="-", **m,
                                      **l4a, **l4b, **l4o, pass4a=all(l4a.values()),
                                      pass4b_full=all(l4b.values()),
                                      pass4b_oos=all(l4o.values()),
                                      pass4b_both=all(l4b.values()) and all(l4o.values())))

    def policy_rows(name, keep_fn, src, kn, setting):
        """Act on the IS argmax pick only when the named gate says so, else stay at the anchor.
        Nothing here reads 2017-2026; the gate is an IS object at a named knob setting."""
        for (pn, an, lad, ch) in DEC:
            if ch != "CH_ISSHARPE":
                continue
            pan = pans[pn]
            R, obs, j, oout, rungs = pre[(pn, an, lad, ch)]
            row = src[(src.panel == pn) & (src.anchor == an) & (src.ladder == lad)
                      & (src.chooser == ch)]
            if len(row) != 1:
                raise AssertionError(f"{name}: {len(row)} rows for {(pn, an, lad, ch)}")
            row = row.iloc[0]
            use = rungs[j] if keep_fn(row) else ANCHORS[an][lad]
            r = LB[(pn, an, lad)][use]
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            l4a, l4b = legs_4a(m, live[pn]), legs_4b(m, spyb[pn])
            l4o = legs_4b_oos(m, spyb[pn])
            wrows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(use), selector=name,
                              knob=kn, setting=str(setting), **m, **l4a, **l4b, **l4o,
                              pass4a=all(l4a.values()), pass4b_full=all(l4b.values()),
                              pass4b_oos=all(l4o.values()),
                              pass4b_both=all(l4b.values()) and all(l4o.values())))

    frozen_src = froz
    policy_rows("SEL_ALLPICKS", lambda r: True, frozen_src, "-", "-")
    policy_rows("SEL_REACH_knobfree", lambda r: r.O_REACH > 0.5, frozen_src, "-", "-")
    fs_sh = frozen_src[frozen_src.chooser == "CH_ISSHARPE"]
    med_marg = float(np.nanmedian(fs_sh.O_MARGIN))
    policy_rows("SEL_MARGIN_knobfree", lambda r: r.O_MARGIN >= med_marg, frozen_src, "-", "-")
    med_gr = float(np.nanmedian(fs_sh.O_GAPRATIO))
    policy_rows("SEL_GAPRATIO_knobfree", lambda r: r.O_GAPRATIO >= med_gr, frozen_src, "-", "-")
    for kn, spec in KNOBS.items():
        for setting in spec["ladder"]:
            sub = odf[(odf.knob == kn) & (odf.setting == str(setting))
                      & (odf.chooser == "CH_ISSHARPE")]
            sub = sub[sub.stream == (setting if kn == "K_SEED" else SEED_REPS[0])]
            if len(sub) != 24:
                raise AssertionError(f"{kn}/{setting}: {len(sub)} rows, expected 24")
            policy_rows(f"SEL_RESOLVED_{kn}_{setting}", lambda r: r.B_RESOLVED > 0.5,
                        sub, kn, setting)
            policy_rows(f"SEL_GAPEXCEEDS_{kn}_{setting}", lambda r: r.B_GAPEXCEEDS > 0.5,
                        sub, kn, setting)
            policy_rows(f"SEL_PCTRANK_{kn}_{setting}", lambda r: r.B_PCTRANK >= 0.5,
                        sub, kn, setting)
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")
    P(f"  rule-8 rows: {len(wdf)}   4a passes {int(wdf.pass4a.sum())}   "
      f"4b full {int(wdf.pass4b_full.sum())}   4b OOS {int(wdf.pass4b_oos.sum())}   "
      f"4b BOTH {int(wdf.pass4b_both.sum())}")
    rb = wdf[wdf.selector == "RUNG_BOOK"]
    P(f"  of the {len(rb)} rung books: 4a {int(rb.pass4a.sum())}, 4b full "
      f"{int(rb.pass4b_full.sum())}, 4b BOTH {int(rb.pass4b_both.sum())}")
    P("  4b legs, failure counts over the rung books (which leg binds):")
    for lg in ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]:
        P(f"    {lg:<7s} fails {int((~rb[lg]).sum()):>4d} of {len(rb)}")
    if wdf.pass4b_both.any():
        w = wdf[wdf.pass4b_both]
        k2 = (w.OOS_CAGR.round(10).astype(str) + "|" + w.OOS_Sharpe.round(10).astype(str))
        P(f"  the {len(w)} 4b-BOTH rows collapse to {k2.nunique()} DISTINCT realised books.")
        best = w.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  best: {best.panel} {best.ladder}={best.rung} anchor {best.anchor} "
          f"[{best.selector}]  full {best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}   "
          f"OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}")
        P(f"        vs {best.panel} SPY OOS {spyb[best.panel]['OOS_CAGR']:.2%} / "
          f"{spyb[best.panel]['OOS_Sharpe']:.4f} / {spyb[best.panel]['OOS_MaxDD']:.2%}"
          f"   vs LIVE v2 OOS {live[best.panel]['OOS_CAGR']:.2%} / "
          f"{live[best.panel]['OOS_Sharpe']:.4f} / {live[best.panel]['OOS_MaxDD']:.2%}")
    sel = (wdf[wdf.selector != "RUNG_BOOK"].groupby(["selector", "knob"], sort=False)
           .agg(n=("OOS_Sharpe", "size"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                mean_full_Sharpe=("Sharpe", "mean"), n4a=("pass4a", "sum"),
                n4b=("pass4b_both", "sum")).reset_index())
    sel["gate_class"] = np.where(sel.selector.str.contains("knobfree"), "OBS_KNOB_FREE",
                                 np.where(sel.selector == "SEL_ALLPICKS", "NO_GATE",
                                          "BAR_KNOB_KEYED"))
    P("  does the OBSERVED / BAR split move MONEY, or only the word?")
    P(sel.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(sel, "money")
    obs_best = float(sel[sel.gate_class == "OBS_KNOB_FREE"].mean_OOS_Sharpe.max())
    bar_best = float(sel[sel.gate_class == "BAR_KNOB_KEYED"].mean_OOS_Sharpe.max())
    bar_worst = float(sel[sel.gate_class == "BAR_KNOB_KEYED"].mean_OOS_Sharpe.min())
    nog = float(sel.loc[sel.selector == "SEL_ALLPICKS", "mean_OOS_Sharpe"].iloc[0])
    P(f"  best OBS (knob-free) gate {obs_best:.4f} vs best BAR (knob-keyed) gate {bar_best:.4f} "
      f"(worst {bar_worst:.4f}) vs no gate {nog:.4f}")
    hyp("H_MONEY", "a knob-free OBSERVED gate buys at least as much OOS Sharpe as the best "
                   "knob-keyed BAR gate",
        f"OBS {obs_best:.4f} vs BAR {bar_best:.4f} (no gate {nog:.4f})", obs_best >= bar_best)
    P(f"  the SPREAD a knob choice alone opens inside one gate family, in OOS Sharpe:")
    fam = (sel[sel.gate_class == "BAR_KNOB_KEYED"]
           .assign(family=lambda d: d.selector.str.extract(r"^(SEL_[A-Z]+)_")[0])
           .groupby(["family", "knob"]).mean_OOS_Sharpe.agg(["min", "max", "size"]).reset_index())
    fam["spread"] = fam["max"] - fam["min"]
    P(fam.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(fam, "knobspread")
    a = wdf[wdf.selector == "SEL_ALLPICKS"].sort_values(["panel", "anchor", "ladder"])
    bsel = sel.loc[sel.gate_class == "OBS_KNOB_FREE"].sort_values("mean_OOS_Sharpe").iloc[-1].selector
    bb2 = wdf[wdf.selector == bsel].sort_values(["panel", "anchor", "ladder"])
    d = bb2.OOS_Sharpe.values - a.OOS_Sharpe.values
    tt = float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))) if d.std(ddof=1) > 0 else np.nan
    P(f"  paired delta of {bsel} over SEL_ALLPICKS: {d.mean():+.4f} mean OOS Sharpe "
      f"(t {tt:+.2f}, n {len(d)})")
    P("")

    # ------------------------------------------------------------ verdict
    P("=" * 100)
    n_fail = sum(1 for g in GATES if not g["pass_"])
    P(f"GATES: {len(GATES) - n_fail}/{len(GATES)} pass")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hypotheses.csv", index=False)
    P(f"ANSWER: the OBSERVED/BAR line is {'THE WHOLE STORY' if line_whole else 'NOT the whole story'}"
      f" — {len(specific)} of {len(spec_tbl)} BAR outputs are KNOB-SPECIFIC.")
    P("VERDICT: KILL (capital) — no new book; the deliverable is the PARTITION plus the "
      "knob-spread price.")
    P(f"runtime {time.time() - t0:.0f}s")
    P("=" * 100)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
