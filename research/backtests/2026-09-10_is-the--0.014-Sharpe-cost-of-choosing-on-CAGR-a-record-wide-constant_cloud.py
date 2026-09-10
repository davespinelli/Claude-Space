#!/usr/bin/env python3
"""Idea 493 (cloud, 2026-09-10) -- is the -0.014 Sharpe cost of choosing on CAGR a
record-wide CONSTANT?

Idea 270 (lane B) reported the DENOMINATOR of the S_CAGR / S_SHARPE exchange rate --
dOOS_Sharpe = OOS Sharpe of the arm picked by IS CAGR minus OOS Sharpe of the arm picked by IS
Sharpe -- as homogeneous across five dials at about -0.014 (blocked permutation p 0.3081),
while the NUMERATOR (dOOS CAGR) was emphatically not (p 0.0001).  Its own record census gave
-0.0162 file-clustered over 73 files and could not resolve dial-specificity (p 0.3114 clustered
vs p < 0.0001 menu-pooled).  What neither leg controlled for is MENU LENGTH: a menu with more
arms gives the two selectors more room to disagree AND a wider OOS Sharpe range to disagree
over, and the dials differ in how long their ladders are.  If -0.014 is a menu-length statistic
wearing a dial's name, it is not quotable anywhere.

This run tests the denominator directly on the record's 6,956 COMMITTED menus, file-clustered,
with the dial family and the arm count as the only covariates -- exactly the queue's ask.

Pre-registration (fixed before any number was read):

  * TWO tuned parameters and no more:
      FAMSET  -- FULL5 (idea 270's committed families: n | trim | gross | cadence | other)
               | POOLED3 (SIZE = n+trim, MONO = gross+cadence, OTHER -- idea 270-B2's
                 mechanism: Sharpe and CAGR are co-monotone along gross and cadence)
               | BINARY (n vs everything else)
      ARMSCTL -- NONE | Q4 (arm-count quartiles of the pooled population)
               | FIXED4 (3 | 4-5 | 6-9 | >=10) | LOG (residualise dS on log2(arms) first)
    All 3 x 4 = 12 grid points reported.  Nothing else is chosen: the population, the family
    map, the metric and the 20,000-draw permutation seed are idea 270's, unchanged.

  * POPULATION.  `2026-09-09_..._B.census.csv` as committed: 6,956 menus over 73 files.  That
    file IS the object the queue names, so it is the headline; a FRESH re-scan of today's
    corpus with idea 270's own `census()` code is run as a reported robustness leg, never as
    the headline (the corpus has grown since 2026-09-09).

  * THE TESTS, at every grid point:
      (1) POOLED  -- file-clustered mean of dS (mean of per-file means, files equally weighted)
                     with a 2,000-draw cluster bootstrap 95% CI (seed 493).  The constant is
                     QUOTABLE at that point iff -0.014 lies inside the CI.
      (2) HETEROGENEITY -- spread (max - min) of the per-family means of the BLOCK-DEMEANED dS,
                     with two nulls, 20,000 draws each:
                       UNRESTRICTED  family labels shuffled freely (idea 270's leg-B test);
                       BLOCKED       family labels shuffled WITHIN (file x arms bucket), the
                                     exact null for "family adds nothing once the arm count and
                                     the file are held fixed".  Files carrying one family
                                     contribute nothing to the blocked test, correctly: they
                                     hold no within-file family information.
      (3) ARMS -- mean dS by arm-count bucket and the file-clustered slope of dS on log2(arms).

  * PART C -- THE LIVE LEG (PROTOCOL 4 + 8).  The same two covariates, controlled: five dial
    families, each a 12-rung ladder on three panels, sub-sampled to menus of L in {3,4,6,8,12}
    arms by taking L EVENLY SPACED rungs INCLUDING BOTH ENDPOINTS, so the ladder's EXTENT is
    held fixed and only its RESOLUTION (the arm count) moves.  RULE 8: inside each menu both
    selectors choose on 2009-2016 IS only and 2017-01-01.. is read ONCE.  Both KEEP paths are
    evaluated on every underlying arm at both cost rungs.

SURVIVORSHIP (idea 54, carried): B136 and SMALL439 are CURRENT-constituent screens, so their
LEVELS are biased upward; both selectors read the same panel, so the bias is common to the pair
and cannot manufacture a DIFFERENCE between them, but it does inflate every OOS level below.
SMALL439 drops the 44 sub-$2B names with max_1d_move >= 1.0 from data/small_meta.csv first, and
SPY there is a benchmark column, never selectable.  U56 is a fixed ETF/mega-cap list.

Costs 10/25 bps per unit turnover; weights decided at close t applied at t+1 (PROTOCOL 2).
Deterministic (seed 493), no network.  Writes .menus.csv .grid.csv .arms.csv .fresh.csv
.live.csv .livemenus.csv .keeppaths.csv .console.txt
"""
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state, score  # noqa
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

