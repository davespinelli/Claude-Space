#!/usr/bin/env python3
"""Idea 966 (lane cloud, 2026-09-22): IS 4b PASSABILITY A PANEL FACT RATHER THAN A BOOK FACT?

Idea 962 found 12 of 30 families contain at least one 4b-passing phase, that U56 carries 9 of
them, B136 3 and SMALL 0, and that this holds across all five books.  If the panel decides the
verdict then every published '<book X> clears 4b' is really '<panel> clears 4b', and no amount
of book work on B136 or SMALL can reach it.

DESIGN.  A rectangular (panel x book x cadence x phase) grid, each cell priced at four cost
rungs in three windows, and the OOS 4b pass rate decomposed over the three factors.

  panels  U56 (56 names), B136 (136), SMALL (the sub-$2B pool, see the SURVIVORSHIP note below)
  books   five, spanning the record's families and ending in a book with NO rule in it at all:
            BAND03_G075  live RULES v2: 200d +/-3% band, gross 0.75/N, gated weight to cash
            BAND03_G100  the same band at gross 1.00/N
            V1TOP5       RULES v1: vol-scaled composite, top 5 at 15% each
            TOP20EW      the 2026-09-04 KEEP-4b form: composite WITHOUT the vol scaler, top 20
                         equal-weight at gross 1.00
            EWALL        equal-weight the WHOLE panel at gross 1.00 -- a pure PANEL read, zero
                         book information.  This is the control the question turns on.
          cadence D, W, M, Q;  phase d = 0..4 trading days before the period end (D has one).
  costs   0 / 10 / 25 / 50 bps (headline 10);  windows FULL / IS (->2016) / OOS (2017->).

TUNED (2, exactly, as the idea specifies): DECOMPOSITION in {eta2, linear-probability-model}
and PANEL SET in {U56+B136, U56+B136+SMALL}.  Both settings of both are reported.  The book,
cadence, phase and cost axes are PUBLISHED-NOT-TUNED: every grid point appears in the CSV.

Rule 8: inside each panel, (book, cadence) chosen on 2009-2016 IS Sharpe ALONE at phase 0 and
10 bps; 2017-2026 read ONCE.  Both KEEP paths on every cell: 4a vs live RULES v2 on the same
panel, 4b vs SPY.

SURVIVORSHIP: the SMALL panel is CURRENT constituents of a sub-$2B screen (data/SMALL_PANEL_README.md),
so its levels are biased UP; tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped
first.  The label 'SMALL483' no longer matches the pool size (ideas 706 / 1074) -- the count
actually used is printed and published.  Nothing here is a claim about small-cap returns; the
panel enters only as a third independent reading of the same five books.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights, band_state, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

CADENCES = ["D", "W", "M", "Q"]
PHASES = [0, 1, 2, 3, 4]
COSTS = [0.0, 10.0, 25.0, 50.0]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = ROOT / "research" / "backtests"
STEM = "2026-09-22_is-4b-passability-a-panel-fact_cloud"


# ---------------------------------------------------------------- books
def w_band(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def w_topn(px, n, gross, vol_scale, max_vol=0.60):
    s, above, vol20 = score(px, vol_scale)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (gross / n)


def w_ewall(px, gross=1.0):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


BOOKS = {
    "BAND03_G075": lambda px: w_band(px, 0.03, 0.75),
    "BAND03_G100": lambda px: w_band(px, 0.03, 1.00),
    "V1TOP5":      lambda px: rules_v1_weights(px),
    "TOP20EW":     lambda px: w_topn(px, 20, 1.00, vol_scale=False),
    "EWALL":       lambda px: w_ewall(px),
}


# ---------------------------------------------------------------- runner
def offset_mask(idx, freq, d):
    """Rebalance d trading days EARLIER than the last trading day of each period.  d=0 at
    freq='W' is byte-identical to engine.rebalance_mask(idx,'W') (gate G1).  A period with
    <= d trading days falls back to its earliest day; those are CLIPPED and counted."""
    if freq == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(freq), index=idx)
    mask = pd.Series(False, index=idx); clipped = 0
    for _, grp in key.groupby(key, sort=False):
        days = grp.index
        if len(days) > d:
            pick = days[-(1 + d)]
        else:
            pick = days[0]; clipped += 1
        mask.loc[pick] = True
    return mask, clipped


def run(px, W, mask):
    """engine.backtest semantics (decide at t, apply at t+1, drift between rebalances), numpy.
    Returns gross-of-cost returns + turnover, so every cost rung is an exact affine re-read."""
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    m = mask.shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); held = np.zeros_like(rets); to = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]; to[i] = np.abs(new - cur).sum(); cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return pd.Series((held * rets).sum(axis=1), index=px.index), pd.Series(to, index=px.index)


def m6(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def keep4a(a, b):
    return bool(a["H1"] > b["H1"] and a["H2"] > b["H2"] and a["MaxDD"] >= b["MaxDD"])


def legs4b(a, s):
    return dict(H1=bool(a["H1"] > s["H1"]), H2=bool(a["H2"] > s["H2"]),
                DD=bool(a["MaxDD"] >= 0.60 * s["MaxDD"]), CAGR=bool(a["CAGR"] >= 0.70 * s["CAGR"]))


# ---------------------------------------------------------------- panels
def panels():
    out = {}
    out["U56"] = (load_universe(), None)
    out["B136"] = (load_universe(broad=True), None)
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c not in bad]
    px = px[keep]
    out["SMALL"] = (px, "SPY")          # SPY is a benchmark column, NOT a constituent
    return out


def main():
    rows = []; gates = {}
    for pname, (px, bench_only) in panels().items():
        idx = px.index
        trad = px.drop(columns=[bench_only]) if bench_only else px
        start = idx[260]
        wins = {"FULL": (start, idx[-1]), "IS": (start, pd.Timestamp(IS_END)),
                "OOS": (pd.Timestamp(OOS_START), idx[-1])}
        print(f"\n=== {pname}: {trad.shape[1]} tradable names, {idx[0].date()}..{idx[-1].date()} ===")

        mW, _ = offset_mask(idx, "W", 0)
        gates[f"G1_{pname}_Wmask_vs_engine"] = int((mW.values != rebalance_mask(idx, "W").values).sum())
        gates[f"G2_{pname}_band_vs_rules_v2"] = float((w_band(trad, 0.03, 0.75) -
                                                       rules_v2_weights(trad, 0.03, 0.75)).abs().max().max())
        wl = rules_v2_weights(trad, 0.03, 0.75)
        g, t = run(trad, wl, mW)
        eng = engine_backtest(trad, wl, cost_bps=10.0, freq="W")["returns"]
        gates[f"G3_{pname}_runner_vs_engine"] = float((g - t * 10.0 / 1e4 - eng).abs().max())
        gates[f"G4_{pname}_clipped_Q_d4"] = offset_mask(idx, "Q", 4)[1]
        gates[f"G5_{pname}_tradable_names"] = int(trad.shape[1])

        spy = px["SPY"].pct_change().fillna(0.0)
        bench = {}
        for wn, (a, b) in wins.items():
            bench[("SPY", wn)] = m6(spy.loc[a:b])
            bench[("RULESv2", wn)] = m6(eng.loc[a:b])
        for (nm, wn), v in bench.items():
            rows.append(dict(panel=pname, book=nm, cadence="W", phase=0, cost=10.0, window=wn,
                             turn=np.nan, **v, keep4a=False, keep4b=False,
                             **{f"leg_{x}": False for x in ("H1", "H2", "DD", "CAGR")}))

        for bname, fn in BOOKS.items():
            W = fn(trad)
            for cad in CADENCES:
                for d in (PHASES if cad != "D" else [0]):
                    mk, _ = offset_mask(idx, cad, d)
                    g, t = run(trad, W, mk)
                    for cost in COSTS:
                        r = g - t * cost / 1e4
                        for wn, (a, b) in wins.items():
                            mm = m6(r.loc[a:b]); s = bench[("SPY", wn)]; bl = bench[("RULESv2", wn)]
                            lg = legs4b(mm, s)
                            rows.append(dict(panel=pname, book=bname, cadence=cad, phase=d,
                                             cost=cost, window=wn,
                                             turn=float(t.loc[a:b].sum() / (len(t.loc[a:b]) / 252)),
                                             **mm, keep4a=keep4a(mm, bl), keep4b=all(lg.values()),
                                             **{f"leg_{k}": v for k, v in lg.items()}))
            print(f"  {bname} done ({len(rows)} rows)")

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{STEM}.csv.gz", index=False, compression="gzip")
    print("\n=== GATES ===")
    for k, v in gates.items():
        print(f"  {k}: {v}")
    print(f"\n{len(df)} published rows -> {STEM}.csv.gz")
    return df, gates


# ---------------------------------------------------------------- decomposition
def eta2(y, f):
    """Share of the binary outcome's total sum of squares carried by a factor's group means."""
    y = np.asarray(y, float); gm = y.mean()
    sst = ((y - gm) ** 2).sum()
    if sst == 0:
        return 0.0
    ssb = sum(len(y[f == lv]) * (y[f == lv].mean() - gm) ** 2 for lv in pd.unique(f))
    return float(ssb / sst)


def lpm(y, factors):
    """Additive linear-probability model on dummy-coded main effects.  Returns full R2 and each
    factor's partial R2 (R2 lost when that factor's dummies are dropped)."""
    y = np.asarray(y, float)

    def design(keys):
        cols = [np.ones(len(y))]
        for k in keys:
            lv = sorted(pd.unique(factors[k]))[1:]        # drop-first coding
            cols += [(factors[k] == v).astype(float).values for v in lv]
        return np.column_stack(cols)

    def r2(keys):
        X = design(keys)
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ beta
        sst = ((y - y.mean()) ** 2).sum()
        return 1.0 - (res ** 2).sum() / sst if sst > 0 else 0.0

    keys = list(factors)
    full = r2(keys)
    return full, {k: full - r2([x for x in keys if x != k]) for k in keys}


def analysis(df):
    L = df[df.book.isin(BOOKS)].copy()
    h = L[L.cost == 10.0]

    print("\n########## A. MARGINAL 4b PASS RATES (10 bps; 80 cells per panel, 48 per book) ##########")
    for wn in ["FULL", "IS", "OOS"]:
        x = h[h.window == wn]
        print(f"\n-- {wn} --")
        print("  by panel:  " + "  ".join(f"{p} {x[x.panel==p].keep4b.mean():.3f} "
                                          f"({int(x[x.panel==p].keep4b.sum())}/{len(x[x.panel==p])})"
                                          for p in ["U56", "B136", "SMALL"]))
        print("  by book:   " + "  ".join(f"{b} {x[x.book==b].keep4b.mean():.3f}" for b in BOOKS))
        print("  by cadence:" + "  ".join(f"{c} {x[x.cadence==c].keep4b.mean():.3f}" for c in CADENCES))
        print(x.pivot_table(index="book", columns="panel", values="keep4b", aggfunc="mean").round(3).to_string())

    print("\n########## B. THE DECOMPOSITION (tuned param 1 x tuned param 2: both settings of both) ##########")
    for pset, label in (( ["U56", "B136"], "U56+B136"), (["U56", "B136", "SMALL"], "U56+B136+SMALL")):
        for wn in ["FULL", "OOS"]:
            x = h[(h.window == wn) & h.panel.isin(pset)]
            y = x.keep4b.values
            fac = {"panel": x.panel, "book": x.book, "cadence": x.cadence}
            e = {k: eta2(y, v.values) for k, v in fac.items()}
            full, part = lpm(y, fac)
            print(f"\n-- panel set {label}, window {wn} (base rate {y.mean():.3f}, n={len(y)}) --")
            print(f"   D1 eta2   : panel {e['panel']:.4f}  book {e['book']:.4f}  cadence {e['cadence']:.4f}"
                  f"   -> panel/book ratio {e['panel']/max(e['book'],1e-12):.2f}x")
            print(f"   D2 LPM    : R2 {full:.4f} | partial R2 panel {part['panel']:.4f}  "
                  f"book {part['book']:.4f}  cadence {part['cadence']:.4f}")

    print("\n########## C. THE DIRECT QUESTION: does ANY book pass where U56 does not? ##########")
    for wn in ["FULL", "IS", "OOS"]:
        for cost in COSTS:
            x = h[(h.window == wn)] if cost == 10.0 else L[(L.window == wn) & (L.cost == cost)]
            k = x.set_index(["panel", "book", "cadence", "phase"]).keep4b
            u = k.xs("U56")
            for other in ["B136", "SMALL"]:
                o = k.xs(other)
                common = u.index.intersection(o.index)
                only = [i for i in common if o[i] and not u[i]]
                print(f"{wn:4s} {cost:5.1f} bps  {other} passes where U56 fails: {len(only)} of {len(common)}"
                      + (f"  -> {only[:6]}" if only else ""))

    print("\n########## D. THE PURE-PANEL CONTROL (EWALL: no book information at all) ##########")
    for wn in ["FULL", "IS", "OOS"]:
        x = h[(h.window == wn) & (h.book == "EWALL")]
        for p in ["U56", "B136", "SMALL"]:
            y = x[x.panel == p]
            bestrow = y.sort_values("Sharpe", ascending=False).iloc[0]
            print(f"{wn:4s} {p:6s} EWALL 4b {int(y.keep4b.sum())}/{len(y)} | best cell "
                  f"{bestrow.cadence}{int(bestrow.phase)} {bestrow.CAGR:.2%}/{bestrow.Sharpe:.4f}/{bestrow.MaxDD:.2%}"
                  f" | legs failed: H1 {int((~y.leg_H1).sum())} H2 {int((~y.leg_H2).sum())} "
                  f"DD {int((~y.leg_DD).sum())} CAGR {int((~y.leg_CAGR).sum())}")

    print("\n########## E. BINDING LEGS BY PANEL (10 bps, OOS) -- WHICH leg the panel moves ##########")
    for p in ["U56", "B136", "SMALL"]:
        x = h[(h.window == "OOS") & (h.panel == p)]
        f = x[~x.keep4b]
        s = df[(df.panel == p) & (df.book == "SPY") & (df.window == "OOS")].iloc[0]
        print(f"{p:6s} SPY OOS {s.CAGR:.2%}/{s.Sharpe:.4f}/{s.MaxDD:.2%} (H1 {s.H1:.3f} H2 {s.H2:.3f}) | "
              f"of {len(f)} fails: H1 {int((~f.leg_H1).sum())} H2 {int((~f.leg_H2).sum())} "
              f"DD {int((~f.leg_DD).sum())} CAGR {int((~f.leg_CAGR).sum())}")

    print("\n########## F. RULE 8 (book, cadence on 2009-2016 IS Sharpe only; 2017-2026 read once) ##########")
    for p in ["U56", "B136", "SMALL"]:
        g = h[(h.panel == p) & (h.phase == 0)]
        s = df[(df.panel == p) & (df.book == "SPY") & (df.window == "OOS")].iloc[0]
        b = df[(df.panel == p) & (df.book == "RULESv2") & (df.window == "OOS")].iloc[0]
        pick = g[g.window == "IS"].sort_values("Sharpe", ascending=False).iloc[0]
        o = g[(g.window == "OOS") & (g.book == pick.book) & (g.cadence == pick.cadence)].iloc[0]
        fu = g[(g.window == "FULL") & (g.book == pick.book) & (g.cadence == pick.cadence)].iloc[0]
        ph = L[(L.panel == p) & (L.book == pick.book) & (L.cadence == pick.cadence) &
               (L.window == "OOS") & (L.cost == 10.0)].sort_values("phase")
        cs = L[(L.panel == p) & (L.book == pick.book) & (L.cadence == pick.cadence) &
               (L.window == "OOS") & (L.phase == 0)].sort_values("cost")
        print(f"\n{p}: pick {pick.book} / {pick.cadence} (IS Sharpe {pick.Sharpe:.4f})")
        print(f"   OOS  {o.CAGR:.2%} / {o.Sharpe:.4f} / {o.MaxDD:.2%} (H1 {o.H1:.3f} H2 {o.H2:.3f}) "
              f"4b={o.keep4b} 4a={o.keep4a} legs H1={o.leg_H1} H2={o.leg_H2} DD={o.leg_DD} CAGR={o.leg_CAGR}")
        print(f"   FULL {fu.CAGR:.2%} / {fu.Sharpe:.4f} / {fu.MaxDD:.2%} (H1 {fu.H1:.3f} H2 {fu.H2:.3f}) 4b={fu.keep4b} 4a={fu.keep4a}")
        print(f"   SPY OOS {s.CAGR:.2%} / {s.Sharpe:.4f} / {s.MaxDD:.2%} | RULES v2 OOS {b.CAGR:.2%} / {b.Sharpe:.4f} / {b.MaxDD:.2%}")
        print(f"   OOS 4b at phases {list(ph.phase)} = {list(ph.keep4b.astype(int))}; at 0/10/25/50 bps = {list(cs.keep4b.astype(int))}")

    print("\n########## G. BEST CELL PER (panel, book): can ANY book reach 4b on B136 / SMALL? ##########")
    for wn in ["FULL", "OOS"]:
        print(f"\n-- {wn}, best OOS-legal cell per (panel, book) by Sharpe, 10 bps --")
        for p in ["U56", "B136", "SMALL"]:
            for bk in BOOKS:
                y = h[(h.window == wn) & (h.panel == p) & (h.book == bk)]
                r = y.sort_values("Sharpe", ascending=False).iloc[0]
                print(f"   {p:6s} {bk:12s} {r.cadence}{int(r.phase)} {r.CAGR:7.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}"
                      f"  4b {int(y.keep4b.sum())}/{len(y)}  4a {int(y.keep4a.sum())}/{len(y)}")


if __name__ == "__main__":
    df, gates = main()
    analysis(df)
