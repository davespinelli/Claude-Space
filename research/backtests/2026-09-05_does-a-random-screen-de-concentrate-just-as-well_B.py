#!/usr/bin/env python3
"""IDEA 198  does-a-random-screen-de-concentrate-just-as-well   (lane B, 2026-09-05)

THE QUESTION
------------
Idea 178 published the IS-window 4b SCREEN as a selector worth +0.0287 paired OOS Sharpe
(t +1.92, 3W/0L/8T over 11 cells) and diagnosed its mechanism as DE-CONCENTRATION: every one
of its changed arm-cells moved the pick to a LARGER book and OOS |MaxDD| fell in 14 of 14.
Idea 199 then showed a bare pre-registered floor `n >= 25` on the same IS-Sharpe argmax
returns +0.1297 (t +12.43, 11W/0L/0T) -- 453% of the screen's edge, with no bars, no
coefficients and no window split.

Both of those compare the screen against DOING NOTHING.  Neither compares it against the
right null.  A screen does two things at once: it RESTRICTS THE ARGMAX POOL (from N books to
s), and it restricts it TO A PARTICULAR SUBSET.  Idea 151 found a random selector inside the
band of every real one.  So the missing arm, and the queue's ask verbatim:

    a screen that admits a RANDOM SUBSET OF THE SAME SIZE the 4b screen admits in each cell,
    200 draws, and report where the real screen's +0.0287 sits in that null.
    If it is inside, the screen is a book-size prior wearing a 4b label.

  Q1  REPRODUCTION.  Rebuild idea 178's 1003-row corpus through its OWN committed code and
      check it against BOTH committed copies (idea 178's and idea 199's), then reproduce the
      published +0.0287 screen edge and +0.1297 floor edge before any new number is read.
  Q2  THE NULL THE QUEUE ASKS FOR.  Per cell, draw 200 random subsets of the screen's own
      admitted SIZE, take the IS-Sharpe argmax inside each, and locate the real screen's
      paired dOOS in that distribution -- pooled and cell by cell.
  Q3  THE SAME NULL FOR THE FLOOR.  Idea 199's floors are restrictions too.  Run each
      `n >= k` against a null matched to ITS OWN admitted size.  This is the discriminating
      test: if the screen is inside its null and the floor is outside its null, then
      restriction per se buys nothing and DE-CONCENTRATION is the whole effect.
  Q4  MECHANISM.  (a) a pure pool-size ladder -- random subsets at fixed sizes in every cell,
      to price restriction per se; (b) within the 200 draws, does a draw's mean PICKED n
      predict its dOOS?  If yes, every instrument's position in its null is just how much
      book size it happens to buy.
  Q5  RULE 8 / KEEP.  Every number here IS the walk-forward read (pick on <= 2016-12-31,
      read 2017-2026 once).  OOS CAGR/Sharpe/MaxDD for the real instruments, the null mean
      and the null's 95th percentile, against RULES v1 and SPY, with 4a and 4b on every book.

DESIGN
------
Idea 199's script is IMPORTED (it in turn imports idea 178's), so the panels, book
constructions, eligibility masks, 4b bar machinery and window splits all execute their own
committed code.  Nothing is re-typed.  The base pass is idea 199's `run_cell` verbatim.

  cells    : 11 = C159 x {u56, broad, small} x {10, 25} bps  (6)
                + C168 x {u56, broad}        x {10, 25} bps  (4)
                + C165 x u56                 x 10 bps        (1)
  books    : 98 / 88 / 63 per cell = 1003 book-rows at the published static gross 0.75
  draws    : 200 per cell per matched size, seeded (the queue's own number)

  TUNED PARAMETER 1: the screen's coefficient convention, AS165 (phi 0.60, delta 0.70) or
                     PUB (phi 0.70, delta 0.60) -- idea 178's audit found three committed
                     call sites with the arguments swapped, so both readings are carried.
  TUNED PARAMETER 2: the size floor k in {10, 15, 20, 25} for the Q3 arm (idea 199's grid).
  ALL grid points reported.  Nothing else is fitted; the null needs no parameters.

THE NULL, STATED EXACTLY (pre-registered)
-----------------------------------------
For cell c the real instrument admits s_c of the N_c books.  One draw of the null picks a
uniform random s_c-subset of the same N_c books, takes the IS-Sharpe argmax inside it, and
scores it against S0 (the full-pool IS-Sharpe argmax) exactly as the real instrument is
scored.  When s_c = 0 the real instrument FALLS BACK to S0 and scores 0; the null does the
same, so the structurally-empty cells are ties on both sides and the comparison is like for
like.  When s_c = N_c both are S0 by construction.  The pooled statistic is the mean paired
dOOS over the 11 cells, which is exactly the statistic idea 178 published as +0.0287.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  The corpus reproduces against both committed copies at < 1e-10, and the published
      +0.0287 (screen AS165) and +0.1297 (n>=25) edges reproduce to 4 decimals.
  P2  The screen's +0.0287 sits INSIDE its own size-matched null (two-sided, 5th-95th
      percentile) -- i.e. the queue's "if it is inside" branch fires.
  P3  The best size floor sits ABOVE its own size-matched null (> 95th percentile), because
      it selects big books specifically rather than s books at random.
  P4  Within the null draws, a draw's mean picked n is positively rank-correlated with its
      dOOS in the pooled statistic (rho > 0).
  P5  The pure pool-size ladder is not flat at zero: restricting the argmax pool at random
      has a NON-ZERO mean effect, because S0 is itself an IS-fitted pick and the pools'
      mean OOS Sharpe need not equal it (idea 204's pool-sign point, tested here directly).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; the small panel has no
    delistings and its LEVELS are biased upward.  Every arm reads the same biased panel, so
    the COMPARISON is unaffected; no level here is a tradable estimate.
  * The screen fires in only 4 of 11 cells (admitted sizes 35, 23, 3, 2 under AS165); the
    other 7 are structurally empty.  The null therefore has 4 live cells, and its power is
    correspondingly small.  This is a property of the screen, not a choice made here, and it
    is reported rather than smoothed over.
  * 11 cells sharing three panels and two corpora is a small, correlated sample.  Every
    paired difference is reported with its t and its win/loss/tie count and is called an
    estimate, because that is what it is.
  * Idea 38: calendar-day index after 2014-09-17 on u56/broad.  Idea 126: t+1 only.
  * This run proposes NO new book.  Every book is idea 159/165/168's, already priced; what is
    on trial is the SELECTION RULE and the null it should be judged against.

Deterministic (seed 198), standalone.  Writes .console.txt, .corpus.csv, .null.csv,
.percell.csv, .ladder.csv, .walkforward.csv.

The 1003-backtest base pass is cached PER CELL under `<STEM>.cellcache/` so an interrupted run
resumes where it stopped; every cell -- cached or freshly computed -- is read back from that
cache file, so the corpus is byte-identical whether the script runs once or in pieces, and the
directory is deleted on a clean finish.  Delete it by hand to force a full rebuild.
"""
import importlib.util
import json
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import metrics  # noqa: E402,F401

