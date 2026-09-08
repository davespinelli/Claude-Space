#!/usr/bin/env python3
"""QUEUE idea 151 — does-any-selector-beat-doing-nothing  (lane B, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 151)
    "idea 141's rule-8 walk-forward put all 8 selectors x 4 tightness levels in 0.698-0.773 OOS
     Sharpe with a RANDOM selector at 0.738-0.753 and the ungated do-nothing control at 0.762,
     i.e. no selector earns its complexity.  Test the do-nothing control directly as the rule-8
     default: run every leaderboard cell with NO arm selection at all against the incumbent
     IS-Sharpe pick, paired, and report how many cells the selection actually helps."

WHAT IS ACTUALLY BEING TESTED
    PROTOCOL rule 8 does not name a selector.  In practice every rule-8 run in this record has
    used the SAME default: pick the arm with the best in-sample Sharpe, read it once out of
    sample.  The record now carries ~20 scattered anecdotes of that default losing to inaction
    (ideas 110/132/136/140/141/151/155/172/204/228/230/261/278/282/287/293/354/376 among them),
    each a by-product of a run about something else, each on a different corpus, and no census.
    This run is the census, and it asks the only question that changes PROTOCOL:

        Against the DO-NOTHING default — hold the cell's own ungated book, select nothing —
        does the incumbent IS-Sharpe argmax help, on a PAIRED reading of every cell?

    "Do nothing" is a genuine arm here, not a straw man: the `control` arm IS the cell's ungated
    book, so the comparison is the same instrument, same panel, same cost rung, same window, and
    the difference is exactly the act of selection.  A cell where the argmax lands ON the control
    is a no-op (d == 0 exactly) and is reported separately from a cell where selection moved and
    was right.  That distinction is what an average over selectors cannot show.

    This is a statement about the PROTOCOL's own machinery, not a book.  It cannot promote a
    candidate and does not try; both KEEP paths are nevertheless scored on all 1,224 arm-rows.

CORPUS — idea 133/142's, RE-DERIVED, and widened on the one axis idea 235 says matters
    3 panels (u56 / broad / small) x 9 books at matched gross 0.75 (EWall, V1u, R5, R10, R20,
    R40, S3-25, S3-50, S4-50; the sleeve books exist on u56/broad only, so small has 6)
    x 3 cost rungs (0, 10, 25 bps) x idea 94's 17 arms
      = 72 cells, 1,224 arm-rows, every one written to .grid.csv.
    The 0-bps rung is NEW here and is a REPORTED axis, never selected on.  Idea 235 asks whether
    "selection beats do-nothing" is a rung artefact (idea 230 found the premium monotone in the
    rung, -0.0161 at 0 bps -> +0.1055 at 30, and a coin flip at PROTOCOL's own 10 bps).  With
    only the committed 10/25 rungs that question cannot be answered; with 0 in the grid it can.
    Idea 142's committed 816-row grid is the 10/25 sub-grid and is used as the reproduction gate.

TUNED PARAMETERS — exactly two, both fully reported at every value
    1. the rule-8 DEFAULT, 6 values (4 real selectors + 2 controls):
         D_NONE     hold the ungated `control` arm.  Select nothing.       [THE THING UNDER TEST]
         K_Sharpe   argmax IS Sharpe                            [the incumbent, the comparand]
         K_CAGR     argmax IS CAGR
         K_Calmar   argmax IS CAGR / |IS MaxDD|
         K_MaxDD    argmax IS MaxDD  (shallowest IS drawdown)
         K_Random   a seeded uniform draw over the same pool    [CONTROL, seed 20260908,
                    reported as a 400-draw distribution AND as one seeded realisation]
    2. the POOL the default chooses from, 2 values:
         P_ALL      all 17 arms
         P_S1       the IS-4b-admissible arms (phi=0.70, delta=0.60), control held on empty
    6 defaults x 2 pools x 72 cells = 864 picks, all written to .picks.csv.
    Panels, books, cost rungs, arms, scoring metric and the OOS window are REPORTED axes.

THREE SCORING METRICS, all reported, none tuned
    OOS Sharpe is the metric idea 141 and every prior anecdote used.  Idea 163 hypothesises the
    screen's whole value is DRAWDOWN control, so OOS MaxDD is scored alongside, and OOS CAGR
    with it, on the identical paired cells.  A default that helps on one and hurts on another is
    reported as such rather than collapsed.

WALK-FORWARD (PROTOCOL rule 8) — this run IS the walk-forward experiment
    Every default reads the IS window (<= 2016-12-31) ONLY.  Each pick is read ONCE on
    2017-01-01..2026 and reported as OOS CAGR / Sharpe / MaxDD against that cell's do-nothing
    control, the LIVE RULES v2 book, RULES v1 and SPY, cost-matched at each rung.  Both KEEP
    paths are evaluated on every one of the 1,224 rows: 4a against RULES v2 (live) and RULES v1
    (continuity), and 4b on the full sample and again on the OOS window alone for every pick.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  At PROTOCOL's own 10-bps rung, K_Sharpe/P_ALL helps in FEWER THAN HALF of the 24 cells
        on OOS Sharpe (idea 230's coin flip, tested directly for the first time).
    P2  The paired mean d(OOS Sharpe) of K_Sharpe/P_ALL over all 72 cells is NEGATIVE.
    P3  K_Sharpe is not separable from K_Random: the seeded random control's paired mean sits
        within one standard error of K_Sharpe's.
    P4  Idea 235's rung effect is REAL in sign: d(OOS Sharpe) for K_Sharpe rises monotonically
        in the cost rung across 0 -> 10 -> 25 bps.
    P5  Idea 163's drawdown hypothesis is REAL: K_Sharpe's paired win rate on OOS MaxDD is
        strictly higher than its win rate on OOS Sharpe.
    P6  The screen is near-inert on picks: P_S1 changes the pick in fewer than 25% of cells.

CAVEATS carried, not buried
    * Survivorship (idea 54): all three panels are current constituents; absent delistings
      inflate every arm's CAGR, so every 4b CAGR-floor margin here is optimistic and no level
      in this file is an achievable return.  It cannot flip the paired sign — both sides of
      every pair are drawn from the same flattered panel — but it does inflate the 4b counts.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so an IS-window
      drawdown cap is measured on a window that cannot express a deep drawdown; this biases
      P_S1 toward admitting too much.
    * Idea 401's DEFECT: data/prices.csv was rewritten by a daily-close vendor restatement after
      idea 133/142 were committed while the broad/small caches were not, so the u56 leg of the
      reproduction gate can only match to ~1e-5.  The gate reports per-panel tolerances and, more
      importantly, re-runs every argmax on the committed columns to count picks the restatement
      itself could move.
    * Idea 126: every row is quoted at t+1 execution only.
    * 72 cells are not 72 independent observations — books and arms overlap heavily within a
      panel.  The t-statistics below are quoted on that understanding and the per-panel and
      per-rung breakdowns are given so the clustering is visible rather than hidden.

HARNESS
    Idea 94's script (H.run, H.arm_specs, H.halves, H.window, H.pass4a), idea 129's census
    machinery (C.bars_win, C.margins_at, C.fails) and idea 133's book family (D.book_weights,
    D.books_for, D.panel_px) are IMPORTED, not re-implemented.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .picks.csv, .walkforward.csv,
.paired.csv, .keeppaths.csv and .restatement.csv next to itself.  Modifies nothing.
"""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-08_does-any-selector-beat-doing-nothing_B"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I142_GRID = OUT / "2026-09-08_selector-comparison-needs-more-cells_B.grid.csv"

