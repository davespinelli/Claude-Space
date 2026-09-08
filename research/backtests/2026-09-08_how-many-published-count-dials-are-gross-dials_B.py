#!/usr/bin/env python3
"""Idea 244 - "how-many-published-count-dials-are-gross-dials" (lane B, 2026-09-08).

The question
------------
Idea 240 found that idea 73's FIXED `GROSS/n` weight silently de-grosses a wide book: on
U56 the realised gross at n=60 is 0.474 against 0.721 at n=20, because the panel cannot
supply 60 eligible names in most weeks and the unfilled slots go to cash.  So a sweep
labelled "position count" is, under that convention, partly a GROSS ladder wearing an `n`
label, and idea 240 reported that closing the channel halves the width premium and flips
two cells.

QUEUE 244 asks for the record-wide version:

    Q1 (CENSUS, the deliverable): census every count / position-number sweep in the
       committed record for the same construction.  Which weighting convention does each
       sweep's parent script actually use, and how much realised gross does the sweep
       therefore move across its own grid?  How many published count findings are
       gross-ladder points?
    Q2 (RE-QUOTE): re-price the record's count grid at MATCHED REALISED GROSS -- the same
       book, scaled so its realised gross equals the FIXED point's at every n -- and
       report what survives: does the width curve keep its sign, its argmax, its 4a/4b
       pass counts?
    Q3 (RULE 8): does an IS-chosen count dial survive out of sample once the gross
       channel is closed, against RULES v2, SPY and doing nothing?

Definitions, pre-registered here before any number was read
-----------------------------------------------------------
Three weighting conventions the record actually uses:

    FIXEDTOT   w = GROSS / n on the top-n names            (idea 73's / idea 240's FIXED)
               gross = GROSS * E[n_held]/n  -> FALLS as n outruns supply
    FIXEDW     w = W_FIXED (0.15) per name, top-n          (RULES v1's construction)
               gross = W_FIXED * E[n_held] -> RISES ~linearly in n
    NORM       w = GROSS / n_held                          (gross channel closed)
               gross = GROSS whenever the book is non-empty

where n_held(t) = #{names the top-n book actually holds at t} <= min(n, n_elig(t)).  The
count is n_held and NOT n_elig: a name can pass the eligibility gate and still be
unrankable (no 252-day history yet), and using n_elig makes the FIXED/NORM identity below
inexact by up to a full position weight.  This run uses n_held everywhere.

The identity that organises the whole run, checked numerically in the harness:

        FIXEDTOT(n) == NORM(n) * phi_t,   phi_t = n_held(t) / n

i.e. idea 73's convention is EXACTLY the equal-weighted width book multiplied by a
BREADTH-TIMED exposure overlay.  So a count sweep under it moves two things at once: the
book's width, and a market-timing overlay that de-grosses precisely when few names pass
the trend gate.  The MATCHED control below removes that overlay's LEVEL and leaves its
TIMING, which separates the two.

FIXEDTOT and NORM are backtested on every live grid point.  FIXEDW is NOT backtested past
n=5: at w=0.15 its target gross is 0.15*n, so n=10 is 150% and n=60 is 900% of NAV, which
PROTOCOL rule 2 bars ("no leverage unless the idea says so") and which the engine turns
into a negative equity path rather than a result.  It is therefore carried as an ANALYTIC
census label with its gross curve computed exactly (it is a closed form in n_held), and
the number of published count cells whose implied gross exceeds 1.0 under it
is reported as its own statistic.  Declaring this here, before the census was read, is
the honest handling: the arm is barred by the protocol, not dropped because it looked bad.

    MATCHED    the idea-244 control: the NORM book scaled by a single scalar per (panel,
               n) cell so that its MEAN realised gross equals that cell's FIXEDTOT book's
               mean realised gross.  One scalar, computed on the FULL sample for the
               full-sample table and on the IS window only for the rule-8 arm (stated at
               each use).  This is the "re-quote at matched realised gross" the queue asks
               for: it holds gross at the FIXED convention's own realised level while
               restoring an equal-weighted book, so any difference left across n is
               width, not exposure.

    REALISED GROSS g(cell) = mean over the evaluated sample of the daily HELD gross
    (`engine.backtest`'s `weights` frame row-sum), i.e. after drift, not the target.
    TARGET GROSS is the same quantity before drift, averaged over rebalance dates only;
    it is the census's measure (it is defined at any n, including the levered FIXEDW
    cells that cannot be simulated) and the two are printed side by side on every live
    cell so the substitution is auditable rather than assumed.

    GROSS-LADDER POINT (pre-registered, absolute): a published count sweep whose realised
    gross SPAN across its own quoted grid, on its own mapped panel, is >= 0.05 of NAV
    (5 pp).  A relative criterion (span / mean realised gross >= 0.10) is reported beside
    it, and the FULL span distribution is published in `.census.csv`, so any other
    threshold can be read off the table rather than taken on trust.

Census scope and its honest limits
----------------------------------
The census is MECHANICAL.  Every committed CSV in research/backtests/ is scanned with
idea 242's published filter, verbatim, so the two censuses are comparable: a count column
(`n`, `top_n`, `n_names`, `npos`, `count`, ...) with >= 3 distinct integer values inside
[2, 500], sitting beside a Sharpe column, from a parent script that actually ranks on a
count.  Every rejection is logged with its reason in `.census_rejects.csv`.

Convention labelling is the new step and it is fallible, so it is reported as a
three-valued label with its evidence:
    - if the CSV itself carries a convention column (conv / convention / weighting /
      wconv / norm), that value is AUTHORITATIVE for the rows carrying it;
    - else the parent script's source is matched against pre-registered patterns for the
      three constructions, and the matched literal is written into the census row;
    - if neither fires, or if both a FIXED and a NORM pattern fire with no column to
      separate them, the cell is labelled UNKNOWN or MIXED and is COUNTED AS SUCH in
      every denominator.  UNKNOWN cells are never quietly assigned to a convention.

Panels are mapped by name exactly as idea 242 mapped them; unmappable panels are reported
as `unmapped` and excluded from the gross-span statistics (they cannot be re-priced), but
they remain in the convention counts.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (7)     2. n (6 values)
Convention is a reported CONTROL carried on every point (all live arms, always) plus the
MATCHED control -- not a third tuned dial.  Cost rung (10 / 25 bps) is a reporting axis;
both are derived from the same held/turnover paths, so they are not a fitted choice.
Live grid = 7 panels x 6 n x 3 arms (FIXEDTOT, NORM, MATCHED) = 126 points,
+ 7 EWall + 7 RULES v1 + 7 RULES v2 + 7 SPY references = 154, ALL in `.grid.csv`.

Walk-forward (PROTOCOL rule 8) -- arms and directions fixed before any OOS number
    IS = 2009-2016 (through 2016-12-31), OOS = 2017-2026, read once.
    ISARGMAX-FIXEDTOT  n = argmax IS Sharpe under FIXEDTOT   (the dial as published)
    ISARGMAX-NORM      n = argmax IS Sharpe under NORM       (channel closed)
    ISARGMAX-MATCHED   n = argmax IS Sharpe under MATCHED, scalar fitted on IS ONLY
    NOTHING            RULES v2 on the same panel            (do-nothing incumbent)
    EWALL              the un-ranked equal-weight book       (no count dial at all)
    SPY                buy and hold
    Reported per panel and pooled equal-weight over panels, at both cost rungs, with OOS
    CAGR / Sharpe / MaxDD for every arm.

Verdicts (both KEEP paths, every live point, PROTOCOL rule 4)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: every panel is CURRENT constituents, one-directional, hardest on STK20 /
BSTK100 / SMALL.  Widening n on a survivor list adds names known ex post to have
survived, so any "wider is better" reading is partly manufactured here -- which is
exactly why this run's headline is a CONVENTION statistic (gross span), not a width
verdict.  The census additionally inherits the bias of every parent script it reads.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST_RUNGS = (10, 25)
COST_BPS = 10                      # PROTOCOL rung for every headline
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [5, 10, 20, 30, 40, 60]
ARMS = ("FIXEDTOT", "NORM", "MATCHED")     # FIXEDW is analytic-only (levered past n=5)
MAX_GROSS = 1.0                            # PROTOCOL rule 2: no leverage
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SPAN_ABS = 0.05                    # pre-registered gross-ladder threshold (NAV)
SPAN_REL = 0.10                    # pre-registered relative companion
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


# ---------------------------------------------------------------- panels (idea 240/242, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    broad_g = [t for t in U["broad"] if t not in crypto]
    sect_g = [t for t in U["sectors"] if t not in crypto]
    bfc_g = [t for t in U["bonds_fx_commod"] if t not in crypto]
    stk_g = [t for t in U["megacap"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep_small = [c for c in pxs.columns if c == "SPY" or c not in bad]
    dropped = pxs.shape[1] - len(keep_small)
    pxs = pxs[keep_small]

    etf36 = broad_g + sect_g + bfc_g
    etf24 = broad_g + sect_g
    b_stk = [t for t in px136.columns if t not in set(etf36)]
    s_stk = [c for c in pxs.columns if c != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    panels = {
        "U56":     sub(px56, list(px56.columns)),
        "ETF36":   sub(px56, etf36),
        "ETF24":   sub(px56, etf24),
        "STK20":   sub(px56, stk_g, tradable=stk_g),
        "B136":    sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL":   sub(pxs, s_stk, tradable=s_stk),
    }
    return panels, dropped


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def sel_frame(px, elig, n):
    """top-n selection indicator under the v1 composite (vol_scale off, idea 240's)."""
    s = score(px, vol_scale=False)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float)


