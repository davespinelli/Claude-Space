#!/usr/bin/env python3
"""Idea 140 — abstention is the whole screen.

Idea 132 found rule 8's in-sample 4b screen changes 0 of 18 picks and that all of its
apparent OOS value is DECLINING TO ENTER (the small panel, the V1u book).  That was
measured on PICKS.  This tests the abstention directly on RETURNS.

Corpus: 18 cells = 6 book-forms (EWALL, BAND v2-form, MA200-EW, TOP10/20/30) x 3 panels
(u56, broad136, small439), each at the record's default 0.75 gross, weekly, t+1, 10 bps.

At every year-end a CAUSAL screen re-fits on history only and each cell is flagged pass
/ fail on the 4b bars (Sharpe > SPY, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) over
that window.  The next calendar year is then traded by five composites, all equal-weighted
across cells and all charged 10 bps on the weight they move at each re-screen:

    ALWAYS            hold all 18 cells                       (exposure 1.00)
    SCREEN-DEGROSS    hold the passing cells only, rest CASH   (exposure = pass share)
    SCREEN-RESPREAD   hold the passing cells re-weighted to full exposure (exposure 1.00)
    RANDOM-MATCHED    hold a RANDOM subset of the same size    (exposure = pass share)
    NEVER             cash                                     (exposure 0.00)

The three-way split is the whole point: SCREEN-DEGROSS beating ALWAYS is worth nothing
if RANDOM-MATCHED does it too (that is exposure, i.e. abstention), and the screen only
has SELECTION value if SCREEN-RESPREAD beats ALWAYS at matched exposure.

TUNED DIALS (max 2, per PROTOCOL 4): the screen's fitting window (expanding | trailing 5y)
and the abstention convention (de-gross | re-spread).  Both are reported at every level.
Rule 8: the dial pair is chosen on the first half only and the second half is read once.

SURVIVORSHIP: small439 = the 483-name sub-$2B panel less the 44 with max_1d_move >= 1.0,
current constituents of the screen only; broad136 is current large-cap constituents.  Both
overstate every cell's level, the controls included, so read the CONTRASTS, not the levels.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

COST, FREQ, GROSS = 10.0, "W", 0.75
SEEDS = 20

def run(px, W, cost_bps=COST, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = W.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n, k = rets.shape
    cur = np.zeros(k); port = np.zeros(n); turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        port[i] = cur @ rets[i] - turn[i] * cost_bps / 1e4
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    return pd.Series(port, index=px.index)

def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])

def ewall(px, g=GROSS):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

def ma200(px, g=GROSS):
    above = (px > px.rolling(200).mean()).astype(float).where(px.notna(), 0.0)
    n = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0).sum(axis=1)
    return g * above.div(n.replace(0, np.nan), axis=0).fillna(0.0)

def topn(px, n, g=GROSS):
    s, above, vol20 = score(px, vol_scale=False)
    elig = s.where(above & (vol20 < 0.60))
    return g * (elig.rank(axis=1, ascending=False) <= n).astype(float) / n

BOOKS = [("EWALL", ewall), ("BAND", lambda px: rules_v2_weights(px, gross=GROSS)),
         ("MA200", ma200)] + [(f"TOP{n}", (lambda n: lambda px: topn(px, n))(n)) for n in (10, 20, 30)]

def panels():
    out = {"u56": load_universe(), "broad136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    out[f"small{len(keep)-1}"] = sm[keep]
    return out

def bars4b(r, spy):
    """4b bars over one window: Sharpe > SPY, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    if len(r) < 120: return False
    a, s = metrics(r), metrics(spy)
    return bool(a["Sharpe"] > s["Sharpe"] and a["MaxDD"] >= 0.60 * s["MaxDD"]
                and a["CAGR"] >= 0.70 * s["CAGR"])

def composite(R, Wc, cost_bps=COST):
    """Equal-ish weighted composite of cell return series with cell-switch costs.
    Wc: DataFrame of cell weights (index = R.index), already forward-filled."""
    switch = Wc.diff().abs().sum(axis=1).fillna(0.0)
    return (R * Wc).sum(axis=1) - switch * cost_bps / 1e4

