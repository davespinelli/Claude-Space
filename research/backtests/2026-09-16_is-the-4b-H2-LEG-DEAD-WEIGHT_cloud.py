#!/usr/bin/env python3
"""
Idea 1014 (cloud lane, 2026-09-16, idea 2 of 2)
is-the-4b-H2-LEG-DEAD-WEIGHT
============================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 1001 found the H2 leg passes at EVERY window on BOTH book sets (leg2 rate 1.000 on
  45 books x 5 windows, comparand sd 0.0118, comparand carries 0 of 9) so `r_leg2_spyH2` is
  undefined for want of variance.  Census every committed 4b FAIL row in the record for
  whether `L_H2` was ever the binding leg, and report whether the clause removes anything
  at all.  Max 2 params (claim set, binding definition).

WHAT "THE CLAUSE REMOVES ANYTHING" MEANS, ARITHMETICALLY
-------------------------------------------------------
4b is a CONJUNCTION of five legs.  Deleting a leg L from the conjunction is MONOTONE: it can
never turn a PASS into a FAIL, and it turns a FAIL into a PASS **exactly** when L is the SOLE
binding leg of that row.  So "does the `L2_H2` clause remove anything" has a closed form:

        rows the deletion flips  ==  rows whose binding set is exactly {L2_H2}

and this run measures that directly (gate G7 asserts the identity row by row rather than
assuming it).  The same statistic is computed for all FIVE legs, because "dead weight" is a
comparative claim and a leg can only be dead weight RELATIVE to the others.

Three quantities, per leg, per arm:
  IN-FAIL   share of committed FAIL rows whose binding set CONTAINS the leg
  SOLE      share whose binding set IS the leg  ( == the deletion-flip rate)
  NESTED    P(`L1_H1` also fails | the leg fails) -- is the leg saying anything `L1_H1` is
            not already saying?
and one two-sided reading of the deletion, because a share of FAIL rows understates it:
  the flipped rows as a fraction of the record's committed 4b PASS population.

TUNED AXIS 1 -- CLAIM SET (4 levels, all reported, none selected)
  ALLROWS   every parsed committed 4b FAIL row
  REALROWS  null-draw rows removed
  FILEWT    each committed CSV counts once (its own within-file share)
  FRESH     this run's own priced ladder, where all five legs are known exactly
TUNED AXIS 2 -- BINDING DEFINITION (3 levels, all reported, none selected)
  STRICT    the committed `fail4b` token set, read literally
  RECOMP    the committed string IGNORED; all five legs recomputed from the row's own
            numerics against the SPY comparands committed in the SAME file
  FAMILY    SHARPE = {H1, H2, OOS} vs DD vs CAGR -- the weakest reading, under which
            deleting "the H2 leg" means deleting the whole Sharpe family
12 cells.  No third dial is moved.

CORPUS: every committed `research/backtests/*.csv[.gz]` carrying a column literally named
`fail4b` -- the same corpus definition idea 1010 pinned, so gate G3 can cross-run its
committed `.census.csv` share by share.

PRE-REGISTERED HYPOTHESES (bars fixed before any number of this run was read)
-----------------------------------------------------------------------------
  H_DEAD    THE QUESTION.  `L2_H2` is in the binding set of < 25% of committed FAIL rows.
  H_NOFLIP  Deleting `L2_H2` from 4b flips < 0.5% of committed FAIL rows to PASS -- the
            clause removes essentially nothing.
  H_LEAST   `L2_H2` is the LEAST pivotal of the five legs (lowest deletion-flip rate) in
            EVERY claim-set x definition cell.  If this fails, the record has a deader leg
            than the one 1001 named.
  H_NEST    `L2_H2` is redundant with `L1_H1`: P(`L1_H1` fails | `L2_H2` fails) >= 0.90.
  H_1001    1001's rate claim on fresh prices: `p_L2_H2` == 1.000 on the priced ladder.
            Bar >= 0.95, pooled over the ladder.
  H_STABLE  The deletion-flip rate for `L2_H2` stays under 0.5% in ALL 12 tuned cells --
            the answer does not depend on which of the two dials you turn.
  H_RULE8   PROTOCOL rule 8.  Picks chosen on 2009-2016 alone, OOS read once, score
            IDENTICALLY under 4b and under 4b-minus-H2 -- the clause changes no verdict
            this run can reach.

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  ALPHABET CLOSURE: every non-empty `fail4b` value parses into the 5-leg
      alphabet; unparsed values are EXCLUDED and counted, never guessed at         count
  G1  PASS/FAIL CONSISTENCY: where a file carries `pass4b`, pass4b == (the
      binding set is empty) on every row                                    0 disagreeing
  G2  LEG-BOOL CONSISTENCY: where a file carries the five `leg_*` booleans,
      the token set equals the set of False legs                            0 disagreeing
  G3  CROSS-RUN: idea 1010's committed `.census.csv` sole-binder shares
      reproduced on every shared (claimset, defn) cell                             1e-12
  G4  fast Ctx == engine.backtest on returns AND turnover post warm-up      1e-12 / 1e-10
  G5  CROSS-RUN: SPY OOS == the record's committed 15.21% / 0.8713 / -33.72%       0.005
  G6  determinism: a rebuilt fresh cell reproduces its own stream exactly            0.0
  G7  DELETION IDENTITY: recomputing the 4b verdict with `L2_H2` deleted flips
      EXACTLY the rows whose binding set is {L2_H2}, and flips no PASS to FAIL 0 disagreeing

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
The RECORD arm is a census of committed text and inherits whatever bias its source files
carried.  The FRESH arm runs on U56 / B136, which are CURRENT-CONSTITUENT lists, so realised
CAGR is lifted and drawdowns compressed.  That cuts SPECIFICALLY against this run's own
hypotheses in a nameable direction: survivorship raises a book's Sharpe in BOTH halves
together, which makes the half-sample legs EASIER to clear and therefore makes `L2_H2` look
DEADER than it would on a real-time panel.  Every "dead weight" reading below is an UPPER
bound on deadness; the deletion-flip counts are a LOWER bound.

NOT MODIFIED (PROTOCOL rule 6): RULES.md, PROTOCOL.md, scan.py, bot.py, baseline.py.
"""
from __future__ import annotations

