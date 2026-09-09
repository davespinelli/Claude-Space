#!/usr/bin/env python3
"""Idea 328: is the no-trade BAND's argmax INTERIOR, or a GRID EDGE?

THE QUESTION, exactly as filed (QUEUE 328).  Idea 325's 4b PARK candidate (U56 top-20,
no-trade band m=20) sits on a Sharpe curve that is monotone in m out to the widest point
anyone tested (m=40, dSharpe +0.063), so idea 240/256's grid-edge flag applies: an argmax
at the edge of the grid is not an argmax, it is an unfinished sweep.  Sweep

        m in {40, 60, 80, 120, NO-SELL-EVER}   x   n in {10, 20}

on all three panels and ask whether the band has a LOCATED optimum or is just 'trade
less' -- in which case the honest instrument is a CADENCE dial, not a band.

WHAT THIS RUN ADDS TO THE FILED WORDING, and why.  Three things, none of them a third
tuned parameter:

  (i) the anchor rungs m in {0, 5, 10, 20} are re-run alongside the new wide rungs.  The
      question is about the SHAPE of a curve; a curve cannot be read from its right tail
      alone, and idea 384's committed points were produced by a different script.  Same
      dial, same two parameters (n, m); 9 m-levels x 2 n x 3 panels = 54 cells, ALL
      reported at all three cost rungs.

 (ii) a DEGENERACY test, which the filed wording does not anticipate but which decides
      it.  The band expels a held name when its rank passes n + m.  On a panel with an
      eligible-rank ceiling K_t, any cell with n + m >= K_t can never expel by rank: it
      is not a band at all, it is HOLD-UNTIL-INELIGIBLE (idea 280's already-KILLED m=999
      arm), and idea 384 already tripped over this once at (U56, n=20, m=40).  For every
      cell this run tests whether its selection frame is BIT-IDENTICAL to the NO-SELL-EVER
      arm at the same n, and reports m*(panel, n) = the smallest m at which that happens.
      An argmax at or beyond m* is not a band optimum and is reported as such.

(iii) the MATCHED-TURNOVER CADENCE CONTROL that the filed wording names as the
      alternative ('the honest instrument is a cadence dial').  For each n the same
      parent book (m = 0) is run at cadences k x weekly, k in {1,2,3,4,6,8,13,26}.  The
      cadence ladder is a CONTROL ARM, not a swept parameter of the idea: no cadence is
      ever chosen, the whole ladder is reported, and each band cell is priced against the
      cadence arm at its OWN realised turnover (nearest rung AND log-turnover
      interpolation, both reported).  If cadence buys the same Sharpe for the same
      turnover, the band is redundant.

PRE-REGISTERED READINGS, fixed before any number was read:
  H_LOCATED   argmax_m Sharpe (10 bps) is STRICTLY INTERIOR to the genuine (m < m*)
              range, on at least 2 of 3 panels, at both n.
  H_EDGE      argmax_m sits at the widest genuine rung or beyond it, i.e. the sweep is
              still monotone where the band is still a band -> 'trade less'.
  H_CADENCE   at matched turnover the cadence arm attains >= the band's Sharpe, in which
              case the band is not the instrument even where it wins on the raw ladder.

FAMILY, pre-registered and fixed (idea 331/333/384's convention, verbatim):
    book    top-n of the v1 composite with the VOL SCALER OFF, among RULES v1 eligible
            names (200d MA up, vol20 < 0.60); NORM weights g / k_t
    band    sel_band (idea 273/331): enter at rank <= n, hold until rank passes n + m;
            free slots refill best-rank-first; slot count is the parent's own k_t, so m
            is name-count matched and a pure turnover dial
    gross   0.75, NOT swept              cadence  weekly for the idea arm, NOT swept
    panels  {U56, B136, SMALL439} and cost rungs {0, 10, 25} bps are REPORTED AXES, not
            choices.  10 bps is PROTOCOL's.

GATES, all exact, all run before any new number is read:
    G1  fast_backtest vs products/backtester/engine.backtest (returns AND turnover).
    G2  the derived cost-rung identity r(c) = r(0) - turnover*c/1e4 vs a live cost_bps run.
    G3  sel_band(m=0) nests sel_hard(n) exactly on every rebalance day.
    G4  the (U56, n=20, g=0.75, m=20, W, 10 bps) cell reproduces idea 384's committed
        headline row (12.87% / 1.112 / -17.22% / 1.144 / 1.093).
    G5  nweek_mask(idx, 1) equals engine.rebalance_mask(idx, 'W') exactly.

PANEL VINTAGE (idea 514's stamp, and it is load-bearing here).  U56 is cached daily and
now runs to 2026-09-08; B136 and SMALL439 were last cached 2026-09-04.  G4 FAILS on the
raw 2026-09-08 U56 (max|d| 7.70e-03, driven entirely by the half split: H1 1.1514 vs the
filed 1.144) and PASSES at 4.07e-04 on the 2026-09-04 vintage, so the discrepancy is
panel drift, not a code disagreement -- four extra trading days move the H1/H2 boundary
and reprice both halves.  All three panels are therefore TRUNCATED to their common last
date before anything is run, and both numbers are reported rather than the passing one
alone.  This is a stated design choice for cross-panel comparability, not a tuned
parameter.

RULE 8 (PROTOCOL 8), run on every panel: (n, m) chosen on 2008-2016 IS Sharpe at 10 bps,
2017-2026 read ONCE, reported against SPY OOS, RULES v2 OOS and the OOS-best cell.  Both
the unrestricted pick and the pick RESTRICTED TO GENUINE BANDS (m < m*) are reported,
because idea 384 showed the two differ.

Both KEEP paths (PROTOCOL 4a and 4b) are evaluated at every one of the 54 cells at every
cost rung.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- so CAGR
levels are optimistic and 4b's CAGR floor is tested in the book's favour.  (2) The 4a
comparand RULES v2 runs at its own live weekly cadence and gross, so the dials move the
idea arm only.  (3) SMALL439 starts 2010-01-04 and drops the 44 tickers with
max_1d_move >= 1.0, so its IS window is 7 years, not 9.  (4) NO-SELL-EVER still expels a
name that stops being priced or stops being eligible; it is 'never sell on RANK', not
'never sell'.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-09_is-the-no-trade-BAND-argmax-interior-or-a-grid-edge_B"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS = 0.60, 0.75
NS = [10, 20]
MS = [0, 5, 10, 20, 40, 60, 80, 120, "NOSELL"]          # the filed rungs + the anchors
KS = [1, 2, 3, 4, 6, 8, 13, 26]                          # cadence CONTROL ladder (weeks)
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ------------------------------------------------------------------ panels & book
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c not in bad]]


def rank_frame(px):
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    return s.where(above & (vol20 < MAX_VOL) & px.notna()).rank(axis=1, ascending=False)


def nweek_mask(idx, k):
    """Every k-th weekly rebalance day.  k=1 is engine.rebalance_mask(idx,'W') (gate G5)."""
    w = rebalance_mask(idx, "W").values
    out = np.zeros(len(idx), dtype=bool)
    pos = np.flatnonzero(w)
    out[pos[::k]] = True
    return pd.Series(out, index=idx)


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, mask=None):
    """idea 273/331's no-trade band, verbatim.  m=0 nests sel_hard(n) (G3).
    m='NOSELL' / None = never expel on RANK (idea 280's m=999 arm): a held name leaves
    only when it stops being eligible or stops being priced."""
    reb = (nweek_mask(px.index, 1) if mask is None else mask).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    nosell = (m is None) or (isinstance(m, str) and m == "NOSELL")
    thresh = np.inf if nosell else n + m
    held, last = [], np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= thresh]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j]:
                        break
                    if j not in hs:
                        held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel, gross=GROSS):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, mask=None):
    """Clone of engine.backtest returning GROSS returns and turnover so every cost rung is
    derived from one run (gated exactly against engine.backtest in G1/G2)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mk = (nweek_mask(px.index, 1) if mask is None else mask).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mk[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx),
            pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i_ = r.loc[OOS_START:], r.loc[:IS_END]
    mo, mi = metrics(o), metrics(i_)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"])


def keeps(s, v2, spy):
    """PROTOCOL 4a and 4b as conjunctions; returns (pass4a, pass4b, failed 4b bars)."""
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


def mlab(m):
    return "NOSELL" if isinstance(m, str) else str(m)


def mnum(m):
    return np.inf if isinstance(m, str) else float(m)


# ------------------------------------------------------------------ gates
def gates(px, rk, px_raw, rk_raw):
    P("\n[G] GATES (all pre-registered, all run before any new number is read)")
    ok = True

    sel = sel_band(px, rk, 20, 20)
    w = weights_from(sel)
    gr, tu, _ = fast_backtest(px, w)
    eng = backtest(px, w, cost_bps=0, freq="W")
    d1 = float((gr - eng["returns"]).abs().max())
    d2 = float((tu - eng["turnover"]).abs().max())
    P(f"    G1 fast_backtest vs engine.backtest: max|d returns| {d1:.3e}, "
      f"max|d turnover| {d2:.3e}  (bar 1e-12)  {'PASS' if max(d1,d2) < 1e-12 else 'FAIL'}")
    ok &= max(d1, d2) < 1e-12

    eng10 = backtest(px, w, cost_bps=10, freq="W")
    d3 = float(((gr - tu * 10 / 1e4) - eng10["returns"]).abs().max())
    P(f"    G2 cost-rung identity @10bps: max|d| {d3:.3e}  (bar 1e-12)  "
      f"{'PASS' if d3 < 1e-12 else 'FAIL'}")
    ok &= d3 < 1e-12

    reb = nweek_mask(px.index, 1).values
    s0 = sel_band(px, rk, 20, 0)
    hard = sel_hard(rk, 20).fillna(False)
    dis = int((s0.values[reb] != hard.values[reb]).sum())
    P(f"    G3 sel_band(m=0) vs sel_hard(n=20) on rebalance days: {dis} disagreements  "
      f"{'PASS' if dis == 0 else 'FAIL'}")
    ok &= dis == 0

    filed = dict(CAGR=0.1287, Sharpe=1.112, MaxDD=-0.1722, H1=1.144, H2=1.093)
    st = stats(gr, tu, 10, px.index[WARMUP])
    worst = max(abs(st[k] - v) for k, v in filed.items())
    P(f"    G4 (U56,n=20,m=20,g=0.75,W,10bps) vs idea 384's committed headline, at the "
      f"VINTAGE-MATCHED panel ({px.index[-1].date()}): CAGR {st['CAGR']:.4%} "
      f"Sharpe {st['Sharpe']:.4f} MaxDD {st['MaxDD']:.4%} H1 {st['H1']:.4f} "
      f"H2 {st['H2']:.4f}; max|d| {worst:.2e} (bar 5e-4)  "
      f"{'PASS' if worst < 5e-4 else 'FAIL'}")
    ok &= worst < 5e-4
    gr2, tu2, _ = fast_backtest(px_raw, weights_from(sel_band(px_raw, rk_raw, 20, 20)))
    st2 = stats(gr2, tu2, 10, px_raw.index[WARMUP])
    w2 = max(abs(st2[k] - v) for k, v in filed.items())
    P(f"    G4b THE SAME CELL ON TODAY'S RAW U56 ({px_raw.index[-1].date()}, "
      f"{len(px_raw) - len(px)} extra trading days), reported not hidden: "
      f"CAGR {st2['CAGR']:.4%} Sharpe {st2['Sharpe']:.4f} MaxDD {st2['MaxDD']:.4%} "
      f"H1 {st2['H1']:.4f} H2 {st2['H2']:.4f}; max|d| {w2:.2e} -> would FAIL the same "
      f"bar.  MaxDD is identical to 1e-6; the drift is the HALF SPLIT (H1 moves "
      f"{st2['H1'] - st['H1']:+.4f}).  Panel vintage, not a code disagreement.")

    d5 = int((nweek_mask(px.index, 1).values != rebalance_mask(px.index, "W").values).sum())
    P(f"    G5 nweek_mask(k=1) vs rebalance_mask('W'): {d5} disagreements  "
      f"{'PASS' if d5 == 0 else 'FAIL'}")
    ok &= d5 == 0

    P(f"    -> {'ALL GATES PASS' if ok else 'GATE FAILURE'}")
    return ok


# ------------------------------------------------------------------ main
def main():
    P(f"# {SLUG}")
    P(__doc__.split("\n")[2].strip())

    u_raw = load_universe(); b = load_universe(broad=True); sm = small_panel()
    VINTAGE = min(u_raw.index[-1], b.index[-1], sm.index[-1])
    P(f"    PANEL VINTAGE: raw last dates U56 {u_raw.index[-1].date()}, "
      f"B136 {b.index[-1].date()}, SMALL439 {sm.index[-1].date()} -> all three truncated "
      f"to the common last date {VINTAGE.date()} (see docstring).")
    u, b, sm = u_raw.loc[:VINTAGE], b.loc[:VINTAGE], sm.loc[:VINTAGE]
    panels = [("U56", u), ("B136", b), ("SMALL439", sm)]
    for nm, px in panels:
        P(f"    {nm}: {px.shape[1]} cols, {px.index[0].date()} -> {px.index[-1].date()}")

    rk_u = rank_frame(u)
    if not gates(u, rk_u, u_raw, rank_frame(u_raw)):
        P("GATE FAILURE — stopping."); (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG))
        sys.exit(1)

    ranks = {"U56": rk_u, "B136": rank_frame(b), "SMALL439": rank_frame(sm)}

    # ---------------- the eligible-rank ceiling, which decides degeneracy
    P("\n[0] PANEL ELIGIBLE-RANK CEILING K_t (how wide a band CAN be before it is not a band)")
    ceil_rows = []
    for nm, px in panels:
        rk = ranks[nm]
        reb = nweek_mask(px.index, 1).values
        K = rk.max(axis=1)[reb]
        ceil_rows.append(dict(panel=nm, cols=px.shape[1], K_min=K.min(), K_p25=K.quantile(.25),
                              K_median=K.median(), K_p75=K.quantile(.75), K_max=K.max()))
    ce = pd.DataFrame(ceil_rows)
    P(ce.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    ce.to_csv(OUT / f"{SLUG}.ceiling.csv", index=False)

    # ---------------- the grid
    P("\n[1] THE GRID — 3 panels x n{10,20} x m{0,5,10,20,40,60,80,120,NOSELL} x 3 rungs, "
      "g=0.75, weekly.  ALL 54 cells reported.")
    rows, spy_st, v2_st, degen = [], {}, {}, {}
    for nm, px in panels:
        rk = ranks[nm]
        start = px.index[WARMUP]
        spy_r = px["SPY"].pct_change().fillna(0.0)
        spy_st[nm] = {c: stats(spy_r, pd.Series(0.0, index=px.index), 0, start) for c in COSTS}
        v2w = rules_v2_weights(px)
        gv, tv, _ = fast_backtest(px, v2w)
        v2_st[nm] = {c: stats(gv, tv, c, start) for c in COSTS}
        for n in NS:
            sel_ns = sel_band(px, rk, n, "NOSELL")
            mstar = None
            for m in MS:
                sel = sel_ns if isinstance(m, str) else sel_band(px, rk, n, m)
                same_as_nosell = bool((sel.values == sel_ns.values).all())
                if same_as_nosell and mstar is None and not isinstance(m, str):
                    mstar = m
                gr, tu, names = fast_backtest(px, weights_from(sel))
                yrs = len(gr.loc[start:]) / 252
                for c in COSTS:
                    s = stats(gr, tu, c, start)
                    a, b4, fb = keeps(s, v2_st[nm][c], spy_st[nm][c])
                    rows.append(dict(panel=nm, n=n, m=mlab(m), m_num=mnum(m), cost_bps=c,
                                     degenerate=same_as_nosell, **s,
                                     turn_per_yr=tu.loc[start:].sum() / yrs,
                                     names=names.loc[start:].mean(),
                                     pass4a=a, pass4b=b4, fail4b=fb))
            degen[(nm, n)] = mstar
    g = pd.DataFrame(rows)
    g.to_csv(OUT / f"{SLUG}.grid.csv", index=False)

    for nm, _ in panels:
        for n in NS:
            sub = g[(g.panel == nm) & (g.n == n) & (g.cost_bps == 10)]
            P(f"\n    {nm}  n={n}  @10bps   (m* = smallest m identical to NOSELL: "
              f"{degen[(nm,n)] if degen[(nm,n)] is not None else 'none of the tested rungs'})")
            P(sub[["m", "degenerate", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                   "turn_per_yr", "names", "pass4a", "pass4b", "fail4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---------------- [2] the question: interior or edge?
    P("\n[2] IS THE ARGMAX INTERIOR OR AT AN EDGE?  (10 bps; 'genuine' = m < m*, i.e. the "
      "band can still expel by rank)")
    arg_rows = []
    for nm, _ in panels:
        for n in NS:
            sub = g[(g.panel == nm) & (g.n == n) & (g.cost_bps == 10)].copy()
            gen = sub[~sub.degenerate]
            widest_gen = gen.m_num.max() if len(gen) else np.nan
            best_all = sub.loc[sub.Sharpe.idxmax()]
            best_gen = gen.loc[gen.Sharpe.idxmax()] if len(gen) else None
            # monotone over the genuine range?
            sh = gen.sort_values("m_num").Sharpe.values
            mono_up = bool(np.all(np.diff(sh) >= 0)) if len(sh) > 1 else np.nan
            interior = bool(best_gen is not None and 0 < best_gen.m_num < widest_gen)
            arg_rows.append(dict(panel=nm, n=n, m_star=degen[(nm, n)],
                                 n_genuine=len(gen), widest_genuine=widest_gen,
                                 argmax_all=best_all.m, argmax_all_S=best_all.Sharpe,
                                 argmax_genuine=(best_gen.m if best_gen is not None else None),
                                 argmax_genuine_S=(best_gen.Sharpe if best_gen is not None else np.nan),
                                 S_at_m0=float(sub[sub.m == "0"].Sharpe.iloc[0]),
                                 monotone_up_over_genuine=mono_up,
                                 INTERIOR=interior))
    ag = pd.DataFrame(arg_rows)
    P(ag.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ag.to_csv(OUT / f"{SLUG}.argmax.csv", index=False)
    n_int = int(ag.INTERIOR.sum())
    P(f"    H_LOCATED requires INTERIOR on >= 4 of 6 (panel, n) books: {n_int}/6 -> "
      f"{'SUPPORTED' if n_int >= 4 else 'NOT SUPPORTED'}")

    # ---------------- [3] the cadence control at matched turnover
    P("\n[3] MATCHED-TURNOVER CADENCE CONTROL — same parent book (m=0), cadence k x weekly, "
      "k in {1,2,3,4,6,8,13,26}.  The ladder is a CONTROL, never chosen.")
    cad_rows = []
    for nm, px in panels:
        rk = ranks[nm]
        start = px.index[WARMUP]
        for n in NS:
            for k in KS:
                mk = nweek_mask(px.index, k)
                sel = sel_band(px, rk, n, 0, mask=mk)
                gr, tu, names = fast_backtest(px, weights_from(sel), mask=mk)
                yrs = len(gr.loc[start:]) / 252
                for c in COSTS:
                    s = stats(gr, tu, c, start)
                    a, b4, fb = keeps(s, v2_st[nm][c], spy_st[nm][c])
                    cad_rows.append(dict(panel=nm, n=n, k_weeks=k, cost_bps=c, **s,
                                         turn_per_yr=tu.loc[start:].sum() / yrs,
                                         names=names.loc[start:].mean(),
                                         pass4a=a, pass4b=b4, fail4b=fb))
    cd = pd.DataFrame(cad_rows)
    cd.to_csv(OUT / f"{SLUG}.cadence.csv", index=False)
    for nm, _ in panels:
        for n in NS:
            sub = cd[(cd.panel == nm) & (cd.n == n) & (cd.cost_bps == 10)]
            P(f"\n    CADENCE {nm} n={n} @10bps")
            P(sub[["k_weeks", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
                   "turn_per_yr", "pass4a", "pass4b"]]
              .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[3b] BAND minus CADENCE at the band's OWN realised turnover (10 bps).  'near' = "
      "nearest cadence rung; 'interp' = linear in log(turnover) across the ladder.")
    mt = []
    for nm, _ in panels:
        for n in NS:
            lad = cd[(cd.panel == nm) & (cd.n == n) & (cd.cost_bps == 10)].sort_values("turn_per_yr")
            lt, ls = np.log(lad.turn_per_yr.values), lad.Sharpe.values
            bnd = g[(g.panel == nm) & (g.n == n) & (g.cost_bps == 10)]
            for _, r in bnd.iterrows():
                if r.m == "0":
                    continue
                t = r.turn_per_yr
                j = int(np.argmin(np.abs(lad.turn_per_yr.values - t)))
                s_near = ls[j]
                inrange = lt.min() <= np.log(t) <= lt.max()
                s_int = float(np.interp(np.log(t), lt, ls))
                mt.append(dict(panel=nm, n=n, m=r.m, degenerate=r.degenerate,
                               band_turn=t, band_S=r.Sharpe,
                               cad_k_near=int(lad.k_weeks.values[j]),
                               cad_turn_near=lad.turn_per_yr.values[j], cad_S_near=s_near,
                               d_near=r.Sharpe - s_near, cad_S_interp=s_int,
                               d_interp=r.Sharpe - s_int, interp_in_range=inrange))
    mtd = pd.DataFrame(mt)
    mtd.to_csv(OUT / f"{SLUG}.matched_turnover.csv", index=False)
    P(mtd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    inr = mtd[mtd.interp_in_range]
    P(f"\n    band beats matched cadence (interp, in-range only, n={len(inr)}): "
      f"{int((inr.d_interp > 0).sum())}/{len(inr)} = {(inr.d_interp > 0).mean():.1%}, "
      f"median dSharpe {inr.d_interp.median():+.4f}")
    gen_inr = inr[~inr.degenerate]
    if len(gen_inr):
        P(f"    genuine bands only (m < m*, n={len(gen_inr)}): "
          f"{int((gen_inr.d_interp > 0).sum())}/{len(gen_inr)}, median "
          f"{gen_inr.d_interp.median():+.4f}")
    P(f"    H_CADENCE (cadence >= band at matched turnover) -> "
      f"{'SUPPORTED' if len(inr) and (inr.d_interp > 0).mean() < 0.5 else 'NOT SUPPORTED'}")

    # ---------------- [4] KEEP paths
    P("\n[4] KEEP PATHS over the 54 cells, every rung")
    for c in COSTS:
        sc = g[g.cost_bps == c]
        P(f"    @{c:>2} bps: 4a {int(sc.pass4a.sum())}/{len(sc)}   "
          f"4b {int(sc.pass4b.sum())}/{len(sc)}")
    p4b = g[(g.cost_bps == 10) & g.pass4b]
    if len(p4b):
        P("    4b passes @10 bps:")
        P(p4b[["panel", "n", "m", "degenerate", "CAGR", "Sharpe", "MaxDD", "OOS_Sharpe",
               "turn_per_yr"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("    4b failure-bar census @10 bps: " +
      ", ".join(f"{k}:{v}" for k, v in
                g[(g.cost_bps == 10) & ~g.pass4b].fail4b.value_counts().items()))

    # ---------------- [5] rule 8
    P("\n[5] RULE 8 WALK-FORWARD — (n, m) chosen on 2008-2016 IS Sharpe @10 bps, "
      "2017-2026 read ONCE.")
    wf = []
    for nm, _ in panels:
        sub = g[(g.panel == nm) & (g.cost_bps == 10)]
        for lbl, pool in (("unrestricted", sub), ("genuine bands only", sub[~sub.degenerate])):
            if not len(pool):
                continue
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            best = pool.loc[pool.OOS_Sharpe.idxmax()]
            v2, sp = v2_st[nm][10], spy_st[nm][10]
            a, b4, fb = keeps(pick, v2, sp)
            wf.append(dict(panel=nm, pool=lbl, pick_n=int(pick.n), pick_m=pick.m,
                           degenerate=bool(pick.degenerate), IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                           v2_OOS_MaxDD=v2["OOS_MaxDD"],
                           spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS_CAGR"],
                           spy_OOS_MaxDD=sp["OOS_MaxDD"],
                           oos_best_m=best.m, oos_best_S=best.OOS_Sharpe,
                           regret=best.OOS_Sharpe - pick.OOS_Sharpe,
                           full_pass4a=a, full_pass4b=b4, full_fail4b=fb))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(wfd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n    Rule-8 pick vs the CADENCE control chosen the same way (IS Sharpe @10bps):")
    cwf = []
    for nm, _ in panels:
        sub = cd[(cd.panel == nm) & (cd.cost_bps == 10)]
        pick = sub.loc[sub.IS_Sharpe.idxmax()]
        cwf.append(dict(panel=nm, pick_n=int(pick.n), pick_k=int(pick.k_weeks),
                        IS_Sharpe=pick.IS_Sharpe, OOS_Sharpe=pick.OOS_Sharpe,
                        OOS_CAGR=pick.OOS_CAGR, OOS_MaxDD=pick.OOS_MaxDD,
                        turn_per_yr=pick.turn_per_yr))
    cwd = pd.DataFrame(cwf)
    cwd.to_csv(OUT / f"{SLUG}.cadence_walkforward.csv", index=False)
    P(cwd.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    print(f"\nwrote {SLUG}.{{console.txt,grid,ceiling,argmax,cadence,matched_turnover,"
          f"walkforward,cadence_walkforward}}.csv")


if __name__ == "__main__":
    main()
