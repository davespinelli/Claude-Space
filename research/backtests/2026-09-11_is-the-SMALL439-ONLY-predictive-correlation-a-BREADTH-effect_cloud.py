#!/usr/bin/env python3
"""
IDEA 761 - is the SMALL439-ONLY predictive correlation a BREADTH effect?
=======================================================================
Cloud lane, 2026-09-11.

THE QUESTION.  Idea 560 measured the correlation between an IS drop-rate statistic and a
gate's OOS advantage over its depth-matched control, across a 27-cell grid (3 gate families
x 9 thresholds) inside each panel.  It reads

    SMALL439  +0.4815 .. +0.6505          U56  -0.0330 .. +0.1169      B136  +0.0026 .. +0.1893

i.e. the screen only works on the small-cap panel.  SMALL439 carries 439 names against 55 and
135, so every cell's legs are averages over 8x / 3x more names and are correspondingly less
noisy.  A correlation measured across cells is ATTENUATED by per-cell noise, so a panel-size
gap of that size is exactly what pure BREADTH would produce with no small-cap content at all.

    BREADTH  -> a RANDOM 55-name subset of SMALL439 should read like U56 (~0).
    CONTENT  -> a random 55-name subset of SMALL439 should stay near +0.5.

Those are different predictions on the same object, so this run just measures it.

CONSTRUCTION (idea 560's, verbatim, re-run on random supports).
  support S (a set of tickers priced on the panel's own calendar), family V, threshold th:
    GATE    = absolute-threshold gate on V                       (MA-DIST / MOM12_1 / LOWVOL)
    CONTROL = top ceil(x*n_t) names by V each day, x = the gate's own mean breadth
    books   = RESPREAD, gross 0.75, weekly, 10 bps, next-day (engine convention)
    ADVANTAGE     = sel_geo_pp = 100 x (CAGR(gate, zero-cost) - CAGR(control, zero-cost))
    rbar_drop     = annualised return rate of the names the gate declines to hold
    STATISTIC     DROP   = -rbar_drop            (560's own object, the one 761 quotes)
                  SPREAD = rbar_add - rbar_drop  (560's best pooled correlate)
    both signed so HIGHER = predicts a BIGGER advantage.
    r(support) = pearson over that support's 27 cells of (IS statistic, OOS advantage).

SUPPORTS
  FULL       U56 (55 names), B136 (135), SMALL439 (439)              - 560's own three, reproduced
  SMALL@55   D random 55-name subsets of SMALL439                    - size-matched to U56
  SMALL@135  D random 135-name subsets of SMALL439                   - size-matched to B136
  B136@55    D random 55-name subsets of B136                        - PLACEBO: does shrinking a
                                                                       LARGE panel move r at all?

TUNED PARAMETERS - exactly 2, all grid points reported:
  (1) SUBSET SIZE   n in {55, 135}          (+ the three full panels as fixed references)
  (2) DRAWS         D = 30 per (support, size), seed 761, every draw's r reported in the CSV
  The statistic (2) x window (3) axes are REPORTED IN FULL, not tuned: no number below is
  chosen by looking at them.

RULE 8 WALK-FORWARD (required).  IS = start..2016-12-31, OOS = 2017-01-01..end, read once.
  A. CENSUS   per-draw r at every (support, statistic, window); distributions vs the full-panel
              references; the attenuation model (signal vs between-draw noise) that BREADTH
              predicts, with its predicted r printed beside the observed one.
  B. DECISION per draw x family, pick th = argmax(IS statistic) and score its OOS advantage
              against that cell's own median threshold.
  C. BOOK     per draw x family, pick th on the IS window ALONE by (i) IS Sharpe (PROTOCOL's
              rule-8 selector) and (ii) the IS statistic; read the OOS once and score the book's
              OOS CAGR / Sharpe / MaxDD against RULES v2 ON THE SAME SUPPORT and against SPY.
              BOTH KEEP PATHS on every book (4a vs live RULES v2, 4b vs SPY).

GATES (pre-registered, all reported pass or fail):
  G0  fast_run reproduces engine.backtest returns AND turnover to 1e-12 on a subset support.
  G1  three-leg identity |ADD + DROP + BOTH - gap| <= 1e-12 on every cell.
  G2  the three FULL panels reproduce idea 560's committed .census.csv per-panel columns
      (r_U56 / r_B136 / r_SMALL439 at DROP x 3 windows) to 1e-6.
  G3  depth match |mean breadth(gate) - mean breadth(control)| on every cell.
  G4  draw determinism: the seeded draw list re-generates byte-identically.

SURVIVORSHIP: SMALL439 and B136 are CURRENT constituents only - names that died are absent, so
every CAGR level here is inflated and neither KEEP column is immune.  The 44 SMALL names with
max_1d_move >= 1.0 are dropped first (data/small_meta.csv), idea 560's own filter.  The census
leg compares arm-minus-arm differences inside one support, where the bias very largely cancels;
the BOOK leg does not, and is read with that in mind.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .cells.csv .draws.csv .census.csv .decision.csv .walkforward.csv .keeppaths.csv
         .console.txt
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_BPS = 10
GROSS = 0.75
CADENCE = "W"
FAMILIES = ["MA-DIST", "MOM12_1", "LOWVOL"]
THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]     # 560's grid
CVOL = [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.80]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
TRAIL3Y_START = "2014-01-01"
TRAIL1Y_START = "2016-01-01"
WINDOWS = {"FULL_IS": (None, IS_END), "TRAIL3Y": (TRAIL3Y_START, IS_END),
           "TRAIL1Y": (TRAIL1Y_START, IS_END)}
STATS = ["DROP", "SPREAD"]

SIZES = [55, 135]          # tuned param 1
DRAWS = 30                 # tuned param 2
SEED = 761

EPS = 1e-12
BAR_ENGINE = 1e-12
BAR_IDENT = 1e-12
BAR_REPRO = 1e-6

IDEA560 = REPO / "research" / "backtests" / \
    "2026-09-11_is-rbar_drop-a-screening-statistic_B.census.csv"

OUT = Path(__file__).with_suffix("")
LOG = []
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 400)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def fast_run(px, W, cost_bps=COST_BPS, freq=CADENCE):
    """Bit-for-bit replica of engine.backtest (gated G0)."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, m = rets.shape
    held = np.empty((n, m))
    turn = np.zeros(n)
    cur = np.zeros(m)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index),
            "weights": pd.DataFrame(held, index=px.index, columns=px.columns)}


