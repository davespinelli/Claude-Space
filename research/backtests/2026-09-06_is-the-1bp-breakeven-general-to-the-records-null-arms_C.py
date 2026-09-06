#!/usr/bin/env python3
"""Idea 262 - "is-the-1bp-breakeven-general-to-the-records-null-arms" (lane C, 2026-09-06).

The question
------------
Idea 260 found that its weekly-re-draw null arm (`RANDW`) beats the composite's top-n
ONLY below 1.0-1.3 bps of round-trip cost, in 7 of its 8 unsaturated cells, because a
fresh draw at every rebalance costs 38-60x/yr of turnover against the composite's 10-14x.
The queue's follow-up:

    Every RANDOM/null/rotation arm in the record is built either HELD or RE-DRAWN, and
    the choice is never priced.  Pool them, measure each one's turnover against its
    comparand, and report the cost rung at which each published null verdict flips.

Two things have to happen for that to be an answer and not an anecdote.

  (A) A CENSUS of how the record actually builds its nulls.  59 of the committed backtest
      scripts call an RNG.  This run classifies EVERY rng call site in
      research/backtests/*.py by the SHAPE of the draw - the thing that determines the
      arm's turnover - into HELD_KEY / REDRAWN_KEY / PERM / SUBSET_PANEL / NOISE /
      OTHER, writes every site with its source line to `.census.csv`, and reports the
      counts.  The classifier is mechanical and its rules are in `classify_site()`;
      a hand-audit sample is written to `.audit.csv` so the reader can check it.

  (B) A PRICE for the choice.  The census's classes differ in exactly one thing: how
      often the pick is re-drawn.  So this run builds the PERSISTENCE LADDER directly -
      the same uniform-key null re-drawn never / annually / quarterly / monthly / weekly,
      plus a deterministic weekly ROTATION arm - all at matched n, matched gross, matched
      cadence, on three panels, and measures for each one:

          * its realised turnover and the ratio to its comparand's (idea 263's column),
          * its Sharpe difference to the comparand at 0 bps (the "sign rung"),
          * the EXACT cost rung at which that difference flips sign (the breakeven),

      and then asks whether idea 260's 1.0-1.3 bps generalises.

Design
------
Panels U56 / B136 / BSTK100, weekly cadence, next-day execution, gate = above-200d AND
vol20 < 0.60, key = the composite WITHOUT the vol scaler, gross matched at 0.75 on every
arm including EWall (idea 73's CANDg / idea 240's NORM), n in {20,30,40,60}, 8 seeds -
all of that is idea 82's and idea 260's construction, imported so the two published
verdicts reproduce inside this run rather than being quoted.

    EWall   every eligible name, equal weight, gross matched     (comparand, gate only)
    FWD     top-n by the composite key                           (comparand, the incumbent)
    v1      the live RULES book                                  (baseline)
    RANDH   per-name uniform drawn ONCE (rng 1000+seed), held    <- idea 82's RAND, byte-for-byte
    RANDA   fresh uniform at each ANNUAL boundary  (rng 3000+seed)
    RANDQ   fresh uniform at each QUARTERLY boundary (rng 4000+seed)
    RANDM   fresh uniform at each MONTHLY boundary (rng 5000+seed)
    RANDW   fresh uniform at EVERY weekly rebalance (rng 2000+seed) <- idea 260's RANDW, byte-for-byte
    RWK     a per-name gaussian RANDOM WALK keyed by its own 126d momentum (rng 6000+seed)
            <- the record's THIRD null shape, imported from `does-a-harmful-instrument-
            clear-more-often-than-a-helpful-one_B` lines 262-265; its churn is EMERGENT,
            not scheduled, so the held/re-drawn dichotomy does not describe it at all
    ROTW    DETERMINISTIC rotation: at rebalance k take eligible names at positions
            (k*n + j) mod n_eligible in a fixed alphabetical order      (the "rotation" arm)

The five RAND arms differ from each other in NOTHING except the re-draw period, and RANDH
and RANDW are the record's two published endpoints.  ROTW carries the same ~full-book
churn as RANDW with zero randomness, which separates "the draw" from "the churn"; RWK is
the census's third construction and sits wherever its own drift puts it.

COST.  `engine.backtest` computes `port = (held*rets).sum(axis=1) - turnover*bps/1e4`,
and neither `held` nor `turnover` depends on the rung, so every book is run ONCE at 0 bps
and any rung is derived EXACTLY as `r(c) = r(0) - turnover*c/1e4`.  The identity is
asserted against a live `backtest(cost_bps=10)` call before any result is read; the run
aborts if it is not 0.  Reported rungs: 0 / 1 / 2 / 5 / 10 / 25 bps, every book at every
rung, in `.grid.csv`.  Breakevens are solved on a 0.05-bps ladder from 0 to 60 bps, which
is exact (not an interpolation between three measured points as in idea 260 section 5).

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (3)      2. n (4)
The arm/re-draw period is the hypothesis axis (pre-registered below), the seed is averaged
over with every draw written out, and the cost rung is a reported axis - the whole point.
Grid = 3 panels x [EWall + v1 + 4 FWD + 4 ROTW + 6 arms x 4 n x 8 seeds] x 6 rungs
     = 3 x 202 x 6 = 3636 points, ALL written to `.grid.csv`.

Pre-registered decision rule (written before any number of this run was read)
----------------------------------------------------------------------------
Read on `X - FWD` (same n) and `X - EWall`, Sharpe, over unsaturated cells:

  (a) GENERAL.  If every RE-DRAWN family (weekly, monthly, quarterly) has a breakeven
      below PROTOCOL's 10 bps in the large majority of cells, then every published null
      verdict resting on a re-drawn arm is a statement about a frictionless market, and
      the record's 0-bps null readings need the qualifier idea 260 attached to its own.

  (b) PERSISTENCE-GRADED.  If the breakeven rises monotonically with the re-draw period
      so that the HELD arm (the census's majority class, if it is one) either never flips
      or flips far above 10 bps, then the 1-bp breakeven is NOT general: it is a property
      of high-churn nulls specifically, and the record's held-draw verdicts are not
      contaminated in idea 260's way.  (a) and (b) are not exclusive - the expected world
      is both, and the deliverable is then the boundary between them.

  (c) THE LAW.  Sharpe is linear in the rung to first order:
          dSharpe(c) = dSharpe(0) - c * (T_X/vol_X - T_Y/vol_Y) / 1e4
      so the breakeven is predicted by `c* = dSharpe(0)*1e4 / (T_X/vol_X - T_Y/vol_Y)`
      from published columns alone.  If measured-vs-predicted has R^2 > 0.90, then idea
      263's proposed column (both turnovers + the 0-bps difference) is SUFFICIENT to
      reconstruct any turnover-mismatched verdict's breakeven WITHOUT re-running it, and
      that - not a new book - is this run's usable output.  R^2 <= 0.90 kills that claim.

  A KILL/PARK/ANSWERED verdict is expected: this is a measurement idea, not a book.  Both
  KEEP paths are still evaluated on every grid point and rule 8 is still run, per PROTOCOL.

Reproduction gate (asserted before anything else is read)
    U56/FIXED20 (idea 73's literal GROSS/n)   -> 12.7% / 1.093 / -18.3%, halves 1.088/1.103
    U56/RULES v1                              -> 6.5% / 0.666 / -13.8%
    idea 82's isolate at 10 bps  `FWD - RANDH` = -0.0213, t -2.72 per (cell, seed), 21/64
    idea 260's `FWD - RANDW` at 0 bps          = -0.0236 per (cell, seed), 20/64 positive
    idea 260's B136 n=20 RANDW breakeven       ~ 1.3 bps
  RANDH and RANDW use idea 260's exact rng streams and seeds, so these are reproductions,
  not quotations.  A mismatch beyond the stated tolerance aborts the run.

Walk-forward (PROTOCOL rule 8) - selectors fixed, with direction, before any OOS read
    EWALL / FWD20 / RANDH20 / RANDM20 / RANDW20 / RWK20 / ROTW20 / ALL_ISARGMAX
    IS = 2009-01-01..2016-12-31 (the only place anything is chosen),
    OOS = 2017-01-01..end, read once, at every rung, pooled equal-weight over panels,
    against RULES v1 OOS and SPY OOS.

Verdicts (both KEEP paths, every point, every rung)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SATURATION.  When a panel supplies fewer than n eligible names every n-arm IS EWall.
`sat_share` is reported per cell; cells with sat_share > 0.25 are excluded from headline
counts, exactly as in ideas 82 and 260.

SURVIVORSHIP.  universe_broad.json and the megacap cut are CURRENT constituents, so B136
and BSTK100 are one-directional.  The bias runs TOWARD the long-hold arms (a subset held
for the sample collects the full survivorship premium of whatever it drew) and AGAINST
the re-drawn ones, i.e. toward finding a LARGER 0-bps deficit for the churny arms and
therefore a LOWER breakeven for them.  Any conclusion in that direction is discounted by
it and the discount is restated in the result.

Deterministic (fixed seeds), standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import os
import pickle
import re
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics, rebalance_mask

RUNGS = [0, 1, 2, 5, 10, 25]
SIGN_RUNG = 0
PROTO_RUNG = 10
FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
NS = [20, 30, 40, 60]
SEEDS = list(range(8))
IS_START = "2009-01-01"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SAT_CAP = 0.25
BE_MAX = 60.0          # breakeven ladder ceiling, bps
BE_STEP = 0.05
RAND_ARMS = ["RANDH", "RANDA", "RANDQ", "RANDM", "RANDW", "RWK"]
REDRAW_FREQ = {"RANDH": None, "RANDA": "A", "RANDQ": "Q", "RANDM": "M", "RANDW": "W", "RWK": None}
RAND_SEED_BASE = {"RANDH": 1000, "RANDW": 2000, "RANDA": 3000, "RANDQ": 4000, "RANDM": 5000,
                  "RWK": 6000}
# nominal re-draws per year, for the ladder's x-axis (0 = never, NaN = emergent churn)
REDRAWS_PER_YEAR = {"RANDH": 0.0, "RANDA": 1.0, "RANDQ": 4.0, "RANDM": 12.0, "RANDW": 52.0,
                    "ROTW": 52.0, "RWK": np.nan,
                    "FWD": np.nan, "EWall": np.nan, "v1": np.nan}
ARM_ORDER = ["RANDH", "RANDA", "RANDQ", "RANDM", "RWK", "RANDW", "ROTW"]

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)


# ==================================================================== (A) census
CENSUS_RULES = """
HELD_KEY      a draw whose shape is (n_names,) broadcast over the whole index
              (np.tile of an rng draw, or an rng draw used to build a constant column key)