def weights_for(px, elig, n, arm, scale=1.0):
    sel = sel_frame(px, elig, n)
    if arm == "FIXEDTOT":
        return sel * (GROSS / n)
    if arm == "FIXEDW":
        return sel * W_FIXED
    held = sel.sum(axis=1).replace(0, np.nan)
    norm = sel.div(held, axis=0).mul(GROSS).fillna(0.0)
    return norm * scale                       # NORM (scale 1.0) or MATCHED (scale != 1)


def rank_on_rebal(px, elig):
    """The eligibility-masked composite RANK frame, restricted to weekly rebalance dates
    after the 260-day warm-up.  `(rank <= n).sum(axis=1)` is then the exact number of
    names a top-n book actually HOLDS -- which is <= n_elig, because a name can pass the
    gate and still be unrankable (no 252-day history yet).  Using n_elig here instead is
    the slip that makes the FIXED/NORM identity inexact, so it is not used."""
    s = score(px, vol_scale=False)[0]
    rk = s.where(elig).rank(axis=1, ascending=False)
    mask = rebalance_mask(px.index, FREQ)
    return rk[mask.values].loc[px.index[260]:]


def held_count(rk, n):
    return (rk <= n).sum(axis=1)


def target_gross(rk, n, conv):
    """Mean TARGET gross of a top-n book under each convention, exactly.  Defined at any
    n, levered or not, so it is the census's measure (the levered FIXEDW cells cannot be
    simulated).  Held gross -- the same quantity after drift -- is printed beside it on
    every live cell."""
    filled = held_count(rk, n)
    if conv == "FIXEDTOT":
        return float((filled * (GROSS / n)).mean())
    if conv == "FIXEDW":
        return float((filled * W_FIXED).mean())
    if conv == "NORM":
        return float((GROSS * (filled > 0)).mean())
    return np.nan


def ewall_weights(px, elig):
    cnt = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


