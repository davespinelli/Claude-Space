#!/usr/bin/env python3
"""Idea 953 (lane cloud, 2026-09-22): is an IS-CHOSEN FREE PARAMETER worth LESS THAN ITS
DEFAULT on every dial?

Idea 944 found that SHIPPING the canonical month-end beats CHOOSING the rebalance phase on
2009-2016 by +0.0232 of OOS Sharpe, and that where the IS chooser deviates from the default it
wins out of sample only 45 of 132 times (34.1%) — on that one dial the free parameter is worth
less than nothing.  944 tested ONE dial (rebalance phase).  This run asks whether the result is
a phase fact or a general one, by running the SAME contrast on the five other free parameters
the record actually ships:

  DIAL      FAMILY     RUNGS                                     SHIPPED DEFAULT
  N         RULES v1   3, 5, 8, 10, 15, 20  (w = 0.75/n, so      n = 5   (v1's own)
                       gross is held at 0.75 and only n moves)
  MAXVOL    RULES v1   0.30 .. 1.00, 6 rungs                     max_vol = 0.60
  GROSS     RULES v2   0.25 .. 1.50, 6 rungs                     gross = 0.75
  BAND      RULES v2   0.00 .. 0.08, 6 rungs                     band = 0.03
  CADENCE   RULES v2   D, W, M, Q                                W (v2 is live weekly)

TWO TUNED PARAMETERS (the queue's own: "parameter set, chooser"), every level reported:
  TUNED 1  THE DIAL, 5 levels above.  Each dial is walked in ITS OWN family, so the default is
           always the value the live book actually ships and the contrast is the real one an
           author faces: ship the default, or spend the half-sample choosing.
  TUNED 2  THE CHOOSER, 3 levels, all computed on 2009..first-half only: IS_SHARPE (argmax IS
           Sharpe, 944's own), IS_CALMAR (argmax IS CAGR / |IS MaxDD|), IS_CAGR (argmax IS
           CAGR).  DEFAULT is not a chooser — it is the comparand.

REPORTED CONSTANTS (not tuned): t+1 execution, 10 bps headline cost with 25 and 50 reported
beside it, 260-row warm-up, weekly cadence except on the CADENCE dial, equal/flat weights as
each family ships them.  PROTOCOL rule 8 is the whole design: the chooser sees the FIRST HALF
only, the SECOND HALF is read once, untouched.

PANELS: U56, B136, SMALL (719 cached sub-$2B names less the 54 with max_1d_move >= 1.0 in
data/small_meta.csv, leaving 665 investable; SPY joined as BENCHMARK ONLY, never held).

SURVIVORSHIP, STATED: all three panels are CURRENT-CONSTITUENT lists (U56/B136 the 2026
universe files held from 2008, SMALL the current sub-$2B screen held from 2010), so every level
is an upper bound.  The contrast reported here is a DIFFERENCE between two books on the same
panel, which cancels most of that bias; the absolute 4a/4b verdicts do not, and are read
against SPY, which is traded and unbiased.

BOTH KEEP PATHS (4a vs the live RULES v2 book, 4b vs SPY) are evaluated at EVERY rung, and the
chooser-vs-default contrast is reported per cell and pooled.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
WARMUP, GROSS0, BAND0, N0, MAXVOL0, FREQ0 = 260, 0.75, 0.03, 5, 0.60, "W"
COSTS = [10.0, 25.0, 50.0]
CHOOSERS = ["IS_SHARPE", "IS_CALMAR", "IS_CAGR"]

DIALS = {
    "N":       dict(family="v1", rungs=[3, 5, 8, 10, 15, 20],                  default=N0),
    "MAXVOL":  dict(family="v1", rungs=[0.30, 0.40, 0.50, 0.60, 0.80, 1.00],   default=MAXVOL0),
    "GROSS":   dict(family="v2", rungs=[0.25, 0.50, 0.75, 1.00, 1.25, 1.50],   default=GROSS0),
    "BAND":    dict(family="v2", rungs=[0.00, 0.01, 0.02, 0.03, 0.05, 0.08],   default=BAND0),
    "CADENCE": dict(family="v2", rungs=["D", "W", "M", "Q"],                   default=FREQ0),
}


# ---------------------------------------------------------------- panels
def panels():
    u, b, s = load_universe(), load_universe(broad=True), load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in s.columns if c != "SPY" and c not in bad]
    print(f"SMALL: {s.shape[1]-1} cached names, dropped {len(bad & set(s.columns))} with "
          f"max_1d_move >= 1.0, {len(keep)} investable (+SPY as benchmark only)")
    return {"U56": (u, list(u.columns)), "B136": (b, list(b.columns)), "SMALL": (s, keep)}


# ---------------------------------------------------------------- books
def v1_weights(px, cols, n=N0, max_vol=MAXVOL0, gross=GROSS0):
    """RULES v1's screen on a column subset, with w = gross/n so the GROSS is held fixed and
    only n moves.  n = 5, max_vol = 0.60, gross = 0.75 reproduces baseline.rules_v1_weights."""
    sub = px[cols]
    s, above, vol20 = score(sub, vol_scale=True)
    elig = s.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float) * (gross / n)
    return w.reindex(columns=px.columns).fillna(0.0)


def v2_weights(px, cols, band=BAND0, gross=GROSS0):
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    ew = ew.where(band_state(sub, band), 0.0)
    return ew.reindex(columns=px.columns).fillna(0.0)


def book(px, cols, dial, rung):
    """(weights, freq) for one rung of one dial; every other dial sits at its shipped default."""
    if dial == "N":       return v1_weights(px, cols, n=rung), FREQ0
    if dial == "MAXVOL":  return v1_weights(px, cols, max_vol=rung), FREQ0
    if dial == "GROSS":   return v2_weights(px, cols, gross=rung), FREQ0
    if dial == "BAND":    return v2_weights(px, cols, band=rung), FREQ0
    if dial == "CADENCE": return v2_weights(px, cols), rung
    raise ValueError(dial)


def run(px, w, freq, start):
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    g, to = res["returns"].loc[start:], res["turnover"].loc[start:]
    return {c: g - to * c / 1e4 for c in COSTS}, to.sum() / (len(to) / 252)


# ---------------------------------------------------------------- scoring
def keep_paths(r, spy, base, is_idx, oos_idx):
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    s, s1, s2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    b, b1, b2 = metrics(base), metrics(base.iloc[:h]), metrics(base.iloc[h:])
    mi, mo = metrics(r.loc[is_idx]), metrics(r.loc[oos_idx])
    so, bo = metrics(spy.loc[oos_idx]), metrics(base.loc[oos_idx])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
             IS_Calmar=mi["CAGR"] / abs(mi["MaxDD"]) if mi["MaxDD"] else np.nan,
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
             SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"], SPY_OOS_MaxDD=so["MaxDD"],
             BASE_OOS_CAGR=bo["CAGR"], BASE_OOS_Sharpe=bo["Sharpe"], BASE_OOS_MaxDD=bo["MaxDD"])
    d["p4a"] = bool(m1["Sharpe"] > b1["Sharpe"] and m2["Sharpe"] > b2["Sharpe"] and m["MaxDD"] >= b["MaxDD"])
    L = {"H1": m1["Sharpe"] > s1["Sharpe"], "H2": m2["Sharpe"] > s2["Sharpe"],
         "OOS": mo["Sharpe"] > so["Sharpe"], "DD": m["MaxDD"] >= 0.60 * s["MaxDD"],
         "CAGR": m["CAGR"] >= 0.70 * s["CAGR"]}
    d["p4b"] = bool(all(L.values()))
    d["bind"] = ",".join(k for k, v in L.items() if not v) or "-"
    d["p4b_oos"] = bool(mo["Sharpe"] > so["Sharpe"] and mo["MaxDD"] >= 0.60 * so["MaxDD"]
                        and mo["CAGR"] >= 0.70 * so["CAGR"])
    d["p4a_oos"] = bool(mo["Sharpe"] > bo["Sharpe"] and mo["MaxDD"] >= bo["MaxDD"])
    return d


def main():
    P = panels()
    rows = []
    for pname, (px, cols) in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        h = len(spy) // 2
        is_idx, oos_idx = spy.index[:h], spy.index[h:]
        base_c, _ = run(px, rules_v2_weights(px), FREQ0, start)
        print(f"\n=== {pname}  n={len(cols)}  IS {is_idx[0].date()}..{is_idx[-1].date()}  "
              f"OOS {oos_idx[0].date()}..{oos_idx[-1].date()}")
        for dial, spec in DIALS.items():
            for rung in spec["rungs"]:
                w, freq = book(px, cols, dial, rung)
                rc, turn = run(px, w, freq, start)
                for c in COSTS:
                    d = keep_paths(rc[c], spy, base_c[c], is_idx, oos_idx)
                    d.update(panel=pname, dial=dial, rung=str(rung), cost=c, turnover=turn,
                             is_default=(rung == spec["default"]))
                    rows.append(d)
                d10 = rows[-len(COSTS)]
                print(f"  {dial:8s} {str(rung):>5s}{' *DEFAULT*' if rung == spec['default'] else '          '} "
                      f"turn={turn:5.2f}x | IS Sh {d10['IS_Sharpe']:.4f} Cal {d10['IS_Calmar']:.3f} "
                      f"CAGR {d10['IS_CAGR']:6.2%} | OOS {d10['OOS_CAGR']:7.2%}/{d10['OOS_Sharpe']:.4f}/"
                      f"{d10['OOS_MaxDD']:7.2%} | 4a={int(d10['p4a'])} 4b={int(d10['p4b'])}({d10['bind']}) "
                      f"4bOOS={int(d10['p4b_oos'])}")
    df = pd.DataFrame(rows)
    df.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n{len(df)} grid points -> {OUT.name}.grid.csv")

    # ------------- the contrast: IS chooser vs SHIPPED default, read out of sample
    key = {"IS_SHARPE": "IS_Sharpe", "IS_CALMAR": "IS_Calmar", "IS_CAGR": "IS_CAGR"}
    cells = []
    for (pname, dial, c), g in df.groupby(["panel", "dial", "cost"]):
        dflt = g[g.is_default].iloc[0]
        for ch in CHOOSERS:
            pick = g.loc[g[key[ch]].idxmax()]
            cells.append(dict(panel=pname, dial=dial, cost=c, chooser=ch,
                              pick=pick.rung, default=dflt.rung, deviates=bool(pick.rung != dflt.rung),
                              dOOS_Sharpe=pick.OOS_Sharpe - dflt.OOS_Sharpe,
                              dOOS_CAGR=pick.OOS_CAGR - dflt.OOS_CAGR,
                              dOOS_MaxDD=pick.OOS_MaxDD - dflt.OOS_MaxDD,
                              dFull_Sharpe=pick.Sharpe - dflt.Sharpe,
                              pick_4b=int(pick.p4b), dflt_4b=int(dflt.p4b),
                              pick_4b_oos=int(pick.p4b_oos), dflt_4b_oos=int(dflt.p4b_oos),
                              pick_4a=int(pick.p4a), dflt_4a=int(dflt.p4a),
                              pick_OOS_Sharpe=pick.OOS_Sharpe, dflt_OOS_Sharpe=dflt.OOS_Sharpe,
                              pick_OOS_CAGR=pick.OOS_CAGR, dflt_OOS_CAGR=dflt.OOS_CAGR,
                              pick_OOS_MaxDD=pick.OOS_MaxDD, dflt_OOS_MaxDD=dflt.OOS_MaxDD,
                              SPY_OOS_Sharpe=dflt.SPY_OOS_Sharpe, SPY_OOS_CAGR=dflt.SPY_OOS_CAGR,
                              SPY_OOS_MaxDD=dflt.SPY_OOS_MaxDD,
                              BASE_OOS_Sharpe=dflt.BASE_OOS_Sharpe, BASE_OOS_CAGR=dflt.BASE_OOS_CAGR,
                              BASE_OOS_MaxDD=dflt.BASE_OOS_MaxDD))
    cd = pd.DataFrame(cells)
    cd.to_csv(OUT.with_suffix(".chooser.csv"), index=False)

    print("\n=== IS CHOOSER vs SHIPPED DEFAULT, read out of sample (rule 8), every cell ===")
    for _, r in cd[cd.cost == 10.0].iterrows():
        print(f"  {r.panel:6s} {r.dial:8s} {r.chooser:9s} pick={r['pick']:>5s} default={r['default']:>5s} "
              f"{'DEV' if r.deviates else '   '} | dOOS_Sharpe {r.dOOS_Sharpe:+.4f} "
              f"dOOS_CAGR {r.dOOS_CAGR:+7.2%} dOOS_MaxDD {r.dOOS_MaxDD:+7.2%} | "
              f"4bOOS pick/def {r.pick_4b_oos}/{r.dflt_4b_oos}")

    print("\n=== POOLED (944's own statistics, restated on five dials) ===")
    for lbl, sub in [("ALL CELLS", cd)] + [(f"cost {c:.0f} bps", cd[cd.cost == c]) for c in COSTS]:
        dev = sub[sub.deviates]
        print(f"  {lbl:14s} n={len(sub):3d}  deviates {len(dev):3d} ({len(dev)/len(sub):.1%})  "
              f"mean dOOS_Sharpe {sub.dOOS_Sharpe.mean():+.4f}  median {sub.dOOS_Sharpe.median():+.4f}  "
              f"chooser wins OOS {int((sub.dOOS_Sharpe > 0).sum())} of {len(sub)} "
              f"({(sub.dOOS_Sharpe > 0).mean():.1%})" +
              (f"  | conditional on deviating: wins {int((dev.dOOS_Sharpe > 0).sum())} of {len(dev)} "
               f"({(dev.dOOS_Sharpe > 0).mean():.1%}), mean {dev.dOOS_Sharpe.mean():+.4f}" if len(dev) else ""))

    print("\n  BY DIAL (all costs, all choosers):")
    for dial, g in cd.groupby("dial"):
        dev = g[g.deviates]
        print(f"    {dial:8s} n={len(g):2d} deviates {len(dev):2d}  mean dOOS_Sharpe {g.dOOS_Sharpe.mean():+.4f}  "
              f"wins {int((g.dOOS_Sharpe > 0).sum())}/{len(g)}  mean dOOS_CAGR {g.dOOS_CAGR.mean():+.2%}  "
              f"mean dOOS_MaxDD {g.dOOS_MaxDD.mean():+.2%}  4bOOS pick/def {int(g.pick_4b_oos.sum())}/{int(g.dflt_4b_oos.sum())}")
    print("\n  BY CHOOSER (all costs, all dials):")
    for ch, g in cd.groupby("chooser"):
        dev = g[g.deviates]
        print(f"    {ch:9s} n={len(g):2d} deviates {len(dev):2d}  mean dOOS_Sharpe {g.dOOS_Sharpe.mean():+.4f}  "
              f"wins {int((g.dOOS_Sharpe > 0).sum())}/{len(g)}  4bOOS pick/def {int(g.pick_4b_oos.sum())}/{int(g.dflt_4b_oos.sum())}")
    print("\n  BY PANEL (all costs, all dials, all choosers):")
    for pn, g in cd.groupby("panel"):
        print(f"    {pn:6s} n={len(g):2d} deviates {int(g.deviates.sum()):2d}  mean dOOS_Sharpe {g.dOOS_Sharpe.mean():+.4f}  "
              f"wins {int((g.dOOS_Sharpe > 0).sum())}/{len(g)}")

    print("\n=== KEEP-PATH CENSUS over all rungs ===")
    for c in COSTS:
        s = df[df.cost == c]
        print(f"  {c:4.0f} bps: 4a {int(s.p4a.sum())} of {len(s)}   4b(full) {int(s.p4b.sum())} of {len(s)}   "
              f"4b(OOS) {int(s.p4b_oos.sum())} of {len(s)}   4a(OOS) {int(s.p4a_oos.sum())} of {len(s)}")
    f = df[(df.cost == 10.0) & (~df.p4b)]
    print("  4b binding legs at 10 bps:",
          {k: int(sum(k in b.split(",") for b in f.bind)) for k in ("H1", "H2", "OOS", "DD", "CAGR")})
    p = df[(df.cost == 10.0) & df.p4b]
    if len(p):
        print("\n  4b passers at 10 bps:")
        print(p[["panel", "dial", "rung", "is_default", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                 "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4b_oos", "p4a"]].to_string(index=False,
                 float_format=lambda x: f"{x:.4f}"))


if __name__ == "__main__":
    main()
