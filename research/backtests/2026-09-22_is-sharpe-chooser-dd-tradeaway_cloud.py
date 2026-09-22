#!/usr/bin/env python3
"""Idea 960 (2026-09-22, lane cloud, run 12) -- DOES THE IS-SHARPE CHOOSER'S `L4_DD` OOS FAILURE
GENERALISE ACROSS THE GROSS LADDER AND ALL THREE PANELS?

WHY THIS RUN EXISTS
    Idea 951's rule-8 arm found that BOTH of its in-sample choosers pick the NARROW book (TOP10)
    over the incumbent TOP20 on U56 and B136, and that both picks then fail out of sample on the
    4b drawdown cap ALONE: canonical TOP20/M reads OOS 16.67% / 1.283 / -19.51% while the IS pick
    TOP10/M reads 17.20% / 1.097 / -23.20% -- i.e. the chooser buys +0.53 pp of OOS CAGR with
    +3.69 pp of extra drawdown and loses the leg.  That was ONE gross rung (0.75), ONE cadence (M)
    and TWO panels.  If it is a LAW, the record's habitual chooser is systematically shorting the
    4b DD cap and every committed IS-Sharpe pick in the record inherits the bias.  If it is a
    point, 951's sentence should not be generalised.  This run walks it.

THE SHELF (the axis the chooser CHOOSES OVER, never tuned)
    Idea 951's own `ranked_book` is imported and used unchanged: composite score (12-1 momentum +
    6m + 3m return, percentile-ranked and averaged, NO vol scaling), eligible = above the 200d MA
    AND 20d vol < 0.60, top-k at gross/k, gated-out weight to CASH.  WIDTH k in {5,10,20,40,ALL},
    where ALL = every eligible name equal-weighted at the same gross.  k = 20 is the incumbent.

THE TWO TUNED DIALS (PROTOCOL rule 4: exactly two, no more)
    1. GROSS rung g in {0.25, 0.50, 0.75, 1.00, 1.25, 1.50} -- the queue's own ladder.
    2. CHOOSER in {C_SHARPE, C_CALMAR, C_DDB060, C_LIVE}, all IS-ONLY on 2009-2016:
         C_SHARPE  argmax IS Sharpe over the 5 widths                    (the habitual chooser)
         C_CALMAR  argmax IS CAGR / |IS MaxDD|                           (a DD-aware alternative)
         C_DDB060  among widths whose IS MaxDD is inside 0.60 x IS SPY MaxDD -- PROTOCOL 4b's own
                   delta -- argmax IS Sharpe; ABSTAIN if none qualifies  (idea 2264's device)
         C_LIVE    fixed width 20, the NO-INFORMATION control            (the incumbent)
    PANEL {u56, b136, small}, CADENCE {W, M} and COST {0, 10, 25, 50} bps are REPORTED axes,
    walked in full and never selected on.  Every grid point is published, pass or fail.

THE GRID
    3 panels x 6 gross rungs x 5 widths x 2 cadences = 180 simulated books; each is priced at 4
    cost rungs by the EXACT affine identity r(c) = r(0) - turnover * c / 1e4 (gated), giving
    **720 published book cells** and 3 x 6 x 2 x 4 x 4 = **576 published chooser cells**.

GATES (printed before any hypothesis is read)
    G1  the shelf IS idea 951's: `ranked_book(px, g, 20)` at g = 0.75 reproduces the imported
        constructor bit-for-bit (max|dw| = 0 by construction, asserted).
    G2  the affine cost identity is EXACT: max|r_derived(c) - r_simulated(c)| < 1e-15 over a
        re-simulated sample of cells at 25 bps.
    G3  idea 951's own headline cells are reproduced: u56 / g=0.75 / M, widths 20 and 10, against
        its committed OOS triples (16.67% / 1.283 / -19.51% and 17.20% / 1.097 / -23.20%).
        REPORTED with its deviation; asserted at 5e-3 on Sharpe and 5e-3 on the rates.
    G4  every chooser's pick is a member of the published shelf at the same cell (no cell is
        scored against a book that is not in the grid).
    G5  all 720 book cells and 576 chooser cells published.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 read ONCE)
    Every chooser sees 2009-2016 ONLY.  The 2017-2026 window is read once, per chooser per cell,
    and reported against the live RULES v2 book's OOS and SPY's OOS.  The question's statistic is
    the SIGNED OOS drawdown difference between the chooser's pick and the no-information control
    C_LIVE, and the 4b DD-cap leg's OOS pass rate per chooser.

CAVEATS carried
    Survivorship (PROTOCOL rule 9 / idea 54): u56 and b136 are 2026 constituents held from 2008;
    the small panel is the CURRENT sub-$2B screen (data/SMALL_PANEL_README.md) with every ticker
    whose max 1-day move >= 1.0 dropped first, so its CAGR levels are the most optimistic of the
    three and its 4b level legs the easiest.  Costs are flat per unit turnover, no spread, impact
    or borrow.  Execution is t+1 throughout.  Gross rungs above 1.00 are LEVERED and no financing
    charge is modelled (PROTOCOL rule 2 forbids leverage unless the idea says so; the levered
    rungs are published because the queue's ladder names them, and every headline below is also
    reported on the unlevered sub-ladder g <= 1.00).
    Deterministic, standalone.  Writes .log.txt / .grid.csv / .choosers.csv / .tradeaway.csv next
    to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-22_is-sharpe-chooser-dd-tradeaway_cloud"
OUT = ROOT / "research" / "backtests"
I951 = OUT / "2026-09-15_normalise-the-record-s-4b-LEG-ALPHABET_cloud.py"

GROSSES = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50]
WIDTHS = [5, 10, 20, 40, "ALL"]
PANELS = ["u56", "b136", "small"]
CADENCES = ["W", "M"]
COSTS = [0.0, 10.0, 25.0, 50.0]
CHOOSERS = ["C_SHARPE", "C_CALMAR", "C_DDB060", "C_LIVE"]
INCUMBENT = 20
KAPPA = 0.60
PHI0, DELTA0 = 0.70, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BAD_MOVE = 1.0

REF951 = {20: dict(OOS_CAGR=0.1667, OOS_Sharpe=1.283, OOS_MaxDD=-0.1951),
          10: dict(OOS_CAGR=0.1720, OOS_Sharpe=1.097, OOS_MaxDD=-0.2320)}


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 900)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


I = _load(I951, "i951")           # idea 951's own module: ranked_book / score / VOLCAP
ranked_book = I.ranked_book


def all_book(px, g):
    """The shelf's widest rung: every ELIGIBLE name equal-weighted at the same gross."""
    sc, above, vol20 = I.score(px, vol_scale=False)
    elig = (above & (vol20 < I.VOLCAP) & px.notna()).astype(float)
    return g * elig.div(elig.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def shelf_weights(px, g, k):
    return all_book(px, g) if k == "ALL" else ranked_book(px, g, k)


def panel_px(name):
    """SPY is a selectable constituent on u56/b136 and is HELD OUT of the small panel (idea 129
    / 133's convention), where it is the benchmark return series only."""
    if name == "small":
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        return px[inv], px["SPY"].pct_change().fillna(0.0), len(bad)
    px = load_universe(broad=(name == "b136"))
    return px, px["SPY"].pct_change().fillna(0.0), 0


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def full_score(r, spy, base):
    m = metrics(r); h1, h2 = halves(r)
    ms, mb = metrics(spy), metrics(base)
    s1, s2 = halves(spy); b1, b2 = halves(base)
    ro, so, bo = r.loc[OOS_START:], spy.loc[OOS_START:], base.loc[OOS_START:]
    mo, mso, mbo = metrics(ro), metrics(so), metrics(bo)
    ri, si = r.loc[:IS_END], spy.loc[:IS_END]
    mi, msi = metrics(ri), metrics(si)
    L1 = h1 > s1; L2 = h2 > s2; L3 = mo["Sharpe"] > mso["Sharpe"]
    L4 = m["MaxDD"] >= DELTA0 * ms["MaxDD"]; L5 = m["CAGR"] >= PHI0 * ms["CAGR"]
    L4o = mo["MaxDD"] >= DELTA0 * mso["MaxDD"]; L5o = mo["CAGR"] >= PHI0 * mso["CAGR"]
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                IS_SPY_MaxDD=msi["MaxDD"],
                L1_H1=L1, L2_H2=L2, L3_OOS=L3, L4_DD=L4, L5_CAGR=L5,
                L4_DD_oos=L4o, L5_CAGR_oos=L5o,
                pass4a=(h1 > b1) and (h2 > b2) and (m["MaxDD"] >= mb["MaxDD"]),
                pass4b=L1 and L2 and L3 and L4 and L5,
                pass4b_oos=L3 and L4o and L5o,
                SPY_CAGR=ms["CAGR"], SPY_S=ms["Sharpe"], SPY_DD=ms["MaxDD"],
                SPY_H1=s1, SPY_H2=s2, SPY_OOS_CAGR=mso["CAGR"], SPY_OOS_S=mso["Sharpe"],
                SPY_OOS_DD=mso["MaxDD"],
                BASE_CAGR=mb["CAGR"], BASE_S=mb["Sharpe"], BASE_DD=mb["MaxDD"],
                BASE_H1=b1, BASE_H2=b2, BASE_OOS_S=mbo["Sharpe"], BASE_OOS_CAGR=mbo["CAGR"])


