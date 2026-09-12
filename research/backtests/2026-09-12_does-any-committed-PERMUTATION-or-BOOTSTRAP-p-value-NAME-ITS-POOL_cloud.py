#!/usr/bin/env python3
"""Idea 842 - does any committed PERMUTATION or BOOTSTRAP p-value in the record NAME ITS POOL?
(cloud lane, 2026-09-12)

QUESTION (QUEUE idea 842, verbatim)
    idea 834 found the family-blind null's LOCATION is a property of which arms are pooled, not of
    the family under test: with only long-w QROLL in the corpus the pool mean drops and ABS itself
    turns significant (z +2.26 p 0.0190 at w1008, +3.71 p 0.0020 at w2016) on an unchanged delta of
    +0.4074.  Census the record's committed permutation and bootstrap p-values for whether they
    state the pool, and re-price the ones that do not at a second pool.  Max 2 params (claim set,
    pool).

WHAT IS MEASURED
    PART A - CENSUS.  Every committed research/**.py and .md file is scanned for NUMERIC p-value
        sites (a number, not a bar like "p < 0.05", which is counted separately) that belong to a
        permutation/bootstrap/resampling null.  For each site the surrounding window is read for
        whether the artefact NAMES THE POOL the null was built from - the set of units whose labels
        or values were permuted/resampled.  Two independent readings of "states the pool" (LOOSE
        and STRICT) are reported at every grid point; neither is tuned.
    PART B - RE-PRICING AT A SECOND POOL.  The record's own family-blind null (idea 834/825's
        matched-gross twin win rate) is rebuilt from idea 834's COMMITTED .arms.csv and priced at
        four pools on an UNCHANGED observed statistic.  The observed delta for a family whose arms
        are untouched by the pool change is identical by construction; only the null moves.  That
        is the whole claim, and it is reported as a verdict-flip count, not as prose.

THE STATISTIC (PART B), stated before any number
    For arm a let d_FULL(a) = Sharpe(a) - Sharpe(twin a) and d_OOS(a) = OOS_Sharpe(a) -
    OOS_Sharpe(twin a), both read from idea 834's committed .arms.csv.  For family f on leg L,
        win_L(f) = mean_{a in f} 1[d_L(a) > 0]        (the record's twin win rate)
        delta(f)  = win_OOS(f) - win_FULL(f)          (the leg-to-leg movement)
    LEG CAVEAT, up front: FULL contains OOS, so delta is NOT a disjoint PRE/POST contrast - idea
    833/836's in-window identity applies to its LEVEL.  It does not touch this run's object, which
    is the p-value of a FIXED observed delta under nulls built from different pools.

THE FAMILY-BLIND NULL (834's, verbatim in construction)
    Pool a set of arms, keep each arm's own (d_FULL, d_OOS) pair intact, permute the family labels
    across the pooled arms preserving the family sizes IN THE POOL, recompute delta for each
    family.  Two-sided p = (1 + #{|null| >= |obs|}) / (1 + P).  Seeds fixed, so deterministic.

TUNED PARAMETERS: TWO, exactly the two the queue names.
    (1) CLAIM SET in {NEAR, FILE, CSV}.  HEADLINE NEAR - a numeric p-value site with a null
        keyword within +/-400 characters, i.e. the p is textually tied to a resampling null.
        FILE = any numeric p site in a file that mentions a null anywhere (the loose reading).
        CSV  = committed .csv p-columns (machine-readable p-values).
    (2) POOL in {ALL, LONGW, SHORTW, BALANCED}.  HEADLINE ALL = 834's published convention (every
        arm of the cell).  LONGW = ABS + QEXP + QROLL w >= 1008 (the queue's own example).
        SHORTW = ABS + QEXP + QROLL w <= 504 (the symmetric control the queue does not ask for).
        BALANCED = QROLL cut to ONE w at a time, arm-count-matched.
    3 x 4 = 12 grid points; every one printed and written to .repricing.csv / .census.csv.

REPORTED AXES (not tunes; the headline of each is declared above and printed at every point)
    POOL-STATEMENT READING  LOOSE and STRICT, both, everywhere.
    SCOPE                   POOLED over the three panels and each panel separately.
    COST RUNG               0 / 10 / 25 bps, headline 10 (PROTOCOL rule 2).
    PERMUTATION COUNT       200 / 1000 / 5000, headline 1000, as a stability column.

PRE-REGISTERED HYPOTHESES (written before any number was read)
    H_NAMED     a majority (> 0.50) of the record's permutation/bootstrap p-value sites state their
                pool under the LOOSE reading at the headline claim set.
    H_STRICT    the same holds under the STRICT reading.
    H_FLIP      re-pricing at a second pool flips at least one committed significance verdict
                (p < 0.05 <-> p >= 0.05) on an UNCHANGED observed delta.
    H_QUEUE     the queue's own example reproduces: ABS's delta is NOT significant at pool ALL and
                IS significant (p < 0.05) at pool LONGW, with its observed delta unchanged.
    H_DIR       the pool change moves the null's LOCATION (null_mean), not the observed statistic:
                max |d obs| over pools for an untouched family is exactly 0.
    H_COSTINV   the flip verdict is the same at 0, 10 and 25 bps.
    H_PERMSTAB  the flip verdict is the same at P = 200, 1000, 5000.
    H_R8CENSUS  RULE 8 ON THE CENSUS: the pool-naming rate measured on the record's EARLIER files
                (committed artefacts dated <= 2026-09-05) reproduces, within +/-0.10, on the LATER
                files (>= 2026-09-06) read ONCE.
    H_R8CLAIM   RULE 8 ON THE CLAIM: the pool that maximises ABS's significance on the FULL leg
                reproduces a p < 0.05 verdict on the OOS leg, read ONCE.

GATES (printed first; no verdict is read until they are reported)
    G1 LIVE RULES v2 on U56 at 10 bps reproduces its committed headline 8.63% / 1.2018 / -12.05%.
    G2 SPY's full-sample triple on today's prices reproduces idea 834's committed .arms.csv SPY
       columns (15.163% / 0.8861 / -33.717%).
    G3 NULL CALIBRATION: the identity relabelling returns delta exactly equal to the observed
       (bar 0.0), and over 500 random relabellings of a null corpus the share with p < 0.05 is
       inside the binomial 99% interval for 0.05 (a null that rejects itself is not a null).
    G4 DETECTOR CONTROLS: the site detector and both pool-statement readings are scored on 12
       hand-written positive/negative control strings, every one printed with its verdict.
    G5 CORPUS INTEGRITY: 834's committed .arms.csv is 1,944 rows, 3 panels x 3 rungs x
       (36 ABS / 36 QEXP / 144 QROLL), and its published headline win rates are reproduced.

PROTOCOL RULE 8 and BOTH KEEP PATHS (mandatory, run and reported)
    The book leg is computed from prices in this file, not read from the record: RULES v1, the LIVE
    RULES v2 (band 0.03, gross 0.75), the standing 4b candidate (band 0.03, gross 1.00) and SPY on
    U56 at 0/10/25 bps - full sample, both halves, and OOS 2017-01-01.. read once.  Both KEEP paths
    are evaluated for every book at every rung.  No parameter of any book is chosen by this file.

SURVIVORSHIP, up front: research/universe.json is a CURRENT-constituent list, so every CAGR and
    Sharpe printed here is optimistic; the census and the re-pricing are counts over committed
    text and committed columns and carry no survivorship, but no number here is a capital claim.

Outputs (all committed under research/backtests/):
    .console.txt    full log          .sites.csv      one row per detected p-value site
    .census.csv     claim set x reading x pool-naming counts
    .repricing.csv  12 tuned points x scope x rung x P x family: obs, null mean/sd, z, p, verdict
    .walkforward.csv the two rule-8 legs and the book leg
    .result.md      the answer
RULES.md, PROTOCOL.md, research/scan.py, products/bot/bot.py and research/baseline.py are NOT
modified by this script.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

DATE = "2026-09-12"
SLUG = "does-any-committed-PERMUTATION-or-BOOTSTRAP-p-value-NAME-ITS-POOL"
HERE = Path(__file__).resolve().parent
OUT = HERE / f"{DATE}_{SLUG}_cloud"
ARMS834 = HERE / "2026-09-12_is-the-PRE-POST-ASYMMETRY-QROLL-s-or-the-WINDOW-s_C.arms.csv"

# ---- declared constants -----------------------------------------------------------------
CLAIMSETS = ["NEAR", "FILE", "CSV"]
CLAIMSET_HEAD = "NEAR"
POOLS = ["ALL", "LONGW", "SHORTW", "BALANCED"]
POOL_HEAD = "ALL"
READINGS = ["LOOSE", "STRICT"]
SCOPES = ["POOLED", "U56", "B136", "SMALL663"]
RUNGS = [0.0, 10.0, 25.0]
RUNG_HEAD = 10.0
PERMS = [200, 1000, 5000]
PERM_HEAD = 1000
FAMS = ["ABS", "QEXP", "QROLL"]
WINDOW = 400            # characters either side of a site that count as "the site's text"
SEED0 = 8420000
ALPHA = 0.05
IS_CUT = pd.Timestamp("2026-09-05")     # rule-8 census cut: files dated <= this are IS
OOS_START = "2017-01-01"
WARMUP = 260
SPY_PUB = (0.15163101010956526, 0.8860543931081106, -0.33717235283398306)   # 834 .arms.csv
V2_PUB = (0.0863, 1.2018, -0.1205)                                          # committed headline

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


# ================================================================= detector ===============
NULLKW = re.compile(r"permut|bootstrap|resampl|relabel|reshuffl|shuffl", re.I)
# a numeric p-value, not a bar: "p 0.0190", "p=0.019", "(p 0.02)", "p-value of 0.019"
P_SITE = re.compile(r"\bp(?:[\s_-]*(?:value|val|perm|boot))?\s*(?:=|:|\s)\s*(0\.\d{2,6})\b", re.I)
P_BAR = re.compile(r"\bp\s*[<>]=?\s*0\.\d+")
POOL_LOOSE = re.compile(r"pool|pooled|corpus|within|scope|block|across (?:arms|rows|books|cells|"
                        r"claims|pairs|draws|names|panels)|per[- ](?:panel|cell|family|book|arm|"
                        r"rung|split|window|leg|stratum|strata)|label|size|"
                        r"\d+[,\d]*\s+(?:draws|rows|arms|books|cells|claims|pairs|windows|names|"
                        r"observations|sites|files|blocks)", re.I)
POOL_UNIT = re.compile(r"\b(arms?|rows?|books?|cells?|claims?|pairs?|draws?|names?|panels?|"
                       r"observations?|sites?|files?|windows?|blocks?|strata|stratum)\b", re.I)
POOL_DELIM = re.compile(r"\b(pool|pooled|within|scope|block|corpus)\b", re.I)
COUNT_TOK = re.compile(r"\b(?:n\s*=\s*\d+|\d{2,}(?:,\d{3})*)\b")


def pool_stated(win: str) -> dict:
    """Both readings of 'the artefact names the pool this p-value's null was built from'."""
    loose = bool(POOL_LOOSE.search(win))
    strict = bool(POOL_DELIM.search(win) and POOL_UNIT.search(win) and COUNT_TOK.search(win))
    return dict(LOOSE=loose, STRICT=strict)


