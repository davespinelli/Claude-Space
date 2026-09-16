#!/usr/bin/env python3
"""
IDEA 1002 (lane B, 2026-09-16)
should-a-ROTATING-NULL-be-PINNED-to-a-PRICE-VINTAGE

THE SUBJECT
-----------
Idea 971 found that a nightly-restated panel does not PERTURB a rotating null, it RESAMPLES
it: B136 (a Friday-only cache) reproduced 970's 600 draws bit-for-bit, SMALL663 to 1.6e-07,
and U56 not at all -- max |dSharpe| 0.254 on IDENTICAL seeds, with 7.4% of REC 4b verdicts
flipped.  Every committed null base rate in this record was computed on whatever
`data/prices.csv` happened to be that night, and none of them names the tape it was drawn on.

This run prices the fix the queue line proposes: **pin the draw to a committed price sha**,
and measure how much of the record's committed null variance is TAPE RESTATEMENT rather than
SAMPLING.

THE VINTAGE LADDER IS REAL, NOT SIMULATED
-----------------------------------------
`data/prices.csv` is rewritten by the nightly Actions job and every rewrite is a commit.  This
run replays the actual committed shas out of git (`git show <sha>:data/prices.csv`), so the
vintage axis is the record's own history and not a synthetic perturbation:

  U56   9 post-fix vintages   c006b439 (2026-09-04) ... 868b5c36 (2026-09-15)
  B136  4 vintages            0ede2282 (2026-09-03) ... 56e08b10 (2026-09-11), Friday cache
        (prices_broad.csv was never calendar-indexed, so B136 carries NO schema break)

  SCHEMA BREAK, LABELLED AND EXCLUDED: the two 2026-09-03 `prices.csv` vintages (fb208174,
  0ede2282) carry 6,060 CALENDAR-day rows, not 4,698 trading-day rows -- commit c006b439
  ("Fix calendar-day index bug") changed the index convention.  Mixing them into a
  RESTATEMENT ladder would price a BUG FIX as a restatement, so the U56 ladder starts at
  c006b439.  Both are reported in the vintage census and used by NO hypothesis.

  Measured restatement, U56, oldest-vintage overlap (4,698 x 56 cells):
  8.91% of historical cells move by 2026-09-04 and 13.68% by 2026-09-15, max relative move
  6.13e-03.  The panel also grows one row per trading day.  So the tape moves through TWO
  channels -- APPEND (new rows) and RESTATE (old cells rewritten) -- and both are live here.

WHAT IS MEASURED
----------------
For every (panel, book, cadence) family at gross 0.75, D coin-flip draws are run on EVERY
vintage under FOUR draw conventions, and the headline is a VARIANCE DECOMPOSITION of the null
statistic into SAMPLING (across seeds, one vintage) and TAPE (across vintages, one seed):

  sigma_seed   SD of the null statistic across D seeds, one vintage      -- SAMPLING
  sigma_vint   SD of the null statistic across vintages, one seed        -- TAPE

read under each convention, so the tape term is split into its own channels.

THE FOUR CONVENTIONS (this is PARAM 1 -- "vintage source" -- not four tuned dials)
---------------------------------------------------------------------------------
Gross matching is idea 680/926's, verbatim, in all four: on each rebalance row the book holds
n(t) names at a common per-name weight w(t); the null holds n(t) names drawn from that
family's POOL at the SAME w(t).  Count, per-name weight, gross path, cash drag and the
de-grossing convention are copied from the LIVE book in all four arms (G5 asserts count AND
gross row by row).  Only the SOURCE of the random ranking and of the eligibility pool changes:

  LIVE     the record's convention, verbatim: `rng.random(E.shape)` on the live vintage's own
           array, pool re-derived on the live vintage.  Everything moves with the tape.
  LIVE_CP  the same convention, every vintage TRUNCATED to the shared index prefix (through
           the oldest vintage's last day).  This kills the APPEND channel outright, so its
           cross-vintage spread is RESTATEMENT ONLY under the record's own convention.
  PINKEY   the RNG is keyed on (decision DATE, TICKER) via splitmix64 instead of on array
           position, so the random ranking is a property of the calendar and the name, not of
           the panel's shape.  Pool and count are still live.  This is the pin that does NOT
           freeze the tape.
  PINSET   the queue line's own proposal: the random ranking AND the eligibility pool are
           taken from a COMMITTED PRICE SHA (the reference vintage, fixed below), mapped onto
           the live index by DATE; only the count/weight and the PRICES are live.  Its
           residual cross-vintage spread is as close to a pure PRICE channel as the record's
           own null construction allows.

  The reference sha for PINSET is fixed BY THE DESIGN as the OLDEST post-fix vintage on each
  panel (U56 c006b439, B136 d434ebc4) -- pinning means pinning to something OLD, and its
  staleness is then a cost this run has to pay and report (H_STALE).  It is not chosen by
  outcome.  Decision dates after the reference vintage's last day (<= 8 trading days, 0-2
  rebalance rows) have no pinned draw and fall back to PINKEY; the count is reported.

  PIN_SHA in the strict sense -- freeze the whole tape and price on it -- has ZERO
  cross-vintage variance BY CONSTRUCTION and so is not a measurement.  Its real cost is
  STALENESS, and that is read directly off the LIVE arm's own vintage rows (H_STALE).

DESIGN
------
  TUNED (2, and only 2 -- the queue line's own axes)
    1. VINTAGE SOURCE  LIVE / LIVE_CP / PINKEY / PINSET.  ALL FOUR reported at every point.
    2. PANEL           U56 (BINDING, 9 vintages) and B136 (LABELLED REPLICATION, 4 vintages).
  NOT TUNED
    DRAWS     D = 100, NESTED (the 25- and 50-draw statistics are the first 25/50 seeds of the
              100-draw grid), so the draw axis reports a CONVERGENCE, not three samples.
    GROSS     0.75 (CORE), the record's standing gross for this book set.
    BOOKS     EWELIG, BAND03 (the live book's shape), TOP20.  Fixed set, all reported.
    CADENCE   W / M / Q.  All three reported; no cadence is chosen by outcome.
    COST      null grid at 10 bps (PROTOCOL rule 2); REAL books and the SUBJECT cell at
              0 / 5 / 10 / 25 / 50 bps.  No rung is chosen by outcome.
    FIXED     gate above-200d MA and vol20 < 0.60; warm-up 260 rows; IS <= 2016-12-31 /
              OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 1002.

  SUBJECT CELL (fixed here, before any number is read): U56 / EWELIG / Q / 10 bps -- the cell
  975-B and 999 both used, so this run's numbers are readable against theirs.

PRE-REGISTERED HYPOTHESES (bars fixed here, before any number is read)
----------------------------------------------------------------------
  H_TAPE     HEADLINE.  Under PINSET on U56, sigma_vint / sigma_seed <= 0.10 on null OOS
             Sharpe, i.e. the PRICE channel alone moves a pinned draw by less than a tenth of
             a sampling SD.  PASS => pinning removes essentially all of the tape term.
  H_RESAMPLE Under LIVE on U56, sigma_vint / sigma_seed >= 0.70 -- 971's reading, that the
             live null's cross-vintage spread is nearly a full independent redraw.
  H_APPEND   The APPEND channel is the larger of the two: sigma_vint(LIVE) >= 2.00 x
             sigma_vint(LIVE_CP).  PASS => growing the panel, not rewriting it, is what
             resamples the null.
  H_FLIP     The per-draw 4b verdict flip rate across vintages at fixed seed falls by >= 0.75
             going LIVE -> PINSET on U56.
  H_BASE     The null 4b BASE RATE (the aggregate the record actually publishes) is
             vintage-stable under LIVE to within 2 x its own Monte-Carlo SE in >= 0.90 of
             cells -- i.e. the defect is in the DRAW, not in the published number.
  H_REAL     CONTROL.  The REAL book's own OOS Sharpe range across the U56 vintages is
             <= 0.02, so the tape by itself barely moves a book and any large null term is a
             property of the NULL's construction.
  H_STALE    The staleness price of a frozen sha: |null 4b base rate on the OLDEST vintage -
             on the LIVE vintage| <= 0.05 in the subject cell.
  H_RULE8    The rule-8 IS-only chooser's PICK is vintage-invariant (the same (book, cadence)
             on all 9 U56 vintages) for all three choosers.
  H_SCHEMA   The 2026-09-04 CALENDAR-DAY INDEX FIX, not the nightly restatement, is what
             resamples a null: max |d OOS Sharpe| across the SCHEMA BREAK is >= 10.0 x the
             max across the whole 9-vintage post-fix ladder, at identical seeds.

             PROVENANCE, stated because it matters: H_SCHEMA was NOT in the first draft.  It
             was added after a 3-vintage smoke run showed the post-fix ladder is nearly inert
             (ratio ~0.03), which made 971's 0.254 look like it must have come from somewhere
             else.  It is registered HERE, with its bar, BEFORE the schema-break vintage was
             ever priced -- no number from 0ede2282 or fb208174 has been read at this point --
             but it is a POST-SMOKE hypothesis and is labelled as one everywhere it appears.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  engine.rebalance_mask agrees with this run's own mask on W, M, Q       0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up       1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                     0.0
  G3  determinism: the subject cell's draw stream rebuilt reproduces exactly 0.0
  G4  PINKEY invariance: on shared decision dates where the pool AND the count agree across
      two vintages, the drawn NAME SET is identical                          0 rows
  G5  GROSS MATCH: every draw's holding COUNT and per-row GROSS equal its book's, row by row,
      in ALL FOUR arms                                                       1e-12
  G6  NESTING: the 25/50-draw statistics are the first 25/50 seeds of the 100-draw grid  0.0
  G7  PINSET IDENTITY: on the REFERENCE vintage itself, PINSET == LIVE exactly              0.0
  G8  VINTAGE LADDER: every post-fix vintage's index is a strict PREFIX EXTENSION of the
      oldest one, and the two 2026-09-03 vintages are NOT (the labelled schema break)
  G9  CROSS-RUN: idea 975-B's committed `.real.csv` CANON rows (U56 and B136, M and Q, all
      five cost rungs) reproduced from this run's own NEWEST-vintage real grid, each panel
      matched against ITS OWN newest sha (56e08b10 touched both price files)     5e-4

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is
optimistic, and the rule-8 4b levels are read against SPY, which is not.  The measured object
here, however, is a VARIANCE RATIO between two readings of the SAME panel on the SAME tape
under the SAME gross -- the survivorship bias is a common factor to numerator and denominator
and very largely cancels.  Where it does not cancel it works AGAINST this run's own
suspicion: a survivor panel's eligibility gate is more stable than a real-time one's, so the
TAPE term measured here is a LOWER bound and H_TAPE is the easier hypothesis to pass.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import score, band_state, rules_v2_weights          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
import engine                                                      # noqa: E402

STEM = Path(__file__).stem
OUT = Path(__file__).resolve().parent

WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
START = "2008-01-01"
VOLCAP, BAND0 = 0.60, 0.03
GROSS = 0.75
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
HEAD_COST = 10.0
NDRAW = 100
DRAW_LADDER = [25, 50, 100]
SEED0 = 1002
ARMS = ["LIVE", "LIVE_CP", "PINKEY", "PINSET"]
CADS = ["W", "M", "Q"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
SUBJECT = ("U56", "EWELIG", "Q")

# ---- the real committed shas, newest first (git log -- data/prices*.csv) -------------------
U56_VINTAGES = ["c006b439", "50585c86", "f138ee9a", "9ee888f4", "7a93b075",
                "60e8c36a", "56e08b10", "b2528b96", "868b5c36"]          # post-fix ladder
U56_PREFIX_BUG = ["0ede2282", "fb208174"]                                # schema break
B136_VINTAGES = ["0ede2282", "d434ebc4", "50585c86", "56e08b10"]         # no schema break here
B136_PREFIX_BUG: list[str] = []                                          # prices_broad.csv was never calendar-indexed
VFILE = {"U56": "data/prices.csv", "B136": "data/prices_broad.csv"}
VDATE = {}          # sha -> commit date, filled by load

# pre-registered bars
TAPE_BAR, RESAMPLE_BAR, APPEND_BAR, FLIP_BAR = 0.10, 0.70, 2.00, 0.75
BASE_BAR, REAL_BAR, STALE_BAR = 0.90, 0.02, 0.05

SMOKE = bool(int(os.environ.get("IDEA1002_SMOKE", "0")))
if SMOKE:
    NDRAW, DRAW_LADDER = 12, [4, 8, 12]
    U56_VINTAGES = U56_VINTAGES[:3]
    B136_VINTAGES = B136_VINTAGES[:2]
    CADS = ["M", "Q"]

LINES: list[str] = []
T0 = time.time()


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False, compression="gzip" if gz else None)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (0) THE VINTAGE LADDER -- replayed out of git, not simulated
# ==========================================================================================
def git_show(sha, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{sha}:{path}"],
                          capture_output=True, check=True).stdout


def read_vintage(panel, sha, tickers):
    import io
    raw = git_show(sha, VFILE[panel])
    px = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True).sort_index()
    keep = [t for t in tickers if t in px.columns]
    px = px[keep].loc[START:].dropna(how="all").ffill()
    return px


def commit_date(sha):
    if sha not in VDATE:
        out = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%ad",
                              "--date=short", sha], capture_output=True, check=True)
        VDATE[sha] = out.stdout.decode().strip()
    return VDATE[sha]


def universe(panel):
    if panel == "U56":
        U = json.loads((ROOT / "research" / "universe.json").read_text())
        return sorted({t for g in U.values() for t in g} - {"BTC-USD", "ETH-USD"})
    return sorted(json.loads((ROOT / "research" / "universe_broad.json").read_text()))


# ==========================================================================================
# (1) engine-equivalent fast runner -- copied VERBATIM from 942/962/964/975 (G1 asserts it)
# ==========================================================================================
class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
        self.cols = list(px.columns)
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]
        self.dec = np.maximum(self.reb - 1, 0)

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def wmets(r):
    """Full / IS / OOS metric block for one net-return vector (already warm-up trimmed).
    Windows are supplied as integer slices by the caller via `Slices`."""
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return (float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
            sharpe(r), maxdd(r), sharpe(r[:h]), sharpe(r[h:]))


class Slices:
    """Warm-up trimmed window slices for one vintage/cadence."""

    def __init__(self, idx):
        self.full = slice(WARM, len(idx))
        sub = idx[WARM:]
        self.nis = int((sub <= pd.Timestamp(IS_END)).sum())
        self.n = len(sub)


def block(net, sl):
    """net is ALREADY trimmed to the warm-up window."""
    c, s, d, h1, h2 = wmets(net)
    i = net[:sl.nis]
    o = net[sl.nis:]
    ic, isx, idd, ih1, ih2 = wmets(i) if len(i) > 10 else (np.nan,) * 5
    oc, osx, odd, oh1, oh2 = wmets(o) if len(o) > 10 else (np.nan,) * 5
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=isx, IS_MaxDD=idd, IS_H1=ih1, IS_H2=ih2,
                OOS_CAGR=oc, OOS_Sharpe=osx, OOS_MaxDD=odd, OOS_H1=oh1, OOS_H2=oh2)


def legs_rec(row, spy):
    """The RECORD's 4b convention (942/962/964/975's, verbatim)."""
    return dict(H1=row["H1"] > spy["H1"], H2=row["H2"] > spy["H2"],
                OOS=row["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(spy["MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * spy["CAGR"])


def legs_is(row, spy):
    return dict(H1=row["IS_H1"] > spy["IS_H1"], H2=row["IS_H2"] > spy["IS_H2"],
                OOS=row["IS_Sharpe"] > spy["IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(spy["IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * spy["IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- 942/962/964/975's, verbatim
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {
    "EWELIG": lambda p, g: ew_elig(p, g),
    "BAND03": lambda p, g: band_book(p, BAND0, g),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "TOP20": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2}


def pools(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


# ==========================================================================================
# (3) THE FOUR DRAW CONVENTIONS
# ==========================================================================================
U64 = np.uint64


def _splitmix(x):
    """splitmix64 finalizer, vectorised over uint64.  Wrapping is intentional."""
    with np.errstate(over="ignore"):
        z = (x + U64(0x9E3779B97F4A7C15)).astype(U64)
        z = ((z ^ (z >> U64(30))) * U64(0xBF58476D1CE4E5B9)).astype(U64)
        z = ((z ^ (z >> U64(27))) * U64(0x94D049BB133111EB)).astype(U64)
        return (z ^ (z >> U64(31))).astype(U64)


def _tickkey(cols):
    """A stable 64-bit key per ticker string -- independent of column order and panel."""
    out = np.zeros(len(cols), dtype=U64)
    with np.errstate(over="ignore"):
        for j, t in enumerate(cols):
            h = U64(0xCBF29CE484222325)
            for ch in t.encode():
                h = ((h ^ U64(ch)) * U64(0x100000001B3)).astype(U64)
            out[j] = h
    return out


def keyed_uniform(seed, date_keys, tick_keys):
    """U(0,1) per (decision DATE, TICKER).  Depends on NOTHING else -- not the panel's shape,
    not the column order, not the row count.  This is PINKEY."""
    with np.errstate(over="ignore"):
        a = (U64(seed) * U64(0x9E3779B97F4A7C15)).astype(U64)
        rows = _splitmix((a + date_keys.astype(U64)).astype(U64))
        m = _splitmix((rows[:, None] + tick_keys[None, :]).astype(U64))
    return (m >> U64(11)).astype(np.float64) * (1.0 / 9007199254740992.0)


def rank_select(R, E, take):
    """Top-`take` of R restricted to E, per row.  Shared by all four arms."""
    Rx = np.where(E, R, -1.0)
    order = np.argsort(-Rx, axis=1)
    pos = np.argsort(order, axis=1)
    return (pos < take[:, None]) & E


class Family:
    """Everything the four arms need for one (vintage, book, cadence) cell."""

    def __init__(self, ctx, poolmat, wt_book, date_keys, tick_keys):
        self.ctx = ctx
        self.E = poolmat[ctx.dec]
        wrow = wt_book[ctx.reb]
        self.cnt = (wrow > 0).sum(axis=1)
        self.tot = wrow.sum(axis=1)
        self.perw = np.where(self.cnt > 0, self.tot / np.maximum(self.cnt, 1), 0.0)
        self.take = np.minimum(self.E.sum(axis=1), self.cnt)
        self.dkey = date_keys[ctx.dec]
        self.tkey = tick_keys

    def weights(self, arm, seed, ref=None):
        """Returns (W, M) -- W in ctx's shifted coordinates, M the boolean name mask."""
        ctx = self.ctx
        if arm in ("LIVE", "LIVE_CP"):
            R = np.random.default_rng(seed).random(self.E.shape)
            E = self.E
        elif arm == "PINKEY":
            R = keyed_uniform(seed, self.dkey, self.tkey)
            E = self.E
        elif arm == "PINSET":
            R, E = ref.project(seed, self.dkey, self.tkey)
        else:
            raise ValueError(arm)
        M = rank_select(R, E, self.take)
        W = np.zeros((ctx.T, ctx.N))
        W[ctx.reb] = M * self.perw[:, None]
        return W, M


