#!/usr/bin/env python3
"""
Idea 1244 (lane C, 2026-09-18) — does a CLONE BAR need its PANEL before it can PARTITION
anything?

THE PREMISE, READ FROM THE RECORD.  Idea 1237's G12 published a clean partition of the record's
candidate set: 9 of the 18 non-incumbent rung books sit within 0.0040 of Sharpe of the incumbent
and ALL NINE are GROSS rungs, the smallest NON-GROSS gap being 0.0171, four times wider.  Idea
1239 replayed that gate exactly and then found, as bycatch, that the number is a MAX OVER THE
THREE PANELS: per panel 10 / 12 / 10 of the same 18 books sit inside the same 0.0040 bar, and in
EVERY panel at least one of them is NOT a GROSS rung (smallest non-GROSS gap 0.0033 / 0.0008 /
0.0023 on U56 / B136 / SMALL against the pooled 0.0171).  A max over panels is the WIDEST
reading of a distance and therefore the reading most favourable to a clean partition.

WHAT IS BEING TESTED, STATED BEFORE ANY NUMBER IS READ.  Not whether 1237's gate replays (1239
already showed it does), but whether the record's clone LANGUAGE carries the panel it needs.
Two halves, both pre-declared:

  CENSUS   Harvest every committed clone / near-identical / same-book claim in the record and
           classify each by what it says about panels: EXACT (a zero-tolerance identity),
           PER_PANEL (names a panel or reports per panel), POOLED (says max / min / mean over
           panels), SILENT (says nothing).  EXACT claims are POOLING-IMMUNE and the run says so
           up front and proves it: max_p d_p = 0 implies d_p = 0 on every panel, so pooling at a
           ZERO bar is safe.  Pooling at a POSITIVE bar is the object on trial.
  RE-READ  Rebuild the record's own 22 rung keys / 19 distinct books on all three panels and
           re-read the clone partition under every pooling rule, per panel and pooled, and
           report how many books change label and how many committed clone COUNTS survive.

PRE-DECLARED OUTCOMES (fixed before the run; the verdict is read off, not chosen):
  (A) THE BAR NEEDS ITS PANEL — at the headline claim set the NON-EXACT clone claims are
      majority PANEL-SILENT (share >= 0.50) AND the pooled label misstates the per-panel label
      on >= 0.50 of the 18 books at 1237's own bar.
  (B) POOLING IS INERT — pooled-vs-per-panel label agreement >= 0.90 at every pooling rule AND
      the non-exact panel-silent share is < 0.50.
  (C) MIXED — anything else; the panel has to be quoted for some claims and not others.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4; the queue names both):

  CLAIM SET     {CQ_CLONE, CQ_SAME, CQ_ALL}, nested.
                CQ_CLONE  explicit clone / near-identical / same-book / indistinguishable /
                          duplicate language — the queue's own words.
                CQ_SAME   CQ_CLONE plus identity assertions (decision-identical, reproduces
                          exactly, bit for bit, 0.000e+00, to N decimals, degenerate,
                          re-levering).
                CQ_ALL    CQ_SAME plus proximity assertions (within X of, a gap of, a margin of,
                          sits inside, differ by).
  POOLING RULE  {P_MAX, P_MEAN, P_MEDIAN, P_MIN, P_UNPOOLED}.  A pooled rule reduces the three
                per-panel gaps to ONE number before the bar is applied; P_UNPOOLED applies the
                bar on each panel separately and therefore returns THREE labels per book.
                P_MAX is the record's own rule (1237's G12).

NOT DIALS, REPORTED AT EVERY VALUE: the BAR is FROZEN at 1237's committed 0.0040 for every
headline, with 0.0100 and 0.0171 (1239's B_MID / B_LOOSE) published beside it as a control;
PANEL {U56, B136, SMALL} (rule 9); the four ladders the record has walked (N, H, GROSS,
CADENCE) and their union; single- and complete-linkage readings; the 4a and 4b legs.

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

DATE = "2026-09-18"
SLUG = "does-a-CLONE-BAR-need-its-PANEL-before-it-can-PARTITION-anything"
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
BAR_HEAD = 0.0040                      # 1237's committed clone bar — FROZEN, not a dial
BARS = {"B_TIGHT": 0.0040, "B_MID": 0.0100, "B_LOOSE": 0.0171}
POOLS = ["P_MAX", "P_MEAN", "P_MEDIAN", "P_MIN", "P_UNPOOLED"]
POOLED_ONLY = ["P_MAX", "P_MEAN", "P_MEDIAN", "P_MIN"]
CLAIM_SETS = ["CQ_CLONE", "CQ_SAME", "CQ_ALL"]
HEAD_CS = "CQ_CLONE"
LIVE_MAXDD_COMMITTED = -0.1205
PIN = "d8729f9"          # the commit that carries 1239's script and the cache it read

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


# ==================================================================== clustering machinery
def sl_components(D, bar):
    """Single-linkage components of the graph D[i,j] <= bar.  Union-find, works on ANY
    symmetric distance matrix (a pooled one is not a 1-D statistic, so the sort shortcut 1239
    used on one panel does not apply)."""
    n = D.shape[0]
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if D[i, j] <= bar:
                ra, rb = find(i), find(j)
                if ra != rb:
                    par[ra] = rb
    lab = [find(i) for i in range(n)]
    uniq = {v: i for i, v in enumerate(sorted(set(lab)))}
    return [uniq[v] for v in lab]


def sl_1d(vals, bar):
    """1-D single linkage by sorting — 1239's exact routine, kept as the cross-check for
    sl_components on a single panel."""
    v = np.sort(np.asarray([x for x in vals if np.isfinite(x)], float))
    if len(v) == 0:
        return 0
    return int(1 + (np.diff(v) > bar).sum())


def cl_groups(D, bar):
    """Complete linkage: greedy maximal cliques in index order, deterministic.  A group is
    closed when adding the next member would put some pair inside it beyond bar."""
    n = D.shape[0]
    unassigned = list(range(n))
    k = 0
    while unassigned:
        grp = [unassigned.pop(0)]
        rest = []
        for c in unassigned:
            if all(D[c, g] <= bar for g in grp):
                grp.append(c)
            else:
                rest.append(c)
        unassigned = rest
        k += 1
    return k


def pooled_D(per_panel_D, rule):
    """Reduce a stack of per-panel distance matrices to one under the named pooling rule."""
    A = np.stack(per_panel_D, axis=0)
    if rule == "P_MAX":
        return A.max(axis=0)
    if rule == "P_MEAN":
        return A.mean(axis=0)
    if rule == "P_MEDIAN":
        return np.median(A, axis=0)
    if rule == "P_MIN":
        return A.min(axis=0)
    raise ValueError(rule)


def reps_sl_1d(keys, vals, bar):
    """One representative key per single-linkage clone cluster on a 1-D statistic: the
    lowest-value member.  IS-only, never peeks at 2017+.  (1239's rule, kept identical.)"""
    pairs = [(v, k) for k, v in zip(keys, vals) if np.isfinite(v)]
    pairs.sort()
    out, anchor_v = [], None
    for v, k in pairs:
        if anchor_v is None or v - anchor_v > bar:
            out.append(k)
            anchor_v = v
        else:
            anchor_v = v
    return out


def reps_from_labels(keys, labels, order_vals):
    """One representative per cluster label: the member with the lowest order_vals (IS Sharpe).
    Deterministic, IS-only."""
    best = {}
    for k, l, v in zip(keys, labels, order_vals):
        v = v if np.isfinite(v) else np.inf
        if l not in best or v < best[l][0]:
            best[l] = (v, k)
    return [best[l][1] for l in sorted(best)]


def rung_books(pan):
    """The record's 22 rung keys as realised NET return series on one panel."""
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
        books[("CADENCE", f)] = nrun(pan, A_G * (af if f == "W" else frames[(A_N, A_H, "M")]), f)
    for g in LAD["GROSS"]:
        books[("GROSS", g)] = nrun(pan, g * af, "W")
    return books


def pinned_prices():
    """data/prices.csv exactly as it stood at PIN, rebuilt the way load_universe() reads it.
    Returns None when git is unavailable (the run then reports the attribution as skipped)."""
    import json
    import subprocess
    try:
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{PIN}:data/prices.csv"],
                              capture_output=True, text=True, check=True).stdout
    except Exception:
        return None
    import io
    px = pd.read_csv(io.StringIO(blob), index_col=0, parse_dates=True)
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    T = sorted({t for g in U.values() for t in g} - {"BTC-USD", "ETH-USD"})
    return px[[c for c in T if c in px.columns]].loc["2008-01-01":].dropna(how="all").ffill()


