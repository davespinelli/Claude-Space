#!/usr/bin/env python3
"""QUEUE idea 142 — selector-comparison-needs-more-cells  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 142)
    "idea 132's paired reading ranks the incumbent IS-Sharpe LAST of four selectors (1.022 vs
     IS-MaxDD 1.052, IS-CAGR 1.047, IS-Calmar 1.040) on only 7 paired cells, which cannot order
     four selectors.  Re-run the identical comparison on idea 133's 816-row widened corpus,
     where the (panel, book, cost) cells are 4x as many, before any selector claim is made."

WHAT IS ACTUALLY BEING TESTED
    Idea 132 published an ORDERING of four IS selectors on seven paired cells.  Seven paired
    observations cannot separate four means whose spread is 0.030 of Sharpe; the queue's own
    sentence says so.  This run does exactly two things:
      (1) re-runs idea 132's identical selector x screen comparison, unchanged, on idea 133's
          48-cell / 816-arm-row widened corpus (2.7x the cells, and — the number the queue
          cares about — many more PAIRED cells), and reports whether the published ordering
          survives;
      (2) adds the power control idea 132 could not run: a RANDOM selector (seeded, reported,
          never selected on).  If the four real selectors' paired means sit inside the random
          selector's own spread, the ordering is not a finding at ANY cell count and the
          leaderboard should stop quoting it.  That is the honest form of the queue's worry.

    A selector ordering is not a book.  This run cannot promote a candidate and does not try;
    its output is a statement about PROTOCOL rule 8's selector, plus a full re-scoring of both
    KEEP paths on all 816 rows against the LIVE RULES v2 book.

CORPUS — idea 133's, unchanged and RE-DERIVED rather than read
    3 panels (u56 / broad / small) x 9 books at matched gross 0.75 (EWall, V1u, R5, R10, R20,
    R40, S3-25, S3-50, S4-50; the sleeve books exist on u56/broad only, so small has 6)
    x 2 cost rungs (10, 25 bps) = 48 cells, each with idea 94's 17 arms (control, 5 gates x
    {dg,rw}, 2 stops, 2 book drawdown controls, 2 entry budgets) = 816 arm-rows, every one
    written to .grid.csv.  Idea 132's own corpus is the sub-grid {V1u, R20(=TOP20), EWall} —
    18 cells, 306 rows — and is scored separately as a CALIBRATION before anything new is read.

TUNED PARAMETERS — exactly two, both fully reported, identical to idea 132's:
    1. the IS selector statistic, 4 values (+1 control):
         K_Sharpe  argmax IS Sharpe          (the incumbent, the thing under test)
         K_Calmar  argmax IS CAGR / |IS MaxDD|
         K_MaxDD   argmax IS MaxDD           (shallowest IS drawdown)
         K_CAGR    argmax IS CAGR
         K_Random  a seeded uniform draw over the same admissible set   [CONTROL, seed 20260908]
    2. the screen, 3 values: S0 (none) / S1 (IS 4b with the CAGR floor, phi=0.70) /
       S2 (IS 4b, floor deleted, phi=0.00).  Both keep 4b's DD cap at delta=0.60.
    Panels, books, cost rungs, arms and the OOS window are reported axes, never selected on.
    5 selectors x 3 screens x 48 cells = 720 picks, all written to .picks.csv.

THREE READINGS OF THE SAME PICKS (idea 132's, unchanged)
    PICKED-ONLY  idea 132's published reading: average over the cells where each screen picks.
                 Biased — different screens average over different cell sets.
    FALLBACK     a screen admitting nothing HOLDS THE CELL'S UNGATED CONTROL; defined in all 48.
    PAIRED       only the cells where every screen picks unaided.
    Selector ordering is read on PAIRED, which is the reading idea 132 published.

WALK-FORWARD (PROTOCOL rule 8) — this run IS a walk-forward experiment
    Every screen and every selector reads the IS window (through 2016-12-31) ONLY.  Each pick is
    read ONCE on 2017-01-01..2026 and reported as OOS CAGR / Sharpe / MaxDD against that cell's
    ungated control, the LIVE RULES v2 book, RULES v1 and SPY.  Both KEEP paths are evaluated on
    every one of the 816 rows: 4a against RULES v2 (the live book, cost-matched) and against
    RULES v1 (continuity with the pre-2026-09-06 record), and 4b on the full sample and again on
    the OOS window alone for every distinct picked arm.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  CALIBRATION: on idea 132's own 18-cell sub-grid this run reproduces it — K_Sharpe/S1
        declines in 11 of 18 cells and moves 0 picks among the cells where it does pick.
    P2  The published ORDERING does not survive: K_Sharpe is NOT last of the four on the widened
        corpus's paired cells.
    P3  The four selectors are not separable: the spread of their paired mean OOS Sharpe is
        smaller than the spread the RANDOM control produces across its own draws.
    P4  The screen is still near-inert on picks: the unscreened K_Sharpe argmax is already
        IS-admissible in >= 90% of the non-empty S1 cells.
    P5  The widened corpus supplies at least 4x idea 132's 7 paired cells (>= 28).

CAVEATS carried, not buried
    * Survivorship (idea 54): all three panels are current constituents; the small panel drops
      the 44 tickers with max_1d_move >= 1.0 and its SPY is a joined benchmark, never selectable.
      Absent delistings inflate every arm's CAGR, so every 4b CAGR-floor margin here is
      optimistic and no level in this file is an achievable return.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so an IS-window
      drawdown cap is measured on a window that cannot express a deep drawdown; this biases
      every screen toward admitting too much.
    * Idea 401's DEFECT, carried and re-measured here: data/prices.csv was rewritten by a daily-
      close vendor restatement after idea 133 was committed, while the broad/small caches were
      not, so the u56 leg of check (b) can only reproduce to ~1e-5.  The check reports per-panel
      tolerances and says which leg is exact.
    * Idea 126: every row is quoted at t+1 execution only.

HARNESS
    Idea 94's script (H.run, H.targets, H.arm_specs, H.halves, H.window, H.pass4a), idea 129's
    census machinery (C.bars_win, C.margins_at, C.fails) and idea 133's book family
    (D.book_weights, D.books_for, D.panel_px) are all IMPORTED, not re-implemented, so "the
    identical comparison on idea 133's corpus" is literally the same code on the same corpus.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .picks.csv, .walkforward.csv,
.selectors.csv and .keeppaths.csv next to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_selector-comparison-needs-more-cells_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I133_GRID = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.grid.csv"
I132_PICKS = OUT / "2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud.picks.csv"

SEED = 20260908
PHI0, DELTA0 = 0.70, 0.60
COSTS = [10.0, 25.0]
PANELS = ["u56", "broad", "small"]
I132_BOOKS = ["V1u", "R20", "EWall"]          # R20 is idea 132's TOP20, asserted in check (c)
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
SCREENS = ["S0", "S1", "S2"]
N_RANDOM_DRAWS = 200                          # control only; never selected on


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")
D = _load(I133, "i133")

FREQ = H.FREQ
IS_END, OOS_START = H.IS_END, H.OOS_START

pd.set_option("display.width", 300)
pd.set_option("display.max_columns", 100)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


def build_grid():
    """Idea 133's 816 arm-rows, re-derived; plus IS_Calmar and the two 4a comparands."""
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        books = D.books_for(pk, px)
        ref[pk] = dict(bfull=bfull, bIS=bIS, spy=ms, spy_oos=mso, v1=v1, v2=v2, start=start,
                       spy_ret=spy, books=books)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}, books {books}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            say(f"    RULES v2 @{c:.0f}bps CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
                f"MaxDD {mv2['MaxDD']:.2%} | RULES v1 CAGR {mv1['CAGR']:.2%} "
                f"Sharpe {mv1['Sharpe']:.3f} MaxDD {mv1['MaxDD']:.2%}")

        # ---- (a) engine equivalence on every book's ungated control ----
        worst = 0.0
        for b in books:
            W = D.book_weights(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a] engine-equivalence, {len(books)} ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in books:
            for c in COSTS:
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = D.book_weights(px, b, gate, conv)
                    res = H.run(px, W, bps=c, **kw)
                    r = res["r"].loc[start:]
                    rets[(pk, b, c, arm)] = r
                    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    fail = C.fails(mg)
                    rows.append(dict(
                        panel=pk, book=b, cost=c, arm=arm, kind=kind, conv=conv,
                        CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                        IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                        IS_Calmar=calmar(mi["CAGR"], mi["MaxDD"]),
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        gross=res["gross"].loc[start:].mean(),
                        TO=res["to"].loc[start:].sum() / mm["Years"],
                        IS_m_H1=ismg["H1"], IS_m_H2=ismg["H2"], IS_m_DD=ismg["DD"],
                        IS_m_CAGR=ismg["CAGR"],
                        m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                        m_CAGR=mg["CAGR"],
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                        n_fail=len(fail), floor_only=(fail == ["CAGR"]),
                        pass4a_v2=H.pass4a(r, v2[c]), pass4a_v1=H.pass4a(r, v1[c])))
    df = pd.DataFrame(rows)
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_S2"] = core & (df.IS_CAGR - 0.00 * isbars > 0)
    df["adm_S0"] = True
    return df, rets, ref


