#!/usr/bin/env python3
"""
Idea 1239 (lane cloud, 2026-09-17) — is the record's CANDIDATE SET half CLONES on EVERY AXIS
it has ever WALKED?

THE PREMISE, READ FROM THE RECORD.  Idea 1237's G12 found that 9 of the 18 non-incumbent rung
books sit within 0.0040 of Sharpe of the incumbent, and that all nine are GROSS rungs — 1189's
degeneracy, where the cash sleeve returns exactly 0% so mean and vol both scale by g and Sharpe
cancels.  The smallest NON-GROSS gap in that same candidate set is 0.0171, four times wider.
Consequence: a "we walked 18 alternatives" sentence on this record is, half the time, a walk
over RE-LEVERINGS OF ONE BOOK.  1237 also found mean-over-candidates and median-over-candidates
gave opposite answers (106.3% vs 13.2%) on the same set, which is exactly what a clone-heavy
candidate set does to a mean.

WHAT IS BEING TESTED, STATED BEFORE ANY NUMBER IS READ.  The queue's word is "every axis".  So
the question is not whether the GROSS ladder is degenerate (1189 proved that and 1237 replayed
it) but whether DEGENERACY IS A PROPERTY OF THE GROSS DIAL OR OF THE RECORD'S CANDIDATE SETS IN
GENERAL.  Define, for a candidate set of K books with realised daily NET return series r_k:

    CLONE GRAPH        edge(i,j)  <=>  |Sharpe(r_i) - Sharpe(r_j)| <= b        (b = the bar dial)
    N_eff^SL(b)        number of connected components of that graph (single linkage)
    N_eff^CL(b)        number of complete-linkage groups (every pair inside a group within b)
    N_eff^PR           (sum lambda)^2 / sum lambda^2 of the candidate returns' correlation
                       matrix — BAR-FREE, and by 1189's identity it must read ~1 on GROSS

N_eff^SL is the reading the record's own language implies ("these two are the same book"), so
it is the headline; N_eff^CL is reported beside it at every cell because single linkage chains,
and N_eff^PR is the bar-free cross-check.  The ratio N_eff/K is the CLONE-FREE SHARE of a walk.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) EVERY AXIS — the median clone-free share N_eff^SL/K is <= 0.60 on a MAJORITY of the
      (panel, non-GROSS ladder) cells at the record's own bar.  "Half clones" is a property of
      the record's walks, not of the gross dial.
  (B) GROSS ONLY — GROSS reads N_eff/K <= 0.30 while every non-GROSS ladder reads >= 0.80 at
      the record's own bar.  1237's finding is a gross-dial fact and does not generalise.
  (C) MIXED — some non-GROSS axis is degenerate and some is not; the clone share is an AXIS
      property that has to be quoted per axis.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET       {CS_STRICT, CS_PROX, CS_ALL} — which committed units count as a "we walked N
                  alternatives" claim.
                  CS_STRICT  walk language AND an explicit candidate COUNT AND a verdict word.
                  CS_PROX    walk language AND an explicit candidate COUNT.
                  CS_ALL     any committed unit naming a ladder / candidate set / comparison set.
  DEGENERACY BAR  {B_TIGHT, B_MID, B_LOOSE} = |dSharpe| <= 0.0040 / 0.0100 / 0.0171.
                  B_TIGHT is 1237's own clone bar; B_LOOSE is 1237's smallest NON-GROSS gap, so
                  it is the widest bar at which the record's own reading still discriminates.

NOT DIALS, REPORTED AT EVERY VALUE: PANEL {U56, B136, SMALL} (rule 9); the four ladders the
record has actually walked (N, H, GROSS, CADENCE) and their union; the 22 rung keys / 19
distinct books; the linkage rule (SL, CL, PR all published); the 4a and 4b legs.

FROZEN AT THE RECORD'S CONSTRUCTION: 3-leg composite (21/252, 0/126, 0/63), above-200d
eligibility, max_vol 0.60, GROSS 0.75 anchor, N=20, H=126, weekly cadence, 10 bps (rule 2),
decide-at-t / apply-at-t+1, warm-up 260 rows, OOS split 2017-01-01 (rule 8).

PROTOCOL: rule 2 costs and execution; rule 8 walk-forward with every choice made on the IS
window ONLY and 2017-2026 read once; BOTH KEEP paths (4a vs live RULES v2, 4b vs SPY) on every
candidate book and every rule-8 row; rule 9 survivorship stated.
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

DATE = "2026-09-17"
SLUG = "is-the-record-s-CANDIDATE-SET-half-CLONES-on-every-axis-it-has-ever-WALKED"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

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
BARS = {"B_TIGHT": 0.0040, "B_MID": 0.0100, "B_LOOSE": 0.0171}
CLAIM_SETS = ["CS_STRICT", "CS_PROX", "CS_ALL"]
LIVE_MAXDD_COMMITTED = -0.1205

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=value, target=target, pass_=bool(ok)))
    return bool(ok)


# ==================================================================== panels / runner (1237's)
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


def build1(pan, N, H, freq, lag=1):
    """The record's min-hold selection frame at GROSS = 1.0; lag=1 is rule 2's decide-at-t /
    apply-at-t+1.  Row t is the APPLICATION-time weight."""
    reb = pan.seg[freq]
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
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
    m = triple(r)
    return dict(H1=h1, H2=h2, **m)


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


# ==================================================================== degeneracy machinery
def n_eff_sl(vals, bar):
    """Single-linkage components of the |dSharpe| <= bar graph.  Sorting makes this exact on a
    1-D statistic: a component breaks exactly where consecutive sorted values differ by > bar."""
    v = np.sort(np.asarray([x for x in vals if np.isfinite(x)], float))
    if len(v) == 0:
        return 0, []
    breaks = np.flatnonzero(np.diff(v) > bar)
    groups = np.split(v, breaks + 1)
    return len(groups), [len(g) for g in groups]


def n_eff_cl(vals, bar):
    """Complete-linkage on a 1-D statistic: greedily close a group when its span exceeds bar.
    Deterministic and optimal for the interval-cover reading (minimum number of width-bar
    intervals covering the points)."""
    v = np.sort(np.asarray([x for x in vals if np.isfinite(x)], float))
    if len(v) == 0:
        return 0
    k, anchor = 1, v[0]
    for x in v[1:]:
        if x - anchor > bar:
            k += 1
            anchor = x
    return k


def n_eff_pr(mat):
    """Participation ratio of the correlation matrix's eigenvalues.  Bar-free.  == 1 when every
    candidate is a re-levering of one book; == K when they are mutually uncorrelated."""
    X = np.asarray(mat, float)
    X = X[:, np.isfinite(X).all(axis=0)]
    sd = X.std(axis=0, ddof=0)
    ok = sd > 0
    X = X[:, ok]
    if X.shape[1] == 0:
        return np.nan
    R = np.corrcoef(X, rowvar=False)
    R = np.atleast_2d(R)
    lam = np.linalg.eigvalsh(R)
    lam = np.clip(lam, 0, None)
    s1, s2 = lam.sum(), (lam ** 2).sum()
    return float(s1 * s1 / s2) if s2 > 0 else np.nan


def reps_sl(keys, vals, bar):
    """One representative key per single-linkage clone cluster (the lowest-Sharpe member, a
    deterministic rule that does not peek at OOS)."""
    pairs = [(v, k) for k, v in zip(keys, vals) if np.isfinite(v)]
    pairs.sort()
    out, anchor_v, anchor_k = [], None, None
    for v, k in pairs:
        if anchor_v is None or v - anchor_v > bar:
            out.append(k)
            anchor_v, anchor_k = v, k
        else:
            anchor_v = v      # single linkage: the chain extends
    return out


# ==================================================================== the record's own text
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


def census(U):
    """TEXTUAL classification, reported as such.  A unit is a WALK CLAIM if it uses walk
    language; it is COUNTED if it states an explicit candidate count; it is ADJUDICATED if it
    also carries a verdict word.  Axes are whichever of the record's four ladders it names."""
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
                         names_GROSS=("GROSS" in ax),
                         CS_ALL=bool(w),
                         CS_PROX=bool(w and cs),
                         CS_STRICT=bool(w and cs and ver)))
    return pd.DataFrame(rows)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1239 (lane cloud, 2026-09-17) — is the record's CANDIDATE SET half CLONES on")
    say("EVERY AXIS it has ever WALKED?")
    say("=" * 110)
    say("")
    say("  1237's G12: 9 of 18 non-incumbent rung books within 0.0040 of Sharpe of the")
    say("  incumbent, ALL NINE GROSS rungs; smallest non-GROSS gap 0.0171.  The queue asks")
    say("  whether that is a GROSS fact or a property of the record's candidate sets.")
    say("  N_eff^SL(b) = components of the |dSharpe| <= b graph; N_eff^CL(b) = complete-linkage")
    say("  groups; N_eff^PR = participation ratio of the candidates' correlation matrix (BAR-")
    say("  FREE, and ~1 on GROSS by 1189's scaling identity).  CLONE-FREE SHARE = N_eff / K.")
    say("  PRE-DECLARED: (A) EVERY AXIS — median clone-free share <= 0.60 on a majority of")
    say("  (panel, non-GROSS ladder) cells at the record's own bar.  (B) GROSS ONLY — GROSS")
    say("  <= 0.30 and every non-GROSS ladder >= 0.80.  (C) MIXED — otherwise.")

    # ------------------------------------------------------------------ ARM A: panels, books
    say("")
    say("=" * 110)
    say("ARM A — PANELS, THE 22 RUNG KEYS, AND THE MACHINERY GATES")
    say("=" * 110)
    panels = []
    pxU = load_universe()
    panels.append(Panel("U56", pxU, [c for c in pxU.columns if c != "SPY"]))
    pxB = load_universe(broad=True)
    panels.append(Panel("B136", pxB, [c for c in pxB.columns if c != "SPY"]))
    pxS = load_universe(small=True)
    mv = pxS.pct_change().abs().max()
    inv = [c for c in pxS.columns if c != "SPY" and mv[c] < 1.0]
    panels.append(Panel("SMALL", pxS, inv))
    say("")
    say(f"  PANELS: U56 {len(pxU.columns)-1} names; B136 {len(pxB.columns)-1}; "
        f"SMALL {len(inv)} investable of {len(pxS.columns)-1} "
        f"({len(pxS.columns)-1-len(inv)} dropped for max_1d_move >= 1.0); SPY benchmark only.")

    booked, BM, BOOKKEY = {}, {}, []
    for pan in panels:
        frames = {}
        for N in LAD["N"]:
            frames[(N, A_H, "W")] = None
        for H in LAD["H"]:
            frames[(A_N, H, "W")] = None
        frames[(A_N, A_H, "M")] = None
        for key in list(frames):
            frames[key] = build1(pan, key[0], key[1], key[2])
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
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        BM[(pan.name, "SPY")] = bmref(pan.spy[pan.i0:])
        BM[(pan.name, "LIVE")] = bmref(b["returns"].values[pan.i0:])
        say(f"    {pan.name:6s} {len(books)} rung books built.")
        del frames

    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    INC = ("N", A_N)
    ilim = {pan.name: int(pan.idx.searchsorted(pd.Timestamp(OOS_START))) for pan in panels}
    for pan in panels:
        BM[(pan.name, "SPY_OOS")] = bmref(pan.spy[ilim[pan.name]:])
        bb = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")["returns"].values
        BM[(pan.name, "LIVE_OOS")] = bmref(bb[ilim[pan.name]:])

    pan = panels[0]
    Wt = A_G * build1(pan, A_N, A_H, "W")
    Wdf = pd.DataFrame(Wt, index=pan.idx, columns=pan.px.columns)
    eb = backtest(pan.px, Wdf.shift(-1).fillna(0.0), cost_bps=COST, freq="W")["returns"].values
    g1 = float(np.nanmax(np.abs(eb[WARMUP:] - nrun(pan, Wt, "W")[WARMUP:])))
    gate("G1 fast runner == engine.backtest on the decision-time frame", g1, 1e-10, g1 < 1e-10)
    lm = BM[("U56", "LIVE")]["MaxDD"]
    gate("G2 live RULES v2 U56 MaxDD == committed -12.05%", lm, LIVE_MAXDD_COMMITTED,
         abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    dev = 0.0
    for k in ANCH_KEYS[1:]:
        dev = max(dev, float(np.abs(booked["U56"][k] - booked["U56"][ANCH_KEYS[0]]).max()))
    gate("G3 the four anchor keys are ONE book (bit for bit)", dev, 0.0, dev == 0.0)
    ALT = [k for k in BOOKKEY if k == INC or k not in ANCH_KEYS]
    gate("G4 distinct candidate set size (1237's 19)", float(len(ALT)), 19.0, len(ALT) == 19)

    # replay 1237's G12 exactly (ITS statistic: gap = MAX over the three panels, bar 0.005)
    Sfull = {(p.name, k): sharpe(booked[p.name][k][p.i0:]) for p in panels for k in BOOKKEY}
    PN = [q.name for q in panels]
    gapmax = {k: max(abs(Sfull[(p, k)] - Sfull[(p, INC)]) for p in PN)
              for k in BOOKKEY if k not in ANCH_KEYS}
    DEGEN = [k for k in gapmax if k[0] == "GROSS"]
    REAL = [k for k in gapmax if k[0] != "GROSS"]
    worst_g = max(gapmax[k] for k in DEGEN)
    worst_r = min(gapmax[k] for k in REAL)
    gate("G5a 1237's G12 replay — worst GROSS gap (max over 3 panels)", round(worst_g, 4),
         0.0040, abs(worst_g - 0.0040) < 5e-4)
    gate("G5b 1237's G12 replay — smallest NON-GROSS gap (max over 3 panels)",
         round(worst_r, 4), 0.0171, abs(worst_r - 0.0171) < 5e-4)
    gate("G5c the partition is 9 GROSS clones and 9 non-GROSS non-clones",
         f"{len(DEGEN)}/{len(REAL)}", "9/9", len(DEGEN) == 9 and len(REAL) == 9)
    say("")
    say(f"    1237's G12 replays EXACTLY: worst GROSS gap {worst_g:.4f}, smallest non-GROSS gap")
    say(f"    {worst_r:.4f}, partition {len(DEGEN)} GROSS / {len(REAL)} non-GROSS.")
    say("")
    say("    BYCATCH, READ BEFORE THE CENSUS.  1237's gap is a MAX OVER THE THREE PANELS, which")
    say("    is the widest reading of a distance and therefore the most favourable one for a")
    say("    clean partition.  Per panel the same partition is NOT clean:")
    say("      panel   non-incumbent books within 0.0040 of the incumbent   all GROSS?   "
        "smallest non-GROSS gap")
    for p in PN:
        w = [k for k in gapmax if abs(Sfull[(p, k)] - Sfull[(p, INC)]) <= BARS["B_TIGHT"]]
        ngp = min(abs(Sfull[(p, k)] - Sfull[(p, INC)]) for k in REAL)
        say(f"      {p:6s}  {len(w):2d} of {len(gapmax)}"
            f"{'':38s}{str(all(k[0] == 'GROSS' for k in w)):10s}   {ngp:.4f}")
    say("    So the record's own clone / non-clone partition is a MAX-over-panels artefact: on")
    say("    at least one panel a genuinely different book is closer to the incumbent than the")
    say("    bar that defines a clone.")

    # ------------------------------------------------------------------ ARM B: degeneracy
    say("")
    say("=" * 110)
    say("ARM B — DEGENERACY OF EVERY AXIS THE RECORD HAS WALKED (all 9 dial cells published)")
    say("=" * 110)
    say("")
    say("    K = rungs on the ladder.  N_eff^SL / N_eff^CL at each bar; N_eff^PR is bar-free.")
    say("    CLONE-FREE SHARE = N_eff^SL / K.")
    drows = []
    for pan in panels:
        for lad in LADS + ["UNION"]:
            keys = BOOKKEY if lad == "UNION" else [(lad, r) for r in LAD[lad]]
            if lad == "UNION":
                keys = ALT                       # 19 distinct books, anchors already collapsed
            vals = [Sfull[(pan.name, k)] for k in keys]
            mat = np.column_stack([booked[pan.name][k][pan.i0:] for k in keys])
            pr = n_eff_pr(mat)
            rho = np.corrcoef(mat, rowvar=False)
            offd = rho[~np.eye(len(keys), dtype=bool)] if len(keys) > 1 else np.array([1.0])
            for bn, b in BARS.items():
                k_sl, sizes = n_eff_sl(vals, b)
                k_cl = n_eff_cl(vals, b)
                drows.append(dict(panel=pan.name, ladder=lad, K=len(keys), bar=bn, bar_v=b,
                                  N_eff_SL=k_sl, N_eff_CL=k_cl, N_eff_PR=pr,
                                  clone_free_SL=k_sl / len(keys), clone_free_CL=k_cl / len(keys),
                                  clone_free_PR=pr / len(keys),
                                  min_rho=float(offd.min()), med_rho=float(np.median(offd)),
                                  S_spread=float(np.nanmax(vals) - np.nanmin(vals)),
                                  largest_cluster=max(sizes) if sizes else 0))
    D = pd.DataFrame(drows)
    D.to_csv(f"{OUT}.degeneracy.csv", index=False)
    for bn in BARS:
        say("")
        say(f"    BAR {bn} (|dSharpe| <= {BARS[bn]}):")
        say("      panel  ladder     K   N_SL  N_CL   N_PR   free_SL  min_rho  Sharpe spread")
        for _, r in D[D.bar == bn].iterrows():
            say(f"      {r.panel:6s} {r.ladder:8s} {r.K:4d}  {r.N_eff_SL:4d}  {r.N_eff_CL:4d}  "
                f"{r.N_eff_PR:5.2f}   {r.clone_free_SL:6.3f}  {r.min_rho:7.4f}  {r.S_spread:.4f}")

    # the pre-declared reading
    rec = D[D.bar == "B_TIGHT"]
    ng_cells = rec[(rec.ladder != "GROSS") & (rec.ladder != "UNION")]
    g_cells = rec[rec.ladder == "GROSS"]
    share_ng = ng_cells.clone_free_SL.values
    share_g = g_cells.clone_free_SL.values
    maj_deg = float((share_ng <= 0.60).mean())
    say("")
    say(f"    AT THE RECORD'S OWN BAR (B_TIGHT = {BARS['B_TIGHT']}):")
    say(f"      GROSS       clone-free share {share_g.min():.3f}-{share_g.max():.3f} "
        f"(median {np.median(share_g):.3f}) over {len(share_g)} panels")
    say(f"      NON-GROSS   clone-free share {share_ng.min():.3f}-{share_ng.max():.3f} "
        f"(median {np.median(share_ng):.3f}) over {len(share_ng)} (panel, ladder) cells; "
        f"{maj_deg:.3f} of them <= 0.60")
    gate("G6 GROSS returns are near-exact re-leverings (min pairwise rho)",
         round(float(g_cells.min_rho.min()), 6), ">= 0.999", g_cells.min_rho.min() >= 0.999)
    gate("G7 GROSS N_eff^PR ~ 1 (bar-free 1189 identity)",
         round(float(g_cells.N_eff_PR.max()), 4), "<= 1.05", g_cells.N_eff_PR.max() <= 1.05)

    # ------------------------------------------------------------------ ARM C: mean vs median
    say("")
    say("=" * 110)
    say("ARM C — WHY MEAN-OVER-CANDIDATES AND MEDIAN-OVER-CANDIDATES DISAGREE")
    say("=" * 110)
    say("")
    say("    d_A = OOS Sharpe(A) - OOS Sharpe(incumbent) over the 19-book candidate set.  The")
    say("    record summarises such a set with a MEAN and with a MEDIAN.  Deduplicating to one")
    say("    representative per clone cluster moves the MEAN (clones are all near the")
    say("    incumbent, so they drag the mean toward 0) and barely moves the MEDIAN's sign.")
    crows = []
    for pan in panels:
        io = ilim[pan.name]
        soos = {k: sharpe(booked[pan.name][k][io:]) for k in ALT}
        d_raw = np.array([soos[k] - soos[INC] for k in ALT if k != INC], float)
        for bn, b in BARS.items():
            reps = reps_sl([k for k in ALT], [Sfull[(pan.name, k)] for k in ALT], b)
            d_ded = np.array([soos[k] - soos[INC] for k in reps if k != INC], float)
            crows.append(dict(panel=pan.name, bar=bn, K_raw=len(d_raw), K_ded=len(d_ded),
                              mean_raw=float(np.nanmean(d_raw)),
                              med_raw=float(np.nanmedian(d_raw)),
                              mean_ded=float(np.nanmean(d_ded)) if len(d_ded) else np.nan,
                              med_ded=float(np.nanmedian(d_ded)) if len(d_ded) else np.nan,
                              sign_flip_raw=bool(np.sign(np.nanmean(d_raw))
                                                 != np.sign(np.nanmedian(d_raw))),
                              sign_flip_ded=bool(len(d_ded) and np.sign(np.nanmean(d_ded))
                                                 != np.sign(np.nanmedian(d_ded)))))
    C = pd.DataFrame(crows)
    C.to_csv(f"{OUT}.meanmedian.csv", index=False)
    say("")
    say("      panel  bar      K_raw K_ded   mean_raw  med_raw   mean_ded  med_ded  flip_raw")
    for _, r in C.iterrows():
        say(f"      {r.panel:6s} {r.bar:8s} {r.K_raw:5d} {r.K_ded:5d}  {r.mean_raw:9.4f} "
            f"{r.med_raw:8.4f}  {r.mean_ded:9.4f} {r.med_ded:8.4f}  {str(r.sign_flip_raw)}")
    flips = int(C.sign_flip_raw.sum())
    say("")
    say(f"    MEAN and MEDIAN over the RAW candidate set disagree in SIGN at {flips} of "
        f"{len(C)} (panel, bar) readings.")

    # ------------------------------------------------------------------ ARM D: the text census
    say("")
    say("=" * 110)
    say("ARM D — THE CENSUS OF THE RECORD'S COMMITTED 'WE WALKED N ALTERNATIVES' CLAIMS")
    say("=" * 110)
    U, nmd = units()
    X = census(U)
    X.to_csv(f"{OUT}.census.csv", index=False)
    say("")
    say(f"    {len(U)} committed text units over LEADERBOARD.md + CHANGELOG.md + {nmd} .md")
    say("    files in research/backtests/.")
    say("")
    say("      claim set   units   state a COUNT   name an AXIS   name GROSS   median stated N")
    for cs in CLAIM_SETS:
        z = X[X[cs]]
        if not len(z):
            continue
        say(f"      {cs:10s} {len(z):6d}   {int(z.n_counts.gt(0).sum()):13d}   "
            f"{int(z.n_axes.gt(0).sum()):12d}   {int(z.names_GROSS.sum()):10d}   "
            f"{np.nanmedian(z.stated_N):.1f}")
    zs = X[X.CS_STRICT]
    gross_share = float(zs.names_GROSS.mean()) if len(zs) else np.nan
    say("")
    say(f"    OF THE {len(zs)} CS_STRICT WALK CLAIMS, {int(zs.names_GROSS.sum())} "
        f"({gross_share:.4f}) NAME THE GROSS AXIS — i.e. that share of the record's adjudicated")
    say("    walks has a candidate set that provably contains the degenerate ladder.")

    # effective N each claim actually had, using the rebuildable ladders it names
    say("")
    say("    EFFECTIVE N EACH CLAIM ACTUALLY HAD.  For every CS_STRICT claim naming at least one")
    say("    of the record's four ladders, the candidate set is rebuilt from those ladders and")
    say("    its N_eff measured on this tape (median over the three panels).  Claims naming no")
    say("    rebuildable ladder are NOT given a number — they are reported as UNRESOLVABLE.")
    axis_neff = {}
    for bn, b in BARS.items():
        for axes in [frozenset(s) for s in
                     [{"N"}, {"H"}, {"GROSS"}, {"CADENCE"}, {"N", "H"}, {"N", "GROSS"},
                      {"H", "GROSS"}, {"N", "CADENCE"}, {"GROSS", "CADENCE"}, {"H", "CADENCE"},
                      {"N", "H", "GROSS"}, {"N", "H", "CADENCE"}, {"N", "GROSS", "CADENCE"},
                      {"H", "GROSS", "CADENCE"}, {"N", "H", "GROSS", "CADENCE"}]]:
            ks = []
            for a in sorted(axes):
                ks += [(a, r) for r in LAD[a]]
            ks = [k for k in ks if k == INC or k not in ANCH_KEYS] or ks
            ks = list(dict.fromkeys(ks))
            vv = [np.median([Sfull[(p.name, k)] for p in panels]) for k in ks]
            per_panel = [n_eff_sl([Sfull[(p.name, k)] for k in ks], b)[0] for p in panels]
            axis_neff[(bn, axes)] = (len(ks), float(np.median(per_panel)))
    erows = []
    for _, r in zs.iterrows():
        axes = frozenset(a for a in LADS if a in str(r["axes"]).split("|"))
        for bn in BARS:
            if not axes:
                erows.append(dict(uid=r.uid, bar=bn, stated_N=r.stated_N, K=np.nan,
                                  N_eff=np.nan, resolvable=False))
            else:
                K, ne = axis_neff[(bn, axes)]
                erows.append(dict(uid=r.uid, bar=bn, stated_N=r.stated_N, K=K, N_eff=ne,
                                  resolvable=True))
    E = pd.DataFrame(erows)
    E.to_csv(f"{OUT}.effective_n.csv", index=False)
    say("")
    say("      bar       CS_STRICT   resolvable   median stated N   median K   median N_eff   "
        "N_eff/K")
    for bn in BARS:
        z = E[E.bar == bn]
        zr = z[z.resolvable]
        if not len(z):
            continue
        say(f"      {bn:9s} {len(z):9d}   {len(zr):10d}   "
            f"{np.nanmedian(z.stated_N):15.1f}   {np.nanmedian(zr.K):8.1f}   "
            f"{np.nanmedian(zr.N_eff):12.1f}   "
            f"{(np.nanmedian(zr.N_eff)/np.nanmedian(zr.K) if len(zr) else np.nan):.4f}")

    # ------------------------------------------------------------------ ARM E: rule 8, capital
    say("")
    say("=" * 110)
    say("ARM E — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (does DE-CLONING buy anything?)")
    say("=" * 110)
    say("")
    say("    (E1) Every rung book on the full sample and on 2017-2026, 4a vs live RULES v2 and")
    say("         4b vs SPY, all grid points reported.")
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
    for p in [q.name for q in panels]:
        s, l = BM[(p, "SPY")], BM[(p, "LIVE")]
        so, lo_ = BM[(p, "SPY_OOS")], BM[(p, "LIVE_OOS")]
        say(f"         {p:6s} SPY full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
            f"   OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:8.2%}")
        say(f"         {p:6s} LIVE v2  {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
            f"   OOS {lo_['CAGR']:7.2%} / {lo_['Sharpe']:.4f} / {lo_['MaxDD']:8.2%}")

    say("")
    say("    (E2) THE CHOOSER ON TRIAL, RUN WALK-FORWARD.  For every (panel, ladder) the IS")
    say("         Sharpe argmax is taken on the IS window ONLY (warm-up .. 2016-12-31) and the")
    say("         2017-2026 return is read ONCE.  RAW = choose over all rungs.  DEDUP(b) =")
    say("         choose only among one representative per IS clone cluster at bar b (the")
    say("         representative rule is IS-only and never peeks at 2017+).  If the record's")
    say("         candidate sets are half clones AND that costs anything, DEDUP must pay.")
    wrows = []
    for pan in panels:
        i0, io = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = BM[(pan.name, "SPY_OOS")], BM[(pan.name, "LIVE_OOS")]
        Sis = {k: sharpe(booked[pan.name][k][i0:io]) for k in BOOKKEY}
        for lad in LADS + ["UNION"]:
            keys = ALT if lad == "UNION" else [(lad, r) for r in LAD[lad]]
            for mode in ["RAW"] + [f"DEDUP:{bn}" for bn in BARS]:
                if mode == "RAW":
                    cand = keys
                else:
                    cand = reps_sl(keys, [Sis[k] for k in keys], BARS[mode.split(":")[1]])
                if not cand:
                    continue
                ch = max(cand, key=lambda k: (Sis[k] if np.isfinite(Sis[k]) else -np.inf))
                rr = booked[pan.name][ch]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
                wrows.append(dict(panel=pan.name, ladder=lad, mode=mode, K=len(keys),
                                  K_cand=len(cand), chosen=akey(ch), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o))
        # do-nothing reference
        rr = booked[pan.name][INC]
        k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
        _, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
        wrows.append(dict(panel=pan.name, ladder="NONE", mode="DO_NOTHING", K=0, K_cand=0,
                          chosen=akey(INC), **m, H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                          OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a,
                          KEEP_4b=k4b, KEEP_4b_OOS=k4b_o))
    W8 = pd.DataFrame(wrows)
    W8.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("")
    say(f"         RULE-8 ROWS: {len(W8)}.  4a {int(W8.KEEP_4a.sum())}; 4b full "
        f"{int(W8.KEEP_4b.sum())}; 4b OOS {int(W8.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())}.")
    dn = float(W8[W8["mode"] == "DO_NOTHING"].OOS_Sharpe.mean())
    say("")
    say(f"         Mean OOS Sharpe by chooser mode (DO_NOTHING = {dn:.4f}):")
    for mode in ["RAW"] + [f"DEDUP:{bn}" for bn in BARS]:
        z = W8[W8["mode"] == mode]
        say(f"           {mode:14s} {z.OOS_Sharpe.mean():.4f}  over {len(z)} rows, "
            f"{z.chosen.nunique()} distinct books, mean candidates {z.K_cand.mean():.2f}")
    say("")
    say("         Per (panel, ladder): RAW pick vs DEDUP:B_TIGHT pick and their OOS Sharpes.")
    for _, r in W8[W8["mode"] == "RAW"].iterrows():
        d = W8[(W8.panel == r.panel) & (W8.ladder == r.ladder)
               & (W8["mode"] == "DEDUP:B_TIGHT")]
        if not len(d):
            continue
        d = d.iloc[0]
        flag = "   <-- pick MOVES" if d.chosen != r.chosen else ""
        say(f"           {r.panel:6s} {r.ladder:8s} RAW {r.chosen:12s} OOS S {r.OOS_Sharpe:.4f}"
            f"   DEDUP {d.chosen:12s} OOS S {d.OOS_Sharpe:.4f}{flag}")
    both = W8[W8.KEEP_4b & W8.KEEP_4b_OOS]
    if len(both):
        rk = sorted({(r.panel, round(r.OOS_CAGR, 8), round(r.OOS_Sharpe, 8))
                     for _, r in both.iterrows()})
        say("")
        say(f"         The {len(both)} both-4b rule-8 rows collapse to {len(rk)} DISTINCT "
            "realised books:")
        for p, c, s in rk:
            m0 = both[(both.panel == p) & (both.OOS_CAGR.round(8) == c)].iloc[0]
            say(f"           {p:6s} {m0.chosen:12s} full {m0.CAGR:7.2%} / {m0.Sharpe:.4f} / "
                f"{m0.MaxDD:8.2%}  halves {m0.H1:.4f}/{m0.H2:.4f}  OOS {m0.OOS_CAGR:7.2%} / "
                f"{m0.OOS_Sharpe:.4f} / {m0.OOS_MaxDD:8.2%}")

    # ------------------------------------------------------------------ verdict
    say("")
    say("=" * 110)
    say("VERDICT")
    say("=" * 110)
    if maj_deg > 0.50:
        outcome = "(A) EVERY AXIS"
    elif share_g.max() <= 0.30 and share_ng.min() >= 0.80:
        outcome = "(B) GROSS ONLY"
    else:
        outcome = "(C) MIXED"
    say("")
    say(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    say(f"      At the record's own bar {BARS['B_TIGHT']}: GROSS clone-free share median "
        f"{np.median(share_g):.3f}; non-GROSS median {np.median(share_ng):.3f}, with "
        f"{maj_deg:.3f} of the {len(share_ng)} non-GROSS cells at or below 0.60.")
    say(f"      Bar-free cross-check: GROSS N_eff^PR max {g_cells.N_eff_PR.max():.3f} against a")
    say(f"      non-GROSS N_eff^PR range "
        f"{ng_cells.N_eff_PR.min():.3f}-{ng_cells.N_eff_PR.max():.3f}.")
    ded_gain = (W8[W8["mode"] == "DEDUP:B_TIGHT"].OOS_Sharpe.mean()
                - W8[W8["mode"] == "RAW"].OOS_Sharpe.mean())
    say("")
    say(f"    CAPITAL.  De-cloning the candidate set moves mean OOS Sharpe by {ded_gain:+.4f} "
        "against")
    say("    the RAW chooser; the do-nothing anchor is the reference above.  4a "
        f"{int(BK.KEEP_4a.sum())} of {len(BK)} books and {int(W8.KEEP_4a.sum())} of {len(W8)}")
    say(f"    rule-8 rows; 4b BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books / "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())} rule-8 rows, collapsing to books the")
    say("    record already holds.  NO NEW BOOK, NO RULES CHANGE, NO PROTOCOL EDIT FROM THIS RUN.")
    say("")
    say("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the")
    say("    current constituents of a sub-$2B screen with max_1d_move >= 1.0 names dropped.")
    say("    Every LEVEL here is optimistic.  It largely cancels out of the headline, which is a")
    say("    RATIO of one construction against itself on the same tape (N_eff / K on the same")
    say("    books), and it does NOT cancel out of the 4b legs, so those passes are upper bounds.")

    GD = pd.DataFrame(GATES)
    GD.to_csv(f"{OUT}.gates.csv", index=False)
    say("")
    say(f"    GATES: {int(GD.pass_.sum())} of {len(GD)} pass.")
    for _, r in GD.iterrows():
        say(f"      {'PASS' if r.pass_ else 'FAIL'}  {r.gate}  value={r.value}  "
            f"target={r.target}")
    say("")
    say(f"    runtime {time.time()-t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
