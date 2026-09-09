#!/usr/bin/env python3
"""IDEA 317R ADDENDUM — reconciling lane B with the concurrent cloud run   (2026-09-09)

WHY THIS EXISTS
    Two runs of QUEUE idea 317 landed on 2026-09-09 within minutes of each other and reached
    OPPOSITE recommendations:

      cloud  720 books, 3 panels x 30 ORDERED pairs drawn from a 6-book menu that INCLUDES
             CASH, x 8 states.  Single-leg full-sample pass rates CAGR 4.2%, Sharpe 6.2%,
             MaxDD 8.2%; the joint ALL3 bar 2/720 = 0.3%.  Recommends the bar as PROTOCOL 4c.
      lane B 288 books, 3 panels x 6 NAMED clause families from the record x 4 states x 4 q,
             no CASH parent.  Single-leg full-sample CAGR 7.3%, Sharpe 28.5%, MaxDD 51.7%.
             Recommends AGAINST a gate, on a placebo the cloud run does not have.

    The Sharpe leg differs 4.6x and the MaxDD leg 6.3x.  This script tests the one structural
    difference between the corpora that can produce a gap that size: the cloud menu admits
    CASH as a parent, and lane B's does not.

WHAT IS RUN
    Lane B's exact machinery, corpus, states, panels and pinned settings, with ONE change: the
    risk-off parent B is replaced by CASH (gross 0).  5 risk-on books x 4 states x 4 q x 3
    panels = 240 CASH-parent cells, reported beside the 240 non-degenerate lane-B cells.

    MATCHED GROSS IS UNDEFINED against CASH.  A cash parent has mean gross 0, so there is no
    scalar that brings it to C's exposure; the only available convention is to leave it at 0.
    That is stated, not hidden, and it is the point: the leg outcomes below are then FIXED BY
    CONSTRUCTION, not measured.

TUNED PARAMETERS: 0 new.  Everything is inherited from the lane B script it imports.
Outputs (committed): _addendum.console.txt  _addendum.cash.csv
Deterministic; no network.
"""
from __future__ import annotations
import sys, time, importlib.util
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe  # noqa
from engine import metrics  # noqa

_spec = importlib.util.spec_from_file_location(
    "lb317", HERE / "2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-"
                    "unconditional-parents_B.py")
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)

STAMP = ("2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-own-"
         "unconditional-parents_B_addendum")
RISK_ON = ("EWall", "TOP20", "TOP10", "MA-DG", "LOWVOL20")
_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); _LOG.append(s)


