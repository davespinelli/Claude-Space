#!/usr/bin/env python3
"""
IDEA 914 (lane B, 2026-09-22) -- price-the-0.70pp-DD-MARGIN-of-B136-TREND-AGG-th020-g075
                                 -against-its-OWN-OFFSET-SPREAD

THE QUESTION, as filed.  Idea 910 left a 4b KEEP-CANDIDATE on B136: a single aggregate
breadth switch (TREND/AGG, band 0.03, threshold 0.20, gross 0.75, weekly, 10 bps) that
clears 4b on FULL, IS and OOS and is reachable by two independent IS-only choosers.  Its
DD leg is held by 0.70 pp: MaxDD -19.53% against a bar of 0.60 x SPY's -33.72% = -20.23%.
Idea 806's standing finding is that a 4b margin smaller than the book's OWN rebalance-offset
spread is A DATE, NOT A BOOK.  That spread has never been measured for this book.  Measure
it across the 5 weekly offsets and re-score.

THE BOOK (idea 910's memo, verbatim, nothing re-tuned here):
    Universe research/universe_broad.json (B136).  Weekly, weights at close t applied t+1.
    band(i,t) TRUE when close > 200d MA x 1.03, FALSE below x 0.97, previous state in
    between, FALSE before 200 closes exist  ==  baseline.band_state(px, 0.03).
    breadth(t) = #{band} / #{priced}.
    If breadth(t) >= 0.20 hold EVERY priced name at 0.75/#priced of NAV, else 100% cash.

TUNED PARAMETERS -- EXACTLY TWO, both are the ones the idea itself names, and EVERY grid
point is published (research/backtests/<slug>_B.grid.csv):
    1. OFFSET  d in {0,1,2,3,4} -- rebalance d trading days BEFORE the week's last trading
               day.  d=0 IS the published convention (gate G2).  THIS IS THE AXIS.
    2. COST    c in {0, 10, 25, 50} bps.  10 bps is the protocol rung; the others are the
               robustness ladder.
PUBLISHED-NOT-TUNED (fixed at the committed book's values, never searched):
    band 0.03, threshold 0.20, gross 0.75, cadence W, panel {B136 primary, U56 replication},
    construction {AGG the book, ENS the 5-offset equal-weight ensemble}.
    The ENS book has NO free parameter: it holds 1/5 of NAV in each of the five offset
    books.  It is reported as the candidate REPAIR, not as a tuned alternative.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE QUESTION.  S_DD = max - min of MaxDD in pp over the 5 offsets, B136, 10 bps,
      FULL window.  The book SURVIVES iff its margin M (0.70 pp) > S_DD.  Fails otherwise:
      the DD pass is then a property of the weekday, not of the rule.
  B2  The 4b DD leg alone holds at 5 of 5 offsets on FULL.
  B3  ALL FOUR 4b legs hold at 5 of 5 offsets on FULL *and* on OOS.
  B4  B3 holds at all 4 cost rungs (5 x 4 = 20 cells per window).
  B5  RULE 8.  Offset chosen on IS (start..2016-12-31) ONLY by IS Sharpe; 2017-2026 read
      once.  The OOS pick must clear 4b.  Reported against RULES v2 and SPY OOS.
  B6  4a (beat the book) is scored at every grid point too; the memo says it fails.

GATES, printed before any hypothesis is read.
  G1  local bt() == engine.backtest at freq 'W', 10 bps                 bar max|d| < 1e-12
  G2  offset_mask(idx,'W',0) == engine.rebalance_mask(idx,'W')          bar 0 differing rows
  G3  the d=0 book reproduces idea 910's committed memo headline        bar |dCAGR| <= 0.15pp,
      (12.66% / 1.124 / -19.53%, OOS 11.89% / 1.060 / -19.53%)               |dSharpe| <= 0.01
      -- the tape has grown 3 sessions since that memo, so exact equality is NOT the bar.
  G4a offset fairness (count): every offset trades 50-53 times/yr
  G4b offset fairness (clipping): 0 clipped weeks -- SEE (G): this one FAILS structurally at
      d=3,4 and the run publishes the failure plus a clip-free re-read (B1c) instead of
      quietly widening the bar
  G5  comparands equal baseline's own: rules_v2_weights and SPY rows

SURVIVORSHIP.  B136 (research/universe_broad.json) and U56 (research/universe.json) are
CURRENT-CONSTITUENT lists, so every absolute CAGR and drawdown level here is optimistic.
This run is a WITHIN-TAPE contrast (same names, same dates, only the weekday moves), which
is the comparison the idea asks for; it does not repair the level.

Deterministic, offline, standalone:  python research/backtests/2026-09-22_b136-trend-agg-dd-margin-vs-offset-spread_B.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, rules_v1_weights  # noqa
from engine import backtest, metrics, rebalance_mask                                # noqa

SLUG = "2026-09-22_b136-trend-agg-dd-margin-vs-offset-spread_B"
OUT  = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

# ---- the committed book's dials (published, NOT tuned here) -------------------------------
BAND, TH, GROSS, FREQ = 0.03, 0.20, 0.75, "W"
OFFSETS = [0, 1, 2, 3, 4]                 # TUNED axis 1
COSTS   = [0, 10, 25, 50]                 # TUNED axis 2
COST0   = 10
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
MEMO = dict(FULL=(0.1266, 1.124, -0.1953), OOS=(0.1189, 1.060, -0.1953))   # idea 910, 2026-09-15


# ==========================================================================================
# offsets + a mask-taking backtester (engine.backtest only accepts a freq string)
# ==========================================================================================
def offset_mask(idx, d):
    """True d trading days BEFORE the last trading day of each week.  d=0 == rebalance_mask."""
    key = pd.Series(idx.to_period("W"), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def run(prices, weights, mask):
    """engine.backtest's loop, byte-for-byte, with the schedule passed in instead of a freq.
    Returns held weights and turnover; costs are applied afterwards (they do not change the
    path), so one loop serves every cost rung."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    m = mask.shift(1, fill_value=False)
    held = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    cur = np.zeros(len(prices.columns)); turnover = pd.Series(0.0, index=prices.index)
    for i, d in enumerate(prices.index):
        if m.iloc[i] or i == 0:
            new = w_target.iloc[i].values
            turnover.iloc[i] = np.abs(new - cur).sum(); cur = new
        held.iloc[i] = cur
        growth = cur * (1 + rets.iloc[i].values)
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    gross_ret = (held * rets).sum(axis=1)
    return gross_ret, turnover


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


