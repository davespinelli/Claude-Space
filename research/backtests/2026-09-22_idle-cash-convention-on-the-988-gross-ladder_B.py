#!/usr/bin/env python3
"""Idea 2286 (lane B, 2026-09-22) -- does the IDLE-CASH CONVENTION change any committed
GROSS-LADDER verdict?

THE QUESTION, from the queue line.  Idea 988 walked the live `BAND03` shape over gross
0.25..1.50 x cadence {D,W,M} x 3 panels (234 books) and found BOTH KEEP paths clear at
0 of 234, with a measured mechanism: the two KEEP windows on the gross dial are DISJOINT on
9 of 9 cells -- 4a's drawdown leg CAPS gross (g <= 0.55-0.80) while 4b's CAGR floor FLOORS it
(g >= 0.90-1.05).  Every one of those 234 books pays EXACTLY 0% on its uninvested residual,
because `engine.backtest` drifts `1 - sum(w)` with no return attached.  A carry sleeve on
idle cash raises CAGR at every rung BELOW g = 1.00 while leaving the drawdown leg almost
untouched, so it is the one device that could close that gap FROM THE LOW SIDE.  Re-run 988's
ladder with idle cash carried and report whether any cell clears BOTH paths.

WHAT IS NEW HERE AND WHAT IS NOT.  Idea 2213 (cloud) swept idle NAV into SHY on a
band x gross ladder capped at g = 1.00, weekly only, and found the credit runs +0.014-0.018 pp
of CAGR per idle pp against a shortfall rising +0.15-0.18 pp per idle pp.  This run is 988's
ladder, not 2119's: it carries the FAST CADENCES (D and M as well as W) and it goes ABOVE
g = 1.00, where the residual is NEGATIVE and the same convention becomes a FINANCING CHARGE
rather than a credit.  That sign flip is the whole point.  The rungs that clear 4b's CAGR
floor are the levered ones; the rungs that clear 4a's DD leg are the de-grossed ones; a single
consistent cash convention must pay one and charge the other, and nothing in the record has
ever priced both ends of the same dial at once.

TUNED PARAMETERS: EXACTLY TWO, as the queue line specifies.
  (1) gross rung g = 0.25 .. 1.50 in 0.05 steps (26 rungs), 988's ladder verbatim.
  (2) carry on/off -- arm OFF is 988's committed convention (idle at 0%); arm ON credits and
      charges the residual at a T-bill proxy.
PUBLISHED, NOT TUNED (no selection is ever made over these): panel {U56, B136, SMALL} x
cadence {D, W, M} x window {FULL, H1, H2, IS, OOS}.  Band c = the LIVE 0.03.  Cost 10 bps,
t+1 execution (PROTOCOL rule 2).  ALL grid points are written to *.grid.csv.gz.

TWO CONTROL ARMS, published for reference and NEVER selected over:
  ON_SPREAD -- identical to ON except borrowing (g > 1.00) is charged at the proxy + 150 bps
      a year, which is nearer a real broker call rate.  ON is deliberately the arm most
      GENEROUS to leverage, so that a KILL under ON is not an artefact of my spread choice.
  FLAT2 -- a flat 2.0%/yr on both sides, i.e. the convention with the proxy's own path and
      duration removed, so that any verdict move can be attributed to the RATE or to SHY.

HONEST CONSTRUCTION NOTES, stated and not repaired.
 * The proxy is SHY (1-3y Treasuries) from the committed `data/prices_broad.csv`.  It is NOT
   a T-bill: it carries real duration risk and its realised path is regime-bound (2009-2021
   near-zero, 2022+ repricing).  It is used because it is the shortest instrument cached in
   this sandbox; no network is touched.
 * Carry is applied INSIDE the drift, not added to the return afterwards: the cash leg grows
   at (1 + c) and the book renormalises through the grown total, exactly as the engine does
   at c = 0.  Gate G1 asserts the local runner reproduces `engine.backtest` to machine
   precision when c = 0, so arm OFF is 988's numbers, not a re-derivation of them.
 * The sleeve is an ACCOUNTING credit: no sleeve trade is charged, and turnover is 988's
   turnover unchanged.  That is the most FAVOURABLE possible reading of the convention, and
   idea 2213 measured the traded version to cost 21-22% of the credit at 10 bps.
 * g > 1.00 is LEVERAGE.  PROTOCOL rule 2's default forbids it; the queue line's own ladder
   asks for it.  Every levered rung is flagged `levered=True` and is never recommended.
 * SURVIVORSHIP (rule 9): U56, B136 and SMALL are current-constituent lists, so every
   absolute level is optimistic.  The OFF-vs-ON contrast is within-tape and does not repair it.

Outputs beside this file:
  *.grid.csv.gz      every published book, both KEEP verdicts, every binding leg
  *.deltas.csv       the OFF -> ON verdict census, per cell
  *.walkforward.csv  rule-8 choosers (IS 2009-2016 only, OOS 2017-2026 read once)
  *.gates.csv        every asserted gate with its realised value
  *.console.txt      stdout

Run: python3 research/backtests/2026-09-22_idle-cash-convention-on-the-988-gross-ladder_B.py
"""
import sys, time, gzip
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights            # noqa
from engine import backtest, rebalance_mask                                       # noqa

