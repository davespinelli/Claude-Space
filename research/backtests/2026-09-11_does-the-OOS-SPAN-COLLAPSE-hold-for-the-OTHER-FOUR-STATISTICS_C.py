#!/usr/bin/env python3
"""Idea 773 (lane C, 2026-09-11) - does-the-OOS-SPAN-COLLAPSE-hold-for-the-OTHER-FOUR-STATISTICS.

QUESTION
--------
Idea 567 (lane B, same day) measured the three-panel SPAN of the MA-gate premium against the
draw-level noise floor and found it falls from 1.58x its IS floor to 0.75x its OOS floor, while
the IS ordering U56>B136>SMALL439 flips at cadence M in 3 of 6 (gross, cadence) cells.  That is
a strong statement - out of sample the published panel ordering is smaller than one panel's own
composition luck - but it was measured for PREM_SHARPE ONLY.  The record quotes panel orderings
in four other currencies (SHARPE, CAGR, MAXDD, PREM_CAGR).  This run repeats the span-vs-floor
walk-forward for all five and reports which panel claims have ANY out-of-sample content.

"OOS content" is defined up front, before any new number is read:
    a statistic's panel ordering has OOS content iff, out of sample, the three-parent SPAN
    exceeds the draw floor built on the SAME OOS window (span/floor > 1) in a MAJORITY of the
    (gross, cadence) cells AND the IS ordering survives into OOS in a majority of them.
Span above the floor with a scrambled ordering is dispersion, not content; a stable ordering
inside the floor is a coin that keeps landing the same way at this draw count.

DESIGN (identical panels, draws and books to idea 567, so the two runs are directly comparable)
-----
Parents:  U56 research/universe.json (56 names, 64.3% ETF)
          B136 research/universe_broad.json (136 names)
          SMALL439 data/prices_small.csv.gz (439 names, max_1d_move < 1.0)
Draws:    k = 36 names, 24 crc32 seeds per parent, `DRAW|{parent}|{seed}`.  k is matched across
          parents so panel WIDTH never confounds parent identity.  U56 draws 36 of 56 so its
          draws overlap ~64% by construction and its floor is structurally smallest - reported,
          never corrected (idea 775 is the open question about exactly that).
Arms:     EWall  gross g over every priced tradable name                  (CONTROL)
          MA-RS  gross g over names above their 200d MA, RESPREAD         (TREATMENT)
Floor:    within-parent sd of the statistic across k-matched draws, averaged over the reported
          (gross, cadence) cells - idea 567's estimator verbatim.
Span:     max - min of the statistic across the three REAL parents at one (gross, cadence).
Margin:   the smallest ADJACENT gap in the three-parent ordering (the bar a 3-panel ordering
          claim actually has to clear; the span only bounds the two extremes).

TUNED PARAMETERS (PROTOCOL rule 4, exactly two, as the queue specifies):
    1. STATISTIC in {PREM_SHARPE, PREM_CAGR, SHARPE, CAGR, MAXDD}
    2. SPLIT     in {FULL, IS, OOS}
All 5 x 3 = 15 grid points are reported, at every gross, every cadence, every draw count and
both floor forms.  REPORTED (never selected) axes: gross g in {0.50, 0.75, 1.00}, cadence in
{W, M}, draw count D in {3, 6, 12, 24}, floor form in {POOLED, RSS}.  Nothing is picked on any
of them; the headline is quoted at D=6 (idea 567's D, for comparability) and D=24 (the most
draws, i.e. the best-resolved floor) and both are printed.

PRE-REGISTERED HYPOTHESES (written before any new number was read)
-----------------------------------------------------------------
IS567 = 1.58, OOS567 = 0.75   (idea 567's committed PREM_SHARPE span/floor ratios, D=6, POOLED)
H_REPRO    : this run reproduces IS567 and OOS567 to within 0.01 from its own rebuilt grid.
             If it does not, nothing downstream is trustworthy and the run reports that instead.
H_COLLAPSE : the OOS span/floor ratio is BELOW the IS span/floor ratio for a MAJORITY (>=3) of
             the five statistics.  This is the queue's premise stated as a number.
H_NONE     : at least one of the five statistics keeps OOS content by the definition above.
             Falsified => NO panel-ordering currency in the record survives out of sample.
H_LEVEL    : the LEVEL statistics (SHARPE, CAGR, MAXDD) carry a larger span/floor ratio than the
             PREMIUM statistics in both windows, because a level span inherits the parents'
             real return differences (and their differing survivorship bias) while a premium is
             an arm-minus-arm object measured inside one panel.

GATES (run and printed BEFORE any new number is read)
    G0 determinism : the crc32 draw scheme rebuilt twice gives identical name sets.     bar 0
    G1 identity    : fast_backtest vs engine.backtest on one book per parent.        bar 1e-12
    G2 reproduction: idea 567's committed .floors.csv rebuilt from source here, all 60
                     (statistic, D, period) rows and all 9 columns.                  bar 1e-12
    G3 reproduction: idea 567's committed .walkforward.csv ORDER rows (IS_span, OOS_span at all
                     six (gross, cadence) cells) rebuilt from source here.           bar 1e-12
    G4 reproduction: the live U56 RULES v2 row the record commits, 0.0861 / 1.1998 / -0.1205.
                                                                                     bar 1e-4
G2 and G3 make this a genuine same-day CROSS-LANE reproduction of lane B's numbers, not a
re-quote of them.

RULE 8 WALK-FORWARD (required, and it is the object of the question)
    IS = start..2016-12-31, OOS = 2017-01-01..end, OOS read ONCE.
    WF-A on the ANSWER: every span, floor, ratio and ordering is computed separately on IS and
       on OOS; the answer IS the IS-vs-OOS comparison.
    WF-B on a BOOK: the ordering claim taken at face value is a trading instruction - "run the
       book on the panel the ordering puts first".  Select (parent, gross, cadence) by IS Sharpe
       ALONE, then read OOS CAGR/Sharpe/MaxDD ONCE against RULES v2 on the same panel and
       against SPY.  Run once per statistic used as the selector, so the question "does the
       statistic you rank panels by change the book you end up holding?" is answered too.

KEEP PATHS: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and 4b (Sharpe > SPY
    in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) are evaluated for
    EVERY book on the grid and the counts reported.  Stated up front: a DRAW panel is a seeded
    random 36-name subset, not a rule anyone can trade, so a 4b pass on a draw is a diagnostic;
    only the REAL parents' books can be capital candidates.

SURVIVORSHIP: universe_broad.json and the small panel are CURRENT constituents.  On a premium
    (arm minus arm on the same panel) the bias largely cancels; on the LEVEL statistics it does
    not, so every level span here is an upper bound on the true one and every level floor a
    lower bound - which biases H_LEVEL toward holding.  Said again beside the result.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its own
outputs: .grid.csv .floors.csv .spans.csv .verdicts.csv .walkforward.csv .keeppaths.csv
.console.txt
"""
from __future__ import annotations

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
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_DRAW = 36
N_SEED = 24
DRAW_COUNTS = [3, 6, 12, 24]
STATS = ["PREM_SHARPE", "PREM_CAGR", "SHARPE", "CAGR", "MAXDD"]
SPLITS = ["FULL", "IS", "OOS"]
FLOOR_FORMS = ["POOLED", "RSS"]