def main():
    P = panels()
    idx = None
    cells, spys = {}, {}
    gate = None
    for pn, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for bn, fn in BOOKS:
            W = fn(px)
            r = run(px, W).loc[start:]
            if gate is None:                                  # GATE vs engine.backtest
                eng = backtest(px, W, cost_bps=COST, freq=FREQ)["returns"].loc[start:]
                gate = np.abs(r - eng).max()
                print(f"[GATE] max|run - engine.backtest| ({pn}/{bn}) = {gate:.3e}")
            cells[f"{pn}/{bn}"] = r
        spys[pn] = spy
        idx = spy.index if idx is None else idx.intersection(spy.index)

    R = pd.DataFrame({k: v for k, v in cells.items()}).loc[idx].fillna(0.0)
    SPY = pd.DataFrame({k: v for k, v in spys.items()}).loc[idx].fillna(0.0)
    names = list(R.columns)
    print(f"\ncells {len(names)} | common sample {idx[0].date()} -> {idx[-1].date()} ({len(idx)} days)")

    # ---------------- causal year-end screen
    years = sorted(set(idx.year))
    ends = {y: idx[idx.year == y][-1] for y in years}
    FLAGS = {}                                                 # (window, year) -> pass vector
    for win in ("expanding", "trail5"):
        for y in years[:-1]:
            t = ends[y]
            lo = idx[0] if win == "expanding" else max(idx[0], t - pd.DateOffset(years=5))
            f = []
            for c in names:
                pn = c.split("/")[0]
                f.append(bars4b(R[c].loc[lo:t], SPY[pn].loc[lo:t]))
            FLAGS[(win, y)] = np.array(f, dtype=bool)

    first = years[3]                                           # need >=3y of history
    trade = idx[idx.year > first]
    rng = np.random.default_rng(7)

    def weight_path(win, conv, pick=None):
        Wc = pd.DataFrame(0.0, index=idx, columns=names)
        for y in years:
            if y <= first: continue
            fl = FLAGS[(win, y - 1)] if pick is None else pick[(win, y)]
            m = idx.year == y
            k = fl.sum()
            if k == 0: continue
            w = np.where(fl, 1.0 / len(names), 0.0) if conv == "degross" else np.where(fl, 1.0 / k, 0.0)
            Wc.loc[m, :] = w
        return Wc

    results = {}
    always = pd.DataFrame(1.0 / len(names), index=idx, columns=names)
    always.loc[idx.year <= first, :] = 0.0
    results["ALWAYS"] = composite(R, always)
    results["NEVER"] = pd.Series(0.0, index=idx)
    onshare = {}
    for win in ("expanding", "trail5"):
        for conv in ("degross", "respread"):
            Wc = weight_path(win, conv)
            results[f"SCREEN-{win}-{conv}"] = composite(R, Wc)
        onshare[win] = np.mean([FLAGS[(win, y - 1)].mean() for y in years if y > first])
        # RANDOM-MATCHED: same yearly count, random membership, averaged over SEEDS draws
        acc = []
        for s in range(SEEDS):
            rg = np.random.default_rng(1000 + s)
            pick = {}
            for y in years:
                if y <= first: continue
                k = FLAGS[(win, y - 1)].sum()
                v = np.zeros(len(names), dtype=bool)
                if k: v[rg.choice(len(names), int(k), replace=False)] = True
                pick[(win, y)] = v
            acc.append(composite(R, weight_path(win, "degross", pick)))
        results[f"RANDOM-{win}-degross"] = pd.concat(acc, axis=1).mean(axis=1)

    out = pd.DataFrame({k: stats(v.loc[trade]) for k, v in results.items()}).T
    spy_t = SPY["u56"].loc[trade]
    out.loc["SPY"] = stats(spy_t)
    print("\n" + "=" * 96); print("COMPOSITES over the traded sample (10 bps, incl. cell-switch cost)")
    print("=" * 96)
    print(out.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\nmean yearly PASS share: expanding {onshare['expanding']:.3f}  trail5 {onshare['trail5']:.3f}")

    print("\n" + "=" * 96); print("THE THREE-WAY SPLIT (the idea's actual question)"); print("=" * 96)
    for win in ("expanding", "trail5"):
        a = out.loc["ALWAYS"]; d = out.loc[f"SCREEN-{win}-degross"]
        rr = out.loc[f"SCREEN-{win}-respread"]; rm = out.loc[f"RANDOM-{win}-degross"]
        print(f"\n[{win}]")
        print(f"  dSharpe SCREEN-degross  - ALWAYS = {d.Sharpe - a.Sharpe:+.4f}   (exposure + selection)")
        print(f"  dSharpe RANDOM-matched  - ALWAYS = {rm.Sharpe - a.Sharpe:+.4f}   (exposure ALONE = abstention)")
        print(f"  dSharpe SCREEN-degross  - RANDOM = {d.Sharpe - rm.Sharpe:+.4f}   (SELECTION, exposure held)")
        print(f"  dSharpe SCREEN-respread - ALWAYS = {rr.Sharpe - a.Sharpe:+.4f}   (SELECTION at full exposure)")
        share = (d.Sharpe - rm.Sharpe) / (d.Sharpe - a.Sharpe) if abs(d.Sharpe - a.Sharpe) > 1e-9 else np.nan
        print(f"  -> selection share of the screen's total edge: {share:+.1%}")

    print("\n" + "=" * 96); print("RULE 8 — dial pair chosen on the FIRST HALF only, second half read once")
    print("=" * 96)
    h = len(trade) // 2; is_i, oos_i = trade[:h], trade[h:]
    cand = [k for k in results if k.startswith("SCREEN-")]
    is_sh = {k: metrics(results[k].loc[is_i])["Sharpe"] for k in cand}
    pick = max(is_sh, key=is_sh.get)
    print(f"IS Sharpe by dial pair: " + ", ".join(f"{k.replace('SCREEN-','')} {v:.4f}" for k, v in is_sh.items()))
    print(f"chosen: {pick}")
    oos = {k: stats(results[k].loc[oos_i]) for k in ["ALWAYS", pick, f"RANDOM-{pick.split('-')[1]}-degross", "NEVER"]}
    oos["SPY"] = stats(spy_t.loc[oos_i])
    base_px = P["u56"]
    oos["RULES v2 (live)"] = stats(run(base_px, rules_v2_weights(base_px)).reindex(oos_i).fillna(0.0))
    O = pd.DataFrame(oos).T[["CAGR", "Sharpe", "MaxDD"]]
    print("\nOOS (" + str(oos_i[0].date()) + " -> " + str(oos_i[-1].date()) + "):")
    print(O.to_string(float_format=lambda x: f"{x:.4f}"))
    d, a = O.loc[pick], O.loc["ALWAYS"]; rm = O.loc[f"RANDOM-{pick.split('-')[1]}-degross"]
    print(f"\nOOS dSharpe screen-ALWAYS {d.Sharpe - a.Sharpe:+.4f} | random-ALWAYS {rm.Sharpe - a.Sharpe:+.4f} "
          f"| screen-RANDOM {d.Sharpe - rm.Sharpe:+.4f}")

    print("\n" + "=" * 96); print("PER-CELL: how often each cell is admitted, and what it earns")
    print("=" * 96)
    rows = []
    for i, c in enumerate(names):
        adm = np.mean([FLAGS[("expanding", y - 1)][i] for y in years if y > first])
        rows.append(dict(cell=c, admitted=adm, CAGR=metrics(R[c].loc[trade])["CAGR"],
                         Sharpe=metrics(R[c].loc[trade])["Sharpe"], MaxDD=metrics(R[c].loc[trade])["MaxDD"]))
    T = pd.DataFrame(rows).sort_values("admitted", ascending=False)
    print(T.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\ncells never admitted: {(T.admitted == 0).sum()}/{len(T)} | always admitted: {(T.admitted == 1).sum()}/{len(T)}")
    print(f"corr(admitted share, realised OOS Sharpe) = {T.admitted.corr(T.Sharpe):+.4f}")
    T.to_csv(ROOT / "research" / "backtests" / "2026-09-08_abstention_cells.csv", index=False)
    out.to_csv(ROOT / "research" / "backtests" / "2026-09-08_abstention_composites.csv")

if __name__ == "__main__":
    main()
