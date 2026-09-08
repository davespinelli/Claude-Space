#!/usr/bin/env python3
"""Idea 234 — re-read-single-rung-argmaxes-on-V1C-shaped-books (lane B, 2026-09-08).

Pre-registered question (QUEUE 234): idea 230 found chooser-sensitivity is a property of the
CONSTRUCTION (V1C 7/12 panel x dial cells re-rankable by the cost rung, EWALL 2/9).  Flag every
published dial argmax whose parent quoted ONE cost rung and whose book is V1C-shaped
(vol-scaled ranking, >20x/yr turnover); re-run those at 0/10/30 bps.

THE HYPOTHESIS, stated so it can fail: a single-rung argmax published on a V1C-shaped book is
AT RISK — the rung it was read at is a free parameter that moves the winner.  Under the
hypothesis the flagged population should (i) be large (the record mostly quotes one rung),
(ii) sit on constructions whose re-rank rate at 0/10/30 bps is materially above the un-scaled
and un-ranked controls, and (iii) carry a measurable cost of ignoring the rung.  The falsifier
is a re-rank rate on V1C-shaped books that is NOT above its controls, or a cost of ignoring the
rung that is inside noise — in which case "V1C-shaped" is not a useful flag and the record's
single-rung argmaxes need no asterisk.

TWO TUNED PARAMETERS ONLY:
    p1 = TURNOVER THRESHOLD T of the shape test  {0 (off), 10, 20, 30, 50} x/yr.  The queue
         names 20; all five are reported (census.py + flagcurve.csv).
    p2 = COST RUNG at which an argmax is read  {0, 5, 10, 15, 20, 25, 30} bps.  The queue names
         0/10/30; the full ladder is free under the cost identity and ALL of it is reported.
Nothing else is tuned.  The vol-scaled leg of the shape test has TWO pre-registered readings
(LOOSE and NAMED, below) and BOTH are reported side by side — neither is selected.

PART A — the census (exact, over the committed record).  Every committed CSV under
research/backtests is re-read.  A file is a SINGLE-RUNG parent if it has no cost-rung column or
a cost-rung column with exactly one distinct value.  Inside such a file, every (dial column,
other-dial values held fixed) rectangle with >=3 arms and a Sharpe-like objective is ONE
published dial argmax claim.  Each claim gets:
    vol_scaled_LOOSE  the sibling .py builds a vol-scaled ranking key at all
                      (`vol_scale=True` | `/vol20` | `vol20.clip` | literal `V1C`)
    vol_scaled_NAMED  LOOSE and the claim's own book label is not an explicitly un-scaled book
                      ({EWALL, TOPN, COMP, EW, EWALL*, BAND*, SPY, ...} -> False)
    turn_yr           the file's own committed per-year turnover for that claim, when it
                      commits one (column name contains 'turn'); NaN otherwise
    FLAGGED(T)        vol_scaled AND (turn_yr > T, or T == 0)
The census is a count, not a re-simulation: an archive file that quotes one rung cannot be read
at another rung without re-simulating, which is what Part B does.

PART B — the live re-run at 0/10/30 (and the whole ladder).  The dial families the census
actually finds are re-simulated from prices on three panels x three books:
    V1C   the flagged shape: rank = composite / max(vol20, 0.08)**0.5 (the traded score), top n
    TOPN  same shape, un-scaled composite ranking            -- ranking control
    EWALL equal-weight every eligible name, no ranking        -- construction control
Dials: N (count), G (200d band), V (vol cap), K (cadence weeks), GROSS (target gross).  For each
(panel, book, dial) the argmax is read at every rung; the verdict is whether the winner MOVES
between 0/10/30 bps, and the cost of ignoring the rung is OOS_Sharpe(pick at own rung) minus
OOS_Sharpe(pick at 0 bps), evaluated at the true rung.
Cost identity: held weights and turnover do not depend on cost, so net(c) = gross - turn*c/1e4
exactly; asserted against engine.backtest at 10 bps and reported (.identity.csv).

PROTOCOL rule 8 (walk-forward) is run for every (panel, book, dial, rung): the dial value is
chosen on 2009-2016 IS only, 2017-2026 is read ONCE, and reported against do-nothing (the
default arm), a random arm (mean over arms), the oracle ceiling, RULES v1, RULES v2 and SPY.
Both KEEP paths (4a vs the live RULES v2 book, 4b vs SPY) are evaluated on EVERY grid point.

SURVIVORSHIP: universe.json and universe_broad.json are current constituents; the small panel is
current constituents of a sub-$2B screen (data/SMALL_PANEL_README.md) with the 44 tickers whose
max_1d_move >= 1.0 dropped first (484 -> SMALL439 + SPY).  All long-book numbers here are upper
bounds.

Outputs (all committed):
    .claims.csv     PART A: every published single-rung dial-argmax claim, with its flags
    .flagcurve.csv  PART A: flagged counts vs T, under LOOSE and NAMED
    .grid.csv       PART B: every (panel, book, dial, value, rung) with 4a/4b bars
    .census.csv     PART B: per (panel, book, dial) argmax at each rung, re-rank verdict, cost
    .walkforward.csv PART B: rule 8, IS pick per rung, OOS read once, all comparands
    .keep.csv       PART B: 4a / 4b pass counts per (panel, book, dial, rung)
    .identity.csv   cost-identity check vs engine.backtest
    .console.txt    full console log
"""
import glob
import re
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
from engine import backtest, metrics                                          # noqa: E402