OUT       = Path(__file__).with_suffix("")
BAND      = 0.03                                        # LIVE band constant, not tuned
LIVE_G    = 0.75                                        # LIVE gross, for reference
COST_BPS  = 10                                          # PROTOCOL rule 2
WARMUP    = 260
IS_END    = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")
GROSS     = np.round(np.arange(0.25, 1.5001, 0.05), 4)  # tuned param 1 (26 rungs) -- 988's ladder
CADENCES  = ("D", "W", "M")                             # published, not tuned
ARMS      = ("OFF", "ON", "ON_SPREAD", "FLAT2")         # tuned param 2 is OFF vs ON; last two are controls
SPREAD    = 0.0150                                      # borrow spread for the ON_SPREAD control, per yr
FLAT_RATE = 0.0200                                      # the FLAT2 control's rate, per yr

log_lines = []
def say(s=""):
    print(s, flush=True); log_lines.append(str(s))

# ---------------------------------------------------------------- metrics
def sharpe(r): return float(r.mean() * 252 / (r.std() * np.sqrt(252))) if r.std() > 0 else np.nan
def maxdd(r):  e = (1 + r).cumprod(); return float((e / e.cummax() - 1).min())
def cagr(r):   e = (1 + r).cumprod(); return float(e.iloc[-1] ** (252 / len(r)) - 1)

def full_metrics(r):
    h = len(r) // 2
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]),
                IS_CAGR=cagr(r.loc[:IS_END]), IS_Sharpe=sharpe(r.loc[:IS_END]),
                IS_MaxDD=maxdd(r.loc[:IS_END]),
                OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                OOS_MaxDD=maxdd(r.loc[OOS_START:]))

def legs(m, v2, spy, v2m=None):
    """988's leg definitions verbatim, so OFF is comparable to the committed ladder.

    v2m, when given, is the SAME baseline book run under the SAME cash convention as m.
    The `_matched` legs use it.  This matters: 4a's yardstick is RULES v2 at g = 0.75, which
    is a book with ~47% idle NAV of its own, so crediting the candidate while leaving the
    yardstick at 0% hands every candidate the same free +0.8 pp.  The unmatched legs are
    988's definitions and are reported for continuity; the matched legs are the honest ones.
    """
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
    if v2m is not None:
        L["4a_H1_gt_v2_matched"]    = m["H1"] > v2m["H1"]
        L["4a_H2_gt_v2_matched"]    = m["H2"] > v2m["H2"]
        L["4a_DD_no_worse_matched"] = m["MaxDD"] >= v2m["MaxDD"]
        L["keep4a_matched"] = all(L[k] for k in ("4a_H1_gt_v2_matched", "4a_H2_gt_v2_matched",
                                                 "4a_DD_no_worse_matched"))
        L["keep_BOTH_matched"] = L["keep4a_matched"] and L["keep4b"]
    return L