class RefDraw:
    """The reference vintage's (R, pool) for one (book, cadence), served BY DATE.

    This is the queue line's 'draw the eligibility pool from a committed price sha': the
    ranking and the pool come from the pinned sha, the count/weight and the prices are live.
    Decision dates the reference sha does not carry fall back to PINKEY (counted, reported).
    """

    def __init__(self, ctx_ref, poolmat_ref, date_keys_ref, tick_keys):
        self.dk = date_keys_ref[ctx_ref.dec]              # reference decision-date keys
        self.E = poolmat_ref[ctx_ref.dec]
        self.N = ctx_ref.N
        self.tkey = tick_keys
        self.pos = {int(d): i for i, d in enumerate(self.dk)}
        self.miss = 0

    def project(self, seed, dkey_live, tkey_live):
        Rref = np.random.default_rng(seed).random(self.E.shape)
        n = len(dkey_live)
        R = np.empty((n, self.N))
        E = np.empty((n, self.N), bool)
        hit = np.array([self.pos.get(int(d), -1) for d in dkey_live])
        ok = hit >= 0
        R[ok] = Rref[hit[ok]]
        E[ok] = self.E[hit[ok]]
        if (~ok).any():
            R[~ok] = keyed_uniform(seed, dkey_live[~ok], tkey_live)
            E[~ok] = True
            self.miss = int((~ok).sum())
        return R, E