OUT = Path(__file__).with_suffix("")
BT = ROOT / "research" / "backtests"
SELF = Path(__file__).name

RUNGS = [0, 5, 10, 15, 20, 25, 30]
HEADLINE_RUNGS = [0, 10, 30]                 # p2, the rungs the queue names
T_GRID = [0, 10, 20, 30, 50]                 # p1, turnover threshold of the shape test
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

_log_lines = []


def log(*a):
    s = " ".join(str(x) for x in a)
    _log_lines.append(s)
    print(s, flush=True)


# ===================================================================== PART A
COST_NAMES = {"bps", "cost_bps", "cost", "rung", "cost_rung", "bps_rung", "c_bps", "costbps"}
METRIC_SUBSTR = ("sharpe", "cagr", "maxdd", "dd", "vol", "turn", "gross", "pass", "fail",
                 "p4a", "p4b", "f4a", "f4b", "oos", "_is", "is_", "h1", "h2", "ret", "equity",
                 "pval", "p_", "_p", "ci", "sd", "std", "mean", "median", "hit", "win",
                 "margin", "regret", "excess", "premium", "delta", "d_", "rho", "corr", "n_",
                 "count", "seed", "invested", "held", "days", "sortino", "calmar", "alpha",
                 "beta", "skew", "kurt", "note", "verdict", "reason", "file", "date", "nobs")
# books the record names that are explicitly NOT vol-scaled rankings
UNSCALED_BOOKS = {"ewall", "ew", "ewal", "topn", "comp", "equal", "eqw", "spy", "bh",
                  "buyhold", "band", "band3", "band3-rw", "ewall+band3", "none", "raw",
                  "r6", "r3", "mom", "lowvol", "shuff", "shufw", "random", "rand"}
VS_LOOSE = re.compile(r"vol_scale\s*=\s*True|/\s*vol20|vol20\.clip|\bV1C\b|\bV1LIT\b")


def is_metric(col):
    c = str(col).strip().lower()
    return any(s in c for s in METRIC_SUBSTR)


def sibling_py(csv_path):
    p = Path(csv_path)
    stem = p.name.split(".")[0]
    q = p.parent / (stem + ".py")
    return q if q.exists() else None


_py_cache = {}


def vol_scaled_loose(csv_path):
    q = sibling_py(csv_path)
    if q is None:
        return None                      # unknowable: no sibling script committed
    if q not in _py_cache:
        _py_cache[q] = bool(VS_LOOSE.search(q.read_text(errors="ignore")))
    return _py_cache[q]


