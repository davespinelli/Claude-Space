#!/usr/bin/env python3
"""Idea 733 - "is-the-c_sd-vs-TURNOVER-correlation-SIGN-FLIP-a-property-of-every-published-
pooled-rho" (lane B, 2026-09-11).

NOTE ON THE ID.  The queue carries TWO ideas numbered 733; the other one
("is-the-EWALL-g1.00-vs-RULES-v2-OOS-SHARPE-TIE-real-or-a-COST-RUNG-artefact") was closed by
the cloud lane earlier today.  This run is the SIGN-FLIP one and is referred to throughout as
733-SIGNFLIP.

The question
------------
Idea 538 published

    rho(c_sd(IS), turn_yr_DG(IS)) over its 162 cells  =  +0.0444 Pearson / -0.1291 Spearman

and read that near-zero as "c_sd and turnover are DISTINCT variables".  But the same 162 cells
cut by GATE FAMILY read +0.5141 (MA-THRESH, n=81) and -0.3879 (QUANTILE, n=81): the pooled
zero is CANCELLATION between two opposite-signed halves, not independence.  Every conclusion
that leans on a pooled rho is exposed to the same failure mode.

This run asks whether that is a property of idea 538's particular pair, or of the record's
pooled correlations generally, and prices the reporting fix the queue proposes -- publish
(rho, n) PER STRATUM beside every pooled one.

Population
----------
The record's own committed book tables: every `research/backtests/*.grid.csv` (441 blocks,
~467k rows).  Each block is a population over which a pooled rho could be quoted, and each
carries its own categorical columns (panel, family, cadence, construction, gross, cost, ...)
that a re-cut could use.  Plus a FRESH rebuild of idea 538's exact 162-cell population, so the
queue's premise number is re-derived from prices rather than read off a CSV.

Tuned parameters (PROTOCOL rule 4: at most two).  Reported at EVERY grid point, selected at
none except inside the rule-8 walk-forward.
    1. CLAIM SET, 3 values -- which (x, y) pairs count as "a pooled rho claim":
         QUEUE  every (z, TURNOVER) pair            -- idea 538's own claim family
         CANON  10 fixed headline metric pairs      -- what the record actually quotes
         ALL    every numeric column pair in the block (<= 120 per block, deterministic)
    2. STRATUM, the re-cut variable -- every categorical column the block carries
         (panel, family, cad/cadence, con, arm, book, kind, gross, cost, bps, universe,
          dial, conv, level, freq, mode, variant), plus two CONTROLS:
         ROWHALF  first half / second half of the block's own row order
         RANDOM2  seeded random halves -- the base rate of a MEANINGLESS re-cut

Fixed, NOT tuned (stated so they cannot be read as dials): EPS_SIGN = 0.10 (a |rho| below
which a sign is not worth quoting), NMIN = 8 rows per stratum, MAXCOLS = 16 numeric columns
per block, seed 733.

Definitions, pre-registered before any corpus number was read.  For one (block, pair, stratum)
with pooled rho `r` and per-stratum rho `r_k` (only strata with n_k >= NMIN; `strong` = those
with |r_k| >= EPS_SIGN):
    FLIP     |r| >= EPS_SIGN and some strong r_k has the opposite sign.
             This is the queue's wording -- "a per-family re-cut reverses the sign in either
             half".
    SIMPSON  |r| >= EPS_SIGN, >= 2 strong strata, and EVERY strong r_k has the opposite sign.
             The strict reversal.
    CANCEL   the strong strata carry BOTH signs and |r| < min_k |r_k|.
             Idea 538's exact pattern: the pooled number is smaller than every stratum it is
             made of, so "near zero" is cancellation, not independence.
    CANCEL0  CANCEL and |r| < EPS_SIGN -- the pooled number reads as "no relationship" and is
             not one.

Pre-registered bars
-------------------
G1  PREMISE, READ OFF THE RECORD.  Idea 538's committed .cells.csv must reproduce the queue's
    four published numbers: pooled Pearson +0.0444 and Spearman -0.1291, per-family Pearson
    +0.51 / -0.39, to < 5e-3 (pooled) and < 1e-2 (per family).
G2  PREMISE, REBUILT FROM PRICES.  A fresh build of the same 162 cells (3 panels x 2 families
    x 9 levels x 3 cadences, gross 0.75, 10 bps, 324 books) must reproduce the same four
    numbers to < 0.05 in rho and max|d c_sd| < 1e-2, max|d turn_yr| < 1e-2.  (data/prices.csv
    is re-cached daily; idea 301 recorded a 1.287e-02 pp drift of its own gate for the same
    reason.  The allowance is stated, not silently taken.)
B1  IS THE FLIP GENERIC?  Over the CANON claim set on the record's real strata, CANCEL rate
    >= 0.25 of quads.  PASS -> the failure mode is common and the reporting fix is warranted;
    FAIL -> idea 538's pair is unusual.
B2  IS IT MORE THAN THE NULL?  CANCEL rate on real strata >= 2.0x the RANDOM2 control rate on
    the same blocks and pairs.  PASS -> stratification finds real structure; FAIL -> any
    re-cut of anything produces this and the "fix" is noise mining.
B3  IS THE STRATUM THE PART THAT MATTERS?  Within blocks carrying >= 2 stratum columns, the
    spread between the best and worst stratum's CANCEL rate >= 0.20.  PASS -> "report per
    stratum" is under-specified: WHICH stratum decides, and PROTOCOL must name it.
B4  DOES THE POOLED NUMBER EVER STAND ALONE?  Text census of every published rho claim in
    `research/backtests/*.result.md` + CHANGELOG.md + LEADERBOARD.md: share quoting an `n`
    and share quoting a per-stratum companion.  BAR (descriptive, no pass/fail): report both.

Rule 8 walk-forward (PROTOCOL rule 8).  IS <= 2016-12-31, OOS >= 2017-01-01.
  WF-1  THE CLAIM.  Does a sign survive out of sample -- pooled, and per stratum?
        (a) idea 538's own pair on the fresh cells: rho(c_sd, turnover) pooled and per family,
            computed on IS-window quantities and then ONCE on OOS-window quantities.
        (b) record-wide: every block carrying both IS_ and OOS_ readings of the same pair;
            sign-survival rate of the pooled rho vs of the per-stratum rho.
        A stratum rho that does not keep its sign OOS is not a reporting fix, it is noise.
  WF-2  THE BOOK.  Inside each (panel, family, construction) arm of the fresh 324-book grid --
        12 arms -- the cell dials (level, cadence) are chosen on 2010..2016 IS Sharpe ALONE and
        2017..end is read ONCE.  OOS CAGR / Sharpe / MaxDD reported against RULES v2 (live),
        SPY, and the cadence-matched no-gate equal-weight control at the same gross.

Verdicts (both KEEP paths, on every one of the 324 fresh books)
    4a  Sharpe > RULES v2 (live) in BOTH halves AND MaxDD no worse than RULES v2.
    4b  Sharpe > SPY in BOTH halves AND out of sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: prices_small.csv.gz, universe.json and universe_broad.json are all CURRENT
constituents -- no delistings -- so every CAGR LEVEL here is inflated and the 4a/4b columns
inherit that whole.  The headline object of this run is a CORRELATION SIGN across cells of one
panel, which is far less exposed than a level; it is not immune.  SMALL439 drops every ticker
with max_1d_move >= 1.0 in data/small_meta.csv before use (idea 298's rule).

Costs 10 bps, next-day execution, no shorting, no leverage (gross 0.75).

Deterministic, standalone.  Reads research/baseline.py; modifies nothing outside its outputs.
Outputs: .grid.csv .cells.csv .census.csv .pairs.csv.gz .textcensus.csv .wf1.csv
         .walkforward.csv .console.txt .result.md
"""
import itertools
import re
import sys
import warnings
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics

warnings.filterwarnings("ignore")
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 400)

# ---------------------------------------------------------------- fixed constants (NOT dials)
COST_BPS = 10
GROSS = 0.75
CADENCES = ["W", "M", "Q"]
CONSTRUCTIONS = ["RESPREAD", "DEGROSS"]
QUANT_X = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95]
MA_THETA = [0.30, 0.20, 0.12, 0.06, 0.00, -0.06, -0.12, -0.25, -0.40]
FAMILIES = ["QUANTILE", "MA-THRESH"]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"

EPS_SIGN = 0.10
NMIN = 8
MAXCOLS = 16
MAXPAIRS_ALL = 120
SEED = 733
METHODS = ["pearson", "spearman"]

# dial 1
CLAIMSETS = ["QUEUE", "CANON", "ALL"]
# dial 2 -- real strata the record's blocks carry, then the two controls
STRATUM_COLS = ["panel", "family", "cad", "cadence", "con", "construction", "arm", "book",
                "kind", "gross", "cost", "bps", "universe", "dial", "conv", "level", "freq",
                "mode", "variant"]
CONTROL_STRATA = ["ROWHALF", "RANDOM2"]

TURN_NAMES = ["turn_yr", "turnover", "turn", "TO", "turn_yr_is", "turn_yr_oos", "TOrs", "DTO"]
CANON_PAIRS = [("Sharpe", "MaxDD"), ("Sharpe", "CAGR"), ("CAGR", "MaxDD"),
               ("Sharpe", "@TURN"), ("CAGR", "@TURN"), ("H1", "H2"),
               ("IS_Sharpe", "OOS_Sharpe"), ("IS_CAGR", "OOS_CAGR"),
               ("Sharpe", "OOS_Sharpe"), ("MaxDD", "OOS_MaxDD")]
# WF-1(b): the same pair read on the IS window and on the OOS window
WF1_PAIRS = [("Sharpe", "CAGR"), ("Sharpe", "MaxDD"), ("CAGR", "MaxDD")]
IS_ALIAS = {"Sharpe": ["IS_Sharpe", "isSharpe"], "CAGR": ["IS_CAGR", "isCAGR"],
            "MaxDD": ["IS_MaxDD", "isMaxDD"]}
OOS_ALIAS = {"Sharpe": ["OOS_Sharpe", "oSharpe"], "CAGR": ["OOS_CAGR", "oCAGR"],
             "MaxDD": ["OOS_MaxDD", "oMaxDD"]}

# G1 -- idea 538's four published numbers
REF_POOL_P, REF_POOL_S = 0.0444, -0.1291
REF_MA_P, REF_QU_P = 0.5141, -0.3879
G1_TOL_POOL, G1_TOL_FAM = 5e-3, 1e-2
G2_TOL_RHO, G2_TOL_LEVEL = 0.05, 1e-2
B1_BAR, B2_BAR, B3_BAR = 0.25, 2.0, 0.20

REF538 = REPO / "research" / "backtests" / (
    "2026-09-11_is-c_sd-the-right-SCALE-or-is-it-a-TURNOVER-proxy_B.cells.csv")
BT = REPO / "research" / "backtests"

OUT = Path(__file__).with_suffix("")
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def flush_log():
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return np.nan
    return float(np.corrcoef(a[m], b[m])[0, 1])


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, float)), pd.Series(np.asarray(b, float))
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return np.nan
    return pearson(a[m].rank().values, b[m].rank().values)


def rho(a, b, method):
    return pearson(a, b) if method == "pearson" else spearman(a, b)


# ================================================================ FLAGS
def quad_flags(r, rks):
    """r = pooled rho, rks = list of per-stratum rho.  Returns the four pre-registered flags."""
    ks = [x for x in rks if np.isfinite(x)]
    strong = [x for x in ks if abs(x) >= EPS_SIGN]
    out = dict(n_strata=len(ks), n_strong=len(strong),
               min_abs_strong=(min(abs(x) for x in strong) if strong else np.nan),
               max_abs_strong=(max(abs(x) for x in strong) if strong else np.nan),
               spread=(max(ks) - min(ks) if len(ks) >= 2 else np.nan))
    if not np.isfinite(r) or len(ks) < 2:
        return {**out, "FLIP": False, "SIMPSON": False, "CANCEL": False, "CANCEL0": False}
    sr = np.sign(r)
    flip = abs(r) >= EPS_SIGN and any(np.sign(x) != sr for x in strong)
    simpson = (abs(r) >= EPS_SIGN and len(strong) >= 2
               and all(np.sign(x) == -sr for x in strong))
    both_signs = len({np.sign(x) for x in strong}) == 2
    cancel = bool(both_signs and abs(r) < min(abs(x) for x in strong))
    return {**out, "FLIP": bool(flip), "SIMPSON": bool(simpson), "CANCEL": cancel,
            "CANCEL0": bool(cancel and abs(r) < EPS_SIGN)}


# ================================================================ the record's blocks
def block_numeric(d):
    """Numeric, non-degenerate columns; canonical names first so the MAXCOLS cap keeps them."""
    good = []
    for c in d.columns:
        s = d[c]
        if s.dtype == bool or not pd.api.types.is_numeric_dtype(s):
            continue
        v = s.dropna()
        if len(v) < NMIN or v.nunique() < 3:
            continue
        good.append(c)
    pref = [c for c in ["Sharpe", "CAGR", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe",
                        "IS_CAGR", "OOS_CAGR", "IS_MaxDD", "OOS_MaxDD"] + TURN_NAMES
            if c in good]
    rest = sorted(c for c in good if c not in pref)
    return (pref + rest)[:MAXCOLS]