SEED = 20260908
PHI0, DELTA0 = 0.70, 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_CAGR": "IS_CAGR",
             "K_Calmar": "IS_Calmar", "K_MaxDD": "IS_MaxDD"}
DEFAULTS = ["D_NONE", "K_Sharpe", "K_CAGR", "K_Calmar", "K_MaxDD", "K_Random"]
POOLS = ["P_ALL", "P_S1"]
N_RANDOM_DRAWS = 400


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

pd.set_option("display.width", 320)
pd.set_option("display.max_columns", 120)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def calmar(cagr, dd):
    return cagr / abs(dd) if np.isfinite(dd) and abs(dd) > 1e-12 else np.nan


def tstat(x):
    x = np.asarray([v for v in x if np.isfinite(v)], float)
    if len(x) < 3 or x.std(ddof=1) == 0:
        return np.nan
    return float(x.mean() / (x.std(ddof=1) / math.sqrt(len(x))))


def sign_p(wins, n):
    """Two-sided exact binomial sign test at p=0.5, ties excluded by the caller."""
    if n == 0:
        return np.nan
    def _c(k):
        return math.comb(n, k)
    lo = min(wins, n - wins)
    tail = sum(_c(k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


# ------------------------------------------------------------------ grid
def build_grid():
    """3 panels x 9 (or 6) books x 3 rungs x 17 arms, re-derived from the imported harness."""
    rows, rets, ref = [], {}, {}
    for pk in PANELS:
        px, spy_full = D.panel_px(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        bOOS = C.bars_win(spy, "OOS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        books = D.books_for(pk, px)
        ref[pk] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms, spy_oos=mso, v1=v1, v2=v2,
                       start=start, spy_ret=spy, books=books)
        say(f"\n[panel] {pk}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}, {len(books)} books {books}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            o2, o1 = metrics(H.window(v2[c], "OOS")), metrics(H.window(v1[c], "OOS"))
            say(f"    RULES v2 @{c:>4.0f}bps CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
                f"MaxDD {mv2['MaxDD']:.2%} OOS {o2['Sharpe']:.3f}/{o2['CAGR']:.2%}/"
                f"{o2['MaxDD']:.2%} | v1 CAGR {mv1['CAGR']:.2%} Sharpe {mv1['Sharpe']:.3f} "
                f"MaxDD {mv1['MaxDD']:.2%} OOS {o1['Sharpe']:.3f}")

        # ---- gate (a): the modified runner reproduces engine.backtest on every ungated book ----
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
                    omg = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    fail, ofail = C.fails(mg), C.fails(omg)
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
                        pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-", n_fail=len(fail),
                        pass4b_oos=(len(ofail) == 0), fail4b_oos=",".join(ofail) or "-",
                        pass4a_v2=H.pass4a(r, v2[c]), pass4a_v1=H.pass4a(r, v1[c])))
    df = pd.DataFrame(rows)
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_P_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_P_ALL"] = True
    return df, rets, ref


# ------------------------------------------------------------------ gate (b)
def reproduction_check(df):
    """Idea 142's committed 816-row grid, arm-for-arm, per column and per panel, plus a direct
    count of argmaxes the idea-401 restatement can move."""
    g = pd.read_csv(I142_GRID)
    j = df.merge(g, on=["panel", "book", "cost", "arm"], suffixes=("", "_142"))
    keys = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
            "IS_Calmar", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]
    say(f"\n[b] reproduction of idea 142's committed grid: {len(j)} of {len(df)} rows matched "
        f"(idea 142 published {len(g)}; the unmatched rows here are the NEW 0-bps rung).")
    out = []
    for pk, s in j.groupby("panel"):
        out.append(dict(panel=pk, rows=len(s), **{k: float((s[k] - s[f"{k}_142"]).abs().max())
                                                  for k in keys}))
    RP = pd.DataFrame(out).set_index("panel")
    say(RP.to_string(float_format=lambda x: f"{x:.2e}"))
    exact = [p for p in RP.index if RP.loc[p, keys].max() < 1e-12]
    say(f"    EXACT (max|diff| < 1e-12) on: {exact or 'no panel'}.  Any remainder is idea 401's "
        f"data/prices.csv daily-close restatement, a DATA difference — gate (a) shows the "
        f"simulator is exact on every panel.")

    say("\n[b2] RESTATEMENT SENSITIVITY — every selector's argmax re-run on idea 142's own "
        "COMMITTED columns, counting picks that differ from this run's.")
    srows = []
    for (pk, b, c), s in j.groupby(["panel", "book", "cost"]):
        for sel, col in SELECTORS.items():
            mine, theirs = s.loc[s[col].idxmax()].arm, s.loc[s[f"{col}_142"].idxmax()].arm
            top2 = s[col].nlargest(2).values
            srows.append(dict(panel=pk, book=b, cost=c, sel=sel, mine=mine, theirs=theirs,
                              same=(mine == theirs),
                              argmax_margin=float(top2[0] - top2[1]) if len(top2) > 1 else np.nan,
                              col_perturb=float((s[col] - s[f"{col}_142"]).abs().max())))
    S = pd.DataFrame(srows)
    for pk, s in S.groupby("panel"):
        say(f"    {pk:6s}: {int((~s.same).sum())} of {len(s)} argmaxes differ; "
            f"{int((s.argmax_margin < s.col_perturb).sum())} cells have an argmax margin thinner "
            f"than that column's own perturbation")
    say(f"    TOTAL: {int((~S.same).sum())} of {len(S)} argmaxes moved by the restatement.")
    if int((~S.same).sum()):
        say(S[~S.same].to_string(index=False, float_format=lambda x: f"{x:.2e}"))
    return RP, S


# ------------------------------------------------------------------ picks
def make_picks(df, rets, ref):
    """6 defaults x 2 pools x 72 cells.  D_NONE is the do-nothing control and is a real row."""
    rng = np.random.default_rng(SEED)
    prows, rand_rows = [], []
    for (pk, b, c), s in df.groupby(["panel", "book", "cost"]):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl_row = s[s.arm == "control"].iloc[0]
        ctl = rets[(pk, b, c, "control")]
        mc = metrics(H.window(ctl, "OOS"))
        mv1 = metrics(H.window(ref[pk]["v1"][c], "OOS"))
        mv2 = metrics(H.window(ref[pk]["v2"][c], "OOS"))
        mso = ref[pk]["spy_oos"]
        for pool in POOLS:
            cand = s[s[f"adm_{pool}"]]
            fell_back = not len(cand)
            pool_use = s[s.arm == "control"] if fell_back else cand
            # pool-level context for idea 204's hypothesis: is the pool's own mean any good?
            pool_oos = np.array([metrics(H.window(rets[(pk, b, c, a)], "OOS"))["Sharpe"]
                                 for a in pool_use.arm])
            pool_mean_d = float(pool_oos.mean() - mc["Sharpe"])
            for dft in DEFAULTS:
                if dft == "D_NONE":
                    p, moved_note = ctl_row, False
                elif dft == "K_Random":
                    p = pool_use.iloc[int(rng.integers(0, len(pool_use)))]
                    moved_note = p.arm != "control"
                else:
                    col = SELECTORS[dft]
                    p = pool_use.loc[pool_use[col].idxmax()]
                    moved_note = p.arm != "control"
                top2 = (pool_use[SELECTORS[dft]].nlargest(2).values
                        if dft in SELECTORS else np.array([np.nan, np.nan]))
                mo = metrics(H.window(rets[(pk, b, c, p.arm)], "OOS"))
                prows.append(dict(
                    default=dft, pool=pool, panel=pk, book=b, cost=c, arm=p.arm,
                    pool_empty=fell_back, n_pool=len(pool_use), n_arms=len(s),
                    moved_off_control=bool(moved_note), pool_mean_dSharpe=pool_mean_d,
                    IS_argmax_margin=(float(top2[0] - top2[1]) if len(top2) > 1
                                      and np.isfinite(top2[0]) else np.nan),
                    TO=float(p.TO), TO_ratio=float(p.TO / ctl_row.TO) if ctl_row.TO > 0 else np.nan,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_CAGR=mc["CAGR"],
                    ctl_OOS_MaxDD=mc["MaxDD"],
                    d_OOS_Sharpe=mo["Sharpe"] - mc["Sharpe"],
                    d_OOS_CAGR=mo["CAGR"] - mc["CAGR"],
                    d_OOS_MaxDD=abs(mc["MaxDD"]) - abs(mo["MaxDD"]),   # >0 = shallower = better
                    v1_OOS_Sharpe=mv1["Sharpe"], v2_OOS_Sharpe=mv2["Sharpe"],
                    spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                    spy_OOS_MaxDD=mso["MaxDD"],
                    beat_v2=bool(mo["Sharpe"] > mv2["Sharpe"]),
                    beat_spy=bool(mo["Sharpe"] > mso["Sharpe"]),
                    pass4a_v2=bool(p.pass4a_v2), pass4a_v1=bool(p.pass4a_v1),
                    pass4b=bool(p.pass4b), fail4b=p.fail4b,
                    pass4b_oos=bool(p.pass4b_oos), fail4b_oos=p.fail4b_oos))
            # RANDOM as a distribution, on the same pool
            oos_s = pool_oos
            for d_i in rng.integers(0, len(pool_use), N_RANDOM_DRAWS):
                rand_rows.append(dict(pool=pool, panel=pk, book=b, cost=c,
                                      d_OOS_Sharpe=float(oos_s[d_i] - mc["Sharpe"])))
    return pd.DataFrame(prows), pd.DataFrame(rand_rows)


# ------------------------------------------------------------------ paired reading
def paired_table(P, metric, label):
    """The queue's question, exactly: over the 72 cells, how many does the default help?"""
    rows = []
    for (dft, pool), s in P.groupby(["default", "pool"]):
        d = s[metric].values
        nz = d[np.abs(d) > 1e-12]
        wins = int((nz > 0).sum())
        rows.append(dict(default=dft, pool=pool, cells=len(d),
                         noop=int(len(d) - len(nz)), helps=wins, hurts=int(len(nz) - wins),
                         win_rate=(wins / len(nz)) if len(nz) else np.nan,
                         mean_d=float(np.nanmean(d)), median_d=float(np.nanmedian(d)),
                         sd=float(np.nanstd(d, ddof=1)),
                         se=float(np.nanstd(d, ddof=1) / math.sqrt(len(d))),
                         t=tstat(d), sign_p=sign_p(wins, len(nz))))
    T = pd.DataFrame(rows).set_index(["default", "pool"]).sort_index()
    say(f"\n[PAIRED — {label}]  d = default's pick minus the DO-NOTHING control, per cell.  "
        f"'noop' = cells where the default landed on the control itself (d == 0 exactly) and "
        f"win_rate/sign_p are computed on the remaining cells only.")
    say(T.to_string(float_format=lambda x: f"{x:.4f}"))
    return T


def main():
    say(f"=== idea 151 — does-any-selector-beat-doing-nothing (lane B, 2026-09-08) ===")
    say(f"PROTOCOL: t+1 execution, weekly cadence, costs {COSTS} bps, IS <= {IS_END}, "
        f"OOS >= {OOS_START}.  Two tuned params: DEFAULT (6 values) x POOL (2 values).")

    df, rets, ref = build_grid()
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    repro, sens = reproduction_check(df)
    sens.to_csv(OUT / f"{STEM}.restatement.csv", index=False)

    ncell = df.groupby(["panel", "book", "cost"]).ngroups
    say(f"\n[GRID] {len(df)} arm-rows over {ncell} cells, ALL written to .grid.csv")
    gc = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
          "IS_Calmar", "IS_CAGR", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross",
          "TO", "adm_P_S1", "pass4a_v2", "pass4a_v1", "pass4b", "fail4b", "pass4b_oos"]
    with pd.option_context("display.max_rows", None):
        say(df[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P, R = make_picks(df, rets, ref)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    P.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n[PICKS] {len(P)} = {len(DEFAULTS)} defaults x {len(POOLS)} pools x {ncell} cells.  "
        f"Every default reads the IS window only; every OOS number is read once.  Full table:")
    pc = ["default", "pool", "panel", "book", "cost", "arm", "n_pool", "moved_off_control",
          "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "ctl_OOS_Sharpe", "d_OOS_Sharpe",
          "d_OOS_CAGR", "d_OOS_MaxDD", "v2_OOS_Sharpe", "spy_OOS_Sharpe", "beat_v2", "beat_spy",
          "pass4a_v2", "pass4b", "pass4b_oos"]
    with pd.option_context("display.max_rows", None):
        say(P[pc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # --------------------------------------------------------- THE ANSWER
    TS = paired_table(P, "d_OOS_Sharpe", "OOS SHARPE (idea 141's metric)")
    TC = paired_table(P, "d_OOS_CAGR", "OOS CAGR")
    TD = paired_table(P, "d_OOS_MaxDD", "OOS MaxDD, sign flipped so >0 = SHALLOWER = better "
                                        "(idea 163's hypothesis)")
    pd.concat({"OOS_Sharpe": TS, "OOS_CAGR": TC, "OOS_MaxDD": TD},
              names=["metric"]).to_csv(OUT / f"{STEM}.paired.csv")

    say("\n[P1/P2] The queue's own question, at PROTOCOL's own rung and over the whole grid, "
        "for the INCUMBENT default K_Sharpe on the unscreened pool:")
    for scope, sub in [("ALL 72 cells", P), (f"{PROTOCOL_RUNG:.0f} bps only",
                                             P[P.cost == PROTOCOL_RUNG])]:
        k = sub[(sub.default == "K_Sharpe") & (sub.pool == "P_ALL")]
        nz = k[k.d_OOS_Sharpe.abs() > 1e-12]
        say(f"    {scope:16s}: {len(k)} cells, {int(len(k) - len(nz))} no-op, "
            f"helps {int((nz.d_OOS_Sharpe > 0).sum())} / hurts "
            f"{int((nz.d_OOS_Sharpe < 0).sum())}, mean d {k.d_OOS_Sharpe.mean():+.4f}, "
            f"median {k.d_OOS_Sharpe.median():+.4f}, t {tstat(k.d_OOS_Sharpe.values):+.2f}, "
            f"sign p {sign_p(int((nz.d_OOS_Sharpe > 0).sum()), len(nz)):.3f}")

    say("\n[P3] K_Sharpe vs the RANDOM control on the same pools "
        f"({N_RANDOM_DRAWS} draws per cell, seed {SEED}):")
    for pool in POOLS:
        k = P[(P.default == "K_Sharpe") & (P.pool == pool)].d_OOS_Sharpe
        rr = P[(P.default == "K_Random") & (P.pool == pool)].d_OOS_Sharpe
        dist = R[R.pool == pool].groupby(["panel", "book", "cost"]).d_OOS_Sharpe.mean()
        se = float(k.std(ddof=1) / math.sqrt(len(k)))
        say(f"    {pool}: K_Sharpe mean {k.mean():+.4f} (se {se:.4f}) | one seeded random "
            f"{rr.mean():+.4f} | random EXPECTATION over {N_RANDOM_DRAWS} draws/cell "
            f"{dist.mean():+.4f} | separable at 1 se: "
            f"{'NO' if abs(k.mean() - dist.mean()) < se else 'YES'}")

    say("\n[P4] Idea 235's rung question — d(OOS Sharpe) by cost rung, unscreened pool:")
    rung = (P[P.pool == "P_ALL"].groupby(["default", "cost"])
            .d_OOS_Sharpe.agg(["mean", "median", "count",
                               lambda x: float((x > 1e-12).sum())]))
    rung.columns = ["mean_d", "median_d", "cells", "helps"]
    say(rung.to_string(float_format=lambda x: f"{x:.4f}"))
    ks = P[(P.default == "K_Sharpe") & (P.pool == "P_ALL")].groupby("cost").d_OOS_Sharpe.mean()
    mono = bool(ks.is_monotonic_increasing)
    say(f"    K_Sharpe mean d by rung: " + ", ".join(f"{c:.0f}bps {v:+.4f}"
                                                    for c, v in ks.items())
        + f"  -> monotone increasing in the rung: {'YES' if mono else 'NO'}")

    say("\n[P5] Idea 163's drawdown hypothesis — the same picks scored three ways "
        "(unscreened pool, non-noop cells only):")
    for dft in DEFAULTS:
        k = P[(P.default == dft) & (P.pool == "P_ALL")]
        line = f"    {dft:9s}:"
        for m, lab in [("d_OOS_Sharpe", "Sharpe"), ("d_OOS_CAGR", "CAGR"),
                       ("d_OOS_MaxDD", "MaxDD")]:
            nz = k[k[m].abs() > 1e-12]
            wr = (nz[m] > 0).mean() if len(nz) else np.nan
            line += f"  {lab} win {wr:.3f} ({int((nz[m] > 0).sum())}/{len(nz)}) mean {k[m].mean():+.4f} |"
        say(line)

    say("\n[P6] Pool inertness — does the IS-4b screen change the pick?")
    for dft in DEFAULTS:
        a = P[(P.default == dft) & (P.pool == "P_ALL")].set_index(["panel", "book", "cost"]).arm
        b = P[(P.default == dft) & (P.pool == "P_S1")].set_index(["panel", "book", "cost"]).arm
        say(f"    {dft:9s}: pick differs in {int((a != b).sum())} of {len(a)} cells "
            f"({(a != b).mean():.1%}); empty-pool fallbacks "
            f"{int(P[(P.default == dft) & (P.pool == 'P_S1')].pool_empty.sum())}")

    # --------------------------------------------------------- WHEN does it help
    say("\n[MECHANISM] Spearman of K_Sharpe's paired d(OOS Sharpe) against three candidate "
        "explanators, unscreened pool, 72 cells (reported, never selected on):")
    k = P[(P.default == "K_Sharpe") & (P.pool == "P_ALL")]
    for col, note in [("IS_argmax_margin", "how decisive the IS argmax was"),
                      ("pool_mean_dSharpe", "idea 204: the pool's own sign"),
                      ("TO_ratio", "idea 261: turnover ratio vs the control"),
                      ("cost", "idea 235: the cost rung")]:
        say(f"    rho(d, {col:18s}) = {H.spearman(k.d_OOS_Sharpe.values, k[col].values):+.3f}"
            f"   [{note}]")

    say("\n[PER PANEL] K_Sharpe/P_ALL, the clustering made visible:")
    per = k.groupby("panel").agg(cells=("d_OOS_Sharpe", "size"),
                                 helps=("d_OOS_Sharpe", lambda x: int((x > 1e-12).sum())),
                                 noop=("d_OOS_Sharpe", lambda x: int((x.abs() <= 1e-12).sum())),
                                 mean_d=("d_OOS_Sharpe", "mean"),
                                 mean_dDD=("d_OOS_MaxDD", "mean"))
    say(per.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n[PER BOOK] K_Sharpe/P_ALL:")
    perb = k.groupby("book").agg(cells=("d_OOS_Sharpe", "size"),
                                 helps=("d_OOS_Sharpe", lambda x: int((x > 1e-12).sum())),
                                 mean_d=("d_OOS_Sharpe", "mean"))
    say(perb.to_string(float_format=lambda x: f"{x:.4f}"))

    # --------------------------------------------------------- benchmarks + KEEP paths
    say("\n[BENCHMARKS] OOS window (2017-01-01..) — every default's mean OOS Sharpe against the "
        "do-nothing control, RULES v2 (live), RULES v1 and SPY, unscreened pool:")
    bm = P[P.pool == "P_ALL"].groupby("default").agg(
        OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), beat_v2=("beat_v2", "sum"),
        beat_spy=("beat_spy", "sum"), pass4b=("pass4b", "sum"),
        pass4b_oos=("pass4b_oos", "sum"), pass4a_v2=("pass4a_v2", "sum"))
    ctlrow = P[(P.default == "D_NONE") & (P.pool == "P_ALL")]
    say(bm.to_string(float_format=lambda x: f"{x:.4f}"))
    say(f"    reference levels: control OOS Sharpe {ctlrow.ctl_OOS_Sharpe.mean():.4f} / CAGR "
        f"{ctlrow.ctl_OOS_CAGR.mean():.2%} / MaxDD {ctlrow.ctl_OOS_MaxDD.mean():.2%}; "
        f"RULES v2 {ctlrow.v2_OOS_Sharpe.mean():.4f}; RULES v1 {ctlrow.v1_OOS_Sharpe.mean():.4f}; "
        f"SPY {ctlrow.spy_OOS_Sharpe.mean():.4f} / {ctlrow.spy_OOS_CAGR.mean():.2%} / "
        f"{ctlrow.spy_OOS_MaxDD.mean():.2%}")

    say("\n[KEEP PATHS] all {} arm-rows, scored against the LIVE RULES v2 book and RULES v1:"
        .format(len(df)))
    kp = pd.DataFrame([dict(scope="all rows", n=len(df),
                            pass4a_v2=int(df.pass4a_v2.sum()), pass4a_v1=int(df.pass4a_v1.sum()),
                            pass4b_full=int(df.pass4b.sum()), pass4b_oos=int(df.pass4b_oos.sum()),
                            both=int((df.pass4a_v2 & df.pass4b).sum()))]
                      + [dict(scope=f"cost {c:.0f}bps", n=int((df.cost == c).sum()),
                              pass4a_v2=int(df[df.cost == c].pass4a_v2.sum()),
                              pass4a_v1=int(df[df.cost == c].pass4a_v1.sum()),
                              pass4b_full=int(df[df.cost == c].pass4b.sum()),
                              pass4b_oos=int(df[df.cost == c].pass4b_oos.sum()),
                              both=int((df[df.cost == c].pass4a_v2
                                        & df[df.cost == c].pass4b).sum())) for c in COSTS]
                      + [dict(scope=f"panel {p}", n=int((df.panel == p).sum()),
                              pass4a_v2=int(df[df.panel == p].pass4a_v2.sum()),
                              pass4a_v1=int(df[df.panel == p].pass4a_v1.sum()),
                              pass4b_full=int(df[df.panel == p].pass4b.sum()),
                              pass4b_oos=int(df[df.panel == p].pass4b_oos.sum()),
                              both=int((df[df.panel == p].pass4a_v2
                                        & df[df.panel == p].pass4b).sum())) for p in PANELS])
    kp.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    say(kp.to_string(index=False))
    both = df[df.pass4a_v2 & df.pass4b]
    say(f"    rows clearing BOTH paths: {len(both)}")
    if len(both):
        say(both[["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "TO", "pass4b_oos"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("    NOTE: a KEEP row here is a property of the CORPUS, not of the selection question "
        "this idea asks.  Nothing is proposed from it; see the .result.md.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\n[done] wrote {STEM}.{{console.txt,grid.csv,picks.csv,walkforward.csv,paired.csv,"
        f"keeppaths.csv,restatement.csv}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