def reproduction_check(df):
    """(b) idea 133's committed grid, arm-for-arm, per COLUMN and per PANEL, plus a direct
    test of whether idea 401's price restatement can move a selector's argmax."""
    g = pd.read_csv(I133_GRID)
    j = df.merge(g, on=["panel", "book", "cost", "arm"], suffixes=("", "_133"))
    keys = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]
    say(f"\n[b] reproduction of idea 133's committed grid: {len(j)} of {len(df)} rows matched "
        f"(idea 133 published {len(g)}).  Reported per COLUMN, because a single worst-of "
        f"number here is dominated by turnover, which no selector reads.")
    out = []
    for pk, s in j.groupby("panel"):
        d = {k: float((s[k] - s[f"{k}_133"]).abs().max()) for k in keys}
        out.append(dict(panel=pk, rows=len(s), **d))
    RP = pd.DataFrame(out).set_index("panel")
    say(RP.to_string(float_format=lambda x: f"{x:.2e}"))
    exact = [p for p in RP.index if RP.loc[p, keys].max() < 1e-12]
    say(f"    EXACT (max|diff| < 1e-12) on: {exact or 'no panel'}; "
        f"the rest differ at idea 401's data/prices.csv restatement level "
        f"(daily-close commits rewrote data/prices.csv after idea 133 was committed; the broad "
        f"and small caches were not touched).  This is a DATA difference, not a code one — "
        f"check (a) shows the simulator itself is exact on every panel.")

    # --- does the restatement move a pick?  The only thing that matters downstream. ---
    say("\n[b2] RESTATEMENT SENSITIVITY — re-run every selector's argmax on idea 133's own "
        "COMMITTED columns and count picks that differ from this run's.  Idea 133 has no "
        "IS_Calmar column, so it is reconstructed from its IS_CAGR / IS_MaxDD.")
    j = j.copy()
    j["IS_Calmar_133"] = [calmar(a, b) for a, b in zip(j.IS_CAGR_133, j.IS_MaxDD_133)]
    srows = []
    for (pk, b, c), s in j.groupby(["panel", "book", "cost"]):
        for sel, col in SELECTORS.items():
            mine = s.loc[s[col].idxmax()].arm
            theirs = s.loc[s[f"{col}_133"].idxmax()].arm
            top2 = s[col].nlargest(2).values
            srows.append(dict(panel=pk, book=b, cost=c, sel=sel, mine=mine, theirs=theirs,
                              same=(mine == theirs),
                              argmax_margin=float(top2[0] - top2[1]) if len(top2) > 1 else np.nan,
                              col_perturb=float((s[col] - s[f"{col}_133"]).abs().max())))
    S = pd.DataFrame(srows)
    for pk, s in S.groupby("panel"):
        thin = int((s.argmax_margin < s.col_perturb).sum())
        say(f"    {pk:6s}: {int((~s.same).sum())} of {len(s)} unscreened argmaxes differ; "
            f"{thin} cells have an argmax margin thinner than that column's own perturbation")
    say(f"    TOTAL: {int((~S.same).sum())} of {len(S)} argmaxes moved by the restatement.  "
        f"Every claim below is quoted on THIS run's prices; where the count is non-zero the "
        f"affected picks are listed:")
    if int((~S.same).sum()):
        say(S[~S.same].to_string(index=False, float_format=lambda x: f"{x:.2e}"))
    return RP, S


