#!/usr/bin/env python3
"""IDEA 215  back-fill-the-q95-band-over-every-committed-null-claim   (lane B, 2026-09-08)

QUESTION (queue, idea 215)
    Idea 207 shows the MAX band at K=20 and a Q95 band at K=100 disagree on 26.7% of
    configurations.  Re-read every committed rotation-null claim (ideas 181/186/191/192/201)
    under Q95/K=100 wherever the parent's grid CSV survives, and count how many published
    `clears` verdicts move and in which direction.  The output is the size of the record's
    exposure to the statistic it happened to pick.

WHAT THE COMMITTED RECORD ACTUALLY CONTAINS  (audited before anything was run)
    id   stem                                                per-draw nulls?   corpus
    186  the-null-column-for-instruments-that-are-not-...    YES  grid.csv     108 rows, 20 draws
    191  the-on-share-column                                 YES  grid.csv     180 rows, 20 draws
    192  does-a-harmful-instrument-clear-more-often-...      YES  repro_O.csv  108 rows, 20 draws
    201  the-margin-column-instead-of-two                    NO   summaries    180 rows, 60 draws
    181  does-a-null-column-change-any-published-verdict     n/a               180 rows, 4 draws
    181 is OUT OF SCOPE and this is a structural fact, not a convenience: its null is a KEY
    SUBSTITUTION (`kind == "nullkey"`, 4 substituted ranking keys per real row), not a circular
    rotation.  The null population has exactly 4 members, so "K=100" does not exist for it and
    a 95th percentile of 4 numbers is an interpolation between the 3rd and 4th.  Both facts are
    printed rather than hidden, together with what Q95-at-K=4 would do to its 180 verdicts.
    201 committed only per-config band summaries (band / band_b1 / band_b2 / band_all60), not
    its 10800 null rows, so its verdicts cannot be re-read from its own draws; they are carried
    into the accounting as PUBLISHED values and re-priced against this run's fresh draws.

    186 / 191 / 192's configurations are all SUBSETS of 191's 90 configs x 2 cost rungs:
    186's threshold grid (3 per family) is a strict subset of 191's widened grid (5 per family),
    and 192's corpus O is 186's grid verbatim.  So ONE fresh rotation grid over 191's 180
    configuration-rows re-prices every rotation-null claim in the record at once.

THE DECOMPOSITION THIS RUN REPORTS
    The record's published verdicts already disagree with each other BEFORE any statistic is
    changed.  191 and 201 read the SAME 180 configurations with the SAME statistic (MAX) at the
    SAME K=20 and differ only in rotation seed.  So the exposure splits three ways and each leg
    is measured separately:
      SEED  same stat, same K, different draws           (191 vs 201; and 5 disjoint blocks here)
      STAT  MAX -> Q95 on the SAME draws                 (free, exact, from committed grids)
      DEPTH K = 20 -> 50 -> 100 at a fixed stat          (fresh nested draw set)
      TOTAL published MAX@K=20 -> Q95@K=100
    STAT alone is one-directional by arithmetic: Q95(v) <= MAX(v) for any finite v, so at fixed
    draws a verdict can only move False -> True.  That is a theorem, not a finding; the finding
    is the COUNT, and the counts for SEED and DEPTH, which are not one-directional.

CONSTRUCTION (inherited, not re-invented)
    Panels, base book, overlay families, on-indicator, apply_overlay, fast_backtest and the
    4a/4b evaluators are imported from idea 191's committed script and executed unmodified.
    Rotation null = circular rotation of the ON indicator over the rebalance dates (idea 186).
    Seeds use idea 201's crc32 `det_seed`, NOT the parent's `SEED + hash(...) % 10000`, which is
    process-salted; idea 201 documented that the parent's REAL rows reproduce exactly and its
    BANDS cannot.  Both are checked below.

    TUNED PARAMETER 1: band statistic   {MAX, Q95}      all grid points reported
    TUNED PARAMETER 2: draw depth K     {20, 50, 100}   all grid points reported, nested
    Nothing else is swept.  N_ROT = 100 draws per configuration; K reads the first K of them,
    so the K ladder is a depth ladder on ONE draw set and MAX is monotone in K by construction.

RULE 8 (PROTOCOL clause 8)
    Every selector picks on data <= 2016-12-31 only and is read once on 2017-01-01 onward.
    18 cells = 3 panels x 3 families x 2 cost rungs, pool = 10 points (5 thr x 2 depth).
    ORACLE-OOS is priced beside the selectors as the headroom column.

KEEP PATHS
    4a and 4b are evaluated on every real row (p191.keep_4a vs the panel's own RULES v1 book,
    p191.keep_4b vs SPY), and BOTH PATHS is reported.  This run proposes NO book: the arms are
    idea 186/191's overlays on idea 2's standing candidate, already priced there.  A verdict
    about a BAND is not a trading rule.

KNOWN LIMITS (stated, not worked around)
    * Only J-1 distinct rotations exist and neighbouring offsets are correlated, so 100 draws
      are not 100 independent samples.  The Q95 of a correlated sample has no guaranteed
      nominal size; idea 214 is the open question that would settle it.  This run measures
      REALISED verdict movement, and claims nothing about size.
    * A rotation moves an overlay's episodes but cannot move the sample's crises, so the whole
      family of bands is a weak null.  Widening or narrowing it does not fix that.
    * SMALL439 is current constituents only (survivorship); real and rotated draws inherit the
      bias identically, so the CLAUSE reading is comparative and the LEVEL is not.
    * 201's per-draw nulls are not committed, so its 34 published clears are re-priced against
      this run's draws, not re-read from its own.

Deterministic (crc32 seeds, no reliance on PYTHONHASHSEED), standalone, runnable.
"""
import importlib.util
import os
import sys
import time
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "backtests"
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_back-fill-the-q95-band-over-every-committed-null-claim_B"
S186 = "2026-09-05_the-null-column-for-instruments-that-are-not-keyed-tilts_cloud"
S191 = "2026-09-05_the-on-share-column_cloud"
S192 = "2026-09-05_does-a-harmful-instrument-clear-more-often-than-a-helpful-one_B"
S201 = "2026-09-05_the-margin-column-instead-of-two_cloud"
S181 = "2026-09-05_does-a-null-column-change-any-published-verdict_cloud"

