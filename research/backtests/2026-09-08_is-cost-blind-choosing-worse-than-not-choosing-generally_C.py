#!/usr/bin/env python3
"""Idea 455 — is-cost-blind-choosing-worse-than-not-choosing-generally  (lane C, 2026-09-08).

PRE-REGISTERED QUESTION (QUEUE 455): idea 231's rule-8 has the naive 0-bps chooser at -0.0237
OOS Sharpe against do-nothing while the rung-aware chooser is +0.0177, i.e. the ladder's whole
value looks like avoiding the COST-BLIND pick rather than beating the default.  Re-read the
record's "selection loses" instances splitting chooser-minus-default into a cost-blind and a
cost-aware half.

THE HYPOTHESIS, stated so it can fail.  Write, for a swept dial read at cost rung c:
    L_aware(c) = OOS(argmax_d IS_Sharpe(d, c))      - OOS(default)
    L_blind(c) = OOS(argmax_d IS_Sharpe(d, c_lo=0)) - OOS(default)
    DELTA(c)   = L_aware(c) - L_blind(c)            "what costing the choice is worth"
Idea 231's sentence generalises iff, across the record: (H1) L_blind < 0, (H2) L_aware > 0, and
(H3) DELTA > 0, at PROTOCOL's own 10 bps and not only at the high rungs.
THE FALSIFIER, and the reason this is worth running: DELTA(c) is IDENTICALLY ZERO whenever the
rung does not move the argmax, and idea 228 measured that the argmax moves in only 3 of 12
cells and NEVER above 10 bps.  So H3 can only be carried by a small re-ranking minority, and
the honest decomposition is  E[DELTA] = P(pick moves) x E[DELTA | pick moves].  If the moving
minority is small and its conditional gain is noise, "cost-blind choosing is worse than not
choosing" is a statement about a handful of cells, not about choosing.
A SECOND, mechanical caveat this script prices: DELTA >= 0 IS AN IDENTITY IN SAMPLE (the aware
pick maximises IS Sharpe at c by construction), so only the OOS TRANSFER RATE of that
entitlement is evidence.  Both are reported side by side.

TWO TUNED PARAMETERS ONLY:
    p1 = COMPARAND, i.e. what "not choosing" means  {MEDIAN arm, RANDOM (mean over arms),
         DEFAULT (the live RULES value, Part B only)}  — all parameter-free readings of the
         same swept grid; no arm is hand-picked.  ALL LEVELS REPORTED.
    p2 = RUNG the claim is read at  {0, 5, 10, 15, 20, 25, 30 bps}.  ALL GRID POINTS REPORTED.
Nothing else is tuned.  ORACLE (the OOS argmax) is printed as a ceiling, never as a comparand.

CORRECTION TO IDEA 235's ARCHIVE READING, carried here: idea 235 defined the cost-blind pick as
the argmax at the ladder's LOWEST rung, which is 0 bps for some committed ladders and 10 or 25
bps for others.  Where the lowest rung is not 0 the "cost-blind" reading is not cost-blind at
all and DELTA is mechanically attenuated.  Every archive number below is reported twice: over
all ladders, and over the ZERO-ANCHORED subcorpus (ladders that actually commit a 0-bps rung).

PART A (the record): every committed CSV carrying a cost rung + IS_Sharpe + OOS_Sharpe is
re-read as a selection claim, at every rung, under both comparands, split into the blind and
aware halves.  The record's "selection loses" instances (cells where L_aware < 0) are then
classified by whether cost-blindness is what loses them.
PART B (live, PROTOCOL rule 8): 3 panels x 6 dials x 7 rungs re-simulated from prices, IS =
2009-2016, OOS = 2017-2026 read once.  The 4 dials of idea 235 are re-run unchanged as an
exact reproduction gate against its committed walkforward.csv; 2 further dials (MA length,
gross) widen the live corpus from 12 to 18 cells.  OOS CAGR/Sharpe/MaxDD are reported against
RULES v1, RULES v2 and SPY, and both KEEP paths (4a and 4b) are evaluated at every grid point.

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen only (see
data/SMALL_PANEL_README.md); the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (483 -> SMALL439).  Small-panel numbers are upper bounds.

Outputs (all committed):
    .census.csv.gz     every archive (file, dial, cell, rung): aware/blind picks and margins
    .rungcurve.csv     L_aware, L_blind, DELTA vs rung, by comparand/weighting/source
    .instances.csv     the record's "selection loses" instances, classified
    .grid.csv          Part B: every (panel, dial, value, rung) point with 4a/4b bars
    .walkforward.csv   Part B rule 8: aware pick, blind pick, comparands, OOS read once
    .keeppaths.csv     4a/4b pass counts per (panel, dial, rung)
"""
import math
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import metrics                                                     # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF = Path(__file__).name
STEM = SELF.replace(".py", "")
RNG = np.random.default_rng(20260908)

# idea 235's committed live walk-forward, used as an exact reproduction gate
REF235 = BT / "2026-09-08_is-selection-beats-do-nothing-just-a-rung-artefact_cloud.walkforward.csv"