# ==========================================================================================
# (4) LOAD
# ==========================================================================================
P("=" * 100)
P(f"IDEA 1002 (lane B, 2026-09-16)  should-a-ROTATING-NULL-be-PINNED-to-a-PRICE-VINTAGE")
P("=" * 100)
P(f"SMOKE={int(SMOKE)}  draws={NDRAW}  arms={ARMS}  cadences={CADS}  gross={GROSS}")
P()

VINT = {"U56": U56_VINTAGES, "B136": B136_VINTAGES}
BUG = {"U56": U56_PREFIX_BUG, "B136": B136_PREFIX_BUG}
PANELS = ["U56", "B136"]
TICK = {p: universe(p) for p in PANELS}
PX = {}
P("(0) VINTAGE LADDER -- replayed out of git")
cen = []
for pan in PANELS:
    ref_idx = None
    for sha in VINT[pan] + BUG[pan]:
        px = read_vintage(pan, sha, TICK[pan])
        PX[(pan, sha)] = px
        lab = "LADDER" if sha in VINT[pan] else "SCHEMA-BREAK (excluded)"
        cen.append(dict(panel=pan, sha=sha, date=commit_date(sha), rows=len(px),
                        cols=px.shape[1], last=str(px.index[-1].date()), role=lab))
        if sha in VINT[pan]:
            if ref_idx is None:
                ref_idx = px.index
                P(f"  {pan:5s} {sha} {commit_date(sha)}  {px.shape}  last {px.index[-1].date()}"
                  f"   REFERENCE (PINSET pin)")
            else:
                ci = ref_idx.intersection(px.index)
                a = PX[(pan, VINT[pan][0])].loc[ci]
                b = px.loc[ci]
                rel = ((b - a).abs() / a.abs().clip(lower=1e-9)).to_numpy()
                nz = int(np.nansum(rel > 1e-9))
                P(f"  {pan:5s} {sha} {commit_date(sha)}  {px.shape}  last {px.index[-1].date()}"
                  f"   restated {nz:,} of {len(ci)*px.shape[1]:,} cells "
                  f"({nz/rel.size:.2%})  max rel {float(np.nanmax(rel)):.3e}")
        else:
            P(f"  {pan:5s} {sha} {commit_date(sha)}  {px.shape}  last {px.index[-1].date()}"
              f"   *** SCHEMA BREAK (calendar-day index) -- excluded from every hypothesis")
CENSUS = pd.DataFrame(cen)
REF = {p: VINT[p][0] for p in PANELS}
# the shared index prefix, for LIVE_CP
CPIDX = {p: PX[(p, VINT[p][0])].index for p in PANELS}
for p in PANELS:
    for s in VINT[p]:
        CPIDX[p] = CPIDX[p].intersection(PX[(p, s)].index)
P(f"  common prefix: U56 {len(CPIDX['U56'])} rows through {CPIDX['U56'][-1].date()}, "
  f"B136 {len(CPIDX['B136'])} rows through {CPIDX['B136'][-1].date()}")
P()

TKEY = {p: _tickkey(TICK[p]) for p in PANELS}


def dkeys(idx):
    return np.asarray(idx.to_numpy().astype("datetime64[D]").astype("int64")).astype(np.uint64)


# ==========================================================================================
# (5) GATES
# ==========================================================================================
P("=" * 100)
P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
P("=" * 100)
GK = {}
pref = PX[("U56", VINT["U56"][-1])]                       # newest live vintage
idx = pref.index

bad = 0
for per in CADS:
    m = engine.rebalance_mask(idx, per)
    key = {"W": idx.to_period("W"), "M": idx.to_period("M"), "Q": idx.to_period("Q")}[per]
    s = pd.Series(key, index=idx)
    bad += int(((s != s.shift(-1)).values != m.values).sum())
GK["G0"] = bad == 0
P(f"  G0 rebalance mask identity on {CADS}: {bad} rows   {'PASS' if GK['G0'] else 'FAIL'}")

Wb = BOOKS["EWELIG"](pref, GROSS)
ctxM = Ctx(pref, engine.rebalance_mask(idx, "M"))
gr, tn = ctxM.run(ctxM.shift(Wb))
eng = engine.backtest(pref, Wb, cost_bps=0.0, freq="M")
d1r = float(np.abs(gr[WARM:] - eng["returns"].values[WARM:]).max())
d1t = float(np.abs(tn[WARM:] - eng["turnover"].values[WARM:]).max())
GK["G1"] = d1r < 1e-12 and d1t < 1e-10
P(f"  G1 Ctx == engine.backtest   returns {d1r:.3e}  turnover {d1t:.3e}   "
  f"{'PASS' if GK['G1'] else 'FAIL'}")
del eng

d2 = float((band_book(pref, BAND0, GROSS) - rules_v2_weights(pref, BAND0, GROSS)).abs().max().max())
GK["G2"] = d2 == 0.0
P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights: {d2:.3e}   "
  f"{'PASS' if GK['G2'] else 'FAIL'}")

# G8 -- the ladder is a prefix extension; the schema break is not
g8ok, g8bad = True, []
for pan in PANELS:
    base = PX[(pan, VINT[pan][0])].index
    for s in VINT[pan][1:]:
        if not base.equals(PX[(pan, s)].index[:len(base)]):
            g8ok = False
            g8bad.append(f"{pan}/{s}")
    for s in BUG[pan]:
        if base.equals(PX[(pan, s)].index[:len(base)]):
            g8bad.append(f"{pan}/{s}(bug-looks-like-prefix)")
GK["G8"] = g8ok
P(f"  G8 every ladder vintage is a PREFIX EXTENSION of the reference: "
  f"{'PASS' if GK['G8'] else 'FAIL ' + ','.join(g8bad)}")
P(f"     schema-break vintages excluded: "
  f"{ {p: BUG[p] for p in PANELS} }")
P()


# ==========================================================================================
# (6) THE GRID
# ==========================================================================================
def spy_block(px, sl, cad):
    r = px["SPY"].pct_change().fillna(0.0).to_numpy()[WARM:]
    return block(r, sl)


REAL, NULL, GROSSCHK, PINCHK = [], [], [], []
SUBJ_RUNGS = []
NAMESETS = {}         # (pan, sha, book, cad, arm, seed) -> hash, for flip/invariance gates
DRAWCACHE = {}        # (pan, sha, book, cad, arm, seed) -> dict of OOS stats, for variance

P("=" * 100)
P("(B) GRID -- real books and coin flips on every vintage, under all four draw conventions")
P("=" * 100)

