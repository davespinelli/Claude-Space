#!/usr/bin/env python3
"""Idea 288 - "price-the-vol20-drawdown-purchase-against-the-cheaper-instruments".

The question
------------
Idea 56 killed `vol20 < 0.60` as a RETURN edge on research/universe.json and re-read it as a
DRAWDOWN instrument: at n=20, de-gross convention, it costs 1.94pp of CAGR and 0.065 of
Sharpe and buys 3.12pp of MaxDD.  That is a PRICE, and a price means nothing until it is put
beside the other things on the same shelf.  This run puts idea 74's axis (pp of CAGR
surrendered per pp of MaxDD bought) on the record's existing drawdown menu, all four
instruments applied to the SAME base book, and asks where vol20 ranks at MATCHED MaxDD
reduction - not at its own arbitrary threshold.

The base book B0 (idea 56's `NONE` cell, held fixed everywhere)
    scan.py's composite with NO vol scaler, NO eligibility gate, top 20 equal-weighted at
    GROSS/n = 0.75/20 of NAV each, weekly rebalancing, 10 bps per unit turnover, weights
    decided at close t applied at t+1.  Panels: universe.json (U56, where idea 56 measured
    the price) and universe_broad.json (B136, reported never selected on).  SPY is a
    benchmark column, never tradable (idea 56's convention verbatim).

The menu - four instruments, each a one-dial modification of B0
    VOL20(v)   eligibility `vol20 < v`, gated-out weight to CASH (de-gross).  Idea 56's own
               instrument; v = 0.60 is its published point.
    BAND(b)    eligibility = RULES v2 clause 2's 200d +/- b band with hysteresis, de-gross.
               b = 0.00 is the hard 200d gate; b = 0.03 is the live book's band.
    DEGROSS(m) every weight x m, remainder cash.  The null instrument: a pure exposure cut
               that contains no information at all.  Ideas 135/244 keep finding that other
               instruments ARE this one, so it is the comparand that matters.
    SLEEVE(f)  (1-f) x B0 + f x the S4 = {TLT,GLD,DBC,UUP} sleeve (idea 18 variant B:
               trend-vote x inverse-vol, re-grossed to 0.75), idea 129's census construction.
               The four sleeve assets stay in B0's own selectable set (stated, not fixed).

Tuned parameters (PROTOCOL rule 4: at most two)
    1. instrument in {VOL20, BAND, DEGROSS, SLEEVE}     2. that instrument's dial level
Every grid point of both is reported.  Panel and cost rung are NOT tuned: U56 is the panel
idea 56 measured on, B136 is printed beside it, and 10 bps is PROTOCOL's rung.

How the ranking is done
    For each grid point x:  dDD = MaxDD(x) - MaxDD(B0)  (pp of drawdown BOUGHT),
                            dCAGR = CAGR(B0) - CAGR(x)  (pp SURRENDERED),
                            price = dCAGR / dDD,  sprice = (Sharpe(B0) - Sharpe(x)) / dDD.
    Then each instrument's whole ladder is interpolated onto a common depth grid
    T in {1,2,3,4,5,6,8} pp of MaxDD reduction, so the four are compared at MATCHED purchase
    depth rather than at whatever their published dial happened to be.  Realised mean gross
    is carried through every row: an instrument that only pays by being a smaller book is a
    DEGROSS ladder point wearing a costume (ideas 135/244), and the matched-gross column is
    what says so.

Rule 8 walk-forward: choose (instrument, dial) on <= 2016 by cheapest IS price among points
whose IS dDD >= 3.0pp, then read 2017-2026 once.  Reported against B0 (do-nothing), the
pre-registered anchor VOL20(0.60), the best OOS point (regret), SPY and RULES v2.

Both KEEP paths (4a vs live RULES v2, 4b vs SPY) are evaluated on every grid point.

Outputs: .grid.csv, .matched.csv, .control.csv, .walkforward.csv, .console.txt.
The .result.md beside them is written by hand from those files, not by this script.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, band_state, rules_v1_weights, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa

OUT = Path(__file__).with_suffix("")
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 500)

COST, FREQ, GROSS, NBOOK = 10, "W", 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
S4 = ["TLT", "GLD", "DBC", "UUP"]
MOM_LAGS, VOL_WINDOW = (252, 126, 63), 60

# ------------------------------------------------------------------ the four ladders
VOL_LADDER    = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 1.00, 1.50]
BAND_LADDER   = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.30]
DEGROSS_LADDER= [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.60, 0.50, 0.40, 0.30]
SLEEVE_LADDER = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60]
DEPTHS = [1.0, 2.0, 3.0, 3.12, 4.0, 5.0, 6.0, 8.0]      # pp of MaxDD reduction, matched
ANCHOR = ("VOL20", 0.60)                                 # idea 56's published point
IS_MIN_DEPTH = 3.0                                       # rule-8 screen, pre-registered


# ------------------------------------------------------------------ books
def _tradable(px):
    return [c for c in px.columns if c != "SPY"]


def _base_sel(px):
    """B0's selection mask: top-20 of the un-gated composite, no vol scaler."""
    sub = px[_tradable(px)]
    s, _, _ = score(sub, vol_scale=False)
    return s, (s.rank(axis=1, ascending=False) <= NBOOK)


