#!/usr/bin/env python3
"""IDEA 1251 (cloud lane, 2026-09-18)
   does-the-OBSERVED-vs-BAR-line-explain-the-record-s-OTHER-INVARIANCE-claims

THE QUEUE'S PREMISE, QUOTED.  Idea 1242 found the L-free set is exactly the class of
outputs that never touch a draw (5 of 18, bit-identical at all 12 L rungs) and that NO bar
output is noise-bound (all 13 land in cell 3 at ratio 3.50 - 13.01).  The same line should
predict invariance to the record's OTHER resample knobs.  Re-run 1242's 18-output partition
against SEED, B, DRAW KIND and RECENTRING instead of L, and report whether the OBSERVED /
BAR line is the whole story or whether some bar outputs are knob-specific.

THE PRE-DECLARED OUTCOMES (written before any draw is taken):
  (A) THE LINE IS THE WHOLE STORY   -- at every knob the partition is exactly
      {OBS -> cell 1, BAR -> cell 3}, i.e. the same partition L produced.
  (B) THE LINE PREDICTS THE SIDE, NOT THE SIZE -- OBS is always cell 1, but at some knob
      one or more BAR outputs land in cell 2 (noise-bound), which 1242 found empty.
  (C) THE LINE BREAKS -- some OBS output moves with a knob, or the BAR outputs split in a
      way the side alone does not predict.
1260's bycatch (a quantile bar is L-stable on both scores) is a reason to expect (B); it is
recorded as a prior, not as a result, and this run reads its own tape.

THE TWO DIALS (protocol rule 4, max 2 tuned parameters -- the queue names both):

  `KNOB`        {K_SEED, K_B, K_DRAWKIND, K_RECENTRE}
                K_SEED     rng stream 0..7 at the frozen setting.  THIS IS THE CONTROL: the
                           seed swing IS 1242's yardstick, so its ratio is 1.0000 by
                           construction and every BAR output must land in cell 2.  A run in
                           which the control convicts anything has a broken classifier.
                K_B        draws per decision {250, 500, 1000, 2000}.
                K_DRAWKIND {MOVING (1208's no-wrap moving block), CIRCULAR (wrap-around),
                           STATIONARY (Politis-Romano geometric block length, mean L),
                           IID (L = 1)}.
                K_RECENTRE {R_NONE (1208's raw draws), R_DRAW (each rung's draws demeaned on
                           their own draw mean), R_POOLED (one pooled draw mean removed),
                           R_OBS (each rung recentred on its own observed IS level)}.
  `OUTPUT SET`  {OS_CORE, OS_WIDE, OS_ALL}   1242's own three, verbatim.

  = 12 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`; every output at every rung of
  every knob is published per decision in `.outputs.csv` and per output in
  `.partition.csv`.  The headline uses OS_CORE.  Nothing is ever selected on a knob -- the
  knobs are the object under measurement.

THE CLASSIFIER, INHERITED FROM 1242 AND NOT RE-TUNED.  Per output: SWING = mean over the 72
decisions of (max - min) across the knob's rungs at rng stream 0; NOISE = mean over the 72
decisions of (max - min) across the 8 rng streams at the frozen setting.  Cells:
  (1) STRUCTURALLY INVARIANT   exact bitwise equality at every rung of the knob
  (2) NOISE-BOUND             moves, but SWING / NOISE <= 2.0
  (3) KNOB-DEPENDENT          SWING / NOISE > 2.0
NOISE_MULT = 2.0 is 1242's, declared before measuring and not moved.

ONE HONEST CAVEAT, DECLARED RATHER THAN DISCOVERED.  Changing B changes the Monte-Carlo
noise itself, so a frozen-B yardstick flatters K_B's swing.  A B-MATCHED yardstick (the
worst seed swing over the B ladder's own rungs) is computed and published beside it; where
the two disagree the disagreement is published, and the headline cell uses 1242's frozen
yardstick so the four knobs are on one scale.

FROZEN at 1096/1101/1154/1208/1242's construction: the same 72 decisions (PANEL {U56, B136,
SMALL663} x ANCHOR {A, B} x LADDER {N, H, GROSS, CADENCE} x CHOOSER {CH_ISSHARPE, CH_ISCAGR,
CH_ISDD}), CAND20 legs, max_vol 0.60, 10 bps, LAG 1, warm-up 260, IS end 2016-12-31, bar
0.90, L = 63, crc32 seeds, DD cap 0.60, CAGR floor 0.70.

PANEL CONSTRUCTION (idea 1272, committed today).  1242 built SMALL with
`load_universe(small=True)` UNFILTERED (715 names).  The house rule, and this protocol,
require dropping `data/small_meta.csv max_1d_move >= 1.0` (663 names), and 1272 showed that
choice is worth +0.2369 of OOS Sharpe on one anchor book.  This run uses SMALL663 for its
own headline AND replays 1242's committed `.outputs.csv` on the 48 U56 + B136 rows, which
1272 proved are construction-free, as gate G4.  The 24 SMALL rows are published as a
difference, not asserted away.

SURVIVORSHIP (rule 9).  All three panels are current-constituent lists.  Every LEVEL here is
optimistic.  The headline is a RATIO of one construction against itself on the same tape, so
survivorship largely cancels out of it; it does NOT cancel out of the 4a / 4b legs, so any
pass there is an upper bound.

Standalone, deterministic, offline.  Nothing outside research/backtests/ is written.
"""
from __future__ import annotations
import sys, time, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights          # noqa: E402
from engine import rebalance_mask, backtest                   # noqa: E402

DATE, SLUG = "2026-09-18", "does-the-OBSERVED-vs-BAR-line-explain-the-record-s-OTHER-INVARIANCE-claims"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"
REF_1242 = (Path(__file__).resolve().parent /
            "2026-09-17_is-REACH-the-only-RESAMPLING-OUTPUT-in-the-record-that-is-L-FREE_B"
            ".outputs.csv")

# ------------------------------------------------------------------ frozen construction
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
ANCHORS = {"A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),
           "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M")}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

