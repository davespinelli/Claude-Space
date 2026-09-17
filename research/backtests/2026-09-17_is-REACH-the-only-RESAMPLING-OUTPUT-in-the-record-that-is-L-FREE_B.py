#!/usr/bin/env python3
"""Idea 1242 (lane B, 2026-09-17)
   is-REACH-the-only-RESAMPLING-OUTPUT-in-the-record-that-is-L-FREE

THE QUEUE'S PREMISE, QUOTED.  Idea 1208 found reach (IS argmax rung == anchor rung) reads
exactly 14 of 72 at ALL TWELVE L rungs including the degenerate L = T, because it is an
IS-OBSERVED fact and only the BAR moves with L, while the resolution rate over the same 72
decisions swings 0.1528 -> 1.0000 on that ladder.  The queue asks for the census: take the
record's other committed resample-derived OUTPUTS (P_boot, q95 bars, null medians,
recentred ranges, B_BOOT95, percentile ranks) and partition them into OBSERVED facts and
BAR facts, and publish the partition.

WHAT THIS RUN ADDS, BECAUSE THE QUEUE'S TWO-CELL PARTITION IS NOT MEASURABLE AS STATED.

  An OBSERVED output can be shown L-free by EXACT equality: the function never touches the
  draws, so its value is bit-identical at every rung.  A BAR output CANNOT be tested that
  way, because different L means different DRAWS, so an output that does not depend on L at
  all still moves from Monte-Carlo noise alone.  Exact inequality would therefore convict
  every bar output by construction and prove nothing.

  So this run measures each output's L SWING against its own SEED SWING: the same output,
  same 72 decisions, same B, at the record's frozen L = 63 across 8 rng streams.  An output
  whose L swing is inside its own seed swing is L-free UP TO THE PRECISION THE RECORD BUYS
  ITSELF; one whose L swing is a multiple of it is L-dependent in fact.  That makes the
  partition THREE cells, not two:
      (1) STRUCTURALLY L-FREE     exact bitwise invariance across all 12 rungs
      (2) BAR-SIDE, NOISE-BOUND   moves, but no more than its own seed noise
      (3) BAR-SIDE, L-DEPENDENT   L swing a declared multiple of seed swing
  The bar for cell 3 is declared BEFORE measuring: L_swing / SEED_swing > 2.0.

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `OUTPUT SET`   {OS_CORE, OS_WIDE, OS_ALL}     OS_CORE = the six outputs the queue names
                 plus reach; OS_WIDE = OS_CORE plus the bar-side outputs the record also
                 publishes (P_max, modal rung, bootstrap SD, gap-exceeds, resolved, q05);
                 OS_ALL = OS_WIDE plus the observed-side outputs published beside them
                 (pick, margin, level, gap ratio).
  `L RUNG PAIR`  {LP_REC, LP_NEAR, LP_EXTREME}  the pair the sensitivity verdict is read
                 off: LP_REC = (21, 252) (1154's own endpoints), LP_NEAR = (42, 126) (the
                 rungs either side of the record's frozen 63), LP_EXTREME = (1, T).

  = 9 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`; every output at every one of the
  12 L rungs is published per decision in `.outputs.csv` and per output in `.partition.csv`.
  The headline uses OS_CORE and LP_REC.  Nothing is ever selected on the L ladder -- it is
  the object under measurement.

  PANEL {U56, B136, SMALL} x ANCHOR {A, B} x LADDER {N, H, GROSS, CADENCE} x CHOOSER
  {CH_ISSHARPE, CH_ISCAGR, CH_ISDD} = 1208's SAME 72 decisions, all built at every rung.
  SEED is not a dial: it is the noise yardstick, swept across 8 streams at L = 63 only.

FROZEN at 1096/1101/1154/1208's construction: CAND20 legs, max_vol 0.60, min hold from the
H ladder, cadence from the CADENCE ladder, 10 bps (rule 2), LAG 1, warm-up 260, IS end
2016-12-31, bar 0.90, B = 1000 draws, crc32 seeds, DD cap 0.60, CAGR floor 0.70.  The
bootstrap is 1208's own moving-block redraw with 1208's own seeds and chunking, so P_pick
replays 1208's `.ladder.csv` BIT FOR BIT -- gate G4 checks all 864 rows against the
committed artefact rather than asserting it.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the current
constituents of a sub-$2B screen (data/SMALL_PANEL_README.md).  Every LEVEL here -- CAGR,
MaxDD, Sharpe and every null built on them -- is optimistic, and a resample null prices
SAMPLING error on the tape it is handed and cannot correct that.  It largely cancels out of
the headline, which is a RATIO of one construction against itself on the same tape (the
same 72 decisions at different L and different seeds), and it does NOT cancel out of the 4b
legs, so any pass there is an upper bound.

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

DATE = "2026-09-17"
SLUG = "is-REACH-the-only-RESAMPLING-OUTPUT-in-the-record-that-is-L-FREE"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
REF_1208 = (Path(__file__).resolve().parent /
            "2026-09-17_is-the-BLOCK-LENGTH-the-record-s-LARGEST-UNSTATED-DIAL-across-"
            "every-RESAMPLING-claim_B.ladder.csv")

# ------------------------------------------------------------------ 1101/1208 construction
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
BDRAWS = 1000
SEED_BASE = 12081208
LL_FULL = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008]
L_ALL = LL_FULL + ["T"]
L_HEAD = 63
SEED_LADDER = [0, 1, 2, 3, 4, 5, 6, 7]
NOISE_MULT = 2.0                      # DECLARED BEFORE MEASURING (cell-3 bar)

# ------------------------------------------------------------------ dial 1: output sets
#  class: OBS = computed from the observed IS path alone, draws never touched
#         BAR = a functional of the resample law
OUTPUTS = {
    # the six the queue names, plus reach
    "O_REACH":      ("OBS", "bool",  "IS argmax rung == anchor rung"),
    "B_PPICK":      ("BAR", "float", "P_boot that the observed argmax is the draw argmax"),
    "B_Q95":        ("BAR", "float", "95th percentile of the pick rung's null statistic"),
    "B_NULLMED":    ("BAR", "float", "median of the pick rung's null statistic"),
    "B_RECRANGE":   ("BAR", "float", "recentred null range q95-q05 of the pick rung"),
    "B_BOOT95":     ("BAR", "float", "95th percentile of the draw top-minus-second gap"),
    "B_PCTRANK":    ("BAR", "float", "percentile rank of the observed level in its own draws"),
    # OS_WIDE adds the other bar-side outputs the record publishes
    "B_PMAX":       ("BAR", "float", "largest P_boot over rungs"),
    "B_MODALRUNG":  ("BAR", "int",   "index of the modal draw argmax"),
    "B_MODALMATCH": ("BAR", "bool",  "observed argmax IS the modal draw argmax"),
    "B_SD":         ("BAR", "float", "bootstrap SD of the pick rung's statistic"),
    "B_GAPEXCEEDS": ("BAR", "bool",  "observed margin exceeds B_BOOT95"),
    "B_RESOLVED":   ("BAR", "bool",  "P_pick >= 0.90 (the record's decisive bar)"),
    "B_Q05":        ("BAR", "float", "5th percentile of the pick rung's null statistic"),
    # OS_ALL adds the observed-side outputs published beside them
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

# ------------------------------------------------------------------ dial 2: L rung pairs
L_PAIRS = {"LP_REC": (21, 252), "LP_NEAR": (42, 126), "LP_EXTREME": (1, "T")}
LP_HEAD = "LP_REC"

# ------------------------------------------------------------------ record's own numbers
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
A1208_REACH = 14
A1208_RATES = {1: 0.152778, 21: 0.194444, 63: 0.222222, 252: 0.277778, 1008: 0.472222}
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
    """Reuse this script's OWN deterministic artefact if it is already on disk (delete the
    .csv to force a rebuild).  Same construction, same seeds, same numbers either way."""
    p = Path(f"{OUT}.{suffix}.csv")
    if p.exists():
        df = pd.read_csv(p)
        if "L" in df.columns:
            df["L"] = df.L.map(lambda v: "T" if str(v) == "T" else int(float(v)))
        P(f"  reused {p.name}  ({len(df):,} rows) — deterministic artefact already on disk")
        return df
    df = builder()
    dump(df, suffix)
    return df


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<6s} {'PASS' if ok else 'FAIL'}  {what:<66s} {value:.3e}")
    return bool(ok)


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<16s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


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


# ================================================================== 1208's block bootstrap
def block_index(rng, T, L, B):
    """(B, T) moving-block index; blocks with replacement, no wrap (1101's construction)."""
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def draw_stats(R, stat, L, seed, B=BDRAWS, chunk=100):
    """(B, k) statistic per draw.  Identical rng consumption to 1208's pboot_argmax, so
    P_boot derived here replays 1208's committed ladder bit for bit."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    parts, done = [], 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]
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
    """The OBSERVED-side outputs: no draw is touched, so these cannot move with L."""
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
    """Every BAR-side output, all from the SAME (B, k) draw matrix."""
    am = D.argmax(axis=1)
    Pv = np.bincount(am, minlength=D.shape[1]) / D.shape[0]
    col = D[:, j]
    colf = col[np.isfinite(col)]                 # -inf draws are kept for the argmax (1208's
    if colf.size == 0:                           # construction) but excluded from the levels
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


# ================================================================== ARM A: the census
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
        rows.append(dict(src=src, n_chars=len(txt),
                         n_outputs=sum(hits.values()),
                         n_obs=len(obs_h), n_bar=len(bar_h),
                         side=("OBS_ONLY" if bar_h == [] else
                               ("BAR_ONLY" if obs_h == [] else "MIXED")),
                         STATES_L=bool(ls), L_STATED=ls[0] if ls else 0,
                         CARRIES_VERDICT=bool(VERDICTTOK.search(txt)),
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
    P(f"IDEA 1242 (lane B, {DATE}) — is REACH the only RESAMPLING OUTPUT in the record that is L-FREE?")
    P("=" * 100)
    P("  dial 1 = OUTPUT SET  {OS_CORE, OS_WIDE, OS_ALL}          (headline OS_CORE)")
    P("  dial 2 = L RUNG PAIR {LP_REC, LP_NEAR, LP_EXTREME}       (headline LP_REC = (21, 252))")
    P("  NOT dials: 1208's same 72 decisions (3 panels x 2 anchors x 4 ladders x 3 choosers),")
    P("             all 12 L rungs, B = 1000, q = 0.90.  SEED is the NOISE YARDSTICK (8 streams")
    P(f"             at L = {L_HEAD}), and the cell-3 bar L_swing/SEED_swing > {NOISE_MULT} is DECLARED HERE.")
    P("")

    # ------------------------------------------------------------ ARM 0: data-free
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What makes an output L-free before any tape is read.")
    P("-" * 100)
    cls = pd.DataFrame([dict(output=k, declared_class=v[0], kind=v[1], definition=v[2],
                             in_OS_CORE=k in OS_CORE, in_OS_WIDE=k in OS_WIDE)
                        for k, v in OUTPUTS.items()])
    P(cls.to_string(index=False))
    dump(cls, "classes")
    P("  The OBS rows take the observed IS path and nothing else; the draws are not an argument")
    P("  of the function, so their value is bit-identical at every L.  The BAR rows are")
    P("  functionals of the resample law, so different L means different DRAWS and they move")
    P("  even where they do not depend on L.  That is why cell 2 exists and why the yardstick is")
    P("  the SEED swing, not zero.")
    # mechanical proof on a synthetic tape: same function, two very different L
    rng = np.random.default_rng(1242)
    Rs = rng.normal(0.0004, 0.01, size=(1200, 6))
    obs_s = np.array([fsharpe(Rs[:, i]) for i in range(6)])
    j_s, o_s = observed_outputs(obs_s, list(range(6)), 3)
    d5 = draw_stats(Rs, "CH_ISSHARPE", 5, 99, B=400)
    d500 = draw_stats(Rs, "CH_ISSHARPE", 500, 99, B=400)
    b5, b500 = bar_outputs(d5, obs_s, j_s), bar_outputs(d500, obs_s, j_s)
    j2, o2 = observed_outputs(obs_s, list(range(6)), 3)
    obs_dev = max(abs(o_s[k] - o2[k]) for k in o_s if np.isfinite(o_s[k]))
    gate("G1", "OBS outputs bit-identical when L changes on a synthetic tape (max dev)",
         obs_dev, obs_dev == 0.0)
    bar_dev = max(abs(b5[k] - b500[k]) for k in b5)
    gate("G2", "BAR outputs DO move on that same synthetic tape (max dev > 0)",
         bar_dev, bar_dev > 0.0)
    ii = block_index(np.random.default_rng(1), 500, 500, 64)
    gate("G3", "L=T joint redraw is the identity (max |idx - arange|)",
         float(np.abs(ii - np.arange(500)[None, :]).max()),
         np.abs(ii - np.arange(500)).max() == 0)
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
    gate("G4a", "U56 anchor A full Sharpe replays 1101/1208's 1.139701",
         abs(m["Sharpe"] - A1101_TRIPLE[1]), abs(m["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)
    P("")

    # ------------------------------------------------------------ ARM B: every output, every L
    P("-" * 100)
    P("ARM B — EVERY OUTPUT AT EVERY L RUNG, ON 1208's SAME 72 DECISIONS.")
    P("-" * 100)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    P(f"  decisions: {len(DEC)}   x {len(L_ALL)} L rungs x {len(OUTPUTS)} outputs")
    pre = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        j, oout = observed_outputs(obs, rungs, ANCHORS[an][lad])
        pre[(pn, an, lad, ch)] = (R, obs, j, oout, rungs)

    def build_outputs():
        rows = []
        for (pn, an, lad, ch) in DEC:
            R, obs, j, oout, rungs = pre[(pn, an, lad, ch)]
            for L in L_ALL:
                Lv = R.shape[0] if L == "T" else int(L)
                D = draw_stats(R, ch, Lv, seed_of(pn, an, lad, ch, L), B=BDRAWS)
                rows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, k=len(rungs),
                                 L=("T" if L == "T" else L), L_eff=Lv,
                                 pick=str(rungs[j]), **oout, **bar_outputs(D, obs, j)))
        return pd.DataFrame(rows)

    odf = cached("outputs", build_outputs)
    P(f"  ({time.time() - t0:.0f}s)")

    # cross-check against 1208's committed artefact, row by row
    if REF_1208.exists():
        ref = pd.read_csv(REF_1208)
        ref["L"] = ref.L.astype(str)
        mine = odf.copy()
        mine["L"] = mine.L.astype(str)
        mg = ref.merge(mine, on=["panel", "anchor", "ladder", "chooser", "L"],
                       suffixes=("_r", "_m"))
        dev = float(np.abs(mg.P_pick - mg.B_PPICK).max())
        gate("G4", f"P_boot replays 1208's committed ladder on all {len(mg)} rows (max dev)",
             dev, dev == 0.0 and len(mg) == len(ref))
        rdev = float(np.abs(mg.is_anchor.astype(float) - mg.O_REACH).max())
        gate("G5", "reach replays 1208's is_anchor on every row (max dev)", rdev, rdev == 0.0)
    else:
        gate("G4", "1208's committed ladder.csv present for the row-by-row replay", 0.0, False)
    reach_by_L = odf.groupby("L", sort=False).O_REACH.sum()
    gate("G6", f"reach = {A1208_REACH} of 72 at EVERY L rung incl. L=T (max |dev|)",
         float(np.abs(reach_by_L - A1208_REACH).max()),
         bool((reach_by_L == A1208_REACH).all()))
    rate_by_L = odf.groupby("L", sort=False).B_RESOLVED.mean()
    for L, v in A1208_RATES.items():
        got = float(rate_by_L.loc[L])
        gate(f"G7_{L}", f"1208's resolution rate at L={L} ({v:.4f}) replays", abs(got - v),
             abs(got - v) < 1e-6)
    gate("G8", "L=T resolves all 72 by construction (rate)", float(rate_by_L.loc["T"]),
         float(rate_by_L.loc["T"]) == 1.0)
    P("")
    P("  the two ends of the queue's premise, side by side, over the SAME 72 decisions:")
    side = pd.DataFrame(dict(L=rate_by_L.index, reach=reach_by_L.values,
                             resolution_rate=rate_by_L.values,
                             mean_P_pick=odf.groupby("L", sort=False).B_PPICK.mean().values,
                             mean_B_BOOT95=odf.groupby("L", sort=False).B_BOOT95.mean().values,
                             mean_B_PCTRANK=odf.groupby("L", sort=False).B_PCTRANK.mean().values))
    P(side.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(side, "ends")
    P("")

    # ------------------------------------------------------------ the SEED yardstick
    P("-" * 100)
    P(f"ARM C — THE NOISE YARDSTICK.  Every output recomputed at L = {L_HEAD} on {len(SEED_LADDER)} rng streams.")
    P("-" * 100)
    def build_seedsweep():
        srows = []
        for sd in SEED_LADDER:
            for (pn, an, lad, ch) in DEC:
                R, obs, j, oout, rungs = pre[(pn, an, lad, ch)]
                D = draw_stats(R, ch, L_HEAD, seed_of("SEED", sd, pn, an, lad, ch), B=BDRAWS)
                srows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, seed=sd,
                                  **oout, **bar_outputs(D, obs, j)))
        return pd.DataFrame(srows)

    sdf = cached("seedsweep", build_seedsweep)
    P(f"  ({time.time() - t0:.0f}s)")

    KEY = ["panel", "anchor", "ladder", "chooser"]

    def swing_table(df, names):
        """Per-decision max-min of each output over `group_col`, then the ACROSS-DECISION mean."""
        out = {}
        for nm in names:
            g = df.groupby(KEY)[nm]
            sw = (g.max() - g.min())
            scale = df.groupby(KEY)[nm].apply(lambda s: np.nanmedian(np.abs(s)))
            rel = sw / scale.replace(0.0, np.nan)
            out[nm] = dict(mean_abs_swing=float(np.nanmean(sw)),
                           max_abs_swing=float(np.nanmax(sw)),
                           n_decisions_moving=int((sw > 0).sum()),
                           mean_rel_swing=float(np.nanmean(rel)))
        return pd.DataFrame(out).T.reset_index().rename(columns={"index": "output"})

    full = odf[odf.L.isin(LL_FULL)]
    names = list(OUTPUTS)
    sw_L = swing_table(full, names).add_suffix("_L").rename(columns={"output_L": "output"})
    sw_T = swing_table(odf, names).add_suffix("_LT").rename(columns={"output_LT": "output"})
    sw_S = swing_table(sdf, names).add_suffix("_S").rename(columns={"output_S": "output"})
    part = sw_L.merge(sw_T, on="output").merge(sw_S, on="output")
    part["declared_class"] = part.output.map(lambda k: OUTPUTS[k][0])
    part["ratio_L_over_SEED"] = part.mean_abs_swing_L / part.mean_abs_swing_S.replace(0.0, np.nan)
    part["decisions_moving_L"] = part.n_decisions_moving_L.astype(int)
    part["decisions_moving_SEED"] = part.n_decisions_moving_S.astype(int)

    def cell(r):
        if r.mean_abs_swing_LT == 0.0 and r.n_decisions_moving_LT == 0:
            return "1_STRUCTURALLY_L_FREE"
        if not np.isfinite(r.ratio_L_over_SEED):
            # seed swing exactly 0 while L moves it: L-dependent, not noise
            return "3_BAR_L_DEPENDENT" if r.mean_abs_swing_L > 0 else "2_BAR_NOISE_BOUND"
        return "3_BAR_L_DEPENDENT" if r.ratio_L_over_SEED > NOISE_MULT else "2_BAR_NOISE_BOUND"

    part["cell"] = part.apply(cell, axis=1)
    part = part.sort_values(["cell", "ratio_L_over_SEED"], ascending=[True, False])
    show = part[["output", "declared_class", "cell", "mean_abs_swing_L", "mean_abs_swing_S",
                 "ratio_L_over_SEED", "decisions_moving_L", "decisions_moving_SEED",
                 "mean_abs_swing_LT", "n_decisions_moving_LT"]]
    P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(part, "partition")
    P("")
    c1 = list(part[part.cell == "1_STRUCTURALLY_L_FREE"].output)
    c2 = list(part[part.cell == "2_BAR_NOISE_BOUND"].output)
    c3 = list(part[part.cell == "3_BAR_L_DEPENDENT"].output)
    P(f"  CELL 1 structurally L-free ({len(c1)}): {c1}")
    P(f"  CELL 2 bar-side, noise-bound ({len(c2)}): {c2}")
    P(f"  CELL 3 bar-side, L-dependent ({len(c3)}): {c3}")
    hyp("H_UNIQUE", "reach is the ONLY L-free output in the record",
        f"cell 1 holds {len(c1)} outputs: {c1}", len(c1) == 1 and c1 == ["O_REACH"])
    hyp("H_CLASS", "cell 1 is exactly the OBS-declared class and nothing else",
        f"cell1={sorted(c1)} vs OBS={sorted(k for k,v in OUTPUTS.items() if v[0]=='OBS')}",
        sorted(c1) == sorted(k for k, v in OUTPUTS.items() if v[0] == "OBS"))
    hyp("H_ALLBAR", "every BAR-side output is L-dependent beyond its own seed noise",
        f"{len(c3)} of {len([k for k,v in OUTPUTS.items() if v[0]=='BAR'])} BAR outputs in cell 3; "
        f"noise-bound: {c2}", len(c2) == 0)
    P("")

    # ------------------------------------------------------------ dial grid
    P("-" * 100)
    P("DIAL GRID — all 9 cells (OUTPUT SET x L RUNG PAIR), each one published.")
    P("-" * 100)
    grid = []
    for osn, oset in OUTPUT_SETS.items():
        for lpn, (la, lb) in L_PAIRS.items():
            A = odf[odf.L.astype(str) == str(la)].set_index(KEY)
            Bv = odf[odf.L.astype(str) == str(lb)].set_index(KEY)
            n_free, n_dep, movers = 0, 0, {}
            for nm in oset:
                d = (A[nm] - Bv[nm]).abs()
                nmov = int((d > 0).sum())
                movers[nm] = nmov
                sref = float(part.loc[part.output == nm, "mean_abs_swing_S"].iloc[0])
                mean_d = float(np.nanmean(d))
                dep = (mean_d > NOISE_MULT * sref) if sref > 0 else (nmov > 0)
                n_dep += int(dep)
                n_free += int(not dep)
            grid.append(dict(output_set=osn, L_pair=lpn, pair=f"({la},{lb})",
                             n_outputs=len(oset), n_L_FREE=n_free, n_L_DEPENDENT=n_dep,
                             frac_L_free=n_free / len(oset),
                             L_free_outputs=";".join(
                                 nm for nm in oset if movers[nm] == 0)))
    gdf = pd.DataFrame(grid)
    P(gdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(gdf, "dialgrid")
    hd = gdf[(gdf.output_set == OS_HEAD) & (gdf.L_pair == LP_HEAD)].iloc[0]
    P(f"  HEADLINE ({OS_HEAD} / {LP_HEAD}): {hd.n_L_FREE} of {hd.n_outputs} outputs L-free; "
      f"exactly invariant: {hd.L_free_outputs}")
    P("")

    # ------------------------------------------------------------ ARM D: the census
    P("-" * 100)
    P("ARM D — CENSUS.  How the record's committed sentences SPLIT across the partition.")
    P("-" * 100)
    cdf, n_units, n_md = census()
    P(f"  corpus: {n_units:,} committed text units over LEADERBOARD.md + CHANGELOG.md + {n_md} .md files;"
      f" {len(cdf):,} name at least one of the {len(OUTPUTS)} outputs.")
    crows = []
    for osn, oset in OUTPUT_SETS.items():
        cols = [f"h_{k}" for k in oset]
        sub = cdf[cdf[cols].any(axis=1)].copy()
        barcols = [f"h_{k}" for k in oset if OUTPUTS[k][0] == "BAR"]
        obscols = [f"h_{k}" for k in oset if OUTPUTS[k][0] == "OBS"]
        hasbar = sub[barcols].any(axis=1) if barcols else pd.Series(False, index=sub.index)
        hasobs = sub[obscols].any(axis=1) if obscols else pd.Series(False, index=sub.index)
        vs = sub[sub.CARRIES_VERDICT]
        vbar = vs[barcols].any(axis=1) if barcols else pd.Series(False, index=vs.index)
        crows.append(dict(output_set=osn, n_units=len(sub),
                          OBS_ONLY=int((hasobs & ~hasbar).sum()),
                          BAR_ANY=int(hasbar.sum()),
                          MIXED=int((hasobs & hasbar).sum()),
                          n_with_verdict=len(vs),
                          verdict_BAR_ANY=int(vbar.sum()),
                          verdict_BAR_no_L=int((vbar & ~vs.STATES_L).sum()),
                          verdict_OBS_ONLY=int((~vbar).sum()),
                          frac_verdict_needing_L=float(vbar.mean()) if len(vs) else np.nan,
                          states_L=int(sub.STATES_L.sum()),
                          frac_states_L=float(sub.STATES_L.mean()) if len(sub) else np.nan))
    cendf = pd.DataFrame(crows)
    P(cendf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(cdf, "census_units")
    dump(cendf, "census")
    per = []
    for k in OUTPUTS:
        sub = cdf[cdf[f"h_{k}"]]
        per.append(dict(output=k, declared_class=OUTPUTS[k][0],
                        cell=str(part.loc[part.output == k, "cell"].iloc[0]),
                        n_units=len(sub),
                        n_with_verdict=int(sub.CARRIES_VERDICT.sum()),
                        n_states_L=int(sub.STATES_L.sum()),
                        frac_states_L=float(sub.STATES_L.mean()) if len(sub) else np.nan))
    perdf = pd.DataFrame(per).sort_values("n_units", ascending=False)
    P(perdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(perdf, "per_output_census")
    hc = cendf[cendf.output_set == OS_HEAD].iloc[0]
    P(f"  HEADLINE ({OS_HEAD}): of {int(hc.n_with_verdict)} verdict-carrying units naming one of")
    P(f"  these outputs, {int(hc.verdict_BAR_ANY)} ({hc.frac_verdict_needing_L:.4f}) name a BAR-side")
    P(f"  output and so NEED an L; {int(hc.verdict_BAR_no_L)} of those state none. "
      f"{int(hc.verdict_OBS_ONLY)} rest on OBSERVED outputs only and need no L at all.")
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
    gate("G9", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
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
                                      selector="RUNG_BOOK", **m, **l4a, **l4b, **l4o,
                                      pass4a=all(l4a.values()),
                                      pass4b_full=all(l4b.values()),
                                      pass4b_oos=all(l4o.values()),
                                      pass4b_both=all(l4b.values()) and all(l4o.values())))

    # the gate policies: act on the IS argmax pick only when the named output says so.
    # OBSERVED gates are L-free by construction; BAR gates carry an L.
    def policy_rows(name, keep_fn, src):
        for (pn, an, lad, ch) in DEC:
            if ch != "CH_ISSHARPE":
                continue
            pan = pans[pn]
            R, obs, j, oout, rungs = pre[(pn, an, lad, ch)]
            row = src[(src.panel == pn) & (src.anchor == an) & (src.ladder == lad)
                      & (src.chooser == ch)]
            if len(row) != 1:
                raise AssertionError(f"{name}: {len(row)} rows for {(pn,an,lad,ch)}")
            row = row.iloc[0]
            use = rungs[j] if keep_fn(row) else ANCHORS[an][lad]
            r = LB[(pn, an, lad)][use]
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            l4a, l4b = legs_4a(m, live[pn]), legs_4b(m, spyb[pn])
            l4o = legs_4b_oos(m, spyb[pn])
            wrows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(use),
                              selector=name, **m, **l4a, **l4b, **l4o,
                              pass4a=all(l4a.values()), pass4b_full=all(l4b.values()),
                              pass4b_oos=all(l4o.values()),
                              pass4b_both=all(l4b.values()) and all(l4o.values())))

    base63 = odf[odf.L == L_HEAD]
    policy_rows("SEL_ALLPICKS", lambda r: True, base63)
    policy_rows("SEL_REACH_obsfree", lambda r: r.O_REACH > 0.5, base63)
    # observed-side gate with one bar: the IS margin clears its own cross-decision median,
    # computed on IS decisions only (no OOS data touched)
    med_marg = float(np.nanmedian(base63[base63.chooser == "CH_ISSHARPE"].O_MARGIN))
    policy_rows("SEL_MARGIN_obsfree", lambda r: r.O_MARGIN >= med_marg, base63)
    med_gr = float(np.nanmedian(base63[base63.chooser == "CH_ISSHARPE"].O_GAPRATIO))
    policy_rows("SEL_GAPRATIO_obsfree", lambda r: r.O_GAPRATIO >= med_gr, base63)
    for L in L_ALL:
        sub = odf[odf.L.astype(str) == str(L)]
        policy_rows(f"SEL_RESOLVED_L{L}", lambda r: r.B_RESOLVED > 0.5, sub)
        policy_rows(f"SEL_GAPEXCEEDS_L{L}", lambda r: r.B_GAPEXCEEDS > 0.5, sub)
        policy_rows(f"SEL_PCTRANK_L{L}", lambda r: r.B_PCTRANK >= 0.5, sub)
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")
    P(f"  rule-8 rows: {len(wdf)}   4a passes {int(wdf.pass4a.sum())}   "
      f"4b full {int(wdf.pass4b_full.sum())}   4b OOS {int(wdf.pass4b_oos.sum())}   "
      f"4b BOTH {int(wdf.pass4b_both.sum())}")
    rb = wdf[wdf.selector == "RUNG_BOOK"]
    P(f"  of the {len(rb)} rung books: 4a {int(rb.pass4a.sum())}, 4b full "
      f"{int(rb.pass4b_full.sum())}, 4b BOTH {int(rb.pass4b_both.sum())}")
    if wdf.pass4b_both.any():
        w = wdf[wdf.pass4b_both]
        key = (w.OOS_CAGR.round(10).astype(str) + "|" + w.OOS_Sharpe.round(10).astype(str))
        P(f"  the {len(w)} 4b-BOTH rows collapse to {key.nunique()} DISTINCT realised books.")
        best = w.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  best: {best.panel} {best.ladder}={best.rung} anchor {best.anchor} "
          f"[{best.selector}]  full {best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}   "
          f"OOS {best.OOS_CAGR:.2%} / {best.OOS_Sharpe:.4f} / {best.OOS_MaxDD:.2%}")
        P(f"        vs {best.panel} SPY OOS {spyb[best.panel]['OOS_CAGR']:.2%} / "
          f"{spyb[best.panel]['OOS_Sharpe']:.4f} / {spyb[best.panel]['OOS_MaxDD']:.2%}"
          f"   vs LIVE v2 OOS {live[best.panel]['OOS_CAGR']:.2%} / "
          f"{live[best.panel]['OOS_Sharpe']:.4f} / {live[best.panel]['OOS_MaxDD']:.2%}")
    sel = (wdf[wdf.selector != "RUNG_BOOK"].groupby("selector", sort=False)
           .agg(n=("OOS_Sharpe", "size"), mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                mean_OOS_CAGR=("OOS_CAGR", "mean"), mean_OOS_MaxDD=("OOS_MaxDD", "mean"),
                mean_full_Sharpe=("Sharpe", "mean"),
                n4a=("pass4a", "sum"), n4b=("pass4b_both", "sum")).reset_index())
    sel["gate_class"] = np.where(sel.selector.str.contains("obsfree"), "OBS_L_FREE",
                                 np.where(sel.selector == "SEL_ALLPICKS", "NO_GATE", "BAR_L_KEYED"))
    P("  does the OBSERVED / BAR split move MONEY, or only the word?")
    P(sel.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(sel, "money")
    obs_best = sel[sel.gate_class == "OBS_L_FREE"].mean_OOS_Sharpe.max()
    bar_best = sel[sel.gate_class == "BAR_L_KEYED"].mean_OOS_Sharpe.max()
    nog = float(sel.loc[sel.selector == "SEL_ALLPICKS", "mean_OOS_Sharpe"].iloc[0])
    P(f"  best OBS (L-free) gate {obs_best:.4f} vs best BAR (L-keyed) gate {bar_best:.4f} "
      f"vs no gate {nog:.4f}")
    hyp("H_MONEY", "an L-free OBSERVED gate buys at least as much OOS Sharpe as the best "
                   "L-keyed BAR gate",
        f"OBS {obs_best:.4f} vs BAR {bar_best:.4f} (no gate {nog:.4f})", obs_best >= bar_best)
    # t-stat on the best OBS gate vs no gate, paired across decisions
    a = wdf[wdf.selector == "SEL_ALLPICKS"].sort_values(["panel", "anchor", "ladder"])
    bsel = sel.loc[sel.gate_class == "OBS_L_FREE"].sort_values("mean_OOS_Sharpe").iloc[-1].selector
    bb = wdf[wdf.selector == bsel].sort_values(["panel", "anchor", "ladder"])
    d = bb.OOS_Sharpe.values - a.OOS_Sharpe.values
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
    P("VERDICT: KILL (capital) — no new book; the deliverable is the PARTITION, a schema fact.")
    P(f"runtime {time.time() - t0:.0f}s")
    P("=" * 100)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