import gzip
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, band_state, rules_v2_weights   # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
import engine                                                             # noqa: E402

STEM = Path(__file__).stem
OUT = Path(__file__).resolve().parent
BT = ROOT / "research" / "backtests"

WARM = 260
OOS_START = "2017-01-01"
VOLCAP, BAND0, GROSS = 0.60, 0.03, 0.75
RUNGS = [0.0, 10.0, 25.0]
HEAD = 10.0
CADS = ["D", "W", "M", "Q"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
FAMILY = {"H1": "SHARPE", "H2": "SHARPE", "OOS": "SHARPE", "DD": "DD", "CAGR": "CAGR"}
PASS_SENTINEL = {"-", "", "none", "NONE", "None", "nan", "-none-", "NaN", "n/a"}
BIT = {k: 1 << i for i, k in enumerate(LEGS)}
FAMBIT = {"SHARPE": BIT["H1"] | BIT["H2"] | BIT["OOS"], "DD": BIT["DD"], "CAGR": BIT["CAGR"]}

REC_SPY_OOS = dict(CAGR=0.1521, Sharpe=0.8713, MaxDD=-0.3372)
SEED0 = 1014

SMOKE = bool(int(os.environ.get("IDEA1014_SMOKE", "0")))
DRAWS = 20 if SMOKE else 100
PANELS_WANTED = ["U56"] if SMOKE else ["U56", "B136"]

# pre-registered bars
BAR_DEAD = 0.25
BAR_NOFLIP = 0.005
BAR_NEST = 0.90
BAR_1001 = 0.95

LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (0) the token alphabet -- 1010's, verbatim, so G3 can cross-run its census
# ==========================================================================================
TOKMAP = {}
for k, v in LEGNAME.items():
    TOKMAP[k] = k
    TOKMAP[v] = k
for extra, leg in (("L5_CAGRfloor", "CAGR"), ("CAGRfloor", "CAGR"), ("CAGRFLOOR", "CAGR"),
                   ("DDcap", "DD"), ("DDCAP", "DD"), ("L4_DDcap", "DD")):
    TOKMAP[extra] = leg
TOKMAP = {k.upper(): v for k, v in TOKMAP.items()}
SPLIT = re.compile(r"[,|;+/ ]+")
NULL_KIND = re.compile(r"draw|null", re.I)
NUMSET = ["H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "OOS_CAGR",
          "spy_H1", "spy_H2", "spy_OOS_Sharpe", "spy_MaxDD", "spy_CAGR"]
LEGBOOLSETS = [["leg_L1_H1", "leg_L2_H2", "leg_L3_OOS", "leg_L4_DD", "leg_L5_CAGR"],
               ["leg_H1", "leg_H2", "leg_OOS", "leg_DD", "leg_CAGR"]]


def parse_fail(s):
    if s is None:
        return 0, False
    t = str(s).strip()
    if t in PASS_SENTINEL:
        return 0, True
    m = 0
    for tok in SPLIT.split(t):
        if not tok:
            continue
        k = TOKMAP.get(tok.strip().upper())
        if k is None:
            return 0, False
        m |= BIT[k]
    return m, True


def header_of(p: Path):
    op = gzip.open(p, "rt") if p.name.endswith(".gz") else open(p, newline="")
    with op as fh:
        line = fh.readline()
    return [c.strip() for c in line.rstrip("\n").rstrip("\r").split(",")]


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "1.0", "yes", "t")


def legs_rec_v(df):
    """The RECORD's 4b convention, vectorised -- 1010/1007/975's, verbatim."""
    return dict(H1=df["H1"] > df["spy_H1"], H2=df["H2"] > df["spy_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_CAGR"])


# ==========================================================================================
# (1) price machinery -- 942/962/964/975/1007/1009's, verbatim
# ==========================================================================================
def offset_mask(idx, per):
    if per == "D":
        return pd.Series(True, index=idx)
    key = pd.Series(idx.to_period(per), index=idx)
    return key != key.shift(-1)


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


def cagr(r):
    eq = np.cumprod(1.0 + r)
    y = len(r) / 252.0
    return float(eq[-1] ** (1 / y) - 1) if y > 0 else np.nan


def profile(r, oi):
    h = len(r) // 2
    o, i_ = r[oi:], r[:oi]
    hi = len(i_) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r[:h]), H2=sharpe(r[h:]),
                OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o),
                IS_CAGR=cagr(i_), IS_Sharpe=sharpe(i_), IS_MaxDD=maxdd(i_),
                IS_H1=sharpe(i_[:hi]), IS_H2=sharpe(i_[hi:]))


