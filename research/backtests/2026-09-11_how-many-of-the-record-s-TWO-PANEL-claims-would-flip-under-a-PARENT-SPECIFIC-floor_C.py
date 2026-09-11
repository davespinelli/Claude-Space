#!/usr/bin/env python3
"""Idea 774 (lane C, 2026-09-11) - how-many-of-the-record-s-TWO-PANEL-claims-would-flip-under-a-PARENT-SPECIFIC-floor.

QUESTION
--------
Idea 567 (lane B, same day) scored 607 committed panel-ordering claims against a POOLED
family floor - the mean, over the three real parents, of the within-parent sd of the
statistic across k-matched draws - and found two-panel claims clear that bar far more often
(16.4% of nonzero margins inside) than three-panel ones (37.1%).  But the same run measured
the floor to be PARENT-SPECIFIC at max/min 1.98x (U56 0.0502, B136 0.0995, SMALL439 0.0941
for PREM_SHARPE at D=6), so a pooled bar is too wide for U56-anchored claims and too narrow
for the other two.  This run re-scores the identical census against each claim's OWN
named-parent floor and reports how many verdicts move in each direction.

THE PART THE QUEUE DID NOT SPECIFY, AND WHY IT DECIDES THE ANSWER
-----------------------------------------------------------------
"Its own named-parent floor" is not a single object once a claim names TWO parents, which is
what 344 of the 607 claims do.  A claim of the form "U56 0.31 > B136 0.17" is a statement
about a DIFFERENCE between two parents' draws, so the quantity whose dispersion sets the bar
is the difference, not either parent's own level.  Five assignments are therefore priced side
by side, and the choice between them IS this run's first tuned dial:

    POOLED  mean floor over ALL three parents          (idea 567's incumbent bar)
    MIN     min floor over the parents the claim names (the most forgiving reading)
    MEAN    mean floor over the parents the claim names
    MAX     max floor over the parents the claim names (conservative single-parent bar)
    RSS     sqrt(sum of squares) over the named parents - the sd of an independent
            difference, i.e. the statistically correct bar for a two-parent gap

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. FLOOR ASSIGNMENT in {POOLED, MIN, MEAN, MAX, RSS}
    2. BAR b in {1.0, 2.0} sd
All 5 x 2 = 10 grid points are reported, for every statistic family and every draw count.
REPORTED (never selected) axes: statistic family (5), draw count D in {3, 6, 12, 24}, period
    (FULL / IS / OOS), gross g in {0.50, 0.75, 1.00}, cadence in {W, M}.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
H_DIR   : the queue's implied direction - a parent-specific floor EXONERATES claims (fewer
          inside) - because 558 of the census's claims name U56 and U56's floor is the
          narrowest.  Falsified if the net movement at the correct (RSS) assignment is
          toward MORE claims inside.
H_TWO   : the two-panel / three-panel asymmetry idea 567 published (16.4% vs 37.1% inside on
          nonzero margins) is an ARTEFACT of the pooled bar and shrinks by more than half
          under a parent-specific one.  Falsified if the asymmetry survives.
H_SPREAD: the verdict is assignment-sensitive - the share inside at D=6 bar 1.0 moves by
          more than 10 pp between the MIN and RSS assignments.  If it does, no single
          "parent-specific floor" answer exists and the queue's question is under-specified.

GATES (pre-registered, run and printed before any new census number is read)
    G1 harvest reproduction: re-harvesting the committed record reproduces every one of idea
       567's 607 committed census rows exactly (file, family, n_panels, margin, span).  bar 607
    G2 floor reproduction  : the per-parent floors rebuilt from prices in this script match
       idea 567's committed .floors.csv on all 60 (statistic, D, period) rows.      bar 1e-12
    G3 identity            : fast_backtest vs engine.backtest on one book per parent. bar 1e-12
    G4 headline reproduction: idea 567's published census headlines re-derived from its own
       committed .census.csv - 42.7% of 607 inside, 25.2% of 465 nonzero, three-panel 52.7%,
       two-panel nonzero 16.4%, three-panel PREM_SHARPE 35/55.                       bar 1e-3

RULE 8 WALK-FORWARD (required, run whatever the census says)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: rebuild every parent's floor on IS returns only and on OOS returns
       only, re-score the census under all 10 grid points in each period, and report whether
       the direction of verdict movement is the same object out of sample.
    WF-B on a BOOK: the re-score is a DECISION RULE, so it is priced as one.  In each
       (gross, cadence) cell, rank the three parents by the IS MA-gate premium; ACT on that
       ordering (trade MA-RS on the IS-best parent) only if the IS span clears bar b times
       the assignment's floor, else STAND DOWN to the live book (RULES v2 on U56).  OOS is
       read ONCE for all 10 (assignment, bar) decision books and compared against RULES v2
       on U56 and against SPY.  Idea 567's ungated rule (always act) is the control.
    KEEP paths 4a and 4b are evaluated for every book on the 900-book price grid AND for
       every decision book.  Stated up front: a DRAW panel is a seeded random 36-name subset,
       not a rule anyone can trade, so a 4b pass on a draw is a diagnostic, not a candidate.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents, so every
    stock-side level carries a survivorship premium; the LEVEL floors (SHARPE, CAGR, MAXDD)
    are therefore lower bounds on true dispersion.  An arm-minus-arm premium measured on the
    same panel largely cancels it.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py and two committed
artefacts of idea 567; modifies nothing but its own outputs:
    .grid.csv .floors.csv .census.csv .rescore.csv .moves.csv .walkforward.csv
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
ASSIGNS = ["POOLED", "MIN", "MEAN", "MAX", "RSS"]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]

PARENT567 = OUT / "2026-09-11_how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor_B"
# idea 567's published census headlines (its result.md / LEADERBOARD row)
PUB = dict(n=607, inside_all=0.427, nonzero=465, inside_nonzero=0.252,
           three_all=0.527, three_nonzero=0.371, two_nonzero=0.164,
           three_prem_sharpe=(35, 55))
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
    """crc32-seeded k-matched draws, `DRAW|{parent}|{seed}` (idea 312/567 scheme, verbatim)."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