def objective_cols(cols):
    """Sharpe-like objective columns, full-sample preferred over OOS."""
    out = []
    for c in cols:
        lc = str(c).strip().lower()
        if "sharpe" in lc:
            out.append(c)
    full = [c for c in out if "oos" not in str(c).lower()]
    return full or out


def part_a():
    """Census every committed CSV for single-rung published dial argmaxes."""
    files = sorted(glob.glob(str(BT / "*.csv"))) + sorted(glob.glob(str(BT / "*.csv.gz")))
    files = [f for f in files if SELF.split(".")[0] not in Path(f).name]
    claims, n_read, n_sharpe, n_single = [], 0, 0, 0
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        n_read += 1
        if len(df) < 3:
            continue
        df = df.loc[:, ~df.columns.duplicated()]
        cols = list(df.columns)
        low = [str(c).strip().lower() for c in cols]
        obj = objective_cols(cols)
        if not obj:
            continue
        n_sharpe += 1
        cc = [cols[i] for i, c in enumerate(low) if c in COST_NAMES]
        rung_vals = sorted(pd.to_numeric(df[cc[0]], errors="coerce").dropna().unique()) if cc else []
        if cc and len(rung_vals) > 1:
            continue                      # multi-rung parent: not this idea's population
        n_single += 1
        quoted_rung = float(rung_vals[0]) if len(rung_vals) == 1 else np.nan   # NaN == implicit
        dials = [c for c in cols
                 if not is_metric(c) and c not in cc and 3 <= df[c].nunique(dropna=True) <= 40]
        if not dials:
            continue
        vsl = vol_scaled_loose(f)
        turn_cols = [cols[i] for i, c in enumerate(low) if "turn" in c]
        book_cols = [cols[i] for i, c in enumerate(low)
                     if c in ("book", "arm", "construction", "shape")]
        ob = obj[0]
        for d in dials:
            others = [c for c in dials if c != d]
            if others:
                keys = df[others].apply(lambda r: "|".join(map(str, r.tolist())), axis=1)
            else:
                keys = pd.Series(["_"] * len(df), index=df.index)
            for kv, sub in df.groupby(keys):
                arms = sub[d].nunique(dropna=True)
                if arms < 3:
                    continue
                y = pd.to_numeric(sub[ob], errors="coerce")
                if y.notna().sum() < 3:
                    continue
                lab = ""
                if book_cols:
                    u = sub[book_cols[0]].dropna().astype(str).unique()
                    lab = str(u[0]).strip().lower() if len(u) == 1 else "|".join(u[:3]).lower()
                named = bool(vsl) and not any(b in lab for b in UNSCALED_BOOKS)
                tv = np.nan
                tcol = ""
                if turn_cols:
                    t = pd.to_numeric(sub[turn_cols[0]], errors="coerce").dropna()
                    if len(t):
                        tv = float(t.median())
                        tcol = str(turn_cols[0])
                dv = pd.to_numeric(sub[d], errors="coerce")
                numeric_dial = bool(dv.notna().sum() >= max(3, 0.8 * len(sub)))
                claims.append(dict(
                    file=Path(f).name, dial=str(d).strip().lower(), objective=str(ob),
                    cell=str(kv)[:60], arms=int(arms), quoted_rung=quoted_rung,
                    book_label=lab[:30], turn_yr=tv, turn_col=tcol,
                    numeric_dial=numeric_dial,
                    vol_scaled_LOOSE=bool(vsl) if vsl is not None else np.nan,
                    vol_scaled_NAMED=named if vsl is not None else np.nan,
                    argmax=str(sub.loc[y.idxmax(), d]),
                    top1=float(y.max()),
                    top2=float(y.sort_values(ascending=False).iloc[1]),
                ))
    cl = pd.DataFrame(claims)
    log(f"[A] CSVs read {n_read}; with a Sharpe-like objective {n_sharpe}; "
        f"single-rung parents {n_single}; published dial-argmax claims {len(cl)}")
    if len(cl):
        cl["gap"] = cl.top1 - cl.top2
        log(f"[A] claims with a committed per-year turnover column: "
            f"{int(cl.turn_yr.notna().sum())} of {len(cl)}")
        log(f"[A] quoted rung: explicit on {int(cl.quoted_rung.notna().sum())} claims "
            f"(values {sorted(cl.quoted_rung.dropna().unique())[:6]}), "
            f"implicit (PROTOCOL 10 bps) on {int(cl.quoted_rung.isna().sum())}")
    rows = []
    for T in T_GRID:
        for leg in ("vol_scaled_LOOSE", "vol_scaled_NAMED"):
            for pop, mask in (("ALL", pd.Series(True, index=cl.index)),
                              ("NUMERIC_DIALS", cl.numeric_dial.astype(bool)
                               if len(cl) else pd.Series(dtype=bool))):
                ok = cl[leg].fillna(False).astype(bool) & mask
                tn = cl.turn_yr > T if T > 0 else pd.Series(True, index=cl.index)
                rows.append(dict(
                    T=T, leg=leg, population=pop, n_claims=int(mask.sum()),
                    n_vol_scaled=int(ok.sum()), n_turn_known=int((cl.turn_yr.notna() & mask).sum()),
                    n_flagged=int((ok & tn.fillna(False)).sum()),
                    n_flagged_turn_unknown=int((ok & cl.turn_yr.isna()).sum()),
                    n_files_flagged=int(cl.loc[ok & tn.fillna(False), "file"].nunique())))
    fc = pd.DataFrame(rows)
    return cl, fc


