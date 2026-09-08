#!/usr/bin/env python3
"""QUEUE idea 436 — price-ORACLE-OOS-as-the-headroom-column-beside-every-selector-kill
   (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 436)
    "idea 203's rule-8 table has perfect hindsight over the whole tau ladder buying only
     +0.0336 of OOS Sharpe, which makes 'the selector loses to do-nothing' unfalsifiable for
     that family.  Back-fill the oracle gap wherever a committed walk-forward CSV survives and
     report how many of the record's 12 selector kills were run on ladders with no headroom to
     find.  Max 2 params."

THE STATISTIC, WRITTEN OUT BEFORE IT IS RUN
    For a pool P of arms with OOS metric M(a) and a do-nothing control c,

        H_ctl  := max_{a in P} M(a) - M(c)        (control convention)
        H_mean := max_{a in P} M(a) - mean_P M    (pool-mean convention, "pick at random")

    Any selector R that maps information to an arm of P obeys  M(R) - M(c) <= H_ctl.  So
    H = 0 is a PROOF that the kill was unfalsifiable, and the queue's instinct is right.

THE TWO THINGS THE QUEUE DID NOT NOTICE (both measured here, neither argued)
    (i) H IS A MAXIMUM, SO IT IS UPWARD-BIASED.  Even when every arm has exactly the same true
        Sharpe, max-minus-mean over A arms is strictly positive in every finite sample.  A
        column that reads "ORACLE-OOS +0.0286" therefore does NOT establish that there was
        anything to find; it establishes that a max was taken.  The falsifiability certificate
        the queue wants is NET headroom: H minus the H that pure noise produces in the SAME
        pool, estimated here by a paired stationary-block bootstrap that equalises every arm's
        true Sharpe while preserving each arm's own vol, its higher moments and the pool's
        cross-arm correlation.  Raw H and net H are both reported everywhere.
   (ii) H IS NOT AVAILABLE AT DECISION TIME.  ORACLE-OOS is computed on the OOS window the rule
        is not allowed to look at.  As a LEADERBOARD column beside a finished kill it is fine;
        as a screen ("only run selectors where there is headroom") it needs the IS twin to
        predict the OOS one.  That link is measured (L2) and then priced under PROTOCOL rule 8
        as an actual instrument (L3), because a column the record cannot act on and a column
        the record can act on are different recommendations.

WHAT THIS RUN DOES
    G   GATES.  fast_backtest == engine.backtest; the cost-rung turnover identity; and the
        reconstruction gate that matters — on every committed CSV that PUBLISHES an oracle /
        best-in-pool column, does this run's pool reconstruction reproduce it?
    C1  THE BACK-FILL.  Every committed CSV under research/backtests (1,664 files) is read and
        tiered: T1 publishes an oracle column, T2 is pool-reconstructable from its own rows,
        T3 cannot be re-read for headroom at all.  Per-file headroom distributions, and the
        share of pools under a reported threshold ladder.  The T3 count is a finding, not a
        failure: it says how much of the record cannot be audited this way.
    C2  THE KILL JOIN, and the count the queue asks for.  Every LEADERBOARD row whose text
        makes a selector-vs-do-nothing kill claim is extracted, joined to its script stem's
        committed CSVs, and given a headroom reading.  Because the record's "12" is an ORDINAL
        in a running streak sentence and not a set, the streak counters are audited too.
    L1  LIVE LADDERS.  63 pools (3 panels x 7 dial families x 3 cost rungs, 41 arms per panel)
        rebuilt here, so headroom can be measured against a null instead of only tallied:
        H_IS, H_OOS under both conventions, the noise floor H0 by block bootstrap, net headroom
        and its bootstrap p-value.
    L2  IS THE COLUMN PREDICTIVE?  corr(H_IS, H_OOS), corr(H_IS, realised selector gain), and
        the selector-gain distribution by H tercile.
    L3  RULE 8 (PROTOCOL 8).  Pre-registered instrument R(tau, s): take the IS-argmax pick in a
        pool whose IS headroom under statistic s exceeds tau, else the pool's own do-nothing
        control.  tau is chosen on an INNER IS split (fit <= 2013-12-31, choose on 2014-2016)
        and the outer window 2017-2026 is read ONCE.  Every tau on the grid is reported anyway,
        against S0 do-nothing, S1 always-pick, ORACLE-OOS, RULES v2, RULES v1 and SPY.
    L4  BOTH KEEP PATHS (PROTOCOL 4a and 4b) on every arm and every rule-selected book, full
        sample and OOS.  This is a diagnostic idea and is not expected to promote a book; the
        paths are scored because PROTOCOL requires it.

TUNED PARAMETERS (exactly 2, every grid point reported, nothing else selected on)
    1. tau - the headroom gate in L3 (11 points: 0 and the deciles of the IS headroom sample).
    2. s   - the headroom statistic, ctl or mean (2 points, both reported end to end).
    Panels, families, cost rungs, block length L, bootstrap draws, census thresholds and
    metrics are REPORTED axes and are never selected on.

PRE-REGISTERED PREDICTIONS (written before any number below was computed)
    P1  Raw H_OOS_mean is positive in essentially every live pool (a max exceeds a mean by
        construction), but NET headroom is indistinguishable from zero in a MAJORITY of them.
        The raw column over-states what was there to find.
    P2  The record's kill ladders are mostly small-H: over half the reconstructable kill-row
        pools come in under 0.10 of Sharpe on H_mean.
    P3  IS headroom does NOT carry to OOS: |corr(H_IS, H_OOS)| < 0.3 across the 63 live pools.
        If so the column is a post-hoc diagnostic and must not be adopted as a screen.
    P4  Under rule 8, R(tau*) does not beat do-nothing - the record's straight-line result for
        every clause-gated selector so far.
    P5  The queue's "12 selector kills" is not a recoverable set: the LEADERBOARD carries more
        than 12 kill rows and more than one parallel ordinal streak.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): u56, broad and small are current constituents.  Every CAGR here
      is flattered.  Every statistic is a WITHIN-POOL contrast, which the level bias does not
      move; no level below is an achievable return.
    * The census reconstruction is a HEURISTIC over heterogeneous committed files: it infers a
      cell/arm split from column names and cardinalities.  It is therefore quoted with (a) the
      published-oracle reproduction gate, (b) the count of files where the arm column is
      AMBIGUOUS, and (c) the min/median/max headroom across EVERY admissible arm column, not
      only the chosen one.  Where those disagree the file is reported as ambiguous rather than
      resolved.
    * A reconstructed "pool" is not always a selector's real choice set - some committed grids
      pool over reported axes.  This inflates pool size and therefore H, which cuts AGAINST
      the finding that H is small.  The bias is conservative and stated rather than corrected.
    * 63 live pools are not 63 independent observations: arms and panels overlap heavily.
      Every t is quoted with its n, and the bootstrap resamples time blocks, not rows.
    * data/prices.csv was rewritten 2026-09-07 (idea 401), so reproductions of older committed
      numbers are quoted per number rather than asserted bit-exact.
    * PROTOCOL rung is 10 bps; 0 and 25 bps are reported.  All books are t+1 execution.

Deterministic (seeded), standalone, offline.  Writes .console.txt, .census.csv, .kills.csv,
.cells.csv, .walkforward.csv and .keeppaths.csv next to itself.  Modifies nothing.
"""
import collections
import glob
import zlib
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

