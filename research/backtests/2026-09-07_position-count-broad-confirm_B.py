#!/usr/bin/env python3
"""Idea 44: position-count BROAD CONFIRM — does idea 2's 4b KEEP survive a universe change?

Idea 2's KEEP is `top-20 eligible by the v1 composite, /sqrt(vol20) scaler OFF, equal weight at
75% gross, RULES v1 eligibility (above 200d MA, vol20 < 0.60), weekly, next-day execution, 10 bps`.
It clears 4b on U56 (research/universe.json) and, as published, misses 4b's H2 Sharpe bar on
B136 (research/universe_broad.json) by 0.02.  This script runs the FULL n sweep with B136 as the
PRIMARY universe and reports where 4b clears at all, and whether the KEEP is a universe artefact.

Two tuned parameters, no more:
    1. n     in {5, 10, 20, 30, 40, 60, 80, ALL}   position count (ALL = every eligible name)
    2. gross in {0.50, 0.75, 1.00}                 constant gross target
The pre-registered anchor is idea 2's own cell, n=20 / gross=0.75.

Panel (B136 primary, U56 reference), cost rung (10 = PROTOCOL's anchor, 25 = idea 323's rung) and
weighting CONVENTION are reported axes, not tuned choices; every point of every axis is printed.

Two weighting conventions are run because idea 244 showed a fixed `gross/n` weight silently
de-grosses a wide book:
    NORM  w_i = g / k_t      k_t = names actually selected that day -> realised gross is g at every n
    FIXED w_i = g / n        idea 2's published form -> realised gross falls as n outruns eligibility
The grid is NORM (so the n dial is a pure WIDTH dial and gross is a pure GROSS dial, orthogonal);
FIXED is run at g=0.75 across all n as a reproduction column for idea 2's published book.

Rule 8 walk-forward: (n, gross) chosen on 2008-2016 by IS Sharpe, 2017-2026 read once, against the
n=20/g=0.75 anchor, the OOS-best cell (regret), RULES v2 and SPY.

Idea 326 derived that for an unlevered cash-blend book Sharpe is gross-invariant while CAGR and
|MaxDD| both scale ~linearly in g, so 4b's DD cap + CAGR floor collapse to a gross-invariant Calmar
bar of (0.70/0.60) x Calmar_SPY = 1.1667 x Calmar_SPY.  That prediction is tested here on B136/U56
directly (section [G]): if the binding bar is a Sharpe bar, no gross level can rescue the cell.

CAVEATS: (1) both universes are current-constituent lists (survivorship), which flatters every
momentum book -- the CAGR levels are optimistic, the n-DIFFERENCES much less so.  (2) data/prices*.csv
are still on a calendar-day index (queue idea 38, unfixed): equities are ffilled across weekends, so
vol20 and the weekly rebalance mask are computed on a 7-day week.  This affects all three panels
identically and is a level effect, not an n effect.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest, metrics                                            # noqa

SLUG = "2026-09-07_position-count-broad-confirm_B"
OUT = ROOT / "research" / "backtests"
MAX_VOL, FREQ = 0.60, "W"
NS = [5, 10, 20, 30, 40, 60, 80, "ALL"]
GROSSES = [0.50, 0.75, 1.00]
COSTS = [10, 25]
ANCHOR_N, ANCHOR_G = 20, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"


# ---------------------------------------------------------------- the book
def selected(px, n):
    """Boolean frame: top-n eligible names by the v1 composite with the vol scaler OFF."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    e = s.where(elig)
    if n == "ALL":
        return elig & e.notna()
    return e.rank(axis=1, ascending=False) <= n


def weights(px, n, g, conv):
    sel = selected(px, n).astype(float)
    if conv == "NORM":                       # constant realised gross g at every n
        k = sel.sum(axis=1).replace(0, np.nan)
        return g * sel.div(k, axis=0).fillna(0.0)
    nn = sel.shape[1] if n == "ALL" else n   # idea 2's published form
    return sel * (g / nn)


