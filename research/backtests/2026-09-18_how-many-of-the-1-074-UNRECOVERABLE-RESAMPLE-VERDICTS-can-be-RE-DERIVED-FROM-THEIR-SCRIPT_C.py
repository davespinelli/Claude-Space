#!/usr/bin/env python3
"""QUEUE idea 1249 (lane C, 2026-09-18) — how many of the 1,074 UNRECOVERABLE RESAMPLE
VERDICTS can be RE-DERIVED FROM THEIR SCRIPT?

QUESTION (QUEUE '## Open', verbatim)
    idea 1243 found 1,074 of the 1,371 units a resample-keyed schema clause would bind state
    no L at all, so editing cannot bring them into conformance.  Resolve each to the committed
    script that produced it and report how many carry a recoverable L in code where the prose
    lost it, and what a re-run of the rest would cost in draws.  Max 2 params (claim set,
    resolution rule).

WHY THE QUESTION IS WORTH A RUN.  1243's 1,074 is the single largest cost number in the
record's schema-clause debate: it is the count of committed verdicts that a resample-keyed
clause would make non-conforming AND that no amount of editing could repair, because the
sentence itself carries no block length.  1247 (lane C, yesterday) then priced the cheapest
conforming clause and billed 1,099 re-runs against exactly this population.  BOTH numbers
assume the L is GONE.  It need not be: every committed unit was emitted by a committed script,
and a script that ran a block bootstrap had to name an L somewhere to run it.  If the code
kept what the prose dropped, the bill is an EDIT, not a re-run, and the difference is four
orders of magnitude in draws.  This run measures which it is.

THE POPULATION IS A CENSUS, NOT A SAMPLE, AND IT IS PINNED TO 1243's OWN TREE.
    1230 (lane C, 2026-09-17) proved the record's censuses are REFLEXIVE and have no fixed
    point: a census committed to the record changes the record it censused.  Re-harvesting
    today's corpus therefore CANNOT return 1,074 — three lanes have committed since — and then
    no number here would be comparable to the number the queue asks about.  So the corpus is
    recovered from git at `e890434^`, the PARENT of the commit that added 1243's outputs, i.e.
    the tree 1243's census actually read.  G1 requires this run's census to reproduce 1243's
    committed `.scope.csv` on all three scopes and all seven columns EXACTLY; if it does not,
    the run says so and stops trusting the population.  Today's HEAD corpus is harvested too,
    as a CONTROL, and its size is published beside the pinned one (ARM A).

THE TWO TUNED DIALS AND NO MORE (PROTOCOL rule 4; the queue names both)
    CLAIM SET {CS_BLOCK, CS_RESAMPLE, CS_ALL} x RESOLUTION RULE {R_CONST, R_LADDER, R_ANY,
    R_UNION} = 12 cells, EVERY ONE PUBLISHED (.recovery.csv), and every one also reported on
    the capital arm (.walkforward.csv).
      CLAIM SET — 1243's own three scopes, intersected with its "unrecoverable" test
      (states no L AND states no L ladder).  Nested by construction; G5 checks it.
        CS_BLOCK      1243's SC_BLOCK unrecoverable set        (committed: 154)
        CS_RESAMPLE   1243's SC_RESAMPLE unrecoverable set     (committed: 1,074)  HEADLINE
        CS_ALL        1243's SC_ALL unrecoverable set          (committed: 7,631)
      RESOLUTION RULE — what counts as "the script carries a recoverable L".  Nested by
      construction; G4 checks it.
        R_CONST   a MODULE-LEVEL assignment (including tuple unpacking, which is how this
                  record's scripts write `L_HEAD, BDRAWS = 63, 1000`) whose target name is in
                  the declared L-NAME SET and whose right-hand side is ONE integer literal in
                  [1, 5000].  The script states a point L.
        R_LADDER  R_CONST plus list/tuple literals of such integers (and the token "T").  The
                  script WALKS an L ladder — which is not a failure but the strongest possible
                  conformance with 1208's clause, so it is credited.  HEADLINE.
        R_ANY     R_LADDER plus any `L=<int>` keyword argument, any `def f(..., L=<int>)`
                  default, and any integer literal passed to a block-resampling call site
                  (`block_index`, `pboot*`, `blockboot*`, `moving_block*`) anywhere in the
                  file.  The L is in the code but not as a named constant.
        R_UNION   R_ANY plus the SIBLING PROSE: an L stated anywhere in the emitting script's
                  own artefact family (its module docstring and every other paragraph of the
                  .md file the unit came from).  This is the honest upper bound on "the prose
                  lost it" — a neighbouring sentence may have kept it.
      A CALL-SITE DEFAULT IS NOT READ AS A PIN under R_CONST/R_LADDER (`def f(..., L=63)` is a
      signature, not a decision); it is exactly what R_ANY adds, and the two are reported
      separately so the reader can see which half of the answer is load-bearing.

ATTRIBUTION IS NOT A DIAL.  All four paths are run on every unit, in this fixed precedence,
and each path's marginal reach is published (.attrib.csv):
      A_STEM  the unit's own source file `X.result.md` / `X.memo.md` -> `X.py`.  The record's
              artefact convention, and the only path that is an identity rather than a lookup.
      A_COL   a LEADERBOARD row's last column — PROTOCOL rule 5's script column.
      A_NAME  any `*.py` filename token appearing in the unit's own text.
      A_IDEA  a LEADERBOARD row opening `NNNN lane X` -> the committed script for idea NNNN in
              lane X.  Restricted to that pattern ON PURPOSE: an "idea 1243 found ..." mention
              inside a body paragraph names the PARENT idea, not the emitter, and attributing
              on it would silently mis-credit.  The count it would have added is published.
    Every unit gets AT MOST ONE script (G3) and the script must exist at the pinned vintage.

PRE-DECLARED OUTCOMES (fixed before the recovery arm was run; the verdict is read off)
    (A) THE SCRIPT KEPT IT — >= 0.50 of the claim set resolves to a script with a recoverable L
        under the headline rule R_LADDER.  1243's and 1247's re-run bills are then wrong by
        construction: the repair is a STAMP on committed text, at zero draws.
    (B) THE SCRIPT LOST IT TOO — < 0.25 recoverable.  The record did not drop an L it had; it
        largely never fixed one, and 1243's "editing cannot bring them into conformance"
        stands as written.
    (C) ATTRIBUTION IS THE BINDING CONSTRAINT — more units fail for want of an identifiable
        emitting script than for want of an L inside the script they do have.

HYPOTHESES, PRE-REGISTERED AND UNMEASURED WHEN THIS FILE WAS WRITTEN
    CALIBRATED, AND SAYING SO IS CHEAPER THAN PRETENDING: the CENSUS arm (ARM A) was built and
    run in a wiring prototype before this file was written, so its counts are MEASUREMENTS
    reported against 1243's committed file, not forecasts, and are labelled CALIBRATED where
    quoted.  Everything in ARMS B, C, D and E below was unmeasured when this was written.
      H_REACH       [PRE-REGISTERED] >= 0.90 of the claim set resolves to a committed script
                    that exists at the pinned vintage.  (1149's H_CITE, on a new population.)
      H_LADDER      [PRE-REGISTERED] among RESOLVED units, LADDER-carrying scripts outnumber
                    POINT-pinned ones.  The record's stated habit is to walk L.
      H_STEM        [PRE-REGISTERED] A_STEM alone reaches more units than A_COL alone.
      H_HEAD63      [PRE-REGISTERED] among scripts that pin a single L, the modal value is the
                    record's frozen 63, at a share >= 0.50.
      H_EDIT        [PRE-REGISTERED] units repairable by EDIT (script carries an L) outnumber
                    units owing a RE-RUN.  This is outcome (A) as a head-to-head count.
      H_CAPITAL     [PRE-REGISTERED] no (claim set, resolution rule) cell moves mean OOS Sharpe
                    by more than 0.02 against BOTH references.  A recoverability rule is a
                    DISCLOSURE about the archive, not a filter on capital; if it does move
                    money, that is the finding and it is reported as one.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); ANCHOR {A, B}; the four
ladders N / H / GROSS / CADENCE; the three choosers CH_ISSHARPE / CH_ISCAGR / CH_ISDD; the
resolution bar q = 0.90; B = 1000 draws; the clause forms CF_POINT / CF_LADDER4 / CF_LADDER11 /
CF_IDENTITY (1247's) for the draws bill; the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION (1101/1208/1243/1247): 3-leg composite (21/252, 0/126,
0/63), above-200d eligibility, max_vol 0.60, 10 bps (rule 2), decide-at-t / apply-at-t+1,
warm-up 260 rows, IS end 2016-12-31 (rule 8), 4b constants 0.60 / 0.70.

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every pick made on the IS window
ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every rung
book and every grid cell; rule 9 survivorship stated in the verdict.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches and the committed git history
only).
"""
from __future__ import annotations