STEM = "2026-09-08_price-ORACLE-OOS-as-the-headroom-column-beside-every-selector-kill_C"
OUT = ROOT / "research" / "backtests"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

FREQ = "W"
GROSS = 0.75
MAX_VOL = 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
INNER_END, INNER2_START = "2013-12-31", "2014-01-01"
PHI, DELTA = 0.70, 0.60                 # PROTOCOL 4b CAGR floor / MaxDD cap
BLOCK_LENS = [5, 21, 63]                # reported axis; PRE-REGISTERED primary = 21
BLOCK_PRIMARY = 21
N_BOOT = 500
SEED = 436
CENSUS_THRESH = [0.0, 0.01, 0.02, 0.05, 0.10, 0.20]
ROW_CAP = 400_000                       # per-file read cap, files hitting it are flagged

pd.set_option("display.width", 340)
pd.set_option("display.max_columns", 200)
pd.set_option("display.max_rows", 4000)
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


def spearman(y, x):
    y, x = np.asarray(y, float), np.asarray(x, float)
    ok = np.isfinite(y) & np.isfinite(x)
    if ok.sum() < 3:
        return np.nan
    return corr(pd.Series(y[ok]).rank().values, pd.Series(x[ok]).rank().values)


def sign_p(wins, n):
    if n == 0:
        return np.nan
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


def window(r, which):
    if which == "IS":
        return r.loc[:IS_END]
    if which == "IS1":
        return r.loc[:INNER_END]
    if which == "IS2":
        return r.loc[INNER2_START:IS_END]
    if which == "OOS":
        return r.loc[OOS_START:]
    return r


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def sharpe(r):
    return float(metrics(r)["Sharpe"])


# =====================================================================================
# PART C — the back-fill census over committed CSVs
# =====================================================================================
# Column-name vocabulary, pre-registered.  A column is METRIC-like (never a cell/arm key) if
# its name matches METRIC; ARM-like names get priority when several key splits are admissible.
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
SELNAME = re.compile(r"(?i)^(sel|selector|chooser|rule|s|strategy|strat|method)$")
REFCOL = re.compile(r"(?i)spy|bench|base|ctl|control|v1|v2|anchor|live|null|do.?noth|pool")
BOOLISH = {"true", "false", "yes", "no", "keep", "kill", "park", "0", "1", "0.0", "1.0"}
CTLVAL = re.compile(r"(?i)^(control|ctl|do-?nothing|none|nothing|base|baseline|s0|off|no-?gate|"
                    r"identity|null|untreated|full|all)$")


def _is_oos_sharpe(c):
    cl = c.lower()
    return "oos" in cl and "sharpe" in cl


def _boolish(s):
    vals = {str(v).strip().lower() for v in pd.unique(s.dropna())}
    return len(vals) > 0 and vals.issubset(BOOLISH)


def key_candidates(df):
    """Columns admissible as a cell key or an arm key."""
    out = []
    n = len(df)
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


def pool_split(df, y, cands):
    """Every admissible (arm column -> pools) split, scored.  Returns list of dicts, best first.

    Score, pre-registered: number of cells with >= 3 arms, then ARM-name priority, then the
    pooled row count.  A pool needs >= 3 arms for max-minus-mean to mean anything."""
    opts = []
    for c in cands:
        others = [o for o in cands if o != c]
        try:
            if others:
                g = df.groupby(others, dropna=False)[y]
            else:
                g = df.assign(_one=0).groupby("_one")[y]
            sizes = g.size()
        except Exception:
            continue
        n3 = int((sizes >= 3).sum())
        if n3 == 0:
            continue
        opts.append(dict(arm=c, n_cells3=n3, pooled=int(sizes[sizes >= 3].sum()),
                         prio=1 if ARMNAME.match(str(c)) else 0, others=others))
    opts.sort(key=lambda d: (d["n_cells3"], d["prio"], d["pooled"]), reverse=True)
    return opts


def pools_from(df, y, opt, ctl_col=None):
    """Per-cell headroom rows for one admissible split."""
    others = opt["others"]
    rows = []
    grp = df.groupby(others, dropna=False) if others else [((), df)]
    for key, sub in (grp if others else grp):
        v = pd.to_numeric(sub[y], errors="coerce").astype(float)
        v = v[np.isfinite(v)]
        if len(v) < 3:
            continue
        mx, mn = float(v.max()), float(v.mean())
        ctl = np.nan
        if ctl_col is not None and ctl_col in sub.columns:
            cv = pd.to_numeric(sub[ctl_col], errors="coerce").astype(float)
            cv = cv[np.isfinite(cv)]
            if len(cv):
                ctl = float(cv.iloc[0])
        else:                                    # a row whose arm value NAMES the control
            av = sub[opt["arm"]].astype(str)
            hit = av[av.str.match(CTLVAL)]
            if len(hit):
                ctl = float(pd.to_numeric(sub.loc[hit.index[0], y], errors="coerce"))
        rows.append(dict(cell=str(key), src="recon", n_arms=int(len(v)), oracle=mx,
                         pool_mean=mn, ctl=ctl, H_mean=mx - mn,
                         H_ctl=(mx - ctl) if np.isfinite(ctl) else np.nan))
    return rows


def pools_published(df, pub_col, ctl_col, y):
    """EXACT headroom rows for a file that publishes BOTH an oracle column and a control
    column: H_ctl = oracle - control, read off the file, no reconstruction involved.  The
    pool-mean convention is not recoverable this way (the pool's other arms are not in the
    file), so H_mean is left NaN rather than approximated."""
    if pub_col is None or ctl_col is None:
        return []
    p = pd.to_numeric(df[pub_col], errors="coerce").astype(float)
    c = pd.to_numeric(df[ctl_col], errors="coerce").astype(float)
    ok = np.isfinite(p) & np.isfinite(c)
    return [dict(cell=str(i), src="published", n_arms=np.nan, oracle=float(p.iloc[i]),
                 pool_mean=np.nan, ctl=float(c.iloc[i]), H_mean=np.nan,
                 H_ctl=float(p.iloc[i] - c.iloc[i]))
            for i in range(len(df)) if ok.iloc[i]]


