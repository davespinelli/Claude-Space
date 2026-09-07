#!/usr/bin/env python3
"""Idea 355 (lane C, 2026-09-07): is-it-WIDTH-or-CADENCE-that-carries-the-0.14-OOS-Sharpe.

QUEUE TEXT: "idea 352's PARK by-product (U56 TOP40 EW g0.75 MONTHLY, 4b at 10 and 25 bps,
c*=43.5 bps) beats the pre-registered chooser's pick (TOP20 g1.00 monthly) by +0.14 of OOS
Sharpe.  Decompose that gap into the n dial (20->40) and the gross dial (1.00->0.75) at
fixed monthly cadence, on U56 and B136.  Max 2 params (n, gross)."

NOTE ON THE TITLE.  The queue title says WIDTH-or-CADENCE but the queue BODY pins cadence
at MONTHLY and names the two dials as n and gross.  The body is the operative spec, so the
decomposition below is WIDTH (n) vs GROSS (g) at fixed monthly cadence.  Cadence is carried
only as a pre-registered robustness check (Part E), not as a third tuned dial.

TUNED PARAMETERS: exactly 2 -- n and g.  Cadence is FIXED at monthly.  Panels (U56, B136)
are the replication axis, not a dial.  EVERY grid point is reported.

DESIGN
------
PART A  THE 2x2.  Reproduce idea 352's two corners exactly -- A=(n=20, g=1.00) the
        pre-registered chooser's pick, D=(n=40, g=0.75) the PARK by-product -- plus the two
        off-diagonal corners B=(40,1.00) and C=(20,0.75).  The total gap D-A then splits
        two ways along the two edge paths:
            n-first:     A -> B (n dial)     then B -> D (gross dial)
            gross-first: A -> C (gross dial) then C -> D (n dial)
        Main effects are the average of the two readings of each dial; the interaction is
        (D - B - C + A).  Reported for OOS Sharpe (the quantity the queue names) and for
        every other 4b-relevant statistic (CAGR, MaxDD, halves, turnover).

PART B  THE FULL GRID.  n in {5,10,20,40,80,ALL} x g in {0.50,0.75,1.00} x 2 panels = 36
        books, monthly, 10 bps.  All 36 reported with both KEEP paths.  This says whether
        the 2x2's local reading is a slice of a monotone surface or a local accident.

PART C  THE INVARIANCE TEST.  The record (idea 51) claims Sharpe is near-invariant in g for
        unlevered gross-scalar books (span <= 0.0050) while CAGR and MaxDD scale ~linearly.
        If that holds here, the gross dial CANNOT carry an OOS Sharpe gap and the whole
        +0.14 must be the n dial.  Measured directly: Sharpe span across g at fixed n.

PART D  RULE 8 WALK-FORWARD (required).  (n, g) chosen by max Sharpe on 2008-2016 ONLY, then
        read ONCE on 2017-2026.  Reported against the unscreened alternatives, RULES v2
        (live baseline) and SPY.  Also reported: what the IS chooser would have picked vs
        what the OOS argmax was, per panel.

PART E  CADENCE ROBUSTNESS (not a tuned dial).  The 2x2 re-read at W and Q cadence to check
        that the decomposition's SIGN is a monthly-only artefact or not.

BOTH KEEP PATHS reported for every point: 4a vs RULES v2 (Sharpe in both halves + MaxDD no
worse), 4b vs that panel's own SPY (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of
SPY's, CAGR >= 70% of SPY's).

Costs 10 bps/unit turnover, weights at close t applied t+1 (engine).  Deterministic,
standalone, offline:
    python3 research/backtests/2026-09-07_is-it-WIDTH-or-GROSS-that-carries-the-0.14-OOS-Sharpe_C.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights  # noqa
from engine import backtest, metrics  # noqa

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

OUT = ROOT / "research" / "backtests" / "2026-09-07_is-it-WIDTH-or-GROSS-that-carries-the-0.14-OOS-Sharpe_C"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
COST = 10.0
NS = [5, 10, 20, 40, 80, "ALL"]
GS = [0.50, 0.75, 1.00]
CORNERS = {"A_n20_g100": (20, 1.00), "B_n40_g100": (40, 1.00),
           "C_n20_g075": (20, 0.75), "D_n40_g075": (40, 0.75)}


# ===================================================================== panels / books
def panels():
    return {"U56": load_universe(), "B136": load_universe(broad=True)}


def eligibility(px):
    """RULES v1 eligibility: above 200d MA and vol20 < 0.60, scored by the live composite."""
    s, above, vol20 = score(px)
    ok = above & (vol20 < 0.60)
    return s.where(ok), ok


def weights(elig, ok, n, g):
    """Equal weight over the top-n eligible names (n='ALL' -> every eligible name), gross g.
    Identical construction to idea 352's w_rank / w_ewall."""
    sel = ok.astype(float) if n == "ALL" else (elig.rank(axis=1, ascending=False) <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0) * g