CENSUS = OUT / "2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B.census.csv"
QUOTED = -0.014                       # the number under test
N_PERM = 20000
N_BOOT = 2000
SEED = 493
FAMSETS = ["FULL5", "POOLED3", "BINARY"]
ARMSCTLS = ["NONE", "Q4", "FIXED4", "LOG"]

# ---- live leg ------------------------------------------------------------------------------
FREQ = "W"
GROSS = 0.75
BAND = 0.03
MAX_VOL = 0.60
RUNGS = [10.0, 25.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
LS = [3, 4, 6, 8, 12]
PANELS = ["U56", "B136", "SMALL439"]
NLADDER = [3, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50, 60]
GLADDER = [0.30, 0.36, 0.42, 0.49, 0.55, 0.62, 0.68, 0.75, 0.81, 0.88, 0.94, 1.00]
CLADDER = [1, 2, 3, 5, 10, 15, 21, 42, 63, 126, 189, 252]          # rebalance every k days
VLADDER = [0.20, 0.27, 0.34, 0.42, 0.49, 0.56, 0.64, 0.71, 0.78, 0.85, 0.93, 1.00]
TLADDER = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11]
LADDERS = {"n": NLADDER, "gross": GLADDER, "cadence": CLADDER,
           "volgate": VLADDER, "trim": TLADDER}

LINES = []


def P(s=""):
    print(s)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# families / buckets
# ================================================================================================
POOL3 = {"n": "SIZE", "trim": "SIZE", "gross": "MONO", "cadence": "MONO",
         "volgate": "MONO", "other": "OTHER"}


def famcol(d, famset):
    if famset == "FULL5":
        return d.family.astype(str)
    if famset == "POOLED3":
        return d.family.map(lambda x: POOL3.get(x, "OTHER"))
    return d.family.map(lambda x: "n" if x == "n" else "rest")


def bucketcol(d, ctl):
    a = d.arms.astype(float)
    if ctl in ("NONE", "LOG"):
        return pd.Series("ALL", index=d.index)
    if ctl == "Q4":
        try:
            return pd.qcut(a, 4, duplicates="drop").astype(str)
        except Exception:
            return pd.Series("ALL", index=d.index)
    return pd.cut(a, [0, 3, 5, 9, 10 ** 9], labels=["3", "4-5", "6-9", ">=10"]).astype(str)


# ================================================================================================
# statistics
# ================================================================================================
def file_clustered(d, col="dOOS_Sharpe"):
    """Mean of per-file means (files equally weighted) + t on the file-level dispersion."""
    per = d.groupby("file")[col].mean()
    m = float(per.mean())
    t = float(m / (per.std(ddof=1) / np.sqrt(len(per)))) if len(per) > 1 and per.std(ddof=1) else np.nan
    return m, t, len(per), int((per < 0).sum())


def cluster_boot_ci(d, col="dOOS_Sharpe", n=N_BOOT, seed=SEED):
    """Resample FILES with replacement; statistic = mean of the resampled per-file means."""
    per = d.groupby("file")[col].mean().to_numpy(float)
    k = len(per)
    rng = np.random.default_rng(seed)
    stats = per[rng.integers(0, k, (n, k))].mean(axis=1)
    return float(np.quantile(stats, 0.025)), float(np.quantile(stats, 0.975)), k


def demean_blocks(d, blockcols, col="dOOS_Sharpe"):
    v = d[col].to_numpy(float)
    if not blockcols:
        return v - v.mean()
    key = d[blockcols].astype(str).agg("|".join, axis=1)
    return v - key.map(d.assign(_v=v).groupby(key)["_v"].mean()).to_numpy(float)


def spread_of_means(vals, codes, k):
    cnt = np.bincount(codes, minlength=k).astype(float)
    cnt[cnt == 0] = np.nan
    m = np.bincount(codes, weights=vals, minlength=k) / cnt
    m = m[~np.isnan(m)]
    return float(m.max() - m.min()) if len(m) > 1 else np.nan


def perm_free(vals, codes, k, n=N_PERM, seed=SEED):
    obs = spread_of_means(vals, codes, k)
    if not np.isfinite(obs):
        return obs, np.nan
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n):
        if spread_of_means(rng.permutation(vals), codes, k) >= obs:
            hits += 1
    return obs, (hits + 1) / (n + 1)