def census():
    """C1 — read every committed CSV, tier it, and price its headroom."""
    files = [f for f in sorted(glob.glob(str(OUT / "**" / "*.csv"), recursive=True))
             if not Path(f).name.startswith(STEM)]        # never census this run's own output
    say(f"\n[C1] BACK-FILL CENSUS over {len(files)} committed CSVs under research/backtests "
        f"(this run's own output files excluded)")
    tier = collections.Counter()
    frows, prows, gate_rows = [], [], []
    for f in files:
        base = Path(f).name
        try:
            head = pd.read_csv(f, nrows=0).columns.tolist()
        except Exception:
            tier["T3_unreadable"] += 1
            continue
        oos = [c for c in head if _is_oos_sharpe(c) and not REFCOL.search(str(c))
               and not re.search(r"(?i)best|oracle", str(c))]
        pub = [c for c in head if _is_oos_sharpe(c) and re.search(r"(?i)best|oracle", str(c))]
        if not oos:
            tier["T0_no_OOS_Sharpe_column"] += 1
            continue
        try:
            df = pd.read_csv(f, nrows=ROW_CAP)
        except Exception:
            tier["T3_unreadable"] += 1
            continue
        capped = len(df) >= ROW_CAP
        y = oos[0]
        cands = key_candidates(df)
        opts = pool_split(df, y, cands) if cands else []
        ctl_cols = [c for c in head if _is_oos_sharpe(c)
                    and re.search(r"(?i)ctl|control|base|anchor|v2|live|do.?noth|^S0", str(c))]
        ctl_col = ctl_cols[0] if ctl_cols else None
        if not opts:
            tier["T3_unrecoverable"] += 1
            frows.append(dict(file=base, tier="T3", n_cells=0, arm_col="", ambiguous="",
                              n_alt=0, H_mean_med=np.nan, H_mean_max=np.nan,
                              H_mean_med_lo=np.nan, H_mean_med_hi=np.nan,
                              published=bool(pub), capped=capped))
            continue
        prim = opts[0]
        rows = pools_from(df, y, prim, ctl_col)
        if not rows:
            tier["T3_unrecoverable"] += 1
            frows.append(dict(file=base, tier="T3", n_cells=0, arm_col="", ambiguous="",
                              n_alt=len(opts), H_mean_med=np.nan, H_mean_max=np.nan,
                              H_mean_med_lo=np.nan, H_mean_med_hi=np.nan,
                              published=bool(pub), capped=capped))
            continue
        H = np.array([r["H_mean"] for r in rows], float)
        # sensitivity: median H under EVERY admissible arm column (reported, never selected on)
        meds = []
        for o in opts[:4]:
            rr = pools_from(df, y, o, ctl_col)
            if rr:
                meds.append(float(np.median([x["H_mean"] for x in rr])))
        ambiguous = len(opts) > 1 and (max(meds) - min(meds) > 0.02 if meds else False)
        tier["T1_published" if pub else "T2_reconstructed"] += 1
        frows.append(dict(file=base, tier="T1" if pub else "T2", n_cells=len(rows),
                          arm_col=str(prim["arm"]), ambiguous=str(bool(ambiguous)),
                          n_alt=len(opts), H_mean_med=float(np.median(H)),
                          H_mean_max=float(H.max()),
                          H_mean_med_lo=float(min(meds)) if meds else np.nan,
                          H_mean_med_hi=float(max(meds)) if meds else np.nan,
                          published=bool(pub), capped=capped))
        for r in rows:
            prows.append(dict(file=base, **r))
        # EXACT rows wherever the file publishes an oracle AND a control column
        if pub:
            for r in pools_published(df, pub[0], ctl_col, y):
                prows.append(dict(file=base, **r))
        # G-RECON gate: does the reconstruction reproduce a PUBLISHED oracle column?
        if pub:
            pc = pub[0]
            others = prim["others"]
            try:
                g = df.groupby(others, dropna=False) if others else [((), df)]
                for key, sub in (g if others else g):
                    v = pd.to_numeric(sub[y], errors="coerce").astype(float)
                    p = pd.to_numeric(sub[pc], errors="coerce").astype(float)
                    v, p = v[np.isfinite(v)], p[np.isfinite(p)]
                    if len(v) >= 3 and len(p):
                        gate_rows.append(dict(file=base, recon=float(v.max()),
                                              published=float(p.iloc[0]),
                                              signed=float(v.max()) - float(p.iloc[0]),
                                              d=abs(float(v.max()) - float(p.iloc[0]))))
            except Exception:
                pass
    fdf = pd.DataFrame(frows)
    pdf = pd.DataFrame(prows)
    say("     tiers: " + ", ".join(f"{k} {v}" for k, v in sorted(tier.items())))
    say(f"     reconstructable pools: {len(pdf)} across "
        f"{fdf[fdf.tier.isin(['T1', 'T2'])].shape[0]} files; "
        f"ambiguous arm column in {int((fdf.ambiguous == 'True').sum())} files "
        f"({int((fdf.n_alt > 1).sum())} files admit >1 split); "
        f"row-capped files {int(fdf.capped.sum())}")
    if len(gate_rows):
        gdf = pd.DataFrame(gate_rows)
        ok = float((gdf.d <= 1e-9).mean())
        fl = gdf.groupby("file").signed.median()
        say(f"     [G-RECON] published oracle columns vs this run's reconstruction: "
            f"{len(gdf)} cells over {gdf.file.nunique()} files, exact {ok:.1%}, "
            f"median |d| {gdf.d.median():.3e}, max |d| {gdf.d.max():.3e}")
        say(f"     [G-RECON] **THE GATE DOES NOT PASS, and its DIRECTION is the finding:** "
            f"recon BELOW published in {int((fl < -1e-9).sum())} files, equal in "
            f"{int((fl.abs() <= 1e-9).sum())}, ABOVE in {int((fl > 1e-9).sum())}. A committed "
            f"walk-forward file usually holds only the PICKS, not the arm ladder, so a "
            f"row-max under-states the true oracle; where it over-states, the reconstruction "
            f"has pooled over a REPORTED axis. Net bias is DOWNWARD, i.e. the census below "
            f"finds LESS headroom than the record really had — which cuts AGAINST, not for, "
            f"the 'no headroom' reading. T2 numbers are bounds, not measurements.")
    else:
        say("     [G-RECON] no published-oracle cell was reconstructable — gate VACUOUS, said so")
    if len(pdf):
        rec, publ = pdf[pdf.src == "recon"], pdf[pdf.src == "published"]
        say(f"     pools by source: reconstructed {len(rec)}, published-exact {len(publ)} "
            f"(over {publ.file.nunique() if len(publ) else 0} files)")
        say(f"     H_mean over {len(rec)} RECONSTRUCTED pools: median {rec.H_mean.median():.4f}, "
            f"mean {rec.H_mean.mean():.4f}, p90 {rec.H_mean.quantile(0.90):.4f}, "
            f"max {rec.H_mean.max():.4f}")
        if len(publ):
            say(f"     H_ctl over {len(publ)} PUBLISHED-EXACT rows (oracle minus the file's own "
                f"control column, no reconstruction): median {publ.H_ctl.median():.4f}, "
                f"mean {publ.H_ctl.mean():.4f}, "
                f"share <= 0: {float((publ.H_ctl <= 0).mean()):.1%}, "
                f"share <= 0.05: {float((publ.H_ctl <= 0.05).mean()):.1%}, "
                f"share <= 0.10: {float((publ.H_ctl <= 0.10).mean()):.1%}")
        say("     share of pools at or below a threshold (ALL grid points reported):")
        for t in CENSUS_THRESH:
            sh = float((rec.H_mean <= t).mean())
            shc = float((rec.H_ctl <= t).mean()) if rec.H_ctl.notna().any() else np.nan
            shp = float((publ.H_ctl <= t).mean()) if len(publ) else np.nan
            say(f"       H <= {t:<5.2f}   recon H_mean {sh:6.1%}   recon H_ctl {shc:6.1%} "
                f"(n {int(rec.H_ctl.notna().sum())})   published H_ctl {shp:6.1%}")
        say(f"     pools with H_ctl <= 0 (the control IS the pool's OOS best): recon "
            f"{int((rec.H_ctl <= 0).sum())} of {int(rec.H_ctl.notna().sum())}, published "
            f"{int((publ.H_ctl <= 0).sum()) if len(publ) else 0} of {len(publ)}")
    return fdf, pdf