# ------------------------------------------------------------------------- census
# idea 567's harvester, verbatim, plus ONE added column: the panels the claim names.
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
            order = sorted(vals.values())
            gaps = [b - a for a, b in zip(order, order[1:])]
            margin = min(gaps) if gaps else np.nan
            if not np.isfinite(margin):
                continue
            rows.append(dict(file=p.name, family=fam, n_panels=len(vals),
                             margin=abs(margin), span=abs(order[-1] - order[0]),
                             parents="+".join(sorted(vals)), claim=s.strip()[:240]))
    return pd.DataFrame(rows)


def assign_floor(named, per_parent, how, small_name):
    """The bar a claim naming `named` parents is scored against, under assignment `how`."""
    if how == "POOLED":
        v = list(per_parent.values())
        return float(np.nanmean(v))
    keys = [small_name if p == "SMALL" else p for p in named]
    v = [per_parent[k] for k in keys if k in per_parent and np.isfinite(per_parent[k])]
    if not v:
        return np.nan
    if how == "MIN":
        return float(np.min(v))
    if how == "MEAN":
        return float(np.mean(v))
    if how == "MAX":
        return float(np.max(v))
    if how == "RSS":
        return float(np.sqrt(np.sum(np.square(v))))
    raise ValueError(how)


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 774 - how many of the record's TWO-PANEL claims flip under a PARENT-SPECIFIC floor?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): FLOOR ASSIGNMENT in " + str(ASSIGNS) + " x BAR in " + str(BARS)
      + "  -- all 10 points reported")
    P("")

    parents = real_panels()
    pnames = list(parents)
    small_name = [p for p in pnames if p.startswith("SMALL")][0]
    P("PARENTS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in parents.items()))
    P("")

    # ------------------------------------------------------------------ G1 harvest
    P("=" * 100)
    P("GATES (pre-registered; printed before any new census number is read)")
    P("=" * 100)
    paths = (sorted(OUT.glob("*.result.md")) + sorted(OUT.glob("*.memo.md"))
             + sorted(OUT.glob("*.md")) + sorted((ROOT / "research").glob("*.md")))
    paths = sorted({p for p in paths if p.is_file()})
    fresh = harvest(paths)
    old = pd.read_csv(f"{PARENT567}.census.csv")

    def key(d):
        return list(zip(d.file, d.family, d.n_panels, d.margin.round(12), d.span.round(12),
                        d.claim.str[:200]))

    ca, cb = collections.Counter(key(old)), collections.Counter(key(fresh))
    g1 = sum(min(v, cb[k]) for k, v in ca.items())
    P(f"G1 harvest      : idea 567's committed census rows reproduced by a fresh harvest of "
      f"{len(paths)} committed markdown files: {g1} of {len(old)} "
      f"(this run harvests {len(fresh)}; the surplus is files committed after 567 ran) "
      f"-> {'PASS' if g1 == len(old) == PUB['n'] else 'FAIL'}")

    # census of record = idea 567's committed 607 rows, with the named parents attached
    look = {}
    for _, r in fresh.iterrows():
        look.setdefault((r.file, r.family, r.n_panels, round(r.margin, 12), round(r.span, 12)),
                        r.parents)
    cen = old.copy()
    cen["parents"] = [look.get((r.file, r.family, r.n_panels, round(r.margin, 12),
                                round(r.span, 12)), None) for _, r in cen.iterrows()]
    n_unrec = int(cen.parents.isna().sum())
    P(f"                  parent set attached to {len(cen)-n_unrec} of {len(cen)} committed "
      f"claims ({n_unrec} unrecoverable)")

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
    m0 = old.margin.to_numpy(float)
    nz = m0 > 0
    fl_old = pd.read_csv(f"{PARENT567}.floors.csv")

    def pooled_floor(stat, D=6, period="FULL"):
        s = fl_old[(fl_old.statistic == stat) & (fl_old.D == D) & (fl_old.period == period)]
        return float(s.floor_pooled.iloc[0])

    ins_old = np.array([m < pooled_floor(f) for m, f in zip(m0, old.family)])
    g4 = []
    g4.append(("inside_all", ins_old.mean(), PUB["inside_all"]))
    g4.append(("nonzero_n", float(nz.sum()), float(PUB["nonzero"])))
    g4.append(("inside_nonzero", ins_old[nz].mean(), PUB["inside_nonzero"]))
    th = old.n_panels == 3
    tw = old.n_panels == 2
    g4.append(("three_all", ins_old[th].mean(), PUB["three_all"]))
    g4.append(("three_nonzero", ins_old[th & nz].mean(), PUB["three_nonzero"]))
    g4.append(("two_nonzero", ins_old[tw & nz].mean(), PUB["two_nonzero"]))
    sel = th & (old.family == "PREM_SHARPE").to_numpy()
    g4.append(("three_PREM_SHARPE_num", float(ins_old[sel].sum()), float(PUB["three_prem_sharpe"][0])))
    g4.append(("three_PREM_SHARPE_den", float(sel.sum()), float(PUB["three_prem_sharpe"][1])))
    worst = max(abs(a - b) for _, a, b in g4)
    for nm, a, b in g4:
        P(f"                  {nm:<24s} recomputed {a:.4f} vs published {b:.4f} "
          f"|d| {abs(a-b):.4f}")
    P(f"G4 headlines    : idea 567's published census numbers re-derived from its OWN "
      f"committed .census.csv, max |d| = {worst:.3e} (bar {G4_TOL:.0e}) -> "
      f"{'PASS' if worst <= G4_TOL else 'FAIL'}")
    P("")

    # ------------------------------------------------------------------ price leg
    P("=" * 100)
    P("PRICE LEG - 36-name draws out of each real parent (the floors, rebuilt from source)")
    P("=" * 100)
    rows = []
    spy_cache = {}
    for pn, (px, names) in parents.items():
        spy_cache[pn] = px["SPY"].pct_change().fillna(0.0)
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
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
                        rows.append(d)
        P(f"  {pn}: {len(units)} panels x {len(GROSS)} gross x {len(CADENCE)} cadence x 2 arms "
          f"({time.time()-t0:.0f}s)")
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

    # ------------------------------------------------------------------ floors
    def stat_series(sub, stat, period="FULL"):
        pre = {"FULL": "", "IS": "IS_", "OOS": "OOS_"}[period]
        ma = sub[sub.arm == "MA-RS"]
        if stat == "PREM_SHARPE":
            col = {"FULL": "dSharpe_vs_EWall", "IS": "IS_dSharpe", "OOS": "OOS_dSharpe"}[period]
            return ma[col]
        if stat == "PREM_CAGR":
            if period != "FULL":
                ew = sub[sub.arm == "EWall"].set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
                m2 = ma.set_index(["seed", "gross", "cadence"])[pre + "CAGR"]
                return m2 - ew.reindex(m2.index)
            return ma["dCAGR_vs_EWall"]
        return ma[pre + {"SHARPE": "Sharpe", "CAGR": "CAGR", "MAXDD": "MaxDD"}[stat]]

    fl_rows = []
    dr = grid[grid.kind == "DRAW"]
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in ("FULL", "IS", "OOS"):
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
                row["parent_ratio"] = row["floor_max"] / row["floor_min"] if row["floor_min"] else np.nan
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)

    mg = floors.merge(fl_old, on=["statistic", "D", "period"], suffixes=("_r", "_c"))
    assert len(mg) == len(fl_old) == len(floors), (len(mg), len(fl_old), len(floors))
    cols = ["floor_pooled", "floor_max", "floor_min"] + [f"floor_{p}" for p in pnames]
    g2 = max(float(np.abs(mg[c + "_r"] - mg[c + "_c"]).max()) for c in cols)
    P("")
    P(f"G2 floors       : per-parent floors rebuilt from prices vs idea 567's committed "
      f".floors.csv, all {len(mg)} (statistic, D, period) rows, max |d| = {g2:.3e} "
      f"(bar {TOL:.0e}) -> {'PASS' if g2 <= TOL else 'FAIL'}")
    P("")
    P("PER-PARENT FLOORS (FULL period; the object the queue says the record used wrong)")
    P(fmt(floors[floors.period == "FULL"].set_index(["statistic", "D"])
          [["floor_pooled"] + [f"floor_{p}" for p in pnames] + ["parent_ratio"]], 4))
    P("")

    # ------------------------------------------------------------------ RE-SCORE
    P("=" * 100)
    P("RE-SCORE - every claim against its OWN named-parent floor (10 tuned points, all shown)")
    P("=" * 100)
    cen = cen[cen.parents.notna()].reset_index(drop=True)
    rs_rows = []
    for period in ("FULL", "IS", "OOS"):
        for D in DRAW_COUNTS:
            fsub = floors[(floors.D == D) & (floors.period == period)].set_index("statistic")
            for how in ASSIGNS:
                bar_map = {}
                for stat in STATS:
                    pp = {p: float(fsub.loc[stat, f"floor_{p}"]) for p in pnames}
                    bar_map[stat] = pp
                fl_claim = np.array([
                    assign_floor(r.parents.split("+"), bar_map[r.family], how, small_name)
                    for _, r in cen.iterrows()])
                for b in BARS:
                    inside = cen.margin.to_numpy(float) < b * fl_claim
                    rs_rows.append(dict(period=period, D=D, assign=how, bar=b,
                                        n=len(cen), inside=int(inside.sum()),
                                        share=float(inside.mean()),
                                        nz_n=int((cen.margin > 0).sum()),
                                        nz_share=float(inside[(cen.margin > 0).to_numpy()].mean()),
                                        two_share=float(inside[(cen.n_panels == 2).to_numpy()].mean()),
                                        three_share=float(inside[(cen.n_panels == 3).to_numpy()].mean()),
                                        two_nz=float(inside[((cen.n_panels == 2) & (cen.margin > 0)).to_numpy()].mean()),
                                        three_nz=float(inside[((cen.n_panels == 3) & (cen.margin > 0)).to_numpy()].mean()),
                                        mean_floor=float(np.nanmean(fl_claim))))
                    if period == "FULL" and D == 6:
                        cen[f"inside_{how}_{b}"] = inside
    rescore = pd.DataFrame(rs_rows)
    head = rescore[(rescore.period == "FULL") & (rescore.D == 6)]
    P("HEADLINE GRID (D=6, FULL): share of the census inside its own floor")
    P(fmt(head.set_index(["assign", "bar"])[["n", "inside", "share", "nz_share",
                                             "two_share", "three_share", "two_nz",
                                             "three_nz", "mean_floor"]], 4))
    P("")
    P("ALL DRAW COUNTS (FULL period, share inside / two-panel nonzero / three-panel nonzero)")
    P(fmt(rescore[rescore.period == "FULL"].pivot_table(
        index=["assign", "bar"], columns="D", values="share"), 4))
    P("")

    # ---- movement against the incumbent POOLED verdict
    P("=" * 100)
    P("VERDICT MOVEMENT vs idea 567's POOLED bar (the queue's actual question)")
    P("=" * 100)
    mv_rows = []
    for period in ("FULL", "IS", "OOS"):
        for D in DRAW_COUNTS:
            fsub = floors[(floors.D == D) & (floors.period == period)].set_index("statistic")
            bar_map = {stat: {p: float(fsub.loc[stat, f"floor_{p}"]) for p in pnames}
                       for stat in STATS}
            base_fl = np.array([assign_floor(r.parents.split("+"), bar_map[r.family], "POOLED",
                                             small_name) for _, r in cen.iterrows()])
            for how in ASSIGNS:
                fl_claim = np.array([
                    assign_floor(r.parents.split("+"), bar_map[r.family], how, small_name)
                    for _, r in cen.iterrows()])
                for b in BARS:
                    m = cen.margin.to_numpy(float)
                    was = m < b * base_fl
                    now = m < b * fl_claim
                    to_in = int((~was & now).sum())
                    to_out = int((was & ~now).sum())
                    for sub_nm, msk in (("ALL", np.ones(len(cen), bool)),
                                        ("2PANEL", (cen.n_panels == 2).to_numpy()),
                                        ("3PANEL", (cen.n_panels == 3).to_numpy())):
                        mv_rows.append(dict(
                            period=period, D=D, assign=how, bar=b, subset=sub_nm,
                            n=int(msk.sum()),
                            was_inside=int(was[msk].sum()), now_inside=int(now[msk].sum()),
                            to_inside=int((~was & now)[msk].sum()),
                            to_outside=int((was & ~now)[msk].sum()),
                            net=int((~was & now)[msk].sum()) - int((was & ~now)[msk].sum()),
                            moved_share=float(((was != now)[msk]).mean())))
                    if period == "FULL" and D == 6:
                        P(f"  {how:<7s} bar {b:.1f}: was_inside {int(was.sum()):3d} -> "
                          f"now_inside {int(now.sum()):3d}   OUT->IN {to_in:3d}, "
                          f"IN->OUT {to_out:3d}, net {to_in-to_out:+4d}, "
                          f"moved {(was != now).mean():.1%}")
    moves = pd.DataFrame(mv_rows)
    P("")
    P("BY PANEL COUNT (D=6, FULL): the two-panel / three-panel asymmetry under each assignment")
    piv = moves[(moves.period == "FULL") & (moves.D == 6) & (moves.subset != "ALL")]
    P(fmt(piv.pivot_table(index=["assign", "bar"], columns="subset",
                          values="now_inside", aggfunc="sum"), 1))
    P("")
    P("BY NAMED-PARENT SET (D=6, FULL, bar 1.0): share inside under each assignment")
    ps_rows = []
    fsub = floors[(floors.D == 6) & (floors.period == "FULL")].set_index("statistic")
    bar_map = {stat: {p: float(fsub.loc[stat, f"floor_{p}"]) for p in pnames} for stat in STATS}
    for pset, grp in cen.groupby("parents"):
        d = dict(parents=pset, n=len(grp))
        for how in ASSIGNS:
            fl = np.array([assign_floor(r.parents.split("+"), bar_map[r.family], how, small_name)
                           for _, r in grp.iterrows()])
            d[how] = float((grp.margin.to_numpy(float) < 1.0 * fl).mean())
        ps_rows.append(d)
    psets = pd.DataFrame(ps_rows).set_index("parents")
    P(fmt(psets, 4))
    P("")

    # ---- hypotheses
    h = head[(head.bar == 1.0)].set_index("assign")
    pooled_share = float(h.loc["POOLED", "share"])
    rss_share = float(h.loc["RSS", "share"])
    min_share = float(h.loc["MIN", "share"])
    net_rss = int(moves[(moves.period == "FULL") & (moves.D == 6) & (moves["assign"] == "RSS")
                        & (moves.bar == 1.0) & (moves.subset == "ALL")].net.iloc[0])
    P(f"H_DIR   : net movement at RSS, D=6, bar 1.0 = {net_rss:+d} claims "
      f"({pooled_share:.1%} -> {rss_share:.1%} inside) -> "
      f"{'HOLDS (exonerates)' if net_rss < 0 else 'FALSIFIED - the parent-specific bar CONVICTS'}")
    asym_pool = float(h.loc["POOLED", "three_nz"]) - float(h.loc["POOLED", "two_nz"])
    asym_rss = float(h.loc["RSS", "three_nz"]) - float(h.loc["RSS", "two_nz"])
    P(f"H_TWO   : three-minus-two-panel nonzero inside-share gap {asym_pool:.4f} (POOLED) -> "
      f"{asym_rss:.4f} (RSS), {asym_rss/asym_pool if asym_pool else float('nan'):.2f}x -> "
      f"{'HOLDS' if abs(asym_rss) < 0.5*abs(asym_pool) else 'FALSIFIED - the asymmetry survives'}")
    spread = abs(rss_share - min_share)
    P(f"H_SPREAD: MIN {min_share:.1%} vs RSS {rss_share:.1%}, spread {spread*100:.1f} pp -> "
      f"{'HOLDS - the question is under-specified' if spread > 0.10 else 'FALSIFIED'}")
    P("")

    # ------------------------------------------------------------------ KEEP paths
    P("=" * 100)
    P("KEEP PATHS over the full price grid (PROTOCOL rule 4a and 4b, every book)")
    P("=" * 100)
    kp_rows = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b, s = bases[pn], spys[pn]
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    for arm, w in bks.items():
                        r = fast_backtest(sub, w, freq=cad)["returns"].loc[warm:]
                        f4b = fail_4b(r, s)
                        kp_rows.append(dict(parent=pn, kind=kind, seed=sd, arm=arm, gross=g,
                                            cadence=cad, keep4a=keep_4a(r, b), fail4b=f4b,
                                            keep4b=(f4b == "-")))
    kp = pd.DataFrame(kp_rows)
    P(f"over {len(kp)} books: 4a {int(kp.keep4a.sum())}/{len(kp)}, "
      f"4b {int(kp.keep4b.sum())}/{len(kp)}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}/{len(kp)}")
    P("  4b by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4b.sum().items()))
    P("  4b REAL books: " + ", ".join(
        f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence}"
        for _, r in kp[(kp.kind == "REAL") & kp.keep4b].iterrows()) or "  4b REAL books: none")
    P("  4b binding failure legs: " + ", ".join(
        f"{k} {v}" for k, v in kp.fail4b.value_counts().head(6).items()))
    P("")

    # ------------------------------------------------------------------ RULE 8
    P("=" * 100)
    P("RULE 8 WALK-FORWARD")
    P("=" * 100)
    P("WF-A: the ANSWER out of sample - floors rebuilt on IS only and OOS only, census re-scored")
    wfa = rescore[(rescore.D == 6) & (rescore.bar == 1.0)].pivot_table(
        index="assign", columns="period", values="share")
    P(fmt(wfa[["FULL", "IS", "OOS"]], 4))
    nets = moves[(moves.D == 6) & (moves.bar == 1.0) & (moves.subset == "ALL")].pivot_table(
        index="assign", columns="period", values="net")
    P("  net verdict movement vs POOLED, by period:")
    P(fmt(nets[["FULL", "IS", "OOS"]], 1))
    sign_ok = int(((np.sign(nets["IS"]) == np.sign(nets["OOS"])) | (nets["IS"] == 0)).sum())
    P(f"  direction of movement agrees IS vs OOS for {sign_ok} of {len(nets)} assignments")
    P("")

    P("WF-B: the RE-SCORE as a DECISION RULE, priced - act on the IS panel ordering only if")
    P("      its IS span clears bar x the assignment's floor, else stand down to RULES v2 U56.")
    real = grid[grid.kind == "REAL"]
    u56 = "U56"
    warm56 = parents[u56][0].index[260]
    base56 = bases[u56]
    spy56 = spys[u56]
    # OOS return series of every REAL MA-RS book, keyed (parent, gross, cadence)
    oos_series, full_series = {}, {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        for g in GROSS:
            bks = make_books(px, set(names), g)
            for cad in CADENCE:
                r = fast_backtest(px, bks["MA-RS"], freq=cad)["returns"].loc[warm:]
                full_series[(pn, g, cad)] = r
                oos_series[(pn, g, cad)] = r.loc[OOS_START:]
    fsubIS = floors[(floors.D == 6) & (floors.period == "IS")].set_index("statistic")
    ppIS = {p: float(fsubIS.loc["PREM_SHARPE", f"floor_{p}"]) for p in pnames}
    wf_rows = []
    for how in ASSIGNS:
        for b in BARS:
            acted, picks, segs = 0, [], []
            for g in GROSS:
                for cad in CADENCE:
                    prem = {pn: float(real[(real.parent == pn) & (real.gross == g)
                                           & (real.cadence == cad)
                                           & (real.arm == "MA-RS")].IS_dSharpe.iloc[0])
                            for pn in pnames}
                    order = sorted(prem, key=prem.get, reverse=True)
                    span = prem[order[0]] - prem[order[-1]]
                    fl = assign_floor(["U56", "B136", "SMALL"], ppIS, how, small_name)
                    act = span >= b * fl
                    acted += int(act)
                    picks.append(order[0] if act else "STANDDOWN")
                    segs.append(oos_series[(order[0], g, cad)] if act
                                else base56.loc[OOS_START:])
            idx = segs[0].index
            book = pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)
            mo = metrics(book)
            wf_rows.append(dict(assign=how, bar=b, acted=acted, cells=len(segs),
                                picks="/".join(picks),
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                OOS_MaxDD=mo["MaxDD"]))
    # controls: idea 567's ungated rule, the live book, SPY
    ctrl = []
    segs = [oos_series[(max(pnames, key=lambda pn: float(real[(real.parent == pn)
            & (real.gross == g) & (real.cadence == cad) & (real.arm == "MA-RS")]
            .IS_dSharpe.iloc[0])), g, cad)] for g in GROSS for cad in CADENCE]
    idx = segs[0].index
    ungated = pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)
    for nm, r in (("ALWAYS-ACT (idea 567's rule)", ungated),
                  ("RULES v2 U56 (live book)", base56.loc[OOS_START:]),
                  ("SPY", spy56.loc[OOS_START:])):
        m = metrics(r)
        ctrl.append(dict(assign=nm, bar=np.nan, acted=np.nan, cells=np.nan, picks="-",
                         OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    wf = pd.DataFrame(wf_rows + ctrl)
    P(fmt(wf.set_index(["assign", "bar"])[["acted", "cells", "OOS_CAGR", "OOS_Sharpe",
                                           "OOS_MaxDD"]], 4))
    bsh = metrics(base56.loc[OOS_START:])["Sharpe"]
    ssh = metrics(spy56.loc[OOS_START:])["Sharpe"]
    beat_b = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > bsh).sum())
    beat_s = int((wf.iloc[:len(wf_rows)].OOS_Sharpe > ssh).sum())
    P(f"  decision books beating RULES v2 U56 OOS Sharpe ({bsh:.4f}): {beat_b}/{len(wf_rows)}; "
      f"beating SPY ({ssh:.4f}): {beat_s}/{len(wf_rows)}")

    # 4a/4b on the decision books, judged over the FULL sample version of the same rule
    P("")
    P("  KEEP paths for the decision books (full-sample twin of each rule, 4a vs RULES v2 U56):")
    dk = []
    for how in ASSIGNS:
        for b in BARS:
            segs = []
            for g in GROSS:
                for cad in CADENCE:
                    prem = {pn: float(real[(real.parent == pn) & (real.gross == g)
                                           & (real.cadence == cad)
                                           & (real.arm == "MA-RS")].IS_dSharpe.iloc[0])
                            for pn in pnames}
                    order = sorted(prem, key=prem.get, reverse=True)
                    span = prem[order[0]] - prem[order[-1]]
                    fl = assign_floor(["U56", "B136", "SMALL"], ppIS, how, small_name)
                    segs.append(full_series[(order[0], g, cad)] if span >= b * fl else base56)
            idx = segs[0].index
            bk = pd.concat([s.reindex(idx).fillna(0.0) for s in segs], axis=1).mean(axis=1)
            f4 = fail_4b(bk, spy56.reindex(idx).fillna(0.0))
            dk.append(dict(assign=how, bar=b, CAGR=metrics(bk)["CAGR"],
                           Sharpe=metrics(bk)["Sharpe"], MaxDD=metrics(bk)["MaxDD"],
                           keep4a=keep_4a(bk, base56.reindex(idx).fillna(0.0)),
                           fail4b=f4, keep4b=(f4 == "-")))
    dkf = pd.DataFrame(dk)
    P(fmt(dkf.set_index(["assign", "bar"]), 4))
    P(f"  decision books: 4a {int(dkf.keep4a.sum())}/{len(dkf)}, 4b {int(dkf.keep4b.sum())}/{len(dkf)}, "
      f"BOTH {int((dkf.keep4a & dkf.keep4b).sum())}/{len(dkf)}")
    P("")

    # ------------------------------------------------------------------ write
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    floors.to_csv(OUT / f"{STAMP}.floors.csv", index=False)
    cen.to_csv(OUT / f"{STAMP}.census.csv", index=False)
    rescore.to_csv(OUT / f"{STAMP}.rescore.csv", index=False)
    moves.to_csv(OUT / f"{STAMP}.moves.csv", index=False)
    pd.concat([wf.assign(leg="WF-B_OOS"), dkf.assign(leg="WF-B_KEEP")],
              ignore_index=True).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"wrote grid {len(grid)}, floors {len(floors)}, census {len(cen)}, rescore {len(rescore)}, "
      f"moves {len(moves)}, keeppaths {len(kp)} in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