def stat(r):
    h = len(r) // 2
    m, mi, mo = metrics(r), metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def verdict_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def fail_4b(s, spy):
    t = {"H1": s["H1"] > spy["H1"], "H2": s["H2"] > spy["H2"],
         "OOS": s["oSharpe"] > spy["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def cagr(r):
    return metrics(r)["CAGR"]


def rank_var(px, fam):
    live = live_mask(px)
    if fam == "MA-DIST":
        return (px / px.rolling(200).mean() - 1).where(live), live
    if fam == "MOM12_1":
        return (px.shift(21) / px.shift(252) - 1).where(live), live
    if fam == "LOWVOL":
        vol = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (-vol).where(live), live
    raise ValueError(fam)


def thresholds(fam):
    return [-c for c in CVOL] if fam == "LOWVOL" else list(THETA)


def gate_abs(px, fam, th):
    """560's own forms, including the MULTIPLICATIVE MA-DIST gate (last-float-bit exact)."""
    live = live_mask(px)
    if fam == "MA-DIST":
        return (px > px.rolling(200).mean() * (1 + th)) & live
    if fam == "MOM12_1":
        return ((px.shift(21) / px.shift(252) - 1) > th).fillna(False) & live
    if fam == "LOWVOL":
        vol = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (vol < -th).fillna(False) & live
    raise ValueError(fam)


def gate_quantile(V, live, x):
    n = live.sum(axis=1)
    kt = np.ceil(x * n).astype(int).clip(lower=1)
    rank = V.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def respread(g):
    k = g.sum(axis=1).clip(lower=1)
    return g.astype(float).div(k, axis=0) * GROSS


def leg_series(A, B, R):
    on_a, on_b = A > EPS, B > EPS
    add, drop, both = on_a & ~on_b, on_b & ~on_a, on_a & on_b
    cA = (A.where(add, 0.0) * R).sum(axis=1)
    cD = -(B.where(drop, 0.0) * R).sum(axis=1)
    cC = ((A.where(both, 0.0) - B.where(both, 0.0)) * R).sum(axis=1)
    wA = A.where(add, 0.0).sum(axis=1)
    wD = B.where(drop, 0.0).sum(axis=1)
    r0a, r0b = (A * R).sum(axis=1), (B * R).sum(axis=1)
    gb = B.sum(axis=1)
    return dict(cA=cA, cD=cD, cC=cC, wA=wA, wD=wD, r0a=r0a, r0b=r0b, gb=gb)


def window_legs(S, lo, hi):
    sl = slice(lo, hi)
    cA, cD, cC = S["cA"].loc[sl], S["cD"].loc[sl], S["cC"].loc[sl]
    wA, wD = S["wA"].loc[sl], S["wD"].loc[sl]
    r0a, r0b, gb = S["r0a"].loc[sl], S["r0b"].loc[sl], S["gb"].loc[sl]
    gap = r0a - r0b
    return dict(ident_max=float((cA + cD + cC - gap).abs().max()),
                sel_geo_pp=100 * (cagr(r0a) - cagr(r0b)),
                rbar_add=float(252 * 100 * cA.sum() / wA.sum()) if wA.sum() > 1e-12 else np.nan,
                rbar_drop=float(252 * 100 * (-cD).sum() / wD.sum()) if wD.sum() > 1e-12 else np.nan,
                rbar_ctrl=float(252 * 100 * r0b.sum() / gb.sum()) if gb.sum() > 1e-12 else np.nan)


def signed(row, which, w):
    if which == "DROP":
        return -row[f"rbar_drop_{w}"]
    if which == "SPREAD":
        return row[f"rbar_add_{w}"] - row[f"rbar_drop_{w}"]
    raise ValueError(which)


def spearman(a, b):
    return float(a.rank().corr(b.rank()))


def pear_t(r, n):
    return r * np.sqrt(max(n - 2, 1) / max(1 - r ** 2, 1e-12))


# ------------------------------------------------------------------ one support = 27 cells
def run_support(px, spy_px, tag):
    """Run the full 27-cell grid on one price support.  Returns (cells DataFrame, comparands)."""
    start = px.index[260]
    years = len(px.loc[start:]) / 252
    R = px.pct_change().fillna(0.0).loc[start:]
    nlive = live_mask(px).loc[start:].sum(axis=1)
    spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
    live_s = stat(fast_run(px, rules_v2_weights(px))["returns"].loc[start:])
    rows, g1, g3 = [], 0.0, 0.0
    for fam in FAMILIES:
        V, lv = rank_var(px, fam)
        for th in thresholds(fam):
            gA = gate_abs(px, fam, th)
            x = float((gA.loc[start:].sum(axis=1) / nlive).mean())
            gB = gate_quantile(V, lv, x)
            xq = float((gB.loc[start:].sum(axis=1) / nlive).mean())
            g3 = max(g3, abs(x - xq))
            ra = fast_run(px, respread(gA))
            rb = fast_run(px, respread(gB))
            sa = stat(ra["returns"].loc[start:])
            S = leg_series(ra["weights"].loc[start:], rb["weights"].loc[start:], R)
            d = dict(support=tag, family=fam, th=th, x=x, xq=xq,
                     turn_yr=float(ra["turnover"].loc[start:].sum() / years), **sa)
            for wn, (lo, hi) in WINDOWS.items():
                wl = window_legs(S, lo, hi)
                g1 = max(g1, wl["ident_max"])
                for k in ("rbar_add", "rbar_drop", "rbar_ctrl", "sel_geo_pp"):
                    d[f"{k}_{wn}"] = wl[k]
            wl = window_legs(S, OOS_START, None)
            g1 = max(g1, wl["ident_max"])
            d["OOS_adv"] = wl["sel_geo_pp"]
            d["p4a"] = verdict_4a(sa, live_s)
            d["f4b"] = fail_4b(sa, spy_s)
            rows.append(d)
    return pd.DataFrame(rows), dict(spy=spy_s, live=live_s, start=start, years=years,
                                    n_names=px.shape[1], g1=g1, g3=g3)


def census_rows(cells, tag, size, draw):
    out = []
    for st in STATS:
        for wn in WINDOWS:
            sv = cells.apply(lambda r: signed(r, st, wn), axis=1)
            d = pd.concat([sv.rename("stat"), cells["OOS_adv"], cells["family"]], axis=1).dropna()
            if len(d) < 3:
                continue
            r = float(d.stat.corr(d.OOS_adv))
            row = dict(support=tag, size=size, draw=draw, statistic=st, window=wn, n=len(d),
                       pearson=r, spearman=spearman(d.stat, d.OOS_adv), t=pear_t(r, len(d)))
            for f in FAMILIES:
                s = d[d.family == f]
                row[f"r_{f}"] = float(s.stat.corr(s.OOS_adv)) if len(s) > 2 else np.nan
            out.append(row)
    return out


# ================================================================== main
def main():
    P("=" * 180)
    P("IDEA 761 - is the SMALL439-ONLY predictive correlation a BREADTH effect?   cloud, 2026-09-11")
    P("=" * 180)
    P("PROTOCOL: 10 bps/unit turnover, next-day execution (engine), no shorting, no leverage,")
    P(f"gross {GROSS}, cadence {CADENCE}.  IS = start..{IS_END}, OOS = {OOS_START}..end (read once).")
    P(f"2 tuned params: SUBSET SIZE in {SIZES} and DRAWS = {DRAWS} (seed {SEED}).  Statistic x")
    P("window axes reported in full.  Both KEEP paths on every book in leg C.")
    P("SURVIVORSHIP: B136 and SMALL439 are CURRENT constituents only; CAGR levels inflated and")
    P("neither KEEP column is immune.  The census leg is arm-minus-arm inside one support.")

    # ---------------------------------------------------------------- panels
    u = load_universe()
    b = load_universe(broad=True)
    s = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = sorted(set(meta.loc[meta.max_1d_move >= 1.0, "ticker"]))
    PN = {
        "U56": (u.drop(columns=["SPY"]), u["SPY"]),
        "B136": (b.drop(columns=["SPY"], errors="ignore"), b["SPY"]),
        "SMALL439": (s[[c for c in s.columns if c != "SPY" and c not in set(bad)]], s["SPY"]),
    }
    P(f"\nPanels: " + "  ".join(f"{k} {v[0].shape[1]} names x {len(v[0])} rows"
                                for k, v in PN.items())
      + f"   ({len(bad)} SMALL names dropped for max_1d_move >= 1.0)")

    # ---------------------------------------------------------------- G0
    P("\n" + "=" * 180)
    P("G0  fast_run vs engine.backtest (on a 55-name SMALL subset, the object this run uses)")
    P("=" * 180)
    rng0 = np.random.default_rng(SEED)
    probe = PN["SMALL439"][0][list(rng0.choice(PN["SMALL439"][0].columns, 55, replace=False))]
    W = rules_v2_weights(probe)
    a = backtest(probe, W, cost_bps=COST_BPS, freq=CADENCE)
    f = fast_run(probe, W)
    g0 = max(float((a["returns"] - f["returns"]).abs().max()),
             float((a["turnover"] - f["turnover"]).abs().max()))
    P(f"  max |d returns|, |d turnover| = {g0:.3e}  (bar {BAR_ENGINE:.0e})  "
      f"{'PASS' if g0 < BAR_ENGINE else 'FAIL'}")
    flush_log()

    # ---------------------------------------------------------------- full-panel references
    P("\n" + "=" * 180)
    P("FULL-PANEL REFERENCES (idea 560's own three supports, re-run here)")
    P("=" * 180)
    CELLS, CENSUS, COMP = [], [], {}
    g1_max, g3_max = 0.0, 0.0
    for pn in PN:
        px, spy_px = PN[pn]
        c, comp = run_support(px, spy_px, pn)
        g1_max, g3_max = max(g1_max, comp["g1"]), max(g3_max, comp["g3"])
        CELLS.append(c.assign(size=comp["n_names"], draw=-1))
        CENSUS.extend(census_rows(c, pn, comp["n_names"], -1))
        COMP[pn] = comp
        sp, lv = comp["spy"], comp["live"]
        P(f"  {pn:9s} {comp['n_names']:3d} names  {comp['start'].date()}..{px.index[-1].date()} "
          f"({comp['years']:.2f} yrs)")
        P(f"      SPY        CAGR {sp['CAGR']:.4f} Sharpe {sp['Sharpe']:.4f} MaxDD {sp['MaxDD']:.4f}"
          f"  H1/H2 {sp['H1']:.4f}/{sp['H2']:.4f}  OOS {sp['oCAGR']:.4f}/{sp['oSharpe']:.4f}/{sp['oMaxDD']:.4f}")
        P(f"      RULES v2   CAGR {lv['CAGR']:.4f} Sharpe {lv['Sharpe']:.4f} MaxDD {lv['MaxDD']:.4f}"
          f"  H1/H2 {lv['H1']:.4f}/{lv['H2']:.4f}  OOS {lv['oCAGR']:.4f}/{lv['oSharpe']:.4f}/{lv['oMaxDD']:.4f}")
        flush_log()

    REF = pd.DataFrame(CENSUS)
    P("\n  Per-panel r over the 27 cells (this run's rebuild):")
    P(fmt(REF.pivot_table(index=["statistic", "window"], columns="support", values="pearson")))

    # ---------------------------------------------------------------- G1 / G2 / G3
    C0 = pd.concat(CELLS)
    P("\n" + "=" * 180)
    P("GATES G1 / G2 / G3")
    P("=" * 180)
    P(f"G1 three-leg identity |ADD+DROP+BOTH - gap|, worst cell-window over the full panels = "
      f"{g1_max:.3e}  (bar {BAR_IDENT:.0e})  {'PASS' if g1_max < BAR_IDENT else 'FAIL'}")
    P(f"G3 depth match max |breadth(gate) - breadth(control)| over the full panels = {g3_max:.3e}")
    if IDEA560.exists():
        ref = pd.read_csv(IDEA560)
        ref = ref[ref.statistic.isin(STATS)].set_index(["statistic", "window"])
        mine = REF.pivot_table(index=["statistic", "window"], columns="support", values="pearson")
        d = []
        for (st, wn), row in mine.iterrows():
            if (st, wn) not in ref.index:
                continue
            rr = ref.loc[(st, wn)]
            for pn in PN:
                d.append(dict(statistic=st, window=wn, panel=pn, ref=float(rr[f"r_{pn}"]),
                              mine=float(row[pn]), d=abs(float(rr[f"r_{pn}"]) - float(row[pn]))))

        D2 = pd.DataFrame(d)
        g2 = float(D2.d.max())
        P(f"G2 reproduction of idea 560 .census.csv per-panel columns ({len(D2)} points):")
        P(fmt(D2.pivot_table(index=["statistic", "window"], columns="panel", values="d"), 6))
        P(f"   G2 max {g2:.3e}  (bar {BAR_REPRO:.0e})  {'PASS' if g2 < BAR_REPRO else 'FAIL'}")
        by = D2.groupby("panel").d.max()
        P("   by panel: " + "  ".join(f"{k} {v:.3e}" for k, v in by.items()))
        D2.to_csv(f"{OUT}.g2.csv", index=False)
    else:
        g2 = np.nan
        P("G2 SKIPPED - idea 560 census.csv not on disk")
    flush_log()

    # ---------------------------------------------------------------- the draws
    P("\n" + "=" * 180)
    P(f"A.  CENSUS - {DRAWS} random subsets per (parent, size), seed {SEED}")
    P("=" * 180)
    rng = np.random.default_rng(SEED)
    plan = [("SMALL439", n) for n in SIZES] + [("B136", 55)]
    draw_lists = {}
    for parent, n in plan:
        cols = list(PN[parent][0].columns)
        draw_lists[(parent, n)] = [sorted(rng.choice(cols, n, replace=False).tolist())
                                   for _ in range(DRAWS)]
    # G4 determinism
    rng2 = np.random.default_rng(SEED)
    ok4 = True
    for parent, n in plan:
        cols = list(PN[parent][0].columns)
        for k in range(DRAWS):
            if sorted(rng2.choice(cols, n, replace=False).tolist()) != draw_lists[(parent, n)][k]:
                ok4 = False
    P(f"G4 draw determinism (same seed re-generates all {len(plan)*DRAWS} draws): "
      f"{'PASS' if ok4 else 'FAIL'}")

    DRAWCELLS = []
    for parent, n in plan:
        tag = f"{parent}@{n}"
        P(f"\n  {tag}: running {DRAWS} draws x 27 cells x 2 arms ...")
        for k, cols in enumerate(draw_lists[(parent, n)]):
            px = PN[parent][0][cols]
            c, comp = run_support(px, PN[parent][1], tag)
            g1_max, g3_max = max(g1_max, comp["g1"]), max(g3_max, comp["g3"])
            c = c.assign(size=n, draw=k, parent=parent)
            DRAWCELLS.append(c)
            COMP[(tag, k)] = comp
            CENSUS.extend(census_rows(c, tag, n, k))
        P(f"    done.")
        flush_log()

    CA = pd.concat(CELLS + DRAWCELLS, ignore_index=True)
    CA.to_csv(f"{OUT}.cells.csv", index=False)
    CE = pd.DataFrame(CENSUS)
    CE.to_csv(f"{OUT}.draws.csv", index=False)

    # ---------------------------------------------------------------- the answer
    P("\n" + "=" * 180)
    P("A1.  THE ANSWER - r by support, every statistic x window, all draws reported in .draws.csv")
    P("=" * 180)
    dr = CE[CE.draw >= 0]
    fu = CE[CE.draw < 0].set_index(["statistic", "window", "support"]).pearson

    tbl = []
    for st in STATS:
        for wn in WINDOWS:
            row = dict(statistic=st, window=wn,
                       U56=fu.get((st, wn, "U56"), np.nan),
                       B136=fu.get((st, wn, "B136"), np.nan),
                       SMALL439=fu.get((st, wn, "SMALL439"), np.nan))
            for tag in [f"SMALL439@{n}" for n in SIZES] + ["B136@55"]:
                v = dr[(dr.statistic == st) & (dr.window == wn) & (dr.support == tag)].pearson
                row[f"{tag}_med"] = float(v.median())
                row[f"{tag}_mean"] = float(v.mean())
                row[f"{tag}_p10"] = float(v.quantile(0.10))
                row[f"{tag}_p90"] = float(v.quantile(0.90))
                row[f"{tag}_pos"] = float((v > 0).mean())
            tbl.append(row)
    T = pd.DataFrame(tbl)
    P(fmt(T[["statistic", "window", "U56", "B136", "SMALL439",
             "SMALL439@55_med", "SMALL439@55_p10", "SMALL439@55_p90", "SMALL439@55_pos",
             "SMALL439@135_med", "SMALL439@135_p10", "SMALL439@135_p90",
             "B136@55_med", "B136@55_p10", "B136@55_p90"]]))
    T.to_csv(f"{OUT}.census.csv", index=False)

    P("\n  READING (DROP, the statistic idea 761 quotes):")
    for wn in WINDOWS:
        r = T[(T.statistic == "DROP") & (T.window == wn)].iloc[0]
        keep_frac = float(dr[(dr.statistic == "DROP") & (dr.window == wn) &
                             (dr.support == "SMALL439@55")].pearson.gt(r["U56"]).mean())
        P(f"    {wn:8s}  full SMALL439 {r['SMALL439']:+.4f} -> SMALL@55 median "
          f"{r['SMALL439@55_med']:+.4f} [p10 {r['SMALL439@55_p10']:+.4f}, p90 "
          f"{r['SMALL439@55_p90']:+.4f}]  vs U56 {r['U56']:+.4f}  vs B136 {r['B136']:+.4f}")
        P(f"              SMALL@135 median {r['SMALL439@135_med']:+.4f}   B136@55 (placebo) median "
          f"{r['B136@55_med']:+.4f}   draws above the U56 reference: {keep_frac:.0%}")
    P("\n  BREADTH predicts SMALL@55 ~ U56 (~0).  CONTENT predicts SMALL@55 ~ +0.5.")

    # ---------------------------------------------------------------- attenuation model
    P("\n" + "=" * 180)
    P("A2.  THE ATTENUATION MODEL - what pure BREADTH predicts, quantitatively")
    P("=" * 180)
    P("Each cell's OOS advantage is measured with noise that shrinks with panel size.  Across")
    P("draws of a given size the same (family, th) cell gives a spread: that is the NOISE.  The")
    P("spread of the draw-MEAN advantage across cells is the SIGNAL.  Classical attenuation then")
    P("predicts r(size) = r_true * sqrt(var_signal / (var_signal + var_noise)).")
    att = []
    for parent, n in plan:
        tag = f"{parent}@{n}"
        sub = CA[CA.support == tag]
        gm = sub.groupby(["family", "th"]).OOS_adv
        var_noise = float(gm.var().mean())
        var_sig = float(gm.mean().var())
        lam = np.sqrt(var_sig / (var_sig + var_noise)) if var_sig + var_noise > 0 else np.nan
        full = "SMALL439" if parent == "SMALL439" else "B136"
        subf = CA[CA.support == full]
        for st in STATS:
            for wn in WINDOWS:
                obs = float(dr[(dr.support == tag) & (dr.statistic == st) &
                               (dr.window == wn)].pearson.median())
                # r_true taken as the parent panel's own full-support r (the least favourable
                # assumption for BREADTH: the full panel is itself attenuated)
                rt = float(fu.get((st, wn, full), np.nan))
                att.append(dict(support=tag, statistic=st, window=wn, var_signal=var_sig,
                                var_noise=var_noise, lam=lam, r_full=rt, r_pred=rt * lam,
                                r_obs=obs, d=obs - rt * lam))
    A = pd.DataFrame(att)
    P(fmt(A, 4))
    P(f"\n  Mean |observed - attenuation-predicted| = {A.d.abs().mean():.4f}; "
      f"mean signed {A.d.mean():+.4f} (positive = MORE survives than breadth alone predicts).")
    A.to_csv(f"{OUT}.attenuation.csv", index=False)
    flush_log()

    # ---------------------------------------------------------------- B. decision leg
    P("\n" + "=" * 180)
    P("B.  DECISION - pick th = argmax(IS statistic) per (support, family); score OOS advantage")
    P("=" * 180)
    dec = []
    for (tag, size, draw), g in CA.groupby(["support", "size", "draw"]):
        for fam in FAMILIES:
            sub = g[g.family == fam]
            if sub.empty:
                continue
            oos = sub.set_index("th").OOS_adv
            for st in STATS:
                for wn in WINDOWS:
                    sv = sub.apply(lambda r: signed(r, st, wn), axis=1)
                    sv = sv.dropna()
                    if sv.empty:
                        continue
                    pick = float(sub.loc[sv.idxmax(), "th"])
                    adv = float(oos.loc[pick])
                    dec.append(dict(support=tag, size=size, draw=draw, family=fam, statistic=st,
                                    window=wn, pick=pick, pick_OOS_adv=adv,
                                    median_OOS_adv=float(oos.median()),
                                    beat_median=bool(adv > oos.median()),
                                    rank_of_pick=int((oos > adv).sum()) + 1))
    DEC = pd.DataFrame(dec)
    DEC.to_csv(f"{OUT}.decision.csv", index=False)
    P(fmt(DEC.groupby(["support", "statistic"]).agg(
        picks=("beat_median", "size"), beat_median=("beat_median", "mean"),
        mean_rank=("rank_of_pick", "mean"), mean_adv=("pick_OOS_adv", "mean"),
        cell_median=("median_OOS_adv", "mean"))))
    P("  (random pick = 50% beat-median, mean rank 5.000 of 9)")
    flush_log()

    # ---------------------------------------------------------------- C. book leg / rule 8
    P("\n" + "=" * 180)
    P("C.  BOOK LEG / RULE 8 - th chosen on the IS window ALONE, OOS read once, both KEEP paths")
    P("=" * 180)
    P("Selectors: IS_SHARPE = argmax IS Sharpe of the gate book (PROTOCOL's rule-8 selector);")
    P("IS_DROP / IS_SPREAD = argmax of the IS statistic (FULL_IS window).  Comparands are RULES v2")
    P("and SPY computed ON THE SAME SUPPORT.")
    wf = []
    for (tag, size, draw), g in CA.groupby(["support", "size", "draw"]):
        comp = COMP[tag] if draw < 0 else COMP[(tag, draw)]
        sp, lv = comp["spy"], comp["live"]
        for fam in FAMILIES:
            sub = g[g.family == fam]
            if sub.empty:
                continue
            sels = {"IS_SHARPE": sub.isSharpe,
                    "IS_DROP": sub.apply(lambda r: signed(r, "DROP", "FULL_IS"), axis=1),
                    "IS_SPREAD": sub.apply(lambda r: signed(r, "SPREAD", "FULL_IS"), axis=1)}
            for sn, sv in sels.items():
                sv = sv.dropna()
                if sv.empty:
                    continue
                row = sub.loc[sv.idxmax()]
                wf.append(dict(support=tag, size=size, draw=draw, family=fam, selector=sn,
                               th=float(row.th), CAGR=row.CAGR, Sharpe=row.Sharpe,
                               MaxDD=row.MaxDD, H1=row.H1, H2=row.H2, isSharpe=row.isSharpe,
                               oCAGR=row.oCAGR, oSharpe=row.oSharpe, oMaxDD=row.oMaxDD,
                               turn_yr=row.turn_yr,
                               base_oCAGR=lv["oCAGR"], base_oSharpe=lv["oSharpe"],
                               base_oMaxDD=lv["oMaxDD"],
                               spy_oCAGR=sp["oCAGR"], spy_oSharpe=sp["oSharpe"],
                               spy_oMaxDD=sp["oMaxDD"],
                               beat_base_oos=bool(row.oSharpe > lv["oSharpe"]),
                               beat_spy_oos=bool(row.oSharpe > sp["oSharpe"]),
                               p4a=verdict_4a(row, lv), f4b=fail_4b(row, sp)))
    WF = pd.DataFrame(wf)
    WF["p4b"] = WF.f4b == "-"
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.groupby(["support", "selector"]).agg(
        books=("p4a", "size"), oCAGR=("oCAGR", "mean"), oSharpe=("oSharpe", "mean"),
        oMaxDD=("oMaxDD", "mean"), base_oSharpe=("base_oSharpe", "mean"),
        spy_oSharpe=("spy_oSharpe", "mean"), beat_base=("beat_base_oos", "mean"),
        beat_spy=("beat_spy_oos", "mean"), p4a=("p4a", "sum"), p4b=("p4b", "sum"))))
    P(f"\n  TOTAL books {len(WF)}:  4a passes {int(WF.p4a.sum())}   4b passes {int(WF.p4b.sum())}")
    fb = WF[~WF.p4b].f4b.str.split(",").explode().value_counts()
    P("  binding 4b bars (count of books failing each): " +
      "  ".join(f"{k} {v}" for k, v in fb.items()))
    P("\n  FULL-PANEL books (the ones a reader can act on), every row:")
    P(fmt(WF[WF.draw < 0][["support", "family", "selector", "th", "CAGR", "Sharpe", "MaxDD",
                           "H1", "H2", "oCAGR", "oSharpe", "oMaxDD", "base_oSharpe",
                           "spy_oSharpe", "turn_yr", "p4a", "f4b"]]))
    keep = WF[WF.p4b | WF.p4a]
    P(f"\n  KEEP-candidates (4a or 4b): {len(keep)}")
    if len(keep):
        P(fmt(keep[["support", "family", "selector", "th", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                    "oCAGR", "oSharpe", "oMaxDD", "p4a", "p4b"]]))
    WF.to_csv(f"{OUT}.keeppaths.csv", index=False)
    flush_log()

    P("\n" + "=" * 180)
    P("VERDICT")
    P("=" * 180)
    P(f"  G0 {g0:.3e}  G1 {g1_max:.3e}  G2 {g2:.3e}  G3 {g3_max:.3e}  G4 {'PASS' if ok4 else 'FAIL'}")
    flush_log()


if __name__ == "__main__":
    main()
