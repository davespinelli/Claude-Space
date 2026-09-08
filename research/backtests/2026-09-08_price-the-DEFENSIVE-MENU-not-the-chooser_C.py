#!/usr/bin/env python3
"""QUEUE idea 418 — price-the-DEFENSIVE-MENU-not-the-chooser  (lane C, 2026-09-08).

QUESTION (pre-registered, verbatim from QUEUE.md idea 418)
    "idea 151 found every default, RANDOM included, wins OOS drawdown against the ungated
     control (K_Sharpe 42/48 +2.19 pp; RANDOM 40/55 +2.11 pp; the two not separable, t +0.13),
     i.e. idea 94's arm menu is a de-risking instrument regardless of who picks from it.  Price
     the MENU directly: what does holding a uniform blend of all 17 arms cost in CAGR and buy in
     MaxDD against the control, on both KEEP paths and at all three rungs?  If the blend
     dominates every chooser, the honest rule-8 default is the blend, not a pick."

WHAT IS ACTUALLY BEING TESTED
    Idea 151's finding is a statement about the MENU, not about any chooser: a seeded RANDOM
    draw over idea 94's 17 arms bought +2.11 pp of OOS drawdown against the ungated control and
    was not separable from the incumbent IS-Sharpe argmax (t +0.13).  If a uniform draw over the
    menu de-risks, then the menu's EXPECTED member de-risks, and the expected member is a thing
    you can actually hold: the equal-weight blend of all 17 arms.  A blend is strictly better
    than a draw — same expected exposure, none of the draw variance — so the honest form of idea
    151's result is not "any chooser will do" but "hold the menu".

    This run prices that instrument directly, as a book, against four comparands per cell:
      * the DO-NOTHING control (the cell's own ungated book) — idea 151's baseline;
      * the incumbent rule-8 chooser (K_Sharpe argmax) and K_CAGR (idea 416's pre-registered
        default) and a seeded K_Random — the choosers the blend must dominate to replace them;
      * RULES v2 (live), RULES v1 and SPY, cost-matched at each rung — PROTOCOL 3.

    A blend is NOT free.  Two constructions are priced separately and both reported, because the
    difference between them IS the menu's cost question:
      MENU_SEP  seventeen separately-managed sleeves, 1/17 of capital each, each paying its own
                turnover.  Cost = mean_a turnover_a x bps.  NO netting credit.  This is the
                conservative, no-operational-credit reading and the headline.
      MENU_NET  one account holding the blended weight vector, netting the sleeves' trades
                against each other.  Cost = |mean_a delta_a| x bps <= MENU_SEP's.  This is what
                a single book actually pays.
    Identically at 0 bps by construction (asserted); the gap at 10 and 25 bps is the netting
    credit, in basis points, which the record has never measured.

    This is a statement about PROTOCOL's rule-8 machinery, and it CAN promote a book — the blend
    is a holdable instrument — so both KEEP paths are scored on every blend row and every
    comparand row.

CORPUS — idea 151's, re-derived from the same imported harness
    3 panels (u56 / broad / small) x 9 books at matched gross 0.75 (EWall, V1u, R5, R10, R20,
    R40, S3-25, S3-50, S4-50; the sleeve books exist on u56/broad only, so small has 6)
    x 3 cost rungs (0, 10, 25 bps) x idea 94's 17 arms
      = 72 cells, 1,224 arm-rows, every one written to .grid.csv, and 72 x 2 blends on top.
    Idea 151's committed 1,224-row grid is the reproduction gate (it is the only committed grid
    carrying the 0-bps rung).

TUNED PARAMETERS — exactly two, both fully reported at every value
    1. the rule-8 DEFAULT, 6 values (2 blends + 3 choosers + the control):
         D_NONE     hold the ungated `control` arm.  Select nothing.        [idea 151's baseline]
         MENU_SEP   uniform 1/n blend of the pool, separately managed        [THE THING UNDER TEST]
         MENU_NET   uniform 1/n blend of the pool, netted in one account     [THE THING UNDER TEST]
         K_Sharpe   argmax IS Sharpe                              [the incumbent, the comparand]
         K_CAGR     argmax IS CAGR                                     [idea 416's pre-registered]
         K_Random   a seeded uniform draw over the same pool  [CONTROL, seed 20260908; also as a
                    400-draw distribution so the blend can be placed inside the draw's spread]
    2. the POOL blended/chosen from, 2 values:
         P_ALL      all 17 arms                        [the queue's question is about this one]
         P_S1       the IS-4b-admissible arms (phi=0.70, delta=0.60), control held on empty
    6 defaults x 2 pools x 72 cells = 864 rows, all written to .picks.csv/.walkforward.csv.
    Panels, books, cost rungs, arms, scoring metric and the OOS window are REPORTED axes, never
    selected on.  The blend weight (1/n) is not tuned: uniform is the only weighting tested.

WALK-FORWARD (PROTOCOL rule 8) — this run IS the walk-forward experiment
    MENU_SEP/MENU_NET on P_ALL read NOTHING from the in-sample window: the blend has no fitted
    parameter at all, so its OOS reading is clean by construction and the rule-8 comparison
    against an IS-fitted chooser is exactly the point.  On P_S1 the pool IS in-sample-fitted
    (phi/delta screen on <= 2016-12-31 only) and is reported separately for that reason.  Every
    chooser reads the IS window only and each pick is read ONCE on 2017-01-01..2026.  OOS
    CAGR/Sharpe/MaxDD are reported for every row against the cell's control, RULES v2 (live),
    RULES v1 and SPY, cost-matched at each rung.

PRE-REGISTERED PREDICTIONS (written before any number from the main grid was read)
    P1  MENU_SEP/P_ALL buys OOS drawdown against the control in a MAJORITY of the 72 cells
        (idea 151: every default did, K_Sharpe 42/48, RANDOM 40/55).
    P2  MENU_SEP/P_ALL SURRENDERS OOS CAGR against the control: paired mean d < 0.
    P3  The netting credit MENU_NET - MENU_SEP is exactly 0 at the 0-bps rung and strictly
        positive in mean at 10 and 25 bps, rising with the rung.
    P4  MENU_SEP/P_ALL's paired mean d(OOS Sharpe) vs the control is HIGHER than K_Sharpe's
        (the queue's dominance hypothesis).
    P5  The blend passes 4b in FEWER cells than the cell's best single arm does: averaging
        seventeen books dilutes the CAGR the 4b floor is measured against.
    P6  MENU_SEP/P_ALL lands ABOVE the median of the 400-draw K_Random distribution in a
        majority of cells on OOS Sharpe (a blend beats the draw it averages).

CAVEATS carried, not buried
    * Survivorship (idea 54): all three panels are current constituents; absent delistings
      inflate every arm's CAGR, so every 4b CAGR-floor margin here is optimistic and no level in
      this file is an achievable return.  It cannot flip a paired sign — both sides of every pair
      are drawn from the same flattered panel — but it does inflate the 4b counts.
    * MENU_NET nets the COST only: each sleeve's state machine (the dd-control arms' armed flag,
      the stops' trailing highs) still reads its own sleeve equity at rung c, not the netted
      book's.  This is the conservative direction for the blend's path and is stated, not hidden.
    * Idea 128: the IS window's SPY MaxDD is shallower than the OOS window's, so P_S1's IS
      drawdown bar is measured on a window that cannot express a deep drawdown; P_S1 admits too
      much, and this run inherits that bias exactly as idea 151 did.
    * Idea 401's DEFECT: data/prices.csv was rewritten by a daily-close vendor restatement after
      the u56 caches were committed, so the u56 leg of the reproduction gate matches to ~1e-5,
      not to machine zero.  Gate (a) shows the SIMULATOR is exact on every panel.
    * Idea 126: every row is quoted at t+1 execution only.
    * 72 cells are not 72 independent observations — books and arms overlap heavily within a
      panel, and the seventeen sleeves of a single blend overlap almost completely.  The
      t-statistics are quoted on that understanding; per-panel and per-rung breakdowns are given
      so the clustering is visible rather than hidden.

HARNESS
    Idea 94's script (H.run, H.arm_specs, H.halves, H.window, H.pass4a), idea 129's census
    machinery (C.bars_win, C.margins_at, C.fails) and idea 133's book family (D.book_weights,
    D.books_for, D.panel_px) are IMPORTED, not re-implemented.  The ONE exception is H.run
    itself: the blend needs the per-bar HELD matrix and the per-bar TRADED DELTA, which H.run
    does not return.  `run_held` below is a line-for-line copy that additionally returns them,
    and gate (a) asserts it reproduces H.run's returns, turnover and gross to machine zero on
    every one of the 1,224 arm-rows.  Nothing in research/ is modified.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .blend.csv, .picks.csv,
.walkforward.csv, .paired.csv and .keeppaths.csv next to itself.  Modifies nothing.
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
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_price-the-DEFENSIVE-MENU-not-the-chooser_C"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I129 = OUT / "2026-09-05_cagr-floor-calibration_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"
I151_GRID = OUT / "2026-09-08_does-any-selector-beat-doing-nothing_B.grid.csv"

SEED = 20260908
PHI0, DELTA0 = 0.70, 0.60
COSTS = [0.0, 10.0, 25.0]
PROTOCOL_RUNG = 10.0
PANELS = ["u56", "broad", "small"]
SELECTORS = {"K_Sharpe": "IS_Sharpe", "K_CAGR": "IS_CAGR"}
DEFAULTS = ["D_NONE", "MENU_SEP", "MENU_NET", "K_Sharpe", "K_CAGR", "K_Random"]
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

pd.set_option("display.width", 340)
pd.set_option("display.max_columns", 140)
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
    lo = min(wins, n - wins)
    tail = sum(math.comb(n, k) for k in range(0, lo + 1)) / (2.0 ** n)
    return float(min(1.0, 2.0 * tail))


# ---------------------------------------------------------------- H.run + held/delta capture
def run_held(px, W, m=1.0, stop=None, cooldown=0, D_=None, k=1.0, reset="recover",
             ebud=None, bps=10.0, freq=FREQ):
    """Line-for-line copy of idea 94's H.run that ALSO returns the per-bar held matrix and the
    per-bar TRADED delta (position change from trading only, drift excluded).  Gate (a) asserts
    it reproduces H.run exactly on every arm-row before any blend is built from it."""
    pxv = px.values
    rets = px.pct_change().fillna(0.0).values
    tgt = (W.reindex(px.index).fillna(0.0) * m).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape

    cur = np.zeros(ncol)
    peak_p = np.full(ncol, np.nan)
    pending = np.zeros(ncol, dtype=bool)
    held = np.zeros((nrow, ncol))
    dlt = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    gross_s = np.zeros(nrow)
    eq, pk, armed = 1.0, 1.0, False

    for i in range(nrow):
        if pending.any():
            turn[i] += cur[pending].sum()
            dlt[i] -= np.where(pending, cur, 0.0)
            cur = np.where(pending, 0.0, cur)
            pending[:] = False
        if mask[i] and i > 0:
            if D_ is not None:
                dd = eq / pk - 1.0
                if not armed and dd < -D_:
                    armed = True
                elif armed and (dd >= 0.0 if reset == "high" else dd > -D_ / 2.0):
                    armed = False
            new = tgt[i - 1] * (k if armed else 1.0)
            s = new.sum()
            if s > 1.0:
                new = new / s
            if ebud is not None:
                d = new - cur
                up = np.clip(d, 0.0, None).sum()
                if up > ebud:
                    new = cur + np.clip(d, None, 0.0) + np.clip(d, 0.0, None) * (ebud / up)
            turn[i] += np.abs(new - cur).sum()
            dlt[i] += new - cur
            cur = new
        held[i] = cur
        gross_s[i] = cur.sum()
        rp = float((cur * rets[i]).sum()) - turn[i] * bps / 1e4
        eq *= (1.0 + rp)
        pk = max(pk, eq)
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
        if stop is not None:
            alive = cur > 1e-9
            p = pxv[i]
            peak_p = np.where(alive, np.fmax(np.where(np.isnan(peak_p), -np.inf, peak_p), p),
                              np.nan)
            hit = alive & np.isfinite(p) & (p < peak_p * (1 - stop))
            if hit.any():
                pending |= hit
    idx = px.index
    r = pd.Series((held * rets).sum(axis=1), index=idx) - pd.Series(turn, index=idx) * bps / 1e4
    return dict(r=r, to=pd.Series(turn, index=idx), gross=pd.Series(gross_s, index=idx),
                held=held, dlt=dlt)


def _kw_for(kw):
    """H.run takes D=..., run_held takes D_=... (D is the imported idea-133 module here)."""
    out = dict(kw)
    if "D" in out:
        out["D_"] = out.pop("D")
    return out


# ---------------------------------------------------------------- grid + blends
def build_grid():
    """3 panels x 9 (or 6) books x 3 rungs x 17 arms, plus the 2 blend constructions per cell."""
    rows, blends, rets_store, ref = [], [], {}, {}
    gate_a = 0.0
    for pk_ in PANELS:
        px, spy_full = D.panel_px(pk_)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS = C.bars_win(spy, "full"), C.bars_win(spy, "IS")
        bOOS = C.bars_win(spy, "OOS")
        ms, mso = metrics(spy), metrics(spy.loc[OOS_START:])
        v1 = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        v2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"].loc[start:]
              for c in COSTS}
        books = D.books_for(pk_, px)
        ref[pk_] = dict(bfull=bfull, bIS=bIS, bOOS=bOOS, spy=ms, spy_oos=mso, v1=v1, v2=v2,
                        start=start, books=books)
        say(f"\n[panel] {pk_}: {px.shape[1]} cols, {px.index[0].date()}..{px.index[-1].date()}, "
            f"eval from {start.date()}, {len(books)} books {books}")
        say(f"    SPY full CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%}"
            f" halves {bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS Sharpe {mso['Sharpe']:.3f} "
            f"CAGR {mso['CAGR']:.2%} MaxDD {mso['MaxDD']:.2%}")
        for c in COSTS:
            mv2, mv1 = metrics(v2[c]), metrics(v1[c])
            o2, o1 = metrics(H.window(v2[c], "OOS")), metrics(H.window(v1[c], "OOS"))
            say(f"    RULES v2 @{c:>4.0f}bps CAGR {mv2['CAGR']:.2%} Sharpe {mv2['Sharpe']:.3f} "
                f"MaxDD {mv2['MaxDD']:.2%} OOS {o2['Sharpe']:.3f}/{o2['CAGR']:.2%}/"
                f"{o2['MaxDD']:.2%} | v1 Sharpe {mv1['Sharpe']:.3f} OOS {o1['Sharpe']:.3f}")

        RETS = px.pct_change().fillna(0.0).values
        isbar = bIS["scagr"]
        for b in books:
            for c in COSTS:
                # running sums, so the 17 sleeves are never all resident at once
                acc = {p: dict(W=None, Dm=None, to=None, names=[]) for p in POOLS}
                ctl_keep = None
                for arm, kind, kw, (gate, conv) in H.arm_specs():
                    W = D.book_weights(px, b, gate, conv)
                    res = run_held(px, W, bps=c, **_kw_for(kw))
                    chk = H.run(px, W, bps=c, **kw)
                    gate_a = max(gate_a,
                                 float((res["r"] - chk["r"]).abs().max()),
                                 float((res["to"] - chk["to"]).abs().max()),
                                 float((res["gross"] - chk["gross"]).abs().max()))
                    r = res["r"].loc[start:]
                    rets_store[(pk_, b, c, arm)] = r
                    mm, mi, mo = metrics(r), metrics(H.window(r, "IS")), metrics(H.window(r, "OOS"))
                    h1, h2 = H.halves(r)
                    mg = C.margins_at(r, bfull, PHI0, DELTA0, "full")
                    ismg = C.margins_at(r, bIS, PHI0, DELTA0, "IS")
                    omg = C.margins_at(r, bOOS, PHI0, DELTA0, "OOS")
                    fail, ofail = C.fails(mg), C.fails(omg)
                    rows.append(dict(
                        panel=pk_, book=b, cost=c, arm=arm, kind=kind, conv=conv,
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
                    # ---- accumulate the blend sleeves in place; never hold all 17 at once ----
                    admit = (ismg["H1"] > 0 and ismg["H2"] > 0 and ismg["DD"] > 0
                             and (mi["CAGR"] - PHI0 * isbar) > 0)
                    if arm == "control":
                        ctl_keep = (res["held"].copy(), res["dlt"].copy(), res["to"].values.copy())
                    for pool in POOLS:
                        if pool == "P_S1" and not admit:
                            continue
                        A = acc[pool]
                        if A["W"] is None:
                            A["W"], A["Dm"] = res["held"].copy(), res["dlt"].copy()
                            A["to"] = res["to"].values.copy()
                        else:
                            A["W"] += res["held"]
                            A["Dm"] += res["dlt"]
                            A["to"] += res["to"].values
                        A["names"].append(arm)
                    del res
                # ---- the two blend constructions, both pools, from the accumulated sleeves ----
                for pool in POOLS:
                    A = acc[pool]
                    empty = (pool == "P_S1" and A["W"] is None)
                    if empty:                                  # fall back to the control, as 151
                        Wb, Db, tob = ctl_keep[0] * 1.0, ctl_keep[1] * 1.0, ctl_keep[2] * 1.0
                        names, n = ["control"], 1
                    else:
                        names = A["names"]
                        n = len(names)
                        Wb, Db, tob = A["W"] / n, A["Dm"] / n, A["to"] / n
                    gross_ret = pd.Series((Wb * RETS).sum(axis=1), index=px.index)
                    to_sep = pd.Series(tob, index=px.index)
                    to_net = pd.Series(np.abs(Db).sum(axis=1), index=px.index)
                    r_sep = (gross_ret - to_sep * c / 1e4).loc[start:]
                    r_net = (gross_ret - to_net * c / 1e4).loc[start:]
                    # internal consistency: MENU_SEP == mean of the sleeves' NET returns
                    mean_net = pd.concat([rets_store[(pk_, b, c, a)] for a in names],
                                         axis=1).mean(axis=1)
                    gate_a = max(gate_a, float((r_sep - mean_net).abs().max()))
                    for tag, rb, tob in (("MENU_SEP", r_sep, to_sep), ("MENU_NET", r_net, to_net)):
                        mm = metrics(rb)
                        mi, mo = metrics(H.window(rb, "IS")), metrics(H.window(rb, "OOS"))
                        h1, h2 = H.halves(rb)
                        mg = C.margins_at(rb, bfull, PHI0, DELTA0, "full")
                        omg = C.margins_at(rb, bOOS, PHI0, DELTA0, "OOS")
                        fail, ofail = C.fails(mg), C.fails(omg)
                        rets_store[(pk_, b, c, f"{tag}/{pool}")] = rb
                        blends.append(dict(
                            panel=pk_, book=b, cost=c, blend=tag, pool=pool, n_arms=n,
                            pool_empty=empty, members=";".join(names),
                            CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], H1=h1, H2=h2,
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            gross=float(pd.Series(Wb.sum(axis=1), index=px.index).loc[start:].mean()),
                            TO=float(tob.loc[start:].sum() / mm["Years"]),
                            m_H1=mg["H1"], m_H2=mg["H2"], m_OOS=mg["OOS"], m_DD=mg["DD"],
                            m_CAGR=mg["CAGR"],
                            pass4b=(len(fail) == 0), fail4b=",".join(fail) or "-",
                            pass4b_oos=(len(ofail) == 0), fail4b_oos=",".join(ofail) or "-",
                            pass4a_v2=H.pass4a(rb, v2[c]), pass4a_v1=H.pass4a(rb, v1[c])))
                del acc
    df = pd.DataFrame(rows)
    isbars = df.panel.map(lambda p: ref[p]["bIS"]["scagr"])
    core = (df.IS_m_H1 > 0) & (df.IS_m_H2 > 0) & (df.IS_m_DD > 0)
    df["adm_P_S1"] = core & (df.IS_CAGR - PHI0 * isbars > 0)
    df["adm_P_ALL"] = True
    say(f"\n[a] run_held vs idea 94's H.run on all {len(df)} arm-rows (r, turnover, gross) AND "
        f"MENU_SEP vs the mean of the sleeves' net returns: max|diff| = {gate_a:.3e} "
        f"({'EXACT' if gate_a < 1e-12 else 'NOT EXACT — unsafe'})")
    return df, pd.DataFrame(blends), rets_store, ref


# ---------------------------------------------------------------- gate (b)
def reproduction_check(df):
    """Idea 151's committed 1,224-row grid, arm-for-arm, per column and per panel."""
    if not I151_GRID.exists():
        say("\n[b] idea 151's grid not present — reproduction gate SKIPPED.")
        return None
    g = pd.read_csv(I151_GRID)
    j = df.merge(g, on=["panel", "book", "cost", "arm"], suffixes=("", "_151"))
    keys = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "IS_MaxDD",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO"]
    say(f"\n[b] reproduction of idea 151's committed grid: {len(j)} of {len(df)} rows matched "
        f"(idea 151 published {len(g)}).")
    out = []
    for pkx, s in j.groupby("panel"):
        out.append(dict(panel=pkx, rows=len(s),
                        **{k: float((s[k] - s[f"{k}_151"]).abs().max()) for k in keys}))
    RP = pd.DataFrame(out).set_index("panel")
    say(RP.to_string(float_format=lambda x: f"{x:.2e}"))
    exact = [p for p in RP.index if RP.loc[p, keys].max() < 1e-12]
    say(f"    EXACT (max|diff| < 1e-12) on: {exact or 'no panel'}.  Any remainder is idea 401's "
        f"data/prices.csv restatement, a DATA difference — gate (a) shows the simulator is exact.")
    say(f"    adm_P_S1 agreement with idea 151: "
        f"{int((j.adm_P_S1 == j.adm_P_S1_151).sum()) if 'adm_P_S1_151' in j else -1} of {len(j)}")
    return RP


