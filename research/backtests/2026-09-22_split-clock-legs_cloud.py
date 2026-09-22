#!/usr/bin/env python3
"""Idea 2256 (2026-09-22, lane cloud, run 12) -- DOES THE BOTH-PATHS CELL'S TURNOVER FLOOR MOVE
IF THE TWO LEGS RUN ON DIFFERENT CLOCKS?

WHY THIS RUN EXISTS
    The 2026-09-20 Sunday review disqualified the record's ONLY book clearing PROTOCOL path 4a
    AND path 4b at once -- idea 142's by-product `u56 / S3-50 + band3-rw @10 bps` -- on TURNOVER
    alone: 8.18x/yr on u56 (10.88x on broad) against the live RULES v2 book's 1.77x, so its whole
    advantage lives at or below 10 bps.  Three devices have been priced against that number since
    and all three KILLED: 2254 (rank hysteresis), 2250 (slow rank refresh), and 2246's accounting
    run, which decomposed the 8.18x into 6.36x equity + 1.82x sleeve and showed that the COMMON
    RESCALE re-couples the legs for +15.6% of turnover while DECOUPLING them entirely (each leg
    pinned at its own fixed gross) costs 2.5 pp of CAGR and both KEEP paths.
    The untested middle is a CADENCE SPLIT: keep the common rescale -- so each refresh still
    targets the committed book -- but let the two legs REFRESH ON DIFFERENT CLOCKS.  A leg that
    is not refreshed simply drifts; a leg that is refreshed snaps back to the committed target.
    This run walks the full 4x4 clock grid and reports what it does to the turnover floor and to
    both KEEP paths.

THE BOOK (frozen, bit-for-bit the committed cell -- idea 133's `S3-50` under idea 94's `band3`
gate in the `rw` convention, t+1 execution)
        raw equity leg : R = (1-f) * ranked(px, 20, band3, rw)          f = 0.50, n = 20
        raw sleeve leg : S = f * sleeve_weights(px, [TLT,GLD,UUP]) masked by band3
        common rescale : k_t = GROSS / (R+S).sum(axis=1),  A = k*R, B = k*S,  GROSS = 0.75
    NOTHING about the book is tuned.  n, f, band, gross, the sleeve asset list and the t+1
    execution are FROZEN at the committed values; panel and cost rung are REPORTED axes, never
    selected on.  Tuned-parameter count for PROTOCOL rule 4: TWO (equity clock, sleeve clock).

THE SPLIT CLOCK (what is new here, and what it is NOT)
    Two independent rebalance masks, one per leg.  At date t:
        if the EQUITY clock fires : cur_A <- A_t        (else cur_A just drifts)
        if the SLEEVE clock fires : cur_B <- B_t        (else cur_B just drifts)
        traded vector  d_j = fireA*(A_tj - cur_Aj) + fireB*(B_tj - cur_Bj)
        turnover_t     = sum_j |d_j|      (legs NET within a column when both clocks fire)
    This is NOT idea 2246's DECOUPLED twin: the rescale is untouched, so every refresh still aims
    at the committed blend.  The only thing that changes is HOW OFTEN each leg is allowed to aim.
    Consequence stated up front, not discovered: between refreshes of one leg the book's total
    gross is no longer exactly 0.75 -- the stale leg drifts while the fresh leg is re-solved.
    That is the honest cost of a split clock and is reported (mean realised gross per cell).

THE GRID (every point published, pass or fail)
    PANEL {u56, broad} x EQUITY CLOCK {D,W,M,Q} x SLEEVE CLOCK {D,W,M,Q} x COST {5,10,25,50} bps
    = 128 published rows, each with CAGR / Sharpe / MaxDD / H1 / H2 / OOS triple / turnover /
    leg-attributed turnover / mean realised gross / 4a / 4b.
    The DIAGONAL (equity clock == sleeve clock) is the committed same-clock family and is the
    comparand the split cells must beat; (W,W) IS the committed cell.

GATES (printed before any hypothesis is read)
    G1  A + B reproduces `i133.book_weights(px,'S3-50','band3','rw')`, max|dw| < 1e-12.
    G2  the split-clock simulator at (W,W) reproduces `engine.backtest` returns AND turnover
        to < 1e-12 -- i.e. the degenerate limit IS the committed engine.
    G3  the (u56, 10 bps, W, W) cell reproduces the Sunday review's re-run of idea 142 to < 5e-3
        on CAGR / Sharpe / MaxDD / H1 / H2 / OOS Sharpe.
    G4  leg attribution is additive: |TO_eq + TO_sl - TO_total| < 1e-10 at every cell.
    G5  all 128 cells published.
    G6  the WHOLE DIAGONAL is the committed cadence ladder: (f,f) reproduces
        `engine.backtest(px, book_weights, freq=f)` returns AND turnover to < 1e-12 for every
        f in {D,W,M,Q} -- so the off-diagonal cells are the only thing this run adds.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 read ONCE)
    The two clocks are the tuned dials, so the legal IS-only chooser is argmax IN-SAMPLE Sharpe
    over the 16 clock pairs on 2009-2016 alone, per panel per cost rung; the 2017-2026 leg is then
    reported untouched against the live RULES v2 book's OOS and SPY's OOS.  A second, equally
    IS-only chooser is published beside it (C_TO: among IS clock pairs whose IS turnover is at or
    under the live book's own IS turnover, take the max IS Sharpe; ABSTAIN if none qualifies),
    because the Sunday review's objection was turnover, not Sharpe.  C_TO is reported, not
    selected on -- both choosers' picks are published whatever they say.
    A THIRD chooser, C_DIAG, is published beside them and is DISCLOSED AS POST-HOC: it was added
    after the first run of this script showed that no split cell beats its own same-clock floor,
    and it restricts the same IS-Sharpe argmax to the 4 SAME-CLOCK rungs (i.e. it spends ONE
    parameter, cadence, not two).  It is reported precisely because it is the honest chooser once
    the split device is dead; its pick is published at every cell whatever it says.

CAVEATS carried
    Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT constituents, so every
    CAGR level is optimistic and both 4b level legs are easier than on a point-in-time panel.
    Turnover contrasts are same-tape / same-names and first-order immune; the pass counts are not.
    Costs are flat per unit turnover, no spread, impact or borrow.  One execution delay (t+1), one
    blend (0.50), one band (3%), one gross (0.75), one sleeve.  This run proposes no rules change
    (PROTOCOL rule 6 gives that to the Sunday review).
    Deterministic, standalone.  Writes .log.txt / .grid.csv / .floor.csv / .walkforward.csv next
    to itself.  Modifies nothing.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-22_split-clock-legs_cloud"
OUT = ROOT / "research" / "backtests"
I94 = OUT / "2026-09-04_drawdown-insurance-price-list_B.py"
I133 = OUT / "2026-09-05_is-the-defensive-class-one-book_cloud.py"

COSTS = [5.0, 10.0, 25.0, 50.0]
PANELS = ["u56", "broad"]
CLOCKS = ["D", "W", "M", "Q"]
GATE, CONV, BLEND, NTOP = "band3", "rw", 0.50, 20
PHI0, DELTA0 = 0.70, 0.60          # PROTOCOL 4b: CAGR floor and MaxDD cap multipliers

REF142 = dict(CAGR=0.11264347733520674, Sharpe=1.2631836842789088, MaxDD=-0.11630008422595184,
              H1=1.2821692801839668, H2=1.2472607800728146, OOS_Sharpe=1.288118742321921)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(I94, "i94")
D = _load(I133, "i133")
FREQ, GROSS, OOS_START, IS_END = H.FREQ, H.GROSS, H.OOS_START, H.IS_END
S3 = D.S3

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 600)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ------------------------------------------------------------------ the two scaled legs ----
def scaled_legs(px):
    """A, B with A + B == the committed book's target weights at every date (common rescale)."""
    gm = H.gate_mask(px, GATE)
    R = ((1 - BLEND) * D.ranked(px, NTOP, GATE, CONV)).fillna(0.0)
    S = (BLEND * D.sleeve_weights(px, S3).where(gm, 0.0)).fillna(0.0)
    k = (GROSS / (R + S).sum(axis=1).replace(0, np.nan)).fillna(0.0)
    return R.mul(k, axis=0).fillna(0.0), S.mul(k, axis=0).fillna(0.0)


