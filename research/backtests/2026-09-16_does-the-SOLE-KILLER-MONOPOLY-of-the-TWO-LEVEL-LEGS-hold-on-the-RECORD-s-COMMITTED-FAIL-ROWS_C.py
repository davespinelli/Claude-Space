#!/usr/bin/env python3
"""
Idea 1010 (lane C, 2026-09-16)
does-the-SOLE-KILLER-MONOPOLY-of-the-TWO-LEVEL-LEGS-hold-on-the-RECORD-s-COMMITTED-FAIL-ROWS
============================================================================================

THE QUESTION (QUEUE.md, verbatim)
---------------------------------
  idea 1007 found `L1_H1`, `L2_H2` and `L3_OOS` are the SOLE binding leg in 0 of 30 null cells
  while `L5_CAGR` (7) and `L4_DD` (5) take all of them, on one 30-cell grid.  Census the
  record's committed 4b FAIL rows for sole-binder identity under one pinned census definition
  and report whether the Sharpe legs ever decide a verdict alone.  Max 2 params (claim set,
  sole-binder definition).

WHAT IS MEASURED
----------------
4b is a CONJUNCTION of five legs, read in the record's convention:
  L1_H1   Sharpe(H1)   > SPY's        L2_H2   Sharpe(H2)   > SPY's
  L3_OOS  Sharpe(OOS)  > SPY's        L4_DD   |OOS MaxDD|  <= 0.60 x |SPY MaxDD|
  L5_CAGR OOS CAGR     >= 0.70 x SPY's CAGR
A row FAILS 4b when at least one leg fails.  Its BINDING SET is the set of failing legs.  The
row has a SOLE BINDER when that set has exactly one member: one leg, alone, decided the
verdict, and the other four are decorative on that row.  1007's monopoly claim is about SOLE
binders only -- it says the two LEVEL legs (`L4_DD`, `L5_CAGR`) take every sole-binder cell and
the three SHARPE legs take none.  This run asks the same question of the RECORD, not of one
30-cell null grid.

THE CORPUS
----------
Every committed `research/backtests/*.csv[.gz]` carrying a column literally named `fail4b`
(446 files, ~247 MB).  That column is the record's own comma- or pipe-separated list of the
legs that failed, in two spellings the record actually uses:
  LONG  `L1_H1,L2_H2,L3_OOS,L4_DD,L5_CAGR`   SHORT `H1,H2,OOS,DD,CAGR`
  plus the record's own aliases `L5_CAGRfloor` / `CAGRFLOOR` -> L5_CAGR and `DDCAP` -> L4_DD,
  read case-insensitively, separators `,` `|` `;` `+` `/`.
A row is a committed 4b FAIL row when its `fail4b` is non-empty, is not one of the record's
PASS sentinels (`-`, `-none-`, empty), and parses COMPLETELY into that alphabet.  Nothing else
is read as a FAIL.  Values that do NOT parse -- a handful of files write an aggregate COUNTER
dict (`{'DD': 44, 'CAGR': 4}`) or prose (`no IS-admissible point`) into the same column -- are
EXCLUDED from every claim set and counted in G0 rather than guessed at.

TUNED 1 -- CLAIM SET (4 levels, ALL reported, none selected)
  ALLROWS   every committed FAIL row counts once (row-weighted).
  REALROWS  FAIL rows that are NOT null draws.  A row is a NULL draw when its file carries a
            `draw` column with a value >= 0, or a `kind` column matching draw|null, or the
            file's suffix stem is `nulls`/`draws`.  This is the split that matters for
            capital: a coin flip's binding leg is not a rule's binding leg.
  FILEWT    every committed CSV counts once (its own FAIL rows' shares, averaged equally over
            files).  A row-weighted headline can be carried by three 200k-row grid dumps; a
            file-weighted one cannot.
  FRESH     this run's OWN priced grid -- 2 panels x 5 books x 2 cadences x 3 cost rungs = 60
            book cells, legs computed here from prices, not read from anyone's text.

TUNED 2 -- SOLE-BINDER DEFINITION (3 levels, ALL reported, none selected)
  STRICT    exactly ONE token in the committed `fail4b`.  Identity = that leg.
  FAMILY    the tokens collapse to families SHARPE={L1_H1,L2_H2,L3_OOS}, DD={L4_DD},
            CAGR={L5_CAGR}; sole binder = exactly ONE family present.  `H1,H2,OOS` is then a
            sole SHARPE binder -- this is the WEAKEST reading of 1007's claim and the one
            most likely to break it.
  RECOMP    the committed string is IGNORED and all five legs are recomputed from the row's
            own numeric columns against the SPY comparands committed in the SAME file; sole
            binder = exactly one recomputed leg fails.  Available only on rows carrying the
            full numeric set, and only from files that pass the fidelity gate G7.

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
--------------------------------------------------------------------------------------------
  H_MONO    1007's monopoly, read STRICTly on ALLROWS: the three SHARPE legs are the sole
            binder on < 1.0% of committed FAIL rows.  At or above 1.0% the monopoly is a
            property of 1007's 30-cell grid, not of the record.
  H_MONO_R  the same bar on REALROWS -- the claim that matters for a real book.
  H_FAMILY  under FAMILY x ALLROWS, SHARPE-alone < 5.0%.
  H_TAKE    1007's positive half: `L4_DD` + `L5_CAGR` take >= 90% of all sole-binder rows
            under STRICT x ALLROWS.
  H_STABLE  the leg holding the LARGEST sole-binder share is the same leg under all four
            claim sets (STRICT).  An unstable ranking means the record's answer is a
            weighting artefact.
  H_FRESH   this run's own priced 60-cell grid reproduces the record's sole-binder ORDERING
            (same leg on top, SHARPE share on the same side of 1.0%).
  H_RULE8   PROTOCOL rule 8: a (book, cadence) chosen on 2009-2016 ALONE by an IS-only
            chooser delivers an OOS 4b pass on at least one (panel, cost rung).

PRE-REGISTERED GATES (printed before any result number is read)
---------------------------------------------------------------
  G0  ALPHABET CLOSURE: every non-empty `fail4b` value in the corpus parses into the
      five-leg alphabet                                              unparsed rows reported
  G1  PASS/FAIL CONSISTENCY: where a file carries `pass4b` beside `fail4b`,
      pass4b == (fail4b is the PASS sentinel) on every row                     0 disagreeing
  G2  TOKEN/BOOLEAN CONSISTENCY: where a file carries the five leg booleans beside
      `fail4b`, the token set equals the set of False legs, row by row         0 disagreeing
  G3  FAST RUNNER == engine.backtest on returns AND turnover post warm-up      1e-12 / 1e-10
  G4  BAND03(0.03, 0.75) == baseline.rules_v2_weights                                   0.0
  G5  DETERMINISM: a rebuilt FRESH cell reproduces its own streams exactly               0.0
  G6  CENSUS CLOSURE: sole-binder + multi-binder rows partition the FAIL population
      exactly, under every claim set x definition cell                            0 leftover
  G7  RECOMP FIDELITY: on files where both readings exist, the recomputed binding SET
      equals the committed one on >= 99% of rows; a file below the bar is DROPPED from
      the RECOMP claim set and counted                                       >= 0.99 per file

SURVIVORSHIP (PROTOCOL rule 9)
------------------------------
The FRESH arm prices U56 (research/universe.json) and B136 (research/universe_broad.json),
both CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL in the price arm is
optimistic.  That cuts in a KNOWN direction here: survivorship lifts realised CAGR and
compresses drawdowns, so it makes `L5_CAGR` and `L4_DD` EASIER to clear and therefore makes a
LEVEL-leg sole binder HARDER to observe.  Any SHARPE-leg sole-binder share measured on the
FRESH arm is thus an UPPER bound, and any LEVEL-leg monopoly found here is a LOWER bound on
how monopolistic the level legs would be on a real-time panel.  The record arm inherits
whatever bias its own 446 source files carried; it is a census of text, and is reported as
such.

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
IS_END, OOS_START = "2016-12-31", "2017-01-01"
VOLCAP, BAND0, GROSS = 0.60, 0.03, 0.75
RUNGS = [0.0, 10.0, 25.0]
HEAD_COST = 10.0
CADS = [("W", "W"), ("M", "M")]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
FAMILY = {"H1": "SHARPE", "H2": "SHARPE", "OOS": "SHARPE", "DD": "DD", "CAGR": "CAGR"}
PASS_SENTINEL = {"-", "", "none", "NONE", "None", "nan", "-none-", "NaN", "n/a"}

# pre-registered bars
MONO_BAR = 0.010          # H_MONO / H_MONO_R : SHARPE sole-binder share
FAMILY_BAR = 0.050        # H_FAMILY
TAKE_BAR = 0.90           # H_TAKE
FID_BAR = 0.99            # G7 per-file fidelity

SMOKE = bool(int(os.environ.get("IDEA1010_SMOKE", "0")))
LINES: list[str] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix, gz=False):
    p = OUT / (f"{STEM}.{suffix}.csv.gz" if gz else f"{STEM}.{suffix}.csv")
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ==========================================================================================
# (0) the token alphabet
# ==========================================================================================
TOKMAP = {}
for k, v in LEGNAME.items():
    TOKMAP[k] = k
    TOKMAP[v] = k
    TOKMAP[k.lower()] = k
    TOKMAP[v.lower()] = k
for extra, leg in (("L5_CAGRfloor", "CAGR"), ("CAGRfloor", "CAGR"), ("CAGRFLOOR", "CAGR"),
                   ("DDcap", "DD"), ("DDCAP", "DD"), ("L4_DDcap", "DD")):
    TOKMAP[extra] = leg
    TOKMAP[extra.lower()] = leg
    TOKMAP[extra.upper()] = leg
TOKMAP = {k.upper(): v for k, v in TOKMAP.items()}      # the record spells these 4 ways
SPLIT = re.compile(r"[,|;+/ ]+")


BIT = {k: 1 << i for i, k in enumerate(LEGS)}
FAMBIT = {"SHARPE": BIT["H1"] | BIT["H2"] | BIT["OOS"], "DD": BIT["DD"], "CAGR": BIT["CAGR"]}


def parse_fail(s):
    """-> (bitmask over LEGS, ok).  ok=False means the value did not parse (G0)."""
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


def maskname(m):
    return ",".join(LEGNAME[k] for k in LEGS if m & BIT[k]) or "-"


# ==========================================================================================
# (1) price machinery -- 942/962/964/975/1007's, verbatim, so this run NESTS
# ==========================================================================================
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
    "TOP10":  lambda p, g: ranked_book(p, g, 10),
    "TOP20":  lambda p, g: ranked_book(p, g, 20),
    "TOP40":  lambda p, g: ranked_book(p, g, 40),
}


def legs_rec(row):
    """The RECORD's 4b alphabet on a dict/Series of statistics."""
    return dict(H1=row["H1"] > row["spy_H1"],
                H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_rec_v(df):
    return dict(H1=df["H1"] > df["spy_H1"], H2=df["H2"] > df["spy_H2"],
                OOS=df["OOS_Sharpe"] > df["spy_OOS_Sharpe"],
                DD=df["OOS_MaxDD"].abs() <= 0.60 * df["spy_MaxDD"].abs(),
                CAGR=df["OOS_CAGR"] >= 0.70 * df["spy_CAGR"])


# ==========================================================================================
# (2) THE CORPUS SCAN
# ==========================================================================================
NUMSET = ["H1", "H2", "OOS_Sharpe", "OOS_MaxDD", "OOS_CAGR",
          "spy_H1", "spy_H2", "spy_OOS_Sharpe", "spy_MaxDD", "spy_CAGR"]
LEGBOOLSETS = [["leg_L1_H1", "leg_L2_H2", "leg_L3_OOS", "leg_L4_DD", "leg_L5_CAGR"],
               ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"],
               ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGRfloor"]]
NULL_KIND = re.compile(r"draw|null", re.I)


def header_of(p: Path):
    op = gzip.open(p, "rt") if p.name.endswith(".gz") else open(p, newline="")
    with op as fh:
        line = fh.readline()
    return [c.strip() for c in line.rstrip("\n").rstrip("\r").split(",")]


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "1.0", "yes", "t")


def scan_corpus():
    files = sorted(list(BT.glob("*.csv")) + list(BT.glob("*.csv.gz")))
    if SMOKE:
        files = files[::17]
    per_file, rows_agg = [], []
    g0_unparsed = g1_bad = g2_bad = 0
    g1_seen = g2_seen = 0
    t0 = time.time()
    for n, p in enumerate(files):
        try:
            hdr = header_of(p)
        except Exception:
            continue
        if "fail4b" not in hdr:
            continue
        hs = set(hdr)
        legset = next((L for L in LEGBOOLSETS if set(L) <= hs), None)
        want = ["fail4b"]
        for c in ("pass4b", "draw", "kind"):
            if c in hs:
                want.append(c)
        if legset:
            want += legset
        has_num = all(c in hs for c in NUMSET)
        if has_num:
            want += NUMSET
        try:
            df = pd.read_csv(p, usecols=want, low_memory=False)
        except Exception:
            continue
        stem_sfx = p.name.replace(".csv.gz", "").replace(".csv", "").split(".")[-1]
        file_is_null = stem_sfx in ("nulls", "draws", "nulls_wide")

        raw = df["fail4b"].astype("string").fillna("")
        uniq = raw.unique().tolist()
        pmap = {u: parse_fail(u) for u in uniq}
        okmap = {u: pmap[u][1] for u in uniq}
        mmap = {u: pmap[u][0] for u in uniq}
        ok = raw.map(okmap).fillna(False).to_numpy(bool)
        nbad = int((~ok).sum())
        g0_unparsed += nbad
        masks = raw.map(mmap).fillna(0).to_numpy(np.int64)
        nfail = ok & (masks > 0)

        # ---- G1 ----
        f_g1 = f_g2 = 0
        if "pass4b" in df.columns:
            pv = df["pass4b"].map(truthy).to_numpy(bool)
            g1_seen += int(ok.sum())
            f_g1 = int((pv[ok] != (masks[ok] == 0)).sum())
            g1_bad += f_g1
        # ---- G2 ----
        if legset:
            B = np.column_stack([df[c].map(truthy).to_numpy(bool) for c in legset])
            bm = np.zeros(len(df), np.int64)
            for i, k in enumerate(LEGS):
                bm |= (~B[:, i]).astype(np.int64) * BIT[k]
            g2_seen += int(ok.sum())
            f_g2 = int((bm[ok] != masks[ok]).sum())
            g2_bad += f_g2

        # ---- null / real ----
        isnull = np.full(len(df), file_is_null, bool)
        if "draw" in df.columns:
            d = pd.to_numeric(df["draw"], errors="coerce").to_numpy()
            isnull = isnull | (np.nan_to_num(d, nan=-1.0) >= 0)
        if "kind" in df.columns:
            isnull = isnull | df["kind"].astype(str).str.contains(NULL_KIND, na=False).to_numpy(bool)

        # ---- RECOMP ----
        rec_masks = None
        rec_pop = None
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
                if cmp_.sum() > 0:
                    fid = float((rec_masks[cmp_] == masks[cmp_]).mean())
                # the RECOMP population: rows the RECOMPUTATION itself calls FAIL, whatever
                # the committed string says (the point of the definition is not to trust it)
                sel = good & (rec_masks > 0)
                rec_pop = (rec_masks[sel].copy(), isnull[sel].copy())

        if nfail.any():
            rows_agg.append(dict(
                file=p.name, n_fail=int(nfail.sum()),
                masks=masks[nfail].copy(),
                isnull=isnull[nfail].copy(),
                rec=rec_pop,
                rec_ok=bool((not np.isnan(fid)) and fid >= FID_BAR),
                fid=fid))
        per_file.append(dict(file=p.name, rows=int(len(df)), n_fail=int(nfail.sum()),
                             unparsed=nbad, has_legbools=bool(legset), has_numerics=bool(has_num),
                             recomp_fidelity=fid,
                             recomp_admitted=bool((not np.isnan(fid)) and fid >= FID_BAR),
                             null_rows=int(isnull[nfail].sum()),
                             g1_disagree=f_g1, g2_disagree=f_g2))
        if n % 80 == 0:
            P(f"    ... scanned {n:4d}/{len(files)} files  ({time.time()-t0:5.1f}s)")
    return per_file, rows_agg, dict(g0=g0_unparsed, g1_bad=g1_bad, g1_seen=g1_seen,
                                    g2_bad=g2_bad, g2_seen=g2_seen)


# ==========================================================================================
# (3) CENSUS
# ==========================================================================================
def census(masks):
    """masks: 1-d int array of binding-set bitmasks (all > 0).  -> counts dict."""
    m = np.asarray(masks, dtype=np.int64)
    n = int(m.size)
    sole = {k: int((m == BIT[k]).sum()) for k in LEGS}
    n_sole = int(sum(sole.values()))
    fam_sole = {f: int(((m & fb) == m).sum()) for f, fb in FAMBIT.items()}
    n_fsole = int(sum(fam_sole.values()))
    return dict(n=n, n_sole=n_sole, n_multi=n - n_sole,
                n_fsole=n_fsole, n_fmulti=n - n_fsole,
                sole=sole, fam_sole=fam_sole)


def shares(c, mode):
    if c["n"] == 0:
        return {}
    if mode == "STRICT":
        d = {f"sole_{LEGNAME[k]}": c["sole"][k] / c["n"] for k in LEGS}
        d["sole_any"] = c["n_sole"] / c["n"]
        d["sole_SHARPE"] = sum(c["sole"][k] for k in ("H1", "H2", "OOS")) / c["n"]
        d["sole_LEVEL"] = sum(c["sole"][k] for k in ("DD", "CAGR")) / c["n"]
    else:
        d = {f"fsole_{k}": c["fam_sole"][k] / c["n"] for k in ("SHARPE", "DD", "CAGR")}
        d["sole_any"] = c["n_fsole"] / c["n"]
        d["sole_SHARPE"] = c["fam_sole"]["SHARPE"] / c["n"]
        d["sole_LEVEL"] = (c["fam_sole"]["DD"] + c["fam_sole"]["CAGR"]) / c["n"]
    return d


# ==========================================================================================
# (4) FRESH price arm
# ==========================================================================================
def build_fresh(panels):
    rows, streams = [], {}
    for pname, px in panels.items():
        idx = px.index
        start = idx[WARM]
        spy = px["SPY"].pct_change().fillna(0.0)
        for cad, freq in CADS:
            mask = engine.rebalance_mask(idx, freq)
            ctx = Ctx(px, mask)
            for bname, fn in BOOKS.items():
                W = fn(px, GROSS)
                wt = ctx.shift(W)
                r, turn = ctx.run(wt)
                rs = pd.Series(r, index=idx)
                ts = pd.Series(turn, index=idx)
                for rung in RUNGS:
                    net = (rs - ts * rung / 1e4).loc[start:]
                    s = spy.loc[start:]
                    m = mets(net.values)
                    ms = mets(s.values)
                    mi = mets(net.loc[:IS_END].values)
                    mo = mets(net.loc[OOS_START:].values)
                    msi = mets(s.loc[:IS_END].values)
                    mso = mets(s.loc[OOS_START:].values)
                    row = dict(panel=pname, book=bname, cadence=cad, cost_bps=rung,
                               turn_per_yr=float(ts.loc[start:].sum() / (len(net) / 252.0)),
                               CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                               H1=m["H1"], H2=m["H2"],
                               IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                               IS_H1=mi["H1"], IS_H2=mi["H2"],
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                               spy_H1=ms["H1"], spy_H2=ms["H2"],
                               spy_IS_Sharpe=msi["Sharpe"], spy_IS_CAGR=msi["CAGR"],
                               spy_IS_MaxDD=msi["MaxDD"], spy_IS_H1=msi["H1"],
                               spy_IS_H2=msi["H2"],
                               spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                               spy_OOS_MaxDD=mso["MaxDD"])
                    lr = legs_rec(row)
                    for k in LEGS:
                        row["leg_" + LEGNAME[k]] = bool(lr[k])
                    row["pass4b"] = all(lr[k] for k in LEGS)
                    row["fail4b"] = ",".join(LEGNAME[k] for k in LEGS if not lr[k]) or "-"
                    rows.append(row)
                    if rung == HEAD_COST:
                        streams[(pname, bname, cad)] = net
    return pd.DataFrame(rows), streams


def baseline_rows(panels):
    """RULES v2 (live) + SPY, per panel and rung, full and OOS."""
    out = {}
    for pname, px in panels.items():
        idx = px.index
        start = idx[WARM]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        mask = engine.rebalance_mask(idx, "W")
        ctx = Ctx(px, mask)
        wt = ctx.shift(rules_v2_weights(px, BAND0, GROSS))
        r, turn = ctx.run(wt)
        rs, ts = pd.Series(r, index=idx), pd.Series(turn, index=idx)
        for rung in RUNGS:
            net = (rs - ts * rung / 1e4).loc[start:]
            out[(pname, rung)] = dict(
                full=mets(net.values), oos=mets(net.loc[OOS_START:].values),
                spy_full=mets(spy.values), spy_oos=mets(spy.loc[OOS_START:].values))
    return out


# ==========================================================================================
# MAIN
# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 1010 (lane C, 2026-09-16) -- {STEM}")
    P("does the SOLE-KILLER MONOPOLY of the two LEVEL legs hold on the RECORD's committed")
    P("4b FAIL rows?   1007: SHARPE legs sole in 0 of 30 null cells; DD 5, CAGR 7.")
    P("=" * 100)
    P(__doc__.split("PRE-REGISTERED BARS")[1].split("SURVIVORSHIP")[0])

    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- printed before any result number is read")
    P("=" * 100)
    P("  scanning the committed corpus ...")
    per_file, agg, gstat = scan_corpus()
    pf = pd.DataFrame(per_file)
    gk, grows = {}, []

    n_rows_all = int(pf["rows"].sum())
    gk["G0"] = gstat["g0"] == 0
    grows.append(("G0", "every non-empty fail4b parses into the 5-leg alphabet",
                  f"{gstat['g0']:,} unparsed of {n_rows_all:,} rows "
                  f"({gstat['g0']/max(n_rows_all,1):.5f}) -- all EXCLUDED, none guessed",
                  "0", gk["G0"]))
    gk["G1"] = gstat["g1_bad"] == 0
    grows.append(("G1", "pass4b == (fail4b is the PASS sentinel)",
                  f"{gstat['g1_bad']:,} of {gstat['g1_seen']:,} disagree", "0", gk["G1"]))
    gk["G2"] = gstat["g2_bad"] == 0
    grows.append(("G2", "token set == set of False leg booleans",
                  f"{gstat['g2_bad']:,} of {gstat['g2_seen']:,} disagree", "0", gk["G2"]))

    P("  building the FRESH price arm ...")
    panels = {"U56": load_universe()} if SMOKE else {"U56": load_universe(),
                                                     "B136": load_universe(broad=True)}
    px = panels["U56"]
    idx = px.index

    # G3
    Wt = ranked_book(px, GROSS, 20)
    dr = dt = 0.0
    for freq in ("W", "M"):
        eng = engine.backtest(px, Wt, cost_bps=0.0, freq=freq)
        ctx = Ctx(px, engine.rebalance_mask(idx, freq))
        r, turn = ctx.run(ctx.shift(Wt))
        a = eng["returns"].loc[idx[WARM]:]
        b = pd.Series(r, index=idx).loc[idx[WARM]:]
        dr = max(dr, float(np.abs(a.values - b.values).max()))
        at = eng["turnover"].loc[idx[WARM]:]
        bt = pd.Series(turn, index=idx).loc[idx[WARM]:]
        dt = max(dt, float(np.abs(at.values - bt.values).max()))
    gk["G3"] = dr < 1e-12 and dt < 1e-10
    grows.append(("G3", "fast Ctx == engine.backtest (returns / turnover)",
                  f"{dr:.3e} / {dt:.3e}", "1e-12 / 1e-10", gk["G3"]))

    # G4
    d4 = float(np.abs(band_book(px, BAND0, GROSS).values
                      - rules_v2_weights(px, BAND0, GROSS).values).max())
    gk["G4"] = d4 == 0.0
    grows.append(("G4", "BAND03(0.03,0.75) == baseline.rules_v2_weights", f"{d4:.3e}", "0.0", gk["G4"]))

    FRESH, streams = build_fresh(panels)

    # G5
    ctx = Ctx(px, engine.rebalance_mask(idx, "W"))
    r1, _ = ctx.run(ctx.shift(ranked_book(px, GROSS, 20)))
    r2, _ = Ctx(px, engine.rebalance_mask(idx, "W")).run(ctx.shift(ranked_book(px, GROSS, 20)))
    d5 = float(np.abs(r1 - r2).max())
    gk["G5"] = d5 == 0.0
    grows.append(("G5", "determinism: a rebuilt FRESH cell reproduces its streams", f"{d5:.3e}",
                  "0.0", gk["G5"]))

    # ---- claim sets ----
    ALL_SETS, REAL_SETS, RECA, RECR = [], [], [], []
    FILE_ROWS = []
    for a in agg:
        ALL_SETS.append(a["masks"])
        REAL_SETS.append(a["masks"][~a["isnull"]])
        if a["rec"] is not None and a["rec_ok"]:
            rm, rn = a["rec"]
            RECA.append(rm)
            RECR.append(rm[~rn])
        c = census(a["masks"])
        d = shares(c, "STRICT")
        d.update(file=a["file"], n_fail=c["n"])
        FILE_ROWS.append(d)
    FILEDF = pd.DataFrame(FILE_ROWS)
    cat = lambda L: (np.concatenate(L) if L else np.zeros(0, np.int64))
    ALL_SETS, REAL_SETS = cat(ALL_SETS), cat(REAL_SETS)
    RECA, RECR = cat(RECA), cat(RECR)
    fm = np.array([parse_fail(s)[0] for s in FRESH["fail4b"]], np.int64)
    fresh_fail = fm[fm > 0]

    CLAIM = {"ALLROWS": ALL_SETS, "REALROWS": REAL_SETS, "FRESH": fresh_fail,
             "ALLROWS/RECOMP": RECA, "REALROWS/RECOMP": RECR}
    CENS = {k: census(v) for k, v in CLAIM.items() if len(v)}

    # G6 closure
    leftover = 0
    for k, c in CENS.items():
        leftover += abs(c["n"] - c["n_sole"] - c["n_multi"])
        leftover += abs(c["n"] - c["n_fsole"] - c["n_fmulti"])
    gk["G6"] = leftover == 0
    grows.append(("G6", "sole + multi partitions the FAIL population exactly",
                  f"{leftover} leftover", "0", gk["G6"]))

    # G7 fidelity
    fid = pf["recomp_fidelity"].dropna()
    n_adm = int(pf["recomp_admitted"].sum())
    n_num = int(pf["has_numerics"].sum())
    gk["G7"] = (n_num == 0) or (n_adm > 0)
    grows.append(("G7", f"RECOMP fidelity >= {FID_BAR:.2f} per file",
                  f"{n_adm} of {n_num} numeric files admitted; median fidelity "
                  f"{(fid.median() if len(fid) else float('nan')):.4f}",
                  ">=1 admitted", gk["G7"]))

    G = pd.DataFrame(grows, columns=["gate", "what", "observed", "bar", "pass"])
    P(G.to_string(index=False))
    P(f"  GATES: {int(G['pass'].sum())} of {len(G)} PASS")
    dump(G, "gates")
    dump(pf, "corpusfiles")

    # ======================================================================================
    P("")
    P("=" * 100)
    P("(B) THE CORPUS")
    P("=" * 100)
    P(f"  committed CSVs carrying a `fail4b` column     : {len(pf):,}")
    P(f"  rows read                                     : {int(pf['rows'].sum()):,}")
    P(f"  committed 4b FAIL rows (parsed)               : {int(pf['n_fail'].sum()):,}")
    P(f"  of which NULL-draw rows                       : {int(pf['null_rows'].sum()):,}")
    P(f"  of which REAL (not a null draw)               : {len(REAL_SETS):,}")
    P(f"  files carrying the 5 leg booleans             : {int(pf['has_legbools'].sum()):,}")
    P(f"  files carrying the full numeric set           : {n_num:,}  (admitted to RECOMP: {n_adm:,})")
    P(f"  FRESH priced cells / FAIL cells               : {len(FRESH):,} / {len(fresh_fail):,}")

    # ======================================================================================
    P("")
    P("=" * 100)
    P("(C) THE CENSUS -- 4 claim sets x 3 sole-binder definitions, ALL 12 cells reported")
    P("=" * 100)
    # populations: (claim set, definition) -> the mask array the census is read on.
    # STRICT and FAMILY read the COMMITTED string; RECOMP ignores it and reads the row's
    # own numerics.  FILEWT is the same populations, averaged one file at a time.
    POP = {("ALLROWS", "STRICT"): ALL_SETS, ("ALLROWS", "FAMILY"): ALL_SETS,
           ("ALLROWS", "RECOMP"): RECA,
           ("REALROWS", "STRICT"): REAL_SETS, ("REALROWS", "FAMILY"): REAL_SETS,
           ("REALROWS", "RECOMP"): RECR,
           ("FRESH", "STRICT"): fresh_fail, ("FRESH", "FAMILY"): fresh_fail,
           ("FRESH", "RECOMP"): fresh_fail}   # FRESH legs ARE recomputed, by construction
    cells = []
    for cs in ("ALLROWS", "REALROWS", "FILEWT", "FRESH"):
        for defn in ("STRICT", "FAMILY", "RECOMP"):
            if cs == "FILEWT":
                fr = []
                for a in agg:
                    if defn == "RECOMP":
                        if a["rec"] is None or not a["rec_ok"] or len(a["rec"][0]) == 0:
                            continue
                        c2 = census(a["rec"][0])
                        mode = "STRICT"
                    else:
                        c2 = census(a["masks"])
                        mode = defn
                    if c2["n"]:
                        fr.append(shares(c2, mode))
                if not fr:
                    cells.append(dict(claimset=cs, defn=defn, n=0))
                    continue
                d = pd.DataFrame(fr).mean().to_dict()
                c = dict(n=len(fr))
            else:
                pop = POP[(cs, defn)]
                if len(pop) == 0:
                    cells.append(dict(claimset=cs, defn=defn, n=0))
                    continue
                c = census(pop)
                d = shares(c, "STRICT" if defn == "RECOMP" else defn)
            row = dict(claimset=cs, defn=defn, n=c["n"])
            row.update({k: float(v) for k, v in d.items()})
            cells.append(row)
    CELLS = pd.DataFrame(cells)
    cols = ["claimset", "defn", "n", "sole_any", "sole_SHARPE", "sole_LEVEL",
            "sole_L1_H1", "sole_L2_H2", "sole_L3_OOS", "sole_L4_DD", "sole_L5_CAGR",
            "fsole_SHARPE", "fsole_DD", "fsole_CAGR"]
    cols = [c for c in cols if c in CELLS.columns]
    P(CELLS[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(CELLS, "census")

    # counts, plainly
    P("")
    P("  RAW SOLE-BINDER COUNTS (STRICT), the number 1007's '0 of 30' is compared against:")
    for cs in CENS:
        c = CENS[cs]
        P(f"    {cs:16s} n_FAIL {c['n']:9,}  sole {c['n_sole']:9,}  "
          + "  ".join(f"{LEGNAME[k]} {c['sole'][k]:,}" for k in LEGS))
        P(f"    {'':16s} family-sole {c['n_fsole']:9,}  "
          + "  ".join(f"{f} {c['fam_sole'][f]:,}" for f in ("SHARPE", "DD", "CAGR")))

    # ------------------------------------------------------------------ the decomposition
    ca = CENS["ALLROWS"]
    P("")
    P("  WHICH SHARPE LEG, ALONE?  (ALLROWS, STRICT -- the three legs 1007 pooled)")
    for k in ("H1", "H2", "OOS"):
        P(f"    {LEGNAME[k]:8s} sole on {ca['sole'][k]:7,} of {ca['n']:,} FAIL rows "
          f"({ca['sole'][k]/ca['n']:.5f}); {ca['sole'][k]/max(ca['n_sole'],1):.5f} of all "
          f"sole-binder rows")
    P(f"    -> the three pooled: {sum(ca['sole'][k] for k in ('H1','H2','OOS')):,} rows "
      f"({sum(ca['sole'][k] for k in ('H1','H2','OOS'))/ca['n']:.5f}).  1007 read 0 of 30.")
    P(f"    the two LEVEL legs : {ca['sole']['DD']+ca['sole']['CAGR']:,} rows "
      f"({(ca['sole']['DD']+ca['sole']['CAGR'])/ca['n']:.5f}), "
      f"{(ca['sole']['DD']+ca['sole']['CAGR'])/max(ca['n_sole'],1):.5f} of all sole rows")
    g1f = pf[pf["g1_disagree"] > 0]
    if len(g1f):
        P("")
        P("  G1's disagreeing files (a committed `pass4b` that its own `fail4b` contradicts):")
        for _, r in g1f.sort_values("g1_disagree", ascending=False).head(10).iterrows():
            P(f"    {r['g1_disagree']:5,} rows  {r['file']}")

    # ======================================================================================
    P("")
    P("=" * 100)
    P("(D) PRE-REGISTERED BARS")
    P("=" * 100)
    H = []
    a_str = shares(CENS["ALLROWS"], "STRICT")
    r_str = shares(CENS["REALROWS"], "STRICT")
    a_fam = shares(CENS["ALLROWS"], "FAMILY")
    f_str = shares(CENS["FRESH"], "STRICT")

    H.append(("H_MONO", "SHARPE legs sole on < 1.0% of committed FAIL rows (STRICT/ALLROWS)",
              f"{a_str['sole_SHARPE']:.4f}", f"< {MONO_BAR}", a_str["sole_SHARPE"] < MONO_BAR))
    H.append(("H_MONO_R", "same, REALROWS",
              f"{r_str['sole_SHARPE']:.4f}", f"< {MONO_BAR}", r_str["sole_SHARPE"] < MONO_BAR))
    H.append(("H_FAMILY", "SHARPE-alone < 5.0% under FAMILY x ALLROWS",
              f"{a_fam['sole_SHARPE']:.4f}", f"< {FAMILY_BAR}", a_fam["sole_SHARPE"] < FAMILY_BAR))
    take = (a_str["sole_LEVEL"] / a_str["sole_any"]) if a_str["sole_any"] > 0 else float("nan")
    H.append(("H_TAKE", "L4_DD + L5_CAGR take >= 90% of sole-binder rows (STRICT/ALLROWS)",
              f"{take:.4f}", f">= {TAKE_BAR}", bool(take >= TAKE_BAR)))
    tops = {}
    for cs in ("ALLROWS", "REALROWS", "FRESH"):
        s = shares(CENS[cs], "STRICT")
        tops[cs] = max(LEGS, key=lambda k: s[f"sole_{LEGNAME[k]}"])
    if not FILEDF.empty:
        w = FILEDF[FILEDF["n_fail"] > 0]
        m = w[[f"sole_{LEGNAME[k]}" for k in LEGS]].mean()
        tops["FILEWT"] = LEGS[int(np.argmax(m.values))]
    H.append(("H_STABLE", "same leg on top under all four claim sets (STRICT)",
              " / ".join(f"{k}:{LEGNAME[v]}" for k, v in tops.items()),
              "one leg", len(set(tops.values())) == 1))
    H.append(("H_FRESH", "FRESH reproduces the record's ordering and SHARPE-share side of 1.0%",
              f"top {LEGNAME[tops['FRESH']]}, SHARPE {f_str['sole_SHARPE']:.4f}",
              f"top {LEGNAME[tops['ALLROWS']]}, same side of {MONO_BAR}",
              bool(tops["FRESH"] == tops["ALLROWS"]
                   and ((f_str["sole_SHARPE"] < MONO_BAR) == (a_str["sole_SHARPE"] < MONO_BAR)))))

    # ======================================================================================
    P("")
    P("=" * 100)
    P("(E) PROTOCOL RULE 8 -- (book, cadence) chosen on 2009-2016 ALONE, OOS read once")
    P("=" * 100)
    BASE = baseline_rows(panels)
    CHOOSERS = {
        "C_ISSHARPE": lambda d: d.sort_values(["IS_Sharpe"], ascending=False).iloc[0],
        "C_ISCAGR":   lambda d: d.sort_values(["IS_CAGR"], ascending=False).iloc[0],
        "C_ISLEGS":   lambda d: d.assign(_L=d[[f"isleg_{LEGNAME[k]}" for k in LEGS]].sum(axis=1)
                                         ).sort_values(["_L", "IS_Sharpe"], ascending=False).iloc[0],
    }
    # IS-only legs (the 4b alphabet read entirely inside 2009-2016), chooser input only
    isleg = dict(
        H1=FRESH["IS_H1"] > FRESH["spy_IS_H1"],
        H2=FRESH["IS_H2"] > FRESH["spy_IS_H2"],
        OOS=FRESH["IS_Sharpe"] > FRESH["spy_IS_Sharpe"],
        DD=FRESH["IS_MaxDD"].abs() <= 0.60 * FRESH["spy_IS_MaxDD"].abs(),
        CAGR=FRESH["IS_CAGR"] >= 0.70 * FRESH["spy_IS_CAGR"])
    for k in LEGS:
        FRESH[f"isleg_{LEGNAME[k]}"] = isleg[k].values

    wf = []
    for pname in panels:
        for rung in RUNGS:
            d = FRESH[(FRESH.panel == pname) & (FRESH.cost_bps == rung)].copy()
            b = BASE[(pname, rung)]
            for cname, fn in CHOOSERS.items():
                pick = fn(d)
                lr = legs_rec(pick)
                p4b = all(lr[k] for k in LEGS)
                p4a = (pick["H1"] > b["full"]["H1"] and pick["H2"] > b["full"]["H2"]
                       and pick["MaxDD"] >= b["full"]["MaxDD"])
                wf.append(dict(panel=pname, cost_bps=rung, chooser=cname,
                               pick=f"{pick['book']}/{pick['cadence']}",
                               IS_Sharpe=pick["IS_Sharpe"], IS_CAGR=pick["IS_CAGR"],
                               OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                               OOS_MaxDD=pick["OOS_MaxDD"],
                               full_CAGR=pick["CAGR"], full_Sharpe=pick["Sharpe"],
                               full_MaxDD=pick["MaxDD"], H1=pick["H1"], H2=pick["H2"],
                               spy_OOS_CAGR=pick["spy_OOS_CAGR"],
                               spy_OOS_Sharpe=pick["spy_OOS_Sharpe"],
                               spy_OOS_MaxDD=pick["spy_OOS_MaxDD"],
                               base_OOS_CAGR=b["oos"]["CAGR"], base_OOS_Sharpe=b["oos"]["Sharpe"],
                               base_OOS_MaxDD=b["oos"]["MaxDD"],
                               pass4a=bool(p4a), pass4b=bool(p4b),
                               fail4b=",".join(LEGNAME[k] for k in LEGS if not lr[k]) or "-"))
    WF = pd.DataFrame(wf)
    P(WF[["panel", "cost_bps", "chooser", "pick", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
          "pass4a", "pass4b", "fail4b"]].to_string(index=False,
                                                   float_format=lambda x: f"{x:.4f}"))
    P(f"  OOS 4b {int(WF.pass4b.sum())} of {len(WF)};  OOS 4a {int(WF.pass4a.sum())} of {len(WF)}")
    for pname in panels:
        b = BASE[(pname, HEAD_COST)]
        P(f"  {pname:5s} @10bps  SPY       full {b['spy_full']['CAGR']:7.2%} "
          f"{b['spy_full']['Sharpe']:7.4f} {b['spy_full']['MaxDD']:7.2%}   "
          f"OOS {b['spy_oos']['CAGR']:7.2%} {b['spy_oos']['Sharpe']:7.4f} {b['spy_oos']['MaxDD']:7.2%}")
        P(f"  {pname:5s} @10bps  RULES v2  full {b['full']['CAGR']:7.2%} "
          f"{b['full']['Sharpe']:7.4f} {b['full']['MaxDD']:7.2%}   "
          f"OOS {b['oos']['CAGR']:7.2%} {b['oos']['Sharpe']:7.4f} {b['oos']['MaxDD']:7.2%}")
    dump(WF, "walkforward")
    dump(FRESH, "fresh")

    H.append(("H_RULE8", "an IS-only chooser delivers an OOS 4b pass on >= 1 (panel, rung)",
              f"{int(WF.pass4b.sum())} of {len(WF)}", ">= 1", bool(WF.pass4b.sum() >= 1)))
    HD = pd.DataFrame(H, columns=["bar", "what", "observed", "pre-registered", "pass"])
    P("")
    P(HD.to_string(index=False))
    P(f"  BARS: {int(HD['pass'].sum())} of {len(HD)} PASS")
    dump(HD, "hypotheses")

    # ======================================================================================
    P("")
    P("=" * 100)
    P("(F) BOTH KEEP PATHS")
    P("=" * 100)
    kp = []
    for _, r in WF.iterrows():
        kp.append(dict(panel=r.panel, cost_bps=r.cost_bps, chooser=r.chooser, pick=r["pick"],
                       keep4a=bool(r.pass4a), keep4b=bool(r.pass4b), fail4b=r.fail4b))
    KP = pd.DataFrame(kp)
    P(f"  4a (beat the book) : {int(KP.keep4a.sum())} of {len(KP)}")
    P(f"  4b (capital-worthy): {int(KP.keep4b.sum())} of {len(KP)}")
    dump(KP, "keeppaths")

    P("")
    P("=" * 100)
    P(f"DONE in {time.time()-t0:.1f}s")
    P("=" * 100)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES))


if __name__ == "__main__":
    main()