def main():
    t0 = time.time()
    P("=" * 108)
    P("IDEA 317R ADDENDUM — is the cloud run's low leg-pass rate the CASH PARENT?   (lane B, 2026-09-09)")
    P("  same panels/states/q/pins as the lane B census; risk-off parent replaced by CASH (gross 0)")
    P("  matched gross is UNDEFINED against a gross-0 parent; cash is left at 0.  Stated, not hidden.")
    P("=" * 108)

    pxU = load_universe(); pxB = load_universe(broad=True)
    pxS_all = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    scols = [c for c in pxS_all.columns if c != "SPY" and c not in bad]
    pxS = pxS_all[scols + ["SPY"]].dropna(how="all").ffill()
    panels = [("U56", pxU, np.ones(len(pxU.columns), bool)),
              ("B136", pxB, np.ones(len(pxB.columns), bool)),
              ("SMALL439", pxS, np.array([c != "SPY" for c in pxS.columns]))]

    rows = []
    for pname, px, tr in panels:
        books, elig, ma, vol20 = L.build_books(px, tr)
        start = px.index[max(260, L.MA_WIN + 20)]
        CASH = pd.DataFrame(0.0, index=px.index, columns=px.columns)
        for an in RISK_ON:
            WA = books[an]
            gA = L.mean_gross(WA, px.index)
            rA_un = L.fast_bt(px, WA)[0]
            states = L.build_states(px, elig, ma, vol20, rA_un)
            for st in L.STATES:
                for q in L.QS:
                    off = L.risk_off_mask(states[st], q)
                    WC = L.build_C(WA, CASH, off)
                    gC = L.mean_gross(WC, px.index)
                    kA = gC / gA if gA else 0.0
                    rC = L.fast_bt(px, WC)[0].loc[start:]
                    rA = L.fast_bt(px, WA * kA)[0].loc[start:]
                    rB = pd.Series(0.0, index=rC.index)          # cash: 0 return, 0 drawdown
                    mC, mA = metrics(rC), metrics(rA)
                    h1C, h2C = L.halves(rC); h1A, h2A = L.halves(rA)
                    rows.append(dict(
                        panel=pname, riskon=an, state=st, q=q,
                        off_rate=float(off.loc[start:].mean()), gA=gA, gC=gC, kA=kA,
                        C_CAGR=mC["CAGR"], C_Sharpe=mC["Sharpe"], C_MaxDD=mC["MaxDD"],
                        A_CAGR=mA["CAGR"], A_Sharpe=mA["Sharpe"], A_MaxDD=mA["MaxDD"],
                        B_CAGR=0.0, B_Sharpe=0.0, B_MaxDD=0.0,
                        C_H1=h1C, C_H2=h2C, A_H1=h1A, A_H2=h2A,
                        C_oSharpe=metrics(rC.loc[L.OOS_START:])["Sharpe"],
                        A_oSharpe=metrics(rA.loc[L.OOS_START:])["Sharpe"]))
        P(f"  {pname}: {len(RISK_ON) * len(L.STATES) * len(L.QS)} CASH-parent cells done "
          f"({time.time() - t0:.0f}s)")

    d = pd.DataFrame(rows)
    d["pt_cagr"] = (d.C_CAGR > d.A_CAGR) & (d.C_CAGR > d.B_CAGR)
    d["pt_sharpe"] = (d.C_Sharpe > d.A_Sharpe) & (d.C_Sharpe > d.B_Sharpe)
    d["pt_dd"] = (d.C_MaxDD > d.A_MaxDD) & (d.C_MaxDD > d.B_MaxDD)
    d["pt_all3"] = d.pt_cagr & d.pt_sharpe & d.pt_dd
    d.to_csv(HERE / f"{STAMP}.cash.csv", index=False)

    cells = pd.read_csv(HERE / "2026-09-09_do-the-record-s-CONDITIONAL-clauses-ever-beat-their-"
                               "own-unconditional-parents_B.cells.csv")
    degen = cells.groupby("family").apply(
        lambda s: (s.A_Sharpe - s.B_Sharpe).abs().max() < 1e-9, include_groups=False)
    nd = cells[~cells.family.map(degen)]
    nd_all3 = nd.pt_cagr & nd.pt_sharpe & nd.pt_dd

    P("\n" + "=" * 108)
    P("THE RECONCILIATION — single-leg and joint pass rates, same machinery, one corpus change")
    P("=" * 108)
    P(f"  {'corpus':44s} {'cells':>6s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'ALL3':>8s}")
    P(f"  {'lane B, NAMED clause families (no CASH parent)':44s} {len(nd):6d} "
      f"{nd.pt_cagr.mean():7.1%} {nd.pt_sharpe.mean():7.1%} {nd.pt_dd.mean():7.1%} {nd_all3.mean():7.1%}")
    P(f"  {'lane B corpus, risk-off parent -> CASH':44s} {len(d):6d} "
      f"{d.pt_cagr.mean():7.1%} {d.pt_sharpe.mean():7.1%} {d.pt_dd.mean():7.1%} {d.pt_all3.mean():7.1%}")
    P(f"  {'cloud run, 6-book menu INCLUDING cash':44s} {720:6d} "
      f"{0.042:7.1%} {0.062:7.1%} {0.082:7.1%} {2/720:7.1%}   (quoted from its LEADERBOARD rows)")

    P("\n  WHY the CASH column is what it is — these are identities, not measurements:")
    P(f"    MaxDD leg: C must beat CASH's 0.00% drawdown.  Observed {d.pt_dd.sum()}/{len(d)}; "
      f"max C_MaxDD over all {len(d)} cells = {d.C_MaxDD.max():.2%}.")
    P(f"    Sharpe leg: the CASH half is free (Sharpe 0, so any positive-mean book clears it), so "
      f"the leg reduces to C vs the risk-on parent ALONE.  Observed {d.pt_sharpe.sum()}/{len(d)} "
      f"({d.pt_sharpe.mean():.1%}) — a ONE-parent test, not a two-parent one.")
    P(f"    CAGR leg:   same reduction, {d.pt_cagr.sum()}/{len(d)} ({d.pt_cagr.mean():.1%}).")
    P(f"    ALL3 therefore = the MaxDD leg = {d.pt_all3.sum()}/{len(d)} by construction.")
    P("\n  Cash-parent pairs are 10 of the cloud run's 30 ordered pairs (33% of its 720 cells).")
    P("  Every one of those cells contributes a GUARANTEED MaxDD-leg failure, so the cloud run's")
    P("  ALL3 rate of 0.3% is computed over a corpus a third of which CANNOT pass ALL3 at all.")
    P("  HOW MUCH THIS EXPLAINS, stated precisely rather than generously:")
    P("    - the MaxDD leg and ALL3: fully.  Both are 0 by construction on cash pairs, and the")
    P("      cloud's 8.2% MaxDD leg is about what 2/3 of a corpus passing at lane B's 12-42%")
    P("      would give.")
    P(f"    - the Sharpe leg: NOT explained by cash.  Cash pairs pass it here at {d.pt_sharpe.mean():.1%}, which is")
    P("      HIGHER than the cloud run's 6.2%, so its low Sharpe leg comes from the rest of its")
    P("      corpus — 30 ORDERED pairs over an arbitrary 6-book menu (both orderings of each pair,")
    P("      many of which are not clauses the record ever ran) crossed with 8 states, against")
    P("      lane B's 6 NAMED clause families.  Which corpus answers the queued question is a")
    P("      judgement call, and the two runs made it differently; neither is an error.")

    P("\n  Lane B's own reading, unchanged by this: on the 240 cells where the parents test is")
    P("  WELL-POSED (both parents hold risk, gross matched to < 1e-12), the legs pass at")
    P(f"  {nd.pt_cagr.mean():.1%} / {nd.pt_sharpe.mean():.1%} / {nd.pt_dd.mean():.1%} and ALL3 at "
      f"{nd_all3.mean():.1%} — and lane B's placebo (the same masks shifted +504d/+1260d) clears the")
    P("  Sharpe leg 18.1% of the time, so the leg does not separate real conditioning from noise.")
    P("\n  WHERE THE TWO RUNS AGREE (both should be believed):")
    P("    - idea 48's '0/16 on drawdown' does NOT generalise; both runs contradict it.")
    P("    - no conditional book on any panel clears 4a.")
    P("    - conditional clauses beat both parents rarely, and rarely twice.")
    P("  WHERE THEY DISAGREE, and why lane B does not recommend the gate:")
    P("    - a bar that 99.7% of books fail is not evidence the books are bad if a third of the")
    P("      corpus cannot pass it by construction and a misaligned placebo clears its legs at")
    P("      near the real rate.  Recommend the matched-gross parents REPORTING line, not 4c.")
    P("    - the two runs' recommendations should go to the Sunday review TOGETHER.")

    P(f"\nelapsed {time.time() - t0:.1f}s")
    (HERE / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