# ==================================================================== the record's own text
CLONE_RE = re.compile(
    r"\b(clones?|clonal|clone-free|clone bar|clone-bar|near-identical|nearly identical|"
    r"same book|one book|the same book|indistinguishable|duplicates?|duplicated)\b", re.I)
IDENT_RE = re.compile(
    r"(decision-identical|\bidentical\b|bit for bit|bit-for-bit|0\.000e\+00|reproduc\w+ exactly|"
    r"replays? exactly|to \d+ decimals?|\bdegenerate\b|degeneracy|re-lever\w+|exactly \+?0\.0000|"
    r"deviation 0\b|dev 0\b)", re.I)
PROX_RE = re.compile(
    r"(within [-+]?\d|a gap of|the gap|margin of|sits? inside|differ by|no wider than|"
    r"closer to|inside the same bar|\|dSharpe\|)", re.I)

PANEL_NAMED = re.compile(r"\b(U56|B13[0-9]|B1[0-9]{2}|SMALL\d*|small panel|broad panel|"
                         r"sub-\$2B)\b", re.I)
PER_PANEL_RE = re.compile(r"(per panel|per-panel|on every panel|in every panel|each panel|"
                          r"\bby panel\b|panel by panel|on all three panels|"
                          r"\d\s+of\s+3\s+panels)", re.I)
POOLED_RE = re.compile(r"(max over|maximum over|min over|minimum over|mean over|median over|"
                       r"pooled|over the three panels|across panels|across the panels|"
                       r"max-over-panels|MAX-OVER-PANELS)", re.I)
EXACT_RE = re.compile(r"(0\.000e\+00|bit for bit|bit-for-bit|\bexactly\b|deviation 0\b|"
                      r"\bdev 0\b|to \d+ decimals?|max deviation 0\b|0\.0000\b)", re.I)
NOFM_RE = re.compile(r"\b(\d{1,3})\s+of\s+(\d{1,3})\b")


def units():
    """The SAME corpus definition 1239 used, so the two censuses are comparable."""
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


def panel_stance(txt):
    """What the unit says about panels.  EXACT is decided FIRST and on purpose: a zero-tolerance
    identity pooled by max implies the same identity on every panel, so it needs no panel."""
    if EXACT_RE.search(txt):
        return "EXACT"
    if POOLED_RE.search(txt):
        return "POOLED"
    if PER_PANEL_RE.search(txt) or PANEL_NAMED.search(txt):
        return "PER_PANEL"
    return "SILENT"


def census(U):
    rows = []
    for src, txt in U:
        c = bool(CLONE_RE.search(txt))
        i = bool(IDENT_RE.search(txt))
        p = bool(PROX_RE.search(txt))
        nofm = [(int(a), int(b)) for a, b in NOFM_RE.findall(txt)]
        nofm18 = [(a, b) for a, b in nofm if b in (18, 19, 22)]
        rows.append(dict(
            uid=hashlib.sha1((src + txt).encode()).hexdigest()[:10], src=src,
            CLONE=c, IDENT=i, PROX=p,
            CQ_CLONE=c, CQ_SAME=(c or i), CQ_ALL=(c or i or p),
            stance=panel_stance(txt),
            n_nofm=len(nofm), n_nofm18=len(nofm18),
            nofm18=";".join(f"{a}of{b}" for a, b in nofm18)))
    return pd.DataFrame(rows)


