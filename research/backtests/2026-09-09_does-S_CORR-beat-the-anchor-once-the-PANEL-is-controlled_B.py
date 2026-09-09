#!/usr/bin/env python3
"""Idea 309 — does S_CORR beat the anchor once the PANEL is controlled?

THE QUEUE'S CHARGE
------------------
Idea 293 reported that S_CORR (pick the panel with the LOWEST in-sample mean pairwise
correlation) beats the do-nothing anchor in 15 of 18 (stratum x book) cells, and that its
one 4b-clearing pick sits on a panel where the UN-RANKED EWall book and RULES v2 also clear
4b.  That makes the raw score ambiguous: a selector that picks a good PANEL is scored the
same as a selector that picks a panel the RANKING exploits.

Re-score every selector on the EWALL RESIDUAL of OOS Sharpe

    D(panel, book) = book_OOS_Sharpe(panel) - EWall_OOS_Sharpe(panel)

so a selector is credited only for the part of the book's OOS Sharpe that the ranking adds
on top of holding the same panel equal-weighted.  Report which selectors survive.

TWO TUNED PARAMETERS (protocol rule 4, max 2)
---------------------------------------------
    1. STATISTIC : RAW (book OOS Sharpe, idea 293's score) vs RESID (EWall residual)
    2. BLOCK     : A = seeds 0..59   (idea 293's committed panels)
                   B = seeds 100..159 (idea 310's disjoint fresh block)
Everything else — the 9 strata (k x q), the 60 seeds each, the two ranked books, the six
pre-registered selectors and their directions — is inherited verbatim from idea 293 and is
NOT tuned here.  ALL grid points are reported.

DATA
----
No prices are re-simulated.  The two committed panel artefacts are the input:
    research/backtests/2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv
    research/backtests/2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.panelsB.csv
Gates G0-G2 below check them against prices and against idea 293's published numbers before
a single new number is read.

SURVIVORSHIP: every constructed panel is drawn from the current constituents of the small-cap
screen (data/SMALL_PANEL_README.md) plus the large-cap universe; all levels are optimistic.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, backtest, metrics  # noqa

OUT = str(Path(__file__).with_suffix(""))
LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)
def fmt(df): return df.to_string(float_format=lambda x: f"{x:+.4f}")

PANELS_A = ROOT / "research/backtests/2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.panels.csv"
PANELS_B = ROOT / "research/backtests/2026-09-09_is-EVOL-the-real-survivor-not-DISP_B.panelsB.csv"
WF_A     = ROOT / "research/backtests/2026-09-06_does-the-CORR-ordering-hold-off-q-0.5_cloud.walkforward.csv"

KS, QS = (20, 40, 80), (0.25, 0.50, 0.75)
BOOKS = ("CAND10", "CAND20")
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---- pre-registered selectors, verbatim from idea 293 (direction is NOT a free parameter)
SEL = {
    "S_CORR":    ("corr_IS",    "min", "LOWEST IS mean pairwise correlation"),
    "S_DISP":    ("disp_IS",    "max", "HIGHEST IS dispersion"),
    "S_BREADTH": ("breadth_IS", "max", "HIGHEST IS breadth"),
    "S_EVOL":    ("evol_IS",    "min", "LOWEST IS eligible-set vol"),
    "S_EWALL":   ("EWall_IS_Sharpe", "max", "HIGHEST IS EWall Sharpe (panel level, not ranking)"),
}
# S_ISS and S_RESID are book-dependent and added per arm below.


def keep_flags(row, spy_row, v2_row):
    """PROTOCOL rule 4a / 4b, byte-for-byte the predicate idea 293 used."""
    a = bool(row["H1"] > v2_row["H1"] and row["H2"] > v2_row["H2"]
             and row["MaxDD"] >= v2_row["MaxDD"])
    fails = []
    if not row["H1"] > spy_row["H1"]: fails.append("H1")
    if not row["H2"] > spy_row["H2"]: fails.append("H2")
    if not row["OOS_Sharpe"] > spy_row["OOS_Sharpe"]: fails.append("OOS")
    if not abs(row["MaxDD"]) <= 0.60 * abs(spy_row["MaxDD"]): fails.append("DD")
    if not row["CAGR"] >= 0.70 * spy_row["CAGR"]: fails.append("CAGR")
    return a, (len(fails) == 0), (",".join(fails) if fails else "-")


# ==================================================================== gates
def gates():
    P("=" * 100)
    P("GATES — the two committed artefacts are checked before any new number is read")
    P("=" * 100)
    A = pd.read_csv(PANELS_A); B = pd.read_csv(PANELS_B)
    A = A[A.kind != "NAMED"].copy(); A["block"] = "A"
    B = B.copy(); B["block"] = "B"
    P(f"block A {len(A)} constructed panels, seeds {A.seed.min()}..{A.seed.max()}")
    P(f"block B {len(B)} constructed panels, seeds {B.seed.min()}..{B.seed.max()}")
    assert sorted(A.seed.unique()) == list(range(60))
    assert sorted(B.seed.unique()) == list(range(100, 160))
    P("G-SEED: the two blocks are DISJOINT in seed  -> PASS")

    # G0 — SPY, the 4b comparand, recomputed from prices.  Both artefacts price SPY on the
    # SMALL panel's own trading calendar with its own 260-day warm-up (that is the calendar
    # every constructed panel lives on), so that is the calendar the gate must use; the
    # large-cap calendar is printed beside it to show how much the calendar alone is worth.
    def spy_row(series):
        h = len(series) // 2
        return dict(Sharpe=metrics(series)["Sharpe"], CAGR=metrics(series)["CAGR"],
                    MaxDD=metrics(series)["MaxDD"], H1=metrics(series.iloc[:h])["Sharpe"],
                    H2=metrics(series.iloc[h:])["Sharpe"],
                    OOS=metrics(series.loc[OOS_START:])["Sharpe"])
    sp = load_universe(small=True)
    m = spy_row(sp["SPY"].pct_change().fillna(0).loc[sp.index[260]:])
    px = load_universe()
    ml = spy_row(px["SPY"].pct_change().fillna(0).loc[px.index[260]:])
    d = max(abs(A.SPY_Sharpe.mean() - m["Sharpe"]), abs(A.SPY_OOS_Sharpe.mean() - m["OOS"]),
            abs(A.SPY_H1.mean() - m["H1"]), abs(A.SPY_H2.mean() - m["H2"]),
            abs(A.SPY_CAGR.mean() - m["CAGR"]), abs(A.SPY_MaxDD.mean() - m["MaxDD"]))
    P(f"G0  SPY recomputed on the SMALL-panel calendar: Sharpe {m['Sharpe']:.4f} "
      f"(H1 {m['H1']:.4f} / H2 {m['H2']:.4f}) OOS {m['OOS']:.4f} CAGR {m['CAGR']:.4%} "
      f"MaxDD {m['MaxDD']:.4%}")
    P(f"    committed in both artefacts:            Sharpe {A.SPY_Sharpe.mean():.4f} "
      f"(H1 {A.SPY_H1.mean():.4f} / H2 {A.SPY_H2.mean():.4f}) OOS "
      f"{A.SPY_OOS_Sharpe.mean():.4f} CAGR {A.SPY_CAGR.mean():.4%} "
      f"MaxDD {A.SPY_MaxDD.mean():.4%}")
    P(f"    max |committed - recomputed| over 6 SPY columns = {d:.3e}  -> "
      f"{'PASS' if d < 5e-4 else 'FAIL'}  (a data-vintage sliver: data/prices.csv was "
      f"refreshed after both artefacts were written)")
    P(f"    for reference the LARGE-cap calendar gives Sharpe {ml['Sharpe']:.4f} / OOS "
      f"{ml['OOS']:.4f} / CAGR {ml['CAGR']:.4%} — the calendar alone is worth "
      f"{abs(ml['Sharpe'] - m['Sharpe']):.4f} Sharpe, which is why the 4b bar here is the "
      f"small-calendar SPY and NOT the large-cap one quoted elsewhere in the record")

    # G1 — idea 293's published S_CORR raw edge over the anchor, recomputed here
    raw = []
    for k in KS:
        for q in QS:
            dd = A[A.kind == f"k{k:02d}q{q:.3f}"]
            for arm in BOOKS:
                pick = dd.loc[dd["corr_IS"].idxmin()]
                raw.append(dict(book=arm, edge=pick[f"{arm}_OOS_Sharpe"]
                                - dd[f"{arm}_OOS_Sharpe"].mean()))
    r = pd.DataFrame(raw).groupby("book").edge.agg(["mean", lambda s: (s > 0).sum()])
    P(f"G1  S_CORR raw edge over the anchor, recomputed from the committed panels:")
    P(f"    CAND10 mean {r.loc['CAND10','mean']:+.4f} (published +0.1456), "
      f"CAND20 mean {r.loc['CAND20','mean']:+.4f} (published +0.1430); "
      f"wins {int(r['<lambda_0>'].sum())}/18 (published 15/18)")
    g1 = max(abs(r.loc["CAND10", "mean"] - 0.1456), abs(r.loc["CAND20", "mean"] - 0.1430))
    P(f"    max |d| vs the published means = {g1:.3e}  -> {'PASS' if g1 < 5e-5 else 'FAIL'}"
      f"; win count {'MATCHES' if int(r['<lambda_0>'].sum()) == 15 else 'DIFFERS'}")

    # G2 — the same numbers against idea 293's own committed walkforward.csv
    w = pd.read_csv(WF_A)
    sc = w[(w.rule == "S_CORR")].set_index(["k", "q", "book"]).vs_anchor
    mine = pd.DataFrame(
        [dict(k=k, q=q, book=arm,
              v=A[A.kind == f"k{k:02d}q{q:.3f}"].loc[
                  A[A.kind == f"k{k:02d}q{q:.3f}"]["corr_IS"].idxmin(), f"{arm}_OOS_Sharpe"]
              - A[A.kind == f"k{k:02d}q{q:.3f}"][f"{arm}_OOS_Sharpe"].mean())
         for k in KS for q in QS for arm in BOOKS]).set_index(["k", "q", "book"]).v
    g2 = float((sc - mine).abs().max())
    P(f"G2  vs idea 293's committed .walkforward.csv vs_anchor, 18 cells: max |d| = {g2:.3e}"
      f"  -> {'PASS' if g2 < 1e-9 else 'FAIL'}")
    return pd.concat([A, B], ignore_index=True)


# ==================================================================== the residual itself
def residual_level(panels):
    P("\n" + "=" * 100)
    P("STEP 1 — WHAT IS THERE TO SELECT ON?  the EWall residual's own level, per stratum")
    P("=" * 100)
    P("D = book OOS Sharpe - EWall OOS Sharpe on the SAME panel.  If D's mean is <= 0 the")
    P("ranking subtracts value on average and no selector can be credited for exploiting it.")
    rows = []
    for blk in ("A", "B"):
        for k in KS:
            for q in QS:
                dd = panels[(panels.block == blk) & (panels.kind == f"k{k:02d}q{q:.3f}")]
                for arm in BOOKS:
                    D = dd[f"{arm}_OOS_Sharpe"] - dd["EWall_OOS_Sharpe"]
                    rows.append(dict(block=blk, k=k, q=q, book=arm, n=len(D),
                                     D_mean=D.mean(), D_sd=D.std(), D_min=D.min(),
                                     D_max=D.max(), share_pos=(D > 0).mean(),
                                     t=D.mean() / (D.std() / np.sqrt(len(D))),
                                     raw_mean=dd[f"{arm}_OOS_Sharpe"].mean(),
                                     ewall_mean=dd["EWall_OOS_Sharpe"].mean()))
    lev = pd.DataFrame(rows)
    lev.to_csv(f"{OUT}.residual_level.csv", index=False)
    P("\nALL 36 (block x stratum x book) points:")
    P(lev.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    P(f"\nPooled: mean D = {lev.D_mean.mean():+.4f}; D_mean > 0 in "
      f"{(lev.D_mean > 0).sum()}/36 cells; panel-level share of positive D = "
      f"{lev.share_pos.mean():.3f}")
    for arm in BOOKS:
        s = lev[lev.book == arm]
        P(f"  {arm}: mean D {s.D_mean.mean():+.4f}, positive in {(s.D_mean>0).sum()}/18, "
          f"|t| >= 2 in {(s.t.abs()>=2).sum()}/18, mean seed sd {s.D_sd.mean():.4f}")
    return lev


# ==================================================================== selectors, both scores
def score_selectors(panels):
    P("\n" + "=" * 100)
    P("STEP 2 — EVERY SELECTOR RE-SCORED ON BOTH STATISTICS, ALL GRID POINTS")
    P("=" * 100)
    P("Each selector picks ONE panel of the 60 in a stratum on an IS (<=2016) statistic only;")
    P("the OOS (>=2017) score is read once.  Anchor = mean of the same score over all 60.")
    P("Reverse directions are carried as sign checks.  rank = the pick's rank of 60 on the")
    P("score, 1 = best (a uniform draw has mean rank 30.5).")
    rows = []
    for blk in ("A", "B"):
        for k in KS:
            for q in QS:
                dd = panels[(panels.block == blk)
                            & (panels.kind == f"k{k:02d}q{q:.3f}")].copy()
                for arm in BOOKS:
                    dd = dd.dropna(subset=[f"{arm}_OOS_Sharpe", "EWall_OOS_Sharpe"])
                    RAW = dd[f"{arm}_OOS_Sharpe"]
                    RES = RAW - dd["EWall_OOS_Sharpe"]
                    sels = dict(SEL)
                    sels["S_ISS"] = (f"{arm}_IS_Sharpe", "max", "HIGHEST IS Sharpe of the book")
                    # the residual-native selector: pick where the RANKING beat EWall in-sample
                    dd["_residIS"] = dd[f"{arm}_IS_Sharpe"] - dd["EWall_IS_Sharpe"]
                    sels["S_RESID"] = ("_residIS", "max",
                                       "HIGHEST IS (book - EWall) Sharpe, the residual's own selector")
                    for nm, (col, direction, desc) in sels.items():
                        for lbl, dr in ((nm, direction),
                                        (nm + "^rev", "min" if direction == "max" else "max")):
                            i = dd[col].idxmax() if dr == "max" else dd[col].idxmin()
                            pick = dd.loc[i]
                            _, kb, fails = keep_flags(
                                {x: pick[f"{arm}_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                                {x: pick[f"SPY_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                                {x: pick[f"v2_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")})
                            ea, ekb, _ = keep_flags(
                                {x: pick[f"EWall_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                                {x: pick[f"SPY_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")},
                                {x: pick[f"v2_{x}"] for x in
                                 ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")})
                            rows.append(dict(
                                block=blk, k=k, q=q, book=arm, rule=lbl,
                                prereg=desc if lbl == nm else "sign check",
                                pick=pick["panel"],
                                RAW=RAW.loc[i], RAW_anchor=RAW.mean(),
                                RAW_edge=RAW.loc[i] - RAW.mean(),
                                RAW_rank=int(RAW.rank(ascending=False).loc[i]),
                                RES=RES.loc[i], RES_anchor=RES.mean(),
                                RES_edge=RES.loc[i] - RES.mean(),
                                RES_rank=int(RES.rank(ascending=False).loc[i]),
                                ewall_oos=pick["EWall_OOS_Sharpe"],
                                OOS_CAGR=pick[f"{arm}_OOS_CAGR"],
                                OOS_MaxDD=pick[f"{arm}_OOS_MaxDD"],
                                spy_oos=pick["SPY_OOS_Sharpe"], v2_oos=pick["v2_OOS_Sharpe"],
                                keep4b=kb, keep4a_ewall=ea, ewall_keep4b=ekb, fails4b=fails,
                                seed_sd=RAW.std(), res_sd=RES.std()))
                    rows.append(dict(block=blk, k=k, q=q, book=arm,
                                     rule="ANCHOR (do nothing, mean of 60)", prereg="control",
                                     pick="-", RAW=RAW.mean(), RAW_anchor=RAW.mean(),
                                     RAW_edge=0.0, RAW_rank=-1, RES=RES.mean(),
                                     RES_anchor=RES.mean(), RES_edge=0.0, RES_rank=-1,
                                     ewall_oos=dd["EWall_OOS_Sharpe"].mean(),
                                     OOS_CAGR=dd[f"{arm}_OOS_CAGR"].mean(),
                                     OOS_MaxDD=dd[f"{arm}_OOS_MaxDD"].mean(),
                                     spy_oos=dd["SPY_OOS_Sharpe"].mean(),
                                     v2_oos=dd["v2_OOS_Sharpe"].mean(),
                                     keep4b=False, keep4a_ewall=False, ewall_keep4b=False,
                                     fails4b="n/a (mean)", seed_sd=RAW.std(), res_sd=RES.std()))
    wf = pd.DataFrame(rows)
    wf.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(f"\n{len(wf)} selector-cell rows written ({len(wf[wf.rule.str.contains('ANCHOR')])} anchors, "
      f"{len(wf) - len(wf[wf.rule.str.contains('ANCHOR')])} picks) — every grid point in "
      f"{Path(OUT).name}.walkforward.csv")
    return wf


def survivors(wf):
    P("\n" + "=" * 100)
    P("STEP 3 — WHICH SELECTORS SURVIVE THE CONTROL")
    P("=" * 100)
    prime = wf[(~wf.rule.str.contains("\\^rev")) & (~wf.rule.str.contains("ANCHOR"))]
    P("\nPRE-REGISTERED BARS (fixed before the residual numbers were read):")
    P("  B1  mean edge over the anchor > 0 in BOTH blocks")
    P("  B2  edge > 0 in >= 14 of 18 (stratum x book) cells in BOTH blocks  (idea 293's")
    P("      headline for S_CORR on RAW was 15/18 in block A; 14/18 is p<0.05 one-sided")
    P("      against a fair coin, so it is the weakest count that is not chance)")
    P("  B3  the reverse direction is WORSE than the forward one in BOTH blocks (sign check)")
    P("  A selector SURVIVES the control only if it clears B1+B2+B3 on the RESID statistic.")

    out = []
    for stat in ("RAW", "RES"):
        for rule in sorted(prime.rule.unique()):
            r = {}
            for blk in ("A", "B"):
                s = prime[(prime.rule == rule) & (prime.block == blk)]
                rv = wf[(wf.rule == rule + "^rev") & (wf.block == blk)]
                r[blk] = dict(mean=s[f"{stat}_edge"].mean(),
                              wins=int((s[f"{stat}_edge"] > 0).sum()), n=len(s),
                              rev=rv[f"{stat}_edge"].mean(),
                              mrank=s[f"{stat}_rank"].mean())
            b1 = r["A"]["mean"] > 0 and r["B"]["mean"] > 0
            b2 = r["A"]["wins"] >= 14 and r["B"]["wins"] >= 14
            b3 = r["A"]["mean"] > r["A"]["rev"] and r["B"]["mean"] > r["B"]["rev"]
            out.append(dict(stat=stat, rule=rule,
                            A_mean=r["A"]["mean"], A_wins=f"{r['A']['wins']}/18",
                            A_rev=r["A"]["rev"], A_meanrank=r["A"]["mrank"],
                            B_mean=r["B"]["mean"], B_wins=f"{r['B']['wins']}/18",
                            B_rev=r["B"]["rev"], B_meanrank=r["B"]["mrank"],
                            B1=b1, B2=b2, B3=b3, SURVIVES=(b1 and b2 and b3)))
    su = pd.DataFrame(out)
    su.to_csv(f"{OUT}.survivors.csv", index=False)
    for stat, ttl in (("RAW", "idea 293's SCORE (book OOS Sharpe)"),
                      ("RES", "THE CONTROLLED SCORE (book OOS Sharpe - EWall OOS Sharpe)")):
        P(f"\n--- {stat}: {ttl} ---   (a uniform draw has mean rank 30.5 of 60)")
        P(su[su.stat == stat].drop(columns="stat").to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))
    P("\nSURVIVORS on RAW : " + (", ".join(su[(su.stat == "RAW") & su.SURVIVES].rule) or "NONE"))
    P("SURVIVORS on RESID: " + (", ".join(su[(su.stat == "RES") & su.SURVIVES].rule) or "NONE"))

    P("\nS_CORR, the queue's subject, cell by cell (edge over the anchor):")
    for stat in ("RAW", "RES"):
        t = prime[prime.rule == "S_CORR"].pivot_table(index=["block", "k", "q"],
                                                      columns="book", values=f"{stat}_edge")
        P(f"  [{stat}]"); P(fmt(t))

    # permutation test: is the pick's rank better than a uniform draw?
    P("\nPERMUTATION TEST — under the null the pick is a uniform draw of the 60, so its rank")
    P("is uniform on 1..60 (mean 30.5, sd 17.32).  z = (30.5 - mean rank) * sqrt(m) / 17.32")
    P("over the m=18 cells of a block; positive z = better than a random draw.")
    pr = []
    for stat in ("RAW", "RES"):
        for rule in sorted(prime.rule.unique()):
            for blk in ("A", "B"):
                s = prime[(prime.rule == rule) & (prime.block == blk)]
                mr = s[f"{stat}_rank"].mean()
                z = (30.5 - mr) * np.sqrt(len(s)) / (np.sqrt((60 ** 2 - 1) / 12))
                pr.append(dict(stat=stat, rule=rule, block=blk, mean_rank=mr, z=z))
    prd = pd.DataFrame(pr)
    P(prd.pivot_table(index="rule", columns=["stat", "block"], values="z").to_string(
        float_format=lambda x: f"{x:+.2f}"))
    P("(|z| > 1.96 is the 5% two-sided bar)")
    prd.to_csv(f"{OUT}.permutation.csv", index=False)
    return su, prime


def four_b_footprint(wf, panels):
    P("\n" + "=" * 100)
    P("STEP 4 — THE QUEUE'S SECOND CLAIM: is a 4b pass the PANEL's or the RANKING's?")
    P("=" * 100)
    rows = []
    for _, d in panels.iterrows():
        spy = {x: d[f"SPY_{x}"] for x in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}
        v2 = {x: d[f"v2_{x}"] for x in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}
        ea, eb, _ = keep_flags({x: d[f"EWall_{x}"] for x in spy}, spy, v2)
        for arm in BOOKS + ("EWall",):
            a, b, f = keep_flags({x: d[f"{arm}_{x}"] for x in spy}, spy, v2)
            rows.append(dict(block=d["block"], k=d["k"], q=d["q"], seed=d["seed"], book=arm,
                             keep4a=a, keep4b=b, fails=f, ewall_keep4b=eb,
                             D=d[f"{arm}_OOS_Sharpe"] - d["EWall_OOS_Sharpe"]))
    kp = pd.DataFrame(rows)
    kp.to_csv(f"{OUT}.keeppaths.csv", index=False)
    n = len(kp)
    P(f"\nBOTH KEEP PATHS over ALL {n} panel-books "
      f"({len(panels)} panels x 3 arms, no selection):")
    P(f"  4a (beat RULES v2 in both halves, MaxDD no worse): {int(kp.keep4a.sum())}/{n} "
      f"({kp.keep4a.mean():.2%})")
    P(f"  4b (beat SPY H1+H2+OOS, DD <= 60% SPY, CAGR >= 70% SPY): {int(kp.keep4b.sum())}/{n} "
      f"({kp.keep4b.mean():.2%})")
    P(f"  BOTH: {int((kp.keep4a & kp.keep4b).sum())}/{n}")
    P("\n4b count by arm and stratum (ALL grid points):")
    P(kp.pivot_table(index=["block", "k", "q"], columns="book", values="keep4b",
                     aggfunc="sum").to_string())
    P("\n4b binding bars over the failures:")
    fc = kp[~kp.keep4b].fails.str.split(",").explode().value_counts()
    P(fc.to_string())

    rk = kp[kp.book != "EWall"]
    p4 = rk[rk.keep4b]
    P(f"\nTHE DECOMPOSITION.  Of the {len(p4)} ranked-book 4b passes:")
    P(f"  {int(p4.ewall_keep4b.sum())} sit on a panel whose UN-RANKED EWall book ALSO clears 4b "
      f"({p4.ewall_keep4b.mean():.1%}) — the pass is the PANEL's")
    P(f"  {int((~p4.ewall_keep4b).sum())} sit on a panel where EWall does NOT clear 4b "
      f"— the only candidates for a pass the RANKING earns")
    P(f"  of those, {int(((~p4.ewall_keep4b) & (p4.D > 0)).sum())} also have a POSITIVE EWall "
      f"residual (the book actually out-Sharpes its own panel OOS)")
    P(f"  base rate of 4b among EWall books alone: "
      f"{int(kp[kp.book=='EWall'].keep4b.sum())}/{len(kp[kp.book=='EWall'])} "
      f"({kp[kp.book=='EWall'].keep4b.mean():.2%})")

    sp = wf[(~wf.rule.str.contains("ANCHOR"))]
    P(f"\nAmong the {len(sp)} SELECTOR PICKS: {int(sp.keep4b.sum())} clear 4b, of which "
      f"{int(sp[sp.keep4b].ewall_keep4b.sum())} sit on a panel whose EWall also clears 4b.")
    if sp.keep4b.any():
        P(sp[sp.keep4b][["block", "k", "q", "book", "rule", "pick", "RAW", "ewall_oos", "RES",
                         "OOS_CAGR", "OOS_MaxDD", "spy_oos", "ewall_keep4b"]].to_string(
            index=False, float_format=lambda x: f"{x:+.4f}"))
    return kp


def headline(wf, lev, su, kp):
    P("\n" + "=" * 100)
    P("STEP 5 — RULE 8 HEADLINE: the picks priced against SPY and the LIVE RULES v2")
    P("=" * 100)
    prime = wf[(~wf.rule.str.contains("\\^rev")) & (~wf.rule.str.contains("ANCHOR"))]
    anc = wf[wf.rule.str.contains("ANCHOR")]
    P(f"\nComparands (mean over cells): SPY OOS Sharpe {anc.spy_oos.mean():.4f}, "
      f"RULES v2 OOS Sharpe {anc.v2_oos.mean():.4f}, do-nothing anchor OOS Sharpe "
      f"{anc.RAW.mean():.4f}, EWall OOS Sharpe {anc.ewall_oos.mean():.4f}")
    t = prime.groupby("rule").agg(
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("RAW", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), resid=("RES", "mean"),
        beats_SPY=("RAW", lambda s: 0), )
    bs = prime.assign(bspy=prime.RAW > prime.spy_oos, bv2=prime.RAW > prime.v2_oos,
                      banc=prime.RAW_edge > 0, bres=prime.RES_edge > 0).groupby("rule")[
        ["bspy", "bv2", "banc", "bres"]].sum()
    t = t.drop(columns="beats_SPY").join(bs)
    t.columns = ["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "mean_resid",
                 "beats_SPY/36", "beats_v2/36", "beats_anchor_RAW/36", "beats_anchor_RES/36"]
    P("\nEvery pre-registered selector, pooled over both blocks (36 cells each):")
    P(t.to_string(float_format=lambda x: f"{x:+.4f}"))
    P(f"\nSPY OOS CAGR {anc.OOS_CAGR.mean():.4%} is NOT the row above — the panel books' own "
      f"OOS CAGR is shown; SPY's OOS CAGR from the artefacts is "
      f"{pd.read_csv(PANELS_B).SPY_OOS_CAGR.mean():.4%}, MaxDD "
      f"{pd.read_csv(PANELS_B).SPY_OOS_MaxDD.mean():.4%}.")


def main():
    panels = gates()
    lev = residual_level(panels)
    wf = score_selectors(panels)
    su, prime = survivors(wf)
    kp = four_b_footprint(wf, panels)
    headline(wf, lev, su, kp)
    P("\n" + "=" * 100)
    P("SURVIVORSHIP: constructed panels are drawn from CURRENT constituents of the small-cap")
    P("screen and the large-cap universe; every level quoted here is optimistic.  The object")
    P("under test is a SELECTOR over panels, not a book — no RULES change is proposed.")
    P("=" * 100)
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