def block_strata(d, rng):
    """{name: Series of labels} -- real categorical columns plus the two controls."""
    out = {}
    for c in STRATUM_COLS:
        if c not in d.columns:
            continue
        g = d[c].astype(str).fillna("NA")
        vc = g.value_counts()
        if 2 <= int((vc >= NMIN).sum()) <= 12:
            out[c] = g
    n = len(d)
    out["ROWHALF"] = pd.Series(np.where(np.arange(n) < n // 2, "A", "B"), index=d.index)
    out["RANDOM2"] = pd.Series(rng.integers(0, 2, n).astype(str), index=d.index)
    return out


def resolve_turn(cols):
    for t in TURN_NAMES:
        if t in cols:
            return t
    return None


def claim_pairs(cols):
    """{claimset: [(x, y), ...]} for one block's numeric columns."""
    turn = resolve_turn(cols)
    cs = set(cols)
    canon = []
    for x, y in CANON_PAIRS:
        xx = turn if x == "@TURN" else x
        yy = turn if y == "@TURN" else y
        if xx and yy and xx in cs and yy in cs and xx != yy:
            canon.append((xx, yy))
    queue = [(c, turn) for c in cols if turn and c != turn] if turn else []
    allp = list(itertools.combinations(cols, 2))[:MAXPAIRS_ALL]
    return {"QUEUE": queue, "CANON": canon, "ALL": allp}


def scan_blocks():
    files = sorted(BT.glob("*.grid.csv"))
    rng = np.random.default_rng(SEED)
    rows = []
    for fi, f in enumerate(files):
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if len(d) < 2 * NMIN:
            continue
        cols = block_numeric(d)
        if len(cols) < 2:
            continue
        packs = claim_pairs(cols)
        cs_of = {}
        for cname in CLAIMSETS:
            for pr in packs[cname]:
                cs_of.setdefault(pr, []).append(cname)
        if not cs_of:
            continue
        strata = block_strata(d, rng)
        X = d[cols]
        for sname, lab in strata.items():
            groups = [g for _, g in X.groupby(lab.values) if len(g) >= NMIN]
            if len(groups) < 2:
                continue
            for method in METHODS:
                Cp = X.corr(method=method)
                Cks = [g.corr(method=method) for g in groups]
                for (x, y), sets in cs_of.items():
                    r = Cp.at[x, y]
                    rks = [c.at[x, y] for c in Cks]
                    fl = quad_flags(r, rks)
                    rows.append(dict(block=f.name, stratum=sname, method=method,
                                     x=x, y=y, n=len(d), rho=r,
                                     claimsets="|".join(sets), **fl))
        if (fi + 1) % 60 == 0:
            P(f"  ... scanned {fi+1}/{len(files)} blocks, {len(rows)} quads")
            flush_log()
    return pd.DataFrame(rows), len(files)


# ================================================================ text census (B4)
RHO_RE = re.compile(r"(pearson|spearman|rho|correlation|corr)\b[^\n]{0,60}?"
                    r"([+-]?\d\.\d{2,6}|[+-]?0\.\d+)", re.I)
N_RE = re.compile(r"(n\s*[=:]\s*\d+|\bn\s+\d+\b|over\s+\d+\s+(cells|points|rows|books|blocks)"
                  r"|\(\s*n\s*=\s*\d+\s*\)|across\s+the\s+\d+)", re.I)
STRAT_RE = re.compile(r"(per[- ](family|panel|stratum|arm|cadence|book|cell)|by (family|panel|"
                      r"cadence|arm)|within[- ](family|panel)|each (family|panel|arm)|"
                      r"stratif|/\s*[+-]?\d\.\d{2,6}\s*/)", re.I)
POOL_RE = re.compile(r"\bpooled\b", re.I)


def text_census():
    files = sorted(BT.glob("*.result.md")) + [REPO / "research" / "CHANGELOG.md",
                                              REPO / "research" / "LEADERBOARD.md"]
    rows = []
    for f in files:
        try:
            txt = f.read_text(errors="ignore")
        except Exception:
            continue
        for line in txt.split("\n"):
            for m in RHO_RE.finditer(line):
                lo, hi = max(0, m.start() - 120), min(len(line), m.end() + 120)
                win = line[lo:hi]
                rows.append(dict(file=f.name, kw=m.group(1).lower(), value=m.group(2),
                                 has_n=bool(N_RE.search(win)),
                                 has_stratum=bool(STRAT_RE.search(win)),
                                 says_pooled=bool(POOL_RE.search(win)),
                                 snippet=win.replace("|", "/")[:200]))
    return pd.DataFrame(rows)


# ================================================================ idea 298/301/535 book grid
def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "SMALL439": (pxs[inv], pxs["SPY"]),
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
    }
    P(f"panels: SMALL439 {out['SMALL439'][0].shape[1]} names ({len(bad)} dropped for "
      f"max_1d_move >= 1.0), U56 {out['U56'][0].shape[1]}, B136 {out['B136'][0].shape[1]}")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def gate_mask(px, family, level):
    live = live_mask(px)
    ma = px.rolling(200).mean()
    if family == "MA-THRESH":
        return (px > ma * (1 + level)) & live
    dist = (px / ma - 1).where(live)
    n = live.sum(axis=1)
    kt = np.ceil(level * n).astype(int).clip(lower=1)
    rank = dist.rank(axis=1, ascending=False, method="first")
    return rank.le(kt, axis=0).fillna(False) & live


def unit_book(px, g, construction):
    if construction == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0)
    n = live_mask(px).sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0)


def control_unit(px):
    live = live_mask(px)
    return live.astype(float).div(live.sum(axis=1).clip(lower=1), axis=0)


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