# ---------------------------------------------------------------- local runner (carry inside the drift)
def run(px, W, freq, credit, borrow, cost_bps=COST_BPS):
    """`engine.backtest` with the cash leg grown at (1 + c) instead of flat.

    credit/borrow are daily-return arrays aligned to px.index; credit applies when the
    residual 1 - sum(w) is POSITIVE (idle cash), borrow when it is NEGATIVE (leverage).
    At credit == borrow == 0 this is `engine.backtest` exactly -- asserted by gate G1.
    """
    idx  = px.index
    rets = px.pct_change().fillna(0.0).values
    wt   = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values
    n    = len(idx)
    cur  = np.zeros(px.shape[1])
    port = np.empty(n); turn = np.zeros(n); idle = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new.copy()
        s = cur.sum(); res = 1.0 - s
        idle[i] = res
        c = credit[i] if res >= 0 else borrow[i]
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + res * (1.0 + c)
        port[i] = tot - 1.0 - turn[i] * cost_bps / 1e4
        if tot > 0: cur = growth / tot
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx), pd.Series(idle, index=idx))

# ---------------------------------------------------------------- carry proxy
def carry_series(idx):
    """SHY daily total return from the committed broad cache, reindexed onto idx."""
    b = pd.read_csv(ROOT / "data" / "prices_broad.csv", index_col=0, parse_dates=True)["SHY"]
    return b.reindex(idx).ffill().bfill().pct_change().fillna(0.0)

