#!/usr/bin/env python3
"""Idea 374 (cloud, 2026-09-07): does-the-SECOND-worst-drawdown-episode-bound-every-overlay.

QUESTION (queue text): idea 350 found overlay DD improvement saturates at the runner-up episode
(the residual window is 98.3% unreachable in 230/486 displaced points).  Compute, for every book,
the gap between the WORST and the SECOND-WORST drawdown episode and ask whether it predicts the
maximum achievable dMaxDD of ANY overlay.  "If it does, PROTOCOL should quote an overlay's DD
headroom before it is run."

THE STATISTIC (zero backtests, computable from the base book's equity curve alone)
    episodes  = maximal under-water intervals of the equity curve, disjoint by construction
                (each one opens at an all-time high).  D1 = deepest, D2 = second deepest.
    HEADROOM  H_pp = 100 * (|D1| - |D2|)
H is the drawdown improvement available to an overlay that erases the worst episode ENTIRELY and
leaves every other day of the book untouched.  MaxDD is a min-statistic, so such an overlay lands
exactly on the runner-up.  The queue's claim is that H bounds -- and predicts -- what any overlay
can buy.

WHY THE CLAIM CANNOT BE UNIVERSAL, AND HOW THE FILE SPLITS IT
A constant exposure multiplier (idea 351's numeraire) scales EVERY episode by g, so it buys
g*|D1| of drawdown and can exceed H at will.  The saturation argument only applies to overlays
that leave the book alone outside their armed regime.  So the overlay corpus is pre-registered in
three CLASSES and the bound is tested inside each, not pooled:
    GLOBAL     GROSS g in {0.40,0.50,0.60,0.75,0.90}      (scales every day)
               VOLTGT t in {0.08,0.10,0.12,0.15}          (scales most days)
    SELECTIVE  BREADTH B in {0.30,0.40,0.50} x cut {0.50,1.00}   (idea 41/42/48's dial)
               DDCTRL  T in {0.05,0.10,0.15,0.20}, cut 0.50      (idea 40's)
               HIVOL80 arm on the book's own expanding 80th-pct vol, cut 0.50 (idea 246/247's)
    CADENCE    rebalance M, Q against the W base                 (idea 351's worst ratio)
Every overlay is causal: it reads the book's own lagged returns / the panel's lagged breadth.

BOOKS: idea 350's six canonical forms (EWALL, TOP3, TOP10, TOP20, MAEW, RULESV2) x 3 panels
(U56, B136, SMALL439) x 3 cost rungs (0/10/25 bps) = 54 stamped books, 22 overlay points each
= 1188 priced points, ALL reported.

TUNED PARAMETERS: none.  Every dial above is a REPORTED axis (all points printed and committed
to the .grid.csv); the file fits no parameter to any outcome.

RULE 8: H is re-computed on the IS window (<= 2016-12-31) alone and scored against the OOS window
(2017-01-01 ->, equity restarted) as an EX-ANTE predictor of what the overlay corpus actually buys
there, against two naive rivals (the book's own IS |MaxDD|, and the IS realised max dDD).  That is
the queue's proposal tested as stated: a number PROTOCOL would quote BEFORE the overlay is run.

BOTH KEEP PATHS are evaluated at every one of the 1188 points (4a vs the live RULES v2 on the same
panel; 4b vs SPY over the same evaluation window).

CAVEATS: (1) U56/B136/SMALL439 are current-constituent lists -- survivorship flatters every level
here, and SMALL439 most of all (the 44 names with max_1d_move >= 1.0 are dropped per
data/small_meta.csv, but delisted names were never in the screen).  (2) D1/D2 are window
statistics: both are functions of which crises the sample contains, which is exactly why the
IS/OOS split is run.  (3) SMALL439 starts 2010, so its windows are shorter than U56/B136's.

Deterministic, standalone, offline.  Modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score            # noqa
from engine import backtest, metrics                                    # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
OUT = ROOT / "research" / "backtests" / "2026-09-07_does-the-SECOND-worst-drawdown-episode-bound-every-overlay_cloud"

MAX_VOL, GROSS, BAND = 0.60, 0.75, 0.03          # idea 350's constants, unchanged
FORMS = ["EWALL", "TOP3", "TOP10", "TOP20", "MAEW", "RULESV2"]
COSTS = [0, 10, 25]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260
FREQ = "W"


# ---------------------------------------------------------------- panels (idea 350's, verbatim)
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def panels():
    p = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    for k, v in p.items():
        print(f"    {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")
    return p


def book_cols(px, panel):
    return [c for c in px.columns if not (panel == "SMALL439" and c == "SPY")]


def breadth(px, panel):
    cols = [c for c in px.columns if c != "SPY"]
    q = px[cols]
    above = q > q.rolling(200).mean()
    priced = q.notna() & q.rolling(200).mean().notna()
    return (above & priced).sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)


def weights_for(px, panel, form):
    cols = book_cols(px, panel)
    q = px[cols]
    if form == "EWALL":
        e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
        w = GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    elif form.startswith("TOP"):
        n = int(form[3:])
        s = score(q, vol_scale=False)[0]
        _, above, vol20 = score(q)
        rank = s.where(above & (vol20 < MAX_VOL)).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float) * (GROSS / n)
    elif form == "MAEW":
        above = q > q.rolling(200).mean()
        e = above.astype(float).where(q.notna(), 0.0)
        n_priced = q.notna().sum(axis=1).replace(0, np.nan)
        w = GROSS * e.div(n_priced, axis=0).fillna(0.0)
    elif form == "RULESV2":
        w = rules_v2_weights(q, band=BAND, gross=GROSS)
    else:
        raise ValueError(form)
    return w.reindex(columns=px.columns).fillna(0.0)


# ---------------------------------------------------------------- drawdown episodes
def episodes(r):
    """All maximal under-water intervals of (1+r).cumprod(), deepest first.

    Each interval opens on an all-time high, so the intervals are disjoint and MaxDD is the
    depth of the first one.  Returns [(start, trough, depth<0), ...]."""
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1.0
    grp = (dd >= -1e-12).cumsum()
    out = []
    for _, sub in dd.groupby(grp):
        d = float(sub.min())
        if d < -1e-12:
            out.append((sub.index[0], sub.idxmin(), d))
    return sorted(out, key=lambda x: x[2])


def headroom(r):
    """(|D1|, |D2|, H_pp) in pp.  D2 = 0 when the path has a single under-water episode."""
    ep = episodes(r)
    d1 = abs(ep[0][2]) if ep else 0.0
    d2 = abs(ep[1][2]) if len(ep) > 1 else 0.0
    return 100 * d1, 100 * d2, 100 * (d1 - d2)


# ---------------------------------------------------------------- overlays (all causal)
def ov_gross(w, ctx, g):
    return w * (g / GROSS)


def ov_voltgt(w, ctx, t):
    vol = ctx["base_r"].rolling(20).std() * np.sqrt(252)
    k = (t / vol.replace(0, np.nan)).clip(upper=1.0).shift(1).reindex(w.index).fillna(1.0)
    return w.mul(k, axis=0)


def ov_breadth(w, ctx, B, cut):
    armed = (ctx["E"].shift(1) < B).reindex(w.index).fillna(False)
    return w.mul(np.where(armed, 1.0 - cut, 1.0), axis=0)


def ov_ddctrl(w, ctx, T, cut):
    eq = (1 + ctx["base_r"]).cumprod()
    dd = (eq / eq.cummax() - 1.0).shift(1).reindex(w.index).fillna(0.0)
    return w.mul(np.where(dd < -T, 1.0 - cut, 1.0), axis=0)


def ov_hivol(w, ctx, cut):
    vol = ctx["base_r"].rolling(20).std() * np.sqrt(252)
    thr = vol.expanding(252).quantile(0.80)
    armed = (vol > thr).shift(1).reindex(w.index).fillna(False)
    return w.mul(np.where(armed, 1.0 - cut, 1.0), axis=0)


OVERLAYS = (
    [(f"GROSS_g{g:.2f}", "GLOBAL", (lambda g: (lambda w, c: ov_gross(w, c, g)))(g), FREQ)
     for g in [0.40, 0.50, 0.60, 0.75, 0.90]] +
    [(f"VOLTGT_t{t:.2f}", "GLOBAL", (lambda t: (lambda w, c: ov_voltgt(w, c, t)))(t), FREQ)
     for t in [0.08, 0.10, 0.12, 0.15]] +
    [(f"BREADTH_B{B:.2f}_c{c:.2f}", "SELECTIVE",
      (lambda B, c: (lambda w, ctx: ov_breadth(w, ctx, B, c)))(B, c), FREQ)
     for B in [0.30, 0.40, 0.50] for c in [0.50, 1.00]] +
    [(f"DDCTRL_T{T:.2f}", "SELECTIVE", (lambda T: (lambda w, c: ov_ddctrl(w, c, T, 0.50)))(T), FREQ)
     for T in [0.05, 0.10, 0.15, 0.20]] +
    [("HIVOL80_c0.50", "SELECTIVE", lambda w, c: ov_hivol(w, c, 0.50), FREQ)] +
    [(f"CADENCE_{f}", "CADENCE", (lambda w, c: w), f) for f in ["M", "Q"]]
)


# ---------------------------------------------------------------- metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def bars_4a(r, base):
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), f


def stats(r):
    m = metrics(r); o = metrics(r.loc[OOS_START:]); h1, h2 = hs(r)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS=o["Sharpe"], OOS_CAGR=o["CAGR"], OOS_MaxDD=o["MaxDD"])


def spearman(a, b):
    a, b = pd.Series(a, dtype=float), pd.Series(b, dtype=float)
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(a[ok].rank().corr(b[ok].rank()))


# ---------------------------------------------------------------- per-panel sweep
def sweep(px, panel):
    start = px.index[WARMUP]
    E = breadth(px, panel)
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    base_v2 = backtest(px, rules_v2_weights(px[book_cols(px, panel)]).reindex(columns=px.columns).fillna(0.0),
                       cost_bps=0, freq=FREQ)
    rows = []
    for form in FORMS:
        w = weights_for(px, panel, form)
        b0 = backtest(px, w, cost_bps=0, freq=FREQ)
        br, bt = b0["returns"].loc[start:], b0["turnover"].loc[start:]
        ctx = {"E": E, "base_r": b0["returns"]}
        runs = {"BASE": (br, bt, b0["weights"].loc[start:].sum(axis=1))}
        for name, cls, fn, freq in OVERLAYS:
            o = backtest(px, fn(w, ctx), cost_bps=0, freq=freq)
            runs[name] = (o["returns"].loc[start:], o["turnover"].loc[start:],
                          o["weights"].loc[start:].sum(axis=1))
        for k in COSTS:
            v2 = base_v2["returns"].loc[start:] - base_v2["turnover"].loc[start:] * k / 1e4
            bn = br - bt * k / 1e4
            d1, d2, H = headroom(bn)
            d1i, d2i, Hi = headroom(bn.loc[:IS_END])
            d1o, d2o, Ho = headroom(bn.loc[OOS_START:])
            bs = stats(bn)
            for name, cls, _, _ in [("BASE", "BASE", None, None)] + [(n, c, None, None) for n, c, _, _ in OVERLAYS]:
                orr, ott, ogr = runs[name]
                rn = orr - ott * k / 1e4
                st = stats(rn)
                st["gross"] = float(ogr.mean())
                st["IS_Sharpe"] = metrics(rn.loc[:IS_END])["Sharpe"]
                p4b, f4b = bars_4b(rn, spy)
                p4a, f4a = bars_4a(rn, v2)
                rows.append(dict(
                    panel=panel, form=form, overlay=name, cls=cls, bps=k,
                    base_D1=d1, base_D2=d2, H_pp=H, H_IS=Hi, H_OOS=Ho, D1_IS=d1i, D1_OOS=d1o,
                    base_CAGR=bs["CAGR"], base_Sharpe=bs["Sharpe"], base_MaxDD=bs["MaxDD"],
                    base_OOS=bs["OOS"], turn=ott.mean() * 252, **st,
                    dDD_pp=100 * (abs(bs["MaxDD"]) - abs(st["MaxDD"])),
                    dCAGR_pp=100 * (st["CAGR"] - bs["CAGR"]), dSharpe=st["Sharpe"] - bs["Sharpe"],
                    dDD_IS=100 * (abs(metrics(bn.loc[:IS_END])["MaxDD"]) - abs(metrics(rn.loc[:IS_END])["MaxDD"])),
                    dDD_OOS=100 * (abs(metrics(bn.loc[OOS_START:])["MaxDD"]) - abs(metrics(rn.loc[OOS_START:])["MaxDD"])),
                    pass4a=p4a, fail4a=",".join(f4a), pass4b=p4b, fail4b=",".join(f4b)))
        print(f"    [{panel}/{form}] base @10bps {bn.name if False else ''}"
              f"D1 {d1:.2f} D2 {d2:.2f} H {H:.2f} pp")
    spyrow = []
    for k in COSTS:
        spyrow.append(dict(panel=panel, form="SPY", overlay="SPY", cls="CTRL", bps=k, **stats(spy)))
    return pd.DataFrame(rows), pd.DataFrame(spyrow)


# ---------------------------------------------------------------- gates
def gates(P):
    print("\n" + "=" * 118)
    print("REPRODUCTION GATES")
    print("=" * 118)
    px = P["U56"]; start = px.index[WARMUP]
    # gate 0: cost identity (net = gross - turnover*bps/1e4) used for all three rungs
    w = weights_for(px, "U56", "TOP20")
    b = backtest(px, w, cost_bps=0, freq=FREQ)
    e = []
    for k in COSTS:
        direct = backtest(px, w, cost_bps=k, freq=FREQ)["returns"].loc[start:]
        e.append(float(np.abs(direct - (b["returns"].loc[start:] - b["turnover"].loc[start:] * k / 1e4)).max()))
    print(f"GATE 0  cost identity vs engine.backtest(cost_bps=k): max abs diff {max(e):.2e}")
    # gate 1: idea 40/41's published UNGATED books and the live RULES v2, all U56 @10 bps
    for n, pub in ((3, (0.219, 1.04, -0.258)), (5, (0.165, 0.95, -0.216)), (20, None)):
        rr = backtest(px, weights_for(px, "U56", f"TOP{n}"), cost_bps=10, freq=FREQ)["returns"].loc[start:]
        m = metrics(rr)
        tag = "" if pub is None else (f" vs idea 40/41 published {pub[0]:.1%}/{pub[1]:.2f}/{pub[2]:.1%} -> "
                                      + ("PASS" if abs(m["CAGR"] - pub[0]) < 0.005 and abs(m["Sharpe"] - pub[1]) < 0.02
                                         and abs(m["MaxDD"] - pub[2]) < 0.005 else "FAIL"))
        print(f"GATE 1  U56 TOP{n} @10bps: {m['CAGR']:.1%}/{m['Sharpe']:.2f}/{m['MaxDD']:.1%}{tag}")
    rv2 = backtest(px, rules_v2_weights(px, band=BAND, gross=GROSS), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    m = metrics(rv2)
    ok = abs(m["CAGR"] - 0.0866) < 0.002 and abs(m["Sharpe"] - 1.2056) < 0.01 and abs(m["MaxDD"] + 0.1205) < 0.002
    print(f"GATE 1b LIVE RULES v2 U56 @10bps: {m['CAGR']:.2%}/{m['Sharpe']:.4f}/{m['MaxDD']:.2%} "
          f"vs published 8.66%/1.2056/-12.05% -> {'PASS' if ok else 'FAIL'}")
    # gate 2: idea 41's committed gated cells, reproduced in ITS OWN return-space convention
    # (multiply the realised return path, charge GROSS turnover on each switch).  This file's
    # overlays act in WEIGHT space and are re-run through the engine, so the level differs; the
    # gate exists to tie the depth-invariance FINDING to the committed grid.
    E = breadth(px, "U56")
    w3 = weights_for(px, "U56", "TOP3")
    b3 = backtest(px, w3, cost_bps=0, freq=FREQ)
    rc = (b3["returns"] - b3["turnover"] * 10 / 1e4).loc[start:]
    armed = (E.loc[start:] < 0.30).shift(1).fillna(False)
    i41 = ROOT / "research" / "backtests" / "2026-09-07_breadth-gate-depth_cloud.grid.csv"
    ref = pd.read_csv(i41).query("panel == 'U56' and n == 3").set_index("depth") if i41.exists() else None
    for d, refd in ((0.25, 0.75), (0.50, 0.50), (1.00, 0.00)):
        mult = pd.Series(np.where(armed, 1.0 - d, 1.0), index=rc.index)
        dm = np.abs(np.diff(np.concatenate([[1.0], mult.values])))
        rg = pd.Series(mult.values * rc.values - dm * GROSS * 10 / 1e4, index=rc.index)
        got = metrics(rg)["MaxDD"]
        exp = float(ref.loc[refd, "MaxDD_10"]) if ref is not None and refd in ref.index else np.nan
        print(f"GATE 2  idea 41 U56 n=3 mult={1-d:.2f} @10bps (return-space): MaxDD {got:.6f} vs committed "
              f"{exp:.6f} -> {'PASS' if abs(got - exp) < 1e-6 else 'FAIL'}")
    # gate 2b: the same invariance in THIS file's weight-space convention
    ctx = {"E": E, "base_r": b3["returns"]}
    dds = [metrics(backtest(px, ov_breadth(w3, ctx, 0.30, c), cost_bps=10, freq=FREQ)["returns"].loc[start:])["MaxDD"]
           for c in [0.25, 0.50, 1.00]]
    print(f"GATE 2b depth invariance in WEIGHT space, cut 0.25/0.50/1.00: "
          + " / ".join(f"{d:.6f}" for d in dds) + f"   spread {max(dds)-min(dds):.2e}")
    # gate 3: episode decomposition is exact -- deepest episode == MaxDD
    err = []
    for pan, q in P.items():
        s = q.index[WARMUP]
        for form in FORMS:
            rr = backtest(q, weights_for(q, pan, form), cost_bps=10, freq=FREQ)["returns"].loc[s:]
            err.append(abs(abs(episodes(rr)[0][2]) - abs(metrics(rr)["MaxDD"])))
    print(f"GATE 3  deepest episode == MaxDD on all 18 books: max abs diff {max(err):.2e}")


# ---------------------------------------------------------------- analysis
def analyse(df, spy):
    ov = df[df.overlay != "BASE"].copy()
    ov["ratio"] = ov.dDD_pp / ov.H_pp.replace(0, np.nan)
    ov["viol"] = ov.dDD_pp > ov.H_pp + 1e-9

    print("\n" + "=" * 118)
    print("1. THE BOUND:  is  max achievable dMaxDD <= H = |D1| - |D2|  ?   (all 1188 points)")
    print("=" * 118)
    t = ov.groupby("cls").agg(n=("dDD_pp", "size"), viol=("viol", "sum"),
                              med_dDD=("dDD_pp", "median"), max_dDD=("dDD_pp", "max"),
                              med_ratio=("ratio", "median"), max_ratio=("ratio", "max"))
    t["viol_share"] = t.viol / t.n
    print(t.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  same, per cost rung:")
    t2 = ov.groupby(["cls", "bps"]).agg(n=("viol", "size"), viol=("viol", "sum"),
                                        med_ratio=("ratio", "median"))
    t2["viol_share"] = t2.viol / t2.n
    print(t2.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n  class MAXIMUM per book (the queue's object: 'the maximum achievable dMaxDD of ANY overlay')")
    mx = ov.groupby(["panel", "form", "bps", "cls"]).agg(
        H_pp=("H_pp", "first"), D1=("base_D1", "first"), D2=("base_D2", "first"),
        max_dDD=("dDD_pp", "max"), arg=("dDD_pp", "idxmax")).reset_index()
    mx["overlay"] = ov.loc[mx["arg"], "overlay"].values
    mx["ratio"] = mx.max_dDD / mx.H_pp.replace(0, np.nan)
    mx["viol"] = mx.max_dDD > mx.H_pp + 1e-9
    s = mx.groupby("cls").agg(n=("viol", "size"), viol=("viol", "sum"), med_ratio=("ratio", "median"),
                              min_ratio=("ratio", "min"), max_ratio=("ratio", "max"))
    s["viol_share"] = s.viol / s.n
    print(s.to_string(float_format=lambda x: f"{x:.3f}"))
    mx.drop(columns=["arg"]).to_csv(f"{OUT}.classmax.csv", index=False)

    print("\n" + "=" * 118)
    print("2. DOES H PREDICT?  Spearman(H, class-max dDD) across the 18 books, per class x rung")
    print("   rival predictor: the book's own |MaxDD| (D1), which needs no episode decomposition")
    print("=" * 118)
    rows = []
    for (cls, k), g in mx.groupby(["cls", "bps"]):
        rows.append(dict(cls=cls, bps=k, n=len(g),
                         rho_H=spearman(g.H_pp, g.max_dDD), rho_D1=spearman(g.D1, g.max_dDD),
                         rho_D2=spearman(g.D2, g.max_dDD),
                         med_H=g.H_pp.median(), med_max=g.max_dDD.median()))
    pr = pd.DataFrame(rows)
    print(pr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("3. WHERE THE BOUND BITES:  headroom utilisation  dDD / H  by overlay family (10 bps)")
    print("=" * 118)
    g10 = ov[ov.bps == 10].copy()
    g10["fam"] = g10.overlay.str.split("_").str[0]
    f = g10.groupby(["cls", "fam"]).agg(n=("ratio", "size"), med_ratio=("ratio", "median"),
                                        p90_ratio=("ratio", lambda x: x.quantile(0.90)),
                                        med_dDD=("dDD_pp", "median"), med_dCAGR=("dCAGR_pp", "median"),
                                        med_dSharpe=("dSharpe", "median"), viol=("viol", "sum"))
    print(f.to_string(float_format=lambda x: f"{x:.3f}"))

    print("\n" + "=" * 118)
    print("4. RULE 8 -- H as an EX-ANTE quotable number: fit nothing, quote H_IS, score OOS")
    print("=" * 118)
    is_ = ov.groupby(["panel", "form", "bps", "cls"]).agg(
        H_IS=("H_IS", "first"), H_OOS=("H_OOS", "first"), D1_IS=("D1_IS", "first"),
        max_dDD_IS=("dDD_IS", "max"), max_dDD_OOS=("dDD_OOS", "max")).reset_index()
    is_["bound_ex_ante"] = is_.max_dDD_OOS <= is_.H_IS + 1e-9
    is_["bound_in_window"] = is_.max_dDD_OOS <= is_.H_OOS + 1e-9
    print(is_.groupby("cls").agg(n=("bound_ex_ante", "size"),
                                 held_ex_ante=("bound_ex_ante", "sum"),
                                 held_in_window=("bound_in_window", "sum"),
                                 med_H_IS=("H_IS", "median"), med_H_OOS=("H_OOS", "median"),
                                 med_maxdDD_OOS=("max_dDD_OOS", "median")
                                 ).to_string(float_format=lambda x: f"{x:.3f}"))
    rows = []
    for (cls, k), g in is_.groupby(["cls", "bps"]):
        rows.append(dict(cls=cls, bps=k, n=len(g),
                         rho_HIS=spearman(g.H_IS, g.max_dDD_OOS),
                         rho_D1IS=spearman(g.D1_IS, g.max_dDD_OOS),
                         rho_realisedIS=spearman(g.max_dDD_IS, g.max_dDD_OOS),
                         rho_HOOS=spearman(g.H_OOS, g.max_dDD_OOS)))
    print("\n  Spearman vs OOS-window class-max dDD (18 books per cell):")
    print(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    is_.to_csv(f"{OUT}.walkforward.csv", index=False)

    print("\n" + "=" * 118)
    print("5. KEEP PATHS at every one of the 1188 points")
    print("=" * 118)
    print(f"  4a: {int(df.pass4a.sum())}/{len(df)}     4b: {int(df.pass4b.sum())}/{len(df)}")
    print(df.groupby(["bps"]).agg(n=("pass4b", "size"), p4b=("pass4b", "sum"), p4a=("pass4a", "sum")).to_string())
    print("\n  4b passes by panel x class:")
    pb = df[df.pass4b].groupby(["panel", "cls"]).size()
    print(pb.to_string() if len(pb) else "  none")
    if df.pass4b.any():
        best = df[df.pass4b].sort_values("OOS", ascending=False).head(8)
        print("\n  top 4b passes by OOS Sharpe:")
        print(best[["panel", "form", "overlay", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                    "OOS", "OOS_CAGR", "OOS_MaxDD", "dDD_pp", "turn"]].to_string(
            index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  first failing bar, 4b (all points):")
    print(df.fail4b.replace("", "PASS").str.split(",").str[0].value_counts().to_string())
    print("\n  SPY reference per panel (evaluation window):")
    print(spy[spy.bps == 0][["panel", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS", "OOS_CAGR",
                             "OOS_MaxDD"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))


def byproduct(P, df):
    """The census throws off 4b passers.  The record's standing requirement (ideas 311/351) is
    that any de-grossing overlay must beat its own MATCHED-REALISED-GROSS ladder point, and rule 8
    must be able to pick it.  Both are applied here before anything is called a candidate."""
    print("\n" + "=" * 118)
    print("6. RULE 8 ON THE BOOKS (not on H): IS<=2016 Sharpe picks one of the 23 menu points")
    print("=" * 118)
    rows = []
    for (pan, form, k), g in df.groupby(["panel", "form", "bps"]):
        pick = g.loc[g.IS_Sharpe.idxmax()]
        base = g[g.overlay == "BASE"].iloc[0]
        best = g.loc[g.OOS.idxmax()]
        v2 = df[(df.panel == pan) & (df.form == "RULESV2") & (df.overlay == "BASE") & (df.bps == k)].iloc[0]
        rows.append(dict(panel=pan, form=form, bps=k, pick=pick.overlay, IS=pick.IS_Sharpe,
                         OOS_pick=pick.OOS, OOS_base=base.OOS, OOS_best=best.OOS,
                         regret=best.OOS - pick.OOS, beats_base=pick.OOS > base.OOS,
                         beats_v2=pick.OOS > v2.OOS, pick_4b=pick.pass4b, base_4b=base.pass4b))
    w = pd.DataFrame(rows)
    print(f"  chooser takes an overlay over the base book in {(w['pick'] != 'BASE').sum()}/{len(w)} cells;"
          f" beats its own base book OOS in {int(w.beats_base.sum())}/{len(w)}"
          f" (median dOOS {(w.OOS_pick - w.OOS_base).median():+.4f}); beats live RULES v2 OOS in"
          f" {int(w.beats_v2.sum())}/{len(w)}; mean regret {w.regret.mean():.4f}")
    print(w.groupby("bps").agg(n=("regret", "size"), beats_base=("beats_base", "sum"),
                               beats_v2=("beats_v2", "sum"), mean_regret=("regret", "mean"),
                               pick_4b=("pick_4b", "sum")).to_string(float_format=lambda x: f"{x:.4f}"))
    print("\n  most-picked overlays:", w["pick"].value_counts().head(6).to_dict())
    w.to_csv(f"{OUT}.rule8books.csv", index=False)

    print("\n" + "=" * 118)
    print("7. THE ONE MULTI-PANEL 4b BY-PRODUCT: EWALL + VOLTGT, priced against its MATCHED-GROSS")
    print("   ladder point (idea 351's numeraire).  A de-grossing overlay must beat it to exist.")
    print("=" * 118)
    out = []
    for pan in ["U56", "B136", "SMALL439"]:
        px = P[pan]; start = px.index[WARMUP]
        wE = weights_for(px, pan, "EWALL")
        lad = df[(df.panel == pan) & (df.form == "EWALL") & (df.overlay.str.startswith("GROSS")) & (df.bps == 0)]
        xs = np.array([float(o.split("_g")[1]) for o in lad.overlay]); ys = lad.gross.values
        o = np.argsort(ys); xs, ys = xs[o], ys[o]
        for t in [0.10, 0.12, 0.15]:
            v = df[(df.panel == pan) & (df.form == "EWALL") & (df.overlay == f"VOLTGT_t{t:.2f}")]
            gt = float(v[v.bps == 0].gross.iloc[0])
            gm = float(np.interp(gt, ys, xs))
            b = backtest(px, ov_gross(wE, None, gm), cost_bps=0, freq=FREQ)
            for k in COSTS:
                rn = b["returns"].loc[start:] - b["turnover"].loc[start:] * k / 1e4
                st = stats(rn); st["gross"] = float(b["weights"].loc[start:].sum(axis=1).mean())
                spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
                p4b, f4b = bars_4b(rn, spy)
                vv = v[v.bps == k].iloc[0]
                out.append(dict(panel=pan, t=t, bps=k, ov_Sharpe=vv.Sharpe, ov_CAGR=vv.CAGR,
                                ov_MaxDD=vv.MaxDD, ov_OOS=vv.OOS, ov_4b=vv.pass4b, ov_gross=vv.gross,
                                ov_turn=vv.turn, lad_g=gm, lad_gross=st["gross"],
                                lad_Sharpe=st["Sharpe"], lad_CAGR=st["CAGR"], lad_MaxDD=st["MaxDD"],
                                lad_OOS=st["OOS"], lad_4b=p4b, gross_resid=abs(st["gross"] - gt),
                                dSharpe=vv.Sharpe - st["Sharpe"], dOOS=vv.OOS - st["OOS"],
                                dDD_pp=100 * (abs(st["MaxDD"]) - abs(vv.MaxDD))))
    b = pd.DataFrame(out)
    print(b.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"\n  vol target beats its matched-gross ladder point on Sharpe in {(b.dSharpe > 0).sum()}/{len(b)},"
          f" on OOS Sharpe in {(b.dOOS > 0).sum()}/{len(b)}, on MaxDD in {(b.dDD_pp > 0).sum()}/{len(b)};"
          f" gross-match residual max {b.gross_resid.max():.2e}")
    print(f"  4b: overlay {int(b.ov_4b.sum())}/{len(b)} vs matched ladder point {int(b.lad_4b.sum())}/{len(b)}")
    b.to_csv(f"{OUT}.numeraire.csv", index=False)


def main():
    print("=" * 118)
    print("IDEA 374 - does the SECOND-worst drawdown episode bound every overlay?")
    print("  headroom H = |D1| - |D2| (pp) from the base book's equity curve; 0 tuned parameters")
    print("=" * 118)
    P = panels()
    gates(P)
    frames, spys = [], []
    for name, px in P.items():
        d, s = sweep(px, name)
        frames.append(d); spys.append(s)
    df = pd.concat(frames, ignore_index=True)
    spy = pd.concat(spys, ignore_index=True)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    analyse(df, spy)
    byproduct(P, df)
    print(f"\nwrote {OUT}.grid.csv ({len(df)} rows), .classmax.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