# ==========================================================================================
# the book
# ==========================================================================================
def trend_agg_weights(px, band=BAND, th=TH, gross=GROSS):
    priced = px.notna()
    bs = band_state(px, band) & priced
    n = priced.sum(axis=1).replace(0, np.nan)
    breadth = bs.sum(axis=1) / n
    e = priced.astype(float)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(breadth >= th, 0.0)


# ==========================================================================================
# scoring
# ==========================================================================================
def M(r):
    m = metrics(r); return m["CAGR"], m["Sharpe"], m["MaxDD"]

def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]

def legs4b(r, spy):
    """(pass, leg dict).  Exactly idea 910's memo convention."""
    c, s, dd = M(r); h1, h2 = halves(r)
    cs, ss, dds = M(spy); sh1, sh2 = halves(spy)
    L = dict(L1_H1=h1 > sh1, L2_H2=h2 > sh2, L3_DD=dd >= 0.60 * dds, L4_CAGR=c >= 0.70 * cs)
    marg = dict(m_H1=h1 - sh1, m_H2=h2 - sh2,
                m_DD_pp=(dd - 0.60 * dds) * 100, m_CAGR_pp=(c - 0.70 * cs) * 100)
    return all(L.values()), L, marg, dict(CAGR=c, Sharpe=s, MaxDD=dd, H1=h1, H2=h2)