def _vol20(sub):
    return sub.pct_change().rolling(20).std() * np.sqrt(252)


def _sleeve_weights(px):
    """idea 18 variant B on S4, re-grossed to GROSS; zero elsewhere. (idea 102/129 verbatim)"""
    sub = px[S4]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    tot = w.sum(axis=1)
    w = GROSS * w.div(tot.where(tot > 1e-12), axis=0).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[S4] = w
    return out


def make_book(instrument, level):
    """Every instrument returns weights over px.columns (SPY column always 0)."""
    def f(px):
        sub = px[_tradable(px)]
        s, sel = _base_sel(px)
        if instrument == "BASE":
            w = sel.astype(float) * (GROSS / NBOOK)
        elif instrument == "VOL20":
            elig = s.where(_vol20(sub) < level)
            w = (elig.rank(axis=1, ascending=False) <= NBOOK).astype(float) * (GROSS / NBOOK)
        elif instrument == "BAND":
            elig = s.where(band_state(sub, level))
            w = (elig.rank(axis=1, ascending=False) <= NBOOK).astype(float) * (GROSS / NBOOK)
        elif instrument == "DEGROSS":
            w = sel.astype(float) * (GROSS / NBOOK) * level
        elif instrument == "SLEEVE":
            eq = sel.astype(float) * (GROSS / NBOOK)
            eq = eq.reindex(columns=px.columns).fillna(0.0)
            return ((1 - level) * eq + level * _sleeve_weights(px)).fillna(0.0)
        else:
            raise ValueError(instrument)
        return w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    return f


def v2_book(px):
    return rules_v2_weights(px[_tradable(px)]).reindex(columns=px.columns).fillna(0.0)


def v1_book(px):
    return rules_v1_weights(px[_tradable(px)]).reindex(columns=px.columns).fillna(0.0)


# ------------------------------------------------------------------ measurement
def stats(res, start):
    r = res["returns"].loc[start:]
    g = res["weights"].loc[start:].sum(axis=1)
    h = len(r) // 2
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"], IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                gross=g.mean(), turnover=res["turnover"].loc[start:].sum() / (len(r) / 252))


def spy_stats(px, start):
    r = px["SPY"].pct_change().fillna(0.0).loc[start:]
    h = len(r) // 2
    m, mo = metrics(r), metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                IS_CAGR=metrics(r.loc[:IS_END])["CAGR"], IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                gross=1.0, turnover=0.0)


def keep_paths(x, spy, v2):
    a = (x["H1"] > v2["H1"] and x["H2"] > v2["H2"] and x["MaxDD"] >= v2["MaxDD"])
    b = (x["H1"] > spy["H1"] and x["H2"] > spy["H2"] and x["OOS_Sharpe"] > spy["OOS_Sharpe"]
         and x["MaxDD"] >= 0.60 * spy["MaxDD"] and x["CAGR"] >= 0.70 * spy["CAGR"])
    return bool(a), bool(b)


