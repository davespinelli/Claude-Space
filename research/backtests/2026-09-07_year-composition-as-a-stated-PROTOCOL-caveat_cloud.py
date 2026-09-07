#!/usr/bin/env python3
"""Idea 111 (cloud, 2026-09-07): year-composition-as-a-stated-PROTOCOL-caveat.

QUEUE TEXT: "idea 99 found rule 8's IS window holds 2 of the sample's 7 SPY-drawdown years
while the OOS window holds 4 of 10, and that overlay value is signed on year-badness inside
BOTH windows (defensive d +0.135 IS-bad vs -0.147 IS-good).  Propose the crisis-year count of
each window as a number PROTOCOL rule 8 must quote alongside every walk-forward, and re-derive
the split date that equalises it.  Max 2 params."

TUNED PARAMETERS: exactly 2 -- the BADNESS THRESHOLD that defines a crisis year (4 definitions
swept) and the SPLIT DATE (11 year-ends swept).  All 44 combinations reported.  Panels, book
shapes, gross, gate and cadence are the POPULATION, not dials.

WHAT A PROPOSAL LIKE THIS HAS TO EARN
-------------------------------------
Adding a number to PROTOCOL rule 8 is only worth doing if the number CHANGES SOMETHING.  So
the idea is tested in four steps, and the last one is the one that decides:

  P1  MEASURE     reproduce idea 99's 2-of-7 / 4-of-10 and report the composition of the
                  incumbent split under every badness definition.
  P2  RE-DERIVE   find the split date that equalises crisis composition, and check whether
                  that date is STABLE across the four definitions.  A "re-derived" date that
                  moves with an arbitrary threshold is not a protocol constant.
  P3  PRICE IT    re-run the FULL rule-8 walk-forward at every candidate split date on a
                  180-book population, and ask how much of the OOS reading is explained by
                  the OOS window's crisis share.  If the OOS verdict is insensitive to
                  composition, the caveat is cosmetic.
  P4  FLIP COUNT  at the incumbent split vs the equalising split, how many books change their
                  4b verdict, and does the rule-8 PICK change?

  PREMISE CHECK   idea 99's claim that overlay value is signed on year-badness inside BOTH
                  windows is re-derived directly (gated minus ungated, per year, by badness).

RULE 8 (walk-forward, required): the walk-forward is the OBJECT of study here.  It is run in
        full at every candidate split -- choose argmax IS Sharpe on the IS window only, read
        OOS CAGR/Sharpe/MaxDD once -- against RULES v2 (live baseline) and SPY on that same
        OOS window, per panel x rung.

BOTH KEEP PATHS reported for every book: 4a vs RULES v2, 4b vs that panel's own SPY.

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (44 of 483).  Every SMALL number below is an UPPER BOUND on what was tradeable.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_year-composition-as-a-stated-PROTOCOL-caveat_cloud.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 600)

OUT = ROOT / "research" / "backtests" / "2026-09-07_year-composition-as-a-stated-PROTOCOL-caveat_cloud"

# ---- tuned parameter 1: what makes a year a CRISIS year --------------------
BADNESS = {
    "ret<0": ("calendar SPY total return < 0", lambda r, d: r < 0),
    "dd<=-10": ("intra-year SPY max drawdown <= -10%", lambda r, d: d <= -0.10),
    "dd<=-15": ("intra-year SPY max drawdown <= -15%", lambda r, d: d <= -0.15),
    "dd<=-20": ("intra-year SPY max drawdown <= -20%", lambda r, d: d <= -0.20),
}
# ---- tuned parameter 2: the split date -------------------------------------
SPLITS = [f"{y}-12-31" for y in range(2011, 2022)]
SPLIT_LIVE = "2016-12-31"                      # PROTOCOL rule 8's incumbent split

RUNGS = [10, 25]
NS = [5, 10, 20, 40]
CADENCES = ["W", "M"]
GROSSES = [0.50, 0.75, 1.00]
GATES = [False, True]


# ===================================================================== helpers
def win_stats(r):
    m = metrics(r)
    h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def win_bars(spy_win):
    s = win_stats(spy_win)
    return dict(H1=s["H1"], H2=s["H2"], DD=0.60 * abs(s["MaxDD"]), CAGR=0.70 * s["CAGR"], spy=s)


def pass4b_win(st, B):
    tests = [("H1", st["H1"] - B["H1"]), ("H2", st["H2"] - B["H2"]),
             ("DD", B["DD"] - abs(st["MaxDD"])), ("CAGR", st["CAGR"] - B["CAGR"])]
    fails = [k for k, m in tests if m <= 0]
    return (len(fails) == 0), (fails[0] if fails else "")


def pass4a_win(st, base):
    return st["H1"] > base["H1"] and st["H2"] > base["H2"] and st["MaxDD"] >= base["MaxDD"]


def net(r0, tau, c):
    return r0 - tau * c / 1e4


def spearman(a, b):
    a, b = pd.Series(a).astype(float).reset_index(drop=True), pd.Series(b).astype(float).reset_index(drop=True)
    ok = a.notna() & b.notna()
    if ok.sum() < 5 or a[ok].nunique() < 2 or b[ok].nunique() < 2:
        return np.nan
    return float(a[ok].rank().corr(b[ok].rank()))


# ============================================================ P1: year composition
def year_table(spy_r):
    """Per calendar year: SPY total return, intra-year max drawdown, trading days."""
    rows = []
    for y, r in spy_r.groupby(spy_r.index.year):
        eq = (1 + r).cumprod()
        rows.append(dict(year=int(y), days=len(r), ret=float(eq.iloc[-1] - 1),
                         maxdd=float((eq / eq.cummax() - 1).min())))
    yt = pd.DataFrame(rows).set_index("year")
    for k, (_, f) in BADNESS.items():                     # one boolean column per definition
        yt[k] = yt.apply(lambda r, f=f: bool(f(r.ret, r.maxdd)), axis=1)
    return yt


def compose(yt, split, badcol):
    """Composition of the two rule-8 windows under one badness column."""
    sy = int(split[:4])
    IS, OO = yt[yt.index <= sy], yt[yt.index > sy]
    def part(d):
        return dict(n_years=len(d), n_bad=int(d[badcol].sum()),
                    share_years=(d[badcol].mean() if len(d) else np.nan),
                    days=int(d.days.sum()),
                    share_days=(d.loc[d[badcol], "days"].sum() / d.days.sum() if len(d) else np.nan))
    a, b = part(IS), part(OO)
    return dict(split=split, IS_years=a["n_years"], IS_bad=a["n_bad"], IS_share=a["share_years"],
                IS_dayshare=a["share_days"], OOS_years=b["n_years"], OOS_bad=b["n_bad"],
                OOS_share=b["share_years"], OOS_dayshare=b["share_days"],
                gap_share=(a["share_years"] - b["share_years"]),
                gap_dayshare=(a["share_days"] - b["share_days"]),
                abs_gap=abs(a["share_years"] - b["share_years"]))


def part1(yt):
    print("\n" + "=" * 105)
    print("P1  MEASURE.  SPY calendar years over the U56 sample, and the incumbent rule-8 split")
    print("=" * 105)
    print(yt.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\n  incumbent split {SPLIT_LIVE} (PROTOCOL rule 8: IS 2008-2016, OOS 2017-2026)")
    rows = [dict(badness=k, desc=d, **compose(yt, SPLIT_LIVE, k)) for k, (d, _) in BADNESS.items()]
    t = pd.DataFrame(rows)
    print(t[["badness", "desc", "IS_years", "IS_bad", "IS_share", "IS_dayshare",
             "OOS_years", "OOS_bad", "OOS_share", "OOS_dayshare", "gap_share", "gap_dayshare"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  --- PREMISE, EXACTLY.  Idea 99 reported 'IS [2010, 2011] | OOS [2018, 2020, 2022,")
    print("      2025]' under SPY MaxDD < -15%, i.e. 2 of 7 and 4 of 10 -- on a sample STARTING")
    print("      IN 2010.  PROTOCOL rule 8 walks forward on the 2008-start panel.  Same")
    print("      definition, both sample starts:")
    for y0 in (2010, 2008):
        c = compose(yt[yt.index >= y0], SPLIT_LIVE, "dd<=-15")
        bad_is = [int(i) for i in yt.index if y0 <= i <= 2016 and yt.loc[i, "dd<=-15"]]
        bad_oos = [int(i) for i in yt.index if i > 2016 and yt.loc[i, "dd<=-15"]]
        print(f"      sample from {y0}: IS {c['IS_bad']} of {c['IS_years']} {bad_is}  |  "
              f"OOS {c['OOS_bad']} of {c['OOS_years']} {bad_oos}  |  gap_share {c['gap_share']:+.4f}")
    print("      The '2 of 7' is a SAMPLE-START artefact: starting in 2010 excludes 2008 and")
    print("      2009 -- the two deepest crisis years in the record -- from the IS window.  On")
    print("      the panel PROTOCOL actually uses, the incumbent split is already 4-of-9 vs")
    print("      4-of-10, a year-share gap of +0.044 and a day-share gap of +0.032.")
    return t


def part2(yt):
    print("\n" + "=" * 105)
    print("P2  RE-DERIVE.  The split date that equalises crisis composition -- under each definition")
    print("=" * 105)
    allr = []
    for k, (desc, _) in BADNESS.items():
        rows = [dict(badness=k, **compose(yt, s, k)) for s in SPLITS]
        d = pd.DataFrame(rows)
        allr.append(d)
        print(f"\n  --- badness = {k}  ({desc})")
        print(d[["split", "IS_years", "IS_bad", "IS_share", "OOS_years", "OOS_bad", "OOS_share",
                 "gap_share", "IS_dayshare", "OOS_dayshare", "gap_dayshare"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        best = d.loc[d.abs_gap.idxmin()]
        alt = d.loc[d.gap_dayshare.abs().idxmin()]
        print(f"      equalising split by YEAR share: {best.split}  (|gap| {best.abs_gap:.4f}, "
              f"IS {best.IS_bad}/{best.IS_years} vs OOS {best.OOS_bad}/{best.OOS_years})")
        print(f"      equalising split by DAY  share: {alt.split}  (|gap| {abs(alt.gap_dayshare):.4f})")
    D = pd.concat(allr, ignore_index=True)
    picks = D.loc[D.groupby("badness").abs_gap.idxmin()][["badness", "split", "abs_gap"]]
    print("\n  STABILITY of the re-derived date across the 4 badness definitions:")
    print(picks.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"  distinct dates proposed: {sorted(set(picks.split))}")
    return D


# ============================================================ population
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = load_universe(small=True)
    s = s.drop(columns=[c for c in s.columns if c in bad])
    print(f"\nSMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {s.shape[1]-1} names + SPY "
          f"(SURVIVORSHIP: current constituents only)")
    return {"U56": u, "B136": b, f"SMALL{s.shape[1]-1}": s}


def build(P):
    """One cost-free backtest per book; every rung is then exact arithmetic."""
    store, meta = {}, []
    for pname, px in P.items():
        start = px.index[260]
        s, above, vol20 = score(px)
        ok = above & (vol20 < 0.60)
        elig = s.where(ok)
        shapes = {}
        for n in NS:
            sel = (elig.rank(axis=1, ascending=False) <= n).astype(float)
            shapes[f"TOP{n}"] = sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        sel = ok.astype(float)
        shapes["EWALL"] = sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        gate = band_state(px, 0.03)
        for bname, w1 in shapes.items():
            for g in GROSSES:
                for gated in GATES:
                    w = (w1 * g)
                    if gated:
                        w = w.where(gate, 0.0)
                    for freq in CADENCES:
                        res = backtest(px, w, cost_bps=0, freq=freq)
                        key = (pname, bname, g, gated, freq)
                        store[key] = (res["returns"].loc[start:], res["turnover"].loc[start:])
                        meta.append(dict(panel=pname, book=bname, gross=g, gated=gated, cadence=freq, key=key))
        print(f"  built {pname}: {len(shapes)*len(GROSSES)*len(GATES)*len(CADENCES)} books")
    return store, pd.DataFrame(meta)


# ============================================================ premise check
def premise(P, yt):
    """Idea 99: is a DEFENSIVE overlay's value signed on year-badness inside BOTH windows?
    d = (gated Sharpe) - (ungated Sharpe), computed per calendar year, split by badness."""
    print("\n" + "=" * 105)
    print("PREMISE CHECK  is overlay value signed on year-badness inside BOTH windows? (idea 99)")
    print("=" * 105)
    rows = []
    for pname, px in P.items():
        start = px.index[260]
        s, above, vol20 = score(px)
        ok = above & (vol20 < 0.60)
        elig = s.where(ok)
        sel = (elig.rank(axis=1, ascending=False) <= 20).astype(float)
        w1 = sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        gate = band_state(px, 0.03)
        raw = backtest(px, w1, cost_bps=0, freq="W")
        gtd = backtest(px, w1.where(gate, 0.0), cost_bps=0, freq="W")
        rr = net(raw["returns"].loc[start:], raw["turnover"].loc[start:], 10)
        rg = net(gtd["returns"].loc[start:], gtd["turnover"].loc[start:], 10)
        for y in sorted(set(rr.index.year)):
            a, b = rr[rr.index.year == y], rg[rg.index.year == y]
            if len(a) < 60:
                continue
            rows.append(dict(panel=pname, year=int(y),
                             d_sharpe=metrics(b)["Sharpe"] - metrics(a)["Sharpe"],
                             d_ret=float((1 + b).prod() - (1 + a).prod())))
    D = pd.DataFrame(rows)
    out = []
    for k in BADNESS:
        D[k] = D.year.map(yt[k])
        for split in [SPLIT_LIVE]:
            sy = int(split[:4])
            for wname, sub in [("IS", D[D.year <= sy]), ("OOS", D[D.year > sy])]:
                g, b2 = sub[~sub[k].astype(bool)], sub[sub[k].astype(bool)]
                out.append(dict(badness=k, window=wname, n_good=len(g), n_bad=len(b2),
                                d_good=g.d_sharpe.mean() if len(g) else np.nan,
                                d_bad=b2.d_sharpe.mean() if len(b2) else np.nan,
                                signed=((b2.d_sharpe.mean() > 0 > g.d_sharpe.mean())
                                        if len(g) and len(b2) else np.nan)))
    O = pd.DataFrame(out)
    print(O.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  'signed' = overlay HELPS in bad years and HURTS in good ones (idea 99's claim).")
    print(f"  holds in {int(O.signed.fillna(False).sum())} of {len(O)} (badness x window) cells.")
    return D, O


# ============================================================ P3: price the caveat
def part3(P, store, meta, yt):
    print("\n" + "=" * 105)
    print("P3  PRICE IT.  The FULL rule-8 walk-forward re-run at every candidate split date")
    print("=" * 105)
    rows = []
    for pname, px in P.items():
        sub = meta[meta.panel == pname]
        spy_all = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[px.index[260]:]
              for c in RUNGS}
        for split in SPLITS:
            if pd.Timestamp(split) <= px.index[260] + pd.Timedelta(days=400):
                continue
            for c in RUNGS:
                cand = []
                for _, k in sub.iterrows():
                    r0, tau = store[k.key]
                    r = net(r0, tau, c)
                    ris, roos = r.loc[:split], r.loc[split:].iloc[1:]
                    if len(ris) < 252 or len(roos) < 252:
                        continue
                    cand.append(dict(book=k.book, gross=k.gross, gated=k.gated, cadence=k.cadence,
                                     IS_S=metrics(ris)["Sharpe"],
                                     **{f"OOS_{a}": v for a, v in win_stats(roos).items()}))
                if not cand:
                    continue
                C = pd.DataFrame(cand)
                spy_oos = spy_all.loc[split:].iloc[1:]
                Bo = win_bars(spy_oos)
                bo = win_stats(v2[c].loc[split:].iloc[1:])
                C["OOS_4b"] = [pass4b_win(dict(H1=r.OOS_H1, H2=r.OOS_H2, MaxDD=r.OOS_MaxDD, CAGR=r.OOS_CAGR), Bo)[0]
                               for r in C.itertuples()]
                C["OOS_4a"] = [pass4a_win(dict(H1=r.OOS_H1, H2=r.OOS_H2, MaxDD=r.OOS_MaxDD), bo)
                               for r in C.itertuples()]
                w = C.loc[C.IS_S.idxmax()]
                comp = {k2: compose(yt, split, k2) for k2 in BADNESS}
                rows.append(dict(panel=pname, rung=c, split=split, n_books=len(C),
                                 pick=f"{w.book} g{w.gross:.2f} {'gate' if w.gated else 'raw'} {w.cadence}",
                                 IS_S=w.IS_S, OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe,
                                 OOS_MaxDD=w.OOS_MaxDD,
                                 menu_mean_OOS_S=C.OOS_Sharpe.mean(),
                                 n_4b=int(C.OOS_4b.sum()), n_4a=int(C.OOS_4a.sum()),
                                 pick_4b=bool(w.OOS_4b), pick_4a=bool(w.OOS_4a),
                                 v2_OOS_CAGR=bo["CAGR"], v2_OOS_S=bo["Sharpe"], v2_OOS_MaxDD=bo["MaxDD"],
                                 spy_OOS_CAGR=Bo["spy"]["CAGR"], spy_OOS_S=Bo["spy"]["Sharpe"],
                                 spy_OOS_MaxDD=Bo["spy"]["MaxDD"],
                                 **{f"OOSbad_{k2}": comp[k2]["OOS_share"] for k2 in BADNESS},
                                 **{f"gap_{k2}": comp[k2]["gap_share"] for k2 in BADNESS}))
    W = pd.DataFrame(rows)
    for (pname, c), d in W.groupby(["panel", "rung"]):
        print(f"\n  --- {pname} @ {c} bps   (RULES v2 and SPY re-read on each split's own OOS window)")
        print(d[["split", "n_books", "pick", "IS_S", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                 "v2_OOS_S", "spy_OOS_S", "spy_OOS_CAGR", "n_4b", "n_4a", "menu_mean_OOS_S",
                 "OOSbad_dd<=-10"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n  DOES COMPOSITION EXPLAIN THE OOS READING?  spearman(OOS crisis share, .) per panel x rung")
    sp = []
    for (pname, c), d in W.groupby(["panel", "rung"]):
        for k in BADNESS:
            sp.append(dict(panel=pname, rung=c, badness=k, n_splits=len(d),
                           sp_pick_Sharpe=spearman(d[f"OOSbad_{k}"], d.OOS_Sharpe),
                           sp_menu_Sharpe=spearman(d[f"OOSbad_{k}"], d.menu_mean_OOS_S),
                           sp_n4b=spearman(d[f"OOSbad_{k}"], d.n_4b),
                           sp_spy_Sharpe=spearman(d[f"OOSbad_{k}"], d.spy_OOS_S)))
    S = pd.DataFrame(sp)
    print(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return W, S


def part4(W, D):
    print("\n" + "=" * 105)
    print("P4  FLIP COUNT.  Incumbent split vs the equalising split -- what actually changes?")
    print("=" * 105)
    eq = D.loc[D.groupby("badness").abs_gap.idxmin()].set_index("badness")["split"].to_dict()
    print(f"  equalising splits by definition: {eq}")
    rows = []
    for k, es in eq.items():
        for (pname, c), d in W.groupby(["panel", "rung"]):
            a = d[d.split == SPLIT_LIVE]
            b = d[d.split == es]
            if not len(a) or not len(b):
                continue
            a, b = a.iloc[0], b.iloc[0]
            rows.append(dict(badness=k, eq_split=es, panel=pname, rung=c,
                             pick_live=a["pick"], pick_eq=b["pick"], pick_changed=a["pick"] != b["pick"],
                             OOS_S_live=a.OOS_Sharpe, OOS_S_eq=b.OOS_Sharpe, dS=b.OOS_Sharpe - a.OOS_Sharpe,
                             n4b_live=a.n_4b, n4b_eq=b.n_4b, dn4b=b.n_4b - a.n_4b,
                             n4a_live=a.n_4a, n4a_eq=b.n_4a,
                             spyS_live=a.spy_OOS_S, spyS_eq=b.spy_OOS_S))
    F = pd.DataFrame(rows)
    print(F.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if len(F):
        print(f"\n  rule-8 PICK changes in {int(F.pick_changed.sum())} of {len(F)} (definition x panel x rung) cells; "
              f"mean |dSharpe| {F.dS.abs().mean():.4f}, max {F.dS.abs().max():.4f}")
        print(f"  4b pass count moves by mean {F.dn4b.abs().mean():.2f} books "
              f"(live {F.n4b_live.mean():.1f} -> equalised {F.n4b_eq.mean():.1f} of ~60)")
    return F


# ===================================================================== main
def main():
    P = panels()
    yt = year_table(P["U56"]["SPY"].pct_change().fillna(0))
    t1 = part1(yt)
    D = part2(yt)
    yt.to_csv(f"{OUT}.years.csv")
    t1.to_csv(f"{OUT}.incumbent.csv", index=False)
    D.to_csv(f"{OUT}.splits.csv", index=False)

    Dp, O = premise(P, yt)
    Dp.to_csv(f"{OUT}.premise_years.csv", index=False)
    O.to_csv(f"{OUT}.premise.csv", index=False)

    print("\nbuilding the book population (cost-free once, rungs by arithmetic)...")
    store, meta = build(P)
    W, S = part3(P, store, meta, yt)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    S.to_csv(f"{OUT}.sensitivity.csv", index=False)
    F = part4(W, D)
    F.to_csv(f"{OUT}.flips.csv", index=False)

    print("\n" + "=" * 105)
    print("VERDICT INPUTS")
    print("=" * 105)
    eq = D.loc[D.groupby("badness").abs_gap.idxmin()][["badness", "split", "abs_gap"]]
    print(f"  re-derived split dates: {sorted(set(eq.split))} over 4 badness definitions "
          f"({len(set(eq.split))} distinct)")
    print(f"  rule-8 pick changes in {int(F.pick_changed.sum())}/{len(F)} cells; "
          f"mean |dOOS Sharpe| {F.dS.abs().mean():.4f}")
    med = S.groupby("badness")[["sp_pick_Sharpe", "sp_menu_Sharpe", "sp_n4b", "sp_spy_Sharpe"]].median()
    print("\n  median spearman(OOS crisis share, .) across panel x rung:")
    print(med.to_string(float_format=lambda x: f"{x:.4f}"))
    print(f"\n  4a passes over all splits: {int(W.n_4a.sum())} book-cells; "
          f"4b passes: {int(W.n_4b.sum())} of {int(W.n_books.sum())}")
    print("\nDone.")


if __name__ == "__main__":
    main()