# ---------------------------------------------------------------- run cache (cost-free paths)
def run(px, w, freq=FREQ):
    """One backtest -> gross return path, turnover and held gross. Cost is applied
    afterwards because engine.backtest's held/turnover paths do not depend on cost_bps."""
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    gross_ret = res["returns"]                       # cost_bps=0 -> pure held*rets
    return dict(gret=gross_ret, turn=res["turnover"], hg=res["weights"].sum(axis=1))


def net(r, bps):
    return r["gret"] - r["turn"] * bps / 1e4


def half_sharpes(x):
    h = len(x) // 2
    return metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"]


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r)
    s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def fail_4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan, int(ok.sum())
    xr = pd.Series(x[ok]).rank().values
    yr = pd.Series(y[ok]).rank().values
    if xr.std() == 0 or yr.std() == 0:
        return np.nan, int(ok.sum())
    return float(np.corrcoef(xr, yr)[0, 1]), int(ok.sum())


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- census over the committed record
COUNT_COLS = ("n", "top_n", "topn", "n_names", "npos", "n_pos", "count", "nn")
PANEL_COLS = ("panel", "universe", "corpus", "book", "panel_name", "uni")
SHARPE_COLS = ("Sharpe", "OOS_Sharpe", "IS_Sharpe", "mean_OOS_Sharpe")
CONV_COLS = ("conv", "convention", "weighting", "wconv", "norm", "gross_conv", "weight_conv")
PANEL_MAP = {
    "u56": "U56", "universe.json": "U56", "universe": "U56", "56": "U56", "etf56": "U56",
    "etf36": "ETF36", "etf24": "ETF24", "stk20": "STK20", "megacap": "STK20", "mega": "STK20",
    "b136": "B136", "broad": "B136", "universe_broad.json": "B136", "broad136": "B136",
    "b100": "BSTK100", "bstk100": "BSTK100", "bstk": "BSTK100",
    "small": "SMALL", "small484": "SMALL", "small483": "SMALL", "small439": "SMALL",
    "small485": "SMALL", "smallcap": "SMALL",
}
RANK_PAT = re.compile(r"rank\s*\(|rank\s*<=|nlargest|argsort|<=\s*n\b|top[_ ]?n", re.I)

# pre-registered convention patterns, matched against the PARENT SCRIPT source
PAT_FIXEDTOT = re.compile(r"GROSS\s*/\s*n\b|gross\s*/\s*n\b|/\s*n\s*\)\s*$|GROSS\s*/\s*float\(\s*n", re.M)
PAT_FIXEDW = re.compile(r"\*\s*W_FIXED\b|\*\s*0\.15\b|w\s*=\s*0\.15\b|W\s*=\s*0\.15\b")
PAT_NORM = re.compile(r"div\(\s*held|div\(\s*cnt|div\(\s*n_?held|sum\(axis=1\)\s*\)?\s*,\s*axis=0|"
                      r"GROSS\s*/\s*min\(|div\(\s*sel\.sum")
CONV_VALUE_MAP = {
    "fixed": "FIXEDTOT", "fixedtot": "FIXEDTOT", "fix": "FIXEDTOT", "gross/n": "FIXEDTOT",
    "norm": "NORM", "normalised": "NORM", "normalized": "NORM", "ew": "NORM", "equal": "NORM",
    "fixedw": "FIXEDW", "w015": "FIXEDW", "v1": "FIXEDW",
}


def script_for(csv_path):
    stem = csv_path.name.split(".")[0]
    p = csv_path.parent / f"{stem}.py"
    return p if p.exists() else None


def label_convention(src, conv_val):
    """Return (label, evidence). Column value wins; else source patterns; else UNKNOWN."""
    if conv_val is not None:
        key = str(conv_val).strip().lower().replace("-", "").replace("_", "").replace(" ", "")
        if key in CONV_VALUE_MAP:
            return CONV_VALUE_MAP[key], f"column:{conv_val}"
    hits = []
    if PAT_FIXEDTOT.search(src): hits.append("FIXEDTOT")
    if PAT_FIXEDW.search(src): hits.append("FIXEDW")
    if PAT_NORM.search(src): hits.append("NORM")
    if len(hits) == 1:
        return hits[0], "source:" + hits[0]
    if len(hits) > 1:
        return "MIXED", "source:" + "+".join(hits)
    return "UNKNOWN", "no pattern"


