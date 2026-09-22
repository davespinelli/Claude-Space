#!/usr/bin/env python3
"""
IDEA 2111 (lane cloud, run 4, 2026-09-22) --
    does-the-OFFSET-SPREAD-CLAUSE-KILL-the-LIVE-RULES-v2-BOOK-ITSELF

THE QUESTION, as filed.  Idea 914 (2026-09-22 lane B) earned a rule-4b clause -- *a DD or
CAGR margin must exceed the book's own rebalance-offset spread; a margin inside that spread
is not a pass* -- on a CANDIDATE, and 2119 generalised it over a 25-cell ladder.  Neither
turned it on the book that is ACTUALLY LIVE.  This run does exactly that, and in BOTH
directions, because the clause is symmetric and the record has only ever read the PASS side:

    a PASS whose margin is inside its own offset spread is not a pass;
    a FAIL whose margin is inside its own offset spread is not a FAIL EITHER.

RULES v2 is known (2026-09-22 CHANGELOG) to fail 4b on the CAGR floor alone while its DD
margin is ~4.5x outside the weekday noise.  If that CAGR failure margin is itself INSIDE the
live book's own CAGR offset spread, then the record's standing reading of the live book --
"4b FAIL on the CAGR leg" -- is a weekday, not a rule, and the clause cuts the incumbent
before it cuts any candidate.

THE BOOK -- the LIVE one, unmodified:
    baseline.rules_v2_weights(px, band=0.03, gross=0.75).  Hold every priced name inside the
    200d +/-3% hysteresis band at 0.75/N of NAV; gated-out weight goes to CASH (de-gross,
    never re-spread).  Weekly, weights decided at close t applied at t+1, long only, no
    leverage.  Gate G3 proves the object priced here is bit-identical to baseline's.

TUNED PARAMETERS -- EXACTLY TWO, as the idea line specifies, and EVERY grid point published:
    1. OFFSET d in {0,1,2,3,4} trading days before each week's last session.
    2. COST   c in {0, 10, 25, 50} bps per unit turnover (PROTOCOL rung is 10).
NOT TUNED, declared before any number was read:
    PANEL  {U56 = research/universe.json, B136 = research/universe_broad.json,
            SMALL = data/prices_small, sub-$2B, max_1d_move < 1.0 dropped}.
    WINDOWS FULL / IS (..2016-12-31) / OOS (2017-01-01..), rule 8.
    The REPORTED book is ALWAYS d=0, the published convention (gate G2).  d=1..4 exist only
    to build the spread the margins are judged against.  No verdict below is read off d>0.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE PASS SIDE.  For each 4b leg (H1, H2, DD, CAGR) of the live book at d=0, is
      |margin| > S, the leg's own max-minus-min spread over the 5 offsets, in the leg's unit?
      Reported per panel per window per cost rung.  A leg with |M| <= S is UNRESOLVED.
  B2  THE FAIL SIDE (the symmetric half the record has never read).  Same test on the legs
      the live book FAILS.  An unresolved FAIL is not a fail.
  B3  VERDICT STABILITY.  Is the 4b verdict (and the 4a verdict) identical at 5 of 5 offsets?
      B1/B2 and B3 are different tests and are reported separately.
  B4  THE COST AXIS.  B1-B3 re-read at 0 / 25 / 50 bps.  Does the clause's bite move with
      cost?  (2115 established the spread is a PATH artefact, so the prediction is NO.)
  B5  RULE 8.  (d, c) chosen on the IS window ONLY by IS Sharpe; 2017-2026 read ONCE.
      Report OOS CAGR / Sharpe / MaxDD against RULES v2 (d=0, 10 bps) and SPY, BOTH KEEP
      paths, and whether the picked cell's OOS margins clear its own OOS offset spread.
      This arm also MEASURES the selection width on a dial nobody is allowed to choose.
  B6  PATH 4a at every grid point, scored against the live d=0 10 bps book.
  B7  CONTROL.  SPY is buy-and-hold, so its legs do not move with d; the 4b bars are
      constant across offsets by construction and every spread reported is the BOOK's.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)   bar max|d| < 1e-12
  G2  offset_mask(idx,0) == engine.rebalance_mask(idx,'W')     bar 0 differing rows
  G3  the weights priced == baseline.rules_v2_weights          bar max|d| == 0
  G4a offset fairness (count): every offset trades 50-53 times/yr
  G4b offset fairness (clipping): weeks too short to carry offset d.  Known to FAIL
      structurally at d=3,4 (short holiday weeks) -- published, and B1/B2 are re-read on the
      clip-free offsets {0,1,2} as the 3-OFFSET variant rather than widening the bar quietly.
  G5  comparands are baseline's own: rules_v2_weights and SPY buy-and-hold.
  G6  SMALL panel hygiene: every ticker with max_1d_move >= 1.0 in data/small_meta.csv is
      dropped before any pricing.

SURVIVORSHIP (PROTOCOL rule 9).  U56, B136 and SMALL are CURRENT-CONSTITUENT lists, so every
absolute CAGR and drawdown level here is optimistic.  This run is a WITHIN-TAPE contrast --
same names, same dates, only the weekday of the rebalance moves -- which is what the idea
asks for; it does not repair the level.

offset_mask / run / net are lane B's (2026-09-22_4b-margin-vs-own-offset-spread-...) so the
two runs' spreads are measured by the same instrument.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_offset-spread-clause-on-the-live-book_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights      # noqa
from engine import backtest, metrics, rebalance_mask                        # noqa

SLUG = "2026-09-22_offset-spread-clause-on-the-live-book_cloud"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

OFFSETS = [0, 1, 2, 3, 4]        # TUNED axis 1 (reported book is always d=0)
COSTS   = [0, 10, 25, 50]        # TUNED axis 2
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
LIVE_BAND, LIVE_GROSS = 0.03, 0.75
CLIPFREE = [0, 1, 2]


# ---------------------------------------------------------------- offsets + backtester
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
    """engine.backtest's loop in numpy, semantics byte-for-byte (gate G1).  Costs are applied
    afterwards -- they never change the held path -- so one loop serves every cost rung."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
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
    return (pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


# ---------------------------------------------------------------- scoring
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    """PROTOCOL 4b against SPY on the SAME window.  Margins signed, positive == pass, in the
    leg's own unit (Sharpe points for H1/H2, pp for DD and CAGR)."""
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= 0.60 * ss["MaxDD"], CAGR=s["CAGR"] >= 0.70 * ss["CAGR"])
    M = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
             DD=(s["MaxDD"] - 0.60 * ss["MaxDD"]) * 100,
             CAGR=(s["CAGR"] - 0.70 * ss["CAGR"]) * 100)
    return all(L.values()), L, M