def build_cells():
    """Fresh rebuild of idea 538's 162 cells / 324 books."""
    PN = panels()
    px_u = load_universe()
    live_full = backtest(px_u, rules_v2_weights(px_u), cost_bps=COST_BPS, freq="W")["returns"]
    rows, cells, panel_spy, panel_live = [], [], {}, {}
    for pname, (px, spy_px) in PN.items():
        start = px.index[260]
        idx = px.loc[start:].index
        yrs_is = len(idx[idx <= IS_END]) / 252
        yrs_oos = len(idx[idx >= OOS_START]) / 252
        yrs_full = len(idx) / 252
        spy_s = stat(spy_px.pct_change().fillna(0.0).loc[start:])
        live_s = stat(live_full.reindex(px.index).fillna(0.0).loc[start:])
        panel_spy[pname], panel_live[pname] = spy_s, live_s
        cu = control_unit(px)
        ctrl = {c: stat(backtest(px, cu * GROSS, cost_bps=COST_BPS, freq=c)["returns"].loc[start:])
                for c in CADENCES}
        P(f"\n  PANEL {pname}: from {start.date()} ({yrs_full:.2f} yrs; IS {yrs_is:.2f}, "
          f"OOS {yrs_oos:.2f})")
        P(f"    SPY CAGR {spy_s['CAGR']:.4f} Sharpe {spy_s['Sharpe']:.4f} MaxDD {spy_s['MaxDD']:.4f} "
          f"halves {spy_s['H1']:.4f}/{spy_s['H2']:.4f} OOS Sharpe {spy_s['oSharpe']:.4f} "
          f"OOS CAGR {spy_s['oCAGR']:.4f} OOS MaxDD {spy_s['oMaxDD']:.4f}")
        P(f"    RULES v2 (live): CAGR {live_s['CAGR']:.4f} Sharpe {live_s['Sharpe']:.4f} "
          f"MaxDD {live_s['MaxDD']:.4f} halves {live_s['H1']:.4f}/{live_s['H2']:.4f} "
          f"OOS Sharpe {live_s['oSharpe']:.4f} OOS CAGR {live_s['oCAGR']:.4f} "
          f"OOS MaxDD {live_s['oMaxDD']:.4f}")
        P(f"    4b bars from SPY: H1>{spy_s['H1']:.3f} H2>{spy_s['H2']:.3f} "
          f"OOS>{spy_s['oSharpe']:.3f} MaxDD>=-{0.60*abs(spy_s['MaxDD']):.1%} "
          f"CAGR>={0.70*spy_s['CAGR']:.2%}")
        flush_log()
        for family in FAMILIES:
            levels = QUANT_X if family == "QUANTILE" else MA_THETA
            for level in levels:
                gm = gate_mask(px, family, level)
                ub = {con: unit_book(px, gm, con) for con in CONSTRUCTIONS}
                for cad in CADENCES:
                    got = {}
                    for con in CONSTRUCTIONS:
                        res = backtest(px, ub[con] * GROSS, cost_bps=COST_BPS, freq=cad)
                        r10 = res["returns"].loc[start:]
                        turn = res["turnover"].loc[start:]
                        grs = res["weights"].loc[start:].sum(axis=1)
                        s = stat(r10)
                        t_is = turn.loc[:IS_END].sum() / yrs_is
                        t_oos = turn.loc[OOS_START:].sum() / yrs_oos
                        got[con] = dict(gross=grs, s=s, t_is=t_is, t_oos=t_oos)
                        rows.append(dict(panel=pname, family=family, level=level, cad=cad,
                                         gross=GROSS, con=con, **s,
                                         turn_yr=turn.sum() / yrs_full,
                                         turn_yr_is=t_is, turn_yr_oos=t_oos,
                                         ctrl_oSharpe=ctrl[cad]["oSharpe"],
                                         p4a=verdict_4a(s, live_s), f4b=fail_4b(s, spy_s)))
                    dg, rs = got["DEGROSS"], got["RESPREAD"]
                    c_t = (dg["gross"] / rs["gross"].replace(0, np.nan)).fillna(0.0)
                    cells.append(dict(panel=pname, family=family, level=level, cad=cad,
                                      c_sd_is=float(c_t.loc[:IS_END].std()),
                                      c_sd_oos=float(c_t.loc[OOS_START:].std()),
                                      to_is=dg["t_is"], to_oos=dg["t_oos"],
                                      tors_is=rs["t_is"], tors_oos=rs["t_oos"]))
            P(f"    ... {pname} / {family} done ({len(levels)*len(CADENCES)*2} books)")
            flush_log()
    return pd.DataFrame(rows), pd.DataFrame(cells), panel_spy, panel_live