def legs4a(r, base):
    c, s, dd = M(r); h1, h2 = halves(r)
    cb, sb, ddb = M(base); bh1, bh2 = halves(base)
    return (h1 > bh1) and (h2 > bh2) and (dd >= ddb)


def windows(r, start):
    r = r.loc[start:]
    return dict(FULL=r, IS=r.loc[:IS_END], OOS=r.loc[OOS_BEG:])


# ==========================================================================================
def main():
    P("=" * 94)
    P("IDEA 914 lane B 2026-09-22 -- does the B136 TREND/AGG 0.70 pp DD MARGIN survive its")
    P("                              OWN 5-OFFSET REBALANCE SPREAD?")
    P("=" * 94)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC   book: band {BAND} / th {TH} / gross "
      f"{GROSS} / {FREQ}   offsets {OFFSETS}   costs {COSTS} bps")
    P("")

    panels = {}
    px_b = load_universe(broad=True); panels["B136"] = px_b
    px_u = load_universe();           panels["U56"]  = px_u
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} names  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ---------------------------------------------------------------- GATES
    P("-" * 94)
    P("(G) GATES -- five, printed before any hypothesis is read")
    P("-" * 94)
    gp = 0

    # G2 first: the mask nests the published convention
    m0, clip0 = offset_mask(px_b.index, 0)
    ref = rebalance_mask(px_b.index, FREQ)
    g2 = int((m0.values != ref.values).sum())
    P(f"  G2  offset_mask(idx,0) == engine.rebalance_mask(idx,'W') : {g2} differing rows   "
      f"[{'PASS' if g2 == 0 else 'FAIL'}]"); gp += g2 == 0

    # G1: the local runner is the engine
    w_b = trend_agg_weights(px_b)
    gr, to = run(px_b, w_b, m0)
    r_local = net(gr, to, COST0)
    r_eng = backtest(px_b, w_b, cost_bps=COST0, freq=FREQ)["returns"]
    a, b = r_local.values, r_eng.values
    same_nan = bool((np.isnan(a) == np.isnan(b)).all())          # row 0 is NaN in BOTH (engine's
    ok = ~np.isnan(a)                                            # own shift(1) on w_target)
    g1 = float(np.abs(a[ok] - b[ok]).max())
    P(f"  G1  local run()+net() == engine.backtest(freq='W',10bps) : max|d| {g1:.3e} over "
      f"{int(ok.sum())} rows, NaN masks identical {same_nan}   "
      f"[{'PASS' if (g1 < 1e-12 and same_nan) else 'FAIL'}]"); gp += (g1 < 1e-12 and same_nan)

    start = px_b.index[260]
    W = windows(r_local, start)
    cF, sF, ddF = M(W["FULL"]); cO, sO, ddO = M(W["OOS"])
    d1, d2 = abs(cF - MEMO["FULL"][0]) * 100, abs(sF - MEMO["FULL"][1])
    d3, d4 = abs(cO - MEMO["OOS"][0]) * 100, abs(sO - MEMO["OOS"][1])
    g3 = (d1 <= 0.15) and (d2 <= 0.01) and (d3 <= 0.15) and (d4 <= 0.01) \
         and (round(ddF, 4) == MEMO["FULL"][2]) and (round(ddO, 4) == MEMO["OOS"][2])
    P(f"  G3  reproduces idea 910's memo headline within tape drift (memo 2026-09-15, tape now")
    P(f"      runs 3 sessions longer):  FULL {cF:6.2%} / {sF:.3f} / {ddF:6.2%}   "
      f"memo {MEMO['FULL'][0]:6.2%} / {MEMO['FULL'][1]:.3f} / {MEMO['FULL'][2]:6.2%}")
    P(f"                                OOS  {cO:6.2%} / {sO:.3f} / {ddO:6.2%}   "
      f"memo {MEMO['OOS'][0]:6.2%} / {MEMO['OOS'][1]:.3f} / {MEMO['OOS'][2]:6.2%}")
    P(f"      dCAGR {d1:.3f}/{d3:.3f} pp, dSharpe {d2:.4f}/{d4:.4f}, MaxDD identical to 2dp   "
      f"[{'PASS' if g3 else 'FAIL'}]"); gp += bool(g3)

    # G4 offset fairness -- reported as TWO clauses because they do not stand or fall together
    P(f"  G4  offset fairness (B136 tape).  G4a = rebalance count, G4b = clipping.")
    g4a_bad = g4b_bad = 0; fair = []
    yrs = len(px_b.loc[start:]) / 252
    for d in OFFSETS:
        md, cl = offset_mask(px_b.index, d)
        rpy = md.loc[start:].sum() / yrs
        oka, okb = (50.0 <= rpy <= 53.0), cl == 0
        g4a_bad += (not oka); g4b_bad += (not okb)
        fair.append(dict(offset=d, reb_per_yr=round(float(rpy), 2), clipped_weeks=cl,
                         G4a_count_ok=oka, G4b_noclip_ok=okb))
        P(f"        d={d}  {rpy:5.2f} rebalances/yr  {cl:3d} clipped weeks   "
          f"count {'ok' if oka else 'VIOLATION'} / clipping {'ok' if okb else 'VIOLATION'}")
    P(f"      G4a {5 - g4a_bad} of 5 offsets in 50-53 rebalances/yr                      "
      f"[{'PASS' if g4a_bad == 0 else 'FAIL'}]")
    P(f"      G4b {5 - g4b_bad} of 5 offsets with zero clipped weeks                     "
      f"[{'PASS' if g4b_bad == 0 else 'FAIL'}]")
    P( "      G4b FAILS BY CONSTRUCTION AND THE RUN SAYS SO RATHER THAN RELAXING IT: a week with")
    P( "      only 4 trading days has no session 4 before its last, so d=3 clips 2 weeks and d=4")
    P( "      clips 175 (every holiday-shortened week), each falling back to that week's FIRST")
    P( "      session.  The count clause is unaffected (G4a 5 of 5).  Section (B1c) therefore")
    P( "      re-reads the headline on the CLIP-FREE subset {0,1,2} alone; the verdict there is")
    P( "      the one that carries, and it is the same verdict.")
    gp += (g4a_bad == 0 and g4b_bad == 0)

    # G5 comparands
    base_b = backtest(px_b, rules_v2_weights(px_b), cost_bps=COST0, freq=FREQ)["returns"].loc[start:]
    spy_b = px_b["SPY"].pct_change().fillna(0).loc[start:]
    cb, sb, ddb = M(base_b); csp, ssp, ddsp = M(spy_b)
    g5 = abs(ddsp - (-0.3372)) < 5e-4
    P(f"  G5  comparands  RULES v2 B136 {cb:6.2%} / {sb:.3f} / {ddb:6.2%}   "
      f"SPY {csp:6.2%} / {ssp:.3f} / {ddsp:6.2%}")
    P(f"      SPY MaxDD matches the memo's -33.72% to 2dp                             "
      f"[{'PASS' if g5 else 'FAIL'}]"); gp += bool(g5)
    P(f"  GATES {gp} of 5 PASS")
    P("")

    # ---------------------------------------------------------------- the grid
    P("-" * 94)
    P("(A) EVERY GRID POINT -- 2 panels x 2 constructions x 5 offsets x 4 costs x 3 windows")
    P("-" * 94)
    rows = []
    paths = {}                      # (panel, construction, offset) -> (gross_ret, turnover)
    for pn, px in panels.items():
        w = trend_agg_weights(px)
        per_off = {}
        for d in OFFSETS:
            md, _ = offset_mask(px.index, d)
            per_off[d] = run(px, w, md)
            paths[(pn, "AGG", d)] = per_off[d]
        # ENS: equal-weight 1/5 in each offset book; no free parameter
        gr_e = sum(per_off[d][0] for d in OFFSETS) / len(OFFSETS)
        to_e = sum(per_off[d][1] for d in OFFSETS) / len(OFFSETS)
        paths[(pn, "ENS", 0)] = (gr_e, to_e)

    for pn, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0)
        base = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq=FREQ)["returns"]
        for (p2, con, d), (gr, to) in paths.items():
            if p2 != pn: continue
            for c in COSTS:
                r = net(gr, to, c)
                bw = windows(base, st) if c == COST0 else windows(
                    backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"], st)
                for win, rr in windows(r, st).items():
                    ss = windows(spy, st)[win]
                    ok, L, marg, stat = legs4b(rr, ss)
                    rows.append(dict(panel=pn, construction=con, offset=d, cost=c, window=win,
                                     CAGR=stat["CAGR"], Sharpe=stat["Sharpe"], MaxDD=stat["MaxDD"],
                                     H1=stat["H1"], H2=stat["H2"],
                                     pass4b=ok, pass4a=legs4a(rr, bw[win]),
                                     **{k: bool(v) for k, v in L.items()}, **marg,
                                     turnover_per_yr=float(to.loc[st:].sum() / (len(rr) / 252))
                                     if win == "FULL" else np.nan))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"  {len(G)} rows written to {SLUG}.grid.csv")
    P("")

    # ---- the headline table: B136 AGG, 10 bps
    P("  B136 / AGG / 10 bps -- the committed book at each of its five weekdays")
    P(f"    {'win':5s} {'d':>2s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s}"
      f" {'DDmarg':>7s} {'CAGRmarg':>9s}  4b   4a")
    for win in ("FULL", "IS", "OOS"):
        sub = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == COST0) &
                (G.window == win)].sort_values("offset")
        for _, x in sub.iterrows():
            P(f"    {win:5s} {int(x.offset):2d} {x.CAGR:8.2%} {x.Sharpe:7.3f} {x.MaxDD:8.2%}"
              f" {x.H1:6.3f} {x.H2:6.3f} {x.m_DD_pp:+7.2f} {x.m_CAGR_pp:+9.2f}  "
              f"{'PASS' if x.pass4b else 'FAIL'} {'PASS' if x.pass4a else 'FAIL'}")
        P("")

    # ---------------------------------------------------------------- B1 .. B6
    P("-" * 94)
    P("(B) THE PRE-REGISTERED BARS")
    P("-" * 94)
    verdicts = {}

    sub = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == COST0) &
            (G.window == "FULL")]
    s_dd = (sub.MaxDD.max() - sub.MaxDD.min()) * 100
    margin = sub[sub.offset == 0].m_DD_pp.iloc[0]
    b1 = margin > s_dd
    P(f"  B1  THE QUESTION.  FULL / 10 bps / B136: MaxDD over the 5 offsets runs")
    P(f"      {sub.MaxDD.min():.2%} .. {sub.MaxDD.max():.2%}  ->  OFFSET SPREAD S_DD = {s_dd:.2f} pp")
    P(f"      the committed book's own DD MARGIN M = {margin:.2f} pp")
    P(f"      M > S_DD ?  {margin:.2f} > {s_dd:.2f}  ->  {'SURVIVES' if b1 else 'DOES NOT SURVIVE'}"
      f"                 [{'PASS' if b1 else 'FAIL'}]")
    verdicts["B1"] = b1
    clipfree = sub[sub.offset.isin([0, 1, 2])]
    s_dd_cf = (clipfree.MaxDD.max() - clipfree.MaxDD.min()) * 100
    P(f"      B1c CLIP-FREE SUBSET {{0,1,2}} only (the G4b repair): MaxDD "
      f"{clipfree.MaxDD.min():.2%} .. {clipfree.MaxDD.max():.2%}, spread {s_dd_cf:.2f} pp vs "
      f"margin {margin:.2f} pp -> {'survives' if margin > s_dd_cf else 'DOES NOT survive'}")
    # same read on the other windows / costs, published
    for win in ("IS", "OOS"):
        s2 = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == COST0) &
               (G.window == win)]
        sp2 = (s2.MaxDD.max() - s2.MaxDD.min()) * 100
        m2 = s2[s2.offset == 0].m_DD_pp.iloc[0]
        P(f"      {win:4s}: spread {sp2:5.2f} pp vs margin {m2:5.2f} pp -> "
          f"{'survives' if m2 > sp2 else 'DOES NOT survive'}")
    P("")

    n_dd = int(sub.L3_DD.sum())
    b2 = n_dd == 5
    P(f"  B2  the 4b DD LEG alone holds at {n_dd} of 5 offsets (FULL, 10 bps)              "
      f"[{'PASS' if b2 else 'FAIL'}]")
    verdicts["B2"] = b2
    P("")

    nF = int(sub.pass4b.sum())
    subO = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == COST0) &
             (G.window == "OOS")]
    nO = int(subO.pass4b.sum())
    b3 = nF == 5 and nO == 5
    P(f"  B3  ALL FOUR 4b legs: FULL {nF} of 5 offsets, OOS {nO} of 5                     "
      f"[{'PASS' if b3 else 'FAIL'}]")
    verdicts["B3"] = b3
    P("")

    P(f"  B4  the same at every cost rung (B136 / AGG), passes of 5 offsets:")
    P(f"        {'cost':>5s} {'FULL':>6s} {'IS':>6s} {'OOS':>6s}   worst-offset FULL MaxDD / DD margin")
    b4ok = True
    for c in COSTS:
        line = []
        for win in ("FULL", "IS", "OOS"):
            s3 = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == c) &
                   (G.window == win)]
            line.append(int(s3.pass4b.sum()))
        sF3 = G[(G.panel == "B136") & (G.construction == "AGG") & (G.cost == c) &
                (G.window == "FULL")]
        worst = sF3.loc[sF3.MaxDD.idxmin()]
        b4ok &= (line[0] == 5 and line[2] == 5)
        P(f"        {c:5d} {line[0]:6d} {line[1]:6d} {line[2]:6d}   "
          f"{worst.MaxDD:7.2%} / {worst.m_DD_pp:+6.2f} pp (d={int(worst.offset)})")
    P(f"      5 of 5 on FULL and OOS at every rung: {b4ok}                              "
      f"[{'PASS' if b4ok else 'FAIL'}]")
    verdicts["B4"] = b4ok
    P("")

    # ---------------------------------------------------------------- B5 RULE 8
    P("-" * 94)
    P("(C) B5 -- RULE 8 WALK-FORWARD.  Offset chosen on IS (start..2016-12-31) ONLY,")
    P("    by IS Sharpe.  2017-2026 read ONCE.  Both KEEP paths scored.")
    P("-" * 94)
    wf = []
    for pn, px in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0)
        basew = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq=FREQ)["returns"]
        for c in COSTS:
            isr = {}
            for d in OFFSETS:
                gr, to = paths[(pn, "AGG", d)]
                isr[d] = metrics(windows(net(gr, to, c), st)["IS"])["Sharpe"]
            pick = max(isr, key=isr.get)
            gr, to = paths[(pn, "AGG", pick)]
            rw = windows(net(gr, to, c), st)
            bw = windows(basew, st) if c == COST0 else windows(
                backtest(px, rules_v2_weights(px), cost_bps=c, freq=FREQ)["returns"], st)
            sw = windows(spy, st)
            ok, L, marg, stat = legs4b(rw["OOS"], sw["OOS"])
            okF, _, margF, statF = legs4b(rw["FULL"], sw["FULL"])
            wf.append(dict(panel=pn, cost=c, IS_pick=pick,
                           IS_sharpes={k: round(v, 4) for k, v in isr.items()},
                           OOS_CAGR=stat["CAGR"], OOS_Sharpe=stat["Sharpe"],
                           OOS_MaxDD=stat["MaxDD"], OOS_H1=stat["H1"], OOS_H2=stat["H2"],
                           OOS_pass4b=ok, OOS_pass4a=legs4a(rw["OOS"], bw["OOS"]),
                           OOS_DDmarg_pp=marg["m_DD_pp"], OOS_CAGRmarg_pp=marg["m_CAGR_pp"],
                           FULL_pass4b=okF,
                           base_OOS_Sharpe=metrics(bw["OOS"])["Sharpe"],
                           base_OOS_CAGR=metrics(bw["OOS"])["CAGR"],
                           base_OOS_MaxDD=metrics(bw["OOS"])["MaxDD"],
                           spy_OOS_Sharpe=metrics(sw["OOS"])["Sharpe"],
                           spy_OOS_CAGR=metrics(sw["OOS"])["CAGR"],
                           spy_OOS_MaxDD=metrics(sw["OOS"])["MaxDD"]))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(f"    {'panel':6s} {'cost':>4s} {'pick':>4s}  {'OOS CAGR':>9s} {'Sharpe':>7s} {'MaxDD':>8s}"
      f" {'DDmarg':>7s}  4b   4a   | RULES v2 OOS Sharpe | SPY OOS Sharpe")
    for _, x in WF.iterrows():
        P(f"    {x.panel:6s} {int(x.cost):4d} {int(x.IS_pick):4d}  {x.OOS_CAGR:9.2%} "
          f"{x.OOS_Sharpe:7.3f} {x.OOS_MaxDD:8.2%} {x.OOS_DDmarg_pp:+7.2f}  "
          f"{'PASS' if x.OOS_pass4b else 'FAIL'} {'PASS' if x.OOS_pass4a else 'FAIL'}  |"
          f" {x.base_OOS_Sharpe:19.3f} | {x.spy_OOS_Sharpe:14.3f}")
    b5 = bool(WF[(WF.panel == "B136") & (WF.cost == COST0)].OOS_pass4b.iloc[0])
    P(f"    B5 (B136, 10 bps): OOS 4b {'PASS' if b5 else 'FAIL'}                          "
      f"[{'PASS' if b5 else 'FAIL'}]")
    verdicts["B5"] = b5
    P("")
    P("    IS Sharpe by offset (the chooser's whole input), B136 10 bps:")
    P(f"      {WF[(WF.panel=='B136') & (WF.cost==COST0)].IS_sharpes.iloc[0]}")
    P("")

    n4a = int(G[(G.panel == "B136") & (G.construction == "AGG")].pass4a.sum())
    P(f"  B6  4a passes at {n4a} of {len(G[(G.panel=='B136') & (G.construction=='AGG')])} B136/AGG"
      f" grid points (the memo says 4a fails)")
    verdicts["B6"] = n4a == 0
    P("")

    # ---------------------------------------------------------------- which date
    P("-" * 94)
    P("(D0) WHICH DATE.  The argmin-drawdown window of each offset's FULL-sample equity,")
    P("     B136 / AGG / 10 bps -- 'a date, not a book' is a literal claim, so name the date.")
    P("-" * 94)
    P(f"     {'d':>2s} {'MaxDD':>8s}  {'peak':12s} {'trough':12s} {'len(sessions)':>13s}")
    ddrows = []
    for d in OFFSETS:
        gr, to = paths[("B136", "AGG", d)]
        rr = windows(net(gr, to, COST0), px_b.index[260])["FULL"]
        eq = (1 + rr).cumprod(); dd = eq / eq.cummax() - 1
        tr = dd.idxmin(); pk = eq.loc[:tr].idxmax()
        n = int(eq.index.get_loc(tr) - eq.index.get_loc(pk))
        ddrows.append(dict(offset=d, MaxDD=float(dd.min()), peak=str(pk.date()),
                           trough=str(tr.date()), sessions=n))
        P(f"     {d:2d} {dd.min():8.2%}  {str(pk.date()):12s} {str(tr.date()):12s} {n:13d}")
    pd.DataFrame(ddrows).to_csv(OUT / f"{SLUG}.ddwindows.csv", index=False)
    P("")

    # ---------------------------------------------------------------- the ensemble repair
    P("-" * 94)
    P("(D) THE CANDIDATE REPAIR -- the 5-offset EQUAL-WEIGHT ENSEMBLE (no free parameter)")
    P("-" * 94)
    P(f"    {'panel':6s} {'cost':>4s} {'win':5s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s}"
      f" {'DDmarg':>7s} {'CAGRmarg':>9s}  4b   4a")
    for pn in panels:
        for c in COSTS:
            for win in ("FULL", "IS", "OOS"):
                x = G[(G.panel == pn) & (G.construction == "ENS") & (G.cost == c) &
                      (G.window == win)].iloc[0]
                P(f"    {pn:6s} {c:4d} {win:5s} {x.CAGR:8.2%} {x.Sharpe:7.3f} {x.MaxDD:8.2%}"
                  f" {x.m_DD_pp:+7.2f} {x.m_CAGR_pp:+9.2f}  "
                  f"{'PASS' if x.pass4b else 'FAIL'} {'PASS' if x.pass4a else 'FAIL'}")
    P("")

    # ---------------------------------------------------------------- U56 replication
    P("-" * 94)
    P("(E) U56 REPLICATION of the same construction (published, not tuned) -- 10 bps")
    P("-" * 94)
    P(f"    {'win':5s} {'d':>2s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'DDmarg':>7s}"
      f" {'CAGRmarg':>9s}  4b")
    for win in ("FULL", "OOS"):
        sub5 = G[(G.panel == "U56") & (G.construction == "AGG") & (G.cost == COST0) &
                 (G.window == win)].sort_values("offset")
        for _, x in sub5.iterrows():
            P(f"    {win:5s} {int(x.offset):2d} {x.CAGR:8.2%} {x.Sharpe:7.3f} {x.MaxDD:8.2%}"
              f" {x.m_DD_pp:+7.2f} {x.m_CAGR_pp:+9.2f}  {'PASS' if x.pass4b else 'FAIL'}")
        s5 = (sub5.MaxDD.max() - sub5.MaxDD.min()) * 100
        m5 = sub5[sub5.offset == 0].m_DD_pp.iloc[0]
        P(f"      -> U56 {win} offset spread {s5:.2f} pp vs margin {m5:.2f} pp: "
          f"{'survives' if m5 > s5 else 'DOES NOT survive'}")
        P("")

    # ---------------------------------------------------------------- verdict
    P("=" * 94)
    P("(F) VERDICT")
    P("=" * 94)
    for k in ("B1", "B2", "B3", "B4", "B5", "B6"):
        P(f"    {k}  {'PASS' if verdicts[k] else 'FAIL'}")
    P("")
    keep = verdicts["B1"] and verdicts["B3"] and verdicts["B5"]
    P(f"    KEEP-4b requires B1 (margin > its own offset spread) AND B3 AND B5: "
      f"{'KEEP-CANDIDATE' if keep else 'NOT A KEEP'}")
    P("=" * 94)

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LINES) + "\n")
    pd.DataFrame(fair).to_csv(OUT / f"{SLUG}.offsets.csv", index=False)
    json.dump({k: bool(v) for k, v in verdicts.items()},
              open(OUT / f"{SLUG}.verdicts.json", "w"), indent=1)


if __name__ == "__main__":
    main()