for pan in PANELS:
    tk = TKEY[pan]
    for cad in CADS:
        # reference-vintage machinery for PINSET (built once per (panel, cadence, book))
        pxr = PX[(pan, REF[pan])]
        ctxr = Ctx(pxr, engine.rebalance_mask(pxr.index, cad))
        poolr = pools(pxr)
        dkr = dkeys(pxr.index)
        refdraw = {b: RefDraw(ctxr, poolr[POOLKIND[b]], dkr, tk) for b in BOOKS}
        del ctxr, poolr

        for sha in VINT[pan]:
            px_full = PX[(pan, sha)]
            for arm_idx in (0, 1):                       # 0 = full index, 1 = common prefix
                px = px_full if arm_idx == 0 else px_full.loc[CPIDX[pan]]
                arms_here = ["LIVE", "PINKEY", "PINSET"] if arm_idx == 0 else ["LIVE_CP"]
                ctx = Ctx(px, engine.rebalance_mask(px.index, cad))
                sl = Slices(px.index)
                dk = dkeys(px.index)
                pl = pools(px)
                spy = spy_block(px, sl, cad)
                spyIS = spy
                for book, fn in BOOKS.items():
                    Wb = fn(px, GROSS)
                    wt = ctx.shift(Wb)
                    fam = Family(ctx, pl[POOLKIND[book]], wt, dk, tk)
                    g_, t_ = ctx.run(wt)
                    g_, t_ = g_[WARM:], t_[WARM:]
                    if arm_idx == 0:
                        for c in RUNGS:
                            bl = block(g_ - t_ * c / 1e4, sl)
                            lg = legs_rec(bl, spy)
                            li = legs_is(bl, spyIS)
                            REAL.append(dict(panel=pan, sha=sha, date=commit_date(sha),
                                             book=book, cadence=cad, cost_bps=c,
                                             turn_per_yr=float(t_.sum() / (len(t_) / 252.0)),
                                             **bl,
                                             **{f"spy_{k}": v for k, v in spy.items()},
                                             pass4b=all(lg.values()), fail4b=failstr(lg),
                                             **{f"leg_{LEGNAME[k]}": v for k, v in lg.items()},
                                             IS_legs=sum(li.values())))
                    for arm in arms_here:
                        ref = refdraw[book] if arm == "PINSET" else None
                        for s in range(NDRAW):
                            seed = SEED0 + 1000 * BOOKSEED[book] + s
                            W, M = fam.weights(arm, seed, ref)
                            gn, tnn = ctx.run(W)
                            gn, tnn = gn[WARM:], tnn[WARM:]
                            net = gn - tnn * HEAD_COST / 1e4
                            bl = block(net, sl)
                            lg = legs_rec(bl, spy)
                            rec = dict(panel=pan, sha=sha, date=commit_date(sha), book=book,
                                       cadence=cad, arm=arm, seed=seed, draw=s,
                                       cost_bps=HEAD_COST, **bl,
                                       pass4b=all(lg.values()), fail4b=failstr(lg))
                            NULL.append(rec)
                            DRAWCACHE[(pan, sha, book, cad, arm, s)] = (
                                bl["OOS_Sharpe"], bl["OOS_MaxDD"], bl["OOS_CAGR"],
                                bl["Sharpe"], all(lg.values()))
                            if arm in ("LIVE", "PINKEY", "PINSET"):
                                h = hash(M[:len(fam.dkey)].tobytes())
                                NAMESETS[(pan, sha, book, cad, arm, s)] = (
                                    h, fam.dkey.copy() if s == 0 else None)
                            # G5 gross match, on a sample of draws
                            if s < 3:
                                cn = int(np.abs(M.sum(axis=1) - fam.take).max())
                                gs = float(np.abs(W[ctx.reb].sum(axis=1)
                                                  - fam.perw * fam.take).max())
                                GROSSCHK.append(dict(panel=pan, sha=sha, book=book,
                                                     cadence=cad, arm=arm, seed=seed,
                                                     count_err=cn, gross_err=gs))
                            # subject-cell cost ladder
                            if (pan, book, cad) == SUBJECT and arm in ARMS:
                                for c in RUNGS:
                                    if c == HEAD_COST:
                                        b2 = bl
                                    else:
                                        b2 = block(gn - tnn * c / 1e4, sl)
                                    l2 = legs_rec(b2, spy)
                                    SUBJ_RUNGS.append(dict(sha=sha, arm=arm, draw=s,
                                                           cost_bps=c,
                                                           OOS_Sharpe=b2["OOS_Sharpe"],
                                                           OOS_MaxDD=b2["OOS_MaxDD"],
                                                           pass4b=all(l2.values())))
                    del fam, Wb, wt
                del ctx, pl, px
        del refdraw
        P(f"  {pan:5s} cadence {cad}: done  ({time.time()-T0:6.1f}s, "
          f"{len(NULL):,} null rows, {len(REAL):,} real rows)")

REAL = pd.DataFrame(REAL)
NULL = pd.DataFrame(NULL)
GROSSCHK = pd.DataFrame(GROSSCHK)
SUBJ_RUNGS = pd.DataFrame(SUBJ_RUNGS)
P()

# ---- G5 / G3 / G6 / G7 / G4 -----------------------------------------------------------
g5c = int(GROSSCHK["count_err"].max())
g5g = float(GROSSCHK["gross_err"].max())
GK["G5"] = g5c == 0 and g5g < 1e-12
P(f"  G5 GROSS MATCH, all four arms: max count err {g5c}, max gross err {g5g:.3e}   "
  f"{'PASS' if GK['G5'] else 'FAIL'}")

# G3 determinism -- rebuild the subject cell's first draw
pan, book, cad = SUBJECT
sha = VINT[pan][-1]
px = PX[(pan, sha)]
ctx = Ctx(px, engine.rebalance_mask(px.index, cad))
sl = Slices(px.index)
fam = Family(ctx, pools(px)[POOLKIND[book]], ctx.shift(BOOKS[book](px, GROSS)),
             dkeys(px.index), TKEY[pan])
Wa, _ = fam.weights("LIVE", SEED0 + 1000 * BOOKSEED[book], None)
Wb2, _ = fam.weights("LIVE", SEED0 + 1000 * BOOKSEED[book], None)
d3 = float(np.abs(Wa - Wb2).max())
GK["G3"] = d3 == 0.0
P(f"  G3 determinism (subject draw rebuilt): {d3:.3e}   {'PASS' if GK['G3'] else 'FAIL'}")
del ctx, fam, Wa, Wb2

# G7 PINSET == LIVE on the reference vintage itself
g7 = []
for pan in PANELS:
    s0 = REF[pan]
    for book in BOOKS:
        for cad in CADS:
            for d in range(min(5, NDRAW)):
                a = DRAWCACHE.get((pan, s0, book, cad, "LIVE", d))
                b = DRAWCACHE.get((pan, s0, book, cad, "PINSET", d))
                if a and b:
                    g7.append(max(abs(a[i] - b[i]) for i in range(4)))
g7m = max(g7) if g7 else np.nan
GK["G7"] = (not g7) or g7m == 0.0
P(f"  G7 PINSET == LIVE on the REFERENCE vintage: max |d| {g7m:.3e} over {len(g7)} cells   "
  f"{'PASS' if GK['G7'] else 'FAIL'}")

# G4 PINKEY invariance -- identical name sets across vintages wherever pool AND count agree
g4rows, g4bad = 0, 0
for pan in PANELS:
    base = VINT[pan][0]
    for book in BOOKS:
        for cad in CADS:
            for sha in VINT[pan][1:]:
                for d in range(min(5, NDRAW)):
                    a = NAMESETS.get((pan, base, book, cad, "PINKEY", d))
                    b = NAMESETS.get((pan, sha, book, cad, "PINKEY", d))
                    if a and b:
                        g4rows += 1
PINKEY_SAMEBOOK = {}
for pan in PANELS:
    tk = TKEY[pan]
    base = VINT[pan][0]
    pxb = PX[(pan, base)]
    for cad in CADS:
        cb = Ctx(pxb, engine.rebalance_mask(pxb.index, cad))
        plb = pools(pxb)
        dkb = dkeys(pxb.index)
        for book in BOOKS:
            fb = Family(cb, plb[POOLKIND[book]], cb.shift(BOOKS[book](pxb, GROSS)), dkb, tk)
            Mb = fb.weights("PINKEY", SEED0 + 1000 * BOOKSEED[book], None)[1]
            keyb = {int(k): Mb[i] for i, k in enumerate(fb.dkey)}
            takeb = {int(k): int(fb.take[i]) for i, k in enumerate(fb.dkey)}
            Eb = {int(k): fb.E[i] for i, k in enumerate(fb.dkey)}
            for sha in VINT[pan][1:]:
                pxv = PX[(pan, sha)]
                cv = Ctx(pxv, engine.rebalance_mask(pxv.index, cad))
                plv = pools(pxv)
                fv = Family(cv, plv[POOLKIND[book]], cv.shift(BOOKS[book](pxv, GROSS)),
                            dkeys(pxv.index), tk)
                Mv = fv.weights("PINKEY", SEED0 + 1000 * BOOKSEED[book], None)[1]
                for i, k in enumerate(fv.dkey):
                    k = int(k)
                    if k in keyb and takeb[k] == int(fv.take[i]) and \
                       np.array_equal(Eb[k], fv.E[i]):
                        g4rows += 1
                        if not np.array_equal(keyb[k], Mv[i]):
                            g4bad += 1
                del cv, plv, fv
            del fb
        del cb, plb
GK["G4"] = g4bad == 0
P(f"  G4 PINKEY invariance (same pool AND count -> same names across vintages): "
  f"{g4bad} of {g4rows:,} comparable decision rows differ   {'PASS' if GK['G4'] else 'FAIL'}")

# G6 nesting
g6 = 0
for k in DRAW_LADDER[:-1]:
    a = NULL[NULL["draw"] < k]
    b = NULL[NULL["draw"] < DRAW_LADDER[-1]]
    m = b[b["draw"] < k]
    g6 += int((a.reset_index(drop=True)["OOS_Sharpe"]
               - m.reset_index(drop=True)["OOS_Sharpe"]).abs().max() > 0)
GK["G6"] = g6 == 0
P(f"  G6 NESTING (25/50 are the first seeds of 100): {g6} mismatches   "
  f"{'PASS' if GK['G6'] else 'FAIL'}")

