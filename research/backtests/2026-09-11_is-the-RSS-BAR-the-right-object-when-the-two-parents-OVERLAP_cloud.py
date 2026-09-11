#!/usr/bin/env python3
"""Idea 778 (cloud, 2026-09-11) - is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP.

QUESTION
--------
Idea 774 (lane C, same day) re-scored 607 committed panel-ordering claims against each
claim's own named-parent floor and found the statistically "correct" bar for a gap between
two parents is the root-sum-square RSS = sqrt(f_a^2 + f_b^2).  That bar CONVICTS 41 more
claims than idea 567's pooled bar and acquits none.  But RSS is the sd of a difference of
INDEPENDENT draws.  The queue's objection: U56's names are largely a subset of B136's, so
the two parents' composition luck is positively correlated, Var(X_a - X_b) =
f_a^2 + f_b^2 - 2*rho*f_a*f_b < RSS^2, and the +41 conviction count is inflated by a bar
that is too wide.  This run measures the cross-parent draw correlation DIRECTLY (same k,
overlap-preserving coupling) and re-issues the conviction count at the corrected bar.

THE STRUCTURAL FACT THIS RUN ESTABLISHES FIRST (gate G5)
-------------------------------------------------------
The three real parents are not "partially overlapping".  Measured from the committed
panels: U56 has 55 stocks and ALL 55 are in B136's 135 - complete nesting, overlap
coefficient 1.000 - while SMALL439 is DISJOINT from both (0 shared names).  So the queue's
premise applies to exactly one of the three parent pairs, and RSS is exactly right for the
other two.  Of the 607 claims, 490 (228 two-panel B136+U56 plus 262 three-panel) name the
nested pair.

WHY INDEPENDENT SEEDS CANNOT MEASURE THE CORRELATION (and what this run does instead)
------------------------------------------------------------------------------------
With the price history fixed, two draws taken with INDEPENDENT seeds have exactly zero
covariance whatever the pools share - drawing S_b never looks at S_a.  Pairing idea 774's
own draws by seed index therefore estimates rho ~ 0 by construction, which is why RSS looked
correct.  The correlation the queue is asking about is a property of the COUPLING, not of
the pools: the real U56/B136 pair is two views of ONE set of names, so a re-roll of
composition must move both panels together.  This run builds that coupling explicitly - a
COMMON RANDOM PERMUTATION of the union pool, from which each parent takes the first k of its
own members - so a name that ranks early is in both draws whenever both pools contain it.
For disjoint pools the same construction yields zero shared names and rho ~ 0, so the
estimator degrades gracefully to RSS exactly where RSS is right.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. CORRELATION ESTIMATOR in {RSS_INDEP, PAIR_INDEP, PAIR_SEED, PAIR_COUPLED, PAIR_DIRECT}
         RSS_INDEP    sqrt(sum f_i^2) over ALL named parents         (idea 774's incumbent)
         PAIR_INDEP   sqrt(f_i^2 + f_j^2) for the MIN-GAP pair only  (isolates pair-vs-all)
         PAIR_SEED    rho from same-index INDEPENDENT seed pairs     (the null control)
         PAIR_COUPLED rho from the overlap-preserving coupled ensemble
         PAIR_DIRECT  sd of (X_i - X_j) measured on that ensemble    (no rho, no normality)
    2. BAR b in {1.0, 2.0} sd
All 5 x 2 = 10 grid points are reported, for every statistic family and every draw count.
REPORTED (never selected) axes: statistic family (5), draw count D in {3, 6, 12, 24}, period
    (FULL / IS / OOS), gross g in {0.50, 0.75, 1.00}, cadence in {W, M}.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
H_RHO   : the coupled cross-parent draw correlation is materially positive for the NESTED
          pair (rho > 0.20 for U56/B136 at PREM_SHARPE, D=6, FULL) and ~ 0 for both DISJOINT
          pairs (|rho| < 0.20).  Falsified if the nested pair's rho is not positive.
H_ZERO  : pairing INDEPENDENT draws by seed index estimates rho indistinguishable from zero
          (|rho_seed| < 2/sqrt(D) for every pair), i.e. the whole correction is a coupling
          fact and idea 774's RSS is the right bar for independent draws.
H_SHRINK: the queue's implied direction - correcting for the correlation shrinks idea 774's
          +41 conviction count by more than half (net vs POOLED < +20 at PAIR_COUPLED, D=6,
          bar 1.0).  Falsified if the corrected bar convicts as hard or harder.

GATES (pre-registered, run and printed before any new number is read)
    G1 harvest     : a fresh harvest of the committed record reproduces every one of idea
                     567/774's 607 census rows exactly.                        bar 607 of 607
    G2 floors      : per-parent floors rebuilt from prices match idea 774's committed
                     .floors.csv on all 60 (statistic, D, period) rows.               bar 1e-12
    G3 identity    : fast_backtest vs engine.backtest on one book per parent.         bar 1e-12
    G4 headlines   : idea 774's published movement numbers (POOLED 259 inside of 607,
                     MIN -8, MEAN +0, MAX +8, RSS +41, RSS share 0.4942) re-derived from its
                     OWN committed .moves.csv / .rescore.csv.                          bar 1e-3
    G5 structure   : the parent overlap matrix (U56 nested in B136, SMALL disjoint), asserted
                     from the committed panels, not assumed.                       bar exact

RULE 8 WALK-FORWARD (required, run whatever the census says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: rebuild floors AND both correlation estimators on IS returns only and
       on OOS returns only, re-score the census at all 10 grid points in each period, and
       report whether the corrected conviction count is the same object out of sample.
    WF-B on a BOOK: the corrected bar is a DECISION RULE, so it is priced as one.  In each
       (gross, cadence) cell rank the three parents by IS MA-gate premium; ACT on the IS-best
       parent (trade MA-RS there) only if the IS span between the best and worst parent
       clears bar b times THAT PAIR's corrected difference-sd, else STAND DOWN to the live
       book (RULES v2 on U56).  OOS is read ONCE for all 10 decision books and compared to
       RULES v2 U56 and SPY.  Idea 774's always-act rule is the control.
    KEEP paths 4a and 4b are evaluated for every book on the price grid (REAL panels, idea
       774's independent draws, and this run's coupled pair draws) AND for every decision
       book.  Stated up front: a DRAW panel is a seeded random 36-name subset, not a rule
       anyone can trade, so a 4b pass on a draw is a diagnostic, not a candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, so every
    stock-side level carries a survivorship premium; the LEVEL floors (SHARPE, CAGR, MAXDD)
    are lower bounds on true dispersion.  An arm-minus-arm premium on the same panel largely
    cancels it.  The small panel additionally drops every ticker with max_1d_move >= 1.0.
    The three parents also start on different dates (U56/B136 2008, SMALL 2010), which is
    inherited from idea 567's floor construction and noted wherever a cross-parent
    correlation is quoted.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and committed artefacts of
ideas 567/774; modifies nothing but its own outputs:
    .grid.csv .floors.csv .rho.csv .census.csv .rescore.csv .moves.csv .walkforward.csv
    .keeppaths.csv .console.txt
"""
from __future__ import annotations

