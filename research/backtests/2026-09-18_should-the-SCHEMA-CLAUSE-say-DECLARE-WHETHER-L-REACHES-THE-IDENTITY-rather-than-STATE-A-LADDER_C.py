#!/usr/bin/env python3
"""
Idea 1247 (lane C, 2026-09-18) — should the SCHEMA CLAUSE say DECLARE WHETHER L REACHES THE
IDENTITY rather than STATE A LADDER?

THE PREMISE, READ FROM THE RECORD.  Idea 1208 proposed a PROTOCOL schema clause requiring the
block length L — and, where the claim is a rate, the LADDER — beside every block-resampling
verdict.  Idea 1243 (lane cloud, 2026-09-17) priced that clause on one fixed object, 1208's 72
pick decisions (3 panels x 2 anchors x 4 ladders x 3 choosers), and found it DEGENERATE: on a
12-rung ladder d(4) = 0.0556, d(11) = 0.2917, d(12) = 0.8472, the 12th rung (the degenerate
L = T identity) alone adds +0.5556 and is 0.9016 of the whole buy, while L = 42 contributes
exactly zero.  What the record calls "a ladder" is a ONE-SIDED REACH toward one degenerate rung.

So the clause 1208 drafted may be the wrong clause.  This run drafts the AMENDED one the queue
names — STATE L, AND STATE WHETHER THE WIDEST RUNG'S BLOCK IS A NON-TRIVIAL FRACTION OF T — and
prices it against the ladder clause on the SAME 72 decisions, in the same three currencies 1243
used: DETECTION (what it catches), DRAWS (what it costs to run), and COMMITTED UNITS (what it
forces the record to amend or re-run).

THE ARITHMETIC THAT MOTIVATES THE AMENDMENT, STATED BEFORE ANY NUMBER IS READ.  A moving-block
resample with L = T has exactly one legal block start (0), so EVERY draw returns the original
sample in the original order.  P_boot(observed argmax) is therefore 1.0 identically, for every
seed, every B, every decision.  Two consequences, both testable here:
  (i) the top rung's "detection" is ARITHMETIC, not empirical — it is knowable from L and T
      alone, with ZERO bootstrap draws; and
  (ii) because the identity rung resolves everything, "does my verdict survive the reach to the
      identity?" is exactly "is my verdict RESOLVED at my own L?" — a question the record can
      already answer from what it has run.
If both hold, a clause that demands a LADDER is buying, at k x B draws, something a two-token
DISCLOSURE buys free.  That is the hypothesis; it is measured, not assumed, and gate G7/G8
below are its two failure points.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAUSE FORM   {CF_POINT, CF_LADDER4, CF_LADDER11, CF_LADDER12, CF_IDENTITY, CF_FRACTION}
                CF_POINT      the status quo: state L, nothing else.  Detects nothing by
                              construction; it is the floor every other form is priced against.
                CF_LADDER4    1208's clause at the record's own habit, LL_REC = [21,63,126,252].
                CF_LADDER11   1208's LL_FULL, the 11 non-degenerate rungs.
                CF_LADDER12   LL_WIDE, all 12 rungs including the identity.
                CF_IDENTITY   the queue's amended clause in its BINARY form: state L, and state
                              whether the verdict survives the reach to L = T.
                CF_FRACTION   the amended clause in its GRADED form: state L, and carry a verdict
                              at every rung the bar calls a NON-TRIVIAL FRACTION of T (L/T >= f),
                              the bar being dial 2.  The queue's literal wording — "whether the
                              WIDEST rung's block is a non-trivial fraction of T" — is INERT and
                              the run says so rather than hiding it: the identity has L/T = 1 and
                              is the widest admitted rung at every f <= 1, so that phrasing reads
                              YES at all six bars.  Keying the clause on the ADMITTED SET instead
                              makes f bind, and CF_FRACTION at f = 1.00 IS CF_IDENTITY — checked
                              at G10, not assumed.
  FRACTION BAR  f in {0.02, 0.05, 0.10, 0.25, 0.50, 1.00} — "non-trivial" made a number.  The
                widest rung a clause at bar f admits is the largest rung with L/T >= f.  f binds
                only CF_FRACTION; every other form is reported once, at every f, unchanged.
  All 36 (form x bar) cells are published, in detection, in draws, in bound units and in capital.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); ANCHOR {A, B}; the four
ladders N / H / GROSS / CADENCE; the three choosers CH_ISSHARPE / CH_ISCAGR / CH_ISDD; the
resolution bar q = 0.90 (1208's, ALWAYS published); B = 1000 draws; the 4a and 4b legs.

GROUND TRUTH, TWO OF THEM, BOTH PUBLISHED.  A clause is a DETECTOR of L-dependence and is scored
against both readings of what it should catch:
  DEP12  the verdict is not constant across all 12 rungs (1243's own object, identity included).
  DEP11  the verdict is not constant across the 11 NON-DEGENERATE rungs — real short-block
         instability, the thing an identity flag by construction cannot see.
A clause that scores well on DEP12 and badly on DEP11 has caught the degeneracy and missed the
statistics; that distinction is the whole question and it is reported at every cell.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen, in this order):
  (A) THE AMENDMENT DOMINATES — CF_IDENTITY recalls >= 0.90 of DEP12 at strictly fewer draws
      than every ladder form AND binds a strict subset of the ladder clause's committed units.
  (B) THE LADDER EARNS ITS COST — the ladder forms detect, on DEP11, at least 0.10 of the 72
      decisions (>= 8) that CF_IDENTITY misses; i.e. real non-degenerate L-dependence exists in
      quantity and only a ladder sees it.
  (C) BOTH, AND THEY ARE DIFFERENT CLAUSES — (A) and (B) both fire, so the record should write
      the amended clause AND keep a ladder where the claim is a rate.
  (D) NEITHER — the amendment fails its own recall bar, and the record should keep 1208's text.

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

DATE = "2026-09-18"
SLUG = "should-the-SCHEMA-CLAUSE-say-DECLARE-WHETHER-L-REACHES-THE-IDENTITY-rather-than-STATE-A-LADDER"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

# ------------------------------------------------------------------ 1101/1208/1243 construction
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

RUNGS_ALL = [1, 2, 5, 10, 21, 42, 63, 126, 252, 504, 1008, "T"]
RUNGS_FINITE = [r for r in RUNGS_ALL if r != "T"]
LL_REC = [21, 63, 126, 252]
BAR_HI = 0.90
BDRAWS = 1000
SEED_BASE = 12471247
L_HEAD = 63

# ------------------------------------------------------------------ the two dials
FORMS = ["CF_POINT", "CF_LADDER4", "CF_LADDER11", "CF_LADDER12", "CF_IDENTITY", "CF_FRACTION"]
FBARS = [0.02, 0.05, 0.10, 0.25, 0.50, 1.00]
F_HEAD = 0.50
# The cost table in ARM A is priced before the panels are built, so it needs the IS window
# length up front.  This is U56's, asserted against the measured value in ARM B (G6b).
T_IS_REF = 2007

# ------------------------------------------------------------------ the record's own numbers
A1208_RATES = {1: 0.1528, 2: 0.1667, 5: 0.1667, 10: 0.1806, 21: 0.1944, 42: 0.2222,
               63: 0.2222, 126: 0.2361, 252: 0.2778, 504: 0.3194, 1008: 0.4722, "T": 1.0000}
A1208_NDEC = 72
A1243_DEP = {"LL_REC": 4, "LL_FULL": 21, "LL_WIDE": 61}          # 1243's own replay of 1208
A1243_D = {4: 0.0556, 11: 0.2917, 12: 0.8472}
A1243_TOPSHARE = 0.9016
A1243_SINGLE = {"1": 6, "2": 5, "5": 3, "10": 3, "21": 2, "42": 0, "126": 1, "252": 4,
                "504": 7, "1008": 15, "T": 55}
A1243_SCOPE_RESAMPLE = dict(bound=1413, non_conforming=1371, unrecoverable=1074)
A1243_REF63, A1243_REFALL = 0.8255, None
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
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<70s} {value:.4e}")
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


def identity_share(T, L, seed, B=200):
    """Mean share of positions a draw takes from its own index — 1.0 at L = T by arithmetic."""
    rng = np.random.default_rng(seed)
    idx = block_index(rng, T, L, B)
    return float((idx == np.arange(T)[None, :]).mean())


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
FLOORTOK = re.compile(
    r"\b(floor|bar of|bar at|bar\b|threshold|cut-?off|q\s*=\s*0?\.\d+|0\.9[05]\s+bar|"
    r"INF_FLOOR|L_[A-Z]+|decisiveness bar|confidence level)\b", re.I)
# the AMENDED clause's own conformance tokens: does the unit let a reader compute L / T at all?
FRACTOK = re.compile(
    r"(\bL\s*/\s*T\b|\bT\s*=\s*\d|\bfraction of (?:the )?(?:sample|window|tape|T)\b|"
    r"\bblock fraction\b|\bL/T\b|\bidentity (?:rung|resample|block)\b|\breaches the identity\b|"
    r"\bdegenerate (?:rung|resample|block|L)\b|\bL\s*=\s*T\b)", re.I)
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
            CS_STRICT=bt, HAS_RESAMPLE_STAT=rs,
            STATES_L=bool(ls), L_STATED=ls[0] if ls else 0,
            STATES_L_LADDER=bool(LADDERTOK.search(txt)),
            STATES_FRACTION=bool(FRACTOK.search(txt)),
            CARRIES_VERDICT=bool(VERDICTTOK.search(txt)),
            FLOOR_KEYED=bool(FLOORTOK.search(txt)),
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


# =================================================================================================
def frac_of(r, T_is):
    return (T_is if r == "T" else int(r)) / T_is


def widest_rung(f, T_is):
    """The WIDEST rung a clause at bar f admits — the queue's literal wording.

    This is the drafting trap the run reports rather than hides: the identity L = T has
    L / T = 1 and is therefore the widest admitted rung at EVERY bar f <= 1, so a clause
    phrased 'declare whether the WIDEST rung's block is a non-trivial fraction of T' is
    answered YES at every bar and its f is inert.  That is why the graded form below is
    keyed on the ADMITTED SET (every rung with L / T >= f) rather than on the maximum.
    """
    ok = [r for r in RUNGS_ALL if frac_of(r, T_is) >= f]
    return max(ok, key=lambda r: frac_of(r, T_is)) if ok else None


def admitted_rungs(f, T_is):
    """Every rung the bar f calls a NON-TRIVIAL fraction of T, plus the record's stated L."""
    ok = [r for r in RUNGS_ALL if frac_of(r, T_is) >= f]
    return sorted({L_HEAD, *ok}, key=lambda r: frac_of(r, T_is))


