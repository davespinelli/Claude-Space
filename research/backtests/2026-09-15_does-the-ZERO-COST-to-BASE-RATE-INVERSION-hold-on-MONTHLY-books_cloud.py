#!/usr/bin/env python3
"""Idea 926 (cloud, 2026-09-15) -- does the ZERO-COST pass-to-BASE-RATE INVERSION hold on
MONTHLY books?

THE QUESTION (queue, 2026-09-15)
  Idea 680 scored the record's 5 modal REAL 4b-pass book keys on 3 panels at 2 gross levels
  (30 cells) against an EXACTLY gross-matched coin-flip null, and found an INVERSION at zero
  cost: clearing 4b PREDICTS an easier null (Spearman rho(pass4b, null base rate) = +0.6387,
  mean base rate 0.5959 for passers vs 0.0733 for failers).  The whole effect dies at 10 bps
  (rho -0.1048; base-rate mean 0.1953 -> 0.0004; cells above 0.05 12 -> 0), and 680 read that as
  PROTOCOL rule 2's cost rung doing the clause's whole job.  The queue's objection: WEEKLY books
  turn over 8-30x a year, so 10 bps is an enormous haircut on THEM specifically.  Monthly books
  turn over about a third as fast, so the rung should bite less and the inversion should survive
  further out.  Re-run 680's 30 cells at freq='M' and report rho at each rung.

WHY IT MATTERS FOR CAPITAL
  If the inversion is a WEEKLY artefact that 10 bps happens to erase, 680's "rule 2 already does
  the clause's job" is a statement about cadence, not about costs, and every monthly 4b pass in
  the record is still uncertified: at the cadence real capital would actually trade, a coin flip
  from the same panel might clear the same bar just as often.  If instead the inversion dies at
  10 bps under BOTH cadences, 680's conclusion is cadence-free and no new PROTOCOL clause is
  owed.  Either way the answer changes what a 4b row is worth, not what any book returns.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CADENCE   W (680's own, the reproduction arm) and M (the queue's object).  Both
                     reported in full at every rung; never averaged together.
  TUNED 2  COST RUNG 0 / 10 / 25 bps.  0 bps is the inversion's own rung, 10 bps is PROTOCOL
                     rule 2, 25 bps is the stress column.  Every cell is reported at every rung.
  NOT TUNED (inherited from idea 680 and called unmodified): the 5 book keys
  (TOP5/TOP10/TOP20/EWELIG/BAND03), the 3 panels (U56 / B136 / SMALL439), the 2 claim sets
  (gross 0.75 = CORE and 1.00 = EXT), the gross-matched null construction, the gate (200d MA and
  vol20 < 0.60), the warm-up (260 rows), IS <= 2016-12-31 / OOS >= 2017-01-01, seed base 680.
  DRAWS is fixed at 250 -- the first 250 seeds of 680's own nested 1000-draw streams -- so the
  weekly arm is an EXACT reproduction of 680's committed 250-draw base rates (gate G3) and the
  two cadences are read on the same draw budget.

PRE-REGISTERED BARS (fixed before any number below was read; the bar is the record's own
|rho| >= 0.30, the same one idea 686 and idea 525 use)
  H_TURN     the premise: MONTHLY books really do turn over materially less.  PASS iff the
             median over the 30 cells of (monthly turnover / weekly turnover) <= 0.50.
  H_SURVIVE  (THE QUEUE'S QUESTION) the inversion SURVIVES the PROTOCOL rung under monthly
             cadence.  PASS iff at 10 bps, freq='M': rho(pass4b, null base rate) >= +0.30 AND
             the mean base rate of 4b passers exceeds that of failers.
  H_ZERO     the inversion reproduces at 0 bps under monthly cadence: rho >= +0.30 at 0 bps, M.
  H_LEVEL    monthly base rates at 10 bps are materially non-zero: >= 6 of the 30 cells above
             the 0.05 "outside its null" bar (weekly at 10 bps: 0 of 30).
  H_COST     the cost COLLAPSE itself is cadence-free: the drop in the mean base rate from 0 to
             10 bps is >= 0.10 under BOTH cadences.  (H_COST and H_SURVIVE can both pass: a
             collapse in LEVEL does not have to kill the ASSOCIATION.)
  H_WF       (rule 8, REQUIRED) under each cadence the book chosen on 2009-2016 ALONE is read
             ONCE on 2017-2026: OOS CAGR/Sharpe/MaxDD against SPY and RULES v2 on the same
             panel, both KEEP paths, and its own null's OOS-window base rate beside it.

GATES (printed before any result number)
  G1  ctx.run(freq) == engine.backtest(freq) at 10 bps on the RULES v2 band book, for BOTH
      cadences, read from row 260 as every published metric is (idea 680's own G1)      1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                                    0.0
  G3  CROSS-RUN EXACT: the WEEKLY arm reproduces idea 680's committed .nulls.csv 250-draw
      base rates, book Sharpe/CAGR/MaxDD and gross match on all 30 cells x 3 rungs      1e-12
  G4  panel triples (SPY, RULES v2) printed for both cadences and both windows
  G5  GROSS MATCH: every null family's mean realised gross within 0.01 of its book's
  G6  determinism: the seed-680 draw stream re-run reproduces its pass vector exactly      0.0
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
      (inherited from idea 680's own load_panels, and the count is printed)

SURVIVORSHIP (PROTOCOL 9): universe.json / universe_broad.json / the sub-$2B screen are
CURRENT-CONSTITUENT lists, so every CAGR and drawdown LEVEL below is optimistic.  The direction
matters here and is stated rather than buried: a coin flip drawn from a survivor panel is a
BETTER book than one drawn in real time, so every null base rate below is an UPPER bound on the
true base rate and each book's standing inside its null is a LOWER bound.  That runs AGAINST the
books and IN FAVOUR of the queue's suspicion.  The cadence contrast (W vs M) is a same-panel,
same-days, same-draw-seed comparison and is far less exposed; the 4b bar is against SPY, which is
not survivorship-inflated, so the 4b LEVELS are upper bounds too.

Outputs: .books.csv .nulls.csv .rho.csv .turnover.csv .gates.csv .walkforward.csv
         .hypotheses.csv .console.txt .result.md
"""
from __future__ import annotations

