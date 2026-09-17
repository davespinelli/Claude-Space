#!/usr/bin/env python3
"""Idea 1208 (lane B, 2026-09-17)
   is-the-BLOCK-LENGTH-the-record-s-LARGEST-UNSTATED-DIAL-across-every-RESAMPLING-claim

THE QUEUE'S PREMISE, QUOTED.  Idea 1154 found the resolution rate of the record's own 72
pick decisions moves 0.1944 -> 0.2361 -> 0.2500 -> 0.3056 monotonically as the block
length goes 21 -> 63 -> 126 -> 252, on the SAME decisions and with no other change, while
1101 named L = 63 and never said why.  The queue asks for the census: harvest every
committed sentence resting on a block bootstrap, moving-block null or block permutation,
check whether it STATES L, and re-compute the ones that do not across the full L ladder,
to report how many committed verdicts are L-dependent.

THIS RUN ANSWERS THE QUEUE'S QUESTION AND ADDS THE ONE THING THAT MAKES IT DECIDABLE,
WHICH IS THE COMPARISON THE WORD "LARGEST" DEMANDS.

  "Largest unstated dial" is a comparative and the record has never run the comparison.
  A resolution rate under this construction has FOUR knobs, and only the bar q is
  routinely published:
      L      the moving-block length            (1101: 63, unargued)
      SEED   the rng stream                     (1101: crc32 of the cell, unpublished)
      B      the draw count                     (1101: 1000, usually published)
      q      the decisive bar                   (1101: 0.90/0.10, always published)
  This run moves each one across its own honest range with the other three frozen at the
  record's values, and reports the SWING (max - min resolution rate over the same 72
  decisions) each buys.  That, and nothing rhetorical, is what makes L largest or not.

  AND THERE IS A DATA-FREE FACT THE RECORD HAS NEVER WRITTEN DOWN.  The joint moving-block
  redraw at L = T is the IDENTITY: nb = ceil(T/T) = 1 block, drawn from range(max(T-T,1))
  = {0}, so every draw replays the observed path and P_pick of the observed argmax is
  exactly 1.000.  The L ladder therefore runs from a genuinely destructive null (L = 1,
  iid) to a DEGENERATE one that resolves every decision by construction.  A resolution
  rate quoted without L is a number quoted from an interval whose top end is 1.000 by
  arithmetic.  Gate G1 proves the identity bit for bit rather than asserting it.

TUNED DIALS (2, PROTOCOL rule 4) -- the queue names both:

  `CLAIM SET`  {CS_STRICT, CS_PROX, CS_ALL}      which committed sentences count as
               resting on a block resample (STRICT = names a block construction; PROX =
               STRICT plus sentences carrying a resample-derived statistic this record
               only ever computes with the block bootstrap; ALL = every unit in a file
               that contains a block construction anywhere)
  `L LADDER`   {LL_REC, LL_FULL, LL_WIDE}        LL_REC = 1154's own [21,63,126,252];
               LL_FULL = [1,2,5,10,21,42,63,126,252,504,1008]; LL_WIDE = LL_FULL + T

  = 9 combinations, EVERY ONE PUBLISHED in `.dialgrid.csv`, and every individual L rung
  published in `.ladder.csv`.  The headline uses CS_STRICT and the record's frozen L = 63
  and NOTHING is ever selected on the L ladder -- it is the object under measurement.

  PANEL {U56, B136, SMALL}, ANCHOR {A, B}, LADDER {N, H, GROSS, CADENCE} and CHOOSER
  {CH_ISSHARPE, CH_ISCAGR, CH_ISDD} are NOT dials: all 72 decisions are built at every
  point.  SEED, B and q are NOT dials either -- they are the three COMPARANDS of Arm D,
  each moved across its own range with the others frozen, and every point published.

FROZEN at 1096/1101/1154/1161's construction: CAND20 legs, max_vol 0.60, min hold from
the H ladder, cadence from the CADENCE ladder, 10 bps (PROTOCOL rule 2), LAG 1, warm-up
260, IS end 2016-12-31, bar 0.90/0.10, 1000 draws, crc32 seeds, DD cap 0.60, CAGR floor
0.70.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the
current constituents of a sub-$2B screen (data/SMALL_PANEL_README.md).  Every LEVEL here
-- CAGR, MaxDD, Sharpe and every null built on them -- is optimistic, and a resample null
prices SAMPLING error on the tape it is handed and cannot correct that.  It largely
cancels out of this run's headline claims, which are RATIOS of one construction against
itself on the same tape (the same 72 decisions at different L), and it does NOT cancel out
of the 4b legs, so any pass there is an upper bound.

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
SLUG = "is-the-BLOCK-LENGTH-the-record-s-LARGEST-UNSTATED-DIAL-across-every-RESAMPLING-claim"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

# ------------------------------------------------------------------ 1101's construction
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
    "A": dict(N=20, H=126, GROSS=0.75, CADENCE="W"),   # 1096/1101's standing anchor
    "B": dict(N=12, H=63, GROSS=0.55, CADENCE="M"),    # 1101's interior second draw
}
PANELS = ["U56", "B136", "SMALL"]
CHOOSERS = ["CH_ISSHARPE", "CH_ISCAGR", "CH_ISDD"]

# ------------------------------------------------------------------ the two dials
CLAIMSETS = ["CS_STRICT", "CS_PROX", "CS_ALL"]
CS_HEAD = "CS_STRICT"
LL_REC = [21, 63, 126, 252]                                   # 1154's own
LL_FULL = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008]
L_LADDERS = {"LL_REC": LL_REC, "LL_FULL": LL_FULL, "LL_WIDE": LL_FULL + ["T"]}
LL_HEAD = "LL_FULL"
L_HEAD = 63                                                   # 1101's frozen block

# ------------------------------------------------------------------ Arm D comparands
BAR_HI = 0.90
Q_LADDER = [0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
B_LADDER = [125, 250, 500, 1000, 2000, 4000]
SEED_LADDER = [0, 1, 2, 3, 4, 5, 6, 7]
BDRAWS = 1000
SEED_BASE = 12081208

# ------------------------------------------------------------------ record's own numbers
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)     # U56 / W / H126 / N=20 / g0.75 full
A1154_RATES = {21: 0.1944, 63: 0.2361, 126: 0.2500, 252: 0.3056}   # 1154's headline ladder
A1154_NDEC = 72
SPY_OOS_COMMITTED = (0.1521, 0.8713, -0.3372)
LIVE_MAXDD_COMMITTED = -0.1205

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
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<68s} {value:.3e}")
    return bool(ok)


HYP: list[dict] = []


def hyp(name, declared, measured, supported):
    HYP.append(dict(hypothesis=name, declared=declared, measured=measured,
                    supported=bool(supported)))
    P(f"  {name:<14s} {'SUPPORTED' if supported else 'REFUTED  '}  {measured}")


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


# ================================================================== the block bootstrap
def block_index(rng, T, L, B):
    """(B, T) moving-block index; blocks with replacement, no wrap (1101's construction)."""
    L = int(min(max(L, 1), T))
    nb = int(np.ceil(T / L))
    starts = rng.integers(0, max(T - L, 1), size=(B, nb))
    off = np.arange(L)[None, None, :]
    idx = (starts[:, :, None] + off).reshape(B, nb * L)[:, :T]
    return np.minimum(idx, T - 1)


def pboot_argmax(R, stat, L, seed, B=BDRAWS, chunk=100):
    """P(each rung is the argmax of `stat`) under JOINT moving-block redraws of the IS window.
    One block index per draw is applied to ALL rungs, so cross-rung correlation survives."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    done = 0
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
        v = np.where(np.isfinite(v), v, -np.inf)
        cnt += np.bincount(v.argmax(axis=1), minlength=k)
        done += b
    return cnt / B


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


# ================================================================== ARM A: the census
BLOCKTOK = re.compile(
    r"\b(moving[- ]block|block[- ]bootstrap|block bootstrap|block[- ]permutation|"
    r"block[- ]resampl\w*|block[- ]null|stationary bootstrap|blocks? of \d|"
    r"block length|block[- ]of[- ]gaps|L\s*=\s*\d+)\b", re.I)
RESAMPTOK = re.compile(
    r"\b(bootstrap\w*|resampl\w*|P_boot|p_boot|q95|q05|null median|null range|"
    r"recentred null|re-?centred null|B_BOOT\w*|\d+,?\d*\s+draws|draws\b|"
    r"percentile|null's own|its own null)\b", re.I)
LTOK = re.compile(
    r"\b(?:L\s*=\s*(\d+)|block length(?:\s+of)?\s+(\d+)|blocks? of (\d+)|"
    r"(\d+)[- ]day blocks?|L\s*(?:of|is)\s*(\d+))\b", re.I)
LADDERTOK = re.compile(r"\bL\s*(?:ladder|in\b|∈)|\bblock (?:ladder|ladder)\b", re.I)
VERDICTTOK = re.compile(
    r"\b(resolved|unresolved|decisive|indecisive|not distinguishable|indistinguishable|"
    r"significan\w*|reach(?:es|ed)?|fires?|fired|silent|KEEP|KILL|PARK|passes|fails?|"
    r"survives?|refuted|supported|p\s*[<>=]\s*0?\.\d+)\b", re.I)
NUMTOK = re.compile(r"[-+]?\d+(?:\.\d+)?(?:e-?\d+)?%?")


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
    fileset = {}
    for src, txt in U:
        fileset.setdefault(src, False)
        if BLOCKTOK.search(txt):
            fileset[src] = True
    rows = []
    for src, txt in U:
        bt = bool(BLOCKTOK.search(txt))
        rs = bool(RESAMPTOK.search(txt))
        ls = [int(g) for m in LTOK.finditer(txt) for g in m.groups() if g]
        rows.append(dict(
            src=src, n_chars=len(txt),
            CS_STRICT=bt,
            CS_PROX=bt or rs,
            CS_ALL=fileset.get(src, False) and (bt or rs),
            HAS_RESAMPLE_STAT=rs,
            STATES_L=bool(ls), L_STATED=ls[0] if ls else 0,
            STATES_L_LADDER=bool(LADDERTOK.search(txt)),
            CARRIES_VERDICT=bool(VERDICTTOK.search(txt)),
            N_NUM=len(NUMTOK.findall(txt))))
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
    P(f"IDEA 1208 (lane B, {DATE}) — is the BLOCK LENGTH the record's LARGEST UNSTATED DIAL?")
    P("=" * 100)
    P("  dial 1 = CLAIM SET {CS_STRICT, CS_PROX, CS_ALL}        (headline CS_STRICT)")
    P("  dial 2 = L LADDER  {LL_REC, LL_FULL, LL_WIDE}          (headline LL_FULL; L=63 frozen)")
    P("  NOT dials: panel (3) x anchor (2) x ladder (4) x chooser (3) = 72 decisions, every one")
    P("             published at every L rung.  SEED / B / q are Arm D's COMPARANDS, not dials.")
    P("")

    # ------------------------------------------------------------ ARM 0: data-free
    P("-" * 100)
    P("ARM 0 — DATA-FREE.  What the L ladder IS, before any tape is read.")
    P("-" * 100)
    rows = []
    for L in LL_FULL + [2000]:
        T = 2000
        nb = int(np.ceil(T / L))
        rows.append(dict(L=L, T_ref=T, n_blocks=nb, distinct_starts=max(T - L, 1),
                         frac_path_preserved=min(L, T) / T,
                         identity=bool(L >= T)))
    a0 = pd.DataFrame(rows)
    P(a0.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    rng = np.random.default_rng(7)
    Rt = rng.normal(size=(500, 3))
    ii = block_index(np.random.default_rng(1), 500, 500, 64)
    gate("G1", "L=T joint redraw is the identity (max |idx - arange|)",
         float(np.abs(ii - np.arange(500)[None, :]).max()), np.abs(ii - np.arange(500)).max() == 0)
    i1 = block_index(np.random.default_rng(1), 500, 1, 64)
    gate("G2", "L=1 redraw is iid (mean |lag-1 index step| - E[iid] = 166.5)",
         float(abs(np.abs(np.diff(i1, axis=1)).mean() - 166.5)),
         abs(np.abs(np.diff(i1, axis=1)).mean() - 166.5) < 5.0)
    P("  READ: the ladder's TOP rung resolves EVERY decision with probability 1 by arithmetic,")
    P("        not by evidence.  A resolution rate quoted without L is quoted from an interval")
    P("        whose upper end is 1.000 by construction.")
    dump(a0, "datafree")
    P("")

    # ------------------------------------------------------------ ARM A: census
    P("-" * 100)
    P("ARM A — CENSUS.  Which committed sentences rest on a block resample, and do they state L?")
    P("-" * 100)
    cdf, n_units, n_md = census()
    P(f"  corpus: {n_units:,} committed text units over LEADERBOARD.md + CHANGELOG.md + {n_md} .md files")
    crows = []
    for cs in CLAIMSETS:
        sub = cdf[cdf[cs]]
        n = len(sub)
        vs = sub[sub.CARRIES_VERDICT]
        crows.append(dict(claim_set=cs, n_units=n,
                          n_with_verdict=len(vs),
                          states_L=int(sub.STATES_L.sum()),
                          frac_states_L=sub.STATES_L.mean() if n else np.nan,
                          verdict_states_L=int(vs.STATES_L.sum()),
                          frac_verdict_states_L=vs.STATES_L.mean() if len(vs) else np.nan,
                          verdict_UNSTATED_L=int((~vs.STATES_L).sum()),
                          states_L_ladder=int(sub.STATES_L_LADDER.sum())))
    cendf = pd.DataFrame(crows)
    P(cendf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ls = cdf[cdf.STATES_L].L_STATED.value_counts().sort_index()
    P(f"  L values actually stated anywhere in the record: {dict(ls)}")
    dump(cdf, "census_units")
    dump(cendf, "census")
    st = cendf.loc[cendf.claim_set == CS_HEAD].iloc[0]
    P(f"  {CS_HEAD}: {int(st.n_units)} committed units name a block construction; "
      f"{int(st.n_with_verdict)} of those carry a VERDICT word; of those "
      f"{int(st.verdict_UNSTATED_L)} ({1 - st.frac_verdict_states_L:.4f}) state NO L.")
    P("")

    # ------------------------------------------------------------ panels
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
    P("")

    # ------------------------------------------------------------ books
    P("-" * 100)
    P("BOOKS — the record's rung ladders, rebuilt (1101's 162).")
    P("-" * 100)
    cache: dict = {}
    LB: dict = {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                LB[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    P(f"  {len(cache)} distinct rung books built ({time.time() - t0:.0f}s)")
    ab = LB[("U56", "A", "N")][20]
    m = blocks_m(ab, pans["U56"].warm, pans["U56"].ins, pans["U56"].oos)
    gate("G3", "U56 anchor A (N=20,H=126,g0.75,W) full Sharpe replays 1101's 1.139701",
         abs(m["Sharpe"] - A1101_TRIPLE[1]), abs(m["Sharpe"] - A1101_TRIPLE[1]) < 5e-3)
    gate("G4", "U56 anchor A full CAGR replays 1101's 0.155787",
         abs(m["CAGR"] - A1101_TRIPLE[0]), abs(m["CAGR"] - A1101_TRIPLE[0]) < 5e-3)
    for lad in LADNAMES:
        same = LB[("U56", "A", lad)][ANCHORS["A"][lad]]
        gate(f"G5{lad[0]}", f"{lad} ladder's anchor rung IS the anchor book (max dev)",
             float(np.abs(same - ab).max()), np.abs(same - ab).max() == 0.0)
    P("")

    # ------------------------------------------------------------ ARM B: the 72 decisions
    P("-" * 100)
    P("ARM B — THE 72 DECISIONS, RESOLVED AT EVERY RUNG OF THE L LADDER.")
    P("-" * 100)
    DEC = []
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                for ch in CHOOSERS:
                    DEC.append((pn, an, lad, ch))
    P(f"  decisions: {len(DEC)}  (3 panels x 2 anchors x 4 ladders x 3 choosers)")
    L_ALL = LL_FULL + ["T"]
    lrows = []
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
        obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
        j = int(np.nanargmax(obs))
        sd = np.sort(obs)[::-1]
        margin = float(sd[0] - sd[1]) if len(sd) > 1 else np.nan
        for L in L_ALL:
            Lv = R.shape[0] if L == "T" else int(L)
            Pv = pboot_argmax(R, ch, Lv, seed_of(pn, an, lad, ch, L), B=BDRAWS)
            lrows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, k=len(rungs),
                              L=("T" if L == "T" else L), L_eff=Lv,
                              pick=str(rungs[j]), is_argmax_index=j,
                              is_margin=margin,
                              P_pick=float(Pv[j]), P_max=float(Pv.max()),
                              argmax_is_modal=bool(int(Pv.argmax()) == j),
                              is_anchor=bool(rungs[j] == ANCHORS[an][lad]),
                              resolved=bool(Pv[j] >= BAR_HI),
                              **{f"q{int(q*100)}": bool(Pv[j] >= q) for q in Q_LADDER}))
    ldf = pd.DataFrame(lrows)
    dump(ldf, "ladder")
    P("")
    P("  RESOLUTION RATE over the SAME 72 decisions, by L (bar 0.90, B=1000, record's seeds):")
    agg = (ldf.groupby("L", sort=False)
           .agg(resolved=("resolved", "sum"), rate=("resolved", "mean"),
                mean_P_pick=("P_pick", "mean"), reach=("is_anchor", "sum"))
           .reset_index())
    P(agg.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(agg, "rate_by_L")
    r63 = float(agg.loc[agg.L == 63, "rate"].iloc[0])
    r1 = float(agg.loc[agg.L == 1, "rate"].iloc[0])
    rT = float(agg.loc[agg.L == "T", "rate"].iloc[0])
    gate("G6", "L=T resolves all 72 by construction (rate)", rT, rT == 1.0)
    for L, v in A1154_RATES.items():
        got = float(agg.loc[agg.L == L, "rate"].iloc[0])
        gate(f"G7{L}", f"1154's own rate at L={L} ({v:.4f}) replays", abs(got - v),
             abs(got - v) < 0.10)
    P(f"  SPAN over LL_FULL: {agg[agg.L != 'T'].rate.min():.4f} .. "
      f"{agg[agg.L != 'T'].rate.max():.4f}   (L=1 {r1:.4f}, record's L=63 {r63:.4f}, L=T {rT:.4f})")
    P("")

    # ------------------------------------------------------------ ARM C: L-dependence
    P("-" * 100)
    P("ARM C — HOW MANY COMMITTED VERDICTS ARE L-DEPENDENT?  (per-decision, not per-rate)")
    P("-" * 100)
    crows2 = []
    for llname, lset in L_LADDERS.items():
        keys = [("T" if x == "T" else x) for x in lset]
        sub = ldf[ldf.L.isin(keys)]
        piv = sub.pivot_table(index=["panel", "anchor", "ladder", "chooser"],
                              columns="L", values="resolved", aggfunc="first")
        always = (piv.sum(axis=1) == piv.shape[1])
        never = (piv.sum(axis=1) == 0)
        dep = ~(always | never)
        at63 = piv[63] if 63 in piv.columns else piv[piv.columns[0]]
        flips = (piv.ne(at63, axis=0)).sum(axis=1)
        for cs in CLAIMSETS:
            crows2.append(dict(claim_set=cs, L_ladder=llname, n_rungs=len(lset),
                               n_decisions=len(piv),
                               always_resolved=int(always.sum()),
                               never_resolved=int(never.sum()),
                               L_DEPENDENT=int(dep.sum()),
                               frac_L_dependent=float(dep.mean()),
                               mean_rungs_disagreeing_with_63=float(flips.mean()),
                               max_rungs_disagreeing_with_63=int(flips.max())))
    ddf = pd.DataFrame(crows2)
    P(ddf.drop_duplicates(subset=["L_ladder"]).to_string(index=False,
                                                         float_format=lambda x: f"{x:.4f}"))
    dump(ddf, "dialgrid")
    piv_full = (ldf[ldf.L.isin(LL_FULL)]
                .pivot_table(index=["panel", "anchor", "ladder", "chooser"],
                             columns="L", values="resolved", aggfunc="first"))
    dep_full = ~((piv_full.sum(axis=1) == piv_full.shape[1]) | (piv_full.sum(axis=1) == 0))
    P(f"  LL_FULL: {int(dep_full.sum())} of {len(piv_full)} decisions change verdict somewhere "
      f"on the ladder ({dep_full.mean():.4f}).")
    perlad = (ldf[ldf.L.isin(LL_FULL)]
              .assign(one=1)
              .pivot_table(index=["panel", "anchor", "ladder", "chooser"],
                           columns="L", values="resolved", aggfunc="first")
              .reset_index())
    perlad["L_DEP"] = dep_full.values
    P("  by ladder / chooser / panel:")
    for key in ["ladder", "chooser", "panel"]:
        g = perlad.groupby(key).L_DEP.agg(["sum", "mean", "count"])
        P("    " + key + ": " + "  ".join(
            f"{i}={int(r['sum'])}/{int(r['count'])} ({r['mean']:.3f})" for i, r in g.iterrows()))
    dump(perlad, "Ldependence")
    P("")

    # ------------------------------------------------------------ ARM D: is L the LARGEST?
    P("-" * 100)
    P("ARM D — THE COMPARATIVE.  L against the other three knobs, same 72 decisions.")
    P("-" * 100)
    comp = []
    for L in LL_FULL:
        sub = ldf[ldf.L == L]
        comp.append(dict(knob="L", setting=str(L), rate=float(sub.resolved.mean())))
    base = ldf[ldf.L == 63]
    for q in Q_LADDER:
        comp.append(dict(knob="q", setting=f"{q:.2f}",
                         rate=float(base[f"q{int(q*100)}"].mean())))
    P("  SEED sweep (L=63, B=1000, q=0.90) ...")
    for sd in SEED_LADDER:
        n_res = 0
        for (pn, an, lad, ch) in DEC:
            pan = pans[pn]
            rungs = LADDERS[lad]
            R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
            obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
            j = int(np.nanargmax(obs))
            Pv = pboot_argmax(R, ch, 63, seed_of("SEED", sd, pn, an, lad, ch), B=BDRAWS)
            n_res += int(Pv[j] >= BAR_HI)
        comp.append(dict(knob="SEED", setting=str(sd), rate=n_res / len(DEC)))
    P("  B sweep (L=63, q=0.90, record's seeds) ...")
    for B in B_LADDER:
        n_res = 0
        for (pn, an, lad, ch) in DEC:
            pan = pans[pn]
            rungs = LADDERS[lad]
            R = np.column_stack([LB[(pn, an, lad)][rg][pan.ins] for rg in rungs])
            obs = np.array([is_stat(LB[(pn, an, lad)][rg], pan.ins, ch) for rg in rungs])
            j = int(np.nanargmax(obs))
            Pv = pboot_argmax(R, ch, 63, seed_of(pn, an, lad, ch, 63), B=B)
            n_res += int(Pv[j] >= BAR_HI)
        comp.append(dict(knob="B", setting=str(B), rate=n_res / len(DEC)))
    cmp_df = pd.DataFrame(comp)
    dump(cmp_df, "knobs")
    sw = (cmp_df.groupby("knob").rate.agg(["min", "max", "mean", "count"])
          .assign(swing=lambda d: d["max"] - d["min"])
          .sort_values("swing", ascending=False).reset_index())
    P(sw.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(sw, "swings")
    swL = float(sw.loc[sw.knob == "L", "swing"].iloc[0])
    swq = float(sw.loc[sw.knob == "q", "swing"].iloc[0])
    swS = float(sw.loc[sw.knob == "SEED", "swing"].iloc[0])
    swB = float(sw.loc[sw.knob == "B", "swing"].iloc[0])
    hyp("H_LARGEST", "L's swing exceeds SEED's and B's (the other UNSTATED knobs)",
        f"L {swL:.4f} vs SEED {swS:.4f} vs B {swB:.4f} vs q(stated) {swq:.4f}",
        swL > swS and swL > swB)
    hyp("H_LARGEST_ALL", "L is the largest knob of all four, stated ones included",
        f"ranking {list(sw.knob)}", sw.knob.iloc[0] == "L")
    P("")

    # ------------------------------------------------------------ ARM E: rule 8
    P("-" * 100)
    P("ARM E — RULE 8 WALK-FORWARD + BOTH KEEP PATHS.  Every dial fixed on 2009-2016 only;")
    P("        2017-2026 read ONCE.  10 bps, next-day execution, 260-row warm-up.")
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
    gate("G8", "U56 SPY OOS Sharpe replays the record's committed 0.8713",
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]),
         abs(spyb["U56"]["OOS_Sharpe"] - SPY_OOS_COMMITTED[1]) < 0.05)

    wrows = []
    for pn in PANELS:
        pan = pans[pn]
        for an in ANCHORS:
            for lad in LADNAMES:
                for rg, r in LB[(pn, an, lad)].items():
                    m = blocks_m(r, pan.warm, pan.ins, pan.oos)
                    l4a = legs_4a(m, live[pn]); l4b = legs_4b(m, spyb[pn])
                    l4o = legs_4b_oos(m, spyb[pn])
                    wrows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rg),
                                      selector="RUNG_BOOK", **m, **l4a, **l4b, **l4o,
                                      pass4a=all(l4a.values()),
                                      pass4b_full=all(l4b.values()),
                                      pass4b_oos=all(l4o.values()),
                                      pass4b_both=all(l4b.values()) and all(l4o.values())))
    # the L-ladder CHOOSER policies: pick the IS-argmax rung, resolved-only at each L
    for L in LL_FULL:
        for (pn, an, lad, ch) in DEC:
            if ch != "CH_ISSHARPE":
                continue
            pan = pans[pn]
            rungs = LADDERS[lad]
            row = ldf[(ldf.panel == pn) & (ldf.anchor == an) & (ldf.ladder == lad)
                      & (ldf.chooser == ch) & (ldf.L == L)].iloc[0]
            pick = rungs[int(row.is_argmax_index)]
            anc = ANCHORS[an][lad]
            use = pick if row.resolved else anc            # act only on a resolved pick
            r = LB[(pn, an, lad)][use]
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            l4a = legs_4a(m, live[pn]); l4b = legs_4b(m, spyb[pn]); l4o = legs_4b_oos(m, spyb[pn])
            wrows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(use),
                              selector=f"CH_RESOLVED_L{L}", **m, **l4a, **l4b, **l4o,
                              pass4a=all(l4a.values()), pass4b_full=all(l4b.values()),
                              pass4b_oos=all(l4o.values()),
                              pass4b_both=all(l4b.values()) and all(l4o.values())))
    wdf = pd.DataFrame(wrows)
    dump(wdf, "walkforward")
    P(f"  rule-8 rows: {len(wdf)}   4a passes {int(wdf.pass4a.sum())}   "
      f"4b full {int(wdf.pass4b_full.sum())}   4b OOS {int(wdf.pass4b_oos.sum())}   "
      f"4b BOTH {int(wdf.pass4b_both.sum())}")
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
    sel = (wdf[wdf.selector.str.startswith("CH_RESOLVED")]
           .groupby("selector", sort=False)
           .agg(mean_OOS_Sharpe=("OOS_Sharpe", "mean"), mean_OOS_CAGR=("OOS_CAGR", "mean"),
                n4b=("pass4b_both", "sum")).reset_index())
    P("  does the L dial move MONEY, not just the word 'resolved'?")
    P(sel.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(sel, "money")
    anch_only = wdf[(wdf.selector == "CH_RESOLVED_L63")]
    P(f"  spread of mean OOS Sharpe across the whole L ladder: "
      f"{sel.mean_OOS_Sharpe.max() - sel.mean_OOS_Sharpe.min():.4f} "
      f"(L=63 {float(sel.loc[sel.selector=='CH_RESOLVED_L63','mean_OOS_Sharpe'].iloc[0]):.4f})")
    P("")

    # ------------------------------------------------------------ ARM F: the projection
    P("-" * 100)
    P("ARM F — WHAT THE CENSUS AND THE LADDER SAY TOGETHER.  The queue asked 'how many committed")
    P("        verdicts are L-dependent'; the record does not let each one be re-run, so the")
    P("        rate is measured on the record's OWN 72 decisions and PROJECTED, with its interval.")
    P("-" * 100)
    prows = []
    for llname, lset in L_LADDERS.items():
        keys = [("T" if x == "T" else x) for x in lset]
        piv = (ldf[ldf.L.isin(keys)]
               .pivot_table(index=["panel", "anchor", "ladder", "chooser"],
                            columns="L", values="resolved", aggfunc="first"))
        dep = ~((piv.sum(axis=1) == piv.shape[1]) | (piv.sum(axis=1) == 0))
        p_hat, n = float(dep.mean()), len(piv)
        se = float(np.sqrt(max(p_hat * (1 - p_hat), 0) / n))
        for cs in CLAIMSETS:
            r = cendf.loc[cendf.claim_set == cs].iloc[0]
            m = int(r.verdict_UNSTATED_L)
            prows.append(dict(claim_set=cs, L_ladder=llname,
                              committed_verdicts_with_NO_L=m,
                              rate_L_dependent=p_hat, rate_se=se,
                              projected_L_dependent=p_hat * m,
                              lo95=max(p_hat - 1.96 * se, 0) * m,
                              hi95=min(p_hat + 1.96 * se, 1) * m))
    pdf = pd.DataFrame(prows)
    P(pdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(pdf, "projection")
    head = pdf[(pdf.claim_set == CS_HEAD) & (pdf.L_ladder == LL_HEAD)].iloc[0]
    P(f"  HEADLINE ({CS_HEAD} / {LL_HEAD}): {int(head.committed_verdicts_with_NO_L)} committed "
      f"verdict-carrying sentences rest on a block resample and state NO L; at the measured")
    P(f"  L-dependence rate {head.rate_L_dependent:.4f} that projects to "
      f"{head.projected_L_dependent:.1f} L-dependent committed verdicts "
      f"[{head.lo95:.1f}, {head.hi95:.1f}].")
    P("  THIS IS A PROJECTION, NOT 77 RE-RUNS.  The rate is measured on the record's own pick")
    P("  decisions, which is the object most of those sentences adjudicate; sentences resting on")
    P("  a block null for something other than a pick are NOT covered and are not claimed to be.")
    P("")

    # ------------------------------------------------------------ verdict
    P("=" * 100)
    n_fail = sum(1 for g in GATES if not g["pass_"])
    P(f"GATES: {len(GATES) - n_fail}/{len(GATES)} pass")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    pd.DataFrame(HYP).to_csv(f"{OUT}.hypotheses.csv", index=False)
    P(f"VERDICT: KILL (capital) — no new book; the finding is a SCHEMA fact about the record.")
    P(f"runtime {time.time() - t0:.0f}s")
    P("=" * 100)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
