#!/usr/bin/env python3
"""Idea 41: does the breadth gate's CUT DEPTH close idea 40's 0.4pp drawdown miss?

Idea 40's nearest 4b miss was `BREADTH n=3, B=30%`: 21.0% / 1.03 / **-20.6%** against a cap of
-20.23%, passing H1, H2, OOS and the CAGR floor and failing the drawdown cap ALONE by 0.4pp.
Idea 40 halved exposure (depth 0.5) when universe breadth fell below B.  The queue's question is
deliberately narrow: hold B at the PRE-CHOSEN 30% and move the DEPTH of the cut instead, because
tuning B on the same sample that produced the miss would be curve-fitting the failure away.

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. n     positions held        in {3, 5, 8}     (idea 40's own grid)
     2. d     exposure kept while the gate is ON, in {0.5, 0.25, 0.0}
              d = 0.5 reproduces idea 40 EXACTLY (asserted in section [0]); d = 0 is a full
              flight to cash; d = 1.0 is carried as the un-gated control, NOT as a tuned point.
  NOT TUNED: B is pinned at 0.30.  Panel (U56 / B136 / SMALL439) and cost rung (0/10/25 bps) are
  reported axes.  Section [E] sweeps B in {0.25 .. 0.50} as a SENSITIVITY READ ONLY -- no verdict
  anywhere in this file is taken from it, and it is labelled as such at the point of use.

  THE TEST.  4b is a conjunction, so a deeper cut only helps if it buys DD margin faster than it
  spends CAGR and Sharpe margin.  Section [B] prices that exchange directly:
        dDD margin per 1pp of CAGR given up,  measured along the depth axis at fixed n.
  If the ratio is such that the 0.4pp DD gap closes before the CAGR floor or a Sharpe bar breaks,
  depth is the instrument the queue hoped for.  If every depth that closes DD breaks another bar,
  the miss is not a depth problem and idea 40's near-miss is a dead end -- a KILL, and a useful one.

  Book (fixed, idea 40's own, never tuned): eligible = above the 200d MA and vol20 < 0.60; rank
  eligible names by the v1 composite WITHOUT the /sqrt(vol20) term; hold the top n equal-weight at
  w = 0.75/n; weekly; next-day execution.  Breadth = the fraction of the panel's own constituents
  trading above their 200d MA, computed through day t and executed at t+1; the exposure switch pays
  the rung's cost on |d(mult)| * 0.75 of notional on the day it takes effect (idea 40's convention).

  RULE 8 walk-forward: (n, d) chosen on 2008-2016 by IS Sharpe at 10 bps, 2017-2026 read once,
  against idea 40's (n=3, d=0.5) anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.
  Both KEEP paths are evaluated on every grid point: 4a vs the LIVE RULES v2 book, 4b vs SPY.

REPRODUCTION GATES (section [0], asserted or printed before any new number is read):
  * the derived cost rung r(c) = r(0) - turnover*c/1e4 equals engine.backtest(cost_bps=c) to 1e-12;
  * d = 1.0 reproduces idea 40's published un-gated controls: NONE n=3 21.9%/1.04/-25.8% (1.01/1.06),
    n=5 16.5%/0.95/-21.6% (0.90/1.00);
  * d = 0.5 reproduces idea 40's published gated rows: B=30% n=3 21.0%/1.03/-20.6% (0.96/1.09) --
    the near-miss this idea exists to close -- and, on the sensitivity axis, B=40% 19.9%/1.00/-20.9%
    and B=50% 19.4%/0.99/-21.4%.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters every
momentum book; the CAGR and drawdown LEVELS are optimistic and 4b's drawdown cap is exactly a level
test, so the near-miss itself is the number most exposed to this bias.  The small panel is the worst
offender and the 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is run.  (2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as
U56/B136, and its breadth series is computed on a different cross-section.  (3) A gate that only ever
de-grosses cannot raise CAGR (idea 42 measured 0 of 486); this run does not re-litigate that, it asks
only whether the DD it buys is cheap enough.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights, rules_v1_weights          # noqa
from engine import backtest, metrics, rebalance_mask                                   # noqa

SLUG = "2026-09-07_breadth-gate-depth_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, FREQ = 0.60, 0.75, "W"
B_FIXED = 0.30                      # PRE-CHOSEN, never tuned
NS = [3, 5, 8]                      # tuned parameter 1
DEPTHS = [0.5, 0.25, 0.0]           # tuned parameter 2
CONTROL_DEPTH = 1.0                 # un-gated control, not a tuned point
B_SENS = [0.25, 0.30, 0.35, 0.40, 0.50]   # sensitivity axis ONLY (section [E])
COSTS = [0, 10, 25]
ANCHOR_N, ANCHOR_D = 3, 0.5         # idea 40's near-miss cell
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book
def base_weights(px, n, drop_spy=False):
    """Idea 40's OFF book: top-n eligible by the v1 composite WITHOUT /sqrt(vol20), w = GROSS/n."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL)
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    rank = s.where(elig).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def breadth(px, drop_spy=False):
    """Fraction of the panel's own constituents above their 200d MA, computed at each day t.
    On SMALL439 SPY is joined only as a benchmark (see baseline.load_universe) and is excluded."""
    cols = [c for c in px.columns if not (drop_spy and c == "SPY")]
    q = px[cols]
    above = q > q.rolling(200).mean()
    return above.sum(axis=1) / above.notna().sum(axis=1).replace(0, np.nan)


