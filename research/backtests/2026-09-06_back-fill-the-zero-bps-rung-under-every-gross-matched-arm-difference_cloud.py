#!/usr/bin/env python3
"""Idea 261 - "back-fill-the-zero-bps-rung-under-every-gross-matched-arm-difference" (cloud, 2026-09-06).

The question
------------
Idea 260 found that idea 82's published isolate

    FWD - RANDH  =  -0.0213 Sharpe   (quoted at PROTOCOL's 10 bps rung)

moves -0.0111 -> -0.0213 -> -0.0416 across the 0 / 10 / 30 bps rungs, i.e. roughly 52% of
the published magnitude is not the effect the label names, it is the two arms' TURNOVER
DIFFERENCE priced at the rung the number happened to be quoted at.  The contaminant is
invisible at any single rung because BOTH arms pay it; only the 0-bps twin exposes it.

Almost every arm difference the project publishes is gross-matched (idea 73's NORM /
idea 240's constant-gross convention) precisely so that the two arms differ in ONE dial.
Gross matching does not match turnover.  So the queue's charge is:

    re-read every gross-matched arm difference in the record beside its 0-bps twin and
    report how many published magnitudes are MAJORITY-COST.

Pre-registered definition (written before any number was read)
-------------------------------------------------------------
A difference `D` between two arms, published at cost rung c, is

    MAJORITY-COST   iff   |D(c) - D(0)|  >  0.5 * |D(c)|

i.e. more than half of the quoted magnitude is the cost term.  A difference that CHANGES
SIGN between 0 and c is majority-cost by construction (the cost term then exceeds the
quoted magnitude outright) and is reported separately as a SIGN FLIP, which is the
strictly worse failure: there the published verdict, not just its size, is a rung artefact.

Three tiers of evidence, in increasing order of directness
----------------------------------------------------------
TIER L (live, exact).  A pre-registered library of gross-matched one-dial arm pairs is
    re-run here from scratch on three panels, at 0 / 10 / 25 bps.  Costs are exact, not
    approximated: `engine.backtest` computes `port = (held*rets).sum(1) - turnover*c/1e4`
    and neither `held` nor `turnover` depends on c, so each book is run ONCE at 0 bps and
    every other rung is derived as `r(c) = r(0) - turnover*c/1e4`.  The identity is
    asserted against a live 10 bps `backtest()` call and the run aborts if it fails.
    This tier answers the question directly for the families the record actually publishes
    (ranking key, count, 200d gate, vol cap, vol scaler, cadence).

TIER V (estimator validation).  The record's committed grids do not carry return series,
    only summary rows.  But the cost drag is a known function of turnover:

        AnnRet(c) = AnnRet(0) - (c/1e4) * TO          TO = annualised turnover, x/yr
        Sharpe(c) ~ Sharpe(0) - (c/1e4) * TO / Vol
        CAGR(c)   ~ CAGR(0)   - (c/1e4) * TO          (to first order in the drag)

    so a single-rung row that carries `TO` (and `Vol`, for the Sharpe form) can be
    back-filled to 0 bps.  Tier V measures that estimator's ERROR against tier L's exact
    truth, on all 51 live books, before it is used on anything.  If the error is large
    relative to the 0.5 threshold, tier R is reported as indicative only and said so.

TIER R (the record).  Every committed `research/backtests/*.grid.csv` is scanned.
    (i) how many carry more than one cost rung at all (the queue's premise);
    (ii) MULTI-RUNG grids: the 0-bps twin is obtained by linear extrapolation through the
         two lowest rungs actually run - no turnover model, no estimator;
    (iii) SINGLE-RUNG grids carrying turnover: the tier-V estimator is applied.
    Pairs are formed only between rows that agree on every dial column but ONE and whose
    `gross` column matches to 1e-6 - that is what "gross-matched arm difference" means.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (5: 5/10/20/40/60)
The ARM is the hypothesis axis, the COST RUNG is the reported axis the queue names, and
the seed is reported per draw.  Nothing is selected on an outcome outside rule 8's IS window.

Walk-forward (PROTOCOL rule 8), fixed with direction before any OOS number was read
    IS = 2009-01-01..2016-12-31, OOS = 2017-01-01..end.
    ANCHOR      FWD20 weekly                          (do-nothing control)
    EWALL       EWall                                 (the record's other do-nothing)
    PICK@10     arm = argmax IS Sharpe scored at 10 bps  (the record's convention)
    PICK@0      arm = argmax IS Sharpe scored at  0 bps  (the queue's convention)
    The point of the last pair: if published magnitudes are majority-cost, then which rung
    you score on should change WHICH ARM you pick, and rule 8 prices that in OOS Sharpe.
    Reported OOS CAGR / Sharpe / MaxDD against RULES v1 OOS and SPY OOS, per panel.

Verdicts (both KEEP paths, on every arm, at every rung)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: universe.json / universe_broad.json are CURRENT constituents, and the small
panel (data/SMALL_PANEL_README.md) is a current sub-$2B screen - all three are
one-directional.  For THIS question the bias is close to neutral: it inflates every arm's
return, and the statistic reported is a RATIO of a difference to a difference, in which a
common additive premium largely cancels.  It does not cancel in the 4a/4b counts, which
are therefore optimistic, and is restated with them.  Per instruction, the small panel
first drops every ticker with `max_1d_move >= 1.0` in data/small_meta.csv (44 of 483).

Deterministic (fixed seeds), standalone.  Reads baseline.py and committed grid CSVs;
modifies nothing outside its own outputs.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import glob
import json
import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights
from engine import backtest, metrics, rebalance_mask

RUNGS = [0, 10, 25]
PUB_RUNG = 10                 # PROTOCOL's rung; the one the record quotes
GROSS = 0.75
MAX_VOL = 0.60
NS = [5, 10, 20, 40, 60]
ANCHOR_N = 20
SEEDS = [0, 1, 2]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
MAJ = 0.5                     # pre-registered majority-cost threshold
GROSS_TOL = 0.01              # realised mean gross may drift between rebalances; nominal gross is exact
TINY_S = 0.02                 # |dSharpe| below this is "too small to publish" - reported separately
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)


# ------------------------------------------------------------------ panels
def build_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)

    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxs = load_universe(small=True)
    keep = [c for c in pxs.columns if c != "SPY" and c not in bad]
    pxs = pxs[keep + ["SPY"]].dropna(how="all").ffill()

    return {
        "U56":      (px56, set(px56.columns)),                    # SPY tradable (record convention)
        "B136":     (px136, set(px136.columns)),
        "SMALL439": (pxs, set(keep)),                             # SPY = benchmark only
    }, len(bad)


# ------------------------------------------------------------------ books (all gross-matched)
def gates(px, tradable, gate=True, volcap=True):
    _, above, vol20 = score(px)
    m = pd.DataFrame(True, index=px.index, columns=px.columns)
    if gate:
        m &= above
    if volcap:
        m &= (vol20 < MAX_VOL)
    m &= px.notna()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def _rand_key(px, seed):
    """idea 82's RAND, byte-for-byte: one uniform per name, drawn once, held forever."""
    rng = np.random.default_rng(1000 + seed)
    return pd.DataFrame(np.tile(rng.random(px.shape[1]), (len(px.index), 1)),
                        index=px.index, columns=px.columns)


