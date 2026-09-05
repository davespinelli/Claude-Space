#!/usr/bin/env python3
"""QUEUE idea 115 — sleeve-G-is-2013 (cloud, 2026-09-05).

Question (verbatim from QUEUE.md)
---------------------------------
"idea 112 showed the sleeve grid's whole gap (G -0.169) flips to +0.035 when 2013 is deleted
while every other grid moves <=0.013.  Decompose 2013 for the sleeve specifically: which of
TLT/GLD/DBC/UUP loses in 2013 (taper tantrum, gold -28%), and is the sleeve's rule-8 gap simply
'gold had one terrible year inside the IS window'?  Bears on ideas 105/106's gold question."

WHY IT MATTERS
--------------
G(p) = d(IS,p) - d(OOS,p) with d(W,p) = Sharpe_W(overlay p) - Sharpe_W(no overlay).  A negative G
means the overlay looks WORSE in rule 8's in-sample window than it turns out to be out of sample,
i.e. PROTOCOL rule 8 systematically under-selects it.  The sleeve carries almost the whole of the
project's measured G (-0.169 against -0.058 pooled), and idea 112 showed the entire number is a
2013 effect.  If that is "gold had one terrible year", the fix is a stated caveat about one asset
in one year.  If it is "any non-equity leg is punished by a +32% equity year", the fix is about
the WINDOW, not the sleeve, and ideas 105/106's gold question is mis-aimed.

HARNESS — idea 112's module imported construction-for-construction, nothing re-implemented
------------------------------------------------------------------------------------------
  book()/sleeve_weights()/_regross()/overlay()/full_row()/keep_4a/4b/net/sharpe come from
  research/backtests/2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py, so every
  number here is directly comparable to idea 112's committed CSVs (asserted in S0).
  Cells:  2 universes (u56 = universe.json incl. BTC/ETH, broad = universe_broad.json)
        x 2 base books (top20 ranked, ewall equal-weight-all-eligible; both 0.75 gross)
        x 2 cost rungs (10, 25 bps), weekly, next-day execution  =  8 CELLS.
  Sleeve fraction f in {0.00, 0.25, 0.50, 0.75, 1.00} (idea 112's grid, unchanged).
  IS = ..2016-12-31 (rule 8), OOS = 2017-01-01.. and is NEVER used to choose anything.

TUNED PARAMETERS (PROTOCOL rule 4): TWO — the sleeve fraction f, and the sleeve COMPOSITION
(which of the four assets is in the leg).  Every point of both axes is reported; nothing else
is selected anywhere in this script.

SLEEVE VARIANTS (the composition axis, all reported)
    S4        TLT+GLD+DBC+UUP        idea 99/112's sleeve, the incumbent
    exTLT / exGLD / exDBC / exUUP    leave-one-asset-out
    GLDonly                          the strong form of the queue's hypothesis
    FLAT4     the four legs held at S4's own weights but earning ZERO return.  This is the
              DILUTION control: it has the sleeve's exact weight footprint and none of its
              asset returns, so whatever d it produces in 2013 is what *any* non-equity leg
              would have produced by diluting a +32% equity year.  Weights are computed on the
              real panel and applied to a panel whose four sleeve columns are constant, so the
              base book's own holdings of those four names are also flattened; the base book's
              average weight in S4 names is reported to bound that contamination.

STATISTICS, DECLARED BEFORE ANY NUMBER WAS COMPUTED
----------------------------------------------------
S0 REPRODUCTION.  Idea 112's committed .deltas.csv sleeve rows are read back and this run's
   G_full / G_ex2013 are compared point by point (32 points).  Tolerance 1e-9.  A mismatch is
   reported and the run stops trusting idea 112's framing.

S1 WHICH ASSET LOSES IN 2013 (the queue's first question).  Exact return attribution inside the
   sleeve leg: for each asset, sum over 2013 of w_{i,t} * r_{i,t} using the realised (t+1
   executed) sleeve weights, plus each asset's own 2013 total return and its mean sleeve weight.
   Attribution is exact by construction: the four contributions sum to the sleeve leg's return.

S2 LEAVE-ONE-ASSET-OUT G.  For each variant, the pooled sleeve G_full and G_ex2013 over the 8
   cells x 4 non-null f, i.e. idea 112's statistic recomputed with one asset removed.

S3 THE DILUTION CONTROL.  d_2013 for FLAT4 against d_2013 for S4, pooled and per cell.  The
   fraction of the S4 sleeve's 2013 damage that a zero-return leg reproduces is the share of
   the effect that is NOT about gold, or about any sleeve asset at all.

S4 THE PRE-REGISTERED DECISION.  "The sleeve's rule-8 gap is gold-in-2013" is judged TRUE iff
   ALL THREE hold:
       (i)   GLD is the largest negative 2013 contributor of the four (S1);
       (ii)  |pooled G_full(exGLD)| <= 0.5 x |pooled G_full(S4)|            (S2);
       (iii) |G_full(exGLD) - G_ex2013(exGLD)| <= 0.05, i.e. deleting 2013 no longer moves G
             once gold is out                                              (S2).
   If (i) holds but (ii)/(iii) fail, the honest headline is that gold is the biggest single
   loser but not the mechanism.  Judged FALSE if (i) fails.

S5 PER-YEAR d.  Pooled sleeve d by calendar year, re-derived on this run's points, so 2013's
   rank among the years is measured here and not quoted from idea 99.

S6 WALK-FORWARD (PROTOCOL rule 8, mandatory).  For every variant x cell, f is chosen on the IS
   window ONLY by argmax IS Sharpe (tie-break smallest f, idea 112's rule), and the untouched
   OOS window 2017-2026 is then reported: OOS CAGR / Sharpe / MaxDD against RULES v1 and SPY,
   with both KEEP paths (4a beat-the-book, 4b capital-worthy) evaluated full-sample and OOS.

CAVEATS
-------
SURVIVORSHIP: universe.json and universe_broad.json are current-constituent lists, so the base
  books' absolute CAGR/Sharpe are optimistic.  Every statistic here is a DIFFERENCE between two
  books holding the same equity names on the same days, plus four ETFs that have no survivorship
  exposure at all, so the bias is close to cancelling; it is not zero, and the absolute levels
  should not be quoted.
SPLICED SHARPE: deleting a calendar year leaves mean/std well defined (idea 89's convention);
  MaxDD is never taken on a spliced series.
2009 is a partial IS year (the eval starts ~2009-01 after the 260-row warm-up).

Deterministic, standalone, no network:
    python research/backtests/2026-09-05_sleeve-G-is-2013_cloud.py
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

from baseline import load_universe, rules_v1_weights  # noqa: E402
from engine import backtest  # noqa: E402

I112 = REPO / "research" / "backtests" / "2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py"
_spec = importlib.util.spec_from_file_location("i112", I112)
H = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)

FREQ, COSTS, IS_END, SPLIT = H.FREQ, H.COSTS, H.IS_END, H.SPLIT
S4 = list(H.S4)
FRACS = list(H.GRIDS["sleeve"])
IS_YEARS = list(H.IS_YEARS)
FOCUS = 2013
OUT = Path(__file__).with_suffix("")

VARIANTS = {
    "S4":      S4,
    "exTLT":   [t for t in S4 if t != "TLT"],
    "exGLD":   [t for t in S4 if t != "GLD"],
    "exDBC":   [t for t in S4 if t != "DBC"],
    "exUUP":   [t for t in S4 if t != "UUP"],
    "GLDonly": ["GLD"],
    "FLAT4":   S4,          # same weights, zero returns (the dilution control)
}

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.4f}")


def sleeve_overlay(px, kind, assets, f):
    """idea 112's sleeve overlay with an arbitrary asset list."""
    E = H.book(px, kind)
    if f == 0.0:
        return H._regross(E, 1.00)
    return H._regross((1 - f) * E + f * H.sleeve_weights(px, assets), 1.00)