# ================================================================ main
def main():
    P("=" * 190)
    P("Idea 733-SIGNFLIP  is-the-c_sd-vs-TURNOVER-correlation-SIGN-FLIP-a-property-of-every-"
      "published-pooled-rho  (lane B) | " + Path(__file__).name)
    P("=" * 190)
    P(f"tuned dials (2): CLAIM SET {CLAIMSETS} x STRATUM (every categorical column a block "
      f"carries, plus controls {CONTROL_STRATA}).  ALL grid points reported.")
    P(f"fixed, not tuned: EPS_SIGN {EPS_SIGN}, NMIN {NMIN}, MAXCOLS {MAXCOLS}, "
      f"MAXPAIRS_ALL {MAXPAIRS_ALL}, seed {SEED}, methods {METHODS}.")
    P("flags: FLIP (|pooled|>=EPS and some strong stratum has the opposite sign) | SIMPSON "
      "(every strong stratum opposite) | CANCEL (strong strata carry both signs AND |pooled| < "
      "min|stratum|) | CANCEL0 (CANCEL and |pooled| < EPS).")
    P(f"bars: B1 CANCEL rate(CANON, real strata) >= {B1_BAR} | B2 >= {B2_BAR}x the RANDOM2 "
      f"control | B3 best-worst stratum CANCEL spread >= {B3_BAR} | B4 descriptive text census.")
    flush_log()

    # ---------------- G1: the premise off the record
    P("\n" + "=" * 190)
    P("G1  THE QUEUE'S PREMISE, READ OFF IDEA 538'S COMMITTED .cells.csv")
    P("=" * 190)
    C538 = pd.read_csv(REF538)
    g1 = {}
    g1["pool_p"] = pearson(C538.c_sd_is, C538.to_is)
    g1["pool_s"] = spearman(C538.c_sd_is, C538.to_is)
    fam = {f: g for f, g in C538.groupby("family")}
    g1["ma_p"] = pearson(fam["MA-THRESH"].c_sd_is, fam["MA-THRESH"].to_is)
    g1["qu_p"] = pearson(fam["QUANTILE"].c_sd_is, fam["QUANTILE"].to_is)
    P(f"  n = {len(C538)} cells.  pooled Pearson {g1['pool_p']:+.4f} (published {REF_POOL_P:+.4f}) "
      f"| pooled Spearman {g1['pool_s']:+.4f} (published {REF_POOL_S:+.4f})")
    P(f"  per family Pearson: MA-THRESH {g1['ma_p']:+.4f} (n={len(fam['MA-THRESH'])}, published "
      f"{REF_MA_P:+.4f}) | QUANTILE {g1['qu_p']:+.4f} (n={len(fam['QUANTILE'])}, published "
      f"{REF_QU_P:+.4f})")
    g1_pass = (abs(g1["pool_p"] - REF_POOL_P) < G1_TOL_POOL
               and abs(g1["pool_s"] - REF_POOL_S) < G1_TOL_POOL
               and abs(g1["ma_p"] - REF_MA_P) < G1_TOL_FAM
               and abs(g1["qu_p"] - REF_QU_P) < G1_TOL_FAM)
    f538 = quad_flags(g1["pool_p"], [g1["ma_p"], g1["qu_p"]])
    P(f"  G1 -> {'PASS' if g1_pass else 'FAIL'}.  Flags on idea 538's own quad (Pearson): "
      f"FLIP {f538['FLIP']} SIMPSON {f538['SIMPSON']} CANCEL {f538['CANCEL']} "
      f"CANCEL0 {f538['CANCEL0']}")
    fs538 = quad_flags(g1["pool_s"], [spearman(fam["MA-THRESH"].c_sd_is, fam["MA-THRESH"].to_is),
                                      spearman(fam["QUANTILE"].c_sd_is, fam["QUANTILE"].to_is)])
    P(f"  (Spearman: FLIP {fs538['FLIP']} SIMPSON {fs538['SIMPSON']} CANCEL {fs538['CANCEL']} "
      f"CANCEL0 {fs538['CANCEL0']})")
    P("  PANEL is the other stratum idea 538's cells carry -- the same quad cut by panel:")
    for p, g in C538.groupby("panel"):
        P(f"    {p:9s} n {len(g):3d}  Pearson {pearson(g.c_sd_is, g.to_is):+.4f}  "
          f"Spearman {spearman(g.c_sd_is, g.to_is):+.4f}")
    fpan = quad_flags(g1["pool_p"], [pearson(g.c_sd_is, g.to_is)
                                     for _, g in C538.groupby("panel")])
    P(f"    -> by PANEL: FLIP {fpan['FLIP']} CANCEL {fpan['CANCEL']} "
      f"(the flip is a FAMILY fact, not a stratification fact)")
    flush_log()

    # ---------------- LEG B: the re-cut census over the record's blocks
    P("\n" + "=" * 190)
    P("LEG B  RE-CUT CENSUS over every committed research/backtests/*.grid.csv block")
    P("=" * 190)
    Q, nfiles = scan_blocks()
    # the ALL claim set alone runs to several hundred thousand quads; the committed quad-level
    # file carries the QUEUE and CANON rows (the ones any claim is read off) and the aggregate
    # for ALL is in .census.csv.  Nothing is selected on -- ALL is reported in every table.
    Q[Q.claimsets.str.contains("QUEUE|CANON")].to_csv(f"{OUT}.pairs.csv.gz", index=False)
    P(f"  {nfiles} .grid.csv files on disk; {Q.block.nunique()} usable blocks; {len(Q)} "
      f"(block x pair x stratum x method) quads with >= 2 strata of n >= {NMIN}.")

    def expand(df):
        out = []
        for cs in CLAIMSETS:
            sel = df[df.claimsets.str.contains(cs, regex=False)].copy()
            sel["claimset"] = cs
            out.append(sel)
        return pd.concat(out, ignore_index=True)

    QE = expand(Q)
    QE["is_control"] = QE.stratum.isin(CONTROL_STRATA)
    agg = QE.groupby(["claimset", "stratum", "method"]).agg(
        n_quads=("FLIP", "size"), n_blocks=("block", "nunique"),
        FLIP=("FLIP", "mean"), SIMPSON=("SIMPSON", "mean"),
        CANCEL=("CANCEL", "mean"), CANCEL0=("CANCEL0", "mean"),
        med_abs_rho=("rho", lambda s: float(np.nanmedian(np.abs(s)))),
        med_spread=("spread", lambda s: float(np.nanmedian(s)))).reset_index()
    agg.to_csv(f"{OUT}.census.csv", index=False)
    P("\n  ALL GRID POINTS (claimset x stratum x method).  Rates are per quad.")
    P(fmt(agg.set_index(["claimset", "stratum", "method"]), 4))
    flush_log()

    # ---------------- B1/B2: generic?  above the null?
    P("\n" + "=" * 190)
    P("B1 / B2  IS THE FLIP GENERIC, AND IS IT MORE THAN A RANDOM RE-CUT?")
    P("=" * 190)
    real = QE[~QE.is_control]
    ctrl = QE[QE.is_control]
    tab = []
    for cs in CLAIMSETS:
        for me in METHODS:
            r = real[(real.claimset == cs) & (real.method == me)]
            c = ctrl[(ctrl.claimset == cs) & (ctrl.method == me)]
            cr = float(r.CANCEL.mean()) if len(r) else np.nan
            cc = float(c.CANCEL.mean()) if len(c) else np.nan
            tab.append(dict(claimset=cs, method=me, n_real=len(r), n_ctrl=len(c),
                            CANCEL_real=cr, CANCEL_ctrl=cc,
                            ratio=(cr / cc if cc and cc > 0 else np.nan),
                            FLIP_real=float(r.FLIP.mean()) if len(r) else np.nan,
                            FLIP_ctrl=float(c.FLIP.mean()) if len(c) else np.nan,
                            SIMPSON_real=float(r.SIMPSON.mean()) if len(r) else np.nan,
                            SIMPSON_ctrl=float(c.SIMPSON.mean()) if len(c) else np.nan))
    T12 = pd.DataFrame(tab)
    P(fmt(T12.set_index(["claimset", "method"]), 4))
    canon_real = float(real[(real.claimset == "CANON")].CANCEL.mean())
    canon_ctrl = float(ctrl[(ctrl.claimset == "CANON")].CANCEL.mean())
    b1 = canon_real >= B1_BAR
    ratio = canon_real / canon_ctrl if canon_ctrl > 0 else np.inf
    b2 = ratio >= B2_BAR
    P(f"\n  B1  CANCEL rate, CANON claim set, real strata, both methods: {canon_real:.4f} "
      f"(n {int((real.claimset=='CANON').sum())}) vs bar {B1_BAR} -> {'PASS' if b1 else 'FAIL'}")
    P(f"  B2  vs RANDOM2/ROWHALF control {canon_ctrl:.4f} "
      f"(n {int((ctrl.claimset=='CANON').sum())}): ratio {ratio:.2f}x vs bar {B2_BAR}x -> "
      f"{'PASS' if b2 else 'FAIL'}")
    P("\n  CANCEL rate by stratum (CANON, both methods, real strata only), n stated -- "
      "the queue's own reporting rule applied to this run's numbers:")
    bys = real[real.claimset == "CANON"].groupby("stratum").agg(
        n=("CANCEL", "size"), blocks=("block", "nunique"), CANCEL=("CANCEL", "mean"),
        FLIP=("FLIP", "mean"), SIMPSON=("SIMPSON", "mean")).sort_values("CANCEL",
                                                                       ascending=False)
    P(fmt(bys, 4))
    flush_log()

    # ---------------- B3: does WHICH stratum matter?
    P("\n" + "=" * 190)
    P("B3  DOES IT MATTER WHICH STRATUM?  (blocks carrying >= 2 real stratum columns)")
    P("=" * 190)
    rc = real[real.claimset == "CANON"]
    per_bs = rc.groupby(["block", "stratum"]).CANCEL.mean().reset_index()
    cnt = per_bs.groupby("block").stratum.nunique()
    multi = cnt[cnt >= 2].index
    mm = per_bs[per_bs.block.isin(multi)]
    spread = mm.groupby("block").CANCEL.agg(["min", "max", "size"])
    spread["spread"] = spread["max"] - spread["min"]
    b3_val = float(spread.spread.mean()) if len(spread) else np.nan
    b3 = bool(np.isfinite(b3_val) and b3_val >= B3_BAR)
    P(f"  {len(multi)} blocks carry >= 2 real stratum columns.  mean(best - worst stratum "
      f"CANCEL rate within a block) = {b3_val:.4f} vs bar {B3_BAR} -> "
      f"{'PASS' if b3 else 'FAIL'}")
    P(f"  distribution of the within-block spread: "
      f"{spread.spread.describe().to_dict() if len(spread) else 'n/a'}")
    flush_log()

    # ---------------- B4: text census
    P("\n" + "=" * 190)
    P("B4  TEXT CENSUS -- how does the record actually PUBLISH a correlation?")
    P("=" * 190)
    TC = text_census()
    TC.to_csv(f"{OUT}.textcensus.csv", index=False)
    P(f"  {len(TC)} published correlation mentions across {TC.file.nunique()} files "
      f"(regex scan of *.result.md + CHANGELOG.md + LEADERBOARD.md; a keyword within 60 chars "
      f"of a signed decimal).  FALSE POSITIVES ARE POSSIBLE and this is a text scan, not a "
      f"parse -- the rates below are upper/lower bounds, not exact counts.")
    if len(TC):
        P(f"  quotes an n nearby      : {TC.has_n.mean():.1%}  ({int(TC.has_n.sum())}/{len(TC)})")
        P(f"  quotes a stratum nearby : {TC.has_stratum.mean():.1%}  "
          f"({int(TC.has_stratum.sum())}/{len(TC)})")
        P(f"  quotes BOTH             : {(TC.has_n & TC.has_stratum).mean():.1%}  "
          f"({int((TC.has_n & TC.has_stratum).sum())}/{len(TC)})")
        P(f"  quotes NEITHER          : {(~TC.has_n & ~TC.has_stratum).mean():.1%}  "
          f"({int((~TC.has_n & ~TC.has_stratum).sum())}/{len(TC)})")
        sp = TC[TC.says_pooled]
        P(f"  of the {len(sp)} that say 'pooled' explicitly: n {sp.has_n.mean() if len(sp) else float('nan'):.1%}, "
          f"stratum {sp.has_stratum.mean() if len(sp) else float('nan'):.1%}")
        P("\n  by keyword:")
        P(fmt(TC.groupby("kw").agg(n=("has_n", "size"), has_n=("has_n", "mean"),
                                   has_stratum=("has_stratum", "mean")), 4))
    flush_log()

    # ---------------- fresh rebuild (G2) + book grid
    P("\n" + "=" * 190)
    P("G2  THE PREMISE, REBUILT FROM PRICES  (idea 538's exact 162 cells / 324 books)")
    P("=" * 190)
    G, C, panel_spy, panel_live = build_cells()
    G.to_csv(f"{OUT}.grid.csv", index=False)
    C.to_csv(f"{OUT}.cells.csv", index=False)
    assert len(C) == 162 and len(G) == 324, f"{len(C)} cells / {len(G)} books"
    key = ["panel", "family", "level", "cad"]
    M = C.merge(C538[key + ["c_sd_is", "to_is"]], on=key, suffixes=("", "_ref"))
    d_csd = float((M.c_sd_is - M.c_sd_is_ref).abs().max())
    d_to = float((M.to_is - M.to_is_ref).abs().max())
    n_pool_p, n_pool_s = pearson(C.c_sd_is, C.to_is), spearman(C.c_sd_is, C.to_is)
    nf = {f: g for f, g in C.groupby("family")}
    n_ma, n_qu = (pearson(nf["MA-THRESH"].c_sd_is, nf["MA-THRESH"].to_is),
                  pearson(nf["QUANTILE"].c_sd_is, nf["QUANTILE"].to_is))
    P(f"\n  matched {len(M)}/162 cells to idea 538.  max|d c_sd_is| {d_csd:.3e} "
      f"(bar {G2_TOL_LEVEL}), max|d turn_yr_is| {d_to:.3e} (bar {G2_TOL_LEVEL})")
    P(f"  rebuilt pooled Pearson {n_pool_p:+.4f} vs committed {g1['pool_p']:+.4f} | Spearman "
      f"{n_pool_s:+.4f} vs {g1['pool_s']:+.4f}")
    P(f"  rebuilt per family Pearson: MA-THRESH {n_ma:+.4f} vs {g1['ma_p']:+.4f} | QUANTILE "
      f"{n_qu:+.4f} vs {g1['qu_p']:+.4f}")
    g2_rho = max(abs(n_pool_p - g1["pool_p"]), abs(n_pool_s - g1["pool_s"]),
                 abs(n_ma - g1["ma_p"]), abs(n_qu - g1["qu_p"]))
    g2_pass = (g2_rho < G2_TOL_RHO and d_csd < G2_TOL_LEVEL and d_to < G2_TOL_LEVEL)
    P(f"  G2 -> {'PASS' if g2_pass else 'FAIL'}  (max|d rho| {g2_rho:.4f} vs bar {G2_TOL_RHO})")
    flush_log()

    # ---------------- WF-1(a): does the sign survive OOS, pooled and per stratum?
    P("\n" + "=" * 190)
    P("WF-1(a)  RULE 8 ON THE CLAIM ITSELF -- idea 538's pair, IS-window fit, OOS window read ONCE")
    P("=" * 190)
    w1 = []
    for me in METHODS:
        ris = rho(C.c_sd_is, C.to_is, me)
        ros = rho(C.c_sd_oos, C.to_oos, me)
        w1.append(dict(cut="POOLED", stratum="-", n=len(C), method=me, rho_IS=ris, rho_OOS=ros,
                       sign_survives=bool(np.sign(ris) == np.sign(ros))))
        for f, g in C.groupby("family"):
            a, b = rho(g.c_sd_is, g.to_is, me), rho(g.c_sd_oos, g.to_oos, me)
            w1.append(dict(cut="FAMILY", stratum=f, n=len(g), method=me, rho_IS=a, rho_OOS=b,
                           sign_survives=bool(np.sign(a) == np.sign(b))))
        for p, g in C.groupby("panel"):
            a, b = rho(g.c_sd_is, g.to_is, me), rho(g.c_sd_oos, g.to_oos, me)
            w1.append(dict(cut="PANEL", stratum=p, n=len(g), method=me, rho_IS=a, rho_OOS=b,
                           sign_survives=bool(np.sign(a) == np.sign(b))))
    W1 = pd.DataFrame(w1)
    P(fmt(W1.set_index(["method", "cut", "stratum"]), 4))
    P(f"\n  sign survives OOS: pooled {int(W1[W1.cut=='POOLED'].sign_survives.sum())}/"
      f"{int((W1.cut=='POOLED').sum())} | FAMILY strata "
      f"{int(W1[W1.cut=='FAMILY'].sign_survives.sum())}/{int((W1.cut=='FAMILY').sum())} | "
      f"PANEL strata {int(W1[W1.cut=='PANEL'].sign_survives.sum())}/"
      f"{int((W1.cut=='PANEL').sum())}")

    # ---------------- WF-1(b): record-wide IS -> OOS sign survival
    P("\n" + "-" * 190)
    P("WF-1(b)  RECORD-WIDE.  Blocks carrying BOTH an IS and an OOS reading of the same pair: "
      "does the sign survive, pooled vs per stratum?")
    rng = np.random.default_rng(SEED + 1)
    w1b = []
    for f in sorted(BT.glob("*.grid.csv")):
        try:
            d = pd.read_csv(f, low_memory=False)
        except Exception:
            continue
        if len(d) < 2 * NMIN:
            continue
        strata = {k: v for k, v in block_strata(d, rng).items() if k not in CONTROL_STRATA}
        if not strata:
            continue
        for (a, b) in WF1_PAIRS:
            xi = next((c for c in IS_ALIAS[a] if c in d.columns), None)
            yi = next((c for c in IS_ALIAS[b] if c in d.columns), None)
            xo = next((c for c in OOS_ALIAS[a] if c in d.columns), None)
            yo = next((c for c in OOS_ALIAS[b] if c in d.columns), None)
            if not all([xi, yi, xo, yo]):
                continue
            for sname, lab in strata.items():
                for me in METHODS:
                    ri, ro = rho(d[xi], d[yi], me), rho(d[xo], d[yo], me)
                    if not (np.isfinite(ri) and np.isfinite(ro)):
                        continue
                    w1b.append(dict(block=f.name, pair=f"{a}~{b}", stratum=sname, method=me,
                                    cut="POOLED", n=len(d), rho_IS=ri, rho_OOS=ro,
                                    strong=abs(ri) >= EPS_SIGN,
                                    survives=bool(np.sign(ri) == np.sign(ro))))
                    for kk, g in d.groupby(lab.values):
                        if len(g) < NMIN:
                            continue
                        ri2, ro2 = rho(g[xi], g[yi], me), rho(g[xo], g[yo], me)
                        if not (np.isfinite(ri2) and np.isfinite(ro2)):
                            continue
                        w1b.append(dict(block=f.name, pair=f"{a}~{b}", stratum=sname,
                                        method=me, cut=f"STRATUM:{kk}", n=len(g),
                                        rho_IS=ri2, rho_OOS=ro2,
                                        strong=abs(ri2) >= EPS_SIGN,
                                        survives=bool(np.sign(ri2) == np.sign(ro2))))
    W1B = pd.DataFrame(w1b)
    pd.concat([W1.assign(block="FRESH-162-CELLS", pair="c_sd~turnover", strong=True),
               W1B], ignore_index=True).to_csv(f"{OUT}.wf1.csv", index=False)
    if len(W1B):
        W1B["kind"] = np.where(W1B.cut == "POOLED", "POOLED", "STRATUM")
        s = W1B[W1B.strong].groupby(["kind", "method"]).agg(
            n=("survives", "size"), blocks=("block", "nunique"),
            sign_survival=("survives", "mean"),
            med_abs_rho_IS=("rho_IS", lambda x: float(np.nanmedian(np.abs(x))))).reset_index()
        P(fmt(s.set_index(["kind", "method"]), 4))
        pooled_sv = float(W1B[(W1B.kind == "POOLED") & W1B.strong].survives.mean())
        strat_sv = float(W1B[(W1B.kind == "STRATUM") & W1B.strong].survives.mean())
        P(f"\n  IS->OOS sign survival on |rho_IS| >= {EPS_SIGN}: POOLED {pooled_sv:.4f} vs "
          f"PER-STRATUM {strat_sv:.4f}  (difference {strat_sv-pooled_sv:+.4f})")
    else:
        pooled_sv = strat_sv = np.nan
        P("  no block carried a matched IS/OOS pair -- WF-1(b) is empty.")
    flush_log()

    # ---------------- WF-2: the book
    P("\n" + "=" * 190)
    P("WF-2  THE BOOK.  (level, cadence) chosen on IS Sharpe alone inside each (panel, family, "
      "construction) arm; OOS read ONCE.")
    P("=" * 190)
    G["p4b"] = G.f4b == "-"
    wf = []
    for (pn, fm, con), grp in G.groupby(["panel", "family", "con"]):
        pick = grp.loc[grp.isSharpe.idxmax()]
        sp_, lv = panel_spy[pn], panel_live[pn]
        wf.append(dict(panel=pn, family=fm, con=con, level=pick.level, cad=pick.cad,
                       isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                       oMaxDD=pick.oMaxDD, live_oSharpe=lv["oSharpe"], live_oCAGR=lv["oCAGR"],
                       live_oMaxDD=lv["oMaxDD"], spy_oSharpe=sp_["oSharpe"],
                       spy_oCAGR=sp_["oCAGR"], spy_oMaxDD=sp_["oMaxDD"],
                       ctrl_oSharpe=pick.ctrl_oSharpe,
                       beats_live=pick.oSharpe > lv["oSharpe"],
                       beats_spy=pick.oSharpe > sp_["oSharpe"],
                       beats_ctrl=pick.oSharpe > pick.ctrl_oSharpe,
                       p4a=bool(pick.p4a), p4b=bool(pick.p4b), f4b=pick.f4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(fmt(WF.set_index(["panel", "family", "con"]), 4))
    P(f"\n  WF-2 picks: beat RULES v2 OOS {int(WF.beats_live.sum())}/{len(WF)} | beat SPY OOS "
      f"{int(WF.beats_spy.sum())}/{len(WF)} | beat the no-gate EW control OOS "
      f"{int(WF.beats_ctrl.sum())}/{len(WF)} | 4a {int(WF.p4a.sum())}/{len(WF)} | "
      f"4b {int(WF.p4b.sum())}/{len(WF)}")
    P("\n  KEEP paths over ALL 324 books (PROTOCOL rule 4):")
    P(f"    4a (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse): {int(G.p4a.sum())}/{len(G)}")
    P(f"    4b (Sharpe > SPY both halves AND OOS, MaxDD <= 60% SPY, CAGR >= 70% SPY): "
      f"{int(G.p4b.sum())}/{len(G)}")
    P("    4b failing-bar sets:")
    for k, v in G.f4b.value_counts().items():
        P(f"      {k:28s} {v}")
    P("\n  per panel/construction:")
    P(fmt(G.groupby(["panel", "con"]).agg(n=("p4a", "size"), p4a=("p4a", "sum"),
                                          p4b=("p4b", "sum"), best_Sharpe=("Sharpe", "max"),
                                          best_oSharpe=("oSharpe", "max"),
                                          best_oCAGR=("oCAGR", "max")), 4))
    flush_log()

    # ---------------- verdict
    P("\n" + "=" * 190)
    P("VERDICT")
    P("=" * 190)
    keep = int(G.p4a.sum()) > 0 or int(G.p4b.sum()) > 0
    P(f"  G1 {'PASS' if g1_pass else 'FAIL'} | G2 {'PASS' if g2_pass else 'FAIL'} | "
      f"B1 {'PASS' if b1 else 'FAIL'} ({canon_real:.4f}) | B2 {'PASS' if b2 else 'FAIL'} "
      f"({ratio:.2f}x) | B3 {'PASS' if b3 else 'FAIL'} ({b3_val:.4f}) | B4 descriptive")
    P(f"  4a {int(G.p4a.sum())}/{len(G)}, 4b {int(G.p4b.sum())}/{len(G)}; WF-2 picks beat "
      f"RULES v2 {int(WF.beats_live.sum())}/{len(WF)}, SPY {int(WF.beats_spy.sum())}/{len(WF)}")
    P(f"  KEEP candidate: {keep}")

    md = [
        f"# Idea 733-SIGNFLIP - is the c_sd-vs-TURNOVER sign flip a property of every published "
        f"pooled rho?  (lane B, {pd.Timestamp.today().date()})",
        "",
        f"Corpus: every committed `research/backtests/*.grid.csv` ({Q.block.nunique()} usable "
        f"blocks of {nfiles} on disk, {len(Q)} quads) plus a FRESH rebuild of idea 538's 162 "
        f"cells / 324 books (3 panels x 2 families x 9 levels x 3 cadences, gross {GROSS}, "
        f"{COST_BPS} bps, next-day execution).",
        f"Tuned (2): CLAIM SET {CLAIMSETS} x STRATUM (every categorical column a block carries "
        f"+ controls {CONTROL_STRATA}). All grid points in `.census.csv`.",
        f"Fixed, not tuned: EPS_SIGN {EPS_SIGN}, NMIN {NMIN}, MAXCOLS {MAXCOLS}, seed {SEED}.",
        "",
        "## Gates",
        f"- **G1 {'PASS' if g1_pass else 'FAIL'}** - idea 538's published premise reproduces off "
        f"its committed `.cells.csv`: pooled Pearson {g1['pool_p']:+.4f} / Spearman "
        f"{g1['pool_s']:+.4f}, per family {g1['ma_p']:+.4f} (MA-THRESH, n=81) / {g1['qu_p']:+.4f} "
        f"(QUANTILE, n=81).",
        f"- **G2 {'PASS' if g2_pass else 'FAIL'}** - the same four numbers rebuilt from prices: "
        f"{n_pool_p:+.4f} / {n_pool_s:+.4f} / {n_ma:+.4f} / {n_qu:+.4f}; max|d rho| "
        f"{g2_rho:.4f}, max|d c_sd| {d_csd:.2e}, max|d turn_yr| {d_to:.2e}.",
        "",
        "## Bars",
        f"- **B1 {'PASS' if b1 else 'FAIL'}** - CANCEL rate on the CANON claim set over real "
        f"strata = {canon_real:.4f} (bar {B1_BAR}).",
        f"- **B2 {'PASS' if b2 else 'FAIL'}** - vs the RANDOM2/ROWHALF control {canon_ctrl:.4f}: "
        f"{ratio:.2f}x (bar {B2_BAR}x).",
        f"- **B3 {'PASS' if b3 else 'FAIL'}** - mean within-block spread between the best and "
        f"worst stratum's CANCEL rate = {b3_val:.4f} over {len(multi)} blocks (bar {B3_BAR}).",
        f"- **B4 (descriptive)** - {len(TC)} published correlation mentions; "
        f"{TC.has_n.mean():.1%} quote an n nearby, {TC.has_stratum.mean():.1%} quote a stratum, "
        f"{(~TC.has_n & ~TC.has_stratum).mean():.1%} quote neither. Text scan, not a parse.",
        "",
        "## Rule 8",
        f"- WF-1(a) idea 538's own pair, IS fit / OOS read once: pooled sign survives "
        f"{int(W1[W1.cut=='POOLED'].sign_survives.sum())}/{int((W1.cut=='POOLED').sum())}, "
        f"FAMILY strata {int(W1[W1.cut=='FAMILY'].sign_survives.sum())}/"
        f"{int((W1.cut=='FAMILY').sum())}, PANEL strata "
        f"{int(W1[W1.cut=='PANEL'].sign_survives.sum())}/{int((W1.cut=='PANEL').sum())}.",
        f"- WF-1(b) record-wide IS->OOS sign survival on |rho_IS| >= {EPS_SIGN}: POOLED "
        f"{pooled_sv:.4f} vs PER-STRATUM {strat_sv:.4f}.",
        f"- WF-2 the book: 18 arms, (level, cadence) picked on IS Sharpe alone; beat RULES v2 OOS "
        f"{int(WF.beats_live.sum())}/{len(WF)}, SPY {int(WF.beats_spy.sum())}/{len(WF)}, no-gate "
        f"EW control {int(WF.beats_ctrl.sum())}/{len(WF)}.",
        "",
        "## KEEP paths",
        f"- 4a {int(G.p4a.sum())}/{len(G)} books; 4b {int(G.p4b.sum())}/{len(G)} books. "
        f"KEEP candidate: {keep}.",
        "",
        "SURVIVORSHIP: all three panels are current constituents; CAGR levels are inflated and "
        "the 4a/4b columns inherit that. The headline object is a correlation SIGN across cells "
        "of one panel, which is far less exposed than a level, but not immune.",
    ]
    Path(f"{OUT}.result.md").write_text("\n".join(md) + "\n")
    line = (f"| {pd.Timestamp.today().date()} | idea733-SIGNFLIP pooled-rho re-cut census "
            f"({Q.block.nunique()} blocks, {len(Q)} quads, 324 fresh books) | - | - | - | - | - | "
            f"G1 {'PASS' if g1_pass else 'FAIL'}, G2 {'PASS' if g2_pass else 'FAIL'}, "
            f"B1 {'PASS' if b1 else 'FAIL'}, B2 {'PASS' if b2 else 'FAIL'}, "
            f"B3 {'PASS' if b3 else 'FAIL'} | {Path(__file__).name} |")
    P("\nLEADERBOARD row (headline):\n" + line)
    flush_log()


if __name__ == "__main__":
    main()
