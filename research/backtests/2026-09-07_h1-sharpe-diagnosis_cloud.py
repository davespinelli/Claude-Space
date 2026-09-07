#!/usr/bin/env python3
"""Idea 43: H1-SHARPE DIAGNOSIS — is the first-half Sharpe bar a 2009-10 beta miss or a regime failure,
and is PROTOCOL 4b reachable at all on this universe?

The queue's premise: "H1 (2009-2017) Sharpe vs SPY's 0.957 is the single binding 4b constraint in
ideas 24, 25, 28 and 40."  Two things are tested, in this order:

  [P] IS THE PREMISE STILL TRUE?  Ideas 24/25/28/40 are pre-index-fix rows (QUEUE 38/39).  The
      flagged family is re-run from scratch -- EWALL (equal weight over every eligible name) and
      the ranked top-n book -- and the BINDING 4b bar is read off each cell.  If H1 is no longer
      the bar that fails, the premise is dead and the diagnosis has to be re-aimed at whatever bar
      does bind.  Reported, not asserted.

  [Y] THE DECOMPOSITION THE QUEUE ASKED FOR.  For each book:
      - per-calendar-year returns, vol, Sharpe, realised beta and alpha vs SPY, and the mean
        invested gross (the trend gate's exposure channel);
      - LEAVE-ONE-YEAR-OUT on the first half: recompute the H1 Sharpe gap with each year deleted.
        A "2009-10 beta miss" means deleting 2009 and/or 2010 flips the gap's sign; a regime
        failure means no single year does;
      - the gap split into its two arithmetic channels,
            S_b - S_s = (mu_b - mu_s)/sig_b   +   mu_s * (1/sig_b - 1/sig_s)
        i.e. a RETURN shortfall term and a VOL term, plus the vol-matched counterfactual Sharpe.
      A key arithmetic fact is used throughout and asserted in [0]: an unlevered cash-blend book's
      Sharpe is invariant to the gross dial, so the H1 gap CANNOT be closed by taking more
      exposure -- "the book misses 2009-10 beta" is a statement about CORRELATION and TIMING, not
      about position size.

  [R] IS 4b REACHABLE?  Census over the whole grid x 3 panels x 3 cost rungs: how many cells clear
      the H1 bar alone, how many clear all five, and what the best achievable H1 Sharpe is.

Two tuned parameters, no more:
    1. n     in {5, 10, 20, 40, ALL}     position count (ALL = EWALL, ideas 24/25/28/40's book)
    2. gross in {0.75, 0.85, 1.00}       idea 28's own three-gross ask
Panel (U56 / B136 / SMALL439) and cost rung (0/10/25) are reported axes, not tuned choices; every
point of every axis is printed and written to `<slug>.grid.csv`.

Rule 8 walk-forward: (n, gross) chosen on 2008-2016 by IS Sharpe, 2017-2026 read once, against the
anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters every
momentum book; the small panel is the worst offender and the 44 tickers with `max_1d_move >= 1.0`
in data/small_meta.csv are dropped before anything is run.  (2) SMALL439 starts 2010-01-04, so it
has no 2009 and cannot speak to the 2009-10 question -- it is carried as a regime control only.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_h1-sharpe-diagnosis_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, FREQ = 0.60, "W"
NS = [5, 10, 20, 40, "ALL"]
GROSSES = [0.75, 0.85, 1.00]
COSTS = [0, 10, 25]
ANCHOR_N, ANCHOR_G = "ALL", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def rank_frame(px, drop_spy=False):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def weights_for(rk, n, g):
    sel = (rk.notna() if n == "ALL" else (rk <= n)).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return g * sel.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    """Vectorised-loop clone of engine.backtest; asserted against it in section [0]."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(np.nansum(held, axis=1), index=idx))


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def gap_channels(rb, rs):
    """S_b - S_s = (mu_b - mu_s)/sig_b + mu_s*(1/sig_b - 1/sig_s).  Returns both terms and the
    vol-matched counterfactual Sharpe (the book's mean carried at SPY's vol)."""
    mb, ms = rb.mean() * 252, rs.mean() * 252
    sb, ss = rb.std() * np.sqrt(252), rs.std() * np.sqrt(252)
    return (mb - ms) / sb, ms * (1 / sb - 1 / ss), mb / ss