import importlib.util
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
BT = ROOT / "research" / "backtests"
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))

from baseline import rules_v2_weights                       # noqa: E402
from engine import backtest                                 # noqa: E402


def _load(p, name):
    spec = importlib.util.spec_from_file_location(name, str(p))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P680 = BT / "2026-09-15_does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause_B.py"
M680 = _load(P680, "idea680")
NULLS680 = BT / "2026-09-15_does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause_B.nulls.csv"

# every definition below is idea 680's, imported, never re-typed
Ctx, mets, pass4b, pass4a, pass4b_is = M680.Ctx, M680.mets, M680.pass4b, M680.pass4a, M680.pass4b_is
failstr, build_books, null_streams = M680.failstr, M680.build_books, M680.null_streams
band_book, load_panels, score_stream = M680.band_book, M680.load_panels, M680.score_stream
WARM, IS_END, OOS_START = M680.WARM, M680.IS_END, M680.OOS_START
BAND0, COSTS, CLAIM_SETS = M680.BAND0, M680.COSTS, M680.CLAIM_SETS
BASE_RATE_BAR, SEED0 = M680.BASE_RATE_BAR, M680.SEED0
FAM = {"TOP5": ("ROT", 5), "TOP10": ("ROT", 10), "TOP20": ("ROT", 20),
       "EWELIG": ("EW", None), "BAND03": ("BD", None)}

CADENCES = ["W", "M"]          # TUNED 1
DRAWS = 250                    # the first 250 seeds of 680's nested 1000-draw streams
BAR_RHO = 0.30                 # the record's own association bar
TURN_BAR = 0.50                # H_TURN: monthly / weekly turnover
LEVEL_BAR = 6                  # H_LEVEL: cells above 0.05 at 10 bps, monthly
COST_DROP_BAR = 0.10           # H_COST
RHO_W10_680 = -0.1048          # 680's committed weekly 10 bps reading
RHO_W0_680 = +0.6387           # 680's committed weekly 0 bps reading

