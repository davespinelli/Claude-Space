#!/usr/bin/env python3
"""QUEUE idea 87 — interior-4b-passes-are-unselectable (cloud lane, 2026-09-04).

Question
--------
Ideas 66 (gross) and 15 (crypto cap) each produced a cross-universe 4b pass at an
*interior* value of their risk parameter (g = 0.90; cap = 5%), and rule 8 threw both away,
because rule 8 selects on in-sample Sharpe and IS Sharpe is (nearly) monotone in a pure
risk lever while 4b's drawdown cap is not.  The claim to test is therefore about
**PROTOCOL's selection rule, not about those ideas**:

    If rule 8 maximised IS Sharpe SUBJECT TO the in-sample 4b drawdown cap being met with
    margin m, would it recover the interior arm out of sample?

If yes, several published PARKs were selection failures and rule 8 should be amended.
If no, the interior passes are sample artefacts and the ideas were correctly parked.

Design (PROTOCOL rules 1-8)
---------------------------
Universes: universe.json (56) and universe_broad.json (136).  Cross-universe = both.
           SURVIVORSHIP: current constituents; absolute CAGRs optimistic.  This run
           compares *selection rules on a common grid*, so the bias hits every arm alike.
Grids    : six 1-parameter risk grids, each re-run from scratch here (no numbers are taken
           on trust from the earlier runs; the harness reproduces the published anchors):
             GROSS/top20   g in {0.50,0.60,0.70,0.75,0.80,0.90,1.00}   (idea 66, idea 2's book)
             GROSS/EWall   same g grid                                  (idea 66)
             CRYPTO/CAND20 cap in {0,0.05,0.10,0.15}, matched funding, `same` gate (idea 15)
             CRYPTO/EWall  same cap grid                                (idea 15)
             BAND/ew-all   band in {0,0.02,0.03,0.05,0.08}              (idea 57)
             N/ranked      n in {5,10,15,20,30,40}                      (idea 2)
Params   : exactly 2 -- the grid parameter and the selection margin m in {0,1,2} pp.
           Every grid point is printed with IS, OOS and full-sample statistics.
Selection: fitted on 2009-2016 ONLY, evaluated untouched on 2017-2026.
             R0    argmax IS Sharpe                                    (incumbent rule 8)
             Rm(m) argmax IS Sharpe s.t. |IS MaxDD| <= 0.60*|SPY_IS MaxDD| - m pp  (m TIGHTENS the cap)
                                     and IS CAGR  >= 0.70*SPY_IS CAGR
           Pre-registered outcome measures, fixed before any OOS number is read:
             (a) does the selected arm pass 4b on the OOS window alone?
             (b) OOS Sharpe of the selected arm vs the grid's OOS-best and vs the default arm;
             (c) does the selection recover the arm that passes full-sample cross-universe 4b?
Execution: weekly, weights at close t applied t+1, 10 bps per unit turnover.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

COST, FREQ, MAX_VOL = 10, "W", 0.60
GROSS = 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
CRYPTO = ["BTC-USD", "ETH-USD"]
MARGINS = [0.0, 0.01, 0.02]
SCRIPT = "research/backtests/2026-09-04_interior-4b-selection_cloud.py"


# ---------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def trend(px, band=0.0):
    ma = px.rolling(200).mean()
    if band <= 0:
        return (px > ma).fillna(False)
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def eligible(px, band=0.0):
    return (vol20(px) < MAX_VOL) & trend(px, band)


def w_ranked(n=20, g=GROSS, band=0.0):
    def f(px):
        rank = composite(px).where(eligible(px, band)).rank(axis=1, ascending=False)
        return (rank <= n).astype(float) * (g / n)
    return f


def w_ewall(g=GROSS, band=0.0):
    def f(px):
        e = eligible(px, band).astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
    return f


def w_crypto(base_fn, cap):
    """idea 15's `matched`/`same` sleeve: cap per crypto name, funded by scaling the
    equity leg down so realised gross is unchanged; crypto uses v1's own 200d+vol20 gate."""
    def f(px):
        eq_cols = [c for c in px.columns if c not in CRYPTO]
        w_eq = base_fn(px[eq_cols])
        w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        w[w_eq.columns] = w_eq.values
        if cap <= 0:
            return w
        pxc = px[CRYPTO]
        gate = ((pxc > pxc.rolling(200).mean()) & (vol20(pxc) < MAX_VOL)).fillna(False)
        wc = gate.astype(float) * cap
        gsum = w_eq.sum(axis=1)
        keep = wc.sum(axis=1).clip(upper=gsum)
        scale = np.divide(keep, wc.sum(axis=1).replace(0, np.nan)).fillna(0.0)
        wc = wc.mul(scale, axis=0)
        eq_scale = np.divide(gsum - keep, gsum.replace(0, np.nan)).fillna(0.0)
        w[w_eq.columns] = w_eq.mul(eq_scale, axis=0).values
        w[CRYPTO] = wc[CRYPTO].values
        return w
    return f


