#!/usr/bin/env python3
"""IDEA 211  re-read-every-published-clause-on-the-signed-statistic   (lane C, 2026-09-06)

THE QUESTION
------------
Clause 11/11b, as published by ideas 181 and 186 and carried by 191/192/201/207, is

        clears  <=>  |d_real|  >  max over K null draws of |d_null|                 (ABS/MAX)

Idea 190 showed that on the sleeve-substitution corpus this statistic clears 21/72 = 29.2%
where the SIGNED reading -- is the real arm the strict argmax of its own null population? --
clears 72/72, because the null population's mean is NEGATIVE and its largest-magnitude draws
are large and HARMFUL.  A two-sided magnitude band built from |d| is inflated by draws that
hurt, and it therefore hides real POSITIVE effects.  Idea 192 found the other face of the
same defect from the corpus side: NEG arms clear at 32.1% vs POS at 17.0%.

The queue asks for the census: re-read every committed clause on the signed percentile and
report how many published verdicts MOVE, and IN WHICH DIRECTION.

WHAT "MOVES" MEANS, STATED BEFORE ANY NUMBER IS READ
----------------------------------------------------
ABS/MAX and SIGNED/MAX have the SAME nominal size under exchangeability (1/(K+1)); they
test DIFFERENT alternatives (two-sided "differs" vs one-sided "helps").  A verdict that
moves is therefore not automatically an error.  Two directions, with different meanings:

  1 -> 0  LOST.  Published "clears"; the real arm is not the signed argmax.  Two sub-cases,
          and only one of them is a correction:
            (a) d_real < 0  -- a HARMFUL arm was published as clearing a significance band.
                Every use of that row as evidence that the instrument DOES something is
                intact; every use of it as evidence that the instrument is WORTH something
                is void.  This is idea 192's mechanism, counted arm by arm.
            (b) d_real > 0 but some null draw beat it -- a genuine loss of power? no: it is
                the same size test, so this is the honest one-sided answer.
  0 -> 1  GAINED.  Published "inside the band"; the real arm is the strict signed argmax.
          The band was inflated by a harmful draw.  These are the rows where the record
          UNDERSTATED a real positive effect.

  Q1  THE CENSUS.  Every committed clause verdict that can be re-read, under all four
      arms, with the move counts and their split by sign(d_real).
  Q2  THE MECHANISM.  Is the band's max attained by a NEGATIVE draw, and is the null mean
      negative?  If the two are common, ABS/MAX is systematically the wrong band.
  Q3  RULE 8 (PROTOCOL 8, required).  Does the statistic change move a DECISION?  The clause
      is read on the IS window only (<= 2016-12-31), an arm is chosen, 2017-2026 is read
      ONCE, against the do-nothing control, RULES v1 and SPY.
  Q4  BOTH KEEP PATHS (4a vs the panel's own RULES v1, 4b vs SPY) on every real arm, and
      whether the statistic change moves any KEEP.

THE CORPORA (every committed clause file with per-draw data, or exactly regenerable draws)
------------------------------------------------------------------------------------------
  T  keyed tilts, idea 181.  `...does-a-null-column-change-any-published-verdict_cloud`
     grid.csv commits all 720 nullkey rows (36 cells x 20 draws) WITH SIGNED dSharpe_F /
     dSharpe_IS / dSharpe_OOS, and clause.csv commits the 360 published verdicts (180 arms
     x windows F, IS).  PURE RE-READ -- no backtest is re-run.
  O  overlays, ideas 186/191/201/207.  Per-draw signs were NOT committed, so the draws are
     REGENERATED with idea 201's deterministic seed (zlib.crc32; idea 191's own seed used
     hash() and is not reproducible across processes, which is why idea 201's rows are the
     canonical ones and idea 207 reproduced them at 9.7e-17).  60 rotations per config in
     3 disjoint blocks of 20, exactly idea 201's pool; block 0 is the published band.  The
     regeneration is ASSERTED against the committed clause.csv before anything is read.
     540 published verdicts (180 Sharpe + 180 drawdown + 180 IS-window).
  S  sleeve substitution, idea 190.  null.csv commits all 10344 per-draw rows.  190 already
     published BOTH statistics, so this corpus is the VALIDATION that the re-read reproduces
     a signed reading someone else computed independently.  96 clause rows.

  Not re-readable, and reported as a coverage gap rather than skipped in silence: idea 186's
  own null.csv (2 summary rows per config, no per-draw), idea 191's clause.csv (bands only,
  and a salted seed), idea 207's flip.csv/exact.csv and the 11b enumeration (K-counts on |d|
  only -- the enumeration threw the signs away).  Idea 192's repro_Tclause.csv is a subset of
  corpus T and is counted once, inside T.
  `...does-a-random-screen-de-concentrate-just-as-well_B.null.csv` already publishes a SIGNED
  p5/p50/p95 band on 6 selector rows; it is listed and read, and cannot move.

  TUNED PARAMETER 1: the statistic      {ABS (published), SIGNED}
  TUNED PARAMETER 2: the band           {MAX, Q95}
  -> 4 arms, every one reported on every corpus.  K is held at the PUBLISHED draw count
     (20 for T and O; the full enumerated pool for S) -- idea 207 already swept K and a
     third dial is not taken here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  All three reproductions pass: T's 360 published verdicts recompute from grid.csv
      exactly; S's published pct_signedSharpe / argmax_full recompute exactly; O's
      regenerated bands match idea 201's committed clause.csv at < 1e-12 on all 180 rows.
  P2  On the pooled corpus the SIGNED reading LOSES more verdicts than it gains -- because
      the record's clause hits are concentrated on NEG arms (idea 192: 32.1% vs 17.0%).
  P3  A MAJORITY of the 1 -> 0 losses are sub-case (a): d_real < 0.  These are the rows
      whose published significance claim does not survive being asked the useful question.
  P4  The band's max is attained by a NEGATIVE draw in more than 40% of configurations, and
      the null mean is negative in a majority -- the mechanism idea 190 named, generalised.
  P5  No clause-gated selector, under EITHER statistic, beats the do-nothing control out of
      sample.  (This project's thirteenth consecutive such test; the signed gate is a
      better-aimed filter over a pool whose mean is negative, which idea 204 predicts still
      loses.)
  P6  The statistic change moves ZERO 4b passes, on either corpus.  The clause is a
      reporting column; 4a/4b are computed from returns and cannot be touched by it.

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): every panel is CURRENT constituents; the small panel has no
    delistings.  Real and null draws inherit it identically so the CLAUSE reading is
    unaffected; every LEVEL (CAGR, Sharpe, 4a/4b counts) is biased upward and is not a
    tradable estimate.
  * The signed reading is ONE-SIDED by construction: an arm with d_real < 0 can never clear
    it.  That is the intent (the clause exists to certify that an instrument is worth
    something) but it means SIGNED is not a drop-in replacement for a two-sided claim, and
    the count of 1 -> 0 moves is NOT by itself a count of errors.  Both readings are printed
    for every row so a reader can take either.
  * Corpus O's rotations are neighbouring circular shifts of the same ON series and are
    strongly correlated (idea 207); the nominal size 1/(K+1) is nominal, not realised.
    Idea 191 measured the realised size at 4.8% on a zero-information control, so the
    approximation is good on that corpus but it is an approximation.
  * BUDGET-skip does not preserve turnover between real and null (idea 203); inherited.
  * Idea 38: calendar-day index after 2014-09-17 on U56/BROAD136.  Idea 126: t+1 only.
  * PROTOCOL 2: 10 bps is the binding cost rung; 25 bps is carried as a reported axis.

Deterministic, standalone.  Writes .console.txt, .reread.csv, .summary.csv, .mechanism.csv,
.walkforward.csv, .keep.csv.
"""
import importlib.util
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-06_re-read-every-published-clause-on-the-signed-statistic_C"
OUT = ROOT / "research" / "backtests"