COST_NAMES = {"bps", "cost_bps", "cost", "rung", "cost_rung", "bps_rung", "c_bps"}
TURN_NAMES = {"turnover", "to", "turn", "turn_yr", "turnover_yr", "turn_per_yr", "TO_yr"}
METRIC_SUBSTR = ("sharpe", "cagr", "maxdd", "dd", "vol", "turn", "gross", "pass", "fail",
                 "p4a", "p4b", "f4b", "m_", "oos", "_is", "is_", "h1", "h2", "ret", "equity",
                 "pval", "p_", "_p", "z", "ci", "sd", "std", "mean", "median", "hit", "win",
                 "margin", "regret", "room", "excess", "premium", "delta", "d_", "rho", "corr",
                 "n_", "count", "seed", "invested", "held", "episodes", "days", "bind", "y20",
                 "sortino", "calmar", "alpha", "beta", "te", "ir", "skew", "kurt", "auc")


# ------------------------------------------------------------------ small helpers
def is_metric(col):
    c = str(col).lower()
    return any(s in c for s in METRIC_SUBSTR)


def named(cols, names):
    for c in cols:
        if str(c).strip().lower() in names:
            return c
    return None


def exact(cols, name):
    for c in cols:
        if str(c).strip().lower() == name:
            return c
    return None