# ---------------------------------------------------------------- metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4b_window(r, spy):
    """4b's three absolute bars on one window (Sharpe/DD/CAGR vs SPY on the same days)."""
    c, s, dd = m3(r); sc, ss, sdd = m3(spy)
    bad = []
    if s <= ss: bad.append("Sh")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def fail4b_full(r, spy):
    c, s, dd = m3(r); h1, h2 = halves(r)
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    o, so = metrics(r.loc[OOS_START:])["Sharpe"], metrics(spy.loc[OOS_START:])["Sharpe"]
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if o <= so: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def run(px, fn, start):
    res = backtest(px, fn(px), cost_bps=COST, freq=FREQ)
    r = res["returns"].loc[start:]
    return r, res["turnover"].loc[start:].sum() / (len(r) / 252)


# ---------------------------------------------------------------- grids
def grids(px, px_c):
    """(name, default_value, {value: weights_fn, ...}, panel) for each risk grid."""
    G = [
        ("GROSS/top20", 0.75, {g: w_ranked(20, g) for g in [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]}, "eq"),
        ("GROSS/EWall", 0.75, {g: w_ewall(g) for g in [0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]}, "eq"),
        ("BAND/ew-all", 0.00, {b: w_ewall(GROSS, b) for b in [0.00, 0.02, 0.03, 0.05, 0.08]}, "eq"),
        ("N/ranked", 20, {n: w_ranked(n) for n in [5, 10, 15, 20, 30, 40]}, "eq"),
    ]
    if px_c is not None:
        G += [
            ("CRYPTO/CAND20", 0.00, {c: w_crypto(w_ranked(20), c) for c in [0.00, 0.05, 0.10, 0.15]}, "cry"),
            ("CRYPTO/EWall", 0.00, {c: w_crypto(w_ewall(), c) for c in [0.00, 0.05, 0.10, 0.15]}, "cry"),
        ]
    return G


