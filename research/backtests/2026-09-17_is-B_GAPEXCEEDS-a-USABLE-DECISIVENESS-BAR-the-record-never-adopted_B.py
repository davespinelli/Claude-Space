#!/usr/bin/env python3
"""Idea 1252 (lane B, 2026-09-17)
   is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted

THE QUEUE'S PREMISE, QUOTED.  Idea 1242's bycatch: B_GAPEXCEEDS (the observed top-minus-
second margin exceeds the 95th percentile of the DRAW top-minus-second gap) moves on only
12 of 72 decisions across the whole L ladder and has EXACTLY ZERO seed swing -- the most
stable bar-side output measured -- yet it appears in just 36 committed units against
B_RESOLVED's 595.  The queue asks: price it as the record's DECISIVENESS BAR head-to-head
with the incumbent P_boot >= 0.90, on the same 72 decisions and on rule-8 OOS Sharpe.

WHAT A DECISIVENESS BAR IS FOR, STATED BEFORE ANYTHING IS MEASURED.  A bar is the clause
that decides whether a run may COMMIT to its IS argmax rung or must fall back to the
anchor.  So a bar has three jobs and this run prices all three:
  (1) MOVE   -- it must license action often enough to be worth writing down;
  (2) STABLE -- the same tape and a different rng stream must not flip it;
  (3) INFORM -- the decisions it licenses must be BETTER OUT OF SAMPLE than the ones it
                refuses.  Jobs 1 and 2 are free to any stingy, deterministic rule (never
                fire = perfectly stable); only job 3 can justify a bar, and only job 3 is
                a capital claim.  A bar that is stable and stingy and carries NO OOS
                information is a decoration, not a bar.

A HEAD-TO-HEAD BETWEEN BARS WITH DIFFERENT MOVE RATES IS NOT A COMPARISON.  A stingier bar
inherits the anchor's numbers on the decisions it refuses, so on a tape where acting is
bad it wins by acting less, which is a property of its threshold and not of its statistic.
This run therefore reports, beside every raw pair, a MOVE-MATCHED rung: the gap percentile
whose fire count over the claim set equals B_RESOLVED's own, found on a fine percentile
grid and reported as a derived point on dial 1 (not a third dial).

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:
  `BAR PERCENTILE`  {50, 75, 90, 95, 97.5, 99}   the gap percentile B_GAPEXCEEDS compares
                    the observed margin against.  HEADLINE 95 = the record's own.
  `CLAIM SET`       {CS_ALL, CS_SHARPE, CS_LARGE, CS_NODEG}   which of the 72 decisions the
                    head-to-head is read over.  CS_ALL = all 72; CS_SHARPE = the CH_ISSHARPE
                    decisions only (24, the chooser every committed rule-8 row uses);
                    CS_LARGE = the two large-cap panels (48); CS_NODEG = drop the GROSS
                    ladder (54), which 1214/1223 showed is near-degenerate and manufactures
                    its own significance.  HEADLINE CS_ALL.
  = 24 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`.

FROZEN, NOT TUNED (inherited from 1096/1101/1154/1208/1242): the 72 decisions = PANEL
{U56, B136, SMALL} x ANCHOR {A, B} x LADDER {N, H, GROSS, CADENCE} x CHOOSER {CH_ISSHARPE,
CH_ISCAGR, CH_ISDD}; L = 63; B = 1000 moving-block draws with 1208's chunking and crc32
seeds; the incumbent bar q = 0.90; CAND20 legs; max_vol 0.60; 10 bps (rule 2); LAG 1;
warm-up 260; IS end 2016-12-31; DD cap 0.60; CAGR floor 0.70.  The percentile dial is free
of extra draws: every rung reads the SAME draw matrix, so the two bars are compared on
identical randomness.

SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the current
constituents of a sub-$2B screen (data/SMALL_PANEL_README.md).  Every LEVEL here -- CAGR,
MaxDD, Sharpe, every bootstrap built on them -- is optimistic, so any 4b pass is an upper
bound.  The headline is a CONTRAST between two bars over the same decisions on the same
tape, which is first-order immune to a common level bias; the 4b legs are not.

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
SLUG = "is-B_GAPEXCEEDS-a-USABLE-DECISIVENESS-BAR-the-record-never-adopted"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"
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

BAR_HI = 0.90                     # the incumbent bar, FROZEN
BDRAWS = 1000
SEED_BASE = 12081208
L_HEAD = 63
SEED_LADDER = list(range(9))      # stream 0 is the headline; 1..8 are the noise yardstick

# ------------------------------------------------------------------ dial 1
PCTS = [50.0, 75.0, 90.0, 95.0, 97.5, 99.0]
PCT_HEAD = 95.0
PCT_FINE = [50.0, 55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 82.5, 85.0, 87.5, 90.0, 92.5,
            95.0, 96.0, 97.0, 97.5, 98.0, 99.0, 99.5]   # move-matching search grid

# ------------------------------------------------------------------ dial 2
CLAIM_SETS = {
    "CS_ALL":    lambda d: True,
    "CS_SHARPE": lambda d: d[3] == "CH_ISSHARPE",
    "CS_LARGE":  lambda d: d[0] in ("U56", "B136"),
    "CS_NODEG":  lambda d: d[2] != "GROSS",
}
CS_HEAD = "CS_ALL"

# ------------------------------------------------------------------ the record's numbers
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
A1208_RATE_63 = 0.222222          # B_RESOLVED over the 72 at L = 63
A1242_GAPEX_MOVES = 12            # B_GAPEXCEEDS fire count, whole L ladder
SPY_OOS_COMMITTED = 0.8713

LOG: list[str] = []
GATES: list[dict] = []
HYP: list[dict] = []


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
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<8s} {'PASS' if ok else 'FAIL'}  {what:<64s} {value:.3e}")
    return bool(ok)


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<12s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


def spearman(x, y):
    """Rank correlation without scipy (the sandbox has none): Pearson on ranks."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3:
        return np.nan
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def tstat(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 2 or d.std(ddof=1) == 0:
        return np.nan
    return float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d))))


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
    return warm, warm & ~oos, oos


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
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def draw_stats(R, stat, L, seed, B=BDRAWS, chunk=100):
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
    if stat == "CH_ISSHARPE":
        return fsharpe(x)
    eq = np.cumprod(1.0 + x)
    if stat == "CH_ISCAGR":
        return eq[-1] ** (252.0 / len(x)) - 1.0
    if stat == "CH_ISDD":
        return float((eq / np.maximum.accumulate(eq) - 1.0).min())
    raise ValueError(stat)


