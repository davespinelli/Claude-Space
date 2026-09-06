#!/usr/bin/env python3
"""Idea 289 - "is-the-soft-200d-tilt-inside-the-score-doing-the-gate-s-job".

The question
------------
Idea 56 (cloud, 2026-09-06) decomposed RULES v1's two-clause eligibility gate on the two
large-cap panels and found the HARD 200d gate is bit-identical to NO gate at n=5.  The
reason is that `research/scan.py`'s composite is not gate-free to begin with: it already
carries a SOFT trend tilt,

    s = comp * (0.5 + 0.5 * above200)

so a below-200d name is ranked at HALF its composite before any eligibility filter runs.
At small n the tilt alone is enough to keep every below-200d name out of the top n, and
the hard gate then has nothing left to remove.  That makes idea 56's "the 200d clause is
INERT" reading ambiguous: the clause may be inert because trend does not matter, or inert
because the tilt is already doing its job.  This run separates the two.

The generalisation actually swept
---------------------------------
    s(t) = comp * (1 - t + t * above200)          with the HARD gate switched OFF

    t = 0.00   no trend information in the score at all (pure composite)
    t = 0.25   quarter tilt
    t = 0.50   the LIVE scan.py form
    t = 0.75   three-quarter tilt
    t = 1.00   hard MULTIPLICATIVE gate - a below-200d name scores exactly 0

t = 1.00 with the hard gate OFF and the hard gate ON differ only in tie handling: at t=1
every below-200d name scores 0 and they tie, so they can still enter the book when fewer
than n names are above their average, whereas the hard gate makes them unrankable.  The
script counts the days on which the two selections actually differ, which is the direct
measurement idea 56's "bit-identical" claim needs.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. tilt t in {0.00, 0.25, 0.50, 0.75, 1.00}
    2. n     in {5, 10, 20}

Reported decomposition axes - never selected on; every cell is printed and the rule-8
selection runs strictly INSIDE each (universe, convention, gate) cell:
    universe    U56 = research/universe.json, B136 = research/universe_broad.json
    convention  dg = de-gross (gross/n each, gated-out weight to CASH, the live convention)
                rw = re-spread (always deploy 75% across however many names are held)
    gate        OFF = rank the tilted score over every priced name (the idea's question)
                MA  = the HARD 200d gate ALONE on top of the tilted score.  This is the
                      form idea 56 called inert, and it is the only correct comparand for
                      "tilt vs gate": RULES v1's filter also carries `vol20<0.60`, which
                      idea 56 showed is the destructive half, so pricing OFF against the
                      full filter would attribute the vol clause's damage to the 200d gate.
                V1  = RULES v1's full `above200 & vol20<0.60` filter (the incumbent form;
                      t=0.5/V1/n=20/dg is idea 2's KEEP candidate), reported for continuity

Construction held fixed: composite of research/scan.py with NO vol scaler, top n equal
weighted at 75% gross, weekly rebalance, 10 bps per unit turnover, weights decided at
close t applied at t+1 (engine does this).  Nothing in scan.py, RULES.md, bot.py or
baseline.py is touched - the tilt is re-implemented locally.

Grid = 5 tilts x 3 n x 2 universes x 2 conventions x 3 gates = 180 book cells, ALL
reported, plus RULES v2 (live book), RULES v1 and SPY on each universe.

Rule 8 walk-forward: parameters (t, n) chosen on <= 2016-12-31 by in-sample Sharpe inside
each (universe, convention, gate) cell, then 2017-2026 read ONCE.  Reported against SPY
OOS, RULES v2 OOS, the pre-registered anchor (t=0.5, n=20 - the live tilt at idea 2's
width) and the best OOS cell in the same block (regret).

Both KEEP paths are evaluated on every cell:
    4a  Sharpe > RULES v2 in BOTH halves AND MaxDD no worse than RULES v2's
    4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's

Outputs: .grid.csv, .walkforward.csv, .console.txt, .result.md
Deterministic, standalone, no network.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

COST, FREQ, GROSS = 10, "W", 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TILTS = [0.00, 0.25, 0.50, 0.75, 1.00]
NS = [5, 10, 20]
CONVS = ["dg", "rw"]
GATES = ["OFF", "MA", "V1"]
MAX_VOL = 0.60
ANCHOR = (0.50, 20)                        # the live tilt at idea 2's width, pre-registered


# ------------------------------------------------------------------ score
def composite(px):
    """scan.py's rank composite, WITHOUT the trend tilt and without the vol scaler."""
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def tilted(px, comp, above, t):
    """s(t) = comp * (1 - t + t*above).  t=0.5 reproduces baseline.score exactly."""
    return comp * (1.0 - t + t * above.astype(float))


