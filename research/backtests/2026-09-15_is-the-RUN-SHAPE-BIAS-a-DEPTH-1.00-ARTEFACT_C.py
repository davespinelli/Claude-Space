#!/usr/bin/env python3
"""Idea 883 (lane C, 2026-09-15) - is the RUN-SHAPE BIAS a DEPTH-1.00 ARTEFACT across the whole
placebo record?

THE CLAIM UNDER TEST
--------------------
Idea 875 measured a systematic bias of -0.0046 of Sharpe against BLOCK for a switch-matched null
whose fire-run dispersion is 5.87x the real arm's (SM_DOM), and proposed a PROTOCOL clause naming
the longest run.  Idea 881 confirmed the bias is a MAX-RUN-LENGTH fact and, in its [6b] mechanism
table, reported the one cut that changes the reading:

    depth = 1.00   signed gap -0.00590   z +3.67     (resolved)
    depth = 0.50   signed gap -0.00184   z +1.75     (inside the seed-noise band, unresolvable)

Both runs priced the headline POOLED over a two-point depth axis {0.50, 1.00}, so the published
-0.0046 is an average of a resolved full-de-grossing number and an unresolvable partial one.  The
queue's question is whether the defect PROTOCOL is being asked to legislate exists at the depths
the record's actual books de-gross at, or only at depth 1.00.

This run answers it in two pieces, and the second is the one that decides it:

    (A) CENSUS - which committed placebo-differenced numbers in the record were priced on a grid
        that includes depth 1.00, and how many were priced at partial depth at all.
    (B) THE DEPTH LAW - walk depth on a FOUR-point grid {0.25, 0.50, 0.75, 1.00} and measure the
        SM_DOM-minus-BLOCK signed gap at each rung, then re-read the bias at each of the 8
        memo-backed shelf books' OWN realised de-grossing depth (measured from the book's own
        exposure path, not assumed).

A multiplier of (1 - d) scales the book's return on every firing day, so if the bias is the
mean-return effect idea 881 measured (its [6b]: placebo vol is flat to 0.2% across nulls, so the
whole signed gap is a MEAN-RETURN difference), it must be PROPORTIONAL to d and must vanish as
d -> 0.  That is a falsifiable law, not a description, and it is pre-registered below as H_LAW.
If it holds, the -0.0046 headline is an artefact of where the grid put its depth points, and the
number that matters for any real book is the law read at that book's own depth.

TUNED PARAMETERS (PROTOCOL rule 4: at most two) - the queue names both
    1. claim set   NARROW (committed scripts that BUILD a placebo null - the files that can
                   publish a null-differenced number) vs BROAD (NARROW plus every committed
                   script that carries both a null-kind vocabulary and a depth axis).  Both
                   censused, both reported, neither selected on.
    2. depth grid  {0.25, 0.50, 0.75, 1.00}.  881's two rungs are a subset, so its published
                   numbers are reproduction bars (G3), not new points.
    ALL grid points reported at every panel / family / q / w / cadence / gross / cost rung.
    Nothing is chosen on the answer; every null is priced on every arm into .excess.csv.

THE NULLS (all firing-rate-matched and information-free)
    RAND     iid singles, switch count unmatched (13x)                  ideas 602/606
    BLOCK    circular shift of the real path - THE REFERENCE            ideas 602/606
    BLOCK2   BLOCK from an independent seed stream; its true gap is EXACTLY ZERO by construction,
             so it measures this grid's signed-statistic band rather than assuming one  (idea 881)
    SM_DOM   switch-matched, ONE dominant run of k-(m-1) days           ideas 875/881  <- the defect
    SM_UNIF  switch-matched, near-uniform runs (875's clean control)    ideas 875/881

GATES (printed before any hypothesis is read)
    G1  a never-firing multiplier path reproduces the ungated book exactly.            bar 1e-12
    G6  the fast Sharpe used on placebo cells equals engine.metrics()['Sharpe'].       bar 1e-10
    G2  every null's mean effective multiplier equals the real arm's (rate match).     bar 1e-12
    G4  determinism: every placebo recomputed from its md5 seed, max |d| must be 0.
    G5  construction: SM_DOM and SM_UNIF preserve the real arm's k and m EXACTLY.
    G3  REPRODUCTION of idea 881 at the two rungs it published: SM_DOM's signed pooled gap within
        0.0020 of -0.0059 (depth 1.00, z >= +3.0) and of -0.0018 (depth 0.50), and SM_DOM's
        dispersion ratio within 0.60 of 5.87.  Seed strings and the arm count differ (four depth
        rungs, not two), so these are agreement bars, not identity bars; any miss is printed.
    G7  CALIBRATION: BLOCK2's signed pooled gap |.| <= 0.0010 with |z| < 2.0.  This is the band
        every reading below is judged against.
    G8  every shelf book reproduces its committed memo triple (CAGR within 1.00 pp, Sharpe within
        0.10, MaxDD within 2.00 pp).  A book that fails G8 is printed and its depth reading is
        marked UNVERIFIED rather than dropped.

PRE-REGISTERED HYPOTHESES (fixed before any number below the gates was read)
    H_LAW     the SM_DOM signed gap is PROPORTIONAL to depth: gap(d)/d is constant across the
              four rungs to within +/-25% of its mean, and a through-origin fit explains
              R^2 >= 0.90 of the four rung medians.  PASS = the bias is a de-grossing-depth
              effect with no fixed component, i.e. the published headline is a grid artefact.
    H_ART     the queue's title.  At every rung with d <= 0.50 the signed gap is INSIDE the
              BLOCK2 band (|signed| <= 0.0010 AND |z| < 2.0), and at d = 1.00 it is OUTSIDE.
              PASS = the run-shape defect is a DEPTH-1.00 ARTEFACT at the depths books use.
    H_BOOK    reading the fitted law at each shelf book's OWN measured de-grossing depth, the
              predicted bias is smaller than the record's own resolution (the BLOCK2 band,
              0.0010 of Sharpe) for a MAJORITY of the 8 books.  PASS = no committed book's
              published placebo verdict is exposed to the defect.
    H_CENSUS  a MAJORITY of the record's committed placebo-differenced numbers (NARROW claim set)
              were priced on a grid containing depth 1.00 AND pooled across depth, i.e. their
              headline carries the depth-1.00 rung inside it.
    H_COSTINV the signed gap moves < 0.005 across 0 / 10 / 25 bps at every depth rung.  The
              switch counts are matched, so the depth law must not be a cost story.
    H_WF      Spearman(IS signed gap, OOS signed gap) >= +0.30 in >= 6 of 8 families for SM_DOM
              at depth 1.00.

RULE 8 WALK-FORWARD (required, run whatever the verdict)
    IS = ..2016-12-31 fitted, OOS = 2017-01-01.. read once.  (a) the signed gap is measured on IS
    and read on OOS per family and per depth rung (H_WF).  (b) THE BOOKS: one declared IS-only
    selector - the arm with the highest 2009-2016 Sharpe on each panel - is picked and its
    untouched OOS CAGR / Sharpe / MaxDD is reported against RULES v2 (live) OOS and SPY OOS, with
    BOTH KEEP paths, plus the unselected base rate of 4a and 4b over all arms.

SURVIVORSHIP: U56 and B136 are current-constituent lists.  SMALL is the sub-$2B panel with every
ticker whose max_1d_move >= 1.0 in data/small_meta.csv dropped first, and it is CURRENT
CONSTITUENTS ONLY - dead small caps are absent, so its CAGRs are the most optimistic numbers here
and its 4b readings are upper bounds.  This run's headline quantity is a DIFFERENCE BETWEEN TWO
NULLS ON THE SAME ARM, which is far less exposed to that bias than any level.

PROTOCOL: 10 bps per unit turnover (0 and 25 also reported), next-day fills, no shorting, no
leverage.  Deterministic (md5-seeded), standalone, no network - committed caches only.  Modifies
nothing but its own outputs:
    .census.csv  .arms.csv  .excess.csv  .gap.csv  .depthlaw.csv  .books.csv  .shelf.csv
    .walkforward.csv  .console.txt
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))
from baseline import load_universe, score, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).name[:-3]
OUT = REPO / "research" / "backtests"
LINES: list[str] = []

FREQ, MAX_VOL, SMOOTH = "W", 0.60, 20
QS = [0.07, 0.12, 0.17]
WS = [252, 1008]
DEPTHS = [0.25, 0.50, 0.75, 1.00]          # TUNED PARAMETER 2 (the manipulated axis)
CADENCES = ["D", "W"]
GROSSES = [0.75, 1.00]
RUNGS = [0, 10, 25]
STATES = ["BREADTH", "VOL20", "DISP", "CORR"]
SIDES = {"BREADTH": ("LO", "HI"), "VOL20": ("HI", "LO"), "DISP": ("HI", "LO"), "CORR": ("HI", "LO")}
KINDS = ["RAND", "BLOCK", "BLOCK2", "SM_DOM", "SM_UNIF"]
SMKINDS = ["SM_DOM", "SM_UNIF"]
NSEED = 20
SPLIT = "2017-01-01"

# idea 881's published depth cuts, for G3 (agreement bars, not identity bars)
PUB881 = {1.00: -0.00590, 0.50: -0.00184}
PUB881_Z = {1.00: 3.67, 0.50: 1.75}
PUB881_DISP = 5.87
SIGN_BAR, DISP_BAR, Z_BAR = 0.0020, 0.60, 3.0
CAL_BAR, CAL_Z = 0.0010, 2.0


def log(s=""):
    print(s, flush=True)
    LINES.append(str(s))


# ------------------------------------------------------------------ primitives (602/606/875/881)
def eligible_mask(px):
    _, above, vol20 = score(px)
    return above & (vol20 < MAX_VOL)


def ewall_weights(px, gross):
    e = eligible_mask(px).astype(float)
    n = e.sum(axis=1).replace(0, np.nan)
    return e.div(n, axis=0).mul(gross).fillna(0.0)


def fast_sharpe(v):
    v = np.asarray(v, float)
    sd = v.std(ddof=1)
    return v.mean() * 252 / (sd * np.sqrt(252)) if sd > 0 else np.nan


def ann_vol(v):
    return float(np.asarray(v, float).std(ddof=1) * np.sqrt(252))


def state_breadth(px):
    above = px > px.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def state_vol20(px):
    return (px.pct_change().rolling(SMOOTH).std() * np.sqrt(252)).mean(axis=1)


def state_disp(px):
    return px.pct_change().std(axis=1).rolling(SMOOTH).mean()


def state_corr(px):
    rt = px.pct_change()
    sig = rt.rolling(SMOOTH).std()
    s_idx = rt.mean(axis=1).rolling(SMOOTH).std()
    n = sig.notna().sum(axis=1).replace(0, np.nan)
    sbar, s2bar = sig.mean(axis=1), (sig ** 2).mean(axis=1)
    return ((s_idx ** 2 - s2bar / n) / (sbar ** 2 - s2bar / n).replace(0, np.nan)).clip(-1, 1)


STATE_FN = {"BREADTH": state_breadth, "VOL20": state_vol20, "DISP": state_disp, "CORR": state_corr}


def gate_mult(st, thr, side, depth, cadence, idx):
    fire = ((st < thr) if side == "LO" else (st > thr)) & st.notna() & thr.notna()
    m = pd.Series(1.0, index=idx).where(~fire, 1.0 - depth)
    if cadence == "W":
        m = m.where(rebalance_mask(idx, FREQ)).ffill().fillna(1.0)
    return m


def apply_eff(r_base, m_eff, gross, cost_bps):
    switch = np.abs(np.diff(m_eff, prepend=m_eff[0]))
    return m_eff * r_base - switch * gross * cost_bps / 1e4


def nswitch(m_eff):
    return int((np.abs(np.diff(np.asarray(m_eff, float), prepend=m_eff[0])) > 0).sum())


def seed_of(*parts):
    return int(hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def runs_of(fire):
    fire = np.asarray(fire, bool)
    n = len(fire)
    d = np.diff(fire.astype(np.int8))
    starts = np.flatnonzero(d == 1) + 1
    ends = np.flatnonzero(d == -1) + 1
    if fire[0]:
        starts = np.r_[0, starts]
    if fire[-1]:
        ends = np.r_[ends, n]
    if len(starts) == 0:
        return np.array([], int), np.array([n], int)
    fl = (ends - starts).astype(int)
    gl = np.empty(len(starts) + 1, int)
    gl[0] = starts[0]
    gl[1:-1] = starts[1:] - ends[:-1]
    gl[-1] = n - ends[-1]
    return fl, gl


def assemble(fl, gl, n):
    out = np.zeros(n, bool)
    p = 0
    for i, f in enumerate(fl):
        p += gl[i]
        out[p:p + f] = True
        p += f
    return out


def rand_composition(total, parts, rng, min_each):
    if parts <= 0:
        return np.array([], int)
    rem = total - parts * min_each
    if rem < 0:
        raise ValueError("infeasible composition")
    if parts == 1:
        return np.array([total], int)
    cuts = np.sort(rng.choice(np.arange(rem + parts - 1), size=parts - 1, replace=False))
    pieces = np.diff(np.r_[-1, cuts, rem + parts - 1]) - 1
    return (pieces + min_each).astype(int)


def _gaps_like_switchmatch(n, k, m, rng):
    """871/875/881's gap draw, identical across switch-matched nulls so the fire-run SHAPE is the
    single manipulated axis within a depth rung."""
    gl = rand_composition(n - k - (m - 1), m + 1, rng, 0)
    gl[1:-1] += 1
    return gl


def _even(total, parts):
    base, rem = divmod(total, parts)
    out = np.full(parts, base, int)
    out[:rem] += 1
    return out


def fire_lengths(kind, k, m, rng):
    if kind == "SM_UNIF":
        fl = _even(k, m)
        return fl[rng.permutation(m)]
    fl = np.ones(m, int)                                  # SM_DOM: one run of k-(m-1)
    fl[0] = k - m + 1
    return fl[rng.permutation(m)]


def placebo_eff(m_eff, depth, kind, seed):
    """Rate-matched, information-free twin of the EFFECTIVE multiplier path m_eff."""
    v = np.asarray(m_eff, float)
    n = len(v)
    fire = v < 1.0
    k = int(fire.sum())
    if k == 0 or k == n:
        return v.copy()
    rng = np.random.default_rng(seed)
    if kind == "RAND":
        out = np.ones(n)
        out[rng.choice(n, size=k, replace=False)] = 1.0 - depth
        return out
    if kind in ("BLOCK", "BLOCK2"):
        return np.roll(v, int(rng.integers(1, n)))
    fl, _ = runs_of(fire)
    m = len(fl)
    if (n - k) < (m - 1):
        return np.roll(v, int(rng.integers(1, n)))
    gl2 = _gaps_like_switchmatch(n, k, m, rng)
    fl2 = fire_lengths(kind, k, m, rng)
    out = np.ones(n)
    out[assemble(fl2, gl2, n)] = 1.0 - depth
    return out


# ------------------------------------------------------------------------------ helpers
def pack(r):
    m = metrics(pd.Series(r) if not isinstance(r, pd.Series) else r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def halves(r):
    h = len(r) // 2
    return fast_sharpe(r[:h]), fast_sharpe(r[h:])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return float("nan")
    return float(a[ok].rank().corr(b[ok].rank()))


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"  SMALL panel: {px.shape[1]} columns -> {len(keep)} kept "
        f"({px.shape[1]-len(keep)} dropped for max_1d_move >= 1.0)")
    return px[keep]


# ============================================================== (A) CENSUS - TUNED PARAMETER 1
NULLVOCAB = re.compile(r'"BLOCK"|\'BLOCK\'|SM_DOM|placebo', re.I)
BUILDER = re.compile(r"def\s+placebo", re.I)
DEPTHLIST = re.compile(r"DEPTHS?\s*=\s*\[([^\]]*)\]")
DEPTHLIT = re.compile(r"depth\s*[=:]\s*([01]?\.\d+|1\b)")


def census():
    """Which committed placebo-differenced numbers were priced at depth 1.00?

    NARROW = files that BUILD a placebo null (a `def placebo*`): the files that can publish a
             null-differenced Sharpe at all.
    BROAD  = NARROW plus every committed script carrying both the null vocabulary and a depth
             axis (it may quote or re-price such a number without constructing one).
    Classification of each file's depth grid, from its own source:
        FULL_ONLY    the only depth priced is 1.00
        POOLED       the grid contains 1.00 and at least one partial depth, and the file's
                     headline statistic is pooled over it
        PARTIAL_ONLY every depth priced is < 1.00
        NO_DEPTH     no depth axis in the source
    """
    rows = []
    for p in sorted((REPO / "research" / "backtests").glob("*.py")):
        if p.name == Path(__file__).name:
            continue
        try:
            src = p.read_text(errors="ignore")
        except OSError:
            continue
        has_vocab = bool(NULLVOCAB.search(src))
        builds = bool(BUILDER.search(src))
        if not has_vocab:
            continue
        ds = set()
        for m in DEPTHLIST.finditer(src):
            for tok in m.group(1).split(","):
                tok = tok.strip()
                try:
                    ds.add(round(float(tok), 4))
                except ValueError:
                    pass
        for m in DEPTHLIT.finditer(src):
            try:
                ds.add(round(float(m.group(1)), 4))
            except ValueError:
                pass
        ds = {d for d in ds if 0.0 < d <= 1.0}
        if not ds:
            cls = "NO_DEPTH"
        elif ds == {1.0}:
            cls = "FULL_ONLY"
        elif 1.0 in ds:
            cls = "POOLED"
        else:
            cls = "PARTIAL_ONLY"
        rows.append(dict(file=p.name, builds_null=builds,
                         claim_set=("NARROW" if builds else "BROAD"),
                         depths=";".join(f"{d:g}" for d in sorted(ds)), n_depths=len(ds),
                         has_1p00=(1.0 in ds), cls=cls))
    return pd.DataFrame(rows)


# ================================================================== the 8 memo-backed shelf books
def shelf_books(U, B):
    """861's shelf, restated verbatim from the committed lane-C script so the depth reading below
    is on the same 8 books the record's other censuses use."""
    out = {}
    out["u56-v2band-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.03, 1.00), memo=(0.1155, 1.2067, -0.1570))
    out["u56-band008-gross100"] = dict(
        panel="U56", freq="W", W=rules_v2_weights(U, 0.08, 1.00), memo=(0.1137, 1.1439, -0.1905))

    s, above, vol20 = score(U, vol_scale=False)
    rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
    out["u56-top20-band-m20"] = dict(
        panel="U56", freq="W", W=(rank <= 20).astype(float) * 0.75 / 20,
        memo=(0.1287, 1.112, -0.1722))

    ab = (U > U.rolling(200).mean()).astype(float)
    n = ab.sum(axis=1).replace(0, np.nan)
    out["u56-marsrespread-gross075"] = dict(
        panel="U56", freq="W", W=ab.div(n, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1155, 1.0914, None))

    rel = U / U.rolling(200).mean() - 1
    sel = (rel.rank(axis=1, ascending=False, pct=True) <= 0.50) & rel.notna()
    k = sel.astype(float).sum(axis=1).replace(0, np.nan)
    out["u56-quantile50-respread-M"] = dict(
        panel="U56", freq="M", W=sel.astype(float).div(k, axis=0).mul(0.75).fillna(0.0),
        memo=(0.1547, 1.2359, -0.1980))

    r6 = B / B.shift(126) - 1
    out["b136-r620-gross065-W"] = dict(
        panel="B136", freq="W", W=(r6.rank(axis=1, ascending=False) <= 20).astype(float) * 0.65 / 20,
        memo=(0.1499, 1.1264, -0.1943))

    for nm, px, q, dep, memo in (
            ("b136-qroll-q012-w1008-d050-g100", B, 0.12, 0.50, (0.1430, 1.1121, -0.1731)),
            ("u56-k8-qroll-q017-w1008-d100-g100", U, 0.17, 1.00, (0.1416, 1.2226, -0.1479))):
        elig = eligible_mask(px).astype(float)
        nn = elig.sum(axis=1).replace(0, np.nan)
        base = elig.div(nn, axis=0).fillna(0.0)
        br = state_breadth(px)
        thr = br.rolling(1008, min_periods=1008).quantile(q)
        m = pd.Series(1.0, index=px.index).where(~(br < thr), 1.0 - dep)
        m = m.where(br.notna() & thr.notna(), 1.0)
        m = m.where(rebalance_mask(px.index, FREQ)).ffill().fillna(1.0)
        out[nm] = dict(panel=("B136" if px is B else "U56"), freq="W",
                       W=base.mul(m, axis=0), memo=memo, nominal_depth=dep)
    return out


def realised_depth(W, start):
    """A book's OWN de-grossing depth, measured from its own exposure path rather than assumed.

    g_t  = the book's target gross on day t (its summed weights)
    g*   = the 95th percentile of g_t - the book's un-de-grossed exposure
    days de-grossed = g_t < 0.98 * g*
    depth_own = 1 - mean(g_t | de-grossed) / g*      (0 = never de-grosses, 1 = to full cash)
    """
    g = W.sum(axis=1).loc[start:]
    gstar = float(g.quantile(0.95))
    if gstar <= 0:
        return np.nan, np.nan, np.nan
    dg = g < 0.98 * gstar
    share = float(dg.mean())
    if dg.sum() == 0:
        return 0.0, 0.0, gstar
    return float(1.0 - g[dg].mean() / gstar), share, gstar


# ======================================================================================== gates
def gates(panels):
    log("\n[0] GATES (printed before any hypothesis is read)")
    px = panels["U56"]
    core = px.drop(columns=["SPY"], errors="ignore")
    r_base = backtest(core, ewall_weights(core, 0.75), cost_bps=10,
                      freq=FREQ)["returns"].loc["2009-01-01":]
    ones = np.ones(len(r_base))
    g1 = float(np.max(np.abs(apply_eff(r_base.values, ones, 0.75, 10) - r_base.values)))
    log(f"  G1 never-firing multiplier == ungated book   max|d| {g1:.3e}  bar 1e-12  "
        f"[{'PASS' if g1 < 1e-12 else 'FAIL'}]")
    g6 = abs(fast_sharpe(r_base.values) - metrics(r_base)["Sharpe"])
    log(f"  G6 fast Sharpe == engine.metrics()['Sharpe'] |d| {g6:.3e}  bar 1e-10  "
        f"[{'PASS' if g6 < 1e-10 else 'FAIL'}]")
    rng = np.random.default_rng(0)
    bad_km = 0
    for t in range(300):
        n = 1200
        fire = np.zeros(n, bool)
        p = int(rng.integers(0, 30))
        while p < n:
            L = int(rng.integers(1, 25))
            fire[p:p + L] = True
            p += L + int(rng.integers(3, 60))
        v = np.where(fire, 0.5, 1.0)
        fl, _ = runs_of(fire)
        k, m = int(fire.sum()), len(fl)
        for kind in SMKINDS:
            pe = placebo_eff(v, 0.5, kind, seed_of("G5", t, kind))
            pf = pe < 1.0
            pfl, _ = runs_of(pf)
            if int(pf.sum()) != k or len(pfl) != m:
                bad_km += 1
    log(f"  G5 k and m preserved by both switch-matched nulls: {bad_km} violations in "
        f"{300*len(SMKINDS)} synthetic draws  [{'PASS' if bad_km == 0 else 'FAIL'}]")


# ==================================================================================== per panel
def run_panel(name, px):
    t0 = time.time()
    idx = px.index
    core = px.drop(columns=["SPY"], errors="ignore")
    spy = px["SPY"].pct_change().fillna(0.0)
    states = {s: STATE_FN[s](core) for s in STATES}
    base = {}
    for g in GROSSES:
        w = ewall_weights(core, g)
        for c in RUNGS:
            base[(g, c)] = backtest(core, w, cost_bps=c, freq=FREQ)["returns"]

    start = idx[260]
    ii = idx[idx >= start]
    oos = np.asarray(ii >= pd.Timestamp(SPLIT))
    isw = ~oos
    RB = {k: v.loc[ii].values for k, v in base.items()}

    spy_v = spy.loc[ii].values
    spy_c, spy_s, spy_d = pack(pd.Series(spy_v, index=ii))
    spy_h1, spy_h2 = halves(spy_v)
    spy_oc, spy_os, spy_od = pack(pd.Series(spy_v[oos], index=ii[oos]))
    bl = backtest(core, rules_v2_weights(core), cost_bps=10, freq=FREQ)["returns"].loc[ii]
    bl_c, bl_s, bl_d = pack(bl)
    bl_h1, bl_h2 = halves(bl.values)
    bl_oc, bl_os, bl_od = pack(bl.loc[ii[oos]])
    bench = dict(panel=name, spy_cagr=spy_c, spy_sh=spy_s, spy_dd=spy_d, spy_h1=spy_h1,
                 spy_h2=spy_h2, spy_oos_c=spy_oc, spy_oos_s=spy_os, spy_oos_d=spy_od,
                 bl_cagr=bl_c, bl_sh=bl_s, bl_dd=bl_d, bl_h1=bl_h1, bl_h2=bl_h2,
                 bl_oos_c=bl_oc, bl_oos_s=bl_os, bl_oos_d=bl_od)

    rows, exrows = [], []
    g2 = 0.0
    km_viol = 0
    for st_name in STATES:
        st_full = states[st_name]
        for side in SIDES[st_name]:
            fam = f"{st_name}-{side}"
            for q, w in product(QS, WS):
                thr = st_full.rolling(w, min_periods=max(60, w // 4)).quantile(
                    q if side == "LO" else 1 - q)
                for depth, cad in product(DEPTHS, CADENCES):
                    mult = gate_mult(st_full, thr, side, depth, cad, idx)
                    me = mult.shift(1).fillna(1.0).loc[ii].values
                    fired = me < 1.0
                    k_real = int(fired.sum())
                    sw_real = nswitch(me)
                    fl_r, _ = runs_of(fired)
                    nruns = int(len(fl_r))
                    sd_real = float(fl_r.std(ddof=1)) if nruns > 1 else 0.0
                    lstar = int(fl_r.max()) if nruns else 0
                    for g in GROSSES:
                        real = {c: apply_eff(RB[(g, c)], me, g, c) for c in RUNGS}
                        rr = real[10]
                        c_, s_, d_ = pack(pd.Series(rr, index=ii))
                        h1, h2 = halves(rr)
                        oc, os_, od = pack(pd.Series(rr[oos], index=ii[oos]))
                        rows.append(dict(
                            panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                            depth=depth, cadence=cad, gross=g, rate=float(fired.mean()),
                            nswitch=sw_real, nruns=nruns, max_runlen=lstar, sd_runlen=sd_real,
                            CAGR=c_, Sharpe=s_, MaxDD=d_, H1=h1, H2=h2,
                            IS_Sharpe=fast_sharpe(rr[isw]), OOS_CAGR=oc, OOS_Sharpe=os_,
                            OOS_MaxDD=od))
                        sh_real = {c: fast_sharpe(real[c]) for c in RUNGS}
                        sh_is, sh_oos = fast_sharpe(rr[isw]), fast_sharpe(rr[oos])
                        for kind in KINDS:
                            acc = {c: [] for c in RUNGS}
                            acc_is, acc_oos = [], []
                            swr, sdr, mxr, pvols, kmok = [], [], [], [], []
                            for sd in range(NSEED):
                                seed = seed_of(name, fam, q, w, depth, cad, g, kind, sd)
                                pe = placebo_eff(me, depth, kind, seed)
                                g2 = max(g2, abs(pe.mean() - me.mean()))
                                swr.append(nswitch(pe) / max(sw_real, 1))
                                pf = pe < 1.0
                                pfl, _ = runs_of(pf)
                                kmok.append(int(pf.sum()) == k_real and len(pfl) == nruns)
                                sdr.append((float(pfl.std(ddof=1)) / sd_real)
                                           if (len(pfl) > 1 and sd_real > 0) else np.nan)
                                mxr.append((float(pfl.max()) / lstar) if (len(pfl) and lstar)
                                           else np.nan)
                                for c in RUNGS:
                                    pr = apply_eff(RB[(g, c)], pe, g, c)
                                    acc[c].append(sh_real[c] - fast_sharpe(pr))
                                    if c == 10:
                                        pvols.append(ann_vol(pr))
                                        acc_is.append(sh_is - fast_sharpe(pr[isw]))
                                        acc_oos.append(sh_oos - fast_sharpe(pr[oos]))
                            if kind in SMKINDS:
                                km_viol += int(NSEED - sum(kmok))
                            exrows.append(dict(
                                panel=name, family=fam, state=st_name, side=side, q=q, w=w,
                                depth=depth, cadence=cad, gross=g, kind=kind,
                                nswitch_real=sw_real, sw_ratio=float(np.mean(swr)),
                                nruns=nruns, max_runlen_real=lstar,
                                sd_runlen_ratio=float(np.nanmean(sdr)),
                                max_run_ratio=float(np.nanmean(mxr)),
                                pvol_10bps=float(np.mean(pvols)),
                                km_exact=float(np.mean(kmok)),
                                **{f"excess_{c}bps": float(np.median(acc[c])) for c in RUNGS},
                                **{f"seedsd_{c}bps": float(np.std(acc[c], ddof=1))
                                   for c in RUNGS},
                                excess_IS=float(np.median(acc_is)),
                                excess_OOS=float(np.median(acc_oos))))
        log(f"    {name}: {st_name} done  ({time.time() - t0:.0f}s)")

    d4 = 0.0
    for r in exrows[:8] + exrows[len(exrows) // 2: len(exrows) // 2 + 8]:
        st_full = states[r["state"]]
        thr = st_full.rolling(r["w"], min_periods=max(60, r["w"] // 4)).quantile(
            r["q"] if r["side"] == "LO" else 1 - r["q"])
        me = gate_mult(st_full, thr, r["side"], r["depth"], r["cadence"], idx
                       ).shift(1).fillna(1.0).loc[ii].values
        rb = RB[(r["gross"], 10)]
        sh = fast_sharpe(apply_eff(rb, me, r["gross"], 10))
        acc = [sh - fast_sharpe(apply_eff(rb, placebo_eff(
            me, r["depth"], r["kind"], seed_of(name, r["family"], r["q"], r["w"], r["depth"],
                                               r["cadence"], r["gross"], r["kind"], sd)),
            r["gross"], 10)) for sd in range(NSEED)]
        d4 = max(d4, abs(float(np.median(acc)) - r["excess_10bps"]))
    return pd.DataFrame(rows), pd.DataFrame(exrows), bench, g2, d4, km_viol


# ========================================================================================= main
def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 883 - is the RUN-SHAPE BIAS a DEPTH-1.00 ARTEFACT across the whole placebo record?"
        "  (lane C 2026-09-15)")
    log("=" * 100)
    log(f"# pandas {pd.__version__} numpy {np.__version__}  |  {len(KINDS)} nulls x {NSEED} seeds "
        f"x {len(RUNGS)} rungs x {len(DEPTHS)} depths")

    # ------------------------------------------------------------------ (A) CENSUS
    log("\n" + "=" * 100)
    log("[A] CENSUS - which committed placebo-differenced numbers were priced at depth 1.00?")
    log("    TUNED PARAMETER 1 (claim set): NARROW = files that BUILD a null; BROAD = NARROW plus")
    log("    every committed script carrying the null vocabulary and a depth axis.  Both reported.")
    log("=" * 100)
    cen = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    for cs in ("NARROW", "BROAD"):
        sub = cen[cen.claim_set == "NARROW"] if cs == "NARROW" else cen
        n = len(sub)
        tab = sub.cls.value_counts()
        log(f"  {cs:7s} n = {n:4d} committed files")
        for k in ("FULL_ONLY", "POOLED", "PARTIAL_ONLY", "NO_DEPTH"):
            v = int(tab.get(k, 0))
            log(f"      {k:13s} {v:4d}  ({v/max(n,1):6.1%})")
        carry = int(sub.has_1p00.sum())
        log(f"      carries depth 1.00 on its grid: {carry} of {n} ({carry/max(n,1):.1%})")
    narrow = cen[cen.claim_set == "NARROW"]
    h_census = bool((narrow.has_1p00.sum() / max(len(narrow), 1)) > 0.50)
    log(f"  H_CENSUS (majority of NARROW files price depth 1.00): "
        f"{'CONFIRMED' if h_census else 'REFUTED'}")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL": small_panel()}
    for n_, p in panels.items():
        log(f"  {n_}: {p.shape[1]} cols x {len(p)} days  {p.index[0].date()} .. "
            f"{p.index[-1].date()}")
    gates(panels)

    # ------------------------------------------------------- G8 + the shelf's own depths
    log("\n[0b] G8 - the 8 memo-backed shelf books, and each book's OWN de-grossing depth")
    U = panels["U56"].drop(columns=["SPY"], errors="ignore")
    B = panels["B136"].drop(columns=["SPY"], errors="ignore")
    sb = shelf_books(U, B)
    shelf_rows = []
    for nm, d in sb.items():
        px = U if d["panel"] == "U56" else B
        start = px.index[260]
        res = backtest(px, d["W"], cost_bps=10, freq=d["freq"])["returns"].loc[start:]
        c_, s_, dd_ = pack(res)
        oosr = res.loc[SPLIT:]
        oc, os_, od = pack(oosr)
        dep, share, gstar = realised_depth(d["W"], start)
        memo = d["memo"]
        ok = (abs(c_ - memo[0]) <= 0.01 and abs(s_ - memo[1]) <= 0.10
              and (memo[2] is None or abs(dd_ - memo[2]) <= 0.02))
        shelf_rows.append(dict(book=nm, panel=d["panel"], freq=d["freq"],
                               nominal_depth=d.get("nominal_depth", np.nan),
                               depth_own=dep, degross_day_share=share, gstar=gstar,
                               CAGR=c_, Sharpe=s_, MaxDD=dd_, OOS_CAGR=oc, OOS_Sharpe=os_,
                               OOS_MaxDD=od, memo_CAGR=memo[0], memo_Sharpe=memo[1],
                               memo_MaxDD=memo[2], G8=ok))
        log(f"  {nm:36s} {d['panel']:5s} memo {memo[0]:.4f}/{memo[1]:.4f}/"
            f"{'None' if memo[2] is None else format(memo[2], '.4f')}  "
            f"here {c_:.4f}/{s_:.4f}/{dd_:.4f}  [{'PASS' if ok else 'MISS'}]  "
            f"depth_own {dep:.3f} on {share:.1%} of days (g* {gstar:.3f})")
    shelf = pd.DataFrame(shelf_rows)
    shelf.to_csv(OUT / f"{STEM}.shelf.csv", index=False)
    log(f"  G8 {int(shelf.G8.sum())} of {len(shelf)} books reproduce their memo triple "
        f"[{'PASS' if shelf.G8.all() else 'PARTIAL - misses marked UNVERIFIED below'}]")

    # ------------------------------------------------------------------ (B) the depth law
    arms, ex, benches = [], [], []
    g2m = d4m = 0.0
    kmv = 0
    for n_, p in panels.items():
        a, e, b, g2, d4, km = run_panel(n_, p)
        arms.append(a)
        ex.append(e)
        benches.append(b)
        g2m, d4m = max(g2m, g2), max(d4m, d4)
        kmv += km
    arms = pd.concat(arms, ignore_index=True)
    ex = pd.concat(ex, ignore_index=True)
    bench = pd.DataFrame(benches).set_index("panel")
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    ex.to_csv(OUT / f"{STEM}.excess.csv", index=False)
    log(f"\n  arms {len(arms)} rows, excess {len(ex)} rows  ({time.time()-t0:.0f}s)")
    log(f"  G2 rate match  max|mean(placebo) - mean(real)| {g2m:.3e}  bar 1e-12  "
        f"[{'PASS' if g2m < 1e-12 else 'FAIL'}]")
    log(f"  G4 determinism max|d| {d4m:.3e}  bar 0  [{'PASS' if d4m == 0.0 else 'FAIL'}]")
    log(f"  G5 on REAL arms: k/m violations across switch-matched cells: {kmv} of "
        f"{len(SMKINDS)*len(arms)*NSEED}  [{'PASS' if kmv == 0 else 'FAIL'}]")

    key = ["panel", "family", "q", "w", "depth", "cadence", "gross"]
    piv = ex.pivot_table(index=key, columns="kind",
                         values=[f"excess_{c}bps" for c in RUNGS]
                         + [f"seedsd_{c}bps" for c in RUNGS]
                         + ["excess_IS", "excess_OOS", "sd_runlen_ratio", "sw_ratio",
                            "max_run_ratio", "pvol_10bps"])
    gap = pd.DataFrame(index=piv.index)
    for kind in KINDS:
        for c in RUNGS:
            gap[f"{kind}_ex_{c}"] = piv[(f"excess_{c}bps", kind)]
            gap[f"{kind}_sd_{c}"] = piv[(f"seedsd_{c}bps", kind)]
        for f in ("sd_runlen_ratio", "sw_ratio", "max_run_ratio", "pvol_10bps"):
            gap[f"{kind}_{f}"] = piv[(f, kind)]
        gap[f"{kind}_IS"] = piv[("excess_IS", kind)]
        gap[f"{kind}_OOS"] = piv[("excess_OOS", kind)]
    OTHERS = [k for k in KINDS if k != "BLOCK"]
    for kind in OTHERS:
        for c in RUNGS:
            gap[f"s_{kind}_{c}"] = gap[f"{kind}_ex_{c}"] - gap[f"BLOCK_ex_{c}"]
            gap[f"d_{kind}_{c}"] = gap[f"s_{kind}_{c}"].abs()
        gap[f"dIS_{kind}"] = gap[f"{kind}_IS"] - gap["BLOCK_IS"]
        gap[f"dOOS_{kind}"] = gap[f"{kind}_OOS"] - gap["BLOCK_OOS"]
    gap = gap.reset_index()
    gap.to_csv(OUT / f"{STEM}.gap.csv", index=False)

    def signed(kind, c=10, sub=None):
        s = (gap if sub is None else sub)[f"s_{kind}_{c}"]
        med, mean = float(s.median()), float(s.mean())
        se = float(s.std(ddof=1) / np.sqrt(len(s)))
        below = float((s < 0).mean())
        z = (below - 0.5) / np.sqrt(0.25 / len(s))
        return med, mean, se, below, z

    log("\n" + "=" * 100)
    log("[1] G7 CALIBRATION - BLOCK2 differs from BLOCK ONLY BY SEED, so its true gap is ZERO")
    log("=" * 100)
    b2 = signed("BLOCK2")
    log(f"  BLOCK2 pooled signed median {b2[0]:+.5f}  mean {b2[1]:+.5f} (SE {b2[2]:.5f})  "
        f"share below BLOCK {b2[3]:.1%}  sign-test z {b2[4]:+.2f}")
    g7 = abs(b2[0]) <= CAL_BAR and abs(b2[4]) < CAL_Z
    log(f"  G7 |signed| <= {CAL_BAR} and |z| < {CAL_Z}  [{'PASS' if g7 else 'FAIL'}]  "
        f"-> BAND for every reading below")
    log("  per depth rung (the band must itself be depth-free, or the law below is unreadable):")
    for d in DEPTHS:
        s = signed("BLOCK2", 10, gap[gap.depth == d])
        log(f"    d={d:.2f}  signed {s[0]:+.5f}  z {s[4]:+.2f}  n {int((gap.depth==d).sum())}")

    log("\n" + "=" * 100)
    log("[2] G3 REPRODUCTION OF IDEA 881's TWO PUBLISHED DEPTH CUTS")
    log("=" * 100)
    g3ok = True
    for d in (1.00, 0.50):
        s = signed("SM_DOM", 10, gap[gap.depth == d])
        hit = abs(s[0] - PUB881[d]) <= SIGN_BAR
        g3ok &= hit
        log(f"  depth {d:.2f}: published {PUB881[d]:+.5f} (z {PUB881_Z[d]:+.2f})  here "
            f"{s[0]:+.5f} (z {s[4]:+.2f})  |d| {abs(s[0]-PUB881[d]):.5f}  bar {SIGN_BAR}  "
            f"[{'PASS' if hit else 'MISS'}]")
    disp = float(gap["SM_DOM_sd_runlen_ratio"].mean())
    okd = abs(disp - PUB881_DISP) <= DISP_BAR
    g3ok &= okd
    log(f"  SM_DOM dispersion ratio {disp:.2f}x vs published {PUB881_DISP}x  "
        f"[{'PASS' if okd else 'MISS'}]")
    zz = signed("SM_DOM", 10, gap[gap.depth == 1.00])[4]
    log(f"  G3 overall [{'PASS' if g3ok and zz >= Z_BAR else 'PARTIAL'}]  (depth-1.00 z {zz:+.2f}, "
        f"bar +{Z_BAR})")

    log("\n" + "=" * 100)
    log("[3] H_LAW - THE DEPTH LAW.  gap(d) for SM_DOM, all four rungs, all three cost rungs")
    log("    A (1-d) multiplier scales the book's return on firing days, so a MEAN-return effect")
    log("    must be proportional to d and must vanish as d -> 0.")
    log("=" * 100)
    log(f"  {'depth':>7s}{'n arms':>8s}" + "".join(f"{'signed@'+str(c):>13s}" for c in RUNGS)
        + f"{'z@10':>8s}{'gap/d':>10s}{'|gap|':>9s}{'seed SE':>10s}{'band':>9s}")
    law = []
    for d in DEPTHS:
        sub = gap[gap.depth == d]
        vals = {c: signed("SM_DOM", c, sub) for c in RUNGS}
        s10 = vals[10]
        inside = abs(s10[0]) <= CAL_BAR and abs(s10[4]) < CAL_Z
        law.append(dict(depth=d, n=len(sub), signed_0=vals[0][0], signed_10=s10[0],
                        signed_25=vals[25][0], mean_10=s10[1], se_10=s10[2], z_10=s10[4],
                        ratio=s10[0] / d, inside_band=inside,
                        pvol=float(sub["SM_DOM_pvol_10bps"].mean()),
                        maxrun=float(sub["SM_DOM_max_run_ratio"].mean())))
        log(f"  {d:7.2f}{len(sub):8d}" + "".join(f"{vals[c][0]:+13.5f}" for c in RUNGS)
            + f"{s10[4]:+8.2f}{s10[0]/d:+10.5f}{abs(s10[0]):9.5f}{s10[2]:10.5f}"
            + f"{'INSIDE' if inside else 'OUTSIDE':>9s}")
    law = pd.DataFrame(law)
    law.to_csv(OUT / f"{STEM}.depthlaw.csv", index=False)
    rat = law.ratio.values
    dev = float(np.max(np.abs(rat - rat.mean())) / abs(rat.mean()))
    dv, gv = law.depth.values, law.signed_10.values
    beta = float((dv * gv).sum() / (dv * dv).sum())
    ss_res = float(((gv - beta * dv) ** 2).sum())
    ss_tot = float(((gv - gv.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    log(f"  gap/d across the four rungs: " + "  ".join(f"{v:+.5f}" for v in rat)
        + f"   max deviation from mean {dev:.1%}  (bar 25%)")
    log(f"  through-origin fit  gap(d) = {beta:+.5f} * d    R^2 {r2:.3f}  (bar 0.90)")
    h_law = dev <= 0.25 and r2 >= 0.90
    log(f"  H_LAW {'CONFIRMED' if h_law else 'REFUTED'}  -> the bias {'IS' if h_law else 'is NOT'}"
        f" proportional to de-grossing depth with no fixed component")
    log(f"  placebo annualised vol by depth: " + "  ".join(f"d{d:.2f} {v:.4f}" for d, v
                                                           in zip(law.depth, law.pvol)))
    log("  (881's [6b]: vol is flat across NULLS at a depth, so the gap is a MEAN-return effect;")
    log("   here it is read ACROSS depths, where vol necessarily falls as the book de-grosses.)")

    log("\n" + "=" * 100)
    log("[4] H_ART - THE QUEUE'S TITLE.  Is the defect a DEPTH-1.00 artefact?")
    log("=" * 100)
    lo = law[law.depth <= 0.50]
    hi = law[law.depth == 1.00]
    h_art = bool(lo.inside_band.all() and (not hi.inside_band.iloc[0]))
    for _, r in law.iterrows():
        log(f"  d={r.depth:.2f}  signed {r.signed_10:+.5f}  z {r.z_10:+.2f}  "
            f"{'INSIDE the BLOCK2 band (UNRESOLVABLE)' if r.inside_band else 'OUTSIDE (resolved)'}")
    log(f"  H_ART {'CONFIRMED' if h_art else 'REFUTED'}  -> at d <= 0.50 the run-shape defect is "
        f"{'not measurable' if h_art else 'still measurable'} against this record's own seed noise")

    log("\n" + "=" * 100)
    log("[5] H_BOOK - THE EXPOSURE RE-READ AT EACH SHELF BOOK'S OWN DEPTH")
    log("    predicted bias = beta * depth_own, with beta from [3]'s through-origin fit;")
    log("    resolution = the BLOCK2 band (0.0010 of Sharpe) measured in [1].")
    log("=" * 100)
    log(f"  {'book':36s}{'depth_own':>11s}{'days dg':>9s}{'pred bias':>12s}{'vs band':>10s}"
        f"{'G8':>7s}")
    nb_small = 0
    preds = []
    for _, r in shelf.iterrows():
        pred = beta * (r.depth_own if np.isfinite(r.depth_own) else 0.0)
        small = abs(pred) < CAL_BAR
        nb_small += int(small)
        preds.append(pred)
        log(f"  {r.book:36s}{r.depth_own:11.3f}{r.degross_day_share:9.1%}{pred:+12.5f}"
            f"{'BELOW' if small else 'ABOVE':>10s}{'ok' if r.G8 else 'UNVER':>7s}")
    shelf["pred_bias"] = preds
    shelf.to_csv(OUT / f"{STEM}.shelf.csv", index=False)
    h_book = nb_small > len(shelf) / 2
    log(f"  {nb_small} of {len(shelf)} shelf books sit below the record's own resolution")
    log(f"  H_BOOK {'CONFIRMED' if h_book else 'REFUTED'}")
    log("  NOTE: a book with NO macro gate de-grosses only through its own eligibility mask;")
    log("  depth_own measures that directly from the book's exposure path and is not assumed.")

    log("\n" + "=" * 100)
    log("[6] H_COSTINV - switch counts are matched, so the depth law must not be a cost story")
    log("=" * 100)
    worst = 0.0
    for d in DEPTHS:
        sub = gap[gap.depth == d]
        v = [signed("SM_DOM", c, sub)[0] for c in RUNGS]
        rg = max(v) - min(v)
        worst = max(worst, rg)
        log(f"  d={d:.2f}  0/10/25 bps {v[0]:+.5f} / {v[1]:+.5f} / {v[2]:+.5f}   range {rg:.5f}"
            f"   switch ratio {sub['SM_DOM_sw_ratio'].mean():.2f}x")
    log(f"  RAND (unmatched switches) for contrast: " + " / ".join(
        f"{signed('RAND', c)[0]:+.5f}" for c in RUNGS)
        + f"   switch ratio {gap['RAND_sw_ratio'].mean():.1f}x")
    h_cost = worst < 0.005
    log(f"  H_COSTINV (worst range {worst:.5f} < 0.005): {'CONFIRMED' if h_cost else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[7] ALL GRID POINTS - signed gap by depth x panel x cadence x gross (nothing selected)")
    log("=" * 100)
    for cut in ("panel", "cadence", "gross"):
        log(f"  by {cut}:")
        for v, sub0 in gap.groupby(cut):
            line = f"    {cut}={v!s:6s}"
            for d in DEPTHS:
                s = signed("SM_DOM", 10, sub0[sub0.depth == d])
                line += f"  d{d:.2f} {s[0]:+.5f} (z{s[4]:+5.2f})"
            log(line)
    log("  by family (depth 1.00 / 0.50 / 0.25):")
    for fam, sub0 in gap.groupby("family"):
        log(f"    {fam:12s}" + "".join(
            f"  d{d:.2f} {signed('SM_DOM', 10, sub0[sub0.depth == d])[0]:+.5f}"
            for d in (1.00, 0.50, 0.25)))
    log("  SM_UNIF (875's clean control) by depth:")
    for d in DEPTHS:
        s = signed("SM_UNIF", 10, gap[gap.depth == d])
        log(f"    d={d:.2f}  signed {s[0]:+.5f}  z {s[4]:+.2f}")

    log("\n" + "=" * 100)
    log("[8] RULE 8 (a) - DOES THE SIGNED GAP WALK FORWARD?  (IS fitted, OOS read once)")
    log("=" * 100)
    wf = []
    for kind in ("SM_DOM", "SM_UNIF", "BLOCK2", "RAND"):
        for d in DEPTHS:
            sub = gap[gap.depth == d]
            n_ok = 0
            for fam, g_ in sub.groupby("family"):
                rho = spearman(g_[f"dIS_{kind}"], g_[f"dOOS_{kind}"])
                wf.append(dict(kind=kind, depth=d, family=fam, rho=rho,
                               IS_median=float(g_[f"dIS_{kind}"].median()),
                               OOS_median=float(g_[f"dOOS_{kind}"].median())))
                n_ok += int(rho >= 0.30)
            log(f"  {kind:8s} d={d:.2f}  rho(IS,OOS) >= +0.30 in {n_ok} of 8 families   "
                f"IS median {sub[f'dIS_{kind}'].median():+.5f}   "
                f"OOS median {sub[f'dOOS_{kind}'].median():+.5f}"
                + ("   <- H_WF" if (kind == "SM_DOM" and d == 1.00) else ""))
            if kind == "SM_DOM" and d == 1.00:
                h_wf = n_ok >= 6
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    log(f"  H_WF {'CONFIRMED' if h_wf else 'REFUTED'}")

    log("\n" + "=" * 100)
    log("[9] RULE 8 (b) - THE BOOKS: IS-only selector, OOS read once, BOTH KEEP PATHS")
    log("=" * 100)
    sel = []
    for pn, g_ in arms.groupby("panel"):
        b = bench.loc[pn]
        pick = g_.loc[g_.IS_Sharpe.idxmax()]
        p4a = bool(pick.H1 > b.bl_h1 and pick.H2 > b.bl_h2 and pick.MaxDD >= b.bl_dd)
        p4b = bool(pick.H1 > b.spy_h1 and pick.H2 > b.spy_h2
                   and pick.OOS_Sharpe > b.spy_oos_s
                   and pick.MaxDD >= 0.60 * b.spy_dd and pick.CAGR >= 0.70 * b.spy_cagr)
        sel.append(dict(panel=pn, arm=f"{pick.family} q{pick.q} w{pick.w} d{pick.depth} "
                                      f"{pick.cadence} g{pick.gross}",
                        CAGR=pick.CAGR, Sharpe=pick.Sharpe, MaxDD=pick.MaxDD, H1=pick.H1,
                        H2=pick.H2, OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                        OOS_MaxDD=pick.OOS_MaxDD, p4a=p4a, p4b=p4b))
        log(f"  {pn}: IS-pick {sel[-1]['arm']}")
        log(f"     FULL {pick.CAGR:.2%} / {pick.Sharpe:.3f} / {pick.MaxDD:.2%}  halves "
            f"{pick.H1:.3f}/{pick.H2:.3f}   OOS {pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.3f} / "
            f"{pick.OOS_MaxDD:.2%}")
        log(f"     RULES v2 (live) {b.bl_cagr:.2%} / {b.bl_sh:.3f} / {b.bl_dd:.2%}  halves "
            f"{b.bl_h1:.3f}/{b.bl_h2:.3f}  OOS {b.bl_oos_c:.2%} / {b.bl_oos_s:.3f} / "
            f"{b.bl_oos_d:.2%}")
        log(f"     SPY            {b.spy_cagr:.2%} / {b.spy_sh:.3f} / {b.spy_dd:.2%}  halves "
            f"{b.spy_h1:.3f}/{b.spy_h2:.3f}  OOS {b.spy_oos_c:.2%} / {b.spy_oos_s:.3f} / "
            f"{b.spy_oos_d:.2%}")
        log(f"     4b bars: DD >= {0.60*b.spy_dd:.2%}, CAGR >= {0.70*b.spy_cagr:.2%}, "
            f"OOS Sharpe > {b.spy_oos_s:.3f}")
        log(f"     4a {'PASS' if p4a else 'fail'}   4b {'PASS' if p4b else 'fail'}")
        n4a = n4b = 0
        for _, r in g_.iterrows():
            n4a += int(r.H1 > b.bl_h1 and r.H2 > b.bl_h2 and r.MaxDD >= b.bl_dd)
            n4b += int(r.H1 > b.spy_h1 and r.H2 > b.spy_h2 and r.OOS_Sharpe > b.spy_oos_s
                       and r.MaxDD >= 0.60 * b.spy_dd and r.CAGR >= 0.70 * b.spy_cagr)
        log(f"     unselected base rate over {len(g_)} arms: 4a {n4a} ({n4a/len(g_):.1%}), "
            f"4b {n4b} ({n4b/len(g_):.1%})")
    pd.DataFrame(sel).to_csv(OUT / f"{STEM}.books.csv", index=False)

    log("\n" + "=" * 100)
    log("[10] SUMMARY OF PRE-REGISTERED HYPOTHESES")
    log("=" * 100)
    for nm, v in (("H_LAW", h_law), ("H_ART", h_art), ("H_BOOK", h_book),
                  ("H_CENSUS", h_census), ("H_COSTINV", h_cost), ("H_WF", h_wf)):
        log(f"  {nm:10s} {'CONFIRMED' if v else 'REFUTED'}")
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