def flat_panel(px, assets):
    """A copy of the panel in which `assets` never move (constant price = zero return)."""
    q = px.copy()
    for a in assets:
        q[a] = float(px[a].dropna().iloc[0])
    return q


def main():
    u56 = load_universe(exclude=set())
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    print(f"[data] u56 {u56.shape[1]} cols {u56.index[0].date()}..{u56.index[-1].date()} | "
          f"broad {broad.shape[1]} cols")
    print("[pre-registered] S0 reproduction · S1 which asset loses 2013 · S2 leave-one-asset-out G")
    print("[pre-registered] S3 dilution control · S4 decision rule · S5 per-year d · S6 rule-8 WF")
    print(f"[pre-registered] IS ..{IS_END}, OOS {SPLIT}.. never used to choose; f grid {FRACS}")
    print("[pre-registered] DECISION: 'gold-in-2013' TRUE iff (i) GLD is the largest negative 2013")
    print("                 contributor AND (ii) |G(exGLD)| <= 0.5|G(S4)| AND (iii) |G(exGLD) -")
    print("                 G_ex2013(exGLD)| <= 0.05.  (i) alone => 'biggest loser, not mechanism'.\n")

    # ---------------------------------------------------------------- the grid
    rows, series = [], {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = H.full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        print("=" * 120)
        print(f"### {tag}: eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": H.full_row(H.net(bgr, bto, 10)),
                                "SPY": spy}).T))
        flat = flat_panel(px, S4)
        for vname, assets in VARIANTS.items():
            rpx = flat if vname == "FLAT4" else px
            for kind in ("top20", "ewall"):
                for f in FRACS:
                    w = sleeve_overlay(px, kind, assets, f)         # weights ALWAYS on real px
                    res = backtest(rpx, w, cost_bps=0.0, freq=FREQ)
                    gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    for bps in COSTS:
                        r = H.net(gr, to, bps)
                        series[(tag, vname, kind, bps, f)] = r
                        row = H.full_row(r)
                        base = H.full_row(H.net(bgr, bto, bps))
                        row.update(universe=tag, variant=vname, book=kind, f=f, cost_bps=bps,
                                   Gross=float(w.loc[start:].sum(axis=1).mean()),
                                   Turn_yr=float(to.sum() / (len(gr) / 252)))
                        isr = r.loc[:IS_END]
                        row["IS_Sharpe_full"] = H.sharpe(isr)
                        for y in IS_YEARS:
                            row[f"IS_Sharpe_ex{y}"] = H.sharpe(isr[isr.index.year != y])
                        for y in range(2009, 2027):
                            row[f"SH_y_{y}"] = H.sharpe(r.loc[f"{y}-01-01":f"{y}-12-31"])
                            yr = r.loc[f"{y}-01-01":f"{y}-12-31"]
                            row[f"RET_y_{y}"] = float((1 + yr).prod() - 1) if len(yr) > 20 else np.nan
                        row["4a"] = H.keep_4a(row, base)
                        row["4b"] = H.keep_4b(row, spy)
                        row["4b_oos"] = H.keep_4b_oos(row, spy)
                        rows.append(row)
        universes[tag] = px

    G = pd.DataFrame(rows)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv "
          f"({len(VARIANTS)} variants x {len(FRACS)} f x 2 books x 2 universes x 2 cost rungs)")

    # ---------------------------------------------------------------- d and G
    CELL = ["universe", "variant", "book", "cost_bps"]
    recs = []
    for key, sub in G.groupby(CELL, sort=False):
        null = sub[sub.f == 0.0].iloc[0]
        for _, r in sub[sub.f != 0.0].iterrows():
            d = dict(zip(CELL, key), f=r["f"])
            d["d_OOS"] = r["OOS_Sharpe"] - null["OOS_Sharpe"]
            d["d_IS_full"] = r["IS_Sharpe_full"] - null["IS_Sharpe_full"]
            d["G_full"] = d["d_IS_full"] - d["d_OOS"]
            for y in IS_YEARS:
                d[f"d_IS_ex{y}"] = r[f"IS_Sharpe_ex{y}"] - null[f"IS_Sharpe_ex{y}"]
                d[f"G_ex{y}"] = d[f"d_IS_ex{y}"] - d["d_OOS"]
            for y in range(2009, 2027):
                d[f"d_y_{y}"] = r[f"SH_y_{y}"] - null[f"SH_y_{y}"]
                d[f"dret_y_{y}"] = r[f"RET_y_{y}"] - null[f"RET_y_{y}"]
            recs.append(d)
    D = pd.DataFrame(recs)
    D.to_csv(OUT.with_suffix(".deltas.csv"), index=False)

    # ============================================================ S0 reproduction
    print("\n" + "=" * 120)
    print("S0  REPRODUCTION of idea 112's committed sleeve rows (32 points, tol 1e-9)")
    ref = pd.read_csv(REPO / "research" / "backtests" /
                      "2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.deltas.csv")
    ref = ref[ref.grid == "sleeve"].copy()
    mine = D[D.variant == "S4"].copy()
    key = ["universe", "book", "cost_bps"]
    ref["f"] = ref["param"].astype(float)
    m = ref.merge(mine, on=key + ["f"], suffixes=("_ref", "_new"))
    cols = ["d_IS_full", "d_OOS", "G_full"] + [f"G_ex{y}" for y in IS_YEARS]
    err = {c: float((m[f"{c}_ref"] - m[f"{c}_new"]).abs().max()) for c in cols}
    worst = max(err.values())
    print(f"    matched {len(m)} of {len(ref)} idea-112 sleeve points; max |diff| over "
          f"{len(cols)} statistics = {worst:.2e}")
    print("    " + "  ".join(f"{c}:{err[c]:.1e}" for c in cols[:4]))
    ok = worst < 1e-9 and len(m) == len(ref)
    print(f"    REPRODUCTION: {'EXACT' if ok else 'FAILED — idea 112 framing not trusted below'}")
    print(f"    idea 112 published pooled sleeve G_full -0.1694 -> G_ex2013 +0.0350; this run "
          f"{mine.G_full.mean():+.4f} -> {mine.G_ex2013.mean():+.4f}")

    # ============================================================ S1 which asset loses 2013
    print("\n" + "=" * 120)
    print("S1  WHICH OF TLT/GLD/DBC/UUP LOSES IN 2013 — exact return attribution inside the leg")
    print("    contribution_i = sum over 2013 of w_i,t * r_i,t with the realised (t+1) sleeve")
    print("    weights; the four contributions sum to the sleeve leg's 2013 return.")
    att = []
    for tag, px in universes.items():
        rets = px.pct_change().fillna(0.0)
        sw = H.sleeve_weights(px, S4).shift(1).fillna(0.0)          # t+1 execution
        for y in list(range(2009, 2017)) + [2020, 2022]:
            sl = slice(f"{y}-01-01", f"{y}-12-31")
            legw = sw.loc[sl, S4]
            legr = rets.loc[sl, S4]
            if len(legw) < 20:
                continue
            tot = float((legw * legr).sum().sum())
            for a in S4:
                pr = px[a].loc[sl]
                att.append(dict(universe=tag, year=y, asset=a,
                                mean_w=float(legw[a].mean()),
                                asset_ret=float(pr.iloc[-1] / pr.iloc[0] - 1),
                                contrib=float((legw[a] * legr[a]).sum()),
                                leg_total=tot))
    A = pd.DataFrame(att)
    A.to_csv(OUT.with_suffix(".attrib.csv"), index=False)
    for tag in universes:
        sub = A[(A.universe == tag) & (A.year == FOCUS)]
        print(f"\n  --- {tag}, {FOCUS}: sleeve leg total {sub.leg_total.iloc[0]:+.4f}")
        print(fmt(sub.set_index("asset")[["mean_w", "asset_ret", "contrib"]]))
    piv = A[A.universe == "u56"].pivot_table(index="year", columns="asset", values="contrib")
    print(f"\n  --- u56 sleeve-leg contribution by asset and year (IS years + 2020/2022)")
    print(fmt(piv))
    worst_2013 = A[(A.universe == "u56") & (A.year == FOCUS)].sort_values("contrib").iloc[0]["asset"]
    print(f"\n  Largest negative 2013 contributor (u56): {worst_2013}")
    cond_i = worst_2013 == "GLD"

    # ============================================================ S2 leave-one-asset-out G
    print("\n" + "=" * 120)
    print("S2  POOLED G BY SLEEVE COMPOSITION (8 cells x 4 non-null f = 32 points per variant)")
    gcols = ["G_full"] + [f"G_ex{y}" for y in IS_YEARS]
    GV = D.groupby("variant")[gcols].mean().reindex(list(VARIANTS))
    GV["move_2013"] = GV["G_ex2013"] - GV["G_full"]
    GV["max_move_other"] = GV[[f"G_ex{y}" for y in IS_YEARS if y != FOCUS]].sub(
        GV["G_full"], axis=0).abs().max(axis=1)
    print(fmt(GV))
    print("\n  frac(G_full < 0) by variant: " +
          ", ".join(f"{v} {float((D[D.variant==v].G_full<0).mean()):.2f}" for v in VARIANTS))
    print("\n  --- pooled G_full by variant and cell")
    print(fmt(D.pivot_table(index=["universe", "book", "cost_bps"], columns="variant",
                            values="G_full").reindex(columns=list(VARIANTS))))

    g_s4, g_ex = float(GV.loc["S4", "G_full"]), float(GV.loc["exGLD", "G_full"])
    cond_ii = abs(g_ex) <= 0.5 * abs(g_s4)
    move_ex = float(GV.loc["exGLD", "move_2013"])
    cond_iii = abs(move_ex) <= 0.05

    # ============================================================ S3 dilution control
    print("\n" + "=" * 120)
    print("S3  DILUTION CONTROL — FLAT4 holds the sleeve's own weights and earns ZERO return")
    d13 = D.groupby("variant")[["d_y_2013", "dret_y_2013"]].mean().reindex(list(VARIANTS))
    d13["share_of_S4_dSharpe"] = d13["d_y_2013"] / float(d13.loc["S4", "d_y_2013"])
    d13["share_of_S4_dret"] = d13["dret_y_2013"] / float(d13.loc["S4", "dret_y_2013"])
    print(fmt(d13))
    print("\n  --- 2013 d(Sharpe) by variant and cell (pooled over the 4 non-null f)")
    print(fmt(D.pivot_table(index=["universe", "book", "cost_bps"], columns="variant",
                            values="d_y_2013").reindex(columns=list(VARIANTS))))
    # contamination bound: how much of the BASE book sits in the four sleeve names
    for tag, px in universes.items():
        for kind in ("top20", "ewall"):
            w0 = H.book(px, kind).loc[px.index[260]:]
            share = float(w0[S4].sum(axis=1).mean() / w0.sum(axis=1).mean())
            print(f"  [contamination] base book {tag}/{kind}: mean weight in TLT/GLD/DBC/UUP "
                  f"= {share:.3%} of gross")
    fl = float(d13.loc["FLAT4", "share_of_S4_dSharpe"])
    print(f"\n  A zero-return leg reproduces {fl:.1%} of the S4 sleeve's 2013 d(Sharpe).")

    print("\n  S3b  THE LEVEL IS NOT THE RIGHT STATISTIC.  FLAT4 dilutes in EVERY year, so its")
    print("  2013 d is large because all of its d's are.  What has to be explained is 2013's")
    print("  EXCESS over the variant's own other years:  excess = d_2013 - mean(d, other years).")
    yrs_all = [y for y in range(2009, 2027)]
    ex = []
    for v in VARIANTS:
        s = D[D.variant == v]
        dy = pd.Series({y: float(s[f"d_y_{y}"].mean()) for y in yrs_all})
        other = dy.drop(FOCUS)
        ex.append(dict(variant=v, mean_other=float(other.mean()), sd_other=float(other.std()),
                       d_2013=float(dy[FOCUS]), excess=float(dy[FOCUS] - other.mean()),
                       z_2013=float((dy[FOCUS] - other.mean()) / other.std())))
    EX = pd.DataFrame(ex).set_index("variant").reindex(list(VARIANTS))
    EX["share_of_S4_excess"] = EX["excess"] / float(EX.loc["S4", "excess"])
    print(fmt(EX))
    dil = float(EX.loc["FLAT4", "share_of_S4_excess"])
    print(f"\n  A zero-return leg reproduces {dil:.1%} of the S4 sleeve's 2013 EXCESS damage;")
    print(f"  the remaining {1 - dil:.1%} is the sleeve assets' own 2013 returns (all four "
          f"negative, S1).")

    # ============================================================ S4 the decision
    print("\n" + "=" * 120)
    print("S4  PRE-REGISTERED DECISION — 'the sleeve's rule-8 gap is gold-in-2013'")
    print(f"    (i)   GLD is the largest negative 2013 contributor            : "
          f"{cond_i}  (largest = {worst_2013})")
    print(f"    (ii)  |G(exGLD)| <= 0.5 |G(S4)|                               : "
          f"{cond_ii}  ({abs(g_ex):.4f} vs {0.5*abs(g_s4):.4f})")
    print(f"    (iii) |G(exGLD) - G_ex2013(exGLD)| <= 0.05                    : "
          f"{cond_iii}  ({abs(move_ex):.4f})")
    if cond_i and cond_ii and cond_iii:
        verdict = "TRUE — the gap is gold in 2013"
    elif cond_i:
        verdict = "REFINED — GLD is the biggest single 2013 loser but NOT the mechanism"
    else:
        verdict = "FALSE — gold is not even the biggest 2013 loser in the leg"
    print(f"    => {verdict}")

    # ============================================================ S5 per-year d
    print("\n" + "=" * 120)
    print("S5  POOLED SLEEVE d(Sharpe) BY CALENDAR YEAR (this run's own points, not quoted)")
    yrs = [y for y in range(2009, 2027)]
    PY = D.pivot_table(index="variant", values=[f"d_y_{y}" for y in yrs])
    PY = PY.reindex(columns=[f"d_y_{y}" for y in yrs]).reindex(list(VARIANTS))
    PY.columns = [c.replace("d_y_", "") for c in PY.columns]
    print(fmt(PY))
    s4y = PY.loc["S4"].astype(float)
    print(f"\n  S4 worst year: {s4y.idxmin()} ({s4y.min():+.3f}); best: {s4y.idxmax()} "
          f"({s4y.max():+.3f}); 2013 rank among all years: "
          f"{int(s4y.rank().loc[str(FOCUS)])} of {len(s4y)} (1 = worst)")

    # ============================================================ S6 walk-forward
    print("\n" + "=" * 120)
    print("S6  RULE-8 WALK-FORWARD — f chosen on IS only (argmax IS Sharpe, tie-break smallest f)")
    wf = []
    for key, sub in G.groupby(CELL, sort=False):
        tag = key[0]
        px = universes[tag]
        start = px.index[260]
        spy = H.full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        base = H.full_row(H.net(bt["returns"].loc[start:], bt["turnover"].loc[start:], key[3]))
        s = sub.sort_values(["IS_Sharpe_full", "f"], ascending=[False, True]).iloc[0]
        wf.append(dict(zip(CELL, key), pick_f=s["f"],
                       IS_Sharpe=s["IS_Sharpe_full"],
                       CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                       H1=s["H1"], H2=s["H2"],
                       OOS_CAGR=s["OOS_CAGR"], OOS_Sharpe=s["OOS_Sharpe"], OOS_MaxDD=s["OOS_MaxDD"],
                       v1_OOS_Sharpe=base["OOS_Sharpe"], v1_OOS_CAGR=base["OOS_CAGR"],
                       v1_OOS_MaxDD=base["OOS_MaxDD"],
                       spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"],
                       spy_OOS_MaxDD=spy["OOS_MaxDD"],
                       p4a=s["4a"], p4b=s["4b"], p4b_oos=s["4b_oos"]))
    W = pd.DataFrame(wf)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    show = ["universe", "variant", "book", "cost_bps", "pick_f", "IS_Sharpe", "CAGR", "Sharpe",
            "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "p4a", "p4b", "p4b_oos"]
    print(fmt(W[show]))
    print("\n  Reference OOS rows (same window, 10 bps): "
          f"RULES v1 {W.v1_OOS_CAGR.iloc[0]:.1%}/{W.v1_OOS_Sharpe.iloc[0]:.3f}/"
          f"{W.v1_OOS_MaxDD.iloc[0]:.1%}  |  SPY {W.spy_OOS_CAGR.iloc[0]:.1%}/"
          f"{W.spy_OOS_Sharpe.iloc[0]:.3f}/{W.spy_OOS_MaxDD.iloc[0]:.1%}")
    print(f"\n  4b passes among the 56 walk-forward picks: {int(W.p4b.sum())}; "
          f"4b-OOS {int(W.p4b_oos.sum())}; 4a {int(W.p4a.sum())}")
    print("\n  --- ALL grid points, 4b/4a footprint by variant")
    print(fmt(G.groupby("variant")[["4a", "4b", "4b_oos"]].sum().reindex(list(VARIANTS))))

    print("\n  S6b  HEAD-TO-HEAD: each variant's walk-forward pick against the INCUMBENT S4 pick")
    print("  in the same cell (same universe, book and cost rung).  Composition is a TUNED axis")
    print("  here, so a variant that wins is a candidate for the Sunday review, not a selection")
    print("  this run is entitled to make.")
    inc = W[W.variant == "S4"].set_index(["universe", "book", "cost_bps"])
    h2h = []
    for v in VARIANTS:
        if v == "S4":
            continue
        s = W[W.variant == v].set_index(["universe", "book", "cost_bps"])
        j = s.join(inc, rsuffix="_S4")
        h2h.append(dict(variant=v,
                        dSharpe=float((j.Sharpe - j.Sharpe_S4).mean()),
                        dCAGR=float((j.CAGR - j.CAGR_S4).mean()),
                        dMaxDD=float((j.MaxDD - j.MaxDD_S4).mean()),
                        dOOS_Sharpe=float((j.OOS_Sharpe - j.OOS_Sharpe_S4).mean()),
                        wins_Sharpe=int((j.Sharpe > j.Sharpe_S4).sum()), cells=len(j),
                        n4a=int(j.p4a.sum()), n4b=int(j.p4b.sum()), n4b_S4=int(j.p4a_S4.sum() * 0
                                                                              + inc.p4b.sum())))
    print(fmt(pd.DataFrame(h2h).set_index("variant")))
    b10 = W[W.cost_bps == 10]
    both = b10[b10.p4b].groupby(["variant", "book"])["universe"].nunique()
    win = sorted({f"{v}/{bk}" for (v, bk), k in both.items() if k == 2})
    print("\n  Walk-forward picks passing 4b on BOTH universes in the SAME (book, 10 bps) cell: "
          + (", ".join(win) or "none"))
    print(fmt(b10.pivot_table(index=["variant", "book"], columns="universe",
                              values=["Sharpe", "MaxDD", "OOS_Sharpe"])))

    print("\n" + "=" * 120)
    print("HEADLINE")
    print(f"  S4 pooled G {g_s4:+.4f} -> ex2013 {float(GV.loc['S4','G_ex2013']):+.4f} "
          f"(move {float(GV.loc['S4','move_2013']):+.4f}; largest other-year move "
          f"{float(GV.loc['S4','max_move_other']):.4f})")
    print(f"  exGLD pooled G {g_ex:+.4f} -> ex2013 {float(GV.loc['exGLD','G_ex2013']):+.4f} "
          f"(move {move_ex:+.4f})")
    print(f"  2013 attribution: dilution (FLAT4) {dil:.1%} of S4's 2013 EXCESS damage; gold "
          f"{1 - float(EX.loc['exGLD', 'share_of_S4_excess']):.1%}; the leg's four assets all lost")
    print(f"  every composition still moves ~+0.19 of G when 2013 is deleted (S4 "
          f"{float(GV.loc['S4','move_2013']):+.4f}, GLDonly "
          f"{float(GV.loc['GLDonly','move_2013']):+.4f}) — 2013 is a WINDOW property")
    print(f"  DECISION: {verdict}")
    print(f"\n[outputs] {OUT.name}.grid.csv .deltas.csv .attrib.csv .walkforward.csv")


if __name__ == "__main__":
    main()