# ---------------------------------------------------------------- C2 kills ---
KILL = re.compile(
    r"(?i)lose[sd]? to (do-?nothing|doing nothing)|do-?nothing win|"
    r"beats? the .{0,40}control in 0 of|straight (gate )?(KILL|do-?nothing)|"
    r"no (selector|chooser|clause) (beats|finds)|loses to the ungated|"
    r"selector .{0,30}KILL|chooser .{0,30}(loses|KILL)")
ORD = re.compile(r"(?i)\b(second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
                 r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|"
                 r"eighteenth|nineteenth|twentieth)\b")


def kill_join(pdf):
    """C2 — the count the queue asks for."""
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in txt if l.startswith("|") and l.count("|") >= 9
            and not l.startswith("|---") and not l.startswith("| Date")]
    hits = [l for l in rows if KILL.search(l)]
    stems = []
    for l in hits:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        stems.append(cells[-1].strip("` ").replace(".py", ""))
    say(f"\n[C2] THE RECORD'S SELECTOR KILLS — LEADERBOARD rows {len(rows)}, "
        f"kill-claim rows {len(hits)}, distinct scripts {len(set(stems))}")
    # ordinal-streak audit: is "12 selector kills" a set?
    ords = collections.Counter()
    for l in rows:
        for m in ORD.finditer(l):
            ords[m.group(1).lower()] += 1
    say("     ordinal streak words used in LEADERBOARD verdict text: "
        + ", ".join(f"{k} x{v}" for k, v in sorted(ords.items(), key=lambda kv: -kv[1])[:12]))
    say(f"     total ordinal mentions {sum(ords.values())} over "
        f"{sum(1 for l in rows if ORD.search(l))} rows — the record runs SEVERAL parallel "
        f"streak counters (gate kills, do-nothing wins, 4b reproductions), so '12 selector "
        f"kills' names an ORDINAL, not a recoverable set.")
    # join each kill script stem to its own committed CSV pools
    pmap = collections.defaultdict(list)
    for r in pdf.itertuples():
        pmap[re.sub(r"\.[a-zA-Z_0-9]+\.csv$", "", r.file)].append(r)
    out = []
    for stem, line in zip(stems, hits):
        pool = pmap.get(stem, [])
        pub = [p for p in pool if p.src == "published"]
        rec = [p for p in pool if p.src == "recon"]
        H = np.array([p.H_mean for p in rec], float)
        H = H[np.isfinite(H)]
        Hc_pub = np.array([p.H_ctl for p in pub], float)
        Hc_pub = Hc_pub[np.isfinite(Hc_pub)]
        Hc_rec = np.array([p.H_ctl for p in rec], float)
        Hc_rec = Hc_rec[np.isfinite(Hc_rec)]
        # the EXACT reading wins where the script published one; else the recon bound
        Hc = Hc_pub if len(Hc_pub) else Hc_rec
        out.append(dict(stem=stem, n_pools=len(rec), n_published=len(pub),
                        src="published" if len(Hc_pub) else ("recon" if len(Hc_rec) else "none"),
                        H_mean_med=float(np.median(H)) if len(H) else np.nan,
                        H_mean_max=float(H.max()) if len(H) else np.nan,
                        H_ctl_med=float(np.median(Hc)) if len(Hc) else np.nan,
                        H_ctl_max=float(Hc.max()) if len(Hc) else np.nan,
                        share_H_le_005=float((H <= 0.05).mean()) if len(H) else np.nan,
                        share_H_le_010=float((H <= 0.10).mean()) if len(H) else np.nan,
                        claim=line[:220]))
    kdf = pd.DataFrame(out).drop_duplicates(subset=["stem", "claim"])
    have = kdf[kdf.n_pools > 0]
    hc = kdf[kdf.H_ctl_med.notna()]
    say(f"     kill rows whose own script has reconstructable pools: {len(have)} of {len(kdf)} "
        f"({len(kdf) - len(have)} kills CANNOT be re-read for headroom at all)")
    say(f"     kill rows with a CONTROL-convention headroom at all: {len(hc)} "
        f"({int((kdf.src == 'published').sum())} of them read EXACTLY off the script's own "
        f"published oracle column, {int((kdf.src == 'recon').sum())} reconstructed)")
    if len(have):
        say(f"     [recon, POOL-MEAN convention, a bound not a measurement] median-of-medians "
            f"H_mean on kill ladders {have.H_mean_med.median():.4f}, "
            f"mean {have.H_mean_med.mean():.4f}")
        for t in (0.02, 0.05, 0.10, 0.20):
            n = int((have.H_mean_med <= t).sum())
            say(f"       kills whose ladder's MEDIAN H_mean <= {t:.2f}: {n} of {len(have)} "
                f"({n / len(have):.0%})")
    if len(hc):
        say(f"     [CONTROL convention — the quantity a selector kill is actually bounded by] "
            f"median-of-medians H_ctl {hc.H_ctl_med.median():.4f}")
        for t in (0.0, 0.02, 0.05, 0.10, 0.20):
            n = int((hc.H_ctl_med <= t).sum())
            say(f"       kills whose ladder's MEDIAN H_ctl <= {t:+.2f}: {n} of {len(hc)} "
                f"({n / len(hc):.0%})")
        say(f"     kills where the ladder's BEST arm never beat the control at all "
            f"(max H_ctl <= 0 — the kill was unfalsifiable by construction): "
            f"{int((hc.H_ctl_max <= 0).sum())} of {len(hc)}")
    return kdf


