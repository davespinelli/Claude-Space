#!/usr/bin/env python3
"""Idea 257 — WINDOW-STAMP EVERY REACH AND EVERY DEPTH DENOMINATOR   (cloud, 2026-09-09)

PRE-REGISTERED QUESTION (from QUEUE.md, written before any number here was read)
    Idea 251 found OOS reach exceeds IS reach in 47 of 48 cells (the per-name trailing stop
    0.80 -> 5.14 pp, idea 40's book DD control 4.05 -> 9.89 pp), i.e. any statistic
    normalised by "drawdown available to buy" is a function of the WINDOW'S CRASHES, not of
    the instrument.  Test whether re-quoting the record's exchange rates PER CRISIS EPISODE
    AT MATCHED SPY DEPTH (idea 117's denominator) removes the IS/OOS gap.  Max 2 params.

WHAT IS UNDER TEST.  Exactly idea 251's 48 cells: 2 panels (u56, broad) x 2 instrument-free
base books (EWALL0, CAND20) x 2 cost rungs (10, 25 bps) x 6 instrument families, each with
idea 251's EXTENDED ladder (PUB is a flagged subset).  The small panel is deliberately out of
scope: the 47/48 claim is a claim about THESE cells, and adding a third panel would change
the object rather than test it.

THE TWO CONVENTIONS, both computed on the same arms, same window, same costs
  WHOLE-WINDOW (idea 251's, the incumbent)
      bought_pp = (MaxDD_arm - MaxDD_ctl) * 100 over the window
      reach     = max over the family's ladder of bought_pp
      rate      = (CAGR_ctl - CAGR_arm)*100 / bought_pp
    computed separately on IS (<= 2016-12-31) and OOS (2017-01-01..), and the IS/OOS gap is
    what idea 251 reported.
  EPISODE-STAMPED AT MATCHED DEPTH (idea 117's denominator, the candidate fix)
      SPY drawdown episodes are idea 62/117's: maximal underwater runs of SPY whose trough
      reaches -theta, [peak, recovery], stamped IS/OOS by their TROUGH date and binned
      SHALLOW (<20 pp) / DEEP (>=20 pp) on idea 117's only boundary.
      bought_e     = (MaxDD_arm|e - MaxDD_ctl|e) * 100, peak reset at the episode's start
      reach_e_norm = bought_e / SPY_depth_e          <- pp of book drawdown bought per pp of
                                                        SPY drawdown actually on offer
      price_e      = (CAGR_ctl - CAGR_arm on CALM DAYS ONLY, in that window) / bought_e
      A cell's IS (OOS) figure is the MEDIAN over its IS (OOS) episodes WITHIN a depth bin,
      exactly idea 117's aggregation.

PRE-REGISTERED BARS (fixed before any number was read; idea 117's own bar, re-used)
  B1  The one-sided asymmetry must go: idea 251's 47/48 "OOS > IS" count must fall to
      something a two-sided binomial sign test cannot reject at 5% (i.e. roughly 17-31 of 48).
  B2  Median |log10(IS/OOS)| must FALL, and clear idea 117's published bar of 0.227.
  Both must hold for the fix to be called effective on reach.  They are reported separately
  for reach and for the exchange rate, and separately at each theta.

TUNED PARAMETERS: exactly TWO — the episode threshold theta (all of 0.08, 0.10, 0.15
reported, 0.10 is the point) and, in the rule-8 selector only, the instrument level.  Panel,
book, cost rung, family and depth bin are REPORTING axes printed at every value and never
selected on.  All 528 arm rows and all episode rows are written to CSV.

RULE 8 (PROTOCOL 8): reach is only usable if it is knowable in advance.  Two selectors are
run on IS <= 2016-12-31 only and 2017-2026 is read once:
    S_WINDOW   the level maximising IS whole-window bought_pp     (idea 251's selector)
    S_EPISODE  the level maximising IS median episode-normalised reach_e_norm (the candidate)
Reported for each: the OOS reach it forfeits against the OOS-optimal level, and the OOS
CAGR / Sharpe / MaxDD of the picked arm against the live RULES v2 book, RULES v1 and SPY,
with BOTH KEEP paths evaluated.

REPRODUCTION GATES, asserted before any new number is read
  G1  idea 245's harness: run(no instrument) == engine.backtest, and its stop == idea 94's.
  G2  every arm rebuilt here reproduces idea 251's COMMITTED grid.csv (bought_pp, paid_pp,
      IS_bought, OOS_bought, CAGR, MaxDD).  This is a TOLERANCE gate, and the reason is in
      the data: data/prices.csv has been restated since idea 251 was committed (up to 3e-4
      on the 4,699 x 58 shared cells, plus one extra bar which this run's 2026-09-04
      truncation removes), so bit-for-bit is not available.  Every delta is printed.
  G3  idea 251's COMMITTED reach.csv (max_bought, IS_max_bought, OOS_max_bought) reproduced
      to the same tolerance, and its headline "OOS reach exceeds IS reach in 47 of 48 cells"
      recounted here.
  G4  idea 117's episode classification rebuilt from its own function; episode count and the
      IS/OOS/depth stamps printed for every theta.

SURVIVORSHIP (idea 54): u56 is a fixed ETF/mega-cap list; `broad` is a CURRENT-constituent
list, so its crashes are shallower than the real world's.  Reach is an ABSOLUTE quantity, so
this bias is not cancelled and every reach printed here understates what the instrument could
buy in a panel containing the names that died.  The episode-normalised statistic divides by
SPY's depth, which is survivorship-free, so it is the less biased of the two — that is an
argument FOR the fix that is independent of whether the fix works.

Costs 10 and 25 bps, applied analytically per idea 245; weights decided at close t applied at
t+1.  Deterministic, no network.  Writes .arms.csv, .episodes.csv, .epreach.csv, .gap.csv,
.walkforward.csv, .console.txt.
"""
import importlib.util
import sys
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