def gate_apply(r_book, br_lag, B, depth, cost_bps):
    """Halve-to-`depth` while breadth is below B.  `br_lag` is already shifted by one day
    (decided at t, executed at t+1).  The switch pays cost_bps on |d(mult)| * GROSS of notional
    on the day it takes effect -- idea 40's convention, reproduced exactly at depth 0.5."""
    on = br_lag.reindex(r_book.index).fillna(False)
    mult = np.where(on.values, depth, 1.0)
    dmult = np.abs(np.diff(np.concatenate([[1.0], mult])))
    out = r_book.values * mult - dmult * GROSS * cost_bps / 1e4
    return pd.Series(out, index=r_book.index), pd.Series(mult, index=r_book.index)


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
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


def breakeven(r0, t0, mult_dmult, spy, hi=200):
    """Largest whole bps at which all five 4b bars hold, with BOTH the book's turnover and the
    gate's own switching cost re-charged at each rung."""
    cstar, bar = None, ""
    for c in range(0, hi + 1):
        r = (r0 - t0 * c / 1e4) - mult_dmult * c / 1e4
        ok, _, f = bars_4b(r, spy)
        if ok:
            cstar = c
        else:
            bar = ",".join(f)
            break
    return cstar, bar


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book (idea 40's OFF book, fixed): top-n eligible by the v1 composite, vol scaler OFF, "
          f"w = {GROSS}/n, weekly, next-day execution.")
    print(f"Gate: exposure -> d while panel breadth < B = {B_FIXED:.0%} (PRE-CHOSEN, not tuned).")
    print(f"Tuned: n in {NS} x d in {DEPTHS}.  Control d={CONTROL_DEPTH} (un-gated, not a tuned "
          f"point).  Reported axes: panel, cost {COSTS} bps.  Section [E] B-sensitivity is NOT a verdict.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv, scsv = (OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv", OUT / f"{SLUG}.bsens.csv")
    if RESUME and gcsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"), pd.read_csv(scsv))
        return

    rows, ctx_rows, sens_rows = [], [], []
    for pname, px in panels.items():
        drop_spy = (pname == "SMALL439")
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        br = breadth(px, drop_spy)
        br_lag_full = br.shift(1)
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        bl = br.loc[start:]
        print(f"    breadth: mean {bl.mean():.3f} min {bl.min():.3f} max {bl.max():.3f} | "
              f"days below B={B_FIXED:.0%}: {int((bl < B_FIXED).sum())} of {len(bl)} "
              f"({(bl < B_FIXED).mean():.1%})")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        print(f"    4b bars on this panel: H1 > {s1:.3f}, H2 > {s2:.3f}, OOS > {so['Sharpe']:.3f}, "
              f"MaxDD <= {0.60*abs(ms_['MaxDD']):.2%}, CAGR >= {0.70*ms_['CAGR']:.2%}")

        bres = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=FREQ)
        br0, bt0 = bres["returns"].loc[start:], bres["turnover"].loc[start:]
        base10 = br0 - bt0 * 10 / 1e4
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")

        # ---- the un-gated books, once per n
        raw = {}
        for n in NS:
            res = backtest(px, base_weights(px, n, drop_spy), cost_bps=0.0, freq=FREQ)
            raw[n] = (res["returns"].loc[start:], res["turnover"].loc[start:])

        if pname == "U56":
            print("\n[0] GATES")
            r0, t0 = raw[3]
            eng10 = backtest(px, base_weights(px, 3), cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
            dmax = np.abs(eng10 - (r0 - t0 * 10 / 1e4)).max()
            print(f"    derived rung r(10) vs live backtest(cost_bps=10): max|d| {dmax:.3e}")
            assert dmax < 1e-12
            PUB = {("NONE", 3): "21.9% / 1.04 / -25.8%, H1/H2 1.01/1.06",
                   ("NONE", 5): "16.5% / 0.95 / -21.6%, H1/H2 0.90/1.00",
                   ("NONE", 8): "(idea 40 control, n=8)",
                   ("B30", 3): "21.0% / 1.03 / -20.6%, H1/H2 0.96/1.09  <-- THE NEAR-MISS"}
            for key, pub in PUB.items():
                n = key[1]
                rr, tt = raw[n]
                rb = rr - tt * 10 / 1e4
                if key[0] == "NONE":
                    r, _ = gate_apply(rb, br_lag_full.loc[start:] < B_FIXED, B_FIXED, 1.0, 10)
                else:
                    r, _ = gate_apply(rb, br_lag_full.loc[start:] < B_FIXED, B_FIXED, 0.5, 10)
                mt = metrics(r); q1, q2 = hs(r)
                print(f"    idea 40 {key[0]:>4} n={n}: {mt['CAGR']:.2%} / {mt['Sharpe']:.3f} / "
                      f"{mt['MaxDD']:.2%}  H1/H2 {q1:.3f}/{q2:.3f}   [published {pub}]")

        # ---- the grid
        print(f"\n[A] GRID {pname}  (d=1.00 is the un-gated CONTROL, not a tuned point; "
              f"B pinned at {B_FIXED:.0%})")
        print(f"    {'n':>2} {'d':>5} {'on%':>5} {'sw/yr':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} "
                           f"{'DDmarg':>7} {'CAGRmarg':>8} 4b 4a" for c in COSTS))
        sig = (br_lag_full < B_FIXED).loc[start:]
        for n in NS:
            r0, t0 = raw[n]
            for d in [CONTROL_DEPTH] + DEPTHS:
                _, mult = gate_apply(r0, sig, B_FIXED, d, 0)
                dmult = pd.Series(np.abs(np.diff(np.concatenate([[1.0], mult.values]))),
                                  index=mult.index) * GROSS
                yrs = len(r0) / 252
                line = (f"    {n:>2} {d:>5.2f} {(mult < 1).mean():>5.1%} "
                        f"{dmult[dmult > 0].count()/yrs:>6.1f} |")
                rec = dict(panel=pname, n=n, depth=d, on_frac=float((mult < 1).mean()),
                           switches_per_yr=float(dmult[dmult > 0].count() / yrs),
                           turn_per_yr=float(t0.sum() / yrs))
                for c in COSTS:
                    r = (r0 - t0 * c / 1e4) * mult - dmult * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, br0 - bt0 * c / 1e4)
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} {d4b['DD']:>+7.2%} "
                             f"{d4b['CAGR']:>+8.2%} {'Y' if ok4b else 'n'}  {'Y' if ok4a else 'n'} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a),
                                f"m4b_H1_{c}": d4b["H1"], f"m4b_H2_{c}": d4b["H2"],
                                f"m4b_OOS_{c}": d4b["OOS"], f"m4b_DD_{c}": d4b["DD"],
                                f"m4b_CAGR_{c}": d4b["CAGR"]})
                cst, cbar = breakeven(r0 * mult, t0 * mult, dmult, spy)
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                print(line + f" c*={rec['breakeven_bps']:>3}")
                rows.append(rec)

        # ---- [E] B sensitivity (REPORTED ONLY, no verdict is taken from it)
        for B in B_SENS:
            sg = (br_lag_full < B).loc[start:]
            for n in NS:
                r0, t0 = raw[n]
                for d in DEPTHS:
                    _, mult = gate_apply(r0, sg, B, d, 0)
                    dmult = pd.Series(np.abs(np.diff(np.concatenate([[1.0], mult.values]))),
                                      index=mult.index) * GROSS
                    r = (r0 - t0 * 10 / 1e4) * mult - dmult * 10 / 1e4
                    mt = metrics(r); ok, dm, f = bars_4b(r, spy)
                    sens_rows.append(dict(panel=pname, B=B, n=n, depth=d, CAGR=mt["CAGR"],
                                          Sharpe=mt["Sharpe"], MaxDD=mt["MaxDD"],
                                          DD_margin=dm["DD"], CAGR_margin=dm["CAGR"],
                                          keep4b=ok, fail=",".join(f)))

        ctx_rows.append(dict(panel=pname, spy_sharpe=ms_["Sharpe"], spy_cagr=ms_["CAGR"],
                             spy_dd=ms_["MaxDD"], spy_h1=s1, spy_h2=s2,
                             spy_oos_sharpe=so["Sharpe"], spy_oos_cagr=so["CAGR"],
                             spy_oos_dd=so["MaxDD"], base_sharpe=bm["Sharpe"],
                             base_cagr=bm["CAGR"], base_dd=bm["MaxDD"],
                             base_oos_sharpe=bo["Sharpe"], base_oos_cagr=bo["CAGR"],
                             base_oos_dd=bo["MaxDD"]))

    df = pd.DataFrame(rows); df.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.to_csv(ccsv)
    sens = pd.DataFrame(sens_rows); sens.to_csv(scsv, index=False)
    analyse(df, ctx, sens)


