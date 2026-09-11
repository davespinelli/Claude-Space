#!/usr/bin/env python3
"""Idea 788 - "publish-a-PERIOD-STABILITY-column-beside-every-FLOOR-COMPARISON-verdict-in-the-record"
(cloud lane, 2026-09-11).

The question
------------
Idea 779 closed with a PROTOCOL proposal it did not itself execute: "If a future run wants
to retire anything on a floor comparison, the floor's own PERIOD STABILITY has to be
published beside it."  779's evidence for that proposal was one number - the mover set's
Jaccard of 0.0222 between IS-only and OOS-only floors (18 FULL / 35 IS / 11 OOS movers, 1
shared) - measured on ONE bar form (PAIR_INDEP vs POOLED) at ONE dial setting.

This run turns the proposal into the column.  Every committed 'inside/outside its floor'
verdict in the record's 607-claim census is re-scored on FULL, IS-only and OOS-only floors,
and the per-claim AGREEMENT is published as a required field.  The question the queue
actually asks is not "does the count reproduce" (778 already showed it does) but "for what
share of individual claims does the verdict survive being measured on half the sample".

Note the two objects are different.  779 measured the stability of a RESTATEMENT (which
claims MOVE when the bar form changes).  This run measures the stability of the VERDICT
itself (does a claim read INSIDE or OUTSIDE when the floor is estimated on a different
period), which is the object every published floor comparison actually quotes.

Definitions, verbatim from the record's own machinery (ideas 567/774/778/779)
-----------------------------------------------------------------------------
    floor_p(stat, D, period) = mean over (gross x cadence) of the s.d. across D independent
                               k=36 crc32-seeded draws from parent p, of `stat` measured on
                               `period`.  (idea 567's construction; rebuilt here, gated.)
    INSIDE  (not distinguishable from its floor):   margin <  bar * floor
    OUTSIDE (distinguishable):                      margin >= bar * floor
    margin = the MIN GAP between adjacent panel values inside the claim (778's object).

Three bar forms, all published, none selected:
    POOLED      idea 567's incumbent - one floor for the whole statistic family.
    RSS_INDEP   idea 774's correction - RSS over every parent the claim NAMES.
    PAIR_INDEP  idea 778's restatement - RSS over the two parents bracketing the margin.

Tuned parameters (PROTOCOL rule 4: at most two).  All 20 points reported.
    1. VERDICT SET in {ALL, 2PANEL, 3PANEL, NESTED_PAIR, NZ} - which committed verdicts the
       stability column is required on (779's claim sets, verbatim).
    2. SPLIT in {FULL_vs_IS, FULL_vs_OOS, IS_vs_OOS, ALL3} - which periods have to agree.
Reported, never selected: bar form (3), D in {3,6,12,24}, bar multiple in {1.0, 2.0},
statistic family (5), period (3), venue.

Pre-registered gates, written before any agreement rate was read
-----------------------------------------------------------------
G1 HARVEST   A fresh harvest of the committed markdown corpus must reproduce all 607 rows of
             idea 778's committed `.census.csv` (779's G1, same bar).
G2 FLOORS    Per-parent floors rebuilt from prices must restate 774/778's committed
             `.floors.csv` on every row and column to < 1e-12.
G3 IDENTITY  `fast_backtest` must equal `engine.backtest` to < 1e-12 on one book per parent.
G4 779 REPRO The FULL/IS/OOS mover counts of 779's WF-A leg (18 / 35 / 11, IS n OOS = 1,
             Jaccard 0.0222) must be re-derived here from prices.  This run's object is
             different from 779's, so reproducing 779's object is the only thing that shows
             the shared machinery is being replayed faithfully.
G5 DEGENERACY Neither verdict can be degenerate: at the headline point the INSIDE share over
             ALL claims must sit strictly inside 2%-98% in EVERY period, or the agreement
             rate is measuring a constant and means nothing.

Bars (pre-registered)
---------------------
B1 IS THE VERDICT PERIOD-STABLE?  PASS iff the ALL3 agreement rate over ALL claims is
   >= 90% at the headline point.  A FAIL means the record's floor comparisons are, per
   claim, a statement about the sample period as much as about the panels.
B2 DOES THE COLUMN DISCRIMINATE?  No bar - the spread of agreement across bar forms, D and
   statistic family is the answer, reported as a table.
B3 DOES PERIOD INSTABILITY COST ANYTHING IN CAPITAL?  Rule 8 WF-B below: a decision rule
   that acts on an IS-only floor comparison, priced OOS against the live book and SPY.

Rule 8 walk-forward
-------------------
WF-A  the agreement column itself is the walk-forward: every verdict is computed on IS-only
      floors and on OOS-only floors and the two are compared claim by claim.
WF-B  a DECISION RULE built only on the first half.  For each (statistic, D) cell, rank the
      three parents by their IS value of that statistic on the REAL MA-RS book, compute the
      IS min-gap between adjacent parents, and ACT (hold the IS-best parent's MA-RS book
      through the OOS half) iff that IS min-gap >= bar * IS floor; else STAND DOWN to the
      live book (RULES v2 on U56).  OOS read exactly once.  Controls: ALWAYS-ACT,
      NEVER-ACT, and the same rule run on FULL floors (a look-ahead oracle) so the cost of
      the period instability is priced directly.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and the committed
artefacts of ideas 774/778/779; modifies nothing but its own outputs:
    .grid.csv .floors.csv .stability.csv .agreement.csv .g4.csv .walkforward.csv
    .keeppaths.csv .console.txt
"""
from __future__ import annotations