# ---------------------------------------------------------------- one universe
def sweep(px, px_c, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]
    sc, ss, sdd = m3(spy); s1, s2 = halves(spy)
    ic, isr, idd = m3(spy_is)
    oc, osr, odd = m3(spy_oos)

    print("\n" + "=" * 138)
    print(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()}")
    print(f"SPY full {sc:.1%}/{ss:.3f}/{sdd:.1%} halves {s1:.3f}/{s2:.3f} | "
          f"IS(->{IS_END[:4]}) {ic:.1%}/{isr:.3f}/{idd:.1%} | OOS({OOS_START[:4]}->) {oc:.1%}/{osr:.3f}/{odd:.1%}")
    print(f"IS 4b bars used by Rm: MaxDD >= {0.60*idd:.2%} (+m, i.e. tighter)   CAGR >= {0.70*ic:.2%}")
    print(f"OOS 4b bars: Sharpe > {osr:.3f}   MaxDD >= {0.60*odd:.2%}   CAGR >= {0.70*oc:.2%}")
    print("=" * 138)

    rows = []
    for gname, default, arms, panel in grids(px, px_c):
        P = px if panel == "eq" else px_c
        sp = P["SPY"].pct_change().fillna(0).loc[start:]
        sp_is, sp_oos = sp.loc[:IS_END], sp.loc[OOS_START:]
        print(f"\n[{tag}] grid {gname}   (default arm = {default})")
        print(f"  {'param':>7}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}{'H1':>7}{'H2':>7}"
              f"{'IS_Sh':>8}{'IS_DD':>8}{'IS_CAGR':>9}{'OOS_Sh':>8}{'OOS_DD':>8}{'OOS_CAGR':>10}"
              f"{'turn':>6}  {'4b full':<16}{'4b OOS'}")
        for v, fn in arms.items():
            r, tn = run(P, fn, start)
            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
            c, s, dd = m3(r); h1, h2 = halves(r)
            ic_, is_, idd_ = m3(r_is)
            oc_, os_, odd_ = m3(r_oos)
            f_full = fail4b_full(r, sp)
            f_oos = fail4b_window(r_oos, sp_oos)
            print(f"  {v:>7}{c:8.1%}{s:8.3f}{dd:8.1%}{h1:7.3f}{h2:7.3f}"
                  f"{is_:8.3f}{idd_:8.1%}{ic_:9.1%}{os_:8.3f}{odd_:8.1%}{oc_:10.1%}{tn:6.1f}  "
                  f"{','.join(f_full) or 'PASS':<16}{','.join(f_oos) or 'PASS'}")
            rows.append(dict(universe=tag, grid=gname, param=v, is_default=(v == default),
                             CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2, turn=tn,
                             IS_Sh=is_, IS_DD=idd_, IS_CAGR=ic_,
                             OOS_Sh=os_, OOS_DD=odd_, OOS_CAGR=oc_,
                             IS_DD_bar=0.60 * m3(sp_is)[2], IS_CAGR_bar=0.70 * m3(sp_is)[0],
                             pass4b_full=not f_full, pass4b_oos=not f_oos,
                             fail_full=",".join(f_full), fail_oos=",".join(f_oos)))
        d = pd.DataFrame([x for x in rows if x["grid"] == gname and x["universe"] == tag])
        pr = d["param"].rank()
        print(f"  monotonicity check (the premise): Spearman(param, IS Sharpe) "
              f"{pr.corr(d.IS_Sh.rank()):+.3f}   Spearman(param, |IS MaxDD|) "
              f"{pr.corr(d.IS_DD.abs().rank()):+.3f}{' (IS MaxDD is constant across the grid)' if d.IS_DD.nunique() == 1 else ''}   Spearman(param, OOS Sharpe) "
              f"{pr.corr(d.OOS_Sh.rank()):+.3f}")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- selection rules
def select(d, m):
    """argmax IS Sharpe subject to IS 4b DD cap with margin m pp, and the IS CAGR floor.
    m is None -> unconstrained (incumbent rule 8)."""
    if m is None:
        return d.loc[d.IS_Sh.idxmax()], len(d)
    # both quantities are negative: adding m raises the floor, i.e. TIGHTENS the cap by m pp
    ok = d[(d.IS_DD >= d.IS_DD_bar + m) & (d.IS_CAGR >= d.IS_CAGR_bar)]
    if ok.empty:
        return None, 0
    return ok.loc[ok.IS_Sh.idxmax()], len(ok)


def rule8(df):
    print("\n" + "=" * 138)
    print("RULE 8 — selection fitted on 2009-2016 only, evaluated untouched on 2017-2026")
    print("=" * 138)
    out = []
    for (u, g), d in df.groupby(["universe", "grid"], sort=False):
        best_oos = d.loc[d.OOS_Sh.idxmax()]
        dflt = d[d.is_default].iloc[0]
        interior = d[d.pass4b_full & ~d.is_default]
        print(f"\n[{u}] {g}   default arm {dflt.param} (OOS Sh {dflt.OOS_Sh:.3f})   "
              f"grid OOS-best {best_oos.param} ({best_oos.OOS_Sh:.3f})   "
              f"full-sample 4b passes: {sorted(d[d.pass4b_full].param.tolist()) or 'none'}")
        print(f"  {'rule':<10}{'feasible':>9}{'pick':>8}{'IS Sh':>8}{'OOS Sh':>8}"
              f"{'vs default':>11}{'vs OOS-best':>12}   {'4b OOS':<14}{'= a full-4b arm?'}")
        for label, m in [("R0", None)] + [(f"Rm(m={int(x*100)}pp)", x) for x in MARGINS]:
            pick, nfeas = select(d, m)
            if pick is None:
                print(f"  {label:<10}{0:>9}{'-':>8}{'':>8}{'':>8}{'':>11}{'':>12}   infeasible")
                out.append(dict(universe=u, grid=g, rule=label, pick=None))
                continue
            print(f"  {label:<10}{nfeas:>9}{pick.param:>8}{pick.IS_Sh:8.3f}{pick.OOS_Sh:8.3f}"
                  f"{pick.OOS_Sh - dflt.OOS_Sh:+11.3f}{pick.OOS_Sh - best_oos.OOS_Sh:+12.3f}   "
                  f"{pick.fail_oos or 'PASS':<14}{'YES' if pick.pass4b_full else 'no'}")
            out.append(dict(universe=u, grid=g, rule=label, pick=pick.param,
                            IS_Sh=pick.IS_Sh, OOS_Sh=pick.OOS_Sh,
                            vs_default=pick.OOS_Sh - dflt.OOS_Sh,
                            vs_oosbest=pick.OOS_Sh - best_oos.OOS_Sh,
                            pass4b_oos=bool(pick.pass4b_oos), pass4b_full=bool(pick.pass4b_full),
                            interior=bool(pick.pass4b_full and not pick.is_default),
                            n_interior=len(interior)))
    sel = pd.DataFrame(out)
    sel.to_csv(ROOT / "research" / "backtests" / "2026-09-04_interior-4b-selection_cloud.selections.csv",
               index=False)
    return sel