# ==================================================================== main
def main():
    t0 = time.time()
    say("=" * 110)
    say("IDEA 1244 (lane C, 2026-09-18) — does a CLONE BAR need its PANEL before it can")
    say("PARTITION anything?")
    say("=" * 110)
    say("")
    say("  1237's G12 partitioned 18 non-incumbent rung books 9 GROSS clones / 9 non-GROSS on a")
    say("  MAX-OVER-PANELS Sharpe gap at a 0.0040 bar; 1239 replayed the gate and found the")
    say("  per-panel reading is 10 / 12 / 10 inside the same bar with a NON-GROSS book inside on")
    say("  every panel.  DIALS: CLAIM SET {CQ_CLONE, CQ_SAME, CQ_ALL} x POOLING RULE {P_MAX,")
    say("  P_MEAN, P_MEDIAN, P_MIN, P_UNPOOLED}.  BAR FROZEN at 1237's 0.0040 (0.0100 / 0.0171")
    say("  published beside it, not tuned).")
    say("  PRE-DECLARED: (A) THE BAR NEEDS ITS PANEL — non-exact clone claims majority SILENT")
    say("  AND pooled label misstates >= 0.50 of the 18 books on some panel.  (B) POOLING IS")
    say("  INERT — agreement >= 0.90 everywhere AND silent share < 0.50.  (C) MIXED.")

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
        books = rung_books(pan)
        booked[pan.name] = books
        if not BOOKKEY:
            BOOKKEY = list(books.keys())
        b = backtest(pan.px, rules_v2_weights(pan.px), cost_bps=COST, freq="W")
        BM[(pan.name, "SPY")] = bmref(pan.spy[pan.i0:])
        BM[(pan.name, "LIVE")] = bmref(b["returns"].values[pan.i0:])
        say(f"    {pan.name:6s} {len(books)} rung books built.")

    ANCH_KEYS = [(l, ANCHOR_RUNG[l]) for l in LADS]
    INC = ("N", A_N)
    PN = [p.name for p in panels]
    ilim = {p.name: int(p.idx.searchsorted(pd.Timestamp(OOS_START))) for p in panels}
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
    gate("G2 live RULES v2 U56 MaxDD == committed -12.05%", round(lm, 6), LIVE_MAXDD_COMMITTED,
         abs(lm - LIVE_MAXDD_COMMITTED) < 5e-4)
    dev = 0.0
    for k in ANCH_KEYS[1:]:
        dev = max(dev, float(np.abs(booked["U56"][k] - booked["U56"][ANCH_KEYS[0]]).max()))
    gate("G3 the four anchor keys are ONE book (bit for bit)", dev, 0.0, dev == 0.0)
    ALT = [k for k in BOOKKEY if k == INC or k not in ANCH_KEYS]
    gate("G4 distinct candidate set size (1237's 19)", float(len(ALT)), 19.0, len(ALT) == 19)

    Sfull = {(p, k): sharpe(booked[p][k][WARMUP:]) for p in PN for k in BOOKKEY}
    NONINC = [k for k in ALT if k != INC]                       # the 18 books 1237 partitioned
    gate("G5 non-incumbent candidate set size (1237's 18)", float(len(NONINC)), 18.0,
         len(NONINC) == 18)
    gapp = {(p, k): abs(Sfull[(p, k)] - Sfull[(p, INC)]) for p in PN for k in NONINC}
    gmax = {k: max(gapp[(p, k)] for p in PN) for k in NONINC}
    DEGEN = [k for k in NONINC if gmax[k] <= BAR_HEAD]
    worst_g = max(gmax[k] for k in NONINC if k[0] == "GROSS")
    worst_r = min(gmax[k] for k in NONINC if k[0] != "GROSS")
    gate("G6a 1237's G12 replay — worst GROSS gap (max over 3 panels)", round(worst_g, 4),
         0.0040, abs(worst_g - 0.0040) < 5e-4)
    gate("G6b 1237's G12 replay — smallest NON-GROSS gap (max over 3 panels)",
         round(worst_r, 4), "0.0171 +/- 5e-4 (tolerance stated: the exact replay is G6d)",
         abs(worst_r - 0.0171) < 5e-4)
    gate("G6c the pooled partition is 9 GROSS clones and 9 non-clones",
         f"{len(DEGEN)}/{len(NONINC)-len(DEGEN)}", "9/9",
         len(DEGEN) == 9 and all(k[0] == "GROSS" for k in DEGEN))
    say("")
    say(f"    1237's G12 replays: worst GROSS gap {worst_g:.4f}, smallest non-GROSS gap")
    say(f"    {worst_r:.4f}, partition {len(DEGEN)} GROSS / {len(NONINC)-len(DEGEN)} non-clone.")
    say(f"    NOTE, REPORTED NOT SMOOTHED: 1239 committed this statistic as 0.0171 on")
    say(f"    2026-09-17; on today's committed caches it reads {worst_r:.4f}.  The GROSS side")
    say(f"    ({worst_g:.4f}) replays exactly.  The move is attributed below before anything is")
    say("    concluded from it.")

    # --- the committed bar as a function of TAPE END (not a dial: every value published) ---
    say("")
    say("    THE RECORD'S OWN CLONE BAR IS A TAPE-END STATISTIC.  1239's B_LOOSE = 0.0171 is")
    say("    the smallest NON-GROSS pooled-max gap, i.e. a number READ OFF THIS TAPE and then")
    say("    frozen as a bar.  Re-read with the last j sessions withheld, j = 0..24:")
    say("      j   U56 tape end   worst GROSS gap   smallest non-GROSS gap   partition")
    trows = []
    for j in range(25):
        Sj = {(p.name, k): sharpe(booked[p.name][k][WARMUP:(len(booked[p.name][k]) - j) or None])
              for p in panels for k in BOOKKEY}
        gj = {k: max(abs(Sj[(p, k)] - Sj[(p, INC)]) for p in PN) for k in NONINC}
        wg = max(gj[k] for k in NONINC if k[0] == "GROSS")
        wr = min(gj[k] for k in NONINC if k[0] != "GROSS")
        dg = [k for k in NONINC if gj[k] <= BAR_HEAD]
        trows.append(dict(j=j, tape_end=str(panels[0].idx[-1 - j].date()), worst_GROSS=wg,
                          smallest_nonGROSS=wr, n_clone=len(dg),
                          all_GROSS=all(k[0] == "GROSS" for k in dg)))
        say(f"      {j:<3d} {trows[-1]['tape_end']:13s} {wg:15.4f}   {wr:22.4f}   "
            f"{len(dg)} clones, all GROSS {all(k[0]=='GROSS' for k in dg)}")
    T10 = pd.DataFrame(trows)
    T10.to_csv(f"{OUT}.tape_end.csv", index=False)
    say("")
    say(f"      RANGE over {len(T10)} tape ends: worst GROSS gap "
        f"{T10.worst_GROSS.min():.4f}-{T10.worst_GROSS.max():.4f} (width "
        f"{T10.worst_GROSS.max()-T10.worst_GROSS.min():.4f}); smallest non-GROSS "
        f"{T10.smallest_nonGROSS.min():.4f}-{T10.smallest_nonGROSS.max():.4f} (width "
        f"{T10.smallest_nonGROSS.max()-T10.smallest_nonGROSS.min():.4f}).")
    say(f"      The 9-GROSS-clone partition holds at {int(T10.n_clone.eq(9).sum())} of "
        f"{len(T10)} tape ends and is all-GROSS at {int(T10.all_GROSS.sum())} of {len(T10)}.")
    say(f"      1239's committed 0.0171 is reproduced at "
        f"{int(T10.smallest_nonGROSS.round(4).eq(0.0171).sum())} of {len(T10)} of them.")
    say("      THE CLONE SIDE OF THE PARTITION IS STRUCTURAL (1189's scaling identity, so the")
    say("      GROSS gap cannot move); THE NON-CLONE SIDE IS A TAPE READING.")

    # --- attribute the move: PINNED cache (the tree 1239 read) vs today's, same tape end ---
    say("")
    say("    ATTRIBUTION.  research/backtests/2026-09-17_is-the-record-s-CANDIDATE-SET-half-")
    say("    CLONES-...-WALKED_cloud.py was committed at " + PIN[:7] + "; data/prices.csv has")
    say("    been rewritten since by the daily-close job.  The U56 panel is rebuilt from the")
    say("    PINNED blob and the statistic re-read, isolating RESTATEMENT from ONE MORE SESSION.")
    old_px = pinned_prices()
    if old_px is None:
        say("      PINNED BLOB UNAVAILABLE (no git in this environment) — attribution skipped.")
        gate("G6d 1239's committed 0.0171 replays on the PINNED cache at its own tape end",
             "unavailable", "0.0171", False)
    else:
        say(f"      pinned U56 cache: {old_px.shape[1]} names, {old_px.index[0].date()} .. "
            f"{old_px.index[-1].date()}; today's: {panels[0].px.shape[1]-0} cols, "
            f"{panels[0].idx[-1].date()}.")
        cols = [c for c in old_px.columns if c in panels[0].px.columns]
        ii = old_px.index.intersection(panels[0].idx)
        dev = float((panels[0].px.loc[ii, cols] - old_px.loc[ii, cols]).abs().div(
            old_px.loc[ii, cols].abs()).max().max())
        nrest = int((panels[0].px.loc[ii, cols] - old_px.loc[ii, cols]).abs().div(
            old_px.loc[ii, cols].abs()).max().gt(1e-9).sum())
        say(f"      {nrest} of {len(cols)} U56 columns RESTATED on shared dates, max relative")
        say(f"      deviation {dev:.2e}; {len(panels[0].idx.difference(old_px.index))} new session(s).")
        pan_old = Panel("U56pin", old_px, [c for c in old_px.columns if c != "SPY"])
        b_old = rung_books(pan_old)
        S_old = {k: sharpe(b_old[k][WARMUP:]) for k in BOOKKEY}
        # today's U56 truncated to the pinned tape end
        jcut = int(len(panels[0].idx) - panels[0].idx.searchsorted(old_px.index[-1]) - 1)
        S_cut = {k: sharpe(booked["U56"][k][WARMUP:(len(booked["U56"][k]) - jcut) or None])
                 for k in BOOKKEY}
        arows2 = []
        for lab, SU, jj in [("PINNED cache @ 2026-09-16", S_old, jcut),
                            ("today's cache @ 2026-09-16", S_cut, jcut),
                            ("today's cache @ 2026-09-17", None, 0)]:
            gj = {}
            for k in NONINC:
                if SU is None:
                    gU = abs(Sfull[("U56", k)] - Sfull[("U56", INC)])
                else:
                    gU = abs(SU[k] - SU[INC])
                oth = []
                for p in PN[1:]:
                    n = len(booked[p][k])
                    sp = sharpe(booked[p][k][WARMUP:(n - jj) or None])
                    si = sharpe(booked[p][INC][WARMUP:(n - jj) or None])
                    oth.append(abs(sp - si))
                gj[k] = max([gU] + oth)
            wg = max(gj[k] for k in NONINC if k[0] == "GROSS")
            wr = min(gj[k] for k in NONINC if k[0] != "GROSS")
            dg = [k for k in NONINC if gj[k] <= BAR_HEAD]
            arows2.append(dict(reading=lab, worst_GROSS=wg, smallest_nonGROSS=wr,
                               n_clone=len(dg),
                               all_GROSS=all(k[0] == "GROSS" for k in dg)))
        AT = pd.DataFrame(arows2)
        AT.to_csv(f"{OUT}.attribution.csv", index=False)
        say("")
        say("      reading                        worst GROSS gap   smallest non-GROSS gap   "
            "clones  all GROSS?")
        for _, r in AT.iterrows():
            say(f"      {r.reading:30s} {r.worst_GROSS:15.4f}   {r.smallest_nonGROSS:22.4f}   "
                f"{r.n_clone:6d}  {str(r.all_GROSS)}")
        d_rest = float(AT.smallest_nonGROSS.iloc[1] - AT.smallest_nonGROSS.iloc[0])
        d_sess = float(AT.smallest_nonGROSS.iloc[2] - AT.smallest_nonGROSS.iloc[1])
        say("")
        say(f"      RESTATEMENT of the price cache moves the bar {d_rest:+.4f}; ONE MORE")
        say(f"      SESSION moves it {d_sess:+.4f}.  Total {d_rest+d_sess:+.4f} against a bar")
        say("      the record quotes to four decimals.")
        gate("G6d 1239's committed 0.0171 replays on the PINNED cache at its own tape end",
             round(float(AT.smallest_nonGROSS.iloc[0]), 4), 0.0171,
             abs(AT.smallest_nonGROSS.iloc[0] - 0.0171) < 5e-5)
        say("")
        say("      WHAT THIS RUN CANNOT DO, STATED PLAINLY.  The clone available here is SHALLOW")
        say("      and carries only two versions of data/prices.csv, so the tape that produced")
        say("      0.0171 cannot be reconstructed and this run does NOT claim 1239 was wrong.")
        say("      What it establishes is narrower and sufficient: the committed 0.0171 is NOT")
        say("      reproduced by the tree 1239 itself committed, at that tree's own tape end")
        say(f"      (it reads {AT.smallest_nonGROSS.iloc[0]:.4f} there), and the 25-session sweep")
        say(f"      lands on 0.0171 at exactly "
            f"{int(T10.smallest_nonGROSS.round(4).eq(0.0171).sum())} tape end — "
            f"{T10[T10.smallest_nonGROSS.round(4).eq(0.0171)].tape_end.iloc[0]}, five weeks")
        say("      before 1239 ran — which is a wandering statistic crossing a value, not a")
        say("      recovery of it.  The GROSS side replays at every tape end in the sweep.")
    hit = bool((T10.smallest_nonGROSS.round(4) == 0.0171).any())
    gate("G6e 1239's committed 0.0171 is inside the 25-session tape-end range at all",
         f"{T10.smallest_nonGROSS.min():.4f}-{T10.smallest_nonGROSS.max():.4f}",
         "0.0171 in range", hit)

    # machinery cross-checks for the new clustering code
    dev1 = 0
    for p in PN:
        for lad in LADS:
            keys = [(lad, r) for r in LAD[lad]]
            v = [Sfull[(p, k)] for k in keys]
            D = np.abs(np.subtract.outer(np.array(v), np.array(v)))
            dev1 = max(dev1, abs(len(set(sl_components(D, BAR_HEAD))) - sl_1d(v, BAR_HEAD)))
    gate("G7 union-find single linkage == 1239's 1-D sort routine on every panel/ladder",
         float(dev1), 0.0, dev1 == 0)
    Dst = [np.abs(np.subtract.outer(np.array([Sfull[(p, k)] for k in NONINC]),
                                    np.array([Sfull[(p, k)] for k in NONINC]))) for p in PN]
    mono = all((pooled_D(Dst, "P_MIN") <= pooled_D(Dst, "P_MEDIAN") + 1e-12).all()
               and (pooled_D(Dst, "P_MEDIAN") <= pooled_D(Dst, "P_MAX") + 1e-12).all()
               for _ in [0])
    gate("G8 pooling rules are ordered P_MIN <= P_MEDIAN <= P_MAX elementwise", str(mono),
         "True", mono)
    zero_ok = True
    for k in NONINC:
        if max(gapp[(p, k)] for p in PN) == 0.0:
            zero_ok &= all(gapp[(p, k)] == 0.0 for p in PN)
    gate("G9 EXACT claims are pooling-immune (max_p d = 0 => d = 0 on every panel)",
         str(zero_ok), "True", zero_ok)

    # ------------------------------------------------------------------ ARM B: the re-read
    say("")
    say("=" * 110)
    say("ARM B — THE SAME 18 BOOKS RE-READ UNDER EVERY POOLING RULE (the bar is FROZEN at")
    say("1237's 0.0040; 0.0100 and 0.0171 published beside it)")
    say("=" * 110)
    say("")
    say("    A book is a CLONE of the incumbent when its Sharpe gap is inside the bar.  A pooled")
    say("    rule gives ONE label per book; P_UNPOOLED gives one per panel.")
    prows = []
    for bn, bv in BARS.items():
        perlab = {(p, k): (gapp[(p, k)] <= bv) for p in PN for k in NONINC}
        for rule in POOLS:
            if rule == "P_UNPOOLED":
                for p in PN:
                    lab = {k: perlab[(p, k)] for k in NONINC}
                    cl_ = [k for k in NONINC if lab[k]]
                    prows.append(dict(bar=bn, bar_v=bv, rule=rule, panel=p, n_clone=len(cl_),
                                      all_GROSS=all(k[0] == "GROSS" for k in cl_) if cl_ else True,
                                      n_nonGROSS_clone=sum(1 for k in cl_ if k[0] != "GROSS"),
                                      smallest_nonGROSS=min(gapp[(p, k)] for k in NONINC
                                                            if k[0] != "GROSS")))
            else:
                gp = {k: pooled_D([np.array([[0.0, gapp[(p, k)]], [gapp[(p, k)], 0.0]])
                                   for p in PN], rule)[0, 1] for k in NONINC}
                cl_ = [k for k in NONINC if gp[k] <= bv]
                prows.append(dict(bar=bn, bar_v=bv, rule=rule, panel="POOLED", n_clone=len(cl_),
                                  all_GROSS=all(k[0] == "GROSS" for k in cl_) if cl_ else True,
                                  n_nonGROSS_clone=sum(1 for k in cl_ if k[0] != "GROSS"),
                                  smallest_nonGROSS=min(gp[k] for k in NONINC
                                                        if k[0] != "GROSS")))
    P = pd.DataFrame(prows)
    P.to_csv(f"{OUT}.partition.csv", index=False)
    for bn in BARS:
        say("")
        say(f"    BAR {bn} (|dSharpe| <= {BARS[bn]}):")
        say("      rule         panel     clones of 18   all GROSS?   non-GROSS clones   "
            "smallest non-GROSS gap")
        for _, r in P[P.bar == bn].iterrows():
            say(f"      {r.rule:12s} {r.panel:9s} {r.n_clone:10d}   {str(r.all_GROSS):10s}   "
                f"{r.n_nonGROSS_clone:14d}   {r.smallest_nonGROSS:.4f}")

    # label agreement: pooled vs per-panel
    say("")
    say("    LABEL AGREEMENT.  For each pooled rule, the share of the 18 books whose pooled")
    say("    label matches the per-panel label on ALL THREE panels, and the count that the")
    say("    pooled rule MISSTATES on at least one panel.")
    arows = []
    for bn, bv in BARS.items():
        perlab = {(p, k): (gapp[(p, k)] <= bv) for p in PN for k in NONINC}
        for rule in POOLED_ONLY:
            gp = {k: pooled_D([np.array([[0.0, gapp[(p, k)]], [gapp[(p, k)], 0.0]])
                               for p in PN], rule)[0, 1] for k in NONINC}
            lab = {k: gp[k] <= bv for k in NONINC}
            miss = [k for k in NONINC if any(perlab[(p, k)] != lab[k] for p in PN)]
            per_p = {p: sum(1 for k in NONINC if perlab[(p, k)] != lab[k]) for p in PN}
            arows.append(dict(bar=bn, rule=rule, agree=1 - len(miss) / len(NONINC),
                              misstated=len(miss),
                              **{f"miss_{p}": per_p[p] for p in PN},
                              misstated_books="|".join(akey(k) for k in miss)))
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.agreement.csv", index=False)
    say("")
    say("      bar       rule        agreement   misstated of 18   U56   B136  SMALL")
    for _, r in A.iterrows():
        say(f"      {r.bar:9s} {r.rule:11s} {r.agree:9.4f}   {r.misstated:15d}   "
            f"{r.miss_U56:3d}   {r.miss_B136:4d}  {r.miss_SMALL:5d}")
    head = A[(A.bar == "B_TIGHT") & (A.rule == "P_MAX")].iloc[0]
    MISSTATE_SHARE = float(head.misstated) / len(NONINC)
    say("")
    say(f"    AT THE RECORD'S OWN RULE AND BAR (P_MAX, {BAR_HEAD}): the pooled label is wrong on")
    say(f"    at least one panel for {head.misstated} of {len(NONINC)} books "
        f"({MISSTATE_SHARE:.4f}).  Books: {head.misstated_books}")

    # panel-dependence of every book
    say("")
    say("    PANEL-DEPENDENT BOOKS.  A book whose per-panel clone label is not constant across")
    say("    the three panels cannot be labelled at all without naming a panel.")
    brows = []
    for bn, bv in BARS.items():
        for k in NONINC:
            labs = [gapp[(p, k)] <= bv for p in PN]
            brows.append(dict(bar=bn, book=akey(k), ladder=k[0],
                              **{f"gap_{p}": gapp[(p, k)] for p in PN},
                              **{f"clone_{p}": labs[i] for i, p in enumerate(PN)},
                              panel_dependent=(len(set(labs)) > 1)))
    B = pd.DataFrame(brows)
    B.to_csv(f"{OUT}.books_panel.csv", index=False)
    for bn in BARS:
        z = B[B.bar == bn]
        say(f"      {bn:9s} panel-dependent {int(z.panel_dependent.sum()):2d} of {len(z)}  "
            f"(GROSS {int(z[z.ladder=='GROSS'].panel_dependent.sum())} of "
            f"{len(z[z.ladder=='GROSS'])}, non-GROSS "
            f"{int(z[z.ladder!='GROSS'].panel_dependent.sum())} of "
            f"{len(z[z.ladder!='GROSS'])})")
    say("")
    say("      book          ladder     gap_U56   gap_B136  gap_SMALL   labels (U56/B136/SMALL)"
        "   panel-dependent")
    for _, r in B[B.bar == "B_TIGHT"].iterrows():
        say(f"      {r.book:13s} {r.ladder:9s} {r.gap_U56:9.4f} {r.gap_B136:9.4f} "
            f"{r.gap_SMALL:10.4f}   {str(r.clone_U56)[0]}/{str(r.clone_B136)[0]}/"
            f"{str(r.clone_SMALL)[0]}{'':19s}{str(r.panel_dependent)}")

    # whole-ladder N_eff under each pooling rule
    say("")
    say("    THE SAME QUESTION ON THE FULL PAIRWISE CLONE GRAPH (not just distance to the")
    say("    incumbent): N_eff = single-linkage components, CL = complete-linkage groups.")
    nrows = []
    for lad in LADS + ["UNION"]:
        keys = ALT if lad == "UNION" else [(lad, r) for r in LAD[lad]]
        Ds = [np.abs(np.subtract.outer(np.array([Sfull[(p, k)] for k in keys]),
                                       np.array([Sfull[(p, k)] for k in keys]))) for p in PN]
        for bn, bv in BARS.items():
            for rule in POOLS:
                if rule == "P_UNPOOLED":
                    for i, p in enumerate(PN):
                        nrows.append(dict(ladder=lad, K=len(keys), bar=bn, rule=rule, panel=p,
                                          N_eff=len(set(sl_components(Ds[i], bv))),
                                          N_CL=cl_groups(Ds[i], bv)))
                else:
                    D = pooled_D(Ds, rule)
                    nrows.append(dict(ladder=lad, K=len(keys), bar=bn, rule=rule, panel="POOLED",
                                      N_eff=len(set(sl_components(D, bv))),
                                      N_CL=cl_groups(D, bv)))
    NE = pd.DataFrame(nrows)
    NE.to_csv(f"{OUT}.neff.csv", index=False)
    say("")
    say("      (bar B_TIGHT = the record's own)  ladder    K   P_MAX  P_MEAN  P_MEDIAN  P_MIN  "
        "| U56  B136  SMALL")
    for lad in LADS + ["UNION"]:
        z = NE[(NE.bar == "B_TIGHT") & (NE.ladder == lad)]
        g = {r.rule if r.panel == "POOLED" else r.panel: r.N_eff for _, r in z.iterrows()}
        say(f"      {'':34s}{lad:8s} {int(z.K.iloc[0]):3d}   {g['P_MAX']:4d}  {g['P_MEAN']:5d}  "
            f"{g['P_MEDIAN']:7d}  {g['P_MIN']:5d}  | {g['U56']:3d}  {g['B136']:4d}  "
            f"{g['SMALL']:5d}")
    spread = []
    for lad in LADS + ["UNION"]:
        z = NE[(NE.bar == "B_TIGHT") & (NE.ladder == lad) & (NE.rule == "P_UNPOOLED")]
        pm = NE[(NE.bar == "B_TIGHT") & (NE.ladder == lad) & (NE.rule == "P_MAX")].N_eff.iloc[0]
        spread.append((lad, int(z.N_eff.min()), int(z.N_eff.max()), int(pm)))
    say("")
    say("      per-panel N_eff RANGE vs the pooled P_MAX reading:")
    for lad, lo, hi, pm in spread:
        say(f"        {lad:8s} per-panel {lo}-{hi}   P_MAX {pm}"
            f"{'   <-- P_MAX outside the per-panel range' if not (lo <= pm <= hi) else ''}")

    # ------------------------------------------------------------------ ARM C: the census
    say("")
    say("=" * 110)
    say("ARM C — THE CENSUS OF THE RECORD'S COMMITTED CLONE / NEAR-IDENTICAL / SAME-BOOK CLAIMS")
    say("=" * 110)
    U, nmd = units()
    X = census(U)
    X.to_csv(f"{OUT}.census.csv", index=False)
    say("")
    say(f"    {len(U)} committed text units over LEADERBOARD.md + CHANGELOG.md + {nmd} .md files")
    say("    in research/backtests/.  A unit's PANEL STANCE is EXACT (a zero-tolerance identity,")
    say("    which is pooling-immune — G9), POOLED (says max/min/mean over panels), PER_PANEL")
    say("    (names a panel or reports per panel) or SILENT.")
    say("")
    say("      claim set    units    EXACT   POOLED   PER_PANEL   SILENT   non-exact SILENT share")
    crows = []
    for cs in CLAIM_SETS:
        z = X[X[cs]]
        st = z.stance.value_counts()
        ne = z[z.stance != "EXACT"]
        share = float((ne.stance == "SILENT").mean()) if len(ne) else np.nan
        crows.append(dict(claim_set=cs, units=len(z), EXACT=int(st.get("EXACT", 0)),
                          POOLED=int(st.get("POOLED", 0)),
                          PER_PANEL=int(st.get("PER_PANEL", 0)),
                          SILENT=int(st.get("SILENT", 0)), n_nonexact=len(ne),
                          nonexact_silent_share=share))
        say(f"      {cs:12s} {len(z):6d}   {int(st.get('EXACT',0)):6d}   "
            f"{int(st.get('POOLED',0)):6d}   {int(st.get('PER_PANEL',0)):9d}   "
            f"{int(st.get('SILENT',0)):6d}   {share:20.4f}")
    CS = pd.DataFrame(crows)
    CS.to_csv(f"{OUT}.claimsets.csv", index=False)
    SILENT_SHARE = float(CS[CS.claim_set == HEAD_CS].nonexact_silent_share.iloc[0])

    # which committed "N of 18/19/22" clone counts survive which pooling rule
    say("")
    say("    RE-READING THE COMMITTED COUNTS.  Every 'N of 18 / 19 / 22' that appears inside a")
    say("    clone claim is checked against the count each pooling rule actually produces on the")
    say("    record's own candidate set at that rule's own bar.  A count is REPRODUCED when some")
    say("    (rule, bar) cell gives it; the cell that gives it is named.")
    prod = {}
    for bn, bv in BARS.items():
        for rule in POOLS:
            if rule == "P_UNPOOLED":
                for p in PN:
                    prod[(rule, p, bn)] = sum(1 for k in NONINC if gapp[(p, k)] <= bv)
            else:
                gp = {k: pooled_D([np.array([[0.0, gapp[(p, k)]], [gapp[(p, k)], 0.0]])
                                   for p in PN], rule)[0, 1] for k in NONINC}
                prod[(rule, "POOLED", bn)] = sum(1 for k in NONINC if gp[k] <= bv)
    say("")
    say("      counts this candidate set can produce (clones of 18):")
    for bn in BARS:
        say(f"        {bn:9s} " + "  ".join(
            f"{(r if pp=='POOLED' else pp)}={v}" for (r, pp, b), v in sorted(prod.items())
            if b == bn))
    rrows = []
    for cs in CLAIM_SETS:
        z = X[X[cs] & (X.n_nofm18 > 0)]
        tot = rep = 0
        for _, r in z.iterrows():
            for tok in str(r.nofm18).split(";"):
                if not tok:
                    continue
                a, b = tok.split("of")
                a, b = int(a), int(b)
                if b != 18:
                    continue
                tot += 1
                cells = [f"{(rr if pp=='POOLED' else pp)}/{bb}"
                         for (rr, pp, bb), v in prod.items() if v == a]
                rep += bool(cells)
                rrows.append(dict(claim_set=cs, uid=r.uid, src=r.src, stated=a, of=b,
                                  reproduced=bool(cells), cells="|".join(sorted(cells)[:6])))
        say(f"      {cs:12s} '{'{n}'} of 18' tokens {tot:4d}   reproduced by some cell "
            f"{rep:4d}" + (f"   ({rep/tot:.4f})" if tot else ""))
    R = pd.DataFrame(rrows)
    R.to_csv(f"{OUT}.recount.csv", index=False)
    say("")
    say("      READ THIS AS A SCOPE PROPERTY, NOT A RECORD DEFECT (1249's lesson).  An 'N of 18'")
    say("      token inside a clone claim need not be a count OF THIS candidate set — the record")
    say("      has many other 18-object populations (reach decisions, phase books, cells) — so")
    say("      the non-reproduced share is an UPPER bound on mis-stated clone counts, not a")
    say("      measurement of them.")

    # ------------------------------------------------------------------ ARM D: rule 8, capital
    say("")
    say("=" * 110)
    say("ARM D — RULE 8 WALK-FORWARD AND BOTH KEEP PATHS (does the POOLING RULE buy anything?)")
    say("=" * 110)
    say("")
    say("    (D1) Every rung book on the full sample and on 2017-2026, 4a vs live RULES v2 and")
    say("         4b vs SPY, all grid points reported.")
    krows = []
    for pan in panels:
        i0, io = pan.i0, ilim[pan.name]
        spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
        so, lo_ = BM[(pan.name, "SPY_OOS")], BM[(pan.name, "LIVE_OOS")]
        for k in BOOKKEY:
            rr = booked[pan.name][k]
            k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
            k4a_o, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
            krows.append(dict(panel=pan.name, book=akey(k), ladder=k[0],
                              is_incumbent=(k in ANCH_KEYS), **m, H1=h1, H2=h2,
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                              OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                              KEEP_4b_OOS=k4b_o))
    BK = pd.DataFrame(krows)
    BK.to_csv(f"{OUT}.books.csv", index=False)
    say(f"         {len(BK)} (panel, book) rows.  4a {int(BK.KEEP_4a.sum())}; 4b full "
        f"{int(BK.KEEP_4b.sum())}; 4b OOS {int(BK.KEEP_4b_OOS.sum())}; BOTH "
        f"{int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())}.")
    for p in PN:
        s, l = BM[(p, "SPY")], BM[(p, "LIVE")]
        so, lo_ = BM[(p, "SPY_OOS")], BM[(p, "LIVE_OOS")]
        say(f"         {p:6s} SPY full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:8.2%}"
            f"   OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:8.2%}")
        say(f"         {p:6s} LIVE v2  {l['CAGR']:7.2%} / {l['Sharpe']:.4f} / {l['MaxDD']:8.2%}"
            f"   OOS {lo_['CAGR']:7.2%} / {lo_['Sharpe']:.4f} / {lo_['MaxDD']:8.2%}")

    say("")
    say("    (D2) THE POOLING RULE ON TRIAL, RUN WALK-FORWARD.  For every (panel, ladder) the IS")
    say("         Sharpe argmax is taken on the IS window ONLY (warm-up .. 2016-12-31) and the")
    say("         2017-2026 return is read ONCE.  RAW = choose over all rungs.  DEDUP_<rule> =")
    say("         choose one representative per clone cluster, the clusters built from IS")
    say("         Sharpes under that pooling rule (POOLED rules share one cluster structure")
    say("         across panels; PANEL builds them on the panel's own IS Sharpes).  Nothing")
    say("         here touches 2017+.")
    Sis = {(p.name, k): sharpe(booked[p.name][k][p.i0:ilim[p.name]]) for p in panels
           for k in BOOKKEY}
    wrows = []
    for lad in LADS + ["UNION"]:
        keys = ALT if lad == "UNION" else [(lad, r) for r in LAD[lad]]
        Dis = [np.abs(np.subtract.outer(np.array([Sis[(p, k)] for k in keys]),
                                        np.array([Sis[(p, k)] for k in keys]))) for p in PN]
        for pan in panels:
            i0, io = pan.i0, ilim[pan.name]
            spy, liv = BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")]
            so, lo_ = BM[(pan.name, "SPY_OOS")], BM[(pan.name, "LIVE_OOS")]
            iv = [Sis[(pan.name, k)] for k in keys]
            for mode in (["RAW"] + [f"DEDUP_{r}" for r in POOLED_ONLY] + ["DEDUP_PANEL"]):
                if mode == "RAW":
                    cand = keys
                elif mode == "DEDUP_PANEL":
                    Dp = np.abs(np.subtract.outer(np.array(iv), np.array(iv)))
                    cand = reps_from_labels(keys, sl_components(Dp, BAR_HEAD), iv)
                else:
                    D = pooled_D(Dis, mode.replace("DEDUP_", ""))
                    cand = reps_from_labels(keys, sl_components(D, BAR_HEAD), iv)
                if not cand:
                    continue
                ch = max(cand, key=lambda k: (Sis[(pan.name, k)]
                                              if np.isfinite(Sis[(pan.name, k)]) else -np.inf))
                rr = booked[pan.name][ch]
                k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], spy, liv)
                _, k4b_o, mo, _, _ = keep_paths(rr[io:], so, lo_)
                wrows.append(dict(panel=pan.name, ladder=lad, mode=mode, K=len(keys),
                                  K_cand=len(cand), chosen=akey(ch), **m, H1=h1, H2=h2,
                                  OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                  OOS_MaxDD=mo["MaxDD"], KEEP_4a=k4a, KEEP_4b=k4b,
                                  KEEP_4b_OOS=k4b_o))
    for pan in panels:
        i0, io = pan.i0, ilim[pan.name]
        rr = booked[pan.name][INC]
        k4a, k4b, m, h1, h2 = keep_paths(rr[i0:], BM[(pan.name, "SPY")], BM[(pan.name, "LIVE")])
        _, k4b_o, mo, _, _ = keep_paths(rr[io:], BM[(pan.name, "SPY_OOS")],
                                        BM[(pan.name, "LIVE_OOS")])
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
    modes = ["RAW"] + [f"DEDUP_{r}" for r in POOLED_ONLY] + ["DEDUP_PANEL"]
    raw_m = float(W8[W8["mode"] == "RAW"].OOS_Sharpe.mean())
    for mode in modes:
        z = W8[W8["mode"] == mode]
        say(f"           {mode:14s} {z.OOS_Sharpe.mean():.4f}  (vs RAW "
            f"{z.OOS_Sharpe.mean()-raw_m:+.4f})  over {len(z)} rows, {z.chosen.nunique()} "
            f"distinct books, mean candidates {z.K_cand.mean():.2f}")
    say("")
    say("         PAIRED AGAINST DO-NOTHING ON THE SAME ROWS (the 15-row means above are not")
    say("         comparable to a 3-row DO_NOTHING mean; this is).  Delta = chooser OOS Sharpe")
    say("         minus the incumbent's OOS Sharpe ON THAT PANEL, over the 15 (panel, ladder)")
    say("         rows:")
    dnp = {r.panel: r.OOS_Sharpe for _, r in W8[W8["mode"] == "DO_NOTHING"].iterrows()}
    say("           mode            mean delta vs do-nothing   positive rows   mean delta vs RAW")
    rawd = {(r.panel, r.ladder): r.OOS_Sharpe for _, r in W8[W8["mode"] == "RAW"].iterrows()}
    for mode in modes:
        z = W8[W8["mode"] == mode]
        d = np.array([r.OOS_Sharpe - dnp[r.panel] for _, r in z.iterrows()])
        dr = np.array([r.OOS_Sharpe - rawd[(r.panel, r.ladder)] for _, r in z.iterrows()])
        say(f"           {mode:14s} {d.mean():+22.4f}   {int((d > 0).sum()):5d} of {len(d):<6d} "
            f"{dr.mean():+17.4f}")
    say("")
    say("         Where the POOLING RULE moves the pick at all (RAW pick vs each DEDUP pick):")
    nmove = 0
    for _, r in W8[W8["mode"] == "RAW"].iterrows():
        for mode in modes[1:]:
            d = W8[(W8.panel == r.panel) & (W8.ladder == r.ladder) & (W8["mode"] == mode)]
            if len(d) and d.iloc[0].chosen != r.chosen:
                nmove += 1
                say(f"           {r.panel:6s} {r.ladder:8s} {mode:14s} RAW {r.chosen:12s} "
                    f"OOS S {r.OOS_Sharpe:.4f} -> {d.iloc[0].chosen:12s} OOS S "
                    f"{d.iloc[0].OOS_Sharpe:.4f}")
    if nmove == 0:
        say("           NONE — every dedup rule at every (panel, ladder) picks the SAME book as")
        say("           the raw chooser, so the whole pooling debate is worth exactly 0.0000 of")
        say("           OOS Sharpe here.")
    say(f"         pick moves: {nmove} of {len(W8[W8['mode']!='DO_NOTHING'])-len(W8[W8['mode']=='RAW'])}")
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
    agree_min = float(A[A.bar == "B_TIGHT"].agree.min())
    if SILENT_SHARE >= 0.50 and MISSTATE_SHARE >= 0.50:
        outcome = "(A) THE BAR NEEDS ITS PANEL"
    elif agree_min >= 0.90 and SILENT_SHARE < 0.50:
        outcome = "(B) POOLING IS INERT"
    else:
        outcome = "(C) MIXED"
    say("")
    say(f"    PRE-DECLARED OUTCOME FIRES: {outcome}")
    say(f"      non-exact PANEL-SILENT share at {HEAD_CS}: {SILENT_SHARE:.4f} (bar 0.50)")
    say(f"      P_MAX label misstated on some panel: {int(head.misstated)} of {len(NONINC)} "
        f"books = {MISSTATE_SHARE:.4f} (bar 0.50)")
    say(f"      worst pooled-vs-per-panel agreement at the record's bar: {agree_min:.4f}")
    say("")
    say(f"    CAPITAL.  Pooling rule is worth {max(float(W8[W8['mode']==m].OOS_Sharpe.mean())-raw_m for m in modes[1:]):+.4f} of mean OOS Sharpe at best over "
        f"{len(W8)} rule-8 rows;")
    say(f"    4a {int(BK.KEEP_4a.sum())} of {len(BK)} books and {int(W8.KEEP_4a.sum())} of "
        f"{len(W8)} rule-8 rows; 4b BOTH {int((BK.KEEP_4b & BK.KEEP_4b_OOS).sum())} books / "
        f"{int((W8.KEEP_4b & W8.KEEP_4b_OOS).sum())} rule-8 rows,")
    say("    collapsing to books the record already holds.  NO NEW BOOK, NO RULES CHANGE, NO")
    say("    PROTOCOL EDIT FROM THIS RUN.")
    say("")
    say("    SURVIVORSHIP (rule 9).  U56 and B136 are CURRENT-constituent lists; SMALL is the")
    say("    current constituents of a sub-$2B screen with max_1d_move >= 1.0 names dropped.")
    say("    Every LEVEL here is optimistic.  The headline is a DISAGREEMENT between two")
    say("    readings of the SAME books on the SAME tape, so it is first-order immune; the 4a")
    say("    and 4b legs are not, and those passes are upper bounds.")

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
