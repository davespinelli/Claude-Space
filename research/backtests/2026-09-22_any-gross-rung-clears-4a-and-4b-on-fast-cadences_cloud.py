#!/usr/bin/env python3
"""Idea 988 (lane cloud, 2026-09-22): does ANY GROSS RUNG clear 4a AND 4b AT ONCE on the
FAST CADENCES?

Idea 984's four OOS 4b passes are all D/W and all the SAME book -- U56 / `BAND03` at gross
1.00 -- refused on 4a for the fourth time because gross 1.00 buys about a third more return
for about a third more drawdown than the live book's -12.05%.  That refusal is a statement
about ONE rung.  This run walks the WHOLE gross ladder at every fast cadence on all three
panels and asks the queue's question directly: is there ANY rung where both KEEP paths
close at once, and if not, WHICH LEG refuses, at every rung?

CONSTRUCTION
  BOOK = `BAND03`, the live RULES v2 shape: hold every name inside the 200d +/-3% band at
  gross/N of NAV, N = instruments priced that day; gated-out weight goes to CASH, never
  re-spread.  No ranking, no vol filter.  This is `baseline.rules_v2_weights(px, band=0.03,
  gross=g)` -- the band constant 0.03 is the LIVE value and is NOT tuned here.
  TUNED PARAMETERS: exactly two, as the queue line specifies -- (gross ladder, cadence).
    gross g = 0.25 .. 1.50 in 0.05 steps (26 rungs).  g > 1.00 is LEVERAGE, declared by the
      queue line itself; PROTOCOL rule 2's default is no leverage, so every levered rung is
      flagged in the output and excluded from any recommendation.
    cadence = D and W (the fast cadences the question is about) plus M, published as a
      control so the answer cannot be a fast-cadence artefact.
  3 panels x 3 cadences x 26 rungs = 234 published books.  Costs 10 bps, next-day execution.

  COMPARANDS at every cell: the LIVE RULES v2 book (4a's yardstick), RULES v1, and SPY
  (4b's yardstick), all on the same panel and sample.
  BINDING-LEG CENSUS: every failing rung reports WHICH of 4a's three legs and 4b's five legs
  refused it, so "no rung clears both" comes with a mechanism instead of a tally.
  RULE 8: (g, cadence) chosen on 2009-2016 ONLY by three published IS-only rulers --
  IS Sharpe, IS Calmar, and a DD-BUDGET ruler (the largest g whose IS MaxDD stays inside the
  live book's own IS MaxDD, the one dial idea 2266 found the budget does not break on) --
  and 2017-2026 is read ONCE.

Outputs (beside this file):
  *.grid.csv     every published book with both KEEP verdicts and its binding legs
  *.legs.csv     the binding-leg census
  *.walkforward.csv  rule-8 choosers
  *.gates.csv    every asserted gate with its realised value
  *.out.txt      stdout

Run: python3 research/backtests/2026-09-22_any-gross-rung-clears-4a-and-4b-on-fast-cadences_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights                # noqa
from engine import backtest                                                           # noqa

OUT       = Path(__file__).with_suffix("")
BAND      = 0.03          # the LIVE band constant, not tuned here
LIVE_G    = 0.75          # the LIVE gross, for reference
COST_BPS  = 10            # PROTOCOL rule 2
WARMUP    = 260
OOS_START = pd.Timestamp("2017-01-01")
IS_END    = pd.Timestamp("2016-12-31")
GROSS     = np.round(np.arange(0.25, 1.5001, 0.05), 4)     # tuned param 1 (26 rungs)
CADENCES  = ("D", "W", "M")                                # tuned param 2 (D/W = the question)

def sharpe(r):  return r.mean() * 252 / (r.std() * np.sqrt(252)) if r.std() > 0 else np.nan
def maxdd(r):   e = (1 + r).cumprod(); return float((e / e.cummax() - 1).min())
def cagr(r):    e = (1 + r).cumprod(); return float(e.iloc[-1] ** (252 / len(r)) - 1)

def full_metrics(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                IS_MaxDD=maxdd(r.loc[:IS_END]),
                OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                OOS_MaxDD=maxdd(r.loc[OOS_START:]))

def legs(m, v2, spy):
    """Every leg of both KEEP paths as a named boolean, so a FAIL names its own binder."""
    L = {
        "4a_H1_gt_v2":    m["H1"] > v2["H1"],
        "4a_H2_gt_v2":    m["H2"] > v2["H2"],
        "4a_DD_no_worse": m["MaxDD"] >= v2["MaxDD"],
        "4b_H1_gt_SPY":   m["H1"] > spy["H1"],
        "4b_H2_gt_SPY":   m["H2"] > spy["H2"],
        "4b_OOS_gt_SPY":  m["OOS_Sharpe"] > spy["OOS_Sharpe"],
        "4b_DD_cap":      m["MaxDD"] >= 0.60 * spy["MaxDD"],
        "4b_CAGR_floor":  m["CAGR"] >= 0.70 * spy["CAGR"],
    }
    L["keep4a"] = all(L[k] for k in ("4a_H1_gt_v2", "4a_H2_gt_v2", "4a_DD_no_worse"))
    L["keep4b"] = all(L[k] for k in ("4b_H1_gt_SPY", "4b_H2_gt_SPY", "4b_OOS_gt_SPY",
                                     "4b_DD_cap", "4b_CAGR_floor"))
    L["keep4b_oos"] = (m["OOS_Sharpe"] > spy["OOS_Sharpe"]) \
        and (m["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]) \
        and (m["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])
    L["keep_BOTH"] = L["keep4a"] and L["keep4b"]
    return L

def main():
    t0 = time.time(); log = []
    def say(s):
        print(s, flush=True); log.append(str(s))

    say("IDEA 988 -- does ANY gross rung clear 4a AND 4b at once on the fast cadences?")
    say(f"BAND03 book (live RULES v2 shape, band={BAND}), gross {GROSS[0]}..{GROSS[-1]} step 0.05 "
        f"({len(GROSS)} rungs) x cadence {CADENCES} x 3 panels, cost {COST_BPS} bps, t+1.")
    say("LEVERAGE NOTE: rungs above g = 1.00 are levered; the queue line asks for them, "
        "PROTOCOL rule 2's default forbids them, so they are flagged and never recommended.")

    grid, gates, wf = [], [], []
    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        if lbl == "SMALL":
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad  = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
            keep = [c for c in px.columns if c == "SPY" or c not in bad]
            gates.append(dict(panel=lbl, gate="G0_small_blowups_dropped",
                              value=px.shape[1] - len(keep), expect="54", ok=px.shape[1] - len(keep) == 54))
            px = px[keep]
        start = px.index[WARMUP]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r  = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        v1_r  = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        spy_m, v2_m, v1_m = full_metrics(spy_r), full_metrics(v2_r), full_metrics(v1_r)
        say(f"\n[{lbl}] {px.shape[1]} cols  {start.date()}..{px.index[-1].date()}  ({time.time()-t0:.0f}s)")
        say(f"  SPY      CAGR {spy_m['CAGR']:.2%}  Sharpe {spy_m['Sharpe']:.4f}  MaxDD {spy_m['MaxDD']:.2%}"
            f"   -> 4b cap {0.60*spy_m['MaxDD']:.2%}, 4b floor {0.70*spy_m['CAGR']:.2%}")
        say(f"  RULESv2  CAGR {v2_m['CAGR']:.2%}  Sharpe {v2_m['Sharpe']:.4f}  MaxDD {v2_m['MaxDD']:.2%}"
            f"   halves {v2_m['H1']:.4f} / {v2_m['H2']:.4f}  (4a's yardstick)")
        for nm, m in (("SPY", spy_m), ("RULESv2_live", v2_m), ("RULESv1", v1_m)):
            grid.append(dict(panel=lbl, cadence="-", gross=np.nan, levered=False, family="REF",
                             rung=nm, turnover=np.nan, **m, **legs(m, v2_m, spy_m)))

        for cad in CADENCES:
            for g in GROSS:
                res = backtest(px, rules_v2_weights(px, band=BAND, gross=float(g)),
                               cost_bps=COST_BPS, freq=cad)
                r  = res["returns"].loc[start:]
                m  = full_metrics(r)
                tn = float(res["turnover"].loc[start:].sum() / (len(r) / 252))
                grid.append(dict(panel=lbl, cadence=cad, gross=float(g), levered=bool(g > 1.0),
                                 family="BAND03", rung=f"g={g:.2f}", turnover=tn,
                                 realised_gross=float(res["weights"].sum(axis=1).loc[start:].mean()),
                                 **m, **legs(m, v2_m, spy_m)))
            say(f"  cadence {cad} done ({time.time()-t0:.0f}s)")

        # ---- gates on this panel's ladder -------------------------------------
        P = pd.DataFrame([r for r in grid if r["panel"] == lbl and r["family"] == "BAND03"])
        for cad in CADENCES:
            C = P[P.cadence == cad].sort_values("gross")
            gates.append(dict(panel=lbl, gate=f"G1_{cad}_MaxDD_monotone_deeper_in_gross",
                              value=float(np.diff(C.MaxDD.values).max()), expect="<=0",
                              ok=bool(np.diff(C.MaxDD.values).max() <= 1e-9)))
            gates.append(dict(panel=lbl, gate=f"G2_{cad}_Sharpe_range_over_the_whole_ladder",
                              value=float(C.Sharpe.max() - C.Sharpe.min()), expect="report", ok=True))
        W75 = P[(P.cadence == "W") & (np.isclose(P.gross, LIVE_G))]
        if len(W75):
            d = float(abs(W75.iloc[0]["Sharpe"] - v2_m["Sharpe"]))
            gates.append(dict(panel=lbl, gate="G3_W_g0.75_reproduces_live_RULESv2",
                              value=d, expect="~0", ok=bool(d < 1e-9)))

        # ---- rule 8: choose on 2009-2016, read 2017-2026 ONCE ------------------
        for pool_name, Q in (("FAST_DW", P[P.cadence.isin(["D", "W"])]),
                             ("ALL_DWM", P),
                             ("UNLEVERED_DW", P[P.cadence.isin(["D", "W"]) & (~P.levered)])):
            for ruler in ("IS_Sharpe", "IS_Calmar", "IS_DDBUDGET"):
                if ruler == "IS_Sharpe":   pick = Q.loc[Q.IS_Sharpe.idxmax()]
                elif ruler == "IS_Calmar": pick = Q.loc[(Q.IS_CAGR / Q.IS_MaxDD.abs()).idxmax()]
                else:                                            # largest g inside the live IS DD
                    ok = Q[Q.IS_MaxDD >= v2_m["IS_MaxDD"]]
                    if not len(ok): continue
                    pick = ok.loc[ok.gross.idxmax()]
                wf.append(dict(panel=lbl, pool=pool_name, ruler=ruler,
                               pick=f"{pick.cadence} g={pick.gross:.2f}", levered=pick.levered,
                               IS_Sharpe=pick.IS_Sharpe, IS_MaxDD=pick.IS_MaxDD,
                               OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                               OOS_MaxDD=pick.OOS_MaxDD, keep4a=pick.keep4a, keep4b=pick.keep4b,
                               keep4b_oos=pick.keep4b_oos, keep_BOTH=pick.keep_BOTH))
        for nm, m in (("SPY", spy_m), ("RULESv2_live", v2_m)):
            l = legs(m, v2_m, spy_m)
            wf.append(dict(panel=lbl, pool="CONTROL", ruler="none", pick=nm, levered=False,
                           IS_Sharpe=m["IS_Sharpe"], IS_MaxDD=m["IS_MaxDD"],
                           OOS_CAGR=m["OOS_CAGR"], OOS_Sharpe=m["OOS_Sharpe"],
                           OOS_MaxDD=m["OOS_MaxDD"], keep4a=l["keep4a"], keep4b=l["keep4b"],
                           keep4b_oos=l["keep4b_oos"], keep_BOTH=l["keep_BOTH"]))

    GD = pd.DataFrame(grid); GA = pd.DataFrame(gates); WF = pd.DataFrame(wf)
    GD.to_csv(f"{OUT}.grid.csv", index=False)
    GA.to_csv(f"{OUT}.gates.csv", index=False)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    B = GD[GD.family == "BAND03"]

    say("\n================ GATES ================")
    say(GA.to_string(index=False, float_format=lambda x: f"{x:.6f}"))

    say("\n================ THE QUEUE'S QUESTION ================")
    say(f"books published: {len(B)}  (3 panels x {len(CADENCES)} cadences x {len(GROSS)} rungs)")
    say(f"clear 4a:            {int(B.keep4a.sum())} of {len(B)}")
    say(f"clear 4b:            {int(B.keep4b.sum())} of {len(B)}")
    say(f"clear 4b FULL+OOS:   {int((B.keep4b & B.keep4b_oos).sum())} of {len(B)}")
    say(f"clear BOTH AT ONCE:  {int(B.keep_BOTH.sum())} of {len(B)}   <-- the answer")
    say("\nby panel x cadence (4a / 4b / BOTH):")
    t = B.groupby(["panel", "cadence"])[["keep4a", "keep4b", "keep_BOTH"]].sum()
    t["n"] = B.groupby(["panel", "cadence"]).size()
    say(t.to_string())
    say("\nunlevered subset (g <= 1.00), which is all PROTOCOL rule 2 permits:")
    U = B[~B.levered]
    say(f"  4a {int(U.keep4a.sum())} / 4b {int(U.keep4b.sum())} / BOTH {int(U.keep_BOTH.sum())} of {len(U)}")

    say("\n================ WHICH LEG REFUSES, AT EVERY RUNG ================")
    legnames = ["4a_H1_gt_v2", "4a_H2_gt_v2", "4a_DD_no_worse",
                "4b_H1_gt_SPY", "4b_H2_gt_SPY", "4b_OOS_gt_SPY", "4b_DD_cap", "4b_CAGR_floor"]
    fail = pd.DataFrame({k: (~B[k]).astype(int) for k in legnames})
    fail["panel"] = B.panel.values; fail["cadence"] = B.cadence.values
    say("FAIL rate per leg over all 234 books:")
    say((fail[legnames].mean()).to_string(float_format=lambda x: f"{x:.4f}"))
    say("\nSOLE binder (the only leg of its own path that refused):")
    sole4a, sole4b = {}, {}
    for _, r in B.iterrows():
        f4a = [k for k in legnames[:3] if not r[k]]
        f4b = [k for k in legnames[3:] if not r[k]]
        if len(f4a) == 1: sole4a[f4a[0]] = sole4a.get(f4a[0], 0) + 1
        if len(f4b) == 1: sole4b[f4b[0]] = sole4b.get(f4b[0], 0) + 1
    say(f"  4a: {sole4a}")
    say(f"  4b: {sole4b}")
    fail.to_csv(f"{OUT}.legs.csv", index=False)

    say("\n================ IS GROSS A SHARPE DIAL? (the mechanism) ================")
    say("4a's two Sharpe legs are the ones gross cannot buy.  Sharpe range over the WHOLE "
        f"{GROSS[0]}..{GROSS[-1]} ladder, against the gap each cell must close:")
    rows = []
    for (p, c), C in B.groupby(["panel", "cadence"]):
        v2 = GD[(GD.panel == p) & (GD.rung == "RULESv2_live")].iloc[0]
        rows.append(dict(panel=p, cadence=c,
                         Sharpe_range=C.Sharpe.max() - C.Sharpe.min(),
                         H1_range=C.H1.max() - C.H1.min(), H2_range=C.H2.max() - C.H2.min(),
                         H1_gap_to_v2=C.H1.max() - v2.H1, H2_gap_to_v2=C.H2.max() - v2.H2,
                         MaxDD_range=C.MaxDD.max() - C.MaxDD.min(),
                         CAGR_range=C.CAGR.max() - C.CAGR.min()))
    S = pd.DataFrame(rows)
    say(S.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    say(f"\nMaxDD moves {S.MaxDD_range.mean()/max(S.H1_range.mean(),1e-9):.0f}x as far as H1 "
        f"does over the same ladder (mean range {S.MaxDD_range.mean():.4f} vs {S.H1_range.mean():.4f}): "
        "gross is a DRAWDOWN dial, not a SHARPE dial, and 4a needs Sharpe.")

    say("\n================ THE 984 RUNG, RE-PRICED ================")
    x = B[(B.panel == "U56") & (B.cadence.isin(["D", "W"])) & (np.isclose(B.gross, 1.00))]
    say(x[["panel", "cadence", "gross", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
           "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "turnover", "keep4a", "keep4b", "keep_BOTH"]]
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("\nthe SHALLOWEST rung that still clears 4b, per panel x cadence "
        "(the closest any rung gets to 4a's drawdown leg while keeping 4b):")
    best = []
    for (p, c), C in B[B.keep4b].groupby(["panel", "cadence"]):
        r = C.loc[C.gross.idxmin()]
        v2 = GD[(GD.panel == p) & (GD.rung == "RULESv2_live")].iloc[0]
        best.append(dict(panel=p, cadence=c, gross=r.gross, MaxDD=r.MaxDD, v2_MaxDD=v2.MaxDD,
                         DD_shortfall_pp=(r.MaxDD - v2.MaxDD) * 100,
                         H1=r.H1, v2_H1=v2.H1, H2=r.H2, v2_H2=v2.H2, levered=r.levered))
    say(pd.DataFrame(best).to_string(index=False, float_format=lambda x: f"{x:.4f}")
        if best else "  none")

    say("\n================ RULE 8 (chosen on 2009-2016, 2017-2026 read ONCE) ================")
    say(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nrule-8 picks clearing BOTH paths: {int(WF.keep_BOTH.sum())} of {len(WF)}")

    say(f"\ndone in {time.time()-t0:.0f}s")
    Path(f"{OUT}.out.txt").write_text("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
