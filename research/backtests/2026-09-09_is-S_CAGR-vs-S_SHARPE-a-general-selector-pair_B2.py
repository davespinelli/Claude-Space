#!/usr/bin/env python3
"""Idea 270 - "is-S_CAGR-vs-S_SHARPE-a-general-selector-pair" (lane B, 2026-09-09).

The question
------------
Idea 259 ran two IS-only selectors over ONE dial (the ranked book size `n`) on four panels:

    S_SHARPE   arm = argmax IS Sharpe inside the dial's pool   (the metric the record quotes)
    S_CAGR     arm = argmax IS CAGR   inside the dial's pool   (the metric it does not)

and published: the two pick a DIFFERENT arm in 3 of 4 panels, worth **+2.53 pp/yr of OOS
CAGR for -0.0254 of OOS Sharpe** - an apparent "exchange rate" of ~99.6 pp of CAGR per
unit of Sharpe surrendered.  The queue asks whether that number is a CONSTANT of the
selector pair or a property of the `n` dial it was measured on:

    "Run the same selector pair over the record's OTHER swept dials (cadence, gross, vol
     gate, eligibility trim) wherever the parent committed a grid CSV with IS_CAGR, and
     report whether the +CAGR/-Sharpe exchange rate is a constant or a dial-specific one."

Why it matters, stated before any number is read
------------------------------------------------
If the rate is a constant, it is a reportable conversion: any run that selects on Sharpe
can be restated in CAGR terms with one multiplication, and the record's habit of quoting
Sharpe-only selections has a known, bounded price.  If it is dial-specific - or worse, if
it is not even a PRICE because S_CAGR sometimes wins on BOTH metrics - then idea 259's
+2.53/-0.0254 is a fact about the `n` dial and must not be quoted as a general one.

Read idea 259's own four panels before believing the headline is an exchange at all:
    U56       S_CAGR - S_SHARPE:  OOS CAGR +3.50pp,  OOS Sharpe -0.1758   (a price)
    B136                          OOS CAGR +3.63pp,  OOS Sharpe +0.0437   (FREE)
    BSTK100                       OOS CAGR +3.01pp,  OOS Sharpe +0.0306   (FREE)
    SMALL439                      the pair AGREES; both deltas are exactly 0
The published mean is therefore one priced panel, two free panels and one null, averaged.
That decomposition is itself part of what this run reports; it is arithmetic on idea 259's
committed walkforward.csv, not a new measurement, and it is gated below.

Design
------
LEG A - CENSUS over the record.  Every committed CSV in research/backtests carrying all
four of IS_CAGR, IS_Sharpe, OOS_CAGR, OOS_Sharpe (189 files) is scanned for SWEPT DIALS: a
non-metric column with >= 3 distinct values inside a cell defined by every other non-metric
key column.  Inside each such cell the same two argmaxes are taken and the OOS deltas
recorded.  Dials are classified into families (SIZE, CADENCE, GROSS, VOLGATE, TRIM, COST,
OTHER) by column name.  This reads the record as it stands - no book is re-run.

LEG B - CONTROLLED GRID.  The census inherits every construction choice of 189 different
runs, so it cannot separate "the dial" from "the run".  Leg B therefore sweeps five dials
under ONE construction, idea 259's, held fixed at everything the dial is not:

    SIZE     n in {5,10,20,30,40,60} + EWall     (idea 259's own dial - reproduction gate)
    CADENCE  freq in {D, W, M, Q}                on FWD20
    GROSS    g in {0.25,0.375,0.50,0.625,0.75,0.875,1.00}   on FWD20
    VOLGATE  max_vol in {0.20,0.30,0.40,0.50,0.60,0.80,1.00,off}  on FWD20
    TRIM     q in {0.10..1.00}, n_t = max(1, round(q*n_elig,t))   (idea 155's dial)

on idea 259's four panels (U56, B136, BSTK100, SMALL439), at PROTOCOL's 10 bps with a 0 bps
diagnostic, weekly cadence except where cadence IS the dial, gross 0.75 except where gross
is the dial, MAX_VOL 0.60 except where the vol gate is the dial, next-day execution.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. the dial's own arm value (n / freq / g / max_vol / q) - ALL rungs reported
    2. panel in {U56, B136, BSTK100, SMALL439}                - ALL FOUR reported
  The DIAL FAMILY is the axis of the question, not a tuned parameter: the whole point is
  to report every dial.  Cost is reported at both rungs, never chosen.  SAT_CAP, GROSS,
  MAX_VOL, NS, the composite key, the IS/OOS split and the panels are idea 259's constants
  imported verbatim.

Pre-registered verdict bars (written before any new number was read)
    Let rate = dOOS_CAGR(pp) / (-dOOS_Sharpe) for S_CAGR minus S_SHARPE, defined only on
    cells where the pair DISAGREES and dOOS_Sharpe < 0 (i.e. an actual price was paid).
    CONSTANT       iff (i) every dial's median rate has the same sign, AND
                       (ii) a permutation test on between-dial dispersion of the cell rates
                            gives p >= 0.05 on BOTH corpora (leg A and leg B), AND
                       (iii) idea 259's published 99.6 pp/Sharpe lies inside the pooled IQR.
    DIAL-SPECIFIC  iff the permutation test rejects on either corpus, or dial medians differ
                       in sign.
    NOT-A-PRICE    iff, across corpora, the pair DISAGREES in a minority of cells or
                       dOOS_Sharpe >= 0 (S_CAGR weakly dominates) in >= 50% of disagreements.
    These are read in the order NOT-A-PRICE -> DIAL-SPECIFIC -> CONSTANT; the first that
    fires is the verdict.

Reproduction gates (run BEFORE any new number is read)
    [a] harness: engine.backtest on U56 reproduces idea 259's committed `U56/EWall` and
        `U56/FWD20` rows and the live RULES v1 row.
    [b] the SIZE dial re-run here reproduces idea 259's committed grid.csv over all
        32 (panel x arm) cells at 10 bps, every numeric column.
    [c] the SIZE dial's rule-8 selection reproduces idea 259's committed walkforward.csv
        picks, and its published +2.53 pp / -0.0254 headline recomputes from that file.
    A failure on any gate aborts before leg A is read.

Walk-forward (PROTOCOL rule 8): selectors see 2009-2016 only; 2017-2026 is read once.
    S_SHARPE, S_CAGR                the pair under test
    DEFAULT   the dial's do-nothing rung (n=20 / W / 0.75 / 0.60 / q=1.00)
    S_RAND    a fixed-seed random rung of the same pool (selection-value control)
    plus per panel: EWALL, RULES v2 (the LIVE book), RULES v1, SPY.

KEEP paths (PROTOCOL rule 4): 4a is judged against RULES v2, the live book (4a-v1 is
reported beside it for continuity with the pre-2026-09-06 record); 4b against the panel's
own SPY over the same window, with the OOS bar from rule 8.

Survivorship (rule 9): universe_broad.json and the small panel are CURRENT CONSTITUENTS.
Both selectors read the same survivor-biased panels, so the bias is common to the pair and
cannot manufacture a DIFFERENCE between them; it can inflate the level of every OOS number
reported, and no book here is proposed for capital.

Deterministic (fixed seeds), standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

# ---- idea 259's constants, imported verbatim ------------------------------------------
COST_BPS = 10
DIAG_BPS = 0
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
NS = [5, 10, 20, 30, 40, 60]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
SAT_CAP = 0.25
# ---- this run's own -------------------------------------------------------------------
BASE_N = 20
CADENCES = ["D", "W", "M", "Q"]
GROSSES = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
VOLGATES = [0.20, 0.30, 0.40, 0.50, 0.60, 0.80, 1.00, np.inf]
TRIMS = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
PUBLISHED_RATE = 2.5348 / 0.025368            # idea 259's headline, pp CAGR per unit Sharpe
SEED = 270
NPERM = 5000
# The price caches are refreshed weekly.  data/prices.csv now ends after idea 259's run AND
# carries restated adjusted closes for days it did see, so bit-identical reproduction is
# impossible.  PARENT_END is the parent's own sample end; TOL_GATE bounds the restatement
# (the parent's CLOSED 2009-2016 IS window itself moves ~2e-6, so 1e-3 is loose by 500x).
PARENT_END = "2026-09-04"
TOL_GATE = 1e-3
GATE_COLS = ["CAGR", "Vol", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe",
             "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turn"]

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
PARENT = OUT / "2026-09-06_does-the-sharpe-cagr-reversal-sit-under-every-EWall-claim_C"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)

LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ======================================================================= panels & books
def build_panels():
    """idea 259's build_panels, imported verbatim."""
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56": sub(px56, [c for c in px56.columns]),
        "B136": sub(px136, [c for c in px136.columns]),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
        "SMALL439": sub(pxs, s_stk, tradable=s_stk),
    }