# --------------------------------------------------- engine.backtest, two independent clocks ----
def run_split(px, A, B, cost_bps, f_eq, f_sl):
    """The engine's drift/cost accounting with each leg on its OWN rebalance clock."""
    rets = px.pct_change().fillna(0.0)
    wA = A.reindex(px.index).fillna(0.0).shift(1)      # decided at t, applied at t+1
    wB = B.reindex(px.index).fillna(0.0).shift(1)
    mA = rebalance_mask(px.index, f_eq).shift(1, fill_value=False).values
    mB = rebalance_mask(px.index, f_sl).shift(1, fill_value=False).values
    n = px.shape[1]
    nT = len(px.index)
    held = np.zeros((nT, n))
    cA = np.zeros(n); cB = np.zeros(n)
    to = np.zeros(nT); toA = np.zeros(nT); toB = np.zeros(nT); gr = np.zeros(nT)
    rv = rets.values; aV = wA.values; bV = wB.values
    for i in range(nT):
        fa = bool(mA[i]) or i == 0
        fb = bool(mB[i]) or i == 0
        if fa or fb:
            dA = (aV[i] - cA) if fa else np.zeros(n)
            dB = (bV[i] - cB) if fb else np.zeros(n)
            d = dA + dB
            ad = np.abs(d); aA = np.abs(dA); aB = np.abs(dB)
            den = aA + aB
            shA = np.divide(aA, den, out=np.zeros_like(aA), where=den > 0)
            to[i] = ad.sum(); toA[i] = (ad * shA).sum(); toB[i] = (ad * (1 - shA)).sum()
            if fa: cA = aV[i].copy()
            if fb: cB = bV[i].copy()
        cur = cA + cB
        held[i] = cur
        gr[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            f = (1 + rv[i]) / tot
            cA = cA * f; cB = cB * f
    idx = px.index
    port = pd.Series((held * rv).sum(axis=1), index=idx) - pd.Series(to, index=idx) * cost_bps / 1e4
    return dict(returns=port, turnover=pd.Series(to, index=idx),
                to_eq=pd.Series(toA, index=idx), to_sl=pd.Series(toB, index=idx),
                gross=pd.Series(gr, index=idx))


# ------------------------------------------------------------------------ scoring ----
def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def score(r, spy, base):
    m = metrics(r); h1, h2 = halves(r)
    ms, mb = metrics(spy), metrics(base)
    s1, s2 = halves(spy); b1, b2 = halves(base)
    ro, so, bo = r.loc[OOS_START:], spy.loc[OOS_START:], base.loc[OOS_START:]
    mo, mso, mbo = metrics(ro), metrics(so), metrics(bo)
    p4a = (h1 > b1) and (h2 > b2) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = (h1 > s1) and (h2 > s2) and (mo["Sharpe"] > mso["Sharpe"]) \
        and (m["MaxDD"] >= DELTA0 * ms["MaxDD"]) and (m["CAGR"] >= PHI0 * ms["CAGR"])
    p4b_oos = (mo["Sharpe"] > mso["Sharpe"]) and (mo["MaxDD"] >= DELTA0 * mso["MaxDD"]) \
        and (mo["CAGR"] >= PHI0 * mso["CAGR"])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                pass4a=p4a, pass4b=p4b, pass4b_oos=p4b_oos,
                SPY_S=ms["Sharpe"], SPY_CAGR=ms["CAGR"], SPY_DD=ms["MaxDD"],
                SPY_OOS_S=mso["Sharpe"], SPY_OOS_CAGR=mso["CAGR"], SPY_OOS_DD=mso["MaxDD"],
                BASE_S=mb["Sharpe"], BASE_CAGR=mb["CAGR"], BASE_DD=mb["MaxDD"],
                BASE_OOS_S=mbo["Sharpe"], BASE_OOS_CAGR=mbo["CAGR"],
                SPY_H1=s1, SPY_H2=s2, BASE_H1=b1, BASE_H2=b2)