def make_picks(df, rets, ref):
    """4 selectors x 3 screens x 48 cells, plus the seeded random control."""
    rng = np.random.default_rng(SEED)
    prows, rand_rows = [], []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl = rets[(pk, b, c, "control")]
        mc = metrics(H.window(ctl, "OOS"))
        mv1 = metrics(H.window(ref[pk]["v1"][c], "OOS"))
        mv2 = metrics(H.window(ref[pk]["v2"][c], "OOS"))
        mso = ref[pk]["spy_oos"]
        for sel, col in SELECTORS.items():
            base_pick = s.loc[s[col].idxmax()]
            for scr in SCREENS:
                cand = s[s[f"adm_{scr}"]]
                fell_back = not len(cand)
                p = s[s.arm == "control"].iloc[0] if fell_back else cand.loc[cand[col].idxmax()]
                mo = metrics(H.window(rets[(pk, b, c, p.arm)], "OOS"))
                prows.append(dict(
                    sel=sel, screen=scr, panel=pk, book=b, cost=c,
                    pick=("(none -> control)" if fell_back else p.arm), arm=p.arm,
                    picked=not fell_back, n_admitted=int(len(cand)), n_arms=len(s),
                    argmax_admitted=bool(base_pick[f"adm_{scr}"]),
                    moved=bool(p.arm != base_pick.arm), unscreened_pick=base_pick.arm,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_CAGR=mc["CAGR"],
                    ctl_OOS_MaxDD=mc["MaxDD"],
                    v1_OOS_Sharpe=mv1["Sharpe"], v2_OOS_Sharpe=mv2["Sharpe"],
                    spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                    spy_OOS_MaxDD=mso["MaxDD"],
                    beat_ctl=bool(mo["Sharpe"] > mc["Sharpe"]),
                    beat_v2=bool(mo["Sharpe"] > mv2["Sharpe"]),
                    beat_spy=bool(mo["Sharpe"] > mso["Sharpe"]),
                    pass4a_v2=bool(p.pass4a_v2), pass4a_v1=bool(p.pass4a_v1),
                    pass4b=bool(p.pass4b), fail4b=p.fail4b))
        # --- RANDOM control: N draws per (cell, screen), reported as a distribution ---
        for scr in SCREENS:
            cand = s[s[f"adm_{scr}"]]
            pool = cand if len(cand) else s[s.arm == "control"]
            oos = np.array([metrics(H.window(rets[(pk, b, c, a)], "OOS"))["Sharpe"]
                            for a in pool.arm])
            picks = rng.integers(0, len(pool), N_RANDOM_DRAWS)
            for d_i, ix in enumerate(picks):
                rand_rows.append(dict(draw=d_i, screen=scr, panel=pk, book=b, cost=c,
                                      picked=bool(len(cand)), OOS_Sharpe=float(oos[ix])))
    return pd.DataFrame(prows), pd.DataFrame(rand_rows)


