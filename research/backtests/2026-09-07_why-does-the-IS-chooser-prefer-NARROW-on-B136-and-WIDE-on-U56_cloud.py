#!/usr/bin/env python3
"""Idea 385: why does the IS chooser prefer NARROW on B136 and WIDE on U56?

Idea 333's rule-8 pick, same family, same window, same two dials, is n=10 g=0.75 on B136 (OOS
0.781, regret +0.266, fails 4b) and n=20 g=0.75 on U56 (OOS 1.131, regret +0.005).  The queue's
hypothesis is that the split is a property of the ONE 2008-2016 IS window -- specifically the
2009-2013 momentum run -- rather than a property of the panels.  If so, re-choosing on rolling
5-year IS blocks should make each panel's preferred WIDTH flip from block to block, and the
B136-narrow / U56-wide contrast should not survive as a stable ordering.

THE FAMILY (idea 333's, unchanged, nothing added): top-n of the RULES v1 composite with the vol
scaler OFF among v1-eligible names (200d MA up, vol20 < 0.60), NORM weights w_i = g/k_t, hard cut
(m = 0), WEEKLY cadence, next-day execution.
    THE TWO TUNED PARAMETERS, and the only two: n in {10, 20, 40, 80, ALL} x g in {0.375, 0.50,
    0.625, 0.75} = 20 points per panel, every one reported.  Cost 10 bps is PROTOCOL's; 0 and 25
    are reported rungs, not choices.  Panel is a reported axis.

THE TEST, pre-registered:

  [A] ROLLING IS BLOCKS.  For every 5-calendar-year block inside a panel's evaluation sample,
      re-run idea 333's chooser -- argmax IS Sharpe over the same 20 points at 10 bps -- and
      record the pick.  Report, per panel: the distribution of pick_n, the FLIP RATE (share of
      consecutive blocks whose pick_n differs), and how often B136's pick is strictly narrower
      than U56's on the SAME block, which is the queue's claim stated as an ordering.

  [B] IS IT THE 2009-2013 MOMENTUM RUN?  Blocks are split by whether they overlap 2009-2013 by
      >= 3 years.  If the queue's mechanism is right, the B136-narrow pick lives in the
      overlapping blocks and dies outside them.

  [C] IS THE PREFERENCE EVEN REAL?  Two readings, because a chooser that reads noise flips for
      free.  (C1) the MARGIN: IS Sharpe of the pick minus IS Sharpe of the n=20 cell at the same
      gross, per block -- how much the chooser thinks width is worth.  (C2) does it PAY: each
      block's pick is evaluated on the NEXT 3 years (out-of-block, never seen by the chooser)
      against the fixed n=20 g=0.75 anchor and the block's own out-of-block best.  A preference
      that flips AND does not pay is a noise reading, whatever its mechanism.

  [D] RULE 8, PROTOCOL's own form: (n, g) chosen on 2008-2016 IS Sharpe at 10 bps, 2017-2026 read
      ONCE, against the anchor (n=20, g=0.75), the OOS-best cell (regret), RULES v2 (live) and
      SPY.  Both KEEP paths evaluated at every grid point and every cost rung.

REPRODUCTION GATES (section [0], asserted before any new number is read):
  * fast_backtest == engine.backtest to 1e-12 on returns AND turnover;
  * the derived cost rung r(c) = r(0) - turnover*c/1e4 == engine.backtest(cost_bps=c) to 1e-12;
  * idea 333's COMMITTED walk-forward rows: B136 pick n=10 g=0.75, IS 1.055860, OOS 0.780593;
    U56 pick n=20 g=0.75, IS 0.975940, OOS 1.130697; SMALL439 n=20 g=0.75, OOS 0.465731;
  * idea 333's COMMITTED B136 grid rows at g=0.75 and 10 bps, which are also idea 329's W m=0
    cells: n=20 reads 12.99% / 0.943 / -20.05%, H1/H2 1.1048/0.8025, IS 1.022604.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; a chooser study is less exposed than a level claim, but the 2009-2013 block
is exactly where survivorship is strongest, so a narrow-book preference there is the most
suspect number in this run.  The 44 tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped from the small panel first.  (2) SMALL439 starts 2010-01-04, so it has fewer blocks and
none covering 2009.  (3) The first block of U56/B136 begins at the panel's evaluation start
(2009-01-13), ~8 trading days into 2009; every later block is a full calendar span.
(4) Out-of-block windows at the end of the sample are truncated by the data (last close
2026-09-04); blocks with under 2 years of follow-on are not scored in [C2].

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_why-does-the-IS-chooser-prefer-NARROW-on-B136-and-WIDE-on-U56_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL = 0.60
NS = [10, 20, 40, 80, "ALL"]
GROSSES = [0.375, 0.50, 0.625, 0.75]
COSTS = [0, 10, 25]
COST = 10.0
ANCHOR_N, ANCHOR_G = 20, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
BLOCK_YEARS = 5
FOLLOW_YEARS = 3
MOM_RUN = (2009, 2013)          # the queue's proposed mechanism


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book
def rank_frame(px, drop_spy=False):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def weights_top_n(rk, n, gross):
    """n == 'ALL' holds every eligible name; it nests eligible-equal-weight at the same gross."""
    s = (rk.notna() if n == "ALL" else (rk <= n)).astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, w, cadence="W"):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, cadence).shift(1, fill_value=False).values
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
    return (pd.Series(np.nansum(held * rets, axis=1), index=px.index),
            pd.Series(turn, index=px.index))


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
    d = {"H1": h1 - b1, "H2": h2 - b2,
         "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def sharpe(r):
    return metrics(r)["Sharpe"] if len(r) > 20 else np.nan


# ---------------------------------------------------------------- [0] gates
def gates(panels, series):
    print("\n[0] REPRODUCTION GATES")
    px = panels["U56"]
    rk, _ = rank_frame(px)
    w = weights_top_n(rk, 20, 0.75)
    r0, t0 = fast_backtest(px, w)
    e0 = backtest(px, w, cost_bps=0.0, freq="W")
    e25 = backtest(px, w, cost_bps=25.0, freq="W")
    d_ret = float(np.abs(r0 - e0["returns"]).max())
    d_turn = float(np.abs(t0 - e0["turnover"]).max())
    d_rung = float(np.abs((r0 - t0 * 25 / 1e4) - e25["returns"]).max())
    print(f"    fast_backtest vs engine.backtest : returns {d_ret:.3e}  turnover {d_turn:.3e}")
    print(f"    derived rung r(25) vs engine(25) : {d_rung:.3e}")
    assert d_ret < 1e-12 and d_turn < 1e-12 and d_rung < 1e-12

    wf = pd.read_csv(OUT / "2026-09-07_does-the-B136-drawdown-cap-admit-any-top-n-book_C.walkforward.csv")
    g333 = pd.read_csv(OUT / "2026-09-07_does-the-B136-drawdown-cap-admit-any-top-n-book_C.grid.csv")
    for panel, want_n, want_g, want_is, want_oos in (
            ("B136", "10", 0.75, 1.055860, 0.780593),
            ("U56", "20", 0.75, 0.975940, 1.130697),
            ("SMALL439", "20", 0.75, 0.423147, 0.465731)):
        key = {"SMALL439": "SMALL439"}.get(panel, panel)
        row = wf[wf.panel == panel].iloc[0]
        mine = series[key][(str(want_n), want_g)]
        r = mine["r10"]
        got_is, got_oos = sharpe(r.loc[:IS_END]), sharpe(r.loc[OOS_START:])
        print(f"    idea 333 {panel:<8} n={want_n:<3} g={want_g}: IS {got_is:.6f} (pub "
              f"{want_is:.6f})  OOS {got_oos:.6f} (pub {want_oos:.6f})   [its own pick "
              f"n={row.pick_n} g={row.pick_gross}]")
        assert abs(got_is - want_is) < 1e-4 and abs(got_oos - want_oos) < 1e-4

    row = g333[(g333.panel == "B136") & (g333.n == "20") & (g333.gross == 0.75)].iloc[0]
    r = series["B136"][("20", 0.75)]["r10"]
    m = metrics(r); h1, h2 = hs(r)
    print(f"    idea 333 B136 n=20 g=0.75 @10bps: CAGR {m['CAGR']:.4%} (pub {row.CAGR_10:.4%})  "
          f"Sharpe {m['Sharpe']:.6f} (pub {row.Sharpe_10:.6f})  MaxDD {m['MaxDD']:.4%} "
          f"(pub {row.MaxDD_10:.4%})  H1/H2 {h1:.4f}/{h2:.4f} (pub {row.H1_10:.4f}/{row.H2_10:.4f})")
    assert abs(m["CAGR"] - row.CAGR_10) < 1e-6 and abs(m["Sharpe"] - row.Sharpe_10) < 1e-6
    assert abs(m["MaxDD"] - row.MaxDD_10) < 1e-6 and abs(h2 - row.H2_10) < 1e-6
    print("    ALL GATES PASS")


# ---------------------------------------------------------------- build every book once
def build(panels):
    """One backtest per (panel, n, gross) at zero cost; every rung and every window is a slice."""
    series, meta = {}, {}
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        br, bt = fast_backtest(px, rules_v2_weights(px))
        base = (br - bt * COST / 1e4).loc[start:]
        meta[pname] = dict(start=start, spy=spy, base=base, elig=elig)
        d = {}
        for n in NS:
            for g in GROSSES:
                w = weights_top_n(rk, n, g)
                r0, t0 = fast_backtest(px, w)
                d[(str(n), g)] = dict(r0=r0.loc[start:], t0=t0.loc[start:],
                                      r10=(r0 - t0 * COST / 1e4).loc[start:])
        series[pname] = d
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        bm = metrics(base); b1, b2 = hs(base)
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, eval from {start.date()} "
              f"-> {px.index[-1].date()}, eligible/day mean {elig.sum(axis=1).loc[start:].mean():.1f}")
        print(f"    SPY  CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f}")
        print(f"    RULES v2 (live, W, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe "
              f"{metrics(base.loc[OOS_START:])['Sharpe']:.3f}")
    return series, meta


def full_grid(series, meta):
    rows = []
    for pname, d in series.items():
        spy, base = meta[pname]["spy"], meta[pname]["base"]
        for (n, g), s in d.items():
            row = dict(panel=pname, n=n, gross=g,
                       turn_yr=s["t0"].sum() / (len(s["t0"]) / 252))
            for c in COSTS:
                r = s["r0"] - s["t0"] * c / 1e4
                m = metrics(r); h1, h2 = hs(r); mo = metrics(r.loc[OOS_START:])
                ok4b, d4b, f4b = bars_4b(r, spy)
                ok4a, _, f4a = bars_4a(r, base)
                row.update({f"CAGR_{c}": m["CAGR"], f"Sharpe_{c}": m["Sharpe"],
                            f"MaxDD_{c}": m["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                            f"IS_Sharpe_{c}": sharpe(r.loc[:IS_END]),
                            f"OOS_Sharpe_{c}": mo["Sharpe"], f"OOS_CAGR_{c}": mo["CAGR"],
                            f"OOS_MaxDD_{c}": mo["MaxDD"],
                            f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                            f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a)})
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- [A]/[B]/[C] blocks
def blocks_for(idx):
    """Every 5-calendar-year block fully inside the sample; the first may start mid-January at
    the panel's evaluation start."""
    y0, y1 = idx[0].year, idx[-1].year
    return [(y, y + BLOCK_YEARS - 1) for y in range(y0, y1 - BLOCK_YEARS + 2)
            if y + BLOCK_YEARS - 1 <= y1 - 1]