# =====================================================================================
# PART L — the live ladders (idea 432's corpus, rebuilt so headroom has a null)
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


# ------------------------------------------------------------- KEEP paths ---
def bars(spy_r, which):
    m = metrics(window(spy_r, which))
    return dict(S=m["Sharpe"], CAGR=m["CAGR"], DD=m["MaxDD"])


def pass4b(r, spy_r, which="full"):
    rr = window(r, which)
    b = bars(spy_r, which)
    m = metrics(rr)
    h1, h2 = halves(rr)
    sb1, sb2 = halves(window(spy_r, which))
    mg = dict(H1=h1 - sb1, H2=h2 - sb2, S=m["Sharpe"] - b["S"],
              DD=DELTA * abs(b["DD"]) - abs(m["MaxDD"]), CAGR=m["CAGR"] - PHI * b["CAGR"])
    return bool(all(v > 0 for v in mg.values())), min(mg, key=lambda k: mg[k]), mg


def pass4a(r, base_r):
    h1, h2 = halves(r)
    b1, b2 = halves(base_r)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base_r)["MaxDD"])


# ------------------------------------------------------- the null for H ------
def null_headroom(R, ctl_idx, rng, block, n_boot=N_BOOT):
    """E[max - mean] and E[max - ctl] of pool Sharpes when every arm has the SAME true Sharpe.

    R is (T x A) daily returns over the window.  Each arm is shifted to the pool's mean Sharpe
    (vol, higher moments and the cross-arm correlation are untouched), then stationary blocks of
    length `block` are resampled JOINTLY across arms.  Returns (E_mean, E_ctl, p_mean, p_ctl)
    where p is the share of draws at least as extreme as the observed headroom."""
    T, A = R.shape
    mu, sd = R.mean(axis=0), R.std(axis=0, ddof=0)
    sd = np.where(sd > 0, sd, np.nan)
    S = mu / sd * math.sqrt(252.0)
    Sbar = np.nanmean(S)
    R0 = R - mu + (Sbar * sd / math.sqrt(252.0))          # equal-Sharpe null
    H_obs_mean = float(np.nanmax(S) - np.nanmean(S))
    H_obs_ctl = float(np.nanmax(S) - S[ctl_idx]) if ctl_idx is not None else np.nan
    nb = int(math.ceil(T / block))
    starts = rng.integers(0, T, size=(n_boot, nb))
    off = np.arange(block)
    idx = (starts[:, :, None] + off[None, None, :]).reshape(n_boot, nb * block)[:, :T] % T
    draws = R0[idx]                                        # (B, T, A)
    dmu, dsd = draws.mean(axis=1), draws.std(axis=1, ddof=0)
    dS = np.where(dsd > 0, dmu / np.where(dsd > 0, dsd, 1.0) * math.sqrt(252.0), np.nan)
    hm = np.nanmax(dS, axis=1) - np.nanmean(dS, axis=1)
    out = [float(np.nanmean(hm)), np.nan,
           float(np.nanmean(hm >= H_obs_mean)), np.nan]
    if ctl_idx is not None:
        hc = np.nanmax(dS, axis=1) - dS[:, ctl_idx]
        out[1] = float(np.nanmean(hc))
        out[3] = float(np.nanmean(hc >= H_obs_ctl))
    return tuple(out)


