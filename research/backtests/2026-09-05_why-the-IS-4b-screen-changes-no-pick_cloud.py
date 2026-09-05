#!/usr/bin/env python3
"""QUEUE idea 132 — why-the-IS-4b-screen-changes-no-pick  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 132)
    "idea 129 found S0, S1 and S2 select the IDENTICAL arm in all 7 cells where the screens
     pick, i.e. the IS 4b screen changes 0 of 18 rule-8 picks and its apparent OOS gain over
     S0 is entirely the 11 cells where it declines to pick.  Test whether that is a property
     of IS-Sharpe-argmax (the argmax is always already admissible) or of this arm family, by
     re-running with a selector that is NOT IS-Sharpe (IS Calmar, IS MaxDD) on the same
     corpus.  Bears on idea 110."

    Two rival explanations, both testable on one corpus:
      (A) SELECTOR PROPERTY — the IS-Sharpe argmax is nearly always already inside the IS 4b
          admissible set, so intersecting with that set cannot move it.  Then a selector that
          is NOT IS-Sharpe should have its pick moved by the screen.
      (B) ARM-FAMILY PROPERTY — the admissible set, whenever non-empty, contains the argmax of
          ANY reasonable IS statistic (e.g. it is nearly the whole cell, or the same handful of
          arms dominate on every statistic).  Then no selector's pick moves either.
    The discriminator is direct and is measured, not inferred: for each selector and cell,
    (i) is the unscreened argmax itself IS-admissible, and (ii) does the screened pick differ.

CORPUS — idea 129's, unchanged and re-derived rather than read
    3 panels (u56 / broad / small) x 3 books (V1u, TOP20, EWall) x 2 cost rungs (10, 25 bps)
    = 18 cells, each with idea 94's 17 arms (control, 5 gates x {dg,rw}, 2 stops, 2 book
    drawdown controls, 2 entry budgets) = 306 arm-rows, every one printed and written to
    .grid.csv.  Check (a) below asserts this run's 306 rows equal idea 129's published
    .grid.csv arm-for-arm before any new number is read; if that check is not EXACT nothing
    downstream is trustworthy and the script says so.

TUNED PARAMETERS — exactly two, both fully reported:
    1. the IS selector statistic, 4 values:
         K_Sharpe  argmax IS Sharpe          (idea 129's incumbent, the thing under test)
         K_Calmar  argmax IS CAGR / |IS MaxDD|
         K_MaxDD   argmax IS MaxDD           (i.e. the shallowest IS drawdown)
         K_CAGR    argmax IS CAGR
    2. the screen, 3 values: S0 (none) / S1 (IS 4b with the CAGR floor, phi=0.70) /
       S2 (IS 4b with the floor deleted, phi=0.00).  Both keep 4b's DD cap at delta=0.60.
    Panels, books, cost rungs, arms and the OOS window are reported axes, never selected on.
    4 selectors x 3 screens x 18 cells = 216 picks, all reported.

A FIX FOR THE COMPARISON IDEA 129 COULD NOT MAKE (pre-registered)
    Idea 129's mean OOS Sharpe per selector is averaged over DIFFERENT cell sets — S0 picks in
    18 cells, S1 in 7 — so "S1 beats S0" partly measures which cells it declined to enter, not
    which arm it chose.  Two corrections are reported side by side:
      PAIRED   restrict every comparison to the cells where ALL screens pick.
      FALLBACK a screen that admits nothing HOLDS THE CELL'S UNGATED CONTROL BOOK, which is what
               a prospective rule would actually do; every screen is then defined in all 18
               cells and the means are comparable.
    Neither is a new selector: both are ways of reading the same 216 picks honestly.

WALK-FORWARD (PROTOCOL rule 8) — this run IS a walk-forward experiment
    Every screen and selector reads the IS window (through 2016-12-31) ONLY.  Each resulting
    pick is read ONCE on 2017-01-01..2026, and reported as OOS CAGR / Sharpe / MaxDD against
    that cell's ungated control, RULES v1 (the live book) and SPY.  Both KEEP paths are
    evaluated on every pick: 4a (beat the live book in both halves at no worse MaxDD) and 4b
    (SPY-relative halves + OOS Sharpe, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's), on the
    full sample and again on the OOS window alone.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  Reproduction: with K_Sharpe, S1 and S2 pick the same arm as S0 in every cell where they
        pick, and S1 declines in 11 of 18 cells — idea 129's result, re-derived.
    P2  Explanation (A) wins: at least one non-Sharpe selector has a screened pick that differs
        from its unscreened pick in >= 1 cell.  If NO selector's pick ever moves, (B) wins and
        the screen is cosmetic on this arm family, which is a stronger and more useful KILL.
    P3  The IS-admissible set is a MINORITY of each cell (median admitted < 9 of 17 arms under
        S1) yet contains the K_Sharpe argmax in >= 90% of the cells where it is non-empty.
    P4  Under FALLBACK, S1's mean OOS Sharpe advantage over S0 shrinks by more than half for
        every selector — the apparent gain is the declining-to-pick cells.
    P5  K_Sharpe has the highest mean OOS Sharpe of the four selectors on the PAIRED cells (a
        control: if a broken selector won, the exercise would be measuring noise).

CAVEATS carried, not buried
    * Survivorship: all three panels are current constituents (idea 54); the small panel drops
      the 44 tickers with max_1d_move >= 1.0 (439 names) and its SPY is a joined benchmark that
      is never selectable.  Absent delistings inflate every arm's CAGR, so every 4b CAGR-floor
      margin here is optimistic.  No level in this file is an achievable return.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so an IS-window
      drawdown cap is measured on a window that cannot express a deep drawdown.  This biases
      every screen toward admitting too much, which if anything works AGAINST P3.
    * Idea 126: every row is quoted at t+1 execution only.
    * This run selects among EXISTING arms; it cannot promote a book and does not try to.  Its
      output is a statement about PROTOCOL rule 8's screen, not a candidate.

HARNESS
    Idea 94's script is IMPORTED (H.run, H.targets, H.arm_specs, H.halves, H.window, H.pass4a)
    and idea 129's screen machinery too (C.panel, C.bars_win, C.margins_at, C.fails), so the
    screen under test is literally the code that produced the result under test.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .picks.csv and .walkforward.csv.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights  # noqa: E402,F401
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_why-the-IS-4b-screen-changes-no-pick_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I129_GRID = OUT / "2026-09-05_cagr-floor-calibration_B.grid.csv"
I129_WF = OUT / "2026-09-05_cagr-floor-calibration_B.walkforward.csv"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
C = _load(I129, "i129")

FREQ, COSTS, BOOKS = H.FREQ, [10.0, 25.0], H.BOOKS
IS_END, OOS_START = H.IS_END, H.OOS_START
PANELS = ["u56", "broad", "small"]
PHI0, DELTA0 = 0.70, 0.60

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 90)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


# selector = (column to maximise).  All four are IS-window statistics only.
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_Calmar": "IS_Calmar",
             "K_MaxDD": "IS_MaxDD", "K_CAGR": "IS_CAGR"}
SCREENS = ["S0", "S1", "S2"]


def main():
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        ref[pk] = dict(bfull=bfull, bIS=bIS, spy=ms, spy_oos=mso, v1=v1, start=start,
                       spy_ret=spy, desc=desc)
        say(f"\n[panel] {pk} = {desc}: {px.shape[1]} cols, {px.index[0].date()}.."
            f"{px.index[-1].date()}, eval from {start.date()}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        say(f"    IS-window SPY bars (what the screens see): halves {bIS['s1']:.3f}/{bIS['s2']:.3f}"
            f" MaxDD {bIS['sdd']:.2%} CAGR {bIS['scagr']:.2%}")

        worst = 0.0
        for b in BOOKS:
            W = H.targets(px, b)
            worst = max(worst, float((H.run(px, W, bps=10.0)["r"].loc[start:]
                                      - backtest(px, W, cost_bps=10.0,
                                                 freq=FREQ)["returns"].loc[start:]).abs().max()))
        say(f"[a0] engine-equivalence, 3 ungated books: max|diff| = {worst:.3e} "
            f"({'EXACT' if worst < 1e-12 else 'NOT EXACT — unsafe'})")

        for b in BOOKS:
            for c in COSTS:
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = H.targets(px, b, gate, conv)
                    res = H.run(px, W, bps=c, **kw)
                    r = res["r"].loc[start:]
                    rets[(pk, b, c, arm)] = r
                    mm = metrics(r)
                    mi = metrics(H.window(r, "IS"))
                    mo = metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    fail = C.fails(mg)
                    rows.append(dict(
                        panel=pk, book=b, cost=c, arm=arm, kind=kind,
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
                        pass4a=H.pass4a(r, v1[c])))

    df = pd.DataFrame(rows)
    # IS admissibility: exactly idea 129's isok, expressed as columns
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_S2"] = core & (df.IS_CAGR - 0.00 * isbars > 0)
    df["adm_S0"] = True
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    # ---- (a) reproduction of idea 129's grid ----
    g129 = pd.read_csv(I129_GRID)
    j = df.merge(g129, on=["panel", "book", "cost", "arm"], suffixes=("", "_129"))
    keys = [k for k in ("CAGR", "Sharpe", "MaxDD", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
                        "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross")
            if f"{k}_129" in j.columns]
    d = {k: float((j[k] - j[f"{k}_129"]).abs().max()) for k in keys}
    ok = max(d.values()) < 1e-9
    say(f"\n[a] reproduction of idea 129's grid: {len(j)} of {len(df)} rows matched, max|diff| "
        + " ".join(f"{k} {v:.2e}" for k, v in d.items())
        + ("  EXACT" if ok else "  NOT EXACT — nothing below is trustworthy"))

    say(f"\n[GRID] {len(df)} arm-rows, ALL reported")
    gc = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
          "IS_Calmar", "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO",
          "adm_S1", "adm_S2", "pass4a", "pass4b", "fail4b"]
    with pd.option_context("display.max_rows", None):
        say(df[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- picks
    say("\n[PICKS] 4 selectors x 3 screens x 18 cells; screens and selectors read the IS window "
        "only; OOS read once.")
    prows = []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        ctl = rets[(pk, b, c, "control")]
        mc = metrics(H.window(ctl, "OOS"))
        mv = metrics(H.window(ref[pk]["v1"][c], "OOS"))
        mso = ref[pk]["spy_oos"]
        for sel, col in SELECTORS.items():
            base_pick = s.loc[s[col].idxmax()]
            for scr in SCREENS:
                cand = s[s[f"adm_{scr}"]]
                fell_back = not len(cand)
                if fell_back:
                    p = s[s.arm == "control"].iloc[0]     # FALLBACK convention
                else:
                    p = cand.loc[cand[col].idxmax()]
                r_oos = H.window(rets[(pk, b, c, p.arm)], "OOS")
                mo = metrics(r_oos)
                prows.append(dict(
                    sel=sel, screen=scr, panel=pk, book=b, cost=c,
                    pick=("(none -> control)" if fell_back else p.arm), arm=p.arm,
                    picked=not fell_back, n_admitted=int(len(cand)), n_arms=len(s),
                    argmax_admitted=bool(base_pick[f"adm_{scr}"]),
                    moved=bool(p.arm != base_pick.arm),
                    unscreened_pick=base_pick.arm,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_CAGR=mc["CAGR"], ctl_OOS_MaxDD=mc["MaxDD"],
                    v1_OOS_Sharpe=mv["Sharpe"], v1_OOS_CAGR=mv["CAGR"], v1_OOS_MaxDD=mv["MaxDD"],
                    spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                    spy_OOS_MaxDD=mso["MaxDD"],
                    beat_ctl=bool(mo["Sharpe"] > mc["Sharpe"]),
                    beat_v1=bool(mo["Sharpe"] > mv["Sharpe"]),
                    beat_spy=bool(mo["Sharpe"] > mso["Sharpe"]),
                    pass4a=bool(p.pass4a), pass4b=bool(p.pass4b), fail4b=p.fail4b))
    pk_df = pd.DataFrame(prows)
    pk_df.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    with pd.option_context("display.max_rows", None):
        say(pk_df[["sel", "screen", "panel", "book", "cost", "pick", "unscreened_pick", "moved",
                   "picked", "n_admitted", "argmax_admitted", "OOS_CAGR", "OOS_Sharpe",
                   "OOS_MaxDD", "ctl_OOS_Sharpe", "v1_OOS_Sharpe", "spy_OOS_Sharpe", "beat_ctl",
                   "beat_v1", "beat_spy", "pass4a", "pass4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---------------------------------------------------------------- P1 reproduction
    ks = pk_df[pk_df.sel == "K_Sharpe"]
    s1 = ks[ks.screen == "S1"]
    picked_cells = int(s1.picked.sum())
    moved_where_picked = int(s1[s1.picked].moved.sum())
    say(f"\n[P1] K_Sharpe / S1 reproduction of idea 129: picks in {picked_cells} of 18 cells, "
        f"declines in {18 - picked_cells}; among the cells where it picks the arm DIFFERS from "
        f"the unscreened S0 pick in {moved_where_picked}.")
    if I129_WF.exists():
        w129 = pd.read_csv(I129_WF)
        n129 = int((w129[w129.sel == "S1"]["pick"] == "(none)").sum())
        say(f"     idea 129's published walkforward.csv: S1 declines in {n129} of "
            f"{len(w129[w129.sel == 'S1'])} cells.")

    # ---------------------------------------------------------------- the discriminator
    say("\n[DISCRIMINATOR] does the screen move the pick, per selector?  (A) selector property "
        "-> only K_Sharpe is immune; (B) arm-family property -> nobody moves.")
    disc = (pk_df[pk_df.screen != "S0"]
            .groupby(["sel", "screen"])
            .agg(cells=("moved", "size"), picked=("picked", "sum"),
                 moved=("moved", "sum"),
                 moved_where_picked=("moved", lambda x: int(x[pk_df.loc[x.index, "picked"]].sum())),
                 argmax_already_admitted=("argmax_admitted", "sum"),
                 mean_admitted=("n_admitted", "mean")).reset_index())
    say(disc.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    tot_moved = int(pk_df[(pk_df.screen != "S0") & pk_df.picked].moved.sum())
    non_sharpe_moved = int(pk_df[(pk_df.screen != "S0") & pk_df.picked
                                 & (pk_df.sel != "K_Sharpe")].moved.sum())
    say(f"[DISCRIMINATOR] screened picks that differ from the unscreened pick, over all "
        f"selectors and both screens, counting only cells where the screen picks: {tot_moved}; "
        f"of those, non-K_Sharpe selectors account for {non_sharpe_moved}.")

    say("\n[ADMISSIBILITY] how big is the admissible set, and is the argmax already in it?")
    adm = []
    for (pk_, b, c), s in df.groupby(["panel", "book", "cost"]):
        row = dict(panel=pk_, book=b, cost=c, n_arms=len(s),
                   adm_S1=int(s.adm_S1.sum()), adm_S2=int(s.adm_S2.sum()))
        for sel, col in SELECTORS.items():
            am = s.loc[s[col].idxmax()]
            row[f"{sel}_in_S1"] = bool(am.adm_S1)
            row[f"{sel}_in_S2"] = bool(am.adm_S2)
        adm.append(row)
    A = pd.DataFrame(adm)
    say(A.to_string(index=False))
    ne1 = A[A.adm_S1 > 0]
    ne2 = A[A.adm_S2 > 0]
    say(f"[ADMISSIBILITY] S1 admitted count per cell: median {A.adm_S1.median():.1f} of 17 "
        f"(non-empty in {len(ne1)} of 18); S2: median {A.adm_S2.median():.1f} of 17 "
        f"(non-empty in {len(ne2)} of 18)")
    for sel in SELECTORS:
        r1 = float(ne1[f"{sel}_in_S1"].mean()) if len(ne1) else np.nan
        r2 = float(ne2[f"{sel}_in_S2"].mean()) if len(ne2) else np.nan
        say(f"     {sel}: unscreened argmax already admissible in {r1:.0%} of non-empty S1 "
            f"cells, {r2:.0%} of non-empty S2 cells")

    # ---------------------------------------------------------------- OOS reading
    say("\n[OOS] mean OOS Sharpe by (selector, screen).  FALLBACK = a screen that admits nothing "
        "holds the cell's ungated control (all 18 cells); PAIRED = only cells where every "
        "screen picks on its own.")
    common = (pk_df[pk_df.screen != "S0"].groupby(["panel", "book", "cost"]).picked.all())
    common = set(common[common].index)
    pk_df["in_paired"] = [tuple(x) in common for x in
                          zip(pk_df.panel, pk_df.book, pk_df.cost)]
    fb = (pk_df.groupby(["sel", "screen"])
          .agg(OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
               OOS_MaxDD=("OOS_MaxDD", "mean"), beat_spy=("beat_spy", "sum"),
               beat_v1=("beat_v1", "sum"), beat_ctl=("beat_ctl", "sum"),
               pass4a=("pass4a", "sum"), pass4b=("pass4b", "sum"), n=("OOS_Sharpe", "size"))
          .reset_index())
    say("  FALLBACK (18 cells each):")
    say(fb.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    pr = (pk_df[pk_df.in_paired].groupby(["sel", "screen"])
          .agg(OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
               OOS_MaxDD=("OOS_MaxDD", "mean"), n=("OOS_Sharpe", "size")).reset_index())
    say(f"  PAIRED ({len(common)} cells where every screen picks unaided):")
    say(pr.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("  reference OOS levels per cell (SPY / RULES v1 / ungated control):")
    refc = (pk_df[(pk_df.sel == "K_Sharpe") & (pk_df.screen == "S0")]
            [["panel", "book", "cost", "spy_OOS_CAGR", "spy_OOS_Sharpe", "spy_OOS_MaxDD",
              "v1_OOS_CAGR", "v1_OOS_Sharpe", "v1_OOS_MaxDD", "ctl_OOS_CAGR", "ctl_OOS_Sharpe",
              "ctl_OOS_MaxDD"]])
    say(refc.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # advantage of S1/S2 over S0, both readings
    say("\n[GAIN] S1 - S0 and S2 - S0 in mean OOS Sharpe, both readings")
    grows = []
    for sel in SELECTORS:
        a = fb[fb.sel == sel].set_index("screen").OOS_Sharpe
        b_ = pr[pr.sel == sel].set_index("screen").OOS_Sharpe
        d129 = (pk_df[(pk_df.sel == sel) & pk_df.picked]
                .groupby("screen").OOS_Sharpe.mean())      # idea 129's own (biased) reading
        grows.append(dict(sel=sel,
                          fb_S1_minus_S0=a.get("S1", np.nan) - a.get("S0", np.nan),
                          fb_S2_minus_S0=a.get("S2", np.nan) - a.get("S0", np.nan),
                          paired_S1_minus_S0=b_.get("S1", np.nan) - b_.get("S0", np.nan),
                          paired_S2_minus_S0=b_.get("S2", np.nan) - b_.get("S0", np.nan),
                          picked_only_S1_minus_S0=d129.get("S1", np.nan) - d129.get("S0", np.nan),
                          picked_only_S2_minus_S0=d129.get("S2", np.nan) - d129.get("S0", np.nan)))
    G = pd.DataFrame(grows)
    say(G.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    pk_df.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- KEEP paths on the picks
    say("\n[KEEP PATHS] every distinct picked arm, both paths, full sample AND OOS window alone")
    seen, krows = set(), []
    for r_ in pk_df.itertuples():
        key = (r_.panel, r_.book, r_.cost, r_.arm)
        if key in seen:
            continue
        seen.add(key)
        rr = rets[key]
        g = df[(df.panel == r_.panel) & (df.book == r_.book) & (df.cost == r_.cost)
               & (df.arm == r_.arm)].iloc[0]
        spyo = ref[r_.panel]["spy_ret"].loc[OOS_START:]
        bo = C.bars_win(spyo, "full")
        mgo = C.margins_at(H.window(rr, "OOS"), bo, PHI0, DELTA0, "full")
        fo = C.fails(mgo)
        krows.append(dict(panel=r_.panel, book=r_.book, cost=r_.cost, arm=r_.arm,
                          CAGR=g.CAGR, Sharpe=g.Sharpe, MaxDD=g.MaxDD, H1=g.H1, H2=g.H2,
                          full_4a=bool(g.pass4a), full_4b=bool(g.pass4b), full_fail4b=g.fail4b,
                          OOS_CAGR=g.OOS_CAGR, OOS_Sharpe=g.OOS_Sharpe, OOS_MaxDD=g.OOS_MaxDD,
                          oos_window_4b=(len(fo) == 0), oos_window_fail=",".join(fo) or "-"))
    K = pd.DataFrame(krows)
    say(K.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"[KEEP PATHS] distinct picked arms {len(K)}; full-sample 4a passes "
        f"{int(K.full_4a.sum())}, 4b passes {int(K.full_4b.sum())}, "
        f"OOS-window 4b passes {int(K.oos_window_4b.sum())}")

    # ---------------------------------------------------------------- predictions
    say("\n[P] PRE-REGISTERED PREDICTIONS, scored")
    p1 = (moved_where_picked == 0) and (18 - picked_cells == 11)
    say(f"   P1 K_Sharpe/S1 reproduces idea 129 (0 moves, declines in 11 of 18): "
        f"{moved_where_picked} moves, declines in {18 - picked_cells} -> "
        f"{'HELD' if p1 else 'FAILED'}")
    p2 = non_sharpe_moved >= 1
    say(f"   P2 explanation (A): a non-Sharpe selector's pick is moved by the screen in >= 1 "
        f"cell: {non_sharpe_moved} -> {'HELD (A)' if p2 else 'FAILED -> (B) the screen is '
                                       'cosmetic on this arm family'}")
    med1 = float(A.adm_S1.median())
    rate = float(ne1["K_Sharpe_in_S1"].mean()) if len(ne1) else np.nan
    p3 = (med1 < 9) and (rate >= 0.90)
    say(f"   P3 minority admissible (median {med1:.1f} < 9) AND contains the K_Sharpe argmax in "
        f">= 90% of non-empty cells ({rate:.0%}) -> {'HELD' if p3 else 'FAILED'}")
    shr = []
    for r_ in G.itertuples():
        if np.isfinite(r_.picked_only_S1_minus_S0) and abs(r_.picked_only_S1_minus_S0) > 1e-9:
            shr.append(abs(r_.fb_S1_minus_S0) < 0.5 * abs(r_.picked_only_S1_minus_S0))
    p4 = bool(shr) and all(shr)
    say(f"   P4 FALLBACK halves S1's apparent gain for every selector: {shr} -> "
        f"{'HELD' if p4 else 'FAILED'}")
    bestp = pr[pr.screen == "S0"].sort_values("OOS_Sharpe", ascending=False)
    p5 = len(bestp) and bestp.iloc[0].sel == "K_Sharpe"
    say(f"   P5 K_Sharpe is the best selector on PAIRED cells: "
        f"{list(zip(bestp.sel, bestp.OOS_Sharpe.round(3)))} -> {'HELD' if p5 else 'FAILED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