PARENT567 = OUT / "2026-09-11_how-many-published-PANEL-ORDERING-claims-survive-a-draw-level-noise-floor_B"
IS567, OOS567 = 1.58, 0.75
V2_U56 = (0.0861, 1.1998, -0.1205)          # committed live RULES v2 row on U56
G1_TOL = G2_TOL = G3_TOL = 1e-12
G4_TOL = 1e-4

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
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
    """crc32-seeded k-matched draws, `DRAW|{parent}|{seed}` (idea 567's scheme verbatim)."""
    pool = np.array(sorted(names))
    out = []
    for sd in range(n_seed):
        seed = zlib.crc32(f"DRAW|{parent}|{sd}".encode()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        pick = sorted(rng.choice(pool, size=min(k, len(pool)), replace=False).tolist())
        out.append((sd, pick))
    return out


# ------------------------------------------------------------- statistic extraction
def stat_series(sub, stat, period="FULL"):
    """idea 567's estimator verbatim: the per-draw value of `stat` on window `period`."""
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


def real_value(real, pn, stat, period, g, cad):
    """The REAL parent's value of `stat` on window `period` at one (gross, cadence) cell."""
    sub = real[(real.parent == pn) & (real.gross == g) & (real.cadence == cad)]
    v = stat_series(sub, stat, period)
    return float(v.iloc[0])


# ------------------------------------------------------------------------- main
def main():
    t0 = time.time()
    P(f"# {STAMP}")
    P("# idea 773 - does the IS->OOS SPAN COLLAPSE idea 567 found for PREM_SHARPE hold for the")
    P("#            other four statistics the record ranks panels by?")
    P(f"# PROTOCOL: cost {COST:.0f} bps, next-day fills, IS <= {IS_END}, OOS >= {OOS_START}")
    P("# TUNED (2): STATISTIC x SPLIT.  REPORTED-NOT-SELECTED: gross, cadence, draw count D,")
    P("#            floor form.  ALL grid points printed and committed.")
    P("")
    P("PRE-REGISTERED: H_REPRO (567's 1.58x IS / 0.75x OOS reproduce here to 0.01),")
    P("  H_COLLAPSE (OOS ratio < IS ratio for >=3 of 5 statistics),")
    P("  H_NONE (>=1 statistic keeps OOS content: median OOS span/floor > 1 AND ordering stable")
    P("          in a majority of cells), H_LEVEL (level statistics carry a bigger ratio than")
    P("          premium statistics in both windows).")
    P("")

    parents = real_panels()
    pnames = list(parents)
    P("PARENTS: " + ", ".join(
        f"{k} ({len(v[1])} names, {v[0].index[0].date()}..{v[0].index[-1].date()})"
        for k, v in parents.items()))
    P("")

    # ---------------------------------------------------------------- gates
    P("=" * 100)
    P("GATES (printed before any new number is read)")
    P("=" * 100)
    g0 = 0
    for pn, (_, names) in parents.items():
        a = [set(x[1]) for x in draws(pn, names)]
        b = [set(x[1]) for x in draws(pn, names)]
        g0 += sum(0 if x == y else 1 for x, y in zip(a, b))
        assert all(len(x) == min(K_DRAW, len(names)) for x in a)
    P(f"G0 determinism  : {g0} of {N_SEED*len(parents)} draws differ on rebuild (bar 0) -> "
      f"{'PASS' if g0 == 0 else 'FAIL'}")

    g1 = 0.0
    for pn, (px, names) in parents.items():
        bk = make_books(px, set(names), 0.75)["MA-RS"]
        a = fast_backtest(px, bk, freq="W")["returns"]
        b = backtest(px, bk, cost_bps=COST, freq="W")["returns"]
        g1 = max(g1, float(np.abs(a.values - b.values).max()))
    P(f"G1 identity     : fast_backtest vs engine.backtest max |dret| = {g1:.3e} "
      f"(bar {G1_TOL:.0e}) -> {'PASS' if g1 <= G1_TOL else 'FAIL'}")

    g4 = float("nan")
    px56 = parents["U56"][0]
    warm56 = px56.index[260]
    b56 = fast_backtest(px56, rules_v2_weights(px56), freq="W")["returns"].loc[warm56:]
    m56 = metrics(b56)
    g4 = max(abs(m56["CAGR"] - V2_U56[0]), abs(m56["Sharpe"] - V2_U56[1]),
             abs(m56["MaxDD"] - V2_U56[2]))
    P(f"G4 reproduction : live RULES v2 on U56 = {m56['CAGR']:.4f} / {m56['Sharpe']:.4f} / "
      f"{m56['MaxDD']:.4f} vs committed {V2_U56} max |d| = {g4:.3e} (bar {G4_TOL:.0e}) -> "
      f"{'PASS' if g4 <= G4_TOL else 'FAIL'}")
    P("  (G2 and G3 reproduce idea 567's committed floors and spans; they need the grid and are")
    P("   printed immediately after it, before any NEW number is read.)")
    P("")

    # ---------------------------------------------------------------- price grid
    P("=" * 100)
    P("PRICE LEG - REAL parents + 24 k=36 draws each, 3 gross x 2 cadence x 2 arms")
    P("=" * 100)
    rows = []
    spy_cache = {}
    for pn, (px, names) in parents.items():
        spy_cache[pn] = px["SPY"].pct_change().fillna(0.0)
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            warm = sub.index[260]
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    res = {a: fast_backtest(sub, w, freq=cad) for a, w in bks.items()}
                    base = {a: r["returns"].loc[warm:] for a, r in res.items()}
                    ew_m, ew_is, ew_oos = (metrics(base["EWall"]),
                                           metrics(base["EWall"].loc[:IS_END]),
                                           metrics(base["EWall"].loc[OOS_START:]))
                    for arm in ("EWall", "MA-RS"):
                        r = base[arm]
                        d = rowify(r, res[arm]["turnover"].loc[warm:])
                        d.update(parent=pn, kind=kind, seed=sd, arm=arm, gross=g, cadence=cad,
                                 k=len(pick))
                        d["dSharpe_vs_EWall"] = d["Sharpe"] - ew_m["Sharpe"]
                        d["dCAGR_vs_EWall"] = d["CAGR"] - ew_m["CAGR"]
                        d["IS_dSharpe"] = metrics(r.loc[:IS_END])["Sharpe"] - ew_is["Sharpe"]
                        d["OOS_dSharpe"] = metrics(r.loc[OOS_START:])["Sharpe"] - ew_oos["Sharpe"]
                        rows.append(d)
        P(f"  {pn}: {len(units)} panels done ({time.time()-t0:.0f}s)")
    grid = pd.DataFrame(rows)
    real = grid[(grid.kind == "REAL")]
    dr = grid[grid.kind == "DRAW"]
    P("")

    # ---------------------------------------------------------------- floors
    fl_rows = []
    for stat in STATS:
        for D in DRAW_COUNTS:
            for period in SPLITS:
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
                pooled = float(np.nanmean(list(per_parent.values())))
                row = dict(statistic=stat, D=D, period=period, floor_pooled=pooled,
                           floor_max=float(np.nanmax(list(per_parent.values()))),
                           floor_min=float(np.nanmin(list(per_parent.values()))))
                row.update({f"floor_{k}": v for k, v in per_parent.items()})
                row["parent_ratio"] = row["floor_max"] / row["floor_min"] if row["floor_min"] else np.nan
                fl_rows.append(row)
    floors = pd.DataFrame(fl_rows)

    def floor_of(stat, D, period):
        return floors[(floors.statistic == stat) & (floors.D == D)
                      & (floors.period == period)].iloc[0]

    # -------------------------------------------------- G2 / G3 cross-lane reproduction
    P("=" * 100)
    P("G2 / G3 - CROSS-LANE REPRODUCTION of idea 567 from source (still no new number read)")
    P("=" * 100)
    g2 = g3 = float("nan")
    try:
        f567 = pd.read_csv(f"{PARENT567}.floors.csv")
        cols = [c for c in f567.columns if c not in ("statistic", "D", "period")]
        mg = f567.merge(floors, on=["statistic", "D", "period"], suffixes=("_c", "_r"))
        assert len(mg) == len(f567) == 60, (len(mg), len(f567))
        g2 = max(float(np.abs(mg[c + "_c"] - mg[c + "_r"]).max()) for c in cols)
        P(f"G2 reproduction : idea 567 .floors.csv, all {len(f567)} rows x {len(cols)} cols, "
          f"max |d| = {g2:.3e} (bar {G2_TOL:.0e}) -> {'PASS' if g2 <= G2_TOL else 'FAIL'}")
    except Exception as e:  # pragma: no cover - reported, never silently skipped
        P(f"G2 reproduction : FAILED TO RUN ({e!r})")
    try:
        w567 = pd.read_csv(f"{PARENT567}.walkforward.csv")
        o567 = w567[w567.leg == "ORDER"][["gross", "cadence", "IS_span", "OOS_span"]]
        mine = []
        for g in GROSS:
            for cad in CADENCE:
                vi = {pn: real_value(real, pn, "PREM_SHARPE", "IS", g, cad) for pn in pnames}
                vo = {pn: real_value(real, pn, "PREM_SHARPE", "OOS", g, cad) for pn in pnames}
                mine.append(dict(gross=g, cadence=cad,
                                 IS_span=max(vi.values()) - min(vi.values()),
                                 OOS_span=max(vo.values()) - min(vo.values())))
        mine = pd.DataFrame(mine)
        mg3 = o567.merge(mine, on=["gross", "cadence"], suffixes=("_c", "_r"))
        assert len(mg3) == 6, len(mg3)
        g3 = max(float(np.abs(mg3[c + "_c"] - mg3[c + "_r"]).max()) for c in ("IS_span", "OOS_span"))
        P(f"G3 reproduction : idea 567 .walkforward.csv ORDER spans, all 6 cells, "
          f"max |d| = {g3:.3e} (bar {G3_TOL:.0e}) -> {'PASS' if g3 <= G3_TOL else 'FAIL'}")
    except Exception as e:  # pragma: no cover
        P(f"G3 reproduction : FAILED TO RUN ({e!r})")
    P("")

    # ---------------------------------------------------------------- SPANS (the new leg)
    P("=" * 100)
    P("SPANS - three-parent span and margin per (STATISTIC, SPLIT), all cells reported")
    P("=" * 100)
    sp_rows = []
    for stat in STATS:
        for period in SPLITS:
            for g in GROSS:
                for cad in CADENCE:
                    v = {pn: real_value(real, pn, stat, period, g, cad) for pn in pnames}
                    order = sorted(v, key=lambda k: v[k], reverse=True)
                    vals = [v[p] for p in order]
                    gaps = [a - b for a, b in zip(vals, vals[1:])]
                    span = vals[0] - vals[-1]
                    j = int(np.argmin(gaps))
                    margin = gaps[j]
                    row = dict(statistic=stat, period=period, gross=g, cadence=cad,
                               order=">".join(order), span=span, margin=margin,
                               top=order[0], span_pair=f"{order[0]}|{order[-1]}",
                               margin_pair=f"{order[j]}|{order[j+1]}")
                    row.update({f"val_{p}": v[p] for p in pnames})
                    for D in DRAW_COUNTS:
                        fl = floor_of(stat, D, period)
                        pooled = fl.floor_pooled
                        rss_span = float(np.hypot(fl[f"floor_{order[0]}"], fl[f"floor_{order[-1]}"]))
                        rss_marg = float(np.hypot(fl[f"floor_{order[j]}"], fl[f"floor_{order[j+1]}"]))
                        row[f"floorP_D{D}"] = pooled
                        row[f"spanR_POOLED_D{D}"] = span / pooled
                        row[f"marginR_POOLED_D{D}"] = margin / pooled
                        row[f"floorR_D{D}"] = rss_span
                        row[f"spanR_RSS_D{D}"] = span / rss_span
                        row[f"marginR_RSS_D{D}"] = margin / rss_marg
                    sp_rows.append(row)
    spans = pd.DataFrame(sp_rows)

    for D in (6, 24):
        P("")
        P(f"--- span / floor and margin / floor, D = {D} (median over the 6 gross x cadence cells)")
        agg = []
        for stat in STATS:
            for period in SPLITS:
                s = spans[(spans.statistic == stat) & (spans.period == period)]
                agg.append(dict(statistic=stat, period=period,
                                span=s.span.median(), floor=s[f"floorP_D{D}"].iloc[0],
                                spanR_POOLED=s[f"spanR_POOLED_D{D}"].median(),
                                spanR_RSS=s[f"spanR_RSS_D{D}"].median(),
                                marginR_POOLED=s[f"marginR_POOLED_D{D}"].median(),
                                marginR_RSS=s[f"marginR_RSS_D{D}"].median(),
                                cells_span_gt1=int((s[f"spanR_POOLED_D{D}"] > 1).sum()),
                                cells_margin_gt1=int((s[f"marginR_POOLED_D{D}"] > 1).sum())))
        agg = pd.DataFrame(agg)
        P(fmt(agg.set_index(["statistic", "period"]), 4))
        if D == 6:
            agg6 = agg.copy()
        else:
            agg24 = agg.copy()

    P("")
    P("--- every (statistic, split, gross, cadence) cell: ordering and span (D=6 POOLED bar)")
    P(fmt(spans.set_index(["statistic", "period", "gross", "cadence"])
          [["order", "span", "margin", "spanR_POOLED_D6", "marginR_POOLED_D6"]], 4))

    # ---------------------------------------------------------------- ordering stability
    P("")
    P("=" * 100)
    P("ORDERING STABILITY - does the IS ordering survive into OOS, per statistic?")
    P("=" * 100)
    st_rows = []
    for stat in STATS:
        same = 0
        top_same = 0
        for g in GROSS:
            for cad in CADENCE:
                oi = spans[(spans.statistic == stat) & (spans.period == "IS")
                           & (spans.gross == g) & (spans.cadence == cad)].iloc[0]
                oo = spans[(spans.statistic == stat) & (spans.period == "OOS")
                           & (spans.gross == g) & (spans.cadence == cad)].iloc[0]
                same += int(oi["order"] == oo["order"])
                top_same += int(oi["top"] == oo["top"])
                st_rows.append(dict(statistic=stat, gross=g, cadence=cad, IS_order=oi["order"],
                                    OOS_order=oo["order"], same=oi["order"] == oo["order"],
                                    top_same=oi["top"] == oo["top"],
                                    IS_span=oi["span"], OOS_span=oo["span"]))
        P(f"  {stat:12s}: full ordering survives {same}/6 cells, top panel survives {top_same}/6")
    stab = pd.DataFrame(st_rows)
    P("")
    P(fmt(stab.set_index(["statistic", "gross", "cadence"]), 4))

    # ---------------------------------------------------------------- verdicts
    P("")
    P("=" * 100)
    P("VERDICT PER STATISTIC - does the panel ordering have ANY out-of-sample content?")
    P("=" * 100)
    ver = []
    for stat in STATS:
        for D in DRAW_COUNTS:
            for form in FLOOR_FORMS:
                row = dict(statistic=stat, D=D, floor_form=form)
                for period in SPLITS:
                    s = spans[(spans.statistic == stat) & (spans.period == period)]
                    sr = s[f"spanR_{form}_D{D}"]
                    mr = s[f"marginR_{form}_D{D}"]
                    row[f"spanR_{period}"] = float(sr.median())
                    row[f"marginR_{period}"] = float(mr.median())
                    row[f"cells_gt1_{period}"] = int((sr > 1).sum())
                sub = stab[stab.statistic == stat]
                row["order_same"] = int(sub.same.sum())
                row["top_same"] = int(sub.top_same.sum())
                row["collapse"] = row["spanR_OOS"] < row["spanR_IS"]
                row["OOS_content"] = bool(row["cells_gt1_OOS"] >= 4 and row["order_same"] >= 4)
                ver.append(row)
    verd = pd.DataFrame(ver)
    P(fmt(verd.set_index(["statistic", "D", "floor_form"]), 4))

    head = verd[(verd.D == 6) & (verd.floor_form == "POOLED")].set_index("statistic")
    P("")
    P("HEADLINE (D=6, POOLED bar - idea 567's exact bar):")
    for stat in STATS:
        r = head.loc[stat]
        P(f"  {stat:12s} span/floor IS {r.spanR_IS:5.2f}x -> OOS {r.spanR_OOS:5.2f}x  "
          f"({'COLLAPSE' if r.collapse else 'NO COLLAPSE'}); OOS cells above floor "
          f"{int(r.cells_gt1_OOS)}/6; ordering survives {int(r.order_same)}/6  => "
          f"{'OOS CONTENT' if r.OOS_content else 'NO OOS CONTENT'}")

    # hypotheses
    P("")
    ps = head.loc["PREM_SHARPE"]
    d_is, d_oos = abs(ps.spanR_IS - IS567), abs(ps.spanR_OOS - OOS567)
    P(f"H_REPRO   : PREM_SHARPE IS {ps.spanR_IS:.4f} vs 567's {IS567} (|d| {d_is:.4f}); "
      f"OOS {ps.spanR_OOS:.4f} vs {OOS567} (|d| {d_oos:.4f}) -> "
      f"{'HOLDS' if max(d_is, d_oos) <= 0.01 else 'FALSIFIED'}")
    n_col = int(head.collapse.sum())
    P(f"H_COLLAPSE: OOS ratio below IS ratio in {n_col} of 5 statistics -> "
      f"{'HOLDS' if n_col >= 3 else 'FALSIFIED'}")
    n_cont = int(head.OOS_content.sum())
    P(f"H_NONE    : {n_cont} of 5 statistics keep OOS content -> "
      f"{'HOLDS' if n_cont >= 1 else 'FALSIFIED (no panel-ordering currency survives OOS)'}")
    lev = head.loc[["SHARPE", "CAGR", "MAXDD"]]
    pre = head.loc[["PREM_SHARPE", "PREM_CAGR"]]
    h_lev = bool(lev.spanR_IS.min() > pre.spanR_IS.max() and lev.spanR_OOS.min() > pre.spanR_OOS.max())
    P(f"H_LEVEL   : level span/floor IS [{lev.spanR_IS.min():.2f}, {lev.spanR_IS.max():.2f}] vs "
      f"premium [{pre.spanR_IS.min():.2f}, {pre.spanR_IS.max():.2f}]; OOS level "
      f"[{lev.spanR_OOS.min():.2f}, {lev.spanR_OOS.max():.2f}] vs premium "
      f"[{pre.spanR_OOS.min():.2f}, {pre.spanR_OOS.max():.2f}] -> "
      f"{'HOLDS' if h_lev else 'FALSIFIED'}")

    # ---------------------------------------------------------------- KEEP paths
    P("")
    P("=" * 100)
    P("KEEP PATHS 4a / 4b over every book on the grid")
    P("=" * 100)
    bases = {}
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        bases[pn] = fast_backtest(px, rules_v2_weights(px), freq="W")["returns"].loc[warm:]
        s = spy_cache[pn].loc[warm:]
        mb, msp = metrics(bases[pn]), metrics(s)
        P(f"  BASE {pn}: RULES v2 {mb['CAGR']:.2%} / {mb['Sharpe']:.4f} / {mb['MaxDD']:.2%} "
          f"(OOS Sharpe {metrics(bases[pn].loc[OOS_START:])['Sharpe']:.4f})   "
          f"SPY {msp['CAGR']:.2%} / {msp['Sharpe']:.4f} / {msp['MaxDD']:.2%} "
          f"(OOS Sharpe {metrics(s.loc[OOS_START:])['Sharpe']:.4f})")
    kp_rows = []
    for pn, (px, names) in parents.items():
        warm = px.index[260]
        b, s = bases[pn], spy_cache[pn].loc[warm:]
        units = [("REAL", -1, sorted(names))] + [("DRAW", sd, pick) for sd, pick in draws(pn, names)]
        for kind, sd, pick in units:
            cols = list(dict.fromkeys(pick + ["SPY"]))
            sub = px[cols].dropna(how="all").ffill()
            w0 = sub.index[260]
            for g in GROSS:
                bks = make_books(sub, set(pick), g)
                for cad in CADENCE:
                    for arm, w in bks.items():
                        r = fast_backtest(sub, w, freq=cad)["returns"].loc[w0:]
                        f4b = fail_4b(r, s)
                        kp_rows.append(dict(parent=pn, kind=kind, seed=sd, arm=arm, gross=g,
                                            cadence=cad, keep4a=keep_4a(r, b), fail4b=f4b,
                                            keep4b=(f4b == "-")))
    kp = pd.DataFrame(kp_rows)
    P("")
    P(f"  over {len(kp)} books: 4a {int(kp.keep4a.sum())}, 4b {int(kp.keep4b.sum())}, "
      f"BOTH {int((kp.keep4a & kp.keep4b).sum())}")
    P("  4a by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4a.sum().items()))
    P("  4b by parent: " + ", ".join(f"{k} {int(v)}" for k, v in kp.groupby('parent').keep4b.sum().items()))
    P("  4a/4b on the REAL parents only: "
      + ", ".join(f"{r.parent}/{r.arm}/g{r.gross}/{r.cadence} 4a={r.keep4a} 4b={r.keep4b}"
                  for _, r in kp[(kp.kind == "REAL") & (kp.keep4a | kp.keep4b)].iterrows()) or "none")
    P("  4b binding failure legs: " + ", ".join(
        f"{k} {v}" for k, v in kp.fail4b.value_counts().head(6).items()))

    # ---------------------------------------------------------------- WF-B
    P("")
    P("=" * 100)
    P("RULE 8 WALK-FORWARD, WF-B: trade the panel the ordering puts first")
    P("=" * 100)
    P("  Selector: (parent, gross, cadence) picked on the IS window ALONE by each statistic in")
    P("  turn; OOS 2017+ read ONCE against RULES v2 on that panel and against SPY.")
    ma = real[real.arm == "MA-RS"]
    wfb = []
    for stat in STATS:
        cand = []
        for _, rr in ma.iterrows():
            pn, g, cad = rr["parent"], rr["gross"], rr["cadence"]
            cand.append(dict(statistic=stat, parent=pn, gross=g, cadence=cad,
                             IS_value=real_value(real, pn, stat, "IS", g, cad),
                             OOS_CAGR=rr["OOS_CAGR"], OOS_Sharpe=rr["OOS_Sharpe"],
                             OOS_MaxDD=rr["OOS_MaxDD"],
                             base_OOS_Sharpe=metrics(bases[pn].loc[OOS_START:])["Sharpe"],
                             base_OOS_CAGR=metrics(bases[pn].loc[OOS_START:])["CAGR"],
                             base_OOS_MaxDD=metrics(bases[pn].loc[OOS_START:])["MaxDD"],
                             spy_OOS_Sharpe=metrics(spy_cache[pn].loc[parents[pn][0].index[260]:]
                                                    .loc[OOS_START:])["Sharpe"],
                             spy_OOS_CAGR=metrics(spy_cache[pn].loc[parents[pn][0].index[260]:]
                                                  .loc[OOS_START:])["CAGR"],
                             spy_OOS_MaxDD=metrics(spy_cache[pn].loc[parents[pn][0].index[260]:]
                                                   .loc[OOS_START:])["MaxDD"]))
        c = pd.DataFrame(cand)
        # MAXDD is "higher is better" as a signed number; every other statistic likewise
        best = c.sort_values("IS_value", ascending=False).iloc[0]
        c["selected"] = (c.parent == best.parent) & (c.gross == best.gross) & (c.cadence == best.cadence)
        wfb.append(c)
    wfb = pd.concat(wfb, ignore_index=True)
    sel = wfb[wfb.selected]
    P("")
    P(fmt(sel.set_index(["statistic", "parent", "gross", "cadence"])
          [["IS_value", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "base_OOS_Sharpe",
            "base_OOS_CAGR", "base_OOS_MaxDD", "spy_OOS_Sharpe", "spy_OOS_CAGR",
            "spy_OOS_MaxDD"]], 4))
    P("")
    for _, r in sel.iterrows():
        P(f"  {r.statistic:12s} picks {r.parent} g{r.gross:.2f} {r.cadence}: OOS "
          f"{r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%}  | RULES v2 "
          f"{r.base_OOS_CAGR:.2%} / {r.base_OOS_Sharpe:.4f} / {r.base_OOS_MaxDD:.2%}  | SPY "
          f"{r.spy_OOS_CAGR:.2%} / {r.spy_OOS_Sharpe:.4f} / {r.spy_OOS_MaxDD:.2%}  -> "
          f"{'BEATS' if r.OOS_Sharpe > r.base_OOS_Sharpe else 'LOSES TO'} baseline, "
          f"{'BEATS' if r.OOS_Sharpe > r.spy_OOS_Sharpe else 'LOSES TO'} SPY on OOS Sharpe")
    n_pick = sel.parent.nunique()
    P("")
    P(f"  The five statistics pick {n_pick} distinct parent(s): "
      + ", ".join(f"{r.statistic}->{r.parent}" for _, r in sel.iterrows()))
    P(f"  Across all {len(ma)} REAL MA-RS books: beat RULES v2 OOS Sharpe "
      f"{int((wfb[wfb.statistic=='SHARPE'].OOS_Sharpe > wfb[wfb.statistic=='SHARPE'].base_OOS_Sharpe).sum())}"
      f"/{len(ma)}, beat SPY OOS Sharpe "
      f"{int((wfb[wfb.statistic=='SHARPE'].OOS_Sharpe > wfb[wfb.statistic=='SHARPE'].spy_OOS_Sharpe).sum())}"
      f"/{len(ma)}")

    # ---------------------------------------------------------------- write
    grid.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    floors.to_csv(OUT / f"{STAMP}.floors.csv", index=False)
    spans.to_csv(OUT / f"{STAMP}.spans.csv", index=False)
    verd.to_csv(OUT / f"{STAMP}.verdicts.csv", index=False)
    pd.concat([wfb.assign(leg="WF-B"), stab.assign(leg="ORDER")], ignore_index=True).to_csv(
        OUT / f"{STAMP}.walkforward.csv", index=False)
    kp.to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    P("")
    P(f"wrote grid {len(grid)}, floors {len(floors)}, spans {len(spans)}, verdicts {len(verd)}, "
      f"keeppaths {len(kp)} rows in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