# ---------------------------------------------------------------- analysis
def analyse(df, ctx, sens):
    # ------------------------------------------------------- [B] the exchange rate
    print("\n\n[B] THE EXCHANGE RATE: what does a deeper cut BUY and what does it COST?")
    print("    Along the depth axis at fixed n (10 bps): dDD margin (pp) and dCAGR (pp) vs the")
    print("    un-gated control d=1.00, and the ratio pp of DD bought per pp of CAGR given up.")
    print(f"    {'panel':9s} {'n':>2} {'d':>5} {'dDD (pp)':>9} {'dCAGR (pp)':>11} {'pp DD / pp CAGR':>16} "
          f"{'dSharpe':>8} {'DD margin':>10} {'CAGR margin':>12} {'4b':>3}")
    ex = []
    for pname in df.panel.unique():
        for n in NS:
            d0 = df[(df.panel == pname) & (df.n == n)]
            ctrl = d0[d0.depth == CONTROL_DEPTH].iloc[0]
            for d in DEPTHS:
                r = d0[d0.depth == d].iloc[0]
                dDD = (abs(ctrl.MaxDD_10) - abs(r.MaxDD_10)) * 100          # pp of DD bought
                dC = (ctrl.CAGR_10 - r.CAGR_10) * 100                       # pp of CAGR given up
                ratio = dDD / dC if abs(dC) > 1e-9 else float("nan")
                print(f"    {pname:9s} {n:>2} {d:>5.2f} {dDD:>+9.2f} {dC:>+11.2f} {ratio:>16.2f} "
                      f"{r.Sharpe_10-ctrl.Sharpe_10:>+8.3f} {r.m4b_DD_10:>+10.2%} "
                      f"{r.m4b_CAGR_10:>+12.2%} {'Y' if r.keep4b_10 else 'n':>3}")
                ex.append(dict(panel=pname, n=n, depth=d, dDD_pp=dDD, dCAGR_pp=dC, ratio=ratio,
                               dSharpe=r.Sharpe_10 - ctrl.Sharpe_10, DD_margin=r.m4b_DD_10,
                               CAGR_margin=r.m4b_CAGR_10, keep4b=bool(r.keep4b_10)))
    exd = pd.DataFrame(ex); exd.to_csv(OUT / f"{SLUG}.exchange.csv", index=False)
    good = exd[exd.dCAGR_pp > 0]
    print(f"    ratio across the {len(good)} cells where depth actually costs CAGR: median "
          f"{good.ratio.median():.2f}, range {good.ratio.min():.2f} .. {good.ratio.max():.2f} pp DD per pp CAGR")
    print("    READ: 4b needs the DD margin to reach 0 BEFORE the CAGR margin falls through it.")

    # ------------------------------------------------------- [C] does depth close the miss?
    print("\n[C] THE QUESTION: does DEPTH close idea 40's 0.4pp drawdown miss at n=3, B=30%?")
    a = df[(df.panel == "U56") & (df.n == ANCHOR_N)].sort_values("depth", ascending=False)
    print(f"    {'d':>5} {'CAGR':>8} {'Sharpe':>7} {'MaxDD':>8} {'H1/H2':>14} {'OOS':>6} "
          f"{'DD margin':>10} {'CAGR margin':>12} {'4b':>3} {'failing bars':>16}")
    for _, r in a.iterrows():
        print(f"    {r.depth:>5.2f} {r.CAGR_10:>8.2%} {r.Sharpe_10:>7.3f} {r.MaxDD_10:>8.2%} "
              f"{r.H1_10:>6.3f}/{r.H2_10:<7.3f} {r.OOS_Sharpe_10:>6.3f} {r.m4b_DD_10:>+10.2%} "
              f"{r.m4b_CAGR_10:>+12.2%} {'Y' if r.keep4b_10 else 'n':>3} {str(r.fail4b_10):>16}")
    closed = a[(a.depth < CONTROL_DEPTH) & (a.m4b_DD_10 >= 0)]
    print(f"    depths that CLOSE the drawdown cap at n=3: "
          f"{', '.join(f'{d:.2f}' for d in closed.depth) if len(closed) else 'NONE'}")
    print(f"    of those, depths that clear ALL FIVE 4b bars: "
          f"{', '.join(f'{r.depth:.2f}' for _, r in closed.iterrows() if r.keep4b_10) or 'NONE'}")

    # ------------------------------------------------------- [D] census
    print("\n[D] KEEP-path census over the whole grid (36 cells: 3 panels x 3 n x 4 depths incl. control)")
    for c in COSTS:
        t = df[df.depth != CONTROL_DEPTH]
        print(f"    c={c:>2} bps: 4b {int(df[f'keep4b_{c}'].sum())}/{len(df)} "
              f"(gated only {int(t[f'keep4b_{c}'].sum())}/{len(t)}, "
              f"controls {int(df[df.depth==CONTROL_DEPTH][f'keep4b_{c}'].sum())}/"
              f"{len(df[df.depth==CONTROL_DEPTH])})   4a {int(df[f'keep4a_{c}'].sum())}/{len(df)}")
    fails = {}
    for _, r in df.iterrows():
        for k in str(r["fail4b_10"]).split(","):
            if k:
                fails[k] = fails.get(k, 0) + 1
    print("    binding 4b bars at 10 bps:", ", ".join(f"{k} {v}/{len(df)}" for k, v in
                                                      sorted(fails.items(), key=lambda x: -x[1])))
    for c in COSTS:
        k = df[df[f"keep4b_{c}"]]
        if k.empty:
            print(f"    4b passes at {c} bps: none")
        else:
            print(f"    4b passes at {c} bps:")
            for _, r in k.iterrows():
                print(f"      {r.panel:9s} n={int(r.n)} d={r.depth:.2f} {r[f'CAGR_{c}']:.2%} / "
                      f"{r[f'Sharpe_{c}']:.3f} / {r[f'MaxDD_{c}']:.2%} H1/H2 {r[f'H1_{c}']:.3f}/"
                      f"{r[f'H2_{c}']:.3f} OOS {r[f'OOS_Sharpe_{c}']:.3f} c*={int(r.breakeven_bps)}")
    print("\n    DD margin of the GATED cells vs their own un-gated control (10 bps), all panels:")
    print(f"    {'panel':9s} {'n':>2} | " + " ".join(f"{'d='+format(d,'.2f'):>12}" for d in
                                                     [CONTROL_DEPTH] + DEPTHS))
    for pname in df.panel.unique():
        for n in NS:
            d0 = df[(df.panel == pname) & (df.n == n)]
            cells = " ".join(f"{d0[d0.depth==d].iloc[0].m4b_DD_10:>+12.2%}"
                             for d in [CONTROL_DEPTH] + DEPTHS)
            print(f"    {pname:9s} {n:>2} | {cells}")

    # ------------------------------------------------------- [E] B sensitivity (NOT a verdict)
    print(f"\n[E] SENSITIVITY ONLY -- B swept over {B_SENS}; NO verdict in this file is taken from")
    print("    this section.  It exists to say whether the section [C] answer is B-specific.")
    print(f"    4b passes at 10 bps by B: " + ", ".join(
        f"B={B:.0%}: {int(sens[(sens.B==B)].keep4b.sum())}/{len(sens[sens.B==B])}" for B in B_SENS))
    print(f"    cells whose DD margin is >= 0 by B: " + ", ".join(
        f"B={B:.0%}: {int((sens[sens.B==B].DD_margin >= 0).sum())}" for B in B_SENS))
    hit = sens[sens.keep4b]
    if not hit.empty:
        print("    every 4b pass on the sensitivity axis (reported, NOT adopted):")
        for _, r in hit.iterrows():
            print(f"      {r.panel:9s} B={r.B:.0%} n={int(r.n)} d={r.depth:.2f} {r.CAGR:.2%} / "
                  f"{r.Sharpe:.3f} / {r.MaxDD:.2%}")

    # ------------------------------------------------------- [F] rule 8 walk-forward
    print("\n[F] RULE 8 WALK-FORWARD: (n, d) chosen on IS <= 2016 by Sharpe @10 bps, OOS 2017+ "
          "read once.  The control d=1.00 is INSIDE the chooser's menu (it is a legitimate choice).")
    wf = []
    for pname in df.panel.unique():
        d0 = df[df.panel == pname]
        pick = d0.loc[d0["IS_Sharpe_10"].idxmax()]
        best = d0.loc[d0["OOS_Sharpe_10"].idxmax()]
        anch = d0[(d0.n == ANCHOR_N) & (d0.depth == ANCHOR_D)].iloc[0]
        cx = ctx.loc[pname]
        print(f"\n    --- {pname}")
        print(f"    {'arm':32s} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for lab, r in [(f"IS-chosen n={int(pick.n)} d={pick.depth:.2f}", pick),
                       (f"idea 40 anchor n=3 d=0.50", anch),
                       (f"OOS-best n={int(best.n)} d={best.depth:.2f}", best)]:
            print(f"    {lab:32s} {r.OOS_CAGR_10:>9.2%} {r.OOS_Sharpe_10:>11.3f} {r.OOS_MaxDD_10:>10.2%}")
        print(f"    {'RULES v2 (live)':32s} {cx.base_oos_cagr:>9.2%} {cx.base_oos_sharpe:>11.3f} "
              f"{cx.base_oos_dd:>10.2%}")
        print(f"    {'SPY':32s} {cx.spy_oos_cagr:>9.2%} {cx.spy_oos_sharpe:>11.3f} {cx.spy_oos_dd:>10.2%}")
        print(f"    regret (IS-chosen - OOS-best) {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.4f}; "
              f"vs the idea 40 anchor {pick.OOS_Sharpe_10-anch.OOS_Sharpe_10:+.4f}; "
              f"chooser picks {'a GATED' if pick.depth < 1 else 'the UN-GATED'} cell")
        wf.append(dict(panel=pname, pick_n=int(pick.n), pick_depth=pick.depth,
                       pick_oos_sharpe=pick.OOS_Sharpe_10, pick_oos_cagr=pick.OOS_CAGR_10,
                       pick_oos_dd=pick.OOS_MaxDD_10, anchor_oos_sharpe=anch.OOS_Sharpe_10,
                       best_n=int(best.n), best_depth=best.depth,
                       best_oos_sharpe=best.OOS_Sharpe_10, spy_oos_sharpe=cx.spy_oos_sharpe,
                       base_oos_sharpe=cx.base_oos_sharpe))
    w = pd.DataFrame(wf); w.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\n    chooser picks a GATED cell on {int((w.pick_depth < 1).sum())} of {len(w)} panels; "
          f"beats the idea 40 anchor OOS on {int((w.pick_oos_sharpe > w.anchor_oos_sharpe).sum())}/{len(w)}, "
          f"SPY on {int((w.pick_oos_sharpe > w.spy_oos_sharpe).sum())}/{len(w)}, "
          f"the live book on {int((w.pick_oos_sharpe > w.base_oos_sharpe).sum())}/{len(w)}")
    print(f"\nwrote {SLUG}.grid.csv ({len(df)} rows), .exchange.csv, .bsens.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
