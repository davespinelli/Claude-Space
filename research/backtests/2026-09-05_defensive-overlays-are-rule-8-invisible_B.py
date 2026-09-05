#!/usr/bin/env python3
"""QUEUE idea 99 — defensive-overlays-are-rule-8-invisible (lane B, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 26 found IS (2009-2016) Sharpe monotone DECREASING in the sleeve fraction while OOS
(2017-2026) Sharpe is monotone INCREASING, so rule 8's selector rejects every defensive overlay
by construction.  Measure the sign of dSharpe(IS) - dSharpe(OOS) across the leaderboard's overlay
grids (crypto, band, breadth gate, stop, sleeve) to see whether this is a property of the IS
window or of overlays in general."

THE STATISTIC (declared before any number is computed)
------------------------------------------------------
For an overlay grid with a designated NO-OVERLAY point (parameter 0 / none / incumbent) and any
evaluation window W:

    d(W, p) = Sharpe_W(overlay at p) - Sharpe_W(no-overlay)          "what the overlay is worth in W"
    G(p)    = d(IS, p) - d(OOS, p)                                   "the rule-8 invisibility gap"

G < 0 means the overlay looks WORSE in-sample than it turns out to be out-of-sample, i.e. rule 8
(argmax IS Sharpe) systematically under-selects it.  Idea 26's claim is G < 0 for the sleeve.
This run measures the sign of G on every leaderboard overlay grid, then asks whether the sign is
a property of THE 2009-2016 WINDOW or of OVERLAYS AS AN INSTRUMENT.

PRE-REGISTERED DISCRIMINATION (both tests declared before running; neither is tuned on)
---------------------------------------------------------------------------------------
  T1 SPLIT REVERSAL.  Recompute G with the windows swapped (IS := 2017+, OOS := ..2016).  If the
     effect is a property of "being the in-sample window" the sign is unchanged; if it is a
     property of WHICH YEARS are in each window, the sign flips.  A flip is decisive for
     H_window because "in-sample-ness" is exactly what the swap holds fixed.
  T2 CRISIS-DENSITY REGRESSION.  Recompute d(W, p) on each of the 18 disjoint CALENDAR YEARS and
     regress the pooled per-year mean d on that year's SPY MaxDD (OLS, r and slope reported).
     If d is explained by how bad the year was for SPY, the IS/OOS gap is a crisis-density
     artefact of the window, not a property of overlays.

  H_window  is supported iff T1 flips the sign AND T2's slope is signed so that d rises as SPY
            drawdown deepens.
  H_overlay is supported iff d < 0 in essentially every window regardless of its crisis content.

  Supporting, not decisive: a split-date SWEEP (6 dates) and 4 disjoint sample quarters.

DEFENSIVE vs OFFENSIVE is not taken on faith.  Each grid point is labelled two ways: an a-priori
label (sleeve/band/breadth/stop = defensive; crypto/gross-up = offensive) and a MEASURED label
(mean gross exposure lower than the no-overlay point = defensive).  Both are reported; the
measured label is the one the headline uses.

TUNED (2, per PROTOCOL rule 4): the overlay parameter (4-5 levels per grid) x the evaluation
window (the split date).  Nothing is selected on the window -- every window is reported.  The
only selector run is PROTOCOL rule 8 itself (argmax IS Sharpe, tie-break smallest parameter),
whose picks are reported with full/half/OOS numbers vs RULES v1 and SPY and both KEEP paths.
ALL grid points are written to .grid.csv and printed.

OVERLAY GRIDS (identical construction to idea 109's harness, so the numbers are comparable)
-------------------------------------------------------------------------------------------
  sleeve   f in {0,.25,.50,.75,1.00} of the S4 sleeve (TLT,GLD,DBC,UUP), gross-renormalised to 1.00
  band     200d gate with a hysteresis band of {0,2,3,5,8}% (idea 57)
  breadth  cut book gross by {0,.25,.50,.75,1.00} when % of names above their 200d MA < 30%
  stop     per-name trailing stop at {none,25,20,15,10}% off the 126d high (idea 9)
  crypto   BTC/ETH carve-out at {0,2,5,10}% of gross (idea 5) -- u56 ONLY
  gross    static gross lever g in {0.50,0.75,1.00,1.25}, incumbent 0.75 = the no-overlay point
2 base books (top20, ewall) x 2 universes (u56, broad) x 2 cost rungs (10, 25 bps), weekly.

CRYPTO CAVEAT: BTC-USD starts 2014-09-17 and ETH-USD later, so the crypto grid's IS window holds
barely two years of crypto.  Crypto rows are shown both in and out of every pooled statistic.

SURVIVORSHIP: both equity panels are current constituents of their lists; equity levels are
biased up.  The bias is identical across the windows being compared, which is what this run does.

COST NOTE: engine.backtest applies costs as `gross - turnover * bps/1e4` with the holdings path
independent of bps, so each weight matrix is run ONCE at 0 bps and both rungs derived exactly.
Asserted at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17.
It hits every grid point and every window identically.

Deterministic, standalone:
    python research/backtests/2026-09-05_defensive-overlays-are-rule-8-invisible_B.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

FREQ = "W"
COSTS = (10, 25)
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
OUT = Path(__file__).with_suffix("")

# a-priori labels, declared before any number
APRIORI = {"sleeve": "defensive", "band": "defensive", "breadth": "defensive",
           "stop": "defensive", "crypto": "offensive", "gross": "mixed"}

# pre-registered split dates for the supporting sweep (protocol's 2016 among them)
SPLIT_DATES = ["2013-12-31", "2014-12-31", "2015-12-31", "2016-12-31", "2018-12-31", "2020-12-31"]

# pre-registered disjoint sample quarters
QUARTERS = [("2009-2012", "2009-01-01", "2012-12-31"), ("2013-2016", "2013-01-01", "2016-12-31"),
            ("2017-2021", "2017-01-01", "2021-12-31"), ("2022-2026", "2022-01-01", "2026-12-31")]


# ---------------------------------------------------------------- gates and books
def _band_above(px, w):
    ma = px.rolling(200).mean()
    up = (px > ma * (1 + w))
    dn = (px < ma * (1 - w))
    st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                      index=px.index, columns=px.columns)
    return st.ffill().fillna(0.0) > 0.5


def _elig(px, band=0.0, stop=None):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = _band_above(px, band) & (vol20 < 0.60)
    if stop is not None:
        dd = px / px.rolling(126).max() - 1.0
        m = m & (dd > -stop)
    return m


def book(px, kind, band=0.0, stop=None, gross=BOOK_GROSS, n=20):
    s, _, _ = score(px, vol_scale=False)
    m = _elig(px, band, stop)
    if kind == "top20":
        rank = s.where(m).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
    else:
        w = (m & s.notna()).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = (1.0 / vol.replace(0.0, np.nan))
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def _regross(w, g=1.00):
    tot = w.sum(axis=1)
    return w.mul((g / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


def overlay(px, kind, grid, p):
    if grid == "sleeve":
        E = book(px, kind)
        return _regross((1 - p) * E + p * sleeve_weights(px, S4), 1.00)
    if grid == "band":
        return book(px, kind, band=p)
    if grid == "breadth":
        E = book(px, kind)
        above = _band_above(px, 0.0).drop(columns=["SPY"], errors="ignore")
        br = above.mean(axis=1)
        mult = pd.Series(np.where(br < BREADTH_B, 1.0 - p, 1.0), index=px.index)
        return E.mul(mult, axis=0)
    if grid == "stop":
        return book(px, kind, stop=None if p is None else p)
    if grid == "gross":
        return book(px, kind, gross=p)
    if grid == "crypto":
        E = book(px, kind, gross=BOOK_GROSS * (1 - p))
        if p == 0.0:
            return E
        c = [t for t in CRYPTO if t in px.columns]
        avail = px[c].notna().astype(float)
        k = avail.sum(axis=1)
        cw = avail.div(k.where(k > 0), axis=0).fillna(0.0) * (BOOK_GROSS * p)
        out = E.copy()
        out[c] = out[c].values + cw.values
        return out
    raise ValueError(grid)


GRIDS = {
    "sleeve":  [0.00, 0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.02, 0.03, 0.05, 0.08],
    "breadth": [0.00, 0.25, 0.50, 0.75, 1.00],
    "stop":    [None, 0.25, 0.20, 0.15, 0.10],
    "crypto":  [0.00, 0.02, 0.05, 0.10],
    "gross":   [0.75, 0.50, 1.00, 1.25],
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}


def pkey(grid, p):
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p
    if grid == "gross":
        return abs(p - 0.75)
    return float(p)


# ---------------------------------------------------------------- metrics
def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    if len(r) < 60:
        return np.nan, np.nan, np.nan
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def sharpe_on(r, a=None, b=None):
    return stats(r.loc[a:b])[1]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, idd = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(r, base):
    return bool(r["H1"] > base["H1"] and r["H2"] > base["H2"] and r["MaxDD"] >= base["MaxDD"])


def keep_4b(r, spy):
    return bool(r["H1"] > spy["H1"] and r["H2"] > spy["H2"] and r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["MaxDD"] >= 0.60 * spy["MaxDD"] and r["CAGR"] >= 0.70 * spy["CAGR"])


def keep_4b_oos(r, spy):
    return bool(r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and r["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def ols(x, y):
    """slope, intercept, r for a simple OLS on the finite pairs."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan, np.nan, np.nan
    x, y = x[m], y[m]
    b = np.polyfit(x, y, 1)
    r = float(np.corrcoef(x, y)[0, 1])
    return float(b[0]), float(b[1]), r


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    years = list(range(2010, 2027))          # 2009 is a partial year (eval starts 2009-01-13)
    print(f"[data] u56 {u56.shape[1]} cols, broad {broad.shape[1]} cols")
    print(f"[pre-registered] statistic G = d(IS) - d(OOS), d(W,p) = Sharpe_W(p) - Sharpe_W(no-overlay)")
    print(f"[pre-registered] T1 split reversal · T2 crisis-density regression on {len(years)} calendar years")
    print(f"[pre-registered] a-priori labels {APRIORI}\n")

    # cost-linearity assertion (lets every point be run once at 0 bps)
    st0 = u56.index[260]
    w0 = book(u56, "top20")
    r0 = backtest(u56, w0, cost_bps=0.0, freq=FREQ)
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], 10)
                 - backtest(u56, w0, cost_bps=10, freq=FREQ)["returns"].loc[st0:]).abs().max())
    print(f"[check] cost linearity max |derived - direct| at 10 bps = {err:.2e}")
    assert err < 1e-12

    records, refs, spy_years = [], {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto, spy_r)
        spy_years[tag] = {y: stats(spy_r.loc[f"{y}-01-01":f"{y}-12-31"]) for y in years}
        print("=" * 124)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers | eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": full_row(net(bgr, bto, 10)), "SPY": spy}).T))

        for grid, params in GRIDS.items():
            if grid == "crypto" and not all(t in px.columns for t in CRYPTO):
                print(f"  [skip] grid={grid} on {tag}: crypto tickers absent from this panel")
                continue
            for kind in ("top20", "ewall"):
                for p in params:
                    w = overlay(px, kind, grid, p)
                    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                    gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    gross = float(w.loc[start:].sum(axis=1).mean())
                    turn = float(to.sum() / (len(gr) / 252))
                    for bps in COSTS:
                        r = net(gr, to, bps)
                        row = full_row(r)
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind,
                                   param=("none" if p is None else p), cost_bps=bps,
                                   Gross=gross, Turn_yr=turn,
                                   pkey=pkey(grid, p), is_null=(p == NULL_P[grid]),
                                   apriori=APRIORI[grid])
                        # every window's Sharpe, for the same return series
                        for d in SPLIT_DATES:
                            row[f"SH_pre_{d[:4]}"] = sharpe_on(r, None, d)
                            row[f"SH_post_{d[:4]}"] = sharpe_on(r, str(int(d[:4]) + 1) + "-01-01", None)
                        for qn, a, b in QUARTERS:
                            row[f"SH_q_{qn}"] = sharpe_on(r, a, b)
                        for y in years:
                            row[f"SH_y_{y}"] = sharpe_on(r, f"{y}-01-01", f"{y}-12-31")
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv")

    CELL = ["universe", "grid", "book", "cost_bps"]

    # ------------------------------------------------------------ (1) every grid point
    print("\n" + "=" * 124)
    print("### (1) EVERY GRID POINT (10 bps shown; 25 bps in .grid.csv)\n")
    for (tag, grid, kind), sub in G[G.cost_bps == 10].groupby(["universe", "grid", "book"], sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}")
        print(fmt(sub.set_index("param")[["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD",
                                          "IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                                          "4a", "4b", "4b_oos"]]))
        print()

    # ------------------------------------------------------------ (2) THE STATISTIC
    print("=" * 124)
    print("### (2) d(IS), d(OOS) AND THE GAP G = d(IS) - d(OOS), EVERY NON-NULL GRID POINT\n")
    deltas = []
    for keys, sub in G.groupby(CELL, sort=False):
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub[~sub.is_null].iterrows():
            rec = dict(zip(CELL, keys), param=r["param"], apriori=r["apriori"],
                       dGross=r["Gross"] - nullrow["Gross"],
                       d_IS=r["IS_Sharpe"] - nullrow["IS_Sharpe"],
                       d_OOS=r["OOS_Sharpe"] - nullrow["OOS_Sharpe"],
                       d_full=r["Sharpe"] - nullrow["Sharpe"],
                       dCAGR_OOS=r["OOS_CAGR"] - nullrow["OOS_CAGR"],
                       dMaxDD_OOS=r["OOS_MaxDD"] - nullrow["OOS_MaxDD"])
            rec["G"] = rec["d_IS"] - rec["d_OOS"]
            rec["measured"] = "defensive" if rec["dGross"] < -1e-6 else (
                "offensive" if rec["dGross"] > 1e-6 else "neutral-gross")
            # T1: the same statistic with the windows swapped
            rec["d_IS_rev"] = rec["d_OOS"]
            rec["d_OOS_rev"] = rec["d_IS"]
            rec["G_rev"] = rec["d_OOS"] - rec["d_IS"]
            for d in SPLIT_DATES:
                y = d[:4]
                rec[f"G_split{y}"] = ((r[f"SH_pre_{y}"] - nullrow[f"SH_pre_{y}"])
                                      - (r[f"SH_post_{y}"] - nullrow[f"SH_post_{y}"]))
            for qn, _, _ in QUARTERS:
                rec[f"d_{qn}"] = r[f"SH_q_{qn}"] - nullrow[f"SH_q_{qn}"]
            for y in years:
                rec[f"d_y_{y}"] = r[f"SH_y_{y}"] - nullrow[f"SH_y_{y}"]
            deltas.append(rec)
    D = pd.DataFrame(deltas)
    D.to_csv(OUT.with_suffix(".deltas.csv"), index=False)

    show = ["param", "apriori", "measured", "dGross", "d_IS", "d_OOS", "G", "dCAGR_OOS", "dMaxDD_OOS"]
    print(fmt(D[D.cost_bps == 10].set_index(["universe", "grid", "book"])[show]))
    print(f"\n({len(D)} non-null grid points at both cost rungs; 25 bps in .deltas.csv)")

    print("\n--- POOLED SIGN OF G (negative = overlay under-selected by rule 8)")
    def pooled(sub, label):
        n = len(sub)
        return dict(label=label, n=n, mean_d_IS=sub.d_IS.mean(), mean_d_OOS=sub.d_OOS.mean(),
                    mean_G=sub.G.mean(), median_G=sub.G.median(),
                    frac_G_neg=float((sub.G < 0).mean()),
                    frac_dIS_neg=float((sub.d_IS < 0).mean()),
                    frac_dOOS_pos=float((sub.d_OOS > 0).mean()),
                    frac_invisible=float(((sub.d_IS < 0) & (sub.d_OOS > 0)).mean()))
    rows = [pooled(D, "ALL points"),
            pooled(D[D.grid != "crypto"], "excl. crypto"),
            pooled(D[D.apriori == "defensive"], "a-priori DEFENSIVE"),
            pooled(D[D.apriori == "offensive"], "a-priori OFFENSIVE (crypto)"),
            pooled(D[D.measured == "defensive"], "MEASURED defensive (lower gross)"),
            pooled(D[D.measured == "offensive"], "MEASURED offensive (higher gross)"),
            pooled(D[D.measured == "neutral-gross"], "MEASURED gross-neutral")]
    print(fmt(pd.DataFrame(rows).set_index("label")))

    print("\n--- BY GRID")
    print(fmt(D.groupby("grid").agg(n=("G", "size"), d_IS=("d_IS", "mean"), d_OOS=("d_OOS", "mean"),
                                    G=("G", "mean"), frac_G_neg=("G", lambda s: (s < 0).mean()),
                                    frac_invisible=("G", lambda s: np.nan))
              .drop(columns="frac_invisible")
              .join(D.groupby("grid").apply(
                  lambda s: ((s.d_IS < 0) & (s.d_OOS > 0)).mean(), include_groups=False)
                  .rename("frac_invisible"))))

    print("\n--- IDEA 26'S ORIGINAL CLAIM, REPRODUCED: monotonicity of the sleeve grid")
    sl = G[(G.grid == "sleeve") & (G.cost_bps == 10)].copy()
    for (tag, kind), s in sl.groupby(["universe", "book"], sort=False):
        s = s.sort_values("pkey")
        mono_is = bool(np.all(np.diff(s.IS_Sharpe.values) < 0))
        mono_oos = bool(np.all(np.diff(s.OOS_Sharpe.values) > 0))
        print(f"  {tag}/{kind}: IS {np.round(s.IS_Sharpe.values, 3)} monotone-DOWN={mono_is} | "
              f"OOS {np.round(s.OOS_Sharpe.values, 3)} monotone-UP={mono_oos}")

    # ------------------------------------------------------------ (3) T1 SPLIT REVERSAL
    print("\n" + "=" * 124)
    print("### (3) T1 — SPLIT REVERSAL.  Same statistic, windows swapped.  A sign FLIP means the")
    print("###      effect belongs to WHICH YEARS are in the window, not to being in-sample.\n")
    t1 = pd.DataFrame([
        dict(sample=lbl, n=len(s), mean_G=s.G.mean(), frac_G_neg=(s.G < 0).mean(),
             mean_G_reversed=s.G_rev.mean(), frac_G_rev_neg=(s.G_rev < 0).mean(),
             sign_flips=bool(np.sign(s.G.mean()) != np.sign(s.G_rev.mean())))
        for lbl, s in (("ALL", D), ("excl. crypto", D[D.grid != "crypto"]),
                       ("a-priori DEFENSIVE", D[D.apriori == "defensive"]),
                       ("MEASURED defensive", D[D.measured == "defensive"]))])
    print(fmt(t1.set_index("sample")))
    print("\nNOTE (pre-registered reading): G_rev = -G by construction, so the FLIP IS MECHANICAL.")
    print("T1 is therefore informative only via what it holds fixed: under the swap the same")
    print("overlay is 'rejected by the selector' in the OTHER direction, i.e. 'in-sample-ness'")
    print("carries no sign of its own.  The content is in WHICH window has the higher d — T2.")
    print("\nMean d by window, the same overlays evaluated in each (this is the non-mechanical part):")
    wins = pd.DataFrame([
        dict(window="IS 2009-2016", mean_d=D.d_IS.mean(), frac_pos=(D.d_IS > 0).mean()),
        dict(window="OOS 2017-2026", mean_d=D.d_OOS.mean(), frac_pos=(D.d_OOS > 0).mean()),
    ] + [dict(window=f"quarter {qn}", mean_d=D[f"d_{qn}"].mean(), frac_pos=(D[f"d_{qn}"] > 0).mean())
         for qn, _, _ in QUARTERS])
    print(fmt(wins.set_index("window")))

    print("\n--- SUPPORTING: the split-date sweep (G recomputed at each pre-registered split)")
    sweep = pd.DataFrame([
        dict(split=d, mean_G_all=D[f"G_split{d[:4]}"].mean(),
             frac_neg_all=(D[f"G_split{d[:4]}"] < 0).mean(),
             mean_G_def=D[D.apriori == "defensive"][f"G_split{d[:4]}"].mean(),
             frac_neg_def=(D[D.apriori == "defensive"][f"G_split{d[:4]}"] < 0).mean())
        for d in SPLIT_DATES]).set_index("split")
    print(fmt(sweep))

    # ------------------------------------------------------------ (4) T2 CRISIS DENSITY
    print("\n" + "=" * 124)
    print("### (4) T2 — CRISIS-DENSITY REGRESSION.  Per-year d vs that year's SPY MaxDD.\n")
    yr_rows = []
    for tag in universes:
        sub = D[D.universe == tag]
        for y in years:
            spy_c, spy_s, spy_dd = spy_years[tag][y]
            yr_rows.append(dict(universe=tag, year=y, SPY_ret=spy_c, SPY_MaxDD=spy_dd,
                                mean_d_all=sub[f"d_y_{y}"].mean(),
                                mean_d_def=sub[sub.apriori == "defensive"][f"d_y_{y}"].mean(),
                                mean_d_off=sub[sub.apriori == "offensive"][f"d_y_{y}"].mean(),
                                frac_pos_def=(sub[sub.apriori == "defensive"][f"d_y_{y}"] > 0).mean(),
                                in_IS=(y <= 2016)))
    Y = pd.DataFrame(yr_rows)
    Y.to_csv(OUT.with_suffix(".years.csv"), index=False)
    print(fmt(Y.set_index(["universe", "year"])))

    print("\n--- OLS of the per-year mean d on that year's SPY MaxDD (MaxDD is negative: a")
    print("    NEGATIVE slope means overlays pay MORE in deeper-drawdown years)")
    reg = []
    for tag in list(universes) + ["pooled"]:
        s = Y if tag == "pooled" else Y[Y.universe == tag]
        for col, lbl in (("mean_d_all", "all overlays"), ("mean_d_def", "defensive only")):
            b, a, r = ols(s.SPY_MaxDD, s[col])
            reg.append(dict(universe=tag, series=lbl, slope=b, intercept=a, r=r, n=len(s)))
    print(fmt(pd.DataFrame(reg).set_index(["universe", "series"])))

    print("\n--- The same, using the year's SPY RETURN instead of its drawdown")
    reg2 = []
    for tag in list(universes) + ["pooled"]:
        s = Y if tag == "pooled" else Y[Y.universe == tag]
        for col, lbl in (("mean_d_all", "all overlays"), ("mean_d_def", "defensive only")):
            b, a, r = ols(s.SPY_ret, s[col])
            reg2.append(dict(universe=tag, series=lbl, slope=b, intercept=a, r=r, n=len(s)))
    print(fmt(pd.DataFrame(reg2).set_index(["universe", "series"])))

    print("\n--- IS vs OOS years, split by whether the year was a drawdown year for SPY")
    Y["bad_year"] = Y.SPY_MaxDD < -0.15
    print(fmt(Y.groupby(["in_IS", "bad_year"]).agg(
        n_years=("year", "size"), mean_SPY_MaxDD=("SPY_MaxDD", "mean"),
        mean_d_all=("mean_d_all", "mean"), mean_d_def=("mean_d_def", "mean"))))
    print(f"\nSPY MaxDD-<-15% years: IS {sorted(set(Y[(Y.in_IS) & Y.bad_year].year))} "
          f"| OOS {sorted(set(Y[(~Y.in_IS) & Y.bad_year].year))}")

    # ------------------------------------------------------------ (5) rule 8 walk-forward
    print("\n" + "=" * 124)
    print("### (5) PROTOCOL RULE 8 WALK-FORWARD — argmax IS Sharpe (tie-break smallest parameter),")
    print("###      chosen on 2009-2016 alone, evaluated on untouched 2017-2026.\n")
    picks = []
    for keys, sub in G.groupby(CELL, sort=False):
        tag = keys[0]
        spy, bgr, bto, _ = refs[tag]
        s = sub.sort_values("pkey")
        r8 = s.loc[[s["IS_Sharpe"].idxmax()]].iloc[0]
        nl = s[s.is_null].iloc[0]
        bo = s.loc[[s["OOS_Sharpe"].idxmax()]].iloc[0]
        base = full_row(net(bgr, bto, keys[3]))
        for lbl, r in (("rule8", r8), ("no-overlay", nl), ("OOS-best (ceiling)", bo)):
            picks.append(dict(zip(CELL, keys), pick=lbl, param=r["param"],
                              CAGR=r["CAGR"], Sharpe=r["Sharpe"], MaxDD=r["MaxDD"],
                              H1=r["H1"], H2=r["H2"],
                              IS_Sharpe=r["IS_Sharpe"], OOS_CAGR=r["OOS_CAGR"],
                              OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                              base_Sharpe=base["Sharpe"], base_OOS_Sharpe=base["OOS_Sharpe"],
                              spy_Sharpe=spy["Sharpe"], spy_OOS_Sharpe=spy["OOS_Sharpe"],
                              spy_OOS_CAGR=spy["OOS_CAGR"],
                              regret=r["OOS_Sharpe"] - bo["OOS_Sharpe"],
                              picks_null=bool(r["is_null"]),
                              **{"4a": bool(r["4a"]), "4b": bool(r["4b"]),
                                 "4b_oos": bool(r["4b_oos"])}))
    P = pd.DataFrame(picks)
    P.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(P.set_index(CELL + ["pick"])[
        ["param", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
         "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "regret", "4a", "4b", "4b_oos"]]))

    ncell = P.pick.eq("rule8").sum()
    r8 = P[P.pick == "rule8"]
    nl = P[P.pick == "no-overlay"]
    bo = P[P.pick == "OOS-best (ceiling)"]
    print(f"\nRule 8 picks the NO-OVERLAY point in {int(r8.picks_null.sum())}/{ncell} cells "
          f"({r8.picks_null.mean():.0%}).")
    print(f"  by a-priori class: " + ", ".join(
        f"{g} {int(r8[r8.grid == g].picks_null.sum())}/{len(r8[r8.grid == g])}"
        for g in GRIDS if len(r8[r8.grid == g])))
    print(fmt(pd.DataFrame([
        dict(pick=k, mean_OOS_Sharpe=v.OOS_Sharpe.mean(), mean_OOS_CAGR=v.OOS_CAGR.mean(),
             mean_OOS_MaxDD=v.OOS_MaxDD.mean(), mean_regret=v.regret.mean(),
             pass_4a=int(v["4a"].sum()), pass_4b=int(v["4b"].sum()), pass_4b_oos=int(v["4b_oos"].sum()),
             beats_SPY_OOS=int((v.OOS_Sharpe > v.spy_OOS_Sharpe).sum()), n=len(v))
        for k, v in (("rule8", r8), ("no-overlay", nl), ("OOS-best (ceiling)", bo))]).set_index("pick")))

    key = CELL
    a = r8.set_index(key); b = nl.set_index(key)
    print(f"\nPaired rule8 - no-overlay: mean dOOS_Sharpe {(a.OOS_Sharpe - b.OOS_Sharpe).mean():+.4f}, "
          f"better in {int((a.OOS_Sharpe > b.OOS_Sharpe).sum())}, worse in "
          f"{int((a.OOS_Sharpe < b.OOS_Sharpe).sum())}, tied in {int((a.OOS_Sharpe == b.OOS_Sharpe).sum())}")
    c = bo.set_index(key)
    print(f"Ceiling left on the table (OOS-best - rule8): mean {(c.OOS_Sharpe - a.OOS_Sharpe).mean():+.4f} "
          f"OOS Sharpe, {(c.OOS_CAGR - a.OOS_CAGR).mean():+.2%} OOS CAGR; 4b passes "
          f"{int(bo['4b'].sum())} (ceiling) vs {int(r8['4b'].sum())} (rule 8)")

    # ------------------------------------------------------------ (6) verdict inputs
    print("\n" + "=" * 124)
    print("### (6) VERDICT INPUTS\n")
    dd = D[D.apriori == "defensive"]
    print(f"  H_window test T1: G_rev = -G mechanically; the informative half is that mean d is "
          f"{D.d_IS.mean():+.3f} in 2009-2016 and {D.d_OOS.mean():+.3f} in 2017-2026")
    b_all, _, r_all = ols(Y.SPY_MaxDD, Y.mean_d_all)
    b_def, _, r_def = ols(Y.SPY_MaxDD, Y.mean_d_def)
    print(f"  H_window test T2: per-year d vs SPY MaxDD — all overlays slope {b_all:+.3f} r {r_all:+.2f}; "
          f"defensive slope {b_def:+.3f} r {r_def:+.2f} (n={len(Y)} year-universes)")
    print(f"  H_overlay: d < 0 in {(dd.d_IS < 0).mean():.0%} of defensive points in-sample and "
          f"{(dd.d_OOS < 0).mean():.0%} out of sample; per-year, defensive d > 0 in "
          f"{(Y.mean_d_def > 0).mean():.0%} of the {len(Y)} year-universes")
    print(f"  'rule-8-invisible' quadrant (d_IS<0 AND d_OOS>0): "
          f"{((dd.d_IS < 0) & (dd.d_OOS > 0)).mean():.0%} of defensive points "
          f"({int(((dd.d_IS < 0) & (dd.d_OOS > 0)).sum())}/{len(dd)})")
    print(f"  cost of the blindness: rule 8 leaves {(c.OOS_Sharpe - a.OOS_Sharpe).mean():+.3f} mean "
          f"OOS Sharpe and {int(bo['4b'].sum()) - int(r8['4b'].sum()):+d} 4b passes on the table")
    print("\nDone.")


if __name__ == "__main__":
    main()