def legs_of(d, spy):
    return dict(H1=d["H1"] > spy["H1"], H2=d["H2"] > spy["H2"],
                OOS=d["OOS_Sharpe"] > spy["OOS_Sharpe"],
                DD=abs(d["OOS_MaxDD"]) <= 0.60 * abs(spy["OOS_MaxDD"]),
                CAGR=d["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def legs_is(d, spy):
    return dict(H1=d["IS_H1"] > spy["IS_H1"], H2=d["IS_H2"] > spy["IS_H2"],
                OOS=d["IS_Sharpe"] > spy["IS_Sharpe"],
                DD=abs(d["IS_MaxDD"]) <= 0.60 * abs(spy["IS_MaxDD"]),
                CAGR=d["IS_CAGR"] >= 0.70 * spy["IS_CAGR"])


def mask_of(lg):
    m = 0
    for k in LEGS:
        if not lg[k]:
            m |= BIT[k]
    return m


def maskname(m):
    return ",".join(LEGNAME[k] for k in LEGS if m & BIT[k]) or "-"


# ---- books ------------------------------------------------------------------------------
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
         "TOP20":  lambda p, g: ranked_book(p, g, 20),
         "TOP10":  lambda p, g: ranked_book(p, g, 10),
         "TOP40":  lambda p, g: ranked_book(p, g, 40)}
POOLKIND = {"EWELIG": "EW", "BAND03": "BD", "TOP20": "ROT", "TOP10": "ROT", "TOP40": "ROT"}
BOOKSEED = {"EWELIG": 0, "BAND03": 1, "TOP20": 2, "TOP10": 3, "TOP40": 4}
CADSEED = {"D": 0, "W": 1, "M": 2, "Q": 3}
PANSEED = {"U56": 0, "B136": 1}


def pools(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    return {"EW": px.notna().values, "BD": px.notna().values,
            "ROT": (elig & sc.notna()).values}


def period_id(idx, per):
    if per == "D":
        return np.arange(len(idx), dtype="int64")
    return np.asarray(idx.to_period(per).astype("int64"))


def null_weights(ctx, poolmat, wt_book, seed, pid):
    T, N = ctx.T, ctx.N
    reb, dec = ctx.reb, ctx.dec
    wrow = wt_book[reb]
    cnt = (wrow > 0).sum(axis=1)
    perw = np.where(cnt > 0, wrow.sum(axis=1) / np.maximum(cnt, 1), 0.0)
    E = poolmat[dec]
    take = np.minimum(E.sum(axis=1), cnt)
    rng = np.random.default_rng(seed)
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
# (2) CORPUS SCAN
# ==========================================================================================
def scan_corpus():
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    if SMOKE:
        files = files[::23]
    per_file = []
    agg = dict(rows=0, unparsed=0, fail=0, pass_=0,
               g1_seen=0, g1_bad=0, g2_seen=0, g2_bad=0, g7_bad=0)
    # accumulators: STRICT over ALLROWS / REALROWS
    acc = {a: dict(n=0, infail=np.zeros(5, np.int64), sole=np.zeros(5, np.int64),
                   nest_den=0, nest_num=0, famsole=np.zeros(3, np.int64), passes=0)
           for a in ("ALLROWS", "REALROWS", "RECOMP_ALL", "RECOMP_REAL")}
    filewt = []
    t0 = time.time()
    nf = 0
    for p in files:
        try:
            hdr = header_of(p)
        except Exception:
            continue
        if "fail4b" not in hdr:
            continue
        hs = set(hdr)
        legset = next((L for L in LEGBOOLSETS if set(L) <= hs), None)
        want = ["fail4b"] + [c for c in ("pass4b", "draw", "kind") if c in hs]
        if legset:
            want += legset
        has_num = all(c in hs for c in NUMSET)
        if has_num:
            want += NUMSET
        try:
            df = pd.read_csv(p, usecols=want, low_memory=False)
        except Exception:
            continue
        nf += 1
        sfx = p.name.replace(".csv.gz", "").replace(".csv", "").split(".")[-1]
        file_is_null = sfx in ("nulls", "draws", "nulls_wide")

        raw = df["fail4b"].astype("string").fillna("")
        uniq = raw.unique().tolist()
        pm = {u: parse_fail(u) for u in uniq}
        ok = raw.map({u: pm[u][1] for u in uniq}).fillna(False).to_numpy(bool)
        masks = raw.map({u: pm[u][0] for u in uniq}).fillna(0).to_numpy(np.int64)
        agg["rows"] += len(df)
        agg["unparsed"] += int((~ok).sum())

        isnull = np.full(len(df), file_is_null, bool)
        if "draw" in df.columns:
            d = pd.to_numeric(df["draw"], errors="coerce").to_numpy()
            isnull |= np.nan_to_num(d, nan=-1.0) >= 0
        if "kind" in df.columns:
            isnull |= df["kind"].astype(str).str.contains(NULL_KIND, na=False).to_numpy(bool)

        g1b = g2b = 0
        if "pass4b" in df.columns:
            pv = df["pass4b"].map(truthy).to_numpy(bool)
            agg["g1_seen"] += int(ok.sum())
            g1b = int((pv[ok] != (masks[ok] == 0)).sum())
            agg["g1_bad"] += g1b
        if legset:
            B = np.column_stack([df[c].map(truthy).to_numpy(bool) for c in legset])
            bm = np.zeros(len(df), np.int64)
            for i, k in enumerate(LEGS):
                bm |= (~B[:, i]).astype(np.int64) * BIT[k]
            agg["g2_seen"] += int(ok.sum())
            g2b = int((bm[ok] != masks[ok]).sum())
            agg["g2_bad"] += g2b

        fmask = ok & (masks > 0)
        pmask = ok & (masks == 0)
        agg["fail"] += int(fmask.sum())
        agg["pass_"] += int(pmask.sum())

        # --- G7: the deletion identity, asserted on the committed masks
        delH2 = masks & ~BIT["H2"]
        flips = ok & (masks > 0) & (delH2 == 0)
        agg["g7_bad"] += int(((flips) != (ok & (masks == BIT["H2"]))).sum())
        agg["g7_bad"] += int((ok & (masks == 0) & (delH2 > 0)).sum())   # no PASS may break

        def feed(name, sel, mk):
            a = acc[name]
            f = sel & (mk > 0)
            a["n"] += int(f.sum())
            a["passes"] += int((sel & (mk == 0)).sum())
            for i, k in enumerate(LEGS):
                a["infail"][i] += int((f & (mk & BIT[k] > 0)).sum())
                a["sole"][i] += int((f & (mk == BIT[k])).sum())
            h2 = f & (mk & BIT["H2"] > 0)
            a["nest_den"] += int(h2.sum())
            a["nest_num"] += int((h2 & (mk & BIT["H1"] > 0)).sum())
            for j, fam in enumerate(("SHARPE", "DD", "CAGR")):
                a["famsole"][j] += int((f & (mk & ~FAMBIT[fam] == 0)).sum())

        feed("ALLROWS", ok, masks)
        feed("REALROWS", ok & ~isnull, masks)

        rec_masks = None
        fid = np.nan
        if has_num:
            sub = df[NUMSET].apply(pd.to_numeric, errors="coerce")
            good = sub.notna().all(axis=1).to_numpy(bool)
            if good.any():
                lr = legs_rec_v(sub)
                rec_masks = np.zeros(len(df), np.int64)
                for k in LEGS:
                    rec_masks |= (~lr[k].to_numpy(bool)).astype(np.int64) * BIT[k]
                cmp_ = ok & good
                if cmp_.sum():
                    fid = float((rec_masks[cmp_] == masks[cmp_]).mean())
                feed("RECOMP_ALL", good, rec_masks)
                feed("RECOMP_REAL", good & ~isnull, rec_masks)

        n_f = int(fmask.sum())
        if n_f:
            row = dict(file=p.name, rows=len(df), n_fail=n_f,
                       unparsed=int((~ok).sum()), null_rows=int((isnull & ok).sum()),
                       recomp_fidelity=fid, g1_disagree=g1b, g2_disagree=g2b)
            for i, k in enumerate(LEGS):
                row["infail_" + LEGNAME[k]] = float((fmask & (masks & BIT[k] > 0)).sum()) / n_f
                row["sole_" + LEGNAME[k]] = float((fmask & (masks == BIT[k])).sum()) / n_f
            filewt.append(row)
        per_file.append(dict(file=p.name, rows=len(df), n_fail=n_f))
    P(f"  scanned {nf} committed CSVs carrying `fail4b`  ({time.time()-t0:.0f}s)")
    return acc, agg, pd.DataFrame(filewt), nf


# ==========================================================================================
# (3) FRESH LADDER
# ==========================================================================================
def fresh_ladder():
    panels = {}
    panels["U56"] = load_universe()
    if "B136" in PANELS_WANTED:
        panels["B136"] = load_universe(broad=True)
    real, nullrows, cellrows = [], [], []
    spyprof, meta = {}, {}
    for pn, px in panels.items():
        idx = px.index
        oi = int(np.searchsorted(idx[WARM:], pd.Timestamp(OOS_START)))
        spy = px["SPY"].pct_change().fillna(0.0).values[WARM:]
        spyprof[pn] = profile(spy, oi)
        meta[pn] = oi
    v2 = {}
    for pn, px in panels.items():
        ctx = Ctx(px, offset_mask(px.index, "W"))
        g, t = ctx.run(ctx.shift(rules_v2_weights(px, BAND0, GROSS)))
        for c in RUNGS:
            v2[(pn, c)] = profile((g - t * c / 1e4)[WARM:], meta[pn])
    for pn, px in panels.items():
        idx, oi, spy, pl = px.index, meta[pn], spyprof[pn], pools(px)
        for bk, fn in BOOKS.items():
            Wb = fn(px, GROSS)
            pool = pl[POOLKIND[bk]]
            for cad in CADS:
                ctx = Ctx(px, offset_mask(idx, cad))
                wt = ctx.shift(Wb)
                pid = period_id(idx, cad)
                gb, tb = ctx.run(wt)
                for c in RUNGS:
                    d = profile((gb - tb * c / 1e4)[WARM:], oi)
                    lg, li = legs_of(d, spy), legs_is(d, spy)
                    real.append(dict(panel=pn, book=bk, cadence=cad, rung=c,
                                     mask=mask_of(lg), fail4b=maskname(mask_of(lg)),
                                     pass4b=all(lg.values()), IS_legs=sum(li.values()),
                                     **{k: v for k, v in d.items()}))
                gs = np.empty((DRAWS, ctx.T))
                ts = np.empty((DRAWS, ctx.T))
                for s in range(DRAWS):
                    seed = (SEED0 * 1_000_000 + PANSEED[pn] * 100_000
                            + BOOKSEED[bk] * 10_000 + CADSEED[cad] * 1_000 + s)
                    Wn, _, _ = null_weights(ctx, pool, wt, seed, pid)
                    gs[s], ts[s] = ctx.run(Wn)
                for c in RUNGS:
                    mk = np.zeros(DRAWS, np.int64)
                    for s in range(DRAWS):
                        d = profile((gs[s] - ts[s] * c / 1e4)[WARM:], oi)
                        mk[s] = mask_of(legs_of(d, spy))
                    for s in range(DRAWS):
                        nullrows.append(dict(panel=pn, book=bk, cadence=cad, rung=c,
                                             draw=s, mask=int(mk[s]),
                                             fail4b=maskname(int(mk[s]))))
                    cellrows.append(dict(panel=pn, book=bk, cadence=cad, rung=c, draws=DRAWS,
                                         **{("p_" + LEGNAME[k]):
                                            float((mk & BIT[k] == 0).mean()) for k in LEGS},
                                         base4b=float((mk == 0).mean())))
    return panels, spyprof, meta, v2, pd.DataFrame(real), pd.DataFrame(nullrows), \
        pd.DataFrame(cellrows)


def stat_block(n, infail, sole, nest_den, nest_num, famsole, passes):
    if n == 0:
        return None
    d = dict(n=int(n), passes=int(passes))
    for i, k in enumerate(LEGS):
        d["infail_" + LEGNAME[k]] = float(infail[i]) / n
        d["sole_" + LEGNAME[k]] = float(sole[i]) / n
        d["soleN_" + LEGNAME[k]] = int(sole[i])
    d["nest_H1_given_H2"] = (float(nest_num) / nest_den) if nest_den else np.nan
    for j, fam in enumerate(("SHARPE", "DD", "CAGR")):
        d["famsole_" + fam] = float(famsole[j]) / n
    d["flip_pct_of_PASS"] = (float(sole[1]) / passes) if passes else np.nan
    return d


# ==========================================================================================
def main():
    t00 = time.time()
    P("=" * 100)
    P("IDEA 1014 (cloud, 2026-09-16, idea 2 of 2)  is-the-4b-H2-LEG-DEAD-WEIGHT")
    P("=" * 100)
    P(__doc__.split("PRE-REGISTERED HYPOTHESES")[1].split("PRE-REGISTERED GATES")[0].strip())
    P()

    P("=" * 100)
    P("(A) THE CORPUS")
    P("=" * 100)
    acc, agg, fw, nfiles = scan_corpus()
    P(f"  rows in those files                     : {agg['rows']:,}")
    P(f"  unparsed `fail4b` values (EXCLUDED)     : {agg['unparsed']:,}")
    P(f"  parsed committed 4b FAIL rows           : {agg['fail']:,}")
    P(f"  parsed committed 4b PASS rows           : {agg['pass_']:,}")
    P()

    P("=" * 100)
    P("(B) PRE-REGISTERED GATES")
    P("=" * 100)
    grows = []
    grows.append(("G0", "every non-empty `fail4b` parses into the 5-leg alphabet",
                  f"{agg['unparsed']:,} unparsed of {agg['rows']:,}, all EXCLUDED",
                  "counted, never guessed", True))
    grows.append(("G1", "pass4b == (binding set is empty)",
                  f"{agg['g1_bad']:,} of {agg['g1_seen']:,}", "0", agg["g1_bad"] == 0))
    grows.append(("G2", "committed leg booleans == the token set",
                  f"{agg['g2_bad']:,} of {agg['g2_seen']:,}", "0", agg["g2_bad"] == 0))

    # G3 -- cross-run against 1010's committed census
    c1010 = BT / ("2026-09-16_does-the-SOLE-KILLER-MONOPOLY-of-the-TWO-LEVEL-LEGS-"
                  "hold-on-the-RECORD-s-COMMITTED-FAIL-ROWS_C.census.csv")
    g3 = np.nan
    g3n = 0
    census_rows = []
    for cs, key in (("ALLROWS", "ALLROWS"), ("REALROWS", "REALROWS")):
        b = stat_block(acc[key]["n"], acc[key]["infail"], acc[key]["sole"],
                       acc[key]["nest_den"], acc[key]["nest_num"],
                       acc[key]["famsole"], acc[key]["passes"])
        if b:
            census_rows.append(dict(claimset=cs, defn="STRICT", **b))
    for cs, key in (("ALLROWS", "RECOMP_ALL"), ("REALROWS", "RECOMP_REAL")):
        b = stat_block(acc[key]["n"], acc[key]["infail"], acc[key]["sole"],
                       acc[key]["nest_den"], acc[key]["nest_num"],
                       acc[key]["famsole"], acc[key]["passes"])
        if b:
            census_rows.append(dict(claimset=cs, defn="RECOMP", **b))
    cen = pd.DataFrame(census_rows)
    if c1010.exists() and not SMOKE:
        ref = pd.read_csv(c1010)
        dmax, n = 0.0, 0
        for _, r in ref.iterrows():
            m = cen[(cen.claimset == r["claimset"]) & (cen.defn == r["defn"])]
            if m.empty:
                continue
            for k in LEGS:
                col = "sole_" + LEGNAME[k]
                if col in ref.columns and pd.notna(r[col]):
                    dmax = max(dmax, abs(float(r[col]) - float(m.iloc[0][col])))
                    n += 1
        g3, g3n = dmax, n
    grows.append(("G3", "CROSS-RUN: idea 1010's committed census sole-binder shares",
                  f"max|d| {g3:.3e} over {g3n} shared cells" if np.isfinite(g3)
                  else "reference not available", "1e-12",
                  bool(np.isfinite(g3) and g3 < 1e-12)))
    # G3b -- the DIAGNOSIS of any G3 miss: re-run the row-weighted census restricted to the
    # EXACT file list idea 1010 saw.  The corpus is append-only and now contains 1010's own
    # artifacts, so a growing denominator is the first thing to rule out.
    g3b = np.nan
    g3bn = 0
    f1010 = BT / ("2026-09-16_does-the-SOLE-KILLER-MONOPOLY-of-the-TWO-LEVEL-LEGS-"
                  "hold-on-the-RECORD-s-COMMITTED-FAIL-ROWS_C.corpusfiles.csv")
    if f1010.exists() and c1010.exists() and len(fw) and not SMOKE:
        seen = set(pd.read_csv(f1010)["file"].astype(str))
        sub = fw[fw["file"].isin(seen)]
        n = float(sub["n_fail"].sum())
        ref = pd.read_csv(c1010)
        r = ref[(ref.claimset == "ALLROWS") & (ref.defn == "STRICT")]
        if n > 0 and len(r):
            d = 0.0
            for k in LEGS:
                col = "sole_" + LEGNAME[k]
                mine = float((sub[col] * sub["n_fail"]).sum()) / n
                d = max(d, abs(mine - float(r.iloc[0][col])))
                g3bn += 1
            g3b = d
        g3b_ctx = (f"; this run sees {len(fw)} FAIL-bearing files / "
                   f"{int(fw['n_fail'].sum()):,} FAIL rows, 1010 saw {len(seen)} files of "
                   f"which {len(sub)} / {int(sub['n_fail'].sum()):,} rows are still present")
    else:
        g3b_ctx = ""
    grows.append(("G3b", "DIAGNOSIS: the same census restricted to idea 1010's OWN file list",
                  (f"max|d| {g3b:.3e} over {g3bn} legs" + g3b_ctx) if np.isfinite(g3b)
                  else "reference not available", "1e-12",
                  bool(np.isfinite(g3b) and g3b < 1e-12)))
    grows.append(("G7", "DELETION IDENTITY on the committed masks (both directions)",
                  f"{agg['g7_bad']:,} disagreeing rows", "0", agg["g7_bad"] == 0))

    panels, spyprof, meta, v2, real, nulls, cells = fresh_ladder()

    px = panels["U56"]
    W = ranked_book(px, GROSS, 20)
    dr = dt = 0.0
    for per in ("W", "M"):
        eng = engine.backtest(px, W, cost_bps=0.0, freq=per)
        ctx = Ctx(px, offset_mask(px.index, per))
        g, t = ctx.run(ctx.shift(W))
        dr = max(dr, float(np.abs(g[WARM:] - eng["returns"].values[WARM:]).max()))
        dt = max(dt, float(np.abs(t[WARM:] - eng["turnover"].values[WARM:]).max()))
    grows.append(("G4", "fast Ctx == engine.backtest (returns / turnover)",
                  f"dret {dr:.3e} dturn {dt:.3e}", "1e-12 / 1e-10",
                  dr < 1e-12 and dt < 1e-10))
    s = spyprof["U56"]
    ok5 = all(abs(s["OOS_" + k] - REC_SPY_OOS[k]) < 0.005 for k in ("CAGR", "Sharpe", "MaxDD"))
    grows.append(("G5", "CROSS-RUN: SPY OOS == the record's committed triple",
                  f"{s['OOS_CAGR']:.2%}/{s['OOS_Sharpe']:.4f}/{s['OOS_MaxDD']:.2%}",
                  "0.005 each", ok5))
    ctx = Ctx(px, offset_mask(px.index, "M"))
    a1, _ = ctx.run(ctx.shift(W))
    a2, _ = Ctx(px, offset_mask(px.index, "M")).run(ctx.shift(W))
    d6 = float(np.abs(a1 - a2).max())
    grows.append(("G6", "determinism: a rebuilt fresh cell reproduces its own stream",
                  f"max|d| {d6:.3e}", "0.0", d6 == 0.0))

    for g, what, got, bar, okk in grows:
        P(f"  {g}  {'PASS' if okk else 'FAIL'}  {what}")
        P(f"        got {got}   bar {bar}")
    P(f"  GATES: {sum(r[4] for r in grows)} of {len(grows)} PASS")
    P()

    # ---- FILEWT and FRESH arms ----------------------------------------------------------
    if len(fw):
        w = dict(claimset="FILEWT", defn="STRICT", n=len(fw), passes=np.nan)
        for k in LEGS:
            w["infail_" + LEGNAME[k]] = float(fw["infail_" + LEGNAME[k]].mean())
            w["sole_" + LEGNAME[k]] = float(fw["sole_" + LEGNAME[k]].mean())
            w["soleN_" + LEGNAME[k]] = int((fw["sole_" + LEGNAME[k]] > 0).sum())
        w["nest_H1_given_H2"] = np.nan
        w["flip_pct_of_PASS"] = np.nan
        census_rows.append(w)

    fr = pd.concat([real[["mask"]], nulls[["mask"]]], ignore_index=True)["mask"].to_numpy()
    fpass = int((fr == 0).sum())
    ffail = fr[fr > 0]
    if len(ffail):
        infail = np.array([int((ffail & BIT[k] > 0).sum()) for k in LEGS])
        sole = np.array([int((ffail == BIT[k]).sum()) for k in LEGS])
        h2 = ffail[(ffail & BIT["H2"]) > 0]
        famsole = np.array([int((ffail & ~FAMBIT[f] == 0).sum())
                            for f in ("SHARPE", "DD", "CAGR")])
        b = stat_block(len(ffail), infail, sole, len(h2),
                       int((h2 & BIT["H1"] > 0).sum()), famsole, fpass)
        census_rows.append(dict(claimset="FRESH", defn="STRICT", **b))
        census_rows.append(dict(claimset="FRESH", defn="RECOMP", **b))   # identical by
        #   construction on FRESH: the legs ARE the recomputation (stated, not hidden)

    cen = pd.DataFrame(census_rows)
    # FAMILY definition -- deleting "the H2 leg" means deleting the whole Sharpe family
    fam_rows = []
    for _, r in cen.iterrows():
        fam_rows.append(dict(claimset=r["claimset"], defn="FAMILY", n=r["n"],
                             passes=r.get("passes", np.nan),
                             sole_L2_H2=r.get("famsole_SHARPE", np.nan),
                             infail_L2_H2=r.get("infail_L2_H2", np.nan)))
    fam = pd.DataFrame(fam_rows)
    dump(cen, "census")
    dump(fam, "family")
    dump(fw, "corpusfiles")
    dump(cells, "freshcells")
    dump(real, "freshreal")
    P()

    P("=" * 100)
    P("(C) THE CENSUS -- per leg, over committed 4b FAIL rows")
    P("=" * 100)
    show = ["claimset", "defn", "n"] + ["infail_" + LEGNAME[k] for k in LEGS]
    P("  IN-FAIL share (the leg is somewhere in the binding set):")
    P("  " + cen[show].to_string(index=False, float_format=lambda x: f"{x:.4f}")
      .replace("\n", "\n  "))
    P()
    show2 = ["claimset", "defn", "n"] + ["sole_" + LEGNAME[k] for k in LEGS]
    P("  SOLE share == the DELETION-FLIP rate (deleting the leg flips exactly these rows):")
    P("  " + cen[show2].to_string(index=False, float_format=lambda x: f"{x:.5f}")
      .replace("\n", "\n  "))
    P()
    P("  FAMILY definition (deleting the whole SHARPE family):")
    P("  " + fam.to_string(index=False, float_format=lambda x: f"{x:.5f}")
      .replace("\n", "\n  "))
    P()

    # ---- hypotheses ---------------------------------------------------------------------
    A = cen[(cen.claimset == "ALLROWS") & (cen.defn == "STRICT")].iloc[0]
    H = []
    H.append(("H_DEAD", float(A["infail_L2_H2"]) < BAR_DEAD,
              f"`L2_H2` in the binding set of {A['infail_L2_H2']:.4f} of {int(A['n']):,} "
              f"committed FAIL rows", f"< {BAR_DEAD}"))
    H.append(("H_NOFLIP", float(A["sole_L2_H2"]) < BAR_NOFLIP,
              f"deleting `L2_H2` flips {int(A['soleN_L2_H2']):,} of {int(A['n']):,} rows "
              f"= {A['sole_L2_H2']:.5f}; as a fraction of the {int(A['passes']):,} committed "
              f"PASS rows that is {A['flip_pct_of_PASS']:+.4f}", f"< {BAR_NOFLIP}"))
    least = []
    for _, r in cen.iterrows():
        vals = {k: r.get("sole_" + LEGNAME[k], np.nan) for k in LEGS}
        if all(np.isfinite(list(vals.values()))):
            least.append((f"{r['claimset']}/{r['defn']}", min(vals, key=vals.get)))
    nH2 = sum(1 for _, k in least if k == "H2")
    H.append(("H_LEAST", nH2 == len(least) and len(least) > 0,
              f"least-pivotal leg per cell: "
              + "  ".join(f"{c}={LEGNAME[k]}" for c, k in least)
              + f"   ({nH2} of {len(least)} are L2_H2)", "L2_H2 in every cell"))
    H.append(("H_NEST", float(A["nest_H1_given_H2"]) >= BAR_NEST,
              f"P(`L1_H1` fails | `L2_H2` fails) = {A['nest_H1_given_H2']:.4f}",
              f">= {BAR_NEST}"))
    p2 = float(cells["p_L2_H2"].mean())
    p2min = float(cells["p_L2_H2"].min())
    H.append(("H_1001", p2 >= BAR_1001,
              f"`p_L2_H2` on the fresh ladder: mean {p2:.4f}, min {p2min:.4f} over "
              f"{len(cells)} cells x {DRAWS} draws"
              + ("  [and per-leg means " + ", ".join(
                  f"{LEGNAME[k]} {cells['p_'+LEGNAME[k]].mean():.3f}" for k in LEGS) + "]"),
              f">= {BAR_1001}"))
    P("  `p_L2_H2` broken out (reported, not a bar) -- 1001 read REAL books, so the")
    P("  comparable population is the real-book row, not the pooled ladder:")
    P("    null draws, by rung : "
      + "  ".join(f"{int(c)} bps {cells[cells.rung == c]['p_L2_H2'].mean():.4f}"
                  for c in RUNGS))
    for c in RUNGS:
        sub = real[real.rung == c]
        P(f"    REAL books @{int(c):2d} bps: L2_H2 clears "
          f"{float((sub['mask'] & BIT['H2'] == 0).mean()):.4f} of {len(sub)} books"
          + "   (other legs " + ", ".join(
              f"{LEGNAME[k]} {float((sub['mask'] & BIT[k] == 0).mean()):.3f}"
              for k in LEGS if k != "H2") + ")")
    worst = cen["sole_L2_H2"].max()
    famworst = fam["sole_L2_H2"].max()
    H.append(("H_STABLE", float(worst) < BAR_NOFLIP,
              f"worst `L2_H2` deletion-flip rate over the {len(cen)} STRICT/RECOMP cells "
              f"{worst:.5f}; under FAMILY (whole Sharpe family deleted) {famworst:.5f}",
              f"< {BAR_NOFLIP}"))

    # ---- rule 8 -------------------------------------------------------------------------
    P("=" * 100)
    P("(D) PROTOCOL RULE 8 -- picks chosen on 2009-2016 ALONE, OOS read ONCE,")
    P("    scored under 4b AND under 4b-minus-H2")
    P("=" * 100)
    wf = []
    for pn in panels:
        for c in RUNGS:
            sub = real[(real.panel == pn) & (real.rung == c)]
            picks = {"C_ISSHARPE": sub.sort_values("IS_Sharpe", ascending=False).iloc[0],
                     "C_ISCAGR": sub.sort_values("IS_CAGR", ascending=False).iloc[0],
                     "C_ISLEGS": sub.sort_values(["IS_legs", "IS_Sharpe"],
                                                 ascending=[False, False]).iloc[0]}
            for ch, row in picks.items():
                b, sp = v2[(pn, c)], spyprof[pn]
                m = int(row["mask"])
                wf.append(dict(panel=pn, rung=c, chooser=ch,
                               pick=f"{row['book']}/{row['cadence']}",
                               OOS_CAGR=row["OOS_CAGR"], OOS_Sharpe=row["OOS_Sharpe"],
                               OOS_MaxDD=row["OOS_MaxDD"], fail4b=maskname(m),
                               pass4b=m == 0, pass4b_noH2=(m & ~BIT["H2"]) == 0,
                               pass4a=bool(row["H1"] > b["H1"] and row["H2"] > b["H2"]
                                           and row["MaxDD"] >= b["MaxDD"]),
                               spy_OOS_CAGR=sp["OOS_CAGR"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                               spy_OOS_MaxDD=sp["OOS_MaxDD"],
                               v2_OOS_CAGR=b["OOS_CAGR"], v2_OOS_Sharpe=b["OOS_Sharpe"],
                               v2_OOS_MaxDD=b["OOS_MaxDD"]))
    wfd = pd.DataFrame(wf)
    dump(wfd, "walkforward")
    P(wfd[["panel", "rung", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
           "pass4b", "pass4b_noH2", "pass4a", "fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    same = int((wfd.pass4b == wfd.pass4b_noH2).sum())
    P()
    P(f"  OOS 4b {int(wfd.pass4b.sum())} of {len(wfd)}   "
      f"OOS 4b-minus-H2 {int(wfd.pass4b_noH2.sum())} of {len(wfd)}   "
      f"OOS 4a {int(wfd.pass4a.sum())} of {len(wfd)}")
    for pn in panels:
        sp, b = spyprof[pn], v2[(pn, HEAD)]
        P(f"  comparands {pn}: SPY OOS {sp['OOS_CAGR']:.2%}/{sp['OOS_Sharpe']:.4f}"
          f"/{sp['OOS_MaxDD']:.2%};  RULES v2 @10bps OOS {b['OOS_CAGR']:.2%}"
          f"/{b['OOS_Sharpe']:.4f}/{b['OOS_MaxDD']:.2%}")
    H.append(("H_RULE8", same == len(wfd),
              f"{same} of {len(wfd)} picks score identically under 4b and 4b-minus-H2",
              "all"))
    P()

    # ---- the two-sided reading ----------------------------------------------------------
    P("=" * 100)
    P("(E) WHAT THE CLAUSE REMOVES, READ BOTH WAYS")
    P("=" * 100)
    for _, r in cen.iterrows():
        if not np.isfinite(r.get("flip_pct_of_PASS", np.nan)):
            continue
        P(f"  {r['claimset']:9s}/{r['defn']:7s}  flips {int(r['soleN_L2_H2']):>7,} rows"
          f"  = {r['sole_L2_H2']:.5f} of {int(r['n']):,} FAIL rows"
          f"  = {r['flip_pct_of_PASS']:+.4f} of {int(r['passes']):,} PASS rows")
    P()

    P("=" * 100)
    P("(F) HYPOTHESIS SCORECARD")
    P("=" * 100)
    for name, okk, got, bar in H:
        P(f"  {name:10s} {'PASS' if okk else 'FAIL'}   {got}")
        P(f"             bar {bar}")
    P(f"  {sum(h[1] for h in H)} of {len(H)} PASS")
    pd.DataFrame([dict(hypothesis=n, verdict="PASS" if o else "FAIL", got=g, bar=b)
                  for n, o, g, b in H]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    pd.DataFrame([dict(gate=g, what=w, got=gt, bar=b, verdict="PASS" if o else "FAIL")
                  for g, w, gt, b, o in grows]).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    P()
    P(f"  total runtime {time.time() - t00:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