import collections
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
CLAIM_SETS = ["ALL", "2PANEL", "3PANEL", "NESTED_PAIR", "NZ"]
SPLITS = ["FULL_vs_IS", "FULL_vs_OOS", "IS_vs_OOS", "ALL3"]
ESTS = ["POOLED", "RSS_INDEP", "PAIR_INDEP"]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
PERIODS = ("FULL", "IS", "OOS")
CONTROL_DOCS = ("RULES.md", "PROTOCOL.md", "CHANGELOG.md", "LEADERBOARD.md", "QUEUE.md")
HEAD_EST, HEAD_D, HEAD_BAR = "PAIR_INDEP", 6, 1.0     # declared before the run, not chosen
B1_BAR = 0.90

P778 = OUT / "2026-09-11_is-the-RSS-BAR-the-right-object-when-the-two-parents-OVERLAP_cloud"
P779 = OUT / ("2026-09-11_does-the-MIN-GAP-PAIR-restatement-change-any-published-VERDICT-"
              "not-just-the-count_C")
PUB779_WFA = {"FULL": 18, "IS": 35, "OOS": 11, "shared": 1}   # 779's committed WF-A counts
TOL = 1e-12

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G3).  Idea 779's, verbatim."""
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
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])      # PROTOCOL: always dropped
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


# ------------------------------------------------------------------------- census
# idea 567/774/778/779's harvester, verbatim.
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
            j = int(np.argmin(gaps))
            mpair = "|".join(sorted((pairs[j][0], pairs[j + 1][0])))
            rows.append(dict(file=p.name, family=fam, n_panels=len(vals),
                             margin=abs(margin), span=abs(order[-1] - order[0]),
                             parents="+".join(sorted(vals)), mpair=mpair,
                             claim=s.strip()[:240]))
    return pd.DataFrame(rows)


def corpus_files():
    return sorted({p for p in (list((ROOT / "research").glob("*.md"))
                               + list((ROOT / "research" / "backtests").glob("*.md")))
                   if p.is_file()})


# ------------------------------------------------------------------------- bars
def pkey(name, small_name):
    return small_name if name == "SMALL" else name


def bar_rss_indep(named, stat, floors_pp, small_name):
    f = floors_pp[stat]
    v = [f[pkey(p, small_name)] for p in named if pkey(p, small_name) in f]
    return float(np.sqrt(np.sum(np.square(v)))) if v else np.nan


def bar_pair_indep(mpair, stat, floors_pp, small_name):
    f = floors_pp[stat]
    i, j = [pkey(x, small_name) for x in mpair.split("|")]
    if i not in f or j not in f:
        return np.nan
    return float(np.sqrt(f[i] ** 2 + f[j] ** 2))