STEM = "2026-09-05_does-a-random-screen-de-concentrate-just-as-well_B"
OUT = ROOT / "research" / "backtests"
P178_STEM = "2026-09-05_is-the-IS-4b-screen-a-one-cell-accident_C"
P199_STEM = "2026-09-05_the-screen-is-a-book-size-rule_cloud"

DRAWS = 200
SEED = 198
SIZE_FLOORS = [10, 15, 20, 25]
COEFS = ["AS165", "PUB"]
LADDER = [1, 2, 3, 5, 8, 12, 20, 35, 50, 75]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 90)
pd.set_option("display.max_rows", 1400)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I199 = _load(OUT / f"{P199_STEM}.py", "i199")
CELLS = I199.CELLS
CELLKEY = ["corpus", "panel", "cost"]


CACHE = OUT / f"{STEM}.cellcache"


def run_cell(job):
    """idea 199's base pass, verbatim, cached per cell so an interrupted run resumes.

    Wrapped also so the child process can unpickle it.  The result is ALWAYS read back from the
    cache file, so a resumed run and a single-shot run produce the identical corpus.
    """
    cp, pk, ct = job
    CACHE.mkdir(exist_ok=True)
    fg, fb = CACHE / f"{cp}_{pk}_{int(ct)}.csv", CACHE / f"{cp}_{pk}_{int(ct)}.bench.json"
    if not (fg.exists() and fb.exists()):
        g, b = I199.run_cell(job)
        g.to_csv(fg, index=False)
        fb.write_text(json.dumps(b))
    return pd.read_csv(fg), json.loads(fb.read_text())


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x))))


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    if len(a) < 3:
        return np.nan
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def pct_of(x, null):
    """Share of null draws strictly below x, in percent (the one-sided position of x)."""
    null = np.asarray(null, float)
    return float(100.0 * (null < x).mean())