def make_weights(px, tradable, spec):
    """spec: dict(key=..., n=..., gate=..., volcap=..., seed=...). Gross matched at GROSS."""
    elig = gates(px, tradable, spec.get("gate", True), spec.get("volcap", True))
    key_name = spec["key"]
    if key_name == "EW":
        sel = elig.astype(float)
    else:
        if key_name == "RAND":
            key, asc = _rand_key(px, spec["seed"]), False
        elif key_name == "FWDVS":
            key, asc = score(px, vol_scale=True)[0], False
        else:
            key = score(px, vol_scale=False)[0]
            asc = (key_name == "REV")
        rank = key.where(elig).rank(axis=1, ascending=asc)
        sel = (rank <= spec["n"]).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


# ------------------------------------------------------------------ arm library (pre-registered)
def arm_library():
    """Anchor plus one-dial neighbours. `fam` names the dial the pair differs in."""
    A = dict(key="FWD", n=ANCHOR_N, gate=True, volcap=True, freq="W")
    arms = {"FWD20": A}
    arms["EWall"] = dict(A, key="EW", n=None)
    arms["REV20"] = dict(A, key="REV")
    arms["FWDVS20"] = dict(A, key="FWDVS")
    for s in SEEDS:
        arms[f"RAND20_s{s}"] = dict(A, key="RAND", seed=s)
    for n in NS:
        if n != ANCHOR_N:
            arms[f"FWD{n}"] = dict(A, n=n)
    arms["FWD20_nogate"] = dict(A, gate=False)
    arms["FWD20_novolcap"] = dict(A, volcap=False)
    arms["FWD20_M"] = dict(A, freq="M")
    arms["FWD20_Q"] = dict(A, freq="Q")
    arms["EWall_M"] = dict(A, key="EW", n=None, freq="M")
    return arms