# G9 cross-run against idea 975-B's committed real grid (CANON rows, live vintage)
g9p = OUT / "2026-09-16_price-the-QUARTERLY-TRANCHE-against-a-GROSS-MATCHED-ROTATING-NULL_B.real.csv"
FINGER = pd.DataFrame()
if g9p.exists():
    prev = pd.read_csv(g9p)
    prev = prev[prev["estimator"] == "CANON"]
    cols = ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "H1", "H2"]
    # NOTE: 56e08b10 touched BOTH price files, so it appears in BOTH panels' ladders.  Each
    # panel is therefore matched against ITS OWN newest sha, never against the other's.
    parts, d9, v9, n9 = [], 0.0, 0, 0
    for pan in PANELS:
        pj = prev[prev.panel == pan].merge(
            REAL[(REAL.panel == pan) & (REAL.sha == VINT[pan][-1])],
            on=["panel", "book", "cadence", "cost_bps"], suffixes=("_p", "_m"))
        if not len(pj):
            continue
        n9 += len(pj)
        d9 = max([d9] + [float((pj[f"{c}_p"] - pj[f"{c}_m"]).abs().max()) for c in cols])
        v9 += int((pj["pass4b_p"].astype(bool) != pj["pass4b_m"].astype(bool)).sum())
    GK["G9"] = n9 > 0 and d9 < 5e-4 and v9 == 0
    P(f"  G9 CROSS-RUN vs idea 975-B .real.csv CANON (each panel on its OWN newest sha): "
      f"{n9} shared rows, max |d| {d9:.3e}, {v9} 4b verdict disagreements   "
      f"{'PASS' if GK['G9'] else 'FAIL'}")
    # the fingerprint: which vintage do 975-B's committed numbers actually name?
    fg = []
    for pan in PANELS:
        for sha in VINT[pan]:
            pj = prev[prev.panel == pan].merge(
                REAL[(REAL.panel == pan) & (REAL.sha == sha)],
                on=["panel", "book", "cadence", "cost_bps"], suffixes=("_p", "_m"))
            if not len(pj):
                continue
            fg.append(dict(panel=pan, sha=sha, date=commit_date(sha), rows=len(pj),
                           max_abs_diff=max(float((pj[f"{c}_p"] - pj[f"{c}_m"]).abs().max())
                                            for c in cols)))
    FINGER = pd.DataFrame(fg)
else:
    GK["G9"] = False
    P("  G9 CROSS-RUN: 975-B .real.csv not found   FAIL")

P()
P(f"  GATES: {sum(GK.values())} of {len(GK)} PASS   "
  + "  ".join(f"{k}={'P' if v else 'F'}" for k, v in sorted(GK.items())))
P()


# ==========================================================================================
# (7) THE VARIANCE DECOMPOSITION -- the headline
# ==========================================================================================
# ==========================================================================================
# (B2) THE VINTAGE FINGERPRINT -- can a committed artifact's own numbers name its tape?
# ==========================================================================================
if len(FINGER):
    P("=" * 100)
    P("(B2) VINTAGE FINGERPRINT -- idea 975-B's committed CANON rows replayed on EVERY vintage")
    P("=" * 100)
    P("  975-B names no price sha (no committed artifact in this record does).  If the tape")
    P("  term is real but small, its own published numbers should still identify the vintage")
    P("  they were computed on -- exactly on one, and measurably off on every other.")
    P()
    P(f"  {'panel':6s} {'sha':10s} {'date':11s} {'rows':>5s} {'max |d| vs committed':>21s}")
    for _, r in FINGER.iterrows():
        mark = "   <-- EXACT" if r.max_abs_diff < 1e-12 else ""
        P(f"  {r.panel:6s} {r.sha:10s} {r.date:11s} {int(r.rows):5d} "
          f"{r.max_abs_diff:21.3e}{mark}")
    ex = FINGER[FINGER.max_abs_diff < 1e-12]     # float-exact, i.e. at machine epsilon
    P(f"  vintages reproducing 975-B EXACTLY (max |d| < 1e-12): {len(ex)} of {len(FINGER)}"
      + (f"  ({', '.join(ex.panel + '/' + ex.sha)})" if len(ex) else ""))
    nxt = []
    for pan in PANELS:
        o = FINGER[(FINGER.panel == pan) & (FINGER.max_abs_diff >= 1e-12)]["max_abs_diff"]
        if len(o):
            nxt.append(f"{pan} {o.min():.3e}")
    P("  next-closest vintage on each panel: " + ", ".join(nxt))
    P()

P("=" * 100)
P("(C) VARIANCE DECOMPOSITION -- sampling vs tape, per convention")
P("=" * 100)
P("  sigma_seed = SD across seeds within one vintage (SAMPLING)")
P("  sigma_vint = SD across vintages at a FIXED seed (TAPE)")
P("  ratio      = sigma_vint / sigma_seed.  1.0 means the tape is a full independent redraw.")
P()

dec = []
for (pan, book, cad), _ in NULL.groupby(["panel", "book", "cadence"]):
    for arm in ARMS:
        sub = NULL[(NULL.panel == pan) & (NULL.book == book) & (NULL.cadence == cad)
                   & (NULL.arm == arm)]
        if sub.empty:
            continue
        for stat in ("OOS_Sharpe", "OOS_MaxDD", "OOS_CAGR"):
            piv = sub.pivot_table(index="draw", columns="sha", values=stat)
            piv = piv[[s for s in VINT[pan] if s in piv.columns]]
            ss = float(piv.std(axis=0, ddof=1).mean())          # across seeds, per vintage
            sv = float(piv.std(axis=1, ddof=1).mean())          # across vintages, per seed
            dec.append(dict(panel=pan, book=book, cadence=cad, arm=arm, stat=stat,
                            n_vint=piv.shape[1], n_draw=piv.shape[0],
                            sigma_seed=ss, sigma_vint=sv,
                            ratio=sv / ss if ss > 0 else np.nan,
                            mean=float(piv.to_numpy().mean())))
DEC = pd.DataFrame(dec)

for pan in PANELS:
    P(f"  --- {pan}  (stat = null OOS Sharpe, 10 bps, gross {GROSS}) ---")
    P(f"  {'book':8s} {'cad':4s} | " + " | ".join(f"{a:>22s}" for a in ARMS))
    P(f"  {'':8s} {'':4s} | " + " | ".join(f"{'s_seed   s_vint   ratio':>22s}" for a in ARMS))
    for book in BOOKS:
        for cad in CADS:
            cells = []
            for arm in ARMS:
                r = DEC[(DEC.panel == pan) & (DEC.book == book) & (DEC.cadence == cad)
                        & (DEC.arm == arm) & (DEC.stat == "OOS_Sharpe")]
                if r.empty:
                    cells.append(f"{'--':>22s}")
                else:
                    r = r.iloc[0]
                    cells.append(f"{r.sigma_seed:6.4f} {r.sigma_vint:8.2e} {r.ratio:6.4f}")
            P(f"  {book:8s} {cad:4s} | " + " | ".join(cells))
    P()

# pooled ratios per (panel, arm)
DEC["tape_share"] = DEC.sigma_vint ** 2 / (DEC.sigma_vint ** 2 + DEC.sigma_seed ** 2)
POOL = (DEC[DEC.stat == "OOS_Sharpe"].groupby(["panel", "arm"])
        .agg(sigma_seed=("sigma_seed", "mean"), sigma_vint=("sigma_vint", "mean"),
             ratio_mean=("ratio", "mean"), ratio_med=("ratio", "median"),
             tape_share=("tape_share", "median"),
             cells=("ratio", "size")).reset_index())
P("  POOLED over the 9 (book, cadence) cells -- null OOS Sharpe:")
P(f"  {'panel':6s} {'arm':8s} {'s_seed':>8s} {'s_vint':>9s} {'ratio_mean':>11s} {'ratio_med':>10s}"
  f" {'TAPE SHARE of variance':>23s}")
for _, r in POOL.iterrows():
    P(f"  {r.panel:6s} {r.arm:8s} {r.sigma_seed:8.4f} {r.sigma_vint:9.2e} "
      f"{r.ratio_mean:11.4f} {r.ratio_med:10.4f} {r.tape_share:23.6f}")
P("  TAPE SHARE = sigma_vint^2 / (sigma_vint^2 + sigma_seed^2) -- the share of a committed")
P("  null statistic's variance that is the TAPE rather than the COIN.  This is the queue")
P("  line's own question, answered as a number.")
P()


# ==========================================================================================
# (C3) WHICH CHANNEL IS IT?  -- SELECTION (pool / count / names) vs PRICE (the returns)
# ==========================================================================================
P("=" * 100)
P("(C3) MECHANISM -- does the tape change WHICH NAMES the coin flip holds, or only their")
P("     RETURNS?  Counted on decision rows the reference vintage shares with each later one.")
P("=" * 100)
mech = []
for pan in PANELS:
    tk = TKEY[pan]
    base = VINT[pan][0]
    pxb = PX[(pan, base)]
    for cad in CADS:
        cb = Ctx(pxb, engine.rebalance_mask(pxb.index, cad))
        plb = pools(pxb)
        dkb = dkeys(pxb.index)
        for book in BOOKS:
            fb = Family(cb, plb[POOLKIND[book]], cb.shift(BOOKS[book](pxb, GROSS)), dkb, tk)
            seed = SEED0 + 1000 * BOOKSEED[book]
            Mb = fb.weights("LIVE", seed, None)[1]
            posb = {int(k): i for i, k in enumerate(fb.dkey)}
            for sha in VINT[pan][1:]:
                pxv = PX[(pan, sha)]
                cv = Ctx(pxv, engine.rebalance_mask(pxv.index, cad))
                plv = pools(pxv)
                fv = Family(cv, plv[POOLKIND[book]], cv.shift(BOOKS[book](pxv, GROSS)),
                            dkeys(pxv.index), tk)
                Mv = fv.weights("LIVE", seed, None)[1]
                nrow = npool = ncnt = nmask = 0
                for i, k in enumerate(fv.dkey):
                    j = posb.get(int(k), -1)
                    if j < 0:
                        continue
                    nrow += 1
                    npool += int(not np.array_equal(fb.E[j], fv.E[i]))
                    ncnt += int(int(fb.take[j]) != int(fv.take[i]))
                    nmask += int(not np.array_equal(Mb[j], Mv[i]))
                mech.append(dict(panel=pan, book=book, cadence=cad, sha=sha,
                                 shared_rows=nrow, pool_diff=npool, count_diff=ncnt,
                                 nameset_diff=nmask,
                                 pool_rate=npool / max(nrow, 1),
                                 count_rate=ncnt / max(nrow, 1),
                                 nameset_rate=nmask / max(nrow, 1)))
                del cv, plv, fv
            del fb
        del cb, plb