def sign_test(x):
    """Exact two-sided binomial sign test.  Returns (win rate, p, n non-zero)."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x) & (x != 0)]
    n = len(x)
    if n < 3:
        return np.nan, np.nan, n
    k = int((x > 0).sum())
    tail = sum(math.comb(n, i) for i in range(0, min(k, n - k) + 1)) / 2 ** n
    return k / n, float(min(1.0, 2 * tail)), n


def boot_ci(x, clusters=None, B=2000):
    """Bootstrap mean CI, clustered on `clusters` (e.g. the source file) when given."""
    x = np.asarray(x, float)
    ok = np.isfinite(x)
    x = x[ok]
    if len(x) < 5:
        return np.nan, np.nan
    if clusters is None:
        idx = RNG.integers(0, len(x), size=(B, len(x)))
        m = x[idx].mean(axis=1)
    else:
        cl = np.asarray(clusters)[ok]
        groups = [x[cl == g] for g in pd.unique(cl)]
        m = np.empty(B)
        for b in range(B):
            pick = RNG.integers(0, len(groups), size=len(groups))
            m[b] = np.concatenate([groups[i] for i in pick]).mean()
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3 or np.ptp(x[m]) == 0:
        return np.nan, np.nan
    b, a = np.polyfit(x[m], y[m], 1)
    yhat = a + b * x[m]
    ss = ((y[m] - y[m].mean()) ** 2).sum()
    return float(b), float(1 - ((y[m] - yhat) ** 2).sum() / ss) if ss > 0 else np.nan


# ------------------------------------------------------------------ Part A: the archive
def read_cell(piv_is, piv_oos):
    """One (dial values) x (cost rungs) rectangle, split into blind and aware halves.

    aware(c) = argmax_d IS_Sharpe(d, c)       chosen in sample AT the rung it will be paid at
    blind    = argmax_d IS_Sharpe(d, c_lo)    chosen at the ladder's lowest rung, paid at c
    MEDIAN   = the middle arm of the swept grid            "do nothing", parameter-free
    RANDOM   = mean OOS over all arms                      "any arm at all"
    ORACLE   = max OOS over arms                           ceiling, not a comparand
    """
    vals = list(piv_is.index)
    rungs = sorted(piv_is.columns)
    med = vals[len(vals) // 2]
    c_lo = rungs[0]
    blind = piv_is[c_lo].idxmax()
    out = []
    for c in rungs:
        aware = piv_is[c].idxmax()
        o, i = piv_oos[c], piv_is[c]
        out.append(dict(
            bps=float(c), c_lo=float(c_lo), zero_anchored=bool(float(c_lo) == 0.0),
            n_values=len(vals), aware=aware, blind=blind, median_arm=med,
            moved=bool(aware != blind),
            OOS_aware=float(o[aware]), OOS_blind=float(o[blind]),
            OOS_MEDIAN=float(o[med]), OOS_RANDOM=float(o.mean()), OOS_ORACLE=float(o.max()),
            IS_aware=float(i[aware]), IS_blind=float(i[blind]),
            L_aware_MEDIAN=float(o[aware] - o[med]), L_blind_MEDIAN=float(o[blind] - o[med]),
            L_aware_RANDOM=float(o[aware] - o.mean()), L_blind_RANDOM=float(o[blind] - o.mean()),
            DELTA=float(o[aware] - o[blind]), DELTA_IS=float(i[aware] - i[blind])))
    return out


def scan_archive():
    """Dial/cell detection is idea 231/235's, unchanged: numeric id column with 3..60 values,
    grouping columns bijective with the dial dropped, complete rectangle required."""
    rows, seen, t0, files_used = [], 0, time.time(), set()
    for f in sorted(BT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        seen += 1
        if seen % 400 == 0:
            print(f"    ...{seen} files, {len(rows)} rung-readings, {time.time()-t0:.0f}s", flush=True)
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        if len(df) < 6:
            continue
        ccol = named(df.columns, COST_NAMES)
        icol, ocol = exact(df.columns, "is_sharpe"), exact(df.columns, "oos_sharpe")
        tcol = named(df.columns, TURN_NAMES)
        if ccol is None or icol is None or ocol is None:
            continue
        for c in (ccol, icol, ocol):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df[df[ccol].notna() & df[icol].notna() & df[ocol].notna()].copy()
        if len(df) < 6 or df[ccol].nunique() < 2:
            continue
        used = {ccol, icol, ocol, tcol}
        ids = [c for c in df.columns if c not in used and not is_metric(c) and df[c].nunique() > 1]
        dials = [c for c in ids if pd.api.types.is_numeric_dtype(df[c]) and 3 <= df[c].nunique() <= 60]
        vals = [icol, ocol]
        for d in dials:
            nd = df[d].nunique()
            grp = [g for g in ids if g != d]
            grp = [g for g in grp if not (df[g].nunique() == nd and df.groupby(d)[g].nunique().max() == 1
                                          and df.groupby(g)[d].nunique().max() == 1)]
            grp = [g for g in grp if df[g].nunique() <= 200]
            agg = df.groupby(grp + [d, ccol], dropna=False, sort=False)[vals].median().reset_index()
            if grp:
                keys = agg[grp[0]].astype(str)
                for g in grp[1:]:
                    keys = keys + "|" + agg[g].astype(str)
            else:
                keys = pd.Series("_", index=agg.index)
            agg["_k"] = keys.values
            sz = agg.groupby("_k", sort=False).size()
            big = sz[sz >= 6].index
            if not len(big):
                continue
            for k, sub in agg[agg._k.isin(big)].groupby("_k", sort=False):
                nv, nc = sub[d].nunique(), sub[ccol].nunique()
                if nv < 3 or nc < 2 or len(sub) != nv * nc:
                    continue
                pi = sub.pivot(index=d, columns=ccol, values=icol)
                po = sub.pivot(index=d, columns=ccol, values=ocol)
                if pi.isna().any().any() or po.isna().any().any():
                    continue
                if po.nunique().max() < 2:            # OOS identical across arms: no claim
                    continue
                files_used.add(f.name)
                for r in read_cell(pi, po):
                    rows.append(dict(file=f.name, dial=d, cell=str(k)[:80], **r))
    C = pd.DataFrame(rows)
    print(f"    scan done: {seen} files scanned, {len(files_used)} usable, "
          f"{len(C)} rung-readings, {time.time()-t0:.0f}s", flush=True)
    return C


# ------------------------------------------------------------------ Part B: live
RUNGS = [0, 5, 10, 15, 20, 25, 30]
OOS_START = "2017-01-01"
IS_END = "2016-12-31"
# idea 235's 4 dials, unchanged (reproduction gate), plus 2 new ones (L = trend lookback,
# W = gross scalar).  DEFAULTS are the live RULES values and are the "do-nothing" arm.
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1, L=200, W=1.00)
DIAL_VALUES = {"N": [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
               "G": [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
               "V": [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
               "K": [1, 2, 3, 4, 6, 8, 13],
               "L": [50, 100, 150, 200, 250, 300],
               "W": [0.25, 0.50, 0.75, 1.00, 1.25]}
REF_DIALS = ("N", "G", "V", "K")


def load_small439():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    print(f"  SMALL: dropped {px.shape[1]-len(keep)} of {px.shape[1]-1} names "
          f"(max_1d_move >= 1.0) -> {len(keep)-1} constituents", flush=True)
    return px[keep]


def week_mask(idx, k):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    last = (s != s.shift(-1)).values
    if k == 1:
        return last
    ordinal = pd.Series(pd.factorize(per)[0], index=idx).values
    return last & ((ordinal % k) == 0)


def simulate(px, W, mask):
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1]); held = np.empty_like(rets); turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1), index=px.index),
            pd.Series(turn, index=px.index))


def book_weights(px, comp, ma, vol20, n, g, max_vol, gross=1.0):
    if g == 0:
        above = px > ma
    else:
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0, np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    elig = comp.where(above & (vol20 < max_vol))
    return (elig.rank(axis=1, ascending=False) <= n).astype(float) * (gross / n)


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]: f.append("H1")
    if not s["H2"] > b["H2"]: f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]: f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]: f.append("H1")
    if not s["H2"] > spy["H2"]: f.append("H2")
    if not oos_s > oos_spy: f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]: f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: f.append("CAGR")
    return ",".join(f)


def part_b():
    t0 = time.time()
    grid = []
    for pname, px in (("U56", load_universe()), ("B136", load_universe(broad=True)),
                      ("SMALL439", load_small439())):
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))
        mas = {L: px.rolling(L).mean() for L in DIAL_VALUES["L"]}
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r); spy_o = metrics(spy_r.loc[OOS_START:])
        bg, bt = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base = {c: stats(net(bg, bt, c).loc[start:]) for c in RUNGS}
        base_oos = {c: metrics(net(bg, bt, c).loc[OOS_START:]) for c in RUNGS}
        vg, vt = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        v2_oos = {c: metrics(net(vg, vt, c).loc[OOS_START:]) for c in RUNGS}
        for dial, values in DIAL_VALUES.items():
            for v in values:
                kw = dict(DEFAULTS); kw[dial] = v
                if dial == "N" and v > px.shape[1] - 1:
                    continue
                W = book_weights(px, comp, mas[kw["L"]], vol20, kw["N"], kw["G"], kw["V"], kw["W"])
                g_, t_ = simulate(px, W, week_mask(px.index, kw["K"]))
                g_, t_ = g_.loc[start:], t_.loc[start:]
                yrs = len(g_) / 252
                yrs_oos = len(g_.loc[OOS_START:]) / 252
                for c in RUNGS:
                    r = net(g_, t_, c); st = stats(r); o = metrics(r.loc[OOS_START:])
                    ir = r.loc[:IS_END]
                    grid.append(dict(panel=pname, dial=dial, value=v, bps=c,
                                     turn_yr=t_.sum() / yrs,
                                     turn_yr_oos=t_.loc[OOS_START:].sum() / yrs_oos,
                                     OOS_vol=r.loc[OOS_START:].std() * np.sqrt(252), **st,
                                     IS_Sharpe=metrics(ir)["Sharpe"],
                                     OOS_Sharpe=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"],
                                     fail4a=bars_4a(st, base[c]),
                                     fail4b=bars_4b(st, spy_s, o["Sharpe"], spy_o["Sharpe"]),
                                     spy_Sharpe=spy_s["Sharpe"], spy_CAGR=spy_s["CAGR"],
                                     spy_MaxDD=spy_s["MaxDD"],
                                     spy_OOS_Sharpe=spy_o["Sharpe"], spy_OOS_CAGR=spy_o["CAGR"],
                                     spy_OOS_MaxDD=spy_o["MaxDD"],
                                     v1_OOS_Sharpe=base_oos[c]["Sharpe"],
                                     v1_OOS_CAGR=base_oos[c]["CAGR"],
                                     v1_OOS_MaxDD=base_oos[c]["MaxDD"],
                                     v2_OOS_Sharpe=v2_oos[c]["Sharpe"],
                                     v2_OOS_CAGR=v2_oos[c]["CAGR"],
                                     v2_OOS_MaxDD=v2_oos[c]["MaxDD"]))
        print(f"  {pname}: {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(grid)


def walk_forward(G):
    """PROTOCOL rule 8.  Pick on 2009-2016 IS Sharpe; 2017-2026 read once.
    aware = argmax IS_Sharpe at the rung being paid; blind = argmax IS_Sharpe at 0 bps.
    DEFAULT = the live RULES arm, MEDIAN = middle swept arm, RANDOM = mean over arms."""
    wf = []
    for (p_, d_), sub in G.groupby(["panel", "dial"]):
        vals = sorted(sub.value.unique())
        med, dn = vals[len(vals) // 2], DEFAULTS[d_]
        pi = sub.pivot_table(index="value", columns="bps", values="IS_Sharpe")
        blind = pi[min(pi.columns)].idxmax()
        for c in RUNGS:
            o = sub[sub.bps == c].set_index("value")
            aware = pi[c].idxmax()
            row = dict(panel=p_, dial=d_, bps=c, aware=aware, blind=blind, median_arm=med,
                       do_nothing=dn, moved=bool(aware != blind),
                       OOS_aware=float(o.OOS_Sharpe[aware]), OOS_blind=float(o.OOS_Sharpe[blind]),
                       OOS_DEFAULT=float(o.OOS_Sharpe[dn]), OOS_MEDIAN=float(o.OOS_Sharpe[med]),
                       OOS_RANDOM=float(o.OOS_Sharpe.loc[vals].mean()),
                       OOS_ORACLE=float(o.OOS_Sharpe.max()),
                       IS_aware=float(pi[c][aware]), IS_blind=float(pi[c][blind]),
                       CAGR_aware=float(o.OOS_CAGR[aware]), CAGR_blind=float(o.OOS_CAGR[blind]),
                       CAGR_DEFAULT=float(o.OOS_CAGR[dn]),
                       CAGR_RANDOM=float(o.OOS_CAGR.loc[vals].mean()),
                       MaxDD_aware=float(o.OOS_MaxDD[aware]), MaxDD_blind=float(o.OOS_MaxDD[blind]),
                       MaxDD_DEFAULT=float(o.OOS_MaxDD[dn]),
                       MaxDD_RANDOM=float(o.OOS_MaxDD.loc[vals].mean()),
                       turn_aware=float(o.turn_yr_oos[aware]), turn_blind=float(o.turn_yr_oos[blind]),
                       turn_DEFAULT=float(o.turn_yr_oos[dn]),
                       vol_aware=float(o.OOS_vol[aware]),
                       v1_OOS_Sharpe=float(o.v1_OOS_Sharpe.iloc[0]),
                       v1_OOS_CAGR=float(o.v1_OOS_CAGR.iloc[0]),
                       v1_OOS_MaxDD=float(o.v1_OOS_MaxDD.iloc[0]),
                       v2_OOS_Sharpe=float(o.v2_OOS_Sharpe.iloc[0]),
                       v2_OOS_CAGR=float(o.v2_OOS_CAGR.iloc[0]),
                       v2_OOS_MaxDD=float(o.v2_OOS_MaxDD.iloc[0]),
                       spy_OOS_Sharpe=float(o.spy_OOS_Sharpe.iloc[0]),
                       spy_OOS_CAGR=float(o.spy_OOS_CAGR.iloc[0]),
                       spy_OOS_MaxDD=float(o.spy_OOS_MaxDD.iloc[0]))
            for comp in ("DEFAULT", "MEDIAN", "RANDOM"):
                row[f"L_aware_{comp}"] = row["OOS_aware"] - row[f"OOS_{comp}"]
                row[f"L_blind_{comp}"] = row["OOS_blind"] - row[f"OOS_{comp}"]
            row["DELTA"] = row["OOS_aware"] - row["OOS_blind"]
            row["DELTA_IS"] = row["IS_aware"] - row["IS_blind"]
            wf.append(row)
    return pd.DataFrame(wf)


def repro_gate(W):
    """Exact reproduction of idea 235's committed live walk-forward on its own 4 dials."""
    if not REF235.exists():
        print("  [repro] idea 235's walkforward.csv not committed — gate SKIPPED")
        return
    R = pd.read_csv(REF235).rename(columns={"OOS_pick": "ref_OOS_aware", "OOS_pick0": "ref_OOS_blind",
                                            "OOS_DN": "ref_OOS_DEFAULT", "OOS_MEDIAN": "ref_OOS_MEDIAN",
                                            "OOS_RANDOM": "ref_OOS_RANDOM"})
    cols = ["panel", "dial", "bps", "ref_OOS_aware", "ref_OOS_blind", "ref_OOS_DEFAULT",
            "ref_OOS_MEDIAN", "ref_OOS_RANDOM"]
    J = W[W.dial.isin(REF_DIALS)].merge(R[cols], on=["panel", "dial", "bps"], how="inner")
    print(f"  [repro] joined {len(J)} of {len(W[W.dial.isin(REF_DIALS)])} shared rows "
          f"against idea 235")
    for a, b in (("OOS_aware", "ref_OOS_aware"), ("OOS_blind", "ref_OOS_blind"),
                 ("OOS_DEFAULT", "ref_OOS_DEFAULT"), ("OOS_MEDIAN", "ref_OOS_MEDIAN"),
                 ("OOS_RANDOM", "ref_OOS_RANDOM")):
        d = (J[a] - J[b]).abs().max()
        print(f"    max |{a} - idea235| = {d:.3e}  {'OK' if d < 1e-9 else '*** MISMATCH ***'}")
    t = J[J.bps == 10]
    print(f"    idea 235's 10-bps headline re-read: aware-DEFAULT "
          f"{(t.ref_OOS_aware - t.ref_OOS_DEFAULT).mean():+.4f}, blind-DEFAULT "
          f"{(t.ref_OOS_blind - t.ref_OOS_DEFAULT).mean():+.4f} over {len(t)} cells "
          f"(idea 231 quoted +0.0177 / -0.0237 on its own corpus)")