# pre-registered pair list: (label, arm_a, arm_b, family). D = a - b, published as "a beats b by D".
def pair_list():
    P = [("EWall-FWD20", "EWall", "FWD20", "RANKKEY"),
         ("FWD20-REV20", "FWD20", "REV20", "RANKKEY"),
         ("FWDVS20-FWD20", "FWDVS20", "FWD20", "SCALER")]
    P += [(f"FWD20-RAND20_s{s}", "FWD20", f"RAND20_s{s}", "RANKKEY") for s in SEEDS]
    P += [(f"FWD{n}-FWD20", f"FWD{n}", "FWD20", "COUNT") for n in NS if n != ANCHOR_N]
    P += [("FWD20-FWD20_nogate", "FWD20", "FWD20_nogate", "GATE200"),
          ("FWD20-FWD20_novolcap", "FWD20", "FWD20_novolcap", "VOLCAP"),
          ("FWD20_M-FWD20", "FWD20_M", "FWD20", "CADENCE"),
          ("FWD20_Q-FWD20", "FWD20_Q", "FWD20", "CADENCE"),
          ("EWall_M-EWall", "EWall_M", "EWall", "CADENCE")]
    return P


# ------------------------------------------------------------------ stats helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def pass4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail4b(r, spy):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    mo = metrics(r.loc[OOS_START:])
    mso = metrics(spy.loc[OOS_START:])
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not mo["Sharpe"] > mso["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def cost_share(d0, dc):
    """Fraction of the magnitude published at rung c that is the cost term."""
    if not np.isfinite(d0) or not np.isfinite(dc) or dc == 0:
        return np.nan
    return abs(dc - d0) / abs(dc)


def breakeven_bps(d0, dc, c):
    """Rung at which a difference linear in cost crosses zero (nan if it never does at c>=0)."""
    slope = (dc - d0) / c
    if slope == 0 or not np.isfinite(slope):
        return np.nan
    b = -d0 / slope
    return b if b > 0 else np.nan


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ================================================================== TIER L
def run_tier_L():
    panels, n_dropped = build_panels()
    arms = arm_library()
    rows, series = [], {}

    print("=" * 200)
    print(f"Idea 261 back-fill-the-zero-bps-rung-under-every-gross-matched-arm-difference | {SCRIPT}")
    print(f"gross matched at {GROSS} on every arm | next-day execution | rungs {RUNGS} bps | "
          f"small panel dropped {n_dropped} tickers with max_1d_move>=1.0")
    print("=" * 200)

    for pname, (px, tradable) in panels.items():
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=PUB_RUNG, freq="W")["returns"].loc[start:]
        print(f"\n{pname}: {len(tradable)} tradable, {px.index[0].date()} -> {px.index[-1].date()}, "
              f"eval from {start.date()}, {yrs.loc[2015:2024].max()} rows in the busiest year")

        checked = False
        for aname, spec in arms.items():
            w = make_weights(px, tradable, spec)
            res = backtest(px, w, cost_bps=0.0, freq=spec["freq"])
            r0, turn = res["returns"], res["turnover"]
            if not checked:                                    # harness identity, once per panel
                live = backtest(px, w, cost_bps=float(PUB_RUNG), freq=spec["freq"])["returns"]
                err = float(np.max(np.abs((r0 - turn * PUB_RUNG / 1e4) - live)))
                print(f"  harness identity |derived - live @{PUB_RUNG}bps| max = {err:.3e}")
                if err > 1e-12:
                    print("!! cost identity failed - aborting."); sys.exit(1)
                checked = True
            gross_realised = float(res["weights"].sum(axis=1).loc[start:].mean())
            years = len(r0.loc[start:]) / 252
            to_yr = float(turn.loc[start:].sum() / years)
            for c in RUNGS:
                r = (r0 - turn * c / 1e4).loc[start:]
                m = metrics(r)
                mo = metrics(r.loc[OOS_START:])
                h1, h2 = half_sharpes(r)
                key = (pname, aname, c)
                series[key] = r
                rows.append(dict(panel=pname, arm=aname, cost=c, family=spec["key"], freq=spec["freq"],
                                 n=spec.get("n"), CAGR=m["CAGR"], Sharpe=m["Sharpe"], Vol=m["Vol"],
                                 MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                 IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                 TO=to_yr, gross=gross_realised,
                                 p4a=pass4a(r, base), f4b=fail4b(r, spy),
                                 p4b=(fail4b(r, spy) == "-")))
        series[(pname, "__SPY__", PUB_RUNG)] = spy
        series[(pname, "__BASE__", PUB_RUNG)] = base

    return pd.DataFrame(rows), series, panels