def bar_pooled(stat, floors_pp):
    return float(np.nanmean(list(floors_pp[stat].values())))


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 788 - publish a PERIOD STABILITY column beside every FLOOR COMPARISON verdict")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): VERDICT SET in " + str(CLAIM_SETS) + " x SPLIT in " + str(SPLITS)
      + "  -- all 20 points reported")
    P(f"# REPORTED not selected: est in {ESTS}, D in {DRAW_COUNTS}, bar in {BARS}, "
      f"5 statistic families.  Headline point declared up front: est={HEAD_EST}, "
      f"D={HEAD_D}, bar={HEAD_BAR}.")
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

    # ------------------------------------------------------------------ G1 harvest
    paths = corpus_files()
    fresh = harvest(paths)
    cen = pd.read_csv(f"{P778}.census.csv")

    def key(d):
        return list(zip(d.file, d.family, d.n_panels, d.margin.round(12), d.span.round(12),
                        d.claim.str[:200]))

    ca, cb = collections.Counter(key(cen)), collections.Counter(key(fresh))
    g1 = sum(min(v, cb[k]) for k, v in ca.items())
    P(f"G1 harvest   : idea 778's committed census rows reproduced by a fresh harvest of "
      f"{len(paths)} committed markdown files: {g1} of {len(cen)} (this run harvests "
      f"{len(fresh)}; the surplus is files committed after 778 ran) -> "
      f"{'PASS' if g1 == len(cen) == 607 else 'FAIL'}")

    # ------------------------------------------------------------------ G3 identity
    g3 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g3 = max(g3, float(np.abs(a.values - b.values).max()))
    P(f"G3 identity  : fast_backtest vs engine.backtest max |dret| = {g3:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g3 <= TOL else 'FAIL'}")

    # ------------------------------------------------------------------ price leg
    P("")
    P("=" * 100)
    P("PRICE LEG - REAL panels + idea 774's INDEPENDENT draws (rebuilds the floors)")
    P("=" * 100)
    rows = []
    spy_cache = {}

    def run_unit(pn, px, pick, kind, sd):
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
                             k=len(pick))
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
    grid = pd.DataFrame(rows)

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
        pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
        ma = sub[sub.arm == "MA-RS"].set_index("seed")
        if stat == "PREM_SHARPE":
            return ma[{"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe",
                       "OOS": "OOS_dSharpe"}[period]]
        if stat == "PREM_CAGR":
            return ma[{"FULL": "dCAGR_vs_EWall", "IS": "IS_dCAGR",
                       "OOS": "OOS_dCAGR"}[period]]
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
                            sub = dr[(dr.parent == pn) & (dr.gross == g)
                                     & (dr.cadence == cad) & (dr.seed < D)]
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
    fl_old = pd.read_csv(f"{P778}.floors.csv")
    mg = floors.merge(fl_old, on=["statistic", "D", "period"], suffixes=("_r", "_c"))
    assert len(mg) == len(fl_old) == len(floors), (len(mg), len(fl_old), len(floors))
    fcols = ["floor_pooled", "floor_max", "floor_min"] + [f"floor_{p}" for p in pnames]
    g2 = max(float(np.abs(mg[c + "_r"] - mg[c + "_c"]).max()) for c in fcols)
    P(f"G2 floors    : per-parent floors rebuilt from prices vs 774/778's committed "
      f".floors.csv, all {len(mg)} rows x {len(fcols)} columns, max |d| = {g2:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")

    # ------------------------------------------- the INSIDE/OUTSIDE verdict, every period
    def maps(D, period):
        fsub = floors[(floors.D == D) & (floors.period == period)].set_index("statistic")
        return {s: {p: float(fsub.loc[s, f"floor_{p}"]) for p in pnames} for s in STATS}

    cen = cen[cen.mpair.notna()].reset_index(drop=True)
    m0 = cen.margin.to_numpy(float)
    fams = cen.family.tolist()
    parents_named = [r.split("+") for r in cen.parents.tolist()]
    mpairs = cen.mpair.tolist()

    inside = {}                      # (period, D, est, bar) -> bool array over claims
    barval = {}                      # (period, D, est)      -> float array (the floor used)
    for period in PERIODS:
        for D in DRAW_COUNTS:
            fpp = maps(D, period)
            bp = np.array([bar_pooled(f, fpp) for f in fams])
            br = np.array([bar_rss_indep(pl, f, fpp, small_name)
                           for pl, f in zip(parents_named, fams)])
            bq = np.array([bar_pair_indep(mp, f, fpp, small_name)
                           for mp, f in zip(mpairs, fams)])
            barval[(period, D, "POOLED")] = bp
            barval[(period, D, "RSS_INDEP")] = br
            barval[(period, D, "PAIR_INDEP")] = bq
            for b in BARS:
                inside[(period, D, "POOLED", b)] = m0 < b * bp
                inside[(period, D, "RSS_INDEP", b)] = m0 < b * br
                inside[(period, D, "PAIR_INDEP", b)] = m0 < b * bq

    # ------------------------------------------------------------------ G4 779 repro
    g4_rows = []
    sets = {}
    for period in PERIODS:
        was = inside[(period, 6, "POOLED", 1.0)]
        now = inside[(period, 6, "PAIR_INDEP", 1.0)]
        sets[period] = set(np.flatnonzero(was != now).tolist())
        g4_rows.append(dict(period=period, published_779=PUB779_WFA[period],
                            rebuilt_here=len(sets[period])))
    shared = len(sets["IS"] & sets["OOS"])
    union = len(sets["IS"] | sets["OOS"])
    jac = shared / union if union else np.nan
    g4_rows.append(dict(period="IS n OOS", published_779=PUB779_WFA["shared"],
                        rebuilt_here=shared))
    g4df = pd.DataFrame(g4_rows)
    g4 = bool((g4df.published_779 == g4df.rebuilt_here).all())
    for _, r in g4df.iterrows():
        P(f"                {r.period:>8}: 779 published {r.published_779:3d}, "
          f"rebuilt from prices here {r.rebuilt_here:3d}")
    P(f"                Jaccard(IS, OOS) rebuilt = {jac:.4f} "
      f"(779 published 0.0222)")
    P(f"G4 779 repro : idea 779's WF-A mover counts re-derived from prices -> "
      f"{'PASS' if g4 else 'FAIL'} (exact integers)")

    # ------------------------------------------------------------------ G5 degeneracy
    deg = {p: float(inside[(p, HEAD_D, HEAD_EST, HEAD_BAR)].mean()) for p in PERIODS}
    g5 = all(0.02 < v < 0.98 for v in deg.values())
    P(f"G5 degeneracy: INSIDE share at the headline point ({HEAD_EST}, D={HEAD_D}, "
      f"bar={HEAD_BAR}) over all {len(cen)} claims - "
      + ", ".join(f"{k} {v:.1%}" for k, v in deg.items())
      + f" -> {'PASS' if g5 else 'FAIL'} (each must sit strictly inside 2%-98%)")
    P("")

    # ------------------------------------------------------------------ THE COLUMN
    P("=" * 100)
    P("THE PERIOD-STABILITY COLUMN - every committed floor-comparison verdict, re-scored")
    P("=" * 100)

    def subset_mask(nm):
        if nm == "ALL":
            return np.ones(len(cen), bool)
        if nm == "2PANEL":
            return (cen.n_panels == 2).to_numpy()
        if nm == "3PANEL":
            return (cen.n_panels == 3).to_numpy()
        if nm == "NESTED_PAIR":
            return (cen.mpair == "B136|U56").to_numpy()
        if nm == "NZ":
            return (cen.margin > 0).to_numpy()
        raise KeyError(nm)

    def agree_mask(split, D, est, b):
        f = inside[("FULL", D, est, b)]
        i = inside[("IS", D, est, b)]
        o = inside[("OOS", D, est, b)]
        return {"FULL_vs_IS": f == i, "FULL_vs_OOS": f == o,
                "IS_vs_OOS": i == o, "ALL3": (f == i) & (f == o)}[split]

    ag_rows = []
    for cs in CLAIM_SETS:
        msk = subset_mask(cs)
        for split in SPLITS:
            for est in ESTS:
                for D in DRAW_COUNTS:
                    for b in BARS:
                        a = agree_mask(split, D, est, b)
                        ok = a & msk
                        ag_rows.append(dict(
                            claim_set=cs, split=split, est=est, D=D, bar=b,
                            n=int(msk.sum()), agree=int(ok.sum()),
                            disagree=int((msk & ~a).sum()),
                            agree_rate=float(ok.sum() / max(msk.sum(), 1))))
    agr = pd.DataFrame(ag_rows)
    agr.to_csv(f"{OUT}/{STAMP}.agreement.csv", index=False)

    head = agr[(agr.est == HEAD_EST) & (agr.D == HEAD_D) & (agr.bar == HEAD_BAR)]
    P(f"HEADLINE GRID - the 20 tuned points ({HEAD_EST}, D={HEAD_D}, bar={HEAD_BAR}), "
      "all shown")
    piv = head.pivot_table(index="claim_set", columns="split", values="agree_rate")
    P(fmt(piv.loc[CLAIM_SETS, SPLITS], 4))
    P("")
    P("  counts (n / agree / disagree) at the same point")
    P(fmt(head.set_index(["claim_set", "split"])[["n", "agree", "disagree"]], 0))
    P("")

    all3_all = float(head[(head.claim_set == "ALL") & (head.split == "ALL3")]
                     .agree_rate.iloc[0])
    P(f"B1  IS THE VERDICT PERIOD-STABLE?  ALL3 agreement over ALL claims at the headline "
      f"point = {all3_all:.2%} (bar {B1_BAR:.0%}) -> "
      + ("PASS - the verdict survives being measured on half the sample"
         if all3_all >= B1_BAR else
         "FAIL - the per-claim verdict is period-dependent"))
    P("")

    P("B2  DOES THE COLUMN DISCRIMINATE?  ALL3 agreement over ALL claims, every reported "
      "dial (bar form x D x bar multiple)")
    d2 = agr[(agr.claim_set == "ALL") & (agr.split == "ALL3")]
    P(fmt(d2.pivot_table(index=["est", "bar"], columns="D", values="agree_rate"), 4))
    P("")
    P("  the same by SPLIT (ALL claims, headline est/D/bar aside - averaged over the three "
      "bar forms, both bar multiples and all four D)")
    P(fmt(agr[agr.claim_set == "ALL"].pivot_table(index="split", columns="est",
                                                  values="agree_rate").loc[SPLITS], 4))
    P("")

    # per-claim column + per-family breakdown
    st_rows = []
    for est in ESTS:
        for D in DRAW_COUNTS:
            for b in BARS:
                f = inside[("FULL", D, est, b)]
                i = inside[("IS", D, est, b)]
                o = inside[("OOS", D, est, b)]
                for idx in range(len(cen)):
                    st_rows.append(dict(
                        idx=idx, est=est, D=D, bar=b,
                        file=cen.file.iloc[idx], family=cen.family.iloc[idx],
                        n_panels=int(cen.n_panels.iloc[idx]), mpair=cen.mpair.iloc[idx],
                        margin=float(cen.margin.iloc[idx]),
                        floor_FULL=float(barval[("FULL", D, est)][idx]),
                        floor_IS=float(barval[("IS", D, est)][idx]),
                        floor_OOS=float(barval[("OOS", D, est)][idx]),
                        verdict_FULL="INSIDE" if f[idx] else "OUTSIDE",
                        verdict_IS="INSIDE" if i[idx] else "OUTSIDE",
                        verdict_OOS="INSIDE" if o[idx] else "OUTSIDE",
                        STABLE=bool(f[idx] == i[idx] == o[idx]),
                        control_doc=cen.file.iloc[idx] in CONTROL_DOCS,
                        claim=cen.claim.iloc[idx]))
    stab = pd.DataFrame(st_rows)
    stab.to_csv(f"{OUT}/{STAMP}.stability.csv", index=False)
    P(f"  per-claim column written: {len(stab)} rows "
      f"({len(cen)} claims x {len(ESTS)} bar forms x {len(DRAW_COUNTS)} D x {len(BARS)} bar)")
    P("")

    hs = stab[(stab.est == HEAD_EST) & (stab.D == HEAD_D) & (stab.bar == HEAD_BAR)]
    P("  STABILITY by STATISTIC FAMILY (headline point)")
    by_fam = hs.groupby("family").agg(n=("STABLE", "size"), stable=("STABLE", "sum"))
    by_fam["stable_rate"] = by_fam.stable / by_fam.n
    P(fmt(by_fam, 4))
    P("")
    nst = hs[~hs.STABLE]
    P(f"  UNSTABLE claims at the headline point: {len(nst)} of {len(hs)} "
      f"({len(nst)/len(hs):.1%}); {int(nst.control_doc.sum())} of them live in a CONTROL "
      f"document ({', '.join(CONTROL_DOCS)}) against a base rate of "
      f"{hs.control_doc.mean():.1%}")
    P("  the unstable claims that sit in a control document (verdict per period):")
    show = nst[nst.control_doc].head(12)
    for _, r in show.iterrows():
        P(f"    [{r.file}] {r.family} margin {r.margin:.4f}  "
          f"FULL {r.verdict_FULL} / IS {r.verdict_IS} / OOS {r.verdict_OOS}")
        P(f"      {r.claim[:170]}")
    if not len(show):
        P("    (none)")
    P("")

    # ------------------------------------------------------------------ WF-B
    P("=" * 100)
    P("RULE 8 WF-B - the floor comparison priced as a DECISION RULE (OOS read once)")
    P("=" * 100)
    real = grid[(grid.kind == "REAL") & (grid.arm == "MA-RS") & (grid.gross == 0.75)
                & (grid.cadence == "W")].set_index("parent")
    real_books = {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        real_books[pn] = fast_backtest(
            px, make_books(px, set(names), 0.75)["MA-RS"], freq="W")["returns"].loc[warm:]

    STAT_COL = {"SHARPE": ("IS_Sharpe", "Sharpe"), "CAGR": ("IS_CAGR", "CAGR"),
                "PREM_SHARPE": ("IS_dSharpe", "dSharpe_vs_EWall")}
    wf_rows = []
    for stat, (iscol, _) in STAT_COL.items():
        for D in DRAW_COUNTS:
            vals = {pn: float(real.loc[pn, iscol]) for pn in pnames}
            order = sorted(vals.items(), key=lambda kv: -kv[1])
            best = order[0][0]
            gaps = [order[i][1] - order[i + 1][1] for i in range(len(order) - 1)]
            mingap = min(gaps)
            for period_used in ("IS", "FULL"):      # FULL = look-ahead oracle control
                fsub = floors[(floors.D == D) & (floors.period == period_used)
                              ].set_index("statistic")
                fl = [float(fsub.loc[stat, f"floor_{p}"]) for p in pnames]
                floor = float(np.sqrt(np.sum(np.square(fl))))     # RSS over the named parents
                for b in BARS:
                    act = bool(mingap >= b * floor)
                    r = real_books[best] if act else bases["U56"]
                    ro = r.loc[OOS_START:]
                    wf_rows.append(dict(stat=stat, D=D, floor_period=period_used, bar=b,
                                        IS_mingap=mingap, floor=floor, acted=act,
                                        picked=best if act else "STAND-DOWN (RULES v2 U56)",
                                        OOS_CAGR=metrics(ro)["CAGR"],
                                        OOS_Sharpe=metrics(ro)["Sharpe"],
                                        OOS_MaxDD=metrics(ro)["MaxDD"],
                                        FULL_CAGR=metrics(r)["CAGR"],
                                        FULL_Sharpe=metrics(r)["Sharpe"],
                                        FULL_MaxDD=metrics(r)["MaxDD"],
                                        H1=halves(r)[0], H2=halves(r)[1]))
    # controls
    for nm, r in [("ALWAYS-ACT (IS-best, no floor test)", None), ("NEVER-ACT (live book)",
                                                                 bases["U56"])]:
        if r is None:
            picks = {stat: sorted({pn: float(real.loc[pn, STAT_COL[stat][0]])
                                   for pn in pnames}.items(), key=lambda kv: -kv[1])[0][0]
                     for stat in STAT_COL}
            for stat, bestp in picks.items():
                rr = real_books[bestp]
                ro = rr.loc[OOS_START:]
                wf_rows.append(dict(stat=stat, D=-1, floor_period="ALWAYS", bar=np.nan,
                                    IS_mingap=np.nan, floor=np.nan, acted=True, picked=bestp,
                                    OOS_CAGR=metrics(ro)["CAGR"],
                                    OOS_Sharpe=metrics(ro)["Sharpe"],
                                    OOS_MaxDD=metrics(ro)["MaxDD"],
                                    FULL_CAGR=metrics(rr)["CAGR"],
                                    FULL_Sharpe=metrics(rr)["Sharpe"],
                                    FULL_MaxDD=metrics(rr)["MaxDD"],
                                    H1=halves(rr)[0], H2=halves(rr)[1]))
        else:
            ro = r.loc[OOS_START:]
            wf_rows.append(dict(stat="-", D=-1, floor_period="NEVER", bar=np.nan,
                                IS_mingap=np.nan, floor=np.nan, acted=False,
                                picked="RULES v2 U56",
                                OOS_CAGR=metrics(ro)["CAGR"], OOS_Sharpe=metrics(ro)["Sharpe"],
                                OOS_MaxDD=metrics(ro)["MaxDD"], FULL_CAGR=metrics(r)["CAGR"],
                                FULL_Sharpe=metrics(r)["Sharpe"], FULL_MaxDD=metrics(r)["MaxDD"],
                                H1=halves(r)[0], H2=halves(r)[1]))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(f"{OUT}/{STAMP}.walkforward.csv", index=False)

    spy_u = spys["U56"]
    spy_o = spy_u.loc[OOS_START:]
    P(f"  LIVE BOOK  RULES v2 U56 : OOS CAGR {metrics(bases['U56'].loc[OOS_START:])['CAGR']:.2%} "
      f"Sharpe {metrics(bases['U56'].loc[OOS_START:])['Sharpe']:.4f} "
      f"MaxDD {metrics(bases['U56'].loc[OOS_START:])['MaxDD']:.2%}")
    P(f"  SPY                     : OOS CAGR {metrics(spy_o)['CAGR']:.2%} "
      f"Sharpe {metrics(spy_o)['Sharpe']:.4f} MaxDD {metrics(spy_o)['MaxDD']:.2%}")
    P("")
    P("  DECISION BOOKS (IS-only floor vs the FULL-floor look-ahead oracle)")
    P(fmt(wf[wf.D > 0].set_index(["stat", "D", "floor_period", "bar"])[
        ["IS_mingap", "floor", "acted", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]], 4))
    P("")
    P("  CONTROLS")
    P(fmt(wf[wf.D < 0].set_index(["stat", "floor_period"])[
        ["picked", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]], 4))
    P("")
    dec = wf[wf.D > 0]
    is_only = dec[dec.floor_period == "IS"]
    full_or = dec[dec.floor_period == "FULL"]
    same = int((is_only.acted.to_numpy() == full_or.acted.to_numpy()).sum())
    P(f"  DECISION AGREEMENT IS-floor vs FULL-floor: {same} of {len(is_only)} cells "
      f"({same/len(is_only):.1%}) - the period instability of the FLOOR changes the "
      f"decision in {len(is_only)-same} of {len(is_only)} cells")
    bsh = metrics(bases["U56"].loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy_o)["Sharpe"]
    P(f"  Beating RULES v2 OOS Sharpe ({bsh:.4f}): "
      f"{int((dec.OOS_Sharpe > bsh).sum())} of {len(dec)}")
    P(f"  Beating SPY      OOS Sharpe ({ssh:.4f}): "
      f"{int((dec.OOS_Sharpe > ssh).sum())} of {len(dec)}")
    P("")
    P(f"B3  DOES PERIOD INSTABILITY COST CAPITAL?  "
      + ("NO - no decision book beats the live book OOS on Sharpe, so the floor "
         "comparison is not a tradable object either way"
         if int((dec.OOS_Sharpe > bsh).sum()) == 0 else
         f"YES - {int((dec.OOS_Sharpe > bsh).sum())} decision books beat the live book OOS"))
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 100)
    P("KEEP PATHS (PROTOCOL rule 4a and 4b) - full price grid and the decision books")
    P("=" * 100)
    kp = []
    for _, r in grid.iterrows():
        pn = r.parent
        px = parents[pn][0]
        warm = px.index[260]
        # recompute returns is expensive; use the stored metrics against stored bases
        kp.append(dict(parent=pn, kind=r.kind, seed=r.seed, arm=r.arm, gross=r.gross,
                       cadence=r.cadence, Sharpe=r.Sharpe, CAGR=r.CAGR, MaxDD=r.MaxDD,
                       H1=r.H1, H2=r.H2, OOS_Sharpe=r.OOS_Sharpe))
    kdf = pd.DataFrame(kp)
    # 4a/4b judged with the stored halves against per-parent baseline/SPY halves
    binfo = {pn: dict(H1=halves(bases[pn])[0], H2=halves(bases[pn])[1],
                      MaxDD=metrics(bases[pn])["MaxDD"]) for pn in pnames}
    sinfo = {pn: dict(H1=halves(spys[pn])[0], H2=halves(spys[pn])[1],
                      MaxDD=metrics(spys[pn])["MaxDD"], CAGR=metrics(spys[pn])["CAGR"],
                      OOS=metrics(spys[pn].loc[OOS_START:])["Sharpe"]) for pn in pnames}
    a4, b4 = [], []
    for _, r in kdf.iterrows():
        bi, si = binfo[r.parent], sinfo[r.parent]
        a4.append(bool(r.H1 > bi["H1"] and r.H2 > bi["H2"] and r.MaxDD >= bi["MaxDD"]))
        f = []
        if not r.H1 > si["H1"]:
            f.append("H1")
        if not r.H2 > si["H2"]:
            f.append("H2")
        if not r.OOS_Sharpe > si["OOS"]:
            f.append("OOS")
        if not r.MaxDD >= 0.60 * si["MaxDD"]:
            f.append("DD")
        if not r.CAGR >= 0.70 * si["CAGR"]:
            f.append("CAGR")
        b4.append(",".join(f) if f else "-")
    kdf["keep4a"], kdf["fail4b"] = a4, b4
    kdf["keep4b"] = kdf.fail4b == "-"
    kdf.to_csv(f"{OUT}/{STAMP}.keeppaths.csv", index=False)
    P(f"  PRICE GRID  ({len(kdf)} books): 4a {int(kdf.keep4a.sum())}/{len(kdf)}, "
      f"4b {int(kdf.keep4b.sum())}/{len(kdf)}, "
      f"BOTH {int((kdf.keep4a & kdf.keep4b).sum())}/{len(kdf)}")
    rl = kdf[kdf.kind == "REAL"]
    P(f"  REAL books  ({len(rl)}): 4a {int(rl.keep4a.sum())}, 4b {int(rl.keep4b.sum())}"
      + ("  ->  " + "; ".join(f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence}"
                              for _, r in rl[rl.keep4b].iterrows())
         if rl.keep4b.any() else ""))
    P("  4b binding failure legs over the whole grid: "
      + str(collections.Counter(
          leg for s in kdf.fail4b for leg in (s.split(",") if s != "-" else []))))
    d4a = sum(1 for _, r in wf.iterrows()
              if r.H1 > binfo["U56"]["H1"] and r.H2 > binfo["U56"]["H2"]
              and r.FULL_MaxDD >= binfo["U56"]["MaxDD"])
    su = sinfo["U56"]
    d4b = sum(1 for _, r in wf.iterrows()
              if r.H1 > su["H1"] and r.H2 > su["H2"] and r.OOS_Sharpe > su["OOS"]
              and r.FULL_MaxDD >= 0.60 * su["MaxDD"] and r.FULL_CAGR >= 0.70 * su["CAGR"])
    P(f"  DECISION BOOKS ({len(wf)}): 4a {d4a}/{len(wf)}, 4b {d4b}/{len(wf)}")
    P("")

    # ------------------------------------------------------------------ survivorship
    P("SURVIVORSHIP: `universe_broad.json` and the small panel are CURRENT CONSTITUENTS "
      "only; every stock-side level carries a survivorship premium and the LEVEL floors "
      "(SHARPE, CAGR, MAXDD) are lower bounds on true dispersion.  Names with "
      "max_1d_move >= 1.0 are dropped from the small panel per PROTOCOL.  The three "
      "parents start on different dates (U56/B136 2008, SMALL 2010), inherited from 567's "
      "floor construction.")
    P("")
    grid.to_csv(f"{OUT}/{STAMP}.grid.csv", index=False)
    floors.to_csv(f"{OUT}/{STAMP}.floors.csv", index=False)
    g4df.to_csv(f"{OUT}/{STAMP}.g4.csv", index=False)
    P(f"# gates: G1 {'PASS' if g1 == len(cen) == 607 else 'FAIL'}, "
      f"G2 {'PASS' if g2 <= TOL else 'FAIL'}, G3 {'PASS' if g3 <= TOL else 'FAIL'}, "
      f"G4 {'PASS' if g4 else 'FAIL'}, G5 {'PASS' if g5 else 'FAIL'}")
    P(f"# done in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