import ast
import io
import re
import subprocess
import sys
import tarfile
import tempfile
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
SLUG = "how-many-of-the-1-074-UNRECOVERABLE-RESAMPLE-VERDICTS-can-be-RE-DERIVED-FROM-THEIR-SCRIPT"
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
SEED_BASE = 12491249
L_HEAD = 63

# ------------------------------------------------------------------ the two dials
CLAIMSETS = ["CS_BLOCK", "CS_RESAMPLE", "CS_ALL"]
CS_HEAD = "CS_RESAMPLE"
RULES = ["R_CONST", "R_LADDER", "R_ANY", "R_UNION"]
R_HEAD = "R_LADDER"

# the clause forms whose draw bills are priced (1247's; the identity rung is FREE)
FORMS = ["CF_POINT", "CF_IDENTITY", "CF_LADDER4", "CF_LADDER11"]

# ------------------------------------------------------------------ the pinned corpus
PIN_COMMIT = "e890434^"          # the PARENT of 1243's commit: the tree 1243's census read
PIN_LABEL = "e890434^ (parent of 1243's commit)"

# ------------------------------------------------------------------ the record's own numbers
A1243_SCOPE = {           # 1243's committed .scope.csv, verbatim — the thing G1 reproduces
    "SC_BLOCK":    dict(bound=489,  states_L=331, states_LADDER=39, carries_verdict=272,
                        floor_keyed=166,  non_conforming=450,  unrecoverable=154),
    "SC_RESAMPLE": dict(bound=1413, states_L=332, states_LADDER=42, carries_verdict=1196,
                        floor_keyed=575,  non_conforming=1371, unrecoverable=1074),
    "SC_ALL":      dict(bound=7989, states_L=335, states_LADDER=58, carries_verdict=4260,
                        floor_keyed=6353, non_conforming=7931, unrecoverable=7631),
}
A1247_RERUNS = 1099       # 1247's committed re-run bill against this very population
A1208_NDEC = 72
A1101_TRIPLE = (0.155787, 1.139701, -0.191276)
LIVE_MAXDD_COMMITTED = -0.1205
T_IS_REF = 2007

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
    P(f"  {name:<5s} {'PASS' if ok else 'FAIL'}  {what:<74s} {value:.4e}")
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
    """P(each rung is the argmax of `stat`) under JOINT moving-block redraws of the IS window."""
    T, k = R.shape
    rng = np.random.default_rng(seed)
    cnt = np.zeros(k)
    done = 0
    while done < B:
        b = min(chunk, B - done)
        idx = block_index(rng, T, L, b)
        X = R[idx]                                   # (b, T, k)
        if stat == "CH_ISSHARPE":
            sd = X.std(axis=1, ddof=1)
            v = np.where(sd > 0, X.mean(axis=1) * 252.0 / (sd * np.sqrt(252.0)), -np.inf)
        elif stat == "CH_ISCAGR":
            eq = np.prod(1.0 + X, axis=1)
            v = np.sign(eq) * np.abs(eq) ** (252.0 / T) - 1.0
        else:                                        # CH_ISDD
            eq = np.cumprod(1.0 + X, axis=1)
            v = (eq / np.maximum.accumulate(eq, axis=1) - 1.0).min(axis=1)
        cnt += np.bincount(np.nanargmax(v, axis=1), minlength=k)
        done += b
    return cnt / B


def is_stat(r, ins, stat):
    x = np.asarray(r, float)[ins]
    T_is = len(x)
    if stat == "CH_ISSHARPE":
        sd = x.std(ddof=1)
        return (x.mean() * 252.0) / (sd * np.sqrt(252.0)) if sd > 0 else -np.inf
    if stat == "CH_ISCAGR":
        return float(np.cumprod(1.0 + x)[-1] ** (252.0 / T_is) - 1.0)
    eq = np.cumprod(1.0 + x)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())


# ================================================================== ARM A: 1243's census, pinned
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


def units_of(rroot):
    """1243's unit definition, verbatim: LEADERBOARD rows, CHANGELOG paragraphs, md paragraphs."""
    U = []
    for ln in (rroot / "LEADERBOARD.md").read_text(errors="ignore").split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in (rroot / "CHANGELOG.md").read_text(errors="ignore").split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    n_md = 0
    for f in sorted((rroot / "backtests").rglob("*.md")):
        n_md += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, n_md


def census_of(rroot):
    U, n_md = units_of(rroot)
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
            CS_STRICT=bt, CS_PROX=bt or rs,
            CS_ALL_FILE=fileset.get(src, False) and (bt or rs),
            HAS_RESAMPLE_STAT=rs,
            STATES_L=bool(ls), L_STATED=ls[0] if ls else 0,
            STATES_L_LADDER=bool(LADDERTOK.search(txt)),
            CARRIES_VERDICT=bool(VERDICTTOK.search(txt)),
            FLOOR_KEYED=bool(FLOORTOK.search(txt)), _txt=txt))
    return pd.DataFrame(rows), len(U), n_md


def scope_mask(C, sc):
    """1243's scope_frame, verbatim."""
    if sc == "SC_BLOCK":
        return C.CS_STRICT
    if sc == "SC_RESAMPLE":
        return C.CS_STRICT | (C.HAS_RESAMPLE_STAT & C.CARRIES_VERDICT)
    return C.CS_STRICT | C.HAS_RESAMPLE_STAT | C.FLOOR_KEYED


def scope_frame(C):
    rows = []
    for sc in ["SC_BLOCK", "SC_RESAMPLE", "SC_ALL"]:
        z = C[scope_mask(C, sc)]
        rows.append(dict(scope=sc, bound=len(z),
                         states_L=int(z.STATES_L.sum()),
                         states_LADDER=int(z.STATES_L_LADDER.sum()),
                         carries_verdict=int(z.CARRIES_VERDICT.sum()),
                         floor_keyed=int(z.FLOOR_KEYED.sum()),
                         non_conforming=int((~z.STATES_L_LADDER).sum()),
                         unrecoverable=int((~z.STATES_L & ~z.STATES_L_LADDER).sum())))
    return pd.DataFrame(rows)


# ================================================================== ARM B: attribution
PYTOK = re.compile(r"[0-9A-Za-z_][0-9A-Za-z_.\-]*\.py\b")
LBROW_IDEA = re.compile(r"^\|\s*20\d\d-\d\d-\d\d\s*\|\s*\**\s*(\d{3,4})\s+lane\s+([A-Za-z]+)")
BODY_IDEA = re.compile(r"\bidea\s+(\d{3,4})\b", re.I)
MDSTEM = re.compile(r"^(?P<stem>.+?)\.(result|memo|MEMO|README|notes)\.md$")