def tier_L_pairs(L):
    """Every pre-registered pair, at every rung, with its 0-bps twin and cost share."""
    idx = L.set_index(["panel", "arm", "cost"])
    out = []
    for label, a, b, fam in pair_list():
        for pname in L["panel"].unique():
            try:
                ra = {c: idx.loc[(pname, a, c)] for c in RUNGS}
                rb = {c: idx.loc[(pname, b, c)] for c in RUNGS}
            except KeyError:
                continue
            d = {c: dict(Sharpe=ra[c]["Sharpe"] - rb[c]["Sharpe"],
                         CAGR=ra[c]["CAGR"] - rb[c]["CAGR"]) for c in RUNGS}
            dTO = float(ra[0]["TO"] - rb[0]["TO"])
            row = dict(panel=pname, pair=label, family=fam,
                       TO_a=float(ra[0]["TO"]), TO_b=float(rb[0]["TO"]), dTO=dTO,
                       TO_ratio=float(max(ra[0]["TO"], rb[0]["TO"]) / max(min(ra[0]["TO"], rb[0]["TO"]), 1e-9)),
                       gross_a=float(ra[0]["gross"]), gross_b=float(rb[0]["gross"]),
                       gross_gap=float(abs(ra[0]["gross"] - rb[0]["gross"])),
                       gross_matched=bool(abs(ra[0]["gross"] - rb[0]["gross"]) < GROSS_TOL))
            for c in RUNGS:
                row[f"dSharpe@{c}"] = d[c]["Sharpe"]
                row[f"dCAGR@{c}"] = d[c]["CAGR"]
            row["share_S"] = cost_share(d[0]["Sharpe"], d[PUB_RUNG]["Sharpe"])
            row["share_C"] = cost_share(d[0]["CAGR"], d[PUB_RUNG]["CAGR"])
            row["maj_S"] = bool(np.isfinite(row["share_S"]) and row["share_S"] > MAJ)
            row["maj_C"] = bool(np.isfinite(row["share_C"]) and row["share_C"] > MAJ)
            row["flip_S"] = bool(np.sign(d[0]["Sharpe"]) != np.sign(d[PUB_RUNG]["Sharpe"]))
            row["flip_C"] = bool(np.sign(d[0]["CAGR"]) != np.sign(d[PUB_RUNG]["CAGR"]))
            row["be_bps_S"] = breakeven_bps(d[0]["Sharpe"], d[PUB_RUNG]["Sharpe"], PUB_RUNG)
            row["tiny_S"] = bool(abs(d[PUB_RUNG]["Sharpe"]) < TINY_S)
            out.append(row)
    return pd.DataFrame(out)


# ================================================================== TIER V
def tier_V(L):
    """Validate the turnover back-fill estimator against tier L's exact 0-bps truth."""
    idx = L.set_index(["panel", "arm", "cost"])
    rows = []
    for (pname, aname, c), r in idx.iterrows():
        if c == 0:
            continue
        truth = idx.loc[(pname, aname, 0)]
        est_S = r["Sharpe"] + (c / 1e4) * r["TO"] / r["Vol"]
        est_C = r["CAGR"] + (c / 1e4) * r["TO"]
        rows.append(dict(panel=pname, arm=aname, cost=c, TO=r["TO"],
                         true_S0=truth["Sharpe"], est_S0=est_S, err_S=est_S - truth["Sharpe"],
                         true_C0=truth["CAGR"], est_C0=est_C, err_C=est_C - truth["CAGR"]))
    return pd.DataFrame(rows)