def main():
    grid, wf = [], []
    for panel in PANELS:
        px, _ = D.panel_px(panel)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]

        A, B = scaled_legs(px)
        ref = D.book_weights(px, "S3-50", GATE, CONV)
        g1 = float((A + B - ref).abs().to_numpy().max())
        say(f"[G1] {panel}: max|A+B - i133.book_weights(S3-50,band3,rw)| = {g1:.3e}")
        assert g1 < 1e-12, g1

        eng = backtest(px, ref, cost_bps=10.0, freq=FREQ)
        mine = run_split(px, A, B, 10.0, "W", "W")
        g2r = float((eng["returns"] - mine["returns"]).abs().max())
        g2t = float((eng["turnover"] - mine["turnover"]).abs().max())
        say(f"[G2] {panel}: degenerate limit (W,W) vs engine.backtest -- max|dret| = {g2r:.3e}  "
            f"max|dturnover| = {g2t:.3e}")
        assert g2r < 1e-12 and g2t < 1e-12

        g6 = {}
        for f in CLOCKS:                                                    # G6
            e = backtest(px, ref, cost_bps=10.0, freq=f)
            m = run_split(px, A, B, 10.0, f, f)
            g6[f] = (float((e["returns"] - m["returns"]).abs().max()),
                     float((e["turnover"] - m["turnover"]).abs().max()))
        say(f"[G6] {panel}: diagonal (f,f) vs engine.backtest(freq=f) -- "
            + "  ".join(f"{f}: dret {v[0]:.1e} / dTO {v[1]:.1e}" for f, v in g6.items()))
        assert max(max(v) for v in g6.values()) < 1e-12, g6

        for cost in COSTS:
            bres = backtest(px, rules_v2_weights(px), cost_bps=cost, freq=FREQ)
            base = bres["returns"].loc[start:]
            base_to = bres["turnover"].loc[start:]
            yrs = len(base) / 252
            is_yrs = len(base.loc[:IS_END]) / 252
            base_to_is = base_to.loc[:IS_END].sum() / is_yrs
            for fe in CLOCKS:
                for fs in CLOCKS:
                    res = run_split(px, A, B, cost, fe, fs)
                    r = res["returns"].loc[start:]
                    to = res["turnover"].loc[start:].sum() / yrs
                    toe = res["to_eq"].loc[start:].sum() / yrs
                    tos = res["to_sl"].loc[start:].sum() / yrs
                    add = abs(toe + tos - to)
                    assert add < 1e-10, (panel, cost, fe, fs, add)               # G4
                    sc = score(r, spy, base)
                    grid.append(dict(panel=panel, cost_bps=cost, f_eq=fe, f_sl=fs,
                                     same_clock=(fe == fs), TO=to, TO_eq=toe, TO_sl=tos,
                                     sh_eq=toe / to if to else np.nan,
                                     IS_TO=res["turnover"].loc[start:IS_END].sum() / is_yrs,
                                     base_TO=base_to.sum() / yrs, base_TO_is=base_to_is,
                                     mean_gross=res["gross"].loc[start:].mean(),
                                     drag_pp=to * cost / 1e4 * 100, additivity=add, **sc))
        say(f"[G4] {panel}: leg attribution additive at all {len(COSTS)*len(CLOCKS)**2} cells "
            f"(max |TO_eq+TO_sl-TO| = {max(g['additivity'] for g in grid if g['panel']==panel):.2e})")

    G = pd.DataFrame(grid)

    ref_cell = G[(G.panel == "u56") & (G.cost_bps == 10.0) & (G.f_eq == "W") & (G.f_sl == "W")].iloc[0]
    g3 = {k: abs(ref_cell[k] - v) for k, v in REF142.items()}
    say("[G3] u56/10bps/(W,W) vs the Sunday review's idea-142 re-run: "
        + "  ".join(f"{k} d={v:.2e}" for k, v in g3.items()))
    assert max(g3.values()) < 5e-3, g3
    say(f"[G5] {len(G)} of {len(PANELS)*len(COSTS)*len(CLOCKS)**2} cells published.\n")

    # ------------------------------------------------------------------ rule 8 ----
    for panel in PANELS:
        for cost in COSTS:
            cells = [g for g in grid if g["panel"] == panel and g["cost_bps"] == cost]
            pick = max(cells, key=lambda g: g["IS_Sharpe"])
            elig = [g for g in cells if g["IS_TO"] <= g["base_TO_is"]]
            pto = max(elig, key=lambda g: g["IS_Sharpe"]) if elig else None
            pdg = max([g for g in cells if g["same_clock"]], key=lambda g: g["IS_Sharpe"])
            wf.append(dict(panel=panel, cost_bps=cost,
                           C_SHARPE=f"{pick['f_eq']}/{pick['f_sl']}",
                           IS_Sharpe=pick["IS_Sharpe"], IS_TO=pick["IS_TO"],
                           OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                           OOS_MaxDD=pick["OOS_MaxDD"], TO=pick["TO"],
                           pass4a=pick["pass4a"], pass4b=pick["pass4b"],
                           pass4b_oos=pick["pass4b_oos"],
                           C_TO=(f"{pto['f_eq']}/{pto['f_sl']}" if pto else "ABSTAIN"),
                           C_TO_OOS_Sharpe=(pto["OOS_Sharpe"] if pto else np.nan),
                           C_TO_TO=(pto["TO"] if pto else np.nan),
                           C_TO_pass4b=(pto["pass4b"] if pto else False),
                           C_DIAG=f"{pdg['f_eq']}/{pdg['f_sl']}", C_DIAG_TO=pdg["TO"],
                           C_DIAG_OOS_CAGR=pdg["OOS_CAGR"], C_DIAG_OOS_Sharpe=pdg["OOS_Sharpe"],
                           C_DIAG_OOS_MaxDD=pdg["OOS_MaxDD"], C_DIAG_pass4a=pdg["pass4a"],
                           C_DIAG_pass4b=pdg["pass4b"], C_DIAG_pass4b_oos=pdg["pass4b_oos"],
                           BASE_OOS_S=pick["BASE_OOS_S"], SPY_OOS_S=pick["SPY_OOS_S"],
                           BASE_OOS_CAGR=pick["BASE_OOS_CAGR"], SPY_OOS_CAGR=pick["SPY_OOS_CAGR"],
                           base_TO_is=pick["base_TO_is"]))
    WF = pd.DataFrame(wf)

    # -------------------------------------------------------------- the floor table ----
    floor = []
    for panel in PANELS:
        for cost in COSTS:
            c = G[(G.panel == panel) & (G.cost_bps == cost)]
            diag = c[c.same_clock]; off = c[~c.same_clock]
            floor.append(dict(panel=panel, cost_bps=cost,
                              TO_committed_WW=float(c[(c.f_eq == "W") & (c.f_sl == "W")].TO.iloc[0]),
                              TO_min_same_clock=float(diag.TO.min()),
                              argmin_same_clock=diag.loc[diag.TO.idxmin(), "f_eq"],
                              TO_min_split=float(off.TO.min()),
                              argmin_split=f"{off.loc[off.TO.idxmin(),'f_eq']}/{off.loc[off.TO.idxmin(),'f_sl']}",
                              floor_moved_pp=float(off.TO.min() - diag.TO.min()),
                              live_TO=float(c.base_TO.iloc[0]),
                              n4a=int(c.pass4a.sum()), n4b=int(c.pass4b.sum()),
                              nboth=int((c.pass4a & c.pass4b).sum())))
    FL = pd.DataFrame(floor)

    cols = ["panel", "cost_bps", "f_eq", "f_sl", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO", "TO_eq", "TO_sl", "mean_gross",
            "drag_pp", "pass4a", "pass4b", "pass4b_oos"]
    say("=" * 126)
    say("ALL 128 CELLS  (f_eq = equity clock, f_sl = sleeve clock; (W,W) is the committed cell)")
    say("=" * 126)
    say(G[cols].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("BENCHMARKS (same sample, per panel per cost rung)")
    say(G[["panel", "cost_bps", "BASE_CAGR", "BASE_S", "BASE_DD", "BASE_H1", "BASE_H2",
           "BASE_OOS_CAGR", "BASE_OOS_S", "SPY_CAGR", "SPY_S", "SPY_DD", "SPY_H1", "SPY_H2",
           "SPY_OOS_CAGR", "SPY_OOS_S", "SPY_OOS_DD", "base_TO"]].drop_duplicates()
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 126)
    say("THE TURNOVER FLOOR: split clocks vs the same-clock family")
    say("=" * 126)
    say(FL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 126)
    say("RULE 8 WALK-FORWARD (clock pair chosen on 2009-2016 only; 2017-2026 read once)")
    say("=" * 126)
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")

    say("=" * 126)
    say("HYPOTHESES")
    say("=" * 126)
    for panel in PANELS:
        f10 = FL[(FL.panel == panel) & (FL.cost_bps == 10.0)].iloc[0]
        say(f"H1  {panel} @10 bps: committed (W,W) trades {f10.TO_committed_WW:.2f}x/yr.  The best "
            f"SAME-clock rung is {f10.argmin_same_clock} at {f10.TO_min_same_clock:.2f}x; the best "
            f"SPLIT pair is {f10.argmin_split} at {f10.TO_min_split:.2f}x.  The split moves the "
            f"floor by {f10.floor_moved_pp:+.2f}x/yr against the live book's {f10.live_TO:.2f}x.")
    for panel in PANELS:
        c = G[(G.panel == panel) & (G.cost_bps == 10.0)]
        piv = c.pivot(index="f_eq", columns="f_sl", values="TO").reindex(index=CLOCKS, columns=CLOCKS)
        say(f"\nH2  {panel} @10 bps -- annual turnover, equity clock (rows) x sleeve clock (cols):")
        say(piv.to_string(float_format=lambda x: f"{x:.3f}"))
        pv2 = c.pivot(index="f_eq", columns="f_sl", values="Sharpe").reindex(index=CLOCKS, columns=CLOCKS)
        say(f"    ... and full-sample Sharpe on the same grid:")
        say(pv2.to_string(float_format=lambda x: f"{x:.4f}"))
    say("")
    n4a, n4b = int(G.pass4a.sum()), int(G.pass4b.sum())
    nboth = int((G.pass4a & G.pass4b).sum())
    say(f"H3  KEEP paths over all {len(G)} cells: 4a passes {n4a}, 4b passes {n4b}, BOTH {nboth}.")
    both = G[G.pass4a & G.pass4b]
    if len(both):
        say(both[["panel", "cost_bps", "f_eq", "f_sl", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "TO"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        say(f"    of which SPLIT (off-diagonal): {int((~both.same_clock).sum())} of {len(both)}.")
    say("")
    say(f"H4  the Sunday bar (a both-paths cell at 25 bps or worse): "
        f"{int(((G.cost_bps >= 25) & G.pass4a & G.pass4b).sum())} of "
        f"{int((G.cost_bps >= 25).sum())} cells at 25/50 bps clear BOTH paths.")
    say(f"H5  rule 8, C_SHARPE picks {dict(WF.C_SHARPE.value_counts())} over the {len(WF)} "
        f"panel x cost cells; {int(WF.pass4b.sum())} clear 4b FULL, {int(WF.pass4b_oos.sum())} "
        f"clear 4b OOS, {int(WF.pass4a.sum())} clear 4a.")
    say(f"H6  rule 8, C_TO (IS turnover <= the live book's own IS turnover) picks "
        f"{dict(WF.C_TO.value_counts())}; {int(WF.C_TO_pass4b.sum())} of {len(WF)} clear 4b FULL.")
    gmin = G.loc[G.groupby(['panel'])['TO'].idxmin()]
    say(f"H7  THE DEVICE'S OWN VERDICT: of the {int((~G.same_clock).sum())} SPLIT cells, "
        f"{int(sum((G[~G.same_clock].TO.values < [G[(G.panel==p)&(G.cost_bps==c)&G.same_clock].TO.min() for p,c in zip(G[~G.same_clock].panel,G[~G.same_clock].cost_bps)])))} "
        f"trade LESS than their own (panel,cost) cell's best SAME-clock rung.")
    say(f"H7b rule 8, C_DIAG (POST-HOC, IS-Sharpe argmax over the 4 SAME-CLOCK rungs only) picks "
        f"{dict(WF.C_DIAG.value_counts())}; 4a {int(WF.C_DIAG_pass4a.sum())} of {len(WF)}, "
        f"4b FULL {int(WF.C_DIAG_pass4b.sum())}, 4b OOS {int(WF.C_DIAG_pass4b_oos.sum())}, "
        f"turnover {WF.C_DIAG_TO.min():.2f}-{WF.C_DIAG_TO.max():.2f}x/yr.")
    say(f"H8  the lowest turnover ANY clock pair reaches: "
        + "; ".join(f"{r.panel} {r.TO:.2f}x/yr at ({r.f_eq},{r.f_sl}) vs live {r.base_TO:.2f}x"
                    for _, r in gmin.iterrows()))

    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    FL.to_csv(OUT / f"{STEM}.floor.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    (OUT / f"{STEM}.log.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