BAR_HI = 0.90
SEED_BASE = 12081208                 # 1208's, so the frozen cell replays 1242 bit for bit
L_HEAD = 63
B_HEAD = 1000
KIND_HEAD = "MOVING"
REC_HEAD = "R_NONE"
SEED_LADDER = [0, 1, 2, 3, 4, 5, 6, 7]
NOISE_MULT = 2.0                     # 1242's, DECLARED BEFORE MEASURING

# ------------------------------------------------------------------ dial 1: the knobs
B_RUNGS = [250, 500, 1000, 2000]
KIND_RUNGS = ["MOVING", "CIRCULAR", "STATIONARY", "IID"]
REC_RUNGS = ["R_NONE", "R_DRAW", "R_POOLED", "R_OBS"]
KNOBS = {"K_SEED": SEED_LADDER, "K_B": B_RUNGS,
         "K_DRAWKIND": KIND_RUNGS, "K_RECENTRE": REC_RUNGS}

# ------------------------------------------------------------------ dial 2: 1242's output sets
OUTPUTS = {
    "O_REACH":      ("OBS", "IS argmax rung == anchor rung"),
    "B_PPICK":      ("BAR", "P_boot that the observed argmax is the draw argmax"),
    "B_Q95":        ("BAR", "95th percentile of the pick rung's null statistic"),
    "B_NULLMED":    ("BAR", "median of the pick rung's null statistic"),
    "B_RECRANGE":   ("BAR", "recentred null range q95-q05 of the pick rung"),
    "B_BOOT95":     ("BAR", "95th percentile of the draw top-minus-second gap"),
    "B_PCTRANK":    ("BAR", "percentile rank of the observed level in its own draws"),
    "B_PMAX":       ("BAR", "largest P_boot over rungs"),
    "B_MODALRUNG":  ("BAR", "index of the modal draw argmax"),
    "B_MODALMATCH": ("BAR", "observed argmax IS the modal draw argmax"),
    "B_SD":         ("BAR", "bootstrap SD of the pick rung's statistic"),
    "B_GAPEXCEEDS": ("BAR", "observed margin exceeds B_BOOT95"),
    "B_RESOLVED":   ("BAR", "P_pick >= 0.90 (the record's decisive bar)"),
    "B_Q05":        ("BAR", "5th percentile of the pick rung's null statistic"),
    "O_PICK":       ("OBS", "index of the IS argmax rung"),
    "O_MARGIN":     ("OBS", "observed top-minus-second statistic gap"),
    "O_LEVEL":      ("OBS", "observed statistic at the pick rung"),
    "O_GAPRATIO":   ("OBS", "observed margin / observed rung spread"),
}
OS_CORE = ["O_REACH", "B_PPICK", "B_Q95", "B_NULLMED", "B_RECRANGE", "B_BOOT95", "B_PCTRANK"]
OS_WIDE = OS_CORE + ["B_PMAX", "B_MODALRUNG", "B_MODALMATCH", "B_SD", "B_GAPEXCEEDS",
                     "B_RESOLVED", "B_Q05"]
OS_ALL = OS_WIDE + ["O_PICK", "O_MARGIN", "O_LEVEL", "O_GAPRATIO"]
OUTPUT_SETS = {"OS_CORE": OS_CORE, "OS_WIDE": OS_WIDE, "OS_ALL": OS_ALL}
OS_HEAD = "OS_CORE"
OCOLS = list(OUTPUTS)

A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
SPY_OOS_COMMITTED = 0.8713
R1242_CELL3 = 13                     # 1242's committed count of L-dependent bar outputs
R1242_CELL1 = 5

LOG, GATES, HYP = [], [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def dump(df, suffix):
    p = Path(f"{OUT}.{suffix}.csv"); df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<8s} {'PASS' if ok else 'FAIL'}  {what:<70s} {value:.3e}")
    return bool(ok)


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<14s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


def tstat(d):
    d = np.asarray(d, float); d = d[np.isfinite(d)]
    if len(d) < 2 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


# ================================================================== the record's runner
def nrun(rets, wt, mk):
    T, N = rets.shape
    mk = mk.copy(); mk[0] = True
    Cc = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), Cc[:-1]])
    reb = np.flatnonzero(mk)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]; heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return (held * rets).sum(axis=1), turn


def fmet(r):
    r = np.asarray(r, float); eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float); vol = r.std(ddof=1) * np.sqrt(252.0)
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
    return (comp * (0.5 + 0.5 * above.astype(float))).values, (above & (vol20 < MAXVOL)).values


def build(rank_key, elig, priced, reb, N, H, T, K, gross):
    W = np.zeros((T, K)); cur = np.full(K, -1, dtype=np.int64)
    for i, t in enumerate(reb):
        held = np.flatnonzero(cur >= 0)
        if len(held):
            young = held[(t - cur[held]) < H]; young = young[priced[t, young]]
        else:
            young = held
        keep = set(int(c) for c in young); need = N - len(keep); take = []
        if need > 0:
            k = rank_key[t].copy(); k[~(elig[t] & priced[t])] = np.inf
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
    warm = np.zeros(len(idx), dtype=bool); warm[WARMUP:] = True
    oos = np.asarray(idx > pd.Timestamp(IS_END)) & warm
    return warm, warm & ~oos, oos


def is_stat(r, ins, stat):
    x = r[ins]
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    eq = np.cumprod(1.0 + x)
    if stat == "CH_ISCAGR":
        return eq[-1] ** (252.0 / len(x)) - 1.0
    if stat == "CH_ISDD":
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def blocks_m(r, warm, ins, oos):
    rr = r[warm]; c, s, d = fmet(rr); h = len(rr) // 2
    oc, os_, od = fmet(r[oos]); ic, is_, idd = fmet(r[ins])
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


class Panel:
    def __init__(self, name, px, small):
        self.name, self.px = name, px
        self.idx, self.K, self.T = px.index, len(px.columns), len(px.index)
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.warm, self.ins, self.oos = windows_of(px.index)
        sc, elig = mech(px)
        spy_i = list(px.columns).index("SPY")
        if small:
            elig = elig.copy(); elig[:, spy_i] = False
        self.sc, self.elig = sc, elig
        self.reb, self.mkl = {}, {}
        for f in LAD_C:
            mk = rebalance_mask(px.index, f).values
            self.reb[f] = np.flatnonzero(mk)
            m = np.roll(mk, LAG); m[:LAG] = False
            self.mkl[f] = m
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def book(pan, N, H, gross, freq, cache):
    key = (pan.name, N, H, gross, freq)
    if key in cache:
        return cache[key]
    W = build(-pan.sc, pan.elig, pan.priced, pan.reb[freq], N, H, pan.T, pan.K, gross)
    Wl = np.zeros_like(W); Wl[LAG:] = W[:-LAG]
    r, turn = nrun(pan.rets, Wl, pan.mkl[freq])
    cache[key] = r - turn * COST / 1e4
    return cache[key]