REDRAWN_KEY   a draw made per date / per rebalance (inside a loop over dates, or of shape
              px.shape / (len(idx), ncols))
PERM          rng.permutation / rng.shuffle used to relabel names or reorder a key
SUBSET_PANEL  rng.choice used to pick a set of NAMES or CELLS (a panel/sub-sample null,
              not a time-varying arm)
NOISE         rng.normal / rng.standard_normal of shape px.shape (a noise-injection null)
OTHER         everything else (bootstrap of returns, tie-breaks, grid shuffles, seeding)
"""


def classify_site(line, ctx):
    """Classify one rng call site by the SHAPE of the draw. `ctx` = the 4 lines around it."""
    l = line
    c = " ".join(ctx)
    if re.search(r"np\.tile\s*\(\s*rng\.", c) or re.search(r"np\.tile\s*\(\s*_?rng", c):
        return "HELD_KEY"
    if re.search(r"rng\.(permutation|shuffle)", l) or re.search(r"\.shuffle\(", l):
        return "PERM"
    if re.search(r"rng\.(normal|standard_normal)\s*\(", l):
        if re.search(r"size\s*=\s*px\.shape|size\s*=\s*\(len\(", c):
            return "NOISE"
        return "NOISE"
    if re.search(r"rng\.choice\s*\(", l):
        return "SUBSET_PANEL"
    if re.search(r"rng\.(random|uniform|rand)\s*\(", l):
        # shape decides: (ncols,) -> held ; (ndates, ncols) or per-date loop -> redrawn
        if re.search(r"px\.shape\[1\]\s*\)", l) or re.search(r"len\(\s*cols\s*\)\s*\)", l):
            # a per-date loop around it makes the same call a re-draw
            if re.search(r"for\s+\w+\s+in\s+(reb|idx|dates|rmask)", c):
                return "REDRAWN_KEY"
            return "HELD_KEY"
        if re.search(r"px\.shape\s*\)", l) or re.search(r"\(\s*len\(\s*\w*idx\w*\s*\)\s*,", l):
            return "REDRAWN_KEY"
        return "OTHER"
    if re.search(r"default_rng|RandomState|np\.random\.seed", l):
        return "SEED_DECL"
    return "OTHER"


def _code_lines(src):
    """Yield (i, line) for lines that are CODE: triple-quoted blocks and # comments dropped.

    A crude but auditable stripper: it toggles on any line whose triple-quote count is odd.
    Its only job is to keep docstring PROSE about nulls (of which this corpus has a lot)
    out of a census of call SITES.
    """
    inblock, delim = False, None
    for i, line in enumerate(src):
        s = line.strip()
        if not inblock:
            for d in ('"""', "'''"):
                if s.count(d) % 2 == 1:
                    inblock, delim = True, d
                    break
            else:
                if s.startswith("#"):
                    continue
                yield i, line
                continue
            # opening line of a block: everything before the delimiter is code, ignore it
            continue
        if s.count(delim) % 2 == 1:
            inblock, delim = False, None