def legs4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


LEGUNIT = dict(H1=("H1", 1.0), H2=("H2", 1.0), DD=("MaxDD", 100.0), CAGR=("CAGR", 100.0))
WINS = ["FULL", "IS", "OOS"]


def windows(r, start):
    r = r.loc[start:]
    return dict(FULL=r, IS=r.loc[:IS_END], OOS=r.loc[OOS_BEG:])


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad), len([c for c in px.columns if c != "SPY"])


# ==========================================================================================
def main():
    P("=" * 100)
    P("IDEA 2111  lane cloud run 4  2026-09-22 -- DOES THE OFFSET-SPREAD CLAUSE KILL THE")
    P("                                           LIVE RULES v2 BOOK ITSELF?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"book: LIVE RULES v2, band {LIVE_BAND}, gross {LIVE_GROSS}, weekly, t+1, long only")
    P(f"tuned: OFFSET d {OFFSETS} x COST c {COSTS} bps  ({len(OFFSETS)*len(COSTS)} cells/panel)")
    P(f"not tuned: panels U56 / B136 / SMALL, windows FULL / IS..{IS_END} / OOS {OOS_BEG}..")
    P("reported book is ALWAYS d=0; d>0 measures the spread only.")
    P("")

    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm, n_drop, n_tot = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P(f"  SMALL hygiene (G6): dropped {n_drop} of {n_tot} names with max_1d_move >= 1.0")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("(G) GATES -- printed before any hypothesis is read")
    P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]

    m0, _ = offset_mask(px_u.index, 0)
    g2 = int((m0.values != rebalance_mask(px_u.index, FREQ).values).sum())
    ok = g2 == 0; gp += ok; gn += 1
    P(f"  G2  offset_mask(idx,0) == engine.rebalance_mask(idx,'W') : {g2} differing rows"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G2", value=g2, bar="0 differing rows", passed=bool(ok)))

    w_live = rules_v2_weights(px_u, band=LIVE_BAND, gross=LIVE_GROSS)
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  weights priced == baseline.rules_v2_weights defaults : max|d| {g3:.3e}"
      f"   [{'PASS' if ok else 'FAIL'}]  (this IS the live book)")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))

    gr, to = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b)
    g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}"
      f" over {int(fin.sum())} rows   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))

    yrs = len(px_u) / 252
    cnt, clip = {}, {}
    for d in OFFSETS:
        md, cd = offset_mask(px_u.index, d)
        cnt[d] = md.sum() / yrs; clip[d] = cd
    ok = all(50 <= cnt[d] <= 53 for d in OFFSETS); gp += ok; gn += 1
    P("  G4a offset fairness (trades/yr): " + "  ".join(f"d{d}={cnt[d]:.1f}" for d in OFFSETS)
      + f"   bar 50-53   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4a", value=float(min(cnt.values())), bar="50-53/yr", passed=bool(ok)))
    okc = all(v == 0 for v in clip.values()); gp += okc; gn += 1
    P("  G4b offset fairness (clipped weeks): " + "  ".join(f"d{d}={clip[d]}" for d in OFFSETS)
      + f"   bar 0   [{'PASS' if okc else 'FAIL - STRUCTURAL, 3-offset variant published'}]")
    gate_rows.append(dict(gate="G4b", value=int(max(clip.values())), bar="0 clipped", passed=bool(okc)))
    P("  G5  comparands: baseline.rules_v2_weights (d=0, 10 bps) and SPY buy-and-hold  [PASS by construction]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True))
    ok = n_drop > 0; gp += ok; gn += 1
    P(f"  G6  SMALL max_1d_move filter applied: {n_drop} dropped   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G6", value=n_drop, bar=">0 dropped", passed=bool(ok)))
    P(f"  --> {gp} of {gn} gates PASS.  G4b's structural failure is published, not patched.")
    P("")

    # ------------------------------------------------------------------ the grid
    rows = []
    paths = {}                       # (panel, d, c, win) -> stats
    spy_s = {}                       # (panel, win) -> SPY stats
    for pname, px in panels.items():
        w = rules_v2_weights(px, band=LIVE_BAND, gross=LIVE_GROSS)
        w1 = rules_v1_weights(px)
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        for wn, rr in windows(spy, spy.index[0]).items():
            spy_s[(pname, wn)] = stats(rr)
        # RULES v1 continuity row, d=0 only
        g1r, t1r = run(px, w1, offset_mask(px.index, 0)[0])
        for wn, rr in windows(net(g1r, t1r, COST0), start).items():
            s = stats(rr)
            rows.append(dict(panel=pname, book="RULES v1", d=0, cost=COST0, win=wn, **s))
        for d in OFFSETS:
            md, _ = offset_mask(px.index, d)
            gd, td = run(px, w, md)
            for c in COSTS:
                r = net(gd, td, c)
                for wn, rr in windows(r, start).items():
                    s = stats(rr)
                    paths[(pname, d, c, wn)] = s
                    p4b, L, M = legs4b(s, spy_s[(pname, wn)])
                    rows.append(dict(panel=pname, book="RULES v2", d=d, cost=c, win=wn,
                                     turnover_yr=td.loc[start:].sum() / (len(rr) / 252) if False else np.nan,
                                     **s,
                                     pass4b=p4b,
                                     **{f"leg_{k}": v for k, v in L.items()},
                                     **{f"mrg_{k}": v for k, v in M.items()}))
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"(0) GRID: {len(grid)} rows published to {SLUG}.grid.csv "
      f"({len(panels)} panels x {len(OFFSETS)} offsets x {len(COSTS)} costs x {len(WINS)} windows"
      f" + a RULES v1 continuity row per panel/window)")
    P("")

    # ------------------------------------------------------------------ the live book, d=0
    P("-" * 100)
    P("(A) THE LIVE BOOK AT THE PUBLISHED CONVENTION (d=0, 10 bps) vs SPY and RULES v1")
    P("-" * 100)
    P(f"{'panel':6s} {'win':5s} | {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s}"
      f" | {'SPY CAGR':>9s} {'SPY Sh':>7s} {'SPY DD':>8s} | 4b")
    for pname in panels:
        for wn in WINS:
            s = paths[(pname, 0, COST0, wn)]; ss = spy_s[(pname, wn)]
            p4b, L, M = legs4b(s, ss)
            fails = ",".join(k for k, v in L.items() if not v) or "-"
            P(f"{pname:6s} {wn:5s} | {s['CAGR']:8.2%} {s['Sharpe']:7.4f} {s['MaxDD']:8.2%}"
              f" {s['H1']:6.3f} {s['H2']:6.3f} | {ss['CAGR']:9.2%} {ss['Sharpe']:7.4f}"
              f" {ss['MaxDD']:8.2%} | {'PASS' if p4b else 'FAIL on ' + fails}")
    P("")

    # ------------------------------------------------------------------ B1/B2 the clause
    P("-" * 100)
    P("(B) B1 + B2 -- EVERY 4b LEG'S MARGIN AGAINST ITS OWN 5-OFFSET SPREAD (the clause,")
    P("               read on BOTH sides: an unresolved PASS is not a pass, an unresolved")
    P("               FAIL is not a fail)")
    P("-" * 100)
    clause = []
    for pname in panels:
        for c in COSTS:
            for wn in WINS:
                ss = spy_s[(pname, wn)]
                s0 = paths[(pname, 0, c, wn)]
                _, L0, M0 = legs4b(s0, ss)
                for leg in ["H1", "H2", "DD", "CAGR"]:
                    stat, scale = LEGUNIT[leg]
                    vals = [paths[(pname, d, c, wn)][stat] * scale for d in OFFSETS]
                    vals3 = [paths[(pname, d, c, wn)][stat] * scale for d in CLIPFREE]
                    S = max(vals) - min(vals); S3 = max(vals3) - min(vals3)
                    clause.append(dict(panel=pname, cost=c, win=wn, leg=leg,
                                       side="PASS" if L0[leg] else "FAIL",
                                       margin=M0[leg], spread5=S, spread3=S3,
                                       resolved5=abs(M0[leg]) > S,
                                       resolved3=abs(M0[leg]) > S3,
                                       ratio=abs(M0[leg]) / S if S > 0 else np.inf))
    cl = pd.DataFrame(clause)
    cl.to_csv(OUT / f"{SLUG}.clause.csv", index=False)

    P(f"{'panel':6s} {'win':5s} {'leg':5s} | {'side':4s} {'margin':>9s} {'spread5':>9s}"
      f" {'|M|/S':>7s} {'res5':>5s} | {'spread3':>9s} {'res3':>5s}   (10 bps)")
    sub = cl[cl.cost == COST0]
    for _, r in sub.iterrows():
        P(f"{r.panel:6s} {r.win:5s} {r.leg:5s} | {r.side:4s} {r.margin:9.4f} {r.spread5:9.4f}"
          f" {r.ratio:7.2f} {'YES' if r.resolved5 else 'no':>5s} | {r.spread3:9.4f}"
          f" {'YES' if r.resolved3 else 'no':>5s}")
    P("")
    for c in COSTS:
        s = cl[cl.cost == c]
        sp, sf = s[s.side == "PASS"], s[s.side == "FAIL"]
        P(f"  {c:2d} bps | PASS legs {len(sp):3d}, resolved {int(sp.resolved5.sum()):3d}"
          f" ({sp.resolved5.mean() if len(sp) else float('nan'):.3f})"
          f" | FAIL legs {len(sf):3d}, resolved {int(sf.resolved5.sum()):3d}"
          f" ({sf.resolved5.mean() if len(sf) else float('nan'):.3f})"
          f" | ALL {len(s):3d}, resolved {s.resolved5.mean():.3f}")
    P("")

    # ------------------------------------------------------------------ B3 verdict stability
    P("-" * 100)
    P("(C) B3 -- VERDICT STABILITY ACROSS THE 5 OFFSETS (4b and 4a)")
    P("-" * 100)
    vrows = []
    for pname in panels:
        base0 = paths[(pname, 0, COST0, "FULL")]     # 4a anchor is the live d=0 10 bps book
        for c in COSTS:
            for wn in WINS:
                ss = spy_s[(pname, wn)]
                anch = paths[(pname, 0, COST0, wn)]
                v4b = [legs4b(paths[(pname, d, c, wn)], ss)[0] for d in OFFSETS]
                v4a = [legs4a(paths[(pname, d, c, wn)], anch) for d in OFFSETS]
                vrows.append(dict(panel=pname, cost=c, win=wn,
                                  pass4b_d0=v4b[0], n4b=int(sum(v4b)), stable4b=len(set(v4b)) == 1,
                                  pass4a_d0=v4a[0], n4a=int(sum(v4a)), stable4a=len(set(v4a)) == 1))
    vd = pd.DataFrame(vrows)
    vd.to_csv(OUT / f"{SLUG}.verdicts.csv", index=False)
    P(f"{'panel':6s} {'cost':>4s} {'win':5s} | 4b at d=0  n/5  stable | 4a at d=0  n/5  stable")
    for _, r in vd.iterrows():
        P(f"{r.panel:6s} {r.cost:4d} {r.win:5s} | {str(r.pass4b_d0):>9s} {r.n4b:4d}"
          f" {str(r.stable4b):>7s} | {str(r.pass4a_d0):>9s} {r.n4a:4d} {str(r.stable4a):>7s}")
    P(f"  4b verdict identical at 5 of 5 offsets: {int(vd.stable4b.sum())} of {len(vd)} cells")
    P(f"  4a verdict identical at 5 of 5 offsets: {int(vd.stable4a.sum())} of {len(vd)} cells")
    P("")

    # ------------------------------------------------------------------ B4 cost axis
    P("-" * 100)
    P("(D) B4 -- DOES THE CLAUSE'S BITE MOVE WITH COST?  (2115 says the spread is a PATH")
    P("           artefact, so the prediction is NO)")
    P("-" * 100)
    piv = cl.pivot_table(index=["panel", "win", "leg"], columns="cost", values="spread5")
    P(piv.to_string(float_format=lambda x: f"{x:.4f}"))
    P("")
    for leg in ["H1", "H2", "DD", "CAGR"]:
        s = cl[cl.leg == leg]
        w = s.pivot_table(index=["panel", "win"], columns="cost", values="spread5")
        rel = (w[50] / w[0].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan)
        P(f"  leg {leg:5s} spread(50bps)/spread(0bps): median {rel.median():.4f}"
          f"  min {rel.min():.4f}  max {rel.max():.4f}")
    P("")

    # ------------------------------------------------------------------ B5 rule 8
    P("-" * 100)
    P("(E) B5 -- RULE 8 WALK-FORWARD.  (d, c) chosen on IS ONLY by IS Sharpe; 2017-2026 read ONCE.")
    P("-" * 100)
    wf = []
    for pname in panels:
        arms = (("both dials", [(d, c) for d in OFFSETS for c in COSTS]),
                ("offset only @10bps", [(d, COST0) for d in OFFSETS]))
        for arm, cand in arms:
            d_, c_ = max(cand, key=lambda k: paths[(pname, k[0], k[1], "IS")]["Sharpe"])
            sO = paths[(pname, d_, c_, "OOS")]; ssO = spy_s[(pname, "OOS")]
            bO = paths[(pname, 0, COST0, "OOS")]
            p4b, L, M = legs4b(sO, ssO)
            p4a = legs4a(sO, bO)
            # do the pick's OOS margins clear its own OOS offset spread (at its own cost rung)?
            resolved = {}
            for leg in ["H1", "H2", "DD", "CAGR"]:
                stat, scale = LEGUNIT[leg]
                vals = [paths[(pname, d, c_, "OOS")][stat] * scale for d in OFFSETS]
                resolved[leg] = abs(M[leg]) > (max(vals) - min(vals))
            oosS = [paths[(pname, d, c_, "OOS")]["Sharpe"] for d in OFFSETS]
            wf.append(dict(panel=pname, arm=arm, pick_d=d_, pick_cost=c_,
                           IS_Sharpe=paths[(pname, d_, c_, "IS")]["Sharpe"],
                           OOS_CAGR=sO["CAGR"], OOS_Sharpe=sO["Sharpe"], OOS_MaxDD=sO["MaxDD"],
                           base_CAGR=bO["CAGR"], base_Sharpe=bO["Sharpe"], base_MaxDD=bO["MaxDD"],
                           spy_CAGR=ssO["CAGR"], spy_Sharpe=ssO["Sharpe"], spy_MaxDD=ssO["MaxDD"],
                           pass4b=p4b, pass4a=p4a,
                           fails=",".join(k for k, v in L.items() if not v) or "-",
                           all_legs_resolved=all(resolved.values()),
                           unresolved=",".join(k for k, v in resolved.items() if not v) or "-",
                           offset_Sharpe_width=max(oosS) - min(oosS)))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    for _, r in wfd.iterrows():
        P(f"  {r.panel:6s} [{r.arm:18s}] IS pick d={r.pick_d} c={r.pick_cost} bps (IS Sharpe {r.IS_Sharpe:.4f})")
        P(f"         OOS book     {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:8.4f} {r.OOS_MaxDD:8.2%}")
        P(f"         OOS RULES v2 {r.base_CAGR:8.2%} {r.base_Sharpe:8.4f} {r.base_MaxDD:8.2%}   (d=0, 10 bps)")
        P(f"         OOS SPY      {r.spy_CAGR:8.2%} {r.spy_Sharpe:8.4f} {r.spy_MaxDD:8.2%}")
        P(f"         4b {'PASS' if r.pass4b else 'FAIL on ' + r.fails}   4a {'PASS' if r.pass4a else 'FAIL'}"
          f"   all legs resolved vs own offset spread: {r.all_legs_resolved}"
          f" (unresolved: {r.unresolved})")
        P(f"         SELECTION WIDTH on the offset dial (OOS Sharpe, max-min): {r.offset_Sharpe_width:.4f}")
    P("")

    # ------------------------------------------------------------------ B6 4a
    P("-" * 100)
    P("(F) B6 -- PATH 4a AT EVERY GRID POINT, scored against the live d=0 10 bps book")
    P("-" * 100)
    n4a = int(vd.pass4a_d0.sum())
    P(f"  4a at d=0: {n4a} of {len(vd)} (panel x cost x window) cells.  By construction the")
    P(f"  (d=0, 10 bps) cell ties itself on all three legs, so 4a's strict '>' fails there.")
    tot = 0; hit = 0
    for pname in panels:
        for c in COSTS:
            for wn in WINS:
                anch = paths[(pname, 0, COST0, wn)]
                for d in OFFSETS:
                    tot += 1
                    hit += legs4a(paths[(pname, d, c, wn)], anch)
    P(f"  4a over ALL {tot} (panel x offset x cost x window) grid points: {hit} pass ({hit/tot:.3f})")
    P("")

    pd.DataFrame(gate_rows).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {SLUG}.{{grid,clause,verdicts,walkforward,gates}}.csv + .console.txt")


if __name__ == "__main__":
    main()