# ================================================================== TIER R
DIAL_LIKE = {"arm", "book", "kind", "signal", "conv", "key", "instr", "instrument", "sleeve",
             "selector", "mode", "variant", "leg", "band", "gate", "n", "g", "m", "f", "p",
             "max_vol", "freq", "cadence", "d", "k", "q", "w", "width", "stop", "tilt", "seed",
             "fund", "cap", "reset", "panel", "universe", "uni"}
COST_COLS = {"cost", "cost_bps", "bps", "rung", "costbps"}
TO_COLS = {"to", "turn", "turnover", "turn_yr", "to_yr", "turnover_yr"}
METRIC_COLS = {"cagr", "sharpe", "maxdd", "vol", "h1", "h2", "sortino", "calmar", "total",
               "is_sharpe", "is_maxdd", "is_cagr", "oos_cagr", "oos_sharpe", "oos_maxdd",
               "m_h1", "m_h2", "m_oos", "m_dd", "m_cagr", "p4a", "p4b", "f4b", "pass4a",
               "pass4b", "fail4a", "fail4b", "4a", "4b", "pass4b_oos", "gross", "point",
               "years", "winrate", "flips", "sat_share", "episodes", "cut_days"}


def _norm(df):
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    return df.loc[:, ~df.columns.duplicated()]


def tier_R(err_S_band, err_C_band):
    files = sorted(glob.glob(str(OUT / "*.grid.csv")))
    fstats, pairs = [], []
    for f in files:
        try:
            df = _norm(pd.read_csv(f))
        except Exception as e:
            fstats.append(dict(file=Path(f).name, status=f"unreadable:{type(e).__name__}",
                               rungs=0, pairs=0)); continue
        ccol = next((c for c in df.columns if c in COST_COLS), None)
        tcol = next((c for c in df.columns if c in TO_COLS), None)
        rungs = sorted(pd.to_numeric(df[ccol], errors="coerce").dropna().unique()) if ccol else []
        has_g = "gross" in df.columns
        metr = [c for c in ("sharpe", "cagr") if c in df.columns]
        if not metr:
            fstats.append(dict(file=Path(f).name, status="no-metric", rungs=len(rungs), pairs=0)); continue

        # dial columns = everything that is not a metric, not the cost column, not turnover
        dials = [c for c in df.columns
                 if c not in METRIC_COLS and c != ccol and c != tcol and df[c].nunique() > 1]
        if not dials:
            fstats.append(dict(file=Path(f).name, status="no-dial", rungs=len(rungs), pairs=0)); continue

        # published rung = the single rung, or PROTOCOL's 10 if present, else the max
        if len(rungs) >= 2:
            pub = PUB_RUNG if PUB_RUNG in rungs else rungs[-1]
            lo, hi = rungs[0], next((r for r in rungs if r > rungs[0]), rungs[-1])
            mode = "multi"
        else:
            pub = rungs[0] if rungs else PUB_RUNG
            mode = "single"

        sub = df if not ccol else df[pd.to_numeric(df[ccol], errors="coerce") == pub]
        if len(sub) < 2:
            fstats.append(dict(file=Path(f).name, status="thin", rungs=len(rungs), pairs=0)); continue

        npairs = 0
        for dcol in dials:
            others = [c for c in dials if c != dcol]
            if not others:
                grp = [((), sub)]
            else:
                grp = list(sub.fillna("~NA~").groupby(others, dropna=False))
            for _, g in grp:
                if len(g) < 2 or len(g) > 40:
                    continue
                g = g.reset_index(drop=True)
                for i in range(len(g)):
                    for j in range(i + 1, len(g)):
                        a, b = g.loc[i], g.loc[j]
                        if has_g and pd.notna(a.get("gross")) and pd.notna(b.get("gross")):
                            try:
                                if abs(float(a["gross"]) - float(b["gross"])) > 1e-6:
                                    continue                       # NOT gross-matched
                            except (TypeError, ValueError):
                                pass
                        for met in metr:
                            try:
                                dc = float(a[met]) - float(b[met])
                            except (TypeError, ValueError):
                                continue
                            if not np.isfinite(dc) or dc == 0:
                                continue
                            d0 = np.nan
                            how = ""
                            if mode == "multi":                     # exact: extrapolate through 2 rungs
                                key = [c for c in dials]
                                ma = df[(df[ccol] == lo)]
                                mb = df[(df[ccol] == hi)]
                                try:
                                    al = ma.merge(a[key].to_frame().T, on=key)
                                    bl = ma.merge(b[key].to_frame().T, on=key)
                                    ah = mb.merge(a[key].to_frame().T, on=key)
                                    bh = mb.merge(b[key].to_frame().T, on=key)
                                    if len(al) == 1 and len(bl) == 1 and len(ah) == 1 and len(bh) == 1:
                                        dlo = float(al[met].iloc[0]) - float(bl[met].iloc[0])
                                        dhi = float(ah[met].iloc[0]) - float(bh[met].iloc[0])
                                        slope = (dhi - dlo) / (hi - lo)
                                        d0 = dlo - slope * lo
                                        how = "exact"
                                except Exception:
                                    pass
                            if not np.isfinite(d0) and tcol is not None:
                                try:
                                    dto = float(a[tcol]) - float(b[tcol])
                                except (TypeError, ValueError):
                                    continue
                                if not np.isfinite(dto):
                                    continue
                                if met == "cagr":
                                    d0 = dc + (pub / 1e4) * dto
                                else:
                                    v = float(a["vol"]) if "vol" in df.columns and pd.notna(a.get("vol")) else np.nan
                                    if not np.isfinite(v) or v <= 0:
                                        continue
                                    d0 = dc + (pub / 1e4) * dto / v
                                how = "estimated"
                            if not np.isfinite(d0):
                                continue
                            sh = cost_share(d0, dc)
                            band = err_C_band if met == "cagr" else err_S_band
                            pairs.append(dict(file=Path(f).name, dial=dcol, metric=met, rung=pub,
                                              mode=mode, how=how, d0=d0, dc=dc, share=sh,
                                              maj=bool(np.isfinite(sh) and sh > MAJ),
                                              flip=bool(np.sign(d0) != np.sign(dc)),
                                              uncertain=bool(2 * band > abs(dc))))
                            npairs += 1
        fstats.append(dict(file=Path(f).name, status="ok", rungs=len(rungs), pairs=npairs,
                           mode=mode, has_TO=tcol is not None, has_gross=has_g))
    return pd.DataFrame(fstats), pd.DataFrame(pairs)