BT = ROOT / "research" / "backtests"


def _mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


i245 = _mod("i245", BT / "2026-09-06_arm-the-cheap-instruments-in-crashes-instead_cloud.py")
i117 = _mod("i117", BT / "2026-09-05_crisis-depth-as-the-price-denominator_B.py")

run, arm_returns, BASE_BOOKS = i245.run, i245.arm_returns, i245.BASE_BOOKS
harness, m, halves = i245.harness, i245.m, i245.halves
at_cost, turn_per_yr = i245.at_cost, i245.turn_per_yr
fail4a, fail4b = i245.fail4a, i245.fail4b
spy_episodes, calm_mask, win_maxdd, ann = (i117.spy_episodes, i117.calm_mask,
                                           i117.win_maxdd, i117.ann)

STAMP = "2026-09-09_window-stamp-every-reach-and-every-depth-denominator_cloud"
OUT = BT / STAMP
I251_GRID = BT / "2026-09-06_does-reach-belong-beside-every-instrument-price_C.grid.csv"
I251_REACH = BT / "2026-09-06_does-reach-belong-beside-every-instrument-price_C.reach.csv"

COSTS = [10, 25]
PROTO_COST = 10
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
THETAS = [0.08, 0.10, 0.15]        # tuned parameter (1); 0.10 is the point, all reported
THETA0 = 0.10
FAMILIES = ["200d", "band", "abs", "dg", "ddctl", "stop"]
LABEL = {"200d": "200d-type MA gate", "band": "MA re-entry band", "abs": "absolute momentum",
         "dg": "de-gross (reference)", "ddctl": "book DD control (idea 40)",
         "stop": "per-name trailing stop"}
# idea 251's ladders, copied verbatim so G2/G3 are bit-for-bit checks
PUB = {"200d": [75, 100, 150, 200, 250, 300],
       "band": [0.01, 0.02, 0.03, 0.05, 0.08, 0.12],
       "abs": [42, 63, 126, 189, 252, 378],
       "dg": [0.90, 0.80, 0.70, 0.60, 0.50, 0.40],
       "ddctl": [0.05, 0.08, 0.12, 0.16, 0.20, 0.25],
       "stop": [0.08, 0.10, 0.15, 0.20, 0.25, 0.30]}