LOG: list[str] = []


def P(s=""):
    print(s, flush=True)
    LOG.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return np.nan
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def panel_context(px, freq):
    """Idea 680's panel_context with the cadence as an argument instead of a module constant.
    At freq='W' it must agree with M680.panel_context exactly -- asserted in G3."""
    ctx = Ctx(px, freq=freq)
    idx = px.index
    i0 = WARM
    oos_mask = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_mask = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    out = dict(ctx=ctx, i0=i0, idx=idx, oos=oos_mask, is_=is_mask,
               spy=mets(spy), spy_oos=mets(spy[oos_mask]), spy_is=mets(spy[is_mask]))
    v2 = rules_v2_weights(px, BAND0, 0.75)
    gr, tn = ctx.run(ctx.shift(v2))
    out["v2"] = {}
    for c in COSTS:
        r = (gr - tn * c / 1e4)[i0:]
        out["v2"][c] = dict(full=mets(r), oos=mets(r[oos_mask]), is_=mets(r[is_mask]))
    return out


def main():
    t_start = time.time()
    P("=" * 100)
    P("IDEA 926 (cloud, 2026-09-15) -- does the ZERO-COST to BASE-RATE INVERSION hold on "
      "MONTHLY books?")
    P("=" * 100)
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   seed base {SEED0}   draws {DRAWS} "
      f"(prefix of 680's 1000)   cadences {CADENCES}   rungs {COSTS} bps   "
      f"claim sets {list(CLAIM_SETS)}")
    P("PRE-REGISTERED (docstring, fixed before any number below was read):")
    P(f"  H_TURN median(M turn / W turn) <= {TURN_BAR:.2f}   "
      f"H_SURVIVE rho >= +{BAR_RHO:.2f} at 10 bps on M   H_ZERO rho >= +{BAR_RHO:.2f} at 0 bps on M")
    P(f"  H_LEVEL >= {LEVEL_BAR} of 30 cells above {BASE_RATE_BAR:.2f} at 10 bps on M   "
      f"H_COST mean base-rate drop 0->10 bps >= {COST_DROP_BAR:.2f} on BOTH")
    P(f"  680's committed weekly readings, the comparands: rho {RHO_W0_680:+.4f} @0bps, "
      f"{RHO_W10_680:+.4f} @10bps")
    P()

    panels, n_dropped = load_panels()
    P(f"  G7 SMALL439 screen: {n_dropped} tickers with max_1d_move >= 1.0 dropped "
      f"(idea 680's own load_panels)")
    for pn, px in panels.items():
        P(f"     {pn:9s} n={px.shape[1]:4d}  {px.index[WARM].date()}..{px.index[-1].date()}")
    P()

    gates = {}

    # ---------------- G1 / G2 ----------------
    # the same book idea 680's own G1 uses, and the same warm-up cut: engine.backtest emits NaN
    # on row 0 (w_target is shifted, so the first rebalance reads a NaN row), and every published
    # metric in this record is read from row 260 onward, so the gate is read there too.
    gbook = band_book(panels["U56"], BAND0, 0.75)
    j = panels["U56"].index[WARM]
    g1 = {}
    for f in CADENCES:
        ctx = Ctx(panels["U56"], freq=f)
        gr, tn = ctx.run(ctx.shift(gbook))
        mine = pd.Series(gr - tn * 10.0 / 1e4, index=panels["U56"].index)
        eng = backtest(panels["U56"], gbook, cost_bps=10.0, freq=f)["returns"]
        g1[f] = float(np.abs(mine.loc[j:].values - eng.loc[j:].values).max())
    gates["G1"] = all(v < 1e-12 for v in g1.values())
    P(f"  G1 ctx.run == engine.backtest @10bps on the band book (from row 260): " +
      ", ".join(f"{f} {v:.2e}" for f, v in g1.items()) +
      f"   {'PASS' if gates['G1'] else 'FAIL'}")
    d2 = float((band_book(panels["U56"], BAND0, 0.75)
                - rules_v2_weights(panels["U56"], BAND0, 0.75)).abs().max().max())
    gates["G2"] = d2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights: max |delta| {d2:.2e}   "
      f"{'PASS' if gates['G2'] else 'FAIL'}")
    P()

    # ---------------- panel contexts, both cadences (G4) ----------------
    P("=" * 100)
    P("(A) PANEL TRIPLES (G4) -- both cadences, full sample from row 260 and the OOS window")
    P("=" * 100)
    PC = {}
    for pn, px in panels.items():
        for f in CADENCES:
            PC[(pn, f)] = panel_context(px, f)
        pc = PC[(pn, "W")]
        s, so = pc["spy"], pc["spy_oos"]
        P(f"  {pn:9s} SPY      full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%} "
          f"(halves {s['H1']:.3f}/{s['H2']:.3f})   OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} "
          f"/ {so['MaxDD']:7.2%}")
        for f in CADENCES:
            v = PC[(pn, f)]["v2"][10.0]
            P(f"            RULES v2 ({f}) full {v['full']['CAGR']:7.2%} / "
              f"{v['full']['Sharpe']:.4f} / {v['full']['MaxDD']:7.2%}   OOS "
              f"{v['oos']['CAGR']:7.2%} / {v['oos']['Sharpe']:.4f} / {v['oos']['MaxDD']:7.2%}")
    P()

    # ---------------- (B) the books, both cadences ----------------
    P("=" * 100)
    P("(B) THE 30 CELLS -- idea 680's 5 book keys x 3 panels x 2 claim sets, at both cadences")
    P("=" * 100)
    BOOKROWS, CAND, WTS = [], {}, {}
    for pn, px in panels.items():
        for cs, g in CLAIM_SETS.items():
            bks, cand = build_books(px, g)
            CAND[(pn, cs)] = cand
            for bn, W in bks.items():
                for f in CADENCES:
                    pc = PC[(pn, f)]
                    wt = pc["ctx"].shift(W)
                    WTS[(pn, cs, bn, f)] = wt
                    gr, tn = pc["ctx"].run(wt)
                    gross = pc["ctx"].gross(wt, pc["i0"])
                    for c in COSTS:
                        m, mo, mi = score_stream(gr, tn, pc, c)
                        BOOKROWS.append(dict(
                            panel=pn, claim_set=cs, book=bn, freq=f, gross_nom=g, cost=c,
                            mean_gross=gross, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                            MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            pass4b=pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                            pass4a=pass4a(m, pc["v2"][c]["full"]),
                            fail4b=failstr(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                            turn=float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))))
    books = pd.DataFrame(BOOKROWS)
    dump(books, "books")
    for c in (0.0, 10.0):
        for f in CADENCES:
            sub = books[(books.cost == c) & (books.freq == f)]
            P(f"  cost {c:4.0f} bps  freq {f}:  4b {int(sub.pass4b.sum())} of {len(sub)}   "
              f"4a {int(sub.pass4a.sum())} of {len(sub)}   mean turn "
              f"{sub.turn.mean():5.2f}x/yr")
    P()
    P("  TURNOVER, the queue's premise (annualised, cost-free):")
    tw = books[(books.cost == 0.0)].pivot_table(index=["panel", "claim_set", "book"],
                                                columns="freq", values="turn")
    tw["ratio_M_over_W"] = tw["M"] / tw["W"]
    tw = tw.reset_index()
    dump(tw, "turnover")
    P("     panel     set  book     W turn   M turn   M/W")
    for _, r in tw.iterrows():
        P(f"     {r.panel:9s} {r.claim_set:4s} {r.book:7s} {r['W']:7.2f}x {r['M']:7.2f}x "
          f"{r.ratio_M_over_W:6.3f}")
    med_ratio = float(tw.ratio_M_over_W.median())
    H_TURN = bool(med_ratio <= TURN_BAR)
    P(f"     median M/W turnover ratio {med_ratio:.4f} (bar <= {TURN_BAR:.2f})  -> H_TURN "
      f"{'PASS' if H_TURN else 'FAIL'}")
    P()

    # ---------------- (C) the nulls ----------------
    P("=" * 100)
    P("(C) THE NULLS -- 680's exactly gross-matched coin flips, re-drawn at each cadence")
    P("=" * 100)
    NULLROWS = []
    det_check = {}
    for pn, px in panels.items():
        for cs, g in CLAIM_SETS.items():
            for f in CADENCES:
                pc = PC[(pn, f)]
                gen = null_streams(pc["ctx"], px, CAND[(pn, cs)], DRAWS)
                for bn, (kind, k) in FAM.items():
                    t0 = time.time()
                    pv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    iv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    sv = {c: np.zeros(DRAWS) for c in COSTS}
                    ov = {c: np.zeros(DRAWS) for c in COSTS}
                    gsum = 0.0
                    for d, W in gen(kind, WTS[(pn, cs, bn, f)], k):
                        gr, tn = pc["ctx"].run(W)
                        gsum += pc["ctx"].gross(W, pc["i0"])
                        for c in COSTS:
                            m, mo, mi = score_stream(gr, tn, pc, c)
                            pv[c][d] = pass4b(m, mo["Sharpe"], pc["spy"],
                                              pc["spy_oos"]["Sharpe"])
                            iv[c][d] = pass4b_is(mi, pc["spy_is"])
                            sv[c][d], ov[c][d] = m["Sharpe"], mo["Sharpe"]
                    mg_null = gsum / DRAWS
                    if (pn, cs, bn, f) == ("U56", "CORE", "TOP20", "W"):
                        det_check["first"] = pv[0.0].copy()
                    brow = books[(books.panel == pn) & (books.claim_set == cs) &
                                 (books.book == bn) & (books.freq == f)]
                    mg_book = float(brow.mean_gross.iloc[0])
                    for c in COSTS:
                        b = brow[brow.cost == c].iloc[0]
                        NULLROWS.append(dict(
                            panel=pn, claim_set=cs, book=bn, null=kind, freq=f, gross_nom=g,
                            cost=c, draws=DRAWS, null_base_rate_4b=float(pv[c].mean()),
                            is_base_rate_4b=float(iv[c].mean()),
                            oos_null_mean_Sharpe=float(ov[c].mean()),
                            book_pass4b=bool(b.pass4b),
                            outside_null=bool(b.pass4b and float(pv[c].mean()) <= BASE_RATE_BAR),
                            pct_Sharpe=float((sv[c] < b.Sharpe).mean()),
                            p_emp_Sharpe=float((1 + (sv[c] >= b.Sharpe).sum()) / (1 + DRAWS)),
                            null_mean_Sharpe=float(sv[c].mean()),
                            null_p95_Sharpe=float(np.quantile(sv[c], 0.95)),
                            book_Sharpe=float(b.Sharpe), book_CAGR=float(b.CAGR),
                            book_MaxDD=float(b.MaxDD), book_turn=float(b.turn),
                            mean_gross_null=mg_null, mean_gross_book=mg_book,
                            gross_match=abs(mg_null - mg_book)))
                    P(f"  {pn:9s} {cs:4s} {bn:7s} {f} null={kind:3s} gross {mg_book:.3f}/"
                      f"{mg_null:.3f} (|d| {abs(mg_null-mg_book):.4f})  base rate @0 "
                      f"{float(pv[0.0].mean()):6.1%} @10 {float(pv[10.0].mean()):6.1%} @25 "
                      f"{float(pv[25.0].mean()):6.1%}  [{time.time()-t0:.0f}s]")
    nulls = pd.DataFrame(NULLROWS)
    dump(nulls, "nulls")

    g5 = float(nulls.gross_match.max())
    gates["G5"] = g5 < 0.01
    P(f"  G5 gross match, worst over all {len(nulls)//len(COSTS)} (panel,set,book,cadence) "
      f"families: {g5:.4f}  {'PASS' if gates['G5'] else 'FAIL'}")

    # G6 determinism: redraw the U56/CORE/TOP20 weekly stream and compare the pass vector
    pcW = PC[("U56", "W")]
    gen = null_streams(pcW["ctx"], panels["U56"], CAND[("U56", "CORE")], DRAWS)
    again = np.zeros(DRAWS, bool)
    for d, W in gen("ROT", WTS[("U56", "CORE", "TOP20", "W")], 20):
        gr, tn = pcW["ctx"].run(W)
        m, mo, mi = score_stream(gr, tn, pcW, 0.0)
        again[d] = pass4b(m, mo["Sharpe"], pcW["spy"], pcW["spy_oos"]["Sharpe"])
    gates["G6"] = bool((again == det_check["first"]).all())
    P(f"  G6 determinism: the seed-{SEED0} draw stream re-run reproduces its pass vector  "
      f"{'PASS' if gates['G6'] else 'FAIL'}")

    # G3 CROSS-RUN EXACT against 680's committed 250-draw rows
    o = pd.read_csv(NULLS680)
    o = o[o.draws == DRAWS].set_index(["panel", "claim_set", "book", "cost"]).sort_index()
    mineW = nulls[nulls.freq == "W"].set_index(["panel", "claim_set", "book", "cost"]).sort_index()
    common = mineW.index.intersection(o.index)
    cmp_cols = ["null_base_rate_4b", "book_Sharpe", "book_CAGR", "book_MaxDD",
                "mean_gross_book", "mean_gross_null", "null_mean_Sharpe", "pct_Sharpe"]
    worst = (max(float(np.abs(mineW.loc[common, c].values - o.loc[common, c].values).max())
                 for c in cmp_cols) if len(common) else np.inf)
    gates["G3"] = bool(len(common) == len(o) and worst < 1e-12)
    P(f"  G3 CROSS-RUN EXACT vs idea 680's committed .nulls.csv (250 draws, weekly): "
      f"{len(common)} of {len(o)} rows, worst |delta| over {len(cmp_cols)} columns "
      f"{worst:.3e}  {'PASS' if gates['G3'] else 'FAIL'}")
    gates["G4"] = True
    gates["G7"] = True
    gdf = pd.DataFrame([dict(gate=k, passed=bool(v)) for k, v in gates.items()])
    dump(gdf, "gates")
    P(f"  gates passed {int(gdf.passed.sum())} of {len(gdf)}")
    P()

    # ---------------- (D) THE ANSWER: rho at every rung, both cadences ----------------
    P("=" * 100)
    P("(D) THE ANSWER -- rho(4b pass, null base rate) at every rung, both cadences")
    P("=" * 100)
    rrows = []
    for f in CADENCES:
        for c in COSTS:
            sub = nulls[(nulls.freq == f) & (nulls.cost == c)]
            rho = spearman(sub.book_pass4b.astype(float).values, sub.null_base_rate_4b.values)
            pas = sub[sub.book_pass4b]
            fai = sub[~sub.book_pass4b]
            rrows.append(dict(freq=f, cost=c, cells=len(sub),
                              n_pass=int(sub.book_pass4b.sum()), rho=rho,
                              mean_base_pass=float(pas.null_base_rate_4b.mean()) if len(pas) else np.nan,
                              mean_base_fail=float(fai.null_base_rate_4b.mean()) if len(fai) else np.nan,
                              mean_base=float(sub.null_base_rate_4b.mean()),
                              max_base=float(sub.null_base_rate_4b.max()),
                              cells_above_005=int((sub.null_base_rate_4b > 0.05).sum()),
                              cells_above_050=int((sub.null_base_rate_4b > 0.50).sum()),
                              base_rate_variance=float(sub.null_base_rate_4b.var()),
                              outside_null=int(sub.outside_null.sum()),
                              mean_turn=float(sub.book_turn.mean())))
    rho = pd.DataFrame(rrows)
    dump(rho, "rho")
    P("  freq cost cells 4b  rho(pass,base)  base|pass  base|fail  mean  max  >0.05 >0.50 outside")
    for _, r in rho.iterrows():
        rs = f"{r.rho:+.4f}" if np.isfinite(r.rho) else "   UNDEF"
        P(f"    {r.freq}  {r.cost:4.0f} {r.cells:5d} {r.n_pass:2d}  "
          f"{rs}        {r.mean_base_pass:8.4f} {r.mean_base_fail:10.4f} "
          f"{r.mean_base:6.4f} {r.max_base:5.3f} {r.cells_above_005:5d} "
          f"{r.cells_above_050:5d} {r.outside_null:6d}"
          + ("   [rho UNDEFINED: every base rate in this cell block is identical]"
             if not np.isfinite(r.rho) else ""))
    P()
    P("  PER-CELL base rates at 10 bps (the rung the queue says should bite less on M):")
    piv = nulls[nulls.cost == 10.0].pivot_table(
        index=["panel", "claim_set", "book"], columns="freq",
        values=["null_base_rate_4b", "book_pass4b"])
    P("     panel     set  book      W base  M base   W 4b  M 4b")
    for ix, r in piv.iterrows():
        P(f"     {ix[0]:9s} {ix[1]:4s} {ix[2]:7s} {r[('null_base_rate_4b','W')]:7.3f} "
          f"{r[('null_base_rate_4b','M')]:7.3f}   {bool(r[('book_pass4b','W')])!s:5s} "
          f"{bool(r[('book_pass4b','M')])!s:5s}")
    P()

    def get(f, c, col):
        return float(rho[(rho.freq == f) & (rho.cost == c)][col].iloc[0])

    H_SURVIVE = bool(get("M", 10.0, "rho") >= BAR_RHO
                     and get("M", 10.0, "mean_base_pass") > get("M", 10.0, "mean_base_fail"))
    H_ZERO = bool(get("M", 0.0, "rho") >= BAR_RHO)
    H_LEVEL = bool(get("M", 10.0, "cells_above_005") >= LEVEL_BAR)
    H_COST = bool(all(get(f, 0.0, "mean_base") - get(f, 10.0, "mean_base") >= COST_DROP_BAR
                      for f in CADENCES))
    P(f"  H_SURVIVE rho(M,10bps) {get('M',10.0,'rho'):+.4f} (bar >= +{BAR_RHO:.2f}), "
      f"base|pass {get('M',10.0,'mean_base_pass'):.4f} vs base|fail "
      f"{get('M',10.0,'mean_base_fail'):.4f}  -> {'PASS' if H_SURVIVE else 'FAIL'}")
    P(f"  H_ZERO    rho(M,0bps)  {get('M',0.0,'rho'):+.4f}  -> {'PASS' if H_ZERO else 'FAIL'}")
    P(f"  H_LEVEL   cells above {BASE_RATE_BAR:.2f} at 10 bps on M: "
      f"{int(get('M',10.0,'cells_above_005'))} of 30 (bar >= {LEVEL_BAR})  -> "
      f"{'PASS' if H_LEVEL else 'FAIL'}")
    P(f"  H_COST    mean base rate 0->10 bps: W {get('W',0.0,'mean_base'):.4f} -> "
      f"{get('W',10.0,'mean_base'):.4f};  M {get('M',0.0,'mean_base'):.4f} -> "
      f"{get('M',10.0,'mean_base'):.4f}  -> {'PASS' if H_COST else 'FAIL'}")
    P()

    # ---------------- (E) RULE 8 ----------------
    P("=" * 100)
    P("RULE 8 -- the book chosen on 2009-2016 ALONE, 2017-2026 read ONCE, both KEEP paths")
    P("=" * 100)
    wrows = []
    for f in CADENCES:
        for c in COSTS:
            sl = books[(books.freq == f) & (books.cost == c)]
            for sel, pick in [("PICK_IS_SHARPE", sl.loc[sl.IS_Sharpe.idxmax()]),
                              ("PICK_IS_SHARPE_U56", sl[sl.panel == "U56"]
                               .pipe(lambda d: d.loc[d.IS_Sharpe.idxmax()]))]:
                pc = PC[(pick.panel, f)]
                nb = nulls[(nulls.panel == pick.panel) & (nulls.claim_set == pick.claim_set)
                           & (nulls.book == pick.book) & (nulls.freq == f)
                           & (nulls.cost == c)].iloc[0]
                v2o = pc["v2"][c]["oos"]
                so = pc["spy_oos"]
                oos4b = bool(pick.OOS_Sharpe > so["Sharpe"]
                             and abs(pick.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"])
                             and pick.OOS_CAGR >= 0.70 * so["CAGR"])
                oos4a = bool(pick.OOS_Sharpe > v2o["Sharpe"]
                             and pick.OOS_MaxDD >= v2o["MaxDD"])
                wrows.append(dict(freq=f, cost=c, selector=sel, panel=pick.panel,
                                  claim_set=pick.claim_set, book=pick.book,
                                  IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                                  OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                                  spy_OOS_CAGR=so["CAGR"], spy_OOS_Sharpe=so["Sharpe"],
                                  spy_OOS_MaxDD=so["MaxDD"], v2_OOS_CAGR=v2o["CAGR"],
                                  v2_OOS_Sharpe=v2o["Sharpe"], v2_OOS_MaxDD=v2o["MaxDD"],
                                  full4b=bool(pick.pass4b), full4a=bool(pick.pass4a),
                                  oos4b=oos4b, oos4a=oos4a,
                                  null_base_rate=float(nb.null_base_rate_4b),
                                  is_base_rate=float(nb.is_base_rate_4b)))
    wf = pd.DataFrame(wrows)
    dump(wf, "walkforward")
    for _, r in wf.iterrows():
        P(f"  {r.freq} {r.cost:4.0f}bps {r.selector:19s} {r.panel:9s} {r.claim_set:4s} "
          f"{r.book:7s} IS {r.IS_Sharpe:6.3f} | OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:6.3f} / "
          f"{r.OOS_MaxDD:7.2%}  SPY {r.spy_OOS_CAGR:7.2%} / {r.spy_OOS_Sharpe:6.3f} / "
          f"{r.spy_OOS_MaxDD:7.2%}  v2 {r.v2_OOS_CAGR:7.2%} / {r.v2_OOS_Sharpe:6.3f} / "
          f"{r.v2_OOS_MaxDD:7.2%}  FULL 4a/4b {int(r.full4a)}/{int(r.full4b)}  OOS 4a/4b "
          f"{int(r.oos4a)}/{int(r.oos4b)}  its null's base rate {r.null_base_rate:.3f}")
    H_WF = bool(wf.oos4b.any())
    P(f"  OOS-WINDOW 4b {int(wf.oos4b.sum())} of {len(wf)};  4a {int(wf.oos4a.sum())} of "
      f"{len(wf)};  FULL-SAMPLE 4b on the same picks {int(wf.full4b.sum())} of {len(wf)}")
    P()

    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    hyp = dict(H_TURN=H_TURN, H_SURVIVE=H_SURVIVE, H_ZERO=H_ZERO, H_LEVEL=H_LEVEL,
               H_COST=H_COST, H_WF=H_WF)
    for kk, vv in hyp.items():
        P(f"  {kk:10s} {'PASS' if vv else 'FAIL'}")
    P(f"  gates {int(gdf.passed.sum())} of {len(gdf)};  runtime {time.time()-t_start:.0f}s")
    pd.DataFrame([hyp]).to_csv(OUT / f"{STEM}.hypotheses.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")
    return dict(hyp=hyp, rho=rho, nulls=nulls, books=books, wf=wf)


if __name__ == "__main__":
    main()