def main():
    print(f"=== {SLUG}")
    print("Books: EWALL (n=ALL) and top-n by the v1 composite (vol scaler OFF), NORM weights g/k_t, "
          "weekly, next-day execution, RULES v1 eligibility (above 200d MA, vol20 < 0.60).")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    rows, yearly, loyo, ctx_rows = [], [], [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        half = len(spy) // 2
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, eval {start.date()} -> "
              f"{px.index[-1].date()}  (H1 = {spy.index[0].date()}..{spy.index[half-1].date()}, "
              f"H2 = {spy.index[half].date()}..)")
        print(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")

        br, bt, _ = fast_backtest(px, rules_v2_weights(px), 0.0)
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")
        ctx_rows.append(dict(panel=pname, spy_h1=s1, spy_h2=s2, spy_oos_sharpe=so["Sharpe"],
                             spy_oos_cagr=so["CAGR"], spy_oos_dd=so["MaxDD"],
                             base_h1=b1, base_h2=b2, base_oos_sharpe=bo["Sharpe"],
                             base_oos_cagr=bo["CAGR"], base_oos_dd=bo["MaxDD"]))

        if pname == "U56":
            print("\n[0] GATES")
            w = weights_for(rk, 20, 0.75)
            eng = backtest(px, w, cost_bps=0.0, freq=FREQ)
            f_r, f_t, _ = fast_backtest(px, w, 0.0)
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            e25 = backtest(px, w, cost_bps=25.0, freq=FREQ)
            d3 = np.abs(e25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    derived rung r(25) vs live backtest(25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            # gross-invariance of Sharpe (the claim [Y] leans on), measured not assumed
            sA = metrics(fast_backtest(px, weights_for(rk, 20, 0.75), 10.0)[0].loc[start:])["Sharpe"]
            sB = metrics(fast_backtest(px, weights_for(rk, 20, 1.00), 10.0)[0].loc[start:])["Sharpe"]
            print(f"    Sharpe at gross 0.75 vs 1.00 (top-20, 10 bps): {sA:.4f} vs {sB:.4f} "
                  f"(span {abs(sA-sB):.4f}) -- exposure cannot close a Sharpe gap")

        # ------------------------------------------------ grid
        print(f"\n[P] GRID {pname} — every cell, with the BINDING 4b bar named")
        print(f"    {'n':>4} {'g':>5} {'turn':>6} | " + " | ".join(
            f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1':>6} {'H2':>6} {'OOS':>6} "
            f"{'4b':>2} {'fails':<14} 4a" for c in COSTS))
        for n in NS:
            for g in GROSSES:
                r0, t0, gr = fast_backtest(px, weights_for(rk, n, g), 0.0)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                line = f"    {str(n):>4} {g:>5.2f} {tpy:>6.2f} |"
                rec = dict(panel=pname, n=str(n), gross=g, turn_per_yr=tpy)
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, _, _ = bars_4a(r, (br - bt * c / 1e4).loc[start:])
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f} {h2:>6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n':>2} {','.join(f4b):<14} {'Y' if ok4a else 'n'} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a,
                                **{f"m4b_{k}_{c}": v for k, v in d4b.items()}})
                print(line)
                rows.append(rec)

        # ------------------------------------------------ [Y] year decomposition, anchor books
        for n in ["ALL", 20]:
            r0, t0, gr = fast_backtest(px, weights_for(rk, n, 0.75), 0.0)
            r = (r0 - t0 * 10 / 1e4).loc[start:]
            gr = gr.loc[start:]
            h1, h2 = hs(r)
            print(f"\n[Y] {pname} / n={n} / g=0.75 / 10 bps — per-year decomposition "
                  f"(book H1 {h1:.3f} vs SPY H1 {s1:.3f}, gap {h1-s1:+.3f})")
            print(f"    {'year':>5} {'bookRet':>8} {'spyRet':>8} {'bookVol':>8} {'spyVol':>7} "
                  f"{'bookShrp':>9} {'spyShrp':>8} {'beta':>6} {'alpha':>7} {'gross':>6} {'elig%':>6}")
            for y, rr in r.groupby(r.index.year):
                ss = spy.loc[rr.index]
                cov = np.cov(rr.values, ss.values)
                beta = cov[0, 1] / cov[1, 1] if cov[1, 1] else np.nan
                alpha = (rr.mean() - beta * ss.mean()) * 252
                ep = elig.loc[rr.index].sum(axis=1).mean() / (px.shape[1] - 1)
                print(f"    {y:>5} {(1+rr).prod()-1:>8.2%} {(1+ss).prod()-1:>8.2%} "
                      f"{rr.std()*np.sqrt(252):>8.2%} {ss.std()*np.sqrt(252):>7.2%} "
                      f"{sharpe(rr):>9.3f} {sharpe(ss):>8.3f} {beta:>6.2f} {alpha:>7.2%} "
                      f"{gr.loc[rr.index].mean():>6.3f} {ep:>6.1%}")
                yearly.append(dict(panel=pname, n=str(n), year=int(y), book_ret=(1+rr).prod()-1,
                                   spy_ret=(1+ss).prod()-1, book_vol=rr.std()*np.sqrt(252),
                                   spy_vol=ss.std()*np.sqrt(252), book_sharpe=sharpe(rr),
                                   spy_sharpe=sharpe(ss), beta=beta, alpha=alpha,
                                   gross=gr.loc[rr.index].mean(), elig_share=ep))

            hlen = len(r) // 2
            rH, sH = r.iloc[:hlen], spy.iloc[:hlen]
            t_ret, t_vol, cf = gap_channels(rH, sH)
            print(f"    H1 gap {sharpe(rH)-sharpe(sH):+.4f} = RETURN term {t_ret:+.4f} + VOL term "
                  f"{t_vol:+.4f} | vol-matched counterfactual Sharpe {cf:.3f} vs SPY {sharpe(sH):.3f}")
            print(f"    LEAVE-ONE-YEAR-OUT on H1 (gap with that year deleted; sign flip = that year "
                  f"is the whole story):")
            base_gap = sharpe(rH) - sharpe(sH)
            for y in sorted(set(rH.index.year)):
                keep = rH.index.year != y
                g2 = sharpe(rH[keep]) - sharpe(sH[keep])
                flag = "  <-- FLIPS" if (g2 > 0) != (base_gap > 0) else ""
                print(f"      drop {y}: gap {g2:+.4f} (d {g2-base_gap:+.4f}){flag}")
                loyo.append(dict(panel=pname, n=str(n), drop_year=int(y), gap=g2,
                                 base_gap=base_gap, flips=(g2 > 0) != (base_gap > 0)))
            for lab, mask in [("drop 2009+2010", ~np.isin(rH.index.year, [2009, 2010])),
                              ("2009+2010 only", np.isin(rH.index.year, [2009, 2010]))]:
                if mask.sum() > 60:
                    print(f"      {lab}: book {sharpe(rH[mask]):.3f} vs SPY {sharpe(sH[mask]):.3f} "
                          f"-> gap {sharpe(rH[mask])-sharpe(sH[mask]):+.4f}")

    df = pd.DataFrame(rows); df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    pd.DataFrame(yearly).to_csv(OUT / f"{SLUG}.yearly.csv", index=False)
    pd.DataFrame(loyo).to_csv(OUT / f"{SLUG}.loyo.csv", index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel")

    # ---------------------------------------------------------- [P] premise census
    print("\n\n[P] IS THE QUEUE'S PREMISE STILL TRUE?  binding-bar census over the grid")
    for c in COSTS:
        cnt = {}
        for _, r in df.iterrows():
            for k in str(r[f"fail4b_{c}"]).split(","):
                if k:
                    cnt[k] = cnt.get(k, 0) + 1
        h1only = sum(1 for _, r in df.iterrows() if str(r[f"fail4b_{c}"]) == "H1")
        print(f"    c={c:>2} bps: 4b {int(df[f'keep4b_{c}'].sum())}/{len(df)}  "
              f"4a {int(df[f'keep4a_{c}'].sum())}/{len(df)}  | failing bars: "
              + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items(), key=lambda x: -x[1]))
              + f"  | H1 is the SOLE failing bar in {h1only}/{len(df)}")
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        print(f"    {pname:9s} best H1 Sharpe @10 bps {d['H1_10'].max():.3f} vs SPY H1 "
              f"{ctx.loc[pname,'spy_h1']:.3f} (margin {d['H1_10'].max()-ctx.loc[pname,'spy_h1']:+.3f}); "
              f"H1 bar cleared by {int((d['m4b_H1_10']>0).sum())}/{len(d)} cells")

    # ---------------------------------------------------------- [R] reachability
    print("\n[R] IS 4b REACHABLE ON THIS UNIVERSE? (10 bps)")
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        n_pass = int(d["keep4b_10"].sum())
        print(f"    {pname:9s} 4b {n_pass}/{len(d)}", end="")
        if n_pass:
            b = d[d["keep4b_10"]].sort_values("Sharpe_10", ascending=False).iloc[0]
            print(f"  best: n={b.n} g={b.gross} {b.CAGR_10:.2%} / {b.Sharpe_10:.3f} / "
                  f"{b.MaxDD_10:.2%} H1/H2 {b.H1_10:.3f}/{b.H2_10:.3f} OOS {b.OOS_Sharpe_10:.3f}")
        else:
            w = d.loc[d[["m4b_H1_10", "m4b_H2_10", "m4b_OOS_10", "m4b_DD_10",
                         "m4b_CAGR_10"]].min(axis=1).idxmax()]
            print(f"  closest: n={w.n} g={w.gross}, worst bar margin "
                  f"{w[['m4b_H1_10','m4b_H2_10','m4b_OOS_10','m4b_DD_10','m4b_CAGR_10']].min():+.4f} "
                  f"(fails {w.fail4b_10})")

    # ---------------------------------------------------------- [D] rule 8
    print("\n[D] RULE 8 WALK-FORWARD: (n, gross) chosen on IS <= 2016 by Sharpe, OOS 2017+ read once "
          "(10 bps)")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        pick = d.loc[d["IS_Sharpe_10"].idxmax()]
        best = d.loc[d["OOS_Sharpe_10"].idxmax()]
        anch = d[(d.n == str(ANCHOR_N)) & (d.gross == ANCHOR_G)].iloc[0]
        cx = ctx.loc[pname]
        print(f"\n    --- {pname}")
        print(f"    {'arm':30s} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for lab, r in [(f"IS-chosen n={pick.n} g={pick.gross}", pick),
                       (f"anchor n=ALL g=0.75", anch),
                       (f"OOS-best n={best.n} g={best.gross}", best)]:
            print(f"    {lab:30s} {r.OOS_CAGR_10:>9.2%} {r.OOS_Sharpe_10:>11.3f} "
                  f"{r.OOS_MaxDD_10:>10.2%}")
        print(f"    {'RULES v2 (live)':30s} {cx.base_oos_cagr:>9.2%} {cx.base_oos_sharpe:>11.3f} "
              f"{cx.base_oos_dd:>10.2%}")
        print(f"    {'SPY':30s} {cx.spy_oos_cagr:>9.2%} {cx.spy_oos_sharpe:>11.3f} "
              f"{cx.spy_oos_dd:>10.2%}")
        print(f"    regret (IS-chosen - OOS-best) {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.4f}; "
              f"IS-chosen - anchor {pick.OOS_Sharpe_10-anch.OOS_Sharpe_10:+.4f}")
        wf.append(dict(panel=pname, pick_n=pick.n, pick_g=pick.gross,
                       pick_oos_sharpe=pick.OOS_Sharpe_10, pick_oos_cagr=pick.OOS_CAGR_10,
                       pick_oos_dd=pick.OOS_MaxDD_10, anchor_oos_sharpe=anch.OOS_Sharpe_10,
                       best_n=best.n, best_g=best.gross, best_oos_sharpe=best.OOS_Sharpe_10,
                       spy_oos_sharpe=cx.spy_oos_sharpe, base_oos_sharpe=cx.base_oos_sharpe))
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\nwrote {SLUG}.grid.csv ({len(df)} rows), .yearly.csv, .loyo.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
