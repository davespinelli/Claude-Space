#!/usr/bin/env python3
"""Idea 372 (cloud, 2026-09-07): price-the-sleeve-fraction-against-the-gross-numeraire-on-an-UNGATED-core.

QUESTION (queue text): idea 30's only 4b passers are UNGATED at c=0.50 (50% QQQ + 50% macro
sleeve, 13.0%/1.041/-20.1%, DD slack 0.2pp).  Idea 351 established the constant exposure
multiplier as the NUMERAIRE for buying drawdown.  Price the sleeve fraction (1-c) on that axis
against a static-gross ladder point at MATCHED MEAN GROSS.  "If the sleeve does not beat its own
ladder point it is a de-grossing device with extra moving parts."

CONSTRUCTION (verbatim from idea 30, which copied idea 24, which copied idea 18 variant B)
    CTRL      : 100% QQQ, ungated, weekly            <- the un-overlaid control (c = 1.00)
    BLEND(c)  : c in QQQ (gate ON/OFF) + (1-c) in the idea-18 variant-B macro sleeve
    LADDER(m) : m in QQQ ungated + (1-m) CASH        <- the numeraire, no moving parts

THE RULER (idea 351's, sign conventions kept so the numbers are comparable to the record)
    dCAGR_pp = 100*(CAGR_book - CAGR_ctrl)          negative when the overlay costs return
    dDD_pp   = 100*(|MaxDD_ctrl| - |MaxDD_book|)    positive when the overlay BUYS drawdown
    ratio    = dDD_pp / (-dCAGR_pp)                 pp of drawdown bought per pp of CAGR paid
    numeraire= |MaxDD_ctrl| / CAGR_ctrl             what a constant multiplier gets for free
The queue's phrasing ("pp of CAGR surrendered per pp of MaxDD bought") is 1/ratio; both printed.
An overlay EARNS ITS MOVING PARTS only if its ratio exceeds the matched-gross ladder point's.

TUNED PARAMETERS: 1 - the core fraction c (10 values, all reported).  The ladder multiplier m is
SOLVED to match the blend's realised mean gross, not tuned.  Panel (U56 / B136), cost rung
(0 / 10 / 25 bps) and the core GATE (ON / OFF) are REPORTED axes: every point of every axis is
printed.  Cost rungs are derived from one 0-bps run per book via the exact identity
net = gross - turnover*c/1e4 (engine.backtest's held weights do not depend on cost_bps; gated).

RULE 8: c chosen on IS Sharpe to 2016-12-31, read once on 2017-2026, against (a) the queue's
anchor c=0.50 ungated, (b) the matched-gross ladder point picked the same way, (c) RULES v2,
(d) SPY.  BOTH KEEP paths reported at every grid point.

CAVEATS: (1) U56/B136 are current-constituent lists - survivorship flatters every level; the
c-differences far less.  (2) this book holds only QQQ + the 9 macro ETFs, so the panel axis is
degenerate by construction (idea 30 measured max |U56-B136| Sharpe 1.09e-04); it is reported
anyway and the degeneracy is re-measured, not assumed.  (3) QQQ's 2009-2017 run is the best
large-cap equity decade in the sample; every level here is conditioned on it.

Deterministic, standalone, offline.  Modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights   # noqa
from engine import backtest, metrics                                     # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
OUT = ROOT / "research" / "backtests" / "2026-09-07_price-the-sleeve-fraction-against-the-gross-numeraire_cloud"

FREQ = "W"
RUNGS = [0, 10, 25]
CS = [0.00, 0.25, 0.40, 0.50, 0.60, 0.70, 0.75, 0.80, 0.90, 1.00]
MS = [round(x, 2) for x in np.arange(0.20, 1.001, 0.05)]     # ladder solve grid
ANCHOR_C = 0.50
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---------------------------------------------------------------- sleeve (idea 18 variant B)
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW, MA_WINDOW = 60, 200


def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_b_weights(px):
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


def core_leg(px, ticker, frac, gate):
    p = px[ticker]
    if gate:
        ma = p.rolling(MA_WINDOW).mean()
        on = (p > ma).astype(float).where(ma.notna(), 0.0)
    else:
        on = pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def blend_weights(px, c, gate, sleeve):
    """c of NAV in QQQ (gated on its own 200d MA when gate=True), (1-c) in the macro sleeve."""
    return core_leg(px, "QQQ", c, gate) + (1.0 - c) * sleeve


def ladder_weights(px, m):
    """m of NAV in ungated QQQ, (1-m) in CASH.  The numeraire: no moving parts."""
    return core_leg(px, "QQQ", m, False)


# ---------------------------------------------------------------- engine helpers
def run(px, w, start):
    r = backtest(px, w, cost_bps=0, freq=FREQ)
    return (r["returns"].loc[start:], r["turnover"].loc[start:],
            r["weights"].loc[start:].sum(axis=1))


def stats(rn):
    m = metrics(rn); h = len(rn) // 2
    o = rn.loc[OOS_START:]; mo = metrics(o)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(rn.iloc[:h])["Sharpe"], H2=metrics(rn.iloc[h:])["Sharpe"],
                OOS=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"])


def ruler(book, ctrl):
    """idea 351's ruler, computed against the book's OWN un-overlaid control."""
    dc = 100.0 * (book["CAGR"] - ctrl["CAGR"])
    dd = 100.0 * (abs(ctrl["MaxDD"]) - abs(book["MaxDD"]))
    ratio = dd / (-dc) if dc < -1e-9 else np.nan          # undefined when the overlay is free
    return dict(dCAGR_pp=dc, dDD_pp=dd, ratio=ratio,
                inv_ratio=(1.0 / ratio if ratio and ratio == ratio and abs(ratio) > 1e-12 else np.nan),
                dSharpe=book["Sharpe"] - ctrl["Sharpe"])


# ---------------------------------------------------------------- per-panel sweep
def sweep(px, panel):
    start = px.index[260]
    sleeve = sleeve_b_weights(px)
    books, rows = {}, []

    def add(name, w, kind, c=np.nan, gate=np.nan, m=np.nan):
        rg, tau, gr = run(px, w, start)
        books[name] = (rg, tau, gr)
        for k in RUNGS:
            rn = rg - tau * k / 1e4
            rows.append(dict(panel=panel, book=name, kind=kind, c=c, gate=gate, m=m, bps=k,
                             gross=gr.mean(), turn=tau.mean() * 252, **stats(rn)))

    # ladder solve grid (the numeraire)
    for m in MS:
        add(f"LADDER_m{m:.2f}", ladder_weights(px, m), "LADDER", m=m)
    gmap = {m: rows[[r["book"] for r in rows].index(f"LADDER_m{m:.2f}")]["gross"] for m in MS}

    def solve_m(target):
        """Realised mean gross is monotone and near-linear in m; interpolate then verify."""
        xs, ys = np.array(MS), np.array([gmap[m] for m in MS])
        if target <= ys.min(): return float(xs[0])
        if target >= ys.max(): return float(xs[-1])
        return float(np.interp(target, ys, xs))

    # blends
    for gate in [False, True]:
        for c in CS:
            add(f"BLEND_c{c:.2f}_g{int(gate)}", blend_weights(px, c, gate, sleeve),
                "BLEND", c=c, gate=gate)
    # controls
    add("RULESv2", rules_v2_weights(px), "CTRL")
    add("RULESv1", rules_v1_weights(px), "CTRL")
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    for k in RUNGS:
        rows.append(dict(panel=panel, book="SPY", kind="CTRL", c=np.nan, gate=np.nan, m=np.nan,
                         bps=k, gross=1.0, turn=0.0, **stats(spy)))
    df = pd.DataFrame(rows)

    # matched-gross ladder point for every (c, gate), solved once (gross is cost-free)
    matched = []
    for gate in [False, True]:
        for c in CS:
            g = df[(df.book == f"BLEND_c{c:.2f}_g{int(gate)}") & (df.bps == 0)].gross.iloc[0]
            mm = solve_m(g)
            w = ladder_weights(px, mm)
            rg, tau, gr = run(px, w, start)
            books[f"MATCH_c{c:.2f}_g{int(gate)}"] = (rg, tau, gr)
            for k in RUNGS:
                rn = rg - tau * k / 1e4
                matched.append(dict(panel=panel, book=f"MATCH_c{c:.2f}_g{int(gate)}", kind="MATCH",
                                    c=c, gate=gate, m=mm, bps=k, gross=gr.mean(),
                                    turn=tau.mean() * 252, target_gross=g, **stats(rn)))
    md = pd.DataFrame(matched)
    df = pd.concat([df, md], ignore_index=True)
    print(f"  [{panel}] {len(px)} rows {px.index[0].date()}->{px.index[-1].date()} eval from {start.date()};"
          f" gross-match residual max {np.abs(md.gross - md.target_gross).max():.2e}")
    return df, books


# ---------------------------------------------------------------- main
def main():
    print("=" * 118)
    print("IDEA 372 - price the sleeve fraction (1-c) against the GROSS NUMERAIRE at matched mean gross")
    print("=" * 118)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    frames, allbooks = [], {}
    for name, px in panels.items():
        d, b = sweep(px, name)
        frames.append(d); allbooks[name] = b
    df = pd.concat(frames, ignore_index=True)
    df.to_csv(f"{OUT}.grid.csv", index=False)

    # ---- GATE 0: cost identity
    px = panels["U56"]; start = px.index[260]
    sl = sleeve_b_weights(px)
    e = []
    for c in [0.50, 0.80]:
        for k in RUNGS:
            direct = metrics(backtest(px, blend_weights(px, c, False, sl), cost_bps=k,
                                      freq=FREQ)["returns"].loc[start:])["Sharpe"]
            got = df[(df.panel == "U56") & (df.book == f"BLEND_c{c:.2f}_g0") & (df.bps == k)].Sharpe.iloc[0]
            e.append(abs(direct - got))
    print(f"\nGATE 0  cost identity vs engine.backtest(cost_bps=k): max abs diff {max(e):.2e}")

    # ---- GATE 1: idea 30's published anchor cell (U56 @10bps, c=0.50, gate OFF): 13.0%/1.041/-20.1%
    a = df[(df.panel == "U56") & (df.book == "BLEND_c0.50_g0") & (df.bps == 10)].iloc[0]
    print(f"GATE 1  idea 30's 4b passer (U56 @10bps, c=0.50, ungated): "
          f"{a.CAGR:.1%} / {a.Sharpe:.3f} / {a.MaxDD:.1%}   (published 13.0% / 1.041 / -20.1%)")

    # ---- GATE 2: panel degeneracy
    j = df[df.book.str.startswith(("BLEND", "LADDER", "MATCH"))].pivot_table(
        index=["book", "bps"], columns="panel", values=["Sharpe", "CAGR", "MaxDD"])
    dg = {k: float(np.abs(j[k]["U56"] - j[k]["B136"]).max()) for k in ["Sharpe", "CAGR", "MaxDD"]}
    print(f"GATE 2  panel axis degeneracy, max |U56-B136|: " + "  ".join(f"{k} {v:.2e}" for k, v in dg.items())
          + "   (idea 30 measured Sharpe 1.09e-04)")

    # ---- 1. the ruler: sleeve vs its matched-gross ladder point, every c x gate x rung x panel
    print("\n" + "=" * 118)
    print("1. THE RULER - overlay vs its OWN un-overlaid control (CTRL = 100% QQQ ungated = BLEND c=1.00 g=0)")
    print("   ratio = pp of MaxDD bought per pp of CAGR paid (idea 351 sign).  1/ratio = the queue's phrasing.")
    print("   numeraire = |MaxDD_ctrl| / CAGR_ctrl.   BEATS = sleeve ratio > matched-gross ladder ratio.")
    print("=" * 118)
    out = []
    for p in panels:
        for k in RUNGS:
            sub = df[(df.panel == p) & (df.bps == k)].set_index("book")
            ctrl = sub.loc["BLEND_c1.00_g0"]
            numer = abs(ctrl.MaxDD) / ctrl.CAGR if ctrl.CAGR > 0 else np.nan
            for gate in [False, True]:
                for c in CS:
                    b = sub.loc[f"BLEND_c{c:.2f}_g{int(gate)}"]
                    mm = sub.loc[f"MATCH_c{c:.2f}_g{int(gate)}"]
                    rb, rm = ruler(b, ctrl), ruler(mm, ctrl)
                    out.append(dict(panel=p, bps=k, gate=gate, c=c, gross=b.gross, m=mm.m,
                                    CAGR=b.CAGR, Sharpe=b.Sharpe, MaxDD=b.MaxDD,
                                    sleeve_dCAGR=rb["dCAGR_pp"], sleeve_dDD=rb["dDD_pp"],
                                    sleeve_ratio=rb["ratio"], sleeve_invratio=rb["inv_ratio"],
                                    sleeve_dSharpe=rb["dSharpe"],
                                    ladder_CAGR=mm.CAGR, ladder_Sharpe=mm.Sharpe, ladder_MaxDD=mm.MaxDD,
                                    ladder_dCAGR=rm["dCAGR_pp"], ladder_dDD=rm["dDD_pp"],
                                    ladder_ratio=rm["ratio"], ladder_dSharpe=rm["dSharpe"],
                                    numeraire=numer,
                                    BEATS=bool(rb["ratio"] > rm["ratio"]) if (rb["ratio"] == rb["ratio"]
                                          and rm["ratio"] == rm["ratio"]) else np.nan,
                                    BEATS_Sharpe=bool(b.Sharpe > mm.Sharpe)))
    R = pd.DataFrame(out)
    R.to_csv(f"{OUT}.ruler.csv", index=False)
    cols = ["c", "gross", "m", "CAGR", "Sharpe", "MaxDD", "sleeve_dCAGR", "sleeve_dDD", "sleeve_ratio",
            "ladder_CAGR", "ladder_Sharpe", "ladder_MaxDD", "ladder_dCAGR", "ladder_dDD", "ladder_ratio",
            "numeraire", "BEATS", "BEATS_Sharpe"]
    for p in panels:
        for gate in [False, True]:
            for k in RUNGS:
                s = R[(R.panel == p) & (R.gate == gate) & (R.bps == k)]
                print(f"\n--- {p}  gate={'ON ' if gate else 'OFF'}  {k} bps ---")
                print(s[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    print("\n" + "=" * 118)
    print("1b. SUMMARY of the head-to-head (points with a defined ratio, i.e. the sleeve costs CAGR)")
    print("=" * 118)
    d = R.dropna(subset=["sleeve_ratio", "ladder_ratio"])
    print(f"points priced: {len(d)} of {len(R)}")
    print(f"sleeve ratio > matched-gross ladder ratio : {int(d.BEATS.sum())}/{len(d)}")
    print(f"sleeve Sharpe > matched-gross ladder Sharpe: {int(R.BEATS_Sharpe.sum())}/{len(R)}")
    print(f"sleeve ratio > the numeraire |MaxDD|/CAGR  : {int((d.sleeve_ratio > d.numeraire).sum())}/{len(d)}")
    print(f"ladder ratio > the numeraire |MaxDD|/CAGR  : {int((d.ladder_ratio > d.numeraire).sum())}/{len(d)}")
    print("\nmedian ratio by (gate, rung):")
    print(d.groupby(["gate", "bps"])[["sleeve_ratio", "ladder_ratio", "numeraire", "sleeve_dSharpe",
                                      "ladder_dSharpe"]].median().to_string(float_format=lambda x: f"{x:.4f}"))
    print("\nsleeve ratio MINUS ladder ratio, by (panel, gate, rung):")
    d = d.assign(edge=d.sleeve_ratio - d.ladder_ratio)
    print(d.groupby(["panel", "gate", "bps"]).edge.agg(["count", "median", "min", "max"]).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ---- 2. both KEEP paths
    print("\n" + "=" * 118)
    print("2. BOTH KEEP PATHS - every blend and every matched-gross ladder point")
    print("=" * 118)
    kp = []
    for p in panels:
        for k in RUNGS:
            s = df[(df.panel == p) & (df.bps == k)].set_index("book")
            v2, spy = s.loc["RULESv2"], s.loc["SPY"]
            for b in [f"BLEND_c{c:.2f}_g{int(g)}" for g in [0, 1] for c in CS] + \
                     [f"MATCH_c{c:.2f}_g{int(g)}" for g in [0, 1] for c in CS]:
                r = s.loc[b]
                bars = [("H1", r.H1 > spy.H1), ("H2", r.H2 > spy.H2), ("OOS", r.OOS > spy.OOS),
                        ("DD", abs(r.MaxDD) <= 0.60 * abs(spy.MaxDD)),
                        ("CAGR", r.CAGR >= 0.70 * spy.CAGR)]
                kp.append(dict(panel=p, bps=k, book=b, CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD,
                               H1=r.H1, H2=r.H2, OOS=r.OOS,
                               v4a=bool(r.H1 > v2.H1 and r.H2 > v2.H2 and r.MaxDD >= v2.MaxDD),
                               v4b=all(x for _, x in bars),
                               fail4b=next((kk for kk, x in bars if not x), "")))
    K = pd.DataFrame(kp)
    K.to_csv(f"{OUT}.keeppaths.csv", index=False)
    for p in panels:
        spy = df[(df.panel == p) & (df.book == "SPY") & (df.bps == 10)].iloc[0]
        v2 = df[(df.panel == p) & (df.book == "RULESv2") & (df.bps == 10)].iloc[0]
        print(f"\n{p}: SPY {spy.CAGR:.2%}/{spy.Sharpe:.3f}/{spy.MaxDD:.2%} halves {spy.H1:.3f}/{spy.H2:.3f} "
              f"OOS {spy.OOS:.3f}  |  RULES v2 @10bps {v2.CAGR:.2%}/{v2.Sharpe:.3f}/{v2.MaxDD:.2%} "
              f"halves {v2.H1:.3f}/{v2.H2:.3f} OOS {v2.OOS:.3f}  |  4b bars H1>{spy.H1:.3f} H2>{spy.H2:.3f} "
              f"OOS>{spy.OOS:.3f} DD<{0.60*abs(spy.MaxDD):.2%} CAGR>{0.70*spy.CAGR:.2%}")
    print(f"\n4a TRUE {int(K.v4a.sum())}/{len(K)}   4b TRUE {int(K.v4b.sum())}/{len(K)}")
    print("first failing 4b bar:", K[~K.v4b].fail4b.value_counts().to_dict())
    print("\n4b passers (all):")
    print(K[K.v4b].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\n4b pass counts, BLEND vs matched-gross LADDER:")
    K2 = K.assign(kind=np.where(K.book.str.startswith("BLEND"), "BLEND", "MATCH"),
                  gate=K.book.str[-1])
    print(K2.groupby(["kind", "gate"]).v4b.agg(["sum", "count"]).to_string())

    # ---- 3. rule 8
    print("\n" + "=" * 118)
    print("3. RULE 8 - c chosen on IS Sharpe <=2016, read once on 2017-2026 (ungated core, the 4b form)")
    print("=" * 118)
    wf = []
    for p in panels:
        for gate in [False, True]:
            for k in RUNGS:
                IS = {}
                for c in CS:
                    rg, tau, _ = allbooks[p][f"BLEND_c{c:.2f}_g{int(gate)}"]
                    rn = (rg - tau * k / 1e4).loc[:IS_END]
                    IS[c] = metrics(rn)["Sharpe"]
                pick = max(IS, key=lambda x: IS[x])
                def oos(book):
                    rg, tau, _ = allbooks[p][book]
                    return metrics((rg - tau * k / 1e4).loc[OOS_START:])
                mo = oos(f"BLEND_c{pick:.2f}_g{int(gate)}")
                ml = oos(f"MATCH_c{pick:.2f}_g{int(gate)}")
                ma = oos(f"BLEND_c{ANCHOR_C:.2f}_g{int(gate)}")
                best = max(CS, key=lambda c: oos(f"BLEND_c{c:.2f}_g{int(gate)}")["Sharpe"])
                mb = oos(f"BLEND_c{best:.2f}_g{int(gate)}")
                wf.append(dict(panel=p, gate=gate, bps=k, pick=pick, IS_Sharpe=IS[pick],
                               OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                               ladder_OOS=ml["Sharpe"], ladder_OOS_CAGR=ml["CAGR"],
                               ladder_OOS_MaxDD=ml["MaxDD"],
                               anchor_c=ANCHOR_C, anchor_OOS=ma["Sharpe"],
                               oos_best_c=best, oos_best_OOS=mb["Sharpe"],
                               regret=mb["Sharpe"] - mo["Sharpe"],
                               vs_ladder=mo["Sharpe"] - ml["Sharpe"]))
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nchooser picks the anchor c=0.50 in {int((W['pick'] == ANCHOR_C).sum())}/{len(W)} cells; "
          f"beats its matched-gross ladder point OOS in {int((W.vs_ladder > 0).sum())}/{len(W)}; "
          f"median regret {W.regret.median():.4f}")
    print("\nfiles:", f"{OUT}.grid.csv / .ruler.csv / .keeppaths.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