def census():
    cells, rejects = [], []
    src_cache = {}
    files_scanned = 0
    for f in sorted(OUT.glob("*.csv")):
        if f.name.startswith(STEM):
            continue
        files_scanned += 1
        try:
            df = pd.read_csv(f)
        except Exception as e:
            rejects.append(dict(file=f.name, col="", reason=f"unreadable:{type(e).__name__}"))
            continue
        if df.empty:
            rejects.append(dict(file=f.name, col="", reason="empty"))
            continue
        ccols = [c for c in df.columns if c in COUNT_COLS]
        if not ccols:
            continue
        scols = [c for c in df.columns if c in SHARPE_COLS]
        sp = script_for(f)
        if sp is None:
            rejects.append(dict(file=f.name, col=",".join(ccols), reason="no parent script"))
            continue
        if sp not in src_cache:
            src_cache[sp] = sp.read_text(errors="ignore")
        src = src_cache[sp]
        ranks = bool(RANK_PAT.search(src))
        convcol = next((c for c in CONV_COLS if c in df.columns), None)
        for c in ccols:
            v = pd.to_numeric(df[c], errors="coerce").dropna()
            uv = sorted(set(v.astype(int))) if len(v) and (v % 1 == 0).all() else []
            if len(uv) < 3:
                rejects.append(dict(file=f.name, col=c, reason=f"<3 distinct int values ({len(uv)})"))
                continue
            if min(uv) < 2 or max(uv) > 500:
                rejects.append(dict(file=f.name, col=c, reason=f"range {min(uv)}..{max(uv)} outside [2,500]"))
                continue
            if not scols:
                rejects.append(dict(file=f.name, col=c, reason="no Sharpe column beside it"))
                continue
            if not ranks:
                rejects.append(dict(file=f.name, col=c, reason="parent script never ranks on a count"))
                continue
            pcol = next((p for p in PANEL_COLS if p in df.columns), None)
            gcols = [x for x in (pcol, convcol) if x]
            groups = df.groupby([df[x].astype(str) for x in gcols]) if gcols else [((), df)]
            for gkey, g in groups:
                gkey = gkey if isinstance(gkey, tuple) else (gkey,)
                gmap = dict(zip(gcols, gkey))
                praw = gmap.get(pcol, "(all)") if pcol else "(all)"
                cval = gmap.get(convcol) if convcol else None
                key = str(praw).strip().lower().replace("-", "").replace("_", "")
                pk = PANEL_MAP.get(key, "")
                conv, ev = label_convention(src, cval)
                for scol in scols:
                    gg = g[[c, scol]].apply(pd.to_numeric, errors="coerce").dropna()
                    if gg.empty or gg[c].nunique() < 3:
                        continue
                    grid = sorted(set(gg[c].astype(int)))
                    best = gg.loc[gg[scol].idxmax()]
                    cells.append(dict(file=f.name, count_col=c, sharpe_col=scol,
                                      panel_raw=str(praw), panel=pk if pk else "unmapped",
                                      conv=conv, conv_evidence=ev,
                                      n_grid=len(grid), n_min=int(min(grid)), n_max=int(max(grid)),
                                      n_argmax=int(best[c]), sharpe_at_argmax=float(best[scol])))
    return pd.DataFrame(cells), pd.DataFrame(rejects), files_scanned