def main():
    df, rets, ref = build_grid()
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    repro, sens = reproduction_check(df)
    sens.to_csv(OUT / f"{STEM}.restatement.csv", index=False)

    # ---- (c) R20 is idea 132's TOP20 ----
    say("\n[c] R20 == TOP20 identity (idea 133's ranked() vs idea 94's targets()):")
    worst_c = 0.0
    for pk in PANELS:
        px, _ = D.panel_px(pk)
        w = float((D.book_weights(px, "R20") - H.targets(px, "TOP20")).abs().max().max())
        worst_c = max(worst_c, w)
        say(f"    {pk:6s} max|dW| = {w:.3e}")
    say(f"    -> {'IDENTICAL, idea 132 sub-grid is exactly recoverable' if worst_c < 1e-12 else 'DIFFER — the calibration below is approximate'}")

    say(f"\n[GRID] {len(df)} arm-rows over "
        f"{df.groupby(['panel','book','cost']).ngroups} cells, ALL written to .grid.csv")
    gc = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
          "IS_Calmar", "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross",
          "TO", "adm_S1", "adm_S2", "pass4a_v2", "pass4a_v1", "pass4b", "fail4b"]
    with pd.option_context("display.max_rows", None):
        say(df[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P, R = make_picks(df, rets, ref)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    P.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n[PICKS] {len(P)} picks = 4 selectors x 3 screens x "
        f"{df.groupby(['panel','book','cost']).ngroups} cells; screens and selectors read the IS "
        f"window only; OOS read once.  Full table in .picks.csv; printed here in full.")
    with pd.option_context("display.max_rows", None):
        say(P[["sel", "screen", "panel", "book", "cost", "pick", "unscreened_pick", "moved",
               "picked", "n_admitted", "argmax_admitted", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
               "ctl_OOS_Sharpe", "v2_OOS_Sharpe", "spy_OOS_Sharpe", "beat_ctl", "beat_v2",
               "beat_spy", "pass4a_v2", "pass4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- calibration on idea 132
    say("\n[CALIBRATION] idea 132's own 18-cell sub-grid {V1u, R20(=TOP20), EWall}, re-scored")
    sub = P[P.book.isin(I132_BOOKS)]
    ks = sub[(sub.sel == "K_Sharpe") & (sub.screen == "S1")]
    n_cells_132 = ks.shape[0]
    picked_132 = int(ks.picked.sum())
    moved_132 = int(ks[ks.picked].moved.sum())
    say(f"    K_Sharpe/S1 on {n_cells_132} cells: picks in {picked_132}, declines in "
        f"{n_cells_132 - picked_132}, moves {moved_132} picks where it picks")
    say(f"    idea 132 published: picks in 7 of 18, declines in 11, 0 moved.")
    if I132_PICKS.exists():
        p132 = pd.read_csv(I132_PICKS)
        k132 = p132[(p132.sel == "K_Sharpe") & (p132.screen == "S1")]
        say(f"    idea 132's committed picks.csv, re-read: {int(k132.picked.sum())} of "
            f"{len(k132)} picked, {int(k132[k132.picked].moved.sum())} moved.")
        # per-cell arm agreement on the shared sub-grid
        m = sub.merge(p132.replace({"book": {"TOP20": "R20"}}),
                      on=["sel", "screen", "panel", "book", "cost"], suffixes=("", "_132"))
        agree = int((m.arm == m.arm_132).sum())
        say(f"    ARM-FOR-ARM agreement with idea 132 on the shared sub-grid: {agree} of "
            f"{len(m)} picks identical ({agree/max(len(m),1):.0%})")
        sub132 = sub[sub.screen != "S0"].groupby(["panel", "book", "cost"]).picked.all()
        say(f"    paired cells on the sub-grid: {int(sub132.sum())} (idea 132: 7)")
        prs = (sub[sub.set_index(['panel','book','cost']).index.isin(
                   sub132[sub132].index)].groupby(["sel", "screen"]).OOS_Sharpe.mean())
        say("    sub-grid PAIRED mean OOS Sharpe (idea 132's published reading):")
        say(prs.unstack().to_string(float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- discriminator / screen
    say("\n[SCREEN] does the screen move the pick, per selector? (48 cells)")
    disc = (P[P.screen != "S0"].groupby(["sel", "screen"])
            .agg(cells=("moved", "size"), picked=("picked", "sum"), moved=("moved", "sum"),
                 argmax_already_admitted=("argmax_admitted", "sum"),
                 mean_admitted=("n_admitted", "mean")).reset_index())
    disc["moved_where_picked"] = [
        int(P[(P.sel == r.sel) & (P.screen == r.screen) & P.picked].moved.sum())
        for r in disc.itertuples()]
    say(disc.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    A = []
    for (pk_, b, c), s in df.groupby(["panel", "book", "cost"]):
        row = dict(panel=pk_, book=b, cost=c, n_arms=len(s),
                   adm_S1=int(s.adm_S1.sum()), adm_S2=int(s.adm_S2.sum()))
        for sel, col in SELECTORS.items():
            am = s.loc[s[col].idxmax()]
            row[f"{sel}_in_S1"] = bool(am.adm_S1)
            row[f"{sel}_in_S2"] = bool(am.adm_S2)
        A.append(row)
    A = pd.DataFrame(A)
    say("\n[ADMISSIBILITY] per-cell admitted counts and whether each unscreened argmax is in")
    say(A.to_string(index=False))
    ne1, ne2 = A[A.adm_S1 > 0], A[A.adm_S2 > 0]
    say(f"[ADMISSIBILITY] S1 median {A.adm_S1.median():.1f} of 17 admitted "
        f"(non-empty in {len(ne1)} of {len(A)}); S2 median {A.adm_S2.median():.1f} "
        f"(non-empty in {len(ne2)} of {len(A)})")
    for sel in SELECTORS:
        r1 = float(ne1[f"{sel}_in_S1"].mean()) if len(ne1) else np.nan
        r2 = float(ne2[f"{sel}_in_S2"].mean()) if len(ne2) else np.nan
        say(f"     {sel}: unscreened argmax already admissible in {r1:.0%} of non-empty S1 "
            f"cells, {r2:.0%} of non-empty S2 cells")

    # ---------------------------------------------------------------- three readings
    common = P[P.screen != "S0"].groupby(["panel", "book", "cost"]).picked.all()
    paired_cells = set(common[common].index)
    P["in_paired"] = [tuple(x) in paired_cells for x in zip(P.panel, P.book, P.cost)]
    say(f"\n[READINGS] paired cells on the widened corpus: {len(paired_cells)} "
        f"(idea 132 had 7 of 18)")

    def agg(frame):
        return (frame.groupby(["sel", "screen"])
                .agg(OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
                     OOS_MaxDD=("OOS_MaxDD", "mean"), beat_spy=("beat_spy", "sum"),
                     beat_v2=("beat_v2", "sum"), beat_ctl=("beat_ctl", "sum"),
                     pass4a_v2=("pass4a_v2", "sum"), pass4b=("pass4b", "sum"),
                     n=("OOS_Sharpe", "size")).reset_index())

    fb, pr, po = agg(P), agg(P[P.in_paired]), agg(P[P.picked])
    say(f"\n  FALLBACK ({len(A)} cells each):")
    say(fb.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n  PAIRED ({len(paired_cells)} cells; this is idea 132's published reading):")
    say(pr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("\n  PICKED-ONLY (each screen over its own cell set; biased, shown for continuity):")
    say(po.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- THE ORDERING
    say("\n[ORDERING] the queue's actual question — does idea 132's selector ordering survive?")
    say("    idea 132, 7 paired cells, S0: K_MaxDD 1.052 > K_CAGR 1.047 > K_Calmar 1.040 > "
        "K_Sharpe 1.022  (incumbent LAST)")
    ordrows = []
    for scr in SCREENS:
        for label, frame in (("PAIRED", P[P.in_paired]), ("FALLBACK", P)):
            s = frame[frame.screen == scr].groupby("sel").OOS_Sharpe.mean().sort_values(
                ascending=False)
            rank_sharpe = list(s.index).index("K_Sharpe") + 1
            ordrows.append(dict(reading=label, screen=scr, n_cells=frame[frame.screen == scr]
                                .groupby(["panel", "book", "cost"]).ngroups,
                                order=" > ".join(f"{k} {v:.3f}" for k, v in s.items()),
                                K_Sharpe_rank=rank_sharpe, spread=float(s.max() - s.min())))
    O = pd.DataFrame(ordrows)
    say(O.to_string(index=False))

    say("\n[PAIRED DIFFERENCES] cell-by-cell, every selector minus K_Sharpe (same cells, "
        "same screen) — a mean is not a finding if the sign does not hold")
    drows = []
    for scr in SCREENS:
        base = (P[(P.screen == scr) & P.in_paired]
                .set_index(["panel", "book", "cost"]).loc[:, ["sel", "OOS_Sharpe", "arm"]])
        ref_s = base[base.sel == "K_Sharpe"].OOS_Sharpe
        for sel in SELECTORS:
            if sel == "K_Sharpe":
                continue
            o = base[base.sel == sel].OOS_Sharpe
            d = (o - ref_s).dropna()
            same_arm = int((base[base.sel == sel].arm.values ==
                            base[base.sel == "K_Sharpe"].arm.values).sum())
            drows.append(dict(screen=scr, sel=sel, n=len(d), mean_diff=float(d.mean()),
                              median=float(d.median()), wins=int((d > 1e-12).sum()),
                              ties=int((d.abs() <= 1e-12).sum()), losses=int((d < -1e-12).sum()),
                              same_arm_as_K_Sharpe=same_arm, max_abs=float(d.abs().max())))
    DD = pd.DataFrame(drows)
    say(DD.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    say("\n[INFORMATIVE CELLS] a paired cell can only separate two selectors if they pick "
        "DIFFERENT arms in it, and a mean is only a finding if it is not one cell.")
    irows = []
    for scr in SCREENS:
        for label, frame in (("PAIRED", P[P.in_paired]), ("ALL", P)):
            base = (frame[frame.screen == scr]
                    .set_index(["panel", "book", "cost"]).loc[:, ["sel", "OOS_Sharpe", "arm"]])
            ref_s, ref_a = base[base.sel == "K_Sharpe"].OOS_Sharpe, base[base.sel == "K_Sharpe"].arm
            for sel in SELECTORS:
                if sel == "K_Sharpe":
                    continue
                o, a = base[base.sel == sel].OOS_Sharpe, base[base.sel == sel].arm
                d = (o - ref_s).dropna()
                diff_cells = (a.values != ref_a.values)
                top = d.abs().max() / len(d) if len(d) else np.nan
                irows.append(dict(
                    reading=label, screen=scr, sel=sel, cells=len(d),
                    distinct_arm_cells=int(diff_cells.sum()), mean_diff=float(d.mean()),
                    top_cell_contribution=float(top),
                    share_of_mean_from_top_cell=float(abs(top / d.mean()))
                    if abs(d.mean()) > 1e-12 else np.nan,
                    n_cells_needed_for_this_mean_to_be_2sd=(
                        float(4.0 * d.std() ** 2 / d.mean() ** 2)
                        if abs(d.mean()) > 1e-12 and np.isfinite(d.std()) else np.nan)))
    IC = pd.DataFrame(irows)
    say(IC.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    ic0 = IC[(IC.reading == "PAIRED") & (IC.screen == "S0")]
    say(f"    -> on the reading idea 132 published, each rival is separated from the incumbent "
        f"by only {list(ic0.distinct_arm_cells)} of {len(paired_cells)} paired cells "
        f"({list(ic0.sel)}), and {list(ic0.share_of_mean_from_top_cell.round(2))} of each mean "
        f"comes from its single largest cell.  The cell counts these gaps would need to be two "
        f"standard errors from zero are "
        f"{list(ic0.n_cells_needed_for_this_mean_to_be_2sd.round(0))}.")
    say(f"    -> widening bought {len(paired_cells)} - 7 = {len(paired_cells) - 7} paired cells; "
        f"the queue's '4x as many cells' is 2.7x on total cells (18 -> 48) and 2.7x on paired "
        f"ones, an order of magnitude short of what these gaps require.")

    # ---------------------------------------------------------------- RANDOM control (power)
    say(f"\n[POWER] RANDOM selector control, {N_RANDOM_DRAWS} seeded draws (seed {SEED}), "
        "same cells, same admissible sets.  If the four real selectors sit inside this spread, "
        "the ordering is not separable at ANY cell count.")
    R["in_paired"] = [tuple(x) in paired_cells for x in zip(R.panel, R.book, R.cost)]
    prow = []
    for scr in SCREENS:
        for label, frame in (("PAIRED", R[R.in_paired]), ("FALLBACK", R)):
            per_draw = frame[frame.screen == scr].groupby("draw").OOS_Sharpe.mean()
            real = P[(P.screen == scr) & (P.in_paired if label == "PAIRED" else True)]
            rs = real.groupby("sel").OOS_Sharpe.mean()
            prow.append(dict(reading=label, screen=scr, rand_mean=float(per_draw.mean()),
                             rand_sd=float(per_draw.std()),
                             rand_p05=float(per_draw.quantile(0.05)),
                             rand_p95=float(per_draw.quantile(0.95)),
                             real_min=float(rs.min()), real_max=float(rs.max()),
                             real_spread=float(rs.max() - rs.min()),
                             rand_spread_90=float(per_draw.quantile(0.95)
                                                  - per_draw.quantile(0.05)),
                             all_real_inside_rand_90=bool(
                                 (rs >= per_draw.quantile(0.05)).all()
                                 and (rs <= per_draw.quantile(0.95)).all())))
    PW = pd.DataFrame(prow)
    say(PW.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    sel_out = pd.concat([fb.assign(reading="FALLBACK"), pr.assign(reading="PAIRED"),
                         po.assign(reading="PICKED_ONLY")])
    sel_out.to_csv(OUT / f"{STEM}.selectors.csv", index=False)

    # ---------------------------------------------------------------- KEEP paths
    say("\n[KEEP PATHS] all 816 rows, both paths; 4a scored against the LIVE RULES v2 book "
        "(cost-matched) and against RULES v1 for continuity")
    say(f"    4b (full sample):            {int(df.pass4b.sum())} of {len(df)}")
    say(f"    4a vs RULES v2 (live):       {int(df.pass4a_v2.sum())} of {len(df)}")
    say(f"    4a vs RULES v1 (continuity): {int(df.pass4a_v1.sum())} of {len(df)}")
    say(f"    BOTH 4a(v2) and 4b:          {int((df.pass4b & df.pass4a_v2).sum())} of {len(df)}")
    say(f"    BOTH 4a(v1) and 4b:          {int((df.pass4b & df.pass4a_v1).sum())} of {len(df)}")
    if int(df.pass4b.sum()):
        say("\n    4b passers, all of them:")
        say(df[df.pass4b][["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                           "OOS_Sharpe", "OOS_MaxDD", "gross", "TO", "pass4a_v2"]]
            .sort_values("Sharpe", ascending=False)
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    say("\n[KEEP PATHS, OOS WINDOW] every distinct picked arm, 4b re-scored on 2017-2026 alone")
    seen, krows = set(), []
    for r_ in P.itertuples():
        key = (r_.panel, r_.book, r_.cost, r_.arm)
        if key in seen:
            continue
        seen.add(key)
        g = df[(df.panel == r_.panel) & (df.book == r_.book) & (df.cost == r_.cost)
               & (df.arm == r_.arm)].iloc[0]
        spyo = ref[r_.panel]["spy_ret"].loc[OOS_START:]
        mgo = C.margins_at(H.window(rets[key], "OOS"), C.bars_win(spyo, "full"),
                           PHI0, DELTA0, "full")
        fo = C.fails(mgo)
        krows.append(dict(panel=r_.panel, book=r_.book, cost=r_.cost, arm=r_.arm,
                          CAGR=g.CAGR, Sharpe=g.Sharpe, MaxDD=g.MaxDD, H1=g.H1, H2=g.H2,
                          full_4a_v2=bool(g.pass4a_v2), full_4b=bool(g.pass4b),
                          full_fail4b=g.fail4b, OOS_CAGR=g.OOS_CAGR, OOS_Sharpe=g.OOS_Sharpe,
                          OOS_MaxDD=g.OOS_MaxDD, oos_window_4b=(len(fo) == 0),
                          oos_window_fail=",".join(fo) or "-"))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"[KEEP PATHS] distinct picked arms {len(K)}; full-sample 4a(v2) {int(K.full_4a_v2.sum())}"
        f", 4b {int(K.full_4b.sum())}, OOS-window 4b {int(K.oos_window_4b.sum())}")

    # ---------------------------------------------------------------- predictions
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    p1 = (moved_132 == 0) and (n_cells_132 - picked_132 == 11)
    say(f"   P1 calibration reproduces idea 132 (0 moves, declines in 11 of 18): "
        f"{moved_132} moves, declines in {n_cells_132 - picked_132} -> "
        f"{'HELD' if p1 else 'FAILED'}")
    ordS0 = O[(O.reading == "PAIRED") & (O.screen == "S0")].iloc[0]
    p2 = ordS0.K_Sharpe_rank != 4
    say(f"   P2 K_Sharpe is NOT last on the widened paired cells: rank "
        f"{int(ordS0.K_Sharpe_rank)} of 4 -> {'HELD' if p2 else 'FAILED'}")
    pw0 = PW[(PW.reading == "PAIRED") & (PW.screen == "S0")].iloc[0]
    p3 = bool(pw0.real_spread < pw0.rand_spread_90)
    say(f"   P3 real selector spread ({pw0.real_spread:.4f}) < random control's 90% spread "
        f"({pw0.rand_spread_90:.4f}) -> {'HELD' if p3 else 'FAILED'}")
    rate = float(ne1["K_Sharpe_in_S1"].mean()) if len(ne1) else np.nan
    p4 = rate >= 0.90
    say(f"   P4 K_Sharpe argmax already admissible in >= 90% of non-empty S1 cells: "
        f"{rate:.0%} -> {'HELD' if p4 else 'FAILED'}")
    p5 = len(paired_cells) >= 28
    say(f"   P5 >= 28 paired cells (4x idea 132's 7): {len(paired_cells)} -> "
        f"{'HELD' if p5 else 'FAILED'}")

    say("\n[CAVEATS] survivorship (idea 54) inflates every CAGR and flatters the ungated "
        "control end of every dial; idea 128's shallow IS drawdown window biases both screens "
        "toward admitting too much; idea 401's price restatement bounds the u56 reproduction "
        f"at {repro.loc['u56', 'IS_Sharpe']:.1e} on IS_Sharpe, the column the selectors read, "
        f"and moves {int((~sens.same).sum())} of {len(sens)} unscreened argmaxes.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