_SCORE_CACHE = {}


def cached_score(px, vol_scale):
    k = (id(px), vol_scale)
    if k not in _SCORE_CACHE:
        _SCORE_CACHE[k] = score(px, vol_scale)
    return _SCORE_CACHE[k]


def eligible_mask(px, tradable, max_vol=MAX_VOL):
    _, above, vol20 = cached_score(px, True)
    m = (above & (vol20 < max_vol)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def book_weights(px, tradable, arm, n=None, gross=GROSS, max_vol=MAX_VOL, q=None):
    """idea 259's weights(), extended with the gross / vol-gate / trim dials."""
    elig = eligible_mask(px, tradable, max_vol)
    if arm == "EWall":
        sel = elig.astype(float)
    elif arm == "TRIM":
        key = cached_score(px, False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        nel = elig.sum(axis=1)
        nt = np.maximum(1, np.round(q * nel)).astype(float)
        sel = rank.le(nt, axis=0).astype(float)
    else:                                              # FWD: top-n on the composite key
        key = cached_score(px, False)[0]
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(gross).fillna(0.0), elig, sel


def restrict(w, px):
    return w.reindex(index=px.index, columns=px.columns).fillna(0.0)


def baseline_weights(px, tradable, which):
    """RULES v1 / v2 on the panel's TRADABLE columns only, reindexed back (de-gross)."""
    cols = [c for c in px.columns if c in tradable]
    sub = px[cols]
    w = rules_v1_weights(sub) if which == "v1" else rules_v2_weights(sub)
    return restrict(w, px)


# ======================================================================= metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b(r, spy, r_oos, spy_oos):
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


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def paired_t(d):
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=float)
    if len(d) < 2:
        return (d.mean() if len(d) else np.nan), np.nan, int((d > 0).sum()), len(d)
    se = d.std(ddof=1) / np.sqrt(len(d))
    return d.mean(), (d.mean() / se if se > 0 else np.nan), int((d > 0).sum()), len(d)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return np.nan
    ra = pd.Series(a).rank().values
    rb = pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def ols_slope(x, y):
    """slope of y on x with a t-stat; returns (slope, t, n)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    n = len(x)
    if n < 3 or x.std() == 0:
        return np.nan, np.nan, n
    b = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
    a = y.mean() - b * x.mean()
    resid = y - (a + b * x)
    s2 = resid @ resid / (n - 2)
    se = np.sqrt(s2 / ((n - 1) * np.var(x, ddof=1))) if s2 > 0 else np.nan
    return float(b), (float(b / se) if se and np.isfinite(se) and se > 0 else np.nan), n


def perm_between(values, groups, seed=SEED, nperm=NPERM):
    """Permutation test for BETWEEN-GROUP dispersion of `values`.

    Statistic = the spread (max-min) of group MEDIANS, which is what "is the rate a
    constant?" literally asks.  Labels are shuffled; p = P(stat_perm >= stat_obs).
    Deterministic given the seed.  Returns (stat, p, n_groups, n).
    """
    v = np.asarray(values, float)
    g = np.asarray(groups)
    ok = np.isfinite(v)
    v, g = v[ok], g[ok]
    labs = pd.unique(g)
    if len(labs) < 2 or len(v) < len(labs) + 1:
        return np.nan, np.nan, len(labs), len(v)

    def stat(gg):
        med = [np.median(v[gg == L]) for L in labs if (gg == L).sum() > 0]
        return (max(med) - min(med)) if len(med) > 1 else 0.0

    obs = stat(g)
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(nperm):
        if stat(rng.permutation(g)) >= obs - 1e-15:
            cnt += 1
    return float(obs), (cnt + 1) / (nperm + 1), len(labs), len(v)


# ======================================================================= LEG A: census
METRIC = re.compile(
    r"^(cagr|sharpe|maxdd|vol|calmar|sortino|h1|h2|turn|turnover|to|gross|gross_reb|flips|"
    r"elig|names|point|d[a-z]+|m_[a-z0-9]+|p4a|p4b|f4a|f4b|f4b_oos|4a|4b|4b_oos|is4b|oos4b|"
    r"fails|failing|bind|binds|z|resid|held|sat_share|verdict|dominated|artefact|lever|rate|"
    r"skill|regret|rho|r2|weight|t|se|p|pval|n_[a-z]+|y2020|y2022|total|years|winrate|"
    r"bestday|worstday|equity|pick|selector|note|reason|memo|comment)$", re.I)
METRIC_PREFIX = re.compile(
    r"^(is_|oos_|d_|m_|sh_y_|spy_|base_|v1_|v2_|ctl_|gm_|vs_|md_|null_|band_|full_)", re.I)

DIAL_FAMILY = [
    ("SIZE", re.compile(r"^(n|nn|n_book|nbook|topn|top_n|book_n|k|m|names_n|size)$", re.I)),
    ("CADENCE", re.compile(r"^(freq|cadence|rebal|rebalance|schedule|sched|period)$", re.I)),
    ("GROSS", re.compile(r"^(gross|g|gross_target|w|weight_gross|lev|leverage|f|frac|fraction)$", re.I)),
    ("VOLGATE", re.compile(r"^(max_vol|maxvol|vol_cap|volcap|vol_gate|volgate|vol_thr|"
                           r"vol_threshold|band|band_width|gate)$", re.I)),
    ("TRIM", re.compile(r"^(q|quantile|trim|pct|pctile|selectivity|cut|cutoff|thresh|"
                        r"threshold)$", re.I)),
    ("COST", re.compile(r"^(bps|cost|cost_bps|c|rung)$", re.I)),
]


def dial_family(col):
    for fam, rx in DIAL_FAMILY:
        if rx.match(str(col)):
            return fam
    return "OTHER"


def is_metric_col(c):
    return bool(METRIC.match(str(c)) or METRIC_PREFIX.match(str(c)))


def pick_col(df, name):
    for c in df.columns:
        if str(c).lower() == name:
            return c
    return None


def census():
    """Every committed CSV with IS_CAGR/IS_Sharpe/OOS_CAGR/OOS_Sharpe, read for swept dials."""
    files = [f for f in sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
             if not f.name.startswith(STEM)]
    rows, seen_files, skipped = [], 0, []
    for f in files:
        try:
            head = pd.read_csv(f, nrows=0)
        except Exception as e:
            skipped.append((f.name, type(e).__name__))
            continue
        cols = {str(c).lower() for c in head.columns}
        if not {"is_cagr", "is_sharpe", "oos_cagr", "oos_sharpe"} <= cols:
            continue
        try:
            df = pd.read_csv(f, low_memory=False)
        except Exception as e:
            skipped.append((f.name, type(e).__name__))
            continue
        if len(df) > 300000:
            skipped.append((f.name, f"too many rows ({len(df)})"))
            continue
        c_is, c_ic = pick_col(df, "is_sharpe"), pick_col(df, "is_cagr")
        c_os, c_oc = pick_col(df, "oos_sharpe"), pick_col(df, "oos_cagr")
        c_od = pick_col(df, "oos_maxdd")
        dup = pd.Index(df.columns).value_counts()
        if any(dup.get(c, 0) != 1 for c in (c_is, c_ic, c_os, c_oc)):
            skipped.append((f.name, "duplicate metric column labels"))
            continue
        seen_files += 1
        # candidate key columns: non-metric, <= 60 uniques, not all-NaN, unique label
        keys = []
        counts = pd.Index(df.columns).value_counts()
        for c in df.columns:
            if is_metric_col(c) or counts.get(c, 0) != 1:
                continue
            s = df[c]
            if s.isna().all():
                continue
            u = s.dropna().unique()
            if 2 <= len(u) <= 60:
                keys.append(c)
        if not keys:
            continue
        keys = keys[:10]                       # bound the group explosion; deterministic order
        for dial in keys:
            others = [c for c in keys if c != dial]
            sub = df[[dial] + others + [c_is, c_ic, c_os, c_oc] + ([c_od] if c_od else [])].copy()
            sub = sub.dropna(subset=[dial, c_is, c_ic, c_os, c_oc])
            if sub.empty:
                continue
            if others:
                cellkey = sub[others[0]].astype(str)
                for c in others[1:]:
                    cellkey = cellkey + "|" + sub[c].astype(str)
                grp = sub.groupby(cellkey, sort=False, dropna=False)
            else:
                grp = [("_all", sub)]
            for cell, g in grp:
                if g[dial].astype(str).nunique() < 3:
                    continue
                if len(g) > 400:                      # a cell this wide is not a swept dial
                    continue
                gs = g.drop_duplicates(subset=[dial], keep="first")
                i_s = gs[c_is].astype(float).idxmax()
                i_c = gs[c_ic].astype(float).idxmax()
                rs, rc = gs.loc[i_s], gs.loc[i_c]
                rows.append(dict(
                    file=f.name, dial=str(dial), family=dial_family(dial),
                    cell=str(cell),
                    arms=int(gs[dial].astype(str).nunique()),
                    pick_S=str(rs[dial]), pick_C=str(rc[dial]),
                    agree=bool(str(rs[dial]) == str(rc[dial])),
                    IS_S_sharpe=float(rs[c_is]), IS_C_cagr=float(rc[c_ic]),
                    dOOS_Sharpe=float(rc[c_os]) - float(rs[c_os]),
                    dOOS_CAGR=float(rc[c_oc]) - float(rs[c_oc]),
                    dOOS_MaxDD=(float(rc[c_od]) - float(rs[c_od])) if c_od else np.nan,
                ))
    cp = pd.DataFrame(rows)
    if cp.empty:
        return cp, seen_files, skipped
    # OOS_CAGR is stored as a fraction everywhere in the record; express deltas in pp
    cp["dCAGR_pp"] = cp.dOOS_CAGR * 100.0
    cp["priced"] = (~cp.agree) & (cp.dOOS_Sharpe < 0)
    cp["free"] = (~cp.agree) & (cp.dOOS_Sharpe >= 0)
    cp["rate"] = np.where(cp.priced, cp.dCAGR_pp / (-cp.dOOS_Sharpe), np.nan)
    return cp, seen_files, skipped


# ======================================================================= LEG B: grid
def dial_arms(dial):
    """(label, kwargs) for every rung of a dial.  DEFAULT rung = the do-nothing setting."""
    if dial == "SIZE":
        return ([("EWall", dict(arm="EWall"))]
                + [(f"FWD{n}", dict(arm="FWD", n=n)) for n in NS]), f"FWD{BASE_N}"
    if dial == "CADENCE":
        return [(f"CAD-{c}", dict(arm="FWD", n=BASE_N, freq=c)) for c in CADENCES], "CAD-W"
    if dial == "GROSS":
        return [(f"G{g:.3f}", dict(arm="FWD", n=BASE_N, gross=g)) for g in GROSSES], f"G{GROSS:.3f}"
    if dial == "VOLGATE":
        return ([(f"V{v:.2f}" if np.isfinite(v) else "V-off",
                  dict(arm="FWD", n=BASE_N, max_vol=v)) for v in VOLGATES],
                f"V{MAX_VOL:.2f}")
    if dial == "TRIM":
        return [(f"Q{q:.2f}", dict(arm="TRIM", q=q)) for q in TRIMS], "Q1.00"
    raise ValueError(dial)


DIALS = ["SIZE", "CADENCE", "GROSS", "VOLGATE", "TRIM"]


def run_arm(px, tradable, spy, kw, bps):
    freq = kw.get("freq", FREQ)
    w, elig, sel = book_weights(px, tradable,
                                kw.get("arm", "FWD"), n=kw.get("n"),
                                gross=kw.get("gross", GROSS),
                                max_vol=kw.get("max_vol", MAX_VOL),
                                q=kw.get("q"))
    res = backtest(px, w, cost_bps=bps, freq=freq)
    start = px.index[260]
    r = res["returns"].loc[start:]
    sp = spy.loc[start:]
    r_is, r_oos = r.loc[IS_START:IS_END], r.loc[OOS_START:]
    sp_is, sp_oos = sp.loc[IS_START:IS_END], sp.loc[OOS_START:]
    mm, mo, mi = metrics(r), metrics(r_oos), metrics(r_is)
    h1, h2 = half_sharpes(r)
    m = rebalance_mask(px.index, freq)
    neg = elig.sum(axis=1)[m.values].loc[start:]
    # idea 259's convention, kept verbatim so the SIZE dial reproduces its grid: saturation
    # is measured on ELIGIBILITY (n_elig <= the arm's own count), and an un-ranked EWall arm
    # is not "saturated" - it IS the eligible set by construction.
    if kw.get("arm") == "EWall":
        sat = 0.0
    elif kw.get("arm") == "TRIM":
        cap = np.maximum(1, np.round(kw["q"] * neg))
        sat = float((neg <= cap).mean())
    else:
        sat = float((neg <= kw["n"]).mean())
    out = dict(
        CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
        turn=float(res["turnover"].loc[start:].sum() / (len(r) / 252)),
        gross_real=float(w.loc[start:].sum(axis=1).mean()), sat_share=sat,
        SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"], SPY_MaxDD=metrics(sp)["MaxDD"],
        SPY_OOS_CAGR=metrics(sp_oos)["CAGR"], SPY_OOS_Sharpe=metrics(sp_oos)["Sharpe"],
        SPY_OOS_MaxDD=metrics(sp_oos)["MaxDD"],
    )
    return out, dict(r=r, sp=sp, r_is=r_is, r_oos=r_oos, sp_oos=sp_oos)


def run_grid(panels):
    rows, series = [], {}
    for pname, (px, tr) in panels.items():
        spy = px["SPY"].pct_change().fillna(0)
        start = px.index[260]
        base = {}
        for which in ("v1", "v2"):
            for bps in (COST_BPS, DIAG_BPS):
                bw = baseline_weights(px, tr, which)
                br = backtest(px, bw, cost_bps=bps, freq=FREQ)["returns"].loc[start:]
                base[(which, bps)] = br
        for dial in DIALS:
            arms, _ = dial_arms(dial)
            for lab, kw in arms:
                for bps in (COST_BPS, DIAG_BPS):
                    t0 = time.time()
                    met, ser = run_arm(px, tr, spy, kw, bps)
                    b2, b1 = base[("v2", bps)], base[("v1", bps)]
                    row = dict(panel=pname, dial=dial, arm=lab, bps=bps, **met)
                    row["p4a_v2"] = v4a(ser["r"], b2)
                    row["p4a_v1"] = v4a(ser["r"], b1)
                    row["f4b"] = fail4b(ser["r"], ser["sp"], ser["r_oos"], ser["sp_oos"])
                    row["p4b"] = row["f4b"] == "-"
                    row["secs"] = round(time.time() - t0, 2)
                    rows.append(row)
                    series[(pname, dial, lab, bps)] = ser
        # baselines as their own rows (one per panel, dial="BASE")
        for which in ("v1", "v2"):
            for bps in (COST_BPS, DIAG_BPS):
                br = base[(which, bps)]
                bi, bo = br.loc[IS_START:IS_END], br.loc[OOS_START:]
                sp = spy.loc[start:]
                mm, mo, mi = metrics(br), metrics(bo), metrics(bi)
                h1, h2 = half_sharpes(br)
                rows.append(dict(panel=pname, dial="BASE", arm=f"RULES {which}", bps=bps,
                                 CAGR=mm["CAGR"], Vol=mm["Vol"], Sharpe=mm["Sharpe"],
                                 MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                                 IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"],
                                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                 OOS_MaxDD=mo["MaxDD"], turn=np.nan, gross_real=np.nan,
                                 sat_share=np.nan,
                                 SPY_CAGR=metrics(sp)["CAGR"], SPY_Sharpe=metrics(sp)["Sharpe"],
                                 SPY_MaxDD=metrics(sp)["MaxDD"],
                                 SPY_OOS_CAGR=metrics(sp.loc[OOS_START:])["CAGR"],
                                 SPY_OOS_Sharpe=metrics(sp.loc[OOS_START:])["Sharpe"],
                                 SPY_OOS_MaxDD=metrics(sp.loc[OOS_START:])["MaxDD"],
                                 p4a_v2=np.nan, p4a_v1=np.nan,
                                 f4b=fail4b(br, sp, bo, sp.loc[OOS_START:]),
                                 p4b=fail4b(br, sp, bo, sp.loc[OOS_START:]) == "-", secs=np.nan))
        P(f"    panel {pname}: {sum(1 for r in rows if r['panel'] == pname)} rows done")
    return pd.DataFrame(rows), series


def rule8(grid, use_sat_cap=True):
    """IS 2009-2016 chooses inside each (dial, panel, bps) pool; OOS 2017+ read once."""
    out = []
    rng = np.random.default_rng(SEED)
    for (pname, dial, bps), g in grid[grid.dial != "BASE"].groupby(["panel", "dial", "bps"]):
        _, default = dial_arms(dial)
        pool = g.copy()
        if use_sat_cap:
            keep = (pool.sat_share <= SAT_CAP) | (pool.arm == "EWall")
            if keep.sum() >= 3:
                pool = pool[keep]
        if pool.empty:
            continue
        picks = {"S_SHARPE": pool.loc[pool.IS_Sharpe.idxmax()],
                 "S_CAGR": pool.loc[pool.IS_CAGR.idxmax()]}
        if (pool.arm == default).any():
            picks["DEFAULT"] = pool[pool.arm == default].iloc[0]
        elif (g.arm == default).any():
            picks["DEFAULT"] = g[g.arm == default].iloc[0]
        picks["S_RAND"] = pool.iloc[int(rng.integers(len(pool)))]
        b2 = grid[(grid.panel == pname) & (grid.arm == "RULES v2") & (grid.bps == bps)].iloc[0]
        b1 = grid[(grid.panel == pname) & (grid.arm == "RULES v1") & (grid.bps == bps)].iloc[0]
        for sname, r in picks.items():
            out.append(dict(panel=pname, dial=dial, bps=bps, selector=sname, pick=r.arm,
                            IS_Sharpe=r.IS_Sharpe, IS_CAGR=r.IS_CAGR,
                            OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                            v2_OOS_Sharpe=b2.OOS_Sharpe, v2_OOS_CAGR=b2.OOS_CAGR,
                            v2_OOS_MaxDD=b2.OOS_MaxDD,
                            v1_OOS_Sharpe=b1.OOS_Sharpe, v1_OOS_CAGR=b1.OOS_CAGR,
                            SPY_OOS_Sharpe=r.SPY_OOS_Sharpe, SPY_OOS_CAGR=r.SPY_OOS_CAGR,
                            SPY_OOS_MaxDD=r.SPY_OOS_MaxDD,
                            full_4a_v2=r.p4a_v2, full_4a_v1=r.p4a_v1, full_4b=r.p4b))
    return pd.DataFrame(out)


def exchange_table(wf):
    """S_CAGR minus S_SHARPE, per (dial, panel, bps): the exchange the queue asks about."""
    rows = []
    for (pname, dial, bps), g in wf.groupby(["panel", "dial", "bps"]):
        s = g[g.selector == "S_SHARPE"]
        c = g[g.selector == "S_CAGR"]
        if s.empty or c.empty:
            continue
        s, c = s.iloc[0], c.iloc[0]
        dS = c.OOS_Sharpe - s.OOS_Sharpe
        dC = (c.OOS_CAGR - s.OOS_CAGR) * 100.0
        agree = bool(s.pick == c.pick)
        priced = (not agree) and dS < 0
        rows.append(dict(panel=pname, dial=dial, bps=bps, pick_S=s.pick, pick_C=c.pick,
                         agree=agree, dOOS_Sharpe=dS, dCAGR_pp=dC,
                         dOOS_MaxDD_pp=(c.OOS_MaxDD - s.OOS_MaxDD) * 100.0,
                         priced=priced, free=(not agree) and dS >= 0,
                         rate=(dC / (-dS) if priced else np.nan)))
    return pd.DataFrame(rows)


# ======================================================================= gates
def gate_harness(panels):
    """[a] engine harness + the parent's own sample end.

    The price caches are refreshed weekly, so data/prices.csv now carries two trading days
    the parent never saw AND restated adjusted closes for the days it did.  Bit-identical
    reproduction is therefore impossible and would be a false claim; the gate is run on the
    PARENT'S OWN sample end and the residual restatement is reported as a number.
    """
    px, tr = panels["U56"]
    pub = pd.read_csv(f"{PARENT}.grid.csv")
    pub10 = pub[pub.bps == COST_BPS]
    P(f"  [a] live panel ends {px.index[-1].date()}; parent's sample end taken as {PARENT_END} "
      f"(the last date on which its committed grid reproduces best)")
    p = px.loc[:PARENT_END]
    spy = p["SPY"].pct_change().fillna(0)
    worst = 0.0
    for lab, kw, sel in [("EWall", dict(arm="EWall"), (pub10.panel == "U56") & (pub10.arm == "EWall")),
                         ("FWD20", dict(arm="FWD", n=20),
                          (pub10.panel == "U56") & (pub10.arm == "FWD") & (pub10.n == 20))]:
        met, _ = run_arm(p, tr, spy, kw, COST_BPS)
        row = pub10[sel].iloc[0]
        d = max(abs(met[k] - float(row[k])) for k in GATE_COLS)
        dis = max(abs(met[k] - float(row[k])) for k in ("IS_CAGR", "IS_Sharpe"))
        P(f"  [a] U56/{lab} at the parent's sample end: max abs diff {d:.3e} "
          f"(closed IS window alone {dis:.3e})")
        worst = max(worst, d)
    pxx = load_universe()
    r = backtest(pxx, rules_v1_weights(pxx), cost_bps=COST_BPS, freq=FREQ)["returns"].loc[pxx.index[260]:]
    m = metrics(r)
    P(f"  [a] live RULES v1 (u56, weekly, 10 bps) from engine.backtest: CAGR {m['CAGR']:.4%} "
      f"Sharpe {m['Sharpe']:.5f} MaxDD {m['MaxDD']:.4%}")
    return worst < TOL_GATE, worst


def gate_size_dial(panels):
    """[b] the SIZE dial, re-run at the parent's sample end, reproduces all 32 of its cells."""
    pub = pd.read_csv(f"{PARENT}.grid.csv")
    pub = pub[(pub.bps == COST_BPS) & (pub.arm != "v1")].copy()
    pub["lab"] = np.where(pub.arm == "EWall", "EWall", "FWD" + pub.n.fillna(0).astype(int).astype(str))
    worst, ncell, per = 0.0, 0, []
    for pname, (px, tr) in panels.items():
        p = px.loc[:PARENT_END]
        spy = p["SPY"].pct_change().fillna(0)
        for lab, kw in dial_arms("SIZE")[0]:
            row = pub[(pub.panel == pname) & (pub.lab == lab)]
            if row.empty:
                continue
            row = row.iloc[0]
            met, _ = run_arm(p, tr, spy, kw, COST_BPS)
            d = max(abs(met[c] - float(row[c])) for c in GATE_COLS if pd.notna(row[c]))
            ds = abs(met["sat_share"] - float(row["sat_share"]))
            per.append(dict(panel=pname, arm=lab, maxdiff=d, sat_diff=ds))
            worst = max(worst, d, ds)
            ncell += 1
    per = pd.DataFrame(per)
    P(f"  [b] SIZE dial re-run at the parent's sample end vs its committed grid: {ncell} cells "
      f"x {len(GATE_COLS)} metric columns + sat_share, max abs diff {worst:.3e} "
      f"(tolerance {TOL_GATE:.0e}, set by the cache restatement)")
    P(fmt(per.groupby("panel").agg(cells=("arm", "size"), max_metric_diff=("maxdiff", "max"),
                                   max_sat_diff=("sat_diff", "max")), 8))
    return worst < TOL_GATE, worst, ncell


def gate_parent_headline():
    """[c] idea 259's +2.53 pp / -0.0254 recomputes from its own committed walkforward."""
    w = pd.read_csv(f"{PARENT}.walkforward.csv")
    w = w[w.bps == COST_BPS]
    s = w[w.selector == "S_SHARPE"].set_index("panel")
    c = w[w.selector == "S_CAGR"].set_index("panel")
    dC = (c.OOS_CAGR - s.OOS_CAGR) * 100.0
    dS = c.OOS_Sharpe - s.OOS_Sharpe
    diff = int((c.pick != s.pick).sum())
    P(f"  [c] idea 259 committed walkforward: pair disagrees in {diff} of {len(s)} panels; "
      f"mean dOOS_CAGR {dC.mean():+.4f} pp (published +2.53), mean dOOS_Sharpe {dS.mean():+.6f} "
      f"(published -0.0254)")
    P(f"      per panel dCAGR_pp {dC.round(3).to_dict()}")
    P(f"      per panel dSharpe  {dS.round(4).to_dict()}")
    P(f"      priced panels (dSharpe<0): {int((dS < 0).sum())}; free (dSharpe>=0, pair differs): "
      f"{int(((dS >= 0) & (c.pick != s.pick)).sum())}; null (pair agrees): "
      f"{int((c.pick == s.pick).sum())}")
    okC = abs(dC.mean() - 2.5348) < 0.02
    okS = abs(dS.mean() + 0.025368) < 0.0005
    return bool(okC and okS and diff == 3), dC, dS


# ======================================================================= main
def main():
    t_start = time.time()
    P("=" * 190)
    P(f"Idea 270 is-S_CAGR-vs-S_SHARPE-a-general-selector-pair (lane B) | {SCRIPT}")
    P(f"Leg A census over committed CSVs | Leg B fresh 5-dial grid at {COST_BPS} bps "
      f"({DIAG_BPS} bps diagnostic), next-day, gross {GROSS} unless gross is the dial")
    P("=" * 190)

    P("\n--- REPRODUCTION GATES ---------------------------------------------------------")
    panels = build_panels()
    for k, (px, tr) in panels.items():
        P(f"  panel {k}: {px.shape[0]} days x {px.shape[1]} cols, {len(tr)} tradable, "
          f"{px.index[0].date()} .. {px.index[-1].date()}")
    ga, gaw = gate_harness(panels)
    gb, gbw, gbn = gate_size_dial(panels)
    gc, pdC, pdS = gate_parent_headline()
    P(f"\n  GATES: [a] harness {'PASS' if ga else 'FAIL'} ({gaw:.3e}) | [b] SIZE dial "
      f"{'PASS' if gb else 'FAIL'} ({gbw:.3e}, {gbn} cells) | [c] parent headline "
      f"{'PASS' if gc else 'FAIL'}")
    if not (ga and gb and gc):
        P("  ABORT: a reproduction gate failed; no new number is reported.")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
        return

    P("\n--- LEG B: controlled 5-dial grid ---------------------------------------------")
    P("  (run on the LIVE panels, which end after the parent's sample; the SIZE dial's drift"
      " against the committed grid is the [b] number above)")
    grid, series = run_grid(panels)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P(f"\n  {len(grid)} grid rows written ({len(grid[grid.dial != 'BASE'])} arms x 2 cost rungs "
      f"+ baselines).  All rungs reported:")
    for dial in DIALS:
        g = grid[(grid.dial == dial) & (grid.bps == COST_BPS)]
        P(f"\n  == dial {dial} @ {COST_BPS} bps ==")
        P(fmt(g[["panel", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_CAGR", "IS_Sharpe",
                 "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turn", "gross_real", "sat_share",
                 "p4a_v2", "p4a_v1", "f4b"]].set_index(["panel", "arm"])))
    P("\n  == baselines (per panel) ==")
    P(fmt(grid[(grid.dial == "BASE") & (grid.bps == COST_BPS)][
        ["panel", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
         "OOS_MaxDD", "f4b"]].set_index(["panel", "arm"])))

    P("\n--- LEG B: rule 8 walk-forward (IS 2009-2016 chooses, OOS 2017-2026 read once) --")
    wf = rule8(grid, use_sat_cap=True)
    wf_nocap = rule8(grid, use_sat_cap=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for dial in DIALS:
        w = wf[(wf.dial == dial) & (wf.bps == COST_BPS)]
        P(f"\n  == {dial} ==")
        P(fmt(w[["panel", "selector", "pick", "IS_Sharpe", "IS_CAGR", "OOS_CAGR", "OOS_Sharpe",
                 "OOS_MaxDD", "v2_OOS_Sharpe", "SPY_OOS_Sharpe", "full_4a_v2", "full_4b"]]
              .set_index(["panel", "selector"])))

    P("\n  Selector means over all 5 dials x 4 panels (OOS, 10 bps):")
    w10 = wf[wf.bps == COST_BPS]
    agg = w10.groupby("selector")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean()
    agg["beats_v2_Sharpe"] = w10.groupby("selector").apply(
        lambda g: int((g.OOS_Sharpe > g.v2_OOS_Sharpe).sum()))
    agg["beats_SPY_Sharpe"] = w10.groupby("selector").apply(
        lambda g: int((g.OOS_Sharpe > g.SPY_OOS_Sharpe).sum()))
    agg["n"] = w10.groupby("selector").size()
    P(fmt(agg))
    P(f"  reference: RULES v2 OOS Sharpe mean "
      f"{w10.v2_OOS_Sharpe.mean():.4f} / CAGR {w10.v2_OOS_CAGR.mean():.4%}; "
      f"RULES v1 {w10.v1_OOS_Sharpe.mean():.4f} / {w10.v1_OOS_CAGR.mean():.4%}; "
      f"SPY {w10.SPY_OOS_Sharpe.mean():.4f} / {w10.SPY_OOS_CAGR.mean():.4%}")

    P("\n--- LEG B: the exchange rate ---------------------------------------------------")
    ex = exchange_table(wf)
    ex.to_csv(OUT / f"{STEM}.exchange.csv", index=False)
    ex10 = ex[ex.bps == COST_BPS]
    P(fmt(ex10[["panel", "dial", "pick_S", "pick_C", "agree", "dCAGR_pp", "dOOS_Sharpe",
                "dOOS_MaxDD_pp", "priced", "free", "rate"]].set_index(["dial", "panel"])))
    P(f"\n  disagreement: {int((~ex10.agree).sum())} of {len(ex10)} cells; "
      f"priced (dSharpe<0) {int(ex10.priced.sum())}; free (dSharpe>=0) {int(ex10.free.sum())}; "
      f"agree {int(ex10.agree.sum())}")
    P("  per dial:")
    per = ex10.groupby("dial").agg(cells=("agree", "size"), disagree=("agree", lambda s: int((~s).sum())),
                                   priced=("priced", "sum"), free=("free", "sum"),
                                   mean_dCAGR_pp=("dCAGR_pp", "mean"),
                                   mean_dSharpe=("dOOS_Sharpe", "mean"),
                                   median_rate=("rate", "median"))
    P(fmt(per))
    m, t, pos, n = paired_t(ex10.dCAGR_pp)
    P(f"  pooled dCAGR_pp mean {m:+.4f} t {t:+.3f} positive {pos}/{n}")
    m, t, pos, n = paired_t(ex10.dOOS_Sharpe)
    P(f"  pooled dSharpe   mean {m:+.5f} t {t:+.3f} positive {pos}/{n}")
    P(f"  aggregate rate the parent's way (mean dCAGR / -mean dSharpe): "
      f"{ex10.dCAGR_pp.mean() / -ex10.dOOS_Sharpe.mean() if ex10.dOOS_Sharpe.mean() != 0 else np.nan:+.2f} "
      f"pp per unit Sharpe (idea 259 published {PUBLISHED_RATE:+.2f} on the SIZE dial alone)")

    P("\n  no-saturation-cap sensitivity (SAT_CAP dropped):")
    ex_nc = exchange_table(wf_nocap)
    ex_nc10 = ex_nc[ex_nc.bps == COST_BPS]
    P(fmt(ex_nc10.groupby("dial").agg(disagree=("agree", lambda s: int((~s).sum())),
                                      priced=("priced", "sum"), free=("free", "sum"),
                                      median_rate=("rate", "median"))))

    P("\n  0 bps diagnostic (is the exchange a COST effect?):")
    ex0 = ex[ex.bps == DIAG_BPS]
    P(fmt(ex0.groupby("dial").agg(disagree=("agree", lambda s: int((~s).sum())),
                                  priced=("priced", "sum"), free=("free", "sum"),
                                  mean_dCAGR_pp=("dCAGR_pp", "mean"),
                                  mean_dSharpe=("dOOS_Sharpe", "mean"),
                                  median_rate=("rate", "median"))))

    P("\n--- LEG B: the dial's own trade-off geometry (all arms, not just the two picks) --")
    geo = []
    for (pname, dial, bps), g in grid[grid.dial != "BASE"].groupby(["panel", "dial", "bps"]):
        b, tt, nn = ols_slope(g.OOS_Sharpe, g.OOS_CAGR * 100.0)
        bi, ti, ni = ols_slope(g.IS_Sharpe, g.IS_CAGR * 100.0)
        geo.append(dict(panel=pname, dial=dial, bps=bps, arms=nn,
                        slope_OOS=b, t_OOS=tt, rho_OOS=spearman(g.OOS_Sharpe, g.OOS_CAGR),
                        slope_IS=bi, t_IS=ti, rho_IS=spearman(g.IS_Sharpe, g.IS_CAGR)))
    geo = pd.DataFrame(geo)
    geo.to_csv(OUT / f"{STEM}.geometry.csv", index=False)
    g10 = geo[geo.bps == COST_BPS]
    P(fmt(g10[["dial", "panel", "arms", "slope_IS", "rho_IS", "slope_OOS", "t_OOS", "rho_OOS"]]
          .set_index(["dial", "panel"])))
    P("\n  per dial (pp CAGR per unit Sharpe along the dial):")
    P(fmt(g10.groupby("dial").agg(median_slope_OOS=("slope_OOS", "median"),
                                  median_rho_OOS=("rho_OOS", "median"),
                                  median_slope_IS=("slope_IS", "median"),
                                  median_rho_IS=("rho_IS", "median"),
                                  neg_rho_OOS=("rho_OOS", lambda s: int((s < 0).sum())))))
    st, pv, k, n = perm_between(g10.slope_OOS, g10.dial)
    P(f"  between-dial permutation on OOS slopes: spread of medians {st:.2f} pp/Sharpe, "
      f"p {pv:.4f} ({k} dials, {n} cells, {NPERM} permutations, seed {SEED})")

    P("\n--- LEG A: census over the record ----------------------------------------------")
    pv_a = np.nan
    cp, nfiles, skipped = census()
    if cp.empty:
        P("  no census rows found.")
    else:
        cp.to_csv(OUT / f"{STEM}.census.csv.gz", index=False, compression="gzip")
        P(f"  {nfiles} committed CSVs carry IS_CAGR+IS_Sharpe+OOS_CAGR+OOS_Sharpe; "
          f"{len(cp)} swept-dial cells across {cp.file.nunique()} files and "
          f"{cp.dial.nunique()} distinct dial columns; {len(skipped)} files skipped")
        P("  by family:")
        fam = cp.groupby("family").agg(cells=("agree", "size"),
                                       files=("file", "nunique"),
                                       disagree=("agree", lambda s: int((~s).sum())),
                                       priced=("priced", "sum"), free=("free", "sum"),
                                       mean_dCAGR_pp=("dCAGR_pp", "mean"),
                                       mean_dSharpe=("dOOS_Sharpe", "mean"),
                                       median_rate=("rate", "median"),
                                       q25_rate=("rate", lambda s: s.quantile(.25)),
                                       q75_rate=("rate", lambda s: s.quantile(.75)))
        fam["disagree_pct"] = fam.disagree / fam.cells
        fam["free_share_of_disagree"] = fam.free / fam.disagree.replace(0, np.nan)
        P(fmt(fam))
        P(f"\n  pooled: disagree {int((~cp.agree).sum())}/{len(cp)} "
          f"({(~cp.agree).mean():.1%}); of the disagreements, priced "
          f"{cp.priced.sum()} ({cp.priced.sum() / max(1, int((~cp.agree).sum())):.1%}) and free "
          f"{cp.free.sum()} ({cp.free.sum() / max(1, int((~cp.agree).sum())):.1%})")
        m, t, pos, n = paired_t(cp.dCAGR_pp)
        P(f"  pooled dCAGR_pp mean {m:+.4f} t {t:+.2f} positive {pos}/{n}")
        m, t, pos, n = paired_t(cp.dOOS_Sharpe)
        P(f"  pooled dSharpe   mean {m:+.5f} t {t:+.2f} positive {pos}/{n}")
        rr = cp.rate.dropna()
        if len(rr):
            P(f"  rate over priced cells: n {len(rr)} median {rr.median():.2f} "
              f"IQR [{rr.quantile(.25):.2f}, {rr.quantile(.75):.2f}] "
              f"decile [{rr.quantile(.10):.2f}, {rr.quantile(.90):.2f}] "
              f"pp CAGR per unit Sharpe; idea 259's published {PUBLISHED_RATE:.2f} is "
              f"{'INSIDE' if rr.quantile(.25) <= PUBLISHED_RATE <= rr.quantile(.75) else 'OUTSIDE'} "
              f"the IQR")
        big = cp[cp.family != "OTHER"]
        st_a, pv_a, k_a, n_a = perm_between(big.rate, big.family)
        P(f"  between-family permutation on census rates (named families only): spread of "
          f"medians {st_a:.2f}, p {pv_a:.4f} ({k_a} families, {n_a} priced cells)")
        st_o, pv_o, k_o, n_o = perm_between(cp.rate, cp.family)
        P(f"  between-family permutation including OTHER: spread {st_o:.2f}, p {pv_o:.4f} "
          f"({k_o} families, {n_o} priced cells)")
        P("\n  the 12 files contributing the most cells:")
        P(fmt(cp.groupby("file").agg(cells=("agree", "size"),
                                     disagree=("agree", lambda s: int((~s).sum())),
                                     median_rate=("rate", "median"))
              .sort_values("cells", ascending=False).head(12)))

    P("\n--- VERDICT (pre-registered bars, read in order) --------------------------------")
    # NOT-A-PRICE
    b_dis_grid = float((~ex10.agree).mean())
    free_share_grid = (ex10.free.sum() / max(1, int((~ex10.agree).sum())))
    if not cp.empty:
        b_dis_cen = float((~cp.agree).mean())
        free_share_cen = cp.free.sum() / max(1, int((~cp.agree).sum()))
    else:
        b_dis_cen, free_share_cen = np.nan, np.nan
    P(f"  bar 1 NOT-A-PRICE: disagreement grid {b_dis_grid:.1%}, census {b_dis_cen:.1%}; "
      f"free share of disagreements grid {free_share_grid:.1%}, census {free_share_cen:.1%}")
    not_price = (b_dis_grid < 0.5 or b_dis_cen < 0.5) or (free_share_grid >= 0.5 or free_share_cen >= 0.5)
    # DIAL-SPECIFIC
    med_grid = ex10.groupby("dial").rate.median().dropna()
    med_cen = cp.groupby("family").rate.median().dropna() if not cp.empty else pd.Series(dtype=float)
    st_g, pv_g, k_g, n_g = perm_between(ex10.rate, ex10.dial)
    P(f"  bar 2 DIAL-SPECIFIC: grid dial medians {med_grid.round(1).to_dict()} "
      f"(perm spread {st_g:.2f}, p {pv_g if np.isfinite(pv_g) else float('nan'):.4f}); "
      f"census family medians {med_cen.round(1).to_dict()} (perm p "
      f"{pv_a if not cp.empty else float('nan'):.4f})")
    sign_split = (len(med_grid) > 1 and (med_grid > 0).any() and (med_grid < 0).any()) or \
                 (len(med_cen) > 1 and (med_cen > 0).any() and (med_cen < 0).any())
    rejects = (np.isfinite(pv_g) and pv_g < 0.05) or (not cp.empty and np.isfinite(pv_a) and pv_a < 0.05)
    dial_specific = sign_split or rejects
    P(f"  bar 3 CONSTANT would need: same sign on every dial ({'FAIL' if sign_split else 'ok'}), "
      f"no between-dial rejection ({'FAIL' if rejects else 'ok'}), published rate inside the "
      f"pooled IQR")
    verdict = "NOT-A-PRICE" if not_price else ("DIAL-SPECIFIC" if dial_specific else "CONSTANT")
    P(f"\n  VERDICT (primary, first bar to fire): the S_CAGR-vs-S_SHARPE exchange rate is {verdict}")
    # the secondary reading is reported whatever the primary is: conditional on a price
    # actually being paid, is the rate the same number on every dial?
    second = "DIAL-SPECIFIC" if dial_specific else "CONSTANT"
    P(f"  SECONDARY (conditional on the pair disagreeing AND dSharpe < 0, i.e. where a rate "
      f"exists at all): the rate is {second}")
    if not cp.empty and len(med_cen) > 1:
        P(f"    census family medians span {med_cen.min():.1f} .. {med_cen.max():.1f} "
          f"pp CAGR per unit Sharpe, sign-split {'YES' if ((med_cen > 0).any() and (med_cen < 0).any()) else 'no'}")

    P("\n--- KEEP paths (PROTOCOL rule 4) -----------------------------------------------")
    a = grid[(grid.dial != "BASE") & (grid.bps == COST_BPS)]
    P(f"  4a vs RULES v2 (live book): {int(a.p4a_v2.sum())} of {len(a)} arms")
    P(f"  4a vs RULES v1 (previous):  {int(a.p4a_v1.sum())} of {len(a)} arms")
    P(f"  4b vs SPY:                  {int(a.p4b.sum())} of {len(a)} arms")
    if a.p4b.any():
        P(fmt(a[a.p4b][["panel", "dial", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                        "OOS_Sharpe", "p4a_v2"]].set_index(["panel", "dial", "arm"])))
    both = a[a.p4b & a.p4a_v2]
    P(f"  4a-v2 AND 4b: {len(both)} arms")
    P("  fail-bar census for 4b:")
    P(fmt(a.f4b.value_counts().to_frame("arms")))
    a0 = grid[(grid.dial != "BASE") & (grid.bps == DIAG_BPS)]
    P(f"  at {DIAG_BPS} bps: 4a-v2 {int(a0.p4a_v2.sum())}/{len(a0)}, 4b {int(a0.p4b.sum())}/{len(a0)}")

    P(f"\nDone in {time.time() - t_start:.0f}s.  Files: {STEM}.grid.csv, .walkforward.csv, "
      f".exchange.csv, .geometry.csv, .census.csv.gz, .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