def perm_blocked(vals, codes, k, blocks, n=N_PERM, seed=SEED):
    """Family labels shuffled WITHIN each block (vectorised via a per-draw lexsort).

    Blocks carrying one family contribute no variation -- correctly, they hold no within-block
    family information; `informative` reports how many rows sit in blocks that do."""
    obs = spread_of_means(vals, codes, k)
    if not np.isfinite(obs):
        return obs, np.nan, 0
    b = pd.factorize(pd.Series(blocks))[0]
    informative = 0
    for u in np.unique(b):
        i = np.where(b == u)[0]
        if len(np.unique(codes[i])) > 1:
            informative += len(i)
    if informative == 0:
        return obs, np.nan, 0
    order0 = np.argsort(b, kind="stable")
    rng = np.random.default_rng(seed)
    m = len(codes)
    hits = 0
    for _ in range(n):
        perm = np.lexsort((rng.random(m), b))          # rows grouped by block, random within
        c = np.empty(m, dtype=codes.dtype)
        c[order0] = codes[perm]
        if spread_of_means(vals, c, k) >= obs:
            hits += 1
    return obs, (hits + 1) / (n + 1), informative


def clustered_slope(d, x="arms", y="dOOS_Sharpe"):
    """Slope of y on log2(x), file-clustered: mean of per-file slopes, t on their dispersion."""
    sl = []
    for f, g in d.groupby("file"):
        lx = np.log2(g[x].to_numpy(float))
        if len(g) < 3 or lx.std() == 0:
            continue
        sl.append(np.polyfit(lx, g[y].to_numpy(float), 1)[0])
    if len(sl) < 2:
        return np.nan, np.nan, len(sl)
    sl = np.array(sl)
    return float(sl.mean()), float(sl.mean() / (sl.std(ddof=1) / np.sqrt(len(sl)))), len(sl)