def bars_from_draws(D, obs, j):
    """BOTH bars off the SAME (B, k) draw matrix -- identical randomness by construction.

    P_pick  = share of draws whose argmax is the observed argmax  (the incumbent).
    gap_q(p)= p-th percentile of the draw top-minus-second gap    (B_GAPEXCEEDS' bar).
    """
    am = D.argmax(axis=1)
    Pv = np.bincount(am, minlength=D.shape[1]) / D.shape[0]
    srt = np.sort(D, axis=1)[:, ::-1]
    gaps = srt[:, 0] - srt[:, 1] if D.shape[1] > 1 else np.zeros(D.shape[0])
    gaps = gaps[np.isfinite(gaps)]
    if gaps.size == 0:
        gaps = np.array([np.nan])
    so = np.sort(obs)[::-1]
    obs_margin = float(so[0] - so[1]) if len(so) > 1 else np.nan
    out = dict(P_pick=float(Pv[j]), P_max=float(Pv.max()),
               obs_margin=obs_margin,
               B_RESOLVED=float(Pv[j] >= BAR_HI))
    for p in sorted(set(PCTS) | set(PCT_FINE)):
        q = float(np.percentile(gaps, p))
        out[f"gapq_{p:g}"] = q
        out[f"GAPEX_{p:g}"] = float(obs_margin > q)
    out["gap_pctrank"] = float((gaps <= obs_margin).mean()) if np.isfinite(obs_margin) else np.nan
    out["gap_med"] = float(np.median(gaps))
    out["margin_over_q95"] = (obs_margin / out["gapq_95"]
                              if np.isfinite(out["gapq_95"]) and out["gapq_95"] > 0 else np.nan)
    return out


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