import collections
import itertools
import re
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent

COST = 10.0
MA_WIN = 200
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
K_DRAW = 36
N_SEED = 24
DRAW_COUNTS = [3, 6, 12, 24]
BARS = [1.0, 2.0]
ESTS = ["RSS_INDEP", "PAIR_INDEP", "PAIR_SEED", "PAIR_COUPLED", "PAIR_DIRECT"]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
PERIODS = ("FULL", "IS", "OOS")

P774 = OUT / "2026-09-11_how-many-of-the-record-s-TWO-PANEL-claims-would-flip-under-a-PARENT-SPECIFIC-floor_C"
# idea 774's published movement headlines (its result.md / LEADERBOARD rows)
PUB774 = dict(n=607, pooled_inside=259, net_MIN=-8, net_MEAN=0, net_MAX=8, net_RSS=41,
              share_RSS=0.4942, share_POOLED=0.4267, share_MIN=0.4135, share_MAX=0.4399)
TOL = 1e-12
G4_TOL = 1e-3

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G3)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return {
        "U56": (px56.dropna(how="all").ffill(), sorted(set(px56.columns) - {"SPY"})),
        "B136": (px136.dropna(how="all").ffill(), sorted(set(px136.columns) - {"SPY"})),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), sorted(s_stk)),
    }


