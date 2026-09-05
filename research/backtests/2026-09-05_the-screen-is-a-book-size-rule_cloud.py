#!/usr/bin/env python3
"""IDEA 199  the-screen-is-a-book-size-rule   (cloud, 2026-09-05)

THE QUESTION
------------
Idea 178 found that the IS-window 4b SCREEN is not a Sharpe selector but a DE-CONCENTRATION
instrument: every one of its 14 changed arm-cells moved the pick to a LARGER book
(n 4->6, 4->20, 14->25, 9->18, 9->25), OOS |MaxDD| fell in 14 of 14, and the screen never
fired at 25 bps at all.  Its paired edge over the do-nothing control was +0.0287 OOS Sharpe
(t +1.92, 3W/0L/8T over 11 cells) -- an estimate, not a result.

If the screen's whole mechanism is "pick a bigger book", then a PRE-REGISTERED MINIMUM BOOK
SIZE gets the same thing for free: no null, no SPY bars, no coefficients, no window split.
PROTOCOL would then say `n >= k` and drop the screen.

  Q1  REPRODUCTION.  Rebuild idea 178's 11 cells from its own imported code and reproduce its
      committed corpus.csv row by row, its W_STATIC picks and its W_4bIS[STATIC][*] picks.
  Q2  THE SUBSTITUTE.  Apply a bare size floor n >= k (k in {10, 15, 20, 25}) to the same
      IS-Sharpe argmax.  How much of the screen's +0.0287 does it capture, and at what k?
  Q3  DOES IT FIRE WHERE THE SCREEN CANNOT?  The screen is empty at 25 bps and on the whole
      small panel.  A size floor has no such boundary.  Is that a feature or a cost?
  Q4  IS SIZE THE WHOLE STORY?  Within each cell, how much of the OOS Sharpe ordering does n
      alone explain, and does the screen's pick beat the size floor's pick conditional on n?
  Q5  RULE 8 / KEEP.  Every number here IS a walk-forward read (pick on <= 2016-12-31, read
      2017-2026 once).  Report OOS CAGR/Sharpe/MaxDD for every selector against RULES v1 and
      SPY on the same window, and evaluate both KEEP paths on every picked book.

DESIGN
------
Idea 178's script is IMPORTED, not re-implemented, so its panels, book constructions (C159's
key ranking, C165's, C168's exponent family), eligibility masks, 4b bar machinery and window
splits all execute their own committed code.

  cells    : 11 = C159 x {u56, broad, small} x {10, 25} bps  (6)
                + C168 x {u56, broad}        x {10, 25} bps  (4)
                + C165 x u56                 x 10 bps        (1)
  books    : 98 / 88 / 63 per cell = 1003 book-rows, each run ONCE at the published gross 0.75
  TUNED PARAMETER 1: the size floor k in {10, 15, 20, 25}   (the queue's own grid)
  TUNED PARAMETER 2: the screen's coefficient convention, AS165 (phi 0.60, delta 0.70) or
                     PUB (phi 0.70, delta 0.60) -- idea 178's audit found three committed call
                     sites with the arguments swapped, so both readings are carried.
  ALL grid points reported.

  SCOPE LIMIT, stated up front: this run prices the STATIC gross convention only (g = 0.75 for
  every book).  Idea 178's CF_IS ladder is NOT re-run -- it found [STATIC] and [CFIS] differ in
  exactly ONE arm-cell of 22, so the comparison is unaffected; the committed CFIS picks are
  carried alongside for reference and are not recomputed.  This is why the run costs ~1000
  backtests instead of idea 178's ~10000.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  idea 178's corpus.csv reproduces row by row at < 1e-10, and its W_STATIC and
      W_4bIS[STATIC][AS165] picks reproduce in 11/11 cells.
  P2  The best size floor captures at least half of the screen's +0.0287 paired edge.
  P3  A size floor changes the pick in MORE cells than the screen does (the screen abstains in
      7 of 11; a floor cannot abstain unless the whole pool is below it).
  P4  The size floor's changed picks also reduce OOS |MaxDD| (the screen's own mechanism).
  P5  Neither instrument beats the do-nothing control at t >= 2 over 11 cells; both are
      estimates.  (Ten consecutive project instances of an IS-fitted selector failing to earn
      its complexity.)

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): all three panels are CURRENT constituents; the small panel
    contains no delistings and its LEVELS are biased upward.  Every selector reads the same
    biased panel, so the COMPARISON is unaffected; no level here is a tradable estimate.
  * 11 cells sharing three panels and two corpora is a small, correlated sample.  Every
    paired difference below is reported with its t and its win/loss/tie count and is called an
    estimate, because that is what it is.
  * `n` is the book's name count, itself derived from the share m x mean eligible names, so a
    floor on n is a floor on m up to the panel's breadth.  Both are reported.
  * Idea 38: calendar-day index after 2014-09-17 on u56/broad.  Idea 126: t+1 only.

Deterministic, standalone.  Writes .console.txt, .corpus.csv, .picks.csv, .walkforward.csv.
"""
import importlib.util
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_the-screen-is-a-book-size-rule_cloud"
OUT = ROOT / "research" / "backtests"
P178_STEM = "2026-09-05_is-the-IS-4b-screen-a-one-cell-accident_C"

