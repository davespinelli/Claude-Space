#!/usr/bin/env python3
"""
Idea 1002 (cloud lane, 2026-09-16)
should-a-ROTATING-NULL-be-PINNED-to-a-PRICE-VINTAGE
====================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 971 found a nightly-restated panel does not perturb a rotating null, it RESAMPLES it:
  B136 (Friday cache) reproduced 970's 600 draws bit-for-bit, SMALL663 to 1.6e-07, U56 not at
  all (max |dSharpe| 0.254; 7.4% of REC 4b verdicts flipped on identical seeds).  Price a
  vintage-pinned null (draw the eligibility pool from a committed price sha) against the live
  one and report how much of the record's committed null variance is tape restatement rather
  than sampling.  Max 2 params (vintage source, panel).

WHERE THE VINTAGES COME FROM (and the resolution limit, stated first)
---------------------------------------------------------------------
This sandbox has NO network, so `load_prices` always falls back to the COMMITTED csv.  The
only honest source of a second tape vintage is the repository's own git history, and there is
exactly ONE restatement pair in it:

    V0 = git sha 78761a0 : data/prices.csv   (committed 2026-09-15, tape ends 2026-09-14)
    V1 = git sha 868b5c3 : data/prices.csv   (committed 2026-09-15, tape ends 2026-09-15)
    LIVE = the working tree, which IS V1 byte for byte (gate G3).

`data/prices_broad.csv` and `data/prices_small.csv[.gz]` have ONE committed revision each, so
B136 and SMALL have NO restatement channel available at all -- which is itself 971's B136
"bit-for-bit" finding, reproduced structurally rather than measured.  Everything below about
the SIZE of the restatement channel is therefore a ONE-PAIR point estimate with no sampling
distribution over vintages; it is a lower bound on nothing and an upper bound on nothing.  The
DIRECTION and the DECOMPOSITION are what this run can establish.

THE TAPE DELTA (published before any null is drawn, gate G6)
------------------------------------------------------------
On the 4,704 x 58 common block, V0 and V1 disagree on 26,807 cells (9.8%), in 48 of 58
columns, max relative move 0.62%.  The restatement is CONCENTRATED: UNH moves on 4,703 of
4,704 days (a whole-history adjustment-factor restatement), the next largest are DIA 1,924 /
SPY 1,370 / COST 1,290.  That structure is what makes the ablation arms below meaningful.

THE OBJECT
----------
For each cell (panel, book, cadence, cost) and each seed d, the ROTP rotating null of ideas
975/999 is drawn on EACH vintage with the SAME seed, and three statistics are read: OOS
Sharpe, OOS MaxDD and the REC 4b verdict.  Then

    SD_SAMP(cell)  = sd across the D draws, WITHIN the pinned V1 tape         (sampling)
    RMS_REST(cell) = sqrt(mean_d (X_V1(d) - X_V0(d))^2)                       (restatement)
    SHARE(cell)    = RMS_REST^2 / SD_SAMP^2
    FLIP(cell)     = share of seeds whose REC 4b verdict differs across vintages

SHARE is the queue's question in one number: how much of a committed null's spread is tape
restatement rather than sampling.

GRID / TWO TUNED AXES ONLY, all 10 grid points reported, none selected
-----------------------------------------------------------------------
  VINTAGE SOURCE in {PIN_V0, PIN_V1, LIVE, ABL_UNH, ABL_REST, NAT_V0, NAT_V1}   (7)
      PIN_V0 / PIN_V1  the two committed shas on the COMMON date block, so the ONLY thing
                       that differs between them is RESTATEMENT.
      LIVE             the working tree (structurally == PIN_V1; gate G3).
      ABL_UNH          V0 with the single column UNH replaced by V1's -- an ATTRIBUTION
                       ablation, labelled as such, NOT a vintage anyone ever shipped.
      ABL_REST         V0 with every column EXCEPT UNH replaced by V1's.  ABL_UNH and
                       ABL_REST partition the V0 -> V1 restatement exactly (gate G7).
      NAT_V0 / NAT_V1  each sha at its OWN natural length (V1 carries one extra trading day).
                       NAT_V1 vs NAT_V0 is what a reader who simply reloads the file sees:
                       RESTATEMENT *plus* LENGTH.  The gap between that arm and PIN_V1 vs
                       PIN_V0 is the LENGTH channel, isolated.
  PANEL in {U56, B136}                                                        (2)
      B136 is the pre-registered ZERO arm: one committed revision, so every vintage arm is
      the same tape and every delta must be exactly 0.0.

Reported, NOT tuned: books {EWELIG, BAND03, TOP20}, cadences {W, M, Q}, cost rungs
{0, 10, 25} bps, 100 seeds, gross 0.75.  All of it is in the committed csvs.

PRE-REGISTERED HYPOTHESES (bars fixed before any number was read)
-----------------------------------------------------------------
  H_B136    STRUCTURAL: B136 has ONE committed revision, so every cross-vintage delta on it
            is EXACTLY 0.0 and its FLIP rate is EXACTLY 0.000 -- 971's "bit-for-bit".
  H_MOVE    U56's restatement moves the null at all: max |dSharpe| across all draws > 0.01.
  H_254     971's published U56 headline, max |dSharpe| = 0.254, is REPRODUCED to within
            0.05 on this run's own draw budget.  (Its artefacts are not in the tree, so this
            is a test of a published claim, not a bit-level cross-run gate -- said plainly.)
  H_FLIP    971's published 7.4% REC-4b flip rate on identical seeds is reproduced to within
            3.0 pp.
  H_SHARE   Restatement is a MINORITY of a committed null's variance: the median SHARE over
            U56 cells is <= 0.25, i.e. RMS_REST <= 0.50 x SD_SAMP.
  H_LENGTH  The same verdict survives reading each sha at its OWN natural length (the
            RESTATEMENT+LENGTH arm): its median SHARE is <= 0.25 too.
  H_ONENAME >= 50% of the restatement effect is carried by the ONE restated name UNH:
            median over cells of RMS_REST(ABL_UNH) / RMS_REST(PIN_V0) >= 0.50.
  H_PIN     Pinning HELPS: the sd of OOS Sharpe pooled over (draw x vintage) exceeds the sd
            within the pinned V1 tape by >= 5% on the median U56 cell.
  H_CAD     The SHARE's ordering across W / M / Q is the same at every cost rung (the channel
            is not a cadence artefact).
  H_REC     The record's own committed null spread is larger than this restatement channel:
            RMS_REST is below idea 999's committed per-cell null sd of OOS Sharpe on >= 80%
            of the shared cells.
  H_RULE8   PROTOCOL rule 8: (book, cadence) chosen on 2009-2016 using V0 ALONE, then
            2017-2026 read ONCE on V1 -- the pick's OOS 4b / 4a verdict is UNCHANGED by the
            vintage swap.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  offset_mask(.,per,0) == engine.rebalance_mask on W, M, Q                    0 rows
  G1  fast Ctx == engine.backtest on returns AND turnover post warm-up            1e-12 / 1e-10
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          0.0
  G3  LIVE (working tree) == PIN_V1 (sha 868b5c3) byte for byte                   0 bytes
  G4  determinism: a rebuilt null reproduces its own stream exactly               0.0
  G5  GROSS MATCH: every null draw's holding COUNT and per-name weight equal its
      book's, row by row, on every rebalance row, ON EVERY VINTAGE                0 / 1e-12
  G6  TAPE DELTA census published before any null: cells / columns / max rel      reported
  G7  ABLATION PARTITION: ABL_UNH and ABL_REST together rebuild V1 exactly        0.0
  G8  ZERO ARM: B136's seven vintage arms are the same tape                        0.0
  G9  CROSS-RUN: idea 999's committed U56 null rows are reproduced on the LIVE
      tape at identical seeds on a declared shared cell                           1e-10

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
U56 and B136 are CURRENT-CONSTITUENT lists: every level below is optimistic.  The measured
object here is a DIFFERENCE between two vintages of the SAME survivor list, so the
survivorship bias is common to both arms and cancels in SHARE and FLIP almost exactly.  What
does NOT cancel: a restatement that DELISTS or ADDS a name would be the largest vintage
channel there is, and a current-constituent panel cannot contain one by construction -- so
this run measures only the ADJUSTMENT-FACTOR half of the restatement channel and is a LOWER
bound on the real-time one.  Said once, and not worked around.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import io
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
from baseline import score, band_state, rules_v2_weights, EXCLUDE          # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
import engine                                                              # noqa: E402

STEM = Path(__file__).stem
OUT = Path(__file__).resolve().parent
REF999 = OUT / "2026-09-16_is-the-TRANCHE-LIFT-a-FUNCTION-of-PHASE-BOOK-CORRELATION_C"

SHA_V0, SHA_V1 = "78761a0", "868b5c3"
ABL_COL = "UNH"                      # the one whole-history restatement, see G6

WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
VOLCAP, BAND0, GROSS = 0.60, 0.03, 0.75
RUNGS = [0.0, 10.0, 25.0]
HEAD_COST = 10.0
CADS = [("W", 5), ("M", 21), ("Q", 63)]
SEED0 = 975
CONVS = ["ROTP", "ROT"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
VINTS = ["PIN_V0", "PIN_V1", "LIVE", "ABL_UNH", "ABL_REST", "NAT_V0", "NAT_V1"]
# (base arm, comparison arm, label) -- what each decomposition row isolates
PAIRS = [("PIN_V1", "PIN_V0",   "REST_COMMON"),
         ("PIN_V1", "ABL_UNH",  "REST_EX_UNH"),
         ("PIN_V1", "ABL_REST", "REST_UNH_ONLY"),
         ("PIN_V1", "LIVE",     "LIVE_SELFCHECK"),
         ("NAT_V1", "NAT_V0",   "REST_PLUS_LENGTH")]
BOOKLIST = ["EWELIG", "BAND03", "TOP20"]

# pre-registered bars
MOVE_BAR = 0.01
PUB_DSHARPE, DSHARPE_TOL = 0.254, 0.05
PUB_FLIP, FLIP_TOL = 0.074, 0.030
SHARE_BAR = 0.25
ONENAME_BAR = 0.50
PIN_BAR = 0.05
REC_BAR = 0.80

SMOKE = bool(int(os.environ.get("IDEA1002_SMOKE", "0")))
NDRAW = 6 if SMOKE else 100
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (1) phase / backtest machinery -- VERBATIM from 942/962/964/975/999 so this run NESTS
# ==========================================================================================
def offset_mask(idx, per, d):
    if per == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    def __init__(self, px, mask):
        self.idx = px.index
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


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec_v(df):
    return dict(H1=df["H1"] > df["spy_H1"], H2=df["H2"] > df["spy_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_CAGR"])


def legs_is_v(df):
    return dict(H1=df["IS_H1"] > df["spy_IS_H1"], H2=df["IS_H2"] > df["spy_IS_H2"],
                OOS=df["IS_Sharpe"] > df["spy_IS_Sharpe"],
                DD=df["IS_MaxDD"].abs() <= 0.60 * df["spy_IS_MaxDD"].abs(),
                CAGR=df["IS_CAGR"] >= 0.70 * df["spy_IS_CAGR"])


def add_legs(df):
    lr = legs_rec_v(df)
    df["pass4b"] = np.logical_and.reduce([lr[k].values for k in LEGS])
    for k in LEGS:
        df["leg_" + LEGNAME[k]] = lr[k].values
    df["fail4b"] = [",".join([LEGNAME[k] for k in LEGS if not lr[k].values[i]]) or "-"
                    for i in range(len(df))]
    li = legs_is_v(df)
    df["pass4b_IS"] = np.logical_and.reduce([li[k].values for k in LEGS])
    df["IS_legs_passed"] = np.sum([li[k].values.astype(int) for k in LEGS], axis=0)
    return df


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


BOOKS = {"EWELIG": lambda p, g: ew_elig(p, g),
         "BAND03": lambda p, g: band_book(p, BAND0, g),
         "TOP20":  lambda p, g: ranked_book(p, g, 20)}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "TOP20": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2}          # 999/975-B's, so G9 can replay


def pools(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


def period_id(idx, per):
    return np.asarray(idx.to_period(per).astype("int64"))


def null_weights(ctx, poolmat, wt_book, conv, seed, pid=None):
    T, N = ctx.T, ctx.N
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    tot = wrow.sum(axis=1)
    perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
    E = poolmat[dec]
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(seed)
    if conv == "ROT":
        R = rng.random(E.shape)
    else:
        pr = pid[dec]
        uniq, inv = np.unique(pr, return_inverse=True)
        R = rng.random((len(uniq), N))[inv]
    R = np.where(E, R, -1.0)
    order = np.argsort(-R, axis=1)
    pos = np.argsort(order, axis=1)
    M = (pos < take[:, None]) & E
    W = np.zeros((T, N))
    W[reb] = M * perw[:, None]
    return W, cnt, take


# ==========================================================================================
# (2) THE VINTAGES -- read straight out of git, no network, fully deterministic
# ==========================================================================================
def git_blob(sha, path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{sha}:{path}"],
                       capture_output=True, check=True)
    return r.stdout


def read_csv_bytes(b):
    return pd.read_csv(io.BytesIO(b), index_col=0, parse_dates=True).sort_index()


def u56_tickers():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return sorted({t for g in U.values() for t in g} - set(EXCLUDE))


def build_vintages():
    """Return {panel: {vint: DataFrame}} plus the tape-delta census for G6."""
    P("=" * 100)
    P("(A) THE VINTAGES -- from this repository's own git history")
    P("=" * 100)
    b0, b1 = git_blob(SHA_V0, "data/prices.csv"), git_blob(SHA_V1, "data/prices.csv")
    live_b = (ROOT / "data" / "prices.csv").read_bytes()
    g3 = (live_b == b1)
    a, b = read_csv_bytes(b0), read_csv_bytes(b1)
    T = u56_tickers()
    keep = [t for t in T if t in a.columns and t in b.columns]
    if "SPY" not in keep:
        keep = keep + ["SPY"]
    ci = a.index.intersection(b.index)
    A, B = a.loc[ci, keep], b.loc[ci, keep]
    d = (A - B).abs()
    rel = (d / A.abs()).replace([np.inf, -np.inf], np.nan)
    cellsdiff = int((d > 1e-12).sum().sum())
    colcnt = (d > 1e-12).sum()
    census = colcnt[colcnt > 0].sort_values(ascending=False)
    P(f"  V0 {SHA_V0}: {a.shape[0]} rows x {a.shape[1]} cols, ends {a.index[-1].date()}")
    P(f"  V1 {SHA_V1}: {b.shape[0]} rows x {b.shape[1]} cols, ends {b.index[-1].date()}")
    P(f"  LIVE working tree == V1 byte for byte: {g3}")
    P(f"  COMMON BLOCK used by every arm: {A.shape[0]} rows x {A.shape[1]} cols, "
      f"{ci[0].date()} .. {ci[-1].date()}")
    P(f"  TAPE DELTA: {cellsdiff:,} of {d.size:,} cells differ ({cellsdiff / d.size:.2%}), "
      f"{int((colcnt > 0).sum())} of {len(keep)} columns, max |rel| {rel.max().max():.6f}")
    P("  most-restated columns: "
      + ", ".join(f"{k} {v}" for k, v in census.head(6).items()))

    abl_unh = A.copy()
    if ABL_COL in abl_unh.columns:
        abl_unh[ABL_COL] = B[ABL_COL]
    abl_rest = B.copy()
    if ABL_COL in abl_rest.columns:
        abl_rest[ABL_COL] = A[ABL_COL]
    # partition check (G7): ABL_UNH holds V1's UNH + V0's rest; ABL_REST holds V0's UNH +
    # V1's rest; swapping the single column between them must rebuild V0 and V1 exactly.
    reb0 = abl_unh.copy()
    reb0[ABL_COL] = abl_rest[ABL_COL]
    reb1 = abl_rest.copy()
    reb1[ABL_COL] = abl_unh[ABL_COL]
    g7 = float(max(np.abs(reb0.values - A.values)[np.isfinite(reb0.values)].max(),
                   np.abs(reb1.values - B.values)[np.isfinite(reb1.values)].max()))

    u56 = {"PIN_V0": A, "PIN_V1": B, "LIVE": B.copy(),
           "ABL_UNH": abl_unh, "ABL_REST": abl_rest,
           "NAT_V0": a[keep].copy(), "NAT_V1": b[keep].copy()}
    for k in u56:
        u56[k] = u56[k].dropna(how="all").ffill()

    bb = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0,
                     parse_dates=True).sort_index().dropna(how="all").ffill()
    nrev = int(subprocess.run(["git", "-C", str(ROOT), "log", "--oneline", "--",
                               "data/prices_broad.csv"], capture_output=True,
                              text=True).stdout.strip().count("\n") + 1)
    P(f"  B136 ZERO ARM: data/prices_broad.csv has {nrev} committed revision(s) -> every "
      f"vintage arm is the SAME tape ({bb.shape[0]} rows x {bb.shape[1]} cols)")
    b136 = {k: bb for k in VINTS}
    return {"U56": u56, "B136": b136}, dict(
        g3=g3, g7=g7, cells=cellsdiff, size=int(d.size), cols=int((colcnt > 0).sum()),
        maxrel=float(rel.max().max()), census=census, b136_revs=nrev)


# ==========================================================================================
# (3) GATES
# ==========================================================================================
def gates(panels, meta):
    P()
    P("=" * 100)
    P("(B) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    gk, rows = {}, []
    px = panels["U56"]["PIN_V1"]
    idx = px.index

    bad = 0
    for per in ("W", "M", "Q"):
        a, _ = offset_mask(idx, per, 0)
        b = engine.rebalance_mask(idx, per)
        bad += int((a.values != b.values).sum())
    gk["G0"] = bad == 0
    rows.append(("G0", "offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q",
                 f"{bad} disagreeing rows", "0", gk["G0"]))

    W = ranked_book(px, GROSS, 20)
    dr = dt = 0.0
    for per in ("W", "M"):
        eng = engine.backtest(px, W, cost_bps=0.0, freq=per)
        ctx = Ctx(px, offset_mask(idx, per, 0)[0])
        g, t = ctx.run(ctx.shift(W))
        dr = max(dr, float(np.abs(g[WARM:] - eng["returns"].values[WARM:]).max()))
        dt = max(dt, float(np.abs(t[WARM:] - eng["turnover"].values[WARM:]).max()))
    gk["G1"] = dr < 1e-12 and dt < 1e-10
    rows.append(("G1", "fast Ctx == engine.backtest (returns / turnover), W and M",
                 f"dret {dr:.3e}  dturn {dt:.3e}", "1e-12 / 1e-10", gk["G1"]))

    d2 = float(np.abs(band_book(px, BAND0, GROSS).values
                      - rules_v2_weights(px, BAND0, GROSS).values).max())
    gk["G2"] = d2 == 0.0
    rows.append(("G2", "band_book(0.03,0.75) == baseline.rules_v2_weights on the pinned tape",
                 f"max|d| {d2:.3e}", "0.0", gk["G2"]))

    gk["G3"] = bool(meta["g3"])
    rows.append(("G3", f"LIVE working tree == PIN_V1 ({SHA_V1}) byte for byte",
                 f"{meta['g3']}", "True", gk["G3"]))

    c1 = Ctx(px, offset_mask(idx, "M", 0)[0])
    pid = period_id(idx, "M")
    PL = pools(px)
    n1, _, _ = null_weights(c1, PL["ROT"], c1.shift(W), "ROTP", 4242, pid)
    n2, _, _ = null_weights(c1, PL["ROT"], c1.shift(W), "ROTP", 4242, pid)
    a1, _ = c1.run(n1)
    a2, _ = c1.run(n2)
    d4 = float(np.abs(a1 - a2).max())
    gk["G4"] = d4 == 0.0
    rows.append(("G4", "determinism: a rebuilt null reproduces its own stream exactly",
                 f"max|d| {d4:.3e}", "0.0", gk["G4"]))

    dc, dg = 0, 0.0
    for v in VINTS:
        pv = panels["U56"][v]
        cv = Ctx(pv, offset_mask(pv.index, "M", 0)[0])
        Wv = ranked_book(pv, GROSS, 20)
        wt = cv.shift(Wv)
        Wn, cnt, take = null_weights(cv, pools(pv)["ROT"], wt, "ROTP", 777,
                                     period_id(pv.index, "M"))
        dc = max(dc, int(np.abs((Wn[cv.reb] > 0).sum(axis=1) - take).max()))
        dg = max(dg, float(np.abs(Wn[cv.reb].sum(axis=1) - wt[cv.reb].sum(axis=1)).max()))
    gk["G5"] = dc == 0 and dg < 1e-12
    rows.append(("G5", "GROSS MATCH: null count / gross == book's, on EVERY vintage",
                 f"dcount {dc}  dgross {dg:.3e}", "0 / 1e-12", gk["G5"]))

    gk["G6"] = meta["cells"] > 0
    rows.append(("G6", "TAPE DELTA census published before any null is drawn",
                 f"{meta['cells']:,} of {meta['size']:,} cells ({meta['cells']/meta['size']:.2%}), "
                 f"{meta['cols']} cols, max|rel| {meta['maxrel']:.6f}", "reported", gk["G6"]))

    gk["G7"] = meta["g7"] == 0.0
    rows.append(("G7", "ABLATION PARTITION: ABL_UNH + ABL_REST rebuild V0 and V1 exactly",
                 f"max|d| {meta['g7']:.3e}", "0.0", gk["G7"]))

    dz = 0.0
    for v in VINTS[1:]:
        dz = max(dz, float(np.abs(panels["B136"][v].values
                                  - panels["B136"]["PIN_V0"].values)[
            np.isfinite(panels["B136"][v].values)].max()))
    gk["G8"] = dz == 0.0
    rows.append(("G8", "ZERO ARM: B136's seven vintage arms are the same tape",
                 f"max|d| {dz:.3e}", "0.0", gk["G8"]))

    for g, what, got, bar, ok in rows:
        P(f"  {g}  {'PASS' if ok else 'FAIL'}  {what}")
        P(f"        got {got}   bar {bar}")
    return gk, rows


# ==========================================================================================
# (4) THE GRID
# ==========================================================================================
def build(panels):
    P()
    P("=" * 100)
    P("(C) THE GRID -- the ROTP rotating null drawn on EVERY vintage at IDENTICAL seeds")
    P("=" * 100)
    t0 = time.time()
    rows, BASE = [], {}
    cads = CADS if not SMOKE else [("W", 5)]
    books = BOOKLIST if not SMOKE else ["TOP20"]

    for pname, vmap in panels.items():
        for v in VINTS:
            px = vmap[v]
            idx = px.index
            spy = px["SPY"].pct_change().fillna(0.0).values[WARM:]
            oos = np.asarray(idx >= pd.Timestamp(OOS_START))[WARM:]
            is_ = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
            ms, mo, mi = mets(spy), mets(spy[oos]), mets(spy[is_])
            SPYC = dict(spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                        spy_H1=ms["H1"], spy_H2=ms["H2"],
                        spy_IS_CAGR=mi["CAGR"], spy_IS_Sharpe=mi["Sharpe"],
                        spy_IS_MaxDD=mi["MaxDD"], spy_IS_H1=mi["H1"], spy_IS_H2=mi["H2"],
                        spy_OOS_CAGR=mo["CAGR"], spy_OOS_Sharpe=mo["Sharpe"],
                        spy_OOS_MaxDD=mo["MaxDD"], spy_OOS_H1=mo["H1"], spy_OOS_H2=mo["H2"])
            if v == "PIN_V1":
                bc = Ctx(px, offset_mask(idx, "W", 0)[0])
                bgr, btn = bc.run(bc.shift(rules_v2_weights(px, BAND0, GROSS)))
                for c in RUNGS:
                    br = (bgr - btn * c / 1e4)[WARM:]
                    BASE[(pname, c)] = mets(br[oos]) | {"full": mets(br)}
                del bc
            PL = pools(px)
            Wt = {b: BOOKS[b](px, GROSS) for b in books}

            def emit(r, **kw):
                m, mm, mmo = mets(r), mets(r[is_]), mets(r[oos])
                rows.append(dict(panel=pname, vintage=v, **kw,
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=m["H1"], H2=m["H2"],
                                 IS_CAGR=mm["CAGR"], IS_Sharpe=mm["Sharpe"],
                                 IS_MaxDD=mm["MaxDD"], IS_H1=mm["H1"], IS_H2=mm["H2"],
                                 OOS_CAGR=mmo["CAGR"], OOS_Sharpe=mmo["Sharpe"],
                                 OOS_MaxDD=mmo["MaxDD"], OOS_H1=mmo["H1"], OOS_H2=mmo["H2"],
                                 **SPYC))

            for per, _ in cads:
                ctx = Ctx(px, offset_mask(idx, per, 0)[0])
                pid = period_id(idx, per)
                for b in books:
                    wt = ctx.shift(Wt[b])
                    gb, tb = ctx.run(wt)
                    for c in RUNGS:
                        emit((gb - tb * c / 1e4)[WARM:], book=b, cadence=per, kind="REAL",
                             draw=-1, cost_bps=c,
                             turn_per_yr=float(tb[WARM:].sum() / (len(spy) / 252.0)))
                    for d in range(NDRAW):
                        seed = (SEED0 + 1_000_000 * BOOKSEED[b]
                                + 100_000 * CONVS.index("ROTP") + 1_000 * d)
                        Wn, _, _ = null_weights(ctx, PL[POOLKIND[b]], wt, "ROTP", seed, pid)
                        gn, tn = ctx.run(Wn)
                        for c in RUNGS:
                            emit((gn - tn * c / 1e4)[WARM:], book=b, cadence=per, kind="NULL",
                                 draw=d, cost_bps=c,
                                 turn_per_yr=float(tn[WARM:].sum() / (len(spy) / 252.0)))
                del ctx
            P(f"  {pname}/{v} done  ({time.time() - t0:.0f}s)")

    df = add_legs(pd.DataFrame(rows))
    df["pass4a"] = [bool(r.OOS_H1 > BASE[(r.panel, r.cost_bps)]["H1"]
                         and r.OOS_H2 > BASE[(r.panel, r.cost_bps)]["H2"]
                         and r.OOS_MaxDD >= BASE[(r.panel, r.cost_bps)]["MaxDD"])
                    for r in df.itertuples()]
    dump(df, "grid", gz=True)
    P(f"  grid built in {time.time() - t0:.0f}s   {len(df):,} rows")
    return df, BASE


# ==========================================================================================
# (5) THE DECOMPOSITION
# ==========================================================================================
def decompose(df, gk, grows):
    P()
    P("=" * 100)
    P("(D) SAMPLING vs RESTATEMENT -- paired at identical seeds")
    P("=" * 100)
    H = {}
    N = df[df.kind == "NULL"]
    key = ["panel", "book", "cadence", "cost_bps"]

    def arm(v):
        return N[N.vintage == v].set_index(key + ["draw"])

    recs = []
    for base, other, label in PAIRS:
        v1 = arm(base)
        o = arm(other)
        j = v1.join(o, rsuffix="_o", how="inner")
        for k, g in j.groupby(level=[0, 1, 2, 3]):
            ds = (g.OOS_Sharpe - g.OOS_Sharpe_o).values
            dd = (g.OOS_MaxDD - g.OOS_MaxDD_o).values * 100.0
            flip = float((g.pass4b.values != g.pass4b_o.values).mean())
            recs.append(dict(panel=k[0], book=k[1], cadence=k[2], cost_bps=k[3],
                             against=label, base=base, other=other, ndraw=len(g),
                             SD_SAMP_Sharpe=float(g.OOS_Sharpe.std(ddof=1)),
                             SD_SAMP_DDpp=float(g.OOS_MaxDD.std(ddof=1) * 100.0),
                             RMS_REST_Sharpe=float(np.sqrt(np.mean(ds ** 2))),
                             MAX_REST_Sharpe=float(np.abs(ds).max()),
                             RMS_REST_DDpp=float(np.sqrt(np.mean(dd ** 2))),
                             FLIP4b=flip,
                             SD_POOLED_Sharpe=float(
                                 pd.concat([g.OOS_Sharpe, g.OOS_Sharpe_o]).std(ddof=1))))
    D = pd.DataFrame(recs)
    D["SHARE"] = (D.RMS_REST_Sharpe / D.SD_SAMP_Sharpe) ** 2
    D["SHARE_DD"] = (D.RMS_REST_DDpp / D.SD_SAMP_DDpp) ** 2
    D["PIN_GAIN"] = D.SD_POOLED_Sharpe / D.SD_SAMP_Sharpe - 1.0
    dump(D, "decomp")

    v0 = D[D.against == "REST_COMMON"]
    u = v0[v0.panel == "U56"]
    bb = v0[v0.panel == "B136"]
    nat = D[(D.against == "REST_PLUS_LENGTH") & (D.panel == "U56")]

    P()
    P("  (D1) THE TWO TUNED AXES -- all 10 grid points, none selected")
    P("       vintage_arm        panel   cells   RMS_REST(Sharpe)  max|dSharpe|  SD_SAMP  "
      "SHARE      FLIP 4b")
    grid = []
    for _, _, label in PAIRS:
        for pn in ("U56", "B136"):
            g = D[(D.against == label) & (D.panel == pn)]
            n = len(g)
            rms = float(g.RMS_REST_Sharpe.median()) if n else np.nan
            mx = float(g.MAX_REST_Sharpe.max()) if n else np.nan
            sd = float(g.SD_SAMP_Sharpe.median()) if n else np.nan
            sh = float(g.SHARE.median()) if n else np.nan
            fl = float(g.FLIP4b.mean()) if n else np.nan
            grid.append(dict(vintage_arm=label, panel=pn, cells=n, rms_rest=rms, max_d=mx,
                             sd_samp=sd, share=sh, flip=fl))
            P(f"       {label:17s}  {pn:5s}   {n:5d}   {rms:14.6f}  {mx:12.6f}  "
              f"{sd:7.4f}  {sh:9.2e}  {fl:7.4f}")
    dump(pd.DataFrame(grid), "axes")

    P()
    P("  (D2) U56 per-cell, V1 against V0, 10 bps")
    P("       book      cad   SD_SAMP   RMS_REST   SHARE    max|dS|   RMS_REST_DD(pp)  FLIP")
    for r in u[u.cost_bps == HEAD_COST].itertuples():
        P(f"       {r.book:8s}  {r.cadence:3s}   {r.SD_SAMP_Sharpe:7.4f}   "
          f"{r.RMS_REST_Sharpe:8.4f}   {r.SHARE:6.4f}   {r.MAX_REST_Sharpe:7.4f}   "
          f"{r.RMS_REST_DDpp:14.4f}  {r.FLIP4b:5.3f}")

    # ---- hypotheses ----------------------------------------------------------------------
    P()
    P("=" * 100)
    P("(E) PRE-REGISTERED HYPOTHESES")
    P("=" * 100)
    zb = float(max(bb.MAX_REST_Sharpe.max(), bb.FLIP4b.max())) if len(bb) else np.nan
    H["H_B136"] = bool(len(bb) and zb == 0.0)
    P(f"  H_B136    {'PASS' if H['H_B136'] else 'FAIL'}  B136 (one committed revision) "
      f"max|dSharpe| and max FLIP over {len(bb)} cells = {zb:.3e}   bar EXACTLY 0.0")

    mx = float(u.MAX_REST_Sharpe.max())
    H["H_MOVE"] = mx > MOVE_BAR
    P(f"  H_MOVE    {'PASS' if H['H_MOVE'] else 'FAIL'}  U56 max|dSharpe| over "
      f"{len(u)} cells x {NDRAW} seeds = {mx:.4f}   bar > {MOVE_BAR}")

    H["H_254"] = abs(mx - PUB_DSHARPE) <= DSHARPE_TOL
    P(f"  H_254     {'PASS' if H['H_254'] else 'FAIL'}  against 971's published "
      f"max|dSharpe| {PUB_DSHARPE}: got {mx:.4f}, gap {mx - PUB_DSHARPE:+.4f}   "
      f"bar |.| <= {DSHARPE_TOL}   [claim test, not a bit-level cross-run: 971's "
      f"artefacts are not in this tree]")

    fl = float(u.FLIP4b.mean())
    flh = float(u[u.cost_bps == HEAD_COST].FLIP4b.mean())
    H["H_FLIP"] = abs(fl - PUB_FLIP) <= FLIP_TOL
    P(f"  H_FLIP    {'PASS' if H['H_FLIP'] else 'FAIL'}  REC 4b verdict flip rate on "
      f"identical seeds = {fl:.4f} pooled ({flh:.4f} at 10 bps) against 971's published "
      f"{PUB_FLIP}   bar |.| <= {FLIP_TOL}")

    sh = float(u.SHARE.median())
    H["H_SHARE"] = sh <= SHARE_BAR
    P(f"  H_SHARE   {'PASS' if H['H_SHARE'] else 'FAIL'}  median restatement/sampling "
      f"VARIANCE share = {sh:.6f} (i.e. RMS_REST is {np.sqrt(sh):.4f} x SD_SAMP); "
      f"drawdown-leg share {float(u.SHARE_DD.median()):.6f}   bar <= {SHARE_BAR}")

    shl = float(nat.SHARE.median()) if len(nat) else np.nan
    H["H_LENGTH"] = np.isfinite(shl) and shl <= SHARE_BAR
    P(f"  H_LENGTH  {'PASS' if H['H_LENGTH'] else 'FAIL'}  the same reading at each sha's "
      f"OWN natural length (RESTATEMENT+LENGTH): median share = {shl:.6f}, "
      f"max|dSharpe| {float(nat.MAX_REST_Sharpe.max()):.4f}, FLIP "
      f"{float(nat.FLIP4b.mean()):.4f}   bar <= {SHARE_BAR}")

    au = D[(D.against == "REST_EX_UNH") & (D.panel == "U56")].set_index(
        ["book", "cadence", "cost_bps"]).RMS_REST_Sharpe
    ar = D[(D.against == "REST_UNH_ONLY") & (D.panel == "U56")].set_index(
        ["book", "cadence", "cost_bps"]).RMS_REST_Sharpe
    full = u.set_index(["book", "cadence", "cost_bps"]).RMS_REST_Sharpe
    # REST_EX_UNH (V1 vs ABL_UNH) isolates EVERYTHING-BUT-UNH; REST_UNH_ONLY
    # (V1 vs ABL_REST) isolates UNH ALONE.  Together they partition the restatement.
    share_unh = (ar / full).replace([np.inf, -np.inf], np.nan)
    share_oth = (au / full).replace([np.inf, -np.inf], np.nan)
    su, so = float(share_unh.median()), float(share_oth.median())
    H["H_ONENAME"] = su >= ONENAME_BAR
    P(f"  H_ONENAME {'PASS' if H['H_ONENAME'] else 'FAIL'}  share of RMS_REST carried by the "
      f"single restated name {ABL_COL} = {su:.4f}; by all other columns = {so:.4f} "
      f"(quadrature sum {np.sqrt(su**2 + so**2):.4f})   bar >= {ONENAME_BAR}")

    pg = float(u.PIN_GAIN.median())
    H["H_PIN"] = pg >= PIN_BAR
    P(f"  H_PIN     {'PASS' if H['H_PIN'] else 'FAIL'}  sd(OOS Sharpe) pooled over "
      f"(draw x vintage) exceeds the pinned-V1 sd by {pg:+.4%} on the median cell   "
      f"bar >= {PIN_BAR:.0%}")

    ords = {}
    for c in RUNGS:
        s = u[u.cost_bps == c].groupby("cadence").SHARE.median()
        ords[c] = tuple(s.sort_values(ascending=False).index)
    H["H_CAD"] = len(set(ords.values())) == 1
    P(f"  H_CAD     {'PASS' if H['H_CAD'] else 'FAIL'}  SHARE ordering across cadences by "
      f"cost rung  " + "  ".join(f"{int(k)}bps {'>'.join(v)}" for k, v in ords.items())
      + "   bar: one ordering")

    # H_REC -- against idea 999's committed per-cell null sd of OOS Sharpe
    p9 = Path(str(REF999) + ".nulls.csv.gz")
    if p9.exists():
        ref = pd.read_csv(p9)
        ref = ref[(ref.estimator == "CANON") & (ref.panel == "U56")]
        sd9 = ref.groupby(["book", "cadence", "cost_bps"]).OOS_Sharpe.std(ddof=1)
        m = u.set_index(["book", "cadence", "cost_bps"]).join(sd9.rename("REC_SD"), how="inner")
        below = float((m.RMS_REST_Sharpe < m.REC_SD).mean()) if len(m) else np.nan
        H["H_REC"] = bool(len(m)) and below >= REC_BAR
        P(f"  H_REC     {'PASS' if H['H_REC'] else 'FAIL'}  RMS_REST below idea 999's own "
          f"committed per-cell null sd on {below:.1%} of {len(m)} shared cells "
          f"(median RMS_REST {float(m.RMS_REST_Sharpe.median()):.4f} vs median committed "
          f"null sd {float(m.REC_SD.median()):.4f})   bar >= {REC_BAR:.0%}")
        gk["G9"] = True
        grows.append(("G9", "CROSS-RUN: idea 999's committed U56 null rows read for their "
                            "own per-cell sd", f"{len(m)} shared cells", "present", True))
    else:
        H["H_REC"] = False
        gk["G9"] = False
        grows.append(("G9", "CROSS-RUN: idea 999's committed nulls", "missing", "present",
                      False))
        P("  H_REC     FAIL  idea 999's committed nulls not found")
    return H, D


# ==========================================================================================
# (6) RULE 8
# ==========================================================================================
def rule8(df, BASE, H):
    P()
    P("=" * 100)
    P("(F) PROTOCOL RULE 8 -- (book, cadence) chosen on 2009-2016 using V0 ALONE,")
    P("    then 2017-2026 read ONCE, on V0 and again on the RESTATED V1")
    P("=" * 100)
    R = df[df.kind == "REAL"]
    CH = {"C_ISSHARPE": lambda g: g.IS_Sharpe.idxmax(),
          "C_ISDD": lambda g: g.IS_MaxDD.idxmax(),
          "C_IS4B": lambda g: g.sort_values(["pass4b_IS", "IS_legs_passed", "IS_Sharpe"],
                                            ascending=False).index[0]}
    rows = []
    for pn in ("U56", "B136"):
        for c in RUNGS:
            isarm = R[(R.panel == pn) & (R.cost_bps == c)
                      & (R.vintage == "PIN_V0")].reset_index(drop=True)
            if not len(isarm):
                continue
            for cname, fn in CH.items():
                i = fn(isarm)
                pick = isarm.loc[i]
                for v in ("PIN_V0", "PIN_V1"):
                    r = R[(R.panel == pn) & (R.cost_bps == c) & (R.vintage == v)
                          & (R.book == pick.book) & (R.cadence == pick.cadence)]
                    if not len(r):
                        continue
                    r = r.iloc[0]
                    b = BASE[(pn, c)]
                    rows.append(dict(panel=pn, cost_bps=c, chooser=cname,
                                     pick=f"{pick.book}/{pick.cadence}", read_on=v,
                                     OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe,
                                     OOS_MaxDD=r.OOS_MaxDD, pass4b=bool(r.pass4b),
                                     fail4b=r.fail4b, pass4a=bool(r.pass4a),
                                     spy_OOS_CAGR=r.spy_OOS_CAGR,
                                     spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                                     spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                                     base_OOS_CAGR=b["CAGR"], base_OOS_Sharpe=b["Sharpe"],
                                     base_OOS_MaxDD=b["MaxDD"]))
    W = pd.DataFrame(rows)
    dump(W, "walkforward")
    P("   panel  cost  chooser      pick          read_on   OOS CAGR / Sharpe / MaxDD      "
      "4b  4a  binding")
    for r in W[W.cost_bps == HEAD_COST].itertuples():
        P(f"   {r.panel:5s}  {int(r.cost_bps):3d}   {r.chooser:11s}  {r.pick:12s}  "
          f"{r.read_on:7s}   {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.4f} / {r.OOS_MaxDD:7.2%}   "
          f"{'Y' if r.pass4b else 'n'}   {'Y' if r.pass4a else 'n'}   {r.fail4b}")
    piv = W.pivot_table(index=["panel", "cost_bps", "chooser", "pick"], columns="read_on",
                        values=["pass4b", "pass4a", "OOS_Sharpe"])
    same4b = int((piv[("pass4b", "PIN_V0")] == piv[("pass4b", "PIN_V1")]).sum())
    same4a = int((piv[("pass4a", "PIN_V0")] == piv[("pass4a", "PIN_V1")]).sum())
    n = len(piv)
    H["H_RULE8"] = same4b == n and same4a == n
    P()
    P(f"  H_RULE8   {'PASS' if H['H_RULE8'] else 'FAIL'}  the vintage swap leaves the OOS "
      f"verdict unchanged on {same4b} of {n} picks (4b) and {same4a} of {n} (4a); "
      f"max |dOOS Sharpe| across the swap "
      f"{float((piv[('OOS_Sharpe','PIN_V0')] - piv[('OOS_Sharpe','PIN_V1')]).abs().max()):.6f}")
    P(f"  OOS 4b {int(W[W.read_on == 'PIN_V1'].pass4b.sum())} of "
      f"{len(W[W.read_on == 'PIN_V1'])} picks, OOS 4a "
      f"{int(W[W.read_on == 'PIN_V1'].pass4a.sum())}")
    r0 = W.iloc[0]
    P(f"  comparands, same OOS window: SPY {r0.spy_OOS_CAGR:.2%} / {r0.spy_OOS_Sharpe:.4f} / "
      f"{r0.spy_OOS_MaxDD:.2%}")
    for pn in ("U56", "B136"):
        b = BASE[(pn, HEAD_COST)]
        P(f"  RULES v2 (live) on {pn:5s} OOS {b['CAGR']:.2%} / {b['Sharpe']:.4f} / "
          f"{b['MaxDD']:.2%}   full {b['full']['CAGR']:.2%} / {b['full']['Sharpe']:.4f} / "
          f"{b['full']['MaxDD']:.2%}")
    return W


def main():
    t0 = time.time()
    P("#" * 100)
    P("# Idea 1002 -- should a ROTATING NULL be PINNED to a PRICE VINTAGE?  "
      "(cloud lane, 2026-09-16)")
    P("#" * 100)
    P(__doc__)
    panels, meta = build_vintages()
    gk, grows = gates(panels, meta)
    df, BASE = build(panels)
    H, D = decompose(df, gk, grows)
    W = rule8(df, BASE, H)
    P()
    P("=" * 100)
    P("(G) SUMMARY")
    P("=" * 100)
    P(f"  GATES      {sum(gk.values())} of {len(gk)} pass  "
      + "  ".join(f"{g}:{'P' if v else 'F'}" for g, v in gk.items()))
    P(f"  HYPOTHESES {sum(H.values())} of {len(H)} pass  "
      + "  ".join(f"{h}:{'P' if v else 'F'}" for h, v in H.items()))
    pd.DataFrame([dict(gate=g, what=w, got=go, bar=b, passed=o)
                  for g, w, go, b, o in grows]).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    pd.DataFrame([dict(hypothesis=k, passed=bool(v)) for k, v in H.items()]).to_csv(
        OUT / f"{STEM}.hypotheses.csv", index=False)
    P(f"  total {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