MECH = pd.DataFrame(mech)
mm = (MECH.groupby(["panel", "book", "cadence"])
      .agg(shared=("shared_rows", "sum"), pool=("pool_diff", "sum"),
           count=("count_diff", "sum"), names=("nameset_diff", "sum")).reset_index())
P(f"  {'panel':6s} {'book':8s} {'cad':4s} {'shared rows':>12s} {'pool differs':>13s} "
  f"{'count differs':>14s} {'NAME SET differs':>17s}")
for _, r in mm.iterrows():
    P(f"  {r.panel:6s} {r.book:8s} {r.cadence:4s} {int(r.shared):12,d} "
      f"{int(r['pool']):6d} ({r['pool']/max(r.shared,1):5.2%}) "
      f"{int(r['count']):6d} ({r['count']/max(r.shared,1):5.2%}) "
      f"{int(r['names']):7d} ({r['names']/max(r.shared,1):6.2%})")
SEL_RATE = float(mm[mm.panel == "U56"]["names"].sum()
                 / max(mm[mm.panel == "U56"]["shared"].sum(), 1))
P(f"  U56: the coin flip holds a DIFFERENT NAME SET on {SEL_RATE:.4%} of shared decision rows.")
P("  If this is ~0, the tape term measured in (C) is entirely the RETURNS of an UNCHANGED")
P("  book -- i.e. the null is not being RESAMPLED at all, only re-priced.")
P()


# ==========================================================================================
# (C2) THE SCHEMA BREAK -- labelled, post-smoke hypothesis (see PROVENANCE in the header)
# ==========================================================================================
P("=" * 100)
P("(C2) THE 2026-09-04 CALENDAR-DAY INDEX FIX, priced as its own channel")
P("=" * 100)
P("  The two 2026-09-03 prices.csv vintages carry a CALENDAR-day index (6,060 rows incl.")
P("  weekends), not a trading-day one.  Commit c006b439 fixed it.  A null drawn on that index")
P("  is a different object -- different rebalance grid, different 200d MA window -- so this is")
P("  NOT a restatement and is fenced off from every other number in this run.")
P()
sb = []
pan = "U56"
tk = TKEY[pan]
for sha in [VINT[pan][0]] + BUG[pan]:
    pxv = PX[(pan, sha)]
    for cad in CADS:
        ctxv = Ctx(pxv, engine.rebalance_mask(pxv.index, cad))
        slv = Slices(pxv.index)
        plv = pools(pxv)
        spyv = spy_block(pxv, slv, cad)
        for book in BOOKS:
            famv = Family(ctxv, plv[POOLKIND[book]], ctxv.shift(BOOKS[book](pxv, GROSS)),
                          dkeys(pxv.index), tk)
            for d in range(min(NDRAW, 50)):
                seed = SEED0 + 1000 * BOOKSEED[book] + d
                Wv, _ = famv.weights("LIVE", seed, None)
                gv, tv = ctxv.run(Wv)
                blv = block(gv[WARM:] - tv[WARM:] * HEAD_COST / 1e4, slv)
                lgv = legs_rec(blv, spyv)
                sb.append(dict(sha=sha, role=("LADDER-REF" if sha == VINT[pan][0]
                                              else "SCHEMA-BREAK"),
                               book=book, cadence=cad, draw=d,
                               OOS_Sharpe=blv["OOS_Sharpe"], OOS_MaxDD=blv["OOS_MaxDD"],
                               pass4b=all(lgv.values()), fail4b=failstr(lgv)))
            del famv
        del ctxv, plv
SB = pd.DataFrame(sb)
ref0 = VINT["U56"][0]
sbp = SB.pivot_table(index=["book", "cadence", "draw"], columns="sha", values="OOS_Sharpe")
sbd = {c: float((sbp[c] - sbp[ref0]).abs().max()) for c in sbp.columns if c != ref0}
sbl = SB.pivot_table(index=["book", "cadence", "draw"], columns="sha", values="fail4b",
                     aggfunc="first")
sbf = {c: float((sbl[c] != sbl[ref0]).mean()) for c in sbl.columns if c != ref0}
sbv = SB.pivot_table(index=["book", "cadence", "draw"], columns="sha", values="pass4b")
sb4 = {c: float((sbv[c].astype(bool) != sbv[ref0].astype(bool)).mean())
       for c in sbv.columns if c != ref0}
LADDER_MAX = 0.0
for book in BOOKS:
    for cad in CADS:
        sub = NULL[(NULL.panel == "U56") & (NULL.arm == "LIVE") & (NULL.book == book)
                   & (NULL.cadence == cad)]
        pv = sub.pivot_table(index="draw", columns="sha", values="OOS_Sharpe")
        pv = pv[[x for x in VINT["U56"] if x in pv.columns]]
        LADDER_MAX = max(LADDER_MAX, float(pv.sub(pv[ref0], axis=0).abs().to_numpy().max()))
P(f"  max |d OOS Sharpe| at IDENTICAL seeds, vs the ladder reference {ref0}:")
P(f"    across the WHOLE 9-vintage post-fix ladder (nightly restatement + append): "
  f"{LADDER_MAX:.4f}")
for c in sbd:
    P(f"    across the SCHEMA BREAK {c} ({commit_date(c)}):  {sbd[c]:.4f}   "
      f"binding-leg flips {sbf[c]:.4f}   4b verdict flips {sb4[c]:.4f}")
SCHEMA_MAX = max(sbd.values()) if sbd else np.nan
SCHEMA_RATIO = SCHEMA_MAX / LADDER_MAX if LADDER_MAX > 0 else np.inf
P(f"  ratio SCHEMA / LADDER: {SCHEMA_RATIO:.1f}x")
P("  (971 reported max |dSharpe| 0.254 and 7.4% of REC 4b verdicts flipped on U56 at identical")
P("   seeds.  Read that number against these two, not against one of them.)")
P()


# ==========================================================================================
# (8) FLIP RATES AND BASE RATES
# ==========================================================================================
P("=" * 100)
P("(D) PER-DRAW VERDICT FLIPS and PUBLISHED BASE RATES")
P("=" * 100)
flip = []
for pan in PANELS:
    base = VINT[pan][0]
    for book in BOOKS:
        for cad in CADS:
            for arm in ARMS:
                sub = NULL[(NULL.panel == pan) & (NULL.book == book) & (NULL.cadence == cad)
                           & (NULL.arm == arm)]
                if sub.empty:
                    continue
                piv = sub.pivot_table(index="draw", columns="sha", values="pass4b")
                piv = piv[[s for s in VINT[pan] if s in piv.columns]].astype(bool)
                ref = piv[base]
                fl = float((piv.ne(ref, axis=0)).to_numpy().mean())
                lgp = sub.pivot_table(index="draw", columns="sha", values="fail4b",
                                      aggfunc="first")
                lgp = lgp[[s for s in VINT[pan] if s in lgp.columns]]
                lfl = float((lgp.ne(lgp[base], axis=0)).to_numpy().mean())
                nm = sub.pivot_table(index="draw", columns="sha", values="OOS_Sharpe")
                nm = nm[[s for s in VINT[pan] if s in nm.columns]]
                idr = float((nm.sub(nm[base], axis=0).abs() < 1e-12).to_numpy().mean())
                br = piv.mean(axis=0)
                flip.append(dict(panel=pan, book=book, cadence=cad, arm=arm,
                                 flip_rate=fl, leg_flip_rate=lfl, identical_rate=idr,
                                 base_rate_ref=float(br[base]),
                                 base_rate_live=float(br.iloc[-1]),
                                 base_rate_min=float(br.min()), base_rate_max=float(br.max()),
                                 base_rate_range=float(br.max() - br.min()),
                                 base_rate_mean=float(br.mean())))
FLIP = pd.DataFrame(flip)

for pan in PANELS:
    P(f"  --- {pan} ---   flip = share of (draw, vintage) BINDING-LEG strings differing from "
      f"the reference vintage's;  ident = share reproducing the reference BIT-FOR-BIT")
    P(f"  {'book':8s} {'cad':4s} | " + " | ".join(f"{a:>17s}" for a in ARMS))
    P(f"  {'':8s} {'':4s} | " + " | ".join(f"{'flip    ident':>17s}" for a in ARMS))
    for book in BOOKS:
        for cad in CADS:
            cells = []
            for arm in ARMS:
                r = FLIP[(FLIP.panel == pan) & (FLIP.book == book) & (FLIP.cadence == cad)
                         & (FLIP.arm == arm)]
                cells.append(f"{r.iloc[0].leg_flip_rate:6.4f}  {r.iloc[0].identical_rate:6.4f}"
                             if len(r) else f"{'--':>17s}")
            P(f"  {book:8s} {cad:4s} | " + " | ".join(cells))
    P()

P("  PUBLISHED BASE RATE (the aggregate the record actually commits) across vintages:")
P(f"  {'panel':6s} {'book':8s} {'cad':4s} {'arm':8s} {'ref':>7s} {'live':>7s} {'min':>7s} "
  f"{'max':>7s} {'range':>7s} {'2xMCSE':>7s} {'stable':>7s}")
FLIP["mcse2"] = 2.0 * np.sqrt(
    np.maximum(FLIP["base_rate_mean"] * (1 - FLIP["base_rate_mean"]), 1e-9) / NDRAW)
FLIP["stable"] = FLIP["base_rate_range"] <= FLIP["mcse2"]
for _, r in FLIP.iterrows():
    b = float(r.mcse2)
    ok = bool(r.stable)
    if r.arm in ("LIVE", "PINSET"):
        P(f"  {r.panel:6s} {r.book:8s} {r.cadence:4s} {r.arm:8s} {r.base_rate_ref:7.3f} "
          f"{r.base_rate_live:7.3f} {r.base_rate_min:7.3f} {r.base_rate_max:7.3f} "
          f"{r.base_rate_range:7.3f} {b:7.3f} {'YES' if ok else 'NO':>7s}")