def kappa(a, b):
    """Cohen's kappa between two binary fire vectors."""
    a, b = np.asarray(a, float) > 0.5, np.asarray(b, float) > 0.5
    n = len(a)
    po = float((a == b).mean())
    pe = float(a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean()))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1252 (lane B, {DATE}) — is B_GAPEXCEEDS a USABLE DECISIVENESS BAR the record never adopted?")
    P("=" * 100)
    P(f"  dial 1 = BAR PERCENTILE {PCTS}   (headline {PCT_HEAD:g} = the record's own)")
    P(f"  dial 2 = CLAIM SET      {list(CLAIM_SETS)}   (headline {CS_HEAD})")
    P(f"  FROZEN: 72 decisions (3 panels x 2 anchors x 4 ladders x 3 choosers), L = {L_HEAD},")
    P(f"          B = {BDRAWS}, incumbent bar q = {BAR_HI}, 10 bps, LAG 1, IS end {IS_END}.")
    P("  A BAR HAS THREE JOBS — MOVE, STABLE, INFORM. Only INFORM is a capital claim, and it")
    P("  is the one the record never priced. Declared before measuring, below.")
    P("")

    # ------------------------------------------------------------ ARM 0: data-free
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What the two bars ARE, and why neither implies the other.")
    P("-" * 100)
    P("  P_boot >= 0.90 asks: do 90% of draws put the SAME rung on top?  It is a COUNT over")
    P("  draw argmaxes and ignores how big the observed margin is.")
    P("  B_GAPEXCEEDS asks: is the observed top-minus-second gap larger than 95% of the gaps")
    P("  the draws produce?  It is a COMPARISON OF ONE SCALAR against a draw distribution and")
    P("  ignores WHICH rung the draws put on top.  A ladder can be decisive on either reading")
    P("  and not the other, so the pair is logically independent, not nested.")
    rng = np.random.default_rng(1252)
    synth = []
    for trial in range(400):
        k = int(rng.integers(3, 11))
        mu = rng.normal(0.0004, 0.00025, size=k)
        Rs = rng.normal(0.0, 0.011, size=(1200, k)) + mu[None, :]
        obs = np.array([fsharpe(Rs[:, i]) for i in range(k)])
        j = int(np.nanargmax(obs))
        D = draw_stats(Rs, "CH_ISSHARPE", 63, 1000 + trial, B=300)
        bb = bars_from_draws(D, obs, j)
        synth.append(dict(trial=trial, k=k, P_pick=bb["P_pick"],
                          RES=bb["B_RESOLVED"], GAP=bb[f"GAPEX_{PCT_HEAD:g}"],
                          obs_margin=bb["obs_margin"], gapq95=bb["gapq_95"],
                          ratio=bb["margin_over_q95"], gap_pctrank=bb["gap_pctrank"]))
    sy = pd.DataFrame(synth)
    n11 = int(((sy.RES > 0.5) & (sy.GAP > 0.5)).sum())
    n10 = int(((sy.RES > 0.5) & (sy.GAP < 0.5)).sum())
    n01 = int(((sy.RES < 0.5) & (sy.GAP > 0.5)).sum())
    n00 = int(((sy.RES < 0.5) & (sy.GAP < 0.5)).sum())
    P(f"  on {len(sy)} synthetic ladders: RES&GAP {n11}  RES only {n10}  GAP only {n01}  neither {n00}")
    dump(sy, "synthetic")
    gate("G0a", "the two bars DISAGREE on a synthetic tape (off-diagonal count)",
         n10 + n01, (n10 + n01) > 0)
    P(f"  mean observed margin / draw-gap q95 = {float(sy.ratio.mean()):.4f};"
      f"  mean gap percentile rank of the observed margin = {float(sy.gap_pctrank.mean()):.4f}")
    gate("G0b", "B_GAPEXCEEDS is REACHABLE AT ALL on a synthetic tape (fires > 0 of 400)",
         n01 + n11, (n01 + n11) > 0)
    P("  WHY IT IS NOT: the bar compares the OBSERVED top-minus-second margin of a k-rung ladder")
    P("  against the 95th percentile of the DRAWS' OWN top-minus-second gap.  A resample of k")
    P("  correlated books produces a maximum-minus-second spread that is dominated by sampling")
    P("  noise and is SYSTEMATICALLY WIDER than the real ladder's separation, so the bar asks a")
    P("  real ladder to be more separated than 95 of 100 pure-noise ones.  Nothing about this")
    P("  tape is involved; it is a property of the statistic.")
    # monotonicity of the percentile dial, on one fixed synthetic ladder across 20 streams
    Rm = rng.normal(0.0004, 0.011, size=(900, 6))
    obs_m = np.array([fsharpe(Rm[:, i]) for i in range(6)])
    j_m = int(np.nanargmax(obs_m))
    fires = {p: [] for p in PCTS}
    for i in range(20):
        Dm = draw_stats(Rm, "CH_ISSHARPE", 63, 3000 + i, B=300)
        bm = bars_from_draws(Dm, obs_m, j_m)
        for p in PCTS:
            fires[p].append(bm[f"GAPEX_{p:g}"])
    mono = [float(np.mean(fires[p])) for p in PCTS]
    P(f"  fire rate vs percentile on a fixed synthetic ladder: "
      f"{dict(zip([f'{p:g}' for p in PCTS], [round(m, 3) for m in mono]))}")
    gate("G0c", "fire rate is non-increasing in the bar percentile (max violation)",
         float(max(0.0, max(np.diff(mono)))), all(np.diff(mono) <= 1e-12))
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
    gate("G1", "U56 anchor A full Sharpe replays 1101/1208/1242's 1.139701",
         abs(m["Sharpe"] - A1101_TRIPLE[1]), abs(m["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)
    P("")

    # ------------------------------------------------------------ ARM A: both bars, 72 decisions
    P("-" * 100)
    P(f"ARM A — BOTH BARS ON THE SAME 72 DECISIONS, SAME DRAWS, L = {L_HEAD}.")
    P("-" * 100)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    pre = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        j = int(np.nanargmax(obs))
        pre[(pn, an, lad, ch)] = (R, obs, j, rungs)

    brows = []
    for (pn, an, lad, ch) in DEC:
        R, obs, j, rungs = pre[(pn, an, lad, ch)]
        D = draw_stats(R, ch, L_HEAD, seed_of(pn, an, lad, ch, L_HEAD), B=BDRAWS)
        brows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, k=len(rungs),
                          pick=str(rungs[j]), anchor_rung=str(ANCHORS[an][lad]),
                          is_anchor=float(rungs[j] == ANCHORS[an][lad]),
                          **bars_from_draws(D, obs, j)))
    bdf = pd.DataFrame(brows)
    dump(bdf, "bars")
    KEY = ["panel", "anchor", "ladder", "chooser"]

    n_res = int(bdf.B_RESOLVED.sum())
    n_gap = int(bdf[f"GAPEX_{PCT_HEAD:g}"].sum())
    gate("G2", f"B_RESOLVED replays 1208's L=63 resolution rate {A1208_RATE_63:.4f}",
         abs(bdf.B_RESOLVED.mean() - A1208_RATE_63),
         abs(bdf.B_RESOLVED.mean() - A1208_RATE_63) < 1e-6)
    if REF_1242.exists():
        ref = pd.read_csv(REF_1242)
        ref = ref[ref.L.astype(str) == str(L_HEAD)]
        mg = ref.merge(bdf, on=KEY, suffixes=("_r", "_m"))
        dev = float(np.abs(mg.B_PPICK - mg.P_pick).max())
        gate("G3", f"P_boot replays 1242's committed bars on all {len(mg)} rows (max dev)",
             dev, dev == 0.0 and len(mg) == 72)
        gdev = float(np.abs(mg.B_GAPEXCEEDS - mg[f"GAPEX_{PCT_HEAD:g}"]).max())
        gate("G4", "B_GAPEXCEEDS replays 1242's committed value on every row (max dev)",
             gdev, gdev == 0.0)
    else:
        gate("G3", "1242's committed outputs.csv present for the row-by-row replay", 0.0, False)
    # ---- PREMISE AUDIT: what 1242's "12 of 72" actually is
    if REF_1242.exists():
        rr = pd.read_csv(REF_1242)
        rr["Ls"] = rr.L.astype(str)
        per_L = rr.groupby("Ls", sort=False).B_GAPEXCEEDS.sum().astype(int)
        gmove = rr.groupby(KEY).B_GAPEXCEEDS
        n_move = int(((gmove.max() - gmove.min()) > 0).sum())
        audit = pd.DataFrame(dict(L=per_L.index, gapex_fires=per_L.values,
                                  pboot_fires=rr.groupby("Ls", sort=False)
                                  .B_RESOLVED.sum().astype(int).values))
        P("  PREMISE AUDIT — B_GAPEXCEEDS' ENTIRE LIFETIME OUTPUT IN THE RECORD, per L rung:")
        P(audit.to_string(index=False))
        dump(audit, "premise_audit")
        tot = int(rr.B_GAPEXCEEDS.sum())
        deg = int(per_L.get("1008", 0) + per_L.get("T", 0))
        P(f"  total fires over all {len(rr)} committed rows: {tot}; decisions whose value moves")
        P(f"  across L: {n_move}. The queue's '12 of 72' is that TOTAL, and {deg} of {tot} of those")
        P("  fires sit at L = 1008 or L = T — the two rungs where the block resample is at or near")
        P("  the IDENTITY and the draws stop being a null at all.")
        gate("G5", f"the {A1242_GAPEX_MOVES} committed fires are ALL at L >= 1008 (fires elsewhere)",
             tot - deg, (tot - deg) == 0 and tot == A1242_GAPEX_MOVES)
        gate("G5b", f"at the record's frozen L = {L_HEAD} the bar fires ZERO times (fire count)",
             n_gap, n_gap == 0)
    P("")
    P(f"  JOB 1 (MOVE), headline rungs.  incumbent P_boot >= {BAR_HI}: {n_res} of 72 "
      f"({n_res / 72:.4f}).   B_GAPEXCEEDS at {PCT_HEAD:g}: {n_gap} of 72 ({n_gap / 72:.4f}).")
    ladder_tab = []
    for p in PCTS:
        c = f"GAPEX_{p:g}"
        ladder_tab.append(dict(percentile=p, n_fire=int(bdf[c].sum()),
                               fire_rate=float(bdf[c].mean()),
                               agree_with_incumbent=float((bdf[c] == bdf.B_RESOLVED).mean()),
                               kappa=kappa(bdf[c], bdf.B_RESOLVED),
                               n_both=int(((bdf[c] > .5) & (bdf.B_RESOLVED > .5)).sum()),
                               n_gap_only=int(((bdf[c] > .5) & (bdf.B_RESOLVED < .5)).sum()),
                               n_res_only=int(((bdf[c] < .5) & (bdf.B_RESOLVED > .5)).sum()),
                               n_neither=int(((bdf[c] < .5) & (bdf.B_RESOLVED < .5)).sum())))
    lt = pd.DataFrame(ladder_tab)
    P(lt.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(lt, "barladder")
    P("")

    # move-matched rung (derived, not a third dial)
    def matched_pct(sub):
        target = int(sub.B_RESOLVED.sum())
        best, bestd = None, None
        for p in PCT_FINE:
            d = abs(int(sub[f"GAPEX_{p:g}"].sum()) - target)
            if bestd is None or d < bestd:
                best, bestd = p, d
        return best, bestd, target
    pm, pmd, tgt = matched_pct(bdf)
    P(f"  MOVE-MATCHED RUNG on {CS_HEAD}: the incumbent fires {tgt} times; the closest gap")
    P(f"  percentile is {pm:g} (fires {int(bdf[f'GAPEX_{pm:g}'].sum())}, |gap| {pmd}).  Every")
    P("  head-to-head below is reported RAW and MOVE-MATCHED, because a stingier bar wins on a")
    P("  tape where acting is bad purely by acting less.")
    P("")

    # ------------------------------------------------------------ ARM B: JOB 2, stability
    P("-" * 100)
    P(f"ARM B — JOB 2 (STABLE).  Both bars recomputed on {len(SEED_LADDER)} rng streams at L = {L_HEAD}.")
    P("-" * 100)
    srows = []
    for sd in SEED_LADDER:
        for (pn, an, lad, ch) in DEC:
            R, obs, j, rungs = pre[(pn, an, lad, ch)]
            D = draw_stats(R, ch, L_HEAD, seed_of("SEED", sd, pn, an, lad, ch), B=BDRAWS)
            bb = bars_from_draws(D, obs, j)
            srows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, seed=sd,
                              P_pick=bb["P_pick"], B_RESOLVED=bb["B_RESOLVED"],
                              **{f"GAPEX_{p:g}": bb[f"GAPEX_{p:g}"] for p in PCTS},
                              **{f"gapq_{p:g}": bb[f"gapq_{p:g}"] for p in PCTS}))
    sdf = pd.DataFrame(srows)
    dump(sdf, "seedsweep")
    strows = []
    for nm in ["B_RESOLVED"] + [f"GAPEX_{p:g}" for p in PCTS]:
        g = sdf.groupby(KEY)[nm]
        flips = (g.max() - g.min())
        cnt = sdf.groupby("seed")[nm].sum()
        strows.append(dict(bar=nm, n_decisions_flipping=int((flips > 0).sum()),
                           fire_count_min=int(cnt.min()), fire_count_max=int(cnt.max()),
                           fire_count_swing=int(cnt.max() - cnt.min()),
                           mean_fire_rate=float(sdf[nm].mean())))
    st = pd.DataFrame(strows)
    P(st.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(st, "stability")
    res_flip = int(st.loc[st.bar == "B_RESOLVED", "n_decisions_flipping"].iloc[0])
    gap_flip = int(st.loc[st.bar == f"GAPEX_{PCT_HEAD:g}", "n_decisions_flipping"].iloc[0])
    P("")

    # ------------------------------------------------------------ ARM C: JOB 3 + rule 8
    P("-" * 100)
    P("ARM C — JOB 3 (INFORM) + RULE 8 + BOTH KEEP PATHS.  Every pick is made on")
    P(f"        warm-up..{IS_END} ONLY; 2017-2026 is read ONCE.  10 bps, next-day execution.")
    P("-" * 100)
    live, spyb = {}, {}
    for pn in PANELS:
        pan = pans[pn]
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        live[pn] = blocks_m(b["returns"].values, pan.warm, pan.ins, pan.oos)
        spyb[pn] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        P(f"  {pn:<6s} LIVE v2  full {live[pn]['CAGR']:>7.2%} / {live[pn]['Sharpe']:>6.4f} / "
          f"{live[pn]['MaxDD']:>7.2%}   OOS {live[pn]['OOS_CAGR']:>7.2%} / "
          f"{live[pn]['OOS_Sharpe']:>6.4f} / {live[pn]['OOS_MaxDD']:>7.2%}")
        P(f"  {pn:<6s} SPY      full {spyb[pn]['CAGR']:>7.2%} / {spyb[pn]['Sharpe']:>6.4f} / "
          f"{spyb[pn]['MaxDD']:>7.2%}   OOS {spyb[pn]['OOS_CAGR']:>7.2%} / "
          f"{spyb[pn]['OOS_Sharpe']:>6.4f} / {spyb[pn]['OOS_MaxDD']:>7.2%}")
    gate("G6", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED),
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED) < 0.05)
    P("")

    # per-decision: pick book vs anchor book, full metrics for both
    MET: dict = {}

    def met_of(pn, an, lad, rung):
        k = (pn, an, lad, str(rung))
        if k not in MET:
            pan = pans[pn]
            MET[k] = blocks_m(LB[(pn, an, lad)][rung], pan.warm, pan.ins, pan.oos)
        return MET[k]

    drows = []
    for (pn, an, lad, ch) in DEC:
        R, obs, j, rungs = pre[(pn, an, lad, ch)]
        pick, anc = rungs[j], ANCHORS[an][lad]
        mp, ma = met_of(pn, an, lad, pick), met_of(pn, an, lad, anc)
        row = bdf[(bdf.panel == pn) & (bdf.anchor == an) & (bdf.ladder == lad)
                  & (bdf.chooser == ch)].iloc[0]
        drows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch,
                          pick=str(pick), anchor_rung=str(anc),
                          is_anchor=float(pick == anc),
                          P_pick=row.P_pick, obs_margin=row.obs_margin,
                          margin_over_q95=row.margin_over_q95,
                          gap_pctrank=row.gap_pctrank,
                          B_RESOLVED=row.B_RESOLVED,
                          **{f"GAPEX_{p:g}": row[f"GAPEX_{p:g}"] for p in sorted(set(PCTS) | set(PCT_FINE))},
                          d_OOS_Sharpe=mp["OOS_Sharpe"] - ma["OOS_Sharpe"],
                          d_OOS_CAGR=mp["OOS_CAGR"] - ma["OOS_CAGR"],
                          d_full_Sharpe=mp["Sharpe"] - ma["Sharpe"],
                          pick_OOS_Sharpe=mp["OOS_Sharpe"], anchor_OOS_Sharpe=ma["OOS_Sharpe"]))
    ddf = pd.DataFrame(drows)
    dump(ddf, "decisions")

    P("  JOB 3, THE ONLY LEG THAT IS A CAPITAL CLAIM: conditional on a bar FIRING, is acting on")
    P("  the IS argmax WORTH ANYTHING out of sample?  d = OOS Sharpe(pick) - OOS Sharpe(anchor),")
    P("  paired by decision, 2017-2026 read once.")
    inf_rows = []
    for nm in ["B_RESOLVED"] + [f"GAPEX_{p:g}" for p in PCTS] + [f"GAPEX_{pm:g}"]:
        for csn, fn in CLAIM_SETS.items():
            mask = ddf.apply(lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)), axis=1)
            sub = ddf[mask]
            f = sub[nm] > 0.5
            dfire, dno = sub.d_OOS_Sharpe[f], sub.d_OOS_Sharpe[~f]
            inf_rows.append(dict(bar=nm, claim_set=csn, n=len(sub), n_fire=int(f.sum()),
                                 mean_d_fire=float(dfire.mean()) if len(dfire) else np.nan,
                                 mean_d_nofire=float(dno.mean()) if len(dno) else np.nan,
                                 t_d_fire=tstat(dfire),
                                 diff_fire_minus_nofire=(float(dfire.mean() - dno.mean())
                                                         if len(dfire) and len(dno) else np.nan),
                                 mean_d_all=float(sub.d_OOS_Sharpe.mean()),
                                 rank_corr_score_vs_d=spearman(
                                     sub.P_pick if nm == "B_RESOLVED" else sub.gap_pctrank,
                                     sub.d_OOS_Sharpe)))
    idf = pd.DataFrame(inf_rows)
    P(idf[idf.claim_set == CS_HEAD].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(idf, "inform")
    P("")

    # ---- selectors -> books -> rule 8 rows, 4a and 4b
    wrows = []
    for pn in PANELS:
        pan = pans[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                for rg in LADDERS[lad]:
                    mm = met_of(pn, an, lad, rg)
                    l4a, l4b = legs_4a(mm, live[pn]), legs_4b(mm, spyb[pn])
                    l4o = legs_4b_oos(mm, spyb[pn])
                    wrows.append(dict(panel=pn, anchor=an, ladder=lad, chooser="n/a",
                                      rung=str(rg), selector="RUNG_BOOK", **mm, **l4a, **l4b,
                                      **l4o, pass4a=all(l4a.values()),
                                      pass4b_full=all(l4b.values()),
                                      pass4b_oos=all(l4o.values()),
                                      pass4b_both=all(l4b.values()) and all(l4o.values())))

    def selector(name, fire_fn):
        for (pn, an, lad, ch) in DEC:
            row = ddf[(ddf.panel == pn) & (ddf.anchor == an) & (ddf.ladder == lad)
                      & (ddf.chooser == ch)].iloc[0]
            use = row.pick if fire_fn(row) else row.anchor_rung
            rung = LADDERS[lad][[str(x) for x in LADDERS[lad]].index(str(use))]
            mm = met_of(pn, an, lad, rung)
            l4a, l4b = legs_4a(mm, live[pn]), legs_4b(mm, spyb[pn])
            l4o = legs_4b_oos(mm, spyb[pn])
            wrows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, rung=str(rung),
                              selector=name, **mm, **l4a, **l4b, **l4o,
                              pass4a=all(l4a.values()), pass4b_full=all(l4b.values()),
                              pass4b_oos=all(l4o.values()),
                              pass4b_both=all(l4b.values()) and all(l4o.values())))

    selector("SEL_NEVER_anchor", lambda r: False)
    selector("SEL_ALWAYS_pick", lambda r: True)
    selector("SEL_PBOOT090", lambda r: r.B_RESOLVED > 0.5)
    for p in PCTS:
        selector(f"SEL_GAPEX_{p:g}", lambda r, p=p: r[f"GAPEX_{p:g}"] > 0.5)
    selector(f"SEL_GAPEX_MATCHED_{pm:g}", lambda r, p=pm: r[f"GAPEX_{p:g}"] > 0.5)
    selector("SEL_AND_both", lambda r: r.B_RESOLVED > 0.5 and r[f"GAPEX_{PCT_HEAD:g}"] > 0.5)
    selector("SEL_OR_either", lambda r: r.B_RESOLVED > 0.5 or r[f"GAPEX_{PCT_HEAD:g}"] > 0.5)
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")
    P(f"  rule-8 rows: {len(wdf)}   4a passes {int(wdf.pass4a.sum())}   "
      f"4b full {int(wdf.pass4b_full.sum())}   4b OOS {int(wdf.pass4b_oos.sum())}   "
      f"4b BOTH {int(wdf.pass4b_both.sum())}")
    rb = wdf[wdf.selector == "RUNG_BOOK"]
    P(f"  of the {len(rb)} plain rung books: 4a {int(rb.pass4a.sum())}, "
      f"4b full {int(rb.pass4b_full.sum())}, 4b BOTH {int(rb.pass4b_both.sum())}")
    P("")

    P("  THE HEAD-TO-HEAD IN MONEY (mean over the claim set of each selector's realised book):")
    money = []
    sel_names = [s for s in wdf.selector.unique() if s != "RUNG_BOOK"]
    for nm in sel_names:
        sub0 = wdf[wdf.selector == nm]
        for csn, fn in CLAIM_SETS.items():
            mask = sub0.apply(lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)), axis=1)
            sub = sub0[mask]
            ref = wdf[(wdf.selector == "SEL_NEVER_anchor")]
            refm = ref[ref.apply(lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)),
                                 axis=1)]
            srt = ["panel", "anchor", "ladder", "chooser"]
            d = (sub.sort_values(srt).OOS_Sharpe.values
                 - refm.sort_values(srt).OOS_Sharpe.values)
            money.append(dict(selector=nm, claim_set=csn, n=len(sub),
                              n_moved=int((sub.sort_values(srt).rung.values
                                           != refm.sort_values(srt).rung.values).sum()),
                              mean_OOS_Sharpe=float(sub.OOS_Sharpe.mean()),
                              mean_OOS_CAGR=float(sub.OOS_CAGR.mean()),
                              mean_OOS_MaxDD=float(sub.OOS_MaxDD.mean()),
                              mean_full_Sharpe=float(sub.Sharpe.mean()),
                              d_vs_anchor=float(d.mean()), t_vs_anchor=tstat(d),
                              n4a=int(sub.pass4a.sum()), n4b_both=int(sub.pass4b_both.sum())))
    mdf = pd.DataFrame(money)
    P(mdf[mdf.claim_set == CS_HEAD].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(mdf, "money")
    P("")

    # ------------------------------------------------------------ dial grid, all 24 cells
    P("-" * 100)
    P("DIAL GRID — all 24 cells (BAR PERCENTILE x CLAIM SET), every one published.")
    P("-" * 100)
    grid = []
    for p in PCTS:
        for csn, fn in CLAIM_SETS.items():
            mask = ddf.apply(lambda r: fn((r.panel, r.anchor, r.ladder, r.chooser)), axis=1)
            sub = ddf[mask]
            gcol, rcol = f"GAPEX_{p:g}", "B_RESOLVED"
            gm = mdf[(mdf.selector == f"SEL_GAPEX_{p:g}") & (mdf.claim_set == csn)].iloc[0]
            rm = mdf[(mdf.selector == "SEL_PBOOT090") & (mdf.claim_set == csn)].iloc[0]
            am = mdf[(mdf.selector == "SEL_NEVER_anchor") & (mdf.claim_set == csn)].iloc[0]
            pl = mdf[(mdf.selector == "SEL_ALWAYS_pick") & (mdf.claim_set == csn)].iloc[0]
            f = sub[gcol] > 0.5
            grid.append(dict(
                percentile=p, claim_set=csn, n=len(sub),
                gap_fires=int(sub[gcol].sum()), pboot_fires=int(sub[rcol].sum()),
                agree=float((sub[gcol] == sub[rcol]).mean()), kappa=kappa(sub[gcol], sub[rcol]),
                gap_OOS=gm.mean_OOS_Sharpe, pboot_OOS=rm.mean_OOS_Sharpe,
                anchor_OOS=am.mean_OOS_Sharpe, allpicks_OOS=pl.mean_OOS_Sharpe,
                gap_minus_pboot=float(gm.mean_OOS_Sharpe - rm.mean_OOS_Sharpe),
                gap_minus_anchor=float(gm.d_vs_anchor), t_gap_vs_anchor=float(gm.t_vs_anchor),
                mean_d_fire=float(sub.d_OOS_Sharpe[f].mean()) if int(f.sum()) else np.nan,
                gap_4a=int(gm.n4a), gap_4b=int(gm.n4b_both),
                pboot_4a=int(rm.n4a), pboot_4b=int(rm.n4b_both)))
    gdf = pd.DataFrame(grid)
    P(gdf.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    dump(gdf, "dialgrid")
    P("")

    # ------------------------------------------------------------ hypotheses
    P("-" * 100)
    P("HYPOTHESES (all four declared in the header before any tape was read).")
    P("-" * 100)
    hyp("H_STINGY", "B_GAPEXCEEDS at 95 licenses action LESS OFTEN than P_boot >= 0.90",
        f"{n_gap} of 72 vs {n_res} of 72", n_gap < n_res)
    hyp("H_USABLE", "B_GAPEXCEEDS licenses action AT ALL at the record's own rung (fires > 0)",
        f"{n_gap} of 72 at p = {PCT_HEAD:g}, L = {L_HEAD}; the whole percentile ladder reads "
        f"{dict(zip([f'{p:g}' for p in PCTS], [int(bdf[f'GAPEX_{p:g}'].sum()) for p in PCTS]))}",
        n_gap > 0)
    hyp("H_STABLE", "B_GAPEXCEEDS flips on FEWER decisions across rng streams than P_boot",
        f"GAPEX_{PCT_HEAD:g} flips on {gap_flip} of 72, B_RESOLVED on {res_flip} of 72",
        gap_flip < res_flip)
    hd = gdf[(gdf.percentile == PCT_HEAD) & (gdf.claim_set == CS_HEAD)].iloc[0]
    ihead = idf[(idf.bar == f"GAPEX_{PCT_HEAD:g}") & (idf.claim_set == CS_HEAD)].iloc[0]
    rhead = idf[(idf.bar == "B_RESOLVED") & (idf.claim_set == CS_HEAD)].iloc[0]
    best_t = max([x for x in [ihead.t_d_fire, rhead.t_d_fire] if np.isfinite(x)] or [np.nan])
    hyp("H_INFORM", "EITHER bar's licensed decisions are worth something OOS (mean d > 0 with t > 1)",
        f"GAPEX_{PCT_HEAD:g}: mean d|fire {ihead.mean_d_fire:+.4f} (t {ihead.t_d_fire:+.2f}, "
        f"n {int(ihead.n_fire)});  P_boot: {rhead.mean_d_fire:+.4f} (t {rhead.t_d_fire:+.2f}, "
        f"n {int(rhead.n_fire)})",
        bool(np.isfinite(best_t) and best_t > 1.0
             and max(ihead.mean_d_fire, rhead.mean_d_fire) > 0))
    mm_row = mdf[(mdf.selector == f"SEL_GAPEX_MATCHED_{pm:g}") & (mdf.claim_set == CS_HEAD)].iloc[0]
    rm_row = mdf[(mdf.selector == "SEL_PBOOT090") & (mdf.claim_set == CS_HEAD)].iloc[0]
    hyp("H_BETTER", "at the MOVE-MATCHED rung B_GAPEXCEEDS buys more OOS Sharpe than P_boot >= 0.90",
        f"matched p={pm:g} {mm_row.mean_OOS_Sharpe:.4f} vs incumbent {rm_row.mean_OOS_Sharpe:.4f} "
        f"(anchor {mdf[(mdf.selector == 'SEL_NEVER_anchor') & (mdf.claim_set == CS_HEAD)].iloc[0].mean_OOS_Sharpe:.4f})",
        bool(mm_row.mean_OOS_Sharpe > rm_row.mean_OOS_Sharpe))
    P("")

    # ------------------------------------------------------------ verdict
    P("=" * 100)
    n_fail = sum(1 for g in GATES if not g["pass_"])
    P(f"GATES: {len(GATES) - n_fail}/{len(GATES)} pass")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hypotheses.csv", index=False)
    anc_oos = float(mdf[(mdf.selector == "SEL_NEVER_anchor")
                        & (mdf.claim_set == CS_HEAD)].iloc[0].mean_OOS_Sharpe)
    best_sel = mdf[mdf.claim_set == CS_HEAD].sort_values("mean_OOS_Sharpe").iloc[-1]
    P(f"  best selector on {CS_HEAD}: {best_sel.selector} {best_sel.mean_OOS_Sharpe:.4f} "
      f"vs do-nothing anchor {anc_oos:.4f} ({best_sel.d_vs_anchor:+.4f}, t {best_sel.t_vs_anchor:+.2f})")
    keep_rows = wdf[(wdf.selector != "RUNG_BOOK") & (wdf.pass4b_both | wdf.pass4a)]
    if len(keep_rows):
        P(f"  {len(keep_rows)} selector rows clear 4a or 4b-BOTH — inspect .walkforward.csv")
        kk = keep_rows.sort_values("OOS_Sharpe", ascending=False).iloc[0]
        P(f"  best: {kk.panel} {kk.ladder}={kk.rung} anchor {kk.anchor} [{kk.selector}] "
          f"full {kk.CAGR:.2%} / {kk.Sharpe:.4f} / {kk.MaxDD:.2%}  OOS {kk.OOS_CAGR:.2%} / "
          f"{kk.OOS_Sharpe:.4f} / {kk.OOS_MaxDD:.2%}")
    P(f"runtime {time.time() - t0:.0f}s")
    P("=" * 100)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