SIZE_FLOORS = [10, 15, 20, 25]
COEFS = {"AS165": (0.60, 0.70), "PUB": (0.70, 0.60)}
GROSS = 0.75

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 1200)

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


I178 = _load(OUT / f"{P178_STEM}.py", "i178")
C, H = I178.C, I178.H
FREQ, IS_END, OOS_START = I178.FREQ, I178.IS_END, I178.OOS_START
SCREEN_BARS = I178.SCREEN_BARS

CELLS = ([("C159", pk, c) for pk in I178.P159 for c in I178.COSTS]
         + [("C168", pk, c) for pk in I178.P168 for c in I178.COSTS]
         + [("C165", "u56", 10.0)])


# ---------------------------------------------------------------- one cell, base pass only
def run_cell(job):
    corpus, pk, cost = job
    t0 = time.time()
    R = I178.panel_ref(pk)
    arms_axis, shares = {"C159": (I178.K159, I178.S159),
                         "C168": (I178.K168, I178.S168),
                         "C165": (I178.K165, I178.S165)}[corpus]
    nmap = I178.nmap_for(pk, shares)
    books = [(a, m) for a in arms_axis for m in shares]

    v1 = backtest(R["px"], rules_v1_weights(R["px"]), cost_bps=cost,
                  freq=FREQ)["returns"].loc[R["start"]:]
    v1o = metrics(v1.loc[OOS_START:])
    spyo = metrics(R["spy"].loc[OOS_START:])

    rows = []
    for a, m in books:
        n = nmap[m]
        r = I178.run_at(pk, corpus, a, m, n, cost, GROSS)
        mm, mo, mi = metrics(r), metrics(r.loc[OOS_START:]), metrics(H.window(r, "IS"))
        h1, h2 = H.halves(r)
        f_full, _ = I178.fails_at(r, R["bars_full"], 0.70, 0.60, "full",
                                  keys=("H1", "H2", "OOS", "DD", "CAGR"))
        d = dict(corpus=corpus, panel=pk, cost=cost, arm=str(a), share=m, n=n, g=GROSS,
                 CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                 IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                 OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                 pass4a=H.pass4a(r, v1), pass4b=(len(f_full) == 0),
                 failing="|".join(f_full))
        # the IS-window 4b screen, both coefficient conventions, idea 165's four bars
        for cf, (phi, delta) in COEFS.items():
            fails, _ = I178.fails_at(r, R["bars_IS"], phi, delta, "IS", keys=SCREEN_BARS)
            d[f"screen_{cf}"] = (len(fails) == 0)
        # OOS-window 4b of this book, PUB coefficients, the "did it work" read
        fo, _ = I178.fails_at(r, R["bars_OOS"], 0.70, 0.60, "OOS",
                              keys=("H1", "H2", "OOS", "DD", "CAGR"))
        d["OOS4b_clears"] = (len(fo) == 0)
        d["OOS4b_fail"] = "|".join(fo) if fo else "(none)"
        rows.append(d)

    G = pd.DataFrame(rows)
    bench = dict(corpus=corpus, panel=pk, cost=cost,
                 v1_OOS_Sharpe=v1o["Sharpe"], v1_OOS_CAGR=v1o["CAGR"],
                 v1_OOS_MaxDD=v1o["MaxDD"], spy_OOS_Sharpe=spyo["Sharpe"],
                 spy_OOS_CAGR=spyo["CAGR"], spy_OOS_MaxDD=spyo["MaxDD"],
                 n_books=len(books), secs=time.time() - t0)
    return G, bench


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