# ---------------------------------------------------------------- main
def main():
    panels, small_dropped = build_panels()
    print("=" * 190)
    print(f"Idea 244 how-many-published-count-dials-are-gross-dials (lane B) | {SCRIPT} | "
          f"{COST_BPS} bps headline (+25 bps rung), weekly, next-day execution")
    print("=" * 190)

    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
    print(f"small panel hygiene: dropped {small_dropped} tickers with max_1d_move >= 1.0; "
          f"{len(panels['SMALL'][1])} tradable remain")

    # ============================================================ HARNESS CHECK
    print("\n" + "-" * 190)
    print("HARNESS: reproduce the live book and idea 240's construction before anything is claimed")
    print("-" * 190)
    start56 = px56.index[260]
    ref = backtest(px56, rules_v1_weights(px56), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[start56:]
    mine = net(run(px56, rules_v1_weights(px56)), COST_BPS).loc[start56:]
    print(f"cost-free-path reconstruction of RULES v1 vs engine.backtest(cost_bps=10): "
          f"max|diff| {float((ref - mine).abs().max()):.3e}  (must be ~0)")
    e56 = eligible_mask(*panels["U56"])
    ref240 = OUT / "2026-09-06_is-n20-a-constant-or-a-grid-edge_C.grid.csv"
    pub = pd.read_csv(ref240).query("panel == 'U56' and conv == 'FIXED'").set_index("n")["mean_gross"] \
        if ref240.exists() else pd.Series(dtype=float)
    rk56 = rank_on_rebal(px56, e56)
    for n in NS:
        hg = run(px56, weights_for(px56, e56, n, "FIXEDTOT"))["hg"].loc[start56:].mean()
        tg = target_gross(rk56, n, "FIXEDTOT")
        p = pub.get(n, np.nan)
        print(f"idea 240 replication  U56 FIXEDTOT n={n:>2}: held gross {hg:.3f}  target gross {tg:.3f}  "
              f"published (idea 240 .grid.csv) {p:.3f}  diff(target-published) {tg - p:+.4f}")
    print("  [idea 240 evaluates all seven panels on ONE common window starting 2011-01-13; this run "
          "uses each panel's own index[260]. That window difference, not the construction, is the residual.]")

    # the identity the whole run turns on: FIXEDTOT is the NORM book times a BREADTH factor
    print("\nIDENTITY CHECK  FIXEDTOT(n) == NORM(n) * phi_t,  phi_t = n_held_t / n   (max |weight diff|)")
    s56 = score(px56, vol_scale=False)[0].where(e56).rank(axis=1, ascending=False)
    for n in NS:
        wf = weights_for(px56, e56, n, "FIXEDTOT")
        wn = weights_for(px56, e56, n, "NORM")
        phi = (s56 <= n).sum(axis=1) / n
        d = float((wf - wn.mul(phi, axis=0)).abs().max().max())
        print(f"  n={n:>2}: {d:.3e}   mean phi {float(phi.loc[start56:].mean()):.3f}   "
              f"sd phi {float(phi.loc[start56:].std()):.3f}   "
              f"corr(phi, SPY 20d fwd ret) {float(pd.Series(phi).loc[start56:].corr(px56['SPY'].pct_change(20).shift(-20).loc[start56:])):+.3f}")
    print("  => the FIXED convention is NOT a static gross ladder: it is the width book times a")
    print("     BREADTH-TIMED exposure overlay whose MEAN the MATCHED control removes and whose")
    print("     TIMING it does not. Level and timing are separated at every (panel, n) below.")

    # ============================================================ (1) CENSUS
    print("\n" + "=" * 190)
    print("Q1  CENSUS - every count/position sweep in the committed record, labelled by weighting convention")
    print("=" * 190)
    cen, rej, nfiles = census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    rej.to_csv(OUT / f"{STEM}.census_rejects.csv", index=False)
    print(f"CSV files scanned: {nfiles}   qualifying count-sweep cells: {len(cen)}   "
          f"distinct files contributing: {cen['file'].nunique() if len(cen) else 0}")
    print(f"rejections logged: {len(rej)} (reasons in .census_rejects.csv)")
    if len(rej):
        print(rej.groupby("reason").size().sort_values(ascending=False).head(12).to_string())
    print("\nconvention label counts (UNKNOWN/MIXED are counted, never assigned):")
    print(cen.groupby("conv").size().sort_values(ascending=False).to_string())
    print("\nconvention x panel-mappability:")
    print(pd.crosstab(cen["conv"], cen["panel"] == "unmapped").rename(columns={False: "mapped", True: "unmapped"}).to_string())

    # ============================================================ (2) live grid
    print("\n" + "=" * 190)
    print("Q2  THE GRID - 7 panels x n in {5,10,20,30,40,60} x 3 live arms (FIXEDTOT, NORM, MATCHED), every point reported")
    print("=" * 190)
    grid_rows, curves = [], {}
    wf_rows = []
    for pk, (px, trad) in panels.items():
        elig = eligible_mask(px, trad)
        start = px.index[260]
        rkp = rank_on_rebal(px, elig)
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos = spy.loc[OOS_START:]
        base_r = run(px, rules_v2_weights(px))
        v1_r = run(px, rules_v1_weights(px))
        ew_r = run(px, ewall_weights(px, elig))
        is_mask = lambda s: s.loc[:IS_END]

        # realised gross of each FIXED cell -> the MATCHED scalar (full sample and IS-only)
        cache = {}
        for n in NS:
            for arm in ("FIXEDTOT", "NORM"):
                cache[(n, arm)] = run(px, weights_for(px, elig, n, arm))
        for n in NS:
            g_norm_full = cache[(n, "NORM")]["hg"].loc[start:].mean()
            g_fix_full = cache[(n, "FIXEDTOT")]["hg"].loc[start:].mean()
            g_norm_is = cache[(n, "NORM")]["hg"].loc[start:IS_END].mean()
            g_fix_is = cache[(n, "FIXEDTOT")]["hg"].loc[start:IS_END].mean()
            cache[(n, "MATCHED")] = run(px, weights_for(px, elig, n, "MATCHED",
                                                        scale=g_fix_full / g_norm_full))
            cache[(n, "MATCHED_IS")] = run(px, weights_for(px, elig, n, "MATCHED",
                                                           scale=g_fix_is / g_norm_is))

        for bps in COST_RUNGS:
            b = net(base_r, bps).loc[start:]
            for n in NS:
                for arm in ARMS:
                    rr = cache[(n, arm)]
                    r = net(rr, bps).loc[start:]
                    m = metrics(r)
                    h1, h2 = half_sharpes(r)
                    r_oos = r.loc[OOS_START:]
                    mo = metrics(r_oos)
                    row = dict(panel=pk, n=n, arm=arm, cost_bps=bps,
                               realised_gross=float(rr["hg"].loc[start:].mean()),
                               target_gross=target_gross(rkp, n, "FIXEDTOT" if arm == "FIXEDTOT" else "NORM"),
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               H1=h1, H2=h2, OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                               OOS_MaxDD=mo["MaxDD"],
                               turnover_yr=float(rr["turn"].loc[start:].sum() / m["Years"]),
                               fail_4a=fail_4a(r, b), fail_4b=fail_4b(r, spy, r_oos, spy_oos))

                    row["pass_4a"] = row["fail_4a"] == "-"
                    row["pass_4b"] = row["fail_4b"] == "-"
                    grid_rows.append(row)
            for nm, rr in (("EWall", ew_r), ("RULESv1", v1_r), ("RULESv2", base_r)):
                r = net(rr, bps).loc[start:]
                m = metrics(r); h1, h2 = half_sharpes(r); r_oos = r.loc[OOS_START:]; mo = metrics(r_oos)
                grid_rows.append(dict(panel=pk, n=np.nan, arm=nm, cost_bps=bps,
                                      realised_gross=float(rr["hg"].loc[start:].mean()),
                                      CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                                      OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                      turnover_yr=float(rr["turn"].loc[start:].sum() / m["Years"]),
                                      fail_4a=fail_4a(r, b), fail_4b=fail_4b(r, spy, r_oos, spy_oos),
                                      pass_4a=fail_4a(r, b) == "-", pass_4b=fail_4b(r, spy, r_oos, spy_oos) == "-"))
            spy_m = metrics(spy); sh1, sh2 = half_sharpes(spy); spy_mo = metrics(spy_oos)
            grid_rows.append(dict(panel=pk, n=np.nan, arm="SPY", cost_bps=bps, realised_gross=1.0,
                                  CAGR=spy_m["CAGR"], Sharpe=spy_m["Sharpe"], MaxDD=spy_m["MaxDD"],
                                  H1=sh1, H2=sh2, OOS_CAGR=spy_mo["CAGR"], OOS_Sharpe=spy_mo["Sharpe"],
                                  OOS_MaxDD=spy_mo["MaxDD"], turnover_yr=0.0, fail_4a="n/a", fail_4b="n/a",
                                  pass_4a=False, pass_4b=False))

        # ---- rule 8: IS pick per arm, OOS read once (both rungs)
        for bps in COST_RUNGS:
            picks = {}
            for arm in ("FIXEDTOT", "NORM", "MATCHED_IS"):
                iss = {n: metrics(net(cache[(n, arm)], bps).loc[start:IS_END])["Sharpe"] for n in NS}
                nbest = max(iss, key=iss.get)
                picks[arm] = (nbest, iss[nbest])
            for arm, (nbest, is_sh) in picks.items():
                r_oos = net(cache[(nbest, arm)], bps).loc[OOS_START:]
                mo = metrics(r_oos)
                wf_rows.append(dict(panel=pk, cost_bps=bps, arm="ISARGMAX-" + arm.replace("_IS", ""),
                                    n_pick=nbest, IS_Sharpe=is_sh,
                                    realised_gross=float(cache[(nbest, arm)]["hg"].loc[OOS_START:].mean()),
                                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
            for nm, rr in (("NOTHING(RULESv2)", base_r), ("EWALL", ew_r), ("RULESv1", v1_r)):
                r_oos = net(rr, bps).loc[OOS_START:]
                mo = metrics(r_oos)
                wf_rows.append(dict(panel=pk, cost_bps=bps, arm=nm, n_pick=np.nan, IS_Sharpe=np.nan,
                                    realised_gross=float(rr["hg"].loc[OOS_START:].mean()),
                                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
            so = metrics(spy_oos)
            wf_rows.append(dict(panel=pk, cost_bps=bps, arm="SPY", n_pick=np.nan, IS_Sharpe=np.nan,
                                realised_gross=1.0, OOS_CAGR=so["CAGR"], OOS_Sharpe=so["Sharpe"],
                                OOS_MaxDD=so["MaxDD"]))
        print(f"  panel {pk:<8} done ({len(NS) * len(ARMS)} live points)")

    G = pd.DataFrame(grid_rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    W = pd.DataFrame(wf_rows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    live = G[G["arm"].isin(ARMS) & (G["cost_bps"] == COST_BPS)]
    print(f"\nlive points at {COST_BPS} bps: {len(live)}  (+ {len(G[(G.cost_bps == COST_BPS) & ~G.arm.isin(ARMS)])} reference rows)")

    # ---- the gross channel, measured
    print("\n" + "-" * 190)
    print("THE CHANNEL: realised gross across the count grid, by panel and convention (mean held gross)")
    print("-" * 190)
    piv = live.pivot_table(index=["panel", "arm"], columns="n", values="realised_gross")
    piv["SPAN"] = piv.max(axis=1) - piv.min(axis=1)
    piv["REL"] = piv["SPAN"] / piv[NS].mean(axis=1)
    print(fmt(piv))
    span_by_arm = piv.reset_index().groupby("arm")[["SPAN", "REL"]].agg(["min", "median", "max"])
    print("\ngross span by convention over the 7 panels:")
    print(fmt(span_by_arm))
    piv.reset_index().to_csv(OUT / f"{STEM}.gross.csv", index=False)

    # ---- census x channel: how many published count findings are gross-ladder points
    print("\n" + "=" * 190)
    print("Q1 ANSWER - how many published count findings are GROSS-LADDER points")
    print(f"(pre-registered: realised-gross span across the cell's OWN quoted grid >= {SPAN_ABS:.2f} NAV; "
          f"relative companion span/mean >= {SPAN_REL:.2f})")
    print("=" * 190)
    ne_map = {pk: rank_on_rebal(px, eligible_mask(px, trad)) for pk, (px, trad) in panels.items()}

    span_rows = []
    for _, c in cen.iterrows():
        if c["panel"] == "unmapped" or c["conv"] in ("UNKNOWN", "MIXED"):
            span_rows.append(dict(**c, g_lo=np.nan, g_hi=np.nan, gross_span=np.nan,
                                  gross_span_rel=np.nan, max_gross=np.nan, levered=False,
                                  ladder=("UNKNOWN" if c["conv"] in ("UNKNOWN", "MIXED") else "UNMAPPED")))
            continue
        ne = ne_map[c["panel"]]
        g_lo = target_gross(ne, int(c["n_min"]), c["conv"])
        g_hi = target_gross(ne, int(c["n_max"]), c["conv"])
        span = abs(g_hi - g_lo)
        mid = (g_hi + g_lo) / 2
        rel = span / mid if mid > 0 else np.nan
        gmax = max(g_lo, g_hi)
        span_rows.append(dict(**c, g_lo=g_lo, g_hi=g_hi, gross_span=span, gross_span_rel=rel,
                              max_gross=gmax, levered=bool(gmax > MAX_GROSS + 1e-9),
                              ladder=("LADDER" if span >= SPAN_ABS else "FLAT")))
    S = pd.DataFrame(span_rows)
    S.to_csv(OUT / f"{STEM}.census.csv", index=False)
    print(S.groupby("ladder").size().sort_values(ascending=False).to_string())
    prc = S.groupby(["conv", "ladder"]).size().unstack(fill_value=0)
    print("\nby convention:")
    print(prc.to_string())
    dec = S[S["ladder"].isin(["LADDER", "FLAT"])]
    if len(dec):
        n_lad = int((dec["ladder"] == "LADDER").sum())
        print(f"\nDECIDABLE cells (mapped panel AND known convention): {len(dec)} of {len(S)} "
              f"({len(dec)/len(S):.1%} coverage)")
        print(f"  GROSS-LADDER points (span >= {SPAN_ABS}): {n_lad} of {len(dec)} = {n_lad/len(dec):.1%}")
        n_rel = int((dec["gross_span_rel"] >= SPAN_REL).sum())
        print(f"  relative criterion (span/mean >= {SPAN_REL}): {n_rel} of {len(dec)} = {n_rel/len(dec):.1%}")
        print(f"  span distribution over decidable cells: min {dec['gross_span'].min():.3f} "
              f"p25 {dec['gross_span'].quantile(.25):.3f} median {dec['gross_span'].median():.3f} "
              f"p75 {dec['gross_span'].quantile(.75):.3f} max {dec['gross_span'].max():.3f}")
        print(f"  distinct FILES carrying at least one ladder cell: "
              f"{dec.loc[dec['ladder'] == 'LADDER', 'file'].nunique()} of {dec['file'].nunique()}")
        print(f"  cells whose grid top implies gross > {MAX_GROSS:.2f} of NAV (leverage, PROTOCOL rule 2): "
              f"{int(dec['levered'].sum())} of {len(dec)}; max implied gross {dec['max_gross'].max():.2f}")
        print("\n  ladder rate by convention and panel (decidable cells only):")
        print(pd.crosstab([dec["conv"], dec["panel"]], dec["ladder"]).to_string())
        print("\n  the 12 largest gross spans in the record:")
        print(fmt(dec.nlargest(12, "gross_span")[["file", "panel", "conv", "n_min", "n_max",
                                                  "g_lo", "g_hi", "gross_span", "n_argmax"]]))
    print(f"\nCOVERAGE LIMIT (published, not hidden): "
          f"{int((S['ladder'] == 'UNKNOWN').sum())} cells label-UNKNOWN/MIXED, "
          f"{int((S['ladder'] == 'UNMAPPED').sum())} cells on an unmappable panel.")

    # ---- deduplicated view: one row per (file, count column, panel, convention) SWEEP
    keyc = ["file", "count_col", "panel", "conv"]
    Sw = S.drop_duplicates(subset=keyc + ["n_min", "n_max"])
    decw = Sw[Sw["ladder"].isin(["LADDER", "FLAT"])]
    print(f"\nDEDUPLICATED (one row per file x count-column x panel x convention SWEEP, not per Sharpe column): "
          f"{len(Sw)} sweeps, {len(decw)} decidable, "
          f"{int((decw['ladder'] == 'LADDER').sum())} gross ladders "
          f"({(decw['ladder'] == 'LADDER').mean():.1%} of decidable)")

    # ---- bounds for the undecidable cells: what WOULD they be under each candidate label
    und = S[(S["ladder"] == "UNKNOWN") & (S["panel"] != "unmapped")].copy()
    if len(und):
        wl = []
        for _, c in und.iterrows():
            ne = ne_map[c["panel"]]
            row = {}
            for cand in ("FIXEDTOT", "NORM"):
                row[cand] = abs(target_gross(ne, int(c["n_max"]), cand)
                                - target_gross(ne, int(c["n_min"]), cand)) >= SPAN_ABS
            wl.append(row)
        WL = pd.DataFrame(wl)
        lo = int((dec["ladder"] == "LADDER").sum())
        hi = lo + int(WL["FIXEDTOT"].sum())
        den_lo, den_hi = len(dec), len(dec) + len(und)
        print(f"\nBOUNDS on the record-wide ladder rate, carrying the undecidable cells explicitly:")
        print(f"  {len(und)} label-UNKNOWN/MIXED cells sit on a MAPPABLE panel; under a FIXEDTOT reading "
              f"{int(WL['FIXEDTOT'].sum())} of them would be ladders, under NORM {int(WL['NORM'].sum())}.")
        print(f"  LOWER bound (undecidables all FLAT/NORM): {lo}/{den_hi} = {lo/den_hi:.1%}")
        print(f"  POINT estimate on decidable cells only:   {lo}/{den_lo} = {lo/den_lo:.1%}")
        print(f"  UPPER bound (undecidables all FIXEDTOT):  {hi}/{den_hi} = {hi/den_hi:.1%}")

    # ---- Q2: what the re-quote does to the width reading
    print("\n" + "=" * 190)
    print("Q2 ANSWER - the width curve re-quoted at MATCHED realised gross (10 bps, full sample)")
    print("=" * 190)
    sh = live.pivot_table(index=["panel", "arm"], columns="n", values="Sharpe")
    print(fmt(sh))
    print("\nWIDTH PREMIUM (Sharpe at the panel's widest n minus Sharpe at n=5), by convention:")
    prem = pd.DataFrame({a: {pk: sh.loc[(pk, a), NS[-1]] - sh.loc[(pk, a), NS[0]] for pk in panels}
                         for a in ARMS})
    prem.loc["MEAN"] = prem.mean()
    print(fmt(prem, 4))
    print("\nARGMAX n by panel and convention (full-sample Sharpe):")
    amax = pd.DataFrame({a: {pk: int(sh.loc[(pk, a), NS].idxmax()) for pk in panels} for a in ARMS})
    print(amax.to_string())
    moved = int((amax["MATCHED"] != amax["FIXEDTOT"]).sum())
    print(f"argmax cells that MOVE when the gross channel is closed (MATCHED vs FIXEDTOT): "
          f"{moved} of {len(panels)}")
    moved_n = int((amax["NORM"] != amax["FIXEDTOT"]).sum())
    print(f"argmax cells that move under plain NORM vs FIXEDTOT: {moved_n} of {len(panels)}")
    amax.to_csv(OUT / f"{STEM}.argmax.csv")
    prem.to_csv(OUT / f"{STEM}.premium.csv")

    print(f"\nKEEP paths over the {len(live)} live points, by convention (10 bps):")
    kp = live.groupby("arm")[["pass_4a", "pass_4b"]].sum()
    kp["n_points"] = live.groupby("arm").size()
    print(kp.to_string())
    print(f"TOTAL 10 bps: 4a {int(live['pass_4a'].sum())}/{len(live)}, 4b {int(live['pass_4b'].sum())}/{len(live)}")
    live25 = G[G["arm"].isin(ARMS) & (G["cost_bps"] == 25)]
    print(f"TOTAL 25 bps: 4a {int(live25['pass_4a'].sum())}/{len(live25)}, "
          f"4b {int(live25['pass_4b'].sum())}/{len(live25)}")
    if live["pass_4b"].any():
        print("\n4b passes at 10 bps:")
        print(fmt(live[live["pass_4b"]][["panel", "n", "arm", "realised_gross", "CAGR", "Sharpe",
                                         "MaxDD", "H1", "H2", "OOS_Sharpe", "turnover_yr"]]))
    print("\n" + "-" * 190)
    print("LEVEL vs TIMING - the same n, the same mean gross, only the overlay's TIMING differs")
    print("(FIXEDTOT minus MATCHED at every (panel, n); MATCHED already holds mean realised gross equal)")
    print("-" * 190)
    lv = live.pivot_table(index=["panel", "n"], columns="arm", values=["Sharpe", "OOS_Sharpe", "MaxDD", "CAGR"])
    dec_lt = pd.DataFrame({
        "d_Sharpe": lv[("Sharpe", "FIXEDTOT")] - lv[("Sharpe", "MATCHED")],
        "d_OOS_Sharpe": lv[("OOS_Sharpe", "FIXEDTOT")] - lv[("OOS_Sharpe", "MATCHED")],
        "d_MaxDD": lv[("MaxDD", "FIXEDTOT")] - lv[("MaxDD", "MATCHED")],
        "d_CAGR": lv[("CAGR", "FIXEDTOT")] - lv[("CAGR", "MATCHED")],
        "gross_gap": live.pivot_table(index=["panel", "n"], columns="arm", values="realised_gross")["FIXEDTOT"]
                     - live.pivot_table(index=["panel", "n"], columns="arm", values="realised_gross")["MATCHED"],
    })
    print(fmt(dec_lt, 4))
    print(f"\nover the {len(dec_lt)} matched (panel, n) cells: mean d_Sharpe {dec_lt['d_Sharpe'].mean():+.4f} "
          f"(positive on {int((dec_lt['d_Sharpe'] > 0).sum())}/{len(dec_lt)}), "
          f"mean d_OOS_Sharpe {dec_lt['d_OOS_Sharpe'].mean():+.4f} "
          f"(positive on {int((dec_lt['d_OOS_Sharpe'] > 0).sum())}/{len(dec_lt)}), "
          f"mean gross gap {dec_lt['gross_gap'].mean():+.4f} (must be ~0 by construction)")
    print(f"mean d_MaxDD {dec_lt['d_MaxDD'].mean():+.4f} (positive = FIXED draws down LESS), "
          f"mean d_CAGR {dec_lt['d_CAGR'].mean():+.2%}")
    dec_lt.to_csv(OUT / f"{STEM}.leveltiming.csv")

    print("\nbinding 4b bar over all failing live points (10 bps):")
    print(live.loc[~live["pass_4b"], "fail_4b"].value_counts().head(10).to_string())

    # ---- Q3: rule 8
    print("\n" + "=" * 190)
    print("Q3 ANSWER - RULE 8 walk-forward: n chosen on IS 2009-2016 only, OOS 2017-2026 read once")
    print("=" * 190)
    for bps in COST_RUNGS:
        w = W[W["cost_bps"] == bps]
        print(f"\n--- {bps} bps ---")
        print(fmt(w.pivot_table(index="panel", columns="arm",
                                values="OOS_Sharpe")))
        pooled = w.groupby("arm")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "realised_gross"]].mean()
        pooled["n_pick_median"] = w.groupby("arm")["n_pick"].median()
        print("\npooled equal-weight over the 7 panels:")
        print(fmt(pooled.sort_values("OOS_Sharpe", ascending=False)))
    w10 = W[W["cost_bps"] == COST_BPS]
    for a in ("ISARGMAX-FIXEDTOT", "ISARGMAX-NORM", "ISARGMAX-MATCHED"):
        sub = w10[w10["arm"] == a].set_index("panel")
        beat = int((sub["OOS_Sharpe"] > w10[w10["arm"] == "NOTHING(RULESv2)"].set_index("panel")["OOS_Sharpe"]).sum())
        beats_ew = int((sub["OOS_Sharpe"] > w10[w10["arm"] == "EWALL"].set_index("panel")["OOS_Sharpe"]).sum())
        print(f"{a:<20} beats do-nothing OOS on {beat}/7 panels; beats the un-ranked EWall on {beats_ew}/7")
    picks = w10[w10["arm"].str.startswith("ISARGMAX")].pivot_table(index="panel", columns="arm", values="n_pick")
    print("\nIS picks (n) by arm, 10 bps:")
    print(picks.to_string())
    same = int((picks["ISARGMAX-FIXEDTOT"] == picks["ISARGMAX-MATCHED"]).sum())
    print(f"IS pick identical under FIXEDTOT and MATCHED on {same}/7 panels")

    # does the published-style FIXED reading survive OOS at matched gross?
    d = []
    for pk in panels:
        f = w10[(w10["panel"] == pk) & (w10["arm"] == "ISARGMAX-FIXEDTOT")].iloc[0]
        m = w10[(w10["panel"] == pk) & (w10["arm"] == "ISARGMAX-MATCHED")].iloc[0]
        d.append(dict(panel=pk, n_fixed=f["n_pick"], n_matched=m["n_pick"],
                      OOS_Sharpe_fixed=f["OOS_Sharpe"], OOS_Sharpe_matched=m["OOS_Sharpe"],
                      excess=f["OOS_Sharpe"] - m["OOS_Sharpe"]))
    D = pd.DataFrame(d)
    print("\nFIXEDTOT minus MATCHED, OOS Sharpe (the gross channel's own OOS contribution):")
    print(fmt(D))
    print(f"mean excess {D['excess'].mean():+.4f}, sign positive on {int((D['excess'] > 0).sum())}/7 panels")

    rho, nn = spearman(dec["gross_span"], dec["n_argmax"]) if len(dec) else (np.nan, 0)
    print(f"\nSpearman(gross span, published n argmax) over decidable census cells: {rho:+.3f} (N={nn})")

    print("\n" + "=" * 190)
    print("Artifacts: .census.csv .census_rejects.csv .grid.csv .gross.csv .argmax.csv .premium.csv .walkforward.csv")
    print("=" * 190)


if __name__ == "__main__":
    main()