def draws(parent, names, n_seed=N_SEED, k=K_DRAW):
    """crc32-seeded k-matched INDEPENDENT draws, `DRAW|{parent}|{seed}` (312/567/774 scheme)."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


def coupled_draws(pa, na, pb, nb, n_seed=N_SEED, k=K_DRAW):
    """Overlap-PRESERVING coupled draws: one common random permutation of the union pool,
    each parent takes the first k of its OWN members.  Shared names appear in both draws
    exactly when both pools contain them, so nested pools give a positive correlation and
    disjoint pools give zero shared names by construction."""
    union = sorted(set(na) | set(nb))
    sa, sb = set(na), set(nb)
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"PAIRDRAW|{pa}|{pb}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        perm = rng.permutation(np.array(union))
        ia = [x for x in perm if x in sa][:k]
        ib = [x for x in perm if x in sb][:k]
        out.append((sd, sorted(ia), sorted(ib), len(set(ia) & set(ib))))
    return out


# ------------------------------------------------------------------------- census
# idea 567/774's harvester, verbatim, plus ONE added column: the MIN-GAP pair.
PANELS_RE = re.compile(r"\b(U56|B136|SMALL\d{2,4}|SMALL)\b")
NUM_RE = re.compile(r"[-+]?\d*\.\d+|[-+]?\d+")
FAMILY_KEYS = [
    ("PREM_SHARPE", ("premium", "dsharpe", "d sharpe", "advantage", "gate premium", "selection")),
    ("PREM_CAGR", ("dcagr", "d cagr", "pp/yr", "pp / yr")),
    ("SHARPE", ("sharpe",)),
    ("CAGR", ("cagr", "return")),
    ("MAXDD", ("maxdd", "max dd", "drawdown", "dd")),
]


def classify(text):
    t = text.lower()
    for fam, keys in FAMILY_KEYS:
        if any(k in t for k in keys):
            return fam
    return None


def sentences(txt):
    txt = txt.replace("\n", " ")
    return re.split(r"(?<=[.;!?])\s+|\|", txt)


def harvest(paths):
    """Committed sentences quoting a number against >=2 of the three panels."""
    rows = []
    for p in paths:
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for s in sentences(txt):
            if len(s) > 600:
                continue
            found = PANELS_RE.findall(s)
            fams = {("SMALL" if f.startswith("SMALL") else f) for f in found}
            if len(fams) < 2:
                continue
            fam = classify(s)
            if fam is None:
                continue
            vals = {}
            for m in PANELS_RE.finditer(s):
                key = "SMALL" if m.group(1).startswith("SMALL") else m.group(1)
                tail = s[m.end(): m.end() + 40]
                nums = [float(x) for x in NUM_RE.findall(tail)
                        if not re.fullmatch(r"[-+]?\d{2,4}", x)]
                if nums and key not in vals:
                    vals[key] = nums[0]
            if len(vals) < 2:
                continue
            pairs = sorted(vals.items(), key=lambda kv: kv[1])
            order = [v for _, v in pairs]
            gaps = [b - a for a, b in zip(order, order[1:])]
            margin = min(gaps) if gaps else np.nan
            if not np.isfinite(margin):
                continue
            j = int(np.argmin(gaps))                       # the adjacent pair that IS the margin
            mpair = "|".join(sorted((pairs[j][0], pairs[j + 1][0])))
            rows.append(dict(file=p.name, family=fam, n_panels=len(vals),
                             margin=abs(margin), span=abs(order[-1] - order[0]),
                             parents="+".join(sorted(vals)), mpair=mpair,
                             claim=s.strip()[:240]))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------- bars
def pkey(name, small_name):
    return small_name if name == "SMALL" else name


def bar_for(named, mpair, stat, est, floors_pp, rho_seed, rho_cpl, direct, small_name):
    """The bar a claim is scored against, under correlation estimator `est`."""
    f = floors_pp[stat]
    if est == "RSS_INDEP":
        v = [f[pkey(p, small_name)] for p in named if pkey(p, small_name) in f]
        return float(np.sqrt(np.sum(np.square(v)))) if v else np.nan
    i, j = [pkey(x, small_name) for x in mpair.split("|")]
    if i not in f or j not in f:
        return np.nan
    key = tuple(sorted((i, j)))
    if est == "PAIR_DIRECT":
        return float(direct[stat].get(key, np.nan))
    rho = 0.0
    if est == "PAIR_SEED":
        rho = float(rho_seed[stat].get(key, 0.0))
    elif est == "PAIR_COUPLED":
        rho = float(rho_cpl[stat].get(key, 0.0))
    fa, fb = float(f[i]), float(f[j])
    return float(np.sqrt(max(fa * fa + fb * fb - 2.0 * rho * fa * fb, 0.0)))


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 778 - is the RSS bar the right object when the two parents OVERLAP?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): CORRELATION ESTIMATOR in " + str(ESTS) + " x BAR in " + str(BARS)
      + "  -- all 10 points reported")
    P("")

    parents = real_panels()
    pnames = list(parents)
    small_name = [p for p in pnames if p.startswith("SMALL")][0]
    P("PARENTS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in parents.items()))
    P("")

    P("=" * 100)
    P("GATES (pre-registered; printed before any new number is read)")
    P("=" * 100)

    # ------------------------------------------------------------------ G5 structure
    P("G5 structure    : parent overlap matrix, measured from the committed panels")
    ov = {}
    for a, b in itertools.combinations(pnames, 2):
        A, B = set(parents[a][1]), set(parents[b][1])
        inter = len(A & B)
        coef = inter / min(len(A), len(B))
        ov[tuple(sorted((a, b)))] = coef
        P(f"                  {a:<9s} n={len(A):3d}  vs {b:<9s} n={len(B):3d}   shared {inter:3d}"
          f"   overlap coefficient {coef:.3f}"
          + ("   <- COMPLETE NESTING" if coef >= 0.999 else
             ("   <- DISJOINT" if inter == 0 else "")))
    nested = [k for k, v in ov.items() if v >= 0.999]
    disjoint = [k for k, v in ov.items() if v == 0.0]
    g5 = (len(nested) == 1 and len(disjoint) == 2)
    P(f"                  {len(nested)} nested pair, {len(disjoint)} disjoint pairs -> "
      f"{'PASS' if g5 else 'FAIL'}  (the queue's premise applies to 1 of 3 pairs)")

    # ------------------------------------------------------------------ G1 harvest
    paths = (sorted(OUT.glob("*.result.md")) + sorted(OUT.glob("*.memo.md"))
             + sorted(OUT.glob("*.md")) + sorted((ROOT / "research").glob("*.md")))
    paths = sorted({p for p in paths if p.is_file()})
    fresh = harvest(paths)
    old = pd.read_csv(f"{P774}.census.csv")

    def key(d):
        return list(zip(d.file, d.family, d.n_panels, d.margin.round(12), d.span.round(12),
                        d.claim.str[:200]))

    ca, cb = collections.Counter(key(old)), collections.Counter(key(fresh))
    g1 = sum(min(v, cb[k]) for k, v in ca.items())
    P(f"G1 harvest      : idea 567/774's committed census rows reproduced by a fresh harvest "
      f"of {len(paths)} committed markdown files: {g1} of {len(old)} "
      f"(this run harvests {len(fresh)}; the surplus is files committed after 774 ran) -> "
      f"{'PASS' if g1 == len(old) == PUB774['n'] else 'FAIL'}")

    look = {}
    for _, r in fresh.iterrows():
        look.setdefault((r.file, r.family, r.n_panels, round(r.margin, 12), round(r.span, 12)),
                        (r.parents, r.mpair))
    cen = old.copy()
    got = [look.get((r.file, r.family, r.n_panels, round(r.margin, 12), round(r.span, 12)),
                    (None, None)) for _, r in cen.iterrows()]
    cen["parents_r"] = [g[0] for g in got]
    cen["mpair"] = [g[1] for g in got]
    same = int((cen.parents_r.fillna("") == cen.parents.fillna("")).sum())
    P(f"                  min-gap pair attached to {int(cen.mpair.notna().sum())} of {len(cen)} "
      f"claims; re-harvested parent set agrees with 774's on {same} of {len(cen)}")

    # ------------------------------------------------------------------ G3 identity
    g3 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g3 = max(g3, float(np.abs(a.values - b.values).max()))
    P(f"G3 identity     : fast_backtest vs engine.backtest max |dret| = {g3:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g3 <= TOL else 'FAIL'}")

    # ------------------------------------------------------------------ G4 headlines
    mv_old = pd.read_csv(f"{P774}.moves.csv")
    rs_old = pd.read_csv(f"{P774}.rescore.csv")
    sel = mv_old[(mv_old.period == "FULL") & (mv_old.D == 6) & (mv_old.bar == 1.0)
                 & (mv_old.subset == "ALL")].set_index("assign")
    rsel = rs_old[(rs_old.period == "FULL") & (rs_old.D == 6) & (rs_old.bar == 1.0)
                  ].set_index("assign")
    g4 = [("pooled_inside", float(sel.loc["POOLED", "now_inside"]), float(PUB774["pooled_inside"])),
          ("net_MIN", float(sel.loc["MIN", "net"]), float(PUB774["net_MIN"])),
          ("net_MEAN", float(sel.loc["MEAN", "net"]), float(PUB774["net_MEAN"])),
          ("net_MAX", float(sel.loc["MAX", "net"]), float(PUB774["net_MAX"])),
          ("net_RSS", float(sel.loc["RSS", "net"]), float(PUB774["net_RSS"])),
          ("share_RSS", float(rsel.loc["RSS", "share"]), PUB774["share_RSS"]),
          ("share_POOLED", float(rsel.loc["POOLED", "share"]), PUB774["share_POOLED"]),
          ("share_MIN", float(rsel.loc["MIN", "share"]), PUB774["share_MIN"]),
          ("share_MAX", float(rsel.loc["MAX", "share"]), PUB774["share_MAX"])]
    worst = max(abs(a - b) for _, a, b in g4)
    for nm, a, b in g4:
        P(f"                  {nm:<16s} committed {a:9.4f} vs published {b:9.4f} |d| {abs(a-b):.4f}")
    P(f"G4 headlines    : idea 774's published movement numbers re-derived from its OWN "
      f"committed artefacts, max |d| = {worst:.3e} (bar {G4_TOL:.0e}) -> "
      f"{'PASS' if worst <= G4_TOL else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------ price leg
    P("=" * 100)
    P("PRICE LEG - REAL panels, idea 774's INDEPENDENT draws, and this run's COUPLED pair draws")
    P("=" * 100)
    rows = []
    spy_cache = {}

    def run_unit(pn, px, pick, kind, sd, pair=""):
        cols = list(dict.fromkeys(list(pick) + ["SPY"]))
        sub = px[cols].dropna(how="all").ffill()
        out = []
        for g in GROSS:
            bks = make_books(sub, set(pick), g)
            for cad in CADENCE:
                res = {a: fast_backtest(sub, w, freq=cad) for a, w in bks.items()}
                warm = sub.index[260]
                base = {a: r["returns"].loc[warm:] for a, r in res.items()}
                for arm in ("EWall", "MA-RS"):
                    r = base[arm]
                    d = rowify(r, res[arm]["turnover"].loc[warm:])
                    d.update(parent=pn, kind=kind, seed=sd, arm=arm, gross=g, cadence=cad,
                             k=len(pick), pair=pair)
                    d["dSharpe_vs_EWall"] = d["Sharpe"] - metrics(base["EWall"])["Sharpe"]
                    d["dCAGR_vs_EWall"] = d["CAGR"] - metrics(base["EWall"])["CAGR"]
                    d["IS_dSharpe"] = (metrics(r.loc[:IS_END])["Sharpe"]
                                       - metrics(base["EWall"].loc[:IS_END])["Sharpe"])
                    d["OOS_dSharpe"] = (metrics(r.loc[OOS_START:])["Sharpe"]
                                        - metrics(base["EWall"].loc[OOS_START:])["Sharpe"])
                    d["IS_dCAGR"] = (metrics(r.loc[:IS_END])["CAGR"]
                                     - metrics(base["EWall"].loc[:IS_END])["CAGR"])
                    d["OOS_dCAGR"] = (metrics(r.loc[OOS_START:])["CAGR"]
                                      - metrics(base["EWall"].loc[OOS_START:])["CAGR"])
                    out.append(d)
        return out

    for pn, (px, names) in parents.items():
        spy_cache[pn] = px["SPY"].pct_change().fillna(0.0)
        rows += run_unit(pn, px, sorted(names), "REAL", -1)
        for sd, pick in draws(pn, names):
            rows += run_unit(pn, px, pick, "DRAW", sd)
        P(f"  {pn}: 1 REAL + {N_SEED} independent draws x {len(GROSS)} gross x "
          f"{len(CADENCE)} cadence x 2 arms ({time.time()-t0:.0f}s)")

    ovl_rows = []
    for a, b in itertools.combinations(pnames, 2):
        pxa, na = parents[a]
        pxb, nb = parents[b]
        shares = []
        for sd, ia, ib, nshare in coupled_draws(a, na, b, nb):
            shares.append(nshare)
            rows += run_unit(a, pxa, ia, "CPL", sd, pair=f"{a}|{b}")
            rows += run_unit(b, pxb, ib, "CPL", sd, pair=f"{a}|{b}")
        ovl_rows.append(dict(pair=f"{a}|{b}", mean_shared=float(np.mean(shares)),
                             min_shared=int(np.min(shares)), max_shared=int(np.max(shares)),
                             k=K_DRAW, overlap_coef=ov[tuple(sorted((a, b)))]))
        P(f"  COUPLED {a}|{b}: {N_SEED} common-permutation pairs, shared names per pair "
          f"mean {np.mean(shares):.2f} of {K_DRAW} (min {np.min(shares)}, max {np.max(shares)})"
          f" ({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(rows)
    ovl = pd.DataFrame(ovl_rows)

    bases, spys = {}, {}
    P("")
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:]
        bases[pn] = b
        s = spy_cache[pn].loc[warm:]
        spys[pn] = s
        P(f"  BASE {pn}: RULES v2 {metrics(b)['CAGR']:.2%} / {metrics(b)['Sharpe']:.4f} / "
          f"{metrics(b)['MaxDD']:.2%} (OOS {metrics(b.loc[OOS_START:])['Sharpe']:.4f})   "
          f"SPY {metrics(s)['CAGR']:.2%} / {metrics(s)['Sharpe']:.4f} / "
          f"{metrics(s)['MaxDD']:.2%} (OOS {metrics(s.loc[OOS_START:])['Sharpe']:.4f})")
    P("")

    # ------------------------------------------------------------------ floors (G2)
    def stat_series(sub, stat, period="FULL"):
        """idea 567/774's statistic extractor, verbatim, keyed by seed."""
        pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
        ma = sub[sub.arm == "MA-RS"].set_index("seed")
        if stat == "PREM_SHARPE":
            col = {"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe", "OOS": "OOS_dSharpe"}[period]
            return ma[col]
        if stat == "PREM_CAGR":
            col = {"FULL": "dCAGR_vs_EWall", "IS": "IS_dCAGR", "OOS": "OOS_dCAGR"}[period]
            return ma[col]
        return ma[pre + {"SHARPE": "Sharpe", "CAGR": "CAGR", "MAXDD": "MaxDD"}[stat]]

    fl_rows = []
    dr = grid[grid.kind == "DRAW"]
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in PERIODS:
                per_parent = {}
                for pn in pnames:
                    vals = []
                    for g in GROSS:
                        for cad in CADENCE:
                            sub = dr[(dr.parent == pn) & (dr.gross == g) & (dr.cadence == cad)
                                     & (dr.seed < D)]
                            v = stat_series(sub, stat, period).to_numpy(float)
                            if len(v) >= 2:
                                vals.append(np.std(v, ddof=1))
                    per_parent[pn] = float(np.mean(vals)) if vals else np.nan
                row = dict(statistic=stat, D=D, period=period,
                           floor_pooled=float(np.nanmean(list(per_parent.values()))),
                           floor_max=float(np.nanmax(list(per_parent.values()))),
                           floor_min=float(np.nanmin(list(per_parent.values()))))
                row.update({f"floor_{k}": v for k, v in per_parent.items()})
                row["parent_ratio"] = (row["floor_max"] / row["floor_min"]
                                       if row["floor_min"] else np.nan)
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)
    fl_old = pd.read_csv(f"{P774}.floors.csv")
    mg = floors.merge(fl_old, on=["statistic", "D", "period"], suffixes=("_r", "_c"))
    assert len(mg) == len(fl_old) == len(floors), (len(mg), len(fl_old), len(floors))
    cols = ["floor_pooled", "floor_max", "floor_min"] + [f"floor_{p}" for p in pnames]
    g2 = max(float(np.abs(mg[c + "_r"] - mg[c + "_c"]).max()) for c in cols)
    P(f"G2 floors       : per-parent floors rebuilt from prices vs idea 774's committed "
      f".floors.csv, all {len(mg)} (statistic, D, period) rows, max |d| = {g2:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------ correlations
    P("=" * 100)
    P("CROSS-PARENT DRAW CORRELATION - measured directly, two ways (the queue's ask)")
    P("=" * 100)
    rho_rows = []
    cpl = grid[grid.kind == "CPL"]
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in PERIODS:
                for a, b in itertools.combinations(pnames, 2):
                    pr = f"{a}|{b}"
                    rs_c, rs_s, dd_c, dd_s, sa_l, sb_l = [], [], [], [], [], []
                    for g in GROSS:
                        for cad in CADENCE:
                            # coupled ensemble
                            xa = stat_series(cpl[(cpl.parent == a) & (cpl.pair == pr)
                                                 & (cpl.gross == g) & (cpl.cadence == cad)
                                                 & (cpl.seed < D)], stat, period)
                            xb = stat_series(cpl[(cpl.parent == b) & (cpl.pair == pr)
                                                 & (cpl.gross == g) & (cpl.cadence == cad)
                                                 & (cpl.seed < D)], stat, period)
                            xa, xb = xa.sort_index(), xb.sort_index()
                            if len(xa) >= 3 and len(xa) == len(xb):
                                va, vb = xa.to_numpy(float), xb.to_numpy(float)
                                if np.std(va) > 0 and np.std(vb) > 0:
                                    rs_c.append(float(np.corrcoef(va, vb)[0, 1]))
                                dd_c.append(float(np.std(va - vb, ddof=1)))
                                sa_l.append(float(np.std(va, ddof=1)))
                                sb_l.append(float(np.std(vb, ddof=1)))
                            # independent draws paired by seed index (the null control)
                            ya = stat_series(dr[(dr.parent == a) & (dr.gross == g)
                                                & (dr.cadence == cad) & (dr.seed < D)],
                                             stat, period).sort_index()
                            yb = stat_series(dr[(dr.parent == b) & (dr.gross == g)
                                                & (dr.cadence == cad) & (dr.seed < D)],
                                             stat, period).sort_index()
                            if len(ya) >= 3 and len(ya) == len(yb):
                                wa, wb = ya.to_numpy(float), yb.to_numpy(float)
                                if np.std(wa) > 0 and np.std(wb) > 0:
                                    rs_s.append(float(np.corrcoef(wa, wb)[0, 1]))
                                dd_s.append(float(np.std(wa - wb, ddof=1)))
                    rho_rows.append(dict(
                        statistic=stat, D=D, period=period, pair=pr,
                        rho_coupled=float(np.mean(rs_c)) if rs_c else np.nan,
                        rho_seed=float(np.mean(rs_s)) if rs_s else np.nan,
                        sd_diff_coupled=float(np.mean(dd_c)) if dd_c else np.nan,
                        sd_diff_seed=float(np.mean(dd_s)) if dd_s else np.nan,
                        sd_a_coupled=float(np.mean(sa_l)) if sa_l else np.nan,
                        sd_b_coupled=float(np.mean(sb_l)) if sb_l else np.nan,
                        overlap_coef=ov[tuple(sorted((a, b)))]))
    rho = pd.DataFrame(rho_rows)
    P("SHARED NAMES PER COUPLED PAIR (k = 36 each side)")
    P(fmt(ovl.set_index("pair"), 3))
    P("")
    P("CORRELATION at D=6, FULL period - rho_coupled (overlap-preserving) vs rho_seed (null)")
    hd = rho[(rho.D == 6) & (rho.period == "FULL")]
    P(fmt(hd.pivot_table(index="pair", columns="statistic",
                         values="rho_coupled")[STATS], 4))
    P("  rho_seed (INDEPENDENT draws paired by seed index - expected 0 by construction):")
    P(fmt(hd.pivot_table(index="pair", columns="statistic", values="rho_seed")[STATS], 4))
    P("")
    P("IMPLIED BAR at PREM_SHARPE, D=6, FULL (the object idea 774 quoted as RSS):")
    fs = floors[(floors.D == 6) & (floors.period == "FULL")].set_index("statistic")
    for a, b in itertools.combinations(pnames, 2):
        pr = f"{a}|{b}"
        fa, fb = float(fs.loc["PREM_SHARPE", f"floor_{a}"]), float(fs.loc["PREM_SHARPE", f"floor_{b}"])
        r_c = float(hd[(hd.pair == pr) & (hd.statistic == "PREM_SHARPE")].rho_coupled.iloc[0])
        r_s = float(hd[(hd.pair == pr) & (hd.statistic == "PREM_SHARPE")].rho_seed.iloc[0])
        d_c = float(hd[(hd.pair == pr) & (hd.statistic == "PREM_SHARPE")].sd_diff_coupled.iloc[0])
        rss = np.sqrt(fa * fa + fb * fb)
        cor = np.sqrt(max(fa * fa + fb * fb - 2 * r_c * fa * fb, 0.0))
        P(f"  {pr:<18s} f_a {fa:.4f}  f_b {fb:.4f}  RSS {rss:.4f}   rho_cpl {r_c:+.4f} -> "
          f"corrected {cor:.4f} ({cor/rss:.3f}x RSS)   DIRECT {d_c:.4f} ({d_c/rss:.3f}x)   "
          f"rho_seed {r_s:+.4f}")
    P("")

    # hypothesis H_RHO / H_ZERO
    nest_pair = "|".join(sorted(nested[0])) if nested else None
    nest_pair = next((f"{a}|{b}" for a, b in itertools.combinations(pnames, 2)
                      if ov[tuple(sorted((a, b)))] >= 0.999), None)
    r_nest = float(hd[(hd.pair == nest_pair) & (hd.statistic == "PREM_SHARPE")].rho_coupled.iloc[0])
    r_dis = [float(hd[(hd.pair == f"{a}|{b}") & (hd.statistic == "PREM_SHARPE")].rho_coupled.iloc[0])
             for a, b in itertools.combinations(pnames, 2) if ov[tuple(sorted((a, b)))] == 0.0]
    P(f"H_RHO   : nested pair {nest_pair} rho_coupled = {r_nest:+.4f}; disjoint pairs "
      + ", ".join(f"{x:+.4f}" for x in r_dis)
      + f" -> {'HOLDS' if (r_nest > 0.20 and all(abs(x) < 0.20 for x in r_dis)) else 'FALSIFIED'}")
    seed_rhos = hd.rho_seed.dropna().to_numpy(float)
    zbar = 2.0 / np.sqrt(6)
    P(f"H_ZERO  : |rho_seed| over all pairs x statistics at D=6 FULL: max "
      f"{np.abs(seed_rhos).max():.4f}, mean {np.abs(seed_rhos).mean():.4f} vs bar "
      f"2/sqrt(D) = {zbar:.4f} -> "
      f"{'HOLDS - independent draws carry no correlation, RSS is right for them' if np.abs(seed_rhos).max() < zbar else 'FALSIFIED'}")
    P("")

    # lookup dicts per (stat, D, period)
    def maps(D, period):
        fsub = floors[(floors.D == D) & (floors.period == period)].set_index("statistic")
        fpp = {s: {p: float(fsub.loc[s, f"floor_{p}"]) for p in pnames} for s in STATS}
        rsub = rho[(rho.D == D) & (rho.period == period)]
        rs = {s: {} for s in STATS}
        rc = {s: {} for s in STATS}
        dd = {s: {} for s in STATS}
        for _, r in rsub.iterrows():
            k = tuple(sorted(r.pair.split("|")))
            rs[r.statistic][k] = 0.0 if not np.isfinite(r.rho_seed) else r.rho_seed
            rc[r.statistic][k] = 0.0 if not np.isfinite(r.rho_coupled) else r.rho_coupled
            dd[r.statistic][k] = r.sd_diff_coupled
        return fpp, rs, rc, dd

    # ------------------------------------------------------------------ RE-SCORE
    P("=" * 100)
    P("RE-SCORE - every claim at the correlation-corrected bar (10 tuned points, all shown)")
    P("=" * 100)
    cen = cen[cen.mpair.notna()].reset_index(drop=True)
    m0 = cen.margin.to_numpy(float)
    rs_rows, mv_rows = [], []
    for period in PERIODS:
        for D in DRAW_COUNTS:
            fpp, rs, rc, dd = maps(D, period)
            fl = {}
            for est in ESTS:
                fl[est] = np.array([bar_for(r.parents.split("+"), r.mpair, r.family, est,
                                            fpp, rs, rc, dd, small_name)
                                    for _, r in cen.iterrows()])
            # idea 567's POOLED incumbent, for the movement count
            pooled = np.array([float(np.nanmean(list(fpp[r.family].values())))
                               for _, r in cen.iterrows()])
            for est in ESTS:
                for b in BARS:
                    inside = m0 < b * fl[est]
                    was = m0 < b * pooled
                    was_rss = m0 < b * fl["RSS_INDEP"]
                    rs_rows.append(dict(
                        period=period, D=D, est=est, bar=b, n=len(cen),
                        inside=int(inside.sum()), share=float(inside.mean()),
                        nz_share=float(inside[(m0 > 0)].mean()),
                        two_share=float(inside[(cen.n_panels == 2).to_numpy()].mean()),
                        three_share=float(inside[(cen.n_panels == 3).to_numpy()].mean()),
                        two_nz=float(inside[((cen.n_panels == 2) & (cen.margin > 0)).to_numpy()].mean()),
                        three_nz=float(inside[((cen.n_panels == 3) & (cen.margin > 0)).to_numpy()].mean()),
                        mean_bar=float(np.nanmean(fl[est]))))
                    for sub_nm, msk in (("ALL", np.ones(len(cen), bool)),
                                        ("2PANEL", (cen.n_panels == 2).to_numpy()),
                                        ("3PANEL", (cen.n_panels == 3).to_numpy()),
                                        ("NESTED_PAIR", (cen.mpair == "|".join(
                                            sorted(["B136", "U56"]))).to_numpy())):
                        mv_rows.append(dict(
                            period=period, D=D, est=est, bar=b, subset=sub_nm,
                            n=int(msk.sum()),
                            was_inside=int(was[msk].sum()), now_inside=int(inside[msk].sum()),
                            to_inside=int((~was & inside)[msk].sum()),
                            to_outside=int((was & ~inside)[msk].sum()),
                            net=int((~was & inside)[msk].sum()) - int((was & ~inside)[msk].sum()),
                            net_vs_RSS=int(inside[msk].sum()) - int(was_rss[msk].sum()),
                            moved_share=float(((was != inside)[msk]).mean())))
                    if period == "FULL" and D == 6:
                        cen[f"inside_{est}_{b}"] = inside
    rescore = pd.DataFrame(rs_rows)
    moves = pd.DataFrame(mv_rows)

    head = rescore[(rescore.period == "FULL") & (rescore.D == 6)]
    P("HEADLINE GRID (D=6, FULL): share of the 607-claim census inside its bar")
    P(fmt(head.set_index(["est", "bar"])[["n", "inside", "share", "nz_share", "two_share",
                                          "three_share", "two_nz", "three_nz", "mean_bar"]], 4))
    P("")
    P("ALL DRAW COUNTS (FULL period, share inside)")
    P(fmt(rescore[rescore.period == "FULL"].pivot_table(index=["est", "bar"], columns="D",
                                                        values="share"), 4))
    P("")
    P("=" * 100)
    P("THE RE-ISSUED CONVICTION COUNT (net vs idea 567's POOLED bar; 774 published RSS +41)")
    P("=" * 100)
    hm = moves[(moves.period == "FULL") & (moves.D == 6)]
    for est in ESTS:
        for b in BARS:
            r = hm[(hm.est == est) & (hm.bar == b) & (hm.subset == "ALL")].iloc[0]
            P(f"  {est:<13s} bar {b:.1f}: inside {int(r.now_inside):3d}/{int(r.n)}  "
              f"OUT->IN {int(r.to_inside):3d}, IN->OUT {int(r.to_outside):3d}, "
              f"net vs POOLED {int(r.net):+4d}, net vs RSS {int(r.net_vs_RSS):+4d}, "
              f"moved {r.moved_share:.1%}")
    P("")
    P("BY SUBSET (D=6, FULL, bar 1.0): claims whose MIN-GAP pair is the NESTED pair vs the rest")
    P(fmt(hm[hm.bar == 1.0].pivot_table(index="est", columns="subset",
                                        values="now_inside", aggfunc="sum"), 1))
    P(fmt(hm[hm.bar == 1.0].pivot_table(index="est", columns="subset", values="n",
                                        aggfunc="first"), 0))
    P("")
    P("MIN-GAP PAIR DISTRIBUTION over the census")
    P(fmt(cen.groupby("mpair").size().rename("claims").to_frame(), 0))
    P("")

    rss_net = int(hm[(hm.est == "RSS_INDEP") & (hm.bar == 1.0) & (hm.subset == "ALL")].net.iloc[0])
    cpl_net = int(hm[(hm.est == "PAIR_COUPLED") & (hm.bar == 1.0) & (hm.subset == "ALL")].net.iloc[0])
    dir_net = int(hm[(hm.est == "PAIR_DIRECT") & (hm.bar == 1.0) & (hm.subset == "ALL")].net.iloc[0])
    pin_net = int(hm[(hm.est == "PAIR_INDEP") & (hm.bar == 1.0) & (hm.subset == "ALL")].net.iloc[0])
    P(f"H_SHRINK: idea 774's RSS net {rss_net:+d} (reproduced) -> PAIR_INDEP {pin_net:+d} -> "
      f"PAIR_COUPLED {cpl_net:+d} -> PAIR_DIRECT {dir_net:+d} -> "
      f"{'HOLDS - the corrected bar convicts less than half as hard' if cpl_net < 20 else 'FALSIFIED - the correction does NOT shrink the conviction count below +20'}")
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 100)
    P("KEEP PATHS over the full price grid (PROTOCOL rule 4a and 4b, every book)")
    P("=" * 100)
    kp_rows = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b, s = bases[pn], spys[pn]
        units = ([("REAL", -1, sorted(names), "")]
                 + [("DRAW", sd, pick, "") for sd, pick in draws(pn, names)])
        for a2, b2 in itertools.combinations(pnames, 2):
            if pn not in (a2, b2):
                continue
            for sd, ia, ib, _n in coupled_draws(a2, parents[a2][1], b2, parents[b2][1]):
                units.append(("CPL", sd, ia if pn == a2 else ib, f"{a2}|{b2}"))
        for kind, sd, pick, pair in units:
            cols = list(dict.fromkeys(list(pick) + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    for arm, w in bks.items():
                        r = fast_backtest(sub, w, freq=cad)["returns"].loc[warm:]
                        f4b = fail_4b(r, s)
                        kp_rows.append(dict(parent=pn, kind=kind, seed=sd, pair=pair, arm=arm,
                                            gross=g, cadence=cad, keep4a=keep_4a(r, b),
                                            fail4b=f4b, keep4b=(f4b == "-")))
    kp = pd.DataFrame(kp_rows)
    P(f"over {len(kp)} books: 4a {int(kp.keep4a.sum())}/{len(kp)}, "
      f"4b {int(kp.keep4b.sum())}/{len(kp)}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}/{len(kp)}")
    P("  by kind: " + ", ".join(
        f"{k} 4a {int(v.keep4a.sum())}/{len(v)} 4b {int(v.keep4b.sum())}/{len(v)}"
        for k, v in kp.groupby("kind")))
    P("  4b by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4b.sum().items()))
    real4b = [f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence}"
              for _, r in kp[(kp.kind == "REAL") & kp.keep4b].iterrows()]
    P("  4b REAL books: " + (", ".join(real4b) if real4b else "none"))
    P("  4b binding failure legs: " + ", ".join(
        f"{k} {v}" for k, v in kp.fail4b.value_counts().head(6).items()))
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P("WF-A: the ANSWER out of sample - floors AND correlations rebuilt on IS only / OOS only")
    wfa = rescore[(rescore.D == 6) & (rescore.bar == 1.0)].pivot_table(
        index="est", columns="period", values="share")
    P(fmt(wfa[["FULL", "IS", "OOS"]].loc[ESTS], 4))
    nets = moves[(moves.D == 6) & (moves.bar == 1.0) & (moves.subset == "ALL")].pivot_table(
        index="est", columns="period", values="net")
    P("  net conviction count vs POOLED, by period:")
    P(fmt(nets[["FULL", "IS", "OOS"]].loc[ESTS], 1))
    sign_ok = int(((np.sign(nets["IS"]) == np.sign(nets["OOS"])) | (nets["IS"] == 0)).sum())
    P(f"  direction agrees IS vs OOS for {sign_ok} of {len(nets)} estimators")
    rr = rho[(rho.D == 6) & (rho.statistic == "PREM_SHARPE")].pivot_table(
        index="pair", columns="period", values="rho_coupled")
    P("  rho_coupled (PREM_SHARPE, D=6) by period:")
    P(fmt(rr[["FULL", "IS", "OOS"]], 4))
    P("")

    P("WF-B: the corrected bar as a DECISION RULE, priced - act on the IS-best parent only if")
    P("      the IS span clears bar x THAT PAIR's corrected difference-sd, else stand down.")
    real = grid[grid.kind == "REAL"]
    u56 = "U56"
    base56, spy56 = bases[u56], spys[u56]
    oos_series, full_series = {}, {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        for g in GROSS:
            bks = make_books(px, set(names), g)
            for cad in CADENCE:
                r = fast_backtest(px, bks["MA-RS"], freq=cad)["returns"].loc[warm:]
                full_series[(pn, g, cad)] = r
                oos_series[(pn, g, cad)] = r.loc[OOS_START:]
    fppIS, rsIS, rcIS, ddIS = maps(6, "IS")

    def decide(est, b):
        picks, segsO, segsF, acted = [], [], [], 0
        for g in GROSS:
            for cad in CADENCE:
                prem = {pn: float(real[(real.parent == pn) & (real.gross == g)
                                       & (real.cadence == cad)
                                       & (real.arm == "MA-RS")].IS_dSharpe.iloc[0])
                        for pn in pnames}
                order = sorted(prem, key=prem.get, reverse=True)
                span = prem[order[0]] - prem[order[-1]]
                mp = "|".join(sorted((order[0], order[-1])))
                fl = bar_for([order[0], order[-1]], mp, "PREM_SHARPE", est,
                             fppIS, rsIS, rcIS, ddIS, small_name)
                act = span >= b * fl
                acted += int(act)
                picks.append(order[0] if act else "STANDDOWN")
                segsO.append(oos_series[(order[0], g, cad)] if act else base56.loc[OOS_START:])
                segsF.append(full_series[(order[0], g, cad)] if act else base56)
        mk = lambda segs: pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs],
                                    axis=1).mean(axis=1)
        return acted, picks, mk(segsO), mk(segsF)

    wf_rows, dk = [], []
    for est in ESTS:
        for b in BARS:
            acted, picks, bo, bf = decide(est, b)
            mo = metrics(bo)
            wf_rows.append(dict(est=est, bar=b, acted=acted, cells=len(picks),
                                picks="/".join(picks), OOS_CAGR=mo["CAGR"],
                                OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
            sp = spy56.reindex(bf.index).fillna(0.0)
            f4 = fail_4b(bf, sp)
            dk.append(dict(est=est, bar=b, CAGR=metrics(bf)["CAGR"], Sharpe=metrics(bf)["Sharpe"],
                           MaxDD=metrics(bf)["MaxDD"],
                           keep4a=keep_4a(bf, base56.reindex(bf.index).fillna(0.0)),
                           fail4b=f4, keep4b=(f4 == "-")))
    ctrl = []
    segs = [oos_series[(max(pnames, key=lambda pn: float(real[(real.parent == pn)
            & (real.gross == g) & (real.cadence == cad) & (real.arm == "MA-RS")]
            .IS_dSharpe.iloc[0])), g, cad)] for g in GROSS for cad in CADENCE]
    ungated = pd.concat([s.reindex(segs[0].index).fillna(0.0) for s in segs], axis=1).mean(axis=1)
    for nm, r in (("ALWAYS-ACT (774's control)", ungated),
                  ("RULES v2 U56 (live book)", base56.loc[OOS_START:]),
                  ("SPY", spy56.loc[OOS_START:])):
        m = metrics(r)
        ctrl.append(dict(est=nm, bar=np.nan, acted=np.nan, cells=np.nan, picks="-",
                         OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    wf = pd.DataFrame(wf_rows + ctrl)
    P(fmt(wf.set_index(["est", "bar"])[["acted", "cells", "OOS_CAGR", "OOS_Sharpe",
                                        "OOS_MaxDD"]], 4))
    bsh = metrics(base56.loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy56.loc[OOS_START:])["Sharpe"]
    beat_b = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > bsh).sum())
    beat_s = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > ssh).sum())
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bsh:.4f}): {beat_b}/{len(wf_rows)}; "
      f"beating SPY ({ssh:.4f}): {beat_s}/{len(wf_rows)}")
    dkf = pd.DataFrame(dk)
    P("")
    P("  KEEP paths for the decision books (full-sample twin of each rule, 4a vs RULES v2 U56):")
    P(fmt(dkf.set_index(["est", "bar"]), 4))
    P(f"  decision books: 4a {int(dkf.keep4a.sum())}/{len(dkf)}, "
      f"4b {int(dkf.keep4b.sum())}/{len(dkf)}, BOTH {int((dkf.keep4a & dkf.keep4b).sum())}/{len(dkf)}")
    P("")

    # ------------------------------------------------------------------ write
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    floors.to_csv(OUT / f"{STAMP}.floors.csv", index=False)
    rho.to_csv(OUT / f"{STAMP}.rho.csv", index=False)
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    rescore.to_csv(OUT / f"{STAMP}.rescore.csv", index=False)
    moves.to_csv(OUT / f"{STAMP}.moves.csv", index=False)
    pd.concat([wf.assign(leg="WF-B_OOS"), dkf.assign(leg="WF-B_KEEP")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P(f"wrote grid {len(grid)}, floors {len(floors)}, rho {len(rho)}, census {len(cen)}, "
      f"rescore {len(rescore)}, moves {len(moves)}, keeppaths {len(kp)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