# ===================================================================== metrics
def stats(r):
    m = metrics(r)
    h = len(r) // 2
    m1, m2 = metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o = metrics(r.loc[OOS_START:])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def bars_4b(spy_stats):
    return dict(H1=spy_stats["H1"], H2=spy_stats["H2"], OOS=spy_stats["OOS_Sharpe"],
                DD=0.60 * abs(spy_stats["MaxDD"]), CAGR=0.70 * spy_stats["CAGR"])


def pass_4b(st, B):
    tests = [("H1", st["H1"] - B["H1"]), ("H2", st["H2"] - B["H2"]), ("OOS", st["OOS_Sharpe"] - B["OOS"]),
             ("DD", B["DD"] - abs(st["MaxDD"])), ("CAGR", st["CAGR"] - B["CAGR"])]
    fails = [k for k, m in tests if m <= 0]
    return (len(fails) == 0), (fails[0] if fails else ""), {k: m for k, m in tests}


def pass_4a(st, bs):
    return (st["H1"] > bs["H1"]) and (st["H2"] > bs["H2"]) and (st["MaxDD"] >= bs["MaxDD"])


def run(px, elig, ok, n, g, freq):
    res = backtest(px, weights(elig, ok, n, g), cost_bps=COST, freq=freq)
    start = px.index[260]
    r = res["returns"].loc[start:]
    tau = res["turnover"].loc[start:]
    st = stats(r)
    st["turnover"] = tau.sum() / (len(tau) / 252)          # units of gross traded per year
    return st, r


