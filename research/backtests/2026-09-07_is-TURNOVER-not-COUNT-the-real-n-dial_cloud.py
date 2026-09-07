#!/usr/bin/env python3
"""Idea 325: is TURNOVER, not COUNT, the real n-dial?

Idea 47 found the wide fractional book turns over LESS than top-20 (9.52x vs 13.77x on B136)
because a fractional count moves smoothly with the eligible count E_t while a hard rank cut
churns the boundary.  The record's n-dial results (ideas 44/46/318/320) therefore have a
confound: "wider is better on B136" may just be "cheaper is better".

This run separates the two channels.

  [A] COST DECOMPOSITION.  Every n-dial book is run ONCE at 0 bps and the 10/25 bps rungs are
      derived exactly (`r(c) = r(0) - turnover * c / 1e4`, an identity of engine.backtest,
      asserted in section [0]).  If the n-ordering is a cost artefact it must be ABSENT at
      0 bps and appear only as cost rises.  This is the decisive test of the queue's premise
      and it needs no matching at all.

  [B] TURNOVER MATCHING.  The queue's own instrument: hold turnover roughly fixed and move
      width, by putting a NO-TRADE BAND on the rank of the NARROW book instead of widening it
      (idea 273's buffer: enter in the top n, sell only past rank n+m; gate exits are a risk
      rule and are never banded).  If a band-matched top-20 reproduces the wide book, the dial
      is turnover.  If it does not, width is doing something a cost saving cannot buy.

Two tuned parameters, no more:
    1. n in {5, 10, 20, 30, 40, 60, 80, ALL}   position count
    2. m in {0, 5, 10, 20, 40}                 no-trade band width in rank units (m=0 nests
                                               the record's hard-cut book exactly, asserted)
Panel (U56 / B136 / SMALL439), cost rung (0/10/25) and cadence (weekly, the record's) are
reported axes, not tuned choices.  Every point of every axis is printed and written to
`<slug>.grid.csv`.

Weighting is NORM (w_i = g / k_t, k_t = names actually held) at g = 0.75, so the n dial is a
pure WIDTH dial and cannot smuggle in a gross change (idea 244 / idea 44's convention split).

Rule 8 walk-forward: (n, m) chosen on 2008-2016 by IS Sharpe, 2017-2026 read once, against the
n=20/m=0 anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.  Both KEEP paths are
evaluated on every grid point: 4a vs the LIVE RULES v2 book, 4b vs SPY.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; the CAGR levels are optimistic, the n- and m-DIFFERENCES much less so.
The small panel is the worst offender (sub-$2B names that survived to 2026-09) and the 44
tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything is run.
(2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"     # re-print [A]-[D] from the committed CSVs
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_is-TURNOVER-not-COUNT-the-real-n-dial_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, FREQ, GROSS = 0.60, "W", 0.75
NS = [5, 10, 20, 30, 40, 60, 80, "ALL"]
MS = [0, 5, 10, 20, 40]
COSTS = [0, 10, 25]
ANCHOR_N, ANCHOR_M = 20, 0
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
def rank_frame(px, drop_spy=False):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; RULES v1 eligibility).

    drop_spy: on U56/B136 SPY is a genuine universe constituent and the record's books can hold
    it, so it is left eligible (idea 44's convention, needed for the reproduction gate).  On the
    small panel SPY is joined ONLY as a benchmark (see baseline.load_universe) and is removed."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    """The record's book: hard top-n rank cut, recomputed from scratch every rebalance."""
    if n == "ALL":
        return rk.notna()
    return rk <= n