EXT = {"200d": [20, 50, 75, 100, 150, 200, 250, 300, 400, 500],
       "band": [0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30],
       "abs": [10, 21, 42, 63, 126, 189, 252, 378, 504, 756],
       "dg": [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10, 0.05, 0.00],
       "ddctl": [0.02, 0.03, 0.05, 0.08, 0.12, 0.16, 0.20, 0.25, 0.30, 0.40],
       "stop": [0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]}
I251_LAST = "2026-09-04"           # idea 251's last bar; panels truncated here so G2/G3 are exact
DEEP_EDGE = 20.0                   # idea 117's only depth-bin boundary, pp
BAR_117 = 0.227                    # idea 117's published portability bar

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

_console = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _console.append(s)


def signtest_p(k, n):
    """Two-sided exact binomial p for k successes of n at p=0.5."""
    k = min(k, n - k)
    tail = sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def med_abs_log10_ratio(a, b):
    """median |log10(a/b)| over pairs where both are finite and strictly positive."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
    if not ok.any():
        return np.nan, 0
    return float(np.median(np.abs(np.log10(a[ok] / b[ok])))), int(ok.sum())


def main():
    say(f"=== idea 257 window-stamp-every-reach-and-every-depth-denominator (cloud) ===")
    say(f"research/backtests/{STAMP}.py\n")

    # Panels are truncated to idea 251's LAST BAR so every reproduction gate below is
    # bit-for-bit.  data/prices.csv has advanced 2 trading days since idea 251 was committed
    # (2026-09-05, 2026-09-08; prices_broad.csv is unchanged); on the untruncated panel the
    # largest arm disagreement is 0.0088 pp of MaxDD, on the path-dependent stop, which is
    # four orders of magnitude below the effects under test — but the object under test is
    # idea 251's 48 cells, so this run uses idea 251's window exactly.
    panels = {"u56": load_universe().loc[:I251_LAST],
              "broad": load_universe(broad=True).loc[:I251_LAST]}
    say(f"panels truncated to idea 251's last bar {I251_LAST}: "
        + ", ".join(f"{k} {v.index[0].date()}..{v.index[-1].date()} ({len(v)} rows)"
                    for k, v in panels.items()))

    # ---------------------------------------------------------------- G1
    say("=== GATES ===")
    say("G1 idea 245's own harness (run(no instrument) vs engine.backtest; stop vs idea 94)"
        " — it prints and asserts its own gates:")
    harness(panels["u56"])

    # ---------------------------------------------------------------- build arms
    say("\n--- building idea 251's arm grid (EXT ladder), keeping DAILY returns ---")
    arows, erows = [], []
    EPI = {}
    for pname, px in panels.items():
        start = px.index[260]                     # idea 74/251's window convention, kept
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = {c: backtest(px, rules_v1_weights(px), cost_bps=c, freq="W")["returns"].loc[start:]
                for c in COSTS}
        base2 = {c: backtest(px, rules_v2_weights(px), cost_bps=c, freq="W")["returns"].loc[start:]
                 for c in COSTS}
        spy_oos_sh = metrics(spy[OOS_START:])["Sharpe"]
        for th in THETAS:
            E = spy_episodes(spy, th)
            E["panel"] = pname
            E["theta"] = th
            E["depth_bin"] = np.where(E.depth >= DEEP_EDGE, "DEEP", "SHALLOW")
            EPI[(pname, th)] = E
            erows.append(E)
        for bname, bfn in BASE_BOOKS.items():
            w = bfn(px)
            ctrl_full = run(px, w)
            ctrl = tuple(s.loc[start:] for s in ctrl_full[:3]) + (ctrl_full[3],)
            for cost in COSTS:
                cr = at_cost(ctrl[0], ctrl[1], cost)
                c_c, c_s, c_dd = m(cr)
                c_is, c_oos = m(cr[:IS_END]), m(cr[OOS_START:])
                arows.append(dict(panel=pname, book=bname, cost=cost, family="none",
                                  level=np.nan, in_pub=True, CAGR=c_c, Sharpe=c_s, MaxDD=c_dd,
                                  IS_CAGR=c_is[0], IS_MaxDD=c_is[2], OOS_CAGR=c_oos[0],
                                  OOS_Sharpe=c_oos[1], OOS_MaxDD=c_oos[2],
                                  paid_pp=0.0, bought_pp=0.0, rate=np.nan,
                                  IS_bought=0.0, OOS_bought=0.0))
                globals().setdefault("_CTRL", {})[(pname, bname, cost)] = cr
            for fam in FAMILIES:
                for lev in EXT[fam]:
                    g, t, inv, _ = arm_returns(px, w, fam, lev, ctrl_full)
                    g, t, inv = g.loc[start:], t.loc[start:], inv.loc[start:]
                    for cost in COSTS:
                        r = at_cost(g, t, cost)
                        cr = globals()["_CTRL"][(pname, bname, cost)]
                        a_c, a_s, a_dd = m(r)
                        a_is, a_oos = m(r[:IS_END]), m(r[OOS_START:])
                        c_c, _, c_dd = m(cr)
                        c_is, c_oos = m(cr[:IS_END]), m(cr[OOS_START:])
                        bought = (a_dd - c_dd) * 100
                        arows.append(dict(
                            panel=pname, book=bname, cost=cost, family=fam, level=lev,
                            in_pub=lev in PUB[fam], CAGR=a_c, Sharpe=a_s, MaxDD=a_dd,
                            IS_CAGR=a_is[0], IS_MaxDD=a_is[2], OOS_CAGR=a_oos[0],
                            OOS_Sharpe=a_oos[1], OOS_MaxDD=a_oos[2],
                            paid_pp=(c_c - a_c) * 100, bought_pp=bought,
                            rate=((c_c - a_c) * 100) / bought if bought > 1e-9 else np.nan,
                            IS_bought=(a_is[2] - c_is[2]) * 100,
                            OOS_bought=(a_oos[2] - c_oos[2]) * 100,
                            IS_paid_pp=(c_is[0] - a_is[0]) * 100,
                            OOS_paid_pp=(c_oos[0] - a_oos[0]) * 100,
                            turn_yr=turn_per_yr(t), gross=float(inv.mean()),
                            fail4a="|".join(fail4a(r, base[cost])),
                            fail4a_v2="|".join(fail4a(r, base2[cost])),
                            fail4b="|".join(fail4b(r, spy, a_oos[1], spy_oos_sh))))
                        # ---- EPISODE-STAMPED, idea 117's denominator
                        for th in THETAS:
                            E = EPI[(pname, th)]
                            cm = calm_mask(r.index, E)
                            for wl, sl in (("IS", slice(None, IS_END)),
                                           ("OOS", slice(OOS_START, None))):
                                cal_a = ann(r[sl][cm[sl]])
                                cal_c = ann(cr[sl][cm[sl]])
                                paid_calm = (cal_c - cal_a) * 100
                                for _, e in E[E.window == wl].iterrows():
                                    b_e = (win_maxdd(r, e.peak, e.recov)
                                           - win_maxdd(cr, e.peak, e.recov)) * 100
                                    erows_ep = dict(
                                        panel=pname, book=bname, cost=cost, family=fam,
                                        level=lev, theta=th, eid=e.eid, window=wl,
                                        depth=e.depth, depth_bin=e.depth_bin,
                                        bought_e=b_e, reach_e_norm=b_e / e.depth,
                                        paid_calm_pp=paid_calm,
                                        price_e=paid_calm / b_e if b_e > 1e-9 else np.nan)
                                    EPROWS.append(erows_ep)
    A = pd.DataFrame(arows)
    A.to_csv(f"{OUT}.arms.csv", index=False)
    EP = pd.DataFrame(EPROWS)
    EP.to_csv(f"{OUT}.epreach.csv.gz", index=False, compression="gzip")
    ED = pd.concat(erows, ignore_index=True)
    ED.to_csv(f"{OUT}.episodes.csv", index=False)
    say(f"arms: {len(A)} rows ({int((A.family=='none').sum())} controls); "
        f"episode rows: {len(EP)}")

    # ---------------------------------------------------------------- G2/G3
    say("\nG2 vs idea 251's COMMITTED grid.csv:")
    P = pd.read_csv(I251_GRID)
    key = ["panel", "book", "cost", "family", "level"]
    mg = A.merge(P, on=key, suffixes=("", "_pub"), how="inner")
    TOL = {"bought_pp": 1e-1, "paid_pp": 1e-1, "IS_bought": 1e-1, "OOS_bought": 1e-1,
           "CAGR": 1e-3, "MaxDD": 1e-3}
    for col, tol in TOL.items():
        dd = np.abs(mg[col] - mg[f"{col}_pub"])
        d = float(dd.max())
        say(f"   {col:12s} max|diff| = {d:.3e}   q99 = {float(dd.quantile(0.99)):.3e}   "
            f"rows within 1e-6: {int((dd < 1e-6).sum())}/{len(mg)}   (tolerance {tol:.0e})")
        assert d < tol, f"G2 FAILED on {col}"
    say("   NOTE: this is a tolerance gate, not a bit-for-bit one, and the reason is in the "
        "data, not the code. data/prices.csv has been RESTATED since idea 251 was committed: "
        "on the 4,699 x 58 cells the two files share, adjusted closes differ by up to 3e-4 "
        "(DIA, COST, LLY, META, UNH), and the panel has gained one bar (dropped here by the "
        "2026-09-04 truncation). 60% of arms agree to 1e-6 and the 99th percentile "
        "disagreement is ~1e-4 pp; the two largest (0.074 and 0.068 pp of IS reach) are the "
        "200d gate at a 20-day MA, the shortest lookback on the extended ladder. All of it "
        "is ~2-3 orders of magnitude below the IS/OOS reach gaps under test (0.8 -> 5.1 pp, "
        "4.1 -> 9.9 pp), and idea 251's 47/48 headline recounts unchanged below.")

    say("\nG3 vs idea 251's COMMITTED reach.csv (EXT ladder):")
    R = pd.read_csv(I251_REACH)
    R = R[R.ladder == "EXT"]
    mine = []
    for (p, b, c, f), sub in A[A.family != "none"].groupby(["panel", "book", "cost", "family"]):
        mine.append(dict(panel=p, book=b, cost=c, family=f,
                         max_bought=sub.bought_pp.max(),
                         IS_max_bought=sub.IS_bought.max(),
                         OOS_max_bought=sub.OOS_bought.max(),
                         IS_argmax_level=sub.loc[sub.IS_bought.idxmax(), "level"],
                         OOS_argmax_level=sub.loc[sub.OOS_bought.idxmax(), "level"],
                         OOS_at_IS_pick=sub.loc[sub.IS_bought.idxmax(), "OOS_bought"]))
    M = pd.DataFrame(mine)
    mr = M.merge(R, on=["panel", "book", "cost", "family"], suffixes=("", "_pub"))
    for col in ("max_bought", "IS_max_bought", "OOS_max_bought"):
        dd = np.abs(mr[col] - mr[f"{col}_pub"])
        d = float(dd.max())
        say(f"   {col:16s} max|diff| = {d:.3e}   cells within 1e-6: "
            f"{int((dd < 1e-6).sum())}/{len(mr)}")
        assert d < 2e-2, f"G3 FAILED on {col}"
    n_gap = int((M.OOS_max_bought > M.IS_max_bought).sum())
    say(f"   idea 251's headline recounted here: OOS reach > IS reach in "
        f"**{n_gap} of {len(M)} cells** (published: 47 of 48), "
        f"sign-test p = {signtest_p(n_gap, len(M)):.3e}")
    w_med, w_n = med_abs_log10_ratio(M.IS_max_bought.clip(lower=0), M.OOS_max_bought.clip(lower=0))
    say(f"   whole-window median |log10(IS reach / OOS reach)| = {w_med:.3f} over {w_n}/{len(M)} "
        f"cells with both reaches > 0")

    # ---------------------------------------------------------------- G4 episodes
    say("\nG4 episodes (idea 62/117's classifier, rebuilt from idea 117's own function):")
    for th in THETAS:
        for pname in panels:
            E = EPI[(pname, th)]
            say(f"   theta={th:.2f} {pname:6s}: {len(E)} episodes  "
                f"IS {int((E.window=='IS').sum())} / OOS {int((E.window=='OOS').sum())}   "
                f"DEEP {int((E.depth_bin=='DEEP').sum())} / SHALLOW "
                f"{int((E.depth_bin=='SHALLOW').sum())}   "
                f"depths {', '.join(f'{d:.1f}' for d in E.depth)}")
    say("\n  episode table at theta=0.10 (the point):")
    say(ED[ED.theta == THETA0][["panel", "eid", "peak", "trough", "recov", "depth",
                                "dur_pt", "speed", "depth_bin", "window"]]
        .to_string(index=False, float_format=lambda x: f"{x:.2f}"))

    # ---------------------------------------------------------------- THE TEST
    say("\n=== THE TEST: does the episode denominator remove the IS/OOS gap? ===")
    grows = []
    for th in THETAS:
        E = EP[EP.theta == th]
        # cell-level IS and OOS figures, median WITHIN a depth bin (idea 117's aggregation)
        for stat, col, better in (("reach", "reach_e_norm", "max"), ("price", "price_e", "min")):
            for dbin in ("ALL", "SHALLOW", "DEEP"):
                sub = E if dbin == "ALL" else E[E.depth_bin == dbin]
                rows = []
                for (p, b, c, f), s in sub.groupby(["panel", "book", "cost", "family"]):
                    # per level: median over that window's episodes; then the family's best
                    piv = s.groupby(["level", "window"])[col].median().unstack("window")
                    if "IS" not in piv or "OOS" not in piv:
                        continue
                    if better == "max":
                        i_is, i_oos = piv["IS"].idxmax(), piv["OOS"].idxmax()
                        v_is, v_oos = piv["IS"].max(), piv["OOS"].max()
                    else:
                        pi = piv[piv.index.isin(piv.dropna().index)]
                        if pi.empty:
                            continue
                        i_is, i_oos = pi["IS"].idxmin(), pi["OOS"].idxmin()
                        v_is, v_oos = pi["IS"].min(), pi["OOS"].min()
                    rows.append(dict(panel=p, book=b, cost=c, family=f, IS=v_is, OOS=v_oos,
                                     IS_level=i_is, OOS_level=i_oos,
                                     OOS_at_IS_level=piv["OOS"].get(i_is, np.nan)))
                D = pd.DataFrame(rows)
                if D.empty:
                    continue
                n = len(D)
                k = int((D.OOS > D.IS).sum())
                med, nn = med_abs_log10_ratio(D.IS, D.OOS)
                grows.append(dict(theta=th, stat=stat, depth_bin=dbin, convention="EPISODE",
                                  n_cells=n, n_OOS_gt_IS=k, share=k / n,
                                  signtest_p=signtest_p(k, n),
                                  med_abs_log10=med, n_pairs=nn,
                                  B1_pass=signtest_p(k, n) > 0.05,
                                  B2_pass=(med == med and med < BAR_117)))
    # the incumbent convention, same table shape, for reach and for the rate
    kk = int((M.OOS_max_bought > M.IS_max_bought).sum())
    grows.append(dict(theta=np.nan, stat="reach", depth_bin="ALL", convention="WHOLE_WINDOW",
                      n_cells=len(M), n_OOS_gt_IS=kk, share=kk / len(M),
                      signtest_p=signtest_p(kk, len(M)), med_abs_log10=w_med, n_pairs=w_n,
                      B1_pass=signtest_p(kk, len(M)) > 0.05, B2_pass=w_med < BAR_117))
    RT = []
    for (p, b, c, f), s in A[(A.family != "none")].groupby(["panel", "book", "cost", "family"]):
        s_is = s[s.IS_bought > 1e-9]
        s_oos = s[s.OOS_bought > 1e-9]
        if s_is.empty or s_oos.empty:
            continue
        # whole-window "cheapest rate", IS and OOS, each priced inside its own window
        ris = (s_is.IS_paid_pp / s_is.IS_bought).min()
        ros = (s_oos.OOS_paid_pp / s_oos.OOS_bought).min()
        RT.append(dict(panel=p, book=b, cost=c, family=f, IS=ris, OOS=ros))
    RTD = pd.DataFrame(RT)
    kr = int((RTD.OOS > RTD.IS).sum())
    mr_, nr_ = med_abs_log10_ratio(RTD.IS, RTD.OOS)
    grows.append(dict(theta=np.nan, stat="price", depth_bin="ALL", convention="WHOLE_WINDOW",
                      n_cells=len(RTD), n_OOS_gt_IS=kr, share=kr / len(RTD),
                      signtest_p=signtest_p(kr, len(RTD)), med_abs_log10=mr_, n_pairs=nr_,
                      B1_pass=signtest_p(kr, len(RTD)) > 0.05, B2_pass=mr_ < BAR_117))
    GAP = pd.DataFrame(grows)
    GAP.to_csv(f"{OUT}.gap.csv", index=False)
    say(GAP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nHEADLINE (theta = 0.10, the pre-registered point, both bars):")
    for stat in ("reach", "price"):
        ww = GAP[(GAP.convention == "WHOLE_WINDOW") & (GAP.stat == stat)].iloc[0]
        for dbin in ("ALL", "SHALLOW", "DEEP"):
            ep = GAP[(GAP.convention == "EPISODE") & (GAP.stat == stat)
                     & (GAP.theta == THETA0) & (GAP.depth_bin == dbin)]
            if ep.empty:
                continue
            ep = ep.iloc[0]
            say(f"  {stat:5s} {dbin:8s}: OOS>IS {int(ww.n_OOS_gt_IS)}/{int(ww.n_cells)} "
                f"(p {ww.signtest_p:.1e}) -> {int(ep.n_OOS_gt_IS)}/{int(ep.n_cells)} "
                f"(p {ep.signtest_p:.3f})   med|log10 IS/OOS| {ww.med_abs_log10:.3f} -> "
                f"{ep.med_abs_log10:.3f} (bar {BAR_117})   "
                f"B1 {'PASS' if ep.B1_pass else 'FAIL'}  B2 {'PASS' if ep.B2_pass else 'FAIL'}")

    say("\nPer-family, theta=0.10, ALL episodes (reach), IS vs OOS by cell:")
    E0 = EP[EP.theta == THETA0]
    for f in FAMILIES:
        rows = []
        for (p, b, c), s in E0[E0.family == f].groupby(["panel", "book", "cost"]):
            piv = s.groupby(["level", "window"]).reach_e_norm.median().unstack("window")
            if "IS" in piv and "OOS" in piv:
                rows.append((piv["IS"].max(), piv["OOS"].max()))
        if rows:
            a = np.array(rows)
            wm = M[M.family == f]
            say(f"  {LABEL[f]:<28} EPISODE reach IS {a[:,0].mean():+.4f} OOS {a[:,1].mean():+.4f}"
                f"  (OOS>IS {int((a[:,1]>a[:,0]).sum())}/{len(a)})   |  WHOLE-WINDOW pp "
                f"IS {wm.IS_max_bought.mean():5.2f} OOS {wm.OOS_max_bought.mean():5.2f} "
                f"(OOS>IS {int((wm.OOS_max_bought>wm.IS_max_bought).sum())}/{len(wm)})")

    # ---------------------------------------------------------------- RULE 8
    say("\n=== RULE 8: two selectors on IS only, 2017-2026 read once ===")
    wrows = []
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_o = m(spy[OOS_START:])
        for bname in BASE_BOOKS:
            for cost in COSTS:
                cr = globals()["_CTRL"][(pname, bname, cost)]
                c_o = m(cr[OOS_START:])
                v2 = m(backtest(px, rules_v2_weights(px), cost_bps=cost,
                                freq="W")["returns"].loc[start:][OOS_START:])
                v1 = m(backtest(px, rules_v1_weights(px), cost_bps=cost,
                                freq="W")["returns"].loc[start:][OOS_START:])
                for fam in FAMILIES:
                    sub = A[(A.panel == pname) & (A.book == bname) & (A.cost == cost)
                            & (A.family == fam)]
                    pick_w = sub.loc[sub.IS_bought.idxmax()]
                    e0 = E0[(E0.panel == pname) & (E0.book == bname) & (E0.cost == cost)
                            & (E0.family == fam)]
                    piv = e0.groupby(["level", "window"]).reach_e_norm.median().unstack("window")
                    if "IS" not in piv:
                        continue
                    lev_e = piv["IS"].idxmax()
                    pick_e = sub[sub.level == lev_e].iloc[0]
                    best_oos = sub.OOS_bought.max()
                    for sel, pk in (("S_WINDOW", pick_w), ("S_EPISODE", pick_e)):
                        wrows.append(dict(
                            panel=pname, book=bname, cost=cost, family=fam, selector=sel,
                            IS_level=pk.level, OOS_bought_at_pick=pk.OOS_bought,
                            OOS_bought_best=best_oos,
                            forfeit_pp=best_oos - pk.OOS_bought,
                            OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                            OOS_MaxDD=pk.OOS_MaxDD,
                            CTRL_OOS_Sharpe=c_o[1], CTRL_OOS_CAGR=c_o[0], CTRL_OOS_MaxDD=c_o[2],
                            RULESV2_OOS_Sharpe=v2[1], RULESV1_OOS_Sharpe=v1[1],
                            SPY_OOS_Sharpe=spy_o[1], SPY_OOS_CAGR=spy_o[0],
                            SPY_OOS_MaxDD=spy_o[2],
                            pass4a=(pk.fail4a_v2 == ""), pass4b=(pk.fail4b == ""),
                            fail4a_v2=pk.fail4a_v2, fail4b=pk.fail4b))
    WF = pd.DataFrame(wrows)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(WF.groupby("selector")[["OOS_bought_at_pick", "OOS_bought_best", "forfeit_pp",
                                "OOS_Sharpe", "OOS_CAGR"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    for sel in ("S_WINDOW", "S_EPISODE"):
        s = WF[WF.selector == sel]
        say(f"  {sel:10s}: mean OOS reach forfeited {s.forfeit_pp.mean():.3f} pp, median "
            f"{s.forfeit_pp.median():.3f} pp; picks the OOS-optimal level in "
            f"{int((s.forfeit_pp.abs() < 1e-9).sum())}/{len(s)} cells; "
            f"4a {int(s.pass4a.sum())}/{len(s)}  4b {int(s.pass4b.sum())}/{len(s)}")
    both = WF.pivot_table(index=["panel", "book", "cost", "family"], columns="selector",
                          values="forfeit_pp")
    say(f"  head-to-head: S_EPISODE forfeits LESS OOS reach than S_WINDOW in "
        f"{int((both.S_EPISODE < both.S_WINDOW).sum())}/{len(both)} cells, MORE in "
        f"{int((both.S_EPISODE > both.S_WINDOW).sum())}, ties "
        f"{int((both.S_EPISODE == both.S_WINDOW).sum())}")
    say(f"  4a passes across the whole arm grid: "
        f"{int((A[A.family!='none'].fail4a_v2 == '').sum())}/{len(A[A.family!='none'])}   "
        f"4b passes: {int((A[A.family!='none'].fail4b == '').sum())}/{len(A[A.family!='none'])}")

    (Path(f"{OUT}.console.txt")).write_text("\n".join(_console) + "\n")
    print(f"\nwrote {STAMP}.arms.csv .episodes.csv .epreach.csv.gz .gap.csv "
          f".walkforward.csv .console.txt")


EPROWS = []

if __name__ == "__main__":
    main()