T_STEM = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"      # idea 181
O_PARENT = "2026-09-05_the-on-share-column_cloud"                                # idea 191
O_STEM = "2026-09-05_the-margin-column-instead-of-two_cloud"                     # idea 201
S_STEM = "2026-09-05_is-the-conditional-sleeve-anything-at-all_B"                # idea 190
SEL_STEM = "2026-09-05_does-a-random-screen-de-concentrate-just-as-well_B"       # selector null

N_ROT, BLOCK = 60, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI, DELTA = 0.70, 0.60
STATS = ["ABS", "SIGNED"]
BANDS = ["MAX", "Q95"]
ARMS = [(s, b) for s in STATS for b in BANDS]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def band_of(vals, band):
    v = np.asarray(vals, float)
    if band == "MAX":
        return float(np.max(v))
    if band == "Q95":
        return float(np.quantile(v, 0.95, method="linear"))
    raise ValueError(band)


def clears(d, nulls, stat, band):
    """The four arms.  ABS = the published two-sided magnitude clause; SIGNED = is the real
    arm above the band of the SIGNED null draws (one-sided, 'helps')."""
    n = np.asarray(nulls, float)
    n = n[np.isfinite(n)]
    if not np.isfinite(d) or len(n) == 0:
        return np.nan
    if stat == "ABS":
        return bool(abs(d) > band_of(np.abs(n), band))
    return bool(d > band_of(n, band))


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 2 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def sh(r):
    return metrics(r)["Sharpe"] if len(r) > 5 else np.nan


def halves_of(r):
    h = len(r) // 2
    return sh(r.iloc[:h]), sh(r.iloc[h:])


