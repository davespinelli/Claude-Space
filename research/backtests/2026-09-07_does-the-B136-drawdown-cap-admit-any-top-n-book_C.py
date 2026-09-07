#!/usr/bin/env python3
"""Idea 333: does the B136 DRAWDOWN CAP admit ANY top-n book at all?

Idea 329 (lane C, same day) found the pre-registered cell (B136, n=20, band m=20, gross 0.75,
weekly) fails 4b on TWO bars, H2 (-0.0170) and the DRAWDOWN CAP (-0.0020), at every cadence
and band width tried, while the same family clears 4b at 15 of 15 cells on U56.  Idea 326
found on SMALL439 that 4b's DD cap and CAGR floor are not two independent bars but one
GROSS-INVARIANT CALMAR BAR:

        MaxDD  >= -0.60 * |MaxDD_SPY|      and      CAGR >= 0.70 * CAGR_SPY
    =>  CAGR / |MaxDD|  >=  (0.70/0.60) * (CAGR_SPY / |MaxDD_SPY|)  =  1.16667 * Calmar_SPY

If de-grossing scaled returns exactly linearly, Calmar would not move with gross at all and
the joint region would be decided by the RANKING alone -- no gross can rescue a book whose
Calmar is short of the bar.  On SMALL439 that made the admissible gross band EMPTY at all 5 n.
This run asks the same question of B136, and measures how close to gross-invariant the
empirical Calmar actually is (cash earns 0 and positions drift between rebalances, so the
closed form is an approximation, not an identity).

PRE-REGISTRATION.  The family is idea 329's ANCHOR arm, fixed before anything is run:

        panel    B136 (research/universe_broad.json, 136 names + SPY) -- the question's panel
        book     top-n of the v1 composite (vol scaler OFF) among RULES v1 eligible names
                 (200d MA up, vol20 < 0.60), NORM weights w_i = g / k_t, k_t = |{rank <= n}|
        band     m = 0 (hard cut) -- idea 329's anchor; NOT swept
        cadence  weekly -- the live book's cadence; NOT swept

    THE TWO TUNED PARAMETERS, and the only two:
        n      in {10, 20, 40, 80, ALL}
        gross  in {0.375, 0.50, 0.625, 0.75}
    = 20 grid points per panel, ALL of them reported at each of the three cost rungs.
    The cost rung {0, 10, 25} bps is a reported axis, not a choice; 10 bps is PROTOCOL's.

DECISION RULES, fixed in advance (read on B136 at 10 bps):
    R1  ADMISSIBLE-DD REGION: the set of (n, g) with MaxDD >= -0.60 * |MaxDD_SPY|.
        Empty  -> the DD cap admits NO top-n book on B136 and the queue's question is answered
                  NO on its own terms.
        Non-empty -> R2.
    R2  Inside that region, is the CAGR floor met at any point?  Empty intersection ->
        the two bars are jointly empty on B136 as idea 326 found on SMALL439, and the
        finding is the CALMAR BAR, not the DD cap.
    R3  FULL 4b at any (n, g)?  A DD+CAGR pass is NOT a 4b pass -- the H1/H2/OOS Sharpe bars
        are reported at every point and 4b is a conjunction.
    A pass on R1 or R2 alone changes no rules; only R3 plus rule 8 could make a candidate.

U56 and SMALL439 are run on the IDENTICAL grid as context.  They cannot change the B136
verdict; they say whether the DD cap's behaviour under (n, g) is a panel fact or a B136 fact.

Rule 8 walk-forward: (n, g) chosen on 2008-2016 IS Sharpe at 10 bps, 2017-2026 read ONCE,
against the anchor (n=20, g=0.75), the OOS-best cell (chooser regret), RULES v2 (live) and SPY.
Both KEEP paths are evaluated at every grid point: 4a vs the LIVE RULES v2 book, 4b vs SPY.

GATES (all exact, run before any new number is read):
    G1  fast_backtest vs products/backtester/engine.backtest at 0 and 25 bps.
    G2  n=ALL at g=0.75 nests eligible-equal-weight-at-0.75 exactly.
    G3  the (B136, n=20, g=0.75) cell reproduces idea 329's committed grid row (W, m=0).

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so CAGR levels
are optimistic and the CAGR floor is therefore tested in the book's FAVOUR; a floor that fails
here fails harder on a survivorship-free panel.  (2) The 4a comparand RULES v2 always runs at
its live weekly cadence and full live gross, so the gross dial moves the idea arm only.
(3) SMALL439 starts 2010-01-04 and drops the 44 tickers with max_1d_move >= 1.0.

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

SLUG = "2026-09-07_does-the-B136-drawdown-cap-admit-any-top-n-book_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL = 0.60
FREQ = "W"                              # the live cadence; never moved
PRE_PANEL = "B136"
NS = [10, 20, 40, 80, "ALL"]
GROSSES = [0.375, 0.50, 0.625, 0.75]
COSTS = [0, 10, 25]
ANCHOR = (20, 0.75)
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
CALMAR_MULT = 0.70 / 0.60               # 4b's DD cap + CAGR floor as one Calmar bar


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book (idea 329's anchor arm)
def rank_frame(px, drop_spy=False):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk.notna() if n == "ALL" else rk <= n


def weights_from(sel, gross):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


# ---------------------------------------------------------------- fast backtester (idea 325/329's)
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
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def breakeven(r0, t0, spy, lo=0.0, hi=200.0):
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
    print(f"PRE-REGISTERED: family = idea 329's anchor arm (composite, vol scaler OFF, v1 "
          f"eligibility, NORM weights, m=0, weekly).")
    print(f"Two tuned params: n in {NS} x gross in {GROSSES} = {len(NS)*len(GROSSES)} points, "
          f"ALL reported at {COSTS} bps.")
    print("R1 admissible-DD region on B136 -> R2 CAGR floor inside it -> R3 full 4b anywhere.")

    panels = {}
    print("\n[panels]")
    panels["B136"] = load_universe(broad=True)
    panels["U56"] = load_universe()
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
        calmar_spy = ms_["CAGR"] / abs(ms_["MaxDD"])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        print(f"    4b bars here: H1>{s1:.3f} H2>{s2:.3f} OOS>{so['Sharpe']:.3f} "
              f"MaxDD>={-0.60*abs(ms_['MaxDD']):.2%} CAGR>={0.70*ms_['CAGR']:.2%}")
        print(f"    Calmar_SPY {calmar_spy:.4f} -> the joint DD+CAGR bar is Calmar >= "
              f"{CALMAR_MULT*calmar_spy:.4f}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, FREQ)
        base = {c: (br - bt * c / 1e4).loc[start:] for c in COSTS}
        bm = metrics(base[10]); b1, b2 = hs(base[10]); bo = metrics(base[10].loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f}")

        if pname == "B136":
            print("\n[0] GATES")
            wA = weights_from(sel_hard(rk, ANCHOR[0]), ANCHOR[1])
            eng = backtest(px, wA, cost_bps=0.0, freq=FREQ)
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, FREQ)
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    G1 fast_backtest vs engine.backtest (W): max|dr| {d1:.3e} max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq=FREQ)
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    G1 derived rung r(25) vs backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            scored = elig & rk.notna()
            ew_scored = 0.75 * scored.astype(float).div(
                scored.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            d4 = np.abs(weights_from(sel_hard(rk, "ALL"), 0.75) - ew_scored).max().max()
            print(f"    G2 n=ALL @0.75 nests SCORED-eligible equal weight: max|dw| {d4:.3e}")
            assert d4 < 1e-12
            ewall = 0.75 * elig.astype(float).div(
                elig.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            gap = int((elig & rk.isna()).loc[start:].values.sum())
            d5 = np.abs(weights_from(sel_hard(rk, "ALL"), 0.75) - ewall).loc[start:].max().max()
            print(f"    G2b n=ALL is NOT plain eligible-equal-weight on this panel: "
                  f"{gap} name-days after {start.date()} are eligible but UNSCORED (no 252d "
                  f"history), max|dw| {d5:.3e}.  The family is rank-based, so 'ALL' means "
                  f"'all SCORED eligible names' throughout; stated, not asserted away.")

        print(f"\n[A] GRID {pname} -- n x gross, ALL points (m=0, weekly)")
        hdr = f"    {'n':>4} {'gross':>6} {'turn/yr':>8} {'names':>6} |"
        hdr += " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'Calmar':>7} "
                          f"{'H1/H2':>13} {'OOS':>6} {'DDok':>4} {'CGok':>4} {'4b':>2} {'4a':>2}"
                          for c in COSTS)
        print(hdr)
        for n in NS:
            sel = sel_hard(rk, n)
            for g in GROSSES:
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel, g), 0.0, FREQ)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                rec = dict(panel=pname, n=str(n), gross=g, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), avg_gross=gr.loc[start:].mean(),
                           breakeven_bps=breakeven(r0, t0, spy),
                           calmar_spy=calmar_spy, calmar_bar=CALMAR_MULT * calmar_spy)
                line = f"    {str(n):>4} {g:>6.3f} {tpy:>8.2f} {rec['names']:>6.1f} |"
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    ok4a, d4a, f4a = bars_4a(r, base[c])
                    calmar = mt["CAGR"] / abs(mt["MaxDD"])
                    ddok, cgok = d4b["DD"] >= 0, d4b["CAGR"] >= 0
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{calmar:>7.4f} {h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ddok else 'n':>4} {'Y' if cgok else 'n':>4} "
                             f"{'Y' if ok4b else 'n':>2} {'Y' if ok4a else 'n':>2} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"Calmar_{c}": calmar,
                                f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"ddok_{c}": ddok, f"cgok_{c}": cgok,
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a),
                                f"m4b_H1_{c}": d4b["H1"], f"m4b_H2_{c}": d4b["H2"],
                                f"m4b_OOS_{c}": d4b["OOS"], f"m4b_DD_{c}": d4b["DD"],
                                f"m4b_CAGR_{c}": d4b["CAGR"]})
                print(line)
                rows.append(rec)
        for r_ in rows:
            if r_["panel"] == pname:
                r_.update(spy_H1=s1, spy_H2=s2, spy_OOS=so["Sharpe"], spy_CAGR=ms_["CAGR"],
                          spy_MaxDD=ms_["MaxDD"], base_H1=b1, base_H2=b2,
                          base_OOS=bo["Sharpe"], base_Sharpe=bm["Sharpe"],
                          base_MaxDD=bm["MaxDD"])

    df = pd.DataFrame(rows)
    df.to_csv(gcsv, index=False)
    analyse(df, panels)


# ---------------------------------------------------------------- analysis
def region(d, c, key):
    return d[d[f"{key}_{c}"].astype(bool)]


def analyse(df, panels):
    # ---- G3: reproduce idea 329's committed anchor row
    print("\n[0b] G3 CROSS-RUN GATE vs idea 329's committed grid (B136, W, m=0, n=20, g=0.75)")
    pg = OUT / "2026-09-07_does-the-BAND-rescue-the-B136-H2-bar_C.grid.csv"
    mine = df[(df.panel == "B136") & (df.n == "20") & (df.gross == 0.75)]
    if pg.exists() and len(mine):
        p = pd.read_csv(pg)
        p = p[(p.panel == "B136") & (p.cadence == "W") & (p.m == 0)]
        if len(p):
            a, b = p.iloc[0], mine.iloc[0]
            for k in ("CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10", "OOS_Sharpe_10"):
                print(f"    {k:>14}  idea329 {a[k]:>10.6f}   this run {b[k]:>10.6f}   "
                      f"|d| {abs(a[k]-b[k]):.3e}")
            print("    -> the anchor cell is the SAME OBJECT in both runs"
                  if max(abs(a[k] - b[k]) for k in ("CAGR_10", "Sharpe_10", "MaxDD_10")) < 1e-12
                  else "    -> MISMATCH: the two runs do not price the same anchor")
        else:
            print("    parent row not found")
    else:
        print("    parent grid CSV not found; gate skipped")

    # ---- [B] R1/R2/R3 on B136
    print(f"\n[B] R1 / R2 / R3 on {PRE_PANEL} at 10 bps -- the question, on its own terms")
    d = df[df.panel == PRE_PANEL]
    spy_dd, spy_cagr = d.iloc[0]["spy_MaxDD"], d.iloc[0]["spy_CAGR"]
    print(f"    bars: MaxDD >= {-0.60*abs(spy_dd):.2%}   CAGR >= {0.70*spy_cagr:.2%}")
    print(f"    {'n':>4} {'gross':>6} {'MaxDD':>8} {'DD marg':>9} {'CAGR':>8} {'CAGR marg':>10} "
          f"{'Calmar':>8} {'H1 marg':>8} {'H2 marg':>8} {'OOS marg':>9}  DD CG 4b")
    for _, r in d.iterrows():
        print(f"    {r['n']:>4} {r['gross']:>6.3f} {r['MaxDD_10']:>8.2%} {r['m4b_DD_10']:>+9.4f} "
              f"{r['CAGR_10']:>8.2%} {r['m4b_CAGR_10']:>+10.4f} {r['Calmar_10']:>8.4f} "
              f"{r['m4b_H1_10']:>+8.4f} {r['m4b_H2_10']:>+8.4f} {r['m4b_OOS_10']:>+9.4f}  "
              f"{'Y' if r['ddok_10'] else 'n':>2} {'Y' if r['cgok_10'] else 'n':>2} "
              f"{'Y' if r['keep4b_10'] else 'n':>2}")
    r1 = region(d, 10, "ddok"); r2 = r1[r1["cgok_10"].astype(bool)]; r3 = region(d, 10, "keep4b")
    print(f"\n    R1 admissible-DD region: {len(r1)}/{len(d)} points"
          + (f" -> {[(x.n, x.gross) for x in r1.itertuples()]}" if len(r1) else " -> EMPTY"))
    print(f"    R2 CAGR floor inside R1:  {len(r2)}/{len(r1) if len(r1) else 0} points"
          + (f" -> {[(x.n, x.gross) for x in r2.itertuples()]}" if len(r2) else " -> EMPTY"))
    print(f"    R3 full 4b anywhere:      {len(r3)}/{len(d)} points"
          + (f" -> {[(x.n, x.gross) for x in r3.itertuples()]}" if len(r3) else " -> EMPTY"))

    # ---- [C] the Calmar closed form: is the joint bar gross-invariant?
    print("\n[C] IS THE JOINT BAR GROSS-INVARIANT?  Calmar by (n, gross) at 10 bps, per panel")
    inv = []
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        bar = dd.iloc[0]["calmar_bar"]
        print(f"    {pname}: bar = {CALMAR_MULT:.4f} x Calmar_SPY = {bar:.4f}")
        print("        " + f"{'n':>5}" + "".join(f"{g:>10.3f}" for g in GROSSES)
              + f"{'spread':>10}{'max-bar':>10}")
        for n in NS:
            v = dd[dd.n == str(n)].set_index("gross")
            cal = [v.loc[g, "Calmar_10"] for g in GROSSES]
            sp = max(cal) - min(cal)
            inv.append(dict(panel=pname, n=str(n), calmar_min=min(cal), calmar_max=max(cal),
                            spread=sp, bar=bar, best_minus_bar=max(cal) - bar))
            print("        " + f"{str(n):>5}" + "".join(f"{c:>10.4f}" for c in cal)
                  + f"{sp:>10.4f}{max(cal)-bar:>+10.4f}")
        print(f"        -> max spread across gross, any n: "
              f"{max(x['spread'] for x in inv if x['panel']==pname):.4f}  "
              f"(gross-invariant closed form predicts 0)")
    pd.DataFrame(inv).to_csv(OUT / f"{SLUG}.calmar.csv", index=False)

    # ---- [D] which bar binds, per panel, at the best cell for each bar
    print("\n[D] TIGHTEST BAR at 10 bps, per panel (over all 20 cells: best margin per bar)")
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        s = {k: dd[f"m4b_{k}_10"].max() for k in ("H1", "H2", "OOS", "DD", "CAGR")}
        arg = {k: dd.loc[dd[f"m4b_{k}_10"].idxmax(), ["n", "gross"]].tolist()
               for k in s}
        print(f"    {pname}: " + "  ".join(f"{k} {v:+.4f}@{arg[k][0]}/{arg[k][1]:.3f}"
                                           for k, v in s.items()))
        print(f"        never-clearable bars on this panel (best margin < 0): "
              f"{[k for k, v in s.items() if v < 0] or 'none'}")

    # ---- [E] pass counts
    print("\n[E] KEEP-PATH PASS COUNTS over the full reported grid "
          f"({len(df.panel.unique())} panels x {len(NS)} n x {len(GROSSES)} gross)")
    for c in COSTS:
        n4b = int(df[f"keep4b_{c}"].sum()); n4a = int(df[f"keep4a_{c}"].sum())
        nDD = int(df[f"ddok_{c}"].sum()); nCG = int(df[f"cgok_{c}"].sum())
        print(f"    c={c:>2} bps: DD-cap {nDD}/{len(df)}  CAGR-floor {nCG}/{len(df)}  "
              f"4b {n4b}/{len(df)}  4a {n4a}/{len(df)}")
        for key, lbl in (("keep4b", "4b"), ("keep4a", "4a")):
            for _, r in df[df[f"{key}_{c}"].astype(bool)].iterrows():
                print(f"        {lbl} PASS  {r['panel']:>9} n={r['n']:<4} g={r['gross']:.3f} "
                      f"{r[f'CAGR_{c}']:.2%} / {r[f'Sharpe_{c}']:.3f} / {r[f'MaxDD_{c}']:.2%} "
                      f"OOS {r[f'OOS_Sharpe_{c}']:.3f}  breakeven {r['breakeven_bps']:.1f} bps")

    # ---- [F] rule 8 walk-forward
    print("\n[F] RULE 8 WALK-FORWARD: (n, gross) chosen on 2008-2016 IS Sharpe @10 bps, "
          "2017-2026 read once")
    wf = []
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        pick = dd.loc[dd["IS_Sharpe_10"].idxmax()]
        best = dd.loc[dd["OOS_Sharpe_10"].idxmax()]
        anch = dd[(dd.n == str(ANCHOR[0])) & (dd.gross == ANCHOR[1])].iloc[0]
        print(f"\n    {pname}: SPY OOS {pick['spy_OOS']:.3f} | RULES v2 OOS {pick['base_OOS']:.3f}")
        for lbl, r in (("IS pick", pick), ("anchor (20, 0.75)", anch), ("OOS best", best)):
            ok, _, f = bars_4b(pd.Series(dtype=float), pd.Series(dtype=float)) if False else (
                bool(r["keep4b_10"]), None, r["fail4b_10"])
            print(f"        {lbl:<18} n={r['n']:<4} g={r['gross']:.3f} "
                  f"IS {r['IS_Sharpe_10']:.3f} | OOS Sharpe {r['OOS_Sharpe_10']:.3f} "
                  f"CAGR {r['OOS_CAGR_10']:.2%} MaxDD {r['OOS_MaxDD_10']:.2%} | "
                  f"full-sample 4b {'Y' if ok else 'n'} "
                  f"({f if isinstance(f, str) and f else '-'})")
        print(f"        chooser regret (OOS best - IS pick): "
              f"{best['OOS_Sharpe_10'] - pick['OOS_Sharpe_10']:+.4f}")
        print(f"        IS pick vs anchor OOS {pick['OOS_Sharpe_10'] - anch['OOS_Sharpe_10']:+.4f}"
              f" | vs SPY {pick['OOS_Sharpe_10'] - pick['spy_OOS']:+.4f}"
              f" | vs RULES v2 {pick['OOS_Sharpe_10'] - pick['base_OOS']:+.4f}")
        wf.append(dict(panel=pname, pick_n=pick["n"], pick_gross=pick["gross"],
                       IS_Sharpe=pick["IS_Sharpe_10"], OOS_Sharpe=pick["OOS_Sharpe_10"],
                       OOS_CAGR=pick["OOS_CAGR_10"], OOS_MaxDD=pick["OOS_MaxDD_10"],
                       anchor_OOS=anch["OOS_Sharpe_10"], oosbest_OOS=best["OOS_Sharpe_10"],
                       oosbest_n=best["n"], oosbest_gross=best["gross"],
                       regret=best["OOS_Sharpe_10"] - pick["OOS_Sharpe_10"],
                       spy_OOS=pick["spy_OOS"], base_OOS=pick["base_OOS"]))
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    # ---- [G] the n dial at fixed gross, and the gross dial at fixed n
    print("\n[G] THE TWO DIALS SEPARATELY at 10 bps (Sharpe / MaxDD), per panel")
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        print(f"    {pname}  Sharpe")
        print("        " + f"{'n':>5}" + "".join(f"{g:>16.3f}" for g in GROSSES))
        for n in NS:
            v = dd[dd.n == str(n)].set_index("gross")
            print("        " + f"{str(n):>5}" + "".join(
                f"{v.loc[g,'Sharpe_10']:>9.3f}/{v.loc[g,'MaxDD_10']:>6.1%}" for g in GROSSES))
        sp_n = dd.groupby("n")["Sharpe_10"].max()
        print(f"        best Sharpe by n: " + "  ".join(f"{k}:{v:.3f}" for k, v in sp_n.items()))

    # ---- [I] the admissible GROSS INTERVAL per n, by inverting the two bars in g
    print("\n[I] ADMISSIBLE GROSS INTERVAL per n at 10 bps (the queue's '(n, g) region'), from a "
          "linear fit of MaxDD(g) and CAGR(g) over the four grid points")
    print("    Both quantities are near-linear in gross (cash earns 0); R2 of each fit is shown "
          "so the inversion is auditable.  Values outside [0.375, 0.750] are EXTRAPOLATION and "
          "are flagged, not claimed.")
    ivs = []
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        dd_cap = 0.60 * abs(dd.iloc[0]["spy_MaxDD"]); cg_floor = 0.70 * dd.iloc[0]["spy_CAGR"]
        print(f"    {pname}: |MaxDD| <= {dd_cap:.2%}, CAGR >= {cg_floor:.2%}")
        print(f"        {'n':>5} {'g_hi(DD)':>9} {'g_lo(CAGR)':>11} {'interval':>22} "
              f"{'R2 DD':>7} {'R2 CAGR':>8}  status")
        for n in NS:
            v = dd[dd.n == str(n)].sort_values("gross")
            g = v["gross"].values
            y_dd = np.abs(v["MaxDD_10"].values); y_cg = v["CAGR_10"].values
            out = []
            for y in (y_dd, y_cg):
                a, b = np.polyfit(g, y, 1)
                r2 = 1 - ((y - (a * g + b)) ** 2).sum() / ((y - y.mean()) ** 2).sum()
                out.append((a, b, r2))
            (a1, b1, r1), (a2, b2, r2_) = out
            g_hi = (dd_cap - b1) / a1 if a1 else np.nan          # DD cap binds from above
            g_lo = (cg_floor - b2) / a2 if a2 else np.nan        # CAGR floor binds from below
            empty = not (g_lo <= g_hi)
            oor = (g_lo > max(GROSSES)) or (g_hi < min(GROSSES)) or (g_lo < min(GROSSES) and
                                                                     g_hi > max(GROSSES))
            status = ("EMPTY" if empty else
                      ("non-empty (partly OUTSIDE the tested grid)" if
                       (g_lo < min(GROSSES) or g_hi > max(GROSSES)) else "non-empty, IN grid"))
            print(f"        {str(n):>5} {g_hi:>9.3f} {g_lo:>11.3f} "
                  f"{('[' + f'{max(g_lo,0):.3f}' + ', ' + f'{g_hi:.3f}' + ']'):>22} "
                  f"{r1:>7.4f} {r2_:>8.4f}  {status}")
            ivs.append(dict(panel=pname, n=str(n), g_hi_DD=g_hi, g_lo_CAGR=g_lo,
                            width=g_hi - g_lo, empty=empty, out_of_grid=oor,
                            r2_dd=r1, r2_cagr=r2_))
        w = [x for x in ivs if x["panel"] == pname]
        print(f"        -> admissible gross band EMPTY at {sum(x['empty'] for x in w)}/{len(w)} n; "
              f"widest band {max(x['width'] for x in w):+.3f} at n="
              f"{max(w, key=lambda x: x['width'])['n']}")
    pd.DataFrame(ivs).to_csv(OUT / f"{SLUG}.gross_interval.csv", index=False)

    print("\n[H] BREAKEVEN (highest cost rung at which all five 4b bars hold), bps")
    for pname in df.panel.unique():
        dd = df[df.panel == pname]
        print(f"    {pname}")
        print("        " + f"{'n':>5}" + "".join(f"{g:>10.3f}" for g in GROSSES))
        for n in NS:
            v = dd[dd.n == str(n)].set_index("gross")
            print("        " + f"{str(n):>5}" + "".join(
                f"{v.loc[g,'breakeven_bps']:>10.1f}" for g in GROSSES))


if __name__ == "__main__":
    main()