# ================================================================== rule 8
def rule8(L, series):
    rows = []
    for pname in L["panel"].unique():
        spy = series[(pname, "__SPY__", PUB_RUNG)]
        base = series[(pname, "__BASE__", PUB_RUNG)]
        sub = L[L["panel"] == pname]
        picks = {}
        for score_rung in (0, PUB_RUNG):
            s = sub[sub["cost"] == score_rung].set_index("arm")["IS_Sharpe"]
            picks[f"PICK@{score_rung}"] = s.idxmax()
        sel = {"ANCHOR": "FWD20", "EWALL": "EWall", **picks}
        for lab, arm in sel.items():
            r = series[(pname, arm, PUB_RUNG)]        # every selector is TRADED at PROTOCOL's 10 bps
            ro = r.loc[OOS_START:]
            m, mo = metrics(r), metrics(ro)
            rows.append(dict(panel=pname, selector=lab, arm=arm, OOS_CAGR=mo["CAGR"],
                             OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             p4a=pass4a(r, base), f4b=fail4b(r, spy)))
        for lab, r in (("RULES v1", base), ("SPY", spy)):
            ro = r.loc[OOS_START:]
            mo, m = metrics(ro), metrics(r)
            rows.append(dict(panel=pname, selector=lab, arm="-", OOS_CAGR=mo["CAGR"],
                             OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                             CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                             p4a=np.nan, f4b="-"))
    return pd.DataFrame(rows)