# ============================================================================================
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 198  does-a-random-screen-de-concentrate-just-as-well   (lane B, 2026-09-05)")
    P("=" * 118)
    P(f"\n{len(CELLS)} cells, idea 199's base pass imported verbatim; {DRAWS} draws/cell, "
      f"seed {SEED}.\n")

    with ProcessPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(run_cell, CELLS))
    G = pd.concat([g for g, _ in res], ignore_index=True)
    B = pd.DataFrame([b for _, b in res])
    G.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    P(f"corpus: {len(G)} book-rows in {time.time() - t0:.0f}s -> {STEM}.corpus.csv")

    # ------------------------------------------------------------------- Q1 REPRODUCTION
    P("\n" + "=" * 118)
    P("Q1  REPRODUCTION -- asserted before any new number is read")
    P("=" * 118)
    key = CELLKEY + ["arm", "share"]
    num = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]
    repro_ok = True
    for tag, stem in [("idea 178", P178_STEM), ("idea 199", P199_STEM)]:
        PC = pd.read_csv(OUT / f"{stem}.corpus.csv")
        PC["arm"] = PC["arm"].astype(str)
        mg = G.assign(arm=G["arm"].astype(str)).merge(PC, on=key, suffixes=("", "_p"))
        worst = max(float((mg[c] - mg[c + "_p"]).abs().max()) for c in num)
        nmis = int((mg["n"] != mg["n_p"]).sum())
        ok = worst < 1e-10 and nmis == 0 and len(mg) == len(PC) == len(G)
        repro_ok &= ok
        P(f"  [a] {tag}'s corpus.csv: {len(mg)}/{len(PC)} rows matched, worst numeric diff "
          f"{worst:.3e}, n mismatches {nmis} -> {'PASS' if ok else 'FAIL'}")

    def argmax_pick(sub, mask=None):
        d = sub if mask is None else sub[mask]
        if not len(d):
            return None
        r = d.loc[d["IS_Sharpe"].idxmax()]
        return (str(r["arm"]), float(r["share"]))

    # cell tables in a fixed order, plus S0 and the instruments' admitted sets
    cells, S0 = [], {}
    for ck, sub in G.groupby(CELLKEY, sort=True):
        sub = sub.reset_index(drop=True)
        st = argmax_pick(sub)
        srow = sub[(sub.arm.astype(str) == st[0]) & (sub.share == st[1])].iloc[0]
        S0[ck] = srow
        cells.append((ck, sub))
    P(f"  [b] {len(cells)} cells rebuilt; S0 (full-pool IS-Sharpe argmax) mean OOS Sharpe "
      f"{np.mean([S0[c]['OOS_Sharpe'] for c, _ in cells]):+.4f}")

    def score(pick, ck):
        """paired OOS numbers for a pick against this cell's S0."""
        _, sub = next(x for x in cells if x[0] == ck)
        r = sub[(sub.arm.astype(str) == pick[0]) & (sub.share == pick[1])].iloc[0]
        s = S0[ck]
        return dict(n=int(r["n"]), OOS_Sharpe=r["OOS_Sharpe"], OOS_CAGR=r["OOS_CAGR"],
                    OOS_MaxDD=r["OOS_MaxDD"], OOS4b=bool(r["OOS4b_clears"]),
                    pass4a=bool(r["pass4a"]), pass4b=bool(r["pass4b"]),
                    dOOS=float(r["OOS_Sharpe"] - s["OOS_Sharpe"]),
                    dMaxDD=float(abs(r["OOS_MaxDD"]) - abs(s["OOS_MaxDD"])),
                    changed=(pick != (str(s["arm"]), float(s["share"]))))

    # the real instruments and their admitted masks
    INSTR = {}
    for cf in COEFS:
        INSTR[f"SCREEN 4bIS [{cf}]"] = lambda sub, cf=cf: sub[f"screen_{cf}"].values
    for k in SIZE_FLOORS:
        INSTR[f"SIZE n>={k}"] = lambda sub, k=k: (sub["n"] >= k).values

    real = {}
    for tag, mfn in INSTR.items():
        rows = []
        for ck, sub in cells:
            m = mfn(sub)
            pick = argmax_pick(sub, m) or (str(S0[ck]["arm"]), float(S0[ck]["share"]))
            d = dict(zip(CELLKEY, ck), selector=tag, s=int(m.sum()), N=len(sub),
                     pick=f"{pick[0]}@{pick[1]}", **score(pick, ck))
            rows.append(d)
        real[tag] = pd.DataFrame(rows)
    R = pd.concat(real.values(), ignore_index=True)

    scr = float(real["SCREEN 4bIS [AS165]"]["dOOS"].mean())
    flr = float(real["SIZE n>=25"]["dOOS"].mean())
    P(f"  [c] screen [AS165] paired edge = {scr:+.4f}  (idea 178 published +0.0287)")
    P(f"  [d] SIZE n>=25 paired edge     = {flr:+.4f}  (idea 199 published +0.1297)")
    edges_ok = abs(scr - 0.0287) < 5e-5 and abs(flr - 0.1297) < 5e-5
    repro_ok &= edges_ok
    P(f"\n  reproduction {'PASSES' if repro_ok else 'IS INCOMPLETE'} -- proceeding")

    # ------------------------------------------------------------------- the null
    P("\n" + "=" * 118)
    P("Q2/Q3  THE SIZE-MATCHED NULL -- 200 random subsets of each instrument's own admitted")
    P("       size, per cell, IS-Sharpe argmax inside each")
    P("=" * 118)
    rng = np.random.default_rng(SEED)

    # cache: for a given cell and subset size s, DRAWS draws -> arrays of dOOS / dMaxDD / n
    cache = {}

    def draw_null(ck, sub, s):
        kk = (ck, int(s))
        if kk in cache:
            return cache[kk]
        N = len(sub)
        isS = sub["IS_Sharpe"].values
        oos = sub["OOS_Sharpe"].values
        dd = np.abs(sub["OOS_MaxDD"].values)
        nn = sub["n"].values
        s0 = S0[ck]
        base_o, base_d = float(s0["OOS_Sharpe"]), abs(float(s0["OOS_MaxDD"]))
        s0i = int(np.argmax(isS))
        if s <= 0 or s >= N:                       # fallback / whole pool: both are S0
            idx = np.full(DRAWS, s0i)
        else:
            idx = np.empty(DRAWS, int)
            for d in range(DRAWS):
                pick = rng.choice(N, size=int(s), replace=False)
                idx[d] = pick[np.argmax(isS[pick])]
        out = dict(dOOS=oos[idx] - base_o, dMaxDD=dd[idx] - base_d, n=nn[idx].astype(float),
                   OOS_Sharpe=oos[idx], degenerate=(s <= 0 or s >= N))
        cache[kk] = out
        return out

    null_rows, percell_rows = [], []
    for tag in INSTR:
        rr = real[tag].set_index(CELLKEY)
        mats = {k: [] for k in ("dOOS", "dMaxDD", "n", "OOS_Sharpe")}
        for ck, sub in cells:
            s = int(rr.loc[ck, "s"])
            nd = draw_null(ck, sub, s)
            for k in mats:
                mats[k].append(nd[k])
            x = float(rr.loc[ck, "dOOS"])
            percell_rows.append(dict(zip(CELLKEY, ck), selector=tag, s=s, N=len(sub),
                                     real_dOOS=x, real_n=int(rr.loc[ck, "n"]),
                                     null_mean=float(nd["dOOS"].mean()),
                                     null_sd=float(nd["dOOS"].std(ddof=1)),
                                     null_p5=float(np.percentile(nd["dOOS"], 5)),
                                     null_p95=float(np.percentile(nd["dOOS"], 95)),
                                     null_mean_n=float(nd["n"].mean()),
                                     pct=pct_of(x, nd["dOOS"]),
                                     degenerate=bool(nd["degenerate"])))
        # pooled statistic: mean over the 11 cells, one value per draw
        pooled = {k: np.vstack(v).mean(axis=0) for k, v in mats.items()}
        x = float(real[tag]["dOOS"].mean())
        xm = float(real[tag]["dMaxDD"].mean())
        xn = float(real[tag]["n"].mean())
        nd = pooled["dOOS"]
        sd = float(nd.std(ddof=1))
        null_rows.append(dict(
            selector=tag, real_dOOS=x, real_dMaxDD=xm, real_mean_n=xn,
            cells_live=int((real[tag]["s"] > 0).sum()),
            mean_s=float(real[tag]["s"].mean()),
            null_mean=float(nd.mean()), null_sd=sd,
            null_p5=float(np.percentile(nd, 5)), null_p50=float(np.percentile(nd, 50)),
            null_p95=float(np.percentile(nd, 95)),
            pct=pct_of(x, nd), z=(x - float(nd.mean())) / sd if sd > 0 else np.nan,
            inside_90=bool(np.percentile(nd, 5) <= x <= np.percentile(nd, 95)),
            null_mean_dMaxDD=float(pooled["dMaxDD"].mean()),
            null_mean_n=float(pooled["n"].mean()),
            rho_n_dOOS=spearman(pooled["n"], pooled["dOOS"])))
    NL = pd.DataFrame(null_rows)
    PCd = pd.DataFrame(percell_rows)
    NL.to_csv(OUT / f"{STEM}.null.csv", index=False)
    PCd.to_csv(OUT / f"{STEM}.percell.csv", index=False)

    P("\n  POOLED (statistic = mean paired dOOS over the 11 cells, the same statistic idea")
    P("  178 published as +0.0287).  pct = % of the 200 null draws below the real value.")
    P(NL[["selector", "cells_live", "mean_s", "real_dOOS", "null_mean", "null_sd",
          "null_p5", "null_p50", "null_p95", "pct", "z", "inside_90"]]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  the same null on DE-CONCENTRATION itself (mean picked n) and on drawdown:")
    P(NL[["selector", "real_mean_n", "null_mean_n", "real_dMaxDD", "null_mean_dMaxDD",
          "rho_n_dOOS"]].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    P("\n  PER CELL (degenerate = the instrument admits 0 or all books, so real and null are")
    P("  both S0 by construction and the cell is a structural tie):")
    P(PCd[PCd.selector.isin(["SCREEN 4bIS [AS165]", "SIZE n>=25"])]
      .to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    scr_row = NL[NL.selector == "SCREEN 4bIS [AS165]"].iloc[0]
    flr_row = NL[NL.selector == "SIZE n>=25"].iloc[0]
    P(f"\n  Q2 ANSWER: the screen's {scr_row['real_dOOS']:+.4f} sits at the "
      f"{scr_row['pct']:.1f}th percentile of its own size-matched null "
      f"(mean {scr_row['null_mean']:+.4f}, sd {scr_row['null_sd']:.4f}, "
      f"z {scr_row['z']:+.2f}) -- "
      f"{'INSIDE' if scr_row['inside_90'] else 'OUTSIDE'} the 5-95 band.")
    P(f"  Q3 ANSWER: SIZE n>=25's {flr_row['real_dOOS']:+.4f} sits at the "
      f"{flr_row['pct']:.1f}th percentile of ITS size-matched null "
      f"(mean {flr_row['null_mean']:+.4f}, sd {flr_row['null_sd']:.4f}, "
      f"z {flr_row['z']:+.2f}) -- "
      f"{'INSIDE' if flr_row['inside_90'] else 'OUTSIDE'} the 5-95 band.")

    # ------------------------------------------------------------------- Q4 mechanism
    P("\n" + "=" * 118)
    P("Q4  MECHANISM")
    P("=" * 118)
    P("\n  (a) restriction per se: random subsets at a FIXED size in every cell (no matching).")
    P("      If the ladder is flat at 0, shrinking the argmax pool buys nothing by itself.")
    lad = []
    for s in LADDER:
        mats = {k: [] for k in ("dOOS", "dMaxDD", "n")}
        live = 0
        for ck, sub in cells:
            ss = min(s, len(sub))
            live += int(0 < s < len(sub))
            nd = draw_null(ck, sub, ss if ss < len(sub) else len(sub))
            for k in mats:
                mats[k].append(nd[k])
        pooled = {k: np.vstack(v).mean(axis=0) for k, v in mats.items()}
        lad.append(dict(subset_size=s, cells_nondegenerate=live,
                        mean_dOOS=float(pooled["dOOS"].mean()),
                        sd_dOOS=float(pooled["dOOS"].std(ddof=1)),
                        p5=float(np.percentile(pooled["dOOS"], 5)),
                        p95=float(np.percentile(pooled["dOOS"], 95)),
                        mean_picked_n=float(pooled["n"].mean()),
                        mean_dMaxDD=float(pooled["dMaxDD"].mean())))
    LD = pd.DataFrame(lad)
    LD.to_csv(OUT / f"{STEM}.ladder.csv", index=False)
    P("\n" + LD.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\n      rho(subset size, mean dOOS) over the ladder = "
      f"{spearman(LD.subset_size, LD.mean_dOOS):+.3f};  "
      f"rho(subset size, mean picked n) = {spearman(LD.subset_size, LD.mean_picked_n):+.3f}")

    P("\n  (b) inside the null: does a DRAW's mean picked n predict that draw's dOOS?")
    mech = []
    for tag in INSTR:
        rr = real[tag].set_index(CELLKEY)
        mats = {k: [] for k in ("dOOS", "n")}
        for ck, sub in cells:
            nd = draw_null(ck, sub, int(rr.loc[ck, "s"]))
            for k in mats:
                mats[k].append(nd[k])
        pooled = {k: np.vstack(v).mean(axis=0) for k, v in mats.items()}
        mech.append(dict(selector=tag, rho_draw_n_vs_dOOS=spearman(pooled["n"], pooled["dOOS"]),
                         real_mean_n=float(real[tag]["n"].mean()),
                         null_mean_n=float(pooled["n"].mean()),
                         n_pct=pct_of(float(real[tag]["n"].mean()), pooled["n"])))
    MC = pd.DataFrame(mech)
    P("\n" + MC.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\n      n_pct = where the instrument's own mean picked book size sits in the null's")
    P("      distribution of mean picked size.  An instrument that de-concentrates MORE than")
    P("      a random subset of its size will show n_pct near 100.")

    # per-book within-cell reference: is n itself the ordering?
    q4c = []
    for ck, sub in cells:
        q4c.append(dict(zip(CELLKEY, ck), books=len(sub),
                        rho_n_OOSSharpe=spearman(sub.n, sub.OOS_Sharpe),
                        rho_n_ISSharpe=spearman(sub.n, sub.IS_Sharpe),
                        rho_n_OOSabsDD=spearman(sub.n, sub.OOS_MaxDD.abs())))
    Q4C = pd.DataFrame(q4c)
    P("\n  (c) within-cell rank correlation of book size n with the outcomes (idea 199's Q4,")
    P("      recomputed here as the reference the null is read against):")
    P(Q4C.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P(f"      means: rho(n, OOS Sharpe) {Q4C.rho_n_OOSSharpe.mean():+.3f} "
      f"(t {tstat(Q4C.rho_n_OOSSharpe):+.2f}), rho(n, IS Sharpe) "
      f"{Q4C.rho_n_ISSharpe.mean():+.3f}, rho(n, OOS |MaxDD|) "
      f"{Q4C.rho_n_OOSabsDD.mean():+.3f}")

    # ------------------------------------------------------------------- Q5 rule 8 / KEEP
    P("\n" + "=" * 118)
    P("Q5  RULE 8 -- every row above IS the walk-forward read (parameters and picks chosen on")
    P("    <= 2016-12-31, 2017-2026 read once).  Against RULES v1 and SPY on the same window.")
    P("=" * 118)
    bench = B.set_index(CELLKEY)
    wf_rows = []
    s0df = pd.DataFrame([dict(zip(CELLKEY, ck), **score((str(S0[ck]["arm"]),
                                                         float(S0[ck]["share"])), ck))
                         for ck, _ in cells])
    wf_rows.append(dict(selector="S0 do-nothing (IS-Sharpe argmax)",
                        OOS_CAGR=float(s0df.OOS_CAGR.mean()),
                        OOS_Sharpe=float(s0df.OOS_Sharpe.mean()),
                        OOS_MaxDD=float(s0df.OOS_MaxDD.mean()), dOOS=0.0,
                        mean_n=float(s0df.n.mean()), OOS4b=int(s0df.OOS4b.sum()),
                        pass4a=int(s0df.pass4a.sum()), pass4b=int(s0df.pass4b.sum())))
    for tag in INSTR:
        d = real[tag]
        wf_rows.append(dict(selector=tag, OOS_CAGR=float(d.OOS_CAGR.mean()),
                            OOS_Sharpe=float(d.OOS_Sharpe.mean()),
                            OOS_MaxDD=float(d.OOS_MaxDD.mean()),
                            dOOS=float(d.dOOS.mean()), mean_n=float(d.n.mean()),
                            OOS4b=int(d.OOS4b.sum()), pass4a=int(d.pass4a.sum()),
                            pass4b=int(d.pass4b.sum())))
    # the null as a tradable arm: its mean and its 95th-percentile draw
    for tag in ["SCREEN 4bIS [AS165]", "SIZE n>=25"]:
        rr = real[tag].set_index(CELLKEY)
        mats = {k: [] for k in ("dOOS", "OOS_Sharpe")}
        for ck, sub in cells:
            nd = draw_null(ck, sub, int(rr.loc[ck, "s"]))
            for k in mats:
                mats[k].append(nd[k])
        pooled = {k: np.vstack(v).mean(axis=0) for k, v in mats.items()}
        wf_rows.append(dict(selector=f"NULL matched to {tag} (mean draw)",
                            OOS_CAGR=np.nan,
                            OOS_Sharpe=float(pooled["OOS_Sharpe"].mean()),
                            OOS_MaxDD=np.nan, dOOS=float(pooled["dOOS"].mean()),
                            mean_n=np.nan, OOS4b=-1, pass4a=-1, pass4b=-1))
    wf_rows.append(dict(selector="RULES v1 @ each cell's cost", OOS_CAGR=float(bench.v1_OOS_CAGR.mean()),
                        OOS_Sharpe=float(bench.v1_OOS_Sharpe.mean()),
                        OOS_MaxDD=float(bench.v1_OOS_MaxDD.mean()), dOOS=np.nan,
                        mean_n=np.nan, OOS4b=-1, pass4a=-1, pass4b=-1))
    wf_rows.append(dict(selector="SPY buy-and-hold", OOS_CAGR=float(bench.spy_OOS_CAGR.mean()),
                        OOS_Sharpe=float(bench.spy_OOS_Sharpe.mean()),
                        OOS_MaxDD=float(bench.spy_OOS_MaxDD.mean()), dOOS=np.nan,
                        mean_n=np.nan, OOS4b=-1, pass4a=-1, pass4b=-1))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P("\n  (OOS4b/pass4a/pass4b are counts over the 11 picked books; -1 = not a single book)")
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  per-cell benchmarks (the means above average across three panels, so they are")
    P("  descriptive only):")
    P(bench.reset_index()[CELLKEY + ["v1_OOS_Sharpe", "v1_OOS_CAGR", "v1_OOS_MaxDD",
                                     "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"\n  BOTH KEEP PATHS, pool-wide: {int(G.pass4a.sum())}/{len(G)} books pass 4a, "
      f"{int(G.pass4b.sum())}/{len(G)} pass 4b, "
      f"{int(G.OOS4b_clears.sum())}/{len(G)} clear the OOS window.")
    P("  No arm in this run is a KEEP candidate: the run prices a NULL for an existing")
    P("  selector and proposes no new book and no new rule.")

    R.to_csv(OUT / f"{STEM}.instruments.csv", index=False)

    # ---------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    best_floor = NL[NL.selector.str.startswith("SIZE")].sort_values("real_dOOS",
                                                                    ascending=False).iloc[0]
    preds = [
        ("P1 corpus + published edges reproduce", bool(repro_ok),
         f"screen {scr:+.4f} vs +0.0287, floor {flr:+.4f} vs +0.1297"),
        ("P2 the screen sits INSIDE its size-matched null", bool(scr_row["inside_90"]),
         f"{scr_row['pct']:.1f}th pct, z {scr_row['z']:+.2f}"),
        ("P3 the best size floor sits ABOVE its own null", bool(best_floor["pct"] > 95),
         f"{best_floor['selector']} at {best_floor['pct']:.1f}th pct, "
         f"z {best_floor['z']:+.2f}"),
        ("P4 within the null, a draw's mean picked n predicts its dOOS",
         bool(MC.rho_draw_n_vs_dOOS.mean() > 0),
         f"mean rho {MC.rho_draw_n_vs_dOOS.mean():+.3f} over {len(MC)} instruments"),
        ("P5 the pure pool-size ladder is not flat at zero",
         bool(LD.mean_dOOS.abs().max() > 0.01),
         f"largest |mean dOOS| on the ladder {LD.mean_dOOS.abs().max():.4f}"),
    ]
    for tag, hit, detail in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {tag:<58s}  {detail}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
    shutil.rmtree(CACHE, ignore_errors=True)     # clean finish -> the resume cache is scratch


if __name__ == "__main__":
    main()