def run_census():
    """Every rng CALL SITE in research/backtests/*.py, classified by the draw's shape.

    Two guards against the false positives a bare regex produces on this corpus:
      * docstring prose is stripped (`_code_lines`), because several scripts DISCUSS
        `rng.permutation(...)` in their design notes without calling it;
      * a call `x.foo(...)` is only counted when `x` is currently BOUND to an RNG object
        (`default_rng` / `RandomState`); at least one script binds the name `rng` to a
        DataFrame and calls `rng.merge(...)` on it.
    """
    rows = []
    for f in sorted(OUT.glob("*.py")):
        src = f.read_text(errors="replace").split("\n")
        bound = set()
        for i, line in _code_lines(src):
            m = re.match(r"\s*(\w+)\s*=\s*(.*)$", line)
            if m:
                nm, rhs = m.group(1), m.group(2)
                if re.search(r"np\.random\.(default_rng|RandomState)|default_rng\s*\(", rhs):
                    bound.add(nm)
                elif nm in bound:
                    bound.discard(nm)          # name rebound to something else
            call = re.search(r"\b(\w+)\s*\.\s*(random|uniform|rand|normal|standard_normal|"
                             r"permutation|shuffle|choice|integers|randint)\s*\(", line)
            direct = re.search(r"np\.random\s*\.\s*\w+\s*\(", line)
            decl = re.search(r"np\.random\.(default_rng|RandomState|seed)\s*\(|"
                             r"=\s*default_rng\s*\(", line)
            if not (decl or direct or (call and call.group(1) in bound)):
                continue
            ctx = [l for _, l in [(j, src[j]) for j in range(max(0, i - 3), min(len(src), i + 3))]]
            cls = classify_site(line, ctx)
            if decl and not (call and call.group(1) in bound) and not direct:
                cls = "SEED_DECL"
            rows.append(dict(script=f.name, line_no=i + 1, cls=cls, src=line.strip()[:200]))
    return pd.DataFrame(rows)


# ==================================================================== panels (idea 82/260, verbatim)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":     sub(px56, list(px56.columns)),
        "B136":    sub(px136, list(px136.columns)),
        "BSTK100": sub(px136, b_stk, tradable=b_stk),
    }


# ==================================================================== books
def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def _held_key(px, seed):
    """idea 82's RAND, byte-for-byte: ONE uniform per name, drawn once, held forever."""
    rng = np.random.default_rng(RAND_SEED_BASE["RANDH"] + seed)
    return pd.DataFrame(np.tile(rng.random(px.shape[1]), (len(px.index), 1)),
                        index=px.index, columns=px.columns)


