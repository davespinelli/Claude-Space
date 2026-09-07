#!/usr/bin/env python3
"""Idea 349: does a band on the EXIT side only beat a band on both sides?

Idea 331 established that the no-trade BAND is a distinct instrument from the cadence dial --
turnover-matched, the banded cell beat the cadence-only cell of nearest annual turnover in 10 of
18 comparisons -- but it ran the band as ONE dial `m`: a name enters at rank <= n and is held
until its rank passes n+m.  Two mechanisms are fused inside that single dial:

  * EXIT stickiness -- a held name that drifts to rank n+1..n+m is not sold;
  * ENTRY reluctance -- because the drifting name keeps occupying a slot, the name ranked
    n-something that would have replaced it is not bought.

The queue's claim is that the band's gains concentrate at FAST cadences where entry churn
dominates, so the ENTRY side may be carrying the win.  This run splits the dial in two and
sweeps the sides independently.

THE TEST, pre-registered before any number was read:

  [A] SPLIT THE DIAL.  Two thresholds around the same centre n = 20:
        enter  an unheld name only if its rank <= n - e      (ENTRY buffer e, stricter entry)
        exit   a held name only once its rank  >  n + x      (EXIT buffer x, stickier exit)
      Slot count each rebalance is the parent's own k_t = |{rank <= n}|, so the arms stay
      name-count-matched to the hard cut wherever the entry pool can fill it.  (e, x) = (0, 0)
      nests the hard rank cut EXACTLY; (0, 20) nests idea 331's weekly band cell EXACTLY.  Both
      are asserted in section [0] against idea 331's own committed `.grid.csv`.
      Exactly two tuned parameters: e in {0,2,4,6,8,12,16} x x in {0,5,10,20,40,80} = 42 cells.
      Panel {U56, B136, SMALL439} and cost rung {0, 10, 25} bps are REPORTED axes, not tuned
      choices; every point of every axis is printed and written to `<slug>.grid.csv`.
      Cadence is FIXED WEEKLY throughout, per the queue text.

  [B] WHICH SIDE CARRIES IT?  Four readings:
      B1  MARGINAL: dSharpe(e, 0) along the entry-only ladder vs dSharpe(0, x) along the
          exit-only ladder, both against the (0,0) hard cut.
      B2  TURNOVER-MATCHED (the decisive one, mirroring idea 331's B2): each entry-only cell
          against the exit-only cell of nearest annual turnover, and the reverse.  A side that
          only wins by trading less is not a side, it is the turnover dial again.
      B3  ADDITIVITY: is Sharpe(e, x) - Sharpe(0, 0) equal to the sum of the two marginals?
          If the interaction term is large the two sides are not separable and the parent's
          single dial was the right parameterisation.
      B4  ADMISSION: does any e > 0 cell clear a KEEP path that no e = 0 cell clears?

  [C] BREAKEVEN c*: the largest whole bps at which all five 4b bars still hold, on every cell
      that clears 4b at 25 bps.  Idea 331's weekly record is 47 bps (U56, m=20).

  [D] RULE 8 walk-forward: (e, x) chosen on 2008-2016 by IS Sharpe at 10 bps, 2017-2026 read
      once, on three MENUS -- FULL (42 cells), EXIT-ONLY (e=0, 6 cells), ENTRY-ONLY (x=0, 7
      cells) -- against the (0,0) anchor, idea 331's (0,20) cell, the OOS-best cell (regret),
      RULES v2 (live) and SPY.  Which menu an ex-ante chooser is better off with is the honest
      version of "which side carries the win".

Book (fixed, idea 331's convention, never tuned): top-20 eligible by the RULES v1 composite with
the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60), NORM weights
w_i = g/k_t at g = 0.75 so neither buffer can smuggle in a gross change, next-day execution,
10 bps per unit turnover at the anchor rung.

KNOWN ASYMMETRY, stated up front because it is not a defect to be hidden: the EXIT buffer is
name-count-neutral by construction (the cap absorbs it), while the ENTRY buffer can leave the
cap unfillable -- if fewer than k_t eligible names sit at rank <= n-e and are not already held,
the book simply holds fewer names at g/k each.  So e is a concentration dial as well as a
turnover dial and x is not.  `names` (mean holdings/day) is printed for every cell so the reader
can price that; the B2 turnover-matched reading is reported with the name counts attached.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; the CAGR levels are optimistic, the e- and x-DIFFERENCES much less so.
(2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136, and
the 44 tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything runs.
(3) rule 8's IS window is 2008-2016 on U56/B136 but effectively 2010-2016 on SMALL439.

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

SLUG = "2026-09-07_does-a-band-on-the-EXIT-ONLY-beat-a-band-on-both-sides_C"
OUT = ROOT / "research" / "backtests"
PARENT = OUT / "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud.grid.csv"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
FREQ = "W"                                   # fixed by the idea; never moved
ES = [0, 2, 4, 6, 8, 12, 16]                 # entry buffer  (enter at rank <= n - e)
XS = [0, 5, 10, 20, 40, 80]                  # exit  buffer  (exit  at rank >  n + x)
COSTS = [0, 10, 25]
ANCHOR = (0, 0)                              # the hard rank cut
PARENT_CELL = (0, 20)                        # idea 331's weekly band cell
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
    it (idea 44's convention, needed for the reproduction gate).  On the small panel SPY is
    joined ONLY as a benchmark (see baseline.load_universe) and is removed."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    """The record's book: hard top-n rank cut, recomputed from scratch every rebalance."""
    return rk <= n