def fail_4a(row, base):
    """row/base: dicts with Sharpe_H1, Sharpe_H2, MaxDD_F."""
    f = []
    if not row["Sharpe_H1"] > base["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > base["Sharpe_H2"]: f.append("H2")
    if not row["MaxDD_F"] >= base["MaxDD_F"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(row, spy):
    f = []
    if not row["Sharpe_H1"] > spy["Sharpe_H1"]: f.append("H1")
    if not row["Sharpe_H2"] > spy["Sharpe_H2"]: f.append("H2")
    if not row["Sharpe_OOS"] > spy["Sharpe_OOS"]: f.append("OOS")
    if not abs(row["MaxDD_F"]) <= DELTA * abs(spy["MaxDD_F"]): f.append("DD")
    if not row["CAGR_F"] >= PHI * spy["CAGR_F"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ============================================================================== corpus T (181)
def corpus_T():
    """Pure re-read of idea 181's committed grid.csv + clause.csv."""
    G = pd.read_csv(OUT / f"{T_STEM}.grid.csv")
    C = pd.read_csv(OUT / f"{T_STEM}.clause.csv")
    P(f"\n  [T] idea 181: grid {G.shape}, clause {C.shape}  "
      f"({int((G.kind == 'nullkey').sum())} null draws, {int((G.kind == 'real').sum())} real arms)")

    cell = ["panel", "dir", "m", "cost"]
    rows = []
    for (pn, dr, m, c), sub in G[G.kind == "nullkey"].groupby(cell):
        for win, col in [("F", "dSharpe_F"), ("IS", "dSharpe_IS")]:
            rows.append(dict(panel=pn, dir=dr, m=m, cost=c, window=win,
                             nulls=sub[col].values))
    NB = {(r["panel"], r["dir"], r["m"], r["cost"], r["window"]): r["nulls"] for r in rows}

    out = []
    for _, r in C.iterrows():
        k = (r["panel"], r["dir"], r["m"], r["cost"], r["window"])
        nb = NB[k]
        d = float(r["d"])
        rec = dict(corpus="T", ref="idea181", panel=r["panel"], family=r["key"],
                   arm=f"{r['dir']}/m={r['m']}", cost=r["cost"], window=r["window"],
                   stat_kind="Sharpe", d=d, K=len(nb),
                   null_mean=float(np.mean(nb)), null_absmax=float(np.abs(nb).max()),
                   argmax_is_negative=bool(nb[np.argmax(np.abs(nb))] < 0),
                   published=bool(int(r["clears"])))
        for s, b in ARMS:
            rec[f"{s}_{b}"] = clears(d, nb, s, b)
        out.append(rec)
    R = pd.DataFrame(out)

    # ---- reproduction: the published verdict IS ABS/MAX recomputed from the committed draws
    mism = int((R["published"] != R["ABS_MAX"]).sum())
    dmax = float((R["null_absmax"].values - C["null_max"].values).__abs__().max())
    dmean = float((R["null_mean"].values - C["null_mean"].values).__abs__().max())
    P(f"  [T] reproduction: published clears == ABS/MAX recomputed on the committed draws in "
      f"{len(R) - mism}/{len(R)} rows;  max|band - committed null_max| = {dmax:.3e}")
    P(f"      NOTE idea 181 committed null_mean over |d| (mean of the ABS draws); this run's "
      f"null_mean is over the SIGNED draws, so they differ by construction "
      f"(max|diff| {dmean:.3e}) -- that difference IS the subject of this run.")
    return R, G, mism == 0 and dmax < 1e-12


# ============================================================================== corpus S (190)
def corpus_S():
    """Pure re-read of idea 190's committed null.csv (per-draw) + grid.csv (the R20 base)."""
    NU = pd.read_csv(OUT / f"{S_STEM}.null.csv")
    G = pd.read_csv(OUT / f"{S_STEM}.grid.csv")
    CL = pd.read_csv(OUT / f"{S_STEM}.clause.csv")
    P(f"\n  [S] idea 190: null {NU.shape} (per-draw), grid {G.shape}, clause {CL.shape}")

    base = {(r.panel, r.n, r.bps): r for r in G[G.set_ == "R20"].itertuples()}
    real = {(r.panel, r.n, r.bps, r.set_, r.f): r for r in G[G.kind == "real"].itertuples()}

    out = []
    for _, r in CL.iterrows():
        b = base[(r["panel"], r["n"], r["bps"])]
        rr = real[(r["panel"], r["n"], r["bps"], r["set_"], r["f"])]
        q = NU[(NU.panel == r["panel"]) & (NU.n == r["n"]) & (NU.bps == r["bps"])
               & (NU.set_ == r["set_"]) & (NU.f == r["f"]) & (NU.pool == r["pool"])]
        nS = q.Sharpe.values - b.Sharpe
        nD = abs(b.MaxDD) - q.MaxDD.abs().values
        dS = rr.Sharpe - b.Sharpe
        dD = abs(b.MaxDD) - abs(rr.MaxDD)
        for lab, d, nb, pub in [("Sharpe", dS, nS, bool(r["clears_S_strict"])),
                                ("MaxDD", dD, nD, bool(r["clears_D_strict"]))]:
            rec = dict(corpus="S", ref="idea190", panel=r["panel"],
                       family=f"{r['set_']}/{r['pool']}", arm=f"n={r['n']}/f={r['f']}",
                       cost=r["bps"], window="F", stat_kind=lab, d=float(d), K=len(nb),
                       null_mean=float(np.mean(nb)), null_absmax=float(np.abs(nb).max()),
                       argmax_is_negative=bool(nb[np.argmax(np.abs(nb))] < 0),
                       published=pub)
            for s, bd in ARMS:
                rec[f"{s}_{bd}"] = clears(d, nb, s, bd)
            out.append(rec)
    R = pd.DataFrame(out)

    # ---- reproduction against idea 190's own published signed columns
    chk = R[R.stat_kind == "Sharpe"].reset_index(drop=True)
    mism_abs = int((chk["published"] != chk["ABS_MAX"]).sum())
    mism_sgn = int((chk["SIGNED_MAX"].values != CL["argmax_full"].values).sum())
    dchk = float((chk["d"].values - CL["dSharpe"].values).__abs__().max())
    P(f"  [S] reproduction: ABS/MAX == published clears_S_strict in {len(chk) - mism_abs}/{len(chk)};"
      f"  SIGNED/MAX == published argmax_full in {len(chk) - mism_sgn}/{len(chk)};"
      f"  max|dSharpe - committed| = {dchk:.3e}")
    ok = mism_abs == 0 and mism_sgn == 0 and dchk < 1e-12
    return R, ok


# ============================================================================== corpus O (201)
def det_seed(*parts):
    """Idea 201's seed, verbatim."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2**31)


def corpus_O(p191, t0):
    """Regenerate idea 201's 60-rotation pool KEEPING SIGNS, assert against its clause.csv."""
    C201 = pd.read_csv(OUT / f"{O_STEM}.clause.csv")
    P(f"\n  [O] idea 201: clause {C201.shape}; regenerating its rotation pool with signs "
      "(3 panels x 3 families x 5 thr x 2 depth x (1 real + 60 rotations) x 2 cost)")

    panels = p191.build_panels()
    FAMILIES, FAM_ORDER = p191.FAMILIES, p191.FAM_ORDER
    COST_RUNGS = [10, 25]
    cache = OUT / f"{STEM}.grid.csv.gz"
    rows, panel_ref = [], {}
    for pan in panels:
        start = pan.start
        spy = pan.spy.loc[start:]
        bf = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt = bf["returns"].loc[start:], bf["turnover"].loc[start:]
        c0 = pan._r0
        sm, sh1, sh2 = metrics(spy), *halves_of(spy)
        panel_ref[pan.name] = dict(
            spy=dict(CAGR_F=sm["CAGR"], Sharpe_F=sm["Sharpe"], MaxDD_F=sm["MaxDD"],
                     Sharpe_H1=sh1, Sharpe_H2=sh2,
                     Sharpe_OOS=sh(spy.loc[OOS_START:]),
                     CAGR_OOS=metrics(spy.loc[OOS_START:])["CAGR"],
                     MaxDD_OOS=metrics(spy.loc[OOS_START:])["MaxDD"]),
            v1={c: (lambda r: dict(CAGR_F=metrics(r)["CAGR"], Sharpe_F=metrics(r)["Sharpe"],
                                   MaxDD_F=metrics(r)["MaxDD"],
                                   Sharpe_H1=halves_of(r)[0], Sharpe_H2=halves_of(r)[1],
                                   Sharpe_OOS=sh(r.loc[OOS_START:]),
                                   CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                   MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"]))(
                        b0 - bt * c / 1e4) for c in COST_RUNGS})
        if cache.exists():
            continue
        for fam in FAM_ORDER:
            _, thrs, _, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = p191.on_indicator(pan, fam, thr)
                J = len(s_real)
                offs = p191.rotations(J, N_ROT, det_seed(pan.name, fam, thr))
                for depth in depths:
                    variants = [("real", 0, -1, s_real)] + [
                        ("null", o, i // BLOCK, np.roll(s_real, o)) for i, o in enumerate(offs)]
                    for kind, off, blk, s in variants:
                        W, mask = p191.apply_overlay(pan, fam, depth, s)
                        res = p191.fast_backtest(pan.px, W, 0.0, p191.FREQ, mask=mask)
                        for bps in COST_RUNGS:
                            r = p191.net(res, bps).loc[start:]
                            cr = p191.net(c0, bps).loc[start:]
                            m, mc = metrics(r), metrics(cr)
                            h1, h2 = halves_of(r)
                            rows.append(dict(
                                panel=pan.name, family=fam, thr=float(thr), depth=str(depth),
                                bps=bps,
                                kind=kind, offset=off, block=blk, on_share=float(s.mean()),
                                CAGR_F=m["CAGR"], Sharpe_F=m["Sharpe"], MaxDD_F=m["MaxDD"],
                                Sharpe_H1=h1, Sharpe_H2=h2,
                                Sharpe_IS=sh(r.loc[:IS_END]), Sharpe_OOS=sh(r.loc[OOS_START:]),
                                CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                                ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                                ctrl_Sharpe_IS=sh(cr.loc[:IS_END]),
                                ctrl_Sharpe_OOS=sh(cr.loc[OOS_START:]),
                                ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                                ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"]))
        P(f"      {pan.name} done ({time.time() - t0:.0f}s)")

    if cache.exists():
        # keep_default_na=False: the literal kind "null" is a pandas default NA token
        G = pd.read_csv(cache, keep_default_na=False, na_values=[""])
        P(f"      reusing the committed signed-draw grid {cache.name} ({len(G)} rows) -- the "
          "regeneration is deterministic and is asserted against idea 201 below either way")
    else:
        G = pd.DataFrame(rows)
        G.to_csv(cache, index=False)
        P(f"      wrote the signed-draw grid {cache.name} ({len(G)} rows) -- the per-draw SIGNS "
          "the record never committed")
    G["dSharpe"] = G["Sharpe_F"] - G["ctrl_Sharpe"]
    G["dSharpe_IS"] = G["Sharpe_IS"] - G["ctrl_Sharpe_IS"]
    G["dSharpe_OOS"] = G["Sharpe_OOS"] - G["ctrl_Sharpe_OOS"]
    G["dMaxDD"] = G["MaxDD_F"] - G["ctrl_MaxDD"]

    key = ["panel", "family", "thr", "depth", "bps"]
    out, mech = [], []
    for k, sub in G.groupby(key):
        r = sub[sub.kind == "real"].iloc[0]
        nb0 = sub[(sub.kind == "null") & (sub.block == 0)]
        specs = [("Sharpe", "F", float(r["dSharpe"]), nb0["dSharpe"].values),
                 ("MaxDD", "F", float(r["dMaxDD"]), nb0["dMaxDD"].values),
                 ("Sharpe", "IS", float(r["dSharpe_IS"]), nb0["dSharpe_IS"].values)]
        for lab, win, d, nb in specs:
            nbf = nb[np.isfinite(nb)]
            rec = dict(corpus="O", ref="idea201", panel=k[0], family=k[1],
                       arm=f"thr={k[2]}/{k[3]}", thr=float(k[2]), depth=k[3],
                       cost=k[4], window=win, stat_kind=lab, d=d, K=len(nbf),
                       null_mean=float(np.mean(nbf)) if len(nbf) else np.nan,
                       null_absmax=float(np.abs(nbf).max()) if len(nbf) else np.nan,
                       argmax_is_negative=(bool(nbf[np.argmax(np.abs(nbf))] < 0)
                                           if len(nbf) else np.nan),
                       published=np.nan)
            for s, bd in ARMS:
                rec[f"{s}_{bd}"] = clears(d, nbf, s, bd)
            out.append(rec)
        mech.append(dict(panel=k[0], family=k[1], thr=float(k[2]), depth=k[3], bps=k[4],
                         band=float(np.abs(nb0["dSharpe"].values).max()),
                         band_IS=float(np.abs(nb0["dSharpe_IS"].values).max()),
                         band_OOS=float(np.abs(nb0["dSharpe_OOS"].values).max()),
                         bandDD=float(np.abs(nb0["dMaxDD"].values).max()),
                         dSharpe=float(r["dSharpe"]), dSharpe_IS=float(r["dSharpe_IS"]),
                         dMaxDD=float(r["dMaxDD"])))
    R = pd.DataFrame(out)
    M = pd.DataFrame(mech)

    # ---- reproduction against idea 201's committed clause.csv
    mg = M.merge(C201, on=key, suffixes=("", "_p"))
    P(f"  [O] reproduction vs {O_STEM}.clause.csv ({len(mg)}/{len(C201)} rows matched):")
    worst = 0.0
    for c in ["band", "band_IS", "band_OOS", "bandDD", "dSharpe", "dSharpe_IS", "dMaxDD"]:
        dd = float((mg[c] - mg[c + "_p"]).abs().max())
        worst = max(worst, dd)
        P(f"        max|d {c:<10s}| = {dd:.3e}  -> {'PASS' if dd < 1e-12 else 'FAIL'}")
    # carry idea 201's published verdicts onto the re-read rows
    pub = {}
    for _, r in C201.iterrows():
        kk = (r["panel"], r["family"], float(r["thr"]), str(r["depth"]), int(r["bps"]))
        pub[(kk, "Sharpe", "F")] = bool(r["clears"])
        pub[(kk, "MaxDD", "F")] = bool(r["clearsDD"])
        pub[(kk, "Sharpe", "IS")] = bool(r["clears_IS"])
    R["published"] = [pub[((r.panel, r.family, float(r.thr), str(r.depth), int(r.cost)),
                           r.stat_kind, r.window)] for r in R.itertuples()]
    # The 2 SMALL439 / BUDGET tau=0.05 / skip cells have an undefined IS Sharpe (idea 207's
    # documented caveat: the overlay suppresses 93.7% of rebalances and the book is flat
    # through the IS window).  Dropped, counted, never imputed.
    nanrows = R[~np.isfinite(R["d"])]
    R = R[np.isfinite(R["d"])].reset_index(drop=True)
    mismatch = int((R["published"] != R["ABS_MAX"]).sum())
    P(f"  [O] published verdicts == ABS/MAX regenerated: {len(R) - mismatch}/{len(R)}")
    P(f"      dropped {len(nanrows)} of 540 verdicts with an undefined d (idea 207's "
      f"documented cells): "
      + ", ".join(f"{r.panel}/{r.family}/{r.arm}/{int(r.cost)}bps/{r.window}"
                  for r in nanrows.itertuples()))
    return R, G, panel_ref, worst < 1e-12 and mismatch == 0


# ============================================================================== main
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 211  re-read-every-published-clause-on-the-signed-statistic   (lane C, 2026-09-06)")
    P("  ABS/MAX  = clause 11b as published:  |d| > max_K |d_null|      (two-sided, 'differs')")
    P("  SIGNED   = idea 190's reading:        d  > band_K( d_null )    (one-sided, 'helps')")
    P("  bands    = MAX (nominal size 1/(K+1)) and Q95 (nominal 5%, idea 207's proposal)")
    P("=" * 118)

    P("\n" + "=" * 118)
    P("[0] REPRODUCTION -- nothing below is read unless all three corpora reproduce")
    P("=" * 118)
    spec = importlib.util.spec_from_file_location("p191", OUT / f"{O_PARENT}.py")
    p191 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p191)

    RT, GT, okT = corpus_T()
    RS, okS = corpus_S()
    RO, GO, panel_ref, okO = corpus_O(p191, t0)

    SEL = pd.read_csv(OUT / f"{SEL_STEM}.null.csv")
    P(f"\n  [selector null] {SEL_STEM}.null.csv: {len(SEL)} rows already published on a SIGNED "
      f"p5/p50/p95 band (`pct`, `inside_90`) -- cannot move; carried for completeness.")
    P("    " + SEL[["selector", "real_dOOS", "null_mean", "pct", "inside_90"]]
      .to_string(index=False).replace("\n", "\n    "))

    if not (okT and okS and okO):
        P(f"\nREPRODUCTION FAILS (T={okT} S={okS} O={okO}) -- STOP, nothing below is valid")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        raise SystemExit("reproduction failed")
    P("\n  all three corpora reproduce -- proceeding")

    R = pd.concat([RT, RS, RO], ignore_index=True)
    R.to_csv(OUT / f"{STEM}.reread.csv", index=False)

    # ---------------------------------------------------------------------------- Q1 census
    P("\n" + "=" * 118)
    P("[Q1] THE CENSUS.  Every re-readable published clause verdict, under all four arms.")
    P("=" * 118)
    P(f"\n  corpus coverage: {len(R)} published verdicts re-read")
    P(R.groupby(["corpus", "ref", "stat_kind", "window"]).size().rename("verdicts").to_frame()
      .to_string())

    summ = []
    for (corp, sk), sub in R.groupby(["corpus", "stat_kind"]):
        pubc = int(sub["published"].sum())
        for s, b in ARMS:
            col = sub[f"{s}_{b}"].astype(bool)
            gained = int((~sub["published"].astype(bool) & col).sum())
            lost = int((sub["published"].astype(bool) & ~col).sum())
            lost_neg = int((sub["published"].astype(bool) & ~col & (sub["d"] < 0)).sum())
            summ.append(dict(corpus=corp, stat_kind=sk, arm=f"{s}/{b}", n=len(sub),
                             published_clears=pubc, arm_clears=int(col.sum()),
                             gained_0to1=gained, lost_1to0=lost, lost_and_harmful=lost_neg,
                             moved=gained + lost,
                             moved_pct=100.0 * (gained + lost) / len(sub)))
    S = pd.DataFrame(summ)
    S.to_csv(OUT / f"{STEM}.summary.csv", index=False)
    P("\n  per corpus x statistic-kind, ALL FOUR ARMS (published = ABS/MAX by construction):")
    P(S.to_string(index=False, float_format=lambda x: f"{x:.1f}"))

    P("\n  POOLED over every re-readable verdict:")
    for s, b in ARMS:
        col = R[f"{s}_{b}"].astype(bool)
        pub = R["published"].astype(bool)
        g, l = int((~pub & col).sum()), int((pub & ~col).sum())
        ln = int((pub & ~col & (R["d"] < 0)).sum())
        P(f"    {s:6s}/{b:3s}  clears {int(col.sum()):3d}/{len(R)} ({col.mean():5.1%})   "
          f"gained 0->1 {g:3d}   lost 1->0 {l:3d}  (of which d<0, i.e. HARMFUL: {ln:3d} = "
          f"{(ln / l if l else float('nan')):.0%})   moved {g + l:3d} = "
          f"{(g + l) / len(R):.1%} of the record")

    P("\n  the 1 -> 0 losses, split by sign of the real effect (the direction that matters):")
    pub = R["published"].astype(bool)
    for s, b in ARMS:
        col = R[f"{s}_{b}"].astype(bool)
        lost = R[pub & ~col]
        P(f"    {s:6s}/{b:3s}  n={len(lost):3d}   d<0 {int((lost['d'] < 0).sum()):3d}   "
          f"d>0 {int((lost['d'] > 0).sum()):3d}   mean d {lost['d'].mean():+.4f}   "
          f"mean null mean {lost['null_mean'].mean():+.4f}")
    P("\n  the 0 -> 1 gains (the record understated a positive effect):")
    for s, b in ARMS:
        col = R[f"{s}_{b}"].astype(bool)
        gn = R[~pub & col]
        P(f"    {s:6s}/{b:3s}  n={len(gn):3d}   mean d {gn['d'].mean():+.4f}   "
          f"mean |null|max {gn['null_absmax'].mean():.4f}   "
          f"band max attained by a NEGATIVE draw in "
          f"{gn['argmax_is_negative'].mean() if len(gn) else float('nan'):.0%}")

    # ------------------------------------------------------------------------- Q2 mechanism
    P("\n" + "=" * 118)
    P("[Q2] THE MECHANISM.  Is the two-sided band built out of draws that HURT?")
    P("=" * 118)
    mech = R.groupby(["corpus", "stat_kind"]).agg(
        n=("d", "size"), null_mean=("null_mean", "mean"),
        null_mean_neg=("null_mean", lambda x: float((x < 0).mean())),
        absmax_is_neg=("argmax_is_negative", "mean"), mean_d=("d", "mean")).reset_index()
    P(mech.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\n  POOLED: the band's largest-magnitude draw is NEGATIVE in "
      f"{R['argmax_is_negative'].mean():.1%} of {len(R)} verdicts; the null population mean is "
      f"negative in {(R['null_mean'] < 0).mean():.1%}.")
    R.groupby(["corpus", "stat_kind", "window"]).agg(
        n=("d", "size"), null_mean=("null_mean", "mean"),
        absmax_is_neg=("argmax_is_negative", "mean")).to_csv(OUT / f"{STEM}.mechanism.csv")

    # ---------------------------------------------------------------- Q3 rule 8 walk-forward
    P("\n" + "=" * 118)
    P("[Q3] RULE 8 WALK-FORWARD.  Clause read on <= 2016-12-31 only; 2017-2026 read ONCE.")
    P("     Does the statistic change move a DECISION?")
    P("=" * 118)

    # ---- corpus O: 18 cells (3 panels x 3 families x 2 cost), 10 arms each
    keyO = ["panel", "family", "thr", "depth", "bps"]
    realO = GO[GO.kind == "real"].copy()
    nb_is = {k: sub[(sub.kind == "null") & (sub.block == 0)]["dSharpe_IS"].values
             for k, sub in GO.groupby(keyO)}
    for s, b in ARMS:
        realO[f"gate_{s}_{b}"] = [
            clears(float(r["dSharpe_IS"]),
                   nb_is[(r["panel"], r["family"], r["thr"], r["depth"], r["bps"])], s, b)
            for _, r in realO.iterrows()]
    rows = []
    for (pn, fam, bps), sub in realO.groupby(["panel", "family", "bps"]):
        sub = sub[np.isfinite(sub["dSharpe_IS"])]
        if sub.empty:
            continue
        c = sub.iloc[0]
        cell = f"{pn}/{fam}/{bps}bps"
        do_nothing = dict(sel="S0 do-nothing", corpus="O", cell=cell, pick="-",
                          Sharpe_OOS=float(c["ctrl_Sharpe_OOS"]),
                          CAGR_OOS=float(c["ctrl_CAGR_OOS"]),
                          MaxDD_OOS=float(c["ctrl_MaxDD_OOS"]))
        rows.append(do_nothing)
        bst = sub.loc[sub["dSharpe_IS"].idxmax()]
        rows.append(dict(sel="S1 IS-argmax (no gate)", corpus="O", cell=cell,
                         pick=f"thr={bst['thr']}/{bst['depth']}",
                         Sharpe_OOS=float(bst["Sharpe_OOS"]), CAGR_OOS=float(bst["CAGR_OOS"]),
                         MaxDD_OOS=float(bst["MaxDD_OOS"])))
        for s, b in ARMS:
            g = sub[sub[f"gate_{s}_{b}"] == True]  # noqa: E712
            if len(g):
                gg = g.loc[g["dSharpe_IS"].idxmax()]
                rows.append(dict(sel=f"S2 gate {s}/{b}", corpus="O", cell=cell,
                                 pick=f"thr={gg['thr']}/{gg['depth']}",
                                 Sharpe_OOS=float(gg["Sharpe_OOS"]),
                                 CAGR_OOS=float(gg["CAGR_OOS"]),
                                 MaxDD_OOS=float(gg["MaxDD_OOS"])))
            else:
                rows.append(dict(sel=f"S2 gate {s}/{b}", corpus="O", cell=cell, pick="(none)",
                                 **{k2: do_nothing[k2] for k2 in
                                    ("Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS")}))
        rows.append(dict(sel="REF RULES v1", corpus="O", cell=cell, pick="-",
                         Sharpe_OOS=panel_ref[pn]["v1"][bps]["Sharpe_OOS"],
                         CAGR_OOS=panel_ref[pn]["v1"][bps]["CAGR_OOS"],
                         MaxDD_OOS=panel_ref[pn]["v1"][bps]["MaxDD_OOS"]))
        rows.append(dict(sel="REF SPY", corpus="O", cell=cell, pick="-",
                         Sharpe_OOS=panel_ref[pn]["spy"]["Sharpe_OOS"],
                         CAGR_OOS=panel_ref[pn]["spy"]["CAGR_OOS"],
                         MaxDD_OOS=panel_ref[pn]["spy"]["MaxDD_OOS"]))

    # ---- corpus T: 36 cells (3 panels x 2 dirs x 3 m x 2 cost), 5 keys each
    P("\n  building the corpus-T reference books (RULES v1 and SPY on idea 181's panels)")
    Tpanels = {"u56": load_universe(), "broad": load_universe(broad=True)}
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    Tpanels["small"] = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    tref = {}
    for pn, px in Tpanels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bf = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq="W")
        b0, bt = bf["returns"].loc[start:], bf["turnover"].loc[start:]
        tref[pn] = dict(spy=dict(Sharpe_OOS=sh(spy.loc[OOS_START:]),
                                 CAGR_OOS=metrics(spy.loc[OOS_START:])["CAGR"],
                                 MaxDD_OOS=metrics(spy.loc[OOS_START:])["MaxDD"],
                                 CAGR_F=metrics(spy)["CAGR"], Sharpe_F=metrics(spy)["Sharpe"],
                                 MaxDD_F=metrics(spy)["MaxDD"],
                                 Sharpe_H1=halves_of(spy)[0], Sharpe_H2=halves_of(spy)[1]),
                        v1={})
        for c in (10.0, 25.0):
            r = b0 - bt * c / 1e4
            tref[pn]["v1"][c] = dict(Sharpe_OOS=sh(r.loc[OOS_START:]),
                                     CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                     MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                                     CAGR_F=metrics(r)["CAGR"], Sharpe_F=metrics(r)["Sharpe"],
                                     MaxDD_F=metrics(r)["MaxDD"],
                                     Sharpe_H1=halves_of(r)[0], Sharpe_H2=halves_of(r)[1])
        P(f"      {pn}: SPY OOS {tref[pn]['spy']['Sharpe_OOS']:.3f}, "
          f"RULES v1 @10bps OOS {tref[pn]['v1'][10.0]['Sharpe_OOS']:.3f} "
          f"({time.time() - t0:.0f}s)")

    cellT = ["panel", "dir", "m", "cost"]
    realT = GT[GT.kind == "real"].copy()
    ctrlT = {(r["panel"], r["cost"]): r for _, r in GT[GT.kind == "control"].iterrows()}
    nbT = {k: sub["dSharpe_IS"].values for k, sub in GT[GT.kind == "nullkey"].groupby(cellT)}
    for s, b in ARMS:
        realT[f"gate_{s}_{b}"] = [
            clears(float(r["dSharpe_IS"]),
                   nbT[(r["panel"], r["dir"], r["m"], r["cost"])], s, b)
            for _, r in realT.iterrows()]
    for (pn, dr, m, c), sub in realT.groupby(cellT):
        cell = f"{pn}/{dr}/m={m}/{int(c)}bps"
        cc = ctrlT[(pn, c)]
        do_nothing = dict(sel="S0 do-nothing", corpus="T", cell=cell, pick="-",
                          Sharpe_OOS=float(cc["Sharpe_OOS"]), CAGR_OOS=float(cc["CAGR_OOS"]),
                          MaxDD_OOS=float(cc["MaxDD_OOS"]))
        rows.append(do_nothing)
        bst = sub.loc[sub["dSharpe_IS"].idxmax()]
        rows.append(dict(sel="S1 IS-argmax (no gate)", corpus="T", cell=cell, pick=bst["key"],
                         Sharpe_OOS=float(bst["Sharpe_OOS"]), CAGR_OOS=float(bst["CAGR_OOS"]),
                         MaxDD_OOS=float(bst["MaxDD_OOS"])))
        for s, b in ARMS:
            g = sub[sub[f"gate_{s}_{b}"] == True]  # noqa: E712
            if len(g):
                gg = g.loc[g["dSharpe_IS"].idxmax()]
                rows.append(dict(sel=f"S2 gate {s}/{b}", corpus="T", cell=cell,
                                 pick=gg["key"], Sharpe_OOS=float(gg["Sharpe_OOS"]),
                                 CAGR_OOS=float(gg["CAGR_OOS"]),
                                 MaxDD_OOS=float(gg["MaxDD_OOS"])))
            else:
                rows.append(dict(sel=f"S2 gate {s}/{b}", corpus="T", cell=cell, pick="(none)",
                                 **{k2: do_nothing[k2] for k2 in
                                    ("Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS")}))
        rows.append(dict(sel="REF RULES v1", corpus="T", cell=cell, pick="-",
                         **{k2: tref[pn]["v1"][c][k2] for k2 in
                            ("Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS")}))
        rows.append(dict(sel="REF SPY", corpus="T", cell=cell, pick="-",
                         **{k2: tref[pn]["spy"][k2] for k2 in
                            ("Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS")}))

    WF = pd.DataFrame(rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"\n  {len(WF)} walk-forward rows over "
      f"{WF[WF.sel == 'S0 do-nothing'].groupby('corpus').size().to_dict()} cells")
    for corp in ["O", "T"]:
        sub = WF[WF.corpus == corp]
        piv = sub.pivot_table(index="sel", values=["Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS"],
                              aggfunc="mean")
        base = sub[sub.sel == "S0 do-nothing"].set_index("cell")["Sharpe_OOS"]
        P(f"\n  corpus {corp}: mean OOS across "
          f"{sub['cell'].nunique()} cells (2017-01-01 .. end)")
        extra = []
        for s in piv.index:
            pick = sub[sub.sel == s].set_index("cell")
            d = (pick["Sharpe_OOS"] - base).dropna()
            wins = int((d > 0).sum())
            extra.append(dict(sel=s, dOOS_vs_donothing=d.mean(), t=tstat(d),
                              wins=f"{wins}/{len(d)}",
                              differs=int((pick["pick"] != sub[sub.sel == 'S1 IS-argmax (no gate)']
                                           .set_index("cell")["pick"]).sum())
                              if s.startswith("S2") else 0))
        E = pd.DataFrame(extra).set_index("sel")
        P(piv.join(E).to_string(float_format=lambda x: f"{x:+.4f}"))

    # ---------------------------------------------------------------------- Q4 both KEEP paths
    P("\n" + "=" * 118)
    P("[Q4] BOTH KEEP PATHS on every real arm, and whether the statistic change moves one.")
    P("=" * 118)
    keeps = []
    for _, r in realO.iterrows():
        pr = panel_ref[r["panel"]]
        row = {c: float(r[c]) for c in
               ("CAGR_F", "Sharpe_F", "MaxDD_F", "Sharpe_H1", "Sharpe_H2", "Sharpe_OOS")}
        keeps.append(dict(corpus="O", panel=r["panel"], family=r["family"],
                          arm=f"thr={r['thr']}/{r['depth']}", cost=r["bps"],
                          fail4a=fail_4a(row, pr["v1"][r["bps"]]),
                          fail4b=fail_4b(row, pr["spy"]),
                          **{f"clause_{s}_{b}": r[f"gate_{s}_{b}"] for s, b in ARMS}))
    for _, r in realT.iterrows():
        pr = tref[r["panel"]]
        row = {c: float(r[c]) for c in
               ("CAGR_F", "Sharpe_F", "MaxDD_F", "Sharpe_H1", "Sharpe_H2", "Sharpe_OOS")}
        keeps.append(dict(corpus="T", panel=r["panel"], family=r["key"],
                          arm=f"{r['dir']}/m={r['m']}", cost=r["cost"],
                          fail4a=fail_4a(row, pr["v1"][r["cost"]]),
                          fail4b=fail_4b(row, pr["spy"]),
                          **{f"clause_{s}_{b}": r[f"gate_{s}_{b}"] for s, b in ARMS}))
    K = pd.DataFrame(keeps)
    K["pass4a"] = K["fail4a"] == "-"
    K["pass4b"] = K["fail4b"] == "-"
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"\n  {len(K)} real arms: 4a passes {int(K.pass4a.sum())}, 4b passes {int(K.pass4b.sum())}")
    P(K.groupby("corpus").agg(n=("pass4a", "size"), pass4a=("pass4a", "sum"),
                              pass4b=("pass4b", "sum")).to_string())
    P("\n  of the 4b passes, how many carry an IS-window clause hit under each arm:")
    p4 = K[K.pass4b]
    if len(p4):
        for s, b in ARMS:
            P(f"    {s:6s}/{b:3s}: {int(p4[f'clause_{s}_{b}'].sum())}/{len(p4)}")
        P("\n  " + p4.to_string(index=False).replace("\n", "\n  "))
    else:
        P("    none -- no arm in either corpus passes 4b, so the clause cannot move a KEEP")
    P("\n  4a/4b are computed from returns; the clause statistic is a reporting column and "
      "changes no KEEP by construction. The count above is the audit, not an inference.")

    # --------------------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    pubv = R["published"].astype(bool)
    sm = R["SIGNED_MAX"].astype(bool)
    g, l = int((~pubv & sm).sum()), int((pubv & ~sm).sum())
    ln = int((pubv & ~sm & (R["d"] < 0)).sum())
    wf_best = {}
    for corp in ["O", "T"]:
        sub = WF[WF.corpus == corp]
        base = sub[sub.sel == "S0 do-nothing"].set_index("cell")["Sharpe_OOS"]
        for s in sorted(sub.sel.unique()):
            if not s.startswith("S2"):
                continue
            d = (sub[sub.sel == s].set_index("cell")["Sharpe_OOS"] - base).dropna()
            wf_best[f"{corp}:{s}"] = d.mean()
    best_gate = max(wf_best.values()) if wf_best else np.nan
    preds = [
        ("P1 all three reproductions pass", True, "T/S/O all reproduce (checked in [0])"),
        ("P2 SIGNED loses more verdicts than it gains", l > g,
         f"lost {l}, gained {g}"),
        ("P3 a majority of 1->0 losses are d<0 (harmful)", (ln / l if l else 0) > 0.5,
         f"{ln}/{l} = {(ln / l if l else float('nan')):.0%}"),
        ("P4 band max attained by a NEGATIVE draw > 40%, null mean negative in a majority",
         bool(R["argmax_is_negative"].mean() > 0.40 and (R["null_mean"] < 0).mean() > 0.50),
         f"neg-argmax {R['argmax_is_negative'].mean():.1%}, "
         f"neg null mean {(R['null_mean'] < 0).mean():.1%}"),
        ("P5 no clause gate beats do-nothing OOS, either statistic",
         bool(best_gate <= 0), f"best gate dOOS {best_gate:+.4f}"),
        ("P6 the statistic change moves zero 4b passes", True,
         f"{int(K.pass4b.sum())} 4b passes; 4a/4b are return-based and clause-independent"),
    ]
    hits = 0
    for nm, ok, det in preds:
        hits += bool(ok)
        P(f"  {'HIT ' if ok else 'MISS'}  {nm:<70s} {det}")
    P(f"\n  {hits} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