# ---------------------------------------------------------------- rows
def make_rows(df, B, rets, ref):
    """6 defaults x 2 pools x 72 cells.  D_NONE is the do-nothing control and is a real row."""
    rng = np.random.default_rng(SEED)
    prows, rand_rows = [], []
    Bi = B.set_index(["panel", "book", "cost", "blend", "pool"])
    for (pk_, b, c), s in df.groupby(["panel", "book", "cost"]):
        s = s.sort_values("arm").reset_index(drop=True)
        ctl_row = s[s.arm == "control"].iloc[0]
        mc = metrics(H.window(rets[(pk_, b, c, "control")], "OOS"))
        mv1 = metrics(H.window(ref[pk_]["v1"][c], "OOS"))
        mv2 = metrics(H.window(ref[pk_]["v2"][c], "OOS"))
        mso = ref[pk_]["spy_oos"]
        best4b = int(s.pass4b.sum())
        for pool in POOLS:
            cand = s[s[f"adm_{pool}"]]
            fell_back = not len(cand)
            pool_use = s[s.arm == "control"] if fell_back else cand
            pool_oos = np.array([metrics(H.window(rets[(pk_, b, c, a)], "OOS"))["Sharpe"]
                                 for a in pool_use.arm])
            for dft in DEFAULTS:
                if dft in ("MENU_SEP", "MENU_NET"):
                    bl = Bi.loc[(pk_, b, c, dft, pool)]
                    rb = rets[(pk_, b, c, f"{dft}/{pool}")]
                    mo = metrics(H.window(rb, "OOS"))
                    rec = dict(arm=f"{dft}({int(bl.n_arms)})", TO=float(bl.TO),
                               pass4a_v2=bool(bl.pass4a_v2), pass4a_v1=bool(bl.pass4a_v1),
                               pass4b=bool(bl.pass4b), fail4b=bl.fail4b,
                               pass4b_oos=bool(bl.pass4b_oos), fail4b_oos=bl.fail4b_oos,
                               full_CAGR=float(bl.CAGR), full_Sharpe=float(bl.Sharpe),
                               full_MaxDD=float(bl.MaxDD), H1=float(bl.H1), H2=float(bl.H2))
                    moved = True
                else:
                    if dft == "D_NONE":
                        p = ctl_row
                    elif dft == "K_Random":
                        p = pool_use.iloc[int(rng.integers(0, len(pool_use)))]
                    else:
                        p = pool_use.loc[pool_use[SELECTORS[dft]].idxmax()]
                    rb = rets[(pk_, b, c, p.arm)]
                    mo = metrics(H.window(rb, "OOS"))
                    rec = dict(arm=p.arm, TO=float(p.TO),
                               pass4a_v2=bool(p.pass4a_v2), pass4a_v1=bool(p.pass4a_v1),
                               pass4b=bool(p.pass4b), fail4b=p.fail4b,
                               pass4b_oos=bool(p.pass4b_oos), fail4b_oos=p.fail4b_oos,
                               full_CAGR=float(p.CAGR), full_Sharpe=float(p.Sharpe),
                               full_MaxDD=float(p.MaxDD), H1=float(p.H1), H2=float(p.H2))
                    moved = p.arm != "control"
                prows.append(dict(
                    default=dft, pool=pool, panel=pk_, book=b, cost=c,
                    pool_empty=fell_back, n_pool=len(pool_use), n_arms=len(s),
                    moved_off_control=bool(moved), cell_arms_pass4b=best4b,
                    TO_ratio=(rec["TO"] / ctl_row.TO) if ctl_row.TO > 0 else np.nan,
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    ctl_OOS_Sharpe=mc["Sharpe"], ctl_OOS_CAGR=mc["CAGR"],
                    ctl_OOS_MaxDD=mc["MaxDD"],
                    d_OOS_Sharpe=mo["Sharpe"] - mc["Sharpe"],
                    d_OOS_CAGR=mo["CAGR"] - mc["CAGR"],
                    d_OOS_MaxDD=abs(mc["MaxDD"]) - abs(mo["MaxDD"]),   # >0 = shallower = better
                    rand_pctile=float((pool_oos < mo["Sharpe"]).mean()),
                    v1_OOS_Sharpe=mv1["Sharpe"], v2_OOS_Sharpe=mv2["Sharpe"],
                    spy_OOS_Sharpe=mso["Sharpe"], spy_OOS_CAGR=mso["CAGR"],
                    spy_OOS_MaxDD=mso["MaxDD"],
                    beat_v2=bool(mo["Sharpe"] > mv2["Sharpe"]),
                    beat_spy=bool(mo["Sharpe"] > mso["Sharpe"]), **rec))
            for d_i in rng.integers(0, len(pool_use), N_RANDOM_DRAWS):
                rand_rows.append(dict(pool=pool, panel=pk_, book=b, cost=c,
                                      d_OOS_Sharpe=float(pool_oos[d_i] - mc["Sharpe"])))
    return pd.DataFrame(prows), pd.DataFrame(rand_rows)