def run(px, n, g, conv, cost):
    res = backtest(px, weights(px, n, g, conv), cost_bps=cost, freq=FREQ)
    start = px.index[260]
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].loc[start:].sum(axis=1), res["weights"].loc[start:].gt(0).sum(axis=1))


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def main():
    panels = {"B136": load_universe(broad=True), "U56": load_universe()}   # B136 PRIMARY
    recs, ctx = [], {}

    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        ctx[pname] = dict(spy=spy, ms=ms, s1=s1, s2=s2, so=so)
        _, above, vol20 = score(px)
        nel = (above & (vol20 < MAX_VOL) & px.notna()).sum(axis=1).loc[start:]
        print(f"\n=== {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()} -> {px.index[-1].date()}"
              f"  (eligible/day mean {nel.mean():.1f}, min {nel.min()}, max {nel.max()})")
        print(f"    SPY CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} Calmar {ms['Calmar']:.4f} | OOS CAGR {so['CAGR']:.2%} "
              f"Sharpe {so['Sharpe']:.3f} MaxDD {so['MaxDD']:.2%}")
        print(f"    4b bars: H1 > {s1:.3f}, H2 > {s2:.3f}, OOS > {so['Sharpe']:.3f}, "
              f"MaxDD >= {-0.60*abs(ms['MaxDD']):.2%}, CAGR >= {0.70*ms['CAGR']:.2%} "
              f"| idea 326 Calmar bar {1.1667*ms['Calmar']:.4f}")

        for cost in COSTS:
            b2, _, _, _ = run_base(px, rules_v2_weights, cost)
            b1, _, _, _ = run_base(px, rules_v1_weights, cost)
            mb, bh1, bh2 = metrics(b2), *hs(b2)
            ctx[(pname, cost)] = dict(b2=b2, mb=mb, bh1=bh1, bh2=bh2)
            print(f"\n  -- {cost} bps | RULES v2 (live) {mb['CAGR']:6.2%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:7.2%} "
                  f"({bh1:.3f}/{bh2:.3f})   RULES v1 {metrics(b1)['CAGR']:6.2%}/"
                  f"{metrics(b1)['Sharpe']:.3f}/{metrics(b1)['MaxDD']:7.2%}")
            for conv in ("NORM", "FIXED"):
                gs = GROSSES if conv == "NORM" else [ANCHOR_G]
                for g in gs:
                    for n in NS:
                        r, to, gross, cnt = run(px, n, g, conv, cost)
                        m = metrics(r); h1, h2 = hs(r)
                        ok4b, d, f = bars(r, spy)
                        ok4a = (h1 > bh1) and (h2 > bh2) and (m["MaxDD"] >= mb["MaxDD"])
                        mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
                        recs.append(dict(panel=pname, cost=cost, conv=conv, gross=g, n=str(n),
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         Calmar=m["Calmar"], H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"],
                                         OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                         m_H1=d["H1"], m_H2=d["H2"], m_OOS=d["OOS"], m_DD=d["DD"],
                                         m_CAGR=d["CAGR"], fails="+".join(f) or "none",
                                         pass4b=ok4b, pass4a=ok4a, turnover=to.sum() / m["Years"],
                                         real_gross=gross.mean(), names=cnt.mean()))
                        tag = "  <-- idea 2's KEEP cell" if (conv == "FIXED" and n == ANCHOR_N) else ""
                        print(f"     {conv:>5} g={g:.2f} n={str(n):>3} | CAGR {m['CAGR']:6.2%} Sh {m['Sharpe']:.3f} "
                              f"DD {m['MaxDD']:7.2%} H1/H2 {h1:.3f}/{h2:.3f} turn {to.sum()/m['Years']:5.2f}x "
                              f"g_real {gross.mean():.3f} names {cnt.mean():5.1f} | DD {d['DD']:+.4f} "
                              f"CAGR {d['CAGR']:+.4f} H1 {d['H1']:+.3f} H2 {d['H2']:+.3f} OOS {d['OOS']:+.3f} | "
                              f"4b {'PASS' if ok4b else 'fail:'+'+'.join(f)} 4a {'PASS' if ok4a else 'fail'}{tag}")

    df = pd.DataFrame(recs)
    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    # ---------------------------------------------------------------- [A] where 4b clears
    print(f"\n[A] 4b / 4a PASS COUNTS over all {len(df)} cells")
    print(df.groupby(["panel", "cost", "conv"])[["pass4b", "pass4a"]].sum().to_string())
    print(f"    total 4b {df.pass4b.sum()}/{len(df)}, 4a {df.pass4a.sum()}/{len(df)}")
    print("    4b failure-mode tally:")
    print(df.loc[~df.pass4b, "fails"].value_counts().to_string())
    print("    bar-by-bar: how often each 4b bar is NEGATIVE")
    for bar in ["m_H1", "m_H2", "m_OOS", "m_DD", "m_CAGR"]:
        print(f"      {bar:>6}: {(df[bar] < 0).sum():>3}/{len(df)}")

    # ---------------------------------------------------------------- [B] the anchor cell
    print("\n[B] IDEA 2's PUBLISHED CELL (FIXED, n=20, g=0.75) ON EACH PANEL AND RUNG")
    a = df[(df.conv == "FIXED") & (df.n == "20")].sort_values(["panel", "cost"])
    for _, r in a.iterrows():
        print(f"    {r.panel:>4} {r.cost:>2} bps | CAGR {r.CAGR:6.2%} Sh {r.Sharpe:.3f} DD {r.MaxDD:7.2%} "
              f"H1/H2 {r.H1:.3f}/{r.H2:.3f} g_real {r.real_gross:.3f} | margins H1 {r.m_H1:+.4f} "
              f"H2 {r.m_H2:+.4f} OOS {r.m_OOS:+.4f} DD {r.m_DD:+.4f} CAGR {r.m_CAGR:+.4f} "
              f"| 4b {'PASS' if r.pass4b else 'fail:'+r.fails}")

    # ---------------------------------------------------------------- [C] the n curve
    print("\n[C] THE n CURVE (NORM, g=0.75), the pure width dial")
    for p in panels:
        for cost in COSTS:
            s = df[(df.panel == p) & (df.cost == cost) & (df.conv == "NORM") & (df.gross == ANCHOR_G)]
            s = s.set_index("n").reindex([str(x) for x in NS])
            print(f"    {p} @{cost}bps  " + "  ".join(f"n={i}:{r.Sharpe:.3f}" for i, r in s.iterrows()))
            print(f"    {'':>{len(p)+len(str(cost))+5}}" + "  ".join(
                f"n={i}:{r.m_H2:+.3f}" for i, r in s.iterrows()) + "   (H2 margin vs SPY)")

    # ---------------------------------------------------------------- [D] NORM vs FIXED
    print("\n[D] CONVENTION CHECK: is the published n dial a GROSS dial? (g=0.75, per panel/rung)")
    for p in panels:
        for cost in COSTS:
            for n in NS:
                f_ = df[(df.panel == p) & (df.cost == cost) & (df.conv == "FIXED") & (df.n == str(n))].iloc[0]
                nm = df[(df.panel == p) & (df.cost == cost) & (df.conv == "NORM")
                        & (df.gross == ANCHOR_G) & (df.n == str(n))].iloc[0]
                print(f"    {p:>4} {cost:>2}bps n={str(n):>3} | FIXED g_real {f_.real_gross:.3f} "
                      f"Sh {f_.Sharpe:.3f} CAGR {f_.CAGR:6.2%} | NORM g_real {nm.real_gross:.3f} "
                      f"Sh {nm.Sharpe:.3f} CAGR {nm.CAGR:6.2%} | dSharpe {nm.Sharpe-f_.Sharpe:+.4f} "
                      f"dCAGR {nm.CAGR-f_.CAGR:+.4f}")

    # ---------------------------------------------------------------- [E] the gross dial
    print("\n[E] THE GROSS DIAL (NORM): Sharpe span across g at fixed n — idea 326's invariance claim")
    for p in panels:
        for cost in COSTS:
            s = df[(df.panel == p) & (df.cost == cost) & (df.conv == "NORM")]
            for n in NS:
                t = s[s.n == str(n)].sort_values("gross")
                print(f"    {p:>4} {cost:>2}bps n={str(n):>3} | Sharpe " +
                      " ".join(f"g{g:.2f}:{v:.3f}" for g, v in zip(t.gross, t.Sharpe)) +
                      f" span {t.Sharpe.max()-t.Sharpe.min():.4f} | Calmar " +
                      " ".join(f"{v:.3f}" for v in t.Calmar) +
                      f" span {t.Calmar.max()-t.Calmar.min():.4f}")

    # ---------------------------------------------------------------- [F] joint surface
    print("\n[F] 4b VERDICT SURFACE (NORM): rows = panel/cost/gross, cols = n")
    piv = (df[df.conv == "NORM"].assign(v=np.where(df[df.conv == "NORM"].pass4b, "PASS",
                                                   df[df.conv == "NORM"].fails))
           .pivot_table(index=["panel", "cost", "gross"], columns="n", values="v", aggfunc="first")
           .reindex(columns=[str(x) for x in NS]))
    print(piv.to_string())

    # ---------------------------------------------------------------- [G] the Calmar bar
    print("\n[G] IDEA 326's GROSS-INVARIANT CALMAR BAR ((0.70/0.60) x Calmar_SPY) ON THESE PANELS")
    for p in panels:
        bar = 1.1667 * ctx[p]["ms"]["Calmar"]
        for cost in COSTS:
            s = df[(df.panel == p) & (df.cost == cost) & (df.conv == "NORM")]
            best = s.loc[s.Calmar.idxmax()]
            n_ok = (s.Calmar >= bar).sum()
            print(f"    {p:>4} {cost:>2}bps | Calmar bar {bar:.4f} | best cell n={best.n} g={best.gross:.2f} "
                  f"Calmar {best.Calmar:.4f} ({best.Calmar-bar:+.4f}) | cells clearing the bar {n_ok}/{len(s)}"
                  f" | cells failing a SHARPE bar {(s[['m_H1','m_H2','m_OOS']].min(axis=1) < 0).sum()}/{len(s)}")

    # ---------------------------------------------------------------- [H] rule 8
    print("\n[H] RULE 8 WALK-FORWARD: (n, gross) chosen on 2008-2016 by IS Sharpe, 2017-2026 read once")
    wf = []
    for p in panels:
        so = ctx[p]["so"]
        for cost in COSTS:
            s = df[(df.panel == p) & (df.cost == cost) & (df.conv == "NORM")]
            pick = s.loc[s.IS_Sharpe.idxmax()]
            anc = s[(s.n == str(ANCHOR_N)) & (s.gross == ANCHOR_G)].iloc[0]
            best = s.loc[s.OOS_Sharpe.idxmax()]
            b2o = metrics(ctx[(p, cost)]["b2"].loc[OOS_START:])
            # does the pick clear 4b in the OOS window read on its own?
            ro = None
            wf.append(dict(panel=p, cost=cost, pick_n=pick.n, pick_g=pick.gross,
                           pick_OOS_CAGR=pick.OOS_CAGR, pick_OOS=pick.OOS_Sharpe, pick_OOS_DD=pick.OOS_MaxDD,
                           anchor_OOS=anc.OOS_Sharpe, anchor_OOS_CAGR=anc.OOS_CAGR, anchor_OOS_DD=anc.OOS_MaxDD,
                           best_n=best.n, best_g=best.gross, best_OOS=best.OOS_Sharpe,
                           regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                           vs_anchor=pick.OOS_Sharpe - anc.OOS_Sharpe,
                           pool_mean_OOS=s.OOS_Sharpe.mean(), pool_sd_OOS=s.OOS_Sharpe.std(),
                           base_OOS=b2o["Sharpe"], base_OOS_CAGR=b2o["CAGR"],
                           spy_OOS=so["Sharpe"], spy_OOS_CAGR=so["CAGR"], spy_OOS_DD=so["MaxDD"]))
            print(f"    {p:>4} {cost:>2}bps | chooser n={pick.n} g={pick.gross:.2f} OOS {pick.OOS_CAGR:6.2%}/"
                  f"{pick.OOS_Sharpe:.3f}/{pick.OOS_MaxDD:7.2%} | anchor n=20 g=0.75 OOS {anc.OOS_CAGR:6.2%}/"
                  f"{anc.OOS_Sharpe:.3f}/{anc.OOS_MaxDD:7.2%} ({pick.OOS_Sharpe-anc.OOS_Sharpe:+.4f}) | "
                  f"OOS-best n={best.n} g={best.gross:.2f} {best.OOS_Sharpe:.3f} "
                  f"(regret {best.OOS_Sharpe-pick.OOS_Sharpe:.4f}) | pool mean {s.OOS_Sharpe.mean():.3f} | "
                  f"RULES v2 {b2o['Sharpe']:.3f} | SPY {so['CAGR']:6.2%}/{so['Sharpe']:.3f}/{so['MaxDD']:7.2%}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"    chooser beats the n=20/g=0.75 anchor OOS in {(wfd.vs_anchor>0).sum()}/{len(wfd)}; "
          f"beats the pool mean in {(wfd.pick_OOS>wfd.pool_mean_OOS).sum()}/{len(wfd)}; "
          f"beats SPY OOS in {(wfd.pick_OOS>wfd.spy_OOS).sum()}/{len(wfd)}; "
          f"beats RULES v2 OOS in {(wfd.pick_OOS>wfd.base_OOS).sum()}/{len(wfd)}")
    print(f"    mean regret {wfd.regret.mean():.4f}, mean vs-anchor {wfd.vs_anchor.mean():+.4f}; "
          f"picked (n,g): {list(zip(wfd.pick_n, wfd.pick_g))}")

    # ---------------------------------------------------------------- [I] the universe question
    print("\n[I] THE UNIVERSE QUESTION: same (conv, g, n, cost) cell, B136 vs U56")
    j = df.pivot_table(index=["conv", "gross", "n", "cost"], columns="panel",
                       values=["Sharpe", "m_H2", "pass4b"], aggfunc="first")
    both = int((j[("pass4b", "B136")] & j[("pass4b", "U56")]).sum())
    u_only = int((~j[("pass4b", "B136")] & j[("pass4b", "U56")]).sum())
    b_only = int((j[("pass4b", "B136")] & ~j[("pass4b", "U56")]).sum())
    print(f"    matched cells: {len(j)} | 4b on BOTH {both} | U56 only {u_only} | B136 only {b_only} | "
          f"neither {len(j)-both-u_only-b_only}")
    print(f"    mean Sharpe B136 {j[('Sharpe','B136')].mean():.4f} vs U56 {j[('Sharpe','U56')].mean():.4f} "
          f"(B136 - U56 = {j[('Sharpe','B136')].mean()-j[('Sharpe','U56')].mean():+.4f}); "
          f"B136 higher in {(j[('Sharpe','B136')]>j[('Sharpe','U56')]).sum()}/{len(j)}")
    print(f"    mean H2 margin B136 {j[('m_H2','B136')].mean():+.4f} vs U56 {j[('m_H2','U56')].mean():+.4f}")

    print(f"\nwrote {SLUG}.grid.csv and {SLUG}.walkforward.csv")


def run_base(px, wfn, cost):
    res = backtest(px, wfn(px), cost_bps=cost, freq=FREQ)
    start = px.index[260]
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].loc[start:].sum(axis=1), res["weights"].loc[start:].gt(0).sum(axis=1))


if __name__ == "__main__":
    main()
