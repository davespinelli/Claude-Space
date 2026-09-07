#!/usr/bin/env python3
"""Idea 39 (lane B, 2026-09-07): rerun-sandbox-rows-corrected.

QUESTION (queue text): "after 38, re-run any leaderboard row produced in the sandbox on
the corrected index and mark rows that change verdict."

Idea 38 is DONE: data/prices.csv and data/prices_broad.csv are now trading-day indexed
(4699 rows, 0 weekend rows, 2008-01-02 -> 2026-09-04).  The pre-fix caches are not in the
repo, so the honest way to answer 39 is not to hunt for old CSVs but to REBUILD the
artefact deterministically and price it.  The old cache differed from the current one in
exactly two ways, both stated in idea 38's own text:

  (a) START truncation - it began 2014-09-17 because BTC-USD was in the download;
  (b) CALENDAR index   - every equity forward-filled across weekends/holidays.

Both are exactly invertible in the direction that matters (calendar = trading reindexed
to a daily calendar and ffilled), so the four index regimes below reproduce the sandbox
cache bit-for-bit in construction, and the two single-cause arms attribute any damage.

  CORRECTED : trading days, 2008-01-02 ->            (today's cache; the truth)
  TRUNC     : trading days, 2014-09-17 ->            (start effect only)
  CALENDAR  : calendar days, 2008-01-02 ->           (index effect only)
  SANDBOX   : calendar days, 2014-09-17 ->           (the pre-fix cache)

TUNED PARAMETERS: 2 (book width n, gross g).  All 12 grid points reported, every regime,
every panel, every cost rung.  Everything else (RULES v1, RULES v2, EWALL) is a fixed
structural control, not a tuned choice.

4a/4b are evaluated INSIDE each regime against that regime's own SPY and RULES v2 rows -
that is what an analyst working off the broken cache would have computed - and the verdict
flip is (CORRECTED verdict) vs (SANDBOX verdict) on the same book.

Rule 8: (n, g) chosen on IS Sharpe to 2016-12-31 inside a regime, OOS 2017-01-01 -> read
once, and the OOS number is always scored on the CORRECTED tape, because reality is the
corrected tape whatever the analyst was looking at.

Deterministic, standalone: python3 research/backtests/2026-09-07_rerun-sandbox-rows-corrected_B.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights, compare  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 200)
SANDBOX_START = "2014-09-17"          # yfinance BTC-USD inception; idea 38's stated cause
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RUNGS = [0, 10, 25]
NS, GS = [3, 5, 10, 20], [0.75, 0.85, 1.00]   # the only two tuned axes

# ---------------------------------------------------------------- index regimes
def to_calendar(px):
    """Reproduce the pre-fix cache: reindex onto every calendar day and forward-fill."""
    idx = pd.date_range(px.index[0], px.index[-1], freq="D")
    return px.reindex(idx).ffill()

def regimes(px):
    return {
        "CORRECTED": px,
        "TRUNC":     px.loc[SANDBOX_START:],
        "CALENDAR":  to_calendar(px),
        "SANDBOX":   to_calendar(px.loc[SANDBOX_START:]),
    }

# ---------------------------------------------------------------- books
def topn_w(n, g):
    def f(px):
        s, above, vol20 = score(px)
        elig = s.where(above & (vol20 < 0.60))
        rank = elig.rank(axis=1, ascending=False)
        sel = (rank <= n).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0) * g
    return f

def ewall_w(g):
    def f(px):
        s, above, vol20 = score(px)
        sel = (above & (vol20 < 0.60)).astype(float)
        k = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(k, axis=0).fillna(0.0) * g
    return f

def book_menu():
    books = {}
    for n in NS:
        for g in GS:
            books[f"TOP{n}_g{g:.2f}"] = topn_w(n, g)          # the 12 grid points
    for g in GS:
        books[f"EWALL_g{g:.2f}"] = ewall_w(g)                  # structural control
    books["RULESv1"] = rules_v1_weights                        # structural control
    books["RULESv2"] = rules_v2_weights                        # the live book
    return books

GRID = [f"TOP{n}_g{g:.2f}" for n in NS for g in GS]

# ---------------------------------------------------------------- measurement
def stats(r, oos_start=OOS_START):
    m = metrics(r); h = len(r) // 2
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    o = r.loc[oos_start:]
    d["OOS"] = metrics(o)["Sharpe"] if len(o) > 60 else np.nan
    d["OOS_CAGR"] = metrics(o)["CAGR"] if len(o) > 60 else np.nan
    d["OOS_MaxDD"] = metrics(o)["MaxDD"] if len(o) > 60 else np.nan
    return d

def run_panel(px, panel):
    """All books x all regimes x all rungs on one panel. Returns tidy DataFrame."""
    books, out = book_menu(), []
    for rname, rpx in regimes(px).items():
        start = rpx.index[260]                                  # same warm-up rule as compare()
        spy = rpx["SPY"].pct_change().fillna(0).loc[start:]
        for bname, fn in books.items():
            w = fn(rpx)
            for c in RUNGS:
                res = backtest(rpx, w, cost_bps=c, freq="W")
                r = res["returns"].loc[start:]
                row = dict(panel=panel, regime=rname, book=bname, bps=c,
                           turn=res["turnover"].loc[start:].sum() / metrics(r)["Years"])
                row.update(stats(r))
                out.append(row)
        for c in RUNGS:                                         # SPY row per regime/rung
            row = dict(panel=panel, regime=rname, book="SPY", bps=c, turn=0.0)
            row.update(stats(spy)); out.append(row)
        print(f"  [{panel}/{rname}] {len(rpx)} rows, {rpx.index[0].date()} -> {rpx.index[-1].date()}, "
              f"eval from {start.date()}")
    return pd.DataFrame(out)

def verdicts(df):
    """4a vs that regime's RULES v2 row; 4b vs that regime's SPY row. Both computed
    INSIDE the regime - the numbers the analyst on that cache would have seen."""
    df = df.copy(); df["v4a"] = False; df["v4b"] = False; df["fail4b"] = ""
    for (p, rg, c), sub in df.groupby(["panel", "regime", "bps"]):
        v2 = sub[sub.book == "RULESv2"].iloc[0]; spy = sub[sub.book == "SPY"].iloc[0]
        for i, row in sub.iterrows():
            if row.book in ("RULESv2", "SPY"): continue
            df.loc[i, "v4a"] = bool(row.H1 > v2.H1 and row.H2 > v2.H2 and row.MaxDD >= v2.MaxDD)
            bars = [("H1", row.H1 > spy.H1), ("H2", row.H2 > spy.H2), ("OOS", row.OOS > spy.OOS),
                    ("DD", abs(row.MaxDD) <= 0.60 * abs(spy.MaxDD)), ("CAGR", row.CAGR >= 0.70 * spy.CAGR)]
            df.loc[i, "v4b"] = all(b for _, b in bars)
            df.loc[i, "fail4b"] = next((k for k, b in bars if not b), "")
    return df

# ---------------------------------------------------------------- main
def main():
    print("=" * 100)
    print("IDEA 39 - rerun-sandbox-rows-corrected: does the pre-fix calendar-day index change VERDICTS?")
    print("=" * 100)

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        wk = int((v.index.dayofweek >= 5).sum())
        print(f"{k}: {v.shape} {v.index[0].date()}->{v.index[-1].date()} weekend rows={wk} "
              f"(idea 38 fix {'CONFIRMED IN PLACE' if wk == 0 else 'NOT APPLIED'})")

    frames = [run_panel(px, name) for name, px in panels.items()]
    df = verdicts(pd.concat(frames, ignore_index=True))
    df.to_csv(ROOT / "research" / "backtests" / "2026-09-07_rerun-sandbox-rows-corrected_B_grid.csv", index=False)

    fm = lambda x: f"{x:.3f}" if isinstance(x, float) else str(x)

    # ---- 1. the headline: full grid, corrected vs sandbox, at the protocol rung
    print("\n" + "=" * 100)
    print("1. ALL GRID POINTS at 10 bps - CORRECTED tape vs SANDBOX tape (the pre-fix cache)")
    print("=" * 100)
    for p in panels:
        a = df[(df.panel == p) & (df.bps == 10) & (df.regime == "CORRECTED")].set_index("book")
        s = df[(df.panel == p) & (df.bps == 10) & (df.regime == "SANDBOX")].set_index("book")
        t = pd.DataFrame({
            "CAGR_c": a.CAGR, "CAGR_s": s.CAGR, "Sh_c": a.Sharpe, "Sh_s": s.Sharpe,
            "dSh": s.Sharpe - a.Sharpe, "ratio": s.Sharpe / a.Sharpe,
            "DD_c": a.MaxDD, "DD_s": s.MaxDD,
            "4a_c": a.v4a, "4a_s": s.v4a, "4b_c": a.v4b, "4b_s": s.v4b,
        })
        t["FLIP"] = np.where(t["4a_c"] != t["4a_s"], "4a", "") + np.where(t["4b_c"] != t["4b_s"], " 4b", "")
        print(f"\n--- {p} ---")
        print(t.to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- 2. verdict flip census over the whole cube
    print("\n" + "=" * 100)
    print("2. VERDICT FLIP CENSUS - every book x panel x rung, CORRECTED vs SANDBOX (all reported)")
    print("=" * 100)
    piv = df[df.book.isin(GRID + [f"EWALL_g{g:.2f}" for g in GS] + ["RULESv1"])]
    a = piv[piv.regime == "CORRECTED"].set_index(["panel", "book", "bps"])
    s = piv[piv.regime == "SANDBOX"].set_index(["panel", "book", "bps"])
    j = a[["v4a", "v4b", "Sharpe", "CAGR", "MaxDD", "fail4b"]].join(
        s[["v4a", "v4b", "Sharpe", "CAGR", "MaxDD", "fail4b"]], lsuffix="_c", rsuffix="_s")
    n = len(j)
    print(f"cells: {n}   4a TRUE corrected {int(j.v4a_c.sum())}, sandbox {int(j.v4a_s.sum())}")
    print(f"          4b TRUE corrected {int(j.v4b_c.sum())}, sandbox {int(j.v4b_s.sum())}")
    f4a, f4b = j[j.v4a_c != j.v4a_s], j[j.v4b_c != j.v4b_s]
    print(f"FLIPS: 4a {len(f4a)}/{n}  ({len(f4a)/n:.1%}),  4b {len(f4b)}/{n}  ({len(f4b)/n:.1%})")
    print(f"       any-verdict flip: {len(j[(j.v4a_c != j.v4a_s) | (j.v4b_c != j.v4b_s)])}/{n}")
    if len(f4b):
        print("\n4b flips (corrected -> sandbox):")
        print(f4b[["v4b_c", "v4b_s", "Sharpe_c", "Sharpe_s", "CAGR_c", "CAGR_s",
                   "fail4b_c", "fail4b_s"]].to_string(float_format=lambda x: f"{x:.3f}"))
    if len(f4a):
        print("\n4a flips (corrected -> sandbox):")
        print(f4a[["v4a_c", "v4a_s", "Sharpe_c", "Sharpe_s"]].to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- 3. attribution: which of the two causes does the damage
    print("\n" + "=" * 100)
    print("3. ATTRIBUTION - TRUNC (start only) vs CALENDAR (index only) vs SANDBOX (both)")
    print("   CALENDAR/CORRECTED and SANDBOX/TRUNC are matched-span pairs: index effect alone.")
    print("=" * 100)
    for p in panels:
        d = df[(df.panel == p) & (df.bps == 10)].pivot_table(index="book", columns="regime", values="Sharpe")
        c = df[(df.panel == p) & (df.bps == 10)].pivot_table(index="book", columns="regime", values="CAGR")
        t = pd.DataFrame({
            "Sh_CORRECTED": d.CORRECTED, "Sh_TRUNC": d.TRUNC, "Sh_CALENDAR": d.CALENDAR, "Sh_SANDBOX": d.SANDBOX,
            "idxSh_full": d.CALENDAR / d.CORRECTED, "idxSh_trunc": d.SANDBOX / d.TRUNC,
            "CAGR_CORR": c.CORRECTED, "CAGR_CAL": c.CALENDAR, "idxCAGR": c.CALENDAR / c.CORRECTED,
        })
        print(f"\n--- {p} ---")
        print(t.to_string(float_format=lambda x: f"{x:.3f}"))
        print(f"  index-only Sharpe ratio: median {t.idxSh_full.median():.4f} (full span), "
              f"{t.idxSh_trunc.median():.4f} (truncated span); sqrt(5/7) = {np.sqrt(5/7):.4f}")
        print(f"  index-only CAGR  ratio: median {t.idxCAGR.median():.4f}; the pure re-annualisation "
              f"identity (1+c)^(252/365)-1 predicts {((1.10)**(252/365)-1)/0.10:.4f}x on a 10%/yr book")
        # is the CAGR damage pure bookkeeping, or a real path difference? matched-span pair.
        pred = (1 + c.TRUNC) ** (252 / 365) - 1
        err = (c.SANDBOX - pred) * 100
        print(f"  CAGR identity on the matched-span pair (TRUNC -> SANDBOX): mean error "
              f"{err.mean():+.3f} pp, MAE {err.abs().mean():.3f} pp, max |err| {err.abs().max():.3f} pp "
              f"-> the CAGR gap is {'PURE re-annualisation bookkeeping' if err.abs().max() < 0.25 else 'NOT pure bookkeeping'}")

    # ---- 4. does the ORDERING survive? (a scalar distortion is harmless for ranking)
    print("\n" + "=" * 100)
    print("4. DOES THE ARTEFACT PRESERVE THE RANKING OF THE 12 GRID POINTS?")
    print("=" * 100)
    for p in panels:
        for c in RUNGS:
            g = df[(df.panel == p) & (df.bps == c) & (df.book.isin(GRID))]
            a2 = g[g.regime == "CORRECTED"].set_index("book").Sharpe
            for rg in ("TRUNC", "CALENDAR", "SANDBOX"):
                b2 = g[g.regime == rg].set_index("book").Sharpe.reindex(a2.index)
                sp = a2.rank().corr(b2.rank())          # pearson on ranks == spearman (no scipy here)
                same = a2.idxmax() == b2.idxmax()
                print(f"  {p} @{c:2d}bps  {rg:9s}  spearman(rank) = {sp:+.3f}   argmax same? "
                      f"{'YES' if same else 'NO  (' + str(a2.idxmax()) + ' -> ' + str(b2.idxmax()) + ')'}")

    # ---- 5. rule 8 walk-forward: does the broken tape change the DECISION?
    print("\n" + "=" * 100)
    print("5. RULE 8 WALK-FORWARD - (n,g) chosen on IS<=2016 inside each regime; OOS 2017- always")
    print("   scored on the CORRECTED tape (reality), at 10 bps. Menu = the 12 grid points.")
    print("=" * 100)
    wf = []
    for p, px in panels.items():
        rg = regimes(px)
        # OOS truth, computed once on the corrected tape
        truth = {}
        for b in GRID + ["EWALL_g0.75", "RULESv2", "SPY"]:
            row = df[(df.panel == p) & (df.regime == "CORRECTED") & (df.bps == 10) & (df.book == b)].iloc[0]
            truth[b] = (row.OOS, row.OOS_CAGR, row.OOS_MaxDD)
        for rname in ("CORRECTED", "TRUNC", "CALENDAR", "SANDBOX"):
            rpx = rg[rname]; start = rpx.index[260]
            is_sh, is_days = {}, 0
            for b in GRID:
                n, gg = int(b[3:].split("_")[0]), float(b.split("_g")[1])
                r = backtest(rpx, topn_w(n, gg)(rpx), cost_bps=10, freq="W")["returns"].loc[start:IS_END]
                is_sh[b], is_days = (metrics(r)["Sharpe"] if len(r) > 120 else np.nan), len(r)
            pick = max(is_sh, key=lambda k: (-np.inf if np.isnan(is_sh[k]) else is_sh[k]))
            wf.append(dict(panel=p, regime=rname, IS_rows=is_days, pick=pick, IS_Sharpe=is_sh[pick],
                           OOS_Sharpe_true=truth[pick][0], OOS_CAGR_true=truth[pick][1],
                           OOS_MaxDD_true=truth[pick][2]))
    wfd = pd.DataFrame(wf)
    print(wfd.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for p in panels:
        sub = wfd[wfd.panel == p].set_index("regime")
        cpick, spick = sub.loc["CORRECTED", "pick"], sub.loc["SANDBOX", "pick"]
        reg = sub.loc["SANDBOX", "OOS_Sharpe_true"] - sub.loc["CORRECTED", "OOS_Sharpe_true"]
        print(f"\n  {p}: corrected tape picks {cpick} (OOS {sub.loc['CORRECTED','OOS_Sharpe_true']:.3f}); "
              f"sandbox tape picks {spick} (OOS {sub.loc['SANDBOX','OOS_Sharpe_true']:.3f})")
        print(f"      DECISION {'UNCHANGED' if cpick == spick else 'CHANGED'}; OOS regret from using the "
              f"broken tape = {reg:+.3f} Sharpe")
        print(f"      anchors: EWALL_g0.75 OOS {truth_of(df,p,'EWALL_g0.75'):.3f}, "
              f"RULESv2 OOS {truth_of(df,p,'RULESv2'):.3f}, SPY OOS {truth_of(df,p,'SPY'):.3f}")

    # ---- 6. protocol-standard row for the best corrected grid point
    print("\n" + "=" * 100)
    print("6. baseline.compare() on the corrected tape, best grid point by full-sample Sharpe (U56)")
    print("=" * 100)
    best = df[(df.panel == "U56") & (df.regime == "CORRECTED") & (df.bps == 10) &
              (df.book.isin(GRID))].sort_values("Sharpe", ascending=False).iloc[0]
    n, gg = int(best.book[3:].split("_")[0]), float(best.book.split("_g")[1])
    compare(f"39 corrected-tape control {best.book}", topn_w(n, gg), panels["U56"], cost_bps=10)

def truth_of(df, p, b):
    return df[(df.panel == p) & (df.regime == "CORRECTED") & (df.bps == 10) & (df.book == b)].iloc[0].OOS

if __name__ == "__main__":
    main()