# ------------------------------------------------------------------ build ---
def build_live():
    rng = np.random.default_rng(SEED)
    cells, armrows, keeprows = [], [], []
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        say(f"\n[panel] {pk}: {px.shape[1]} cols {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}")

        Wg = ew_weights(px, GROSS, "band3")
        e1 = fast_backtest(px, Wg, 0.0, FREQ)
        e0 = backtest(px, Wg, cost_bps=0.0, freq=FREQ)
        d_r = float((e1["returns"] - e0["returns"]).abs().max())
        d_t = float((e1["turnover"] - e0["turnover"]).abs().max())
        e25 = backtest(px, Wg, cost_bps=25.0, freq=FREQ)
        d_c = float((e25["returns"] - (e0["returns"] - e0["turnover"] * 25.0 / 1e4)).abs().max())
        say(f"  [G1] fast vs engine: returns {d_r:.3e} turnover {d_t:.3e} | "
            f"[G5] rung identity {d_c:.3e}")
        assert d_r < 1e-12 and d_t < 1e-12 and d_c < 1e-12, "G1/G5 FAILED - unsafe"

        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}

        for fam in FAMILIES:
            arms = family_arms(fam)
            raw = {}
            for name, wf, fq, isctl in arms:
                res = fast_backtest(px, wf(px), 0.0, fq)
                raw[name] = (res["returns"].loc[start:], res["turnover"].loc[start:], isctl)
            for c in COSTS:
                names = [a[0] for a in arms]
                rets = {n: (raw[n][0] - raw[n][1] * c / 1e4) for n in names}
                ctl_i = next((i for i, n in enumerate(names) if raw[n][2]), None)
                for n in names:
                    r = rets[n]
                    ok4a = pass4a(r, v2[c])
                    ok4b, bar, _ = pass4b(r, spy, "full")
                    ok4b_o, bar_o, _ = pass4b(r, spy, "OOS")
                    m, mo = metrics(r), metrics(window(r, "OOS"))
                    h1, h2 = halves(r)
                    armrows.append(dict(panel=pk, family=fam, cost=c, arm=n,
                                        is_ctl=bool(raw[n][2]),
                                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                        H1=h1, H2=h2, IS_Sharpe=sharpe(window(r, "IS")),
                                        IS1_Sharpe=sharpe(window(r, "IS1")),
                                        IS2_Sharpe=sharpe(window(r, "IS2")),
                                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                        OOS_MaxDD=mo["MaxDD"],
                                        pass4a=ok4a, pass4b=ok4b, bar4b=bar,
                                        pass4b_oos=ok4b_o, bar4b_oos=bar_o))
                # ---- the headroom columns, both conventions, IS and OOS ----
                S_is = np.array([sharpe(window(rets[n], "IS")) for n in names])
                S_is1 = np.array([sharpe(window(rets[n], "IS1")) for n in names])
                S_is2 = np.array([sharpe(window(rets[n], "IS2")) for n in names])
                S_oos = np.array([sharpe(window(rets[n], "OOS")) for n in names])
                Rmat = np.column_stack([window(rets[n], "OOS").values for n in names])
                nulls = {}
                for L in BLOCK_LENS:
                    seed = SEED + zlib.crc32(f"{pk}|{fam}|{int(c)}|{L}".encode())  # never hash()
                    nulls[L] = null_headroom(Rmat, ctl_i,
                                             np.random.default_rng(seed), L)
                E_mean, E_ctl, p_mean, p_ctl = nulls[BLOCK_PRIMARY]
                pick_is = int(np.nanargmax(S_is))
                pick_is1 = int(np.nanargmax(S_is1))
                cells.append(dict(
                    panel=pk, family=fam, cost=c, n_arms=len(names),
                    ctl=names[ctl_i] if ctl_i is not None else "",
                    H_IS_mean=float(S_is.max() - S_is.mean()),
                    H_IS_ctl=float(S_is.max() - S_is[ctl_i]) if ctl_i is not None else np.nan,
                    H_IS1_mean=float(S_is1.max() - S_is1.mean()),
                    H_IS1_ctl=float(S_is1.max() - S_is1[ctl_i]) if ctl_i is not None else np.nan,
                    H_OOS_mean=float(S_oos.max() - S_oos.mean()),
                    H_OOS_ctl=float(S_oos.max() - S_oos[ctl_i]) if ctl_i is not None else np.nan,
                    H0_mean=E_mean, H0_ctl=E_ctl, p_mean=p_mean, p_ctl=p_ctl,
                    net_H_mean=float(S_oos.max() - S_oos.mean()) - E_mean,
                    net_H_ctl=(float(S_oos.max() - S_oos[ctl_i]) - E_ctl)
                    if ctl_i is not None else np.nan,
                    **{f"H0_mean_L{L}": nulls[L][0] for L in BLOCK_LENS},
                    **{f"p_mean_L{L}": nulls[L][2] for L in BLOCK_LENS},
                    pick_IS=names[pick_is], pick_IS1=names[pick_is1],
                    ctl_OOS=float(S_oos[ctl_i]) if ctl_i is not None else np.nan,
                    pick_OOS=float(S_oos[pick_is]),
                    pick_IS1_OOS=float(S_oos[pick_is1]),
                    pick_IS1_IS2=float(S_is2[pick_is1]),
                    ctl_IS2=float(S_is2[ctl_i]) if ctl_i is not None else np.nan,
                    oracle_OOS=float(S_oos.max()), pool_OOS=float(S_oos.mean()),
                    sel_gain=float(S_oos[pick_is] - S_oos[ctl_i]) if ctl_i is not None else np.nan,
                    pick_OOS_CAGR=float(metrics(window(rets[names[pick_is]], "OOS"))["CAGR"]),
                    pick_OOS_MaxDD=float(metrics(window(rets[names[pick_is]], "OOS"))["MaxDD"]),
                    ctl_OOS_CAGR=float(metrics(window(rets[names[ctl_i]], "OOS"))["CAGR"])
                    if ctl_i is not None else np.nan,
                    ctl_OOS_MaxDD=float(metrics(window(rets[names[ctl_i]], "OOS"))["MaxDD"])
                    if ctl_i is not None else np.nan,
                    v2_OOS=sharpe(window(v2[c], "OOS")), v1_OOS=sharpe(window(v1[c], "OOS")),
                    spy_OOS=sharpe(window(spy, "OOS")),
                    spy_OOS_CAGR=float(metrics(window(spy, "OOS"))["CAGR"]),
                    spy_OOS_MaxDD=float(metrics(window(spy, "OOS"))["MaxDD"]),
                ))
                # KEEP paths for the two rule-selected books (pick vs control)
                for lbl, nm in (("PICK_IS", names[pick_is]), ("CTL", names[ctl_i] if ctl_i
                                                              is not None else names[0])):
                    r = rets[nm]
                    ok4b, bar, _ = pass4b(r, spy, "full")
                    ok4b_o, _, _ = pass4b(r, spy, "OOS")
                    keeprows.append(dict(panel=pk, family=fam, cost=c, book=lbl, arm=nm,
                                         pass4a=pass4a(r, v2[c]), pass4b=ok4b,
                                         pass4b_oos=ok4b_o, bar4b=bar,
                                         both=bool(pass4a(r, v2[c]) and ok4b)))
    return pd.DataFrame(cells), pd.DataFrame(armrows), pd.DataFrame(keeprows)