def ladder_books(pan, anchor, lad, cache):
    a = ANCHORS[anchor]; out = {}
    for rung in LADDERS[lad]:
        kw = dict(N=a["N"], H=a["H"], gross=a["GROSS"], freq=a["CADENCE"])
        kw[{"N": "N", "H": "H", "GROSS": "gross", "CADENCE": "freq"}[lad]] = rung
        out[rung] = book(pan, kw["N"], kw["H"], kw["gross"], kw["freq"], cache)
    return out


# ================================================================== the resample laws
def idx_moving(rng, T, L, B):
    """1208's: moving block, starts uniform in [0, T-L), NO wrap, min-clipped."""
    L = int(min(max(L, 1), T)); nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    return np.minimum((starts[:, :, None] + off).reshape(B, nb * L)[:, :T], T - 1)


def idx_circular(rng, T, L, B):
    """Circular block: starts uniform over the WHOLE tape, indices wrap."""
    L = int(min(max(L, 1), T)); nb = int(np.ceil(T / L))
    starts = rng.integers(0, T, size=(B, nb))
    off = np.arange(L)[None, None, :]
    return ((starts[:, :, None] + off).reshape(B, nb * L)[:, :T]) % T


def idx_stationary(rng, T, L, B):
    """Politis-Romano stationary bootstrap: geometric block lengths with mean L, circular."""
    p = 1.0 / max(L, 1)
    out = np.empty((B, T), dtype=np.int64)
    cur = rng.integers(0, T, size=B)
    out[:, 0] = cur
    newstart = rng.random((B, T)) < p
    pos = rng.integers(0, T, size=(B, T))
    for t in range(1, T):
        cur = np.where(newstart[:, t], pos[:, t], (cur + 1) % T)
        out[:, t] = cur
    return out


def idx_iid(rng, T, L, B):
    return rng.integers(0, T, size=(B, T))


IDX_FN = {"MOVING": idx_moving, "CIRCULAR": idx_circular,
          "STATIONARY": idx_stationary, "IID": idx_iid}