def sel_ex(px, rk, n, e, x, freq=FREQ):
    """Two-sided band: enter at rank <= n-e, hold until rank > n+x or the name leaves the
    eligible set.  Free slots refill from the best-ranked ADMISSIBLE (rank <= n-e) name not held.

    Slot cap each rebalance day is the parent's own k_t = |{rank <= n}|, exactly as in idea 331,
    so x is a pure turnover dial.  e is NOT: when fewer than k_t admissible names exist the book
    holds fewer names (weights g/k keep gross at g, so it concentrates rather than de-grosses).

    (e, x) = (0, 0) nests sel_hard(n) exactly; (0, x) nests idea 331's sel_band(m=x) exactly --
    its refill loop takes the best-ranked unheld name with no explicit threshold, but the slot
    algebra (slots = |r<=n| - |held| and |held n {r<=n}| = |held| - |held n {r>n}|) means it can
    never reach past rank n.  Both nestings are asserted in section [0]."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    enter_at = n - e
    held = []
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + x]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j] or r[j] > enter_at:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
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
    """Vectorised-loop clone of engine.backtest (same semantics, numpy arrays).
    Asserted against engine.backtest at 0.000e+00 in section [0]."""
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


def breakeven(r0, t0, spy, hi=200):
    """Largest whole bps at which all five 4b bars still hold (None if it fails at 0)."""
    cstar, bar = None, ""
    for c in range(0, hi + 1):
        ok, _, f = bars_4b(r0 - t0 * c / 1e4, spy)
        if ok:
            cstar = c
        else:
            bar = ",".join(f)
            break
    return cstar, bar


def spearman(a, b):
    x, y = pd.Series(list(a)).rank(), pd.Series(list(b)).rank()
    return float(x.corr(y))


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: top-{N} eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t at "
          f"g={GROSS}, WEEKLY, next-day execution.")
    print(f"Tuned: entry buffer e in {ES} (enter at rank <= n-e) x exit buffer x in {XS} "
          f"(exit at rank > n+x).  {len(ES)*len(XS)} cells.")
    print(f"Reported axes: panel, cost {COSTS} bps.  (e,x)=(0,0) is the hard cut; "
          f"(0,20) is idea 331's band.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"))
        return

    parent = pd.read_csv(PARENT)
    parent = parent[parent.cadence == "W"].set_index(["panel", "m"])

    rows, ctx_rows = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} "
              f"MaxDD {so['MaxDD']:.2%}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, "W")
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f} "
              f"CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")
        ctx_rows.append(dict(panel=pname, names=px.shape[1] - 1, start=str(start.date()),
                             end=str(px.index[-1].date()),
                             spy_CAGR=ms_["CAGR"], spy_Sharpe=ms_["Sharpe"], spy_MaxDD=ms_["MaxDD"],
                             spy_H1=s1, spy_H2=s2, spy_OOS=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                             spy_OOS_MaxDD=so["MaxDD"],
                             base_CAGR=bm["CAGR"], base_Sharpe=bm["Sharpe"], base_MaxDD=bm["MaxDD"],
                             base_H1=b1, base_H2=b2, base_OOS=bo["Sharpe"],
                             base_IS=metrics(base10.loc[:IS_END])["Sharpe"]))

        # ------------------------------------------------ [0] gates
        if pname == "U56":
            print("\n[0] GATES (all asserted before any new number is read)")
            wA = weights_from(sel_hard(rk, N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    G1 fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    G2 derived rung r(25) vs backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
        reb = rebalance_mask(px.index, FREQ)
        dd = int((sel_ex(px, rk, N, 0, 0)[reb] != sel_hard(rk, N)[reb]).values.sum())
        print(f"    G3 [{pname}] sel_ex(0,0) nests sel_hard on {int(reb.sum())} weekly rebalance "
              f"days: {dd} disagreements of {int(reb.sum()) * px.shape[1]}")
        assert dd == 0

        # ------------------------------------------------ the grid
        print(f"\n[A] GRID {pname} (every point; turn/yr = mean yearly sum|dw|)")
        print(f"    {'e':>3} {'x':>3} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                           for c in COSTS))
        for e in ES:
            for x in XS:
                sel = sel_ex(px, rk, N, e, x)
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0, FREQ)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                line = (f"    {e:>3} {x:>3} {tpy:>8.2f} {kk.loc[start:].mean():>6.2f} "
                        f"{gr.loc[start:].mean():>6.3f} |")
                rec = dict(panel=pname, e=e, x=x, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), gross=gr.loc[start:].mean())
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    basec = base10 if c == 10 else (br - bt * c / 1e4).loc[start:]
                    ok4a, d4a, f4a = bars_4a(r, basec)
                    line += (f" {mt['CAGR']:>10.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n':>2} {'Y' if ok4a else 'n':>2} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a)})
                    rec.update({f"m4b_{k}_{c}": v for k, v in d4b.items()})
                    rec.update({f"m4a_{k}_{c}": v for k, v in d4a.items()})
                cst, cbar = (breakeven(r0, t0, spy) if rec["keep4b_0"]
                             else (None, rec["fail4b_0"]))
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                line += f" c*={rec['breakeven_bps']:>4}"
                print(line)
                rows.append(rec)

                # -------- reproduction against idea 331's committed weekly rows
                if e == 0 and x in (0, 20):
                    p = parent.loc[(pname, x)]
                    ds = abs(p["Sharpe_10"] - rec["Sharpe_10"]); dc = abs(p["CAGR_10"] - rec["CAGR_10"])
                    dt_ = abs(p["turn_per_yr"] - rec["turn_per_yr"]); dm = abs(p["MaxDD_10"] - rec["MaxDD_10"])
                    do = abs(p["OOS_Sharpe_10"] - rec["OOS_Sharpe_10"])
                    print(f"        G4 vs idea 331 grid.csv [{pname} W m={x}]: |dSharpe| {ds:.3e} "
                          f"|dCAGR| {dc:.3e} |dMaxDD| {dm:.3e} |dturn| {dt_:.3e} |dOOS| {do:.3e}")
                    assert max(ds, dc, dt_, dm, do) < 1e-12

    g = pd.DataFrame(rows); g.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.reset_index().to_csv(ccsv, index=False)
    print(f"\n    wrote {gcsv.name} ({len(g)} rows) and {ccsv.name}")
    analyse(g, ctx)


# ---------------------------------------------------------------- analysis
def analyse(g, ctx):
    panels = list(dict.fromkeys(g.panel))
    key = lambda d, e, x: d[(d.e == e) & (d.x == x)].iloc[0]

    # ------------------------------------------------------------ [B1] marginals
    print("\n\n[B1] MARGINAL EFFECT OF EACH SIDE (dSharpe vs the (0,0) hard cut, 10 bps)")
    print("     ENTRY-ONLY ladder (x=0) and EXIT-ONLY ladder (e=0); turn/yr and names attached.")
    b1 = []
    for pname in panels:
        d = g[g.panel == pname]
        a = key(d, 0, 0)
        print(f"  {pname}: anchor (0,0) Sharpe {a.Sharpe_10:.3f} turn {a.turn_per_yr:.2f} "
              f"names {a.names:.2f}")
        for side, vals in (("ENTRY e", ES), ("EXIT  x", XS)):
            parts = []
            for v in vals:
                if v == 0:
                    continue
                c = key(d, v, 0) if side.startswith("ENTRY") else key(d, 0, v)
                parts.append(f"{v:>3}: dS {c.Sharpe_10 - a.Sharpe_10:+.3f} T {c.turn_per_yr:5.2f} "
                             f"k {c.names:5.2f}")
                b1.append(dict(panel=pname, side=side.split()[0], v=v,
                               dSharpe=c.Sharpe_10 - a.Sharpe_10, turn=c.turn_per_yr,
                               names=c.names, dOOS=c.OOS_Sharpe_10 - a.OOS_Sharpe_10))
            print(f"     {side} | " + " | ".join(parts))
    b1 = pd.DataFrame(b1)
    for s in ("ENTRY", "EXIT"):
        z = b1[b1.side == s]
        print(f"     {s:>5}: mean dSharpe {z.dSharpe.mean():+.4f}  positive {int((z.dSharpe>0).sum())}"
              f"/{len(z)}  mean dOOS {z.dOOS.mean():+.4f}  "
              f"spearman(v, turnover) {spearman(z.v, z.turn):+.3f}  "
              f"spearman(v, names) {spearman(z.v, z.names):+.3f}")

    # ------------------------------------------------------------ [B2] turnover-matched
    print("\n[B2] TURNOVER-MATCHED, entry side vs exit side (the decisive reading, 10 bps)")
    print("     Each buffered cell of one side vs the cell of the OTHER side with the nearest")
    print("     annual turnover.  A win that only comes from trading less is not a side.")
    m2 = []
    for pname in panels:
        d = g[g.panel == pname]
        ent = d[(d.x == 0) & (d.e > 0)]
        ext = d[(d.e == 0) & (d.x > 0)]
        for label, src, dst in (("ENTRY->exit", ent, ext), ("EXIT->entry", ext, ent)):
            for _, c in src.iterrows():
                t = dst.iloc[(dst.turn_per_yr - c.turn_per_yr).abs().values.argmin()]
                m2.append(dict(panel=pname, direction=label, e=int(c.e), x=int(c.x),
                               turn=c.turn_per_yr, names=c.names, Sharpe=c.Sharpe_10,
                               m_e=int(t.e), m_x=int(t.x), m_turn=t.turn_per_yr,
                               m_names=t.names, m_Sharpe=t.Sharpe_10,
                               dS=c.Sharpe_10 - t.Sharpe_10,
                               dOOS=c.OOS_Sharpe_10 - t.OOS_Sharpe_10,
                               dturn=c.turn_per_yr - t.turn_per_yr))
    m2 = pd.DataFrame(m2)
    for pname in panels:
        for label in ("ENTRY->exit", "EXIT->entry"):
            z = m2[(m2.panel == pname) & (m2.direction == label)]
            print(f"  {pname:>9} {label}:")
            for _, r in z.iterrows():
                print(f"       (e={r.e:>2},x={r.x:>2}) T {r.turn:5.2f} k {r.names:5.2f} S {r.Sharpe:.3f}"
                      f"  vs  (e={r.m_e:>2},x={r.m_x:>2}) T {r.m_turn:5.2f} k {r.m_names:5.2f} "
                      f"S {r.m_Sharpe:.3f}  ->  dS {r.dS:+.3f} (dT {r.dturn:+5.2f}) dOOS {r.dOOS:+.3f}")
    for label in ("ENTRY->exit", "EXIT->entry"):
        z = m2[m2.direction == label]
        print(f"     {label}: wins {int((z.dS>0).sum())}/{len(z)}  median dS {z.dS.median():+.4f}  "
              f"mean dS {z.dS.mean():+.4f}  mean |dT| {z.dturn.abs().mean():.2f}  "
              f"OOS wins {int((z.dOOS>0).sum())}/{len(z)}")
    ee = m2[m2.direction == "ENTRY->exit"]; xe = m2[m2.direction == "EXIT->entry"]
    print(f"     VERDICT B2: the ENTRY side beats its turnover-matched EXIT twin in "
          f"{int((ee.dS>0).sum())} of {len(ee)} (median {ee.dS.median():+.4f}); the EXIT side "
          f"beats its turnover-matched ENTRY twin in {int((xe.dS>0).sum())} of {len(xe)} "
          f"(median {xe.dS.median():+.4f}).  Out of sample: entry {int((ee.dOOS>0).sum())}/{len(ee)}, "
          f"exit {int((xe.dOOS>0).sum())}/{len(xe)}.")
    print(f"     Saturation note: on a panel with k eligible names the exit buffer stops biting "
          f"once n+x exceeds k.  Cells where x=40 and x=80 are identical: "
          f"{sum(1 for p in panels if abs(key(g[g.panel==p],0,40).Sharpe_10 - key(g[g.panel==p],0,80).Sharpe_10) < 1e-12)}"
          f"/{len(panels)} panels at e=0.")

    # ------------------------------------------------------------ [B3] additivity
    print("\n[B3] ADDITIVITY: dS(e,x) vs dS(e,0) + dS(0,x)  (10 bps; interaction = actual - sum)")
    add = []
    for pname in panels:
        d = g[g.panel == pname]
        a = key(d, 0, 0).Sharpe_10
        print(f"  {pname}:  {'x=':>6}" + "".join(f"{x:>9}" for x in XS if x > 0))
        for e in ES:
            if e == 0:
                continue
            me = key(d, e, 0).Sharpe_10 - a
            cells = []
            for x in XS:
                if x == 0:
                    continue
                mx = key(d, 0, x).Sharpe_10 - a
                act = key(d, e, x).Sharpe_10 - a
                inter = act - me - mx
                cells.append(f"{inter:>+9.3f}")
                add.append(dict(panel=pname, e=e, x=x, marg_e=me, marg_x=mx, actual=act,
                                interaction=inter))
            print(f"     e={e:<3} " + "".join(cells))
    add = pd.DataFrame(add)
    print(f"     interaction: mean {add.interaction.mean():+.4f} sd {add.interaction.std():.4f} "
          f"|mean| vs mean|marginal| "
          f"{abs(add.interaction.mean()) / (abs(add.marg_e).mean() + abs(add.marg_x).mean()):.3f}  "
          f"negative {int((add.interaction<0).sum())}/{len(add)}")
    print(f"     corr(actual, marg_e+marg_x) = {add.actual.corr(add.marg_e + add.marg_x):+.3f}; "
          f"R2 of the additive model {add.actual.corr(add.marg_e + add.marg_x)**2:.3f}")

    # ------------------------------------------------------------ [B4]/[C] admission
    print("\n[B4] ADMISSION (both KEEP paths, every cell, every rung)")
    for c in COSTS:
        tot = len(g)
        print(f"  c={c:>2} bps: 4b {int(g[f'keep4b_{c}'].sum())}/{tot}   "
              f"4a {int(g[f'keep4a_{c}'].sum())}/{tot}")
        for pname in panels:
            d = g[g.panel == pname]
            p4b, p4a = d[d[f"keep4b_{c}"]], d[d[f"keep4a_{c}"]]
            ent_only = p4b[p4b.e > 0]
            print(f"      {pname:>9}: 4b {len(p4b):>2}/{len(d)} (with e>0: {len(ent_only)})  "
                  f"4a {len(p4a):>2}/{len(d)}")
        fails = g[~g[f"keep4b_{c}"]][f"fail4b_{c}"].str.split(",").explode()
        print(f"      binding 4b bars: " + "  ".join(f"{k} {v}" for k, v in fails.value_counts().items()))
    q = g[g.keep4b_10]
    print(f"  Does any e>0 cell clear a path no e=0 cell clears?")
    for pname in panels:
        d = g[g.panel == pname]
        e0 = d[(d.e == 0) & d.keep4b_10]; ep = d[(d.e > 0) & d.keep4b_10]
        print(f"      {pname:>9}: 4b@10 e=0 {len(e0)}  e>0 {len(ep)}  "
              f"-> {'NO new panel' if (len(ep) == 0 or len(e0) > 0) else 'NEW'}")
    print("\n[C] BREAKEVEN c* (largest whole bps at which all five 4b bars hold; -1 = fails at 0)")
    top = g.sort_values("breakeven_bps", ascending=False).head(12)
    for _, r in top.iterrows():
        print(f"      {r.panel:>9} (e={int(r.e):>2},x={int(r.x):>2})  c* {int(r.breakeven_bps):>4} bps  "
              f"first fail {r.breakeven_first_fail:<12} S10 {r.Sharpe_10:.3f} T {r.turn_per_yr:5.2f}")
    print(f"      cells with c* >= 10 bps: {int((g.breakeven_bps >= 10).sum())}/{len(g)}; "
          f"c* > 0: {int((g.breakeven_bps > 0).sum())}/{len(g)}; "
          f"record weekly c* here {int(g.breakeven_bps.max())} vs idea 331's weekly 47")

    # ------------------------------------------------------------ [D] rule 8
    print("\n[D] RULE 8 WALK-FORWARD: (e,x) chosen on 2008-2016 IS Sharpe @10 bps, 2017-2026 read once")
    menus = {"FULL (42)": lambda d: d,
             "EXIT-ONLY (e=0, 6)": lambda d: d[d.e == 0],
             "ENTRY-ONLY (x=0, 7)": lambda d: d[d.x == 0]}
    wf = []
    for pname in panels:
        d = g[g.panel == pname]
        cx = ctx.loc[pname]
        best = d.iloc[d.OOS_Sharpe_10.values.argmax()]
        anch = key(d, *ANCHOR); par = key(d, *PARENT_CELL)
        print(f"  {pname}:  SPY OOS {cx.spy_OOS:.3f} | RULES v2 (live) OOS {cx.base_OOS:.3f} | "
              f"anchor (0,0) OOS {anch.OOS_Sharpe_10:.3f} | idea 331 (0,20) OOS "
              f"{par.OOS_Sharpe_10:.3f} | OOS-best (e={int(best.e)},x={int(best.x)}) "
              f"{best.OOS_Sharpe_10:.3f}")
        for mname, f in menus.items():
            sub = f(d)
            pick = sub.iloc[sub.IS_Sharpe_10.values.argmax()]
            print(f"      {mname:>20}: pick (e={int(pick.e):>2},x={int(pick.x):>2}) IS "
                  f"{pick.IS_Sharpe_10:.3f} -> OOS Sharpe {pick.OOS_Sharpe_10:.3f} "
                  f"CAGR {pick.OOS_CAGR_10:.2%} MaxDD {pick.OOS_MaxDD_10:.2%} | "
                  f"regret {pick.OOS_Sharpe_10 - best.OOS_Sharpe_10:+.3f} | "
                  f"vs anchor {pick.OOS_Sharpe_10 - anch.OOS_Sharpe_10:+.3f} "
                  f"vs 331 {pick.OOS_Sharpe_10 - par.OOS_Sharpe_10:+.3f} "
                  f"vs SPY {pick.OOS_Sharpe_10 - cx.spy_OOS:+.3f} "
                  f"vs LIVE {pick.OOS_Sharpe_10 - cx.base_OOS:+.3f}")
            wf.append(dict(panel=pname, menu=mname, e=int(pick.e), x=int(pick.x),
                           IS=pick.IS_Sharpe_10, OOS=pick.OOS_Sharpe_10,
                           OOS_CAGR=pick.OOS_CAGR_10, OOS_MaxDD=pick.OOS_MaxDD_10,
                           regret=pick.OOS_Sharpe_10 - best.OOS_Sharpe_10,
                           vs_anchor=pick.OOS_Sharpe_10 - anch.OOS_Sharpe_10,
                           vs_parent=pick.OOS_Sharpe_10 - par.OOS_Sharpe_10,
                           vs_spy=pick.OOS_Sharpe_10 - cx.spy_OOS,
                           vs_live=pick.OOS_Sharpe_10 - cx.base_OOS,
                           keep4b_oos=bool(pick[f"keep4b_10"])))
    wf = pd.DataFrame(wf)
    print("\n     MENU SUMMARY (mean over the 3 panels):")
    for mname in menus:
        z = wf[wf.menu == mname]
        print(f"      {mname:>20}: OOS {z.OOS.mean():.4f}  regret {z.regret.mean():+.4f}  "
              f"beats anchor {int((z.vs_anchor>0).sum())}/3  beats idea331 "
              f"{int((z.vs_parent>0).sum())}/3  beats SPY {int((z.vs_spy>0).sum())}/3  "
              f"beats LIVE {int((z.vs_live>0).sum())}/3")
    wf.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    m2.to_csv(OUT / f"{SLUG}.matched.csv", index=False)
    add.to_csv(OUT / f"{SLUG}.additivity.csv", index=False)
    b1.to_csv(OUT / f"{SLUG}.marginals.csv", index=False)
    print(f"\n    wrote {SLUG}.walkforward.csv / .matched.csv / .additivity.csv / .marginals.csv")


if __name__ == "__main__":
    main()