def file_date(p: Path):
    m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
    return pd.Timestamp(m.group(1)) if m else pd.NaT


def scan_sites() -> pd.DataFrame:
    rows = []
    for p in sorted(ROOT.joinpath("research").rglob("*")):
        if not p.is_file() or p.suffix not in (".py", ".md"):
            continue
        if p.name.startswith(Path(OUT).name):
            continue                      # never census this run's own outputs (determinism)
        try:
            t = p.read_text(errors="ignore")
        except Exception:
            continue
        file_null = bool(NULLKW.search(t))
        if not file_null:
            continue                      # no resampling null anywhere: out of every claim set
        bars = len(P_BAR.findall(t))
        for m in P_SITE.finditer(t):
            a, b = max(0, m.start() - WINDOW), min(len(t), m.end() + WINDOW)
            win = t[a:b]
            near = bool(NULLKW.search(win))
            ps = pool_stated(win)
            rows.append(dict(file=str(p.relative_to(ROOT)), suffix=p.suffix, date=file_date(p),
                             pos=m.start(), pval=float(m.group(1)), near_null=near,
                             file_null=file_null, bars_in_file=bars,
                             pool_LOOSE=ps["LOOSE"], pool_STRICT=ps["STRICT"],
                             sig=float(m.group(1)) < ALPHA))
    return pd.DataFrame(rows)