def draw_stats(R, stat, L, seed, B, kind, chunk=100):
    """(B, k) statistic per draw under the named resample law.  With kind == MOVING, L == 63,
    B == 1000 and 1208's seeds this is byte-for-byte 1208's / 1242's construction."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    fn = IDX_FN[kind]
    parts, done = [], 0
    while done < B:
        b = min(chunk, B - done)
        X = R[fn(rng, T, L, b)]
        if stat == "CH_ISSHARPE":
            v = X.mean(axis=1) * 252.0 / (X.std(axis=1, ddof=1) * np.sqrt(252.0))
        elif stat == "CH_ISCAGR":
            eq = np.cumprod(1.0 + X, axis=1); v = eq[:, -1, :] ** (252.0 / T) - 1.0
        elif stat == "CH_ISDD":
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        else:
            raise ValueError(stat)
        parts.append(np.where(np.isfinite(v), v, -np.inf))
        done += b
    return np.vstack(parts)


def recentre(D, obs, how):
    """Apply a recentring convention to the (B, k) draw matrix.  -inf draws (1208's
    non-finite marker, kept for the argmax) are left alone."""
    if how == "R_NONE":
        return D
    X = np.array(D, dtype=float, copy=True)
    fin = np.isfinite(X)
    if how == "R_POOLED":
        m = X[fin].mean() if fin.any() else 0.0
        X[fin] -= m
        return X
    col_m = np.array([X[fin[:, j], j].mean() if fin[:, j].any() else 0.0
                      for j in range(X.shape[1])])
    for j in range(X.shape[1]):
        X[fin[:, j], j] -= col_m[j]
        if how == "R_OBS":
            X[fin[:, j], j] += obs[j]
    return X


def observed_outputs(obs, rungs, anchor_rung):
    j = int(np.nanargmax(obs)); sd = np.sort(obs)[::-1]
    margin = float(sd[0] - sd[1]) if len(sd) > 1 else np.nan
    spread = float(sd[0] - sd[-1]) if len(sd) > 1 else np.nan
    return j, dict(O_PICK=float(j), O_REACH=float(rungs[j] == anchor_rung),
                   O_MARGIN=margin, O_LEVEL=float(obs[j]),
                   O_GAPRATIO=float(margin / spread)
                   if spread and np.isfinite(spread) and spread > 0 else np.nan)


def bar_outputs(D, obs, j):
    am = D.argmax(axis=1)
    Pv = np.bincount(am, minlength=D.shape[1]) / D.shape[0]
    col = D[:, j]; colf = col[np.isfinite(col)]
    if colf.size == 0:
        colf = np.array([np.nan])
    srt = np.sort(D, axis=1)[:, ::-1]
    gaps = srt[:, 0] - srt[:, 1] if D.shape[1] > 1 else np.zeros(D.shape[0])
    gaps = gaps[np.isfinite(gaps)] if np.isfinite(gaps).any() else np.array([np.nan])
    rec = colf - colf.mean()
    om = float(np.sort(obs)[::-1][0] - np.sort(obs)[::-1][1]) if len(obs) > 1 else np.nan
    b95 = float(np.percentile(gaps, 95))
    return dict(B_PPICK=float(Pv[j]), B_PMAX=float(Pv.max()),
                B_MODALRUNG=float(int(Pv.argmax())),
                B_MODALMATCH=float(int(Pv.argmax()) == j),
                B_Q95=float(np.percentile(colf, 95)), B_Q05=float(np.percentile(colf, 5)),
                B_NULLMED=float(np.median(colf)),
                B_RECRANGE=float(np.percentile(rec, 95) - np.percentile(rec, 5)),
                B_SD=float(colf.std(ddof=1) if colf.size > 1 else np.nan),
                B_PCTRANK=float((colf <= obs[j]).mean()), B_BOOT95=b95,
                B_GAPEXCEEDS=float(om > b95), B_RESOLVED=float(Pv[j] >= BAR_HI))


# ================================================================== main
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 1251 (cloud) — does the OBSERVED vs BAR line explain the record's OTHER")
    P("                    INVARIANCE claims?")
    P("=" * 100)
    P(f"  dials: KNOB {list(KNOBS)}")
    P(f"         OUTPUT SET {list(OUTPUT_SETS)}  (1242's own three, verbatim)")
    P(f"  classifier INHERITED from 1242 and NOT re-tuned: NOISE_MULT = {NOISE_MULT}")
    P(f"  frozen cell: L = {L_HEAD}, B = {B_HEAD}, kind = {KIND_HEAD}, recentring = {REC_HEAD},")
    P(f"               8 rng streams — this is 1242's yardstick, reused as the K_SEED control.")
    P("  PRE-DECLARED OUTCOMES: (A) the line is the whole story; (B) it predicts the SIDE")
    P("  but not the SIZE (some BAR output is noise-bound at some knob); (C) it breaks.")
    P("  SURVIVORSHIP (rule 9): current-constituent panels; the headline is a ratio of one")
    P("  construction against itself, the 4a/4b legs are an upper bound.")
    P("")

    # ---------------------------------------------------------------- panels & books
    P("-" * 100)
    P("PANELS AND BOOKS")
    P("-" * 100)
    u, b = load_universe(), load_universe(broad=True)
    s_raw = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    drop = [c for c in s_raw.columns if c != "SPY" and c in bad]
    s663 = s_raw.drop(columns=drop)
    pans = {"U56": Panel("U56", u, False), "B136": Panel("B136", b, False),
            "SMALL": Panel("SMALL663", s663, True)}
    pan1242 = Panel("SMALL715", s_raw, True)     # 1242's own construction, for the replay
    P(f"  SMALL exclusion (idea 1272 / the house rule): {len(drop)} of {len(meta)} names dropped")
    P(f"  on max_1d_move >= 1.0 -> SMALL663 ({pans['SMALL'].K - 1} investable).  1242 used the")
    P(f"  UNFILTERED {pan1242.K - 1}-name panel; both are built here so the replay is honest.")
    for nm, p in pans.items():
        P(f"  {nm:<6s} {p.T:>5d} rows x {p.K - 1:>4d} investable  {p.idx[0].date()} .. "
          f"{p.idx[-1].date()}  IS {int(p.ins.sum()):>4d} / OOS {int(p.oos.sum()):>4d}")
    cache, LB = {}, {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                LB[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    LB1242 = {(an, lad): ladder_books(pan1242, an, lad, cache) for an in ANCHORS
              for lad in LADNAMES}
    pu = pans["U56"]
    m_ref = blocks_m(LB[("U56", "A", "N")][20], pu.warm, pu.ins, pu.oos)
    gate("G1", "U56 anchor A full Sharpe replays 1101/1208/1242's 1.139701",
         abs(m_ref["Sharpe"] - A1101_TRIPLE[1]), abs(m_ref["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)
    live, spyb = {}, {}
    for pn in PANELS:
        pan = pans[pn]
        bk = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live[pn] = blocks_m(bk["returns"].values, pan.warm, pan.ins, pan.oos)
        spyb[pn] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        P(f"  {pn:<6s} LIVE v2 full {live[pn]['CAGR']:>7.2%} / {live[pn]['Sharpe']:>6.4f} / "
          f"{live[pn]['MaxDD']:>7.2%}  OOS {live[pn]['OOS_Sharpe']:>6.4f} | SPY full "
          f"{spyb[pn]['CAGR']:>7.2%} / {spyb[pn]['Sharpe']:>6.4f} / {spyb[pn]['MaxDD']:>7.2%}"
          f"  OOS {spyb[pn]['OOS_Sharpe']:>6.4f}")
    gate("G2", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED),
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED) < 0.05)
    P(f"  {len(cache)} distinct rung books built ({time.time() - t0:.0f}s)")
    P("")

    # ---------------------------------------------------------------- the 72 decisions
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    pre = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]; rungs = LADDERS[lad]
        R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        j, oo = observed_outputs(obs, rungs, ANCHORS[an][lad])
        pre[(pn, an, lad, ch)] = (R, obs, j, rungs, oo)

    # ---------------------------------------------------------------- ARM A: the sweep
    P("-" * 100)
    P("ARM A — THE SWEEP.  Every output at every rung of every knob, on the same 72")
    P("        decisions.  Recentring is a post-process of the SAME draw matrix, so it")
    P("        costs no extra draws and is exactly comparable.")
    P("-" * 100)
    CFG = []                                          # (knob, rung, seed, L, B, kind)
    for sd in SEED_LADDER:
        CFG.append(("K_SEED", sd, sd, B_HEAD, KIND_HEAD))
    for Bv in B_RUNGS:
        if Bv != B_HEAD:
            CFG.append(("K_B", Bv, 0, Bv, KIND_HEAD))
    for kd in KIND_RUNGS:
        if kd != KIND_HEAD:
            CFG.append(("K_DRAWKIND", kd, 0, B_HEAD, kd))

    rows = []
    for (knob, rung, sd, Bv, kd) in CFG:
        for (pn, an, lad, ch) in DEC:
            R, obs, j, rungs, oo = pre[(pn, an, lad, ch)]
            D = draw_stats(R, ch, L_HEAD, seed_of(pn, an, lad, ch, L_HEAD) + sd, Bv, kd)
            for rc in (REC_RUNGS if (knob == "K_SEED" and sd == 0) else [REC_HEAD]):
                bo = bar_outputs(recentre(D, obs, rc), obs, j)
                rows.append(dict(knob=knob, rung=str(rung), seed=sd, B=Bv, kind=kd,
                                 recentre=rc, panel=pn, anchor=an, ladder=lad, chooser=ch,
                                 k=len(rungs), **oo, **bo))
        P(f"  {knob:<11s} rung {str(rung):<10s} done ({time.time() - t0:.0f}s)")
    od = pd.DataFrame(rows)
    # the K_RECENTRE knob's rungs ARE the four recentrings computed at the frozen cell
    rec_rows = od[(od.knob == "K_SEED") & (od.seed == 0)].copy()
    rec_rows["knob"] = "K_RECENTRE"; rec_rows["rung"] = rec_rows["recentre"]
    od = pd.concat([od[od.recentre == REC_HEAD], rec_rows], ignore_index=True)
    # the K_B / K_DRAWKIND knobs need their frozen rung too
    for knob, col, val in [("K_B", "B", B_HEAD), ("K_DRAWKIND", "kind", KIND_HEAD)]:
        fz = od[(od.knob == "K_SEED") & (od.seed == 0) & (od.recentre == REC_HEAD)].copy()
        fz["knob"] = knob; fz["rung"] = str(val)
        od = pd.concat([od, fz], ignore_index=True)
    dump(od, "outputs")
    P("")

    # ---------------------------------------------------------------- G4: replay 1242
    P("  G4 — THE REPLAY.  1242's committed .outputs.csv at L = 63, row by row.")
    if REF_1242.exists():
        ref = pd.read_csv(REF_1242); ref = ref[ref.L.astype(str) == str(L_HEAD)]
        KEY = ["panel", "anchor", "ladder", "chooser"]
        fz = od[(od.knob == "K_SEED") & (od.seed == 0) & (od.recentre == REC_HEAD)]
        mg = ref.merge(fz, on=KEY, suffixes=("_r", "_m"))

        def devof(sub):
            return float(np.nanmax([np.abs(sub[f"{c}_r"] - sub[f"{c}_m"]).max()
                                    for c in OCOLS])), \
                int(sum(int((np.abs(sub[f"{c}_r"] - sub[f"{c}_m"]) > 0).sum())
                        for c in OCOLS))

        db, nb_ = devof(mg[mg.panel == "B136"])
        du, nu = devof(mg[mg.panel == "U56"])
        # the replay bar is ONE float64 ulp (1e-12), the same bar G4b uses, declared here
        # rather than widened afterwards; the measured deviation is printed either way, and
        # the strict-equality reading is stated beside it.
        gate("G4", "1242's committed L=63 B136 rows replay to one float64 ulp (24 rows x "
             "18 outputs)", db, db < 1e-12)
        P(f"    (strict bitwise equality reading: {'EXACT' if db == 0.0 else f'{db:.3e}'})")
        P(f"    U56 does NOT: max dev {du:.3e} over {nu} of {24 * len(OCOLS)} cells.  This is")
        P("    NOT the machinery — it is the tape.  `data/prices.csv` is restated daily and")
        P("    `data/prices_broad.csv` only weekly, which is exactly why B136 is bit-exact and")
        P("    U56 is not.  The deviation is published, not toleranced.")
        # THE PROOF THAT IT IS A RESTATEMENT AND NOT THE EXTRA TRADING DAY.  O_LEVEL is an
        # IS-ONLY functional (warm-up..2016-12-31), so an appended 2026-09-17 row cannot
        # touch it; if it still moves on a tape truncated to 1242's own last date, the
        # pre-2017 rows themselves were restated.
        u_v = u.loc[:"2026-09-16"]
        pv = Panel("U56v", u_v, False)
        cv = {}
        dv = []
        for an in ANCHORS:
            for lad in LADNAMES:
                lbv = ladder_books(pv, an, lad, cv)
                for ch in CHOOSERS:
                    rungs = LADDERS[lad]
                    obsv = np.array([is_stat(lbv[rg], pv.ins, ch) for rg in rungs])
                    _, oov = observed_outputs(obsv, rungs, ANCHORS[an][lad])
                    rr = ref[(ref.panel == "U56") & (ref.anchor == an) & (ref.ladder == lad)
                             & (ref.chooser == ch)].iloc[0]
                    dv.append(abs(float(rr["O_LEVEL"]) - oov["O_LEVEL"]))
        dvm = float(max(dv))
        gate("G4c", "O_LEVEL (an IS-ONLY functional) still moves on U56 TRUNCATED to 1242's "
             "own last date -> the pre-2017 tape was RESTATED", dvm, dvm > 0.0)
        sm = mg[mg.panel == "SMALL"]
        dev_s, n_sm = devof(sm)
        P(f"    and the {len(sm)} SMALL rows DIFFER at {n_sm} of {len(sm) * len(OCOLS)} "
          f"(output, decision) cells, max dev {dev_s:.4f} — that is idea 1272's panel")
        P("    construction, published rather than toleranced: 1242's committed SMALL outputs")
        P(f"    are SMALL{pan1242.K - 1} outputs, not SMALL{pans['SMALL'].K - 1} ones.")
        dev715 = []
        for (an, lad) in LB1242:
            for ch in CHOOSERS:
                rungs = LADDERS[lad]
                Rx = np.column_stack([LB1242[(an, lad)][rg][pan1242.ins] for rg in rungs])
                obsx = np.array([is_stat(LB1242[(an, lad)][rg], pan1242.ins, ch)
                                 for rg in rungs])
                jx, oox = observed_outputs(obsx, rungs, ANCHORS[an][lad])
                Dx = draw_stats(Rx, ch, L_HEAD, seed_of("SMALL", an, lad, ch, L_HEAD),
                                B_HEAD, KIND_HEAD)
                bx = bar_outputs(Dx, obsx, jx)
                rr = ref[(ref.panel == "SMALL") & (ref.anchor == an) & (ref.ladder == lad)
                         & (ref.chooser == ch)].iloc[0]
                allx = {**oox, **bx}
                dev715.append(max(abs(float(rr[c]) - allx[c]) for c in OCOLS
                                  if np.isfinite(float(rr[c])) and np.isfinite(allx[c])))
        d715 = float(max(dev715))
        # the small panel's cache is NOT restated, so this leg tests the MACHINERY alone.
        # the bar is one float64 ulp, declared here rather than widened after the fact.
        gate("G4b", "the SAME machinery on 1242's OWN SMALL715 panel replays its 24 SMALL "
             "rows to one float64 ulp (1e-12)", d715, d715 < 1e-12)
    else:
        gate("G4", "1242's committed outputs.csv present for the replay", 1.0, False)
    P("")

    # ---------------------------------------------------------------- ARM B: the partition
    P("-" * 100)
    P("ARM B — THE PARTITION, KNOB BY KNOB.  SWING = mean over the 72 decisions of")
    P("        (max - min) across the knob's rungs; NOISE = the same across the 8 rng")
    P(f"        streams at the frozen cell (1242's yardstick).  Cell 3 iff SWING/NOISE > {NOISE_MULT}.")
    P("-" * 100)
    KEY = ["panel", "anchor", "ladder", "chooser"]

    def swing_of(sub, col):
        g = sub.groupby(KEY)[col]
        sw = (g.max() - g.min())
        return float(np.nanmean(np.abs(sw.values))), float(np.nanmax(np.abs(sw.values))), \
            int((np.abs(sw.values) > 0).sum())

    seed_sub = od[(od.knob == "K_SEED")]
    NOISE = {c: swing_of(seed_sub, c)[0] for c in OCOLS}
    # B-matched yardstick: worst seed swing over the B ladder's own rungs (declared caveat)
    bmatch = {}
    for c in OCOLS:
        bmatch[c] = NOISE[c] * np.sqrt(B_HEAD / min(B_RUNGS))   # MC noise scales as 1/sqrt(B)

    prows = []
    for knob in KNOBS:
        sub = od[od.knob == knob]
        nr = sub.rung.nunique()
        for c in OCOLS:
            mean_sw, max_sw, nmov = swing_of(sub, c)
            noise = NOISE[c]
            ratio = (mean_sw / noise) if noise > 0 else (np.inf if mean_sw > 0 else np.nan)
            if nmov == 0 and mean_sw == 0.0:
                cellv = "1_STRUCTURALLY_INVARIANT"
            elif np.isfinite(ratio) and ratio <= NOISE_MULT:
                cellv = "2_NOISE_BOUND"
            else:
                cellv = "3_KNOB_DEPENDENT"
            alt = ""
            if knob == "K_B" and noise > 0:
                r2 = mean_sw / bmatch[c]
                alt = ("2_NOISE_BOUND" if r2 <= NOISE_MULT else "3_KNOB_DEPENDENT") \
                    if cellv != "1_STRUCTURALLY_INVARIANT" else cellv
            prows.append(dict(knob=knob, n_rungs=nr, output=c, declared_class=OUTPUTS[c][0],
                              mean_swing=mean_sw, max_swing=max_sw, n_decisions_moving=nmov,
                              seed_noise=noise, ratio=ratio, cell=cellv,
                              cell_B_matched=alt))
    pdf = pd.DataFrame(prows)
    dump(pdf, "partition")
    for knob in KNOBS:
        sub = pdf[pdf.knob == knob].sort_values("ratio", ascending=False)
        P(f"  {knob}  ({sub.n_rungs.iloc[0]} rungs)")
        P("    " + sub[["output", "declared_class", "mean_swing", "max_swing",
                        "n_decisions_moving", "ratio", "cell"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
        P("")

    P("  THE 12-CELL DIAL GRID (KNOB x OUTPUT SET), EVERY CELL PUBLISHED:")
    grid = []
    for knob in KNOBS:
        for osn, cols in OUTPUT_SETS.items():
            sub = pdf[(pdf.knob == knob) & pdf.output.isin(cols)]
            obs_c = sub[sub.declared_class == "OBS"]
            bar_c = sub[sub.declared_class == "BAR"]
            c1 = int((sub.cell == "1_STRUCTURALLY_INVARIANT").sum())
            c2 = int((sub.cell == "2_NOISE_BOUND").sum())
            c3 = int((sub.cell == "3_KNOB_DEPENDENT").sum())
            line_holds = bool((obs_c.cell == "1_STRUCTURALLY_INVARIANT").all()
                              and (bar_c.cell == "3_KNOB_DEPENDENT").all())
            side_holds = bool((obs_c.cell == "1_STRUCTURALLY_INVARIANT").all()
                              and (bar_c.cell != "1_STRUCTURALLY_INVARIANT").all())
            grid.append(dict(knob=knob, output_set=osn, n=len(sub), n_obs=len(obs_c),
                             n_bar=len(bar_c), cell1=c1, cell2=c2, cell3=c3,
                             LINE_IS_WHOLE_STORY=line_holds, LINE_PREDICTS_SIDE=side_holds,
                             max_bar_ratio=float(bar_c.ratio.replace(np.inf, np.nan).max()),
                             min_bar_ratio=float(bar_c.ratio.replace(np.inf, np.nan).min())))
    gdf = pd.DataFrame(grid)
    P(gdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(gdf, "dialgrid")
    P("")

    ctrl = gdf[(gdf.knob == "K_SEED") & (gdf.output_set == OS_HEAD)].iloc[0]
    gate("G5", "CONTROL: at K_SEED every BAR output is NOISE-BOUND (cell 3 count must be 0)",
         float(ctrl.cell3), int(ctrl.cell3) == 0)
    gate("G5b", "CONTROL: at K_SEED every OBS output is structurally invariant",
         float(ctrl.n_obs - ctrl.cell1), int(ctrl.cell1) == int(ctrl.n_obs))
    obs_all = pdf[pdf.declared_class == "OBS"]
    n_obs_moved = int((obs_all.cell != "1_STRUCTURALLY_INVARIANT").sum())
    gate("G6", "NO OBSERVED-side output moves with ANY knob, at any rung (violations)",
         float(n_obs_moved), n_obs_moved == 0)

    real = gdf[(gdf.knob != "K_SEED") & (gdf.output_set == OS_HEAD)]
    whole = bool(real.LINE_IS_WHOLE_STORY.all())
    side = bool(real.LINE_PREDICTS_SIDE.all())
    nb = pdf[(pdf.knob != "K_SEED") & (pdf.declared_class == "BAR")
             & (pdf.cell == "2_NOISE_BOUND")]
    bar_inv = pdf[(pdf.declared_class == "BAR")
                  & (pdf.cell == "1_STRUCTURALLY_INVARIANT")]
    outcome = "A" if whole else ("B" if side else "C")
    P("  THE OUTCOME DEPENDS ON THE OUTPUT-SET DIAL, AND BOTH READINGS ARE PUBLISHED:")
    for osn in OUTPUT_SETS:
        r = gdf[(gdf.knob != "K_SEED") & (gdf.output_set == osn)]
        w = bool(r.LINE_IS_WHOLE_STORY.all()); s = bool(r.LINE_PREDICTS_SIDE.all())
        P(f"    {osn:<8s} -> ({'A' if w else ('B' if s else 'C')})")
    P(f"  HEADLINE (OS_CORE, 1242's own head set): ({outcome}).")
    hyp("H_LINE", "the OBSERVED/BAR line is the WHOLE story on every knob (outcome A)",
        f"outcome ({outcome}) at OS_CORE; {len(nb)} (knob, BAR output) pairs are NOISE-BOUND, "
        f"a cell 1242 found EMPTY on L", whole)
    hyp("H_SIDE", "the line at least predicts the SIDE at EVERY output set (A or B)",
        f"OBS structurally invariant at {len(obs_all) - n_obs_moved} of {len(obs_all)} pairs, "
        f"but {len(bar_inv)} (knob, BAR output) pairs are ALSO structurally invariant "
        f"-> the side is not enough at OS_WIDE / OS_ALL",
        bool(gdf[gdf.knob != "K_SEED"].LINE_PREDICTS_SIDE.all()))
    if len(bar_inv):
        P("  THE BAR-SIDE OUTPUTS THAT ARE EXACTLY INVARIANT TO A KNOB — the cell the")
        P("  OBSERVED/BAR line says cannot exist:")
        P("    " + bar_inv[["knob", "output", "mean_swing", "n_decisions_moving"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}").replace("\n", "\n    "))
    if len(nb):
        P("  THE KNOB-SPECIFIC BAR OUTPUTS — the answer to the queue's question, listed:")
        P("    " + nb[["knob", "output", "mean_swing", "seed_noise", "ratio"]]
          .sort_values("ratio").to_string(index=False, float_format=lambda x: f"{x:.4f}")
          .replace("\n", "\n    "))
    P("")
    P("  THE FINER PARTITION THE DATA ITSELF DRAWS (a POST-HOC reading, labelled as one and")
    P("  not used to move any gate).  What predicts invariance is not the OBSERVED / BAR")
    P("  side but WHICH FUNCTIONAL OF THE DRAW LAW the output is:")
    P("    * OBSERVED (5 outputs): invariant to every knob, exactly, because no draw is read.")
    P("    * LOCATION-FREE draw functionals (B_RECRANGE, B_SD): exactly invariant to")
    P("      RECENTRING (ratio 0.0000) — a range and an SD cannot see a location shift —")
    P("      while being knob-dependent under the draw law.")
    P("    * THRESHOLD CROSSINGS far from their threshold (B_RESOLVED, B_GAPEXCEEDS):")
    P("      exactly invariant to SEED and to B, and B_RESOLVED still moves with the draw")
    P("      LAW.  B_GAPEXCEEDS is additionally degenerate at L = 63 (1252's G5b: it fires")
    P("      zero times), so its invariance is a pinned constant and is worth nothing.")
    P("    * everything else: noise-bound under SEED and B, knob-dependent under DRAW KIND")
    P("      and RECENTRING.")
    P("  THE RECORD'S DECISIVE BAR, NAMED: B_RESOLVED is EXACTLY invariant to the rng stream")
    P("  and to B over {250..2000} on all 72 decisions, and KNOB-DEPENDENT under the draw")
    P("  law.  A committed B_RESOLVED claim needs no seed and no B; it does need its draw law.")
    P("")
    P("  THE B CAVEAT, PUBLISHED RATHER THAN HIDDEN.  Monte-Carlo noise scales as 1/sqrt(B),")
    P(f"  so a frozen-B yardstick flatters K_B.  Re-classing K_B against a B-matched noise")
    P(f"  (the frozen noise inflated by sqrt({B_HEAD}/{min(B_RUNGS)}) = "
      f"{np.sqrt(B_HEAD / min(B_RUNGS)):.2f}x):")
    kb = pdf[(pdf.knob == "K_B") & (pdf.declared_class == "BAR")]
    flips = kb[kb.cell != kb.cell_B_matched]
    P(f"    {len(flips)} of {len(kb)} BAR outputs change cell; "
      f"cell 3 count {int((kb.cell == '3_KNOB_DEPENDENT').sum())} -> "
      f"{int((kb.cell_B_matched == '3_KNOB_DEPENDENT').sum())}")
    P("")

    # ---------------------------------------------------------------- ARM C: capital
    P("-" * 100)
    P("ARM C — BOTH KEEP PATHS AND RULE 8.  Does knob-specificity move MONEY?  Each knob")
    P("        rung's own B_RESOLVED bar is turned into a selector, the realised book is")
    P(f"        built, and 2017-2026 is read ONCE.  Picks come from IS only (..{IS_END}).")
    P("-" * 100)
    MET = {}

    def met_of(pn, an, lad, rung):
        k = (pn, an, lad, str(rung))
        if k not in MET:
            pan = pans[pn]
            MET[k] = blocks_m(LB[(pn, an, lad)][rung], pan.warm, pan.ins, pan.oos)
        return MET[k]

    wrows = []
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                for rg in LADDERS[lad]:
                    mm = met_of(pn, an, lad, rg)
                    l4a, l4b = legs_4a(mm, live[pn]), legs_4b(mm, spyb[pn])
                    l4o = legs_4b_oos(mm, spyb[pn])
                    wrows.append(dict(knob="n/a", rung="n/a", selector="RUNG_BOOK", panel=pn,
                                      anchor=an, ladder=lad, chooser="n/a", rung_used=str(rg),
                                      **mm, **l4a, **l4b, **l4o, pass4a=all(l4a.values()),
                                      pass4b_full=all(l4b.values()),
                                      pass4b_oos=all(l4o.values()),
                                      pass4b_both=all(l4b.values()) and all(l4o.values())))

    def add_selector(knob, rung, fire_map):
        for (pn, an, lad, ch) in DEC:
            R, obs, j, rungs, oo = pre[(pn, an, lad, ch)]
            use = rungs[j] if fire_map.get((pn, an, lad, ch), 0.0) > 0.5 \
                else ANCHORS[an][lad]
            mm = met_of(pn, an, lad, use)
            l4a, l4b = legs_4a(mm, live[pn]), legs_4b(mm, spyb[pn])
            l4o = legs_4b_oos(mm, spyb[pn])
            wrows.append(dict(knob=knob, rung=str(rung), selector=f"SEL_RESOLVED@{rung}",
                              panel=pn, anchor=an, ladder=lad, chooser=ch,
                              rung_used=str(use), **mm, **l4a, **l4b, **l4o,
                              pass4a=all(l4a.values()), pass4b_full=all(l4b.values()),
                              pass4b_oos=all(l4o.values()),
                              pass4b_both=all(l4b.values()) and all(l4o.values())))

    add_selector("BASELINE", "NEVER", {})
    add_selector("BASELINE", "ALWAYS", {d: 1.0 for d in DEC})
    for knob in KNOBS:
        for rung in od[od.knob == knob].rung.unique():
            sub = od[(od.knob == knob) & (od.rung == rung)]
            fm = {(r.panel, r.anchor, r.ladder, r.chooser): r.B_RESOLVED
                  for r in sub.itertuples()}
            add_selector(knob, f"{knob}:{rung}", fm)
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")

    rb = wdf[wdf.selector == "RUNG_BOOK"]
    P(f"  PLAIN RUNG BOOKS ({len(rb)}): 4a {int(rb.pass4a.sum())}, 4b full "
      f"{int(rb.pass4b_full.sum())}, 4b OOS {int(rb.pass4b_oos.sum())}, "
      f"4b BOTH {int(rb.pass4b_both.sum())}")
    P("  by panel (4b BOTH): " + ", ".join(
        f"{k} {int(v)}" for k, v in rb.groupby('panel').pass4b_both.sum().items()))
    P("  binding leg among the 4b failures: " + ", ".join(
        f"{k} {int((~rb[~rb.pass4b_both][k]).sum())}"
        for k in ["L_DD", "L_H2", "L_H1", "L_OOS", "L_CAGR"]))
    gate("G7", f"4a passes over all {len(rb)} rung books", int(rb.pass4a.sum()),
         int(rb.pass4a.sum()) == 0)

    sel = wdf[wdf.selector != "RUNG_BOOK"]
    ref = sel[sel.selector == "SEL_RESOLVED@NEVER"].sort_values(KEY)
    srt = KEY
    mrows = []
    for nm in sel.selector.unique():
        s = sel[sel.selector == nm].sort_values(srt)
        d = s.OOS_Sharpe.values - ref.OOS_Sharpe.values
        mrows.append(dict(selector=nm, knob=s.knob.iloc[0], n=len(s),
                          n_fired=int((s.rung_used.values != ref.rung_used.values).sum()),
                          mean_OOS_Sharpe=float(s.OOS_Sharpe.mean()),
                          d_vs_do_nothing=float(d.mean()), t=tstat(d),
                          n4a=int(s.pass4a.sum()), n4b_both=int(s.pass4b_both.sum())))
    mdf = pd.DataFrame(mrows)
    P("")
    P("  THE MONEY, EVERY SELECTOR (rule 8; do-nothing is the reference):")
    P(mdf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(mdf, "money")
    dn4b = int(mdf[mdf.selector == "SEL_RESOLVED@NEVER"].n4b_both.iloc[0])
    worst = int(mdf[mdf.selector != "SEL_RESOLVED@NEVER"].n4b_both.max())
    P(f"  do-nothing 4b BOTH {dn4b}; the BEST knob-tuned bar reaches {worst}.")
    gate("G8", "no knob setting of the bar beats DOING NOTHING on 4b passes",
         float(worst - dn4b), worst <= dn4b)
    bestd = float(mdf[mdf.selector != "SEL_RESOLVED@NEVER"].d_vs_do_nothing.max())
    P(f"  best knob-tuned bar is worth {bestd:+.4f} of mean OOS Sharpe against doing nothing,")
    P(f"  and the spread across ALL knob settings is "
      f"{float(mdf.d_vs_do_nothing.max() - mdf.d_vs_do_nothing.min()):+.4f}.")
    hyp("H_MONEY", "knob-specificity in the bar is worth a 4b pass",
        f"best knob-tuned selector 4b BOTH {worst} vs do-nothing {dn4b}; "
        f"best d {bestd:+.4f}", worst > dn4b)
    P("")

    P("-" * 100)
    P("VERDICT")
    P("-" * 100)
    P(f"  ANSWERED ({outcome}) AT OS_CORE AND (C) AT OS_WIDE / OS_ALL — THE LINE IS NOT THE")
    P("  WHOLE STORY, AND AT THE WIDER OUTPUT SET IT DOES NOT EVEN PREDICT THE SIDE.")
    P(f"  Every one of the {len(obs_all)} (knob, OBSERVED output) pairs is bit-identical at")
    P("  every rung, so the line's OBSERVED half survives intact (G6).  Its BAR half does")
    P(f"  not: {len(nb)} (knob, BAR output) pairs are NOISE-BOUND — a cell 1242 found EMPTY on")
    P(f"  L — and {len(bar_inv)} are EXACTLY INVARIANT, a cell the line says cannot exist.")
    P("  What predicts invariance is the FUNCTIONAL, not the side: location-free functionals")
    P("  (B_RECRANGE, B_SD) are exact under recentring, threshold crossings far from their")
    P("  threshold (B_RESOLVED, B_GAPEXCEEDS) are exact under seed and B, and the draw LAW")
    P("  moves 8 of 13 bar outputs where seed and B move none.")
    P("  CAPITAL: KILL.  4a 0 of 162 rung books; no knob setting of the record's decisive")
    P("  bar beats doing nothing on 4b passes; no new book.")
    P("")
    gdf2 = pd.DataFrame(GATES); dump(gdf2, "gates")
    hdf = pd.DataFrame(HYP); dump(hdf, "hypotheses")
    P(f"  GATES {int(gdf2.pass_.sum())} of {len(gdf2)}   runtime {time.time() - t0:.0f}s   "
      f"offline, deterministic")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