# ------------------------------------------------------------------ reporting
def split_table(D, comparand, label, cluster=None, curve=None, source=""):
    """Print L_aware / L_blind / DELTA at every rung for one comparand."""
    print(f"\n  --- {label}  (comparand p1 = {comparand}) ---")
    print(f"  {'rung':>5s} {'n':>6s} {'L_aware':>9s} {'win':>5s} {'p':>7s} {'L_blind':>9s} "
          f"{'win':>5s} {'p':>7s} {'DELTA':>9s} {'win':>5s} {'p':>7s} {'moved':>6s} "
          f"{'D|moved':>8s} {'DELTA_IS':>9s} {'transfer':>8s}")
    for c in sorted(D.bps.unique()):
        S = D[D.bps == c]
        if len(S) < 10:
            continue
        la, lb = S[f"L_aware_{comparand}"], S[f"L_blind_{comparand}"]
        dl, dis = S["DELTA"], S["DELTA_IS"]
        wa, pa, _ = sign_test(la); wb, pb, _ = sign_test(lb); wd, pd_, _ = sign_test(dl)
        mv = S.moved.mean()
        dm = dl[S.moved].mean() if S.moved.any() else np.nan
        tr = dl.mean() / dis.mean() if dis.mean() > 1e-12 else np.nan
        print(f"  {c:5.0f} {len(S):6d} {la.mean():+9.4f} {wa:5.2f} {pa:7.4f} {lb.mean():+9.4f} "
              f"{wb:5.2f} {pb:7.4f} {dl.mean():+9.4f} "
              f"{wd if wd == wd else float('nan'):5.2f} {pd_ if pd_ == pd_ else float('nan'):7.4f} "
              f"{mv:6.3f} {dm if dm == dm else float('nan'):+8.4f} {dis.mean():+9.4f} "
              f"{tr if tr == tr else float('nan'):8.3f}")
        if curve is not None:
            lo, hi = boot_ci(dl.values, S[cluster].values if cluster else None)
            curve.append(dict(source=source, weighting=label, comparand=comparand, bps=c, n=len(S),
                              L_aware=float(la.mean()), L_blind=float(lb.mean()),
                              DELTA=float(dl.mean()), DELTA_lo=lo, DELTA_hi=hi,
                              DELTA_IS=float(dis.mean()), moved_rate=float(mv),
                              DELTA_given_moved=float(dm) if dm == dm else np.nan,
                              win_aware=wa, p_aware=pa, win_blind=wb, p_blind=pb,
                              win_delta=wd, p_delta=pd_))