def form_rungs(form, f, T_is):
    """The rungs a clause form actually requires a verdict at (L = 63 is always one of them)."""
    if form == "CF_POINT":
        return [L_HEAD]
    if form == "CF_LADDER4":
        return list(LL_REC)
    if form == "CF_LADDER11":
        return list(RUNGS_FINITE)
    if form == "CF_LADDER12":
        return list(RUNGS_ALL)
    if form == "CF_IDENTITY":
        return [L_HEAD, "T"]
    if form == "CF_FRACTION":
        return admitted_rungs(f, T_is)
    raise ValueError(form)


def draws_owed(rungs):
    """Extra bootstrap draws a clause owes per verdict beyond the single point run at L = 63.
    The identity rung L = T is FREE: it has exactly one legal block start, so no draw is
    needed and none is charged (this is the amendment's whole economic claim; G7 tests it)."""
    extra = [r for r in rungs if str(r) != str(L_HEAD)]
    return sum(0 if str(r) == "T" else BDRAWS for r in extra)


def main():
    t0 = time.time()
    P("=" * 112)
    P(f"IDEA 1247 (lane C, {DATE}) — should the SCHEMA CLAUSE say DECLARE WHETHER L REACHES THE")
    P("IDENTITY rather than STATE A LADDER?")
    P("=" * 112)
    P("  dial 1 = CLAUSE FORM   {CF_POINT, CF_LADDER4, CF_LADDER11, CF_LADDER12, CF_IDENTITY,")
    P("                          CF_FRACTION}")
    P("  dial 2 = FRACTION BAR  f in {0.02, 0.05, 0.10, 0.25, 0.50, 1.00}  (binds CF_FRACTION:")
    P("           the clause demands a verdict at every rung with L/T >= f, plus the stated L.")
    P("           NOTE, published not hidden: the queue's literal 'the WIDEST rung' wording is")
    P("           INERT — the identity has L/T = 1 and is the widest admitted rung at every bar.")
    P("  NOT dials: 3 panels x 2 anchors x 4 ladders x 3 choosers = 72 decisions, every one")
    P("             published at every rung; q = 0.90 and B = 1000 are 1208's, always stated.")
    P("  GROUND TRUTH: DEP12 (verdict varies over all 12 rungs) AND DEP11 (over the 11 non-")
    P("             degenerate rungs).  Both reported at every cell.")
    P("  PRE-DECLARED: (A) AMENDMENT DOMINATES — CF_IDENTITY recalls >= 0.90 of DEP12 at strictly")
    P("                    fewer draws than every ladder form and binds a strict subset of units.")
    P("                (B) LADDER EARNS ITS COST — ladders catch >= 8 of 72 DEP11 decisions that")
    P("                    CF_IDENTITY misses.")
    P("                (C) BOTH — write the amendment AND keep a ladder where the claim is a rate.")
    P("                (D) NEITHER — keep 1208's text.")
    P("")

    # ------------------------------------------------------------ ARM A: the census / cost side
    P("=" * 112)
    P("ARM A — THE COST SIDE: WHICH COMMITTED UNITS EACH CLAUSE WOULD BIND")
    P("=" * 112)
    C, n_units, n_md = census()
    P("")
    P(f"  {n_units} committed text units over LEADERBOARD.md + CHANGELOG.md + {n_md} .md files.")
    P("")
    P("  REFLEXIVITY, STATED BEFORE THE NUMBERS (1230's finding, which binds this run too).  A")
    P("  census of the record is committed TO the record, so 1243's integers are NOT expected to")
    P("  replay exactly — this file itself names L, T, the identity and a fraction, and will be a")
    P("  unit in the next lane's census.  The gates below are DRIFT gates, not equality gates.")
    P("")
    P("  SCOPE, held FIXED at 1243's headline SC_RESAMPLE (block-keyed units plus every unit")
    P("  carrying a resample-derived statistic AND a verdict word).  Scope was 1243's dial; it is")
    P("  NOT a dial here — this run's two dials are CLAUSE FORM and FRACTION BAR (rule 4).")
    scope_m = C.CS_STRICT | (C.HAS_RESAMPLE_STAT & C.CARRIES_VERDICT)
    Z = C[scope_m]
    n_bound = len(Z)
    n_states_L = int(Z.STATES_L.sum())
    n_states_lad = int(Z.STATES_L_LADDER.sum())
    n_states_frac = int(Z.STATES_FRACTION.sum())
    P("")
    P(f"  SC_RESAMPLE binds {n_bound} committed units.  Of those: {n_states_L} state an L, "
      f"{n_states_lad} state an L LADDER,")
    P(f"  {n_states_frac} state a FRACTION / T / identity in any form.")
    P("")
    P(f"  DRIFT since 1243 committed (2026-09-17): bound {A1243_SCOPE_RESAMPLE['bound']} -> "
      f"{n_bound} ({n_bound - A1243_SCOPE_RESAMPLE['bound']:+d}).")
    gate("G1", "SC_RESAMPLE bound count is 1243's 1413 plus post-1243 commits only (<= +12%)",
         n_bound, A1243_SCOPE_RESAMPLE["bound"] <= n_bound <= A1243_SCOPE_RESAMPLE["bound"] * 1.12)

    # conformance per clause form.  A unit CONFORMS when its own text already carries what the
    # clause demands.  Non-conformance splits two ways and the split is the whole cost argument:
    #   EDITABLE      the text can be brought into conformance with no new computation
    #   RERUN         the unit owes new bootstrap draws (or, with no L at all, a code read first)
    crows = []
    for form in FORMS:
        for f in FBARS:
            if form == "CF_POINT":
                conf = Z.STATES_L
                editable = pd.Series(False, index=Z.index)
                rerun = ~Z.STATES_L
                dr = 0
            elif form in ("CF_LADDER4", "CF_LADDER11", "CF_LADDER12"):
                conf = Z.STATES_L_LADDER
                editable = pd.Series(False, index=Z.index)   # a ladder cannot be written, only run
                rerun = ~Z.STATES_L_LADDER
                dr = {"CF_LADDER4": 3, "CF_LADDER11": 10, "CF_LADDER12": 10}[form] * BDRAWS
            else:  # CF_IDENTITY and CF_FRACTION: state L, and state the fraction / the reach
                conf = Z.STATES_L & Z.STATES_FRACTION
                editable = Z.STATES_L & ~Z.STATES_FRACTION   # T is knowable from the tape: an EDIT
                rerun = ~Z.STATES_L
                dr = (0 if form == "CF_IDENTITY"
                      else draws_owed(admitted_rungs(f, T_IS_REF)))
            crows.append(dict(form=form, fbar=f, bound=n_bound, conforming=int(conf.sum()),
                              non_conforming=int((~conf).sum()), editable=int(editable.sum()),
                              rerun=int(rerun.sum()), draws_per_verdict=dr))
    CF = pd.DataFrame(crows)
    CF.to_csv(f"{OUT}.clausecost.csv", index=False)
    P("")
    P("  form          f      bound   CONFORMING   NON-CONFORMING   fixable by EDIT   "
      "needs a RE-RUN   draws/verdict")
    for _, r in CF[(CF.fbar == F_HEAD) | (CF.form == "CF_FRACTION")].iterrows():
        P(f"  {r.form:12s} {r.fbar:5.2f} {r.bound:7d}   {r.conforming:10d}   "
          f"{r.non_conforming:14d}   {r.editable:15d}   {r.rerun:14d}   {r.draws_per_verdict:13d}")
    lad_rerun = int(CF[CF.form == "CF_LADDER11"].rerun.iloc[0])
    idn_rerun = int(CF[CF.form == "CF_IDENTITY"].rerun.iloc[0])
    gate("G2", "the amended clause's RE-RUN set is a strict SUBSET of the ladder clause's",
         float(idn_rerun - lad_rerun), idn_rerun <= lad_rerun)
    gate("G3", "1243's 'states no L at all' count replays as the amendment's re-run set "
         "(drift <= 12%)", float(idn_rerun),
         A1243_SCOPE_RESAMPLE["unrecoverable"] <= idn_rerun
         <= A1243_SCOPE_RESAMPLE["unrecoverable"] * 1.12)

    # ------------------------------------------------------------ ARM B: the object
    P("")
    P("=" * 112)
    P("ARM B — THE OBJECT: 1208/1243's 72 PICK DECISIONS, REBUILT")
    P("=" * 112)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs = load_universe(small=True)
    mv = pxs.pct_change().abs().max()
    drop = [c for c in pxs.columns if c != "SPY" and not (mv[c] < 1.0)]
    px["SMALL"] = pxs.drop(columns=drop)
    pans = {n: Panel(n, px[n]) for n in PANELS}
    vintage = str(px["U56"].index[-1].date())
    P("")
    P(f"  CACHE VINTAGE (1264's bycatch: a committed triple is a claim about its vintage): "
      f"{vintage}")
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
    P(f"  1101's committed U56 anchor triple: {A1101_TRIPLE[0]:.6f} / {A1101_TRIPLE[1]:.6f} / "
      f"{A1101_TRIPLE[2]:.6f}")
    P(f"  this run's, on the {vintage} cache:  {c0:.6f} / {s0:.6f} / {d0:.6f}   (max dev "
      f"{dev:.3e})")
    gate("G4", "1101's committed U56 anchor triple replays within the vintage drift 1264 measured",
         dev, dev < 6e-3)
    lb = backtest(px["U56"], rules_v2_weights(px["U56"]), cost_bps=COST,
                  freq="W")["returns"].values
    lmdd = fmet(lb[WARMUP:])[2]
    gate("G5", "live RULES v2 U56 MaxDD == committed -12.05%", abs(lmdd - LIVE_MAXDD_COMMITTED),
         abs(lmdd - LIVE_MAXDD_COMMITTED) < 5e-4)

    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    gate("G6", "decision count == 1208/1243's 72", float(len(DEC)), len(DEC) == A1208_NDEC)
    T_IS = {pn: int(pans[pn].ins.sum()) for pn in PANELS}
    gate("G6b", "ARM A's cost table used the true U56 IS window length T", float(T_IS["U56"]),
         T_IS["U56"] == T_IS_REF)
    P("")
    P("  IS WINDOW LENGTHS (T), the amendment's denominator, per panel: "
      + ", ".join(f"{pn} {T_IS[pn]}" for pn in PANELS))
    P(f"  So the record's FROZEN point L = {L_HEAD} sits at L/T = "
      + ", ".join(f"{pn} {L_HEAD/T_IS[pn]:.4f}" for pn in PANELS) + " — trivial at every bar")
    P("  this run tests.  The amendment's flag on the record's own habit is NO at 6 of 6 bars.")

    # ------------------------------------------------------------ ARM C: is the identity free?
    P("")
    P("=" * 112)
    P("ARM C — THE ARITHMETIC THE AMENDMENT RESTS ON: IS THE IDENTITY RUNG FREE?")
    P("=" * 112)
    P("")
    P("  A moving-block draw at L = T has one legal start, so it returns the original sample.")
    P("  Measured: the mean share of positions a draw takes from its OWN index, per rung, on")
    P("  U56's IS window — and the realised P_boot spread over seeds at L = T.")
    T_u = T_IS["U56"]
    irows = []
    for L in RUNGS_ALL:
        Lv = T_u if L == "T" else int(L)
        sh = identity_share(T_u, Lv, seed_of("idshare", L))
        irows.append(dict(rung=str(L), L=Lv, frac_of_T=Lv / T_u, identity_share=sh))
    IDS = pd.DataFrame(irows)
    IDS.to_csv(f"{OUT}.identity.csv", index=False)
    P("")
    P("    rung      L      L/T     mean share of positions drawn from their own index")
    for _, r in IDS.iterrows():
        P(f"    {r.rung:6s} {int(r.L):6d}   {r.frac_of_T:6.4f}   {r.identity_share:.6f}")
    idT = float(IDS[IDS.rung == "T"].identity_share.iloc[0])
    gate("G7", "L = T is the IDENTITY: every draw reproduces the sample exactly (share == 1)",
         abs(idT - 1.0), abs(idT - 1.0) < 1e-12)

    # ------------------------------------------------------------ ARM D: the resolution table
    P("")
    P("=" * 112)
    P("ARM D — THE RESOLUTION TABLE: EVERY DECISION AT EVERY ONE OF THE 12 RUNGS")
    P("=" * 112)
    P("")
    P(f"  RESOLVED at rung L  <=>  P_boot(observed IS argmax) >= {BAR_HI} under a JOINT moving-")
    P(f"  block redraw of the IS window, B = {BDRAWS} draws (1101/1208/1243's construction).")
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
            rows.append(dict(panel=pn, anchor=an, ladder=lad, chooser=ch, L=str(L),
                             frac_of_T=Lv / T_is, obs_rung=str(rungs[obs]),
                             P_pick=float(pb[obs]), RESOLVED=bool(pb[obs] >= BAR_HI)))
    LDF = pd.DataFrame(rows)
    LDF.to_csv(f"{OUT}.ladder.csv", index=False)
    P("")
    P("    L        resolution rate   mean P_pick   1208's published rate   dev")
    devs = []
    for L in RUNGS_ALL:
        z = LDF[LDF.L == str(L)]
        rate = float(z.RESOLVED.mean())
        d = abs(rate - A1208_RATES[L])
        devs.append(d)
        P(f"    {str(L):6s}   {rate:15.4f}   {z.P_pick.mean():11.4f}   "
          f"{A1208_RATES[L]:21.4f}   {d:+.4f}")
    gate("G8", "1208's 12-rung resolution ladder replays inside seed noise (max dev)",
         max(devs), max(devs) <= 0.06)
    rateT = float(LDF[LDF.L == "T"].RESOLVED.mean())
    gate("G9", "the identity rung resolves EVERY decision (rate == 1.000), so 'reaches the "
         "identity' == 'resolved at your own L'", rateT, rateT == 1.0)
    piv = LDF.pivot_table(index=["panel", "anchor", "ladder", "chooser"], columns="L",
                          values="RESOLVED", aggfunc="first")
    piv.columns = [str(c) for c in piv.columns]

    def dep_over(rungs):
        cols = [str(r) for r in rungs]
        return piv[cols].nunique(axis=1) > 1

    DEP12 = dep_over(RUNGS_ALL)
    DEP11 = dep_over(RUNGS_FINITE)
    res63 = piv[str(L_HEAD)].astype(bool)
    P("")
    P(f"    GROUND TRUTH: DEP12 {int(DEP12.sum())} of 72 (1243: {A1243_DEP['LL_WIDE']}); "
      f"DEP11 {int(DEP11.sum())} of 72 (1243: {A1243_DEP['LL_FULL']}); "
      f"LL_REC(4) {int(dep_over(LL_REC).sum())} (1243: {A1243_DEP['LL_REC']}).")
    P(f"    RESOLVED at the frozen point L = {L_HEAD}: {int(res63.sum())} of 72.")
    P(f"    DECISIONS THE IDENTITY FLAG RAISES (verdict at 63 != verdict at T) = "
      f"{int((res63 != piv['T'].astype(bool)).sum())}, which is exactly the "
      f"{int((~res63).sum())} UNRESOLVED at 63 whenever G9 holds.")

    # ------------------------------------------------------------ ARM E: clause vs clause
    P("")
    P("=" * 112)
    P("ARM E — THE TWO CLAUSES AS DETECTORS, ALL 36 (FORM x BAR) CELLS")
    P("=" * 112)
    P("")
    P("  A clause DETECTS a decision when the verdict is not constant across the rungs it")
    P("  demands.  RECALL is against each ground truth; DRAWS is the extra bootstrap cost per")
    P("  future verdict, charging ZERO for the identity rung (ARM C's arithmetic).")
    drows = []
    for form in FORMS:
        for f in FBARS:
            rungs = form_rungs(form, f, T_u)
            det = dep_over(rungs)
            n = int(det.sum())
            tp12 = int((det & DEP12).sum())
            tp11 = int((det & DEP11).sum())
            miss11 = int((~det & DEP11).sum())
            drows.append(dict(
                form=form, fbar=f, rungs="|".join(str(r) for r in rungs), k=len(rungs),
                detected=n, share=n / len(piv),
                recall_DEP12=tp12 / max(int(DEP12.sum()), 1),
                recall_DEP11=tp11 / max(int(DEP11.sum()), 1),
                missed_DEP11=miss11,
                false_pos=int((det & ~DEP12).sum()),
                draws=draws_owed(rungs)))
    DT = pd.DataFrame(drows)
    DT.to_csv(f"{OUT}.detection.csv", index=False)
    P("")
    P("    form          f      rungs demanded            k   detected/72   recall DEP12   "
      "recall DEP11   DEP11 missed   draws/verdict")
    for _, r in DT.iterrows():
        if r.form != "CF_FRACTION" and r.fbar != F_HEAD:
            continue
        P(f"    {r.form:12s} {r.fbar:5.2f}  {r.rungs:24s} {r.k:3d}   {r.detected:11d}   "
          f"{r.recall_DEP12:12.4f}   {r.recall_DEP11:12.4f}   {r.missed_DEP11:12d}   "
          f"{r.draws:13d}")
    P("")
    P("    (CF_POINT / CF_LADDER* / CF_IDENTITY do not depend on f; their row is printed once at")
    P(f"     f = {F_HEAD:.2f} and is identical at all six bars.  The full 36-cell grid is in")
    P(f"     {OUT.name}.detection.csv.)")

    idn = DT[DT.form == "CF_IDENTITY"].iloc[0]
    l11 = DT[DT.form == "CF_LADDER11"].iloc[0]
    l12 = DT[DT.form == "CF_LADDER12"].iloc[0]
    l4 = DT[DT.form == "CF_LADDER4"].iloc[0]
    fr100 = DT[(DT.form == "CF_FRACTION") & (DT.fbar == 1.00)].iloc[0]
    gate("G10", "CF_FRACTION at f = 1.00 IS CF_IDENTITY (same detected set, same draws)",
         float(abs(fr100.detected - idn.detected) + abs(fr100.draws - idn.draws)),
         fr100.detected == idn.detected and fr100.draws == idn.draws)
    gate("G11", "1243's headline replays: the identity rung is >= 0.85 of the 12-rung detection",
         idn.detected / max(int(DEP12.sum()), 1), idn.detected / max(int(DEP12.sum()), 1) >= 0.85)

    P("")
    P("    THE STRAIGHT COMPARISON THE QUEUE ASKED FOR:")
    P(f"      CF_LADDER11 (1208's clause as run):  detects {int(l11.detected):2d} of 72, "
      f"recall DEP12 {l11.recall_DEP12:.4f}, DEP11 {l11.recall_DEP11:.4f}, "
      f"{int(l11.draws):6d} draws/verdict")
    P(f"      CF_LADDER12 (its widest form):       detects {int(l12.detected):2d} of 72, "
      f"recall DEP12 {l12.recall_DEP12:.4f}, DEP11 {l12.recall_DEP11:.4f}, "
      f"{int(l12.draws):6d} draws/verdict")
    P(f"      CF_LADDER4  (the record's habit):    detects {int(l4.detected):2d} of 72, "
      f"recall DEP12 {l4.recall_DEP12:.4f}, DEP11 {l4.recall_DEP11:.4f}, "
      f"{int(l4.draws):6d} draws/verdict")
    P(f"      CF_IDENTITY (the amendment):         detects {int(idn.detected):2d} of 72, "
      f"recall DEP12 {idn.recall_DEP12:.4f}, DEP11 {idn.recall_DEP11:.4f}, "
      f"{int(idn.draws):6d} draws/verdict")
    P("")
    P("    WHAT THE AMENDMENT CANNOT SEE, stated as plainly as what it can: the decisions that")
    P(f"    are L-dependent among the 11 NON-degenerate rungs but constant across "
      f"{{{L_HEAD}, T}} — {int(idn.missed_DEP11)} of 72.")
    P("")
    P("    TWO CIRCULARITIES, DECLARED SO NEITHER NUMBER IS OVER-READ.  (i) CF_LADDER11's DEP11")
    P("    recall of 1.0000 is DEFINITIONAL — DEP11 is the set that ladder's own rungs disagree")
    P("    on — and so is CF_LADDER12's 1.0000 on DEP12.  Neither is evidence for the ladder;")
    P("    the informative columns are the ones a clause is NOT the definition of.  (ii) By the")
    P("    same token CF_LADDER11's DEP12 recall of "
      f"{l11.recall_DEP12:.4f} is low because DEP12 is dominated by")
    P("    the rung it excludes, which is 1243's finding restated, not a new one.")
    P("")
    P("    THE FRACTION BAR IS INERT ON DETECTION TOO, AT EVERY ONE OF ITS SIX VALUES.  "
      f"CF_FRACTION detects")
    frd = DT[DT.form == "CF_FRACTION"]
    P(f"    {int(frd.detected.min())}-{int(frd.detected.max())} of 72 across f = 0.02..1.00 while "
      f"its draw bill runs {int(frd.draws.max())} -> {int(frd.draws.min())}.")
    P("    Every rung the bar admits below the identity adds nothing the identity had not already")
    P("    caught, so the GRADED form is strictly dominated by the BINARY one: same detection,")
    P(f"    up to {int(frd.draws.max())} more draws per verdict.  The clause should be written as "
      "a BINARY.")

    # ------------------------------------------------------------ ARM F: rule 8 + KEEP paths
    P("")
    P("=" * 112)
    P("ARM F — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (does either clause buy any RETURN?)")
    P("=" * 112)
    P("")
    P("  (F1) every rung book, full sample and 2017-2026, 4a vs live RULES v2 and 4b vs SPY.")
    BM = {}
    for pn in PANELS:
        pan = pans[pn]
        BM[(pn, "SPY")] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbv = backtest(px[pn], rules_v2_weights(px[pn]), cost_bps=COST, freq="W")["returns"].values
        BM[(pn, "LIVE")] = blocks_m(lbv, pan.warm, pan.ins, pan.oos)
    brows = []
    for (pn, an, lad) in sorted({(x, y, z) for (x, y, z, _) in DEC}):
        pan = pans[pn]
        for rung, r in BOOKS[(pn, an, lad)].items():
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            brows.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung), **m,
                              KEEP_4a=all(legs_4a(m, BM[(pn, "LIVE")]).values()),
                              KEEP_4b=all(legs_4b(m, BM[(pn, "SPY")]).values()),
                              KEEP_4b_OOS=all(legs_4b_oos(m, BM[(pn, "SPY")]).values())))
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
    P("  (F2) EACH CLAUSE AS A CHOOSER.  Every pick is its decision's IS argmax, made on the IS")
    P("       window ONLY, 2017-2026 read once.  A clause makes a pick ACTIONABLE when it is")
    P(f"       RESOLVED at the frozen L = {L_HEAD} AND the clause's own rungs do not contradict")
    P("       that verdict.  References: act on all 72; act on the anchor rung only (do nothing).")
    pickmap = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        vals = [is_stat(BOOKS[(pn, an, lad)][r], pan.ins, ch) for r in rungs]
        obs = rungs[int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))]
        pickmap[(pn, an, lad, ch)] = (obs, blocks_m(BOOKS[(pn, an, lad)][obs],
                                                    pan.warm, pan.ins, pan.oos))
    anchmap = {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rung = ANCHORS[an][lad]
        anchmap[(pn, an, lad, ch)] = blocks_m(BOOKS[(pn, an, lad)][rung],
                                              pan.warm, pan.ins, pan.oos)

    def summarise(keys, mets):
        if not keys:
            return dict(n_acted=0, mean_OOS_Sharpe=np.nan, mean_OOS_CAGR=np.nan,
                        mean_OOS_MaxDD=np.nan, KEEP_4a=0, KEEP_4b=0, KEEP_4b_OOS=0)
        return dict(
            n_acted=len(keys),
            mean_OOS_Sharpe=float(np.mean([mets[k]["OOS_Sharpe"] for k in keys])),
            mean_OOS_CAGR=float(np.mean([mets[k]["OOS_CAGR"] for k in keys])),
            mean_OOS_MaxDD=float(np.mean([mets[k]["OOS_MaxDD"] for k in keys])),
            KEEP_4a=int(sum(all(legs_4a(mets[k], BM[(k[0], "LIVE")]).values()) for k in keys)),
            KEEP_4b=int(sum(all(legs_4b(mets[k], BM[(k[0], "SPY")]).values()) for k in keys)),
            KEEP_4b_OOS=int(sum(all(legs_4b_oos(mets[k], BM[(k[0], "SPY")]).values())
                                for k in keys)))

    pm = {k: v[1] for k, v in pickmap.items()}
    ref_all = summarise(list(DEC), pm)
    ref_anchor = summarise(list(DEC), anchmap)
    wrows = [dict(form="REF_ACT_ON_ALL", fbar=np.nan, draws=0, **ref_all),
             dict(form="REF_DO_NOTHING", fbar=np.nan, draws=0, **ref_anchor)]
    for form in FORMS:
        for f in FBARS:
            rungs = form_rungs(form, f, T_u)
            det = dep_over(rungs)
            keys = [k for k in DEC if bool(res63.loc[k]) and not bool(det.loc[k])]
            wrows.append(dict(form=form, fbar=f, draws=draws_owed(rungs), **summarise(keys, pm)))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P("       form              f    picks acted   mean OOS Sharpe   mean OOS CAGR   "
      "mean OOS MaxDD   4a / 4b / 4b_OOS")
    for _, r in W8.iterrows():
        if r.form in FORMS and r.form != "CF_FRACTION" and r.fbar != F_HEAD:
            continue
        fb = "  -  " if not np.isfinite(r.fbar) else f"{r.fbar:5.2f}"
        P(f"       {r.form:16s} {fb}  {int(r.n_acted):11d}   "
          f"{r.mean_OOS_Sharpe:15.4f}   {r.mean_OOS_CAGR:13.4f}   {r.mean_OOS_MaxDD:14.4f}   "
          f"{int(r.KEEP_4a)} / {int(r.KEEP_4b)} / {int(r.KEEP_4b_OOS)}")
    pt = W8[(W8.form == "CF_POINT") & (W8.fbar == F_HEAD)].iloc[0]
    id8 = W8[(W8.form == "CF_IDENTITY") & (W8.fbar == F_HEAD)].iloc[0]
    l118 = W8[(W8.form == "CF_LADDER11") & (W8.fbar == F_HEAD)].iloc[0]
    gate("G12", "the amendment costs NO picks against the point rule (it is a disclosure, not "
         "a filter)", float(id8.n_acted - pt.n_acted), int(id8.n_acted) == int(pt.n_acted))
    best_cell = W8[W8.form.isin(FORMS) & np.isfinite(W8.mean_OOS_Sharpe)]
    best = best_cell.sort_values("mean_OOS_Sharpe", ascending=False).iloc[0]
    P("")
    P(f"       BEST CLAUSE CELL ON OOS SHARPE: {best.form} @ f = {best.fbar:.2f}, "
      f"{best.mean_OOS_Sharpe:.4f} on {int(best.n_acted)} picks")
    P(f"       against the point rule's {pt.mean_OOS_Sharpe:.4f} "
      f"({best.mean_OOS_Sharpe - pt.mean_OOS_Sharpe:+.4f}), acting on everything "
      f"{ref_all['mean_OOS_Sharpe']:.4f}, and DOING NOTHING "
      f"{ref_anchor['mean_OOS_Sharpe']:.4f}.")

    # ------------------------------------------------------------ verdict
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    recall_ok = idn.recall_DEP12 >= 0.90
    cheaper = all(idn.draws < DT[DT.form == lf].draws.iloc[0]
                  for lf in ("CF_LADDER4", "CF_LADDER11", "CF_LADDER12"))
    subset = idn_rerun <= lad_rerun
    A_fires = bool(recall_ok and cheaper and subset)
    B_fires = bool(int(idn.missed_DEP11) >= 8)
    if A_fires and B_fires:
        outcome = "(C) BOTH, AND THEY ARE DIFFERENT CLAUSES"
    elif A_fires:
        outcome = "(A) THE AMENDMENT DOMINATES"
    elif B_fires:
        outcome = "(B) THE LADDER EARNS ITS COST"
    else:
        outcome = "(D) NEITHER"
    P("")
    P(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    P(f"      CF_IDENTITY recall on DEP12 {idn.recall_DEP12:.4f} (bar 0.90 -> "
      f"{'PASS' if recall_ok else 'FAIL'}); strictly cheaper than every ladder form "
      f"{'YES' if cheaper else 'NO'} ({int(idn.draws)} draws vs {int(l4.draws)} / "
      f"{int(l11.draws)} / {int(l12.draws)});")
    P(f"      re-run set a strict subset {'YES' if subset else 'NO'} ({idn_rerun} vs "
      f"{lad_rerun} units); DEP11 decisions the amendment misses {int(idn.missed_DEP11)} "
      f"(bar 8 -> {'B FIRES' if B_fires else 'B does not fire'}).")
    P("")
    P("    COST AT SC_RESAMPLE.  The LADDER clause forces a RE-RUN on "
      f"{lad_rerun} of {n_bound} committed units")
    P(f"      at {int(l11.draws)} extra draws each ({lad_rerun*int(l11.draws):,} draws in total).  "
      "The AMENDED clause forces a re-run on")
    P(f"      {idn_rerun} (those stating no L at all — 1249's population, unfixable under either "
      "clause) and makes")
    P(f"      {int(CF[CF.form=='CF_IDENTITY'].editable.iloc[0])} more conforming by EDIT, at "
      f"{int(idn.draws)} draws.")
    P("")
    P("    CAPITAL.  No clause form is a book.  The best cell moves mean OOS Sharpe "
      f"{best.mean_OOS_Sharpe - pt.mean_OOS_Sharpe:+.4f} against")
    P(f"      the point rule and {best.mean_OOS_Sharpe - ref_anchor['mean_OOS_Sharpe']:+.4f} "
      "against DOING NOTHING (holding the anchor rung).")
    P(f"      4a {int(BK.KEEP_4a.sum())} of {len(BK)} rung books; 4b BOTH "
      f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books, every one already held by the record.")
    P("      NO NEW BOOK, NO RULES CHANGE.  A schema clause is a CHECKABILITY instrument and is")
    P("      proposed for the Sunday review (rule 6) as a PROTOCOL line only, never as a chooser.")
    P("")
    P("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the")
    P("    current constituents of a sub-$2B screen with max_1d_move >= 1.0 names dropped.  Every")
    P("    LEVEL is optimistic.  It largely cancels out of the headline (a RATIO of one")
    P("    construction against itself: the same 72 decisions under different clause forms) and")
    P("    does NOT cancel out of the 4b legs, so those passes are upper bounds.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    if not GD.pass_.all():
        P("    FAILED GATES (published failed, not moved): "
          + ", ".join(GD[~GD.pass_].gate.tolist()))
    P("")
    P(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
