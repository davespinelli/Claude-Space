#!/usr/bin/env python3
"""Idea 329: does the no-trade BAND rescue the B136 H2 bar?

Idea 325 PARKed `top-n eligible, NORM weights g/k_t at g=0.75, no-trade band m` at the cell
(U56, n=20, m=20): 12.87% / 1.112 / -17.22%, OOS 1.187, breakeven 47 bps, 4b PASS on U56.
The SAME cell on B136 misses 4b.  The queue entry says it misses on ONE bar (H2 0.817 vs SPY
0.834, margin -0.017).  Section [0] re-reads the parent's committed grid: at 10 bps the cell
misses on TWO bars, H2 (-0.0170) and the drawdown cap (-0.0020) -- the queue text is corrected
here rather than carried forward.

PRE-REGISTRATION.  The cell under test is fixed before anything is run:

        panel   B136 (research/universe_broad.json, ~136 names + SPY)
        n       20          (NOT swept; the parent's anchor width)
        m       20          (NOT swept for the verdict; swept only as a reported context axis)
        gross   0.75, NORM weights w_i = g / k_t
        rank    v1 composite with the vol scaler OFF, RULES v1 eligibility (200d MA, vol20<0.60)

The single tuned dial is CADENCE in {W, M, Q}.  The cost rung {0, 10, 25} is a reported axis,
not a choice.  m in {0, 5, 10, 20, 40} is the second parameter and is reported in full at every
cadence, but the VERDICT is read off m=20 only, so the run cannot be rescued by picking an m.

DECISION RULE, fixed in advance:
    * If (B136, n=20, m=20) clears ALL FIVE 4b bars at PROTOCOL's 10 bps at ANY of W/M/Q,
      idea 325's PARK is cross-universe and goes to Sunday review.
    * If none does, the candidate is a U56 object and is labelled one.
A pass on the H2 bar alone is NOT a pass: 4b is a conjunction and the DD bar is live here.

U56 and SMALL439 are run on the identical grid as context -- they cannot change the verdict,
they say whether the cadence dial moves the cell the same way off B136.

Rule 8 walk-forward: (cadence, m) chosen on 2008-2016 by IS Sharpe at 10 bps, 2017-2026 read
ONCE, against the (W, m=0) anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.
Both KEEP paths are evaluated at every grid point: 4a vs the LIVE RULES v2 book, 4b vs SPY.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; CAGR levels are optimistic, cadence/m DIFFERENCES much less so.  (2) The
4a comparand RULES v2 is always run at its live WEEKLY cadence, so the cadence dial moves the
idea arm only.  (3) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves
as U56/B136, and the 44 tickers with max_1d_move >= 1.0 are dropped before anything is run.

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

SLUG = "2026-09-07_does-the-BAND-rescue-the-B136-H2-bar_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS = 0.60, 0.75
BASE_FREQ = "W"                       # the LIVE book's cadence; never moved
PRE_PANEL, PRE_N, PRE_M = "B136", 20, 20          # the pre-registered cell
CADENCES = ["W", "M", "Q"]
MS = [0, 5, 10, 20, 40]
COSTS = [0, 10, 25]
ANCHOR = ("W", 0)
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


# ---------------------------------------------------------------- the book (idea 325's, verbatim)
def rank_frame(px, drop_spy=False):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; RULES v1 eligibility).
    On U56/B136 SPY is a genuine constituent and stays eligible (idea 44's convention); on the
    small panel it is joined only as a benchmark and is removed."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk.notna() if n == "ALL" else rk <= n


def sel_band(px, rk, n, m, freq):
    """No-trade band (idea 273 / idea 325): a name enters at rank <= n, is held until its rank
    passes n+m or it leaves the eligible set; free slots refill with the best-ranked eligible
    name not held.  Slot count is the hard-cut parent's OWN count k_t = |{rank <= n}| that day,
    so m is a pure turnover dial.  m = 0 nests sel_hard(n) exactly (asserted in [0])."""
    if n == "ALL":
        return rk.notna()
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held = []
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j]:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester (idea 325's)
def fast_backtest(px, w, cost_bps=0.0, freq="W"):
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


# ---------------------------------------------------------------- bars
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


def breakeven(r0, t0, spy, lo=0.0, hi=200.0):
    """Highest cost rung (bps) at which all five 4b bars still hold; bisection on a monotone
    (in practice) pass set.  Returns 0.0 if the book fails 4b already at 0 bps."""
    if not bars_4b(r0, spy)[0]:
        return 0.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if bars_4b(r0 - t0 * mid / 1e4, spy)[0]:
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"PRE-REGISTERED CELL: panel={PRE_PANEL}  n={PRE_N}  m={PRE_M}  gross={GROSS} NORM.")
    print(f"Tuned dial: cadence in {CADENCES}.  Context axis: m in {MS}.  Rungs {COSTS} bps reported.")
    print("Verdict rule: the cell clears 4b at 10 bps at some cadence -> cross-universe PARK to "
          "Sunday review; else the parent's candidate is a U56 object.")

    # ---- [0] re-read the parent's committed grid, correct the queue text
    print("\n[0] PARENT GRID RE-READ (idea 325, committed CSV) -- B136, n=20, weekly")
    pg = OUT / "2026-09-07_is-TURNOVER-not-COUNT-the-real-n-dial_cloud.grid.csv"
    if pg.exists():
        p = pd.read_csv(pg)
        p = p[(p.panel == "B136") & (p.n.astype(str) == "20")]
        print(p[["m", "Sharpe_10", "H1_10", "H2_10", "OOS_Sharpe_10", "MaxDD_10",
                 "m4b_H2_10", "m4b_DD_10", "fail4b_10"]].to_string(index=False,
                 float_format=lambda x: f"{x:.4f}"))
        c = p[p.m == PRE_M].iloc[0]
        print(f"    -> the pre-registered cell fails 4b at 10 bps on: {c['fail4b_10']} "
              f"(H2 margin {c['m4b_H2_10']:+.4f}, DD margin {c['m4b_DD_10']:+.4f}).")
        print("    NOTE: the queue entry says ONE bar.  It is TWO -- the DD cap is live at "
              "m=20 (the band's held names drift, deepening MaxDD).  Corrected here.")
    else:
        print("    parent grid CSV not found; skipping the re-read")

    panels = {}
    print("\n[panels]")
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    panels["SMALL439"] = small_panel()

    gcsv = OUT / f"{SLUG}.grid.csv"
    if RESUME and gcsv.exists():
        analyse(pd.read_csv(gcsv), panels)
        return

    rows = []
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
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        print(f"    4b bars on this panel: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{so['Sharpe']:.3f}  "
              f"MaxDD>={-0.60*abs(ms_['MaxDD']):.2%}  CAGR>={0.70*ms_['CAGR']:.2%}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, BASE_FREQ)
        base = {c: (br - bt * c / 1e4).loc[start:] for c in COSTS}
        bm = metrics(base[10]); b1, b2 = hs(base[10]); bo = metrics(base[10].loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")

        if pname == "U56":
            print("\n[0b] GATES")
            wA = weights_from(sel_hard(rk, PRE_N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    fast_backtest vs engine.backtest (W): max|dr| {d1:.3e} max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    derived rung r(25) vs live backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            for fq in CADENCES:
                sb = sel_band(px, rk, PRE_N, 0, fq); sh = sel_hard(rk, PRE_N)
                reb = rebalance_mask(px.index, fq)
                dd = (sb[reb] != sh[reb]).values.sum()
                print(f"    sel_band(n={PRE_N}, m=0, {fq}) nests sel_hard on rebalance days: "
                      f"{dd} disagreements of {int(reb.sum()) * px.shape[1]}")
                assert dd == 0

        print(f"\n[A] GRID {pname} -- cadence x m, all points, n={PRE_N} fixed")
        hdr = f"    {'cad':>3} {'m':>3} {'turn/yr':>8} {'names':>6} {'gross':>6} |"
        hdr += " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} "
                          f"{'OOS':>6} {'4b':>2} {'4a':>2}" for c in COSTS)
        print(hdr)
        for fq in CADENCES:
            for m in MS:
                sel = sel_hard(rk, PRE_N) if m == 0 else sel_band(px, rk, PRE_N, m, fq)
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0, fq)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                rec = dict(panel=pname, cadence=fq, n=PRE_N, m=m, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), gross=gr.loc[start:].mean(),
                           breakeven_bps=breakeven(r0, t0, spy))
                line = f"    {fq:>3} {m:>3} {tpy:>8.2f} {rec['names']:>6.1f} {rec['gross']:>6.3f} |"
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, base[c])
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n':>2} {'Y' if ok4a else 'n':>2} |")
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
        # panel context for the analysis section
        rows[-1]  # noqa  (rows already carry panel; SPY context recomputed in analyse)
        for r_ in rows:
            if r_["panel"] == pname:
                r_.update(spy_H1=s1, spy_H2=s2, spy_OOS=so["Sharpe"], spy_CAGR=ms_["CAGR"],
                          spy_MaxDD=ms_["MaxDD"], base_H1=b1, base_H2=b2,
                          base_OOS=bo["Sharpe"], base_Sharpe=bm["Sharpe"])

    df = pd.DataFrame(rows)
    df.to_csv(gcsv, index=False)
    analyse(df, panels)


def analyse(df, panels):
    # ---------------------------------------------------------- [B] the verdict
    print("\n\n[B] THE PRE-REGISTERED CELL: B136, n=20, m=20 -- does any cadence clear 4b?")
    print(f"    {'cad':>3} {'c':>3} {'Sharpe':>7} {'H2':>7} {'H2 marg':>8} {'DD marg':>8} "
          f"{'OOS marg':>9} {'CAGR marg':>10} {'H1 marg':>8}  4b  fails")
    cell = df[(df.panel == PRE_PANEL) & (df.m == PRE_M)]
    passes = []
    for _, r in cell.iterrows():
        for c in COSTS:
            ok = bool(r[f"keep4b_{c}"])
            if ok and c == 10:
                passes.append(r["cadence"])
            print(f"    {r['cadence']:>3} {c:>3} {r[f'Sharpe_{c}']:>7.3f} {r[f'H2_{c}']:>7.3f} "
                  f"{r[f'm4b_H2_{c}']:>+8.4f} {r[f'm4b_DD_{c}']:>+8.4f} {r[f'm4b_OOS_{c}']:>+9.4f} "
                  f"{r[f'm4b_CAGR_{c}']:>+10.4f} {r[f'm4b_H1_{c}']:>+8.4f}  "
                  f"{'Y' if ok else 'n'}   {r[f'fail4b_{c}'] if isinstance(r[f'fail4b_{c}'], str) else ''}")
    print(f"\n    DECISION: cadences clearing ALL FIVE 4b bars at 10 bps: "
          f"{passes if passes else 'NONE'}")
    print("    -> " + ("cross-universe: idea 325's PARK goes to Sunday review"
                       if passes else
                       "the parent's candidate is a U56 OBJECT and is labelled one"))

    # ---------------------------------------------------------- [C] is H2 the binding bar?
    print("\n[C] WHICH BAR BINDS on the pre-registered cell (10 bps, per cadence)?")
    for _, r in cell.iterrows():
        marg = {k: r[f"m4b_{k}_10"] for k in ("H1", "H2", "OOS", "DD", "CAGR")}
        worst = min(marg, key=marg.get)
        print(f"    {r['cadence']}: " + "  ".join(f"{k} {v:+.4f}" for k, v in marg.items())
              + f"   -> tightest: {worst}")

    # ---------------------------------------------------------- [D] cadence effect on H2, all m
    print("\n[D] H2 MARGIN vs SPY at 10 bps, cadence x m (context axis; verdict is the m=20 row)")
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        print(f"    {pname}")
        print("        " + f"{'m':>4}" + "".join(f"{fq:>12}" for fq in CADENCES))
        for m in MS:
            line = f"        {m:>4}"
            for fq in CADENCES:
                v = d[(d.m == m) & (d.cadence == fq)]
                line += f"{v.iloc[0]['m4b_H2_10']:>+12.4f}" if len(v) else f"{'-':>12}"
            print(line + ("   <- pre-registered m" if m == PRE_M else ""))

    print("\n[E] 4b / 4a PASS COUNTS over the whole reported grid (3 panels x 3 cadences x 5 m)")
    for c in COSTS:
        n4b = int(df[f"keep4b_{c}"].sum()); n4a = int(df[f"keep4a_{c}"].sum())
        print(f"    c={c:>2} bps: 4b {n4b}/{len(df)}   4a {n4a}/{len(df)}")
        if n4b:
            p = df[df[f"keep4b_{c}"]]
            for _, r in p.iterrows():
                print(f"        4b PASS  {r['panel']:>9} {r['cadence']} m={r['m']:<3} "
                      f"{r[f'CAGR_{c}']:.2%} / {r[f'Sharpe_{c}']:.3f} / {r[f'MaxDD_{c}']:.2%} "
                      f"OOS {r[f'OOS_Sharpe_{c}']:.3f}  breakeven {r['breakeven_bps']:.1f} bps")

    # ---------------------------------------------------------- [F] rule 8 walk-forward
    print("\n[F] RULE 8 WALK-FORWARD: (cadence, m) chosen on 2008-2016 IS Sharpe @10 bps, "
          "2017-2026 read once")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        pick = d.loc[d["IS_Sharpe_10"].idxmax()]
        best = d.loc[d["OOS_Sharpe_10"].idxmax()]
        anch = d[(d.cadence == ANCHOR[0]) & (d.m == ANCHOR[1])].iloc[0]
        pre = d[(d.cadence == "W") & (d.m == PRE_M)].iloc[0]
        print(f"\n    {pname}: SPY OOS {pick['spy_OOS']:.3f} | RULES v2 OOS {pick['base_OOS']:.3f}")
        for lbl, r in (("IS pick", pick), ("pre-reg (W,m=20)", pre),
                       ("anchor (W,m=0)", anch), ("OOS best", best)):
            print(f"        {lbl:<18} cad={r['cadence']} m={r['m']:<3} "
                  f"IS {r['IS_Sharpe_10']:.3f} | OOS Sharpe {r['OOS_Sharpe_10']:.3f} "
                  f"CAGR {r['OOS_CAGR_10']:.2%} MaxDD {r['OOS_MaxDD_10']:.2%}")
        print(f"        regret of the IS chooser (OOS best - IS pick): "
              f"{best['OOS_Sharpe_10'] - pick['OOS_Sharpe_10']:+.4f}")
        print(f"        IS pick vs anchor OOS: {pick['OOS_Sharpe_10'] - anch['OOS_Sharpe_10']:+.4f}"
              f" | vs SPY: {pick['OOS_Sharpe_10'] - pick['spy_OOS']:+.4f}"
              f" | vs RULES v2: {pick['OOS_Sharpe_10'] - pick['base_OOS']:+.4f}")
        wf.append(dict(panel=pname, pick_cadence=pick["cadence"], pick_m=pick["m"],
                       IS_Sharpe=pick["IS_Sharpe_10"], OOS_Sharpe=pick["OOS_Sharpe_10"],
                       OOS_CAGR=pick["OOS_CAGR_10"], OOS_MaxDD=pick["OOS_MaxDD_10"],
                       anchor_OOS=anch["OOS_Sharpe_10"], prereg_OOS=pre["OOS_Sharpe_10"],
                       oosbest_OOS=best["OOS_Sharpe_10"],
                       regret=best["OOS_Sharpe_10"] - pick["OOS_Sharpe_10"],
                       spy_OOS=pick["spy_OOS"], base_OOS=pick["base_OOS"]))
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    print("\n[G] BREAKEVEN (highest cost rung at which all five 4b bars still hold), bps")
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        print(f"    {pname}")
        print("        " + f"{'m':>4}" + "".join(f"{fq:>10}" for fq in CADENCES))
        for m in MS:
            line = f"        {m:>4}"
            for fq in CADENCES:
                v = d[(d.m == m) & (d.cadence == fq)]
                line += f"{v.iloc[0]['breakeven_bps']:>10.1f}" if len(v) else f"{'-':>10}"
            print(line)


if __name__ == "__main__":
    main()
