#!/usr/bin/env python3
"""QUEUE idea 463 — does-the-live-4b-candidate-beat-its-own-EWall-at-25-bps-on-any-panel
(cloud, 2026-09-10)

PRE-REGISTERED QUESTION (verbatim from QUEUE.md idea 463, written before any number below was read)
    "idea 460's cross-link: U56 top-20 equal weight (the 2026-09-04 KEEP 4b candidate) beats its
     un-ranked control at 10 bps (+0.0728) and LOSES at 25 bps (-0.0284), where its 4b clears on
     the DD cap alone.  Sweep n and cadence for the smallest book-form that beats EW_ALL at BOTH
     rungs on U56 and holds it out of sample; if none exists, the candidate's edge is a cost-rung
     fact and PROTOCOL should say so.  Max 2 params (n, freq)."

WHY IT MATTERS — this is the live candidate, not a census
    The 2026-09-04 KEEP 4b candidate (top-20 equal weight, no vol scaler, weekly) is the only book
    in the record on a path to real capital.  A book whose entire measured edge over EQUAL WEIGHT
    evaporates between 10 and 25 bps is not a ranking edge; it is a statement about the cost rung
    the record happens to quote.  Real capital pays a rung it does not choose.  So the question is
    not whether some (n, freq) can be found that wins at both rungs — with 40 forms one usually can
    — but whether the winner is CHOSEN WITHOUT LOOKING AT THE ANSWER and still wins out of sample.
    That is what rule 8 is for and it is the whole test here.

THE DECISIVE QUANTITY (defined before the design, because it drives it)
    Cost reaches a return series only through turnover: r(c) = r0 - turnover * c/1e4 exactly (no
    instrument here reads equity, so the identity is exact and is ASSERTED in gate G3).  Therefore
    every arm has a BREAKEVEN COST c* — the rung at which its Sharpe advantage over its own EW_ALL
    crosses zero — and c* is a property of the arm, computable exactly, not a grid artefact.  A
    "cost-rung fact" then has a number attached: the candidate's edge is a cost-rung fact IF AND
    ONLY IF its c* sits inside the range of rungs the record quotes.  c* is reported for every arm
    and is the transferable output of this run.

WHAT IS SWEPT (all 480 points published in .grid.csv; nothing is selected on but the two params)
    n        3, 5, 8, 10, 15, 20, 25, 30, 40, 50 — the ranked book's depth.  20 is the live
             candidate; 50 is included on every panel as the CONVERGENCE control (on U56, n = 50
             of 56 names is EW_ALL in all but name, so dSharpe must go to ~0 there or the
             comparand is wrong).
    freq     D, W, M, Q — the rebalance cadence.  W is the live candidate's.
    rungs    0, 10, 25, 50 bps — ALL reported.  10 and 25 are the queue's two; 0 is the control
             that decides whether the question is a cost question at all; 50 is PROTOCOL's stress.
    panels   U56, B136, SMALL439 — "on any panel" is in the title, so all three are run.
    control  EW_ALL at the SAME panel, SAME cadence and SAME rung.  Matching the cadence matters:
             an un-matched control would credit the ranked book with the cadence's own turnover.
    = 10 n x 4 freq x 3 panels = 120 arms + 12 matched EW_ALL controls, read at 4 rungs = 528 rows.

TUNED PARAMETERS: exactly two, per PROTOCOL 4 — n (10 values) and freq (4 values).  Panels, cost
    rungs, both KEEP paths and both selectors are REPORTED AXES, never selected on.

RULE 8 (PROTOCOL 8, required, and the point of the run): the form is chosen on 2009/2011-2016
    ALONE by a criterion fixed before any OOS number was read — S1, the queue's own words: among
    forms whose IS dSharpe vs their own matched EW_ALL is > 0 at BOTH 10 and 25 bps, take the
    SMALLEST n (tie-break: lowest IS turnover); abstain to EW_ALL if the set is empty.  S2 (max IS
    dSharpe at 25 bps) is reported beside it as a robustness read, not as a third parameter.
    2017-2026 is then read ONCE: OOS dSharpe at both rungs, and OOS CAGR/Sharpe/MaxDD against the
    arm's own EW_ALL, the LIVE RULES v2 book (cost-matched), RULES v1 and SPY.

KEEP PATHS (PROTOCOL 4, on every arm row and every rule-8 pick)
    4a  Sharpe > RULES v2 in BOTH halves and MaxDD no worse, cost-matched.
    4b  the FIVE bars: Sharpe > SPY in both halves AND out of sample, MaxDD <= 60% of SPY's, CAGR
        >= 70% of SPY's.  NOTE: idea 460's committed grid used the FOUR-bar form (no OOS bar); the
        G1 gate below therefore reproduces its Sharpe/MaxDD/dSharpe columns, which are unaffected,
        and this file's 4b column is the protocol-correct five-bar one and will differ from 460's.
    A third column, 4b AND beats its own EW_ALL at the rung, is idea 460's stricter clause and is
    the one the queue's premise is about.

WINDOW: idea 460's COMMON window (the intersection of the three panels' post-warm-up indices) is
    the headline, so the gate reproduces and the three panels are comparable.  U56 on its own
    NATIVE window is reported beside the adopted form and the rule-8 picks, because the 2026-09-04
    candidate was published there and a window change is not a free comparison.

GATES (all must print PASS before any new statistic is read)
    G1  idea 460's committed grid reproduces on the shared rows: U56 TOP20 dSharpe +0.072778 at
        10 bps and -0.028406 at 25 bps, Sharpe 1.141922 / 1.029863, MaxDD -0.193888, mean drifted
        gross 0.726509 — off 460's own imported book builders.  This is the premise check.
    G2  `fast_backtest` equals `engine.backtest` on returns AND turnover, at W and at M.
    G3  the cost identity r(c) = r0 - turnover*c/1e4, so c* is exact rather than interpolated.
    G4  IS and OOS disjoint and exhaustive over the common window.

PRE-REGISTERED PREDICTIONS (written before the main grid was read)
    P1  Some (n, freq) will beat EW_ALL at both rungs on U56 full-sample — 40 forms is a lot of
        forms — and it will be a SLOW cadence (M or Q), because the loss between 10 and 25 bps is
        a turnover loss and cadence is the turnover dial.
    P2  The rule-8 pick will NOT hold at 25 bps out of sample.  If P2 is right the answer to the
        queue is its own second clause: the edge is a cost-rung fact and PROTOCOL should say so.
    P3  c* for the live candidate (U56, n = 20, W) will land between 10 and 25 bps, near 17-18,
        which is BELOW the 25 bps rung PROTOCOL already stresses and inside the range real capital
        pays.

CAVEATS carried, not buried
    * SURVIVORSHIP (idea 54): all three panels are current-constituent lists.  SMALL439 is a
      sub-$2B screen run TODAY and back-filled, with data/small_meta.csv's `max_1d_move >= 1.0`
      names dropped first (idea 118; idea 627: that filter is itself terminal-dated).  A ranked
      book on a survivorship-biased panel is flattered MORE than its equal-weight control, because
      ranking concentrates into the survivors, so every dSharpe on SMALL439 is an UPPER bound.
    * U56 and B136 hold SPY as a constituent (idea 460's convention, carried verbatim), so the
      panel's own benchmark is inside the control book.  Stated because it shrinks dSharpe.
    * Cadence is not a pure cost dial: D/W/M/Q change WHEN the book sees its signal as well as how
      often it trades.  That is why c* — which changes drag and nothing else — is the arbiter here
      and cadence is a reported axis.
    * MaxDD is one number off one path and the 4b DD cap turns on exactly that number (idea 321).
    * Idea 126: t+1 execution, no lag band.  Idea 38: U56/B136 carry the calendar-day index.

Deterministic, standalone.  Modifies nothing.  Writes .console.txt, .grid.csv, .cstar.csv,
.walkforward.csv next to itself.
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest as engine_backtest, metrics  # noqa: E402

STEM = "2026-09-10_does-the-live-4b-candidate-beat-its-own-EWall-at-25-bps-on-any-panel_cloud"
OUT = ROOT / "research" / "backtests"
I460 = OUT / "2026-09-08_back-fill-the-EWall-column-on-panel-ordering-files_cloud.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load(I460, "i460")
fast_backtest, net, mstats = M.fast_backtest, M.net, M.mstats
topn_weights, dg_weights = M.topn_weights, M.dg_weights
GROSS, IS_END, OOS_START = M.GROSS, M.IS_END, M.OOS_START

NS = [3, 5, 8, 10, 15, 20, 25, 30, 40, 50]
FREQS = ["D", "W", "M", "Q"]
RUNGS = [0, 10, 25, 50]
PANELS = ["U56", "B136", "SMALL439"]
LIVE = (20, "W")                       # the 2026-09-04 KEEP 4b candidate
PHI, DELTA = 0.70, 0.60

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def bars5(r, sb):
    """The five 4b bars against the SPY reference dict sb."""
    h = len(r) // 2
    m = metrics(r)
    return dict(H1=sharpe(r.iloc[:h]) - sb["H1"], H2=sharpe(r.iloc[h:]) - sb["H2"],
                OOS=sharpe(r.loc[OOS_START:]) - sb["OOS"],
                DD=DELTA * abs(sb["MaxDD"]) - abs(m["MaxDD"]),
                CAGR=m["CAGR"] - PHI * sb["CAGR"])


def cstar(r0a, toa, r0b, tob, lo=0.0, hi=200.0, tol=1e-4):
    """Exact breakeven cost (bps) where Sharpe(a) - Sharpe(b) crosses zero, off the cost identity.
    Returns nan when the sign does not change on [lo, hi]; the sign at each end is reported."""
    f = lambda c: sharpe(r0a - toa * c / 1e4) - sharpe(r0b - tob * c / 1e4)
    flo, fhi = f(lo), f(hi)
    if not np.isfinite(flo) or not np.isfinite(fhi) or flo * fhi > 0:
        return np.nan
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# ================================================================== main
def main():
    say("=" * 195)
    say("IDEA 463 — does the live 4b candidate (U56 top-20 EW, weekly) beat its OWN EW_ALL at 25 "
        "bps on ANY panel, and does the smallest form that does hold OUT OF SAMPLE?  (cloud)")
    say(f"10 n x 4 cadences x 3 panels, matched EW_ALL control, rungs {RUNGS} bps.  "
        f"IS <= {IS_END}, OOS >= {OOS_START}.  t+1, book gross {GROSS:.0%}.")
    say("=" * 195)

    PX = M.panels()
    idx = None
    for k in PANELS:
        own = PX[k][0].index[260:]
        idx = own if idx is None else idx.intersection(own)
    say(f"\ncommon window {idx[0].date()} -> {idx[-1].date()} ({len(idx)} days, {len(idx)/252:.1f}y)"
        "  [idea 460's convention, so G1 reproduces and the panels are comparable]")

    # ---------------------------------------------------------------- gates G2 / G3 / G4
    upx, ucols = PX["U56"]
    st = upx.index[260]
    w2 = rules_v2_weights(upx)
    for fq in ("W", "M"):
        e = engine_backtest(upx, w2, cost_bps=10, freq=fq)
        f = fast_backtest(upx, w2, freq=fq)
        dr = float(np.abs((net(f, 10) - e["returns"]).loc[st:].values).max())
        dt = float(np.abs((f["turnover"] - e["turnover"]).loc[st:].values).max())
        say(f"[G2] fast_backtest vs engine.backtest @{fq}: max|d returns| {dr:.3e}, "
            f"max|d turnover| {dt:.3e} -> {'PASS' if dr < 1e-12 and dt < 1e-12 else 'FAIL'}")
        assert dr < 1e-12 and dt < 1e-12
    f = fast_backtest(upx, w2)
    d3 = float(np.abs(net(f, 25) - (f["returns0"] - f["turnover"] * 25 / 1e4)).max())
    say(f"[G3] cost identity r(c) = r0 - turnover*c/1e4: max|d| {d3:.3e} -> "
        f"{'PASS' if d3 == 0.0 else 'FAIL'}  (so c* below is exact, not interpolated)")
    isx, oox = idx[idx <= IS_END], idx[idx >= OOS_START]
    g4 = len(isx.intersection(oox)) == 0 and len(isx) + len(oox) == len(idx)
    say(f"[G4] IS {isx[0].date()}..{isx[-1].date()} ({len(isx)}) / OOS {oox[0].date()}.."
        f"{oox[-1].date()} ({len(oox)}); overlap {len(isx.intersection(oox))}, union "
        f"{len(isx)+len(oox)} vs {len(idx)} -> {'PASS' if g4 else 'FAIL'}")

    # ---------------------------------------------------------------- simulate
    R0, TO, GR = {}, {}, {}
    for k in PANELS:
        px, cols = PX[k]
        for fq in FREQS:
            res = fast_backtest(px, dg_weights(px, pd.DataFrame(True, index=px[cols].index,
                                                                columns=px[cols].columns), cols=cols), freq=fq)
            R0[(k, "EWALL", fq)] = res["returns0"].reindex(idx)
            TO[(k, "EWALL", fq)] = res["turnover"].reindex(idx)
            GR[(k, "EWALL", fq)] = float(res["gross"].reindex(idx).mean())
            for n in NS:
                res = fast_backtest(px, topn_weights(px, n, cols), freq=fq)
                R0[(k, n, fq)] = res["returns0"].reindex(idx)
                TO[(k, n, fq)] = res["turnover"].reindex(idx)
                GR[(k, n, fq)] = float(res["gross"].reindex(idx).mean())
        for nm, W in (("RULESV2", rules_v2_weights(px)), ("RULESV1", rules_v1_weights(px))):
            res = fast_backtest(px, W, freq="W")
            R0[(k, nm, "W")] = res["returns0"].reindex(idx)
            TO[(k, nm, "W")] = res["turnover"].reindex(idx)
        say(f"  {k}: {len(cols)} held names, {len(FREQS) * (len(NS) + 1) + 2} books simulated")

    spy = PX["U56"][0]["SPY"].pct_change().fillna(0.0).reindex(idx)
    h = len(spy) // 2
    ms = metrics(spy)
    SB = dict(H1=sharpe(spy.iloc[:h]), H2=sharpe(spy.iloc[h:]), OOS=sharpe(spy.loc[OOS_START:]),
              MaxDD=ms["MaxDD"], CAGR=ms["CAGR"])
    mso = metrics(spy.loc[OOS_START:])
    say(f"\nSPY on the common window: CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.4f} MaxDD "
        f"{ms['MaxDD']:.2%}  halves {SB['H1']:.4f}/{SB['H2']:.4f}  OOS {mso['CAGR']:.2%}/"
        f"{SB['OOS']:.4f}/{mso['MaxDD']:.2%}   4b bars: DD cap {DELTA*abs(ms['MaxDD']):.2%}, "
        f"CAGR floor {PHI*ms['CAGR']:.2%}")

    yrs = len(idx) / 252.0
    rows = []
    for k in PANELS:
        for fq in FREQS:
            for n in NS + ["EWALL"]:
                for c in RUNGS:
                    r = R0[(k, n, fq)] - TO[(k, n, fq)] * c / 1e4
                    e = R0[(k, "EWALL", fq)] - TO[(k, "EWALL", fq)] * c / 1e4
                    v2 = R0[(k, "RULESV2", "W")] - TO[(k, "RULESV2", "W")] * c / 1e4
                    m, me, mv = mstats(r), mstats(e), mstats(v2)
                    b = bars5(r, SB)
                    mo = metrics(r.loc[OOS_START:])
                    rows.append(dict(
                        panel=k, n=str(n), freq=fq, bps=c, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                        MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"], gross=GR[(k, n, fq)],
                        turnover_yr=float(TO[(k, n, fq)].sum() / yrs),
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        EW_Sharpe=me["Sharpe"], dSharpe=m["Sharpe"] - me["Sharpe"],
                        dCAGR=m["CAGR"] - me["CAGR"],
                        OOS_dSharpe=mo["Sharpe"] - metrics(e.loc[OOS_START:])["Sharpe"],
                        IS_dSharpe=(sharpe(r.loc[:IS_END]) - sharpe(e.loc[:IS_END])),
                        pass4a=bool(m["H1"] > mv["H1"] and m["H2"] > mv["H2"]
                                    and m["MaxDD"] >= mv["MaxDD"]),
                        pass4b=bool(all(b[x] > 0 for x in ("H1", "H2", "OOS", "DD", "CAGR"))),
                        beats_EW=bool(m["Sharpe"] > me["Sharpe"]),
                        **{"m_" + x: b[x] for x in ("H1", "H2", "OOS", "DD", "CAGR")}))
    G = pd.DataFrame(rows)
    G["pass4b_and_beats_EW"] = G["pass4b"] & G["beats_EW"]
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"\nGRID: {len(G)} rows ({len(G[G['n'] != 'EWALL'])} arms + "
        f"{len(G[G['n'] == 'EWALL'])} matched controls) — all published in .grid.csv")

    # ---------------------------------------------------------------- G1
    liv = G[(G["panel"] == "U56") & (G["n"] == "20") & (G["freq"] == "W")].set_index("bps")
    d10, d25 = liv.loc[10, "dSharpe"], liv.loc[25, "dSharpe"]
    ok = (abs(d10 - 0.072778) < 5e-6 and abs(d25 + 0.028406) < 5e-6
          and abs(liv.loc[10, "Sharpe"] - 1.141922) < 5e-6
          and abs(liv.loc[25, "Sharpe"] - 1.029863) < 5e-6
          and abs(liv.loc[10, "MaxDD"] + 0.193888) < 5e-6
          and abs(liv.loc[10, "gross"] - 0.726509) < 5e-6)
    say(f"\n[G1] idea 460's premise, U56 TOP20 weekly: dSharpe @10 {d10:+.6f} (published "
        f"+0.072778), @25 {d25:+.6f} (-0.028406); Sharpe {liv.loc[10,'Sharpe']:.6f}/"
        f"{liv.loc[25,'Sharpe']:.6f} (1.141922/1.029863); MaxDD {liv.loc[10,'MaxDD']:.6f} "
        f"(-0.193888); gross {liv.loc[10,'gross']:.6f} (0.726509) -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        raise SystemExit("G1 failed — idea 460's premise does not reproduce")

    # ---------------------------------------------------------------- A1
    say(f"\n{'=' * 195}\nA1  THE QUEUE'S QUESTION — which (n, freq) beat their OWN matched EW_ALL "
        f"at BOTH 10 and 25 bps, full sample?")
    arms = G[G["n"] != "EWALL"]
    piv = arms.pivot_table(index=["panel", "freq"], columns=["bps"], values="dSharpe",
                           aggfunc=lambda s: np.nan)  # placeholder, real tables below
    for k in PANELS:
        sub = arms[arms["panel"] == k]
        t10 = sub[sub["bps"] == 10].pivot(index="n", columns="freq", values="dSharpe")
        t25 = sub[sub["bps"] == 25].pivot(index="n", columns="freq", values="dSharpe")
        t10 = t10.reindex([str(x) for x in NS])[FREQS]
        t25 = t25.reindex([str(x) for x in NS])[FREQS]
        say(f"\n  {k}  dSharpe vs matched EW_ALL   @10 bps                    @25 bps")
        say(pd.concat({"10bps": t10, "25bps": t25}, axis=1).to_string(
            float_format=lambda x: f"{x:+.4f}"))
        both = (t10 > 0) & (t25 > 0)
        say(f"  beats EW_ALL at BOTH rungs: {int(both.values.sum())} of {both.size} forms"
            + ("" if not both.values.sum() else
               "  ->  " + ", ".join(f"n={i}/{c}" for i in both.index for c in both.columns
                                    if bool(both.loc[i, c]))))
    a10 = arms[arms["bps"] == 10].set_index(["panel", "n", "freq"])["dSharpe"]
    a25 = arms[arms["bps"] == 25].set_index(["panel", "n", "freq"])["dSharpe"]
    say(f"\n  POOLED over 120 forms: beats EW_ALL at 10 bps {int((a10 > 0).sum())}/120, at 25 bps "
        f"{int((a25 > 0).sum())}/120, at BOTH {int(((a10 > 0) & (a25 > 0)).sum())}/120, "
        f"at 0 bps {int((arms[arms['bps'] == 0]['dSharpe'] > 0).sum())}/120, at 50 bps "
        f"{int((arms[arms['bps'] == 50]['dSharpe'] > 0).sum())}/120.")

    # ---------------------------------------------------------------- A2: c*
    say(f"\n{'=' * 195}\nA2  THE BREAKEVEN COST c* — the rung at which each arm's Sharpe edge over "
        f"its OWN EW_ALL crosses zero (exact, off the cost identity)")
    cs = []
    for k in PANELS:
        for fq in FREQS:
            for n in NS:
                c = cstar(R0[(k, n, fq)], TO[(k, n, fq)], R0[(k, "EWALL", fq)], TO[(k, "EWALL", fq)])
                cs.append(dict(panel=k, n=n, freq=fq, cstar_bps=c,
                               d0=sharpe(R0[(k, n, fq)]) - sharpe(R0[(k, "EWALL", fq)]),
                               to_yr=float(TO[(k, n, fq)].sum() / yrs),
                               ew_to_yr=float(TO[(k, "EWALL", fq)].sum() / yrs)))
    CS = pd.DataFrame(cs)
    CS.to_csv(OUT / f"{STEM}.cstar.csv", index=False)
    for k in PANELS:
        t = CS[CS["panel"] == k].pivot(index="n", columns="freq", values="cstar_bps")
        say(f"\n  {k}  c* (bps; nan = no crossing on [0, 200], sign given by d0):")
        say(t.reindex(NS)[FREQS].to_string(float_format=lambda x: f"{x:8.2f}"))
    lv = CS[(CS["panel"] == "U56") & (CS["n"] == 20) & (CS["freq"] == "W")].iloc[0]
    say(f"\n  THE LIVE CANDIDATE (U56, n=20, weekly): c* = {lv['cstar_bps']:.2f} bps, zero-cost "
        f"edge {lv['d0']:+.4f}, turnover {lv['to_yr']:.2f}x/yr vs EW_ALL {lv['ew_to_yr']:.2f}x/yr.")
    fin = CS[CS["cstar_bps"].notna()]
    say(f"  Over the 120 forms: {len(fin)} have a crossing inside [0, 200] bps; median c* "
        f"{fin['cstar_bps'].median():.1f}, and {int((fin['cstar_bps'] < 25).sum())} of {len(fin)} "
        f"cross BELOW the 25 bps rung PROTOCOL already stresses.")
    say(f"  {int((CS['d0'] <= 0).sum())} of 120 forms do not beat EW_ALL even at ZERO cost — for "
        f"those the question is not a cost question at all.")

    # ---------------------------------------------------------------- A3: rule 8
    say(f"\n{'=' * 195}\nA3  RULE 8 — the form is chosen on {isx[0].date()}..{isx[-1].date()} ALONE, "
        f"then 2017-2026 is read ONCE")
    say("  S1 (the queue's own criterion): among forms with IS dSharpe > 0 at BOTH 10 and 25 bps, "
        "take the SMALLEST n; tie-break lowest IS turnover; abstain to EW_ALL if empty.")
    say("  S2 (robustness, not a third parameter): the form with the highest IS dSharpe at 25 bps.")
    wf = []
    for k in PANELS:
        cand = []
        for fq in FREQS:
            for n in NS:
                r0, to = R0[(k, n, fq)], TO[(k, n, fq)]
                e0, eo = R0[(k, "EWALL", fq)], TO[(k, "EWALL", fq)]
                d = {}
                for c in (10, 25):
                    d[c] = (sharpe((r0 - to * c / 1e4).loc[:IS_END])
                            - sharpe((e0 - eo * c / 1e4).loc[:IS_END]))
                cand.append(dict(n=n, freq=fq, IS_d10=d[10], IS_d25=d[25],
                                 IS_to=float(to.loc[:IS_END].sum())))
        C = pd.DataFrame(cand)
        el = C[(C["IS_d10"] > 0) & (C["IS_d25"] > 0)].sort_values(["n", "IS_to"])
        say(f"\n  {k}: {len(el)} of 40 forms beat EW_ALL at BOTH rungs IN SAMPLE"
            + ("" if el.empty else f" — smallest n available: {int(el.iloc[0]['n'])}"))
        picks = [("S1", (None if el.empty else (int(el.iloc[0]["n"]), el.iloc[0]["freq"]))),
                 ("S2", (int(C.loc[C["IS_d25"].idxmax(), "n"]), C.loc[C["IS_d25"].idxmax(), "freq"]))]
        for sel, pk in picks:
            for c in (10, 25):
                if pk is None:
                    say(f"    {sel} @{c}bps: ABSTAIN to EW_ALL (no form qualifies in sample)")
                    n, fq = "EWALL", "W"
                else:
                    n, fq = pk
                r = (R0[(k, n, fq)] - TO[(k, n, fq)] * c / 1e4)
                e = (R0[(k, "EWALL", fq)] - TO[(k, "EWALL", fq)] * c / 1e4)
                v2 = (R0[(k, "RULESV2", "W")] - TO[(k, "RULESV2", "W")] * c / 1e4)
                v1 = (R0[(k, "RULESV1", "W")] - TO[(k, "RULESV1", "W")] * c / 1e4)
                mo, meo = metrics(r.loc[OOS_START:]), metrics(e.loc[OOS_START:])
                mv2, mv1 = metrics(v2.loc[OOS_START:]), metrics(v1.loc[OOS_START:])
                b = bars5(r, SB)
                mf, mvf = mstats(r), mstats(v2)
                wf.append(dict(panel=k, selector=sel, bps=c, pick=f"n={n}/{fq}",
                               abstained=(pk is None),
                               is_live=bool(pk == LIVE),
                               IS_d25=(np.nan if pk is None else
                                       float(C[(C["n"] == n) & (C["freq"] == fq)]["IS_d25"].iloc[0])),
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                               OOS_EW_Sharpe=meo["Sharpe"], OOS_dSharpe=mo["Sharpe"] - meo["Sharpe"],
                               OOS_beats_EW=bool(mo["Sharpe"] > meo["Sharpe"]),
                               OOS_RULESV2_Sharpe=mv2["Sharpe"], OOS_RULESV1_Sharpe=mv1["Sharpe"],
                               OOS_SPY_Sharpe=SB["OOS"], OOS_SPY_CAGR=mso["CAGR"],
                               OOS_SPY_MaxDD=mso["MaxDD"],
                               OOS_beats_SPY=bool(mo["Sharpe"] > SB["OOS"]),
                               pass4a=bool(mf["H1"] > mvf["H1"] and mf["H2"] > mvf["H2"]
                                           and mf["MaxDD"] >= mvf["MaxDD"]),
                               pass4b=bool(all(b[x] > 0 for x in ("H1", "H2", "OOS", "DD", "CAGR")))))
                w = wf[-1]
                say(f"    {sel} @{c}bps pick {w['pick']:10s} IS d25 {w['IS_d25']:+.4f}  ->  OOS "
                    f"{w['OOS_CAGR']:7.2%} / {w['OOS_Sharpe']:.4f} / {w['OOS_MaxDD']:7.2%}   "
                    f"OOS dSharpe vs its own EW_ALL {w['OOS_dSharpe']:+.4f}   "
                    f"[EW {w['OOS_EW_Sharpe']:.4f}, v2 {w['OOS_RULESV2_Sharpe']:.4f}, "
                    f"v1 {w['OOS_RULESV1_Sharpe']:.4f}, SPY {SB['OOS']:.4f}]  4a "
                    f"{w['pass4a']} 4b {w['pass4b']}")
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(f"\n  rule-8 summary: picks beating their own EW_ALL out of sample "
        f"{int(WF['OOS_beats_EW'].sum())}/{len(WF)}; beating SPY {int(WF['OOS_beats_SPY'].sum())}"
        f"/{len(WF)}; 4a {int(WF['pass4a'].sum())}, 4b {int(WF['pass4b'].sum())}.")
    at25 = WF[(WF["bps"] == 25) & (~WF["abstained"])]
    say(f"  AT THE 25 BPS RUNG specifically: {int(at25['OOS_beats_EW'].sum())} of {len(at25)} "
        f"non-abstaining picks still beat their own EW_ALL out of sample.")

    # ---------------------------------------------------------------- live candidate, native window
    say(f"\n{'=' * 195}\nTHE LIVE CANDIDATE ON ITS OWN NATIVE WINDOW (published 2026-09-04 on U56 "
        f"without the small panel's start date imposed)")
    px, cols = PX["U56"]
    nidx = px.index[260:]
    for c in (10, 25):
        rr = fast_backtest(px, topn_weights(px, 20, cols))
        ee = fast_backtest(px, dg_weights(px, pd.DataFrame(True, index=px[cols].index,
                                                           columns=px[cols].columns), cols=cols))
        r = net(rr, c).reindex(nidx)
        e = net(ee, c).reindex(nidx)
        m, me = mstats(r), mstats(e)
        say(f"  @{c}bps  TOP20 {m['CAGR']:7.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:7.2%}   "
            f"EW_ALL {me['CAGR']:7.2%} / {me['Sharpe']:.4f} / {me['MaxDD']:7.2%}   "
            f"dSharpe {m['Sharpe'] - me['Sharpe']:+.4f}")
    cn = cstar(rr["returns0"].reindex(nidx), rr["turnover"].reindex(nidx),
               ee["returns0"].reindex(nidx), ee["turnover"].reindex(nidx))
    say(f"  native-window c* = {cn:.2f} bps (common-window c* = {lv['cstar_bps']:.2f}).")

    # ---------------------------------------------------------------- KEEP paths
    say(f"\n{'=' * 195}\nKEEP PATHS on all {len(G)} rows: 4a {int(G['pass4a'].sum())}, "
        f"4b {int(G['pass4b'].sum())}, 4b AND beats its own EW_ALL "
        f"{int(G['pass4b_and_beats_EW'].sum())}, BOTH 4a and 4b "
        f"{int((G['pass4a'] & G['pass4b']).sum())}.")
    say("  4b passers by panel x rung:")
    say(G[G["pass4b"]].groupby(["panel", "bps"]).size().to_string())
    kk = G[G["pass4b_and_beats_EW"] & (G["bps"] == 25)]
    if len(kk):
        say(f"\n  the population the queue asks for — 4b AND beats its own EW_ALL AT 25 BPS "
            f"({len(kk)} rows):")
        say(kk[["panel", "n", "freq", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "dSharpe",
                "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "OOS_dSharpe", "turnover_yr", "pass4a"]]
            .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        say("\n  NO row passes 4b AND beats its own EW_ALL at 25 bps, on any panel.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