def main():
    t0 = time.time()
    say("IDEA 2286 -- does the IDLE-CASH CONVENTION change any committed GROSS-LADDER verdict?")
    say(f"988's ladder verbatim: BAND03 (band={BAND}) x gross {GROSS[0]:.2f}..{GROSS[-1]:.2f} step 0.05 "
        f"({len(GROSS)} rungs) x cadence {CADENCES} x 3 panels, cost {COST_BPS} bps, t+1.")
    say(f"Arms {ARMS}: tuned dial is OFF vs ON; ON_SPREAD (borrow +{SPREAD:.2%}/yr) and "
        f"FLAT2 ({FLAT_RATE:.2%}/yr flat) are published controls, never selected over.")
    say("LEVERAGE: rungs above g = 1.00 are levered; flagged and never recommended.")
    say()

    grid, gates, wf = [], [], []

    for lbl, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        px = load_universe(**kw)
        if lbl == "SMALL":                                  # 988's G0, reproduced
            meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
            bad  = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
            keep = [c for c in px.columns if c == "SPY" or c not in bad]
            gates.append(dict(panel=lbl, gate="G0_small_blowups_dropped",
                              realised=px.shape[1] - len(keep), expect=54,
                              ok=bool(px.shape[1] - len(keep) == 54)))
            px = px[keep]
        start = px.index[WARMUP]
        idx   = px.index
        shy   = carry_series(idx)
        zero  = pd.Series(0.0, index=idx)
        flat  = pd.Series(FLAT_RATE / 252.0, index=idx)
        spr   = shy + SPREAD / 252.0
        ARM_RATES = {"OFF":       (zero.values, zero.values),
                     "ON":        (shy.values,  shy.values),
                     "ON_SPREAD": (shy.values,  spr.values),
                     "FLAT2":     (flat.values, flat.values)}

        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        v2_r  = backtest(px, rules_v2_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        v1_r  = backtest(px, rules_v1_weights(px), cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
        spy_m, v2_m, v1_m = full_metrics(spy_r), full_metrics(v2_r), full_metrics(v1_r)

        say(f"[{lbl}] {px.shape[1]} cols  {start.date()}..{idx[-1].date()}   ({time.time()-t0:.0f}s)")
        say(f"  SHY proxy: {(1+shy.loc[start:]).prod()**(252/len(shy.loc[start:]))-1:+.2%}/yr over the sample; "
            f"IS {(1+shy.loc[start:IS_END]).prod()**(252/len(shy.loc[start:IS_END]))-1:+.2%}, "
            f"OOS {(1+shy.loc[OOS_START:]).prod()**(252/len(shy.loc[OOS_START:]))-1:+.2%}")
        say(f"  SPY      CAGR {spy_m['CAGR']:.2%}  Sharpe {spy_m['Sharpe']:.4f}  MaxDD {spy_m['MaxDD']:.2%}"
            f"   -> 4b DD cap {0.60*spy_m['MaxDD']:.2%}, 4b CAGR floor {0.70*spy_m['CAGR']:.2%}")
        say(f"  RULESv2  CAGR {v2_m['CAGR']:.2%}  Sharpe {v2_m['Sharpe']:.4f}  MaxDD {v2_m['MaxDD']:.2%}"
            f"   halves {v2_m['H1']:.4f} / {v2_m['H2']:.4f}   (4a's yardstick)")

        for nm, m in (("SPY", spy_m), ("RULESv2_live", v2_m), ("RULESv1", v1_m)):
            grid.append(dict(panel=lbl, cadence="-", arm="-", gross=np.nan, levered=False,
                             family="REF", rung=nm, turnover=np.nan, idle_mean=np.nan,
                             **m, **legs(m, v2_m, spy_m, v2_m)))

        W1 = rules_v2_weights(px, band=BAND, gross=1.0)     # rules_v2_weights is LINEAR in gross

        # MATCHED YARDSTICK: the live RULES v2 book (g = 0.75, weekly) under EACH convention.
        W_live = rules_v2_weights(px, band=BAND, gross=LIVE_G)
        V2M = {}
        for arm in ARMS:
            cr, bo = ARM_RATES[arm]
            rr, _, _ = run(px, W_live, "W", cr, bo)
            V2M[arm] = full_metrics(rr.loc[start:])
            grid.append(dict(panel=lbl, cadence="W", arm=arm, gross=LIVE_G, levered=False,
                             family="REF_MATCHED_V2", rung=f"RULESv2_under_{arm}",
                             turnover=np.nan, idle_mean=np.nan,
                             **V2M[arm], **legs(V2M[arm], v2_m, spy_m, V2M[arm])))
        say("  matched yardstick (RULES v2 g=0.75 W under each convention): " +
            "  ".join(f"{a} {V2M[a]['CAGR']:.2%}/{V2M[a]['Sharpe']:.4f}/{V2M[a]['MaxDD']:.2%}" for a in ARMS))
        gates.append(dict(panel=lbl, gate="G2_gross_linearity",
                          realised=float((rules_v2_weights(px, band=BAND, gross=LIVE_G)
                                          - LIVE_G * W1).abs().max().max()),
                          expect=0.0, ok=None))

        for cad in CADENCES:
            for g in GROSS:
                Wg = LIVE_G * W1 * (g / LIVE_G)
                for arm in ARMS:
                    cr, bo = ARM_RATES[arm]
                    r_all, tn_all, idle_all = run(px, Wg, cad, cr, bo)
                    r = r_all.loc[start:]
                    m = full_metrics(r)
                    row = dict(panel=lbl, cadence=cad, arm=arm, gross=float(g),
                               levered=bool(g > 1.0), family="BAND03", rung=f"g={g:.2f}",
                               turnover=float(tn_all.loc[start:].sum() / (len(r) / 252)),
                               idle_mean=float(idle_all.loc[start:].mean()),
                               **m, **legs(m, v2_m, spy_m, V2M[arm]))
                    grid.append(row)

                    # ---- gates, checked on the live cell only (cheap, decisive)
                    if arm == "OFF" and cad == "W" and abs(g - LIVE_G) < 1e-9:
                        eng = backtest(px, Wg, cost_bps=COST_BPS, freq="W")["returns"].loc[start:]
                        gates.append(dict(panel=lbl, gate="G1_OFF_reproduces_engine",
                                          realised=float((r - eng).abs().max()), expect=0.0,
                                          ok=bool((r - eng).abs().max() < 1e-12)))
                        gates.append(dict(panel=lbl, gate="G1b_OFF_live_cell_is_baseline_v2",
                                          realised=float((r - v2_r).abs().max()), expect=0.0,
                                          ok=bool((r - v2_r).abs().max() < 1e-12)))
                    if arm == "OFF" and cad == "W" and abs(g - LIVE_G) < 1e-9:
                        off_live = r.copy()
                    if arm == "ON" and cad == "W" and abs(g - LIVE_G) < 1e-9:
                        rz, _, _ = run(px, Wg, cad, zero.values, zero.values)
                        gates.append(dict(panel=lbl, gate="G3_ON_at_zero_rate_collapses_to_OFF",
                                          realised=float((rz.loc[start:] - off_live).abs().max()),
                                          expect=0.0,
                                          ok=bool((rz.loc[start:] - off_live).abs().max() < 1e-15)))
                        gates.append(dict(panel=lbl, gate="G4_ON_credit_positive_at_live_cell",
                                          realised=float((r - off_live).mean() * 252 * 100),
                                          expect=">0 pp/yr", ok=bool((r - off_live).mean() > 0)))
            say(f"   {cad}: {len(GROSS)*len(ARMS)} books done  ({time.time()-t0:.0f}s)")

    G = pd.DataFrame(grid)
    G.to_csv(OUT.with_suffix(".grid.csv.gz"), index=False, compression="gzip")

    # ---------------------------------------------------------------- G5: sign of the residual
    band = G[G.family == "BAND03"]
    # G5: no UNLEVERED rung can ever run a negative residual (the band only de-grosses).
    gates.append(dict(panel="ALL", gate="G5_no_negative_residual_below_g1",
                      realised=float(band.loc[~band.levered, "idle_mean"].min()),
                      expect=">0", ok=bool((band.loc[~band.levered, "idle_mean"] > 0).all())))
    # G5b: mean residual is NOT negative on most levered rungs either -- the band gates names
    # out, so realised gross sits well below the target g.  Stated, not repaired: above g=1.00
    # the convention is a MIXTURE of credit and charge, not a pure financing cost.
    gates.append(dict(panel="ALL", gate="G5b_share_of_levered_rungs_with_idle_mean_lt_0",
                      realised=float((band.loc[band.levered, "idle_mean"] < 0).mean()),
                      expect="measured, not asserted", ok=None))
    # G6: turnover is NOT identical across arms -- carry changes the drift, hence the drifted
    # weights at the next rebalance.  The size of that second-order effect is the gate.
    gates.append(dict(panel="ALL", gate="G6_max_turnover_spread_across_arms_x_per_yr",
                      realised=float(band.groupby(["panel", "cadence", "gross"])["turnover"]
                                     .apply(lambda s: s.max() - s.min()).max()),
                      expect="second-order, measured", ok=None))
    Gt = pd.DataFrame(gates); Gt.to_csv(OUT.with_suffix(".gates.csv"), index=False)
    say("\n=== GATES ===")
    say(Gt.to_string(index=False, max_colwidth=40))

    # ---------------------------------------------------------------- A. the headline census
    say("\n=== A. DOES ANY CELL CLEAR BOTH PATHS? (988's question, per arm) ===")
    COLS = ["keep4a", "keep4a_matched", "keep4b", "keep4b_oos", "keep_BOTH", "keep_BOTH_matched"]
    cen = (band.groupby("arm")[COLS].sum().astype(int).assign(n=band.groupby("arm").size()))
    say(cen.to_string())
    say("  keep4a  = 988's leg (candidate under its arm vs the yardstick under the OLD 0% convention)")
    say("  keep4a_matched = the SAME comparison with the yardstick under the SAME convention -- the honest one")
    unlev = band[~band.levered]
    say("\nunlevered subset only (g <= 1.00, the only rungs PROTOCOL rule 2 permits):")
    say((unlev.groupby("arm")[COLS].sum().astype(int).assign(n=unlev.groupby("arm").size())).to_string())

    # ---------------------------------------------------------------- B. verdict deltas OFF -> ON
    key = ["panel", "cadence", "gross"]
    piv = band.pivot_table(index=key, columns="arm",
                           values=["keep4a", "keep4a_matched", "keep4b", "keep4b_oos", "keep_BOTH",
                                   "keep_BOTH_matched", "CAGR", "Sharpe", "MaxDD",
                                   "OOS_CAGR", "idle_mean"], aggfunc="first")
    d = pd.DataFrame(index=piv.index)
    d["idle_mean"] = piv[("idle_mean", "OFF")]
    d["levered"]   = d.index.get_level_values("gross") > 1.0
    for v in ("keep4a", "keep4a_matched", "keep4b", "keep4b_oos", "keep_BOTH", "keep_BOTH_matched"):
        d[v + "_OFF"] = piv[(v, "OFF")].astype(bool)
        d[v + "_ON"]  = piv[(v, "ON")].astype(bool)
        d[v + "_flip"] = d[v + "_ON"].astype(int) - d[v + "_OFF"].astype(int)
    d["dCAGR_pp"]   = (piv[("CAGR", "ON")]     - piv[("CAGR", "OFF")]) * 100
    d["dOOSCAGR_pp"] = (piv[("OOS_CAGR", "ON")] - piv[("OOS_CAGR", "OFF")]) * 100
    d["dSharpe"]    = piv[("Sharpe", "ON")]    - piv[("Sharpe", "OFF")]
    d["dMaxDD_pp"]  = (piv[("MaxDD", "ON")]    - piv[("MaxDD", "OFF")]) * 100
    d.reset_index().to_csv(OUT.with_suffix(".deltas.csv"), index=False)

    say("\n=== B. HOW FAR THE CONVENTION MOVES EACH BOOK (OFF -> ON) ===")
    say(d.groupby("levered")[["dCAGR_pp", "dOOSCAGR_pp", "dSharpe", "dMaxDD_pp"]]
         .describe().loc[:, (slice(None), ["mean", "min", "max"])].to_string(float_format=lambda x: f"{x:+.4f}"))
    say("\nverdict flips (ON minus OFF, summed over all 234 cells):")
    say(d[[c for c in d.columns if c.endswith("_flip")]].sum().to_string())
    say("\nflips by cadence x panel (keep4a unmatched / keep4a MATCHED / keep4b / keep_BOTH matched):")
    say(d.reset_index().groupby(["panel", "cadence"])[["keep4a_flip", "keep4a_matched_flip",
                                                       "keep4b_flip", "keep_BOTH_matched_flip"]]
         .sum().to_string())

    # ---------------------------------------------------------------- C. the disjointness gap
    say("\n=== C. DOES THE CONVENTION CLOSE 988's DISJOINT KEEP WINDOWS? ===")
    say("per (panel, cadence, arm): max gross clearing 4a's DD leg vs min gross clearing 4b's CAGR floor")
    rows = []
    for (p, c, a), sub in band.groupby(["panel", "cadence", "arm"]):
        hi4a = sub.loc[sub["4a_DD_no_worse"], "gross"]
        lo4b = sub.loc[sub["4b_CAGR_floor"], "gross"]
        rows.append(dict(panel=p, cadence=c, arm=a,
                         g_max_4aDD=float(hi4a.max()) if len(hi4a) else np.nan,
                         g_min_4bCAGR=float(lo4b.min()) if len(lo4b) else np.nan))
    gap = pd.DataFrame(rows)
    gap["gap"] = gap.g_min_4bCAGR - gap.g_max_4aDD
    say(gap.pivot_table(index=["panel", "cadence"], columns="arm",
                        values=["g_max_4aDD", "g_min_4bCAGR", "gap"])
        .to_string(float_format=lambda x: f"{x:.2f}"))

    # ---------------------------------------------------------------- D. rule 8
    say("\n=== D. RULE 8 -- g chosen on 2009-2016 IS ONLY, per (panel, cadence, arm); OOS read ONCE ===")
    for (p, c, a), sub in band.groupby(["panel", "cadence", "arm"]):
        for ruler, pool in (("IS_SHARPE", sub), ("IS_SHARPE_UNLEV", sub[~sub.levered]),
                            ("IS_4b_LEGAL", sub[(~sub.levered) & (sub.IS_CAGR >= 0)])):
            if not len(pool): continue
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            wf.append(dict(panel=p, cadence=c, arm=a, ruler=ruler, pick_gross=pick.gross,
                           levered=bool(pick.levered),
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           keep4a=bool(pick.keep4a), keep4a_matched=bool(pick.keep4a_matched),
                           keep4b=bool(pick.keep4b), keep4b_oos=bool(pick.keep4b_oos),
                           keep_BOTH=bool(pick.keep_BOTH),
                           keep_BOTH_matched=bool(pick.keep_BOTH_matched)))
    WF = pd.DataFrame(wf); WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    main_wf = WF[WF.ruler == "IS_SHARPE_UNLEV"]
    say(main_wf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say(f"\nrule-8 picks clearing BOTH paths: {int(WF.keep_BOTH.sum())} of {len(WF)} "
        f"(unlevered ruler: {int(main_wf.keep_BOTH.sum())} of {len(main_wf)}); "
        f"BOTH under the MATCHED yardstick: {int(WF.keep_BOTH_matched.sum())} of {len(WF)}; "
        f"4b-OOS only: {int(WF.keep4b_oos.sum())} of {len(WF)}")

    # ---------------------------------------------------------------- E. OOS vs baseline and SPY
    say("\n=== E. OOS (2017-2026) AT THE LIVE CELL (g=0.75, W) AND AT EACH ARM's BEST UNLEVERED RUNG ===")
    for p in ("U56", "B136", "SMALL"):
        ref = G[(G.panel == p) & (G.family == "REF")].set_index("rung")
        say(f"[{p}] SPY OOS CAGR {ref.loc['SPY','OOS_CAGR']:.2%} Sharpe {ref.loc['SPY','OOS_Sharpe']:.4f} "
            f"MaxDD {ref.loc['SPY','OOS_MaxDD']:.2%} | RULESv2 OOS CAGR {ref.loc['RULESv2_live','OOS_CAGR']:.2%} "
            f"Sharpe {ref.loc['RULESv2_live','OOS_Sharpe']:.4f} MaxDD {ref.loc['RULESv2_live','OOS_MaxDD']:.2%}")
        live = band[(band.panel == p) & (band.cadence == "W") & (np.isclose(band.gross, LIVE_G))]
        for _, r in live.iterrows():
            say(f"   live cell arm {r.arm:10s} FULL {r.CAGR:6.2%}/{r.Sharpe:.4f}/{r.MaxDD:7.2%}  "
                f"OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}  "
                f"idle {r.idle_mean:5.2%}  4a={bool(r.keep4a)} 4a_matched={bool(r.keep4a_matched)} "
                f"4b={bool(r.keep4b)}")

    say(f"\nDONE in {time.time()-t0:.0f}s.  {len(G)} published rows -> {OUT.name}.grid.csv.gz")
    OUT.with_suffix(".console.txt").write_text("\n".join(log_lines) + "\n")

if __name__ == "__main__":
    main()