def cross_universe(df, sel):
    print("\n" + "=" * 138)
    print("CROSS-UNIVERSE — an arm counts only if it passes on BOTH lists")
    print("=" * 138)
    p = df.pivot_table(index=["grid", "param"], columns="universe", values="pass4b_full")
    both = p[p.sum(axis=1) == 2]
    print(f"  full-sample 4b on both universes: {len(both)} arms")
    for (g, v) in both.index:
        print(f"    {g:<16} param {v}")
    q = sel.dropna(subset=["pick"])
    print("\n  Does a selection rule pick a both-universe arm, per grid?")
    for g, d in q.groupby("grid", sort=False):
        ok = {v for (gg, v) in both.index if gg == g}
        for rule, dd in d.groupby("rule", sort=False):
            hits = [f"{r.universe.split('.')[0]}:{r.pick}{'*' if r.pick in ok else ''}"
                    for _, r in dd.iterrows()]
            agree = len(set(dd.pick)) == 1
            print(f"    {g:<16}{rule:<12}{' '.join(hits):<34}"
                  f"{'same pick on both lists' if agree else 'DIFFERENT pick per list'}"
                  f"{'  <- recovers a both-universe arm' if ok and set(dd.pick) & ok else ''}")


def main():
    frames = []
    for tag, kw in (("universe.json", {}), ("universe_broad.json", {"broad": True})):
        px = load_universe(**kw)
        yrs = px.index.to_series().groupby(px.index.year).count()
        if yrs.loc[2015:2024].max() > 300:
            sys.exit("!! CALENDAR-DAY INDEX DETECTED (idea 38) -- aborting.")
        raw = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)
        px_c = None
        if all(c in raw.columns for c in CRYPTO):
            px_c = pd.concat([px, raw[CRYPTO].reindex(px.index).ffill()], axis=1)
        frames.append(sweep(px, px_c, tag))
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(ROOT / "research" / "backtests" / "2026-09-04_interior-4b-selection_cloud.grid.csv", index=False)

    sel = rule8(df)
    cross_universe(df, sel)

    print("\n" + "=" * 138)
    print("SUMMARY")
    print("=" * 138)
    q = sel.dropna(subset=["pick"])
    print(f"  grid points: {len(df)}   selections attempted: {len(sel)}   infeasible: {sel.pick.isna().sum()}")
    for rule, d in q.groupby("rule", sort=False):
        n_oos = int(d.pass4b_oos.astype(bool).sum())
        n_int = int(d.interior.astype(bool).sum())
        n_full = int(d.pass4b_full.astype(bool).sum())
        print(f"  {rule:<12} OOS Sharpe vs default arm: mean {d.vs_default.mean():+.3f}  "
              f"wins {int((d.vs_default > 1e-9).sum())}/{len(d)}   |  vs grid OOS-best: mean "
              f"{d.vs_oosbest.mean():+.3f}  hits {int((d.vs_oosbest >= -1e-9).sum())}/{len(d)}   |  "
              f"picks pass OOS-4b {n_oos}/{len(d)}   |  picks a full-sample-4b arm {n_full}/{len(d)}"
              f"   |  picks an INTERIOR full-4b arm {n_int}/{len(d)}")
    print("\n  Premise check (IS Sharpe monotone in the risk parameter?) — per grid Spearman is "
          "printed above each grid; see console.")
    print(f"  Interior (non-default) full-sample 4b arms available anywhere: "
          f"{int((df.pass4b_full & ~df.is_default).sum())} of {len(df)} points.")


if __name__ == "__main__":
    main()