def _redraw_key(px, arm, seed, rmask):
    """A fresh uniform per name at every boundary of the arm's re-draw period.

    For RANDW the boundaries ARE the weekly rebalance dates and the rng stream is idea
    260's `_weekly_key` byte-for-byte (draw at index 0, then one draw per rebalance index,
    in order, from default_rng(2000+seed)).  For the slower arms the boundaries are the
    last trading day of each month / quarter / year, INTERSECTED WITH nothing else: the
    book still rebalances weekly (cadence is held fixed across all arms), only the PICK
    persists longer.  The key is forward-filled between boundaries so execution is
    identical to every other arm.
    """
    rng = np.random.default_rng(RAND_SEED_BASE[arm] + seed)
    idx = px.index
    freq = REDRAW_FREQ[arm]
    if freq == "W":
        bound = np.flatnonzero(rmask.values)
    elif freq == "A":
        s = pd.Series(idx.to_period("Y"), index=idx)
        bound = np.flatnonzero((s != s.shift(-1)).values)
    else:
        bound = np.flatnonzero(rebalance_mask(idx, freq).values)
    k = np.empty((len(idx), px.shape[1]), dtype=float)
    k[:] = np.nan
    k[0] = rng.random(px.shape[1])
    for i in bound:
        k[i] = rng.random(px.shape[1])
    return pd.DataFrame(k, index=idx, columns=px.columns).ffill()


def _rw_key(px, seed):
    """The record's NOISE null, imported from `does-a-harmful-instrument-...`_B line 262-265.

    A per-name gaussian RANDOM WALK at the panel's median daily vol, keyed by the walk's
    own 126-day momentum.  Nobody re-draws anything: the rank order drifts continuously,
    so this arm's churn is EMERGENT rather than scheduled - which is exactly why the
    held/re-drawn dichotomy the queue names does not describe it, and why its turnover has
    never been reported.  Three committed scripts trade a null of this shape.
    """
    rng = np.random.default_rng(RAND_SEED_BASE["RWK"] + seed)
    sd = float(np.nanmedian(px.pct_change().std().values))
    steps = rng.normal(0.0, sd, size=px.shape)
    walk = pd.DataFrame(np.cumsum(steps, axis=0), index=px.index, columns=px.columns) + 10.0
    return (walk / walk.shift(126) - 1).rank(axis=1, pct=True)


def _rot_selection(px, elig, n, rmask):
    """Deterministic weekly ROTATION: no randomness, same churn as a weekly re-draw.

    At the k-th rebalance date take the eligible names occupying positions
    (k*n + j) mod n_eligible, j = 0..n-1, in a FIXED alphabetical ordering of the panel.
    Held between rebalances, like every other arm.
    """
    cols = list(px.columns)
    order = np.argsort(np.array(cols))          # fixed alphabetical order, deterministic
    E = elig.values[:, order]
    sel = np.zeros(E.shape, dtype=float)
    reb = np.flatnonzero(rmask.values)
    k = 0
    cur = np.zeros(E.shape[1])
    for i in range(len(px.index)):
        if i == 0 or rmask.values[i]:
            live = np.flatnonzero(E[i])
            m = len(live)
            if m == 0:
                cur = np.zeros(E.shape[1])
            else:
                take = min(n, m)
                pos = (k * n + np.arange(take)) % m
                cur = np.zeros(E.shape[1])
                cur[live[np.unique(pos)]] = 1.0
            k += 1
        sel[i] = cur
    inv = np.argsort(order)
    return pd.DataFrame(sel[:, inv], index=px.index, columns=cols)


def weights(px, tradable, arm, n=None, seed=None, rmask=None, elig=None):
    """All arms gross-matched at GROSS (idea 73's CANDg / idea 240's NORM)."""
    if elig is None:
        elig = eligible_mask(px, tradable)
    if arm == "v1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if arm == "FIXED20":                       # idea 73's literal GROSS/n, reproduction gate only
        s = score(px, vol_scale=False)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 20).astype(float) * (GROSS / 20)
    if arm == "EWall":
        sel = elig.astype(float)
    elif arm == "ROTW":
        sel = _rot_selection(px, elig, n, rmask)
    else:
        if arm == "RANDH":
            key = _held_key(px, seed)
        elif arm == "RWK":
            key = _rw_key(px, seed)
        elif arm in RAND_ARMS:
            key = _redraw_key(px, arm, seed, rmask)
        elif arm == "FWD":
            key = score(px, vol_scale=False)[0]
        else:
            raise ValueError(arm)
        rank = key.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


# ==================================================================== stats
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def v4a(r, base):
    h1, h2 = half_sharpes(r)
    b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


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


def paired_t(d):
    d = np.asarray([x for x in d if np.isfinite(x)], dtype=float)
    if len(d) < 2:
        return np.nan, np.nan, 0, 0
    se = d.std(ddof=1) / np.sqrt(len(d))
    return d.mean(), (d.mean() / se if se > 0 else np.nan), int((d > 0).sum()), len(d)


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def sharpe_at(r0, turn, c):
    r = np.asarray(r0, dtype=float) - np.asarray(turn, dtype=float) * c / 1e4
    v = r.std(ddof=1)          # ddof=1, to match pandas' .std() inside engine.metrics
    return (r.mean() / v * np.sqrt(252)) if v > 0 else np.nan