def fisher_exact_2x2(a, b, c, d):
    """Two-sided Fisher exact p for [[a,b],[c,d]] (no scipy dependency)."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def pr(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = pr(a)
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    return float(sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 * (1 + 1e-12)))


# ===================================================================== PART B
DEFAULTS = dict(N=20, G=0.00, V=0.60, K=1, GROSS=1.00)
DIAL_VALUES = {
    "N":     [3, 5, 8, 10, 15, 20, 25, 30, 40, 56],
    "G":     [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
    "V":     [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, 5.00],
    "K":     [1, 2, 3, 4, 6, 8, 13],
    "GROSS": [0.25, 0.50, 0.75, 0.90, 1.00],
}
BOOKS = ["V1C", "TOPN", "EWALL"]
BOOK_DIALS = {"V1C": ["N", "G", "V", "K", "GROSS"],
              "TOPN": ["N", "G", "V", "K", "GROSS"],
              "EWALL": ["G", "V", "K", "GROSS"]}      # EWALL has no count dial


def week_mask(idx, k):
    per = idx.to_period("W")
    s = pd.Series(per, index=idx)
    last = (s != s.shift(-1)).values
    if k == 1:
        return last
    ordinal = pd.Series(pd.factorize(per)[0], index=idx).values
    return last & ((ordinal % k) == 0)


def simulate(px, W, mask):
    """engine.backtest's loop with an arbitrary rebalance mask; GROSS returns + turnover."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).values
    m = np.concatenate([[False], mask[:-1]])
    cur = np.zeros(px.shape[1])
    held = np.empty_like(rets)
    turn = np.zeros(len(px))
    for i in range(len(px)):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    gross = pd.Series((held * rets).sum(axis=1), index=px.index)
    return gross, pd.Series(turn, index=px.index), pd.Series(held.sum(axis=1), index=px.index)


def eligible(px, ma, vol20, g, max_vol):
    if g == 0:
        above = px > ma
    else:
        sig = pd.DataFrame(np.where(px > ma * (1 + g), 1.0,
                                    np.where(px < ma * (1 - g), 0.0, np.nan)),
                           index=px.index, columns=px.columns)
        above = sig.ffill().fillna(0.0) > 0.5
    return above & (vol20 < max_vol)


def book_weights(book, px, keys, ma, vol20, n, g, max_vol, gross):
    el = eligible(px, ma, vol20, g, max_vol)
    if book == "EWALL":
        w = el.astype(float)
        cnt = w.sum(axis=1)
        return gross * w.div(cnt.where(cnt > 0), axis=0).fillna(0.0)
    key = keys["comp"] if book == "TOPN" else keys["v1score"]
    rank = key.where(el).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def net(gross, turn, bps):
    return gross - turn * bps / 1e4


def stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def bars_4a(s, b):
    f = []
    if not s["H1"] > b["H1"]:
        f.append("H1")
    if not s["H2"] > b["H2"]:
        f.append("H2")
    if not s["MaxDD"] >= b["MaxDD"]:
        f.append("DD")
    return ",".join(f)


def bars_4b(s, spy, oos_s, oos_spy):
    f = []
    if not s["H1"] > spy["H1"]:
        f.append("H1")
    if not s["H2"] > spy["H2"]:
        f.append("H2")
    if not oos_s > oos_spy:
        f.append("OOS")
    if not s["MaxDD"] >= 0.60 * spy["MaxDD"]:
        f.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]:
        f.append("CAGR")
    return ",".join(f)


def small_screened():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    log(f"[B] SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY")
    return px[keep]


def panels():
    yield "U56", load_universe()
    yield "B136", load_universe(broad=True)
    yield "SMALL439", small_screened()


def part_b():
    grid, census, wf, ident = [], [], [], []
    for pname, px in panels():
        t0 = time.time()
        s_ns, above_raw, vol20 = score(px, vol_scale=False)
        comp = s_ns / (0.5 + 0.5 * above_raw.astype(float))      # exact composite
        v1score, _, _ = score(px, vol_scale=True)                # the traded score
        keys = dict(comp=comp, v1score=v1score)
        ma = px.rolling(200).mean()
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_s = stats(spy_r)
        spy_oos = metrics(spy_r.loc[OOS_START:])["Sharpe"]
        spy_is = metrics(spy_r.loc[:IS_END])["Sharpe"]

        # baselines per rung: RULES v2 (live, 4a comparand) and RULES v1 (continuity)
        b2g, b2t, _ = simulate(px, rules_v2_weights(px), week_mask(px.index, 1))
        b1g, b1t, _ = simulate(px, rules_v1_weights(px), week_mask(px.index, 1))
        base2 = {c: stats(net(b2g, b2t, c).loc[start:]) for c in RUNGS}
        base2_oos = {c: metrics(net(b2g, b2t, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
        base1 = {c: stats(net(b1g, b1t, c).loc[start:]) for c in RUNGS}
        base1_oos = {c: metrics(net(b1g, b1t, c).loc[OOS_START:])["Sharpe"] for c in RUNGS}
        eng = backtest(px, rules_v1_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        d = float(np.abs(eng - net(b1g, b1t, 10).loc[start:]).max())
        ident.append(dict(panel=pname, book="RULES v1", max_abs_diff_vs_engine_10bps=d))
        log(f"[B] {pname}: cost-identity max|d| vs engine at 10 bps = {d:.3e}")

        sims = {}
        for book in BOOKS:
            for dial in BOOK_DIALS[book]:
                for v in DIAL_VALUES[dial]:
                    kw = dict(DEFAULTS)
                    kw[dial] = v
                    if dial == "N" and v > px.shape[1] - 1:
                        continue
                    sig = (book, kw["N"] if book != "EWALL" else -1, kw["G"], kw["V"],
                           kw["K"], kw["GROSS"])
                    if sig not in sims:
                        W = book_weights(book, px, keys, ma, vol20, kw["N"], kw["G"], kw["V"],
                                         kw["GROSS"])
                        sims[sig] = simulate(px, W, week_mask(px.index, kw["K"]))
                    g, t, inv = sims[sig]
                    gs, ts = g.loc[start:], t.loc[start:]
                    yrs = len(gs) / 252
                    for c in RUNGS:
                        r = net(gs, ts, c)
                        st = stats(r)
                        oos = metrics(r.loc[OOS_START:])["Sharpe"]
                        is_s = metrics(r.loc[:IS_END])["Sharpe"]
                        grid.append(dict(panel=pname, book=book, dial=dial, value=v, bps=c,
                                         turn_yr=float(ts.sum() / yrs),
                                         mean_invested=float(inv.loc[start:].mean()),
                                         **st, IS_Sharpe=is_s, OOS_Sharpe=oos,
                                         OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                         OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                         f4a=bars_4a(st, base2[c]),
                                         f4b=bars_4b(st, spy_s, oos, spy_oos)))
        log(f"[B] {pname}: {len(sims)} simulations in {time.time() - t0:.0f}s")

        G = pd.DataFrame([r for r in grid if r["panel"] == pname])
        for book in BOOKS:
            for dial in BOOK_DIALS[book]:
                sub = G[(G.book == book) & (G.dial == dial)]
                if sub.empty:
                    continue
                piv_full = sub.pivot_table(index="value", columns="bps", values="Sharpe")
                piv_is = sub.pivot_table(index="value", columns="bps", values="IS_Sharpe")
                piv_oos = sub.pivot_table(index="value", columns="bps", values="OOS_Sharpe")
                am = {c: piv_full[c].idxmax() for c in RUNGS}
                am_head = {c: am[c] for c in HEADLINE_RUNGS}
                # cost of ignoring the rung: full-sample Sharpe at rung c of the 0-bps winner
                # vs the rung-c winner, evaluated at rung c
                cost = {c: float(piv_full.loc[am[c], c] - piv_full.loc[am[0], c]) for c in RUNGS}
                census.append(dict(
                    panel=pname, book=book, dial=dial, n_arms=len(piv_full),
                    argmax_0=am[0], argmax_10=am[10], argmax_30=am[30],
                    distinct_argmax_headline=len(set(am_head.values())),
                    distinct_argmax_all=len(set(am.values())),
                    rerank_headline=len(set(am_head.values())) > 1,
                    rerank_all=len(set(am.values())) > 1,
                    cost_of_ignoring_rung_10=cost[10], cost_of_ignoring_rung_30=cost[30],
                    max_cost_of_ignoring=max(cost.values()),
                    turn_yr_at_default=float(
                        sub[(sub.value == DEFAULTS[dial]) & (sub.bps == 10)]["turn_yr"].mean()
                        if (sub.value == DEFAULTS[dial]).any() else np.nan),
                    turn_yr_median=float(sub[sub.bps == 10]["turn_yr"].median()),
                ))
                # ---- rule 8: choose on IS only, read OOS once
                for c in RUNGS:
                    pick = piv_is[c].idxmax()
                    pick0 = piv_is[RUNGS[0]].idxmax()
                    default = DEFAULTS[dial] if DEFAULTS[dial] in piv_oos.index else \
                        piv_oos.index[len(piv_oos) // 2]
                    wf.append(dict(
                        panel=pname, book=book, dial=dial, bps=c,
                        IS_pick=pick, IS_pick_at_0bps=pick0, moved=bool(pick != pick0),
                        OOS_pick=float(piv_oos.loc[pick, c]),
                        OOS_pick_at_0bps=float(piv_oos.loc[pick0, c]),
                        OOS_donothing=float(piv_oos.loc[default, c]),
                        OOS_random=float(piv_oos[c].mean()),
                        OOS_oracle=float(piv_oos[c].max()),
                        OOS_rulesv1=base1_oos[c], OOS_rulesv2=base2_oos[c], OOS_SPY=spy_oos,
                        IS_SPY=spy_is,
                        prem_vs_donothing=float(piv_oos.loc[pick, c] - piv_oos.loc[default, c]),
                        prem_vs_random=float(piv_oos.loc[pick, c] - piv_oos[c].mean()),
                        cost_of_0bps_pick=float(piv_oos.loc[pick, c] - piv_oos.loc[pick0, c]),
                    ))
    return (pd.DataFrame(grid), pd.DataFrame(census), pd.DataFrame(wf), pd.DataFrame(ident))


def main():
    t0 = time.time()
    log("=" * 100)
    log("IDEA 234 — re-read-single-rung-argmaxes-on-V1C-shaped-books (lane B)")
    log("p1 = turnover threshold T of the shape test", T_GRID,
        "| p2 = cost rung", RUNGS, "(headline", HEADLINE_RUNGS, ")")
    log("=" * 100)

    log("\n--- PART A: census of published single-rung dial argmaxes ---")
    claims, flagcurve = part_a()
    claims.to_csv(OUT.with_suffix(".claims.csv"), index=False)
    flagcurve.to_csv(OUT.with_suffix(".flagcurve.csv"), index=False)
    log(flagcurve.to_string(index=False))
    if len(claims):
        log(f"\n[A] of {len(claims)} claims, {int(claims.numeric_dial.sum())} sweep a NUMERIC "
            f"dial (n, band, gross, cadence, ...); {int((~claims.numeric_dial).sum())} sweep a "
            f"CATEGORICAL choice (panel, book, arm, family, sleeve) — reported separately "
            f"because Part B can only re-run a numeric dial.")
        log("\n[A] top dial families among claims (numeric dials first):")
        log(claims[claims.numeric_dial].dial.value_counts().head(12).to_string())
        log(claims[~claims.numeric_dial].dial.value_counts().head(8).to_string())
        for leg in ("vol_scaled_LOOSE", "vol_scaled_NAMED"):
            f = claims[claims[leg].fillna(False).astype(bool) & (claims.turn_yr > 20)]
            fn = f[f.numeric_dial]
            log(f"[A] FLAGGED at the queue's own T=20 under {leg}: {len(f)} claims "
                f"in {f.file.nunique()} files ({len(fn)} of them numeric dials); families "
                f"{dict(f.dial.value_counts().head(8))}")
        fl = claims[claims.vol_scaled_NAMED.fillna(False).astype(bool) & (claims.turn_yr > 20)]
        if len(fl):
            log("[A] the flagged files (these are the record's single-rung V1C-shaped "
                "argmaxes at T=20):")
            log(fl.groupby("file").agg(claims=("dial", "size"),
                                       dials=("dial", lambda s: ",".join(sorted(set(s)))),
                                       turn_yr=("turn_yr", "median"),
                                       turn_col=("turn_col", "first"))
                .to_string(float_format=lambda x: f"{x:.1f}"))

    log("\n--- PART B: live re-run at 0/10/30 bps (full ladder reported) ---")
    grid, census, wfd, ident = part_b()
    grid.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    census.to_csv(OUT.with_suffix(".census.csv"), index=False)
    wfd.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    ident.to_csv(OUT.with_suffix(".identity.csv"), index=False)

    log(f"\n[B] grid points reported: {len(grid)}  (all committed to .grid.csv)")
    log("\n[B] per (panel, book, dial) argmax ladder:")
    log(census[["panel", "book", "dial", "argmax_0", "argmax_10", "argmax_30",
                "rerank_headline", "rerank_all", "cost_of_ignoring_rung_10",
                "cost_of_ignoring_rung_30", "turn_yr_median"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    log("\n[B] RE-RANK RATE by book (headline rungs 0/10/30, and the full 0-30 ladder):")
    bb = census.groupby("book").agg(cells=("dial", "size"),
                                    rerank_headline=("rerank_headline", "sum"),
                                    rerank_all=("rerank_all", "sum"),
                                    mean_cost_10=("cost_of_ignoring_rung_10", "mean"),
                                    mean_cost_30=("cost_of_ignoring_rung_30", "mean"),
                                    mean_turn=("turn_yr_median", "mean"))
    log(bb.to_string(float_format=lambda x: f"{x:.4f}"))
    a = int(bb.loc["V1C", "rerank_headline"]); b = int(bb.loc["V1C", "cells"]) - a
    c = int(bb.loc[["TOPN", "EWALL"], "rerank_headline"].sum())
    d = int(bb.loc[["TOPN", "EWALL"], "cells"].sum()) - c
    log(f"[B] V1C {a}/{a + b} cells re-rank across 0/10/30 vs controls {c}/{c + d}; "
        f"Fisher exact two-sided p = {fisher_exact_2x2(a, b, c, d):.4f}")
    # matched pairing: V1C and TOPN sweep the SAME dials on the SAME panels
    m = census[census.book.isin(["V1C", "TOPN"])].pivot_table(
        index=["panel", "dial"], columns="book", values="rerank_headline")
    both = m.dropna()
    n01 = int(((both.V1C == 1) & (both.TOPN == 0)).sum())
    n10 = int(((both.V1C == 0) & (both.TOPN == 1)).sum())
    from math import comb
    nd = n01 + n10
    mcn = float(sum(comb(nd, k) for k in range(0, min(n01, n10) + 1)) / 2 ** nd * 2) if nd else 1.0
    log(f"[B] matched V1C-vs-TOPN pairs (same panel, same dial, same eligible set): "
        f"V1C-only re-ranks {n01}, TOPN-only {n10}, "
        f"both {int(((both.V1C == 1) & (both.TOPN == 1)).sum())}, "
        f"neither {int(((both.V1C == 0) & (both.TOPN == 0)).sum())} of {len(both)}; "
        f"McNemar exact two-sided p = {min(mcn, 1.0):.4f}")
    mc = census[census.book.isin(["V1C", "TOPN"])].pivot_table(
        index=["panel", "dial"], columns="book", values="cost_of_ignoring_rung_10").dropna()
    log(f"[B] matched cost of ignoring the rung at PROTOCOL's own 10 bps: "
        f"V1C {mc.V1C.mean():.4f} vs TOPN {mc.TOPN.mean():.4f} "
        f"(mean paired difference {(mc.V1C - mc.TOPN).mean():+.4f}, "
        f"V1C larger in {int((mc.V1C > mc.TOPN).sum())} of {len(mc)} pairs)")

    log("\n[B] rule 8 (walk-forward) by book x rung — OOS pick vs comparands:")
    w = wfd.groupby(["book", "bps"]).agg(
        cells=("dial", "size"), moved=("moved", "sum"),
        OOS_pick=("OOS_pick", "mean"), OOS_donothing=("OOS_donothing", "mean"),
        OOS_random=("OOS_random", "mean"), OOS_oracle=("OOS_oracle", "mean"),
        prem_vs_donothing=("prem_vs_donothing", "mean"),
        cost_of_0bps_pick=("cost_of_0bps_pick", "mean"),
        OOS_SPY=("OOS_SPY", "mean"), OOS_rulesv2=("OOS_rulesv2", "mean"))
    log(w.to_string(float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP accounting on every grid point
    keep = grid.assign(pass4a=grid.f4a == "", pass4b=grid.f4b == "")
    kk = keep.groupby(["panel", "book", "dial", "bps"]).agg(
        points=("value", "size"), pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"))
    kk.to_csv(OUT.with_suffix(".keep.csv"))
    log(f"\n[KEEP] 4a passes {int(keep.pass4a.sum())} of {len(keep)} grid points; "
        f"4b passes {int(keep.pass4b.sum())} of {len(keep)}")
    at10 = keep[(keep.bps == 10) & keep.pass4b]
    log(f"[KEEP] at PROTOCOL's own 10 bps: 4b passes {len(at10)} of "
        f"{int((keep.bps == 10).sum())}; by panel {dict(at10.panel.value_counts())}")
    if len(at10):
        xp = at10.groupby(["book", "dial", "value"]).panel.nunique()
        log(f"[KEEP] 4b passers at 10 bps holding on >1 panel: {int((xp > 1).sum())} of {len(xp)}"
            " — a single-panel 4b pass is a PARK under the record's standing convention.")
    if keep.pass4b.any():
        log("[KEEP] 4b passers:")
        log(keep[keep.pass4b][["panel", "book", "dial", "value", "bps", "CAGR", "Sharpe",
                               "MaxDD", "H1", "H2", "OOS_Sharpe", "turn_yr"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    if keep.pass4a.any():
        log("[KEEP] 4a passers (top 20 by Sharpe):")
        log(keep[keep.pass4a].nlargest(20, "Sharpe")
            [["panel", "book", "dial", "value", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
              "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    log(f"\ntotal runtime {time.time() - t0:.0f}s")
    OUT.with_suffix(".console.txt").write_text("\n".join(_log_lines) + "\n")


if __name__ == "__main__":
    main()