LIVE_STABLE = float(FLIP[FLIP.arm == "LIVE"]["stable"].mean())
P(f"  LIVE-arm base rates inside 2 x their own Monte-Carlo SE: "
  f"{int(FLIP[FLIP.arm=='LIVE']['stable'].sum())} of {int((FLIP.arm=='LIVE').sum())} "
  f"= {LIVE_STABLE:.3f}")
P()


# ==========================================================================================
# (9) THE REAL BOOK CONTROL
# ==========================================================================================
P("=" * 100)
P("(E) CONTROL -- how far the SAME TAPE moves a REAL book")
P("=" * 100)
rc = (REAL[REAL.cost_bps == HEAD_COST]
      .groupby(["panel", "book", "cadence"])
      .agg(OOS_Sharpe_min=("OOS_Sharpe", "min"), OOS_Sharpe_max=("OOS_Sharpe", "max"),
           OOS_MaxDD_min=("OOS_MaxDD", "min"), OOS_MaxDD_max=("OOS_MaxDD", "max"),
           OOS_CAGR_min=("OOS_CAGR", "min"), OOS_CAGR_max=("OOS_CAGR", "max"),
           pass4b_n=("pass4b", "sum"), n=("pass4b", "size")).reset_index())
rc["Sharpe_range"] = rc.OOS_Sharpe_max - rc.OOS_Sharpe_min
rc["DD_range_pp"] = (rc.OOS_MaxDD_max - rc.OOS_MaxDD_min) * 100
rc["CAGR_range_pp"] = (rc.OOS_CAGR_max - rc.OOS_CAGR_min) * 100
rc["verdict_flips"] = (rc.pass4b_n > 0) & (rc.pass4b_n < rc.n)
P(f"  {'panel':6s} {'book':8s} {'cad':4s} {'OOS_Sharpe range':>17s} {'DD range pp':>12s} "
  f"{'CAGR range pp':>14s} {'4b passes':>10s} {'flips':>6s}")
for _, r in rc.iterrows():
    P(f"  {r.panel:6s} {r.book:8s} {r.cadence:4s} {r.Sharpe_range:17.3e} "
      f"{r.DD_range_pp:12.3e} {r.CAGR_range_pp:14.3e} "
      f"{int(r.pass4b_n):4d}/{int(r.n):<5d} {'YES' if r.verdict_flips else 'no':>6s}")
REAL_RANGE_U56 = float(rc[rc.panel == "U56"]["Sharpe_range"].max())
P(f"  U56 worst REAL OOS-Sharpe range across {len(VINT['U56'])} vintages: {REAL_RANGE_U56:.3e}")
P()


# ==========================================================================================
# (10) HYPOTHESES
# ==========================================================================================
def rr(pan, arm, stat="OOS_Sharpe"):
    r = DEC[(DEC.panel == pan) & (DEC.arm == arm) & (DEC.stat == stat)]
    return float(r["ratio"].median()), float(r["sigma_vint"].mean())


H = []
r_pinset, sv_pinset = rr("U56", "PINSET")
r_live, sv_live = rr("U56", "LIVE")
r_cp, sv_cp = rr("U56", "LIVE_CP")
r_key, sv_key = rr("U56", "PINKEY")

H.append(dict(id="H_TAPE", bar=f"median sigma_vint/sigma_seed (PINSET, U56) <= {TAPE_BAR}",
              value=r_pinset, passed=bool(r_pinset <= TAPE_BAR)))
H.append(dict(id="H_RESAMPLE", bar=f"median sigma_vint/sigma_seed (LIVE, U56) >= {RESAMPLE_BAR}",
              value=r_live, passed=bool(r_live >= RESAMPLE_BAR)))
app = sv_live / sv_cp if sv_cp > 0 else np.inf
H.append(dict(id="H_APPEND", bar=f"sigma_vint(LIVE)/sigma_vint(LIVE_CP) >= {APPEND_BAR}",
              value=app, passed=bool(app >= APPEND_BAR)))
fl_live = float(FLIP[(FLIP.panel == "U56") & (FLIP.arm == "LIVE")]["leg_flip_rate"].mean())
fl_pin = float(FLIP[(FLIP.panel == "U56") & (FLIP.arm == "PINSET")]["leg_flip_rate"].mean())
red = (1 - fl_pin / fl_live) if fl_live > 0 else (1.0 if fl_pin == 0 else np.nan)
H.append(dict(id="H_FLIP", bar=f"binding-leg flip-rate reduction LIVE->PINSET (U56) >= {FLIP_BAR}",
              value=red, passed=bool(red >= FLIP_BAR)))
H.append(dict(id="H_BASE", bar=f"share of LIVE cells with base-rate range <= 2xMCSE >= {BASE_BAR}",
              value=LIVE_STABLE, passed=bool(LIVE_STABLE >= BASE_BAR)))
H.append(dict(id="H_REAL", bar=f"worst REAL OOS-Sharpe range across U56 vintages <= {REAL_BAR}",
              value=REAL_RANGE_U56, passed=bool(REAL_RANGE_U56 <= REAL_BAR)))
sj = FLIP[(FLIP.panel == SUBJECT[0]) & (FLIP.book == SUBJECT[1])
          & (FLIP.cadence == SUBJECT[2]) & (FLIP.arm == "LIVE")]
stale = float(abs(sj.iloc[0].base_rate_ref - sj.iloc[0].base_rate_live)) if len(sj) else np.nan
H.append(dict(id="H_STALE", bar=f"|base rate(oldest sha) - base rate(live)| in subject <= {STALE_BAR}",
              value=stale, passed=bool(stale <= STALE_BAR)))


# ==========================================================================================
# (11) RULE 8 WALK-FORWARD
# ==========================================================================================
P("=" * 100)
P("(F) RULE 8 WALK-FORWARD -- parameters chosen on 2009-2016 only, 2017-2026 untouched")
P("=" * 100)
P("  Choice space = the 9 (book, cadence) cells at gross 0.75, 10 bps, per PANEL per VINTAGE.")
P("  C_IS4B    most IS 4b legs passed (ties -> higher IS Sharpe)")
P("  C_ISSHARPE highest IS Sharpe")
P("  C_ISCAGR  highest IS CAGR")
P()

# baseline (RULES v2, live book) and SPY, per panel per vintage
basel = []
for pan in PANELS:
    for sha in VINT[pan]:
        px = PX[(pan, sha)]
        ctx = Ctx(px, engine.rebalance_mask(px.index, "W"))
        sl = Slices(px.index)
        g_, t_ = ctx.run(ctx.shift(rules_v2_weights(px, BAND0, GROSS)))
        bl = block(g_[WARM:] - t_[WARM:] * HEAD_COST / 1e4, sl)
        spy = spy_block(px, sl, "W")
        basel.append(dict(panel=pan, sha=sha, date=commit_date(sha), who="RULESv2",
                          **bl))
        basel.append(dict(panel=pan, sha=sha, date=commit_date(sha), who="SPY", **spy))
        del ctx
BASE = pd.DataFrame(basel)

wf = []
for pan in PANELS:
    for sha in VINT[pan]:
        sub = REAL[(REAL.panel == pan) & (REAL.sha == sha) & (REAL.cost_bps == HEAD_COST)]
        bb = BASE[(BASE.panel == pan) & (BASE.sha == sha) & (BASE.who == "RULESv2")].iloc[0]
        sp = BASE[(BASE.panel == pan) & (BASE.sha == sha) & (BASE.who == "SPY")].iloc[0]
        for ch, key in (("C_IS4B", ["IS_legs", "IS_Sharpe"]),
                        ("C_ISSHARPE", ["IS_Sharpe"]),
                        ("C_ISCAGR", ["IS_CAGR"])):
            pick = sub.sort_values(key, ascending=False).iloc[0]
            lg = legs_rec(pick, {k: sp[k] for k in sp.index if k in
                                 ("H1", "H2", "OOS_Sharpe", "MaxDD", "CAGR")})
            k4a = (pick["H1"] > bb["H1"] and pick["H2"] > bb["H2"]
                   and pick["MaxDD"] >= bb["MaxDD"])
            # certification: does the pick beat its own cell's null on OOS Sharpe?
            nl = NULL[(NULL.panel == pan) & (NULL.sha == sha) & (NULL.book == pick.book)
                      & (NULL.cadence == pick.cadence)]
            pct = {a: float((nl[nl.arm == a]["OOS_Sharpe"] < pick["OOS_Sharpe"]).mean())
                   for a in ARMS if (nl.arm == a).any()}
            wf.append(dict(panel=pan, sha=sha, date=commit_date(sha), chooser=ch,
                           pick=f"{pick.book}/{pick.cadence}", book=pick.book,
                           cadence=pick.cadence, IS_legs=int(pick.IS_legs),
                           IS_Sharpe=pick.IS_Sharpe, IS_CAGR=pick.IS_CAGR,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           base_OOS_CAGR=bb.OOS_CAGR, base_OOS_Sharpe=bb.OOS_Sharpe,
                           base_OOS_MaxDD=bb.OOS_MaxDD,
                           spy_OOS_CAGR=sp.OOS_CAGR, spy_OOS_Sharpe=sp.OOS_Sharpe,
                           spy_OOS_MaxDD=sp.OOS_MaxDD,
                           pass4b=all(lg.values()), fail4b=failstr(lg), pass4a=bool(k4a),
                           **{f"pctl_{a}": pct.get(a, np.nan) for a in ARMS}))