def main():
    curve = []
    print("=" * 100)
    print("PART A — the record, re-read as blind-vs-aware selection claims")
    print("=" * 100)
    C = scan_archive()
    C.to_csv(f"{OUT}.census.csv.gz", index=False, compression="gzip")
    ncell = C.groupby(["file", "dial", "cell"]).ngroups
    nz = C[C.zero_anchored]
    print(f"\n  corpus: {len(C)} rung-readings, {C.file.nunique()} files, {ncell} cells; "
          f"ZERO-ANCHORED (ladder commits a 0-bps rung): {len(nz)} readings, "
          f"{nz.file.nunique()} files, {nz.groupby(['file','dial','cell']).ngroups} cells "
          f"({len(nz)/max(len(C),1):.1%} of readings)")

    print("\n=== GATE 0 — the identity DELTA == 0 whenever the rung does not move the argmax ===")
    still = C[~C.moved]
    print(f"  non-moving readings: {len(still)} of {len(C)} ({len(still)/len(C):.1%}); "
          f"max |DELTA| there = {still.DELTA.abs().max():.3e}, max |DELTA_IS| = "
          f"{still.DELTA_IS.abs().max():.3e}  "
          f"{'OK' if still.DELTA.abs().max() < 1e-12 else '*** BROKEN ***'}")
    print(f"  so ALL of the blind-vs-aware difference lives in the {C.moved.mean():.1%} of "
          f"readings where the cost rung actually re-ranks the dial "
          f"(zero-anchored subcorpus: {nz.moved.mean():.1%})")
    print(f"  GATE 0b — DELTA_IS >= 0 is an in-sample identity: violations "
          f"{(C.DELTA_IS < -1e-12).sum()} of {len(C)}  "
          f"{'OK' if (C.DELTA_IS < -1e-12).sum() == 0 else '*** BROKEN ***'}")

    for comp in ("MEDIAN", "RANDOM"):
        split_table(C, comp, "ARCHIVE cell-weighted", cluster="file", curve=curve, source="ARCHIVE")
        split_table(nz, comp, "ARCHIVE zero-anchored", cluster="file", curve=curve,
                    source="ARCHIVE_ZERO")
        F = (C.groupby(["file", "bps"])[[f"L_aware_{comp}", f"L_blind_{comp}", "DELTA", "DELTA_IS",
                                         "moved"]].mean().reset_index())
        F["moved"] = F.moved > 0
        split_table(F, comp, "ARCHIVE file-weighted", curve=curve, source="ARCHIVE_FILEWTD")

    print("\n=== the record's 'SELECTION LOSES' instances, split into blind and aware halves ===")
    print("  an instance = one (file, dial, cell) read at one rung whose COST-AWARE chooser")
    print("  loses to the comparand.  The question is how many of them cost-awareness would")
    print("  have saved, i.e. how many are really COST-BLINDNESS losing rather than choosing.")
    inst = []
    for comp in ("MEDIAN", "RANDOM"):
        for tag, D in (("ALL", C), ("ZERO_ANCHORED", nz)):
            for c in sorted(D.bps.unique()):
                S = D[D.bps == c]
                if len(S) < 10:
                    continue
                la, lb = S[f"L_aware_{comp}"], S[f"L_blind_{comp}"]
                lose_a, lose_b = la < 0, lb < 0
                both = int((lose_a & lose_b).sum())
                only_blind = int((~lose_a & lose_b).sum())      # cost-awareness SAVES the claim
                only_aware = int((lose_a & ~lose_b).sum())      # costing the choice HURTS
                inst.append(dict(comparand=comp, subcorpus=tag, bps=c, n=len(S),
                                 lose_aware=int(lose_a.sum()), lose_blind=int(lose_b.sum()),
                                 lose_both=both, saved_by_costing=only_blind,
                                 broken_by_costing=only_aware,
                                 mean_L_aware_when_losing=float(la[lose_a].mean()) if lose_a.any() else np.nan,
                                 mean_L_blind_when_losing=float(lb[lose_b].mean()) if lose_b.any() else np.nan,
                                 share_of_aware_losses_fixable=float(
                                     (lose_a & (lb < la)).sum() / max(int(lose_a.sum()), 1))))
    I = pd.DataFrame(inst)
    I.to_csv(f"{OUT}.instances.csv", index=False)
    for tag in ("ALL", "ZERO_ANCHORED"):
        S = I[(I.comparand == "MEDIAN") & (I.subcorpus == tag)]
        print(f"\n  [{tag}, comparand MEDIAN]")
        print(f"  {'rung':>5s} {'n':>6s} {'aware loses':>12s} {'blind loses':>12s} "
              f"{'both':>6s} {'saved by costing':>17s} {'broken by costing':>18s}")
        for _, r in S.iterrows():
            print(f"  {r.bps:5.0f} {r.n:6.0f} {r.lose_aware:6.0f} ({r.lose_aware/r.n:5.1%}) "
                  f"{r.lose_blind:6.0f} ({r.lose_blind/r.n:5.1%}) {r.lose_both:6.0f} "
                  f"{r.saved_by_costing:9.0f} ({r.saved_by_costing/r.n:5.1%}) "
                  f"{r.broken_by_costing:10.0f} ({r.broken_by_costing/r.n:5.1%})")

    print("\n=== rung slopes (does the blind half fall away faster than the aware half?) ===")
    A = pd.DataFrame(curve)
    for src in ("ARCHIVE", "ARCHIVE_ZERO", "ARCHIVE_FILEWTD"):
        S = A[(A.source == src) & (A.comparand == "MEDIAN")].sort_values("bps")
        if len(S) < 3:
            continue
        ba, ra = slope(S.bps, S.L_aware); bb, rb = slope(S.bps, S.L_blind)
        bd, rd = slope(S.bps, S.DELTA)
        print(f"  {src:17s} L_aware {ba:+.6f}/bp (R2 {ra:.2f})   L_blind {bb:+.6f}/bp "
              f"(R2 {rb:.2f})   DELTA {bd:+.6f}/bp (R2 {rd:.2f})")

    print("\n" + "=" * 100)
    print("PART B — live, PROTOCOL rule 8: pick on 2009-2016, read 2017-2026 once")
    print("=" * 100)
    G = part_b()
    G["pass4a"] = G.fail4a == ""; G["pass4b"] = G.fail4b == ""
    G.to_csv(f"{OUT}.grid.csv", index=False)
    G.groupby(["panel", "dial", "bps"])[["pass4a", "pass4b"]].sum().reset_index().to_csv(
        f"{OUT}.keeppaths.csv", index=False)
    W = walk_forward(G)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n=== GATE 1 — reproduction of idea 235's committed live walk-forward ===")
    repro_gate(W)

    print(f"\n=== LIVE rung curve, {W[W.bps == 10].shape[0]} (panel x dial) cells per rung ===")
    for comp in ("DEFAULT", "MEDIAN", "RANDOM"):
        split_table(W, comp, "LIVE 18 cells", cluster="panel", curve=curve, source="LIVE")
    for comp in ("DEFAULT",):
        split_table(W[W.dial.isin(REF_DIALS)], comp, "LIVE idea-235 dials only",
                    cluster="panel", curve=curve, source="LIVE_235DIALS")
    pd.DataFrame(curve).to_csv(f"{OUT}.rungcurve.csv", index=False)

    print("\n=== LIVE OOS Sharpe levels by rung (what each chooser actually earns) ===")
    print(f"  {'rung':>5s} {'aware':>8s} {'blind':>8s} {'default':>8s} {'median':>8s} "
          f"{'random':>8s} {'oracle':>8s} {'SPY':>8s} {'v1':>8s} {'v2':>8s}")
    for c in RUNGS:
        S = W[W.bps == c]
        print(f"  {c:5d} {S.OOS_aware.mean():8.4f} {S.OOS_blind.mean():8.4f} "
              f"{S.OOS_DEFAULT.mean():8.4f} {S.OOS_MEDIAN.mean():8.4f} {S.OOS_RANDOM.mean():8.4f} "
              f"{S.OOS_ORACLE.mean():8.4f} {S.spy_OOS_Sharpe.mean():8.4f} "
              f"{S.v1_OOS_Sharpe.mean():8.4f} {S.v2_OOS_Sharpe.mean():8.4f}")

    print("\n=== is DELTA one dial? (live, per dial, pooled over rungs and panels) ===")
    print(f"  {'dial':>5s} {'cells':>6s} {'moved':>6s} {'DELTA':>9s} {'D|moved':>9s} "
          f"{'L_aware':>9s} {'L_blind':>9s}")
    for d_, S in W.groupby("dial"):
        dm = S.DELTA[S.moved].mean() if S.moved.any() else np.nan
        print(f"  {d_:>5s} {len(S):6d} {S.moved.mean():6.3f} {S.DELTA.mean():+9.4f} "
              f"{dm if dm == dm else float('nan'):+9.4f} {S.L_aware_DEFAULT.mean():+9.4f} "
              f"{S.L_blind_DEFAULT.mean():+9.4f}")
    tot = W.DELTA.mean()
    for d_ in sorted(W.dial.unique()):
        ex = W[W.dial != d_].DELTA.mean()
        print(f"  drop dial {d_}: pooled DELTA {tot:+.4f} -> {ex:+.4f}")

    print("\n=== rule 8 headline at PROTOCOL's own 10 bps ===")
    t = W[W.bps == 10]
    for nm, s, cg, dd in (("aware chooser", "OOS_aware", "CAGR_aware", "MaxDD_aware"),
                          ("blind chooser", "OOS_blind", "CAGR_blind", "MaxDD_blind"),
                          ("do-nothing   ", "OOS_DEFAULT", "CAGR_DEFAULT", "MaxDD_DEFAULT"),
                          ("random arm   ", "OOS_RANDOM", "CAGR_RANDOM", "MaxDD_RANDOM")):
        print(f"  {nm:14s} OOS Sharpe {t[s].mean():.4f}  CAGR {t[cg].mean():7.2%}  "
              f"MaxDD {t[dd].mean():7.2%}")
    for nm, s, cg, dd in (("RULES v1", "v1_OOS_Sharpe", "v1_OOS_CAGR", "v1_OOS_MaxDD"),
                          ("RULES v2", "v2_OOS_Sharpe", "v2_OOS_CAGR", "v2_OOS_MaxDD"),
                          ("SPY     ", "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD")):
        print(f"  {nm:14s} OOS Sharpe {t[s].mean():.4f}  CAGR {t[cg].mean():7.2%}  "
              f"MaxDD {t[dd].mean():7.2%}   (panel mean)")
    for p_ in ("U56", "B136", "SMALL439"):
        s = t[t.panel == p_].iloc[0]
        print(f"    {p_:9s} v1 {s.v1_OOS_Sharpe:.4f} ({s.v1_OOS_CAGR:.2%}, {s.v1_OOS_MaxDD:.2%})  "
              f"v2 {s.v2_OOS_Sharpe:.4f} ({s.v2_OOS_CAGR:.2%}, {s.v2_OOS_MaxDD:.2%})  "
              f"SPY {s.spy_OOS_Sharpe:.4f} ({s.spy_OOS_CAGR:.2%}, {s.spy_OOS_MaxDD:.2%})")
    for comp in ("DEFAULT", "MEDIAN", "RANDOM"):
        wa, pa, na = sign_test(t[f"L_aware_{comp}"]); wb, pb, nb = sign_test(t[f"L_blind_{comp}"])
        lo, hi = boot_ci(t.DELTA.values, t.panel.values)
        print(f"  vs {comp:8s}: aware {t[f'L_aware_{comp}'].mean():+.4f} "
              f"({int(wa*na)}/{na}, p {pa:.3f})   blind {t[f'L_blind_{comp}'].mean():+.4f} "
              f"({int(wb*nb)}/{nb}, p {pb:.3f})   DELTA {t.DELTA.mean():+.4f} "
              f"[{lo:+.4f}, {hi:+.4f}]")

    print("\n=== KEEP paths over all Part B grid points ===")
    print(f"  4a {int(G.pass4a.sum())} / {len(G)}    4b {int(G.pass4b.sum())} / {len(G)}")
    for p_ in ("U56", "B136", "SMALL439"):
        s = G[G.panel == p_]
        print(f"    {p_:9s} 4a {int(s.pass4a.sum()):3d}/{len(s)}   4b {int(s.pass4b.sum()):3d}/{len(s)}")
    fb = G[~G.pass4b].fail4b.str.split(",").explode().value_counts()
    print("  4b failing bars (sole + joint): " + ", ".join(f"{k} {v}" for k, v in fb.items()))
    print("\n  do the CHOSEN books pass anything? (the arms rule 8 actually picks, at 10 bps)")
    for _, r in t.iterrows():
        g = G[(G.panel == r.panel) & (G.dial == r.dial) & (G.value == r.aware) & (G.bps == 10)]
        if len(g):
            g = g.iloc[0]
            print(f"    {r.panel:9s} {r.dial}={r.aware:<6} 4a {'PASS' if g.pass4a else g.fail4a:12s} "
                  f"4b {'PASS' if g.pass4b else g.fail4b}")
    print("\n  full sample at 10 bps, best Sharpe per panel:")
    for p_ in ("U56", "B136", "SMALL439"):
        s = G[(G.panel == p_) & (G.bps == 10)].nlargest(1, "Sharpe").iloc[0]
        print(f"    {p_:9s} {s.dial}={s.value}  Sharpe {s.Sharpe:.3f} (H1 {s.H1:.3f}/H2 {s.H2:.3f})  "
              f"CAGR {s.CAGR:.2%}  MaxDD {s.MaxDD:.2%}  OOS {s.OOS_Sharpe:.3f}  "
              f"4a {'PASS' if s.pass4a else s.fail4a}  4b {'PASS' if s.pass4b else s.fail4b}")


if __name__ == "__main__":
    main()