STATS = ["MAX", "Q95"]
# SMOKE=1 shrinks the draw ladder for a wiring check only; the committed run uses the defaults.
K_GRID = [4, 8, 12] if os.environ.get("SMOKE") else [20, 50, 100]
N_ROT = 12 if os.environ.get("SMOKE") else 100
KLO, KHI = K_GRID[0], K_GRID[-1]
BLOCK = KLO
COST_RUNGS = [10, 25]
KEY = ["panel", "family", "thr", "depth", "bps"]

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load_p191():
    spec = importlib.util.spec_from_file_location("p191", OUT / f"{S191}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


p191 = _load_p191()
p191.P = P                                   # route the parent's own prints into this console
FAMILIES, FAM_ORDER = p191.FAMILIES, p191.FAM_ORDER
IS_END, OOS_START, FREQ = p191.IS_END, p191.OOS_START, p191.FREQ


def det_seed(*parts):
    """idea 201's convention: deterministic across processes."""
    return int(zlib.crc32("|".join(str(p) for p in parts).encode())) % (2 ** 31)


def band_of(vals, stat):
    """The clause-11b band from a vector of |d| null draws.  MAX is clause 11b as written;
    Q95 is idea 207's proposed replacement.  Q95 <= MAX for any finite vals."""
    v = np.asarray(vals, float)
    v = v[np.isfinite(v)]
    if not len(v):
        return np.nan
    return float(v.max()) if stat == "MAX" else float(np.quantile(v, 0.95, method="linear"))


def _depth_key(s):
    """depth is written '0.5'/'1.0'/'skip'/'half' in every committed clause CSV."""
    return str(s)


# ================================================================================ committed re-read
def committed_draws():
    """Per-draw |dSharpe| null vectors that SURVIVE in the record, keyed by configuration.
    Returns {parent_id: (per-config draw table, published clause table, colmap)}."""
    out = {}

    g = pd.read_csv(OUT / f"{S186}.grid.csv")
    g["depth"] = g["depth"].map(_depth_key)
    c = pd.read_csv(OUT / f"{S186}.clause.csv")
    c["depth"] = c["depth"].map(_depth_key)
    out[186] = (g[g.draw >= 0], c, dict(band="null_max_abs", clears="clears",
                                        bandDD="null_max_abs_dMaxDD", clearsDD="clears_DD"))

    g = pd.read_csv(OUT / f"{S191}.grid.csv")
    g["depth"] = g["depth"].map(_depth_key)
    g = g[g.kind != "real"] if "kind" in g else g
    g = g[g.offset != 0]
    c = pd.read_csv(OUT / f"{S191}.clause.csv")
    c["depth"] = c["depth"].map(_depth_key)
    out[191] = (g, c, dict(band="band", clears="clears", bandDD="bandDD", clearsDD="clearsDD"))

    g = pd.read_csv(OUT / f"{S192}.repro_O.csv")
    g["depth"] = g["depth"].map(_depth_key)
    a = pd.read_csv(OUT / f"{S192}.arms.csv")
    a = a[a.corpus == "O"].copy()
    out[192] = (g[g.draw >= 0], a, None)                 # 192's key is its `arm` string
    return out


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P(f"IDEA 215  back-fill-the-q95-band-over-every-committed-null-claim   (lane B, 2026-09-08)")
    P("=" * 118)
    P(__doc__.split("QUESTION")[1].split("WHAT THE COMMITTED")[0].strip()[:0] or "")

    # ----------------------------------------------------------------------- reproduction gate
    P("\n" + "=" * 118)
    P("REPRODUCTION, asserted before any new number is read")
    P("=" * 118)
    panels = p191.build_panels()
    P("  panels: " + "  ".join(f"{p.name}={len(p.tradable)}" for p in panels))
    ok = all(p191.checks(pan) for pan in panels)
    pu = load_universe()
    ru = backtest(pu, rules_v1_weights(pu), cost_bps=10.0, freq="W")["returns"].loc[pu.index[260]:]
    mu = metrics(ru)
    drift = mu["Sharpe"] - 0.66418
    hit = abs(drift) < 5e-3
    P(f"  [d] RULES v1 on u56 @10bps: {mu['CAGR']:.5%} / {mu['Sharpe']:.5f} / {mu['MaxDD']:.5%}"
      f"  (idea 191/201 published 6.45305% / 0.66418 / -13.82780% on 2026-09-05)")
    P(f"      PRICE-REVISION DRIFT {drift:+.2e} in Sharpe.  This is NOT a reproduction failure "
      f"and it is not hidden: data/prices.csv last bar is "
      f"{pd.read_csv(ROOT / 'data' / 'prices.csv', index_col=0, parse_dates=True).index[-1].date()}"
      f", the SAME last bar the parents saw, but the file has been rewritten by the daily")
    P(f"      Actions job since (adjusted closes revise on dividends/splits).  The gate is "
      f"therefore |drift| < 5e-3, not the stale constant -> {'PASS' if hit else 'FAIL'}.")
    P(f"      Consequence, stated up front: this run's FRESH real rows cannot match idea 191's")
    P(f"      published real rows to 1e-12.  The gap is sized at [j] and, more usefully, turned")
    P(f"      into a VERDICT count of its own at LEG 2b, so it can be subtracted from LEG 4.")
    P(f"      Idea 216 (2026-09-08) independently priced the same re-commit on an overlapping")
    P(f"      corpus: 104 rows' ON set moved by exactly 1 rebalance date, drift bounded at")
    P(f"      1.25e-02, all 360 of its KEEP verdicts unchanged.")
    ok &= hit

    CD = committed_draws()

    # [e] 186's bands ARE reproducible from its own committed draws (fixed seed, no hash)
    g186, c186, m186 = CD[186]
    rb = (g186.assign(a=g186.dSharpe.abs()).groupby(KEY)["a"].max().rename("band_recomp"))
    j = c186.set_index(KEY).join(rb)
    d = float((j[m186["band"]] - j["band_recomp"]).abs().max())
    P(f"  [e] idea 186 band re-read from its own {len(g186)} committed null rows: "
      f"max|d band| = {d:.3e} over {len(j)} configs -> {'PASS' if d < 1e-12 else 'FAIL'}")
    ok &= d < 1e-12

    # [f] 191's bands likewise (its grid.csv carries the draws even though its SEED was salted)
    g191, c191, m191 = CD[191]
    rb = (g191.assign(a=g191.dSharpe.abs()).groupby(KEY)["a"].max().rename("band_recomp"))
    j91 = c191.set_index(KEY).join(rb)
    d91 = float((j91["band"] - j91["band_recomp"]).abs().max())
    P(f"  [f] idea 191 band re-read from its own {len(g191)} committed null rows: "
      f"max|d band| = {d91:.3e} over {len(j91)} configs -> {'PASS' if d91 < 1e-12 else 'FAIL'}")
    ok &= d91 < 1e-12

    # [g] 192's corpus O is 186's grid verbatim -- check the two agree config for config
    g192, a192, _ = CD[192]
    rb192 = (g192.assign(a=g192.dSharpe.abs()).groupby(KEY)["a"].max().rename("band_192"))
    rb186 = (g186.assign(a=g186.dSharpe.abs()).groupby(KEY)["a"].max().rename("band_186"))
    both = rb186.to_frame().join(rb192, how="inner")
    d192 = float((both.band_186 - both.band_192).abs().max())
    P(f"  [g] idea 192 corpus O vs idea 186 draws (both use the FIXED seed 186_400), "
      f"{len(both)} shared configs: max|d band| = {d192:.3e} -> "
      f"{'PASS' if d192 < 1e-12 else 'FAIL'}")
    ok &= d192 < 1e-12
    rb191o = rb.rename("band_191").to_frame().join(rb192, how="inner")
    P(f"      vs idea 191's draws on the same {len(rb191o)} configs: max|d band| = "
      f"{float((rb191o.band_191 - rb191o.band_192).abs().max()):.3e} -- NOT zero, because 191's "
      f"seed was `SEED + hash(...) % 10000` and Python salts hash() per process.  That is the "
      f"SEED leg below, visible in the reproduction gate itself.")

    # [h] what the record cannot supply
    g181 = pd.read_csv(OUT / f"{S181}.grid.csv")
    n181 = g181[g181.kind == "nullkey"]
    P(f"  [h] idea 181 is a KEY-SUBSTITUTION null, not a rotation: kind values "
      f"{sorted(g181.kind.unique())}, {len(n181)} null rows over "
      f"{int((g181.kind == 'real').sum())} real rows = "
      f"{len(n181) // max(int((g181.kind == 'real').sum()), 1)} draws each.  The null "
      f"population has 4 members; K=100 does not exist for it.  OUT OF SCOPE, reported not run.")
    c201 = pd.read_csv(OUT / f"{S201}.clause.csv")
    c201["depth"] = c201["depth"].map(_depth_key)
    P(f"  [i] idea 201 committed {len(c201)} band SUMMARIES and no per-draw rows "
      f"(files: {', '.join(sorted(p.name.split('.')[-2] for p in OUT.glob(S201 + '.*csv')))}). "
      "Its verdicts are carried as PUBLISHED and re-priced against this run's draws.")

    if not ok:
        P("\nreproduction FAILS -- STOP")
        return
    P("\nreproduction PASSES -- proceeding")

    # ------------------------------------------------------- the record disagrees with itself
    P("\n" + "=" * 118)
    P("LEG 0  SEED EXPOSURE -- the record's published verdicts already disagree BEFORE the")
    P("       statistic is touched.  191 and 201 read the same 180 configurations with the")
    P("       same statistic (MAX) at the same depth (K=20); only the rotation seed differs.")
    P("=" * 118)
    mm = c191.merge(c201, on=KEY, suffixes=("_191", "_201"))
    agree = int((mm.clears_191 == mm.clears_201).sum())
    ft = int((~mm.clears_191 & mm.clears_201).sum())
    tf = int((mm.clears_191 & ~mm.clears_201).sum())
    P(f"\n  191 clears {int(c191.clears.sum())}/180   201 clears {int(c201.clears.sum())}/180"
      f"   agree {agree}/{len(mm)}  ({1 - agree / len(mm):.1%} disagree)")
    P(f"  direction 191 -> 201:  False->True {ft}   True->False {tf}")
    m86 = c186.merge(c191, on=KEY, suffixes=("_186", "_191"))
    ag86 = int((m86.clears_186 == m86.clears_191).sum())
    P(f"  186 (fixed seed) vs 191 (salted seed) on the 108 shared configs: agree {ag86}/108 "
      f"({1 - ag86 / len(m86):.1%} disagree), 186 clears {int(c186.clears.sum())}/108, "
      f"191 clears {int(m86.clears_191.sum())}/108")
    P("\n  READ THIS FIRST: any statistic-change count below must be compared against this")
    P("  floor.  Two honest runs of clause 11b as WRITTEN already move 13.9% of verdicts.")

    # -------------------------------------------------- LEG 1: statistic swap at fixed draws
    P("\n" + "=" * 118)
    P("LEG 1  STATISTIC EXPOSURE -- MAX -> Q95 on the SAME committed draws (K=20, free, exact)")
    P("=" * 118)
    leg1 = []
    for pid, (g, c, cm) in CD.items():
        if pid == 192:
            continue                                  # 192's corpus O == 186's, already counted
        cm = cm or {}
        q = (g.assign(a=g.dSharpe.abs()).groupby(KEY)["a"]
             .apply(lambda s: band_of(s, "Q95")).rename("band_q95"))
        jj = c.set_index(KEY).join(q)
        pub = jj[cm["clears"]].astype(bool)
        new = jj[cm["band"]].notna() & (jj[cm["band"]].index.map(lambda _: True))
        absd = jj["dSharpe"].abs() if "dSharpe" in jj else jj["d"].abs()
        new = absd > jj["band_q95"]
        leg1.append(dict(parent=pid, n=len(jj), pub_clears=int(pub.sum()),
                         q95_clears=int(new.sum()), moved=int((pub != new).sum()),
                         F_to_T=int((~pub & new).sum()), T_to_F=int((pub & new.eq(False)).sum()),
                         mean_band_MAX=float(jj[cm["band"]].mean()),
                         mean_band_Q95=float(jj["band_q95"].mean())))
    L1 = pd.DataFrame(leg1)
    P("\n" + L1.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  T_to_F is 0 by arithmetic (Q95 <= MAX on the same draws), and that is the point:")
    P("  swapping the statistic at fixed depth can only ADD clears.  The number that matters")
    P("  is how many, and whether depth cancels it.")

    # ------------------------------------------------------------------ LEG 2: the fresh grid
    P("\n" + "=" * 118)
    P(f"LEG 2  FRESH ROTATION GRID -- 3 panels x 3 families x 5 thr x 2 depth x "
      f"(1 real + {N_ROT} rotations) x 2 cost")
    P(f"       K reads the FIRST K of the {N_ROT} draws, so the K ladder is nested on one set.")
    P("=" * 118)
    rows, draws = [], []
    for pan in panels:
        start = pan.start
        spy = pan.spy.loc[start:]
        basefull = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=0.0, freq="W")
        b0, bt = basefull["returns"].loc[start:], basefull["turnover"].loc[start:]
        c0 = pan._r0
        for fam in FAM_ORDER:
            _, thrs, _, depths = FAMILIES[fam]
            for thr in thrs:
                s_real = p191.on_indicator(pan, fam, thr)
                J = len(s_real)
                offs = p191.rotations(J, N_ROT, det_seed(pan.name, fam, thr))
                for depth in depths:
                    variants = ([("real", 0, -1, s_real)]
                                + [("null", o, i, np.roll(s_real, o)) for i, o in enumerate(offs)])
                    for kind, off, di, s in variants:
                        W, mask = p191.apply_overlay(pan, fam, depth, s)
                        res = p191.fast_backtest(pan.px, W, 0.0, FREQ, mask=mask)
                        for bps in COST_RUNGS:
                            r = p191.net(res, bps).loc[start:]
                            cr = p191.net(c0, bps).loc[start:]
                            m = metrics(r)
                            mc = metrics(cr)
                            rec = dict(panel=pan.name, family=fam, thr=thr, depth=str(depth),
                                       bps=bps, draw=di,
                                       dSharpe=m["Sharpe"] - mc["Sharpe"],
                                       dSharpe_IS=(p191._sh(r.loc[:IS_END])
                                                   - p191._sh(cr.loc[:IS_END])),
                                       dMaxDD=m["MaxDD"] - mc["MaxDD"])
                            if kind == "null":
                                draws.append(rec)
                                continue
                            br = b0 - bt * bps / 1e4
                            h1, h2 = p191.halves(r)
                            rec.update(on_share=float(s.mean()),
                                       switches=p191.circ_switches(s),
                                       CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                       H1=h1, H2=h2,
                                       Sharpe_IS=p191._sh(r.loc[:IS_END]),
                                       Sharpe_OOS=p191._sh(r.loc[OOS_START:]),
                                       CAGR_OOS=metrics(r.loc[OOS_START:])["CAGR"],
                                       MaxDD_OOS=metrics(r.loc[OOS_START:])["MaxDD"],
                                       ctrl_Sharpe=mc["Sharpe"], ctrl_MaxDD=mc["MaxDD"],
                                       ctrl_Sharpe_OOS=p191._sh(cr.loc[OOS_START:]),
                                       ctrl_CAGR_OOS=metrics(cr.loc[OOS_START:])["CAGR"],
                                       ctrl_MaxDD_OOS=metrics(cr.loc[OOS_START:])["MaxDD"],
                                       fail4a=p191.keep_4a(r, br), fail4b=p191.keep_4b(r, spy))
                            rows.append(rec)
        P(f"  {pan.name} done ({time.time() - t0:.0f}s)")

    R = pd.DataFrame(rows)
    D = pd.DataFrame(draws)
    R["pass4a"] = R.fail4a == "-"
    R["pass4b"] = R.fail4b == "-"
    R.to_csv(OUT / f"{STEM}.real.csv", index=False)
    D.to_csv(OUT / f"{STEM}.draws.csv", index=False)
    P(f"\n  real rows {len(R)}, null rows {len(D)}  ({time.time() - t0:.0f}s)")

    # real rows must reproduce idea 191's published real rows exactly (deterministic part)
    mg = R.merge(c191, on=KEY, suffixes=("", "_p"))
    dd = {c: float((mg[c] - mg[c + "_p"]).abs().max())
          for c in ["dSharpe", "dSharpe_IS", "Sharpe", "Sharpe_OOS", "CAGR", "MaxDD"]}
    P(f"  [j] fresh real rows vs {S191}.clause.csv ({len(mg)}/180 matched), PRICE-REVISION GAP: "
      + "  ".join(f"{k} {v:.1e}" for k, v in dd.items()))
    P(f"      The construction is identical and deterministic, so this gap is entirely the "
      f"revised price file (see [d]).  It is REPORTED, not gated at a threshold picked to "
      f"pass: the number that matters is how many published VERDICTS the revision alone moves, "
      f"and that is measured as its own leg immediately below.  Sanity stop only: "
      f"max|d Sharpe| < 5e-2 -> {'PASS' if dd['Sharpe'] < 5e-2 else 'FAIL'}.")

    # ------------------------------------------------------------------- LEG 2b: the PRICE leg
    P("\n  LEG 2b  PRICE EXPOSURE, isolated: idea 191's OWN committed 20-draw MAX bands, read")
    P("          against THIS run's fresh real |dSharpe|.  Statistic, depth and draws are all")
    P("          held at the published values, so every move here is the price revision alone.")
    pub191 = c191.set_index(KEY)["clears"].astype(bool)
    band191 = (g191.assign(a=g191.dSharpe.abs()).groupby(KEY)["a"].max())
    fresh_absd = R.set_index(KEY)["dSharpe"].abs().reindex(pub191.index)
    price_new = (fresh_absd > band191.reindex(pub191.index))
    price_moved = int((pub191 != price_new).sum())
    price_ft = int((~pub191 & price_new).sum())
    price_tf = int((pub191 & ~price_new).sum())
    P(f"          {price_moved}/{len(pub191)} published verdicts move on the price revision "
      f"alone ({price_moved / len(pub191):.1%}): {price_ft} False->True, {price_tf} True->False."
      f"  clears {int(pub191.sum())} -> {int(price_new.sum())}.")
    P(f"          This is the irreducible floor under every count in LEG 4, which uses fresh")
    P(f"          real rows.  LEG 1 uses the parents' own real rows and carries none of it.")

    # ------------------------------------------------------------- bands over the (stat, K) grid
    P("\n" + "=" * 118)
    P("LEG 3  THE (stat, K) GRID -- every point reported.  `clears` = |dSharpe| > band.")
    P("=" * 118)
    Dk = D.sort_values("draw")
    grp = Dk.groupby(KEY)
    absd = R.set_index(KEY)["dSharpe"].abs()
    absdd = R.set_index(KEY)["dMaxDD"].abs()
    absis = R.set_index(KEY)["dSharpe_IS"].abs()
    bands, verd = {}, {}
    for stat in STATS:
        for K in K_GRID:
            sub = Dk[Dk.draw < K]
            b = (sub.groupby(KEY)["dSharpe"].apply(lambda s: band_of(s.abs(), stat))
                 .reindex(absd.index))
            bdd = (sub.groupby(KEY)["dMaxDD"].apply(lambda s: band_of(s.abs(), stat))
                   .reindex(absdd.index))
            bis = (sub.groupby(KEY)["dSharpe_IS"].apply(lambda s: band_of(s.abs(), stat))
                   .reindex(absis.index))
            bands[(stat, K)] = (b, bdd, bis)
            verd[(stat, K)] = (absd > b, absdd > bdd, absis > bis)
    grid = []
    for (stat, K), (b, bdd, bis) in bands.items():
        cl, cdd, cis = verd[(stat, K)]
        grid.append(dict(stat=stat, K=K,
                         nominal_size=(1 / (K + 1)) if stat == "MAX" else 0.05,
                         mean_band=float(b.mean()), median_band=float(b.median()),
                         mean_margin=float((absd - b).mean()),
                         clears=int(cl.sum()), clear_rate=float(cl.mean()),
                         clearsDD=int(cdd.sum()), clears_IS=int(cis.sum())))
    G = pd.DataFrame(grid).sort_values(["stat", "K"])
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P("\n" + G.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    mx = G[G.stat == "MAX"].set_index("K")
    q9 = G[G.stat == "Q95"].set_index("K")
    P(f"\n  MAX band K={KLO} -> {KHI}: {mx.loc[KLO, 'mean_band']:.4f} -> {mx.loc[KHI, 'mean_band']:.4f}"
      f"  ({mx.loc[KHI, 'mean_band'] / mx.loc[KLO, 'mean_band'] - 1:+.1%}),"
      f"  clear rate {mx.loc[KLO, 'clear_rate']:.1%} -> {mx.loc[KHI, 'clear_rate']:.1%}")
    P(f"  Q95 band K={KLO} -> {KHI}: {q9.loc[KLO, 'mean_band']:.4f} -> {q9.loc[KHI, 'mean_band']:.4f}"
      f"  ({q9.loc[KHI, 'mean_band'] / q9.loc[KLO, 'mean_band'] - 1:+.1%}),"
      f"  clear rate {q9.loc[KLO, 'clear_rate']:.1%} -> {q9.loc[KHI, 'clear_rate']:.1%}")

    # seed exposure measured inside this run: 5 disjoint blocks of 20 under MAX
    blk = {}
    for bi in range(N_ROT // BLOCK):
        s = Dk[(Dk.draw >= bi * BLOCK) & (Dk.draw < (bi + 1) * BLOCK)]
        bb = (s.groupby(KEY)["dSharpe"].apply(lambda v: band_of(v.abs(), "MAX"))
              .reindex(absd.index))
        blk[bi] = (absd > bb)
    B = pd.DataFrame(blk)
    anyflip = int((B.nunique(axis=1) > 1).sum())
    P(f"\n  SEED leg, measured here: {N_ROT // BLOCK} DISJOINT blocks of {BLOCK} draws, MAX band. Verdict")
    P(f"  differs across at least two blocks on {anyflip}/{len(B)} configurations "
      f"({anyflip / len(B):.1%}); block clear counts {[int(B[c].sum()) for c in B]}.")
    P(f"  That brackets the 191-vs-201 disagreement of {len(mm) - agree}/180 "
      f"({1 - agree / len(mm):.1%}) measured on the published record.")

    # ------------------------------------------------------- LEG 4: published verdicts moving
    P("\n" + "=" * 118)
    P("LEG 4  THE ANSWER -- how many PUBLISHED `clears` verdicts move, and in which direction")
    P("=" * 118)
    pubs = {186: (c186, "clears"), 191: (c191, "clears"), 201: (c201, "clears")}
    g192b = (g192.assign(a=g192.dSharpe.abs()).groupby(KEY)["a"].max())
    a192i = a192.copy()
    moves = []
    for (stat, K) in [("MAX", KLO), ("MAX", KHI), ("Q95", KLO), ("Q95", KHI)]:
        cl = verd[(stat, K)][0]
        for pid, (c, col) in pubs.items():
            jj = c.set_index(KEY)
            new = cl.reindex(jj.index)
            pub = jj[col].astype(bool)
            keep = new.notna()
            pub, new = pub[keep], new[keep].astype(bool)
            moves.append(dict(stat=stat, K=K, parent=pid, n=len(pub),
                              published_clears=int(pub.sum()), new_clears=int(new.sum()),
                              moved=int((pub != new).sum()),
                              F_to_T=int((~pub & new).sum()), T_to_F=int((pub & ~new).sum()),
                              moved_pct=float((pub != new).mean())))
    M = pd.DataFrame(moves)
    M.to_csv(OUT / f"{STEM}.moves.csv", index=False)
    P("\n" + M.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    hdl = M[(M.stat == "Q95") & (M.K == KHI)]
    P(f"\n  HEADLINE, published MAX@K={KLO} -> Q95@K={KHI}:")
    for _, r in hdl.iterrows():
        P(f"    idea {int(r.parent)}: {int(r.moved)}/{int(r.n)} verdicts move "
          f"({r.moved_pct:.1%}), {int(r.F_to_T)} False->True, {int(r.T_to_F)} True->False; "
          f"clears {int(r.published_clears)} -> {int(r.new_clears)}")
    tot = hdl[["n", "moved", "F_to_T", "T_to_F"]].sum()
    P(f"    POOLED (186+191+201, {int(tot.n)} published verdicts): {int(tot.moved)} move "
      f"({tot.moved / tot.n:.1%}), {int(tot.F_to_T)} F->T, {int(tot.T_to_F)} T->F")
    P(f"    idea 192 corpus O is idea 186's grid verbatim (band agreement above), so its "
      f"{int(a192i.clears.sum())}/108 published clears move with idea 186's row.")
    P(f"    idea 181: 180 published verdicts, key-substitution null, 4 draws -- OUT OF SCOPE.")
    n181draws = len(n181) // max(int((g181.kind == "real").sum()), 1)
    P(f"      For the record: Q95 of {n181draws} numbers interpolates between the 3rd and 4th, "
      f"so at its own depth Q95 is NOT the max and the swap is defined but meaningless.")

    # ------------------------------------------------------------------------- LEG 5: rule 8
    P("\n" + "=" * 118)
    P("RULE 8  Selectors pick on data <= 2016-12-31 ONLY and are read once on 2017-01-01 ->.")
    P("        18 cells = 3 panels x 3 families x 2 cost.  Pool = 10 points (5 thr x 2 depth).")
    P("        The clause-gated arms differ ONLY in which band gates them.")
    P("=" * 118)
    RI = R.set_index(KEY)
    for (stat, K) in [("MAX", KLO), ("Q95", KHI), ("Q95", KLO), ("MAX", KHI)]:
        RI[f"clears_IS_{stat}{K}"] = verd[(stat, K)][2].reindex(RI.index)
    RR = RI.reset_index()
    wf = []
    for (pn, fm, bp), sub in RR.groupby(["panel", "family", "bps"]):
        base = dict(OOS_Sharpe=float(sub.ctrl_Sharpe_OOS.iloc[0]),
                    OOS_CAGR=float(sub.ctrl_CAGR_OOS.iloc[0]),
                    OOS_MaxDD=float(sub.ctrl_MaxDD_OOS.iloc[0]))

        def take(df, tag, col="dSharpe_IS"):
            if not len(df) or not np.isfinite(df[col]).any():
                return dict(selector=tag, pick="ABSTAIN", **base)
            r = df.loc[df[col].idxmax()]
            return dict(selector=tag, pick=f"{r['thr']}/{r['depth']}",
                        OOS_Sharpe=float(r.Sharpe_OOS), OOS_CAGR=float(r.CAGR_OOS),
                        OOS_MaxDD=float(r.MaxDD_OOS))

        o = sub.loc[sub.Sharpe_OOS.idxmax()]
        arms = [dict(selector="S0 do-nothing", pick="-", **base),
                take(sub, "S1 IS-argmax, ungated")]
        for (stat, K) in [("MAX", KLO), ("Q95", KLO), ("MAX", KHI), ("Q95", KHI)]:
            arms.append(take(sub[sub[f"clears_IS_{stat}{K}"].fillna(False)],
                             f"S-gated {stat}@K={K}"))
        arms.append(dict(selector="ORACLE-OOS", pick=f"{o['thr']}/{o['depth']}",
                         OOS_Sharpe=float(o.Sharpe_OOS), OOS_CAGR=float(o.CAGR_OOS),
                         OOS_MaxDD=float(o.MaxDD_OOS)))
        for a in arms:
            a.update(panel=pn, family=fm, bps=bp, dOOS=a["OOS_Sharpe"] - base["OOS_Sharpe"])
            wf.append(a)
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    piv = W.pivot_table(index=["panel", "family", "bps"], columns="selector", values="OOS_Sharpe")
    out = []
    for s in piv.columns:
        d = (piv[s] - piv["S0 do-nothing"]).dropna()
        sw = W[W.selector == s]
        out.append(dict(selector=s, mean_OOS_Sharpe=float(piv[s].mean()),
                        mean_OOS_CAGR=float(sw.OOS_CAGR.mean()),
                        mean_OOS_MaxDD=float(sw.OOS_MaxDD.mean()),
                        dOOS=float(d.mean()), t=p191.tstat(d), wins=int((d > 0).sum()),
                        losses=int((d < 0).sum()), n=int(len(d)),
                        abstains=int((sw["pick"] == "ABSTAIN").sum())))
    SW = pd.DataFrame(out).sort_values("mean_OOS_Sharpe", ascending=False)
    P("\n" + SW.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    a20 = W[W.selector == f"S-gated MAX@K={KLO}"].set_index(["panel", "family", "bps"])
    b100 = W[W.selector == f"S-gated Q95@K={KHI}"].set_index(["panel", "family", "bps"])
    chg = int((a20["pick"] != b100.reindex(a20.index)["pick"]).sum())
    dd_ = float((b100.reindex(a20.index)["OOS_Sharpe"] - a20["OOS_Sharpe"]).mean())
    P(f"\n  THE DECISION TEST: swapping the gate MAX@{KLO} -> Q95@{KHI} changes {chg}/18 rule-8 picks"
      f", mean dOOS_Sharpe {dd_:+.4f}")

    P("\n  BENCHMARKS over the same OOS window (2017-01-01 ->):")
    bm = []
    for pan in panels:
        st = pan.start
        spy_o = pan.spy.loc[st:].loc[OOS_START:]
        bl = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10, freq="W")["returns"]
        bl = bl.loc[st:].loc[OOS_START:]
        for nm, r in [("SPY", spy_o), ("RULES v1 @10bps", bl)]:
            m = metrics(r)
            bm.append(dict(panel=pan.name, series=nm, OOS_CAGR=m["CAGR"],
                           OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
    BM = pd.DataFrame(bm)
    P(BM.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  FULL SAMPLE and HALVES for the same 18 cells' do-nothing book vs SPY and RULES v1:")
    fh = []
    for pan in panels:
        st = pan.start
        r0 = p191.net(pan._r0, 10).loc[st:]
        spy = pan.spy.loc[st:]
        bl = backtest(pan.px, rules_v1_weights(pan.px), cost_bps=10, freq="W")["returns"].loc[st:]
        for nm, r in [("base book @10bps", r0), ("SPY", spy), ("RULES v1 @10bps", bl)]:
            m = metrics(r)
            h1, h2 = p191.halves(r)
            fh.append(dict(panel=pan.name, series=nm, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                           MaxDD=m["MaxDD"], H1=h1, H2=h2))
    FH = pd.DataFrame(fh)
    P(FH.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    FH.to_csv(OUT / f"{STEM}.benchmarks.csv", index=False)

    # --------------------------------------------------------------------------- KEEP paths
    P("\n" + "=" * 118)
    P("KEEP PATHS -- 4a and 4b on every real row (180).  This run proposes NO book.")
    P("=" * 118)
    P(f"\n  4a passes: {int(R.pass4a.sum())}/{len(R)}   4b passes: {int(R.pass4b.sum())}/{len(R)}"
      f"   BOTH PATHS: {int((R.pass4a & R.pass4b).sum())}/{len(R)}")
    P("\n  4b failing bars:")
    P(R.fail4b.value_counts().to_string())
    if int(R.pass4b.sum()):
        P("\n  the 4b passes:")
        P(R[R.pass4b][KEY + ["on_share", "CAGR", "Sharpe", "MaxDD", "Sharpe_OOS", "CAGR_OOS",
                             "MaxDD_OOS", "pass4a"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    R[KEY + ["pass4a", "pass4b", "fail4a", "fail4b", "CAGR", "Sharpe", "MaxDD",
             "Sharpe_OOS", "CAGR_OOS", "MaxDD_OOS"]].to_csv(OUT / f"{STEM}.keeppaths.csv",
                                                            index=False)
    P("\n  NOTE: every 4b pass here is an overlay on idea 2's standing candidate, already priced")
    P("  by ideas 186/191/201.  Nothing new is promoted and RULES.md is untouched.")

    # ------------------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS (written before the fresh grid ran; LEG 0/1 are re-reads")
    P("of committed files and were known)")
    P("=" * 118)
    q95_100 = float(hdl.moved_pct.mean())
    seed_floor = 1 - agree / len(mm)
    preds = [
        ("P1 T->F is 0 in LEG 1 (Q95 <= MAX at fixed draws) -- arithmetic, not evidence",
         int(L1.T_to_F.sum()) == 0, f"{int(L1.T_to_F.sum())} T->F over {int(L1.n.sum())} rows"),
        ("P2 the MAX band rises with K and the Q95 band does not (|dQ95| < 5%)",
         mx.loc[KHI, "mean_band"] > mx.loc[KLO, "mean_band"]
         and abs(q9.loc[KHI, "mean_band"] / q9.loc[KLO, "mean_band"] - 1) < 0.05,
         f"MAX {mx.loc[KHI, 'mean_band'] / mx.loc[KLO, 'mean_band'] - 1:+.1%}, "
         f"Q95 {q9.loc[KHI, 'mean_band'] / q9.loc[KLO, 'mean_band'] - 1:+.1%}"),
        ("P3 published->Q95@100 movement exceeds the seed floor measured on the record",
         q95_100 > seed_floor, f"{q95_100:.1%} vs seed floor {seed_floor:.1%}"),
        ("P4 the price revision alone moves fewer verdicts than the seed leg does",
         price_moved / len(pub191) < seed_floor,
         f"price {price_moved}/180 = {price_moved / len(pub191):.1%} vs seed "
         f"{len(mm) - agree}/180 = {seed_floor:.1%}"),
        ("P5 no clause-gated selector beats do-nothing out of sample",
         float(SW[SW.selector.str.startswith("S-gated")].dOOS.max()) <= 0,
         f"best gated dOOS {float(SW[SW.selector.str.startswith('S-gated')].dOOS.max()):+.4f}"),
        ("P6 swapping the gate changes at most a third of the 18 rule-8 picks",
         chg <= 6, f"{chg}/18 picks changed"),
    ]
    for tag, h, det in preds:
        P(f"  {'HIT ' if h else 'MISS'}  {tag:<74s}  {det}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")

    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