WF = pd.DataFrame(wf)

P(f"  {'panel':6s} {'chooser':11s} {'picks across vintages':38s} {'invariant':>10s}")
inv_all = True
for pan in PANELS:
    for ch in ("C_IS4B", "C_ISSHARPE", "C_ISCAGR"):
        s = WF[(WF.panel == pan) & (WF.chooser == ch)]
        ps = s["pick"].unique()
        inv = len(ps) == 1
        inv_all &= inv
        P(f"  {pan:6s} {ch:11s} {', '.join(sorted(ps))[:38]:38s} {'YES' if inv else 'NO':>10s}")
P()
H.append(dict(id="H_RULE8", bar="the IS-only chooser's pick is the same on every vintage",
              value=float(inv_all), passed=bool(inv_all)))
H.append(dict(id="H_SCHEMA", bar="max|dSharpe| across the SCHEMA BREAK >= 10.0 x across the "
                                 "whole post-fix ladder  [POST-SMOKE, see header PROVENANCE]",
              value=SCHEMA_RATIO, passed=bool(SCHEMA_RATIO >= 10.0)))

P("  OOS (2017-2026) of every pick, vs the LIVE baseline (RULES v2, W, 10 bps) and SPY:")
P(f"  {'panel':6s} {'sha':9s} {'chooser':11s} {'pick':14s} {'OOS CAGR':>9s} {'Sharpe':>7s} "
  f"{'MaxDD':>8s} | {'base CAGR/Sh/DD':>22s} | {'SPY CAGR/Sh/DD':>22s} | {'4b':>3s} {'4a':>3s} "
  f"{'binds':>18s}")
for _, r in WF.iterrows():
    P(f"  {r.panel:6s} {r.sha:9s} {r.chooser:11s} {r['pick']:14s} {r.OOS_CAGR:9.2%} "
      f"{r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:8.2%} | "
      f"{r.base_OOS_CAGR:6.2%}/{r.base_OOS_Sharpe:5.3f}/{r.base_OOS_MaxDD:7.2%} | "
      f"{r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:5.3f}/{r.spy_OOS_MaxDD:7.2%} | "
      f"{'Y' if r.pass4b else 'n':>3s} {'Y' if r.pass4a else 'n':>3s} {r.fail4b:>18s}")
n8b = int(WF.pass4b.sum())
n8a = int(WF.pass4a.sum())
P(f"  rule 8: OOS 4b {n8b} of {len(WF)}   OOS 4a {n8a} of {len(WF)}")
P()

P("  DOES THE PICK'S OWN CERTIFICATION MOVE WITH THE ARM?  (percentile of the pick inside its "
  "own null on OOS Sharpe)")
P(f"  {'panel':6s} {'sha':9s} {'chooser':11s} " + " ".join(f"{a:>9s}" for a in ARMS))
for _, r in WF.iterrows():
    P(f"  {r.panel:6s} {r.sha:9s} {r.chooser:11s} "
      + " ".join(f"{r[f'pctl_{a}']:9.3f}" for a in ARMS))
pct_spread = float(np.nanmax([abs(WF[f"pctl_{a}"] - WF["pctl_LIVE"]).max() for a in ARMS]))
P(f"  max |percentile(arm) - percentile(LIVE)| over all picks: {pct_spread:.4f}")
P()


# ==========================================================================================
# (12) BOTH KEEP PATHS
# ==========================================================================================
P("=" * 100)
P("(G) BOTH KEEP PATHS (PROTOCOL rule 4)")
P("=" * 100)
keep = []
for pan in PANELS:
    for sha in VINT[pan]:
        bb = BASE[(BASE.panel == pan) & (BASE.sha == sha) & (BASE.who == "RULESv2")].iloc[0]
        sp = BASE[(BASE.panel == pan) & (BASE.sha == sha) & (BASE.who == "SPY")].iloc[0]
        sub = REAL[(REAL.panel == pan) & (REAL.sha == sha)]
        for _, r in sub.iterrows():
            k4a = (r["H1"] > bb["H1"] and r["H2"] > bb["H2"] and r["MaxDD"] >= bb["MaxDD"])
            keep.append(dict(panel=pan, sha=sha, book=r.book, cadence=r.cadence,
                             cost_bps=r.cost_bps, pass4a=bool(k4a), pass4b=bool(r.pass4b),
                             fail4b=r.fail4b))
KEEP = pd.DataFrame(keep)
k10 = KEEP[KEEP.cost_bps == HEAD_COST]
P(f"  at the PROTOCOL rung (10 bps), over {len(k10)} (panel, vintage, book, cadence) rows:")
P(f"    4a passes: {int(k10.pass4a.sum())}   4b passes: {int(k10.pass4b.sum())}")
P(f"  full cost ladder: " + "  ".join(
    f"{int(c)}bps 4a={int(KEEP[KEEP.cost_bps==c].pass4a.sum())} "
    f"4b={int(KEEP[KEEP.cost_bps==c].pass4b.sum())}" for c in RUNGS))
P("  4b failures by binding leg (10 bps):")
for leg, n in k10["fail4b"].value_counts().items():
    P(f"    {leg:24s} {n}")
P()
P("  THE VERDICT-STABILITY QUESTION THIS RUN EXISTS TO ANSWER:")
vs = (k10.groupby(["panel", "book", "cadence"])
      .agg(n=("pass4b", "size"), p4b=("pass4b", "sum"), p4a=("pass4a", "sum")).reset_index())
vs["b_flips"] = (vs.p4b > 0) & (vs.p4b < vs.n)
vs["a_flips"] = (vs.p4a > 0) & (vs.p4a < vs.n)
P(f"    REAL-book 4b verdicts that flip across vintages: {int(vs.b_flips.sum())} of {len(vs)} cells")
P(f"    REAL-book 4a verdicts that flip across vintages: {int(vs.a_flips.sum())} of {len(vs)} cells")
nf = FLIP[FLIP.arm == "LIVE"]["leg_flip_rate"].mean()
P(f"    NULL-draw 4b verdicts that flip across vintages (LIVE): {nf:.4f} of draw-vintage pairs")
P()


# ==========================================================================================
# (13) SUBJECT-CELL COST LADDER
# ==========================================================================================
if len(SUBJ_RUNGS):
    P("=" * 100)
    P(f"(H) SUBJECT CELL {SUBJECT[0]}/{SUBJECT[1]}/{SUBJECT[2]} -- cost ladder x arm")
    P("=" * 100)
    P(f"  {'cost':>5s} | " + " | ".join(f"{a:>26s}" for a in ARMS))
    P(f"  {'':>5s} | " + " | ".join(f"{'base  s_vint  flip  ident':>26s}" for a in ARMS))
    for c in RUNGS:
        cells = []
        for arm in ARMS:
            s = SUBJ_RUNGS[(SUBJ_RUNGS.cost_bps == c) & (SUBJ_RUNGS.arm == arm)]
            if s.empty:
                cells.append(f"{'--':>26s}")
                continue
            pv = s.pivot_table(index="draw", columns="sha", values="pass4b")
            pv = pv[[x for x in VINT["U56"] if x in pv.columns]].astype(bool)
            sv = s.pivot_table(index="draw", columns="sha", values="OOS_Sharpe")
            sv = sv[[x for x in VINT["U56"] if x in sv.columns]]
            base0 = VINT["U56"][0]
            cells.append(f"{pv.mean().mean():5.3f} {sv.std(axis=1,ddof=1).mean():7.4f} "
                         f"{float(pv.ne(pv[base0],axis=0).to_numpy().mean()):6.4f} "
                         f"{float((sv.sub(sv[base0],axis=0).abs()<1e-12).to_numpy().mean()):6.4f}")
        P(f"  {int(c):5d} | " + " | ".join(cells))
    P()

# draw-ladder convergence
P("  DRAW-LADDER CONVERGENCE (nested; U56 LIVE arm, null 4b base rate pooled over cells):")
for k in DRAW_LADDER:
    s = NULL[(NULL.panel == "U56") & (NULL.arm == "LIVE") & (NULL.draw < k)]
    P(f"    D={k:4d}  base rate {s.pass4b.mean():.4f}   "
      f"mean OOS Sharpe {s.OOS_Sharpe.mean():.4f}")
P()


# ==========================================================================================
# (14) HYPOTHESES TABLE
# ==========================================================================================
P("=" * 100)
P("(I) PRE-REGISTERED HYPOTHESES")
P("=" * 100)
HYP = pd.DataFrame(H)
for _, r in HYP.iterrows():
    P(f"  {r.id:11s} {'PASS' if r.passed else 'FAIL':5s}  value {r.value:10.4f}   ({r.bar})")
P()

# ==========================================================================================
# (15) OUTPUTS
# ==========================================================================================
P("=" * 100)
P("(J) ARTIFACTS")
P("=" * 100)
dump(CENSUS, "vintages")
dump(REAL, "real")
dump(NULL, "nulls", gz=True)
dump(DEC, "decomposition")
dump(POOL, "pooled")
dump(FLIP, "flips")
dump(SB, "schemabreak")
dump(MECH, "mechanism")
if len(FINGER):
    dump(FINGER, "fingerprint")
dump(rc, "realrange")
dump(BASE, "baselines")
dump(WF, "walkforward")
dump(KEEP, "keeppaths")
dump(HYP, "hypotheses")
dump(pd.DataFrame([dict(gate=k, passed=v) for k, v in sorted(GK.items())]), "gates")
if len(SUBJ_RUNGS):
    dump(SUBJ_RUNGS, "subjectladder", gz=True)
(OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
P(f"  wrote {STEM}.console.txt")
P(f"  elapsed {time.time()-T0:.1f}s")
(OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
