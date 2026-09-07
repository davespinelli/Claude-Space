#!/usr/bin/env python3
"""Idea 326: is the 4b DRAWDOWN CAP unreachable on SMALL439 BY CONSTRUCTION?

Idea 34 found the DD bar failing in 24 of 24 cells because the panel's own EWALL book
draws more than SPY.  4b caps MaxDD at 60% of SPY's and floors CAGR at 70% of SPY's.
If the panel's beta is the whole story, then de-grossing (the only unlevered instrument
that moves DD) should close the DD bar and open the CAGR bar, with NO gross level
satisfying both -- i.e. "SMALL439 fails 4b" is a statement about the panel, not a rule.

Two tuned parameters only: n (number of names held) and g (gross).  All 30 grid points
reported.  Rule 8 walk-forward: (n,g) chosen on 2010-2016, read once on 2017-2026.
Costs 10 bps, next-day execution (engine), weekly cadence.

SURVIVORSHIP: the small panel is current constituents of a sub-$2B screen (see
data/SMALL_PANEL_README.md).  Tickers with max_1d_move >= 1.0 in data/small_meta.csv
are dropped first (44 of 483) -> 439 names.
"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights          # noqa
from engine import backtest, metrics                                            # noqa

SLUG = "2026-09-07_is-the-DD-cap-unreachable-on-SMALL439-by-construction_cloud"
OUT = ROOT / "research" / "backtests"
COST, FREQ = 10, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [10, 20, 40, 80, "ALL"]
GS = [0.25, 0.375, 0.50, 0.625, 0.75, 1.00]


# ---------------------------------------------------------------- data
def panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    cols = [c for c in px.columns if c not in bad]
    px = px[cols]
    print(f"panel: {px.shape[1]-1} small names + SPY, {px.index[0].date()} -> {px.index[-1].date()} "
          f"({len(bad)} tickers dropped for max_1d_move >= 1.0)")
    return px


# ---------------------------------------------------------------- books
def mom_weights(px, n, g):
    """Top-n by 12-1 momentum among names priced that day, equal weight at g/n gross.
    n='ALL' -> EWALL: every priced name, g/N.  Cash holds the remainder (de-gross)."""
    live = px.notna() & (px.shift(252).notna())
    if n == "ALL":
        e = live.astype(float)
        return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    mom = (px.shift(21) / px.shift(252) - 1).where(live)
    rank = mom.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return g * sel.div(float(n))


def run(px, wfn):
    res = backtest(px, wfn(px), cost_bps=COST, freq=FREQ)
    start = px.index[260]
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def stats(r):
    m = metrics(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"])


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# ---------------------------------------------------------------- 4b bars
def bars_4b(r, spy):
    """Return (pass, dict of per-bar margins).  4b = Sharpe > SPY in BOTH halves and OOS,
    MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    s = stats(r); h1, h2 = halves(r)
    ss = stats(spy); sh1, sh2 = halves(spy)
    ro, so = r.loc[OOS_START:], spy.loc[OOS_START:]
    oos = metrics(ro)["Sharpe"] - metrics(so)["Sharpe"]
    m = {
        "H1":   h1 - sh1,
        "H2":   h2 - sh2,
        "OOS":  oos,
        "DD":   0.60 * abs(ss["MaxDD"]) - abs(s["MaxDD"]),      # >=0 passes
        "CAGR": s["CAGR"] - 0.70 * ss["CAGR"],                  # >=0 passes
    }
    fails = [k for k, v in m.items() if v < 0]
    return (len(fails) == 0), m, fails