# ===================================================================== main
def main():
    P = panels()
    rows, ctx, corner_rows, cad_rows = [], {}, [], []

    for pname, px in P.items():
        elig, ok = eligibility(px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        spy_st = stats(spy)
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:]
        base_st = stats(base)
        B = bars_4b(spy_st)
        ctx[pname] = dict(spy=spy_st, base=base_st, bars=B, n_names=px.shape[1] - 1,
                          start=str(px.index[260].date()), end=str(px.index[-1].date()))

        print(f"\n{'='*110}\nPANEL {pname}: {px.shape[1]-1} names + SPY, {ctx[pname]['start']} .. {ctx[pname]['end']}")
        print(f"  SPY        CAGR {spy_st['CAGR']:.2%}  Sharpe {spy_st['Sharpe']:.3f}  MaxDD {spy_st['MaxDD']:.2%} "
              f"| H1 {spy_st['H1']:.3f} H2 {spy_st['H2']:.3f} | OOS {spy_st['OOS_CAGR']:.2%}/{spy_st['OOS_Sharpe']:.3f}/{spy_st['OOS_MaxDD']:.2%}")
        print(f"  RULES v2   CAGR {base_st['CAGR']:.2%}  Sharpe {base_st['Sharpe']:.3f}  MaxDD {base_st['MaxDD']:.2%} "
              f"| H1 {base_st['H1']:.3f} H2 {base_st['H2']:.3f} | OOS {base_st['OOS_CAGR']:.2%}/{base_st['OOS_Sharpe']:.3f}/{base_st['OOS_MaxDD']:.2%}")
        print(f"  4b bars    H1>{B['H1']:.3f}  H2>{B['H2']:.3f}  OOS>{B['OOS']:.3f}  |MaxDD|<={B['DD']:.2%}  CAGR>={B['CAGR']:.2%}")

        # ------------------------------------------------- PART B: the full grid (monthly)
        for n in NS:
            for g in GS:
                st, r = run(px, elig, ok, n, g, "M")
                ok4b, firstfail, marg = pass_4b(st, B)
                rec = dict(panel=pname, n=str(n), gross=g, freq="M", **st,
                           pass4a=pass_4a(st, base_st), pass4b=ok4b, first_fail_4b=firstfail,
                           m_H1=marg["H1"], m_H2=marg["H2"], m_OOS=marg["OOS"], m_DD=marg["DD"], m_CAGR=marg["CAGR"])
                rows.append(rec)

        # ------------------------------------------------- PART A: the 2x2 corners
        for cname, (n, g) in CORNERS.items():
            st, _ = run(px, elig, ok, n, g, "M")
            ok4b, ff, _ = pass_4b(st, B)
            corner_rows.append(dict(panel=pname, corner=cname, n=n, gross=g, **st,
                                    pass4a=pass_4a(st, base_st), pass4b=ok4b, first_fail_4b=ff))

        # ------------------------------------------------- PART E: cadence robustness
        for freq in ["W", "M", "Q"]:
            for cname, (n, g) in CORNERS.items():
                st, _ = run(px, elig, ok, n, g, freq)
                ok4b, ff, _ = pass_4b(st, B)
                cad_rows.append(dict(panel=pname, freq=freq, corner=cname, n=n, gross=g, **st,
                                     pass4a=pass_4a(st, base_st), pass4b=ok4b, first_fail_4b=ff))

    grid = pd.DataFrame(rows)
    corners = pd.DataFrame(corner_rows)
    cad = pd.DataFrame(cad_rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    corners.to_csv(f"{OUT}.corners.csv", index=False)
    cad.to_csv(f"{OUT}.cadence.csv", index=False)

    # ================================================================= PART B print
    print(f"\n{'='*110}\nPART B  FULL GRID (monthly, {COST:.0f} bps) -- all 36 points")
    show = ["panel", "n", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe",
            "OOS_MaxDD", "turnover", "pass4a", "pass4b", "first_fail_4b"]
    print(grid[show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ================================================================= PART A decomposition
    print(f"\n{'='*110}\nPART A  THE 2x2 AND ITS DECOMPOSITION (monthly, {COST:.0f} bps)")
    METS = ["OOS_Sharpe", "Sharpe", "H1", "H2", "CAGR", "MaxDD", "OOS_CAGR", "OOS_MaxDD", "turnover"]
    dec_rows = []
    for pname in P:
        c = corners[corners.panel == pname].set_index("corner")
        print(f"\n-- {pname} corners")
        print(c[["n", "gross"] + METS + ["pass4a", "pass4b", "first_fail_4b"]].to_string(float_format=lambda x: f"{x:.4f}"))
        A, Bc, C, D = (c.loc[k] for k in ["A_n20_g100", "B_n40_g100", "C_n20_g075", "D_n40_g075"])
        for m in METS:
            a, b, cc, d = A[m], Bc[m], C[m], D[m]
            dec_rows.append(dict(panel=pname, metric=m,
                                 A_n20_g100=a, B_n40_g100=b, C_n20_g075=cc, D_n40_g075=d,
                                 total_D_minus_A=d - a,
                                 n_dial_at_g100=b - a, n_dial_at_g075=d - cc,
                                 gross_dial_at_n20=cc - a, gross_dial_at_n40=d - b,
                                 n_main=((b - a) + (d - cc)) / 2,
                                 gross_main=((cc - a) + (d - b)) / 2,
                                 interaction=d - b - cc + a))
    dec = pd.DataFrame(dec_rows)
    dec.to_csv(f"{OUT}.decomposition.csv", index=False)
    print(f"\n-- decomposition: total gap D-A split into the two dials (main effect = mean of the two edges)")
    print(dec.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    print("\n-- headline: share of the total D-A gap attributable to each dial")
    for pname in P:
        d = dec[(dec.panel == pname) & (dec.metric == "OOS_Sharpe")].iloc[0]
        tot = d["total_D_minus_A"]
        sh = (lambda x: f"{x/tot:+.1%}" if abs(tot) > 1e-9 else "n/a")
        print(f"  {pname:5s} OOS Sharpe: total {tot:+.4f} = n_main {d['n_main']:+.4f} ({sh(d['n_main'])}) "
              f"+ gross_main {d['gross_main']:+.4f} ({sh(d['gross_main'])}) + interaction {d['interaction']:+.4f} ({sh(d['interaction'])})")

    # ================================================================= PART C invariance
    print(f"\n{'='*110}\nPART C  IS SHARPE INVARIANT IN THE GROSS DIAL?  (span across g at fixed n)")
    inv = (grid.groupby(["panel", "n"])
               .agg(Sharpe_span=("Sharpe", lambda s: s.max() - s.min()),
                    OOS_Sharpe_span=("OOS_Sharpe", lambda s: s.max() - s.min()),
                    CAGR_span=("CAGR", lambda s: s.max() - s.min()),
                    MaxDD_span=("MaxDD", lambda s: s.max() - s.min()))
               .reset_index())
    inv.to_csv(f"{OUT}.invariance.csv", index=False)
    print(inv.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\n  max |OOS Sharpe span across g| over all (panel,n) = {inv['OOS_Sharpe_span'].max():.4f}")
    print(f"  max |CAGR span across g|        over all (panel,n) = {inv['CAGR_span'].max():.4f}")
    # same question for the n dial, at fixed g -- the comparand
    invn = (grid.groupby(["panel", "gross"])
                .agg(Sharpe_span=("Sharpe", lambda s: s.max() - s.min()),
                     OOS_Sharpe_span=("OOS_Sharpe", lambda s: s.max() - s.min()))
                .reset_index())
    print("\n  comparand -- span across n at fixed g:")
    print(invn.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ================================================================= PART D rule 8
    print(f"\n{'='*110}\nPART D  RULE 8 WALK-FORWARD -- (n,g) chosen on 2008-{IS_END[:4]} only, read once {OOS_START[:4]}-")
    wf_rows = []
    for pname, px in P.items():
        elig, ok = eligibility(px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[start:]
        cand = {}
        for n in NS:
            for g in GS:
                _, r = run(px, elig, ok, n, g, "M")
                cand[(str(n), g)] = r
        is_sharpe = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in cand.items()}
        oos_sharpe = {k: metrics(v.loc[OOS_START:])["Sharpe"] for k, v in cand.items()}
        pick = max(is_sharpe, key=is_sharpe.get)
        best_oos = max(oos_sharpe, key=oos_sharpe.get)
        for k, r in cand.items():
            o = metrics(r.loc[OOS_START:])
            wf_rows.append(dict(panel=pname, n=k[0], gross=k[1], IS_Sharpe=is_sharpe[k],
                                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                is_IS_pick=(k == pick), is_OOS_argmax=(k == best_oos)))
        for lbl, r in [("RULES v2", base), ("SPY", spy)]:
            o = metrics(r.loc[OOS_START:])
            wf_rows.append(dict(panel=pname, n=lbl, gross=np.nan, IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"],
                                is_IS_pick=False, is_OOS_argmax=False))
        oA, oD = metrics(cand[("20", 1.00)].loc[OOS_START:]), metrics(cand[("40", 0.75)].loc[OOS_START:])
        print(f"\n-- {pname}: IS pick (n={pick[0]}, g={pick[1]:.2f}) IS Sharpe {is_sharpe[pick]:.4f} "
              f"-> OOS Sharpe {oos_sharpe[pick]:.4f} | OOS argmax was (n={best_oos[0]}, g={best_oos[1]:.2f}) at {oos_sharpe[best_oos]:.4f} "
              f"| chooser regret {oos_sharpe[pick]-oos_sharpe[best_oos]:+.4f}")
        print(f"   queue's two corners OOS Sharpe: A(20,1.00) {oA['Sharpe']:.4f}  D(40,0.75) {oD['Sharpe']:.4f}  "
              f"gap {oD['Sharpe']-oA['Sharpe']:+.4f}")
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    print("\n-- full walk-forward table (all grid points + baselines)")
    print(wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------- PART F: is IS Sharpe informative about n?
    print(f"\n{'='*110}\nPART F  IS THE IS SHARPE INFORMATIVE ABOUT THE n DIAL?  (rank corr IS vs OOS over the 18 grid points)")
    def spearman(a, b):
        """Rank correlation without scipy (the sandbox has no scipy): pearson on ranks."""
        return a.rank().corr(b.rank())

    f_rows = []
    for pname in P:
        w = wf[(wf.panel == pname) & (~wf.n.isin(["RULES v2", "SPY"]))]
        rho_all = spearman(w["IS_Sharpe"], w["OOS_Sharpe"])
        # collapse the (near-null) gross dial: mean over g, so this is purely the n ordering
        wn = w.groupby("n")[["IS_Sharpe", "OOS_Sharpe"]].mean()
        rho_n = spearman(wn["IS_Sharpe"], wn["OOS_Sharpe"])
        f_rows.append(dict(panel=pname, spearman_all18=rho_all, spearman_n_only=rho_n,
                           IS_argmax_n=wn["IS_Sharpe"].idxmax(), OOS_argmax_n=wn["OOS_Sharpe"].idxmax()))
        print(f"\n-- {pname}: spearman(IS, OOS) over all 18 points {rho_all:+.4f}; over the 6 n-levels "
              f"(g averaged out) {rho_n:+.4f}  | IS argmax n={wn['IS_Sharpe'].idxmax()}  OOS argmax n={wn['OOS_Sharpe'].idxmax()}")
        print(wn.to_string(float_format=lambda x: f"{x:.4f}"))
    pd.DataFrame(f_rows).to_csv(f"{OUT}.informativeness.csv", index=False)

    # ================================================================= PART E cadence
    print(f"\n{'='*110}\nPART E  CADENCE ROBUSTNESS (the 2x2 re-read at W/M/Q -- NOT a tuned dial)")
    print(cad[["panel", "freq", "corner", "OOS_Sharpe", "Sharpe", "H1", "H2", "CAGR", "MaxDD", "turnover",
               "pass4a", "pass4b", "first_fail_4b"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n-- D-A gap by cadence (does the sign of the decomposition survive?)")
    for pname in P:
        for freq in ["W", "M", "Q"]:
            c = cad[(cad.panel == pname) & (cad.freq == freq)].set_index("corner")
            a, b, cc, d = (c.loc[k, "OOS_Sharpe"] for k in ["A_n20_g100", "B_n40_g100", "C_n20_g075", "D_n40_g075"])
            print(f"  {pname:5s} {freq}: total {d-a:+.4f} | n_main {((b-a)+(d-cc))/2:+.4f} | "
                  f"gross_main {((cc-a)+(d-b))/2:+.4f} | interaction {d-b-cc+a:+.4f}")

    # ================================================================= verdict summary
    print(f"\n{'='*110}\nKEEP-PATH SUMMARY (monthly grid, {COST:.0f} bps)")
    print(f"  4a passes: {int(grid.pass4a.sum())}/{len(grid)}   4b passes: {int(grid.pass4b.sum())}/{len(grid)}")
    if grid.pass4b.any():
        print(grid[grid.pass4b][show].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n  4b first-failing bar, counts:")
    print(grid.first_fail_4b.value_counts().to_string())

    pd.DataFrame([dict(panel=k, **{f"spy_{a}": b for a, b in v["spy"].items()},
                       **{f"base_{a}": b for a, b in v["base"].items()},
                       **{f"bar_{a}": b for a, b in v["bars"].items()},
                       n_names=v["n_names"], start=v["start"], end=v["end"]) for k, v in ctx.items()]
                ).to_csv(f"{OUT}.ctx.csv", index=False)
    print(f"\nwrote {OUT.name}.{{grid,corners,cadence,decomposition,invariance,walkforward,ctx}}.csv")


if __name__ == "__main__":
    main()
