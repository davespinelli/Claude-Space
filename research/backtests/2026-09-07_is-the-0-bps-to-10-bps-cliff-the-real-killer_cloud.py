#!/usr/bin/env python3
"""Idea 352 (cloud, 2026-09-07): is-the-0-bps-to-10-bps-cliff-the-real-killer-of-the-idea-40-family.

QUEUE TEXT: "idea 41's grid clears 4b 8/36 at 0 bps and 0/36 at 10, with a best breakeven of
6 bps on a 24%/yr-turnover book.  Measure, for every 0-bps-only 4b pass in the record, the
turnover level at which the 10-bps rung becomes survivable, and ask whether a turnover
ceiling (not a Sharpe bar) is the cheapest pre-screen for the whole queue.  Max 2 params
(turnover ceiling, cost rung)."

TUNED PARAMETERS: exactly 2 -- the turnover ceiling T* and the cost rung c.  Everything
else (panels, book families, n, cadence, gross) is the POPULATION being screened, and every
point of it is reported.

TWO HALVES
----------
PART A  THE RECORD (retrospective census).  180 of the 1,108 committed CSVs carry both a
        turnover column and a full-sample 4b flag.  Pool every parseable row, split by the
        cost rung the row states, and ask directly: does turnover separate 4b passes from
        4b failures in the committed record?

PART B  THE LIVE GRID (mechanism).  Rebuild a 90-book population spanning the record's
        shapes and, for every book, compute the EXACT cost breakeven c* -- the largest rung
        at which the book still clears 4b.  This is possible without re-running anything
        because `engine.backtest` holds cost-free weights, so

            r_c = r_0 - tau * c/1e4                    (gated below at machine precision)

        is exact for every rung c.  c* is then a bisection on a nonlinear-but-monotone
        function of one scalar.  Report which 4b bar binds first at c* + eps, and test the
        naive closed form c*_pred = (CAGR margin) / (T/1e4) that a turnover ceiling implies.

PART C  THE SCREEN.  Compare, over the same population, two pre-screens for "clears 4b at
        rung c": the TURNOVER CEILING (T <= T*) and the incumbent-style 0-bps SHARPE BAR
        (S_0 >= S*).  All thresholds reported, with precision / recall / lift over the base
        rate.  "Cheapest" is read two ways: fewest points admitted per true pass (precision)
        and least information required (turnover is a property of the book's construction,
        knowable before any return is scored; a Sharpe bar is not).

RULE 8 (walk-forward, required): T* and the Sharpe bar are chosen on 2008-2016 only and the
        screened menu is read ONCE on 2017-2026.  Reported as (i) the screen's OOS lift and
        (ii) the OOS CAGR/Sharpe/MaxDD of the book the screened menu picks, against the
        unscreened pick, RULES v2 (live baseline) and SPY.

BOTH KEEP PATHS reported for every live point: 4a vs RULES v2, 4b vs SPY (per panel).

SURVIVORSHIP: the SMALL panel is current constituents of a sub-$2B screen only
(data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv are
dropped first (44 of 483).  Any small-panel number below is an upper bound on what was
tradeable.

Deterministic, standalone, offline:
    python3 research/backtests/2026-09-07_is-the-0-bps-to-10-bps-cliff-the-real-killer_cloud.py
"""
import csv
import glob
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

OUT = ROOT / "research" / "backtests" / "2026-09-07_is-the-0-bps-to-10-bps-cliff-the-real-killer_cloud"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
RUNGS = [0, 5, 10, 25]
NS = [5, 10, 20, 40]
CADENCES = ["D", "W", "M"]
GROSSES = [0.75, 1.00]
CSTAR_MAX, CSTAR_STEP = 100.0, 0.5      # bps ladder for the breakeven search


# ===================================================================== data
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    s = load_universe(small=True)
    s = s.drop(columns=[c for c in s.columns if c in bad])
    print(f"SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {s.shape[1]-1} names + SPY")
    return {"U56": u, "B136": b, f"SMALL{s.shape[1]-1}": s}


# ===================================================================== books
def eligibility(px):
    s, above, vol20 = score(px)
    ok = above & (vol20 < 0.60)
    return s.where(ok), ok