def first_failing_4b(x, spy):
    for lbl, ok in (("H1", x["H1"] > spy["H1"]), ("H2", x["H2"] > spy["H2"]),
                    ("OOS", x["OOS_Sharpe"] > spy["OOS_Sharpe"]),
                    ("DD", x["MaxDD"] >= 0.60 * spy["MaxDD"]),
                    ("CAGR", x["CAGR"] >= 0.70 * spy["CAGR"])):
        if not ok:
            return lbl
    return "-"


def interp_at(sub, depth, col, dcol):
    """Linear interpolation of `col` at MaxDD-reduction `depth` along one instrument's ladder.
    Returns NaN when the ladder does not span the depth (reported as unreachable, never
    extrapolated)."""
    d = sub[[dcol, col]].dropna().sort_values(dcol)
    if len(d) < 2 or depth < d[dcol].iloc[0] or depth > d[dcol].iloc[-1]:
        return np.nan
    return float(np.interp(depth, d[dcol].values, d[col].values))


# ------------------------------------------------------------------ run one panel
def run_panel(tag, px):
    start = px.index[260]
    P(f"\n{'='*118}\nPANEL {tag}  ({px.shape[1]} columns, SPY held out of the book)  "
      f"sample {px.index[0].date()} -> {px.index[-1].date()}, measured from {start.date()}, "
      f"{COST} bps, {FREQ}, gross {GROSS}, n={NBOOK}\n{'='*118}")

    cells = [("BASE", np.nan)] \
        + [("VOL20", v) for v in VOL_LADDER] \
        + [("BAND", b) for b in BAND_LADDER] \
        + [("DEGROSS", m) for m in DEGROSS_LADDER] \
        + [("SLEEVE", f) for f in SLEEVE_LADDER]

    rows = []
    for inst, lvl in cells:
        r = backtest(px, make_book(inst, lvl)(px), cost_bps=COST, freq=FREQ)
        rows.append(dict(panel=tag, instrument=inst, level=lvl, **stats(r, start)))
    g = pd.DataFrame(rows)

    spy = spy_stats(px, start)
    v2 = stats(backtest(px, v2_book(px), cost_bps=COST, freq=FREQ), start)
    v1 = stats(backtest(px, v1_book(px), cost_bps=COST, freq=FREQ), start)
    b0 = g[g.instrument == "BASE"].iloc[0].to_dict()

    # ---- the exchange-rate columns (idea 74's axis)
    for pre, cs, dd in (("", "CAGR", "MaxDD"), ("IS_", "IS_CAGR", "IS_MaxDD"),
                        ("OOS_", "OOS_CAGR", "OOS_MaxDD")):
        g[pre + "dDD"] = (g[dd] - b0[dd]) * 100
        g[pre + "dCAGR"] = (b0[cs] - g[cs]) * 100
        g[pre + "price"] = g[pre + "dCAGR"] / g[pre + "dDD"].replace(0.0, np.nan)
    g["dSharpe"] = g["Sharpe"] - b0["Sharpe"]
    g["sprice"] = (b0["Sharpe"] - g["Sharpe"]) / g["dDD"].replace(0.0, np.nan)
    g["dgross"] = g["gross"] - b0["gross"]
    kp = [keep_paths(r, spy, v2) for _, r in g.iterrows()]
    g["keep4a"] = [a for a, _ in kp]
    g["keep4b"] = [b for _, b in kp]
    g["fail4b"] = [first_failing_4b(r, spy) for _, r in g.iterrows()]

    P("\nREFERENCE ROWS")
    ref = pd.DataFrame([dict(name="B0 (top20 EW, no gate)", **{k: b0[k] for k in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "turnover")}),
                        dict(name="RULES v2 (live)", **{k: v2[k] for k in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "turnover")}),
                        dict(name="RULES v1", **{k: v1[k] for k in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "turnover")}),
                        dict(name="SPY", **{k: spy[k] for k in
                             ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "turnover")})]).set_index("name")
    P(ref.to_string(float_format=lambda x: f"{x:.4f}"))

    P("\nFULL GRID - every point of every ladder (dDD>0 = drawdown BOUGHT, price = pp CAGR per pp DD)")
    show = ["instrument", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "gross", "turnover", "dDD", "dCAGR", "price", "dSharpe", "sprice",
            "keep4a", "keep4b", "fail4b"]
    P(g[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- matched-depth table
    P(f"\nMATCHED-DEPTH COMPARISON - each instrument interpolated onto a common MaxDD-reduction "
      f"grid\n(blank = the ladder does not reach that depth; NEVER extrapolated)")
    mrows = []
    b0row = g[g.instrument == "BASE"]
    for inst in ("VOL20", "BAND", "DEGROSS", "SLEEVE"):
        # every ladder's OWN null point is B0 (VOL20 v=inf, BAND off, DEGROSS m=1, SLEEVE f=0),
        # so it anchors the curve at dDD = 0 and no depth below the ladder's first rung is
        # extrapolated from nothing.
        sub = pd.concat([g[g.instrument == inst], b0row], ignore_index=True)
        for T in DEPTHS:
            row = dict(panel=tag, instrument=inst, depth_pp=T,
                       level=interp_at(sub, T, "level", "dDD"),
                       CAGR=interp_at(sub, T, "CAGR", "dDD"),
                       Sharpe=interp_at(sub, T, "Sharpe", "dDD"),
                       gross=interp_at(sub, T, "gross", "dDD"),
                       OOS_Sharpe=interp_at(sub, T, "OOS_Sharpe", "dDD"),
                       OOS_CAGR=interp_at(sub, T, "OOS_CAGR", "dDD"))
            row["dCAGR"] = (b0["CAGR"] - row["CAGR"]) * 100 if row["CAGR"] == row["CAGR"] else np.nan
            row["price"] = row["dCAGR"] / T if row["dCAGR"] == row["dCAGR"] else np.nan
            row["sprice"] = ((b0["Sharpe"] - row["Sharpe"]) / T) if row["Sharpe"] == row["Sharpe"] else np.nan
            mrows.append(row)
    m = pd.DataFrame(mrows)
    P(m.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\nRANK AT MATCHED DEPTH (1 = cheapest; ordered by pp of CAGR surrendered per pp of MaxDD)")
    piv = m.pivot(index="depth_pp", columns="instrument", values="price")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  rank by price (CAGR cost):")
    P(piv.rank(axis=1).to_string(float_format=lambda x: f"{x:.1f}"))
    pivs = m.pivot(index="depth_pp", columns="instrument", values="sprice")
    P("\n  Sharpe cost per pp of MaxDD (negative = the instrument RAISES Sharpe while cutting DD):")
    P(pivs.to_string(float_format=lambda x: f"{x:.4f}"))
    P("\n  rank by Sharpe cost:")
    P(pivs.rank(axis=1).to_string(float_format=lambda x: f"{x:.1f}"))

    P("\nMATCHED-GROSS CONTROL (ideas 135/244) - is the instrument anything DEGROSS does not buy?\n"
      "  at each depth, DEGROSS's own realised gross vs the instrument's, and the CAGR gap.")
    dg = m[m.instrument == "DEGROSS"].set_index("depth_pp")
    ctl = []
    for inst in ("VOL20", "BAND", "SLEEVE"):
        s2 = m[m.instrument == inst].set_index("depth_pp")
        for T in DEPTHS:
            if T in s2.index and T in dg.index and s2.loc[T, "CAGR"] == s2.loc[T, "CAGR"] \
               and dg.loc[T, "CAGR"] == dg.loc[T, "CAGR"]:
                ctl.append(dict(panel=tag, instrument=inst, depth_pp=T,
                                gross=s2.loc[T, "gross"], dg_gross=dg.loc[T, "gross"],
                                dCAGR_vs_dg=(s2.loc[T, "CAGR"] - dg.loc[T, "CAGR"]) * 100,
                                dSharpe_vs_dg=s2.loc[T, "Sharpe"] - dg.loc[T, "Sharpe"],
                                dOOS_Sharpe_vs_dg=s2.loc[T, "OOS_Sharpe"] - dg.loc[T, "OOS_Sharpe"]))
    c = pd.DataFrame(ctl)
    P(c.to_string(index=False, float_format=lambda x: f"{x:.4f}") if len(c) else "  (no overlapping depths)")

    # ---- rule 8
    P(f"\nRULE 8 WALK-FORWARD - (instrument, level) chosen on <= {IS_END} by cheapest IS price "
      f"among points with IS dDD >= {IS_MIN_DEPTH}pp; 2017-2026 read once")
    pool = g[(g.instrument != "BASE") & (g["IS_dDD"] >= IS_MIN_DEPTH)].copy()
    P(f"  eligible IS pool: {len(pool)} of {len(g) - 1} points  "
      f"({dict(pool.instrument.value_counts())})")
    if len(pool):
        P(pool[["instrument", "level", "IS_dDD", "IS_dCAGR", "IS_price", "IS_Sharpe",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].sort_values("IS_price")
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        pick = pool.sort_values("IS_price").iloc[0]
    else:
        pick = None
    anc = g[(g.instrument == ANCHOR[0]) & (g.level == ANCHOR[1])].iloc[0]
    bestoos = g[g.instrument != "BASE"].sort_values("OOS_Sharpe", ascending=False).iloc[0]
    wf = pd.DataFrame([
        dict(arm="IS pick", instrument=(pick["instrument"] if pick is not None else "-"),
             level=(pick["level"] if pick is not None else np.nan),
             OOS_CAGR=(pick["OOS_CAGR"] if pick is not None else np.nan),
             OOS_Sharpe=(pick["OOS_Sharpe"] if pick is not None else np.nan),
             OOS_MaxDD=(pick["OOS_MaxDD"] if pick is not None else np.nan)),
        dict(arm="anchor VOL20(0.60)", instrument=anc["instrument"], level=anc["level"],
             OOS_CAGR=anc["OOS_CAGR"], OOS_Sharpe=anc["OOS_Sharpe"], OOS_MaxDD=anc["OOS_MaxDD"]),
        dict(arm="do-nothing B0", instrument="BASE", level=np.nan, OOS_CAGR=b0["OOS_CAGR"],
             OOS_Sharpe=b0["OOS_Sharpe"], OOS_MaxDD=b0["OOS_MaxDD"]),
        dict(arm="best OOS point", instrument=bestoos["instrument"], level=bestoos["level"],
             OOS_CAGR=bestoos["OOS_CAGR"], OOS_Sharpe=bestoos["OOS_Sharpe"], OOS_MaxDD=bestoos["OOS_MaxDD"]),
        dict(arm="RULES v2 (live)", instrument="-", level=np.nan, OOS_CAGR=v2["OOS_CAGR"],
             OOS_Sharpe=v2["OOS_Sharpe"], OOS_MaxDD=v2["OOS_MaxDD"]),
        dict(arm="SPY", instrument="-", level=np.nan, OOS_CAGR=spy["OOS_CAGR"],
             OOS_Sharpe=spy["OOS_Sharpe"], OOS_MaxDD=spy["OOS_MaxDD"]),
    ])
    wf["panel"] = tag
    P(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if pick is not None:
        P(f"  edge vs do-nothing  {pick['OOS_Sharpe'] - b0['OOS_Sharpe']:+.4f} Sharpe, "
          f"{(pick['OOS_CAGR'] - b0['OOS_CAGR'])*100:+.2f} pp CAGR, "
          f"{(pick['OOS_MaxDD'] - b0['OOS_MaxDD'])*100:+.2f} pp MaxDD")
        P(f"  edge vs anchor      {pick['OOS_Sharpe'] - anc['OOS_Sharpe']:+.4f} Sharpe;  "
          f"regret vs best OOS {pick['OOS_Sharpe'] - bestoos['OOS_Sharpe']:+.4f}")
        P(f"  IS->OOS price drift: IS {pick['IS_price']:.4f} -> OOS "
          f"{pick['OOS_price']:.4f} pp/pp   (IS depth {pick['IS_dDD']:.2f}pp -> OOS "
          f"{pick['OOS_dDD']:.2f}pp)")

    P(f"\nKEEP PATHS over all {len(g)} grid points on {tag}:  "
      f"4a {int(g.keep4a.sum())}/{len(g)}   4b {int(g.keep4b.sum())}/{len(g)}")
    P("  first-failing 4b bar over the failures: " +
      str(dict(g.loc[~g.keep4b, "fail4b"].value_counts())))
    if g.keep4b.any():
        P(g.loc[g.keep4b, ["instrument", "level", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                           "OOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    return g, m, c, wf, dict(b0=b0, spy=spy, v2=v2, v1=v1,
                             pick=(None if pick is None else pick.to_dict()),
                             anchor=anc.to_dict(), best=bestoos.to_dict())


# ------------------------------------------------------------------ main
def main():
    P(__doc__)
    G, M, C, W, S = [], [], [], [], {}
    for tag, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        g, m, c, w, s = run_panel(tag, px)
        G.append(g); M.append(m); C.append(c); W.append(w); S[tag] = s

    grid = pd.concat(G, ignore_index=True)
    matched = pd.concat(M, ignore_index=True)
    ctl = pd.concat([x for x in C if len(x)], ignore_index=True) if any(len(x) for x in C) else pd.DataFrame()
    wfa = pd.concat(W, ignore_index=True)
    grid.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    matched.to_csv(OUT.with_suffix(".matched.csv"), index=False)
    if len(ctl): ctl.to_csv(OUT.with_suffix(".control.csv"), index=False)
    wfa.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)

    # ---- the headline: reproduce idea 56's published price, then rank it
    P(f"\n{'='*118}\nHEADLINE\n{'='*118}")
    for tag in ("U56", "B136"):
        sub = grid[(grid.panel == tag) & (grid.instrument == "VOL20") & (grid.level == 0.60)].iloc[0]
        P(f"{tag}  VOL20(0.60) vs B0:  dCAGR {sub['dCAGR']:+.2f}pp  dSharpe {sub['dSharpe']:+.4f}  "
          f"dDD {sub['dDD']:+.2f}pp   price {sub['price']:.4f} pp/pp   sprice {sub['sprice']:.4f}/pp"
          f"   (idea 56 published 1.94pp / 0.065 / 3.12pp on U56)")

    P("\nWHERE VOL20 RANKS (pp of CAGR per pp of MaxDD, lower = cheaper; rank of 4 at each depth)")
    for tag in ("U56", "B136"):
        piv = matched[matched.panel == tag].pivot(index="depth_pp", columns="instrument", values="price")
        rk = piv.rank(axis=1)
        for T in DEPTHS:
            if T in rk.index and rk.loc[T].notna().any():
                order = piv.loc[T].dropna().sort_values()
                vr = rk.loc[T].get("VOL20", np.nan)
                tail = (f"   [VOL20 rank {int(vr)} of {int(rk.loc[T].notna().sum())}]"
                        if vr == vr else "   [VOL20 does not reach this depth]")
                P(f"  {tag} depth {T:>4.2f}pp:  " +
                  "  <  ".join(f"{k} {v:.3f}" for k, v in order.items()) + tail)

    P(f"\n4b passes overall: {int(grid.keep4b.sum())}/{len(grid)};  "
      f"4a passes overall: {int(grid.keep4a.sum())}/{len(grid)}")

    OUT.with_suffix(".console.txt").write_text("\n".join(LOG))
    print(f"\nwrote {OUT.name}.grid.csv / .matched.csv / .control.csv / .walkforward.csv / .console.txt")


if __name__ == "__main__":
    main()