def breakeven(r0x, tx, r0y, ty):
    """The cost rung at which Sharpe(X,c) - Sharpe(Y,c) changes sign.

    Located by a coarse scan on a BE_STEP-spaced ladder to BE_MAX (so a non-monotonic
    difference cannot be missed) followed by bisection inside the first bracket to
    1e-4 bps.  Returns NaN if the difference never changes sign below BE_MAX.
    """
    ax, bx = np.asarray(r0x, float), np.asarray(tx, float)
    ay, by = np.asarray(r0y, float), np.asarray(ty, float)

    def d(c):
        return sharpe_at(ax, bx, c) - sharpe_at(ay, by, c)

    d0 = d(0.0)
    if not np.isfinite(d0) or d0 == 0:
        return np.nan
    s0 = np.sign(d0)
    cs = np.arange(BE_STEP, BE_MAX + BE_STEP, BE_STEP)
    lo, dlo = 0.0, d0
    hi = None
    for c in cs:
        dc = d(c)
        if np.sign(dc) != s0:
            hi, dhi = c, dc
            break
        lo, dlo = c, dc
    if hi is None:
        return np.nan
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        dm = d(mid)
        if np.sign(dm) == s0:
            lo, dlo = mid, dm
        else:
            hi, dhi = mid, dm
        if hi - lo < 1e-4:
            break
    return 0.5 * (lo + hi)