# ================================================================================================
# PART A/B -- the record's menus
# ================================================================================================
def part_ab():
    P()
    P("=" * 100)
    P("(A) POPULATION -- idea 270's committed census, exactly as the queue names it")
    P("=" * 100)
    d = pd.read_csv(CENSUS)
    d["arms"] = pd.to_numeric(d["arms"], errors="coerce")
    d = d.dropna(subset=["arms", "dOOS_Sharpe"])
    P(f"  {CENSUS.name}")
    P(f"  menus {len(d):,}   files {d.file.nunique()}   families {sorted(d.family.unique())}")
    P(f"  G1 population matches idea 270's published 6,956 menus / 73 files : "
      f"{'PASS' if len(d) == 6956 and d.file.nunique() == 73 else 'FAIL'}")
    m, t, nf, neg = file_clustered(d)
    P(f"  G2 file-clustered pooled dOOS_Sharpe reproduces its published -0.0162 (t -3.07, "
      f"36/73 negative): {m:+.4f} (t {t:+.2f}, {neg}/{nf} negative)  -> "
      f"{'PASS' if abs(m + 0.0162) < 5e-4 and neg == 36 else 'FAIL'}")
    P(f"  G3 menu-pooled dOOS_Sharpe reproduces its published -0.0116 : "
      f"{d.dOOS_Sharpe.mean():+.4f}  -> "
      f"{'PASS' if abs(d.dOOS_Sharpe.mean() + 0.0116) < 5e-4 else 'FAIL'}")
    P()
    P("  arm-count distribution of the population:")
    P("    " + d.arms.describe().to_string().replace("\n", "\n    "))
    P("  arms by family (median / mean / n):")
    for f, g in d.groupby("family"):
        P(f"    {f:8s} median {g.arms.median():5.1f}  mean {g.arms.mean():6.2f}  n {len(g):5d}  "
          f"disagree {1 - g.same.mean():.3f}")

    P()
    P("=" * 100)
    P("(B) THE 3 x 4 GRID -- every point reported (FAMSET x ARMS control)")
    P("=" * 100)
    rows = []
    for famset in FAMSETS:
        for ctl in ARMSCTLS:
            e = d.copy()
            e["fam"] = famcol(e, famset)
            e["buck"] = bucketcol(e, ctl)
            if ctl == "LOG":
                # residualise dS on log2(arms) pooled, then run the family test on residuals
                lx = np.log2(e.arms.to_numpy(float))
                b1, b0 = np.polyfit(lx, e.dOOS_Sharpe.to_numpy(float), 1)
                e["work"] = e.dOOS_Sharpe - (b0 + b1 * lx)
                logslope = b1
            else:
                e["work"] = e.dOOS_Sharpe
                logslope = np.nan
            m, t, nf, neg = file_clustered(e)
            lo, hi, _ = cluster_boot_ci(e)
            blocks_free = []
            blocks_blk = ["file"] + ([] if ctl in ("NONE", "LOG") else ["buck"])
            vals = demean_blocks(e, blocks_blk, "work")
            codes, uniq = pd.factorize(e.fam)
            k = len(uniq)
            obs_f, p_f = perm_free(demean_blocks(e, blocks_free, "work"), codes, k)
            bkey = e[blocks_blk].astype(str).agg("|".join, axis=1).to_numpy()
            obs_b, p_b, info = perm_blocked(vals, codes, k, bkey)
            fam_means = {u: float(e.loc[codes == i, "work"].mean()) for i, u in enumerate(uniq)}
            rows.append(dict(famset=famset, armsctl=ctl, menus=len(e), files=nf,
                             pooled_dS=m, t=t, ci_lo=lo, ci_hi=hi,
                             quotable=bool(lo <= QUOTED <= hi),
                             neg_files=neg, k_fam=k,
                             spread_free=obs_f, p_free=p_f,
                             spread_blocked=obs_b, p_blocked=p_b, informative_rows=info,
                             log2arms_slope=logslope,
                             fam_means="; ".join(f"{u}={fam_means[u]:+.4f}" for u in uniq)))
    G = pd.DataFrame(rows)
    P(G[["famset", "armsctl", "menus", "files", "pooled_dS", "t", "ci_lo", "ci_hi", "quotable",
         "k_fam", "spread_free", "p_free", "spread_blocked", "p_blocked",
         "informative_rows"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    for _, r in G.iterrows():
        P(f"    {r.famset:8s} {r.armsctl:6s}  {r.fam_means}")

    P()
    P("=" * 100)
    P("(C) THE ARM COUNT ITSELF")
    P("=" * 100)
    arows = []
    for ctl in ("Q4", "FIXED4"):
        e = d.copy(); e["buck"] = bucketcol(e, ctl)
        for b, g in e.groupby("buck"):
            m, t, nf, neg = file_clustered(g)
            arows.append(dict(scheme=ctl, bucket=str(b), menus=len(g), files=nf,
                              pooled_dS=m, t=t, menu_mean=float(g.dOOS_Sharpe.mean()),
                              disagree=float(1 - g.same.mean()),
                              med_arms=float(g.arms.median())))
    A = pd.DataFrame(arows).sort_values(["scheme", "med_arms"])
    P(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    sl, st, nsl = clustered_slope(d)
    P(f"\n  file-clustered slope of dOOS_Sharpe on log2(arms): {sl:+.5f} per doubling "
      f"(t {st:+.2f}, {nsl} files)")
    slp = np.polyfit(np.log2(d.arms.to_numpy(float)), d.dOOS_Sharpe.to_numpy(float), 1)[0]
    P(f"  menu-pooled slope (no clustering)                 : {slp:+.5f} per doubling")
    return d, G, A


def _census_guarded(mod):
    """Idea 270's census(), one line changed: duplicate normalised columns are dropped
    (first kept) before `pd.to_numeric`.  Everything else -- the guards, the dial map, the
    barred axes, the menu construction -- is `mod`'s own code, called by reference."""
    files = sorted(OUT.glob("*.csv")) + sorted(OUT.glob("*.csv.gz"))
    files = [f for f in files if not f.name.startswith((mod.STEM, STEM))]
    menus, nfiles, unread, big, guarded = [], 0, 0, 0, []
    for f in files:
        try:
            df = pd.read_csv(f)
        except Exception:
            unread += 1
            continue
        if len(df) > mod.MAX_ROWS:
            big += 1
            continue
        norm = pd.Index([c.lower().replace(" ", "") for c in df.columns])
        if norm.duplicated().any():
            keep = ~norm.duplicated()
            if set(mod.METRIC_KEYS).issubset(set(norm)):
                guarded.append(f.name)
            df = df.loc[:, keep]
        low = {c.lower().replace(" ", ""): c for c in df.columns}
        if not all(k in low for k in mod.METRIC_KEYS):
            continue
        df = df.rename(columns={low[k]: v for k, v in mod.METRIC_KEYS.items()})
        for v in mod.METRIC_KEYS.values():
            df[v] = pd.to_numeric(df[v], errors="coerce")
        df = df.dropna(subset=list(mod.METRIC_KEYS.values()))
        if len(df) < 3:
            continue
        labels = [c for c in df.columns
                  if c not in mod.METRIC_KEYS.values()
                  and c.lower().replace(" ", "") not in mod.NON_DIAL
                  and not c.lower().startswith(("is_", "oos_", "spy_", "v1_", "v2_"))
                  and 1 < df[c].nunique(dropna=False) <= mod.MAX_LEVELS]
        used = False
        cands = [c for c in labels
                 if df[c].nunique(dropna=False) >= 3 and not mod.barred_dial(c)][:mod.MAX_DIALS]
        for d in cands:
            others = [c for c in labels if c != d]
            try:
                grp = df.groupby(others, dropna=False) if others else [((), df)]
                if others and grp.ngroups > mod.MAX_MENUS:
                    continue
            except Exception:
                continue
            for key, g in grp:
                g = g.dropna(subset=[d])
                if g[d].nunique() < 3 or len(g) < 3:
                    continue
                s = g.loc[g.IS_Sharpe.idxmax()]
                c = g.loc[g.IS_CAGR.idxmax()]
                dS = float(c.OOS_Sharpe - s.OOS_Sharpe)
                dC = float(c.OOS_CAGR - s.OOS_CAGR)
                dC_pp = dC * 100.0 if g.OOS_CAGR.abs().max() < 2.0 else dC
                menus.append(dict(file=f.name, dial_col=d, family=mod.dial_family(d),
                                  arms=len(g), same=bool(s.name == c.name),
                                  dOOS_Sharpe=dS, dOOS_CAGR_pp=dC_pp,
                                  xr=(np.nan if (s.name == c.name or dS >= 0) else dC_pp / (-dS)),
                                  key=str(key)))
                used = True
        nfiles += used
    P(f"  duplicate-column guard fired on {len(guarded)} qualifying file(s): {guarded}")
    return pd.DataFrame(menus), len(files), nfiles, unread, big


def fresh_scan():
    """Idea 270's census() re-run on TODAY's corpus.

    Its code is imported and called; if it raises, the ONE documented deviation below is used
    instead -- a duplicate-column guard.  Idea 270's `census()` does
    `df[v] = pd.to_numeric(df[v])` after renaming, which raises the moment a file carries two
    columns that normalise to the same metric name.  Exactly one committed CSV does
    (`2026-09-09_is-the-4b-footprint-a-monotone-function-of-cap-mix_B.grid.csv`, two `oos_cagr`
    columns), and it landed after idea 270 ran -- so idea 270's leg-B census no longer executes
    on the record it censused.  That is reported as a finding, not patched away: the guard keeps
    the FIRST such column and changes nothing else."""
    P()
    P("=" * 100)
    P("(D) ROBUSTNESS -- the same statistic on a FRESH scan of today's corpus (reported, not the headline)")
    P("=" * 100)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ideab270", OUT / "2026-09-09_is-S_CAGR-vs-S_SHARPE-a-general-selector-pair_B.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    t0 = time.time()
    try:
        d2, nfiles, used, unread, big = mod.census()
        P("  idea 270's census() ran unmodified on today's corpus")
    except Exception as e:
        P(f"  idea 270's census() RAISES on today's corpus: {type(e).__name__}: {e}")
        P("  -> re-running it with the documented duplicate-column guard (first column kept)")
        d2, nfiles, used, unread, big = _census_guarded(mod)
    P(f"  scan time {time.time() - t0:.1f}s   csvs {nfiles}  contributing {used}  "
      f"unreadable {unread}  skipped>200k {big}")
    if d2.empty:
        return d2
    d2["arms"] = pd.to_numeric(d2["arms"], errors="coerce")
    d2 = d2.dropna(subset=["arms", "dOOS_Sharpe"])
    m, t, nf, neg = file_clustered(d2)
    lo, hi, _ = cluster_boot_ci(d2)
    sl, st, _ = clustered_slope(d2)
    P(f"  menus {len(d2):,} over {nf} files (was 6,956 / 73)")
    P(f"  file-clustered pooled dOOS_Sharpe {m:+.4f} (t {t:+.2f}, {neg}/{nf} negative)  "
      f"95% CI [{lo:+.4f}, {hi:+.4f}]  contains -0.014: {lo <= QUOTED <= hi}")
    P(f"  file-clustered slope on log2(arms) {sl:+.5f} (t {st:+.2f})")
    return d2


# ================================================================================================
# PART C -- LIVE LEG
# ================================================================================================
def fast_backtest(px, weights, mask=None, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    W = weights.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    if mask is None:
        mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values.copy()
    else:
        mask = pd.Series(mask, index=px.index).shift(1, fill_value=False).values.copy()
    mask[0] = True
    n = len(px)
    A = np.cumprod(1.0 + rets, axis=0)
    A = np.vstack([np.ones((1, rets.shape[1])), A[:-1]])
    port = np.zeros(n); turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    starts = np.flatnonzero(mask)
    for i0, i1 in zip(starts, list(starts[1:]) + [n]):
        w = W[i0]
        turn[i0] = np.abs(w - cur).sum()
        u = w[None, :] * (A[i0:i1] / A[i0][None, :])
        T = u.sum(axis=1) + (1.0 - w.sum())
        port[i0:i1] = (u * rets[i0:i1]).sum(axis=1) / T
        cur = (u[-1] * (1.0 + rets[i1 - 1])) / (T[-1] * (1.0 + port[i1 - 1]))
    return {"returns0": pd.Series(port, index=px.index),
            "turnover": pd.Series(turn, index=px.index)}


def net(res, bps):
    return res["returns0"] - res["turnover"] * bps / 1e4


def mstats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def ew(px, adm, gross):
    """RULES v2's own construction (baseline.rules_v2_weights): gross/N of NAV on every
    ADMITTED name, N = instruments PRICED that day, gated-out weight -> CASH, never re-spread.
    Gates G6/G7 assert this reproduces the live book at its own rungs."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    w = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.where(adm, 0.0)


def arm_weights(px, dial, v, drop=()):
    """One rung of one dial family.  Every dial is a RULES-v2-form band/EW book except `n`,
    which is the top-n momentum book; the OTHER dials sit at their live defaults."""
    cols = [c for c in px.columns if c not in drop]
    p = px[cols]
    if dial == "n":
        s, _, _ = score(p, vol_scale=False)
        r = s.rank(axis=1, ascending=False, method="first")
        w = (r <= v).astype(float) * (GROSS / v)
    elif dial == "gross":
        w = ew(p, band_state(p, BAND) & p.notna(), v)
    elif dial == "trim":
        w = ew(p, band_state(p, v) & p.notna(), GROSS)
    elif dial == "volgate":
        vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
        w = ew(p, band_state(p, BAND) & p.notna() & (vol20 < v), GROSS)
    elif dial == "cadence":
        w = ew(p, band_state(p, BAND) & p.notna(), GROSS)
    else:
        raise ValueError(dial)
    return w.reindex(columns=px.columns).fillna(0.0)


def sub_ladder(ladder, L):
    """L evenly spaced rungs INCLUDING both endpoints -- extent fixed, resolution varies."""
    ix = np.unique(np.round(np.linspace(0, len(ladder) - 1, L)).astype(int))
    return [ladder[i] for i in ix]


def panels():
    out = {}
    out["U56"] = (load_universe(), ())
    out["B136"] = (load_universe(broad=True), ())
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    out["SMALL439"] = (sm[[c for c in sm.columns if c not in bad]], ("SPY",))
    for k, (p, dr) in out.items():
        P(f"  {k:9s} {p.shape[1]:4d} cols  {p.index[0].date()} -> {p.index[-1].date()}  "
          f"({len(p)} rows)  non-selectable: {dr or '-'}")
    return out


def gates(PX):
    P()
    P("=" * 100)
    P("GATES (run before any new number is read)")
    P("=" * 100)
    px = PX["U56"][0]
    w = rules_v2_weights(px)
    st = px.index[260]
    a = engine_backtest(px, w, cost_bps=0.0, freq=FREQ)["returns"]
    g1 = float(np.nanmax(np.abs((a - fast_backtest(px, w)["returns0"]).loc[st:])))
    P(f"  G4 fast_backtest == engine.backtest (RULES v2, 0 bps, from warm-up)   : {g1:.3e}")
    a25 = engine_backtest(px, w, cost_bps=25.0, freq=FREQ)["returns"].loc[st:]
    g2 = float(np.nanmax(np.abs(a25 - net(fast_backtest(px, w), 25.0).loc[st:])))
    P(f"  G5 cost-rung identity vs a live engine.backtest(25)                   : {g2:.3e}")
    # the gross dial at 0.75 IS the live book
    g3 = float(np.abs(arm_weights(px, "gross", 0.75) - rules_v2_weights(px)).max().max())
    P(f"  G6 gross-dial rung 0.75 IS baseline.rules_v2_weights                  : {g3:.3e}")
    g4 = float(np.abs(arm_weights(px, "trim", BAND) - rules_v2_weights(px)).max().max())
    P(f"  G7 trim-dial rung 0.03 IS baseline.rules_v2_weights                   : {g4:.3e}")
    # cadence mask sanity: k=1 is daily, k=252 rebalances ~ once a year
    m1 = pd.Series(np.arange(len(px)) % 1 == 0, index=px.index).sum()
    m252 = pd.Series(np.arange(len(px)) % 252 == 0, index=px.index).sum()
    P(f"  G8 cadence mask k=1 -> {m1} rebalances, k=252 -> {m252}                  : "
      f"{'PASS' if m1 == len(px) and m252 == int(np.ceil(len(px) / 252)) else 'FAIL'}")
    return dict(G4=g1, G5=g2, G6=g3, G7=g4)


def pass4a(d, b):
    return bool(d["H1"] > b["H1"] and d["H2"] > b["H2"] and d["MaxDD"] >= b["MaxDD"])


def pass4b(d, spy, oos_sh, spy_oos_sh):
    return bool(d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and oos_sh > spy_oos_sh
                and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])


def live(PX):
    P()
    P("=" * 100)
    P("(E) LIVE LEG -- the denominator measured under a CONTROLLED arm count")
    P("=" * 100)
    arms, t0 = [], time.time()
    for pname in PANELS:
        px, drop = PX[pname]
        st = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[st:]
        spy = mstats(spy_r); spy_oos = metrics(spy_r.loc[OOS_START:])
        base = fast_backtest(px, rules_v2_weights(px))
        BAS, BOOS = {}, {}
        for rung in RUNGS:
            BAS[rung] = mstats(net(base, rung).loc[st:])
            BOOS[rung] = metrics(net(base, rung).loc[OOS_START:])["Sharpe"]
            b = BAS[rung]
            P(f"  {pname} @{int(rung)}bps  SPY {spy['CAGR']:.2%}/{spy['Sharpe']:.4f}/"
              f"{spy['MaxDD']:.2%} (OOS Sh {spy_oos['Sharpe']:.4f})   RULES v2 "
              f"{b['CAGR']:.2%}/{b['Sharpe']:.4f}/{b['MaxDD']:.2%} (OOS Sh {BOOS[rung]:.4f})")
        for dial, ladder in LADDERS.items():
            for v in ladder:
                w = arm_weights(px, dial, v, drop=drop)
                mask = None
                if dial == "cadence":
                    mask = pd.Series(np.arange(len(px)) % v == 0, index=px.index)
                res = fast_backtest(px, w, mask=mask)
                for rung in RUNGS:
                    r = net(res, rung)
                    d = mstats(r.loc[st:])
                    oos = metrics(r.loc[OOS_START:])
                    isw = r.loc[st:IS_END]
                    arms.append(dict(panel=pname, dial=dial, rung=int(rung), v=v, **d,
                                     IS_Sharpe=metrics(isw)["Sharpe"],
                                     IS_CAGR=metrics(isw)["CAGR"],
                                     OOS_Sharpe=oos["Sharpe"], OOS_CAGR=oos["CAGR"],
                                     OOS_MaxDD=oos["MaxDD"],
                                     spy_oos_Sharpe=spy_oos["Sharpe"],
                                     v2_oos_Sharpe=BOOS[rung],
                                     p4a=pass4a(d, BAS[rung]),
                                     p4b=pass4b(d, spy, oos["Sharpe"], spy_oos["Sharpe"])))
    AR = pd.DataFrame(arms)
    P(f"\n  live arms {len(AR)} ({AR[['panel','dial','v']].drop_duplicates().shape[0]} books "
      f"x {len(RUNGS)} rungs)   time {time.time() - t0:.1f}s")

    # ---- menus: L evenly spaced rungs, both selectors choose on IS only
    rows = []
    for (pname, dial, rung), g in AR.groupby(["panel", "dial", "rung"]):
        full = LADDERS[dial]
        for L in LS:
            sub = sub_ladder(full, L)
            m = g[g.v.isin(sub)]
            if len(m) < 3:
                continue
            s = m.loc[m.IS_Sharpe.idxmax()]
            c = m.loc[m.IS_CAGR.idxmax()]
            rows.append(dict(panel=pname, dial=dial, rung=rung, L=len(m), arms=len(m),
                             pick_S=s.v, pick_C=c.v, same=bool(s.v == c.v),
                             dOOS_Sharpe=float(c.OOS_Sharpe - s.OOS_Sharpe),
                             dOOS_CAGR_pp=float((c.OOS_CAGR - s.OOS_CAGR) * 100),
                             S_OOS_Sharpe=float(s.OOS_Sharpe), C_OOS_Sharpe=float(c.OOS_Sharpe),
                             spy_oos=float(s.spy_oos_Sharpe), v2_oos=float(s.v2_oos_Sharpe),
                             S_p4a=bool(s.p4a), S_p4b=bool(s.p4b),
                             C_p4a=bool(c.p4a), C_p4b=bool(c.p4b)))
    M = pd.DataFrame(rows)
    P()
    P("  RULE 8 -- both selectors choose on 2009-2016 IS only; 2017+ read once.")
    P("  dOOS_Sharpe by ARM COUNT (pooled over panels and dials, both cost rungs):")
    for L, g in M.groupby("L"):
        P(f"    L={L:<3d} menus {len(g):3d}  disagree {1 - g.same.mean():.3f}  "
          f"mean dS {g.dOOS_Sharpe.mean():+.4f}  median {g.dOOS_Sharpe.median():+.4f}  "
          f"mean dCAGR {g.dOOS_CAGR_pp.mean():+.2f} pp")
    P()
    P("  dOOS_Sharpe by DIAL FAMILY (pooled over panels, arm counts and rungs):")
    for dial, g in M.groupby("dial"):
        P(f"    {dial:8s} menus {len(g):3d}  disagree {1 - g.same.mean():.3f}  "
          f"mean dS {g.dOOS_Sharpe.mean():+.4f}  median {g.dOOS_Sharpe.median():+.4f}  "
          f"mean dCAGR {g.dOOS_CAGR_pp.mean():+.2f} pp")
    P()
    P("  the FULL 5 x 5 controlled grid (dial x arm count), mean dOOS_Sharpe, all points:")
    piv = M.pivot_table(index="dial", columns="L", values="dOOS_Sharpe", aggfunc="mean")
    P("  " + piv.to_string(float_format=lambda x: f"{x:+.4f}").replace("\n", "\n  "))
    P()
    P("  disagreement rate, same grid:")
    piv2 = M.pivot_table(index="dial", columns="L", values="same",
                         aggfunc=lambda x: 1 - np.mean(x))
    P("  " + piv2.to_string(float_format=lambda x: f"{x:.3f}").replace("\n", "\n  "))
    P()
    P(f"  KEEP paths over ALL {len(AR)} live arms: 4a {int(AR.p4a.sum())}, "
      f"4b {int(AR.p4b.sum())}, BOTH {int((AR.p4a & AR.p4b).sum())}")
    for pn in PANELS:
        s = AR[AR.panel == pn]
        P(f"    {pn:9s} 4a {int(s.p4a.sum()):3d}/{len(s)}   4b {int(s.p4b.sum()):3d}/{len(s)}")
    P(f"  of the rule-8 PICKS: S_SHARPE 4a {int(M.S_p4a.sum())}/{len(M)} 4b "
      f"{int(M.S_p4b.sum())}/{len(M)};  S_CAGR 4a {int(M.C_p4a.sum())}/{len(M)} 4b "
      f"{int(M.C_p4b.sum())}/{len(M)}")
    P(f"  picks beating SPY OOS Sharpe: S_SHARPE {int((M.S_OOS_Sharpe > M.spy_oos).sum())}/{len(M)}"
      f"   S_CAGR {int((M.C_OOS_Sharpe > M.spy_oos).sum())}/{len(M)}")
    P(f"  picks beating RULES v2 OOS Sharpe: S_SHARPE {int((M.S_OOS_Sharpe > M.v2_oos).sum())}"
      f"/{len(M)}   S_CAGR {int((M.C_OOS_Sharpe > M.v2_oos).sum())}/{len(M)}")
    return AR, M


# ================================================================================================
def main():
    t00 = time.time()
    P("#" * 100)
    P("# Idea 493 -- is the -0.014 Sharpe cost of choosing on CAGR a record-wide CONSTANT?"
      "   (cloud, 2026-09-10)")
    P("#" * 100)
    PX = panels()
    G = gates(PX)
    d, GR, A = part_ab()
    F = fresh_scan()
    AR, M = live(PX)

    P()
    P("=" * 100)
    P("(F) THE ANSWER")
    P("=" * 100)
    q = GR.quotable.sum()
    P(f"  -0.014 lies inside the file-clustered 95% CI at {q} of {len(GR)} grid points.")
    P(f"  pooled file-clustered dS range across the grid: "
      f"{GR.pooled_dS.min():+.4f} .. {GR.pooled_dS.max():+.4f}")
    P(f"  family heterogeneity: UNRESTRICTED p {GR.p_free.min():.4f}..{GR.p_free.max():.4f}; "
      f"BLOCKED on (file x arms) p {GR.p_blocked.min():.4f}..{GR.p_blocked.max():.4f}")
    sl, st, _ = clustered_slope(d)
    P(f"  arm count: file-clustered slope {sl:+.5f} per doubling of arms (t {st:+.2f})")

    K = pd.DataFrame([dict(k=k, v=v) for k, v in G.items()]
                     + [dict(k="quotable_points", v=int(q)),
                        dict(k="live_4a", v=int(AR.p4a.sum())),
                        dict(k="live_4b", v=int(AR.p4b.sum()))])
    P()
    dump(d, "menus"); dump(GR, "grid"); dump(A, "arms")
    if len(F):
        dump(F, "fresh")
    dump(AR, "live"); dump(M, "livemenus"); dump(K, "keeppaths")
    P(f"\n  total {time.time() - t00:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