def rolling(series, meta):
    rows = []
    for pname, d in series.items():
        idx = meta[pname]["spy"].index
        for (ya, yb) in blocks_for(idx):
            lo, hi = f"{ya}-01-01", f"{yb}-12-31"
            picks = []
            for (n, g), s in d.items():
                picks.append((sharpe(s["r10"].loc[lo:hi]), n, g))
            picks = [p for p in picks if not np.isnan(p[0])]
            if not picks:
                continue
            best = max(picks, key=lambda t: t[0])
            same_g = {(n, g): v for v, n, g in picks if g == best[2]}
            margin = best[0] - same_g.get((str(ANCHOR_N), best[2]), np.nan)
            # out-of-block follow-on window, never seen by the chooser
            fa, fb = f"{yb+1}-01-01", f"{yb+FOLLOW_YEARS}-12-31"
            def fwd(key):
                r = d[key]["r10"].loc[fa:fb]
                return (sharpe(r), len(r))
            pick_fwd, nfwd = fwd((best[1], best[2]))
            anch_fwd, _ = fwd((str(ANCHOR_N), ANCHOR_G))
            fwd_all = [(fwd((n, g))[0], n, g) for _, n, g in picks]
            fwd_all = [t for t in fwd_all if not np.isnan(t[0])]
            fbest = max(fwd_all, key=lambda t: t[0]) if fwd_all else (np.nan, "", np.nan)
            ovl = max(0, min(yb, MOM_RUN[1]) - max(ya, MOM_RUN[0]) + 1)
            rows.append(dict(panel=pname, block=f"{ya}-{yb}", ya=ya, yb=yb,
                             mom_overlap_yrs=ovl, mom_block=(ovl >= 3),
                             pick_n=best[1], pick_gross=best[2], pick_IS=best[0],
                             margin_vs_n20=margin,
                             fwd_days=nfwd, fwd_Sharpe=pick_fwd, anchor_fwd_Sharpe=anch_fwd,
                             fwd_vs_anchor=pick_fwd - anch_fwd,
                             fwd_best_Sharpe=fbest[0], fwd_best_n=fbest[1],
                             fwd_regret=fbest[0] - pick_fwd))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- [D] rule 8