def selection(px, comp, above, vol20, t, n, gate):
    s = tilted(px, comp, above, t)
    if gate == "MA":                       # the HARD 200d gate, on its own
        s = s.where(above)
    elif gate == "V1":                     # RULES v1's full eligibility filter
        s = s.where(above & (vol20 < MAX_VOL))
    return s.rank(axis=1, ascending=False) <= n


def weights_of(sel, n, conv):
    if conv == "dg":
        return sel.astype(float) * (GROSS / n)
    cnt = sel.sum(axis=1)
    return sel.astype(float).div(cnt.replace(0, np.nan), axis=0) * GROSS


def st(r, lo=None, hi=None):
    x = r.loc[lo:hi] if (lo or hi) else r
    m = metrics(x); return m["CAGR"], m["Sharpe"], m["MaxDD"]


def row_of(r):
    h = len(r) // 2
    c, s, d = st(r)
    oc, os_, od = st(r, OOS_START)
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=metrics(r.iloc[:h])["Sharpe"],
                H2=metrics(r.iloc[h:])["Sharpe"], IS_Sharpe=st(r, None, IS_END)[1],
                IS_MaxDD=st(r, None, IS_END)[2], OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_paths(x, spy, v2):
    a = (x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
    b = (x["H1"] > spy["H1"] and x["H2"] > spy["H2"] and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and x["MaxDD"] >= 0.60 * spy["MaxDD"] and x["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def first_fail_4b(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]), ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok:
            return lbl
    return "-"


def main():
    unis = {"U56": load_universe(), "B136": load_universe(broad=True)}
    rows, ident_rows, refs = [], [], {}

    P("=" * 132)
    P("Idea 289  is-the-soft-200d-tilt-inside-the-score-doing-the-gate-s-job   (cloud, 2026-09-06)")
    P("=" * 132)
    P(f"s(t) = comp * (1 - t + t*above200);  t=0 no tilt, t=0.5 = the LIVE scan.py form, t=1 hard "
      f"multiplicative gate.")
    P(f"Costs {COST} bps/unit turnover, gross {GROSS}, weekly, next-day execution. "
      f"Tuned: t in {TILTS} x n in {NS}. Reported: universe x convention x hard-gate.")

    for uname, px in unis.items():
        px = px.dropna(how="all").ffill()
        tr = [c for c in px.columns if c != "SPY"]
        sub = px[tr]
        start = px.index[260]
        comp = composite(sub)
        above = sub > sub.rolling(200).mean()
        vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)

        yrs = px.index.to_series().groupby(px.index.year).count()
        P(f"\n{'='*132}\n{uname}: {len(tr)} tradables + SPY, {px.index[0].date()} .. {px.index[-1].date()}, "
          f"scored from {start.date()}")
        P(f"  index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, "
          f"2024 {yrs.get(2024)}")
        P(f"  mean share of tradables above their 200d MA: {100*above.loc[start:].sum(axis=1).mean()/len(tr):.1f}%")
        P("=" * 132)

        spy = row_of(px["SPY"].pct_change().fillna(0).loc[start:])
        v2 = row_of(backtest(px, rules_v2_weights(sub).reindex(columns=px.columns).fillna(0.0),
                             cost_bps=COST, freq=FREQ)["returns"].loc[start:])
        v1 = row_of(backtest(px, rules_v1_weights(sub).reindex(columns=px.columns).fillna(0.0),
                             cost_bps=COST, freq=FREQ)["returns"].loc[start:])
        refs[uname] = dict(SPY=spy, v2=v2, v1=v1)
        for tag, x in (("SPY", spy), ("RULES v2 (live)", v2), ("RULES v1", v1)):
            P(f"  {tag:16s} CAGR {x['CAGR']:6.2%}  Sharpe {x['Sharpe']:.3f}  MaxDD {x['MaxDD']:7.2%}"
              f"  H1/H2 {x['H1']:.3f}/{x['H2']:.3f}"
              f"  OOS {x['OOS_CAGR']:6.2%}/{x['OOS_Sharpe']:.3f}/{x['OOS_MaxDD']:7.2%}")
        P(f"  4b bars on {uname}: Sharpe > SPY in both halves AND OOS, MaxDD >= {0.60*spy['MaxDD']:.2%}, "
          f"CAGR >= {0.70*spy['CAGR']:.2%}")

        # -- how much of the hard gate is left once the tilt has run -------
        P(f"\n-- {uname}: SELECTION OVERLAP.  Days on which top-n(hard MA200 gate) differs from "
          f"top-n(no gate), and mean count of held names BELOW their 200d MA with no gate --")
        P(f"  {'t':>5s} {'n':>3s} {'days sel differs':>17s} {'of days':>8s} {'% days':>7s} "
          f"{'mean below-MA held (OFF)':>25s} {'mean names MA is short of n':>28s}")
        idx = sub.loc[start:].index
        for t in TILTS:
            for n in NS:
                so = selection(sub, comp, above, vol20, t, n, "OFF").loc[start:]
                sn = selection(sub, comp, above, vol20, t, n, "MA").loc[start:]
                diff = int((so != sn).any(axis=1).sum())
                below = float((so & ~above.loc[start:]).sum(axis=1).mean())
                short = float((n - sn.sum(axis=1)).clip(lower=0).mean())
                ident_rows.append(dict(universe=uname, tilt=t, n=n, days=len(idx),
                                       days_selection_differs=diff,
                                       pct_days=100 * diff / len(idx),
                                       mean_belowMA_held_gateOFF=below,
                                       mean_shortfall_gateMA=short))
                P(f"  {t:5.2f} {n:3d} {diff:17d} {len(idx):8d} {100*diff/len(idx):6.1f}% "
                  f"{below:25.3f} {short:28.3f}")

        # -- the grid ------------------------------------------------------
        for gate in GATES:
            for conv in CONVS:
                P(f"\n-- {uname} / hard gate {gate} / convention {conv} "
                  f"({'de-gross to cash' if conv=='dg' else 're-spread 75% over the held names'}) --")
                P(f"  {'t':>5s} {'n':>3s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
                  f"{'IS_S':>6s} {'OOS_C':>7s} {'OOS_S':>6s} {'OOS_DD':>8s} {'turn/yr':>8s} {'gross':>6s} "
                  f"{'4a':>5s} {'4b':>5s} {'fail4b':>7s}")
                for t in TILTS:
                    for n in NS:
                        sel = selection(sub, comp, above, vol20, t, n, gate)
                        w = weights_of(sel, n, conv).fillna(0.0).reindex(columns=px.columns).fillna(0.0)
                        res = backtest(px, w, cost_bps=COST, freq=FREQ)
                        r = res["returns"].loc[start:]
                        x = row_of(r)
                        turn = res["turnover"].loc[start:].sum() / (len(r) / 252)
                        gross = res["weights"].loc[start:].sum(axis=1).mean()
                        a, b = keep_paths(x, spy, v2)
                        fb = first_fail_4b(x, spy)
                        rows.append(dict(universe=uname, gate=gate, conv=conv, tilt=t, n=n, **x,
                                         turnover_yr=turn, mean_gross=gross, pass4a=a, pass4b=b,
                                         first_fail_4b=fb, spy_S=spy["Sharpe"], spy_H1=spy["H1"],
                                         spy_H2=spy["H2"], spy_OOS_S=spy["OOS_Sharpe"],
                                         spy_CAGR=spy["CAGR"], spy_DD=spy["MaxDD"],
                                         v2_S=v2["Sharpe"], v2_H1=v2["H1"], v2_H2=v2["H2"],
                                         v2_DD=v2["MaxDD"], v2_OOS_S=v2["OOS_Sharpe"]))
                        P(f"  {t:5.2f} {n:3d} {x['CAGR']:7.2%} {x['Sharpe']:7.3f} {x['MaxDD']:8.2%} "
                          f"{x['H1']:6.3f} {x['H2']:6.3f} {x['IS_Sharpe']:6.3f} {x['OOS_CAGR']:7.2%} "
                          f"{x['OOS_Sharpe']:6.3f} {x['OOS_MaxDD']:8.2%} {turn:8.2f} {gross:6.3f} "
                          f"{str(a):>5s} {str(b):>5s} {fb:>7s}")

    grid = pd.DataFrame(rows)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(ident_rows).to_csv(f"{OUT}.overlap.csv", index=False)

    # ---------------- is the TILT load-bearing? --------------------------
    P(f"\n{'='*132}\nQ1  IS THE TILT LOAD-BEARING?   dSharpe and dMaxDD vs t=0 (no trend information), "
      f"hard gate OFF\n{'='*132}")
    for uname in unis:
        for conv in CONVS:
            d = grid[(grid.universe == uname) & (grid.conv == conv) & (grid.gate == "OFF")]
            P(f"\n  {uname} / OFF / {conv}")
            P(f"    {'n':>3s} {'S(t=0)':>8s} " + " ".join(f"{'dS t='+f'{t:.2f}':>10s}" for t in TILTS[1:])
              + "   " + " ".join(f"{'dDD t='+f'{t:.2f}':>11s}" for t in TILTS[1:]))
            for n in NS:
                b0 = d[(d.tilt == 0.0) & (d.n == n)].iloc[0]
                P(f"    {n:3d} {b0.Sharpe:8.3f} " + " ".join(
                    f"{d[(d.tilt==t)&(d.n==n)].iloc[0].Sharpe-b0.Sharpe:+10.3f}" for t in TILTS[1:])
                  + "   " + " ".join(
                    f"{d[(d.tilt==t)&(d.n==n)].iloc[0].MaxDD-b0.MaxDD:+11.2%}" for t in TILTS[1:]))

    for g in ("MA", "V1"):
        lbl = "the HARD 200d GATE alone" if g == "MA" else "RULES v1's FULL filter (200d AND vol20<0.60)"
        P(f"\n{'='*132}\nQ2{'a' if g=='MA' else 'b'}  IS {lbl} LOAD-BEARING ONCE THE TILT IS THERE?"
          f"   {g} minus OFF at the same (t, n)\n{'='*132}")
        for uname in unis:
            for conv in CONVS:
                P(f"\n  {uname} / {conv}   dSharpe ({g} - OFF) / dCAGR / dMaxDD")
                P(f"    {'t':>5s} " + " ".join(f"{'n='+str(n):>26s}" for n in NS))
                for t in TILTS:
                    cells = []
                    for n in NS:
                        on = grid[(grid.universe==uname)&(grid.conv==conv)&(grid.gate==g)&(grid.tilt==t)&(grid.n==n)].iloc[0]
                        of = grid[(grid.universe==uname)&(grid.conv==conv)&(grid.gate=="OFF")&(grid.tilt==t)&(grid.n==n)].iloc[0]
                        cells.append(f"{on.Sharpe-of.Sharpe:+7.3f}/{on.CAGR-of.CAGR:+7.2%}/{on.MaxDD-of.MaxDD:+7.2%}")
                    P(f"    {t:5.2f} " + " ".join(f"{c:>26s}" for c in cells))

    # ---------------- rule 8 walk-forward ---------------------------------
    P(f"\n{'='*132}\nRULE 8 WALK-FORWARD - (t, n) chosen on <= {IS_END} by IS Sharpe inside each "
      f"(universe, gate, convention); {OOS_START}+ read once\n{'='*132}")
    wf = []
    P(f"  {'universe':9s} {'gate':4s} {'conv':4s} {'pick (t,n)':>12s} {'IS_S':>6s} | "
      f"{'OOS CAGR':>9s} {'OOS S':>7s} {'OOS DD':>8s} | {'anchor(0.5,20) OOS S':>21s} | "
      f"{'SPY OOS S':>10s} {'v2 OOS S':>9s} | {'best OOS cell':>14s} {'regret':>7s} {'4b(OOS win)':>12s}")
    for uname in unis:
        spy, v2 = refs[uname]["SPY"], refs[uname]["v2"]
        for gate in GATES:
            for conv in CONVS:
                d = grid[(grid.universe == uname) & (grid.gate == gate) & (grid.conv == conv)]
                pick = d.sort_values(["IS_Sharpe", "tilt", "n"], ascending=[False, True, True]).iloc[0]
                anc = d[(d.tilt == ANCHOR[0]) & (d.n == ANCHOR[1])].iloc[0]
                best = d.sort_values("OOS_Sharpe", ascending=False).iloc[0]
                wf.append(dict(universe=uname, gate=gate, conv=conv, pick_tilt=pick.tilt, pick_n=int(pick.n),
                               pick_IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                               OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               anchor_OOS_Sharpe=anc.OOS_Sharpe, anchor_OOS_CAGR=anc.OOS_CAGR,
                               spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                               v2_OOS_Sharpe=v2["OOS_Sharpe"],
                               best_tilt=best.tilt, best_n=int(best.n), best_OOS_Sharpe=best.OOS_Sharpe,
                               regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                               pick_beats_spy_OOS=bool(pick.OOS_Sharpe > spy["OOS_Sharpe"]),
                               pick_pass4b=bool(pick.pass4b), pick_pass4a=bool(pick.pass4a)))
                P(f"  {uname:9s} {gate:4s} {conv:4s} {f'({pick.tilt:.2f},{int(pick.n)})':>12s} "
                  f"{pick.IS_Sharpe:6.3f} | {pick.OOS_CAGR:9.2%} {pick.OOS_Sharpe:7.3f} "
                  f"{pick.OOS_MaxDD:8.2%} | {anc.OOS_Sharpe:21.3f} | {spy['OOS_Sharpe']:10.3f} "
                  f"{v2['OOS_Sharpe']:9.3f} | {f'({best.tilt:.2f},{int(best.n)})':>14s} "
                  f"{best.OOS_Sharpe-pick.OOS_Sharpe:7.3f} {str(bool(pick.OOS_Sharpe>spy['OOS_Sharpe'])):>12s}")
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)

    P(f"\n  Does the IS chooser ever pick a tilt other than the live 0.50?  "
      f"picks = {sorted(W.pick_tilt.unique().tolist())}, "
      f"counts {W.pick_tilt.value_counts().to_dict()}")
    P(f"  Chooser vs the pre-registered anchor (0.50, 20): mean OOS Sharpe "
      f"{W.OOS_Sharpe.mean():.4f} vs {W.anchor_OOS_Sharpe.mean():.4f} "
      f"(delta {W.OOS_Sharpe.mean()-W.anchor_OOS_Sharpe.mean():+.4f}); chooser wins "
      f"{int((W.OOS_Sharpe>W.anchor_OOS_Sharpe).sum())} of {len(W)} cells")
    P(f"  Mean regret vs the best OOS cell: {W.regret.mean():.4f}")

    # ---------------- KEEP tallies ---------------------------------------
    P(f"\n{'='*132}\nKEEP PATHS over all {len(grid)} cells\n{'='*132}")
    P(f"  4a passes: {int(grid.pass4a.sum())} / {len(grid)}      4b passes: "
      f"{int(grid.pass4b.sum())} / {len(grid)}")
    P("  first failing 4b bar, counts: " + str(grid.first_fail_4b.value_counts().to_dict()))
    for uname in unis:
        for gate in GATES:
            d = grid[(grid.universe == uname) & (grid.gate == gate)]
            P(f"    {uname} gate {gate}: 4a {int(d.pass4a.sum())}/{len(d)}, 4b {int(d.pass4b.sum())}/{len(d)}")
    if grid.pass4b.any():
        P("\n  4b passers:")
        for _, r in grid[grid.pass4b].sort_values("OOS_Sharpe", ascending=False).iterrows():
            P(f"    {r.universe} {r.gate} {r.conv} t={r.tilt:.2f} n={int(r.n)}  CAGR {r.CAGR:.2%} "
              f"Sharpe {r.Sharpe:.3f} MaxDD {r.MaxDD:.2%} H1/H2 {r.H1:.3f}/{r.H2:.3f} "
              f"OOS {r.OOS_CAGR:.2%}/{r.OOS_Sharpe:.3f}/{r.OOS_MaxDD:.2%}")

    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {OUT}.grid.csv, {OUT}.overlap.csv, {OUT}.walkforward.csv, {OUT}.console.txt")


if __name__ == "__main__":
    main()
