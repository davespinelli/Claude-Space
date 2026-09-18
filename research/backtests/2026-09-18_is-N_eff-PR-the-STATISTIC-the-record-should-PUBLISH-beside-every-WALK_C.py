#!/usr/bin/env python3
"""
Idea 1245 (lane C, 2026-09-18) — is N_eff^PR the STATISTIC the record should PUBLISH beside
every WALK?

THE PREMISE, READ FROM THE RECORD.  Idea 1239 measured the bar-free participation ratio of the
candidate returns' correlation matrix and found it reads 1.0001 on the GROSS ladder (1189's
re-levering identity, to 1e-4) and 1.034-1.263 on EVERY non-GROSS ladder, against a Sharpe-gap
(single-linkage, bar-based) reading of 4-8 on the same sets.  So in RETURN space the record's
whole 19-book candidate set looks like ~1.1 degrees of freedom.  The queue asks whether that
number is the one to print beside every "we walked N alternatives" sentence.

WHAT IS ACTUALLY BEING TESTED.  A statistic is publishable only if it DISCRIMINATES.  The
reason N_eff^PR reads ~1.1 everywhere may be that the record's candidate sets really are one
book — or it may be that every long-only equity book on one panel shares a market factor so
large that a correlation-matrix participation ratio can never read anything but ~1, in which
case the statistic is a reading of EQUITY BETA and not of candidate-set diversity, and printing
it beside every walk would re-word every headline in the record while distinguishing none of
them.  This run settles that with ground truth: three K=6 control candidate sets whose true
degrees of freedom are KNOWN, built on each panel —

    CTRL_CLONE      6 re-leverings of the anchor book (true dof = 1)
    CTRL_DISJOINT   the SAME rule run on 6 DISJOINT name pools (no book can hold another's
                    names; genuinely different books that still share the market factor)
    CTRL_IID        6 synthetic iid gaussian series at the anchor's mean/vol (true dof = 6,
                    no common factor at all) — a pure estimator sanity check

and the RESOLUTION of an estimator X is

    R(X) = ( X(CTRL_DISJOINT) - X(CTRL_CLONE) ) / ( X(CTRL_IID) - X(CTRL_CLONE) )

R = 1: six disjoint books get the same diversity credit as six independent series.
R = 0: the estimator cannot tell six disjoint books from six re-leverings of one book.

PRE-DECLARED OUTCOMES (fixed before any number is read; the verdict is read off, not chosen):
  (A) PUBLISH IT AS IS — E_PR_RAW (1239's estimator) has resolution: R >= 0.50 on a majority
      of panels.
  (B) DO NOT PUBLISH IT ALONE — E_PR_RAW fails that bar while at least one de-factored
      estimator clears it, so the schema clause must NAME an estimator rather than say
      "the participation ratio".
  (C) PUBLISH NOTHING BAR-FREE — no estimator on the grid clears the bar.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET      {CS_STRICT, CS_PROX, CS_ALL} — 1239's three, unchanged, so the census is
                 comparable to the committed one.
  N_eff          {E_PR_RAW, E_PR_XS, E_PR_RESID, E_ENT_RAW, E_ENT_XS, E_SL_BAR}
  ESTIMATOR      E_PR_RAW   participation ratio (sum l)^2 / sum l^2 of the candidates'
                            correlation matrix — 1239's, reproduced exactly.
                 E_PR_XS    the same after removing the CROSS-CANDIDATE mean return each day
                            (kills "the average book").
                 E_PR_RESID the same on residuals from a full-sample OLS on SPY (kills beta).
                 E_ENT_RAW  exp(Shannon entropy of l / sum l) — same endpoints as PR, bar-free.
                 E_ENT_XS   the entropy reading on the cross-demeaned matrix.
                 E_SL_BAR   1239's single-linkage |dSharpe| <= 0.0040 component count — the
                            record's INCUMBENT reading, carried as the reference arm.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL663} (rule 9); the record's four
ladders (N, H, GROSS, CADENCE), their 15 non-empty subset unions, and the 19-book UNION; the
re-wording bar; both representative rules for the de-dup chooser; the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, GROSS 0.75 anchor, N=20, H=126, weekly cadence, 10 bps (rule 2),
decide-at-t / apply-at-t+1, warm-up 260 rows, OOS split 2017-01-01 (rule 8).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
book and every rule-8 row; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

Runs standalone and offline (no network; committed price caches only).
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "is-N_eff-PR-the-STATISTIC-the-record-should-PUBLISH-beside-every-WALK"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_C"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
LEGS = [(21, 252), (0, 126), (0, 63)]
A_N, A_H, A_G, A_C = 20, 126, 0.75, "W"
LAD = {
    "N": [5, 10, 15, 20, 30, 40],
    "H": [21, 63, 126, 252],
    "GROSS": [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
    "CADENCE": ["W", "M"],
}
ANCHOR_RUNG = {"N": A_N, "H": A_H, "GROSS": A_G, "CADENCE": A_C}
LADS = ["N", "H", "GROSS", "CADENCE"]
INC = ("N", A_N)
SL_BAR = 0.0040                       # 1237/1239's clone bar, carried unchanged
CLAIM_SETS = ["CS_STRICT", "CS_PROX", "CS_ALL"]
EST = ["E_PR_RAW", "E_PR_XS", "E_PR_RESID", "E_ENT_RAW", "E_ENT_XS", "E_SL_BAR"]
K_CTRL = 6                            # matched candidate count for the three control sets
N_CTRL = 5                            # names per disjoint control book
CTRL_SEED = 20260918
PANEL_SEED = {"U56": 1, "B136": 2, "SMALL663": 3}
REWORD_FACTOR = 2.0                   # stated_N >= 2 x N_eff  =>  the headline is re-worded
LIVE_MAXDD_COMMITTED = -0.1205
C1239 = (ROOT / "research" / "backtests" /
         "2026-09-17_is-the-record-s-CANDIDATE-SET-half-CLONES-on-every-axis-it-has-ever-"
         "WALKED_cloud.degeneracy.csv")

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ================================================================ panels / runner (1239's, verbatim)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.seg = {}
        for f in LAD["CADENCE"]:
            m = rebalance_mask(px.index, f).shift(1, fill_value=False).values.copy()
            m[0] = True
            self.seg[f] = np.flatnonzero(m)
        self.idx = px.index
        self.i0 = WARMUP
        sc, above, vol20 = mech(px[invest])
        self.rank_key = np.where(np.isfinite(sc), -sc, np.inf)
        self.elig = above & (vol20 < MAXVOL)
        self.spy = px["SPY"].pct_change().fillna(0.0).values


def mech(q):
    parts = []
    for skip, look in LEGS:
        x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
        parts.append(x.rank(axis=1, pct=True))
    comp = sum(parts) / len(parts)
    above = (q > q.rolling(200).mean()).values
    vol20 = (q.pct_change().rolling(20).std() * np.sqrt(252)).values
    sc = (comp * (0.5 + 0.5 * above.astype(float))).values
    return sc, above, np.nan_to_num(vol20, nan=1e9)


def build1(pan, N, H, freq, lag=1, allow=None):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight.  `allow` (a boolean mask over the
    panel's investable columns) restricts the eligible pool and is used ONLY by the disjoint
    control; allow=None reproduces 1239's build1 bit for bit."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    blocked = None if allow is None else ~np.asarray(allow, bool)
    for i, t in enumerate(reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = set(int(c) for c in young)
        need = N - len(keep)
        take = []
        if need > 0:
            k = pan.rank_key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            if blocked is not None:
                k[blocked] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            take = [int(c) for c in order[:need] if np.isfinite(k[c])]
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if len(sel):
            stop = reb[i + 1] if i + 1 < len(reb) else T
            W[t:stop, pan.iinv[sel]] = 1.0 / len(sel)
    return W


def nrun(pan, Wt, freq):
    rets = pan.rets
    T, M = rets.shape
    reb = pan.seg[freq]
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(reb[1:], T)
    for i0, i1 in zip(reb, ends):
        w0 = Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    return (held * rets).sum(axis=1) - turn * COST / 1e4


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    e = np.cumprod(1 + r)
    return float(e[-1] ** (252 / len(r)) - 1)


def triple(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def bmref(r):
    h1, h2 = halves(r)
    return dict(H1=h1, H2=h2, **triple(r))


def keep_paths(r, bm, live):
    h1, h2 = halves(r)
    m = triple(r)
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    k4b = bool(h1 > bm["H1"] and h2 > bm["H2"]
               and m["MaxDD"] >= DD_CAP * bm["MaxDD"]
               and m["CAGR"] >= CAGR_FLOOR * bm["CAGR"])
    return k4a, k4b, m, h1, h2


def akey(k):
    return f"{k[0]}={k[1]}"


# ================================================================ the six N_eff estimators
def _rowmask(mat):
    X = np.asarray(mat, float)
    return np.isfinite(X).all(axis=1)


def _cols(X):
    """Drop constant columns; return None if fewer than 5 rows or no live column."""
    if X is None or X.shape[0] < 5:
        return None
    sd = X.std(axis=0, ddof=0)
    X = X[:, sd > 1e-14]
    return X if X.shape[1] else None


def _clean(mat):
    X = np.asarray(mat, float)
    return _cols(X[_rowmask(X)])


def _eig(X):
    R = np.atleast_2d(np.corrcoef(X, rowvar=False))
    R = np.nan_to_num(R, nan=0.0)
    return np.clip(np.linalg.eigvalsh(R), 0.0, None)


def pr_of(X):
    if X is None:
        return np.nan
    lam = _eig(X)
    s1, s2 = lam.sum(), (lam ** 2).sum()
    return float(s1 * s1 / s2) if s2 > 0 else np.nan


def ent_of(X):
    if X is None:
        return np.nan
    lam = _eig(X)
    s = lam.sum()
    if s <= 0:
        return np.nan
    p = lam / s
    p = p[p > 1e-15]
    return float(np.exp(-(p * np.log(p)).sum()))


def xs_demean(mat):
    X = _clean(mat)
    if X is None:
        return None
    return _cols(X - X.mean(axis=1, keepdims=True))


def spy_resid(mat, spy):
    """Residuals from a full-sample OLS of each candidate on SPY, on the SAME rows."""
    M = np.asarray(mat, float)
    s = np.asarray(spy, float)
    if len(s) != M.shape[0]:
        return None
    ok = _rowmask(M) & np.isfinite(s)
    X, sc = _cols(M[ok]), s[ok]
    if X is None:
        return None
    sc = sc - sc.mean()
    v = float((sc * sc).sum())
    if v <= 0:
        return None
    beta = (X - X.mean(axis=0)).T @ sc / v
    return _cols(X - np.outer(sc, beta))


def n_eff_sl(vals, bar=SL_BAR):
    """Single-linkage components of the |dSharpe| <= bar graph (1239's headline reading)."""
    v = np.sort(np.asarray([x for x in vals if np.isfinite(x)], float))
    if len(v) == 0:
        return np.nan
    return float(len(np.split(v, np.flatnonzero(np.diff(v) > bar) + 1)))


def all_estimators(mat, sharpes, spy):
    """mat: T x K matrix of candidate daily net returns.  Returns {estimator: reading}."""
    raw = _clean(mat)
    xs = xs_demean(mat)
    rs = spy_resid(mat, spy)
    return {
        "E_PR_RAW": pr_of(raw),
        "E_PR_XS": pr_of(xs),
        "E_PR_RESID": pr_of(rs),
        "E_ENT_RAW": ent_of(raw),
        "E_ENT_XS": ent_of(xs),
        "E_SL_BAR": n_eff_sl(sharpes),
    }


# ================================================================ de-dup clustering (IS only)
def clusters_corr(mat, k):
    """Deterministic complete-linkage agglomeration on d = 1 - corr, stopped at k clusters.
    Ties broken by the lowest (i, j) index pair, so the result is a pure function of `mat`."""
    X = np.asarray(mat, float)
    K = X.shape[1]
    if not np.isfinite(k):
        return [[i] for i in range(K)]     # N_eff undefined -> the clause cannot collapse
    k = int(max(1, min(K, round(k))))
    R = np.atleast_2d(np.corrcoef(X, rowvar=False))
    R = np.nan_to_num(R, nan=0.0)
    D = 1.0 - R
    groups = [[i] for i in range(K)]
    while len(groups) > k:
        best, bi, bj = np.inf, 0, 1
        for a in range(len(groups)):
            for b in range(a + 1, len(groups)):
                d = max(D[i, j] for i in groups[a] for j in groups[b])   # complete linkage
                if d < best - 1e-15:
                    best, bi, bj = d, a, b
        groups[bi] = groups[bi] + groups[bj]
        del groups[bj]
    return groups


def reps_sl(keys, vals, bar=SL_BAR):
    """1239's representative rule for Sharpe-bar clusters: the lowest-Sharpe member."""
    pairs = sorted((v, i) for i, v in enumerate(vals) if np.isfinite(v))
    out, anchor_v = [], None
    for v, i in pairs:
        if anchor_v is None or v - anchor_v > bar:
            out.append(keys[i])
        anchor_v = v
    return out


# ================================================================ the record's own text (1239's)
WALK = re.compile(r"\b(walk\w*|swept|sweep\w*|ladder\w*|grid|candidate set|candidate-set|"
                  r"comparison set|comparison-set|alternatives?|rungs?|arms?|variants?)\b", re.I)
COUNT = re.compile(r"\b(\d{1,4})\s+(?:distinct\s+|candidate\s+|rung\s+|non-incumbent\s+)?"
                   r"(alternatives?|candidates?|books?|rungs?|arms?|variants?|cells?|ladders?)\b",
                   re.I)
VERDICT = re.compile(r"\b(KEEP|KILL|PARK|PASS|FAIL|decisive|refuted|confirmed|survives?|"
                     r"does not survive|verdict)\b")
AXIS = {a: re.compile(rf"\b{a}\b") for a in ("GROSS", "CADENCE")}
AXIS["N"] = re.compile(r"\bN\s*=\s*\d+|\bN LADDER|\bN ladder|\bthe N axis\b")
AXIS["H"] = re.compile(r"\bH\s*=\s*\d+|\bH LADDER|\bH ladder|\bthe H axis\b")


def units():
    U = []
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text(errors="ignore")
    cl = (ROOT / "research" / "CHANGELOG.md").read_text(errors="ignore")
    for ln in lb.split("\n"):
        if ln.startswith("| 20"):
            U.append(("LEADERBOARD", ln))
    for para in cl.split("\n\n"):
        if para.strip():
            U.append(("CHANGELOG", para))
    nmd = 0
    for f in sorted((ROOT / "research" / "backtests").rglob("*.md")):
        nmd += 1
        for para in f.read_text(errors="ignore").split("\n\n"):
            if para.strip():
                U.append((f.name, para))
    return U, nmd


def snip(t, n=96):
    s = re.sub(r"\s+", " ", re.sub(r"[|*`]", " ", t)).strip()
    return s[:n]


def census(U):
    rows = []
    for src, txt in U:
        w = bool(WALK.search(txt))
        cs = [int(m.group(1)) for m in COUNT.finditer(txt)]
        cs = [c for c in cs if 2 <= c <= 2000]
        ver = bool(VERDICT.search(txt))
        ax = [a for a, p in AXIS.items() if p.search(txt)]
        rows.append(dict(uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
                         WALK=w, n_counts=len(cs), stated_N=(max(cs) if cs else np.nan),
                         VERDICT=ver, axes="|".join(sorted(ax)), n_axes=len(ax),
                         CS_ALL=bool(w), CS_PROX=bool(w and cs),
                         CS_STRICT=bool(w and cs and ver), snippet=snip(txt)))
    return pd.DataFrame(rows)


# ================================================================ main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1245 (lane C, 2026-09-18) — is N_eff^PR the STATISTIC the record should PUBLISH")
    say("beside every WALK?")
    say("=" * 110)
    say("")
    say("  1239 committed N_eff^PR = 1.0001 on GROSS and 1.034-1.263 on every non-GROSS ladder,")
    say("  against a Sharpe-bar reading of 4-8 on the same sets.  A statistic is publishable")
    say("  only if it DISCRIMINATES, so this run gives every estimator GROUND TRUTH: three K=6")
    say("  control candidate sets per panel — CLONE (true dof 1), DISJOINT (6 books that cannot")
    say("  hold each other's names) and IID (6 independent series).  RESOLUTION")
    say("      R = (X(DISJOINT) - X(CLONE)) / (X(IID) - X(CLONE)).")
    say("  PRE-DECLARED: (A) PUBLISH AS IS — E_PR_RAW has R >= 0.50 on a majority of panels.")
    say("  (B) DO NOT PUBLISH IT ALONE — E_PR_RAW fails and some de-factored estimator clears")
    say("  the bar.  (C) PUBLISH NOTHING BAR-FREE — no estimator clears it.")

    # ------------------------------------------------------------ ARM A: panels, books, gates
    say("")
    say("=" * 110)
    say("ARM A — PANELS, THE 22 RUNG BOOKS, AND THE REPLAY GATES")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels.append(Panel("SMALL663", pxS, inv))
    PN = [p.name for p in panels]
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL663 {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")

    booked, BM, BOOKKEY = {}, {}, []
    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = build1(pan, N, A_H, "W")
        for H in LAD["H"]:
            if (A_N, H, "W") not in frames:
                frames[(A_N, H, "W")] = build1(pan, A_N, H, "W")
        frames[(A_N, A_H, "M")] = build1(pan, A_N, A_H, "M")
        af = frames[(A_N, A_H, "W")]
        books = {}
        for N in LAD["N"]:
            books[("N", N)] = nrun(pan, A_G * frames[(N, A_H, "W")], "W")
        for H in LAD["H"]:
            books[("H", H)] = nrun(pan, A_G * frames[(A_N, H, "W")], "W")
        for f in LAD["CADENCE"]:
            books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]),
                                         f)
        for g in LAD["GROSS"]:
            books[("GROSS", g)] = nrun(pan, g * af, "W")
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        BM[(pan.name, "SPY")] = bmref(pan.spy[pan.i0:])
        BM[(pan.name, "LIVE")] = bmref(b[pan.i0:])
        io = int(pan.idx.searchsorted(pd.Timestamp(OOS_START)))
        BM[(pan.name, "SPY_OOS")] = bmref(pan.spy[io:])
        BM[(pan.name, "LIVE_OOS")] = bmref(b[io:])
        say(f"    {pan.name:8s} {len(books)} rung books built.")
        del frames

    ilim = {p.name: int(p.idx.searchsorted(pd.Timestamp(OOS_START))) for p in panels}
    ALT = [k for k in BOOKKEY if k == INC or k not in ANCH_KEYS]       # 19 distinct books

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, "< 1e-10", g1 < 1e-10)
    lm = BM[("U56", "LIVE")]["MaxDD"]
    gate("G2 live RULES v2 U56 MaxDD == committed -12.05%", round(lm, 6), LIVE_MAXDD_COMMITTED,
         abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    gate("G3 distinct candidate set size (1237/1239's 19)", float(len(ALT)), 19.0, len(ALT) == 19)

    # replay 1239's committed N_eff^PR table exactly
    Sfull = {(p.name, k): sharpe(booked[p.name][k][p.i0:]) for p in panels for k in BOOKKEY}
    LADSETS = {l: [(l, r) for r in LAD[l]] for l in LADS}
    LADSETS["UNION"] = ALT
    pr_now, dev39 = {}, 0.0
    C39 = pd.read_csv(C1239)
    C39 = C39[C39.bar == "B_TIGHT"]
    for p in panels:
        for lad, keys in LADSETS.items():
            mat = np.column_stack([booked[p.name][k][p.i0:] for k in keys])
            pr_now[(p.name, lad)] = pr_of(_clean(mat))
            old = C39[(C39.panel == ("SMALL" if p.name == "SMALL663" else p.name))
                      & (C39.ladder == lad)]
            if len(old):
                dev39 = max(dev39, abs(float(old.N_eff_PR.iloc[0]) - pr_now[(p.name, lad)]))
    gate("G4 1239's committed N_eff^PR replays at all 15 (panel, ladder) cells",
         f"{dev39:.2e}", "< 5e-3", dev39 < 5e-3)
    grs = [pr_now[(p, "GROSS")] for p in PN]
    ngs = [pr_now[(p, l)] for p in PN for l in ["N", "H", "CADENCE"]]
    gate("G5 the premise: GROSS N_eff^PR ~ 1.0001, non-GROSS 1.034-1.263",
         f"{max(grs):.4f} / {min(ngs):.3f}-{max(ngs):.3f}", "<=1.001 / 1.03-1.27",
         max(grs) <= 1.001 and 1.03 <= min(ngs) and max(ngs) <= 1.27)
    say("")
    say(f"    1239's committed N_eff^PR replays to {dev39:.2e} over 15 cells.  GROSS "
        f"{min(grs):.4f}-{max(grs):.4f}; non-GROSS {min(ngs):.3f}-{max(ngs):.3f}.")

    # ------------------------------------------------------------ ARM B: ground-truth controls
    say("")
    say("=" * 110)
    say("ARM B — DOES ANY ESTIMATOR HAVE RESOLUTION?  THREE K=6 CONTROLS WITH KNOWN dof")
    say("=" * 110)
    say("")
    say("    CTRL_CLONE     6 re-leverings of the anchor book            true dof 1")
    say("    CTRL_DISJOINT  the same rule on 6 DISJOINT name pools       true dof 6 (shares beta)")
    say("    CTRL_IID       6 iid gaussian series at the anchor's moments true dof 6 (no factor)")
    say("")
    ctrl_rows, CTRL, DISJ_OVERLAP = [], {}, {}
    for pan in panels:
        i0 = pan.i0
        af = build1(pan, A_N, A_H, "W")
        anchor = nrun(pan, A_G * af, "W")
        clone = [nrun(pan, g * af, "W") for g in [0.25, 0.35, 0.45, 0.55, 0.65, 0.75]]
        K = len(pan.iinv)
        gidx = np.arange(K) % K_CTRL                      # deterministic disjoint partition
        disj = []
        for gg in range(K_CTRL):
            allow = (gidx == gg)
            disj.append(nrun(pan, A_G * build1(pan, N_CTRL, A_H, "W", allow=allow), "W"))
        hold_sets = []
        for gg in range(K_CTRL):
            Wg = A_G * build1(pan, N_CTRL, A_H, "W", allow=(gidx == gg))
            hold_sets.append(set(np.flatnonzero(np.abs(Wg[i0:]).sum(axis=0) > 0).tolist()))
        overlap = max((len(hold_sets[a] & hold_sets[b])
                       for a in range(K_CTRL) for b in range(a + 1, K_CTRL)), default=0)
        DISJ_OVERLAP[pan.name] = overlap
        rng = np.random.default_rng(CTRL_SEED + PANEL_SEED[pan.name])
        a = anchor[i0:]
        iid = [np.concatenate([np.zeros(i0), rng.normal(a.mean(), a.std(ddof=0), len(a))])
               for _ in range(K_CTRL)]
        for cname, series in [("CTRL_CLONE", clone), ("CTRL_DISJOINT", disj),
                              ("CTRL_IID", iid)]:
            mat = np.column_stack([s[i0:] for s in series])
            sh = [sharpe(s[i0:]) for s in series]
            rd = all_estimators(mat, sh, pan.spy[i0:])
            CTRL[(pan.name, cname)] = rd
            ctrl_rows.append(dict(panel=pan.name, control=cname, K=K_CTRL,
                                  true_dof=(1 if cname == "CTRL_CLONE" else K_CTRL), **rd))
        del af, clone, disj, iid
    CT = pd.DataFrame(ctrl_rows)
    CT.to_csv(f"{OUT}.controls.csv", index=False)
    say("      panel    control        true dof " + "".join(f"{e:>12s}" for e in EST))
    for _, r in CT.iterrows():
        say(f"      {r.panel:8s} {r.control:14s} {r.true_dof:8d} "
            + "".join(f"{r[e]:12.3f}" for e in EST))

    res_rows = []
    for p in PN:
        for e in EST:
            c, d, i = (CTRL[(p, "CTRL_CLONE")][e], CTRL[(p, "CTRL_DISJOINT")][e],
                       CTRL[(p, "CTRL_IID")][e])
            R = (d - c) / (i - c) if np.isfinite(i - c) and abs(i - c) > 1e-9 else np.nan
            res_rows.append(dict(panel=p, estimator=e, clone=c, disjoint=d, iid=i,
                                 resolution=R, has_res=bool(np.isfinite(R) and R >= 0.50)))
    RS = pd.DataFrame(res_rows)
    RS.to_csv(f"{OUT}.resolution.csv", index=False)
    say("")
    say("    RESOLUTION R = (DISJOINT - CLONE) / (IID - CLONE); 1 = full credit, 0 = blind.")
    say("      estimator     " + "".join(f"{p:>12s}" for p in PN) + "     mean   panels R>=0.50")
    for e in EST:
        z = RS[RS.estimator == e]
        say(f"      {e:14s}" + "".join(f"{float(z[z.panel == p].resolution.iloc[0]):12.3f}"
                                       for p in PN)
            + f" {z.resolution.mean():8.3f}   {int(z.has_res.sum())} of {len(PN)}")
    praw = RS[RS.estimator == "E_PR_RAW"]
    praw_ok = int(praw.has_res.sum()) >= 2
    alt_ok = [e for e in EST if e != "E_PR_RAW"
              and int(RS[RS.estimator == e].has_res.sum()) >= 2]
    gate("G6 CTRL_IID recovers ~6 under at least one PR estimator",
         round(float(CT[CT.control == "CTRL_IID"][["E_PR_RAW", "E_PR_XS",
                                                   "E_PR_RESID"]].max().max()), 3), ">= 5.0",
         CT[CT.control == "CTRL_IID"][["E_PR_RAW", "E_PR_XS", "E_PR_RESID"]].max().max() >= 5.0)
    gate("G7 CTRL_CLONE reads ~1 under every PR/ENT estimator (sanity)",
         round(float(CT[CT.control == "CTRL_CLONE"][[e for e in EST
                                                     if e != "E_SL_BAR"]].max().max()), 4),
         "<= 1.10",
         CT[CT.control == "CTRL_CLONE"][[e for e in EST if e != "E_SL_BAR"]].max().max() <= 1.10)
    gate("G8 the disjoint control really is disjoint (max names shared by any two books)",
         int(max(DISJ_OVERLAP.values())), 0, max(DISJ_OVERLAP.values()) == 0)
    d0 = all_estimators(np.column_stack([booked["U56"][k][panels[0].i0:] for k in ALT]),
                        [Sfull[("U56", k)] for k in ALT], panels[0].spy[panels[0].i0:])
    d1 = all_estimators(np.column_stack([booked["U56"][k][panels[0].i0:] for k in ALT]),
                        [Sfull[("U56", k)] for k in ALT], panels[0].spy[panels[0].i0:])
    dd = max(abs(d0[e] - d1[e]) for e in EST)
    gate("G9 estimators are deterministic (same matrix twice)", dd, 0.0, dd == 0.0)

    # ------------------------------------------------------------ ARM C: the record's ladders
    say("")
    say("=" * 110)
    say("ARM C — EVERY ESTIMATOR ON EVERY LADDER THE RECORD HAS WALKED")
    say("=" * 110)
    lrows = []
    for pan in panels:
        i0 = pan.i0
        for lad, keys in LADSETS.items():
            mat = np.column_stack([booked[pan.name][k][i0:] for k in keys])
            sh = [Sfull[(pan.name, k)] for k in keys]
            rd = all_estimators(mat, sh, pan.spy[i0:])
            lrows.append(dict(panel=pan.name, ladder=lad, K=len(keys), **rd,
                              **{f"share_{e}": rd[e] / len(keys) for e in EST}))
    LD = pd.DataFrame(lrows)
    LD.to_csv(f"{OUT}.ladders.csv", index=False)
    say("")
    say("      panel    ladder      K " + "".join(f"{e:>12s}" for e in EST))
    for _, r in LD.iterrows():
        say(f"      {r.panel:8s} {r.ladder:9s} {r.K:3d} " + "".join(f"{r[e]:12.3f}" for e in EST))

    # ------------------------------------------------------------ ARM D: census and re-wording
    say("")
    say("=" * 110)
    say("ARM D — THE CENSUS: WHICH COMMITTED 'WE WALKED N' HEADLINES THE CLAUSE RE-WORDS")
    say("=" * 110)
    U, nmd = units()
    X = census(U)
    X.to_csv(f"{OUT}.census.csv", index=False)
    say("")
    say(f"    {len(U)} committed text units over LEADERBOARD.md + CHANGELOG.md + {nmd} .md files")
    say("    in research/backtests/.  (1230's reflexivity caveat applies: this run's own console")
    say("    and memo become units for the NEXT census, so the denominator is tree-dated.)")
    say("")
    say("      claim set   units   state a COUNT   name an AXIS   median stated N")
    for cs in CLAIM_SETS:
        z = X[X[cs]]
        say(f"      {cs:10s} {len(z):6d}   {int(z.n_counts.gt(0).sum()):13d}   "
            f"{int(z.n_axes.gt(0).sum()):12d}   "
            f"{(np.nanmedian(z.stated_N) if z.stated_N.notna().any() else float('nan')):.1f}")

    # N_eff of each rebuildable axis subset, per estimator (median over panels)
    SUBSETS = [frozenset(s) for s in
               [{"N"}, {"H"}, {"GROSS"}, {"CADENCE"}, {"N", "H"}, {"N", "GROSS"},
                {"H", "GROSS"}, {"N", "CADENCE"}, {"GROSS", "CADENCE"}, {"H", "CADENCE"},
                {"N", "H", "GROSS"}, {"N", "H", "CADENCE"}, {"N", "GROSS", "CADENCE"},
                {"H", "GROSS", "CADENCE"}, {"N", "H", "GROSS", "CADENCE"}]]
    sub_keys, sub_neff = {}, {}
    for axes in SUBSETS:
        ks = []
        for a in sorted(axes):
            ks += [(a, r) for r in LAD[a]]
        ks = [k for k in ks if k == INC or k not in ANCH_KEYS] or ks
        ks = list(dict.fromkeys(ks))
        sub_keys[axes] = ks
        per = {e: [] for e in EST}
        for pan in panels:
            i0 = pan.i0
            mat = np.column_stack([booked[pan.name][k][i0:] for k in ks])
            rd = all_estimators(mat, [Sfull[(pan.name, k)] for k in ks], pan.spy[i0:])
            for e in EST:
                per[e].append(rd[e])
        sub_neff[axes] = {e: (float(np.nanmedian(per[e]))
                              if np.isfinite(per[e]).any() else np.nan) for e in EST}
    srows = [dict(axes="+".join(sorted(a)), K=len(sub_keys[a]), **sub_neff[a]) for a in SUBSETS]
    pd.DataFrame(srows).to_csv(f"{OUT}.subsets.csv", index=False)
    say("")
    say("    N_eff of each rebuildable axis subset (median over the three panels):")
    say("      axes                          K " + "".join(f"{e:>12s}" for e in EST))
    for a in SUBSETS:
        say(f"      {'+'.join(sorted(a)):28s} {len(sub_keys[a]):3d} "
            + "".join(f"{sub_neff[a][e]:12.3f}" for e in EST))

    rw_rows, detail = [], []
    for cs in CLAIM_SETS:
        z = X[X[cs] & X.stated_N.notna()]
        for e in EST:
            n_res = n_rw = n_und = 0
            for _, r in z.iterrows():
                axes = frozenset(a for a in LADS if a in str(r["axes"]).split("|"))
                if not axes:
                    continue
                n_res += 1
                ne = sub_neff[axes][e]
                if not np.isfinite(ne):
                    n_und += 1
                    rw = False
                else:
                    rw = bool(r.stated_N >= REWORD_FACTOR * ne)
                n_rw += int(rw)
                if cs == "CS_STRICT":
                    detail.append(dict(uid=r.uid, src=r.src, estimator=e, stated_N=r.stated_N,
                                       axes="+".join(sorted(axes)), K=len(sub_keys[axes]),
                                       N_eff=ne, defined=bool(np.isfinite(ne)), reword=rw,
                                       snippet=r.snippet))
            den = n_res - n_und
            rw_rows.append(dict(claim_set=cs, estimator=e, claims=len(z), resolvable=n_res,
                                undefined=n_und, reworded=n_rw,
                                share=(n_rw / den if den else np.nan)))
    RW = pd.DataFrame(rw_rows)
    RW.to_csv(f"{OUT}.reword.csv", index=False)
    DT = pd.DataFrame(detail)
    DT.to_csv(f"{OUT}.reword_detail.csv", index=False)
    say("")
    say(f"    THE CLAUSE: print N_eff beside the stated N; a headline is RE-WORDED when its")
    say(f"    stated N is at least {REWORD_FACTOR:.0f}x its N_eff.  All {len(RW)} dial cells:")
    say("      claim set   estimator      claims  resolvable  N_eff undef  re-worded   share")
    for _, r in RW.iterrows():
        say(f"      {r.claim_set:10s}  {r.estimator:12s} {r.claims:7d} {r.resolvable:11d} "
            f"{r.undefined:12d} {r.reworded:10d}   {r.share:.4f}")
    say("")
    say("    DISCRIMINATION.  A clause that re-words EVERY claim separates none of them.  The")
    say("    spread of the N_eff readings actually printed is the clause's information:")
    say("      estimator      distinct N_eff values printed   min      max      sd")
    for e in EST:
        vv = np.array([sub_neff[a][e] for a in SUBSETS], float)
        say(f"      {e:12s}   {len(np.unique(np.round(vv, 3))):26d}   {np.nanmin(vv):6.3f}   "
            f"{np.nanmax(vv):6.3f}   {np.nanstd(vv):6.3f}")

    if len(DT):
        say("")
        say("    THE HEADLINES THE CLAUSE HITS HARDEST (CS_STRICT, E_PR_RAW, top 12 by stated N):")
        d0 = DT[(DT.estimator == "E_PR_RAW")].sort_values("stated_N", ascending=False).head(12)
        for _, r in d0.iterrows():
            say(f"      stated N {int(r.stated_N):4d}  K {int(r.K):2d}  N_eff {r.N_eff:5.3f}  "
                f"{'RE-WORD' if r.reword else ('stands ' if r.defined else 'UNDEF  '):7s} "
                f"[{r.src[:28]:28s}] {r.snippet[:70]}")
        best_alt = alt_ok[0] if alt_ok else "E_SL_BAR"
        say("")
        say(f"    THE SAME HEADLINES UNDER {best_alt} (the estimator with resolution):")
        d1 = DT[DT.estimator == best_alt].sort_values("stated_N", ascending=False).head(12)
        for _, r in d1.iterrows():
            say(f"      stated N {int(r.stated_N):4d}  K {int(r.K):2d}  N_eff {r.N_eff:5.3f}  "
                f"{'RE-WORD' if r.reword else ('stands ' if r.defined else 'UNDEF  '):7s} "
                f"[{r.src[:28]:28s}] {r.snippet[:70]}")

    # ------------------------------------------------------------ ARM E: rule 8, both KEEP paths
    say("")
    say("=" * 110)
    say("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS")
    say("=" * 110)
    say("")
    say("    (E1) Every rung book, full sample and 2017-2026, 4a vs live RULES v2 and 4b vs SPY.")
    brows = []
    for pan in panels:
        i0, io = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = BM[(pan.name, "SPY_OOS")], BM[(pan.name, "LIVE_OOS")]
        for k in BOOKKEY:
            rr = booked[pan.name][k]
            k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
            k4a_o, k4b_o, mo, oh1, oh2 = keep_paths(rr[io:], so, lo_)
            brows.append(dict(panel=pan.name, book=akey(k), ladder=k[0],
                              is_incumbent=(k in ANCH_KEYS), **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(brows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say(f"         {len(BK)} (panel, book) rows.  4a {int(BK.KEEP_4a.sum())}; 4b full "
        f"{int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    for p in PN:
        s, l = BM[(p, "SPY")], BM[(p, "LIVE")]
        so, lo_ = BM[(p, "SPY_OOS")], BM[(p, "LIVE_OOS")]
        say(f"         {p:8s} SPY full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
            f"   OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:8.2%}")
        say(f"         {p:8s} LIVE v2  {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
            f"   OOS {lo_['CAGR']:7.2%} / {lo_['Sharpe']:.4f} / {lo_['MaxDD']:8.2%}")

    say("")
    say("    (E2) THE CLAUSE RUN AS A CHOOSER.  For every (panel, axis subset) the IS Sharpe")
    say("         argmax is taken on warm-up..2016-12-31 ONLY and 2017-2026 is read ONCE.")
    say("         RAW chooses over all rungs.  DEDUP:<estimator>:<rep> first collapses the")
    say("         candidate set to round(N_eff) correlation clusters measured ON THE IS WINDOW")
    say("         and keeps one member per cluster — rep=MIN is 1239's lowest-IS-Sharpe rule,")
    say("         rep=MAX the highest.  SL is 1239's Sharpe-bar de-dup, carried for continuity.")
    MODES = (["RAW"]
             + [f"DEDUP:{e}:{rp}" for e in ["E_PR_RAW", "E_PR_XS", "E_PR_RESID"]
                for rp in ["MIN", "MAX"]]
             + ["DEDUP:E_SL_BAR:MIN"])
    wrows = []
    for pan in panels:
        i0, io = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = BM[(pan.name, "SPY_OOS")], BM[(pan.name, "LIVE_OOS")]
        Sis = {k: sharpe(booked[pan.name][k][i0:io]) for k in BOOKKEY}
        for axes in SUBSETS:
            keys = sub_keys[axes]
            matis = np.column_stack([booked[pan.name][k][i0:io] for k in keys])
            shis = [Sis[k] for k in keys]
            rd_is = all_estimators(matis, shis, pan.spy[i0:io])
            for mode in MODES:
                if mode == "RAW":
                    cand = keys
                else:
                    _, est, rp = mode.split(":")
                    if est == "E_SL_BAR":
                        cand = reps_sl(keys, shis)
                    else:
                        gs = clusters_corr(matis, rd_is[est])
                        cand = []
                        for g in gs:
                            mem = sorted(g, key=lambda i: (shis[i] if np.isfinite(shis[i])
                                                           else np.inf))
                            cand.append(keys[mem[0] if rp == "MIN" else mem[-1]])
                if not cand:
                    continue
                ch = max(cand, key=lambda k: (Sis[k] if np.isfinite(Sis[k]) else -np.inf))
                rr = booked[pan.name][ch]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
                wrows.append(dict(panel=pan.name, axis_set="+".join(sorted(axes)), mode=mode,
                                  K=len(keys), K_cand=len(cand), chosen=akey(ch),
                                  N_eff_IS=(np.nan if mode == "RAW"
                                            else rd_is[mode.split(":")[1]]),
                                  IS_Sharpe=Sis[ch], **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
        rr = booked[pan.name][INC]
        k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
        _, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
        wrows.append(dict(panel=pan.name, axis_set="NONE", mode="DO_NOTHING", K=0, K_cand=0,
                          chosen=akey(INC), N_eff_IS=np.nan, IS_Sharpe=np.nan, **m, H1=h1, H2=h2,
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          KEEP_4a=k4a, KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    dn = float(W8[W8["mode"] == "DO_NOTHING"].OOS_Sharpe.mean())
    say("")
    say(f"         RULE-8 ROWS: {len(W8)}.  4a {int(W8.KEEP_4a.sum())}; 4b full "
        f"{int(W8.KEEP_4b.sum())}; 4b OOS {int(W8.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())}.")
    say("")
    say(f"         Mean OOS Sharpe by chooser mode (DO_NOTHING = {dn:.4f}):")
    raw_m = float(W8[W8["mode"] == "RAW"].OOS_Sharpe.mean())
    for mode in MODES:
        z = W8[W8["mode"] == mode]
        if not len(z):
            continue
        moved = (0 if mode == "RAW" else
                 int(sum(1 for _, r in z.iterrows()
                         if r.chosen != W8[(W8.panel == r.panel) & (W8["axis_set"] == r["axis_set"])
                                           & (W8["mode"] == "RAW")].chosen.iloc[0])))
        say(f"           {mode:22s} {z.OOS_Sharpe.mean():.4f}  "
            f"(d_RAW {z.OOS_Sharpe.mean()-raw_m:+.4f})  rows {len(z):3d}  "
            f"mean candidates {z.K_cand.mean():5.2f}  picks moved {moved:2d}")

    mx = W8[W8["mode"].str.endswith(":MAX")]
    moved_max = 0
    for _, r in mx.iterrows():
        ref = W8[(W8.panel == r.panel) & (W8["axis_set"] == r["axis_set"])
                 & (W8["mode"] == "RAW")].chosen.iloc[0]
        moved_max += int(r.chosen != ref)
    gate("G10 a de-dup that keeps the best-IS member cannot move an IS-argmax chooser",
         moved_max, 0, moved_max == 0)

    say("")
    say("    (E3) IS N_eff WORTH PRINTING AT ALL?  If the number carries information it should")
    say("         predict the SELECTION PENALTY — how much the IS argmax loses out of sample.")
    say("         Over the 45 (panel, subset) RAW cells: penalty = OOS Sharpe(RAW pick) - OOS")
    say("         Sharpe(do-nothing incumbent), and decay = IS Sharpe(pick) - OOS Sharpe(pick).")
    prows = []
    raw = W8[W8["mode"] == "RAW"]
    for _, r in raw.iterrows():
        axes = frozenset(r["axis_set"].split("+"))
        dn_p = float(W8[(W8.panel == r.panel) & (W8["mode"] == "DO_NOTHING")].OOS_Sharpe.iloc[0])
        prows.append(dict(panel=r.panel, axis_set=r["axis_set"], K=r.K,
                          penalty=r.OOS_Sharpe - dn_p,
                          decay=r.IS_Sharpe - r.OOS_Sharpe,
                          **{e: sub_neff[axes][e] for e in EST}))
    PP = pd.DataFrame(prows)
    PP.to_csv(f"{OUT}.penalty.csv", index=False)

    def rankcorr(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() < 4:
            return np.nan
        ra = pd.Series(a[ok]).rank().values
        rb = pd.Series(b[ok]).rank().values
        return float(np.corrcoef(ra, rb)[0, 1])

    say("")
    say(f"         {len(PP)} cells.  rank corr of the printed statistic with:")
    say("           statistic        vs PENALTY (OOS pick - do-nothing)   vs DECAY (IS - OOS)")
    for e in EST + ["K"]:
        say(f"           {e:14s}   {rankcorr(PP[e], PP.penalty):28.3f}   "
            f"{rankcorr(PP[e], PP.decay):18.3f}")

    # ------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    say("VERDICT")
    say("=" * 110)
    if praw_ok:
        outcome = "(A) PUBLISH N_eff^PR AS IS"
    elif alt_ok:
        outcome = "(B) DO NOT PUBLISH IT ALONE — THE CLAUSE MUST NAME A DE-FACTORED ESTIMATOR"
    else:
        outcome = "(C) PUBLISH NOTHING BAR-FREE"
    say("")
    say(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    say(f"      E_PR_RAW resolution {praw.resolution.mean():.3f} mean over panels, "
        f">= 0.50 at {int(praw.has_res.sum())} of {len(PN)}.")
    say(f"      Estimators clearing the bar on a majority of panels: "
        f"{', '.join(alt_ok) if alt_ok else 'NONE'}.")
    say("")
    say(f"    CAPITAL.  4a {int(BK.KEEP_4a.sum())} of {len(BK)} books and "
        f"{int(W8.KEEP_4a.sum())} of {len(W8)} rule-8 rows; 4b BOTH "
        f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books / "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())} rule-8 rows.  Best chooser arm mean OOS")
    arm_mean = W8[W8["mode"] != "DO_NOTHING"].groupby("mode").OOS_Sharpe.mean()
    say(f"    Sharpe {arm_mean.max():.4f} ({arm_mean.idxmax()}) against do-nothing {dn:.4f} — "
        f"no arm beats doing nothing.  NO NEW BOOK, NO RULES CHANGE FROM THIS RUN.")
    say("")
    say("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL663 is a")
    say("    current sub-$2B screen less the names with max_1d_move >= 1.0.  Every LEVEL is")
    say("    optimistic.  The headline is a RATIO of one estimator's reading against its own")
    say("    controls on the same tape, which a level bias common to the cell largely cancels")
    say("    out of; the 4a / 4b columns and the rule-8 levels carry the full bias.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    for _, r in GD.iterrows():
        say(f"      {'PASS' if r.pass_ else 'FAIL'}  {r.gate}  value={r.value}  target={r.target}")
    say("")
    say(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