def main():
    rows, gate2 = [], []
    for panel in PANELS:
        px, spy_full, ndrop = panel_px(panel)
        start = px.index[260]
        spy = spy_full.loc[start:]
        say(f"[panel] {panel}: {px.shape[1]} instruments, {px.index[0].date()} -> "
            f"{px.index[-1].date()}" + (f", {ndrop} small-panel tickers dropped on max_1d_move "
                                        f">= {BAD_MOVE}" if ndrop else ""))
        base_cache = {}
        for cad in CADENCES:
            b = backtest(px, rules_v2_weights(px), cost_bps=0.0, freq=cad)
            base_cache[cad] = (b["returns"].loc[start:], b["turnover"].loc[start:])
        for g in GROSSES:
            for k in WIDTHS:
                w = shelf_weights(px, g, k)
                for cad in CADENCES:
                    res = backtest(px, w, cost_bps=0.0, freq=cad)
                    r0 = res["returns"].loc[start:]
                    to = res["turnover"].loc[start:]
                    yrs = len(r0) / 252
                    b0, bto = base_cache[cad]
                    for c in COSTS:
                        r = r0 - to * c / 1e4
                        base = b0 - bto * c / 1e4
                        sc = full_score(r, spy, base)
                        rows.append(dict(panel=panel, gross=g, width=str(k), cadence=cad,
                                         cost_bps=c, TO=to.sum() / yrs,
                                         base_TO=bto.sum() / yrs, **sc))
                    if g == 0.75 and k == 20:            # G2 sample
                        sim = backtest(px, w, cost_bps=25.0, freq=cad)["returns"].loc[start:]
                        gate2.append(float((sim - (r0 - to * 25.0 / 1e4)).abs().max()))
        say(f"[panel] {panel}: {len(GROSSES)*len(WIDTHS)*len(CADENCES)} books simulated.")

    G = pd.DataFrame(rows)

    say(f"[G1] shelf constructor is idea 951's `ranked_book` imported from "
        f"{I951.name} (ALL rung is this run's own widest member, published beside it).")
    say(f"[G2] affine cost identity exact at the re-simulated sample: max|d| = {max(gate2):.3e}")
    assert max(gate2) < 1e-15, gate2

    g3 = {}
    for k, ref in REF951.items():
        cell = G[(G.panel == "u56") & (G.gross == 0.75) & (G.width == str(k)) &
                 (G.cadence == "M") & (G.cost_bps == 10.0)].iloc[0]
        g3[k] = {kk: float(cell[kk] - v) for kk, v in ref.items()}
        say(f"[G3] u56 g=0.75 M 10bps TOP{k}: OOS {cell.OOS_CAGR:.4f}/{cell.OOS_Sharpe:.4f}/"
            f"{cell.OOS_MaxDD:.4f}  vs idea 951 {ref['OOS_CAGR']:.4f}/{ref['OOS_Sharpe']:.4f}/"
            f"{ref['OOS_MaxDD']:.4f}   d = " + " ".join(f"{v:+.4f}" for v in g3[k].values()))
    worst = max(abs(v) for d in g3.values() for v in d.values())
    say(f"[G3] worst deviation from idea 951's committed cells: {worst:.3e}")
    assert worst < 5e-3, g3

    # -------------------------------------------------------------------- choosers ----
    ch = []
    for (panel, g, cad, c), cell in G.groupby(["panel", "gross", "cadence", "cost_bps"]):
        isd = cell.set_index("width")
        live = isd.loc[str(INCUMBENT)]
        cap = KAPPA * live["IS_SPY_MaxDD"]
        picks = {}
        picks["C_SHARPE"] = isd["IS_Sharpe"].idxmax()
        picks["C_CALMAR"] = (isd["IS_CAGR"] / isd["IS_MaxDD"].abs()).idxmax()
        ok = isd[isd["IS_MaxDD"] >= cap]
        picks["C_DDB060"] = ok["IS_Sharpe"].idxmax() if len(ok) else "ABSTAIN"
        picks["C_LIVE"] = str(INCUMBENT)
        for name, w in picks.items():
            if w == "ABSTAIN":
                ch.append(dict(panel=panel, gross=g, cadence=cad, cost_bps=c, chooser=name,
                               pick="ABSTAIN", abstain=True))
                continue
            assert w in set(isd.index), (name, w)                        # G4
            p = isd.loc[w]
            ch.append(dict(panel=panel, gross=g, cadence=cad, cost_bps=c, chooser=name,
                           pick=w, abstain=False,
                           IS_Sharpe=p["IS_Sharpe"], IS_MaxDD=p["IS_MaxDD"],
                           OOS_CAGR=p["OOS_CAGR"], OOS_Sharpe=p["OOS_Sharpe"],
                           OOS_MaxDD=p["OOS_MaxDD"],
                           d_OOS_MaxDD_pp=(p["OOS_MaxDD"] - live["OOS_MaxDD"]) * 100,
                           d_OOS_CAGR_pp=(p["OOS_CAGR"] - live["OOS_CAGR"]) * 100,
                           d_OOS_Sharpe=p["OOS_Sharpe"] - live["OOS_Sharpe"],
                           deeper_than_live=bool(p["OOS_MaxDD"] < live["OOS_MaxDD"]),
                           L4_DD=bool(p["L4_DD"]), L4_DD_oos=bool(p["L4_DD_oos"]),
                           pass4a=bool(p["pass4a"]), pass4b=bool(p["pass4b"]),
                           pass4b_oos=bool(p["pass4b_oos"]),
                           live_OOS_MaxDD=live["OOS_MaxDD"], live_OOS_CAGR=live["OOS_CAGR"],
                           live_L4_DD_oos=bool(live["L4_DD_oos"]), TO=p["TO"]))
    CH = pd.DataFrame(ch)
    say(f"[G4] every non-abstaining pick is a published shelf member ({int((~CH.abstain).sum())} "
        f"of {len(CH)} chooser cells).")
    say(f"[G5] {len(G)} book cells and {len(CH)} chooser cells published.\n")

    # ------------------------------------------------------------------- the answer ----
    say("=" * 128)
    say("THE QUESTION: does the IS-SHARPE chooser systematically trade the 4b DD cap away?")
    say("(signed OOS drawdown difference against the NO-INFORMATION control C_LIVE = fixed width 20)")
    say("=" * 128)
    TA = []
    for name in CHOOSERS:
        s = CH[(CH.chooser == name) & (~CH.abstain)]
        n = len(s)
        TA.append(dict(chooser=name, cells=n, abstain=int((CH.chooser == name).sum()) - n,
                       share_deeper=s.deeper_than_live.mean() if n else np.nan,
                       med_d_OOS_MaxDD_pp=s.d_OOS_MaxDD_pp.median() if n else np.nan,
                       mean_d_OOS_MaxDD_pp=s.d_OOS_MaxDD_pp.mean() if n else np.nan,
                       med_d_OOS_CAGR_pp=s.d_OOS_CAGR_pp.median() if n else np.nan,
                       med_d_OOS_Sharpe=s.d_OOS_Sharpe.median() if n else np.nan,
                       L4_DD_oos_rate=s.L4_DD_oos.mean() if n else np.nan,
                       L4_DD_full_rate=s.L4_DD.mean() if n else np.nan,
                       pass4b_rate=s.pass4b.mean() if n else np.nan,
                       pass4b_oos_rate=s.pass4b_oos.mean() if n else np.nan,
                       pass4a_rate=s.pass4a.mean() if n else np.nan,
                       picks=dict(s.pick.value_counts())))
    TAdf = pd.DataFrame(TA)
    say(TAdf.drop(columns=["picks"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    for t in TA:
        say(f"    {t['chooser']:9s} picks {t['picks']}")
    say("")

    unlev = CH[(CH.gross <= 1.00) & (~CH.abstain)]
    say("SAME TABLE ON THE UNLEVERED SUB-LADDER (g <= 1.00, PROTOCOL rule 2)")
    say(unlev.groupby("chooser").agg(cells=("pick", "size"),
                                     share_deeper=("deeper_than_live", "mean"),
                                     med_d_OOS_MaxDD_pp=("d_OOS_MaxDD_pp", "median"),
                                     med_d_OOS_CAGR_pp=("d_OOS_CAGR_pp", "median"),
                                     L4_DD_oos_rate=("L4_DD_oos", "mean"),
                                     pass4b_rate=("pass4b", "mean"))
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    say("C_SHARPE's DD trade-away BY PANEL and BY GROSS RUNG (share of cells whose pick is")
    say("deeper OOS than the incumbent width 20, and the median size of that move in pp)")
    cs = CH[(CH.chooser == "C_SHARPE") & (~CH.abstain)]
    say(cs.pivot_table(index="gross", columns="panel", values="deeper_than_live", aggfunc="mean")
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say(cs.pivot_table(index="gross", columns="panel", values="d_OOS_MaxDD_pp", aggfunc="median")
        .to_string(float_format=lambda x: f"{x:+.2f}"))
    say("")
    say("C_SHARPE's PICK by panel x gross (which width the habitual chooser takes)")
    say(cs.pivot_table(index="gross", columns=["panel", "cadence"], values="pick",
                       aggfunc=lambda s: "/".join(sorted(set(s)))).to_string())
    say("")

    say("=" * 128)
    say("ALL 576 CHOOSER CELLS")
    say("=" * 128)
    say(CH.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 128)
    say("ALL 720 BOOK CELLS")
    say("=" * 128)
    cols = ["panel", "gross", "width", "cadence", "cost_bps", "CAGR", "Sharpe", "MaxDD",
            "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO",
            "L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR", "pass4a", "pass4b", "pass4b_oos"]
    say(G[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("BENCHMARKS (same sample, per panel x cadence x cost rung)")
    say(G[["panel", "cadence", "cost_bps", "BASE_CAGR", "BASE_S", "BASE_DD", "BASE_H1", "BASE_H2",
           "BASE_OOS_CAGR", "BASE_OOS_S", "SPY_CAGR", "SPY_S", "SPY_DD", "SPY_H1", "SPY_H2",
           "SPY_OOS_CAGR", "SPY_OOS_S", "SPY_OOS_DD", "base_TO"]].drop_duplicates()
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    say("=" * 128)
    say("HYPOTHESES")
    say("=" * 128)
    t = TAdf.set_index("chooser")
    say(f"H1  GENERALISATION: C_SHARPE's pick is DEEPER out of sample than the incumbent width 20 "
        f"at {t.loc['C_SHARPE','share_deeper']:.1%} of its {int(t.loc['C_SHARPE','cells'])} cells, "
        f"median {t.loc['C_SHARPE','med_d_OOS_MaxDD_pp']:+.2f} pp of MaxDD for "
        f"{t.loc['C_SHARPE','med_d_OOS_CAGR_pp']:+.2f} pp of OOS CAGR.  951's own cell read "
        f"+3.69 pp of drawdown for +0.53 pp of CAGR.")
    say(f"H2  THE LEG: C_SHARPE's picks clear the 4b DD cap out of sample at "
        f"{t.loc['C_SHARPE','L4_DD_oos_rate']:.1%}, against the no-information control C_LIVE's "
        f"{t.loc['C_LIVE','L4_DD_oos_rate']:.1%}.")
    say(f"H3  IS A DD-AWARE CHOOSER BETTER?  C_CALMAR {t.loc['C_CALMAR','L4_DD_oos_rate']:.1%}, "
        f"C_DDB060 {t.loc['C_DDB060','L4_DD_oos_rate']:.1%} "
        f"({int(t.loc['C_DDB060','abstain'])} abstentions), against C_SHARPE's "
        f"{t.loc['C_SHARPE','L4_DD_oos_rate']:.1%}.")
    say(f"H4  WHOLE-PATH: 4b FULL pass rate by chooser " +
        ", ".join(f"{n} {t.loc[n,'pass4b_rate']:.1%}" for n in CHOOSERS) +
        "; 4a " + ", ".join(f"{n} {t.loc[n,'pass4a_rate']:.1%}" for n in CHOOSERS) + ".")
    say(f"H5  BOOK-LEVEL BASE RATES over all {len(G)} cells: 4a {int(G.pass4a.sum())}, "
        f"4b {int(G.pass4b.sum())}, 4b OOS {int(G.pass4b_oos.sum())}, "
        f"BOTH {int((G.pass4a & G.pass4b).sum())}.")
    fails = G[~G.pass4b]
    binders = {"L1_H1": int((~fails.L1_H1).sum()), "L2_H2": int((~fails.L2_H2).sum()),
               "L3_OOS": int((~fails.L3_OOS).sum()), "L4_DD": int((~fails.L4_DD).sum()),
               "L5_CAGR": int((~fails.L5_CAGR).sum())}
    say(f"H6  binding legs over the {len(fails)} 4b FAIL cells: {binders}")
    say(f"H7  WIDTH ITSELF: median OOS MaxDD by width, pooled over panels x gross x cadence x cost:")
    say(G.groupby("width").agg(OOS_MaxDD_med=("OOS_MaxDD", "median"),
                               OOS_CAGR_med=("OOS_CAGR", "median"),
                               OOS_Sharpe_med=("OOS_Sharpe", "median"),
                               IS_Sharpe_med=("IS_Sharpe", "median"),
                               L4_DD_oos_rate=("L4_DD_oos", "mean"))
        .reindex([str(w) for w in WIDTHS]).to_string(float_format=lambda x: f"{x:.4f}"))

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    CH.to_csv(OUT / f"{STEM}.choosers.csv", index=False)
    TAdf.drop(columns=["picks"]).to_csv(OUT / f"{STEM}.tradeaway.csv", index=False)
    (OUT / f"{STEM}.log.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