# ---------------------------------------------------------------- census of the record
def census():
    txt = (ROOT / "research" / "LEADERBOARD.md").read_text().split("\n")
    rows = [l for l in txt if l.startswith("|") and re.search(r"small|SMALL|439|483|sub-\$2B", l)]
    dd = [l for l in rows if re.search(r"\bDD\b|drawdown|MaxDD", l)]
    ddfirst = [l for l in rows if re.search(r"fail\w*[^|]{0,40}(DD|drawdown)|(DD|drawdown) cap|first failing bar[^|]{0,20}DD", l, re.I)]
    print(f"\n[A] TEXT CENSUS of LEADERBOARD.md small-panel rows (keyword census, not a re-run)")
    print(f"    rows naming the small panel:            {len(rows)}")
    print(f"    of those, rows mentioning DD/drawdown:  {len(dd)}")
    print(f"    of those, DD named as a FAILING bar:    {len(ddfirst)}")
    return len(rows), len(dd), len(ddfirst)


# ---------------------------------------------------------------- main
def main():
    px = panel()
    spy = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
    ss = stats(spy); sh1, sh2 = halves(spy)
    spy_oos = metrics(spy.loc[OOS_START:])
    print(f"SPY: CAGR {ss['CAGR']:.2%} Sharpe {ss['Sharpe']:.3f} MaxDD {ss['MaxDD']:.2%} "
          f"H1/H2 {sh1:.3f}/{sh2:.3f} | OOS CAGR {spy_oos['CAGR']:.2%} Sharpe {spy_oos['Sharpe']:.3f} "
          f"MaxDD {spy_oos['MaxDD']:.2%}")
    print(f"4b bars on this sample: MaxDD cap {-0.60*abs(ss['MaxDD']):.2%}, CAGR floor {0.70*ss['CAGR']:.2%}")

    # baselines on the same panel
    bl_r, _ = run(px, rules_v2_weights)
    v1_r, _ = run(px, rules_v1_weights)
    bs = stats(bl_r); bh1, bh2 = halves(bl_r)
    print(f"RULES v2 on SMALL439: CAGR {bs['CAGR']:.2%} Sharpe {bs['Sharpe']:.3f} MaxDD {bs['MaxDD']:.2%} "
          f"H1/H2 {bh1:.3f}/{bh2:.3f}")
    vs = stats(v1_r); vh1, vh2 = halves(v1_r)
    print(f"RULES v1 on SMALL439: CAGR {vs['CAGR']:.2%} Sharpe {vs['Sharpe']:.3f} MaxDD {vs['MaxDD']:.2%} "
          f"H1/H2 {vh1:.3f}/{vh2:.3f}")

    census()

    print(f"\n[B] GRID: n x g, {len(NS)}x{len(GS)} = {len(NS)*len(GS)} cells, all reported. "
          f"10 bps, weekly, next-day execution.")
    recs = []
    for n in NS:
        for g in GS:
            r, to = run(px, lambda p, n=n, g=g: mom_weights(p, n, g))
            s = stats(r); h1, h2 = halves(r)
            ok4b, m, fails = bars_4b(r, spy)
            # 4a: Sharpe > RULES v2 in both halves and MaxDD no worse
            ok4a = (h1 > bh1) and (h2 > bh2) and (s["MaxDD"] >= bs["MaxDD"])
            ris, roos = r.loc[:IS_END], r.loc[OOS_START:]
            recs.append(dict(n=str(n), g=g, CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                             H1=h1, H2=h2,
                             IS_Sharpe=metrics(ris)["Sharpe"], OOS_Sharpe=metrics(roos)["Sharpe"],
                             OOS_CAGR=metrics(roos)["CAGR"], OOS_MaxDD=metrics(roos)["MaxDD"],
                             m_H1=m["H1"], m_H2=m["H2"], m_OOS=m["OOS"], m_DD=m["DD"], m_CAGR=m["CAGR"],
                             fails="+".join(fails) or "none", pass4b=ok4b, pass4a=ok4a,
                             turnover=to.sum() / metrics(r)["Years"]))
            print(f"  n={str(n):>3} g={g:.3f} | CAGR {s['CAGR']:6.2%} Sh {s['Sharpe']:.3f} "
                  f"DD {s['MaxDD']:7.2%} H1/H2 {h1:.3f}/{h2:.3f} | margins DD {m['DD']:+.4f} "
                  f"CAGR {m['CAGR']:+.4f} H1 {m['H1']:+.3f} H2 {m['H2']:+.3f} OOS {m['OOS']:+.3f} "
                  f"| 4b {'PASS' if ok4b else 'fail:'+('+'.join(fails))} 4a {'PASS' if ok4a else 'fail'}")
    df = pd.DataFrame(recs)
    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    # ------------------------------------------------------------ the construction question
    print("\n[C] IS THE DD BAR THE BINDING FAILURE?")
    nfail = (~df.pass4b).sum()
    ddbind = df.loc[~df.pass4b, "fails"].str.contains("DD").sum()
    cagrbind = df.loc[~df.pass4b, "fails"].str.contains("CAGR").sum()
    print(f"    4b passes: {df.pass4b.sum()}/{len(df)};  4a passes: {df.pass4a.sum()}/{len(df)}")
    print(f"    of {nfail} failures, DD is a failing bar in {ddbind}, CAGR in {cagrbind}")
    print(f"    failure-mode tally:\n{df.loc[~df.pass4b,'fails'].value_counts().to_string()}")

    print("\n[D] DOES DE-GROSSING EVER OPEN BOTH BARS AT ONCE? (per n, over the g ladder)")
    for n in NS:
        sub = df[df.n == str(n)].sort_values("g")
        gd = sub.loc[sub.m_DD >= 0, "g"]
        gc = sub.loc[sub.m_CAGR >= 0, "g"]
        both = sub.loc[(sub.m_DD >= 0) & (sub.m_CAGR >= 0), "g"]
        print(f"    n={str(n):>3}: DD cap met at g <= {gd.max() if len(gd) else 'NONE':<6} | "
              f"CAGR floor met at g >= {gc.min() if len(gc) else 'NONE':<6} | "
              f"BOTH at g in {sorted(both.round(3).tolist()) if len(both) else 'EMPTY'}")

    # linear-in-g check: DD and CAGR are near-affine in gross, so interpolate the crossings
    print("\n[E] INTERPOLATED ADMISSIBLE GROSS BAND (linear in g between grid points)")
    for n in NS:
        sub = df[df.n == str(n)].sort_values("g")
        def cross(col, want_ge):
            x, y = sub.g.values, sub[col].values
            for i in range(len(x) - 1):
                if (y[i] >= 0) != (y[i + 1] >= 0):
                    t = -y[i] / (y[i + 1] - y[i])
                    return x[i] + t * (x[i + 1] - x[i])
            return None
        gdd, gcg = cross("m_DD", True), cross("m_CAGR", True)
        print(f"    n={str(n):>3}: DD cap binds above g~{gdd if gdd is None else round(gdd,3)}, "
              f"CAGR floor binds below g~{gcg if gcg is None else round(gcg,3)} -> "
              f"band {'EMPTY (bars mutually exclusive)' if (gdd is not None and gcg is not None and gcg > gdd) else 'non-empty / undetermined'}")

    # ------------------------------------------------------------ rule 8
    print("\n[F] RULE 8 WALK-FORWARD: (n,g) chosen on 2010-2016 by IS Sharpe, read once on 2017-2026")
    pick = df.loc[df.IS_Sharpe.idxmax()]
    anchor = df[(df.n == "20") & (df.g == 0.75)].iloc[0]   # the record's KEEP-4b book form
    ew = df[(df.n == "ALL") & (df.g == 1.00)].iloc[0]
    bl_oos, bl_is = metrics(bl_r.loc[OOS_START:]), metrics(bl_r.loc[:IS_END])
    print(f"    IS-chooser picks n={pick.n} g={pick.g} (IS Sharpe {pick.IS_Sharpe:.3f})")
    for lbl, row in [("chooser", pick), ("anchor n=20 g=0.75", anchor), ("EWALL g=1.00", ew)]:
        print(f"      {lbl:<20} OOS CAGR {row.OOS_CAGR:6.2%} Sharpe {row.OOS_Sharpe:.3f} MaxDD {row.OOS_MaxDD:7.2%}")
    print(f"      {'RULES v2 baseline':<20} OOS CAGR {bl_oos['CAGR']:6.2%} Sharpe {bl_oos['Sharpe']:.3f} MaxDD {bl_oos['MaxDD']:7.2%}")
    print(f"      {'SPY':<20} OOS CAGR {spy_oos['CAGR']:6.2%} Sharpe {spy_oos['Sharpe']:.3f} MaxDD {spy_oos['MaxDD']:7.2%}")
    best_oos = df.loc[df.OOS_Sharpe.idxmax()]
    print(f"    regret vs OOS-best (n={best_oos.n} g={best_oos.g}, {best_oos.OOS_Sharpe:.3f}): "
          f"{best_oos.OOS_Sharpe - pick.OOS_Sharpe:.4f}")

    # ------------------------------------------------------------ OOS 4b bars, re-cut
    print("\n[G] OOS-ONLY 4b BARS (2017-2026 read once): does the DD cap bind there too?")
    so = spy.loc[OOS_START:]
    cap, floor = 0.60 * abs(metrics(so)["MaxDD"]), 0.70 * metrics(so)["CAGR"]
    print(f"    OOS SPY MaxDD {metrics(so)['MaxDD']:.2%} -> cap {-cap:.2%}; CAGR {metrics(so)['CAGR']:.2%} -> floor {floor:.2%}")
    oosdd = ((df.OOS_MaxDD.abs() > cap)).sum(); ooscg = ((df.OOS_CAGR < floor)).sum()
    print(f"    cells breaching the OOS DD cap: {oosdd}/{len(df)}; below the OOS CAGR floor: {ooscg}/{len(df)}")

    # ------------------------------------------------------------ the closed form
    print("\n[H] WHY THE BAND IS EMPTY: 4b's two level bars are a GROSS-INVARIANT CALMAR BAR")
    print("    An unlevered book at gross g is a cash blend: CAGR and MaxDD both scale ~linearly in g,")
    print("    so CAGR/|MaxDD| (Calmar) is ~invariant to g.  The DD cap needs |DD| <= 0.60*|DD_SPY| and")
    print("    the CAGR floor needs CAGR >= 0.70*CAGR_SPY; both can hold at some g only if")
    print("      Calmar_book >= (0.70/0.60) * Calmar_SPY = 1.1667 * Calmar_SPY.")
    spy_cal = ss["CAGR"] / abs(ss["MaxDD"])
    bar = (0.70 / 0.60) * spy_cal
    print(f"    Calmar_SPY = {ss['CAGR']:.4f}/{abs(ss['MaxDD']):.4f} = {spy_cal:.4f}  ->  bar = {bar:.4f}")
    df["Calmar"] = df.CAGR / df.MaxDD.abs()
    for n in NS:
        sub = df[df.n == str(n)].sort_values("g")
        print(f"    n={str(n):>3}: Calmar over the g ladder "
              f"{[round(v,4) for v in sub.Calmar]}  (spread {sub.Calmar.max()-sub.Calmar.min():.4f}) "
              f"| max {sub.Calmar.max():.4f} vs bar {bar:.4f} -> {'CLEARS' if sub.Calmar.max()>=bar else 'SHORT'}")
    print(f"    cells clearing the Calmar bar: {(df.Calmar >= bar).sum()}/{len(df)}; "
          f"best cell Calmar {df.Calmar.max():.4f} (n={df.loc[df.Calmar.idxmax(),'n']} g={df.loc[df.Calmar.idxmax(),'g']}), "
          f"short of the bar by {bar - df.Calmar.max():.4f}")
    print("    Sharpe is likewise gross-invariant at rf=0, so the H1/H2/OOS bars cannot be de-grossed into either.")
    print(f"    Sharpe-vs-SPY bars fail in {(df[['m_H1','m_H2','m_OOS']] < 0).any(axis=1).sum()}/{len(df)} cells "
          f"(H1 {(df.m_H1<0).sum()}, H2 {(df.m_H2<0).sum()}, OOS {(df.m_OOS<0).sum()}).")

    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    print(f"\nwrote {SLUG}.grid.csv")


if __name__ == "__main__":
    main()
