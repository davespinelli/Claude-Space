#!/usr/bin/env python3
"""
IDEA 2115 (lane C, 2026-09-22) -- is-the-REBALANCE-OFFSET-SPREAD-a-COST-ARTEFACT-or-a-
                                  PATH-ARTEFACT

THE QUESTION, as filed.  Idea 914 killed a KEEP-4b candidate because its DD margin was
smaller than the SAME BOOK's spread across the five weekly rebalance offsets, and idea 2119
(lane B, today) turned that clause on a 25-cell ladder and found only 7 of 16 passes survive
5 of 5 offsets.  Both runs treat the offset spread as a given.  Neither asks WHAT IT IS.
There are exactly two candidates and they have opposite consequences:

    COST ARTEFACT -- the spread is a turnover-TIMING bill.  Different weekdays trade at
      different prices and therefore pay a different cost bill, so the spread must COLLAPSE
      TOWARD ZERO as the cost rung goes to zero.  If so, the spread is a modelling
      convention: it shrinks with better execution and a book is not really weekday-fragile.
    PATH ARTEFACT -- the spread is PATH SAMPLING.  Rebalancing on Thursday instead of Friday
      puts a genuinely different portfolio on the tape, so the spread survives at 0 bps.  If
      so, the spread is irreducible sampling noise in the book itself, 914's clause is about
      the RULE and not about the broker, and no execution improvement removes it.

The discriminator the idea names is the SLOPE of the spread in the cost rung, and its
INTERCEPT at 0 bps.  This run prices it.

AN EXACT DECOMPOSITION IS AVAILABLE AND IS USED (gate G5).  In this engine costs never touch
the held path:
        net_d(c) = gross_d - (c/1e4) * turnover_d
so for any two offsets d and 0, at every cost rung c, the daily net-return difference splits
EXACTLY into
        net_d(c) - net_0(c)  =  [gross_d - gross_0]            <- PATH, cost-independent
                             -  (c/1e4) * [turnover_d - turnover_0]   <- COST, linear in c
The path term is literally the 0 bps difference.  So the question has an arithmetic answer
as well as an empirical one, and B3 below reports both against each other.

THE BOOKS -- FIXED, three of the record's own certified shapes, REPORTED not tuned:
    BAND03_G075  the LIVE RULES v2 book (band 0.03, gross 0.75) == baseline.rules_v2_weights
    TOP20        the 2026-09-04 FIRST KEEP-4b shape: top 20 by the composite with NO vol
                 scaler, eligibility = above 200d MA and vol20 < 0.60, FIXED 0.75/20 per name
    EWELIG       equal-weight EVERY eligible name at 0.75/#priced (the 2026-09-03 memo's
                 Finding 2 book) -- carried because it has a different turnover profile and
                 the cost/path split is a claim about turnover.
    All three: weights decided at close t, applied at t+1; long only; no leverage; gated-out
    weight goes to CASH (de-gross, never re-spread).

TUNED PARAMETERS -- EXACTLY TWO, and EVERY grid point is published (<slug>.grid.csv.gz):
    1. COST RUNG  c in {0, 10, 25, 50} bps     (PROTOCOL rung 2 is 10 bps)
    2. CADENCE    R in {D, W, M, Q}
NOT TUNED, and declared as such before any number was read:
    OFFSET d in {0,1,2,3,4} is a MEASUREMENT, never a choice.  The reported book is ALWAYS
      d=0 (the published convention, gate G2).  d=1..4 exist only to build the spread.  No
      cell is ever selected on its best offset and no verdict is read off d>0.
    PANEL {U56 = research/universe.json, B136 = research/universe_broad.json}.
    BOOK  {BAND03_G075, TOP20, EWELIG}.
    WINDOWS FULL / IS (..2016-12-31) / OOS (2017-01-01..), rule 8.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE DISCRIMINATOR.  For every (panel, book, cadence, window, leg) cell define the
      spread S(c) = max-min over the 5 offsets at cost rung c.  Pre-stated:
         COST-ARTEFACT verdict for a cell if  S(0) <= 0.10 * S(50);
         PATH-ARTEFACT verdict for a cell if  S(0) >= 0.50 * S(50);
         MIXED otherwise.  Report the share of cells in each bucket, per leg and overall.
  B2  SLOPE.  OLS of S(c) on c over the four rungs.  Report slope (leg units per bp),
      intercept, R^2, and the intercept share S(0)/S(10) -- the fraction of the spread that
      PROTOCOL's own rung inherits from path sampling alone.
  B3  THE ARITHMETIC CONTROL.  For every offset d, the annualised cost-bill difference
      COST_d(c) = (c/1e4) * (annualised turnover_d - annualised turnover_0) against the
      cost-free CAGR difference PATH_d = CAGR_d(0) - CAGR_0(0).  Report the ratio
      |COST_d(10)| / |PATH_d| per cell.  If the spread were a cost artefact this ratio is
      large; if a path artefact it is small.  This is the exact split, not a regression.
  B4  DOES THE COST RUNG MOVE 914's CLAUSE?  At every (panel, book, cadence, window, rung)
      report the d=0 4b verdict, every leg margin, and whether each margin exceeds that
      leg's own 5-offset spread -- i.e. whether a book is "weekday-robust" at 0 bps but not
      at 50 bps, or the reverse.  Also the 5-of-5 verdict stability (2119's B3 form).
  B5  RULE 8.  The two tuned dials are chosen on the IS window ONLY (2009..2016), at d=0, by
      IS Sharpe, per panel per book; 2017-2026 is read ONCE.  The COST RUNG IS NOT A FREE
      CHOICE IN REALITY -- PROTOCOL rung 2 fixes it at 10 bps -- so the HEADLINE rule-8 pick
      selects CADENCE at 10 bps, and the both-dials-free pick is reported alongside as a
      sensitivity, never as the headline.  Report OOS CAGR / Sharpe / MaxDD against RULES v2
      and SPY, and BOTH KEEP paths.
  B6  PATH 4a scored at EVERY grid point (Sharpe > RULES v2 in BOTH halves AND MaxDD no
      worse than RULES v2).
  B7  CONTROL.  SPY buy-and-hold never rebalances, so its legs are offset-invariant by
      construction and the 4b bars are constant across d.  Gated (G7); any spread reported
      here is the BOOK's.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', cost_bps=10)   bar max|d| < 1e-12
  G2  offset_mask(idx, 0, R) == engine.rebalance_mask(idx, R)       bar 0 differing rows, 4/4
  G3  the BAND03_G075 weights == baseline.rules_v2_weights          bar max|d| == 0
  G4  CADENCE D is a STRUCTURAL ZERO: every day is a rebalance day, so offset_mask(.,d,'D')
      is identical for all d and the D spread must be EXACTLY 0.  Bar: 0.0 at every leg.
  G5  COST LINEARITY: net(gross,turn,c) from ONE path equals a full re-run at cost c.
      bar max|d| < 1e-15.  This is what makes B3's split exact rather than a fit.
  G6  OFFSET FAIRNESS / CLIPPING census: periods too short to carry offset d (the pick is
      clamped to the period's first day).  Published per cadence per offset; B1 is re-read
      on the clip-free offsets as B1c rather than the bar being quietly widened.
  G7  SPY offset-invariance (B7's control), bar max|d| == 0 across the 5 offsets.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every
absolute CAGR and drawdown level here is optimistic.  This run is a WITHIN-TAPE contrast --
same names, same dates, only the rebalance weekday and the cost rung move -- which is what
the idea asks; it does not repair the level.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_offset-spread-cost-vs-path_C.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score, rules_v1_weights  # noqa
from engine import backtest, metrics, rebalance_mask                                       # noqa

SLUG = "2026-09-22_offset-spread-cost-vs-path_C"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

GATES = []
def gate(name, got, bar, ok):
    GATES.append((name, str(got), str(bar), bool(ok)))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name:52s} got {got}   bar {bar}")

COSTS    = [0, 10, 25, 50]          # TUNED axis 1
CADENCES = ["D", "W", "M", "Q"]     # TUNED axis 2
OFFSETS  = [0, 1, 2, 3, 4]          # measurement only, never selected on
COST0    = 10                       # PROTOCOL rung 2
GROSS0   = 0.75
BAND0    = 0.03
VOLCAP   = 0.60
IS_END   = "2016-12-31"
OOS_BEG  = "2017-01-01"
DD_CAP    = 0.60
CAGR_FLOOR = 0.70
LEGS_SPREAD = ["CAGR", "Sharpe", "MaxDD"]


# ==========================================================================================
# offsets + a schedule-taking backtester (engine.backtest only accepts a freq string)
# ==========================================================================================
def offset_mask(idx, d, freq):
    """True d trading days BEFORE the last trading day of each period.  d=0 == rebalance_mask.
    Clamped to the period's first day when the period is shorter than d+1 days (counted)."""
    if freq == "D":
        return pd.Series(True, index=idx), 0
    key = pd.Series(idx.to_period(freq), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def run(prices, weights, mask):
    """engine.backtest's loop in numpy, semantics byte-for-byte (gate G1).  Costs are applied
    afterwards -- they never change the held path -- so ONE loop serves every cost rung."""
    rets = prices.pct_change().fillna(0.0).values
    wt = pd.DataFrame(weights, index=prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index)


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


# ==========================================================================================
# the three fixed books
# ==========================================================================================
def _ew(px, elig, gross=GROSS0):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(elig, 0.0)


def build_books(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    return {
        "BAND03_G075": rules_v2_weights(px, BAND0, GROSS0),
        "TOP20":       (rank <= 20).astype(float) * (GROSS0 / 20),
        "EWELIG":      _ew(px, elig, GROSS0),
    }


# ==========================================================================================
# scoring
# ==========================================================================================
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    """PROTOCOL 4b against SPY on the SAME window.  Margins in the leg's own unit:
    Sharpe points for H1/H2, pp for DD and CAGR."""
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def legs4a(s, sb):
    return bool(s["H1"] > sb["H1"] and s["H2"] > sb["H2"] and s["MaxDD"] >= sb["MaxDD"])


# leg -> (statistic whose offset spread the margin is judged against, unit scale)
LEGUNIT = dict(H1=("H1", 1.0), H2=("H2", 1.0), DD=("MaxDD", 100.0), CAGR=("CAGR", 100.0))


def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if np.allclose(y, y[0]):
        return 0.0, float(y[0]), 1.0
    sl, ic = np.polyfit(x, y, 1)
    yh = sl * x + ic
    ss_res = float(((y - yh) ** 2).sum()); ss_tot = float(((y - y.mean()) ** 2).sum())
    return float(sl), float(ic), (1 - ss_res / ss_tot if ss_tot > 0 else 1.0)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 2115 lane C 2026-09-22 -- is the REBALANCE-OFFSET SPREAD a COST ARTEFACT")
    P("                               or a PATH ARTEFACT?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: cost rung {COSTS} bps x cadence {CADENCES}   ({len(COSTS)*len(CADENCES)} cells/book/panel)")
    P(f"not tuned: offsets {OFFSETS} (measurement only; the book is ALWAYS d=0),")
    P(f"           books BAND03_G075 / TOP20 / EWELIG, panels U56 + B136,")
    P(f"           windows FULL / IS ..{IS_END} / OOS {OOS_BEG}..")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} cols  {v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P("")

    # ---------------------------------------------------------------- GATES
    P("-" * 100); P("CONSTRUCTION GATES"); P("-" * 100)
    pxg = panels["U56"]
    wg = rules_v2_weights(pxg, BAND0, GROSS0)

    mw, _ = offset_mask(pxg.index, 0, "W")
    g_ref = backtest(pxg, wg, cost_bps=COST0, freq="W")["returns"]
    gr, tu = run(pxg, wg, mw)
    gate("G1 local run()+net() == engine.backtest(W,10bps)",
         f"{float((net(gr, tu, COST0) - g_ref).abs().max()):.3e}", "< 1e-12",
         float((net(gr, tu, COST0) - g_ref).abs().max()) < 1e-12)

    n_ok = 0
    for R in CADENCES:
        m0, _ = offset_mask(pxg.index, 0, R)
        diff = int((m0.values != rebalance_mask(pxg.index, R).values).sum())
        n_ok += (diff == 0)
    gate("G2 offset_mask(.,0,R) == rebalance_mask(.,R)", f"{n_ok}/4 cadences, 0 diffs", "4/4", n_ok == 4)

    bk = build_books(pxg)
    gate("G3 BAND03_G075 == baseline.rules_v2_weights",
         f"{float((bk['BAND03_G075'] - rules_v2_weights(pxg)).abs().max().max()):.3e}", "== 0",
         float((bk["BAND03_G075"] - rules_v2_weights(pxg)).abs().max().max()) == 0.0)

    dmasks = [offset_mask(pxg.index, d, "D")[0] for d in OFFSETS]
    gate("G4 cadence D offset masks identical (structural zero)",
         f"{sum(int((dmasks[0].values != m.values).sum()) for m in dmasks)} diffs", "== 0",
         all(int((dmasks[0].values != m.values).sum()) == 0 for m in dmasks))

    ref25 = backtest(pxg, wg, cost_bps=25, freq="W")["returns"]
    gate("G5 cost linearity: net(path,25) == re-run at 25 bps",
         f"{float((net(gr, tu, 25) - ref25).abs().max()):.3e}", "< 1e-15",
         float((net(gr, tu, 25) - ref25).abs().max()) < 1e-15)

    clip = {}
    for R in CADENCES:
        for d in OFFSETS:
            clip[(R, d)] = offset_mask(pxg.index, d, R)[1]
    clipfree = [d for d in OFFSETS if all(clip[(R, d)] == 0 for R in CADENCES)]
    gate("G6 clipping census (periods shorter than d+1 days)",
         f"clip-free offsets {clipfree}; W: " + ",".join(f"d{d}={clip[('W',d)]}" for d in OFFSETS),
         "published, B1c re-read on clip-free", True)

    spy_g = pxg["SPY"].pct_change().fillna(0)
    gate("G7 SPY buy-and-hold offset-invariant (B7 control)", "0.0 by construction", "== 0", True)
    P("")
    P(f"  GATES {sum(g[3] for g in GATES)}/{len(GATES)} PASS")
    P("")

    # ---------------------------------------------------------------- the grid
    P("-" * 100); P("BUILDING THE GRID"); P("-" * 100)
    rows = []          # one row per (panel, book, cadence, offset, cost, window)
    paths = {}         # (panel, book, cadence, offset) -> (gross, turn) trimmed
    base_s, spy_s = {}, {}

    for pname, px in panels.items():
        start = px.index[260]
        books = build_books(px)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        bmask, _ = offset_mask(px.index, 0, "W")
        bg, bt = run(px, rules_v2_weights(px), bmask)          # live baseline, weekly, d=0
        for c in COSTS:
            br = net(bg, bt, c).loc[start:]
            for wn, rr in (("FULL", br), ("IS", br.loc[:IS_END]), ("OOS", br.loc[OOS_BEG:])):
                base_s[(pname, c, wn)] = stats(rr)
        for wn, rr in (("FULL", spy), ("IS", spy.loc[:IS_END]), ("OOS", spy.loc[OOS_BEG:])):
            spy_s[(pname, wn)] = stats(rr)

        for bname, W in books.items():
            for R in CADENCES:
                for d in OFFSETS:
                    m, _ = offset_mask(px.index, d, R)
                    g, t = run(px, W, m)
                    g, t = g.loc[start:], t.loc[start:]
                    paths[(pname, bname, R, d)] = (g, t)
                    for c in COSTS:
                        r = net(g, t, c)
                        for wn, rr, tt in (("FULL", r, t),
                                           ("IS", r.loc[:IS_END], t.loc[:IS_END]),
                                           ("OOS", r.loc[OOS_BEG:], t.loc[OOS_BEG:])):
                            s = stats(rr)
                            p4b, L, Mg = legs4b(s, spy_s[(pname, wn)])
                            rows.append(dict(
                                panel=pname, book=bname, cadence=R, offset=d, cost=c, window=wn,
                                CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"],
                                H1=s["H1"], H2=s["H2"],
                                turn_ann=float(tt.sum()) / (len(tt) / 252),
                                pass4b=p4b, pass4a=legs4a(s, base_s[(pname, c, wn)]),
                                **{f"leg_{k}": v for k, v in L.items()},
                                **{f"mg_{k}": v for k, v in Mg.items()}))
                P(f"  {pname:5s} {bname:12s} {R}  done  ({time.time()-t0:5.0f}s)")

    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv.gz", index=False, compression="gzip")
    P(f"  grid: {len(G)} rows -> {SLUG}.grid.csv.gz")
    P("")

    # ---------------------------------------------------------------- B1 / B2 spreads
    P("=" * 100); P("B1 + B2 -- THE SPREAD AS A FUNCTION OF THE COST RUNG"); P("=" * 100)
    P("S(c) = max - min over the 5 offsets at cost rung c.  Pre-stated buckets:")
    P("   COST artefact  S(0) <= 0.10*S(50)   |   PATH artefact  S(0) >= 0.50*S(50)   |   MIXED else")
    P("")
    sp_rows = []
    for (pn, bn, R, wn), sub in G.groupby(["panel", "book", "cadence", "window"]):
        for leg in LEGS_SPREAD:
            S = {}
            for c in COSTS:
                v = sub[sub["cost"] == c][leg]
                S[c] = float(v.max() - v.min())
            sl, ic, r2 = ols(COSTS, [S[c] for c in COSTS])
            bucket = ("COST" if S[0] <= 0.10 * S[50] else
                      "PATH" if S[0] >= 0.50 * S[50] else "MIXED") if S[50] > 0 else "ZERO"
            sp_rows.append(dict(panel=pn, book=bn, cadence=R, window=wn, leg=leg,
                                S0=S[0], S10=S[10], S25=S[25], S50=S[50],
                                slope_per_bp=sl, intercept=ic, r2=r2,
                                share_S0_over_S10=(S[0] / S[10] if S[10] > 0 else np.nan),
                                bucket=bucket))
    SP = pd.DataFrame(sp_rows)
    SP.to_csv(OUT / f"{SLUG}.spreads.csv", index=False)

    live = SP[SP["cadence"] != "D"]                     # D is the structural zero (G4)
    P(f"cells (cadence D excluded as the structural-zero control): {len(live)}")
    P("")
    P("BUCKET SHARES, by leg:")
    P(f"  {'leg':8s} {'n':>4s} {'COST':>7s} {'MIXED':>7s} {'PATH':>7s} {'ZERO':>7s}")
    for leg in LEGS_SPREAD:
        s = live[live["leg"] == leg]
        P(f"  {leg:8s} {len(s):4d} " + " ".join(
            f"{(s['bucket']==b).mean():7.3f}" for b in ("COST", "MIXED", "PATH", "ZERO")))
    P(f"  {'ALL':8s} {len(live):4d} " + " ".join(
        f"{(live['bucket']==b).mean():7.3f}" for b in ("COST", "MIXED", "PATH", "ZERO")))
    P("")
    P("MEDIAN S(0)/S(10) -- the share of PROTOCOL's own 10 bps spread already present at 0 bps:")
    for leg in LEGS_SPREAD:
        s = live[live["leg"] == leg]["share_S0_over_S10"].dropna()
        P(f"  {leg:8s} median {s.median():6.3f}   q10 {s.quantile(.10):6.3f}   q90 {s.quantile(.90):6.3f}   n {len(s)}")
    P("")
    P("PER (book, cadence) at window FULL, panel-pooled -- every grid point is in the CSV:")
    P(f"  {'panel':5s} {'book':12s} {'cad':3s} {'leg':7s} {'S(0)':>9s} {'S(10)':>9s} {'S(25)':>9s} {'S(50)':>9s} "
      f"{'slope/bp':>10s} {'icept':>9s} {'R2':>5s} {'S0/S10':>7s} bucket")
    for _, r in live[live["window"] == "FULL"].sort_values(["panel", "book", "cadence", "leg"]).iterrows():
        P(f"  {r['panel']:5s} {r['book']:12s} {r['cadence']:3s} {r['leg']:7s} "
          f"{r['S0']:9.4f} {r['S10']:9.4f} {r['S25']:9.4f} {r['S50']:9.4f} "
          f"{r['slope_per_bp']:10.2e} {r['intercept']:9.4f} {r['r2']:5.2f} "
          f"{r['share_S0_over_S10']:7.3f} {r['bucket']}")
    P("")
    P("B1c -- re-read on the CLIP-FREE offsets only (G6):")
    cf = G[G["offset"].isin(clipfree)]
    b1c = []
    for (pn, bn, R, wn), sub in cf.groupby(["panel", "book", "cadence", "window"]):
        if R == "D":
            continue
        for leg in LEGS_SPREAD:
            S = {c: float(sub[sub["cost"] == c][leg].max() - sub[sub["cost"] == c][leg].min()) for c in COSTS}
            b1c.append(dict(leg=leg, bucket=("COST" if S[0] <= 0.10 * S[50] else
                                             "PATH" if S[0] >= 0.50 * S[50] else "MIXED") if S[50] > 0 else "ZERO",
                            share=(S[0] / S[10] if S[10] > 0 else np.nan)))
    B1C = pd.DataFrame(b1c)
    P(f"  clip-free offsets {clipfree}; n={len(B1C)}; " + " ".join(
        f"{b} {(B1C['bucket']==b).mean():.3f}" for b in ("COST", "MIXED", "PATH", "ZERO")) +
      f"; median S0/S10 {B1C['share'].median():.3f}")
    P("")

    # ---------------------------------------------------------------- B3 exact split
    P("=" * 100); P("B3 -- THE EXACT ARITHMETIC SPLIT (not a fit)"); P("=" * 100)
    P("net_d(c) - net_0(c) = [gross_d - gross_0]  -  (c/1e4)*[turnover_d - turnover_0]")
    P("PATH_d   = CAGR_d(0) - CAGR_0(0)            in pp/yr (cost-free, the FIRST bracket)")
    P("COST_d(c)= (c/1e4) * (annual turnover_d - annual turnover_0)  in pp/yr (the SECOND)")
    P("")
    b3 = []
    for (pn, bn, R, wn), sub in G[G["window"].isin(["FULL", "OOS"])].groupby(["panel", "book", "cadence", "window"]):
        if R == "D":
            continue
        z = sub[sub["cost"] == 0].set_index("offset")
        for d in OFFSETS:
            if d == 0:
                continue
            path = (z.loc[d, "CAGR"] - z.loc[0, "CAGR"]) * 100
            dT = z.loc[d, "turn_ann"] - z.loc[0, "turn_ann"]
            for c in (COST0, 50):
                b3.append(dict(panel=pn, book=bn, cadence=R, window=wn, offset=d, cost=c,
                               path_pp=path, cost_pp=-(c / 1e4) * dT * 100, dTurn_ann=dT,
                               ratio=abs((c / 1e4) * dT * 100) / abs(path) if abs(path) > 1e-12 else np.nan))
    B3 = pd.DataFrame(b3)
    B3.to_csv(OUT / f"{SLUG}.split.csv", index=False)
    for c in (COST0, 50):
        s = B3[B3["cost"] == c]
        P(f"  cost {c:2d} bps: |COST_d| / |PATH_d|  median {s['ratio'].median():7.4f}  "
          f"q90 {s['ratio'].quantile(.90):7.4f}  max {s['ratio'].max():7.4f}  "
          f"share > 1 (cost dominates) {(s['ratio'] > 1).mean():.4f}   n={len(s)}")
    P("")
    P("  by book, at PROTOCOL's 10 bps (median ratio, and median |PATH_d| in pp/yr):")
    for bn, s in B3[B3["cost"] == COST0].groupby("book"):
        P(f"    {bn:12s} ratio median {s['ratio'].median():7.4f}   |PATH_d| median {s['path_pp'].abs().median():6.3f} pp/yr"
          f"   |COST_d| median {s['cost_pp'].abs().median():6.4f} pp/yr")
    P("")
    P("  by cadence, at PROTOCOL's 10 bps:")
    for R, s in B3[B3["cost"] == COST0].groupby("cadence"):
        P(f"    {R}  ratio median {s['ratio'].median():7.4f}   |PATH_d| median {s['path_pp'].abs().median():6.3f} pp/yr"
          f"   |dTurnover| median {s['dTurn_ann'].abs().median():6.3f} x/yr")
    P("")

    # ---------------------------------------------------------------- B4 914's clause vs cost
    P("=" * 100); P("B4 -- DOES THE COST RUNG MOVE IDEA 914's CLAUSE?"); P("=" * 100)
    P("For every d=0 book: the 4b verdict, each leg margin, and whether that margin exceeds")
    P("its OWN 5-offset spread at the same rung.  Plus the 5-of-5 verdict stability (2119's B3).")
    P("")
    b4 = []
    for (pn, bn, R, wn, c), sub in G.groupby(["panel", "book", "cadence", "window", "cost"]):
        if R == "D":
            continue
        z = sub.set_index("offset")
        r0 = z.loc[0]
        spreads = {k: float(z[v[0]].max() - z[v[0]].min()) * v[1] for k, v in LEGUNIT.items()}
        clears = {k: bool(r0[f"leg_{k}"]) and abs(r0[f"mg_{k}"]) > spreads[k] for k in LEGUNIT}
        b4.append(dict(panel=pn, book=bn, cadence=R, window=wn, cost=c,
                       pass4b=bool(r0["pass4b"]), pass4a=bool(r0["pass4a"]),
                       stable5of5=bool(z["pass4b"].all()),
                       all_legs_clear=bool(r0["pass4b"]) and all(clears.values()),
                       **{f"mg_{k}": float(r0[f"mg_{k}"]) for k in LEGUNIT},
                       **{f"sp_{k}": spreads[k] for k in LEGUNIT},
                       **{f"clr_{k}": clears[k] for k in LEGUNIT}))
    B4 = pd.DataFrame(b4)
    B4.to_csv(OUT / f"{SLUG}.clause.csv", index=False)
    P(f"  {'cost':>4s} {'n4b':>4s} {'stable5of5':>11s} {'allLegsClear':>13s} " +
      " ".join(f"{'clr_'+k:>8s}" for k in LEGUNIT))
    for c in COSTS:
        s = B4[(B4["cost"] == c)]
        ps = s[s["pass4b"]]
        P(f"  {c:4d} {len(ps):4d} " +
          (f"{ps['stable5of5'].mean():11.3f} {ps['all_legs_clear'].mean():13.3f} " +
           " ".join(f"{ps['clr_'+k].mean():8.3f}" for k in LEGUNIT) if len(ps) else
           f"{'-':>11s} {'-':>13s} " + " ".join(f"{'-':>8s}" for k in LEGUNIT)))
    P("")
    P("  every d=0 4b PASS, all rungs (panel/book/cadence/window/cost | margins | own spreads):")
    ps = B4[B4["pass4b"]].sort_values(["panel", "book", "cadence", "window", "cost"])
    if len(ps) == 0:
        P("    (none)")
    for _, r in ps.iterrows():
        P(f"    {r['panel']:5s} {r['book']:12s} {r['cadence']} {r['window']:4s} c={r['cost']:2d} | " +
          " ".join(f"{k} {r['mg_'+k]:+7.3f}/sp {r['sp_'+k]:6.3f}{'ok' if r['clr_'+k] else 'XX'}" for k in LEGUNIT) +
          f" | 5of5 {'Y' if r['stable5of5'] else 'N'} | allclear {'Y' if r['all_legs_clear'] else 'N'}")
    P("")

    # ---------------------------------------------------------------- B6 4a
    P("=" * 100); P("B6 -- PATH 4a AT EVERY GRID POINT (d=0)"); P("=" * 100)
    z0 = G[(G["offset"] == 0) & (G["cadence"] != "D")]
    P(f"  4a passes: {int(z0['pass4a'].sum())} of {len(z0)} d=0 cells ({z0['pass4a'].mean():.4f})")
    for (bn,), s in z0.groupby(["book"]):
        P(f"    {bn:12s} {int(s['pass4a'].sum()):3d}/{len(s):3d}   4b {int(s['pass4b'].sum()):3d}/{len(s):3d}")
    P("")

    # ---------------------------------------------------------------- B5 rule 8
    P("=" * 100); P("B5 -- RULE 8 WALK-FORWARD (dials chosen on IS 2009..2016 only; OOS read ONCE)")
    P("=" * 100)
    wf = []
    for pn in panels:
        for bn in ("BAND03_G075", "TOP20", "EWELIG"):
            IS = G[(G["panel"] == pn) & (G["book"] == bn) & (G["window"] == "IS") &
                   (G["offset"] == 0) & (G["cadence"] != "D")]
            for label, cand in (("HEADLINE cadence@10bps", IS[IS["cost"] == COST0]),
                                ("SENSITIVITY both dials", IS)):
                pick = cand.sort_values(["Sharpe", "cadence", "cost"], ascending=[False, True, True]).iloc[0]
                R, c = pick["cadence"], int(pick["cost"])
                O = G[(G["panel"] == pn) & (G["book"] == bn) & (G["window"] == "OOS") &
                      (G["offset"] == 0) & (G["cadence"] == R) & (G["cost"] == c)].iloc[0]
                bs, ss = base_s[(pn, c, "OOS")], spy_s[(pn, "OOS")]
                s = dict(CAGR=O["CAGR"], Sharpe=O["Sharpe"], MaxDD=O["MaxDD"], H1=O["H1"], H2=O["H2"])
                p4b, L, Mg = legs4b(s, ss)
                osp = G[(G["panel"] == pn) & (G["book"] == bn) & (G["window"] == "OOS") &
                        (G["cadence"] == R) & (G["cost"] == c)]
                sp = {k: float(osp[v[0]].max() - osp[v[0]].min()) * v[1] for k, v in LEGUNIT.items()}
                wf.append(dict(panel=pn, book=bn, mode=label, pick_cadence=R, pick_cost=c,
                               IS_Sharpe=pick["Sharpe"],
                               oCAGR=s["CAGR"], oSharpe=s["Sharpe"], oMaxDD=s["MaxDD"],
                               base_oCAGR=bs["CAGR"], base_oSharpe=bs["Sharpe"], base_oMaxDD=bs["MaxDD"],
                               spy_oCAGR=ss["CAGR"], spy_oSharpe=ss["Sharpe"], spy_oMaxDD=ss["MaxDD"],
                               pass4b_oos=p4b, pass4a_oos=legs4a(s, bs),
                               stable5of5_oos=bool(osp["pass4b"].all()),
                               **{f"mg_{k}": Mg[k] for k in LEGUNIT},
                               **{f"sp_{k}": sp[k] for k in LEGUNIT}))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    for _, r in WF.iterrows():
        P(f"  {r['panel']:5s} {r['book']:12s} {r['mode']:24s} pick {r['pick_cadence']}@{r['pick_cost']:2d}bps "
          f"(IS S {r['IS_Sharpe']:.3f})")
        P(f"        OOS  book {r['oCAGR']:7.2%} / {r['oSharpe']:6.3f} / {r['oMaxDD']:7.2%}   "
          f"RULESv2 {r['base_oCAGR']:7.2%} / {r['base_oSharpe']:6.3f} / {r['base_oMaxDD']:7.2%}   "
          f"SPY {r['spy_oCAGR']:7.2%} / {r['spy_oSharpe']:6.3f} / {r['spy_oMaxDD']:7.2%}")
        P(f"        4b {'PASS' if r['pass4b_oos'] else 'FAIL'}   4a {'PASS' if r['pass4a_oos'] else 'FAIL'}"
          f"   5of5 offsets {'Y' if r['stable5of5_oos'] else 'N'}   margins/spreads: " +
          " ".join(f"{k} {r['mg_'+k]:+6.3f}/{r['sp_'+k]:5.3f}" for k in LEGUNIT))
    P("")
    P("  FULL-sample halves for the headline picks (both KEEP paths need them):")
    for _, r in WF[WF["mode"].str.startswith("HEADLINE")].iterrows():
        F = G[(G["panel"] == r["panel"]) & (G["book"] == r["book"]) & (G["window"] == "FULL") &
              (G["offset"] == 0) & (G["cadence"] == r["pick_cadence"]) & (G["cost"] == r["pick_cost"])].iloc[0]
        bs, ss = base_s[(r["panel"], int(r["pick_cost"]), "FULL")], spy_s[(r["panel"], "FULL")]
        P(f"    {r['panel']:5s} {r['book']:12s} FULL {F['CAGR']:7.2%} / {F['Sharpe']:6.3f} / {F['MaxDD']:7.2%}"
          f"   H1 {F['H1']:.3f} H2 {F['H2']:.3f}  vs RULESv2 H1 {bs['H1']:.3f} H2 {bs['H2']:.3f}"
          f"  vs SPY H1 {ss['H1']:.3f} H2 {ss['H2']:.3f}   4b {'PASS' if F['pass4b'] else 'FAIL'}"
          f"  4a {'PASS' if F['pass4a'] else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 100); P("VERDICT"); P("=" * 100)
    sh = live["share_S0_over_S10"].dropna()
    bc = live["bucket"].value_counts(normalize=True)
    r10 = B3[B3["cost"] == COST0]["ratio"]
    P(f"  ANSWER: the offset spread is a {'PATH' if sh.median() >= 0.5 else 'COST'} artefact.")
    P(f"    median S(0)/S(10) = {sh.median():.3f}  ({len(sh)} cells) -- that share of PROTOCOL's own")
    P(f"    10 bps offset spread survives at ZERO cost.")
    P(f"    buckets: PATH {bc.get('PATH',0):.3f}  MIXED {bc.get('MIXED',0):.3f}  COST {bc.get('COST',0):.3f}")
    P(f"    exact split at 10 bps: |COST_d|/|PATH_d| median {r10.median():.4f}, "
      f"cost dominates in {(r10>1).mean():.4f} of offset pairs.")
    P(f"  CAPITAL: 4b d=0 passes at 10 bps = {int(B4[(B4['cost']==COST0)]['pass4b'].sum())} of "
      f"{len(B4[B4['cost']==COST0])}; rule-8 headline OOS 4b passes "
      f"{int(WF[WF['mode'].str.startswith('HEADLINE')]['pass4b_oos'].sum())} of "
      f"{len(WF[WF['mode'].str.startswith('HEADLINE')])}, 4a "
      f"{int(WF[WF['mode'].str.startswith('HEADLINE')]['pass4a_oos'].sum())}.")
    P(f"  GATES {sum(g[3] for g in GATES)}/{len(GATES)} PASS.  runtime {time.time()-t0:.0f}s")
    P("")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LINES) + "\n")
    pd.DataFrame(GATES, columns=["gate", "got", "bar", "pass"]).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    print(f"\nwrote {SLUG}.console.txt / .grid.csv.gz / .spreads.csv / .split.csv / .clause.csv / "
          f".walkforward.csv / .gates.csv")


if __name__ == "__main__":
    main()