# ================================================================== main
def main():
    L, series, _ = run_tier_L()
    L.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\n[tier L] {len(L)} points written to {STEM}.grid.csv "
          f"({L['arm'].nunique()} arms x {L['panel'].nunique()} panels x {len(RUNGS)} rungs)")

    print("\n--- TIER L: every arm at every rung (all points reported) " + "-" * 110)
    show = L[["panel", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe", "TO", "gross", "p4a", "p4b", "f4b"]]
    print(fmt(show.set_index(["panel", "arm", "cost"]), 3))

    print("\n[gross-matching check] realised mean gross by panel (must be flat for a gross-matched read):")
    print(fmt(L[L.cost == 0].groupby("panel")["gross"].agg(["min", "max", "mean"]), 4))

    P = tier_L_pairs(L)
    P.to_csv(OUT / f"{STEM}.pairs.csv", index=False)
    print("\n--- TIER L: gross-matched one-dial arm differences, published rung vs 0-bps twin " + "-" * 40)
    cols = ["panel", "pair", "family", f"dSharpe@{PUB_RUNG}", "dSharpe@0", "share_S", "maj_S",
            "flip_S", "tiny_S", f"dCAGR@{PUB_RUNG}", "dCAGR@0", "share_C", "maj_C", "dTO",
            "TO_ratio", "be_bps_S"]
    print(fmt(P[cols].set_index(["panel", "pair"]), 4))

    print("\n[headline] majority-cost rate among live gross-matched arm differences:")
    hl = pd.DataFrame({
        "n": P.groupby("family").size(),
        "maj_Sharpe": P.groupby("family")["maj_S"].sum(),
        "maj_CAGR": P.groupby("family")["maj_C"].sum(),
        "flip_Sharpe": P.groupby("family")["flip_S"].sum(),
        "flip_CAGR": P.groupby("family")["flip_C"].sum(),
        "median_share_S": P.groupby("family")["share_S"].median(),
        "median_TO_ratio": P.groupby("family")["TO_ratio"].median()})
    print(fmt(hl, 3))
    print(f"\nTOTAL live pairs {len(P)}: majority-cost on Sharpe {P['maj_S'].sum()} "
          f"({P['maj_S'].mean():.1%}), on CAGR {P['maj_C'].sum()} ({P['maj_C'].mean():.1%}); "
          f"SIGN FLIPS Sharpe {P['flip_S'].sum()}, CAGR {P['flip_C'].sum()}")
    print(f"  gross matching: every arm is targeted at {GROSS}; realised mean gross drifts between "
          f"rebalances, max |gap| across a pair {P['gross_gap'].max():.4f}, all {len(P)} pairs within "
          f"the stated {GROSS_TOL} tolerance: {bool(P['gross_matched'].all())}")
    big = P[~P["tiny_S"]]
    print(f"  excluding pairs whose published |dSharpe| < {TINY_S} (too small to be a claim; "
          f"{int(P['tiny_S'].sum())} of {len(P)}): majority-cost {big['maj_S'].sum()}/{len(big)} "
          f"({big['maj_S'].mean():.1%}), sign flips {big['flip_S'].sum()}")
    hi = P[P["TO_ratio"] >= 2.0]
    lo = P[P["TO_ratio"] < 2.0]
    print(f"  turnover ratio >= 2x  : n={len(hi):3d}  majority-cost {hi['maj_S'].mean() if len(hi) else float('nan'):.1%} (Sharpe)")
    print(f"  turnover ratio <  2x  : n={len(lo):3d}  majority-cost {lo['maj_S'].mean() if len(lo) else float('nan'):.1%} (Sharpe)")

    V = tier_V(L)
    V.to_csv(OUT / f"{STEM}.estval.csv", index=False)
    print("\n--- TIER V: turnover back-fill estimator vs exact 0-bps truth " + "-" * 85)
    print(fmt(V.groupby("cost")[["err_S", "err_C"]].agg(["mean", "std", lambda x: x.abs().max()]), 5))
    band_S = float(V.loc[V.cost == PUB_RUNG, "err_S"].abs().quantile(0.95))
    band_C = float(V.loc[V.cost == PUB_RUNG, "err_C"].abs().quantile(0.95))
    print(f"  95th-pct |error| at {PUB_RUNG} bps: Sharpe {band_S:.5f}, CAGR {band_C:.5f} "
          f"-> tier-R rows whose |D(c)| < 2x that band are flagged `uncertain`.")

    F, R = tier_R(band_S, band_C)
    F.to_csv(OUT / f"{STEM}.record_files.csv", index=False)
    R.to_csv(OUT / f"{STEM}.record_pairs.csv", index=False)
    print("\n--- TIER R: the committed record " + "-" * 115)
    print(f"grid CSVs scanned: {len(F)}")
    print(fmt(F.groupby("status").size().to_frame("files"), 0))
    okf = F[F.status == "ok"]
    print(f"  of the {len(okf)} usable grids: {int((okf['rungs'] <= 1).sum())} carry ONE cost rung or none, "
          f"{int((okf['rungs'] >= 2).sum())} carry two or more "
          f"({(okf['rungs'] <= 1).mean():.1%} single-rung)  <- the queue's premise")
    print(f"  carry a turnover column: {int(okf['has_TO'].sum())}/{len(okf)}; "
          f"a gross column: {int(okf['has_gross'].sum())}/{len(okf)}")
    if len(R):
        print(f"\ngross-matched one-dial arm differences recoverable from the record: {len(R)}")
        agg = R.groupby(["how", "metric"]).agg(n=("maj", "size"), majority_cost=("maj", "sum"),
                                               rate=("maj", "mean"), sign_flips=("flip", "sum"),
                                               uncertain=("uncertain", "sum"),
                                               median_share=("share", "median"))
        print(fmt(agg, 3))
        cl = R[~R["uncertain"]]
        print(f"\nexcluding rows inside the estimator's error band ({len(cl)} of {len(R)}): "
              f"majority-cost {cl['maj'].sum()} ({cl['maj'].mean():.1%}), sign flips {cl['flip'].sum()} "
              f"({cl['flip'].mean():.1%})")
        ex = R[R["how"] == "exact"]
        if len(ex):
            cle = ex[~ex["uncertain"]]
            print(f"EXACT tier only (multi-rung grids, no estimator, {len(cle)} clean pairs): "
                  f"majority-cost {cle['maj'].sum()} ({cle['maj'].mean() if len(cle) else float('nan'):.1%}), "
                  f"sign flips {cle['flip'].sum()}")
        print("\ntop 15 files by recoverable pairs:")
        print(fmt(R.groupby("file").agg(n=("maj", "size"), maj=("maj", "sum"), rate=("maj", "mean"))
                  .sort_values("n", ascending=False).head(15), 3))

    W = rule8(L, series)
    W.to_csv(OUT / f"{STEM}.rule8.csv", index=False)
    print("\n--- PROTOCOL rule 8 walk-forward (IS <= 2016-12-31 chooses, OOS >= 2017 evaluates) " + "-" * 40)
    print("every selector is TRADED at 10 bps; the two PICK rows differ only in the rung they SCORE on.")
    print(fmt(W.set_index(["panel", "selector"]), 3))
    piv = W[W.selector.isin(["ANCHOR", "EWALL", "PICK@0", f"PICK@{PUB_RUNG}", "RULES v1", "SPY"])]
    print("\nOOS Sharpe by selector, mean over panels:")
    print(fmt(piv.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean(), 3))
    p0 = W[W.selector == "PICK@0"].set_index("panel")
    pc = W[W.selector == f"PICK@{PUB_RUNG}"].set_index("panel")
    diff = (p0["OOS_Sharpe"] - pc["OOS_Sharpe"])
    print(f"\nrung-of-scoring cost: PICK@0 - PICK@{PUB_RUNG} OOS Sharpe = "
          f"{diff.mean():+.4f} mean, per panel {dict(diff.round(4))}; "
          f"arms picked differ in {int((p0['arm'] != pc['arm']).sum())}/{len(p0)} panels "
          f"({dict(zip(p0.index, zip(p0['arm'], pc['arm'])))})")

    print("\n--- KEEP paths (both, every arm x rung) " + "-" * 110)
    print(fmt(L.groupby(["panel", "cost"])[["p4a", "p4b"]].sum().join(
        L.groupby(["panel", "cost"]).size().to_frame("n")), 0))
    if L["p4b"].any():
        print("\n4b passes:")
        print(fmt(L[L.p4b][["panel", "arm", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                            "OOS_Sharpe", "TO"]].set_index(["panel", "arm", "cost"]), 3))
    else:
        print("\n4b passes: NONE.")

    print("\n" + "=" * 200)
    print("SURVIVORSHIP: all three panels are current constituents (one-directional). The headline "
          "statistic is a ratio of a difference to a difference, in which a common additive premium "
          "largely cancels; the 4a/4b counts are optimistic and should be read as upper bounds.")
    print("=" * 200)


if __name__ == "__main__":
    main()