def rule8(grid, series, meta):
    rows = []
    for pname in series:
        sub = grid[grid.panel == pname]
        pick = sub.loc[sub.IS_Sharpe_10.idxmax()]
        anchor = sub[(sub.n == str(ANCHOR_N)) & (sub.gross == ANCHOR_G)].iloc[0]
        best = sub.loc[sub.OOS_Sharpe_10.idxmax()]
        spy, base = meta[pname]["spy"], meta[pname]["base"]
        so, bo = metrics(spy.loc[OOS_START:]), metrics(base.loc[OOS_START:])
        rows.append(dict(
            panel=pname, pick_n=pick.n, pick_gross=pick.gross, IS_Sharpe=pick.IS_Sharpe_10,
            OOS_CAGR=pick.OOS_CAGR_10, OOS_Sharpe=pick.OOS_Sharpe_10, OOS_MaxDD=pick.OOS_MaxDD_10,
            anchor_OOS=anchor.OOS_Sharpe_10, anchor_OOS_CAGR=anchor.OOS_CAGR_10,
            anchor_OOS_MaxDD=anchor.OOS_MaxDD_10,
            oosbest_OOS=best.OOS_Sharpe_10, oosbest_n=best.n, oosbest_gross=best.gross,
            regret=best.OOS_Sharpe_10 - pick.OOS_Sharpe_10,
            spy_OOS=so["Sharpe"], spy_OOS_CAGR=so["CAGR"], spy_OOS_MaxDD=so["MaxDD"],
            base_OOS=bo["Sharpe"], base_OOS_CAGR=bo["CAGR"], base_OOS_MaxDD=bo["MaxDD"],
            full_keep4b=bool(pick.keep4b_10), full_fail4b=pick.fail4b_10,
            full_keep4a=bool(pick.keep4a_10), full_fail4a=pick.fail4a_10))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print("Family (idea 333's, unchanged): top-n of the v1 composite (vol scaler OFF), v1 "
          "eligibility, NORM weights g/k_t, m=0, WEEKLY, next-day execution.")
    print(f"Tuned: n in {NS} x gross in {GROSSES} = 20 points/panel.  "
          f"Reported axes: cost {COSTS} bps, panel.")
    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    series, meta = build(panels)

    gates(panels, series)

    print("\n[grid] every point, all three rungs -> .grid.csv")
    grid = full_grid(series, meta)
    grid.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    cols = ["panel", "n", "gross", "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10",
            "IS_Sharpe_10", "OOS_Sharpe_10", "turn_yr", "keep4b_10", "fail4b_10", "keep4a_10"]
    print(grid[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for c in COSTS:
        print(f"    @{c:>2} bps: 4b {int(grid[f'keep4b_{c}'].sum())}/{len(grid)}   "
              f"4a {int(grid[f'keep4a_{c}'].sum())}/{len(grid)}")

    print("\n[A] ROLLING 5-YEAR IS BLOCKS -- re-choosing idea 333's chooser on each")
    rb = rolling(series, meta)
    rb.to_csv(OUT / f"{SLUG}.blocks.csv", index=False)
    print(rb.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n    pick_n distribution per panel:")
    print(pd.crosstab(rb.panel, rb.pick_n).to_string())
    print("\n    pick_gross distribution per panel:")
    print(pd.crosstab(rb.panel, rb.pick_gross).to_string())
    print("\n    FLIP RATE (share of consecutive blocks whose pick_n differs):")
    for p, sub in rb.groupby("panel"):
        s = sub.sort_values("ya")
        fl = (s.pick_n.values[1:] != s.pick_n.values[:-1]).sum()
        print(f"      {p:<9} {fl}/{len(s)-1} = {fl/max(1,len(s)-1):.1%}   "
              f"picks in order: {list(s.pick_n)}")

    print("\n    THE QUEUE'S ORDERING -- is B136's pick strictly NARROWER than U56's, block by "
          "block?")
    order = {"10": 0, "20": 1, "40": 2, "80": 3, "ALL": 4}
    a = rb[rb.panel == "B136"].set_index("block").pick_n
    b = rb[rb.panel == "U56"].set_index("block").pick_n
    common = [k for k in a.index if k in b.index]
    nar = sum(order[a[k]] < order[b[k]] for k in common)
    eq = sum(order[a[k]] == order[b[k]] for k in common)
    wid = len(common) - nar - eq
    print(f"      B136 narrower {nar}/{len(common)}   equal {eq}/{len(common)}   "
          f"B136 WIDER {wid}/{len(common)}")
    for k in common:
        print(f"        {k}: B136 n={a[k]:<3} vs U56 n={b[k]:<3} -> "
              f"{'B136 narrower' if order[a[k]]<order[b[k]] else ('equal' if a[k]==b[k] else 'B136 wider')}")

    print("\n[B] IS IT THE 2009-2013 MOMENTUM RUN?  blocks overlapping it by >= 3 years vs not")
    print(pd.crosstab([rb.panel, rb.mom_block], rb.pick_n).to_string())

    print("\n[C0] THE SINGLE-SPLIT WIDTH CURVE: does IS width ORDER agree with OOS width order?")
    wrows = []
    for p, s in grid[grid.gross == ANCHOR_G].groupby("panel"):
        s = s.set_index("n").loc[[str(x) for x in NS]]
        rc = s.IS_Sharpe_10.rank().corr(s.OOS_Sharpe_10.rank())
        wrows.append(dict(panel=p, rank_corr_IS_vs_OOS=rc,
                          IS_spread=s.IS_Sharpe_10.max() - s.IS_Sharpe_10.min(),
                          OOS_spread=s.OOS_Sharpe_10.max() - s.OOS_Sharpe_10.min(),
                          IS_argmax_n=s.IS_Sharpe_10.idxmax(), OOS_argmax_n=s.OOS_Sharpe_10.idxmax(),
                          **{f"IS_n{k}": v for k, v in s.IS_Sharpe_10.items()},
                          **{f"OOS_n{k}": v for k, v in s.OOS_Sharpe_10.items()}))
    wc = pd.DataFrame(wrows)
    wc.to_csv(OUT / f"{SLUG}.widthcurve.csv", index=False)
    print(wc.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n[C1] THE MARGIN the chooser is acting on (IS Sharpe of the pick minus the n=20 cell "
          "at the same gross):")
    mg = rb.groupby("panel").margin_vs_n20.agg(["count", "mean", "median", "min", "max"])
    print(mg.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"    all blocks: median {rb.margin_vs_n20.median():.4f}, "
          f"max {rb.margin_vs_n20.max():.4f} — compare with the block-to-block movement of the "
          f"same cell's IS Sharpe below")
    for p, sub in rb.groupby("panel"):
        s = sub.sort_values("ya")
        mv = np.abs(np.diff(s.pick_IS.values))
        print(f"      {p:<9} |d IS Sharpe| between consecutive blocks: median {np.median(mv):.4f} "
              f"max {mv.max():.4f}")

    print("\n[C2] DOES THE WIDTH PREFERENCE PAY?  each block's pick scored on the NEXT 3 years")
    sc = rb[rb.fwd_days >= 500]
    print(f"    scorable blocks: {len(sc)}/{len(rb)} (>= ~2y of follow-on)")
    for p, sub in sc.groupby("panel"):
        w = (sub.fwd_vs_anchor > 0).sum()
        print(f"      {p:<9} beats the fixed n=20 g=0.75 anchor {w}/{len(sub)} blocks; "
              f"mean dSharpe {sub.fwd_vs_anchor.mean():+.4f} median {sub.fwd_vs_anchor.median():+.4f}; "
              f"mean regret vs the block's own forward-best {sub.fwd_regret.mean():+.4f}")
    w = (sc.fwd_vs_anchor > 0).sum()
    print(f"      POOLED    {w}/{len(sc)} = {w/len(sc):.1%}; mean dSharpe "
          f"{sc.fwd_vs_anchor.mean():+.4f}; mean regret {sc.fwd_regret.mean():+.4f}")

    print("\n[D] RULE 8 (n, gross chosen on 2008-2016 IS Sharpe @10 bps; 2017-2026 read once)")
    r8 = rule8(grid, series, meta)
    r8.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(r8.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n[VERDICT INPUTS]")
    for p, sub in rb.groupby("panel"):
        s = sub.sort_values("ya")
        fl = (s.pick_n.values[1:] != s.pick_n.values[:-1]).sum()
        print(f"    {p:<9} blocks {len(s)}  flip rate {fl/max(1,len(s)-1):.1%}  "
              f"distinct pick_n {sorted(set(s.pick_n), key=lambda x: order[x])}")
    print(f"    B136 narrower than U56 on {nar}/{len(common)} shared blocks "
          f"(equal {eq}, wider {wid})")
    print(f"    pick beats the fixed anchor out-of-block {w}/{len(sc)} = {w/len(sc):.1%}, "
          f"mean dSharpe {sc.fwd_vs_anchor.mean():+.4f}")
    for _, r in wc.iterrows():
        print(f"    {r.panel:<9} IS-vs-OOS width rank corr {r.rank_corr_IS_vs_OOS:+.3f}  "
              f"IS argmax n={r.IS_argmax_n} (spread {r.IS_spread:.4f})  "
              f"OOS argmax n={r.OOS_argmax_n} (spread {r.OOS_spread:.4f})")
    print(f"    4b @10 bps {int(grid.keep4b_10.sum())}/{len(grid)}; "
          f"4a @10 bps {int(grid.keep4a_10.sum())}/{len(grid)}")


if __name__ == "__main__":
    main()