# ============================================================================================ run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 199  the-screen-is-a-book-size-rule   (cloud, 2026-09-05)")
    P("=" * 118)
    P(f"\n{len(CELLS)} cells, base pass at g={GROSS} only (STATIC convention).  Idea 178's")
    P("script is imported; nothing is re-typed.\n")

    with ProcessPoolExecutor(max_workers=3) as ex:
        res = list(ex.map(run_cell, CELLS))
    Gs = [g for g, _ in res]
    B = pd.DataFrame([b for _, b in res])
    G = pd.concat(Gs, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.corpus.csv", index=False)
    P(f"corpus: {len(G)} book-rows in {time.time() - t0:.0f}s -> {STEM}.corpus.csv")

    # ------------------------------------------------------------------- Q1 REPRODUCTION
    P("\n" + "=" * 118)
    P("Q1  REPRODUCTION -- asserted before any new number is read")
    P("=" * 118)
    PC = pd.read_csv(OUT / f"{P178_STEM}.corpus.csv")
    key = ["corpus", "panel", "cost", "arm", "share"]
    PC["arm"] = PC["arm"].astype(str)
    mg = G.merge(PC, on=key, suffixes=("", "_p"))
    P(f"\n  [a] idea 178's corpus.csv, row by row ({len(mg)}/{len(PC)} matched):")
    worst = 0.0
    for c in ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
              "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]:
        d = float((mg[c] - mg[c + "_p"]).abs().max())
        worst = max(worst, d)
        P(f"        max|d {c:<11s}| = {d:.3e}")
    nmis = int((mg["n"] != mg["n_p"]).sum())
    P(f"        n mismatches: {nmis}/{len(mg)};  worst numeric diff {worst:.3e} -> "
      f"{'PASS' if worst < 1e-10 and nmis == 0 and len(mg) == len(PC) else 'FAIL'}")
    repro_a = worst < 1e-10 and nmis == 0 and len(mg) == len(PC)

    PW = pd.read_csv(OUT / f"{P178_STEM}.walkforward.csv")
    PW["pick"] = PW["pick"].astype(str)

    def argmax_pick(sub, mask=None):
        d = sub if mask is None else sub[mask]
        if not len(d):
            return None
        r = d.loc[d["IS_Sharpe"].idxmax()]
        return (str(r["arm"]), float(r["share"]))

    rep_rows = []
    for (cp, pk, ct), sub in G.groupby(["corpus", "panel", "cost"]):
        static = argmax_pick(sub)
        row = dict(corpus=cp, panel=pk, cost=ct, mine_STATIC=f"{static[0]}@{static[1]}")
        ref = PW[(PW.corpus == cp) & (PW.panel == pk) & (PW.cost == ct)]
        rs = ref[ref.arm == "W_STATIC"].iloc[0]
        row["ref_STATIC"] = f"{rs['pick']}@{rs['share']}"
        row["STATIC_ok"] = (static[0] == str(rs["pick"])
                            and abs(static[1] - float(rs["share"])) < 1e-12)
        for cf in COEFS:
            mine = argmax_pick(sub, sub[f"screen_{cf}"]) or static
            rr = ref[ref.arm == f"W_4bIS[STATIC][{cf}]"].iloc[0]
            row[f"mine_{cf}"] = f"{mine[0]}@{mine[1]}"
            row[f"ref_{cf}"] = f"{rr['pick']}@{rr['share']}"
            row[f"{cf}_ok"] = (mine[0] == str(rr["pick"])
                               and abs(mine[1] - float(rr["share"])) < 1e-12)
            row[f"elig_{cf}"] = int(sub[f"screen_{cf}"].sum())
            row[f"ref_elig_{cf}"] = int(rr["screen_elig"])
        rep_rows.append(row)
    RP = pd.DataFrame(rep_rows)
    P(f"\n  [b] W_STATIC pick reproduced in {int(RP.STATIC_ok.sum())}/{len(RP)} cells")
    for cf in COEFS:
        P(f"  [c] W_4bIS[STATIC][{cf}] pick reproduced in "
          f"{int(RP[cf + '_ok'].sum())}/{len(RP)} cells; screen-eligible counts match in "
          f"{int((RP['elig_' + cf] == RP['ref_elig_' + cf]).sum())}/{len(RP)}")
    P("\n" + RP.to_string(index=False))
    repro = repro_a and bool(RP.STATIC_ok.all()) and bool(RP["AS165_ok"].all())
    P(f"\n  reproduction {'PASSES' if repro else 'IS INCOMPLETE'} -- "
      f"{'proceeding' if repro else 'reporting what did and did not reproduce, then proceeding'}")

    # ------------------------------------------------------------------- selectors
    P("\n" + "=" * 118)
    P("Q2  THE SUBSTITUTE -- a bare size floor n >= k against the screen, same IS-Sharpe argmax")
    P("=" * 118)
    picks = []
    for (cp, pk, ct), sub in G.groupby(["corpus", "panel", "cost"]):
        bench = B[(B.corpus == cp) & (B.panel == pk) & (B.cost == ct)].iloc[0]
        static = argmax_pick(sub)
        srow = sub[(sub.arm == static[0]) & (sub.share == static[1])].iloc[0]

        def emit(tag, pick, fired, pool):
            r = sub[(sub.arm == pick[0]) & (sub.share == pick[1])].iloc[0]
            picks.append(dict(
                corpus=cp, panel=pk, cost=ct, selector=tag,
                pick=f"{pick[0]}@{pick[1]}", n=int(r["n"]), share=float(r["share"]),
                fired=fired, pool=pool, changed=(pick != static),
                OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                OOS4b_clears=bool(r["OOS4b_clears"]), OOS4b_fail=r["OOS4b_fail"],
                pass4a=bool(r["pass4a"]), pass4b=bool(r["pass4b"]),
                dOOS=r["OOS_Sharpe"] - srow["OOS_Sharpe"],
                dMaxDD=abs(r["OOS_MaxDD"]) - abs(srow["OOS_MaxDD"]),
                v1_OOS_Sharpe=bench["v1_OOS_Sharpe"], spy_OOS_Sharpe=bench["spy_OOS_Sharpe"],
                v1_OOS_CAGR=bench["v1_OOS_CAGR"], spy_OOS_CAGR=bench["spy_OOS_CAGR"],
                v1_OOS_MaxDD=bench["v1_OOS_MaxDD"], spy_OOS_MaxDD=bench["spy_OOS_MaxDD"]))

        emit("S0 do-nothing (IS-Sharpe argmax)", static, False, len(sub))
        for cf in COEFS:
            m = sub[f"screen_{cf}"]
            pick = argmax_pick(sub, m) or static
            emit(f"SCREEN 4bIS [{cf}]", pick, bool(m.any()), int(m.sum()))
        for k in SIZE_FLOORS:
            m = sub["n"] >= k
            pick = argmax_pick(sub, m) or static
            emit(f"SIZE n>={k}", pick, bool(m.any()), int(m.sum()))
        # ceilings / references
        o = sub.loc[sub["OOS_Sharpe"].idxmax()]
        emit("ORACLE-OOS (ceiling)", (str(o["arm"]), float(o["share"])), False, len(sub))
        b = sub.loc[sub["n"].idxmax()]
        emit("BIGGEST BOOK (no fitting)", (str(b["arm"]), float(b["share"])), False, len(sub))
    K = pd.DataFrame(picks)
    K.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    K.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    order = (["S0 do-nothing (IS-Sharpe argmax)"]
             + [f"SCREEN 4bIS [{c}]" for c in COEFS]
             + [f"SIZE n>={k}" for k in SIZE_FLOORS]
             + ["BIGGEST BOOK (no fitting)", "ORACLE-OOS (ceiling)"])
    s0 = K[K.selector == order[0]].set_index(["corpus", "panel", "cost"])
    summ = []
    for tag in order:
        s = K[K.selector == tag].set_index(["corpus", "panel", "cost"])
        d = (s["OOS_Sharpe"] - s0["OOS_Sharpe"]).dropna()
        dd = (s["OOS_MaxDD"].abs() - s0["OOS_MaxDD"].abs()).dropna()
        summ.append(dict(selector=tag, mean_OOS_Sharpe=float(s["OOS_Sharpe"].mean()),
                         mean_OOS_CAGR=float(s["OOS_CAGR"].mean()),
                         mean_OOS_MaxDD=float(s["OOS_MaxDD"].mean()),
                         dOOS=float(d.mean()), t=tstat(d),
                         W=int((d > 1e-12).sum()), L=int((d < -1e-12).sum()),
                         T=int((d.abs() <= 1e-12).sum()),
                         changed=int(s["changed"].sum()), fired=int(s["fired"].sum()),
                         mean_n=float(s["n"].mean()), dMaxDD=float(dd.mean()),
                         OOS4b=int(s["OOS4b_clears"].sum()),
                         pass4a=int(s["pass4a"].sum()), pass4b=int(s["pass4b"].sum())))
    S = pd.DataFrame(summ)
    P("\n  ALL selectors over all 11 cells (dOOS / dMaxDD are paired vs S0; W/L/T on OOS")
    P("  Sharpe; changed = picks differing from S0; OOS4b = picks clearing the OOS window):")
    P(S.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    scr = float(S.loc[S.selector == "SCREEN 4bIS [AS165]", "dOOS"].iloc[0])
    best_size = S[S.selector.str.startswith("SIZE")].sort_values("dOOS", ascending=False)
    bs = best_size.iloc[0]
    P(f"\n  screen [AS165] paired edge (idea 178 published +0.0287 over these 11 cells): "
      f"{scr:+.4f}")
    P(f"  best size floor: {bs['selector']} at {bs['dOOS']:+.4f} = "
      f"{(bs['dOOS'] / scr) if scr else float('nan'):.0%} of the screen's edge")
    P("\n  the whole size ladder, in order:")
    P(best_size[["selector", "dOOS", "t", "W", "L", "T", "changed", "mean_n",
                 "dMaxDD", "OOS4b"]].to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    # ------------------------------------------------------------------- Q3
    P("\n" + "=" * 118)
    P("Q3  WHERE EACH INSTRUMENT FIRES -- by cost rung and panel")
    P("=" * 118)
    for tag in order[1:-2]:
        s = K[K.selector == tag]
        by_cost = s.groupby("cost").agg(cells=("fired", "size"), fired=("fired", "sum"),
                                        changed=("changed", "sum"))
        P(f"\n  {tag}")
        P("    " + by_cost.to_string().replace("\n", "\n    "))
        sp = s.groupby("panel").agg(cells=("fired", "size"), fired=("fired", "sum"),
                                    changed=("changed", "sum"))
        P("    " + sp.to_string().replace("\n", "\n    "))

    # ------------------------------------------------------------------- Q4
    P("\n" + "=" * 118)
    P("Q4  IS SIZE THE WHOLE STORY?  Within-cell rank correlation of n with the outcomes")
    P("=" * 118)
    q4 = []
    for (cp, pk, ct), sub in G.groupby(["corpus", "panel", "cost"]):
        q4.append(dict(corpus=cp, panel=pk, cost=ct, books=len(sub),
                       rho_n_OOSSharpe=spearman(sub.n, sub.OOS_Sharpe),
                       rho_n_OOSabsDD=spearman(sub.n, sub.OOS_MaxDD.abs()),
                       rho_n_ISSharpe=spearman(sub.n, sub.IS_Sharpe),
                       rho_screen_n=spearman(sub.screen_AS165.astype(float), sub.n),
                       screen_elig=int(sub.screen_AS165.sum())))
    Q4 = pd.DataFrame(q4)
    P("\n" + Q4.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    P(f"\n  means: rho(n, OOS Sharpe) {Q4.rho_n_OOSSharpe.mean():+.3f} "
      f"(t {tstat(Q4.rho_n_OOSSharpe):+.2f}), rho(n, OOS |MaxDD|) "
      f"{Q4.rho_n_OOSabsDD.mean():+.3f} (t {tstat(Q4.rho_n_OOSabsDD):+.2f}), "
      f"rho(screen-eligible, n) {Q4.rho_screen_n.mean():+.3f}")

    P("\n  every changed pick, screen vs the best size floor:")
    show = K[K.selector.isin(["S0 do-nothing (IS-Sharpe argmax)", "SCREEN 4bIS [AS165]",
                              "SCREEN 4bIS [PUB]", bs["selector"]])]
    P(show[["corpus", "panel", "cost", "selector", "pick", "n", "fired", "changed",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "dOOS", "OOS4b_clears"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------- Q5
    P("\n" + "=" * 118)
    P("Q5  RULE 8 -- every row above IS the walk-forward read (pick on <= 2016-12-31, 2017-2026")
    P("    read once).  Selectors against RULES v1 and SPY on the same OOS window.")
    P("=" * 118)
    bench_rows = []
    for tag in order:
        s = K[K.selector == tag]
        bench_rows.append(dict(
            selector=tag, OOS_CAGR=float(s.OOS_CAGR.mean()),
            OOS_Sharpe=float(s.OOS_Sharpe.mean()), OOS_MaxDD=float(s.OOS_MaxDD.mean()),
            beat_v1_Sharpe=int((s.OOS_Sharpe > s.v1_OOS_Sharpe).sum()),
            beat_SPY_Sharpe=int((s.OOS_Sharpe > s.spy_OOS_Sharpe).sum()),
            beat_SPY_CAGR=int((s.OOS_CAGR > s.spy_OOS_CAGR).sum()), n=len(s)))
    bench_rows.append(dict(selector="RULES v1 @ each cell's cost",
                           OOS_CAGR=float(s0.v1_OOS_CAGR.mean()),
                           OOS_Sharpe=float(s0.v1_OOS_Sharpe.mean()),
                           OOS_MaxDD=float(s0.v1_OOS_MaxDD.mean()),
                           beat_v1_Sharpe=np.nan, beat_SPY_Sharpe=np.nan,
                           beat_SPY_CAGR=np.nan, n=len(s0)))
    bench_rows.append(dict(selector="SPY buy-and-hold",
                           OOS_CAGR=float(s0.spy_OOS_CAGR.mean()),
                           OOS_Sharpe=float(s0.spy_OOS_Sharpe.mean()),
                           OOS_MaxDD=float(s0.spy_OOS_MaxDD.mean()),
                           beat_v1_Sharpe=np.nan, beat_SPY_Sharpe=np.nan,
                           beat_SPY_CAGR=np.nan, n=len(s0)))
    P("\n" + pd.DataFrame(bench_rows).to_string(index=False,
                                                float_format=lambda x: f"{x:.4f}"))
    P("\n  per-cell benchmarks (the means above average across three panels, so they are")
    P("  descriptive only):")
    P(s0.reset_index()[["corpus", "panel", "cost", "v1_OOS_Sharpe", "v1_OOS_CAGR",
                        "v1_OOS_MaxDD", "spy_OOS_Sharpe", "spy_OOS_CAGR", "spy_OOS_MaxDD"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n  BOTH KEEP PATHS, on every selector's 11 picked books (full sample, g=0.75):")
    P(S[["selector", "pass4a", "pass4b", "OOS4b"]].to_string(index=False))
    P(f"\n  pool-wide: {int(G.pass4a.sum())}/{len(G)} books pass 4a, "
      f"{int(G.pass4b.sum())}/{len(G)} pass 4b, "
      f"{int(G.OOS4b_clears.sum())}/{len(G)} clear the OOS window.")
    if int(G.pass4b.sum()):
        P("\n  the 4b passes in the pool:")
        P(G[G.pass4b][["corpus", "panel", "cost", "arm", "share", "n", "CAGR", "Sharpe",
                       "MaxDD", "H1", "H2", "OOS_Sharpe"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("\n  NOTE: this run proposes NO new book.  Every book here is idea 159/165/168's,")
    P("  already priced; what is on trial is the SELECTION RULE.")

    # ---------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)
    scr_changed = int(S.loc[S.selector == "SCREEN 4bIS [AS165]", "changed"].iloc[0])
    size_changed = int(bs["changed"])
    best_t = float(max(abs(S.loc[S.selector.str.startswith(("SCREEN", "SIZE")), "t"]
                           .fillna(0))))
    preds = [
        ("P1 idea 178's corpus and picks reproduce", repro,
         f"corpus worst {worst:.1e}, STATIC {int(RP.STATIC_ok.sum())}/11, "
         f"AS165 {int(RP.AS165_ok.sum())}/11, PUB {int(RP.PUB_ok.sum())}/11"),
        ("P2 best size floor captures >= half the screen's edge",
         bool(scr > 0 and bs["dOOS"] >= 0.5 * scr),
         f"{bs['dOOS']:+.4f} vs screen {scr:+.4f}"),
        ("P3 a size floor changes the pick in more cells than the screen",
         size_changed > scr_changed, f"{size_changed} vs {scr_changed} of 11"),
        ("P4 the size floor's changed picks reduce OOS |MaxDD|",
         bool(bs["dMaxDD"] < 0), f"mean d|MaxDD| {bs['dMaxDD']:+.4f}"),
        ("P5 neither instrument reaches |t| >= 2 over 11 cells", best_t < 2.0,
         f"largest |t| {best_t:.2f}"),
    ]
    for tag, hit, detail in preds:
        P(f"  {'HIT ' if hit else 'MISS'}  {tag:<58s}  {detail}")
    P(f"\n  {sum(h for _, h, _ in preds)} of {len(preds)} predictions hit.")
    P(f"\ndone in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