def script_index(sroot):
    """Every committed .py in research/backtests at the pinned vintage, indexed by
    (a) filename, (b) (idea number, lane) read from the FILENAME's lane suffix and the
    module docstring's first `idea NNNN` mention."""
    byname, byidea = {}, {}
    for f in sorted(sroot.glob("*.py")):
        byname[f.name] = f
        lane = None
        m = re.search(r"_(C|B|A|D|cloud|local)\.py$", f.name)
        if m:
            lane = m.group(1)
        head = "\n".join(f.read_text(errors="ignore").split("\n")[:8])
        mi = BODY_IDEA.search(head)
        if mi and lane:
            byidea.setdefault((mi.group(1), lane.lower()), f)
    return byname, byidea


def attribute(C, byname, byidea):
    """unit -> at most one committed script, by the fixed precedence A_STEM > A_COL > A_NAME
    > A_IDEA.  Every path's own reach is recorded so the marginal contribution is publishable."""
    recs = []
    for i, row in C.iterrows():
        src, txt = row.src, row._txt
        hit = {p: None for p in ("A_STEM", "A_COL", "A_NAME", "A_IDEA")}
        m = MDSTEM.match(src)
        if m:
            cand = m.group("stem") + ".py"
            if cand in byname:
                hit["A_STEM"] = cand
        if src == "LEADERBOARD":
            cells = [c.strip() for c in txt.strip().strip("|").split("|")]
            if cells:
                last = cells[-1].strip().strip("`* ")
                if last in byname:
                    hit["A_COL"] = last
            mi = LBROW_IDEA.match(txt)
            if mi:
                key = (mi.group(1), mi.group(2).lower())
                if key in byidea:
                    hit["A_IDEA"] = byidea[key].name
        for tok in PYTOK.findall(txt):
            t = tok.strip("`*")
            if t in byname:
                hit["A_NAME"] = t
                break
        chosen, path = None, "NONE"
        for p in ("A_STEM", "A_COL", "A_NAME", "A_IDEA"):
            if hit[p]:
                chosen, path = hit[p], p
                break
        recs.append(dict(uid=i, src=src, script=chosen, path=path,
                         **{f"hit_{p}": (hit[p] or "") for p in hit}))
    return pd.DataFrame(recs).set_index("uid")


# ================================================================== ARM C: L recovery from code
LNAME = re.compile(
    r"^(L|LS|LB|LGRID|L_GRID|L_HEAD|L_BLOCK|L_LADDER|L_LADDERS|L_STAR|L_SIDE|L_BASE|L_V1|"
    r"L_SPY|L_ROLL|L_PICK|L_RUNGS|L_ALL|L_PAIRS|L_LAD|L_COARSE|L_FOLD|LL|LL_FULL|LL_REC|"
    r"LL_HEAD|LL_WIDE|LAD_L|ALL_L|BASE_L|CORE_L|WIDE_L|BOOT_L|BOOK_L|PXABS_L|BLOCK|BLOCKS|"
    r"BLOCKS_L|BLOCKS_W|BLOCK_L|BLOCK_LEN|BLOCK_LENS|BLOCK_LENGTH|BLOCK_YEARS|BLOCK_PRIMARY|"
    r"BLOCK_HEAD|BLOCK_TAPE|BOOT_BLOCK|NULL_BLOCK|PERM_BLOCK|CTX_BLOCK|QUEUE_BLOCK)$")
BLOCKCALL = re.compile(r"^(block_index|blockboot\w*|pboot\w*|moving_block\w*|block_\w*boot\w*)$")
# Did the SCRIPT ever run a block resample at all?  This is the question behind the question:
# 1243's RESAMPTOK binds any unit saying "percentile" or "draws", so a unit can be counted
# non-conforming although the code that produced it never drew a block in its life — and then
# there is no L to have lost and nothing to re-run.  Source-level, deliberately GENEROUS.
BLOCKSRC = re.compile(
    r"\b(block_index|blockboot\w*|pboot\w*|moving_block\w*|block_\w*boot\w*|"
    r"moving[- ]block|block bootstrap|block[- ]bootstrap|block[- ]permutation|"
    r"stationary bootstrap|block length)\b", re.I)
LMIN, LMAX = 1, 5000