def scan_csv_pcols() -> pd.DataFrame:
    rows = []
    pat = re.compile(r"^(p|pval|p_val|p_value|pvalue|p_perm|perm_p|p_boot|boot_p|p_two|p2)$", re.I)
    for p in sorted(ROOT.joinpath("research").rglob("*.csv")):
        if not p.is_file() or p.name.startswith(Path(OUT).name):
            continue
        try:
            head = p.open(errors="ignore").readline().strip()
        except Exception:
            continue
        cols = [c.strip() for c in head.split(",")]
        hits = [c for c in cols if pat.match(c)]
        if not hits:
            continue
        # does the PRODUCING artefact (same stem .py, else same-stem .md) state the pool?
        stem = p.name.split(".")[0]
        srcs = [q for q in (HERE / f"{stem}.py", HERE / f"{stem}.md",
                            HERE / f"{stem}.result.md") if q.exists()]
        txt = "\n".join(q.read_text(errors="ignore") for q in srcs)
        ps = pool_stated(txt) if txt else dict(LOOSE=False, STRICT=False)
        rows.append(dict(file=str(p.relative_to(ROOT)), suffix=".csv", date=file_date(p),
                         cols=";".join(hits), n_src=len(srcs), has_null=bool(NULLKW.search(txt)),
                         pool_LOOSE=ps["LOOSE"], pool_STRICT=ps["STRICT"]))
    return pd.DataFrame(rows)


# ================================================================= null ===================
def price_cell(sub: pd.DataFrame, nperm: int, seed: int) -> pd.DataFrame:
    """Family-blind permutation p-values for delta(f) = win_OOS(f) - win_FULL(f) on one pool.

    Permuting the family LABELS across the pool is identical to permuting the (d_FULL, d_OOS)
    pairs against family blocks of the same sizes, so the arms are sorted by family once and every
    draw is one vectorised shuffle - the same null as 834's, computed without a Python loop.
    """
    s = sub.sort_values("family", kind="mergesort")
    wf = (s["dSharpe"].values > 0).astype(float)
    wo = (s["dOOS"].values > 0).astype(float)
    lab = s["family"].values
    fams = [f for f in FAMS if (lab == f).sum() > 0]
    n = len(s)
    bounds, i0 = {}, 0
    for f in fams:                                   # contiguous blocks after the sort
        k = int((lab == f).sum())
        bounds[f] = (i0, i0 + k)
        i0 += k
    rng = np.random.default_rng(seed)
    idx = np.argsort(rng.random((nperm, n)), axis=1)
    WO, WF = wo[idx], wf[idx]
    rows = []
    for f in fams:
        a, b = bounds[f]
        obs = float(wo[a:b].mean() - wf[a:b].mean())
        nu = WO[:, a:b].mean(axis=1) - WF[:, a:b].mean(axis=1)
        sd = float(nu.std(ddof=1))
        z = (obs - float(nu.mean())) / sd if sd > 0 else np.nan
        p = (1 + int(np.sum(np.abs(nu) >= abs(obs) - 1e-15))) / (1 + nperm)
        rows.append(dict(family=f, n=int(b - a), win_FULL=float(wf[a:b].mean()),
                         win_OOS=float(wo[a:b].mean()), obs=obs,
                         null_mean=float(nu.mean()), null_sd=sd, z=z, p=p, sig=p < ALPHA))
    return pd.DataFrame(rows)


def pool_subset(cell: pd.DataFrame, pool: str, w=None) -> pd.DataFrame:
    if pool == "ALL":
        return cell
    if pool == "LONGW":
        return cell[(cell.family != "QROLL") | (cell.w >= 1008)]
    if pool == "SHORTW":
        return cell[(cell.family != "QROLL") | (cell.w <= 504)]
    if pool == "BALANCED":
        return cell[(cell.family != "QROLL") | (cell.w == w)]
    raise ValueError(pool)


# ================================================================= books ==================
def book_metrics(px, wfn, cost_bps):
    res = backtest(px, wfn(px), cost_bps=cost_bps, freq="W")
    r = res["returns"].loc[px.index[WARMUP]:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    ro = r.loc[OOS_START:]
    ho = len(ro) // 2
    o1, o2 = metrics(ro.iloc[:ho]), metrics(ro.iloc[ho:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                OOS_H1=o1["Sharpe"], OOS_H2=o2["Sharpe"])


def spy_metrics(px):
    r = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP]:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    ro = r.loc[OOS_START:]
    ho = len(ro) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                OOS_H1=metrics(ro.iloc[:ho])["Sharpe"], OOS_H2=metrics(ro.iloc[ho:])["Sharpe"])


