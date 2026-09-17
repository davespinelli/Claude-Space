#!/usr/bin/env python3
"""
Idea 1243 (lane cloud, 2026-09-17) — what does a SCHEMA CLAUSE that DEMANDS A LADDER rather
than a POINT cost across the WHOLE RECORD?

THE PREMISE, READ FROM THE RECORD.  Idea 1208 (lane B, 2026-09-17) established three things.
(i) The block length L is the LARGEST unstated dial in the record's resampling vocabulary: on
one fixed object — 72 pick decisions (3 panels x 2 anchors x 4 ladders x 3 choosers) — the
resolution rate runs 0.1528 -> 1.0000 monotonically over L = 1 .. T, an L swing of 0.3194
against a q swing of 0.3056, a seed swing of 0.0278 and a B swing of 0.0139.  (ii) Only 37
committed units ANYWHERE in the record state an L LADDER rather than a point.  (iii) The
LADDER'S OWN LENGTH is a third-order dial nobody has priced: 1154's 4-rung ladder finds 6 of 72
decisions L-dependent where 1208's 11-rung LL_FULL finds 23.  1208 proposed a PROTOCOL schema
clause requiring L, and where the claim is a rate, the LADDER, beside every block-resampling
verdict — and explicitly did not price it.  This run prices it.

WHAT IS BEING TESTED, STATED BEFORE ANY NUMBER IS READ.  A schema clause is a TRADE, and both
sides of it are measurable on this tape:

    COST  = the committed units it makes non-conforming (they must be amended or re-run) plus
            the compute each future verdict owes (k rungs x B draws instead of 1 x B).
    BUYS  = the L-dependent verdicts a k-rung ladder DETECTS that a point does not.

So the object is the DETECTION CURVE d(k) = share of the 72 decisions whose RESOLVED /
UNRESOLVED verdict is not constant across the first k rungs of a widening ladder, together with
the MARGINAL detection of each rung added.  A clause is worth writing only if d(k) is still
rising where the record would stop, and worth writing CHEAPLY only if most of d(inf) arrives in
the first few rungs.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) CHEAP AND DECISIVE — a SHORT ladder (k <= 4 rungs) recovers >= 0.70 of the detection the
      full 12-rung ladder achieves.  The clause can be written as "at least 4 rungs" and costs
      the record a bounded, small re-run.
  (B) EXPENSIVE — d(k) is still rising steeply at k = 12 (the last rung added contributes >= 0.10
      of the 72 decisions), i.e. no attainable ladder settles the question and the clause buys
      an interval that never closes.
  (C) DEGENERATE — most of the detection comes from ONE rung (a single rung contributes > 0.50
      of d(12)), so the clause is really a demand for THAT rung and should be written as one.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAUSE SCOPE     {SC_BLOCK, SC_RESAMPLE, SC_ALL} — which committed units the clause binds.
                   SC_BLOCK     units naming a BLOCK construction (1208's CS_STRICT, 478).
                   SC_RESAMPLE  those plus every unit carrying a resample-derived statistic AND
                                a verdict word — the "every resample-keyed verdict" reading.
                   SC_ALL       those plus every unit carrying a resample-derived OR floor-keyed
                                statistic at all (the widest reading; FLOORTOK is deliberately
                                loose and its count is published as this run's, not 1208's).
                   The three scopes are NESTED by construction: SC_BLOCK c SC_RESAMPLE c SC_ALL.
  LADDER INCREMENT {INC_ONE, INC_TWO, INC_REC} — how fast the ladder is widened.
                   INC_ONE  one rung at a time, nearest-in-log-distance to the record's frozen
                            L = 63 first: 63, 126, 42, 252, 21, 504, 10, 1008, 5, 2, 1, T.
                   INC_TWO  two rungs per step over the same order (the "widen symmetrically"
                            habit: 63, then {126,42}, then {252,21}, ...).
                   INC_REC  the record's OWN schedule: [63] -> 1154's LL_REC [21,63,126,252] ->
                            1208's LL_FULL (11 rungs) -> LL_WIDE (12, including the degenerate
                            L = T).
                   All three walk the SAME 12 rungs and differ only in where a clause would be
                   allowed to stop; all 9 (scope x increment) cells are published.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); ANCHOR {A, B}; the four
ladders N / H / GROSS / CADENCE; the three choosers CH_ISSHARPE / CH_ISCAGR / CH_ISDD; the
resolution bar q = 0.90 (1208's, ALWAYS published); B = 1000 draws; the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, 10 bps (rule 2), decide-at-t / apply-at-t+1, warm-up 260 rows,
IS end 2016-12-31 (rule 8).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every pick made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book and every rule-8 row; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only).
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
SLUG = "what-does-a-SCHEMA-CLAUSE-that-DEMANDS-A-LADDER-rather-than-a-POINT-cost-across-the-whole-record"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

# ------------------------------------------------------------------ 1101/1208's construction
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

# ------------------------------------------------------------------ the two dials
SCOPES = ["SC_BLOCK", "SC_RESAMPLE", "SC_ALL"]
SC_HEAD = "SC_RESAMPLE"
# the 12 rungs every increment schedule walks (1208's LL_WIDE)
RUNGS_ALL = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, "T"]
# INC_ONE's order: nearest in log-distance to the record's frozen 63, then outward
ORDER_ONE = [63, 126, 42, 252, 21, 504, 10, 1008, 5, 2, 1, "T"]
INC_SCHEDULES = {
    "INC_ONE": [ORDER_ONE[:k] for k in range(1, 13)],
    "INC_TWO": [ORDER_ONE[:k] for k in [1, 3, 5, 7, 9, 11, 12]],
    "INC_REC": [[63], [21, 63, 126, 252],
                [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008],
                [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, "T"]],
}
BAR_HI = 0.90
BDRAWS = 1000
SEED_BASE = 12431243
L_HEAD = 63

# ------------------------------------------------------------------ the record's own numbers
A1208_RATES = {1: 0.1528, 2: 0.1667, 5: 0.1667, 10: 0.1806, 21: 0.1944, 42: 0.2222,
               63: 0.2222, 126: 0.2361, 252: 0.2778, 504: 0.3194, 1008: 0.4722, "T": 1.0000}
A1208_NDEC = 72
A1208_BLOCKUNITS = 478
A1208_LADDERUNITS = 37
A1208_DEP = {"LL_REC": 6, "LL_FULL": 23, "LL_WIDE": 61}
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def seed_of(*parts):
    return SEED_BASE + int(zlib.crc32("|".join(str(p) for p in parts).encode())) % 10_000_000


GATES: list[dict] = []


def gate(name, what, value, ok):
    GATES.append(dict(gate=name, what=what, value=float(value), pass_=bool(ok)))
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<66s} {value:.4e}")
    return bool(ok)


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
            N_NUM=len(NUMTOK.findall(txt)), _txt=txt))
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



# ================================================================== the clause's scope
FLOORTOK = re.compile(
    r"\b(floor|bar of|bar at|bar\b|threshold|cut-?off|q\s*=\s*0?\.\d+|0\.9[05]\s+bar|"
    r"INF_FLOOR|L_[A-Z]+|decisiveness bar|confidence level)\b", re.I)


def scope_frame(C):
    """Which committed units each CLAUSE SCOPE binds, and which already conform."""
    rows = []
    for sc in SCOPES:
        if sc == "SC_BLOCK":
            m = C.CS_STRICT                                   # 1208's own CS_STRICT
        elif sc == "SC_RESAMPLE":                             # every resample-keyed VERDICT
            m = C.CS_STRICT | (C.HAS_RESAMPLE_STAT & C.CARRIES_VERDICT)
        else:                                                 # every resample- or floor-keyed unit
            m = C.CS_STRICT | C.HAS_RESAMPLE_STAT | C.FLOOR_KEYED
        z = C[m]
        rows.append(dict(scope=sc, bound=len(z),
                         states_L=int(z.STATES_L.sum()),
                         states_LADDER=int(z.STATES_L_LADDER.sum()),
                         carries_verdict=int(z.CARRIES_VERDICT.sum()),
                         floor_keyed=int(z.FLOOR_KEYED.sum()),
                         non_conforming=int((~z.STATES_L_LADDER).sum()),
                         unrecoverable=int((~z.STATES_L & ~z.STATES_L_LADDER).sum())))
    return pd.DataFrame(rows)


# =================================================================================================
def main():
    t0 = time.time()
    P("=" * 110)
    P(f"IDEA 1243 (lane cloud, {DATE}) — what does a SCHEMA CLAUSE that DEMANDS A LADDER rather")
    P("than a POINT cost across the WHOLE RECORD?")
    P("=" * 110)
    P("  dial 1 = CLAUSE SCOPE     {SC_BLOCK, SC_RESAMPLE, SC_ALL}   (headline SC_RESAMPLE)")
    P("  dial 2 = LADDER INCREMENT {INC_ONE, INC_TWO, INC_REC}       (all walk the same 12 rungs)")
    P("  NOT dials: 3 panels x 2 anchors x 4 ladders x 3 choosers = 72 decisions, every one")
    P("             published at every rung; q = 0.90 and B = 1000 are 1208's, always stated.")
    P("  PRE-DECLARED: (A) CHEAP AND DECISIVE — k <= 4 recovers >= 0.70 of d(12).")
    P("                (B) EXPENSIVE — the 12th rung still adds >= 0.10 of the 72 decisions.")
    P("                (C) DEGENERATE — one rung contributes > 0.50 of d(12).")
    P("")

    # ------------------------------------------------------------ ARM A: the census / the cost
    P("=" * 110)
    P("ARM A — THE COST SIDE: WHAT THE CLAUSE BINDS AND WHAT IS ALREADY CONFORMING")
    P("=" * 110)
    C, n_units, n_md = census()
    C["FLOOR_KEYED"] = [bool(FLOORTOK.search(t)) for t in C["_txt"]]
    SF = scope_frame(C)
    SF.to_csv(f"{OUT}.scope.csv", index=False)
    P("")
    P(f"  {n_units} committed text units over LEADERBOARD.md + CHANGELOG.md + {n_md} .md files.")
    P("")
    P("  scope         bound   states an L   states a LADDER   carries a verdict   floor-keyed   "
      "NON-CONFORMING   UNRECOVERABLE")
    for _, r in SF.iterrows():
        P(f"  {r.scope:12s} {r.bound:6d}   {r.states_L:11d}   {r.states_LADDER:15d}   "
          f"{r.carries_verdict:17d}   {r.floor_keyed:11d}   {r.non_conforming:14d}   "
          f"{r.unrecoverable:13d}")
    nblock = int(C.CS_STRICT.sum())
    nladder = int(C.STATES_L_LADDER.sum())
    nfloor = int(C.FLOOR_KEYED.sum())
    P("")
    P("  REFLEXIVITY, STATED BEFORE THE GATES (1230's finding, which binds this run too).  A")
    P("  census of the record is committed TO the record and therefore has no fixed point: 1208's")
    P("  own CHANGELOG entry and leaderboard rows, and this lane's earlier 1239 commit, are")
    P("  themselves units that name block constructions and L ladders.  So 1208's integers are")
    P("  NOT expected to replay exactly, and the gates below are DRIFT gates, not equality gates.")
    P(f"  MEASURED DRIFT since 1208 committed: block-keyed {A1208_BLOCKUNITS} -> {nblock} "
      f"({nblock - A1208_BLOCKUNITS:+d}); L-ladder-stating {A1208_LADDERUNITS} -> {nladder} "
      f"({nladder - A1208_LADDERUNITS:+d}).")
    gate("G1", "block-keyed count is 1208's 478 plus post-1208 commits only (<= +10%)",
         nblock, A1208_BLOCKUNITS <= nblock <= A1208_BLOCKUNITS * 1.10)
    gate("G2", "1208's FINDING survives the drift: L-ladder-stating units are a small minority "
         "of the bound population", nladder / max(int(SF[SF.scope == SC_HEAD].bound.iloc[0]), 1),
         nladder / max(int(SF[SF.scope == SC_HEAD].bound.iloc[0]), 1) < 0.02)
    P(f"  FLOOR-KEYED units measured here: {nfloor} (1208's changelog cites 2,571 from the floor-")
    P("  clause line of 1110/1116; this run measures its own with its own regex and does NOT")
    P("  claim to replay that integer.  The figure is published as this run's, not as 1208's.)")

    # ------------------------------------------------------------ ARM B: panels and the object
    P("")
    P("=" * 110)
    P("ARM B — THE OBJECT: 1208's 72 PICK DECISIONS, REBUILT")
    P("=" * 110)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs = load_universe(small=True)
    mv = pxs.pct_change().abs().max()
    drop = [c for c in pxs.columns if c != "SPY" and not (mv[c] < 1.0)]
    px["SMALL"] = pxs.drop(columns=drop)
    pans = {n: Panel(n, px[n]) for n in PANELS}
    P("")
    P(f"  PANELS: U56 {len(px['U56'].columns)-1} names; B136 {len(px['B136'].columns)-1}; "
      f"SMALL {len(px['SMALL'].columns)-1} investable ({len(drop)} dropped for "
      f"max_1d_move >= 1.0); SPY is a benchmark column, never investable.")

    cache = {}
    BOOKS = {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    P(f"  {len(cache)} distinct rung books built across "
      f"{len(PANELS)*len(ANCHORS)*len(LADNAMES)} (panel, anchor, ladder) families.")

    a = ANCHORS["A"]
    r0 = cache[("U56", a["N"], a["H"], a["GROSS"], a["CADENCE"])]
    c0, s0, d0 = fmet(r0[pans["U56"].warm])
    dev = max(abs(c0 - A1101_TRIPLE[0]), abs(s0 - A1101_TRIPLE[1]), abs(d0 - A1101_TRIPLE[2]))
    gate("G3", "1101's committed U56 anchor triple replays (CAGR/Sharpe/MaxDD)", dev, dev < 2e-3)
    lb = backtest(px["U56"], rules_v2_weights(px["U56"]), cost_bps=COST,
                  freq="W")["returns"].values
    lmdd = fmet(lb[WARMUP:])[2]
    gate("G4", "live RULES v2 U56 MaxDD == committed -12.05%", abs(lmdd - LIVE_MAXDD_COMMITTED),
         abs(lmdd - LIVE_MAXDD_COMMITTED) < 5e-4)

    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    gate("G5", "decision count == 1208's 72", float(len(DEC)), len(DEC) == A1208_NDEC)

    # ------------------------------------------------------------ ARM C: the rung-by-rung table
    P("")
    P("=" * 110)
    P("ARM C — THE RESOLUTION TABLE: EVERY DECISION AT EVERY ONE OF THE 12 RUNGS")
    P("=" * 110)
    P("")
    P(f"  RESOLVED at rung L  <=>  P_boot(observed IS argmax) >= {BAR_HI} under a JOINT moving-")
    P(f"  block redraw of the IS window, B = {BDRAWS} draws, one block index per draw applied to")
    P("  every rung of the decision's ladder so cross-rung correlation survives (1101/1208's).")
    rows = []
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([BOOKS[(pn, an, lad)][r][pan.ins] for r in rungs])
        vals = [is_stat(BOOKS[(pn, an, lad)][r], pan.ins, ch) for r in rungs]
        obs = int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))
        T_is = R.shape[0]
        for L in RUNGS_ALL:
            Lv = T_is if L == "T" else int(L)
            pb = pboot_argmax(R, ch, Lv, seed_of(pn, an, lad, ch, L), B=BDRAWS)
            rows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, L=L,
                             obs_rung=str(rungs[obs]), P_pick=float(pb[obs]),
                             RESOLVED=bool(pb[obs] >= BAR_HI)))
    LDF = pd.DataFrame(rows)
    LDF.to_csv(f"{OUT}.ladder.csv", index=False)
    P("")
    P("    L        resolution rate   mean P_pick   1208's published rate   dev")
    devs = []
    for L in RUNGS_ALL:
        z = LDF[LDF.L.astype(str) == str(L)]
        rate = float(z.RESOLVED.mean())
        d = abs(rate - A1208_RATES[L])
        devs.append(d)
        P(f"    {str(L):6s}   {rate:15.4f}   {z.P_pick.mean():11.4f}   "
          f"{A1208_RATES[L]:21.4f}   {d:+.4f}")
    gate("G6", "1208's 12-rung resolution ladder replays inside seed noise (max dev)",
         max(devs), max(devs) <= 0.06)
    gate("G7", "the degenerate top rung L = T resolves EVERY decision (rate == 1.000)",
         float(LDF[LDF.L.astype(str) == "T"].RESOLVED.mean()),
         float(LDF[LDF.L.astype(str) == "T"].RESOLVED.mean()) == 1.0)
    piv = LDF.pivot_table(index=["panel", "anchor", "ladder", "chooser"], columns="L",
                          values="RESOLVED", aggfunc="first")

    # ------------------------------------------------------------ ARM D: what the clause BUYS
    P("")
    P("=" * 110)
    P("ARM D — THE BUY SIDE: DETECTION AS THE LADDER IS WIDENED ONE RUNG AT A TIME")
    P("=" * 110)
    P("")
    P("  d(k) = share of the 72 decisions whose RESOLVED/UNRESOLVED verdict is NOT CONSTANT")
    P("  across the first k rungs of the schedule.  A point (k = 1) detects nothing by")
    P("  construction.  MARGINAL = the decisions the k-th step adds.")

    def dep_share(rungs):
        cols = [c for c in piv.columns if str(c) in {str(r) for r in rungs}]
        sub = piv[cols]
        return (sub.nunique(axis=1) > 1)

    drows = []
    for inc, sched in INC_SCHEDULES.items():
        prev = 0
        for step, rungs in enumerate(sched, start=1):
            dep = dep_share(rungs)
            n = int(dep.sum())
            drows.append(dict(increment=inc, step=step, k=len(rungs),
                              rungs="|".join(str(r) for r in rungs),
                              added=str(rungs[-1]) if step > 1 else "-",
                              n_dependent=n, share=n / len(piv), marginal=(n - prev) / len(piv)))
            prev = n
    DD = pd.DataFrame(drows)
    DD.to_csv(f"{OUT}.detection.csv", index=False)
    for inc in INC_SCHEDULES:
        P("")
        P(f"    {inc}:")
        P("      step   k   rung added   d(k) = L-dependent of 72   share    marginal")
        for _, r in DD[DD.increment == inc].iterrows():
            P(f"      {r.step:4d} {r.k:3d}   {r.added:10s}   {r.n_dependent:22d}   "
              f"{r.share:6.4f}   {r.marginal:+7.4f}")
    d12 = float(DD[DD.k == 12].share.iloc[0])
    d11 = float(DD[(DD.increment == 'INC_ONE') & (DD.k == 11)].share.iloc[0])
    d4 = float(DD[(DD.increment == "INC_ONE") & (DD.k == 4)].share.iloc[0])
    lastmarg = float(DD[(DD.increment == "INC_ONE") & (DD.k == 12)].marginal.iloc[0])
    P("")
    P(f"    REPLAY OF THE RECORD'S OWN TWO LADDERS: LL_REC (4 rungs) "
      f"{int(dep_share([21,63,126,252]).sum())} of 72 (1208: {A1208_DEP['LL_REC']}); "
      f"LL_FULL (11) {int(dep_share([r for r in RUNGS_ALL if r != 'T']).sum())} "
      f"(1208: {A1208_DEP['LL_FULL']}); LL_WIDE (12) "
      f"{int(dep_share(RUNGS_ALL).sum())} (1208: {A1208_DEP['LL_WIDE']}).")
    P("")
    P("    SINGLE-RUNG CONTRIBUTION — the decisions each rung alone makes L-dependent against")
    P(f"    the record's frozen point L = {L_HEAD} (the clause's smallest possible form):")
    srows = []
    for L in RUNGS_ALL:
        if str(L) == str(L_HEAD):
            continue
        n = int(dep_share([L_HEAD, L]).sum())
        srows.append(dict(rung=str(L), n_dependent=n, share=n / len(piv)))
        P(f"      L = {str(L):6s} vs 63   {n:3d} of 72   {n/len(piv):.4f}")
    SR = pd.DataFrame(srows)
    SR.to_csv(f"{OUT}.single_rung.csv", index=False)
    top = SR.sort_values("n_dependent", ascending=False).iloc[0]
    P("")
    P(f"    LARGEST SINGLE RUNG: L = {top.rung} contributes {top.n_dependent} of 72 "
      f"({top.share:.4f}), i.e. {top.share/d12:.4f} of the full 12-rung detection.")

    P("")
    P("    THE TRADE, PRICED (all 9 dial cells).  AMEND = non-conforming committed units the")
    P("    clause forces; COMPUTE = extra bootstrap draws per future verdict at k rungs.")
    P("")
    P("      scope         increment   k at 0.70 of d(12)   AMEND units   UNRECOVERABLE   "
      "extra draws/verdict")
    trows = []
    for _, s in SF.iterrows():
        for inc in INC_SCHEDULES:
            z = DD[DD.increment == inc]
            hit = z[z.share >= 0.70 * d12]
            kstar = int(hit.k.iloc[0]) if len(hit) else -1
            trows.append(dict(scope=s.scope, increment=inc, k_star=kstar,
                              amend=int(s.non_conforming),
                              unrecoverable=int(s.unrecoverable),
                              extra_draws=(kstar - 1) * BDRAWS if kstar > 0 else np.nan))
            P(f"      {s.scope:12s} {inc:10s}  {kstar:18d}   {int(s.non_conforming):11d}   "
              f"{int(s.unrecoverable):13d}   "
              f"{((kstar-1)*BDRAWS if kstar > 0 else -1):18d}")
    TR = pd.DataFrame(trows)
    TR.to_csv(f"{OUT}.trade.csv", index=False)

    # ------------------------------------------------------------ ARM E: rule 8 + KEEP paths
    P("")
    P("=" * 110)
    P("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (does the CLAUSE buy any RETURN?)")
    P("=" * 110)
    P("")
    P("  (E1) every rung book, full sample and 2017-2026, 4a vs live RULES v2 and 4b vs SPY.")
    BM = {}
    for pn in PANELS:
        pan = pans[pn]
        BM[(pn, "SPY")] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbv = backtest(px[pn], rules_v2_weights(px[pn]), cost_bps=COST, freq="W")["returns"].values
        BM[(pn, "LIVE")] = blocks_m(lbv, pan.warm, pan.ins, pan.oos)
    brows = []
    for (pn, an, lad) in {(a, b, c) for (a, b, c, _) in DEC}:
        pan = pans[pn]
        for rung, r in BOOKS[(pn, an, lad)].items():
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            l4b = legs_4b(m, BM[(pn, "SPY")])
            l4bo = legs_4b_oos(m, BM[(pn, "SPY")])
            l4a = legs_4a(m, BM[(pn, "LIVE")])
            brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung), **m,
                              KEEP_4a=all(l4a.values()), KEEP_4b=all(l4b.values()),
                              KEEP_4b_OOS=all(l4bo.values())))
    BK = pd.DataFrame(brows).drop_duplicates(subset=["panel", "anchor", "ladder", "rung"])
    BK.to_csv(f"{OUT}.books.csv", index=False)
    P(f"       {len(BK)} rung-book rows.  4a {int(BK.KEEP_4a.sum())}; 4b full "
      f"{int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; BOTH "
      f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    for pn in PANELS:
        s, l = BM[(pn, "SPY")], BM[(pn, "LIVE")]
        P(f"       {pn:6s} SPY  full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
          f"   OOS {s['OOS_CAGR']:7.2%} / {s['OOS_Sharpe']:.4f} / {s['OOS_MaxDD']:8.2%}")
        P(f"       {pn:6s} LIVE full {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
          f"   OOS {l['OOS_CAGR']:7.2%} / {l['OOS_Sharpe']:.4f} / {l['OOS_MaxDD']:8.2%}")

    P("")
    P("  (E2) THE CLAUSE ON TRIAL.  Every pick is the decision's IS argmax, made on the IS")
    P("       window ONLY, and its 2017-2026 return is read ONCE.  A CLAUSE of k rungs makes")
    P("       the book ACTIONABLE only where the decision's verdict is CONSTANT across those k")
    P("       rungs (no L-dependence) AND RESOLVED at the record's frozen L = 63.  If the")
    P("       clause is worth return rather than only checkability, acting on the surviving")
    P("       picks must beat acting on all of them.")
    pickmap = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        vals = [is_stat(BOOKS[(pn, an, lad)][r], pan.ins, ch) for r in rungs]
        obs = rungs[int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))]
        m = blocks_m(BOOKS[(pn, an, lad)][obs], pan.warm, pan.ins, pan.oos)
        pickmap[(pn, an, lad, ch)] = (obs, m)
    res63 = {k: bool(LDF[(LDF.panel == k[0]) & (LDF.anchor == k[1]) & (LDF.ladder == k[2])
                         & (LDF.chooser == k[3]) & (LDF.L.astype(str) == str(L_HEAD))]
                     .RESOLVED.iloc[0]) for k in DEC}
    wrows = []
    for inc, sched in INC_SCHEDULES.items():
        for rungs in sched:
            dep = dep_share(rungs)
            acted = []
            for k in DEC:
                key = (k[0], k[1], k[2], k[3])
                if not res63[key]:
                    continue
                if bool(dep.loc[key]):
                    continue
                acted.append(pickmap[key])
            if not acted:
                wrows.append(dict(increment=inc, k=len(rungs), n_acted=0,
                                  mean_OOS_Sharpe=np.nan, mean_OOS_CAGR=np.nan,
                                  KEEP_4a=0, KEEP_4b=0, KEEP_4b_OOS=0))
                continue
            wrows.append(dict(
                increment=inc, k=len(rungs), n_acted=len(acted),
                mean_OOS_Sharpe=float(np.mean([m["OOS_Sharpe"] for _, m in acted])),
                mean_OOS_CAGR=float(np.mean([m["OOS_CAGR"] for _, m in acted])),
                KEEP_4a=int(sum(all(legs_4a(m, BM[(p[0], "LIVE")]).values())
                                for p, (_, m) in zip([k for k in DEC if res63[k]
                                                      and not bool(dep.loc[k])], acted))),
                KEEP_4b=int(sum(all(legs_4b(m, BM[(p[0], "SPY")]).values())
                                for p, (_, m) in zip([k for k in DEC if res63[k]
                                                      and not bool(dep.loc[k])], acted))),
                KEEP_4b_OOS=int(sum(all(legs_4b_oos(m, BM[(p[0], "SPY")]).values())
                                    for p, (_, m) in zip([k for k in DEC if res63[k]
                                                          and not bool(dep.loc[k])], acted)))))
    W8 = pd.DataFrame(wrows)
    # references: act on every pick; act on every pick RESOLVED at the point L=63
    allm = [m for (_, m) in pickmap.values()]
    p63 = [pickmap[k][1] for k in DEC if res63[k]]
    ref_all = float(np.mean([m["OOS_Sharpe"] for m in allm]))
    ref_63 = float(np.mean([m["OOS_Sharpe"] for m in p63])) if p63 else np.nan
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P(f"       ACT ON EVERY PICK (72):                    mean OOS Sharpe {ref_all:.4f}")
    P(f"       ACT ON PICKS RESOLVED AT THE POINT L = 63 ({len(p63)}): mean OOS Sharpe "
      f"{ref_63:.4f}")
    P("")
    P("       increment   k   picks surviving the clause   mean OOS Sharpe   mean OOS CAGR   "
      "4a / 4b / 4b_OOS")
    for _, r in W8.iterrows():
        P(f"       {r.increment:10s} {r.k:3d}   {r.n_acted:25d}   "
          f"{(r.mean_OOS_Sharpe if np.isfinite(r.mean_OOS_Sharpe) else float('nan')):15.4f}   "
          f"{(r.mean_OOS_CAGR if np.isfinite(r.mean_OOS_CAGR) else float('nan')):13.4f}   "
          f"{int(r.KEEP_4a)} / {int(r.KEEP_4b)} / {int(r.KEEP_4b_OOS)}")
    best = W8[np.isfinite(W8.mean_OOS_Sharpe)]
    gain = (float(best.mean_OOS_Sharpe.max()) - ref_63) if len(best) else np.nan

    # ------------------------------------------------------------ verdict
    P("")
    P("=" * 110)
    P("VERDICT")
    P("=" * 110)
    if top.share / d12 > 0.50:
        outcome = "(C) DEGENERATE"
    elif d4 >= 0.70 * d12:
        outcome = "(A) CHEAP AND DECISIVE"
    elif lastmarg >= 0.10:
        outcome = "(B) EXPENSIVE"
    else:
        outcome = "(A) CHEAP AND DECISIVE" if d4 >= 0.70 * d12 else "(B) EXPENSIVE"
    P("")
    P(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    P(f"      d(4) = {d4:.4f}, d(11) = {d11:.4f}, d(12) = {d12:.4f}; the 12th rung alone adds")
    P(f"      {lastmarg:+.4f} of the 72 decisions; the largest single rung (L = {top.rung}) is")
    P(f"      {top.share/d12:.4f} of d(12).")
    P("")
    P(f"    COST AT THE HEADLINE SCOPE ({SC_HEAD}): "
      f"{int(SF[SF.scope==SC_HEAD].non_conforming.iloc[0])} committed units non-conforming, of")
    P(f"      which {int(SF[SF.scope==SC_HEAD].unrecoverable.iloc[0])} state no L at all and so")
    P("      cannot even be re-derived from their own text.")
    P("")
    P(f"    CAPITAL.  Acting on the clause's surviving picks moves mean OOS Sharpe by "
      f"{gain:+.4f} against")
    P(f"      the point rule's {ref_63:.4f} (and {ref_all:.4f} for acting on everything).  4a "
      f"{int(BK.KEEP_4a.sum())} of {len(BK)} rung books;")
    P(f"      4b BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books, all of them books the "
      "record already holds.")
    P("      NO NEW BOOK, NO RULES CHANGE.  The clause is a CHECKABILITY instrument and is")
    P("      proposed for the Sunday review (rule 6) as a PROTOCOL schema line only, never as a")
    P("      chooser.")
    P("")
    P("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the")
    P("    current constituents of a sub-$2B screen with max_1d_move >= 1.0 names dropped.")
    P("    Every LEVEL is optimistic, and a resample null prices sampling error on the tape it")
    P("    is handed and cannot correct that.  It largely cancels out of the headline (a RATIO")
    P("    of one construction against itself: the same 72 decisions at different ladder")
    P("    lengths) and does NOT cancel out of the 4b legs, so those passes are upper bounds.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    P("")
    P(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