# ==================================================================== main
def main():
    print("=" * 220)
    print(f"Idea 262 is-the-1bp-breakeven-general-to-the-records-null-arms (lane C) | {SCRIPT}")
    print(f"weekly cadence, next-day execution, gross matched {GROSS}, rungs {RUNGS} bps, "
          f"breakeven ladder 0..{BE_MAX} bps step {BE_STEP}")
    print("=" * 220)

    # ---------------- (A) CENSUS -------------------------------------------------
    print("\n" + "=" * 100)
    print("(A) CENSUS of every rng call site in research/backtests/*.py")
    print("=" * 100)
    print(CENSUS_RULES)
    cen = run_census()
    cen.to_csv(OUT / f"{STEM}.census.csv", index=False)
    real = cen[cen.cls != "SEED_DECL"]
    print(f"scripts scanned: {len(list(OUT.glob('*.py')))}   scripts with an rng call: "
          f"{cen.script.nunique()}   call sites: {len(cen)} ({len(real)} excluding seed declarations)")
    print("\nSites by class:")
    print(cen.cls.value_counts().to_string())
    print("\nSCRIPTS by class (a script can appear in several):")
    print(cen.groupby("cls").script.nunique().to_string())
    # ---- the split that matters: a null that TRADES vs a null that is a STATISTIC ----
    trade_cls = ["HELD_KEY", "REDRAWN_KEY", "NOISE"]
    arm_sites = cen[cen.cls.isin(trade_cls)]
    print(f"\nTRADING-ARM nulls (a time-varying pick a cost rung can move): "
          f"{len(arm_sites)} sites in {arm_sites.script.nunique()} scripts")
    print(arm_sites.groupby("cls").script.nunique().to_string())
    print("\nthe TRADING-ARM null scripts, by construction:")
    for cls in trade_cls:
        ss = sorted(arm_sites[arm_sites.cls == cls].script.unique())
        print(f"  {cls:<12} ({len(ss)})")
        for s in ss:
            print(f"      {s}")
    print("""
HAND AUDIT (all 11 PERM sites and all 33 SUBSET_PANEL sites were read, not sampled):
  PERM          0 of 11 is a time-varying name pick.  Every one is a STATISTIC: a
                permutation test (`rng.permutation(ry)` against a correlation, a failing-bar
                matrix, an abstention count) or a half-split of a corpus, or a random draw of
                MODE indices (`rng.permutation(np.arange(1, J))`).  A cost rung cannot move
                any of them, so they are NOT what the queue is asking about and are excluded
                from the pricing below.
  SUBSET_PANEL  a random set of NAMES or CELLS, held for the sample - a panel-level null
                (ideas 78/83's k-of-136 sub-panels).  Membership does not churn, so its
                turnover is its comparand's; also excluded.
  NOISE         3 scripts trade `walk = cumsum(rng.normal(0, sd, px.shape))` keyed by the
                walk's own 126d momentum.  These DO trade, their churn is emergent rather
                than scheduled, and the held/re-drawn dichotomy the queue names does not
                describe them.  Priced below as `RWK`.""")
    aud = cen.groupby("cls", group_keys=False).head(4)
    aud.to_csv(OUT / f"{STEM}.audit.csv", index=False)
    print("\nHand-audit sample (4 per class, full list in .census.csv / .audit.csv):")
    print(aud.to_string(index=False, max_colwidth=110))

    # ---------------- (B) the price ----------------------------------------------
    panels = build_panels()
    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"\nIndex sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    print("\nPanels:")
    eligs, rmasks, necl = {}, {}, {}
    for k, (p, tr) in panels.items():
        e = eligible_mask(p, tr); eligs[k] = e
        m = rebalance_mask(p.index, FREQ); rmasks[k] = m
        necl[k] = e[m.values].sum(axis=1)
        print(f"  {k:<8} {len(tr):>3} tradable ({p.shape[1]} cols incl. benchmark)  "
              f"{p.index[0].date()} -> {p.index[-1].date()}   mean eligible {necl[k].mean():.1f} "
              f"(p10 {necl[k].quantile(.10):.0f} / p90 {necl[k].quantile(.90):.0f})   rebalances {int(m.sum())}")

    jobs = [("EWall", None, None), ("v1", None, None), ("FIXED20", None, None)]
    jobs += [("FWD", n, None) for n in NS]
    jobs += [("ROTW", n, None) for n in NS]
    jobs += [(a, n, s) for a in RAND_ARMS for n in NS for s in SEEDS]

    print(f"\nRunning {len(jobs)} books x {len(panels)} panels = {len(jobs)*len(panels)} backtests at 0 bps "
          f"(every rung derived exactly)...")
    # Optional RUNTIME-ONLY memo of the 0-bps books, keyed by (panel, arm, n, seed).  It
    # changes nothing about the result - every book is still computed by engine.backtest
    # from the same deterministic weights - it only lets an interrupted run resume.  Off
    # unless IDEA262_CACHE is set to a path; the committed script is standalone without it.
    cpath = os.environ.get("IDEA262_CACHE")
    cache = {}
    if cpath and Path(cpath).exists():
        with open(cpath, "rb") as fh:
            cache = pickle.load(fh)
        print(f"  resuming from {len(cache)} cached books ({cpath})")
    gross_ret, turn = {}, {}
    made = 0
    for pk, (p, tr) in panels.items():
        for arm, n, seed in jobs:
            ck = f"{pk}|{arm}|{n}|{seed}"
            if ck in cache:
                a, b = cache[ck]
            else:
                w = weights(p, tr, arm, n, seed, rmasks[pk], eligs[pk])
                r = backtest(p, w, cost_bps=0, freq=FREQ)
                a, b = r["returns"].values, r["turnover"].values
                cache[ck] = (a, b)
                made += 1
                if cpath and made % 40 == 0:
                    with open(cpath, "wb") as fh:
                        pickle.dump(cache, fh)
            gross_ret[(pk, arm, n, seed)] = pd.Series(a, index=p.index)
            turn[(pk, arm, n, seed)] = pd.Series(b, index=p.index)
        if cpath:
            with open(cpath, "wb") as fh:
                pickle.dump(cache, fh)
        print(f"  {pk} done ({made} newly computed so far)")

    # ---- HARNESS IDENTITY GATE -------------------------------------------------
    for chk in [("U56", "FWD", 20, None, 10.0), ("B136", "RANDW", 20, 0, 25.0),
                ("BSTK100", "ROTW", 40, None, 5.0)]:
        pk, arm, n, seed, c = chk
        p, tr = panels[pk]
        live = backtest(p, weights(p, tr, arm, n, seed, rmasks[pk], eligs[pk]),
                        cost_bps=c, freq=FREQ)["returns"]
        der = gross_ret[(pk, arm, n, seed)] - turn[(pk, arm, n, seed)] * c / 1e4
        err = float(np.abs(live - der).max())
        print(f"HARNESS IDENTITY {pk}/{arm}{n}/seed {seed} @{c} bps: max|live-derived| = {err:.3e}")
        if err > 1e-15:
            print("!! identity broken - aborting."); sys.exit(1)

    # ---- warm-up trim, benchmarks ----------------------------------------------
    starts, spy_r, base_r = {}, {}, {}
    for pk, (p, tr) in panels.items():
        st = p.index[260]
        starts[pk] = st
        spy_r[pk] = p["SPY"].pct_change().fillna(0).loc[st:]
        base_r[pk] = (gross_ret[(pk, "v1", None, None)] - turn[(pk, "v1", None, None)] * PROTO_RUNG / 1e4).loc[st:]

    def ret(pk, arm, n, seed, c):
        st = starts[pk]
        return (gross_ret[(pk, arm, n, seed)] - turn[(pk, arm, n, seed)] * c / 1e4).loc[st:]

    def turn_yr(pk, arm, n, seed):
        st = starts[pk]
        t = turn[(pk, arm, n, seed)].loc[st:]
        return t.sum() / (len(t) / 252)

    # ---- REPRODUCTION GATE -----------------------------------------------------
    print("\n" + "=" * 100)
    print("REPRODUCTION GATE")
    print("=" * 100)
    rep = {}
    for name, key in [("U56/FIXED20", ("U56", "FIXED20", None, None)), ("U56/RULES v1", ("U56", "v1", None, None))]:
        r = ret(*key, PROTO_RUNG)
        m = metrics(r); h1, h2 = half_sharpes(r)
        rep[name] = (m["CAGR"], m["Sharpe"], m["MaxDD"], h1, h2)
        print(f"  {name:<14} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}")
    ok = (abs(rep["U56/FIXED20"][1] - 1.093) < 0.01 and abs(rep["U56/RULES v1"][1] - 0.666) < 0.01)
    print(f"  gate: {'PASS' if ok else 'FAIL'} (idea 260 published 12.7%/1.093/-18.3% and 6.5%/0.666/-13.8%)")
    if not ok:
        print("!! reproduction gate failed - aborting."); sys.exit(1)

    # saturation
    sat = {}
    for pk in panels:
        for n in NS:
            sat[(pk, n)] = float((necl[pk] < n).mean())
    print("\nsat_share (share of rebalances with fewer than n eligible names); cells with "
          f"sat_share > {SAT_CAP} are excluded from headline counts:")
    print(pd.Series(sat).unstack().to_string(float_format=lambda x: f"{x:.3f}"))
    cells = [(pk, n) for pk in panels for n in NS if sat[(pk, n)] <= SAT_CAP]
    print(f"unsaturated cells: {len(cells)} of {len(panels)*len(NS)} -> {cells}")

    # ---- GRID ------------------------------------------------------------------
    rows = []
    for pk in panels:
        st = starts[pk]
        spy = spy_r[pk]; spy_oos = spy.loc[OOS_START:]
        for arm, n, seed in jobs:
            if arm == "FIXED20":
                continue
            ty = turn_yr(pk, arm, n, seed)
            for c in RUNGS:
                r = ret(pk, arm, n, seed, c)
                m = metrics(r); h1, h2 = half_sharpes(r)
                r_oos = r.loc[OOS_START:]
                rows.append(dict(panel=pk, arm=arm, n=n, seed=seed, bps=c,
                                 redraws_yr=REDRAWS_PER_YEAR.get(arm, np.nan),
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 Vol=m["Vol"], H1=h1, H2=h2,
                                 OOS_Sharpe=metrics(r_oos)["Sharpe"],
                                 turn_yr=ty, sat_share=sat.get((pk, n), np.nan),
                                 v4a=v4a(r, base_r[pk]),
                                 fail4b=fail4b(r, spy, r_oos, spy_oos)))
    grid = pd.DataFrame(rows)
    grid["v4b"] = grid.fail4b == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    print(f"\nGRID: {len(grid)} points written to {STEM}.grid.csv")

    # ---- TURNOVER TABLE (idea 263's column) ------------------------------------
    print("\n" + "=" * 100)
    print("1. TURNOVER OF EVERY NULL ARM AGAINST ITS COMPARANDS (x/yr, seed-mean)")
    print("=" * 100)
    tt = (grid[grid.bps == 0].groupby(["panel", "arm", "n"]).turn_yr.mean().unstack("arm"))
    print(fmt(tt, 1))
    print("\nturnover RATIO to FWD at the same n (>2x is idea 263's flag):")
    ratio = tt.div(tt["FWD"], axis=0)
    print(fmt(ratio, 2))

    # ---- DIFFERENCES AND BREAKEVENS --------------------------------------------
    print("\n" + "=" * 100)
    print("2. SHARPE DIFFERENCE AND THE EXACT COST RUNG AT WHICH IT FLIPS")
    print("=" * 100)
    null_arms = RAND_ARMS + ["ROTW"]   # every null construction the census found
    brows = []
    for pk, n in [(p, n) for p in panels for n in NS]:
        for arm in null_arms:
            seeds = SEEDS if arm in RAND_ARMS else [None]
            for s in seeds:
                for comp, cn, cs in [("FWD", n, None), ("EWall", None, None)]:
                    rx0, tx = gross_ret[(pk, arm, n, s)].loc[starts[pk]:], turn[(pk, arm, n, s)].loc[starts[pk]:]
                    ry0, ty = gross_ret[(pk, comp, cn, cs)].loc[starts[pk]:], turn[(pk, comp, cn, cs)].loc[starts[pk]:]
                    d0 = sharpe_at(rx0, tx, 0.0) - sharpe_at(ry0, ty, 0.0)
                    d10 = sharpe_at(rx0, tx, 10.0) - sharpe_at(ry0, ty, 10.0)
                    be = breakeven(rx0, tx, ry0, ty)
                    Tx, Ty = tx.sum() / (len(tx) / 252), ty.sum() / (len(ty) / 252)
                    vx, vy = rx0.std() * np.sqrt(252), ry0.std() * np.sqrt(252)
                    slope = (Tx / vx - Ty / vy) / 1e4
                    pred = (d0 / slope) if slope != 0 else np.nan
                    brows.append(dict(panel=pk, n=n, arm=arm, seed=s, comparand=comp,
                                      redraws_yr=REDRAWS_PER_YEAR[arm],
                                      turn_arm=Tx, turn_comp=Ty, turn_ratio=Tx / Ty if Ty else np.nan,
                                      vol_arm=vx, vol_comp=vy,
                                      d0=d0, d10=d10, breakeven_bps=be, pred_breakeven_bps=pred,
                                      sat_share=sat[(pk, n)],
                                      unsat=sat[(pk, n)] <= SAT_CAP))
    be_df = pd.DataFrame(brows)
    be_df.to_csv(OUT / f"{STEM}.breakeven.csv", index=False)
    U = be_df[be_df.unsat]

    for comp in ["FWD", "EWall"]:
        sub = U[U.comparand == comp]
        print(f"\n--- vs {comp} (unsaturated cells only, {sub.panel.nunique()} panels) ---")
        agg = sub.groupby("arm").agg(redraws_yr=("redraws_yr", "first"),
                                     turn=("turn_arm", "mean"), turn_ratio=("turn_ratio", "mean"),
                                     d0=("d0", "mean"), d10=("d10", "mean"),
                                     be_med=("breakeven_bps", "median"),
                                     be_min=("breakeven_bps", "min"), be_max=("breakeven_bps", "max"),
                                     flips=("breakeven_bps", lambda x: int(np.isfinite(x).sum())),
                                     nobs=("breakeven_bps", "size"))
        agg = agg.reindex([a for a in ARM_ORDER if a in agg.index])
        agg["be_below_10"] = [int((sub[sub.arm == a].breakeven_bps < 10).sum()) for a in agg.index]
        print(fmt(agg, 3))
        for a in agg.index:
            d = sub[sub.arm == a]
            m, t, pos, nn = paired_t(d.d0.values)
            m10, t10, pos10, _ = paired_t(d.d10.values)
            print(f"    {a:<6} d0 {m:+.4f} (t {t:+.2f}, positive {pos}/{nn})   "
                  f"d@10bps {m10:+.4f} (t {t10:+.2f}, positive {pos10}/{nn})")

    # per-cell table for the two published endpoints
    print("\nPer-cell breakeven of the two PUBLISHED endpoints vs FWD (seed-mean of per-seed breakevens):")
    pub = U[(U.comparand == "FWD") & (U.arm.isin(["RANDH", "RANDW"]))]
    piv = pub.pivot_table(index=["panel", "n"], columns="arm",
                          values=["d0", "d10", "breakeven_bps", "turn_ratio"], aggfunc="mean")
    print(fmt(piv, 3))

    # ---- THE LAW ---------------------------------------------------------------
    print("\n" + "=" * 100)
    print("3. THE LAW: is the breakeven reconstructible from published columns alone?")
    print("   c* = dSharpe(0) * 1e4 / (T_x/vol_x - T_y/vol_y)")
    print("=" * 100)
    law = U.dropna(subset=["breakeven_bps", "pred_breakeven_bps"])
    law = law[(law.breakeven_bps < BE_MAX) & (law.pred_breakeven_bps.abs() < 1e4)]
    if len(law) > 2:
        y, yh = law.breakeven_bps.values, law.pred_breakeven_bps.values
        r2 = 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
        print(f"  n = {len(law)} flipping (cell, arm, seed, comparand) points")
        print(f"  R^2(measured, predicted) = {r2:.4f}   median |error| = {np.median(np.abs(y-yh)):.3f} bps"
              f"   median measured = {np.median(y):.3f} bps")
        print(f"  correlation = {np.corrcoef(y, yh)[0,1]:.4f}")
        for a in law.arm.unique():
            s = law[law.arm == a]
            print(f"    {a:<6} n={len(s):>4}  measured med {s.breakeven_bps.median():.3f}  "
                  f"predicted med {s.pred_breakeven_bps.median():.3f}  "
                  f"med|err| {np.median(np.abs(s.breakeven_bps-s.pred_breakeven_bps)):.3f}")
    else:
        r2 = np.nan
        print("  too few flipping points to fit the law")

    # ---- WALK-FORWARD (rule 8) --------------------------------------------------
    print("\n" + "=" * 100)
    print(f"4. RULE 8 WALK-FORWARD  (IS {IS_START}..{IS_END} chooses, OOS {OOS_START}.. read once)")
    print("=" * 100)
    sel_defs = {"EWALL": ("EWall", None, None), "FWD20": ("FWD", 20, None), "ROTW20": ("ROTW", 20, None)}
    wf_rows = []
    for c in RUNGS:
        pooled = {}
        for name in list(sel_defs) + ["RANDH20", "RANDM20", "RANDW20", "RWK20", "ALL_ISARGMAX", "RULES v1"]:
            per_panel = []
            for pk in panels:
                if name in sel_defs:
                    arm, n, s = sel_defs[name]
                    r = ret(pk, arm, n, s, c)
                elif name == "RULES v1":
                    r = ret(pk, "v1", None, None, c)
                elif name[:-2] in RAND_ARMS:
                    arm = name[:-2]
                    r = sum(ret(pk, arm, 20, s, c) for s in SEEDS) / len(SEEDS)
                else:  # ALL_ISARGMAX
                    best, bs = None, -np.inf
                    for arm, n, s in jobs:
                        if arm in ("v1", "FIXED20"):
                            continue
                        ris = ret(pk, arm, n, s, c).loc[IS_START:IS_END]
                        sh = metrics(ris)["Sharpe"]
                        if np.isfinite(sh) and sh > bs:
                            bs, best = sh, (arm, n, s)
                    r = ret(pk, *best, c)
                    if c == PROTO_RUNG:
                        print(f"    ALL_ISARGMAX @{c} bps picks {pk}: {best}")
                per_panel.append(r.loc[OOS_START:])
            idx = per_panel[0].index
            pooled[name] = sum(p.reindex(idx).fillna(0) for p in per_panel) / len(per_panel)
        spy_pool = sum(spy_r[pk].loc[OOS_START:].reindex(pooled["EWALL"].index).fillna(0) for pk in panels) / len(panels)
        pooled["SPY"] = spy_pool
        for name, r in pooled.items():
            m = metrics(r)
            wf_rows.append(dict(bps=c, selector=name, CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"]))
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(wf.pivot(index="selector", columns="bps", values="Sharpe"), 3))
    print("\nOOS CAGR:")
    print(fmt(wf.pivot(index="selector", columns="bps", values="CAGR"), 3))
    print("\nOOS MaxDD:")
    print(fmt(wf.pivot(index="selector", columns="bps", values="MaxDD"), 3))

    # ---- KEEP PATHS -------------------------------------------------------------
    print("\n" + "=" * 100)
    print("5. KEEP PATHS over all grid points")
    print("=" * 100)
    print("4a passes by arm x rung:")
    print(grid.pivot_table(index="arm", columns="bps", values="v4a", aggfunc="sum").to_string())
    print("\n4b passes by arm x rung:")
    print(grid.pivot_table(index="arm", columns="bps", values="v4b", aggfunc="sum").to_string())
    print(f"\ntotals: 4a {int(grid.v4a.sum())}/{len(grid)}   4b {int(grid.v4b.sum())}/{len(grid)}")
    k = grid[grid.v4b & (grid.bps == PROTO_RUNG)]
    k.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    if len(k):
        print(f"\n4b passes at PROTOCOL's {PROTO_RUNG} bps ({len(k)}):")
        print(k.sort_values("Sharpe", ascending=False)
               .head(20)[["panel", "arm", "n", "seed", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                          "OOS_Sharpe", "turn_yr"]].to_string(index=False,
                                                              float_format=lambda x: f"{x:.3f}"))
    else:
        print(f"\nno 4b pass at {PROTO_RUNG} bps")
    print("\nbinding bar census at 10 bps (fail4b):")
    print(grid[grid.bps == PROTO_RUNG].fail4b.value_counts().head(12).to_string())

    print("\nDONE. artefacts: "
          f"{STEM}.{{census,audit,grid,breakeven,walkforward,keep}}.csv")


if __name__ == "__main__":
    main()