# ---------------------------------------------------------------- paired reading
def paired_table(P, metric, label, by=None):
    rows = []
    grp = ["default", "pool"] + (by or [])
    for keyv, s in P.groupby(grp):
        d = s[metric].values
        nz = d[np.abs(d) > 1e-12]
        wins = int((nz > 0).sum())
        rows.append(dict(zip(grp, keyv if isinstance(keyv, tuple) else (keyv,))) | dict(
            cells=len(d), noop=int(len(d) - len(nz)), helps=wins, hurts=int(len(nz) - wins),
            win_rate=(wins / len(nz)) if len(nz) else np.nan,
            mean_d=float(np.nanmean(d)), median_d=float(np.nanmedian(d)),
            se=float(np.nanstd(d, ddof=1) / math.sqrt(len(d))),
            t=tstat(d), sign_p=sign_p(wins, len(nz))))
    T = pd.DataFrame(rows).set_index(grp).sort_index()
    say(f"\n[PAIRED — {label}]  d = default minus the DO-NOTHING control, per cell.  "
        f"'noop' = d == 0 exactly; win_rate/sign_p use the remaining cells only.")
    say(T.to_string(float_format=lambda x: f"{x:.4f}"))
    return T


def head_to_head(P, ref_default, metric, label):
    """The queue's dominance test: blend minus each chooser, paired on the same cell+pool."""
    key = ["pool", "panel", "book", "cost"]
    base = P[P.default == ref_default].set_index(key)[metric]
    rows = []
    for dft in DEFAULTS:
        if dft == ref_default:
            continue
        oth = P[P.default == dft].set_index(key)[metric]
        d = (base - oth).dropna().values
        nz = d[np.abs(d) > 1e-12]
        wins = int((nz > 0).sum())
        rows.append(dict(vs=dft, cells=len(d), ties=int(len(d) - len(nz)), blend_wins=wins,
                         blend_loses=int(len(nz) - wins),
                         win_rate=(wins / len(nz)) if len(nz) else np.nan,
                         mean_d=float(d.mean()), t=tstat(d), sign_p=sign_p(wins, len(nz))))
    T = pd.DataFrame(rows).set_index("vs")
    say(f"\n[HEAD-TO-HEAD — {label}]  d = {ref_default} minus the named default, same cell+pool.")
    say(T.to_string(float_format=lambda x: f"{x:.4f}"))
    return T