def sel_band(px, rk, n, m):
    """No-trade band (idea 273): a name enters at rank <= n, is held until its rank passes n+m
    or it leaves the eligible set, and free slots are refilled by the best-ranked eligible name
    not already held.  Evaluated only on rebalance days (weights are ignored in between) and
    forward-filled.

    The slot count each day is the parent's OWN count k_t = |{rank <= n}| rather than a flat n,
    which (a) carries the parent's rank-tie quirk (`rank <= n` can name 21 tickers on a tie) and
    (b) keeps the band arm name-count-matched to the hard-cut arm day by day, so m is a pure
    TURNOVER dial and not a second width dial.  m = 0 then nests sel_hard(n) EXACTLY -- asserted
    in section [0]."""
    if n == "ALL":
        return rk.notna()
    reb = rebalance_mask(px.index, FREQ).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held = []                                     # list of column indices, best-rank first
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))          # the hard-cut parent's own name count that day
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j]:
                        break                     # exhausted the eligible set
                    if j not in hs:
                        held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols))
            last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, w, cost_bps=0.0, freq=FREQ):
    """Vectorised-loop clone of engine.backtest (same semantics, numpy arrays, no .iloc writes).
    Asserted against engine.backtest in section [0]."""
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
            pd.Series(np.nansum(held, axis=1), index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def spearman(a, b):
    """Rank correlation without scipy (the sandbox has none)."""
    x, y = pd.Series(a).rank(), pd.Series(b).rank()
    return float(x.corr(y))


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
    """PROTOCOL 4a: Sharpe > the LIVE book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print("Book: top-n eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t at "
          f"g={GROSS}, weekly, next-day execution.  Band m: sell only past rank n+m.")

    panels = {}
    print("\n[panels]")
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    panels["SMALL439"] = small_panel()

    rows, wf_rows = [], []
    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():        # re-print the analysis without re-running
        df = pd.read_csv(gcsv); ctx = pd.read_csv(ccsv).set_index("panel")
        print("\n[resume] grid and context read from disk; sections [A]-[E] recomputed from them")
        analyse(df, ctx, panels)
        return

    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()}")
        print(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} "
              f"MaxDD {so['MaxDD']:.2%}")

        # ---- the LIVE baseline on this panel (4a comparand)
        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0)
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f} "
              f"CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")

        # ---- section [0] gates, once per panel
        if pname == "U56":
            print("\n[0] GATES")
            wA = weights_from(sel_hard(rk, 20))
            eng = backtest(px, wA, cost_bps=0.0, freq=FREQ)
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0)
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturnover| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq=FREQ)
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    derived rung r(25) vs live backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            sb = sel_band(px, rk, 20, 0); sh = sel_hard(rk, 20)
            reb = rebalance_mask(px.index, FREQ)
            dd = (sb[reb] != sh[reb]).values.sum()
            print(f"    sel_band(n=20, m=0) nests sel_hard(n=20) on rebalance days: "
                  f"{dd} disagreements of {int(reb.sum()) * px.shape[1]}")
            assert dd == 0
            # idea 44's published FIXED anchor (w = g/n, not NORM) as a record gate
            fx = sel_hard(rk, 20).astype(float) * (GROSS / 20)
            fr, ft, _, _ = fast_backtest(px, fx, 0.0)
            f10 = (fr - ft * 10 / 1e4).loc[start:]
            mm = metrics(f10); q1, q2 = hs(f10)
            print(f"    idea 44 U56 anchor (FIXED g/n, 10 bps): {mm['CAGR']:.2%} / {mm['Sharpe']:.3f} "
                  f"/ {mm['MaxDD']:.2%}  H1/H2 {q1:.3f}/{q2:.3f}   [published 12.66% / 1.092 / -18.31%]")

        # ---- the grid
        print(f"\n[A/B] GRID {pname} (all points; ann.turnover = mean yearly sum|dw|)")
        print(f"    {'n':>4} {'m':>3} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                           for c in COSTS))
        for n in NS:
            ms_list = [0] if n == "ALL" else MS
            for m in ms_list:
                sel = sel_hard(rk, n) if m == 0 else sel_band(px, rk, n, m)
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                yrs = len(r0) / 252
                tpy = t0.sum() / yrs
                line = f"    {str(n):>4} {m:>3} {tpy:>8.2f} {kk.loc[start:].mean():>6.1f} {gr.loc[start:].mean():>6.3f} |"
                rec = dict(panel=pname, n=str(n), m=m, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), gross=gr.loc[start:].mean())
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, base10 if c == 10 else (br - bt * c / 1e4).loc[start:])
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n'}  {'Y' if ok4a else 'n'} |")
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
                print(line)
                rows.append(rec)

        # context rows for the walk-forward table
        wf_rows.append(dict(panel=pname, spy_oos_sharpe=so["Sharpe"], spy_oos_cagr=so["CAGR"],
                            spy_oos_dd=so["MaxDD"], base_oos_sharpe=bo["Sharpe"],
                            base_oos_cagr=bo["CAGR"], base_oos_dd=bo["MaxDD"]))

    df = pd.DataFrame(rows)
    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    ctx = pd.DataFrame(wf_rows).set_index("panel")
    ctx.to_csv(OUT / f"{SLUG}.ctx.csv")
    analyse(df, ctx, panels)


def analyse(df, ctx, panels):
    df["n"] = df["n"].astype(str)
    # ---------------------------------------------------------- [A] cost decomposition
    print("\n\n[A] IS THE n-ORDERING A COST ARTEFACT?  Spearman(n, Sharpe) at each rung, m=0 only.")
    order = {str(v): i for i, v in enumerate([5, 10, 20, 30, 40, 60, 80])}
    for pname in df.panel.unique():
        d = df[(df.panel == pname) & (df.m == 0) & (df.n != "ALL")].copy()
        d["ni"] = d.n.map(order)
        s = " ".join(f"c={c}: rho {spearman(d.ni, d[f'Sharpe_{c}']):+.3f}" for c in COSTS)
        wide = "80"
        nar = d[d.n == "20"].iloc[0]; wid = d[d.n == wide].iloc[0]
        g0 = wid["Sharpe_0"] - nar["Sharpe_0"]; g10 = wid["Sharpe_10"] - nar["Sharpe_10"]
        print(f"    {pname:9s} {s}   | wide(n=80) - narrow(n=20) dSharpe: "
              f"0bps {g0:+.4f}  10bps {g10:+.4f}  cost channel {g10-g0:+.4f} "
              f"({'100%+' if abs(g10)<1e-9 else f'{(g10-g0)/g10*100:5.1f}%'} of the 10-bps gap) "
              f"| turnover 20 {nar.turn_per_yr:.2f}x vs 80 {wid.turn_per_yr:.2f}x")
    print("    READ: if the 0-bps gap is ~0 and the 10-bps gap is positive, 'wider is better' is a")
    print("          cost artefact.  If the 0-bps gap is already positive, width earns its keep gross.")

    # ---------------------------------------------------------- [B] turnover matching
    print("\n[B] TURNOVER-MATCHED NARROW BOOK vs the WIDE BOOK (10 bps, the PROTOCOL rung).")
    print(f"    {'panel':9s} {'target (n=80,m=0)':>18} | {'matched narrow cell':>22} {'turn':>7} "
          f"{'Sharpe':>7} {'dSharpe vs wide':>16} {'CAGR':>8} {'MaxDD':>8}")
    match_rows = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        wid = d[(d.n == "80") & (d.m == 0)].iloc[0]
        for base_n in ["10", "20", "30"]:
            cand = d[(d.n == base_n)]
            if cand.empty:
                continue
            j = (cand.turn_per_yr - wid.turn_per_yr).abs().idxmin()
            c = d.loc[j]
            print(f"    {pname:9s} {wid.turn_per_yr:>8.2f}x S {wid.Sharpe_10:>6.3f} | "
                  f"n={base_n:>3} m={int(c.m):>3} {c.turn_per_yr:>7.2f}x {c.Sharpe_10:>7.3f} "
                  f"{c.Sharpe_10-wid.Sharpe_10:>+16.4f} {c.CAGR_10:>8.2%} {c.MaxDD_10:>8.2%}")
            match_rows.append(dict(panel=pname, base_n=base_n, m=int(c.m), turn=c.turn_per_yr,
                                   wide_turn=wid.turn_per_yr, sharpe=c.Sharpe_10,
                                   wide_sharpe=wid.Sharpe_10, d=c.Sharpe_10 - wid.Sharpe_10))
    pd.DataFrame(match_rows).to_csv(OUT / f"{SLUG}.match.csv", index=False)

    print("\n[B2] does the BAND alone buy Sharpe at fixed n?  dSharpe(m) - dSharpe(m=0), 10 bps.")
    for pname in df.panel.unique():
        for n in ["10", "20", "40"]:
            d = df[(df.panel == pname) & (df.n == n)].sort_values("m")
            if d.empty:
                continue
            z = d[d.m == 0].iloc[0]
            print(f"    {pname:9s} n={n:>3} | " + "  ".join(
                f"m={int(r.m):<3} turn {r.turn_per_yr:5.2f}x dS {r.Sharpe_10-z.Sharpe_10:+.4f}"
                for r in d.itertuples()))

    # ---------------------------------------------------------- [C] verdict census
    print("\n[C] KEEP-path census over the whole grid")
    for c in COSTS:
        print(f"    c={c:>2} bps: 4b {int(df[f'keep4b_{c}'].sum())}/{len(df)}   "
              f"4a {int(df[f'keep4a_{c}'].sum())}/{len(df)}")
    fails = {}
    for _, r in df.iterrows():
        for k in str(r["fail4b_10"]).split(","):
            if k:
                fails[k] = fails.get(k, 0) + 1
    print("    binding 4b bars at 10 bps:", ", ".join(f"{k} {v}/{len(df)}" for k, v in
                                                      sorted(fails.items(), key=lambda x: -x[1])))
    if df["keep4b_10"].any():
        print("    4b passes at 10 bps:")
        for _, r in df[df["keep4b_10"]].iterrows():
            print(f"      {r.panel:9s} n={r.n:>3} m={int(r.m):>3} turn {r.turn_per_yr:5.2f}x "
                  f"{r.CAGR_10:.2%} / {r.Sharpe_10:.3f} / {r.MaxDD_10:.2%} "
                  f"H1/H2 {r.H1_10:.3f}/{r.H2_10:.3f} OOS {r.OOS_Sharpe_10:.3f}")

    # ---------------------------------------------------------- [E] cost ladder / breakeven
    print("\n[E] COST LADDER on every cell that still clears 4b at 25 bps (idea 323's rung).")
    print("    breakeven c* = the largest whole bps at which all five 4b bars still hold.")
    lad = []
    for pname in df.panel.unique():
        d = df[(df.panel == pname) & df["keep4b_25"]]
        if d.empty:
            continue
        px = panels[pname]
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        rk, _ = rank_frame(px, drop_spy=(pname == "SMALL439"))
        for _, row in d.iterrows():
            n = row.n if row.n == "ALL" else int(row.n)
            m = int(row.m)
            sel = sel_hard(rk, n) if m == 0 else sel_band(px, rk, n, m)
            r0, t0, _, _ = fast_backtest(px, weights_from(sel), 0.0)
            r0, t0 = r0.loc[start:], t0.loc[start:]
            cstar, bar = None, ""
            for c in range(0, 121):
                ok, dd, f = bars_4b(r0 - t0 * c / 1e4, spy)
                if ok:
                    cstar = c
                else:
                    bar = ",".join(f)
                    break
            mt = metrics(r0 - t0 * 25 / 1e4)
            print(f"    {pname:9s} n={row.n:>3} m={m:>3} turn {row.turn_per_yr:5.2f}x | 25 bps "
                  f"{mt['CAGR']:.2%}/{mt['Sharpe']:.3f}/{mt['MaxDD']:.2%} | breakeven c* = "
                  f"{cstar:>3} bps, first bar to fail above it: {bar}")
            lad.append(dict(panel=pname, n=row.n, m=m, turn=row.turn_per_yr,
                            cagr25=mt["CAGR"], sharpe25=mt["Sharpe"], dd25=mt["MaxDD"],
                            breakeven_bps=cstar, first_fail=bar))
    if lad:
        pd.DataFrame(lad).to_csv(OUT / f"{SLUG}.breakeven.csv", index=False)
    else:
        print("    (no cell clears 4b at 25 bps)")

    # ---------------------------------------------------------- [D] rule 8 walk-forward
    print("\n[D] RULE 8 WALK-FORWARD: (n, m) chosen on IS <= 2016 by Sharpe, OOS 2017+ read once "
          "(10 bps)")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        pick = d.loc[d["IS_Sharpe_10"].idxmax()]
        best = d.loc[d["OOS_Sharpe_10"].idxmax()]
        anch = d[(d.n == str(ANCHOR_N)) & (d.m == ANCHOR_M)].iloc[0]
        cx = ctx.loc[pname]
        print(f"\n    --- {pname}")
        print(f"    {'arm':28s} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for lab, r in [(f"IS-chosen n={pick.n} m={int(pick.m)}", pick),
                       (f"anchor n=20 m=0", anch),
                       (f"OOS-best n={best.n} m={int(best.m)}", best)]:
            print(f"    {lab:28s} {r.OOS_CAGR_10:>9.2%} {r.OOS_Sharpe_10:>11.3f} {r.OOS_MaxDD_10:>10.2%}")
        print(f"    {'RULES v2 (live)':28s} {cx.base_oos_cagr:>9.2%} {cx.base_oos_sharpe:>11.3f} "
              f"{cx.base_oos_dd:>10.2%}")
        print(f"    {'SPY':28s} {cx.spy_oos_cagr:>9.2%} {cx.spy_oos_sharpe:>11.3f} {cx.spy_oos_dd:>10.2%}")
        print(f"    regret (IS-chosen - OOS-best) {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.4f} Sharpe; "
              f"IS-chosen - anchor {pick.OOS_Sharpe_10-anch.OOS_Sharpe_10:+.4f}")
        wf.append(dict(panel=pname, pick_n=pick.n, pick_m=int(pick.m),
                       pick_oos_sharpe=pick.OOS_Sharpe_10, pick_oos_cagr=pick.OOS_CAGR_10,
                       pick_oos_dd=pick.OOS_MaxDD_10, anchor_oos_sharpe=anch.OOS_Sharpe_10,
                       best_n=best.n, best_m=int(best.m), best_oos_sharpe=best.OOS_Sharpe_10,
                       spy_oos_sharpe=cx.spy_oos_sharpe, base_oos_sharpe=cx.base_oos_sharpe))
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\nwrote {SLUG}.grid.csv ({len(df)} rows), .match.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