def w_rank(elig, n, g):
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0) * g


def w_ewall(ok, g):
    sel = ok.astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0) * g


# ===================================================================== metrics at a rung
def net(r0, tau, c):
    return r0 - tau * c / 1e4


def stats(r):
    """CAGR / Sharpe / MaxDD / halves / OOS on one return series."""
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def bars_for(spy):
    """PROTOCOL 4b bars, computed from this panel's own SPY sample."""
    s = stats(spy)
    return dict(H1=s["H1"], H2=s["H2"], OOS=s["OOS_Sharpe"],
                DD=0.60 * abs(s["MaxDD"]), CAGR=0.70 * s["CAGR"], spy=s)


def pass4b(st, B):
    """Returns (bool, first failing bar name, margins dict).  Bar order is PROTOCOL's."""
    tests = [("H1", st["H1"] - B["H1"]), ("H2", st["H2"] - B["H2"]), ("OOS", st["OOS_Sharpe"] - B["OOS"]),
             ("DD", B["DD"] - abs(st["MaxDD"])), ("CAGR", st["CAGR"] - B["CAGR"])]
    fails = [k for k, m in tests if m <= 0]
    return (len(fails) == 0), (fails[0] if fails else ""), {k: m for k, m in tests}


def pass4a(st, base):
    return st["H1"] > base["H1"] and st["H2"] > base["H2"] and st["MaxDD"] >= base["MaxDD"]


def cstar(r0, tau, B, lo=0.0, hi=CSTAR_MAX, step=CSTAR_STEP):
    """Largest rung on the 0.5 bp ladder at which 4b still passes.  -1 if it fails at 0."""
    ok0, _, _ = pass4b(stats(net(r0, tau, 0.0)), B)
    if not ok0:
        return -1.0, ""
    c = lo
    last_ok, bind = 0.0, ""
    while c + step <= hi:
        c += step
        ok, fail, _ = pass4b(stats(net(r0, tau, c)), B)
        if not ok:
            return last_ok, fail
        last_ok = c
    return last_ok, ">grid"


# ===================================================================== PART A: the record
NUMERIC_TRUE = {"true", "1", "yes", "y", "pass", "t"}
NUMERIC_FALSE = {"false", "0", "no", "n", "fail", "f", ""}


def _flag(v):
    s = str(v).strip().lower()
    if s in NUMERIC_TRUE:
        return True
    if s in NUMERIC_FALSE:
        return False
    return None


def _num(v):
    try:
        s = str(v).strip().replace("%", "").replace("x", "")
        if s in ("", "nan", "none", "n/a"):
            return None
        return float(s)
    except Exception:
        return None


