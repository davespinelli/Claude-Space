#!/usr/bin/env python3
"""
IDEA 2125 (lane C, 2026-09-22) -- is-the-4b-CAGR-FLOOR-REACHABLE-AT-ALL-below-GROSS-1.00

THE QUESTION, as filed.  Idea 2119 (lane B, 2026-09-22) laddered the live band book over
band x gross and found every one of its 16 4b passes sitting at gross 1.00 on BOTH panels,
with every de-grossed cell (g <= 0.85) dying on the 4b CAGR FLOOR while its DD leg never
binds.  On the BAND family, therefore, the 4b CAGR floor is a pure EXPOSURE bar: the only
dial that reaches it is gross.  This run asks whether that is a property of the BAR or a
property of the FAMILY.  Put a NON-EXPOSURE device on the same book -- CONCENTRATION of the
in-band set, i.e. a holding count N -- and ask whether ANY book clears the CAGR floor at
g <= 0.85.  Publish the LOWEST gross at which any book clears it.

THE BOOK (RULES v2's form, generalised on ONE new dial and nothing else):
    band(i,t) TRUE when close > 200d MA x (1+b), FALSE below x (1-b), previous state in
    between, FALSE before 200 closes exist  ==  baseline.band_state(px, b), b FIXED at the
    live 0.03.
    Among the names whose band state is TRUE, rank by the record's own price-only chooser
    (baseline.score(px, vol_scale=False): the mean of the 12-1 / 6m / 3m cross-sectional
    percentile ranks, halved for names below their 200d MA -- the composite the 2026-09-03
    RECOMMENDATION memo found carries IC t ~ 4.2 BEFORE the vol scaler cancels it, and the
    form the 2026-09-04 KEEP-4b used).  Hold the TOP N of them at g/N of NAV each.
    Fewer than N in band  ->  the shortfall goes to CASH (de-gross, NEVER re-spread), which
    is RULES v2's own convention.  N = ALL recovers baseline.rules_v2_weights EXACTLY
    (gate G3): per-name weight g/#priced.
    Weekly, weights decided at close t applied at t+1, 10 bps per unit turnover, long only,
    no leverage, no shorting.

TUNED PARAMETERS -- EXACTLY TWO, and EVERY grid point is published (<slug>.grid.csv):
    1. GROSS     g in {0.50, 0.60, 0.75, 0.85, 1.00}
    2. HOLDINGS  N in {5, 10, 20, 40, ALL}
NOT TUNED, and declared as such before any number was read:
    BAND b = 0.03, the live value (idea 2119 already laddered it; this run holds it fixed
      so the holding count is the only new dial).
    THE RANKING is FIXED at the composite above.  Two REVERSE/PLACEBO rankings (bottom-N by
      the same composite; alphabetical-by-ticker) are priced as CONTROLS only -- they are
      diagnostics of WHERE any CAGR lift comes from, and NO verdict below is read off them.
    COST c in {0, 10, 25, 50} bps is PROTOCOL rung 2 (10 bps) plus its robustness ladder.
    PANEL {U56 = research/universe.json, B136 = research/universe_broad.json}.
    WINDOWS FULL / IS (..2016-12-31) / OOS (2017-01-01..), rule 8.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE QUESTION.  At 10 bps, does ANY (g <= 0.85, N) cell clear the 4b CAGR floor
      (CAGR >= 0.70 x SPY on the SAME window)?  Reported per panel per window, as a count
      out of the 20 de-grossed cells, with the floor margin of the best cell.
  B2  THE PUBLISHED NUMBER.  The LOWEST gross at which ANY book (a) clears the CAGR floor
      and (b) is a FULL 4b PASS -- per panel per window.  If no de-grossed book clears it,
      that is the answer and the floor is confirmed a pure exposure bar on this family too.
  B3  IS THE DEVICE ACTUALLY NON-EXPOSURE?  Report REALISED MEAN GROSS for every cell.  A
      concentration device that clears the floor by quietly running MORE exposure than its
      nominal g is an exposure device wearing a different hat, and B4 is the test.
  B4  MATCHED-REALISED-GROSS CONTROL.  For every floor-clearing cell with g <= 0.85, build
      the plain N=ALL band book scaled to the SAME realised mean gross (one linear solve on
      nominal g, with the ACHIEVED realised gross reported so any residual mismatch is
      visible) and report dCAGR / dSharpe / dMaxDD.  Concentration earns its keep only if
      it beats its own exposure twin.
  B5  RULE 8.  (g, N) chosen on the IS window ONLY, by IS Sharpe, at 10 bps.  2017-2026 read
      ONCE.  Report OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY, BOTH KEEP paths.
  B6  PATH 4a at every grid point (Sharpe > RULES v2 in BOTH halves AND MaxDD no worse).
  B7  COST LADDER.  B1/B2 re-read at 0 / 25 / 50 bps.
  B8  CONTROL READ.  The same B1/B2 counts under the two placebo rankings, published beside
      the real one.  If the placebo rankings clear the floor just as often, the lift is
      CONCENTRATION (a variance effect on a survivorship-biased tape), not the chooser.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)      bar max|d| < 1e-12
  G2  offset_mask(idx, 0) == engine.rebalance_mask(idx, 'W')      bar 0 differing rows
  G3  N=ALL, g=0.75, b=0.03 weights == baseline.rules_v2_weights  bar max|d| == 0
  G4  NO LEVERAGE: max row-sum of every weight matrix <= its nominal g + 1e-12
  G5  comparands are baseline's own: rules_v2_weights (live RULES v2) and SPY buy-and-hold

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists.  This matters
MORE than usual here: a holding-count device concentrates into the very names the list was
selected on, so every absolute CAGR at small N is optimistic by an unknown and probably
INCREASING amount as N falls.  The B4 matched-gross contrast and the B8 placebo rankings are
WITHIN-TAPE (same names, same dates) and are what any verdict below rests on; they do not
repair the level.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_4b-cagr-floor-below-gross-one_C.py
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights, score    # noqa
from engine import backtest, metrics, rebalance_mask                       # noqa

SLUG = "2026-09-22_4b-cagr-floor-below-gross-one_C"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BAND    = 0.03                                  # FIXED at the live value, not tuned
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]        # TUNED axis 1
HOLDS   = [5, 10, 20, 40, None]                 # TUNED axis 2 (None == ALL == RULES v2 form)
COSTS   = [0, 10, 25, 50]
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
RANKINGS = ["TOP", "BOTTOM", "ALPHA"]           # TOP is the book; the others are CONTROLS


def hname(N):
    return "ALL" if N is None else str(N)


# =========================================================================================
# schedule + a schedule-taking backtester (engine.backtest only accepts a freq string)
# =========================================================================================
def offset_mask(idx, d=0):
    key = pd.Series(idx.to_period("W"), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out


def run(prices, weights, mask):
    """engine.backtest's loop in numpy, semantics byte-for-byte (gate G1).  Costs are applied
    afterwards -- they never change the held path -- so one loop serves every cost rung.
    Also returns the realised HELD gross path (B3)."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n); held_gross = np.empty(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held_gross[i] = cur.sum()
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(gross_ret, index=prices.index),
            pd.Series(turn, index=prices.index),
            pd.Series(held_gross, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


# =========================================================================================
# the book
# =========================================================================================
def rank_frame(px, kind):
    """Higher is better.  TOP/BOTTOM use the record's own composite (no vol scaler);
    ALPHA is a fixed, information-free placebo (alphabetical by ticker)."""
    if kind == "ALPHA":
        order = {c: i for i, c in enumerate(sorted(px.columns))}
        v = np.tile(np.array([-order[c] for c in px.columns], dtype=float), (len(px), 1))
        return pd.DataFrame(v, index=px.index, columns=px.columns)
    s, _, _ = score(px, vol_scale=False)
    return s if kind == "TOP" else -s


def book_weights(px, gross, N, ranks, inband):
    """RULES v2's form with a holding cap.  N=None -> per-name weight gross/#priced (i.e.
    baseline.rules_v2_weights EXACTLY).  N finite -> top-N of the in-band set at gross/N
    each; any shortfall (fewer than N in band) goes to CASH, never re-spread."""
    if N is None:
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(inband, 0.0)
    elig = ranks.where(inband & px.notna())
    rk = elig.rank(axis=1, ascending=False, method="first")
    return (rk <= N).astype(float) * (gross / N)


# =========================================================================================
# scoring
# =========================================================================================
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= 0.60 * ss["MaxDD"], CAGR=s["CAGR"] >= 0.70 * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - 0.60 * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - 0.70 * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def legs4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


def wins(r, start):
    r = r.loc[start:]
    return dict(FULL=r, IS=r.loc[:IS_END], OOS=r.loc[OOS_BEG:])


# =========================================================================================
def main():
    P("=" * 100)
    P("IDEA 2125 lane C 2026-09-22 -- IS THE 4b CAGR FLOOR REACHABLE AT ALL BELOW GROSS 1.00?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: gross {GROSSES} x holdings {[hname(n) for n in HOLDS]}"
      f"  ({len(GROSSES)*len(HOLDS)} cells/panel/ranking)")
    P(f"not tuned: band {BAND} (live), ranking FIXED (TOP by the no-vol-scaler composite;")
    P(f"           BOTTOM/ALPHA are CONTROLS only), costs {COSTS} bps, cadence {FREQ},")
    P(f"           panels U56 + B136, windows FULL / IS..{IS_END} / OOS {OOS_BEG}..")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} names  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("(G) GATES -- printed before any hypothesis is read")
    P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]
    ib_u = band_state(px_u, BAND)
    rk_u = rank_frame(px_u, "TOP")

    m0 = offset_mask(px_u.index, 0)
    g2 = int((m0.values != rebalance_mask(px_u.index, FREQ).values).sum())
    ok = g2 == 0; gp += ok; gn += 1
    P(f"  G2  offset_mask(idx,0) == engine.rebalance_mask(idx,'W') : {g2} differing rows"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G2", value=g2, bar="0 differing rows", passed=bool(ok)))

    w_live = book_weights(px_u, 0.75, None, rk_u, ib_u)
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, band=BAND, gross=0.75).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  book_weights(px,0.75,ALL) == baseline.rules_v2_weights : max|d| {g3:.3e}"
      f"   [{'PASS' if ok else 'FAIL'}]  (the N=ALL column IS the live book)")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))

    gr, to, hg = run(px_u, w_live, m0)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"].values
    fin = np.isfinite(b)
    g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}"
      f" over {int(fin.sum())} rows   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))

    lev = 0.0
    for g in GROSSES:
        for N in HOLDS:
            w = book_weights(px_u, g, N, rk_u, ib_u)
            lev = max(lev, float(w.sum(axis=1).max() - g))
    ok = lev <= 1e-12; gp += ok; gn += 1
    P(f"  G4  NO LEVERAGE: max(row-sum - nominal g) over all 25 U56 weight matrices"
      f" = {lev:.3e}   bar <= 1e-12   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4", value=lev, bar="<= 1e-12", passed=bool(ok)))

    P("  G5  comparands: baseline.rules_v2_weights (band 0.03, gross 0.75, W) and SPY"
      " buy-and-hold   [PASS by construction]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True))
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ------------------------------------------------------------------ the grid
    P("-" * 100)
    P(f"(1) THE GRID -- every one of 2 x 3 x 25 x 4 x 3 cells is written to {SLUG}.grid.csv")
    P("-" * 100)
    rows, bench, keep_paths = [], {}, {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq=FREQ)["returns"]
        mask = offset_mask(px.index, 0)
        inband = band_state(px, BAND)
        bench[pname] = dict(spy={w: stats(x) for w, x in wins(spy, start).items()},
                            base={w: stats(x) for w, x in wins(base_r, start).items()},
                            start=start)
        for kind in RANKINGS:
            ranks = rank_frame(px, kind)
            for g in GROSSES:
                for N in HOLDS:
                    w = book_weights(px, g, N, ranks, inband)
                    gr, to, hg = run(px, w, mask)
                    rg = {wn: float(hg.loc[start:].pipe(
                              lambda s: s.loc[:IS_END] if wn == "IS" else
                                        (s.loc[OOS_BEG:] if wn == "OOS" else s)).mean())
                          for wn in ("FULL", "IS", "OOS")}
                    nh = {wn: float(((w != 0).sum(axis=1)).loc[start:].pipe(
                              lambda s: s.loc[:IS_END] if wn == "IS" else
                                        (s.loc[OOS_BEG:] if wn == "OOS" else s)).mean())
                          for wn in ("FULL", "IS", "OOS")}
                    for c in COSTS:
                        r = net(gr, to, c)
                        for wn, rr in wins(r, start).items():
                            s = stats(rr)
                            sp, sb = bench[pname]["spy"][wn], bench[pname]["base"][wn]
                            ok4b, L, Mg = legs4b(s, sp)
                            rows.append(dict(
                                panel=pname, ranking=kind, gross=g, holds=hname(N), cost=c,
                                window=wn, CAGR=s["CAGR"], Sharpe=s["Sharpe"],
                                MaxDD=s["MaxDD"], H1=s["H1"], H2=s["H2"],
                                realised_gross=rg[wn], mean_names=nh[wn],
                                turnover_yr=float(to.loc[start:].sum() / (len(rr) / 252)),
                                pass4b=ok4b, pass4a=legs4a(s, sb),
                                leg_CAGR=L["CAGR"], leg_DD=L["DD"],
                                leg_H1=L["H1"], leg_H2=L["H2"],
                                m_CAGR=Mg["CAGR"], m_DD=Mg["DD"],
                                m_H1=Mg["H1"], m_H2=Mg["H2"],
                                spy_CAGR=sp["CAGR"], spy_Sharpe=sp["Sharpe"],
                                spy_MaxDD=sp["MaxDD"],
                                base_CAGR=sb["CAGR"], base_Sharpe=sb["Sharpe"],
                                base_MaxDD=sb["MaxDD"]))
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"  {len(G)} rows written.")
    P("")

    # the book only (TOP ranking, 10 bps) is what any verdict is read off
    B = G[(G.ranking == "TOP") & (G.cost == COST0)]

    # ------------------------------------------------------------------ B1
    P("-" * 100)
    P("(B1) THE QUESTION -- does ANY de-grossed cell (g <= 0.85) clear the 4b CAGR FLOOR?")
    P("     [TOP ranking, 10 bps.  20 de-grossed cells per panel per window.]")
    P("-" * 100)
    P(f"  {'panel':6s} {'window':6s} {'floor=0.7xSPY':>14s} {'clear/20':>9s} {'best cell':>16s}"
      f" {'best CAGR':>10s} {'margin pp':>10s}")
    b1 = []
    for pname in panels:
        for wn in ("FULL", "IS", "OOS"):
            d = B[(B.panel == pname) & (B.window == wn) & (B.gross <= 0.85)]
            floor = 0.70 * d.spy_CAGR.iloc[0]
            nclear = int(d.leg_CAGR.sum())
            best = d.loc[d.CAGR.idxmax()]
            P(f"  {pname:6s} {wn:6s} {floor:13.2%}  {nclear:4d}/20    "
              f"g={best.gross:.2f} N={best.holds:>3s}  {best.CAGR:9.2%} {best.m_CAGR:+10.2f}")
            b1.append(dict(panel=pname, window=wn, floor=floor, n_clear=nclear,
                           best_gross=best.gross, best_holds=best.holds,
                           best_CAGR=best.CAGR, best_margin_pp=best.m_CAGR))
    pd.DataFrame(b1).to_csv(OUT / f"{SLUG}.b1.csv", index=False)
    P("")

    # ------------------------------------------------------------------ B2
    P("-" * 100)
    P("(B2) THE PUBLISHED NUMBER -- LOWEST gross at which ANY book clears the CAGR floor,")
    P("     and the LOWEST at which any book is a FULL 4b PASS.  [TOP, 10 bps]")
    P("-" * 100)
    P(f"  {'panel':6s} {'window':6s} {'lowest g: CAGR floor':>22s} {'lowest g: FULL 4b':>20s}")
    b2 = []
    for pname in panels:
        for wn in ("FULL", "IS", "OOS"):
            d = B[(B.panel == pname) & (B.window == wn)]
            cf = d[d.leg_CAGR]; fp = d[d.pass4b]
            lo_c = f"{cf.gross.min():.2f}" if len(cf) else "NONE"
            lo_f = f"{fp.gross.min():.2f}" if len(fp) else "NONE"
            nm_c = ",".join(sorted(cf[cf.gross == cf.gross.min()].holds)) if len(cf) else "-"
            nm_f = ",".join(sorted(fp[fp.gross == fp.gross.min()].holds)) if len(fp) else "-"
            P(f"  {pname:6s} {wn:6s} {lo_c:>12s} (N={nm_c:<7s}) {lo_f:>8s} (N={nm_f:<7s})")
            b2.append(dict(panel=pname, window=wn, lowest_gross_cagr_floor=lo_c,
                           holds_at=nm_c, lowest_gross_full4b=lo_f, holds_at_4b=nm_f))
    pd.DataFrame(b2).to_csv(OUT / f"{SLUG}.b2.csv", index=False)
    P("")

    # ------------------------------------------------------------------ B3
    P("-" * 100)
    P("(B3) IS THE DEVICE NON-EXPOSURE?  realised MEAN GROSS and mean #names, FULL, 10 bps")
    P("-" * 100)
    for pname in panels:
        d = B[(B.panel == pname) & (B.window == "FULL")]
        P(f"  panel {pname}")
        P("    " + "realised mean gross".ljust(22) +
          "  ".join(f"N={hname(n):>3s}" for n in HOLDS))
        for g in GROSSES:
            v = [d[(d.gross == g) & (d.holds == hname(n))].realised_gross.iloc[0] for n in HOLDS]
            P(f"      nominal g={g:.2f}      " + "  ".join(f"{x:6.3f}" for x in v))
        P("    " + "mean #names held".ljust(22) +
          "  ".join(f"N={hname(n):>3s}" for n in HOLDS))
        v = [d[(d.gross == 0.75) & (d.holds == hname(n))].mean_names.iloc[0] for n in HOLDS]
        P("      (any g)           " + "  ".join(f"{x:6.1f}" for x in v))
    P("")

    # ------------------------------------------------------------------ B4
    P("-" * 100)
    P("(B4) MATCHED-REALISED-GROSS CONTROL -- every floor-clearing cell with g <= 0.85")
    P("     against the plain N=ALL band book scaled to the SAME realised mean gross.")
    P("-" * 100)
    b4 = []
    for pname, px in panels.items():
        start = bench[pname]["start"]
        mask = offset_mask(px.index, 0)
        inband = band_state(px, BAND)
        ranks = rank_frame(px, "TOP")
        # realised mean gross of the N=ALL book at nominal 1.00, per window -> linear solve
        gr1, to1, hg1 = run(px, book_weights(px, 1.00, None, ranks, inband), mask)
        for wn in ("FULL", "IS", "OOS"):
            sl = (lambda s: s.loc[:IS_END] if wn == "IS" else
                  (s.loc[OOS_BEG:] if wn == "OOS" else s))
            g_all_1 = float(sl(hg1.loc[start:]).mean())
            d = B[(B.panel == pname) & (B.window == wn) & (B.gross <= 0.85) & (B.leg_CAGR)]
            for _, row in d.iterrows():
                k = row.realised_gross / g_all_1        # nominal gross of the matched twin
                wc = book_weights(px, k, None, ranks, inband)
                grc, toc, hgc = run(px, wc, mask)
                rc = net(grc, toc, COST0)
                sc = stats(sl(rc.loc[start:]))
                ach = float(sl(hgc.loc[start:]).mean())
                b4.append(dict(panel=pname, window=wn, gross=row.gross, holds=row.holds,
                               realised_gross=row.realised_gross,
                               twin_nominal=k, twin_realised=ach,
                               dCAGR_pp=(row.CAGR - sc["CAGR"]) * 100,
                               dSharpe=row.Sharpe - sc["Sharpe"],
                               dMaxDD_pp=(row.MaxDD - sc["MaxDD"]) * 100,
                               twin_CAGR=sc["CAGR"], twin_Sharpe=sc["Sharpe"],
                               twin_MaxDD=sc["MaxDD"]))
    if b4:
        B4 = pd.DataFrame(b4); B4.to_csv(OUT / f"{SLUG}.b4.csv", index=False)
        P(f"  {'panel':6s} {'win':5s} {'g':>5s} {'N':>4s} {'real g':>7s} {'twin g':>7s}"
          f" {'dCAGR pp':>9s} {'dSharpe':>8s} {'dMaxDD pp':>10s}")
        for _, r in B4.iterrows():
            P(f"  {r.panel:6s} {r.window:5s} {r.gross:5.2f} {r.holds:>4s} {r.realised_gross:7.3f}"
              f" {r.twin_realised:7.3f} {r.dCAGR_pp:+9.2f} {r.dSharpe:+8.4f} {r.dMaxDD_pp:+10.2f}")
        P(f"  --> concentration beats its own exposure twin on CAGR at "
          f"{int((B4.dCAGR_pp > 0).sum())} of {len(B4)} cells, on Sharpe at "
          f"{int((B4.dSharpe > 0).sum())}, and is SHALLOWER at {int((B4.dMaxDD_pp > 0).sum())}.")
    else:
        P("  NO de-grossed cell clears the CAGR floor on any panel/window -- nothing to match.")
        P("  (That IS the B1/B2 answer: on this family the floor is a pure exposure bar.)")
    P("")

    # ------------------------------------------------------------------ B6
    P("-" * 100)
    P("(B6) PATH 4a at every grid point [TOP, 10 bps]")
    P("-" * 100)
    for pname in panels:
        for wn in ("FULL", "IS", "OOS"):
            d = B[(B.panel == pname) & (B.window == wn)]
            n = int(d.pass4a.sum())
            P(f"  {pname:6s} {wn:5s}  4a PASS {n:2d} of {len(d)}" +
              ("   " + ", ".join(f"g={r.gross:.2f}/N={r.holds}" for _, r in d[d.pass4a].iterrows())
               if n else ""))
    P("")

    # ------------------------------------------------------------------ B7
    P("-" * 100)
    P("(B7) COST LADDER -- B1 (de-grossed cells clearing the CAGR floor) and B2 by cost")
    P("-" * 100)
    P(f"  {'panel':6s} {'win':5s} " + "  ".join(f"{c:>2d}bps clear/20 | lowest-g 4b" for c in COSTS))
    for pname in panels:
        for wn in ("FULL", "IS", "OOS"):
            cells = []
            for c in COSTS:
                d = G[(G.ranking == "TOP") & (G.cost == c) & (G.panel == pname) & (G.window == wn)]
                nc = int(d[d.gross <= 0.85].leg_CAGR.sum())
                fp = d[d.pass4b]
                cells.append(f"{nc:9d}/20 | {(f'{fp.gross.min():.2f}' if len(fp) else 'NONE'):>12s}")
            P(f"  {pname:6s} {wn:5s} " + "  ".join(cells))
    P("")

    # ------------------------------------------------------------------ B8
    P("-" * 100)
    P("(B8) CONTROL READ -- the same counts under the two PLACEBO rankings (never selected on)")
    P("-" * 100)
    P(f"  {'panel':6s} {'win':5s} {'ranking':8s} {'clear/20 (g<=.85)':>18s} {'full 4b/25':>11s}"
      f" {'lowest-g 4b':>12s} {'best CAGR':>10s}")
    b8 = []
    for pname in panels:
        for wn in ("FULL", "IS", "OOS"):
            for kind in RANKINGS:
                d = G[(G.ranking == kind) & (G.cost == COST0) &
                      (G.panel == pname) & (G.window == wn)]
                nc = int(d[d.gross <= 0.85].leg_CAGR.sum())
                fp = d[d.pass4b]
                lo = f"{fp.gross.min():.2f}" if len(fp) else "NONE"
                P(f"  {pname:6s} {wn:5s} {kind:8s} {nc:15d}/20 {int(len(fp)):8d}/25"
                  f" {lo:>12s} {d.CAGR.max():10.2%}")
                b8.append(dict(panel=pname, window=wn, ranking=kind, clear20=nc,
                               full4b=int(len(fp)), lowest_g_4b=lo, best_CAGR=d.CAGR.max()))
    pd.DataFrame(b8).to_csv(OUT / f"{SLUG}.b8.csv", index=False)
    P("")

    # ------------------------------------------------------------------ B5  RULE 8
    P("-" * 100)
    P("(B5) RULE 8 WALK-FORWARD -- (g, N) chosen on IS (..2016) by IS Sharpe ONLY, 10 bps.")
    P("     2017-2026 READ ONCE.  Both KEEP paths.")
    P("-" * 100)
    wf = []
    for pname in panels:
        dIS = B[(B.panel == pname) & (B.window == "IS")]
        pick = dIS.loc[dIS.Sharpe.idxmax()]
        dO = B[(B.panel == pname) & (B.window == "OOS") &
               (B.gross == pick.gross) & (B.holds == pick.holds)].iloc[0]
        dF = B[(B.panel == pname) & (B.window == "FULL") &
               (B.gross == pick.gross) & (B.holds == pick.holds)].iloc[0]
        P(f"  panel {pname}:  IS pick  gross={pick.gross:.2f}  N={pick.holds}"
          f"   (IS Sharpe {pick.Sharpe:.4f}; IS 4b {'PASS' if pick.pass4b else 'FAIL'})")
        P(f"    {'':22s} {'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'H1/H2':>15s}")
        for lbl, r in (("candidate OOS", dO), ("candidate FULL", dF)):
            P(f"    {lbl:22s} {r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%}"
              f" {r.H1:7.3f}/{r.H2:6.3f}")
        P(f"    {'RULES v2 OOS':22s} {dO.base_CAGR:8.2%} {dO.base_Sharpe:8.4f}"
          f" {dO.base_MaxDD:8.2%}")
        P(f"    {'SPY OOS':22s} {dO.spy_CAGR:8.2%} {dO.spy_Sharpe:8.4f} {dO.spy_MaxDD:8.2%}")
        P(f"    {'RULES v2 FULL':22s} {dF.base_CAGR:8.2%} {dF.base_Sharpe:8.4f}"
          f" {dF.base_MaxDD:8.2%}")
        P(f"    {'SPY FULL':22s} {dF.spy_CAGR:8.2%} {dF.spy_Sharpe:8.4f} {dF.spy_MaxDD:8.2%}")
        P(f"    4b OOS  {'PASS' if dO.pass4b else 'FAIL'}   legs "
          f"H1 {'Y' if dO.leg_H1 else 'n'} ({dO.m_H1:+.4f})  H2 {'Y' if dO.leg_H2 else 'n'}"
          f" ({dO.m_H2:+.4f})  DD {'Y' if dO.leg_DD else 'n'} ({dO.m_DD:+.2f}pp)"
          f"  CAGR {'Y' if dO.leg_CAGR else 'n'} ({dO.m_CAGR:+.2f}pp)")
        P(f"    4b FULL {'PASS' if dF.pass4b else 'FAIL'}   legs "
          f"H1 {'Y' if dF.leg_H1 else 'n'} ({dF.m_H1:+.4f})  H2 {'Y' if dF.leg_H2 else 'n'}"
          f" ({dF.m_H2:+.4f})  DD {'Y' if dF.leg_DD else 'n'} ({dF.m_DD:+.2f}pp)"
          f"  CAGR {'Y' if dF.leg_CAGR else 'n'} ({dF.m_CAGR:+.2f}pp)")
        P(f"    4a OOS  {'PASS' if dO.pass4a else 'FAIL'}    4a FULL "
          f"{'PASS' if dF.pass4a else 'FAIL'}")
        P(f"    realised mean gross  OOS {dO.realised_gross:.3f}  FULL {dF.realised_gross:.3f}"
          f"   turnover/yr OOS {dO.turnover_yr:.2f}")
        wf.append(dict(panel=pname, pick_gross=pick.gross, pick_holds=pick.holds,
                       IS_Sharpe=pick.Sharpe, IS_4b=bool(pick.pass4b),
                       OOS_CAGR=dO.CAGR, OOS_Sharpe=dO.Sharpe, OOS_MaxDD=dO.MaxDD,
                       OOS_4b=bool(dO.pass4b), OOS_4a=bool(dO.pass4a),
                       FULL_CAGR=dF.CAGR, FULL_Sharpe=dF.Sharpe, FULL_MaxDD=dF.MaxDD,
                       FULL_4b=bool(dF.pass4b), FULL_4a=bool(dF.pass4a),
                       spy_OOS_CAGR=dO.spy_CAGR, spy_OOS_Sharpe=dO.spy_Sharpe,
                       spy_OOS_MaxDD=dO.spy_MaxDD, base_OOS_Sharpe=dO.base_Sharpe))
        P("")
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ 4b-passing census
    P("-" * 100)
    P("(2) EVERY FULL-4b PASS on the book [TOP, 10 bps], all windows")
    P("-" * 100)
    pp = B[B.pass4b]
    if len(pp):
        P(f"  {'panel':6s} {'win':5s} {'g':>5s} {'N':>4s} {'CAGR':>8s} {'Sharpe':>8s}"
          f" {'MaxDD':>8s} {'realg':>6s} {'mCAGR':>7s} {'mDD':>7s}")
        for _, r in pp.sort_values(["panel", "window", "gross"]).iterrows():
            P(f"  {r.panel:6s} {r.window:5s} {r.gross:5.2f} {r.holds:>4s} {r.CAGR:8.2%}"
              f" {r.Sharpe:8.4f} {r.MaxDD:8.2%} {r.realised_gross:6.3f}"
              f" {r.m_CAGR:+7.2f} {r.m_DD:+7.2f}")
    else:
        P("  NONE.")
    P("")
    P("=" * 100)
    (OUT / f"{SLUG}.log.txt").write_text("\n".join(LINES) + "\n")
    pd.DataFrame(gate_rows).to_csv(OUT / f"{SLUG}.gates.csv", index=False)


if __name__ == "__main__":
    main()