def _lit_ints(node):
    """The integer L values a literal right-hand side carries.  A plain int -> [v]; a
    list/tuple of ints (and the token "T") -> its ints, with "T" recorded as the identity."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            return None
        if isinstance(node.value, int) and LMIN <= node.value <= LMAX:
            return [node.value]
        if isinstance(node.value, str) and node.value == "T":
            return ["T"]
        return None
    if isinstance(node, (ast.List, ast.Tuple)):
        out = []
        for e in node.elts:
            v = _lit_ints(e)
            if v is None:
                return None
            out += v
        return out or None
    return None


def recover_L(path: Path):
    """What L the SCRIPT states, under each of the four resolution rules.  Returns a dict of
    rule -> (kind, values) where kind is PINNED / LADDER / SILENT."""
    src = path.read_text(errors="ignore")
    out = {r: ("SILENT", []) for r in RULES}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out, src
    const_v, ladder_v, any_v = [], [], []
    for node in tree.body:                                     # MODULE LEVEL ONLY
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        names, values = [], []
        for t in targets:
            if isinstance(t, ast.Name):
                names.append((t.id, node.value))
            elif isinstance(t, (ast.Tuple, ast.List)) and isinstance(node.value,
                                                                     (ast.Tuple, ast.List)) \
                    and len(t.elts) == len(node.value.elts):
                for e, v in zip(t.elts, node.value.elts):
                    if isinstance(e, ast.Name):
                        names.append((e.id, v))
        del values
        for nm, val in names:
            if not LNAME.match(nm):
                continue
            vs = _lit_ints(val)
            if not vs:
                continue
            ints = [v for v in vs if isinstance(v, int)]
            if not ints:
                continue
            if len(set(vs)) == 1 and len(vs) == 1:
                const_v += ints
            else:
                ladder_v += ints
    # R_ANY: keyword args, defaults and block-call literals anywhere in the file
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            fname = fn.id if isinstance(fn, ast.Name) else (
                fn.attr if isinstance(fn, ast.Attribute) else "")
            for kw in node.keywords:
                if kw.arg and LNAME.match(kw.arg.upper()):
                    vs = _lit_ints(kw.value)
                    if vs:
                        any_v += [v for v in vs if isinstance(v, int)]
            if BLOCKCALL.match(fname or ""):
                for a in node.args:
                    vs = _lit_ints(a)
                    if vs:
                        any_v += [v for v in vs if isinstance(v, int)]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            allargs = list(args.args) + list(args.kwonlyargs)
            defs = ([None] * (len(args.args) - len(args.defaults)) + list(args.defaults)
                    + list(args.kw_defaults))
            for a, d in zip(allargs, defs):
                if d is None or not LNAME.match(a.arg.upper()):
                    continue
                vs = _lit_ints(d)
                if vs:
                    any_v += [v for v in vs if isinstance(v, int)]
    out["R_CONST"] = ("PINNED", sorted(set(const_v))) if const_v else ("SILENT", [])
    lad = const_v + ladder_v
    if ladder_v:
        out["R_LADDER"] = ("LADDER", sorted(set(lad)))
    elif const_v:
        out["R_LADDER"] = ("PINNED", sorted(set(const_v)))
    else:
        out["R_LADDER"] = ("SILENT", [])
    al = lad + any_v
    if al:
        out["R_ANY"] = ("LADDER" if len(set(al)) > 1 else "PINNED", sorted(set(al)))
    else:
        out["R_ANY"] = ("SILENT", [])
    return out, src


def prose_L_of(text):
    return sorted({int(g) for m in LTOK.finditer(text) for g in m.groups() if g})


# ================================================================== ARM D: the draws bill
def form_rungs(form):
    if form == "CF_POINT":
        return [L_HEAD]
    if form == "CF_IDENTITY":
        return [L_HEAD, "T"]
    if form == "CF_LADDER4":
        return list(LL_REC)
    if form == "CF_LADDER11":
        return list(RUNGS_FINITE)
    raise ValueError(form)


def draws_per_verdict(form, B):
    """1247's accounting: the identity rung L = T has one legal block start, so it costs no
    draw and is not charged.  Every other rung costs B."""
    return sum(0 if str(r) == "T" else B for r in form_rungs(form))


BNAME = re.compile(r"^(B|BDRAWS|B_DRAWS|NDRAW|NDRAWS|N_DRAWS|BOOT|BOOTS|NBOOT|N_BOOT|DRAWS|"
                   r"B_BOOT|BOOT_B|NSIM|N_SIM|NPERM|N_PERM)$")


def recover_B(path: Path, default=BDRAWS):
    """The script's own draw count, from a module-level constant; else the record's modal B."""
    try:
        tree = ast.parse(path.read_text(errors="ignore"))
    except SyntaxError:
        return default, False
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        pairs = []
        for t in targets:
            if isinstance(t, ast.Name):
                pairs.append((t.id, node.value))
            elif isinstance(t, (ast.Tuple, ast.List)) and isinstance(node.value,
                                                                     (ast.Tuple, ast.List)) \
                    and len(t.elts) == len(node.value.elts):
                pairs += [(e.id, v) for e, v in zip(t.elts, node.value.elts)
                          if isinstance(e, ast.Name)]
        for nm, val in pairs:
            if BNAME.match(nm) and isinstance(val, ast.Constant) \
                    and isinstance(val.value, int) and not isinstance(val.value, bool) \
                    and 50 <= val.value <= 1_000_000:
                return int(val.value), True
    return default, False


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


# ================================================================== the cite-map (capital arm)
PANTOK = {
    "U56": re.compile(r"\bU56\b|\buniverse\.json\b|\b56[- ]name", re.I),
    "B136": re.compile(r"\bB13[56]\b|\bbroad\b|prices_broad", re.I),
    "SMALL": re.compile(r"\bSMALL\d*\b|\bsmall[- ]cap", re.I),
}
LADTOK = {
    "N": re.compile(r"\bN ladder\b|\bn dial\b|\bN\s*=\s*\d+|\bslot count\b|\btop-\d+\b", re.I),
    "H": re.compile(r"\bH ladder\b|\bmin(?:imum)?[- ]hold\b|\bH\s*=\s*\d+|\bhold\b", re.I),
    "GROSS": re.compile(r"\bgross\b|\bde-?gross\w*\b", re.I),
    "CADENCE": re.compile(r"\bcadence\b|\bweekly\b|\bmonthly\b|\bquarterly\b|\brebalance\b", re.I),
}


def main():
    t_start = time.time()
    P("=" * 112)
    P(f"IDEA 1249 (lane C, {DATE}) — HOW MANY OF THE 1,074 UNRECOVERABLE RESAMPLE VERDICTS")
    P("CAN BE RE-DERIVED FROM THEIR SCRIPT?")
    P("=" * 112)
    P("")
    P("  DIALS (2, PROTOCOL rule 4): CLAIM SET {CS_BLOCK, CS_RESAMPLE, CS_ALL} x")
    P("                              RESOLUTION RULE {R_CONST, R_LADDER, R_ANY, R_UNION}")
    P(f"  HEADLINE CELL: {CS_HEAD} x {R_HEAD}.  All 12 cells published (.recovery.csv).")
    P("")

    # ---------------------------------------------------------------- ARM A: the pinned census
    P("=" * 112)
    P("ARM A — THE POPULATION, PINNED TO 1243's OWN TREE  [CALIBRATED: measured in a wiring")
    P("        prototype before this file was written; reported against 1243's committed file]")
    P("=" * 112)
    P("")
    P(f"  1230 proved the record's censuses have NO FIXED POINT, so the corpus is recovered")
    P(f"  from git at {PIN_LABEL} — the tree 1243's census actually read.")
    tmp = tempfile.mkdtemp(prefix="idea1249_")
    try:
        blob = subprocess.run(["git", "archive", PIN_COMMIT, "research"],
                              cwd=str(ROOT), capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
            tf.extractall(tmp)
        got_pin = True
    except Exception as e:                                       # noqa: BLE001
        P(f"  !! git archive FAILED: {e}")
        got_pin = False
    gate("G0", f"the pinned corpus {PIN_LABEL} was recovered from git", float(got_pin), got_pin)
    if not got_pin:
        raise SystemExit("cannot pin the corpus; the population would not be 1243's")
    PR = Path(tmp) / "research"

    C, n_units, n_md = census_of(PR)
    SF = scope_frame(C)
    SF.to_csv(f"{OUT}.scope.csv", index=False)
    P("")
    P(f"  PINNED corpus: {n_units} text units over {n_md} committed .md files + LEADERBOARD "
      f"rows + CHANGELOG paragraphs.")
    P("")
    P("  scope         bound  states_L  ladder  verdict  floor  non_conf  UNRECOVERABLE   "
      "1243's committed")
    dev = 0
    for _, r in SF.iterrows():
        a = A1243_SCOPE[r.scope]
        d = max(abs(int(r[k]) - a[k]) for k in a)
        dev = max(dev, d)
        P(f"  {r.scope:12s} {int(r.bound):6d} {int(r.states_L):9d} {int(r.states_LADDER):7d} "
          f"{int(r.carries_verdict):8d} {int(r.floor_keyed):6d} {int(r.non_conforming):9d} "
          f"{int(r.unrecoverable):14d}   {a['unrecoverable']:d}  (max col dev {d})")
    gate("G1", "this run's census reproduces 1243's committed .scope.csv EXACTLY (all 3 scopes, "
         "7 cols)", float(dev), dev == 0)

    # today's corpus, as a control on the reflexivity
    Ch, n_h, nmd_h = census_of(ROOT / "research")
    SFh = scope_frame(Ch)
    P("")
    P(f"  CONTROL — TODAY'S HEAD corpus: {n_h} units over {nmd_h} .md files "
      f"({n_h - n_units:+d} units, {nmd_h - n_md:+d} files since 1243 ran).  Its SC_RESAMPLE")
    P(f"  unrecoverable count is {int(SFh[SFh.scope=='SC_RESAMPLE'].unrecoverable.iloc[0])}, "
      f"NOT 1,074.  Every number below is about the PINNED tree, and says so.")

    POP = {}
    for cs, sc in zip(CLAIMSETS, ["SC_BLOCK", "SC_RESAMPLE", "SC_ALL"]):
        m = scope_mask(C, sc) & ~C.STATES_L & ~C.STATES_L_LADDER
        POP[cs] = C[m]
    nested = (set(POP["CS_BLOCK"].index) <= set(POP["CS_RESAMPLE"].index)
              <= set(POP["CS_ALL"].index))
    gate("G5", "the three claim sets are NESTED (CS_BLOCK c CS_RESAMPLE c CS_ALL)",
         float(nested), nested)
    gate("G2", f"the headline claim set is 1243's 1,074", float(len(POP[CS_HEAD])),
         len(POP[CS_HEAD]) == A1243_SCOPE["SC_RESAMPLE"]["unrecoverable"])
    zero_prose = int(POP[CS_HEAD].STATES_L.sum()) + int(POP[CS_HEAD].STATES_L_LADDER.sum())
    gate("G9", "0 units in the population state an L in their own prose (by construction)",
         float(zero_prose), zero_prose == 0)
    P("")
    for cs in CLAIMSETS:
        z = POP[cs]
        P(f"  {cs:12s} {len(z):6d} units   "
          f"LEADERBOARD {int((z.src=='LEADERBOARD').sum()):5d}   "
          f"CHANGELOG {int((z.src=='CHANGELOG').sum()):4d}   "
          f"md {int((~z.src.isin(['LEADERBOARD','CHANGELOG'])).sum()):5d} "
          f"over {z[~z.src.isin(['LEADERBOARD','CHANGELOG'])].src.nunique()} files")

    # ---------------------------------------------------------------- ARM B: attribution
    P("")
    P("=" * 112)
    P("ARM B — ATTRIBUTION: DOES EACH UNIT RESOLVE TO A COMMITTED SCRIPT?")
    P("=" * 112)
    byname, byidea = script_index(PR / "backtests")
    P("")
    P(f"  {len(byname)} committed .py files at the pinned vintage; {len(byidea)} carry a "
      f"recoverable (idea, lane) key.")
    AT = attribute(C, byname, byidea)
    # committed for the POPULATION only (CS_ALL, the widest claim set) — the full 34,095-row
    # census attribution is reproducible from this script and is not worth 7.8 MB in the tree.
    AT.loc[POP["CS_ALL"].index].to_csv(f"{OUT}.attrib.csv")
    onecall = bool((AT.script.notna() == (AT.path != "NONE")).all())
    gate("G3", "attribution is a FUNCTION: every unit gets at most one existing script",
         float(onecall), onecall)
    P("")
    P("  claim set    units   A_STEM   A_COL   A_NAME   A_IDEA    NONE    reach")
    arows = []
    for cs in CLAIMSETS:
        a = AT.loc[POP[cs].index]
        vc = a.path.value_counts()
        reach = float((a.path != "NONE").mean())
        P(f"  {cs:12s} {len(a):6d} {int(vc.get('A_STEM',0)):8d} {int(vc.get('A_COL',0)):7d} "
          f"{int(vc.get('A_NAME',0)):8d} {int(vc.get('A_IDEA',0)):8d} "
          f"{int(vc.get('NONE',0)):7d}   {reach:.4f}")
        arows.append(dict(claim_set=cs, units=len(a),
                          **{p: int(vc.get(p, 0)) for p in
                             ("A_STEM", "A_COL", "A_NAME", "A_IDEA", "NONE")}, reach=reach))
        # standalone reach of each path, for the marginal reading
        for p in ("A_STEM", "A_COL", "A_NAME", "A_IDEA"):
            arows[-1][f"alone_{p}"] = int((a[f"hit_{p}"] != "").sum())
    AR = pd.DataFrame(arows)
    AR.to_csv(f"{OUT}.attribreach.csv", index=False)
    ah = AR[AR.claim_set == CS_HEAD].iloc[0]
    P("")
    P("  STANDALONE reach of each path on the headline claim set (they overlap; the table "
      "above is the precedence):")
    P(f"       A_STEM {int(ah.alone_A_STEM):5d}   A_COL {int(ah.alone_A_COL):5d}   "
      f"A_NAME {int(ah.alone_A_NAME):5d}   A_IDEA {int(ah.alone_A_IDEA):5d}")
    body_idea_extra = int(sum(1 for i in POP[CS_HEAD].index
                              if AT.loc[i, "path"] == "NONE"
                              and BODY_IDEA.search(POP[CS_HEAD].loc[i, "_txt"] or "")))
    P(f"  PUBLISHED, NOT USED: {body_idea_extra} unattributed units carry an 'idea NNNN' "
      f"mention in the BODY.  That names the PARENT idea, not the emitter, so attributing on")
    P("  it would mis-credit; the count is reported so a lane wanting the looser rule has it.")
    H_REACH = float(ah.reach) >= 0.90
    H_STEM = int(ah.alone_A_STEM) > int(ah.alone_A_COL)

    # ---------------------------------------------------------------- ARM C: the recovery
    P("")
    P("=" * 112)
    P("ARM C — RECOVERY: DOES THE EMITTING SCRIPT CARRY AN L THE PROSE LOST?")
    P("=" * 112)
    scripts = sorted({s for s in AT.script.dropna().unique()})
    P("")
    P(f"  {len(scripts)} distinct emitting scripts across the whole census.  Parsing each once.")
    SREC, SB, SBLK = {}, {}, {}
    sp_rows = []
    for nm in scripts:
        f = byname[nm]
        rec, src = recover_L(f)
        b, b_named = recover_B(f)
        SREC[nm], SB[nm] = rec, (b, b_named)
        sp_rows.append(dict(script=nm,
                            R_CONST=rec["R_CONST"][0], R_CONST_vals=str(rec["R_CONST"][1]),
                            R_LADDER=rec["R_LADDER"][0], R_LADDER_vals=str(rec["R_LADDER"][1]),
                            R_ANY=rec["R_ANY"][0], R_ANY_vals=str(rec["R_ANY"][1]),
                            has_block=bool(BLOCKSRC.search(src)), B=b, B_named=b_named))
        SBLK[nm] = bool(BLOCKSRC.search(src))
    SP = pd.DataFrame(sp_rows)
    SP.to_csv(f"{OUT}.scripts.csv", index=False)
    nest_ok = True
    for nm in scripts:
        a, b_, c_ = (set(SREC[nm][r][1]) for r in ("R_CONST", "R_LADDER", "R_ANY"))
        nest_ok &= (a <= b_ <= c_)
    gate("G4", "the resolution rules are NESTED on every script (R_CONST c R_LADDER c R_ANY)",
         float(nest_ok), nest_ok)

    # R_UNION also reads the SIBLING PROSE of the unit's own .md family
    sibling_L = {}
    for src_name, grp in C.groupby("src"):
        if src_name in ("LEADERBOARD", "CHANGELOG"):
            continue
        vals = sorted({v for t in grp._txt for v in prose_L_of(t)})
        sibling_L[src_name] = vals
    doc_L = {}
    for nm in scripts:
        head = byname[nm].read_text(errors="ignore")
        d = ast.get_docstring(ast.parse(head)) if head.strip().startswith(('"""', "'''", "#!")) \
            else None
        try:
            d = ast.get_docstring(ast.parse(head))
        except SyntaxError:
            d = None
        doc_L[nm] = prose_L_of(d or "")

    rows = []
    UNIT = {}
    for cs in CLAIMSETS:
        idx = POP[cs].index
        for rule in RULES:
            kinds, vals_all = [], []
            for i in idx:
                nm = AT.loc[i, "script"]
                if not isinstance(nm, str):
                    kinds.append("NO_SCRIPT")
                    continue
                if rule == "R_UNION":
                    k, v = SREC[nm]["R_ANY"]
                    v = list(v) + sibling_L.get(C.loc[i, "src"], []) + doc_L.get(nm, [])
                    v = sorted(set(v))
                    k = ("LADDER" if len(v) > 1 else "PINNED") if v else "SILENT"
                else:
                    k, v = SREC[nm][rule]
                kinds.append(k)
                if k != "SILENT":
                    vals_all += list(v)
            ks = pd.Series(kinds)
            rec_n = int((ks.isin(["PINNED", "LADDER"])).sum())
            rows.append(dict(claim_set=cs, rule=rule, units=len(idx),
                             NO_SCRIPT=int((ks == "NO_SCRIPT").sum()),
                             SILENT=int((ks == "SILENT").sum()),
                             PINNED=int((ks == "PINNED").sum()),
                             LADDER=int((ks == "LADDER").sum()),
                             recoverable=rec_n, share=rec_n / len(idx) if len(idx) else np.nan,
                             modal_L=(pd.Series(vals_all).mode().iloc[0]
                                      if vals_all else np.nan),
                             share_L63=(float(np.mean(np.asarray(vals_all) == L_HEAD))
                                        if vals_all else np.nan)))
            UNIT[(cs, rule)] = ks.values
    RC = pd.DataFrame(rows)
    RC.to_csv(f"{OUT}.recovery.csv", index=False)
    P("")
    P("  ALL 12 CELLS.  NO_SCRIPT = no committed emitter found; SILENT = script found, no L in")
    P("  code; PINNED = the script states one L; LADDER = the script walks a set of them.")
    P("")
    P("  claim set    rule        units  NO_SCRIPT  SILENT  PINNED  LADDER  RECOVERABLE  share"
      "   modal L  share@63")
    for _, r in RC.iterrows():
        ml = "-" if not np.isfinite(r.modal_L) else f"{int(r.modal_L)}"
        s63 = "-" if not np.isfinite(r.share_L63) else f"{r.share_L63:.4f}"
        P(f"  {r.claim_set:12s} {r.rule:10s} {int(r.units):6d} {int(r.NO_SCRIPT):10d} "
          f"{int(r.SILENT):7d} {int(r.PINNED):7d} {int(r.LADDER):7d} {int(r.recoverable):12d} "
          f"{r.share:.4f}  {ml:>7s}  {s63:>8s}")
    head = RC[(RC.claim_set == CS_HEAD) & (RC.rule == R_HEAD)].iloc[0]
    P("")
    P(f"  HEADLINE ({CS_HEAD} x {R_HEAD}): {int(head.recoverable)} of {int(head.units)} "
      f"= {head.share:.4f} of the population carry a recoverable L IN CODE.")
    H_LADDER = int(head.LADDER) > int(head.PINNED)
    pinrow = RC[(RC.claim_set == CS_HEAD) & (RC.rule == "R_CONST")].iloc[0]
    H_HEAD63 = bool(np.isfinite(pinrow.share_L63)) and float(pinrow.share_L63) >= 0.50 \
        and (np.isfinite(pinrow.modal_L) and int(pinrow.modal_L) == L_HEAD)
    H_EDIT = int(head.recoverable) > (int(head.units) - int(head.recoverable))
    OUTCOME_A = float(head.share) >= 0.50
    OUTCOME_B = float(head.share) < 0.25
    OUTCOME_C = int(head.NO_SCRIPT) > int(head.SILENT)

    P("")
    P("  (C2) THE QUESTION BEHIND THE QUESTION: DID THE SILENT SCRIPTS EVER DRAW A BLOCK?")
    P("       1243's RESAMPTOK binds any unit saying 'percentile' or 'draws'.  A unit can")
    P("       therefore be counted non-conforming although the CODE that produced it never")
    P("       ran a block resample — and then there is no L it lost and nothing to re-run.")
    c2 = []
    for cs in CLAIMSETS:
        idx = list(POP[cs].index)
        ks = dict(zip(idx, UNIT[(cs, R_HEAD)]))
        sil = [i for i, k in ks.items() if k == "SILENT"]
        blk = sum(1 for i in sil if SBLK.get(AT.loc[i, "script"], False))
        c2.append(dict(claim_set=cs, silent=len(sil), silent_with_block=blk,
                       silent_no_block=len(sil) - blk,
                       share_no_block=(len(sil) - blk) / len(sil) if sil else np.nan))
    C2 = pd.DataFrame(c2)
    C2.to_csv(f"{OUT}.silent.csv", index=False)
    P("")
    P("       claim set     SILENT   script DOES draw blocks   script NEVER draws a block   share")
    for _, r in C2.iterrows():
        P(f"       {r.claim_set:12s} {int(r.silent):7d} {int(r.silent_with_block):24d} "
          f"{int(r.silent_no_block):28d}   {r.share_no_block:.4f}")
    c2h = C2[C2.claim_set == CS_HEAD].iloc[0]
    H_SCOPE = float(c2h.share_no_block) >= 0.50
    P("")
    P(f"       So of the {int(head.units)} units 1243 called unrecoverable, "
      f"{int(c2h.silent_no_block)} resolve to a script that NEVER")
    P("       draws a block at all.  Those are not verdicts missing an L; they are units the")
    P("       clause's own scope should never have bound.")

    # ---------------------------------------------------------------- ARM D: the bill
    P("")
    P("=" * 112)
    P("ARM D — THE BILL: WHAT A RE-RUN OF THE REST COSTS IN DRAWS")
    P("=" * 112)
    P("")
    P("  An EDIT repairs a unit whose script carries an L (stamp the committed sentence, 0")
    P("  draws).  A RE-RUN is owed by every unit whose script is SILENT or missing.  Each")
    P("  re-run is billed at the EMITTING SCRIPT'S OWN B where the code names one, else the")
    P(f"  record's frozen B = {BDRAWS}, times the rungs the clause form requires.  L = T is")
    P("  free (one legal block start; 1247's arithmetic, gate G7).")
    # calibrate seconds per (draw x T) on this tape
    rngc = np.random.default_rng(seed_of("calib"))
    Rc = rngc.standard_normal((T_IS_REF, 9)) * 0.01
    t0 = time.time()
    _ = pboot_argmax(Rc, "CH_ISSHARPE", L_HEAD, seed_of("calib2"), B=400, chunk=100)
    sec_per_draw = (time.time() - t0) / 400.0
    P(f"  MEASURED on this machine, this tape: {sec_per_draw*1e3:.4f} ms per draw at T = "
      f"{T_IS_REF}, 9 rungs (400 draws timed).")
    brows = []
    for cs in CLAIMSETS:
        idx = list(POP[cs].index)
        for rule in RULES:
            ks = UNIT[(cs, rule)]
            need = [i for i, k in zip(idx, ks) if k in ("SILENT", "NO_SCRIPT")]
            need_blk = [i for i in need
                        if SBLK.get(AT.loc[i, "script"], True)]
            Bs = []
            for i in need:
                nm = AT.loc[i, "script"]
                Bs.append(SB[nm][0] if isinstance(nm, str) else BDRAWS)
            Bs = np.asarray(Bs, float) if Bs else np.zeros(0)
            Bb = np.asarray([SB[AT.loc[i, "script"]][0]
                             if isinstance(AT.loc[i, "script"], str) else BDRAWS
                             for i in need_blk], float) if need_blk else np.zeros(0)
            for form in FORMS:
                mult = draws_per_verdict(form, 1)
                tot = float(Bs.sum() * mult)
                totb = float(Bb.sum() * mult)
                brows.append(dict(claim_set=cs, rule=rule, form=form, rerun_units=len(need),
                                  edit_units=len(idx) - len(need),
                                  rerun_units_inscope=len(need_blk),
                                  rungs_paid=mult, mean_B=float(Bs.mean()) if len(Bs) else 0.0,
                                  draws=tot, hours=tot * sec_per_draw / 3600.0,
                                  draws_inscope=totb,
                                  hours_inscope=totb * sec_per_draw / 3600.0))
    BL = pd.DataFrame(brows)
    BL.to_csv(f"{OUT}.bill.csv", index=False)
    P("")
    P("  claim set    rule        form           re-runs   edits   rungs   mean B      "
      "DRAWS          hours   IN-SCOPE re-runs        DRAWS")
    for _, r in BL[BL.claim_set == CS_HEAD].iterrows():
        P(f"  {r.claim_set:12s} {r.rule:10s} {r.form:12s} {int(r.rerun_units):9d} "
          f"{int(r.edit_units):7d} {int(r.rungs_paid):7d} {r.mean_B:9.1f} "
          f"{r.draws:14,.0f} {r.hours:14.2f} {int(r.rerun_units_inscope):18d} "
          f"{r.draws_inscope:12,.0f}")
    P("")
    P("  (the other 8 cells are in .bill.csv; the same table at CS_BLOCK and CS_ALL)")
    b_head = BL[(BL.claim_set == CS_HEAD) & (BL.rule == R_HEAD)
                & (BL.form == "CF_IDENTITY")].iloc[0]
    b_point = BL[(BL.claim_set == CS_HEAD) & (BL.rule == R_HEAD)
                 & (BL.form == "CF_POINT")].iloc[0]
    b_l11 = BL[(BL.claim_set == CS_HEAD) & (BL.rule == R_HEAD)
               & (BL.form == "CF_LADDER11")].iloc[0]
    gate("G7", "the identity rung is FREE: CF_IDENTITY's bill equals CF_POINT's",
         abs(b_head.draws - b_point.draws), abs(b_head.draws - b_point.draws) < 1e-9)
    mono = bool(BL.groupby(["claim_set", "rule"]).apply(
        lambda g: g.set_index("form").draws.reindex(FORMS).is_monotonic_increasing,
        include_groups=False).all())
    gate("G10", "the draws bill is MONOTONE in the rungs a clause form requires", float(mono),
         mono)
    P("")
    P(f"  AGAINST 1247's COMMITTED BILL of {A1247_RERUNS:,} re-runs against this very")
    P(f"  population: this run bills {int(b_head.rerun_units):,} re-runs and "
      f"{int(b_head.edit_units):,} EDITS at 0 draws.")

    # ---------------------------------------------------------------- ARM E: capital
    P("")
    P("=" * 112)
    P("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    P("=" * 112)
    px = {"U56": load_universe(), "B136": load_universe(broad=True)}
    pxs = load_universe(small=True)
    mv = pxs.pct_change().abs().max()
    drop = [c for c in pxs.columns if c != "SPY" and not (mv[c] < 1.0)]
    px["SMALL"] = pxs.drop(columns=drop)
    pans = {n: Panel(n, px[n]) for n in PANELS}
    vintage = str(px["U56"].index[-1].date())
    P("")
    P(f"  CACHE VINTAGE: {vintage}.  PANELS: U56 {len(px['U56'].columns)-1} names; "
      f"B136 {len(px['B136'].columns)-1}; SMALL {len(px['SMALL'].columns)-1} investable "
      f"({len(drop)} dropped for max_1d_move >= 1.0).")
    cache, BOOKS = {}, {}
    for pn in PANELS:
        for an in ANCHORS:
            for lad in LADNAMES:
                BOOKS[(pn, an, lad)] = ladder_books(pans[pn], an, lad, cache)
    a = ANCHORS["A"]
    r0 = cache[("U56", a["N"], a["H"], a["GROSS"], a["CADENCE"])]
    c0, s0, d0 = fmet(r0[pans["U56"].warm])
    dv = max(abs(c0 - A1101_TRIPLE[0]), abs(s0 - A1101_TRIPLE[1]), abs(d0 - A1101_TRIPLE[2]))
    P(f"  1101's committed U56 anchor triple {A1101_TRIPLE[0]:.6f} / {A1101_TRIPLE[1]:.6f} / "
      f"{A1101_TRIPLE[2]:.6f}; this run {c0:.6f} / {s0:.6f} / {d0:.6f}")
    gate("G6", "1101's committed U56 anchor triple replays within 1264's vintage drift", dv,
         dv < 6e-3)
    lb = backtest(px["U56"], rules_v2_weights(px["U56"]), cost_bps=COST,
                  freq="W")["returns"].values
    lmdd = fmet(lb[WARMUP:])[2]
    gate("G8", "live RULES v2 U56 MaxDD == committed -12.05%", abs(lmdd - LIVE_MAXDD_COMMITTED),
         abs(lmdd - LIVE_MAXDD_COMMITTED) < 5e-4)
    DEC = [(pn, an, lad, ch) for pn in PANELS for an in ANCHORS
           for lad in LADNAMES for ch in CHOOSERS]
    gate("G11", "decision count == 1208/1243/1247's 72", float(len(DEC)), len(DEC) == A1208_NDEC)
    T_IS = {pn: int(pans[pn].ins.sum()) for pn in PANELS}
    oos_clean = all(not bool((pans[pn].ins & pans[pn].oos).any()) for pn in PANELS)
    gate("G12", "rule 8: the OOS window shares NO row with the IS window", float(oos_clean),
         oos_clean)

    P("")
    P("  (E1) every rung book, full sample and 2017-2026, 4a vs live RULES v2, 4b vs SPY.")
    BM = {}
    for pn in PANELS:
        pan = pans[pn]
        BM[(pn, "SPY")] = blocks_m(pan.spy, pan.warm, pan.ins, pan.oos)
        lbv = backtest(px[pn], rules_v2_weights(px[pn]), cost_bps=COST, freq="W")["returns"].values
        BM[(pn, "LIVE")] = blocks_m(lbv, pan.warm, pan.ins, pan.oos)
    brows2 = []
    for (pn, an, lad) in sorted({(x, y, z) for (x, y, z, _) in DEC}):
        pan = pans[pn]
        for rung, r in BOOKS[(pn, an, lad)].items():
            m = blocks_m(r, pan.warm, pan.ins, pan.oos)
            brows2.append(dict(panel=pn, anchor=an, ladder=lad, rung=str(rung), **m,
                               KEEP_4a=all(legs_4a(m, BM[(pn, "LIVE")]).values()),
                               KEEP_4b=all(legs_4b(m, BM[(pn, "SPY")]).values()),
                               KEEP_4b_OOS=all(legs_4b_oos(m, BM[(pn, "SPY")]).values())))
    BK = pd.DataFrame(brows2).drop_duplicates(subset=["panel", "anchor", "ladder", "rung"])
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
    P("  (E2) THE CITE-MAP.  A decision (panel, anchor, ladder, chooser) is R-ADMITTED when at")
    P("       least one committed unit citing its PANEL and its LADDER has an L recoverable")
    P("       under rule R.  Admitted -> act on the decision's IS argmax; otherwise hold the")
    P("       anchor rung (do nothing).  Picks are made on the IS window ONLY (rule 8).")
    cited = {}
    for (pn, an, lad, ch) in DEC:
        key = (pn, lad)
        if key in cited:
            continue
        m = C._txt.map(lambda t: bool(PANTOK[pn].search(t)) and bool(LADTOK[lad].search(t)))
        cited[key] = set(C.index[m.values])
    P("")
    P("       units citing each (panel, ladder) in the WHOLE census:")
    for pn in PANELS:
        P("       " + f"{pn:6s} " + "  ".join(f"{lad} {len(cited[(pn,lad)]):5d}"
                                              for lad in LADNAMES))
    pickmap, anchmap = {}, {}
    for (pn, an, lad, ch) in DEC:
        pan = pans[pn]
        rungs = LADDERS[lad]
        vals = [is_stat(BOOKS[(pn, an, lad)][r], pan.ins, ch) for r in rungs]
        obs = rungs[int(np.nanargmax(np.where(np.isfinite(vals), vals, -np.inf)))]
        pickmap[(pn, an, lad, ch)] = blocks_m(BOOKS[(pn, an, lad)][obs],
                                              pan.warm, pan.ins, pan.oos)
        anchmap[(pn, an, lad, ch)] = blocks_m(BOOKS[(pn, an, lad)][ANCHORS[an][lad]],
                                              pan.warm, pan.ins, pan.oos)
    P("")
    P(f"  (E3) 1208's resolution at the record's frozen L = {L_HEAD}, B = {BDRAWS} "
      f"(the point rule's own reference):")
    res63 = {}
    for (pn, an, lad) in sorted({(x, y, z) for (x, y, z, _) in DEC}):
        pan = pans[pn]
        rungs = LADDERS[lad]
        R = np.column_stack([BOOKS[(pn, an, lad)][r][pan.ins] for r in rungs])
        for ch in CHOOSERS:
            p = pboot_argmax(R, ch, L_HEAD, seed_of(pn, an, lad, ch, L_HEAD))
            res63[(pn, an, lad, ch)] = bool(p.max() >= BAR_HI)
    n_res = sum(res63.values())
    P(f"       RESOLVED at L = {L_HEAD}: {n_res} of {len(DEC)} "
      f"({n_res/len(DEC):.4f}).")

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

    P("")
    P("       (E2b) SHARE of each (panel, ladder)'s citing units that are RECOVERABLE under the")
    P(f"             headline rule {R_HEAD} on the headline claim set {CS_HEAD}.  This is the")
    P("             substance the ANY-quantifier admission rule throws away.")
    idxh = list(POP[CS_HEAD].index)
    ksh = dict(zip(idxh, UNIT[(CS_HEAD, R_HEAD)]))
    goodh = {i for i, k in ksh.items() if k in ("PINNED", "LADDER")}
    sh_rows = []
    for pn in PANELS:
        line = []
        for lad in LADNAMES:
            cc = cited[(pn, lad)] & set(idxh)
            sh = len(cc & goodh) / len(cc) if cc else np.nan
            sh_rows.append(dict(panel=pn, ladder=lad, cited_in_pop=len(cc),
                                recoverable=len(cc & goodh), share=sh))
            line.append(f"{lad} {len(cc & goodh):4d}/{len(cc):4d} = {sh:.3f}")
        P(f"             {pn:6s} " + "   ".join(line))
    pd.DataFrame(sh_rows).to_csv(f"{OUT}.citemap.csv", index=False)

    mixed = {}
    wrows = [dict(claim_set="REF", rule="REF_ACT_ON_ALL", n_admitted=len(DEC),
                  **summarise(list(DEC), pickmap)),
             dict(claim_set="REF", rule="REF_DO_NOTHING", n_admitted=0,
                  **summarise(list(DEC), anchmap)),
             dict(claim_set="REF", rule="REF_POINT_L63", n_admitted=n_res,
                  **summarise([k for k in DEC if res63[k]], pickmap))]
    for cs in CLAIMSETS:
        idx = list(POP[cs].index)
        for rule in RULES:
            ks = dict(zip(idx, UNIT[(cs, rule)]))
            good = {i for i, k in ks.items() if k in ("PINNED", "LADDER")}
            adm = []
            for k in DEC:
                pn, an, lad, ch = k
                adm.append(bool(cited[(pn, lad)] & good))
            keys = [k for k, ok in zip(DEC, adm) if ok]
            mixed[(cs, rule)] = {k: (pickmap[k] if ok else anchmap[k])
                                 for k, ok in zip(DEC, adm)}
            del keys
            wrows.append(dict(claim_set=cs, rule=rule, n_admitted=int(sum(adm)),
                              **summarise(list(DEC), mixed[(cs, rule)])))
    # QUANTIFIER CONTROL — reported, never a third dial: NO BOOK IS SELECTED ON IT.  The
    # ANY quantifier above is saturated (thousands of citing units per cell), so the control
    # shows what a stricter admission rule would have done at the SAME headline cell.
    qrows = []
    for q, fn in [("Q_ANY", lambda a, b: a >= 1),
                  ("Q_MAJORITY", lambda a, b: b and a > b / 2),
                  ("Q_ALL", lambda a, b: b and a == b)]:
        adm = []
        for k in DEC:
            pn, an, lad, ch = k
            cc = cited[(pn, lad)] & set(idxh)
            adm.append(bool(fn(len(cc & goodh), len(cc))))
        mm = {k: (pickmap[k] if ok else anchmap[k]) for k, ok in zip(DEC, adm)}
        qrows.append(dict(claim_set="CONTROL", rule=q, n_admitted=int(sum(adm)),
                          **summarise(list(DEC), mm)))
    wrows += qrows

    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    P("")
    P("       claim set    rule              admitted   mean OOS Sharpe   mean OOS CAGR   "
      "mean OOS MaxDD   4a / 4b / 4b_OOS")
    for _, r in W8.iterrows():
        P(f"       {r.claim_set:12s} {r.rule:16s} {int(r.n_admitted):8d}   "
          f"{r.mean_OOS_Sharpe:15.4f}   {r.mean_OOS_CAGR:13.4f}   {r.mean_OOS_MaxDD:14.4f}   "
          f"{int(r.KEEP_4a)} / {int(r.KEEP_4b)} / {int(r.KEEP_4b_OOS)}")
    ref_all = W8[W8.rule == "REF_ACT_ON_ALL"].iloc[0]
    ref_none = W8[W8.rule == "REF_DO_NOTHING"].iloc[0]
    cells = W8[~W8.claim_set.isin(["REF", "CONTROL"])]
    worst = float(np.nanmax(np.abs(cells.mean_OOS_Sharpe
                                   - ref_none.mean_OOS_Sharpe).values))
    worst2 = float(np.nanmax(np.abs(cells.mean_OOS_Sharpe
                                    - ref_all.mean_OOS_Sharpe).values))
    H_CAPITAL = (worst <= 0.02) and (worst2 <= 0.02)
    best = cells.sort_values("mean_OOS_Sharpe", ascending=False).iloc[0]
    P("")
    P(f"       BEST CELL ON OOS SHARPE: {best.claim_set} x {best.rule} = "
      f"{best.mean_OOS_Sharpe:.4f} on {int(best.n_admitted)} admitted decisions, against")
    P(f"       ACT ON ALL {ref_all.mean_OOS_Sharpe:.4f} and DOING NOTHING "
      f"{ref_none.mean_OOS_Sharpe:.4f}  "
      f"({best.mean_OOS_Sharpe - ref_none.mean_OOS_Sharpe:+.4f} vs do-nothing).")

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 112)
    P("HYPOTHESES, SCORED")
    P("=" * 112)
    HY = [("H_REACH", ">= 0.90 of the claim set resolves to a committed script",
           H_REACH, f"{float(ah.reach):.4f}"),
          ("H_LADDER", "among RESOLVED units, LADDER scripts outnumber PINNED ones",
           H_LADDER, f"{int(head.LADDER)} vs {int(head.PINNED)}"),
          ("H_STEM", "A_STEM alone reaches more units than A_COL alone",
           H_STEM, f"{int(ah.alone_A_STEM)} vs {int(ah.alone_A_COL)}"),
          ("H_HEAD63", "the modal pinned L is the frozen 63, at share >= 0.50",
           H_HEAD63, f"R_CONST modal {pinrow.modal_L:.0f}, share {pinrow.share_L63:.4f} "
           f"(R_LADDER pooled over rungs: {head.share_L63:.4f})"),
          ("H_EDIT", "units repairable by EDIT outnumber units owing a RE-RUN",
           H_EDIT, f"{int(head.recoverable)} vs {int(head.units)-int(head.recoverable)}"),
          ("H_SCOPE", "a MAJORITY of the SILENT units resolve to a script that never draws "
           "a block", H_SCOPE, f"{int(c2h.silent_no_block)} of {int(c2h.silent)} = "
           f"{c2h.share_no_block:.4f}"),
          ("H_CAPITAL", "no cell moves mean OOS Sharpe by more than 0.02 vs BOTH references",
           H_CAPITAL, f"worst |d| {max(worst, worst2):.4f}")]
    HYD = pd.DataFrame([dict(hypothesis=h, statement=s, held=bool(v), value=x)
                        for h, s, v, x in HY])
    HYD.to_csv(f"{OUT}.hypotheses.csv", index=False)
    for h, s, v, x in HY:
        P(f"  {h:<11s} {'HELD ' if v else 'FAILED'}  {s:<66s} {x}")

    G = pd.DataFrame(GATES)
    G.to_csv(f"{OUT}.gates.csv", index=False)
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    P("")
    oc = "(A) THE SCRIPT KEPT IT" if OUTCOME_A else (
        "(B) THE SCRIPT LOST IT TOO" if OUTCOME_B else "(neither A nor B: the middle band)")
    P(f"  PRE-DECLARED OUTCOME: {oc}"
      + ("  +  (C) ATTRIBUTION IS THE BINDING CONSTRAINT" if OUTCOME_C else ""))
    P(f"  ANSWER TO THE QUEUE'S QUESTION: {int(head.recoverable)} of {int(head.units)} "
      f"({head.share:.4f}) of 1243's unrecoverable resample verdicts carry a recoverable L")
    P(f"  in the code that produced them.  The rest — {int(head.units)-int(head.recoverable)} "
      f"units — owe a re-run costing {b_point.draws:,.0f} draws at CF_POINT "
      f"({b_point.hours:.1f} h)")
    P(f"  and {b_l11.draws:,.0f} at CF_LADDER11 ({b_l11.hours:.1f} h) on this machine.")
    P(f"  OF THOSE {int(b_point.rerun_units)} RE-RUNS, only "
      f"{int(b_point.rerun_units_inscope)} resolve to a script that draws a block at all; the")
    P(f"  rest were never in the clause's business.  The in-scope bill is "
      f"{b_point.draws_inscope:,.0f} draws at CF_POINT and "
      f"{b_l11.draws_inscope:,.0f} at CF_LADDER11.")
    P(f"  GATES {int(G.pass_.sum())} of {len(G)}.  Elapsed {time.time()-t_start:.1f}s.")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