def census():
    """Pool every committed CSV row carrying turnover + a full-sample 4b flag."""
    rows = []
    files = 0
    for f in sorted(glob.glob(str(ROOT / "research" / "backtests" / "*.csv"))):
        try:
            with open(f, newline="") as fh:
                rd = list(csv.DictReader(fh))
        except Exception:
            continue
        if not rd:
            continue
        hdr = {c.lower(): c for c in rd[0].keys() if c}
        to_c = next((hdr[c] for c in hdr if "turn" in c), None)
        # prefer a FULL-sample 4b flag; skip oos-only / fail-side columns
        cands = [c for c in hdr if "4b" in c and "fail" not in c and "oos" not in c and "is4b" != c]
        p4_c = hdr[cands[0]] if cands else None
        if not (to_c and p4_c):
            continue
        cost_c = next((hdr[c] for c in hdr if c in ("cost", "bps", "cost_bps", "rung", "cost_rung", "turn_bps")), None)
        sh_c = next((hdr[c] for c in hdr if c in ("sharpe", "full_sharpe", "sharpe_full")), None)
        used = 0
        for r in rd:
            t, p = _num(r.get(to_c)), _flag(r.get(p4_c))
            if t is None or p is None or t < 0 or t > 200:
                continue
            c = _num(r.get(cost_c)) if cost_c else None
            rows.append(dict(file=Path(f).name, turnover=t, pass4b=p,
                             cost=(c if c is not None else np.nan),
                             sharpe=(_num(r.get(sh_c)) if sh_c else np.nan)))
            used += 1
        if used:
            files += 1
    df = pd.DataFrame(rows)
    print(f"\nPART A  CENSUS: {files} committed CSVs contributed {len(df)} parseable "
          f"(turnover, 4b) rows out of 1,108 CSVs on disk.")
    if df.empty:
        return df
    # turnover units in the record are inconsistent (x/yr vs %/yr).  Normalise to x/yr:
    # a row above 25 is almost certainly a percentage.
    df["turn_x"] = np.where(df["turnover"] > 25, df["turnover"] / 100.0, df["turnover"])
    for label, sub in [("ALL rungs pooled", df),
                       ("rung stated == 0 bps", df[df["cost"] == 0]),
                       ("rung stated == 10 bps", df[df["cost"] == 10]),
                       ("rung stated == 25 bps", df[df["cost"] == 25]),
                       ("rung UNSTATED", df[df["cost"].isna()])]:
        if len(sub) < 20:
            print(f"  {label:24s} n={len(sub):5d}  (too few to read)")
            continue
        p, q = sub[sub.pass4b], sub[~sub.pass4b]
        print(f"  {label:24s} n={len(sub):5d}  4b pass rate {sub.pass4b.mean():.3f}  "
              f"median turnover x/yr  pass {p.turn_x.median() if len(p) else float('nan'):6.2f}  "
              f"fail {q.turn_x.median() if len(q) else float('nan'):6.2f}")
    return df