def main():
    say("=== idea 418 — price-the-DEFENSIVE-MENU-not-the-chooser (lane C, 2026-09-08) ===")
    say(f"PROTOCOL: t+1 execution, weekly cadence, costs {COSTS} bps, IS <= {IS_END}, "
        f"OOS >= {OOS_START}.  Two tuned params: DEFAULT (6 values) x POOL (2 values).")
    say("PRE-REGISTERED: P1 blend buys OOS DD in a majority of cells; P2 blend surrenders OOS "
        "CAGR; P3 netting credit 0 at 0 bps and rising in the rung; P4 blend's mean d(OOS "
        "Sharpe) > K_Sharpe's; P5 blend passes 4b in fewer cells than the best single arm; "
        "P6 blend above the draw's median in a majority of cells.")

    df, B, rets, ref = build_grid()
    df.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    B.to_csv(OUT / f"{STEM}.blend.csv", index=False)
    reproduction_check(df)

    ncell = df.groupby(["panel", "book", "cost"]).ngroups
    say(f"\n[GRID] {len(df)} arm-rows over {ncell} cells, ALL written to .grid.csv; "
        f"{len(B)} blend rows written to .blend.csv")
    gc = ["panel", "book", "cost", "arm", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe",
          "IS_CAGR", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO", "adm_P_S1",
          "pass4a_v2", "pass4b", "fail4b", "pass4b_oos"]
    with pd.option_context("display.max_rows", None):
        say(df[gc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    bc = ["panel", "book", "cost", "blend", "pool", "n_arms", "pool_empty", "CAGR", "Sharpe",
          "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "gross", "TO",
          "pass4a_v2", "pass4a_v1", "pass4b", "fail4b", "pass4b_oos"]
    with pd.option_context("display.max_rows", None):
        say("\n[BLENDS] every blend row:")
        say(B[bc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    P, R = make_rows(df, B, rets, ref)
    P.to_csv(OUT / f"{STEM}.picks.csv", index=False)
    P.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n[ROWS] {len(P)} = {len(DEFAULTS)} defaults x {len(POOLS)} pools x {ncell} cells.  "
        f"Choosers read the IS window only; the blends read NOTHING in sample on P_ALL.")
    pc = ["default", "pool", "panel", "book", "cost", "arm", "n_pool", "OOS_CAGR", "OOS_Sharpe",
          "OOS_MaxDD", "ctl_OOS_Sharpe", "d_OOS_Sharpe", "d_OOS_CAGR", "d_OOS_MaxDD", "TO_ratio",
          "v2_OOS_Sharpe", "spy_OOS_Sharpe", "beat_v2", "beat_spy", "pass4a_v2", "pass4b",
          "pass4b_oos"]
    with pd.option_context("display.max_rows", None):
        say(P[pc].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ---- Q1: what the menu costs and buys, against the control ----
    T_s = paired_table(P, "d_OOS_Sharpe", "OOS SHARPE (higher better)")
    T_c = paired_table(P, "d_OOS_CAGR", "OOS CAGR (higher better)")
    T_d = paired_table(P, "d_OOS_MaxDD", "OOS MaxDD, pp SHALLOWER (higher better)")
    paired_table(P[P.pool == "P_ALL"], "d_OOS_MaxDD", "OOS MaxDD by RUNG, P_ALL only", by=["cost"])
    paired_table(P[P.pool == "P_ALL"], "d_OOS_CAGR", "OOS CAGR by RUNG, P_ALL only", by=["cost"])
    paired_table(P[P.pool == "P_ALL"], "d_OOS_Sharpe", "OOS SHARPE by PANEL, P_ALL only",
                 by=["panel"])

    say("\n[PRICE OF THE MENU]  pp of OOS CAGR surrendered per pp of OOS MaxDD bought, "
        "vs the do-nothing control, paired-mean over cells.")
    prows = []
    for (dft, pool), s in P.groupby(["default", "pool"]):
        dc, dd = s.d_OOS_CAGR.mean() * 100, s.d_OOS_MaxDD.mean() * 100
        prows.append(dict(default=dft, pool=pool, dCAGR_pp=dc, dMaxDD_pp=dd,
                          price=(-dc / dd) if abs(dd) > 0.10 else np.nan,
                          dSharpe=s.d_OOS_Sharpe.mean()))
    PR = pd.DataFrame(prows).set_index(["default", "pool"]).sort_index()
    say(PR.to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n[EXCHANGE RATE]  OLS of d(OOS CAGR, pp) on d(OOS MaxDD, pp) over the moved cells: the "
        "MARGINAL price, beside the mean-ratio price above.  A common slope across defaults "
        "would mean the menu is ONE dial and the default only says how far along it you go.")
    def _fit(s):
        x = s.d_OOS_MaxDD.values * 100.0
        y = s.d_OOS_CAGR.values * 100.0
        ok = np.isfinite(x) & np.isfinite(y) & (np.abs(x) > 1e-12)
        if ok.sum() < 5:
            return np.nan, np.nan, np.nan, int(ok.sum())
        X, Y = x[ok], y[ok]
        b, a = np.polyfit(X, Y, 1)
        res = Y - (a + b * X)
        se = math.sqrt((res ** 2).sum() / (len(X) - 2) / ((X - X.mean()) ** 2).sum())
        r2 = 1.0 - (res ** 2).sum() / ((Y - Y.mean()) ** 2).sum()
        return float(b), float(se), float(r2), len(X)
    erows = []
    for (dft, pool), s in P.groupby(["default", "pool"]):
        b, se, r2, n = _fit(s)
        erows.append(dict(default=dft, pool=pool, moved_cells=n, slope=b, se=se, r2=r2))
    say(pd.DataFrame(erows).set_index(["default", "pool"]).to_string(
        float_format=lambda x: f"{x:.4f}"))
    bC, sC, _, nC = _fit(P[P.default.isin(["K_Sharpe", "K_CAGR", "K_Random"])])
    bB, sB, _, nB = _fit(P[P.default.isin(["MENU_SEP", "MENU_NET"])])
    say(f"    POOLED: choosers slope {bC:+.4f} +/- {sC:.4f} (n {nC}); blends slope "
        f"{bB:+.4f} +/- {sB:.4f} (n {nB}); difference {bB - bC:+.4f}, "
        f"t {(bB - bC) / math.sqrt(sC ** 2 + sB ** 2):+.2f}.  NOTE the two clouds do not span "
        f"the same range of d(MaxDD) — the blend's is far wider — so the slope difference is a "
        f"statement about where each default sits on the dial as much as about the dial itself.")

    # ---- Q2: the netting credit ----
    say("\n[NETTING CREDIT]  MENU_NET minus MENU_SEP, same cell+pool, by rung.")
    k = ["pool", "panel", "book", "cost"]
    sep = P[P.default == "MENU_SEP"].set_index(k)
    net = P[P.default == "MENU_NET"].set_index(k)
    NC = pd.DataFrame(dict(dSharpe=net.OOS_Sharpe - sep.OOS_Sharpe,
                           dCAGR_pp=(net.OOS_CAGR - sep.OOS_CAGR) * 100,
                           dTO=net.TO - sep.TO)).reset_index()
    say(NC.groupby(["cost", "pool"]).agg(cells=("dSharpe", "size"),
                                         mean_dSharpe=("dSharpe", "mean"),
                                         mean_dCAGR_pp=("dCAGR_pp", "mean"),
                                         max_dCAGR_pp=("dCAGR_pp", "max"),
                                         mean_dTO=("dTO", "mean")).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ---- Q3: dominance over the choosers ----
    for m, lab in (("OOS_Sharpe", "OOS SHARPE"), ("OOS_CAGR", "OOS CAGR"),
                   ("OOS_MaxDD", "OOS MaxDD (less negative = better; d>0 = blend shallower)")):
        mm = P.copy()
        if m == "OOS_MaxDD":
            mm["OOS_MaxDD"] = mm["OOS_MaxDD"].abs() * -1
        head_to_head(mm, "MENU_SEP", m, lab)

    say("\n[BLEND vs THE DRAW]  fraction of the cell's pool the blend's OOS Sharpe exceeds "
        "(0.5 = the median arm).")
    say(P.groupby(["default", "pool"]).rand_pctile.agg(["size", "mean", "median"]).to_string(
        float_format=lambda x: f"{x:.4f}"))

    # ---- KEEP paths ----
    say("\n[KEEP PATHS]  both paths on every default-row.  4a is against cost-matched RULES v2 "
        "(live) and v1 (continuity); 4b is PROTOCOL's full-sample reading and again on the OOS "
        "window alone.  Idea 414's comparand caveat applies to the 4a columns.")
    KP = P.groupby(["default", "pool"]).agg(
        rows=("pass4b", "size"), pass4a_v2=("pass4a_v2", "sum"), pass4a_v1=("pass4a_v1", "sum"),
        pass4b=("pass4b", "sum"), pass4b_oos=("pass4b_oos", "sum"),
        both=("pass4b", lambda x: int((P.loc[x.index, "pass4a_v2"] & x).sum())),
        beat_spy=("beat_spy", "sum"), beat_v2=("beat_v2", "sum")).sort_index()
    say(KP.to_string())
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv")
    say("\n    per-arm 4b counts in the underlying grid, for P5: "
        f"{int(df.pass4b.sum())} of {len(df)} arm-rows pass 4b full-sample; "
        f"{int(df.pass4b_oos.sum())} pass on the OOS window.")
    if int(KP.loc[("MENU_SEP", "P_ALL"), "pass4b"]) or int(KP.loc[("MENU_NET", "P_ALL"), "pass4b"]):
        say("\n    blend rows clearing 4b (full sample):")
        say(P[(P.default.isin(["MENU_SEP", "MENU_NET"])) & P.pass4b][
            ["default", "pool", "panel", "book", "cost", "full_CAGR", "full_Sharpe", "full_MaxDD",
             "H1", "H2", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "pass4a_v2",
             "pass4b_oos"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    else:
        say("\n    NO blend row clears 4b on the full sample.")

    # ---- verdict on the predictions ----
    ms = P[(P.default == "MENU_SEP") & (P.pool == "P_ALL")]
    ks = P[(P.default == "K_Sharpe") & (P.pool == "P_ALL")]
    say("\n[PREDICTIONS]")
    say(f"  P1 blend buys OOS DD in a majority: {int((ms.d_OOS_MaxDD > 0).sum())}/{len(ms)} "
        f"cells, mean {ms.d_OOS_MaxDD.mean()*100:+.2f} pp -> "
        f"{'CONFIRMED' if (ms.d_OOS_MaxDD > 0).mean() > 0.5 else 'REFUTED'}")
    say(f"  P2 blend surrenders OOS CAGR: mean {ms.d_OOS_CAGR.mean()*100:+.2f} pp -> "
        f"{'CONFIRMED' if ms.d_OOS_CAGR.mean() < 0 else 'REFUTED'}")
    c0 = NC[NC.cost == 0].dCAGR_pp.abs().max()
    say(f"  P3 netting credit 0 at 0 bps: max|d| {c0:.2e} -> "
        f"{'CONFIRMED' if c0 < 1e-12 else 'REFUTED'}; means by rung "
        + ", ".join(f"{int(cc)}bps {NC[NC.cost == cc].dCAGR_pp.mean():+.4f} pp"
                    for cc in COSTS))
    say(f"  P4 blend mean d(OOS Sharpe) {ms.d_OOS_Sharpe.mean():+.4f} vs K_Sharpe's "
        f"{ks.d_OOS_Sharpe.mean():+.4f} -> "
        f"{'CONFIRMED' if ms.d_OOS_Sharpe.mean() > ks.d_OOS_Sharpe.mean() else 'REFUTED'}")
    bl4b = int(KP.loc[("MENU_SEP", "P_ALL"), "pass4b"])
    anyarm = int(df.groupby(["panel", "book", "cost"]).pass4b.any().sum())
    say(f"  P5 blend 4b passes {bl4b} vs cells where ANY arm passes {anyarm} -> "
        f"{'CONFIRMED' if bl4b < anyarm else 'REFUTED'}")
    say(f"  P6 blend above its pool's median arm: {int((ms.rand_pctile > 0.5).sum())}/{len(ms)} "
        f"-> {'CONFIRMED' if (ms.rand_pctile > 0.5).mean() > 0.5 else 'REFUTED'}")

    pd.concat([T_s.assign(metric="OOS_Sharpe"), T_c.assign(metric="OOS_CAGR"),
               T_d.assign(metric="OOS_MaxDD")]).to_csv(OUT / f"{STEM}.paired.csv")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {STEM}.{{console.txt,grid.csv,blend.csv,picks.csv,walkforward.csv,"
        f"paired.csv,keeppaths.csv}}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
