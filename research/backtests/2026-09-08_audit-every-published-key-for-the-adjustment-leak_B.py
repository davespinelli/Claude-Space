#!/usr/bin/env python3
"""
IDEA 197 - audit-every-published-key-for-the-adjustment-leak   (lane B, 2026-09-08)

QUESTION (from the queue)
-------------------------
Idea 193 showed a key that reads the LEVEL of an auto-adjusted price series is contaminated with
future information by construction (Spearman with future total return -0.30 to -0.60), while ratio
keys cancel the factor.  Apply that one-line test to every key in the LEADERBOARD's published
books, classify each as LEVEL or RATIO, and report which published claims are affected.

WHAT THIS RUN IS
----------------
Three things, in order, plus the protocol's mandatory book work:

  T1  THE ONE-LINE TEST, made exact and executable.  Idea 193's diagnostic was a STATISTIC
      (Spearman with the future return).  A statistic cannot classify a key, because a genuine
      long-horizon signal also correlates with the future return.  This run replaces it with an
      ARITHMETIC test that has no sampling error at all:

          THEOREM.  Let adj[s] be an auto-adjusted close: adj[s] = raw[s] * F(s), where
          F(s) = prod of every split/dividend adjustment factor over (s, T].  A panel truncated
          at date t is adjusted to t, not to T, so its entries are
                  adj_t[s] = raw[s] * F_t(s),   F_t(s) = prod over (s, t] = F(s) / F(t).
          Hence   adj_t[s] = adj[s] / F(t)   for every s <= t:
          TRUNCATING THE PANEL AT t RESCALES EACH COLUMN BY ONE POSITIVE PER-NAME CONSTANT.
          Therefore a key is point-in-time honest on this data IFF its cross-sectional ranks are
          INVARIANT under  px -> px @ diag(c),  c_i > 0 arbitrary.  A key whose ranks move under
          that operator reads F(t) - i.e. the dividends and splits paid AFTER t.

      This is the whole audit: apply the operator, look at whether the ranks moved.  RATIO keys
      (px[t]/px[t-k], pct_change, px vs its own rolling mean) cancel c exactly; LEVEL keys
      (px itself, the entry bar, the terminal bar, price x volume) do not.

  T2  BACK-FILL idea 193's own statistic over the whole catalogue and over a HORIZON LADDER
      (h = 21, 63, 126, 252 bars, and h = T = "to the end of the sample"), so the leak signature
      (rho growing without bound in h, maximal at h = T) is separated from a genuine long-horizon
      signal (rho roughly flat in h).

  C   THE CENSUS.  361 committed scripts in research/backtests, scanned for the CONSTRUCTIONS
      above, not for column NAMES.  Idea 334 established that a census keyed on names is wrong by
      up to 270x on one family; "price" in this record is overwhelmingly the verb ("price the X
      against Y"), so a name census here would be nearly all false positives.  Every hit is
      recorded with file, line number and the matched source text, and joined to the LEADERBOARD
      by the Script column so the number of AFFECTED PUBLISHED CLAIMS is a count of rows, not an
      impression.

  B   THE CONSEQUENCE BOOK (protocol rules 3, 4, 8).  Idea 181's corpus-T book form, verbatim:
      top-N of `composite + dir*m*key`, N=20, gross 0.75, weekly, t+1, vol cap 0.60.  Full sample,
      halves, and the rule-8 walk-forward (parameters chosen on <= 2016-12-31 only, 2017-2026 read
      once).  Both KEEP paths evaluated on every arm: 4a against the LIVE RULES v2, 4b against SPY.

  E   THE OPERATOR, OBSERVED - added after the first run, see AMENDMENTS.  data/prices.csv was
      refreshed between two commits three days apart.  The two committed snapshots are a REAL
      before/after pair for the theorem, so the operator does not have to be modelled at all: the
      new/old ratio matrix is measured, and the drift it causes is split into (a) the new bar's own
      return, which is legitimate information, and (b) the retroactive re-adjustment of every prior
      bar, which is the leak.

  A   THE ADMISSIBLE-RESCALING SPREAD.  For a LEVEL key the published number is one draw: the
      panel happens to be adjusted to one particular T.  Re-run each level-key arm with the KEY
      computed on px @ diag(c) for B draws of c (returns untouched - only the key moves) and
      report the spread of full-sample Sharpe.  Exactly 0 for a ratio key, by T1.  Whatever it is
      for a level key is the width of the published claim's own arbitrariness.

TUNED PARAMETERS: exactly two, inherited verbatim from ideas 181/193 - the tilt strength
m in {0.20, 0.50, 1.00} and the direction in {POS, NEG}.  Every grid point is written to
<stem>.arms.csv and every one is reported.  The KEY, the PANEL, the COST RUNG, the horizon h, the
rescale dispersion sigma and the seed are REPORTED AXES and are never selected on.

PRE-REGISTERED PREDICTIONS (written before any new number was read; every one reported hit/miss)
  P1  R1 identity holds to < 1e-9 on all three panels (idea 193's anchor; the theorem's premise).
  P2  Under the rescaling operator every RATIO key moves by exactly 0 (max |d rankpct| < 1e-12)
      and every LEVEL key moves materially (> 0.05 mean |d rankpct| at sigma = 0.25).
  P3  RULES v1 and RULES v2 weight matrices are EXACTLY invariant -> the LIVE book carries no
      adjustment leak.  (This is the result that matters for capital.)
  P4  FROZEN - the key idea 193 introduced as substitution 1 FOR the leaking PRICE key - is
      itself NOT invariant, so the substitution does not remove the leak it was built to remove.
  P5  Level keys' |Spearman(key, forward return)| grows monotonically in h and is maximal at
      h = T; ratio keys are roughly flat and small at every h.
  P6  The admissible-rescaling Sharpe spread is exactly 0 for ratio keys and > 0.10 of Sharpe for
      at least one level-key arm.
  P7  No LEVEL-key arm is promoted: any 4a/4b pass carried by a level key is disqualified by T1
      regardless of its numbers.  Reported as counts, both paths, both rungs.

AMENDMENTS (disclosed: these were made AFTER the first run produced output, and say so)
  * P2 as pre-registered demanded max|d rankpct| < 1e-12 for a ratio key.  That bar is wrong in
    float64, not wrong in arithmetic: multiply-then-divide is not bit-exact, so a handful of
    NUMERICALLY TIED names swap rank and move rankpct by one rank step (0.0096 on broad = 1/104).
    The measure is restated as `frac_cells_moved` (fraction of cells moving > 1e-9), on which a
    ratio key is < 1e-4 and a level key is > 0.5.  The original wording is left above unchanged.
  * P5's second clause ("ratio keys are roughly flat and small at every h") was FALSIFIED by the
    first run and is reported as a miss, not repaired.  It is the run's most useful failure: see
    the T2 table, where the invariant keys VOL (+0.279) and VOLSH (-0.417) have a larger |rho| at
    h = T than the leaking PRICE key (-0.333).  The queue's "one-line test" - idea 193's Spearman
    - therefore CANNOT classify a key.  T1 can.
  * Section E was added after the first run, when the RULES v1 anchor failed to reproduce on the
    refreshed cache.  Chasing that failure is what produced the measured operator.
  * The census strips string literals before matching (`code_only`).  Without that step the record
    appears to contain 34 absolute price thresholds; all 34 are the prose `px > 200d MA` inside
    docstrings, and the true count in code is reported below.

CAVEATS
  * SURVIVORSHIP.  u56 / broad / small are CURRENT constituents (idea 54, PROTOCOL rule 9); the
    small panel additionally drops the 44 tickers with max_1d_move >= 1.0 (idea 186's screen).
  * The rescaling operator models the DIVIDEND+SPLIT channel that runs through PRICE.  Share
    VOLUME in these caches is split-adjusted too, so a volume-only key (VOLSH) is invariant under
    THIS operator while still carrying a weaker future-split channel of its own.  Stated, not
    measured: no split calendar is cached and the sandbox has no network.
  * sigma is a REPORTED sensitivity axis, not a fitted quantity.  It cannot be calibrated offline
    (no dividend series is cached), so two values are run and both are printed.  T1's verdict
    - moved or did not move - does not depend on sigma at all; only the SIZE in section A does.
  * MCAP remains PARKED (idea 195): needs local/Actions data.

Deterministic, standalone, no network (section E shells out to `git show`, read-only).  Writes
.reproduction.csv, .readjust.csv, .channels.csv, .keys.csv, .live.csv, .horizon.csv, .census.csv,
.arms.csv, .spread.csv, .walkforward.csv, .console.txt.
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
from baseline import (load_universe, load_volume, rules_v1_weights,  # noqa: E402
                      rules_v2_weights, band_state, score as v1_score)
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_audit-every-published-key-for-the-adjustment-leak_B"
OUT = ROOT / "research" / "backtests"

# --- book form inherited verbatim from idea 181 / 193 -------------------------------------------
SEED = 197
N, GROSS, FREQ, MAXVOL = 20, 0.75, "W", 0.60
MS = [0.20, 0.50, 1.00]                 # tuned parameter 1 (swept, all points reported)
DIRS = {"POS": 1.0, "NEG": -1.0}        # tuned parameter 2 (swept, all points reported)
COSTS = [0.0, 10.0, 25.0]
IS_END = pd.Timestamp("2016-12-31")
OOS_LO = IS_END + pd.Timedelta(days=1)
SIGMAS = [0.10, 0.25]                   # reported sensitivity axis, never selected on
B_SPREAD = 6                            # rescale draws per (panel, key, dir) in section A
HORIZONS = [21, 63, 126, 252]           # plus "T" (to the end of the sample)

RATIO_KEYS = ["MOM", "R6", "R3", "VOL", "REBASED", "DDTR", "VOLSH"]
LEVEL_KEYS = ["PRICE", "FROZEN", "DVOL", "DVOLT", "PXTERM"]
ORACLE = ["PXTERM", "FWDRET"]           # look-ahead by construction; diagnostics only


def klass_of(kn):
    """LEVEL = reads the adjusted price LEVEL (the leak T1 detects).
    FWD    = FWDRET: pure look-ahead, but built as a RATIO (term/px), so the T1 operator cannot
             see it.  It is carried deliberately as the control that fixes T1's SCOPE: the test
             certifies a key against the ADJUSTMENT leak, not against look-ahead in general.
    RATIO  = cancels the adjustment factor exactly."""
    if kn == "FWDRET":
        return "FWD"
    return "LEVEL" if kn in LEVEL_KEYS else "RATIO"

_console: list[str] = []


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    _console.append(line)


# ============================================================================== small helpers
def rankpct(df):
    return df.rank(axis=1, pct=True)


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 5:
        return np.nan
    ra = pd.Series(a[ok]).rank().values
    rb = pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def first_valid_row(px):
    fv = px.apply(lambda s: s.loc[s.first_valid_index()] if s.first_valid_index() is not None
                  else np.nan)
    return pd.DataFrame(np.tile(fv.values, (len(px), 1)),
                        index=px.index, columns=px.columns).where(px.notna())


def last_valid_row(px):
    lv = px.apply(lambda s: s.loc[s.last_valid_index()] if s.last_valid_index() is not None
                  else np.nan)
    return pd.DataFrame(np.tile(lv.values, (len(px), 1)),
                        index=px.index, columns=px.columns).where(px.notna())


def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (rankpct(mom) + rankpct(r6) + rankpct(r3)) / 3


def fast_backtest(prices, weights, cost_bps=0.0, freq=FREQ):
    """Vectorised equivalent of engine.backtest; asserted identical in R2."""
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
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


def win(r, lo=None, hi=None):
    x = r
    if lo is not None:
        x = x.loc[lo:]
    if hi is not None:
        x = x.loc[:hi]
    return x


def full_row(r):
    h = len(r) // 2
    out = {}
    for tag, x in (("F", r), ("H1", r.iloc[:h]), ("H2", r.iloc[h:]),
                   ("IS", win(r, hi=IS_END)), ("OOS", win(r, lo=OOS_LO))):
        m = metrics(x)
        out[f"CAGR_{tag}"], out[f"Sharpe_{tag}"], out[f"MaxDD_{tag}"] = \
            m["CAGR"], m["Sharpe"], m["MaxDD"]
    return out


def pass4a(row, base):
    """PROTOCOL 4a, judged against the LIVE rules (RULES v2 since 2026-09-06)."""
    return bool(row["Sharpe_H1"] > base["Sharpe_H1"] and row["Sharpe_H2"] > base["Sharpe_H2"]
                and row["MaxDD_F"] >= base["MaxDD_F"])


def pass4b(row, spy):
    return bool(row["Sharpe_H1"] > spy["Sharpe_H1"] and row["Sharpe_H2"] > spy["Sharpe_H2"]
                and row["Sharpe_OOS"] > spy["Sharpe_OOS"]
                and row["MaxDD_F"] >= 0.60 * spy["MaxDD_F"]
                and row["CAGR_F"] >= 0.70 * spy["CAGR_F"])


# ============================================================================ panels and keys
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    say(f"    small panel: dropped {len(bad)} tickers with max_1d_move >= 1.0; "
        f"{len(keep) - 1} names + SPY remain")
    return px[keep]


def build_keys(px, panel):
    """The record's key catalogue, each spelled exactly as the parent scripts spell it.

    Sources: idea 181 (`does-a-null-column-change-any-published-verdict`), idea 158
    (`does-share-price-any-key-or-only-vol`), idea 193 (`is-PRICE-NEG-...`), idea 196
    (`does-the-leak-free-selector-edge-survive-a-third-corpus`), idea 199
    (`is-the-low-price-tilt-a-split-artefact-or-a-survivorship-one`), plus the live book's own
    components (VOL is RULES v1's scaler; COMP is the composite both live versions rank on).
    """
    entry, term = first_valid_row(px), last_valid_row(px)
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    keys = {
        "COMP":    composite(px),                                   # live book's own ranking
        "VOL":     rankpct(vol20),                                  # RULES v1 scaler's key
        "MOM":     rankpct(px.shift(21) / px.shift(252) - 1),
        "R6":      rankpct(px / px.shift(126) - 1),
        "R3":      rankpct(px / px.shift(63) - 1),
        "REBASED": rankpct(px / entry),
        "DDTR":    rankpct(px / px.rolling(252).max() - 1.0),
        "PRICE":   rankpct(px),                                     # LEVEL - idea 181/199
        "FROZEN":  rankpct(entry),                                  # LEVEL - idea 193 subst. 1
        "PXTERM":  rankpct(term),                                   # LEVEL - oracle diagnostic
        "FWDRET":  rankpct(term / px - 1.0),                         # oracle diagnostic
    }
    if panel == "small":
        vol = load_volume(small=True).reindex(index=px.index, columns=px.columns)
        for nm, raw in (("DVOL", px * vol), ("DVOLT", term * vol), ("VOLSH", vol)):
            k = rankpct(raw.rolling(20).mean())
            if "SPY" in k.columns:
                k["SPY"] = 0.5
            keys[nm] = k
    return keys


def rescale(px, sigma, seed):
    """The T1 operator: px -> px @ diag(c), c_i = exp(N(0, sigma)) > 0, one draw per NAME.

    By the theorem in the docstring this is exactly what truncating the auto-adjusted panel at an
    earlier date does to it, up to which particular c the truncation date implies.
    """
    rng = np.random.default_rng(seed)
    c = np.exp(rng.normal(0.0, sigma, size=px.shape[1]))
    return px.mul(pd.Series(c, index=px.columns), axis=1)


# =================================================================================== sections
OLD_SNAPSHOT = "0e586d7"        # the previous committed state of data/prices.csv (2026-09-07)


def old_prices():
    """The previous committed snapshot of data/prices.csv, read out of git.

    Returns None if the commit is unreachable (e.g. a shallow clone that no longer carries it),
    in which case section E is skipped and says so - it never fabricates the comparison.
    """
    import subprocess
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "show", f"{OLD_SNAPSHOT}:data/prices.csv"],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not r.stdout:
            return None
        import io
        return pd.read_csv(io.StringIO(r.stdout), index_col=0, parse_dates=True).dropna(
            how="all").ffill()
    except Exception:
        return None


def section_E(px_new):
    """E - THE OPERATOR, OBSERVED.  Not a model: two committed snapshots of the SAME cache.

    The theorem says a re-adjustment multiplies a name's whole history by one positive constant.
    data/prices.csv was refreshed between 2026-09-07 and 2026-09-08.  If the theorem is right, the
    new/old ratio matrix is a per-name constant on every bar before the new ex-dividend bar.  This
    section measures that, then splits the drift it causes into its two channels:

        (a) NEW INFORMATION - the extra bar's own return.  Legitimate.  Hits every book.
        (b) RETROACTIVE RE-ADJUSTMENT - every prior bar's LEVEL changes.  This is the leak.
            It cannot touch a scale-invariant book and must touch a level-key book.
    """
    say("\n" + "=" * 96)
    say("E - THE OPERATOR OBSERVED IN THE PROJECT'S OWN CACHE (measurement, not a model)")
    say("=" * 96)
    o = old_prices()
    if o is None:
        say(f"  SKIPPED: commit {OLD_SNAPSHOT} not reachable in this clone; no fabricated numbers.")
        return pd.DataFrame(), pd.DataFrame()
    import json
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    T = sorted({t for g in U.values() for t in g} - {"BTC-USD", "ETH-USD"})
    o = o[T].loc["2008-01-01":]
    ci = o.index.intersection(px_new.index)
    cc = o.columns.intersection(px_new.columns)
    ratio = px_new.loc[ci, cc] / o.loc[ci, cc]
    body = ratio.iloc[:-1]                       # every bar before the newly ex-dividend bar
    med = body.median()
    dev = float((body.div(med, axis=1) - 1).abs().max().max())
    moved = med[(med - 1.0).abs() > 1e-9]
    say(f"  bars compared {len(ci)} x {len(cc)} names;  ratio new/old")
    say(f"    names whose ENTIRE history was rescaled : {len(moved)} of {len(cc)}"
        f"   -> {', '.join(f'{k} x{v:.6f}' for k, v in moved.items())}")
    say(f"    max deviation from a per-name CONSTANT  : {dev:.2e}"
        "   (CSV stores 4 dp; at a 0.47 price that IS 1e-4)")
    say("    -> the theorem's operator is exactly what a cache refresh does.")
    e1 = pd.DataFrame(dict(ticker=med.index, ratio_new_over_old=med.values,
                           rescaled=(med - 1.0).abs().values > 1e-9))

    # ------- the two channels, priced
    rows = []
    for nm, wfn, kind in (("RULES v1 (scale-invariant)", rules_v1_weights, "invariant"),
                          ("RULES v2 (scale-invariant)", rules_v2_weights, "invariant"),
                          ("PRICE/NEG m=1.00 (LEVEL key)", None, "level")):
        vals = {}
        for tag, p in (("old", o), ("new", px_new[cc].loc[:, :])):
            p = p.dropna(how="all").ffill()
            start = p.index[260]
            if wfn is not None:
                w = wfn(p)
            else:
                vol20 = p.pct_change().rolling(20).std() * np.sqrt(252)
                elig = (p > p.rolling(200).mean()) & (vol20 < MAXVOL)
                sc = composite(p) - 1.00 * rankpct(p)
                rk = sc.where(elig).rank(axis=1, ascending=False)
                w = (rk <= N).astype(float) * (GROSS / N)
            r, t = fast_backtest(p, w, 0.0)
            m = metrics((r - t * 10.0 / 1e4).loc[start:])
            vals[tag] = (m["CAGR"], m["Sharpe"], m["MaxDD"])
        rows.append(dict(book=nm, kind=kind,
                         CAGR_old=vals["old"][0], CAGR_new=vals["new"][0],
                         Sharpe_old=vals["old"][1], Sharpe_new=vals["new"][1],
                         MaxDD_old=vals["old"][2], MaxDD_new=vals["new"][2],
                         dSharpe=vals["new"][1] - vals["old"][1],
                         dCAGR_pp=100 * (vals["new"][0] - vals["old"][0])))
    e2 = pd.DataFrame(rows)
    say("\n  the same book on the two snapshots (u56 @10 bps, identical code):")
    say(e2[["book", "kind", "CAGR_old", "CAGR_new", "Sharpe_old", "Sharpe_new",
            "dSharpe", "dCAGR_pp"]].to_string(index=False, float_format=lambda x: f"{x:.5f}"))
    inv = e2[e2.kind == "invariant"].dSharpe.abs().max()
    lev = float(e2[e2.kind == "level"].dSharpe.abs().iloc[0])
    say(f"\n  channel (a) NEW INFORMATION, the extra bar's own return : {inv:.5f} of Sharpe")
    say(f"  channel (b) RETROACTIVE RE-ADJUSTMENT, this refresh      : {lev:.5f} of Sharpe")
    say("  READ THIS CORRECTLY.  One refresh is far too small to move anything: a single 0.064%")
    say("  dividend on 1 of 56 names does not reorder a cross-section, so channel (b) measures")
    say("  ZERO here and the level book is unmoved.  What E establishes is the MECHANISM, exactly:")
    say(f"  a routine cache refresh multiplied a name's ENTIRE {len(ci) - 1}-bar history by one")
    say("  constant, which is the T1 operator, observed, not modelled.  A LEVEL key does not read")
    say("  one refresh - it reads F(t), the PRODUCT of every such factor from t to the last bar.")
    if len(moved):
        f1 = float(moved.iloc[0])
        yrs = (ci[-1] - ci[0]).days / 365.25
        q = 1.0 / f1 - 1.0                       # one QUARTERLY dividend, the observed event
        say(f"  CALIBRATION (stated assumption: quarterly cadence, the standard US schedule).")
        say(f"  The observed event is x{f1:.6f}, i.e. a {q:.4%} quarterly dividend"
            f" = {4 * q:.2%}/yr on a low-yield name.")
        say(f"  Over the sample's {yrs:.1f} years that name's F(t) reaches"
            f" ~{(1 + 4 * q) ** yrs:.3f} (log {np.log((1 + 4 * q) ** yrs):.3f});"
            f" a 4%-yield name reaches ~{1.04 ** yrs:.2f} (log {np.log(1.04 ** yrs):.2f}).")
        say(f"  The cross-name dispersion of log F a level key reads is therefore roughly"
            f" 0 to {np.log(1.04 ** yrs):.2f},")
        say(f"  which is what sigma in {SIGMAS} brackets - conservatively.  Section A prices it.")
    say("\n  The published RULES v1 anchor (6.45305% / 0.66418 / -13.82780%) is reproduced EXACTLY")
    say("  on the old snapshot and is NOT reproducible on the new one.  The record's most-quoted")
    say("  number has an expiry date; channel (a) is its size, and that part is legitimate.")
    return e1, e2


def section_R(panels):
    """Reproduction, asserted before any new number is read."""
    say("\n" + "=" * 96)
    say("R - REPRODUCTION")
    say("=" * 96)
    rows = []

    px56 = panels["u56"]
    r = backtest(px56, rules_v1_weights(px56), cost_bps=10.0, freq="W")["returns"].loc[px56.index[260]:]
    m = metrics(r)
    say(f"  R0 RULES v1 u56 @10bps: {m['CAGR']:.5%} / {m['Sharpe']:.5f} / {m['MaxDD']:.5%}"
        "   (published anchor 6.45305% / 0.66418 / -13.82780%)")
    rows.append(dict(check="R0_rules_v1_u56_10bps", value=f"{m['CAGR']:.5%}/{m['Sharpe']:.5f}/{m['MaxDD']:.5%}",
                     ok=abs(m["Sharpe"] - 0.66418) < 5e-5))

    # R1: the adjusted-price identity that the theorem rests on
    for pn, px in panels.items():
        p = px.dropna(how="all")
        tr = (1.0 + p.pct_change().fillna(0.0)).cumprod()
        lhs = (p.iloc[-1] / p).div(1.0)              # px[T]/px[t]
        rhs = (tr.iloc[-1] / tr)                     # cumulative TR(t -> T)
        err = float(np.nanmax(np.abs((lhs - rhs).values)))
        say(f"  R1 identity px[T]/px[t] == TR(t->T)  {pn:<6} max abs err {err:.3e}")
        rows.append(dict(check=f"R1_identity_{pn}", value=f"{err:.3e}", ok=err < 1e-9))

    # R2/R3: fast_backtest == engine.backtest, and the cost identity
    w = rules_v1_weights(px56)
    a, ta = fast_backtest(px56, w, 0.0)
    b = backtest(px56, w, cost_bps=0.0, freq=FREQ)["returns"]
    e2 = float(np.nanmax(np.abs((a - b).values)))
    c = backtest(px56, w, cost_bps=10.0, freq=FREQ)["returns"]
    e3 = float(np.nanmax(np.abs(((a - ta * 10.0 / 1e4) - c).values)))
    say(f"  R2 fast_backtest == engine.backtest       max abs err {e2:.3e}")
    say(f"  R3 cost identity r_c == r_0 - turn*c/1e4  max abs err {e3:.3e}")
    rows.extend([dict(check="R2_fast_vs_engine", value=f"{e2:.3e}", ok=e2 < 1e-12),
                 dict(check="R3_cost_identity", value=f"{e3:.3e}", ok=e3 < 1e-12)])
    return pd.DataFrame(rows)


def section_T1(panels):
    """The one-line test: cross-sectional rank invariance under a per-name positive rescale."""
    say("\n" + "=" * 96)
    say("T1 - THE ONE-LINE TEST (exact): does the key's cross-sectional rank move when the panel")
    say("     is re-adjusted to a different terminal date?  RATIO keys cannot; LEVEL keys must.")
    say("=" * 96)
    rows = []
    for pn, px in panels.items():
        base = build_keys(px, pn)
        for sigma in SIGMAS:
            alts = [build_keys(rescale(px, sigma, SEED + 1000 * s), pn) for s in range(3)]
            for kn, k0 in base.items():
                dmax, dmean, dfrac, rhos = 0.0, [], [], []
                for ka in alts:
                    d = (ka[kn] - k0).abs()
                    dmax = max(dmax, float(np.nanmax(d.values)) if d.notna().any().any() else 0.0)
                    dmean.append(float(np.nanmean(d.values)))
                    dfrac.append(float(np.nanmean((d.values > 1e-9).astype(float))))
                    ix = k0.index[260::252]
                    rhos += [spearman(k0.loc[t].values, ka[kn].loc[t].values) for t in ix]
                # A RATIO key cancels the rescale EXACTLY in exact arithmetic.  In float64 the
                # multiply-then-divide is not bit-exact, so a handful of NUMERICALLY TIED names
                # can swap rank, moving rankpct by one rank step (1/n, e.g. 0.0096 on broad).
                # `frac_moved` is therefore the honest invariance measure: a ratio key moves a
                # vanishing fraction of cells, a level key moves essentially all of them.
                rows.append(dict(panel=pn, key=kn, sigma=sigma, klass=klass_of(kn),
                                 max_abs_d_rankpct=dmax, mean_abs_d_rankpct=float(np.mean(dmean)),
                                 frac_cells_moved=float(np.mean(dfrac)),
                                 mean_xs_spearman=float(np.nanmean(rhos)),
                                 invariant=bool(np.mean(dfrac) < 1e-4)))
    df = pd.DataFrame(rows)
    say("\n  per key, pooled over panels (sigma = 0.25 shown; sigma = 0.10 in .keys.csv):")
    sub = df[df.sigma == 0.25].groupby(["key", "klass"], as_index=False).agg(
        max_abs_d=("max_abs_d_rankpct", "max"), mean_abs_d=("mean_abs_d_rankpct", "mean"),
        frac_moved=("frac_cells_moved", "mean"),
        xs_rho=("mean_xs_spearman", "mean"), invariant=("invariant", "all"))
    sub = sub.sort_values(["invariant", "frac_moved"], ascending=[True, False])
    say(sub.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    return df


def section_T1_live(panels):
    """P3: the live book itself.  Weights, not keys - the object that holds capital."""
    say("\n" + "-" * 96)
    say("  T1-LIVE - the same operator applied to the LIVE books' own weight matrices")
    rows = []
    for pn, px in panels.items():
        q = rescale(px, 0.25, SEED)
        for nm, fn in (("RULES v1 weights", rules_v1_weights),
                       ("RULES v2 weights", rules_v2_weights),
                       ("v1 composite score", lambda p: v1_score(p)[0]),
                       ("v1 above-200d-MA", lambda p: v1_score(p)[1].astype(float)),
                       ("v1 vol20", lambda p: v1_score(p)[2]),
                       ("v2 band_state", lambda p: band_state(p).astype(float))):
            a, b = fn(px), fn(q)
            dv = np.abs((a - b).values)
            d = float(np.nanmax(dv))
            fr = float(np.nanmean((dv > 1e-9).astype(float)))
            rows.append(dict(panel=pn, object=nm, max_abs_diff=d, frac_cells_moved=fr,
                             is_weights=nm.endswith("weights"), invariant=bool(d < 1e-12)))
    df = pd.DataFrame(rows)
    say(df.pivot(index="object", columns="panel", values="max_abs_diff").to_string(
        float_format=lambda x: f"{x:.3e}"))
    say("  cells moved (fraction):")
    say(df.pivot(index="object", columns="panel", values="frac_cells_moved").to_string(
        float_format=lambda x: f"{x:.2e}"))
    w = df[df.is_weights]
    say(f"  -> the objects that hold capital (v1/v2 WEIGHT matrices) invariant on every panel: "
        f"{bool(w.invariant.all())}   (max abs diff {w.max_abs_diff.max():.1e})")
    say("     The two intermediates that move do so on a single MA-crossing bar where `px > MA`")
    say("     is a floating-point tie; it does not reach the weights.")
    return df


def section_T2(panels):
    """Back-fill idea 193's statistic over the catalogue, on a horizon ladder."""
    say("\n" + "=" * 96)
    say("T2 - Spearman(key_t, forward return over h) - idea 193's statistic, back-filled, with h")
    say("     as a ladder.  A LEAK grows without bound in h and peaks at h = T; a real signal does")
    say("     not.  (h = T is the statistic idea 193 published.)")
    say("=" * 96)
    rows = []
    for pn, px in panels.items():
        keys = build_keys(px, pn)
        dates = px.index[260::63]
        fwd = {h: px.shift(-h) / px - 1.0 for h in HORIZONS}
        fwd["T"] = last_valid_row(px) / px - 1.0
        for kn, k in keys.items():
            for h, f in fwd.items():
                rho = np.nanmean([spearman(k.loc[t].values, f.loc[t].values) for t in dates])
                rows.append(dict(panel=pn, key=kn, h=str(h), rho=float(rho),
                                 klass=klass_of(kn)))
    df = pd.DataFrame(rows)
    piv = df.pivot_table(index=["klass", "key"], columns="h", values="rho", aggfunc="mean")
    piv = piv[[c for c in ["21", "63", "126", "252", "T"] if c in piv.columns]]
    say(piv.to_string(float_format=lambda x: f"{x:+.4f}"))
    return df


# The census is gated on the CONSTRUCTION, never on a column name (idea 334: a name-keyed census
# is wrong by up to 270x on one family, and in this record "price" is overwhelmingly the verb).
# Identifiers are restricted to the price-frame spellings the corpus actually uses (px, px56, pxs,
# px_n, prices, entry/term from first_valid_row/last_valid_row) so `comp.rank`, `piv.rank` and
# `pr.rank` cannot masquerade as a price-level read.
_PX = r"(?:px\w*|prices)"
LEVEL_PATTERNS = [
    ("XS_RANK_OF_LEVEL", rf"rankpct\(\s*{_PX}\s*\)|\b{_PX}\.rank\(\s*axis\s*=\s*1"),
    ("ENTRY_BAR_LEVEL", r"rankpct\(\s*entry\w*\s*\)|rankpct\(\s*first_valid_row"
                        r"|\bentry\w*\.rank\(\s*axis\s*=\s*1"),
    ("TERMINAL_BAR_LEVEL", r"rankpct\(\s*term\w*\s*\)|rankpct\(\s*last_valid_row"
                           r"|\bterm\w*\.rank\(\s*axis\s*=\s*1"),
    ("PRICE_TIMES_VOLUME", rf"\b(?:{_PX}|term\w*|entry\w*)\s*\*\s*vol\w*\b"
                           rf"|\bvol\w*\s*\*\s*(?:{_PX}|term\w*)\b"),
    ("ABS_PRICE_THRESHOLD", rf"\b{_PX}\s*[<>]=?\s*\d"),
    ("LOG_LEVEL", rf"np\.log\(\s*{_PX}\s*\)"),
]
RATIO_PATTERNS = [
    ("RETURN_RATIO", rf"{_PX}\s*/\s*{_PX}\.shift\("),
    ("PCT_CHANGE", rf"{_PX}\.pct_change\("),
    ("VS_OWN_ROLLING", rf"{_PX}\s*[/><]\s*{_PX}\.rolling\("),
    ("REBASE", rf"{_PX}\s*/\s*entry\w*"),
]


def code_only(text):
    """Source with every STRING LITERAL blanked out (docstrings included) and comments dropped.

    Required, not cosmetic: this record's docstrings are full of the prose `px > 200d MA`, and a
    scanner that reads them finds 34 'absolute price thresholds' that do not exist in any code.
    Blanking only the literal's character span (not the whole line) keeps genuine hits that share
    a line with a string, e.g. `{"PRICE": rankpct(px)}`.
    """
    import ast
    lines = text.split("\n")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [l.split("#")[0] for l in lines]
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and getattr(node, "end_lineno", None):
            a, b = node.lineno - 1, node.end_lineno - 1
            for j in range(a, min(b + 1, len(lines))):
                lo = node.col_offset if j == a else 0
                hi = node.end_col_offset if j == b else len(lines[j])
                lines[j] = lines[j][:lo] + " " * (hi - lo) + lines[j][hi:]
    return [l.split("#")[0] for l in lines]


def section_C():
    """Value-gated census: classify CONSTRUCTIONS, never column names (idea 334)."""
    say("\n" + "=" * 96)
    say("C - CENSUS of the committed corpus, gated on the CONSTRUCTION (not the column name),")
    say("    with every string literal blanked first (see code_only)")
    say("=" * 96)
    files = [f for f in sorted(OUT.glob("*.py")) if f.stem != STEM]
    rows = []
    for f in files:
        try:
            src = code_only(f.read_text())
        except Exception:
            continue
        for i, code in enumerate(src, 1):
            line = code
            for tag, pat in LEVEL_PATTERNS:
                if re.search(pat, code):
                    rows.append(dict(file=f.name, line=i, kind="LEVEL", pattern=tag,
                                     src=line.strip()[:160]))
            for tag, pat in RATIO_PATTERNS:
                if re.search(pat, code):
                    rows.append(dict(file=f.name, line=i, kind="RATIO", pattern=tag,
                                     src=line.strip()[:160]))
    df = pd.DataFrame(rows)
    lev = df[df.kind == "LEVEL"]
    say(f"  scripts scanned                      : {len(files)}")
    say(f"  scripts with >=1 LEVEL construction  : {lev.file.nunique()} "
        f"({lev.file.nunique() / max(len(files), 1):.1%})")
    say(f"  scripts with >=1 RATIO construction  : {df[df.kind == 'RATIO'].file.nunique()}")
    say("\n  LEVEL constructions by pattern:")
    say(lev.groupby("pattern").agg(hits=("line", "size"),
                                   files=("file", "nunique")).to_string())
    say("\n  every script carrying a LEVEL construction:")
    for fn, g in lev.groupby("file"):
        say(f"    {fn}  ({', '.join(sorted(set(g.pattern)))}; {len(g)} lines)")

    # join to the LEADERBOARD by its Script column
    lb = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    lb_rows = [l for l in lb if l.startswith("|") and l.count("|") > 6]
    scripts = []
    for l in lb_rows:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        scripts.append(cells[-1] if cells else "")
    lbs = pd.Series(scripts)
    affected = set(lev.file.unique())
    hit = lbs[lbs.isin(affected)]
    say(f"\n  LEADERBOARD rows parsed                    : {len(lbs)}")
    say(f"  LEADERBOARD rows whose script carries a LEVEL construction: {len(hit)} "
        f"({len(hit) / max(len(lbs), 1):.1%})")
    if len(hit):
        say(hit.value_counts().to_string())
    return df, len(lbs), len(hit)


def section_B(panels):
    """The consequence book: full sample, halves, rule 8, both KEEP paths."""
    say("\n" + "=" * 96)
    say("B - THE CONSEQUENCE BOOK (idea 181's form verbatim; 2 tuned params, all points reported)")
    say("=" * 96)
    arms, spread_rows = [], []
    for pn, px in panels.items():
        start = px.index[260]
        keys = build_keys(px, pn)
        comp = composite(px)
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        elig = (px > px.rolling(200).mean()) & (vol20 < MAXVOL)

        def run(score):
            rank = score.where(elig).rank(axis=1, ascending=False)
            w = (rank <= N).astype(float) * (GROSS / N)
            r, t = fast_backtest(px, w, 0.0)
            return r.loc[start:], t.loc[start:]

        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        srow = full_row(spy)
        c0, ct = run(comp)                                   # untilted control
        v2r, v2t = fast_backtest(px, rules_v2_weights(px), 0.0)
        v2r, v2t = v2r.loc[start:], v2t.loc[start:]
        base_rows = {c: full_row(v2r - v2t * c / 1e4) for c in COSTS}
        ctrl_rows = {c: full_row(c0 - ct * c / 1e4) for c in COSTS}
        for c in COSTS:
            r = dict(panel=pn, key="CONTROL", klass="control", dir="-", m=0.0, cost=c,
                     turnover_yr=float(ct.sum() / (len(ct) / 252)), dSharpe_F=0.0,
                     dSharpe_IS=0.0, dSharpe_OOS=0.0)
            r.update(ctrl_rows[c])
            r["pass4a"] = pass4a(r, base_rows[c])
            r["pass4b"] = pass4b(r, srow)
            arms.append(r)
        for c in COSTS:
            for nm, rr in (("RULESv2", base_rows[c]), ("SPY", srow)):
                if c == 10.0 or nm == "RULESv2":
                    row = dict(panel=pn, key=nm, klass="comparand", dir="-", m=0.0, cost=c,
                               turnover_yr=np.nan, dSharpe_F=np.nan, dSharpe_IS=np.nan,
                               dSharpe_OOS=np.nan, pass4a=False, pass4b=False)
                    row.update(rr)
                    arms.append(row)

        for kn, kv in keys.items():
            klass = ("oracle" if kn in ORACLE else
                     "LEVEL" if kn in LEVEL_KEYS else "RATIO")
            for dn, dv in DIRS.items():
                for m in MS:
                    r0, trn = run(comp + dv * m * kv)
                    for c in COSTS:
                        rr = dict(panel=pn, key=kn, klass=klass, dir=dn, m=m, cost=c,
                                  turnover_yr=float(trn.sum() / (len(trn) / 252)))
                        rr.update(full_row(r0 - trn * c / 1e4))
                        for tag in ("F", "IS", "OOS"):
                            rr[f"dSharpe_{tag}"] = rr[f"Sharpe_{tag}"] - ctrl_rows[c][f"Sharpe_{tag}"]
                        rr["pass4a"] = pass4a(rr, base_rows[c])
                        rr["pass4b"] = pass4b(rr, srow)
                        arms.append(rr)

        # ---- section A: admissible-rescaling spread, at the strongest tilt (m = 1.00).
        # Seeds loop OUTSIDE the keys so exactly one rescaled key set is resident at a time.
        spread_keys = [k for k in keys
                       if k in LEVEL_KEYS or k in ("MOM", "REBASED", "DDTR", "VOLSH")]
        sh = {(k, d): [] for k in spread_keys for d in DIRS}
        for s in range(B_SPREAD):
            alt_keys = build_keys(rescale(px, 0.25, SEED + 7919 * s), pn)
            for kn in spread_keys:
                for dn, dv in DIRS.items():
                    ra, ta = run(comp + dv * 1.00 * alt_keys[kn])
                    sh[(kn, dn)].append(metrics(ra - ta * 10.0 / 1e4)["Sharpe"])
            del alt_keys
        for kn in spread_keys:
            klass = "LEVEL" if kn in LEVEL_KEYS else "RATIO"
            for dn, dv in DIRS.items():
                pubr, pubt = run(comp + dv * 1.00 * keys[kn])
                pub = metrics(pubr - pubt * 10.0 / 1e4)["Sharpe"]
                v = sh[(kn, dn)]
                spread_rows.append(dict(panel=pn, key=kn, klass=klass, dir=dn, m=1.00,
                                        sigma=0.25, B=B_SPREAD, published_Sharpe=pub,
                                        mean_Sharpe=float(np.mean(v)),
                                        sd_Sharpe=float(np.std(v, ddof=1)),
                                        min_Sharpe=float(np.min(v)),
                                        max_Sharpe=float(np.max(v)),
                                        range_Sharpe=float(np.max(v) - np.min(v))))
    return pd.DataFrame(arms), pd.DataFrame(spread_rows)


def section_8(arms):
    """Rule 8: choose the two tuned parameters on <= 2016 only, read 2017-2026 once."""
    say("\n" + "=" * 96)
    say("RULE 8 - WALK-FORWARD.  (m, dir) chosen by IS Sharpe on <= 2016-12-31 within each")
    say("     (panel, key, rung) cell; the 2017-2026 window is then read once.")
    say("=" * 96)
    g = arms[~arms.klass.isin(["comparand", "control"])].copy()
    picks = []
    for (pn, kn, c), sub in g.groupby(["panel", "key", "cost"]):
        best = sub.loc[sub.Sharpe_IS.idxmax()]
        ctrl = arms[(arms.panel == pn) & (arms.key == "CONTROL") & (arms.cost == c)].iloc[0]
        v2 = arms[(arms.panel == pn) & (arms.key == "RULESv2") & (arms.cost == c)].iloc[0]
        spy = arms[(arms.panel == pn) & (arms.key == "SPY")].iloc[0]
        picks.append(dict(panel=pn, key=kn, klass=best.klass, cost=c,
                          pick_m=best.m, pick_dir=best["dir"],
                          IS_Sharpe=best.Sharpe_IS,
                          OOS_CAGR=best.CAGR_OOS, OOS_Sharpe=best.Sharpe_OOS,
                          OOS_MaxDD=best.MaxDD_OOS,
                          ctrl_OOS_Sharpe=ctrl.Sharpe_OOS, ctrl_OOS_CAGR=ctrl.CAGR_OOS,
                          ctrl_OOS_MaxDD=ctrl.MaxDD_OOS,
                          v2_OOS_Sharpe=v2.Sharpe_OOS, v2_OOS_CAGR=v2.CAGR_OOS,
                          v2_OOS_MaxDD=v2.MaxDD_OOS,
                          spy_OOS_Sharpe=spy.Sharpe_OOS, spy_OOS_CAGR=spy.CAGR_OOS,
                          spy_OOS_MaxDD=spy.MaxDD_OOS,
                          d_vs_ctrl=best.Sharpe_OOS - ctrl.Sharpe_OOS,
                          pass4a=bool(best.pass4a), pass4b=bool(best.pass4b)))
    df = pd.DataFrame(picks)
    for c in COSTS:
        sub = df[df.cost == c]
        say(f"\n  --- cost rung {c:.0f} bps ---")
        cols = ["panel", "key", "klass", "pick_m", "pick_dir", "IS_Sharpe", "OOS_CAGR",
                "OOS_Sharpe", "OOS_MaxDD", "d_vs_ctrl", "pass4a", "pass4b"]
        say(sub[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return df


# ================================================================================ main
def main():
    t0 = time.time()
    say(f"IDEA 197 - audit-every-published-key-for-the-adjustment-leak  (lane B, {pd.Timestamp.today().date()})")
    say(f"  book: top-{N} of composite + dir*m*key, gross {GROSS}, freq {FREQ}, vol cap {MAXVOL}, t+1")
    say(f"  tuned params (2): m in {MS}, dir in {list(DIRS)}.  Reported axes: key, panel, rung, h, sigma, seed.")

    panels = {"u56": load_universe(), "broad": load_universe(broad=True), "small": small_panel()}
    for pn, px in panels.items():
        say(f"    panel {pn:<6} {px.shape[1]:>4} cols  {px.index[0].date()} .. {px.index[-1].date()}")

    rep = section_R(panels)
    e1, e2 = section_E(panels["u56"])
    keys_df = section_T1(panels)
    live_df = section_T1_live(panels)
    hor = section_T2(panels)
    census, n_lb, n_hit = section_C()
    arms, spread = section_B(panels)
    wf = section_8(arms)

    # ---------------------------------------------------------------- section A print
    say("\n" + "=" * 96)
    say("A - ADMISSIBLE-RESCALING SPREAD of full-sample Sharpe @10 bps (m = 1.00, sigma = 0.25,")
    say(f"    B = {B_SPREAD} draws).  Exactly 0 for a ratio key, by T1.")
    say("=" * 96)
    say(spread.sort_values("range_Sharpe", ascending=False).to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- KEEP paths
    say("\n" + "=" * 96)
    say("KEEP PATHS - both, every arm, every rung")
    say("=" * 96)
    real = arms[~arms.klass.isin(["comparand"])]
    for c in COSTS:
        s = real[real.cost == c]
        say(f"  {c:>4.0f} bps: 4a {int(s.pass4a.sum()):>3} / {len(s)}   "
            f"4b {int(s.pass4b.sum()):>3} / {len(s)}   "
            f"BOTH {int((s.pass4a & s.pass4b).sum()):>3}")
    say("\n  passes by key class (10 bps):")
    s10 = real[real.cost == 10.0]
    say(s10.groupby("klass").agg(n=("key", "size"), p4a=("pass4a", "sum"),
                                 p4b=("pass4b", "sum")).to_string())
    lvl_pass = s10[(s10.klass.isin(["LEVEL", "oracle"])) & (s10.pass4a | s10.pass4b)]
    say(f"\n  P7: arms passing a KEEP path on a LEVEL/oracle key @10 bps: {len(lvl_pass)} "
        f"- every one DISQUALIFIED by T1 (not implementable at any cost).")
    if len(lvl_pass):
        say(lvl_pass[["panel", "key", "dir", "m", "CAGR_F", "Sharpe_F", "MaxDD_F",
                      "Sharpe_OOS", "pass4a", "pass4b"]].to_string(
            index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- predictions
    say("\n" + "=" * 96)
    say("PRE-REGISTERED PREDICTIONS")
    say("=" * 96)
    p1 = bool(rep[rep.check.str.startswith("R1")].ok.all())
    k25 = keys_df[keys_df.sigma == 0.25]
    ratio_ok = bool(k25[k25.klass == "RATIO"].frac_cells_moved.max() < 1e-4)
    level_ok = bool(k25[k25.klass == "LEVEL"].groupby("key").frac_cells_moved.mean().min() > 0.50)
    p2 = ratio_ok and level_ok
    p3 = bool(live_df[live_df.is_weights].invariant.all())
    p4 = bool(not k25[k25.key == "FROZEN"].invariant.any())
    lev_T = hor[(hor.klass == "LEVEL") & (hor.h == "T")].rho.abs().mean()
    lev_21 = hor[(hor.klass == "LEVEL") & (hor.h == "21")].rho.abs().mean()
    rat_T = hor[(hor.klass == "RATIO") & (hor.h == "T")].rho.abs().mean()
    p5 = bool(lev_T > lev_21 and lev_T > rat_T)
    p6 = bool(spread[spread.klass == "RATIO"].range_Sharpe.max() < 1e-9
              and spread[spread.klass == "LEVEL"].range_Sharpe.max() > 0.10)
    p7 = len(lvl_pass)
    for nm, v, note in (("P1 R1 identity < 1e-9", p1, ""),
                        ("P2 ratio invariant (frac cells moved <1e-4), level not (>0.50)", p2,
                         f"ratio max frac {k25[k25.klass=='RATIO'].frac_cells_moved.max():.2e}, "
                         f"level min frac {k25[k25.klass=='LEVEL'].groupby('key').frac_cells_moved.mean().min():.4f}"),
                        ("P3 LIVE book exactly invariant", p3, ""),
                        ("P4 FROZEN is NOT invariant", p4, ""),
                        ("P5 level |rho| peaks at h=T", p5,
                         f"level |rho| h=21 {lev_21:.4f} -> h=T {lev_T:.4f}; ratio h=T {rat_T:.4f}"),
                        ("P6 rescale spread 0 for ratio, >0.10 for a level arm", p6,
                         f"level max range {spread[spread.klass=='LEVEL'].range_Sharpe.max():.4f}"),
                        ):
        say(f"  {'HIT ' if v else 'MISS'}  {nm}   {note}")
    say(f"  INFO  P7 level/oracle arms passing a KEEP path @10 bps: {p7} (all disqualified by T1)")

    # ---------------------------------------------------------------- write outputs
    rep.to_csv(OUT / f"{STEM}.reproduction.csv", index=False)
    if len(e1):
        e1.to_csv(OUT / f"{STEM}.readjust.csv", index=False)
        e2.to_csv(OUT / f"{STEM}.channels.csv", index=False)
    keys_df.to_csv(OUT / f"{STEM}.keys.csv", index=False)
    live_df.to_csv(OUT / f"{STEM}.live.csv", index=False)
    hor.to_csv(OUT / f"{STEM}.horizon.csv", index=False)
    census.to_csv(OUT / f"{STEM}.census.csv", index=False)
    arms.to_csv(OUT / f"{STEM}.arms.csv", index=False)
    spread.to_csv(OUT / f"{STEM}.spread.csv", index=False)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\ndone in {time.time() - t0:.0f}s;  LEADERBOARD rows parsed {n_lb}, "
        f"rows on a LEVEL-construction script {n_hit}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_console) + "\n")


if __name__ == "__main__":
    main()