def census_ceiling(df, tag):
    """Lift curve of a turnover ceiling over the pooled record."""
    if len(df) < 50:
        print(f"  ({tag}: n={len(df)}, not read)")
        return pd.DataFrame()
    base = df.pass4b.mean()
    out = []
    for T in [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 20.0]:
        sub = df[df.turn_x <= T]
        if len(sub) == 0:
            continue
        out.append(dict(ceiling_x_yr=T, admitted=len(sub), admit_share=len(sub) / len(df),
                        precision=sub.pass4b.mean(), recall=sub.pass4b.sum() / max(df.pass4b.sum(), 1),
                        lift=sub.pass4b.mean() / base if base else np.nan))
    d = pd.DataFrame(out)
    print(f"\n  {tag}: base 4b rate {base:.4f} over n={len(df)}")
    print(d.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return d


# ===================================================================== main
def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- PART A
    rec = census()
    cen_all = census_ceiling(rec, "turnover ceiling over the WHOLE pooled record")
    cen_0 = census_ceiling(rec[rec.cost == 0], "turnover ceiling on rows stating 0 bps")
    cen_10 = census_ceiling(rec[rec.cost == 10], "turnover ceiling on rows stating 10 bps")
    rec.to_csv(f"{OUT}.census.csv", index=False)
    pd.concat([cen_all.assign(slice="all"), cen_0.assign(slice="0bps"), cen_10.assign(slice="10bps")],
              ignore_index=True).to_csv(f"{OUT}.census_ceiling.csv", index=False)

    # ---------------------------------------------------------------- PART B
    P = panels()
    recs = []
    gate_err = []
    for pname, px in P.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        B = bars_for(spy)
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[start:]
        base = stats(base_r)
        print(f"\n=== {pname}  {px.index[0].date()}->{px.index[-1].date()}  {px.shape[1]-1} names")
        print(f"    SPY  CAGR {B['spy']['CAGR']:.2%}  Sharpe {B['spy']['Sharpe']:.4f}  MaxDD {B['spy']['MaxDD']:.2%}"
              f"  halves {B['spy']['H1']:.4f}/{B['spy']['H2']:.4f}  OOS {B['spy']['OOS_Sharpe']:.4f}")
        print(f"    4b bars: H1>{B['H1']:.4f} H2>{B['H2']:.4f} OOS>{B['OOS']:.4f} "
              f"|DD|<={B['DD']:.2%} CAGR>={B['CAGR']:.2%}")
        print(f"    RULES v2 @10bps: CAGR {base['CAGR']:.2%} Sharpe {base['Sharpe']:.4f} "
              f"MaxDD {base['MaxDD']:.2%} halves {base['H1']:.4f}/{base['H2']:.4f}")

        elig, ok = eligibility(px)
        books = {f"TOP{n}": w_rank(elig, n, 1.0) for n in NS}
        books["EWALL"] = w_ewall(ok, 1.0)
        for bname, w1 in books.items():
            for g in GROSSES:
                for freq in CADENCES:
                    res = backtest(px, w1 * g, cost_bps=0, freq=freq)
                    r0, tau = res["returns"].loc[start:], res["turnover"].loc[start:]
                    yrs = len(r0) / 252
                    T = tau.sum() / yrs                       # x of NAV traded per year
                    st = {c: stats(net(r0, tau, c)) for c in RUNGS}
                    p4b = {c: pass4b(st[c], B) for c in RUNGS}
                    cs, bind = cstar(r0, tau, B)
                    # naive closed form implied by a pure turnover ceiling: the rung at
                    # which the CAGR bar alone would be eaten (drag = T*c/1e4 per year)
                    mC = p4b[0][2]["CAGR"] if p4b[0][0] or True else np.nan
                    pred = (mC / (T / 1e4)) if T > 0 else np.nan
                    recs.append(dict(
                        panel=pname, book=bname, gross=g, cadence=freq, turn_x_yr=T,
                        **{f"S{c}": st[c]["Sharpe"] for c in RUNGS},
                        CAGR0=st[0]["CAGR"], MaxDD0=st[0]["MaxDD"], H1_0=st[0]["H1"], H2_0=st[0]["H2"],
                        OOS_S0=st[0]["OOS_Sharpe"],
                        CAGR10=st[10]["CAGR"], MaxDD10=st[10]["MaxDD"], H1_10=st[10]["H1"],
                        H2_10=st[10]["H2"], OOS_S10=st[10]["OOS_Sharpe"], OOS_CAGR10=st[10]["OOS_CAGR"],
                        OOS_MaxDD10=st[10]["OOS_MaxDD"],
                        **{f"p4b_{c}": p4b[c][0] for c in RUNGS},
                        **{f"fail_{c}": p4b[c][1] for c in RUNGS},
                        p4a_10=pass4a(st[10], base),
                        cstar_bps=cs, cstar_binds=bind, cstar_pred_cagr=pred,
                        m_CAGR0=p4b[0][2]["CAGR"], m_DD0=p4b[0][2]["DD"],
                        m_H1_0=p4b[0][2]["H1"], m_H2_0=p4b[0][2]["H2"], m_OOS0=p4b[0][2]["OOS"],
                    ))
                    # exactness gate on the rung identity, one book per panel
                    if bname == "TOP20" and g == 1.00 and freq == "W":
                        direct = backtest(px, w1 * g, cost_bps=10, freq=freq)["returns"].loc[start:]
                        gate_err.append((pname, float(np.abs(direct - net(r0, tau, 10.0)).max())))
        print(f"    {len(NS)+1} families x {len(GROSSES)} gross x {len(CADENCES)} cadence = "
              f"{(len(NS)+1)*len(GROSSES)*len(CADENCES)} books done")

    G = pd.DataFrame(recs)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    print("\nREPRODUCTION GATE  max|backtest(cost=10) - (r0 - tau*10/1e4)| per panel:")
    for p, e in gate_err:
        print(f"  {p:10s} {e:.3e}   {'PASS' if e < 1e-12 else 'FAIL'}")

    # ---------------------------------------------------------------- the cliff
    print(f"\nPART B  THE CLIFF, all {len(G)} live points reported in {Path(OUT).name}.grid.csv")
    tab = G.groupby("panel").agg(n=("p4b_0", "size"), p4b_0=("p4b_0", "sum"), p4b_5=("p4b_5", "sum"),
                                 p4b_10=("p4b_10", "sum"), p4b_25=("p4b_25", "sum"), p4a_10=("p4a_10", "sum"))
    print(tab.to_string())
    print(f"  TOTAL 4b: {G.p4b_0.sum()}/{len(G)} @0 bps, {G.p4b_5.sum()}/{len(G)} @5, "
          f"{G.p4b_10.sum()}/{len(G)} @10, {G.p4b_25.sum()}/{len(G)} @25.  "
          f"4a @10: {G.p4a_10.sum()}/{len(G)}.")

    zero = G[G.p4b_0].copy()
    print(f"\n  THE 0-bps 4b PASSES ({len(zero)} of {len(G)}): breakeven c*, its binding bar, "
          f"and the turnover that sets it")
    cols = ["panel", "book", "gross", "cadence", "turn_x_yr", "S0", "S10", "CAGR0", "MaxDD0",
            "cstar_bps", "cstar_binds", "cstar_pred_cagr", "m_CAGR0", "m_DD0", "p4b_10"]
    print(zero[cols].sort_values("cstar_bps", ascending=False).to_string(
        index=False, float_format=lambda x: f"{x:.4f}"))
    zero.to_csv(f"{OUT}.cstar.csv", index=False)

    if len(zero) >= 3:
        print(f"\n  WHICH BAR KILLS THE 0-bps PASSES AS COST RISES: "
              f"{zero.cstar_binds.value_counts().to_dict()}")
        surv = zero[zero.cstar_bps >= 10]
        print(f"  Survives the PROTOCOL rung (c* >= 10 bps): {len(surv)}/{len(zero)}.")
        if len(zero) >= 5:
            x, y = zero.turn_x_yr.values, zero.cstar_bps.values
            rho = np.corrcoef(pd.Series(x).rank(), pd.Series(y).rank())[0, 1]  # spearman, no scipy
            pear = np.corrcoef(x, y)[0, 1]
            print(f"  c* vs turnover: spearman {rho:+.4f}, pearson {pear:+.4f} over n={len(zero)}.")
            pr = zero.cstar_pred_cagr.values
            keep = np.isfinite(pr) & (pr >= 0)
            if keep.sum() >= 3:
                err = pr[keep] - y[keep]
                print(f"  Closed form c*_pred = CAGR-margin / (T/1e4): MAE {np.abs(err).mean():.2f} bps, "
                      f"bias {err.mean():+.2f} bps, over-predicts in {(err > 0).sum()}/{keep.sum()} "
                      f"(a turnover ceiling assumes the CAGR bar binds; it does not always).")

    # ---------------------------------------------------------------- PART C: the screen
    print("\nPART C  THE SCREEN.  Target = clears 4b at the PROTOCOL rung (10 bps).")
    scr = []
    base10 = G.p4b_10.mean()
    T_GRID = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 15.0, 1e9]
    S_GRID = [0.0, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, -1e9]
    for T in T_GRID:
        sub = G[G.turn_x_yr <= T]
        scr.append(dict(screen="turnover ceiling", thr=T, admitted=len(sub),
                        admit_share=len(sub) / len(G),
                        precision=sub.p4b_10.mean() if len(sub) else np.nan,
                        recall=sub.p4b_10.sum() / max(G.p4b_10.sum(), 1),
                        lift=(sub.p4b_10.mean() / base10) if (len(sub) and base10) else np.nan))
    for S in S_GRID:
        sub = G[G.S0 >= S]
        scr.append(dict(screen="0-bps Sharpe bar", thr=S, admitted=len(sub),
                        admit_share=len(sub) / len(G),
                        precision=sub.p4b_10.mean() if len(sub) else np.nan,
                        recall=sub.p4b_10.sum() / max(G.p4b_10.sum(), 1),
                        lift=(sub.p4b_10.mean() / base10) if (len(sub) and base10) else np.nan))
    S = pd.DataFrame(scr)
    S.to_csv(f"{OUT}.screen.csv", index=False)
    print(f"  base rate P(4b @10 bps) = {base10:.4f} over n={len(G)}")
    print(S.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------------------------------------------------------- RULE 8
    print("\nRULE 8 WALK-FORWARD  (screen thresholds chosen on 2008-2016 IS only, read once 2017-)")
    wf = []
    for pname, px in P.items():
        start = px.index[260]
        spy_is = px["SPY"].pct_change().fillna(0).loc[start:IS_END]
        spy_oos = px["SPY"].pct_change().fillna(0).loc[OOS_START:]
        mspy_o = metrics(spy_oos)
        elig, ok = eligibility(px)
        books = {f"TOP{n}": w_rank(elig, n, 1.0) for n in NS}
        books["EWALL"] = w_ewall(ok, 1.0)
        menu = []
        for bname, w1 in books.items():
            for g in GROSSES:
                for freq in CADENCES:
                    res = backtest(px, w1 * g, cost_bps=0, freq=freq)
                    r0, tau = res["returns"].loc[start:], res["turnover"].loc[start:]
                    r10 = net(r0, tau, 10.0)
                    ris, roos = r10.loc[:IS_END], r10.loc[OOS_START:]
                    tis = tau.loc[:IS_END].sum() / (len(ris) / 252)
                    mi, mo = metrics(ris), metrics(roos)
                    menu.append(dict(panel=pname, book=bname, gross=g, cadence=freq,
                                     IS_turn=tis, IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
                                     IS_MaxDD=mi["MaxDD"],
                                     OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"]))
        M = pd.DataFrame(menu)
        # IS choice of the ceiling: the T* on the grid maximising IS 4b-proxy precision is
        # not identifiable here (4b needs OOS), so the ceiling is chosen the way a desk
        # would: the tightest ceiling that still admits at least a third of the menu.
        Tstar = float(np.quantile(M.IS_turn, 1 / 3))
        adm = M[M.IS_turn <= Tstar]
        pick_scr = adm.loc[adm.IS_Sharpe.idxmax()]
        pick_all = M.loc[M.IS_Sharpe.idxmax()]
        base_r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"].loc[OOS_START:]
        mb = metrics(base_r)
        wf.append(dict(panel=pname, Tstar_x_yr=Tstar, admitted=len(adm), menu=len(M),
                       screened_pick=f"{pick_scr.book}/g{pick_scr.gross:.2f}/{pick_scr.cadence}",
                       screened_OOS_CAGR=pick_scr.OOS_CAGR, screened_OOS_Sharpe=pick_scr.OOS_Sharpe,
                       screened_OOS_MaxDD=pick_scr.OOS_MaxDD,
                       unscreened_pick=f"{pick_all.book}/g{pick_all.gross:.2f}/{pick_all.cadence}",
                       unscreened_OOS_CAGR=pick_all.OOS_CAGR, unscreened_OOS_Sharpe=pick_all.OOS_Sharpe,
                       unscreened_OOS_MaxDD=pick_all.OOS_MaxDD,
                       rulesv2_OOS_Sharpe=mb["Sharpe"], rulesv2_OOS_CAGR=mb["CAGR"],
                       rulesv2_OOS_MaxDD=mb["MaxDD"],
                       spy_OOS_Sharpe=mspy_o["Sharpe"], spy_OOS_CAGR=mspy_o["CAGR"],
                       spy_OOS_MaxDD=mspy_o["MaxDD"],
                       menu_mean_OOS_Sharpe=M.OOS_Sharpe.mean(),
                       admitted_mean_OOS_Sharpe=adm.OOS_Sharpe.mean()))
        M.to_csv(f"{OUT}.menu_{pname}.csv", index=False)
    W = pd.DataFrame(wf)
    W.to_csv(f"{OUT}.walkforward.csv", index=False)
    print(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d = W.screened_OOS_Sharpe - W.unscreened_OOS_Sharpe
    print(f"\n  Screened minus unscreened OOS Sharpe: {list(np.round(d.values, 4))}  "
          f"mean {d.mean():+.4f}, wins {int((d > 0).sum())}/{len(d)}")
    d2 = W.admitted_mean_OOS_Sharpe - W.menu_mean_OOS_Sharpe
    print(f"  Admitted-set minus whole-menu mean OOS Sharpe: {list(np.round(d2.values, 4))}  "
          f"mean {d2.mean():+.4f}, wins {int((d2 > 0).sum())}/{len(d2)}")
    print("\nWrote:", ", ".join(sorted(p.name for p in OUT.parent.glob(OUT.name + ".*"))))


if __name__ == "__main__":
    main()