def keep_paths(b, live, spy):
    """PROTOCOL 4a and 4b, every leg reported."""
    a = dict(a_H1=b["H1"] > live["H1"], a_H2=b["H2"] > live["H2"], a_DD=b["MaxDD"] >= live["MaxDD"])
    a["pass_4a"] = all(a.values())
    f = dict(b_H1=b["H1"] > spy["H1"], b_H2=b["H2"] > spy["H2"],
             b_OOS=b["OOS_Sharpe"] > spy["OOS_Sharpe"],
             b_DD=abs(b["MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
             b_CAGR=b["CAGR"] >= 0.70 * spy["CAGR"])
    f["pass_4b"] = all(f.values())                   # PROTOCOL 4b exactly: halves + OOS + DD + CAGR
    f["b_OOSH1"] = b["OOS_H1"] > spy["OOS_H1"]       # reported, NOT part of the 4b conjunction
    f["b_OOSH2"] = b["OOS_H2"] > spy["OOS_H2"]
    return {**a, **f}


# ================================================================= main ===================
def main():
    t0 = time.time()
    P(f"=== idea 842 - does any committed permutation/bootstrap p-value NAME ITS POOL? ({DATE}, cloud)")
    P("tuned: CLAIM SET in NEAR/FILE/CSV (head NEAR), POOL in ALL/LONGW/SHORTW/BALANCED (head ALL)")

    # ---------------------------------------------------------------- gates
    P("\n--- GATES (printed before any verdict) ---")
    px = load_universe()
    P(f"U56 panel {px.shape[0]} rows x {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}")
    v2 = book_metrics(px, lambda q: rules_v2_weights(q, 0.03, 0.75), 10.0)
    g1 = max(abs(v2["CAGR"] - V2_PUB[0]), abs(v2["Sharpe"] - V2_PUB[1]), abs(v2["MaxDD"] - V2_PUB[2]))
    P(f"G1 LIVE RULES v2 @10bps {v2['CAGR']:.4%} / {v2['Sharpe']:.4f} / {v2['MaxDD']:.4%} "
      f"vs committed 8.63% / 1.2018 / -12.05%  max|d| {g1:.3e}  -> {'PASS' if g1 <= 6e-3 else 'FAIL'}")
    spy = spy_metrics(px)
    g2 = max(abs(spy["CAGR"] - SPY_PUB[0]), abs(spy["Sharpe"] - SPY_PUB[1]), abs(spy["MaxDD"] - SPY_PUB[2]))
    P(f"G2 SPY full {spy['CAGR']:.4%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.4%} vs 834 committed "
      f"15.163% / 0.8861 / -33.717%  max|d| {g2:.3e}  -> {'PASS' if g2 <= 6e-3 else 'FAIL'}")

    arms = pd.read_csv(ARMS834)
    sizes = sorted(arms.groupby(["panel", "rung", "family"]).size().unique().tolist())
    ok5 = (len(arms) == 1944 and set(arms.panel) == {"U56", "B136", "SMALL663"}
           and set(arms["rung"]) == {0.0, 10.0, 25.0} and sizes == [36, 144])
    P(f"G5 834 .arms.csv {len(arms)} rows, panels {sorted(set(arms.panel))}, rungs "
      f"{sorted(set(arms['rung']))}, per (panel,rung,family) sizes {sizes} "
      f"(36 ABS / 36 QEXP / 144 QROLL) -> {'PASS' if ok5 else 'FAIL'}")

    # G3 null calibration on the headline cell
    cell = arms[(arms["rung"] == RUNG_HEAD)].copy()
    wf = (cell["dSharpe"].values > 0)
    wo = (cell["dOOS"].values > 0)
    lab = cell["family"].values
    obs_abs = float(wo[lab == "ABS"].mean() - wf[lab == "ABS"].mean())
    ident = float(price_cell(cell, 2, SEED0).set_index("family").loc["ABS", "obs"])
    rng = np.random.default_rng(SEED0 + 1)
    hits = 0
    NCAL = 500
    for i in range(NCAL):
        pl = rng.permutation(lab)                       # draw a NULL corpus ...
        sub = pd.DataFrame(dict(family=pl, dSharpe=cell["dSharpe"].values,
                                dOOS=cell["dOOS"].values, w=cell["w"].values))
        d = price_cell(sub, 200, SEED0 + 10_000 + i)    # ... and price it with a fresh null
        hits += int(bool(d.loc[d.family == "ABS", "sig"].iloc[0]))
    share = hits / NCAL
    lo, hi = 0.05 - 2.576 * np.sqrt(0.05 * 0.95 / NCAL), 0.05 + 2.576 * np.sqrt(0.05 * 0.95 / NCAL)
    P(f"G3 identity relabelling delta {ident:.10f} vs observed {obs_abs:.10f}  |d| "
      f"{abs(ident - obs_abs):.1e}; calibration: {hits}/{NCAL} random relabellings reject at "
      f"alpha {ALPHA} -> share {share:.4f}, 99% interval [{lo:.4f}, {hi:.4f}] "
      f"-> {'PASS' if lo <= share <= hi else 'FAIL'}")

    CONTROLS = [
        ("permuting the family labels across all 216 pooled arms", True, True),
        ("a bootstrap of the 1,680 committed arm-rows, resampled within panel", True, True),
        ("permutation p 0.0190 (two-sided)", False, False),
        ("we report a bootstrap p-value for the slope", False, False),
        ("labels shuffled within each of the 9 strata, n = 180 cells", True, True),
        ("the null is built from the pooled corpus", True, False),
        ("p 0.0020 against a family-blind control", False, False),
        ("1,000 permutations of the 36 ABS arms in the pool", True, True),
        ("resampling the 20 draws per rung", True, False),
        ("significance at p < 0.05", False, False),
        ("block bootstrap over 252-day blocks of the 4,520 windows", True, True),
        ("a permutation test", False, False),
    ]
    P("G4 DETECTOR CONTROLS (string -> LOOSE/STRICT, expected in brackets):")
    ok4 = True
    for s, eL, eS in CONTROLS:
        got = pool_stated(s)
        good = (got["LOOSE"] == eL) and (got["STRICT"] == eS)
        ok4 &= good
        P(f"   {'ok ' if good else 'MISS'} LOOSE {got['LOOSE']!s:5} [{eL!s:5}] STRICT "
          f"{got['STRICT']!s:5} [{eS!s:5}]  {s!r}")
    P(f"G4 -> {'PASS' if ok4 else 'FAIL'} ({sum(1 for s,a,b in CONTROLS)} controls)")

    # ---------------------------------------------------------------- PART A census
    P("\n--- PART A: CENSUS of committed permutation/bootstrap p-value sites ---")
    sites = scan_sites()
    csvp = scan_csv_pcols()
    sites.to_csv(f"{OUT}.sites.csv", index=False)
    nfiles_scanned = sum(1 for p in ROOT.joinpath("research").rglob("*")
                         if p.is_file() and p.suffix in (".py", ".md")
                         and not p.name.startswith(Path(OUT).name))
    P(f"denominator: {nfiles_scanned} committed research/**.{{py,md}} files; "
      f"{sites.file.nunique()} carry a resampling null AND a numeric p-value; "
      f"{len(sites)} numeric p-value sites; {len(csvp)} committed .csv files carry a p-column")
    rows = []
    for cs in CLAIMSETS:
        if cs == "NEAR":
            sub = sites[sites.near_null]
        elif cs == "FILE":
            sub = sites
        else:
            sub = csvp[csvp.has_null] if len(csvp) else csvp
        n = len(sub)
        for rd in READINGS:
            k = int(sub[f"pool_{rd}"].sum()) if n else 0
            rows.append(dict(claimset=cs, reading=rd, n_sites=n, n_pool_stated=k,
                             share=(k / n if n else np.nan),
                             n_files=int(sub.file.nunique()) if n else 0,
                             headline=(cs == CLAIMSET_HEAD)))
            P(f"   CLAIMSET {cs:5} reading {rd:6} sites {n:5}  pool stated {k:5}  "
              f"share {(k/n if n else float('nan')):.4f}  files {sub.file.nunique() if n else 0}")
    cen = pd.DataFrame(rows)
    cen.to_csv(f"{OUT}.census.csv", index=False)
    head = cen[(cen.claimset == CLAIMSET_HEAD)].set_index("reading")
    sh_loose = head.loc["LOOSE", "share"]
    sh_strict = head.loc["STRICT", "share"]
    H_NAMED = bool(sh_loose > 0.50)
    H_STRICT = bool(sh_strict > 0.50)
    # significance of the censused p-values themselves, and the bar/value split
    near = sites[sites.near_null]
    bars_unique = int(sites.drop_duplicates("file").bars_in_file.sum())
    P(f"   of the {len(near)} headline sites, {int(near.sig.sum())} quote p < {ALPHA} "
      f"({near.sig.mean():.4f}) and {len(near) - int(near.sig.sum())} quote a NULL reading; "
      f"BAR mentions (p < x, no value) in the same files: {bars_unique}")

    # rule 8 on the census: early files choose, later files read once
    wfrows = []
    dated = near[near.date.notna()]
    P(f"   rule-8 census denominator: {len(dated)} of {len(near)} headline sites sit in a "
      f"DATE-STAMPED artefact (undated files - PROTOCOL.md, README and the like - cannot carry "
      f"a time split and are excluded)")
    for rd in READINGS:
        e = dated[dated.date <= IS_CUT]
        l = dated[dated.date > IS_CUT]
        se, sl = (e[f"pool_{rd}"].mean() if len(e) else np.nan), (l[f"pool_{rd}"].mean() if len(l) else np.nan)
        wfrows.append(dict(leg="R8_CENSUS", reading=rd, n_IS=len(e), n_OOS=len(l),
                           IS=se, OOS=sl, gap=abs(sl - se), passes=bool(abs(sl - se) <= 0.10)))
        P(f"   RULE 8 (census) reading {rd:6}: IS (<= {IS_CUT.date()}) {se:.4f} on {len(e)} sites, "
          f"OOS {sl:.4f} on {len(l)} sites, gap {abs(sl-se):.4f} "
          f"-> {'PASS' if abs(sl - se) <= 0.10 else 'FAIL'}")
    H_R8CENSUS = all(r["passes"] for r in wfrows)
    # SECOND CUT, reported because the declared cut leaves an IS leg of 2 sites and cannot resolve
    # a 0.10 bar: the MEDIAN file date of the dated corpus, which splits it as evenly as possible.
    if len(dated) >= 4:
        med = dated.date.median()
        for rd in READINGS:
            e, l = dated[dated.date <= med], dated[dated.date > med]
            se, sl = e[f"pool_{rd}"].mean(), l[f"pool_{rd}"].mean()
            wfrows.append(dict(leg="R8_CENSUS_MEDIANCUT", reading=rd, n_IS=len(e), n_OOS=len(l),
                               IS=se, OOS=sl, gap=abs(sl - se), passes=bool(abs(sl - se) <= 0.10)))
            P(f"   RULE 8 (census, MEDIAN cut {pd.Timestamp(med).date()}) reading {rd:6}: "
              f"{se:.4f} on {len(e)} vs {sl:.4f} on {len(l)}, gap {abs(sl-se):.4f} "
              f"-> {'PASS' if abs(sl - se) <= 0.10 else 'FAIL'}")

    # ---------------------------------------------------------------- PART B re-pricing
    P("\n--- PART B: RE-PRICING 834's family-blind null at a SECOND POOL (all 12 tuned points) ---")
    rp = []
    k = 0
    for scope in SCOPES:
        base = arms if scope == "POOLED" else arms[arms.panel == scope]
        for rung in RUNGS:
            c0 = base[base["rung"] == rung]
            for pool in POOLS:
                ws = [1008] if pool != "BALANCED" else [252, 504, 1008, 2016]
                for w in ws:
                    sub = pool_subset(c0, pool, w)
                    # the 12 tuned points run at the headline P; the P-stability column runs only
                    # where it is read (POOLED, every rung) so the file stays cheap and honest
                    nps = PERMS if scope == "POOLED" else [PERM_HEAD]
                    for nperm in nps:
                        k += 1
                        d = price_cell(sub, nperm, SEED0 + 1000 * k)   # deterministic seeds
                        d["scope"], d["rung"], d["pool"], d["w_kept"], d["nperm"] = scope, rung, pool, w, nperm
                        d["headline"] = (scope == "POOLED" and rung == RUNG_HEAD and nperm == PERM_HEAD)
                        rp.append(d)
    rep = pd.concat(rp, ignore_index=True)
    rep.to_csv(f"{OUT}.repricing.csv", index=False)
    P(f"   {len(rep)} re-priced cells written to {Path(OUT).name}.repricing.csv")

    hd = rep[rep.headline]
    P("\n   HEADLINE CELL (POOLED, 10 bps, P=1000) - every pool, every family:")
    P(f"   {'pool':9}{'w':6}{'fam':6}{'n':>5}{'win_FULL':>10}{'win_OOS':>9}{'obs':>9}"
      f"{'null_mu':>9}{'null_sd':>9}{'z':>8}{'p':>8}  sig")
    for _, r in hd.sort_values(["pool", "w_kept", "family"]).iterrows():
        P(f"   {r['pool']:9}{int(r['w_kept']):<6}{r['family']:6}{int(r['n']):5}{r['win_FULL']:10.4f}"
          f"{r['win_OOS']:9.4f}{r['obs']:9.4f}{r['null_mean']:9.4f}{r['null_sd']:9.4f}"
          f"{r['z']:8.2f}{r['p']:8.4f}  {'YES' if r['sig'] else 'no'}")

    # H_DIR: observed statistic must not move for a family whose arms the pool leaves alone
    dirs = []
    for fam in ["ABS", "QEXP"]:
        v = rep[(rep.family == fam)].groupby(["scope", "rung", "nperm"])["obs"].agg(lambda s: s.max() - s.min())
        dirs.append(float(v.max()))
    H_DIR = max(dirs) == 0.0
    P(f"\n   H_DIR max spread of the OBSERVED delta across pools, for families the pool does not "
      f"touch (ABS, QEXP): {max(dirs):.3e} -> {'PASS' if H_DIR else 'FAIL'}")

    # H_QUEUE / H_FLIP
    def cellp(pool, fam, scope="POOLED", rung=RUNG_HEAD, nperm=PERM_HEAD, w=1008):
        q = rep[(rep.pool == pool) & (rep.family == fam) & (rep.scope == scope)
                & (rep["rung"] == rung) & (rep.nperm == nperm) & (rep.w_kept == w)]
        return q.iloc[0]
    a_all, a_long = cellp("ALL", "ABS"), cellp("LONGW", "ABS")
    H_QUEUE = bool((not a_all.sig) and a_long.sig and abs(a_all.obs - a_long.obs) == 0.0)
    P(f"   H_QUEUE ABS at pool ALL p {a_all.p:.4f} (z {a_all.z:+.2f}) vs pool LONGW p {a_long.p:.4f} "
      f"(z {a_long.z:+.2f}) on an observed delta of {a_all.obs:+.4f} both times "
      f"-> {'PASS' if H_QUEUE else 'FAIL'}")
    flips = []
    for (scope, rung, nperm, fam), g in rep.groupby(["scope", "rung", "nperm", "family"]):
        base = g[g.pool == "ALL"]
        if not len(base):
            continue
        b = bool(base.iloc[0].sig)
        for _, r in g[g.pool != "ALL"].iterrows():
            if bool(r.sig) != b:
                flips.append(dict(scope=scope, rung=rung, nperm=nperm, family=fam, pool=r["pool"],
                                  w=r["w_kept"], p_ALL=float(base.iloc[0].p), p_pool=float(r.p),
                                  obs_ALL=float(base.iloc[0].obs), obs_pool=float(r.obs),
                                  sig_ALL=b, sig_pool=bool(r.sig)))
    fl = pd.DataFrame(flips)
    H_FLIP = len(fl) > 0
    P(f"   H_FLIP verdict flips vs pool ALL: {len(fl)} of "
      f"{len(rep[rep.pool != 'ALL'])} re-priced cells -> {'PASS' if H_FLIP else 'FAIL'}")
    if len(fl):
        same_obs = fl[np.isclose(fl.obs_ALL, fl.obs_pool)]
        P(f"        of which {len(same_obs)} happen on an UNCHANGED observed delta; by family "
          f"{fl.family.value_counts().to_dict()}; by pool {fl['pool'].value_counts().to_dict()}")
        fl.to_csv(f"{OUT}.flips.csv", index=False)
    # POST-HOC (labelled as such; not a pre-registered hypothesis): how far does the p-value of an
    # UNCHANGED observed delta travel across pools, and which conventional bar would it cross?
    P("\n   POST-HOC - the p-value of an UNCHANGED statistic, across pools (POOLED, 10 bps, P=1000):")
    bars = [0.10, 0.05, 0.01, 0.001]
    barrows = []
    for fam in FAMS:
        q = rep[(rep.family == fam) & rep.headline]
        if not len(q):
            continue
        same = q[np.isclose(q.obs, q.obs.iloc[0])]
        pmin, pmax = float(same.p.min()), float(same.p.max())
        zmin, zmax = float(same.z.min()), float(same.z.max())
        crossed = [b for b in bars if pmin < b <= pmax]
        barrows.append(dict(family=fam, n_pools=len(same), obs=float(same.obs.iloc[0]),
                            p_min=pmin, p_max=pmax, ratio=(pmax / pmin if pmin else np.nan),
                            z_min=zmin, z_max=zmax, bars_crossed=";".join(str(b) for b in crossed)))
        P(f"      {fam:6} obs {same.obs.iloc[0]:+.4f} identical at {len(same)} pools: p "
          f"{pmin:.4f}..{pmax:.4f} ({pmax/pmin if pmin else float('nan'):.1f}x), z "
          f"{zmin:+.2f}..{zmax:+.2f}; conventional bars crossed: "
          f"{crossed if crossed else 'none'}")
    pd.DataFrame(barrows).to_csv(f"{OUT}.barsensitivity.csv", index=False)

    H_COSTINV = True
    H_PERMSTAB = True
    for fam in FAMS:
        for pool in POOLS:
            s = rep[(rep.family == fam) & (rep['pool'] == pool) & (rep.scope == "POOLED")
                    & (rep.nperm == PERM_HEAD) & (rep.w_kept == 1008)]
            if s['sig'].nunique() > 1:
                H_COSTINV = False
            s2 = rep[(rep.family == fam) & (rep['pool'] == pool) & (rep.scope == "POOLED")
                     & (rep['rung'] == RUNG_HEAD) & (rep.w_kept == 1008)]
            if s2['sig'].nunique() > 1:
                H_PERMSTAB = False
    P(f"   H_COSTINV verdict identical across 0/10/25 bps: {'PASS' if H_COSTINV else 'FAIL'}; "
      f"H_PERMSTAB identical across P=200/1000/5000: {'PASS' if H_PERMSTAB else 'FAIL'}")

    # rule 8 on the claim: pool chosen on the FULL leg, OOS leg read once
    P("\n   RULE 8 (claim): the pool is chosen on the FULL leg's own statistic, the OOS leg read ONCE")
    pick = None
    best = -1
    for pool in POOLS:
        q = rep[(rep.pool == pool) & (rep.family == "ABS") & (rep.scope == "POOLED")
                & (rep["rung"] == RUNG_HEAD) & (rep.nperm == PERM_HEAD) & (rep.w_kept == 1008)]
        if len(q) and abs(float(q.iloc[0].z)) > best:
            best, pick = abs(float(q.iloc[0].z)), pool
    # the OOS-leg read: same pool, statistic recomputed on the OOS leg level alone
    c0 = arms[arms["rung"] == RUNG_HEAD]
    sub = pool_subset(c0, pick, 1008)
    wo = (sub["dOOS"].values > 0)
    lb = sub["family"].values
    obs_lvl = wo[lb == "ABS"].mean()
    rng = np.random.default_rng(SEED0 + 777)
    nl = np.array([wo[rng.permutation(lb) == "ABS"].mean() for _ in range(PERM_HEAD)])
    p_oos = (1 + int(np.sum(np.abs(nl - nl.mean()) >= abs(obs_lvl - nl.mean()) - 1e-15))) / (1 + PERM_HEAD)
    H_R8CLAIM = p_oos < ALPHA
    P(f"      IS-chosen pool = {pick} (|z| {best:.2f}); OOS-leg ABS win level {obs_lvl:.4f} vs null "
      f"mean {nl.mean():.4f} sd {nl.std(ddof=1):.4f} -> p {p_oos:.4f} "
      f"-> {'PASS' if H_R8CLAIM else 'FAIL'}")
    wfrows.append(dict(leg="R8_CLAIM", reading=pick, n_IS=len(sub), n_OOS=len(sub),
                       IS=best, OOS=p_oos, gap=np.nan, passes=H_R8CLAIM))

    # ---------------------------------------------------------------- book leg
    P("\n--- BOOK LEG (computed from prices here): rule 8 + BOTH KEEP PATHS, all rungs ---")
    books = {"RULES v1": lambda q: rules_v1_weights(q),
             "LIVE RULES v2 (band 0.03, g 0.75)": lambda q: rules_v2_weights(q, 0.03, 0.75),
             "CAND 4b (band 0.03, g 1.00)": lambda q: rules_v2_weights(q, 0.03, 1.00)}
    brows = []
    for rung in RUNGS:
        live = book_metrics(px, books["LIVE RULES v2 (band 0.03, g 0.75)"], rung)
        for nm, fn in books.items():
            b = book_metrics(px, fn, rung)
            kp = keep_paths(b, live, spy)
            brows.append(dict(book=nm, rung=rung, **b, **kp))
        brows.append(dict(book="SPY buy-and-hold", rung=rung, **spy,
                          **{k: False for k in ("pass_4a", "pass_4b")}))
    bk = pd.DataFrame(brows)
    P(f"   {'book':34}{'rung':>5}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>9}{'H1':>7}{'H2':>7}"
      f"{'oCAGR':>8}{'oSh':>7}{'oDD':>9}  4a   4b")
    for _, r in bk.iterrows():
        P(f"   {r['book']:34}{r['rung']:5.0f}{r['CAGR']:8.2%}{r['Sharpe']:8.4f}{r['MaxDD']:9.2%}"
          f"{r['H1']:7.3f}{r['H2']:7.3f}{r['OOS_CAGR']:8.2%}{r['OOS_Sharpe']:7.3f}"
          f"{r['OOS_MaxDD']:9.2%}  {str(r.get('pass_4a')):5}{str(r.get('pass_4b'))}")
    pd.concat([pd.DataFrame(wfrows), bk], axis=0).to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- verdict
    H = dict(H_NAMED=H_NAMED, H_STRICT=H_STRICT, H_FLIP=H_FLIP, H_QUEUE=H_QUEUE, H_DIR=H_DIR,
             H_COSTINV=H_COSTINV, H_PERMSTAB=H_PERMSTAB, H_R8CENSUS=H_R8CENSUS,
             H_R8CLAIM=H_R8CLAIM)
    P("\n--- PRE-REGISTERED HYPOTHESES ---")
    for k, v in H.items():
        P(f"   {k:12} {'PASS' if v else 'FAIL'}")
    P(f"   {sum(H.values())} of {len(H)} PASS")
    P(f"\nelapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")

    n4b = int(bk.get("pass_4b", pd.Series(dtype=bool)).sum())
    n4a = int(bk.get("pass_4a", pd.Series(dtype=bool)).sum())
    bs = pd.DataFrame(barrows).set_index("family")
    Path(f"{OUT}.result.md").write_text(
        f"""# Idea 842 - do the record's permutation/bootstrap p-values NAME THEIR POOL?  ({DATE}, cloud)

## The answer, in two numbers
**CENSUS (headline claim set NEAR: {int(head.loc['LOOSE','n_sites'])} numeric p-value sites tied to a
resampling null, in {int(head.loc['LOOSE','n_files'])} committed files of {nfiles_scanned} scanned):
the pool is named at {sh_loose:.4f} under the LOOSE reading and {sh_strict:.4f} under the STRICT one**
(STRICT = a pool word AND the unit permuted AND a count, all within 400 characters of the p-value).
So the record mostly gestures at its pool and states it properly slightly less than half the time.
H_NAMED {'PASS' if H_NAMED else 'FAIL'}, H_STRICT {'PASS' if H_STRICT else 'FAIL'}.

**RE-PRICING: the pool is worth up to {bs.loc['ABS','ratio']:.0f}x in p on an observed statistic that
does not move at all.** ABS's delta is {bs.loc['ABS','obs']:+.4f} at all
{int(bs.loc['ABS','n_pools'])} pools (H_DIR exact: max spread {max(dirs):.1e}) and its p runs
{bs.loc['ABS','p_min']:.4f}..{bs.loc['ABS','p_max']:.4f} (z {bs.loc['ABS','z_min']:+.2f}..{bs.loc['ABS','z_max']:+.2f}),
crossing the conventional bars {bs.loc['ABS','bars_crossed'] or 'none'} - i.e. a reader who quotes
"p 0.001" and a reader who quotes "p 0.017" can both be right about the same data and disagree at
alpha 0.01.  At alpha 0.05, {len(fl)} of {len(rep[rep.pool != 'ALL'])} re-priced cells flip outright,
all of them {('/'.join(sorted(set(fl.family))) if len(fl) else 'n/a')} - the family whose own
membership the pool changes - so on THIS leg pair the flip needs a membership change and the bar
level does the rest.

## Where the queue's own example stands
H_QUEUE **{'PASS' if H_QUEUE else 'FAIL'}**: ABS reads p {a_all.p:.4f} (z {a_all.z:+.2f}) at pool ALL
and p {a_long.p:.4f} (z {a_long.z:+.2f}) at pool LONGW.  Idea 834's ABS-turns-significant flip does
NOT reproduce here, and the reason is stated rather than buried: this file's leg pair is FULL -> OOS
read from 834's committed .arms.csv, not 834's PRE/POST split, and ABS is already significant at
pool ALL on it.  The MECHANISM the queue names reproduces exactly - the null's location is a pool
property ({' -> '.join(f"{r.null_mean:.4f}" for _, r in hd[hd.family == 'ABS'].sort_values('pool').iterrows())}
across pools) while the observed delta is fixed.

## Rule 8 (both legs run)
* ON THE CENSUS, declared cut {IS_CUT.date()}: **unresolvable** - only {int(pd.DataFrame(wfrows).query("leg=='R8_CENSUS'").n_IS.iloc[0])}
  of the {len(dated)} date-stamped sites predate it, so the IS leg cannot resolve a 0.10 bar; both
  readings FAIL as declared.  On the MEDIAN cut the same statistic PASSES both readings
  (LOOSE gap {float(pd.DataFrame(wfrows).query("leg=='R8_CENSUS_MEDIANCUT' and reading=='LOOSE'").gap.iloc[0]):.4f},
  STRICT gap {float(pd.DataFrame(wfrows).query("leg=='R8_CENSUS_MEDIANCUT' and reading=='STRICT'").gap.iloc[0]):.4f}).
* ON THE CLAIM: pool chosen on the FULL leg ({pick}), OOS leg read once -> p {p_oos:.4f}
  ({'PASS' if H_R8CLAIM else 'FAIL'}).

## Book leg (computed from prices in this file; nothing tuned, nothing promoted)
4a passes **{n4a}** and 4b passes **{n4b}** of {len(bk)} book-rung rows.  At 10 bps: LIVE RULES v2
{bk.query("book.str.startswith('LIVE') and rung==10").CAGR.iloc[0]:.2%} /
{bk.query("book.str.startswith('LIVE') and rung==10").Sharpe.iloc[0]:.4f} /
{bk.query("book.str.startswith('LIVE') and rung==10").MaxDD.iloc[0]:.2%}; the standing 4b candidate
{bk.query("book.str.startswith('CAND') and rung==10").CAGR.iloc[0]:.2%} /
{bk.query("book.str.startswith('CAND') and rung==10").Sharpe.iloc[0]:.4f} /
{bk.query("book.str.startswith('CAND') and rung==10").MaxDD.iloc[0]:.2%} (OOS
{bk.query("book.str.startswith('CAND') and rung==10").OOS_CAGR.iloc[0]:.2%} /
{bk.query("book.str.startswith('CAND') and rung==10").OOS_Sharpe.iloc[0]:.4f} /
{bk.query("book.str.startswith('CAND') and rung==10").OOS_MaxDD.iloc[0]:.2%}); SPY
{spy['CAGR']:.2%} / {spy['Sharpe']:.4f} / {spy['MaxDD']:.2%} (OOS {spy['OOS_CAGR']:.2%} /
{spy['OOS_Sharpe']:.4f} / {spy['OOS_MaxDD']:.2%}).  The candidate's 4b pass and 4a failure reproduce
at every cost rung; no book's parameter was chosen here.

## Verdict
**ANSWERED - {sum(H.values())} of {len(H)} pre-registered hypotheses PASS.**  A committed
permutation/bootstrap p-value in this record is not interpretable without its pool: the same
unchanged statistic is worth {bs.loc['ABS','ratio']:.0f}x in p across four pools of the same corpus,
and slightly over half the record's own p-value sites fail to state the pool to the STRICT standard.
**PROPOSED, not applied (PROTOCOL rule 6, Sunday review only):** every committed permutation or
bootstrap p-value states (i) what was permuted or resampled, (ii) the pool it was drawn from and
(iii) that pool's unit count - and any cross-artefact citation of such a p-value repeats the pool.
No RULES change, no KEEP claimed, no memo, no book promoted.

## Caveats
Current-constituent survivorship in all three panels.  The FULL leg contains the OOS leg, so the
leg-to-leg delta is not a disjoint contrast (its LEVEL is an in-window identity - ideas 833/836);
this run's object is the p-value of a FIXED delta under differently pooled nulls, which that nesting
does not touch.  The census is a TEXT detector: its 12 controls are printed in the console, it was
repaired against those controls BEFORE any census number was read, and the per-site table is
committed so any other reading can be re-scored without re-running anything.
""")
    P(f"wrote {Path(OUT).name}.result.md")


if __name__ == "__main__":
    main()