# ------------------------------------------------------------- rule 8 -------
def rule8(cdf):
    """L3 — R(tau, s): pick the IS-argmax where IS headroom > tau, else the control.

    tau chosen on the INNER split (fit <= 2013, evaluate 2014-2016); OOS read ONCE."""
    say("\n[L3] RULE 8 — headroom-gated selection, tau on the inner IS split, "
        "2017-2026 read once")
    d = cdf[cdf.ctl != ""].copy()
    grids = {}
    for s in ("mean", "ctl"):
        h_in = d[f"H_IS1_{s}"].values
        taus = [0.0] + [float(np.nanquantile(h_in, q)) for q in np.arange(0.1, 1.0, 0.1)]
        taus = sorted(set(round(t, 6) for t in taus))
        rows = []
        for tau in taus:
            g = h_in > tau
            in_sel = np.where(g, d.pick_IS1_IS2.values, d.ctl_IS2.values)
            rows.append(dict(stat=s, tau=tau, n_gated=int(g.sum()),
                             IS2_mean=float(np.nanmean(in_sel)),
                             IS2_gain=float(np.nanmean(in_sel - d.ctl_IS2.values))))
        grids[s] = pd.DataFrame(rows)
        say(f"\n  inner-IS grid, statistic s={s} (ALL grid points, choice = argmax IS2_gain)")
        say(grids[s].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    allg = pd.concat(grids.values()).reset_index(drop=True)
    best = allg.loc[allg.IS2_gain.idxmax()]
    s_star, tau_star = best.stat, float(best.tau)
    say(f"\n  CHOSEN ON IS ONLY: s* = {s_star}, tau* = {tau_star:.4f} "
        f"(inner-IS gain {best.IS2_gain:+.4f}, {int(best.n_gated)} of {len(d)} pools gated on)")

    out = []
    for s in ("mean", "ctl"):
        h_out = d[f"H_IS_{s}"].values
        taus = sorted(set([0.0, tau_star] + [float(np.nanquantile(h_out, q))
                                             for q in np.arange(0.1, 1.0, 0.1)]))
        for tau in taus:
            g = h_out > tau
            sel = np.where(g, d.pick_OOS.values, d.ctl_OOS.values)
            gain = sel - d.ctl_OOS.values
            out.append(dict(stat=s, tau=round(tau, 6), chosen=bool(s == s_star and
                                                                   abs(tau - tau_star) < 1e-9),
                            n_gated=int(g.sum()), OOS_Sharpe=float(np.nanmean(sel)),
                            d_vs_donothing=float(np.nanmean(gain)), t=tstat(gain),
                            wins=int((gain > 0).sum()), losses=int((gain < 0).sum())))
    wf = pd.DataFrame(out)
    say("\n  OUTER OOS (2017-2026, read once) — ALL tau grid points reported")
    say(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    s0 = float(np.nanmean(d.ctl_OOS.values))
    s1 = float(np.nanmean(d.pick_OOS.values))
    orc = float(np.nanmean(d.oracle_OOS.values))
    ch = wf[wf.chosen]
    say(f"\n  S0 do-nothing (always the control)  OOS Sharpe {s0:.4f}")
    say(f"  S1 always the IS-argmax pick        OOS Sharpe {s1:.4f}   "
        f"d {s1 - s0:+.4f} (t {tstat(d.pick_OOS.values - d.ctl_OOS.values):+.2f}, "
        f"{int((d.pick_OOS.values > d.ctl_OOS.values).sum())}W/"
        f"{int((d.pick_OOS.values < d.ctl_OOS.values).sum())}L)")
    if len(ch):
        say(f"  R(tau*, s*) headroom-gated          OOS Sharpe {float(ch.OOS_Sharpe.iloc[0]):.4f}"
            f"   d {float(ch.d_vs_donothing.iloc[0]):+.4f} "
            f"(t {float(ch.t.iloc[0]):+.2f}, {int(ch.wins.iloc[0])}W/{int(ch.losses.iloc[0])}L)")
    say(f"  ORACLE-OOS (perfect hindsight)      OOS Sharpe {orc:.4f}   "
        f"d {orc - s0:+.4f}  <- the headroom the whole corpus has")
    say(f"  best single tau on the OOS grid (NOT selectable, reported for the ceiling): "
        f"{wf.d_vs_donothing.max():+.4f}")
    say(f"  comparands: RULES v2 OOS {d.v2_OOS.mean():.4f}, RULES v1 OOS {d.v1_OOS.mean():.4f}, "
        f"SPY OOS {d.spy_OOS.mean():.4f} "
        f"(SPY OOS CAGR {d.spy_OOS_CAGR.mean():.2%}, MaxDD {d.spy_OOS_MaxDD.mean():.2%})")
    say(f"  pick book OOS CAGR {d.pick_OOS_CAGR.mean():.2%} / MaxDD {d.pick_OOS_MaxDD.mean():.2%}"
        f" vs do-nothing {d.ctl_OOS_CAGR.mean():.2%} / {d.ctl_OOS_MaxDD.mean():.2%}")
    return wf, s_star, tau_star


def gate_e():
    """[e] REPRODUCE the two oracle gaps the queue quotes, from the record's own files."""
    say("\n[e] REPRODUCTION — the queue's premise, read off the committed record")
    want = [("idea 216 (flip-rate estimator, cloud)",
             OUT / "2026-09-08_a-flip-rate-estimator-that-is-not-confounded-by-block-count"
                   "_cloud.walkforward.csv", "arm", "OOS_Sharpe",
             "ORACLE_OOS", "S0_do_nothing", 0.0286),
            ("idea 203 (turnover-matched null, lane B)",
             OUT / "2026-09-08_a-turnover-matched-null-for-suppressing-overlays"
                   "_B.walkforward.csv", "arm", "OOS_Sharpe",
             "ORACLE-OOS", "S0 do-nothing", 0.0336)]
    got = {}
    for label, path, ac, yc, orc, s0, quoted in want:
        if not path.exists():
            say(f"    {label}: file missing — cannot reproduce, said so")
            continue
        d = pd.read_csv(path)
        g = d.groupby(ac)[yc].mean()
        gap = float(g[orc] - g[s0])
        got[label] = gap
        say(f"    {label}: ORACLE-OOS {g[orc]:.6f}, S0 {g[s0]:.6f}, gap {gap:+.6f} "
            f"vs published {quoted:+.4f}  |d| {abs(gap - quoted):.2e}")
    return got


def main():
    say(f"=== {STEM}")
    say("QUEUE idea 436 — ORACLE-OOS as the headroom column beside every selector kill")

    quoted = gate_e()
    fdf, pdf = census()
    kdf = kill_join(pdf)

    cdf, adf, kpdf = build_live()

    say(f"\n[L1] LIVE LADDERS — {len(cdf)} pools "
        f"({cdf.panel.nunique()} panels x {cdf.family.nunique()} families x "
        f"{cdf.cost.nunique()} cost rungs), {len(adf)} arm-rows")
    say("     RAW headroom is positive by construction; the question is whether it survives "
        "its own noise floor.")
    for s in ("mean", "ctl"):
        H = cdf[f"H_OOS_{s}"].values
        H0 = cdf[f"H0_{s}"].values
        net = cdf[f"net_H_{s}"].values
        p = cdf[f"p_{s}"].values
        say(f"     s={s:<5} H_OOS mean {np.nanmean(H):.4f} median {np.nanmedian(H):.4f} | "
            f"noise floor H0 mean {np.nanmean(H0):.4f} | NET mean {np.nanmean(net):+.4f} "
            f"(t {tstat(net):+.2f}) | pools with net H > 0: "
            f"{int(np.nansum(net > 0))}/{np.isfinite(net).sum()} | "
            f"pools clearing the null at p<0.05: {int(np.nansum(p < 0.05))}")
    say("     noise floor by POOL SIZE (so a 5-arm published ladder can be compared to one):")
    for n, sub in cdf.groupby("n_arms"):
        say(f"       n_arms={int(n)}  pools {len(sub):2d}  H0_mean {sub.H0_mean.mean():.4f}  "
            f"H0_ctl {sub.H0_ctl.mean():.4f}  observed H_OOS_ctl {sub.H_OOS_ctl.mean():.4f}")
    say("     block-length sensitivity of the noise floor (reported axis, never selected on):")
    for L in BLOCK_LENS:
        say(f"       L={L:<3} H0_mean {cdf[f'H0_mean_L{L}'].mean():.4f}   "
            f"pools clearing p<0.05: {int((cdf[f'p_mean_L{L}'] < 0.05).sum())} of {len(cdf)}")
    say("\n     per-family headroom (PROTOCOL rung 10 bps, pooled over panels):")
    t10 = cdf[cdf.cost == PROTOCOL_RUNG]
    say(t10.groupby("family")[["H_IS_mean", "H_OOS_mean", "H0_mean", "net_H_mean",
                               "p_mean", "sel_gain"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n[L2] IS THE COLUMN AVAILABLE AT DECISION TIME?")
    for s in ("mean", "ctl"):
        say(f"     s={s:<5} corr(H_IS, H_OOS) {corr(cdf[f'H_OOS_{s}'], cdf[f'H_IS_{s}']):+.4f}"
            f"  spearman {spearman(cdf[f'H_OOS_{s}'], cdf[f'H_IS_{s}']):+.4f}"
            f"  | corr(H_IS, selector gain) {corr(cdf.sel_gain, cdf[f'H_IS_{s}']):+.4f}"
            f"  | corr(H_OOS, selector gain) {corr(cdf.sel_gain, cdf[f'H_OOS_{s}']):+.4f}")
    q = cdf.dropna(subset=["sel_gain"]).copy()
    q["terc"] = pd.qcut(q.H_IS_mean, 3, labels=["low", "mid", "high"])
    say("     selector gain by IS-headroom tercile:")
    say(q.groupby("terc", observed=True)
        .agg(n=("sel_gain", "size"), mean_gain=("sel_gain", "mean"),
             t=("sel_gain", lambda v: tstat(v)), H_OOS=("H_OOS_mean", "mean"),
             net_H=("net_H_mean", "mean")).to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"     sign test on the selector gain over all {len(q)} pools: "
        f"{int((q.sel_gain > 0).sum())}W/{int((q.sel_gain < 0).sum())}L, "
        f"p {sign_p(int((q.sel_gain > 0).sum()), int((q.sel_gain != 0).sum())):.4f}, "
        f"mean {q.sel_gain.mean():+.4f} (t {tstat(q.sel_gain):+.2f})")

    wf, s_star, tau_star = rule8(cdf)

    say("\n[L4] BOTH KEEP PATHS")
    say(f"     arms ({len(adf)} rows): 4a {int(adf.pass4a.sum())}, 4b full "
        f"{int(adf.pass4b.sum())}, 4b OOS {int(adf.pass4b_oos.sum())}, "
        f"BOTH (4a and 4b full) {int((adf.pass4a & adf.pass4b).sum())}")
    say("     4b binding bar census (full sample): "
        + ", ".join(f"{k} {v}" for k, v in adf[~adf.pass4b].bar4b.value_counts().items()))
    say(f"     rule-selected books ({len(kpdf)} rows): 4a {int(kpdf.pass4a.sum())}, "
        f"4b {int(kpdf.pass4b.sum())}, 4b OOS {int(kpdf.pass4b_oos.sum())}, "
        f"BOTH {int(kpdf.both.sum())}")
    say(kpdf.groupby("book")[["pass4a", "pass4b", "pass4b_oos", "both"]].sum()
        .to_string())
    if int(adf.pass4a.sum()):
        say("     4a passes by family: "
            + ", ".join(f"{k} {v}" for k, v in adf[adf.pass4a].family.value_counts().items()))
    if int(adf.pass4b.sum()):
        say("     4b passes by panel: "
            + ", ".join(f"{k} {v}" for k, v in adf[adf.pass4b].panel.value_counts().items()))

    say("\n[VERDICT / RECOMMENDATION]")
    net_pos = int((cdf.net_H_mean > 0).sum())
    clear = int((cdf.p_mean < 0.05).sum())
    say(f"  1. ORACLE-OOS is publishable but must NEVER be published raw: over the 63 live "
        f"pools the raw gap averages {cdf.H_OOS_mean.mean():.4f} of Sharpe while its own "
        f"equal-Sharpe noise floor is {cdf.H0_mean.mean():.4f}; net headroom is "
        f"{cdf.net_H_mean.mean():+.4f} and only {clear} of {len(cdf)} pools clear the null "
        f"at p<0.05 ({net_pos} are net-positive at all).")
    say(f"  2. The column is NOT a screen: corr(H_IS, H_OOS) = "
        f"{corr(cdf.H_OOS_mean, cdf.H_IS_mean):+.4f}, so headroom is not knowable at decision "
        f"time, and R(tau*) is priced under rule 8 above.")
    if quoted:
        lo = cdf.H0_ctl.min()
        hi = cdf.H0_ctl.max()
        say(f"  3. THE QUEUE'S OWN TWO NUMBERS, re-read: idea 216's "
            f"+{quoted.get('idea 216 (flip-rate estimator, cloud)', float('nan')):.4f} and "
            f"idea 203's +{quoted.get('idea 203 (turnover-matched null, lane B)', float('nan')):.4f} "
            f"of ORACLE-OOS are reproduced here EXACTLY from their own committed files "
            f"(gate [e]) and are UNINTERPRETABLE as published, because a max-minus-control "
            f"gap has no meaning without its own noise floor and the floor is not a constant: "
            f"across the 63 live pools it runs {lo:.4f} (near-identical arms - the GROSS dial) "
            f"to {hi:.4f} (dissimilar arms - GATE/WIDTH), i.e. a {hi / lo:.0f}x span at the SAME "
            f"pool size and window. Their clause-gated arms are near-identical books, so their "
            f"floor plausibly sits at the low end and +0.0286 may well be real headroom - but "
            f"NOTHING in the committed record settles it, because the arm return series were "
            f"not committed. So idea 216's sentence 'unlike idea 434's family there IS "
            f"headroom' is UNSUPPORTED rather than wrong, and it is unsupportable from what "
            f"the record kept. This run does NOT re-price their ladders and does not claim to.")
    say(f"  4. The queue's '12 selector kills' is an ORDINAL, not a set — see [C2].")
    say(f"  5. Recommended LEADERBOARD wording for any future selector kill: "
        f"'ORACLE-OOS +X (noise floor +Y, net +Z, p=P over B draws)' — the floor computed on "
        f"the ladder's OWN arms, never quoted from another run. And the enabling change: a "
        f"run that publishes a selector verdict should commit its ARM-level OOS series (or at "
        f"minimum arm x OOS metric rows), because {int((fdf.tier == 'T3').sum())} committed "
        f"files carry an OOS Sharpe that cannot be pooled at all and only "
        f"{int((fdf.tier == 'T1').sum())} publish an oracle column. Report-only; "
        f"PROTOCOL, RULES.md, scan.py, bot.py and baseline.py untouched.")

    fdf.to_csv(OUT / f"{STEM}.census.csv", index=False)
    kdf.to_csv(OUT / f"{STEM}.kills.csv", index=False)
    cdf.to_csv(OUT / f"{STEM}.cells.csv", index=False)
    adf.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    kpdf.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.[census|kills|cells|arms|walkforward|keeppaths].csv and .console.txt")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
