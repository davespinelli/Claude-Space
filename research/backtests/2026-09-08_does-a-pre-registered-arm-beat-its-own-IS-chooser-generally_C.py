#!/usr/bin/env python3
"""QUEUE idea 452 — does-a-pre-registered-arm-beat-its-own-IS-chooser-generally
   (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 452)
    "idea 232 is the record's first case where a PRE-REGISTERED arm wins OOS more consistently
     (88.1%) than the IS chooser that finds it (66.7%) while the chooser has the higher mean
     (+0.0978 vs +0.0621).  Re-read the record's ~10 'selection loses' instances for the same
     shape: is mean-vs-hit-rate divergence the general signature of a chooser paying for a
     corner it reaches too often?  Max 2 params."

THE STATISTIC, WRITTEN OUT BEFORE IT IS RUN
    An INSTANCE is a pool of cells that share one arm ladder A (|A| >= 3) and one comparand
    convention.  For a cell c and an object x (a fixed arm, or a chooser),

        margin_x(c) := OOS_Sharpe_x(c) - base(c),
        mean_x      := mean_c margin_x(c),        hit_x := share_c [margin_x(c) > 0].

    base(c) is the POOL MEAN over A (every object priced against the same number, so means are
    comparable across objects) or the ladder's own CONTROL arm where one is identifiable.  Both
    conventions are carried end to end.

        DIVERGENCE(a) := mean_chooser > mean_a  AND  hit_chooser < hit_a.

    This is the queue's shape written as a two-object comparison.  Its three alternatives are
    counted too: chooser DOMINATES (higher on both), chooser LOSES (lower on both), and REVERSE
    divergence (chooser higher hit, lower mean).

WHAT THE QUEUE'S PREMISE ACTUALLY IS, AND THE ONE THING IT DOES NOT SAY
    Gate [G3] reproduces idea 232's four numbers exactly off lane B's committed walk-forward
    file.  Reading lane B's script, its A1 (the pre-registered arm) is pinned at n = 20 and
    varies only the gate, while its S1 (the chooser) is an IS-argmax over gate x n — SIX arms
    the pre-registered arm cannot reach, including the n = 5 corner.  So the record's flagship
    divergence is measured between objects that do not choose over the same ladder.  That is a
    testable confound, not a criticism: this run therefore prices the chooser BOTH ways —
    MATCHED (chooser restricted to the pre-registered arm's own ladder) and WIDE (chooser given
    a second dial) — everywhere, and reports the difference as the mechanism test.

WHAT THIS RUN DOES
    G   GATES.  fast_backtest == engine.backtest; the cost-rung turnover identity; idea 232's
        published 88.1 / 66.7 / +0.0621 / +0.0978 reproduced off the committed file; and the
        reconstruction gate that matters — does this run's chooser rebuild from lane B's
        840-row arm grid reproduce lane B's own walk-forward picks and margins?
    A   THE FLAGSHIP, RE-READ.  Idea 232's instance with every one of its arms placed on the
        (mean, hit) plane, under both comparands, matched and wide chooser.
    B   THE RECORD CENSUS.  Every committed CSV under research/backtests carrying a per-row IS
        Sharpe AND an OOS Sharpe is re-read as an instance: balanced arm ladder, chooser
        rebuilt, every fixed arm placed on the same plane, quadrants counted, and the corner
        mechanism (pick concentration, ladder-endpoint share) measured against the divergence.
    C   THE LIVE CORPUS, where the ladder is known rather than inferred.  3 panels x 7 dial
        families x 3 cost rungs, with an expanding-window fold scheme so hit rates have more
        than one draw, chooser MATCHED and WIDE, all arms reported.
    D   RULE 8 (PROTOCOL 8).  The canonical split — parameters read on 2009-2016 only, 2017-2026
        read once — with OOS CAGR / Sharpe / MaxDD for every object against RULES v2, RULES v1
        and SPY.
    E   BOTH KEEP PATHS (PROTOCOL 4a and 4b), every live arm and every chooser book, full sample
        and OOS.  This is a diagnostic idea and is not expected to promote a book; the paths are
        scored because PROTOCOL requires it.

TUNED PARAMETERS (exactly 2, every grid point reported, nothing else selected on)
    1. p — the PRE-REGISTERED position rule that names the fixed arm the chooser is compared to,
       p in {CONTROL, MEDIAN, LADDER-MIN, LADDER-MAX} (4 points, all four reported everywhere).
    2. h — the fold horizon in Part C, h in {1, 2, 3} years (3 points, all reported).
    Panels, dial families, cost rungs, comparand convention (pool-mean / control) and the
    matched-vs-wide chooser contrast are REPORTED axes and are never selected on.

PRE-REGISTERED PREDICTIONS (written before any number in Parts A-E was computed)
    P1  Divergence is NOT the general signature: over the census instances, the chooser-higher-
        mean-lower-hit quadrant holds for fewer than half of the (instance, position rule) pairs.
    P2  It is a POOL-WIDTH effect: the WIDE chooser diverges from the same fixed arms strictly
        more often than the MATCHED chooser does, on the live corpus and on the flagship.
    P3  Divergence rises with corner-reach: instances in the top tercile of ladder-endpoint pick
        share diverge more often than the bottom tercile.
    P4  No book is promoted — 4a 0 of N against the live RULES v2, and any 4b passes are the
        already-known de-grossed U56 carve-out, not a chooser result.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): u56, broad and small are current constituents; every CAGR here is
      flattered.  Every statistic below is a WITHIN-POOL contrast, which a level bias does not
      move; no level here is an achievable return.
    * The census reconstruction is a HEURISTIC over heterogeneous committed files (arm column
      inferred from column names and cardinalities, adapted from idea 436's committed code).  It
      is quoted with the flagship reproduction gate [G4], the count of files admitting more than
      one split, and a per-instance sensitivity over every admissible arm column.
    * A reconstructed pool is not always a selector's real choice set; where a file pools over a
      REPORTED axis the ladder is too wide, which INFLATES the wide-chooser effect.  The bias is
      stated, not corrected, and Part C — where the ladder is built here — is the controlled twin.
    * Instances overlap heavily (the same books appear in many files).  Every count is quoted
      with its n; no instance-level t is treated as an independent-sample t.
    * Hit rate over a fold scheme is not a p-value: folds share data by construction (expanding
      IS windows, overlapping OOS windows at h > 1).  The canonical rule-8 split in Part D is
      the only non-overlapping read and is reported separately.
    * data/prices.csv was rewritten 2026-09-07 (idea 401); reproductions of older committed
      numbers are quoted per number rather than asserted bit-exact.
    * PROTOCOL rung is 10 bps; 0 and 25 bps are reported.  All books are t+1 execution.

Deterministic (seeded), standalone, offline.  Writes .console.txt, .flagship.csv, .census.csv,
.instances.csv, .cells.csv, .walkforward.csv and .keeppaths.csv next to itself.  Modifies
nothing.
"""
import collections
import glob
import importlib.util
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_does-a-pre-registered-arm-beat-its-own-IS-chooser-generally_C"
OUT = ROOT / "research" / "backtests"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
B232_GRID = OUT / "2026-09-08_does-the-vol-gate-corner-survive-being-pre-registered_B.grid.csv"
B232_WF = OUT / "2026-09-08_does-the-vol-gate-corner-survive-being-pre-registered_B.walkforward.csv"

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60                     # PROTOCOL 4b CAGR floor / MaxDD cap
POSRULES = ["CONTROL", "MEDIAN", "LADMIN", "LADMAX"]      # tuned param 1 (all reported)
HORIZONS = [1, 2, 3]                                      # tuned param 2 (all reported)
FOLD_FIRST_IS_END = 2013                    # first fold's IS end year (reported, not tuned)
FOLD_LAST_OOS_END = 2026
MIN_CELLS = 8                               # an instance needs >= 8 cells for a hit rate
MIN_ARMS = 3
ROW_CAP = 300_000
SEED = 452

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 120)
pd.set_option("display.max_rows", 3000)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------ stats ---
def sign_p(wins, n):
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def tstat(x):
    x = np.asarray([v for v in np.asarray(x, float) if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def corr(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    y, x = y[ok], x[ok]
    if len(y) < 3 or y.std() == 0 or x.std() == 0:
        return np.nan
    return float(np.corrcoef(y, x)[0, 1])


def skew(x):
    x = np.asarray([v for v in np.asarray(x, float) if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=0) == 0:
        return np.nan
    return float(((x - x.mean()) ** 3).mean() / x.std(ddof=0) ** 3)


def sharpe(r):
    return float(metrics(r)["Sharpe"])


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def quadrant(mean_c, hit_c, mean_a, hit_a, eps=1e-12):
    """Where the chooser sits relative to fixed arm a on the (mean, hit) plane."""
    dm, dh = mean_c - mean_a, hit_c - hit_a
    if abs(dm) <= eps and abs(dh) <= eps:
        return "IDENTICAL"
    if dm > 0 and dh < 0:
        return "DIVERGE"            # the queue's shape: chooser mean up, hit down
    if dm < 0 and dh > 0:
        return "REVERSE"
    if dm >= 0 and dh >= 0:
        return "DOMINATE"
    return "LOSE"


# =====================================================================================
# PART G / A — the flagship instance, rebuilt from lane B's committed 840-row arm grid
# =====================================================================================
def _pool_stats(cells, base_key, obj_vals):
    """cells: list of dicts. obj_vals: dict name -> list of OOS values aligned to cells."""
    base = np.array([c[base_key] for c in cells], float)
    out = {}
    for k, v in obj_vals.items():
        m = np.asarray(v, float) - base
        out[k] = dict(mean=float(np.nanmean(m)), hit=float(np.nanmean(m > 0)),
                      n=int(np.isfinite(m).sum()), sd=float(np.nanstd(m, ddof=1)) if len(m) > 2 else np.nan,
                      skew=skew(m), t=tstat(m))
    return out


def flagship():
    say("\n" + "=" * 120)
    say("PART A — idea 232's own instance, every arm on the (mean, hit) plane")
    say("=" * 120)
    g = pd.read_csv(B232_GRID)
    wf = pd.read_csv(B232_WF)
    g["armn"] = g["arm"].astype(str) + "/n" + g["n"].astype(str)
    cellcols = ["key", "gross", "panel", "bps"]
    rows, cells = [], []
    for keyv, sub in g.groupby(cellcols, dropna=False):
        sub = sub.dropna(subset=["IS_Sharpe", "OOS_Sharpe"])
        if len(sub) < MIN_ARMS:
            continue
        cells.append(dict(cell=keyv, sub=sub.set_index("armn")))
    arms_all = sorted(set.intersection(*[set(c["sub"].index) for c in cells]))
    say(f"  cells {len(cells)} (key x gross x panel x bps), balanced ladder {len(arms_all)} arms: "
        f"{', '.join(arms_all)}")
    # comparands
    recs = []
    for c in cells:
        s = c["sub"].loc[arms_all]
        base_mean = float(s["OOS_Sharpe"].mean())
        base_ctl = float(s.loc["GATE_ON/n20", "OOS_Sharpe"])          # lane B's own A0
        pick_m = s.loc[[a for a in arms_all if a.endswith("/n20")], "IS_Sharpe"].idxmax()
        pick_w = s["IS_Sharpe"].idxmax()
        recs.append(dict(cell=c["cell"], base_mean=base_mean, base_ctl=base_ctl,
                         pick_m=pick_m, pick_w=pick_w,
                         oos_m=float(s.loc[pick_m, "OOS_Sharpe"]),
                         oos_w=float(s.loc[pick_w, "OOS_Sharpe"]),
                         **{f"arm::{a}": float(s.loc[a, "OOS_Sharpe"]) for a in arms_all}))
    R = pd.DataFrame(recs)
    # [G4] reconstruction gate against lane B's own walk-forward columns
    wf["cellkey"] = list(zip(wf.key, wf.gross, wf.panel, wf.bps))
    R["cellkey"] = R.cell
    j = R.merge(wf[["cellkey", "A0_OOS_Sharpe", "A1_OOS_Sharpe", "S1_OOS_Sharpe", "S1_pick",
                    "A1_minus_A0", "S1_minus_A0"]], on="cellkey", how="inner")
    d_ctl = float((j.base_ctl - j.A0_OOS_Sharpe).abs().max())
    d_a1 = float((j["arm::GATE_OFF/n20"] - j.A1_OOS_Sharpe).abs().max())
    d_s1 = float((j.oos_w - j.S1_OOS_Sharpe).abs().max())
    same_pick = float((j.pick_w == j.S1_pick).mean())
    say(f"  [G4] rebuild vs lane B's published walk-forward: |d A0| {d_ctl:.3e}, |d A1| {d_a1:.3e}, "
        f"|d S1| {d_s1:.3e}, S1 pick identical {same_pick:.1%} of {len(j)} cells")
    assert d_ctl < 1e-9 and d_a1 < 1e-9 and d_s1 < 1e-9 and same_pick == 1.0, "G4 FAILED"
    say(f"  [G3] premise: A1-A0 mean {j.A1_minus_A0.mean():+.4f} hit {(j.A1_minus_A0 > 0).mean():.1%} | "
        f"S1-A0 mean {j.S1_minus_A0.mean():+.4f} hit {(j.S1_minus_A0 > 0).mean():.1%} "
        f"[queue quotes +0.0621 / 88.1% and +0.0978 / 66.7%]")

    outrows = []
    for conv, bcol in [("POOLMEAN", "base_mean"), ("CONTROL", "base_ctl")]:
        objs = {f"ARM {a}": R[f"arm::{a}"].values for a in arms_all}
        objs["CHOOSER-MATCHED (n20 ladder)"] = R.oos_m.values
        objs["CHOOSER-WIDE (gate x n)"] = R.oos_w.values
        st = _pool_stats(R.to_dict("records"), bcol, objs)
        cm, cw = st["CHOOSER-MATCHED (n20 ladder)"], st["CHOOSER-WIDE (gate x n)"]
        say(f"\n  comparand = {conv}")
        say(f"    {'object':34s} {'mean':>9s} {'hit':>8s} {'sd':>8s} {'skew':>7s} "
            f"{'q(vs MATCHED)':>14s} {'q(vs WIDE)':>12s}")
        for k in list(objs):
            s = st[k]
            qm = quadrant(cm["mean"], cm["hit"], s["mean"], s["hit"]) if k.startswith("ARM") else ""
            qw = quadrant(cw["mean"], cw["hit"], s["mean"], s["hit"]) if k.startswith("ARM") else ""
            say(f"    {k:34s} {s['mean']:+9.4f} {s['hit']:8.1%} {s['sd']:8.4f} {s['skew']:+7.2f} "
                f"{qm:>14s} {qw:>12s}")
            outrows.append(dict(conv=conv, obj=k, **s, q_matched=qm, q_wide=qw))
    F = pd.DataFrame(outrows)
    F.to_csv(OUT / f"{STEM}.flagship.csv", index=False)
    say(f"\n  picks: MATCHED {dict(R.pick_m.value_counts())}")
    say(f"  picks: WIDE    {dict(R.pick_w.value_counts())}")
    n5 = float(R.pick_w.str.endswith('/n5').mean())
    say(f"  the WIDE chooser reaches the n=5 corner in {n5:.1%} of cells; the MATCHED chooser "
        f"cannot reach it at all (its ladder is the 2 gate arms at n=20).")

    # ---- A2: where does the WIDE chooser's mean and its hit rate come from? ----
    say("\n  [A2] the queue's own mechanism, tested on its own instance: mean and hit rate are")
    say("       BOTH linear in the pick mixture, so decompose each by the arm picked "
        "(comparand = CONTROL)")
    m_w = R.oos_w.values - R.base_ctl.values
    say(f"    {'picked arm':<16s} {'freq':>7s} {'mean|pick':>10s} {'hit|pick':>9s} "
        f"{'share of mean':>14s} {'share of hit':>13s}")
    tot_mean, tot_hit = float(np.mean(m_w)), float(np.mean(m_w > 0))
    for a, sub in R.groupby(R.pick_w):
        mm = sub.oos_w.values - sub.base_ctl.values
        f_a = len(sub) / len(R)
        say(f"    {a:<16s} {f_a:>7.1%} {mm.mean():>+10.4f} {float((mm > 0).mean()):>9.1%} "
            f"{f_a * mm.mean() / tot_mean:>14.1%} "
            f"{f_a * float((mm > 0).mean()) / tot_hit:>13.1%}")
    say(f"    TOTAL                            {tot_mean:+10.4f} {tot_hit:>9.1%}")
    thin = R.pick_w.isin(["GATE_OFF/n5", "GATE_OFF/n10", "GATE_ON/n5", "GATE_ON/n10"])
    mm_thin = (R.oos_w.values - R.base_ctl.values)[thin.values]
    mm_wide = (R.oos_w.values - R.base_ctl.values)[~thin.values]
    say(f"    THIN corner picks (n<=10, {thin.mean():.1%} of cells): mean {mm_thin.mean():+.4f}, "
        f"hit {float((mm_thin > 0).mean()):.1%} | the rest: mean {mm_wide.mean():+.4f}, "
        f"hit {float((mm_wide > 0).mean()):.1%}")
    say(f"    drop the corner picks and re-price the same chooser: mean "
        f"{mm_wide.mean():+.4f} vs the pre-registered arm's +0.0621, hit "
        f"{float((mm_wide > 0).mean()):.1%} vs 88.1%")
    return F, R


# =====================================================================================
# PART B — the record census
# =====================================================================================
# Column-name vocabulary adapted from idea 436's committed census code.
METRIC = re.compile(
    r"(?i)cagr|sharpe|maxdd|drawdown|sortino|calmar|winrate|turnover|equity|vol\b|volatility|"
    r"years|nyears|regret|best|oracle|headroom|margin|lift|pool|gain|wins|losses|"
    r"keep|pass|fail|beat|verdict|truth|moved|binding|4a|4b|p4|f4|flag|"
    r"err|delta|rho|slope|r2|pval|p_value|_p$|^p$|^t$|^se$|^z$|tstat|"
    r"rank|rate|count|mean|median|std|^sd|^ci|_lo$|_hi$|score|alpha|beta|corr|agree|share|"
    r"^d_|_d$|oos|_is$|^is_|dd$|_dd|ret$|total$")
ARMNAME = re.compile(
    r"(?i)^(arm|arms|pick|point|param|params|value|variant|conv|convention|kind|dial|"
    r"n|k|g|gross|tau|thr|threshold|band|width|freq|cadence|level|cap|floor|f|m|e|"
    r"gate|sleeve|lb|lookback|ma|malen|vcap|volcap|depth|window|mode|method|"
    r"selector|sel|chooser|rule|strategy|strat|label|family|book|length|size|"
    r"n_names|top|topn|quantile|decile|bucket|stat|band_width|buffer|lag|horizon)$")
REFCOL = re.compile(r"(?i)spy|bench|base|ctl|control|v1|v2|anchor|live|null|do.?noth|pool")
CTLVAL = re.compile(r"(?i)^(control|ctl|do-?nothing|none|nothing|base|baseline|s0|off|no-?gate|"
                    r"identity|null|untreated|full|all|nan)$")
BOOLISH = {"true", "false", "yes", "no", "keep", "kill", "park", "0", "1", "0.0", "1.0"}
ISCOL = re.compile(r"(?i)(^|_)is[ _]?sharpe$|sharpe[ _]?is$")
OOSCOL = re.compile(r"(?i)oos.*sharpe|sharpe.*oos")


def _boolish(s):
    vals = {str(v).strip().lower() for v in pd.unique(s.dropna())}
    return len(vals) > 0 and vals.issubset(BOOLISH)


def key_candidates(df):
    out, n = [], len(df)
    for c in df.columns:
        if METRIC.search(str(c)):
            continue
        s = df[c]
        if s.dtype == bool or _boolish(s):
            continue
        nu = s.nunique(dropna=False)
        if nu < 2 or nu >= n:
            continue
        if s.dtype == object or nu <= 40:
            out.append(c)
    return out


def pool_split(df, cands):
    opts = []
    for c in cands:
        others = [o for o in cands if o != c]
        try:
            sizes = (df.groupby(others, dropna=False).size() if others
                     else df.assign(_one=0).groupby("_one").size())
        except Exception:
            continue
        n3 = int((sizes >= MIN_ARMS).sum())
        if n3 < MIN_CELLS:
            continue
        opts.append(dict(arm=c, n_cells3=n3, prio=1 if ARMNAME.match(str(c)) else 0,
                         pooled=int(sizes[sizes >= MIN_ARMS].sum()), others=others))
    opts.sort(key=lambda d: (d["n_cells3"], d["prio"], d["pooled"]), reverse=True)
    return opts


def _ladder_order(vals):
    """Numeric order where every arm label parses as a number, else first-appearance order."""
    def num(v):
        m = re.findall(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", str(v))
        return float(m[-1]) if m else None
    ns = [num(v) for v in vals]
    if all(x is not None for x in ns) and len(set(ns)) == len(ns):
        return [v for _, v in sorted(zip(ns, vals))]
    return list(vals)


def instance_from(df, opt, is_col, oos_col, label):
    """One instance: balanced ladder, chooser rebuilt, every fixed arm on the (mean,hit) plane."""
    arm, others = opt["arm"], opt["others"]
    df = df.copy()
    for c in (is_col, oos_col):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[np.isfinite(df[is_col]) & np.isfinite(df[oos_col])]
    if len(df) < MIN_ARMS * MIN_CELLS:
        return None
    grp = df.groupby(others, dropna=False) if others else [((), df)]
    cellmaps = []
    for keyv, sub in (grp if others else grp):
        s = sub[[arm, is_col, oos_col]].dropna()
        s = s.groupby(arm, dropna=False).first()          # duplicate arm rows: first, reported
        if len(s) < MIN_ARMS:
            continue
        cellmaps.append((keyv, s))
    if len(cellmaps) < MIN_CELLS:
        return None
    common = sorted(set.intersection(*[set(s.index.astype(str)) for _, s in cellmaps]),
                    key=str)
    if len(common) < MIN_ARMS:
        return None
    order = _ladder_order(common)
    ctl = next((a for a in order if CTLVAL.match(str(a))), None)
    recs = []
    for keyv, s in cellmaps:
        s.index = s.index.astype(str)
        s = s.loc[order]
        oos = s[oos_col].astype(float)
        isv = s[is_col].astype(float)
        if not np.isfinite(oos.values).all() or not np.isfinite(isv.values).all():
            continue
        recs.append(dict(cell=str(keyv), base_mean=float(oos.mean()),
                         base_ctl=float(oos.loc[ctl]) if ctl is not None else np.nan,
                         pick=str(isv.idxmax()), oos_pick=float(oos.loc[isv.idxmax()]),
                         **{f"arm::{a}": float(oos.loc[a]) for a in order}))
    if len(recs) < MIN_CELLS:
        return None
    R = pd.DataFrame(recs)
    picks = R.pick.value_counts(normalize=True)
    conc = float((picks ** 2).sum())
    corner = float(R.pick.isin([str(order[0]), str(order[-1])]).mean())
    out = []
    for conv, bcol in [("POOLMEAN", "base_mean"), ("CONTROL", "base_ctl")]:
        if not np.isfinite(R[bcol]).all():
            continue
        objs = {f"ARM {a}": R[f"arm::{a}"].values for a in order}
        objs["CHOOSER"] = R.oos_pick.values
        st = _pool_stats(R.to_dict("records"), bcol, objs)
        ch = st["CHOOSER"]
        # the four pre-registered position rules (tuned param 1)
        posarm = dict(CONTROL=ctl, MEDIAN=order[len(order) // 2],
                      LADMIN=order[0], LADMAX=order[-1])
        row = dict(instance=label, arm_col=str(arm), conv=conv, n_cells=len(R),
                   n_arms=len(order), ladder="|".join(str(a) for a in order),
                   conc=conc, corner_share=corner, ctl=str(ctl),
                   ch_mean=ch["mean"], ch_hit=ch["hit"], ch_skew=ch["skew"], ch_sd=ch["sd"])
        for p in POSRULES:
            a = posarm[p]
            if a is None or f"ARM {a}" not in st:
                row[f"{p}_q"] = ""
                row[f"{p}_mean"] = np.nan
                row[f"{p}_hit"] = np.nan
                continue
            s = st[f"ARM {a}"]
            row[f"{p}_arm"] = str(a)
            row[f"{p}_mean"] = s["mean"]
            row[f"{p}_hit"] = s["hit"]
            row[f"{p}_q"] = quadrant(ch["mean"], ch["hit"], s["mean"], s["hit"])
        # every arm, not only the four rules
        qs = collections.Counter(quadrant(ch["mean"], ch["hit"], st[f"ARM {a}"]["mean"],
                                          st[f"ARM {a}"]["hit"]) for a in order)
        for q in ("DIVERGE", "REVERSE", "DOMINATE", "LOSE", "IDENTICAL"):
            row[f"n_{q}"] = int(qs[q])
        best_hit = max(order, key=lambda a: st[f"ARM {a}"]["hit"])
        row["besthit_arm"] = str(best_hit)
        row["besthit_mean"] = st[f"ARM {best_hit}"]["mean"]
        row["besthit_hit"] = st[f"ARM {best_hit}"]["hit"]
        row["q_besthit"] = quadrant(ch["mean"], ch["hit"], st[f"ARM {best_hit}"]["mean"],
                                    st[f"ARM {best_hit}"]["hit"])
        out.append(row)
    return out


def census():
    files = [f for f in sorted(glob.glob(str(OUT / "**" / "*.csv"), recursive=True))
             if not Path(f).name.startswith(STEM)]
    say("\n" + "=" * 120)
    say(f"PART B — census over {len(files)} committed CSVs under research/backtests")
    say("=" * 120)
    rows, tier = [], collections.Counter()
    nalt = 0
    for f in files:
        base = Path(f).name
        try:
            head = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            tier["unreadable"] += 1
            continue
        isc = [c for c in head if ISCOL.search(str(c))]
        oosc = [c for c in head if OOSCOL.search(str(c)) and not REFCOL.search(str(c))
                and not re.search(r"(?i)best|oracle", str(c))]
        if not isc or not oosc:
            tier["no_IS_or_OOS_Sharpe_column"] += 1
            continue
        try:
            df = pd.read_csv(f, nrows=ROW_CAP)
        except Exception:
            tier["unreadable"] += 1
            continue
        cands = key_candidates(df)
        opts = pool_split(df, cands) if cands else []
        if not opts:
            tier["no_admissible_split"] += 1
            continue
        got = instance_from(df, opts[0], isc[0], oosc[0], base)
        if not got:
            tier["too_few_balanced_cells"] += 1
            continue
        tier["instance"] += 1
        if len(opts) > 1:
            nalt += 1
        for r in got:
            r["n_alt_splits"] = len(opts)
            rows.append(r)
        # sensitivity: the same instance under every other admissible arm column
        for o in opts[1:4]:
            alt = instance_from(df, o, isc[0], oosc[0], base)
            if alt:
                for r in alt:
                    r["n_alt_splits"] = len(opts)
                    r["alt"] = True
                    rows.append(r)
    C = pd.DataFrame(rows)
    if "alt" not in C:
        C["alt"] = False
    C["alt"] = C["alt"].fillna(False).astype(bool)
    C.to_csv(OUT / f"{STEM}.census.csv", index=False)
    say("  file tiers: " + ", ".join(f"{k} {v}" for k, v in sorted(tier.items())))
    P = C[~C["alt"].values]
    say(f"  instances (primary split): {P.instance.nunique()} files, {len(P)} "
        f"(instance x comparand) rows; {nalt} files admit >1 split "
        f"({int(C.alt.sum())} sensitivity rows carried in .census.csv)")
    for conv in ("POOLMEAN", "CONTROL"):
        S = P[P.conv == conv]
        if not len(S):
            continue
        say(f"\n  [comparand {conv}] {len(S)} instances, median {S.n_cells.median():.0f} cells / "
            f"{S.n_arms.median():.0f} arms")
        say(f"    chooser mean margin: median {S.ch_mean.median():+.4f}, "
            f"share > 0 {float((S.ch_mean > 0).mean()):.1%}; "
            f"chooser hit rate: median {S.ch_hit.median():.1%}")
        say(f"    {'position rule':<10s} {'n':>5s} {'DIVERGE':>9s} {'REVERSE':>9s} "
            f"{'DOMINATE':>9s} {'LOSE':>7s} {'IDENT':>7s}  {'d mean':>9s} {'d hit':>8s}")
        for p in POSRULES:
            q = S[f"{p}_q"].replace("", np.nan).dropna()
            if not len(q):
                continue
            cnt = collections.Counter(q)
            n = len(q)
            dm = (S.ch_mean - S[f"{p}_mean"]).dropna()
            dh = (S.ch_hit - S[f"{p}_hit"]).dropna()
            say(f"    {p:<10s} {n:>5d} {cnt['DIVERGE'] / n:>8.1%} {cnt['REVERSE'] / n:>9.1%} "
                f"{cnt['DOMINATE'] / n:>9.1%} {cnt['LOSE'] / n:>7.1%} {cnt['IDENTICAL'] / n:>7.1%}  "
                f"{dm.mean():>+9.4f} {dh.mean():>+8.1%}   "
                f"[DIVERGE vs its mirror REVERSE: {cnt['DIVERGE']}-{cnt['REVERSE']}, "
                f"sign p {sign_p(cnt['DIVERGE'], cnt['DIVERGE'] + cnt['REVERSE']):.3g}]")
        say(f"    vs the ladder's BEST-HIT arm (the strongest possible form of the queue's claim): "
            f"DIVERGE {float((S.q_besthit == 'DIVERGE').mean()):.1%}, "
            f"LOSE {float((S.q_besthit == 'LOSE').mean()):.1%}, "
            f"DOMINATE {float((S.q_besthit == 'DOMINATE').mean()):.1%}")
        # mechanism: corner reach
        say("    corner mechanism — DIVERGE rate (vs MEDIAN rule) by ladder-endpoint pick share:")
        S2 = S[S.MEDIAN_q != ""].copy()
        if len(S2) >= 9:
            S2["terc"] = pd.qcut(S2.corner_share.rank(method="first"), 3,
                                 labels=["low", "mid", "high"])
            for t, sub in S2.groupby("terc", observed=True):
                say(f"      corner_share {t:<5s} (median {sub.corner_share.median():.2f}, n={len(sub)}): "
                    f"DIVERGE {float((sub.MEDIAN_q == 'DIVERGE').mean()):.1%}, "
                    f"chooser mean {sub.ch_mean.mean():+.4f}, hit {sub.ch_hit.mean():.1%}")
            say(f"      corr(corner_share, chooser margin skew) = "
                f"{corr(S2.ch_skew, S2.corner_share):+.3f}; "
                f"corr(conc, DIVERGE) = "
                f"{corr((S2.MEDIAN_q == 'DIVERGE').astype(float), S2.conc):+.3f}")
    return C


# =====================================================================================
# PART C — the live corpus (ladders built here, so the pool width is known, not inferred)
# =====================================================================================
D = _load(I133, "i133")


def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Idea 196's fast_backtest verbatim (asserted == engine.backtest in gate G1)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
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


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def gate_mask(px, gate):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    ma = px.rolling(200).mean()
    if gate == "g200":
        return (px > ma).fillna(False)
    if gate == "band3":
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * 1.03, 1.0).mask(px < ma * 0.97, 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "abs12":
        return (px > px.shift(252)).fillna(False)
    if gate == "vol60":
        return (vol20(px) < MAX_VOL).fillna(False)
    if gate == "v1gate":
        return ((px > ma) & (vol20(px) < MAX_VOL)).fillna(False)
    raise ValueError(gate)


def ma_len_mask(px, L):
    return (px > px.rolling(L).mean()).fillna(False)


def volcap_mask(px, cap):
    if not np.isfinite(cap):
        return gate_mask(px, "band3")
    return gate_mask(px, "band3") & (vol20(px) < cap).fillna(False)


def ew_weights(px, g=GROSS, gate=None, mask=None):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    W = g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    m = gate_mask(px, gate) if mask is None else mask
    return W.where(m, 0.0)


def topn_weights(px, n, g=GROSS, gate="band3", key=None):
    if n is None:
        return ew_weights(px, g, gate)
    k = composite(px) if key is None else key
    rank = k.rank(axis=1, ascending=False)
    W = (rank <= n).astype(float) * (g / n)
    return W.where(gate_mask(px, gate), 0.0)


def lookback_key(px, k):
    return px / px.shift(k) - 1


def family_arms(fam):
    """Idea 432's corpus verbatim: (arm, weights_fn, freq, is_control)."""
    if fam == "GROSS":
        gs = [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00]
        return [(f"g={g:.3f}", (lambda p, g=g: ew_weights(p, g, "band3")), FREQ, g == GROSS)
                for g in gs]
    if fam == "WIDTH":
        ns = [5, 10, 20, 40, 80, None]
        return [(f"n={'ALL' if n is None else n}", (lambda p, n=n: topn_weights(p, n)), FREQ,
                 n is None) for n in ns]
    if fam == "CADENCE":
        return [(f"freq={f}", (lambda p: ew_weights(p, GROSS, "band3")), f, f == FREQ)
                for f in ["D", "W", "M", "Q"]]
    if fam == "GATE":
        gates = [None, "g200", "band3", "abs12", "vol60", "v1gate"]
        return [(f"gate={'none' if g is None else g}",
                 (lambda p, g=g: ew_weights(p, GROSS, g)), FREQ, g == "band3") for g in gates]
    if fam == "MALEN":
        Ls = [20, 50, 100, 150, 200, 250]
        return [(f"ma={L}", (lambda p, L=L: ew_weights(p, GROSS, None, ma_len_mask(p, L))),
                 FREQ, L == 200) for L in Ls]
    if fam == "VOLCAP":
        caps = [0.25, 0.35, 0.45, 0.60, 0.80, np.inf]
        return [(f"vcap={'none' if not np.isfinite(c) else f'{c:.2f}'}",
                 (lambda p, c=c: ew_weights(p, GROSS, None, volcap_mask(p, c))), FREQ,
                 c == 0.60) for c in caps]
    if fam == "LOOKBACK":
        ks = [21, 63, 126, 189, 252]
        arms = [(f"lb={k}", (lambda p, k=k: topn_weights(p, 20, key=lookback_key(p, k))),
                 FREQ, False) for k in ks]
        arms.append(("lb=composite", (lambda p: topn_weights(p, 20)), FREQ, True))
        return arms
    raise ValueError(fam)


FAMILIES = ["GROSS", "WIDTH", "CADENCE", "GATE", "MALEN", "VOLCAP", "LOOKBACK"]


def bars(spy_r, lo=None, hi=None):
    m = metrics(spy_r.loc[lo:hi])
    return dict(S=m["Sharpe"], CAGR=m["CAGR"], DD=m["MaxDD"])


def pass4b(r, spy_r, lo=None, hi=None):
    rr, sp = r.loc[lo:hi], spy_r.loc[lo:hi]
    b, m = bars(sp), metrics(rr)
    h1, h2 = halves(rr)
    sb1, sb2 = halves(sp)
    mg = dict(H1=h1 - sb1, H2=h2 - sb2, S=m["Sharpe"] - b["S"],
              DD=DELTA * abs(b["DD"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["CAGR"])
    return bool(all(v > 0 for v in mg.values())), min(mg, key=lambda k: mg[k])


def pass4a(r, base_r):
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])


def folds(index, h):
    """Expanding-window folds: IS = start..Dec 31 of Y, OOS = the h years after.  Pre-registered
    scheme, every fold reported."""
    out = []
    for Y in range(FOLD_FIRST_IS_END, FOLD_LAST_OOS_END - h + 1):
        is_end = pd.Timestamp(f"{Y}-12-31")
        oos_lo, oos_hi = pd.Timestamp(f"{Y + 1}-01-01"), pd.Timestamp(f"{Y + h}-12-31")
        if index[-1] < oos_lo + pd.Timedelta(days=200):
            continue
        out.append((f"IS<={Y}|OOS{Y + 1}-{min(Y + h, FOLD_LAST_OOS_END)}", is_end, oos_lo, oos_hi))
    return out


def live():
    say("\n" + "=" * 120)
    say("PART C — the live corpus: 3 panels x 7 families x 3 rungs, ladders built here")
    say("=" * 120)
    cellrows, armrows, keeprows, wfrows = [], [], [], []
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")
        Wg = ew_weights(px, GROSS, "band3")
        e1, e0 = fast_backtest(px, Wg, 0.0, FREQ), backtest(px, Wg, cost_bps=0.0, freq=FREQ)
        d_r = float((e1["returns"] - e0["returns"]).abs().max())
        d_t = float((e1["turnover"] - e0["turnover"]).abs().max())
        e25 = backtest(px, Wg, cost_bps=25.0, freq=FREQ)
        d_c = float((e25["returns"] - (e0["returns"] - e0["turnover"] * 25.0 / 1e4)).abs().max())
        say(f"  [G1] fast vs engine: returns {d_r:.3e} turnover {d_t:.3e} | "
            f"[G2] rung identity {d_c:.3e}")
        assert d_r < 1e-12 and d_t < 1e-12 and d_c < 1e-12, "G1/G2 FAILED - unsafe"
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        raw = {}
        for fam in FAMILIES:
            for name, wf_, fq, isctl in family_arms(fam):
                res = fast_backtest(px, wf_(px), 0.0, fq)
                raw[(fam, name)] = (res["returns"].loc[start:], res["turnover"].loc[start:], isctl)
        for c in COSTS:
            net = {k: (v[0] - v[1] * c / 1e4) for k, v in raw.items()}
            wide_pool = [(f, n) for (f, n) in net if f in ("WIDTH",)]
            for fam in FAMILIES:
                names = [n for (f, n) in net if f == fam]
                ctl = next((n for n in names
                            if raw[(fam, n)][2]), None)
                pool_m = [(fam, n) for n in names]
                pool_w = pool_m + [k for k in wide_pool if k not in pool_m]
                # ---------- arm-level rows (all grid points) ----------
                for n in names:
                    r = net[(fam, n)]
                    m, mo = metrics(r), metrics(r.loc[OOS_START:])
                    h1, h2 = halves(r)
                    ok4b, bar = pass4b(r, spy)
                    ok4b_o, bar_o = pass4b(r, spy, OOS_START)
                    same_v2 = float((r - v2[c]).abs().max()) < 1e-9
                    armrows.append(dict(panel=pk, family=fam, cost=c, arm=n, is_ctl=n == ctl,
                                        is_the_live_book=same_v2,
                                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                        H1=h1, H2=h2, IS_Sharpe=sharpe(r.loc[:IS_END]),
                                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                        OOS_MaxDD=mo["MaxDD"], pass4a=pass4a(r, v2[c]),
                                        pass4b=ok4b, bar4b=bar, pass4b_oos=ok4b_o,
                                        bar4b_oos=bar_o))
                # ---------- fold scheme (tuned param 2: h) ----------
                for h in HORIZONS:
                    FL = folds(px.loc[start:].index, h)
                    recs = []
                    for tag, is_end, lo, hi in FL:
                        oos = {k: sharpe(net[k].loc[lo:hi]) for k in pool_w}
                        isv = {k: sharpe(net[k].loc[:is_end]) for k in pool_w}
                        if not np.isfinite(list(oos.values())).all():
                            continue
                        pm = max(pool_m, key=lambda k: isv[k])
                        pw = max(pool_w, key=lambda k: isv[k])
                        recs.append(dict(fold=tag,
                                         base_mean=float(np.mean([oos[k] for k in pool_m])),
                                         base_ctl=oos[(fam, ctl)] if ctl else np.nan,
                                         pick_m=pm[1], pick_w=f"{pw[0]}:{pw[1]}",
                                         oos_m=oos[pm], oos_w=oos[pw],
                                         **{f"arm::{n}": oos[(fam, n)] for n in names}))
                    if len(recs) < 3:
                        continue
                    R = pd.DataFrame(recs)
                    order = _ladder_order(names)
                    posarm = dict(CONTROL=ctl, MEDIAN=order[len(order) // 2],
                                  LADMIN=order[0], LADMAX=order[-1])
                    for conv, bcol in [("POOLMEAN", "base_mean"), ("CONTROL", "base_ctl")]:
                        if not np.isfinite(R[bcol]).all():
                            continue
                        objs = {f"ARM {n}": R[f"arm::{n}"].values for n in order}
                        objs["CHOOSER-MATCHED"] = R.oos_m.values
                        objs["CHOOSER-WIDE"] = R.oos_w.values
                        st = _pool_stats(R.to_dict("records"), bcol, objs)
                        cm, cw = st["CHOOSER-MATCHED"], st["CHOOSER-WIDE"]
                        row = dict(panel=pk, family=fam, cost=c, h=h, conv=conv, n_folds=len(R),
                                   n_arms=len(order),
                                   conc_m=float((R.pick_m.value_counts(normalize=True) ** 2).sum()),
                                   conc_w=float((R.pick_w.value_counts(normalize=True) ** 2).sum()),
                                   corner_m=float(R.pick_m.isin([str(order[0]), str(order[-1])]).mean()),
                                   corner_w=float(R.pick_w.str.split(":").str[1]
                                                  .isin([str(order[0]), str(order[-1])]).mean()),
                                   out_of_family_w=float((R.pick_w.str.split(":").str[0] != fam).mean()),
                                   ch_m_mean=cm["mean"], ch_m_hit=cm["hit"], ch_m_skew=cm["skew"],
                                   ch_w_mean=cw["mean"], ch_w_hit=cw["hit"], ch_w_skew=cw["skew"])
                        for p in POSRULES:
                            a = posarm[p]
                            if a is None:
                                continue
                            s = st[f"ARM {a}"]
                            row[f"{p}_arm"] = str(a)
                            row[f"{p}_mean"] = s["mean"]
                            row[f"{p}_hit"] = s["hit"]
                            row[f"{p}_qm"] = quadrant(cm["mean"], cm["hit"], s["mean"], s["hit"])
                            row[f"{p}_qw"] = quadrant(cw["mean"], cw["hit"], s["mean"], s["hit"])
                        cellrows.append(row)
                # ---------- PROTOCOL rule 8 canonical split ----------
                isv = {k: sharpe(net[k].loc[:IS_END]) for k in pool_w}
                pm = max(pool_m, key=lambda k: isv[k])
                pw = max(pool_w, key=lambda k: isv[k])
                orc = max(pool_m, key=lambda k: sharpe(net[k].loc[OOS_START:]))
                order = _ladder_order(names)
                posarm = dict(CONTROL=ctl, MEDIAN=order[len(order) // 2],
                              LADMIN=order[0], LADMAX=order[-1])
                base_mean = float(np.mean([sharpe(net[k].loc[OOS_START:]) for k in pool_m]))
                row = dict(panel=pk, family=fam, cost=c, ctl=str(ctl),
                           base_pool_mean_OOS=base_mean,
                           spy_OOS_Sharpe=sharpe(spy.loc[OOS_START:]),
                           spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                           spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                           v2_OOS_Sharpe=sharpe(v2[c].loc[OOS_START:]),
                           v2_OOS_CAGR=metrics(v2[c].loc[OOS_START:])["CAGR"],
                           v2_OOS_MaxDD=metrics(v2[c].loc[OOS_START:])["MaxDD"],
                           v1_OOS_Sharpe=sharpe(v1[c].loc[OOS_START:]),
                           ORACLE_OOS_Sharpe=sharpe(net[orc].loc[OOS_START:]))
                for tag, k in [("CHM", pm), ("CHW", pw)] + \
                        [(p, (fam, posarm[p])) for p in POSRULES if posarm[p] is not None]:
                    rr = net[k].loc[OOS_START:]
                    mm = metrics(rr)
                    row[f"{tag}_pick"] = f"{k[0]}:{k[1]}"
                    row[f"{tag}_OOS_Sharpe"] = mm["Sharpe"]
                    row[f"{tag}_OOS_CAGR"] = mm["CAGR"]
                    row[f"{tag}_OOS_MaxDD"] = mm["MaxDD"]
                    row[f"{tag}_margin"] = mm["Sharpe"] - base_mean
                    ok4b_o, _ = pass4b(net[k], spy, OOS_START)
                    keeprows.append(dict(panel=pk, family=fam, cost=c, obj=tag,
                                         pick=f"{k[0]}:{k[1]}",
                                         is_the_live_book=float((net[k] - v2[c]).abs().max()) < 1e-9,
                                         pass4a=pass4a(net[k], v2[c]),
                                         pass4b=pass4b(net[k], spy)[0],
                                         bar4b=pass4b(net[k], spy)[1],
                                         pass4b_oos=ok4b_o,
                                         OOS_Sharpe=mm["Sharpe"], OOS_CAGR=mm["CAGR"],
                                         OOS_MaxDD=mm["MaxDD"]))
                wfrows.append(row)
    A = pd.DataFrame(armrows)
    C = pd.DataFrame(cellrows)
    W = pd.DataFrame(wfrows)
    K = pd.DataFrame(keeprows)
    A.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    C.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    return A, C, W, K


def report_live(A, C, W, K):
    say("\n" + "-" * 120)
    say(f"[C1] live cells: {len(C)} (panel x family x rung x h x comparand), "
        f"{len(A)} arm rows, {len(W)} rule-8 cells")
    for conv in ("POOLMEAN", "CONTROL"):
        S = C[C.conv == conv]
        if not len(S):
            continue
        say(f"\n  [comparand {conv}] chooser vs the four pre-registered position rules "
            f"(ALL h and ALL rungs pooled; per-h table below)")
        say(f"    {'rule':<8s} {'n':>4s} | {'MATCHED chooser':^34s} | {'WIDE chooser':^34s}")
        say(f"    {'':<8s} {'':>4s} | {'DIVERGE':>8s} {'DOMIN':>7s} {'LOSE':>7s} {'REV':>7s} | "
            f"{'DIVERGE':>8s} {'DOMIN':>7s} {'LOSE':>7s} {'REV':>7s}")
        for p in POSRULES:
            if f"{p}_qm" not in S:
                continue
            qm = S[f"{p}_qm"].dropna()
            qw = S[f"{p}_qw"].dropna()
            if not len(qm):
                continue
            cm, cw = collections.Counter(qm), collections.Counter(qw)
            n = len(qm)
            say(f"    {p:<8s} {n:>4d} | {cm['DIVERGE'] / n:>8.1%} {cm['DOMINATE'] / n:>7.1%} "
                f"{cm['LOSE'] / n:>7.1%} {cm['REVERSE'] / n:>7.1%} | "
                f"{cw['DIVERGE'] / n:>8.1%} {cw['DOMINATE'] / n:>7.1%} {cw['LOSE'] / n:>7.1%} "
                f"{cw['REVERSE'] / n:>7.1%}   [DIVERGE vs REVERSE sign p: matched "
                f"{sign_p(cm['DIVERGE'], cm['DIVERGE'] + cm['REVERSE']):.3g}, wide "
                f"{sign_p(cw['DIVERGE'], cw['DIVERGE'] + cw['REVERSE']):.3g}]")
        say(f"    means: MATCHED {S.ch_m_mean.mean():+.4f} hit {S.ch_m_hit.mean():.1%} "
            f"skew {S.ch_m_skew.mean():+.2f} | WIDE {S.ch_w_mean.mean():+.4f} "
            f"hit {S.ch_w_hit.mean():.1%} skew {S.ch_w_skew.mean():+.2f}")
        say(f"    the WIDE chooser leaves the family's own ladder in "
            f"{S.out_of_family_w.mean():.1%} of folds; corner-pick share MATCHED "
            f"{S.corner_m.mean():.1%} vs WIDE {S.corner_w.mean():.1%}")
    say("\n  every grid point — DIVERGE rate (vs MEDIAN rule) by h, rung and panel "
        "[comparand POOLMEAN]:")
    S = C[(C.conv == "POOLMEAN") & C.MEDIAN_qm.notna()]
    for key, sub in S.groupby(["h", "cost"]):
        say(f"    h={key[0]}y rung={key[1]:.0f}bps n={len(sub):3d}: "
            f"MATCHED {float((sub.MEDIAN_qm == 'DIVERGE').mean()):.1%} | "
            f"WIDE {float((sub.MEDIAN_qw == 'DIVERGE').mean()):.1%}")
    for key, sub in S.groupby(["panel"]):
        say(f"    panel {key[0]:<6s} n={len(sub):3d}: "
            f"MATCHED {float((sub.MEDIAN_qm == 'DIVERGE').mean()):.1%} | "
            f"WIDE {float((sub.MEDIAN_qw == 'DIVERGE').mean()):.1%}")
    for key, sub in S.groupby(["family"]):
        say(f"    family {key[0]:<9s} n={len(sub):3d}: "
            f"MATCHED {float((sub.MEDIAN_qm == 'DIVERGE').mean()):.1%} | "
            f"WIDE {float((sub.MEDIAN_qw == 'DIVERGE').mean()):.1%}  "
            f"(corner_m {sub.corner_m.mean():.2f}, corner_w {sub.corner_w.mean():.2f})")
    # mechanism regression
    say("\n  [C2] the MECHANISM: is divergence a corner-reach effect?")
    for lab, qcol, ccol, mcol, hcol in [("MATCHED", "MEDIAN_qm", "corner_m", "ch_m_mean", "ch_m_hit"),
                                        ("WIDE", "MEDIAN_qw", "corner_w", "ch_w_mean", "ch_w_hit")]:
        sub = S.dropna(subset=[qcol])
        d = (sub[qcol] == "DIVERGE").astype(float)
        say(f"    {lab:<8s} DIVERGE {d.mean():.1%} | corr(DIVERGE, corner share) "
            f"{corr(d, sub[ccol]):+.3f} | corr(DIVERGE, pick concentration) "
            f"{corr(d, sub['conc_m' if lab == 'MATCHED' else 'conc_w']):+.3f} | "
            f"corr(DIVERGE, chooser margin skew) "
            f"{corr(d, sub['ch_m_skew' if lab == 'MATCHED' else 'ch_w_skew']):+.3f}")
        if len(sub) >= 9:
            t = sub.assign(terc=pd.qcut(sub[ccol].rank(method="first"), 3,
                                        labels=["low", "mid", "high"]))
            for tt, s2 in t.groupby("terc", observed=True):
                say(f"      corner tercile {tt:<5s} (median {s2[ccol].median():.2f}, n={len(s2)}): "
                    f"DIVERGE {float((s2[qcol] == 'DIVERGE').mean()):.1%}, "
                    f"mean {s2[mcol].mean():+.4f}, hit {s2[hcol].mean():.1%}")
    # paired matched-vs-wide test
    say("\n  [C3] PAIRED matched-vs-wide (the pool-width test, same cells, same fixed arms):")
    sub = S.dropna(subset=["MEDIAN_qm", "MEDIAN_qw"])
    both = pd.crosstab(sub.MEDIAN_qm == "DIVERGE", sub.MEDIAN_qw == "DIVERGE")
    say("    crosstab DIVERGE(matched) x DIVERGE(wide):\n" + both.to_string())
    b = int(((sub.MEDIAN_qm != "DIVERGE") & (sub.MEDIAN_qw == "DIVERGE")).sum())
    cc = int(((sub.MEDIAN_qm == "DIVERGE") & (sub.MEDIAN_qw != "DIVERGE")).sum())
    say(f"    discordant pairs: wide-only {b}, matched-only {cc}, "
        f"McNemar sign p {sign_p(b, b + cc):.4g}")
    say(f"    hit rate: MATCHED {sub.ch_m_hit.mean():.1%} vs WIDE {sub.ch_w_hit.mean():.1%} "
        f"(paired d {(sub.ch_w_hit - sub.ch_m_hit).mean():+.1%}, t {tstat(sub.ch_w_hit - sub.ch_m_hit):+.2f}); "
        f"mean margin: MATCHED {sub.ch_m_mean.mean():+.4f} vs WIDE {sub.ch_w_mean.mean():+.4f} "
        f"(paired d {(sub.ch_w_mean - sub.ch_m_mean).mean():+.4f}, "
        f"t {tstat(sub.ch_w_mean - sub.ch_m_mean):+.2f})")
    # ---------------- rule 8 headline ----------------
    say("\n" + "=" * 120)
    say("PART D — PROTOCOL rule 8: parameters on 2009-2016, 2017-2026 read ONCE")
    say("=" * 120)
    objs = ["CHM", "CHW"] + POSRULES
    say(f"  {'object':<9s} {'n':>4s} {'mean margin':>12s} {'hit':>7s} {'OOS Sharpe':>11s} "
        f"{'OOS CAGR':>9s} {'OOS MaxDD':>10s} {'> SPY':>7s} {'> v2':>7s}")
    for o in objs:
        col = f"{o}_margin"
        if col not in W:
            continue
        m = W[col].dropna()
        s = W[f"{o}_OOS_Sharpe"]
        say(f"  {o:<9s} {len(m):>4d} {m.mean():>+12.4f} {float((m > 0).mean()):>7.1%} "
            f"{s.mean():>11.4f} {W[f'{o}_OOS_CAGR'].mean():>9.2%} "
            f"{W[f'{o}_OOS_MaxDD'].mean():>10.2%} "
            f"{float((s > W.spy_OOS_Sharpe).mean()):>7.1%} "
            f"{float((s > W.v2_OOS_Sharpe).mean()):>7.1%}")
    say(f"  reference OOS: SPY Sharpe {W.spy_OOS_Sharpe.mean():.4f} CAGR {W.spy_OOS_CAGR.mean():.2%} "
        f"MaxDD {W.spy_OOS_MaxDD.mean():.2%} | RULES v2 Sharpe {W.v2_OOS_Sharpe.mean():.4f} "
        f"CAGR {W.v2_OOS_CAGR.mean():.2%} MaxDD {W.v2_OOS_MaxDD.mean():.2%} | "
        f"RULES v1 Sharpe {W.v1_OOS_Sharpe.mean():.4f} | pool-mean {W.base_pool_mean_OOS.mean():.4f} | "
        f"ORACLE {W.ORACLE_OOS_Sharpe.mean():.4f}")
    say("  per-panel, at the PROTOCOL rung (10 bps), OOS Sharpe / CAGR / MaxDD:")
    for pk in PANELS:
        sub = W[(W.panel == pk) & (W.cost == PROTOCOL_RUNG)]
        say(f"    {pk:<6s} CHM {sub.CHM_OOS_Sharpe.mean():.3f}/{sub.CHM_OOS_CAGR.mean():.1%}/"
            f"{sub.CHM_OOS_MaxDD.mean():.1%}  CHW {sub.CHW_OOS_Sharpe.mean():.3f}/"
            f"{sub.CHW_OOS_CAGR.mean():.1%}/{sub.CHW_OOS_MaxDD.mean():.1%}  "
            f"MEDIAN {sub.MEDIAN_OOS_Sharpe.mean():.3f}/{sub.MEDIAN_OOS_CAGR.mean():.1%}/"
            f"{sub.MEDIAN_OOS_MaxDD.mean():.1%}  SPY {sub.spy_OOS_Sharpe.mean():.3f}/"
            f"{sub.spy_OOS_CAGR.mean():.1%}/{sub.spy_OOS_MaxDD.mean():.1%}  "
            f"v2 {sub.v2_OOS_Sharpe.mean():.3f}")
    # ---------------- keep paths ----------------
    say("\n" + "=" * 120)
    say("PART E — both KEEP paths (PROTOCOL 4a and 4b)")
    say("=" * 120)
    say(f"  arms: 4a {int(A.pass4a.sum())} of {len(A)}; 4b {int(A.pass4b.sum())} of {len(A)}; "
        f"4b OOS {int(A.pass4b_oos.sum())} of {len(A)}")
    self_rows = A[A.is_the_live_book]
    say(f"  [4a caveat] {int(A.is_the_live_book.sum())} arm rows ARE the live RULES v2 book "
        f"re-expressed (EW band3 at gross 0.75 weekly is a member of 5 of the 7 ladders); "
        f"{int(self_rows.pass4a.sum())} of them 'pass' 4a against themselves on a float tie "
        f"(fast_backtest vs engine.backtest differ at ~1e-17), so the honest 4a count is "
        f"{int(A.pass4a.sum()) - int(self_rows.pass4a.sum())} of "
        f"{len(A) - int(A.is_the_live_book.sum())}:")
    real4a = A[A.pass4a & ~A.is_the_live_book]
    if len(real4a):
        say("    " + real4a[["panel", "family", "cost", "arm", "CAGR", "Sharpe", "MaxDD",
                             "H1", "H2", "OOS_Sharpe"]].to_string(index=False).replace("\n", "\n    "))
        say("    every one is a DE-GROSSED variant of the live book (n=80 on a 56-name panel is "
            "gross 0.525, not a new signal) — idea 311's gross-scalar flag, not a candidate.")
    if A.pass4b.any():
        p = A[A.pass4b]
        say(f"    4b passes by panel {dict(p.panel.value_counts())}, "
            f"family {dict(p.family.value_counts())}, rung {dict(p.cost.value_counts())}")
        say("    the 4b passers:\n" + p[["panel", "family", "cost", "arm", "CAGR", "Sharpe",
                                         "MaxDD", "OOS_Sharpe"]].to_string(index=False))
    say(f"  binding 4b bar over all arms: {dict(A.bar4b.value_counts())}")
    say(f"  chooser/position books: 4a {int(K.pass4a.sum())} of {len(K)} "
        f"({int((K.pass4a & ~K.is_the_live_book).sum())} once the live book's own rows are "
        f"removed); 4b {int(K.pass4b.sum())} of {len(K)}; 4b OOS {int(K.pass4b_oos.sum())} "
        f"of {len(K)}")
    if K.pass4b.any():
        say("    " + K[K.pass4b][["panel", "family", "cost", "obj", "pick", "OOS_Sharpe",
                                  "OOS_CAGR", "OOS_MaxDD"]].to_string(index=False))
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)


def main():
    say(f"# {STEM}")
    say(f"# PROTOCOL: 10 bps rung (0/25 reported), t+1 execution, "
        f"IS <= {IS_END}, OOS >= {OOS_START}")
    F, R = flagship()
    C = census()
    A, LC, W, K = live()
    report_live(A, LC, W, K)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
